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
cursor_str = conn.cursor()

setsql = 'set names "utf8"'
cursor.execute(setsql)

print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S  ') \
    + 'CREATE Table ing... '

setsql = 'create table if not exists ' + si['wow_item_table'] \
    + ' like ' + si['wow_item_tmp']
cursor.execute(setsql)
conn.commit()

api_item_url = r'http://www.battlenet.com.cn/api/wow/item/'
main_url = r'http://www.battlenet.com.cn/api/wow/realm/status'

sql1 = 'replace into ' + si['wow_item_table'] \
    + "   (id,item_id,description,name,icon,stackable \
        ,itemBind,buyPrice,itemClass,itemSubClass,containerSlots \
        ,inventoryType,equippable,itemLevel,maxCount,maxDurability \
        ,minFactionId,minReputation,quality,sellPrice,requiredSkill \
        ,requiredLevel,requiredSkillRank,itemSource_sourceId,itemSource_sourceType,baseArmor \
        ,hasSockets,isAuctionable,armor,displayInfoId,nameDescription \
        ,nameDescriptionColor,upgradable,heroicTooltip ) \
        values( \
            '%s','%s','%s','%s','%s','%s' \
            ,'%s','%s','%s','%s','%s' \
            ,'%s','%s','%s','%s','%s' \
            ,'%s','%s','%s','%s','%s' \
            ,'%s','%s','%s','%s','%s' \
            ,'%s','%s','%s','%s','%s' \
            ,'%s','%s','%s' )"

count = 0
print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S '), \
    'DATE Update ing... '
print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S '), \
    'JSON load ing... '

cursor_str.execute('select id,item_id,item_str from '
                   + si['wow_item_str'] + ' order by id')
while 1:
    row = cursor_str.fetchone()
    if row == None:
        break
    try:
        j = json.loads(row[2])
    except:
        try:
            j = json.loads(row[2].replace(chr(10), r""))
            print '\n'+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S '),str(row[1]),'replace chr(10) is ok now !'
        except Exception,ex:
            print '\n'+row[2]
            print Exception,':',ex
            break;
    j['description'] = j['description'].replace("'", r"\'")
    j['name'] = j['name'].replace("'", r"\'")
    j['nameDescription'] = j['nameDescription'].replace("'", r"\'")
    sql_cmd = sql1 % (
        row[0],
        j['id'],
        j['description'],
        j['name'],
        j['icon'],
        j['stackable'],
        j['itemBind'],
        j['buyPrice'],
        j['itemClass'],
        j['itemSubClass'],
        j['containerSlots'],
        j['inventoryType'],
        j['equippable'],
        j['itemLevel'],
        j['maxCount'],
        j['maxDurability'],
        j['minFactionId'],
        j['minReputation'],
        j['quality'],
        j['sellPrice'],
        j['requiredSkill'],
        j['requiredLevel'],
        j['requiredSkillRank'],
        j['itemSource']['sourceId'],
        j['itemSource']['sourceType'],
        j['baseArmor'],
        j['hasSockets'],
        j['isAuctionable'],
        j['armor'],
        j['displayInfoId'],
        j['nameDescription'],
        j['nameDescriptionColor'],
        j['upgradable'],
        j['heroicTooltip'],
        )
    cursor.execute(sql_cmd)
    conn.commit()
    count = count + 1
    print str(row[1]),

# now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

cursor.close()
conn.close()

print '\n'+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S  ') \
    + str(count) + ' items OVER!'
end = datetime.datetime.now()
print '\nUSE Time : ' + str(end - start)


