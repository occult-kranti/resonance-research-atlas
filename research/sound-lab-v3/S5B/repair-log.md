# Preserved pre-review attempt

Root review found a plan-admission error: an empty plan or a plan with only one condition could receive `complete_primary_set` with no meaningful two-condition contrast. The complete initial S5B file evidence and exact `batch_intake.py` are retained under `pre-review/`.

The repair adds only pre-output plan validation: the plan must be nonempty, use known A/B codes, include both conditions, and declare a primary trial count matching its length. Four bounded controls assert the intended reasons and no output directory creation. The original 16-trial experiment, fit windows, numerical thresholds and all physical interpretations remain unchanged. This is the same S5B loop, not an added research result.
