"""
MIT BWSI Autonomous Drone Racing Course - UAV Neo
GNU General Public License v3.0

Week 2/3 Lab — Step 3: Blur & Edge Detection
Averaging blur then a Sobel edge-magnitude image.
Source: 02_OpenCV.ipynb (averaging kernel, Sobel stretch goal).
"""

import drone_core
import drone_utils as uav_utils
import cv2
import numpy as np

# -- Constants --------------------------------------------------------------
KERNEL_SIZE = 5
HOVER_TIME  = 3.0

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

    # 1. gray    = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 2. blurred = cv2.blur(gray, (KERNEL_SIZE, KERNEL_SIZE))
    # 3. sobel_x = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
    #    sobel_y = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=3)
    # 4. magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
    # 5. When _timer >= HOVER_TIME: print magnitude.mean(), set _done = True

    ###### END PUT CODE HERE #########
    ##################################
    return _done


if __name__ == "__main__":
    _drone = drone_core.create_drone()
    _launched = False

    def start():
        reset()
        print("Step 3: Blur & Edge Detection")

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
