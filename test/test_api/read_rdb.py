# -*- coding: utf-8 -*-
import re
import os
import csv
import sys
import time

from functools import wraps

import marshal
import json
import phpserialize

def dump_obj(obj, file_name):
    with open(file_name, 'wb') as wf:
        marshal.dump(obj, wf)

def load_obj(file_name):
    with open(file_name, 'rb') as rf:
        return marshal.load(rf)

def fn_cache(key=None):
    _default_key_func = lambda args, kwargs: '<args:%r,kwargs:%r>' % (args, kwargs)
    _key_func = _default_key_func if key is None else key

    def _fn_cache(func):
        cache_dict = {}

        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = _key_func(args, kwargs)
            if cache_key in cache_dict:
                return cache_dict[cache_key]
            else:
                ret = func(*args, **kwargs)
                cache_dict.setdefault(cache_key, ret)
                return ret

        return wrapper

    return _fn_cache

_args_n = lambda args, kwargs, idx, name, default: args[idx] if len(args)>idx else kwargs.get(name, default)

@fn_cache(lambda args, kwargs: '%s,%s' % (_args_n(args, kwargs, 0, 'a', 1), _args_n(args, kwargs, 1, 'b', 2)))
def add(a=1, b=2):
    print '<!-- ', a, '+', b, '=', a + b, ' -->'
    return a + b

@fn_cache(lambda args, kwargs: _args_n(args, kwargs, 0, 'date_str', ''))
def parse_time(date_str, reg=re.compile(r'^(\d+)\/([A-Za-z]+)\/(\d+):([0-9]+):(\d+):(\d+)\s\+([0-9]+)$')):
    # '12/Oct/2017:19:25:00 +0800'
    tmp = reg.match(date_str)
    if not tmp:
        return 0
    day, month, year, h, m, s, utc = tmp.groups()
    time_str = '%s-%s-%s %s:%s:%s' %(year, month, day, h, m, s)
    timestruct = time.strptime(time_str, '%Y-%b-%d %H:%M:%S')
    ret = int(time.mktime(timestruct))
    return ret

@fn_cache(lambda args, kwargs: _args_n(args, kwargs, 0, 'timestamp', 0))
def format_time(timestamp):
    timestruct = time.localtime(timestamp)
    ret = time.strftime('%Y-%m-%d %H:%M:%S', timestruct)
    return ret



def main():
    print '\n---------------Start-------------------\n'
    rdb_file = sys.argv[1].strip() if len(sys.argv) >= 2 and sys.argv[1].strip() else os.path.join(os.getcwd(), 'access.log')

    rdb_file = 'rdb_dump.json'

    if not os.path.isfile(rdb_file):
        print 'No input specified, use as python xx.py abc.rdb.'
        return

    password_set = set()

    with open(rdb_file, 'r') as rf:
        for line in rf:
            if len(line) <= 10:
                continue
            idx = line.find(':')
            if idx > 0:
                key = line[1:idx-1]
                b_idx = line.rfind(';"')
                val = json.loads(line[idx+1:b_idx+2])

                try:
                    obj = phpserialize.loads(val)
                    obj = phpserialize.loads(obj)
                except:
                    pass
                if isinstance(obj, dict) and obj.get('login_password', ''):
                    login_password = obj.get('login_password', '')
                    password_set.add(login_password)

    print 'login_password:', password_set

    out_file = 'rdb_dump_password.json'
    with open(out_file, 'w') as wf:
        json.dump(list(password_set), wf)

    print '\n---------------End--------------------\n'

if __name__ == '__main__':
    main()