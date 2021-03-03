# -*- coding: utf-8 -*-
import os
import json
import sys
import csv
import requests
import datetime
import time

import talib
import numpy

def dump_json(out_file, obj):
    with open(out_file, 'w') as wf:
        json.dump(obj, wf, indent = 2)

def load_json(in_file):
    with open(in_file, 'r') as rf:
        return json.load(rf)

def dump_text(out_file, strlist):
    with open(out_file, 'w') as wf:
        wf.writelines((l + '\r\n' for l in strlist))

def load_text(in_file):
    with open(in_file, 'r') as rf:
        return rf.read()

def _load_list(filename):
    lines = load_text(filename).split('\n')
    lines = [l.strip().split('/') for l in lines if l.strip()]

    return [(i[0].decode('utf-8'), '0' + i[1]) for i in lines if i[0] and i[1]]

_STOCK_LIST = _load_list('sh_50.txt')

_STOCK_FIELDS = 'TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;VOTURNOVER;VATURNOVER'
_stock_liem = lambda n, c, start='20100101', end='20210301': { \
    'name': n, \
    'code': c[1:], \
    '_code':c, \
    'csv': os.path.join(os.getcwd(), '163_csv', '%s_%s-%s.csv' % (c[1:], start, end)), \
    'url': "http://quotes.money.163.com/service/chddata.html?code=%s&start=%s&end=%s&fields=%s" % (c, start, end, _STOCK_FIELDS) \
}
STOCK_MAP = {c[1:]: _stock_liem(n, c) for n, c in _STOCK_LIST}

def log(msg, tag='DEBUG'):
    time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    print '%s [%s] %s' % (time_str, tag, msg)


def build_item_func(item, cde='gbk'):
    def parse_value_auto(val):
        if val.isdecimal():
            return int(val)
        try:
            return float(val)
        except ValueError:
            return val

    item = item.strip()
    item_arr = item.split('#', 1)
    key = item_arr[0]
    fmt = item_arr[1] if len(item_arr) >= 2 else ''
    func_map = {
        'i': (lambda v: int(v), lambda v: 0),
        's': (lambda v: v, lambda v: v),
        'f': (lambda v: float(v), lambda v: 0.0),
        'a': (parse_value_auto, lambda v: v)
    }
    fmt = 'a' if not fmt else fmt

    fmt_func, def_func = func_map[fmt] if fmt in func_map else (None, None)

    def _parse_value(val):
        try:
            val = val.decode(cde)
            if val == 'None':
                return def_func(val)
            return fmt_func(val) if fmt_func else val
        except Exception as err:
            log('_parse_value tag:%s val:%s' % (fmt, val), 'ERROR')
            return def_func(val) if def_func else val

    return (key, _parse_value)

def build_row_func(fmt_str, cde='gbk'):
    fmt_arr = fmt_str.split(',')
    kv_tuple = [build_item_func(item, cde) for item in fmt_arr if item.strip()]
    def _parse_row(row):
        return {k: f(row[idx]) for idx, (k, f) in enumerate(kv_tuple) if k != '_'}
    return _parse_row

def load_data(in_file, csv_url, fmt_str = 'date#s,_,_,tclose#f,high#f,low#f,topen#f,lclose#f,chg#f,pchg#f,voturnover#f,vaturnover#f', skip = 1, cde='gbk'):
    '''
    日期,股票代码,名称,收盘价,最高价,最低价,开盘价,前收盘,涨跌额,涨跌幅,成交量,成交金额
    2019-03-04,'000001,上证指数,3027.5755,3090.7959,3006.9417,3015.9427,2994.005,33.5705,1.1213,525649436,4.80603655462e+11
    '''
    if not os.path.isfile(in_file):
        res = requests.get(csv_url)
        if res.ok:
            log('get csv file:%s url:%s' % (in_file, csv_url), 'INFO')
            with open(in_file, 'w') as wf:
                wf.write(res.content)
        else:
            log('get csv error file:%s url:%s' % (in_file, csv_url), 'ERROR')
            return []

    ret = []
    row_func = None

    with open(in_file, 'r') as rf:
        spamreader = csv.reader(rf, delimiter=',', quotechar='|')
        spamreader = [i for i in spamreader]
        log('read csv file:%s num:%s' % (in_file, len(spamreader)), 'INFO')
        for idx, row in enumerate(spamreader):
            fmt_str = ','.join(row).decode(cde) if idx == 0 and not fmt_str and skip == 1 else fmt_str
            if row_func is None and fmt_str:
                row_func = build_row_func(fmt_str, cde)

            if idx < skip:
                continue

            ret.append(row if row_func is None else row_func(row))

        return ret

def cci(candles, period=7, sequential=True, high=lambda row: row['high'], low=lambda row: row['low'], close=lambda row: row['tclose']):
    """
    CCI - Commodity Channel Index

    :param candles: np.ndarray
    :param period: int - default=14
    :param sequential: bool - default=False

    :return: float | np.ndarray
    """
    if not sequential and len(candles) > 240:
        candles = candles[-240:]

    np = lambda candles, func: numpy.array([func(i) for i in candles])
    res = talib.CCI(np(candles, high), np(candles, low), np(candles, close), timeperiod=period)

    if sequential:
        return res
    else:
        return None if np.isnan(res[-1]) else res[-1]

def main():
    log('---------------Start-------------------')

    data_file = os.path.join(os.getcwd(), 'stock_cci_data.json')

    if not os.path.isfile(data_file):
        stock_data = {c: load_data(v['csv'], v['url']) for c, v in STOCK_MAP.items()}
        dump_json(data_file, stock_data)
        log('write file %s' % (data_file, ))
    else:
        stock_data = load_json(data_file)
        log('read file %s' % (data_file, ))

    for code, candles in stock_data.iteritems():
        res = cci(candles, 28)
        print code, STOCK_MAP[code]['name'], res[-30:], "\n"

    log('---------------End--------------------')

if __name__ == '__main__':
    main()
