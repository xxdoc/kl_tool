#!/usr/bin/python
# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------------
# Name:        down_guild_player_fwq_str
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
import urllib
import time
import random
import binascii


# my download http
import inc_download

import subprocess



def down_guild_player_fwq_str(hp = None):
    if not hp:
        inc_download.log_with_info('no http pool')
        return False
    inc_download.log_with_time('SET Read ing... ')
    # print base_cfg
    bfj = json.loads(inc_download.base_cfg)
    si = bfj['MySQL_set']

    inc_download.log_with_time('DB Link ing... ')
    conn = MySQLdb.connect(host=si['host'], user=si['user'],
                           passwd=si['passwd'], db=si['item_db'],
                           charset=si['charset'])
    cursor_fwq = conn.cursor()
    cursor_guild = conn.cursor()
    cursor_info = conn.cursor()
    cursor_info.execute('set names "utf8"')
    cursor_info.execute('SET GLOBAL innodb_flush_log_at_trx_commit = 0')
    cursor_info.execute('SET UNIQUE_CHECKS = 0')
    conn.commit()

    player_url = r'http://www.battlenet.com.cn/api/wow/guild/%s/%s?fields=members'
    pet_url = r'http://www.battlenet.com.cn/api/wow/character/%s/%s?fields=pets'

    inc_download.log_with_time('DATE download ing... ')

    sql_fwq = 'select slug,zname,fwqID,qu from ' + si['db'] + '.' + si['fwq_all_info'] + ' where fwqID>=0 order by fwqID'
    cursor_fwq.execute(sql_fwq)

    count_download = 0L
    url = ''
    task_id = 0L
    get_count = 0L

    while True:
        row_fwq = cursor_fwq.fetchone()
        if row_fwq == None:
            break
        fwq_slug = row_fwq[0].replace('-','_')
        fwq_zname = row_fwq[1]
        fwq_id = row_fwq[2]
        fwq_qu = row_fwq[3]

        count_fwq_slug = 0L
        sql_check = 'select table_name from information_schema.tables where table_name = "' + fwq_slug + '" and table_schema="' + si['item_db'] + '"'
        if cursor_info.execute(sql_check) == 0:
            sql_creat = 'create table if not exists ' + fwq_slug  + ' like ' + si['wow_guild_tmp']
            cursor_info.execute(sql_creat)
            conn.commit()
            inc_download.log_with_time(str(fwq_id) + ' -> ' + fwq_zname + ' CREATE Table ... ', new_line = True)
        else:
            sql_count = 'select count(*) as total from ' + fwq_slug + ' limit 1'
            cursor_info.execute(sql_count)
            row_count = cursor_info.fetchone()
            count_fwq_slug = row_count[0]
            inc_download.log_with_time(str(fwq_id) + ' -> ' + fwq_zname + '(' + str(row_count[0]) + ') exists Table ... ', new_line = True)

            if count_fwq_slug>0:
                file_name = r'H:\wowxxx\webapp\guild\out\%s.(%s).sql'% (fwq_slug, count_fwq_slug)
                sql_pre_tmp = r'D:\PHPweb\local\mysql5\bin\mysqldump -u%s -p%s %s %s > %s'
                sql_pre_tmp = sql_pre_tmp % (si['user'], si['passwd'], si['item_db'], fwq_slug, file_name )
                print sql_pre_tmp
                ##os.system(sql_pre_tmp)

                zfile_name = r'H:\wowxxx\webapp\guild\out\%s.%s.(%s).sql'% (fwq_zname, fwq_slug, count_fwq_slug)
                new_name = r'H:\wowxxx\webapp\guild\out\z%02d.%03d.%s.%s.(%s).sql'% (fwq_qu, fwq_id, fwq_zname, fwq_slug, count_fwq_slug)
                os.rename(zfile_name, new_name)

    cursor_info.execute('SET GLOBAL innodb_flush_log_at_trx_commit = 1')
    cursor_info.execute('SET UNIQUE_CHECKS = 1')
    conn.commit()
    cursor_fwq.close()
    cursor_guild.close()
    cursor_info.close()
    conn.close()
    return count_download



def main():
    main_start = datetime.datetime.now()

    hp = inc_download.HttpPool(threads_count=30, doing_count=20, fail_op=inc_download.base_fail_op, log=inc_download.base_log)
    inc_download.enable_global_proxy(proxy_http="http", proxy_url="http://127.0.0.1:8087",enable_proxy = True)

    main_count = down_guild_player_fwq_str(hp)

    print '\n',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S  '),str(main_count),' items OVER!'
    main_end = datetime.datetime.now()
    print '\nUSE Time : ',str(main_end - main_start)

if __name__ == '__main__':
    main()


