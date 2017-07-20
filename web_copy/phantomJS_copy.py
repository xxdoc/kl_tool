# -*- coding: utf-8 -*-
from selenium import webdriver
import time, datetime

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



def main():
    url = 'http://zyy.loewenw.com/'
    webkit = webdriver.PhantomJS()
    page = webkit.get(url)

    def callback(requestData, networkRequest):
        pass

    page.onResourceRequested(callback)
    _LOG('end')

if __name__ == '__main__':
    main()