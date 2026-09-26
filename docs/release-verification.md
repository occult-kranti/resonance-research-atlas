# Release verification record

## Reproducible checks

- Primary audio app: `npm run check` passes lint, TypeScript, 1,145 tests across 83 files and production build in the integration audit.
- Preserved Open Sync suite: 730 tests and production build pass. Imported source and deployment adapters are documented in the primary repository's `integrations/open-sync/PROVENANCE.md`.
- Authored atlas: `npm ci && npm test` runs seven independent numerical/data gates and seven DOM behavior gates. These include exact integer binomial checks, independent cycle quadrature, connected graph references, explicit execution statuses, invalid-input clearing and journal persistence failure.
- Research artifacts: `python3 research/verify_rounds.py` verifies six result bundles and lossless CSV manifests. Read `research/README.md` for regeneration instructions and environment requirements.
- Assembled website: `python3 scripts/build_site.py --output dist` fetches exact public commits and adds navigation to the imported exhibits. No imported program is executed by this assembly step.

## What these checks establish

The checks address the declared equations, implementation and provenance. They do not establish clinical efficacy, a unique alchemical decipherment, antigravity, source-free energy, extrasensory perception, or a physical apparatus result. The independent agent reviews are recorded separately from producer outputs and share model-family provenance.

## Publication status

Deployment verification is recorded by the publishing repository's GitHub Actions run and the live `build-manifest.json`. The standalone repository requires its own repository creation and Pages configuration; a workflow file alone does not enable Pages. Read the final delivery record for confirmed URLs and remaining access blockers.
