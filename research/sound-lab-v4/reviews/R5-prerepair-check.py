"""Independent force-observation inverse and all 65536 error-box vertices."""
from pathlib import Path
import hashlib
import importlib.util
import json
import numpy as np

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent


def main():
    masses=np.array([.005,.015,.025,.035]);M=.1;epsilon=2e-6
    total=masses+M;centered=total-total.mean();weights=centered/(centered@centered)
    signs=np.array([-1.,1.])
    def observations(dg,c=0):
        test=masses[:,None]*(dg+c)-.002+signs[None,:]*.0003+.0002
        stator=np.broadcast_to(M*(dg+c)+.002+.0003,test.shape).copy()
        return test,stator
    test,stator=observations(-.02)
    rival_test,rival_stator=observations(0,-.02)
    rival_error=float(max(np.max(abs(test-rival_test)),np.max(abs(stator-rival_stator))))
    assert rival_error<1e-14
    paired=(test+stator).mean(axis=1)
    inferred=float(weights@paired)
    assert abs(inferred+.02)<1e-12
    identifying=np.column_stack([total,np.ones(4)])
    expanded=np.column_stack([total,np.ones(4),total])
    kernel=np.array([1.,0.,-1.]);single=np.tile([total[0],1.],(4,1));single_kernel=np.array([1.,-total[0]])
    assert np.linalg.matrix_rank(identifying)==2 and np.linalg.matrix_rank(expanded)==2
    assert np.linalg.norm(expanded@kernel)<1e-12 and np.linalg.matrix_rank(single)==1
    assert np.linalg.norm(single@single_kernel)<1e-12
    # Two polarities and two support contrasts per mass: 16 independent
    # bounded errors. No stochastic-independence premise is used.
    ids=np.arange(2**16,dtype=np.uint32)[:,None]
    vertices=2*((ids>>np.arange(16,dtype=np.uint32))&1).astype(float)-1
    coefficients=np.tile(np.repeat(weights/2,2),2)
    slope_errors=epsilon*(vertices@coefficients)
    extrema=[float(slope_errors.min()),float(slope_errors.max())]
    assert np.max(abs(np.array(extrema)-[-.00032,.00032]))<1e-12
    worst=vertices[int(np.argmax(slope_errors))]*epsilon
    spec=importlib.util.spec_from_file_location("producer_r5",ROOT/"R5/run.py")
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    fit=module.fit_paired
    base=fit(masses,test,stator)
    saturated=fit(masses,test+worst[:8].reshape(4,2),stator+worst[8:].reshape(4,2))
    bounded=fit(masses,test,stator,mass_bias_bound_m_per_s2=.03)
    single_result=fit(np.full(4,masses[0]),np.tile(test[0],(4,1)),np.tile(stator[0],(4,1)))
    lost_test=test.copy();lost_test[0,:]=-.1
    lost=fit(masses,lost_test,stator)
    malformed={
       "negative_mass":(np.array([-.005,.015,.025,.035]),test,stator,{}),
       "nonfinite_mass":(np.array([np.nan,.015,.025,.035]),test,stator,{}),
       "negative_error":(masses,test,stator,{"per_contrast_error_N":-epsilon}),
       "nonfinite_error":(masses,test,stator,{"per_contrast_error_N":float("inf")}),
       "negative_bias_bound":(masses,test,stator,{"mass_bias_bound_m_per_s2":-.01}),
       "nonfinite_bias_bound":(masses,test,stator,{"mass_bias_bound_m_per_s2":float("nan")}),
       "malformed_shape":(masses,test[:,:1],stator,{}),
       "nonfinite_force":(masses,test,np.full_like(stator,np.nan),{}),
    }
    rejects={}
    for name,(m,a,b,kwargs) in malformed.items():
        try:value=fit(m,a,b,**kwargs)
        except (ValueError,TypeError) as exc:rejects[name]={"rejected":True,"reason":str(exc)}
        else:rejects[name]={"rejected":False,"returned":value}
    assert all(r["rejected"] for r in rejects.values())
    result={"method":"Independent raw support equations, direct rank/kernel derivation and all65536 bounded-error vertices; producer API separately attacked.",
       "slopeWeights_per_kg":weights.tolist(),"rivalMaxRawObservationDifference_N":rival_error,
       "independentlyInferredSlope_m_per_s2":inferred,
       "identifyingModel":{"domainDimension":2,"rank":2,"nullity":0},
       "expandedModel":{"domainDimension":3,"rank":2,"nullity":1,"kernel":[1,0,-1],"residual":float(np.linalg.norm(expanded@kernel))},
       "singleMassModel":{"domainDimension":2,"rank":1,"nullity":1,"kernel":single_kernel.tolist()},
       "exhaustiveErrorVertices":65536,"slopeErrorExtrema_m_per_s2":extrema,
       "baseAPI":base,"saturatingAPI":saturated,"boundedBiasAPI":bounded,
       "singleMassAPI":single_result,"contactLossAPI":lost,"malformedInputs":rejects,
       "scriptSHA256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE/"R5-independent-checks.json").write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
    print(json.dumps({"rivalError_N":rival_error,"slopeErrorExtrema":extrema,"baseAPI":base,
                      "saturatingAPI":saturated,"contactLossAPI":lost,"singleMassAPI":single_result},indent=2))


if __name__=="__main__":main()
