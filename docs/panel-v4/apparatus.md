# Proposed apparatus and energy boundaries

The active focus is now electricity, magnetism and tests that distinguish ordinary force from a hypothetical gravity change. Earlier sound arrangements remain available as a retained checkpoint. A deterministic drawing, a generated concept image and an executed numerical result have different evidence status throughout.

## Electrical model and measurement locations

`assets/sound-lab-v4/electrical-energy-boundary.svg` follows the **frozen electrical R3** topology: isolated source, a single series current, 1 Ω internal resistance, 10 mH inductance, 100 µF capacitance and 4 Ω load. The source is a 1 V peak sine at 1000 rad/s (159.155 Hz), on for ten cycles and off for five. Here “off” means **zero ideal source voltage while the series circuit remains closed**, not opening a switch or disconnecting a real generator. These are model values, not a component-kit recommendation or a measured circuit. The zero-voltage, initially charged capacitor control distinguishes stored energy release from source gain.

The current reference direction leaves the source's positive terminal and enters the positive terminal of every passive component. Voltage probes connect across the source, across the capacitor's two terminals, and across the load resistor. In particular, the capacitor observation is **differential**, not implicitly referenced to the source return. A synchronized waveform recorder of known bandwidth must record `v_s(t)`, `i(t)`, `v_C(t)` and `v_load(t)` together to assess transient energy. The circles in the drawing are observation locations, not a claim that ordinary slow multimeter readings determine instantaneous power. Real probe input resistance, burden, wiring loss, calibration, timing and parasitic components require their own budget.

The source boundary is defined at the plotted terminal pair:

\[
\int v_s i\,dt
=\int R_{\mathrm{load}}i^2\,dt
+\int R_{\mathrm{internal}}i^2\,dt
+\Delta\left(\tfrac12Li^2+\tfrac12Cv_C^2\right).
\]

Here the passive-boundary source work is distinct from power consumed inside an actual generator. An inductor can store magnetic energy and a capacitor can have voltage gain without the completed budget showing net energy generation. Any physical pilot must use isolated ordinary low voltage and components with characterized ratings; this artifact supplies no high-voltage implementation.

## Magnetic force and whole-apparatus interpretation

`assets/sound-lab-v4/magnetic-work-boundary.svg` follows **R4's stipulated variable-inductance model**, `L(z)=0.01+0.1z H` with `z` in metres, current `I=0.2 A` and resistance `R=5 Ω`. The trajectory from 0 to 0.02 m is prescribed over 0.2 s; the simulation does not solve a freely levitating object's motion. The model gives `F = ½I² dL/dz = 2 mN`, and maintaining current requires the source to supply `v = RI + I(dL/dz) dz/dt`. The 40 µJ increase in magnetic storage and 40 µJ of mechanical work both enter the electrical-source budget. Those are analytic consequences of the stipulated model, not magnet measurements. A separate 1 g static test-mass calculation keeps `g = 9.80665 m/s²` fixed and yields support `N = 7.80665 mN` when a 2 mN upward magnetic force is present.

`assets/sound-lab-v4/magnetic-force-plan.svg` and `assets/sound-lab-v4/magnetic-force-3d.png` instead show a **qualitative permanent-magnet contact-force control**. They are not a quantitative apparatus realization of the R4 solenoid law. A small fixed magnet is held above a steel test piece that stays on a balance pan. The magnet's feet and support are off the balance. The opposite force on the magnet is carried through that external support to the table. If the entire interacting magnet/support/test-piece assembly were placed on the same balance, internal forces would cancel in the whole-system static force sum; this illustrated split-support arrangement intentionally does not put the whole system on the pan.

| Proposed magnetic coordinate or dimension | Value |
|---|---|
| Table plane | `z = 0`; 1.00 × 0.65 m outline |
| Test-piece centre | (0.36, 0.30, 0.074) m |
| Test-piece bottom / top | 0.070 / 0.078 m |
| Magnet centre | (0.36, 0.30, 0.161) m |
| Magnet bottom / top | 0.158 / 0.164 m |
| Magnet-to-test-piece air gap | 0.080 m = 8 cm |
| Both drawn radii | 0.015 m, generic geometric proxies |
| Balance pan top | 0.070 m |
| Magnet-support footprint origin / size | (0.645, 0.225, 0) m / (0.13, 0.15, 0.015) m |

No force detectability is inferred from these arbitrary proposed dimensions, and no magnet strength or material property was measured. The figure includes a ruler, levelling support and manual logbook. It does not show a numerical balance reading. Record baseline, fixed magnet position, and return-to-baseline observations, preserving every reading. Check field effects on the balance body, nearby magnetic parts, source support motion and drift separately. Common-table vibration is still possible despite separate feet. Characterized magnet-absent and nonmagnetic controls are required before assigning a change to the test object. A test-piece reading alone is not a direct measurement of gravity.

The contact equation `N = mg − F_m` is valid for the illustrated static force directions while `N ≥ 0` and with the stator or source-magnet reaction supported off the balance. It does not establish a levitation equilibrium or an antigravity mechanism. A direct balance bias could imitate a change in this apparent support force. A separate whole-system and nuisance-identification model determines what further observations would be needed; no such physical discrimination was performed here.

Reproduce these electromagnetic figures with `python scripts/render_electromagnetic_v4.py`. It exports `assets/sound-lab-v4/electromagnetic-coordinates.json` and `electromagnetic-manifest.json`, verifies the 8 cm gap and parses the SVG files. It reuses geometric surface helpers but does not regenerate, rename or modify the earlier sound assets or their manifest. All source, artwork and coordinate files are linked through `docs/panel-v4/setup-catalog.json`.

`assets/sound-lab-v4/magnetic-balance-concept.png` is separate generated ImageGen concept art. Its exact prompt/provenance is in `docs/panel-v4/magnetic-concept-provenance.json`. The generic scale housing and pan in that image are not specifications of magnetic neutrality, and the concept does not substitute for balance-interference controls. It is proposed, unbuilt, not to scale and not a photograph of a performed test.

## Retained sound bench: two ways to observe the same limitation

These are complete proposed arrangements, not photographs of equipment that was built. No physical measurements were made. The drawings prioritize available household materials and provide reproducible placements for a future pilot; the dimensions are neither acoustically optimized nor calibration standards. The advisor accepted them as proposed construction coordinates after reading the R1 contract.

## Deliverables

All image paths below are relative to the repository root.

| Arrangement | Dimensioned top view | Deterministic 3D view | Interpretation |
|---|---|---|---|
| A: two phones | `assets/sound-lab-v4/phone-witness-plan.svg` | `assets/sound-lab-v4/phone-witness-3d.png` | One recording phone captures the mixture; another supplies a pilot from its built-in speaker. Mono separation has not been established by the R1 fixtures. |
| B: optional two-input recorder | `assets/sound-lab-v4/dual-channel-plan.svg` | `assets/sound-lab-v4/dual-channel-3d.png` | A sample microphone and a source-monitor microphone feed two inputs on the same recorder. Shared sampling time does not demonstrate shared gain. |

Reproduction source: `scripts/render_apparatus_v4.py`. Coordinate data: `assets/sound-lab-v4/apparatus-coordinates.json`. Generator and artifact hashes: `assets/sound-lab-v4/apparatus-manifest.json`.

The SVG plans are accurate orthographic projections of the declared coordinates. Their dimensions are in **centimetres**. The 3D axes and JSON coordinates are in **metres**. Perspective changes apparent lengths in the PNGs; use the SVGs for placement. The 3D bowl is a numerically generated, hollow surface of revolution. Devices and supports are generic geometric proxies, not engineering drawings for a particular product. Their exact wall thicknesses and housings do not enter an acoustic simulation.

## Coordinates and complete parts

The origin is at a tabletop corner; `z = 0` is the top surface. The tabletop is 1.00 m wide and 0.70 m deep.

| Point or dimension | Declared value |
|---|---|
| Bowl rim centre | (0.32, 0.26, 0.08) m |
| Sample microphone port | (0.59, 0.26, 0.08) m |
| Pilot emitting port | (0.59, 0.61, 0.08) m |
| Optional source-monitor capsule | (0.59, 0.53, 0.08) m |
| Bowl outer diameter / height | 0.14 m / 0.07 m |
| Bowl soft-support thickness | 0.01 m |
| Nearest bowl rim to sample microphone | 0.20 m = 20 cm |
| Pilot port to sample microphone | 0.35 m = 35 cm |
| Pilot port to optional monitor | 0.08 m = 8 cm |

A needs an intact metal bowl, a soft support such as folded cloth or cork, a pencil eraser, a phone that exports recordings, a second phone capable of playing a steady pilot, stable supports and a marked ruler. Locate each actual microphone and speaker opening before placing it: phones differ. The blocks in the drawings stand for a stable cradle or stack; they must not cover the ports. A separate available speaker/player can replace the pilot phone, but no new speaker purchase is required. The bowl is empty. No historical chemical preparation is part of this bench.

B replaces the recording phone with two ordinary microphones, low supports, two analogue cables and a two-input recorder. It is optional. Each channel remains a mixture of its source, room, sensor and recorder path. The nearby source microphone is a witness to change, not an isolated or calibrated reference. The same clock makes within-record timing possible; it does not establish that the two channels have identical automatic gain, sensitivity, compression or phase response.

Soft supports hold positions and reduce direct table contact; they do not guarantee acoustic or mechanical isolation. Changing them changes boundary conditions and belongs in the acquisition log. Dashed connectors indicate acoustic signal routes, not computed rays, pressure fields, propagation delays or energy flux. Solid connectors in B represent cables. Neither picture contains measured waveforms.

## What R1 permits

The frozen model in `docs/panel-v4/contracts/R1.json` uses ideally separated channels. For target log-envelope slope `m_s = beta_s - alpha` and reference slope `m_r = beta_r - alpha_r`, the proposed estimator is

\[
\widehat{\alpha}=m_r-m_s
=\alpha+(\beta_r-\beta_s)-\alpha_r.
\]

It returns `alpha` only under a stable reference (`alpha_r = 0`) and common gain drift (`beta_s = beta_r`), within the declared observation model. A second microphone does not itself establish either premise. The two diagrams therefore show candidate measurements needed to challenge those premises, not apparatus that automatically recovers intrinsic material damping. R1's generated stereo data are not recordings from either proposed assembly.

A first physical pilot can record source-only, tap-only and simultaneous source-plus-tap conditions at the same marked positions, preserving all files and settings. These controls ask whether the pilot is stable enough to track, whether relevant bands are separable, whether either input clips, and whether processing changes with the presence of the tap. A local frequency selected from a separate pilot would still need its own frozen analysis window, mode definition, noise checks and separation validation. Do not assume a real bowl resonates at the synthetic fixture's 500 Hz or use the fixture's 1000 Hz reference without checking overlap.

Keep ordinary listening volume low and stop if uncomfortable. Gain-control and noise-suppression settings, exported sample rate, source volume, support geometry and all actual distances belong in the log. Record the microphone opening rather than the centre of a phone. A changed pilot can result from source drift, propagation or recorder processing. A stable pilot does not certify that every other frequency band has stable gain. The earlier `research/sound-lab-v3/protocol.md` retains the raw-file, pre-roll, impact-time and repeat requirements.

## Generated concept image

`assets/sound-lab-v4/tabletop-concept.png` is a separate built-in ImageGen illustration supplied by the root agent. The prompt describes a tabletop bowl, soft tapper, recording phone, playback device and speaker on supports, with no measured waveforms or invisible effects. The full generation prompt/provenance is maintained separately by the root agent. This asset is **generated concept art, not a photograph, not to scale and not the experiment specification**. Its optional separate speaker/player can be replaced by a phone's built-in speaker as shown in the least-material plan. The deterministic generator neither reads nor modifies the concept image.

Suggested concept caption: “Generated illustration of possible components. Proposed and unbuilt; component dimensions, cable details and placement are not a measurement. Use the dimensioned plans; a separate loudspeaker is optional.”

## Reproduction and checks

```sh
python scripts/render_apparatus_v4.py
```

The generator uses Python, NumPy and Matplotlib; the run here used NumPy 2.3.5 and Matplotlib 3.10.8. It computes the three labelled separations directly from the common metre coordinates before rendering, writes both SVGs and PNGs, exports coordinate data and records SHA-256 hashes. SVG XML parsing, figure dimensions, hash agreement and visual inspection of both layouts were performed. The rendering initially exposed a Matplotlib collection-depth artefact hiding equipment behind its support; the final renderer uses a common surface collection with subdivided solid faces so equipment remains visible. This was a drawing repair, not a physical or numerical experiment result.

SVGs contain accessibility titles and descriptions. All four figures carry their proposal/no-measurement status and their units. Neither arrangement was tested on hardware. No calibration, participant observation, material identification or unusual physical effect is claimed.
