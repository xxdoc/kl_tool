#-*- coding: utf-8 -*-
import datetime
import pyhtml
import pyjson

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