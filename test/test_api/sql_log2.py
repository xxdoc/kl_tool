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
def parse_time(date_str):
    # '2017-12-28 15:30:00'
    timestruct = time.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    ret = int(time.mktime(timestruct))
    return ret

@fn_cache(lambda args, kwargs: _args_n(args, kwargs, 0, 'timestamp', 0))
def format_time(timestamp):
    timestruct = time.localtime(timestamp)
    ret = time.strftime('%Y-%m-%d %H:%M:%S', timestruct)
    return ret

def _run(sql_file, save_seq, interval, group_path_func):
    '''
        LOG,DB,TID,USER,USER_IP,SQL_TYPE,FAIL,CHECK_ROWS,UPDATE_ROWS,LATENCY,TS
        "select * from room_powers where room_id=1001","java_hk8_5",292327,"hk_wd","172.31.101.189","select","0",1,0,235,2020-03-17 15:45:06
    '''
    pass_func = lambda s: s.startswith('log') or s.startswith('use ') or s.startswith('set ')

    ret_data, ret_group = {}, {}
    with open(sql_file, 'r') as rf:
        for idx, line in enumerate(rf):
            if idx == 0:
                continue

            line = line.strip()
            arr = line.split('","', 1)
            if len(arr) != 2:
                continue

            sql_cmd = arr[0][1:]

            tmp_list = arr[1].split(",")
            if len(tmp_list) != 10:
                continue

            DB,TID,USER,USER_IP,SQL_TYPE,FAIL,CHECK_ROWS,UPDATE_ROWS,LATENCY,TS = \
                tmp_list[0][1:-1], int(tmp_list[1]), tmp_list[2][1:-1], tmp_list[3][1:-1], tmp_list[4][1:-1], tmp_list[5][1:-1], \
                    int(tmp_list[6]), int(tmp_list[7]), int(tmp_list[8]), (tmp_list[9])
            time_local, db_name, user, client_ip, cost_time, ret_num, thread_id = \
                TS, DB, USER, USER_IP, LATENCY, CHECK_ROWS, TID

            if pass_func(sql_cmd):
                continue

            timer_count = format_time( int(parse_time(time_local) / interval) * interval + interval)

            update_count_item(ret_data, sql_cmd, cost_time, ret_num, timer_count)

            group_sql = group_path_func(sql_cmd) if group_path_func else request_path
            update_count_item(ret_group, group_sql, cost_time, ret_num, timer_count)

            if idx % save_seq == 1:
                print '.',

    return ret_data, ret_group

def run(sql_file, save_seq=10000, interval=60, group_path_func=None, use_tmp=False):
    tmp_ret = sql_file + '.ret.tmp'
    tmp_group = sql_file + '.group.tmp'
    if os.path.isfile(tmp_ret) and os.path.isfile(tmp_ret) and use_tmp:
        ret_data, ret_group = load_obj(tmp_ret), load_obj(tmp_group)
    else:
        ret_data, ret_group = _run(sql_file, save_seq, interval, group_path_func)
        dump_obj(ret_data, tmp_ret)
        dump_obj(ret_group, tmp_group)

    ret_data, ret_group = calculateAverage(ret_data), calculateAverage(ret_group)
    ret_data, ret_group = listIntervalMap(ret_data), listIntervalMap(ret_group)
    return ret_data, ret_group

def listIntervalMap(ret_data):
    key = 'interval_map'
    for url, item in ret_data.iteritems():
        data_map = item.get(key, {})
        s_func = lambda l: sorted(l, key=lambda t: t[0])
        f_func = lambda k:1
        r_func = lambda k, v: ( "%s#%s" % (k, v) ).replace(':00#', '#').split(' ', 1)[-1]
        ret_data[url][key] = fix_ret_map(data_map, s_func, r_func, f_func, '\n')

    key = 'ret_map'
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

def update_count_item(obj, sql, cost_time, ret_num, timer_count):
    item = obj.get(sql, {
        'num': 0,
        'ret_map': {},
        'interval_map': {},
        'total_ret_num': 0,
        'total_cost_time': 0.0,
        'max_ret_num': ret_num,
        'min_ret_num': ret_num,
        'max_cost_time': cost_time,
        'min_cost_time': cost_time,
    })

    item['num'] += 1
    item['total_cost_time'] += cost_time
    item['total_ret_num'] += ret_num

    item['max_cost_time'] = cost_time if cost_time > item['max_cost_time'] else item['max_cost_time']
    item['min_cost_time'] = cost_time if cost_time < item['min_cost_time'] else item['min_cost_time']

    item['max_ret_num'] = ret_num if ret_num > item['max_ret_num'] else item['max_ret_num']
    item['min_ret_num'] = ret_num if ret_num < item['min_ret_num'] else item['min_ret_num']


    item['ret_map'][ ret_num ] = item['ret_map'].get(ret_num, 0) + 1
    item['interval_map'][ timer_count ] = item['interval_map'].get(timer_count, 0) + 1

    obj[ sql ] = item

def calculateAverage(obj):
    for key, val in obj.iteritems():
        val['ave_ret_num'] = round(val['total_ret_num'] / val['num'], 2)
        val['ave_cost_time'] = round(val['total_cost_time'] / val['num'], 2)

    return obj

def writeCsv(csv_file, obj):
    s_map = {'request':'req', 'body_bytes':'body'}
    def _fix(str_k, replace_map):
        for k, v in replace_map.items():
            str_k = str_k.replace(k, v)
        return str_k

    with open(csv_file, 'wb') as csvfile:
        fieldnames = ['sql', ] + obj[ obj.keys()[0] ].keys()
        fieldnames = [_fix(i, s_map) for i in fieldnames]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for sql, item in obj.iteritems():
            item['sql'] = sql
            writer.writerow({_fix(k, s_map): v for k, v in item.items()})

def group_path_func(uri):
    uri = uri.lower()
    if uri.startswith('update'):
        return uri.split('where')[0].strip()

    if uri.startswith('select'):
        return uri.split('where')[0].strip()

    if uri.startswith('insert'):
        return uri.split('(')[0].strip()

    if uri.startswith('delete'):
        return uri.split('where')[0].strip()

    return uri

def main():
    print '\n---------------Start-------------------\n'
    sql_file = sys.argv[1].strip() if len(sys.argv) >= 2 and sys.argv[1].strip() else os.path.join(os.getcwd(), 'custins24601839_1584437406891.csv')
    if not os.path.isfile(sql_file):
        print 'No input specified, use as python xx.py abc.sql.'
        return

    ret_data, ret_group = run(sql_file, group_path_func=group_path_func)

    csv_file = sql_file + '.csv'
    writeCsv(csv_file, ret_data)
    group_file = sql_file + '.group.csv'
    writeCsv(group_file, ret_group)

    print '\nwrite file', csv_file
    print '\n---------------End--------------------\n'

if __name__ == '__main__':
    main()