---
name: ablation-test
description: 'Ablation test: isolate the true root cause of a hard bug by systematically removing change sets until only the minimal fix remains. Use when a fix is unclear, multiple changes were made, the bug is intermittent, or the user asks which change actually fixed it, what was unnecessary, or for a minimal fix.'
argument-hint: >-
  Optionally include the bug symptom, current changed files, and test constraints (restart needed, runtime cost, etc.)
---

# Ablation Test

## Purpose & Scope

Use this skill to discover which exact change (or smallest change set)
actually fixes a bug when the path to a fix is uncertain.

This workflow is for cases where:

- many edits were made before success
- hypotheses keep changing
- logs do not clearly identify root cause
- you need a minimal, proven final fix

---

## Core Principles

- **One variable at a time**: each run should answer one question.
- **High-signal states**: test with sharply reduced change sets.
- **Stop when minimal fix is proven**: avoid overfitting extra edits.

---

## Preconditions

Before running ablations:

1. Confirm bug is reproducible (or verify known pass/fail state).
2. Gather current changed-file list (`git status --short`).
3. Group changes by hypothesis (assets, scripts, UI, localisation, etc.).
4. Note expensive test constraints (full restart required, long setup,
   save-file prerequisites).

---

## Standard Workflow

### 1) Snapshot all current work

Create a named stash with untracked files:

```powershell
git stash push -u -m "ablation-<bug>-full-wip"
```

This is your safety net for restoring any subset.

### 2) Build a minimal candidate set

Restore only the smallest likely fix group from the stash:

```powershell
# tracked paths
git restore --source="stash@{0}" -- "<path-a>" "<path-b>"

# untracked paths (from stash third parent)
git checkout "stash@{0}^3" -- "<new-file-a>" "<new-file-b>"
```

Run the target test and record result as **PASS** or **FAIL**.

### 3) Narrow further by ablation

If PASS:

- remove one candidate file/group
- retest
- keep only what remains required

If FAIL:

- add back the next most likely group
- retest
- continue until PASS, then narrow again

### 4) Validate hidden dependencies

When relevant, prove asset integrity and not just file presence:

- compare hashes against known-good upstream
- check load-order-sensitive files
- check if issue only appears after full process restart

### 5) Finalize minimal fix

Keep only proven required changes in working tree.
Drop temporary ablation stash once confidence is high.

---

## Interpretation Rules

- **PASS with tiny set** -> other edits are likely unnecessary.
- **FAIL with tiny set** -> at least one excluded group is required.
- **PASS only with one file type restored** -> root cause is in that
  layer (for example, texture asset corruption vs script logic).
- **Conflicting results** -> rerun from clean baseline; control for
  caching, stale runtime state, and restart requirements.

---

## Practical Patterns

- Start with **3-file hypothesis set**, then reduce to **1-file** or
  **1-layer** set.
- Prefer grouping by subsystem:
  - assets (`gfx/`, binaries)
  - script/data (`common/`)
  - UI registration (`interface/`)
  - text/localisation (`localisation/`)
- When binary assets are involved, run hash checks early.

---

## Command Snippets

```powershell
# show current change scope
git status --short

# inspect latest stashes
git stash list --max-count=5

# list files inside a stash snapshot
git stash show -u --name-only "stash@{0}"

# restore one file from stash
git restore --source="stash@{0}" -- "path/to/file"

# restore untracked file from stash
git checkout "stash@{0}^3" -- "path/to/new-file"

# remove a candidate file back to HEAD
git restore --source=HEAD --staged --worktree -- "path/to/file"

# drop finished ablation stash
git stash drop "stash@{0}"
```

---

## Output Requirements

After ablation, report:

1. **Root cause** (specific layer and file(s))
2. **Minimal required fix set**
3. **Changes proven unnecessary**
4. **Confidence level** and any residual uncertainty

Use concise evidence statements (test state -> result).

---

## Common Pitfalls

- Testing too many variables at once.
- Forgetting untracked files in stash/recovery.
- Assuming text/script caused an asset bug (or vice versa).
- Drawing conclusions without restarting when runtime caches apply.
- Keeping speculative edits after root cause is proven.
