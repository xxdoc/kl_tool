# -*- coding: utf-8 -*-
import requests
import hashlib
import json

def md5str(str_in):
    m2 = hashlib.md5()
    m2.update(str_in)
    return m2.hexdigest()

class _Obj(object):
    def __init__(self, data):
        self.__dict__.update(data)

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
            except ValueError as ex: raise ValueError('api:%s@%s result not json!' % (key, params))
            flag = obj.get('Flag', 'no-flag')
            print 'OK(%s):' % (flag,) if obj and flag==100 else 'Error(%s):' % (flag,),  \
                  obj.get('FlagString', '') if obj else '', '  args:', params
            print json.dumps(obj, indent=2) if obj else res.content, '\n'
        else:
            print res, '\n'
        return _Obj(obj)

    def get(key, params, auth=add_header):
        res = requests.get(api % (key,), params=params, headers=auth)
        return log(res, key, params)

    def post(key, params,  auth=add_header):
        res = requests.post(api % (key,), data=params, headers=auth)
        return log(res, key, params)


    """
    $private_api = array('channellist', 'newchannel');
    $action_api = array( 'channelinfo', 'getgaps', 'addgaps', 'deletegaps', 'getblacklists',
                         'addblacklists', 'deleteblacklists', 'addmgr', 'delmgr', 'getmgrlists' );
    """
    get('channellist', {'page':1, 'num':2})
    get('newchannel', {'uid':10097, 'state':1, 'viewlimit':100, 'real_name':'我是测试', 'qq':123456, 'tel':1212})
    get('channelinfo', {'channelId':2688})

    get('getgaps', {'channelId':3757})
    post('addgaps', {'channelId':3757, 'uid':10020})
    post('deletegaps', {'channelId':3757, 'uid':10020})

    get('getblacklists', {'channelId':3757})
    post('addblacklists', {'channelId':3757, 'uid':10031})
    post('deleteblacklists', {'channelId':3757, 'uid':10031})

    get('getmgrlists', {'channelId':3757})
    post('addmgr', {'channelId':3757, 'uid':10031})
    post('delmgr', {'channelId':3757, 'uid':10031})

    ##错误测试
    assert get('channelinfo', {'channelId':3757}, {'Authorization':'1234'}).Flag==109

    assert get('channelinf', {'channelId':3757}).Flag==111

    assert get('channelinfo', {'channelId':666666}).Flag==108

    assert get('newchannel', {'uid':9999999, 'state':1, 'viewlimit':100, 'real_name':'我是测试', 'qq':123456, 'tel':1212}).Flag==1004
    assert get('newchannel', {'uid':10042, 'viewlimit':100, 'real_name':'我是测试', 'qq':123456, 'tel':1212}).Flag==101

    assert get('channelinfo', {'channelid':666666}).Flag==101
    assert post('addmgr', {'channelId':3757, 'uid':9999999}).Flag==1004
    assert post('addmgr', {'channelId':9999999, 'uid':10031}).Flag==108

if __name__ == '__main__':
    main()

