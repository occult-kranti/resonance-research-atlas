from pathlib import Path
import sys,json,csv as csvlib
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from common import *
p=Path(__file__).parent;lam=343/500;k=2*np.pi/lam;a=np.array([1,.6*np.exp(.7j)]);eta=.001;cases=[];raw=[]
def M(x):return np.column_stack([np.exp(-1j*k*np.asarray(x)),np.exp(1j*k*np.asarray(x))])
for frac in [0,.001,.01,.25,.49,.5]:
    mat=M([0,frac*lam]);u,s,v=np.linalg.svd(mat);rank=int(np.linalg.matrix_rank(mat));pred=np.sqrt(np.maximum(0,[2+2*abs(np.cos(2*np.pi*frac)),2-2*abs(np.cos(2*np.pi*frac))]));z=mat@a;noise=eta*u[:,-1];rec={'fraction':frac,'separation_m':frac*lam,'domainDimension':2,'rank':rank,'nullity':2-rank,'sigma_max':float(s[0]),'sigma_min':float(s[1]),'analytic_sigma_max':float(pred[0]),'analytic_sigma_min':float(pred[1]),'inversePerformed':rank==2}
    assert np.max(abs(s-pred))<1e-12
    if rank==2:
        fit=np.linalg.solve(mat,z+noise);err=float(np.linalg.norm(fit-a));expected=float(eta/s[-1]);assert abs(err-expected)<1e-12;rec.update({'coefficientL2Error':err,'predictedError':expected,'condition':float(s[0]/s[1])})
    else:rec.update({'coefficientL2Error':None,'predictedError':None,'condition':None,'kernelWitness':[[1,0],[-1,0]],'kernelResidual':float(np.linalg.norm(mat@np.array([1,-1])))})
    cases.append(rec)
    for j in range(2):raw.append([frac,j,z[j].real,z[j].imag,noise[j].real,noise[j].imag])
positions=np.array([0,lam/4,lam/8]);mat=M(positions);truth=mat@a;drift=truth.copy();drift[1]*=np.exp(.05j);fit2=np.linalg.solve(mat[:2],drift[:2]);predict=mat@fit2;fit3=np.linalg.lstsq(mat,drift,rcond=None)[0];res3=drift-mat@fit3;globalObs=truth*np.exp(.05j);globalFit=np.linalg.lstsq(mat,globalObs,rcond=None)[0];globalRes=float(np.linalg.norm(globalObs-mat@globalFit));held=float(abs(predict[2]-truth[2]));assert held>.005 and globalRes<1e-12
csv(p/'noise_observations.csv',['separation_fraction','channel','true_real','true_imag','noise_real','noise_imag'],raw);csv(p/'phase_observations.csv',['position_m','true_real','true_imag','drift_observed_real','drift_observed_imag','two_sample_prediction_real','two_sample_prediction_imag','three_sample_residual_real','three_sample_residual_imag'],np.column_stack([positions,truth.real,truth.imag,drift.real,drift.imag,predict.real,predict.imag,res3.real,res3.imag]));writejson(p/'cases.json',cases)
with (p/'conditioning.csv').open('w') as stream:
    writer=csvlib.writer(stream);writer.writerow(['separation_fraction','rank','nullity','sigma_min','condition','coefficient_L2_error','predicted_L2_error','inverse_performed'])
    for r in cases:writer.writerow([r['fraction'],r['rank'],r['nullity'],r['sigma_min'],r['condition'],r['coefficientL2Error'],r['predictedError'],r['inversePerformed']])
metrics={'worst_fullrank_condition':max(r['condition'] for r in cases if r['condition'] is not None),'quarterwave_condition':cases[3]['condition'],'worst_coefficient_L2_error':max(r['coefficientL2Error'] for r in cases if r['inversePerformed']),'quarterwave_coefficient_L2_error':cases[3]['coefficientL2Error'],'singular_cases_not_inverted':sum(not r['inversePerformed'] for r in cases),'two_sample_fit_residual':float(np.linalg.norm(mat[:2]@fit2-drift[:2])),'heldout_phase_drift_error':held,'three_sample_residual_L2':float(np.linalg.norm(res3)),'global_phase_residual_L2':globalRes}
fig,ax=plt.subplots(1,2,figsize=(10,4));valid=[r for r in cases if r['inversePerformed']];ax[0].semilogy([r['fraction'] for r in valid],[r['coefficientL2Error'] for r in valid],'o-');ax[0].set(xlabel='Separation / wavelength',ylabel='Coefficient L2 error',title='Fixed observation error .001; spacing controls gain');ax[1].bar(['2-point fit','Held-out point','3-point fit'],[metrics['two_sample_fit_residual'],held,metrics['three_sample_residual_L2']]);ax[1].set(ylabel='Normalized amplitude discrepancy',title='A perfect 2-point fit can miss phase drift');savefig(fig,p/'figure.svg')
finish(p,metrics,'Near-degenerate spacing amplifies bounded noise; a two-point fit hides channel-specific phase drift that a withheld third point reveals.',[{'control':'Zero and half-wavelength inverse','outcome':'not performed; rank1/nullity1'},{'control':'Two-point residual certifies phase stability','outcome':'rejected by heldout sample'},{'control':'Global phase rotation','outcome':'consistent; not falsely treated as channel mismatch'}],'''# S4B — independent does not automatically mean stable

For two complex samples, M* M has eigenvalues2±2|cos(kDelta)|. At zero or half-wavelength separation the inverse is singular, with complex rank1 and nullity1 and kernel[1,-1]. No inverse is reported there; blank conditioning CSV entries mean undefined, not zero error. At quarter wavelength the columns are orthogonal and condition1. Near-degenerate spacing increases noise gain.

The constructed observation perturbation has total complex L2 norm.001 along the weakest left singular vector. Its coefficient error matches eta/sigma_min. This is a worst-direction finite bound, not a measured phone-noise distribution.

A.05-radian phase change in only the second quarter-wave observation can still fit two coefficients exactly. It predicts the withheld lambda/8 observation incorrectly and produces a nonzero three-point residual. A common global phase shift remains consistent at all positions. A third channel therefore tests this failure mode but does not prove a real room is1D or its references calibrated. The practical conclusion is to preregister held-out/repeat controls and withhold coefficient inversion when shared phase is unavailable.
''',['noise_observations.csv','phase_observations.csv','cases.json','conditioning.csv','figure.svg'])
