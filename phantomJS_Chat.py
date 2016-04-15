# -*- coding: utf-8 -*-
import os
from selenium import webdriver
import time
import json
import urllib
import random
from tool import encrypt, decrypt, load_json, dump_json, chat_msg, _LOG

BASE_MSG_DICT = {u'你好，很高兴见到你':1, u'我想去旅游':1,u'你会下围棋吗':1,u'给我讲个笑话吧':1,
                u'我只是来打个酱油':1,u'最近有什么好看的电影':1,u'推荐几本好看的小说':1}

NEED_KEY = set(['adminUin','adminWxNick','adminWxOpenId','adminWxUid','ava','key','nick','openid','uid','unionid'])


CRYPT_KEY = '66}Y<T8m'
COOKIE_KEY = 'WPD_USER_LOGIN_TOKEN'


def main():
    host_key = '25wx'
    channelId = 3359
    nums = 10

    host = host_key + '.kkyoo.com'
    user_json = '%s_binduid.json' % (host_key,)
    USER_DATA = [{k:v for k,v in item.items() if k in NEED_KEY} for item in load_json(user_json)]

    wait_m = 10
    user_list = [i for i in USER_DATA if i['uid']>=10050]

    del_list = ['content_left', 'content_middle', 'live_bottom', 'paycenter', 'login', 'sitebar']
    url = 'http://%s/dev_wx/wsp/index.php?r=web/livestream&id=%s' % (host, channelId)
    driver_list = []
    for i in range(nums):
        uid, nick = user_list[i]['uid'], urllib.unquote(str(user_list[i]['nick'])).decode('utf-8')
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
        del_elements_by_class_name(tmp, del_list)
        driver_list.append( (tmp, uid) )
        _LOG('add %s<%s>' % (nick, uid))

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

def del_elements_by_class_name(tmp, del_list):
    try:
        js_str = ';'.join(["$('.%s').remove()" % (cls_str,) for cls_str in del_list]) + ';'
        tmp.execute_script( js_str )
    except:
        pass

def send_msg(drv, uid):
    global BASE_MSG_DICT
    _first = lambda ll:ll[0] if ll and isinstance(ll, (list,tuple)) else None
    _last = lambda ll:ll[-1] if ll and isinstance(ll, (list,tuple)) else None
    chat_input = _first(drv.find_elements_by_class_name('chat_input'))
    send_btn = _first(drv.find_elements_by_class_name('send_btn'))
    if not chat_input or not send_btn:
        return None

    all_cunt = len(BASE_MSG_DICT)
    tmp_list = minTopK(BASE_MSG_DICT.items(), 10)
    tmp_msg, cunt = random.choice(tmp_list)
    try:
        my_msg = chat_msg(uid, tmp_msg)
    except Exception as ex:
        _LOG( "chat_msg Error %r:%s.\nmsg:%s" % (ex, ex, tmp_msg) )
        return None

    my_msg = my_msg if my_msg else tmp_msg
    if my_msg:
        _LOG( '%d...%s <%d>{%d} (%d)' % (uid, tmp_msg, BASE_MSG_DICT[tmp_msg], len(tmp_list), len(BASE_MSG_DICT)) )
        BASE_MSG_DICT[tmp_msg] += 1
        BASE_MSG_DICT[my_msg] = BASE_MSG_DICT.get(my_msg, -1) + 1
        _LOG( '%d>>>%s <%d> (%d)' % (uid, my_msg, BASE_MSG_DICT[my_msg], len(BASE_MSG_DICT)) )
        chat_input.send_keys(my_msg)
        send_btn.click()
        return my_msg

def minTopK(ll_in, nums):
    nums = int(nums)+1
    ll_in.sort(key=lambda e:e[1])
    tmp = ll_in[:nums]
    if tmp:
        tmp.extend([ii for ii in ll_in[nums:] if ii[1]== tmp[-1][1] ])
    return tmp

if __name__ == '__main__':
    print "MAIN RUN PID:", os.getpid()
    read_file = 'msg_dict_8956.obj'
    print "MAIN START READ FILE:", read_file
    BASE_MSG_DICT = load_json(read_file)
    main()


