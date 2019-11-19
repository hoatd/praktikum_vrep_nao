# An example demonstrating for capturing robot's cameras
import time

import numpy as np
import matplotlib.pyplot as plt

from naorobot import JointNames, HeadYaw
from naorobot import start_session, end_session, associate_handlers
from naorobot import write_joint_angles
from naorobot import read_vision_images

start_session()
associate_handlers()

plt.ion()
fig, axes = plt.subplots(1, 2)
fig.canvas.set_window_title('NAO CAMERAS')


def draw_images(res, images):
    l_img = np.resize(
        np.array(images[0], dtype=np.uint8), [res[0][1], res[0][0], 3])
    r_img = np.resize(
        np.array(images[1], dtype=np.uint8), [res[1][1], res[1][0], 3])
    axes[0].imshow(l_img, origin='lower')
    axes[1].imshow(r_img, origin='lower')
    plt.draw()
    plt.pause(0.05)


# -----------------------------------------------------------------------------

res, images = read_vision_images()
draw_images(res, images)

head_yaw_degrees = np.array(
    [0, 30, 45, 60, 90, 60, 45, 30, 0, -30, -45, -60, -90, -60, -45, -30, 0])
head_yaw_radians = np.sin(head_yaw_degrees * np.pi / 180)
robot_joint_angles = [None] * len(JointNames)

for _ in range(2):
    for i in range(len(head_yaw_radians)):
        robot_joint_angles[HeadYaw] = head_yaw_radians[i]
        write_joint_angles(robot_joint_angles)
        time.sleep(0.1)

        res, images = read_vision_images()
        draw_images(res, images)

# -----------------------------------------------------------------------------

end_session()
