#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import MySQLdb
import json
import os
import logging
import datetime


base_cfg = \
    """{
                                "base_set": {
                                "base_path": "..\",
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
                                "charset": "utf8",
                                "port": 3306,
                                "ah_tmp": "aaa_ah_tmp",
                                "fwq_info": "aa_fwq_info",
                                "fwq_info_tmp": "aa_fwq_info_tmp",
                                "fwq_all_status": "aa_fwq_status",
                                "fwq_all_tmp": "aaa_fwq_all"
                            },
                            "log_set": {
                                "filename": "db_log.txt",
                                "level": 20,
                                "filemode": "a",
                                "format": "%(asctime)s - %(levelname)s: %(message)s"
                            }
                        }"""

# json_main
def json_main():
    global base_cfg
    logging.basicConfig(filename=os.path.join(os.getcwd(),
                        'base_log.log'), level=logging.ERROR,
                        filemode='a',
                        format='%(asctime)s - %(levelname)s: %(message)s'
                        )

    start = datetime.datetime.now()
    print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S  '), 'SET Read ing... '
    logging.info('cfg JSON: Read JSON>> SET Read ing... ')

    dfj = json.loads(base_cfg)
    bs = dfj['base_set']
    si = dfj['MySQL_set']

    dir_set(bs)
    log_set(dfj['log_set'])

    conn_i = MySQLdb.connect(host=si['host'], user=si['user'], passwd=si['passwd'], db=si['db'], charset=si['charset'])
    cursor_i = conn_i.cursor()
    cursor_fwq = conn_i.cursor()
    si['conn'] = conn_i
    si['cursor'] = cursor_i
    setsql = 'set names "utf8"'
    cursor_i.execute(setsql)

    setsql = "select table_name from information_schema.tables where table_name ='%s' and table_schema='%s' " % (si['fwq_info'], si['db'])
    if cursor_i.execute(setsql) == 0:
        setsql = 'create table if not exists %s like %s' % (si['fwq_info'], si['fwq_tmp'])
        cursor_i.execute(setsql)
    conn_i.commit()

    print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S  '),'Link ing... >> MySQL'
    logging.info('db MySQL: link >> ' + si['db'])
    end = datetime.datetime.now()
    print '\nTime Used:',str(end - start),'\n'

    t_count = 0L
    nd = 0L
    n_count = 0L
    o_count = 0L

    sql_fwq = 'select fwqID,slug,zname,catinfo from ' + si['db'] + '.' + si['fwq_info'] + ' where fwqID>=0 order by fwqID '
    cursor_fwq.execute(sql_fwq)

    for i in cursor_fwq.fetchall():
        if i[3] == 'close':
            continue
        fwq_id = i[0]
        fwq_name = i[2].strip()
        start = datetime.datetime.now()
        si['fwq_name'] = fwq_name
        rd = -1L
        rd = ah_json_mysql(bs, si, del_o=1, useload=True, no_file_print=0)
        end = datetime.datetime.now()
        if rd <= 0:
            if rd == -31:
                if nd != rd:
                    print '\nno JSON file : ' + fwq_name,
                else:
                    print ', ' + fwq_name,
                n_count = n_count + 1
                nd = rd
                continue
            if rd == -30:
                if nd != rd:
                    print '\ndownload ing JSON file : ' + fwq_name,
                else:
                    print ',' + fwq_name,
                n_count = n_count + 1
                nd = rd
                continue
            nd = rd
            print si['fwq_name'] + ' -->> ah_json_mysql  ERROR : ' \
                + str(rd)
            print 'Time Used:' + str(end - start) + '\n'
            if rd == -28:
                o_count = o_count + 1
        else:
            nd = rd
            t_count = t_count + 1
            print si['fwq_name'] + ' -->> ah_json_mysql  DONE : ' \
                + str(rd)
            print 'Time Used:' + str(end - start) + '\n'

    if n_count > 0:
        print '\n\nAll no JSON file :'+str(n_count)+'\n'
    if o_count > 0:
        print 'All old JSON file :'+str(o_count)+'\n'

    conn_i.commit()
    cursor_fwq.close()
    cursor_i.close()
    conn_i.close()

    return t_count

# make_inti_dir
def make_inti_dir(base_path_in, *add_path_in):
    if len(add_path_in) == 0:
        return False
    base_path = base_path_in.strip()
    if len(base_path) == 0:
        base_path = os.getcwd()
    for add_path in add_path_in:
        add_path = str(add_path).strip()
        if len(add_path) == 0:
            continue
        base_path = os.path.join(base_path, add_path)
        if not os.path.isdir(base_path):
            try:
                os.makedirs(base_path)
            except:
                pass

# log_set
def log_set(si):
    logging.basicConfig(filename=si['filename'], level=si['level'],filemode=si['filemode'], format=si['format'])

# dir_set
def dir_set(si):
    make_inti_dir(si['base_path'], si['JSON_path'],si['DATA_TEMP_path'], si['DATA_BAK_path'])

# del_out
def del_out(
    f_s,
    lf_s,
    temp_dir,
    del_o=1,
    ):

    cn = -1L
    if del_o == 1:
        cn = 0
        for l in f_s:
            if l != lf_s:
                l = os.path.join(temp_dir, l)
                if os.path.isfile(l):
                    try:
                        cn = cn + 1
                        os.remove(l)
                    except:
                        pass
    return cn

# back_up
def back_up(
    ah_file_path,
    ah_file_name,
    bak_dir,
    bak_size_limt,
    ):

    bak_size = 0L
    if not os.path.isfile(ah_file_path):
        return -1L
    ah_file_size = os.path.getsize(ah_file_path)
    try:
        if ah_file_size < bak_size_limt * 1024 * 1024:
            bak_file_path = os.path.join(bak_dir, ah_file_name)
            if os.path.isfile(bak_file_path):
                os.remove(bak_file_path)
            os.rename(ah_file_path, bak_file_path)
            if os.path.isfile(ah_file_path):
               os.remove(ah_file_path)
            bak_size = getdirsize(bak_dir)
            msg_str = ''.join(['Bakup JSON file : ', ah_file_name, ' (', str(ah_file_size), ' / ', str(bak_size), ')'])
            logging.info(msg_str)
            print msg_str
        else:
            if os.path.isfile(ah_file_path):
                os.remove(ah_file_path)
            bak_size = getdirsize(bak_dir)
    except:
        pass

    while bak_size > bak_size_limt * 1024 * 1024:
        files = [(os.path.getmtime(os.path.join(bak_dir, x)),
                 os.path.join(bak_dir, x)) for x in os.listdir(bak_dir)]
        files.sort(key=lambda x:x[0])
        if os.path.isfile(files[0][1]):
            try:
                os.remove(files[0][1])
                bak_size = getdirsize(bak_dir)
            except:
                pass
            msg_str = ''.join(['bak JSON: Bakup Out >> ', str(bak_size), ' / ', str(bak_size_limt), ' -Del >> ', files[0][1] ])
            print 'Bakup Out Size: ',str(bak_size),'/',str(bak_size_limt * 1024 * 1024)
            print 'Bakup Del : ',files[0][1]
            logging.info(msg_str)
    return bak_size
# getdirsize
def getdirsize(dir_in):
    size = 0L
    dir_s = dir_in.strip()
    if len(dir_s) == 0 or not os.path.isdir(dir_s):
        return -1L
    for (root, dirs, files) in os.walk(dir_s):
        size += sum([os.path.getsize(os.path.join(root, name))
                    for name in files])
    return size

# json_loadf
def json_loadf(filename, offset=0):
    if filename[offset:offset + 1] == '{':
        fj = json.loads(filename)
    else:
        fo = open(filename, 'r')
        if offset >= 0 and offset < 128:
            fo.seek(offset, 0)
            fs = fo.read()
        try:
            fj = json.loads(fs)
        finally:
            fo.close()
    return fj


# write_list_txt
def write_list_txt(
    ah_from,
    li,
    sql1,
    sql2,
    fo,
    fwq
    ):

    for i in li:
        if not i.has_key('ownerRealm'):
            i['ownerRealm'] = fwq

        k_len = len(i)
        if k_len == 10:
            fo.write((sql1 % (
                i['auc'],
                i['item'],
                i['owner'],
                i['ownerRealm'],
                i['bid'],
                i['buyout'],
                i['quantity'],
                i['timeLeft'],
                i['rand'],
                i['seed'],
                ah_from,
                )).encode('utf-8'))
        elif k_len == 14:
            fo.write((sql2 % (
                i['auc'],
                i['item'],
                i['owner'],
                i['ownerRealm'],
                i['bid'],
                i['buyout'],
                i['quantity'],
                i['timeLeft'],
                i['rand'],
                i['seed'],
                i['petSpeciesId'],
                i['petBreedId'],
                i['petLevel'],
                i['petQualityId'],
                ah_from,
                )).encode('utf-8'))
        else:
            continue
    else:
        fo.flush()


# ah_json_mysql
def ah_json_mysql(
    bs,
    si,
    del_o=1,
    useload=True,
    no_file_print=0
    ):

    base_path = bs['base_path']
    JSON_path = bs['JSON_path']
    DATA_TEMP_path = bs['DATA_TEMP_path']
    DATA_BAK_path = bs['DATA_BAK_path']
    bak_size_limt = bs['bak_size_limt']

    fwq_name = si['fwq_name'].lower()
    conn = si['conn']
    cursor = si['cursor']
    ah_tmp = si['ah_tmp']
    db = si['db']

    if len(fwq_name.strip()) == 0:
        return -99

    if len(base_path.strip()) == 0:
        base_path = os.getcwd()
    json_dir = os.path.join(base_path, JSON_path)
    temp_dir = os.path.join(json_dir, DATA_TEMP_path)
    bak_dir = os.path.join(temp_dir, DATA_BAK_path)

    f_s = []
    isd = 0
    for filename in os.listdir(temp_dir):
        if os.path.isdir(os.path.join(temp_dir, filename)):
            continue
        filename = filename.lower()
        if filename.find(fwq_name) == 0 and filename.find('.json') == len(filename) - 5:
            f_s.append(filename)
        if filename.find(fwq_name) == 0 and filename.find('.json.td') == len(filename) - 8:
            isd = 1
    if len(f_s) <= 0:
        if isd == 1:
            err_str = 'db Error:' + fwq_name + ' Is Downing JSON >> ' + temp_dir + ' (Error:-30)'
            if no_file_print == 1:
                print err_str
            logging.error(err_str)
            return -30
        err_str = 'db Error:' + fwq_name + ' no JSON >> ' + temp_dir + ' (Error:-31)'
        if no_file_print == 1:
            print err_str
        logging.error(err_str)
        return -31

    print '\n\n------------------------' + si['fwq_name'] + '------------------------'
    print 'De AH json ing...'

    f_s.sort(reverse=True)
    lf_s = ''
    for l in f_s:
        try:
            ahf = file(os.path.join(temp_dir, l))
            try:
                ahj = json.load(ahf)
                lf_s = l
                err_str = 'db Info:' + fwq_name + ' load json file >> ' + l + ' (Info:21)'
                print err_str
                logging.info(err_str)
                break
            finally:
                ahf.close()
        except Exception, ex:
            print Exception,':',ex
            err_str = 'db Error:' + fwq_name + ' X_JSON >> ' + l + ' (Error:-32)'
            print err_str
            logging.error(err_str)
            continue

    if lf_s == '':
        err_str = 'db Error:' + fwq_name + ' cannot load file >> ' + temp_dir + ' (Error:-35)'
        print err_str
        logging.error(err_str)
        return -35

    ah_file_url = 'Null'
    ah_file_last = lf_s[lf_s.find('_') + 1:len(lf_s) - 5]
    ah_file_name = lf_s
    ah_file_path = os.path.join(temp_dir, lf_s)
    ah_file_size = os.path.getsize(ah_file_path)

    del_out(f_s, lf_s, temp_dir, del_o)

    fwq_nt = ahj['realm']['slug'].lower().replace('-', '_')

    setsql = \
        'select table_name from information_schema.tables where table_name = "' \
        + fwq_nt + '" and table_schema="' + db + '"'
    ish = cursor.execute(setsql)
    if ish == 1:
        count = cursor.execute('select * from ' + fwq_nt)
    else:
        count = 0

    n = cursor.execute('select last from aa_fwq_info where slug="'
                       + ahj['realm']['slug'] + '"')

    if n == 1:
        result = cursor.fetchone()
        f = lf_s
        if str(result[0]) >= f[f.find('_') + 1:len(f) - 5] and ish == 1 \
            and count > 0:
            err_str = 'db Error:' + fwq_nt + ' db is real new >> ' \
                + f + ' (Error:-28)'
            print err_str
            logging.error(err_str)
            back_up(ah_file_path, ah_file_name, bak_dir, bak_size_limt)
            return -28

    ac = len(ahj['alliance']['auctions'])
    hc = len(ahj['horde']['auctions'])
    nc = len(ahj['neutral']['auctions'])
    cc = ac + hc + nc
    if cc == 0:
        print 'Error : count >> ', ac, hc, nc, cc
        logging.error('db Error:' + fwq_name + ' no count >> 0 (-14)')
        return -14
    if len(ahj['realm']['name'].strip()) == 0:
        print 'Error : fwq_name >> ', ahj['realm']['name']
        logging.error('db Error:' + fwq_name + ' no name >> xxxxx (-15)'
                      )
        return -15

    if ish == 1:
        setsql = 'TRUNCATE table ' + fwq_nt
        cursor.execute(setsql)
    else:
        setsql = 'create table if not exists ' + fwq_nt + ' like ' \
            + ah_tmp
        cursor.execute(setsql)

    conn.commit()
    if useload:
        lf = fwq_nt + '.temp'
        lf = os.path.join(temp_dir, lf)
        if os.path.isfile(lf):
            try:
                os.remove(lf)
            except:
                pass
        fo = open(lf, 'w+')
        try:
            sql1 = \
                u'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t0\t0\t0\t0\t%s\n'
            sql2 = \
                u'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n'

            ah_from = 'alliance'
            write_list_txt(ah_from, ahj[ah_from]['auctions'], sql1, sql2, fo, fwq_name)

            ah_from = 'horde'
            write_list_txt(ah_from, ahj[ah_from]['auctions'], sql1, sql2, fo, fwq_name)

            ah_from = 'neutral'
            write_list_txt(ah_from, ahj[ah_from]['auctions'], sql1, sql2, fo, fwq_name)
        finally:
            fo.close()

        setsql = 'LOAD DATA LOCAL INFILE \'' + lf.replace('\\', '\\\\'
                ).replace("\'", "\\\'") + '\' INTO TABLE ' + fwq_nt \
            + ' LINES TERMINATED BY \'\\r\\n\''

        # print setsql
        lf_count = cursor.execute(setsql)
        if lf_count == 0:
            print 'Load File SQL error !!!'
            return -19
        print 'Load File count: ' + str(lf_count)

    else:
        ah_from = 'alliance'
        print 'Updata ing... >> alliance:' \
            + str(cursor.executemanyklexahdb(ahj[ah_from]['auctions'],
                  ah_from, fwq_nt))
        ah_from = 'horde'
        print 'Updata ing... >> horde :' \
            + str(cursor.executemanyklexahdb(ahj[ah_from]['auctions'],
                  ah_from, fwq_nt))
        ah_from = 'neutral'
        print 'Updata ing... >> neutral :' \
            + str(cursor.executemanyklexahdb(ahj[ah_from]['auctions'],
                  ah_from, fwq_nt))

    print 'Updata ing... >> aa_fwq_info'
    conn.commit()

    ahj['realm']['name'] = ahj['realm']['name'].replace("\'", "\\\'")
    ah_file_path2 = ah_file_path.replace('\\', '\\\\')
    ah_file_path2 = ah_file_path2.replace("\'", "\\\'")
    now = datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S')
    sql1 = "select slug from aa_fwq_info where slug='%s'" % (ahj['realm']['slug'])
    n = cursor.execute(sql1)

    if n == 1:
        sql1 = "update aa_fwq_info set fsize='%s',last='%s',time='%s',url='%s',dir='%s',count='%s',counta='%s',counth='%s',countn='%s' where real_slug='%s'"
        sql1 = sql1 % (ah_file_size,ah_file_last,now,ah_file_url,ah_file_path2,cc,ac,hc,nc,ahj['realm']['slug'],)
        n = cursor.execute(sql1)
    else:
        sql1 = "replace into aa_fwq_info (name,slug,fsize,last,time,url,dir,count,counta,counth,countn,real_slug) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
        sql1 = sql1 % (ahj['realm']['name'],ahj['realm']['slug'],ah_file_size,ah_file_last,now,ah_file_url,ah_file_path2,cc,ac,hc,nc,ahj['realm']['slug'])
        n = cursor.execute(sql1)

    conn.commit()

    back_up(ah_file_path, ah_file_name, bak_dir, bak_size_limt)
    if useload:
        if os.path.isfile(lf):
            try:
                os.remove(lf)
            except:
                pass
    logging.info('db MySQL:' + fwq_name + ' done >> ' + fwq_name)
    print 'Done by: ' + str(now)
    return cc





if __name__ == '__main__':
    print sys.argv[0] + ' >>'

    stime = datetime.datetime.now()

    do_count = json_main()
    print 'all fwq ',do_count,' is over !'
    print 'All Time Used:' + str(datetime.datetime.now() - stime)

print '\nOVER'


