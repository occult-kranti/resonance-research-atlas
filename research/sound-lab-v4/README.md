# Five-round field laboratory v4

Five adaptive rounds with two substantive loops each are complete. R1–R2 retain the sound-measurement checkpoint. The user then redirected the active work to electricity, magnetism and antigravity, so R3–R5 cover electrical energy, magnetic force and a gravity-claim identification design. The historical directory name is preserved for reproducibility. No sixth research round is selected.

All accepted observations here are generated data or model trajectories. No circuit, magnetic bench or gravity experiment was physically run. The deliberately injected R5 acceleration is a synthetic estimator positive control; an ordinary mass-proportional bias reproduces its individual force records. No antigravity, source-free energy or calibrated detector sensitivity is established.

| Round | Executed model | Independent admission |
|---|---|---|
| R1 | Shared-gain target/reference slopes and generated stereo PCM, with exact ambiguous rivals | Conditional recovery only under known stable-reference and shared-gain premises |
| R2 | Exact positive-envelope log-box propagation and explicit nuisance bounds | Conditional set bounds; missing nuisance bounds withhold physical intervals |
| R3 | Series RLC source/storage/load budget, voltage gain, reactive VA and source-off storage release | Passive electrical readout and energy-boundary examples |
| R4 | Maintained-current moving inductance, motional voltage, field/mechanical work and support reactions | Conditional electromechanical model; smaller one-pan reading with unchanged g |
| R5 | Paired supports, current polarity and four masses; null/injected models, error bounds and exact bias rival | Conditional identifying design and retained nonidentifiability |

The authoritative [decision ledger](../panel-v4-decisions.json) contains ten loop entries, ordered contract/review times and exact hashes. The [advisor report](../../docs/panel-v4/advisor-review.md), [panel log](../../docs/panel-v4/panel-log.md) and [future roadmap](../../docs/panel-v4/roadmap-v4.md) distinguish accepted results from proposed physical work. Independent reviewer code and outputs are in `reviews/`. The producer's frozen `executed_pending_review` status is historical; the separate ledger and `summaries.json` carry its admission overlay.

## Reproduce and inspect

Run commands from the repository root. The execution record used Python 3.12.14 with the exact NumPy/SciPy/Matplotlib versions in `requirements.txt`. Install these in an isolated environment if needed:

```sh
python -m pip install -r research/sound-lab-v4/requirements.txt
python research/sound-lab-v4/verify.py
python research/sound-lab-v4/verify.py --regenerate
python scripts/verify_field_notes.py
```

`verify.py` checks the exact producer artifacts and shared-helper binding. `--regenerate` copies the laboratory into a temporary directory, executes R1–R5 there and compares the declared artifact bytes; it does not overwrite accepted outputs. Exact figure bytes are environment dependent, so a mismatch in another environment must be investigated rather than silently replacing hashes. `verify_field_notes.py` checks the five-round/ten-loop admission sequence, independent review bindings, source IDs and release artifacts. Neither command proves an empirical claim.

Each admitted round has a frozen `contract.json`, `run.py`, `results.json`, `report.md`, scientific `figure.svg`, raw CSV/WAV or compressed trajectories, and `manifest.json`. The same contracts are preserved under `docs/panel-v4/contracts/`. Numerical runners can also execute individually in a **separate working copy**, for example:

```sh
python research/sound-lab-v4/R3/run.py
```

An individual runner rewrites its local outputs. Use the temporary-copy verifier for routine reproduction of the accepted tree. `R5/run.py` exposes `fit_paired` for the specified force model, but it is not a physical-recording acquisition system or authentication service. New observations need a separately locked plan and calibration record; do not relabel the generated CSVs.

The field-notes interface is `sound-lab/field-notes.html`. Its electrical calculator is sinusoidal steady state, separately labeled from R3's finite transient. Proposed measurement steps and the distinction between model values and measured parameters are in [protocol.md](protocol.md).

## Preserved failures and scope changes

- `parked-sound-R3/` contains acoustic producer artifacts executed before the user's focus change. Related exploratory reviewer files begin `parked-sound-R3` in `reviews/`. There was no admission verdict; these are excluded from the five completed rounds.
- `R5/pre-review/` preserves the pre-repair code, contract, result, raw files, report and manifest. The reviewer found inward rounding that excluded the true value at an extreme interval endpoint by approximately 3.12e-17 m/s².
- The R5 repair retains the theoretical ±0.00032 m/s² error bound and adds a separately reported 1e-12 m/s² outward arithmetic guard. Independent checks enumerate all 65,536 corners and require strict inclusion at both saturating endpoints. This finite-fixture guard is not a universal floating-point interval certificate.
- The attempted external UPV acoustic import obtained metadata and licensing information only. No measured acoustic payload was acquired or analyzed.

Generated WAVs are analysis fixtures, not listening presets. R3's source-off control sets the ideal source voltage to zero while the series circuit remains **closed**. R4 prescribes motion rather than predicting free levitation. R5 assumes static, contemporaneous supports and known force-error bounds; its supplied 2 µN bound is not measured instrument performance.

Implementation and scientific diagrams are project code. Dependency licenses and source reading records remain distinct from scientific admission. No ngspice or Magpylib execution is claimed in this release.
