#-*- coding: utf-8 -*-
import urllib2
import os
import inspect
import random
from schema import Schema, SchemaError, Regex, And, Use, Optional
from flask import request
from mrq.dashboard.utils import jsonify

from mrq.task import Task
from functools import update_wrapper
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

HttpUrlSchema = And(basestring, len, Regex(r'^(http|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?$'))

def TaskSchemaWrapper(*args, **kwgs):
    schema = Schema(*args, **kwgs)

    def _wrapper(func):
        func.params_schema = schema
        return func

    return _wrapper

def fixTaskParams(all_dict, task, args):
    cls = all_dict.get(task, None)
    if not cls or not issubclass(cls, Task):
        return None, ApiErrorBuild('task:%s is not allowed' % (task,), 531)
    schema = getattr(cls.run, 'params_schema', None)
    ex = None
    if not schema:
        return  args, ex
    else:
        try:
            return schema.validate(args), ex
        except SchemaError as ex:
            return None, ApiErrorBuild('%s:%s' % (ex.__class__.__name__, ex), 511)

def ApiSchemaWrapper(*args, **kwgs):
    schema = Schema(*args, **kwgs)

    def _wrapper(func):

        def api(*func_args, **func_kwgs):
            args = request.args.to_dict()
            try:
                params = schema.validate(args)
                return jsonify(func(**params))
            except SchemaError as ex:
                return jsonify(ApiErrorBuild('%s:%s' % (ex.__class__.__name__, ex), 511))

        update_wrapper(api, func)
        api.params_schema = schema
        return api

    return _wrapper

def ApiErrorBuild(msg='something is error', code=None, errors=None):
    if msg and isinstance(msg, (list, tuple)) and code is None and errors is None:
        return ApiErrorBuild(*msg)
    elif isinstance(msg, Exception):
        code = getattr(msg, 'code', 551) if code is None else code #默认异常错误码 551
        msg = '%s:%s' % (msg.__class__.__name__, msg.message)

    code = 500 if code is None else abs(int(code))
    err = {'code':code, 'message': msg}
    if errors:
        err['errors'] = [ApiErrorBuild(item) for item in errors]
    return {'error': err}
