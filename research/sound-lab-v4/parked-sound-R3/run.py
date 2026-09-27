"""Known-frequency mono separation with explicit finite-block rank diagnostics."""
from pathlib import Path
import json
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from common import csv, finish, plt, savefig, sha, writejson
import numpy as np
from scipy.io import wavfile

HERE = Path(__file__).resolve().parent


def harmonic_design(sample_rate, target_frequency, reference_frequency, block_samples):
    if not isinstance(block_samples,(int,np.integer)) or block_samples<4:
        raise ValueError("integer block size of at least four required")
    if not np.isfinite(sample_rate) or sample_rate<=0:
        raise ValueError("finite positive sample rate required")
    if not all(np.isfinite(f) and 0<f<sample_rate/2 for f in [target_frequency,reference_frequency]):
        raise ValueError("declared frequencies must be positive and below Nyquist")
    tau = (np.arange(block_samples)-(block_samples-1)/2)/sample_rate
    return np.column_stack([fn(2*np.pi*f*tau) for f in [target_frequency,reference_frequency] for fn in [np.cos,np.sin]])


def extract_blocks(samples, sample_rate=8000, target_frequency=500, reference_frequency=1000,
                   block_samples=64, max_condition=10):
    y=np.asarray(samples,dtype=float)
    if y.ndim!=1 or not np.all(np.isfinite(y)) or len(y)<block_samples or len(y)%block_samples:
        raise ValueError("finite mono samples containing complete declared blocks required")
    if not np.isfinite(max_condition) or max_condition<1:
        raise ValueError("finite condition threshold at least one required")
    design=harmonic_design(sample_rate,target_frequency,reference_frequency,block_samples)
    u,s,vh=np.linalg.svd(design,full_matrices=False)
    rank=int(np.linalg.matrix_rank(design))
    condition=float(s[0]/s[-1]) if rank==4 else None
    coefs=np.linalg.lstsq(design,y.reshape(-1,block_samples).T,rcond=None)[0].T
    amplitudes=np.column_stack((np.hypot(coefs[:,0],coefs[:,1]),np.hypot(coefs[:,2],coefs[:,3])))
    centers=(np.arange(len(amplitudes))*block_samples+(block_samples-1)/2)/sample_rate
    residual=y.reshape(-1,block_samples)-coefs@design.T
    selected=(centers>=.05)&(centers<=.95)
    slopes=None
    if selected.sum()>=2 and np.all(amplitudes[selected]>0):
        fit=np.column_stack((centers[selected],np.ones(selected.sum())))
        slopes=np.linalg.lstsq(fit,np.log(amplitudes[selected]),rcond=None)[0][0].tolist()
    admitted=rank==4 and condition<=max_condition and slopes is not None
    diagnostic=None if slopes is None else slopes[1]-slopes[0]
    return {"domainDimension":4,"rank":rank,"nullity":4-rank,"singularValues":s.tolist(),
            "condition":condition,"admitted":bool(admitted),"blockCenters_s":centers.tolist(),
            "amplitudes_FS":amplitudes.tolist(),"coefficients_FS":coefs.tolist(),
            "blockResidualRMS_FS":np.sqrt(np.mean(residual**2,axis=1)).tolist(),
            "selectedBlocks":np.flatnonzero(selected).tolist(),"slopes_per_s":slopes,
            "diagnosticCorrectedAlpha_per_s":diagnostic,
            "correctedAlpha_per_s":diagnostic if admitted else None,
            "status":"conditional_known_frequency_extraction" if admitted else "withheld_rank_condition_or_envelope"}


def main():
    contract=json.loads((HERE/"contract.json").read_text());m=contract["model"]
    fs=m["sampleRate_Hz"];n=int(fs*m["duration_s"]);block=m["blockSamples"]
    t=np.arange(n)/fs
    center_for_sample=(np.floor(np.arange(n)/block)*block+(block-1)/2)/fs
    fsig=m["targetFrequency_Hz"];fref=m["referenceFrequency_Hz"]
    alpha=m["targetAlpha_per_s"];beta=m["sharedBeta_per_s"]
    def waveform(freq,exact=False):
        envelope_time=center_for_sample if exact else t
        return m["targetAmplitude_FS"]*np.exp((-alpha+beta)*envelope_time)*np.cos(2*np.pi*fsig*t+m["targetPhase_rad"])+m["referenceAmplitude_FS"]*np.exp(beta*envelope_time)*np.cos(2*np.pi*freq*t+m["referencePhase_rad"])
    rng=np.random.default_rng(2026092703)
    noise=rng.uniform(-1e-4,1e-4,n)
    cases=[("smooth",fref,waveform(fref)),("exact_blocks",fref,waveform(fref,True)),
           ("bounded_noise",fref,waveform(fref)+noise),("collision",fsig,waveform(fsig)),
           ("near_collision",505,waveform(505))]
    results={};files=[];fig,axes=plt.subplots(1,2,figsize=(11,4))
    for name,freq,values in cases:
        assert np.max(np.abs(values))<1
        pcm=np.rint(values*32767).astype(np.int16);wavfile.write(HERE/(name+".wav"),fs,pcm)
        readfs,readpcm=wavfile.read(HERE/(name+".wav"));assert readfs==fs and np.array_equal(pcm,readpcm)
        result=extract_blocks(readpcm.astype(float)/32767,fs,fsig,freq,block)
        centers=np.array(result["blockCenters_s"]);amps=np.array(result["amplitudes_FS"])
        truth=np.column_stack((m["targetAmplitude_FS"]*np.exp((-alpha+beta)*centers),m["referenceAmplitude_FS"]*np.exp(beta*centers)))
        result.update({"rawSHA256":sha(HERE/(name+".wav")),"referenceFrequency_Hz":freq,
                       "maxAmplitudeAbsError_FS":float(np.max(np.abs(amps-truth))),
                       "maxAmplitudeRelativeError":float(np.max(np.abs(amps/truth-1))),
                       "noiseGuaranteeScope":"additive sample errors only; within-block model discrepancy not included"})
        results[name]=result
        csv(HERE/(name+"-blocks.csv"),["time_s","target_amplitude_FS","reference_amplitude_FS","target_center_truth_FS","reference_center_truth_FS","residual_RMS_FS"],np.column_stack((centers,amps,truth,result["blockResidualRMS_FS"])))
        files.extend([name+".wav",name+"-blocks.csv"])
        if name in ["smooth","exact_blocks","bounded_noise"]:
            axes[0].plot(centers,100*(amps[:,0]/truth[:,0]-1),label=name.replace("_"," "))
    collision_design=harmonic_design(fs,fsig,fsig,block)
    witness=np.array([1.,0.,-1.,0.]);kernel_residual=float(np.linalg.norm(collision_design@witness))
    matrices={"collision":{"matrix":collision_design.tolist(),"domainDimension":4,"rank":2,"nullity":2,"kernelWitness":witness.tolist(),"kernelResidual":kernel_residual},
              "nominal":{"domainDimension":4,"rank":results["smooth"]["rank"],"nullity":results["smooth"]["nullity"],"condition":results["smooth"]["condition"]},
              "nearCollision":{"domainDimension":4,"rank":results["near_collision"]["rank"],"nullity":results["near_collision"]["nullity"],"condition":results["near_collision"]["condition"]}}
    metrics={"smoothCorrectedAlpha_per_s":results["smooth"]["correctedAlpha_per_s"],
             "smoothAlphaAbsError_per_s":abs(results["smooth"]["correctedAlpha_per_s"]-alpha),
             "smoothMaxEnvelopeRelativeError":results["smooth"]["maxAmplitudeRelativeError"],
             "exactBlockMaxAmplitudeError_FS":results["exact_blocks"]["maxAmplitudeAbsError_FS"],
             "exactBlockCorrectedAlpha_per_s":results["exact_blocks"]["correctedAlpha_per_s"],
             "boundedNoiseCorrectedAlpha_per_s":results["bounded_noise"]["correctedAlpha_per_s"],
             "boundedNoiseActualMax_FS":float(np.max(np.abs(noise))),
             "nominalCondition":results["smooth"]["condition"],
             "collisionRank":results["collision"]["rank"],"collisionNullity":results["collision"]["nullity"],
             "collisionKernelResidual":kernel_residual,"collisionCorrection":results["collision"]["correctedAlpha_per_s"],
             "nearCollisionCondition":results["near_collision"]["condition"],
             "nearCollisionDiagnosticAlpha_per_s":results["near_collision"]["diagnosticCorrectedAlpha_per_s"],
             "nearCollisionCorrection":results["near_collision"]["correctedAlpha_per_s"]}
    checks={"nominalRecovery":metrics["smoothAlphaAbsError_per_s"]<=.05,
            "exactBlockAmplitude":metrics["exactBlockMaxAmplitudeError_FS"]<=.0001,
            "nominalRankCondition":results["smooth"]["rank"]==4 and metrics["nominalCondition"]<=10,
            "collisionKernel":metrics["collisionRank"]==2 and metrics["collisionNullity"]==2 and kernel_residual<=1e-10,
            "collisionWithheld":metrics["collisionCorrection"] is None,
            "nearCollisionWithheld":metrics["nearCollisionCondition"]>10 and metrics["nearCollisionCorrection"] is None,
            "noiseBound":metrics["boundedNoiseActualMax_FS"]<=1e-4}
    writejson(HERE/"case-results.json",results);writejson(HERE/"identifiability.json",matrices)
    csv(HERE/"sample-noise.csv",["time_s","added_noise_FS"],np.column_stack((t,noise)))
    axes[0].set(xlabel="Block center (s)",ylabel="Target amplitude error (%)",title="Within-block evolution leaves model error");axes[0].legend(fontsize=8)
    axes[1].bar(["Separated 1000 Hz","Nearby 505 Hz"],[metrics["nominalCondition"],metrics["nearCollisionCondition"]],color=["#267c85","#b35231"])
    axes[1].axhline(10,color="black",ls="--",label="Frozen gate κ ≤ 10")
    axes[1].set(ylabel="Design condition number",title="Full rank alone is insufficient");axes[1].legend(fontsize=8)
    savefig(fig,HERE/"figure.svg")
    report="""# R3 — one-channel, known-frequency extraction

Five generated mono PCM16 files were written then decoded. No physical recording was made. The four design columns are cosine/sine at each declared frequency over 64-sample (8 ms) blocks. Block centers are (start_sample+31.5)/8000 s; each design uses time relative to its center. Least-squares cosine/sine coefficients give amplitudes by their Euclidean norms. OLS log-amplitude rates use centers from .05 to .95 s inclusive. These known frequencies are inputs, not discoveries from arbitrary audio.

The smooth exponential fixture changes amplitude within a block, violating the constant-coefficient extraction model. Its relative envelope error is explicitly reported and plotted. The piecewise-center-amplitude fixture is an exact block model; its remaining amplitude error comes from PCM quantization and numerical error. A separately saved bounded sample-noise draw is added before quantization. Its supplied ±.0001 FS bound does not cover within-block model discrepancy.

Rank four and condition number at most ten are frozen admission requirements. Identical 500 Hz frequencies give rank two in a four-dimensional domain with kernel witness (1,0,−1,0). A 505 Hz reference remains rank four but is badly conditioned and is rejected. Unconstrained diagnostic slopes remain visible; neither rejected case receives a separated correction.

Run: `python research/sound-lab-v4/R3/run.py`. The fixed fixture validates a conditional numerical extraction method. Unmodeled tones, unknown frequencies, temporal variation, acoustic mixing and nonlinear or frequency-dependent recording gain remain unvalidated. A well-conditioned fit does not establish an independently stable physical reference.
"""
    finish(HERE,metrics,"Known separated tones can be extracted from the generated mono signal; coincident or poorly conditioned frequencies withhold correction, and within-block evolution remains a separate error.",[{"control":"frequency collision","outcome":"rank-deficient: correction withheld"},{"control":"near collision","outcome":"condition above gate: correction withheld"},{"control":"smooth envelopes","outcome":"within-block discrepancy retained explicitly"}],report,files+["case-results.json","identifiability.json","sample-noise.csv","figure.svg"],checks)


if __name__=="__main__":main()
