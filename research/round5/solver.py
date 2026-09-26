#!/usr/bin/env python3
"""Exact familywise null probabilities with a seeded synthetic illustration."""
from fractions import Fraction as F
from pathlib import Path
import csv,gzip,hashlib,io,json,math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent

def run():
    alpha=F(1,20);n=50000;seed=20260926;families=(1,5,20,100)
    rng=np.random.default_rng(seed);uniforms=rng.random((n,100));duplicates=rng.random(n)
    checks=[];rows=[];minima=[]
    for m in families:
        mins=np.min(uniforms[:,:m],axis=1);minima.append(mins)
        independent=1-(1-alpha)**m;corrected=1-(1-alpha/m)**m
        checks.append(dict(name=f"exact_probability_bounds_m_{m}",passed=corrected<=alpha and (m==1 or independent>alpha)))
        for dependence,pvals,uncorrected_exact,corrected_exact in (("independent",mins,independent,corrected),("duplicate",duplicates,alpha,alpha/m)):
            uncorrected=pvals<=float(alpha);bonferroni=pvals<=float(alpha/m)
            checks.append(dict(name=f"subset_{dependence}_m_{m}",passed=bool(np.all(~bonferroni|uncorrected))))
            for label,hits,exact in (("uncorrected",uncorrected,uncorrected_exact),("Bonferroni",bonferroni,corrected_exact)):
                rate=float(np.mean(hits));p=float(exact);tolerance=6*math.sqrt(p*(1-p)/n)+1/n
                record=dict(m=m,dependence=dependence,rule=label,exact_probability=str(exact),exact_rate=p,
                            discoveries=int(np.sum(hits)),studies=n,simulated_rate=rate,simulation_tolerance=tolerance)
                rows.append(record);checks.append(dict(name=f"null_rate_{dependence}_{label}_m_{m}",passed=abs(rate-p)<=tolerance))
    with (ROOT/"familywise_rates.csv").open("w",newline="") as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    data=np.column_stack((*minima,duplicates))
    stream=io.StringIO();np.savetxt(stream,data,delimiter=",",header="minimum_p_m1,minimum_p_m5,minimum_p_m20,minimum_p_m100,duplicate_family_p",comments="",fmt="%.17g")
    raw=stream.getvalue().encode();buffer=io.BytesIO()
    with gzip.GzipFile(filename="",fileobj=buffer,mode="wb",mtime=0) as archive:archive.write(raw)
    packed=buffer.getvalue();assert gzip.decompress(packed)==raw
    (ROOT/"synthetic_minima.csv.gz").write_bytes(packed)
    fig,ax=plt.subplots(figsize=(8.5,4.8),layout="constrained")
    x=np.arange(1,101)
    ax.plot(x,1-.95**x,label="Exact: independent, uncorrected",color="#bc4b37")
    ax.plot(x,1-(1-.05/x)**x,label="Exact: independent, Bonferroni",color="#16766c")
    ax.axhline(.05,color="#3659b8",ls="--",label="Exact: duplicated tests, uncorrected")
    for rule,color in (("uncorrected","#bc4b37"),("Bonferroni","#16766c")):
        subset=[row for row in rows if row["dependence"]=="independent" and row["rule"]==rule]
        ax.scatter([r["m"] for r in subset],[r["simulated_rate"] for r in subset],color=color,edgecolor="white",s=45,zorder=4,label=f"Seeded simulation: {rule}")
    ax.set(xlabel="Number of candidate tests in the family",ylabel="Probability of at least one false positive",ylim=(-.02,1.03),title="Picking the smallest p-value changes the false-positive probability")
    ax.legend(fontsize=8,loc="center right");ax.grid(alpha=.2)
    for ext in ("svg","png"):fig.savefig(ROOT/f"selection_bias.{ext}",dpi=170,bbox_inches="tight",metadata={"Date":None} if ext=="svg" else {})
    plt.close(fig)
    output=dict(round=5,status="passed" if all(c["passed"] for c in checks) else "failed",alpha_exact=str(alpha),seed=seed,replicates=n,
                model="Ideal valid uniform null p-values; exact independent and perfectly correlated control families; not empirical claim data",
                results=rows,checks=checks,runtime={"numpy":np.__version__},
                minima_archive=dict(path="synthetic_minima.csv.gz",raw_sha256=hashlib.sha256(raw).hexdigest(),gzip_sha256=hashlib.sha256(packed).hexdigest()),
                contract_sha256=hashlib.sha256((ROOT/"contract.md").read_bytes()).hexdigest(),solver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (ROOT/"results.json").write_text(json.dumps(output,indent=2)+"\n")
    print(json.dumps(dict(status=output["status"],checks=len(checks),selected=[row for row in rows if row["dependence"]=="independent"]),indent=2))
    if output["status"]!="passed":raise SystemExit(1)
if __name__=="__main__":run()
