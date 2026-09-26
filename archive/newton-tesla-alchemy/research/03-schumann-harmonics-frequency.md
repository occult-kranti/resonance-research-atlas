# 03 — Schumann Resonance, Harmonics, and the Frequency Signature of Matter

*Physics dossier for the research archive. Every claim carries an epistemic label:*
**[ESTABLISHED]** = textbook/peer-reviewed consensus; **[HISTORICAL]** = documented record about Tesla and predecessors; **[FRINGE]** = claims circulating in popular culture without demonstrated mechanism or with failed replication; **[SPECULATIVE]** = forward-looking design grounded in established physics but not yet built.

---

## Executive summary

- The Schumann resonances are the electromagnetic eigenmodes of the spherical shell between Earth's surface and the ionosphere, predicted by Winfried Otto Schumann in 1952 and first resolved in measurements by Balser & Wagner in 1960. [ESTABLISHED]
- For an ideal, lossless cavity the eigenfrequencies are exactly **fₙ = (c / 2πa) · √(n(n+1))**, with a = Earth radius, c = speed of light, n = 1, 2, 3, … — a separation constant of the Legendre polynomials. [ESTABLISHED]
- Plugging in a = 6,371 km and c = 299,792.458 km/s (derived independently for this dossier) gives ideal modes 10.59, 18.34, 25.94, 33.49, 41.02 Hz; the *observed* peaks sit lower, at about 7.83, 14.3, 20.8, 27.3, 33.8 Hz, because finite ionospheric conductivity slows propagation and damps the modes (Q ≈ 4–6, peak width ~20%). [ESTABLISHED]

| Mode n | Ideal fₙ (this derivation) | Observed peak (consensus) | Observed/Ideal |
|---|---|---|---|
| 1 | 10.59 Hz | 7.83 Hz | 0.74 |
| 2 | 18.34 Hz | 14.3 Hz | 0.78 |
| 3 | 25.94 Hz | 20.8 Hz | 0.80 |
| 4 | 33.49 Hz | 27.3 Hz | 0.82 |
| 5 | 41.02 Hz | 33.8 Hz | 0.82 |

- The popular claim that the fundamental is "10.6/√2" is numerology: 10.6/√2 = 7.50 Hz, not 7.83 Hz, and √2 has no role in cavity theory. The real correction is a dissipation-induced reduction of the effective ELF phase velocity below c. [ESTABLISHED physics; the √2 story is FRINGE]
- The cavity is rung by ~2,000 active thunderstorms and ~50 lightning strokes per second worldwide; exceptionally strong strokes produce resolvable "Q-bursts" linked to sprites. [ESTABLISHED]
- Resonances are measured with paired horizontal induction-coil magnetometers (signal ~1 pT against Earth's ~50 µT static field) and a vertical ball antenna (~300 µV/m vs ~150 V/m fair-weather field); public stations include Tomsk's Space Observing System and BGS Eskdalemuir. [ESTABLISHED]
- Every solid object has a discrete spectrum of mechanical eigenmodes; engineers map it with impact-hammer + FFT modal analysis, scanning laser Doppler vibrometry, or resonant ultrasound spectroscopy (RUS), which can recover all 21 elastic constants of an anisotropic crystal from one spectrum. [ESTABLISHED]
- Chladni figures are real eigenmode physics: sand collects on nodal lines of a vibrating plate governed by the biharmonic plate equation. [ESTABLISHED]
- Humans have measurable frequency signatures across many physical channels: EEG bands (delta 0.5–4, theta 4–8, alpha 8–13, beta 13–30, gamma 30–100 Hz), ECG ~1 Hz fundamental with HRV, mechano-acoustic BCG/SCG 1–20 Hz, voice F0 85–255 Hz with formants to ~3.5 kHz, and biomagnetic fields (heart ~100 pT, brain ~10–500 fT) via SQUID/OPM magnetometry. [ESTABLISHED]
- The numerical coincidence that 7.83 Hz lies near the theta/alpha EEG boundary is real; Saroka & Persinger reported transient (~300 ms) EEG–Schumann coherence episodes in PLOS ONE (2016), but no coupling mechanism has been demonstrated, the ambient Schumann field (~1 pT) is far weaker than intrinsic brain fields, and Persinger's adjacent paradigms failed independent replication. [FRINGE — "Schumann healing"/entrainment claims]
- Tesla documented "stationary waves" from a receding thunderstorm at Colorado Springs on July 3–4, 1899 — arguably the first observation of Earth–ionosphere cavity phenomena — and his later writings quoted Earth resonance estimates near 6–12 Hz, conceptually anticipating Schumann. [HISTORICAL]
- A modern Tesla-style "whole-organism spectrum" rig — shielded room, ELF coil, EEG/ECG, SQUID or OPM magnetometer, piezo platform, voice/impulse excitation — is entirely buildable at budgets from ~$2k to ~$2M; expected SNR estimates are given in Part 4. [SPECULATIVE design, ESTABLISHED components]
- Characteristic frequencies span at least 18 decades, from Earth's 0.309 mHz gravest free-oscillation mode to molecular vibrations at ~10–100 THz. The atlas table in Part 5 is chart-ready. [ESTABLISHED]

---

## Part 1: The physics of the Schumann resonances

### 1.1 The cavity and the mode formula [ESTABLISHED]

The space between the conducting Earth and the lower ionosphere (~60 km by day, ~90 km by night) forms a spherical waveguide whose height is negligible compared with ELF wavelengths (at 7.83 Hz, λ ≈ 38,000 km — one Earth circumference). Because h ≪ a, the mode structure reduces to the Legendre-polynomial separation constant n(n+1): (ka)² = n(n+1), giving Schumann's formula

**fₙ = (c / 2πa) · √(n(n+1)), n = 1, 2, 3, …**

The formula appears identically in Schumann's 1952 papers, the NASA NTRS review, and the Nickolaenko–Hayakawa monograph [sources 1–5]. Independent derivation for this dossier (c = 299,792,458 m/s, a = 6,371 km) yields c/2πa = 7.4892 Hz and the ideal series 10.59, 18.34, 25.94, 33.49, 41.02, 48.53 Hz — matching textbook values 10.6, 18.3, 25.9, 33.5, 41.0 Hz [3].

### 1.2 Why the real peaks are lower [ESTABLISHED]

The first definitive measurements (Balser & Wagner, New England, 27–28 June 1960) found 7.8, 14.2, 19.6, 25.9, and 32 Hz — well below the ideal series [3, 1]. The cavity walls are *not* perfect conductors: atmospheric conductivity rises gradually with altitude, the ELF wave penetrates the dissipative lower ionosphere, and the effective propagation velocity falls below c. The measured ratios (0.74–0.82, rising with mode number, per the table above) are what dissipative-cavity models predict; Q-factors are only ~4–6 and peaks are broad (~20% spectral width) [1, 5]. Day/night ionosphere asymmetry and other horizontal asymmetries add fine structure [1].

*Note on the "√2 correction":* some secondary literature says the observed fundamental is the ideal 10.6 Hz "divided by √2." Numerically 10.6/√2 = 7.50 Hz — 4% off the real 7.83 Hz, and √2 plays no role in the spherical eigenvalue problem, whose geometry factor is √(n(n+1)). The defensible statement: losses lower each mode by a frequency-dependent factor of roughly 0.74–0.82. Treating √2 as physics is **[FRINGE]** numerology.

### 1.3 Excitation: lightning and Q-bursts [ESTABLISHED]

Roughly 2,000 thunderstorms are active at any moment, producing ~50 flashes per second; lightning channels radiate broadband energy below ~100 kHz and continuously ring the cavity [1]. The diurnal record shows three maxima tied to the tropical "chimneys": Southeast Asia (~09 UT), Africa (~14 UT), South America (~20 UT) [1]. Exceptionally intense positive cloud-to-ground strokes generate isolated transients called Q-bursts — exceeding background 10×, recurring on ~10 s scales, strongly correlated with sprites (Boccippio et al., Science 1995) [1]. Williams (Science 1992) showed resonance parameters track tropical temperature, making SR a candidate global thermometer [1].

### 1.4 How it is measured [ESTABLISHED]

The standard station records two horizontal magnetic components with induction coils — tens to hundreds of thousands of turns on high-permeability cores — plus the vertical electric field via a ball antenna (Ogawa et al., 1966) on a high-impedance amplifier [1, 6, 7]. Signals are tiny: ~1 pT magnetic against Earth's ~30–50 µT static field, ~300 µV/m electric against ~150 V/m fair-weather field [1]. Modern portable receivers reach ~2.9 nV/√Hz input noise and resolve six SR modes in 10 minutes [7]. Public observatories include Tomsk State University's Space Observing System (continuous since 1999 — source of the famous green spectrograms), BGS Eskdalemuir (UK), Cumiana and Etna (Italy), and the HeartMath GCI network [8, 9, 10].

### 1.5 Prehistory [HISTORICAL]

George Francis FitzGerald estimated in 1893 that a conducting layer ~100 km up would give Earth-scale oscillations of ~0.1 s period — leading J. D. Jackson to suggest the name "Schumann–FitzGerald resonances" [1]. Schumann published the full theory in *Zeitschrift für Naturforschung* 7a, 149–154 and 250–252 (1952) and *Nuovo Cimento* 9, 1116–1138 (1952), and attempted measurements with H. L. König in 1952–1954 [1, 11].

---

## Part 2: Measuring an object's full spectrum

### 2.1 The modal worldview [ESTABLISHED]

Any elastic object possesses a countable set of mechanical eigenmodes, each with a resonance frequency, mode shape, and damping ratio fixed by geometry, density, and elastic constants. "The frequency of an object" is therefore a *spectrum*, and measuring it is a solved engineering discipline: experimental modal analysis (EMA).

### 2.2 Chladni plates and cymatics [ESTABLISHED]

Ernst Chladni (1787) bowed sand-sprinkled plates and watched grains migrate to nodal lines — the rest positions of 2-D standing waves. The plate obeys the biharmonic equation D∇⁴w + ρh·∂²w/∂t² = 0, with bending stiffness D = Eh³/12(1−ν²); circular-plate eigenmodes are Bessel patterns [12, 13]. The demonstration prompted Napoleon's prize, won by Sophie Germain (1816). Caveat: driven plates show resonant-frequency shifts and mode-mixing relative to free eigenmodes [13]. Cymatics imagery is legitimate modal physics; mystical overlays are not.

### 2.3 Impulse excitation + FFT modal analysis [ESTABLISHED]

The workhorse method: strike the structure with an instrumented impact hammer (or shaker), record accelerometer response, compute frequency response functions H(f) = S_xy(f)/S_xx(f) from cross- and auto-power spectra [14]. Good practice: averaged impacts, coherence > 0.9, force-exponential windows, PolyMAX parameter extraction, damping from half-power bandwidth; typical plate tests repeat fundamental frequencies within 1.5% [15, 16].

### 2.4 Laser Doppler vibrometry [ESTABLISHED]

Scanning LDVs (Polytec PSV-400 class, DC–20 kHz, µm/s-class resolution) measure surface velocity optically — no accelerometer mass loading — and raster hundreds of points to image full mode shapes: the quantitative successor to Chladni's sand [15, 16].

### 2.5 Resonant ultrasound spectroscopy (RUS) [ESTABLISHED]

RUS suspends a mm-scale specimen between two piezo transducers, sweeps ultrasonic drive, and records a forest of resonance peaks. A Rayleigh–Ritz forward model plus inverse fit recovers the full elastic tensor — up to all 21 constants of a generally anisotropic solid — from one spectrum; non-contact laser variants exist, applied from single crystals to human dentin [17, 18, 19, 20].

### 2.6 Impedance spectroscopy [ESTABLISHED]

The electrical analog: sweep small AC excitation, measure complex impedance/permittivity versus frequency. For the body, bioimpedance analysis measures tissue composition and thoracic fluid dynamics this way [14, 21].

---

## Part 3: The human instrument — what is actually measurable

### 3.1 Electrical: EEG bands [ESTABLISHED]

Scalp EEG (10–100 µV signals) is analyzed in canonical bands: **delta 0.5–4, theta 4–8, alpha 8–13, beta 13–30, gamma 30–100 Hz**, with minor boundary variations between laboratories [22, 23] — the dominant peaks of cortical postsynaptic-current oscillations, and the closest thing to a brain "frequency signature."

### 3.2 Cardiac: ECG, HRV, and mechano-acoustics [ESTABLISHED]

The heartbeat is a ~1–2 Hz fundamental; heart-rate variability analysis resolves autonomic modulation below ~0.4 Hz. Mechanically, ballistocardiography records whole-body recoil of blood ejection at 1–20 Hz (harmonics to ~50 Hz), seismocardiography captures chest-wall vibrations ~0.3–50 Hz, and phonocardiography hears valve acoustics at 20–200 Hz [24, 25, 26].

### 3.3 Voice [ESTABLISHED]

Vocal-fold fundamental F0 spans ~85–180 Hz (adult male) and ~165–255 Hz (adult female); the vocal tract superposes formants F1 ≈ 200–1000 Hz, F2 ≈ 600–3000 Hz, F3 ≈ 1500–3500 Hz — a literal, person-specific resonant-filter signature [27].

### 3.4 Whole-body mechanical resonances [ESTABLISHED]

The seated/standing body vibrated vertically amplifies most in the 4–8 Hz thorax–abdomen band (ISO 2631 sets exposure minima there); horizontal modes resonate at 1–2 Hz [28]. Randall et al. (Ergonomics, 1997; n = 113) measured standing vertical resonance at 9–16 Hz, mean ~12.3 Hz, independent of body mass and height [29].

### 3.5 Biomagnetism: SQUID and OPM [ESTABLISHED]

Cardiac currents produce the body's strongest magnetic field, ~100 pT peak; cortical alpha rhythms give ~10 fT and evoked fields reach ~50–500 fT — against Earth's ~50 µT [30, 31, 32]. SQUID MEG (to ~3 fT/√Hz) inside magnetically shielded rooms maps these fields with millisecond resolution; optically pumped magnetometers (OPMs) now approach similar sensitivity without cryogenics [30, 32, 33].

### 3.6 The Schumann–brain overlap: claim vs. evidence [FRINGE, with ESTABLISHED data points]

It is numerically true that the 7.83 Hz fundamental sits at the theta/alpha boundary. Saroka & Persinger (PLOS ONE, 2016) reported that QEEG spectra from 184 volunteers show transient coherence episodes (~300 ms, roughly twice per minute) with the 7–8, 13–14, and 19–20 Hz bands while a Schumann monitor ran 1 m away [34, 35]. Skeptical analysis: (i) the ambient Schumann field (~1 pT) is far weaker than intrinsic brain fields and below any demonstrated biological detection threshold; (ii) no coupling mechanism has been demonstrated; (iii) Persinger's adjacent weak-field paradigm (the "God helmet") failed its key independent replication (Granqvist et al., 2005); (iv) geomagnetic correlations admit third-factor confounds the authors themselves acknowledge [34, 36, 37]. Marketed claims that the Schumann resonance "heals" or that 7.83 Hz devices entrain the brain are **[FRINGE]**.

---

## Part 4: Tesla's method, then and now

### 4.1 What Tesla actually did [HISTORICAL]

- **Tuned-circuit resonance (1891 onward):** Tesla's core discovery was resonant rise in coupled tuned LC circuits — the Tesla coil, and the "magnifying transmitter" at Colorado Springs (1899), an extra-coil design producing multi-megavolt discharges. Resonance, for Tesla, meant tuning source and receiver to identical frequency so energy accumulates cycle by cycle [38, 39].
- **Colorado Springs, July 3–4, 1899:** monitoring lightning from a storm receding >200 miles, Tesla recorded periodic rise-and-fall of signal strength, noted stationary waves could be produced with an oscillator — "(This is of immense importance)" — and later wrote "No doubt whatever remained: I was observing stationary waves." This is plausibly the first observation of Earth–ionosphere cavity wave phenomena, half a century before Schumann [40, 41].
- **Earth-resonance numbers:** secondary literature variously quotes Tesla's estimates as ~6, 18, 30 Hz (patent-era references), ~8 Hz, and ~10–12 Hz in later writings. All are the right order of magnitude; none was a rigorous modern measurement. Tesla got the *concept* — Earth as a low-frequency resonant conductor — before the instrumentation existed [38, 39, 42, 43].
- **Mechanical resonator:** the steam/compressed-air reciprocating oscillator (US patent 514,169, 1894) was built as an isochronous AC source; the 1898 "earthquake machine" story survives only through Tesla's decades-later retellings (Brooklyn Eagle, July 1935) and O'Neill's 1944 biography. MythBusters (2006) attached a comparable oscillator to a bridge, felt vibrations 100 ft away, and rated the earthquake claim busted. Label the legend [HISTORICAL claim, FRINGE as physics feat]; the underlying resonance principle is [ESTABLISHED] [44, 45].

### 4.2 A Tesla-style modern experiment: the broadband human/object spectrum rig [SPECULATIVE design, ESTABLISHED components]

**Goal:** record a subject's (or object's) complete measurable "frequency signature" — mechanical, acoustic, electric, magnetic — simultaneously, Tesla-fashion: excite, tune, listen.

**Architecture:**
1. **Magnetically/electrically shielded room** (mu-metal MSR; attenuates 50/60 Hz and urban noise that otherwise swamp pT–fT signals) [30, 33].
2. **ELF magnetic channel:** three-axis induction-coil magnetometer (~pT sensitivity), 0.1–100 Hz — captures ambient Schumann background *and* any subject-coupled magnetic signal [7].
3. **Biomagnetic channel:** OPM array (~15–50 fT/√Hz) or, at the high tier, a SQUID dewar (~3 fT/√Hz) over scalp and chest [30, 32].
4. **Electrical channels:** 64-ch EEG (0.5–100 Hz), ECG, 4-electrode bioimpedance sweep (1 kHz–1 MHz) [22, 21].
5. **Mechano-acoustic channels:** piezo force plate for BCG (0.5–50 Hz), chest accelerometer for SCG, studio microphone for voice/heart sounds (20 Hz–20 kHz) [24–27].
6. **Excitation subsystems (the Tesla part):** a calibrated tapping solenoid + vibration exciter for impulse modal analysis (FRF extraction per Part 2.3), and a weak-field ELF coil to test — double-blind — whether externally applied pT–nT fields at 7.83 Hz produce any measurable EEG/HRV effect: the experiment the fringe literature never does properly [14, 34].
7. **Analysis:** synchronized 24-bit DAQ, FFT/Welch PSD, cross-channel coherence, FRF modal extraction.

**Budget tiers and expected SNR:**

| Tier | Cost | Magnetometry | Shielding | What you can resolve |
|---|---|---|---|---|
| Garage | ~$2–5k | Induction coil DIY (~pT–nT) | none; measure at rural site | Schumann modes in spectra (coil at quiet site), EEG alpha, BCG, voice |
| University | ~$50–150k | 3-axis OPM (~50 fT/√Hz) | 2-layer mu-metal booth | MCG (~100 pT) robustly; alpha MEG bursts with averaging; full modal FRFs |
| Flagship | ~$1–2M+ | 300-ch SQUID MEG (~3 fT/√Hz) | MSR (multi-layer, active compensation) | full MEG/MCG, evoked fT fields, coincident SR–EEG coherence tests |

SNR reality check: heart MCG (~100 pT) vs urban magnetic noise (~nT–µT) needs ~40–80 dB shielding plus gradiometry — achievable; brain alpha (~10 fT) needs MSR + SQUID/OPM and signal averaging [30, 32, 33]. A definitive double-blind test of 7.83 Hz external-field effects on EEG/HRV is feasible at the University tier; its expected-null result would itself be publishable [34, 36].

---

## Part 5: Frequency atlas — characteristic frequencies across scales

| Phenomenon | Frequency / wavelength | How measured | Status |
|---|---|---|---|
| Earth free oscillation ₀S₂ ("breathing" mode after great earthquakes) | 0.309 mHz (period ~53.9 min) | superconducting gravimeters, broadband seismographs | [ESTABLISHED] |
| Earth normal-mode band | 0.3–7 mHz | global seismograph networks | [ESTABLISHED] |
| Skyscraper sway (Taipei 101 fundamental) | ~0.15 Hz | in-building accelerometer arrays, GNSS | [ESTABLISHED] |
| Building rule-of-thumb period T ≈ 0.1·N s (N = stories) | ~0.17–10 Hz | code formulae, modal testing | [ESTABLISHED] |
| Human lateral whole-body mode (head–neck) | 1–2 Hz | vibration platforms, ISO 2631 | [ESTABLISHED] |
| Heartbeat fundamental | ~1–2 Hz | ECG, BCG | [ESTABLISHED] |
| Human vertical whole-body resonance (thorax–abdomen, seated) | 4–8 Hz amplification band; standing 9–16 Hz | vibration tables; ISO 2631 weightings | [ESTABLISHED] |
| Schumann resonances | 7.83, 14.3, 20.8, 27.3, 33.8 Hz (λ ≈ 38,000 km fundamental) | ELF induction coils + ball antenna | [ESTABLISHED] |
| EEG bands | delta 0.5–4 / theta 4–8 / alpha 8–13 / beta 13–30 / gamma 30–100 Hz | scalp electrodes; MEG (SQUID/OPM, fT range) | [ESTABLISHED] |
| BCG / SCG mechanical cardiac signature | 1–20 Hz (BCG), 0.3–50 Hz (SCG) | piezo platform, chest accelerometer | [ESTABLISHED] |
| Heart sounds (PCG) | 20–200 Hz | stethoscope/microphone | [ESTABLISHED] |
| Voice fundamental F0 | 85–180 Hz (M), 165–255 Hz (F) | microphone, pitch tracking | [ESTABLISHED] |
| Voice formants F1–F3 | ~200–3,500 Hz | spectrography | [ESTABLISHED] |
| Metal bar / plate eigenmodes (lab scale) | ~0.5–20 kHz | impact hammer + FFT, scanning LDV | [ESTABLISHED] |
| Quartz watch tuning fork | exactly 32.768 kHz = 2¹⁵ Hz | frequency counter; chosen for binary division to 1 Hz | [ESTABLISHED] |
| RUS specimen modes (mm-scale crystals) | ~0.1–2 MHz | piezo transducers + Rayleigh–Ritz inversion | [ESTABLISHED] |
| Molecular vibrations (IR-active bonds) | ~3–100 THz (IR, λ ~3–100 µm) | FTIR / Raman spectroscopy | [ESTABLISHED] |

---

## Source list (only URLs actually retrieved during this research)


1. [Schumann resonances — Wikipedia](https://en.wikipedia.org/wiki/Schumann_resonances)
2. [Observation of Schumann Resonances in the Earth's Cavity (NASA NTRS)](https://ntrs.nasa.gov/api/citations/20120000051/downloads/20120000051.pdf)
3. [ELF Electromagnetic Signals as Possible Seismic Precursors — MDPI Atmosphere](https://www.mdpi.com/2073-4433/15/4/457)
4. [Analysis of the Sierra Nevada ELF station recordings — UGR](https://digibug.ugr.es/bitstream/handle/10481/80703/74119(1).pdf?sequence=4&isAllowed=y)
5. [Nickolaenko & Hayakawa, Schumann Resonance for Tyros (book PDF)](http://ndl.ethernet.edu.et/bitstream/123456789/69705/1/2014_Book_SchumannResonanceForTyros.pdf)
6. [ELF Electromagnetic Waves from Lightning: The Schumann Resonances (Semantic Scholar PDF)](https://pdfs.semanticscholar.org/765e/0527e9d0f264efb1fd530cf5fe79b191f692.pdf)
7. [A new portable ELF Schumann resonance receiver — EURASIP JWCN](https://jwcn-eurasipjournals.springeropen.com/counter/pdf/10.1186/s13638-018-1157-7.pdf)
8. [Where Schumann Resonance Data Comes From: Tomsk, NOAA & GFZ — ResonanceOne](https://resonanceone.app/blog/tomsk-observatory-data)
9. [BGS Geomagnetism — High-frequency magnetometers / induction coils](https://geomag.bgs.ac.uk/research/inductioncoils.html)
10. [About SunGeo — monitoring network](https://sungeo.net/about)
11. [Magnetfeld-Anregung, Biosensor (F. Balck)](http://www.biosensor-physik.de/biosensor/magnetfeld-anregung.htm)
12. [Dust removal on solar panels using Chladni patterns — Nature Scientific Reports](https://www.nature.com/articles/s41598-025-86363-7.pdf)
13. [Exploration of Resonant Modes for Circular and Polygonal Chladni Plates — PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10969725/)
14. [Variable-Impulse Hammer Impact Test (VIHIT) — PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC13165932/)
15. [Impact hammer + scanning LDV modal testing (ISO 7626-2) — RME journal](http://rme-journal.org/index.php/asd/article/download/534/135)
16. [Modal Analysis using Multi-reference and MIMO Techniques — Brüel & Kjær](https://www.bksv.com/-/media/literature/Application-Note/bo0505.ashx)
17. [Resonant Ultrasound Spectroscopy: Asymptotic Behavior of Resonant Frequencies — arXiv](https://arxiv.org/pdf/2307.16095)
18. [Determination of All 21 Independent Elastic Coefficients … by RUS — ResearchGate](https://www.researchgate.net/publication/271866618_Determination_of_All_21_Independent_Elastic_Coefficients_of_Generally_Anisotropic_Solids_by_Resonant_Ultrasound_Spectroscopy_Benchmark_Examples)
19. [Resonant ultrasound spectroscopy — Wikipedia](https://en.wikipedia.org/wiki/Resonant_ultrasound_spectroscopy)
20. [Resonant ultrasound spectroscopy review — TRACE Tennessee](https://trace.tennessee.edu/server/api/core/bitstreams/e283dbcf-dd21-42a7-9306-a323bf416e7d/content)
21. [Measurement, Instrumentation, and Sensors Handbook (biomagnetism chapter)](https://lib.zu.edu.pk/ebookdata/Engineering/Biomedical%20Engineering/Measurement,%20Instrumentation,%20and%20Sensors%20Handbook_%20Electromagnetic,%20Optical,%20Radiation,%20Chemical,%20and%20Biomedical%20Measurement%20edited%20by%20John%20G.%20Webster%20&%20Halit%20Eren.pdf)
22. [Review of EEG signal approaches — PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC9749579/)
23. [Neural Correlates of BPD Based on EEG — PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12428447/)
24. [Ballistocardiography — Simon Fraser University](https://www.sfu.ca/aerospacelab/research-areas/cardiology/ballistocardiography.html)
25. [Ballistocardiography (BCG fundamentals) — J-Stage MEJ](https://www.jstage.jst.go.jp/article/mej/12/3/12_24-00438/_pdf)
26. [Cardiac Multi-Frequency Vibration Signal Sensor — PMC](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11014338/)
27. [What Frequency Is Speech? The Science of the Human Voice — Biology Insights](https://biologyinsights.com/what-frequency-is-speech-the-science-of-the-human-voice/)
28. [Whole Body Vibration overview — ScienceDirect Topics](https://www.sciencedirect.com/topics/biochemistry-genetics-and-molecular-biology/whole-body-vibration)
29. [Resonant frequencies of standing humans (Randall et al., 1997) — PubMed](https://pubmed.ncbi.nlm.nih.gov/9306739/)
30. [The Heart's Electromagnetic Field … — PMC (Palantzas 2026)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12986840/)
31. [Biomagnetic measurements application note — TOPTICA](https://www.toptica.com/literature/application_notes/application-note_TOPTICA_Biomagnetic-measurements-benefit-from-laser-know-how_en.pdf)
32. [SQUIDs in Neuro- and Cardiomagnetism — UNESCO EOLSS](https://www.eolss.net/Sample-Chapters/C05/E6-08-05-02.pdf)
33. [What is MEG? — ASFNR](https://www.asfnr.org/what-is-meg)
34. [Similar Spectral Power Densities Within the Schumann Resonance and … QEEG Profiles — PLOS ONE](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0146595)
35. [Quantitative Similarities Between Schumann and Cerebral Activity (Saroka & Persinger) — ICM](https://yadda.icm.edu.pl/baztech/element/bwmeta1.element.baztech-5c33c1e5-853d-421c-b368-28f8b076240b/c/ILCPA-202-2014-166-194.pdf)
36. [Michael Persinger (controversies/replication) — Grokipedia](https://grokipedia.com/page/Michael_Persinger)
37. [What Is 7.83 Hz? — ResonanceOne](https://resonanceone.app/blog/what-is-7-83-hz)
38. [Nikola Tesla — WikiSlice (Colorado Springs)](http://rachel.education.gov.ck/olpc/wikislice-en/files/articles/Nikola_Tesla.htm)
39. [Implications of Tesla's Inventions … — ResearchGate](https://www.researchgate.net/publication/233904397_Implications_of_Tesla's_Inventions_and_His_Moral_Character_on_the_Development_of_Contemporary_Science_and_Technology)
40. [1994 Tesla Symposium: Nikola Tesla, Lightning Observations, and Stationary Waves (Corum & Corum)](https://rexresearch1.com/TeslaLibrary/CorumTeslaLightning.pdf)
41. [Project Tesla — Demonstration of Artificially Stimulated Resonance … — Scribd](https://www.scribd.com/document/124376593/Project-Tesla-The-Demonstration-of-Artificially-Stimulated-Resonance-of-the-Earth-s-Ionosphere-Waveguide)
42. [Nikola Tesla's Resonance Theories and the Schumann Resonance — L. A. Morales](https://www.laloadrianmorales.com/blog/nikola-teslas-resonance-theories-and-the-schumann-resonance-an-in-depth-review/)
43. [Nikola Tesla biography (Romanian) — IBN/IDSI](https://ibn.idsi.md/sites/default/files/imag_file/Nikola%20Tesla%20cel%20mai%20misterios%20om%20de%20stiinta%20al%20secolului%20XX.pdf)
44. [Tesla's oscillator — Wikipedia](https://en.wikipedia.org/wiki/Tesla%27s_oscillator)
45. [032 – The Earthquake Machine (1896–1898) — Tesla Podcast](http://teslapodcast.com/2022/12/08/032-the-earthquake-machine-1896-1898/)
46. [High-Precision Detection of Earth's Free Oscillation Signals — PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12846067/) and [Low-Frequency Seismology (IRIS/Ishii)](https://www.iris.edu/hq/instrumentation_meeting/files/presentations/ishii.pdf) and [geo-prose IRIS sensor workshop PDF](https://geo-prose.com/pdfs/iris_sensor_ws.pdf)
47. [Vibrations of the TAIPEI 101 skyscraper caused by the 2011 Tohoku earthquake — Springer EPS](https://link.springer.com/article/10.5047/eps.2012.04.004)
48. [Dynamic Deformation Analysis of Super High-Rise Buildings (GNSS) — PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12074224/)
49. [NYC Hazard Mitigation — earthquakes / building spectral acceleration](https://nychazardmitigation.com/documentation/hazard-profiles/earthquakes/)
50. [Crystal vs Oscillator — Wevolver](https://www.wevolver.com/article/crystal-vs-oscillator-choosing-the-right-timing-component)
51. [Seismocardiography signal bandwidth — PMC cardiorespiratory review](https://pmc.ncbi.nlm.nih.gov/articles/PMC9737480/)

*Numerical derivation of the ideal Schumann series was performed independently (c = 299,792,458 m/s; a = 6,371 km): c/2πa = 7.4892 Hz; f₁…f₆ = 10.59, 18.34, 25.94, 33.49, 41.02, 48.53 Hz; observed/ideal ratios 0.74–0.82 — cross-checked against sources 1–5.*
