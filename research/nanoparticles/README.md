# Five adaptive nanoparticle and frequency research rounds

This branch contains exactly five newly selected project hypotheses and executed
benchmarks. Each question was frozen after independent review of the preceding
round. They apply established physics and signal processing to produce falsifiable
measurement designs; they do not claim new physical laws, measured therapeutic
effects, particle manipulation or an experimentally demonstrated material mechanism.
The earlier six research rounds are separate and unchanged.

| Round | Project hypothesis and tested distinction | Executed result |
|---|---|---|
|[N1](round1/interpretation.md)|Loss per cycle versus absorbed power|Debye cycle loss peaks at omega*tau=1; frequency-scan power at that point is half its fixed-parameter limit. Dynamic/passive-energy and quadrature controls pass.|
|[N2](round2/interpretation.md)|Absorption versus thermometer transfer|Constant0.2W looks like0.0723–0.1469W under three naive windows; calibrated estimates recover0.2W. Absolute-power scale ambiguity remains without external calibration.|
|[N3](round3/interpretation.md)|One fitted relaxation time versus distinct populations|A one-frequency fit matches a mixture but has43.0% maximum held-out discrepancy in the baseline example; viscosity and phase predictions distinguish declared models.|
|[N4](round4/interpretation.md)|Particle number, mass and susceptibility weights|The mean-diameter approximation overcounts by12%; conditional count-weighted and susceptibility-weighted spectra differ even with identical DC normalization.|
|[N5](round5/interpretation.md)|Actual audio spectrum versus nonlinear rate detection|Actual OpenSync WAVs, LTI and quadratic-detector outputs differ; phase reversal preserves digital RMS and reverses the predicted mixing component.|

There are **30 parameterized production checks**, across a small set of substantive
model tests and controls, with five separate accepted independent reviews.
Check count is not a discovery count. Every interpretation describes mathematical
derivation, units, rivals, empirical-design improvements, validity limits and the
boundary between computation and unperformed hardware work.

## Verify and reproduce

Verify the packaged source, numeric evidence, review bindings, WAVs and figures
without rerunning a research calculation:

```sh
python3 research/nanoparticles/verify.py
```

Rerun all five existing benchmarks in a temporary copy and compare the saved
numeric evidence, including exact audio regeneration, without modifying originals:

```sh
python3 research/nanoparticles/verify.py --recompute
```

Each `roundN/solver.py` can also run individually. Default verification uses only
the Python standard library. Numeric reproduction uses NumPy and Matplotlib;
actual WAV regeneration additionally uses Node. Exact recorded versions are in
[environment.json](environment.json) and Python pins in [requirements.txt](requirements.txt).
Different environments may change floating-point output or rendering; an exact
binding mismatch requires examination and must not be silently accepted by
refreshing hashes. Recomputed SVG metadata can vary, so isolated recomputation
compares numeric evidence while the original rendered figures remain hash-bound.

The N5 `regenerate_assets.mjs` invokes the actual snapshotted production bundle,
not a substitute sine generator. It verifies the same four WAVs and manifests
byte-for-byte. The research analyzes their decoded PCM samples independently.
The production inputs and renderer source snapshots are bound by N5/inputs.json.

Verify just the four actual production WAVs and JSON manifests:

```sh
node research/nanoparticles/round5/regenerate_assets.mjs
```

This checks byte-for-byte agreement with the frozen input hashes. Add `--write`
only to restore the same bound assets; it does not generate a new condition.

## Inspectable record

Every round contains `contract.md`, `sources.md`, `solver.py`, `results.json`,
`independent-review.json`, `interpretation.md`, compact raw CSVs, and SVG/PNG figures.
The release artifact manifest binds those exact bytes, including CSV and figures.
CSV sizes are modest, so they remain directly inspectable. Advisor selections,
precomputations and portable independent-review replays are preserved under
[reviews/](reviews/). Those reviews used separate formulas/representations; merely
hashing output is not independent scientific validation.

N1 retains an explicit bibliographic erratum, its original contract and the
pre-erratum result metadata. The correction changed a page range and source
bindings, not the model or thresholds. No other round has a hidden contract change.

No nanoparticle synthesis, injection, human exposure, clinical outcome, acoustic
force measurement or magnetic apparatus was performed. New research stops at N5.
