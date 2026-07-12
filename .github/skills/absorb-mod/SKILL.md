---
name: absorb-mod
description: 'Absorb or remove an external Stellaris mod in StellarisPlus. Use for a new full-mod integration or for undoing a previously credited absorption.'
argument-hint: >-
   Workshop ID, folder path, or zip path to absorb; or mod name/ID to undo
---

# Absorb Mod

## Purpose & Scope

Integrate an external Stellaris mod into StellarisPlus, or undo a
previous absorption. Covers the full lifecycle: locate, backup,
analyze, merge, validate, and credit.

- Reference docs: `doc/mod_load_reference.md`,
  `doc/mod_defines_reference.md`, `doc/mod_mechanics_reference.md`.
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

2. **Backup** to `backup/<id>/`.
   Stop if that path exists; never overwrite an absorption baseline without
   explicit user confirmation and a separately preserved copy.
3. **Parse `descriptor.mod`**: extract `name`, `tags`,
   `supported_version`, `remote_file_id`.

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
     positioning). Flag major hierarchy restructures for visual check.
   - **Assets** (`gfx/`, `sound/`): copy directly; if exists, ask
     user which to keep.
3. **Adjust load order** -- rename prefixes if needed per
   `doc/mod_load_reference.md`.
4. **Resolve variable conflicts** -- present shadowed vars to user;
   user picks value.

### Phase 4 -- Validation

1. Run `& "tools/stellarisplus-quality-gate.ps1"` and fix all issues.
2. **Cross-reference check**: verify script-to-localisation,
   script-to-GFX, GFX-to-DDS, inline_script calls, event refs in
   on_actions.
3. **Multi-language localisation**: if incoming mod has only English,
   copy English strings as fallback to `l_braz_por`, `l_french`,
   `l_german`, `l_polish`, `l_russian`, `l_simp_chinese`,
   `l_spanish`.

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
   | merge-local-files: folders merged / files removed | X / X |

## Undo Absorption

Reverses a previously absorbed mod. Triggered by "undo absorb",
"remove mod", etc.

1. **Identify mod** -- match Workshop ID or name against `credits.md`;
   confirm `backup/<id>/` exists.
2. **Build removal manifest** using backup as reference:

   | Situation | Action |
   | --------- | ------ |
   | Direct-copy, unchanged since absorption | Delete |
   | Direct-copy, modified since | Flag for review |
   | Content merged into shared file | Extract and remove absorbed content |
   | Binary asset unique to absorbed mod | Delete |
   | Shared with another absorbed mod | Keep (flag) |

3. Present manifest to user, wait for confirmation.
4. **Remove direct-copy files** and empty parent dirs.
5. **Unmerge shared files** -- remove blocks/keys matching backup;
   validate brace balance after each.
6. **Clean up references** -- fix or remove broken localisation keys,
   GFX sprites, event hooks, orphaned variables.
7. **Update `credits.md`** -- remove entry.
8. **Optionally remove `backup/<id>/`** (ask user).
9. Run `& "tools/stellarisplus-quality-gate.ps1"`, fix issues, report
   summary.

## Completion Criteria

Absorption is complete only when every source file is recorded as copied,
merged, or intentionally skipped; every detected conflict and cross-file
reference is resolved; attribution and date metadata are current; changed files
have been re-read; and two consecutive quality-gate runs are clean.

Undo is complete only when every item in the removal manifest is removed,
retained, or explicitly deferred; no absorbed-only reference remains; credits
are accurate; changed files have been re-read; and two consecutive
quality-gate runs are clean. Preserve `backup/<id>/` unless the user explicitly
authorizes its deletion.
