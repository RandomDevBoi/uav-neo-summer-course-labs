"""
MIT BWSI Autonomous Drone Racing Course - UAV Neo
GNU General Public License v3.0

Week 2/3 Lab — Step 2: Altitude Setpoint Sequence
Chase a sequence of altitude setpoints (a step response).
Source: simple_feedback_control.ipynb (closed-loop tracking).
"""

import drone_core
import drone_utils as uav_utils

# -- Constants --------------------------------------------------------------
SETPOINTS = [2.0, 3.5, 1.5]   # meters, visited in order
KP = 0.8
ALT_TOL = 0.15
HOLD_TIME = 2.0

# -- Module-level state -----------------------------------------------------
_index = 0
_hold = 0.0
_done = False

def reset():
    global _index, _hold, _done
    _index = 0
    _hold = 0.0
    _done = False


def update(drone):
    global _index, _hold, _done
    if _done:
        return True
    ##################################
    #### START PUT CODE HERE #########

    # Reuse your proportional controller, but the target changes over time.
    # 1. If _index >= len(SETPOINTS): stop, set _done = True, return.
    # 2. target = SETPOINTS[_index]
    # 3. error = target - drone.physics.get_altitude()
    # 4. throttle = uav_utils.clamp(KP * error, -1.0, 1.0); send it on the throttle axis.
    # 5. Accumulate _hold while abs(error) < ALT_TOL.
    # 6. When _hold >= HOLD_TIME: advance _index += 1 and reset _hold = 0.0

    ###### END PUT CODE HERE #########
    ##################################
    return _done


if __name__ == "__main__":
    _drone = drone_core.create_drone()
    _launched = False

    def start():
        reset()
        print("Step 2: Altitude Setpoint Sequence")

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
