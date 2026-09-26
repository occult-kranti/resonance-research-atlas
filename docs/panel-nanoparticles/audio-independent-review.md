# Independent audio and model review

Reviewer: Tesla/modern measurement model agent. Date:2026-09-26. This is code/scientific review, not a new research round or human peer review.

Read OpenSync `src/nanolab/model.ts`, `src/pages/NanoLab.tsx`, NanoLab model/page tests, the relevant synthesis and FFT implementations, WAV encoder, shared preview ownership and `LiveEngine.playBuffer/stopPreviews`. Skimmed atlas `models.js` N1/N2 and their UI unit conversions and existing numerical checks. No production files were edited by this reviewer and the coder's full check was not repeated.

## Finding sent to the coder

The original unconditional sentence that a two-tone signal has no Fourier line at its spacing was false for an allowed coincidence. At fc=90Hz,r=60Hz the lower source tone is60Hz; at AMfc=80Hz,r=40Hz the lower sideband is40Hz. These are existing components, not new difference-frequency generation. Recommended correction: superposition creates no **additional** difference-frequency line, while a source component may already equal the numerical rate. Qualify stationary components separately from finite fades and window leakage. The coder implemented this correction and added targeted regressions; I reread the corrected page and tests. This finding is resolved.

One independent targeted check bundled the actual production renderer into a temporary review module, then used a separate float64 Fourier projection over48,000 samples after the fade. At−24dBFS, the two-tone coincidence measured0.03154786717197FS at60Hz (g/2); AM measured0.0157739335630FS at40Hz (g/4). The default400/16Hz two-tone signal measured3.49e−18FS at16Hz in this coherent window. This resolves the concrete prose risk; it is not a broad empirical claim that finite recordings have exactly zero low-frequency leakage.

A nonblocking validation precision was also reported: the original common `fc−r>0` condition rejected fc80/r80 for all modes, even baseband/carrier where that unused field should not matter and two-tone whose actual components40/120Hz remain positive. The coder changed validation to inspect actual active components by mode and added endpoint regressions. I inspected that fix. No outstanding blocking issue remains in this review; the coder reported11 focused tests passing after both corrections.

## Checks that passed by code and algebra inspection

- Two-tone, AM, baseband and carrier synthesis matches the displayed equations. Stationary component amplitudes are g/2 per two-tone component, g/2 AM carrier and g/4 per AM sideband, and g for baseband/carrier. Two-tone envelope magnitude repeats at r; that does not assert a newly generated linear spectral component.
- FFT data is computed from the rendered samples, not the predicted-component table. The centered unfaded segment, periodic Hann coherent-gain correction and Hz-per-bin calculation are consistent with the one-sided FFT normalization. Off-bin peak readings can differ from analytic amplitudes; the UI explicitly describes leakage. Local FFT peaks are not claimed to be exact component frequencies.
- Playback receives the same floating-point arrays that the model measures, with0dB additional preview gain. WAV export encodes those arrays as PCM16; it does not falsely claim byte identity with floating-point data. Manifest includes actual frame duration, effective gain, normalization, analysis window and SHA-256 of the exact WAV bytes. The coder's existing decode/checksum test independently reads PCM and verifies hash; I inspected this test rather than rerunning a duplicate check.
- Allocation/gain/frequency bounds are checked before synthesis; two channels are identical, endpoints fade to zero and output has a stated sample-peak ceiling. RMS is measured rather than asserted equal across signal types. Digital dBFS is not labeled calibrated sound-pressure level.
- Shared preview ownership is used. Editing, stop, replacement, unmount, panic, mute, session start and governor changes revoke the owned preview. Stale natural-end callbacks cannot stop a replacement preview. Export tokens discard asynchronous results after settings/governor/navigation changes. Listening restrictions and failure cleanup are present.

## Atlas N1/N2 review

No scientific-unit error found in the reviewed N1/N2 implementation. N1 uses dimensionless susceptibility per suspension volume, peak H in A/m, cycle energy J/m³ and power W/m³. UI conversions to nJ/m³ and mW/m³ are correct. Separate normalized curves do not falsely share physical units; fixedτ versus fixedf sweeps are distinguished. μ0 is identified as a reference approximation rather than an exact post2019SI constant.

N2 implements Cθdot=P−Gθ and τs ydot+y=θ for constant input and zero initial rises. C:J/K, G:W/K, P:W and temperatures:K are consistent. The no-loss, instantaneous-sensor and repeated-pole limits are handled. The simultaneous P,C,G scale control preserves the temperature trace; its finite-window inferred-power expression correctly retains the independent assumed C. UI identifies the model as lumped and synthetic. A source-off thermometer can briefly keep rising due to lag; this would not be evidence of continued heat generation, and no cooling protocol is claimed by this explorer.

The review does not authenticate sound-pressure calibration, physical transducer behavior, hearing perception, material response or biological effects. A quadratic detector can create difference terms, but its squared signal is not a particle force without a spatial coupling model, material coefficients and an independently calibrated field.
