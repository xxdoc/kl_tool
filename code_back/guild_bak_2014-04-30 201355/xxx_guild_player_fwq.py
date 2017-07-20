#!/usr/bin/python
# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------------
# Name:        down_guild_player_fwq
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


# my download http
import inc_download


def down_guild_player_fwq(hp=None):
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

    inc_download.log_with_time('DATE download ing... ')

    sql_fwq = 'select slug,zname,fwqID from ' + si['db'] + '.' + si['fwq_all_info'] + ' where fwqID>=0 and fwqID<=981 order by fwqID'
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
        sql_check = 'select table_name from information_schema.tables where table_name = "' + fwq_slug + '" and table_schema="' + si['item_db'] + '"'
        if cursor_info.execute(sql_check) == 0:
            sql_creat = 'create table if not exists ' + fwq_slug  + ' like ' + si['wow_guild_tmp']
            cursor_info.execute(sql_creat)
            conn.commit()
            inc_download.log_with_time('%s (fwqID:%s %s) ->  CREATE Table ... ' % (fwq_zname, fwq_id, fwq_slug), new_line = True)
        else:
            sql_count = 'select count(*) as total from ' + fwq_slug + ' limit 1'
            cursor_info.execute(sql_count)
            row_count = cursor_info.fetchone()
            count_fwq_slug = row_count[0]
            inc_download.log_with_time('%s (fwqID:%s %s) ->  exists Table:%s ... ' % (fwq_zname, fwq_id, fwq_slug, count_fwq_slug), new_line = True)

##            sql_pre_tmp = 'TRUNCATE TABLE ' + fwq_slug
##            count_fwq_slug = 0L
##            cursor_info.execute(sql_pre_tmp)
##            conn.commit()
##            inc_download.log_with_time(str(row_fwq[2]) + ' -> ' + row_fwq[1] + ' TRUNCATE Table ... ')

        sql_error = ''
        sql_info = 'replace into ' + fwq_slug  + " (name,class,race,gender,level,rank,guild_id,achievementPoints) values (%s,%s,%s,%s,%s,%s,%s,%s)"
        sql_update = 'update ' + si['wow_guild_list']  + ' set total = %s, up_ver = %s  where id = %s'
        sql_select = ''

        dict_sql = {}
        dict_sql['sql_error'],dict_sql['sql_info'],dict_sql['sql_update'],dict_sql['sql_select'] = sql_error, sql_info, sql_update, sql_select

        dict_in = None

        sql_guild = 'select id,name,realm from ' + si['wow_guild_list'] + ' where realm="'+row_fwq[1]+'" and id>=0 and total>=0 and up_ver<3  order by id'
        cursor_guild.execute(sql_guild)
        count_guild_add = 0L
        while True:
            row_guild = cursor_guild.fetchone()
            if row_guild == None:
                break
            if count_fwq_slug > 0:
                sql_temp = 'select id from ' + fwq_slug  + ' where rank<255 and guild_id = ' + str(row_guild[0]) + ' limit 1'
                if cursor_info.execute(sql_temp) > 0:
                    continue;

            count_download = count_download + 1
            url = player_url % (row_guild[2].encode('utf-8'), row_guild[1].encode('utf-8'))
            url = url.replace(' ','%20')
            task_id = row_guild[0]

            #print task_id,url.decode('utf-8').encode('gbk')
            while True:
                if hp.get_doing_count_now() < hp.get_doing_count_max():
                    if hp.add_task(task_id, url, dict_sql=dict_sql, dict_in=dict_in):
                        inc_download.log_with_info("%s(add)" % (task_id))
                        break;
                results = hp.get_results()
                if not results:
                    time.sleep(1.0 * random.random())
                else:
                    for i in results:
                        tr_count = save_guild_player_fwq(i, cursor_info, conn, hp)
                        if tr_count >= 0 :
                            count_guild_add = count_guild_add + 1
                            inc_download.log_with_info('%s(+%s)' % (i[0], tr_count) )
                        else:
                            inc_download.log_with_info('%s(err:%s)' % (i[0], tr_count) )

        inc_download.log_with_info('%s (fwqID:%s %s) ->  wait to end :%s... ' % (fwq_zname, fwq_id, fwq_slug, count_guild_add), new_line = True)
        count_wait = 0L
        while hp.get_doing_count_now() > 0:
            results = hp.get_results()
            if not results:
                if count_wait > 100 or count_wait > hp.get_doing_count_now()*50:
                    hp.set_doing_count_now(0)
                    break;
                time.sleep(1.0 * random.random())
                count_wait = count_wait + 1
                inc_download.log_with_info('.')
            else:
                count_wait = 0L
                for i in results:
                    tr_count = save_guild_player_fwq(i, cursor_info, conn, hp)
                    if tr_count >= 0 :
                        count_guild_add = count_guild_add + 1
                        inc_download.log_with_info('%s(+%s)' % (i[0], tr_count) )
                    else:
                        inc_download.log_with_info('%s(err:%s)' % (i[0], tr_count) )
        inc_download.log_with_info('%s (fwqID:%s %s) ->  add:%s \n' % (fwq_zname, fwq_id, fwq_slug, count_guild_add), new_line = True)

    cursor_info.execute('SET GLOBAL innodb_flush_log_at_trx_commit = 1')
    cursor_info.execute('SET UNIQUE_CHECKS = 1')
    conn.commit()
    cursor_fwq.close()
    cursor_guild.close()
    cursor_info.close()
    conn.close()
    return count_download


def save_guild_player_fwq(task_info, cursor_in, conn_in, hp):
    task_id = task_info[0]
    rs = task_info[1]
    url = task_info[2]
    dict_sql = task_info[3]
    dict_in = task_info[4]

##    try:
##        url_print = url.decode('utf-8').encode('gbk')
##    except Exception, e:
##        url_print = str(task_id) + ' (canot encode)'

    if len(rs) < 100:
        try:
            err_code = -11L
            if rs == str(inc_download.HTTP_ERROR_PAGE_NOT_FOUND) : err_code = -inc_download.HTTP_ERROR_PAGE_NOT_FOUND
            if rs == str(inc_download.HTTP_ERROR_REQUEST_TIME_OUT) :  err_code = -inc_download.HTTP_ERROR_REQUEST_TIME_OUT
            if rs == str(inc_download.HTTP_ERROR_SERVER_ERROR): err_code = -inc_download.HTTP_ERROR_SERVER_ERROR
            if rs == str(inc_download.HTTP_ERROR_SERVER_UNAVAIABLE): err_code = -inc_download.HTTP_ERROR_SERVER_UNAVAIABLE
            if rs == str(inc_download.HTTP_ERROR_TASSK_INFO): err_code = -inc_download.HTTP_ERROR_TASSK_INFO
            cursor_in.execute( dict_sql['sql_update'] % (err_code, -1, task_id) )
            conn_in.commit()
        except Exception, ex:
            print '\n',str(task_id),' ERROR SQL ERR -> ',
            print Exception, ':', ex

        return err_code

    try:
        j = json.loads(rs)
    except Exception, ex:
        print '\n',str(task_id),' ERROR JSON -> ',
        print Exception, ':', ex
        err_code = -21L

        return err_code

    try:
        info_temp = []
        tuple_temp = ()
        for i in j['members']:
            tuple_temp = (
                i['character']['name'],
                i['character']['class'],
                i['character']['race'],
                i['character']['gender'],
                i['character']['level'],
                i['rank'],
                task_id,
                i['character']['achievementPoints']
                )
            info_temp.append(tuple_temp)
        if info_temp:
            cursor_in.execute( dict_sql['sql_update'] % (len(info_temp), 3, task_id) )
            cursor_in.executemany( dict_sql['sql_info'], info_temp)
            conn_in.commit()
            return len(info_temp)
    except Exception, ex:
        print '\n' + str(task_id) + ' ERROR SQL -> ',
        print Exception, ':', ex
        err_code = -31L
        return err_code


def main():
    main_start = datetime.datetime.now()

    hp = inc_download.HttpPool(threads_count=50, doing_count=30, fail_op=inc_download.base_fail_op, log=inc_download.base_log)
    #inc_download.enable_global_proxy(proxy_http="http", proxy_url="http://127.0.0.1:8087",enable_proxy = True)

    main_count = down_guild_player_fwq(hp)

    print '\n',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S  '),str(main_count),' items OVER!'
    main_end = datetime.datetime.now()
    print '\nUSE Time : ',str(main_end - main_start)

if __name__ == '__main__':
    main()


