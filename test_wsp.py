# -*- coding: utf-8 -*-
import requests
import base64
import json

def main():
    wx25_wsp = {'wspKey':"6c9887da7c41952c406d82e377f7bc65",}
    add_key = '&'.join(['%s=%s' % (key,val) for key,val in wx25_wsp.items()])
    add_header = {
                'Authorization': 'wsp ' + base64.encodestring(add_key),
                'Content-Type': 'application/json',}

    def get(url):
        res = requests.get(url, headers=add_header)
        if res.ok:
            return res.json()
        else:
            print res
            return res.content

    def post(url, data):
        res = requests.post(url, headers=add_header, data=data)
        if res.ok:
            return res.json()
        else:
            return res.content

    gaps_list = 'http://api.wx.aodianyun.com:8800/v3/channels/3757/gaps'
    is_gaps = 'http://api.wx.aodianyun.com:8800/v3/channels/3757/gaps/1000001104'

    print get(gaps_list)
    print get(is_gaps)

    add_gaps = 'http://api.wx.aodianyun.com:8800/v3/channels/3757/gaps/1000001104'

    print post(add_gaps, json.dumps({'nick':'test123','uid':'1000001104'}))


if __name__ == '__main__':
    main()


"""
use dms
db.peidui.ensureIndex({"topic":1})
db.peidui.ensureIndex({"time":1})
db.peidui.ensureIndex({"msg":1})
db.peidui.getIndexes()
"""