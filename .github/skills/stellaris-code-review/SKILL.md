---
name: stellaris-code-review
description: 'Code review for Paradox Script in Stellaris mods. Validates syntax, scope correctness, localisation, GFX/GUI integrity, load-order safety, and cross-file consistency. Use when user says "code review", "review code", "review changes", "check script", "validate mod", "review mod", "review project", "script review", or wants to inspect uncommitted changes or audit the full project.'
argument-hint: >-
   Optionally specify files, folders, or focus areas (e.g., "only
   localisation", "just the events")
disable-model-invocation: true
---

# Stellaris Code Review

## Purpose & Scope

Two-phase review for Paradox Script in Stellaris mods: Phase 1 = deep
review of uncommitted changes; Phase 2 = broad project audit.

This review is strict and merge-readiness oriented: surface concrete
defects and ship risk first, then design-quality issues.

## Goal

Review the change like a strict senior teammate: find real defects and
ship-risk first, then identify design quality issues that should be
fixed before merge.

## Read First

1. `AGENTS.md`
2. the relevant source-of-truth docs under `docs/`
3. changed tests and nearby tests
4. changed implementation files

Use `.github/references/security-checklist.md` and
`.github/references/performance-checklist.md` when the slice touches
trust boundaries or hot paths.

For Stellaris-script reviews, continue to use the Stellaris reference
order below to keep script and load-order decisions linear.

## Use When

- the user asks for review, code review, PR review, or merge readiness
- a change touches parsers, file paths, settings, bridge payloads, or
  process launch paths
- import, extraction, playback, or UI responsiveness may have regressed
- user asks for script review, mod validation, or uncommitted-change
  audit in this repository

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

- Use this reference order to keep decisions linear:

  | Step | Reference | Use for |
  | ---- | --------- | ------- |
  | 1 | `.github\skills\stellaris-code-review\references\paradox-script-rules.md` | Syntax, scope, and parser rules |
  | 2 | `doc/mod_load_reference.md` | Override behavior and LIOS/FIOS/DUPL/MERGE safety |
  | 3 | `doc/mod_merge_order_report.md` | Only when reviewing duplicated or merged local files |

- **Evidence-first**: cross-check assumptions against actual
  vanilla/DLC/mod files; do not assume missing references or override
  validity without concrete evidence.

## Output Contract

Return findings first, highest severity first, then open questions and
residual risk. If no findings remain, say `No findings` and call out
any test gap.

## Quick Finding Example

```markdown
## Findings

### High
- `MixJam/Import/Foo.cs`: parser accepts unchecked offset and can read
  past bounds for malformed input; validate length before read and
  return a user-readable import warning.
```

## Deep Review Reference

Use [REFERENCE.md](references/REFERENCE.md) for the full strict-review policy,
structural quality rules, approval bar, and expanded prompts.

---

## Naming Conventions

- Filename prefixes must match load-order intent per
  `doc/mod_load_reference.md`.
- `_replace` files must contain vanilla objects.
- Override prefixes (`zz_`, `zzzz_`) must be commented or documented.

## Code Style

- Brace balance: `{` count must equal `}` count.
- No effects in trigger blocks (`potential`, `allow`, `limit`,
  `any_*`).
- `if` must have `limit`; `else_if` before `else`; no `else_if`
  after `else`.
- Modifier symmetry: `add` has a corresponding `remove` path.

## Error Handling

- Never review `backup/` files.
- Do not flag whitespace-only changes unless they break Paradox
  parsing.
- 20+ files changed: summarize list first, ask user.

## Testing

- Run `& "tools/stellarisplus-quality-gate.ps1"` as the automated
  validation baseline.
- Check `get_errors` for VS Code Problems.

---

## Phase 1 -- Uncommitted Changes (Deep)

### 1.1 Gather changed files

Use `get_changed_files` + `git status --short`. Categorize:

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

Optionally scan `doc/changelog.md` for recent entries affecting the
files under review so you have intent context before flagging a risky
override or consolidation.

### 1.2 Review each changed file

Read full file. Use diff to focus, but validate surrounding context.

**Gameplay scripts** (`common/**/*.txt`):

1. Brace balance (`{` == `}`)
2. Scope correctness (no invalid chains like `owner = { owner = { } }`)
3. No effects in trigger blocks (`potential`, `allow`, `limit`, `any_*`)
4. `@variable` refs defined in `scripted_variables`; check for shadowing
5. `inline_script` calls: params match template `$PARAM$`; `script =` resolves
6. Filename prefix matches intent per `doc/mod_load_reference.md`
7. Modifier symmetry: add has corresponding remove path
8. Conditional logic: `if` has `limit`, `else_if` before `else`, no
   `else_if` after `else`
9. Non-localisation script files (`.txt`, `.gfx`, `.gui`, `.asset`)
  must be UTF-8 without BOM; a BOM can cause the first parsed key to
  be rejected
10. When changes touch zones, zone slots, traditions, buildings, or
   districts, cross-check `doc/mod_mechanics_reference.md` for linked
   constraints and constants before flagging or approving the change

**Events** (`events/*.txt`): all above plus:

- `namespace = <name>` declared
- IDs follow `<namespace>.<number>`, unique within file
- Event type matches scope context
- Options have `name` key with localisation
- `is_triggered_only = yes` events referenced somewhere

**Localisation** (`.yml`):

- Language header present (`l_english:`)
- Keys use `:0` format, no duplicates
- `$key$` refs point to existing keys; `[Scope.Method]` uses valid methods
- UTF-8 with BOM

**GFX** (`.gfx`):

- `GFX_` prefix on names; `textureFile` (capital F) paths exist; no
  duplicate names

**GUI** (`.gui`):

- Sprite refs exist in `.gfx`; `@` constants defined before use;
  brace balance
- For `topbar_*.gui` and zone or slot UI files, cross-check
  `doc/mod_ui_reference.md` and `doc/mod_mechanics_reference.md` for
  BPV slot-count consistency and fallback behavior
- Check for GUI template name collisions on LIOS surfaces such as
  `topbar_traditions_view.gui`

### 1.3 Cross-file consistency (changed files)

1. Script `_name`/`_desc`/`_tooltip` keys exist in localisation.
2. `icon = "GFX_..."` refs exist in GFX.
3. `textureFile` paths point to existing DDS.
4. `inline_script` calls resolve with matching params.
5. New/changed `@` variables used somewhere; removed ones not still
   referenced.

---

## Phase 2 -- Project-Wide Audit (Broad)

### 2.0 Run automated validation

```powershell
& "tools/stellarisplus-quality-gate.ps1"
```

Covers: brace balance, duplicate keys, @variable integrity, GFX
cross-refs, texture paths, localisation format, inline params. Also
check `get_errors` for VS Code Problems.

Classify findings: **true positive** (report) | **expected** (verify
against actual files) | **false positive** (note).

Before escalating validator output, verify these repo-specific exception
patterns:

- Duplicate keys are expected in additive folders such as
  `ambient_objects/`, `component_sets/`, `component_templates/`,
  `defines/`, `on_actions/`, `special_projects/`, and
  `species_names/`
- Dotted sprite names can be valid Stellaris naming conventions
- Scoped-flag suffix duplicates can be expected depending on usage
- Multiline quoted inline-script payloads can be valid

### 2.1-2.4 Manual checks

- **Variables**: review shadowed vars flagged by script; intentional
  overrides via load-order are OK if documented.
- **Localisation completeness**: cross-reference script object names
  against localisation keys.
- **GFX/GUI integrity**: review script output for duplicate sprites,
  missing refs. Vanilla refs are expected.
- **Inline scripts**: verify `script =` paths resolve, params match.
- **Load order**: `_replace` files contain vanilla objects; override
  prefixes (`zz_`, `zzzz_`) are commented; no prefix collisions;
  verify folder behavior in `doc/mod_load_reference.md` before calling
  something broken.
- **Load order notes**: `events/` is FIOS, not LIOS; `solar_system_initializers/`
  is FIOS; `localisation/replace/` is the guaranteed override path for
  localisation.

---

## Phase 3 -- Report

```markdown
## Code Review Summary

### Phase 1: Uncommitted Changes
| # | File | Severity | Finding | Recommendation |

### Phase 2: Project-Wide
| # | Category | Severity | Finding | Recommendation |

### Statistics
- Files reviewed / scanned: N / N
- Errors / Warnings / Info: N / N / N
```

| Severity | Meaning |
| -------- | ------- |
| Error | Runtime failure or broken gameplay |
| Warning | Likely unintended, may cause subtle issues |
| Info | Style/cleanup opportunity |

---

## Decision Rules

| Situation | Rule |
| --------- | ---- |
| No uncommitted changes | Skip Phase 1, go to Phase 2 |
| User specifies focus | Limit to that category only |
| 20+ files changed | Summarize list first, ask user |
| `backup/` files | Never review |
| Whitespace-only changes | Do not flag unless they break parsing |
