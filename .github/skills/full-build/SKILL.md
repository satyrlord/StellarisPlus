---
name: full-build
description: 'Full build the complete StellarisPlus release-validation sequence: quality gate, confirmed manual test, runtime log repair, and repair-authorized code review.'
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
   - When Problems integration is available, no relevant Problems remain.

Stage 1 is complete only when the quality gate is green and every available
diagnostic is clean. Do not proceed to Stage 2 while this criterion is failing.

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

Stage 2 is complete only when the user explicitly confirms the manual session
ended and the test result is recorded.

### Stage 3 -- Runtime Log Fix

1. Load and follow the `stellaris-log-fix` skill:
   `.github/skills/stellaris-log-fix/SKILL.md`
2. Continue until no actionable mod-owned runtime errors remain.

Stage 3 is complete only when the invoked skill's completion criterion is met.

### Stage 4 -- Code Review and Cleanup

1. Load and follow the `stellaris-code-review` skill:
   `.github/skills/stellaris-code-review/SKILL.md`
2. Invoke its repair branch; this full-build request supplies explicit repair
   authorization for true mod-owned findings.

Stage 4 is complete only when the repair branch's completion criterion is met.

### Stage 5 -- Final Verification and Report

1. Run the canonical quality gate twice consecutively without intervening
   changes; both runs must be clean.
2. Re-read every file changed during the full build.
3. Report files changed, findings fixed, manual-test result, and any external
   noise or explicitly blocked item. Verify vanilla or DLC claims against the
   installed official files; ask one concise question when user intent is the
   only remaining blocker.

Stage 5 is complete only when both final runs are clean, every changed file has
been re-read, and the report accounts for every stage and blocker.

---

## Completion Criteria

The full build is complete only when every stage criterion is satisfied in
order and Stage 5 reports no unresolved true mod-owned finding.

---

## Output Format

Report progress by stage:

| Stage | Result | Findings | Action |
| ----- | ------ | -------- | ------ |

End with a concise completion summary and any explicit blockers.
