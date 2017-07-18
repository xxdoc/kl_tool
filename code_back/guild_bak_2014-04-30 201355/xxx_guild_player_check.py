#!/usr/bin/python
# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------------
# Name:        sql_guild_player_check
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


# my download http
import inc_download


def sql_guild_player_check():

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


    inc_download.log_with_time('DATE check ing... ')

    sql_fwq = 'select slug,zname,fwqID,catinfo,real_slug from ' + si['db'] + '.' + si['fwq_all_info'] + ' where fwqID>=0 order by fwqID'
    cursor_fwq.execute(sql_fwq)
    count_download = 0L
    while True:
        row_fwq = cursor_fwq.fetchone()
        if row_fwq == None:
            break;

        fwq_id = row_fwq[2]
        fwq_zname = row_fwq[1]
        old_slug = row_fwq[0]
        fwq_slug = row_fwq[0].replace('-','_')
        fwq_catinfo = row_fwq[3]
        real_slug = row_fwq[4]
        get_slug = row_fwq[4].replace('-','_')

##        for i in range(0,10):
##            sql_count = 'select count(*) from ( select max(id) from %s where level>=%s and level<%s  group by name) as m' % (fwq_slug,i*10,i*10+10)
##            cursor_info.execute(sql_count )
##            row_count_check = cursor_info.fetchone()
##            check_count = row_count_check[0]
##
##            fwq_data = (si['db'], si['fwq_all_info'], i*10, check_count, fwq_id)
##            sql_fwq_update = 'update %s.%s set player_%s=%s where fwqID=%s'
##            cursor_info.execute(sql_fwq_update % fwq_data )
##
##        conn.commit()
##        continue;

        sql_check = 'select table_name from information_schema.tables where table_name = "' + fwq_slug + '" and table_schema="' + si['item_db'] + '"'
        if cursor_info.execute(sql_check) == 0:
            inc_download.log_with_time('%s (fwqID:%s %s) ->(no table) no items ... ' % (fwq_zname, fwq_id, fwq_slug), new_line = True)
            continue;

        row_count = []
        row_count_check = []

        sql_count = 'select count( id ) from ' + fwq_slug
        cursor_info.execute(sql_count )
        row_count = cursor_info.fetchone()
        all_count = row_count[0]

        if all_count <= 0:
            inc_download.log_with_time('%s (fwqID:%s %s) ->  empty table:%s... ' % (fwq_zname, fwq_id, fwq_slug, all_count), new_line = True)
            continue;

        inc_download.log_with_time('%s (fwqID:%s %s) ->  exists items:%s... ' % (fwq_zname, fwq_id, fwq_slug, all_count), new_line = True)
        # get all_count

        sql_count = 'select count(*) from ( select max(id) from %s group by name) as m' % (fwq_slug)
        cursor_info.execute(sql_count )
        row_count_check = cursor_info.fetchone()
        check_count = row_count_check[0]

        inc_download.log_with_time('%s (fwqID:%s %s) ->  check  items:%s... ' % (fwq_zname, fwq_id, fwq_slug, check_count))
        # get check_count

        sql_count = 'select count(*) from (select max(id) from %s group by account_id) as m' % (fwq_slug)
        cursor_info.execute(sql_count )
        row_count_account = cursor_info.fetchone()
        account_count = row_count_account[0]

        inc_download.log_with_time('%s (fwqID:%s %s) ->  account items:%s... ' % (fwq_zname, fwq_id, fwq_slug, account_count))
        # get account_count

        if all_count != check_count:
            inc_download.log_with_time('Error -> player have error items ... ')

##            sql_pre_tmp = 'TRUNCATE TABLE  IF EXISTS aaa_del_id_tmp'
##            sql_creat_tmp = 'CREATE TABLE aaa_del_id_tmp ( SELECT max(id) as id from ' + fwq_slug + ' group by name)'
##            sql_delete_tmp = 'DELETE FROM ' + fwq_slug + ' where  id not in (SELECT id from aaa_del_id_tmp)'
##            sql_drop_tmp = 'TRUNCATE TABLE aaa_del_id_tmp'
##
##            cursor_info.execute(sql_pre_tmp)
##            conn.commit()
##            cursor_info.execute(sql_creat_tmp )
##            conn.commit()
##            cursor_info.execute(sql_delete_tmp )
##            cursor_info.execute(sql_drop_tmp)
##            conn.commit()
        #guild_list  check
        sql_count = 'select count( id ) from ' + si['wow_guild_list'] + ' where realm="%s" '
        cursor_info.execute(sql_count % (fwq_zname) )
        row_count = cursor_info.fetchone()
        guild_count = row_count[0]

        inc_download.log_with_time('%s (fwqID:%s %s) ->  guild items:%s... ' % (fwq_zname, fwq_id, fwq_slug, guild_count))
        # get guild_list count

        sql_count = 'select count( * ) from ( select max(id) from ' + si['wow_guild_list'] + ' where realm="%s" group by name) as m'
        cursor_info.execute(sql_count % (fwq_zname) )
        row_count_check = cursor_info.fetchone()
        guild_count_check = row_count_check[0]

        inc_download.log_with_time('%s (fwqID:%s %s) ->  guild check items:%s... ' % (fwq_zname, fwq_id, fwq_slug, guild_count_check))

        fwq_data = (si['db'], si['fwq_all_info'], guild_count_check, check_count, account_count, fwq_id)
        sql_fwq_update = 'update %s.%s set guild_count=%s,player_count=%s,account_count=%s where fwqID=%s'
        cursor_info.execute(sql_fwq_update % fwq_data )
        conn.commit()

        if guild_count != guild_count_check and guild_count_check > 0:
            inc_download.log_with_time('Error -> guild have error items ... ')
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

    main_count = sql_guild_player_check()

    print '\n',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S  '),str(main_count),' items OVER!'
    main_end = datetime.datetime.now()
    print '\nUSE Time : ',str(main_end - main_start)

if __name__ == '__main__':
    main()


