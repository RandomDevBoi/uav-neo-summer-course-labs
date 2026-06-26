"""
MIT BWSI Autonomous Drone Racing Course - UAV Neo
GNU General Public License v3.0

Week 2/3 Lab — Step 3: Follow the Line  (SOLUTION)
Steer the drone to keep the line centered while flying forward.
Source: 03_LinearRegression.ipynb applied live.
"""

import drone_core
import drone_utils as uav_utils
import cv2
import numpy as np

import os as _os, sys as _sys
_d = _os.path.dirname(_os.path.abspath(__file__))
while _os.path.basename(_d) != "labs" and _os.path.dirname(_d) != _d:
    _d = _os.path.dirname(_d)
if _d not in _sys.path:
    _sys.path.insert(0, _d)
import neo_lab

# -- Constants --------------------------------------------------------------
SAT_MIN       = 80
VAL_MIN       = 60
MIN_PIXELS    = 200
FORWARD_PITCH = 0.25     # constant forward speed
MAX_ROLL      = 0.30     # strafe authority for centering
FOLLOW_TIME   = 12.0     # seconds to follow before landing
IMAGE_CENTER  = 320      # 640-wide image -> center column

# -- Module-level state -----------------------------------------------------
_timer = 0.0
_done  = False

def reset():
    global _timer, _done
    _timer = 0.0
    _done  = False


def update(drone):
    global _timer, _done
    if _done:
        return True
    _timer += drone.get_delta_time()
    image = drone.camera.get_downward_image()
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = (hsv[:, :, 1] > SAT_MIN) & (hsv[:, :, 2] > VAL_MIN)
    points = np.argwhere(mask)
    if len(points) < MIN_PIXELS:
        drone.flight.stop()                 # lost the line -> hover and wait
        return False
    line_col = points[:, 1].mean()          # average column of the line
    offset = (line_col - IMAGE_CENTER) / IMAGE_CENTER   # -1 (left) .. +1 (right)
    roll = uav_utils.clamp(offset * MAX_ROLL, -MAX_ROLL, MAX_ROLL)
    drone.flight.send_pcmd(FORWARD_PITCH, roll, 0, 0)
    if _timer >= FOLLOW_TIME:
        drone.flight.stop()
        print("[Step 3] Finished following the line")
        _done = True
    return _done


if __name__ == "__main__":
    _drone = drone_core.create_drone()
    _launcher = neo_lab.Launcher(3.0)

    def start():
        _launcher.reset()
        reset()
        print("Step 3: Follow the Line")

    def _update():
        if not _launcher.done:        # arm + climb to a safe height first
            _launcher.update(_drone)
            return
        if update(_drone):
            _drone.flight.land()

    _drone.set_start_update(start, _update)
    _drone.go()
