---
name: grill-me
description: >
  Stress-tests a StellarisPlus plan or design interactively, resolves
  decision-tree branches, and exposes hidden assumptions before
  implementation. Use when the user says "grill me", asks to pressure-test
  a plan, wants interactive design questioning, or needs open decisions
  driven to closure one branch at a time.
argument-hint: >
  Optionally specify the plan, feature, or decision area to grill
---

# Grill Me — StellarisPlus

Challenge the current plan until the important assumptions, dependencies,
and trade-offs are explicit enough that the next step is obvious. Walk the
highest-risk or least-reversible branch first, one question at a time, and
give your recommended answer with each question.

Do not ask the user anything the codebase, docs under `doc/`, or existing
mod files can answer — explore first when the repository can disconfirm a
branch. Treat the docs under `doc/` as the source of truth unless the user
explicitly reopens a prior decision; call out terminology or contract
conflicts against the reference docs and propose one canonical resolution.

Update relevant documentation after each answer: as soon as a branch is
resolved, write the decision into the doc that owns it (reference doc,
changelog, or top-of-file comment) before moving to the next question —
do not batch doc updates to the end of the session.

## Key Areas to Probe

For StellarisPlus designs, prioritize these high-risk branches:

1. **Load-order strategy**: Which prefix? LIOS or FIOS? Which vanilla or
   mod files are overridden, and in what order?
2. **Cross-mod compatibility**: Does this interact with UI Overhaul
   Dynamic, integrated Workshop mods, or other dependencies?
3. **Slot and zone contracts**: Are inline script parameters consistent?
   Are scripted variable names following `@UPPER_SNAKE_CASE`?
4. **Event namespace collisions**: Is the event ID range unique? Does
   `on_actions` registration avoid double-firing?
5. **Localisation coverage**: Are all script-referenced keys defined?
   Are language headers present?
6. **Reversibility**: If this override or mechanic is wrong, how hard is
   it to undo? What files would need to change?

## When the Questioning Converges

- route to `add-feature` if the outcome needs durable documentation in
  reference docs or changelog
- route to `stellaris-code-review` if the resolved plan is ready for
  script-level validation
- route to `full-build` if the feature is implementation-ready and needs
  the full validation pipeline
- route to `absorb-mod` if the resolution points to integrating an
  external mod

## Validation

Run the quality gate on any touched script files:

```powershell
& "tools/stellarisplus-quality-gate.ps1"
```

Run `markdownlint-cli2` on any Markdown the grilling edits. Check
`get_errors` for VS Code Problems on any changed files.
