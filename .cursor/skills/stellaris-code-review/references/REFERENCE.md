# Code Review Reference

Use this reference when the review needs the strict maintainability standard in
full detail.

## Core Prompt

> Perform a deep code quality audit of the current branch's changes.
> Rethink how to structure and implement the changes to improve code quality
> without changing behavior.
> Improve abstractions, modularity, legibility, and reduce spaghetti growth.
> Be ambitious when there is a clear path to simpler structure.
> Be thorough and rigorous.

## Non-Negotiable Standards

1. Be ambitious about structural simplification; prefer deleting complexity over
   rearranging it.
2. Treat crossing from under 1k lines to over 1k lines in one file as a strong
   smell unless strongly justified.
3. Do not normalize ad-hoc branching or scattered special cases.
4. Prefer direct and maintainable code over magical or brittle abstractions.
5. Push for clean type and boundary contracts when they affect maintainability.
6. Keep logic in canonical layers and reuse existing helpers.
7. Flag avoidable orchestration complexity and non-atomic update flows.

## Primary Review Questions

- Is there a code-judo move that makes this dramatically simpler?
- Can fewer concepts, branches, or helper layers solve the same problem?
- Does this improve or worsen local architecture?
- Did branching complexity increase where a cleaner abstraction should exist?
- Is logic in the right file and layer?
- Did the diff bloat a file or component past healthy size?
- Does the implementation rely on incidental control flow?
- Is an abstraction earning its keep or acting as indirection noise?
- Did the diff muddy invariants with casts, optionality, or loose object shapes?
- Is orchestration more sequential or less atomic than needed?

## Aggressive Flags

Escalate when you see:

- complexity that could be deleted with a clearer reframing
- refactors that move complexity around but do not reduce concepts
- new conditionals bolted onto unrelated flows
- one-off flags that tangle existing control paths
- feature logic leaking into general-purpose modules
- thin wrappers or identity abstractions adding no leverage
- duplicate helpers where a canonical one already exists
- avoidable sequential async orchestration
- partial updates that leave state hard to reason about

## Preferred Remedies

- delete unnecessary indirection layers
- reframe state so conditionals disappear
- move ownership to the right module or service
- collapse duplicate branches into one explicit flow
- extract focused helpers or pure functions
- split oversized files into focused modules
- make type boundaries explicit to simplify control flow
- parallelize independent work when it also clarifies orchestration
- restructure related updates into more atomic flows

## Output Expectations

Prioritize findings in this order:

1. structural regressions
2. missed simplification opportunities
3. branching and spaghetti growth
4. boundary and type-contract clarity issues
5. file-size and decomposition concerns
6. modularity and abstraction quality
7. legibility and maintainability

Prefer fewer high-conviction findings over many cosmetic nits.

## Approval Bar

Do not approve solely because behavior seems correct. Approval requires:

- no clear structural regression
- no obvious missed simplification with clear path
- no unjustified file-size explosion
- no obvious spaghetti growth
- no hacky abstraction that worsens reasoning
- no avoidable wrapper/cast/optionality churn obscuring design
- no clear architecture-boundary leak or helper duplication

Treat these as presumptive blockers unless justified clearly by the author.
