# -*- coding: utf-8 -*-
from gevent import monkey; monkey.patch_all()

import os
import requests
import time
import json
import random
import gevent
from gevent import pool

from tool import encrypt, decrypt, load_json, dump_json, chat_msg, _LOG, get_dir_file

BASE_MSG_DICT = {u'你好，很高兴见到你':1, u'我想去旅游':1,u'你会下围棋吗':1,u'给我讲个笑话吧':1,
                u'我只是来打个酱油':1,u'最近有什么好看的电影':1,u'推荐几本好看的小说':1}

class Client(object):

    def __init__(self, uid, name, room_id, dms='', api_key='', seq=60):
        self.uid = uid
        self.name = name
        self.room_id = room_id
        self.dms = dms
        self.api_key = api_key
        self.seq = seq

    def run(self):
        for _ in range(self.seq):
            send_msg(self.dms, self.room_id, self.api_key, self.uid, self.name)
            now = int(time.time() / 10 )
            TIMER_MAP.setdefault(now, 0)
            TIMER_MAP[now] += 1
            # _LOG("last 10 sec num:%d" % (TIMER_MAP.get(now - 1, 0), ))

TIMER_MAP = {}

def main():
    wait_m = 20
    room_id = 1016
    user_list = [{'uid':1000007000 + i, 'name': 't3_%03d' % (i, )} for i in range(1, 7)]
    dms = 'dms.wenshunsoft.com'
    dms = '127.0.0.1'
    api_key = '2b284b8794e233e1f24b0c1fff2c5444'

    u_list = [Client(u['uid'], u['name'], room_id, dms, api_key) for u in user_list]

    u_list = u_list

    save_file = 'msg_dict_%d.obj'% (os.getpid())
    for i in range(wait_m*60):
        if len(u_list) == 1:
            u_list[0].seq = 1
            u_list[0].run()
            time.sleep(0.2)
            continue

        try:
            gevent.Timeout(62).start()
            func_pool = pool.Pool(len(user_list))
            [func_pool.spawn(u.run) for u in u_list]
            func_pool.join()
        except gevent.Timeout as ex:
            pass

        _LOG(u'minute ...')
        with open(save_file, 'w') as wf:
            json.dump(BASE_MSG_DICT, wf)

    _LOG(u'end')


_tc = (int(time.mktime(time.localtime())) % 100000) / 1000
_id = random.randint(0, _tc) * 1000 + 8000

ROBOT_ERROR = 0

def send_msg(dms, room_id, api_key, uid, name):
    global BASE_MSG_DICT, _id, ROBOT_ERROR
    my_msg, topic = '', 'r_test_chat_%d' % (room_id, )

    tmp_list = minTopK(BASE_MSG_DICT.items(), 10)
    tmp_msg, _ = random.choice(tmp_list)
    try:
        my_msg = chat_msg(uid, tmp_msg) if ROBOT_ERROR < 5 else ''
    except Exception as ex:
        ROBOT_ERROR += 1
        _LOG( u"chat_msg Error %r:%s.\nmsg:%s" % (ex, ex, tmp_msg) )

    my_msg = my_msg if my_msg else tmp_msg
    if my_msg:
        # _LOG( u'%d...%s <%d>{%d} (%d)' % (uid, tmp_msg, BASE_MSG_DICT[tmp_msg], len(tmp_list), len(BASE_MSG_DICT)) )
        BASE_MSG_DICT[tmp_msg] += 1
        BASE_MSG_DICT[my_msg] = BASE_MSG_DICT.get(my_msg, -1) + 1
        # _LOG( u'%d>>>%s <%d> (%d)' % (uid, my_msg, BASE_MSG_DICT[my_msg], len(BASE_MSG_DICT)) )
        time_str = time.strftime("%H:%M", time.localtime())
        _id += 1
        my_msg = '[%d] ' % (_id,) + my_msg
        payload = {"uid":uid,"name":name,"type":1,"userType":500,"message":my_msg,"send_roomid":room_id,"plat":"pc","vtype":0,"font_size":"14","font_weight":0,"font_color":"#333","is_audited":1,"origin_audit":1,"room_id":0,"id":_id,"hasFilter":0,"time":time_str,"sendUid":uid,"cmd":"chat"}
        ret = dms_pub(dms, topic, api_key, payload)
        if ret:
            _LOG( u'%d>>>%s <%d>' % (uid, my_msg, _id) )

def dms_pub(dms, topic, api_key, payload):
    query_url = "http://%s:9123/mqtt/pub?topic=%s&qos=%d&key=%s" % (dms, topic, 0, api_key)
    try:
        res = requests.post(query_url, {'payload': json.dumps(payload)})
        return res.ok
    except Exception as ex:
        _LOG( u"dms_pub Error %r:%s." % (ex, ex))
        return False

def minTopK(ll_in, nums):
    nums = int(nums)+1
    ll_in.sort(key=lambda e:e[1])
    tmp = ll_in[:nums]
    if tmp:
        tmp.extend([ii for ii in ll_in[nums:] if ii[1]== tmp[-1][1] ])
    return tmp

if __name__ == '__main__':
    print "MAIN RUN PID:", os.getpid()
    obj_list = get_dir_file(os.getcwd(), is_ok=lambda x:x.endswith('.obj'), key=lambda x:x[1]['size'])
    read_file = obj_list[-1][0]
    print "MAIN START READ FILE:", read_file
    BASE_MSG_DICT = load_json(read_file)
    main()


