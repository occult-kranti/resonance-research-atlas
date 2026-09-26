#!/usr/bin/env python3
"""N1: single-Debye loss/cycle, absorbed power and passive relaxation budget."""
from pathlib import Path
import csv,hashlib,json,math,platform
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent
MU0=4*math.pi*1e-7;CHI0=.02;TAU=1e-6;HPEAK=1.

def absorption(f,tau=TAU,chi0=CHI0,hpeak=HPEAK):
    x=2*np.pi*np.asarray(f)*tau
    loss=chi0*x/(1+x*x)
    cycle=np.pi*MU0*hpeak*hpeak*loss
    return loss,cycle,np.asarray(f)*cycle

def derivative(theta,y,x):
    m,_,_=y;drive=math.cos(theta);a=(drive-m)/x
    return a,drive*a,x*a*a

def integrate(x,steps):
    h=2*math.pi/steps;y=(0.,0.,0.);samples=[];max_residual=0.
    for n in range(60*steps):
        theta=n*h
        if n>=59*steps:samples.append((theta,*y))
        a=derivative(theta,y,x)
        b=derivative(theta+h/2,tuple(v+h*d/2 for v,d in zip(y,a)),x)
        c=derivative(theta+h/2,tuple(v+h*d/2 for v,d in zip(y,b)),x)
        d=derivative(theta+h,tuple(v+h*d for v,d in zip(y,c)),x)
        y=tuple(v+h*(aa+2*bb+2*cc+dd)/6 for v,aa,bb,cc,dd in zip(y,a,b,c,d))
        max_residual=max(max_residual,abs(.5*y[0]*y[0]-y[1]+y[2]))
    samples.append((60*steps*h,*y));data=np.array(samples);theta,m,w,d=data.T
    drive=np.cos(theta);exact=math.pi*x/(1+x*x)
    cycle_input=w[-1]-w[0];cycle_loss=d[-1]-d[0]
    loop=-float(np.sum((m[1:]+m[:-1])/2*np.diff(drive)))
    boundary=float(drive[-1]*m[-1]-drive[0]*m[0]);delta_energy=float((m[-1]**2-m[0]**2)/2)
    record=dict(x=x,steps_per_cycle=steps,cycles=60,settling_time_over_tau=2*np.pi*59/x,
                exact_normalized_cycle_work=exact,cycle_input_normalized=cycle_input,cycle_loss_normalized=cycle_loss,
                loop_quadrature_normalized=loop,cycle_storage_change_normalized=delta_energy,
                HM_boundary_normalized=boundary,max_all_run_budget_residual_normalized=max_residual,
                input_relative_error=abs(cycle_input-exact)/exact,loss_relative_error=abs(cycle_loss-exact)/exact,
                loop_relative_error=abs(loop-exact)/exact)
    return record,data

def run():
    x=np.logspace(-3,3,1201);f=x/(2*np.pi*TAU);real=CHI0/(1+x*x)
    loss,cycle,power=absorption(f);scale=MU0*CHI0*HPEAK**2;plateau=scale/(2*TAU)
    tau_scan=x*TAU;fixed_f=1/(2*np.pi*TAU);_,_,tau_power=absorption(fixed_f,tau=tau_scan)
    checks=[]
    limits={"low_cycle_ratio":float(cycle[0]/(np.pi*scale*x[0])),"low_power_ratio":float(power[0]/(plateau*x[0]**2)),"high_power_plateau_ratio":float(power[-1]/plateau)}
    checks.append(dict(name="frequency_scan_and_limits",passed=bool(np.all(loss>=0) and x[np.argmax(loss)]==1 and np.all(np.diff(power)>0) and all(abs(v-1)<2e-6 for v in limits.values()))))
    z_h=absorption(f,hpeak=0);z_chi=absorption(f,chi0=0);z_tau=absorption(f,tau=0)
    doubled=absorption(f,hpeak=2)
    checks.append(dict(name="zero_and_weak_field_scaling_controls",passed=bool(np.all(z_h[1]==0) and np.all(z_h[2]==0) and np.all(z_chi[1]==0) and np.all(z_tau[2]==0) and np.allclose(doubled[1],4*cycle,rtol=1e-14,atol=0) and np.allclose(doubled[2],4*power,rtol=1e-14,atol=0))))
    ratio_error=float(np.max(abs(loss/real-x)/x));checks.append(dict(name="calibrated_phase_ratio",passed=ratio_error<1e-12,relative_error=ratio_error))
    convergence=[];last_cycles=[]
    for testx in (.1,1.,10.):
        group=[]
        for steps in (512,1024,2048):
            record,data=integrate(testx,steps);convergence.append(record);group.append(record)
            if steps==2048:
                # Save every fourth fine sample, preserving a complete 512-segment cycle.
                angle=data[::4,0];magnetization=CHI0*HPEAK*data[::4,1]
                last_cycles.append(np.column_stack((np.full_like(angle,testx),(angle-angle[0])*TAU/testx,HPEAK*np.cos(angle),magnetization)))
        final=group[-1]
        checks.append(dict(name=f"passive_periodic_budget_x_{testx:g}",passed=final["input_relative_error"]<1e-5 and final["loss_relative_error"]<1e-5 and final["max_all_run_budget_residual_normalized"]<1e-5))
        errors=[item["loop_relative_error"] for item in group]
        checks.append(dict(name=f"independent_loop_convergence_x_{testx:g}",passed=errors[0]>errors[1]>errors[2] and errors[-1]<2e-6))
    checks.append(dict(name="different_fixed_frequency_tau_scan",passed=bool(x[np.argmax(tau_power)]==1)))
    np.savetxt(ROOT/"frequency_sweep.csv",np.column_stack((x,f,real,loss,cycle,power,tau_scan,tau_power)),delimiter=",",comments="",fmt="%.17g",header="x_omega_tau,frequency_Hz,chi_real,chi_loss,loss_per_cycle_J_per_m3,power_W_per_m3,tau_scan_s,tau_scan_fixed_frequency_power_W_per_m3")
    with (ROOT/"convergence.csv").open("w",newline="") as stream:
        writer=csv.DictWriter(stream,fieldnames=list(convergence[0]));writer.writeheader();writer.writerows(convergence)
    np.savetxt(ROOT/"final_cycles.csv",np.vstack(last_cycles),delimiter=",",comments="",fmt="%.17g",header="x_omega_tau,time_within_last_cycle_s,H_A_per_m,M_A_per_m")
    fig,axes=plt.subplots(1,3,figsize=(12,4.2),layout="constrained")
    axes[0].semilogx(x,loss/CHI0,color="#3659b8");axes[0].axvline(1,ls=":",color="#555555")
    axes[0].set(title="Loss factor / cycle",xlabel="ωτ (dimensionless)",ylabel="χ″ / χ₀",ylim=(0,.55))
    axes[1].semilogx(x,power/plateau,color="#bc4b37")
    axes[1].set(title="Frequency scan: τ and H fixed",xlabel="ωτ (dimensionless)",ylabel="Power / high-frequency model limit")
    axes[2].semilogx(x,tau_power/np.max(tau_power),color="#16766c")
    axes[2].set(title="Relaxation-time scan: f and H fixed",xlabel="ωτ (dimensionless)",ylabel="Power / its maximum")
    for ax in axes:ax.grid(alpha=.2)
    fig.suptitle("Single-Debye mathematical response — not a material validity range",fontsize=12)
    save(fig,"loss_and_power")
    fig,ax=plt.subplots(figsize=(6.5,4.8),layout="constrained")
    for values,testx in zip(last_cycles,(.1,1.,10.)):ax.plot(values[:,2],values[:,3],label=f"ωτ = {testx:g}")
    ax.set(xlabel="Applied H (A/m)",ylabel="Magnetization M (A/m)",title="Relaxation phase lag produces a dissipative loop")
    ax.legend();ax.grid(alpha=.2);save(fig,"relaxation_loops")
    result=dict(round=1,branch="nanoparticles",hypothesis="NP-H1, project hypothesis applying established Debye theory",status="passed" if all(c["passed"] for c in checks) else "failed",
                parameters={"chi0":CHI0,"tau_s":TAU,"H_peak_A_per_m":HPEAK,"mu0_nominal_H_per_m":MU0},
                reference_frequency_Hz=fixed_f,loss_peak_x=float(x[np.argmax(loss)]),power_at_x1_W_per_m3=float(absorption(fixed_f)[2]),
                power_model_limit_W_per_m3=plateau,limits=limits,convergence=convergence,checks=checks,
                scope="Linear response synthetic normalization. Full x sweep is mathematical extrapolation, not real nanoparticle/high-frequency/body prediction.",
                runtime={"python":platform.python_version(),"numpy":np.__version__,"matplotlib":matplotlib.__version__},
                hashes={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in ("contract.md","sources.md","bibliographic-erratum.md","solver.py")})
    (ROOT/"results.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(dict(status=result["status"],checks=len(checks),limits=limits,convergence=convergence),indent=2))
    if result["status"]!="passed":raise SystemExit(1)
def save(fig,name):
    for ext in ("svg","png"):fig.savefig(ROOT/f"{name}.{ext}",dpi=170,bbox_inches="tight",metadata={"Date":None} if ext=="svg" else {})
    plt.close(fig)
if __name__=="__main__":run()
