# Final nanoparticle panel review: five adaptive rounds

All five new rounds have explicit **accepted** status within their named mathematical or audio scope. No sixth new round is selected. The previous six investigations are preserved. The machine-readable decisions are in `research/nanoparticle-panel-decisions.json`.

The team used separate source researchers, a simulation producer, an advisor/skeptic, and audio/interface implementers. These model agents share correlated model-family provenance. This is structured computational review, not historical-person participation or human peer review. Each new question was selected only after independent admission of its predecessor; collecting sources, building interfaces, replaying calculations and publishing were not counted as extra research rounds.

## Accepted findings and adaptive decisions

| Round | Accepted finding | Why the next question changed |
|---|---|---|
| N1 — cycle loss and power | In a fixed-parameter Debye model, loss per cycle peaks at ωτ = 1, while frequency-swept power continues toward a finite asymptote. At the loss peak, power is half that asymptote. | Predicted heat input does not determine a thermometer trace. |
| N2 — thermal measurement | A true 0.2 W input produces naive estimates of 0.07227, 0.12882 and 0.14688 W over 10, 30 and 60 seconds. The calibrated inverse recovers 0.2 W. | Thermal calibration does not identify a particle relaxation mechanism. |
| N3 — held-out mechanism test | A single Debye fit with unknown amplitude matches a two-population response exactly at 1 kHz, yet differs by 43.0339% at the held-out 10 Hz point. A viscosity series supplies another explicit prediction. | Susceptibility mixture amplitudes are not automatically particle number fractions. |
| N4 — size and weighting | Using mean particle volume removes a 12% number overestimate. Number, mass and conditional susceptibility weights differ; the wrong weights change the normalized spectral prediction by up to 64.1021% on the tested grid. | A correct material-response model still requires calibrated physical excitation. |
| N5 — actual audio and observation | Actual OpenSync exports distinguish input spectrum, an LTI response and an explicit quadratic detector. A one-tone phase reversal preserves RMS and reverses the quadratic beat phase. | Stop after five. Physical transfer and specimen measurements remain empirical work. |

“Accepted” means that the declared source interpretation, mathematical result and stored execution passed this review. It does not establish a physical nanoparticle response, therapy, transmutation, source-free energy, antigravity or a metaphysical effect. A rejected extrapolation is not an empirical refutation of every possible alternative.

## Project hypotheses and improved experiments

**NP-H1: choose the correct objective.** The source model uses peak magnetic field in A/m, dimensionless volume susceptibility, cycle work in J/m³ and mean power in W/m³. Its hypothetical parameters are χ0 = 0.02, τ = 1 μs and H_peak = 1 A/m. The result concerns a frequency sweep with these quantities fixed; varying relaxation time at fixed frequency is a different experiment. The full dimensionless sweep is mathematical extrapolation, not a validated material bandwidth. The nominal μ0 constant is a rounded model value.

The improved experiment measures actual field amplitude and phase, complex susceptibility, heat flow and a carrier blank separately. A prospective extension, NP-H1E, asks whether the apparent relaxation time χ″/(ωχ′) remains constant after independent phase calibration. A mixture may make it vary; phase error is an explicit rival. Rosensweig's established polydispersion work is the nearest checked prior art, so this is a project design rather than a discovery claim.

**NP-H2: test duration-dependent apparent absorption.** The model separates total thermal capacity C, heat conductance G and thermometer time constant τs: Cθ̇ = P − Gθ, τsẏ + y = θ. Multiplying P, C and G by the same positive factor leaves both temperature traces unchanged. Absolute power therefore needs independent capacity or known-input calibration. This does not imply that calibrated thermal inference is impossible.

The improved nonclinical design pairs pulse durations, a carrier blank, a known-power resistor phantom, an independently measured sensor step response and the full heating/cooling trace. If corrected power still changes with duration beyond calibrated uncertainty, the constant-power transfer model fails. Temperature gradients, mixing, changing absorption or sensor error remain competing explanations. Skinner et al. (2025) supplies an inspected contemporary heating/cooling and blank precedent; our first-order sensor law is a declared surrogate, not a fit to that paper's data.

**NP-H3: predict beyond the calibration point.** One candidate is a Debye response with parallel inverse relaxation rates. The other is a positive sum of two independent populations. These are different interpretations, not interchangeable formulas for one known particle. In the first candidate, effective relaxation frequency is linear in inverse viscosity. The first two viscosities determine predictions for the withheld two. In the mixture, a whole-domain derivative proves that apparent relaxation time decreases with frequency when both positive amplitudes are present and their component times differ.

Allowing the rival's susceptibility amplitude to vary permits an exact fit at one complex calibration point. A separately measured DC amplitude could strengthen discrimination there. The project test uses withheld frequencies rather than equating a fitted point with a mechanism. The improved future experiment adds independent field/phase references, temperature and viscosity measurements, core/hydrodynamic size checks and a matched immobilized reference. Solvent changes or immobilization may also change aggregation and anisotropy; a deviation would not uniquely identify Brownian rotation. Goto et al. (2025) already documents system-specific viscosity behavior, so the panel does not claim to invent this intervention.

**NP-H4: identify the weighting before interpreting a mixture.** The exact equal-number 40/60 nm core example has mean cubed diameter 140000 nm³, compared with 125000 nm³ obtained by cubing the mean diameter. Their ratio is 28/25. This reproduces the current particle-count correction described by Farkas et al. (2025).

Under an additional dilute, identical-material, equilibrium weak-field assumption, susceptibility is proportional to number times squared magnetic core volume. The example therefore has number weights (1/2, 1/2), mass weights (8/35, 27/35), and conditional susceptibility weights (64/793, 729/793). Hydrodynamic diameters are separately specified as 50/70 nm for the Brownian locked-moment illustration. No Néel process, absolute susceptibility, coating structure or valid operating regime for a real 40–60 nm material is established.

The improved design independently measures mass concentration, density, a number-weighted core-size distribution and hydrodynamic size before predicting withheld spectral shape. Monodisperse and label-swap controls check the calculation. Aggregation, varying magnetization, interactions and saturation can defeat the simple mapping. A color alone supplies none of these independent quantities.

**NP-H5: discriminate coupling with phase and energy controls.** The final round uses four actual NanoLab WAV exports: a centered two-tone sum, AM, a real baseband tone and a carrier-only control. The frozen recipe is 375 Hz carrier, 23.4375 Hz rate, −24 dBFS gain, two seconds and 48 kHz stereo PCM16. A coherent interior segment excludes the fades. These selected frequencies do not have an input carrier or sideband coincident with the rate; other allowed recipes can, and the interface must inspect the components.

The decoded pair and AM clips have tiny rate components of about 4×10^-7 FS, below the declared quantization comparison bound. Their explicit squared detector signals have rate components near 9.95×10^-4 FS². A linear time-invariant filter changes component gains and phases; it does not explain an appreciable new mixing term. Squaring is a specified nonlinear observation, not an inferred particle force.

Equal peak gain does not give equal RMS. After analysis-only normalization to RMS = 0.02 FS, quadratic rate amplitudes are about 0.0004000 FS² for the pair and 0.0005333 FS² for AM. Reversing the upper pair component preserves mean-square input and reverses the quadratic beat phase, with a numerical reversal residual of 2.69×10^-8 FS². This phase-sensitive prediction is the project's proposed witness for a future coupling test. It uses established modulation and nonlinear-mixing principles, not a new force.

The hardware concept separates DAC/line voltage, transducer, pressure or acceleration witness, sealed inert reference, imaging and blank. Acoustic particle-force models require spatial pressure/velocity fields, material contrast and a potential gradient; hydrodynamic and interaction forces can compete. The checked acoustic papers concern specific apparatus, including hybrid electrical mechanisms. A WAV alone supplies no calibrated pressure, magnetic field, force or nanoparticle motion.

## Independent mathematical and implementation review

The advisor used alternate derivations and preserved precomputations before reading the corresponding producer result files:

- N1: an exact from-rest magnetization solution, direct dimensional sweep and a separately reconstructed passive budget. Maximum saved-state error was 1.86×10^-12 A/m; sampled budget residual was at most 7.32×10^-17 J/m³.
- N2: integrating-factor convolution, an augmented matrix exponential with a separate cooling propagator and an exact heat-leak integral. The matrix solution matched every saved trace point within 8.89×10^-15 K.
- N3: a combined rational susceptibility expression, a whole-domain monotonicity proof and closed-form viscosity coefficients. Stored spectral rows agreed within 6.33×10^-16 relative error; independently frozen held-out predictions matched.
- N4: a central-moment identity and an exact volume-ratio route, followed by cancellation of the common two-pole denominator. The residual formula agreed across every saved frequency within 6.67×10^-16 absolute error.
- N5: Python WAV decoding, direct complex projections rather than FFT, and a real sine/cosine reflection rather than the producer's FFT phase edit. Every stored spectral column agreed within 1.53×10^-16 absolute error. Export SHA values, input snapshots and final review bindings were checked.

Original selection notes, precompute JSON, executed reviewer scripts and portable replay copies are preserved in `research/nanoparticles/reviews/`. Each round's `independent-review.json` binds the source and outputs reviewed. Replaying them checks reproducibility; it is not another independent agent or research round.

## Source disagreements, repairs and historical interpretation

N1's frozen contract had incorrect Rosensweig page numbers. The original is preserved with an explicit bibliographic erratum to pages 370–374; numerical outputs were unchanged. N2's apparent equation-6 unit problem was an OCR-layout artifact: visual inspection of Skinner's PDF resolved it, and no source-error allegation is retained.

Goto's accepted manuscript describes a loss-peak frequency as proportional to viscosity in one passage, whereas its Brownian-time equation gives the inverse scaling used in our stated model. That wording is not used as directional validation. The study's structure-specific departures remain relevant. The audio bench also needed a real edge-case repair: a carrier or sideband can coincide with the named rate. Component accounting, quantization bounds and energy matching now constrain the claim.

Newton's conditional optical arguments and measured residues motivate inverse questions and independent observations. Faraday's later gold/light work supplies mixture-versus-state alternatives; it is not attributed to Newton or Tesla. Tesla supplies source, phase, loading and energy-accounting questions. Jung/Pauli associations remain cultural context; Penrose's specific proposals do not automatically become a colloidal mechanism; Feynman's methodological lens motivates controls, rival explanations and predictions beyond a fit. These are documented present-day research lenses, not simulated historical endorsements.

The source packet includes selected primary literature, patents, government records and clearly labeled fringe leads. Patent disclosure is not a performance measurement, government custody is not confirmation, and an inaccessible forum excerpt is not an analyzed specimen. This is a bounded reading record, not a claim to have reviewed every book, patent or frontier result.

## Novelty, empirical work and release boundary

The contribution is a new project integration: five adaptive hypotheses, executed model and audio benchmarks, independent reviews, corrected measurement designs, actual OpenSync exports, and traceable source/status boundaries. The panel does not claim a newly discovered physical law or historical decipherment. The nearest checked prior art is named for every proposal; a worldwide priority search has not been completed.

Physical specimens, source-to-field calibration, calorimetry, viscosity/immobilization studies, count/size characterization, pressure/velocity gradients and particle tracking remain unperformed. Hardware diagrams are prospective instrument concepts, and generated 3D images are conceptual illustrations. Publishing code or a website does not turn these into empirical results. Parent integration, GitHub publication and live deployment verification are separate release work.
