#-*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()

from gevent.pool import Pool

import datetime
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
import cPickle

MAX_GEVENT_NUMS = 50

def main():
    page_nums = 10
    url_base = 'http://www.youdaili.net/Daili/http/list_%d.html'
    url_base = 'http://www.youdaili.net/Daili/guonei/list_%d.html'
    url_list = get_url_list(url_base, page_nums)
    _LOG('all url page total:%d, item:%d' % (page_nums, len(url_list)))

    ip_list = get_ip_list(url_list)
    _LOG('all ip list:%s' % (len(ip_list),))

    obj_file = 'ip.cpy'
    save_obj(obj_file, ip_list)
    _LOG('all ip obj:%s list:%s' % (obj_file, len(ip_list),))
    text_file = 'get_ip.txt'
    save_ip_list(ip_list, text_file)
    _LOG('all ip te;%s list:%s' % (text_file, len(ip_list),))

def read_obj(obj_file):
    with open(obj_file, 'r') as ff:
        return cPickle.load(ff)

def save_obj(obj_file, obj):
    with open(obj_file, 'w') as ff:
        cPickle.dump(obj, ff, 0)

def save_ip_list(ip_list, file_name):
    ip_list = [item.encode('utf-8')+'\n' for item in ip_list]
    with open(file_name, 'w') as wf:
        wf.writelines(ip_list)

def get_url_list(url_base, page_nums):
    url_list = []
    url_base_list = [url_base % (idx, ) for idx in range(1, page_nums+1)]
    gpool = Pool(MAX_GEVENT_NUMS)
    for url, tmp in gpool.imap_unordered(get_url_list_by_base, url_base_list):
        url_list.extend( tmp )
        _LOG('add page url:%s, item:%d' % (url, len(tmp)))
    return url_list

def get_url_list_by_base(url):
    dom = pq(url=url)
    ul = dom('.newslist_line').find('a')
    tmp = [item.attrib['href'] for item in ul if item.attrib.get('href', '')]
    return url, tmp

def get_ip_list(url_list):


    ip_list = []

    gpool = Pool(MAX_GEVENT_NUMS)
    for url, tmp in gpool.imap_unordered(get_ip_list_by_url, url_list):
        _LOG('get ip url:%s list:%s' % (url, len(tmp),))
        ip_list.extend(tmp)

    return ip_list

def get_ip_list_by_url(url_item):
    def _fix_url(base_url, url):
        return base_url[:base_url.rfind('/')+1] + url

    dom = pq(url=url_item)
    page_list = [item.attrib['href'] for item in dom('.pagelist').find('a') if item.attrib.get('href', '')]
    if page_list:
        page_list = page_list[1:-1]
        page_list = [_fix_url(url_item, item) for item in page_list]
        tmp = get_ip_by_page_list(page_list, dom.html())
    else:
        tmp = get_ip_by_html(0, dom.html())

    return url_item, tmp

def get_ip_by_page_list(page_list, first_html):
    all_list  = []
    for idx, url in enumerate(page_list):
        html = first_html if idx==0 else pq(url=url).html()
        tmp = get_ip_by_html(idx, html)
        all_list.extend(tmp)

    return all_list

def get_ip_by_html(idx, html):
    bs = BeautifulSoup(html, 'lxml')
    ip_str = bs.find('div', class_='cont_font').find('p').text.split('\n')
    tmp = [item.strip() for item in ip_str if item.strip()]
    _LOG('get ip page:%s list:%s' % (idx+1, len(tmp),))
    return tmp

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
    main_start = datetime.datetime.now()
    main()
    main_end = datetime.datetime.now()
    print '\n','USE Time : ',str(main_end - main_start)
    _LOG('\n============End=============\n')
