# An example demonstrating for the simple hands manipulating by hold tightly a
# ball and release by the right hand (Use the scene NAO-3-BALL.ttt)
from __future__ import print_function

import time

from naorobot import JointNames, RElbowYaw, RWristYaw
from naorobot import start_session, end_session, associate_handlers
from naorobot import write_joint_angles
from naorobot import \
    open_fingers_right_hand, close_fingers_right_hand


start_session()
associate_handlers()

# -----------------------------------------------------------------------------

# hold the ball by right hand for some seconds
close_fingers_right_hand()
time.sleep(1.5)

# rotate the right hand for some times without loose the ball
robot_joint_angles = [None] * len(JointNames)
robot_joint_angles[RWristYaw] = 0.0
robot_joint_angles[RElbowYaw] = 0.0
write_joint_angles(robot_joint_angles)
time.sleep(1.5)

robot_joint_angles = [None] * len(JointNames)
robot_joint_angles[RWristYaw] = 1.5708  # 90.0 degrees
robot_joint_angles[RElbowYaw] = 1.5708  # 90.0 degrees
write_joint_angles(robot_joint_angles)
time.sleep(1.5)

robot_joint_angles = [None] * len(JointNames)
robot_joint_angles[RWristYaw] = 0.0
robot_joint_angles[RElbowYaw] = 0.0
write_joint_angles(robot_joint_angles)
time.sleep(1.5)

# release the ball by right hand
open_fingers_right_hand()
time.sleep(0.5)
# -----------------------------------------------------------------------------

time.sleep(5.5)

end_session()
