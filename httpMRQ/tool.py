#-*- coding: utf-8 -*-
import urllib2
import os
import random
from schema import Schema, SchemaError
from mrq.task import Task

ALL_ERROR = Exception

HTTP_ERROR_MAX = 10
HTTP_TIME_OUT = 30
USER_AGENT = (
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/31.0.1650.63 Safari/537.36'
)
ACCEPT_ENCODING = 'gzip,deflate,sdch'



def getUrl(url, use_gzip=True, timeout=HTTP_TIME_OUT, proxy_info=None):
    if not url:
        return ''

    if proxy_info:
        proxy_support = urllib2.ProxyHandler({"http" : "http://%s" % proxy_info})
        opener = urllib2.build_opener(proxy_support)
        urllib2.install_opener(opener)
        getUrl.proxy_info = proxy_info

    req = urllib2.Request(url)
    if use_gzip:
        req.add_header('Accept-Encoding', ACCEPT_ENCODING)
    req.add_header('User-Agent', USER_AGENT)
    res = urllib2.urlopen(req, timeout=timeout)

    headers, data = res.headers, res.read()
    if headers.getheader('Content-Encoding', default='').lower()=='gzip':
        try:
            data = gzip.GzipFile(fileobj=StringIO.StringIO(data)).read()
        except KeyboardInterrupt as ex:
            raise ex
        except ALL_ERROR:
            if use_gzip:
                return getUrl(url, use_gzip=False, timeout=timeout, proxy_info=proxy_info)
    return data

def getProxy():
    proxy_list = getattr(getProxy, 'proxy_list', None)
    if proxy_list is None and os.path.isfile(os.path.join(os.getcwd(), 'ip.txt')):
        with open('ip.txt', 'r') as rf:
            proxy_list = [i.replace('\n', '') for i in rf if ':' in i]
        getProxy.proxy_list = proxy_list
    if proxy_list:
        return random.choice(proxy_list)
    return None

def SchemaWrapper(*args, **kwgs):
    schema = Schema(*args, **kwgs)

    def _wrapper(func):
        func.params_schema = schema
        return func

    return _wrapper

def fixParams(all_dict, task, args):
    cls = all_dict.get(task, None)
    if not cls or not issubclass(cls, Task):
        return None, {'error': 'task:%s is not allowed' % (task,) }
    schema = getattr(cls.run, 'params_schema', None)
    ex = None
    if not schema:
        return  args, ex
    else:
        try:
            return schema.validate(args), ex
        except SchemaError as ex:
            return None, {'error': '%s:%s' % (ex.__class__.__name__, ex)}