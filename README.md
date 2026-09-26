# Resonance Research Atlas

A source-led research workbench joining OpenSync, Resonant Vessels, the Newton/Tesla alchemy archive and historical astronomy/astrology tools. It studies extraordinary claims through explicit models, controls and competing interpretations.

The first release corrects source/inference errors in the early Resonant Vessels draft, preserves both audio apps in `brainwave_opensync`, and records six adaptive computational panel rounds. Named historical figures are research lenses. The panel consists of model agents, not the historical people or human peer reviewers.

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
- `docs/`: audit, roadmap, reproducibility and source-reading records.
- `archive/newton-tesla-alchemy`: user-requested original dossiers with their original statuses. Check the correction log before treating their claims as verified.
- `integrations/manifest.json`: immutable source revisions and role of each project.
- `scripts/build_site.py`: composes pinned public exhibits and adds return navigation.
- `assets/lab-concept.png`: generated concept illustration; not an engineering or medical schematic. Scientific diagrams and plotted results are separate.

## Publication

Verified live integrated destination: https://occult-kranti.github.io/brainwave_opensync/research/ . See [the release record](docs/live-release.md) for deployed revisions and checks.

Requested standalone repository: `occult-kranti/resonance-research-atlas`. The connected GitHub plugin can update existing repositories but exposes no repository-creation or Pages-administration action. Standalone creation is tracked separately; it must not be reported as published until the remote exists and the site is verified.

For the complete six-loop and parallel follow-on map, read [docs/roadmap.md](docs/roadmap.md). For the final dream session, open the site’s **Dreams & perception** view and the Round 6 contract.

## Scope and provenance

This is a selected source review, not a claim to have read all occult books, patents, government files or current physics. Patents are proposals, government custody is provenance, and fringe discussions are discourse leads. Source records name passages actually read and unresolved checks. Synthetic tests validate their declared mathematics, not the existence of metaphysical powers. Historical toxic processes are interpreted without operational recipes.

New authored code: MIT. Imported works retain their original attribution and licenses. Source archive material is reused at the repository owner's request; third-party linked publications remain at their original hosts.
