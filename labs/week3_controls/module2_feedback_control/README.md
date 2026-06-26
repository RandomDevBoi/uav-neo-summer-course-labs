# Week3 Controls — Module2 Feedback Control

Proportional control: a pure-Python warm-up (p_control.py) then proportional altitude hold on the drone.

## Concept lab (no simulator)

```bash
python3 tasks/p_control.py        # your work (prints PASS/FAIL self-checks)
python3 solutions/p_control.py    # reference
```

## Simulator lab

```bash
drone open_sim                 # launch the Unity sim once
drone sim week3_controls/module2_feedback_control/main.py            # run all steps (student)
drone sim week3_controls/module2_feedback_control/main_solution.py   # reference flight
drone sim week3_controls/module2_feedback_control/tasks/<step>.py    # run a single step
```

Steps:

1. `step1_altitude_hold.py`
2. `step2_altitude_steps.py`

Student stubs live in `tasks/`; completed references in `solutions/`.
