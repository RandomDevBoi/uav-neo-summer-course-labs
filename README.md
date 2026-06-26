# UAV Neo Course Labs — Week 2 (Vision) & Week 3 (Controls)

MIT BWSI Autonomous Drone Racing Course — UAV Neo

These labs re-cast the **Week 2 Vision** and **Week 3 Controls** Jupyter notebooks as
hands-on labs that run against the **UAV Neo simulator**, using the same `labs/module/tasks`
structure as [`uav-neo-prereq-labs`](../uav-neo-prereq-labs).

Each lab is split into small **steps**. Every step has a clearly marked student section:

```python
##################################
#### START PUT CODE HERE #########

# YOUR CODE HERE  (hints in the comments)

###### END PUT CODE HERE #########
##################################
```

A completed reference implementation lives next to every student file under `solutions/`.

## Two kinds of labs

Following a **hybrid** design:

- **Concept labs** (pure Python, no drone) teach the underlying math. Run them directly:
  ```bash
  python3 labs/week2_vision/module1_image_formation/tasks/image_formation.py
  ```
  They print `PASS`/`FAIL` for a set of built-in self-checks.

- **Simulator labs** fly the drone and use the live camera / flight / physics APIs. Run them
  through the course tool, exactly like the prereq labs:
  ```bash
  drone open_sim                                   # launch the Unity sim once
  drone sim week2_vision/module5_color_segmentation/main.py
  ```

## Instructor answer keys

Every simulator module ships two orchestrators:

- `main.py`         — imports the student `tasks/` package (blanks)
- `main_solution.py` — imports the completed `solutions/` package

```bash
drone sim week3_controls/module3_pid/main.py            # student version
drone sim week3_controls/module3_pid/main_solution.py   # reference flight
```

Concept labs keep `tasks/<name>.py` (blanks) and `solutions/<name>.py` (completed).

## Contents

### Week 2 — Vision (`labs/week2_vision/`)

| Module | Source notebook | Type | Topic |
|--------|-----------------|------|-------|
| `module1_image_formation`   | `01_Image_Formation.ipynb`   | concept   | Pinhole camera model, projection, intrinsics, distortion |
| `module2_opencv`            | `02_OpenCV.ipynb`            | simulator | Thresholding & morphology on the live camera feed |
| `module3_linear_regression` | `03_LinearRegression.ipynb`  | concept + sim | Fit a line to pixels → follow a ground line |
| `module4_downward`          | `04_Downward.ipynb`         | simulator | Contour analysis with the downward camera |
| `module5_color_segmentation`| `05_ColorSegmentation.ipynb` | simulator | HSV color segmentation → seek a colored gate |

### Week 3 — Controls (`labs/week3_controls/`)

| Module | Source notebook | Type | Topic |
|--------|-----------------|------|-------|
| `module1_coordinate_frames` | `CoordinateFrames_and_Dynamics.ipynb` | concept   | Euler↔rotation, frame transforms, thrust sizing |
| `module2_feedback_control`  | `simple_feedback_control.ipynb`       | concept + sim | Proportional control → altitude hold |
| `module3_pid`               | `simple_feedback_control.ipynb`       | simulator | PID altitude hold, position hold, visual servoing |

## The drone API (quick reference)

```python
import drone_core
import drone_utils as uav_utils
drone = drone_core.create_drone()

# Flight (all pcmd args in [-1, 1])
drone.flight.takeoff()
drone.flight.send_pcmd(pitch, roll, yaw, throttle)   # +pitch=fwd +roll=right +yaw=CW +throttle=up
drone.flight.stop()                                  # hover
drone.flight.land()

# Physics / sensors
drone.physics.get_altitude()           # meters
drone.physics.get_linear_velocity()    # (x=right, y=up, z=forward) m/s
drone.physics.get_attitude()           # (pitch, roll, yaw) degrees; yaw in [0,360)

# Cameras (numpy BGR / depth arrays)
drone.camera.get_color_image()         # 480x640x3 forward camera
drone.camera.get_downward_image()      # 480x640x3 downward camera

# Vision helpers
uav_utils.find_contours(img, hsv_lower, hsv_upper)
uav_utils.get_largest_contour(contours, min_area)
uav_utils.get_contour_center(contour)  # (row, col) or None
uav_utils.get_contour_area(contour)
uav_utils.clamp(v, lo, hi)
uav_utils.remap_range(v, a, b, c, d)

# Frame loop
drone.set_start_update(start, update, update_slow)
drone.get_delta_time()                 # seconds since last frame
drone.go()
```

GNU General Public License v3.0
