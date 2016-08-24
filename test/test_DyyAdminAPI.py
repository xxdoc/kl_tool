# -*- coding: utf-8 -*-
import requests
import hashlib
import urllib
import json

def md5str(str_in):
    m2 = hashlib.md5()
    m2.update(str_in)
    return m2.hexdigest()

class _Obj(object):
    def __init__(self, data):
        self.__dict__.update(data)

def log(res, key, params, func=json.loads):
    obj = {}
    print key,'>>',
    if res.ok:
        try: obj = func(res.content)
        except ValueError as ex: print 'api:%s@%s result rror:%s!' % (key, params, ex)
        flag = obj.get('Flag', -1)
        print 'OK(%s):' % (flag,) if obj and int(flag)==100 else 'Error(%s):' % (flag,),  \
              obj.get('FlagString', '') if obj else '', '\nargs:', json.dumps(params, indent=2)
        print 'data:',json.dumps(obj, indent=2) if obj else res.content, '\n'
    else:
        print res, res.content.decode('utf-8'), '\n'
    return _Obj(obj)

def main():
    host = '25.kkyoo.com'  # 修改为需要测试的域名
    host = 'my.app'

    auth_dict = {'auth':'dyyAdmin:fb4c1c79548142d11f595634ee62fbbb'}  # 修改为需要测试的auth

    api_url = 'http://' + host + '/api/%s/%s'
    add_header = {
                'User-Agent': ('Mozilla/5.0 (Windows NT 6.1)'
                                ' AppleWebKit/537.36 (KHTML, like Gecko)'
                                ' Chrome/45.0.2454.101 Safari/537.36'),
                'Authorization': auth_dict['auth'],
                "Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                'Accept':'application/json'}

    def get(api, params, auth=add_header):
        res = requests.get(api_url % api, params=params, headers=auth)
        return log(res, api, params)

    def post(api, params,  auth=add_header):
        res = requests.post(api_url % api, data=params, headers=auth)
        return log(res, api, params)

    get(('AdminMgr', 'getSelfSubAdminDictAll'), {})

    get(('AdminMgr', 'reSetAdminApiKey'), {'admin_id':115})

    post(('AdminMgr', 'reSetAdminApiKey'), {'admin_id':116})

    post(('AdminMgr', 'reSetAdminApiKey'), {'admin_id':141})

    post(('AdminMgr', 'getAdminInfo'), {'admin_id':141})

    post(('AdminMgr', 'getAdminInfo'), {'admin_id':30})

if __name__ == '__main__':
    main()

