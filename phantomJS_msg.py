# -*- coding: utf-8 -*-
from selenium import webdriver
import time
import datetime
import os

def main():
    url = 'http://25wx.kkyoo.com/dev_wx/wsp/index.php?r=web/livestream&id=3137'
    driver_list = []
    for i in range(30):
        tmp = webdriver.PhantomJS()
        tmp.get(url)
        driver_list.append(tmp)


def test():
    driver = webdriver.PhantomJS() #webdriver.Firefox()
    url = 'http://25wx.kkyoo.com/dev_wx/wsp/index.php?r=web/livestream&id=3137'
    driver.get(url)
    print driver.title
    dms_box = driver.find_elements_by_id('aodianyun-dms-text')[0]
    dms_btn = driver.find_elements_by_class_name('send_btn')[0]
    for i in range(1000):
        msg = ''.join(map(lambda xx:(hex(ord(xx))[2:]),os.urandom(32)))
        msg += datetime.datetime.now().strftime(' %Y-%m-%d %H:%M:%S.%f')
        time.sleep(0.1)
        dms_box.send_keys(msg)
        time.sleep(0.1)
        dms_btn.click()
        _LOG('send ' + msg)
    driver.quit()

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
    test()