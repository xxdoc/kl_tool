# -*- coding: utf-8 -*-
import os
import json
import sys
import csv
import requests
import datetime
import time

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

_STOCK_LIST = [
    (u'上证指数', '0000001'),
    (u'深证成指', '1399001'),
    (u'创业板指', '1399006'),
    (u'沪深300', '1399300'),
    (u'上证50', '0000016'),
    (u'中证500', '1399905')
]
_STOCK_FIELDS = 'TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;VOTURNOVER;VATURNOVER'
_stock_liem = lambda n, c, start='20020104', end='20210113': { \
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
            return fmt_func(val) if fmt_func else val
        except Exception as err:
            log('_parse_value tag:%s val:%s' % (fmt, val), 'ERROR')
            return def_func(val) if def_func else val

    return (key, _parse_value)

def build_row_func(fmt_str, cde='gbk'):
    fmt_arr = fmt_str.split(',')
    kv_tuple = [build_item_func(item, cde='gbk') for item in fmt_arr if item.strip()]
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
        for idx, row in enumerate(spamreader):
            fmt_str = ','.join(row).decode(cde) if idx == 0 and not fmt_str and skip == 1 else fmt_str
            if row_func is None and fmt_str:
                row_func = build_row_func(fmt_str, cde='gbk')

            if idx < skip:
                continue

            ret.append(row if row_func is None else row_func(row))

        return ret

def dump_json(out_file, obj):
    with open(out_file, 'w') as wf:
        json.dump(obj, wf, indent = 2)

def load_json(in_file):
    with open(in_file, 'r') as rf:
        return json.load(rf)

def build_matrix_data_pre(start_s, end_s, data, step=5):
    _int = lambda s: int(s.replace('-', ''))
    start_i = _int(start_s)
    end_i = _int(end_s)
    range_list = []
    for item in data:
        date_i = _int(item.get('date', '0'))
        if start_i <= date_i <= end_i:
            range_list.append((date_i, item.get('pchg', 0.0)))

    range_list.sort(key = lambda i: i[0])
    pchg_list = [i[1] for i in range_list]
    if len(pchg_list) < 2 * step:
        return None, None

    X, y = [], []
    for idx in range(0, len(pchg_list) - step):
        X.append(pchg_list[idx:idx + step])
        y.append(1 if pchg_list[idx + step] > 0 else 0)
    return X, y

def build_matrix_data_relativity(start_s, end_s, stock_data, code, step=5):
    _int = lambda s: int(s.replace('-', ''))
    start_i = _int(start_s)
    end_i = _int(end_s)

    pchg_map = {}
    for _code, data in stock_data.items():
        range_list = []
        for item in data:
            date_i = _int(item.get('date', '0'))
            if start_i <= date_i <= end_i:
                range_list.append((date_i, item.get('pchg', 0.0)))

        range_list.sort(key = lambda i: i[0])
        pchg_list = [i[1] for i in range_list]
        if len(pchg_list) < step:
            return None, None
        pchg_map[_code] = pchg_list

    X, y = [], []
    code_keys = set(pchg_map.keys())
    for idx in range(0, len(pchg_map[code]) - step):
        tmp_list = []
        for c in code_keys:
            tmp_list.extend(pchg_map[c][idx:idx + step])
        X.append(tmp_list)
        y.append(1 if pchg_map[code][idx + step] > 0 else 0)
    return X, y

def main():
    log('---------------Start-------------------')

    data_file = os.path.join(os.getcwd(), 'stock_data.json')

    if not os.path.isfile(data_file):
        stock_data = {c: load_data(v['csv'], v['url']) for c, v in STOCK_MAP.items()}
        dump_json(data_file, stock_data)
        log('write file %s' % (data_file, ))
    else:
        stock_data = load_json(data_file)
        log('read file %s' % (data_file, ))

    start_s = '2016-05-31'
    end_s = '2019-03-04'
    step = 3
    for code, data in stock_data.items():
        # 获取数据集特征  数据标签
        # X, y = build_matrix_data_pre(start_s, end_s, data, step)  ##  前%d天 同一指数 数据预测
        X, y = build_matrix_data_relativity(start_s, end_s, stock_data, code, step)  ## 前%d天  所有相关指数 数据预测
        if X is None or y is None:
            continue

        # 划分数据集
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1.0 / 4.0, random_state=10)

        model_dict = {
            u'KNN': KNeighborsClassifier(n_neighbors=7),
            u'逻辑回归': LogisticRegression(C=1e4, solver='liblinear', multi_class='auto'),     #正则化参数
            u'SVM': SVC(C=1e4, gamma='auto')  #正则化参数
        }
        stock = STOCK_MAP.get(code, {})
        print "\n\n==========================================="
        print u" 前%d天数据预测  代码:%s  名称:%s  范围:%s-%s" % (step, code, stock.get('name', ''), start_s, end_s)
        for model_name, model in model_dict.items():
            # 训练模型
            model.fit(X_train, y_train)
            # 验证模型
            acc = model.score(X_test, y_test)
            print u'{}模型的预测准确率:{:.2f}%'.format(model_name, acc * 100)

    log('---------------End--------------------')

if __name__ == '__main__':
    main()
