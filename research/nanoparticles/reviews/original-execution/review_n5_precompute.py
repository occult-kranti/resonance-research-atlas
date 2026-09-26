from pathlib import Path
import wave,json,hashlib,math
import numpy as np
root=Path('/tmp/nanolab-research-signals');N=4096;offset=32768;ns=np.arange(N);g=10**(-24/20)
def project(x,k):return 2/N*np.dot(x,np.exp(-2j*np.pi*k*ns/N))
cases=[];signals={}
for kind in ['two-tone','am','baseband','carrier']:
 path=root/(kind+'.wav');manifest=json.loads((root/(kind+'.json')).read_text());assert hashlib.sha256(path.read_bytes()).hexdigest()==manifest['wavSha256']
 with wave.open(str(path),'rb') as w:
  assert(w.getframerate(),w.getnchannels(),w.getsampwidth(),w.getnframes())==(48000,2,2,96000)
  data=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').reshape(-1,2);assert np.array_equal(data[:,0],data[:,1]);x=data[offset:offset+N,0].astype(float)/32768
 signals[kind]=x;rms=float(np.sqrt(np.mean(x*x)));scaled=x*.02/rms
 cases.append({'kind':kind,'wav_sha256':manifest['wavSha256'],'interior_rms_FS':rms,'raw_line_amplitudes_FS':{str(k):float(abs(project(x,k))) for k in [2,4,30,31,32,33,34]},'quadratic_line_amplitudes_FS2':{str(k):float(abs(project(x*x,k))) for k in [2,4]},'equal_RMS_quadratic_line_amplitudes_FS2':{str(k):float(abs(project(scaled*scaled,k))) for k in [2,4]}})
x=signals['two-tone'];u=project(x,33);component=u.real*np.cos(2*np.pi*33*ns/N)-u.imag*np.sin(2*np.pi*33*ns/N);flipped=x-2*component
phase={'independent_method':'Orthogonal real sin/cos projection reflection, noFFT','mean_square_difference_FS2':float(np.mean(flipped**2)-np.mean(x*x)),'beat_complex_reversal_absolute_error_FS2':float(abs(project(flipped*flipped,2)+project(x*x,2))),'original_beat_phasor':[float(v) for v in [project(x*x,2).real,project(x*x,2).imag]],'flipped_beat_phasor':[float(v) for v in [project(flipped*flipped,2).real,project(flipped*flipped,2).imag]]}
out={'computed_before_N5_producer_results':True,'method':'Pythonwave decoding and direct complex dot products, notFFT or producer imports','window':{'N':N,'start':offset,'sampleRate':48000},'cases':cases,'phase_flip_control':phase,'source_sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path('repos/brainwave_opensync/src/nanolab/model.ts'),Path('repos/brainwave_opensync/src/engine/synth.ts'),Path('repos/brainwave_opensync/src/engine/wav.ts')]}}
Path('panel-nano/advisor-N5-precompute.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'cases':[{'kind':c['kind'],'rms':c['interior_rms_FS'],'raw_rate':c['raw_line_amplitudes_FS']['2'],'quadratic':c['quadratic_line_amplitudes_FS2']} for c in cases],'phase':phase},indent=2))
