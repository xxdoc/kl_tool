# -*- coding: utf-8 -*-
from selenium import webdriver
import time
from tool import _LOG

def main():
    host = '25.kkyoo.com'
    room_id = 100025
    nums = 28
    wait_m = 10
    url = 'http://%s/live/%d' % (host, room_id)
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