"""
MIT BWSI Autonomous Drone Racing Course - UAV Neo
GNU General Public License v3.0

Week 2/3 Lab — Step 2: Morphology (Opening)  (SOLUTION)
Clean a binary mask with erosion followed by dilation (an 'opening').
Source: 02_OpenCV.ipynb (cv2.erode / cv2.dilate).
"""

import drone_core
import drone_utils as uav_utils
import cv2
import numpy as np

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
    _timer += drone.get_delta_time()
    image = drone.camera.get_downward_image()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, THRESHOLD_VALUE, 255, cv2.THRESH_BINARY)
    kernel = np.ones((KERNEL_SIZE, KERNEL_SIZE), np.uint8)
    eroded = cv2.erode(mask, kernel, iterations=1)
    opened = cv2.dilate(eroded, kernel, iterations=1)
    before = np.count_nonzero(mask)
    after = np.count_nonzero(opened)
    if _timer >= HOVER_TIME:
        print(f"[Step 2] Opening with {KERNEL_SIZE}x{KERNEL_SIZE} kernel removed "
              f"{before - after} speckle pixels ({before} -> {after})")
        _done = True
    return _done


if __name__ == "__main__":
    _drone = drone_core.create_drone()
    _launched = False

    def start():
        reset()
        print("Step 2: Morphology (Opening)")

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
