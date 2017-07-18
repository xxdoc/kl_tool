#!/usr/bin/python
# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------------
# Name:        down_guild_sina
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
from BeautifulSoup import BeautifulSoup
import re

# my download http
import inc_download


def down_guild_sina(hp):
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

    sina_url = r'http://armory.games.sina.com.cn/GuildList.aspx?action=ajaxload&area=CN&realm=%s&faction=%s&playersmin=%s&playersmax=%s'

    inc_download.log_with_time('DATE download ing... ')

    sql_error = ''
    sql_info = 'replace into ' + si['wow_guild_list'] + " (name,total,area,group_str,realm,faction) values ('%s','%s','%s','%s','%s','%s')"
    sql_update = ''
    sql_select = ''

    dict_sql = {}
    dict_sql['sql_error'],dict_sql['sql_info'],dict_sql['sql_update'],dict_sql['sql_select'] = sql_error, sql_info, sql_update, sql_select

    sql_fwq = 'select slug,zname,fwqID from ' + si['db'] + '.' + si['fwq_all_info'] + ' where fwqID>=38 and fwqID<=822 order by fwqID asc'
    cursor_fwq.execute(sql_fwq)
    count_download = 0L
    count_guild_add = 0L
    while True:
        row_fwq = cursor_fwq.fetchone()
        if row_fwq == None:
            break

        fwq_id = row_fwq[2]
        fwq_zname = row_fwq[1]
        fwq_slug = row_fwq[0].replace('-','_')

        sql_fwq_guild = 'select name,id from ' + si['wow_guild_list'] + ' where realm = "%s" order by id' % (fwq_zname)
        cursor_guild.execute(sql_fwq_guild)

        dict_in = {}
        for row in cursor_guild.fetchall():
            dict_in.setdefault(row[0], row[1])

        inc_download.log_with_time('%s (fwqID:%s %s) ->  download ing... ' % (fwq_zname, fwq_id, fwq_slug), new_line = True)

        count_download = count_download + 1
        for faction in ['a','h']:
            for playersmin in range(0,13):
                if playersmin <= 4:     # 0-4  5  0-8:2 to 1-9:2  1
                    playersmin_str = str(playersmin*2)
                    playersmax_str = str(playersmin*2 + 1)
                elif playersmin <= 7:   # 5-7  3  10-70:30 to 39-99:30  29
                    playersmin_str = str( (playersmin - 5)*30 + 10)
                    playersmax_str = str( (playersmin - 5)*30 + 39)
                elif playersmin <= 11:  # 8-11  4  100-400:100 to 199-499:100  99
                    playersmin_str = str( (playersmin - 8)*100 + 100)
                    playersmax_str = str( (playersmin - 8)*100 + 199)
                elif playersmin == 12:  # 12  500 to NaN
                    playersmin_str = '500'
                    playersmax_str = ''

                url = sina_url % (row_fwq[1].encode('utf-8'), faction, playersmin_str, playersmax_str )
                url = url.replace(' ','%20')
                task_id = (100 + playersmin) if (faction == 'a') else (200 + playersmin)

                print task_id,url.decode('utf-8').encode('gbk')
                while True:
                    if hp.get_doing_count_now() < hp.get_doing_count_max():
                        if hp.add_task(task_id, url, dict_sql=dict_sql, dict_in=dict_in):
                            #inc_download.log_with_info("%s(add)" % (task_id))
                            break;
                    results = hp.get_results()
                    if not results:
                        time.sleep(1.0 * random.random())
                    else:
                        for i in results:
                            tr_count = save_guild_sina(i, cursor_info, conn, hp)
                            if tr_count >= 0:
                                count_guild_add = count_guild_add + 1
                                inc_download.log_with_info('%s(+%s)' % (i[0], tr_count) )
                            else:
                                inc_download.log_with_info('%s(err:%s)' % (i[0], tr_count) )

    inc_download.log_with_info('%s (fwqID:%s %s) ->  wait to end :%s... ' % (fwq_zname, fwq_id, fwq_slug, count_guild_add), new_line = True)
    count_wait = 0L
    while hp.get_doing_count_now() > 0:
        results = hp.get_results()
        if not results:
            if count_wait > 100 or count_wait > hp.get_doing_count_now()*30:
                hp.set_doing_count_now(0)
                break;
            time.sleep(1.0 * random.random())
            count_wait = count_wait + 1
            inc_download.log_with_info('.')
        else:
            count_wait = 0L
            for i in results:
                tr_count = save_guild_sina(i, cursor_info, conn, hp)
                if tr_count >= 0:
                    count_guild_add = count_guild_add + 1
                    inc_download.log_with_info('%s(+%s)' % (i[0], tr_count) )
                else:
                    inc_download.log_with_info('%s(err:%s)' % (i[0], tr_count) )
    inc_download.log_with_info('%s (fwqID:%s %s) ->  add:%s ' % (fwq_zname, fwq_id, fwq_slug, count_guild_add), new_line = True)

    cursor_info.execute('SET GLOBAL innodb_flush_log_at_trx_commit = 1')
    cursor_info.execute('SET UNIQUE_CHECKS = 1')
    conn.commit()
    cursor_fwq.close()
    cursor_guild.close()
    cursor_info.close()
    conn.close()
    return count_download


def save_guild_sina(task_info, cursor_in, conn_in, hp):
    task_id = task_info[0]
    rs = task_info[1]
    url = task_info[2]
    dict_sql = task_info[3]
    dict_in = task_info[4]

    if len(rs) < 40:
        try:
            err_code = -11L
            if rs == str(inc_download.HTTP_ERROR_PAGE_NOT_FOUND) : err_code = -inc_download.HTTP_ERROR_PAGE_NOT_FOUND
            if rs == str(inc_download.HTTP_ERROR_REQUEST_TIME_OUT) :  err_code = -inc_download.HTTP_ERROR_REQUEST_TIME_OUT
            if rs == str(inc_download.HTTP_ERROR_SERVER_ERROR): err_code = -inc_download.HTTP_ERROR_SERVER_ERROR
            if rs == str(inc_download.HTTP_ERROR_SERVER_UNAVAIABLE): err_code = -inc_download.HTTP_ERROR_SERVER_UNAVAIABLE
            if rs == str(inc_download.HTTP_ERROR_TASSK_INFO): err_code = -inc_download.HTTP_ERROR_TASSK_INFO
            pass
        except Exception, ex:
            print '\n',str(task_id),' ERROR SQL ERR -> ',
            print Exception, ':', ex

        return err_code

    try:
        rs = rs.replace('var guildsdata = ','')
        rs = rs.replace('{count:','{"count":')
        rs = rs.replace(',guilds:',',"guilds":')
        rs = rs.replace(',total:',',"total":')
        rs = rs.replace(',area:',',"area":')
        rs = rs.replace('{name:','{"name":')
        rs = rs.replace(',group:',',"group":')
        rs = rs.replace(',realm:',',"realm":')
        rs = rs.replace(',faction:',',"faction":')
        j = json.loads(rs)
    except Exception,ex:
        print '\n' + str(task_id) + ' ERROR JSON -> ',
        print Exception,':',ex
        err_code = -21L
        return err_code

    tr_count = 0L
    if j['count'] > 0:
        for i in j['guilds']:
            try:
                if i['name'] not in dict_in:
                    cursor_in.execute( dict_sql['sql_info'] % (i['name'],i['total'],i['area'],i['group'],i['realm'],i['faction']) )
                    tr_count = tr_count + 1
                    dict_in.setdefault(tr_name, None)
                    #print i['name'],'(new)',
                else:
                    #print i['name'],'(exist)',
                    pass;
            except Exception,ex:
                print '\n',str(task_id),' ERROR SQL -> ',
                print Exception,':',ex

        conn_in.commit()
        return tr_count
    else:
        err_code = -41L
        return err_code


def main():
    main_start = datetime.datetime.now()

    hp = inc_download.HttpPool(40, 20, inc_download.base_fail_op, inc_download.base_log)
    #inc_download.enable_global_proxy(proxy_http="http", proxy_url="http://127.0.0.1:8087",enable_proxy = True)

    main_count = down_guild_sina(hp)

    print '\n',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S  '),str(main_count),' items OVER!'
    main_end = datetime.datetime.now()
    print '\n','USE Time : ',str(main_end - main_start)
    pass

if __name__ == '__main__':
    main()


