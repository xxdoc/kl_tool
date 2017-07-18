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
                                "charset": "utf8",
                                "port": 3306,
                                "ah_tmp": "aaa_ah_tmp",
                                "fwq_tmp": "aaa_fwq_tmp",
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


def json_main(cfg_file='wow_ah.cfg', xz=1):
    global base_cfg
    logging.basicConfig(filename=os.path.join(os.getcwd(),
                        'base_log.log'), level=logging.ERROR,
                        filemode='a',
                        format='%(asctime)s - %(levelname)s: %(message)s'
                        )

    start = datetime.datetime.now()
    print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S  ') \
        + 'SET Read ing... '
    logging.info('cfg JSON: Read JSON>> ' + cfg_file)

    if len(cfg_file.strip()) == 0:
        cfg_file = 'wow_ah.cfg'
    if cfg_file.find(':') <= 0:
        cfg_file = os.path.join(os.getcwd(), cfg_file)

    if os.path.isfile(cfg_file):
        file_size = os.path.getsize(cfg_file)
        if file_size > 1:
            logging.info('cfg JSON: done >> ' + cfg_file)
            dfj = json_loadf(cfg_file, offset=0)
            if len(dfj) < 4:
                err_str = 'cfg Error: x_json >> ' + cfg_file \
                    + ' (Error:-12)'
                print err_str
                logging.error(err_str)
                return -12
        else:
            err_str = 'cfg Error: x_file >> ' + cfg_file \
                + ' (Error:-10)'
            print err_str
            logging.error(err_str)
            return -10
    else:
        err_str = 'cfg Error: no file >> ' + cfg_file + ' (Error:-11)'
        print err_str
        logging.error(err_str)
        return -11

    bfj = json.loads(base_cfg)
    for i in bfj:
        if not dfj.has_key(i):
            err_str = 'cfg Error: no ' + i + ' >> ' + cfg_file \
                + ' (Error:-15)'
            print err_str
            logging.error(err_str)
            return -15
        else:
            for n in bfj[i]:
                if dfj[i].has_key(n):
                    if isinstance(bfj[i][n], unicode):
                        dfj[i][n] = str(dfj[i][n])
                        dfj[i][n] = dfj[i][n].strip()
                        if len(dfj[i][n]) == 0:
                            dfj[i][n] = bfj[i][n]
                else:

                     # print i + ">" + n + ">" + dfj[i][n]

                    if xz == 1:
                        dfj[i][n] = bfj[i][n]
                    else:
                        err_str = 'cfg Error: no ' + str(n) + ' in ' \
                            + str(i) + ' >> ' + cfg_file \
                            + ' (Error:-14)'
                        print err_str
                        logging.error(err_str)
                        return -14

    if len(dfj['base_set']['base_path']) == 0:
        dfj['base_set']['base_path'] = os.getcwd()
        err_str = 'cfg Warning: no basepath use: ' + os.getcwd() \
            + ' >> ' + cfg_file + ' (Warning:1)'
        print err_str
        logging.warning(err_str)
    if dfj['base_set']['bak_size_limt'] <= 0:
        dfj['base_set']['bak_size_limt'] = 0L
        err_str = \
            'cfg Warning: no Bakeup with set: bak_size_limt=0 >> ' \
            + cfg_file + ' (Warning:2)'
        print err_str
        logging.warning(err_str)

    if dfj.has_key('task'):
        if dfj['task'].has_key('info'):
            if len(dfj['task']['info']) > 0:
                for i in dfj['task']['info']:
                    if i.has_key('is') and i.has_key('name'):
                        pass
                    else:
                        err_str = 'cfg Error: error task info >> ' \
                            + cfg_file + ' (Error:-16)'
                        print err_str
                        logging.error(err_str)
                        return -16
                print 'Task Count :' + str(len(dfj['task']['info']))
                logging.info('cfg INFO: task count : '
                             + str(len(dfj['task']['info'])) + ' >> '
                             + cfg_file + '  (' + str(len(dfj['task'
                             ]['info'])) + ')')
            else:
                err_str = 'cfg Error: task count is 0 >> ' + cfg_file \
                    + ' (Error:-17)'
                print err_str
                logging.error(err_str)
                return -17
        else:
            err_str = 'cfg Error: no task info >> ' + cfg_file \
                + ' (Error:-19)'
            print err_str
            logging.error(err_str)
            return -19
    else:
        err_str = 'cfg Error: no task >> ' + cfg_file + ' (Error:-18)'
        print err_str
        logging.error(err_str)
        return -18

    print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S  ') \
        + 'Done JSON file : ' + cfg_file
    logging.info('cfg JSON: Done JSON>> ' + cfg_file)

    dir_set(dfj['base_set'])

    bs = dfj['base_set']
    si = dfj['MySQL_set']

    conn_i = MySQLdb.connect(host=si['host'], user=si['user'],
                             passwd=si['passwd'], db=si['db'],
                             charset=si['charset'])
    cursor_i = conn_i.cursor()
    si['conn'] = conn_i
    si['cursor'] = cursor_i
    setsql = 'set names "utf8"'
    cursor_i.execute(setsql)

    setsql = \
        'select table_name from information_schema.tables where table_name = "aa_fwq_info" and table_schema="' \
        + si['db'] + '"'
    if cursor_i.execute(setsql) == 0:
        setsql = 'create table if not exists aa_fwq_info like ' \
            + si['fwq_tmp']
        cursor_i.execute(setsql)
    conn_i.commit()

    print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S  ') \
        + 'Link ing... >> MySQL'
    logging.info('db MySQL: link >> ' + si['db'])

    end = datetime.datetime.now()
    print '\nTime Used:' + str(end - start) + '\n'

    log_set(dfj['log_set'])

    t_count = 0L
    nd = 0L
    n_count = 0L
    o_count = 0L
    for i in dfj['task']['info']:
        if i['is'] == 1:
            start = datetime.datetime.now()
            si['fwq_name'] = i['name']
            rd = -1L
            rd = ah_json_mysql(bs, si, del_o=1, useload=True)
            end = datetime.datetime.now()
            if rd <= 0:
                if rd == -31:
                    if nd != rd:
                        print '\nno JSON file : ' + i['name'],
                    else:
                        print ', ' + i['name'],
                    n_count = n_count + 1
                    nd = rd
                    continue
                if rd == -30:
                    if nd != rd:
                        print '\ndownload ing JSON file : ' + i['name'],
                    else:
                        print ',' + i['name'],
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
    cursor_i.close()
    conn_i.close()

    return t_count


def make_inti_dir(base_path_in, *add_path_in):
    count_path = 0L
    if len(add_path_in) == 0:
        return -1L
    base_path = ''
    add_path = ''
    base_path = base_path_in.strip()
    if len(base_path) == 0:
        base_path = os.getcwd()
    for add_path in add_path_in:
        if isinstance(add_path, int):
            add_path = str(add_path)
            add_path = add_path.strip()
            if len(add_path) == 0:
                count_path = count_path + 100
                continue
            else:
                base_path = os.path.join(base_path, add_path)
                if not os.path.isdir(base_path):
                    if os.path.isfile(base_path):
                        try:
                            os.remove(base_path)
                        except:
                            pass
                        count_path = count_path + 1000
                    try:
                        os.makedirs(base_path)
                    except:
                        pass
                        count_path = count_path + 1
    return count_path


def log_set(si):
    if len(si) < 4:
        return -1L
    else:
        logging.basicConfig(filename=si['filename'], level=si['level'],
                            filemode=si['filemode'], format=si['format'
                            ])
        return 1L


def dir_set(si):
    if len(si) < 4:
        return -1L
    else:
        rd = -1L
        try:
            rd = make_inti_dir(si['base_path'], si['JSON_path'],
                               si['DATA_TEMP_path'], si['DATA_BAK_path'
                               ])
        except:
            pass
        if rd > 0:
            print 'Make Dir by make_inti_dir(), return :' + str(rd)
        if rd == -1:
            print 'Erroe Dir by make_inti_dir(), return :' + str(rd)
        return rd


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
                    err_str = 'db Info: del old file >> ' + l \
                        + ' (Info:23)'
                    print err_str
                    logging.info(err_str)
    return cn


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
    if ah_file_size < bak_size_limt * 1024 * 1024:
        bak_file_path = bak_dir + '\\' + ah_file_name
        if os.path.isfile(bak_file_path):
            try:
                os.remove(bak_file_path)
            except:
                pass
        try:
            os.rename(ah_file_path, bak_file_path)
        except:
            pass
        if os.path.isfile(ah_file_path):
            try:
                os.remove(ah_file_path)
            except:
                pass
        bak_size = getdirsize(bak_dir)
        logging.info('bak JSON: ' + ah_file_name + ' ('
                     + str(ah_file_size) + ' / ' + str(bak_size) + ')')
        print 'Bakup JSON file : ' + ah_file_name + ' (' \
            + str(ah_file_size) + ' / ' + str(bak_size) + ')'
    else:
        if os.path.isfile(ah_file_path):
            try:
                os.remove(ah_file_path)
            except:
                pass
        bak_size = getdirsize(bak_dir)

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
            print 'Bakup Out Size: ' + str(bak_size) + '/' \
                + str(bak_size_limt * 1024 * 1024)
            print 'Bakup Del : ' + files[0][1]
            logging.info('bak JSON: Bakup Out >> ' + str(bak_size)
                         + ' / ' + str(bak_size_limt) + ' -Del >> '
                         + files[0][1])
    return bak_size


def ah_json_mysql(
    bs,
    si,
    del_o=1,
    useload=False,
    no_file_print=0,
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
    fwq_tmp = si['fwq_tmp']
    db = si['db']
    port = si['port']

    if not isinstance(fwq_name, str):
        pass

        # fwq_name = repr(fwq_name)
        # fwq_name = str(fwq_name)

    fwq_name = fwq_name.lower()
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
        if filename.find(fwq_name) == 0 and filename.find('.json') \
            == len(filename) - 5:
            f_s.append(filename)
        if filename.find(fwq_name) == 0 and filename.find('.json.td') \
            == len(filename) - 8:
            isd = 1

    if len(f_s) <= 0:
        if isd == 1:
            err_str = 'db Error:' + fwq_name + ' Is Downing JSON >> ' \
                + temp_dir + ' (Error:-30)'
            if no_file_print == 1:
                print err_str
            logging.error(err_str)
            return -30
        err_str = 'db Error:' + fwq_name + ' no JSON >> ' + temp_dir \
            + ' (Error:-31)'
        if no_file_print == 1:
            print err_str
        logging.error(err_str)
        return -31

    print '\n\n------------------------' + si['fwq_name'] + '------------------------'
    print 'De AH json ing...'

    f_s.sort(reverse=True)
    lf_s = ''
    for l in f_s:
        ld = os.path.join(temp_dir, l)
        if os.path.isfile(ld):
            l_size = os.path.getsize(ld)
            if l_size > 128:
                try:
                    ahf = file(ld)
                    try:
                        ahj = json.load(ahf)
                        lf_s = l
                        err_str = 'db Info:' + fwq_name \
                            + ' load json file >> ' + l + ' (Info:21)'
                        print err_str
                        logging.info(err_str)
                        break
                    finally:
                        ahf.close()
                except Exception, ex:
                    print Exception,':',ex
                    err_str = 'db Error:' + fwq_name + ' X_JSON >> ' \
                        + l + ' (Error:-32)'
                    print err_str
                    logging.error(err_str)
                    continue
            else:
                err_str = 'db Error:' + fwq_name + ' X_file >> ' + l \
                    + ' (Error:-33)'
                print err_str
                logging.error(err_str)
                continue
        else:
            err_str = 'db Error:' + fwq_name + ' NO_FILE >> ' + l \
                + ' (Error:-34)'
            print err_str
            logging.error(err_str)
            continue

    if lf_s == '':
        err_str = 'db Error:' + fwq_name + ' cannot load file >> ' \
            + temp_dir + ' (Error:-35)'
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
            write_list_txt(ah_from, ahj[ah_from]['auctions'], sql1,
                           sql2, fo, fwq_name)

            ah_from = 'horde'
            write_list_txt(ah_from, ahj[ah_from]['auctions'], sql1,
                           sql2, fo, fwq_name)

            ah_from = 'neutral'
            write_list_txt(ah_from, ahj[ah_from]['auctions'], sql1,
                           sql2, fo, fwq_name)
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
        sql1 = \
            "update aa_fwq_info set fsize='%s',last='%s',time='%s',url='%s',dir='%s', \
            count='%s',counta='%s',counth='%s',countn='%s' where slug='%s'"
        sql1 = sql1 % (
            ah_file_size,
            ah_file_last,
            now,
            ah_file_url,
            ah_file_path2,
            cc,
            ac,
            hc,
            nc,
            ahj['realm']['slug'],
            )
        n = cursor.execute(sql1)
    else:
        sql1 = \
            "replace into aa_fwq_info (name,slug,fsize,last,time,url,dir,count,counta,counth,countn) \
                    values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
        sql1 = sql1 % (
            ahj['realm']['name'],
            ahj['realm']['slug'],
            ah_file_size,
            ah_file_last,
            now,
            ah_file_url,
            ah_file_path2,
            cc,
            ac,
            hc,
            nc,
            )
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


def getdirsize(dir_in):
    size = 0L
    dir_s = dir_in.strip()
    if len(dir_s) == 0 or not os.path.isdir(dir_s):
        return -1L
    for (root, dirs, files) in os.walk(dir_s):
        size += sum([os.path.getsize(os.path.join(root, name))
                    for name in files])
    return size


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


##def executemanyklex(self, query, args, argt=None, constr=None, step=15, a_name=False, s_index=None, e_index=None):
##
##    del self.messages[:]
##    if not args or not isinstance(args, list):
##        return -1L;
##    db = self._get_db()
##
##    query = query.strip()
##    charset = db.character_set_name()
##    if isinstance(query, unicode):
##        query = query.encode(charset)
##
##    s_q = ['insert into ','replace into ']
##    r = 'values'
##    if query.rfind(r.lower())==len(query)-6 or query.rfind(r.upper())==len(query)-6:
##        pass;
##    else:
##        return -1L;
##    a_index = 0L
##    for r in s_q:
##        if query.rfind(r.lower())==0 or query.rfind(r.upper())==0:
##            a_index = 1
##            break;
##    if a_index==0:
##        return -1L;
##
##    if argt is None and args and len(args)>0:
##        if isinstance(args[0], dict):
##            argt = args[0].keys()
##        else:
##            argt = []
##            for k in args:
##                argt.append(k)
##
##    if constr is None:
##        constr = ''
##    if len(query)==0 or len(argt)==0 or len(args)==0:
##        return -1L;
##    if s_index is None:
##        s_index = 0L
##    if e_index is None:
##        e_index = len(args)-1
##    if s_index > e_index or step<=0 or step > 50:
##        return -1L;
##    if a_name:
##        pass;
##    r = '('
##    for a in range(0,len(argt)):
##        r = r + '\'%s\','
##    else:
##        constr = constr.strip()
##        if len(constr) > 0:
##            r = r + constr + ')'
##        else:
##            r = r[0:(len(r)-1)] + ')'
##
##    db.query('SET GLOBAL innodb_flush_log_at_trx_commit = 0')
##    db.query('SET UNIQUE_CHECKS = 0')
##
##    a_index = s_index
##    try:
##        while a_index + step < e_index:
##            s_q = ''
##            for a in range(a_index, a_index + step):
##                s = []
##                for k in argt:
##                    s.append(args[a][k])
##                s_q = s_q + r%tuple(s) + ','
##            else:
##                s_q = s_q[0:(len(s_q)-1)]
##            if isinstance(s_q, unicode):
##                s_q = s_q.encode(charset)
##            db.query(query + s_q)
##            a_index = a_index + step
##
##        while a_index <= e_index:
##            s_q = ''
##            a = a_index
##            s = []
##            for k in argt:
##                s.append(args[a][k])
##            s_q = r%tuple(s)
##            if isinstance(s_q, unicode):
##                s_q = s_q.encode(charset)
##            db.query(query + s_q)
##            a_index = a_index + 1
##
##        db.query('SET GLOBAL innodb_flush_log_at_trx_commit = 1')
##        db.query('SET UNIQUE_CHECKS = 1')
##        return e_index - s_index +1
##
##    except TypeError, msg:
##        if msg.args[0] in ("not enough arguments for format string",
##                           "not all arguments converted"):
##            self.errorhandler(self, ProgrammingError, msg.args[0])
##        else:
##            self.errorhandler(self, TypeError, msg)
##    except (SystemExit, KeyboardInterrupt):
##        raise
##    except:
##        exc, value, tb = sys.exc_info()
##        del tb
##        self.errorhandler(self, exc, value)
##    if not self._defer_warnings: self._warning_check()
##    db.query('SET GLOBAL innodb_flush_log_at_trx_commit = 1')
##    db.query('SET UNIQUE_CHECKS = 1')
##    return 0;
##
##def executemanyklexahdb(self, args, ah_from, fwq_name):
##    """Execute a multi-row query.
##    query -- string, query to execute on server
##    args
##        Sequence of sequences or mappings, parameters to use with
##        query.
##    Returns long integer rows affected, if any.
##    This method improves performance on multiple-row INSERT and
##    REPLACE. Otherwise it is equivalent to looping over args with
##    execute().
##    """
##    del self.messages[:]
##    if len(args)==0:
##        return -1L;
##    db = self._get_db()
##    charset = db.character_set_name()
##    db.query('SET GLOBAL innodb_flush_log_at_trx_commit = 0')
##    db.query('SET UNIQUE_CHECKS = 0')
##
##    query = "insert into " + fwq_name + " values"
##    sql1 = "('%s','%s','%s','%s','%s','%s','%s','%s','%s',0,0,0,0,\"" + ah_from + "\")"
##    sql2 = "('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',\"" + ah_from + "\")"
##
##    if isinstance(query, unicode):
##        query = query.encode(charset)
##    a_index = 0L
##    e_index = len(args)-1
##    step = 15
##    try:
##        while a_index + step < e_index:
##            s_q = ''
##            for a in range(a_index, a_index + step):
##                i = args[a]
##                r = ''
##                k_len = len(i)
##                if k_len ==9:
##                    r = sql1%(i["auc"],i["item"],i["owner"],i["bid"],i["buyout"],i["quantity"],i["timeLeft"],i["rand"],i["seed"])
##                elif k_len ==13:
##                    r = sql2%(i["auc"],i["item"],i["owner"],i["bid"],i["buyout"],i["quantity"],i["timeLeft"],i["rand"],i["seed"],\
##                                        i["petSpeciesId"],i["petBreedId"],i["petLevel"],i["petQualityId"])
##                s_q = s_q + r + ','
##            else:
##                s_q = s_q[0:(len(s_q)-1)]
##            if isinstance(s_q, unicode):
##                s_q = s_q.encode(charset)
##            db.query(query + s_q)
##            a_index = a_index + step
##
##        while a_index <= e_index:
##            i = args[a_index]
##            s_q = ''
##            k_len = len(i)
##            if k_len ==9:
##                s_q = sql1%(i["auc"],i["item"],i["owner"],i["bid"],i["buyout"],i["quantity"],i["timeLeft"],i["rand"],i["seed"])
##            elif k_len ==13:
##                s_q = sql2%(i["auc"],i["item"],i["owner"],i["bid"],i["buyout"],i["quantity"],i["timeLeft"],i["rand"],i["seed"],\
##                                    i["petSpeciesId"],i["petBreedId"],i["petLevel"],i["petQualityId"])
##            if isinstance(s_q, unicode):
##                s_q = s_q.encode(charset)
##            db.query(query + s_q)
##            a_index = a_index + 1
##
##        db.query('SET GLOBAL innodb_flush_log_at_trx_commit = 1')
##        db.query('SET UNIQUE_CHECKS = 1')
##        return e_index +1
##
##    except TypeError, msg:
##        if msg.args[0] in ("not enough arguments for format string",
##                           "not all arguments converted"):
##            self.errorhandler(self, ProgrammingError, msg.args[0])
##        else:
##            self.errorhandler(self, TypeError, msg)
##    except (SystemExit, KeyboardInterrupt):
##        raise
##    except:
##        exc, value, tb = sys.exc_info()
##        del tb
##        self.errorhandler(self, exc, value)
##    if not self._defer_warnings: self._warning_check()
##    db.query('SET GLOBAL innodb_flush_log_at_trx_commit = 1')
##    db.query('SET UNIQUE_CHECKS = 1')
##    return 0;

if __name__ == '__main__':
    print sys.argv[0] + ' >>'
    cfg = ''
    if len(sys.argv) == 1:
        cfg = 'wow_ah.cfg'
    else:
        cfg = sys.argv[1].strip()

    stime = datetime.datetime.now()

    do_count = json_main(cfg)
    print 'all fwq ',do_count,' is over !'
    print 'All Time Used:' + str(datetime.datetime.now() - stime)

print '\nOVER'


