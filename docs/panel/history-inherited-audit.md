# Historical-source integration audit

Date: 2026-09-26. Read after recovery of `newton-tesla-alchemy` and `resonant-vessels`. This is an amendment to the proposed historical work, not a claim that the inherited research was reproduced. The four dossiers were read in selected sections (executive summaries, relevant historical/scientific claims and source lists); the alchemy, experiments, lab and roundtable pages were inspected for provenance and model scope. Not every external link in those inherited files was reopened.

## Preserve the strongest existing work

- Keep the four-dossier organization and the separation of historical, established, speculative, and fringe claims, but make status belong to an individual claim and attach inspected-source depth.
- Keep the alchemy page's distinction among chemistry, allegory and dispute. Preserve the fact that Newton's failed interpretations and crossed-out notes matter.
- Keep the sound lab's intended distinction between stimulus-locked responses and oscillator entrainment, its matched-controls principle, and its explicit alias sets. Treat its displayed numerical outputs as inherited reports until their code and data are recovered and run.
- Keep the existing multi-modal frequency question, boundary-condition controls, input/output accounting, and government-custody-versus-confirmation distinction.

## Corrections and limits before reuse

| Location / inherited claim | Finding | Integration action |
|---|---|---|
| Dossier 01, Clavis paragraph and manuscript table: Newton's original composition | **Correctable error.** The Chymistry project's historical account states that the document derives from a Starkey-to-Boyle letter of 1651. Newman's own reassessment makes the same correction. The later `alchemy.html` already knows this, so the two source repositories disagree. | Change the current synthesis to “Starkey material transcribed by Newton”; retain the inherited draft as dated history, with a correction link. Sources H16–H17. |
| Dossier 01: more than 5,000 cited works | **Denominator ambiguity.** Mink et al.'s abstract uses “works”, but the article body describes >5,000 citation occurrences and hundreds of texts. | Use “over 5,000 bibliographic references in the encoded corpus”; do not imply 5,000 distinct books. Source H18. |
| Dossier 01/02: alchemy yielded non-mechanical gravity; Jung's psychology explains the practitioners | **Interpretation, not settled provenance.** The inherited dossiers themselves mention scholarly disagreement. | Keep competing historical readings side-by-side. Do not equate Newton's vegetative spirit with a modern field or substitute Jung's symbolic framework for laboratory history. H16–H17 provide the contrary historical argument. |
| Dossier 02: a Jung quotation sourced through social media | **Inherited attribution explicitly unverified.** | No quotation in the current synthesis until checked in an authenticated edition. Keep only a paraphrase marked “interpretation; primary passage pending.” |
| Dossier 04: all ~300 Tesla patents are engineered, replicable devices | **Unsupported universal generalization in an inherited source.** A patent list does not test each claim. | Per-patent provenance and per-mechanism evidence; preserve only cases individually reviewed by the Tesla branch. |
| Dossier 04: no scientific publications on 432-Hz healing; neuroscience supports theta entrainment from binaural beats | **Overbroad and mixed claims.** Existence of small studies is a different question from reliable benefit, mechanism or equivalence. | Replace with evidence-specific clinical and measurement statements from the current audio branch. No blanket literature-absence claim or clinical effect inferred from this historical audit. |
| `experiments.html` B7: historical signs map one-to-one to microstructure/composition | **Unproved identifiability claim.** A star, color or mesh can constrain a process without uniquely identifying composition/history. | Reframe B7 as testing the discrimination of signs against alternative materials/states. H-N1 adds an exact synthetic counterexample to the one-to-one assumption. |
| B7: precise material windows, thresholds, “iff” outcomes and success probabilities | **Proposals, not executed findings.** The inherited page says thresholds are preregistration proposals, but individual paragraphs can still read as results. | Label each proposed endpoint locally. Remove forecast success percentages from the current research home; retain only explicit assumptions for power calculations. No hazardous physical replication instructions in the new safe exhibit. |
| `alchemy.html`: dendritic appearance establishes diffusion-limited aggregation specifically | **Mechanism stronger than morphology alone supports.** Dendrites are compatible with several growth dynamics. | Say “branching growth is consistent with transport and solidification processes; mechanism discrimination needs time-resolved/material data.” A4 compares competing image generators. |
| `experiments.html` B2/B3: first whole-body atlas, any object's rigorous fingerprint, pure-material linewidth bounds | **Priority and universality require separate evidence.** Geometry, mode, damping, measurement channel and boundary conditions matter. | Say “proposed multimodal atlas of selected observables”; include a channel/units/boundary table. Do not claim first-ever priority or complete object identification. |
| `roundtable.html`: prior 5% is a subjective allowance | **Explicit subjectivity does not turn a number into calibrated evidence.** | Preserve as historical panel opinion if needed; do not display as experiment success probability. |
| `lab.html`: six executed simulations, code paths and JSON outputs | **Reproducibility gap in the recovered snapshot.** The referenced `lab/sims/` files are absent from the recovered repository; images and prose survive. | Display “inherited reported result; executable source not recovered.” New executed simulations must have their own code, seed, assumptions and results. Never silently relabel the old screenshots as current validation. |

## How the proposed work improves the prior work

The earlier B7 chemical-sign program already asks the right observable question. H-N1 supplies its missing inverse problem: a map can fit data perfectly and still admit multiple states. The third-assay and duplicate-assay controls distinguish additional information from repeated measurement. This gives the site an executable explanation of why a material, a person or a pattern cannot be assigned a unique complete frequency from a few readouts.

The new source graph should connect Starkey → copied Clavis → Newton's notes using an **authorship/transcription** relation, and distinguish that chain from a **modern reconstruction** relation to Newman. The same graph should place Jung's psychological reading on an **interprets** edge, not a causal physics edge. The 2060 card adds the surrounding manuscript qualification directly, avoiding a detached sensational numeral.

## Advisor feedback accepted for H-N1

The advisor identified a numerical trap in the proposed diagnostics: a 2×3 matrix has a one-dimensional domain kernel even if both singular values returned by a compact SVD are positive. The accepted implementation must report `domain_nullity = columns − rank`, the explicit kernel, and optionally the minimum eigenvalue of AᵀA. It must not use the smallest *returned* compact-SVD value alone as a test of injectivity. This review strengthens the candidate contract without changing its frozen A matrix or candidate mixtures.

## Additional sources actually inspected

- **H16:** [Chymistry project grant/history](https://newton.dlib.indiana.edu/page/grant), paragraphs on source attribution and Clavis, plus replication scope (web lines 307–328). This is an older project statement, not a current progress census.
- **H17:** William R. Newman, [A Preliminary Reassessment of Newton's Alchemy](https://history.duke.edu/sites/history.duke.edu/files/documents/Newman%20Colloquium%20Paper%202014.pdf), p.3 and notes 6–7. Only selected passages read, not the whole 35-page paper.
- **H18:** Mink et al., [Encoding Newton's Alchemical Library](https://jawalsh.github.io/assets/pdf/mink_et_al_2019.pdf), abstract and body pp.2–7. The correction distinguishes citation occurrences from unique texts; the abstract/body wording difference is retained, not concealed.
