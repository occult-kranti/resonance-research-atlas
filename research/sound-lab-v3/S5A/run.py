from pathlib import Path
import sys,json,tempfile,csv as csvlib
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from common import *
from scipy.io import wavfile
from intake_v2 import run as intake
p=Path(__file__).parent;c=json.loads((p/'contract.json').read_text());fs=8000;t=np.arange(16000)/fs;gains=.12+.12*np.random.default_rng(206).uniform(size=16);orders=c['parameters']['orders'];allfits=[];rows=[];contrasts={};files=[];rivals=[];plan=[]
# Plan written before generating any trial samples. Its public key is intentionally not blind.
for j,label in enumerate(orders['balanced']):plan.append({'trial_id':f'T{j+1:02d}','order':j,'condition_code':label,'block':j//4,'nominal_frequency_Hz':500,'tap_time_s':0,'fit_start_after_tap_s':.05,'fit_stop_after_tap_s':.8})
writejson(p/'preregistration.json',{'studyType':'synthetic dryrun and proposed household protocol','physicalStudyRun':False,'primaryObservable':'B-minus-A mean recorded-channel amplitude-decay rate','orderedTrials':plan,'expectedPrimaryTrialCount':16,'allTrialsRetained':True,'excludedTrialsReported':True,'frequency_Hz':500,'fitWindowAfterTap_s':[.05,.8],'scope':'A future actual study must create a separate preregistration after an independent pilot chooses its mode/window; never overwrite this synthetic plan','conditionKeyPublic':True,'controls':['silence baseline','untouched/touch support comparison','unchanged-position repeat','recording gain settings','clock/reference provenance'],'decisionRule':'Report descriptive contrast with every exclusion; no material or biological causal conclusion from the contrast alone'})
writejson(p/'condition-key.json',{'A':'untouched spoon support (proposed physical condition)','B':'light finger touch on spoon support/object (proposed physical condition)','blinding':'Public synthetic demo; operator cannot be blind to touching; masked future analyst needs independently held key'})
with (p/'trial-template.csv').open('w') as stream:
    writer=csvlib.writer(stream);writer.writerow(['trial_id','order','condition_code','recording_path','source_sha256','tap_time_s','device','gain_processing','clock_reference','notes'])
    for row in plan:writer.writerow([row['trial_id'],row['order'],row['condition_code'],'','','','','','',''])
with tempfile.TemporaryDirectory() as tmp:
    temp=Path(tmp)
    for ordername,labels in orders.items():
        for delta in [2,0]:
            casename=ordername+('_effect' if delta else '_null');folder=p/casename;folder.mkdir(exist_ok=True);casefits=[]
            for j,label in enumerate(labels):
                b=int(label=='B');alpha=4+delta*b-.08*j;y=gains[j]*np.exp(-alpha*t)*np.cos(2*np.pi*500*t);pcm=np.round(y*32768).astype(np.int16);path=folder/f'T{j+1:02d}.wav';wavfile.write(path,fs,pcm);files.append(path.relative_to(p).as_posix());r=intake(path,temp/f'{casename}_{j}',500,.05,.8,provenance='synthetic_generated');r.update({'case':casename,'trial_id':f'T{j+1:02d}','order':j,'condition_code':label,'trueRecordedAlpha_per_s':alpha,'inputGain_FS':gains[j],'rawPath':path.relative_to(p).as_posix()});allfits.append(r);casefits.append(r);assert r['status']=='fit' and abs(r['alpha_per_s']-alpha)<.01;rows.append([len(allfits)-1,j,b,delta,alpha,r['alpha_per_s'],r['frequency_Hz'],r['normalizedResidual']])
                if casename=='balanced_effect':
                    yr=gains[j]*np.exp(-4*t)*np.exp(.08*j*t)*np.exp(-2*b*t)*np.cos(2*np.pi*500*t);pr=np.round(yr*32768).astype(np.int16);error=float(np.max(np.abs(yr-y)));same=bool(np.array_equal(pr,pcm));assert error<1e-12 and same;rivals.append({'trial_id':r['trial_id'],'condition_code':label,'maxPrequantizationDifference_FS':error,'PCMidentical':same})
                    if j==1:wavfile.write(p/'condition_rival.wav',fs,pr)
                if casename=='balanced_effect' and j==0:(p/'example-fit.csv').write_bytes((temp/f'{casename}_{j}.csv').read_bytes())
            contrast=float(np.mean([r['alpha_per_s'] for r in casefits if r['condition_code']=='B'])-np.mean([r['alpha_per_s'] for r in casefits if r['condition_code']=='A']));contrasts[casename]=contrast;assert abs(contrast-c['acceptance']['predictedContrasts_per_s'][casename])<.005
writejson(p/'trial-results.json',allfits);writejson(p/'rival-identities.json',rivals);csv(p/'trial-fits.csv',['trial_index','order','condition_B','physical_delta_per_s','recorded_true_alpha_per_s','fitted_alpha_per_s','fitted_frequency_Hz','normalized_residual'],rows)
metrics={name+'_contrast_per_s':value for name,value in contrasts.items()};metrics.update({'max_trial_alpha_error_per_s':max(abs(r['alpha_per_s']-r['trueRecordedAlpha_per_s']) for r in allfits),'trials_fitted':len(allfits),'rival_identical_trials':sum(r['PCMidentical'] for r in rivals),'rival_max_difference_FS':max(r['maxPrequantizationDifference_FS'] for r in rivals)})
fig,ax=plt.subplots(1,2,figsize=(10,4));names=list(contrasts);ax[0].bar(range(4),list(contrasts.values()),color=['#ad6143','#326e75','#ad6143','#326e75']);ax[0].set_xticks(range(4),names,rotation=25);ax[0].set(ylabel='B − A recorded decay (s⁻¹)',title='Counterbalance removes this linear order drift');
for name in ['blocked_effect','balanced_effect']:
    rs=[r for r in allfits if r['case']==name];ax[1].plot(range(16),[r['alpha_per_s'] for r in rs],'o-',label=name)
ax[1].set(xlabel='Trial order (zero based)',ylabel='Fitted recorded decay (s⁻¹)',title='All trials retained; positive and null controls');ax[1].legend();savefig(fig,p/'figure.svg')
finish(p,metrics,'Balanced order cancels the declared linear recording drift in positive and null fixtures; a condition-linked gain rival remains byte-identical.',[{'control':'Blocked zero-effect null','outcome':'false contrast near−.64/s'},{'control':'Condition-linked gain rival','outcome':'not removed by counterbalance; all16PCMsignals identical'}],'''# S5A — preregister a modest household question

The practical question is whether lightly touching the spoon changes the recorded-channel decay under a fixed phone/support setup. The public synthetic plan fixes16 trial IDs, order, condition codes, nominal frequency, window and reporting rule before generation. It is not a blinded physical study. The operator necessarily knows whether the object is touched; a future masked analyst needs a separately held key.

Every generated trial passes through the protected intake. The blocked schedule's linear acquisition drift biases a true2 s^-1 contrast toward1.36 and gives a false−.64 contrast under the zero-effect null. The ABBA/BAAB schedule balances condition means in trial index, returning2 and0 respectively. This exact cancellation belongs to the linear drift model; it is not a guarantee against arbitrary physical drift.

The same balanced positive-effect samples arise from zero physical condition effect combined with condition-dependent recording gain exp(−2Bt). All16 rival PCM arrays are identical. Repetition and counterbalancing cannot distinguish causes that produce identical data. The result therefore stays a recorded-channel comparison, with support, microphone processing and calibration documented.

All64 validation WAVs, aggregate fits, source hashes, one decoded fit trace, a public condition key and a blank acquisition CSV are retained. Detailed per-trial traces are reproducible temporary outputs. These files are analysis fixtures, not listening presets. Next: execute the frozen plan through a batch admission/reporting path, preserve failed files and withhold completion if planned trials are absent.
''',files+['condition_rival.wav','preregistration.json','condition-key.json','trial-template.csv','trial-results.json','rival-identities.json','trial-fits.csv','example-fit.csv','figure.svg','../fit_recording.py','../intake_v2.py'])
