# Import package
import paho.mqtt.client as mqtt

# Define Variables
MQTT_HOST = "mosquitto"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 45
MQTT_TOPIC = "omdv/fml"


def on_connect(client, userdata, flags, rc):
    print("Connected with result code {0}".format(str(rc)))
    client.subscribe(MQTT_TOPIC)
    # client.subscribe("$SYS/#")


def on_subscribe(mosq, obj, mid, qos):
    print("Subscribed: {}, {}, {}".format(obj, mid, qos))


def on_message(client, userdata, msg):
    print("Topic: {}, Message: {}".format(msg.topic, msg.payload))


if __name__ == '__main__':
    mqttc = mqtt.Client("federated_town")
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message
    mqttc.on_subscribe = on_subscribe

    mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
    mqttc.loop_forever()
