"""
MIT BWSI Autonomous Drone Racing Course - UAV Neo
GNU General Public License v3.0

Week 2/3 Lab — Step 3: Follow the Line
Steer the drone to keep the line centered while flying forward.
Source: 03_LinearRegression.ipynb applied live.
"""

import drone_core
import drone_utils as uav_utils
import cv2
import numpy as np

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
    ##################################
    #### START PUT CODE HERE #########

    # 1. Build the mask and points = np.argwhere(mask), like Step 2.
    # 2. If too few points: drone.flight.stop(); return False
    # 3. line_col = points[:, 1].mean()
    # 4. offset = (line_col - IMAGE_CENTER) / IMAGE_CENTER      # -1..+1
    # 5. roll = uav_utils.clamp(offset * MAX_ROLL, -MAX_ROLL, MAX_ROLL)
    #    (line to the right -> positive offset -> roll right to recenter)
    # 6. drone.flight.send_pcmd(FORWARD_PITCH, roll, 0, 0)
    # 7. _timer += drone.get_delta_time(); when >= FOLLOW_TIME stop and set _done = True

    ###### END PUT CODE HERE #########
    ##################################
    return _done


if __name__ == "__main__":
    _drone = drone_core.create_drone()
    _launched = False

    def start():
        reset()
        print("Step 3: Follow the Line")

    def _update():
        global _launched
        if not _launched:
            _drone.flight.takeoff()
            if _drone.physics.get_altitude() > 1.0:
                _launched = True
                reset()
            return
        if update(_drone):
            _drone.flight.land()

    _drone.set_start_update(start, _update)
    _drone.go()
