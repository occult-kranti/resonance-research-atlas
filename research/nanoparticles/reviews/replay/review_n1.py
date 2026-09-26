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
import numpy as np, json, math,hashlib
r=(NANO / 'round1')
s=np.genfromtxt(csv_path(r/'frequency_sweep.csv'),delimiter=',',names=True)
a=np.genfromtxt(csv_path(r/'final_cycles.csv'),delimiter=',',names=True)
mu=4*math.pi*1e-7; chi=.02; tau=1e-6
x=s['x_omega_tau']; f=s['frequency_Hz']
expected_cycle=math.pi*mu*chi*x/(1+x*x);expected_power=mu*chi/(2*tau)*x*x/(1+x*x)
checks={'sweep_cycle_max_absolute_error_J_per_m3':float(max(abs(s['loss_per_cycle_J_per_m3']-expected_cycle))),'sweep_power_max_absolute_error_W_per_m3':float(max(abs(s['power_W_per_m3']-expected_power))),'dimensional_fW_max_relative_error':float(max(abs(f*expected_cycle-expected_power)/expected_power))}
cases=[]
for q in [.1,1.,10.]:
 b=a[a['x_omega_tau']==q];t=b['time_within_last_cycle_s'];H=b['H_A_per_m'];M=b['M_A_per_m'];theta=2*math.pi*59+q*t/tau
 exact=chi/(1+q*q)*(np.cos(theta)+q*np.sin(theta)-np.exp(-theta/q))
 loop=-mu*np.sum((M[1:]+M[:-1])/2*np.diff(H)); theoretical=math.pi*mu*chi*q/(1+q*q)
 mdot=(chi*H-M)/tau
 work=np.trapezoid(mu*H*mdot,t);loss=np.trapezoid(mu*tau/chi*mdot**2,t);delta=mu/(2*chi)*(M[-1]**2-M[0]**2)
 cases.append({'x':q,'exact_from_rest_M_max_error_A_per_m':float(max(abs(M-exact))),'512_segment_saved_loop_relative_error':float(abs(loop/theoretical-1)),'independent_sampled_budget_residual_J_per_m3':float(work-loss-delta),'independent_sampled_input_relative_error':float(abs(work/theoretical-1))})
print(json.dumps({'checks':checks,'cases':cases},indent=2))
(REVIEW / 'replayed-N1-values.json').write_text(json.dumps({'checks':checks,'cases':cases},indent=2)+'\n')
