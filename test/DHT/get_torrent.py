#-*- coding: utf-8 -*-
import datetime
# -*- coding: utf-8 -*-

import os
from httptool import MultiHttpDownLoad, _LOG
from bs4 import BeautifulSoup
from dht_api import getTorrentTask, doneTorrentTask

def main():
    main_start = datetime.datetime.now()
    with open( os.path.join(os.getcwd(), 'httptool', 'ip.txt'), 'r') as rf:
        proxy_list = [item.strip() for item in rf.readlines() if item.strip()]

    pnum = 1
    ret = True
    while ret:
        ret = run_get_torrent(pnum, proxy_list)

    main_end = datetime.datetime.now()
    print '\n','USE Time : ',str(main_end - main_start)

def run_get_torrent(pnum, proxy_list):
    url_base = 'http://www.btwalk.org/wiki/%s.html'
    task = getTorrentTask()
    if not task:
        return False;
    _LOG('get task:%d' % (len(task), ))
    url_list = [url_base % (item['hashkey'], ) for item in task if item.get('hashkey', '')]

    def _save_torrent(url, data, headers):
        if not data:
            return
        dom = pq(data)
        ul = dom('.newslist_line').find('a')
        tmp = [item.attrib['href'] for item in ul if item.attrib.get('href', '')]
        _LOG('add page url:%s, item:%d' % (url, len(tmp)))

    gpool = MultiHttpDownLoad(pnum, proxy_list=proxy_list)
    gpool.get_http_list(url_list, _save_torrent, lambda s,h:isinstance(s, str) and len(s)>1000)

    return False


if __name__ == '__main__':
    main()
    _LOG('\n============End=============\n')
