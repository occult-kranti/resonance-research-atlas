from pathlib import Path
import gzip
REVIEW = Path(__file__).resolve().parents[1]
NANO = REVIEW.parent

def csv_path(path):
    return path if path.exists() else path.with_suffix(path.suffix + '.gz')

def evidence_bytes(path):
    if path.exists():
        return path.read_bytes()
    return gzip.decompress(path.with_suffix(path.suffix + '.gz').read_bytes())

from pathlib import Path
from fractions import Fraction as F
import math,json,hashlib,numpy as np
r=(NANO / 'round4');j=json.loads((r/'results.json').read_text());s=np.genfromtxt(csv_path(r/'weighted_response.csv'),delimiter=',',names=True);pre=json.loads((REVIEW / 'advisor-N4-precompute.json').read_text())
# Independent central-moment and exact ratio route.
mean=F(50);variance=F(100);third=mean**3+3*mean*variance
assert third==140000 and third/mean**3==F(28,25)
ratio=F(60,40);q=F(1,1)/(1+ratio**6);p=F(1,2)
assert [str(q),str(1-q)]==j['weights']['conditional_susceptibility']
t1,t2=pre['tau_B_s'];w=2*np.pi*s['frequency_Hz'];alpha=float(q)*t2+float(1-q)*t1
# Cancel common two-pole denominator to obtain an independent residual formula.
expected=abs(float(p-q))*w*abs(t2-t1)/np.sqrt(1+(w*alpha)**2)
err=float(np.max(abs(expected-s['relative_complex_residual'])))
count=pre['number_concentration_per_m3'];cerr=abs(j['number_concentration_correct_per_m3']/count-1)
assert err<1e-12 and cerr<1e-12
out={'round':4,'branch':'nanoparticles','status':'accepted','reviewDate':'2026-09-26','independent_methods':['Exact central-moment identity Ed³=mean³+3mean variance+thirdcentralmoment for symmetric40/60 population','Exact sixth-power ratio of susceptibility weights','Cancelled two-pole residual formula over every stored frequency','Pre-result count and selected spectral predictions compared'],'residual_formula_max_absolute_error':err,'number_concentration_relative_error':cerr,'whole_domain_residual':'R(ω)=|p−q|ω|τ2−τ1|/sqrt(1+ω²[qτ2+(1−q)τ1]²), strictlyincreasingforω>0 ifweights/timesdiffer; nofinite-grid extrapolation needed for monotonicity','high_frequency_residual_limit':abs(float(p-q))*abs(t2-t1)/alpha,'source_sha256':{f:hashlib.sha256(evidence_bytes(r/f)).hexdigest() for f in ['contract.md','sources.md','solver.py','results.json','weighted_response.csv','population_weights.csv']},'source_scope':'NH17 arithmeticmeanvolumecorrection; ROS2002 diluteequilibriumLangevinweakfield weighting; core andhydrodynamicsize distinct; allmaterialparametershypothetical','empirical_work':'No mass, density, size-distribution, magnetization or sample spectral measurement performed.','next_reason':'Even corrected particle response requires a calibrated physical drive; select actual OpenSync waveform-to-linear/nonlinear-detector transfer audit.'}
(REVIEW / 'replayed-N4-review.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'residual_formula_error':err,'count_relative_error':cerr,'high_frequency_limit':out['high_frequency_residual_limit']},indent=2))
