import os
import atexit
import time
import json
import logging
import logging.handlers

import paho.mqtt.client as mqtt
import requests


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

class DmsAnalysis(object):

    def __init__(self, dms_host, dms_port, topic_api, topic_timer=10, nums_timer=10):
        self.dms_host = dms_host
        self.dms_port = dms_port
        self.topic_api = topic_api
        self.topic_timer = topic_timer
        self.nums_timer = nums_timer

        self.dms_config = self.get_dms_config()
        self.dms_list = {}
        self.dms_user_map = {}
        self.dms_count_map = {}
        self.dms_max_map = {}

    def save_topic_max(self, topic, total):
        tmp = 0  #本次数据大于 上次存储的最大用户数 则更新 否则忽略
        if total > tmp:
            log_msg = '%s.save %s total:%s, max:%s' % ('save_topic_max', topic, total, tmp)
            TASK_LOG.info(log_msg)
        else:
            log_msg = '%s.ignore %s total:%s, max:%s' % ('save_topic_max', topic, total, tmp)
            TASK_LOG.debug(log_msg)

    def save_topic_count(self):
        for topic, total in self.dms_max_map.items():
            if total <= 0:
                log_msg = '%s.ignore %s total:%s' % ('save_topic_count', topic, total)
                TASK_LOG.debug(log_msg)
                continue

            self.save_topic_max(topic, total)
            log_msg = '%s.save %s total:%s' % ('save_topic_count', topic, total)
            TASK_LOG.info(log_msg)
            self.dms_max_map[topic] = self.dms_count_map[topic]


    def on_dms_msg(self, topic, dms_str):
        def json_decode(json_str):
            try:
                return json.loads(json_str)
            except Exception as ex:
                log_msg = '%s:%s.json_decode %s->%r' % ('on_dms_msg', topic, json_str, ex)
                USER_LOG.error(log_msg)
                return {}

        dms_data = json_decode(dms_str)
        if not dms_data:
            return

        now_time = int(time.time())
        self.dms_user_map[topic] = self.dms_user_map.get(topic, {})
        self.dms_count_map[topic] = self.dms_count_map.get(topic, 0)
        self.dms_max_map[topic] = self.dms_max_map.get(topic, 0)
        log_msg = '%s:%s.json_decode %s' % ('on_dms_msg', topic, dms_data)
        USER_LOG.debug(log_msg)

        if dms_data.get('cmd', '') == 'present' and dms_data.get('clientId', ''):
            total = int(dms_data.get('total', 0))
            if total >= 0:
                self.dms_count_map[topic] = total  #存储当前用户人数 和 最大人数
                self.dms_max_map[topic] = total if total > self.dms_max_map.get(topic, 0) else self.dms_max_map.get(topic, 0)
                log_msg = '%s:%s.count total:%s, max:%s' % ('on_dms_msg', topic, total, self.dms_max_map[topic])
                (USER_LOG.info if total > 0 else USER_LOG.debug)(log_msg)

            client_id = dms_data.get('clientId', '')
            time_stamp = int(dms_data.get('time', 0))
            time_stamp = time_stamp if time_stamp > 0 else now_time
            if int(dms_data.get('state', -1)) == 1:  #用户进入房间  记录下进入时间
                self.dms_user_map[topic][client_id] = time_stamp
                log_msg = '%s:%s.in %s at %s' % ('on_dms_msg', topic, client_id, time_stamp)
                USER_LOG.debug(log_msg)
            elif int(dms_data.get('state', -1)) == 0:  #用户退出房间  获取进入时间 和 退出时间 存储
                in_time, out_time = self.dms_user_map[topic].pop(client_id, now_time), time_stamp
                log_msg = '%s:%s.out %s at %s-%s(%s)' % ('on_dms_msg', topic, client_id, in_time, out_time, out_time-in_time)
                USER_LOG.info(log_msg)

    def get_dms_config(self):
        tmp = {}
        try:
            tmp = requests.get(self.topic_api).json()
        except Exception as ex:
            pass
        config = []
        for item in tmp:
            dms_item = {}
            dms_item['admin_id'] = int(item.get('admin_id', 0))
            dms_item['dms_pub_key'] = item.get('dms_pub_key', '').strip()
            dms_item['dms_sub_key'] = item.get('dms_sub_key', '').strip()
            dms_item['topic_list'] = set(item.get('topic_list', []))
            if dms_item['topic_list']:
                config.append(dms_item)
        log_msg = '%s, rst:%s' % ('get_dms_config', config)
        TASK_LOG.info(log_msg)
        return config

    def _init_dms_client(self, admin_id, pub_key, sub_key, topic_list):
        # The callback for when the client receives a CONNACK response from the server.
        def on_connect(client_obj, userdata, flags, rc):
            log_msg = '%s<%s> rst:%s' % ('connected', client_obj.admin_id, rc)
            print log_msg
            DMS_LOG.debug(log_msg)
            for topic in topic_list:
                topic = str('__present__' + topic)
                rst = client_obj.subscribe(topic)
                log_msg = '%s<%s>:%s rst:%s' % ('subscribe', client_obj.admin_id, topic, rst)
                DMS_LOG.debug(log_msg)

        # The callback for when a PUBLISH message is received from the server.
        def on_message(client_obj, userdata, msg):
            body = msg.payload.decode('utf-8', 'ignore')
            log_msg = '%s:%s' % (msg.topic, body)
            DMS_LOG.debug(log_msg)
            self.on_dms_msg(msg.topic, body)

        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        client.username_pw_set(pub_key, sub_key)
        client.topic_list = topic_list
        client.admin_id = admin_id
        client.connect(self.dms_host, self.dms_port, 60)
        log_msg = '%s:%s rst:%s' % ('_init_dms_client', client.admin_id, client.topic_list)
        TASK_LOG.info(log_msg)
        return client

    def _fix_dms_client(self, client, topic_list):
        def _get_diff_topic(old_list, new_list):
            old_set, new_set = set(old_list), set(new_list)
            return old_set - new_set, new_set - old_set

        unsub_topic, newsub_topic = _get_diff_topic(client.topic_list, topic_list)
        log_msg = '%s.fix_topic<%s>, unsub_topic:%s, newsub_topic:%s' % ('_fix_dms_client', client.admin_id, unsub_topic, newsub_topic)
        (TASK_LOG.info if unsub_topic or newsub_topic else TASK_LOG.debug)(log_msg)

        for topic in unsub_topic:
            topic = str('__present__' + topic)
            rst = client.unsubscribe(topic)
            log_msg = '%s<%s>:%s rst:%s' % ('unsubscribe', client.admin_id, topic, rst)
            DMS_LOG.info(log_msg)
        for topic in newsub_topic:
            topic = str('__present__' + topic)
            rst = client.subscribe(topic)
            log_msg = '%s<%s>:%s rst:%s' % ('subscribe', client.admin_id, topic, rst)
            DMS_LOG.info(log_msg)

        client.topic_list = topic_list
        log_msg = '%s.fix_client<%s> rst:%s' % ('_fix_dms_client', client.admin_id, client.topic_list)
        TASK_LOG.debug(log_msg)
        return client

    def update_dms_client(self, dms_config=None):
        _last_cofig = self.dms_config
        if dms_config is None:
            dms_config = self.get_dms_config()
        log_msg = '%s rst:%s' % ('update_dms_client', dms_config)
        TASK_LOG.debug(log_msg)

        self.dms_config = dms_config
        for admin_item in self.dms_config:
            admin_id = admin_item['admin_id']
            if admin_id in self.dms_list:
                client = self.dms_list[admin_id]
                self.dms_list[admin_id] = self._fix_dms_client(client, admin_item['topic_list'])
            else:
                client = self._init_dms_client(admin_id, admin_item['dms_pub_key'], admin_item['dms_sub_key'], admin_item['topic_list'])
                self.dms_list[admin_item['admin_id']] = client
                log_msg = '%s:loop_start<%s> rst:%s' % ('update_dms_client', client.admin_id, client.topic_list)
                TASK_LOG.info(log_msg)
                client.loop_start()

        old_client = set([item['admin_id'] for item in _last_cofig])
        now_client = set([item['admin_id'] for item in dms_config])
        del_client = old_client - now_client
        log_msg = '%s, old_client:%s, now_client:%s, del_client:%s' % ('update_dms_client', old_client, now_client, del_client)
        (TASK_LOG.info if del_client else TASK_LOG.debug)(log_msg)

        for admin_id in del_client:
            client = self.dms_list.pop(admin_id, None)
            log_msg = '%s:disconnect<%s> rst:%s' % ('update_dms_client', client.admin_id, client.topic_list)
            TASK_LOG.info(log_msg)
            client.disconnect()

    def run(self):
        if not self.dms_config:
            self.dms_config = self.get_dms_config()

        now_minute = int(time.time() / 60)
        log_msg = '%s:start at %s config:%s' % ('run', now_minute, self.dms_config)
        TASK_LOG.info(log_msg)

        for admin_item in self.dms_config:
            admin_id = admin_item['admin_id']
            tmp = self._init_dms_client(admin_id, admin_item['dms_pub_key'], admin_item['dms_sub_key'], admin_item['topic_list'])
            self.dms_list[admin_id] = tmp

        for _, client in self.dms_list.items():
            log_msg = '%s:loop_start<%s> rst:%s' % ('run', client.admin_id, client.topic_list)
            TASK_LOG.info(log_msg)
            client.loop_start()

        while 1:
            now_minute = int(time.time() / 60)
            log_msg = '%s:timer at %s topic_timer:%s, nums_timer:%s' % ('run', now_minute, self.topic_timer, self.nums_timer)
            TASK_LOG.info(log_msg)

            if now_minute % self.topic_timer == 0:
                self.update_dms_client()
            if now_minute % self.nums_timer == 0:
                self.save_topic_count()

            time.sleep(60)
            print '.'

    def close(self):
        now_minute = int(time.time() / 60)
        log_msg = '%s:close at %s config:%s' % ('run', now_minute, self.dms_config)
        TASK_LOG.info(log_msg)
        for _, dms_item in self.dms_list.items():
            log_msg = '%s:disconnect<%s> rst:%s' % ('close', dms_item.admin_id, dms_item.topic_list)
            TASK_LOG.info(log_msg)
            dms_item.disconnect()

def main():
    init_log()
    class Config(object):
        def __init__(self, **kwgs):
            self.__dict__.update(kwgs)

    my_app_config = Config(**{
        'dms_host': 'mqtt.dms.aodianyun.com',
        'dms_port': 1883,
        'topic_api': 'http://my.app/api/RoomMgr/getDmsList',
    })

    my_app = DmsAnalysis(my_app_config.dms_host, my_app_config.dms_port, my_app_config.topic_api, 10, 10)
    atexit.register(my_app.close)
    my_app.run()


if __name__ == '__main__':
    main()