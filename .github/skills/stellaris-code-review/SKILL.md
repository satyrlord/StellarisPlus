---
name: stellaris-code-review
description: >
  Review StellarisPlus changes for merge readiness across Paradox Script,
  load-order, localisation, GFX/GUI, references, and documentation. The default
  branch is read-only; repair findings only with explicit authorization.
---

# Stellaris Code Review

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
5. changed implementation files and their direct dependencies: definitions or
   consumers connected by one explicit reference edge
6. tests that name a changed identifier or exercise the affected system

Use `.github/skills/stellaris-code-review/references/paradox-script-rules.md`
for syntax, scope, and parser rules. Use
`.github/skills/stellaris-code-review/references/REFERENCE.md` for the
full strict-review policy, structural quality rules, and approval bar.
Use `references/file-type-checks.md` for per-file-type review checklists
during Phase 1.2.

- **Evidence-first**: cross-check assumptions against actual
  vanilla/DLC/mod files; do not assume missing references or override
  validity without concrete evidence.

Reading is complete only when every in-scope file, direct reference edge, and
affected-system test is accounted for, and every unavailable source is recorded
as a verification gap.

---

## Phase 1 — Uncommitted Changes (Deep)

### 1.1 Gather changed files

Use git status to list changed files. Categorize:

| Pattern | Category |
| ------- | -------- |
| `common/**/*.txt` | Gameplay script |
| `events/*.txt` | Event script |
| `interface/*.gfx` | GFX |
| `interface/*.gui` | GUI |
| `localisation/**/*.yml` | Localisation |
| `gfx/**`, `sound/**` | Assets |
| `common/scripted_variables/*.txt` | Variables |
| `common/defines/*.txt` | Defines |
| `common/inline_scripts/**/*.txt` | Inline scripts |
| `doc/**`, `.github/**` | Documentation (light review) |

Skip `backup/`, `tmp/`.

Phase 1.1 is complete only when every `git status` path is categorized or
excluded by the rule above.

### 1.2 Review each changed file

Read full file. Use diff to focus, but validate surrounding context.
Apply the per-file-type checklists in
`references/file-type-checks.md` — gameplay scripts, events,
localisation, GFX, and GUI each have their own checklist.

Phase 1.2 is complete only when every changed file is read in full and every
applicable file-local check has a passing result or a reported finding.

### 1.3 Cross-file consistency (changed files)

1. Script `_name`/`_desc`/`_tooltip` keys exist in localisation.
2. `icon = "GFX_..."` refs exist in GFX.
3. `textureFile` paths point to existing DDS.
4. `inline_script` calls resolve with matching params.
5. New/changed `@` variables used somewhere; removed ones not still
   referenced.

Phase 1.3 is complete only when every applicable edge above resolves or is
reported as a finding.

---

## Phase 2 — Cross-Cutting Validation

Do not repeat Phase 1's file-local checklists. Trace each changed definition to
its direct consumers and each changed reference to its definition. For filename,
prefix, or override judgments, apply `doc/mod_load_reference.md`; for parser,
scope, and inline-script semantics, apply
`references/paradox-script-rules.md`. Phase 2 is complete only when every direct
cross-file edge and load-order-sensitive path is accounted for.

---

## Phase 3 — Project-Wide Audit (Broad)

### 3.0 Run automated validation

```powershell
& "tools/stellarisplus-quality-gate.ps1"
```

Covers brace balance, duplicate keys, variable integrity, GFX cross-references,
texture paths, localisation format, and inline parameters. Check the Problems
view when that integration is available; otherwise report the unavailable
diagnostic rather than inventing a result.

Classify findings: **true positive** (report) | **expected** (verify
against actual files) | **false positive** (note).

Use the exception rules and external-file verification requirements from
`references/paradox-script-rules.md` before escalating validator output. Phase
3 is complete only when every automated finding is classified with evidence and
the manual reference rules have been applied to areas the gate cannot prove.

---

## Phase 4 — Report

```markdown
## Code Review Summary

### Phase 1: Uncommitted Changes
| # | File | Severity | Finding | Recommendation |

### Phase 2: Cross-Cutting Validation
| # | Category | Severity | Finding | Recommendation |

### Phase 3: Project-Wide
| # | Category | Severity | Finding | Recommendation |

### Statistics
- Files reviewed / scanned: N / N
- Critical / High / Medium / Low: N / N / N / N
```

### Finding Severity

| Severity | Criteria |
| -------- | -------- |
| **Critical** | Crash risk, save corruption, load-order reversal, missing required dependency |
| **High** | Broken localisation key, orphan GFX reference, wrong encoding, duplicate event firing |
| **Medium** | Missing changelog entry, missing override comment, style inconsistency |
| **Low** | Documentation clarity, non-blocking code style nits |

Phase 4 is complete only when every confirmed finding and verification gap
appears once in the report, statistics reconcile with the tables, and each
finding includes evidence and the smallest concrete repair.

---

## Decision Rules

| Situation | Rule |
| --------- | ---- |
| No uncommitted changes | Skip Phase 1, go to Phase 2 |
| User specifies focus | Limit deep review to that category; still report direct dependency risk |
| 20+ files changed | Summarize scope, then continue unless user intent is required |
| `backup/` files | Never review |
| Whitespace-only changes | Do not flag unless they break parsing |

## Mutation Contract

The default review branch is read-only: report findings and concrete repairs,
but do not edit files. Enter the repair branch only when the user explicitly
asks to fix findings or an invoking skill explicitly grants repair authority.
In the repair branch, fix every true mod-owned finding, re-read each changed
file, and repeat the quality gate until two consecutive runs are clean. Never
edit vanilla, DLC, external-noise, `backup/`, or `tmp/` files.

## Completion Criteria

The review is complete only when the reading criterion and every applicable
phase criterion are satisfied. The repair branch must also satisfy the Mutation
Contract.
