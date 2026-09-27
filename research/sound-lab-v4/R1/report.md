# R1 — shared-gain witness

Executed synthetic analytic envelopes and generated stereo PCM16, not physical recordings. The independently stable reference is assumed; it is not inferred from the corrected fit. The two stereo channels already separate target and reference. This runner performs no mono frequency separation.

For target log-slope l_s=−alpha+beta_s and reference log-slope l_r=−alpha_r+beta_r, the estimator is alpha_hat=l_r−l_s=alpha−alpha_r+beta_r−beta_s. Shared gain and alpha_r=0 identify alpha. Target-only data have a one-dimensional kernel. Adding the stated reference makes the two-parameter map full rank, but allowing differential gain or reference decay restores a kernel, explicitly recorded in identifiability.json.

The full signed carrier samples are fitted by variable projection over sin/cos amplitudes at the declared frequencies. A bounded scalar optimizer estimates each log slope. This gives a method independent of the skeptic's carrier-maxima fit. Raw WAVs are written then decoded; all hashes are recorded. Zero reference withholds correction. Differential gain and a decaying reference produce exactly identical PCM files here and both retain the expected −1 s⁻¹ bias. A low residual does not validate the shared-gain premise.

Run: `python research/sound-lab-v4/R1/run.py`. Fixture WAVs are analysis artifacts, not playback presets. The result is conditional parameter recovery; intrinsic material damping remains unmeasured.
