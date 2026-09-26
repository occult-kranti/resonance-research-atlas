#!/usr/bin/env python3
"""N3: distinct single-rate and two-population response candidates."""
from pathlib import Path
import csv,hashlib,json,platform
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent
KB=1.380649e-23;T=298.;DIAMETER=50e-9;TAUN=.001;CHI0=.02
def debye(w,tau,chi0=CHI0):return chi0/(1+1j*np.asarray(w)*tau)
def apparent(w,chi):return -chi.imag/(np.asarray(w)*chi.real)
def run():
    eta=np.array([.001,.002,.005,.01]);beta=np.pi*DIAMETER**3/(2*KB*T);tb=beta*eta
    teff=1/(1/tb+1/TAUN);feff=1/(2*np.pi*teff)
    coeff=np.linalg.solve(np.column_stack((1/eta[:2],np.ones(2))),feff[:2]);pred=coeff[0]/eta+coeff[1]
    prediction_error=float(np.max(abs(pred[2:]-feff[2:])/feff[2:]))
    checks=[dict(name="Brownian_scaling_and_held_out_viscosity",passed=bool(tb[1]==2*tb[0] and prediction_error<1e-12),held_out_relative_error=prediction_error)]
    f=np.logspace(1,6,1001);w=2*np.pi*f;refw=2*np.pi*1000;records=[];spectra=[]
    for viscosity,tbrown,effective,freq in zip(eta,tb,teff,feff):
        ca=debye(w,effective);cb=.5*debye(w,tbrown)+.5*debye(w,TAUN)
        appa=apparent(w,ca);appb=apparent(w,cb)
        rational=(.5*tbrown+.5*TAUN+w*w*(.5*tbrown*TAUN**2+.5*TAUN*tbrown**2))/(1+w*w*(.5*TAUN**2+.5*tbrown**2))
        ref=.5*debye(refw,tbrown)+.5*debye(refw,TAUN);fit_tau=float(apparent(refw,ref));fit_chi=float(ref.real*(1+(refw*fit_tau)**2))
        fit=debye(w,fit_tau,fit_chi);ref_error=float(abs(debye(refw,fit_tau,fit_chi)-ref)/abs(ref))
        residual=abs(fit-cb)/abs(cb);held=f!=1000
        # Whole-domain derivative is negative for unequal positive relaxation times.
        derivative=-.25*(tbrown+TAUN)*(tbrown-TAUN)**2/(1+w*w*(.5*TAUN**2+.5*tbrown**2))**2
        row=dict(viscosity_Pa_s=float(viscosity),tau_B_s=float(tbrown),tau_N_s=TAUN,tau_eff_s=float(effective),f_eff_Hz=float(freq),
                 predicted_f_eff_Hz=float(coeff[0]/viscosity+coeff[1]),tau_fit_s=fit_tau,chi0_fit=fit_chi,
                 reference_complex_relative_error=ref_error,max_held_out_relative_residual=float(np.max(residual[held])),
                 single_tau_app_max_relative_error=float(np.max(abs(appa-effective)/effective)),
                 mixture_rational_max_relative_error=float(np.max(abs(appb-rational)/appb)),
                 mixture_tau_app_low_s=float(appb[0]),mixture_tau_app_high_s=float(appb[-1]),
                 mixture_tau_app_in_bounds=bool(np.all(appb>=min(tbrown,TAUN)) and np.all(appb<=max(tbrown,TAUN))),
                 mixture_tau_app_strictly_decreasing=bool(np.all(np.diff(appb)<0)),analytic_derivative_negative=bool(np.all(derivative<0)))
        records.append(row);spectra.append(np.column_stack((np.full_like(f,viscosity),f,ca.real,-ca.imag,cb.real,-cb.imag,appa,appb,fit.real,-fit.imag,residual)))
    checks.extend([
        dict(name="single_Debye_constant_tau_app",passed=max(r["single_tau_app_max_relative_error"] for r in records)<1e-12),
        dict(name="mixture_bounds_monotonicity_and_independent_formula",passed=all(r["mixture_tau_app_in_bounds"] and r["mixture_tau_app_strictly_decreasing"] and r["analytic_derivative_negative"] and r["mixture_rational_max_relative_error"]<1e-12 for r in records)),
        dict(name="one_frequency_match_held_out_rejection",passed=max(r["reference_complex_relative_error"] for r in records)<1e-12 and records[0]["max_held_out_relative_residual"]>.05)
    ])
    equal=.5*debye(w,TAUN)+.5*debye(w,TAUN);equal_error=float(np.max(abs(equal-debye(w,TAUN))/abs(debye(w,TAUN))))
    checks.append(dict(name="equal_time_and_zero_response_controls",passed=equal_error<1e-12 and bool(np.all(debye(w,TAUN,0)==0))))
    np.savetxt(ROOT/"response_spectra.csv",np.vstack(spectra),delimiter=",",comments="",fmt="%.17g",header="viscosity_Pa_s,frequency_Hz,single_chi_real,single_chi_loss,mixture_chi_real,mixture_chi_loss,single_tau_app_s,mixture_tau_app_s,fitted_chi_real,fitted_chi_loss,fit_relative_complex_residual")
    with (ROOT/"viscosity_predictions.csv").open("w",newline="") as stream:writer=csv.DictWriter(stream,fieldnames=list(records[0]));writer.writeheader();writer.writerows(records)
    fig,axes=plt.subplots(1,3,figsize=(12,4.2),layout="constrained")
    axes[0].plot(1/eta,feff,"o",label="Synthetic values",color="#3659b8")
    xx=np.linspace(80,1020,100);axes[0].plot(xx,coeff[0]*xx+coeff[1],label="Fit first two viscosities",color="#16766c")
    axes[0].set(xlabel="Inverse viscosity (Pa⁻¹ s⁻¹)",ylabel="Effective single-Debye loss-peak f (Hz)",title="Single-rate candidate: held-out viscosity")
    for data,row in zip(spectra,records):axes[1].semilogx(f,data[:,7]*1e6,label=f"η = {row['viscosity_Pa_s']:g} Pa s")
    axes[1].set(xlabel="Frequency (Hz)",ylabel="Mixture apparent relaxation time (µs)",title="Two populations: nonconstant apparent time")
    axes[2].semilogx(f,spectra[0][:,-1],color="#bc4b37");axes[2].axvline(1000,color="#555555",ls=":")
    axes[2].set(xlabel="Frequency (Hz)",ylabel="Relative complex-susceptibility residual",title="Single fit matches only the calibration point")
    for ax in axes:ax.grid(alpha=.2)
    axes[0].legend(fontsize=7);axes[1].legend(fontsize=7)
    for ext in ("svg","png"):fig.savefig(ROOT/f"relaxation_discrimination.{ext}",dpi=170,bbox_inches="tight",metadata={"Date":None} if ext=="svg" else {})
    plt.close(fig)
    output=dict(round=3,branch="nanoparticles",status="passed" if all(c["passed"] for c in checks) else "failed",hypothesis="NP-H3 held-out frequency and viscosity distinguish declared relaxation populations",
                parameters=dict(T_K=T,kB_J_per_K=KB,diameter_hydrodynamic_m=DIAMETER,tau_N_s=TAUN,chi0=CHI0),
                fit=dict(slope_Hz_Pa_s=float(coeff[0]),intercept_Hz=float(coeff[1]),training_viscosities_Pa_s=eta[:2].tolist(),held_out_viscosities_Pa_s=eta[2:].tolist()),cases=records,checks=checks,
                scope="Synthetic candidate populations, unknown rival amplitude at one-point fit; no actual particle mechanism inferred.",runtime=dict(python=platform.python_version(),numpy=np.__version__,matplotlib=matplotlib.__version__),
                hashes={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in ("contract.md","sources.md","solver.py")})
    (ROOT/"results.json").write_text(json.dumps(output,indent=2)+"\n");print(json.dumps(output,indent=2))
    if output["status"]!="passed":raise SystemExit(1)
if __name__=="__main__":run()
