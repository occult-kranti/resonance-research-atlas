# Independent advisor evidence and replay

The selection notes and `advisor-N*-precompute.json` files are byte-preserved from the review workspace. Precomputations were written before reading the corresponding producer result files. They are independent calculations, not undisclosed particle measurements. The source, producer and advisor agents share correlated model-family provenance; this is not human peer review.

`original-execution/` preserves the reviewer scripts that were actually run, including their original workspace paths. `preservation-manifest.json` records their original hashes. The scripts use alternate calculations: an exact relaxation transient, thermal matrix exponential, rational transfer identities, exact moments and direct audio projections.

`replay/` contains portable copies with only data/output-path handling changed. They accept raw or gzip-compressed CSV evidence and write `replayed-*` files in this directory. They do not overwrite the frozen round reviews or original precomputations. Replaying a calculation checks reproducibility; it does not recreate the original independence or count as another research round.

From any directory, use Python with NumPy and SciPy installed:

```sh
python /path/to/resonance-research-atlas/research/nanoparticles/reviews/replay/review_n1.py
python /path/to/resonance-research-atlas/research/nanoparticles/reviews/replay/review_n2.py
python /path/to/resonance-research-atlas/research/nanoparticles/reviews/replay/review_n3.py
python /path/to/resonance-research-atlas/research/nanoparticles/reviews/replay/review_n4.py
python /path/to/resonance-research-atlas/research/nanoparticles/reviews/replay/review_n5.py
python /path/to/resonance-research-atlas/research/nanoparticles/reviews/replay/review_n5_final.py
```

The authoritative admission states are in `research/nanoparticle-panel-decisions.json`. Each round's `independent-review.json` binds the source and outputs actually reviewed. Publication and live-site checks are separate release work.

The last command compares every stored N5 spectral row with direct complex projections. Both N5 replay scripts concern the same fifth round. All six replay commands passed on the reviewed artifacts; `replay-verification.json` records that check. Generated `replayed-*` files are optional local outputs, not new admission decisions.
