#!/usr/bin/env python3
"""Exact bounded-noise inverse calculation; fixed assay scales, no clipping."""
from fractions import Fraction as F
from pathlib import Path
import csv,hashlib,itertools,json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent

def determinant(a):
    return sum(((-1)**(sum(p[i]>p[j] for i in range(3) for j in range(i+1,3)))*a[0][p[0]]*a[1][p[1]]*a[2][p[2]]
                for p in itertools.permutations(range(3))),F(0))
def matvec(a,c):return [sum((v*x for v,x in zip(row,c)),F(0)) for row in a]
def near_inverse(y,e):
    c3=(y[2]-y[0])/e
    return [y[0]-c3,y[1]-c3,c3]
def independent_inverse(y):return [y[0]-y[2],y[1]-y[2],y[2]]

def run():
    c=[F(1,5),F(2,5),F(3,10)];delta=F(1,1000)
    corners=list(itertools.product((-delta,delta),repeat=3));checks=[];cases=[];csv_rows=[]
    for eps in (F(1),F(1,10),F(1,100),F(1,1000)):
        a=[[F(1),F(0),F(1)],[F(0),F(1),F(1)],[F(1),F(0),F(1)+eps]]
        clean=matvec(a,c);errors=[];negative=0;numeric_error=0.
        for eta in corners:
            noisy=[v+e for v,e in zip(clean,eta)];estimate=near_inverse(noisy,eps)
            error=[v-x for v,x in zip(estimate,c)];errors.append(error)
            negative+=int(min(estimate)<0)
            numeric=np.linalg.solve(np.array(a,dtype=float),np.array(noisy,dtype=float))
            numeric_error=max(numeric_error,float(np.max(abs(numeric-np.array(estimate,dtype=float)))))
            csv_rows.append([str(eps),*[str(v) for v in eta],*[str(v) for v in estimate],*[str(v) for v in error]])
        maxima=[max(abs(v[i]) for v in errors) for i in range(3)]
        bounds=[delta*(1+2/eps),delta*(1+2/eps),2*delta/eps]
        chosen=[-delta,delta,delta];chosen_est=near_inverse([v+e for v,e in zip(clean,chosen)],eps)
        entry=dict(epsilon=str(eps),determinant=str(determinant(a)),rank=3,condition_number_2=float(np.linalg.cond(np.array(a,dtype=float))),
                   exact_component_error_bounds=[str(v) for v in bounds],corner_max_abs_error=[str(v) for v in maxima],
                   bound_c3_float=float(bounds[2]),negative_corner_count=negative,numeric_vs_exact_max_error=numeric_error)
        cases.append(entry)
        checks.append(dict(name=f"exact_bounds_eps_{eps}",passed=determinant(a)==eps and maxima==bounds and chosen_est[2]-c[2]==bounds[2] and numeric_error<=1e-10))
    independent=[[F(1),F(0),F(1)],[F(0),F(1),F(1)],[F(0),F(0),F(1)]]
    y=matvec(independent,c)
    ie=[[v-x for v,x in zip(independent_inverse([v+n for v,n in zip(y,eta)]),c)] for eta in corners]
    imax=[max(abs(v[i]) for v in ie) for i in range(3)]
    checks.append(dict(name="independent_assay_bounds",passed=imax==[2*delta,2*delta,delta]))
    singular=[[F(1),F(0),F(1)],[F(0),F(1),F(1)],[F(1),F(0),F(1)]]
    # Top-left 2x2 identity proves rank >=2; determinant zero proves rank <3.
    minor=singular[0][0]*singular[1][1]-singular[0][1]*singular[1][0]
    checks.append(dict(name="zero_epsilon_nonuniqueness",passed=determinant(singular)==0 and minor==1))
    checks.append(dict(name="negative_unconstrained_estimates_retained",passed=cases[-1]["negative_corner_count"]>0))
    with (ROOT/"noise_corners.csv").open("w",newline="") as stream:
        writer=csv.writer(stream);writer.writerow(["epsilon_exact","eta1_exact","eta2_exact","eta3_exact","estimate_c1_exact","estimate_c2_exact","estimate_c3_exact","error_c1_exact","error_c2_exact","error_c3_exact"]);writer.writerows(csv_rows)
    x=np.array([float(F(entry["epsilon"])) for entry in cases]);y=np.array([entry["bound_c3_float"] for entry in cases])
    fig,ax=plt.subplots(figsize=(8,4.8),layout="constrained")
    ax.loglog(x,y,"o-",label="Near duplicate: exact worst error 2δ/ε",color="#bc4b37")
    ax.axhline(float(delta),label="Independent third channel: error ≤ δ",color="#16766c",ls="--")
    ax.axhline(.3,label="Reference component amount c₃ = 0.3",color="#666666",ls=":")
    ax.set(xlabel="Difference coefficient ε (dimensionless)",ylabel="Worst absolute c₃ error (dimensionless)",title="Unique inverse, unstable estimate: fixed channel noise δ = 0.001")
    ax.legend(fontsize=9);ax.grid(which="both",alpha=.2)
    for ext in ("svg","png"):fig.savefig(ROOT/f"noise_amplification.{ext}",dpi=170,bbox_inches="tight",metadata={"Date":None} if ext=="svg" else {})
    plt.close(fig)
    output=dict(round=4,status="passed" if all(item["passed"] for item in checks) else "failed",delta_exact=str(delta),relative_amounts=[str(v) for v in c],
                assumptions="Fixed assay row coefficients and fixed absolute additive error per channel. No row rescaling, clipping, stochastic distribution or fraction-sum constraint.",
                cases=cases,independent_component_bounds=[str(v) for v in imax],singular_control_rank=2,checks=checks,
                contract_sha256=hashlib.sha256((ROOT/"contract.md").read_bytes()).hexdigest(),solver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (ROOT/"results.json").write_text(json.dumps(output,indent=2)+"\n");print(json.dumps(output,indent=2))
    if output["status"]!="passed":raise SystemExit(1)
if __name__=="__main__":run()
