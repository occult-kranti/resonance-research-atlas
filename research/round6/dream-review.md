# Dream awareness, unusual bodily experience and external information: design review

Date: 2026-09-26. Status: literature/design preparation for the sixth adaptive loop. No participant session or sixth-loop computation was run by this researcher. The advisor must select the exact sixth target after reviewing Round 5.

## Three claims need three different outcomes

| Claim | Appropriate observable | What does not establish it |
|---|---|---|
| “I knew I was dreaming” | A contemporaneous report of dream awareness; laboratory work can add independently scored sleep and a prearranged signal | Merely vivid imagery or a floating sensation |
| “I felt outside my body” | First-person self-location/body-ownership report, with timing and state characterization where available | A conclusion that a physical entity left the body |
| “I acquired concealed external information” | Prespecified target accuracy under independently audited blinding and information isolation | Confidence, symbolic similarity, EEG activity, an eye signal, or the felt reality of the experience |

A meaningful subjective event can be documented respectfully without deciding its physical explanation in advance. “Astral travel” belongs in the cultural/claim label unless the specific externally testable proposition is stated.

## Current EEG source supplement

**DR-UBE2026:** Campillo-Ferrer et al., Consciousness and Cognition 139,104002, online 11 February 2026; DOI 10.1016/j.concog.2026.104002. The author-posted journal text was inspected because publisher and university endpoints returned 403. Exact URLs and passages are in dream-sources.json.

The source's key limitation is that an eye signal does not by itself demonstrate lucidity. Its EEG associations are correlational; timing uncertainty and disrupted sleep limit interpretation. We do not adopt its induction procedure. Selected methods and discussion were read, not raw EEG reanalyzed.

The advisor is independently preparing the main Konkoly/DREAM/targeted-lucidity/Ehrsson source packet. This supplement should be merged by source ID while preserving each researcher's actual reading depth.

## Sleep-friendly observation session

This is an optional personal observation routine, not an efficacy protocol or a method promised to cause lucid dreams.

1. Before the person's usual bedtime, write a neutral intention: “If I remember a dream, I will record what I experienced.”
2. Follow the ordinary bedtime routine and leave sleep uninterrupted. The project does not add alarms, sleep restriction, flashing cues, electrical stimulation, substances or scheduled awakenings.
3. After naturally waking, record a short free-text account before interpreting it. “No dream recalled” is a valid record.
4. Record separately: approximate recall time; whether the person knew they were dreaming *during the dream*; perceived control; changes in self-location; emotional tone; and how certain they are about the order of events.
5. Distinguish the immediate record from later additions. If the exercise disrupts sleep or becomes distressing, skip it.

No eye-motion “verification” is claimed from an ordinary journal or a phone. Without independent physiological recording, sleep stage remains unknown. The routine supports honest recall, not a demonstrated increase in lucidity or a test of paranormal perception.

Suggested UI: **“Dream journal: record awareness and experience. No recall is a useful entry.”** Keep lucid awareness, perceived location and interpretation as separate fields rather than converting them into a single “astral success” score.

## Preregistered external-target study design — a proposal only

This future study tests a narrow information claim, not metaphysics as a whole. It is distinct from the observation routine and would require an appropriate independent research review before participant implementation.

**Null:** response labels are independent of a concealed target. With four equally probable target identities and one locked response, success probability is 1/4 even when participants prefer one response, provided random target assignment is independent and genuinely uniform.

**Alternative:** accuracy exceeds chance by a prespecified practically relevant margin, under the same blinding and stopping rules. An above-chance result would still need leakage/error checks and independent replication before a mechanism could be proposed.

### Information flow and custody

- Fix four unambiguous target identities and one forced-choice response field. Primary scoring is exact label agreement, not semantic resemblance.
- An independent custodian selects each target after the trial is registered using documented randomness and records the timing. The target stays inaccessible to participant, facilitator and outcome analyst until the response is locked.
- The target and its decryption material must not be downloaded to the participant's device in advance. A checksum/commitment is useful only with sufficient randomness and a secret salt; four unsalted possible target hashes are trivially enumerable.
- Target-generation logs, run IDs, response locks and reveal logs receive tamper-evident records and independent time ordering. There is one eligible response per registered trial.
- Sensory and social leakage is separately audited: device notifications, sounds, experimenter knowledge, reflective surfaces, shared screens, filenames/URLs, caches, accessibility labels and network responses.
- The primary dataset includes every initiated eligible trial. Omitted responses, technical invalidations and withdrawals follow prespecified rules and remain counted in the audit trail. Invalidity cannot be assigned after learning correctness.

A claimed verified dream-state subset is a different endpoint. It requires blinded state scoring and fixed eligibility rules; selecting only striking dreams or successful target matches invalidates the simple chance calculation. Repeated trials from one participant must be handled at the participant level or with a prespecified conditional/randomization analysis.

### Statistical plan

Predeclare trial count, decision threshold, primary endpoint, minimal effect of interest, exclusions and stopping rule before any response is observed. For an independent fixed-N four-choice design, exact binomial calculations provide the reference null. A possible planning specification is one-sided alpha 0.01 and power 0.80 at success probability 0.40; the later code must derive N and the threshold rather than guessing them.

Report the confidence interval and all misses. Do not stop when significance first appears, reset failed runs, explore many targets then publish the best subset, or change the matching rule after seeing the answer. If optional stopping is desired, adopt a valid sequential method before collection.

A null result limits the stated effect at the tested precision; it does not logically disprove every possible external-information claim. A positive result establishes a statistical discrepancy under the recorded design before it establishes any explanation.

## Sixth-loop computational target proposal

The appropriate immediate deliverable is a **synthetic methodology simulator** that checks:

- Uniform independent targets produce the exact chance distribution.
- Biased response preferences still yield chance with uniform independent targets.
- A deliberately leaky target channel inflates accuracy and is explicitly detected/flagged.
- Selecting the best of many null runs or stopping at significance inflates false positives.
- A frozen-count decision rule respects the chosen type-I error, verified analytically and by reproducible Monte Carlo.
- Injected above-chance performance produces the expected planning power; this injection is a mathematical test fixture, not an observed psychic effect.
- Missing trials and clustered responses are handled under declared assumptions rather than silently discarded.

These proposed tests remain unexecuted until advisor selection. Synthetic records must never be labeled participant data, REM-confirmed events or evidence for astral travel.

## Static-site limitation

A GitHub Pages client can show the journal, source map and statistical simulator. It cannot claim genuine target concealment when all target data or decryption secrets are present in client code or assets. A real study needs separate trusted custody or a properly designed server and a verified response-lock process. The site must say **“Simulation of study methods — not an experiment demonstrating external perception.”**

## Source constraints and graphical brief

The named clinical and laboratory papers support only their own measured outcomes. No single EEG band should be labeled the frequency of astral travel, dream consciousness or the entire person. Time-window choice, muscular/eye artifacts, source localization and sleep-state labeling must be retained wherever electrophysiology is discussed.

Draw a three-lane evidence map: **experience report**, **sleep/state evidence**, **concealed-target accuracy**. Permit a connection to a stronger claim only when the corresponding measurement exists. Use a separate box for cultural interpretation. Do not draw a ghost exiting a body as a scientific diagram; if such imagery is used as cultural artwork, label it as interpretation.

