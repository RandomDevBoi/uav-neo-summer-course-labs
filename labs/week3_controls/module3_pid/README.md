# Week3 Controls — Module3 Pid

Full PID control: altitude hold, fly-a-distance (PID on integrated position), and a vision+PID visual-servo capstone.

## Simulator lab

```bash
drone open_sim                 # launch the Unity sim once
drone sim week3_controls/module3_pid/main.py            # run all steps (student)
drone sim week3_controls/module3_pid/main_solution.py   # reference flight
drone sim week3_controls/module3_pid/tasks/<step>.py    # run a single step
```

Steps:

1. `step1_pid_altitude.py`
2. `step2_position_hold.py`
3. `step3_visual_servo.py`

Student stubs live in `tasks/`; completed references in `solutions/`.
