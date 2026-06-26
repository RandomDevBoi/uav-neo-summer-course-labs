"""
MIT BWSI Autonomous Drone Racing Course - UAV Neo
GNU General Public License v3.0

Week 2/3 Lab — Step 3: Visual Servoing (Vision + PID)  (SOLUTION)
Capstone: use a PID loop on the camera pixel error to keep a red
object centered by yawing. Combines Week 2 vision with Week 3 control.
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
MIN_AREA = 300
COL_CENTER = 320
KP = 0.6
KI = 0.05
KD = 0.2
MAX_YAW = 0.5
CENTER_TOL = 0.05    # normalized error considered centered
HOLD_TIME = 3.0

# -- Module-level state -----------------------------------------------------
_err_int = 0.0
_prev_err = 0.0
_hold = 0.0
_done = False

def pid_control(err, err_int, err_dot, kp, ki, kd):
    """Standard PID law: output = kp*err + ki*err_int + kd*err_dot."""
    return kp * err + ki * err_int + kd * err_dot

def reset():
    global _err_int, _prev_err, _hold, _done
    _err_int = 0.0
    _prev_err = 0.0
    _hold = 0.0
    _done = False


def update(drone):
    global _err_int, _prev_err, _hold, _done
    if _done:
        return True
    dt = drone.get_delta_time()
    image = drone.camera.get_color_image()
    contours = (uav_utils.find_contours(image, LOWER1, UPPER1) +
                uav_utils.find_contours(image, LOWER2, UPPER2))
    best = uav_utils.get_largest_contour(contours, MIN_AREA)
    if best is None:
        drone.flight.stop()
        _err_int = 0.0                           # reset integral when target is lost
        _hold = 0.0
        return False
    row, col = uav_utils.get_contour_center(best)
    error = (col - COL_CENTER) / COL_CENTER      # normalized -1..+1
    _err_int = uav_utils.clamp(_err_int + error * dt, -1.0, 1.0)
    err_dot = (error - _prev_err) / dt if dt > 0 else 0.0
    _prev_err = error
    yaw = uav_utils.clamp(pid_control(error, _err_int, err_dot, KP, KI, KD), -MAX_YAW, MAX_YAW)
    drone.flight.send_pcmd(0, 0, yaw, 0)
    if abs(error) < CENTER_TOL:
        _hold += dt
    else:
        _hold = 0.0
    if _hold >= HOLD_TIME:
        drone.flight.stop()
        print("[Step 3] Locked onto the target")
        _done = True
    return _done


if __name__ == "__main__":
    _drone = drone_core.create_drone()
    _launched = False

    def start():
        reset()
        print("Step 3: Visual Servoing (Vision + PID)")

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
