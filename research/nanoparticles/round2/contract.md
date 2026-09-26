# Nanoparticles N2 frozen contract — heat and thermometer transfer

Frozen before execution after N1 advisor admission. Project hypothesis NP-H2:
constant absorbed power can appear duration-dependent under a naive temperature
slope estimate, while calibration of thermal and sensor transfer removes that
artifact in this declared model. This is a new project test of established
first-law dynamics, not a new physical law or measured nanoparticle result.

C theta_dot=P(t)−G theta; tau_s y_dot+y=theta. Here theta is the spatially
uniform specimen temperature rise(K), y is thermometer rise(K), C=4J/K,
G=.02W/K, tau_s=10s. Start theta=y=0K. A known synthetic power pulse P=.2W
acts for120s, then P=0 for280s of cooling. Independent duration comparisons
at10,30,60s use the corresponding trace prefixes. Thermal time constant C/G=200s.
This is a lumped thermal and first-order sensor surrogate; no particular sensor,
specimen, environment or physiological system is identified.

For constant heating with a=C/G and b=tau_s, theta=(P/G)(1−exp(−t/a));
y=(P/G)[1−(a exp(−t/a)−b exp(−t/b))/(a−b)]. The a=b limit is
y=(P/G)[1−(1+t/a) exp(−t/a)]. The pulse response is a difference of shifted
step responses. P=0 yields a blank trace. Direct theta with G=0 gives theta=P t/C;
with finite tau_s, y=(P/C)[t−tau_s(1−exp(−t/tau_s))].

Naive absorbed-power estimator: C*y(t)/t. Calibrated positive control:
P_hat=y(t)/r(t), where r is the analytic sensor rise per unit constant power
under independently known C,G,tau_s; evaluate at10,30,60s.
Exact rival/identifiability control: (P,C,G)→a(P,C,G) for a=1/2,2,10 leaves
theta,y unchanged. Temperature alone does not give absolute power without
an external heat-capacity or known-input calibration.

## Frozen gates

1. RK4 piecewise pulse integration at dt=.1,.05,.025s agrees with exact theta,y
   at every stored step to<1e-7K at the finest step; report errors and refinement.
   Switch input exactly at120s, avoiding a mixed-stage switching artifact.
2. Each finite-window naive estimate lies below .2W and the three differ;
   calibrated estimates at10,30,60s differ from .2W by<1e-12W.
3. Scaled parameter traces agree to<1e-12K on0–400s; blank is exactly zero.
4. a=b branch and G=0 finite-sensor branch agree with independent RK4 to<1e-7K
   at dt=.025s for a120s constant pulse. No singular formula is silently evaluated.
5. Independently trapezoid-integrated thermal budget C theta(t)=integralPdt−
   integralG theta dt has maximum residual<1e-7J for the .025s exact trace;
   trapezoid integration of the discontinuous P column is not used acrossswitch.
6. Save compact exact trace and comparison CSV, convergence, source/contract/code
   hashes, JSON, SVG/PNG and interpretation with conceptual resistor/blank/sensor
   calibration design. A duration-dependent corrected result would falsify this
   particular constant-P transfer model or expose miscalibration, not identify
   its replacement automatically. No next round runs before advisor review.
