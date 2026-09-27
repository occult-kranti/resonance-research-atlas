"""Evidence-preserving recording intake. The historical fitter remains byte-frozen."""
from pathlib import Path
import argparse,hashlib,json,sys
import numpy as np
from fit_recording import analyze
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def run(input_path,output_prefix,frequency,start,stop,alpha_max=20,channel=0,provenance='user_supplied_recording_unverified'):
    source=Path(input_path).resolve(strict=True);prefix=Path(output_prefix);targets=[prefix.with_suffix('.json'),prefix.with_suffix('.csv')]
    if source.suffix.lower()=='.csv' and channel!=0: raise ValueError('CSV has only channel zero')
    if provenance not in ['user_supplied_recording_unverified','synthetic_generated']: raise ValueError('Unknown provenance declaration')
    for dest in targets:
        if dest.resolve()==source: raise ValueError('Output collides with original input; raw evidence is protected')
        if dest.exists() or dest.is_symlink(): raise ValueError('Output already exists; choose a new output prefix')
    original=sha(source);result,trace=analyze(source,frequency,start,stop,alpha_max,channel)
    if sha(source)!=original: raise ValueError('Input changed during analysis')
    result.update({'evidenceType':provenance,'inputProvenance':'Declared by caller; not authenticated by this tool','intakeVersion':2,'intakeSHA256':sha(__file__),'historicalFitterSHA256':sha(Path(__file__).with_name('fit_recording.py')),'rawInputPreserved':True,'outputPolicy':'Exclusive creation; existing files and source collisions rejected'})
    for dest in targets: dest.parent.mkdir(parents=True,exist_ok=True)
    created=[]
    try:
        with targets[0].open('x') as stream:
            created.append(targets[0]);stream.write(json.dumps(result,indent=2,allow_nan=False)+'\n')
        with targets[1].open('x') as stream:
            created.append(targets[1]);np.savetxt(stream,trace,delimiter=',',header='time_s,amplitude_FS,fit_FS,residual_FS',comments='',fmt='%.17g')
    except BaseException:
        for dest in created: dest.unlink(missing_ok=True)
        raise
    return result
def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('input');parser.add_argument('--output',required=True);parser.add_argument('--frequency',type=float,required=True);parser.add_argument('--start',type=float,required=True);parser.add_argument('--stop',type=float,required=True);parser.add_argument('--alpha-max',type=float,default=20);parser.add_argument('--channel',type=int,default=0);parser.add_argument('--provenance',choices=['user_supplied_recording_unverified','synthetic_generated'],default='user_supplied_recording_unverified');a=parser.parse_args()
    try: result=run(a.input,a.output,a.frequency,a.start,a.stop,a.alpha_max,a.channel,a.provenance)
    except (ValueError,OSError) as exc: print(json.dumps({'status':'rejected','reason':str(exc)}),file=sys.stderr);return 2
    print(json.dumps(result,indent=2));return 0
if __name__=='__main__': raise SystemExit(main())
