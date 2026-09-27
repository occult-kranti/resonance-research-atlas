"""Independent coenergy/reaction derivation and sampled-work integration."""
from pathlib import Path
import hashlib
import importlib.util
import json
import numpy as np
from scipy.integrate import simpson

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent


def main():
    p=ROOT/"R4"
    rows=np.genfromtxt(p/"nominal.csv",delimiter=",",names=True)
    t=rows["time_s"];z=rows["position_m"];speed=rows["velocity_m_per_s"]
    I=.2;k=.1;L0=.01;R=5;T=.2
    expected_source=R*I*I*T+I*I*k*(z[-1]-z[0])
    expected_mechanical=.5*I*I*k*(z[-1]-z[0])
    expected_field=expected_mechanical
    source=float(simpson(rows["voltage_V"]*rows["current_A"],x=t))
    mechanical=float(simpson(rows["force_N"]*speed,x=t))
    delta_field=float(rows["magnetic_energy_J"][-1]-rows["magnetic_energy_J"][0])
    closure=source-delta_field-mechanical-R*I*I*T
    assert abs(source-expected_source)<1e-11 and abs(mechanical-expected_mechanical)<1e-11
    assert abs(closure)<1e-11
    # Coenergy depends on the separation of target and stator; this supplies
    # both forces and makes the total magnetic internal force identically zero.
    coenergy=lambda target,stator:.5*I**2*(L0+k*(target-stator))
    h=1e-20
    target_force=float(np.imag(coenergy(.01+1j*h,0))/h)
    stator_force=float(np.imag(coenergy(.01,1j*h))/h)
    assert abs(target_force-.002)<1e-12 and target_force+stator_force==0
    reversed_current=np.genfromtxt(p/"reversed_current.csv",delimiter=",",names=True)
    assert np.array_equal(rows["force_N"],reversed_current["force_N"])
    assert np.max(abs(rows["voltage_V"]+reversed_current["voltage_V"]))<1e-12
    reversed_path=np.genfromtxt(p/"reversed_path.csv",delimiter=",",names=True)
    assert reversed_path["mechanical_work_J"][-1]<0 and np.all(reversed_path["force_N"]>0)
    flux=np.genfromtxt(p/"fixed-flux.csv",delimiter=",",names=True)
    lam=.002
    flux_energy=lambda z:lam**2/(2*(L0+k*z))
    flux_force=-np.imag(flux_energy(flux["position_m"]+1j*h))/h
    flux_force_error=float(np.max(abs(flux_force-flux["force_N"])))
    assert flux_force_error<1e-12
    flux_work=float(simpson(flux["force_N"]*flux["velocity_m_per_s"],x=flux["time_s"]))
    flux_released=float(flux["magnetic_energy_J"][0]-flux["magnetic_energy_J"][-1])
    assert abs(flux_work-flux_released)<1e-11
    # One-pan and complete static support sums differ only in system boundary.
    g=9.80665;test_mass=.001;stator_mass=.1
    test_support=test_mass*g-target_force
    stator_support=stator_mass*g-stator_force
    assembly_support=test_support+stator_support
    assert abs(assembly_support-(test_mass+stator_mass)*g)<1e-14
    spec=importlib.util.spec_from_file_location("producer_r4",p/"run.py")
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    failed_contact=module.static_readout(.02)
    assert failed_contact["indicatedMass_kg"] is None
    assert failed_contact["contactRegime"]=="contact_model_invalid"
    result={"method":"Complex-step independent fixed-current/fixed-flux derivatives, exact endpoint work and Simpson integration; explicit relative-coordinate reaction.",
      "sourceWork_J":source,"exactSourceWork_J":expected_source,
      "mechanicalWork_J":mechanical,"exactMechanicalWork_J":expected_mechanical,
      "magneticEnergyChange_J":delta_field,"exactMagneticEnergyChange_J":expected_field,
      "energyClosureResidual_J":closure,"targetForce_N":target_force,"statorReaction_N":stator_force,
      "netInternalMagneticForce_N":target_force+stator_force,
      "fixedFluxForceMaxError_N":flux_force_error,"fixedFluxWork_J":flux_work,"fixedFluxReleasedEnergy_J":flux_released,
      "testSupport_N":test_support,"statorSupport_N":stator_support,
      "commonScaleSupport_N":assembly_support,"unchangedTotalWeight_N":(test_mass+stator_mass)*g,
      "failedContactControl":failed_contact,
      "reactionLimit":"Static relative-coordinate model with both supports included; omitted external fields, cables, radiated momentum and dynamics still require their own boundary.",
      "scriptSHA256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE/"R4-independent-checks.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__=="__main__":main()
