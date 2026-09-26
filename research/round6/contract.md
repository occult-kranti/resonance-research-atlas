# Round 6 final frozen contract — concealed targets, leakage and stopping

Frozen before implementation and execution, 2026-09-26 UTC. Advisor selected this
FINAL round after independently admitting Round 5. It supplies a methodology
benchmark for a proposed dream-associated concealed-target question. There are
no participant results and no proof or disproof of astral travel in this model.

Primary endpoint: exactly n=40 prespecified four-category target trials, no early
stopping. Targets are independent and equally likely; a fixed choice independent
of the target has chance success p0=1/4. Count K and compute its exact one-sided
binomial tail. Alpha=1/20. The critical count is the smallest k with
P_p0(K>=k)<=alpha. All target categories and exact-match scoring are fixed;
post-hoc semantic similarity, multiple dream selections and exclusions are absent.

Disclosed leakage control: with probability lambda the target is known, otherwise
the guess has chance success. Then p_hit=lambda+(1-lambda)/4 for
lambda=0,1/10,1/2. Compute exact probability of exceeding the SAME fixed-n cutoff.
This positive control is explicitly ordinary information leakage, not a proposed
mechanism of dreaming or an inference from a high score.

Invalid-naive optional-stopping control: inspect every prefix n=1,...,40 and
stop at its first nominal one-sided binomial tail <=.05. Calculate the chance
of ever crossing using exact rational absorbing-state dynamic programming,
not the independent-tests formula. When no attainable count qualifies, the
boundary is n+1. Preserve the fixed-40 endpoint as the primary proposed test.

Secondary synthetic validation: 50000 studies, NumPy default_rng seed2026092606.
Generate a 50000x40 array of uniform target labels {0,1,2,3}; fixed synthetic
prediction0 in every trial, independent of every target. No genuine concealed
target tool or participant interface is implemented. Save every study's total
hits and first crossing index in compressed CSV. No human dream reports exist.

## Frozen gates

1. Every exact PMF is nonnegative and sums to1; tail probabilities decrease in k.
   The n40 cutoff qualifies and its preceding count does not.
2. Absorbing DP conserves remaining plus absorbed probability exactly at every
   prefix; no-absorption transitions reproduce closed-form binomial masses.
3. Exhaustive weighted enumeration of all2^12 sequences independently matches
   the DP crossing probability through n12 exactly.
4. Full40-look crossing probability exceeds the fixed-n false-positive rate;
   dependence is handled by the DP rather than by an independence assumption.
5. Leakage probabilities use the disclosed p_hit formula and fixed cutoff;
   detection probability strictly increases for the three selected lambda values.
6. Synthetic fixed and optional-stop rates differ from their exact probabilities
   by no more than 6 sqrt(p(1-p)/50000)+1/50000. Report both, including failures.
7. Save exact PMF/tails, all prefix boundaries/crossing probabilities, simulation
   counts, hashes, figures and a clearly hypothetical protocol discussion.

Any future real test requires concealed targets outside the participant's browser,
frozen reports/choices before revelation, prespecified sample size and exclusions,
and independent scoring. Dream lucidity and target information are separate
endpoints. This benchmark does not prescribe sleep disruption, drugs, electrical
stimulation, or bodily exposures. After review of this round, stop research loops.
