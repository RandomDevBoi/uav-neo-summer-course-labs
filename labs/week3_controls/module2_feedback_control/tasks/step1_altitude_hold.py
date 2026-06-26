"""
MIT BWSI Autonomous Drone Racing Course - UAV Neo
GNU General Public License v3.0

Week 2/3 Lab — Step 1: Proportional Altitude Hold
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
    ##################################
    #### START PUT CODE HERE #########

    # Proportional control:  output = Kp * error
    # 1. altitude = drone.physics.get_altitude()
    # 2. error = TARGET_ALT - altitude
    # 3. throttle = uav_utils.clamp(KP * error, -1.0, 1.0)
    # 4. drone.flight.send_pcmd(0, 0, 0, throttle)
    # 5. Accumulate _hold while abs(error) < ALT_TOL (else reset _hold = 0).
    # 6. When _hold >= HOLD_TIME: stop and set _done = True

    ###### END PUT CODE HERE #########
    ##################################
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
