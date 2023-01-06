# This method was used to generate positios for the robot.
# Author: Thomas Batchelder

import json
import rospy
import time
# Import TrajectoryClient from movement_wrapper.py
from hashlib import new
from numpy import True_
from tkinter import Y

from movement_wrapper import TrajectoryClient

if __name__ == "__main__":
    # Create a new TrajectoryClient object
    traj_client = TrajectoryClient()
    # Get the current position of the robot
    current_pos = traj_client.get_current_position()
    current_pos_joint = traj_client.get_current_joint_positions()
    print("Current position: ", current_pos)
    print("Current joint position: ", current_pos_joint)

    # Read the current positions from a json file
    with open("/home/tjbatche/dev_ws/src/connect4_camera/positions.json", "r") as f:
        positions = json.load(f)

    type_pos = input("(t)rajectory or (j)oint position: ")
    if type_pos == "t":
        position_name = input("Enter position name: ")
        positions[position_name] = current_pos
    else:
        position_name = input("Enter position name: ")
        positions[position_name] = current_pos_joint

    # Write the current position to a json file
    with open("/home/tjbatche/dev_ws/src/connect4_camera/positions.json", "w") as f:
        json.dump(positions, f)
