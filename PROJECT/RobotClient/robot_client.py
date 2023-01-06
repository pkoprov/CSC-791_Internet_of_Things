# The robot_client.py file will use MQTT to communicate with the other clients in the system
# It will receive messages for where the robot should place its pieces
# Author: Pavel Koprov <pkoprov@ncsu.edu>,


import paho.mqtt.client as mqtt
import time

from robot_control import Connect4Robot


# connect to broker and subscribe to topics
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Successfully connected to the broker!")
        client.publish("robot_client/status",
                       "online", retain=True, qos=2)
        client.message_callback_add(
            "robot_client/place_piece", place_piece)
        client.message_callback_add(
            "game_status", display_animation)
        client.subscribe("robot_client/#")
        client.subscribe("game_status")
        print("Successfully subscribed to topics!")
    else:
        print("Could not connect with rc=", rc)


# publish offline message to status topic before disconnecting
def power_off():
    client.publish("robot_client/status",
                   "offline", retain=True, qos=2)
    client.disconnect()
    print("Gracefully disconnected from the broker!")


# print messages that are out of specified topics
def on_message(clt, userdata, msg):
    print(
        f"Received a message in unknown topic '{msg.topic}' with payload '{msg.payload.decode()}'")


# place a piece depending on players input
def place_piece(clt, userdata, msg):
    global robot_move
    pyld = msg.payload.decode()
    print(f"Received a message in topic '{msg.topic}' with payload '{pyld}'")
    if pyld == "-1":
        return
    try:
        pyld = int(pyld)
        if not robot_move:
            client.publish("robot_client/moving", True, qos=2, retain=True)
            robot_move = True
            client.publish("robot_client/place_piece", -1, qos=2, retain=True)
            robot.place_piece(pyld)
            client.publish("robot_client/moving", False, qos=2, retain=True)
            robot_move = False
    except:
        print("Incorrect format of payload")


# show the animation depending on the game result
def display_animation(clt, userdata, msg):
    if msg.payload.decode() == "win":
        robot.robot_win()
        robot.reset_board()
    elif msg.payload.decode() == "lose":
        robot.robot_lost()
    elif msg.payload.decode() == "tie":
        robot.reset_board()
    elif msg.payload.decode() == "board_reset":
        robot.reset_board()


if __name__ == "__main__":

    robot = Connect4Robot()

    robot_move = False
    broker = "broker.hivemq.com"
    client = mqtt.Client("Robot_client")
    client.on_connect = on_connect
    client.on_message = on_message
    client.poweroff = power_off
    client.will_set("robot_client/status",
                    "offline", retain=True, qos=2)
    client.connect(broker, keepalive=20)
    client.loop_start()
    time.sleep(0.2)

    while True:

        if input("Press Q to stop\n").lower() == "q":
            client.poweroff()
            time.sleep(0.1)
            break

    print("This is the end...")
