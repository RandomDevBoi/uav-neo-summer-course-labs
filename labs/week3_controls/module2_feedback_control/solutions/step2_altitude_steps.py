"""
MIT BWSI Autonomous Drone Racing Course - UAV Neo
GNU General Public License v3.0

Week 2/3 Lab — Step 2: Altitude Setpoint Sequence  (SOLUTION)
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
    if _index >= len(SETPOINTS):
        drone.flight.stop()
        print("[Step 2] Visited all setpoints")
        _done = True
        return _done
    target = SETPOINTS[_index]
    altitude = drone.physics.get_altitude()
    error = target - altitude
    throttle = uav_utils.clamp(KP * error, -1.0, 1.0)
    drone.flight.send_pcmd(0, 0, 0, throttle)
    if abs(error) < ALT_TOL:
        _hold += drone.get_delta_time()
    else:
        _hold = 0.0
    if _hold >= HOLD_TIME:
        print(f"[Step 2] Reached setpoint {target}m")
        _index += 1
        _hold = 0.0
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
