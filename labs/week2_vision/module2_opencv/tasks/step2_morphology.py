"""
MIT BWSI Autonomous Drone Racing Course - UAV Neo
GNU General Public License v3.0

Week 2/3 Lab — Step 2: Morphology (Opening)
Clean a binary mask with erosion followed by dilation (an 'opening').
Source: 02_OpenCV.ipynb (cv2.erode / cv2.dilate).
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
THRESHOLD_VALUE = 127
KERNEL_SIZE     = 5
HOVER_TIME      = 3.0

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

    # 1. Build a binary mask like Step 1 (threshold the grayscale image).
    # 2. kernel = np.ones((KERNEL_SIZE, KERNEL_SIZE), np.uint8)
    # 3. eroded = cv2.erode(mask, kernel, iterations=1)
    # 4. opened = cv2.dilate(eroded, kernel, iterations=1)
    # 5. Compare np.count_nonzero(mask) vs np.count_nonzero(opened).
    # 6. When _timer >= HOVER_TIME: print how many pixels were removed, set _done = True

    ###### END PUT CODE HERE #########
    ##################################
    return _done


if __name__ == "__main__":
    _drone = drone_core.create_drone()
    _launcher = neo_lab.Launcher(3.0)

    def start():
        _launcher.reset()
        reset()
        print("Step 2: Morphology (Opening)")

    def _update():
        if not _launcher.done:        # arm + climb to a safe height first
            _launcher.update(_drone)
            return
        if update(_drone):
            _drone.flight.land()

    _drone.set_start_update(start, _update)
    _drone.go()
