---
name: update-mod
description: 'Update an already-integrated Stellaris mod in StellarisPlus to its latest Workshop version. Backs up the new upstream, diffs against the current integration, applies new features and bug fixes, and resolves conflicts. Use when user says "update mod", "refresh mod", "sync mod", "upgrade mod", "re-sync mod", "pull latest mod", "update Workshop mod", "update integrated mod", "check for mod updates", or wants to bring an already-absorbed mod up to date with its latest Workshop release.'
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

## Naming Conventions

- Follow existing load-order prefixes from
  `doc/mod_load_reference.md` when adding new files.
- Preserve the mod's existing key names; do not rename without
  updating all references.

## Error Handling

- Major `supported_version` jump: warn user; expect broader changes
  and testing needs.
- Workshop folder unchanged: report no upstream changes detected.
- Multiple mods to update: process one at a time.

## Testing

- Run `& "tools/stellarisplus-quality-gate.ps1"` after applying
  updates.
- Cross-reference check: new script refs have localisation keys, GFX
  sprites, inline_script templates, and on_action event hooks.
- Run `merge-local-files` only after quality gate is green.

## Security

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
3. **Copy to `backup/<id>/`** (temporary working cache):

   ```powershell
   Copy-Item -Path "$workshopDir\*" -Destination "backup\<id>" -Recurse -Force
   ```

### Phase 2 -- Diff Analysis

1. **Build inventories**: UPSTREAM = `backup/<id>/`, OURS = workspace
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

1. **Clean up backup**: `Remove-Item -Path "backup\<id>" -Recurse -Force`
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
