"""
MIT BWSI Autonomous Drone Racing Course - UAV Neo
GNU General Public License v3.0

Week 2 · Module 5 — Color Segmentation (Seek a Gate) — SOLUTION orchestrator

Runs every step in sequence against the simulator:
    drone sim module5_color_segmentation/main_solution.py
Run a single step directly instead:
    drone sim solutions/<step_file>.py
"""

import drone_core
from solutions import (
    step1_hsv_mask,
    step2_bounding_box,
    step3_seek_gate,
)

drone = drone_core.create_drone()

_STEPS = [
    ("Step 1: HSV Color Mask", step1_hsv_mask),
    ("Step 2: Bounding Box", step2_bounding_box),
    ("Step 3: Seek the Gate", step3_seek_gate)
]

_launched = False
_index = 0


def start():
    global _launched, _index
    _launched = False
    _index = 0
    print("\n" + "=" * 56)
    print("  Week 2 · Module 5 — Color Segmentation (Seek a Gate)")
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
