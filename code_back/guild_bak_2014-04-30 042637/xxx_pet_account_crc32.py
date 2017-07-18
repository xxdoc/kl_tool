#!/usr/bin/python
# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------------
# Name:        down_pet_account
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

# BeautifulSoup for HTML

# my download http
import inc_download




def down_pet_account(hp = None):
    if not hp:
        inc_download.log_with_info('no http pool')
        return -1

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

    sql_fwq = 'select slug,zname,fwqID from ' + si['db'] + '.' + si['fwq_all_info'] + ' where fwqID>=1 order by fwqID '
    cursor_fwq.execute(sql_fwq)

    count_download = 0L
    url = ''
    task_id = 0L
    get_count = 0L

    while True:
        row_fwq = cursor_fwq.fetchone()
        if row_fwq == None:
            break

        fwq_id = row_fwq[2]
        fwq_zname = row_fwq[1]
        fwq_slug = row_fwq[0].replace('-','_')

        count_fwq_slug = 0L
        sql_check = 'select table_name from information_schema.tables where table_name = "%s" and table_schema="%s"'
        if cursor_info.execute(sql_check % (fwq_slug, si['item_db'])) == 0:
            inc_download.log_with_time('%s (fwqID:%s %s) ->  no Table ... ' % (fwq_zname, fwq_id, fwq_slug), new_line = True)
            continue
        else:
            sql_count = 'select count(*) as total from %s limit 1'
            cursor_info.execute(sql_count % (fwq_slug) )
            row_count = cursor_info.fetchone()
            count_fwq_slug = row_count[0]
            inc_download.log_with_time('%s (fwqID:%s %s) ->  exists Table:%s ... ' % (fwq_zname, fwq_id, fwq_slug, count_fwq_slug), new_line = True)

        sql_drop = "DROP TABLE  IF EXISTS aaa_del_id_tmp"
        cursor_info.execute(sql_drop)
        sql_creat = "CREATE TABLE aaa_del_id_tmp (select max(id) as id,name,count(name) as cn from %s where numCollected<>-999 group by name having cn>1 order by cn desc)"
        #sql_creat = "CREATE TABLE aaa_del_id_tmp (select min(id) as id,pet_crc32,count(id) as m_cc,count(distinct account_id) as m_da from %s WHERE numCollected>0 and pet_crc32<>0 group by pet_crc32 having m_cc>0 and m_da>1 order by m_da desc )"
        count_fwq_slug = cursor_info.execute(sql_creat % (fwq_slug) )

        inc_download.log_with_time('%s (fwqID:%s %s) ->  error name :%s ... ' % (fwq_zname, fwq_id, fwq_slug, count_fwq_slug))

        sql_update = "update %s set numCollected=-999 where id<>%s and name='%s'"
        sql_player = 'select id,name from aaa_del_id_tmp order by id'
        cursor_guild.execute(sql_player)
        count_guild_add = 0L
        while True:
            row_player = cursor_guild.fetchone()
            if row_player == None:
                break
            sql_tmp = sql_update % (fwq_slug, row_player[0], row_player[1])
            print sql_tmp
            cursor_info.execute(sql_tmp )
            count_download = count_download + 1
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

    hp = inc_download.HttpPool(threads_count=50, doing_count=30, fail_op=inc_download.base_fail_op, log=inc_download.base_log)
    #inc_download.enable_global_proxy(proxy_http="http", proxy_url="http://127.0.0.1:8087",enable_proxy = True)

    main_count = down_pet_account(hp)

    print '\n',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S  '),str(main_count),' items OVER!'
    main_end = datetime.datetime.now()
    print '\nUSE Time : ',str(main_end - main_start)

if __name__ == '__main__':
    main()


