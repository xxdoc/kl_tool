# -*- coding: utf-8 -*-
import requests
import hashlib
import json
from test_wsp import log, md5str

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
        return log(res, key, params, func=lambda x:json.loads(json.loads(x)['d']) )

    post_json('UserLOgin', {'parameter':{'Tag':'LoginRoomAuth','Uin':123456,'SessionKey':'WwOMtkdkDpbsEnVWEbFGm6x1Oi5FHHBG','RoomId':222222}})

if __name__ == '__main__':
    main()
