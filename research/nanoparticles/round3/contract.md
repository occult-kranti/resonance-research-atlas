# Nanoparticles N3 frozen contract — relaxation mechanism discrimination

Frozen after N2 independent admission, before implementation/execution.
Project hypothesis NP-H3: calibrated frequency and held-out viscosity observations
can discriminate a single effective Debye response from a declared two-population
mixture that is indistinguishable at one calibration frequency. This is a project
model-discrimination hypothesis, not a new law or a claim to identify actual particles.

## Two distinct candidate populations

T=298K, kB=1.380649e-23J/K (exact SI), hydrodynamic diameter dh=50e-9m;
eta=.001,.002,.005,.01Pa*s; hypothetical tauN=.001s and chi0=.02 dimensionless.
tauB=pi*eta*dh³/(2kB*T). Fixed spherical hydrodynamic volume, Newtonian viscosity,
temperature and susceptibility are assumptions, not measured material properties.

Candidate A: chiA=chi0/(1+i omega tau_eff), tau_eff^-1=tauB^-1+tauN^-1.
Candidate B: chiB=(chi0/2)/(1+i omega tauB)+(chi0/2)/(1+i omega tauN).
B represents two different positive-response populations; it is NOT the same
particle's parallel-channel law written another way. Use chi''=−Im(chi)>=0.

For A, f_eff=1/(2pi tau_eff)=a/eta+b. Fit a,b on the first two viscosities,
then predict the other two without refitting. For B, tau_app=chi''/(omega chi').
Fit one Debye response to B's complex value at exactly1kHz using
tau_fit=tau_app(1kHz) and chi0_fit=chi'(1+(omega*tau_fit)²). The complex value
matches there but is tested at held-out10Hz–1MHz,1001 log-spaced points.

## Frozen gates

1. SI tauB doubles when viscosity doubles; effective rates and two-viscosity fit
   predict held-out f_eff to relative error<1e-12; report coefficients with units.
2. A's tau_app stays equal to tau_eff across the grid to relative error<1e-12.
3. B's tau_app remains between tauB and tauN and strictly decreases with frequency
   for every unequal pair; independently evaluate its rational weighted-mean
   expression with maximum relative agreement error<1e-12.
4. One-frequency fitted Debye response matches B at1kHz to relative complex error
   <1e-12. For baseline eta=.001 only, its held-out maximum relative error must
   exceed.05. Other viscosities are reported without assuming the same threshold.
5. Equal-time rival control tauB=tauN collapses B exactly to one Debye within
   relative error1e-12. Zero susceptibility gives zero response.
6. Save source/contract/code hashes, parameters, compact frequency/viscosity CSV,
   JSON, SVG/PNG and detailed interpretation. A phase-calibration error,
   aggregation and changing size/concentration are rivals for a future empirical
   test; this numerical exercise does not rule them out.

Sources: Rosensweig2002 DOI10.1016/S0304-8853(02)00706-0 for weak-field relaxation;
Goto et al.2025 DOI10.1039/D5NR00722D for structure-dependent empirical comparisons.
The source's internally problematic prose claiming fpeak proportional to viscosity
is not used as evidence of direction; derive inverse-viscosity scaling explicitly.
No nanoparticle synthesis, exposure, clinical inference or next-round execution.
