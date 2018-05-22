import time
import os
import paho.mqtt.client as mqtt
import random

# Define Variables
MQTT_HOST = "mosquitto"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = int(os.environ['MQTT_KEEPALIVE_INTERVAL'])
MQTT_TOPIC = os.environ['MQTT_TOPIC']
MQTT_DELAY = 20
EDGE_HOST = os.environ['HOSTNAME']


def sensor_data():
    return random.random()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code {0}".format(str(rc)))
    mqttc.publish(MQTT_TOPIC, "{} has connected".format(EDGE_HOST))


def on_publish(client, userdata, mid):
    print("Message published ...")


def on_disconnect(client, userdata, rc):
    print("Client disconnected ...")


if __name__ == '__main__':
    # Initiate MQTT Client
    mqttc = mqtt.Client(EDGE_HOST)

    # Register callback functions
    mqttc.on_publish = on_publish
    mqttc.on_disconnect = on_disconnect
    mqttc.on_connect = on_connect

    # Connect with MQTT Broker
    mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)

    mqttc.loop_start()
    while True:
        # publish status
        mqttc.publish(
            "{}/status".format(MQTT_TOPIC),
            "{} is OK".format(EDGE_HOST))
        # publish sensor data
        mqttc.publish(
            "{}/sensor".format(MQTT_TOPIC),
            sensor_data())
        time.sleep(MQTT_DELAY)
