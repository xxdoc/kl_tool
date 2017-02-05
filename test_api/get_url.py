# -*- coding: utf-8 -*-
import requests
import os
import cPickle

def dump_obj(file_name, obj):
    with open(file_name, 'wb') as wf:
        cPickle.dump(obj, wf)

def load_obj(file_name):
    with open(file_name, 'rb') as rf:
        return cPickle.load(rf)

def get_url_set(url_file, tmp_file):
    if os.path.isfile(tmp_file):
        return load_obj(tmp_file)
    elif os.path.isfile(url_file):
        with open(url_file, 'r') as rf:
            tmp_set = list(rf.readlines())
            dump_obj(tmp_file, tmp_set)
            return tmp_set


def main():
    tmp_file = '_tmp_url_set.obj'
    url_file = 'url_list.txt'

    url_set = get_url_set(url_file, tmp_file)
    while url_set:
        url = url_set.pop(0)
        res = requests.get(url)
        if res.ok:
            print res.content
            dump_obj(tmp_file, url_set)


if __name__ == '__main__':
    main()
