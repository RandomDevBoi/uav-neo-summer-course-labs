"""
MIT BWSI Autonomous Drone Racing Course - UAV Neo
GNU General Public License v3.0

Week 2/3 Lab — Step 2: Morphology (Opening)
Clean a binary mask with erosion followed by dilation (an 'opening').
"""

import drone_core
import drone_utils as uav_utils
import cv2
import numpy as np

# -- Course setup: makes the shared `neo_lab` helper importable.
#    You don't need to read or change this block. --
import os as _os, sys as _sys
_d = _os.path.dirname(_os.path.realpath(__file__))
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
    
    # Opening (erode then dilate) removes small speckles but keeps big shapes. Build a
    # binary mask like Step 1, then open it with a KERNEL_SIZE square kernel and compare
    # the white-pixel count before and after to see what was removed. Advance _timer and
    # finish once it reaches HOVER_TIME. See the README (Key terms) for morphology.

    _timer += drone.get_delta_time()
    
    img = drone.camera.get_downward_image()
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary_mask = cv2.threshold(gray_img, THRESHOLD_VALUE, 255, cv2.THRESH_BINARY)

    #Opening
    kernel = np.ones((KERNEL_SIZE, KERNEL_SIZE), np.uint8)
    opened = cv2.dilate(cv2.erode(binary_mask, kernel, iterations=1), kernel, iterations=1)

    #Comparing
    white_pixels_before = np.count_nonzero(binary_mask)
    white_pixels_after = np.count_nonzero(opened)

    #Printing
    print(f"Time: {_timer:.2f} | Before Pixels: {white_pixels_before} | After Pixels: {white_pixels_after} | Total Removed Pixels: {(white_pixels_before - white_pixels_after)}")
    
    if _timer >= HOVER_TIME:
        print(f"Final | Time: {_timer:.2f} | Before Pixels: {white_pixels_before} | After Pixels: {white_pixels_after} | Total Removed Pixels: {(white_pixels_before - white_pixels_after)}")
        _done = True

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
