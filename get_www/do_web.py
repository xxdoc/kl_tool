#-*- coding: utf-8 -*-
"""get all web
kl,2015-9-13 14:57:49
"""
import os
import datetime
import codecs
import base64
import StringIO
import cPickle
import zlib
import gzip
import urllib2
import socket
import httplib
## HttpPool
import time
import random
import threading
from Queue import Queue, Empty, Full

## Retrieve getLinks
from bs4 import BeautifulSoup
import urlparse
## Crawl mongoDB
import pymongo

HTTP_TIME_OUT = 30

class Error(Exception):
    pass


ALL_ERROR = Exception


def E(e):
    try:
        return '%r' % (e)
    except ALL_ERROR as ex:
        return '%s(%r)' % ('cannot get ex.msg!', ex)

ZIP_LEVEL = 7
BZC = lambda o, l: base64.b64encode(zlib.compress(cPickle.dumps(o), l), ('-', '_'))
CZB = lambda s: cPickle.loads(zlib.decompress(base64.b64decode(s, ('-', '_'))))



def get_links(html, charset, msg=''):
    """get html links"""
    def do_head(head):
        ret = {'__list__':[]}
        for i in head:
            ii = {k.lower().strip():i[k] for k in i}
            ret['__list__'].append(ii)
            for k in ii:
                if k=='charset':
                    ret[k] = ii[k]
                elif k=='name' and 'content' in ii:
                    ret[ii[k]] = ii['content']
        return ret

    def func_do_link_list(links):
        _do_netloc = lambda l: '.'.join(l[-4:]) if l[-4:][0]=='www' else '.'.join(l[-3:]) if len(l)>3 else '.'.join(l)
        _fmt_url = lambda ut:'%s://%s/' % (ut.scheme, _do_netloc(ut.netloc.split('.')))
        _replace_space = lambda s:s.replace('\\', '/').replace('\t', '').replace(' ', '').replace('\r', '').replace('\n', '').strip().lower()
        _do_url = lambda url:_fmt_url(urlparse.urlparse(_replace_space(url))).replace('://www.', '://').replace('https://', 'http://')
        _is_url = lambda url:'.' in url and '://' in url
        _is_http = lambda url:url.startswith('http://') or url.startswith('https://')
        tmp = set([_do_url(url) for url in  links if _is_url(url) and _is_http(url)])

        _is_domain_url = lambda l,r=True:(len(l)==3 and l[-3].endswith('://www')) or len(l)==2 or (r and len(l)>=3 and len(l[-2])<=3 and not l[-2].isdigit() and _is_domain_url(l[:-1],False))
        _is_ip_url = lambda l:l[-1].split('/')[0].split(':')[0].isdigit()
        _bad_url = lambda url_l:_is_ip_url(url_l) or not _is_domain_url(url_l)
        bad_url = lambda url:'.' not in url or _bad_url(url.split('.'))
        ret_list = [url for url in tmp if not bad_url(url)]
        return set(ret_list)

    ## get_links(html, url_in, base_url, msg='')
    _get_meta = lambda s:[i.attrs for i in s.head.findAll('meta')] if hasattr(s, 'head') and s.head else []
    _get_head = lambda s:s.title.text if hasattr(s, 'title') and hasattr(s.title, 'text') else ''
    _get_link = lambda s:[i.attrs['href'] for i in s.findAll('a') if i and 'href' in i.attrs]
    soup, retset, title, head = None, set(), '', {}
    try:
        from_encoding = charset if charset else None
        soup = BeautifulSoup(html, 'html.parser',from_encoding=from_encoding)
        title = _get_head(soup)
        head = do_head(_get_meta(soup))
        retset = func_do_link_list(_get_link(soup))
    except ALL_ERROR as ex:
        msg += '\nBeautifulSoup getLinks error:%s\n' % (E(ex))

    soup_str = ''
    try:
        if soup:
            soup_str = BZC(soup, ZIP_LEVEL)
    except RuntimeError as ex:
        msg += '\nRuntimeError in BeautifulSoup:%s\n' % (E(ex))
    return soup_str, (getattr(soup, '_dc', ''), retset, title, head), msg


def do_ret(html, charset, msg=''):
    ret = {'soup':'','linkset': set(),'charset': '','title': '','head': {},}
    try:
        ret['soup'], (ret['charset'], ret['linkset'], ret['title'], ret['head']), msg = get_links(html, charset, msg)
        return ret, msg
    except ALL_ERROR as ex:
        raise ex



#===================Retrieve==================
#=============================================
class Retrieve(object):
    """__init__(self, cr, url, baseUrl=None)
    run task:_run()->_downLoad(self.url)->getLinks(self.html, url_in)
    done task:_done(tid, ret_num, msg)->self.cr.update_setfail(self.url, setfail)
                                        self.cr.todo.update(links)
                                        self.cr.insert_links(links, self.url, self.cr.flag_todo)
                                        self.cr.update_setdict(self.url, setdict)"""

    def __init__(self, cr_in, url_in, deep, get_only=True):
        self.ret = {
            'linkset': set(),
            'content': {},
            'html': '',
            'charset': '',
            'title': '',
            'ip': '',
            'port': 0,
            'head': {},
            'links': []
        }
        self.url = url_in
        self.cr = cr_in
        self.deep = deep
        self.get_only = get_only
        self.pass_done = False

    def _download(self, url_in):
        """download file"""

        def test_charset(content, msg='', default='', use_chardet_detect=False):
            """test_charset(content, msg='', default='', use_chardet_detect=False):"""
            def get_charset(cstr, charset='', fstr='charset=', spl=('"', "'", ';', ',',), max_len=64):
                if fstr in cstr:
                    si = cstr.find(fstr) + len(fstr)
                    charset = cstr[si:si + max_len].split()[0]
                    for sp in spl:
                        charset = charset.split(
                            sp)[0] if sp in charset else charset
                return charset

            ##test_charset(html, content, msg='', default='', use_chardet_detect=False)
            content_text = content.getheader('content-type', '') if hasattr(
                content, 'getheader') else ''
            charset = get_charset(content_text.lower()).strip()
            try:
                charset = codecs.lookup(charset).name if charset else default
            except ALL_ERROR as ex:
                msg += '\nget_charset or chardet.detect error:%s,%s,%s\n' % (
                    E(ex), content_text, charset)
                charset = default
            return charset, msg

        def _save_get_only(url, cr, ret, set_do_flag, msg):
            getonly = {
                'charset': ret['charset'],
                'content': ret['content'],
                'ip': ret['ip'],
                'port': ret['port'],
                'do_flag': set_do_flag,
                'msg': msg
            }
            cr.update_setdict(url, getonly)
            cr.save_html(url, ret['html'])

        ##_download(self, url_in)
        ex_code = lambda n: -n if n is not None and n > 0 else -99
        run_count, msg, html = 1, '', ''
        try:
            # get html
            html, self.ret['content'], _sa = getUrl(url_in, use_gzip=True)
            self.ret['ip'], self.ret['port'] = _sa if isinstance(_sa, tuple) and len(_sa) == 2 else ('', 0)
            # get charset
            self.ret['charset'], msg = test_charset(self.ret['content'], msg)
            self.ret['html'] = BZC(html,ZIP_LEVEL)
            # save html
            _save_get_only(url_in, self.cr, self.ret, self.cr.flag_getonly, msg)

            if not self.get_only:
                tmp, msg = do_ret(html, self.ret['charset'], msg)
                run_count = self.cr.save_ret(url_in, self.deep, tmp, msg, is_log=False)
            self.pass_done = True
            return run_count, msg
        except urllib2.HTTPError as ex:
            msg += '\nurllib2.HTTPError:%s->%s\n' % (E(ex), url_in)
            return ex_code(ex.code), msg
        except urllib2.URLError as ex:
            msg += '\nurllib2.URLError:%s->%s\n' % (E(ex), url_in)
            return ex_code(ex.reason.errno), msg
        except socket.error as ex:
            msg += '\nsocket.error:%s->%s\n' % (E(ex), url_in)
            return ex_code(ex.errno), msg
        except httplib.BadStatusLine as ex:
            msg += '\nhttplib.BadStatusLine:%s->%s\n' % (E(ex), url_in)
            return ex_code(None), msg
        except IOError as ex:
            msg += '\nIOError:%s->%s\n' % (E(ex), url_in)
            return ex_code(None), msg
        except ALL_ERROR as ex:
            raise ex

    def _ready(self):
        return getattr(self, 'msg', '')

    def _run(self):
        return self._download(self.url)

    def _done(self, tid, ret_num, msg):
        if self.pass_done:
            return None
        elif ret_num < 0:
            setfail = {'do_flag': ret_num, 'msg': msg}
            self.cr.update_setdict(self.url, setfail)


#==============BaseObjectWithLog==============
#=============================================
#==============BaseObjectWithLog==============
#=============================================
class BaseObjectWithLog(object):

    def __init__(self, log_func_in=None, log_file_in=None):
        self.log_func = log_func_in
        self.log_file = log_file_in
        if log_file_in:
            self.log_handler = open(log_file_in, 'a') if isinstance(log_file_in, (str, unicode)) else log_file_in
        else:
            self.log_handler = None

    def log(self, msg, is_log=True):
        if self.log_func and is_log:
            try:
                self.log_func(msg, self.log_handler)
            except ALL_ERROR:
                pass

    def __enter__(self):
        cls = self.__class__.__name__
        msg = '\n%s.__enter__\n' % (cls)
        self.log(msg)
        return self

    def __exit__(self, e_type, e_value, e_tb):
        cls = self.__class__.__name__
        msg = '\n%s.__exit__:%s,%s,%s\n' % (cls, e_type, e_value, e_tb)
        self.log(msg)
        self.close()

    def close(self):
        pass

#==============http tool================
#=======================================
def httpProxy(proxy_url, proxy_http="http", enable_proxy=True):
    """httpProxy( proxy_url, proxy_http="http",enable_proxy = True)"""
    if enable_proxy:
        opener = urllib2.build_opener(urllib2.ProxyHandler(
            {proxy_http: proxy_url}))
    else:
        opener = urllib2.build_opener(urllib2.ProxyHandler({}))
    urllib2.install_opener(opener)


USER_AGENT = (
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36'
)
ACCEPT_ENCODING = 'gzip,deflate'
GZIP = 'gzip'


def getUrl(url, use_gzip=True, timeout=HTTP_TIME_OUT):
    """getUrl(url, use_gzip=True)
    raise urllib2.HTTPError or urllib2.URLError when cannot get the url"""
    if not url:
        return '', None, None,

    if 'http://' in url and 'http://www.' not in url:
        url = url.replace('http://', 'http://www.')

    req, res, data, headers = urllib2.Request(url), None, '', None
    if use_gzip:
        req.add_header('Accept-Encoding', ACCEPT_ENCODING)
    req.add_header('User-Agent', USER_AGENT)
    res = urllib2.urlopen(req, timeout=timeout)
    headers, data = res.headers, res.read()
    if headers.getheader('Content-Encoding', default=None) == GZIP:
        try:
            data = gzip.GzipFile(fileobj=StringIO.StringIO(data)).read()
        except ALL_ERROR:
            if use_gzip:
                return getUrl(url, use_gzip=False)

    return data, headers, getattr(res, '_sa', None)


#===============HttpPool Func=================
#=============================================
def base_log(msg, log_handler=None):
    if log_handler is None:
        print msg,
    else:
        log_handler.write(msg)


def base_fail_op(tid, msg):
    print tid, msg


def base_worker(tasks, results, fail_code, fail_op=None):
    while True:
        res, task = 0L, tasks.get()
        tid = task['id']
        in_obj = task['in_obj']
        try:
            res = in_obj._run()
        except ALL_ERROR as ex:
            msg = '\nError in base_worker:%s -> %s\n' % (tid, E(ex))
            if fail_op: fail_op(tid, msg)
            res = (fail_code, msg,)
        finally:
            results.put((tid, res, in_obj,), True)


#===================HttpPool==================
#=============================================
class HttpPool(BaseObjectWithLog):
    """__init__(self, threads_count, doing_count,
    log_file_in=None, usePriorityQueue=False, worker=base_worker,
    log_func_in=base_log, fail_op=base_fail_op)
    httppool to tun task with worker use:add, join"""
    def __init__(self, threads_count, doing_count, fail_code,log_file_in=None, log_func_in=base_log, worker=base_worker, fail_op=base_fail_op):
        super(HttpPool, self).__init__(log_func_in=log_func_in,
                                       log_file_in=log_file_in)
        self.__thread_list = []
        self._tasks, self._results = Queue(), Queue()
        self.worker = worker
        self.worker_args = (self._tasks, self._results, fail_code, fail_op,)
        self.__max = doing_count
        self.__now = 0L
        self.__run_thread(threads_count)

    def close(self):
        if self.log_handler:
            self.log_handler.close()

    @property
    def max(self):
        return self.__max

    @property
    def now(self):
        return self.__now

    def __run_thread(self, threads_count):
        self.log('\n%s.__run_thread:%s\n' %
                 (self.__class__.__name__, threads_count))
        for _ in xrange(threads_count):
            tmp = threading.Thread(target=self.worker, args=self.worker_args)
            tmp.setDaemon(True)
            tmp.start()
            self.__thread_list.append(tmp)

    def __check_thread(self, add_new=True):
        pass

    def __add_task(self, tid, in_obj):
        task = {'id': tid, 'in_obj': in_obj}
        if self.__now < self.__max:
            try:
                self._tasks.put_nowait(task)
                self.__now += 1
                return True
            except Full:
                return False

    def __get_results(self):
        results = []
        if self.__now > 0:
            while True:
                try:
                    res = self._results.get_nowait()
                except Empty:
                    break
                self.__now -= 1
                results.append(res)
        return results

    def __do_info(self, t, n, s, o):
        c = '+' if n > 0 else '!' if n < 0 else '#'
        msg = datetime.datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S') + s if s else ''
        self.log('(%s%d,%d,"%s")' % (c, t, n, msg))
        o._done(t, n, s)
        del o
        return n if n > 0 else 0

    def __do_results(self, results, add_count):
        for info in results:
            t, n, s, o = info[0], info[1][0], info[1][1].strip(), info[2]
            add_count += self.__do_info(t, n, s, o)
        return add_count

    def add_and_run(self, tid, obj, add_count=0L):
        """ add_and_run(self, tid, obj, add_count=0L) in main thread """
        self.__now = 1
        ret = obj._ready()
        self.log('(%s%d,%d,"%s")' % ('*', tid, add_count, ret))
        ret = obj._run()
        t, n, s, o = tid, ret[0], ret[1].strip(), obj
        add_count += self.__do_info(t, n, s, o)
        return add_count

    def add(self, tid, obj, add_count=0L):
        """add_task_obj(self, tid, obj, add_count=0L)"""
        if self.__max <= 0:
            return self.add_and_run(tid, obj, add_count)

        self.__check_thread()
        ret = obj._ready()
        while not self.__add_task(tid, obj):
            results = self.__get_results()
            if results:
                add_count = self.__do_results(results, add_count)
            time.sleep(1.0 * random.random())
        self.log('(%s%d,%d,"%s")' % ('*', tid, add_count, ret))
        return add_count

    def join(self, add_count=0L, max_count_wait=200, per_count_wait=50):
        """wait_task_obj(self, add_count=0L, max_count_wait = 200, per_count_wait=50)"""
        count_wait = 0L
        while self.__now > 0:
            results = self.__get_results()
            if results:
                add_count = self.__do_results(results, add_count)
                count_wait = 0L
            else:
                time.sleep(1.0 * random.random())
                count_wait += 1
                self.log('.')
                if count_wait > max_count_wait or count_wait > self.__now * per_count_wait:
                    ret = "End HttpPool, but worker not all finish!"
                    self.log('(%s%d,%d,"%s")' %
                             ('@', self.__now, add_count, ret))
                    self.__now = 0
                    break
        return add_count


#====================Crawl====================
#=============================================
class Crawl(BaseObjectWithLog):
    def __init__(self, c, job, doing ,log_func_in=None, log_file_in=None):
        super(Crawl, self).__init__(log_func_in=log_func_in,
                                    log_file_in=log_file_in)
        self.__dict__.update(c['debug_mode', 'todo_max',])
        self.__dict__.update(c.flag['flag_todo','flag_done','flag_noobj','flag_getonly',])
        self.todo = {}
        self.new_start = False
        self.job = job
        self.doing = doing
        self.init_db(c.mongo.mongo_host, c.mongo.mongo_port)
        self.inti_todo(c.mongo.root_url, c.mongo.root_ufrom, c.mongo.root_deep, job, doing)

    def close(self):
        _close = lambda f:f.close() if f and hasattr(f, 'close') else None
        _close(self.con)
        _close(self.log_handler)

    def init_db(self, mongo_host, mongo_port):
        self.con = pymongo.MongoClient(mongo_host, mongo_port)
        self.cur = self.con.www.link
        self.cur_html = self.con.html.html
        self.cur_soup = self.con.soup.soup

    def inti_todo(self, root_url, root_ufrom, deep, todo_flag, flag_doing, max_get=1.5):
        ret = self.cur.find({'do_flag': todo_flag}, {'charset': 1, 'url': 1, 'deep': 1, '_id': 0}).sort('deep',pymongo.ASCENDING).limit(int(self.todo_max*max_get))
        if ret.count(with_limit_and_skip=True) > 1:
            self.new_start = False
            for _, u in enumerate(ret):
                if len(self.todo) >= self.todo_max:
                    break
                update_res = self._update_dict({'url': u['url'],'do_flag':todo_flag},{'do_flag': flag_doing}, False)
                if update_res.modified_count>0 and update_res.matched_count>0:
                    self.todo.setdefault(u['url'], (u['deep'], u['charset']) )
        elif root_url:
            self.new_start = True
            self.todo.setdefault(root_url, (deep,'') )
            self.insert_url(root_url, root_ufrom, deep, todo_flag)

    def pop_url(self, use_mongodb=True):
        if self.todo:
            if len(self.todo) == 1 and use_mongodb:
                self.inti_todo(None, None, None, self.job, self.doing)
            return self.todo.popitem()
        elif use_mongodb:
            self.inti_todo(None, None, None, self.job, self.doing)
            return self.pop_url(use_mongodb=False)
        else:
            return None,(None,None)

    def insert_links(self, url_list, ufrom, deep, do_flag, is_log=True):
        ret_num = 0
        for url in url_list:
            ret_bool = self.insert_url(url, ufrom, deep, do_flag, is_log)
            ret_num += 1 if ret_bool else 0
        return ret_num

    def insert_url(self, url, ufrom, deep, do_flag, is_log=True):
        try:
            self.cur.insert_one({'url': url,'ufrom': ufrom,'deep': deep,'do_flag': do_flag,'charset':''})
            return True
        except pymongo.errors.PyMongoError as ex:
            self.log('\nError -> Crawl.insert_url:%s,%s,%s\n' % (E(ex), url, ufrom), is_log)
            return False

    def save_html(self, url, html, is_log=True):
        if url and html:
            self._save(self.cur_html, {'url': url, 'html': html}, is_log)

    def save_soup(self, url, soup, is_log=True):
        if url and soup:
            self._save(self.cur_soup, {'url': url, 'soup': soup}, is_log)

    def _save(self, obj, ret, is_log):
        try:
            if obj and ret:
                obj.insert_one(ret)
        except pymongo.errors.PyMongoError as ex:
            self.log('\nError -> Crawl._save:%s,%s\n' % (obj, ex), is_log)

    def load_html(self, url, is_log=True):
        if url:
            return self._load(self.cur_html, {'url': url}, 'html', is_log)

    def load_soup(self, url, is_log=True):
        if url:
            return self._load(self.cur_soup, {'url': url}, 'soup', is_log)

    def _load(self, obj, find, key, is_log):
        try:
            if obj and find:
                ret = obj.find_one(find, {key:1,'_id':0})
                return ret[key] if ret and key in ret else None
        except pymongo.errors.PyMongoError as ex:
            self.log('\nError -> Crawl._load:%s,%s\n' % (obj, ex), is_log)

    def save_ret(self, url ,deep, ret, msg, is_log=True):
        ret_num = self.insert_links(ret['linkset'], url, deep+1, self.flag_todo, is_log)
        setdict = {
            'title': ret['title'],
            'head': ret['head']['__list__'],
            'description':ret['head']['description'] if 'description' in ret['head'] else '',
            'keywords':ret['head']['keywords'] if 'keywords' in ret['head'] else '',
            'charset': ret['charset'],
            'links': ret['linkset'],
            'do_flag': self.flag_done if ret['soup'] else self.flag_noobj,
            'msg': msg
        }
        self.update_setdict(url, setdict, upsert=False, is_log=True)
        if ret['soup']:
            self.save_soup(url, ret['soup'], is_log)
        return ret_num

    def update_setdict(self, url, setdict, upsert=True, is_log=True):
        return self._update_dict({'url': url}, setdict, upsert, is_log)

    def _update_dict(self, find, update, upsert, is_log=True):
        isdict = lambda kv:hasattr(kv, 'items')
        isiter = lambda kv:hasattr(kv, '__iter__')
        repk = lambda k:k.replace('.', '_') if isinstance(k, (str, unicode)) else k
        mkr = lambda kv:{repk(k):mkr(v) for (k,v) in kv.items()} if isdict(kv) else [mkr(i) for i in kv] if isiter(kv) else kv
        ret = None
        try:
            if update:
                ret = self.cur.update_one(find, {'$set': mkr(update)}, upsert)
        except pymongo.errors.PyMongoError as ex:
            self.log('\nPyMongoError -> Crawl._update_dict:%s,%s,%s\n'%(E(ex), find, repr(update)[:20]), is_log)
        except ALL_ERROR as ex:
            self.log('\nException -> Crawl._update_dict:%s,%s,%s\n' %(E(ex), find, repr(update)[:20]), is_log)
        return ret

def _T(now=None):
    if now is None:
        now = datetime.datetime.now()
    return now, now.strftime('%Y-%m-%d %H:%M:%S')


def _LOG(msg, log_handler=None):
    print msg


GET_CONF = {
    'debug_mode': False,
    'use_hold': True,
    'log': {'log_www': 'www_%s.log',
            'log_debug': 'debug_%s.log'},
    'proxy': {
        'use_proxy': False,
        'proxy_url': 'http://127.0.0.1:8087',
        'proxy_scheme': 'http'
    },
    'mongo': {
        'root_deep': 1,
        'root_url': 'http://163.com/',
        'root_ufrom': 'root',
        'mongo_host': 'localhost',
        'mongo_port': 27017
    },
    'flag': {
        'flag_todo': 0,
        'flag_done': 1,
        'flag_noobj': 2,
        'flag_getonly': 3,
        'flag_doing': 7,
        'flag_geting': 8,
        'flag_get_and_do': 9
    },
    'threads_count': 0,
    'doing_count': 0,
    'fail_code': -999,
    'todo_max': 60,
    'get_only':False,
}


def main():
    c = Conf(GET_CONF, log_func=_LOG)

    m_count = 0
    m_start = _T()[0]

    while c.use_hold and not c.debug_mode:
        m_count = do_web_run(c, log_func=_LOG, run_count=m_count)

    _LOG('\n\n%s    All Count:%s\nUse Time:%s' %
         (_T(_T()[0])[1], m_count, m_start - _T()[0]))

def do_web_run(c, log_func=lambda msg: msg, run_count=0, tid=0, pre_log=10):
    pzb = lambda s:cPickle.loads(zlib.decompress(base64.decodestring(html.replace('-', '+').replace('_', '/')))) if s else ''
    log_pre = lambda msg, tid: log_func(msg) if tid % pre_log == 1 else None
    log_func('\n%s    Run and Run......\n' % (_T()[1]))
    with Crawl(c, c.flag.flag_getonly, c.flag.flag_doing, log_func_in=log_func) as cr:
        while cr.todo:
            url, (deep, charset) = cr.pop_url()
            html_str, html = '', cr.load_html(url)
            try:
                html_str = pzb(html)
            except ALL_ERROR:
                continue
            if html_str:
                tid += 1
                log_pre('\n%s    Tid:%s(%s) >> Url:%s\n' % (_T()[1], tid, run_count, url), tid)
                ret, msg = do_ret(html_str, charset)
                run_count += cr.save_ret(url, deep, ret, msg, is_log=False)
    return run_count
class Conf(object):

    def __init__(self, dict_in, log_func=None, top_init=True):
        dict_in = {
            k: Conf(v, None, False) if isinstance(v, dict) else v
            for k, v in dict_in.items()
        }
        self.__dict__.update(dict_in)
        if top_init:
            file_name = self.log.log_www if not self.debug_mode else self.log.log_debug
            self.log_file = os.path.join(os.getcwd(), file_name % (os.getpid()))
            dumps_set = {'mongo': 0,'proxy': 0,'log': 0,'flag': 0}
            isf = lambda f: hasattr(f, '__call__')
            getv = lambda k, v, fs: fs[k](v) if k in fs and isf(fs[k]) else v
            cls = lambda c:'\n' + c.__class__.__name__ + ':\n\t'
            if log_func and isf(log_func):
                log_func(cls(self) + '\n\t'.join(['%s: %s' % (k, getv(k, v, dumps_set)) for k, v in vars(self).items() if dumps_set.get(k, 1)]))

    def __getitem__(self, key):
        """
        conf.get( iterable=>tuple(in_key [,out_key=in_key [,default]]) )
        return {out_key: getattr(conf, in_key [,default]) }
        """
        ret = {}
        for t in key:
            tn = len(t) if t and isinstance(t, tuple) else 0
            in_key = t[0] if tn >= 1 else t
            out_key = t[1] if tn >= 2 else in_key
            ret[out_key] = getattr(self, in_key, t[2]) if tn == 3 else getattr(self, in_key)
        return ret

    def __str__(self):
        return str({k: str(v) for k, v in self.__dict__.items()})


if __name__ == '__main__':
    main()
    _LOG('\n============End=============\n')
