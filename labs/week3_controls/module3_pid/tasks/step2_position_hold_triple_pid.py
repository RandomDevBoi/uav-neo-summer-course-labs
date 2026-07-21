"""
MIT BWSI Autonomous Drone Racing Course - UAV Neo
GNU General Public License v3.0

Week 2/3 Lab — Step 2: Fly a Distance (PID on Position)
Integrate forward velocity into position and PID to a target distance,
while a proportional term keeps altitude.
"""

import drone_core
import drone_utils as uav_utils
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
#Using Unity Conventions (ZXY)
TARGET = np.array([4.0, -2.0, 3.0])
KP = np.array([0.15, 0.15, 0.18])    # per axis: z, x, y
KI = np.array([0.00, 0.00, 0.06])
KD = np.array([0.50, 0.50, 0.02]) 
OUT_LIMIT = np.array([0.25, 0.25, 0.5]) #Pitch limit, Pitch limit, Throttle Limit
INT_CLAMP = 3.0 #anti windup, derived from step 1
MIN_TRAVEL = 5.0   # fly at least this long before checking 'arrived'
SETTLE_SPEED = 0.25  # must slow below this to count as arrived
HOLD_TIME = 1.5

# -- Module-level state -----------------------------------------------------
_p = np.array([0.0, 0.0, 0.0]) #p stands for position
_err_int = np.array([0.0, 0.0, 0.0])
_err_dot = np.array([0.0, 0.0 ,0.0])
_t = 0.0
_hold = 0.0
_done = False

def pid_control(err, err_int, err_dot, kp, ki, kd):
    """Return the PID controller output from the three gain terms (see README, Key terms)."""
    ##################################
    #### START PUT CODE HERE #########
    p = kp * err
    i = ki * err_int
    d = kd * err_dot
    output = p + i + d
    ###### END PUT CODE HERE #########
    ##################################
    return output

def reset():
    global _p, _err_int, _err_dot, _t, _hold, _done
    _p = np.array([0.0, 0.0, 0.0])
    _err_int = np.array([0.0, 0.0, 0.0])
    _err_dot = np.array([0.0, 0.0, 0.0])
    _t = 0.0
    _hold = 0.0
    _done = False


def update(drone):
    global _p, _err_int, _err_dot, _t, _hold, _done
    if _done:
        return True
    ##################################
    #### START PUT CODE HERE #########

    # There is no direct (x, z) readout, so estimate forward distance by dead reckoning:
    # integrate the forward component of drone.physics.get_linear_velocity() over time.
    # PID that distance to TARGET_DIST for the pitch command (clamped to PITCH_LIMIT), and
    # use a proportional term (ALT_KP) on height to hold TARGET_HEIGHT. Count as arrived
    # only after MIN_TRAVEL, once speed drops below SETTLE_SPEED for HOLD_TIME. See the
    # README (Key terms) for dead reckoning and the PID law.
 
    dt = drone.get_delta_time() #same reason as previously, drone.get_delta_time() could change throughout update
    _t += dt
    vel = np.asarray(drone.physics.get_linear_velocity())[[2, 0, 1]]

    #estimates
    _p += vel * dt
    _p[2] = neo_lab.height(drone)

    #PID
    err = TARGET - _p
    _err_int = np.clip(_err_int + err * dt, -INT_CLAMP, INT_CLAMP)
    #err_dot = -vel #old jittery one
    raw_err_dot = -vel
    _err_dot = 0.95 * _err_dot + 0.05 * raw_err_dot #low pass filtered version
    out = np.clip(pid_control(err, _err_int, _err_dot, KP, KI, KD), -OUT_LIMIT, OUT_LIMIT)
    drone.flight.send_pcmd(out[0], out[1], 0, out[2])

    if _t > MIN_TRAVEL and abs(vel[0]) < SETTLE_SPEED and abs(vel[1]) < SETTLE_SPEED and abs(vel[2]) < SETTLE_SPEED:
        _hold += dt
    else: 
        _hold = 0.0
    if _hold >= HOLD_TIME:
        drone.flight.stop()
        print(f"Estimated Position: ({_p[0]}, {_p[1]}, {_p[2]}) [we actually know y]")
        print(f"Target Position: ({TARGET[0]}, {TARGET[1]}, {TARGET[2]})")
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
        print("Step 2: Fly a Distance (PID on Position)")

    def _update():
        if not _launcher.done:        # arm + climb to a safe height first
            _launcher.update(_drone)
            return
        if update(_drone):
            _drone.flight.land()

    _drone.set_start_update(start, _update)
    _drone.go()
