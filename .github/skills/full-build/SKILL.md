---
name: full-build
description: 'Full build the complete StellarisPlus release-validation sequence: quality gate, confirmed manual test, runtime log repair, and repair-authorized code review.'
argument-hint: >-
   Optionally specify focus areas or constraints, such as a feature to
   watch during manual testing or folders that changed.
---

# Full Build

## Purpose & Scope

Run the full StellarisPlus verification workflow in strict order. This
skill is an orchestrator -- it sequences the quality gate, manual
testing, log analysis, and code review, enforcing stop points and
iterating until all true mod-owned findings are resolved.

Create a TODO list for the run and preserve stage order.

---

## Workflow Stages

### Stage 1 -- Full Quality Gate

1. Run the canonical quality gate:

   ```powershell
   & "tools/stellarisplus-quality-gate.ps1"
   ```

2. Check the Problems view when that integration is available; otherwise report
   that the quality gate is the available diagnostic baseline.
3. Classify findings:
   - True mod-owned issue: fix it.
   - External noise or false positive: verify before dismissing.
   - Ambiguous ownership: confirm the referenced file exists in this
     workspace before editing.
4. Re-run the quality gate until all of the following are clean:
   - Validator findings: 0 errors, 0 warnings.
   - Pyright: 0 issues.
   - Markdownlint: 0 issues.
   - Problems view: no relevant errors.

Do not proceed to Stage 2 while Stage 1 is still failing.

### Stage 2 -- Manual Test Run (User Stop Gate)

1. Run `sptest`:

   ```powershell
   & "tools/stellarisplus-test.ps1" -Wait
   ```

2. When the test command returns, **stop**.
3. Ask the user for explicit confirmation that the manual testing
   session is over.
4. Do not collect or analyze logs until the user confirms.

This stage is mandatory. Do not continue automatically just because
the game process exited.

### Stage 3 -- Runtime Log Fix

1. Load and follow the `stellaris-log-fix` skill:
   `.github/skills/stellaris-log-fix/SKILL.md`
2. Continue until no actionable mod-owned runtime errors remain.

### Stage 4 -- Code Review and Cleanup

1. Load and follow the `stellaris-code-review` skill:
   `.github/skills/stellaris-code-review/SKILL.md`
2. Invoke its repair branch; this full-build request supplies explicit repair
   authorization for true mod-owned findings.
3. Review findings severity-first.
4. Fix all true-positive mod-owned errors and warnings.
5. Repeat until code review finds no remaining unresolved mod-owned
   errors or warnings.

---

## Decision Rules

| Situation | Rule |
| --------- | ---- |
| Stage order | Preserve strictly; do not skip ahead |
| After Stage 2 | Explicit user confirmation required |
| Vanilla/DLC behavior | Verify against official files; never speculate |
| Issue ownership | Only fix workspace-owned or credited mod issues |
| External noise | Document briefly and move on |
| User intent needed | Stop and ask one concise question |

---

## Completion Criteria

The full build is complete only when all of the following are true:

1. The quality gate is green.
2. The user explicitly confirmed completion of the manual test session and its
   result is recorded.
3. Runtime logs were collected and all actionable mod-owned errors
   were fixed.
4. Code review produced no remaining true mod-owned errors or
   warnings.
5. Two consecutive final quality-gate runs are clean.
6. The final report lists files changed, findings fixed, and any
   residual external noise or deferred items.

---

## Output Format

Report progress by stage:

| Stage | Result | Findings | Action |
| ----- | ------ | -------- | ------ |

End with a concise completion summary and any explicit blockers.
