"""
MIT BWSI Autonomous Drone Racing Course - UAV Neo
GNU General Public License v3.0

File Name: neo_lab.py
Shared helpers for the simulator labs.

Why this exists
---------------
In the UAV Neo simulator the drone does NOT spawn at altitude 0 — it reads a
ground offset (e.g. ~7 m), and `takeoff()` alone does not climb. Throttle acts
like a vertical-velocity command (≈12 m/s per unit) and `stop()` holds altitude.

So every flying lab must:
  1. ARM by calling `takeoff()` for a moment, then
  2. CLIMB to a working height using throttle, measuring altitude RELATIVE to the
     ground sampled at launch.

`Launcher` does exactly that, and `height(drone)` gives altitude above the ground
captured at launch so labs never hardcode the absolute spawn altitude.
"""

import drone_utils as uav_utils

_ground_alt = 0.0


def set_ground(alt):
    """Record the ground altitude (sampled once at launch)."""
    global _ground_alt
    _ground_alt = alt


def ground():
    """The ground altitude captured at launch (meters, absolute)."""
    return _ground_alt


def height(drone):
    """Altitude above the launch ground, in meters."""
    return drone.physics.get_altitude() - _ground_alt


class Launcher:
    """
    Arms the drone and climbs to `target_height` meters above the ground measured
    when launching begins. Call update(drone) every frame until it returns True.

    Throttle is a velocity command, so the proportional gain is intentionally small.
    """

    def __init__(self, target_height=3.0, kp=0.2, throttle_limit=0.5,
                 tol=0.4, arm_time=1.5, settle=1.0):
        self.target_height = target_height
        self.kp = kp
        self.throttle_limit = throttle_limit
        self.tol = tol
        self.arm_time = arm_time
        self.settle = settle
        self.reset()

    def reset(self):
        self._t = 0.0
        self._hold = 0.0
        self._ground_set = False
        self.done = False

    def update(self, drone):
        if self.done:
            return True
        dt = drone.get_delta_time()
        if not self._ground_set:
            set_ground(drone.physics.get_altitude())
            self._ground_set = True

        # Phase 1: arm the motors.
        self._t += dt
        if self._t < self.arm_time:
            drone.flight.takeoff()
            return False

        # Phase 2: climb to target height (throttle ~ vertical velocity).
        err = self.target_height - height(drone)
        throttle = uav_utils.clamp(self.kp * err, -self.throttle_limit,
                                   self.throttle_limit)
        drone.flight.send_pcmd(0, 0, 0, throttle)
        self._hold = self._hold + dt if abs(err) < self.tol else 0.0
        if self._hold >= self.settle:
            drone.flight.stop()
            self.done = True
            print(f"[launch] airborne {height(drone):.2f} m above ground "
                  f"(ground={ground():.2f} m)")
        return self.done
