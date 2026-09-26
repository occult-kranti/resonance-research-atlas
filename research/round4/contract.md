# Round 4 frozen contract — full rank can still amplify noise

Frozen before implementation and execution, 2026-09-26 UTC. Advisor selected this
from Round 3's noiseless-reconstruction limitation after independent review.

Use dimensionless relative amounts c=(1/5,2/5,3/10), not normalized fractions.
Original rows are (1,0,1),(0,1,1). The third near-duplicate row is (1,0,1+epsilon),
with epsilon=1,1/10,1/100,1/1000, plus epsilon=0 as the singular control.
Each measured channel has its own bounded additive error |eta_j|<=delta,
delta=1/1000 in calibrated dimensionless signal units. Bounds are deterministic,
not Gaussian confidence intervals. All eight error-box corners will be evaluated
using exact rational arithmetic. Matrix row scaling and the absolute per-channel
noise bound are fixed; renormalizing a row requires renormalizing its noise too.

For epsilon>0, det A=epsilon and c3=(y3-y1)/epsilon. Hence
|error(c3)|<=2 delta/epsilon, attained by eta3=delta,eta1=-delta.
The component-1 and component-2 bounds are delta*(1+2/epsilon).
Compare the independent third row (0,0,1), whose exact bounds are
(2delta,2delta,delta). Report conventional 2-norm condition numbers only as
supplemental floating-point diagnostics, not as the primary bound or an optimal
sensor-design theorem. Negative unconstrained estimates are retained and counted.

## Frozen gates

1. Exact determinant equals epsilon; positive-epsilon cases are invertible and
   epsilon=0 gives duplicate-row rank2/nonuniqueness.
2. For each positive epsilon, exact corner maxima equal all three derived error
   bounds. The c3 specified opposite-sign error pattern attains its bound.
3. Independent-row control has exact corner maxima (2delta,2delta,delta).
4. Supplemental numpy solve agrees with exact rational inversion to <=1e-10
   in each component over the corner grid.
5. At least one epsilon=1/1000 corner yields a negative unconstrained component;
   no clipping or nonnegative estimation is introduced. This flags instability,
   not a physically negative material amount.
6. Save results, corner CSV, bound-versus-epsilon SVG/PNG, hashes and interpretation.

No statistical sampling, chemical operation, or human experiment is executed.
The advisor will select the following round only after reviewing these outputs.
