# S2B — a useful fitter is not a material identifier

Five generated PCM cases pass through the frozen S2A importer with two declared fit windows. The nearby second mode gives a large residual and window-dependent fitted decay. Additive noise grows more important later in a decaying record. All values and flags are saved, including cases that do not cross the fixture's 5% residual flag.

The strongest control is exact: exp(2t) times a 4 s^-1 decay equals a 2 s^-1 decay at every time. Their PCM files are byte-identical. Both receive the same low-residual fit near 2 s^-1; no statistic of that recording alone can decide whether gain changed or physical decay changed. The exp(2t) gain is a constructed counterexample, not a universal model of phone AGC.

A low-material tap protocol therefore requires gain settings, repeat acquisitions, support controls and a modest interpretation: recorded-channel decay under a declared model. Two windows and residuals can reject some data but cannot certify intrinsic damping. The next useful question concerns adding independent geometry/phase observations instead of repeatedly fitting the same scalar trace.

