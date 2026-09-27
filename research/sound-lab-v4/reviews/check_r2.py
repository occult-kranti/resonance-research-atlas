"""Independent exhaustive-corner check and adversarial R2 API admission."""
from pathlib import Path
import hashlib
import importlib.util
import itertools
import json
import numpy as np

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent


def main():
    spec=importlib.util.spec_from_file_location("producer_r2", ROOT/"R2/run.py")
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    interval=module.slope_interval
    t=np.array([0.,.15,.4,1.])
    a=.2*np.exp(-2*t)
    b=.05*np.exp(2*t)
    delta=np.array([.0001,.0002,.0003,.0001])
    # Separate formula: regression slope numerator is cov(t, log(b/a)).
    # Exhaustively evaluate all 256 original-amplitude box vertices.
    corners=[]
    for bits in itertools.product([-1,1],repeat=8):
        target=a+delta*np.array(bits[:4])
        reference=b+delta*np.array(bits[4:])
        logratio=np.log(reference/target)
        slope=sum((t-t.mean())*(logratio-logratio.mean()))/sum((t-t.mean())**2)
        corners.append(float(slope))
    brute=[min(corners),max(corners)]
    observed=interval(t,a,b,delta,.25,.4)
    reported=observed["contrast_interval_per_s"]
    discrepancy=float(np.max(np.abs(np.array(brute)-reported)))
    assert discrepancy<1e-10
    physical=observed["physical_alpha_interval_per_s"]
    width_increase=float((physical[1]-physical[0])-(reported[1]-reported[0]))
    assert abs(width_increase-1.3)<1e-10
    tests={}
    malformed={
        "negative_error": (t,a,b,-.1,.25,.4),
        "nan_error": (t,a,b,float("nan"),.25,.4),
        "infinite_error": (t,a,b,float("inf"),.25,.4),
        "error_shape": (t,a,b,[.01,.02],.25,.4),
        "target_shape": (t,a[:-1],b,delta,.25,.4),
        "reference_shape": (t,a,b[:-1],delta,.25,.4),
        "constant_times": (np.zeros(4),a,b,delta,.25,.4),
        "duplicate_times": (np.array([0.,.1,.1,1.]),a,b,delta,.25,.4),
        "nonfinite_times": (np.array([0.,.1,np.nan,1.]),a,b,delta,.25,.4),
        "negative_reference_budget": (t,a,b,delta,-.25,.4),
        "nan_reference_budget": (t,a,b,delta,float("nan"),.4),
        "infinite_differential_budget": (t,a,b,delta,.25,float("inf")),
        "nonfinite_target": (t,np.array([.1,.2,.3,np.nan]),b,delta,.25,.4),
    }
    for name,args in malformed.items():
        try:
            value=interval(*args)
        except (ValueError,TypeError) as exc:
            tests[name]={"rejected":True,"reason":str(exc)}
        else:
            tests[name]={"rejected":False,"returned":value}
    assert all(row["rejected"] for row in tests.values()), tests
    missing=interval(t,a,b,delta,None,.4)
    assert missing["physical_alpha_interval_per_s"] is None
    assert missing["contrast_interval_per_s"] is not None
    floor_a=a.copy(); floor_a[1]=delta[1]
    floor=interval(t,floor_a,b,delta,.25,.4)
    assert floor["contrast_interval_per_s"] is None
    zero=interval(t,a,np.zeros(4),delta,.25,.4)
    assert zero["contrast_interval_per_s"] is None
    result={"method":"All 256 box corners independently evaluated from covariance regression; API guards attacked separately.",
            "bruteForceInterval_per_s":brute,"reportedInterval_per_s":reported,
            "maximumEndpointDiscrepancy_per_s":discrepancy,"physicalWidthIncrease_per_s":width_increase,
            "malformedInputChecks":tests,"unknownBound":missing,"floor":floor,"zeroReference":zero,
            "scriptSHA256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE/"R2-independent-checks.json").write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    main()
