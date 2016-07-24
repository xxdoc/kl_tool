#-*- coding: utf-8 -*-
import datetime
from httptool import MultiHttpDownLoad, _LOG
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq


def main():
    main_start = datetime.datetime.now()

    tag_list = ['QQ', 'http', 'guonei', 'guowai', 'area']
    page_nums = 10
    for tag in tag_list:
        run_get_proxy(tag, page_nums)

    main_end = datetime.datetime.now()
    print '\n','USE Time : ',str(main_end - main_start)

def run_get_proxy(tag, page_nums):
    url_base = 'http://www.youdaili.net/Daili/' + tag + '/list_%d.html'
    url_list = get_url_list(url_base, page_nums)
    _LOG('all url page total:%d, item:%d' % (page_nums, len(url_list)))

    ip_list = get_ip_list(url_list)
    _LOG('all ip list:%s' % (len(ip_list),))

    def save_ip_list(ip_list, file_name):
        ip_list = [item.encode('gbk', 'ignore')+'\n' for item in ip_list]
        with open(file_name, 'w') as wf:
            wf.writelines(ip_list)

    text_file = tag + '_ip.txt'
    save_ip_list(ip_list, text_file)
    _LOG('all ip tag:%s list:%s' % (text_file, len(ip_list),))


def get_url_list(url_base, page_nums):
    url_list = []
    url_base_list = [url_base % (idx, ) for idx in range(1, page_nums+1)]

    def _save_url(url, data, headers):
        if not data:
            return
        dom = pq(data)
        ul = dom('.newslist_line').find('a')
        tmp = [item.attrib['href'] for item in ul if item.attrib.get('href', '')]
        url_list.extend( tmp )
        _LOG('add page url:%s, item:%d' % (url, len(tmp)))

    gpool = MultiHttpDownLoad(10)
    gpool.get_http_list(url_base_list, _save_url, lambda s,h:isinstance(s, str) and len(s)>1000)

    return url_list


def get_ip_list(url_list):
    ip_list = []
    url_data = {item:'' for item in url_list}

    def _save_page(url, data, headers):
        def _fix_url(base_url, url):
            return base_url[:base_url.rfind('/')+1] + url

        if not data:
            return
        dom = pq(data)
        page_list = [item.attrib['href'] for item in dom('.pagelist').find('a') if item.attrib.get('href', '')]
        if page_list:
            page_list = page_list[1:-1]
            page_list = [_fix_url(url, item) for item in page_list]
            for item in page_list:
                url_data.setdefault(item, '')
        _LOG('get page url:%s, data:%d' % (url, len(data)))
        url_data[url] = data


    gpool = MultiHttpDownLoad(100)
    for _ in range(100):
        gpool.get_http_list([k for k,v in url_data.items() if not v], _save_page, lambda s,h:isinstance(s, str) and len(s)>1000)

    def get_ip_by_html(html):
        if not html:
            return []
        bs = BeautifulSoup(html, 'lxml')
        div = bs.find('div', class_='cont_font')
        ip_str = div.find('p').text.split('\n') if div else ''
        tmp = [item.strip() for item in ip_str if item.strip()]
        return tmp

    for url, data in url_data.items():
        tmp = get_ip_by_html(data)
        _LOG('get ip url:%s list:%s' % (url, len(tmp),))
        ip_list.extend(tmp)

    return ip_list

if __name__ == '__main__':
    main()
    _LOG('\n============End=============\n')
