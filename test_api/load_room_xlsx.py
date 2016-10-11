# -*- coding: utf-8 -*-
import requests
import json
import xlrd
from pyExcelerator import *

def main():
    api_key = '80cf9723bac297e1366ff5958978b0ca'  # 你的API_KEY

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
        if res.ok:
            return res.json()
        print res.content

    def post(api, params,  auth=add_header):
        res = requests.post(url %api, data=params, headers=auth)
        if res.ok:
            return res.json()
        print res.content


    bk = xlrd.open_workbook("room_data.xlsx")
    sh = bk.sheet_by_name(u"证券公司MCS录入")

    w = Workbook()
    ws = w.add_sheet(u"证券公司MCS录入")
    need = {'room_id':u'房间ID', 'room_title':u'房间标题', 'mcs_name':u'主播账号', 'mcs_pwd':u'主播密码', 'lss_app':u'流媒体app', 'stream':u'流媒体stream', 'rtmp_url':u'rtmp地址', 'hls_url':u'hls地址','aodian_id':u'奥点云UIN'}
    ret_idx = 7
    [ws.write(0, i, v) for i,v in enumerate(sh.row_values(0))]
    ws.write(0, ret_idx-1, u'结果')
    [ws.write(0, ret_idx+ti, need[tkey]) for ti,tkey in enumerate(need)]


    for idx in range(1, sh.nrows):
        row_data = sh.row_values(idx)
        if not row_data or not row_data[0]: break
        tmp = post(('RoomMgr', 'newCaiJingRoom'), {'room_title': row_data[2].encode('utf-8'), 'mcs_name':str(row_data[0]), 'mcs_pwd':'123456', 'lss_player_type':'aodianplayer'})
        print tmp.get('FlagString', '')
        [ws.write(idx, i, v) for i,v in enumerate(row_data)]
        ws.write(idx, ret_idx-1, tmp.get('FlagString', ''))
        if tmp and tmp.get('Flag', 0)==100:
            rst = [tmp['Info'].get(key, '') for key in need]
            [ws.write(idx, ret_idx+i, v) for i,v in enumerate(rst)]

    w.save('out.xlsx')

    return



if __name__ == '__main__':
    main()

