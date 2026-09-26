# Round 3 frozen contract — observations and composition

Frozen before implementation and execution, 2026-09-26 UTC. Selected by the advisor
after the Round 2 nonidentifiability result and independent review. This is a
mathematical analogue of an archive interpretation problem, not a chemical recipe
or an assertion about what Newton's observed materials actually contained.

Relative component amounts c=(c1,c2,c3) are nonnegative dimensionless amounts, NOT
fractions constrained to sum to one. Two calibrated hypothetical linear assay
signals satisfy y=A c, A=[[1,0,1],[0,1,1]]. Reference c=(1/5,2/5,3/10).
Expected y=(1/2,7/10). Kernel vector n=(-1,-1,1). All c+t n, for
t in [-3/10,1/5], are nonnegative and have identical y. No hidden normalization
or additional measurement may be introduced to remove this ambiguity.

An independent third assay row (0,0,1) is the positive recovery control.
A duplicate row (1,0,1) is the negative control. Matrix rank and domain dimension
must be reported explicitly. Two nonzero singular values of a 2x3 matrix do not
establish injectivity; its domain has dimension 3.

## Frozen gates

1. Exact rational RREF gives rank(A)=2, nullity=1 and A n=0.
2. All 101 equally spaced rational t values in the stated interval are nonnegative
   and yield exactly the reference y; endpoints are included. The algebraic
   kernel proof, not this sample alone, proves the entire interval's equality.
3. Independent assay matrix rank=3 and exact inverse reconstruction recovers the
   reference and both endpoints; numerical inverse error <=1e-12.
4. Duplicate assay matrix rank=2 and exact equality holds for both distinct
   endpoint compositions. Repeating a signal does not add a new constraint.
5. No normalized composition fractions are silently substituted. Record sums
   along the fiber; at least two sums must differ, demonstrating that no sum-to-one
   side condition is present.
6. Save rational results, sampled family CSV, source/contract hashes, and a diagram
   with component amounts, original measurements and the new independent channel.

Noise and assay conditioning are intentionally absent here and will be considered
only after this round's independent review. No executed chemical process, nuclear
transmutation, or historical mechanism is implied by the assay matrices.
