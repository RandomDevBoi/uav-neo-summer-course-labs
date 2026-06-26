"""
MIT BWSI Autonomous Drone Racing Course - UAV Neo
GNU General Public License v3.0

Week 2/3 Lab — Step 3: Seek the Gate
Yaw to center the gate, then fly forward toward it.
Source: 05_ColorSegmentation.ipynb applied live.
"""

import drone_core
import drone_utils as uav_utils
import cv2
import numpy as np

# -- Constants --------------------------------------------------------------
LOWER1 = np.array([  0, 120,  70], dtype=np.uint8)
UPPER1 = np.array([ 10, 255, 255], dtype=np.uint8)
LOWER2 = np.array([170, 120,  70], dtype=np.uint8)
UPPER2 = np.array([180, 255, 255], dtype=np.uint8)
MIN_AREA   = 400
COL_CENTER = 320
MAX_YAW    = 0.4        # yaw authority for centering
APPROACH_PITCH = 0.25   # forward speed once centered
CENTER_TOL = 60         # px error to count as centered
SEARCH_YAW = 0.25       # spin slowly when no gate is seen
TARGET_WIDTH = 220      # gate this wide (px) => close enough

# -- Module-level state -----------------------------------------------------
_done = False

def reset():
    global _done
    _done = False


def update(drone):
    global _done
    if _done:
        return True
    ##################################
    #### START PUT CODE HERE #########

    # 1. Find the gate's largest contour (two red ranges) like Step 2.
    # 2. If best is None: spin to search -> send_pcmd(0, 0, SEARCH_YAW, 0); return False
    # 3. x, y, w, h = cv2.boundingRect(best)
    # 4. gate_col = x + w / 2.0 ; err = (gate_col - COL_CENTER) / COL_CENTER
    # 5. yaw = uav_utils.clamp(err * MAX_YAW, -MAX_YAW, MAX_YAW)
    # 6. Only fly forward once roughly centered:
    #    pitch = APPROACH_PITCH if abs(gate_col - COL_CENTER) < CENTER_TOL else 0.0
    # 7. send_pcmd(pitch, 0, yaw, 0)
    # 8. When the box is wide enough (w >= TARGET_WIDTH): stop and set _done = True

    ###### END PUT CODE HERE #########
    ##################################
    return _done


if __name__ == "__main__":
    _drone = drone_core.create_drone()
    _launched = False

    def start():
        reset()
        print("Step 3: Seek the Gate")

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
