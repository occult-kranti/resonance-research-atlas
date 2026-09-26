# Round 4 admission and Round 5 selection

Round 4 is accepted under its fixed assay coefficients and separately bounded channel errors. The independent review derived the inverse coefficient rows and their absolute row sums. For eta_j in [−delta,delta], a linear coordinate error attains its maximum when the perturbation signs match its row coefficients. This proves why the eight cube corners cover the componentwise worst cases; no probability distribution or stochastic independence is assumed.

For the near-duplicate third row (1,0,1+epsilon), the error map is

- Delta c1=(1+1/epsilon)eta1−eta3/epsilon;
- Delta c2=eta2+eta1/epsilon−eta3/epsilon;
- Delta c3=(eta3−eta1)/epsilon.

The exact bounds are delta(1+2/epsilon), delta(1+2/epsilon), and 2delta/epsilon. At delta=0.001 and epsilon=0.001, the c3 error bound is 2 despite the true reference amount 0.3 and an invertible matrix. The independent third row gives c3 error at most 0.001 under the same channel-error convention. Negative unconstrained estimates are retained, not silently clipped.

This improves the proposed alchemy research method: an added observation must be both independently informative and sufficiently calibrated for the desired discrimination. The example is conditional on assay scaling and noise assumptions; it does not rank real instruments or identify Newton's materials. Details and hashes are in `research/round4/independent-review.json`.

## Next unresolved premise

An investigator can still choose whichever frequency, material interpretation, statistic or panel hypothesis happens to look most striking. Better measurement conditioning does not control this selection process. Round 5 therefore tests a declared multiple-comparison null.

## Round 5 selected contract class

For m independent continuous Uniform(0,1) null p-values and fixed alpha, the probability of at least one p≤alpha is 1−(1−alpha)^m. The single predeclared test is m=1. Compare m=1,5,20,100 at alpha=0.05 with Bonferroni threshold alpha/m. Under independent tests the corrected familywise rate is 1−(1−alpha/m)^m; under arbitrary dependence the union bound gives at most alpha when each marginal p-value is valid.

A perfectly correlated duplicate-test control must retain the same p-value across all candidates. Its uncorrected rejection probability is alpha, not the independent-test formula. This makes the dependence assumption visible and links the issue to the preceding duplicate-assay lesson.

Exact calculations are the principal result. If a seeded Monte Carlo illustration is used, freeze sample count, generator/seed and a declared sampling-error tolerance before execution. The simulation should retain all generated cases and compare rates without fitting an outcome after seeing it. This is a model of selection bias, not an estimate of false discoveries in any unexamined biological or occult corpus.

After review, the final sixth round will apply the lesson to dream/lucidity reports and a separately specified blinded target-acquisition question. Preparatory source reading is saved, but no sixth-round experiment has yet run.
