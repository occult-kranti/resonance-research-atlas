# S1A — total response and its ambiguous cause

Synthetic, noiseless digital FIR benchmark. No physical sound was recorded. The direct complex ratio recovers the total transfer and predicts a second independently generated probe. The source and output arrays are linearly convolved with sufficient zero padding; no averaging-based estimator is claimed.

The 5 ms/200 Hz echo parameters belong to the declared fixture. They are recoverable after dividing by the independently declared device FIR, but total response alone cannot assign the feature to the room, device, or material. The explicit alternative puts the entire filter in the device. The r=0 control removes the echo comb. The r=1 control has exact transfer zeros; these are excluded from inverse-H without confusing them with unexcited input bins.

Next missing premise: stability and nonzero sensitivity of the recording chain under noise and placement changes. The low-material protocol will hold phone/speaker geometry fixed and retain reference and movement controls. Numerical success here does not validate a phone, loudspeaker, calibrated pressure measurement, or object.

Sources: Farina 2000, theory pp.2–4 (LTI convolution, time variation, ratio deconvolution); Julius O. Smith, Feedforward Comb Filters (difference equation and delayed-path model). Equations and plots are original implementation, not copied figures.

