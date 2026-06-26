"""
MIT BWSI Autonomous Drone Racing Course - UAV Neo
GNU General Public License v3.0

Week 2/3 Lab — Step 3: Center Over the Object  (SOLUTION)
Visual-servo the drone to hover directly above the object.
Source: 04_Downward.ipynb applied live (downward camera).
"""

import drone_core
import drone_utils as uav_utils
import cv2
import numpy as np

# -- Constants --------------------------------------------------------------
SAT_MIN = 100
VAL_MIN = 60
MIN_AREA = 300
MAX_TILT = 0.20      # pitch/roll authority
CENTER_TOL = 40      # pixels considered 'centered'
HOLD_TIME = 2.0      # seconds to stay centered before done
ROW_CENTER = 240
COL_CENTER = 320

# -- Module-level state -----------------------------------------------------
_hold = 0.0
_done = False

def reset():
    global _hold, _done
    _hold = 0.0
    _done = False


def update(drone):
    global _hold, _done
    if _done:
        return True
    image = drone.camera.get_downward_image()
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = ((hsv[:, :, 1] > SAT_MIN) & (hsv[:, :, 2] > VAL_MIN)).astype(np.uint8) * 255
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    best = uav_utils.get_largest_contour(contours, MIN_AREA)
    if best is None:
        drone.flight.stop()
        _hold = 0.0
        return False
    row, col = uav_utils.get_contour_center(best)
    err_col = col - COL_CENTER               # +ve => object is to the right
    err_row = row - ROW_CENTER               # +ve => object is behind (toward image bottom)
    roll = uav_utils.clamp(err_col / COL_CENTER * MAX_TILT, -MAX_TILT, MAX_TILT)
    pitch = uav_utils.clamp(-err_row / ROW_CENTER * MAX_TILT, -MAX_TILT, MAX_TILT)
    drone.flight.send_pcmd(pitch, roll, 0, 0)
    if abs(err_col) < CENTER_TOL and abs(err_row) < CENTER_TOL:
        _hold += drone.get_delta_time()
    else:
        _hold = 0.0
    if _hold >= HOLD_TIME:
        drone.flight.stop()
        print("[Step 3] Centered over the object")
        _done = True
    return _done


if __name__ == "__main__":
    _drone = drone_core.create_drone()
    _launched = False

    def start():
        reset()
        print("Step 3: Center Over the Object")

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
