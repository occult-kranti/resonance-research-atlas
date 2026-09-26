# Advisor review of Round 1 and selection of Round 2

Decision date: 2026-09-26 (user timezone). Round 1 is accepted within its frozen finite mechanical model. Round 2 is selected from its unresolved measurement-map limitation; it was not run in advance.

## Round 1 independent review

Read `research/round1/contract.md` and the complete solver. Contract SHA256 remained `1e66586ee0f4ac4f740b07eeef57d90c8982583cb06356844fe7ceed295dc72d`. Producer reported 15 production checks and four focused unit tests passing. The independent review did not import or call the producer's solver.

| Independent calculation | Observed discrepancy | Interpretation |
|---|---:|---|
| Reconstruct E=1/2 vᵀv+1/2 qᵀKq directly from CSV | ≤5.21×10⁻18 J against saved E | State-to-energy columns agree |
| Reconstruct source and loss powers from q-dot, clock and fixed parameters | 0 at stored floating-point precision | CSV power columns agree |
| Independent trapezoidal source/loss integration at dt=0.002 s | Endpoint closure magnitude 2.780×10⁻9 J | Below frozen 10⁻6 J budget; different quadrature from augmented RK4 |
| Coarsen quadrature to dt=0.016, 0.008, 0.004 s | Closure magnitudes 2.032×10⁻7, 5.032×10⁻8, 1.228×10⁻8 J | Approximately second-order reduction toward finer quadrature |
| Exact augmented linear matrix exponential at 5, 10, 15, 20 s | Max q error ≤9.17×10⁻11 m; v ≤2.38×10⁻8 m/s | Independent full transient solution agrees |
| Closed-form complex 2×2 inverse over saved frequency sweep | Amplitude difference ≤2.09×10⁻17 m; mean power ≤1.83×10⁻17 W | Independent frequency-domain formula agrees |

The exact transient calculation used z=(q1,q2,v1,v2,sin(ωt),cos(ωt)), z(0)=(0,0,0,0,0,1), and a constant six-dimensional generator with q-dot=v, v-dot=−Kq−0.4v+(0.1sin(ωt),0), sine-dot=ωcosine and cosine-dot=−ωsine. SciPy's matrix exponential was a separate numerical method. The independent phasor used a=k0+kc−ω²+iωc and det=a²−kc², yielding Q=(F a/det,F kc/det). Both use the frozen mass of 1 kg.

Independent values, dependency versions and input hashes are preserved in `research/round1/independent-review.json`.

**Admitted result.** In the chosen model and tested parameter ranges, resonant amplitude increase is compatible with source-supplied energy and positive losses. The baseline input work 0.0949329661 J accounts for final stored energy 0.0151181762 J and dissipation 0.0798147903 J. The analytical identity holds under the stated symmetry/passivity assumptions; finite computations support the implementation only over their tested intervals.

**Remaining gap.** Nothing in a passive mechanical energy audit identifies a particular body state, Earth cavity, or source-free mechanism. Even a correct oscillator can produce different measured peak frequencies under different observation maps. This gap selects the next experiment.

## Round 2 selected target

One stable oscillator x''+2γx'+ω0²x=d has transfer H(ω)=1/(ω0²−ω²+2iγω). With white forcing and displacement readout, its nonzero power maximum is sqrt(ω0²−2γ²), if that expression is real. With velocity readout the maximum is ω0. Its poles remain −γ±sqrt(γ²−ω0²). Thus undamped natural frequency, damped oscillation frequency, and driven power maximum are different defined quantities.

Freeze the exact units, PSD conventions, parameters, grids and tolerances before execution. The mandatory controls are a fixed denominator with changed readout, a strong-damping branch where displacement power is maximal at zero, known poles, and known-source calibrated recovery. An unknown positive source spectrum can compensate a changed positive response; that ambiguity must not be generalized to calibrated full transfer measurements.

The ideal Earth-shell equation may appear alongside the toy model only with its distinct boundary assumptions. A mode frequency chosen near 7.83 Hz for illustration does not make the mechanical surrogate a model of Earth, physiology or healing.

## Feedback that changed the implementation plan

- Tesla producer proposed the within-mode displacement/velocity control, improving on a trivial switch of dominant distant modes.
- Skeptic required the positive calibrated-recovery control: peak ambiguity is not universal impossibility of parameter identification.
- The 2026 Annales Geophysicae article's qualitative distinction is usable. Its HTML Eq.(1) defines X and Y inconsistently with the surrounding text; no numerical calibration from that equation is admitted until resolved.
- The next Newton lane will test the inherited archive's unique visual-sign→composition inference rather than merely append cautions. A 2×3 measurement matrix has a structural kernel even when its two returned singular values are positive; rank, domain dimension and an explicit kernel will be required.

## Skills applied and review provenance

Applied historical-physics-panel and its lens/evidence guide; Newton analysis/synthesis and its research and hidden-causes references; Tesla mechanism/resonance and its research and Earth-modes/loading references; and the new resonance-research-advisor skill/contracts.

Concrete workflow improvements from this usage: restrict time reversal to valid conservative dynamics; add independent quadrature/analytical limits to avoid shared RK-stage bookkeeping errors; retain internal source notation conflicts; test injectivity by domain nullity rather than the smallest returned rectangular-SVD value alone.

Separate agents supplied history, Tesla source research, implementation and skeptical calculations, but they share model-family provenance. This is not human peer review.
