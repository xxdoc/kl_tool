#!/usr/bin/python
# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------------
# Name:       down_guild_ah
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
import re

# my download http
import inc_download


def down_guild_ah(hp=None):
    if not hp:
        inc_download.log_with_info('no http pool')
        return -1

    inc_download.log_with_time('SET Read ing... ')
    # print base_cfg
    bfj = json.loads(inc_download.base_cfg)
    si = bfj['MySQL_set']

    inc_download.log_with_time('DB Link ing... ')
    conn = MySQLdb.connect(host=si['host'], user=si['user'],
                           passwd=si['passwd'], db=si['item_db'], port=si['port'],
                           charset=si['charset'])
    cursor_fwq = conn.cursor()
    cursor_guild = conn.cursor()
    cursor_info = conn.cursor()
    cursor_info.execute('set names "utf8"')
    cursor_info.execute('SET GLOBAL innodb_flush_log_at_trx_commit = 0')
    cursor_info.execute('SET UNIQUE_CHECKS = 0')
    conn.commit()

    ah_guild_url = r'http://www.battlenet.com.cn/api/wow/character/%s/%s?fields=guild'

    inc_download.log_with_time('DATE download ing... ')

    sql_fwq = 'select slug,zname,fwqID,real_slug from ' + si['db'] + '.' + si['fwq_all_info'] + ' where fwqID>=0 and fwqID<=936 order by fwqID asc'
    cursor_fwq.execute(sql_fwq)
    count_download = 0L

    while True:
        row_fwq = cursor_fwq.fetchone()
        if row_fwq == None:
            break

        fwq_id = row_fwq[2]
        fwq_zname = row_fwq[1]
        fwq_slug = row_fwq[0].replace('-','_')
        real_slug = row_fwq[3].replace('-','_')

        if real_slug=='':
            continue

        sql_check = 'select table_name from information_schema.tables where table_name = "' + real_slug + '" and table_schema="' + si['db'] + '"'
        if cursor_info.execute(sql_check) == 0:
            inc_download.log_with_time('%s (fwqID:%s %s) ->  no Table ... ' % (fwq_zname, fwq_id, real_slug), new_line = True)
            continue

        inc_download.log_with_time('%s (fwqID:%s %s) ->  download ing... ' % (fwq_zname, fwq_id, fwq_slug), new_line = True)

        sql_error = 'update ' + si['db'] + '.' + real_slug  + ' set rand=%s  where auc="%s"'
        sql_info = 'replace into ' + si['wow_guild_list'] + " (name,total,area,group_str,realm,faction) values ('%s','%s','%s','%s','%s','%s')"
        sql_update = 'replace into ' + fwq_slug  + " (name,class,race,gender,level,rank,guild_id,achievementPoints) values ('%s','%s','%s','%s','%s','%s','%s','%s')"
        sql_select = 'select id from ' + si['wow_guild_list'] + ' where name = "%s" and realm = "%s" limit 1 '

        dict_sql = {}
        dict_sql['sql_error'],dict_sql['sql_info'],dict_sql['sql_update'],dict_sql['sql_select'] = sql_error, sql_info, sql_update, sql_select

        sql_fwq_guild = 'select name,id from ' + si['wow_guild_list'] + ' where realm = "%s" order by id' % (fwq_zname)
        cursor_info.execute(sql_fwq_guild)
        dict_in = {}
        for row in cursor_info.fetchall():
            dict_in.setdefault(row[0], row[1])

        sql_temp = 'select name,id from ' + fwq_slug
        cursor_info.execute(sql_temp)
        dict_player = {}
        for row in cursor_info.fetchall():
            dict_player.setdefault(row[0], row[1])

        sql_guild = 'select owner,min_auc from (select owner,min(auc) as min_auc,rand from ' + si['db'] + '.' + real_slug + ' where ownerRealm="'+fwq_zname+'" group by owner order by min_auc) as m where rand<=0 '
        cursor_guild.execute(sql_guild)
        count_guild_add = 0L
        while True:
            row_guild = cursor_guild.fetchone()
            if row_guild == None:
                break

            owner_name = row_guild[0]
            owner_auc = row_guild[1]

            if owner_name in dict_player:
                continue;

            count_download = count_download + 1
            url = ah_guild_url % ( fwq_zname.encode('utf-8'), owner_name.encode('utf-8') )
            url = url.replace(' ','%20')
            task_id = owner_auc

            #print task_id,url.decode('utf-8').encode('gbk')
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
                        tr_count = save_guild_ah(i, cursor_info, conn, hp)
                        if tr_count >= 0:
                            count_guild_add = count_guild_add + tr_count
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
                    tr_count = save_guild_ah(i, cursor_info, conn, hp)
                    if tr_count >= 0 :
                        count_guild_add = count_guild_add + tr_count
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


def save_guild_ah(task_info, cursor_in, conn_in, hp):
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
            cursor_in.execute( dict_sql['sql_error'] % (1, task_id) )
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

    tr_count = 0L
    guild_dict = j.get('guild')
    if guild_dict:
        try:
            guild_name = guild_dict['name']
            guild_realm = guild_dict['realm']
            guild_id = dict_in.get(guild_name)
            if not guild_id:
                sql_tupe = (guild_name, guild_dict['members'],'CN',guild_dict['battlegroup'], guild_realm,4)
                cursor_in.execute( dict_sql['sql_info']  % sql_tupe )
##                cursor_in.execute( dict_sql['sql_select'] % (guild_name, guild_realm) )
##                guild_row = cursor_in.fetchone()
##                guild_id = guild_row[0]
                guild_id = 0
                sql_tupe = (j['name'],j['class'],j['race'],j['gender'],j['level'],255,guild_id,j['achievementPoints'])
                cursor_in.execute( dict_sql['sql_update']  % sql_tupe )
                conn_in.commit()
                dict_in.setdefault(guild_name, 1)
                tr_count = tr_count + 1
                #print guild_name,'--',guild_realm,'(new) ',
            else:
                sql_tupe = (j['name'],j['class'],j['race'],j['gender'],j['level'],255,guild_id,j['achievementPoints'])
                cursor_in.execute( dict_sql['sql_update']  % sql_tupe  )
                conn_in.commit()
                #print guild_name,'--',guild_realm,'(old) ',
                pass;
            return tr_count
        except Exception,ex:
            print '\n' + str(task_id) + ' ERROR SQL -> ',
            print Exception,':',ex
            err_code = -31L
            return err_code

    else:
        cursor_in.execute( dict_sql['sql_error'] % (2, task_id) )
        conn_in.commit()
        err_code = -41L
        return err_code


def main():
    main_start = datetime.datetime.now()

    hp = inc_download.HttpPool(60, 30, inc_download.base_fail_op, inc_download.base_log)
    #inc_download.enable_global_proxy(proxy_http="http", proxy_url="http://127.0.0.1:8087",enable_proxy = True)

    main_count = down_guild_ah(hp)

    print '\n', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S  '), str(main_count), ' items OVER!'
    main_end = datetime.datetime.now()
    print '\nUSE Time : ', str(main_end - main_start)


if __name__ == '__main__':
    main()


