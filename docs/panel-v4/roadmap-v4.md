# Electricity, magnetism and gravity-claim research roadmap

The user redirected the active program after the two accepted sound rounds. Those results are retained as a checkpoint; the remaining three rounds investigate electrical readouts, magnetic work and a gravity-claim discriminator. The authorized program is complete: **five rounds, two loops each**. Research stopped after R5B; publication checks and future physical acquisition do not become extra research rounds.

Current evidence is mathematical derivation, generated data and executed Python. The project has no new hardware readings, measured anomalous force or verified change of gravity. A source-backed proposal, an injected parameter and a real measured effect have different statuses. Historical figures supply documented research methods; the collaborating agents are models with correlated authorship, not human peer review.

## What this continuation adds

| Round | Practical question and deliverable | Admitted boundary / next question |
|---|---|---|
| R1 | A reference slope can remove a stipulated shared gain; generated PCM and explicit inverse kernels | Unknown reference drift or differential gain leaves exact alternative explanations. This selected the full uncertainty budget. |
| R2 | Positive-envelope errors propagate through exact logarithmic boxes; unknown nuisance bounds withhold a physical interval | A small numerical error is not a calibration. The later user pivot changed the application to electrical and force budgets. |
| R3 | A series RLC circuit demonstrates capacitor voltage gain, reactive VA and source-off output with a complete energy ledger | Source/storage/load accounting closes; source off means a closed loop at zero source voltage. Motion-dependent magnetic work was the next missing boundary. |
| R4 | A moving-inductance model includes motional voltage, magnetic energy and mechanical work; equal/opposite support reactions are checked | A 2 mN ordinary magnetic force changes a test-pan reading while g remains fixed. Current parity alone does not identify gravity. |
| R5 | Paired supports, opposite currents and varied known masses test recovery of a defined injected common-acceleration parameter | Independently admitted as a conditional design. A mass-proportional instrument bias is an exact observational rival and cannot be removed by this design alone. |

The exact status, metrics, hashes, disagreements and next selections are in [the decision ledger](../../research/panel-v4-decisions.json) and [the panel log](panel-log.md). [Derivations](derivations.md) state the equations and identifying premises. Known conservation, common-mode subtraction, least squares and coenergy are established methods. The new project contribution is the linked implementation, explicit failure examples, independent checks and prospective experiment design; no new law or literature-priority claim is made.

The exploratory acoustic R3 was executed but not admitted before the user's change of focus. Its archived contract and artifacts remain labeled **parked, unadmitted, excluded from the five-round total**. No new acoustic research is selected here.

## First physical milestone: close the electrical measurement boundary

Purpose: determine whether the proposed measurement chain can recover an ordinary low-voltage energy budget before interpreting a resonant voltage peak.

1. Start with the [electrical schematic](apparatus.md), a characterized isolated low-voltage source, passive components and a known resistive load. The model values are L = 10 mH, C = 100 µF, internal R = 1 Ω and load R = 4 Ω; these are simulation parameters, not measured component properties or a guaranteed parts kit.
2. Record component identity, measured R/L/C, source impedance, voltage/current probe calibration, sensor polarity, bandwidth and time alignment. Unknown tolerances stay unknown. A meter reading or nominal label alone does not certify the energy budget.
3. Perform source-off zero and known-resistive-load controls. Use a separate pilot to choose the sample rate and a fixed integration window. Include the beginning and ending stored energy. Preserve all raw time samples and their units.
4. Lock the waveform, window, baseline and exclusion rules before the comparison. Acquire source voltage and series current contemporaneously; record capacitor voltage and load voltage where the instruments permit. The closed-loop zero-voltage state and an open switch are different circuits.
5. Compute signed source work, load work, internal loss, capacitor-energy change and magnetic-energy change. Inject a known timing shift into a copied file as a negative readout control. Compare against analytic limits and report a deterministic or statistical uncertainty model with its actual calibration source.
6. Stop the inference if missing endpoints, phase/timing uncertainty or unmodeled loss is as large as the claimed residual. A voltage gain or output after shutdown is already explained by the admitted passive model and is not a surplus-energy result.

**Advance gate:** independently reproduced energy closure within a pilot-derived uncertainty budget and a deliberately failed boundary control. **Claim ceiling:** behavior of the measured circuit over the declared range. There is no physical pass yet.

## Second physical milestone: make magnetic reaction forces visible

Purpose: distinguish the force on one pan from the force on the complete supported apparatus.

1. Draw the weighed boundary before building: test object, magnetic source, supports, leads and power supply. Identify which reactions enter each support. The permanent-magnet illustration is a qualitative ordinary-force arrangement; it is not the numerical R4 linear-inductance device.
2. Keep the test object in static contact during a basic scale demonstration. Measure the source reaction on another support or include both interacting subassemblies on one instrument. Retain an unchanged-position baseline and a nonenergized control.
3. For an actual coil/core implementation, measure the finite-range inductance map or another justified force law. R4's L(z) = 0.01 + 0.1z H is stipulated, not inferred from geometry. Hysteresis, saturation, eddy currents and motion require additional terms where present.
4. Compare current reversal, source/sample separation and lead rerouting independently. Include matched heating, position tracking, on/off/cooling segments and pre/post sensor calibration. Randomize or blind the condition order; keep every run and predeclared exclusion.
5. Test whether the test-pan change is balanced by the source-support change. R4 predicts that an internal magnetic force disappears from the complete static support sum. A residual then requires examination of external fields, cables, buoyancy, thermal drift, support coupling and instrument response.

**Advance gate:** repeatable ordinary-force positive controls, verified support boundary and uncertainty on external forces. **Claim ceiling:** a magnetic/support response. A low-material balance demonstration can make reaction forces visible; it does not establish the precision of a gravity experiment.

## Third milestone: test a defined gravity-like parameter

The final numerical design defines δg as a common downward-acceleration change acting on **both** the test and source subassemblies. This is a model deformation, not a measured effect. Paired-support sums cancel included internal forces; opposite-current averaging removes the specified odd force. Across known masses the remaining stipulated model is

\[
S(m)=(m+M)\,\delta g+B.
\]

Under a mass-independent bias B, varying m identifies a slope. The synthetic null and injected positive control test this identifying map. With an unknown mass-proportional bias c, the model becomes \(S=(m+M)(\delta g+c)+B\); δg and c remain inseparable. Repeating the same records or merely adding the same kind of sensor cannot remove that kernel.

1. Specify which proposed gravitational effect acts on which masses and over what region. A local test-only acceleration, a universal acceleration change and a sensor force have different observation maps; do not substitute one for another after seeing data.
2. Use contemporaneous paired supports and several independently known masses. Add a known ordinary calibration force or calibration mass as the physical positive control. The software's injected negative δg is a data test, not a physical gravity actuator.
3. Predeclare the complete on/off and polarity schedule, mass placement, processing and stopping rule. The synthetic ±2 µN contrast bound is an input assumption; no household instrument has been shown to attain it here.
4. Independently constrain mass-dependent calibration, heating and support changes. A material described as nonmagnetic is not automatically insensitive to every field or force. A second sensor only adds identifying information when its response and nuisance coupling are separately characterized.
5. Compare a residual with the complete uncertainty interval and quantitative rival predictions. If a declared ordinary model fails, revise that model and seek external replication. Do not rename the unexplained residual gravity modification.

**Advance gate:** a defensible independent bound on the mass-scaled nuisance or an independently calibrated observation that distinguishes it from δg, followed by replication. **Claim ceiling now:** a conditional model-design result. **Open:** any empirical gravity modification.

## Source and software follow-ups in priority order

| Priority | Bounded next action | Source / dependency | Stop rule |
|---|---|---|---|
| 1 | External reproduction of R3–R5 and actual low-voltage pilot | Frozen contracts, raw numerical outputs, reviewer scripts | Investigate discrepancies; do not silently refresh accepted bytes |
| 2 | Read a full setup and uncertainty budget for the closest magnetic-force measurement | [EM source review](electromagnetism-review.md), Tajmar 2024 and selected balance references | Report scope and resolution; do not transfer a paper's sensitivity to this bench |
| 3 | Fit a measured coil/geometry model only after obtaining data | R4 source/mechanical boundary; calibrated geometry and material response | Unknown constitutive response blocks a quantitative prediction |
| 4 | Resolve a specific electrostatic-thrust proposal's complete momentum boundary | NASA 2004 report and patent claims in the source ledger | Patent or government provenance alone is not a force test |
| 5 | Read full methods for the 2026 superconducting-material lead | Abstract-only lead and recorded internal inconsistency | No gravity, propulsion or energy conclusion from a material transition abstract |
| Parked | Acquire the selected licensed UPV acoustic response if sound work resumes | [Acquisition status](../../research/external/upv-v02/acquisition-status.json) | No acoustic payload was obtained; metadata is not a measured-data result |
| Documentary | Extend one exact historical material occurrence | [Alchemy candidates](alchemy-materials.md), original folio and modern analysis | Names/colours do not uniquely identify an assayed material; no chemical reconstruction selected |

Open-source ngspice and Magpylib are documented options, not executed tools in this release. The current Python environment and actual runner versions are recorded with the results. Add another solver only to resolve a concrete remaining risk or a required replication gate. No sixth research round is selected by this roadmap.
