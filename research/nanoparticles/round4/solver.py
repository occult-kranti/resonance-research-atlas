#!/usr/bin/env python3
"""N4: exact size moments and conditional normalized susceptibility weights."""
from fractions import Fraction as F
from pathlib import Path
import csv,hashlib,json,math,platform
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent
def normalized_response(w,weights,taus):return sum(float(a)/(1+1j*np.asarray(w)*tau) for a,tau in zip(weights,taus))
def concentration(cmass,rho,moment_nm3):return cmass/(rho*np.pi/6*float(moment_nm3)*1e-27)
def run():
    core=[F(40),F(60)];hydro=np.array([50.,70.])*1e-9;number=[F(1,2),F(1,2)]
    mean=sum(p*d for p,d in zip(number,core));moment=sum(p*d**3 for p,d in zip(number,core));mean_cube=mean**3
    mass=[p*d**3/moment for p,d in zip(number,core)]
    sixth=sum(p*d**6 for p,d in zip(number,core));chi=[p*d**6/sixth for p,d in zip(number,core)]
    ratio=moment/mean_cube;rho=5000.;cmass=.001
    correct=concentration(cmass,rho,moment);naive=concentration(cmass,rho,mean_cube)
    checks=[dict(name="exact_moments_and_distinct_weights",passed=moment==140000 and mean_cube==125000 and ratio==F(28,25) and mass==[F(8,35),F(27,35)] and chi==[F(64,793),F(729,793)] and number!=mass!=chi)]
    checks.append(dict(name="positive_normalizations_and_concentration_scaling",passed=all(sum(ws,F(0))==1 and min(ws)>0 for ws in (number,mass,chi)) and correct>0 and math.isclose(concentration(2*cmass,rho,moment),2*correct,rel_tol=1e-14) and math.isclose(concentration(cmass,2*rho,moment),correct/2,rel_tol=1e-14)))
    kb=1.380649e-23;temp=298.;eta=.001;taus=np.pi*eta*hydro**3/(2*kb*temp)
    f=np.logspace(1,6,1001);w=2*np.pi*f;true=normalized_response(w,chi,taus);rival=normalized_response(w,number,taus)
    residual=abs(rival-true)/abs(true);index=int(np.argmax(residual));maxres=float(residual[index])
    checks.append(dict(name="DC_agreement_held_out_disagreement",passed=normalized_response(0,chi,taus)==1 and normalized_response(0,number,taus)==1 and maxres>.01))
    swapped=normalized_response(w,chi[::-1],taus[::-1]);mono_tau=np.pi*eta*(60e-9)**3/(2*kb*temp)
    mono=normalized_response(w,[F(1,2),F(1,2)],[mono_tau,mono_tau]);single=1/(1+1j*w*mono_tau)
    swaperr=float(np.max(abs(swapped-true)/abs(true)));monoerr=float(np.max(abs(mono-single)/abs(single)))
    checks.append(dict(name="label_swap_and_monodisperse_controls",passed=swaperr<1e-12 and monoerr<1e-12))
    # Independent combined-rational expression has one numerator and two poles.
    rational=(1+1j*w*(float(chi[0])*taus[1]+float(chi[1])*taus[0]))/((1+1j*w*taus[0])*(1+1j*w*taus[1]))
    rationalerr=float(np.max(abs(rational-true)/abs(true)))
    checks.append(dict(name="combined_rational_response_control",passed=rationalerr<1e-12))
    np.savetxt(ROOT/"weighted_response.csv",np.column_stack((f,true.real,-true.imag,rival.real,-rival.imag,residual)),delimiter=",",comments="",fmt="%.17g",header="frequency_Hz,correct_normalized_chi_real,correct_normalized_chi_loss,naive_normalized_chi_real,naive_normalized_chi_loss,relative_complex_residual")
    with (ROOT/"population_weights.csv").open("w",newline="") as stream:
        writer=csv.writer(stream);writer.writerow(["core_diameter_nm_exact","hydrodynamic_diameter_m","number_weight_exact","mass_weight_exact","conditional_chi_weight_exact","tau_B_s"])
        for d,dh,n,m,c,tau in zip(core,hydro,number,mass,chi,taus):writer.writerow([str(d),dh,str(n),str(m),str(c),tau])
    fig,axes=plt.subplots(1,3,figsize=(12,4.3),layout="constrained")
    xpos=np.arange(3);first=np.array([float(number[0]),float(mass[0]),float(chi[0])]);second=1-first
    axes[0].bar(xpos,first,label="40nm core",color="#3659b8");axes[0].bar(xpos,second,bottom=first,label="60nm core",color="#bc4b37")
    axes[0].set(xticks=xpos,xticklabels=["Number","Mass","Susceptibility"],ylabel="Fraction of specified quantity",title="Different quantities, different weights",ylim=(0,1.12))
    axes[0].legend(fontsize=8)
    axes[1].loglog(f,abs(true),label="Conditional susceptibility weights",color="#16766c");axes[1].loglog(f,abs(rival),ls="--",label="Naive equal-number weights",color="#bc4b37")
    axes[1].set(xlabel="Frequency (Hz)",ylabel="|χ(ω) / χ(0)|",title="Same DC scale, different spectral prediction");axes[1].legend(fontsize=7)
    axes[2].semilogx(f,residual*100,color="#bc4b37");axes[2].set(xlabel="Frequency (Hz)",ylabel="Relative complex residual (%)",title="Wrong weights leave a shape discrepancy")
    for ax in axes:ax.grid(axis="y",alpha=.2)
    for ext in ("svg","png"):fig.savefig(ROOT/f"size_and_weighting.{ext}",dpi=170,bbox_inches="tight",metadata={"Date":None} if ext=="svg" else {})
    plt.close(fig)
    output=dict(round=4,branch="nanoparticles",status="passed" if all(q["passed"] for q in checks) else "failed",hypothesis="NP-H4 size moments and distinct response weights alter count and held-out spectrum predictions",
                parameters=dict(core_diameters_nm=[str(d) for d in core],hydrodynamic_diameters_m=hydro.tolist(),rho_kg_per_m3=rho,mass_concentration_kg_per_m3=cmass,eta_Pa_s=eta,T_K=temp),
                exact_moments=dict(mean_core_diameter_nm=str(mean),mean_core_cube_nm3=str(moment),cube_mean_core_nm3=str(mean_cube),naive_to_correct_count_ratio=str(ratio)),
                weights=dict(number=[str(v) for v in number],mass=[str(v) for v in mass],conditional_susceptibility=[str(v) for v in chi]),
                number_concentration_correct_per_m3=correct,number_concentration_naive_per_m3=naive,tau_B_s=taus.tolist(),
                max_relative_spectral_residual=maxres,max_residual_frequency_Hz=float(f[index]),label_swap_relative_error=swaperr,monodisperse_relative_error=monoerr,rational_relative_error=rationalerr,checks=checks,
                scope="Conditional synthetic spheres with identical magnetization density and locked moments. No absolute susceptibility or actual particle operating regime inferred.",
                runtime=dict(python=platform.python_version(),numpy=np.__version__,matplotlib=matplotlib.__version__),hashes={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in ("contract.md","sources.md","solver.py")})
    (ROOT/"results.json").write_text(json.dumps(output,indent=2)+"\n");print(json.dumps(output,indent=2))
    if output["status"]!="passed":raise SystemExit(1)
if __name__=="__main__":run()
