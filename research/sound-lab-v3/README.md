# Low-material sound measurement program

Ten bounded loops were completed sequentially in five rounds and independently accepted within their stated limits. The advisor selected each next loop after inspecting the preceding outputs; each contract froze before its runner was written and executed. Existing original and nanoparticle results remain unchanged. The sound program stops at S5B.

All present measurements are synthetic digital fixtures unless explicitly labeled `actualbytes` (a generated-and-decoded WAV file, still not a physical microphone measurement). No physical bench has been run. A phone microphone records a whole source/room/receiver chain. Its digital full scale is not pressure in pascals, displacement, material energy, or a biological quantity.

The validation WAVs are for file analysis, not listening presets. They include intentional silence, full-scale clipping and other negative controls. In particular S2A/case4.wav is deliberately clipped. Do not present these fixtures as quiet playback probes. No runner plays audio; the household protocol uses manually controlled, comfortable ordinary sound and declared recording/playback settings.

Run from this directory with the repository's pinned NumPy/SciPy/Matplotlib dependencies:

```sh
python verify.py
python verify.py --regenerate
```

Each loop preserves `contract.json`, `run.py`, `results.json`, raw CSV, exact scientific SVG, `report.md`, and SHA-256 `manifest.json`. The verifier checks exact bytes and contract bindings; it does not replace the separate advisor's independently derived review in `docs/panel-v3/reviews`. The UI index is `summaries.json`. Source passages and limits are in `sources.json`. Implementation and scientific plots are original MIT-licensed project contributions. No third-party image assets are copied.

For user file analysis, use the protected, versioned intake. Output files must not exist; choose a new prefix. Inputs are never overwritten. Window times are seconds from file start; nominal frequency defines a local ±50 Hz fit search.

```sh
python research/sound-lab-v3/intake_v2.py path/to/recording.wav --frequency 500 --start 1.05 --stop 1.8 --output path/to/new-fit
```

`fit_recording.py` is retained solely as the frozen historical fitter used by old reproduction scripts; its direct CLI lacks the new file-protection guards. `intake_v2.py` imports that fitter and adds evidence-preserving admission. The fit is a recorded-channel model, not a material identity. See `protocol.md` for household setup, metadata, controls and the event-time window convention. Runtime dependencies are pinned in `requirements.txt` and recorded in `environment.json`.

For a complete comparison, use `batch_intake.py`. It reads the frozen trial plan and a separate acquisition manifest, keeps all exclusions, and reports a primary contrast only when every planned trial is eligible. This runnable example is synthetic:

```sh
python research/sound-lab-v3/batch_intake.py --plan research/sound-lab-v3/S5A/preregistration.json --manifest research/sound-lab-v3/S5B/complete-manifest.json --output /tmp/sound-bench-new-run
```

The output directory must not already exist. It receives a JSON/CSV report and per-trial fit traces. For actual recordings, make a separate pilot-informed plan and acquisition manifest; do not overwrite the synthetic plan. Each acquisition entry needs `trial_id`, `order`, `condition_code`, `path`, `source_sha256` and `impact_time_s`. Manifest metadata must state the device, gain processing, geometry, clock reference and predeclared impact-alignment rule. Hashes preserve identity; they do not authenticate a physical measurement.

| Round | First loop | Second loop |
|---|---|---|
| 1 | Recover total recording-chain transfer; retain factorization ambiguity | Quantify reference drift, notch noise and regularization bias |
| 2 | Fit generated PCM decay through a reusable file importer | Expose multiple-mode and recording-gain alternatives |
| 3 | Protect source files and reject invalid channel/output paths | Test timing metadata, clock scaling and malformed acquisition inputs |
| 4 | Compare magnitude maps with independent complex observations | Test spatial conditioning and a withheld phase observation |
| 5 | Counterbalance a proposed household comparison with null controls | Run strict batch admission and withhold incomplete primary results |

The adaptive record includes an actual intake defect repair and a reviewer-detected timestamp-test error. Original failed attempts and corrected evidence are retained; neither repair is counted as an additional research loop. The producer artifacts stay frozen with `executed_pending_review`; `summaries.json` overlays the separately bound `accepted_narrow` review status. `verify.py` refreshes that index after reproduction without rewriting the historical results.

Source baseline: atlas `e6baa620f2f8666957741cf12f40b769a6a808a0`; OpenSync `1c7dcf26260f621557bc51dd3197d930e8c5044e`. Historical Newton and Tesla methods are modern research lenses: explicit mechanism, phase, loss, inverse ambiguity, falsifier and revision. Neither historical person participated in this model-agent panel.
