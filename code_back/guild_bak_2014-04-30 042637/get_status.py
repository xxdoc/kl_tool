import sys,MySQLdb,json,os,datetime,urllib2

start = datetime.datetime.now()

print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S  ") + "SET Read ing... "

base_cfg = """{
			    "MySQL_set": {
			        "host": "127.0.0.1",
			        "user": "root",
			        "passwd": "root",
			        "db": "wow_ah_db",
			        "charset": "utf8",
			        "port": 3306,
			        "fwq_all_status": "aa_fwq_status",
			        "fwq_all_tmp": "aaa_fwq_tmp"
			    }
			}"""


def try_get_fwq_status():
    #print base_cfg
    bfj = json.loads(base_cfg)
    si = bfj['MySQL_set']

    print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S  ") + "JSON Download ing... "
    main_url = r'http://www.battlenet.com.cn/api/wow/realm/status'

    res = ''
    c = 0L
    while len(res.strip()) == 0 and c < 10:
        try:
            req = urllib2.Request(main_url)
            res = urllib2.urlopen(req).read()
        except Exception, ex:
            c = c + 1
            print '.',

    if res.strip() == 0 :
        print 'network error!!'
        return False

    print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S  ") + "JSON Download " + str(len(res)) + ' byte'

    try:
        sfj = json.loads(res)
    except Exception, ex:
        print Exception, ':', ex
        print 'JSON str error!!'
        return False

    print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S  ") + "DB Link ing... "

    conn = MySQLdb.connect(host=si['host'],user=si['user'],passwd=si['passwd'],db=si['db'],charset=si['charset'])
    cursor = conn.cursor()
    cursor.execute ('set names "%s"' % (si['charset']))

    print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S  ") + "CREATE & TRUNCATE Table ing... "

    sql_table = "select table_name from information_schema.tables where table_name='%s' and table_schema='%s'" %( si['fwq_all_status'], si['db'] )
    ish = cursor.execute (sql_table)
    if ish ==1:
        sql_table = 'TRUNCATE table ' + si['fwq_all_status']
        cursor.execute (sql_table)
    else:
        sql_table = 'create table if not exists ' + si['fwq_all_status'] + ' like ' + si['fwq_all_tmp']
        cursor.execute (sql_table)
    conn.commit()

    print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S  ") + "DATE Update ing... "

    sql_replace = "replace into " + si['fwq_all_status'] + " (zname,name,slug \
    			,type,population,queue \
    			,wintergrasp_area,wintergrasp_controlling_faction,wintergrasp_status,wintergrasp_next \
    			,tol_barad_area,tol_barad_controlling_faction,tol_barad_status,tol_barad_next \
    			,status,battlegroup,locale,timezone,time ) \
                values('%s','%s','%s' \
                ,'%s','%s','%s' \
                ,'%s','%s','%s','%s' \
                ,'%s','%s','%s','%s' \
                ,'%s','%s','%s','%s','%s' )"

    count_download = 0L
    for i in sfj['realms']:
        j = i['wintergrasp']
        k = i['tol-barad']
        #print (sql1%(i['name'],i['slug'],i['slug'],i['type'],i['population'],i['queue'],j['area'],j['controlling-faction'],j['status'],j['next'],k['area'],k['controlling-faction'],k['status'],k['next'],i['status'],i['battlegroup'],i['locale'],i['timezone']))
        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        i['population'] = str(i['population']).lower()
        i['status'] = str(i['status']).lower()
        i['queue'] = str(i['queue']).lower()

        count_download = count_download + 1
        cursor.execute(sql_replace % (i['name'],i['slug'],i['slug'] \
                            ,i['type'],i['population'],i['queue'] \
                            ,j['area'],j['controlling-faction'],j['status'],j['next'] \
                            ,k['area'],k['controlling-faction'],k['status'],k['next'] \
                            ,i['status'],i['battlegroup'],i['locale'],i['timezone'],now_time ))

    conn.commit()
    cursor.close()
    conn.close()

    return count_download

def main():
    main_start = datetime.datetime.now()

    main_count = try_get_fwq_status()

    print '\n',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S  '),str(main_count),' items OVER!'
    main_end = datetime.datetime.now()
    print '\nUSE Time : ',str(main_end - main_start)

if __name__ == '__main__':
    main()

