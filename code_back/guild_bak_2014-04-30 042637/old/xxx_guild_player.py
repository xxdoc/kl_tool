#!/usr/bin/python
# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------------
# Name:        1
# Purpose:
#
# Author:      Administrator
#
# Created:     20/03/2014
# Copyright:   (c) Administrator 2014
# Licence:     <your licence>
# -------------------------------------------------------------------------------

import sys
import MySQLdb
import json
import os
import datetime
import urllib2

import thread
import time
import random
from Queue import Queue, Empty, Full


def base_log(msg):
    print msg


def base_fail_op(task, status, log):
    log('fail op. task = %s, status = %d' % (str(task), status))


def get_remote_data(
    tasks,
    results,
    fail_op=base_fail_op,
    log=base_log,
    ):

    while True:
        task = tasks.get()
        err_str = ''

        if err_str == '':
            try:
                tid = task['id']
                url = task['url']
            except KeyError:
                log(str(e))
                err_str = 'error task info !'
                #log('thread_%s doing task %d' % (thread.get_ident(), tid))

        if err_str == '':
            rs = ''
            count_error = 0L
            while len(rs.strip()) == 0 and count_error < 10:
                try:
                    re = urllib2.Request(url)
                    rs = urllib2.urlopen(re).read()
                except:
                    count_error = count_error + 1
                    continue

        if err_str == '':
            if len(rs.strip()) == 0:
                log('request failed. tid = %s, url = %s' % (tid, url))
                fail_op(task, -1, log)
                err_str = 'error network download !'

        rs = rs if (err_str == '')  else err_str
        results.put((tid, rs), True)


class HttpPool(object):

    def __init__(
        self,
        threads_count,
        fail_op,
        log,
        ):

        self._tasks = Queue()
        self._results = Queue()

        for i in xrange(threads_count):
            thread.start_new_thread(get_remote_data, (self._tasks,
                                    self._results, fail_op, log))

    def add_task(self, tid, url):

        task = {'id': tid, 'url': url}
        try:
            self._tasks.put_nowait(task)
        except Full:
            return False

        return True

    def get_results(self):
        results = []
        while True:
            try:
                res = self._results.get_nowait()
            except Empty:
                break
            results.append(res)
        return results


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
                                "wow_guild_player": "aaa_guild_player"
                            },
                            "log_set": {
                                "filename": "db_log.txt",
                                "level": 20,
                                "filemode": "a",
                                "format": "%(asctime)s - %(levelname)s: %(message)s"
                            }
                        }"""


def down_guild_str():

    # print base_cfg

    start = datetime.datetime.now()
    print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S  ') \
        + 'SET Read ing... '
    bfj = json.loads(base_cfg)
    si = bfj['MySQL_set']
    print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S  ') \
        + 'DB Link ing... '
    conn = MySQLdb.connect(host=si['host'], user=si['user'],
                           passwd=si['passwd'], db=si['item_db'],
                           charset=si['charset'])
    cursor_str = conn.cursor()
    cursor_str.execute('set names "utf8"')
    player_url = r'http://www.battlenet.com.cn/api/wow/guild/%s/%s?fields=members'

    print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S '), 'DATE download ing... '
    cursor_str.execute('select id,name,realm from ' + si['wow_guild_list'] + ' where id>=49860 and id<=54034 order by id')

    hp = HttpPool(50, base_fail_op, base_log)
    count_download = 0L
    count_do = 0L
    while True:
        row = cursor_str.fetchone()
        if row == None:
            break
        if os.path.exists('.\\50000\\'+str(row[0]) + '.json'):
            continue

        count_download = count_download + 1
        url = player_url % (row[2].encode('utf-8'), row[1].encode('utf-8'))
        while True:
            if count_do < 40:
                if hp.add_task(row[0], url):
                    count_do = count_do + 1
                    print str(row[0])+'(add)',
                    break;
            results = hp.get_results()
            if not results:
                time.sleep(1.0 * random.random())
            for i in results:
                count_do = count_do - 1
                if len(i[1]) < 100:
                    continue
                save_json_file(i[1], '.\\50000\\'+str(i[0]) + '.json')
                print str(i[0])+'(get)',

    cursor_str.close()
    conn.close()

    print '\n waite to end-> ',
    count_waite = 0L
    while count_do>0:
        results = hp.get_results()
        if not results:
            if count_waite > 50:
                break;
            time.sleep(1.0 * random.random())
            count_waite = count_waite + 1
            print '.',
            continue;
        count_waite = 0L
        for i in results:
            count_do = count_do - 1
            if len(i[1]) < 100:
                continue
            save_json_file(i[1], '.\\50000\\'+str(i[0]) + '.json')
            print str(i[0])+'(get)',

    return count_download


def save_json_file(str, file):
    if os.path.exists(file):
        return
    try:
        fileHandle = open(file, 'wb')
        fileHandle.write(str)
    finally:
        fileHandle.close()

def main():
    main_start = datetime.datetime.now()

    main_count = down_guild_str()

    print '\n' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S  '
            ) + str(main_count) + ' items OVER!'
    main_end = datetime.datetime.now()
    print '\nUSE Time : ' + str(main_end - main_start)
    pass


if __name__ == '__main__':
    main()


