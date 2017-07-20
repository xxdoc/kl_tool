#-*- coding: utf-8 -*-

import os
import sys
import socket

import lxml.html
import chardet
import re

import datetime
import time
import random

import urllib
import urllib2
import sqlite3

import win32con
import win32api
import win32com.client

import thread
from Queue import Queue, Empty, Full
from urlparse import urlparse

def get_url_path(in_url, in_path=None):
    url_path = None
    in_url = in_url if in_url else ''
    try:
        in_url = 'http://' + in_url if '://' not in in_url else in_url
        url_path = _get_url_path(in_url, in_path) if in_url[:in_url.index('://')] in ('http','https','ftp') else None
    except Exception, ex:
        print '\n','get_url_path err:', in_url, '->', ex
    return url_path

def _get_url_path(in_url, in_path):
    in_path = in_path if (in_path) else os.getcwd()
    if not os.path.exists(in_path): os.makedirs(in_path)
    in_url = unicodeToStr(in_url,'utf-8')

    de_url = in_url
    if '%' in in_url:
        de_url = url_decode_str(in_url)

    url = urlparse(de_url)
    url.in_url = in_url
    url.de_url = de_url

    url.fix_path = url.path
    if url.fix_path=='' or  url.fix_path[:1]!='/':
        url.fix_path = '/' + url.fix_path
    if '.' not in url.fix_path[url.fix_path.rindex("/")+1:] and url.fix_path[-1:]!='/':
        url.fix_path = url.fix_path + '/'

    while '/...' in url.fix_path or '/ ' in url.fix_path or '//' in url.fix_path or '/. ' in url.fix_path or '/.. ' in url.fix_path:
        url.fix_path = url.fix_path.replace('/...', '/..').replace('/ ', '/').replace('//', '/').replace('/. ', '/.').replace('/.. ', '/..')

    url.split_list = url.fix_path.split('/')
    i = 0L
    while i < len(url.split_list):
        if url.split_list[i] == '.':
            del url.split_list[i]
            i -= 1
        if url.split_list[i] == ' ':
            del url.split_list[i]
            i -= 1
        if url.split_list[i] == '..' :
            del url.split_list[i]
            if url.split_list[i-1]!='':
                del url.split_list[i-1]
                i -= 1
            i -= 1
        i += 1

    url.fix_path = '/'.join(url.split_list)

    try:
        url.fix_url = url.in_url.replace('%s://%s%s' % (url.scheme, url.netloc, url.path), '%s://%s%s' % (url.scheme, url.netloc, url_encode_str(url.fix_path)), 1)
    except:
        url.fix_url = url.in_url.replace('%s://%s%s' % (url.scheme, url.netloc, url.path), '%s://%s%s' % (url.scheme, url.netloc, url.fix_path), 1)

    try:
        #print url.fix_path.decode("utf-8").encode("gbk")
        url.fix_path = strToUnicode(url.fix_path, 'utf-8')
    except Exception, ex:
        print '\n','url decode err:', url.fix_path, '->', ex

    url.baseurl = url.fix_url.split('?')[0].split('#')[0]
    url.baseurl = url.baseurl[:url.baseurl.rindex("/")+1]
    url.filename = url.fix_path[url.fix_path.rindex("/")+1:] if url.fix_path[-1:]!='/' else 'index.html'
    url.filetype = url.filename[url.filename.rindex(".")+1:].lower() if '.' in url.filename else ''
    url.save_path = os.path.join(in_path, url.hostname, url.fix_path[1:]) if url.fix_path[-1:]!='/' else os.path.join(in_path, url.hostname, url.fix_path[1:], 'index.html')
    url.save_path = os.path.abspath(url.save_path)
    url.save_dir = os.path.dirname(url.save_path)

    #print url.fix_url.decode("utf-8").encode("gbk")
    #if not os.path.exists(url.save_dir): os.makedirs(url.save_dir)
    return url

def url_decode_str(in_url):
    out_url = urllib.unquote(in_url)
    return out_url

def url_encode_str(in_url):
    out_url = urllib.quote(in_url)
    return out_url

def strToUnicode(html, decoding=None):
    if not isinstance(html, unicode):
        if not decoding:
            decoding, charJust = '', chardet.detect(html)
            try: decoding = 'gbk' if charJust['encoding'].lower() == 'gb2312' else charJust['encoding']
            except Exception, e: print 'strToUnicode chardet detect error:', Exception, '->', e
        decoding = 'utf-8' if not decoding else decoding
        if decoding: html = html.decode(decoding, 'ignore')
    return html

def unicodeToStr(html, encoding='utf-8'):
    if not isinstance(html, unicode):
        decoding, charJust = '', chardet.detect(html)
        try: decoding = 'gbk' if charJust['encoding'].lower() == 'gb2312' else charJust['encoding']
        except Exception, e: print 'unicodeToStr chardet detect error:', Exception, '->', e
        if encoding and decoding and decoding!=encoding : html = html.decode(decoding, 'ignore').encode(encoding, 'ignore')
    else:
        if encoding: html = html.encode(encoding, 'ignore')
    return html


def enable_global_proxy(proxy_http="http", proxy_url="http://127.0.0.1:8087",enable_proxy = True):
    if enable_proxy: opener = urllib2.build_opener(urllib2.ProxyHandler({proxy_http : proxy_url}))
    else: opener = urllib2.build_opener(urllib2.ProxyHandler({}))
    urllib2.install_opener(opener)


def log_with_time(str_log, new_line = None, enter = True):
    if new_line: print '\n',
    if enter: print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S  '),str_log
    else: print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S  '),str_log,

def log_with_info(str_log, new_line = None, enter = None):
    str_temp = (str_log) if (not new_line) else ('\n' + str_log)
    if enter: print str_temp
    else: print str_temp,


def base_log(msg):
    print msg

def base_fail_op(task, status, log):
    if log: log('fail op.id = %s url = %s, status = %d' % (str(task['id']), task['url_print'], status))


def get_remote_data(
    tasks,
    results,
    fail_op=base_fail_op,
    log=base_log,
    ):

    while True:
        task = tasks.get()
        res = 0L
        tid = task['id']
        in_obj = task['in_obj']

        try:
            res = in_obj._download()
        except Exception, ex:
            print '\n', str(tid), 'do task err:', Exception, '->', ex
            res = -10L
        finally:
            results.put((tid, res, in_obj), True)

class HttpPool(object):

    def __init__(
        self,
        threads_count=30,
        doing_count=20,
        fail_op=base_fail_op,
        log=base_log,
        ):

        self._tasks, self._results = Queue(), Queue()
        self._threads_count_max, self._doing_count_max = threads_count, doing_count;
        self._doing_count_now = 0L;

        for i in xrange(threads_count):
            thread.start_new_thread(get_remote_data, (self._tasks,
                                    self._results, fail_op, log))

    def add_task(self, tid, in_obj=None):
        task = {'id': tid, 'in_obj':in_obj}
        results = False
        if self._doing_count_now < self._threads_count_max:
            try:
                self._tasks.put_nowait(task)
                self._doing_count_now = self._doing_count_now + 1
                results = True
            except Full:
                pass
        return results

    def get_results(self):
        results = []
        if self._doing_count_now > 0:
            while True:
                try:
                    res = self._results.get_nowait()
                except Empty:
                    break
                self._doing_count_now = self._doing_count_now - 1
                results.append(res)
        return results

    def get_doing_count_now(self):
        return self._doing_count_now

    def get_threads_count_max(self):
        return self._threads_count_max

    def get_doing_count_max(self):
        return self._doing_count_max

    def set_doing_count_now(self,set_do):
        self._doing_count_now = set_do
        return self._doing_count_now


class Retrieve(object):

    def __init__(self, url, path):
        self.url = url
        self.file = path
        self.save_dir = os.path.dirname(path)
        self.content = None
        if not os.path.exists(self.save_dir):
            try:
                os.makedirs(self.save_dir)
            except Exception, e:
                print 'makedirs error:', e

    def _download(self):
        """下载文件"""
        results = 0L
        socket.setdefaulttimeout(30)
        try:
            real_url = self.url
#           result = urllib.urlretrieve(real_url, self.file)
            http_req = urllib.urlopen(real_url)
            http_code = http_req.getcode()
            if http_code==200:
                http_res = urllib.urlretrieve(real_url, self.file)
                self.content = http_res
                result = os.path.getsize(self.file) if os.path.isfile(self.file) else 0L
            else:
                #print 'http error:', ' http_code ->', http_code
                result = -http_code
        except Exception, e:
            print '\n','download error:', Exception, '->', e,'\n','url ->', self.url
            if os.path.isfile(self.file):
                print 'try remove file : ',self.file
                try: os.remove(self.file)
                except: pass
            result = -900L
        return result

class Crawl(object):

    def __init__(self, in_hp, in_path=None):
        in_path = in_path if (in_path) else os.getcwd()
        if not os.path.exists(in_path): os.makedirs(in_path)
        self.hp = in_hp
        self.in_path = in_path

    def getPage(self, task_info):
        task_id, res, rv = task_info[:3]
        result = self.doPage(res)

        del rv
        return result

    def doPage(self, res):
        if res <= 0: return res
        link_count = 1L
        return link_count

    def add_task_creature_jpg(base_int):
        portrait_url = r'http://content.battlenet.com.cn/wow/renders/npcs/portrait/creature%s.jpg'
        base_name = r'creature%s.jpg'
        str_int = '%s%03d'

        list_down_all = []
        for i in range(0,1000):
            item_str = str_int % (base_int, i)
            file_url = base_url % item_str
            file_name = base_name % item_str
            item_dict = {'file_url':file_url, 'file_name':file_name, 'ps_text':'', 'from_url':''}
            list_down_all.append(item_dict)

        #list_down_all = [{'file_url':file_url, 'file_name':file_name, 'ps_text':ps_text, 'from_url':from_url}]
        #[file_url, file_name, ps_text, from_url]
        ThunderAgent = win32com.client.Dispatch("ThunderAgent.Agent.1")
        for down_info in list_down_all:
            ThunderAgent.AddTask12(down_info['file_url'], down_info['file_name'], "", down_info['ps_text'], down_info['from_url'], "", -1, 0, -1,  "", "", "", 0, "rightup")
        ThunderAgent.CommitTasks2(1)

    def go(self, base_int):
        base_path = os.path.join(self.in_path, 'content.battlenet.com.cn\\wow\\renders\\npcs\\portrait\\creature%s.jpg')
        base_url = r'http://content.battlenet.com.cn/wow/renders/npcs/portrait/creature%s.jpg'

        download_count = 0L
        for i in range(0,1000):
            item_str = '%s%03d' % (base_int, i) if base_int>0 else '%s' % (i)
            item_dict = {'file_url': base_url % item_str , 'file_name': base_path % item_str , 'ps_text':'', 'from_url':''}
            download_count += self.addPage(base_int*1000+i, item_dict)

        if self.hp.get_doing_count_now() > 0:
            download_count += self.waitPage()
        return download_count

    def initPage(self, item_dict):
        rv = None
        if item_dict and not os.path.isfile(item_dict['file_name']):
            rv = Retrieve(item_dict['file_url'], item_dict['file_name'])
        return rv

    def addPage(self, task_id, item_dict):
        add_count = 0L
        rv = self.initPage(item_dict) if item_dict else None
        #if rv: print '\n',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S ->'),task_id,' download link -> ', rv.url
        #else: log_with_info("%s(pass)" % (task_id))

        while rv:
            if rv and self.hp.get_doing_count_now() < self.hp.get_doing_count_max():
                if self.hp.add_task(task_id, rv):
                    #log_with_info("%s(add)" % (task_id))
                    rv = None
            results = self.hp.get_results()
            if not results:
                pass
                time.sleep(0.05 * random.random())
            else:
                for info in results:
                    tr_count = self.getPage(info)
                    if tr_count >= 0 :log_with_info('%s(+%s)' % (info[0], tr_count) )
                    #else:log_with_info('%s(err:%s)' % (info[0], tr_count) )
                    add_count = add_count + tr_count if tr_count >= 0 else add_count

        return add_count

    def waitPage(self):
        add_count = 0L

        count_waite = 0L
        while self.hp.get_doing_count_now() > 0:
            results = self.hp.get_results()
            if not results:
                if count_waite > 200 or count_waite > self.hp.get_doing_count_now()*50:
                    self.hp.set_doing_count_now(0)
                    break;
                time.sleep(1.0 * random.random())
                count_waite += 1
                log_with_info('.')
            else:
                count_waite = 0L
                for info in results:
                    tr_count = self.getPage(info)
                    if tr_count >= 0 :log_with_info('%s(+%s)' % (info[0], tr_count) )
                    else:log_with_info('%s(err:%s)' % (info[0], tr_count) )
                    add_count = add_count + tr_count if tr_count >= 0 else add_count

        return add_count

    def addTask(self,base_int=None):
        base_int = base_int if base_int else 0L
        ThunderAgent = win32com.client.Dispatch("ThunderAgent.Agent.1")
        base_path = os.path.join(self.in_path, 'content.battlenet.com.cn\\wow\\renders\\npcs\\portrait\\')
        base_url = r'http://content.battlenet.com.cn/wow/renders/npcs/rotate/%s'

        file_dict = {}
        [file_dict.setdefault(str2int(x), x) for x in os.listdir(base_path) if os.path.splitext(x)[1]=='.jpg']

        file_dict_keys = file_dict.keys()
        file_dict_keys.sort(key=lambda x:x)

        add_count = 0L
        list_down_all = []
        for i in file_dict_keys:
            item_dict = {'file_url':base_url % file_dict[i], 'file_name':file_dict[i], 'ps_text':'', 'from_url':''}
            list_down_all.append(item_dict)
            del file_dict[i]
            if len(list_down_all) == 999 or len(file_dict) == 0:
                if add_count == base_int:
                    for down_info in list_down_all:
                        ThunderAgent.AddTask12(down_info['file_url'], down_info['file_name'], "", down_info['ps_text'], down_info['from_url'], "", -1, 0, -1,  "", "", "", 0, "rightup")
                    ThunderAgent.CommitTasks2(1)
                    break
                add_count, list_down_all = add_count + 1, []

        return len(list_down_all)

def str2int(in_str, sys_dep=10):
    in_str = in_str if in_str else ''
    res_int = 0L
    for char_item in in_str:
        res_int = res_int*sys_dep + int(char_item) if char_item.isdigit() else res_int
    return res_int

def main():
    main_count = 0L
    main_start = datetime.datetime.now()

    hp = HttpPool(threads_count=50, doing_count=40, fail_op=base_fail_op, log=base_log)
    #enable_global_proxy(proxy_http="http", proxy_url="http://127.0.0.1:8087",enable_proxy = True)

    cr = Crawl(hp)
    main_count = cr.addTask(2)
##    for i in range(73,2000):
##        print '\n',i,' -> is doing ...'
##        main_count = cr.go(i)
##        print '\n\n',i,' -> is done :',main_count


    print '\n',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S  '),str(main_count),' items OVER!'
    main_end = datetime.datetime.now()
    print '\n','USE Time : ',str(main_end - main_start)


if __name__ == '__main__':
    main()