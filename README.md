# Resonance Research Atlas

A source-led research workbench joining OpenSync, Resonant Vessels, the Newton/Tesla alchemy archive and historical astronomy/astrology tools. It studies extraordinary claims through explicit models, controls and competing interpretations.

The latest [Electricity & force bench](https://occult-kranti.github.io/resonance-research-atlas/sound-lab/field-notes.html) follows the user-directed shift to **electricity, magnetism and antigravity claims**. It retains two reviewed sound checkpoint rounds and continues with electrical and magnetic-force models. Open the [V4 scope and provenance](docs/continuation-v4.md), [adaptive roadmap](docs/panel-v4/roadmap-v4.md) and [decision ledger](research/panel-v4-decisions.json). Proposed apparatus, simulations and physical measurements have separate statuses.

The first release corrects source/inference errors in the early Resonant Vessels draft, preserves both audio apps in `brainwave_opensync`, and records six adaptive computational panel rounds. Named historical figures are research lenses. The panel consists of model agents, not the historical people or human peer reviewers.

The nanoparticle extension adds five sequential research rounds, magnetic and thermal calculators, current metrology sources, six historical experiment proposals and an OpenSync audible calibration bench. See [the nanoparticle roadmap](docs/nanoparticle-roadmap.md) and [round decisions](research/nanoparticle-panel-decisions.json).

The [Sound & observation lab](https://occult-kranti.github.io/resonance-research-atlas/sound-lab/) adds a separate continuation: three planning panels, five sound rounds with two review loops each, and three conditional Bashar/AI-consciousness investigations. Its [decision ledger](research/panel-v3-decisions.json) records actual execution and acceptance; the [continuation guide](docs/continuation-v3.md) defines scope. Start with the proposed speaker/phone or gentle-tap protocol, inspect a local WAV/CSV in the browser, then use the protected Python intake for a declared decay fit. No recording is uploaded by the browser screen.

## Use

Start with the source ledger, open an experiment's model and controls, then inspect its reproducible result. The evidence graph records relations (documents, inspires, tests), not proof by association. A person's EEG, ECG, movement, voice and magnetic signals are different measurements; this site does not produce a universal human frequency or establish a healing effect.

## Run locally

```bash
npm ci
npm test
python3 scripts/build_site.py --output dist
python3 -m http.server 8000 --directory dist
```

Open http://localhost:8000/. The build fetches the exact public commits in `integrations/manifest.json` and never executes imported repository code. For existing local checkouts, add `--source-root /absolute/path/to/repos`. `--skip-projects` is an authored-pages preview; imported project links require the full assembly.

## Structure

- `data/research.json`: experiments, source ledger, panel decisions, roadmap and typed evidence graph.
- `research/round1` through `round6`: frozen contracts, derivations, executable models, tests and raw outputs.
- `research/nanoparticles/round1` through `round5`: the additional adaptive program, kept separate from the original six.
- `sound-lab/`: responsive experiment workflow, synthetic calculators, local recording screen, source dictionary and reviewed loop views.
- `sound-lab/field-notes.html`: the electricity/magnetism/force-claim continuation and preserved sound checkpoint.
- `research/sound-lab-v4/`: V4 computational records; the directory retains its original name after the domain pivot. `parked-sound-R3` is exploratory and unadmitted.
- `docs/panel-v4/` and `assets/sound-lab-v4/`: updated sources, derivations, hypotheses, roadmap and proposed apparatus geometry.
- `research/sound-lab-v3/`: ten sound/metrology loops, raw fixtures, protected recording intake, scientific plots and practical protocols.
- `research/consciousness-v3/`: three conditional information/reporting audits and a proposed human/AI study protocol.
- `docs/panel-v3/`: planning exchanges, source reading records, independent reviews, alchemy dictionary and apparatus catalog.
- `assets/sound-lab-v3/`: dimensioned SVGs, reproducible 3D geometry and a separately labeled generated concept.
- `docs/`: audit, roadmap, reproducibility and source-reading records.
- `archive/newton-tesla-alchemy`: user-requested original dossiers with their original statuses. Check the correction log before treating their claims as verified.
- `integrations/manifest.json`: immutable source revisions and role of each project.
- `scripts/build_site.py`: composes pinned public exhibits and adds return navigation.
- `assets/lab-concept.png`: generated concept illustration; not an engineering or medical schematic. Scientific diagrams and plotted results are separate.

## Publication

Verified live integrated destination: https://occult-kranti.github.io/brainwave_opensync/research/ . See [the release record](docs/live-release.md) for deployed revisions and checks.

Standalone atlas: https://occult-kranti.github.io/resonance-research-atlas/ . Source repository: https://github.com/occult-kranti/resonance-research-atlas . GitHub Pages is configured to publish through the included Actions workflow.

Audible signal bench: https://occult-kranti.github.io/brainwave_opensync/nano-lab/ . It exports generated samples and measurement manifests; it does not infer a real nanoparticle response.

The continuation is also integrated at https://occult-kranti.github.io/brainwave_opensync/research/sound-lab/ . It links to NanoLab for signal generation and Recording analysis for existing audio tools. The old six-session and nanoparticle exhibits remain unchanged.

## Reproduce the sound continuation

```bash
python3 -m pip install -r requirements-research.txt
python3 research/sound-lab-v3/verify.py
python3 scripts/verify_continuation.py
```

The complete-release gate requires all thirteen reviewed loop records in order and checks their artifact hashes. For actual file analysis, follow [the sound protocol](research/sound-lab-v3/protocol.md) and use `intake_v2.py`; the earlier `fit_recording.py` is retained as an immutable reproduction dependency. Input provenance is supplied by the caller and is not authenticated by the analysis software. Hardware measurements are proposed, not reported as completed.

For the complete six-loop and parallel follow-on map, read [docs/roadmap.md](docs/roadmap.md). For the final dream session, open the site’s **Dreams & perception** view and the Round 6 contract.

## Reproduce the electricity / force continuation

```bash
python3 -m pip install -r research/sound-lab-v4/requirements.txt
python3 research/sound-lab-v4/verify.py --regenerate
python3 scripts/verify_field_notes.py
npm test
```

The first command after installation regenerates admitted producer artifacts in a temporary copy and checks their hashes. Independent reviewer scripts and results live in `research/sound-lab-v4/reviews/`; the release gate checks exact admitted bytes and ordered contract/review dependencies. The parked sound R3 is preserved but excluded from the five-round count. This verifies computational work, not an operated physical apparatus.

## Scope and provenance

This is a selected source review, not a claim to have read all occult books, patents, government files or current physics. Patents are proposals, government custody is provenance, and fringe discussions are discourse leads. Source records name passages actually read and unresolved checks. Synthetic tests validate their declared mathematics, not the existence of metaphysical powers. Historical toxic processes are interpreted without operational recipes.

New authored code: MIT. Imported works retain their original attribution and licenses. Source archive material is reused at the repository owner's request; third-party linked publications remain at their original hosts.
