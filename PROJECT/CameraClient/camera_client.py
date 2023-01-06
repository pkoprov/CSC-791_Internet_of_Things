# This file will contain the mqtt code for communicating with the other clients in the system
# It will use the camera_processing.py file to get the current status of the board
# An image of the board should be saved when a game has been completed
# The following file contains the mqtt code, but needs to be integrated with camera_processing.py file.
# Currently the code can send dummy data to the topics on the online MQTT broker.

import cv2
import paho.mqtt.client as mqtt

import camera_processing


def on_message(client, userdata, message):
    print("received message: ", str(message.payload.decode("utf-8")))


if __name__ == "__main__":
    print("Starting Video Stream...")
    cap = cv2.VideoCapture(2)

    mqttBroker = "broker.hivemq.com"
    client = mqtt.Client("camera_client")
    client.will_set("camera_client/status", "offline", retain=True, qos=2)
    client.connect(mqttBroker)
    client.loop_start()
    resetOccurred = False
    emptyBoard = "#######\n" \
                 "#######\n" \
                 "#######\n" \
                 "#######\n" \
                 "#######\n" \
                 "#######\n"

    client.publish("camera_client/status", "online", retain=True, qos=2)
    client.publish("game_status", "board_reset", retain=False, qos=2)
    print("Camera Online!")
    print("Waiting for reset...")

    client.subscribe("game_status")
    client.on_message = on_message

    while True:

        ret, frame = cap.read()
        if not ret:
            print("No Image Found!")
            exit()

        data = camera_processing.generate_grid(frame)
        if data is not None:
            if data == "RESET":
                print("Reset Occured!\n")
                client.publish("camera_client/board_data",
                               emptyBoard, retain=True, qos=2)
                client.publish("camera_client/reset",
                               True, retain=True, qos=2)
                resetOccurred = True
            elif resetOccurred:
                print(data + "\n")
                client.publish("camera_client/reset",
                               False, retain=True, qos=2)
                client.publish("camera_client/board_data",
                               data, retain=True, qos=2)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    client.loop_stop()
    cap.release()
    cv2.destroyAllWindows()
