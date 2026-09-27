"""Prospective paired-support gravity-like parameter design and exact rival."""
from pathlib import Path
import json
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from common import csv, finish, plt, savefig, writejson
import numpy as np

HERE=Path(__file__).resolve().parent


def fit_paired(masses_kg,test_contrasts_N,stator_contrasts_N,stator_mass_kg=.1,
               per_contrast_error_N=2e-6,mass_bias_bound_m_per_s2=None,g_m_per_s2=9.80665):
    masses=np.asarray(masses_kg,float);test=np.asarray(test_contrasts_N,float);stator=np.asarray(stator_contrasts_N,float)
    if masses.ndim!=1 or masses.size<1 or test.shape!=(masses.size,2) or stator.shape!=test.shape:
        raise ValueError("one-dimensional masses and N by 2 paired polarity arrays required")
    if not all(np.all(np.isfinite(x)) for x in [masses,test,stator]) or np.any(masses<=0):
        raise ValueError("finite observations and strictly positive masses required")
    for value in [stator_mass_kg,g_m_per_s2]:
        if not np.isscalar(value) or not np.isfinite(value) or value<=0:raise ValueError("positive finite stator mass and gravity required")
    if not np.isscalar(per_contrast_error_N) or not np.isfinite(per_contrast_error_N) or per_contrast_error_N<0:
        raise ValueError("finite nonnegative support-contrast error bound required")
    if mass_bias_bound_m_per_s2 is not None and (not np.isscalar(mass_bias_bound_m_per_s2) or not np.isfinite(mass_bias_bound_m_per_s2) or mass_bias_bound_m_per_s2<0):
        raise ValueError("finite nonnegative mass-bias bound or None required")
    x=masses+stator_mass_kg;design=np.column_stack((x,np.ones_like(x)))
    rank=int(np.linalg.matrix_rank(design))
    paired=np.mean(test+stator,axis=1)
    result={"domainDimension":2,"rank":rank,"nullity":2-rank,"totalMasses_kg":x.tolist(),
            "pairedPolarityObservable_N":paired.tolist(),"slope_m_per_s2":None,"intercept_N":None,
            "conditionalSlopeInterval_m_per_s2":None,"physicalGravityInterval_m_per_s2":None,
            "status":"withheld_rank" if rank<2 else "pending_contact"}
    if np.any(masses[:,None]*g_m_per_s2+test-per_contrast_error_N<0) or np.any(stator_mass_kg*g_m_per_s2+stator-per_contrast_error_N<0):
        result["status"]="withheld_contact_loss_or_uncertainty";return result
    if rank<2:return result
    centered=x-np.mean(x);weights=centered/(centered@centered)
    slope=float(weights@paired);intercept=float(np.mean(paired)-slope*np.mean(x))
    paired_error=2*per_contrast_error_N
    halfwidth=float(paired_error*np.sum(np.abs(weights)))
    interval=[slope-halfwidth,slope+halfwidth]
    physical=None if mass_bias_bound_m_per_s2 is None else [interval[0]-mass_bias_bound_m_per_s2,interval[1]+mass_bias_bound_m_per_s2]
    result.update({"slope_m_per_s2":slope,"intercept_N":intercept,
                   "slopeWeights_per_kg":weights.tolist(),"pairedWorstCaseError_N":paired_error,
                   "slopeWorstCaseError_m_per_s2":halfwidth,
                   "conditionalSlopeInterval_m_per_s2":interval,"physicalGravityInterval_m_per_s2":physical,
                   "status":"conditional_slope_only_unknown_mass_bias" if physical is None else "conditional_physical_interval_under_supplied_mass_bias_bound"})
    return result


def synthetic_supports(masses,delta_g=0.,mass_bias=0.):
    masses=np.asarray(masses,float);p=np.array([-1.,1.])
    test=masses[:,None]*delta_g-.002+p[None,:]*.0003+.0002+masses[:,None]*mass_bias
    stator=np.full((len(masses),2),.1*delta_g+.002+.0003+.1*mass_bias)
    return test,stator


def main():
    contract=json.loads((HERE/"contract.json").read_text());m=contract["model"]
    masses=np.array(m["testMasses_kg"]);M=m["statorMass_kg"];dg=m["injected_delta_g_m_per_s2"]
    epsilon=contract["boundedError"]["perBaselineSubtractedSupportContrast_N"]
    null_test,null_stator=synthetic_supports(masses)
    test,stator=synthetic_supports(masses,delta_g=dg)
    rival_test,rival_stator=synthetic_supports(masses,mass_bias=dg)
    null=fit_paired(masses,null_test,null_stator)
    injected=fit_paired(masses,test,stator)
    rival=fit_paired(masses,rival_test,rival_stator)
    known_zero_bias=fit_paired(masses,test,stator,mass_bias_bound_m_per_s2=0)
    x=masses+M;w=np.array(injected["slopeWeights_per_kg"])
    single_masses=np.full(4,masses[0]);single_t,single_s=synthetic_supports(single_masses,delta_g=dg)
    single=fit_paired(single_masses,single_t,single_s)
    matrix=np.column_stack((x,np.ones(4)));expanded=np.column_stack((x,np.ones(4),x))
    single_matrix=np.column_stack((single_masses+M,np.ones(4)))
    structures={"singleMass":{"parameterOrder":["delta_g","constant_bias"],"matrix":single_matrix.tolist(),"domainDimension":2,"rank":int(np.linalg.matrix_rank(single_matrix)),"nullity":1,"kernelWitness":[1.,-float(x[0])]},
                "fourMasses":{"parameterOrder":["delta_g","constant_bias"],"matrix":matrix.tolist(),"domainDimension":2,"rank":int(np.linalg.matrix_rank(matrix)),"nullity":0,"kernelWitness":None},
                "massBiasRival":{"parameterOrder":["delta_g","constant_bias","mass_proportional_bias"],"matrix":expanded.tolist(),"domainDimension":3,"rank":int(np.linalg.matrix_rank(expanded)),"nullity":1,"kernelWitness":[1.,0.,-1.]}}
    for record in structures.values():
        record["kernelResidual"]=None if record["kernelWitness"] is None else float(np.linalg.norm(np.array(record["matrix"])@record["kernelWitness"]))
    rng=np.random.default_rng(2026092705)
    trials=[];error_rows=[]
    for j in range(128):
        err_t=rng.uniform(-epsilon,epsilon,test.shape);err_s=rng.uniform(-epsilon,epsilon,stator.shape)
        observed=fit_paired(masses,test+err_t,stator+err_s)
        lo,hi=observed["conditionalSlopeInterval_m_per_s2"]
        trials.append([j,observed["slope_m_per_s2"],lo,hi,int(lo<=dg<=hi)])
        for i in range(4):
            for p in range(2):error_rows.append([j,i,[-1,1][p],err_t[i,p],err_s[i,p]])
    extremes=[]
    for sign in [-1,1]:
        errors=sign*np.sign(w)[:,None]*epsilon*np.ones((4,2))
        r=fit_paired(masses,test+errors,stator+errors)
        extremes.append({"sign":sign,"slopeError_m_per_s2":r["slope_m_per_s2"]-dg,
                         "eachSupportError_N":errors.tolist(),"result":r})
    contact_test=test.copy();contact_test[0,0]=-masses[0]*m["baseline_g_m_per_s2"]-.001
    contact=fit_paired(masses,contact_test,stator)
    malformed=[]
    def invalid(name,func):
        try:func()
        except ValueError:malformed.append({"case":name,"rejected":True})
        else:malformed.append({"case":name,"rejected":False})
    invalid("negative_mass",lambda:fit_paired([-1,.015,.025,.035],test,stator))
    invalid("zero_mass",lambda:fit_paired([0,.015,.025,.035],test,stator))
    invalid("nonfinite_mass",lambda:fit_paired([np.nan,.015,.025,.035],test,stator))
    invalid("negative_error",lambda:fit_paired(masses,test,stator,per_contrast_error_N=-epsilon))
    invalid("infinite_error",lambda:fit_paired(masses,test,stator,per_contrast_error_N=np.inf))
    invalid("nonfinite_contrast",lambda:fit_paired(masses,test*np.nan,stator))
    invalid("wrong_shape",lambda:fit_paired(masses,test[:,0],stator))
    invalid("negative_bias_bound",lambda:fit_paired(masses,test,stator,mass_bias_bound_m_per_s2=-1))
    max_rival_difference=float(max(np.max(np.abs(test-rival_test)),np.max(np.abs(stator-rival_stator))))
    metrics={"nullRecoveredSlope_m_per_s2":null["slope_m_per_s2"],"injectedRecoveredSlope_m_per_s2":injected["slope_m_per_s2"],
             "injectedRecoveredIntercept_N":injected["intercept_N"],"conditionalSlopeInterval_m_per_s2":injected["conditionalSlopeInterval_m_per_s2"],
             "worstCaseSlopeHalfwidth_m_per_s2":injected["slopeWorstCaseError_m_per_s2"],
             "extremalSlopeErrors_m_per_s2":[r["slopeError_m_per_s2"] for r in extremes],
             "boundedRealizationsCovered":int(sum(row[-1] for row in trials)),"boundedRealizationsTotal":128,
             "sameIndividualObservationRivalMaxDifference_N":max_rival_difference,
             "singleMassRank":single["rank"],"fourMassRank":structures["fourMasses"]["rank"],
             "expandedRank":structures["massBiasRival"]["rank"],"expandedNullity":structures["massBiasRival"]["nullity"],
             "expandedKernelResidual":structures["massBiasRival"]["kernelResidual"],
             "unknownMassBiasPhysicalGravityInterval":injected["physicalGravityInterval_m_per_s2"],
             "polarityAveragedSinglePanNullContrast_N":float(np.mean(null_test[0])),
             "contactLossStatus":contact["status"],"malformedCasesRejected":sum(r["rejected"] for r in malformed)}
    checks={"noiselessInjectionRecovered":abs(injected["slope_m_per_s2"]-dg)<=1e-10,
            "nullRecovered":abs(null["slope_m_per_s2"])<=1e-10,
            "sameReadoutRival":max_rival_difference<=1e-14,
            "kernelResiduals":all(r["kernelResidual"] is None or r["kernelResidual"]<=1e-12 for r in structures.values()),
            "extremeErrorsAttainBound":max(abs(extremes[0]["slopeError_m_per_s2"]+.00032),abs(extremes[1]["slopeError_m_per_s2"]-.00032))<=1e-12,
            "all128Covered":metrics["boundedRealizationsCovered"]==128,
            "unknownMassBiasWithholds":injected["physicalGravityInterval_m_per_s2"] is None,
            "singleMassWithholds":single["rank"]==1 and single["slope_m_per_s2"] is None,
            "injectionConditionalIntervalExcludesZero":injected["conditionalSlopeInterval_m_per_s2"][1]<0,
            "contactLossWithheld":contact["slope_m_per_s2"] is None,
            "malformedInputsRejected":all(r["rejected"] for r in malformed)}
    files=[]
    for name,tt,ss in [("ordinary-null",null_test,null_stator),("injected-model",test,stator),("mass-bias-rival",rival_test,rival_stator)]:
        rows=[[masses[i],M,p,tt[i,j],ss[i,j],masses[i]*m["baseline_g_m_per_s2"]+tt[i,j],M*m["baseline_g_m_per_s2"]+ss[i,j]] for i in range(4) for j,p in enumerate([-1,1])]
        csv(HERE/(name+".csv"),["test_mass_kg","stator_mass_kg","polarity","test_contrast_N","stator_contrast_N","test_normal_force_N","stator_normal_force_N"],rows);files.append(name+".csv")
    csv(HERE/"bounded-realizations.csv",["trial","slope_m_per_s2","low_m_per_s2","high_m_per_s2","covers_injected_truth"],trials)
    csv(HERE/"individual-errors.csv",["trial","mass_index","polarity","test_error_N","stator_error_N"],error_rows)
    writejson(HERE/"identifiability.json",structures)
    writejson(HERE/"case-results.json",{"null":null,"injected":injected,"rival":rival,"assumed_zero_mass_bias":known_zero_bias,"single_mass":single,"extremes":extremes,"contact_loss":contact,"malformed":malformed,"seed":2026092705})
    fig,axes=plt.subplots(1,2,figsize=(11,4))
    axes[0].plot(x*1000,np.array(null["pairedPolarityObservable_N"])*1000,"o-",label="Ordinary-force null")
    axes[0].plot(x*1000,np.array(injected["pairedPolarityObservable_N"])*1000,"s-",label="Injected common acceleration")
    axes[0].plot(x*1000,np.array(rival["pairedPolarityObservable_N"])*1000,"x",ms=10,label="Exact ordinary mass-bias rival")
    axes[0].set(xlabel="Combined calibrated mass (g)",ylabel="Paired, polarity-averaged contrast (mN)",title="The injected signal has an exact rival");axes[0].legend(fontsize=8)
    trial_array=np.array(trials)
    axes[1].plot(trial_array[:,0],1e3*(trial_array[:,1]-dg),".",label="128 supplied-error fixtures")
    axes[1].axhline(.32,ls="--",color="#b35231");axes[1].axhline(-.32,ls="--",color="#b35231",label="Deterministic extrema ±0.32")
    axes[1].set(xlabel="Synthetic realization",ylabel="Recovered slope error (10⁻³ m/s²)",title="No √n discount for adversarial bounded error");axes[1].legend(fontsize=8)
    savefig(fig,HERE/"figure.svg")
    report="""# R5 — a gravity-like slope and its exact ordinary rival

All force records are synthetic. The injected delta_g=−.02 m/s² is a deliberately stipulated common acceleration change acting on both the test and stator masses. It is a positive control for an estimator, not an observed anomaly, gravity modification, or new physical theory.

For polarity p=±1, D_test=m delta_g−F_internal+p F_odd+B_test and D_stator=M delta_g+F_internal+B_stator. Adding contemporaneous support contrasts includes both internal reactions. Averaging polarities removes the stipulated odd force. Thus S(m)=(m+M)delta_g+B, if B is constant across masses and polarities. Four distinct total masses identify slope and intercept in this two-parameter model. Repeating one mass leaves rank one and kernel (1,−total_mass). The test pan alone retains the even internal magnetic force after polarity averaging.

Each already-baseline-subtracted support contrast has a supplied ±2 µN total error bound. Adding two supports and averaging two polarities gives a worst-case paired error of ±4 µN; no independence or sqrt(n) reduction is assumed. OLS slope weights are (−30,−10,10,30) kg⁻¹. Therefore |slope_error|≤4 µN sum|w_i|=.00032 m/s². The exact sign-aligned errors on both supports and both polarities attain either endpoint. All 128 seeded bounded-error realizations are covered. These numbers are not measured sensitivity or calibrated scale performance.

The decisive retained rival adds ordinary mass-proportional support biases c*m and c*M with true delta_g=0 and c=−.02 m/s². It reproduces every individual polarity/support observation of the injected case, not just its fitted slope. The expanded model S=(m+M)(delta_g+c)+B has parameter order (delta_g,B,c), rank two in dimension three, and kernel (1,0,−1). Mass variation and paired supports remove specified rivals but cannot separate these two contributions. Unknown c withholds any physical gravity interval. Supplying a bound on c yields only a further conditional interval, not independent evidence that the bound holds.

The reusable fit validates shapes, finite positive masses, nonnegative finite error budgets and contact. If the lower bound on any support force is negative, static inference is withheld. It does not authenticate recordings, calibrate masses, establish shared biases, or validate the ordinary-force inventory. A future discriminator would need independently characterized channels with predictions differing for the competing mechanisms; repeating the same ambiguous observation is insufficient.

Run: `python research/sound-lab-v4/R5/run.py`. This final authorized round is a prospective identifying design and a nonidentifiability proof within explicit models. No measured antigravity effect or detector sensitivity has been established.
"""
    finish(HERE,metrics,"Paired supports and four masses recover a deliberately injected acceleration-like slope, but an exact mass-proportional ordinary bias reproduces every observation; unknown bias prevents a gravity conclusion.",[{"control":"mass-proportional ordinary bias","outcome":"exact same individual force observations"},{"control":"single mass","outcome":"rank one: slope withheld"},{"control":"current polarity alone","outcome":"even magnetic support remains"},{"control":"loss of static contact","outcome":"static slope withheld"}],report,files+["bounded-realizations.csv","individual-errors.csv","identifiability.json","case-results.json","figure.svg"],checks,extra={"evidenceType":"synthetic_force_observations_with_injected_model_deformation","domain":"gravity_claim_identifiability"})


if __name__=="__main__":main()
