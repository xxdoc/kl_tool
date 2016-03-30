# -*- coding: utf-8 -*-
from selenium import webdriver
import time
import datetime

def main():
    try:
        channelId = int(raw_input('channelId:'))
        nums = int(raw_input('nums:'))
    except ValueError as ex:
        _LOG('error input')
        time.sleep(5)
        return None

    wait_m = 10
    host = '25wx.kkyoo.com'
    url = 'http://%s/dev_wx/wsp/index.php?r=web/livestream&id=%s' % (host, channelId)
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
    _LOG('end')

def _LOG(msg_in, time_now=True, new_line=True):
    if time_now:
        time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        msg = '%s => %s' % (time_str, msg_in)
    if getattr(_LOG, 'log_file', None):
        _LOG.log_file.write(msg+'\n')
        _LOG.log_file.flush()

    if new_line:
        print msg
    else:
        print msg,

if __name__ == '__main__':
    main()