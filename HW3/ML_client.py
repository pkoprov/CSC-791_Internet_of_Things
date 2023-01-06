import numpy as np
import paho.mqtt.client as mqtt
import pandas as pd
import pickle
import time
import warnings


def on_connect(client, userdata, flags, rc):
    client.publish("fwh2200/c10/STATUS/MLmodel", "online", retain=True, qos=1)
    print("Connected to Broker")


def on_disconnect(self, client, userdata):
    client.publish("fwh2200/c10/STATUS/MLmodel", "offline", retain=True, qos=1)
    print("Disconnected from Broker")


def preprocess(event):
    column_name = []
    # Set the number of intervals in which to sclice the dataset
    sliceNumber = 10
    for i in range(sliceNumber):
        for coord in [f"X{i + 1}a", f"Z{i + 1}a", f"Y{i + 1}g"]:
            column_name.append(coord)

    doorEvent_df = pd.DataFrame(event, columns=["X (m/s^2)", "Z (m/s^2)", "Y (rad/s)"])
    split_array = np.array_split(doorEvent_df, sliceNumber)

    temp = []
    for i in split_array:
        for j in range(3):
            temp.append(i.mean()[j])

    data = pd.DataFrame(temp)
    return data


def prediction(data):
    global loaded_model
    y_pred = loaded_model.predict(data.transpose())
    return y_pred[0]


def on_message(client, userdata, message):
    global event, prev_time, fresh
    # print(message.payload.decode())
    if not fresh:
        fresh = True

    if message.topic == "fwh2200/c10/DDATA/esp32":
        prev_time = time.time()
        msg = message.payload.decode()
        l = msg.split(", ")
        l = list(map(float, l))
        event.append(l)


if __name__ == "__main__":
    client = mqtt.Client("MLmodel")
    print("Starting the MLmodel Client...")

    # broker_ip = "broker.hivemq.com"
    broker_ip = "broker.hivemq.com"

    client.connect(broker_ip, 1883)

    event = []
    prev_time = 0
    fresh = False

    client.subscribe("fwh2200/c10/DDATA/esp32", qos=2)

    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    time.sleep(0.25)
    client.loop_start()

    loaded_model = pickle.load(open("./finalized_model.sav", 'rb'))
    warnings.filterwarnings('ignore')

    while True:

        if time.time() - prev_time > 1 and fresh:
            data = preprocess(event)
            try:
                doorStatus = prediction(data)
            except ValueError as err:
                print(err)
                continue
            finally:
                event = []
                fresh = False
            client.publish("fwh2200/c10/STATUS/door", payload=doorStatus)
            print(doorStatus)
