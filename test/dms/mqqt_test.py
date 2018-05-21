import os
import atexit
import time
import json
import logging
import logging.handlers

import paho.mqtt.client as mqtt
import requests
import random
import string

import hashlib

def php_md5(*str_args):
    strin = ''.join(str_args)
    m2 = hashlib.md5()
    m2.update(strin)
    return m2.hexdigest()

TASK_LOG = logging.getLogger('task')
DMS_LOG = logging.getLogger('dms')
USER_LOG = logging.getLogger('user')

def init_log():
    global TASK_LOG, DMS_LOG, USER_LOG
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(thread)d %(filename)s:%(lineno)s - %(name)s - %(message)s')

    log_file = os.path.join(os.getcwd(), 'log', 'dms_task.log')
    handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=8*1024*1024, backupCount=5)
    handler.setFormatter(formatter)
    TASK_LOG.addHandler(handler)
    TASK_LOG.setLevel(logging.DEBUG)

    log_file = os.path.join(os.getcwd(), 'log', 'dms_msg.log')
    handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=8*1024*1024, backupCount=5)
    handler.setFormatter(formatter)
    DMS_LOG.addHandler(handler)
    DMS_LOG.setLevel(logging.DEBUG)

    log_file = os.path.join(os.getcwd(), 'log', 'dms_user.log')
    handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=8*1024*1024, backupCount=5)
    handler.setFormatter(formatter)
    USER_LOG.addHandler(handler)
    USER_LOG.setLevel(logging.DEBUG)

def flush_log():
    global TASK_LOG, DMS_LOG, USER_LOG
    def _flush(logger):
        for handler in logger.handlers:
            handler.flush()

    for item in [TASK_LOG, DMS_LOG, USER_LOG]:
        _flush(item)

rand_str = lambda n: ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(n))

def rand_config(dms_key):
    tSeq = int(int(time.time()) / 10)

    client_id = rand_str(15)
    dms_pub_key = rand_str(15)
    dms_sub_key = php_md5("%s_%s_%s_%d" % (dms_key, client_id, dms_pub_key, tSeq))

    return {
        'client_id': client_id,
        'pub_key': dms_pub_key,
        'sub_key': dms_sub_key
    }

class DmsAnalysis(object):

    def __init__(self, dms_host, dms_port, dms_key, topics):
        self.dms_host = dms_host
        self.dms_port = dms_port
        self.dms_key = dms_key

        config = rand_config(self.dms_key)

        self.client = self._init_dms_client(topic_list=topics, **config)

    def on_dms_msg(self, topic, dms_str):
        def json_decode(json_str):
            try:
                return json.loads(json_str)
            except Exception as ex:
                log_msg = '%s:%s.json_decode %s->%r' % ('on_dms_msg', topic, json_str, ex)
                USER_LOG.error(log_msg)
                return {}

    def _init_dms_client(self, client_id, pub_key, sub_key, topic_list):
        # The callback for when the client receives a CONNACK response from the server.
        def on_connect(client_obj, userdata, flags, rc):
            log_msg = '%s<%s> rst:%s' % ('connected', client_obj.client_id, rc)
            print log_msg
            DMS_LOG.debug(log_msg)
            for topic in topic_list:
                rst = client_obj.subscribe(topic)
                log_msg = '%s<%s>:%s rst:%s' % ('subscribe', client_obj.client_id, topic, rst)
                DMS_LOG.debug(log_msg)
                print log_msg

        # The callback for when a PUBLISH message is received from the server.
        def on_message(client_obj, userdata, msg):
            body = msg.payload.decode('utf-8', 'ignore')
            log_msg = '%s:%s' % (msg.topic, body)
            DMS_LOG.debug(log_msg)
            print log_msg
            self.on_dms_msg(msg.topic, body)

        client = mqtt.Client(client_id)
        client.on_connect = on_connect
        client.on_message = on_message
        client.username_pw_set(pub_key, sub_key)
        client.topic_list = topic_list
        client.client_id = client_id
        client.connect(self.dms_host, self.dms_port, 60)
        log_msg = '%s:%s rst:%s' % ('_init_dms_client', client.client_id, client.topic_list)
        TASK_LOG.info(log_msg)
        print log_msg
        return client

    def run(self):
        self.client.loop_start()

    def close(self):
        flush_log()
        self.client.disconnect()

def main():
    init_log()
    class Config(object):
        def __init__(self, **kwgs):
            self.__dict__.update(kwgs)

    my_app_config = Config(**{
        'dms_host': '127.0.0.1',
        'dms_port': 1883,
        'dms_key': '2b284b8794e233e1f24b0c1fff2c5444',
        'topics': [
            'test_a', 'test_b'
        ]
    })

    my_app = DmsAnalysis(my_app_config.dms_host, my_app_config.dms_port, my_app_config.dms_key, my_app_config.topics)
    atexit.register(my_app.close)
    my_app.run()


if __name__ == '__main__':
    main()