# Independent atlas review

Reviewer: a separate repository-audit model agent. The reviewer inspected formulas, data relationships and observed DOM behavior; the author agent made the UI/model repairs. This is an engineering and mathematical check, not human peer review, a participant study or clinical validation.

## Corrections prompted by review

| Finding | Why it mattered | Repaired behavior |
|---|---|---|
| Static oscillator energy used the periodic average | At zero drive frequency the force and displacement are constant; averaging a cosine squared is inappropriate | Zero-frequency stored energy is `k A² / 2`, while nonzero periodic motion retains its time average |
| Rounded sample count disagreed with DFT spacing | A noninteger requested `fs × T` was floored, but spacing still used the unrounded duration; zero-sample records were possible | Integer `N ≥ 2`, spacing `fs / N`, and effective duration `N / fs` are reported together |
| Input bounds and numerical overflow were not enforced | Invalid entries left old values or nonfinite chart coordinates visible | Empty/out-of-range controls and unsupported derived values are rejected; old outputs clear on failure |
| The first 40 graph nodes were all sources | The initial data had 41 sources, so the overview displayed no experiment relationships | A bounded connected overview includes experiments and related sources; the accessible table retains every edge |
| Planned rounds were counted as recorded and roadmap status used broad substring matching | “Not started” appeared in progress; pending review could be mistaken for completed or unstarted work | The overview says planned and recorded; explicit status precedence distinguishes unstarted, review-pending and executed states |
| Thin-shell model assumptions were underspecified | The Schumann reference formula is not the eigenfrequency formula for an arbitrary filled spherical cavity | The model explicitly states its ideal thin spherical shell assumption |
| Failed journal persistence could hide the newly entered report | With storage quota exceeded, reading the older saved array discarded the newest memory-only entry from view/export | The memory fallback retains the new report for immediate export and informs the user |
| Very small binomial probabilities underflow numerically | A finite experiment with `0 < p < 1` cannot have a mathematically zero upper tail | The UI reports a small upper bound rather than exact zero |

## Independent numerical and data checks

Run `node tests/independent-review.mjs`.

Seven review gates check: ideal cavity scaling and invalid bounds; the constant-force oscillator limit; independent numerical integration of force × velocity, damping loss and stored energy across a cycle; DFT spacing from the actual sample count; binomial tails against exact integer enumeration of four-category outcomes; unique graph/source IDs, resolvable citations and acyclic roadmap dependencies; and actual local output/review files for every round whose status claims execution or independent review.

The oscillator check computes averages by 8,192-point cycle quadrature at five distinct drive frequencies. It does not merely repeat the closed-form power expression. The chance check enumerates integer binomial outcome counts before converting to floating point, and also checks large-sample symmetry. These gates passed after the repairs.

The source registry exposes reading depth and limitations, including selected passages, abstract-only inspection, blocked access and papers merely located for later reading. Source IDs, citation endpoints and URL syntax were checked; this does not establish that every cited statement is true or that every remote link remains reachable. Existing source researchers' detailed reading records remain the evidence for source interpretation.

## Behavioral checks

Run with an installed `happy-dom`, or point to an existing installation:

```sh
HAPPY_DOM_MODULE=/absolute/path/to/happy-dom/lib/index.js node tests/independent-dom-review.mjs
```

Seven DOM gates inspect all authored routes; source reading-depth disclosures and filtering; invalid control clearing; connected graph nodes and its complete table; six explicit round statuses and planned/review classification; no automatic storage or network transmission while typing dream recall; persistence failure and JSON export; and probability underflow plus an explicitly unexecuted study-template export.

Journal observations are saved only through the labeled Save action. The page discloses unencrypted browser storage. The test substitutes quota-failing storage with an existing saved report, enters a second report, and verifies that both remain in the explicit export. The only mocked network request is the public research JSON; entering, saving and exporting private test text produces no outbound request.

The dream page generates no hidden targets. It distinguishes personal recall, reported self-location and external-information accuracy; its study template requires an independent target custodian and response locking outside the participant device. The journal does not authenticate sleep stage, target concealment, an immutable timestamp or extraordinary perception.

## Remaining limits

- DOM checks do not measure visual layout, focus geometry, contrast or actual Chromium rendering. Chromium was unavailable in this execution environment and its attempted download returned an invalid archive.
- No hardware exposure, human trial, physiological recording analysis, physical prototype or verified alchemical replication was performed by this UI review.
- Round status validation requires actual contract/result/review files; it does not transform an accepted toy model into an empirical result. Planned work remains planned until its recorded outputs and reviews exist.
- Graph connectivity records labeled research relationships. It is not evidence of physical causality or a mechanism connecting symbolic systems to measured fields.
