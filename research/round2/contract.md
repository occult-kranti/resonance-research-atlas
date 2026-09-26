# Round 2 frozen contract — what does a spectral peak measure?

Written before implementation and execution, 2026-09-26 UTC. Advisor selected this
question after independently reviewing Round 1: energy closure did not identify
a unique measurement-to-mechanism map. No human or Earth-cavity model is claimed.

## Model and parameters

x''+2 gamma x'+omega0² x=d(t), x in m, d in m/s²; omega0=2 pi*8 rad/s.
H_x(omega)=1/(omega0²−omega²+i 2 gamma omega), units s²;
H_v=i omega H_x, units s. Two-sided angular-frequency PSD convention:
variance=(1/(2 pi)) integral S(omega) d omega. Unit white acceleration intensity
S_d=1 m²/s³ is an idealized mathematical input, not a laboratory prescription.

For white forcing S_x=|H_x|² S_d and S_v=omega²|H_x|² S_d.
Baseline gamma=5 s⁻¹; sweep gamma=5,20,omega0/sqrt(2),40,60 s⁻¹.
The displacement maximum is at sqrt(max(omega0²−2 gamma²,0)); the velocity
maximum is at omega0 for positive gamma. Poles are −gamma±sqrt(gamma²−omega0²).
Changing the measured variable from x to v does not change those poles.

Frequency grid: 0–20 Hz inclusive, 20001 points (df=0.001 Hz).
Unknown-source ambiguity: model 1 f0=8 Hz,gamma=5 s⁻¹, S_d1=1;
model 2 f0=10 Hz,gamma=8 s⁻¹, S_d2=|H1|²/|H2|².
Then S_x1=S_x2 exactly as functions, despite different poles. This construction
asserts a mathematical source PSD, not a measured mechanism.

Known-source positive control: exact synthetic displacement PSD of model 1,
frequencies 1,4,8,12,18 Hz. Fit reciprocal PSD as polynomial a omega^4+b omega²+c.
For calibrated unit white forcing a=1, b=4 gamma²−2 omega0²,c=omega0^4.
Recover omega0=c^(1/4), gamma=sqrt((b+2 omega0²)/4). Use scaled least squares
to avoid avoidable numerical conditioning loss. No stochastic error in this round.

## Frozen acceptance tests

1. Predicted and grid-measured displacement and velocity peaks agree to <=0.0011 Hz
   for all five damping cases. Strong damping displacement peak is 0 Hz.
2. Computed poles are independent of whether displacement or velocity is reported;
   H_v=i omega H_x residual <=1e-12 in SI numerical magnitudes.
3. Unknown-source compensation produces positive finite S_d2 over the grid,
   nonidentical poles, and relative output-PSD disagreement <=1e-12.
4. Known-source recovery relative errors in f0 and gamma <=1e-9.
5. Source-only control: multiply baseline forcing PSD by
   1+100 exp(−0.5*((f−12 Hz)/0.25 Hz)²). Output peak must move by >1 Hz
   while the transfer-function poles remain unchanged. This is colored forcing,
   not a changed intrinsic oscillator frequency.
6. Save exact parameters, grid, CSV, JSON, and a labeled SVG/PNG two-panel figure.

## Limits

Ideal source spectra have no finite-sample measurement noise here. A peak shift
does not by itself identify a physiological, environmental, or intrinsic frequency
shift. The ideal spherical Earth formula c sqrt(l(l+1))/(2 pi R) belongs to a
different electromagnetic boundary-value model and is not used to calibrate this
mechanical surrogate. Finite conductivity, cavity structure, sources and sensors
would require independent modeling. Round 3 is not executed before advisor review.
