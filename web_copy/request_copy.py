# -*- coding: utf-8 -*-
import os
import requests
import chardet
import lxml
import time
import datetime
import re
from bs4 import BeautifulSoup

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

_split_url = lambda href: href.split('?')[0].split('@')[0].split(',')[0].split(';')[0].split('#')[0]

def get_page(page_html):
    page_html = BeautifulSoup(page_html, 'html.parser', from_encoding=None).prettify()
    soup = BeautifulSoup(page_html, 'html.parser', from_encoding=None)
    _get_links = lambda s:[_split_url(i.attrs['href']) for i in s.findAll('a') if getattr(i, 'attrs', None)  and getattr(i.attrs, 'href', None)]
    link_list = _get_links(soup)

    _get_css = lambda s:[_split_url(i.attrs['href']) for i in s.findAll('link') if getattr(i, 'attrs', None)  and getattr(i.attrs, 'href', None)]
    css_list = _get_css(soup)
    link_list

def load_str(file_name):
    with open(file_name, 'r') as rf:
        return rf.read()

def dump_str(file_str, file_name):
    with open(file_name, 'w') as wf:
        wf.write(file_str)

def main():
    url = 'http://zyy.loewenw.com/'
    tmp_file = os.path.join(os.getcwd(), 'tmp_html.tmp')
    if os.path.isfile(tmp_file):
        page_html = load_str(tmp_file)
    else:
        res = requests.get(url)
        page_html = res.content if res.ok else ''
        dump_str(page_html, tmp_file)
    get_page(page_html)
    _LOG('end')

if __name__ == '__main__':
    main()