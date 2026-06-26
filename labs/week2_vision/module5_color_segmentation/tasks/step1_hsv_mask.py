"""
MIT BWSI Autonomous Drone Racing Course - UAV Neo
GNU General Public License v3.0

Week 2/3 Lab — Step 1: HSV Color Mask
Mask a RED gate in the forward camera using HSV ranges (hue wraps).
Source: 05_ColorSegmentation.ipynb (HSV masking).
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
HOVER_TIME = 3.0

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
    drone.flight.stop()   # hover in place
    ##################################
    #### START PUT CODE HERE #########

    # Red wraps around hue 0/180, so we need TWO ranges combined with | (bitwise or).
    # 1. hsv  = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # 2. mask = cv2.inRange(hsv, LOWER1, UPPER1) | cv2.inRange(hsv, LOWER2, UPPER2)
    # 3. coverage = np.count_nonzero(mask) / mask.size
    # 4. When _timer >= HOVER_TIME: print coverage, set _done = True

    ###### END PUT CODE HERE #########
    ##################################
    return _done


if __name__ == "__main__":
    _drone = drone_core.create_drone()
    _launched = False

    def start():
        reset()
        print("Step 1: HSV Color Mask")

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
