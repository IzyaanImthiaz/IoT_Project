import time
import paho.mqtt.client as paho
from paho import mqtt
from Config import *

def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

def on_publish(client, userdata, mid, properties=None):
    print("Published mid: " + str(mid))
    
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect
client.connect(mqtt_broker, mqtt_port)
client.on_publish = on_publish

def SendData(topic, data):
    print("Publishing MQTT Data...")
    print("Publishing: " + str(topic) + " to " + str(data))
    client.publish(topic, payload=data)
    print("Publishing MQTT Data Done...")

