---
name: add-feature
description: >
  Creates or updates mod documentation, changelog entries, durable design
  decisions, and reference docs for new StellarisPlus features. Use when
  adding a feature, when docs do not define behavior clearly, when making
  load-order or override decisions, changing mod mechanics, adding new
  gameplay systems, or when the user asks for a spec, design doc, changelog
  entry, or mechanic reference update, or when you need to record context
  that future maintainers and agents will need to understand the mod.
argument-hint: >
  Optionally specify the feature name, affected systems, or doc to update
---

# Add Feature

## Goal

Write or update the smallest durable document that makes the next change
unambiguous and records decisions future maintainers would otherwise have to
rediscover. Document decisions, not just code — the context and trade-offs
that explain *why it was built this way*. Skip obvious code and throwaway
prototypes under `tmp/`.

Use `grill-me` instead when the user wants interactive design grilling,
pressure-testing, or branch-by-branch questioning before documentation.

## First Rule

Do not create a duplicate doc or summary when an existing doc already owns the
behavior. Update the owning document instead.

## Read First

1. `AGENTS.md`
2. the relevant source-of-truth docs under `doc/` for the feature area:
   - `doc/mod_load_reference.md` — FIOS/LIOS/DUPL/MERGE, prefix rules
   - `doc/mod_mechanics_reference.md` — core gameplay systems, dependencies
   - `doc/mod_ui_reference.md` — UI layout, GFX/GUI conventions
   - `doc/mod_defines_reference.md` — file types and folder purposes
3. `doc/changelog.md` — recent changes that may interact with the feature
4. any existing integrated-mod credit in `credits.md` for the affected system

## Choose The Right Home

For **feature tracking** (working documents for an in-progress change):

- `doc/changelog.md` — record what changed and why, under the current version
  heading
- Top-of-file comments — record override rationale in the affected script
  files (e.g. `# OVERRIDE: zz_sp_ — <reason>`)

For **canonical reference docs** (durable knowledge):

- load-order, prefix, and override rules → `doc/mod_load_reference.md`
- gameplay mechanics, slot systems, traditions, integrated mod behavior →
  `doc/mod_mechanics_reference.md`
- UI layout, GFX sprite conventions, GUI structure →
  `doc/mod_ui_reference.md`
- file types, folder purposes, encoding rules →
  `doc/mod_defines_reference.md`
- integrated mod attribution → `credits.md`

Create or update a reference doc for anything expensive to reverse:
load-order strategy changes, override prefix decisions, slot system
contracts, inline script parameter conventions, cross-mod dependency
choices.

Keep the skill catalog in `AGENTS.md` current when adding or changing
skill behaviors.

## Documentation Content

When documenting a feature or design decision, include:

- objective and player-facing value
- which game systems are affected (traditions, buildings, districts, zones, etc.)
- load-order strategy: which prefix, why, and which vanilla/mod files are overridden
- explicit assumptions about vanilla/DLC behavior
- the script contracts being defined (inline script params, scripted variables,
  event IDs, localisation keys)
- non-goals or out-of-scope items
- open questions that still need a human answer
- commands for validation: `& "tools/stellarisplus-quality-gate.ps1"`

## Inline Documentation (Paradox Script)

The highest-value comments record override rationale and load-order gotchas
at the top of the file where a reader would otherwise misinterpret the intent:

```paradox
# OVERRIDE: zz_sp_ — overrides vanilla district slot count;
# must load after UI Overhaul Dynamic (dependency: 1623423360).
# Uses @BPV_ZONE_SLOT for dynamic slot indexing.
```

Every time an agent produces a wrong result from a missing fact (prefix
ordering, DUPL vs MERGE folder behavior, encoding requirements), record
the fact where it matters. No commented-out code, no lingering TODOs.

## Repo Constraints

- Follow the documented load-order, naming, encoding, and code-style rules
  from `AGENTS.md` and the relevant docs under `doc/`.
- Prefer updating existing docs over creating new ones.
- Never invent file paths or directory structures; verify against the
  workspace.
- Integrated mods must be credited in `credits.md`.

## Workflow

1. Surface assumptions before drafting.
2. Pick the owning document (changelog entry, reference doc section, or
   top-of-file comment).
3. Draft the smallest documentation change that closes the ambiguity.
4. For override files, add a top-of-file `# OVERRIDE:` comment and a
   corresponding `doc/changelog.md` entry.
5. Get human confirmation when the decision is hard to reverse or surprising.
6. Hand off to implementation.

## Deep Reference

Use [REFERENCE.md](REFERENCE.md) for durable decision rules and the
decision-record threshold. Use [EXAMPLES.md](EXAMPLES.md) for concrete
StellarisPlus documentation examples.

## Validation

Run the quality gate on any touched script files:

```powershell
& "tools/stellarisplus-quality-gate.ps1"
```

Run `markdownlint-cli2` on edited Markdown files. Check `get_errors` for
VS Code Problems on any changed files.
