# Prospective electrical and magnetic measurement protocol

This is a plan for obtaining new evidence. The completed v4 rounds used synthetic data and numerical models; none of the physical steps below has been performed. Begin with the inexpensive ordinary-effect controls, then assess whether the available instruments can answer a narrower question. The [full roadmap](../../docs/panel-v4/roadmap-v4.md) supplies advance and stop gates.

## 1. Lock the observation and system boundary

Choose one target: electrical energy closure, magnetic support-force change, or the specified common-acceleration model. Record the source, load, test object, magnetic source, supports, leads, sensors and external fields. State which components lie inside each energy or force boundary. The [apparatus record](../../docs/panel-v4/apparatus.md) distinguishes exact numerical schematics from qualitative physical arrangements and concept artwork.

Create a new acquisition folder and plan. Give every raw recording an immutable filename and hash. Record timestamps, instruments, sample units, calibration, uncertainty sources, geometry, source settings, component identity, software processing and condition order. Choose pilot and confirmatory data separately. Keep failed trials and exclusions; a missing condition cannot silently become a completed comparison.

## 2. Start with an ordinary low-voltage electrical control

The R3 model uses a 1 V peak ideal source, 10 mH inductance, 100 µF capacitance, 1 Ω internal resistance and 4 Ω load. These are stipulated model values, not measured components or a proven hardware kit. A physical build needs characterized components, source impedance, suitable current limits and measurement bandwidth.

First measure a known resistive load and source-off zero. Record synchronized source voltage and series current, retaining their signs and time alignment. Record capacitor voltage and the load boundary where the instruments permit. Freeze the integration window and endpoint convention from a separate pilot.

Compute:

\[
W_{in}=\int v_s i\,dt,\quad W_{load}=\int R_l i^2dt,\quad W_{internal}=\int R_i i^2dt,
\]

\[
\Delta E=\Delta(\tfrac12 Li^2+\tfrac12 Cv_C^2),\quad r=W_{in}-W_{load}-W_{internal}-\Delta E.
\]

A real apparatus may need additional storage and loss terms. Deliberately introduce a known channel timing shift into a copy of the data and show how it changes the budget. Treat RMS voltage times RMS current as apparent VA unless the phase relationship is included. A voltage ratio is not an energy ratio.

In the simulation, source off means voltage set to zero **with the loop closed**. Opening a switch is a different circuit and transient. Positive load work after shutdown may come from stored energy; measure both endpoints before interpreting it.

Advance only when the independent uncertainty budget is smaller than the effect of interest and the known controls behave as predicted. Unknown calibration does not become zero uncertainty.

## 3. Measure both sides of an ordinary magnetic interaction

For a qualitative static demonstration, keep the test object in contact on a scale and support the magnetic source separately. Record the source-support reaction where possible, or weigh the complete pair. Do not equate a reduced test-pan indication with changed gravity.

R4's model has L(z) = 0.01 + 0.1z H over z = 0–0.02 m, maintained current 0.2 A and an upward model force of 2 mN. Its half-cosine motion is prescribed. The actual L(z) map, hysteresis, saturation and loss are unmeasured. The illustrated permanent-magnet balance is a different qualitative apparatus; its 8 cm gap is not validated by the linear-inductance model.

Check zero current, current reversal, unchanged placement, source/sample separation and lead routing separately. Track temperature and position, include matched heating and cooling segments, and preserve pre/post calibration. An induced magnetic force may be even in current, so reversal alone does not isolate gravity. If the test and source are both inside a complete static boundary, their internal forces should cancel in the support sum.

For moving magnetic components, include source work, magnetic-energy change, heat and mechanical work in one boundary. Fixed-current and fixed-flux derivatives are different constraints. The fixed-flux R4 control is an ideal lossless model; no practical constant-flux device has been built here.

## 4. Use the gravity-like design only with explicit premises

R5 defines δg as a hypothetical common downward-acceleration change acting on both test and source subassemblies. Its synthetic test masses are 5, 15, 25 and 35 g; the source/stator mass is 100 g. For each mass, contemporaneous paired-support contrasts are recorded at opposite current polarities. The modeled support sum and polarity average obey

\[
S(m)=(m+M)\delta g+B
\]

only if the remaining even bias B is independent of mass and polarity. The simulated null and injected δg = −0.02 m/s² are software controls. A physical positive control should use a known ordinary calibration force or mass, with its uncertainty recorded; the injection is not a gravity-changing device.

The numerical ±2 µN per-support contrast bound already includes baseline-subtraction error and is supplied as an assumption. It has not been demonstrated on any instrument. Worst-case errors add; averaging does not justify dividing this bound by a square root. The selected mass design gives a theoretical acceleration-slope halfwidth of 0.00032 m/s² under that bound. The 1e-12 m/s² implementation guard is separately numerical.

An ordinary bias proportional to mass gives the same observations as the injected δg. If its bound is unknown, `fit_paired` intentionally returns no physical-gravity interval. Adding more copies of the same ambiguous sensor does not fix this. A meaningful next experiment needs an independently characterized observation or nuisance bound that distinguishes the competing mechanisms. Static contact loss, unresolved external forces or calibration drift block a static gravity interpretation.

## 5. Preserve and report what actually happened

Report all planned conditions, exclusions, raw-file hashes, calibration inputs, model parameters and uncertainty assumptions. Label simulations, external data and newly measured data separately. Compare the result with predeclared competing predictions. A residual outside one ordinary model's budget calls for a model and apparatus audit plus external replication; it does not by itself identify a new force.

The accepted R1–R2 sound checkpoint and the parked acoustic branch remain available, but no further sound experiment or sixth numerical round is selected in this continuation.
