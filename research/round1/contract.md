# Round 1 frozen contract — passive coupled resonators

Contract written before the solver and before production execution, 2026-09-26 UTC.
This is a classical mechanical analogy; its parameters do not describe a human body,
Earth's cavity, a treatment device, an electrical coil, or an antigravity system.

## Question and admitted statement

Can energy transfer and a resonant amplitude increase occur while a passive linear
system obeys an explicit input-work minus dissipation budget? Forward calculation
uses the equations below. Reverse reconstruction asks what would be needed to
infer extra energy from a growing output: stored initial energy, all input work,
and loss terms must first be resolved within numerical or measurement uncertainty.

Only this round is authorized for this implementation. A later round requires a
new advisor decision based on these outputs. These are known mechanics, not a
claim of a new law or a proof about biological effects.

## Frozen mathematical model and units

q=(q1,q2) in m; v=qdot in m/s; t in s. The state space is R^4, with no spatial
boundary or continuum limit. M qdd + R qd + K q = B u,

- M=diag(1,1) kg, positive definite.
- k0=(2 pi * 2)^2=157.91367041742973 N/m (ground spring stiffness).
- kc=40 N/m (coupling spring stiffness).
- K=[[k0+kc,-kc],[-kc,k0+kc]] N/m, positive definite.
- R=diag(c,c), c=0.4 kg/s in the baseline, positive semidefinite.
- B=(1,0)^T, dimensionless; scalar external input u=0.1 sin(2 pi f t) N.
- Baseline f=2 Hz; start at q=v=0; duration 20 s; dt=0.002 s.
- Energy E=0.5 v^T M v + 0.5 q^T K q, in J.
- Input power P_in=u B^T v, in W; loss power P_loss=v^T R v, in W.
- Integrals W_in and D both start at zero, in J. Input work is signed.
- Fixed reporting reference E_star=1 J; no physical calibration is inferred.
- Endpoint relative closure scale is max(|W_in(T)|,E(0),E(T),D(T),1e-12 J).
  Absolute closure is always reported, including zero states; this scale is a
  reporting denominator, not an adjustable physical energy calibration.

With constant symmetric M,K, dE/dt=v^T(M qdd+Kq)
=u B^T v-v^T Rv. Thus E(t)-E(0)=W_in(t)-D(t).
There are two undamped normal-mode frequencies: sqrt(k0/m)/(2 pi) and
sqrt((k0+2kc)/m)/(2 pi). They are consequences of the parameters, not fitted data.

## Numerical method, outputs, and acceptance tests

The deterministic solver will use classical fourth-order Runge–Kutta on the
augmented state (q1,q2,v1,v2,W_in,D). No randomness, adaptive fitting, or hidden
normalization is used. Work and dissipation use the same RK stages as motion.
Numerical closure is a diagnostic; independent analytic limits guard against
coordinated implementation errors. The analytic response uses the complex linear
system (K-omega^2 M+i omega R)Q=B F and is checked independently against time
integration. This round assumes a sinusoidal drive and a linear passive system.

1. Baseline budget: maximum |E-E0-W_in+D| < 1e-6 J at dt=0.002 s.
2. Undriven undamped: q0=(0.01,0) m, v0=(0,0) m/s, c=0, F=0;
   maximum relative energy drift < 1e-5; analytic normal-mode displacement error
   < 1e-7 m.
3. Undriven damped: same initial state with c=0.4; energy cannot rise by more
   than 1e-12 J between stored steps, and E_final < E_initial.
4. Zero coupling: kc=0, initial rest and baseline drive; q2=v2 remain exactly
   zero within 1e-14 in their SI units.
5. Zero input and rest: all motion, work, and dissipation remain exactly zero.
6. Off resonance: baseline drive at 3.5 Hz; final-5-second RMS displacement of
   mass 1 must be below the 2 Hz baseline. This is a comparison for these
   parameters only, not a universal resonance theorem.
7. Convergence: baseline dt=0.004,0.002,0.001,0.0005 s. The maximum closure
   residual must decrease at each refinement. Endpoint state errors relative
   to dt=0.0005 must decrease; ratios are reported without demanding an exact
   floating-point asymptotic order.
8. Reversibility: c=F=0, initial q=(0.01,-0.004) m,
   v=(0.03,-0.02) m/s; evolve 5 s, reverse velocities, evolve 5 s. Final q
   differs from original q and final v from negative original v by <1e-7 in
   their respective SI units. With damping this symmetry is not claimed.
9. Sign symmetry: with damping and drive, simultaneous negation of initial q,v
   and drive sign negates q,v; E,W_in,D remain unchanged to 1e-12 in SI units.
10. Independent steady-state check: integrate at f=2 and 3.5 Hz for 60 s with
    dt=0.002 s; fit sine/cosine coefficients on the final 10 s and compare mass
    1 and mass 2 amplitudes to the complex solution, relative error < 1e-3.
11. Frequency sweep: analytic amplitude and mean-power curves over 0.5–4 Hz,
    701 points, for c=0.2,0.4,0.8,2.0 kg/s; report power closure, finite values
    and nonnegative mean dissipation; maximum absolute mean-power closure must
    be <1e-12 W. A c=0 response is singular at exact modal
    frequencies, so no finite steady response is asserted there.
12. Independent wrong-model control: omit D from the baseline budget and show
    its endpoint residual exceeds the correct residual by at least 1000x and
    exceeds 1e-4 J. This demonstrates that measuring stored energy alone is
    insufficient for an input-output energy claim.

CSV outputs contain sampled time histories, analytic frequency sweeps, and
convergence data with units in column names. JSON records parameters, controls,
test results, versions, and source/contract hashes. Plots show energy closure,
frequency response, convergence, and the conservative analytic comparison.

## Limits and interpretation rules

Discretization is the relevant numerical approximation; there is no Monte Carlo
sampling uncertainty. Frequency-grid resolution is distinct from integration
error. Input, damping and constitutive assumptions are exact model premises;
they are not empirical estimates. Floating-point results do not establish an
all-time theorem. A linear mechanical model cannot establish healing, a human
single frequency, free energy, antigravity, or any occult claim. External driving
can increase stored energy without violating passivity. Coupling transfers
energy internally; it creates no net energy term.
