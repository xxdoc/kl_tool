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
    host = 'finance.aodianyun.com'
    room_id = 1000
    nums = 30
    wait_m = 10
    url = 'http://%s/slive/%d' % (host, room_id)
    driver_list = []
    for i in range(nums):
        tmp = webdriver.PhantomJS()
        tmp.get(url)
        driver_list.append(tmp)
        _LOG('add')
    _LOG('wait')
    for i in range(wait_m):
        _LOG('...')
        time.sleep(60)

    for item in driver_list:
        try:
            item.close()
            item.quit()
        except:
            pass
    _LOG('end')

if __name__ == '__main__':
    main()