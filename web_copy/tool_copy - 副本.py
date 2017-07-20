# -*- coding: utf-8 -*-
import os
import requests

def load_str(file_name):
    with open(file_name, 'r') as rf:
        return rf.read()

def dump_str(file_str, file_name):
    with open(file_name, 'w') as wf:
        wf.write(file_str)

def url2file(url):
    replace_dict = {
        ':': '_',
        ' ': '',
        '?': '_',
        '/': '',
        '\\': '',
        '#': '_',
        '*': '_',
        '&': '_',
    }
    for s1, s2 in replace_dict.items():
        url = url.replace(s1, s2)
    return url + '.tmp'

def get_url(url, cache_path=None):
    tmp_file = os.path.join(cache_path, url2file(url)) if cache_path else None
    cache_path and not os.path.isdir(cache_path) and os.mkdir(cache_path)

    if cache_path and os.path.isfile(tmp_file):
        page_html = load_str(tmp_file)
    else:
        res = requests.get(url)
        page_html = res.content if res.ok else ''
        cache_path and dump_str(page_html, tmp_file)
    return page_html




def test_charset(html):
    res_charset = ''

    if self.content and self.content[1].plist :
        for item in self.content[1].plist:
            item = str(item).strip()
            if item[:7].lower()=='charset': res_charset = item[item.rindex('=')+1:].strip().lower()
    elif res_charset == '':
        charJust = chardet.detect(html)
        try:
            res_charset = 'gbk' if charJust['encoding'].lower() == 'gb2312' else charJust['encoding']
        except Exception, e:
            print 'chardet detect error:', Exception, '->', e

    res_charset = 'utf-8' if res_charset == '' else res_charset.lower()
    return res_charset

    def getLinks(self):
        """获取文件中的链接"""
        f = open(self.file)
        html = f.read()
        f.close()

        # 编码判断及转换
        self.charset = self.test_charset(html)
        html = strToUnicode(html, self.charset)

        # 统一把页面上的所有链接转换成绝对路径
        doc = lxml.html.fromstring(html)
        doc.make_links_absolute(base_url=self.baseUrl)

        linkList = []
        for link in lxml.html.iterlinks(doc):
            if link[2].startswith(self.baseUrl+'#'):
            # 过滤掉原来链接是这种形式的<a href="#s-latest"><span>Latest</span></a>
                continue
            linkList.append(link[2])

        # 把绝对路径替换成相对路径
        self.linkReplFunc(doc)

        return linkList

    def getCssLinks(self):
        """获取css文件中的链接(一般主要有图片和其他css文件)"""
        f = open(self.file)
        css = f.read()
        f.close()

        def getNewLink(cl):
            up = urlparse(self.url)
            if (not up.path) or ('../' not in cl):
                return cl

            cs = cl.count('../')+1
            newlink = up.scheme+'://'+up.netloc+'/'.join(up.path.split('/')[:-cs])
            newlink = re.sub(r'(\.\./)+', newlink+'/', cl)
            return newlink

        # 图片链接
        picLinks = re.findall(r'background:\s*url\s*\([\'\"]?([a-zA-Z0-9/\._-]+)[\'\"]?\)', css, re.I)
        # 其他css链接
        cssLinks = re.findall(r'@import\s*[\'\"]*([a-zA-Z0-9/\._-]+)[\'\"]*', css, re.I)
        Links = picLinks + cssLinks
        cLinks = []
        for cl in Links:
            cLinks.append(getNewLink(cl))

        return cLinks


#-*- coding: utf-8 -*-

import sys,os,datetime,urllib2,re,urllib
from urlparse import urlparse
import chardet
import sqlite3

def read_file(in_file):
    try:
        fo = open(in_file, 'r')
        str_css = fo.read()
    except Exception, ex:
        print Exception,':',ex
    finally:
        if fo: fo.close()
    return str_css

def write_file(in_file, str_css):
    try:
        fo = open(in_file, 'w')
        fo.write(str_css)
    except Exception, ex:
        print Exception,':',ex
    finally:
        if fo: fo.close()

def read_url(in_url):
    str_css = ''
    try:
        req = urllib2.Request(in_url)
        str_css = urllib2.urlopen(req).read()
    except Exception, ex:
        print Exception,':',ex
    finally:
        pass
    return str_css


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
            try:
                decoding = 'gbk' if charJust['encoding'].lower() == 'gb2312' else charJust['encoding']
            except Exception, e:
                print 'strToUnicode chardet detect error:', Exception, '->', e
        decoding = 'utf-8' if not decoding else decoding
        if decoding:
            html = html.decode(decoding, 'ignore')
    return html

def unicodeToStr(html, encoding='utf-8'):
    if not isinstance(html, unicode):
        decoding, charJust = '', chardet.detect(html)
        try:
            decoding = 'gbk' if charJust['encoding'].lower() == 'gb2312' else charJust['encoding']
        except Exception, e:
            print 'unicodeToStr chardet detect error:', Exception, '->', e
        if encoding and decoding and decoding!=encoding :
            html = html.decode(decoding, 'ignore').encode(encoding, 'ignore')
    else:
        if encoding: html = html.encode(encoding, 'ignore')
    return html


def try_get_css(in_url, in_path = None, in_file = None):
    if not in_url: return -1
    in_path = in_path if (in_path) else os.getcwd()
    if not os.path.exists(in_path): os.makedirs(in_path)

    print '\n\n\n',datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S  "),"CSS Download ing -> ",in_url

    str_css = read_file(in_file) if in_file else read_url(in_url)
    if len(str_css)<1: return -2
    print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S  "),"CSS Download :",str(len(str_css)),' byte'

    # use re parse css and findall url('images/xxx.gif')
    p = re.compile('background(.*?)url\((.*?)\)', re.IGNORECASE)
    g = p.findall(str_css)

    css_path = get_url_path(in_url, in_path)
    #write_file(os.path.join(in_path, css_path.filename+'.bak') , str_css)
    write_file(os.path.join(css_path.save_path) , str_css)

    print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S  "),"img Download :",
    count_download = 0L
    for item in g:
        item_url = item[1]
        item_url = item_url.replace('"','').replace("'",'')
        item_url = os.path.join(css_path.baseurl, item_url) if item_url[0] == '.' else item_url
        item_url = os.path.join('http://', css_path.hostname, item_url[1:]) if item_url[0] == '/' else item_url
        url_path = get_url_path(item_url.replace('\\','/'), in_path)

        if not url_path:
            print '\n\n','ERROR url_path  url -> ',item_url
            continue
        if ';base64,' in url_path.in_url:
            print '\n\n','base64 png  url -> ',item_url
            continue
        if os.path.isfile(url_path.save_path):
            print url_path.filename,'(pass)',
            continue

        data =  None
        try:
            if not os.path.exists(url_path.save_dir): os.makedirs(url_path.save_dir)
            data = urllib.urlretrieve(url_path.in_url, url_path.save_path) if not os.path.isfile(url_path.save_path) else None
        except Exception, ex:
            try:
                data = urllib.urlretrieve(url_path.in_url, url_path.save_path) if not os.path.isfile(url_path.save_path) else None
            except Exception, ex:
                try:
                    data = urllib.urlretrieve(url_path.in_url, url_path.save_path) if not os.path.isfile(url_path.save_path) else None
                except Exception, ex:
                    print '\n', 'urlretrieve error:', ex, '\n','in_url:', url_path.in_url
        data_len = int(data[1]['content-length']) if data else 0L
        count_download = count_download + 1 if data else count_download
        print url_path.filename,'(%s)' % data_len,
        #str_css = str_css.replace(item[1] ,'"./%s%s"' % (url_path.hostname,url_path.path))

    #write_file(os.path.join(in_path, css_path.hostname, css_path.filename) , str_css)
    return count_download

def try_get_css_url_list(in_url, in_path):
    if not in_url: return -1L
    in_path = in_path if (in_path) else os.getcwd()
    if not os.path.exists(in_path): os.makedirs(in_path)

    print '\n',datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S  "),"Link DB ing... "

    url_path = get_url_path(in_url, in_path)
    if not url_path: return -2L

    db_dir = os.path.join(in_path, url_path.hostname)
    if not os.path.exists(db_dir): os.makedirs(db_dir)
    db_path = os.path.join(db_dir, url_path.hostname+'.web_download.db')

    return _get_css_url_list_from_db(db_path)


def _get_css_url_list_from_db(db_path, table_name='wdb_vlink', col_name='filetype'):
    db_conn = sqlite3.connect(db_path)
    if not db_conn: return None
    db_cursor = db_conn.cursor()

    res_url_list = []

    sql_cmd = 'select url from %s where %s="css" ' % (table_name, col_name)

    try:
        db_cursor.execute(sql_cmd)
        result = db_cursor.fetchall()
    except Exception, ex:
        print '\n', '_get_css_url_list_from_db error:', ex, '\n','sql_cmd:', sql_cmd

    for css_item in result:
        res_url_list.append( unicodeToStr(css_item[0]) )

    return res_url_list

def main():
    main_start = datetime.datetime.now()
    main_count = 0L
    print sys.argv[0] + ' >>'

    main_url = sys.argv[1] if len(sys.argv)>1 else None
    main_path = sys.argv[1] if len(sys.argv)>2 else None
    main_file = sys.argv[1] if len(sys.argv)>3 else None

    main_url = r'http://www.battlenet.com.cn/'
    css_url_list = try_get_css_url_list(main_url, main_path)
    #css_url_list = ["http://www.battlenet.com.cn/wow/static/css/wow.css?v=37",]

    for item_url in css_url_list:
        css_url = item_url
        main_count +=  try_get_css(css_url, main_path, main_file)

    print '\n',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S  '),str(main_count),' items OVER!'
    main_end = datetime.datetime.now()
    print '\nUSE Time : ',str(main_end - main_start)

if __name__ == '__main__':
    main()




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
            res = in_obj.downLoad()
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



class RepLink(object):

    def __init__(self, url1, url2, baseurl):
        # 当前页面链接
        self.url1 = strToUnicode(url1,'utf-8')
        # 页面上的一个链接
        self.url2 = strToUnicode(url2,'utf-8')
        self.baseUrl = baseurl

    def getRepStr(self):
        urlList1 = [ i for i in self.url1.replace('http://', '').split('/') if i]
        urlList2 = [ i for i in self.url2.replace('http://', '').split('/') if i]
#        print urlList1
#        print urlList2

        n = 0
        while True:
            if urlList1[:n]==urlList2[:n]:
                n+=1
                if n>10:
                    break
                continue
            break

        urlPart = 'http://'+'/'.join(urlList1[:n-1])
        if urlparse(urlPart).netloc and ('.' not in urlparse(urlPart).path):
            urlPart += '/'

        urlListLen = len(urlList1[n-1:])

        if urlListLen<1:
            return (urlPart, './')

        if urlListLen>=1:
            return (urlPart, urlListLen*'../', self.url1, self.url2)

    def replUrl(self):
        """把绝对路径替换成相对路径"""
        aUrl = self.getRepStr()
#        print aUrl
        if self.url2.startswith(self.baseUrl+'#'):
            # 处理链接是这种形式的<a href="http://www.baidu.com#s-latest"><span>Latest</span></a>
            self.url2 = self.url2.replace(self.baseUrl+'#', '#')
        else:
            self.url2 = self.url2.replace(aUrl[0], aUrl[1])
#        print self.url2
        return self.url2

class Retrieve(object):

    def __init__(self, url, baseUrl, url_path):
        self.url = url
        self.baseUrl = baseUrl
        self.url_path = url_path
        self.charset = ''
        self.save_dir = unicodeToStr(self.url_path.save_dir, 'gbk')
        self.file = unicodeToStr(self.url_path.save_path, 'gbk')

        if not os.path.exists(self.save_dir):
            try:
                os.makedirs(self.save_dir)
            except Exception, e:
                print 'makedirs error:', e

    def downLoad(self):
        """下载文件"""
        results = 0L
        socket.setdefaulttimeout(30)
        try:
            real_url = unicodeToStr(self.url,'utf-8').replace(' ','%20')
#           result = urllib.urlretrieve(self.url, self.file)
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

    def linkReplFunc(self, doc, method='html'):
        """把绝对路径替换成相对路径"""
        def replLink(arg):
            rl = RepLink(self.url, arg, baseurl=self.baseUrl)
            return rl.replUrl()

        doc.rewrite_links(replLink)
        html = lxml.html.tostring(doc, encoding=self.charset, method=method)
        f = open(self.file, 'w')
        f.write(html)
        f.close()

    def test_charset(self, html):
        res_charset = ''

        if self.content and self.content[1].plist :
            for item in self.content[1].plist:
                item = str(item).strip()
                if item[:7].lower()=='charset': res_charset = item[item.rindex('=')+1:].strip().lower()
        elif res_charset == '':
            charJust = chardet.detect(html)
            try:
                res_charset = 'gbk' if charJust['encoding'].lower() == 'gb2312' else charJust['encoding']
            except Exception, e:
                print 'chardet detect error:', Exception, '->', e

        res_charset = 'utf-8' if res_charset == '' else res_charset.lower()
        return res_charset

    def getLinks(self):
        """获取文件中的链接"""
        f = open(self.file)
        html = f.read()
        f.close()

        # 编码判断及转换
        self.charset = self.test_charset(html)
        html = strToUnicode(html, self.charset)

        # 统一把页面上的所有链接转换成绝对路径
        doc = lxml.html.fromstring(html)
        doc.make_links_absolute(base_url=self.baseUrl)

        linkList = []
        for link in lxml.html.iterlinks(doc):
            if link[2].startswith(self.baseUrl+'#'):
            # 过滤掉原来链接是这种形式的<a href="#s-latest"><span>Latest</span></a>
                continue
            linkList.append(link[2])

        # 把绝对路径替换成相对路径
        self.linkReplFunc(doc)

        return linkList

    def getCssLinks(self):
        """获取css文件中的链接(一般主要有图片和其他css文件)"""
        f = open(self.file)
        css = f.read()
        f.close()

        def getNewLink(cl):
            up = urlparse(self.url)
            if (not up.path) or ('../' not in cl):
                return cl

            cs = cl.count('../')+1
            newlink = up.scheme+'://'+up.netloc+'/'.join(up.path.split('/')[:-cs])
            newlink = re.sub(r'(\.\./)+', newlink+'/', cl)
            return newlink

        # 图片链接
        picLinks = re.findall(r'background:\s*url\s*\([\'\"]?([a-zA-Z0-9/\._-]+)[\'\"]?\)', css, re.I)
        # 其他css链接
        cssLinks = re.findall(r'@import\s*[\'\"]*([a-zA-Z0-9/\._-]+)[\'\"]*', css, re.I)
        Links = picLinks + cssLinks
        cLinks = []
        for cl in Links:
            cLinks.append(getNewLink(cl))

        return cLinks

class Crawl(object):
    def _run_cmd_list(self, str_cmd=None, str_list=None):
        str_cmd = str_cmd if str_cmd else ''
        str_list = str_list if str_list else []
        str_res = ''
        try:
            str_res = str_cmd % tuple(str_list)
        except:
            try:
                decode_list = self._run_decode_list(str_list)
                str_res = str_cmd % tuple(decode_list)
            except Exception, ex:
                print '\n', 'make str_cmd error:', ex, '\n','str_cmd:', str_cmd, '\n','decode_list:', str(decode_list)
        return str_res

    def _run_decode_list(self, str_list=None):
        str_list = str_list if str_list else []
        str_list_res = []
        for str_item in str_list:
            try:
                decode_item = str_item if isinstance(str_item, unicode) else strToUnicode(str(str_item), 'utf-8')
                str_list_res.append( decode_item )
            except Exception, ex:
                print '\n', '_run_decode_list decode error:', ex, '\n','str_item:', str_item
        return str_list_res

    def _run_execute_list(self, sql_list=None, sql_commit=True):
        if sql_list:
            for sql_cmd in sql_list: self._run_execute(sql_cmd, False)
        if sql_commit: self.conn.commit()

    def _run_execute(self, sql_cmd=None, sql_commit=True):
        try:
            if sql_cmd: self.cursor.execute(sql_cmd)
        except Exception, ex:
            print '\n', 'execute sql error:', ex, '\n','sql_cmd:', sql_cmd
        if sql_commit: self.conn.commit()

    def _run_fetchall(self, sql_cmd=None):
        result = []
        if sql_cmd:
            self._run_execute(sql_cmd, False)
            result = self.cursor.fetchall()
        return result

    def _run_fetchone(self, sql_cmd=None):
        result = []
        if sql_cmd:
            self._run_execute(sql_cmd, False)
            result = self.cursor.fetchone()
        return result

    def __init__(self, in_url, in_domain, in_hp, in_path=None):
        in_path = in_path if (in_path) else os.getcwd()
        if not os.path.exists(in_path): os.makedirs(in_path)

        self.url = in_url
        self.domain = in_domain
        self.hp = in_hp
        self.in_path = in_path

        self.seen = {}
        self.vlink = {}
        self.baseUrl = 'http://'+self.domain
        self.filetype_order = {'js':10,'jpg':19,'gif':18,'png':17,'bmp':16,'css':25,'html':4}

        self.init_db(self.url, self.in_path)
        self.do_set_vlink(self.url)

    def getPage(self, task_info):
        task_id = task_info[0]
        res = task_info[1]
        rv = task_info[2]

        result = self.doPage(rv, res)

        do_flag = result if result <= 0 else 1L
        do_flag = do_flag if do_flag != -900 else 0L

        self.do_finish_vlink(rv.url, do_flag)
        if do_flag != 0 : self.do_finish_seen(rv.url, result)

        del rv
        return result

    def doPage(self, rv, res):
        if res <= 0: return res

        link_count = 1L
        if rv.url_path.filetype in ['js', 'jpg', 'png', 'gif']:
            return link_count
        try:
            if rv.url_path.filetype == 'css': links = rv.getCssLinks()
            else: links = rv.getLinks()
        except Exception,e:
            print '\n','ERROR -> getLinks error:', e, '\n','url:', rv.url
            return link_count

        self.do_set_linkmap(rv.url, links)

        for link in links:
            link = link.split('?')[0].split('#')[0]
            if (link not in self.seen) and (link not in self.vlink) and self.test_vlink(rv.url, link):
                link_count += self.do_set_vlink(link, rv.url)

        return link_count

    def init_db(self, in_url, in_path):
        url_path = get_url_path(in_url, in_path)
        db_dir = os.path.join(in_path, url_path.hostname)
        if not os.path.exists(db_dir): os.makedirs(db_dir)
        db_path = os.path.join(db_dir, url_path.hostname+'.web_download.db')
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        wdb_vlink_sql = "CREATE TABLE IF NOT EXISTS wdb_vlink (vlink_id integer PRIMARY KEY AUTOINCREMENT, \
                        create_time timestamp NOT NULL, update_time timestamp NOT NULL DEFAULT (datetime('now','localtime')), \
                        url varchar(512) default '', hostname varchar(128) default '', path varchar(256) default '', \
                        filename varchar(128) default '', filetype varchar(16) default '', \
                        do_flag integer default 0, do_order integer default 0, from_url varchar(512) default '')"
        wdb_seen_sql = "CREATE TABLE IF NOT EXISTS wdb_seen (seen_id integer PRIMARY KEY AUTOINCREMENT, \
                        create_time timestamp NOT NULL, update_time timestamp NOT NULL DEFAULT (datetime('now','localtime')), \
                        url varchar(512) default '', link_count integer default 0)"
        wdb_linkmap_sql = "CREATE TABLE IF NOT EXISTS wdb_linkmap (linkmap_id integer PRIMARY KEY AUTOINCREMENT, \
                        create_time timestamp NOT NULL, update_time timestamp NOT NULL DEFAULT (datetime('now','localtime')), \
                        url varchar(512) default '', link varchar(512) default '')"

        sql_list = [wdb_vlink_sql, wdb_seen_sql, wdb_linkmap_sql]
        self._run_execute_list(sql_list)
        self.init_vlink()
        self.init_seen()

    def init_vlink(self):
        self.init_vlink_do_flag()
        init_vlink_sql = "select url, hostname, path, filename, filetype, from_url, do_order from wdb_vlink where do_flag=0 "
        #init_vlink_tuple = (url, url_path.hostname, url_path.fix_path, url_path.filename, url_path.filetype, from_url, do_order)
        for item in self._run_fetchall(init_vlink_sql):
            self.vlink.setdefault(item[0], item)

    def init_vlink_do_flag(self, do_flag_from=None, do_flag_to=None,):
        do_flag_from = do_flag_from if do_flag_from else -1L
        do_flag_to = do_flag_to if do_flag_to else 0L

        init_vlink_do_flag_sql = "update wdb_vlink set do_flag=%s where do_flag=%s "
        init_vlink_do_flag_tuple = (do_flag_to, do_flag_from)

        sql_cmd = init_vlink_do_flag_sql % init_vlink_do_flag_tuple
        self._run_execute(sql_cmd)

    def init_seen(self):
        init_seen_sql = "select url, link_count from wdb_seen where link_count>0 "
        #init_seen_tuple = (url, count)
        for item in self._run_fetchall(init_seen_sql):
            self.seen.setdefault(item[0], item[1])

    def test_vlink(self, url, link):
        return True

    def do_get_vlink(self):
        do_get_vlink_sql = "select url from wdb_vlink where do_flag=0 order by do_order desc limit 1"
        url_row = self._run_fetchone(do_get_vlink_sql)
        url = url_row[0]

        self.vlink.setdefault(url, None)
        do_get_vlink_tuple = self.vlink[url]

        del self.vlink[url]
        return (url, do_get_vlink_tuple)

    def do_set_vlink(self, url, from_url=None):
        if (url in self.seen) or (url in self.vlink): return 0L

        from_url = from_url if from_url else url
        url_path = get_url_path(url, self.in_path)
        if not url_path: return 0L
        if self._str_pass_path(url_path) or self._str_pass_url(url_path): return 0L

        do_order = self.filetype_order.get(url_path.filetype, 0)
        do_set_seen_sql = "insert into wdb_vlink (create_time, url, hostname, path, filename, filetype, from_url, do_order) \
                            values ((datetime('now','localtime')),'%s','%s','%s','%s','%s','%s',%s)"
        do_set_seen_tuple = (url, url_path.hostname, url_path.fix_path, url_path.filename, url_path.filetype, from_url, do_order)

        #sql_cmd = do_set_seen_sql % do_set_seen_tuple
        sql_cmd = self._run_cmd_list(do_set_seen_sql, do_set_seen_tuple)

        self._run_execute(sql_cmd)
        self.vlink[url] = do_set_seen_tuple
        return 1L

    def do_finish_vlink(self, url, do_flag=None):
        do_flag = do_flag if do_flag else 0L
        do_finish_vlink_sql = "update wdb_vlink set do_flag=%s where url = '%s' "
        do_finish_vlink_tuple = (do_flag, url)
        if do_flag==0 : self.do_remove_seen(url)

        sql_cmd = do_finish_vlink_sql % do_finish_vlink_tuple
        self._run_execute(sql_cmd)

    def do_set_linkmap(self, url, link_list):
        sql_list = []
        for link in link_list:
            do_set_linkmap_sql = "insert into wdb_linkmap (create_time, url, link) values ((datetime('now','localtime')),'%s','%s')"
            do_set_linkmap_tuple = (url, link)
            #sql_cmd = do_set_linkmap_sql % do_set_linkmap_tuple
            sql_cmd = self._run_cmd_list(do_set_linkmap_sql, do_set_linkmap_tuple)
            sql_list.append(sql_cmd)
        self._run_execute_list(sql_list)

    def do_remove_seen(self, url):
        do_remove_seen_sql = "delete from wdb_seen where url='%s' "
        dodo_remove_seen_tuple = (url)
        sql_cmd = do_remove_seen_sql % dodo_remove_seen_tuple
        self._run_execute(sql_cmd)

        self.seen.setdefault(url, 0)
        del self.seen[url]

    def do_set_seen(self, url, link_count=None):
        if link_count: self.seen[url] = link_count
        else: self.seen.setdefault(url, 0)

    def do_finish_seen(self, url, link_count=None):
        if link_count: self.seen[url] = link_count
        else: self.seen.setdefault(url, 0)
        link_count = link_count if link_count else 0L
        #do_finish_seen_sql = "update wdb_seen set link_count=%s where url = '%s' "
        do_finish_seen_sql = "insert into wdb_seen (create_time, url, link_count) values ((datetime('now','localtime')),'%s',%s)"
        do_finish_seen_tuple = (url, link_count)
        sql_cmd = do_finish_seen_sql % do_finish_seen_tuple
        self._run_execute(sql_cmd)

    def _str_pass_path(self, url_path):
        result = False
        path = url_path.path
        pass_path_list = ('/wow/zh/character/','/wow/zh/guild/','/wow/zh/forum/',\
                            '/sc2/zh/profile/','/sc2/zh/forum/',\
                            '/wow/renders/npcs/rotate/creature',\
                            '/wow/renders/npcs/portrait/creature',\
                            '/../')
        for pass_path in pass_path_list:
            pass_path = pass_path
            if path[:len(pass_path)].lower() == pass_path:
                result = True
                break
        return result

    def _str_pass_url(self, url_path):
        result = False
        url = url_path.in_url
        if not result and '.' not in url_path.hostname :result = True
        if not result and self.domain not in url and url_path.filetype not in ['css', 'js', 'jpg', 'png', 'gif']:result = True
        return result

    def _str_print_url(self, in_url):
        url = in_url
        url = unicodeToStr(url, 'utf-8')
        url = url_decode_str(url)
        url = strToUnicode(url,"utf8")
        return url

    def go(self):
        download_count = 0L
        while len(self.vlink) > 0 or self.hp.get_doing_count_now() > 0:
            vlink_tuple = self.do_get_vlink() if self.vlink else None
            if vlink_tuple:
                download_count += self.addPage(vlink_tuple[0])
            if len(self.vlink) == 0 and self.hp.get_doing_count_now() > 0:
                download_count += self.waitPage()
        return download_count


    def initPage(self, vlink_url):
        rv = None
        if vlink_url not in self.seen:
            url_path = get_url_path(vlink_url, self.in_path)
            if not url_path : return None
            if self._str_pass_path(url_path)  or self._str_pass_url(url_path):
                self.do_finish_vlink(vlink_url, -2)
            else:
                self.do_set_seen(vlink_url, 0)
                rv = Retrieve(vlink_url, self.baseUrl, url_path)
                if not rv : return None
                if (os.path.isfile(rv.file) and rv.url_path.filetype in ['css', 'js', 'jpg', 'png', 'gif']) \
                    or self._try_download_with_thunder(url_path):
                    self.do_finish_vlink(vlink_url, 1)
                    self.do_finish_seen(vlink_url, 1)
                    rv = None
                else:
                    self.do_finish_vlink(vlink_url, -1)

        return rv

    def addPage(self, vlink_url):
        add_count = 0L
        rv = self.initPage(vlink_url) if vlink_url else None

        task_id = len(self.seen)
        if rv:
            print '\n',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S ->'),task_id,' download link -> ', self._str_print_url(vlink_url)
        else:
            log_with_info("%s(pass)" % (task_id))

        while rv:
            if rv and self.hp.get_doing_count_now() < self.hp.get_doing_count_max():
                if self.hp.add_task(task_id, rv):
                    log_with_info("%s(add)" % (task_id))
                    rv = None
            results = self.hp.get_results()
            if not results:
                time.sleep(1.0 * random.random())
            else:
                for info in results:
                    tr_count = self.getPage(info)
                    if tr_count >= 0 :log_with_info('%s(+%s)' % (info[0], tr_count) )
                    else:log_with_info('%s(err:%s)' % (info[0], tr_count) )
                add_count = add_count + len(results)

        return add_count

    def waitPage(self):
        add_count = 0L

        count_waite = 0L
        while len(self.vlink) == 0 and self.hp.get_doing_count_now() > 0:
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
                add_count = add_count + len(results)

        return add_count

    def _try_download_with_thunder(self, url_path):
        return False

##        list_down_all = [{'file_url':file_url, 'file_name':file_name, \
##                        'ps_text':ps_text, 'from_url':from_url}]
##        #[file_url, file_name, ps_text, from_url]
##        ThunderAgent = win32com.client.Dispatch("ThunderAgent.Agent.1")
##        for down_info in list_down_all:
##            ThunderAgent.AddTask12(down_info['file_url'], down_info['file_name'], "", down_info['ps_text'], down_info['from_url'], "", -1, 0, -1,  "", "", "", 0, "rightup")
##        ThunderAgent.CommitTasks2(1)

def main():
    main_count = 0L
    main_start = datetime.datetime.now()

    url_str = "http://www.battlenet.com.cn/wow/zh/zone/#expansion=4"
    url_host = "www.battlenet.com.cn"

    hp = HttpPool(threads_count=50, doing_count=10, fail_op=base_fail_op, log=base_log)
    #enable_global_proxy(proxy_http="http", proxy_url="http://127.0.0.1:8087",enable_proxy = True)

    cr = Crawl(url_str, url_host, hp)
    main_count = cr.go()


    print '\n',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S  '),str(main_count),' items OVER!'
    main_end = datetime.datetime.now()
    print '\n','USE Time : ',str(main_end - main_start)


if __name__ == '__main__':
    main()