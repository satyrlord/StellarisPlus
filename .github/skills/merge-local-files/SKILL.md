---
name: merge-local-files
description: 'Merge local StellarisPlus files without changing load-order behavior. Use to classify folders by LIOS/FIOS/DUPL/MERGE and consolidate only proven-safe candidates.'
---

# Merge Local Files

## Purpose & Scope

Consolidate redundant files within StellarisPlus into fewer files per
folder. No vanilla override logic is changed. Use this to reduce file
count and simplify the mod's structure after absorbing external mods.

- Load `doc/mod_load_reference.md` before classifying any folder or filename.
- Load `doc/mod_merge_order_report.md` when discovering existing consolidated
  files and update it after an approved merge.

---

## Merge Workflow

### Phase 1 -- Scan and Classify

1. **Enumerate** all files by folder (scope defaults to full mod). This step is
   complete when every in-scope file belongs to exactly one folder inventory.
2. **Classify** each folder's load strategy per
   `doc/mod_load_reference.md`:

   | Strategy | Mergeable? | Merged filename rule |
   | -------- | ---------- | -------------------- |
   | LIOS | Yes | Must sort **last** (`zz_sp_<topic>.txt`) |
   | FIOS | Yes (order-sensitive) | Must sort **first** (`00_sp_<topic>.txt`); preserve content order |
   | MERGE | Yes (additive) | Any name (e.g. `zz_sp_on_actions.txt`) |
   | DUPL | **No** -- skip | `inline_scripts/`, `name_lists/`, `strategic_resources/`, `traits/` keep exact filenames |

   This step is complete when every inventoried folder has one evidenced
   strategy classification.

3. **Identify merge candidates** by applying the authoritative
   [Non-Candidates](#non-candidates) rules. A folder qualifies only if:
   - Strategy is LIOS, FIOS, or MERGE.
   - File count > 1.
   - All files belong to this mod.

Phase 1 is complete only when every scanned folder is classified as a candidate
or non-candidate with evidence.

### Phase 2 -- Report

Present to user before executing:

- **A. Folders to merge**: Folder | Strategy | Current files |
  Proposed merged filename | Notes.
- **B. Folders to skip**: Folder | Reason.
- **C. Risk summary**: total files before/after, load-order safety
  assessment, manual review items.

Wait for user approval.

Phase 2 is complete only when all three report sections account for every
Phase 1 disposition and the user explicitly approves the candidate set.

### Phase 3 -- Execute

1. **Pre-merge check**: run `git status --short`. Continue only when the
   worktree is clean or the user explicitly accepts the recorded dirty state.
2. **For each candidate folder**:
   - Read all source files.
   - Concatenate with `# === merged from <filename> ===` separators.
   - LIOS: sort ascending, last-winning content at end.
   - FIOS: sort ascending, first-winning content at top.
   - MERGE: preserve the original deterministic file order.
   - Write and re-read the merged file. Delete source files only after every
     source segment is represented exactly once in the output and the output
     preserves encoding, CRLF line endings, and source order.
   - Verify the resulting file inventory with
     `(Get-ChildItem -File -Path "<folder>").Count`.
3. **Update `doc/mod_merge_order_report.md`** with new consolidated
   filenames.

Phase 3 is complete only when every approved candidate passes the integrity
check before deletion and the merge-order report names every resulting file.

### Phase 4 -- Validation

1. **Duplicate key scan**: flag duplicate top-level keys in merged
   files (informational, not blocking).
2. **Quality gate**: run `& "tools/stellarisplus-quality-gate.ps1"`, repair
   findings, re-read changed files, and repeat until two consecutive runs are
   clean.
3. **Summary**:

   ```text
   Folders merged: N | Files removed: N | Files created: N
   Duplicate keys: <list or "none"> | Quality gate: pass/fail
   ```

Phase 4 is complete only when duplicate-key dispositions are recorded, both
final gate runs are clean, and the summary counts reconcile with Phase 3.

---

## Non-Candidates

- Files whose path exactly matches a vanilla file (engine uses mod
  copy only on exact filename match).
- `common/solar_system_initializers/` vanilla replacements (VEST
  precursor hook).
- `common/inline_scripts/` (always DUPL; filename = call target).
- `events/` files shadowing vanilla event IDs.
- FIOS `scripted_variables/` files with a `~~` fallback prefix; keep them
  separate from non-`~~` files.

When in doubt, check vanilla installation before treating a file as
renameable.

---

## Completion Criteria

The merge is complete only when every phase criterion is satisfied and the
final summary accounts for every scanned folder and approved candidate.
