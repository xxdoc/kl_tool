import sys
import os
import datetime
import json
import redis

def load_redis_config(config_file):
    if not os.path.isfile(config_file):
        raise ValueError('file not found with:{}'.format(config_file))
    with open(config_file, 'r') as rf:
        config = json.load(rf)
    redisAddr = config.get('redisAddr', '')
    if not redisAddr:
        raise ValueError('redisAddr not found with:{}'.format(json.dumps(config)))
    host = redisAddr.split(':', 1)[0] if ':' in redisAddr else redisAddr
    port = redisAddr.split(':', 1)[1] if ':' in redisAddr else 6379
    redis_config = {
        'host': str(host),
        'port': int(port),
        'db': int(config.get('redisDb', 0)),
        'password': str(config.get('redisPassword', '')),
    }
    '''redis_config.update({
        'host': '127.0.0.1',
        'db': 6,
        'password': 'foobared'
    })'''
    return redis_config

def do_fix_dms(_redis, iter_num=100):
    KEY_CLIENT_ATS = 'CLIENT_ATS'
    PRE_COMET_REG = 'COMET_REG_*'
    PRE_UL = 'UL_*'
    PRE_TD = 'TD_*'

    __replace = lambda s, p: p.replace('*', str(s))
    _reg_key = lambda c_id: __replace(c_id, PRE_COMET_REG)

    _scan = lambda p: _redis.scan_iter(p, count=iter_num)
    _zscan = lambda p: _redis.zscan_iter(p, count=iter_num)
    _hscan = lambda p: _redis.hscan_iter(p, count=iter_num)
    _sscan = lambda p: _redis.sscan_iter(p, count=iter_num)

    del_count, alive_map, client_set = 0, {}, set()
    
    def _is_bad_comet(comet_id):
        if comet_id not in alive_map:
            is_exists = _redis.exists(_reg_key(comet_id))
            alive_map.setdefault(comet_id, int(is_exists))

        return comet_id <= 0 or alive_map.get(comet_id, 0) == 0
        
    for ul_key in _scan(PRE_UL):
        for zkey, _ in _zscan(ul_key):
            idx = zkey.find('^')
            comet_id = int(zkey[:idx]) if idx > 0 else 0
            client_id = zkey[idx + 1:] if idx > 0 else zkey
            client_set.add(client_id)

            if _is_bad_comet(comet_id):
                _hdel = _redis.hdel(KEY_CLIENT_ATS, client_id)
                _zrem = _redis.zrem(ul_key, zkey)
                print _t(), ' [INFO] ', 'ul_key:', ul_key, 'zkey:', zkey, '<%s,%s>' % (_hdel, _zrem)
                del_count += 2

    for td_key in _scan(PRE_TD):
        for comet_id in _sscan(td_key):
            comet_id = int(comet_id)
            if _is_bad_comet(comet_id):
                _srem = _redis.srem(td_key, comet_id)
                print _t(), ' [INFO] ', 'td_key:', td_key, 'comet_id:', comet_id, '<%s>' % (_srem, )
                del_count += 1

    for client_id, comet_id in _hscan(KEY_CLIENT_ATS):
        comet_id = int(comet_id)
        if client_id not in client_set and _is_bad_comet(comet_id):
            _hdel = _redis.hdel(KEY_CLIENT_ATS, client_id)
            print _t(), ' [INFO] ', 'hkey:', KEY_CLIENT_ATS, 'client_id:', client_id, '<%s>' % (_hdel, )
            del_count += 1

    
    return del_count

def _t():
    tmp = str(datetime.datetime.now())
    return tmp if len(tmp)>=26 else tmp + '0' * (26 - len(tmp))

def main(config_file):
    print "======== START ========="
    _redis = redis.Redis(**load_redis_config(config_file))
    del_count = do_fix_dms(_redis)

    print _t(), ' [INFO] ', ' config_file:', config_file, ', del_count:', del_count

    print "======== START ========="

if __name__ == '__main__':
    config_file = str(sys.argv[1]).strip() if len(sys.argv) >=2 else ''
    if not config_file:
        config_file = os.path.join(os.getcwd(), 'black-mqtt-conf.json')
    main(config_file)
