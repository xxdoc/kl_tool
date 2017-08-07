#-*- coding: utf-8 -*-
"""get all web
kl,2015-9-13 14:57:49
"""
from get_and_do import T, LOG, E, ALL_ERROR
from get_and_do import Conf, Crawl, HttpPool
from get_and_do import httpProxy, do_html, do_ret

#===================Retrieve==================
#=============================================
class Retrieve(object):
    def __init__(self, cr_in, url_in, deep, get_only=True):
        self.ret = None  ## ret = {'content': content,'html': zhtml,'charset': charset,'ip': ip,'port': port, '__html__':html}
        self.url = url_in
        self.cr = cr_in
        self.deep = deep
        self.get_only = get_only

    def _ready(self):
        pass

    def _run(self):
        """-11004,-11003,-10061,-10060,-10054,-10053,-10051,-10049,"""
        ex_code, msg = -99, 'run error'
        try:
            ex_code, msg, self.ret = do_html(self.url)
            UnicodeError
        except UnicodeError as ex:
            LOG(E(ex))
            self.cr.del_url(self.url)
        except UnicodeEncodeError as ex:
            LOG(E(ex))
            self.cr.del_url(self.url)
##        except ALL_ERROR as ex:
##            LOG(E(ex))
        return ex_code, msg

    def _done(self, tid, ex_code, msg):
        if ex_code>=0:
            self.cr.save_get_only(self.url, self.ret, self.cr.flag_getonly, msg)
        elif ex_code<0:
            self.cr.update_setdict(self.url, {'do_flag': ex_code, 'msg': msg})


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
        'flag_geting': 8,
        'flag_get_and_do': 9
    },
    'use_multiprocessing':False,
    'threads_count': 100,
    'doing_count': 200,
    'fail_code': -999,
    'todo_max': 2000,
    'get_only':True,
}


def main():
    c = Conf(GET_CONF, log_func=LOG)

    if c.proxy.use_proxy:
        httpProxy(c.proxy.proxy_url, proxy_http=c.proxy.proxy_scheme)

    m_count = 0
    m_start = T()[0]
    with HttpPool(c.threads_count, c.doing_count, c.fail_code, c.use_multiprocessing, log_file_in=c.log_file) as hp:
        m_count = www_run(c, hp, run_count=m_count)
        while c.use_hold and not c.debug_mode:
            m_count = www_run(c, hp, run_count=m_count)

    LOG('\n\n%s    All Count:%s\nUse Time:%s' % (T()[1], m_count, m_start - T()[0]))

def www_run(c, hp, run_count=0,  tid=0, pre_log=50):
    LOG('\n%s    Run and Run......\n' % (T()[1]))
    with Crawl(c, c.flag.flag_todo, c.flag.flag_geting, log_func_in=LOG) as cr:
        while cr.todo or hp.now:
            url, (deep, _) = cr.pop_url()
            if not url:
                continue
            if c.debug_mode: LOG('%s(%s)'%(url, deep))
            tid, ret = tid + 1, Retrieve(cr, url, deep, c.get_only)
            run_count = hp.add_and_run(tid, ret, run_count) if cr.new_start else hp.add(tid, ret, run_count)
            if tid % pre_log == 1:
                LOG('\n%s    Tid:%s(%s) >> Url:%s(%s)\n' % (T()[1], tid, run_count, url, deep))
        run_count = hp.join(run_count)
    return run_count


if __name__ == '__main__':
    main()
    LOG('\n============End=============\n')
