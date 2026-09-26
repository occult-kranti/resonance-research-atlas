#!/usr/bin/env python3
"""Round 2: exact spectral transfer functions; no time-series sample noise."""
from pathlib import Path
import hashlib
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent

def response(f, f0, gamma):
    w=2*np.pi*np.asarray(f)
    return 1/((2*np.pi*f0)**2-w*w+2j*gamma*w)

def poles(f0,gamma):
    root=np.lib.scimath.sqrt(gamma*gamma-(2*np.pi*f0)**2)
    return np.asarray([-gamma+root,-gamma-root],dtype=complex)

def colored_source(f):
    """Even extension required for the PSD of a real stationary forcing."""
    return 1+100*np.exp(-.5*((abs(np.asarray(f))-12)/.25)**2)

def run():
    f=np.linspace(0,20,20001); w=2*np.pi*f; w0=2*np.pi*8
    checks=[]; cases=[]; records=[]
    for gamma in (5.,20.,w0/np.sqrt(2),40.,60.):
        hx=response(f,8,gamma); hv=1j*w*hx
        sx=abs(hx)**2; sv=abs(hv)**2
        px=float(f[np.argmax(sx)]); pv=float(f[np.argmax(sv)])
        predicted=np.sqrt(max(w0*w0-2*gamma*gamma,0))/(2*np.pi)
        entry=dict(gamma_per_s=gamma, predicted_displacement_peak_Hz=float(predicted),
                   grid_displacement_peak_Hz=px, predicted_velocity_peak_Hz=8.,grid_velocity_peak_Hz=pv,
                   poles_per_s=[[float(p.real),float(p.imag)] for p in poles(8,gamma)])
        cases.append(entry)
        checks.append(dict(name=f"peak_prediction_gamma_{gamma:g}",passed=bool(abs(px-predicted)<=.0011 and abs(pv-8)<=.0011)))
        records.append(np.column_stack((f,np.full_like(f,gamma),sx,sv)))
    np.savetxt(ROOT/"spectra.csv",np.vstack(records),delimiter=",",comments="",fmt="%.17g",
               header="frequency_Hz,gamma_per_s,displacement_PSD_m2_s,velocity_PSD_m2_per_s")
    hx=response(f,8,5); hv=1j*w*hx
    # Independent algebraic form of velocity transfer magnitude.
    sv_independent=w*w/((w0*w0-w*w)**2+4*25*w*w)
    residual=float(np.max(abs(abs(hv)**2-sv_independent)))
    checks.append(dict(name="measurement_transfer_identity",passed=residual<=1e-12,observed=residual))
    h2=response(f,10,8); source2=abs(hx)**2/abs(h2)**2
    sx1=abs(hx)**2; sx2=abs(h2)**2*source2
    ambiguous_error=float(np.max(abs(sx1-sx2)/sx1))
    different_poles=not np.allclose(np.sort_complex(poles(8,5)),np.sort_complex(poles(10,8)))
    checks.append(dict(name="unknown_source_nonidentifiability",passed=bool(np.isfinite(source2).all() and np.all(source2>0) and different_poles and ambiguous_error<=1e-12),max_relative_PSD_error=ambiguous_error))
    source_colored=colored_source(f)
    checks.append(dict(name="review_added_real_source_PSD_evenness",passed=bool(np.array_equal(colored_source(-f),source_colored))))
    colored_output=sx1*source_colored
    white_peak=float(f[np.argmax(sx1)]); colored_peak=float(f[np.argmax(colored_output)])
    checks.append(dict(name="source_only_peak_shift",passed=abs(colored_peak-white_peak)>1,
                       white_peak_Hz=white_peak,colored_peak_Hz=colored_peak))
    np.savetxt(ROOT/"source_ambiguity.csv",np.column_stack((f,source2,sx1,sx2,source_colored,colored_output)),
               delimiter=",",comments="",fmt="%.17g",
               header="frequency_Hz,compensating_input_PSD_m2_per_s3,model1_output_PSD_m2_s,model2_output_PSD_m2_s,colored_input_PSD_m2_per_s3,colored_output_PSD_m2_s")
    calibration_f=np.array([1.,4.,8.,12.,18.]); calibration_w=2*np.pi*calibration_f
    calibration_psd=abs(response(calibration_f,8,5))**2
    scale=100.; z=calibration_w/scale
    coefficients=np.linalg.lstsq(np.column_stack((z**4,z**2,np.ones_like(z))),1/calibration_psd/scale**4,rcond=None)[0]
    a,b,c=coefficients*np.array([1,scale**2,scale**4])
    recovered_w0=c**.25; recovered_gamma=np.sqrt((b+2*recovered_w0**2)/4)
    recovered_f0=recovered_w0/(2*np.pi)
    recovery=dict(frequencies_Hz=calibration_f.tolist(),synthetic_PSD_m2_s=calibration_psd.tolist(),
                  inverse_polynomial_coefficients_SI=[float(a),float(b),float(c)],
                  recovered_f0_Hz=float(recovered_f0),recovered_gamma_per_s=float(recovered_gamma),
                  relative_f0_error=float(abs(recovered_f0-8)/8),relative_gamma_error=float(abs(recovered_gamma-5)/5))
    checks.append(dict(name="calibrated_known_source_recovery",passed=max(recovery["relative_f0_error"],recovery["relative_gamma_error"])<=1e-9))
    fig,axes=plt.subplots(1,2,figsize=(11,4.8),layout="constrained")
    gamma=20; h=response(f,8,gamma)
    sx=abs(h)**2; sv=w*w*sx
    axes[0].plot(f,sx/np.max(sx),label="Displacement PSD / its maximum",color="#3659b8")
    axes[0].plot(f,sv/np.max(sv),label="Velocity PSD / its maximum",color="#bc4b37")
    axes[0].set(title="Same poles; different measured-quantity peaks",xlabel="Frequency (Hz)",ylabel="Normalized PSD (dimensionless)",xlim=(0,16))
    axes[0].text(.04,.53,"f₀ = 8 Hz; γ = 20 s⁻¹\nSeparate amplitude normalization;\npeak locations are unchanged",transform=axes[0].transAxes,fontsize=9)
    axes[1].plot(f,sx1*1e6,label="White acceleration source",color="#3659b8")
    axes[1].plot(f,colored_output*1e6,label="Colored acceleration source",color="#16766c")
    axes[1].set(title="Same mechanical system; different source peaks",xlabel="Frequency (Hz)",ylabel="Displacement PSD (10⁻⁶ m² s)",xlim=(0,16))
    for ax in axes: ax.legend(fontsize=8);ax.grid(alpha=.2)
    for extension in ("svg","png"):
        fig.savefig(ROOT/f"measurement_peaks.{extension}",dpi=170,bbox_inches="tight",
                    metadata={"Date":None} if extension=="svg" else {})
    plt.close(fig)
    result=dict(round=2,status="passed" if all(c["passed"] for c in checks) else "failed",
                model="x''+2 gamma x'+omega0^2 x=d; classical surrogate, not Earth or human",
                f0_Hz=8.,white_source_PSD_m2_per_s3=1.,frequency_grid=dict(min_Hz=0,max_Hz=20,step_Hz=.001,points=20001),
                cases=cases,source_ambiguity=dict(model1={"f0_Hz":8,"gamma_per_s":5},model2={"f0_Hz":10,"gamma_per_s":8},
                    max_relative_output_error=ambiguous_error,source2_min=float(np.min(source2)),source2_max=float(np.max(source2))),
                known_source_recovery=recovery,checks=checks,
                runtime={"numpy":np.__version__},contract_sha256=hashlib.sha256((ROOT/"contract.md").read_bytes()).hexdigest(),
                clarification_sha256=hashlib.sha256((ROOT/"contract-clarification.md").read_bytes()).hexdigest(),
                solver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (ROOT/"results.json").write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
    print(json.dumps(result,indent=2))
    if result["status"]!="passed":raise SystemExit(1)

if __name__=="__main__":run()
