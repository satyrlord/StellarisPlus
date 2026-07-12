---
name: stellaris-log-fix
description: 'Log fix explicitly requested Stellaris runtime diagnostics by collecting or analyzing logs and repairing mod-owned errors. Do not collect logs when the user only describes a symptom; ask first.'
---

# Stellaris Log Fix

## Purpose & Scope

Collect Stellaris runtime logs, classify errors by ownership, and
auto-fix mod-owned issues. Use after a test run when the user asks to
check logs or fix errors.

- Logs are collected into `tmp/_logs_inbox/`.

---

## Log Fix Workflow

### 1. Establish log source

If the user supplied logs, analyze those files without recollecting. Otherwise,
collect only when the user explicitly requested log collection, `spcollect`, or
this log-fix workflow:

```powershell
& "tools/stellarisplus-collect-logs.ps1" -NoLaunch -IncludeException
```

Copies `error.log`, `game.log`, `debug.log`, `setup.log`,
`system.log`, `time.log` into `tmp/_logs_inbox/`.
Run `spcollect` only when the user explicitly asks for that command. Do not omit
`-NoLaunch` unless the user explicitly requests a launched test cycle.

Step 1 is complete only when the selected log files exist, are readable, and
their supplied or collected origin is recorded.

### 2. Parse error log

Parse the complete error log selected in Step 1 and group multi-line entries.
Load `.github\skills\stellaris-log-fix\references\error-patterns.md`; it is the
sole authority for ownership, categories, skip rules, and fix strategies.

Step 2 is complete only when every physical log line belongs to one parsed
entry or is explicitly recorded as unparsed.

### 3. Classify each error

Apply the reference's ownership rule first, then assign each parsed entry one
category and disposition. Step 3 is complete only when every entry has both.

### 4. Fix each mod-owned error

Apply the reference's matching fix strategy to the root cause, not cascading
symptoms. Read the complete owning file before editing and re-read it after the
change. Step 4 is complete only when every mod-owned root cause is repaired with
evidence or explicitly blocked.

### 5. Scan game log

Scan the game log selected in Step 1 for `Error`, `Warning`, `FAIL`,
`assert` (skip galaxy generation noise). Apply the same
classify-and-fix workflow.

Step 5 is complete only when every relevant game-log entry has the same
ownership, category, disposition, and root-cause accounting as Step 3.

### 6. Run quality gate

```powershell
& "tools/stellarisplus-quality-gate.ps1"
```

Fix all reported mod-owned issues, re-read every changed file, check available
Problems diagnostics, and repeat until two consecutive runs are clean.

### 7. Report summary

| # | Error | File | Action |
|---|-------|------|--------|

Group skipped errors by category with counts.

Step 7 is complete only when every parsed error and relevant game-log entry
appears once in the table or one skipped-category count, and unresolved entries
include evidence and a blocker.

## Completion Criteria

Log fix is complete only when every step criterion is satisfied and the final
report reconciles with the parsed entry count and both clean gate runs.
