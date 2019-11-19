# An example demonstrating for shaking robot's head left-right and u-down
import time

import numpy as np

from naorobot import JointNames, HeadYaw, HeadPitch
from naorobot import start_session, end_session, associate_handlers
from naorobot import write_joint_angles

start_session()
associate_handlers()

# -----------------------------------------------------------------------------

# an example shaking the robot's head left-right
head_yaw_degrees = np.array(
    [0, 30, 45, 60, 90, 60, 45, 30, 0, -30, -45, -60, -90, -60, -45, -30, 0])
head_yaw_radians = np.sin(head_yaw_degrees * np.pi / 180)
robot_joint_angles = [None] * len(JointNames)
for _ in range(3):
    for i in range(len(head_yaw_radians)):
        robot_joint_angles[HeadYaw] = head_yaw_radians[i]
        write_joint_angles(robot_joint_angles)
        time.sleep(0.1)

# an example shaking the robot's head up-down
head_pitch_degrees = np.array(
    [0, 30, 45, 30, 0, -30, -45, -30, 0])
head_pitch_radians = np.sin(head_pitch_degrees * np.pi / 180)
robot_joint_angles = [None] * len(JointNames)
for _ in range(3):
    for i in range(len(head_pitch_radians)):
        robot_joint_angles[HeadPitch] = head_pitch_radians[i]
        write_joint_angles(robot_joint_angles)
        time.sleep(0.2)
# -----------------------------------------------------------------------------

end_session()
