# Overview
Docker compose cluster simulating IoT network with edge devices communicating via MQTT protocol. Includes Node-RED and Node-RED dashboard.

# Features
- slim containers
- mosquitto broker
- Node-RED with dashboard

# Instructions
To start a cluster with 3 edge devices: `docker-compose up -d --build --scale edge=3`

This will expose the following ports:
- Node-RED: 1880 (add /ui for dashboard)
- MQTT broker: 1883 (for use with mqtt-spy and a like)

# Node-RED
Open Node Red dashboard on `localhost:1880`. Import the following snippet as clipboard to create a sample chart. Deploy and open `localhost:1880/ui`.

```
[{"id":"6e64eb6.c882f14","type":"mqtt in","z":"69ea0e6c.67f028","name":"","topic":"iot/sensor","qos":"2","broker":"ea2b7a21.6fdc58","x":190,"y":140,"wires":[["69aebdc0.3a1ee4"]]},{"id":"69aebdc0.3a1ee4","type":"ui_chart","z":"69ea0e6c.67f028","name":"","group":"3298de50.ab0ff2","order":0,"width":0,"height":0,"label":"chart","chartType":"line","legend":"false","xformat":"HH:mm:ss","interpolate":"linear","nodata":"","dot":false,"ymin":"","ymax":"","removeOlder":1,"removeOlderPoints":"","removeOlderUnit":"3600","cutout":0,"useOneColor":false,"colors":["#1F77B4","#AEC7E8","#FF7F0E","#2CA02C","#98DF8A","#D62728","#FF9896","#9467BD","#C5B0D5"],"useOldStyle":false,"x":370,"y":140,"wires":[[],[]]},{"id":"ea2b7a21.6fdc58","type":"mqtt-broker","z":"","name":"mqtt","broker":"mosquitto","port":"1883","clientid":"","usetls":false,"compatmode":true,"keepalive":"60","cleansession":true,"birthTopic":"","birthQos":"0","birthRetain":"false","birthPayload":"","closeTopic":"","closeQos":"0","closeRetain":"false","closePayload":"","willTopic":"","willQos":"0","willRetain":"false","willPayload":""},{"id":"3298de50.ab0ff2","type":"ui_group","z":"","name":"Default","tab":"e668c41d.f4063","disp":true,"width":"6","collapse":false},{"id":"e668c41d.f4063","type":"ui_tab","z":"","name":"Home","icon":"dashboard"}]
```