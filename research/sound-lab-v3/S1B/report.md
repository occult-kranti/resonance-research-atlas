# S1B — stability and sensitivity

The saved complex transfer table implements four distinct synthetic cases. A stable noiseless blank is exactly one, and an object-only change returns its specified relative transfer. The masked bounded-noise error is below eta/.15. Removing the mask amplifies near-notch error. Regularization has gain no greater than 25, proved by h/(h²+lambda) ≤ 1/(2 sqrt(lambda)), but introduces the explicitly calculated bias.

Moving only the synthetic echo by one sample produces an apparent object change although the object is absent. The .15 gate is specific to these normalized transfer fixtures. A physical reference-repeat check can reject unstable acquisitions but cannot prove that every unobserved part of the chain stayed fixed. Measurements must report excluded bins and the estimator's bias; never silently fill deep notches as measured response.

Next question: can a free-decay observable reduce the dependence on unknown drive amplitude, and what receiver/overlapping-mode assumptions remain? No physical experiment has been run.

