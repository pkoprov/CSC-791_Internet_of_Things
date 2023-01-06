import logging
import os
import paho.mqtt.client as mqtt
import psutil
import sys
import threading
import time
from resource import prlimit
from turtle import update

import connect4
from ui import Connect4UI


def restart_program():
    """Restarts the current program, with file objects and descriptors
       cleanup
    """

    try:
        p = psutil.Process(os.getpid())
        for handler in p.get_open_files() + p.connections():
            os.close(handler.fd)
    except Exception:
        logging.error(Exception)

    python = sys.executable
    os.execl(python, python, *sys.argv)


def on_connect(client, userdata, flags, rc):
    print("Connected to Broker")


def on_disconnect(self, client, userdata):
    print("Disconnected from Broker")


def on_message(client, userdata, message):
    global board, camera_client_status, robot_client_status, robot_moving, reset, gameOver, column

    if message.topic == "robot_client/status":
        msg = message.payload.decode()
        robot_client_status = msg.lower()

    if message.topic == "camera_client/status":
        msg = message.payload.decode()
        camera_client_status = msg.lower()

    if message.topic == "robot_client/moving":
        msg = message.payload.decode()
        if msg == "True":
            robot_moving = True
        elif msg == "False":
            robot_moving = False

    if message.topic == "camera_client/board_data":
        board = connect4.construct_board(message.payload.decode())

    if message.topic == "robot_client/place_piece":
        if message.payload.decode() == "-1":
            column = -1

    if message.topic == "game_status":
        if message.payload == "win" or message.payload == "lose":
            print("New game should begain")

        client.publish("game_status", 0, retain=True, qos=2)

    if message.topic == "reset":
        msg = message.payload.decode()
        if msg == "True":
            reset = True


if __name__ == "__main__":

    client = mqtt.Client("PlayerClientConnect4")
    print("Starting the Player Client...")

    broker_ip = "broker.hivemq.com"
    # broker_ip = "localhost"
    client.connect(broker_ip, 1883)

    global board, gameOver, camera_client_status, robot_client_status, reset, column
    board = [[]]
    gameOver = False
    camera_client_status = "offline"
    robot_client_status = "offline"
    robot_moving = False
    reset = False
    column = -1

    client.subscribe("robot_client/status", qos=2)
    client.subscribe("robot_client/moving", qos=2)
    client.subscribe("robot_client/place_piece", qos=2)
    client.subscribe("camera_client/status", qos=2)
    client.subscribe("camera_client/board_data", qos=2)
    client.subscribe("reset", qos=2)
    client.subscribe("game_status", qos=2)

    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    client.loop_start()

    time.sleep(1.0)

    while True:
        if camera_client_status == "online" and robot_client_status == "online" and reset and connect4.checkForEmpty(
                board):
            print("\n==========================")
            print("    Starting new game")
            print("==========================\n")
            break
        else:
            print("Waiting for clients to be ready...")
            print("Camera Client Status: ", camera_client_status)
            print("Robot Client Status:  ", robot_client_status)
            print("Reset:                ", reset)
            print("Board Empty:          ", connect4.checkForEmpty(board))
            print()
            if not connect4.checkForEmpty(board):
                client.publish("game_status", "board_reset",
                               retain=True, qos=2)
            time.sleep(10.0)

    ui = Connect4UI()

    while not gameOver:
        if column == -1 and not robot_moving:

            current_board = board
            ui.new_board(board)
            ui.update_board()
            gameOver, winner = connect4.checkVictory(board)
            if gameOver and winner == 1:
                client.publish("game_status", "lose", qos=2)
                break
            elif gameOver and winner == 2:
                client.publish("game_status", "win", qos=2)
                break

            red_pieces = connect4.calculateNumberOfRedPieces(board)
            yellow_pieces = connect4.calculateNumberOfYellowPieces(board)

            ui.display_message("Waiting for opponent...")
            while yellow_pieces + 1 != connect4.calculateNumberOfYellowPieces(board):
                pass
            ui.new_board(board)
            ui.update_board()

            gameOver, winner = connect4.checkVictory(board)
            if gameOver and winner == 1:
                client.publish("game_status", "lose", qos=2)
                break
            elif gameOver and winner == 2:
                client.publish("game_status", "win", qos=2)
                break

            ui.display_message("Your turn!")
            connect4.printBoard(board)
            ui.new_board(board)
            current_board = board
            column = -1
            print("Waiting for input...")
            while column == -1:
                column = ui.update_board()
            client.publish("robot_client/place_piece", column, qos=2)
            gameOver, winner = connect4.checkVictory(board)
            if gameOver and winner == 1:
                client.publish("game_status", "lose", qos=2)
                break
            elif gameOver and winner == 2:
                client.publish("game_status", "win", qos=2)
                break

            ui.display_message("Placing piece in column: " + str(column + 1))
            time.sleep(2.0)

            while robot_moving or current_board == board or red_pieces + 1 != connect4.calculateNumberOfRedPieces(
                    board):
                pass
    print("Restarting...")
    time.sleep(1.0)
    # restart_program()
