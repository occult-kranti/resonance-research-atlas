# V4 release wording and consistency audit

Reviewer: `/root/release_review`, 27 September 2026. This is an independent model-agent release audit, not human peer review or an additional research loop. No frozen contract, producer output, manifest or numerical review was changed.

## Finding

No blocking scientific wording defect was found in the stable field-notes interface, continuation scope, apparatus documentation, setup catalog or companion-page generator. The public interpretation remains within the narrow R3–R5 model findings. This audit does not verify a physical device or deployment.

| Boundary examined | Evidence and conclusion |
|---|---|
| Simulation versus observation | `field-notes.html/js` marks the calculators as analytical or synthetic, setup cards as proposed physical comparisons, generated art as illustration, and ledger figures as computational evidence. `continuation-v4.md` and the companion generator explicitly withhold physical results and distinguish model agents from human reviewers. |
| R3 source-off circuit | The admitted R3 review and ledger scope define source off as zero ideal source voltage with the series loop still closed. `apparatus.md` states this explicitly and distinguishes synchronized waveform acquisition from slow-meter readings. The UI calculator separately declares sinusoidal steady state; it does not present its cycle as the transient R3 run. |
| R4 electrical boundary | The producer report distinguishes maintained current and source work from the auxiliary lossless fixed-flux boundary. The release documentation consistently uses the maintained-current model when stating the 40 µJ field increase and 40 µJ mechanical work. The supplied trajectory and inductance are not presented as measured geometry or solved free dynamics. |
| Apparatus versus abstract model | `apparatus.md` and `setup-catalog.json` explicitly separate the qualitative permanent-magnet/steel balance control from R4's stipulated variable-inductance calculation. The external support carries the reaction; static contact, scale interference and ordinary-force controls remain requirements. No force detectability is inferred from the proposed 8 cm gap. |
| R5 gravity identification | The admitted review and report say that a deliberately injected common acceleration change is recovered only under the stipulated two-parameter model. An ordinary mass-proportional bias reproduces all individual readings; unknown bias withholds a physical gravity interval. The interface renders scope and limits from the actual decision ledger, and the companion generator includes those limits. |
| R5 numerical repair | The repaired result, repair log and review retain the theoretical ±0.00032 m/s² bound and separately report 10⁻¹² m/s² outward numerical padding. They preserve the original failed endpoint and do not call the finite-fixture guard a universal floating-point enclosure, confidence interval or measured sensitivity. |

The RLC calculator's stated default mean source/load/internal powers (0.100/0.080/0.020 W) and capacitor transfer gain (2) are consistent with its stated steady-state parameters. Its stored-energy and signed-power expressions use the same passive series-circuit convention.

## Scope of inspection

Read the R3, R4 and repaired R5 `results.json`, their admitted `reviews/R*-review.json`, R4/R5 reports, the R5 repair log, the available decision-ledger entries, `sound-lab/field-notes.html`, `sound-lab/field-notes.js`, `docs/continuation-v4.md`, `docs/panel-v4/apparatus.md`, `docs/panel-v4/setup-catalog.json`, and `scripts/render_vessels_continuation.py`.

The separate release gate must still establish a complete ten-loop ledger, current artifact hashes, successful builds and live deployment. The companion generator already refuses to render before all five narrow admissions exist. This wording audit supplies none of those execution or deployment claims and adds no sixth research round.
