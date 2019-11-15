import time

import numpy as np

from naorobot import JointNames
from naorobot import start_session, end_session, associate_handlers
from naorobot import write_joint_positions

# MAIN PROGRAM

start_session()
associate_handlers()

# -----------------------------------------------------------------------------

# an example shaking the robot's head left-right
head_yaw_id = 0
head_yaw_degrees = np.array(
    [0, 30, 45, 60, 90, 60, 45, 30, 0, -30, -45, -60, -90, -60, -45, -30, 0])
head_yaw_radians = np.sin(head_yaw_degrees * np.pi / 180)
robot_joint_angles = [0.0] * len(JointNames)
for _ in range(3):
    for i in range(len(head_yaw_radians)):
        robot_joint_angles[head_yaw_id] = head_yaw_radians[i]
        write_joint_positions(robot_joint_angles)
        time.sleep(0.1)

# an example shaking the robot's head up-down
head_pitch_id = 1
head_pitch_degrees = np.array(
    [0, 30, 45, 30, 0, -30, -45, -30, 0])
head_pitch_radians = np.sin(head_pitch_degrees * np.pi / 180)
robot_joint_angles = [0.0] * len(JointNames)
for _ in range(3):
    for i in range(len(head_pitch_radians)):
        robot_joint_angles[head_pitch_id] = head_pitch_radians[i]
        write_joint_positions(robot_joint_angles)
        time.sleep(0.2)
# -----------------------------------------------------------------------------

end_session()
