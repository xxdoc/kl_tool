# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
#https://pypi.tuna.tsinghua.edu.cn/simple
import os
import json
import urllib2
import time
import re
import datetime

API_URL = 'http://abc.com/api/OpenApi/allSite?key=ii6KqJ4qlkOWPkrMma'
DB_USER = 'hk_wd'
DB_PWD = 'jbiM3gvxwzUjb7iXZPM3g'
DEL_DAYS = 45

DEL_SQL_LIST = '''
DELETE FROM chats WHERE created_at <= "2020-07-18 15:12:51";
DELETE FROM record_onlines WHERE created_at <= "2020-07-18 15:12:51";
DELETE FROM record_user_onlines WHERE created_at <= "2020-07-18 15:12:51";
DELETE FROM record_visits WHERE created_at <= "2020-07-18 15:12:51";
DELETE FROM record_jfs WHERE created_at <= "2020-07-18 15:12:51";
DELETE FROM record_users WHERE created_at <= "2020-07-18 15:12:51";
DELETE FROM record_user_onlines_summary WHERE created_at <= "2020-07-18 15:12:51";
DELETE FROM users WHERE created_at <= "2020-07-18 15:12:51" and type = 100;
DELETE FROM record_pasts WHERE created_at <= "2020-07-18 15:12:51";
DELETE FROM record_onlines_clerk WHERE created_at <= "2020-07-18 15:12:51";
DELETE FROM user_treasures WHERE created_at <= "2020-07-18 15:12:51";
DELETE FROM got_luck_moneys WHERE created_at <= "2020-07-18 15:12:51";
DELETE FROM record_logs WHERE created_at <= "2020-07-18 15:12:51";
DELETE FROM site_op_logs WHERE created_at <= "2020-07-18 15:12:51";
DELETE FROM count_lifetimes_clerk WHERE created_at <= "2020-07-18 15:12:51";
DELETE FROM filted_chats WHERE created_at <= "2020-07-18 15:12:51";
DELETE FROM record_onlines_multi WHERE created_at <= "2020-07-18 15:12:51";
DELETE FROM count_lifetimes WHERE created_at <= "2020-07-18 15:12:51";
'''

def popen(cmd):
    with os.popen(cmd) as ef:
        return rf.read()
        
def cwd(*f):
    return os.path.join(os.getcwd(), *f)

def read_site(url):
    resp = urllib2.urlopen(url)
    if resp.code == 200:
        json_str = resp.read()
        obj = json.loads(json_str)
        return obj.get('data', [])
    else:
        return []

def cmd_site(siteList, days):
    sqlList = [i.strip() for i in DEL_SQL_LIST.split('\n') if i.strip()]
    t_int = int(time.time()) - days * 24 * 3600
    t_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t_int))
    sqlList = [re.sub(r'("(\d+)-(\d+)-(\d+)(\s+)(\d+):(\d+):(\d+)")', '"%s"' % (t_str,), i) for i in sqlList]

    cmdList = []
    for site in siteList:
        site_note = site.get('site_note', '')
        r = re.match(u'JAVA集群(\d+)-', site_note)
        if not r:
            continue

        group = int(r.group(1))
        if group <= 0 or group >= 10:
            continue

        db_host = site.get('db_host', '')
        db_database = site.get('db_database', '')

        cmdList.append(' echo "" ')
        cmdList.append(' echo " db_database => %s" ' % (db_database, ))
        for sql in sqlList:
            cmd = ''' mysql -h {db_host} -u{db_user} -p{db_pwd} {db_database} -e ' {sql} ' '''.format(
                db_host=db_host,
                db_user=DB_USER,
                db_pwd=DB_PWD,
                db_database=db_database,
                sql=sql,
            )
            cmdList.append(cmd)

        cmdList.append(' echo "================" ')
        cmdList.append(' echo "================" ')
    return cmdList

def main():
    # print _T(), ' get url ', API_URL
    siteList = read_site(API_URL)
    # print _T(), ' get siteList:', len(siteList)
    cmdList = cmd_site(siteList, DEL_DAYS)
    # print _T(), ' get cmdList:', len(cmdList)

    for cmd in cmdList:
        print cmd

def _T(tag = 'INFO'):
    time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    return '%s [%s] => ' % (time_str, tag.upper())

if __name__ == '__main__':
    main()
