# Nanoparticles N1 — frozen contract

Written before implementation/execution. Advisor selection: 2026-09-26.

Project hypothesis NP-H1: within a single-Debye weak-field magnetic model,
the frequency maximizing loss per cycle does not maximize power at fixed field
amplitude and fixed relaxation time. This is an application of known theory;
neither a new law nor demonstrated nanoparticle efficacy is claimed.

## Source and conventions

Rosensweig, *Heating magnetic fluid with alternating magnetic field*, Journal of
Magnetism and Magnetic Materials 252 (2002),169–173,
DOI:10.1016/S0304-8853(02)00706-0, §§2–4 and susceptibility/power equations.
Source researcher and advisor independently read the primary text. Use
H(t)=H_peak cos(omega t), H_peak in A/m, M in A/m; omega=2pi f in rad/s.
With exp(+i omega t), chi=chi'−i chi'', chi''>=0 for this passive model.

Synthetic fixed parameters: chi0=0.02 (dimensionless effective volume
susceptibility), tau=1e-6 s, H_peak=1 A/m. These are declared normalization
parameters, not fitted material properties or a physical exposure prescription.
mu0=4pi*1e-7 H/m is a nominal rounded model constant, not asserted exact modern SI.
No nanoparticle density, size, concentration, synthesis or human system is modeled.

chi'=chi0/(1+x²), chi''=chi0*x/(1+x²), x=omega*tau.
W_cycle=pi*mu0*H_peak²*chi'' J/m³ per cycle.
P=f W_cycle=mu0*chi0*H_peak²/(2tau)*x²/(1+x²) W/m³.
Mathematical x grid: 10^-3 to10^3,1201 logarithmic points, including x=1.
Its full frequency range is mathematical extrapolation only; it does not assert
material validity up to159MHz. The primary model excludes nonlinear hysteresis,
interactions, frequency-dependent source amplitude and changing material state.

## Independent relaxation and passive budget

tau Mdot+M=chi0 H. Storage e=mu0 M²/(2chi0) J/m³;
p_in=mu0 H Mdot W/m³; p_loss=mu0*tau*Mdot²/chi0 W/m³.
Then edot=p_in−p_loss and p_loss>=0. This is the declared passive relaxation
element energy budget, not the complete electromagnetic energy of an apparatus.

Integrate from M(0)=0 for60 cycles at x=.1,1,10. All runs exceed20tau of settling.
Classical RK4 integrates normalized state m=M/(chi0 H_peak), normalized work
and normalized dissipation against theta=omega t. Compare512,1024,2048 steps per
cycle. For the final cycle also independently calculate −mu0 integral M dH by
trapezoidal polygon quadrature. Transient nonclosure is retained: input work minus
loop area equals mu0[HM]_start^end; input work minus dissipation equals delta e.

## Frozen gates

1. On the mathematical sweep, chi''>=0; its maximum is x=1; P increases strictly.
   At x=.001 low-frequency W~x and P~x² ratios differ from their limits by<2e-6;
   at x=1000 P/plateau differs from1 by<2e-6.
2. H_peak=0 and chi0=0 each give zero absorption. Doubling H_peak multiplies
   W and P by4 within this linear model. The zero-tau fixed-f limit has zero loss.
3. Phase ratio chi''/chi'=x with maximum relative error<1e-12.
4. At2048 steps/cycle, final-cycle input work and dissipation match the analytic
   periodic work to relative error<1e-5; normalized maximum all-run passive
   budget residual<1e-5. Sampled cycle nonclosure is reported, not suppressed.
5. Independent loop quadrature error decreases for512→1024→2048; at2048 its
   relative analytic error<2e-6 for all three x cases. Report all errors.
6. Contrasting scan: at fixed f_ref=1/(2pi*tau_ref), varying tau gives a power
   maximum at x=1. No frequency-scan statement may be transferred to this scan.

Outputs: source/contract/solver hashes, compact sweep/convergence/final-cycle CSV,
JSON, precise SVG/PNG figures, detailed interpretation, conceptual measurement
boundary, rejected overinterpretations and next unresolved premise. No N2
computation begins until advisor reviews the completed N1 result.
