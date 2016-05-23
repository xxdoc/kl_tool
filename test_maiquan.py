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

    """UserLogin, LoginStockRoom"""
    #post_json('UserLogin', {'parameter':{'Tag':'LoginRoomAuth','Uin':62853880,'SessionKey':'JVZeD0YEqPJ67r8iotLCpxnyTg4LRUYg','RoomId':0}})

    post_json('LoginStockRoom', {'parameter':{'Tag':'LoginRoomPwd','NeedFlockVip':1,'Uin':62853880,'PassWord':md5str('123456'),'RoomId':100013}})


if __name__ == '__main__':
    main()
