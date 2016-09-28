# -*- coding: utf-8 -*-
import requests
import json

def main():
    api_key = '0f58d051cccd93078dd8f5b0b9997f31'  # 你的API_KEY
    url = 'http://finance.aodianyun.com/api/%s/%s'

    add_header = {
        'User-Agent': ( 'Mozilla/5.0 (Windows NT 6.1)'
                        ' AppleWebKit/537.36 (KHTML, like Gecko)'
                        ' Chrome/45.0.2454.101 Safari/537.36' ),
        'Authorization': 'dyyadmin:' + api_key,
        "Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        'Accept': 'application/json',
    }

    def get(api, params, auth=add_header):
        res = requests.get(url % api, params=params, headers=auth)
        return res.content

    def post(api, params,  auth=add_header):
        res = requests.post(url %api, data=params, headers=auth)
        return res.content

    print post(('RoomMgr', 'newCaiJingRoom'), {'room_title': '测试API建立房间', })

    print get(('RoomMgr', 'getRoomDmsUserCount'), {'room_id': 1000, })

if __name__ == '__main__':
    main()

