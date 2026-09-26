# Repository integration audit — 2026-09-27 UTC

## Frozen source inventory

| Repository | Inspected main/default commit | Access and architecture | Preservation decision |
|---|---|---|---|
| open-sync | 02425613cd057406d92c4f3ee33b5fc54a493601 | Public; React 19 + Vite 7 + TypeScript; BrowserRouter without basename; no workflow or lockfile; MIT | Full source import into brainwave_opensync/integrations/open-sync, independent build deployed at /brainwave_opensync/open-sync/ |
| resonant-vessels | e65c1974fc4f5f90ba4d584ccb3332199e171748 | Public; no-build HTML/CSS/JS; 11 HTML folios and 62 PNGs; ~123 MB working content | Preserve complete relative-path static site under research archive; identify diagrams as prior illustrations until reproduced |
| astrology-sim-ant | 3a3ce9953e47a078e659723a52187648f1f08486 | Public; vanilla ES modules, astronomical calculation engine, sourced historical/occult corpus, operation graph, service worker; ~16 MB | Preserve independent application root and expose linked tools/corpus in new hub; do not mix symbolic graph edges with physical causal edges |
| newton-tesla-alchemy | 1c7b9971b74aa14aeae426d40ba8eda0ae0d8644 | Private; plugin-readable; README and four markdown dossiers only; metadata size 0 is stale, repo is NOT empty | Recovered all 5 text files locally; source commit and original labels required when integrating requested published archive |

Local source directories: /workspace/scratch/43c586568d88/repos/<repository>. newton-tesla-alchemy was recovered with GitHub plugin file reads, not cloned. No remote writes performed by audit.

## open-sync feature set and integration risks

22 routed modules: Home, Guide, Studio, Frequency Library, Presets, Levels, Analyzer, Cymatics, Sleep & Dream, Quick Lab, Theory Explorer, Sample Lab, Sonic Lab, Replication Bay, Safety, MED FREQ, Knowledge, About, Experiment Lab, Critique Library, Hypothesis Tracker, Programs Archive. The newer brainwave app has substantial overlap and different engine/session contracts; replacing its files wholesale would regress newer audio rails, export worker, navigation, everyday player and specialized harmonic/channeled pages.

Keep the complete older app as a separately built suite and use whole-page navigation. This preserves MED FREQ and its original evidence records without creating two live audio providers inside the same document. The main Projects screen stops session and previews before leaving. The preserved app gets a return link that unloads its own audio context.

Defects to repair in imported adapter:
- BrowserRouter has no basename and GitHub Pages cannot resolve its clean deep links. Use HashRouter for the imported suite.
- Preview URLs and 20 X10 stimulus-pack URLs are root absolute. Resolve via build BASE_URL.
- Previews and stimulus WAVs are gitignored but manifests advertise them. Generate previews from original engine; reuse the main app's byte-identical X10 files only after matching hashes, otherwise show absence honestly.
- root-absolute plain anchors for /about and /knowledge must become hash-route links.
- Pin newly resolved package lock; retain MIT notice and source provenance.
- Main Vitest/eslint must scope its own sources; integration's separate project uses its own dependency/test config.
- Main PWA fallback must exclude /open-sync/, /research/, and existing /v2/. Never replace previous-release deployment.

## resonant-vessels findings

README says 10 folios/46 images; actual tree includes bashar.html, making 11 folios, and 62 PNG assets. README claims .github/workflows/pages.yml automation, but no workflow is tracked. Links and assets are relative; isolated directory deployment is straightforward. main.js supplies presentation behavior (parallax, fade-in, outline navigation); it is not a numerical simulation engine. Existing images and prose therefore need separate reproducibility labels. No root license, AGENTS.md or CLAUDE.md is present; preserve provenance, avoid imposing MIT on copied research imagery by inference.

## astrology-sim-ant findings

Extensive feature set: Lilly Western chart workbench; Vedic/Jyotisha alongside it; dignities, houses, elections, horary, natal, transits, returns, time lords, compatibility; Picatrix, Jung, alchemy chronology, cross-tradition comparison, geomancy, I Ching, tarot, runes, kabbalah; operation graph with generated witness gating; export and browser-local LLM assistant.

Architecture rules in HANDOFF.md: no build step; pure core computation under assets/js/core; DOM under assets/js/app; mountChrome computes root from import.meta.url; preserve relative paths. Later docs/plans/HANDOFF.md is authoritative on graph mechanics: never hand-edit generated opgraph.js, run seed-opgraph-gate.mjs then gen-opgraph.mjs, read gate results, verify reproducibility in pristine checkout. Existing corpus explicitly warns about citation misattribution and requires fetcher/compiler split for research.

.github/workflows/pages.yml deploys main and a historical feature branch, enablement true, entire root. New archive copy should not copy its workflow as the outer deployment. Service worker scope must remain inside the archived application directory. No top-level project license; vendored astronomy engine is MIT and D3 ticks carries its own license. Preserve vendor notices and user-source attribution. Known local-config.js key convention exists in handoff; no keys inspected or requested in audit. Export only tracked source, and ensure local configuration ships empty.

## newton-tesla-alchemy findings

README and four substantial dossiers:
1. Newton/Tesla historical corpus, alchemy, patents, stationary-wave claims.
2. Jung/Penrose/Feynman, consciousness and quantum biology claims.
3. Schumann cavity physics, modal analysis, multichannel human measurements.
4. Fringe archives, Reddit discourse, free-energy patents, government programs.

Every paragraph is intended to carry ESTABLISHED / HISTORICAL / FRINGE / SPECULATIVE labels. These are prior research notes, not independently verified primary sources. Hub should preserve originals, then maintain a separate current-source claim ledger and experiments with falsifiers. No application, workflow, executable experiment or license is present.

## Integration sequence

1. Freeze the five source commits and inventory; import open-sync source without deleting either upstream.
2. Build main and imported audio suite independently; preserve v2; verify Pages base paths and cross-app audio stopping.
3. Build new research hub with source archive directories, registry links to all projects, primary-source claim ledger, experiments, numerical calculators and typed graph edges.
4. Run research panel loops as actual proposals/reviews/revisions, recording decisions and outstanding gaps rather than asserting experimental outcomes.
5. Validate route integrity, source links, local reproducibility, and explicit model assumptions.
6. Publish only through user-authorized root workflow after build/test results; record actual deployed commit and URL.
