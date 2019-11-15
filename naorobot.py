from __future__ import print_function

import time

import numpy as np

# load the v-rep remote API
import vrep

# Names of NAO's joints
JointNames = [
    'HeadYaw', 'HeadPitch',
    'LShoulderPitch3', 'LShoulderRoll3', 'LElbowYaw3', 'LElbowRoll3',
    'LWristYaw3',
    'NAO_LThumbBase', 'NAO_LLFingerBase', 'NAO_LRFingerBase',
    'LHipYawPitch3',
    'LHipRoll3', 'LHipPitch3',
    'LKneePitch3',
    'LAnklePitch3', 'LAnkleRoll3',
    'RHipYawPitch3',
    'RHipRoll3', 'RHipPitch3',
    'RKneePitch3',
    'RAnklePitch3', 'RAnkleRoll3',
    'RShoulderPitch3', 'RShoulderRoll3', 'RElbowYaw3', 'RElbowRoll3',
    'RWristYaw3',
    'NAO_RThumbBase', 'NAO_RLFingerBase', 'NAO_RRFingerBase']
# Force sensors fro the left foot
LFsrNames = ['NAO_LFsrFL', 'NAO_LFsrFR', 'NAO_LFsrRL', 'NAO_LFsrRR']

# Force sensors fro the right foot
RFsrNames = ['NAO_RFsrFL', 'NAO_RFsrFR', 'NAO_RFsrRL', 'NAO_RFsrRR']

# Handles for joints and force sensors
JointHandles = [0] * len(JointNames)
LFsrHandles = [0] * len(LFsrNames)
RFsrHandles = [0] * len(RFsrNames)

# clean up communication threads
vrep.simxFinish(-1)

# V-REP communication host (localhost)
vrep_host = '127.0.0.1'

# V-REP communication port
vrep_port = 19999

clientID = -1


def start_session():
    '''start a communication session'''
    global clientID
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
    print('Associating joint handlers')
    for index, name in enumerate(JointNames):
        returnCode, JointHandles[index] = vrep.simxGetObjectHandle(
            clientID, name, vrep.simx_opmode_blocking)
        if returnCode:
            print("Failed to associate with %s (error: %d)" % (
                name, returnCode))
        else:  # make sure joint handlers work properly
            returnCode, position = vrep.simxGetJointPosition(
                clientID, JointHandles[index], vrep.simx_opmode_streaming)
            returnCode = vrep.simxSetJointTargetPosition(
                clientID, JointHandles[index], 0.0,
                vrep.simx_opmode_streaming)
            returnCode, position = vrep.simxGetJointPosition(
                clientID, JointHandles[index], vrep.simx_opmode_streaming)
            returnCode = vrep.simxSetJointTargetPosition(
                clientID, JointHandles[index], 0.0,
                vrep.simx_opmode_streaming)

    print('Associating left force sensor handlers')
    for index, name in enumerate(LFsrNames):
        returnCode, LFsrHandles[index] = vrep.simxGetObjectHandle(
            clientID, name, vrep.simx_opmode_blocking)
        if returnCode:
            print("Failed to associate with %s (error: %d)" % (
                name, returnCode))

    print('Associating right force sensor handlers')
    for index, name in enumerate(RFsrNames):
        returnCode, RFsrHandles[index] = vrep.simxGetObjectHandle(
            clientID, name, vrep.simx_opmode_blocking)
        if returnCode:
            print("Failed to associate with %s (error: %d)" % (
                name, returnCode))


def read_joint_positions():
    '''read current joint positions/angles'''
    angles = [0.0] * len(JointNames)
    for index, name in enumerate(JointNames):
        if JointHandles[index]:
            returnCode, position = vrep.simxGetJointPosition(
                clientID, JointHandles[index], vrep.simx_opmode_streaming)
            if returnCode:
                print("Failed reading position of joint %s (error: %d)" % (
                    name, returnCode))
            else:
                angles[index] = position
    return angles


def write_joint_positions(angles):
    '''write/apply new positions/angles to involved joints'''
    assert len(angles) == len(JointNames)
    for index, name in enumerate(JointNames):
        if JointHandles[index]:
            returnCode = vrep.simxSetJointTargetPosition(
                clientID, JointHandles[index], angles[index],
                vrep.simx_opmode_streaming)
            if returnCode:
                print("Failed to writing position of joint %s (error: %d)" % (
                    name, returnCode))


def read_sensor_values():
    '''read current sensor values'''
    lfsr_values = [0.0] * len(LFsrNames)
    rfsr_values = [0.0] * len(RFsrNames)
    for index, name in enumerate(LFsrNames):
        if LFsrHandles[index]:
            returnCode, state, forces, torques = vrep.simxReadForceSensor(
                clientID, LFsrHandles[index], vrep.simx_opmode_streaming)
            if returnCode:
                print("Failed reading force sensor %s (error: %d)" % (
                    name, returnCode))
            else:
                lfsr_values[index] = forces[2]
    for index, name in enumerate(RFsrNames):
        if RFsrHandles[index]:
            returnCode, state, forces, torques = vrep.simxReadForceSensor(
                clientID, RFsrHandles[index], vrep.simx_opmode_streaming)
            if returnCode:
                print("Failed reading force sensor %s (error code: %d)" % (
                    name, returnCode))
            else:
                rfsr_values[index] = forces[2]
    return lfsr_values, rfsr_values
