import sys,MySQLdb,json,os,datetime,urllib2

start = datetime.datetime.now()

print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S  ") + "SET Read ing... "

base_cfg = """{
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
                    "wow_item": "aaa_wow_item",
                    "wow_item_tmp": "aaa_item_tmp"
			    },
			    "log_set": {
			        "filename": "db_log.txt",
			        "level": 20,
			        "filemode": "a",
			        "format": "%(asctime)s - %(levelname)s: %(message)s"
			    }
			}"""

#print base_cfg
bfj = json.loads(base_cfg)
si = bfj['MySQL_set']

print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S  ") + "DB Link ing... "
conn = MySQLdb.connect(host=si['host'],user=si['user'],passwd=si['passwd'],db=si['item_db'],charset=si['charset'])

cursor = conn.cursor()
setsql = 'set names "utf8"'
cursor.execute (setsql)

print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S  ") + "CREATE Table ing... "

setsql = 'create table if not exists ' + si['wow_item'] + ' like ' + si['wow_item_tmp']
cursor.execute (setsql)
conn.commit()

api_item_url = r'http://www.battlenet.com.cn/api/wow/item/';
main_url = r'http://www.battlenet.com.cn/api/wow/realm/status'

print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S  ") + "JSON Download ing... "

re = urllib2.Request(main_url)
rs = urllib2.urlopen(re).read()
print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S  ") + "JSON Download " + str(len(rs)) + ' byte'

sfj = json.loads(rs)


print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S  ") + "DATE Update ing... "

{"id":76623,"description":"aaa","name":"bbb",
"icon":"inv_misc_gem_x4_uncommon_perfectcut_purple","stackable":20,"itemBind":0,

"bonusStats":[],"itemSpells":[],

"buyPrice":44000,"itemClass":3,"itemSubClass":3,"containerSlots":0,

"gemInfo":{"bonus":{"name":"+80 a +120 s","srcItemId":76623,"requiredSkillId":0,"requiredSkillRank":0,"minLevel":0,"itemLevel":1},
"type":{"type":"PURPLE"},"minItemLevel":417},

"inventoryType":0,"equippable":false,"itemLevel":88,"maxCount":0,"maxDurability":0,"minFactionId":0,
"minReputation":0,"quality":3,"sellPrice":11000,"requiredSkill":0,"requiredLevel":0,"requiredSkillRank":0,
"itemSource":{"sourceId":0,"sourceType":"NONE"},"baseArmor":0,"hasSockets":false,"isAuctionable":true,"armor":0,
"displayInfoId":112227,"nameDescription":"","nameDescriptionColor":"000000","upgradable":false,"heroicTooltip":false}



sql1 = "replace into " + si['wow_item'] + " (item_id,description,name,icon,stackable,itemBind \
			,buyPrice,itemClass,itemSubClass,containerSlots \
			,tol_barad_area,tol_barad_controlling_faction,tol_barad_status,tol_barad_next \
			,status,battlegroup,locale,timezone,time ) \
            values('%s','%s','%s' \
            ,'%s','%s','%s' \
            ,'%s','%s','%s','%s' \
            ,'%s','%s','%s','%s' \
            ,'%s','%s','%s','%s','%s' )"


cursor.execute(sql1%(i['name'],i['slug'],i['slug'] \
						,i['type'],i['population'],i['queue'] \
						,j['area'],j['controlling-faction'],j['status'],j['next'] \
						,k['area'],k['controlling-faction'],k['status'],k['next'] \
						,i['status'],i['battlegroup'],i['locale'],i['timezone'],now_time ))

conn.commit()



#name battlegroup  population type queue
#now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

cursor.close()
conn.close()

print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S  ") + str(len(sfj['realms'])) + ' items OVER!'
end = datetime.datetime.now()
print "\nUSE Time : " + str(end - start)