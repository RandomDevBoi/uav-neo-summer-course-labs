"""
MIT BWSI Autonomous Drone Racing Course - UAV Neo
GNU General Public License v3.0

Week 2/3 Lab — Step 2: Fly a Distance (PID on Position)  (SOLUTION)
Integrate forward velocity into position and PID to a target distance,
while a proportional term keeps altitude.
Source: simple_feedback_control.ipynb (2-D quad).
"""

import drone_core
import drone_utils as uav_utils

# -- Constants --------------------------------------------------------------
TARGET_DIST = 4.0    # meters forward
TARGET_ALT  = 2.5
KP = 0.5
KI = 0.0
KD = 0.4
ALT_KP = 0.8
DIST_TOL = 0.25
HOLD_TIME = 2.0

# -- Module-level state -----------------------------------------------------
_pos = 0.0
_err_int = 0.0
_prev_err = 0.0
_hold = 0.0
_done = False

def pid_control(err, err_int, err_dot, kp, ki, kd):
    """Standard PID law: output = kp*err + ki*err_int + kd*err_dot."""
    return kp * err + ki * err_int + kd * err_dot

def reset():
    global _pos, _err_int, _prev_err, _hold, _done
    _pos = 0.0
    _err_int = 0.0
    _prev_err = 0.0
    _hold = 0.0
    _done = False


def update(drone):
    global _pos, _err_int, _prev_err, _hold, _done
    if _done:
        return True
    dt = drone.get_delta_time()
    velocity = drone.physics.get_linear_velocity()
    _pos += velocity[2] * dt                     # z axis points forward
    error = TARGET_DIST - _pos
    _err_int += error * dt
    err_dot = (error - _prev_err) / dt if dt > 0 else 0.0
    _prev_err = error
    pitch = uav_utils.clamp(pid_control(error, _err_int, err_dot, KP, KI, KD), -0.5, 0.5)
    throttle = uav_utils.clamp(ALT_KP * (TARGET_ALT - drone.physics.get_altitude()), -1.0, 1.0)
    drone.flight.send_pcmd(pitch, 0, 0, throttle)
    if abs(error) < DIST_TOL:
        _hold += dt
    else:
        _hold = 0.0
    if _hold >= HOLD_TIME:
        drone.flight.stop()
        print(f"[Step 2] Reached {TARGET_DIST}m forward (estimate {_pos:.2f}m)")
        _done = True
    return _done


if __name__ == "__main__":
    _drone = drone_core.create_drone()
    _launched = False

    def start():
        reset()
        print("Step 2: Fly a Distance (PID on Position)")

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
