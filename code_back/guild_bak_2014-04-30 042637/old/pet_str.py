#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import MySQLdb
import json
import os
import datetime
import urllib2

start = datetime.datetime.now()

print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S  ') \
    + 'SET Read ing... '

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
                                "fwq_all_tmp": "aaa_fwq_all",
                    "wow_item_table": "aaa_wow_item",
                    "wow_item_tmp": "aaa_item_tmp",
                    "wow_item_str": "aaa_item_str",
                    "wow_pet_str": "aaa_pet_str"
                            },
                            "log_set": {
                                "filename": "db_log.txt",
                                "level": 20,
                                "filemode": "a",
                                "format": "%(asctime)s - %(levelname)s: %(message)s"
                            }
                        }"""

# print base_cfg

bfj = json.loads(base_cfg)
si = bfj['MySQL_set']

print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S  ') \
    + 'DB Link ing... '
conn = MySQLdb.connect(host=si['host'], user=si['user'],
                       passwd=si['passwd'], db=si['item_db'],
                       charset=si['charset'])

cursor = conn.cursor()
setsql = 'set names "utf8"'
cursor.execute(setsql)

api_item_url = r'http://www.battlenet.com.cn/api/wow/item/'

api_pet_ability_url = \
    r'http://www.battlenet.com.cn/api/wow/battlePet/ability/'
api_pet_species_url = \
    r'http://www.battlenet.com.cn/api/wow/battlePet/species/'
api_pet_stats_url = \
    r'http://www.battlenet.com.cn/api/wow/battlePet/stats/258?level=25&breedId=5&qualityId=4'

print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S  ') \
    + 'DATE Update ing... '

sql1 = 'insert into ' + si['wow_pet_str'] \
    + " (species_id,ability_id,pet_str) values(%s,%s,'%s')"

print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S  ') \
    + 'JSON Download ing... '

start = 0
for i_loop in range(start, 1200):
    rs = ''
    i_str = str(i_loop)
    try:
        req = urllib2.Request(api_pet_ability_url + i_str)
        f = urllib2.urlopen(req)
        rs = f.read()
        print '\n' \
            + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S  ') \
            + i_str + ' JSON Download ' + str(len(rs)) + ' byte'
    except Exception, ex:
        print i_str, ',',
    if rs != '':
        rs = rs.replace("'", r"\'")
        cursor.execute(sql1 % (0, i_str, rs.decode('utf8', 'ignore')))
        conn.commit()

start = 0
count = start
for i_loop in range(start, 3000):
    rs = ''
    i_str = str(i_loop)
    try:
        req = urllib2.Request(api_pet_species_url + i_str)
        f = urllib2.urlopen(req)
        rs = f.read()
        print '\n' \
            + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S  ') \
            + i_str + ' JSON Download ' + str(len(rs)) + ' byte'
    except Exception, ex:
        print i_str, ',',
    if rs != '':
        rs = rs.replace("'", r"\'")
        cursor.execute(sql1 % (i_str, 0, rs.decode('utf8', 'ignore')))
        conn.commit()
        count = count + 1

# name battlegroup  population type queue
# now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

cursor.close()
conn.close()

print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S  ') \
    + str(count) + ' items OVER!'
end = datetime.datetime.now()
print '\nUSE Time : ' + str(end - start)


