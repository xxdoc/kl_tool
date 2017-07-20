# -*- coding: utf-8 -*-
import os
import datetime

from tool_copy import (
    get_url
)

def _LOG(msg_in, time_now=True, new_line=True):
    if time_now:
        time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        msg_in = u'%s => %s' % (time_str, msg_in)
    if getattr(_LOG, 'log_file', None):
        _LOG.log_file.write(msg_in+'\n')
        _LOG.log_file.flush()

    if isinstance(msg_in, unicode):
        msg_in = msg_in.encode('gbk', 'ignore')

    if new_line:
        print msg_in
    else:
        print msg_in,

def get_page(page_html):
    pass


def main():
    main_start = datetime.datetime.now()

    url = 'http://zyy.loewenw.com/'
    tmp_path = os.path.join(os.getcwd(), 'tmp')
    page_html = get_url(url, tmp_path)

    get_page(page_html)

    print 'USE Time : ', str(datetime.datetime.now() - main_start)

if __name__ == '__main__':
    main()