import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print("Connected to Broker")


def on_disconnect(self, client, userdata):
    print("Disconnected from Broker")


def on_message(client, userdata, message):
    print(message.topic, message.payload)


ID = input("Type client name\n")
client = mqtt.Client(ID)
print(f"Starting the {ID} Client...")

broker_ip = "broker.hivemq.com"

client.connect(broker_ip, 1883)
topic = "fwh2200/c10/STATUS/door"
client.subscribe(topic, qos=2)
print("Subscribed to", topic)

client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

client.loop_start()
input("Press 'Enter' to exit: ")
client.loop_stop()
client.disconnect()
