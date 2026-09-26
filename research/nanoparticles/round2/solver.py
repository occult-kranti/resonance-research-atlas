#!/usr/bin/env python3
"""N2: thermal energy balance and an explicitly assumed thermometer response."""
from pathlib import Path
import csv,hashlib,json,platform
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent
C=4.;G=.02;P=.2;SENSOR=10.;PULSE=120.

def step(t,p=P,c=C,g=G,sensor=SENSOR):
    t=np.maximum(np.asarray(t,dtype=float),0.)
    if sensor<0 or c<=0 or g<0:raise ValueError("Require c>0,g>=0,sensor>=0")
    if g==0:
        theta=p*t/c
        y=theta if sensor==0 else p/c*(t+sensor*np.expm1(-t/sensor))
    else:
        a=c/g;theta=-p/g*np.expm1(-t/a)
        if sensor==0:y=theta
        elif np.isclose(a,sensor,rtol=0,atol=1e-14):y=p/g*(1-(1+t/a)*np.exp(-t/a))
        else:y=p/g*(1-(a*np.exp(-t/a)-sensor*np.exp(-t/sensor))/(a-sensor))
    return np.column_stack((np.atleast_1d(theta),np.atleast_1d(y)))

def pulse(t,p=P,c=C,g=G,sensor=SENSOR,duration=PULSE):
    return step(t,p,c,g,sensor)-step(np.asarray(t)-duration,p,c,g,sensor)

def rk4(dt,duration=400.,p=P,c=C,g=G,sensor=SENSOR,pulse_end=PULSE):
    if sensor<=0:raise ValueError("Dynamic sensor integration requires sensor>0")
    def rhs(y,power):return np.array([(power-g*y[0])/c,(y[0]-y[1])/sensor])
    n=round(duration/dt);values=np.zeros((n+1,2));state=values[0].copy()
    for i in range(n):
        power=p if i*dt<pulse_end else 0.
        a=rhs(state,power);b=rhs(state+dt*a/2,power);cc=rhs(state+dt*b/2,power);d=rhs(state+dt*cc,power)
        state=state+dt*(a+2*b+2*cc+d)/6;values[i+1]=state
    return np.arange(n+1)*dt,values

def run():
    checks=[];convergence=[]
    for dt in (.1,.05,.025):
        t,numeric=rk4(dt);exact=pulse(t);error=float(np.max(abs(numeric-exact)))
        convergence.append(dict(dt_s=dt,max_temperature_error_K=error))
    checks.append(dict(name="piecewise_ODE_exact_agreement",passed=convergence[-1]["max_temperature_error_K"]<1e-7))
    loss=np.concatenate(([0.],np.cumsum((G*exact[1:,0]+G*exact[:-1,0])*.025/2)))
    work=P*np.minimum(t,PULSE);budget=C*exact[:,0]-work+loss
    budget_error=float(np.max(abs(budget)))
    checks.append(dict(name="independent_thermal_budget",passed=budget_error<1e-7,max_residual_J=budget_error))
    times=np.array([10.,30.,60.]);windows=pulse(times);naive=C*windows[:,1]/times
    unit=step(times,p=1)[:,1];calibrated=windows[:,1]/unit
    checks.append(dict(name="duration_artifact_and_calibrated_inverse",passed=bool(np.all(naive<P) and len(set(naive))==3 and np.max(abs(calibrated-P))<1e-12)))
    scaling=[]
    for factor in (.5,2.,10.):scaling.append(dict(factor=factor,max_trace_error_K=float(np.max(abs(pulse(t,p=factor*P,c=factor*C,g=factor*G)-exact)))))
    checks.append(dict(name="scale_nonidentifiability_and_blank",passed=max(item["max_trace_error_K"] for item in scaling)<1e-12 and bool(np.all(pulse(t,p=0)==0))))
    branch_controls=[]
    for name,c,g,sensor in (("equal_time_constants",4.,.4,10.),("zero_heat_leak",4.,0.,10.)):
        bt,bn=rk4(.025,duration=120,p=P,c=c,g=g,sensor=sensor,pulse_end=120.)
        err=float(np.max(abs(bn-step(bt,p=P,c=c,g=g,sensor=sensor))))
        branch_controls.append(dict(name=name,max_error_K=err))
    checks.append(dict(name="removable_limit_controls",passed=max(item["max_error_K"] for item in branch_controls)<1e-7))
    np.savetxt(ROOT/"thermal_trace.csv",np.column_stack((t[::20],exact[::20],work[::20],loss[::20],budget[::20])),delimiter=",",comments="",fmt="%.17g",header="time_s,specimen_temperature_rise_K,sensor_temperature_rise_K,input_work_J,heat_leak_J,energy_residual_J")
    rows=[dict(window_s=float(tm),specimen_rise_K=float(theta),sensor_rise_K=float(y),naive_power_W=float(n),calibrated_power_W=float(cp)) for tm,(theta,y),n,cp in zip(times,windows,naive,calibrated)]
    for filename,data in (("duration_comparison.csv",rows),("convergence.csv",convergence)):
        with (ROOT/filename).open("w",newline="") as stream:writer=csv.DictWriter(stream,fieldnames=list(data[0]));writer.writeheader();writer.writerows(data)
    fig,axes=plt.subplots(1,2,figsize=(10.5,4.5),layout="constrained")
    axes[0].plot(t,exact[:,0],label="Specimen θ",color="#bc4b37");axes[0].plot(t,exact[:,1],label="Thermometer y",color="#3659b8")
    axes[0].axvline(120,color="#666666",ls=":",label="Power off at120s")
    axes[0].set(title="Constant input power, delayed measured temperature",xlabel="Time (s)",ylabel="Rise above initial temperature (K)")
    axes[1].plot(times,naive,"o-",label="Naive C y / duration",color="#bc4b37")
    axes[1].plot(times,calibrated,"s--",label="Calibrated thermal + sensor inverse",color="#16766c")
    axes[1].axhline(P,color="#555555",ls=":",label="True synthetic input:0.2W")
    axes[1].set(title="Changing the window changes the naive estimate",xlabel="Heating window (s)",ylabel="Estimated absorbed power (W)",ylim=(0,.22))
    for ax in axes:ax.legend(fontsize=8);ax.grid(alpha=.2)
    for ext in ("svg","png"):fig.savefig(ROOT/f"thermometer_bias.{ext}",dpi=170,bbox_inches="tight",metadata={"Date":None} if ext=="svg" else {})
    plt.close(fig)
    output=dict(round=2,branch="nanoparticles",hypothesis="NP-H2 duration-dependent naive power can be thermometer-transfer artifact",status="passed" if all(q["passed"] for q in checks) else "failed",
                parameters=dict(C_J_per_K=C,G_W_per_K=G,P_W=P,sensor_time_s=SENSOR,pulse_duration_s=PULSE),
                duration_comparisons=rows,convergence=convergence,scale_control=scaling,branch_controls=branch_controls,max_budget_residual_J=budget_error,checks=checks,
                scope="Synthetic lumped thermal + first-order sensor model, not nanoparticle or clinical measurements.",runtime=dict(python=platform.python_version(),numpy=np.__version__,matplotlib=matplotlib.__version__),
                hashes={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in ("contract.md","sources.md","solver.py")})
    (ROOT/"results.json").write_text(json.dumps(output,indent=2)+"\n");print(json.dumps(output,indent=2))
    if output["status"]!="passed":raise SystemExit(1)
if __name__=="__main__":run()
