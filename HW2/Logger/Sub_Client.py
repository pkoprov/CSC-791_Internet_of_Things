# Author: Sajal Kaushik <skaushi2@ncsu.edu>
# This MQTT subscriber will subscribe to the topic "MQTT-Data" recorded
# the amount of time is takes to transfer the files.

import os
import paho.mqtt.client as mqtt
import time
from datetime import datetime


def on_message(client, userdata, message):
    global log
    Timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S %p")
    if message.topic == "Status/RaspberryPiA":
        status = message.payload.decode()
        print("Timestamp is {}   Status/RaspberryPiA is {} \t".format(Timestamp, status))

    elif message.topic == "threshold":
        threshold = message.payload.decode()
        print("Timestamp is {}   Threshold is {} \t".format(Timestamp, threshold))
    elif message.topic == "lightSensor":
        lightsensor = message.payload.decode()
        print("Timestamp is {}   lightSensor is {} \t".format(Timestamp, lightsensor))
    elif message.topic == "Status/RaspberryPiC":
        picstatus = message.payload.decode()
        print("Timestamp is {}   Status/RaspberryPiC is {} \t".format(Timestamp, picstatus))
    elif message.topic == "LightStatus":
        LightStatus = message.payload.decode()
        status = "{}, {}\n".format(Timestamp, LightStatus)
        with open("log.csv", "a") as file:
            file.write(status)
        print("Timestamp is {}   LightStatus is {}\t".format(Timestamp, LightStatus))


if not os.path.isfile("./log.csv"):
    with open("log.csv", "w") as file:
        file.write("Timestamp, LightStatus\n")

# IP address of the MQTT broker
broker_ip = input("Enter Broker IP Address: ")
# Create a client instance
client = mqtt.Client("Laptop #2")
client.on_message = on_message
# Connect to the MQTT broker
client.connect(broker_ip, 1883)
client.subscribe("lightSensor", qos=2)
client.subscribe("Status/RaspberryPiA", qos=2)
client.subscribe("threshold", qos=2)
client.subscribe("Status/RaspberryPiC", qos=2)
client.subscribe("LightStatus", qos=2)
time.sleep(0.25)
client.loop_start()
input("Press 'Enter' to exit: ")
client.loop_stop()
client.disconnect()
