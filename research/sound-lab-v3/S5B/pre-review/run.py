from pathlib import Path
import sys,json,tempfile,copy
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from common import *
from scipy.io import wavfile
from batch_intake import run_batch
p=Path(__file__).parent;planpath=ROOT/'S5A/preregistration.json';plan=json.loads(planpath.read_text());fs,original=wavfile.read(ROOT/'S5A/balanced_effect/T01.wav');wavfile.write(p/'padded_T01.wav',fs,np.concatenate([np.zeros(fs,dtype=np.int16),original]));writejson(p/'padded_T01.json',{'derivedFrom':'../S5A/balanced_effect/T01.wav','originalSHA256':sha(ROOT/'S5A/balanced_effect/T01.wav'),'operation':'prepend exactly8000 zero PCM16 samples; original samples unchanged','sampleRate_Hz':fs,'impact_time_s':1,'evidenceType':'synthetic_generated'})
manifest={'evidenceType':'synthetic_generated','metadata':{'device':'deterministic PCM generator; no physical microphone','gain_processing':'declared S5A synthetic condition/order model','geometry':'synthetic waveform; proposed spoon bench not run','clock_reference':'declared exact8000Hz synthetic timebase','impact_alignment_rule':'fixture impact0; derived padded first trial impact1s'},'trials':[]}
for r in plan['orderedTrials']:
    j=r['order'];rel='padded_T01.wav' if j==0 else f"../S5A/balanced_effect/{r['trial_id']}.wav";manifest['trials'].append({'trial_id':r['trial_id'],'order':j,'condition_code':r['condition_code'],'path':rel,'source_sha256':sha(p/rel),'impact_time_s':1 if j==0 else 0})
variants={'complete':manifest,'missing':copy.deepcopy(manifest),'invalid_trials':copy.deepcopy(manifest),'missing_metadata':copy.deepcopy(manifest),'duplicate_id':copy.deepcopy(manifest),'wrong_condition':copy.deepcopy(manifest),'wrong_impact':copy.deepcopy(manifest)}
variants['missing']['trials'].pop();replacements=['../S2A/case3.wav','../S2A/case4.wav','../S2B/overlap.wav']
for i,rel in enumerate(replacements):variants['invalid_trials']['trials'][i].update({'path':rel,'source_sha256':sha(p/rel),'impact_time_s':0})
variants['invalid_trials']['trials'][3]['source_sha256']='0'*64;del variants['missing_metadata']['metadata']['gain_processing'];variants['duplicate_id']['trials'].append(copy.deepcopy(manifest['trials'][0]));variants['wrong_condition']['trials'][0]['condition_code']='B';variants['wrong_impact']['trials'][0]['impact_time_s']=0
for name,value in variants.items():writejson(p/(name+'-manifest.json'),value)
tracked={str((p/r['path']).resolve()):sha(p/r['path']) for v in variants.values() for r in v['trials']};cases=[];files=['padded_T01.wav','padded_T01.json']+[name+'-manifest.json' for name in variants]
with tempfile.TemporaryDirectory() as tmp:
    temp=Path(tmp);complete=None
    for name in variants:
        try:
            result=run_batch(planpath,p/(name+'-manifest.json'),temp/name)
            if name in ['missing_metadata','duplicate_id']:raise AssertionError('Expected global admission rejection')
            if name=='complete':
                complete=result;assert result['status']=='complete_primary_set' and abs(result['primaryContrast_per_s']-2)<.005
                baseline=json.loads((ROOT/'S5A/trial-results.json').read_text());expected=next(r['alpha_per_s'] for r in baseline if r['case']=='balanced_effect' and r['trial_id']=='T01');assert abs(result['trials'][0]['alpha_per_s']-expected)<.01
                (p/'example-aligned-fit.csv').write_bytes((temp/name/'T01.csv').read_bytes())
            else:
                assert result['status']=='incomplete_primary_set' and result['primaryContrast_per_s'] is None
                if name=='missing':assert result['missingTrialIDs']==['T16']
                if name=='invalid_trials':
                    for i,term in enumerate(['silence','clipping','residual','SHA256']):assert term in ' '.join(result['trials'][i]['flags'])
                if name=='wrong_condition':assert 'Condition code' in ' '.join(result['trials'][0]['flags'])
                if name=='wrong_impact':assert 'silence' in ' '.join(result['trials'][0]['flags'])
            writejson(p/(name+'-batch.json'),result);files.append(name+'-batch.json');cases.append({'case':name,'status':result['status'],'eligibleTrials':result['eligibleTrials'],'primaryContrast_per_s':result['primaryContrast_per_s'],'allReasonsChecked':True})
        except ValueError as exc:
            term={'missing_metadata':'gain_processing','duplicate_id':'Duplicate trial ID'}.get(name);assert term and term in str(exc);cases.append({'case':name,'status':'global_admission_rejected','reason':str(exc),'eligibleTrials':0,'primaryContrast_per_s':None,'allReasonsChecked':True})
    before=sha(temp/'complete/batch-results.json')
    try:run_batch(planpath,p/'complete-manifest.json',temp/'complete');raise AssertionError('Output overwrite permitted')
    except ValueError as exc:assert 'already exists' in str(exc)
    output_unchanged=before==sha(temp/'complete/batch-results.json');assert output_unchanged
assert all(sha(Path(path))==digest for path,digest in tracked.items());writejson(p/'admission-cases.json',cases);writejson(p/'source-hashes.json',{'files':[{'path':str(Path(path).relative_to(ROOT)),'sha256':digest,'unchanged':sha(Path(path))==digest} for path,digest in tracked.items()]})
metrics={'complete_primary_contrast_per_s':complete['primaryContrast_per_s'],'complete_eligible_trials':complete['eligibleTrials'],'aligned_first_trial_alpha_per_s':complete['trials'][0]['alpha_per_s'],'aligned_fit_window_start_s':complete['trials'][0]['absoluteFitWindow_s'][0],'wrong_impact_rejected':True,'incomplete_primary_results_withheld':sum(r['status']=='incomplete_primary_set' and r['primaryContrast_per_s'] is None for r in cases),'global_admission_rejections':sum(r['status']=='global_admission_rejected' for r in cases),'raw_files_preserved':len(tracked),'existing_output_preserved':output_unchanged}
csv(p/'admission.csv',['case_index','eligible_trials','primary_reported'],[[i,r['eligibleTrials'],r['primaryContrast_per_s'] is not None]for i,r in enumerate(cases)]);fig,ax=plt.subplots(figsize=(10,4));ax.bar(range(len(cases)),[r['eligibleTrials'] for r in cases],color=['#326e75']+['#ad6143']*(len(cases)-1));ax.axhline(16,color='black',ls=':');ax.set_xticks(range(len(cases)),[r['case'] for r in cases],rotation=25);ax.set(ylabel='Eligible planned trials',title='Final synthetic dryrun: incomplete plans do not produce a primary contrast');savefig(fig,p/'figure.svg')
finish(p,metrics,'The complete planned set produces its synthetic recorded-channel contrast; missing, rejected or mismatched trials withhold the primary result while preserving all raw files.',[{'control':'Wrong zero impact on padded file','outcome':'rejected as silence; correct1s impact restores fit'},{'control':'Incomplete survivors substituted for primary','outcome':'prevented; primary contrast null'},{'control':'Existing output directory','outcome':'refused without overwrite'}],'''# S5B — final plan-to-report dryrun

The batch tool reads a frozen plan and acquisition manifest. It requires trial IDs/order/condition labels, raw-file hashes, an impact time per file and declared device, gain, geometry, clock and impact-alignment metadata. Those declarations are not authentication or physical calibration. Each valid file passes through the unchanged protected intake.

The first valid trial has1 second of prepended silence and impact_time_s=1. Its absolute fit window becomes1.05–1.8 s and matches the original decay. Assigning impact zero to that same file instead reaches the silence rejection. This directly exercises alignment rather than assuming every recording starts at impact.

Seven suites cover the complete16-trial plan, a missing trial, four specific negative-control replacements, missing metadata, duplicate ID, wrong condition and wrong impact. Every intended rejection reason is asserted. All raw hashes and a preexisting output directory remain unchanged. The four incomplete suites have primaryContrast=null; their explicitly descriptive survivor contrasts are never substituted for the preregistered primary result.

The successful contrast is still a synthetic recorded-channel comparison subject to S5A's identical condition-linked gain rival. No household bench has been run, and no material, biological or consciousness effect has been established. This is the tenth and final sound loop; later work requires new independent physical recordings and a separately frozen pilot-informed plan.
''',files+['example-aligned-fit.csv','admission-cases.json','source-hashes.json','admission.csv','figure.svg','../batch_intake.py','../intake_v2.py','../fit_recording.py','../S5A/preregistration.json'])
