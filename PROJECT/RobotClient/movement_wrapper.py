# This file contains all of the ROS code for sending movement commands to the robot.
# Author: Thomas Batchelder


import actionlib
import geometry_msgs.msg as geometry_msgs
import rospy
import sys
import time
from cartesian_control_msgs.msg import (
    FollowCartesianTrajectoryAction,
    FollowCartesianTrajectoryGoal,
    CartesianTrajectoryPoint,
)
from control_msgs.msg import FollowJointTrajectoryAction, FollowJointTrajectoryGoal
from controller_manager_msgs.srv import LoadControllerRequest, LoadController
from controller_manager_msgs.srv import SwitchControllerRequest, SwitchController
from geometry_msgs.msg import Twist
from scipy.spatial.transform import Rotation
from sensor_msgs.msg import JointState
from tf2_msgs.msg import TFMessage
from trajectory_msgs.msg import JointTrajectoryPoint

# If your robot description is created with a tf_prefix, those would have to be adapted
JOINT_NAMES = [
    "shoulder_pan_joint",
    "shoulder_lift_joint",
    "elbow_joint",
    "wrist_1_joint",
    "wrist_2_joint",
    "wrist_3_joint",
]

# All of those controllers can be used to execute joint-based trajectories.
# The scaled versions should be preferred over the non-scaled versions.
JOINT_TRAJECTORY_CONTROLLERS = [
    "scaled_pos_joint_traj_controller",
    "scaled_vel_joint_traj_controller",
    "pos_joint_traj_controller",
    "vel_joint_traj_controller",
    "forward_joint_traj_controller",
]

# All of those controllers can be used to execute Cartesian trajectories.
# The scaled versions should be preferred over the non-scaled versions.
CARTESIAN_TRAJECTORY_CONTROLLERS = [
    "pose_based_cartesian_traj_controller",
    "joint_based_cartesian_traj_controller",
    "forward_cartesian_traj_controller",
]

# We'll have to make sure that none of these controllers are running, as they will
# be conflicting with the joint trajectory controllers
OTHER_CONTROLLERS = ["joint_group_vel_controller", "twist_controller"]


class TrajectoryClient:
    """Small trajectory client to test a joint trajectory"""

    def __init__(self):
        # Start a subscriber to the /tf topic to get the current position of the robot
        self.cart_pos = {'x': 0, 'y': 0, 'z': 0}
        self.cart_orient = {'x': 0, 'y': 0, 'z': 0, 'w': 0}
        self.joint_positions = []
        self.tf = rospy.Subscriber(
            "/tf", TFMessage, self.update_cartesian_position)
        self.pub = rospy.Publisher(
            'twist_controller/command', Twist, queue_size=10)
        self.joint_states = rospy.Subscriber(
            "/joint_states", JointState, self.update_joint_positions)
        rospy.init_node("movement_wrapper")
        rospy.loginfo("Initializing UR Driver...")

        timeout = rospy.Duration(5)
        self.switch_srv = rospy.ServiceProxy(
            "controller_manager/switch_controller", SwitchController
        )
        self.load_srv = rospy.ServiceProxy(
            "controller_manager/load_controller", LoadController)
        try:
            self.switch_srv.wait_for_service(timeout.to_sec())
        except rospy.exceptions.ROSException as err:
            rospy.logerr(
                "Could not reach controller switch service. Msg: {}".format(err))
            sys.exit(-1)

        self.prev_movement = [[], []]
        self.prev_controller = None

        self.cartesian_trajectory_controller = CARTESIAN_TRAJECTORY_CONTROLLERS[2]
        self.joint_trajectory_controller = JOINT_TRAJECTORY_CONTROLLERS[0]
        # self.switch_controller(self.cartesian_trajectory_controller)
        self.trajectory_client = actionlib.SimpleActionClient(
            "{}/follow_cartesian_trajectory".format(
                self.cartesian_trajectory_controller),
            FollowCartesianTrajectoryAction,
        )
        time.sleep(0.5)
        rospy.loginfo("Complete!")

    def update_joint_positions(self, msg):
        self.joint_positions = msg.position

    def is_moving(self):
        """Checks if the robot is moving"""
        return self.trajectory_client.get_state() == actionlib.GoalStatus.ACTIVE

    def send_cartesion_point(self, point, duration, blocking=False):
        self.send_cartesian_trajectory([point], [duration], blocking)

    def send_cartesian_trajectory(self, point_list, duration_list, blocking=False):
        """Creates a Cartesian trajectory and sends it using the selected action server"""

        # Check if the data type for point_list is correct
        if not isinstance(point_list[0][1], list):
            if isinstance(point_list[0][1], dict):
                point_list_updated = []
                for idx in range(len(point_list)):
                    pos = list(point_list[idx][0].values())
                    quat = list(point_list[idx][1].values())
                    point_list_updated.append(pos + quat)
                point_list = point_list_updated

        # print("Point list: " + str(point_list))

        if point_list == self.prev_movement[0] and duration_list == self.prev_movement[1]:
            return
        self.prev_movement = [point_list, duration_list]
        self.switch_controller(self.cartesian_trajectory_controller)
        # make sure the correct controller is loaded and activated
        self.trajectory_client = actionlib.SimpleActionClient(
            "{}/follow_cartesian_trajectory".format(
                self.cartesian_trajectory_controller),
            FollowCartesianTrajectoryAction,
        )
        goal = FollowCartesianTrajectoryGoal()

        # The following list are arbitrary positions
        # Change to your own needs if desired
        pose_list = []
        for point in point_list:
            pose_list.append(geometry_msgs.Pose(
                position=geometry_msgs.Point(
                    x=point[0],
                    y=point[1],
                    z=point[2],
                ),
                orientation=geometry_msgs.Quaternion(
                    x=point[3],
                    y=point[4],
                    z=point[5],
                    w=point[6],
                ),
            ))

        for i, pose in enumerate(pose_list):
            point = CartesianTrajectoryPoint()
            point.pose = pose
            point.time_from_start = rospy.Duration(duration_list[i])
            goal.trajectory.points.append(point)

        rospy.loginfo(
            "Executing trajectory using the {}".format(
                self.cartesian_trajectory_controller)
        )

        self.trajectory_client.send_goal(goal)
        if blocking:
            self.trajectory_client.wait_for_result()
            result = self.trajectory_client.get_result()
            rospy.loginfo(
                "Trajectory execution finished in state {}".format(result.error_code))

    def send_velocity(self, linear_vel=[0, 0, 0], angular_vel=[0, 0, 0], dictionary=False):
        # This method will create a twist message and publish it to the twist controller
        self.switch_controller(OTHER_CONTROLLERS[1])
        twist = Twist()
        if dictionary:
            twist.linear.x = linear_vel['x']
            twist.linear.y = linear_vel['y']
            twist.linear.z = linear_vel['z']
            twist.angular.x = angular_vel['x']
            twist.angular.y = angular_vel['y']
            twist.angular.z = angular_vel['z']
        else:
            twist.linear.x = linear_vel[0]
            twist.linear.y = linear_vel[1]
            twist.linear.z = linear_vel[2]
            twist.angular.x = angular_vel[0]
            twist.angular.y = angular_vel[1]
            twist.angular.z = angular_vel[2]
        self.pub.publish(twist)

    def switch_controller(self, target_controller):
        """Activates the desired controller and stops all others from the predefined list above"""
        other_controllers = (
                JOINT_TRAJECTORY_CONTROLLERS
                + CARTESIAN_TRAJECTORY_CONTROLLERS
                + OTHER_CONTROLLERS
        )

        if self.prev_controller == target_controller:
            return
        print("Switching to {}".format(target_controller))
        self.prev_controller = target_controller

        other_controllers.remove(target_controller)

        srv = LoadControllerRequest()
        srv.name = target_controller
        self.load_srv(srv)

        srv = SwitchControllerRequest()
        srv.stop_controllers = other_controllers
        srv.start_controllers = [target_controller]
        srv.strictness = SwitchControllerRequest.BEST_EFFORT
        self.switch_srv(srv)
        time.sleep(1)
        print("Switched to {}".format(target_controller))

    def update_cartesian_position(self, data):
        # This function is called everytime a new position is published to the /tf topic
        # It updates the current position of the robot

        if data.transforms[0].child_frame_id != "tool0_controller":
            return

        self.cart_pos['x'] = data.transforms[0].transform.translation.x
        self.cart_pos['y'] = data.transforms[0].transform.translation.y
        self.cart_pos['z'] = data.transforms[0].transform.translation.z
        self.cart_orient['x'] = data.transforms[0].transform.rotation.x
        self.cart_orient['y'] = data.transforms[0].transform.rotation.y
        self.cart_orient['z'] = data.transforms[0].transform.rotation.z
        self.cart_orient['w'] = data.transforms[0].transform.rotation.w

    def get_current_position(self):
        return [self.cart_pos, self.cart_orient]

    def get_current_joint_positions(self):
        positions = list(self.joint_positions)
        temp = positions[0]
        positions[0] = positions[2]
        positions[2] = temp
        return positions

    def rotate_z(self, tf, degrees):
        """Rotates a quaternion by an angle in the z axis using scipy"""

        tf_copy = tf.copy()
        input_quat = tf_copy[1]

        # Check if the data type for input_quat is correct
        if not isinstance(input_quat, list):
            if isinstance(input_quat, dict):
                input_quat = list(input_quat.values())

        # Construct a new quaternion using tf.transformations
        quat = Rotation.from_quat(
            [input_quat[0], input_quat[1], input_quat[2], input_quat[3]])
        # Rotate the quaternion by the desired angle
        euler_angles = quat.as_euler('xyz', degrees=True)
        euler_angles[2] += degrees
        quat = Rotation.from_euler('xyz', euler_angles, degrees=True).as_quat()
        input_quat = tf_copy[1]
        input_quat['x'] = quat[0]
        input_quat['y'] = quat[1]
        input_quat['z'] = quat[2]
        input_quat['w'] = quat[3]
        return [tf_copy[0], input_quat]

    def send_single_joint_trajectory(self, position, duration, blocking=False):
        self.send_joint_trajectory([position], [duration], blocking)

    def send_joint_trajectory(self, position_list, duration_list, blocking=False):
        """Creates a trajectory and sends it using the selected action server"""
        print("Position list: {}".format(position_list))

        # make sure the correct controller is loaded and activated
        self.switch_controller(self.joint_trajectory_controller)
        self.trajectory_client = actionlib.SimpleActionClient(
            "{}/follow_joint_trajectory".format(  # traj_client.send_cartesion_point(mid_high, 2.5, True)
                self.joint_trajectory_controller),
            FollowJointTrajectoryAction,
        )

        # Create and fill trajectory goal
        goal = FollowJointTrajectoryGoal()
        goal.trajectory.joint_names = JOINT_NAMES

        for i, position in enumerate(position_list):
            point = JointTrajectoryPoint()
            point.positions = position
            point.time_from_start = rospy.Duration(duration_list[i])
            goal.trajectory.points.append(point)

        time.sleep(1)
        rospy.loginfo("Executing trajectory using the {}".format(
            self.joint_trajectory_controller))

        self.trajectory_client.send_goal(goal)
        if blocking:
            self.trajectory_client.wait_for_result()
            result = self.trajectory_client.get_result()
            rospy.loginfo(
                "Trajectory execution finished in state {}".format(result.error_code))


if __name__ == "__main__":
    client = TrajectoryClient()
    # client.twist_controller()
    print(client.get_current_position())

    point = [{'x': 0.20187183708451983, 'y': -0.814567667069645, 'z': 0.20502601650634273},  # Remove -0.03 from z
             {'x': 4.472168305919136e-06, 'y': 0.9999999999804778, 'z': -1.7520471217904713e-06,
              'w': 3.996804222079008e-06}]

    rotated_point = client.rotate_z(point, 90)
    print(point)
    print(rotated_point)

    point_list = []
    point_list.append(point)
    point_list.append(rotated_point)

    # point_list.append([0.4, -0.5, 0.0, 0.707, 0.707, 0, 1])
    # point_list.append([0.4, -0.5, 0.0, 0.707, 0.707, 0, 0.5])
    # point_list.append([0.4, -0.5, 0.0, 0, 0, 1, 1])
    # point_list.append([0.4, -0.5, 0.0, 0, 0, 0, 1])
    # point_list.append([0.4, -0.5, 0.6, 0, 0, 0, 1])
    # point_list.append([0.4, 0.5, 0.6, 0, 0, 0, 1])
    # point_list.append([0.4, 0.5, 0.0, 0, 0, 0, 1])
    # point_list.append([0.6, -0.5, 0.0, 0, 0, 0, 1])
    duration_list = [3.0, 5.0, 7.0, 9.0, 11.0]
    # duration_list = [3.0, 6.0, 9.0, 14.0, 15.0, 18.0, 21.0, 24.0, 27.0, 30.0]
    client.send_cartesian_trajectory(point_list, [3.0, 6.0], blocking=True)
