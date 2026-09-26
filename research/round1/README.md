# Passive resonator benchmark — Round 1

Start with [interpretation.md](interpretation.md) for the results and limits.
The [contract](contract.md) froze the model, parameters, controls and acceptance
thresholds before the solver was implemented. All 15 production checks and four
focused tests passed in the recorded run.

From the repository root:

```sh
python -m unittest discover -s research/round1 -p 'test_solver.py' -v
python research/round1/solver.py
```

Requires Python 3.10+, NumPy, and Matplotlib. Produces deterministic CSV/JSON and
SVG/PNG figures in this directory. Files may differ in nonnumeric rendering
metadata across dependency versions; numeric runtime versions and source hashes
are in [results.json](results.json).

The model is a pair of classical masses, springs and dampers in SI units. It does
not describe a human body or establish a clinical or unconventional physical
effect. Further rounds are selected through advisor review of completed evidence.
