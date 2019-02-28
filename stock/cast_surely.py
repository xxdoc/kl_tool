# -*- coding: utf-8 -*-
import os
import json
import sys
import csv

def parse_value_auto(val):
    if val.isdecimal():
        return int(val)
    try:
        return float(val)
    except ValueError:
        return val

def build_item_func(item, cde='gbk'):
    item = item.strip()
    item_arr = item.split('#', 1)
    key = item_arr[0]
    fmt = item_arr[1] if len(item_arr) >= 2 else ''
    func_map = {
        'i': lambda v: int(v),
        'f': lambda v: float(v),
        'a': parse_value_auto
    }
    fmt = 'a' if not fmt else fmt

    fmt_func = func_map[fmt] if fmt in func_map else None

    def _parse_value(val):
        val = val.decode(cde)
        return fmt_func(val) if fmt_func else val

    return (key, _parse_value)

def build_row_func(fmt_str, cde='gbk'):
    fmt_arr = fmt_str.split(',')
    kv_tuple = [build_item_func(item, cde='gbk') for item in fmt_arr if item.strip()]
    def _parse_row(row):
        return {k: f(row[idx]) for idx, (k, f) in enumerate(kv_tuple)}
    return _parse_row

def load_data(in_file, fmt_str = '', skip = 1, cde='gbk'):
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

def main():
    print '\n---------------Start-------------------\n'
    csv_file = sys.argv[1].strip() if len(sys.argv) >= 2 and sys.argv[1].strip() else os.path.join(os.getcwd(), 'zxc.log')

    defult_file = '399300.csv'
    if not os.path.isfile(csv_file) and os.path.isfile(os.path.join(os.getcwd(), defult_file)):
        csv_file = os.path.join(os.getcwd(), defult_file)
    out_file = defult_file + '.json'

    if not os.path.isfile(csv_file):
        print 'No input specified, use as python xx.py abc.log.'
        return

    stock_data = load_data(csv_file)
    print '\n read file', csv_file

    dump_json(out_file, stock_data)
    print '\n write file', out_file

    print '\n---------------End--------------------\n'

if __name__ == '__main__':
    main()
