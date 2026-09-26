#!/usr/bin/env python3
"""N5 actual PCM16 evidence: linear spectra vs a declared quadratic detector."""
from pathlib import Path
import csv,hashlib,json,platform,wave
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent
KINDS=("two-tone","am","baseband","carrier");RATE=48000;N=4096;OFFSET=32768
GAIN=10**(-24/20);RAW_TOL=2**-14;SQUARE_TOL=1e-5

def coefficients(values):
    out=np.fft.rfft(values)/len(values);out[1:-1]*=2
    return out
def pair(z):return [float(z.real),float(z.imag)]

def run():
    inputs=json.loads((ROOT/"inputs.json").read_text())
    for name,meta in inputs["files"].items():
        raw=(ROOT/name).read_bytes()
        assert len(raw)==meta["bytes"] and hashlib.sha256(raw).hexdigest()==meta["sha256"],name
    frequency=np.fft.rfftfreq(N,1/RATE);transfer=1/(1+1j*frequency/200);transfer[-1]=transfer[-1].real
    expected={"two-tone":{31:-1j*GAIN/2,33:-1j*GAIN/2},"am":{30:GAIN/4,32:-1j*GAIN/2,34:-GAIN/4},"baseband":{2:-1j*GAIN},"carrier":{32:-1j*GAIN}}
    quadratic={"two-tone":{2:GAIN**2/4,4:0},"am":{2:-1j*GAIN**2/4,4:-GAIN**2/16},"baseband":{2:0,4:-GAIN**2/2},"carrier":{2:0,4:0}}
    cases=[];spectral=[];signals={};all_format=True
    for kind in KINDS:
        manifest=json.loads((ROOT/"assets"/f"{kind}.json").read_text());wav=ROOT/"assets"/f"{kind}.wav"
        assert hashlib.sha256(wav.read_bytes()).hexdigest()==manifest["wavSha256"]
        with wave.open(str(wav),"rb") as file:
            all_format &= file.getnchannels()==2 and file.getsampwidth()==2 and file.getframerate()==RATE and file.getnframes()==96000
            samples=np.frombuffer(file.readframes(file.getnframes()),dtype="<i2").reshape(-1,2)
        all_format &= bool(np.array_equal(samples[:,0],samples[:,1])) and manifest["physicalCalibration"] is None
        u=samples[OFFSET:OFFSET+N,0].astype(float)/32768;signals[kind]=u
        coeff=coefficients(u);filtered=np.fft.irfft(np.fft.rfft(u)*transfer,n=N);linear=coefficients(filtered)
        squared=coefficients(u*u);rms=float(np.sqrt(np.mean(u*u)));factor=.02/rms;matched=u*factor;matched_q=coefficients(matched*matched)
        bins=sorted(set(expected[kind])|{2,4})
        raw_error=max(abs(coeff[k]-expected[kind].get(k,0)) for k in bins)
        linear_error=max(abs(linear[k]-expected[kind].get(k,0)*transfer[k]) for k in bins)
        square_error=max(abs(squared[k]-value) for k,value in quadratic[kind].items())
        row=dict(kind=kind,interior_rms_FS=rms,rate_line_raw_FS=float(abs(coeff[2])),rate_line_linear_FS=float(abs(linear[2])),
                 rate_line_squared_FS2=float(abs(squared[2])),twice_rate_squared_FS2=float(abs(squared[4])),
                 quadratic_rate_complex_FS2=pair(squared[2]),raw_max_complex_error_FS=float(raw_error),linear_max_complex_error_FS=float(linear_error),
                 quadratic_max_complex_error_FS2=float(square_error),rms_match_scale=factor,matched_rms_FS=float(np.sqrt(np.mean(matched*matched))),
                 matched_quadratic_rate_amplitude_FS2=float(abs(matched_q[2])),matched_quadratic_scaling_error_FS2=float(abs(matched_q[2]-factor**2*squared[2])))
        cases.append(row)
        for k in range(86):spectral.append(dict(kind=kind,bin=k,frequency_Hz=float(frequency[k]),raw_peak_amplitude_FS=float(abs(coeff[k])),linear_peak_amplitude_FS=float(abs(linear[k])),quadratic_peak_amplitude_FS2=float(abs(squared[k]))))
    two=signals["two-tone"];ft=np.fft.rfft(two);ft[33]*=-1;flipped=np.fft.irfft(ft,n=N)
    original_q=coefficients(two*two)[2];flipped_q=coefficients(flipped*flipped)[2]
    phase_control=dict(original_rate_complex_FS2=pair(original_q),flipped_rate_complex_FS2=pair(flipped_q),
                       phase_reversal_error_FS2=float(abs(flipped_q+original_q)),
                       rms_change_FS=float(abs(np.sqrt(np.mean(two*two))-np.sqrt(np.mean(flipped*flipped)))))
    checks=[
        dict(name="actual_production_hash_format_and_raw_complex_lines",passed=all_format and max(v["raw_max_complex_error_FS"] for v in cases)<=RAW_TOL),
        dict(name="linear_filter_changes_gain_not_frequency",passed=max(v["linear_max_complex_error_FS"] for v in cases)<=RAW_TOL and all(v["rate_line_linear_FS"]<=RAW_TOL for v in cases if v["kind"] in ("two-tone","am"))),
        dict(name="quadratic_mixing_signed_line_controls",passed=max(v["quadratic_max_complex_error_FS2"] for v in cases)<=SQUARE_TOL),
        dict(name="equal_RMS_scaling_and_blank",passed=all(abs(v["matched_rms_FS"]-.02)<1e-12 and v["matched_quadratic_scaling_error_FS2"]<1e-12 for v in cases) and bool(np.all(coefficients(np.zeros(N))==0))),
        dict(name="phase_witness_preserves_RMS_reverses_difference_signal",passed=phase_control["rms_change_FS"]<1e-12 and phase_control["phase_reversal_error_FS2"]<SQUARE_TOL)
    ]
    for filename,rows in (("decoded_spectrum.csv",spectral),("signal_comparison.csv",[{k:v for k,v in row.items() if not isinstance(v,list)} for row in cases])):
        with (ROOT/filename).open("w",newline="") as stream:writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    x=np.arange(4);labels=["Two-tone","AM","Actual baseband","Carrier"]
    fig,axes=plt.subplots(1,3,figsize=(12,4.4),layout="constrained")
    axes[0].bar(x,[v["rate_line_raw_FS"] for v in cases],color="#3659b8");axes[0].axhline(RAW_TOL,color="#555555",ls=":",label="Declared quantization floor")
    axes[0].set(ylabel="23.4375Hz peak amplitude (FS)",title="Raw decoded waveform")
    axes[1].bar(x,[v["rate_line_squared_FS2"] for v in cases],color="#bc4b37");axes[1].set(ylabel="23.4375Hz peak amplitude (FS²)",title="Explicit nonlinear detector u²")
    axes[2].bar(x,[v["matched_quadratic_rate_amplitude_FS2"] for v in cases],color="#16766c");axes[2].set(ylabel="23.4375Hz peak amplitude (FS²)",title="u² after equal digital RMS =0.02FS")
    for ax in axes:ax.set_xticks(x,labels,rotation=22,ha="right");ax.grid(axis="y",alpha=.2)
    axes[0].legend(fontsize=7)
    for ext in ("svg","png"):fig.savefig(ROOT/f"audio_observation_operators.{ext}",dpi=170,bbox_inches="tight",metadata={"Date":None} if ext=="svg" else {})
    plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(9,4),layout="constrained")
    for label,z,color in (("Original",original_q,"#3659b8"),("Upper tone reversed",flipped_q,"#bc4b37")):
        axes[0].quiver(0,0,z.real,z.imag,angles="xy",scale_units="xy",scale=1,color=color,label=label)
    lim=GAIN**2/3;axes[0].set(xlim=(-lim,lim),ylim=(-lim,lim),xlabel="Real quadratic rate coefficient (FS²)",ylabel="Imaginary coefficient (FS²)",title="A phase-sensitive predicted witness");axes[0].legend(fontsize=8);axes[0].grid(alpha=.2)
    times=np.arange(N)/RATE;axes[1].plot(times[:600],two[:600],label="Original",lw=1);axes[1].plot(times[:600],flipped[:600],label="Upper tone reversed",lw=1)
    axes[1].set(xlabel="Time within interior segment (s)",ylabel="Digital amplitude (FS)",title="Same RMS, changed interference phase");axes[1].legend(fontsize=8);axes[1].grid(alpha=.2)
    for ext in ("svg","png"):fig.savefig(ROOT/f"phase_witness.{ext}",dpi=170,bbox_inches="tight",metadata={"Date":None} if ext=="svg" else {})
    plt.close(fig)
    eps=2**-15
    result=dict(round=5,branch="nanoparticles",final_round=True,status="passed" if all(c["passed"] for c in checks) else "failed",
                hypothesis="NP-H5 decoded spectrum, calibrated linear transfer and explicit nonlinear rate detection are distinct; phase witness tests mixing route",
                analysis=dict(sample_rate_Hz=RATE,segment_frames=N,start_frame=OFFSET,carrier_Hz=375,rate_Hz=23.4375,gain_FS=GAIN,lti_corner_Hz=200,equal_RMS_FS=.02),
                cases=cases,phase_control=phase_control,quantization=dict(sample_error_bound_FS=eps,raw_line_tolerance_FS=RAW_TOL,squared_derived_line_bound_FS2=2*(2*GAIN*eps+eps**2),squared_declared_tolerance_FS2=SQUARE_TOL),checks=checks,
                scope="Actual project audio bytes; mathematical detectors only. No transducer, magnetic field, nanoparticle force or human effect was measured.",
                runtime=dict(python=platform.python_version(),numpy=np.__version__,matplotlib=matplotlib.__version__),hashes={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in ("contract.md","sources.md","inputs.json","regenerate_assets.mjs","solver.py")})
    (ROOT/"results.json").write_text(json.dumps(result,indent=2)+"\n");print(json.dumps(result,indent=2))
    if result["status"]!="passed":raise SystemExit(1)
if __name__=="__main__":run()
