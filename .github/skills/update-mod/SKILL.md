---
name: update-mod
description: 'Update one already-integrated Stellaris mod from its current Workshop files while preserving StellarisPlus customizations and the original absorption backup.'
argument-hint: >-
   Workshop ID or mod name to update (must already be in credits.md)
---

# Update Integrated Mod

## Purpose & Scope

Update an already-absorbed mod (listed in `credits.md`) to its latest
Workshop version. Covers backup, diff analysis, merge, validation, and
cleanup.

- Reference docs: `doc/mod_load_reference.md`,
  `doc/mod_defines_reference.md`, `doc/mod_mechanics_reference.md`.
- If the mod is not in `credits.md`, redirect to the **absorb-mod**
  skill.

---

## Shared Rules

Follow `absorb-mod`'s Naming Conventions, Error Handling, Testing,
and Security rules with these delta additions and overrides:

### Error Handling (delta)

- Major `supported_version` jump: warn user; expect broader changes
  and testing needs.
- Workshop folder unchanged: report no upstream changes detected.
- Multiple mods to update: process one at a time.

### Security (delta)

- Update `credits.md` if mod name or author changed.

---

## Update Workflow

### Phase 1 -- Identify and Backup

1. **Resolve target** -- match user input against `credits.md`:

   | Input | Match strategy |
   | ----- | -------------- |
   | Workshop ID | Match `Workshop ID: <id>` |
   | Mod name | Fuzzy match mod names |
   | `backup/<id>/` path | Extract ID |

2. **Locate latest** at
   `C:\Program Files (x86)\Steam\steamapps\workshop\content\281990\<id>`.
   Verify content exists.
3. **Snapshot current upstream** to a unique
   `tmp/update-mod/<id>/<timestamp>/` working directory. Never overwrite or
   delete `backup/<id>/`; it is the absorption and undo baseline.

   ```powershell
   $snapshot = "tmp\update-mod\<id>\<timestamp>"
   New-Item -ItemType Directory -Path $snapshot
   Copy-Item -Path (Join-Path $workshopDir '*') -Destination $snapshot -Recurse
   ```

### Phase 2 -- Diff Analysis

1. **Build inventories**: UPSTREAM = the unique `tmp/update-mod/` snapshot,
   BASELINE = `backup/<id>/`, OURS = workspace
   root. Skip `descriptor.mod`, `thumbnail.*`, `.mod` files.
2. **Classify changes**:

   | Comparison | Classification | Action |
   | ---------- | -------------- | ------ |
   | Only in UPSTREAM | New upstream content | Add |
   | Only in OURS | Our custom addition | Keep |
   | Both identical | Up to date | Skip |
   | Both differ | Needs merge | Analyze |

3. **Analyze differing files**:
   - **Binary assets**: replace with upstream, unless we have a
     `zzzz_stellarisplus_` version (keep ours).
   - **Scripts**: block-level diff. New upstream blocks: add. Our-only
     blocks: preserve. Both differ: upstream bug-fixes/features
     applied, our customizations preserved. If uncertain, ask user.
   - **Localisation**: new keys from upstream added; differing values
     keep ours (flag for review).
   - **GFX/GUI**: same as scripts -- block-level merge.

4. **Present diff summary** to user, wait for confirmation.

### Phase 3 -- Apply Updates

1. **Add new files** from upstream.
2. **Merge differing files** per type (same strategies as Phase 2.3).
3. **Resolve variable conflicts** -- if upstream changed a variable
   documented in `doc/mod_mechanics_reference.md` as intentionally
   ours, keep ours. Otherwise update.

### Phase 4 -- Validation

1. Run `& "tools/stellarisplus-quality-gate.ps1"` and fix all issues.
2. **Cross-reference check**: new script refs have localisation keys,
   GFX sprites, inline_script templates, and on_action event hooks.
3. **Load-order check**: verify new or renamed files follow
   `doc/mod_load_reference.md` prefix conventions.
4. **Run `merge-local-files`** only after quality gate is green. Fix
   any issues it introduces.

### Phase 5 -- Finalize

1. **Clean up the temporary snapshot** only after the final report accounts for
   it. Preserve `backup/<id>/` without exception unless the user separately
   requests and confirms deletion.
2. **Update `credits.md`** if mod name or author changed.
3. Run `& "tools/stellarisplus-refresh-credits-dates.ps1"` to refresh
   `Last updated` dates from git history.
4. **Report summary**:

   | Metric | Count |
   | ------ | ----- |
   | Files added / merged / unchanged | X / X / X |
   | Conflicts resolved | X |
   | Validation errors fixed | X |
   | merge-local-files: folders merged / files removed | X / X |

---

## Decision Rules

| Situation | Rule |
| --------- | ---- |
| Upstream restructured files | Detect renames (similar content, different paths); treat as rename, not add+delete |
| Update touches SP core vars (`@BPV_CITY_SLOT`, etc.) | Always keep SP values and adapt upstream changes |
| Major `supported_version` jump | Warn user; expect broader changes and testing |
| Multiple mods to update | Process one at a time |
| Workshop folder unchanged | Report no upstream changes detected |

## Completion Criteria

The update is complete only when every upstream change relative to the preserved
baseline is classified; every added, merged, retained, and rejected change is
accounted for; StellarisPlus customizations and load-order behavior are
preserved; cross-file references and credits metadata are current; changed
files have been re-read; and two consecutive quality-gate runs are clean. A
no-change result is complete only when the live Workshop snapshot and baseline
are proven identical for all in-scope files.
