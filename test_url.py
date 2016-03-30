# -*- coding: utf-8 -*-
import urllib2
import gzip
import StringIO
import datetime
import urllib
import time
import json
import pymongo
import cPickle

MONGODB = pymongo.MongoClient('127.0.0.1', 27017)
MONGODB_CUR = MONGODB.dms.peidui


HTTP_TIME_OUT = 30
USER_AGENT = (
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/31.0.1650.63 Safari/537.36'
)
ACCEPT_ENCODING = 'gzip,deflate,sdch'


def getUrl(url, header_list=[], use_gzip=True, timeout=HTTP_TIME_OUT, proxy_info=None):
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
    for (h_tag, h_val) in header_list:
        req.add_header(h_tag, h_val)

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
    return data, headers


def main():
    peidui_dms = {'pub_key':'pub_45c328b9a41ad3d8e03e7b0def64f740',
            'sub_key':'sub_98fdec0e596145633a9735c8594369e0',
            's_key':'s_5c5d76ab1969382c093b5acb5ad97d2f',}


    wx25_dms = {'pub_key':"pub_8665bcf8fc7bdcffa983e7d7d5aaadd4",
                'sub_key':"sub_72f43c9452ba53c313edfe64e1c7eb61",
                's_key':'s_5b6e3a613a099609844c9b07fd1c0cdf',}



    #s_key = peidui_dms['s_key']
    s_key = wx25_dms['s_key']
    add_h = [('Authorization', 'dms ' + s_key), ('Content-Type', 'application/json')]

    topic = 'chat_3137'
    url = 'http://api.dms.aodianyun.com/v1/topics/' + topic + '/users?skip=0&num=100'
    print get_json(url, add_h)

    return None

    s_time = '2016-03-21 23:00:00'
    e_time = '2016-03-21 23:59:59'
    all_list = get_data(s_time, e_time, add_h)
    _LOG( "All get dms:%s" % (len(all_list),) )
    c = {}
    for i in all_list:
        key = i.get('topic', 'null')
        c[key] = c.get(key, 0) + 1
    a = c.items()
    a.sort(key=lambda i:i[1])
    for (key,num) in a:
        print key,',',num

def get_data(s_time, e_time, add_h, per_num=100):

    find_dict = {
        'skip':0,
        'num':per_num,
        #'topic':'chat_3429',
        'topic':'',
        'tartTime':s2t(s_time),
        'endTime':s2t(e_time)}
    obj_file = ('dump_%s_%s.obj' % (s_time, e_time)).replace(':','').replace(' ','_')
    all_list = []
    while 1:
        url = 'http://api.dms.aodianyun.com/v2/historys?'+urllib.urlencode(find_dict)
        json_obj = get_json(url, add_h)
        if len(json_obj)==0:
            break
##        try:
##            MONGODB_CUR.insert_many(json_obj)
##        except pymongo.errors.PyMongoError as ex:
##            _LOG( "PyMongoError %r:%s." % (ex, ex) )
        find_dict['skip'] += per_num
        all_list.extend(json_obj)
    save_obj(all_list, obj_file)
    return all_list

def save_obj(obj, sf):
    with open(sf, 'wb') as wf:
        cPickle.dump(obj, wf)

def load_obj(lf):
    with open(lf, 'rb') as rf:
        return cPickle.load(rf)

def s2t(str_in, str_f='%Y-%m-%d %H:%M:%S'):
    time_int = time.mktime(time.strptime(str_in, str_f))
    return int(time_int)

def get_json(url, add_h):
    try:
        _LOG( "Info get url:%s" % (url,) )
        data, headers = getUrl(url, add_h)
        return json.loads(data)
    except Exception as ex:
        _LOG( "Error %r:%s.\nURL:%s" % (ex, ex, url) )


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

if __name__ == '__main__':
    main()


"""
use dms
db.peidui.ensureIndex({"topic":1})
db.peidui.ensureIndex({"time":1})
db.peidui.ensureIndex({"msg":1})
db.peidui.getIndexes()
"""