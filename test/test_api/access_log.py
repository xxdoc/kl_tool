# -*- coding: utf-8 -*-
import re
import os
import csv
import sys
import time
from ipip import IP


from functools import wraps

import marshal

IP.load(os.path.join(os.getcwd(), "17monipdb.dat"))

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
    timestruct = time.localtime(timestamp * 1.0)
    ret = time.strftime('%Y-%m-%d %H:%M:%S', timestruct)
    return ret

@fn_cache(lambda args, kwargs: _args_n(args, kwargs, 0, 'ip', 0))
def ip_location(ip):
    ip = ip.split(',')[-1].strip()
    ret = IP.find(ip)
    while("\t\t" in ret):
        ret = ret.replace("\t\t", "\t")
    return ret



def _run(url_file, save_seq, interval, group_path_func):
    '''
       log_format main  '$remote_addr $host [$time_local] "$request" '
                     '$status $request_length $body_bytes_sent "$http_referer" "$http_user_agent" '
                     '"$server_addr" "$upstream_addr" "$http_x_forwarded_for" "$upstream_cache_status" $upstream_response_time $request_time';
    '''
    reg_str = r'^([\S]+)\s([\S]+)\s(\[(.*)\])\s\"([A-Z]+)\s([\S]+)\s([^"]+)\"\s([\d]+)\s([\d]+)\s([\d]+)\s\"([^"]+)\"\s\"([^"]+)\"\s\"([^"]+)\"\s\"([^"]+)\"\s\"([^"]+)\"\s\"([^"]+)\"\s([0-9.]+)\s([0-9.]+)$'
    reg = re.compile(reg_str)
    ret_data, ret_group = {}, {}
    url_data = []

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

            ip = http_x_forwarded_for.split(',')[-1].strip()
            ip_loc = ip_location(ip)

            timer_count = format_time( int(parse_time(time_local) / interval) * interval + interval)

            request_path = request_uri.split('?', 1)[0]
            update_count_item(ret_data, request_path, request_time, request_length, body_bytes_sent, status, timer_count)

            group_path = group_path_func(request_path) if group_path_func else request_path
            url_data.append(dict(
                ip=ip, ip_loc=ip_loc, time_str = format_time(parse_time(time_local)), \
                group_path=group_path, request_path=request_path, request_time=request_time, time_local=parse_time(time_local),\
                status=status, request_length=request_length, http_referer=http_referer, http_x_forwarded_for=http_x_forwarded_for,\
                body_bytes_sent=body_bytes_sent, request_method=request_method, request_protocol=request_protocol,\
                upstream_cache_status=upstream_cache_status, \
                upstream_response_time=upstream_response_time, timer_count=timer_count
            ))
            update_count_item(ret_group, group_path, request_time, request_length, body_bytes_sent, status, timer_count)

            if idx % save_seq == 1:
                print '.',

    return ret_data, ret_group, url_data

def run(url_file, save_seq=10000, interval=60, group_path_func=None):
    tmp_ret = url_file + '.ret.tmp'
    tmp_group = url_file + '.group.tmp'
    tmp_url_data = url_file + '.url_data.tmp'

    if os.path.isfile(tmp_ret) and os.path.isfile(tmp_ret) and os.path.isfile(tmp_url_data):
        ret_data, ret_group, url_data = load_obj(tmp_ret), load_obj(tmp_group), load_obj(tmp_url_data)
    else:
        ret_data, ret_group, url_data = _run(url_file, save_seq, interval, group_path_func)
        dump_obj(ret_data, tmp_ret)
        dump_obj(ret_group, tmp_group)
        dump_obj(url_data, tmp_url_data)

    ret_data, ret_group = calculateAverage(ret_data), calculateAverage(ret_group)
    ret_data, ret_group = listIntervalMap(ret_data), listIntervalMap(ret_group)
    return ret_data, ret_group, url_data

def listIntervalMap(ret_data):
    key = 'interval_map'
    for url, item in ret_data.iteritems():
        data_map = item.get(key, {})
        s_func = lambda l: sorted(l, key=lambda t: t[0])
        f_func = lambda k: k
        r_func = lambda k, v: ( "%s#%s" % (k, v) ).replace(':00#', '#').split(' ', 1)[-1]
        ret_data[url][key] = fix_ret_map(data_map, s_func, r_func, f_func, '\n')

    key = 'status_map'
    for url, item in ret_data.iteritems():
        data_map = item.get(key, {})
        s_func = lambda l: sorted(l, key=lambda t: t[0])
        f_func = lambda k: k
        r_func = lambda k, v: "%s#%s" % (k, v)
        ret_data[url][key] = fix_ret_map(data_map, s_func, r_func, f_func, '\n')

    return ret_data

def fix_ret_map(data_map, s_func, r_func, f_func, seq=','):
    item_list = s_func(data_map.iteritems())

    ret_list = []
    for k, v in item_list:
        if f_func(k):
            tmp_str = r_func(k, v)
            ret_list.append(tmp_str)
    return seq.join(ret_list)

def update_count_item(obj, url, request_time, request_length, body_bytes_sent, status, timer_count):
    item = obj.get(url, {
        'num': 0,
        'status_map': {},
        'interval_map': {},
        'total_request_time': 0.0,
        'total_request_length': 0.0,
        'total_body_bytes_sent': 0.0,
        'max_request_time': 0.0,
        'max_request_length': 0.0,
        'max_body_bytes_sent': 0.0,
        'min_request_time': 0.0,
        'min_request_length': 0.0,
        'min_body_bytes_sent': 0.0,
    })
    request_time, request_length, body_bytes_sent = float(request_time), float(request_length), float(body_bytes_sent)
    item['num'] += 1
    item['total_request_time'] += request_time
    item['total_request_length'] += request_length
    item['total_body_bytes_sent'] += body_bytes_sent
    if status and (int(status)==200 or int(status)==201 or int(status)==206):
        item['max_request_time'] = request_time if request_time > item['max_request_time'] else item['max_request_time']
        item['max_request_length'] = request_length if request_length > item['max_request_length'] else item['max_request_length']
        item['max_body_bytes_sent'] = body_bytes_sent if body_bytes_sent > item['max_body_bytes_sent'] else item['max_body_bytes_sent']
        item['min_request_time'] = request_time if request_time < item['min_request_time'] else item['min_request_time']
        item['min_request_length'] = request_length if request_length < item['min_request_length'] else item['min_request_length']
        item['min_body_bytes_sent'] = body_bytes_sent if body_bytes_sent < item['min_body_bytes_sent'] else item['min_body_bytes_sent']

    item['status_map'][ status ] = item['status_map'].get(status, 0) + 1
    item['interval_map'][ timer_count ] = item['interval_map'].get(timer_count, 0) + 1

    obj[ url ] = item

def calculateAverage(obj):
    for key, val in obj.iteritems():
        val['ave_request_time'] = round(val['total_request_time'] / val['num'], 2)
        val['ave_request_length'] = round(val['total_request_length'] / val['num'], 2)
        val['ave_body_bytes_sent'] = round(val['total_body_bytes_sent'] / val['num'], 2)

    return obj

def writeCsv(csv_file, obj):
    s_map = {'request':'req', 'body_bytes':'body'}
    def _fix(str_k, replace_map):
        for k, v in replace_map.items():
            str_k = str_k.replace(k, v)
        return str_k

    with open(csv_file, 'wb') as csvfile:
        fieldnames = ['url', ] + obj[ obj.keys()[0] ].keys()
        fieldnames = [_fix(i, s_map) for i in fieldnames]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for url, item in obj.iteritems():
            item['url'] = url[:50]
            writer.writerow({_fix(k, s_map): v for k, v in item.items()})

def group_path_func(uri):
    _g_map = {
        '/admin': '/admin/(.*)',
        '/super': '/super/(.*)',
        '/v/': '/v/(.*)',
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

def writeDataCsv(csv_file, data):
    data.sort(key = lambda i: i.get('time_local', 0), cmp = lambda a,b: 1 if a > b else -1)
    with open(csv_file, 'wb') as csvfile:
        fieldnames = ['time_str', 'request_path', 'ip', 'ip_loc', 'status', 'http_referer']
        fieldnames = fieldnames + [i for i in data[0].keys() if i not in fieldnames]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            item['request_path'] = item['request_path'][:50]
            item['http_referer'] = item['http_referer'][:50]
            writer.writerow(item)

def main():
    print '\n---------------Start-------------------\n'
    url_file = sys.argv[1].strip() if len(sys.argv) >= 2 and sys.argv[1].strip() else os.path.join(os.getcwd(), 'zxc.log')

    defult_file = 'zxc.log'
    if not os.path.isfile(url_file) and os.path.isfile(os.path.join(os.getcwd(), defult_file)):
        url_file = os.path.join(os.getcwd(), defult_file)

    if not os.path.isfile(url_file):
        print 'No input specified, use as python xx.py abc.log.'
        return

    ret_data, ret_group, url_data = run(url_file, group_path_func=group_path_func)

    csv_file = url_file + '.csv'
    writeCsv(csv_file, ret_data)
    group_file = url_file + '.group.csv'
    writeCsv(group_file, ret_group)

    data_file = url_file + '.data.csv'
    writeDataCsv(data_file, url_data)

    print '\nwrite file', csv_file
    print '\n---------------End--------------------\n'

if __name__ == '__main__':
    main()