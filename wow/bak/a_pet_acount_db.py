#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import MySQLdb
import json
import os
import urllib2
import datetime
import time
import random
import binascii
import thread
from Queue import Queue, Empty, Full


base_cfg = \
    """{
                            "MySQL_set": {
                                "host": "127.0.0.1",
                                "user": "root",
                                "passwd": "root",
                                "db": "wow_test_db",
                                "charset": "utf8",
                                "port": 3306,
                                "fwq_all_info": "aa_fwq_info"
                            }
                        }"""

def enable_global_proxy(proxy_http, proxy_url,enable_proxy = True):
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
    if log: log('fail op. task = %s, status = %d' % (str(task), status))


def get_remote_data(
    tasks,
    results,
    fail_op,
    log,
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

        if err_code == HTTP_NO_ERROR:
            try:
                tid = task['id']
                url = task['url']
            except KeyError:
                if log: log(str(e))
                err_code = HTTP_ERROR_TASSK_INFO
                if fail_op: fail_op(task, err_code, log)
                #log('thread_%s doing task %d' % (thread.get_ident(), tid))

        try:
            url_print = url.decode('utf-8').encode('gbk')
        except Exception, e:
            url_print = str(tid) + ' (canot encode)'
            if log: log("\n'gbk' codec can't encode. tid = %s, url = %s \n%s : %s" % (tid, url_print,Exception, e) )

        if err_code == HTTP_NO_ERROR:
            count_error = 0L
            while len(res.strip()) == 0 and count_error < 10:
                try:
                    req = urllib2.Request(url, None, MOZILLA_HEADER )
                    res = urllib2.urlopen(req).read()
                except urllib2.HTTPError, e:
                    if e.code == 404:
                        if log: log('\npage not found. tid = %s, url = %s \n%s : %s' % (tid, url_print,urllib2.HTTPError, e) )
                        err_code = HTTP_ERROR_PAGE_NOT_FOUND
                        if fail_op: fail_op(task, err_code, log)
                        break
                    elif e.code == 500:
                        if log: log('\nweb server error. tid = %s, url = %s \n%s : %s' % (tid, url_print,urllib2.HTTPError, e) )
                        err_code = HTTP_ERROR_SERVER_ERROR
                        if fail_op: fail_op(task, err_code, log)
                        break
                    elif e.code == 503:
                        if log: log('\nweb Service Unavailable. tid = %s, url = %s \n%s : %s' % (tid, url_print,urllib2.HTTPError, e) )
                        err_code = HTTP_ERROR_SERVER_UNAVAIABLE
                        if fail_op: fail_op(task, err_code, log)
                        break
                    else:
                        if log: log('\nexcept Request. tid = %s, url = %s \n%s : %s' % (tid, url_print,urllib2.HTTPError, e) )
                    count_error = count_error + 1
                    continue

        if err_code == HTTP_NO_ERROR:
            if len(res.strip()) == 0:
                if log: log('request failed. tid = %s, url = %s' % (tid, url_print) )
                err_code = HTTP_ERROR_REQUEST_TIME_OUT
                if fail_op: fail_op(task, err_code, log)

        res = (res) if (err_code == HTTP_NO_ERROR)  else ( str(err_code) )
        results.put((tid, res, url), True)

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

    def add_task(self, tid, url):
        task = {'id': tid, 'url': url}
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


def down_guild_player_fwq_str(hp = None):
    if not hp:
        log_with_info('no http pool')
        return False
    log_with_time('SET Read ing... ')
    # print base_cfg
    bfj = json.loads(base_cfg)
    si = bfj['MySQL_set']

    log_with_time('DB Link ing... ')
    conn = MySQLdb.connect(host=si['host'], user=si['user'],
                           passwd=si['passwd'], db=si['db'],
                           charset=si['charset'], port=si['port'])
    cursor_fwq = conn.cursor()
    cursor_guild = conn.cursor()
    cursor_info = conn.cursor()
    cursor_info.execute('set names "utf8"')
    cursor_info.execute('SET GLOBAL innodb_flush_log_at_trx_commit = 0')
    cursor_info.execute('SET UNIQUE_CHECKS = 0')
    conn.commit()

    player_url = r'http://www.battlenet.com.cn/api/wow/guild/%s/%s?fields=members'
    pet_url = r'http://www.battlenet.com.cn/api/wow/character/%s/%s?fields=pets'

    log_with_time('DATE download ing... ')

    sql_fwq = 'select slug,zname,fwqID from ' + si['fwq_all_info'] + ' where fwqID>=0 order by fwqID'
    cursor_fwq.execute(sql_fwq)

    count_download = 0L

    while True:
        row_fwq = cursor_fwq.fetchone()
        if row_fwq == None:
	        break
        fwq_slug = row_fwq[0].replace('-','_')
        fwq_zname = row_fwq[1]

        sql_check = 'select table_name from information_schema.tables where table_name = "' + fwq_slug + '" and table_schema="' + si['db'] + '"'
        if cursor_info.execute(sql_check) == 0:
            log_with_time(''.join([str(row_fwq[2]), ' -> ', row_fwq[1], ':', fwq_slug, ' no Table ... ']), new_line = True)
            continue

        sql_count = 'select count(*) as total from ' + fwq_slug + ' limit 1'
        cursor_info.execute(sql_count)
        row_count = cursor_info.fetchone()
        log_with_time(''.join([str(row_fwq[2]), ' -> ', row_fwq[1], ':', fwq_slug, ' have:', str(row_count[0])]), new_line = True)

        sql_info = "update " + fwq_slug  + " set level=%s,achievementPoints=%s,pet_crc32=%s,numCollected=%s,lastModified=%s,account_id=%s where id=%s"
        sql_err ="update " + fwq_slug  + " set pet_crc32=%s,numCollected=%s,account_id=%s where id=%s"
        sql_select ="select id,achievementPoints from " + fwq_slug  + " where pet_crc32=%s order by id limit 1"

        sql_player = 'select id,name from ' + fwq_slug + ' where id>=0 and pet_crc32=0 and numCollected>=0 or numCollected=-503 order by id'
        cursor_guild.execute(sql_player)

        while True:
            row_player = cursor_guild.fetchone()
            if row_player == None:
                break

            count_download = count_download + 1

            url = pet_url % (fwq_zname.encode('utf-8'), row_player[1].encode('utf-8'))
            url = url.replace(' ','%20')

            task_id = row_player[0]

            #print task_id,url.decode('utf-8').encode('gbk')
            while True:
                if hp.get_doing_count_now() < hp.get_doing_count_max():
                    if hp.add_task(task_id, url):
                        log_with_info(str(task_id)+'(add)')
                        break;
                results = hp.get_results()
                if not results:
                    time.sleep(1.0 * random.random())
                else:
                    for i in results:
                        get_count = save_db_json_file(i, sql_info, sql_select, sql_err, cursor_info, conn, hp)
                        if get_count:
                            log_with_info(str(i[0])+'(get:' + str(get_count) + ')')
                        else:
                            log_with_info(str(i[0])+'(error)')

        log_with_info('wait to end-> ', new_line = True)
        count_wait = 0L
        while hp.get_doing_count_now() > 0:
            results = hp.get_results()
            if not results:
                if count_wait > 100 or count_wait > hp.get_doing_count_now()*30:
                    hp.set_doing_count_now(0)
                    break;
                time.sleep(1.0 * random.random())
                count_wait = count_wait + 1
                log_with_info('.')
            else:
                count_wait = 0L
                for i in results:
                    get_count = save_db_json_file(i, sql_info, sql_select, sql_err, cursor_info, conn, hp)
                    if get_count:
                        log_with_info(str(i[0])+'(get:' + str(get_count) + ')')
                    else:
                        log_with_info(str(i[0])+'(error)')

    cursor_info.execute('SET GLOBAL innodb_flush_log_at_trx_commit = 1')
    cursor_info.execute('SET UNIQUE_CHECKS = 1')
    conn.commit()
    cursor_fwq.close()
    cursor_guild.close()
    cursor_info.close()
    conn.close()
    return count_download


def save_db_json_file(i, sql_info, sql_select, sql_err, cursor_info, conn_in, hp = None):
    task_id = i[0]
    rs = i[1]
    url = i[2]

    if len(rs) < 100:
        try:
            err_code = -21L
            if rs == str(HTTP_ERROR_PAGE_NOT_FOUND) : err_code = -HTTP_ERROR_PAGE_NOT_FOUND
            if rs == str(HTTP_ERROR_REQUEST_TIME_OUT) :  err_code = -HTTP_ERROR_REQUEST_TIME_OUT
            if rs == str(HTTP_ERROR_SERVER_ERROR): err_code = -HTTP_ERROR_SERVER_ERROR
            if rs == str(HTTP_ERROR_SERVER_UNAVAIABLE): err_code = -HTTP_ERROR_SERVER_UNAVAIABLE
            if rs == str(HTTP_ERROR_TASSK_INFO): err_code = -HTTP_ERROR_TASSK_INFO
            cursor_info.execute(sql_err % (0, err_code, task_id, task_id) )
            conn_in.commit()
        except Exception, ex:
            print '\n' + str(task_id) + ' ERROR SQL ERR -> ',
            print Exception, ':', ex
        return False

    try:
        j = json.loads(rs)
    except Exception, ex:
        print '\n' + str(task_id) + ' ERROR JSON -> ',
        print Exception, ':', ex
        return False

    try:
        pet_crc32 = binascii.crc32( str(j['pets']) )
        account_id = task_id

        if cursor_info.execute(sql_select, pet_crc32) > 0 :
            row_id = cursor_info.fetchone()
            if task_id != row_id[0] and j['achievementPoints'] == row_id[1]:
                account_id = row_id[0]
        info_temp = (j['level'], j['achievementPoints'], pet_crc32,
                        j['pets']['numCollected'], j['lastModified'], account_id, task_id)
        if info_temp:
            cursor_info.execute(sql_info, info_temp)
            conn_in.commit()
            return account_id
    except Exception, ex:
        print '\n' + str(task_id) + ' ERROR SQL IN -> ',
        print Exception, ':', ex
        return False


def main():
    main_start = datetime.datetime.now()

    hp = HttpPool(threads_count=30, doing_count=20, fail_op=base_fail_op, log=base_log)
    ##enable_global_proxy(proxy_http="http", proxy_url="http://127.0.0.1:8087",enable_proxy = True)

    main_count = down_guild_player_fwq_str(hp)

    print '\n',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S  '),str(main_count),' items OVER!'
    main_end = datetime.datetime.now()
    print '\nUSE Time : ',str(main_end - main_start)

if __name__ == '__main__':
    main()


