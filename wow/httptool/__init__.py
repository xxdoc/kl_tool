#-*- coding: utf-8 -*-
import datetime
import pyhtml
import pyjson
import os

from gevent_http_get import MultiHttpDownLoad

def _LOG(msg_in, time_now=True, new_line=True):
    if time_now:
        time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        msg = '%s => %s' % (time_str, msg_in)
    if getattr(_LOG, 'log_file', None):
        _LOG.log_file.write(msg+'\n')
        _LOG.log_file.flush()

    if new_line:
        print msg
    else:
        print msg,

def load_str(file_name):
    with open(file_name, 'r') as rf:
        return rf.read()

def walk_dir(str_dir, filter_func=None, max_deep=-1):
    ret_dict = {}
    str_dir = str_dir.encode('GBK', 'ignore') if isinstance(str_dir, unicode) else str_dir
    if max_deep==0 or not isinstance(str_dir, str) or not os.path.isdir(str_dir):
        return ret_dict

    current_files = os.listdir(str_dir)
    for file_name in current_files:
        full_name = os.path.join(str_dir, file_name)
        if os.path.isfile(full_name):
            if filter_func is not None:
                if filter_func(file_name):
                    ret_dict[full_name] = file_name
            else:
                ret_dict[full_name] = file_name
        elif os.path.isdir(full_name):
            tmp_dict = walk_dir(full_name, filter_func, max_deep-1)
            ret_dict.update(tmp_dict)

    return ret_dict