#!/usr/bin/env python3
"""Exact rational inverse-problem example; synthetic assays, not chemistry."""
from fractions import Fraction as F
from pathlib import Path
import csv,hashlib,json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent

def matvec(a,x):return [sum((F(v)*w for v,w in zip(row,x)),F(0)) for row in a]
def rref(matrix):
    a=[[F(x) for x in row] for row in matrix];row=0;pivots=[]
    for col in range(len(a[0])):
        pivot=next((j for j in range(row,len(a)) if a[j][col]),None)
        if pivot is None:continue
        a[row],a[pivot]=a[pivot],a[row]
        value=a[row][col];a[row]=[x/value for x in a[row]]
        for other in range(len(a)):
            if other!=row:
                factor=a[other][col];a[other]=[x-factor*y for x,y in zip(a[other],a[row])]
        pivots.append(col);row+=1
        if row==len(a):break
    return a,pivots
def inverse_solve(a,b):
    reduced,pivots=rref([list(row)+[y] for row,y in zip(a,b)])
    if pivots!=[0,1,2]:raise ValueError("Not a uniquely invertible 3-component system")
    return [row[-1] for row in reduced]

def run():
    a=[[1,0,1],[0,1,1]];independent=a+[[0,0,1]];duplicate=a+[[1,0,1]]
    reference=[F(1,5),F(2,5),F(3,10)];kernel=[F(-1),F(-1),F(1)]
    y=matvec(a,reference);low=F(-3,10);high=F(1,5)
    ts=[low+(high-low)*F(i,100) for i in range(101)]
    family=[[c+t*n for c,n in zip(reference,kernel)] for t in ts]
    ranks={"original":len(rref(a)[1]),"independent":len(rref(independent)[1]),"duplicate":len(rref(duplicate)[1])}
    checks=[]
    checks.append(dict(name="exact_kernel_and_domain_rank",passed=ranks["original"]==2 and matvec(a,kernel)==[0,0]))
    checks.append(dict(name="nonnegative_equal_signal_fiber",passed=all(min(c)>=0 and matvec(a,c)==y for c in family)))
    exact_recovery=all(inverse_solve(independent,matvec(independent,c))==c for c in (reference,family[0],family[-1]))
    numerical_error=max(float(np.max(abs(np.linalg.solve(np.array(independent,dtype=float),np.array(matvec(independent,c),dtype=float))-np.array(c,dtype=float)))) for c in (reference,family[0],family[-1]))
    checks.append(dict(name="independent_assay_recovery",passed=ranks["independent"]==3 and exact_recovery and numerical_error<=1e-12,numerical_error=numerical_error))
    checks.append(dict(name="duplicate_assay_remains_ambiguous",passed=ranks["duplicate"]==2 and family[0]!=family[-1] and matvec(duplicate,family[0])==matvec(duplicate,family[-1])))
    checks.append(dict(name="no_hidden_sum_constraint",passed=len(set(sum(c) for c in family))>1))
    with (ROOT/"composition_fiber.csv").open("w",newline="") as stream:
        writer=csv.writer(stream);writer.writerow(["t_exact","c1_exact","c2_exact","c3_exact","signal1_exact","signal2_exact","independent_signal3_exact","sum_exact"])
        for t,c in zip(ts,family):writer.writerow([str(t),*[str(v) for v in c],*[str(v) for v in y],str(c[2]),str(sum(c))])
    fig,axes=plt.subplots(1,2,figsize=(10,4.6),layout="constrained")
    x=np.array(ts,dtype=float);cs=np.array(family,dtype=float)
    for i,label in enumerate(("Component 1","Component 2","Component 3")):axes[0].plot(x,cs[:,i],label=label)
    axes[0].set(xlabel="Kernel parameter t (dimensionless)",ylabel="Relative amount (dimensionless)",title="Different nonnegative compositions")
    axes[1].plot(x,np.full_like(x,float(y[0])),label="Original signal 1",color="#3659b8")
    axes[1].plot(x,np.full_like(x,float(y[1])),label="Original signal 2",color="#bc4b37")
    axes[1].plot(x,cs[:,2],label="New independent signal 3",color="#16766c",ls="--")
    axes[1].set(xlabel="Kernel parameter t (dimensionless)",ylabel="Calibrated signal (dimensionless)",title="Two signals cannot distinguish the family")
    for ax in axes:ax.legend(fontsize=8);ax.grid(alpha=.2)
    for ext in ("svg","png"):fig.savefig(ROOT/f"composition_ambiguity.{ext}",dpi=170,bbox_inches="tight",metadata={"Date":None} if ext=="svg" else {})
    plt.close(fig)
    output=dict(round=3,status="passed" if all(c["passed"] for c in checks) else "failed",model="Exact synthetic linear assays; relative amounts are not fractions",
                original_matrix=a,independent_matrix=independent,duplicate_matrix=duplicate,domain_dimension=3,ranks=ranks,
                nullities={name:3-rank for name,rank in ranks.items()},kernel=[str(v) for v in kernel],
                reference=[str(v) for v in reference],original_signals=[str(v) for v in y],fiber_interval=[str(low),str(high)],
                endpoints=[[str(v) for v in family[0]],[str(v) for v in family[-1]]],endpoint_sums=[str(sum(family[0])),str(sum(family[-1]))],
                original_rref=[[str(v) for v in row] for row in rref(a)[0]],
                original_rectangular_singular_values=np.linalg.svd(np.array(a,dtype=float),compute_uv=False).tolist(),
                note="A 2x3 matrix has only two returned singular values; both nonzero does not remove its one-dimensional kernel.",checks=checks,
                contract_sha256=hashlib.sha256((ROOT/"contract.md").read_bytes()).hexdigest(),solver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (ROOT/"results.json").write_text(json.dumps(output,indent=2)+"\n");print(json.dumps(output,indent=2))
    if output["status"]!="passed":raise SystemExit(1)
if __name__=="__main__":run()
