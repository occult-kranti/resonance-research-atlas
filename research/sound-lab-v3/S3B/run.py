from pathlib import Path
import sys,json,tempfile,subprocess
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from common import *
from scipy.io import wavfile
from fit_recording import analyze,read_recording
from intake_v2 import run as intake
p=Path(__file__).parent;actual=8016;header=8000;t=np.arange(16032)/actual;y=.2*np.exp(-4*t)*np.cos(2*np.pi*500*t);pcm=np.round(y*32768).astype(np.int16);decoded=pcm.astype(float)/32768
wavfile.write(p/'wrong_header.wav',header,pcm);csv(p/'correct_time.csv',['time_s','amplitude_FS'],np.column_stack([t,decoded]));tn=np.arange(16000)/8000;wavfile.write(p/'null8000.wav',8000,np.round(.2*np.exp(-4*tn)*np.cos(2*np.pi*500*tn)*32768).astype(np.int16));wavfile.write(p/'reference.wav',header,np.round(.1*np.cos(2*np.pi*1000*t)*32768).astype(np.int16))
files=['wrong_header.wav','correct_time.csv','null8000.wav','reference.wav'];records=[];rows=[]
with tempfile.TemporaryDirectory() as tmp:
    temp=Path(tmp)
    ref=intake(p/'reference.wav',temp/'ref',1000,.05,.8,provenance='synthetic_generated');scale=1000/ref['frequency_Hz'];tc=np.arange(len(pcm))/header/scale;csv(p/'reference_corrected.csv',['time_s','amplitude_FS'],np.column_stack([tc,decoded]));files.append('reference_corrected.csv')
    for name in ['null8000.wav','wrong_header.wav','correct_time.csv','reference_corrected.csv']:
        r=intake(p/name,temp/name.replace('.','_'),500,.05,.8,provenance='synthetic_generated');records.append(r);alphaTarget=4*8000/8016 if name=='wrong_header.wav' else 4;fTarget=500*8000/8016 if name=='wrong_header.wav' else 500;assert abs(r['alpha_per_s']-alphaTarget)<.01 and abs(r['frequency_Hz']-fTarget)<.01;rows.append([r['alpha_per_s'],r['frequency_Hz'],r['normalizedResidual'],alphaTarget,fTarget]);_,trace=analyze(p/name);csv(p/(name.replace('.','_')+'_fit.csv'),['time_s','decoded_FS','fit_FS','residual_FS'],trace);files.append(name.replace('.','_')+'_fit.csv')
    badtime=t.copy();badtime[100]+=.00002;csv(temp/'nonuniform.csv',['time_s','amplitude_FS'],np.column_stack([badtime,decoded]));badamp=decoded.copy();badamp[100]=np.nan;csv(temp/'nan.csv',['time_s','amplitude_FS'],np.column_stack([t,badamp]));bad=[]
    cases=[('nonuniform',temp/'nonuniform.csv',.05,0),('nonfinite',temp/'nan.csv',.05,0),('negative_window',p/'wrong_header.wav',-.1,0),('unavailable_channel',p/'wrong_header.wav',.05,1)]
    for name,src,start,ch in cases:
        before=sha(src)
        try:intake(src,temp/('reject_'+name),500,start,.8,channel=ch);raise AssertionError('Invalid case was accepted')
        except ValueError as exc:
            expected={'nonuniform':'uniform','nonfinite':'nonfinite','negative_window':'Invalid fit window','unavailable_channel':'Channel unavailable'}[name]
            assert expected in str(exc),(name,str(exc))
            bad.append({'case':name,'rejected':True,'reason':str(exc),'expectedReasonSubstring':expected,'sourceSHA256Before':before,'sourceSHA256After':sha(src),'sourceUnchanged':before==sha(src)})
    assert all(r['sourceUnchanged'] for r in bad)
assert abs(records[1]['alpha_per_s']/records[1]['frequency_Hz']-records[2]['alpha_per_s']/records[2]['frequency_Hz'])<1e-5
writejson(p/'intake_results.json',{'fits':records,'reference':ref,'invalidCases':bad});writejson(p/'clock_correction.json',{'estimatedScale':scale,'knownFixtureScale':8016/8000,'conditionalIndependentReference_Hz':1000,'rule':'corrected_time=header_time/(known_reference_Hz/fitted_reference_Hz)','requiredPremise':'Reference frequency independently known; not established by this generated file'});csv(p/'fits.csv',['alpha_per_s','frequency_Hz','normalized_residual','predicted_alpha_per_s','predicted_frequency_Hz'],rows)
metrics={'apparent_frequency_Hz':records[1]['frequency_Hz'],'apparent_alpha_per_s':records[1]['alpha_per_s'],'correct_time_frequency_Hz':records[2]['frequency_Hz'],'correct_time_alpha_per_s':records[2]['alpha_per_s'],'reference_estimated_clock_scale':scale,'reference_corrected_frequency_Hz':records[3]['frequency_Hz'],'reference_corrected_alpha_per_s':records[3]['alpha_per_s'],'reference_boundary_flag':('near_search_bound' in ref['flags']),'invalid_cases_rejected':len(bad),'identical_amplitudes':bool(np.array_equal(read_recording(p/'wrong_header.wav')[1],read_recording(p/'correct_time.csv')[1]))}
fig,ax=plt.subplots(1,2,figsize=(9,4));labels=['Correct null','Wrong header','Correct times','Reference correction'];ax[0].bar(range(4),[r[1] for r in rows]);ax[0].set(ylim=(498.5,500.3),ylabel='Fitted frequency (Hz)',title='Same sample values, different clock premise');ax[1].bar(range(4),[r[0] for r in rows]);ax[1].set(ylim=(3.986,4.004),ylabel='Fitted amplitude decay (s⁻¹)',title='Absolute decay shares the clock error');
for a in ax:a.set_xticks(range(4),labels,rotation=25)
savefig(fig,p/'figure.svg')
finish(p,metrics,'A wrong timebase changes fitted frequency and decay together without changing samples; an independently known reference can correct this synthetic clock error.',[{'control':'Wrong header with low residual','outcome':'accepted file format but wrong absolute physical parameters'},{'control':'Constant reference alpha≈0','outcome':'search-bound flag retained'},{'control':'Malformed time/channel/window/amplitude','outcome':'four cases rejected without modifying raw input'}],'''# S3B — preserved bytes still need a time scale

The generated WAV declares 8000 samples/s while its synthetic signal was sampled at 8016 samples/s. On header time, exactly the same model has frequency and amplitude-decay rate multiplied by 8000/8016. Their ratio is unchanged. Correct-timestamp CSV contains identical decoded amplitudes and recovers the declared true fixture parameters. A correct8000 null excludes a generic importer defect.

The independently known1000 Hz reference is a conditional calibration example. Its fitted frequency gives a clock-scale factor and corrected timestamps recover the original500 Hz and4 s^-1. The reference's alpha≈0 boundary flag remains in metadata. A tone generated by the same uncertain clock does not establish an independent calibration reference. Neither a WAV header nor reported capture settings certify a physical timebase.

Four malformed acquisition cases are rejected while preserving raw hashes. Valid format, source integrity and low residual are useful admission checks, but each is weaker than physical calibration. The next question should add an independent phase/spatial observable or freeze the practical bench's repeat/reference strategy, rather than infer hidden material properties from one clean trace.
''',files+['intake_results.json','clock_correction.json','fits.csv','figure.svg','run-attempt1.py.txt','failure-log.md','run-before-review.py.txt','results-before-review.json','intake-results-before-review.json','manifest-before-review.json','../fit_recording.py','../intake_v2.py'])
