"""Deterministic conditional log-envelope error boxes, not confidence intervals."""
from pathlib import Path
import json
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import csv, finish, plt, savefig, writejson
import numpy as np

HERE = Path(__file__).resolve().parent


def slope_interval(time_s, target_FS, reference_FS, amplitude_error_FS,
                   reference_decay_bound_per_s=None, differential_gain_bound_per_s=None):
    """Enclose the OLS log-slope contrast over a rectangular amplitude error box.

    Bounds on two physical nuisances are premises supplied by the caller. None
    withholds the physical interval. A sample reaching zero withholds the entire
    frozen-window contrast. This is an exact box bound, not a probabilistic CI.
    """
    t, target, reference = (np.asarray(x, dtype=float) for x in (time_s,target_FS,reference_FS))
    if t.ndim != 1 or len(t) < 2 or target.shape != t.shape or reference.shape != t.shape:
        raise ValueError("matching one-dimensional time and channel arrays required")
    if not all(np.all(np.isfinite(x)) for x in (t,target,reference)):
        raise ValueError("finite time and samples required")
    if not np.all(np.diff(t) > 0):
        raise ValueError("strictly increasing physical times required")
    error = np.asarray(amplitude_error_FS,dtype=float)
    if error.ndim == 0:
        error = np.full(t.shape, float(error))
    if error.shape != t.shape or not np.all(np.isfinite(error)) or np.any(error < 0):
        raise ValueError("finite nonnegative scalar or matching error bound required")
    for bound in (reference_decay_bound_per_s,differential_gain_bound_per_s):
        if bound is not None and (not np.isscalar(bound) or not np.isfinite(bound) or bound < 0):
            raise ValueError("physical nuisance bounds must be nonnegative finite scalars or None")
    if np.any(target-error <= 0) or np.any(reference-error <= 0):
        return {"status":"withheld_at_error_floor", "contrast_interval_per_s":None,
                "physical_alpha_interval_per_s":None,"weights_per_s":None}
    centered = t - np.mean(t)
    denominator = float(centered @ centered)
    if not np.isfinite(denominator) or denominator <= 0:
        raise ValueError("finite nonzero time spread required")
    w = centered / denominator
    logs_s = np.column_stack((np.log(target-error),np.log(target+error)))
    logs_r = np.column_stack((np.log(reference-error),np.log(reference+error)))
    low = float(np.sum(np.where(w>=0,w*(logs_r[:,0]-logs_s[:,1]),w*(logs_r[:,1]-logs_s[:,0]))))
    high = float(np.sum(np.where(w>=0,w*(logs_r[:,1]-logs_s[:,0]),w*(logs_r[:,0]-logs_s[:,1]))))
    missing = reference_decay_bound_per_s is None or differential_gain_bound_per_s is None
    width = None if missing else reference_decay_bound_per_s+differential_gain_bound_per_s
    return {"status":"contrast_only_unknown_systematic_bound" if missing else "conditional_physical_interval",
            "contrast_interval_per_s":[low,high],
            "physical_alpha_interval_per_s":None if missing else [low-width,high+width],
            "weights_per_s":w.tolist()}


def main():
    contract = json.loads((HERE/"contract.json").read_text())
    model = contract["model"]
    t = np.linspace(model["time_s"]["start"],model["time_s"]["stop"],model["time_s"]["count"])
    target = model["targetAmplitude_FS"]*np.exp((-model["targetAlpha_per_s"]+model["betaTarget_per_s"])*t)
    reference = model["referenceAmplitude_FS"]*np.exp((model["betaReference_per_s"]-model["referenceAlpha_per_s"])*t)
    delta = model["amplitudeErrorBound_FS"]
    bounds = contract["systematicPremises"]
    refbound = bounds["absoluteReferenceDecayBound_per_s"]
    diffbound = bounds["absoluteDifferentialGainBound_per_s"]
    base = slope_interval(t,target,reference,delta,refbound,diffbound)
    point = slope_interval(t,target,reference,0,refbound,diffbound)
    w = np.array(base["weights_per_s"])
    # The extrema are possible latent positive envelopes, not simulated new data.
    min_s = np.where(w>=0,target+delta,target-delta)
    min_r = np.where(w>=0,reference-delta,reference+delta)
    max_s = np.where(w>=0,target-delta,target+delta)
    max_r = np.where(w>=0,reference+delta,reference-delta)
    endpoints = [float(w@(np.log(min_r)-np.log(min_s))),float(w@(np.log(max_r)-np.log(max_s)))]
    endpoint_error = float(np.max(np.abs(np.array(endpoints)-base["contrast_interval_per_s"])))
    rng = np.random.default_rng(2026092702)
    trials, observations = [], []
    for i in range(128):
        ys = target+rng.uniform(-delta,delta,len(t))
        yr = reference+rng.uniform(-delta,delta,len(t))
        result = slope_interval(t,ys,yr,delta,refbound,diffbound)
        lo,hi = result["contrast_interval_per_s"]
        trials.append([i,lo,hi,float(lo<=4<=hi)])
        observations.extend([[i,j,t[j],ys[j],yr[j],delta] for j in range(len(t))])
    target_floor = target.copy(); target_floor[5]=delta
    floor = slope_interval(t,target_floor,reference,delta,refbound,diffbound)
    zero = slope_interval(t,target,np.zeros_like(reference),delta,refbound,diffbound)
    unknown = [slope_interval(t,target,reference,delta,None,diffbound),
               slope_interval(t,target,reference,delta,refbound,None)]
    out_reference = model["referenceAmplitude_FS"]*np.exp((model["betaReference_per_s"]+.8)*t)
    outside = slope_interval(t,target,out_reference,delta,refbound,diffbound)
    # Simultaneous extrema of the declared physical nuisance budgets remain covered.
    nuisance_corners=[]
    for alpha_ref in [-refbound,refbound]:
        for differential in [-diffbound,diffbound]:
            yr = model["referenceAmplitude_FS"]*np.exp((model["betaReference_per_s"]+differential-alpha_ref)*t)
            ir = slope_interval(t,target,yr,delta,refbound,diffbound)
            lo,hi=ir["physical_alpha_interval_per_s"]
            nuisance_corners.append({"reference_decay_per_s":alpha_ref,"differential_gain_per_s":differential,
                                     "interval_per_s":[lo,hi],"covers_true_alpha":bool(lo<=4<=hi)})
    contrasts = base["contrast_interval_per_s"]
    physical = base["physical_alpha_interval_per_s"]
    metrics = {"baseContrastInterval_per_s":contrasts,"basePhysicalInterval_per_s":physical,
               "systematicWidthIncrease_per_s":(physical[1]-physical[0])-(contrasts[1]-contrasts[0]),
               "noErrorPointMaxError_per_s":float(np.max(np.abs(np.array(point["contrast_interval_per_s"])-4))),
               "endpointAttainmentMaxError_per_s":endpoint_error,"withinBoundCoverageCount":int(sum(r[3] for r in trials)),
               "withinBoundTrials":len(trials),"outOfBudgetPhysicalInterval_per_s":outside["physical_alpha_interval_per_s"],
               "outOfBudgetMissesTrueAlpha":not(outside["physical_alpha_interval_per_s"][0]<=4<=outside["physical_alpha_interval_per_s"][1]),
               "floorWithheld":floor["contrast_interval_per_s"] is None,
               "zeroReferenceWithheld":zero["contrast_interval_per_s"] is None,
               "missingSystematicWithheld":all(r["physical_alpha_interval_per_s"] is None for r in unknown)}
    checks={"noErrorIdentity":metrics["noErrorPointMaxError_per_s"]<=1e-12,
            "endpointsAttained":endpoint_error<=1e-10,"allInBoundCovered":metrics["withinBoundCoverageCount"]==128,
            "systematicWidth":abs(metrics["systematicWidthIncrease_per_s"]-1.3)<=1e-10,
            "floorWholeWindowWithheld":metrics["floorWithheld"],"zeroReferenceWithheld":metrics["zeroReferenceWithheld"],
            "unknownSystematicWithheld":metrics["missingSystematicWithheld"],
            "outOfBudgetFailureRetained":metrics["outOfBudgetMissesTrueAlpha"],
            "nuisanceCornersCovered":all(r["covers_true_alpha"] for r in nuisance_corners)}
    csv(HERE/"base-envelopes.csv",["time_s","target_FS","reference_FS","absolute_error_FS","weight_per_s","min_target_FS","min_reference_FS","max_target_FS","max_reference_FS"],np.column_stack((t,target,reference,np.full_like(t,delta),w,min_s,min_r,max_s,max_r)))
    csv(HERE/"in-bound-trials.csv",["trial","low_per_s","high_per_s","covers_true_alpha"],trials)
    csv(HERE/"observation-realizations.csv",["trial","sample","time_s","target_FS","reference_FS","absolute_error_FS"],observations)
    writejson(HERE/"controls.json",{"base":base,"point":point,"floor":floor,"zero":zero,"missing_bounds":unknown,"outside_budget":outside,"nuisance_corners":nuisance_corners,"seed":2026092702})
    fig,ax=plt.subplots(figsize=(9,4))
    bars=[contrasts,physical,outside["physical_alpha_interval_per_s"]]
    for i,(lo,hi) in enumerate(bars):
        ax.plot([lo,hi],[i,i],lw=8,solid_capstyle="butt",color=["#277c85","#436793","#b35231"][i])
    ax.axvline(4,color="black",ls="--",label="True synthetic α = 4 s⁻¹")
    ax.set(yticks=[0,1,2],yticklabels=["Supplied envelope error only","Plus declared nuisance bounds","β difference 0.8 outside budget"],xlabel="Conditional decay / slope contrast (s⁻¹)",title="Missing a nuisance bound defeats a narrow error bar")
    ax.legend(loc="upper left");savefig(fig,HERE/"figure.svg")
    report="""# R2 — conditional uncertainty budget

These observations are positive synthetic envelopes with a **supplied** absolute amplitude-error guarantee. No algorithm has established this guarantee from a microphone recording. The deterministic interval is not a confidence interval.

With w_i=(t_i−mean(t))/sum_j(t_j−mean(t))², q=sum_i w_i(log r_i−log s_i). Each latent amplitude lies in [a_i−delta_i,a_i+delta_i]. Log is monotone. For positive w choose the lower reference/upper target logs at the minimum; reverse at the maximum. For negative w reverse the choices. Summing these independent extrema gives exact endpoints of the rectangular log box. Frozen time/window and no sample deletion are premises. A single lower endpoint at or below zero withholds the entire contrast.

The physical relation is alpha=q+alpha_reference−(beta_reference−beta_target). Supplied absolute bounds .25 s⁻¹ and .4 s⁻¹ therefore widen q by .65 s⁻¹ on each side. If either bound is missing, no physical-alpha interval is returned. The width rises by 1.3 s⁻¹, irrespective of how precise the supplied envelope errors are.

All 128 seeded in-bound synthetic observations cover their true contrast. Direct extremal-envelope constructions attain both box endpoints. Simultaneous corners of the physical nuisance budgets are also covered. An intentionally out-of-budget differential gain of .8 s⁻¹ produces an interval excluding the true alpha, retained as a failure of the premise, not repaired by widening after observation.

Run: `python research/sound-lab-v4/R2/run.py`. Reusable function `slope_interval` validates shapes, finite increasing times, nonnegative finite error budgets and physical nuisance bounds. It rejects invalid inputs and explicitly withholds floor/missing-bound results. Further assumptions of a single exponential, known timebase and faithful separated envelopes remain conditional.
"""
    finish(HERE,metrics,"Precise envelopes give a narrow contrast box, but stated reference and gain uncertainty add 1.3 s⁻¹ to its width; missing bounds withhold a physical interval.",[{"control":"out-of-budget differential gain","outcome":"true alpha excluded as expected"},{"control":"one sample at error floor","outcome":"whole-window interval withheld"}],report,["base-envelopes.csv","in-bound-trials.csv","observation-realizations.csv","controls.json","figure.svg"],checks)


if __name__=="__main__":main()
