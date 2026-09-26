from pathlib import Path
import math,json,hashlib
import numpy as np
from scipy.linalg import expm
r=Path('repos/resonance-research-atlas/research/nanoparticles/round2'); a=np.genfromtxt(r/'thermal_trace.csv',delimiter=',',names=True); result=json.loads((r/'results.json').read_text()); pre=json.loads(Path('panel-nano/advisor-N2-precompute.json').read_text())
C=4.;G=.02;P=.2;tau=10.;tc=C/G
A=np.array([[-G/C,0,P/C],[1/tau,-1/tau,0],[0,0,0.]])
Aoff=A.copy();Aoff[0,2]=0
z0=np.array([0.,0.,1.]);z120=expm(A*120)@z0
states=np.array([(expm(A*t)@z0 if t<=120 else expm(Aoff*(t-120))@z120)[:2] for t in a['time_s']])
errors={'independent_augmented_matrix_exponential_max_error_K':float(max(np.max(abs(states[:,0]-a['specimen_temperature_rise_K'])),np.max(abs(states[:,1]-a['sensor_temperature_rise_K']))))}
q=[]
for t in a['time_s']:
 if t<=120:val=P*(t-tc*(-math.expm1(-t/tc)))
 else:val=P*(120-tc*(-math.expm1(-120/tc)))+G*z120[0]*tc*(-math.expm1(-(t-120)/tc))
 q.append(val)
errors['sampled_quadrature_heat_leak_vs_exact_integral_max_error_J']=float(np.max(abs(a['heat_leak_J']-q)))
errors['independent_exact_thermal_budget_max_error_J']=float(np.max(abs(C*states[:,0]-P*np.minimum(a['time_s'],120)+q)))
errors['precomputed_convolution_vs_result_max_error_K']=max(abs(x['sensor_K']-y['sensor_rise_K']) for x,y in zip(pre['points'],result['duration_comparisons']))
assert errors['independent_augmented_matrix_exponential_max_error_K']<1e-11
assert errors['independent_exact_thermal_budget_max_error_J']<1e-11
out={'round':2,'branch':'nanoparticles','status':'accepted','reviewDate':'2026-09-26','independent_methods':['Independent integrating-factor convolution frozen before producer results','Augmented3x3 matrix exponential with separate switch propagator compared against all saved trace points','Exact analytic heat-leak integral compared against producer quadrature','Algebraic scale-symmetry proof, with calibrated-capacity positive control'],**errors,'source_sha256':{f:hashlib.sha256((r/f).read_bytes()).hexdigest() for f in ['contract.md','sources.md','solver.py','results.json','thermal_trace.csv','duration_comparison.csv','convergence.csv']},'source_scope':'Skinner2025 inspected heating/cooling, blank, well-mixed limitation; our first-order sensor model is an explicit surrogate, no source-data fit','empirical_work':'None: resistor phantom, thermometer calibration, sample thermometry and uncertainty remain prospective','next_reason':'Calibrating heat input does not identify the particle relaxation mechanism; choose controlled viscosity/phase discrimination next'}
(r/'independent-review.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(errors,indent=2))
