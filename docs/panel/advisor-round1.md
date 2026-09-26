# Advisor decision record: first frozen target and adaptive research roadmap

Status: Round 1 selected for production; Rounds 2 and 3 are conditional selections, not executed results.
Review date: 2026-09-26 (user timezone). Agents share a model family; this is structured independent model review, not human peer review. Historical names identify documented research lenses and do not imply participation or endorsement.

## What this program can establish

The first release should make a small set of claims reproducible: an energy audit of driven resonance, a distinction between measured spectra and inferred mechanisms, and an inverse problem motivated by Newton's laboratory notes. Its new contribution is the integrated source-to-model-to-control workbench and explicit failed-inference demonstrations. The equations are established mathematics; neither new physical laws nor therapeutic, antigravity, transmutation, or metaphysical effects have been demonstrated.

## Admission rule

Every research card must expose the historical assertion, modern interpretation, mathematical model, measured or simulated observable, control, result, and unresolved step. A hypothetical mechanism is admissible for investigation when its alternative prediction and distinguishing control are specified. A successful simulation establishes behavior of its encoded model only.

| Gate | Required artifact | Failure disposition |
|---|---|---|
| Source | Original URL, date/version, section actually read, provenance, exact supported claim | Unread or inaccessible text stays a lead |
| Meaning | Explicit dictionary from historical term to modern quantity | Unmapped symbol stays cultural interpretation |
| Model | State, dynamics, assumptions, initial/boundary conditions, SI units | No physical prediction until frozen |
| Measurement | Sensor/observable, sampling, calibration, bandwidth, nuisance variables | No unique-frequency or identity conclusion |
| Discrimination | Competing model and a control with different predictions | Descriptive illustration only |
| Computation | Reproducible code, parameters, dependency versions, results, error/convergence check | Provisional result |
| Claim | Exact/numerical/empirical status and the narrow conclusion | Remove extrapolation, retain failure |

## Round 1: frozen target

**Question.** Can passive resonance produce a high receiver amplitude while preserving a complete source–storage–loss energy budget, and what does this permit us to infer?

**Historical input.** The Tesla producer read the 1898 article *High Frequency Oscillators for Electro-Therapeutic and Other Purposes*, including synchronism/body-added capacitance and loss/storage discussions. This is evidence for what Tesla wrote and for a resonance/load-inspired question. It is not controlled clinical evidence. URL: https://teslauniverse.com/nikola-tesla/articles/high-frequency-oscillators-electro-therapeutic-and-other-purposes . Specific sections and reading depths belong in the producer's source ledger.

**Frozen model class.** Two linear coupled passive resonators:

\[M\ddot q+R\dot q+Kq=B u(t),\qquad E=\tfrac12\dot q^TM\dot q+\tfrac12q^TKq.\]

Require real symmetric positive definite M and K and positive semidefinite R. For an electrical realization, q is charge in coulombs, M is the inductance matrix in henries, R is resistance in ohms, K is inverse capacitance in F^-1, u is volts, and B is a dimensionless source map. A mechanically equivalent demonstration is acceptable if every unit is replaced consistently and no circuit-value claim is made. Freeze actual parameter values, drive, initial state, integration duration and numerical tolerance in the execution contract before running it.

**Exact identity.** Multiplying the equation by q-dot gives

\[\dot E=\dot q^TBu-\dot q^TR\dot q.\]

Thus E(T)+W_loss(T)=E(0)+W_in(T), where all W terms are joules and W_in is signed work. A load is included exactly once: either within R or as a separately accounted output channel. High amplitude or reactive volt-amperes must not be substituted for net delivered energy.

**Observables.** Two displacement/charge time traces; driven transfer magnitude and phase; initial/final stored energy; signed source work; total dissipation; closure residual. If the implementation is frequency-domain-only, its claim must be steady-state average power, not a verified transient energy trajectory.

**Controls.** Zero input with nonzero stored energy; zero coupling with no receiver initial excitation; off-resonance drive; additional damping/load; timestep or solver-tolerance refinement. Check positive definiteness before propagation. A lossless unforced case must conserve energy up to numerical error; a dissipative unforced case must not gain energy beyond numerical error.

**Acceptance.** Admit the analytical energy identity exactly under its assumptions. Admit numerical energy closure only if the declared residual is below the predeclared tolerance and a finer independent quadrature/step or solver check does not expose an error. Publish the residual denominator and zero-input handling. A large receiver amplitude together with closure is an accepted illustrative result, not evidence of free energy. A failed closure blocks physical interpretation until the defect is repaired and retained in the review record.

**Independent skeptic tasks.** Recompute closure from saved state samples with a separately written calculation; inspect the load accounting; inspect units and determinant/sign conditions; check a control which would fail if coupling or energy bookkeeping were wrong; check that figures use the same parameters as the result file.

## Adaptive decisions after Round 1

Round 2 is selected only after the above review. If closure fails, Round 2 repairs the energy model. If closure passes, the unresolved issue is the measurement map: the circuit model does not identify an Earth's mode, a body property, or a unique object frequency.

Recommended passing branch: **Schumann/measurement identifiability**. Separate the ideal thin-shell eigenfrequency formula f_l=c sqrt(l(l+1))/(2 pi R) from a dissipative, spatially driven spectrum. The first ideal value is about 10.6 Hz for Earth radius 6371 km; 7.83 Hz is not obtained by silently substituting a universal constant. A fitted effective speed is a fit, not a derived physiology parameter. Test whether different mode/source/sensor weights can change a spectral maximum without changing the model's eigenfrequencies. Include off-axis/changed-weight and noise-only controls. Any body/object module should report a vector of operationally defined observables (e.g. voltage spectrum, mechanical transfer, acoustic spectrum), not a single entire frequency.

Round 3 is selected only after Round 2 review. If identifiability checks fail, repair them. Otherwise, transfer the demonstrated inverse-problem limitation to **Newton-inspired mixture identification**. The history producer found a concrete Newton laboratory-note passage with separated extract/residue weights and colors (ALCH00109, Add.3973, f.1r, Dec 15 1678). Proposed modern toy model y=A c, c nonnegative and dimensionless relative concentration, y normalized absorbance, A=[[1,0,1],[0,1,1]]. Mixtures (0,0,1) and (1,1,0) coincide in two channels. An independent third row [1,1,0] should distinguish them; duplicate row [2,0,2] should not. Record rank, null vector, singular values, and residual. This demonstrates a need for independent assays; it does not decipher a historical recipe or demonstrate transmutation.

## Parallel program roadmap

| Lane | Work now | Next dependency | Admission boundary |
|---|---|---|---|
| Integration | Inventory the four named repositories; preserve original apps and attribution; route practical tools, source exhibits, and experiments | Verified builds and deployment routes | Do not claim a code merge from links alone |
| Tesla / energy | Round 1 resonance and load ledger | Review energy controls | No source-free energy inference |
| Earth / signal | Conditional Round 2 modes versus measured peaks | Round 1 review; current calibration paper | No universal biological frequency |
| Newton / laboratory | Conditional Round 3 inverse-mixture assay | Round 2 review; primary notebook passage | No chemistry recipe or transmutation claim |
| Jung / selection | Freeze observations, targets, scoring and null model for symbolic-pattern experiments | Source ledger and preregistered task | Meaningfulness is not causal evidence |
| Penrose / geometry | Separate geometry, model dimension and testable objective-reduction proposals | One specified model and measurement scale | Geometry alone supplies no consciousness mechanism |
| Feynman / metrology | Audit observables, losses, selection effects and damaging counterexamples | Saved datasets and reproducible computation | Simulated agreement is not physical confirmation |
| Government / patent | Link original records; extract actual test or proposal; retain access/reading status | Document-by-document verification | Custody and patent grant do not establish efficacy |
| Speculative apparatus | Source-tagged conceptual 3D views, exact vector schematics, and confound trees for levitation, harvesting, anomalous forces | Named apparatus and measurable alternative hypothesis | Concept illustration is not a build validation |
| Astrology-sim-ant | Keep a separately labeled cultural/discourse and statistical null-testing lane | Prespecified outcomes, holdout data and multiple-test correction | No predicted event becomes causal evidence by retelling |

The website should expose a source/evidence graph with typed edges: historical inspiration, mathematical dependency, implementation, control, supports, contradicts, and unresolved. Graph proximity is not evidence. Suggested statuses: historical record, standard model, simulation passed, simulation failed, empirical result, proposal, inaccessible lead.

## Advisor source reading

1. NIST TN 1297 section 5, especially 5.1–5.5, read via primary NIST page: https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-5-combined-standard-uncertainty . Supports carrying covariance, systematic corrections, and uncertainty assumptions; does not establish a sensor's actual calibration.
2. Malta & Helayël-Neto, arXiv:2208.00527v3 (23 Dec 2022), *Constraining the photon mass via Schumann resonances*, introduction/equation (1), pp.1–2 read: https://arxiv.org/pdf/2208.00527 . Supports the ideal eigenfrequency formula and distinction from finite-conductivity modeled/observed frequencies. Photon-mass claims are outside the present experiment and are not independently verified here.
3. NASA NTRS record *Observation of Schumann Resonances in the Earth's Ionosphere*: https://ntrs.nasa.gov/citations/20120000051 . Advisor read the search record abstract only; the Tesla producer separately reports reading the PDF pp.2–5. Treat these reading depths separately.

Search caution retained: a NASA-hosted public-submission PDF about Schumann/human effects surfaced in discovery. Domain hosting alone does not convert it to NASA-validated experimental evidence. It is not used as an efficacy source here.

## End-of-round record format

For each round retain: selection and why previous evidence caused it; frozen contract before code; producer result; independently checked result; failure/repair history; admitted narrow claim; limitations; next decision. Stop after three actual production–review cycles. Searches, publication, and reruns are not additional research rounds.
