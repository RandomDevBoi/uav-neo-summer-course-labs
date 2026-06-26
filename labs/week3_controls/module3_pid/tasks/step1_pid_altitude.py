"""
MIT BWSI Autonomous Drone Racing Course - UAV Neo
GNU General Public License v3.0

Week 2/3 Lab — Step 1: PID Altitude Hold
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
    ##################################
    #### START PUT CODE HERE #########
    output = 0.0  # YOUR CODE HERE (combine the three gain terms)
    ###### END PUT CODE HERE #########
    ##################################
    return output

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
    ##################################
    #### START PUT CODE HERE #########

    # Implement pid_control() above first, then wire it up here:
    # 1. dt = drone.get_delta_time()
    # 2. error = TARGET_ALT - drone.physics.get_altitude()
    # 3. _err_int = uav_utils.clamp(_err_int + error * dt, -INT_CLAMP, INT_CLAMP)  # anti-windup
    # 4. err_dot = (error - _prev_err) / dt if dt > 0 else 0.0 ; then _prev_err = error
    # 5. throttle = uav_utils.clamp(pid_control(error, _err_int, err_dot, KP, KI, KD), -1, 1)
    # 6. send_pcmd(0, 0, 0, throttle)
    # 7. Accumulate _hold while abs(error) < ALT_TOL; finish after HOLD_TIME

    ###### END PUT CODE HERE #########
    ##################################
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
