#!/usr/bin/python
# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------------
# Name:        try_down_json
# Purpose:
#
# Author:      Administrator
#
# Created:     20/03/2014
# Copyright:   (c) Administrator 2014
# Licence:     <your licence>
# -------------------------------------------------------------------------------

import json
import urllib2
import os
import web
import win32con
import win32api
import time
import datetime

import win32com.client

WOW_AH_DB = web.database(
    host='127.0.0.1',
    dbn='mysql',
    user='root',
    pw='root',
    db='wow_ah_db',
    charset='utf8',
    )

WEB_HOME_PACH = "H:\\wowxxx\\webapp"

def try_down_json(fwq_name):
    global WEB_HOME_PACH
    print fwq_name,

    main_url = r'http://www.battlenet.com.cn/api/wow/auction/data/' + fwq_name.encode('utf-8')
    is_try_download = False

    res = ''
    c = 0L
    while len(res.strip()) == 0 and c < 10:
        try:
            req = urllib2.Request(main_url)
            res = urllib2.urlopen(req).read()
            print '|',
        except Exception, ex:
            c = c + 1
            print '.',

    if res.strip() == 0 :
        print 'network error!!'
        return False

    try:
        drj = json.loads(res)
        print '>>>',
    except Exception, ex:
        print Exception, ':', ex
        print 'JSON str error!!'
        return False

    ah_file_last = drj['files'][0]['lastModified']
    ah_file_url = drj['files'][0]['url']

    file_patch = ''.join([WEB_HOME_PACH, '\\JSON\\', fwq_name, '.json'])
    ah_file_name = ''.join([fwq_name, '_', str(drj['files'][0]['lastModified']), '.json'])
    ah_file_path = WEB_HOME_PACH + '\\JSON\\DATA_TEMP\\'
    ah_bak_path = WEB_HOME_PACH + '\\JSON\\DATA_TEMP\\DATA_BAK\\'
    ah_full_name = ah_file_path + ah_file_name

    try:
        dff = open(file_patch, 'r+') if os.path.isfile(file_patch) else open(file_patch, 'w')

        if os.path.getsize(file_patch) > 999128:
            dfj = json.load(dff)
            if drj['files'][0]['lastModified'] > dfj['files'][0]['lastModified']:
                dff.seek(0, 0)
                dff.write(res)
                is_try_download = True
        else:
            dff.seek(0, 0)
            dff.write(res)
            is_try_download = True
    except Exception, ex:
        print Exception, ':', ex
        print 'JSON file error!!'
        return False
    finally:
        dff.flush()
        dff.close

    if os.path.isfile(ah_full_name) or os.path.isfile(ah_bak_path + ah_file_name) or os.path.isfile(ah_full_name + '.td'):
        is_try_download = False

    if not is_try_download:
        print '(pass) ',
        return False
    else:
        print '(add) ',
        return [fwq_name, ah_file_url, ah_file_name, ah_file_path]


def try_get_fwq(wowdb):

    fwqdb = wowdb.query("select * from aa_fwq_info where fwqID>=0 and count>=0 and catinfo<>'close' and time<'2014-04-19' ")
    n_count = 0L
    list_down = {}
    list_down_all = []

    for n in fwqdb:
        list_down.setdefault(str(n['qu']) , {})
        list_down[ str(n['qu']) ].setdefault( str(n['battlegroup']) , [])
        re_down = try_down_json( n['zname'] )
        if re_down:
            n_count = n_count + 1
            list_down_all.append(re_down)
            list_down[ str(n['qu']) ][ str(n['battlegroup']) ].append(re_down)

    down_list_with_thunder(list_down_all)
    html_str = get_html_fwq(list_down)
    write_str_file(''.join([WEB_HOME_PACH, '.\\',datetime.datetime.now().strftime('ah_down_%Y_%m_%d_%H_%M_%S'), '.html']), html_str)
    return n_count

def down_list_with_thunder(list_down_all):
    ThunderAgent = win32com.client.Dispatch("ThunderAgent.Agent.1")
    for down_info in list_down_all:
        ThunderAgent.AddTask12(down_info[1], down_info[2], "", down_info[0], down_info[1], "", -1, 0, -1,  "", "", "", 0, "rightup")
    ThunderAgent.CommitTasks2(1)


def write_str_file(file_name, str_in):
    try:
        file_object = open(file_name, 'w')
        file_object.write(str_in.encode('utf-8'))
    finally:
        file_object.close()

def get_html_fwq(list_down):
    html_str = ''
    html_head_start ="""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>fwq_list</title>
</head>
<body>
	<ul class="subnavmenu" id="submenus01" style="z-index: 2000; left: 290px; top: 49px; visibility: visible;">
		<li class="topline">
			<a href="/cn-guild/" class="sub">cn</a>
			<ul style="left: 172px; top: 0px; visibility: visible;">
"""
    html_qu_start = """
				<li class="topline">
					<a href="/cn-guild/%s_qu-zone/" class="sub">%s qu</a>
					<ul style="left: 172px; top: 0px; visibility: visible;">
"""
    html_battlegroup_start = """
						<li class="topline">
							<a href="/cn-guild/Battle Group %s-bg/" class="sub">Battle Group %s</a>
							<ul style="left: 0px; top: 0px;">
"""
    html_down_list = """
								<li class="topline">
									<span> %s </span>
                                    <a href="%s">%s</a>
								</li>
"""
    html_battlegroup_end = """
							</ul>
						</li>
"""
    html_qu_end = """
				    </ul>
				</li>
"""
    html_head_end = """
 			</ul>
		</li>
	</ul>
</body>
</html>
"""
    html_str = ''.join( [html_str, html_head_start] )
    for qu in sorted(list_down.keys()):
        html_str = ''.join( [html_str, html_qu_start % (qu, qu)] )
        for battlegroup in sorted(list_down[qu].keys()):
            html_str = ''.join( [html_str, html_battlegroup_start % (battlegroup, battlegroup)] )
            for down_list in list_down[qu][battlegroup]:
                html_str = ''.join( [html_str, html_down_list % (down_list[0], down_list[1], down_list[2])] )
            html_str = ''.join( [html_str, html_battlegroup_end] )
        html_str = ''.join( [html_str, html_qu_end] )
    html_str = ''.join( [html_str, html_head_end] )
    return html_str;

def add_task_creature_jpg(base_int):
    portrait_url = r'http://content.battlenet.com.cn/wow/renders/npcs/portrait/creature%s.jpg'
    base_url = r'http://content.battlenet.com.cn/wow/renders/npcs/rotate/creature%s.jpg'
    base_name = r'creature%s.jpg'
    str_int = '%s%03d'

    list_down_all = []
    for i in range(0,1000):
        item_str = str_int % (base_int, i)
        file_url = base_url % item_str
        file_name = base_name % item_str
        item_dict = {'file_url':file_url, 'file_name':file_name, 'ps_text':'', 'from_url':''}
        list_down_all.append(item_dict)

    #list_down_all = [{'file_url':file_url, 'file_name':file_name, 'ps_text':ps_text, 'from_url':from_url}]
    #[file_url, file_name, ps_text, from_url]
    ThunderAgent = win32com.client.Dispatch("ThunderAgent.Agent.1")
    for down_info in list_down_all:
        ThunderAgent.AddTask12(down_info['file_url'], down_info['file_name'], "", down_info['ps_text'], down_info['from_url'], "", -1, 0, -1,  "", "", "", 0, "rightup")
    ThunderAgent.CommitTasks2(1)

def main():
    main_count = 0L
    main_start = datetime.datetime.now()

    global WOW_AH_DB
    #main_count = try_get_fwq(WOW_AH_DB)

    print '\n',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S  '),str(main_count),' items OVER!'
    main_end = datetime.datetime.now()
    print '\nUSE Time : ',str(main_end - main_start)

if __name__ == '__main__':
    main()