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
import ssl
## HttpPool
import time
import random
import threading
import Queue
import multiprocessing
## Retrieve getLinks
from bs4 import BeautifulSoup
import urlparse
## Crawl mongoDB
import pymongo


HTTP_TIME_OUT = 30
USER_AGENT = (
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36'
)
ACCEPT_ENCODING = 'gzip,deflate'
GZIP = 'gzip'

ZIP_LEVEL = 7
BZC = lambda o, l: base64.b64encode(zlib.compress(cPickle.dumps(o), l), ('-', '_'))
CZB = lambda s: cPickle.loads(zlib.decompress(base64.b64decode(s, ('-', '_'))))
PZB = lambda s:cPickle.loads(zlib.decompress(base64.decodestring(s.replace('-', '+').replace('_', '/')))) if s else ''

class Error(Exception):
    pass

ALL_ERROR = Exception

def E(e):
    try:
        return '%s:%r' % (e.__class__.__name__, e)
    except ALL_ERROR as ex:
        return '%s(%s)' % ('cannot get ex.msg!', E(ex))

def T(now=None):
    if now is None:
        now = datetime.datetime.now()
    return now, now.strftime('%Y-%m-%d %H:%M:%S')


def LOG(msg, log_handler=None):
    print msg

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

def getUrl(url, use_gzip=True, timeout=HTTP_TIME_OUT):
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
    if headers.getheader('Content-Encoding', default='').lower() == GZIP:
        try:
            data = gzip.GzipFile(fileobj=StringIO.StringIO(data)).read()
        except ALL_ERROR:
            if use_gzip:
                return getUrl(url, use_gzip=False)

    return data, headers, getattr(res, '_sa', None)

NO_URL = -10
NO_HTML = -20
NO_LINKS = -11
NET_ERROR = -100
HTTP_LIB_ERROR = -101
IO_ERROR = -102
SSL_ERROR = -103

TIME_OUT = -110
#===================GET_LINKS=================
#=============================================
def get_links(html, charset='', msg=''):
    """get html links"""
    def _do_head(head):
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

    def _func_do_link_list(links):
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
        bad_url = lambda url:':' in url or '.' not in url or _bad_url(url.split('.'))
        ret_list = [url for url in tmp if not bad_url(url)]
        return set(ret_list)

    _get_meta = lambda s:[i.attrs for i in s.head.findAll('meta')] if hasattr(s, 'head') and s.head else []
    _get_head = lambda s:s.title.text if hasattr(s, 'title') and hasattr(s.title, 'text') else ''
    _get_link = lambda s:[i.attrs['href'] for i in s.findAll('a') if i and 'href' in i.attrs]
    code, ret = 1, None
    try:
        from_encoding = charset if charset else None
        soup = BeautifulSoup(html, 'html.parser',from_encoding=from_encoding)
        charset = getattr(soup, '_dc', '')
        title = _get_head(soup)
        head = _do_head(_get_meta(soup))
        retset = _func_do_link_list(_get_link(soup))
        ret = {'linkset': retset,'charset': charset,'title': title,'head': head,}
    except ALL_ERROR as ex:
        msg += '\nGetLinks->%s\n' % (E(ex))
        code = NO_LINKS

    return code, msg, ret


def do_ret(html, charset, msg=''):
    if html:
        code, msg, ret = get_links(html, charset, msg)
        code = NO_LINKS if code>=0 and not ret else code
        return code, msg, ret
    else:
        return NO_HTML, '', None

def _do_ret(tuple_in):
    html_str, charset, url, deep = tuple_in
    ex_code, msg, ret = do_ret(html_str, charset)
    return ex_code, url, deep, ret, msg


#===================GET_HTML=================
#=============================================
def get_html(url_in, msg=''):
    def test_charset(content, msg=''):
        """test_charset(content, msg='', default='', use_chardet_detect=False):"""
        def get_charset(cstr, charset='', fstr='charset=', spl=('"', "'", ';', ',',), max_len=64):
            if fstr in cstr:
                si = cstr.find(fstr) + len(fstr)
                charset = cstr[si:si + max_len].split()[0] if cstr[si:si + max_len].strip() else ''
                for sp in spl:
                    charset = charset.split(sp)[0] if sp in charset else charset
            return charset

        content_text = content.getheader('content-type', '') if hasattr(content, 'getheader') else ''
        ret_charset = get_charset(content_text.lower()).strip()
        try:
            ret_charset = codecs.lookup(ret_charset).name if ret_charset else ''
        except ALL_ERROR as ex:
            msg += '\nget_charset or chardet.detect error:%s,%s,%s\n' % (E(ex), content_text, ret_charset)
        return ret_charset, msg

    ex_code = lambda n, d=NET_ERROR: -abs(int(n)) if n is not None and int(n) else d
    ex_msg = lambda e, u=url_in:'\n%s->%s\n' % (E(e), u)
    code, ret = 1, None
    try:
        html, content, _sa = getUrl(url_in, use_gzip=True)
        ip, port = _sa if isinstance(_sa, tuple) and len(_sa) == 2 else ('', 0)
        charset, msg = test_charset(content, msg)
        zhtml = BZC(html,ZIP_LEVEL)
        ret = {'content': content,'html': zhtml,'charset': charset,'ip': ip,'port': port, '__html__':html}
    except urllib2.HTTPError as ex:
        msg += ex_msg(ex)
        code = ex_code(ex.code)
    except urllib2.URLError as ex:
        msg += ex_msg(ex)
        code = ex_code(SSL_ERROR) if isinstance(ex.reason, ssl.SSLError) else ex_code(ex.reason.errno)
    except socket.error as ex:
        msg += ex_msg(ex)
        code = ex_code(ex.errno, TIME_OUT)
    except httplib.HTTPException as ex:
        msg += ex_msg(ex)
        code = ex_code(HTTP_LIB_ERROR)
    except IOError as ex:
        msg += ex_msg(ex)
        code = ex_code(IO_ERROR)

    code = code-1000 if -100<code<0 else code
    return code, msg, ret

def do_html(url, msg=''):
    if url:
        code, msg, ret = get_html(url, msg)
        code = NET_ERROR if code>=0 and not ret else code
        return code, msg, ret
    else:
        return NO_URL, '', None


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

    def __init__(self, threads_count, doing_count, fail_code, use_multiprocessing=False,log_file_in=None, log_func_in=base_log, worker=base_worker, fail_op=base_fail_op):
        super(HttpPool, self).__init__(log_func_in=log_func_in, log_file_in=log_file_in)
        if not use_multiprocessing:
            self.__dict__.update({'_queue':Queue.Queue, '_start':threading.Thread})
        else:
            self.__dict__.update({'_queue':multiprocessing.Queue, '_start':multiprocessing.Process})
        self.__thread_list = []
        self._tasks, self._results = self._queue(), self._queue()
        self.worker = worker
        self.worker_args = (self._tasks, self._results, fail_code, fail_op,)
        self.__max = doing_count
        self.__now = 0L
        if doing_count>0:
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
            tmp = self._start(target=self.worker, args=self.worker_args)
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
            except Queue.Full:
                return False

    def __get_results(self):
        results = []
        if self.__now > 0:
            while True:
                try:
                    res = self._results.get_nowait()
                except Queue.Empty:
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
        ret_ready = obj._ready()
        self.log('(%s%d,%d,"%s")' % ('*', tid, add_count, ret_ready))
        ret = obj._run()
        t, n, s, o = tid, ret[0], ret[1].strip(), obj
        add_count += self.__do_info(t, n, s, o)
        return add_count

    def add(self, tid, obj, add_count=0L):
        """add_task_obj(self, tid, obj, add_count=0L)"""
        if self.__max <= 0:
            return self.add_and_run(tid, obj, add_count)

        self.__check_thread()
        ret_ready = obj._ready()
        while not self.__add_task(tid, obj):
            results = self.__get_results()
            if results:
                add_count = self.__do_results(results, add_count)
            time.sleep(1.0 * random.random())
        self.log('(%s%d,%d,"%s")' % ('*', tid, add_count, ret_ready))
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
        self.__dict__.update(c.flag['flag_todo','flag_done','flag_getonly',])
        self.todo = {}
        self.new_start = False
        self.job = job
        self.doing = doing
        if self.debug_mode:
            self.doing = None
        self.init_db(c.mongo.mongo_host, c.mongo.mongo_port)
        self.inti_todo(c.mongo.root_url, c.mongo.root_ufrom, c.mongo.root_deep, job, doing)

    def close(self):
        _close = lambda f:f.close() if f and hasattr(f, 'close') else None
        _close(self.con)
        _close(self.log_handler)

    def init_db(self, mongo_host, mongo_port):
        self.con = pymongo.MongoClient(mongo_host, mongo_port)
        self.cur = self.con.www.link2
        self.cur_html = self.con.html.html

    def inti_todo(self, root_url, root_ufrom, deep, todo_flag, flag_doing, max_get=1.5):
        ret = self.cur.find({'do_flag': todo_flag}, {'charset': 1, 'url': 1, 'deep': 1, '_id': 0}).sort('deep',pymongo.ASCENDING).limit(int(self.todo_max*max_get))
        if ret.count(with_limit_and_skip=True) > 1:
            self.new_start = False
            for _, u in enumerate(ret):
                if len(self.todo) >= self.todo_max:
                    break
                if flag_doing and not self.debug_mode:
                    update_res = self._update_dict({'url': u['url'],'do_flag':todo_flag},{'do_flag': flag_doing}, False)
                    if update_res.modified_count>0 and update_res.matched_count>0:
                        self.todo.setdefault(u['url'], (u['deep'], u['charset'], ))
                else:
                    self.todo.setdefault(u['url'], (u['deep'], u['charset'], ))
        elif root_url:
            self.new_start = True
            self.todo.setdefault(root_url, (deep,'') )
            self.insert_url(root_url, root_ufrom, deep, todo_flag)

    def del_url(self, url):
        self.cur.delete_one({'url':url})
        self.cur_html.delete_one({'url':url})

    def pop_url(self, use_mongodb=True):
        if self.todo:
            if self.todo_max>1 and len(self.todo) == 1 and use_mongodb:
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

    def _save(self, obj, ret, is_log):
        try:
            if obj and ret:
                obj.insert_one(ret)
        except pymongo.errors.PyMongoError as ex:
            self.log('\nError -> Crawl._save:%s,%s\n' % (obj, ex), is_log)

    def load_html(self, url, is_log=True):
        if url:
            return self._load(self.cur_html, {'url': url}, 'html', is_log)

    def _load(self, obj, find, key, is_log):
        try:
            if obj and find:
                ret = obj.find_one(find, {key:1,'_id':0})
                return ret[key] if ret and key in ret else None
        except pymongo.errors.PyMongoError as ex:
            self.log('\nError -> Crawl._load:%s,%s\n' % (obj, ex), is_log)

    def save_ret(self, url ,deep, ret, msg, is_log=False):
        ret_num = self.insert_links(ret['linkset'], url, deep+1, self.flag_todo, is_log=is_log)
        setdict = {
            'title': ret['title'],
            'head': ret['head']['__list__'] if '__list__' in ret['head'] else None,
            'description':ret['head']['description'] if 'description' in ret['head'] else '',
            'keywords':ret['head']['keywords'] if 'keywords' in ret['head'] else '',
            'charset': ret['charset'],
            'links': ret['linkset'],
            'do_flag': self.flag_done,
            'msg': msg
        }
        self.update_setdict(url, setdict, is_log=True)
        return ret_num

    def save_get_only(self, url, ret, set_do_flag, msg):
        def _unicode(v, c=None):
            if isinstance(v, str):
                charset = {c, 'gbk', 'utf-8'} if c else {'gbk', 'utf-8'}
                for ct in charset:
                    try:
                        v = v.decode(ct)
                        break
                    except ALL_ERROR:
                        pass
                else:
                    v = repr(v)
            return v
        _unicode_dict = lambda kv,c:{_unicode(k,c):_unicode(v,c) for k,v in kv.items()}
        content = _unicode_dict(ret['content'], ret['charset'])
        getonly = {
            'charset': ret['charset'],
            'content': content,
            'ip': ret['ip'],
            'port': ret['port'],
            'do_flag': set_do_flag,
            'msg': msg
        }
        self.update_setdict(url, getonly, upsert=False, is_log=True)
        self.save_html(url, ret['html'], is_log=False)

    def update_setdict(self, url, setdict, upsert=False, is_log=True):
        return self._update_dict({'url': url}, setdict, upsert, is_log)

    def _update_dict(self, find, update, upsert, is_log=True):
        isdict = lambda kv:hasattr(kv, 'items')
        isiter = lambda kv:hasattr(kv, '__iter__')
        repk = lambda k:k.replace('.', '_').replace('$', '#') if isinstance(k, (str, unicode)) else k
        mkr = lambda kv:{repk(k):mkr(v) for (k,v) in kv.items()} if isdict(kv) else [mkr(i) for i in kv] if isiter(kv) else kv
        ret = None
        try:
            if update:
                ret = self.cur.update_one(find, {'$set': mkr(update)}, upsert)
        except pymongo.errors.PyMongoError as ex:
            msg = '\nPyMongoError -> Crawl._update_dict:%s,%s,%s\n'%(E(ex), find, repr(update)[:20])
            self.log(msg, is_log)
        except ALL_ERROR as ex:
            msg = '\nException -> Crawl._update_dict:%s,%s,%s\n' %(E(ex), find, repr(update)[:20])
            self.log(msg, is_log)
        return ret



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
            self.todo_max = self.todo_max if not self.debug_mode else 5
            self.doing_count = self.doing_count if not self.debug_mode else 0
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
        'flag_getonly': 3,
        'flag_geting': 8
    },
    'threads_count': 30,
    'doing_count': 50,
    'fail_code': -999,
    'todo_max': 60,
    'get_only':False,
}


def main():
    _ = Conf(GET_CONF, log_func=LOG)
    pass

if __name__ == '__main__':
    main()
    LOG('\n============End=============\n')
