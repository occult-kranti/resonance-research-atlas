# N5 executable source provenance and mathematical boundary

Primary executable source is the project's actual OpenSync production renderer:
https://github.com/occult-kranti/brainwave_opensync . NanoLab composes the existing
src/engine/synth.ts functions through src/nanolab/model.ts and exports PCM16 using
src/engine/wav.ts. Its spectral preview uses src/dsp/fft.ts. Exact snapshots and
the actual four exported WAVs/manifests are preserved here and hash-bound in
inputs.json; no remote commit identity is substituted for those exact source bytes.

The standalone production/nanolab-model.mjs bundle was created by the repository
implementation agent from the actual adapter with esbuild forNodeESM. The
regenerate_assets.mjs script invokes that same bundle and verifies its output
bytes. Python analysis decodes the saved WAVs independently; it does not regenerate
sine waves as replacement observations. Closed-form sine products predict the
expected spectra and give independent tests of the decoded output.

The LTI operator and quadratic detector are explicitly chosen mathematical
observation models. Neither is a measured transducer, acoustic pressure field,
magnetic field, nanoparticle force or physiological response. Prior N1–N4 models
cannot be driven by a sound-file label without a calibrated physical conversion.
No external paper is claimed to validate a particle effect from this audio.
