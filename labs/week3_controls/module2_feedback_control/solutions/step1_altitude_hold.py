"""
MIT BWSI Autonomous Drone Racing Course - UAV Neo
GNU General Public License v3.0

Week 2/3 Lab — Step 1: Proportional Altitude Hold  (SOLUTION)
Hold a target altitude using proportional throttle control.
Source: simple_feedback_control.ipynb (p_control).
"""

import drone_core
import drone_utils as uav_utils

# -- Constants --------------------------------------------------------------
TARGET_ALT = 2.5      # meters
KP = 0.8             # proportional gain
ALT_TOL = 0.15       # meters considered 'on target'
HOLD_TIME = 3.0      # seconds on target before done

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
    altitude = drone.physics.get_altitude()
    error = TARGET_ALT - altitude
    throttle = uav_utils.clamp(KP * error, -1.0, 1.0)
    drone.flight.send_pcmd(0, 0, 0, throttle)
    if abs(error) < ALT_TOL:
        _hold += drone.get_delta_time()
    else:
        _hold = 0.0
    if _hold >= HOLD_TIME:
        drone.flight.stop()
        print(f"[Step 1] Held {TARGET_ALT}m (final {altitude:.2f}m)")
        _done = True
    return _done


if __name__ == "__main__":
    _drone = drone_core.create_drone()
    _launched = False

    def start():
        reset()
        print("Step 1: Proportional Altitude Hold")

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
