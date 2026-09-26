# Nanoparticles: mechanisms before frequency labels

Research snapshot: 26 September 2026. These are contemporary model-agent proposals informed by selected primary sources. They are not Tesla's reconstructed intentions, clinical recommendations, a completed empirical experiment, or an exhaustive literature review. Source IDs resolve in `sources-modern.json`; reading depth is deliberately explicit. The advisor selects each next computational round only after reviewing the preceding result.

The useful Tesla-inspired method is to name the source, coupling path, phase, load and energy loss, then change one physical condition. A resonant response does not supply energy by itself. Newton-inspired inverse analysis asks whether the measured signal uniquely determines the proposed mechanism. Together these methods replace a proposed universal nanoparticle frequency with a testable apparatus-and-sample model.

| Modality | Actual drive | Material response | Measurement required | Major confound |
|---|---|---|---|---|
| Magnetic | H(t), A/m; field direction and geometry | Magnetization M, A/m; relaxation/hysteresis | Calibrated complex susceptibility or cycle work | Drive leakage, size distribution, interactions, temperature |
| Acoustic | Pressure p, Pa; fluid velocity, m/s | Radiation force, streaming drag, Brownian motion | Trajectories plus calibrated field and flow | Streaming or adhesion mistaken for a conservative trap |
| Optical | Irradiance I, W/m²; wavelength, polarization | Absorption/scattering, optical forces, heating | Extinction separated from absorption; independent temperature | Optical response drift, scattering, thermal gradients |
| Audio control | Digital amplitude/phase and sample rate | Only the connected transducer determines a physical field | End-to-end transfer calibration | An audio tone's numerical frequency mistaken for field exposure |

## N1: exact declared magnetic surrogate

Source NANO-ROS2002 §§2–4 supplies the standard relaxation construction. In SI, let H(t)=Hpeak cos(ωt), with H and M in A/m, B=μ0(H+M) in tesla, and x=ωτ. Susceptibility is dimensionless and referred to total suspension volume. Choose the exp(+iωt) phasor convention:

\[
\tau\dot M+M=\chi_0H,\qquad
\chi=\chi'-i\chi''=\frac{\chi_0}{1+ix},\quad
\chi'=\frac{\chi_0}{1+x^2},\quad
\chi''=\frac{\chi_0x}{1+x^2}.
\]

\[
w=-\mu_0\oint M\,dH=\pi\mu_0H_{peak}^2\chi''\quad[\mathrm{J/m^3}],\qquad
p=fw=\frac{\mu_0\chi_0H_{peak}^2}{2\tau}\frac{x^2}{1+x^2}\quad[\mathrm{W/m^3}].
\]

At fixed Hpeak, χ0 and τ, w peaks at x=1; p increases toward a plateau. Replacing a frequency sweep by a viscosity or τ sweep at fixed f changes the intervention and can change the position of a power maximum. Peak versus RMS amplitude matters: p=2πμ0 f Hrms²χ''. Dividing by iron mass requires an independently known iron mass per suspension volume; a dimensionless susceptibility must not silently become a mass susceptibility.

The passive energy identity is e=μ0M²/(2χ0), pin=μ0H Mdot and ploss=μ0τ Mdot²/χ0. Thus pin=edot+ploss. Closed-cycle work equals average dissipation; a transient interval needs its endpoint energy change. This is a mathematical surrogate with fixed temperature and response parameters. The high-frequency limit is not a prediction that any real material remains Debye-like indefinitely.

Admissibility conditions: weak excitation, approximately linear response, effectively single relaxation time, and a stated dilute/noninteracting/single-domain approximation. A small magnetic field in A/m alone cannot prove weak response without magnetic moment and temperature. Distribution width, interactions, anisotropy, structure and field amplitude can invalidate this closure. NANO-GOTO2025 gives an empirical reason to test it rather than presume it.

## Conditional relaxation discriminator

For a spherical freely rotating particle in a Newtonian fluid, τB=3ηVhyd/(kBT). In diameter form, τB=πηd³/(2kBT); at fixed T, fB=1/(2πτB) scales as η⁻¹d⁻³. The magnetic core volume and hydrodynamic volume are distinct. A simplified Néel form τN=τ0 exp(KVcore/kBT) is an Arrhenius approximation; Rosensweig's stated Brown prefactor differs. The inverse-rate relation 1/τeff=1/τN+1/τB is a declared parallel-channel surrogate.

NANO-GOTO2025 compares commercially dispersed particles in liquids with different viscosity and solid immobilization. The project proposal is to compare full calibrated χ′ and χ″ spectra across matched sealed references and an immobilized counterpart. The distinguishing observable is the frequency-dependent phase ratio χ″/χ′ and its viscosity derivative, not only an isolated heating maximum. A rotation-dominated single-time surrogate predicts τ from that ratio proportional to η at fixed T and hydrodynamic size; an immobilized reference can retain internal magnetization relaxation. Counterexample: aggregation, altered anisotropy, size distribution or thermal drift can change the response during immobilization. Failure of single-Debye collapse falsifies that closure, not Brownian motion itself; a successful collapse is not proof of unique microscopic origin.

The low-field initial-susceptibility paragraph following Rosensweig Eq15 adds another distinction: with class number density nj and identical particle-domain magnetization Md, χ0,j=μ0 nj Md² Vcore,j²/(3kBT). Thus equal particle counts need not have equal susceptibility weights; spherical classes scale with dcore⁶ under these assumptions. This is distinct from the dcore³ mass sum and dhydro³ rotational time. A hypothetical40/60nm equal-count population has normalized susceptibility weights64/793 and729/793 in that surrogate, without asserting that any real40–60nm material satisfies the required equilibrium regime.

## N2: power is not a thermometer trace

Use the independently derived lumped first-law model Cθdot=P−Gθ, where θ=T−Tamb, C is total effective heat capacity in J/K, G is thermal conductance in W/K and P is absorbed power in W. A simple thermometer adds τs ydot=θ−y. Starting at ambient, θ=(P/G)(1−exp(−Gt/C)); after switching off, θ decays exponentially. The unlagged instantaneous initial slope is P/C, but a finite window, sensor lag or a preheated initial condition changes the observed slope.

The exact symmetry (P,C,G)→a(P,C,G) leaves the temperature trace unchanged. Therefore a heating/cooling trace without an absolute calibration cannot identify all three. A separately metered resistor in an inert water reference can supply a known power, while cooling and independently measured sensor response constrain different nuisance parameters. This is a proposed nonclinical calibration experiment, not a trial reported here. NANO-SKIN2025 supports cooling/blank/instrument controls but is an optical colloid study; its complete apparatus is not our model.

PDF audit: the actual Skinner Eq6 places τ in the denominator of the entire efficiency expression, making the displayed Qblank in joules dimensionally consistent. OCR could falsely suggest power minus energy. We do not implement that efficiency formula or infer a blank-energy procedure from incomplete extraction.

## Acoustic scale and Brownian counterexample

For the isolated Rayleigh-particle standing-wave approximation with fixed material contrast and field geometry, radiation force scales as particle radius cubed. Stokes drag coefficient scales as a, so deterministic drift scales as a². Brownian diffusivity D=kBT/(6πηa) increases as a shrinks. A minimal overdamped project surrogate is dx=[F(x)/ζ+uflow(x)]dt+sqrt(2D)dW. For a truly conservative harmonic well at equilibrium, variance=kBT/κ; this identity fails as a complete description when imposed flow, walls, heating or multibody forces matter.

A force-to-thermal-work ratio FL/(kBT), a trap depth U/(kBT) and residence/escape distributions are more informative than frequency alone. Proposed falsifier: if measured localization remains when the predicted force is removed but streaming persists, a pure radiation-force account fails. Source NANO-PAVL2025 supports force-ablation thinking and hydrodynamic alternatives in its specified simulations. Its weak Brownian effect for particular cases cannot be extrapolated to arbitrarily smaller particles. NANO-ZHANG2021 shows that an acoustically driven apparatus can manipulate particles through electric fields; electrical shielding is a mechanism-specific control.

## Optical absorption and measurement

For one particle in a specified incident field, Pabs=I Cabs, with I in W/m² and Cabs in m². Extinction is absorption plus scattering under the stated scattering problem. For a sphere, Cabs=πa²(Qext−Qsca); shape, wavelength, environment and dielectric dispersion matter. A material absorption peak, extinction peak, hottest finite-time reading and maximum trapping stability need not coincide. NANO-SKIN2025 supplies an experimental reason to separate these observables; its well-mixed optical thermometry must not be promoted to validated local intracellular thermometry.

Project proposal: hold independently measured absorbed power fixed while changing optical wavelength or coupling geometry, then compare an independent thermometer and optical readout. Null: differences are explained by heat transport and instrument response. Rival explanations include local gradients, changing aggregation, reporter photophysics and scattering redistribution. The new2026 preprint NANO-VENE2026 is an abstract-level lead combining optical heating with magnetic readout; it does not establish a modality-independent healing frequency.

## Open tools and data: declared adoption status

| Resource | Appropriate role | Status here | Required check before adoption |
|---|---|---|---|
| OOMMF, NANO-TOOL-OOMMF | Micromagnetic dynamics | Official project page read; not installed/run | Chosen dynamics/thermal extension, convergence, benchmarks; physical colloid rotation not assumed |
| k-Wave, NANO-TOOL-KWAVE | Acoustic field propagation | Official overview read; not run | Pressure benchmark, attenuation and boundary convergence; separate streaming/particle solver |
| miepython, NANO-TOOL-MIE | Mie sphere absorption/scattering | Official3.3.0 docs read; author reports reference agreement; not run | Pin version, reproduce reference case, validate optical-constant conventions |
| NIST MPI simulator, NANO-NIST-MPISIM | Instrument sensitivity/relaxation modeling | Publication abstract only | Locate license/code, verify against independent fixture |
| Pavlič/Baasch Zenodo10.5281/zenodo.15575920 | Acoustic model data | Article names repository; direct access failed | Inspect actual version/files/license; reproduce one held-out figure |
| Goto2025 supplementary data | Relaxation evidence | Data statement read; files not analyzed | Calibrations, units, missing time windows and uncertainty |

The current program pages NANO-NIST-MAGIC and NANO-NCI-NCL establish active metrology/characterization work, not endorsement of this research. NIST's headline performance targets must remain distinguished from reported instrument accomplishments. The historical agent owns the nanoparticle patent/NIST size-metrology ledger; patent publication or grant establishes a proposal record, not validated performance.

## Candidate new hypotheses, pending adaptive selection

1. **Field-transfer explanation:** correcting actual H amplitude and phase collapses an apparent frequency optimum. Defeated if residual changes exceed combined uncertainty under independent calibration. Alternatives: nonlinear magnetization, temperature drift and distributions.
2. **Finite-window thermal bias:** one constant absorbed power produces different estimated initial slopes when thermometer lag/window changes. Defeated by a calibrated sensor plus heat-loss model failing held-out traces. Alternatives: nonconstant power or two thermal compartments.
3. **Rotation signature:** viscosity changes the loss phase according to hydrodynamic rotation in a matched reference. Defeated by systematic phase/residual behavior outside the predeclared surrogate. Alternatives: aggregation, coating changes and coupled Néel/body dynamics.
4. **Apparent acoustic trap:** observed retention is chiefly hydrodynamic shielding rather than a single-particle potential. Test source-off, flow reversal, seed controls and trajectory statistics. Surface adhesion is a strong alternative.
5. **Optical-thermal ambiguity:** extinction alone overestimates heat deposition. Test separate scattering/absorption balance and independent thermal readout; concentration and geometry errors are rivals.

These are project proposals. The advisor's five frozen contracts and independently reviewed computed results determine which are actually executed. No claim of new empirical discovery follows from this source review.
