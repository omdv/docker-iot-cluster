import os
import logging
from json import loads
import paho.mqtt.client as mqtt
from datetime import datetime
from influxdb import InfluxDBClient

# MQTT params
MQTT_HOST = "mosquitto"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = int(os.environ['MQTT_KEEPALIVE_INTERVAL'])
MQTT_TOPIC_PARENT = os.environ['MQTT_TOPIC_PREFIX']

# INFLUX params
INFLUX_HOST = "influxdb"
INFLUX_PORT = 8086
INFLUX_DB = os.environ['INFLUXDB_DB']

# connect to influx
influx = InfluxDBClient(
    host=INFLUX_HOST,
    port=INFLUX_PORT,
    database=INFLUX_DB)


def save_to_influx(msg):
    payload = loads(msg.payload)
    data = [{
        "measurement": "edge",
        "tags": {
            "host": payload["deviceID"]
        },
        "time": datetime.utcnow().isoformat(),
        "fields": {
            "sensor": payload["sensor"]
        }
    }]
    logging.debug(data)
    influx.write_points(data)


def on_connect(client, userdata, flags, rc):
    logging.info("Connected with result code {0}".format(str(rc)))
    client.subscribe("{}/#".format(MQTT_TOPIC_PARENT))


def on_subscribe(mosq, obj, mid, qos):
    logging.info("Subscribed: {}, {}, {}".format(obj, mid, qos))


def on_message(client, userdata, msg):
    logging.debug("Topic: {}, Message: {}".format(msg.topic, msg.payload))
    save_to_influx(msg)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    # create mqtt client
    mqttc = mqtt.Client("hub")
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message
    mqttc.on_subscribe = on_subscribe

    mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
    mqttc.loop_forever()
