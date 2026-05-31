---
name: merge-local-files
description: 'Analyze the StellarisPlus mod''s own files, produce a safe-merge report by folder (LIOS/FIOS/DUPL/MERGE), and then consolidate redundant files into fewer files without changing load-order behaviour or game functionality. Use when user says "merge local files", "consolidate files", "reduce file count", "merge mod files", "file consolidation", "clean up files", "merge duplicate files", or wants to avoid repeated load-order analysis by running a single automated merge pass over the mod''s internal files.'
argument-hint: >-
  Optional: folder path to scope (e.g. "common/buildings"). Omit
  the argument to scan the whole mod.
---

# Merge Local Files

## Purpose & Scope

Consolidate redundant files within StellarisPlus into fewer files per
folder. No vanilla override logic is changed. Use this to reduce file
count and simplify the mod's structure after absorbing external mods.

- Reference: `doc/mod_load_reference.md`,
  `doc/mod_merge_order_report.md`.

---

## Naming Conventions

- LIOS merged files: must sort **last** -- use `zz_sp_<topic>.txt`.
- FIOS merged files: must sort **first** -- use `00_sp_<topic>.txt`;
  preserve content order inside merged file.
- MERGE merged files: any name (e.g. `zz_sp_on_actions.txt`).
- Separator comment between merged sections:
  `# === merged from <original_filename> ===`

## Code Style

- Preserve original whitespace and CRLF line endings.
- Do not modify content inside blocks.
- FIOS `scripted_variables/`: `~~` prefixed files are fallback
  defaults. Keep them separate; do not merge them with non-`~~` files.

## Error Handling

- Pre-merge check: `git status --short`. Warn if dirty; do not proceed
  without user acceptance.
- Never merge files that are exact-path vanilla overrides (engine uses
  mod copy only on exact filename match).

## Testing

- Run `& "tools/stellarisplus-quality-gate.ps1"` after merging.
- Flag duplicate top-level keys in merged files (informational, not
  blocking).

---

## Merge Workflow

### Phase 1 -- Scan and Classify

1. **Enumerate** all files by folder (scope defaults to full mod).
2. **Classify** each folder's load strategy per
   `doc/mod_load_reference.md`:

   | Strategy | Mergeable? | Merged filename rule |
   | -------- | ---------- | -------------------- |
   | LIOS | Yes | Must sort **last** (`zz_sp_<topic>.txt`) |
   | FIOS | Yes (order-sensitive) | Must sort **first** (`00_sp_<topic>.txt`); preserve content order |
   | MERGE | Yes (additive) | Any name (e.g. `zz_sp_on_actions.txt`) |
   | DUPL | **No** -- skip | `inline_scripts/`, `name_lists/`, `strategic_resources/`, `traits/` keep exact filenames |

3. **Identify merge candidates** -- a folder qualifies only if:
   - Strategy is LIOS, FIOS, or MERGE.
   - File count > 1.
   - No file is an exact-path vanilla override.
   - All files belong to this mod.

### Phase 2 -- Report

Present to user before executing:

- **A. Folders to merge**: Folder | Strategy | Current files |
  Proposed merged filename | Notes.
- **B. Folders to skip**: Folder | Reason.
- **C. Risk summary**: total files before/after, load-order safety
  assessment, manual review items.

Wait for user approval.

### Phase 3 -- Execute

1. **Pre-merge check**: `git status --short`.
2. **For each candidate folder**:
   - Read all source files.
   - Concatenate with `# === merged from <filename> ===` separators.
   - LIOS: sort ascending, last-winning content at end.
   - FIOS: sort ascending, first-winning content at top.
   - MERGE: any order.
   - Write merged file. Delete source files only after successful
     write.
   - Verify file count: `(Get-ChildItem -File -Path "<folder>").Count`
3. **Update `doc/mod_merge_order_report.md`** with new consolidated
   filenames.

### Phase 4 -- Validation

1. **Duplicate key scan**: flag duplicate top-level keys in merged
   files (informational, not blocking).
2. **Quality gate**: `& "tools/stellarisplus-quality-gate.ps1"`
3. **Summary**:

   ```text
   Folders merged: N | Files removed: N | Files created: N
   Duplicate keys: <list or "none"> | Quality gate: pass/fail
   ```

---

## Files That Must Never Be Merged

- Files whose path exactly matches a vanilla file (engine uses mod
  copy only on exact filename match).
- `common/solar_system_initializers/` vanilla replacements (VEST
  precursor hook).
- `common/inline_scripts/` (always DUPL; filename = call target).
- `events/` files shadowing vanilla event IDs.

When in doubt, check vanilla installation before treating a file as
renameable.

---

## Quick Decision Matrix

```text
1) If folder has 0 or 1 file: skip.
2) If strategy is DUPL: skip (exact filename required).
3) If strategy is LIOS: merge, and use a filename that sorts LAST.
4) If strategy is FIOS: merge, and use a filename that sorts FIRST;
   preserve content order.
5) If strategy is MERGE: merge as additive content.
```
