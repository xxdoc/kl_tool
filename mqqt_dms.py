import paho.mqtt.client as mqtt


DMS_HOST = 'mqtt.dms.aodianyun.com'
DMS_PORT = 1883
DMS_PUB_KEY = 'pub_665ef75d204a063f72d8afd1f19cf8a2'
DMS_SUB_KEY = 'sub_6df54a1221f517e1b11efd72e795301c'
DMS_TOPIC_LIST = ['chat_97', '__present__chat_97']

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    for topic in DMS_TOPIC_LIST:
        client.subscribe(topic)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print client,userdata,msg
    print msg.topic+" " + msg.payload.decode('utf-8', 'ignore' )

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(DMS_PUB_KEY , DMS_SUB_KEY)
client.connect(DMS_HOST, DMS_PORT, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()