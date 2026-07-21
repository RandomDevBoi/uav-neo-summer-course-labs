"""
MIT BWSI Autonomous Drone Racing Course - UAV Neo
GNU General Public License v3.0

Week 4 · Module 1 — Step 2: Go To a Waypoint
Fly to a target point given as (right, up, forward) meters from the start. This is
your first controller that drives three axes at once: roll for right, pitch for
forward, throttle for up.
"""

import drone_core
import drone_utils as uav_utils

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
TARGET_RIGHT = 2.0
TARGET_FWD = 4.0
TARGET_HEIGHT = 3.0
KP_POS = 0.15
KD_POS = 0.5            # brake with velocity so you don't overshoot
ALT_KP = 0.12
ROLL_LIMIT = 0.25
PITCH_LIMIT = 0.25
THROTTLE_LIMIT = 0.5
POS_TOL = 0.5          # meters from target counted as arrived
SETTLE_SPEED = 0.25    # must slow below this to finish
HOLD_TIME = 1.5

# -- Module-level state -----------------------------------------------------
_x = 0.0
_z = 0.0
_x_prev_d = 0.0
_z_prev_d = 0.0
_hold = 0.0
_done = False

def reset():
    global _x, _z, _x_prev_d, _z_prev_d, _hold, _done
    _x = 0.0
    _z = 0.0
    _x_prev_d = 0.0
    _z_prev_d = 0.0
    _hold = 0.0
    _done = False


def update(drone):
    global _x, _z, _x_prev_d, _z_prev_d, _hold, _done
    if _done:
        return True
    ##################################
    #### START PUT CODE HERE #########

    # GOAL: fly to (TARGET_RIGHT, TARGET_HEIGHT, TARGET_FWD) and hold there.
    #
    # Tools: drone.physics.get_linear_velocity() -> (vx, vy, vz); drone.get_delta_time();
    #        neo_lab.height(drone); uav_utils.clamp(...); drone.flight.send_pcmd(...).
    #
    # Track right/forward position by integrating vx, vz like Step 1. Drive each
    # horizontal axis with a PD controller (gain KP_POS on position error and KD_POS on
    # velocity, which brakes you): roll for the right error, pitch for the forward error.
    # Hold height with a proportional term (ALT_KP). Clamp each to its limit. Finish when
    # both horizontal errors are under POS_TOL and speed is under SETTLE_SPEED for HOLD_TIME.
    dt = drone.get_delta_time()

    vx, _, vz = drone.physics.get_linear_velocity()
    _x += vx * dt
    y = neo_lab.height(drone)
    _z += vz * dt

    z_err = (TARGET_FWD - _z) 
    x_err = (TARGET_RIGHT - _x) 
    y_err = (TARGET_HEIGHT - y) 

    #low pass filter (experimental)
    #it seems the sim is still jittery, perhaps due to the instant acceleration of the props which doesn't happen IRL
    _z_filtered_d = _z_prev_d = 0.3 * (vz * KD_POS) + 0.7 * _z_prev_d
    _x_filtered_d = _x_prev_d = 0.3 * (vx * KD_POS) + 0.7 * _x_prev_d

    #commands
    pitch = uav_utils.clamp((z_err * KP_POS) - _z_filtered_d, -PITCH_LIMIT, PITCH_LIMIT)
    roll = uav_utils.clamp((x_err * KP_POS) - _x_filtered_d, -ROLL_LIMIT, ROLL_LIMIT)
    throttle = uav_utils.clamp(y_err * ALT_KP, -THROTTLE_LIMIT, THROTTLE_LIMIT)
    drone.flight.send_pcmd(pitch, roll, 0, throttle)

    speed = pow(vx**2 + vz**2, 0.5)
    if abs(z_err) < POS_TOL and abs(x_err) < POS_TOL and abs(y_err) < POS_TOL and speed < SETTLE_SPEED:
        _hold += dt
    else:
        _hold = 0.0

    if _hold >= HOLD_TIME:
        drone.flight.stop()
        print(f"Estimated Position (Z, X, Y): ({_z:.3f}, {_x:.3f}, {y:.3f})")
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
        print("Step 2: Go To a Waypoint")

    def _update():
        if not _launcher.done:        # arm + climb to a safe height first
            _launcher.update(_drone)
            return
        if update(_drone):
            _drone.flight.land()

    _drone.set_start_update(start, _update)
    _drone.go()
