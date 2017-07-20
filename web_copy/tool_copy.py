# -*- coding: utf-8 -*-
import os
import requests
from urlparse import urlparse

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


class Retrieve(object):

    def __init__(self, url, baseUrl, save_dir, file_name):
        self.url = url
        self.baseUrl = baseUrl
        self.url_path = url_path
        self.charset = ''
        self.save_dir = unicodeToStr(self.url_path.save_dir, 'gbk')
        self.file_name = unicodeToStr(self.url_path.save_path, 'gbk')

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