#-------------------------------------------------------------------------------
# Name:        ??1
# Purpose:
#
# Author:      konglin
#
# Created:     04-03-2014
# Copyright:   (c) konglin 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import MySQLdb
import json
import os
import datetime
import urllib2



def main():


    qq_url = r'http://qun.594sgk.com/qq/%s.html'


    start = 23312465
    end = 23312465+10

    for i_loop in range(start, end):
        rs = ''
        i_str = str(i_loop)
        try:
            req = urllib2.Request(qq_url%i_str)
            rs = urllib2.urlopen(req).read()

        except Exception, ex:
            print i_str, ',',

        if rs != '':
            table_start = rs.rfind('<table ',4755,4785)
            if table_start > 0:
                table_end = rs.rfind('</table>',table_start)
                if table_end > 0:
                    rs = rs[table_start:table_end+8]

if __name__ == '__main__':
    main_time_start = datetime.datetime.now()
    main();
    main_time_end = datetime.datetime.now()
    print '\nUSE Time : ' + str(main_time_end - main_time_start)