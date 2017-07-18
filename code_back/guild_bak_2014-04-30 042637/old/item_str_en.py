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
                       passwd=si['passwd'], db=si['db'],
                       charset=si['charset'])

cursor = conn.cursor()
cursor_str = conn.cursor()

setsql = 'set names "utf8"'
cursor.execute(setsql)

print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S  ') \
    + 'CREATE Table ing... '

setsql = 'CREATE TABLE aaa_ah_item SELECT id,item_id,name,icon,quality,itemClass,itemSubClass from wow_item_db.aaa_wow_item where isAuctionable="true"'
cursor.execute(setsql)
conn.commit()

#name battlegroup  population type queue
#now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

cursor.close()
conn.close()