# Code Review Reference

Use this reference when the review needs the strict maintainability standard in
full detail.

## Strict Review Lenses

Apply each lens once:

1. **Simplification**: prefer deleting concepts, branches, or indirection over
   rearranging them. Flag a wrapper, helper, or abstraction only when a smaller
   concrete design is available.
2. **Ownership**: keep gameplay, UI, localisation, compatibility, and validation
   logic in their canonical files. Flag leakage only with the intended owner.
3. **Control flow**: reject ad-hoc branches, one-off flags, and incidental state
   when one explicit flow can replace them.
4. **Atomicity**: require related script, localisation, GFX, and documentation
   changes to apply and reverse as one coherent set.
5. **Scale**: treat a change that pushes one file across 1,000 lines as a strong
   decomposition signal, not an automatic defect.
6. **Invariants**: make load-order, variable, helper, and cross-file contracts
   explicit; reject changes that distribute one invariant across multiple
   owners.

For each structural finding, name the observed complexity, the violated lens,
and the smallest maintainable alternative. Omit cosmetic observations that do
not change the approval decision.

## Approval Bar

Approve only when behavior is correct, every applicable lens has been checked,
and no evidenced structural regression or simpler concrete design remains.
Treat an unresolved lens violation as a blocker unless the report records a
specific justification.
