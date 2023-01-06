### Robot Client

To run the robot client one has to run the following script in terminal in this folder:

```commandline
cd IOT_ASSIGNMENT_2/PROJECT/RobotClient
python3 RobotClient.py
```

RobotCLient is using wrappers created for communication with ROS. One has to have this computer connected to robot CNC
unit via Ethernet cable and ROS Noetic runnning with all the packages for UR5e robot.

Driver Used: https://github.com/UniversalRobots/Universal_Robots_ROS_Driver

### position_generator

The position_generator was used to save various positions of the robot
for programming where it was supposed to go

### Movement Wrapper

The movement wrapper simplies sending the robot movement commands

### Robot Control

The robot control script contains all the code for controlling the
robot for connect4 tasks
