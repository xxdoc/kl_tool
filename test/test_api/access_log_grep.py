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
    ret = ''
    try:
        ret = IP.find(ip)
    except Exception as ex:
        print 'x',

    while("\t\t" in ret):
        ret = ret.replace("\t\t", "\t")
    return ret



def _run(url_file, save_seq, interval):
    '''
       log_format main  '$remote_addr $host [$time_local] "$request" '
                     '$status $request_length $body_bytes_sent "$http_referer" "$http_user_agent" '
                     '"$server_addr" "$upstream_addr" "$http_x_forwarded_for" "$upstream_cache_status" $upstream_response_time $request_time';
    '''
    reg_str = r'^([\S]+)\s([\S]+)\s(\[(.*)\])\s\"([A-Z]+)\s([\S]+)\s([^"]+)\"\s([\d]+)\s([\d]+)\s([\d]+)\s\"([^"]+)\"\s\"([^"]+)\"\s\"([^"]+)\"\s\"([^"]+)\"\s\"([^"]+)\"\s\"([^"]+)\"\s([0-9.]+)\s([0-9.]+)$'
    reg = re.compile(reg_str)

    agent_map = {}
    ip_map = {}
    timer_map = {}

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

##            url_data.append(dict(
##                ip=ip, ip_loc=ip_loc, time_str = format_time(parse_time(time_local)), \
##                group_path=group_path, request_path=request_path, request_time=request_time, time_local=parse_time(time_local),\
##                status=status, request_length=request_length, http_referer=http_referer, http_user_agent=http_user_agent, http_x_forwarded_for=http_x_forwarded_for,\
##                body_bytes_sent=body_bytes_sent, request_method=request_method, request_protocol=request_protocol,\
##                upstream_cache_status=upstream_cache_status, \
##                upstream_response_time=upstream_response_time, timer_count=timer_count
##            ))
            agent_map.setdefault(http_user_agent, {})
            if timer_count in agent_map[http_user_agent]:
                agent_map[http_user_agent][timer_count] += 1
            else:
                agent_map[http_user_agent][timer_count] = 1

            ip_map.setdefault(ip, {})
            if timer_count in ip_map[ip]:
                ip_map[ip][timer_count] += 1
            else:
                ip_map[ip][timer_count] = 1

            if timer_count in timer_map:
                timer_map[timer_count] += 1
            else:
                timer_map[timer_count] = 1

            if idx % save_seq == 1:
                print '.',

    return agent_map, ip_map, timer_map

def run(url_file, save_seq=10000, interval=60):
    agent_tmp = url_file + '.agent.tmp'
    ip_tmp = url_file + '.ip.tmp'
    timer_tmp = url_file + '.timer.tmp'

    if os.path.isfile(agent_tmp) and os.path.isfile(ip_tmp) and os.path.isfile(timer_tmp):
        agent_map, ip_map, timer_map = load_obj(agent_tmp), load_obj(ip_tmp), load_obj(timer_tmp)
    else:
        agent_map, ip_map, timer_map = _run(url_file, save_seq, interval)
        dump_obj(agent_map, agent_tmp)
        dump_obj(ip_map, ip_tmp)
        dump_obj(timer_map, timer_tmp)

    return agent_map, ip_map, timer_map

def listIntervalMap(data_map):
    s_func = lambda l: sorted(l, key=lambda t: t[0])
    f_func = lambda k: k
    r_func = lambda k, v: ( "%s#%s" % (k, v) ).replace(':00#', '#').split(' ', 1)[-1]
    return fix_ret_map(data_map, s_func, r_func, f_func, '\n')

def fix_ret_map(data_map, s_func, r_func, f_func, seq=','):
    item_list = s_func(data_map.iteritems())

    ret_list = []
    for k, v in item_list:
        if f_func(k):
            tmp_str = r_func(k, v)
            ret_list.append(tmp_str)
    return seq.join(ret_list)

def writeDataCsv(csv_file, data):
    data.sort(key = lambda i: i.get('num', 0), cmp = lambda a,b: 1 if a < b else -1)
    with open(csv_file, 'wb') as csvfile:
        fieldnames = ['num']
        fieldnames = fieldnames + [i for i in data[0].keys() if i not in fieldnames]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            writer.writerow(item)

def main():
    print '\n---------------Start-------------------\n'
    url_file = sys.argv[1].strip() if len(sys.argv) >= 2 and sys.argv[1].strip() else os.path.join(os.getcwd(), 'zxc.log')

    defult_file = 'access_11_14_151_dms.log'
    if not os.path.isfile(url_file) and os.path.isfile(os.path.join(os.getcwd(), defult_file)):
        url_file = os.path.join(os.getcwd(), defult_file)

    if not os.path.isfile(url_file):
        print 'No input specified, use as python xx.py abc.log.'
        return

    agent_map, ip_map, timer_map = run(url_file)

    agent_csv = url_file + '.agent.csv'
    ip_csv = url_file + '.ip.csv'
    timer_csv = url_file + '.timer.csv'

    writeDataCsv(agent_csv, [{
        'num': sum(n.values()),
        'agent': k,
        'map': listIntervalMap(n),
    } for k,n in agent_map.items()])


    writeDataCsv(ip_csv, [{
        'num': sum(n.values()),
        'ip': k,
        'map': listIntervalMap(n),
        'location': ip_location(k)
    } for k,n in ip_map.items()])


    writeDataCsv(timer_csv, [{
        'num': n,
        'time': k
    } for k,n in timer_map.items()])

    print '\n---------------End--------------------\n'

if __name__ == '__main__':
    main()