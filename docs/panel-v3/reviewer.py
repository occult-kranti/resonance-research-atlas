#!/usr/bin/env python3
"""Independent advisor formulas and replayable checks for the V3 finite program.
Uses standard-library formulas, explicit raw-output checks, and byte bindings.
A successful replay validates declared models, never empirical observations.
"""
from pathlib import Path
from fractions import Fraction
from collections import defaultdict, Counter
import itertools
import argparse, cmath, csv, hashlib, json, math, wave, struct, tempfile, subprocess, sys, shutil
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/panel-v3/reviews'
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def close(a,b,tol=1e-10):
    err=abs(a-b)
    if err>tol: raise AssertionError((a,b,err,tol))
    return err
def expected_s1a():
    fs=8000; nfft=16384
    rows=[]
    for k in range(nfft//2+1):
        z=cmath.exp(-2j*math.pi*k/nfft)
        h=(.7+.2*z+.1*z*z)*(1+.6*z**40)
        rows.append([k,k*fs/nfft,h.real,h.imag])
    # e=1+z**40 has roots on these exact FFT grid bins.
    zeros=[k for k in range(nfft//2+1) if abs(1+cmath.exp(-2j*math.pi*k/nfft)**40)<1e-12]
    return {'id':'S1A','method':'Direct polynomial evaluation from 43 FIR taps, no producer solver imported','expected_transfer_at_dc':1.6,'echo_delay_s':40/fs,'echo_comb_spacing_hz':fs/40,'r1_zero_bins':zeros,'r1_zero_frequencies_hz':[k*fs/nfft for k in zeros],'rows':rows,'factorization_witness':'(d,e) and (d*e,delta) have identical convolution h; total transfer cannot distinguish them.'}
def review_s1a():
    p=ROOT/'research/sound-lab-v3/S1A'
    independent=expected_s1a(); expected=independent.pop('rows')
    rows=list(csv.DictReader((p/'response.csv').open()))
    errors=[]; zero_bins=[]
    for row, exp in zip(rows,expected):
        k=int(row['bin']); assert k==exp[0]
        h=complex(exp[2],exp[3]); est=complex(float(row['estimate_real']),float(row['estimate_imag']))
        errors.append(close(h,est,1e-10))
        z=cmath.exp(-2j*math.pi*k/16384);d=.7+.2*z+.1*z*z
        close(abs(d),float(row['r0_magnitude']),1e-12)
        close(abs(d*(1+z**40)),float(row['r1_magnitude']),1e-12)
        if int(row['inverse_H_excluded']): zero_bins.append(k)
    assert zero_bins==independent['r1_zero_bins']; assert len(rows)==8193
    raw=list(csv.DictReader((p/'probe_outputs.csv').open()))
    rel=math.sqrt(sum((float(r['heldout_prediction_FS'])-float(r['heldout_actual_FS']))**2 for r in raw)/sum(float(r['heldout_actual_FS'])**2 for r in raw))
    assert rel<1e-10
    taps={0:.7,1:.2,2:.1,40:.42,41:.12,42:.06}
    for r in csv.DictReader((p/'impulse.csv').open()): close(float(r['estimated_H']),taps.get(int(r['sample']),0),1e-12)
    return {'independent_polynomial_max_error':max(errors),'independent_saved_heldout_L2':rel,'zero_bins':zero_bins,'tap_identity_checked':True,'factorization_proof':'Associativity: x*(d*e)=(x*d)*e=x*(d_alt*delta). This proves output equivalence for every finite x.'}
def review_s1b():
    p=ROOT/'research/sound-lab-v3/S1B';rows=list(csv.DictReader((p/'response.csv').open()))
    err=0;masked=0;unmasked=0;regnoise=0;regbias=0;move=0;moveall=0;excluded=0
    for r in rows:
        f=float(r['frequency_Hz']);z=cmath.exp(-2j*math.pi*f/8000);d=.7+.2*z+.1*z*z;h=d*(1+.98*z**40);t=1-.3*z**4
        def c(name):return complex(float(r[name+'_real']),float(r[name+'_imag']))
        err=max(err,close(h,c('H0'),1e-12),close(t,c('T'),1e-12));eta=c('eta');close(abs(eta),.002,1e-15)
        q=t+eta/h;ql=t-t*.0004/(abs(h)**2+.0004)+eta*h.conjugate()/(abs(h)**2+.0004)
        err=max(err,close(q,c('direct'),1e-10),close(ql,c('regularized'),1e-10));m=(1+.98*z**41)/(1+.98*z**40);close(m,c('moved_blank'),1e-9)
        ok=abs(h)>=.15;assert bool(int(r['eligible']))==ok;excluded+=not ok
        unmasked=max(unmasked,abs(q-t));moveall=max(moveall,abs(m-1));regnoise=max(regnoise,.002*abs(h)/(abs(h)**2+.0004));regbias=max(regbias,abs(t)*.0004/(abs(h)**2+.0004))
        if ok:masked=max(masked,abs(q-t));move=max(move,abs(m-1))
    assert masked<=.002/.15+1e-12;assert regnoise<=.05+1e-12;assert excluded==234
    return {'independent_formula_max_error':err,'excluded_bins':excluded,'masked_noise_error':masked,'unmasked_noise_error':unmasked,'regularized_noise_bound_attained':regnoise,'regularized_bias_max':regbias,'moved_blank_masked_max':move,'moved_blank_unmasked_max':moveall,'proof':'(a-sqrt(lambda))^2>=0 implies a/(a^2+lambda)<=1/(2sqrt(lambda)); error separates exact bias and bounded-noise term.'}
def pcm16(path):
    with wave.open(str(path)) as w:
        assert w.getsampwidth()==2 and w.getnchannels()==1
        fs=w.getframerate();v=struct.unpack('<'+'h'*w.getnframes(),w.readframes(w.getnframes()))
    return fs,[x/32768 for x in v]
def review_s2a():
    p=ROOT/'research/sound-lab-v3/S2A';intake=json.loads((p/'intake_results.json').read_text());checks=[]
    for n,(gain,phase) in enumerate([(.1,0),(.2,1),(.3,2),(0,0),(1.2,0)]):
        fs,x=pcm16(p/f'case{n}.wav');assert fs==8000 and len(x)==16000
        # Direct closed-form samples before rounding; allow one LSB for libm boundary variation.
        max_pcm_error=max(abs(x[i]-max(-1,min(32767/32768,gain*math.exp(-4*i/fs)*math.cos(2*math.pi*500*i/fs+phase)))) for i in range(len(x)))
        assert max_pcm_error<=.5/32768+1e-13
        clips=sum(abs(v)>=32767/32768 for v in x);assert clips==intake[n]['clippedSamples']
        if n<3:
            q=sum(x[i]*x[i+16] for i in range(400,6384))/sum(x[i]**2 for i in range(400,6384));alpha=-500*math.log(q)
            ts=[(i-x[i]/(x[i+1]-x[i]))/fs for i in range(400,6399) if x[i]<=0<x[i+1]];f=(len(ts)-1)/(ts[-1]-ts[0])
            assert abs(alpha-4)<.01 and abs(f-500)<.01
            raw=list(csv.DictReader((p/f'fit{n}.csv').open()));ratio=math.sqrt(sum(float(r['residual_FS'])**2 for r in raw)/sum(float(r['decoded_FS'])**2 for r in raw));close(ratio,intake[n]['normalizedResidual'],1e-12)
            checks.append({'case':n,'cycle_shift_alpha_per_s':alpha,'zero_crossing_frequency_Hz':f,'residual_recomputed':ratio,'max_PCM_quantization_error':max_pcm_error})
        else:assert intake[n]['status']=='rejected'
    assert intake[4]['clippedSamples']==97
    return {'independent_estimators':checks,'silent_and_97_sample_clipping_rejections_verified':True,'proof':'With a 16-sample period y[n+16]=exp(-4*16/8000)y[n]; constant gain and phase cancel in the ratio, whereas time-varying gain need not.'}
def review_s2b():
    p=ROOT/'research/sound-lab-v3/S2B';records=json.loads((p/'intake_results.json').read_text());assert (p/'gain_drift.wav').read_bytes()==(p/'true_alpha2.wav').read_bytes()
    residuals=[]
    for r in records:
        w=0 if r['window_s'][0]==.05 else 1;rows=list(csv.DictReader((p/(r['case']+f'_{w}.csv')).open()));ratio=math.sqrt(sum(float(x['residual_FS'])**2 for x in rows)/sum(float(x['decoded_FS'])**2 for x in rows));close(ratio,r['normalizedResidual'],1e-12);residuals.append(ratio)
        if r['case'] in ['gain_drift','true_alpha2']:assert abs(r['alpha_per_s']-2)<.01
    assert sum(bool(r['flags']) for r in records)==2
    fs,x=pcm16(p/'gain_drift.wav');q=sum(x[i]*x[i+16] for i in range(400,6384))/sum(x[i]**2 for i in range(400,6384));alpha=-500*math.log(q);assert abs(alpha-2)<.01
    return {'PCM_identity':True,'independent_cycle_shift_alpha':alpha,'residuals_independently_recounted':residuals,'flagged_count':2,'proof':'For all real t, exp(2t)*[.2 exp(-4t) cos(1000pi t)]=.2 exp(-2t)cos(1000pi t). Identical samples force identical outcomes for every deterministic recording-only estimator.'}
def review_s3a():
    p=ROOT/'research/sound-lab-v3/S3A';wrapper=ROOT/'research/sound-lab-v3/intake_v2.py';checks={}
    with tempfile.TemporaryDirectory(prefix='v3-independent-intake-') as tmp:
        t=Path(tmp);src=t/'raw.csv';shutil.copyfile(p/'source.csv',src);original=sha(src)
        def run(prefix,channel=0):
            return subprocess.run([sys.executable,str(wrapper),str(src),'--output',str(prefix),'--frequency','500','--start','.05','--stop','.8','--channel',str(channel)],capture_output=True,text=True)
        checks['source_collision_rejected']=run(t/'raw').returncode!=0 and sha(src)==original
        sent=t/'sentinel.json';sent.write_text('preserve me');before=sha(sent);checks['existing_output_preserved']=run(t/'sentinel').returncode!=0 and sha(sent)==before
        checks['invalid_csv_channel_rejected']=run(t/'channel',1).returncode!=0 and not (t/'channel.json').exists()
        link=t/'alias.csv';link.symlink_to(src);checks['symlink_collision_rejected']=run(t/'alias').returncode!=0 and sha(src)==original
        ok=run(t/'valid');assert ok.returncode==0,ok.stderr;r=json.loads((t/'valid.json').read_text());checks['valid_analysis_preserved_raw']=sha(src)==original and r['rawInputPreserved'] and r['inputSHA256']==original
        assert abs(r['alpha_per_s']-4)<.01;assert abs(r['frequency_Hz']-500)<.01
        checks['provenance_remains_unverified']=r['evidenceType']=='user_supplied_recording_unverified'
    assert all(checks.values());assert (p/'accepted_wav.csv').read_bytes()==(p/'accepted_csv.csv').read_bytes()
    return {'independent_CLI_cases':checks,'accepted_WAV_CSV_trace_byte_identity':True,'scope':'Integrity and channel admission of declared files; neither source authenticity nor physical calibration.'}
def review_s3b():
    p=ROOT/'research/sound-lab-v3/S3B';d=json.loads((p/'intake_results.json').read_text());fs,x=pcm16(p/'wrong_header.wav');rows=list(csv.DictReader((p/'correct_time.csv').open()));assert fs==8000 and len(x)==16032
    assert all(float(r['amplitude_FS'])==v for r,v in zip(rows,x));time_error=max(abs(float(r['time_s'])-i/8016) for i,r in enumerate(rows));assert time_error<1e-15
    expected=[(4,500),(4*8000/8016,500*8000/8016),(4,500),(4,500)]
    for r,(a,f) in zip(d['fits'],expected):assert abs(r['alpha_per_s']-a)<.01 and abs(r['frequency_Hz']-f)<.01
    ref_fs,ref=pcm16(p/'reference.wav');ts=[(i-ref[i]/(ref[i+1]-ref[i]))/ref_fs for i in range(400,12000) if ref[i]<=0<ref[i+1]];ref_f=(len(ts)-1)/(ts[-1]-ts[0]);assert abs(ref_f-1000*8000/8016)<.005
    assert 'near_search_bound' in d['reference']['flags'];bad={r['case']:r for r in d['invalidCases']};assert 'uniform' in bad['nonuniform']['reason'].lower();assert all(r['sourceUnchanged'] for r in bad.values())
    with tempfile.TemporaryDirectory(prefix='v3-time-review-') as tmp:
        q=Path(tmp);badrows=rows[:1000];badrows[100]=dict(badrows[100]);badrows[100]['time_s']=str(float(badrows[100]['time_s'])+.00002);src=q/'irregular.csv'
        with src.open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=['time_s','amplitude_FS']);w.writeheader();w.writerows(badrows)
        before=sha(src);proc=subprocess.run([sys.executable,str(ROOT/'research/sound-lab-v3/intake_v2.py'),str(src),'--output',str(q/'out'),'--frequency','500','--start','.05','--stop','.1'],capture_output=True,text=True)
        assert proc.returncode!=0 and 'uniform' in proc.stderr and sha(src)==before
    return {'same_amplitudes':True,'time_axis_max_error_s':time_error,'analytic_apparent_frequency_Hz':500*8000/8016,'analytic_apparent_alpha_per_s':4*8000/8016,'independent_reference_zero_crossing_Hz':ref_f,'independent_nonuniform_gate_exercised':True,'proof':'Samples depend only on alpha/Fs_actual and f/Fs_actual. Scaling (alpha,f,Fs_actual) together leaves every sample unchanged. A timebase or independent frequency reference fixes this scale only by adding a premise.'}
def review_s4a():
    p=ROOT/'research/sound-lab-v3/S4A';a=1+0j;b=.6*cmath.exp(.7j);k=2*math.pi*500/343;err=0
    for r in csv.DictReader((p/'spatial_response.csv').open()):
        x=float(r['position_m']);z=cmath.exp(1j*k*x);expected=a/z+b*z;observed=complex(float(r['p_real']),float(r['p_imag']));partner=complex(float(r['partner_real']),float(r['partner_imag']));err=max(err,close(expected,observed,1e-12),close(expected.conjugate(),partner,1e-12));close(abs(expected)**2,float(r['magnitude_squared']),1e-12)
    obs=list(csv.DictReader((p/'observations.csv').open()));v=[complex(float(r['p_real']),float(r['p_imag'])) for r in obs];aa=(v[0]+1j*v[1])/2;bb=(v[0]-1j*v[1])/2;close(aa,a,1e-12);close(bb,b,1e-12)
    return {'whole_table_polynomial_error':err,'closed_form_A':[aa.real,aa.imag],'closed_form_B':[bb.real,bb.imag],'domain_dimension_complex':2,'single_sample_rank':1,'single_sample_nullity':1,'kernel':[1,-1],'two_sample_determinant':'2i','two_sample_Gram':'2I','proof':'Conjugate-swapping A,B conjugates p(x), preserving |p| for all x. Multiplying both by exp(i phi) also preserves |p|. At quarter wavelength, the explicit inverse recovers complex coefficients only with the assumed basis and phase reference.'}
def review_s4b():
    p=ROOT/'research/sound-lab-v3/S4B';maximum=0;singular=0
    for r in csv.DictReader((p/'conditioning.csv').open()):
        frac=float(r['separation_fraction']);theta=2*math.pi*frac
        if frac in (0,.5):assert int(r['rank'])==1 and int(r['nullity'])==1 and r['inverse_performed']=='False';singular+=1;continue
        small=2*min(abs(math.sin(theta/2)),abs(math.cos(theta/2)));large=2*max(abs(math.sin(theta/2)),abs(math.cos(theta/2)))
        close(small,float(r['sigma_min']),1e-12);close(large/small,float(r['condition']),1e-9);maximum=max(maximum,close(.001/small,float(r['coefficient_L2_error']),1e-12))
    groups={}
    for r in csv.DictReader((p/'noise_observations.csv').open()):groups.setdefault(r['separation_fraction'],[]).append(complex(float(r['noise_real']),float(r['noise_imag'])))
    for v in groups.values():close(math.sqrt(sum(abs(z)**2 for z in v)),.001,1e-15)
    rows=list(csv.DictReader((p/'phase_observations.csv').open()));v=[complex(float(r['drift_observed_real']),float(r['drift_observed_imag'])) for r in rows];delta=v[1]-complex(float(rows[1]['true_real']),float(rows[1]['true_imag']));pred=(v[0]+v[1])/math.sqrt(2);hold=abs(pred-v[2]);close(hold,abs(delta)/math.sqrt(2),1e-12)
    residual=math.sqrt(sum(float(r['three_sample_residual_real'])**2+float(r['three_sample_residual_imag'])**2 for r in rows));close(residual,abs(delta)/2,1e-12)
    return {'singular_cases_with_kernel_not_inverted':singular,'worst_case_noise_error_identity_max_error':maximum,'independent_heldout_error':hold,'independent_three_sample_residual':residual,'proof':'Gram eigenvalues are 2 +/- 2|cos(theta)|. At the withheld eighth wavelength, p_h=(p_0+p_quarter)/sqrt(2); a drift delta only at the second point causes heldout error |delta|/sqrt(2) and least-squares residual |delta|/2.'}
def review_s5a():
    p=ROOT/'research/sound-lab-v3/S5A';records=json.loads((p/'trial-results.json').read_text());assert len(records)==64;groups={};max_rate_error=0;max_pcm_error=0
    for r in records:
        b=int(r['condition_code']=='B');delta=2 if r['case'].endswith('effect') else 0;expected=4+delta*b-.08*r['order'];close(expected,r['trueRecordedAlpha_per_s'],1e-12);path=p/r['rawPath'];assert sha(path)==r['inputSHA256'];fs,x=pcm16(path);assert fs==8000
        q=sum(x[i]*x[i+16] for i in range(400,6384))/sum(x[i]**2 for i in range(400,6384));rate=-500*math.log(q);max_rate_error=max(max_rate_error,abs(rate-expected));assert abs(rate-expected)<.01
        # Alternate scalar reconstruction of the stored generated signal.
        error=max(abs(v-r['inputGain_FS']*math.exp(-expected*i/fs)*math.cos(2*math.pi*500*i/fs)) for i,v in enumerate(x));assert error<=.5/32768+1e-13;max_pcm_error=max(max_pcm_error,error);groups.setdefault(r['case'],[]).append(r)
    contrasts={};order_gaps={}
    for case,rs in groups.items():
        aa=[r for r in rs if r['condition_code']=='A'];bb=[r for r in rs if r['condition_code']=='B'];gap=sum(r['order'] for r in bb)/8-sum(r['order'] for r in aa)/8;order_gaps[case]=gap;contrast=sum(r['alpha_per_s'] for r in bb)/8-sum(r['alpha_per_s'] for r in aa)/8;contrasts[case]=contrast;expected=(2 if case.endswith('effect') else 0)-.08*gap;assert abs(contrast-expected)<.005
    assert (p/'condition_rival.wav').read_bytes()==(p/'balanced_effect/T02.wav').read_bytes()
    return {'independent_cycle_rate_max_error_per_s':max_rate_error,'all_64_PCM_quantization_max_error':max_pcm_error,'order_mean_differences_B_minus_A':order_gaps,'recounted_contrasts_per_s':contrasts,'saved_rival_byte_identity':True,'proof':'The contrast equals Delta - .08*(mean order_B-mean order_A): gaps8 and0 yield blocked bias-.64 and balanced zero. Multiplying a Delta=0 signal by exp(-2*B*t) gives the Delta=2 signal identically, so order balance cannot remove that condition-linked rival.'}
def review_s5b():
    p=ROOT/'research/sound-lab-v3/S5B';plan=ROOT/'research/sound-lab-v3/S5A/preregistration.json';batch=ROOT/'research/sound-lab-v3/batch_intake.py'
    stored=json.loads((p/'complete-batch.json').read_text());eligible=stored['trials'];assert len(eligible)==16 and all(r['eligible'] for r in eligible)
    contrast=sum(r['alpha_per_s'] for r in eligible if r['condition_code']=='B')/8-sum(r['alpha_per_s'] for r in eligible if r['condition_code']=='A')/8;close(contrast,stored['primaryContrast_per_s'],1e-12)
    fs,padded=pcm16(p/'padded_T01.wav');_,base=pcm16(ROOT/'research/sound-lab-v3/S5A/balanced_effect/T01.wav');assert padded[:8000]==[0]*8000 and padded[8000:]==base
    for name in ['missing','invalid_trials','wrong_condition','wrong_impact']:
        r=json.loads((p/(name+'-batch.json')).read_text());assert r['primaryContrast_per_s'] is None and len(r['trials'])==16
    sources=json.loads((p/'source-hashes.json').read_text())['files']
    for r in sources:assert sha(ROOT/'research/sound-lab-v3'/r['path'])==r['sha256'] and r['unchanged']
    with tempfile.TemporaryDirectory(prefix='v3-batch-review-') as tmp:
        t=Path(tmp)
        def run(pp,mm,out):return subprocess.run([sys.executable,str(batch),'--plan',str(pp),'--manifest',str(mm),'--output',str(out)],capture_output=True,text=True)
        proc=run(plan,p/'complete-manifest.json',t/'complete');assert proc.returncode==0,proc.stderr;fresh=json.loads((t/'complete/batch-results.json').read_text());close(fresh['primaryContrast_per_s'],contrast,1e-10);assert fresh['trials'][0]['absoluteFitWindow_s']==[1.05,1.8]
        before=sha(t/'complete/batch-results.json');again=run(plan,p/'complete-manifest.json',t/'complete');assert again.returncode!=0 and sha(t/'complete/batch-results.json')==before
        pd=json.loads(plan.read_text());md=json.loads((p/'complete-manifest.json').read_text());rejections={}
        for kind in ['empty','A_only']:
            pp=dict(pd);pp['orderedTrials']=[] if kind=='empty' else [r for r in pd['orderedTrials'] if r['condition_code']=='A'];pp['expectedPrimaryTrialCount']=len(pp['orderedTrials']);mm=dict(md);mm['trials']=[] if kind=='empty' else [r for r in md['trials'] if r['condition_code']=='A'];ppath=t/(kind+'-plan.json');mpath=t/(kind+'-manifest.json');ppath.write_text(json.dumps(pp));mpath.write_text(json.dumps(mm));out=t/(kind+'-output');res=run(ppath,mpath,out);assert res.returncode!=0 and not out.exists();reason=json.loads(res.stderr)['reason'];assert ('empty' in reason.lower() or 'nonempty' in reason.lower() or 'at least' in reason.lower() or 'both' in reason.lower());rejections[kind]=reason
    return {'independent_complete_contrast_per_s':contrast,'all_19_raw_hashes_verified':len(sources)==19,'padded_samples_exact_and_absolute_window_checked':True,'four_incomplete_primary_results_withheld':True,'existing_output_preserved_independently':True,'independent_pre_output_plan_rejections':rejections,'repair':'Initial S5B empty/one-condition-plan admission was rejected during review; original evidence and implementation are retained under pre-review/.'}
def expected_b1():
    pri=[11,3,3,3];joint={};summaries={}
    for scenario in range(1,8):
        rows=[]
        for t in range(4):
            for a in range(4):
                for b in range(4):
                    la=13 if a==t else 9;lb=13 if b==t else 9
                    count={1:(pri[t]*320 if a==b==0 else 0),2:(1600 if a==b==0 else 0),3:(pri[t]*pri[a]*16 if a==b else 0),4:100,5:(40*la if a==b else 0),6:la*lb,7:(40*la if a==b else 0)}[scenario]
                    rows.append((t,a,b,count))
        assert sum(r[3] for r in rows)==6400;joint[scenario]=rows
        def ent(indices):
            marginal=defaultdict(int)
            for r in rows:marginal[tuple(r[i] for i in indices)]+=r[3]
            return -sum((v/6400)*math.log2(v/6400) for v in marginal.values() if v)
        ht,ha,hb,hta,htb,hab,htab=[ent(ix) for ix in [(0,),(1,),(2,),(0,1),(0,2),(1,2),(0,1,2)]]
        summaries[scenario]={'hit_A':sum(r[3] for r in rows if r[0]==r[1])/6400,'agreement':sum(r[3] for r in rows if r[1]==r[2])/6400,'I_T_A':ht+ha-hta,'I_T_AB':ht+hab-htab,'CMI_T_B_given_A':hta+hab-ha-htab}
    nulls={}
    for u,v in [(1,4),(11,20),(37,100)]:
        den=v**80;masses=[math.comb(80,k)*u**k*(v-u)**(80-k) for k in range(81)];tails=[sum(masses[k:]) for k in range(81)];cut=next(k for k,n in enumerate(tails) if 20*n<=den);nulls[str(Fraction(u,v))]={'cutoff':cut,'achieved_size':float(Fraction(tails[cut],den)),'tail_at_wrong_quarter_cutoff':None,'integer_mass_sum':sum(masses)==den,'masses':masses,'tails':tails,'denominator':den}
    cutoff=nulls['1/4']['cutoff']
    for d in nulls.values():d['tail_at_wrong_quarter_cutoff']=float(Fraction(d['tails'][cutoff],d['denominator']))
    return {'joint_counts_denominator':6400,'joint_counts':joint,'scenarios':summaries,'binomial':nulls}
def review_b1():
    p=ROOT/'research/consciousness-v3/round1';expected=expected_b1();r=json.loads((p/'results.json').read_text());names=['biased_majority','balanced_majority','biased_common_random','balanced_independent_null','balanced_copied_leak','balanced_independent_leaks','hypothetical_receiver_copy'];lookup={names[i-1]:{(t,a,b):v for t,a,b,v in rows} for i,rows in expected['joint_counts'].items()};rows=list(csv.DictReader((p/'joint_states.csv').open()));assert len(rows)==448
    for x in rows:
        v=Fraction(lookup[x['scenario']][(int(x['target']),int(x['report_A']),int(x['report_B']))],6400);assert Fraction(x['probability_exact'])==v;close(float(x['probability']),float(v),1e-15)
    maxinfo=0
    for i,case in enumerate(r['scenarios'],1):
        assert case['id']==names[i-1];ex=expected['scenarios'][i]
        for name,field in [('hit_A','hit_A'),('agreement','agreement'),('I_T_A','I_T_A_bits'),('I_T_AB','I_T_AB_bits'),('CMI_T_B_given_A','I_T_B_given_A_bits')]:maxinfo=max(maxinfo,close(ex[name],case[field],1e-12))
    rows=list(csv.DictReader((p/'binomial_nulls.csv').open()));assert len(rows)==243
    for x in rows:
        d=expected['binomial'][x['p_exact']];k=int(x['hits']);assert int(x['n'])==80 and int(x['critical_hits'])==d['cutoff'];assert Fraction(x['mass_exact'])==Fraction(d['masses'][k],d['denominator']);assert Fraction(x['tail_exact'])==Fraction(d['tails'][k],d['denominator'])
    return {'exact_joint_states_checked':448,'exact_binomial_masses_and_tails_checked':243,'information_entropy_formula_max_error_bits':maxinfo,'integer_denominator':6400,'cutoffs':{k:v['cutoff'] for k,v in expected['binomial'].items()},'wrong_baseline_rejection':{k:v['tail_at_wrong_quarter_cutoff'] for k,v in expected['binomial'].items()},'proof':'Integer weights over6400 exactly determine the single-trial joint law. B=A makes conditional added information zero; informative conditionally independent reports add information. Relabeling the identical copied-leak distribution as a receiver does not identify its cause. Binomial tails assume independent repeated trials.'}
def expected_b2():
    reports=(0,0,1,1,2,2,3,3);records=[];fixed=Counter();maximum=Counter();selected=Counter()
    for target in itertools.product(range(4),repeat=8):
        if any(target.count(k)!=2 for k in range(4)):continue
        scores=tuple(sum(2-min((t-r-m)%4,(r+m-t)%4) for r,t in zip(reports,target)) for m in range(4));best=max(scores);choice=scores.index(best);records.append((target,scores,choice));fixed[scores[0]]+=1;maximum[best]+=1;selected[choice]+=1
    n=len(records);assert n==2520;ft={s:sum(v for k,v in fixed.items() if k>=s) for s in range(17)};mt={s:sum(v for k,v in maximum.items() if k>=s) for s in range(17)}
    rates={'fixed_rule':Fraction(sum(v for s,v in fixed.items() if 20*ft[s]<=n),n),'post_selected_naive':Fraction(sum(v for s,v in maximum.items() if 20*ft[s]<=n),n),'max_calibrated':Fraction(sum(v for s,v in maximum.items() if 20*mt[s]<=n),n)}
    return {'records':records,'fixed_counts':dict(fixed),'max_counts':dict(maximum),'selected_counts':dict(selected),'rates':{k:str(v) for k,v in rates.items()},'discovery_mean':str(Fraction(sum(s*v for s,v in maximum.items()),n)),'holdout_mean':'8','positive_max_tail':str(Fraction(mt[16],n))}
def review_b2():
    p=ROOT/'research/consciousness-v3/round2';expected=expected_b2();lookup={''.join(map(str,t)):(scores,choice) for t,scores,choice in expected['records']};fixed=expected['fixed_counts'];maximum=expected['max_counts'];n=2520;rows=list(csv.DictReader((p/'assignments.csv').open()));assert len(rows)==n
    for r in rows:
        scores,choice=lookup[r['target_labels']];assert tuple(int(r[f'score_m{i}']) for i in range(4))==scores and int(r['selected_shift'])==choice;best=max(scores);ft=lambda s:Fraction(sum(v for k,v in fixed.items() if k>=s),n);mt=lambda s:Fraction(sum(v for k,v in maximum.items() if k>=s),n);assert Fraction(r['fixed_p_exact'])==ft(scores[0]);assert Fraction(r['naive_selected_p_exact'])==ft(best);assert Fraction(r['max_corrected_p_exact'])==mt(best)
    counts=Counter((choice,max(scores)) for target,scores,choice in expected['records']);pairs=0
    for r in csv.DictReader((p/'discovery_holdout.csv').open()):
        m=int(r['selected_shift']);disc=int(r['discovery_max_score']);hold=int(r['holdout_score']);multiplicity=counts[(m,disc)]*fixed.get(hold,0);assert int(r['pair_multiplicity'])==multiplicity and Fraction(r['probability_exact'])==Fraction(multiplicity,n*n);pairs+=multiplicity
    assert pairs==n*n
    result=json.loads((p/'results.json').read_text())['metrics'];close(result['selected_discovery_mean_score'],float(Fraction(expected['discovery_mean'])),1e-12);close(result['holdout_mean_score'],8,1e-12)
    for key,metric in [('fixed_rule','fixed_rule_rejection'),('post_selected_naive','naive_selected_rejection'),('max_calibrated','max_corrected_rejection')]:close(result[metric],float(Fraction(expected['rates'][key])),1e-15)
    return {'assignments_exhaustively_checked':n,'weighted_independent_pairs_checked':pairs,'exact_rejection_rates':expected['rates'],'exact_discovery_mean':expected['discovery_mean'],'exact_holdout_mean':'8','positive_corrected_tail':expected['positive_max_tail'],'proof':'The independent balanced holdout has the same fixed-rule distribution for every selected cyclic shift. Thus discovery selection changes the maximum distribution but not the untouched holdout mean. At alpha=.05 discreteness makes naive-selected and max-calibrated decisions coincide; neither exceeds nominal .05 in this fixture.'}
def expected_b3():
    tables={};metrics={}
    for regime in ['observational','crossed']:
        for mechanism in ['state_readout','prompt_only']:
            rows=[]
            for z,p,r,f,e,v in itertools.product(range(2),repeat=6):
                prior=(2 if z==p else 0) if regime=='observational' else 1;rn=9 if r==(z if mechanism=='state_readout' else p) else 1;fn=9 if f==p else 1;vn=(2+10*f+5*e) if v else (18-10*f-5*e);rows.append((z,p,r,f,e,v,prior*rn*fn*vn))
            assert sum(row[6] for row in rows)==16000;key=(regime,mechanism);tables[key]=rows
            def cond(event,condition):
                den=sum(x[6] for x in rows if condition(x));return Fraction(sum(x[6] for x in rows if condition(x) and event(x)),den)
            accuracy=Fraction(sum(x[6] for x in rows if x[2]==x[0]),16000);cue=cond(lambda x:x[5]==1,lambda x:x[4]==1)-cond(lambda x:x[5]==1,lambda x:x[4]==0);affirm=cond(lambda x:x[3]==1,lambda x:x[1]==1)-cond(lambda x:x[3]==1,lambda x:x[1]==0)
            metrics[key]={'state_accuracy':str(accuracy),'evaluator_cue_shift':str(cue),'prompt_affirmation_shift':str(affirm),'report_R1_given_E0':str(cond(lambda x:x[2]==1,lambda x:x[4]==0)),'report_R1_given_E1':str(cond(lambda x:x[2]==1,lambda x:x[4]==1))}
    tv={reg:str(Fraction(sum(abs(a[6]-b[6]) for a,b in zip(tables[(reg,'state_readout')],tables[(reg,'prompt_only')])),32000)) for reg in ['observational','crossed']}
    return {'tables':tables,'metrics':metrics,'total_variation':tv}
def review_b3():
    p=ROOT/'research/consciousness-v3/round3';expected=expected_b3();lookup={k:{tuple(row[:6]):row[6] for row in rows} for k,rows in expected['tables'].items()};rows=list(csv.DictReader((p/'joint_states.csv').open()));assert len(rows)==256
    for r in rows:
        key=(r['regime'],r['mechanism']);state=tuple(int(r[x]) for x in ['Z','P','R','F','E','V']);value=Fraction(lookup[key][state],16000);assert Fraction(r['probability_exact'])==value;close(float(r['probability']),float(value),1e-15)
    conditional=list(csv.DictReader((p/'conditional_tables.csv').open()));assert len(conditional)==24
    for r in conditional:
        data=expected['tables'][(r['regime'],r['mechanism'])];z,pp,e=(int(r[k]) for k in ['Z','P','E']);selected=[x for x in data if x[0]==z and x[1]==pp and x[4]==e];den=sum(x[6] for x in selected);assert den>0 and Fraction(r['conditioning_mass_exact'])==Fraction(den,16000)
        for field,event in [('P_R1_exact',lambda x:x[2]==1),('state_accuracy_exact',lambda x:x[2]==x[0]),('P_F1_exact',lambda x:x[3]==1),('P_V1_exact',lambda x:x[5]==1)]:assert Fraction(r[field])==Fraction(sum(x[6] for x in selected if event(x)),den)
    for r in csv.DictReader((p/'mechanism_summary.csv').open()):
        key=(r['regime'],r['mechanism']);ex=expected['metrics'][key];assert Fraction(r['state_accuracy_exact'])==Fraction(ex['state_accuracy']);assert Fraction(r['prompt_affirmation_shift_exact'])==Fraction(ex['prompt_affirmation_shift']);assert Fraction(r['evaluator_verdict_shift_exact'])==Fraction(ex['evaluator_cue_shift']);assert Fraction(r['evaluator_report_shift_exact'])==0
        data=expected['tables'][key]
        def contrast(i):
            vals=[]
            for bit in [0,1]:
                ss=[x for x in data if x[i]==bit];vals.append(Fraction(sum(x[6] for x in ss if x[2]==1),sum(x[6] for x in ss)))
            return vals[1]-vals[0]
        assert Fraction(r['state_report_contrast_exact'])==contrast(0);assert Fraction(r['prompt_report_contrast_exact'])==contrast(1)
    result=json.loads((p/'results.json').read_text())['metrics'];close(result['observational_joint_total_variation'],0,1e-15);close(result['crossed_joint_total_variation'],float(Fraction(expected['total_variation']['crossed'])),1e-15)
    return {'exact_weighted_joint_states_checked':256,'exact_conditional_rows_checked':24,'integer_denominator':16000,'total_variation_exact':expected['total_variation'],'crossed_state_accuracy_exact':{'state_readout':'9/10','prompt_only':'1/2'},'evaluator_cue_verdict_shift_exact':'1/4','prompt_affirmation_shift_exact':'4/5','proof':'When P=Z the two report channels coincide on all observed cells. Crossed independent P,Z exposes their off-diagonal difference. Summing the stipulated evaluator channel changes V by1/4 under E while the R marginal is unchanged. These are functional channel identities, without a phenomenal-consciousness variable or observed AI/human judgments.'}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('id',choices=['S1A','S1B','S2A','S2B','S3A','S3B','S4A','S4B','S5A','S5B','B1','B2','B3']);ap.add_argument('--precompute',action='store_true');args=ap.parse_args()
    OUT.mkdir(exist_ok=True)
    result=expected_s1a()
    rows=result.pop('rows')
    if args.precompute:
        if args.id!='S1A': raise SystemExit('Only S1A has this precompute command; other precomputes are recorded explicitly.')
        with (OUT/'S1A-independent-transfer.csv').open('w',newline='') as f:
            w=csv.writer(f);w.writerow(['k','frequency_hz','real','imag']);w.writerows(rows)
        (OUT/'S1A-precompute.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps(result,indent=2))
    else:
        print(json.dumps({'S1A':review_s1a,'S1B':review_s1b,'S2A':review_s2a,'S2B':review_s2b,'S3A':review_s3a,'S3B':review_s3b,'S4A':review_s4a,'S4B':review_s4b,'S5A':review_s5a,'S5B':review_s5b,'B1':review_b1,'B2':review_b2,'B3':review_b3}[args.id](),indent=2))
if __name__=='__main__': main()
