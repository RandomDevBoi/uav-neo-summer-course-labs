"""
MIT BWSI Autonomous Drone Racing Course - UAV Neo
GNU General Public License v3.0

Week 2/3 Lab — Step 2: Fly a Distance (PID on Position)
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
    ##################################
    #### START PUT CODE HERE #########
    output = 0.0  # YOUR CODE HERE (combine the three gain terms)
    ###### END PUT CODE HERE #########
    ##################################
    return output

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
    ##################################
    #### START PUT CODE HERE #########

    # We have no direct (x, z) position, so integrate velocity to estimate distance.
    # 1. dt = drone.get_delta_time()
    # 2. velocity = drone.physics.get_linear_velocity()   # (x=right, y=up, z=forward)
    # 3. _pos += velocity[2] * dt
    # 4. error = TARGET_DIST - _pos ; update _err_int, err_dot, _prev_err (see Step 1).
    # 5. pitch = uav_utils.clamp(pid_control(error, _err_int, err_dot, KP, KI, KD), -0.5, 0.5)
    # 6. Hold altitude too: throttle = clamp(ALT_KP*(TARGET_ALT - get_altitude()), -1, 1)
    # 7. send_pcmd(pitch, 0, 0, throttle); finish once within DIST_TOL for HOLD_TIME

    ###### END PUT CODE HERE #########
    ##################################
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
