"""
MIT BWSI Autonomous Drone Racing Course - UAV Neo
GNU General Public License v3.0

Week 2/3 Lab — Step 1: Grayscale Thresholding  (SOLUTION)
Grayscale + binary threshold of the live downward camera feed.
Source: 02_OpenCV.ipynb (cv2.threshold).
"""

import drone_core
import drone_utils as uav_utils
import cv2
import numpy as np

# -- Constants --------------------------------------------------------------
THRESHOLD_VALUE = 127     # grayscale cutoff (0-255)
HOVER_TIME      = 3.0     # seconds to observe

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
    image = drone.camera.get_downward_image()              # 480x640x3 BGR
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, THRESHOLD_VALUE, 255, cv2.THRESH_BINARY)
    white_frac = np.count_nonzero(binary) / binary.size
    if _timer >= HOVER_TIME:
        print(f"[Step 1] Threshold @ {THRESHOLD_VALUE}: "
              f"{white_frac * 100:.1f}% of pixels are white")
        _done = True
    return _done


if __name__ == "__main__":
    _drone = drone_core.create_drone()
    _launched = False

    def start():
        reset()
        print("Step 1: Grayscale Thresholding")

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
