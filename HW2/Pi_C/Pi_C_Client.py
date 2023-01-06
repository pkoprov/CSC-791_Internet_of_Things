# Author: Rishi Patel <rapate26@ncsu.edu>
import paho.mqtt.client as mqtt
import time


def compare(lightSensor, threshold, message):
    # Compare the light sensor value with the threshold value
    # to determine if the light should be turned on or off
    global lightStatus_previous

    lightStatus = "TurnOn" if lightSensor >= threshold else "TurnOff"
    if lightStatus != lightStatus_previous:
        if lightSensor >= threshold:
            client.publish("LightStatus", "TurnOn", qos=2, retain=True)
        else:
            client.publish("LightStatus", "TurnOff", qos=2, retain=True)
    print("Topic: ", message.topic, " Message: ", message.payload.decode())
    print("Threshold: ", threshold, "LightSensor: ",
          lightSensor, "light Status: ", lightStatus)
    lightStatus_previous = lightStatus


def on_connect(client, userdata, flags, rc):
    print("Connected to Broker")
    client.publish("Status/RaspberryPiC", payload="online", qos=2, retain=True)


def on_disconnect(self, client, userdata, rc):
    client.publish("Status/RaspberryPiC",
                   payload="offline", qos=2, retain=True)
    print("Disconnected from Broker")


def on_message(client, userdata, message):
    global lightStatus, threshold, lightSensor, lightStatus_previous

    topic = message.topic
    msg = message.payload.decode()

    if topic == "lightSensor":
        lightSensor = int(msg)
        compare(lightSensor, threshold, message)

    elif topic == 'threshold':
        threshold = int(msg)
        compare(lightSensor, threshold, message)

    elif topic == "LightStatus":
        lightStatus = msg
        print("Change in light Status: Previous status:",
              lightStatus_previous, "; New Status:", lightStatus)

    else:
        print("Topic is not known")

    print("---------------")


if __name__ == "__main__":
    client = mqtt.Client("RaspberryPiC")
    print("Starting the Pi C client...")
    broker_ip = input("Enter Broker IP Address: ")

    client.will_set("Status/RaspberryPiC", "offline", qos=2, retain=True)

    lightStatus_previous = "TurnOff"
    lightStatus = "TurnOff"
    lightSensor = 0
    threshold = 0

    client.connect(broker_ip, 1883, keepalive=1)

    client.subscribe("lightSensor", qos=2)
    client.subscribe('threshold', qos=2)
    client.subscribe('LightStatus', qos=2)

    client.on_connect = on_connect
    client.on_message = on_message

    time.sleep(0.25)
    client.loop_start()
    input("Press 'Enter' to exit: ")
    client.loop_stop()
    client.disconnect()
