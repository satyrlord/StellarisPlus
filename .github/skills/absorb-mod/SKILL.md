---
name: absorb-mod
description: 'Absorb a complete external Stellaris mod into StellarisPlus. Use the disclosed removal branch when reversing a credited absorption.'
---

# Absorb Mod

## Purpose & Scope

Integrate an external Stellaris mod into StellarisPlus. For removal requests,
load [`references/undo-absorption.md`](references/undo-absorption.md) and follow
that branch instead of the absorption workflow below.

- Load `doc/mod_load_reference.md` before conflict or prefix decisions.
- Load `doc/mod_defines_reference.md` when incoming content introduces an
  unfamiliar file type, and `doc/mod_mechanics_reference.md` when it changes a
  documented gameplay system.
- Always absorb the **entire** mod. Partial absorption is not allowed
  (creates broken cross-references).

---

## Absorption Workflow

### Phase 1 -- Locate and Backup

1. **Resolve source**:

   | Input | Source path |
   | ----- | ----------- |
   | Workshop ID | `C:\Program Files (x86)\Steam\steamapps\workshop\content\281990\<id>\` |
   | Folder path | As-is |
   | Zip file | Extract to `$env:TEMP`, find `descriptor.mod` inside |

2. **Parse `descriptor.mod`** and extract `name`, `tags`,
   `supported_version`, and `remote_file_id`.
3. **Resolve the Workshop ID** from the explicit input or
   `remote_file_id`. Stop and ask for the ID when neither source provides one;
   do not invent a backup or credits identifier.
4. **Backup** to `backup/<id>/`.
   Stop if that path exists; never overwrite an absorption baseline without
   explicit user confirmation and a separately preserved copy.

Phase 1 is complete only when the source, descriptor metadata, and Workshop ID
are verified and the immutable absorption backup contains the complete source.

### Phase 2 -- Inventory and Analysis

1. **Build file manifest** -- categorize all files in backup:

   | Pattern | Category |
   | ------- | -------- |
   | `common/**/*.txt` | Gameplay script |
   | `events/*.txt` | Event script |
   | `interface/*.gfx`, `*.gui` | GFX/GUI |
   | `localisation/**/*.yml` | Localisation |
   | `gfx/**`, `sound/**`, `flags/**` | Assets |
   | `*.mod`, `thumbnail.*` | Metadata (skip) |

2. **Detect conflicts** -- for each file, check if the same relative
   path exists in workspace:

   When any conflict is found, load
   [`references/conflict-patterns.md`](references/conflict-patterns.md) and
   apply the matching resolution pattern.

   | Conflict | Action |
   | -------- | ------ |
   | None | Direct copy |
   | Identical content | Skip |
   | Both override vanilla differently | Merge review |
   | Both define same custom content | Manual merge |

3. **Check load-order** -- flag prefix clashes per
   `doc/mod_load_reference.md`.
4. **Check scripted variables** -- flag shadowed `@variable`
   definitions (same name, different value).
5. **Report** conflict table to user and wait for approval.

Phase 2 is complete only when every source file has a manifest category, every
conflict and variable shadow has a disposition, and the user approves the
integration plan.

### Phase 3 -- Integration

After user confirms:

1. **Copy non-conflicting files** preserving directory structure.
2. **Merge conflicting files** by type:
   - **Scripts** (`common/**/*.txt`): read both fully; combine blocks,
     deduplicate; preserve brace nesting. If both override vanilla,
     integrate both change-sets.
   - **Localisation** (`.yml`): add new keys; for duplicates keep
     ours; maintain `l_english:` header and `:0` format.
   - **GFX** (`.gfx`): add new sprites; for duplicate names keep ours
     and warn.
   - **GUI** (`.gui`): merge widget trees; new widgets at correct
     nesting; modified widgets merge properties (keep our
     positioning). Record every major hierarchy restructure for Phase 4 visual
     verification.
   - **Assets** (`gfx/`, `sound/`): copy directly; if exists, ask
     user which to keep.
3. **Adjust load order** -- rename prefixes if needed per
   `doc/mod_load_reference.md`.
4. **Resolve variable conflicts** -- present shadowed vars to user;
   user picks value.

Phase 3 is complete only when every manifest entry is copied, merged, or
intentionally skipped and every approved conflict decision is applied.

### Phase 4 -- Validation

1. **Cross-reference check**: verify script-to-localisation,
   script-to-GFX, GFX-to-DDS, inline_script calls, event refs in
   on_actions.
2. **Multi-language localisation**: if incoming mod has only English,
   copy English strings as fallback to `l_braz_por`, `l_french`,
   `l_german`, `l_polish`, `l_russian`, `l_simp_chinese`,
   `l_spanish`.
3. **Visual verification**: when Phase 3 changed a GUI hierarchy, perform the
   relevant in-game visual check. If the environment cannot run it, record the
   check as blocked and obtain explicit user acceptance before completion.
4. Re-read every changed file and run the quality gate until two consecutive
   runs are clean.

Phase 4 is complete only when cross-references, localisation fallbacks, visual
checks, changed-file rereads, and both final gate runs are accounted for.

### Phase 5 -- Finalize

1. **Update `credits.md`** with mod name, Workshop ID, source path,
   author. Add a probe entry for the Workshop ID in
   `tools/credits_date_probes.json` when grep/path heuristics help.
2. Run `& "tools/stellarisplus-refresh-credits-dates.ps1"` to fill
   `Last updated` dates from git history.
3. **Update `descriptor.mod`** only to add new `tags` if applicable.
4. **Report summary**:

   | Metric | Count |
   | ------ | ----- |
   | Files copied / merged / skipped | X / X / X |
   | Conflicts resolved | X |
   | Validation errors fixed | X |

Phase 5 is complete only when attribution metadata is current and the report
counts reconcile with the Phase 2 manifest and Phase 4 evidence.

## Completion Criteria

Absorption is complete only when every phase criterion is satisfied and the
final report accounts for every source file, conflict, reference, validation
result, and attribution change.
