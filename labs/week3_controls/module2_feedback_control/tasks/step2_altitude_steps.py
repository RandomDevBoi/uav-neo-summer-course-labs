"""
MIT BWSI Autonomous Drone Racing Course - UAV Neo
GNU General Public License v3.0

Week 2/3 Lab — Step 2: Altitude Setpoint Sequence
Chase a sequence of target heights (a step response).
Source: simple_feedback_control.ipynb (closed-loop tracking).
"""

import drone_core
import drone_utils as uav_utils

import os as _os, sys as _sys
_d = _os.path.dirname(_os.path.abspath(__file__))
while _os.path.basename(_d) != "labs" and _os.path.dirname(_d) != _d:
    _d = _os.path.dirname(_d)
if _d not in _sys.path:
    _sys.path.insert(0, _d)
import neo_lab

# -- Constants --------------------------------------------------------------
SETPOINTS = [3.0, 6.0, 2.0]   # meters above ground, in order
KP = 0.2
THROTTLE_LIMIT = 0.5
TOL = 0.4
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
    # 3. error = target - neo_lab.height(drone)
    # 4. throttle = uav_utils.clamp(KP * error, -THROTTLE_LIMIT, THROTTLE_LIMIT)
    # 5. Accumulate _hold while abs(error) < TOL.
    # 6. When _hold >= HOLD_TIME: advance _index += 1 and reset _hold = 0.0

    ###### END PUT CODE HERE #########
    ##################################
    return _done


if __name__ == "__main__":
    _drone = drone_core.create_drone()
    _launcher = neo_lab.Launcher(3.0)

    def start():
        _launcher.reset()
        reset()
        print("Step 2: Altitude Setpoint Sequence")

    def _update():
        if not _launcher.done:        # arm + climb to a safe height first
            _launcher.update(_drone)
            return
        if update(_drone):
            _drone.flight.land()

    _drone.set_start_update(start, _update)
    _drone.go()
