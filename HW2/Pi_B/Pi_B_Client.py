# Author: Rachana Kondabala <rkondab@ncsu.edu>

import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import time

LED1 = 17  # green - LightStatus
LED2 = 27  # red - Status/RaspberryPiA
LED3 = 22  # yellow - Status/RaspberryPiC
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)
GPIO.setup(LED3, GPIO.OUT)
signal = None


def on_message(client, userdata, message):
    # This function is called everytime the subscribed topic receives a message
    global signal
    print(message.topic, message.payload.decode())
    if message.topic == "LightStatus" and signal is None:
        signal = str(message.payload.decode())
        if signal == "TurnOn":
            GPIO.output(LED1, GPIO.HIGH)
        elif signal == "TurnOff":
            GPIO.output(LED1, GPIO.LOW)
        else:
            GPIO.output(LED1, GPIO.LOW)

    elif message.topic == "Status/RaspberryPiA":
        signal = message.payload.decode().lower()
        if signal == "online":
            GPIO.output(LED2, GPIO.HIGH)
        elif signal == "offline":
            GPIO.output(LED2, GPIO.LOW)
    elif message.topic == "Status/RaspberryPiC":
        signal = message.payload.decode().lower()
        if signal == "online":
            GPIO.output(LED3, GPIO.HIGH)
        elif signal == "offline":
            GPIO.output(LED3, GPIO.LOW)
            GPIO.output(LED1, GPIO.LOW)


def on_connect(client, userdata, flags, rc):
    # This function is called everytime the client connects to the broker
    print("Connected to Broker")


if __name__ == "__main__":
    print("Starting the Pi B client...")
    broker_ip = input("Enter Broker IP Address: ")
    # Create a client instance
    client = mqtt.Client("RaspberryPiB")
    client.on_message = on_message
    client.on_connect = on_connect
    # Connect to the MQTT broker
    client.connect(broker_ip, keepalive=1)
    # Subscribe to the three topics
    client.subscribe("LightStatus", qos=2)
    client.subscribe("Status/RaspberryPiA", qos=2)
    client.subscribe("Status/RaspberryPiC", qos=2)

    print("Subscribed to topics")
    print("Waiting for messages...")
    time.sleep(0.25)
    client.loop_start()
    input("Press 'Enter' to exit: ")
    client.loop_stop()
    client.disconnect()
