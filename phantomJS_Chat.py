# -*- coding: utf-8 -*-
import os
from selenium import webdriver
import time
import json
import random
from tool import encrypt, decrypt, load_json, dump_json, chat_msg, _LOG

BASE_MSG_DICT = {u'你好，很高兴见到你':1, u'我想去旅游':1,u'你会下围棋吗':1,u'给我讲个笑话吧':1,
                u'我只是来打个酱油':1,u'最近有什么好看的电影':1,u'推荐几本好看的小说':1}
BASE_MSG_DICT = load_json('msg_dict_9344.obj')
NEED_KEY = set(['adminUin','adminWxNick','adminWxOpenId','adminWxUid','ava','key','nick','openid','uid','unionid'])


CRYPT_KEY = '66}Y<T8m'
COOKIE_KEY = 'WPD_USER_LOGIN_TOKEN'


def main():
    host_key = '25wx'
    channelId = 3931
    nums = 10

    host = host_key + '.kkyoo.com'
    user_json = '%s_binduid.json' % (host_key,)
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
                         'value': encrypt(json.dumps(user_list[i]), CRYPT_KEY)}


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
    global BASE_MSG_DICT
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
    tmp_msg = random.choice(BASE_MSG_DICT.keys())
    try:
        my_msg = chat_msg(uid, tmp_msg)
    except Exception as ex:
        _LOG( "chat_msg Error %r:%s.\nmsg:%s" % (ex, ex, tmp_msg) )
        return None

    if my_msg:
        BASE_MSG_DICT[my_msg] = BASE_MSG_DICT.get(my_msg, 1) + 1
        chat_input.send_keys(my_msg)
        send_btn.click()
        return my_msg

if __name__ == '__main__':
    try:
        main()
    finally:
        obj_file = 'msg_dict_%d.obj'% (os.getpid())
        dump_json(BASE_MSG_DICT, obj_file)

