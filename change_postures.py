# An example demonstrating for manipulating multiple joints in change robot's
# postures
from __future__ import print_function

import time

import numpy as np

from naorobot import start_session, end_session, associate_handlers
from naorobot import read_joint_angles, write_joint_angles


def change_posture(posture_joint_angles, fraction=50, fraction_speed=0.015):
    '''change robot posture from current joint angles to the given posture
    joint angles'''
    robot_joint_angles = read_joint_angles()
    fraction_joint_angles = np.divide(np.subtract(
        posture_joint_angles, robot_joint_angles), fraction)
    for i in xrange(int(fraction)):
        # compute new joint angles
        robot_joint_angles = np.add(robot_joint_angles, fraction_joint_angles)
        # apply new joint angles to the robot
        write_joint_angles(robot_joint_angles)
        # wait for physics stable
        time.sleep(fraction_speed)


# joint angles at the move-init posture (ready for walking)
move_init_joint_angles = np.array([
    -0.0123,    # HeadYaw = 0
    +0.0122,    # HeadPitch = 1
    +1.6174,    # LShoulderPitch = 2
    +0.1670,    # LShoulderRoll = 3
    -1.3684,    # LElbowYaw = 4
    -1.2864,    # LElbowRoll = 5
    -0.9138,    # LWristYaw = 6
    +0.0016,    # LHipYawPitch = 7
    +0.0000,    # LHipRoll = 8
    -0.5220,    # LHipPitch = 9
    +0.9483,    # LKneePitch = 10
    -0.5231,    # LAnklePitch = 11
    +0.0000,    # LAnkleRoll = 12
    +0.0016,    # RHipYawPitch = 13
    +0.0000,    # RHipRoll = 14
    -0.5220,    # RHipPitch = 15
    +0.9483,    # RKneePitch = 16
    -0.5231,    # RAnklePitch = 17
    +0.0000,    # RAnkleRoll = 18
    +1.6174,    # RShoulderPitch = 19
    -0.1670,    # RShoulderRoll = 20
    +1.3684,    # RElbowYaw = 21
    +1.2864,    # RElbowRoll = 22
    +0.9138,    # RWristYaw = 23
])

# joint angles at the stand-zero posture (stand with zero angles all joints)
stand_zero_joint_angles = np.array([
    +0.0000,    # HeadYaw = 0
    -0.0000,    # HeadPitch = 1
    +0.0000,    # LShoulderPitch = 2
    +0.0000,    # LShoulderRoll = 3
    +0.0000,    # LElbowYaw = 4
    -0.0000,    # LElbowRoll = 5
    +0.0000,    # LWristYaw = 6
    -0.0000,    # LHipYawPitch = 7
    +0.0000,    # LHipRoll = 8
    -0.0000,    # LHipPitch = 9
    -0.0000,    # LKneePitch = 10
    -0.0000,    # LAnklePitch = 11
    +0.0000,    # LAnkleRoll = 12
    -0.0000,    # RHipYawPitch = 13
    -0.0000,    # RHipRoll = 14
    -0.0000,    # RHipPitch = 15
    -0.0000,    # RKneePitch = 16
    -0.0000,    # RAnklePitch = 17
    -0.0000,    # RAnkleRoll = 18
    +0.0000,    # RShoulderPitch = 19
    -0.0000,    # RShoulderRoll = 20
    -0.0000,    # RElbowYaw = 21
    +0.0000,    # RElbowRoll = 22
    -0.0000,    # RWristYaw = 23
])

start_session()
associate_handlers()

# -----------------------------------------------------------------------------

change_posture(move_init_joint_angles)
time.sleep(0.5)

change_posture(stand_zero_joint_angles)
time.sleep(0.5)

change_posture(move_init_joint_angles)
time.sleep(0.5)

change_posture(stand_zero_joint_angles)
time.sleep(0.5)

change_posture(move_init_joint_angles)
time.sleep(0.5)

change_posture(stand_zero_joint_angles)
time.sleep(0.5)

change_posture(move_init_joint_angles)
time.sleep(0.5)

change_posture(stand_zero_joint_angles)
time.sleep(0.5)

# -----------------------------------------------------------------------------

time.sleep(5.5)

end_session()
