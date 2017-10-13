# -*- coding: utf-8 -*-
import re
import os
import csv
import sys
import time

from functools import wraps

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

def run(url_file, save_seq=10000, interval=300, group_path_func=None):
    '''
       log_format main  '$remote_addr $host [$time_local] "$request" '
                     '$status $request_length $body_bytes_sent "$http_referer" "$http_user_agent" '
                     '"$server_addr" "$upstream_addr" "$http_x_forwarded_for" "$upstream_cache_status" $upstream_response_time $request_time';
    '''
    reg_str = r'^([\S]+)\s([\S]+)\s(\[(.*)\])\s\"([A-Z]+)\s([\S]+)\s([^"]+)\"\s([\d]+)\s([\d]+)\s([\d]+)\s\"([^"]+)\"\s\"([^"]+)\"\s\"([^"]+)\"\s\"([^"]+)\"\s\"([^"]+)\"\s\"([^"]+)\"\s([0-9.]+)\s([0-9.]+)$'
    reg = re.compile(reg_str)
    ret_data, ret_group = {}, {}
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

            timer_count = format_time( int(parse_time(time_local) / interval) * interval + interval)

            request_path = request_uri.split('?', 1)[0]
            update_count_item(ret_data, request_path, request_time, request_length, body_bytes_sent, status, timer_count)

            group_path = group_path_func(request_path) if group_path_func else request_path
            update_count_item(ret_group, group_path, request_time, request_length, body_bytes_sent, status, timer_count)

            if idx % save_seq == 1:
                print '.',

    ret_data, ret_group = calculateAverage(ret_data), calculateAverage(ret_group)
    return ret_data, ret_group

def update_count_item(obj, key, request_time, request_length, body_bytes_sent, status, timer_count):
    obj.setdefault(key, {
        'num': 0,
        'status_map': {},
        'interval_map': {},
        'total_request_time': 0.0,
        'total_request_length': 0.0,
        'total_body_bytes_sent': 0.0,
    })

    obj[ key ]['num'] += 1
    obj[ key ]['total_request_time'] += float(request_time)
    obj[ key ]['total_request_length'] += float(request_length)
    obj[ key ]['total_body_bytes_sent'] += float(body_bytes_sent)
    obj[ key ]['status_map'][ status ] = obj[ key ]['status_map'].get(status, 0) + 1
    obj[ key ]['interval_map'][ timer_count ] = obj[ key ]['interval_map'].get(timer_count, 0) + 1

def calculateAverage(obj):
    for key, val in obj.iteritems():
        val['average_request_time'] = round(val['total_request_time'] / val['num'], 2)
        val['average_request_length'] = round(val['total_request_length'] / val['num'], 2)
        val['average_body_bytes_sent'] = round(val['total_body_bytes_sent'] / val['num'], 2)

    return obj

def writeCsv(csv_file, obj):
    with open(csv_file, 'wb') as csvfile:
        fieldnames = ['url', ] + obj[ obj.keys()[0] ].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for url, item in obj.iteritems():
            item['url'] = url
            writer.writerow(item)

def main():
    print '\n---------------Start-------------------\n'
    url_file = sys.argv[1].strip() if len(sys.argv) >= 2 and sys.argv[1].strip() else os.path.join(os.getcwd(), 'access.log')
    if not os.path.isfile(url_file):
        print 'No input specified, use as python xx.py abc.log.'
        return

    def group_path_func(uri):
        _g_map = {
            '/admin': '/admin/(.*)',
            '/super': '/super/(.*)',
            '/v/': '/user/(.*)',
            '/user/': '/user/(\d+)',
            '/verify/': '/verify/(\d+)',
            '/siteurl/': '/siteurl/(\d+)',
        }

        for pre_key, group in _g_map.iteritems():
            if uri.startswith(pre_key):
                return group

        _d_list = ['live', 'gift', 'chat', 'iframe']
        for reg_d in _d_list:
            reg = re.compile(r'^/%s/([A-Za-z0-9]+)/(\d+)$' % (reg_d, ))
            tmp = reg.match(uri)
            if tmp:
                ctrl = tmp.groups()[0]
                return '/%s/%s/(\d+)' % (reg_d, ctrl)
        return uri

    ret_data, ret_group = run(url_file, group_path_func=group_path_func)

    csv_file = url_file + '.csv'
    writeCsv(csv_file, ret_data)
    group_file = url_file + '.group.csv'
    writeCsv(group_file, ret_group)

    print '\nwrite file', csv_file
    print '\n---------------End--------------------\n'

if __name__ == '__main__':
    main()