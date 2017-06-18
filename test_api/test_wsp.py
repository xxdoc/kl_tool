# -*- coding: utf-8 -*-
import requests
import json
import os
import cPickle

def main():
    api_key = '009ef5d8bec9adb59d2a4fa6dc1d5f37'  # 你的API_KEY
    url = 'http://dyy.aodianyun.com/api/%s/%s'

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
        return res.json()

    def post(api, params,  auth=add_header):
        res = requests.post(url %api, data=params, headers=auth)
        return res.json()

    tmp_admin = post(('CompanyMgr', 'newSubCompany'), {'admin_type': 'jiaoyu', 'billing_type':'liuliang'})
    print tmp_admin
    assert tmp_admin['Flag']==100, '开通客户失败'

    admin_id = tmp_admin['Info']['admin_id']
    print post(('CompanyMgr', 'stateSubCompany'), {'admin_id': admin_id, 'state':2})

    print post(('CompanyMgr', 'stateSubCompany'), {'admin_id': admin_id, 'state':1})

    tmp_room = post(('CompanyMgr', 'newRoomByAdminId'), {'admin_id': admin_id})
    print tmp_room


def fix_api():
    url_file = os.path.join(os.getcwd(), 'access_20170512.log')
    done_file = os.path.join(os.getcwd(), 'done_dict.obj')
    done_dict, url_set = {}, set()
    if os.path.isfile(done_file):
        with open(done_file, 'r') as rf:
            done_dict = cPickle.load(rf)\

    if os.path.isfile(url_file):
        with open(url_file, 'r') as rf:
            for tmp in rf.readlines():
                tmp = tmp.strip()
                if tmp:
                    url_set.add(tmp)

    for url in url_set:
        if url in done_dict:
            continue
        res = requests.get(url)
        print url, res
        if res.ok:
            done_dict.setdefault(url, res.json())
            with open(done_file, 'w') as wf:
                cPickle.dump(done_dict, wf)

if __name__ == '__main__':
    fix_api()

