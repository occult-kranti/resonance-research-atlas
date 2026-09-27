from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from common import *
from scipy.io import wavfile
from fit_recording import analyze
p=Path(__file__).parent;fs=8000;t=np.arange(fs*2)/fs;base=.2*np.exp(-4*t)*np.cos(2*np.pi*500*t)
signals={'clean':base,'overlap':base+.06*np.exp(-1.5*t)*np.cos(2*np.pi*512*t),'gain_drift':base*np.exp(2*t),'true_alpha2':.2*np.exp(-2*t)*np.cos(2*np.pi*500*t),'noise':base+np.random.default_rng(104).normal(0,.001,len(t))}
rows=[];records=[];files=[]
for j,(name,y) in enumerate(signals.items()):
    wavfile.write(p/(name+'.wav'),fs,np.round(y*32768).astype(np.int16));files.append(name+'.wav')
    for w,(start,stop) in enumerate([(.05,.8),(.2,1.2)]):
        r,trace=analyze(p/(name+'.wav'),start=start,stop=stop);r['case']=name;r['evidenceType']='actualbytes_generated_PCM';records.append(r);rows.append([j,w,r['alpha_per_s'],r['frequency_Hz'],r['normalizedResidual'],int(bool(r['flags']))]);csv(p/f'{name}_{w}.csv',['time_s','decoded_FS','fit_FS','residual_FS'],trace);files.append(f'{name}_{w}.csv')
        if name in ['gain_drift','true_alpha2']: assert abs(r['alpha_per_s']-2)<.01
err=float(np.max(np.abs(signals['gain_drift']-signals['true_alpha2'])));identical=(p/'gain_drift.wav').read_bytes()==(p/'true_alpha2.wav').read_bytes();assert err<1e-12 and identical
writejson(p/'intake_results.json',records);csv(p/'fits.csv',['case_index','window_index','alpha_per_s','frequency_Hz','normalized_residual','has_flags'],rows)
metrics={'ambiguity_prequantization_max_FS':err,'ambiguous_PCM_identical':identical,'gain_drift_apparent_alpha_per_s':records[4]['alpha_per_s'],'overlap_alpha_early_per_s':records[2]['alpha_per_s'],'overlap_alpha_late_per_s':records[3]['alpha_per_s'],'overlap_residual_early':records[2]['normalizedResidual'],'noise_residual_late':records[9]['normalizedResidual'],'flagged_fits':sum(bool(r['flags']) for r in records),'fits_total':len(records)}
fig,ax=plt.subplots(1,2,figsize=(10,4));names=list(signals)
for w in range(2):
    ax[0].plot(np.arange(5)+w*.08,[rows[2*j+w][2] for j in range(5)],'o',label=['Early window','Later window'][w]);ax[1].plot(np.arange(5)+w*.08,[rows[2*j+w][4] for j in range(5)],'o')
for a in ax:a.set_xticks(range(5),names,rotation=25)
ax[0].axhline(4,ls=':',color='gray');ax[0].set(ylabel='Fitted amplitude decay (s⁻¹)',title='A fit cannot distinguish identical samples');ax[0].legend();ax[1].axhline(.05,ls=':',color='black');ax[1].set(ylabel='Normalized fit residual',title='Residual flags catch only some failures');savefig(fig,p/'figure.svg')
finish(p,metrics,'Nearby modes and noise can raise residuals, but exponential recording gain is byte-identical to a different decay and passes the same fit checks.',[{'control':'Gain drift versus true alpha2','outcome':'exact observational ambiguity'},{'control':'Single-mode overlap fit','outcome':'model mismatch flagged'},{'control':'All low-residual fits are intrinsic damping','outcome':'rejected by byte-identical gain-drift counterexample'}],'''# S2B — a useful fitter is not a material identifier

Five generated PCM cases pass through the frozen S2A importer with two declared fit windows. The nearby second mode gives a large residual and window-dependent fitted decay. Additive noise grows more important later in a decaying record. All values and flags are saved, including cases that do not cross the fixture's 5% residual flag.

The strongest control is exact: exp(2t) times a 4 s^-1 decay equals a 2 s^-1 decay at every time. Their PCM files are byte-identical. Both receive the same low-residual fit near 2 s^-1; no statistic of that recording alone can decide whether gain changed or physical decay changed. The exp(2t) gain is a constructed counterexample, not a universal model of phone AGC.

A low-material tap protocol therefore requires gain settings, repeat acquisitions, support controls and a modest interpretation: recorded-channel decay under a declared model. Two windows and residuals can reject some data but cannot certify intrinsic damping. The next useful question concerns adding independent geometry/phase observations instead of repeatedly fitting the same scalar trace.
''',files+['fits.csv','intake_results.json','figure.svg','../fit_recording.py'])
