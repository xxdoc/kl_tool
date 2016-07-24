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
# BeautifulSoup for HTML
from BeautifulSoup import BeautifulSoup
import re

# my download http
import inc_download


def down_guild_player_fwq_str():

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
    hp = inc_download.HttpPool(30,20 , inc_download.base_fail_op, inc_download.base_log)

    sql_fwq = 'select slug,zname,fwqID from ' + si['db'] + '.' + si['fwq_all_info'] + ' where fwqID>=0 order by fwqID'
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

        count_fwq_slug = 0L
        sql_check = 'select table_name from information_schema.tables where table_name = "' + fwq_slug + '" and table_schema="' + si['item_db'] + '"'
        if cursor_info.execute(sql_check) == 0:
            sql_creat = 'create table if not exists ' + fwq_slug  + ' like ' + si['wow_guild_tmp']
            cursor_info.execute(sql_creat)
            conn.commit()
            inc_download.log_with_time(str(row_fwq[2]) + ' -> ' + row_fwq[1] + ' CREATE Table ... ', new_line = True)
        else:
            sql_count = 'select count(*) as total from ' + fwq_slug + ' limit 1'
            cursor_info.execute(sql_count)
            row_count = cursor_info.fetchone()
            count_fwq_slug = row_count[0]
            inc_download.log_with_time(str(row_fwq[2]) + ' -> ' + row_fwq[1] + '(' + str(row_count[0]) + ') exists Table ... ', new_line = True)

            sql_pre_tmp = 'SELECT * FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = '+ si['db'] +' AND TABLE_NAME = ' + fwq_slug + ' AND COLUMN_NAME = pet_md5'
            if cursor_info.execute(sql_pre_tmp) == 0:
                sql_pre_tmp = 'alter table ' + fwq_slug + ' add COLUMN pet_md5 VARCHAR(20) DEFAULT ""'
                cursor_info.execute(sql_pre_tmp)
                sql_pre_tmp = 'alter table ' + fwq_slug + ' add COLUMN numCollected int DEFAULT 0'
                cursor_info.execute(sql_pre_tmp)
                sql_pre_tmp = 'alter table ' + fwq_slug + ' add COLUMN lastModified bigint DEFAULT 0'
                cursor_info.execute(sql_pre_tmp)
                conn.commit()
                inc_download.log_with_time(str(row_fwq[2]) + ' -> ' + row_fwq[1] + 'alter add COLUMN ... ')


        sql_info = "update " + fwq_slug  + " set level=%s,achievementPoints=%s,pet_md5='%s',numCollected=%s,lastModified=%s where id=%s"
        sql_update ="update " + fwq_slug  + " set pet_md5='%s',numCollected=%s where id=%s"

        sql_player = 'select id,name from ' + fwq_slug + ' where id>=0 and pet_md5="" by id'
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
                        inc_download.log_with_info(str(task_id)+'(add)')
                        break;
                results = hp.get_results()
                if not results:
                    time.sleep(1.0 * random.random())
                else:
                    for i in results:
                        get_count = save_db_json_file(i, sql_info, sql_update, cursor_info, conn, hp)
                        if get_count:
                            inc_download.log_with_info(str(i[0])+'(get:' + str(get_count) + ')')
                        else:
                            inc_download.log_with_info(str(i[0])+'(error)')


        inc_download.log_with_info('waite to end-> ', new_line = True)
        count_waite = 0L
        while hp.get_doing_count_now() > 0:
            results = hp.get_results()
            if not results:
                if count_waite > 100 or count_waite > hp.get_doing_count_now()*30:
                    hp.set_doing_count_now(0)
                    break;
                time.sleep(1.0 * random.random())
                count_waite = count_waite + 1
                inc_download.log_with_info('.')
            else:
                count_waite = 0L
                for i in results:
                    get_count = save_db_json_file(i, sql_info, sql_update, cursor_info, conn, hp)
                    if get_count:
                        inc_download.log_with_info(str(i[0])+'(get:' + str(get_count) + ')')
                    else:
                        inc_download.log_with_info(str(i[0])+'(error)')

    cursor_info.execute('SET GLOBAL innodb_flush_log_at_trx_commit = 1')
    cursor_info.execute('SET UNIQUE_CHECKS = 1')
    conn.commit()
    cursor_fwq.close()
    cursor_guild.close()
    cursor_info.close()
    conn.close()
    return count_download


def save_db_json_file(i, sql_in, sql_select, cursor_in, conn_in, hp = None):
    task_id = i[0]
    rs = i[1]
    url = i[2]

    if len(rs) < 100:
        if rs == str(inc_download.HTTP_ERROR_PAGE_NOT_FOUND) or rs == str(inc_download.HTTP_ERROR_REQUEST_TIME_OUT) or rs == str(inc_download.HTTP_ERROR_SERVER_ERROR):
            try:
                cursor_in.execute(sql_select % ('', -1, task_id) )
                conn_in.commit()
            except Exception, ex:
                print '\n' + str(task_id) + ' ERROR DEL -> ',
                print Exception, ':', ex
        return False

    try:
        j = json.loads(rs)
    except Exception, ex:
        print '\n' + str(task_id) + ' ERROR JSON -> ',
        print Exception, ':', ex
        return False

    try:
        pet_md5 = md5(rs)
        info_temp = (j['level'], j['achievementPoints'], pet_md5,
                        j['pet']['numCollected'], j['lastModified'], task_id)
        if info_temp:
            cursor_in.execute(sql_in, info_temp)
            conn_in.commit()
            return len(info_temp)
    except Exception, ex:
        print '\n' + str(task_id) + ' ERROR SQL -> ',
        print Exception, ':', ex
        return False


def main():
    main_start = datetime.datetime.now()

    main_count = down_guild_player_fwq_str()

    print '\n',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S  '),str(main_count),' items OVER!'
    main_end = datetime.datetime.now()
    print '\nUSE Time : ',str(main_end - main_start)

if __name__ == '__main__':
    main()


