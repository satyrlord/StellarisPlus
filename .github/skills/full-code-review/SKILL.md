---
name: full-code-review
description: >
  Run a strict, comprehensive review of StellarisPlus changes covering
  Paradox Script correctness, load-order safety, localisation integrity,
  GFX/GUI consistency, cross-file references, and documentation quality.
  Delegates to stellaris-code-review for Paradox Script review and
  adds documentation, changelog, credits, and cross-cutting validation.
  Use when the user asks for a full code review, merge-readiness check,
  pre-release audit, or comprehensive quality sweep.
argument-hint: >
  Optionally specify files, folders, or focus areas (e.g. "only events",
  "just the new traditions")
disable-model-invocation: true
---

# Full Code Review — StellarisPlus

## Purpose & Scope

Comprehensive review covering every layer of a StellarisPlus change:
Paradox Script, load order, localisation, GFX/GUI, cross-file references,
documentation, and credits. This skill orchestrates the
`stellaris-code-review` skill for script-level review and adds the
documentation and cross-cutting layers that a full merge-readiness check
requires.

## Goal

Review the change like a strict senior modder: find real defects and
ship-risk first, then identify design quality issues that should be
fixed before release. Confirm intended behavior from task text, docs
under `doc/`, existing mod files, and vanilla/DLC references before
judging the implementation.

## Read First

1. `AGENTS.md`
2. the relevant source-of-truth docs under `doc/`:
   - `doc/mod_load_reference.md` — load order and prefix rules
   - `doc/mod_mechanics_reference.md` — gameplay system contracts
   - `doc/mod_ui_reference.md` — UI and GFX conventions
   - `doc/mod_defines_reference.md` — file type and encoding rules
3. `doc/changelog.md` — recent changes in affected areas
4. `credits.md` — integrated mod attribution for affected systems
5. changed implementation files and their cross-file dependencies

## Use When

- the user asks for a full review, merge-readiness check, or pre-release audit
- a change touches multiple layers (script + localisation + GFX + docs)
- a new feature is complete and needs final validation before shipping
- an integrated mod update needs comprehensive conflict review
- load-order strategy changes need verification across all affected files

## Review Workflow

### Phase 1 — Paradox Script Review

Delegate to `stellaris-code-review` for deep script validation:

1. Load `.github/skills/stellaris-code-review/SKILL.md` and
   `.github/skills/stellaris-code-review/references/paradox-script-rules.md`.
2. Run the full Phase 1 (uncommitted changes) and Phase 2 (project audit)
   as directed by that skill.
3. Fix all confirmed mod-owned script defects before proceeding.

### Phase 2 — Cross-Cutting Validation

After script review passes, validate the layers that connect scripts to
the rest of the mod:

#### 2.1 Localisation Audit

- Every script-referenced localisation key must resolve to a `.yml` file
  in `localisation/`.
- No duplicate keys across localisation files.
- All `.yml` files: UTF-8 with BOM, correct language headers, `:0`
  formatting.

#### 2.2 GFX / GUI Audit

- Every `GFX_` sprite reference in `.gui` or `.gfx` files must resolve.
- `textureFile` paths (capital F) in `.gfx` files must point to existing
  DDS assets.
- `.gfx`/`.gui`/`.asset` files: UTF-8 without BOM.

#### 2.3 Cross-File Reference Audit

- Event IDs in `events/` must match `on_actions/` registrations.
- `inline_script` calls must match existing script paths and use correct
  `$PARAM$` names.
- `@scripted_variables` must be declared before use and not shadowed.
- Technology, tradition, building, and district keys referenced across
  files must resolve.

#### 2.4 Load-Order Audit

- Filename prefixes must match the intended load-order strategy per
  `doc/mod_load_reference.md`.
- Override files (`_replace`, `zz_sp_`, `zzzz_`) must target real vanilla
  or mod objects.
- No accidental LIOS files in FIOS-only folders (and vice versa).
- `common/on_actions/` MERGE folder: verify no duplicate event
  registrations from accidentally importing the same source block twice.

#### 2.5 Documentation Audit

- `doc/changelog.md` must have an entry for each user-facing change under
  the current version heading.
- Override files must have a top-of-file `# OVERRIDE:` comment.
- New integrated mod content must be credited in `credits.md`.
- Reference docs (`doc/mod_mechanics_reference.md`, etc.) must reflect
  new or changed contracts.

### Phase 3 — Quality Gate

Run the automated validation baseline:

```powershell
& "tools/stellarisplus-quality-gate.ps1"
```

Check `get_errors` for VS Code Problems. Fix all true mod-owned issues.

## Output Contract

Report findings grouped by phase, highest severity first. Each finding
includes the smallest concrete fix. Keep verification gaps separate from
confirmed defects. If no findings remain across all phases, say
`No findings` and confirm the change is merge-ready.

### Finding Severity

| Severity | Criteria |
| -------- | -------- |
| **Critical** | Crash risk, save corruption, load-order reversal, missing required dependency |
| **High** | Broken localisation key, orphan GFX reference, wrong encoding, duplicate event firing |
| **Medium** | Missing changelog entry, missing override comment, style inconsistency |
| **Low** | Documentation clarity, non-blocking code style nits |

## Error Handling

- Only fix issues owned by this workspace or integrated mods credited in
  `credits.md`.
- Never speculate about vanilla or DLC behavior; verify against official
  files.
- Treat cascading findings as root-cause problems. Fix the source, then
  re-run checks.
- Skip `backup/` and `tmp/` files.
- If a finding requires user intent, stop and ask one concise question.

## Testing

- Create a TODO list for the review.
- Run the quality gate after all fixes: `& "tools/stellarisplus-quality-gate.ps1"`
- Re-read changed files after edits to verify correctness.
