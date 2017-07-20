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
                                "wow_guild_tmp": "aaa_guild_tmp",
                                "wow_guild_player": "aaa_guild_player"
                            },
                            "log_set": {
                                "filename": "db_log.txt",
                                "level": 20,
                                "filemode": "a",
                                "format": "%(asctime)s - %(levelname)s: %(message)s"
                            }
                        }"""

def log_with_time(str_log, new_line = None):
    if new_line:
        print '\n' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S  ') + str_log
    else:
        print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S  ') + str_log

def log_with_info(str_log, new_line = None, enter = None):
    str_temp = (str_log) if (not new_line) else ('\n' + str_log)
    if enter:
        print str_temp
    else:
        print str_temp,

def down_guild_str():

    log_with_time('SET Read ing... ')
    # print base_cfg
    bfj = json.loads(base_cfg)
    si = bfj['MySQL_set']

    log_with_time('DB Link ing... ')
    conn = MySQLdb.connect(host=si['host'], user=si['user'],
                           passwd=si['passwd'], db=si['item_db'],
                           charset=si['charset'])
    cursor_fwq = conn.cursor()
    cursor_guild = conn.cursor()
    cursor_info = conn.cursor()
    cursor_info.execute('set names "utf8"')
    player_url = r'http://www.battlenet.com.cn/api/wow/guild/%s/%s?fields=members'

    print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S '), 'DATE download ing... '

    sql_fwq = 'select slug,zname from ' + si['db'] + '.' + si['fwq_all_info'] + ' where fwqID>=262 and fwqID<=282 and guild_count>0 order by fwqID'
    cursor_fwq.execute(sql_fwq)
    count_download = 0L
    while True:
        row_fwq = cursor_fwq.fetchone()
        if row_fwq == None:
            break
        fwq_slug = row_fwq[0].replace('-','_')

        sql_check = 'select table_name from information_schema.tables where table_name = "' + fwq_slug + '" and table_schema="' + si['item_db'] + '"'
        if cursor_info.execute(sql_check) == 0:
            log_with_time(fwq_slug + ' CREATE Table ... ', new_line = True)
            sql_creat = 'create table if not exists ' + fwq_slug  + ' like ' + si['wow_guild_tmp']
            cursor_info.execute(sql_creat)
            conn.commit()
        else:
            sql_count = 'select count(*) as total from ' + fwq_slug + ' limit 1'
            cursor_info.execute(sql_count)
            row_count = cursor_info.fetchone()
            log_with_time(fwq_slug + '(' + str(row_count[0]) + ') exists Table ... ', new_line = True)
            if row_count[0] > 0:
                continue;

        sql_info = 'replace into ' + fwq_slug  + " (name,class,race,gender,level,rank,guild_id,achievementPoints) values (%s,'%s','%s','%s','%s','%s','%s','%s')"

        sql_guild = 'select id,name,realm from ' + si['wow_guild_list'] + ' where realm="'+row_fwq[1]+'" and id>=49860 and id<=54034 order by id'
        cursor_guild.execute(sql_guild)
        count_do = 0L
        while True:
            row_guild = cursor_guild.fetchone()
            if row_guild == None:
                break
            if not os.path.exists('.\\50000\\'+str(row_guild[0]) + '.json'):
                continue

            count_download = count_download + 1
            save_db_json_read(row_guild[0], sql_info, cursor_info, conn)
            log_with_info(str(row_guild[0])+'(read)')

    cursor_fwq.close()
    cursor_guild.close()
    cursor_info.close()
    conn.close()
    return count_download


def save_db_json_read(guild_id, sql_in, cursor_in, conn_in):
    json_str = ''
    file_str = '.\\50000\\'+str(guild_id) + '.json'
    if not os.path.exists(file_str):
        return
    try:
        fileHandle = open(file_str, 'rb')
        json_str = fileHandle.read()
    finally:
        try:
            fileHandle.close()
        except Exception, ex:
            print Exception, ':', ex

    if len(json_str) < 100:
        return

    try:
        j = json.loads(json_str)
    except Exception, ex:
        print str(guild_id) + ' ERROR JSON -> ',
        print Exception, ':', ex
        return

    try:
        info_temp = []
        for i in j['members']:
            tuple_temp = (
                i['character']['name'],
                i['character']['class'],
                i['character']['race'],
                i['character']['gender'],
                i['character']['level'],
                i['rank'],
                guild_id,
                i['character']['achievementPoints']
                )
            info_temp.append(tuple_temp)
        cursor_in.executemany(sql_in, info_temp)
        conn_in.commit()
    except Exception, ex:
        print str(guild_id) + ' ERROR SQL -> ',
        print Exception, ':', ex
        return


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


