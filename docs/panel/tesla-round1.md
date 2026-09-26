# Tesla and modern measurement panel — round 1

Date: 2026-09-26. Scope: selected historical passages, modern primary records, source triage and executable simulation contracts. This is a contemporary Tesla-inspired engineering lens, not Tesla's participation or a reconstruction of his private reasoning. These model agents share training and are not independent human peer review.

## What the source review changes

1. **Tesla's electrotherapy idea is historically real; a universal healing frequency is not established.** The 1898 article contains engineering observations, personal anecdotes, uncertainty about specific applications, and descriptions of adverse effects. Its useful research lead is *coupling and loading*: attaching a load changes an oscillator. Its assertions do not validate clinical efficacy. [TES-1898]
2. **Tesla's terrestrial model and Schumann modes must remain separate.** US787412A proposes a conducting-Earth/quarter-wave condition. The Earth–ionosphere shell equation is a different boundary-value model. A numerical proximity between one of their rates does not equate the mechanisms. [TES-1905, SR-2011]
3. **An observed spectral maximum is not automatically a natural mode.** Source spectrum, damping, propagation, measurement transfer function and interference matter. The 18 September 2026 Annales Geophysicae paper explicitly makes this distinction. [SR-2026]
4. **“Entire frequency of a human/object” is underdefined.** A reproducible result needs an observable, units, time window, sensor position, bandwidth, excitation and state. Distinct physiological channels in public PSG resources illustrate what is actually recorded. Chemical purity does not remove an object's multiple mechanical, electrical and molecular degrees of freedom. [BIO-PSG2026, BIO-SLP1999; final sentence is a general model deduction]
5. **Energy and momentum bookkeeping are productive targets.** Tesla's radiant-energy patent names an external source. The Navy-assigned Pais patent is a proposal, while NASA's tested asymmetric capacitors were explained by ion/gas momentum exchange within the tested conditions. These records support falsification work, not a verified free-energy or antigravity result. [TES-1901, NASA-ACT2004, PAT-PAIS2018]

No all-corpus, all-patent or latest-across-all-fields claim is made. The source ledger records exactly what was read, including unread government files and abstract-only leads. The 2026 motor/load patent is an **individual** patent, not a government experiment.

## Measurement dictionary

| Quantity | Operational meaning | Units / missing condition |
|---|---|---|
| Oscillation frequency | Cycles per unit physical time of a chosen signal | Hz; needs clock and observable |
| Eigenfrequency | Mode of a specified linearized operator and boundary conditions | rad/s or Hz, explicitly converted |
| Driven spectral maximum | Peak of measured power after source and instrument response | Hz; differs from an eigenvalue in general |
| Harmonic | Integer multiple of a defined fundamental in a specific signal/model | Dimensionless index times Hz |
| EEG / ECG / EMG | Different measured electrical potential differences | Voltage versus time, montage and filters |
| Respiration channel | Sensor-specific pressure, flow or movement proxy | Physical/calibration units differ by sensor |
| Audio beat | Envelope/difference feature of specified acoustic signals | Does not define a brain state or field dose |
| Biological intervention | A defined stimulus with waveform, spatial targeting, intensity and endpoint | Frequency alone is insufficient |
| “Metaphysical frequency” | Cultural/interpretive phrase until mapped to an observable | No numerical physical value assigned |

The FDA device framework provides a concrete contrast: waveform, geometry, amplitude and exposure structure all matter. This is a measurement lesson, not a recommendation to construct or use a stimulation device. [BIO-FDA]

## Target T1 — passive resonator energy and loading audit

**Historical inspiration:** synchronism, retuning under load, and stored energy. **Modern interpretation:** a passive source–resonator–load system can amplify an amplitude while obeying an energy budget. The following is a new project reconstruction using standard dynamics, not a new physical law or a Tesla quotation.

Use generalized coordinates q and a common physical clock:
```
M q'' + (R_internal + R_load) q' + K q = B u(t)
E = 1/2 q'^T M q' + 1/2 q^T K q
P_in = q'^T B u
P_internal = q'^T R_internal q'
P_load = q'^T R_load q'
dE/dt = P_in - P_internal - P_load
```
Require M and K symmetric positive definite; both R matrices symmetric positive semidefinite. The off-diagonal coupling must preserve positivity. For a mechanical interpretation, q is displacement (m), M is mass (kg), R is damping (kg/s), K is stiffness (N/m), and Bu is force (N). Electrical analogy may instead use charge coordinates with units fully relabeled. Do not mix the mappings.

**Exact derivation:** multiply the equation by q'^T. Symmetry makes q'^T M q'' and q'^T K q derivatives of the kinetic and potential terms. Positive semidefiniteness establishes nonnegative dissipation.

**Observable:** energy residual
```
r(t) = E(t)-E(0)-integral(P_in-P_internal-P_load) dt
```
and steady-state readout gain versus angular frequency. Report residual relative to a nonzero energy scale, not relative to instantaneous energy near zero. A resonant gain exceeding one is not an energy efficiency above one.

**Controls:** zero forcing; zero coupling with zero receiver initial state; detuning; added passive loading; timestep/tolerance refinement; independent frequency-domain transfer solution. If starting energy is nonzero, it must be included in cumulative output accounting.

**Falsifier / rejection gate:** unforced energy rises beyond integration uncertainty, cumulative delivered energy plus losses exceeds input plus initial storage, or a claimed loading-free gain disappears in the full model. First reject the implementation or model assumptions; a numerical error is not evidence for free energy.

**What counts as success:** code reproduces the exact identity and all nulls; the site shows amplitude gain and energy flow side by side. Scope is a finite passive model only. Proposed in round 1, not executed by this researcher.

## Target T2 — eigenfrequency versus spectral-peak identifiability

**Historical inspiration:** Earth resonance. **Modern interpretation:** distinguish a cavity parameter from a source/readout-shaped peak.

For a thin ideal spherical shell:
```
omega_l = (c/R) sqrt(l(l+1)), l=1,2,...
f_l = omega_l/(2*pi)
```
For a deliberately simplified damped modal surrogate:
```
x_l'' + 2 gamma_l x_l' + omega_l^2 x_l = d_l(t)
H_l(omega) = 1 / (omega_l^2-omega^2 + 2 i gamma_l omega)
S_y(omega) = |C(omega)|^2 |H_l(omega)|^2 S_d(omega)
```
The last line is the scalar, single-mode, independent-noise-free case; multiple correlated modes require the cross-spectral matrix, not a sum of powers by assumption.

With white forcing and flat displacement readout, differentiating the denominator gives:
```
omega_peak^2 = omega_l^2 - 2 gamma_l^2
```
when positive. This formula is not universal across colored forcing or velocity/acceleration readouts.

**Identifiability check:** a single measured power spectrum generally identifies only the product of source, response and readout powers. For a positive candidate response H, a compensating S_d can reproduce the same S_y. A fit with freely adjustable drive spectrum is therefore not a unique determination of a hidden force or biological coupling.

**Observable:** peak location and width, held-out mode ratios, multiple readout channels. **Controls:** flat versus colored input, fixed versus changed detector, damping sweep, synthetic known poles, shuffled alignment for cross-channel claims.

**Falsifier:** a supposed universal frequency changes under a source/readout change while the pole stays fixed, or a one-parameter effective-speed fit misses held-out modes outside declared uncertainty.

**Acceptance:** separately label ideal shell, lossy surrogate and actual observations; avoid exact-integer “harmonics” for the observed Schumann sequence. Do not implement the 2026 paper's calibration blindly: the advisor found an apparent HTML Eq.(1) variable-definition inconsistency (X and Y both printed as ln(df2H), versus surrounding vertical-coordinate text ln(W)). Original PDF or author correction must resolve this before numerical reuse. Qualitative peak/eigenvalue distinction remains readable. [SR-2011, SR-2026]

## Target T3 — “one total frequency” as a falsifiable measurement proposal

**Inspiration:** ask whether a single scalar can summarize a whole body or pure object. **Modern interpretation:** specify exactly which aspect is predicted by that scalar.

A generic multichannel model is:
```
y_j(t) = H_j[x(t)] + epsilon_j(t)
```
The state x may have several independent oscillatory components. A simple constructive counterexample is x=(sin(2*pi*f_a*t), sin(2*pi*f_b*t)) with f_a/f_b irrational: there is no common exact fundamental period. Readouts selecting each component return distinct rates. Even rationally related components need a defined observation window and resolution before a fundamental is estimated.

**Simulation contract:** create synthetic ECG-like, respiration-like and EEG-like *illustrations*, each explicitly labeled synthetic; never present waveform fixtures as recordings. Compare each channel spectrum with a scalar summary that is declared in advance. Include mixtures with an aperiodic background, sampling aliases and filters. A second phase may analyze licensed public PSG recordings, but this is not yet executed.

**Observable:** per-channel spectrum, cross-spectrum/coherence, uncertainty from windows and noise. Physical units stay separate; averaging Hz values from different processes is not a total physiological frequency.

**Controls:** channel permutation; time shuffling; sample-rate and filter changes; stage-stratified windows; injected artifacts; hidden-parameter recovery on synthetic fixtures.

**Falsifier:** a claimed sensor-independent scalar cannot predict held-out channel spectra or changes simply when channel gain, filtering or sensor placement changes. A compressed summary can remain useful for a narrowly defined prediction; it cannot become an ontological frequency without further evidence.

**Clinical boundary:** modern magnetic stimulation has specific device and indication evidence. The 2024 cited trial compared two active treatments, not a Schumann generator with sham. The 2026 EEG-classifier preprint is a predictive research lead, not a treatment-effect result. Neither validates “unlocking powers,” audio healing, or arbitrary RF exposure. [BIO-2024, BIO-2026]

## Additional audit branch — antigravity and source-free energy

For an isolated classical multibody simulation, track total center of mass and momentum including chassis, motors and moving loads. Internal actuation changes shape and orientation but cannot create total linear momentum without an external exchange. Compare a free system with a frictional substrate: a crawling mechanism can move relative to a surface while transferring momentum to that surface. This is a useful controlled explanation for apparent reactionless-motion demonstrations, not a blanket experiment-specific verdict.

For fields, include radiated momentum, external fields, cables and environment. A missing budget term is a failed certificate, not proof of a new force. The Pais patent lacks a validated operational bridge in the portions inspected. The recent Ordutowski patent is retained as an audit lead. NASA's report supplies a concrete counterexample to interpreting atmospheric thrust as gravity reduction.

## Diagram briefs for implementation

1. **T1 exact vector schematic:** source → two coupled resonators → passive load, with separate internal-loss branches, storage boxes, input/output power labels, and full-system boundary. Show a source-off panel. No body silhouette or high-voltage build specifications.
2. **T2 exact chart and shell diagram:** Earth/ionosphere boundaries; lightning driver; detector; distinct eigenvalue/power-peak annotations. Show flat-versus-colored-source spectra from the same pole. Label it a simplified conceptual model.
3. **T3 channel atlas:** one subject/object connects to *measurement categories*, each with units and its own spectrum. A 3D conceptual laboratory illustration can depict a workstation and inert phantom but must say “conceptual simulation setup,” not a successful healing machine.

Use code/SVG for the exact scientific relationships. Any image-generated 3D art is an illustration and carries no quantitative evidence.

## Evidence and open leads

Machine-readable ledger: `sources-tesla.json` (15 entries). Each entry includes exact URL, sections read, depth, date, provenance, claim type, model/observable/control and unresolved verification.

- Primary historical text: TES-1898; TES-1905; TES-1901.
- Primary physics: SR-2011, SR-2026, NASA-ACT2004.
- Current bioelectromagnetic/data context: BIO-FDA, BIO-2024, BIO-2026, BIO-PSG2026, BIO-SLP1999.
- Patent/government leads: PAT-PAIS2018, PAT-2026, FBI-CATALOG.
- Fringe discourse: FRINGE-SR. It is evidence of claims circulating, not evidence those claims are true.

The FBI archive scans, original electrotherapy magazine facsimile, full 2026 preprint methods, the original Schumann 1952 derivation, and independent Pais performance data remain unread/unverified leads. Do not promote them to completed reading in the website.

## Round 2 recommendation

Freeze T1 first because it has an exact identity and clear null controls. Let an independent implementation check it. Use that review to choose whether T2's source/readout ambiguity or T3's multichannel counterexample adds the more important safeguard. Do not label source gathering, simulations and deployment as three adaptive research loops; a loop needs a decision changed by review.

