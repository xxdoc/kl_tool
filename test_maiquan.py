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

def log(res, key, params, func=None):
    obj = {}
    print key,'>>',
    if res.ok:
        try: obj = res.json()
        except ValueError as ex: raise ValueError('api:%s@%s result not json!' % (key, params))
        if func:
            obj = func(obj)
        flag = obj.get('Flag', 'no-flag')
        print 'OK(%s):' % (flag,) if obj and flag==100 else 'Error(%s):' % (flag,),  \
              obj.get('FlagString', '') if obj else '', '  args:', params
        print json.dumps(obj, indent=2) if obj else res.content, '\n'
    else:
        print res, res.content.decode('utf-8'), '\n'
    return _Obj(obj)

def main():
    host = 'api.91mq.com'
    api = 'http://' + host + '/ktvwebservice.asmx/%s'
    add_header = {
                'User-Agent': ('Mozilla/5.0 (Windows NT 6.1)'
                                ' AppleWebKit/537.36 (KHTML, like Gecko)'
                                ' Chrome/45.0.2454.101 Safari/537.36'),
                "Content-type": "application/json; charset=UTF-8",
                'Accept':'application/json'}

    def get(key, params, auth=add_header):
        res = requests.get(api % (key,), params=params, headers=auth)
        return log(res, key, params)

    def post(key, params, auth=add_header):
        res = requests.post(api % (key,), data=params, headers=auth)
        return log(res, key, params)

    def post_json(key, params, auth=add_header):
        res = requests.post(api % (key,), data=json.dumps(params), headers=auth)
        return log(res, key, params, func=lambda x:json.loads(x['d']) )

    post_json('UserLOgin', {'parameter':{'Tag':'LoginRoomAuth','Uin':123456,'SessionKey':'WwOMtkdkDpbsEnVWEbFGm6x1Oi5FHHBG','RoomId':222222}})

if __name__ == '__main__':
    main()
