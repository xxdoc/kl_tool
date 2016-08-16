# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        qq_api
# Purpose:
#
# Author:      Administrator
#
# Created:     01/01/2016
# Copyright:   (c) Administrator 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import pymongo
import redis

from api_tool import Config

_CONF = {
    'api_ver': 'v1.0',
    'mongodb': {
        'host': 'wownga.jios.org',
        'port': 27017,
    },
    'mongofs': {
        'host': 'wownga.jios.org',
        'port': 27018,
    },
    'redis': {
        'host': '127.0.0.1',
        'port': 6379,
        'db': 0,
    }
}

config = Config(_CONF)
config.MONGODB_CONN = pymongo.MongoClient(**config.mongodb)
config.MONGOFS_CONN = pymongo.MongoClient(**config.mongofs)
config.REDIS_CONN = redis.StrictRedis(**config.redis)

def main():
    print config

    config1 = Config()
    print config1
    print id(config)
    print id(config1)

if __name__ == '__main__':
    main()
