from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from common import *
p=Path(__file__).parent;c=json.loads((p/'contract.json').read_text());q=c['parameters'];fs=q['sampleRate_Hz'];n=q['nfft']
x=np.random.default_rng(q['seedA']).normal(0,q['probeStd_FS'],q['probeSamples']);b=np.random.default_rng(q['seedB']).normal(0,q['probeStd_FS'],q['probeSamples'])
d=np.array([.7,.2,.1]);e=np.zeros(41);e[0]=1;e[40]=.6;h=np.convolve(d,e)
y=np.convolve(x,h);yb=np.convolve(b,h);X=np.fft.rfft(x,n);Y=np.fft.rfft(y,n);H=np.fft.rfft(h,n);f=np.fft.rfftfreq(n,1/fs)
excited=np.abs(X)>=q['inputMaskFraction']*np.max(np.abs(X));assert excited.all()
est=Y/X;hp=np.fft.irfft(est,n);pred=np.fft.irfft(np.fft.rfft(b,n)*est,n)
band=(f>=100)&(f<=3500)&excited
superpos=np.convolve(x+b,h)-y-yb
# This inverse concerns H, not X. Fs/n places some (but not all) exact comb zeros on DFT bins.
e_zero=e.copy();e_zero[-1]=1;Hz=np.fft.rfft(np.convolve(d,e_zero),n);dead=np.abs(Hz)<q['inverseHMask'];inverse=np.zeros_like(Hz);inverse[~dead]=1/Hz[~dead]
alternative=np.convolve(x,np.convolve(h,[1.]));metrics={'total_transfer_max_complex_error':float(np.max(np.abs(est[band]-H[band]))),'heldout_relative_L2':float(np.linalg.norm(pred[:len(yb)]-yb)/np.linalg.norm(yb)),'superposition_relative_L2':float(np.linalg.norm(superpos)/np.linalg.norm(y+yb)),'factorization_relative_L2':float(np.linalg.norm(alternative-y)/np.linalg.norm(y)),'declared_echo_delay_s':40/fs,'declared_comb_spacing_Hz':fs/40,'inverse_H_zero_bins':int(dead.sum()),'input_X_excluded_bins':int((~excited).sum()),'impulse_max_error':float(np.max(np.abs(hp[:len(h)]-h)))}
assert metrics['total_transfer_max_complex_error']<1e-10 and metrics['heldout_relative_L2']<1e-10 and metrics['superposition_relative_L2']<1e-12 and metrics['factorization_relative_L2']<1e-12 and dead.sum()>0
csv(p/'response.csv',['bin','frequency_Hz','true_real','true_imag','estimate_real','estimate_imag','r0_magnitude','r1_magnitude','inverse_H_excluded'],np.column_stack([np.arange(len(f)),f,H.real,H.imag,est.real,est.imag,np.abs(np.fft.rfft(d,n)),np.abs(Hz),dead]))
csv(p/'probe_outputs.csv',['sample','time_s','heldout_actual_FS','heldout_prediction_FS','error_FS'],np.column_stack([np.arange(len(yb)),np.arange(len(yb))/fs,yb,pred[:len(yb)],pred[:len(yb)]-yb]))
csv(p/'impulse.csv',['sample','true_H','estimated_H'],np.column_stack([np.arange(100),np.pad(h,(0,100-len(h))),hp[:100]]))
fig,ax=plt.subplots(2,1,figsize=(9,6));m=(f>=100)&(f<=1500);ax[0].plot(f[m],20*np.log10(np.abs(H[m])),label='Known total chain');ax[0].plot(f[m],20*np.log10(np.abs(np.fft.rfft(d,n)[m])),label='r=0 control');ax[0].set(xlabel='Frequency (Hz)',ylabel='Transfer magnitude (dB FS/FS)',title='Synthetic two-path response: a comb is not material identity');ax[0].legend();ax[1].stem(np.arange(len(h))/fs*1000,h,basefmt=' ');ax[1].set(xlabel='Delay (ms)',ylabel='Impulse coefficient (FS/FS)',title='Same total impulse: device × echo or one composite device');savefig(fig,p/'figure.svg')
finding='Total complex transfer is recovered to numerical precision; two distinct device/echo factorizations give exactly the same output.'
finish(p,metrics,finding,[{'control':'Infer physical echo from total response alone','outcome':'rejected','reason':'d_alt=d*e and e_alt=delta is an exact output-equivalent counterexample'}],'''# S1A — total response and its ambiguous cause

Synthetic, noiseless digital FIR benchmark. No physical sound was recorded. The direct complex ratio recovers the total transfer and predicts a second independently generated probe. The source and output arrays are linearly convolved with sufficient zero padding; no averaging-based estimator is claimed.

The 5 ms/200 Hz echo parameters belong to the declared fixture. They are recoverable after dividing by the independently declared device FIR, but total response alone cannot assign the feature to the room, device, or material. The explicit alternative puts the entire filter in the device. The r=0 control removes the echo comb. The r=1 control has exact transfer zeros; these are excluded from inverse-H without confusing them with unexcited input bins.

Next missing premise: stability and nonzero sensitivity of the recording chain under noise and placement changes. The low-material protocol will hold phone/speaker geometry fixed and retain reference and movement controls. Numerical success here does not validate a phone, loudspeaker, calibrated pressure measurement, or object.

Sources: Farina 2000, theory pp.2–4 (LTI convolution, time variation, ratio deconvolution); Julius O. Smith, Feedforward Comb Filters (difference equation and delayed-path model). Equations and plots are original implementation, not copied figures.
''',['response.csv','probe_outputs.csv','impulse.csv','figure.svg'])
