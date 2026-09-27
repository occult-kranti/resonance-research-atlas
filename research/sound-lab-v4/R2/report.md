# R2 — conditional uncertainty budget

These observations are positive synthetic envelopes with a **supplied** absolute amplitude-error guarantee. No algorithm has established this guarantee from a microphone recording. The deterministic interval is not a confidence interval.

With w_i=(t_i−mean(t))/sum_j(t_j−mean(t))², q=sum_i w_i(log r_i−log s_i). Each latent amplitude lies in [a_i−delta_i,a_i+delta_i]. Log is monotone. For positive w choose the lower reference/upper target logs at the minimum; reverse at the maximum. For negative w reverse the choices. Summing these independent extrema gives exact endpoints of the rectangular log box. Frozen time/window and no sample deletion are premises. A single lower endpoint at or below zero withholds the entire contrast.

The physical relation is alpha=q+alpha_reference−(beta_reference−beta_target). Supplied absolute bounds .25 s⁻¹ and .4 s⁻¹ therefore widen q by .65 s⁻¹ on each side. If either bound is missing, no physical-alpha interval is returned. The width rises by 1.3 s⁻¹, irrespective of how precise the supplied envelope errors are.

All 128 seeded in-bound synthetic observations cover their true contrast. Direct extremal-envelope constructions attain both box endpoints. Simultaneous corners of the physical nuisance budgets are also covered. An intentionally out-of-budget differential gain of .8 s⁻¹ produces an interval excluding the true alpha, retained as a failure of the premise, not repaired by widening after observation.

Run: `python research/sound-lab-v4/R2/run.py`. Reusable function `slope_interval` validates shapes, finite increasing times, nonnegative finite error budgets and physical nuisance bounds. It rejects invalid inputs and explicitly withholds floor/missing-bound results. Further assumptions of a single exponential, known timebase and faithful separated envelopes remain conditional.
