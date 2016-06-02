# -*- coding: utf-8 -*-
import urllib
import pymongo
import random
import time
import os
from tool import load_obj, save_obj, get_json, _LOG, s2t, get_dir_file, load_json

MONGODB = pymongo.MongoClient('127.0.0.1', 27017)
MONGODB_CUR = MONGODB.admin_112.room_95

ALL_USER = ['test_%d' % i for i in range(200)]

obj_list = get_dir_file(os.getcwd(), is_ok=lambda x:x.endswith('.obj'), key=lambda x:x[1]['size'])
read_file = obj_list[-1][0]
print "MAIN START READ FILE:", read_file
BASE_MSG = load_json(read_file).keys()

def main():
    for i in range(10000):
        doc = {
                'msg':random.choice(BASE_MSG),
                'room_id':95,
                'user_id':random.choice(ALL_USER),
                'time':time.time(),
                'state':1,
                'last_state':0,
                'replay_list':[],
            }
        MONGODB_CUR.insert(doc)


if __name__ == '__main__':
    main()


"""
use dms
db.peidui.ensureIndex({"topic":1})
db.peidui.ensureIndex({"time":1})
db.peidui.ensureIndex({"msg":1})
db.peidui.getIndexes()
"""