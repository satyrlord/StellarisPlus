---
name: dead-code-audit
description: 'Runs the deterministic MixJam dead-code scan, triages findings into live dead code or false positives, and optionally removes provably dead code with focused validation. Use when the user asks for a dead-code scan, unused-code audit, orphan-file scan, unused-export triage, or cleanup from scan findings.'
---

# Dead Code Audit

## Purpose & Scope

Run the deterministic repo dead-code scan, inspect only the reported
artifacts, and either:

- report live findings and validated false positives, or
- remove provably dead code when the user explicitly asked for cleanup.

Use this skill for dead-code work only. Use `stellaris-code-review` for ordinary
review, security review, performance review, or merge-readiness review.

## Read First

1. `AGENTS.md`
2. `docs/implementation-roadmap-and-acceptance.md`
3. `.github/rules/quality-gate.instructions.md`
4. `tmp/dead-code-scan/summary.json` after running the scan command

## Command

Run this command from the repository root:

```powershell
pwsh -File .\scripts\scan-dead-code.ps1
```

If the command fails, `summary.json` is missing, or the artifacts cannot be
written, report the exact failure and stop. Do not rely on stale artifacts and
do not delete anything.

The command writes fresh artifacts to `tmp/dead-code-scan/`:

- `summary.json` - top-level status and per-step counts
- `summary.txt` - human-readable overview
- `csharp-report.json` - Roslyn and `dotnet format` dead-code diagnostics
- `frontend-tsc-deadcode.log` - TypeScript unused and unreachable diagnostics
- `frontend-unused-exports.json` - filtered `ts-prune` export findings
- `frontend-knip-files.json` - Knip orphan-file findings
- matching `*.log` files for raw tool output

## Workflow

1. Run the scan command and wait for all steps to complete.
2. Read `tmp/dead-code-scan/summary.json` first.
3. Inspect only the raw artifact or artifacts for steps that reported issues.
4. For each finding, gather the smallest local proof before editing:
   - direct imports or usages
   - entrypoint wiring from HTML, Vite, or desktop bridge glue
   - reflection, serialization, XAML, or WebView message binding
   - tests or generated code that rely on the symbol or file
5. If the request is audit-only, report findings without editing.
6. If the request includes cleanup and the finding meets the Deletion
   Standard, delete the smallest slice that removes it.
7. After each deletion, run Audit Validation before widening scope.
8. If a finding is a false positive, report the concrete reason and suggest the
   narrowest suppression or config refinement only when the same false positive
   is likely to recur.

## Deep Reference

Use [REFERENCE.md](REFERENCE.md) for the Deletion Standard, False Positive
Checklist, Reporting contract, and Audit Validation steps.
