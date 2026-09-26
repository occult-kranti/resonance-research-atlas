# Passive phantom protocol: test the frequency claim before inferring biology

Status: proposed research design; no phantom experiment, human exposure or treatment trial has been performed. Date: 2026-09-26. This is a bounded supporting protocol, not an executed adaptive research round.

## Question and allowed conclusion

A claim of frequency-specific healing contains several distinct propositions: a source emits a known waveform; the field couples into a body; it changes a biological process; and a clinically meaningful benefit follows. This protocol examines only the **source, passive coupling and thermal/instrument response**. An inert phantom has no healing, consciousness or neuronal endpoint.

The source inspiration is Tesla's 1898 discussion of load-induced retuning [TES-1898]. The model is contemporary electromagnetics and heat transfer. It does not reconstruct his hazardous body-connected demonstrations. A bench realization would use a passive, sealed, nonliving material surrogate and professionally characterized laboratory equipment; this document supplies no human placement, exposure settings, coil-building or treatment instructions.

**Question:** Does a specified passive phantom show a reproducible frequency-dependent coupling feature beyond the feature predicted by independently measured material properties, apparatus transfer function and temperature?

**H0:** The calibrated source–phantom–sensor model accounts for measured coupling and temperature within its frozen uncertainty envelope.

**H1:** One prespecified frequency contrast leaves a reproducible residual exceeding that envelope, including artifact and thermal controls. H1 would identify an unexplained *apparatus/model residual*. It would not establish a therapeutic or metaphysical mechanism.

A successful H0 result can disfavor a claimed special passive-coupling mechanism. It cannot rule out every possible biological response. A failed H0 result first triggers calibration/model review and independent replication.

## Source-reviewed basis

| ID | Exact source and actual reading | What supports this protocol | Scope limit |
|---|---|---|---|
| TES-1898 | [Historical transcription](https://teslauniverse.com/nikola-tesla/articles/high-frequency-oscillators-electro-therapeutic-and-other-purposes); synchronism/load passage | Loading can change the observed oscillator | Historical assertion; original facsimile not authenticated here |
| BIO-FDA | [FDA rTMS guidance](https://www.fda.gov/medical-devices/guidance-documents-medical-devices-and-radiation-emitting-products/repetitive-transcranial-magnetic-stimulation-rtms-systems-class-ii-special-controls-guidance); §5 and §8 plus selected §10 | Predeclared objectives, calibration, failure reporting, EMC and controls | Device-specific guidance; no qualification of our proposed tool |
| PH-FDA-MDDT | [FDA qualification summary, U210149](https://www.fda.gov/media/154181/download?attachment=); all four pages | Example of explicitly scoped electromagnetic-to-thermal phantom validation | MRI-specific qualified tool; cannot transfer its validation to our frequencies, geometry or solver |
| PH-SIMNIBS | [SimNIBS 4.6.0 FAQ](https://simnibs.github.io/simnibs/build/html/faq.html); TACS, TMS and units sections | Field variables and quasistatic approximation are explicit | Constant-conductivity quasistatic scaling does not itself predict new frequency-selective localization |
| PH-AE2026 | [Rintoul et al., Nature Communications, 17 June 2026](https://www.nature.com/articles/s41467-026-73826-2); abstract, introduction and phantom amplitude-characterization opening | Electrical artifacts and multiplicative mixing can accompany another physical stimulus | Selected sections only; reported animal outcomes not reproduced or generalized; this protocol does not implement ultrasound exposure |

PH-AE2026 is an example of why multiple physical channels must be separated, not support for a healing frequency. Its source describes an acoustoelectric mechanism and acknowledges electrical coupling from the transducer. The FDA MDDT illustrates validation against a defined phantom endpoint and explicitly restricted context, not blanket accuracy for all electromagnetic simulations.

## Apparatus block diagram for the UI

Draw an exact SVG with these labeled components and arrows:

- A **waveform command / blinded run ID** feeds a **calibrated source model**.
- The source feeds both a **reference monitor** and the **coupling fixture**.
- The coupling fixture surrounds a **sealed inert phantom**. Show two small marked measurement regions: frozen primary ROI and reference ROI.
- A dashed unwanted path runs directly from source to **sensor electronics**, labeled “electromagnetic pickup / cable coupling.”
- Phantom outputs run separately to **field measurement** and **optical temperature measurement**. A small ambient-temperature box joins the latter.
- Field and temperature channels enter **blind analysis / frozen prediction**, which outputs “consistent,” “unresolved residual,” or “invalid calibration.”
- Beneath the apparatus, a three-card control strip shows **source off**, **matched source load**, and **heat-only reference**.

Enclose the entire apparatus in a “nonclinical passive phantom” boundary. Keep human figures, disease labels, glowing auras and “healing” arrows outside the figure. A 3D illustration may show a translucent phantom block and workbench; it must retain the caption “Conceptual setup — no experimental result.”

UI caption: **“Test what the apparatus produces: field, absorbed energy and heat. A phantom cannot demonstrate healing.”**

## Frozen model and primary observable

Before evaluating outcome data, archive geometry, material lot/version, source impedance, reference-sensor transfer function, instrument bandwidth, analysis code, units, temperature dependence, boundary conditions and uncertainty budget.

The frequency f* comes from the recorded claim under test or a predeclared passive-model feature. It is not assigned as “the frequency of the human.” Use a preregistered dimensionless sweep around f* only within the apparatus calibration bandwidth; the actual band is an instrument-specific dependency, not a medical setting.

For linear passive material and a defined sinusoidal component:
```
P_ROI(f) = integral_ROI Re[sigma_eff(r,f,T)] |E_rms(r,f)|^2 dV
eta_ROI(f) = P_ROI(f) / P_accepted(f)
```
Here sigma_eff is the measured effective conductive admittance density (S/m), including any dielectric-loss contribution exactly once. E_rms is V/m, volume is m^3, both powers are W and eta is dimensionless. P_accepted includes measured accepted source power after reflected/reactive effects are handled. Total stored reactive energy is not counted as delivered energy.

**Primary observable:** the difference between measured and frozen-model eta_ROI at f*, contrasted with the average of two preregistered flanking frequencies. This tests a narrow feature rather than searching a sweep for the largest effect. ROI, flanks, spectral window and model must be selected using calibration/model data, before blinded outcome runs.

**Secondary observable:** temperature-change field versus the passive heat equation:
```
rho c_p dT/dt = divergence(k grad(T)) + p_abs
```
with measured boundary heat exchange and initial temperature. This inert model has no metabolism, perfusion or tissue repair. Density, heat capacity and conductivity are independently characterized parameters.

If P_accepted or P_ROI is below the calibrated detection limit, report an upper bound or “unresolved”; do not divide by a noisy near-zero denominator. During source-off runs, use absolute noise/pickup metrics rather than eta.

## Control matrix

| Condition | What it isolates | Required observation |
|---|---|---|
| Source off, electronics on | Ambient and analysis baseline | No source-locked signal above declared noise bounds |
| Source active into matched dummy load | Electronics, clock, cables and source-state artifacts | Any residual channel response is recorded as pickup, not phantom coupling |
| Coupling fixture present, inert geometry changed | Ordinary boundary/material effects | Field change should follow updated Maxwell model within error |
| Heat-only reference | Temperature-dependent material and sensor drift | Reproduce the prespecified temperature trajectory without the electromagnetic input |
| Equal accepted power across frequencies | Unequal source delivery | Compare actual accepted power; same knob setting is insufficient |
| Equal deposited-power secondary comparison | Thermal dose differences | Separate spatial-distribution effects from total heating |
| Independent sensor modality and sensor swap | Probe transfer and localization bias | Feature persists under calibrated measurement-method change |
| Blind run IDs, randomized order, fixed settling criterion | Drift, order effects and expectation | Analysis produces the same result before and after label unblinding |

The heat-only reference is not automatically a perfect sham: it can match a few temperature probes while missing the internal temperature field. Quantify the mismatch and carry it into uncertainty. Similarly, a dummy load cannot recreate every field path; combine it with cable-routing and sensor-only tests. A shield can change the actual field and source loading, so remeasure power and transfer response after inserting it.

## Artifact countermeasures and decision rule

Use separate reference measurements for source output and sensor pickup. Optical temperature sensing is a candidate way to reduce direct electrical coupling, but probe perturbation, optical calibration and placement uncertainty still require measurement. Store raw waveforms; avoid a post hoc filter that creates or shifts a desired feature. Respect sampling/anti-alias bandwidth and use leakage-aware spectral estimates.

Model material dispersion when measured; do not run a frequency-independent quasistatic solver and reinterpret its arbitrary sinusoid label as proof of a special material resonance. Include uncertainty in geometry, placement, material loss, accepted power, phase, clock, ambient drift and thermal boundary conditions.

A calibration-only pilot sets repeatability, detection limits and the number of independently repeated runs. Freeze that design before outcome evaluation. Do not count many samples from one run as many independent experiments. Use a single primary contrast; label all other contrasts exploratory with multiplicity handled.

Decision thresholds must come from a prespecified uncertainty calculation and sensitivity target, not an arbitrary p-value alone. “Significant” is insufficient if the effect is smaller than the calibration/model error. Reject the dataset as inconclusive if a frozen validity control fails. A residual that passes the control matrix warrants independent apparatus/analysis replication and model revision; it is not permission to infer healing.

## Patent and government record audit

| Source ID | Read status | What is actually established | Not established |
|---|---|---|---|
| TES-1901 | Selected patent description and Fig.1–4 discussion | Tesla proposed collection/storage from external radiation | Source-free output or measured efficiency |
| TES-1905 | Selected patent resonance conditions | Historical terrestrial model and rate assertion | Identity with Schumann theory or measured global power transfer |
| PAT-PAIS2018 | Bibliography, summary, selected description, claims 1–4 | A Navy-assigned patent makes mass-reduction claims | Independent calibrated mass-reduction experiment |
| PAT-2026 | Metadata, abstract, opening description/classification | An individual 2026 motor/load propulsion patent exists | Government validation or demonstrated reactionless motion |
| NASA-ACT2004 | Catalogue plus report model/conclusion | Tested thrust fit ion/gas momentum transfer within reported conditions | Universal proof about every propulsion proposal |
| FBI-CATALOG | Catalogue and Part01 wrapper only | Three archive parts are available | Contents of unread scans, a suppressed successful device, or a validated healing method |
| PH-FDA-MDDT | Qualification summary read | A specified MRI phantom modeling tool received a bounded qualification | Qualification of this project or clinical benefit |

The ledger in sources-tesla.json contains exact patent/government URLs. Archive custody, government authorship and grant are different evidence categories.

## Imported-project status

The repository-recovery/historical agent reports that inherited **resonant-vessels** materials claim six simulations while corresponding runnable code/results were not located. This report is an imported claim-status note, not this researcher's independent reproduction.

Until files, environment, input contract, output, checksums and tests are recovered, label them **“inherited narrative — execution unverified.”** Do not count those six claims as completed validations, use them to select favorable outcomes, or overwrite them with fresh toy simulations presented as their historical rerun.

## Limits and next gate

No human or animal procedure, treatment recommendation or efficacy result is included. The proposed phantom can test passive coupling and artifact explanations only. Biological benefit needs a separate operational mechanism and independent appropriate evidence.

The next authorized action is advisor selection of a computational target after the current round's results. This protocol does not claim another executed research loop.

