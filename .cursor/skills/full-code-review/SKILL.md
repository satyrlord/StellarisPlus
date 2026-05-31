---
name: full-code-review
description: >
  Run a strict review focused on correctness, architecture, safety,
  performance, and maintainability for MixJam changes. Use when the user asks
  for a code review, PR review, merge-readiness check, hardening pass, or
  performance-focused review.
disable-model-invocation: true
---

# Full Code Review

## Goal

Review the change like a strict senior teammate: find real defects and
ship-risk first, then identify design quality issues that should be fixed
before merge.

## Read First

1. `AGENTS.md`
2. the relevant source-of-truth docs under `docs/`
3. changed tests and nearby tests
4. changed implementation files

Use `.cursor/references/security-checklist.md` and
`.cursor/references/performance-checklist.md` when the slice touches trust
boundaries or hot paths.

## Use When

- the user asks for review, code review, PR review, or merge readiness
- a change touches parsers, file paths, settings, bridge payloads, or process
  launch paths
- import, extraction, playback, or UI responsiveness may have regressed

## Review Workflow

1. Confirm intended behavior from task text, docs, or tests.
2. Review tests first to establish expected behavior and gaps.
3. Review implementation across five axes:
   - correctness
   - readability and simplicity
   - architecture and layer boundaries
   - input/output safety
   - performance and responsiveness
4. Escalate findings by severity and include the smallest concrete fix.
5. Report verification gaps separately from confirmed defects.

## Output Contract

Return findings first, highest severity first, then open questions and residual
risk. If no findings remain, say `No findings` and call out any test gap.

## Quick Finding Example

```markdown
## Findings

### High
- `MixJam/Import/Foo.cs`: parser accepts unchecked offset and can read past
  bounds for malformed input; validate length before read and return a
  user-readable import warning.
```

## Deep Review Reference

Use [REFERENCE.md](REFERENCE.md) for the full strict-review policy, structural
quality rules, approval bar, and expanded prompts.
