# This MQTT subscriber will subscribe to the topic "MQTT-Data" recorded
# the amount of time is takes to transfer the files.

import numpy as np
import paho.mqtt.client as mqtt
import time

messageRecievedTime = []
start_time = time.time()
file_count = 0
messageCount = 0

file_to_size = {10000: 100, 1000: 10000, 100: 1000000, 10: 10000000}


def on_message(client, userdata, message):
    global messageRecievedTime, messageCount, start_time, file_count
    if message.topic == "Start-Time":
        start_time = float(message.payload.decode())
        print("Start time: \t\t", start_time, "\n")
        messageCount = 0
    elif message.topic == "File-Count":
        files = int(message.payload.decode())
        print("Expected File Count: \t", files)
        file_count = files
    elif message.topic == "QoS-Type":
        qos = int(message.payload.decode())
        print("\nQoS Level: \t\t", qos)
        client.unsubscribe("MQTT-Data")
        client.subscribe("MQTT-Data", qos=qos)
    else:
        messageCount += 1
        messageRecievedTime.append(time.time() - start_time)
        if messageCount == file_count:
            finish_time = time.time()
            print("\n===============================================================")
            print("Total Time: \t\t", finish_time - start_time, " Seconds")
            # Calculate the time bewteen each message
            time_between_messages = []
            for i in range(len(messageRecievedTime) - 1):
                time_between_messages.append(
                    messageRecievedTime[i + 1] - messageRecievedTime[i]
                )
            print(
                "Average Time: \t\t",
                sum(time_between_messages) / len(time_between_messages),
                " Seconds",
            )
            # Calculate the standard deviation using numpy
            print(
                "Standard Deviation: \t",
                np.std(time_between_messages),
                " Seconds",
            )
            # Caclulate the kilobits per second for each file
            # and save it to a list
            kbps = []
            for i in range(len(time_between_messages)):
                try:
                    kbps.append(
                        (file_to_size[file_count] * 8 / time_between_messages[i])
                        / 1000
                    )
                except ZeroDivisionError:
                    pass
            print("Average Kbps: \t\t", sum(kbps) / len(kbps), " Kbps")
            print("Standard Deviation: \t", np.std(kbps), " Kbps")

            print("===============================================================")
            print("\n")
            print("Waiting for messages...")
        elif messageCount <= file_count:
            print(
                "Received message!"
                + " Topic: '"
                + message.topic
                + "' QoS: "
                + str(message.qos)
                + ", Message Time: "
                + str(message.timestamp)
                + ", Count "
                + str(messageCount)
                + ", Total Time: "
                + str(time.time() - start_time)
            )


# IP address of the MQTT broker
mqttBroker = "192.168.10.31"
# Create a client instance
client = mqtt.Client("MQTT-Subscriber")
client.on_message = on_message
inflight = 1
client.max_inflight_messages_set(inflight)
# Connect to the MQTT broker
client.connect(mqttBroker)

# Subscribe to the topic "MQTT-Data"
client.subscribe("Start-Time", qos=1)
client.subscribe("File-Count", qos=1)
client.subscribe("QoS-Type", qos=1)
client.subscribe("MQTT-Data", qos=1)
print("Subscribed to topic MQTT-Data")
print("Waiting for messages...")
client.loop_forever()
