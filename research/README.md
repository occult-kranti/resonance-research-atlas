# Six reviewed research-method benchmarks

These six adaptive rounds investigate what specified models and observations can
establish. They are reproducible classical mechanics, inverse-problem and
statistical examples, not demonstrations of healing, free energy, antigravity,
material transmutation or external dream perception.

| Round | Question | Narrow result |
|---|---|---|
| [1](round1/interpretation.md) | Can resonance increase amplitude without creating energy? | Input work accounts for storage and dissipation in the passive model. |
| [2](round2/interpretation.md) | Does a spectral peak identify an intrinsic frequency? | Observable and source changes can shift peaks or reproduce another model's spectrum. |
| [3](round3/interpretation.md) | Do two assay signals determine three component amounts? | An exact nonnegative family remains; an independent assay resolves noiseless ambiguity. |
| [4](round4/interpretation.md) | Is a unique inverse robust to measurement errors? | Near-duplicate assays amplify bounded noise by a precisely derived factor. |
| [5](round5/interpretation.md) | Does selecting the best test preserve its nominal error rate? | Exact familywise errors depend on multiplicity and dependence; calibration is necessary. |
| [6](round6/interpretation.md) | How should a concealed-target claim be calibrated? | Fixed-count, leaked-information and optional-stopping controls have distinct exact rates. |

Each round was selected after the advisor reviewed the preceding completed result.
Every folder contains its frozen contract, solver, observed results, interpretation,
scientific SVG/PNG plots and a separately produced independent review. Round 2
preserves an explicit post-first-execution domain clarification. Review revisions
preserve earlier hashes when plotting-only changes were admitted.

Verify the packaged evidence without rerunning it:

```sh
python research/verify_rounds.py
```

Regenerate and verify all six existing benchmarks with one command:

```sh
python research/verify_rounds.py --regenerate
```

Requires Python 3.10+, NumPy and Matplotlib. Recorded producer runtime: Python
3.12.14, NumPy 2.3.5, Matplotlib 3.10.8. Independent reviews additionally used
separate formulas and, in Round 1, SciPy matrix exponentiation. The verification
command checks source, result and review bindings; archive hashing alone is not
scientific validation. Exact-byte review bindings intentionally detect changed
outputs or dependency-sensitive regeneration and should not be silently refreshed.

CSV evidence is losslessly stored as `.csv.gz`; per-round `csv-manifest.json`
records both the original and compressed SHA-256 hashes and sizes. Solvers
regenerate raw CSVs. `python research/compress_evidence.py` restores deterministic
gzip packaging and verifies byte-for-byte decompression. The four focused Round 1
tests supplement 72 parameterized production checks across the six rounds. Check
counts describe acceptance checks, not distinct scientific discoveries.

The sixth round is the final executed research loop. No participant study or
additional round has been run.
