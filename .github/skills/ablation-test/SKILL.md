---
name: ablation-test
description: 'Ablation test a hard bug to prove the smallest causal change set. Use when competing changes may explain a fix, results are intermittent, or the user needs a minimal proven repair.'
argument-hint: >-
  Optionally include the bug symptom, current changed files, and test constraints (restart needed, runtime cost, etc.)
---

# Ablation Test

## Contract

Change one variable per run and preserve the user's original working state. Use
[`EXAMPLES.md`](EXAMPLES.md) only when a concrete ablation pattern or test-log
template would help.

## Preconditions

Before running ablations:

1. Establish an observable PASS/FAIL test and reproduce the baseline state.
2. Record `git status --short`, the current branch and commit, all existing
   stashes, and untracked files.
3. Group changes by one causal hypothesis each.
4. Obtain explicit user approval before stashing, restoring, resetting,
   deleting, or dropping any working state.

Preconditions are complete only when the baseline is reproducible, every
candidate change belongs to a hypothesis group, and the original state has a
verified recovery path.

---

## Standard Workflow

### 1) Snapshot all current work

After approval, create a uniquely named stash with untracked files and capture
its immutable object ID immediately:

```powershell
git stash push -u -m "ablation-<bug>-full-wip"
$ablationStash = git rev-parse refs/stash
git stash show -u --name-status $ablationStash
```

Compare the stash manifest with the recorded working-tree manifest. Stop if any
path is missing. Never replace the captured object ID with a moving stash
selector after creation.

### 2) Build a minimal candidate set

Restore only the smallest likely fix group from the captured object ID:

```powershell
# tracked paths
git restore --source="$ablationStash" -- "<path-a>" "<path-b>"

# untracked paths (from stash third parent)
git restore --source="$ablationStash^3" -- "<new-file-a>" "<new-file-b>"
```

Run the target test and record the exact included paths, environment, restart
state, and PASS/FAIL result. This step is complete only when the run changes one
hypothesis dimension and is reproducible.

### 3) Narrow further by ablation

If PASS:

- remove one candidate file/group
- retest
- keep only what remains required

If FAIL:

- add back the next most likely group
- retest
- continue until PASS, then narrow again

Continue until removing any remaining candidate makes the test fail, or until
the evidence shows that the candidates interact and cannot be separated.

### 4) Validate hidden dependencies

When relevant, prove asset integrity and not just file presence:

- compare hashes against known-good upstream
- check load-order-sensitive files
- check if issue only appears after full process restart

Hidden-dependency validation is complete only when caching, restart needs,
generated files, and load-order effects relevant to the symptom have been
controlled or explicitly recorded as residual uncertainty.

### 5) Restore and finalize

Restore the exact original working state, then apply only the proven fix with
the user's approval. Verify `git status --short` against the original manifest.
Retain the stash by default; offer its exact object ID and let the user decide
whether to drop it.

## Output Requirements

After ablation, report:

1. **Root cause** (specific layer and file(s))
2. **Minimal required fix set**
3. **Changes proven unnecessary**
4. **Confidence level** and any residual uncertainty

Use concise evidence statements (test state -> result).

## Completion Criteria

The ablation is complete only when:

1. the same test distinguishes the failing and passing states;
2. every candidate group has evidence showing required, unnecessary, or
   inseparable status;
3. removing any claimed-required change makes the test fail;
4. the original worktree and all unrelated changes are accounted for;
5. the final report names the retained stash object, minimal fix, excluded
   changes, test evidence, and residual uncertainty.
