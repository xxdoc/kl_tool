# -*- coding: utf-8 -*-
from gevent import monkey;monkey.patch_all()
import os
import requests
from pykl import pyhttp

def load_str(file_name):
    with open(file_name, 'r') as rf:
        return rf.read()

def dump_str(file_str, file_name):
    with open(file_name, 'wb') as wf:
        wf.write(file_str)

def main():
    list_file = 'imgs.txt'
    img_list = [i.strip() for i in load_str(list_file).split('\n') if i.strip()]
    path_arr = lambda s: s.split('://')[1].split('/')[1:]
    file_path = lambda s: os.path.join(os.getcwd(), 'imgs', *path_arr(s))
    img_map = {u: file_path(u) for u in img_list if not os.path.isfile(file_path(u))}
    dir_list = set([os.path.dirname(p) for p in img_map.values()])
    [os.makedirs(p) for p in dir_list if not os.path.exists(p)]

    pool = pyhttp.MultiHttpDownLoad(10)
    def do_get(url, data, headers):
        print url, ' => ', len(data)
        file_path = img_map.get(url, '')
        if file_path and len(data) > 100:
            dump_str(data, file_path)

    pool.get_http_list(img_map.keys(), do_get)
    print 'END'

if __name__ == '__main__':
    main()