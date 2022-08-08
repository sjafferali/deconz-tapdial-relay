#!/usr/bin/env python3

from deconzpy import Router, Config
import time
import os
import paho.mqtt.client as mqtt
from datetime import datetime

MQTT_IP = os.getenv("MQTT_IP")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1833))
DECONZ_IP = os.getenv("DECONZ_IP")
DECONZ_TOKEN = os.getenv("DECONZ_TOKEN")


SWITCH_MAP = {
    "14": "home/livingroom/dial",
    "16": "home/bedroom/dial1",
}

def print_log(msg):
    now = datetime.now()
    dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
    print(f"{dt_string} {msg}")

def initConfig(ip, token):
    config = Config.Config("config.json")
    config.set("username", token)
    config.set("gatewayIP", ip)
    config.save()


def onChange(sensor, key_that_changed, oldval, newval):
    sensor_id = sensor.getId()
    entity_name = SWITCH_MAP[sensor_id]
    print_log(f"{entity_name}({sensor_id}) updated to {newval}")
    print_log(client.publish(entity_name, payload=newval, qos=1, retain=False))

def subscribe_to_sensors(deconz_client, sensors):
    for key in list(sensors):
        sensor = router.getSensor(key)
        #sensor.dump()
        sensor.subscribeToAttribute("state_expectedrotation", onChange)

if __name__ == "__main__":
    # create config
    initConfig(DECONZ_IP, DECONZ_TOKEN)

    # setup mqtt
    client = mqtt.Client()
    client.connect(MQTT_IP, MQTT_PORT, 60)
    
    # setup deconz
    router = Router()
    router.startAndRunThread()

    # subscribe to sensors
    subscribe_to_sensors(router, SWITCH_MAP.keys())

    while True:
        time.sleep(60)
