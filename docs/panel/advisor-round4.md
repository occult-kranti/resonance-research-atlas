# Round 3 admission and Round 4 selection

Round 3 is accepted within the displayed synthetic observation map. The reviewer read the full implementation and independently used exact matrix minors, a Leibniz determinant calculation and the explicit inverse, rather than the producer's RREF routine.

For A=[[1,0,1],[0,1,1]], a 2×2 minor equals 1 and the three-dimensional domain has nullity 1. Adding row (0,0,1) gives determinant 1 and inverse c=(y1−y3,y2−y3,y3). Repeating (1,0,1) gives determinant zero and retains rank two. All 101 saved rational fiber records passed exact checks. The interval proof uses c1=1/5−t, c2=2/5−t and c3=3/10+t, whose nonnegativity intersection is [−3/10,1/5]. Review evidence is in `research/round3/independent-review.json`.

**Admitted improvement.** The archive's proposed one-to-one mapping from a visual sign to material composition needs an injective observation model. This example supplies two competing candidate states, a whole ambiguity family and an independent-assay intervention that can distinguish them. It does not establish the composition of a historical sample. An independently known total amount would provide an additional assay and can remove this particular ambiguity; the example does not hide that possibility.

**What remains.** The successful inverse assumes exact noiseless values. Full rank by itself does not bound error in a real measurement. That unresolved premise selects Round 4.

## Round 4 decision

Keep the first two synthetic channels and use third row (1,0,1+epsilon). For epsilon>0 it is independent, but c3=(y3−y1)/epsilon. Under a fixed per-channel absolute error bound delta, the exact worst-case c3 error is 2 delta/epsilon. Opposite errors in the two subtracted channels attain this bound.

Compare the near-duplicate assay to direct independent third row (0,0,1), with the same declared per-channel error convention. Enumerate the vertices of the three-dimensional error cube: a linear error map reaches its componentwise extrema at vertices, so the eight corners provide a complete bounded-error calculation, not a Monte Carlo sample. Report determinants/rank, singular values as supporting numerical diagnostics, exact bounds, and a retained negative estimate when it occurs.

Freeze epsilon values, delta and tolerances before production. The comparison is conditional on calibrated rows and the specified absolute error model; it is not a global optimum among real instruments. Clipping negative recovered amounts or imposing a total changes the inference and must not occur silently.

## Inherited corpus review

Reviewed `research-corrections.html` and targeted source assertions in the revised alchemy, experiment and roundtable pages. The process table now separates historical witness, possible interpretation, alternatives and diagnostics. It correctly retains the missing-code status of inherited simulation families. Requested additional consistency repairs: absence of a demonstrated hidden-target effect is not universal refutation; remove remaining unsupported success percentages and priority promises; do not label historical notebook failures as a modern controlled universal null; a null constrains the stated model and sensitivity only.
