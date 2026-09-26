#!/usr/bin/env python3
"""Final round: exact synthetic target-test calibration; no human observations."""
from fractions import Fraction as F
from pathlib import Path
import csv,gzip,hashlib,io,itertools,json,math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent

def pmf(n,p):return [F(math.comb(n,k))*p**k*(1-p)**(n-k) for k in range(n+1)]
def tails(masses):
    out=[F(0)]*(len(masses)+1)
    for k in range(len(masses)-1,-1,-1):out[k]=out[k+1]+masses[k]
    return out
def crossing_dp(nmax,p,boundaries):
    alive={0:F(1)};absorbed=F(0);records=[]
    for n in range(1,nmax+1):
        next_alive={};new_cross=F(0)
        for k,mass in alive.items():
            for hit,prob in ((0,1-p),(1,p)):
                nextk=k+hit;weight=mass*prob
                if nextk>=boundaries[n]:new_cross+=weight
                else:next_alive[nextk]=next_alive.get(nextk,F(0))+weight
        alive=next_alive;absorbed+=new_cross
        records.append((n,boundaries[n],absorbed,new_cross,sum(alive.values(),F(0))))
        assert absorbed+sum(alive.values(),F(0))==1
    return records

def run():
    nmax=40;p=F(1,4);alpha=F(1,20);seed=2026092606;studies=50000
    probabilities={n:pmf(n,p) for n in range(nmax+1)}
    all_tails={n:tails(masses) for n,masses in probabilities.items()}
    boundaries={n:next(k for k,value in enumerate(all_tails[n]) if value<=alpha) for n in range(1,nmax+1)}
    cutoff=boundaries[nmax];fixed=all_tails[nmax][cutoff];checks=[]
    valid=all(sum(masses,F(0))==1 and min(masses)>=0 and all(a>=b for a,b in zip(all_tails[n],all_tails[n][1:])) for n,masses in probabilities.items())
    checks.append(dict(name="exact_probability_and_cutoff",passed=valid and fixed<=alpha and all_tails[nmax][cutoff-1]>alpha))
    records=crossing_dp(nmax,p,boundaries);optional=records[-1][2]
    # Independently propagate the unrestricted Bernoulli distribution.
    unrestricted=[F(1)];unrestricted_agreement=True
    for n in range(1,nmax+1):
        next_dist=[F(0)]*(n+1)
        for k,value in enumerate(unrestricted):next_dist[k]+=value*(1-p);next_dist[k+1]+=value*p
        unrestricted=next_dist;unrestricted_agreement &= unrestricted==probabilities[n]
    checks.append(dict(name="exact_DP_mass_and_binomial_reconstruction",passed=unrestricted_agreement and all(row[2]+row[4]==1 for row in records)))
    exhaustive=F(0)
    for sequence in itertools.product((0,1),repeat=12):
        k=0;cross=False
        for n,hit in enumerate(sequence,1):
            k+=hit;cross |= k>=boundaries[n]
        if cross:exhaustive+=p**k*(1-p)**(12-k)
    checks.append(dict(name="independent_12_trial_exhaustive_control",passed=exhaustive==records[11][2]))
    checks.append(dict(name="optional_stopping_inflation",passed=optional>fixed))
    leakage=[]
    for lam in (F(0),F(1,10),F(1,2)):
        hit=lam+(1-lam)/4;detection=tails(pmf(nmax,hit))[cutoff]
        leakage.append(dict(lambda_exact=str(lam),hit_probability_exact=str(hit),hit_probability=float(hit),
                            fixed_cutoff_detection_exact=str(detection),fixed_cutoff_detection=float(detection)))
    checks.append(dict(name="disclosed_leakage_monotonicity",passed=all(a["fixed_cutoff_detection"]<b["fixed_cutoff_detection"] for a,b in zip(leakage,leakage[1:])) and leakage[0]["fixed_cutoff_detection"]==float(fixed)))
    rng=np.random.default_rng(seed);targets=rng.integers(0,4,size=(studies,nmax),dtype=np.uint8)
    cumulative=np.cumsum(targets==0,axis=1);hits=cumulative[:,-1]
    crossings=cumulative>=np.array([boundaries[n] for n in range(1,nmax+1)])
    ever=np.any(crossings,axis=1);first=np.where(ever,np.argmax(crossings,axis=1)+1,0)
    simulations=[]
    for name,events,exact in (("fixed_40",hits>=cutoff,fixed),("naive_optional_stopping",ever,optional)):
        rate=float(np.mean(events));theory=float(exact);tol=6*math.sqrt(theory*(1-theory)/studies)+1/studies
        simulations.append(dict(rule=name,studies=studies,discoveries=int(np.sum(events)),simulated_rate=rate,exact_rate=theory,tolerance=tol))
        checks.append(dict(name=f"synthetic_rate_{name}",passed=abs(rate-theory)<=tol))
    with (ROOT/"binomial_null.csv").open("w",newline="") as stream:
        writer=csv.writer(stream);writer.writerow(["hits","pmf_exact","tail_exact","pmf_float","tail_float"])
        for k,mass in enumerate(probabilities[nmax]):writer.writerow([k,str(mass),str(all_tails[nmax][k]),float(mass),float(all_tails[nmax][k])])
    with (ROOT/"stopping_boundaries.csv").open("w",newline="") as stream:
        writer=csv.writer(stream);writer.writerow(["prefix_n","critical_hits","cumulative_crossing_exact","first_crossing_exact","remaining_mass_exact","cumulative_crossing_float"])
        for n,k,total,new,remaining in records:writer.writerow([n,k,str(total),str(new),str(remaining),float(total)])
    content=io.StringIO();np.savetxt(content,np.column_stack((hits,first)),delimiter=",",header="total_hits_40,first_nominal_crossing_0_if_none",comments="",fmt="%d")
    raw=content.getvalue().encode();buffer=io.BytesIO()
    with gzip.GzipFile(filename="",fileobj=buffer,mode="wb",mtime=0) as archive:archive.write(raw)
    packed=buffer.getvalue();assert gzip.decompress(packed)==raw
    (ROOT/"synthetic_studies.csv.gz").write_bytes(packed)
    fig,axes=plt.subplots(1,2,figsize=(10,4.8),layout="constrained")
    k=np.arange(nmax+1);mass=np.array(probabilities[nmax],dtype=float)
    axes[0].bar(k,mass,color=np.where(k>=cutoff,"#bc4b37","#3659b8"),width=.85)
    axes[0].axvline(cutoff-.5,color="#bc4b37",ls="--")
    axes[0].set(title="Fixed 40-trial null distribution",xlabel="Exact target matches out of 40",ylabel="Probability mass",xlim=(-.5,40.5))
    axes[0].text(.53,.86,f"Critical count: {cutoff}\nExact null tail: {float(fixed):.3%}",transform=axes[0].transAxes,fontsize=10)
    axes[1].plot([r[0] for r in records],[float(r[2]) for r in records],label="Any nominal crossing by this prefix",color="#bc4b37")
    axes[1].axhline(float(alpha),label="Nominal 5% reference",color="#666666",ls=":")
    axes[1].scatter([40],[float(fixed)],label="Predeclared fixed-40 test",color="#16766c",s=45,zorder=4)
    axes[1].set(title="Repeated looks require their own calibration",xlabel="Maximum number of trials inspected",ylabel="Null probability of a reported positive")
    axes[1].legend(fontsize=8,loc="upper left")
    for ax in axes:ax.grid(axis="y",alpha=.2)
    for ext in ("svg","png"):fig.savefig(ROOT/f"target_null_calibration.{ext}",dpi=170,bbox_inches="tight",metadata={"Date":None} if ext=="svg" else {})
    plt.close(fig)
    output=dict(round=6,status="passed" if all(c["passed"] for c in checks) else "failed",final_round=True,
                scope="Synthetic methodology benchmark only. No dream, lucid-dream or astral-travel observations.",
                n=nmax,targets=4,chance_probability_exact=str(p),alpha_exact=str(alpha),critical_hits=cutoff,
                fixed_false_positive_exact=str(fixed),fixed_false_positive_rate=float(fixed),
                preceding_count_tail_exact=str(all_tails[nmax][cutoff-1]),preceding_count_tail=float(all_tails[nmax][cutoff-1]),
                optional_stopping_false_positive_exact=str(optional),optional_stopping_false_positive_rate=float(optional),
                exhaustive_12_trial_crossing_exact=str(exhaustive),leakage_controls=leakage,seed=seed,simulations=simulations,checks=checks,
                synthetic_archive=dict(path="synthetic_studies.csv.gz",raw_sha256=hashlib.sha256(raw).hexdigest(),gzip_sha256=hashlib.sha256(packed).hexdigest()),
                runtime={"numpy":np.__version__},contract_sha256=hashlib.sha256((ROOT/"contract.md").read_bytes()).hexdigest(),solver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (ROOT/"results.json").write_text(json.dumps(output,indent=2)+"\n");print(json.dumps(output,indent=2))
    if output["status"]!="passed":raise SystemExit(1)
if __name__=="__main__":run()
