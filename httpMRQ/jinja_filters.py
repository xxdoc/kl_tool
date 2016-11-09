#-*- coding: utf-8 -*-
import time
import json

def dateformat(value, fmt='%Y-%m-%d'):
    return time.strftime(fmt, time.localtime(value))

def jsonstringify(value, indent=2):
    return json.dumps(value, indent=indent)