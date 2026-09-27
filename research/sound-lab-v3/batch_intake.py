"""Apply a frozen trial plan to an acquisition manifest; never overwrite source or outputs."""
from pathlib import Path
import argparse,csv,hashlib,json,re,sys
import numpy as np
from intake_v2 import run as intake
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def writejson(path,value):
    with Path(path).open('x') as stream:stream.write(json.dumps(value,indent=2,allow_nan=False)+'\n')
def run_batch(plan_path,manifest_path,output_dir):
    plan_path=Path(plan_path).resolve(strict=True);manifest_path=Path(manifest_path).resolve(strict=True);plan=json.loads(plan_path.read_text());manifest=json.loads(manifest_path.read_text());out=Path(output_dir)
    expected=plan['orderedTrials'];trials=manifest['trials'];metadata=manifest.get('metadata',{})
    if not isinstance(expected,list) or not expected:raise ValueError('Plan must contain at least one trial')
    codes={r.get('condition_code') for r in expected}
    if not codes<={'A','B'}:raise ValueError('Plan condition codes must be A or B')
    if codes!={'A','B'}:raise ValueError('Plan must contain both A and B conditions')
    if plan.get('expectedPrimaryTrialCount')!=len(expected):raise ValueError('expectedPrimaryTrialCount does not match planned length')
    for name in ['device','gain_processing','geometry','clock_reference','impact_alignment_rule']:
        if not isinstance(metadata.get(name),str) or not metadata[name].strip():raise ValueError('Missing required metadata: '+name)
    for group in [expected,trials]:
        ids=[r['trial_id'] for r in group]
        if len(ids)!=len(set(ids)):raise ValueError('Duplicate trial ID')
        if any(not isinstance(i,str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,40}',i) for i in ids):raise ValueError('Invalid trial ID')
    provenance=manifest.get('evidenceType','user_supplied_recording_unverified')
    if provenance not in ['synthetic_generated','user_supplied_recording_unverified']:raise ValueError('Unknown provenance declaration')
    if out.exists() or out.is_symlink():raise ValueError('Output directory already exists; choose a new directory')
    out.mkdir(parents=True,exist_ok=False);lookup={r['trial_id']:r for r in expected};results=[];seen_hashes=set()
    for item in trials:
        tid=item['trial_id'];record={'trial_id':tid,'condition_code':item.get('condition_code'),'order':item.get('order'),'inputPath':item.get('path'),'eligible':False,'flags':[]}
        try:
            if tid not in lookup:raise ValueError('Unplanned trial ID')
            target=lookup[tid]
            if item.get('condition_code')!=target['condition_code']:raise ValueError('Condition code differs from frozen plan')
            if item.get('order')!=target['order']:raise ValueError('Trial order differs from frozen plan')
            source=(manifest_path.parent/item['path']).resolve(strict=True);digest=sha(source);record['observedSourceSHA256']=digest
            if digest!=item.get('source_sha256'):raise ValueError('Source SHA256 mismatch')
            if digest in seen_hashes:raise ValueError('Duplicate source bytes across trials')
            seen_hashes.add(digest);impact=float(item['impact_time_s'])
            if not np.isfinite(impact) or impact<0:raise ValueError('Invalid impact time')
            start=impact+float(target['fit_start_after_tap_s']);stop=impact+float(target['fit_stop_after_tap_s']);frequency=float(target['nominal_frequency_Hz']);record.update({'impact_time_s':impact,'absoluteFitWindow_s':[start,stop]})
            fit=intake(source,out/tid,frequency,start,stop,provenance=provenance);record.update({'fitStatus':fit['status'],'flags':fit['flags'],'sourceUnchanged':sha(source)==digest,'fit_json':tid+'.json','fit_csv':tid+'.csv'})
            for name in ['alpha_per_s','frequency_Hz','normalizedResidual']:
                if name in fit:record[name]=fit[name]
            record['eligible']=fit['status']=='fit' and not fit['flags'] and record['sourceUnchanged']
        except (ValueError,OSError,KeyError,TypeError) as exc:record['flags'].append(str(exc));record['fitStatus']='admission_rejected'
        results.append(record)
    provided={r['trial_id'] for r in trials};missing=[r['trial_id'] for r in expected if r['trial_id'] not in provided]
    for tid in missing:results.append({'trial_id':tid,'condition_code':lookup[tid]['condition_code'],'order':lookup[tid]['order'],'eligible':False,'fitStatus':'not_provided','flags':['Planned trial missing']})
    eligible=[r for r in results if r['eligible']];counts={code:sum(r['condition_code']==code for r in eligible) for code in ['A','B']};means={code:(float(np.mean([r['alpha_per_s'] for r in eligible if r['condition_code']==code])) if counts[code] else None) for code in ['A','B']};descriptive=means['B']-means['A'] if all(means[c] is not None for c in ['A','B']) else None
    complete=len(trials)==len(expected) and {r['trial_id'] for r in eligible}==set(lookup)
    summary={'status':'complete_primary_set' if complete else 'incomplete_primary_set','evidenceType':provenance,'scope':'Recorded-channel comparison. Metadata are caller declarations, not authentication or physical calibration.','planSHA256':sha(plan_path),'manifestSHA256':sha(manifest_path),'batchImplementationSHA256':sha(__file__),'expectedTrials':len(expected),'providedTrials':len(trials),'eligibleTrials':len(eligible),'conditionCounts':counts,'missingTrialIDs':missing,'primaryContrast_per_s':descriptive if complete else None,'descriptiveSurvivorContrast_per_s':descriptive,'descriptiveWarning':'For incomplete plans this survivor contrast is not the preregistered primary result.','metadata':metadata,'trials':results}
    writejson(out/'batch-results.json',summary)
    with (out/'trial-results.csv').open('x') as stream:
        writer=csv.writer(stream);writer.writerow(['trial_id','order','condition_code','eligible','alpha_per_s','frequency_Hz','normalized_residual','flags'])
        for r in results:writer.writerow([r['trial_id'],r.get('order'),r.get('condition_code'),r['eligible'],r.get('alpha_per_s'),r.get('frequency_Hz'),r.get('normalizedResidual'),' | '.join(r['flags'])])
    return summary
def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--plan',required=True);parser.add_argument('--manifest',required=True);parser.add_argument('--output',required=True);a=parser.parse_args()
    try:result=run_batch(a.plan,a.manifest,a.output)
    except (ValueError,OSError,KeyError,TypeError) as exc:print(json.dumps({'status':'rejected','reason':str(exc)}),file=sys.stderr);return 2
    print(json.dumps({k:v for k,v in result.items() if k!='trials'},indent=2));return 0
if __name__=='__main__':raise SystemExit(main())
