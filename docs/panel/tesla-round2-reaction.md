# Tesla lens reaction to the selected second round

Date: 2026-09-26. Read: panel/advisor-round2.md. This is a contract critique, not an independent numerical rerun.

Round 1 established energy closure in a specified passive finite system, while leaving its measurement map unspecified. The selected within-mode displacement/velocity test directly addresses that limitation. It is stronger than switching which of two distant modes dominates a mixed spectrum.

## Mandatory mathematical distinctions

For gamma>0 and omega0>0, define D(omega)=(omega0^2-omega^2)^2+4 gamma^2 omega^2. With constant input PSD, displacement power is proportional to 1/D and velocity power to omega^2/D.

The displacement maximum is at sqrt(omega0^2-2 gamma^2) only when omega0^2>2 gamma^2. Otherwise the maximum on omega>=0 is at zero. Equality belongs to the zero-maximum branch. A finite search grid must include the endpoint zero.

The velocity maximum is at omega0: with z=omega^2, differentiating z/[z^2+(4 gamma^2-2 omega0^2)z+omega0^4] gives a numerator omega0^4-z^2. Thus the maximum remains at z=omega0^2 irrespective of positive damping. This is a direct calculation, not a new physical result.

The poles are -gamma +/- sqrt(gamma^2-omega0^2). Only the underdamped branch has a nonzero imaginary pole component. At critical or overdamping there is no oscillation frequency equal to that imaginary component. Avoid calling omega0 a measured free-decay oscillation rate in those branches.

## Strongest possible criticism and required repair

A power peak alone can be ambiguous; a calibrated complex transfer function need not be. For the normalized equation, a known nonzero-frequency complex response supplies Re[H^-1]=omega0^2-omega^2 and Im[H^-1]=2 gamma omega. Subject to calibrated units and nonzero excitation this gives a positive identification control. Unknown source-power compensation shows nonuniqueness only in the declared uncalibrated observation model.

Displacement PSD and velocity PSD have different dimensions. Normalize each to its own maximum solely for plotting peak locations and label that choice. Do not interpret their numerical heights as comparable power or efficiency. State whether PSD uses Hz or angular frequency; the spectral-density Jacobian matters even though mapped peak locations agree.

Ideal white forcing is a mathematical input model, not a finite-band physical exposure or an Earth/brain simulator. No biological endpoint follows from this control.

## Source boundaries

The 2026 Annales Geophysicae paper supports the qualitative distinction between forced maxima and cavity eigenvalues; its ambiguous HTML calibration equation is unnecessary here. Keep the ideal Earth-shell equation on a separate card with its boundary assumptions and source ID SR-2011. A chosen display frequency near an Earth peak supplies no physical identification map.

Recommendation: admit the proposed target if these branch, calibration and unit controls are frozen before execution. Report the outcome as a within-model measurement limitation, not discovery of hidden energy or failure of all spectroscopy.

