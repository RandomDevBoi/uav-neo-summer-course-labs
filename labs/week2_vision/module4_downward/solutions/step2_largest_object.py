"""
MIT BWSI Autonomous Drone Racing Course - UAV Neo
GNU General Public License v3.0

Week 2/3 Lab — Step 2: Largest Object  (SOLUTION)
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
    _timer += drone.get_delta_time()
    image = drone.camera.get_downward_image()
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = ((hsv[:, :, 1] > SAT_MIN) & (hsv[:, :, 2] > VAL_MIN)).astype(np.uint8) * 255
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    best = uav_utils.get_largest_contour(contours, MIN_AREA)
    if best is None:
        return False
    center = uav_utils.get_contour_center(best)     # (row, col)
    area = uav_utils.get_contour_area(best)
    if _timer >= HOVER_TIME:
        print(f"[Step 2] Largest object at row={center[0]}, col={center[1]}, "
              f"area={area:.0f}")
        _done = True
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
