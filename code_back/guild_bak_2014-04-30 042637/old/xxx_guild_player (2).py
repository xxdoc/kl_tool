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

from Queue import Queue, Empty, Full

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

    cursor = conn.cursor()
    cursor_str = conn.cursor()

    setsql = 'set names "utf8"'
    cursor.execute(setsql)

    api_item_url = r'http://www.battlenet.com.cn/api/wow/item/'
    main_url = r'http://www.battlenet.com.cn/api/wow/realm/status'

    player_url = \
        r'http://www.battlenet.com.cn/api/wow/guild/%s/%s?fields=members'

    print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S '), \
        'DATE Update ing... '
    print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S '), \
        'JSON load ing... '

    cursor_str.execute('select id,name,realm from '
                       + si['wow_guild_list']
                       + ' where id>4433 and id<=4569 order by id')

    sql1 = 'replace into ' + si['wow_guild_player'] \
        + " (name,class,race,gender,level,rank,guild_id,achievementPoints) values (%s,'%s','%s','%s','%s','%s','%s','%s')"

    count = 0
    while 1:
        row = cursor_str.fetchone()
        if row == None:
            break

        rs = ''
        c = 0L
        while len(rs.strip()) == 0 and c < 10:
            try:
                rs = player_url % (row[2].encode('utf-8'), row[1].encode('utf-8'))
                re = urllib2.Request(rs)
                rs = urllib2.urlopen(re).read()
                print '|',
            except:
                c = c + 1
                print '.',
                continue

        if len(rs) < 100:
            continue
        try:
            j = json.loads(rs)
        except Exception, ex:
            print row[1] + ' ERROR JSON -> ',
            print Exception, ':', ex
            continue

        info_temp = []
        for i in j['members']:
            tuple_temp = (
                i['character']['name'],
                i['character']['class'],
                i['character']['race'],
                i['character']['gender'],
                i['character']['level'],
                i['rank'],
                row[0],
                i['character']['achievementPoints']
                )
            info_temp.append(tuple_temp)

            # sql_cmd = sql1 % tuple_temp
            # cursor.execute(sql_cmd)

        cursor.executemany(sql1, info_temp)
        conn.commit()
        count = count + 1

        try:
            print row[1] + '(' + row[2] + ')',
        except Exception, ex:
            print Exception, ':', ex
            continue

    # now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.close()
    cursor_str.close()
    conn.close()
    return count


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


