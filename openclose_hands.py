# An example demonstrating for the simple hands manipulating by open and close
# left and/or right hand fingers
from __future__ import print_function

import time

from naorobot import start_session, end_session, associate_handlers
from naorobot import \
    open_fingers_left_hand, close_fingers_left_hand, \
    open_fingers_right_hand, close_fingers_right_hand


start_session()
associate_handlers()

# -----------------------------------------------------------------------------

# close and open both hands three times
close_fingers_left_hand()
close_fingers_right_hand()
time.sleep(0.5)

open_fingers_left_hand()
open_fingers_right_hand()
time.sleep(0.5)

close_fingers_left_hand()
close_fingers_right_hand()
time.sleep(0.5)

open_fingers_left_hand()
open_fingers_right_hand()
time.sleep(0.5)

close_fingers_left_hand()
close_fingers_right_hand()
time.sleep(0.5)

open_fingers_left_hand()
open_fingers_right_hand()
time.sleep(0.5)

# -----------------------------------------------------------------------------

# close and open left hand three times
close_fingers_left_hand()
time.sleep(0.5)

open_fingers_left_hand()
time.sleep(0.5)

close_fingers_left_hand()
time.sleep(0.5)

open_fingers_left_hand()
time.sleep(0.5)

close_fingers_left_hand()
time.sleep(0.5)

open_fingers_left_hand()
time.sleep(0.5)

# -----------------------------------------------------------------------------

# close and open right hand three times
close_fingers_right_hand()
time.sleep(0.5)

open_fingers_right_hand()
time.sleep(0.5)

close_fingers_right_hand()
time.sleep(0.5)

open_fingers_right_hand()
time.sleep(0.5)

close_fingers_right_hand()
time.sleep(0.5)

open_fingers_right_hand()
time.sleep(0.5)

close_fingers_right_hand()
time.sleep(0.5)

open_fingers_right_hand()
time.sleep(0.5)

# -----------------------------------------------------------------------------

time.sleep(5.5)

end_session()
