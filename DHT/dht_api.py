# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        qq_api
# Purpose:
#
# Author:      Administrator
#
# Created:     01/01/2016
# Copyright:   (c) Administrator 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import inspect
import pymongo
import json
from api_tool import api_wrapper, FNVHash
from dht_config import config

TASK_CUR = config.MONGODB_CONN.btdb.magnet
SAVE_CUR = config.MONGODB_CONN.torrentfs.torrent
REDIS_CUR = config.REDIS_CONN

#========================================================
#========================API FUNCS=======================
#========================================================

@api_wrapper(config.api_ver, parser=lambda i: (i.get('func', '')))
def apiHelper(func=''):
    api_dict = getattr(apiHelper, 'api_dict', None)
    if api_dict is None:
        is_api = lambda obj: getattr(obj, 'api_ver', '')==config.api_ver and hasattr(obj, '__call__')
        doc = lambda f:{'doc': getattr(f, '__doc__', 'no __doc__ .'),
                        'args':str(inspect.getargspec(f)),
                        'parser':inspect.getsource(getattr(f,'parser',lambda args_str, web_input:args_str)),
                        }
        api_dict = {k:doc(v) for k,v in globals().items() if is_api(v)}
        apiHelper.api_dict = api_dict

    result = {'apiHelper':"use /api/func/?a=A&b=B&c=C[&indent=4][&callback=callback]",
              'func':api_dict}
    if not isinstance(func, (str, unicode)):
        return result
    return {func:api_dict[func]} if func in api_dict else result

@api_wrapper(config.api_ver, parser=lambda i: (i.apikey, i.get('nums', '200')))
def getTorrentTask(apikey='', nums=20, use_radis=True):
    """getTorrentTask hashkeys to download torrent.

    :Parameters:
      - `apikey` - api key to auth.
      - `nums` - nums of tasks.

    :Returns:
      task_list of :class:`list`.
    """
    all_time = nums * 100
    task_list = []
    ret = TASK_CUR.find({'info': {'$exists':False},'try_count':{'$lt':1}})
    for item in ret:
        if len(task_list) >= nums:
            break

        if is_in_doing_task(item, all_time):
            continue

        if item['_id']:
            task_list.append({'hashkey':item['_id'], 'count':item['count'], 'uptime':item['uptime']})

    return task_list

@api_wrapper(config.api_ver, parser=lambda i: (i.get('hashkey', ''), json.loads(i.get('info', 'null')), i.get('torrent', '')))
def doneTorrentTask(hashkey, info, torrent=''):
    """doneTorrentTask save info and torrent to hashkeys.

    :Parameters:
      - `hashkey` - bt hashkey.
      - `info` - torrnet file info.
      - `torrent` - torrent file.

    :Returns:
      save_result of :class:`dict`.
    """
    if not hashkey:
        return {'error': 'bad hashkey.'}

    save_result = {'data': {}}
    if info:
        save_result['data']['info_len'] = len(info)
        set_dict = {'$inc':{'try_count': 1}, '$set':{'info': info}}
    else:
        save_result['data']['info_len'] = 0
        set_dict = {'$inc':{'try_count': 1}}

    try:
        TASK_CUR.update_one({'_id': hashkey}, set_dict, upsert=True)
        save_result['data']['info_save'] = 'ok'
    except pymongo.errors.PyMongoError as ex:
        msg = 'PyMongoError:%s, hashkey:%s, info:%s\n' % (ex, hashkey, info)
        save_result['error'] = {'Exception': 'PyMongoError', 'msg': msg}

##    if torrent:
##        save_result['data']['torrent_len'] = len(torrent)
##        try:
##            SAVE_CUR.update_one({'_id': hashkey}, {'$set':{'torrent': torrent}}, upsert=True)
##        except pymongo.errors.PyMongoError as ex:
##            msg = 'PyMongoError:%s, hashkey:%s, torrent:%s\n' % (ex, torrent, info)
    #magnet:?xt=urn:btih:ec6b187a284b097d83079a166cb5c7abce67c83f
    return save_result

def is_in_doing_task(item, expire):
    key = item['_id']
    if REDIS_CUR.get(key) is None:
        REDIS_CUR.set(key, item)
        REDIS_CUR.expire(key, expire)
        return False
    else:
        return True


def get_link():
    info = bt.torrent_info('test.torrent')
    link = "magnet:?xt=urn:btih:%s&dn=%s" % (info.info_hash(), info.name())
    return link

def main():
    test = getTorrentTask('', 10000, False)
    out_list = []
    base_str = 'magnet:?xt=urn:btih:%s'
    for item in test:
        out_list.append(base_str % (item['hashkey'],))

    with open('torrent_test.text', 'w') as wf:
        wf.writelines([s+'\n' for s in out_list])

if __name__ == '__main__':
    main()
