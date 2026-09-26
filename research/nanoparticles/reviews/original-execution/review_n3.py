from pathlib import Path
import json,math,hashlib
import numpy as np
r=Path('repos/resonance-research-atlas/research/nanoparticles/round3');result=json.loads((r/'results.json').read_text());s=np.genfromtxt(r/'response_spectra.csv',delimiter=',',names=True);pre=json.loads(Path('panel-nano/advisor-N3-precompute.json').read_text())
k=1.380649e-23;T=298;d=50e-9;n=.001;chi=.02
eta=s['viscosity_Pa_s'];w=2*np.pi*s['frequency_Hz'];b=np.pi*eta*d**3/(2*k*T)
# Single combined rational function rather than producer's sum of two transfer calls.
z=chi/2*(2+1j*w*(b+n))/(1+1j*w*(b+n)-w*w*b*n)
saved=s['mixture_chi_real']-1j*s['mixture_chi_loss'];res=float(np.max(abs(z-saved)/abs(z)))
a_expected=k*T/(math.pi**2*d**3);b_expected=1/(2*math.pi*n)
fit=result['fit'];ferr=max(abs(fit['slope_Hz_Pa_s']/a_expected-1),abs(fit['intercept_Hz']/b_expected-1))
preerr=max(abs(a['heldout_10Hz_relative_error']-b['max_held_out_relative_residual']) for a,b in zip(pre['cases'],result['cases']))
# The complete derivative argument establishes monotonicity between any grid points.
proof='For z=ω², τapp=(aτ1+bτ2+z(aτ1τ2²+bτ2τ1²))/(a+b+z(aτ2²+bτ1²)); derivative numerator=−ab(τ1+τ2)(τ1−τ2)². All tested coefficients positive; strictnegative for unequal times.'
assert res<1e-12 and ferr<1e-12 and preerr<1e-12
out={'round':3,'branch':'nanoparticles','status':'accepted','reviewDate':'2026-09-26','independent_methods':['Whole-domain positive-mixture derivative proof','Combined rational susceptibility comparison against every saved spectral row','Closed-form physical slope/intercept versus two-point linear solve','Pre-result independently frozen10Hz residual and fit predictions compared against outputs'],'mixture_combined_rational_max_relative_error':res,'physical_coefficient_max_relative_error':ferr,'precomputed_heldout_residual_max_absolute_difference':preerr,'whole_domain_proof':proof,'source_sha256':{f:hashlib.sha256((r/f).read_bytes()).hexdigest() for f in ['contract.md','sources.md','solver.py','results.json','response_spectra.csv','viscosity_predictions.csv']},'scope':'Two distinct hypothetical population models; single-point rival has unknown amplitude. Known independent DC susceptibility may already discriminate at one complex point.','source_disagreement':'Goto2025 prose fpeak proportional to viscosity not used as directional evidence; derive explicit Brownian inverse scaling from time equation.','empirical_work':'No viscosity, immobilization, phase-reference or particle characterization performed.','next_reason':'Susceptibility mixture amplitudes do not establish particle number fractions; select mass/size-moment and response-weight calibration.'}
(r/'independent-review.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if 'error' in k or 'difference' in k},indent=2))
