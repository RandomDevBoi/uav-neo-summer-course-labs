"""
MIT BWSI Autonomous Drone Racing Course - UAV Neo
GNU General Public License v3.0

Week 3 · Module 3 — PID Control — SOLUTION orchestrator

Runs every step in sequence against the simulator:
    drone sim module3_pid/main_solution.py
Run a single step directly instead:
    drone sim solutions/<step_file>.py
"""

import drone_core
from solutions import (
    step1_pid_altitude,
    step2_position_hold,
    step3_visual_servo,
)

drone = drone_core.create_drone()

_STEPS = [
    ("Step 1: PID Altitude Hold", step1_pid_altitude),
    ("Step 2: Fly a Distance (PID on Position)", step2_position_hold),
    ("Step 3: Visual Servoing (Vision + PID)", step3_visual_servo)
]

_launched = False
_index = 0


def start():
    global _launched, _index
    _launched = False
    _index = 0
    print("\n" + "=" * 56)
    print("  Week 3 · Module 3 — PID Control")
    print("=" * 56 + "\n")


def update():
    global _launched, _index
    if not _launched:
        drone.flight.takeoff()
        if drone.physics.get_altitude() > 1.0:
            _launched = True
            _STEPS[0][1].reset()
            print(f"--- {_STEPS[0][0]} ---")
        return

    if _index >= len(_STEPS):
        drone.flight.land()
        return

    name, mod = _STEPS[_index]
    if mod.update(drone):
        _index += 1
        if _index < len(_STEPS):
            _STEPS[_index][1].reset()
            print(f"\n--- {_STEPS[_index][0]} ---")
        else:
            print("\n=== Module complete! Landing... ===")


def update_slow():
    if _launched and _index < len(_STEPS):
        print(f"[{_STEPS[_index][0]}] alt={drone.physics.get_altitude():.2f}m")


if __name__ == "__main__":
    drone.set_start_update(start, update, update_slow)
    drone.go()
