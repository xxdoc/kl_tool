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
    host = 'my.app'  # 修改为需要测试的域名

    wsp_test = {'wspKey':"bfb1ab1a6c4e964fe8b5994895e5f8eb",}  # 修改为需要测试的wspKey


    api = 'http://' + host + '/api/MaiQuanRoomAssist/%s'
    add_header = {
                'User-Agent': ('Mozilla/5.0 (Windows NT 6.1)'
                                ' AppleWebKit/537.36 (KHTML, like Gecko)'
                                ' Chrome/45.0.2454.101 Safari/537.36'),
                'Authorization': md5str('wsp_' + wsp_test['wspKey']),
                "Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                'Accept':'application/json'}

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

    get('getgaps', {'room_id':100228})
    post('addgaps', {'room_id':100228, 'uid':10020})
    get('getgaps', {'room_id':100228})
    post('deletegaps', {'room_id':100228, 'uid':10020})

    get('getblacklists', {'room_id':100228})
    post('addblacklists', {'room_id':100228, 'uid':10031})
    get('getblacklists', {'room_id':100228})
    post('deleteblacklists', {'room_id':100228, 'uid':10031})

    post('addmgr', {'room_id':100228, 'uid':10033})
    post('addmgr', {'room_id':100228, 'uid':10034})
    get('getMgrs', {'room_id':100228})
    post('addmgr', {'room_id':100228, 'uid':10031})
    post('delmgr', {'room_id':100228, 'uid':10031})

    ##错误测试
    assert get('newchannel', {'room_id':97}, {'Authorization':'1234'}).Flag==175

    assert get('channelinfo', {'room_id':666666}).Flag==103


def load_room_data(func, fstr):
    with open(fstr, 'r') as rf:
        data = json.load(rf)
        ret_list = []
        print 'all data:', len(data['RECORDS'])
        for item in data['RECORDS']:
            tmp = {
                'state': 1,
                'room_id': item['room_id'],
                'roomtype': item['roomtype'],
                'viewlimit': item['viewlimit'],
                'expireDay': item['expireDay'],
                'room_title': item['room_title'],
                'owner_id': item['owner_id'],
                'notice': item['notice'],
                'cover_pic': item['cover_pic'],
                'hall_pic': item['hall_pic']
            }
            ret = func('newchannel', tmp)
            ret.mid = item['room_id']
            ret_list.append(ret)

    print '\nALL OK:', [i.mid for i in ret_list if i.Flag==100]
    print '\nALL Error:', [i.mid for i in ret_list if i.Flag!=100]
    return ret_list


if __name__ == '__main__':
    main()

