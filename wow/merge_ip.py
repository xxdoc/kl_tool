#-*- coding: utf-8 -*-
import datetime
import os
import re
from httptool import walk_dir, _LOG

def load_ip(path):
    re_obj = re.compile('^([0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}:[0-9]{1,5})')
    line_list = []
    ip_list = []
    with open(path, 'r') as rf:
        line_list = rf.readlines()
    for line in line_list:
        tmp = re_obj.match(line)
        if tmp:
            ip_list.append(tmp.group())
    return ip_list

def main():
    txt_dict = walk_dir(os.getcwd(), lambda s: s.endswith('.txt'), 1)
    ip_dict = {}
    for path, name in txt_dict.items():
        ip_list = load_ip(path)
        _LOG('%s: len:%d' % (name, len(ip_list)))
        for ip in ip_list:
            ip_dict.setdefault(ip, 0)
            ip_dict[ip] += 1

    _LOG('%s: len:%d' % ('all', len(ip_dict)))
    print dict(sorted(ip_dict.items(), key=lambda t:t[1], reverse=True)[0:20])
    with open('all.ip', 'w') as wf:
        wf.writelines(['%s@HTTP\n'%(ip,) for ip in ip_dict.keys()])

if __name__ == '__main__':
    main()
    _LOG('\n============End=============\n')
