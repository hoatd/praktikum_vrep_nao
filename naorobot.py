# Helper module for basic manipulating NAO robot model in V-REP
from __future__ import print_function

import time

import vrep  # load the v-rep remote API

# NAO robot model in V-REP has 24 separate joints for head, upper and lower
# body. For reading 24 separate joint position/angles values as one using
# function `read_joint_positions` returning an 24-elements buffer. For writing
# 24 separate joint position/angles values as one using function
# `write_joint_positions` with 24-elements buffer corresponding new joint
# angle values, None value elements will not be changed.
#
# Two robot hands have 8 joints for fingers combined for each with simple open
# and close behaviors modeling Open and close hands using functions
# `open_fingers_left_hand`, `open_fingers_right_hand`,
# `close_fingers_left_hand`, `close_fingers_right_hand`

# NAO has 4 force sensors for each bare foot. Reading all sensors value using
# function `read_sensor_values` returning 2 array of left and right foot force
# sensors.
#
# Robot's absolute position and orientation can be accessed using function
# `read_position` and function `read_orientation`
#
# NAO has 2 cameras. Images can be accessed using function `read_vision_images`
#
# Other functions simplify robot manipulating process include: `start_session`,
# `end_session`, and `associate_handlers`

# ID of NAO's joints
HeadYaw = 0
HeadPitch = 1
LShoulderPitch = 2
LShoulderRoll = 3
LElbowYaw = 4
LElbowRoll = 5
LWristYaw = 6
LHipYawPitch = 7
LHipRoll = 8
LHipPitch = 9
LKneePitch = 10
LAnklePitch = 11
LAnkleRoll = 12
RHipYawPitch = 13
RHipRoll = 14
RHipPitch = 15
RKneePitch = 16
RAnklePitch = 17
RAnkleRoll = 18
RShoulderPitch = 19
RShoulderRoll = 20
RElbowYaw = 21
RElbowRoll = 22
RWristYaw = 23

# Names of NAO's joints: 24-separate joints for head, upper and lower body
JointNames = [
    'HeadYaw',              # id = 0
    'HeadPitch',            # id = 1
    'LShoulderPitch3',      # id = 2
    'LShoulderRoll3',       # id = 3
    'LElbowYaw3',           # id = 4
    'LElbowRoll3',          # id = 5
    'LWristYaw3',           # id = 6
    'LHipYawPitch3',        # id = 7
    'LHipRoll3',            # id = 8
    'LHipPitch3',           # id = 9
    'LKneePitch3',          # id = 10
    'LAnklePitch3',         # id = 11
    'LAnkleRoll3',          # id = 12
    'RHipYawPitch3',        # id = 13
    'RHipRoll3',            # id = 14
    'RHipPitch3',           # id = 15
    'RKneePitch3',          # id = 16
    'RAnklePitch3',         # id = 17
    'RAnkleRoll3',          # id = 18
    'RShoulderPitch3',      # id = 19
    'RShoulderRoll3',       # id = 20
    'RElbowYaw3',           # id = 21
    'RElbowRoll3',          # id = 22
    'RWristYaw3',           # id = 23
]

# Left hand joints: 8-combined joints for fingers
LHandJointNames = [
    'NAO_LThumbBase',
    'Revolute_joint8',
    'NAO_LLFingerBase',
    'Revolute_joint12',
    'Revolute_joint14',
    'NAO_LRFingerBase',
    'Revolute_joint11',
    'Revolute_joint13'
]

# Right hand joints: 8-combined joints for fingers
RHandJointNames = [
    'NAO_RThumbBase',
    'Revolute_joint0',
    'NAO_RLFingerBase',
    'Revolute_joint5',
    'Revolute_joint6',
    'NAO_RRFingerBase',
    'Revolute_joint2',
    'Revolute_joint3'
]

# Names of force sensors for the left foot
LFsrNames = ['NAO_LFsrFL', 'NAO_LFsrFR', 'NAO_LFsrRL', 'NAO_LFsrRR']

# Names of force sensors for the right foot
RFsrNames = ['NAO_RFsrFL', 'NAO_RFsrFR', 'NAO_RFsrRL', 'NAO_RFsrRR']

PositionName = 'NAO'

OrientationName = 'NAO'

VisionNames = ['NAO_vision1', 'NAO_vision2']

# Handles for joints, force sensors, orientation, position and visions/cameras
_JointHandles = [0] * len(JointNames)
_LHandJointHandles = [0] * len(LHandJointNames)
_RHandJointHandles = [0] * len(RHandJointNames)
_LFsrHandles = [0] * len(LFsrNames)
_RFsrHandles = [0] * len(RFsrNames)
_PositionHandle = 0
_OrientationHandle = 0
_VisionHandles = [0] * len(VisionNames)


# ID of V-REP session
clientID = -1


def start_session(vrep_host='127.0.0.1', vrep_port=19999):
    '''start a communication session'''
    global clientID
    vrep.simxFinish(-1)  # clean up communication threads
    clientID = vrep.simxStart(vrep_host, vrep_port, True, True, 5000, 5)
    if clientID == -1:
        print('Failed to connect to V-rep!')
        exit()
    print ('Connected to V-rep at %s:%d' % (vrep_host, vrep_port))
    vrep.simxSynchronous(clientID, True)
    vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot)


def end_session():
    '''close the communication session'''
    vrep.simxGetPingTime(clientID)
    vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot)
    vrep.simxSynchronous(clientID, False)
    vrep.simxFinish(clientID)


def associate_handlers():
    '''get handlers involved joints and sensors'''
    global _PositionHandle, _OrientationHandle
    for index, name in enumerate(JointNames):
        returnCode, _JointHandles[index] = vrep.simxGetObjectHandle(
            clientID, name + '#', vrep.simx_opmode_blocking)
        if returnCode:
            print("Failed to associate with %s (error: %d)" % (
                name, returnCode))
        else:  # make sure joint handlers work properly
            returnCode, position = vrep.simxGetJointPosition(
                clientID, _JointHandles[index],
                vrep.simx_opmode_streaming)
    for index, name in enumerate(LHandJointNames):
        returnCode, _LHandJointHandles[index] = vrep.simxGetObjectHandle(
            clientID, name + '#', vrep.simx_opmode_blocking)
        if returnCode:
            print("Failed to associate with %s (error: %d)" % (
                name, returnCode))
        else:  # make sure left hand finger handlers work properly
            returnCode, position = vrep.simxGetJointPosition(
                clientID, _LHandJointHandles[index],
                vrep.simx_opmode_streaming)
    for index, name in enumerate(RHandJointNames):
        returnCode, _RHandJointHandles[index] = vrep.simxGetObjectHandle(
            clientID, name + '#', vrep.simx_opmode_blocking)
        if returnCode:
            print("Failed to associate with %s (error: %d)" % (
                name, returnCode))
        else:  # make sure right hand finger handlers work properly
            returnCode, position = vrep.simxGetJointPosition(
                clientID, _RHandJointHandles[index],
                vrep.simx_opmode_streaming)
    for index, name in enumerate(LFsrNames):
        returnCode, _LFsrHandles[index] = vrep.simxGetObjectHandle(
            clientID, name + '#', vrep.simx_opmode_blocking)
        if returnCode:
            print("Failed to associate with %s (error: %d)" % (
                name, returnCode))
        else:  # make sure LFsr handlers work properly
            returnCode, state, forces, torques = vrep.simxReadForceSensor(
                clientID, _LFsrHandles[index], vrep.simx_opmode_streaming)
    for index, name in enumerate(RFsrNames):
        returnCode, _RFsrHandles[index] = vrep.simxGetObjectHandle(
            clientID, name + '#', vrep.simx_opmode_blocking)
        if returnCode:
            print("Failed to associate with %s (error: %d)" % (
                name, returnCode))
        else:  # make sure RFsr handlers work properly
            returnCode, state, forces, torques = vrep.simxReadForceSensor(
                clientID, _RFsrHandles[index], vrep.simx_opmode_streaming)
    returnCode, _PositionHandle = vrep.simxGetObjectHandle(
        clientID, PositionName + '#', vrep.simx_opmode_blocking)
    if returnCode:
        print("Failed to associate with %s (error: %d)" % (
            PositionName, returnCode))
    else:  # make sure position handler works properly
        returnCode, position = vrep.simxGetObjectPosition(
            clientID, _PositionHandle, -1,
            vrep.simx_opmode_streaming)
    returnCode, _OrientationHandle = vrep.simxGetObjectHandle(
        clientID, OrientationName + '#', vrep.simx_opmode_blocking)
    if returnCode:
        print("Failed to associate with %s (error: %d)" % (
            OrientationName, returnCode))
    else:  # make sure orientation handler works properly
        returnCode, orientation = vrep.simxGetObjectOrientation(
            clientID, _OrientationHandle, -1,
            vrep.simx_opmode_streaming)
    for index, name in enumerate(VisionNames):
        returnCode, _VisionHandles[index] = vrep.simxGetObjectHandle(
            clientID, name + '#', vrep.simx_opmode_blocking)
        if returnCode:
            print("Failed to associate with %s (error: %d)" % (
                name, returnCode))
        else:  # make sure vision handlers work properly
            returnCode, resolution, image = vrep.simxGetVisionSensorImage(
                clientID, _VisionHandles[index], 0,
                vrep.simx_opmode_streaming)
    time.sleep(0.1)


def read_joint_angles(simx_opmode=vrep.simx_opmode_buffer):
    '''read current joint positions/angles'''
    angles = [None] * len(JointNames)
    for index, name in enumerate(JointNames):
        if _JointHandles[index]:
            returnCode, position = vrep.simxGetJointPosition(
                clientID, _JointHandles[index], simx_opmode)
            if returnCode == vrep.simx_return_novalue_flag:
                # Ignore report of the 1st call of simxSetJointTargetPosition
                # that returns no previous buffer in streaming mode
                angles[index] = position
            elif returnCode:
                print("Failed reading position of joint %s (error: %d)" % (
                    name, returnCode))
            else:
                angles[index] = position
    return angles


def write_joint_angles(angles, simx_opmode=vrep.simx_opmode_streaming):
    '''write/apply new positions/angles to joints'''
    assert len(angles) == len(JointNames)
    for index, name in enumerate(JointNames):
        if _JointHandles[index] and angles[index] is not None:
            returnCode = vrep.simxSetJointTargetPosition(
                clientID, _JointHandles[index], angles[index], simx_opmode)
            if returnCode == vrep.simx_return_novalue_flag:
                # Ignore report of the 1st call of simxSetJointTargetPosition
                # that returns no previous buffer in streaming mode
                pass
            elif returnCode:
                print("Failed writing position of joint %s (error: %d)" % (
                    name, returnCode))


def read_sensor_values(simx_opmode=vrep.simx_opmode_streaming):
    '''read force sensor values of the left and right foot'''
    lfsr_values = [None] * len(LFsrNames)
    rfsr_values = [None] * len(RFsrNames)
    for index, name in enumerate(LFsrNames):
        if _LFsrHandles[index]:
            returnCode, state, forces, torques = vrep.simxReadForceSensor(
                clientID, _LFsrHandles[index], simx_opmode)
            if returnCode:
                print("Failed reading force sensor %s (error: %d)" % (
                    name, returnCode))
            else:
                lfsr_values[index] = forces[2]
    for index, name in enumerate(RFsrNames):
        if _RFsrHandles[index]:
            returnCode, state, forces, torques = vrep.simxReadForceSensor(
                clientID, _RFsrHandles[index], vrep.simx_opmode_streaming)
            if returnCode:
                print("Failed reading force sensor %s (error code: %d)" % (
                    name, returnCode))
            else:
                rfsr_values[index] = forces[2]
    return lfsr_values, rfsr_values


def read_position(simx_opmode=vrep.simx_opmode_buffer):
    '''read robot's absolute position (x, y, z)'''
    if _PositionHandle:
        returnCode, position = vrep.simxGetObjectPosition(
            clientID, _PositionHandle, -1, simx_opmode)
        if returnCode:
            print("Failed reading robot's position %s (error: %d)" % (
                PositionName, returnCode))
            return None
        return position
    return None


def read_orientation(simx_opmode=vrep.simx_opmode_buffer):
    '''read robot's absolute orientation: (alpha, beta, gamma)'''
    if _OrientationHandle:
        returnCode, orientation = vrep.simxGetObjectOrientation(
            clientID, _OrientationHandle, -1, simx_opmode)
        if returnCode:
            print("Failed reading robot's orientation %s (error: %d)" % (
                OrientationName, returnCode))
            return None
        return orientation
    else:
        return None


def read_vision_images(simx_opmode=vrep.simx_opmode_buffer):
    '''read images from left[0] and right[1] vision/cameras'''
    images = [None] * len(VisionNames)
    resolutions = [None] * len(VisionNames)
    for index, name in enumerate(VisionNames):
        if _VisionHandles[index]:
            returnCode, resolution, image = vrep.simxGetVisionSensorImage(
                clientID, _VisionHandles[index], 0, simx_opmode)
            if returnCode:
                print("Failed reading vision image %s (error: %d)" % (
                    name, returnCode))
            else:
                images[index] = image
                resolutions[index] = resolution
    return resolutions, images


def _set_hand_fingers(finger_names, finger_handles, value, simx_opmode):
    for index, name in enumerate(finger_names):
        if finger_handles[index]:
            returnCode = vrep.simxSetJointTargetPosition(
                clientID, finger_handles[index], value, simx_opmode)
            if returnCode == vrep.simx_return_novalue_flag:
                # Ignore report of the 1st call of simxSetJointTargetPosition
                # that returns no previous buffer in streaming mode
                pass
            elif returnCode:
                print("Failed writing finger joint %s (error: %d)" % (
                    name, returnCode))


def open_fingers_left_hand(simx_opmode=vrep.simx_opmode_oneshot):
    _set_hand_fingers(LHandJointNames, _LHandJointHandles, 0.0, simx_opmode)


def close_fingers_left_hand(simx_opmode=vrep.simx_opmode_oneshot):
    _set_hand_fingers(LHandJointNames, _LHandJointHandles, 1.0, simx_opmode)


def open_fingers_right_hand(simx_opmode=vrep.simx_opmode_oneshot):
    _set_hand_fingers(RHandJointNames, _RHandJointHandles, 0.0, simx_opmode)


def close_fingers_right_hand(simx_opmode=vrep.simx_opmode_oneshot):
    _set_hand_fingers(RHandJointNames, _RHandJointHandles, 1.0, simx_opmode)
