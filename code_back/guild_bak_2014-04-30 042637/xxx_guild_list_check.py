#!/usr/bin/python
# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------------
# Name:        sql_guild_list_check
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
import time
import random
# BeautifulSoup for HTML

# my download http
import inc_download


def sql_guild_list_check():

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

    inc_download.log_with_time('DATE download ing... ')
    hp = inc_download.HttpPool(30,20 , inc_download.base_fail_op, inc_download.base_log)

    sql_fwq = 'select slug,zname,fwqID from ' + si['db'] + '.' + si['fwq_all_info'] + ' where fwqID>=0 order by fwqID'
    cursor_fwq.execute(sql_fwq)
    count_download = 0L
    while True:
        row_fwq = cursor_fwq.fetchone()
        if row_fwq == None:
            break;

        row_count = []
        row_count_check = []

        sql_count = 'select count( id ) from ' + si['wow_guild_list'] + ' where realm="%s" limit 1'
        cursor_info.execute(sql_count % (row_fwq[1]) )
        row_count = cursor_info.fetchone()
        inc_download.log_with_time(str(row_fwq[2]) + ' -> ' + row_fwq[1] + '(' + str(row_count[0]) + ') exists items ... ', new_line = True)

        if row_count[0] <= 0:
             continue;

        sql_count = 'select count( * ) from ( select max(id) from ' + si['wow_guild_list'] + ' where realm="%s" group by name) as m'
        cursor_info.execute(sql_count % (row_fwq[1]) )
        row_count_check = cursor_info.fetchone()
        inc_download.log_with_time(str(row_fwq[2]) + ' -> ' + row_fwq[1] + '(' + str(row_count_check[0]) + ') check exists items ... ')

        if row_count[0] != row_count_check[0]:
            inc_download.log_with_time('Error -> ' + row_fwq[1] + 'have error items ... ')
            count_download = count_download + 1

            sql_pre_tmp = 'DROP TABLE  IF EXISTS aaa_del_id_tmp'
            sql_creat_tmp = 'CREATE TABLE aaa_del_id_tmp ( SELECT max(id) as id from ' + si['wow_guild_list'] + ' where realm="%s" group by name)'
            sql_delete_tmp = 'DELETE FROM ' + si['wow_guild_list'] + ' where  realm="%s" and id not in (SELECT id from aaa_del_id_tmp)'
            sql_drop_tmp = 'TRUNCATE TABLE aaa_del_id_tmp'

            cursor_info.execute(sql_pre_tmp)
            conn.commit()
            cursor_info.execute(sql_creat_tmp % (row_fwq[1]) )
            conn.commit()
            cursor_info.execute(sql_delete_tmp % (row_fwq[1]) )
            cursor_info.execute(sql_drop_tmp)
            conn.commit()


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

    main_count = sql_guild_list_check()

    print '\n',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S  '),str(main_count),' items OVER!'
    main_end = datetime.datetime.now()
    print '\nUSE Time : ',str(main_end - main_start)

if __name__ == '__main__':
    main()


