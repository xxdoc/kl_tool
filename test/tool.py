# -*- coding: utf-8 -*-
import urllib2
import os
import gzip
import StringIO
import datetime
import urllib
import time
import json
import pymongo
import cPickle
import inspect
import base64

ALL_ERROR = Exception

#================================================
#=================== CHAT MSG ===================
#================================================

def chat_msg(uid, msg, _loc='杭州市', _key="3b8f3f656692f998f6625a0a8d50270e"):
    api_doc = {100000:'文本类', 200000:'链接类', 302000:'新闻类',
                308000:'菜谱类', 313000:'（儿童版）儿歌类', 314000:'（儿童版）'}
    msg = msg.encode('utf-8', 'ignore') if isinstance(msg, unicode) else msg
    args = {'key':_key, 'info':msg, 'loc':_loc, 'userid':uid}
    url = r"http://www.tuling123.com/openapi/api?" + urllib.urlencode(args)
    obj = get_json(url)
    if obj.get('code', 0) in api_doc:
        return obj.get('text', None)
    else:
        return None

#================================================
#================ENCRYPT DECRYPT=================
#================================================

def encrypt(str_in, skey):
    skey = skey[::-1]
    strArr = [i for i in base64.b64encode(str_in)]
    strCount = len(strArr)
    for (key, value) in enumerate(skey):
        if key < strCount:
            strArr[key] += value
    return ''.join(strArr).replace('=', 'O0O0O')

def decrypt(str_in, skey):
    skey = skey[::-1]
    strArr = [a+b for (a,b) in zip(*([iter(str_in.replace('O0O0O', '='))] * 2))]
    strCount = len(strArr);
    for (key, value) in enumerate(skey):
        if (key < strCount):
            strArr[key] = strArr[key].rstrip(value)
    return base64.b64decode(''.join(strArr))

#================================================
#=====================HTTP GET===================
#================================================

HTTP_TIME_OUT = 30
USER_AGENT = (
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/31.0.1650.63 Safari/537.36'
)
ACCEPT_ENCODING = 'gzip,deflate,sdch'

def getUrl(url, header=None, use_gzip=True, timeout=HTTP_TIME_OUT, proxy_info=None):
    if not url:
        return '', None

    if proxy_info:
        proxy_support = urllib2.ProxyHandler({"http" : "http://%s" % proxy_info})
        opener = urllib2.build_opener(proxy_support)
        urllib2.install_opener(opener)
        getUrl.proxy_info = proxy_info

    req = urllib2.Request(url)
    if use_gzip:
        req.add_header('Accept-Encoding', ACCEPT_ENCODING)
    if header and isinstance(header, dict):
        for (h_tag, h_val) in header.items():
            req.add_header(h_tag, h_val)

    req.add_header('User-Agent', USER_AGENT)
    res = urllib2.urlopen(req, timeout=timeout)
    headers, data = res.headers, res.read()
    if headers.getheader('Content-Encoding', default='').lower()=='gzip':
        try:
            data = gzip.GzipFile(fileobj=StringIO.StringIO(data)).read()
        except ALL_ERROR as ex:
            if use_gzip:
                return getUrl(url, use_gzip=False, timeout=timeout, proxy_info=proxy_info)
    return data, headers

#================================================
#====================SAVE LOAD===================
#================================================

def load_json(json_file):
    with open(json_file, 'r') as rf:
        return json.load(rf)

def dump_json(obj, json_file):
    with open(json_file, 'w') as wf:
        json.dump(obj, wf)

def save_obj(obj, sf):
    with open(sf, 'wb') as wf:
        cPickle.dump(obj, wf)

def load_obj(lf):
    with open(lf, 'rb') as rf:
        return cPickle.load(rf)

def s2t(str_in, str_f='%Y-%m-%d %H:%M:%S'):
    time_int = time.mktime(time.strptime(str_in, str_f))
    return int(time_int)

def get_json(url, add_h=None):
    try:
        data, headers = getUrl(url, add_h)
        return json.loads(data)
    except ALL_ERROR as ex:
        _LOG( "get_json Error %r:%s.\nURL:%s" % (ex, ex, url) )


def get_dir_file(p, is_ok, key):
    f = lambda p, x :os.path.join(p,x)
    info = lambda ff:{'ctime': os.path.getctime(ff), \
                        'size':os.path.getsize(ff), \
                        'mtime':os.path.getmtime(ff), \
                        'atime':os.path.getatime(ff)}
    tmp = [(f(p,x), info(f(p,x))) for x in os.listdir(p) if os.path.isfile(f(p,x)) and is_ok(x)]
    tmp.sort(key=key)
    return tmp
#================================================
#=====================DOC LOG====================
#================================================

def _LOG(msg_in, time_now=True, new_line=True):
    if time_now:
        time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        msg_in = u'%s => %s' % (time_str, msg_in)
    if getattr(_LOG, 'log_file', None):
        _LOG.log_file.write(msg_in+'\n')
        _LOG.log_file.flush()

    if isinstance(msg_in, unicode):
        msg_in = msg_in.encode('gbk', 'ignore')

    if new_line:
        print msg_in
    else:
        print msg_in,

def func_doc(g):
    if inspect.isfunction(g):
        print g.__name__,'; doc:',g.__doc__, '; args:',inspect.getargspec(g)
    elif inspect.isclass(g):
        print repe(g),'doc:',g.__doc__

#================================================
#======================MAIN======================
#================================================

def main():
    for _, g in globals().items():
        func_doc(g)

if __name__ == '__main__':
    main()


"""
use dms
db.peidui.ensureIndex({"topic":1})
db.peidui.ensureIndex({"time":1})
db.peidui.ensureIndex({"msg":1})
db.peidui.getIndexes()
"""