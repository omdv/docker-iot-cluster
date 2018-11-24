import time
import os
import paho.mqtt.client as mqtt
import random
import logging
from json import dumps
from math import sin, pi
from datetime import datetime

# Define Variables
MQTT_HOST = "mosquitto"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = int(os.environ['MQTT_KEEPALIVE_INTERVAL'])
MQTT_TOPIC_PARENT = os.environ['MQTT_TOPIC_PREFIX']
MQTT_FREQUENCY = int(os.environ['MQTT_ACQ_FREQUENCY_SEC'])
EDGE_HOST = os.environ['HOSTNAME']


# initialize parameters for the internal sensor model
# we'll choose period so that there are sufficient points sent
def init_params():
    A = random.random() * 10
    B = 2 * pi / (MQTT_FREQUENCY * 10 * random.random())
    C = random.random() * 10
    D = random.random() * 10
    return [A, B, C, D]


def simulate_sensor(params):
    timestamp = datetime.now().timestamp()
    return params[0] * sin(params[1] * (timestamp + params[2])) + params[3]


def construct_payload(params):
    payload = {
        "deviceType": "edge",
        "deviceID": EDGE_HOST,
        "sensor": simulate_sensor(params)
    }
    return dumps(payload)


def on_connect(client, userdata, flags, rc):
    logging.info(client, userdata)
    logging.info("Connected with result code {0}".format(str(rc)))


def on_publish(client, userdata, mid):
    logging.debug("Message published ...")


def on_disconnect(client, userdata, rc):
    logging.info("Client disconnected ...")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    # initiate sensor parameters
    sensor_params = init_params()

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
        # publish sensor data
        mqttc.publish(
            "{}/{}".format(MQTT_TOPIC_PARENT, EDGE_HOST),
            construct_payload(sensor_params))
        # sleep
        time.sleep(MQTT_FREQUENCY)
