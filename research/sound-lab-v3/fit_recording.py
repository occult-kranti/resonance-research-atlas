"""Bounded WAV/CSV intake and local single-mode decay fit. No playback or acquisition."""
from pathlib import Path
import argparse,hashlib,json
import numpy as np
from scipy.io import wavfile
from scipy.optimize import least_squares
def read_recording(path,channel=0):
    path=Path(path)
    if path.stat().st_size>20_000_000: raise ValueError('File exceeds 20 MB intake bound')
    if path.suffix.lower()=='.wav':
        fs,z=wavfile.read(path);channels=1 if z.ndim==1 else z.shape[1]
        if not 0<=channel<channels: raise ValueError('Channel unavailable')
        z=z if z.ndim==1 else z[:,channel]
        if z.dtype.kind=='i': y=z.astype(float)/float(2**(8*z.dtype.itemsize-1))
        elif z.dtype==np.uint8: y=(z.astype(float)-128)/128
        elif z.dtype.kind=='f': y=z.astype(float)
        else: raise ValueError('Unsupported WAV encoding')
        t=np.arange(len(y))/fs
    elif path.suffix.lower()=='.csv':
        z=np.genfromtxt(path,delimiter=',',names=True)
        if z.dtype.names!=('time_s','amplitude_FS'): raise ValueError('CSV header must be time_s,amplitude_FS')
        t=np.atleast_1d(z['time_s']);y=np.atleast_1d(z['amplitude_FS']);channels=1
        if len(t)<4 or np.any(np.diff(t)<=0): raise ValueError('Time must increase with at least four samples')
        dt=np.median(np.diff(t));fs=1/dt
        if not np.allclose(np.diff(t),dt,rtol=1e-4,atol=1e-10): raise ValueError('CSV time samples must be uniform')
        t=t-t[0]
    else: raise ValueError('Use WAV or two-column CSV')
    if len(y)<4 or not np.all(np.isfinite(y)) or not np.all(np.isfinite(t)): raise ValueError('Empty/nonfinite recording')
    if not 1000<=fs<=192000 or len(y)/fs>60: raise ValueError('Require 1–192 kHz and at most 60 seconds')
    meta={'inputSHA256':hashlib.sha256(path.read_bytes()).hexdigest(),'sampleRate_Hz':float(fs),'samples':len(y),'channels':channels,'channel':channel,'duration_s':len(y)/fs,'samplePeak_FS':float(np.max(np.abs(y))),'clippedSamples':int(np.sum(np.abs(y)>=32767/32768))}
    return t,y,meta
def analyze(path,frequency=500,start=.05,stop=.8,alpha_max=20,channel=0):
    t,y,meta=read_recording(path,channel)
    if not all(np.isfinite([frequency,start,stop,alpha_max])) or not 0<=start<stop<=t[-1]+1/meta['sampleRate_Hz'] or not 0<alpha_max<=100: raise ValueError('Invalid fit window/bound')
    if not 50<frequency<.45*meta['sampleRate_Hz']: raise ValueError('Nominal frequency out of range')
    m=(t>=start)&(t<stop);t=t[m];y=y[m]
    if len(y)<64: raise ValueError('Fit window needs at least 64 samples')
    rms=float(np.sqrt(np.mean(y*y)));meta.update({'window_s':[start,stop],'windowRMS_FS':rms,'model':'single exponential cosine+sin+offset','evidenceType':'user_supplied_file_unverified','scope':'Recorded-channel local fit; no material identity or physical measurement provenance assumed'})
    reasons=[]
    if rms<1e-6: reasons.append('silence_or_insufficient_signal')
    if meta['clippedSamples']: reasons.append('full_file_clipping')
    if reasons: return meta|{'status':'rejected','flags':reasons},np.column_stack([t,y,np.zeros_like(y),y])
    tr=t-start
    def solve(theta):
        alpha,f=theta;dec=np.exp(-alpha*tr);M=np.column_stack([dec*np.cos(2*np.pi*f*tr),dec*np.sin(2*np.pi*f*tr),np.ones_like(tr)]);beta=np.linalg.lstsq(M,y,rcond=None)[0];return M@beta,beta
    def residual(theta): return (solve(theta)[0]-y)/rms
    lo=[0,frequency-50];hi=[alpha_max,frequency+50]
    opt=least_squares(residual,[min(2,alpha_max/2),frequency-.5],bounds=(lo,hi),ftol=1e-12,xtol=1e-12,gtol=1e-12,max_nfev=200)
    pred,beta=solve(opt.x);nr=float(np.linalg.norm(pred-y)/np.linalg.norm(y));near=bool(np.any((opt.x-np.array(lo))<1e-4) or np.any((np.array(hi)-opt.x)<1e-4));flags=[]
    if not opt.success: flags.append('optimizer_failed')
    if near: flags.append('near_search_bound')
    if nr>.05: flags.append('single_mode_residual_over_5_percent')
    result=meta|{'status':'fit_with_flags' if flags else 'fit','flags':flags,'alpha_per_s':float(opt.x[0]),'frequency_Hz':float(opt.x[1]),'gain_at_window_start_FS':float(np.hypot(*beta[:2])),'phase_at_window_start_rad':float(np.arctan2(-beta[1],beta[0])),'offset_FS':float(beta[2]),'normalizedResidual':nr,'optimizerSuccess':bool(opt.success),'optimizerEvaluations':int(opt.nfev),'bounds':{'alpha_per_s':lo[:1]+hi[:1],'frequency_Hz':[lo[1],hi[1]]}}
    return result,np.column_stack([t,y,pred,y-pred])
def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('input');parser.add_argument('--frequency',type=float,required=True);parser.add_argument('--start',type=float,required=True);parser.add_argument('--stop',type=float,required=True);parser.add_argument('--alpha-max',type=float,default=20);parser.add_argument('--channel',type=int,default=0);parser.add_argument('--output',required=True);a=parser.parse_args()
    result,trace=analyze(a.input,a.frequency,a.start,a.stop,a.alpha_max,a.channel);out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);out.with_suffix('.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');np.savetxt(out.with_suffix('.csv'),trace,delimiter=',',header='time_s,amplitude_FS,fit_FS,residual_FS',comments='',fmt='%.17g');print(json.dumps(result,indent=2))
if __name__=='__main__': main()
