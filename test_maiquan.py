# -*- coding: utf-8 -*-
import requests
import hashlib
import json
from test_wsp import log, md5str

url = 'http://120.4640.lcps.aodianyun.com:3000/switch'
json_str = '{"formatIndex":0,"enable":true,"publishURL":["rtmp://1436.lsspublish.aodianyun.com/dyy_81/KMGjT"],"playURL":"","videoSize":"1280x720","videoBitrate":"1500k","videoCBR":true,"audioBitrate":"48k"}'
json_str = '{"paraArray":[{"w":1280,"h":720,"x":0,"y":0,"v":100,"z":2},{"w":1280,"h":720,"x":1280,"y":720,"v":0,"z":0},{"w":1280,"h":720,"x":1280,"y":720,"v":0,"z":3},{"w":1280,"h":720,"x":1280,"y":720,"v":0,"z":1}]}'
json_str = '{"paraArray":[{"w":1280,"h":720,"x":0,"y":0,"v":100,"z":3},{"w":1280,"h":720,"x":1280,"y":720,"v":0,"z":1},{"w":1280,"h":720,"x":1280,"y":720,"v":0,"z":2},{"w":1280,"h":720,"x":1280,"y":720,"v":0,"z":0}]}'
res = requests.post(url, data=json_str)
print res
print res.content
a=1

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

    post_json('LoginStockRoom', {'parameter':{'Tag':'LoginRoomPwd','NeedFlockVip':1,'Uin':62853878,'PassWord':md5str('yykfq0916'),'RoomId':100025, 'RoomType':2}})


if __name__ == '__main__':
    #main()
    pass
