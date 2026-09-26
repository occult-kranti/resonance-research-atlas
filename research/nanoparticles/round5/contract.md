# Nanoparticles N5 FINAL frozen contract — the physical drive must be specified

Frozen before analysis/execution after N4 admission. Project hypothesis NP-H5:
an audible envelope rate, a linear drive component and a nonlinear detector's
difference-frequency signal are distinguishable measurements. A phase reversal
can test the proposed quadratic mixing route while preserving digital RMS.
This is a project discrimination test of established signal arithmetic, not
a particle manipulation, human effect or new acoustic force law.

## Actual production inputs

Use the four copied OpenSync NanoLab WAVs and JSON manifests in assets/, generated
by the actual src/nanolab/model.ts adapter and existing synth.ts/wav.ts engine.
Source snapshots and a self-contained executable bundle are in production/.
The complete pre-analysis input hashes and byte counts are frozen in inputs.json.
Never substitute regenerated independent sine formulas for the decoded evidence.

Each file: PCM16 stereo,48000Hz,96000frames (2s), identical left/right channels,
50ms endpoint fades, carrier375Hz, rate r=23.4375Hz, gain−24dBFS,
g=10^(−24/20). Analyze4096 interior frames starting at32768; this contains integer
cycles of every declared line and avoids endpoint fades. Digital samples have
full-scale(FS) amplitude units; no pressure, displacement, magnetic-field or force
calibration exists. Analyze one identical channel.

Two-tone: g/2[sin(2pi(fc−r/2)t)+sin(2pi(fc+r/2)t)] → DFT bins31,33.
AM: g[.5+.5sin(2pi r t)]sin(2pi fc t) → bins30,32,34.
Baseband: g sin(2pi r t) → bin2. Carrier: g sin(2pi fc t) → bin32.
Predicted positive-frequency peak-amplitude magnitudes are respectively
(g/2,g/2), (g/4,g/2,g/4), g, and g.

## Explicit observation operators and rivals

Linear periodic steady-state filter H(f)=1/(1+i f/200Hz), dimensionless.
It changes existing line amplitudes/phases; it does not create a rate line.
Separate nonlinear detector q=u² has FS² units. At rate bin2, ideal pair andAM
have amplitude g²/4 after squaring, despite no raw rate component. AM additionally
has2r amplitude g²/16; baseband has2r amplitude g²/2 and no r; carrier has
neither low line. These are detector-output facts, not particle forces.

Normalize decoded signals to equal interior RMS=.02FS for an analysis-only
positive control. Equal peak gains do not imply equal mean-square values. Compare
the resulting q rate coefficients and report normalization factors. This does
not equalize physical energy without actuator calibration.

Phase witness: flip the upper pair-tone DFT coefficient atbin33(andits conjugate,
implicitly via real inverseFFT). This preserves digital RMS; the quadratic
rate-bin complex coefficient must reverse sign within the quantization bound.

## Frozen gates and uncertainty

1. Verify WAV/manifest/source hashes, encoding, frame count, rate, stereo identity,
   and predicted decoded complex line coefficients. Maximum discrepancy<=2^-14FS.
   All inspected absent low components use that floor, not an exact-zero claim.
2. LTI-transformed line coefficients match predicted original coefficients times
   H(f) within2^-14FS; pair/AM rate bins remain below that floor.
3. Quadratic r and2r coefficients match the signed complex algebra within
   1e-5FS². With sample error bounded conservatively by epsilon=2^-15FS,
   Fourier line error<=2epsilon; squared line error<=2(2g epsilon+epsilon²)
   <1e-5FS². Float32 synthesis errors are smaller than this conservative budget.
4. Equal-RMS outputs have RMS.02 within1e-12FS; squared rate coefficient obeys
   gain-factor² scaling to1e-12FS². A zero digital blank yields zero output.
5. Upper-tone phase reversal preserves RMS to1e-12FS and reverses the quadratic
   rate complex coefficient with |q_flipped(r)+q_original(r)|<1e-5FS².

Save source/input/contract/solver bindings, decoded spectra/summary CSV, JSON,
preciseSVG/PNG and detailed interpretation. Conceptual future chain is line voltage
→characterized transducer→measured pressure/acceleration witness→sealed inert
phantom. Particle material contrast, spatial gradients, hydrodynamics, acoustic
streaming and detector nonlinearity remain unmeasured rivals. No actuator build,
human listening experiment or particle exposure is executed. Stop after N5 review.
