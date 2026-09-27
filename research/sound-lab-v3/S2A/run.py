from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from common import *
from scipy.io import wavfile
from fit_recording import analyze
p=Path(__file__).parent;fs=8000;t=np.arange(fs*2)/fs;rows=[];files=[];all_results=[];fig,ax=plt.subplots(2,1,figsize=(9,6))
for i,(gain,phase) in enumerate([(.1,0),(.2,1),(.3,2),(0,0),(1.2,0)]):
    y=gain*np.exp(-4*t)*np.cos(2*np.pi*500*t+phase);pcm=np.round(np.clip(y,-1,32767/32768)*32768).astype(np.int16);name=f'case{i}.wav';wavfile.write(p/name,fs,pcm);r,trace=analyze(p/name);r['evidenceType']='actualbytes_generated_PCM';all_results.append(r);csv(p/f'fit{i}.csv',['time_s','decoded_FS','fit_FS','residual_FS'],trace);files.extend([name,f'fit{i}.csv'])
    if i<3:
        assert r['optimizerSuccess'] and abs(r['alpha_per_s']-4)<.01 and abs(r['frequency_Hz']-500)<.01
        rows.append([i,gain,phase,r['alpha_per_s'],r['frequency_Hz'],r['normalizedResidual']]);ax[0].plot(trace[::16,0],np.abs(trace[::16,1]),label=f'gain {gain}, phase {phase}');ax[1].plot(trace[::16,0],trace[::16,3],alpha=.6)
assert all_results[3]['status']=='rejected' and all_results[4]['status']=='rejected'
csv(p/'fits.csv',['case','input_gain_FS','input_phase_rad','alpha_per_s','frequency_Hz','normalized_residual'],rows);writejson(p/'intake_results.json',all_results)
metrics={'max_alpha_error_per_s':max(abs(x[3]-4) for x in rows),'max_frequency_error_Hz':max(abs(x[4]-500) for x in rows),'max_normalized_residual':max(x[5] for x in rows),'silence_rejected':True,'clipping_rejected':True,'clipped_sample_count':all_results[4]['clippedSamples']}
ax[0].set(xlabel='Time (s)',ylabel='Decoded magnitude (FS)',title='Generated PCM bytes: gain changes, fitted decay stays fixed');ax[0].legend();ax[1].set(xlabel='Time (s)',ylabel='Fit residual (FS)',title='Quantization-limited local single-mode fits');savefig(fig,p/'figure.svg')
finish(p,metrics,'The shared WAV importer and local fit recover the declared decay across gain/phase cases; silence and clipped recordings are rejected.',[{'control':'Silent WAV','outcome':'rejected'},{'control':'Clipped full file','outcome':'rejected even when fit window is below clipping'}],'''# S2A — reusable recording intake

The actual files are generated PCM16 WAV bytes, decoded by the same importer available for user recordings. They are not physical tap recordings. Three gain/phase cases recover the prescribed 500 Hz, 4 s^-1 decay within the frozen tolerances, starting away from truth at 499.5 Hz and 2 s^-1. Silence and full-file clipping are rejected before fitting.

The variable-projection estimator solves amplitude, phase and offset linearly for each local frequency/decay candidate. Its nonlinear search is bounded and local. Supplying a nominal frequency is an explicit model choice, not evidence that the file contains one mode. A low residual does not make the decay intrinsic to a material.

Example: `python research/sound-lab-v3/fit_recording.py research/sound-lab-v3/S2A/case0.wav --frequency 500 --start .05 --stop .8 --output /tmp/example-fit`. For a real recording choose and prerecord its fit window, retain the raw file, and document provenance and microphone processing. CSV intake requires exactly `time_s,amplitude_FS`.

Next failure tests: nearby modes and time-varying gain. These can make a single-mode fit biased or observationally indistinguishable from a different true decay.
''',files+['fits.csv','intake_results.json','figure.svg','../fit_recording.py'])
