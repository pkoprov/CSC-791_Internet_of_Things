# This file contains the code for the controlling the robot. The robot_client only needs
# to construct a Connect4Robot and use the place_piece method to place the pieces.
# Author: Thomas Batchelder

import json
import rospy
import time

# Import TrajectoryClient from movement_wrapper.py
from movement_wrapper import TrajectoryClient
from robotiq_gripper import RobotiqGripper


class Connect4Robot:
    def __init__(self):
        self.traj_client = TrajectoryClient()
        self.gripper = RobotiqGripper()
        self.gripper.connect("192.168.10.16", 63352)
        if not self.gripper.is_active():
            self.gripper.activate()
        # Get the positions from a json file
        positions = {}
        with open("/home/tjbatche/dev_ws/src/connect4_camera/positions.json", "r") as f:
            positions = json.load(f)
        if positions == {}:
            print("No positions found")
            exit()
        self.mid_low_joint = positions["mid_low"]
        self.mid_high = positions["mid_high"]
        self.home = positions["home"]
        self.home_joint = positions["home_joint"]
        self.mid_high_joint = positions["mid_high_joint"]
        self.pickup = positions["pickup"]
        self.pickup_joint = positions["pickup_joint"]
        self.drop1 = positions["drop1"]
        self.drop2 = positions["drop2"]
        self.drop3 = positions["drop3"]
        self.drop4 = positions["drop4"]
        self.drop5 = positions["drop5"]
        self.drop6 = positions["drop6"]
        self.drop7 = positions["drop7"]
        self.home_right = positions["home_right"]
        self.home_left = positions["home_left"]

        self.reset_top = positions["reset_top"]
        self.reset1 = positions["reset1"]
        self.reset2 = positions["reset2"]
        self.reset3 = positions["reset3"]
        self.reset4 = positions["reset4"]
        self.reset5 = positions["reset5"]
        self.reset6 = positions["reset6"]

        self.win1 = positions["win1"]
        self.win2 = positions["win2"]
        self.win3 = positions["win3"]
        self.win4 = positions["win4"]

        self.lose1 = positions["lose1"]
        self.lose2 = positions["lose2"]
        self.lose3 = positions["lose3"]
        self.lose4 = positions["lose4"]

        self.drop_positions = [self.drop1, self.drop2, self.drop3,
                               self.drop4, self.drop5, self.drop6, self.drop7]

        # self.traj_client.send_joint_trajectory(
        #     [self.mid_low_joint, self.mid_high_joint, self.home_joint], [1.0, 2.0, 3.0], True)

    def __pickup_piece(self):
        self.traj_client.send_joint_trajectory(
            [self.home_joint, self.mid_high_joint, self.mid_low_joint, self.pickup_joint], [
                0.8, 1.5, 2.4, 2.75], True)
        self.gripper.move_and_wait_for_pos(255, 255, 20)
        self.traj_client.send_joint_trajectory(
            [self.mid_low_joint, self.mid_high_joint, self.home_joint], [0.4, 1.5, 2.25], True)

    def reset_board(self):
        self.gripper.move_and_wait_for_pos(255, 255, 20)
        self.traj_client.send_cartesion_point(self.reset_top, 1.0, True)
        self.traj_client.send_cartesion_point(self.reset1, 1.0, True)
        self.traj_client.send_cartesion_point(self.reset2, 0.5, True)
        self.traj_client.send_cartesion_point(self.reset3, 0.5, True)
        self.traj_client.send_cartesion_point(self.reset4, 0.5, True)
        self.traj_client.send_cartesion_point(self.reset5, 0.5, True)
        self.traj_client.send_cartesion_point(self.reset6, 0.5, True)
        self.traj_client.send_cartesion_point(self.reset_top, 1.0, True)
        self.traj_client.send_cartesion_point(self.home, 1.0, True)
        self.gripper.move_and_wait_for_pos(0, 255, 20)
        print("Reset board")

    def robot_win(self):
        self.traj_client.send_joint_trajectory(
            [self.win1, self.win2, self.win3, self.win1, self.win4, self.win1, self.home_joint], [
                2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 9.0], True)

    def robot_lost(self):
        self.traj_client.send_cartesion_point(self.lose1, 0.75, True)
        self.traj_client.send_cartesion_point(self.lose2, 0.75, True)
        self.gripper.move_and_wait_for_pos(255, 255, 20)
        self.traj_client.send_cartesian_trajectory(
            [self.lose3, self.lose4], [0.4, 0.6], False)
        time.sleep(0.45)
        self.gripper.move_and_wait_for_pos(0, 255, 20)
        self.traj_client.send_cartesion_point(self.lose4, 0.75, False)
        self.traj_client.send_cartesion_point(self.home, 0.75, True)

    def place_piece(self, position):
        # If position is a string ignore it
        if isinstance(position, str):
            return
        if position < 0 or position >= 7:
            print("Invalid position")
            exit()
        print("Placing piece at position: " + str(position))
        self.__pickup_piece()
        if position <= 2:
            self.traj_client.send_cartesian_trajectory(
                [self.home_left], [1.0], True)
            self.traj_client.send_cartesion_point(
                self.drop_positions[position], 0.6, True)
        elif position == 3:
            self.traj_client.send_cartesion_point(
                self.drop_positions[position], 2.5, True)
        elif position >= 4:
            self.traj_client.send_cartesian_trajectory(
                [self.home_right], [1.0], True)
            self.traj_client.send_cartesion_point(
                self.drop_positions[position], 0.6, True)
        self.gripper.move_and_wait_for_pos(0, 255, 20)
        self.traj_client.send_cartesion_point(self.home, 0.5, True)


if __name__ == "__main__":
    robot = Connect4Robot()
    # robot.robot_lost()
    robot.robot_win()
    robot.reset_board()
