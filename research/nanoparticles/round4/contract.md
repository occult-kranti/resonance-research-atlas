# Nanoparticles N4 frozen contract — counts, sizes and response weights

Frozen before implementation/execution after N3 admission. Project hypothesis
NP-H4: replacing a number-size distribution by one mean size or equal response
weights can bias counts and response predictions even after DC normalization.
This reproduces established moment physics and defines a project validation test;
it does not claim a new particle-count correction or a real material discovery.

Equal-number populations have core diameters40nm,60nm and separately specified
hydrodynamic diameters50nm,70nm. Number weights are(1/2,1/2).
Synthetic common core density rho=5000kg/m³ and core mass concentration
c_mass=.001kg/m³. They are not an identified material or preparation recipe.
Mean core diameter=50nm. Use exact rational core-size moments before converting
nm³ to m³ (factor1e-27).

n_correct=c_mass/[rho*(pi/6)*E(d_core³)] per m³.
n_naive=c_mass/[rho*(pi/6)*E(d_core)³]. Their ratio is1.12.
Core mass fractions are(8/35,27/35). Under a CONDITIONAL dilute weak-field
equilibrium Langevin model with identical core magnetization density, susceptibility
weights are proportional to n_i V_core_i², hence(64/793,729/793).
These are not number fractions; absolute susceptibility and the regime validity
of real40–60nm cores are not asserted.

For a separate conditional locked-moment Brownian spectrum, use
tauB=pi*eta*d_h³/(2kB*T), eta=.001Pa*s,T=298K,kB=1.380649e-23J/K.
No Néel channel is modeled. Normalize chi(omega)/chi(0)=sum weights/(1+iomega*tauB).
Compare correct susceptibility weights with naive equal-number weights over
10Hz–1MHz,1001 log points. Both share their exact omega=0 normalization; no
finite-frequency shape is fitted. The domain is mathematical, not a certified
particle/actuator operating range.

## Frozen gates

1. Fraction arithmetic gives E(d³)=140000nm³, E(d)³=125000nm³,
   count ratio28/25 and distinct exact count/mass/susceptibility weights.
2. SI concentration and all three normalized weights are positive; each weight
   family sums exactly to1; density/mass scaling changes counts as prescribed
   and leaves normalized response weights unchanged.
3. Both candidate normalized spectra are exactly1 atDC. Maximum finite-frequency
   relative complex residual of naive weights exceeds.01; save its location.
4. Relabeling paired core/hydrodynamic populations leaves the response unchanged
   to relative error<1e-12. A monodisperse control collapses both weight models
   to the same single response to relative error<1e-12.
5. Independent combined-rational two-pole expression reproduces the correctly
   weighted complex spectrum to relative error<1e-12. Save moment/weight table,
   CSV, JSON, SVG/PNG, source/contract/code hashes and detailed interpretation.

Improved prospective test: separately measure number-weighted core-size
distribution, core mass, hydrodynamic sizes and phase response; predict held-out
frequencies after DC normalization. Aggregation, shape, nonuniform magnetization
and intensity-weighted size measurements are rivals. No particle synthesis,
clinical exposure, empirical fit or subsequent-round execution occurs here.
