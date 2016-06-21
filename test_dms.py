# -*- coding: utf-8 -*-
import urllib
import pymongo
from tool import load_obj, save_obj, get_json, _LOG, s2t
import requests
import json
##MONGODB = pymongo.MongoClient('127.0.0.1', 27017)
##MONGODB_CUR = MONGODB.dms.peidui

def main():
    peidui_dms = {'pub_key':'pub_45c328b9a41ad3d8e03e7b0def64f740',
            'sub_key':'sub_98fdec0e596145633a9735c8594369e0',
            's_key':'s_5c5d76ab1969382c093b5acb5ad97d2f',}


    wx25_dms = {'pub_key':"pub_8665bcf8fc7bdcffa983e7d7d5aaadd4",
                'sub_key':"sub_72f43c9452ba53c313edfe64e1c7eb61",
                's_key':'s_5b6e3a613a099609844c9b07fd1c0cdf',}

    test_dms = { 's_key':'s_8b9c0af9ee2be103ccb31189d6c2ec93',}



    #s_key = peidui_dms['s_key']
    s_key = test_dms['s_key']
    add_h = {'Authorization':'dms ' + s_key, 'Content-Type': 'application/json'}

    topic = 'chat_97'
    url = 'http://api.dms.aodianyun.com/v1/messages/%s' % (topic)
    msg = json.dumps({'cmd':'test', 'data':'dajdhuwiadh'})
    res = requests.post(url, data=json.dumps({'body':msg}), headers=add_h)
    print res
    print res.content
    a=1
    return True

    topic = ''
    s_time = '2016-03-31 23:00:00'
    e_time = '2016-03-31 23:03:59'
    all_list = get_data(add_h, s_time, e_time, topic)
    _LOG("All get dms:%s" % (len(all_list),))
    c = {}
    for i in all_list:
        key = i.get('topic', 'null')
        c[key] = c.get(key, 0) + 1
    a = c.items()
    a.sort(key=lambda i:i[1])
    for (key,num) in a:
        print key,',',num

def get_data(add_h, s_time, e_time, topic='', per_num=100):
    find_dict = {
        'skip': 0,
        'num': per_num,
        'topic': topic,
        'tartTime': s2t(s_time),
        'endTime': s2t(e_time)}
    obj_file = ('%s_%s_%s.obj' % (topic or 'all',s_time, e_time)).replace(':','').replace(' ','_')
    all_list = []
    while 1:
        url = 'http://api.dms.aodianyun.com/v2/historys?'+urllib.urlencode(find_dict)
        json_obj = get_json(url, add_h)
        if len(json_obj)==0:
            break
##        try:
##            MONGODB_CUR.insert_many(json_obj)
##        except pymongo.errors.PyMongoError as ex:
##            _LOG( "PyMongoError %r:%s." % (ex, ex) )
        find_dict['skip'] += per_num
        all_list.extend(json_obj)
    save_obj(all_list, obj_file)
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