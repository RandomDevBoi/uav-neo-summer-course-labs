"""
MIT BWSI Autonomous Drone Racing Course - UAV Neo
GNU General Public License v3.0

Week 2/3 Lab — Step 2: Bounding Box
Find the gate's largest contour and its bounding box.
Source: 05_ColorSegmentation.ipynb (bounding boxes).
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
MIN_AREA = 400
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

    # 1. contours = uav_utils.find_contours(image, LOWER1, UPPER1) +
    #               uav_utils.find_contours(image, LOWER2, UPPER2)   # red has 2 ranges
    # 2. best = uav_utils.get_largest_contour(contours, MIN_AREA)
    # 3. if best is None: return False
    # 4. x, y, w, h = cv2.boundingRect(best)
    # 5. When _timer >= HOVER_TIME: print the box and set _done = True

    ###### END PUT CODE HERE #########
    ##################################
    return _done


if __name__ == "__main__":
    _drone = drone_core.create_drone()
    _launched = False

    def start():
        reset()
        print("Step 2: Bounding Box")

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
