# -*- coding: utf-8 -*-
import re
import os
import csv
import sys
import time

from functools import wraps

import marshal

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

def _run(url_file):
    '''
       log_format main  '$remote_addr $host [$time_local] "$request" '
                     '$status $request_length $body_bytes_sent "$http_referer" "$http_user_agent" '
                     '"$server_addr" "$upstream_addr" "$http_x_forwarded_for" "$upstream_cache_status" $upstream_response_time $request_time';
    '''
    reg_str = r'^([\S]+)\s([\S]+)\s(\[(.*)\])\s\"([A-Z]+)\s([\S]+)\s([^"]+)\"\s([\d]+)\s([\d]+)\s([\d]+)\s\"([^"]+)\"\s\"([^"]+)\"\s\"([^"]+)\"\s\"([^"]+)\"\s\"([^"]+)\"\s\"([^"]+)\"\s([0-9.]+)\s([0-9.]+)$'
    reg = re.compile(reg_str)
    ret_data= []
    with open(url_file, 'r') as rf:
        for idx, line in enumerate(rf):
            tmp = reg.match(line)
            if not tmp:
                continue
            tmp_list = tmp.groups()
            remote_addr, host, time_local, request_method, request_uri, \
                request_protocol, status, request_length, body_bytes_sent, \
                    http_referer, http_user_agent, server_addr, upstream_addr, \
                        http_x_forwarded_for, upstream_cache_status, upstream_response_time, \
                            request_time = tmp_list[1:]

            if request_uri == '-':
                continue

            time_int = parse_time(time_local)
            ret_data.append((time_int, line))

    ret_data.sort(key=lambda i: i[0])
    return [i[1] for i in ret_data]

def run(url_file):
    ret_data = _run(url_file)
    return ret_data



def main():
    print '\n---------------Start-------------------\n'
    url_file = sys.argv[1].strip() if len(sys.argv) >= 2 and sys.argv[1].strip() else os.path.join(os.getcwd(), 'log.txt')

    url_file = 'log.txt'
    out_file = 'log_out.txt'

    if not os.path.isfile(url_file):
        print 'No input specified, use as python xx.py abc.log.'
        return

    ret_list = run(url_file)
    with open(out_file, 'w') as wf:
        wf.writelines(ret_list)

    print '\n---------------End--------------------\n'

if __name__ == '__main__':
    main()