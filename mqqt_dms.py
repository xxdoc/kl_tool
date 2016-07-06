import paho.mqtt.client as mqtt
import requests
import json

class DmsAnalysis(object):

    def __init__(self, dms_host, dms_port, topic_api, topic_timer=10, nums_timer=10):
        self.dms_host = dms_host
        self.dms_port = dms_port
        self.topic_api = topic_api
        self.topic_timer = topic_timer
        self.nums_timer = nums_timer

        self.dms_config = self.get_dms_config()
        self.dms_list = {}

    def get_dms_config(self):
        tmp = {}
        try:
            tmp = requests.get(self.topic_api).json()
        except Exception as ex:
            pass
        return tmp

    def init_dms_client(self, pub_key, sub_key, topic_list):
        # The callback for when the client receives a CONNACK response from the server.
        def on_connect(client, userdata, flags, rc):
            print("Connected with result code "+str(rc))
            # Subscribing in on_connect() means that if we lose the connection and
            # reconnect then subscriptions will be renewed.
            for topic in topic_list:
                client.subscribe(topic)

        # The callback for when a PUBLISH message is received from the server.
        def on_message(client, userdata, msg):
            print client,userdata,msg
            print msg.topic+" " + msg.payload.decode('utf-8', 'ignore' )

        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        client.username_pw_set(pub_key , sub_key)
        client.connect(self.dms_host, self.dms_port, 60)
        client.topic_list = topic_list
        return client

    def run(self):
        for admin_item in self.dms_config:
            admin_id = int(admin_item.get('admin_id', 0))
            if admin_id<=0:
                continue
            self.dms_list[admin_id] = self.init_dms_client(admin_item['dms_pub_key'], admin_item['dms_sub_key'], admin_item['topic'])

        for admin_id, dms_item in self.dms_list.items():
            dms_item.loop_start()


def main():
    my_app_config = Config(**{
        'dms_host': 'mqtt.dms.aodianyun.com',
        'dms_port': 1883,
        'topic_api': 'http://my.app/api/RoomMgr/getDmsList',
    })

    my_app = DmsAnalysis(my_app_config.dms_host, my_app_config.dms_port, my_app_config.topic_api, 10, 10)
    my_app.run()

class Config(object):
    def __init__(self, **kwgs):
        self.__dict__.update(kwgs)


if __name__ == '__main__':
    main()



