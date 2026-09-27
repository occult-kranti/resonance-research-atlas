"""Prescribed-path linear magnetic actuator with explicit source boundary."""
from pathlib import Path
import json
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from common import csv, finish, plt, savefig, writejson
import numpy as np
from scipy.integrate import cumulative_trapezoid

HERE=Path(__file__).resolve().parent


def path_values(samples=401,gradient=.1,z_start=0,z_stop=.02,duration=.2,L0=.01):
    if not isinstance(samples,(int,np.integer)) or samples<3:
        raise ValueError("at least three integer time samples required")
    if not all(np.isfinite(x) for x in [gradient,z_start,z_stop,duration,L0]) or duration<=0:
        raise ValueError("finite geometry and positive duration required")
    t=np.linspace(0,duration,samples)
    z=z_start+(z_stop-z_start)*(1-np.cos(np.pi*t/duration))/2
    speed=(z_stop-z_start)*np.pi*np.sin(np.pi*t/duration)/(2*duration)
    inductance=L0+gradient*z
    if np.any(inductance<=0):raise ValueError("positive inductance required throughout declared path")
    return t,z,speed,inductance


def maintained_current(samples=401,current=.2,gradient=.1,z_start=0,z_stop=.02,duration=.2,resistance=5,L0=.01):
    if not np.isfinite(current) or not np.isfinite(resistance) or resistance<0:
        raise ValueError("finite current and nonnegative resistance required")
    t,z,speed,inductance=path_values(samples,gradient,z_start,z_stop,duration,L0)
    force=np.full_like(t,.5*current**2*gradient)
    voltage=resistance*current+current*gradient*speed
    energy=.5*inductance*current**2
    source=cumulative_trapezoid(voltage*current,t,initial=0)
    mechanical=cumulative_trapezoid(force*speed,t,initial=0)
    heat=resistance*current**2*t
    closure=source-(energy-energy[0])-mechanical-heat
    deltaL=gradient*(z_stop-z_start)
    exact={"delta_magnetic_energy_J":.5*current**2*deltaL,
           "mechanical_work_J":.5*current**2*deltaL,
           "joule_loss_J":resistance*current**2*duration,
           "source_work_J":resistance*current**2*duration+current**2*deltaL}
    return {"time_s":t,"position_m":z,"velocity_m_per_s":speed,"inductance_H":inductance,
            "current_A":np.full_like(t,current),"voltage_V":voltage,"force_N":force,
            "magnetic_energy_J":energy,"source_work_J":source,"mechanical_work_J":mechanical,
            "joule_loss_J":heat,"closure_residual_J":closure,"exact":exact}


def fixed_flux(samples=401,flux_linkage=.002,gradient=.1,z_start=0,z_stop=.02,duration=.2,L0=.01):
    if not np.isfinite(flux_linkage):raise ValueError("finite fixed flux linkage required")
    t,z,speed,inductance=path_values(samples,gradient,z_start,z_stop,duration,L0)
    current=flux_linkage/inductance
    force=.5*flux_linkage**2*gradient/inductance**2
    energy=.5*flux_linkage**2/inductance
    mechanical=cumulative_trapezoid(force*speed,t,initial=0)
    return {"time_s":t,"position_m":z,"velocity_m_per_s":speed,"inductance_H":inductance,
            "current_A":current,"force_N":force,"magnetic_energy_J":energy,
            "mechanical_work_J":mechanical,"closure_residual_J":-(energy-energy[0])-mechanical,
            "flux_linkage_Wb_turn":flux_linkage,"source_work_J":0.,"joule_loss_J":0.}


def static_readout(force_N,mass_kg=.001,g_m_per_s2=9.80665):
    if not all(np.isfinite(x) for x in [force_N,mass_kg,g_m_per_s2]) or mass_kg<=0 or g_m_per_s2<=0:
        raise ValueError("finite force, positive mass and calibrated gravity required")
    normal=mass_kg*g_m_per_s2-force_N
    return {"gravitationalAcceleration_m_per_s2":g_m_per_s2,"trueMass_kg":mass_kg,
            "upwardMagneticForce_N":force_N,"normalForce_N":normal,
            "contactRegime":"supported_contact" if normal>=0 else "contact_model_invalid",
            "indicatedMass_kg":normal/g_m_per_s2 if normal>=0 else None}


def summarize(r):
    value={k:float(r[k][-1]) for k in ["magnetic_energy_J","source_work_J","mechanical_work_J","joule_loss_J"]}
    value["delta_magnetic_energy_J"]=float(r["magnetic_energy_J"][-1]-r["magnetic_energy_J"][0])
    value["maxClosureResidual_J"]=float(np.max(np.abs(r["closure_residual_J"])))
    value["force_N"]=float(r["force_N"][0]);value["minimumInductance_H"]=float(np.min(r["inductance_H"]))
    value["exact"]=r["exact"]
    value["maxClosedFormTermError_J"]=max(abs(value[k]-v) for k,v in r["exact"].items())
    return value


def main():
    contract=json.loads((HERE/"contract.json").read_text());m=contract["model"]
    samples=m["timeSamples"];runs=[maintained_current(n) for n in samples];fine=runs[-1]
    cases={"nominal":fine,"reversed_current":maintained_current(current=-.2),
           "zero_current":maintained_current(current=0),"zero_gradient":maintained_current(gradient=0),
           "reversed_path":maintained_current(z_start=.02,z_stop=0)}
    summarized={name:summarize(r) for name,r in cases.items()}
    flux_runs=[fixed_flux(n) for n in samples];flux=flux_runs[-1]
    zmid=.01;step=1e-6
    coenergy=lambda z:.5*(m["L0_H"]+m["Lgradient_H_per_m"]*z)*m["current_A"]**2
    derivative=(coenergy(zmid+step)-coenergy(zmid-step))/(2*step)
    fixed_flux_energy=lambda z:.002**2/(2*(m["L0_H"]+m["Lgradient_H_per_m"]*z))
    flux_derivative=-(fixed_flux_energy(zmid+step)-fixed_flux_energy(zmid-step))/(2*step)
    flux_force_mid=.5*.002**2*m["Lgradient_H_per_m"]/(m["L0_H"]+m["Lgradient_H_per_m"]*zmid)**2
    readout=static_readout(float(fine["force_N"][0]));reversed_readout=static_readout(float(cases["reversed_current"]["force_N"][0]))
    wrong_force=-derivative
    wrong_mechanical=wrong_force*(m["pathStop_m"]-m["pathStart_m"])
    wrong_closure=fine["source_work_J"][-1]-(fine["magnetic_energy_J"][-1]-fine["magnetic_energy_J"][0])-wrong_mechanical-fine["joule_loss_J"][-1]
    metrics={"upwardForce_N":float(fine["force_N"][0]),"sourceWork_J":float(fine["source_work_J"][-1]),
             "fieldEnergyIncrease_J":float(fine["magnetic_energy_J"][-1]-fine["magnetic_energy_J"][0]),
             "mechanicalWork_J":float(fine["mechanical_work_J"][-1]),"jouleLoss_J":float(fine["joule_loss_J"][-1]),
             "finestMaxClosureResidual_J":summarized["nominal"]["maxClosureResidual_J"],
             "coarsestMaxClosureResidual_J":summarize(runs[0])["maxClosureResidual_J"],
             "finestClosedFormTermError_J":summarized["nominal"]["maxClosedFormTermError_J"],
             "forceCoenergyDerivativeError_N":abs(derivative-fine["force_N"][0]),
             "currentReversalForceDifference_N":float(np.max(np.abs(fine["force_N"]-cases["reversed_current"]["force_N"]))),
             "wrongFixedCurrentForce_N":float(wrong_force),"wrongForceBudgetResidual_J":float(wrong_closure),
             "fixedFluxMechanicalWork_J":float(flux["mechanical_work_J"][-1]),
             "fixedFluxFieldEnergyChange_J":float(flux["magnetic_energy_J"][-1]-flux["magnetic_energy_J"][0]),
             "fixedFluxMaxClosureResidual_J":float(np.max(np.abs(flux["closure_residual_J"]))),
             "fixedFluxForceDerivativeError_N":abs(flux_derivative-flux_force_mid),
             "normalForce_N":readout["normalForce_N"],"indicatedMass_kg":readout["indicatedMass_kg"],
             "unchangedGravity_m_per_s2":readout["gravitationalAcceleration_m_per_s2"]}
    checks={"energyClosure":metrics["finestMaxClosureResidual_J"]<=1e-8,
            "closedFormTerms":metrics["finestClosedFormTermError_J"]<=1e-8,
            "coenergyDerivative":metrics["forceCoenergyDerivativeError_N"]<=1e-10,
            "currentReversal":metrics["currentReversalForceDifference_N"]<=1e-12,
            "zeroCurrentForce":np.max(np.abs(cases["zero_current"]["force_N"]))<=1e-12,
            "zeroGradientForce":np.max(np.abs(cases["zero_gradient"]["force_N"]))<=1e-12,
            "positiveInductance":all(np.min(r["inductance_H"])>0 for r in cases.values()),
            "refinement":metrics["finestMaxClosureResidual_J"]<metrics["coarsestMaxClosureResidual_J"],
            "reversePathWorkSign":cases["reversed_path"]["mechanical_work_J"][-1]<0,
            "fixedFluxBudget":metrics["fixedFluxMaxClosureResidual_J"]<=1e-8,
            "fixedFluxDerivative":metrics["fixedFluxForceDerivativeError_N"]<=1e-10,
            "gravityUnchangedContactPositive":readout["gravitationalAcceleration_m_per_s2"]==9.80665 and readout["normalForce_N"]>0,
            "wrongSignFailureRetained":abs(metrics["wrongForceBudgetResidual_J"])>1e-6}
    checks={k:bool(v) for k,v in checks.items()}
    files=[];columns=["time_s","position_m","velocity_m_per_s","inductance_H","current_A","voltage_V","force_N","magnetic_energy_J","source_work_J","mechanical_work_J","joule_loss_J","closure_residual_J"]
    for name,r in cases.items():
        csv(HERE/(name+".csv"),columns,np.column_stack([r[k] for k in columns]));files.append(name+".csv")
    flux_columns=["time_s","position_m","velocity_m_per_s","inductance_H","current_A","force_N","magnetic_energy_J","mechanical_work_J","closure_residual_J"]
    csv(HERE/"fixed-flux.csv",flux_columns,np.column_stack([flux[k] for k in flux_columns]))
    csv(HERE/"convergence.csv",["time_samples","max_residual_J","max_term_error_J","fixed_flux_max_residual_J"],[[n,summarize(r)["maxClosureResidual_J"],summarize(r)["maxClosedFormTermError_J"],np.max(np.abs(f["closure_residual_J"]))] for n,r,f in zip(samples,runs,flux_runs)])
    writejson(HERE/"case-results.json",summarized);writejson(HERE/"readout.json",{"nominal":readout,"reversed_current":reversed_readout,"interpretation":"External upward support changes the normal force with g fixed; external support/reaction boundary remains to be tested."})
    fig,axes=plt.subplots(2,2,figsize=(11,7))
    for key,label in [("source_work_J","Source work minus Joule heat"),("magnetic_energy_J","Field energy increase"),("mechanical_work_J","Mechanical work")]:
        values=fine[key].copy()
        if key=="source_work_J":values-=fine["joule_loss_J"]
        elif key=="magnetic_energy_J":values-=values[0]
        axes[0,0].plot(fine["time_s"],values*1e6,label=label)
    axes[0,0].set(xlabel="Time (s)",ylabel="Energy (µJ)",title="Maintained current: source supplies field and motion");axes[0,0].legend(fontsize=8)
    axes[0,1].plot(fine["position_m"]*1000,fine["force_N"]*1000,label="Maintained current")
    axes[0,1].plot(flux["position_m"]*1000,flux["force_N"]*1000,label="Fixed flux, zero loss")
    axes[0,1].set(xlabel="Prescribed position (mm)",ylabel="Upward force (mN)",title="Different electrical boundaries");axes[0,1].legend(fontsize=8)
    axes[1,0].bar(["No magnetic force","+0.2 A","−0.2 A"],[1,1000*readout["indicatedMass_kg"],1000*reversed_readout["indicatedMass_kg"]],color=["#717985","#286c80","#286c80"])
    axes[1,0].set(ylabel="Static indicated mass (g)",title="Even-in-current support leaves gravity unchanged")
    axes[1,1].loglog(samples,[summarize(r)["maxClosureResidual_J"] for r in runs],marker="o",label="Maintained current")
    axes[1,1].loglog(samples,[np.max(np.abs(f["closure_residual_J"])) for f in flux_runs],marker="s",label="Fixed flux")
    axes[1,1].set(xlabel="Time samples",ylabel="Maximum closure residual (J)",title="Independent endpoint energy comparison");axes[1,1].legend(fontsize=8)
    savefig(fig,HERE/"figure.svg")
    report="""# R4 — magnetic force, source work, and balance boundaries

The finite model assumes L(z)=.01 H+(.1 H/m)z for 0≤z≤.02 m, where positive z is upward and increases inductance. A half-cosine path completes this motion in .2 s with zero endpoint velocities. The path is prescribed by an external motion controller, not predicted by free mechanical dynamics. Maintained current is .2 A through a 5 ohm resistance. No measured coil or claimed achievable geometry supplies this L(z).

Flux linkage is lambda=L(z)I. At fixed current, v=RI+d(lambda)/dt=RI+I L'(z) z_dot. Electrical power is RI²+I²L' z_dot. Field-energy rate is half the motion term, dU/dt=I² L' z_dot/2; the remaining half is mechanical power. Therefore Fz=+I² L'/2 and W_source=Delta U+W_mechanical+W_Joule. The sign equals the fixed-current coenergy derivative. Taking minus the field-energy gradient while silently holding current fixed omits source work and gives the opposite force; that wrong model and its failed budget are retained.

Trapezoidal source and force-power integrals are separately checked against endpoint formulas: Delta U=W_mechanical=I² Delta L/2, W_source=RI²T+I²Delta L. Refinement checks quantify their finite quadrature error. Reversing current changes voltage sign but leaves force and energy unchanged. Reversing the prescribed path keeps force upward while reversing field change and mechanical work. Zero current and zero gradient give zero magnetic force.

The auxiliary lossless fixed-flux case is a different electrical boundary: R=0, lambda=.002 Wb-turn constant, I=lambda/L(z), U=lambda²/(2L). Here Fz=−partial U/partial z at fixed lambda=+lambda²L'/(2L²), W_source=0, and W_mechanical=−Delta U. It is an ideal comparison, not a household persistent-current apparatus.

For a separate static 1 g test mass, N=mg−Fz with g=9.80665 m/s². Contact remains positive. The lower indicated mass N/g and its even-in-current symmetry occur with unchanged g. This readout assumes the magnetic reaction is supported externally; the total apparatus boundary is not yet resolved. The moving electromagnetic subsystem delivers F dz to its mechanical boundary; it does not solve the motion controller, total apparatus mechanics, or gravitational potential changes of a moved test mass.

Run: `python research/sound-lab-v4/R4/run.py`. This is a conditional classical actuator and support-force calculation, not a gravity modification or a physical experiment. Current reversal alone does not remove an ordinary quadratic magnetic force.
"""
    finish(HERE,metrics,"A 2 mN upward magnetic force reduces a 1 g pan indication with unchanged gravity; maintained-current source work supplies both field-energy increase and mechanical work.",[{"control":"minus fixed-current field gradient","outcome":"wrong force sign and failed source-inclusive budget"},{"control":"current reversal","outcome":"ordinary support survives because force depends on I²"},{"control":"prescribed path","outcome":"motion is input, not a free-levitation prediction"}],report,files+["fixed-flux.csv","convergence.csv","case-results.json","readout.json","figure.svg"],checks,extra={"evidenceType":"synthetic_SI_electromechanical_model","domain":"magnetism_and_electromechanics"})


if __name__=="__main__":main()
