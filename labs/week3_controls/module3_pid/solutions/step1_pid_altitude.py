"""
MIT BWSI Autonomous Drone Racing Course - UAV Neo
GNU General Public License v3.0

Week 2/3 Lab — Step 1: PID Altitude Hold  (SOLUTION)
Hold altitude with a full PID controller (P + I + D).
Source: simple_feedback_control.ipynb (pid_control, 1-D quad).
"""

import drone_core
import drone_utils as uav_utils

# -- Constants --------------------------------------------------------------
TARGET_ALT = 2.5
KP = 0.9
KI = 0.25
KD = 0.35
INT_CLAMP = 1.0      # anti-windup limit on the integral
ALT_TOL = 0.10
HOLD_TIME = 3.0

# -- Module-level state -----------------------------------------------------
_err_int = 0.0
_prev_err = 0.0
_hold = 0.0
_done = False

def pid_control(err, err_int, err_dot, kp, ki, kd):
    """Standard PID law: output = kp*err + ki*err_int + kd*err_dot."""
    return kp * err + ki * err_int + kd * err_dot

def reset():
    global _err_int, _prev_err, _hold, _done
    _err_int = 0.0
    _prev_err = 0.0
    _hold = 0.0
    _done = False


def update(drone):
    global _err_int, _prev_err, _hold, _done
    if _done:
        return True
    dt = drone.get_delta_time()
    altitude = drone.physics.get_altitude()
    error = TARGET_ALT - altitude
    _err_int = uav_utils.clamp(_err_int + error * dt, -INT_CLAMP, INT_CLAMP)
    err_dot = (error - _prev_err) / dt if dt > 0 else 0.0
    _prev_err = error
    throttle = uav_utils.clamp(pid_control(error, _err_int, err_dot, KP, KI, KD), -1.0, 1.0)
    drone.flight.send_pcmd(0, 0, 0, throttle)
    if abs(error) < ALT_TOL:
        _hold += dt
    else:
        _hold = 0.0
    if _hold >= HOLD_TIME:
        drone.flight.stop()
        print(f"[Step 1] PID held {TARGET_ALT}m (final {altitude:.2f}m)")
        _done = True
    return _done


if __name__ == "__main__":
    _drone = drone_core.create_drone()
    _launched = False

    def start():
        reset()
        print("Step 1: PID Altitude Hold")

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
