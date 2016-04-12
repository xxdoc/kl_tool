# -*- coding: utf-8 -*-
from selenium import webdriver
import time
import json
from tool import encrypt, decrypt, load_json, dump_json, chat_msg, _LOG

NEED_KEY = set(['adminUin','adminWxNick','adminWxOpenId','adminWxUid','ava','key','nick','openid','uid','unionid'])
CRYPT_KEY = '66}Y<T8m'
COOKIE_KEY = 'WPD_USER_LOGIN_TOKEN'



def main():
    host_key = '25wx'
    channelId = 3359
    nums = 20

    host = host_key + '.kkyoo.com'
    user_json = '%s_binduid.json' % (host_key,)
    USER_DATA = [{k:v for k,v in item.items() if k in NEED_KEY} for item in load_json(user_json)]

    wait_m = 10
    user_list = [i for i in USER_DATA if i['uid']>=10050]


    url = 'http://%s/dev_wx/wsp/index.php?r=web/livestream&id=%s' % (host, channelId)
    driver_list = []
    for i in range(nums):
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
        driver_list.append(tmp)
        _LOG('add %s' % (user_list[i]['uid']))

    _LOG('wait')
    for i in range(wait_m):
        _LOG('...')
        time.sleep(60)

    for item in driver_list:
        try:
            item.close()
            item.quit()
        except:
            pass
    _LOG('end')



if __name__ == '__main__':
    main()

