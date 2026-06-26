"""
MIT BWSI Autonomous Drone Racing Course - UAV Neo
GNU General Public License v3.0

Week 2/3 Lab — Step 2: Largest Object
Locate the largest object and report its center and area.
Source: 04_Downward.ipynb (largest contour + centroid).
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
SAT_MIN = 100
VAL_MIN = 60
MIN_AREA = 300
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

    # 1. Build the mask + contours like Step 1.
    # 2. best = uav_utils.get_largest_contour(contours, MIN_AREA)
    # 3. if best is None: return False        # nothing big enough yet
    # 4. center = uav_utils.get_contour_center(best)   # (row, col)
    #    area   = uav_utils.get_contour_area(best)
    # 5. When _timer >= HOVER_TIME: print center & area, set _done = True

    ###### END PUT CODE HERE #########
    ##################################
    return _done


if __name__ == "__main__":
    _drone = drone_core.create_drone()
    _launcher = neo_lab.Launcher(3.0)

    def start():
        _launcher.reset()
        reset()
        print("Step 2: Largest Object")

    def _update():
        if not _launcher.done:        # arm + climb to a safe height first
            _launcher.update(_drone)
            return
        if update(_drone):
            _drone.flight.land()

    _drone.set_start_update(start, _update)
    _drone.go()
