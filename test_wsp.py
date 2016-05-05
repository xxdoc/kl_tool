# -*- coding: utf-8 -*-
import requests
import hashlib
import json

def md5str(str_in):
    m2 = hashlib.md5()
    m2.update(str_in)
    return m2.hexdigest()

def main():
    host = '25wx.kkyoo.com'  # 修改为需要测试的域名
    wsp_test = {'wspKey':"6c9887da7c41952c406d82e377f7bc65",}  # 修改为需要测试的wspKey

    api = 'http://' + host + '/dev_wx/wpd/index.php?r=console/mqApi&api=%s'
    add_header = {
                'User-Agent': ('Mozilla/5.0 (Windows NT 6.1)'
                                ' AppleWebKit/537.36 (KHTML, like Gecko)'
                                ' Chrome/45.0.2454.101 Safari/537.36'),
                'Authorization': md5str('wsp_' + wsp_test['wspKey']),
                "Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                'Accept':'application/json'}

    def log(res, key, params):
        obj = {}
        print key,'>>',
        if res.ok:
            try: obj = res.json()
            except ValueError as ex: pass
            print 'OK:' if obj and obj.get('Flag', 0)==100 else 'Error:',  obj.get('FlagString', '') if obj else ''
            print json.dumps(obj, indent=2) if obj else res.content, '\n'
        else:
            print res, '\n'

    def get(key, params):
        res = requests.get(api % (key,), params=params, headers=add_header)
        return log(res, key, params)

    def post(key, params):
        res = requests.post(api % (key,), data=params, headers=add_header)
        return log(res, key, params)


    """
    $public_api = array('channellist');
    $private_api = array( 'newchannel');
    $action_api = array( 'channelinfo', 'getgaps', 'addgaps', 'deletegaps', 'getblacklists', 'addblacklists', 'deleteblacklists' );
    """
    get('channellist', {'page':1, 'p_num':2})

    get('newchannel', {'uid':10097, 'state':1, 'viewlimit':100, 'real_name':'我是测试', 'qq':123456, 'tel':1212})

    get('channelinfo', {'channelId':2688})
    get('getgaps', {'channelId':3757})
    get('getblacklists', {'channelId':3757})
    post('addgaps', {'channelId':3757, 'uid':10020})
    post('deletegaps', {'channelId':3757, 'uid':10021})
    post('addblacklists', {'channelId':3757, 'uid':10031})
    post('deleteblacklists', {'channelId':3757, 'uid':10050})


if __name__ == '__main__':
    main()

