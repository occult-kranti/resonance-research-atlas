from pathlib import Path
import sys,json,subprocess,tempfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from common import *
from fit_recording import read_recording
p=Path(__file__).parent;fixture=ROOT/'S2A/case0.wav';t,y,_=read_recording(fixture);csv(p/'source.csv',['time_s','amplitude_FS'],np.column_stack([t,y]));records=[];files=['source.csv']
with tempfile.TemporaryDirectory() as tmp:
    temp=Path(tmp)
    def cli(source,prefix,channel=0):
        args=[sys.executable,str(ROOT/'intake_v2.py'),str(source),'--frequency','500','--start','.05','--stop','.8','--output',str(prefix),'--channel',str(channel),'--provenance','synthetic_generated'];res=subprocess.run(args,capture_output=True,text=True);return res
    a=cli(fixture,temp/'wav');b=cli(p/'source.csv',temp/'csv');assert a.returncode==b.returncode==0
    ra=json.loads(a.stdout);rb=json.loads(b.stdout);ta=np.loadtxt(temp/'wav.csv',delimiter=',',skiprows=1);tb=np.loadtxt(temp/'csv.csv',delimiter=',',skiprows=1);diff=float(np.max(np.abs(ta-tb)));adiff=abs(ra['alpha_per_s']-rb['alpha_per_s']);fdiff=abs(ra['frequency_Hz']-rb['frequency_Hz']);assert diff<1e-12 and adiff<1e-9 and fdiff<1e-9
    for name in ['wav','csv']:
        for ext in ['json','csv']:(p/f'accepted_{name}.{ext}').write_bytes((temp/f'{name}.{ext}').read_bytes());files.append(f'accepted_{name}.{ext}')
    source=temp/'collision.csv';source.write_bytes((p/'source.csv').read_bytes());sentinel=temp/'existing.json';sentinel.write_text('SENTINEL');link=temp/'linked.csv';link.symlink_to(source)
    cases=[('source_collision',source,temp/'collision',0),('existing_output',source,temp/'existing',0),('CSV_channel',source,temp/'channel',1),('symlink_collision',source,temp/'linked',0)]
    for name,src,out,channel in cases:
        before=sha(src);sentinel_before=sha(sentinel);result=cli(src,out,channel);unchanged=sha(src)==before;sentinel_ok=sha(sentinel)==sentinel_before;assert result.returncode==2 and unchanged and sentinel_ok
        records.append({'case':name,'returncode':result.returncode,'error':json.loads(result.stderr),'sourceSHA256Before':before,'sourceSHA256After':sha(src),'sourceUnchanged':unchanged,'sentinelUnchanged':sentinel_ok})
writejson(p/'admission_cases.json',records);csv(p/'admission.csv',['case_index','returncode','source_unchanged','sentinel_unchanged'],[[i,r['returncode'],r['sourceUnchanged'],r['sentinelUnchanged']]for i,r in enumerate(records)])
metrics={'valid_trace_max_difference_FS':diff,'valid_alpha_difference_per_s':adiff,'valid_frequency_difference_Hz':fdiff,'rejected_cases':len(records),'protected_sources':sum(r['sourceUnchanged'] for r in records),'protected_sentinels':sum(r['sentinelUnchanged'] for r in records)}
fig,ax=plt.subplots(figsize=(8,3.8));ax.barh([r['case'] for r in records],[int(r['sourceUnchanged'] and r['returncode']==2) for r in records],color='#326e75');ax.set(xlim=(0,1.2),xticks=[0,1],xlabel='Admission rejected and source hash preserved (1 = yes)',title='Executed file-integrity controls; no acoustic claim');savefig(fig,p/'figure.svg')
finish(p,metrics,'The protected version rejects source collisions, existing outputs, invalid CSV channel and symlink collisions while preserving equivalent valid WAV/CSV analysis.',[{'control':'Historical direct CLI','outcome':'retained for reproduction only; input-collision and channel defects repaired by versioned wrapper'}],'''# S3A — protect evidence before interpreting it

This loop repairs a concrete defect found during root review rather than running the originally proposed geometry study. The historical fitter remains unchanged and hash-bound to S2A/S2B. The new intake_v2.py guards paths before analysis, rejects CSV channel selection other than zero, and uses exclusive file creation. Existing outputs cannot be overwritten; choose a new prefix. If creating the second output fails, only files created by this invocation are cleaned up.

Actual CLI runs demonstrate preserved raw-source and sentinel hashes for source, symlink and existing-output collisions. The valid decoded WAV and exact two-column CSV produce identical fit traces and fitted parameters under the frozen tolerances. Source hashes, provenance declarations and both implementation hashes appear in output JSON.

This is evidence-preserving software/metrology verification, not an acoustic discovery. The caller's provenance label is not independent authentication. The physical limitations established by S2B still hold. Next: malformed acquisition metadata and time-base calibration, including failures that file validation cannot detect.
''',files+['admission_cases.json','admission.csv','figure.svg','../fit_recording.py','../intake_v2.py'])
