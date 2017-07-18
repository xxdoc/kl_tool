#!/usr/bin/python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        web http download
# Purpose:
#
# Author:          Administrator
#
# Created:     20/03/2014
# Copyright:   (c) Administrator 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import sys
import os
import datetime
import urllib2

import thread
import time
import random
from Queue import Queue, Empty, Full
# BeautifulSoup for HTML
import re

base_cfg = \
    """{
                                "base_set": {
                                "base_path": "",
                                "cfg_file": "wow_ah.cfg",
                                "JSON_path": "JSON",
                                "DATA_TEMP_path": "DATA_TEMP",
                                "DATA_BAK_path": "DATA_BAK",
                                "bak_size_limt": 100
                            },
                            "MySQL_set": {
                                "host": "127.0.0.1",
                                "user": "root",
                                "passwd": "root",
                                "db": "wow_ah_db",
                                "item_db": "wow_item_db",
                                "charset": "utf8",
                                "port": 3306,
                                "ah_tmp": "aaa_ah_tmp",
                                "fwq_tmp": "aaa_fwq_tmp",
                                "fwq_all_status": "aa_fwq_status",
                                "fwq_all_info": "aa_fwq_info",
                                "fwq_all_tmp": "aaa_fwq_all",
                                "wow_item_table": "aaa_wow_item",
                                "wow_item_tmp": "aaa_item_tmp",
                                "wow_item_str": "aaa_item_str",
                                "wow_pet_str": "aaa_pet_str",
                                "wow_guild_list": "aaa_guild_list",
                                "wow_guild_tmp": "aaa_guild_tmp"
                            },
                            "log_set": {
                                "filename": "db_log.txt",
                                "level": 20,
                                "filemode": "a",
                                "format": "%(asctime)s - %(levelname)s: %(message)s"
                            }
                        }"""

def enable_global_proxy(proxy_http="http", proxy_url="http://127.0.0.1:8087",enable_proxy = True):
    if enable_proxy:
        proxy_handler = urllib2.ProxyHandler({proxy_http : proxy_url})
        opener = urllib2.build_opener(proxy_handler)
    else:
        null_proxy_handler = urllib2.ProxyHandler({})
        opener = urllib2.build_opener(null_proxy_handler)

    urllib2.install_opener(opener)


def log_with_time(str_log, new_line = None, enter = True):
    if new_line:
        print '\n',
    if enter:
        print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S  '),str_log
    else:
        print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S  '),str_log,

def log_with_info(str_log, new_line = None, enter = None):
    str_temp = (str_log) if (not new_line) else ('\n' + str_log)
    if enter:
        print str_temp
    else:
        print str_temp,


MOZILLA_HEADER ={'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.79 Safari/535.11 QIHU THEWORLD'}

HTTP_NO_ERROR = 0L
HTTP_ERROR_TASSK_INFO = 900L
HTTP_ERROR_PAGE_NOT_FOUND = 404L
HTTP_ERROR_REQUEST_TIME_OUT = 408L
HTTP_ERROR_SERVER_ERROR = 500L
HTTP_ERROR_SERVER_UNAVAIABLE = 503L

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

    global MOZILLA_HEADER
    global HTTP_NO_ERROR
    global HTTP_ERROR_TASSK_INFO
    global HTTP_ERROR_PAGE_NOT_FOUND
    global HTTP_ERROR_REQUEST_TIME_OUT
    global HTTP_ERROR_SERVER_ERROR
    global HTTP_ERROR_SERVER_UNAVAIABLE

    while True:
        task = tasks.get()
        err_code = HTTP_NO_ERROR
        res = ''

        tid = task['id']
        url = task['url']
        dict_sql = task['dict_sql']
        dict_in = task['dict_in']

        try:
            url_print = url.decode('utf-8').encode('gbk')
            task['url_print'] = url_print
        except Exception, e:
            url_print = str(tid) + ' (canot encode)  '
            task['url_print'] = url_print
            if log: log("\n'gbk' codec can't encode. tid = %s, url = %s \n%s : %s" % (tid, url_print,Exception, e) )

        try:
            count_error = 0L
            while len(res.strip()) == 0 and count_error < 10:
                try:
                    req = urllib2.Request(url, None, MOZILLA_HEADER )
                    res = urllib2.urlopen(req).read()
                except urllib2.HTTPError, e:
                    if e.code == 404:
                        #if log: log('\npage not found. tid = %s, url = %s \n%s : %s' % (tid, url_print,urllib2.HTTPError, e) )
                        err_code = HTTP_ERROR_PAGE_NOT_FOUND
                        #if fail_op: fail_op(task, err_code, log)
                        break
                    elif e.code == 500:
                        if log: log('\n web server error. tid = %s, url = %s \n%s : %s' % (tid, url_print,urllib2.HTTPError, e) )
                        err_code = HTTP_ERROR_SERVER_ERROR
                        if fail_op: fail_op(task, err_code, log)
                        break
                    elif e.code == 503:
                        if log: log('\n web Service Unavailable. tid = %s, url = %s \n%s : %s' % (tid, url_print,urllib2.HTTPError, e) )
                        err_code = HTTP_ERROR_SERVER_UNAVAIABLE
                        if fail_op: fail_op(task, err_code, log)
                        break
                    else:
                        if log: log('\n except Request. tid = %s, url = %s \n%s : %s' % (tid, url_print,urllib2.HTTPError, e) )
                        count_error = count_error + 1
                        continue
                except Exception, e:
                    pass
        finally:
            if len(res.strip()) == 0 and err_code == HTTP_NO_ERROR:
                #if log: log('request failed. tid = %s, url = %s' % (tid, url_print) )
                err_code = HTTP_ERROR_REQUEST_TIME_OUT
                #if fail_op: fail_op(task, err_code, log)

            res = (res) if (err_code == HTTP_NO_ERROR)  else ( str(err_code) )
            results.put((tid, res, url, dict_sql, dict_in), True)

class HttpPool(object):

    def __init__(
        self,
        threads_count=30,
        doing_count=20,
        fail_op=base_fail_op,
        log=base_log,
        ):

        self._tasks = Queue()
        self._results = Queue()
        self._threads_count_max = threads_count;
        self._doing_count_max = doing_count;
        self._doing_count_now = 0L;

        for i in xrange(threads_count):
            thread.start_new_thread(get_remote_data, (self._tasks,
                                    self._results, fail_op, log))

    def add_task(self, tid, url, dict_sql=None, dict_in=None):

        task = {'id': tid, 'url': url, 'dict_sql':dict_sql, 'dict_in':dict_in}
        if self._doing_count_now < self._threads_count_max:
            try:
                self._tasks.put_nowait(task)
            except Full:
                return False

            self._doing_count_now = self._doing_count_now + 1
            return True
        else:
            return False

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


    def _auto_add_task(self, task_id, url, dict_sql, dict_in, save_func, cursor_info, conn):
        #print task_id,url.decode('utf-8').encode('gbk')
        while True:
            if self.get_doing_count_now() < self.get_doing_count_max():
                if self.add_task(task_id, url, dict_sql, dict_in):
                    log_with_info("%s(add)" % (task_id))
                    break;
            results = self.get_results()
            if not results:
                time.sleep(1.0 * random.random())
            else:
                for i in results:
                    tr_count = save_func(i, cursor_info, conn, self)
                    if tr_count >= 0 :
                        log_with_info('%s(+%s)' % (i[0], tr_count) )
                    else:
                        log_with_info('%s(err:%s)' % (i[0], tr_count) )



    def _auto_wait_task(self, task_id, url, dict_sql, dict_in, save_func, cursor_info, conn):
        log_with_info('wait to end :%s... ' % (self.get_doing_count_now()), new_line = True)
        count_wait = 0L
        while self.get_doing_count_now() > 0:
            results = self.get_results()
            if not results:
                if count_wait > 100 or count_wait > self.get_doing_count_now()*50:
                    self.set_doing_count_now(0)
                    break;
                time.sleep(1.0 * random.random())
                count_wait = count_wait + 1
                log_with_info('.')
            else:
                count_wait = 0L
                for i in results:
                    tr_count = save_func(i, cursor_info, conn, self)
                    if tr_count >= 0 :
                        count_guild_add = count_guild_add + 1
                        log_with_info('%s(+%s)' % (i[0], tr_count) )
                    else:
                        log_with_info('%s(err:%s)' % (i[0], tr_count) )



