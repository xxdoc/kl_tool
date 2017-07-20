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
import time
import datetime


def try_get_fwq():
    re_db = 'wow_test_db'

    wowdb = web.database(
        host='127.0.0.1',
        dbn='mysql',
        user='root',
        pw='root',
        db=re_db,
        charset='utf8',
        )


    fwqdb = wowdb.query("SELECT table_name as name FROM INFORMATION_SCHEMA.TABLES WHERE table_schema = '%s'" % (re_db))

    n_count = 0L

    for n in fwqdb:
        tname = n['name']
        if tname[0:4] != 'itb_':
            wowdb.query("RENAME TABLE `%s` TO `%s`" % (tname, 'itb_'+tname))
            n_count = n_count + 1
    return n_count

def main():
    main_start = datetime.datetime.now()

    main_count = try_get_fwq()

    print '\n',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S  '),str(main_count),' items OVER!'
    main_end = datetime.datetime.now()
    print '\nUSE Time : ',str(main_end - main_start)

if __name__ == '__main__':
    main()

