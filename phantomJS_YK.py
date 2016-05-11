# -*- coding: utf-8 -*-
from selenium import webdriver
import time
from tool import _LOG

def main():
##    try:
##        host_key = raw_input('host_key:')
##        channelId = int(raw_input('channelId:'))
##        nums = int(raw_input('nums:'))
##    except ValueError as ex:
##        _LOG('error input')
##        time.sleep(5)
##        return None

    host_key = '25wx'
    channelId = 3757
    nums = 10

    wait_m = 10
    host = host_key + '.kkyoo.com'
    url = 'http://%s/dev_wx/web/livestream/%d' % (host, channelId)
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