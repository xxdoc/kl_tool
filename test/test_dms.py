# -*- coding: utf-8 -*-
import urllib
import pymongo
from tool import load_obj, save_obj, get_json, _LOG, s2t, dump_json
import requests
import json


def main():

    test_dms = {"s_key": "s_d4c4f7b5f8f997a343e5cf0af49733e5",}

    add_h = {'Authorization':'dms ' + test_dms['s_key'], 'Content-Type': 'application/json'}

    s_time = '2016-09-22 00:00:00'
    e_time = '2016-09-22 23:59:59'
    all_list = get_data(add_h, s_time, e_time, '')
    _LOG("All get dms:%s" % (len(all_list),))
    c = {}
    for i in all_list:
        key = i.get('topic', 'null')
        c[key] = c.get(key, 0) + 1
    a = c.items()
    a.sort(key=lambda i:i[1])
    print "all:%s" % (len(all_list), )
    for (key,num) in a:
        print key,':',num

def get_data(add_h, s_time, e_time, topic='', per_num=200):
    find_dict = {
        'skip': 0,
        'num': per_num,
        'topic': topic,
        'tartTime': s2t(s_time),
        'endTime': s2t(e_time)}
    obj_file = ('%s_%s_%s.json' % (topic or 'all',s_time, e_time)).replace(':','').replace(' ','_')
    all_list = []
    while 1:
        url = 'http://api.dms.aodianyun.com/v2/historys?'+urllib.urlencode(find_dict)
        json_obj = get_json(url, add_h)
        if len(json_obj)==0:
            break

        find_dict['skip'] += per_num
        all_list.extend(json_obj)
    dump_json(all_list, obj_file)
    return all_list


if __name__ == '__main__':
    main()


"""
use dms
db.peidui.ensureIndex({"topic":1})
db.peidui.ensureIndex({"time":1})
db.peidui.ensureIndex({"msg":1})
db.peidui.getIndexes()
"""