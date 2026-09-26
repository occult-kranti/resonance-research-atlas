# Nanoparticle panel: first selection

2026-09-26. Exactly five new adaptive rounds are authorized. The prior six rounds are preserved. This is a review by model agents with correlated model-family provenance, not historical-person participation or human peer review.

## Incoming source and question

The advisor independently read Rosensweig (2002), DOI 10.1016/S0304-8853(02)00706-0, author-uploaded full text, sections 2–4, equations 2–14: https://www.researchgate.net/publication/216213378_Heating_Magnetic_Fluid_with_Alternating_Magnetic_Field . This establishes a declared relaxation model, not a measurement of our hypothetical sample. The text extraction of equation 5 is garbled; the implementation must use the independently derivable closed-cycle work identity and the clear equations 6–9 instead. The source restricts its discussion to low-frequency relaxation relative to ferromagnetic resonance; arbitrary upper dimensionless sweep points are mathematical extrapolations, not material predictions.

Select N1: when susceptibility loss peaks, does heating power also peak during a frequency sweep? Freeze a synthetic, constant susceptibility χ0=0.02, relaxation time τ=10^-6 s, and peak field H0=1 A/m before execution. No particular material, concentration, magnetic moment, dose or biological target is identified by these values.

## Independent derivation and discriminator

For τ dM/dt + M = χ0 H0 cos(ωt), set x=ωτ. Then χ'=χ0/(1+x²), χ''=χ0 x/(1+x²). Closed-cycle work density is −μ0∮M dH=π μ0 H0² χ'' J/m³; average power is f times this work, in W/m³. At fixed χ0, τ and H0, the loss per cycle peaks at x=1, while power is μ0 χ0 H0²/(2τ) times x²/(1+x²), strictly increasing for positive x and bounded by its asymptote. Varying τ at fixed f is a different intervention and may produce a finite power maximum.

The same ODE supplies a passive storage identity: e=μ0 M²/(2χ0), p_in=μ0 H dM/dt and p_loss=μ0 τ (dM/dt)²/χ0≥0. Thus p_in=de/dt+p_loss. The producer's phase-domain ODE and a separate sampled loop integral will be compared at x=0.1, 1, 10, with convergence. Initial-state or settling conventions must be recorded; a nonclosed transient loop requires an endpoint term before integration-by-parts equivalence is claimed.

## Hypothesis, rival and measurement concept

Hypothesis: a weak-field, effectively single-time sealed magnetic reference exhibits the declared Debye susceptibility relation over a calibrated interval. Rival: changing drive amplitude with frequency, relaxation-time distributions, nonlinear response or parasitic heating creates apparent peaks. A future nonclinical measurement would compare a sealed reference against carrier blank, measure actual field amplitude and phase independently, and compare loss susceptibility with separately calibrated calorimetry. This is an instrument concept, not instructions for a human exposure or a high-power coil build.

The mathematical result will be admitted only after independent source/code/output review. N2–N5 are not yet selected. N1's limits may motivate thermal inverse inference, Brownian/acoustic scale comparison, optical-sign inference or an audio-to-actuator transfer audit, but these routes depend on the previous round's actual finding.

## Historical lenses

Tesla motivates measured phase, source, coupling and losses; Newton motivates inverse reconstruction and independent assays; Feynman motivates an explicit rival and a control that could defeat the preferred explanation. Jung's symbolic associations can organize cultural questions but do not supply chemical identification. Penrose motivates stating the model boundary; no cross-scale quantum mechanism follows merely from invoking it. These are present-day methodological interpretations, not claims that the historical figures participated or knew modern nanoparticles.
