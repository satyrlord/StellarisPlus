---
name: stellaris-code-review
description: >
  Run a strict, comprehensive review of StellarisPlus changes covering
  Paradox Script correctness, load-order safety, localisation integrity,
  GFX/GUI consistency, cross-file references, and documentation quality.
  Use when the user asks for a code review, full code review, merge-readiness
  check, pre-release audit, comprehensive quality sweep, review changes,
  check script, validate mod, review mod, review project, or script review.
argument-hint: >
  Optionally specify files, folders, or focus areas (e.g. "only events",
  "just the new traditions", "only localisation")
disable-model-invocation: true
---

# Stellaris Code Review

## Purpose & Scope

Comprehensive review covering every layer of a StellarisPlus change:
Paradox Script, load order, localisation, GFX/GUI, cross-file references,
documentation, and credits. Four phases: uncommitted-change deep review,
cross-cutting validation, project-wide audit, and final report.

This review is strict and merge-readiness oriented: surface concrete
defects and ship risk first, then design-quality issues.

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
6. changed tests and nearby tests

Use `.github/skills/stellaris-code-review/references/paradox-script-rules.md`
for syntax, scope, and parser rules. Use
`.github/skills/stellaris-code-review/references/REFERENCE.md` for the
full strict-review policy, structural quality rules, and approval bar.

- Use this reference order to keep decisions linear:

  | Step | Reference | Use for |
  | ---- | --------- | ------- |
  | 1 | `references/paradox-script-rules.md` | Syntax, scope, and parser rules |
  | 2 | `doc/mod_load_reference.md` | Override behavior and LIOS/FIOS/DUPL/MERGE safety |
  | 3 | `doc/mod_merge_order_report.md` | Only when reviewing duplicated or merged local files |

- **Evidence-first**: cross-check assumptions against actual
  vanilla/DLC/mod files; do not assume missing references or override
  validity without concrete evidence.

## Use When

- the user asks for review, code review, full code review, PR review, or merge readiness
- a change touches multiple layers (script + localisation + GFX + docs)
- a new feature is complete and needs final validation before shipping
- an integrated mod update needs comprehensive conflict review
- load-order strategy changes need verification across all affected files
- user asks for script review, mod validation, or uncommitted-change audit

---

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

## Phase 2 — Cross-Cutting Validation

After script review passes, validate the layers that connect scripts to
the rest of the mod:

### 2.1 Localisation Audit

- Every script-referenced localisation key must resolve to a `.yml` file
  in `localisation/`.
- No duplicate keys across localisation files.
- All `.yml` files: UTF-8 with BOM, correct language headers, `:0`
  formatting.

### 2.2 GFX / GUI Audit

- Every `GFX_` sprite reference in `.gui` or `.gfx` files must resolve.
- `textureFile` paths (capital F) in `.gfx` files must point to existing
  DDS assets.
- `.gfx`/`.gui`/`.asset` files: UTF-8 without BOM.

### 2.3 Cross-File Reference Audit

- Event IDs in `events/` must match `on_actions/` registrations.
- `inline_script` calls must match existing script paths and use correct
  `$PARAM$` names.
- `@scripted_variables` must be declared before use and not shadowed.
- Technology, tradition, building, and district keys referenced across
  files must resolve.

### 2.4 Load-Order Audit

- Filename prefixes must match the intended load-order strategy per
  `doc/mod_load_reference.md`.
- Override files (`_replace`, `zz_sp_`, `zzzz_`) must target real vanilla
  or mod objects.
- No accidental LIOS files in FIOS-only folders (and vice versa).
- `common/on_actions/` MERGE folder: verify no duplicate event
  registrations from accidentally importing the same source block twice.
- Load order notes: `events/` is FIOS, not LIOS; `solar_system_initializers/`
  is FIOS; `localisation/replace/` is the guaranteed override path for
  localisation.

### 2.5 Documentation Audit

- `doc/changelog.md` must have an entry for each user-facing change under
  the current version heading.
- Override files must have a top-of-file `# OVERRIDE:` comment.
- New integrated mod content must be credited in `credits.md`.
- Reference docs (`doc/mod_mechanics_reference.md`, etc.) must reflect
  new or changed contracts.

---

## Phase 3 — Project-Wide Audit (Broad)

### 3.0 Run automated validation

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

### 3.1-3.4 Manual checks

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

---

## Decision Rules

| Situation | Rule |
| --------- | ---- |
| No uncommitted changes | Skip Phase 1, go to Phase 2 |
| User specifies focus | Limit to that category only |
| 20+ files changed | Summarize list first, ask user |
| `backup/` files | Never review |
| Whitespace-only changes | Do not flag unless they break parsing |

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
- Check `get_errors` for VS Code Problems.

## Quick Finding Example

```markdown
## Findings

### Critical
- `common/buildings/zz_sp_buildings.txt`: override targets non-existent
  vanilla building `building_xxx`; verify target key or remove override.

### High
- `events/my_events.txt`: event `myns.10` missing `name` key in option;
  add `name = myns.10.a` with localisation entry.
```
