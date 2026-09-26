# Round 2 admission and Round 3 decision

The Round 2 producer completed the selected measurement-map experiment. Independent review read the complete source and rebuilt the spectra directly as rational functions, without importing the producer module.

The displacement spectrum agrees with the separately computed denominator to relative error below 9.28×10⁻16. The compensating-source ratio agrees within 1.27×10⁻15. A separate three-point polynomial inverse, leaving two frequencies out, recovers f0=8 Hz and gamma=5 s^-1 and predicts held-out spectra within 9.68×10⁻16 relative error. Results and hashes are in `research/round2/independent-review.json`.

For D(ω)=(ω0²−ω²)²+4γ²ω², the derivative signs provide a completeness check on peak selection:

- dSx/dω=−4ω(ω²+2γ²−ω0²)/D², so the positive displacement maximum exists only below gamma=omega0/sqrt(2); otherwise it lies at zero.
- dSv/dω=2ω(ω0⁴−ω⁴)/D², so the velocity maximum is at omega0 for gamma>0.

The tested same-oscillator example at gamma=20 s^-1 has displacement and velocity peaks at approximately 6.6133 Hz and 8 Hz. Changing only the source spectrum also shifts the displayed maximum. With an unknown source, different poles can generate the same output spectrum through a compensating input; with the calibrated white source, parameter recovery succeeds. The result is an explicit conditional inverse ambiguity, not a theorem that every spectrum is unknowable.

## Repair provenance

The original first production run passed its nine checks. The advisor then noticed that a real two-sided source PSD needed an even extension of its positive-frequency Gaussian bump. The producer retained the original frozen contract, recorded `contract-clarification.md` as post-first-run, implemented the even extension, added its symmetry check, and reran. Positive-frequency results did not change. Admission refers to the repaired ten-check result, with both contract hashes retained.

## Adaptive selection of Round 3

User steering asks to improve the inherited Resonant Vessels alchemical interpretations rather than accept them as deciphered. Round 2 shows why a measured sign cannot be assigned uniquely to an internal cause without a measurement map. Round 3 transfers this precise question to an explicitly synthetic mixture model inspired by Newton's logs of separations, masses and appearance.

Select A=[[1,0,1],[0,1,1]], with dimensionless nonnegative relative amounts c=(0.2,0.4,0.3). Then y=(0.5,0.7). The candidate family c+t(−1,−1,1), for −0.3≤t≤0.2, leaves both channels unchanged. These are relative amounts, not fractions constrained to sum to one.

The positive intervention adds an independent assay row (0,0,1). The damaging control adds a duplicate row (1,0,1). Require exact rational algebra, rank/domain-nullity bookkeeping and noise-free reconstruction before drawing a conclusion. This simplifies the history producer's original proposed assay while retaining its question; the production contract must record actual chosen values before execution.

The expected useful output is a method: list competing material interpretations, identify observations they share, and propose an independent discriminator. The synthetic rows do not identify a historical chemical. Real decipherment still needs manuscript-specific dictionary evidence and calibrated chemical assays. Noise robustness is reserved for a later decision after the exact model is reviewed.
