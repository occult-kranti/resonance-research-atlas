# Round 5 frozen contract — selection among many analyses

Frozen before implementation and execution, 2026-09-26 UTC. The advisor selected
this after Round 4: stable individual measurements do not control false positives
when an analyst chooses the best result among many candidate analyses.

Primary model: m independent continuous Uniform(0,1) null p-values per study,
m=1,5,20,100, alpha=1/20. These are ideal valid null p-values; they are not
measured human, alchemical or frequency data. Uncorrected familywise false
positive probability is 1-(1-alpha)^m. Bonferroni per-test threshold alpha/m
gives independent-model probability 1-(1-alpha/m)^m, no larger than alpha.
The union bound ensures <=alpha under arbitrary dependence if every marginal
p-value is valid and the full family size m was specified correctly.

Negative/control dependence model: all m p-values are the same uniform draw.
Then uncorrected familywise probability is alpha, and Bonferroni familywise
probability is alpha/m. The independence formula must not be applied to this
duplicate family.

Exact rational probability calculations are primary. Secondary illustration:
NumPy default_rng(seed=20260926), 50000 synthetic null studies, one 50000x100
uniform matrix with nested first-m families. A separate 50000-length uniform
array supplies the duplicate-family control. Sharing family prefixes affects
cross-family correlation, not each family's marginal probability. No actual
study is performed; no false-positive percentage estimates a real claim's truth.

## Frozen gates

1. Exact rational independent rates equal their formulas, and corrected rates
   are <=alpha for every declared m.
2. Exact duplicate-family uncorrected rates remain alpha; corrected rates are
   alpha/m. For m>1, uncorrected independence rates exceed duplicate rates.
3. Each simulated rate lies within 6 sqrt(p(1-p)/N)+1/N of its predeclared exact
   probability. This broad deterministic-seed diagnostic is not a confidence
   interval for real data. All rates and tolerances are recorded, not selected.
4. Corrected discoveries are a subset of uncorrected discoveries in each
   simulated family; per-family counts and full study minima are saved.
5. Save JSON, compact summary CSV, compressed per-study minima, and SVG/PNG with
   exact probabilities and simulated points clearly separated.

The subsequent final round is selected only after advisor review and will use
the lessons about calibration, fixed endpoints, and concealed information.
