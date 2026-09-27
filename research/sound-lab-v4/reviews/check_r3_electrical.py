"""Independent RLC state-matrix solution and Simpson energy integration.

This does not import the producer's solver or cumulative work states.
"""
from pathlib import Path
import hashlib
import json
import numpy as np
from scipy.integrate import simpson

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent


def propagate(matrix,times,state):
    eigenvalues,basis=np.linalg.eig(matrix)
    coordinates=np.linalg.solve(basis,state)
    return (basis@(np.exp(eigenvalues[:,None]*np.asarray(times)[None,:])*coordinates[:,None])).T


def exact_states(t,L=.01,C=.0001,R=5,omega=1000,peak=1,periods=10):
    matrix=np.array([[0.,1.],[-1/(L*C),-R/L]])
    force=np.array([0.,peak/L])
    z=np.linalg.solve(1j*omega*np.eye(2)-matrix,force)
    switch=periods*2*np.pi/omega
    active=t<=switch
    x=np.empty((len(t),2))
    x[active]=(np.exp(1j*omega*t[active,None])*z-propagate(matrix,t[active],z)).imag
    boundary=(np.exp(1j*omega*switch)*z-propagate(matrix,[switch],z)[0]).imag
    x[~active]=propagate(matrix,t[~active]-switch,boundary).real
    return x,switch,matrix


def main():
    path=ROOT/"R3/baseline-400.csv.gz"
    rows=np.genfromtxt(path,delimiter=",",names=True)
    t=rows["time_s"]
    x,switch,matrix=exact_states(t)
    charge_error=float(np.max(abs(x[:,0]-rows["charge_C"])))
    current_error=float(np.max(abs(x[:,1]-rows["current_A"])))
    assert charge_error<1e-10 and current_error<1e-7
    # Integrate each smooth side separately with another quadrature formula.
    source=np.where(t<=switch,np.sin(1000*t),0.)
    energy=.5*.01*x[:,1]**2+x[:,0]**2/(2*.0001)
    source_work=simpson(source*x[:,1],x=t)
    load=simpson(4*x[:,1]**2,x=t)
    internal=simpson(x[:,1]**2,x=t)
    residual=float(source_work-(energy[-1]-energy[0])-load-internal)
    assert abs(residual)<1e-8
    off=t>=switch-1e-14
    off_load=float(simpson(4*x[off,1]**2,x=t[off]))
    exact_off_load=.8*float(energy[off][0]-energy[-1])
    assert abs(off_load-exact_off_load)<1e-9
    # Source-off charged capacitor: exact released-energy partition at any T.
    discharge=propagate(matrix,t,np.array([.0001,0.])).real
    e_dis=.5*.01*discharge[:,1]**2+discharge[:,0]**2/(2*.0001)
    w_dis=float(simpson(4*discharge[:,1]**2,x=t))
    expected_dis=.8*float(e_dis[0]-e_dis[-1])
    assert abs(w_dis-expected_dis)<1e-9 and w_dis>0
    phasors={}
    for omega,R in [(1000,5),(500,5),(1000,10)]:
        impedance=R+1j*(omega*.01-1/(omega*.0001))
        current=1/impedance
        capacitor=current/(1j*omega*.0001)
        pcap=float(.5*(capacitor*np.conj(current)).real)
        assert abs(pcap)<1e-10
        phasors[f"omega{omega}_R{R}"]={"capacitorVoltageGain":float(abs(capacitor)),
           "capacitorRealPower_W":pcap,"capacitorApparentPower_VA":float(.5*abs(capacitor)*abs(current)),
           "sourceRealPower_W":float(.5*np.conj(current).real),"loadRealPower_W":float(2*abs(current)**2)}
    assert phasors["omega1000_R5"]["capacitorVoltageGain"]>1.5
    assert phasors["omega1000_R10"]["capacitorVoltageGain"]<phasors["omega1000_R5"]["capacitorVoltageGain"]
    result={"method":"Independent exact matrix-eigenfunction states plus Simpson quadrature; no producer solver import.",
      "sourceWaveform":"sin(1000t) V through 10 periods, then zero",
      "maxChargeDifference_C":charge_error,"maxCurrentDifference_A":current_error,
      "sourceWork_J":float(source_work),"loadWork_J":float(load),"internalLoss_J":float(internal),
      "finalStoredEnergy_J":float(energy[-1]),"independentClosureResidual_J":residual,
      "sourceOffLoadWork_J":off_load,"sourceOffExactEnergyPartition_J":exact_off_load,
      "chargedDischargeLoadWork_J":w_dis,"chargedDischargeExactPartition_J":expected_dis,
      "phasors":phasors,"scriptSHA256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      "producerCSV_SHA256":hashlib.sha256(path.read_bytes()).hexdigest()}
    (HERE/"R3-independent-checks.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__=="__main__":main()
