"""
MIT BWSI Autonomous Drone Racing Course - UAV Neo
GNU General Public License v3.0

Week 2/3 Lab — Step 2: Fit a Line (Least Squares)  (SOLUTION)
Fit y = m*x + b to the line pixels with linear regression.
Source: 03_LinearRegression.ipynb (calculate_regression).
"""

import drone_core
import drone_utils as uav_utils
import cv2
import numpy as np

# -- Constants --------------------------------------------------------------
SAT_MIN    = 80
VAL_MIN    = 60
MIN_PIXELS = 200
HOVER_TIME = 3.0

# -- Module-level state -----------------------------------------------------
_timer = 0.0
_done  = False

def fit_line(points):
    """Least-squares fit of y = m*x + b. points is the (row, col) array from
    np.argwhere, so column = x and row = y."""
    points = points.astype(np.float64)
    ys = points[:, 0]
    xs = points[:, 1]
    m, b = np.polyfit(xs, ys, 1)
    return m, b

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
    mask = (hsv[:, :, 1] > SAT_MIN) & (hsv[:, :, 2] > VAL_MIN)
    points = np.argwhere(mask)             # array of (row, col)
    if len(points) < MIN_PIXELS:
        return False                        # not enough of the line in view yet
    m, b = fit_line(points)
    if _timer >= HOVER_TIME:
        print(f"[Step 2] Fitted line slope m={m:.3f}, intercept b={b:.1f}")
        _done = True
    return _done


if __name__ == "__main__":
    _drone = drone_core.create_drone()
    _launched = False

    def start():
        reset()
        print("Step 2: Fit a Line (Least Squares)")

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
