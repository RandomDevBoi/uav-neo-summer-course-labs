# Week2 Vision — Module5 Color Segmentation

HSV color segmentation of a red gate: mask, bounding box, then yaw-and-approach to seek it.

## Simulator lab

```bash
drone open_sim                 # launch the Unity sim once
drone sim week2_vision/module5_color_segmentation/main.py            # run all steps (student)
drone sim week2_vision/module5_color_segmentation/main_solution.py   # reference flight
drone sim week2_vision/module5_color_segmentation/tasks/<step>.py    # run a single step
```

Steps:

1. `step1_hsv_mask.py`
2. `step2_bounding_box.py`
3. `step3_seek_gate.py`

Student stubs live in `tasks/`; completed references in `solutions/`.
