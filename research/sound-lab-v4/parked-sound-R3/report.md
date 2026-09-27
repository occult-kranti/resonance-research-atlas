# R3 — one-channel, known-frequency extraction

Five generated mono PCM16 files were written then decoded. No physical recording was made. The four design columns are cosine/sine at each declared frequency over 64-sample (8 ms) blocks. Block centers are (start_sample+31.5)/8000 s; each design uses time relative to its center. Least-squares cosine/sine coefficients give amplitudes by their Euclidean norms. OLS log-amplitude rates use centers from .05 to .95 s inclusive. These known frequencies are inputs, not discoveries from arbitrary audio.

The smooth exponential fixture changes amplitude within a block, violating the constant-coefficient extraction model. Its relative envelope error is explicitly reported and plotted. The piecewise-center-amplitude fixture is an exact block model; its remaining amplitude error comes from PCM quantization and numerical error. A separately saved bounded sample-noise draw is added before quantization. Its supplied ±.0001 FS bound does not cover within-block model discrepancy.

Rank four and condition number at most ten are frozen admission requirements. Identical 500 Hz frequencies give rank two in a four-dimensional domain with kernel witness (1,0,−1,0). A 505 Hz reference remains rank four but is badly conditioned and is rejected. Unconstrained diagnostic slopes remain visible; neither rejected case receives a separated correction.

Run: `python research/sound-lab-v4/R3/run.py`. The fixed fixture validates a conditional numerical extraction method. Unmodeled tones, unknown frequencies, temporal variation, acoustic mixing and nonlinear or frequency-dependent recording gain remain unvalidated. A well-conditioned fit does not establish an independently stable physical reference.
