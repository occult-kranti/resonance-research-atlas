# S2A — reusable recording intake

The actual files are generated PCM16 WAV bytes, decoded by the same importer available for user recordings. They are not physical tap recordings. Three gain/phase cases recover the prescribed 500 Hz, 4 s^-1 decay within the frozen tolerances, starting away from truth at 499.5 Hz and 2 s^-1. Silence and full-file clipping are rejected before fitting.

The variable-projection estimator solves amplitude, phase and offset linearly for each local frequency/decay candidate. Its nonlinear search is bounded and local. Supplying a nominal frequency is an explicit model choice, not evidence that the file contains one mode. A low residual does not make the decay intrinsic to a material.

Example: `python research/sound-lab-v3/fit_recording.py research/sound-lab-v3/S2A/case0.wav --frequency 500 --start .05 --stop .8 --output /tmp/example-fit`. For a real recording choose and prerecord its fit window, retain the raw file, and document provenance and microphone processing. CSV intake requires exactly `time_s,amplitude_FS`.

Next failure tests: nearby modes and time-varying gain. These can make a single-mode fit biased or observationally indistinguishable from a different true decay.

