# -*- coding: utf-8 -*-
from selenium import webdriver
import time
import datetime
import os

from tool import _LOG

def main():
    host_key = '25wx'
    channelId = 3931
    nums = 1000

    host = host_key + '.kkyoo.com'
    url = 'http://%s/dev_wx/wsp/index.php?r=web/livestream&id=%s' % (host, channelId)

    driver = webdriver.PhantomJS() #webdriver.Firefox()
    driver.get(url)
    print driver.title
    time.sleep(1)
    dms_box = driver.find_elements_by_class_name('chat_input')[0]
    dms_btn = driver.find_elements_by_class_name('send_btn')[0]
    for i in range(nums):
        msg = ''.join([hex(ord(xx))[2:] for xx in os.urandom(32)])
        msg += datetime.datetime.now().strftime(' %Y-%m-%d %H:%M:%S.%f')
        time.sleep(0.1)
        dms_box.send_keys(msg)
        time.sleep(0.1)
        dms_btn.click()
        _LOG('send ' + msg)
    driver.quit()


if __name__ == '__main__':
    main()