#-*- coding: utf-8 -*-
import datetime
import os
import urllib
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
from httptool import MultiHttpDownLoad, _LOG, load_str, pyhtml

import logging
import logging.handlers

TASK_LOG = logging.getLogger('task')

def init_log():
    global TASK_LOG
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(thread)d %(filename)s:%(lineno)s - %(name)s - %(message)s')

    log_file = os.path.join(os.getcwd(), 'log', 'sina_task.log')
    handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=8*1024*1024, backupCount=5)
    handler.setFormatter(formatter)
    TASK_LOG.addHandler(handler)
    TASK_LOG.setLevel(logging.DEBUG)


def flush_log():
    global TASK_LOG
    def _flush(logger):
        for handler in logger.handlers:
            handler.flush()

    for item in [TASK_LOG, ]:
        _flush(item)

def main():
    init_log()
    fwq_dict = get_fwq()
    print fwq_dict

def get_fwq():
    fwq_dict = {}
    html = load_str('sina_fwq.html')

    bs = BeautifulSoup(html, 'lxml')
    group_ul = bs.find('ul').find('ul')
    for group in group_ul.findChildren('ul'):
        group_title = group.findParent().find('a').text.strip()
        fwq_dict[group_title] = [item.text.strip() for item in group.findAll('li')]

    return fwq_dict

def get_guild(realm, faction='', playersmin='', playersmax=''):
    faction = '' if not faction else ('a' if faction=='a' else 'h')
    base_api = 'http://armory.games.sina.com.cn/GuildList.aspx?action=ajaxload&area=CN&region=&'
    args = {'realm': realm, 'faction': faction, 'playersmin':playersmin, 'playersmax':playersmax}
    api += urllib.urlencode(args)


if __name__ == '__main__':
    main()
