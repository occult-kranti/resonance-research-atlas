"""Passive electrical resonance with separately quadrature-checked SI energy."""
from pathlib import Path
import gzip
import json
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from common import csv, finish, plt, savefig, writejson
import numpy as np
from scipy.integrate import solve_ivp, cumulative_trapezoid

HERE=Path(__file__).resolve().parent
L_H=.01
C_F=.0001


def simulate(samples_per_period,omega=1000,R_internal=1,R_load=4,source_peak=1,
             initial_voltage=0,initial_current=0):
    parameters=[omega,R_internal,R_load,source_peak,initial_voltage,initial_current]
    if not all(np.isfinite(x) for x in parameters) or omega<=0 or R_internal<0 or R_load<0 or R_internal+R_load<=0:
        raise ValueError("finite parameters, positive frequency and positive passive total resistance required")
    if not isinstance(samples_per_period,(int,np.integer)) or samples_per_period<8:
        raise ValueError("at least eight integer samples per period required")
    period=2*np.pi/omega;off_time=10*period;stop=15*period
    times=np.linspace(0,stop,15*samples_per_period+1);split=10*samples_per_period;times[split]=off_time
    def rhs(t,y,driven):
        voltage=source_peak*np.sin(omega*t) if driven else 0.
        return [y[1],(voltage-(R_internal+R_load)*y[1]-y[0]/C_F)/L_H]
    initial=np.array([C_F*initial_voltage,initial_current],float)
    first=solve_ivp(lambda t,y:rhs(t,y,True),(0,off_time),initial,
                    method="DOP853",t_eval=times[:split+1],rtol=1e-11,atol=[1e-15,1e-12],max_step=period/10)
    second=solve_ivp(lambda t,y:rhs(t,y,False),(off_time,stop),first.y[:,-1],
                     method="DOP853",t_eval=times[split:],rtol=1e-11,atol=[1e-15,1e-12],max_step=period/10)
    if not(first.success and second.success):raise RuntimeError("state integration failed")
    q,current=np.concatenate((first.y,second.y[:,1:]),axis=1)
    source=np.where(times<off_time,source_peak*np.sin(omega*times),0.)
    energy=.5*L_H*current**2+q**2/(2*C_F)
    work=cumulative_trapezoid(source*current,times,initial=0.)
    load=cumulative_trapezoid(R_load*current**2,times,initial=0.)
    loss=cumulative_trapezoid(R_internal*current**2,times,initial=0.)
    residual=work-(energy-energy[0])-load-loss
    scale=max(float(np.max(np.abs(work))),float(np.max(energy)),float(load[-1]+loss[-1]),1e-12)
    late=(times>=8*period)&(times<=off_time)
    gain=None if source_peak==0 else float(np.max(np.abs(q[late]/C_F))/abs(source_peak))
    return {"time_s":times,"charge_C":q,"current_A":current,"source_V":source,
            "capacitor_V":q/C_F,"energy_J":energy,"source_work_J":work,
            "load_work_J":load,"internal_loss_J":loss,"closure_residual_J":residual,
            "offIndex":split,"omega_rad_per_s":omega,"voltageGain":gain,
            "maxClosureResidual_J":float(np.max(np.abs(residual))),
            "normalizedMaxResidual":float(np.max(np.abs(residual))/scale),
            "normalizationScale_J":scale,"totalResistance_ohm":R_internal+R_load,
            "R_load_ohm":R_load,"R_internal_ohm":R_internal}


def phasor(omega=1000,R_internal=1,R_load=4,source_peak=1):
    z=R_internal+R_load+1j*(omega*L_H-1/(omega*C_F))
    current=source_peak/z;capacitor=current/(1j*omega*C_F)
    return {"currentPeak_A":float(abs(current)),"capacitorPeak_V":float(abs(capacitor)),
            "voltageGain":float(abs(capacitor)/abs(source_peak)),
            "sourceMeanPower_W":float(.5*np.real(source_peak*np.conj(current))),
            "loadMeanPower_W":float(.5*R_load*abs(current)**2),
            "internalMeanPower_W":float(.5*R_internal*abs(current)**2),
            "capacitorMeanRealPower_W":float(.5*np.real(capacitor*np.conj(current))),
            "capacitorReactivePower_var":float(.5*np.imag(capacitor*np.conj(current))),
            "capacitorApparentPower_VA":float(.5*abs(capacitor)*abs(current))}


def export(name,result):
    columns=["time_s","charge_C","current_A","source_V","capacitor_V","energy_J","source_work_J","load_work_J","internal_loss_J","closure_residual_J"]
    path=HERE/(name+".csv")
    csv(path,columns,np.column_stack([result[k] for k in columns]))
    compressed=path.with_suffix(".csv.gz")
    with compressed.open("wb") as out:
        with gzip.GzipFile(filename="",mode="wb",fileobj=out,mtime=0) as stream:stream.write(path.read_bytes())
    path.unlink();return compressed.name


def summary(result):
    off=result["offIndex"]
    return {"omega_rad_per_s":result["omega_rad_per_s"],"voltageGain":result["voltageGain"],
            "initialEnergy_J":float(result["energy_J"][0]),"finalEnergy_J":float(result["energy_J"][-1]),
            "sourceWork_J":float(result["source_work_J"][-1]),"loadWork_J":float(result["load_work_J"][-1]),
            "internalLoss_J":float(result["internal_loss_J"][-1]),"maxClosureResidual_J":result["maxClosureResidual_J"],
            "normalizedMaxResidual":result["normalizedMaxResidual"],"normalizationScale_J":result["normalizationScale_J"],
            "sourceOffStoredEnergy_J":float(result["energy_J"][off]),
            "sourceOffLoadWork_J":float(result["load_work_J"][-1]-result["load_work_J"][off]),
            "sourceOffInternalLoss_J":float(result["internal_loss_J"][-1]-result["internal_loss_J"][off]),
            "R_internal_ohm":result["R_internal_ohm"],"R_load_ohm":result["R_load_ohm"]}


def main():
    contract=json.loads((HERE/"contract.json").read_text())
    resolutions=contract["model"]["timeResolution_samples_per_period"]
    refinements=[simulate(n) for n in resolutions];fine=refinements[-1]
    discharge=simulate(400,source_peak=0,initial_voltage=1)
    zero=simulate(400,source_peak=0)
    off_resonance=simulate(400,omega=500)
    stronger=simulate(400,R_internal=6,R_load=4)
    phasors={"resonant":phasor(),"off_resonance":phasor(omega=500),"stronger_resistance":phasor(R_internal=6,R_load=4)}
    cases={"baseline":summary(fine),"initially_charged_source_off":summary(discharge),"zero":summary(zero),"off_resonance":summary(off_resonance),"stronger_resistance":summary(stronger)}
    off=fine["offIndex"]
    tail_load=fine["load_work_J"][-1]-fine["load_work_J"][off]
    tail_loss=fine["internal_loss_J"][-1]-fine["internal_loss_J"][off]
    tail_source=fine["source_work_J"][-1]-fine["source_work_J"][off]
    tail_delta=fine["energy_J"][-1]-fine["energy_J"][off]
    metrics={"resonantVoltageGain":fine["voltageGain"],"offResonanceVoltageGain":off_resonance["voltageGain"],
             "strongerResistanceVoltageGain":stronger["voltageGain"],
             "finestMaxEnergyResidual_J":fine["maxClosureResidual_J"],"finestNormalizedResidual":fine["normalizedMaxResidual"],
             "coarsestMaxEnergyResidual_J":refinements[0]["maxClosureResidual_J"],
             "sourceWork_J":float(fine["source_work_J"][-1]),"loadWork_J":float(fine["load_work_J"][-1]),
             "internalLoss_J":float(fine["internal_loss_J"][-1]),"finalStoredEnergy_J":float(fine["energy_J"][-1]),
             "sourceOffLoadWork_J":float(tail_load),"sourceOffStoredEnergyReleased_J":float(-tail_delta),
             "wrongOmittedStorageSurplus_J":float(tail_load+tail_loss-tail_source),
             "correctSourceOffClosure_J":float(tail_source-tail_delta-tail_load-tail_loss),
             "chargedDischargeLoadWork_J":float(discharge["load_work_J"][-1]),
             "chargedDischargeInputWork_J":float(discharge["source_work_J"][-1]),
             "capacitorMeanRealPower_W":phasors["resonant"]["capacitorMeanRealPower_W"],
             "capacitorApparentPower_VA":phasors["resonant"]["capacitorApparentPower_VA"],
             "zeroStateMaxAbs":float(max(np.max(np.abs(zero["charge_C"])),np.max(np.abs(zero["current_A"]))))}
    checks={"energyClosure":metrics["finestNormalizedResidual"]<=.0005,
            "quadratureRefinement":metrics["finestMaxEnergyResidual_J"]<metrics["coarsestMaxEnergyResidual_J"] or metrics["coarsestMaxEnergyResidual_J"]<1e-10,
            "voltageGain":metrics["resonantVoltageGain"]>1.5,
            "capacitorRealPowerZero":abs(metrics["capacitorMeanRealPower_W"])<=1e-10,
            "reactiveVANotRealWatts":metrics["capacitorApparentPower_VA"]>0,
            "zeroState":metrics["zeroStateMaxAbs"]<=1e-12,
            "dischargeFromInitialStorage":metrics["chargedDischargeInputWork_J"]==0 and metrics["chargedDischargeLoadWork_J"]>0,
            "strongerResistanceReducesGain":metrics["strongerResistanceVoltageGain"]<metrics["resonantVoltageGain"],
            "sourceOffPositiveLoad":metrics["sourceOffLoadWork_J"]>0,
            "passiveLoadLoss":all(np.min(np.diff(r[k]))>=-1e-15 for r in refinements for k in ["load_work_J","internal_loss_J"])}
    files=[export(f"baseline-{n}",r) for n,r in zip(resolutions,refinements)]
    for name,r in [("charged-discharge",discharge),("zero",zero),("off-resonance",off_resonance),("stronger-resistance",stronger)]:files.append(export(name,r))
    convergence=[[n,r["maxClosureResidual_J"],r["normalizedMaxResidual"],r["voltageGain"]] for n,r in zip(resolutions,refinements)]
    csv(HERE/"convergence.csv",["samples_per_period","max_residual_J","normalized_max_residual","voltage_gain"],convergence)
    writejson(HERE/"case-results.json",cases);writejson(HERE/"phasors.json",phasors)
    fig,axes=plt.subplots(2,2,figsize=(11,7))
    ms=fine["time_s"]*1000
    axes[0,0].plot(ms,fine["source_V"],label="Source voltage")
    axes[0,0].plot(ms,fine["capacitor_V"],label="Capacitor voltage")
    axes[0,0].set(xlabel="Time (ms)",ylabel="Voltage (V)",title="Voltage amplification, with supplied energy");axes[0,0].legend(fontsize=8)
    for name,label in [("source_work_J","Signed source work"),("load_work_J","Load work"),("internal_loss_J","Internal loss"),("energy_J","Stored energy")]:
        axes[0,1].plot(ms,1000*fine[name],label=label)
    axes[0,1].axvline(ms[off],ls="--",color="black",lw=1);axes[0,1].set(xlabel="Time (ms)",ylabel="Energy (mJ)",title="Switch-off releases previously stored energy");axes[0,1].legend(fontsize=8)
    axes[1,0].plot(ms,1e9*fine["closure_residual_J"])
    axes[1,0].set(xlabel="Time (ms)",ylabel="Closure residual (nJ)",title="Independent sampled-power quadrature")
    axes[1,1].loglog(resolutions,[r["maxClosureResidual_J"] for r in refinements],marker="o")
    axes[1,1].set(xlabel="Samples per drive period",ylabel="Maximum closure residual (J)",title="Quadrature error shrinks with refinement")
    savefig(fig,HERE/"figure.svg")
    report="""# R3 — electrical voltage gain and complete energy boundaries

This is a synthetic lumped circuit in SI units. Source voltage is u(t)=1 V sin(1000 t) for ten drive periods, starting at zero phase, then zero for five periods. A series .01 H inductor, .0001 F capacitor, 1 ohm internal resistor and 4 ohm load obey dq/dt=I and L dI/dt=u−(R_internal+R_load)I−q/C. The state solver integrates only q and I, with a separate solve beginning at the exact source-off boundary. Independent trapezoidal integration of sampled powers computes signed source work, load work and internal loss. No work variable is integrated as part of the state used to establish closure.

Stored energy is E=L I²/2+q²/(2C). Differentiation gives dE/dt=uI−R_internal I²−R_load I², hence W_source=E_final−E_initial+W_internal+W_load. The reported residual is the maximum absolute budget mismatch over the sampled trajectory, normalized by max(max|W_source|, max E, final total dissipation, 10⁻¹² J). Numerical closure is a finite-run check, not an interval proof or physical calibration.

At steady-state resonance the ideal capacitor voltage amplitude is twice the 1 V source amplitude. Its mean real power is zero even though its apparent power V_rms I_rms is positive; reactive VA must not be treated as watts. Steady phasor values in phasors.json are distinguished from the startup transient. The off-resonance control uses omega=500 rad/s with its own drive-period duration. The stronger-resistance control holds the 4 ohm load fixed and raises internal resistance to 6 ohm, total 10 ohm.

After switching off, positive load work is supplied by the stored magnetic/electric energy present at that boundary. Intentionally omitting that initial storage creates the saved false-surplus quantity. A separate initially charged capacitor starts at 1 V with zero source voltage: positive output again comes from initial storage. Zero source plus zero initial state stays zero. These are accounting counterexamples, not newly discovered conservation laws or evidence of overunity or altered gravity.

Run: `python research/sound-lab-v4/R3/run.py`. Compressed CSV files retain every sampled state, source voltage, energy, and independently quadrature-derived work. Gzip timestamps are fixed for exact reproduction. The model omits component nonlinearities, parasitics, heating-dependent parameters and electromagnetic radiation. No hardware build, high-voltage apparatus or calibration is represented.
"""
    finish(HERE,metrics,"The capacitor approaches twice the source voltage while signed input work closes the energy budget; source-off load work is released storage, and reactive VA is not real power.",[{"control":"omit source-off initial storage","outcome":"false positive surplus retained"},{"control":"capacitor apparent power as watts","outcome":"positive VA but zero mean real power"},{"control":"initially charged source-off circuit","outcome":"load work supplied by initial capacitor energy"}],report,files+["convergence.csv","case-results.json","phasors.json","figure.svg"],checks,extra={"evidenceType":"synthetic_SI_circuit_simulation","domain":"electricity_and_magnetic_storage"})


if __name__=="__main__":main()
