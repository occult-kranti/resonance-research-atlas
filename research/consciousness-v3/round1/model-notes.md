# B1 IID clarification

The exact binomial audit assumes 80 independent repetitions of each single-trial joint law. In `biased_common_random`, U is shared by reporters A and B within one trial, is independent of that trial's target, and is redrawn independently on each trial. A study-level shared U would induce a different dependent model and is outside the frozen contract's IID assumption.

This note was added during pending independent review, after the first execution. It clarifies the existing IID limit; the frozen contract and results bytes are unchanged. The generated report now states this assumption explicitly. No parameters or numerical conclusions changed.
