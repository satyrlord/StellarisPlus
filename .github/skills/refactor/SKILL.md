---
name: refactor
description: 'Surgical, behavior-preserving cleanup for the native MixJam repository. Use when the user asks to refactor, simplify, clean up, reduce complexity, untangle, de-duplicate, or make code easier to change without adding features.'
---

# Refactor

## Purpose & Scope

Reduce structural and local complexity without changing behavior, contracts, or
validation coverage.

## Golden Rules

1. preserve behavior exactly
2. understand the existing code before changing it
3. take small, local steps
4. validate after each step
5. prefer clearer control flow over clever compression
6. do not mix cleanup with new feature work

## Cleanup Modes

Use the same skill for both of these shapes:

- structural refactor: extract seams, split responsibilities, and improve
  module boundaries
- local simplification: clarify control flow, naming, duplication, and
  low-value wrappers

If the work widens beyond one of those two shapes, re-evaluate the slice
before continuing.

## Good Targets

- very long methods
- duplicated parsing or mapping logic
- classes that mix UI, IO, and domain concerns
- unclear names that hide the real responsibility
- shallow wrappers that add no leverage
- UI code that mixes orchestration with IO or persistence details

## Process

1. identify one concrete source of complexity
2. confirm current behavior with existing tests or a focused guard test when
   risky
3. apply one cleanup step
4. run focused validation immediately
5. repeat only while the next step is still local and low-risk

## Chesterton's Fence

If you do not know why a piece of code exists, read more context before
changing it. Hidden constraints in parser tolerance, IO behavior, and UI
threading are easy to break by accident.

## MixJam Defaults

- keep refactors separate from new behavior
- prefer extracting seams that improve locality and testability
- do not widen a cleanup into unrelated drive-by edits
- delete dead code only when you can prove it is no longer part of the active
  path

## Native Examples

- extract path validation out of a view model into a dedicated service
- split parser field reads from business mapping
- move MixJam serialization out of UI event handlers
- simplify nested control flow in an import or playback workflow without
  changing outcomes

## Validation

Apply `.github/rules/quality-gate.instructions.md` after each cleanup
step. Preserve existing tests and add a focused regression test before risky
structural changes when needed. If the cleanup changes a durable seam, follow
with `stellaris-code-review` or `specs-and-decisions` as needed.
