---
name: update-mod
description: 'Update one already-integrated Stellaris mod from its current Workshop files while preserving StellarisPlus customizations and the original absorption backup.'
---

# Update Integrated Mod

## Purpose & Scope

Update an already-absorbed mod in `credits.md` from its current Workshop
content while preserving StellarisPlus customizations and the immutable
absorption backup.

- Load `doc/mod_load_reference.md` before rename or prefix decisions.
- Load `doc/mod_defines_reference.md` for unfamiliar incoming file types and
  `doc/mod_mechanics_reference.md` when a changed variable or system is
  documented there.
- When a concurrent edit needs conflict resolution, load
  `.github/skills/absorb-mod/references/conflict-patterns.md` and apply the
  matching pattern.
- If the mod is not in `credits.md`, redirect to the **absorb-mod**
  skill.

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

4. **Resolve baselines**:
   - ORIGINAL = `backup/<id>/`, the immutable absorption and undo baseline.
   - BASELINE = `backup/_update-mod/<id>/`, the last successfully integrated
     upstream snapshot. Initialize it from ORIGINAL on the first update; never
     use it for undo.
   - UPSTREAM = the unique temporary snapshot.
   - OURS = the workspace root.

Phase 1 is complete only when all four roots exist, ORIGINAL is unchanged, and
the UPSTREAM and BASELINE inventories are readable.

### Phase 2 -- Diff Analysis

1. **Build inventories** for BASELINE, UPSTREAM, and OURS. Treat absence as a
   file state and skip `descriptor.mod`, `thumbnail.*`, and `.mod` files.
2. **Classify each path with a three-way comparison**:

   | Comparison | Classification | Action |
   | --- | --- | --- |
   | `UPSTREAM == BASELINE` and `OURS == BASELINE` | Unchanged | Skip |
   | `UPSTREAM == BASELINE` and `OURS != BASELINE` | Local-only change | Retain OURS |
   | `UPSTREAM != BASELINE` and `OURS == BASELINE` | Upstream-only change | Apply UPSTREAM, including deletion |
   | `UPSTREAM == OURS` and both differ from BASELINE | Same change already present | Retain once |
   | All other differing states | Concurrent change | Analyze and merge |

3. Detect renames by content similarity before classifying an upstream
   delete-plus-add pair.
4. **Analyze concurrent files**:
   - **Binary assets**: replace with upstream, unless we have a
     `zzzz_stellarisplus_` version (keep ours).
   - **Scripts**: block-level diff. New upstream blocks: add. Our-only
     blocks: preserve. Both differ: upstream bug-fixes/features
     applied, our customizations preserved. If uncertain, ask user.
   - **Localisation**: new keys from upstream added; differing values
     keep ours (flag for review).
   - **GFX/GUI**: same as scripts -- block-level merge.

5. If `supported_version` crosses a major Stellaris version, include every
   upstream path in the summary and require an explicit manual-test scope before
   applying changes.
6. **Present diff summary** with every path and classification; wait for user
   confirmation.

Phase 2 is complete only when every in-scope path has one evidenced
classification and the user approves the apply set and required test scope.

### Phase 3 -- Apply Updates

1. Apply upstream-only additions, edits, renames, and deletions.
2. Merge concurrent files per type using the approved Phase 2 strategy.
3. **Resolve variable conflicts** -- if upstream changed a variable
   documented in `doc/mod_mechanics_reference.md` as intentionally
   ours, keep ours. Otherwise update.

Phase 3 is complete only when every approved path is applied or explicitly
blocked and no local-only customization is lost.

### Phase 4 -- Validation

1. **Cross-reference check**: new script refs have localisation keys,
   GFX sprites, inline_script templates, and on_action event hooks.
2. **Load-order check**: verify new or renamed files follow
   `doc/mod_load_reference.md` prefix conventions.
3. Run the quality gate and repair every finding before invoking
   `merge-local-files` for approved consolidation.
4. Re-read every changed file, then run the quality gate until two consecutive
   runs are clean.

Phase 4 is complete only when reference and load-order checks pass, every
changed file has been re-read, and both final gate runs are clean.

### Phase 5 -- Finalize

1. **Update `credits.md`** if mod name or author changed.
2. Run `& "tools/stellarisplus-refresh-credits-dates.ps1"` to refresh
   `Last updated` dates from git history.
3. After Phase 4 succeeds, copy UPSTREAM to a separate baseline staging path
   and prove its inventory equals UPSTREAM. Replace BASELINE only after that
   proof; preserve the prior BASELINE until the staged copy is verified.
   Preserve ORIGINAL without exception unless the user separately requests and
   confirms deletion.
4. Remove the temporary snapshot and verify that its path no longer exists.
5. **Report summary**:

   | Metric | Count |
   | ------ | ----- |
   | Upstream applied / concurrent merged / local retained | X / X / X |
   | Renames / deletions / rejected | X / X / X |
   | Unchanged | X |
   | Conflicts resolved | X |
   | Validation errors fixed | X |
   | merge-local-files: folders merged / files removed | X / X |

Phase 5 is complete only when credits metadata is current, BASELINE exactly
matches the verified UPSTREAM inventory, the temporary snapshot is removed, and
the report accounts for every classification and validation result.

## Completion Criteria

The update is complete only when every phase criterion is satisfied. A
no-change result is complete only when UPSTREAM equals the rolling BASELINE for
every in-scope path; ORIGINAL is never used as the no-change comparator.
