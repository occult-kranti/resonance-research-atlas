"""Frozen R1 synthetic reference-channel experiment, not a microphone recording."""
from pathlib import Path
import json
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import csv, finish, plt, savefig, sha, writejson
import numpy as np
from scipy.io import wavfile
from scipy.optimize import minimize_scalar

HERE = Path(__file__).resolve().parent


def estimate_slope(samples, sample_rate, frequency):
    """Variable-project signed sinusoid coefficients for a known-frequency decay."""
    y = np.asarray(samples, dtype=float)
    if y.ndim != 1 or y.size < 100 or not np.all(np.isfinite(y)):
        raise ValueError("finite one-dimensional signal of at least 100 samples required")
    if not np.isfinite(sample_rate) or not np.isfinite(frequency) or not 0 < frequency < sample_rate / 2:
        raise ValueError("finite frequency below Nyquist required")
    if np.max(np.abs(y)) < 2 / 32767:
        return None
    t = np.arange(y.size) / sample_rate
    carrier = np.column_stack((np.cos(2*np.pi*frequency*t), np.sin(2*np.pi*frequency*t)))
    def cost(slope):
        design = np.exp(slope*t)[:, None] * carrier
        coef = np.linalg.lstsq(design, y, rcond=None)[0]
        residual = y - design @ coef
        return float(residual @ residual)
    fitted = minimize_scalar(cost, bounds=(-12, 5), method="bounded", options={"xatol": 1e-12})
    if not fitted.success:
        raise RuntimeError("slope optimizer failed")
    return float(fitted.x)


def main():
    contract = json.loads((HERE / "contract.json").read_text())
    m = contract["model"]
    fs = m["sampleRate_Hz"]
    t = np.arange(round(m["time_s"][1]*fs)) / fs
    alpha = m["targetAlpha_per_s"]
    frequencies = [m["targetFrequency_Hz"], m["referenceFrequency_Hz"]]
    amplitudes = m["amplitudes_FS"]
    cases = [("common_beta0",0,0,0,amplitudes[1]),
             ("common_beta1",1,1,0,amplitudes[1]),
             ("common_beta2",2,2,0,amplitudes[1]),
             ("differential_gain",2,1,0,amplitudes[1]),
             ("unstable_reference",2,2,1,amplitudes[1]),
             ("zero_reference",2,2,0,0)]
    rows, details, files, analytic_errors = [], [], [], []
    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    for i,(name,beta_s,beta_r,alpha_r,amp_r) in enumerate(cases):
        env_s = amplitudes[0]*np.exp((-alpha+beta_s)*t)
        env_r = amp_r*np.exp((-alpha_r+beta_r)*t)
        signals = np.column_stack((env_s*np.cos(2*np.pi*frequencies[0]*t),
                                   env_r*np.cos(2*np.pi*frequencies[1]*t)))
        assert np.max(np.abs(signals)) < 1
        pcm = np.rint(signals*32767).astype(np.int16)
        wavfile.write(HERE / (name+".wav"), fs, pcm)
        read_fs, decoded = wavfile.read(HERE / (name+".wav"))
        assert read_fs == fs and np.array_equal(pcm, decoded)
        decoded = decoded.astype(float)/32767
        slopes = [estimate_slope(decoded[:,j],fs,frequencies[j]) for j in range(2)]
        corrected = None if any(s is None for s in slopes) else slopes[1]-slopes[0]
        analytic_s = float(np.polyfit(t, np.log(env_s), 1)[0])
        analytic_r = None if amp_r == 0 else float(np.polyfit(t,np.log(env_r),1)[0])
        expected = alpha + beta_r-beta_s-alpha_r if amp_r else None
        if expected is not None:
            analytic_errors.append(abs(analytic_r-analytic_s-expected))
        detail = {"case":name,"beta_target_per_s":beta_s,"beta_reference_per_s":beta_r,
                  "true_reference_decay_per_s":alpha_r,"target_log_slope_per_s":slopes[0],
                  "reference_log_slope_per_s":slopes[1],"naive_alpha_per_s":-slopes[0],
                  "corrected_alpha_per_s":corrected,"expected_corrected_per_s":expected,
                  "true_target_alpha_per_s":alpha,"rawSHA256":sha(HERE/(name+".wav")),
                  "correction_status":"withheld_zero_reference" if corrected is None else "conditional_estimate"}
        details.append(detail)
        if corrected is not None:
            rows.append([i,beta_s,beta_r,alpha_r,slopes[0],slopes[1],corrected,expected])
            ax[0].scatter(i, -slopes[0], marker="x", color="#ad4f2a")
            ax[0].scatter(i, corrected, color="#246680")
        if i == 2:
            ax[1].plot(t,env_s,label="Target envelope")
            ax[1].plot(t,env_r,label="Reference envelope")
        files.append(name+".wav")
    matrices = {
       "singleChannel":{"parameterOrder":["alpha","beta"],"matrix":[[-1,1]],"kernelWitness":[1,1]},
       "sharedGain":{"parameterOrder":["alpha","beta"],"matrix":[[-1,1],[0,1]],"kernelWitness":None},
       "differentialGain":{"parameterOrder":["alpha","beta_target","beta_reference"],"matrix":[[-1,1,0],[0,0,1]],"kernelWitness":[1,1,0]},
       "unstableReference":{"parameterOrder":["alpha","alpha_reference","beta"],"matrix":[[-1,0,1],[0,-1,1]],"kernelWitness":[1,1,1]}}
    for item in matrices.values():
        arr=np.array(item["matrix"],float)
        item.update({"domainDimension":int(arr.shape[1]),"rank":int(np.linalg.matrix_rank(arr)),
                     "nullity":int(arr.shape[1]-np.linalg.matrix_rank(arr))})
        item["kernelResidual"] = None if item["kernelWitness"] is None else float(np.linalg.norm(arr@item["kernelWitness"]))
    metrics = {"analyticIdentityMaxError_per_s":max(analytic_errors),
               "commonGainMaxCorrectedError_per_s":max(abs(d["corrected_alpha_per_s"]-alpha) for d in details[:3]),
               "naiveAlphaBeta2_per_s":details[2]["naive_alpha_per_s"],
               "correctedAlphaBeta2_per_s":details[2]["corrected_alpha_per_s"],
               "differentialGainBias_per_s":details[3]["corrected_alpha_per_s"]-alpha,
               "unstableReferenceBias_per_s":details[4]["corrected_alpha_per_s"]-alpha,
               "zeroReferenceCorrection":details[5]["corrected_alpha_per_s"],
               "differentialAndUnstablePCMIdentical": (HERE/"differential_gain.wav").read_bytes()==(HERE/"unstable_reference.wav").read_bytes(),
               "singleChannelRank":matrices["singleChannel"]["rank"],"sharedGainRank":matrices["sharedGain"]["rank"]}
    checks = {"analyticIdentity":metrics["analyticIdentityMaxError_per_s"] <= 1e-10,
              "PCMCorrection":metrics["commonGainMaxCorrectedError_per_s"] <= .02,
              "differentialRivalRetainsBias":abs(metrics["differentialGainBias_per_s"]+1)<=.02,
              "unstableReferenceRetainsBias":abs(metrics["unstableReferenceBias_per_s"]+1)<=.02,
              "zeroReferenceWithheld":metrics["zeroReferenceCorrection"] is None,
              "rankAndKernels":matrices["singleChannel"]["rank"]==1 and matrices["sharedGain"]["rank"]==2 and all(x["kernelResidual"] in (0.,None) for x in matrices.values()),
              "rawDecodeExact":True}
    csv(HERE/"fit-results.csv",["case_index","beta_target_per_s","beta_reference_per_s","reference_decay_per_s","target_slope_per_s","reference_slope_per_s","corrected_alpha_per_s","expected_per_s"],rows)
    writejson(HERE/"case-results.json",details)
    writejson(HERE/"identifiability.json",matrices)
    ax[0].axhline(alpha, ls="--",color="black",label="True fixture decay")
    ax[0].scatter([],[],marker="x",color="#ad4f2a",label="Target alone")
    ax[0].scatter([],[],color="#246680",label="Reference corrected")
    ax[0].set(xticks=range(5),xticklabels=["β=0","β=1","β=2","Diff. gain","Ref. decay"],ylabel="Decay estimate (s⁻¹)",title="Correction works only with its assumptions")
    ax[0].legend(fontsize=8)
    ax[1].set(xlabel="Time (s)",ylabel="Synthetic envelope (FS)",title="Shared β=2 s⁻¹, separated channels")
    ax[1].legend()
    savefig(fig,HERE/"figure.svg")
    report = """# R1 — shared-gain witness

Executed synthetic analytic envelopes and generated stereo PCM16, not physical recordings. The independently stable reference is assumed; it is not inferred from the corrected fit. The two stereo channels already separate target and reference. This runner performs no mono frequency separation.

For target log-slope l_s=−alpha+beta_s and reference log-slope l_r=−alpha_r+beta_r, the estimator is alpha_hat=l_r−l_s=alpha−alpha_r+beta_r−beta_s. Shared gain and alpha_r=0 identify alpha. Target-only data have a one-dimensional kernel. Adding the stated reference makes the two-parameter map full rank, but allowing differential gain or reference decay restores a kernel, explicitly recorded in identifiability.json.

The full signed carrier samples are fitted by variable projection over sin/cos amplitudes at the declared frequencies. A bounded scalar optimizer estimates each log slope. This gives a method independent of the skeptic's carrier-maxima fit. Raw WAVs are written then decoded; all hashes are recorded. Zero reference withholds correction. Differential gain and a decaying reference produce exactly identical PCM files here and both retain the expected −1 s⁻¹ bias. A low residual does not validate the shared-gain premise.

Run: `python research/sound-lab-v4/R1/run.py`. Fixture WAVs are analysis artifacts, not playback presets. The result is conditional parameter recovery; intrinsic material damping remains unmeasured.
"""
    finish(HERE,metrics,"A stable shared-gain witness recovers the stipulated decay; differential gain and reference drift retain a one-per-second bias.",details[3:],report,files+["fit-results.csv","case-results.json","identifiability.json","figure.svg"],checks)


if __name__ == "__main__":
    main()
