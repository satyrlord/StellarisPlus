# Ablation Test Examples

## Example 1: Corrupted UI Icon (Asset-Level Root Cause)

### Example 1 Symptom

- Tooltip icon appears as static/noise.
- Script and localisation edits do not reliably fix it.

### Example 1 Candidate Groups

1. `interface/` sprite registrations
2. `common/` job/script edits
3. `localisation/` key overrides
4. `gfx/` icon textures (`.dds`)

### Example 1 Ablation Sequence

1. Stash full WIP (`git stash push -u -m "ablation-icon-full-wip"`).
2. Restore only groups 1-3 -> test -> **FAIL**.
3. Restore group 4 only -> test -> **PASS**.
4. Remove group 1-3 again while keeping group 4 -> test -> **PASS**.

### Example 1 Conclusion

- Root cause is in `gfx/` asset files.
- Minimal fix is replacing the bad `.dds` files.
- Script/localisation/sprite edits were unnecessary for this bug.

---

## Example 2: Override Not Taking Effect (Load-Order Root Cause)

### Example 2 Symptom

- New definition exists, but game still uses old behavior.
- No syntax errors in validator.

### Example 2 Candidate Groups

1. Object content changes
2. Filename prefix/order changes (`z_`, `zz_`, `zzzz_`)
3. Folder strategy change (LIOS/FIOS/DUPL)

### Example 2 Ablation Sequence

1. Stash full WIP.
2. Restore only content changes -> test -> **FAIL**.
3. Add load-order prefix/file placement changes -> test -> **PASS**.
4. Keep only ordering/folder strategy edits + minimal object body -> test.

### Example 2 Conclusion

- Root cause is load-order/folder semantics, not object logic.
- Final fix is minimal file placement/prefix correction.

---

## Example 3: Logic Regression Hidden by Broad Refactor

### Example 3 Symptom

- Feature previously worked.
- Large refactor touched many script blocks.

### Example 3 Candidate Groups

1. Trigger logic
2. Effect logic
3. Variable names/scopes
4. Formatting-only edits

### Example 3 Ablation Sequence

1. Stash all changes.
2. Restore trigger-only edits -> test.
3. Reset trigger edits; restore effect-only edits -> test.
4. Restore variable/scope edits -> test.
5. Exclude formatting-only edits throughout (control group).

### Example 3 Conclusion

- First group that flips FAIL -> PASS identifies regression source.
- Keep only minimal corrected logic; drop unrelated refactor noise.

---

## Reusable Test Log Template

```text
Run ID: AB-<date>-<index>
State:
- included files/groups:
- excluded files/groups:

Test:
- scenario/save:
- restart required: yes/no

Result:
- PASS/FAIL
- observed symptom:

Inference:
- what this run proves:
- next ablation step:
```

---

## Quick Triage Heuristics

- If binary assets changed and symptom is visual, test asset-only early.
- If content looks correct but behavior is unchanged, test load-order next.
- If behavior changed after broad cleanup, isolate by logic stage
  (triggers -> effects -> scope vars).
