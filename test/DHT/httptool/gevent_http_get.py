#-*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool
import urllib2
import gzip
import datetime
import random
import StringIO

class MultiHttpDownLoad(object):
    user_agent = (
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/31.0.1650.63 Safari/537.36'
    )
    accept_encoding = 'gzip,deflate,sdch'

    def __init__(self, spawn_num, error_max=5, http_time_out=30, proxy_list=None, logger=None):
        self.spawn_num = int(spawn_num)
        self.error_max = int(error_max)
        self.http_time_out = int(http_time_out)
        self.proxy_list = [item.strip() for item in proxy_list if item.strip()] if proxy_list else []
        self.logger = logger

    def log(self, msg, tag='DEBUG'):
        tag = tag.upper()
        if self.logger and getattr(self.logger, 'log', None):
            logger.log(msg, tag)
        else:
            time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            print '%s [%s] %s' % (time_str, tag, msg)

    def get_http_list(self, url_list, do_data, isok_func=lambda d,h:isinstance(d, str) and d, use_gzip=True):
        def _do_get(idx, url, isok_func, use_gzip):
            data, headers = self.__get_data(url, isok_func, use_gzip)
            self.log('get data:%s(length:%d)<idx:%d>' % (url, len(data), idx), 'INFO')
            do_data(url, data, headers)

        if not hasattr(do_data, '__call__') or not hasattr(isok_func, '__call__'):
            fault_msg = 'do_data and isok_func must be callable'
            self.log(fault_msg, 'FAULT')
            raise ValueError(fault_msg)
        if not url_list:
            return None

        gpool = Pool(self.spawn_num) if self.spawn_num > 1 else None
        for idx, url in enumerate(url_list):
            if self.spawn_num>1:
                gpool.spawn(_do_get, idx, url, isok_func, use_gzip)
            else:
                _do_get(idx, url, isok_func, use_gzip)

        if self.spawn_num>1:
            gpool.join()

    def __get_proxy(self):
        if self.proxy_list and isinstance(self.proxy_list, list):
            return random.choice(self.proxy_list)
        else:
            return None

    def __get_data(self, url, isok_func, use_gzip):
        data, headers, proxy_info = '', {}, None
        error_count = 0
        while 1:
            if data is None:
                proxy_info = self.__get_proxy()
                error_count += 1
                self.log('%suse proxy:%s(%s)<err:%d>' % ('.'*error_count, url, proxy_info, error_count), 'ERROR')
                if error_count >= self.error_max:
                    self.log('failure in:%s' % (url, ), 'FAULT')
                    return '', {}

            try:
                data, headers, proxy_info = self.__get_url(url, use_gzip=use_gzip, proxy_info=proxy_info)
            except Exception as ex:
                self.log('get_data error:%s <%s>' % (ex, proxy_info), 'ERROR')

            if isok_func(data, headers):
                return data, headers
            else:
                data = None

    def __get_url(self, url, use_gzip=True, proxy_info=None):
        if not url:
            return '', {}, None

        if proxy_info:
            proxy_support = urllib2.ProxyHandler({"http" : "http://%s" % proxy_info})
            opener = urllib2.build_opener(proxy_support)
            urllib2.install_opener(opener)

        req = urllib2.Request(url)

        if use_gzip:
            req.add_header('Accept-Encoding', self.accept_encoding)
        req.add_header('User-Agent', self.user_agent)
        res = urllib2.urlopen(req, timeout=self.http_time_out)



        headers, data = res.headers, res.read()
        if headers.getheader('Content-Encoding', default='').lower()=='gzip':
            try:
                data = gzip.GzipFile(fileobj=StringIO.StringIO(data)).read()
            except Exception as ex:
                if use_gzip:
                    return self.__get_url(url, use_gzip=False, proxy_info=proxy_info)
                else:
                    raise ex
        return data, dict(headers), proxy_info



def main():
    def get_proxy():
        with open('ip.txt', 'r') as rf:
            proxy_list = [i.strip() for i in rf if ':' in i]
        return proxy_list

    proxy_list = get_proxy()
    proxy_list = None
    test = MultiHttpDownLoad(50, proxy_list=proxy_list)

    url_file_map = {
        'http://1541q47p51.iok.la:61208/': 'glances.html',
        'http://baidu.com': 'baidu.html',
        'http://g.cn': 'google.html',
        #'http://facebook.com': 'facebook.html'
    }

    def do_data(url, data, headers):
        file_str = url_file_map.get(url, '')
        if file_str:
            with open(file_str, 'w') as wf:
                wf.write(data)

    test.get_http_list(url_file_map.keys() * 5, do_data)

if __name__ == '__main__':
    main()

