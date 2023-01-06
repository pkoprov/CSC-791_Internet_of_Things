import paho.mqtt.client as mqtt
import os
import time

# IP address of the MQTT broker
mqttBroker = "192.168.10.31"
# Create a client instance
client = mqtt.Client("MQTT-Publisher")
# Connect to the MQTT broker
client.connect(mqttBroker)


callbacks_received = []
wait = False

# On publish message function
def on_publish(client, userdata, mid):
    global callbacks_received, wait
    print("Published message with mid: " + str(mid))
    callbacks_received.remove(mid)
    wait = False


client.on_publish = on_publish

# Get the absolute path of the file
filePath = os.path.abspath(__file__)
# Move the file path to the parent directory twice
filePath = os.path.dirname(os.path.dirname(filePath))
# Print the file path
print("File path: " + filePath)

# Set the number of inflight messages to 10000
inflight = 100
client.max_inflight_messages_set(inflight)


# Locations of all the data files ordered from smallest to largest
dataFiles = [
    "/DataFiles/100B",
    "/DataFiles/10KB",
    "/DataFiles/1MB",
    "/DataFiles/10MB",
]

# file send amounts
fileSendAmounts = [10000, 1000, 100, 10]

while True:

    # Get user input for which data file to publish
    print("Please enter the number of the data file you would like to publish:")
    print("1. 100B")
    print("2. 10KB")
    print("3. 1MB")
    print("4. 10MB")
    print("5. Stop")
    userInput = int(input("Enter your choice: "))
    # Create a switch case for the data file
    if userInput == 1:
        dataFile = filePath + dataFiles[0]
        sendAmount = fileSendAmounts[0]
    elif userInput == 2:
        dataFile = filePath + dataFiles[1]
        sendAmount = fileSendAmounts[1]
    elif userInput == 3:
        dataFile = filePath + dataFiles[2]
        sendAmount = fileSendAmounts[2]
    elif userInput == 4:
        dataFile = filePath + dataFiles[3]
        sendAmount = fileSendAmounts[3]
    elif userInput == 5:
        print("Stopping...")
        # disconnect the client
        client.disconnect()
        print("Disconnected")
        print("Goodbye!")
        break

    qos = int(input("Type QoS level (1/2): "))
    client.loop_start()
    # publish the data file continuously as fast as possible
    with open(dataFile, "rb") as f:
        data = f.read()
        if not data:
            print("No more data to publish")
        else:
            print("Publishing data file...")
            mid_qos = client.publish("QoS-Type", qos, qos=1)
            mid_count = client.publish("File-Count", sendAmount, qos=1)
            mid_start = client.publish("Start-Time", time.time(), qos=1)
            callbacks_received.append(mid_qos[1])
            callbacks_received.append(mid_count[1])
            callbacks_received.append(mid_start[1])

            for i in range(sendAmount):
                wait = True
                mid = client.publish(
                    "MQTT-Data", payload=bytes(data), qos=qos, retain=True
                )
                callbacks_received.append(mid[1])
                # while wait:
                #     pass
            while len(callbacks_received) != 0:
                pass
            print("Published data files!\n")
