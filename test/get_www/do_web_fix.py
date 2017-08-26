#-*- coding: utf-8 -*-
"""get all web
kl,2015-9-13 14:57:49
"""
import multiprocessing
from get_and_do import T, LOG, PZB, ALL_ERROR, _do_ret
from get_and_do import Conf, Crawl, HttpPool


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
    'threads_count': 5,
    'doing_count': 200,
    'fail_code': -999,
    'todo_max': 800,
    'get_only':False,
}


def main():
    c = Conf(GET_CONF, log_func=LOG)

    m_count = 0
    m_start = T()[0]

    while c.use_hold and not c.debug_mode:
        m_count = do_web_run(c, run_count=m_count)

    LOG('\n\n%s    All Count:%s\nUse Time:%s' %
         (T(T()[0])[1], m_count, m_start - T()[0]))


def do_web_run(c, run_count=0, tid=0, pre_log=10):
    LOG('\n%s    Run and Run......\n' % (T()[1]))
    ret_html = []
    with Crawl(c, c.flag.flag_getonly, None, log_func_in=LOG) as cr:
        while cr.todo:
            url, (deep, charset) = cr.pop_url()
            html_str, html = '', cr.load_html(url)
            try:
                html_str = PZB(html)
            except ALL_ERROR:
                continue
            tid += 1
            ex_code, url, deep, ret, msg = _do_ret((html_str, charset, url, deep,))
            if ex_code<0:
                cr.update_setdict(url, {'do_flag': ex_code, 'msg': msg})
            else:
                run_count += cr.save_ret(url, deep, ret, msg, is_log=False)
    return run_count


def _mutil(func, args_list, process_num=5):
    return [func(i) for i in args_list]

def mutil(func, args_list, process_num=5):
    pool = multiprocessing.Pool(processes=process_num)
    results = pool.map_async(func, args_list)
    pool.close()
    pool.join()
    return results.get()

if __name__ == '__main__':
    main()
    LOG('\n============End=============\n')
