# -*- coding: utf-8 -*-
import sys
import os
from selenium import webdriver
import time
import datetime
import base64
import json
import urllib
import urllib2
import random

BASE_MSG_DICT = {u'你好，很高兴见到你':1, u'我想去旅游':1,u'你会下围棋吗':1,u'给我讲个笑话吧':1,
                u'我只是来打个酱油':1,u'最近有什么好看的电影':1,u'推荐几本好看的小说':1}


TEST = 'emy8JT1<aYW}Q6i6OiIxMDAyNSIsImFkbWluVWluIjo3MTgxLCJhZG1pbld4VWlkIjoib1RmQXl1RkZIRmJveTU2ZjNtT202bmhqem5JQSIsImFkbWluV3hPcGVuSWQiOiJvb1FJUXdZSEdncEpBVGdLMzRrbUdFZGdBQnlvIiwiYWRtaW5XeE5pY2siOiIlRTklQTMlOTgiLCJrZXkiOiI2Yzk4ODdkYTdjNDE5NTJjNDA2ZDgyZTM3N2Y3YmM2NSIsIm9wZW5pZCI6Im9mM1J0dDViY3YzbnlhblAyd2Z4ZURMS3NMTU0iLCJ1bmlvbmlkIjoib1RmQXl1QUJRaG5EVWpoR0ttcFQ5a0xjaXo2byIsIm5pY2siOiJcdTk2M2ZcdTVmYjciLCJhdmEiOiJodHRwOlwvXC93eC5xbG9nby5jblwvbW1vcGVuXC9iTXVtb0pLVGY0eXc2RGFaZHlpY25DUDJ5TDFiVXNyZEs0c013dEltREpqOFRBaWN4SHBkV1h2VEZ6ZDB1bUZNZXhIdEFRNWNIVFVyWDJZNXh3eDUweWRBXC8wIn0O0O0O'
CRYPT_KEY = '66}Y<T8m'
COOKIE_KEY = 'WPD_USER_LOGIN_TOKEN'

def load_json(json_file):
    with open(json_file, 'r') as rf:
        return json.load(rf)

BASE_MSG_DICT = load_json('msg_dict_9344.obj')


def dump_json(obj, json_file):
    with open(json_file, 'w') as wf:
        json.dump(obj, wf)

def encrypt(str_in='', skey=CRYPT_KEY):
    skey = skey[::-1]
    strArr = [i for i in base64.b64encode(str_in)]
    strCount = len(strArr)
    for (key, value) in enumerate(skey):
        if key < strCount:
            strArr[key] += value
    return ''.join(strArr).replace('=', 'O0O0O')

def decrypt(str_in='', skey=CRYPT_KEY):
    skey = skey[::-1]
    strArr = [a+b for (a,b) in zip(*([iter(str_in.replace('O0O0O', '='))] * 2))]
    strCount = len(strArr);
    for (key, value) in enumerate(skey):
        if (key < strCount):
            strArr[key] = strArr[key].rstrip(value)
    return base64.b64decode(''.join(strArr))




def main():
    host_key = '25wx'
    channelId = 3931
    nums = 10

    host = host_key + '.kkyoo.com'
    user_json = '%s_binduid.json' % (host_key,)
    NEED_KEY = set(json.loads(decrypt(TEST)).keys())
    USER_DATA = [{k:v for k,v in item.items() if k in NEED_KEY} for item in load_json(user_json)]

    wait_m = 10
    user_list = [i for i in USER_DATA if i['uid']>=10050]


    url = 'http://%s/dev_wx/wsp/index.php?r=web/livestream&id=%s' % (host, channelId)
    driver_list = []
    for i in range(nums):
        uid = user_list[i]['uid']
        time_s = int(time.mktime(time.localtime())) + 3600
        my_cookies = {   'domain': '.%s' % (host,),
                         'expires': time.ctime(time_s),
                         'expiry': time_s,
                         'httponly': False,
                         'name': COOKIE_KEY,
                         'path': '/',
                         'secure': False,
                         'value': encrypt(json.dumps(user_list[i]))}


        tmp = webdriver.PhantomJS()
        tmp.add_cookie(my_cookies)
        tmp.get(url)
        send_msg(tmp, uid)
        driver_list.append( (tmp, uid) )
        _LOG('add %s<%s>' % (user_list[i]['nick'], uid))

    _LOG('wait')
    for i in range(wait_m*60):
        for (item, uid) in driver_list:
            send_msg(item, uid)

    for (item, uid) in driver_list:
        try:
            item.close()
            item.quit()
        except:
            pass
    _LOG('end')


def send_msg(drv, uid):
    global BASE_MSG_LIST
    _first = lambda ll:ll[0] if ll and isinstance(ll, (list,tuple)) else None
    _last = lambda ll:ll[-1] if ll and isinstance(ll, (list,tuple)) else None
    chat_input = _first(drv.find_elements_by_class_name('chat_input'))
    send_btn = _first(drv.find_elements_by_class_name('send_btn'))
    if not chat_input or not send_btn:
        return None
    list_tmp = [i.text for i in drv.find_elements_by_class_name('message-content')]
    for i in list_tmp:
        BASE_MSG_DICT[i] = BASE_MSG_DICT.get(i, 1) + 1

    _LOG('...<%d>' % (len(BASE_MSG_DICT)))
    try:
        my_msg = chat_msg(uid, random.choice(BASE_MSG_DICT.keys()))
    except:
        return None

    if my_msg:
        BASE_MSG_DICT[my_msg] = BASE_MSG_DICT.get(my_msg, 1) + 1
        chat_input.send_keys(my_msg)
        send_btn.click()
        return my_msg

def _LOG(msg_in, time_now=True, new_line=True):
    if time_now:
        time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        msg = '%s => %s' % (time_str, msg_in)
    if getattr(_LOG, 'log_file', None):
        _LOG.log_file.write(msg+'\n')
        _LOG.log_file.flush()

    if new_line:
        print msg
    else:
        print msg,


def chat_msg(uid, msg, _loc='杭州市', _key="3b8f3f656692f998f6625a0a8d50270e"):
    api_doc = {100000:'文本类', 200000:'链接类', 302000:'新闻类',
                308000:'菜谱类', 313000:'（儿童版）儿歌类', 314000:'（儿童版）'}
    msg = msg.encode('utf-8')
    args = {'key':_key, 'info':msg, 'loc':_loc, 'userid':uid}
    url = r"http://www.tuling123.com/openapi/api?" + urllib.urlencode(args)
    obj = json.loads(urllib2.urlopen(url).read())
    if obj.get('code', 0) in api_doc:
        return obj.get('text', None)
    else:
        return None


if __name__ == '__main__':
    try:
        main()
    finally:
        obj_file = 'msg_dict_%d.obj'% (os.getpid())
        dump_json(BASE_MSG_DICT, obj_file)

