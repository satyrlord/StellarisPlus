---
name: stellaris-log-fix
description: >-
   Collect Stellaris runtime logs, analyze errors, and automatically fix
   mod issues. USE WHEN: user says 'fix errors', 'check logs', 'analyze
   logs', 'spcollect', 'log fix', 'runtime errors', 'error log', or
   wants to debug Stellaris mod issues after a test run.
argument-hint: >-
   Optionally describe specific errors or symptoms to focus on
---

# Stellaris Log Fix

## Purpose & Scope

Collect Stellaris runtime logs, classify errors by ownership, and
auto-fix mod-owned issues. Use after a test run when the user asks to
check logs or fix errors.

- Error classification rules: `references/error-patterns.md`.
- Logs are collected into `tmp/_logs_inbox/`.

---

## Error Handling

- **Ownership rule**: only fix errors referencing files in this
  workspace or assets from integrated mods in `credits.md` (Workshop
  content at
  `C:\Program Files (x86)\Steam\steamapps\workshop\content\281990\<id>\`).
- **Vanilla error, no mod override**: skip unless user asks to create
  override.
- **Ambiguous ownership**: check if file exists in workspace before
  fixing.
- **Cascading errors**: fix at root cause, not each symptom.

## Testing

- Run `& "tools/stellarisplus-quality-gate.ps1"` after all fixes.
- Track each fix in TODO list.

---

## Log Fix Workflow

### 1. Collect logs

```powershell
& "tools/stellarisplus-collect-logs.ps1" -NoLaunch
```

Copies `error.log`, `game.log`, `debug.log`, `setup.log`,
`system.log`, `time.log` into `tmp/_logs_inbox/`.
Omit `-NoLaunch` if user wants a full test cycle.

### 2. Parse error log

Parse `tmp/_logs_inbox/error.log` -- group multi-line entries.
Load `.github\skills\stellaris-log-fix\references\error-patterns.md`
for classification rules.

### 3. Classify each error

| Category | Action |
| -------- | ------ |
| Intentional Override | Skip |
| External Mod Noise | Skip |
| Duplicate Texture (INFO) | Report only |
| Missing Sound Category | Auto-fix |
| Script Error | Auto-fix |
| Missing Localisation | Auto-fix |
| Missing GFX/Sprite | Auto-fix |
| Missing File/Asset | Investigate and report |

### 4. Fix each mod-owned error

- Read referenced file with 20+ lines context around the error.
- Script errors: fix scope, syntax, conditions.
- Missing localisation: add key to `localisation/*_l_english.yml`.
- Missing GFX: add sprite to appropriate `.gfx` in `interface/`.

### 5. Scan game log

Scan `tmp/_logs_inbox/game.log` for `Error`, `Warning`, `FAIL`,
`assert` (skip galaxy generation noise). Apply the same
classify-and-fix workflow.

### 6. Run quality gate

```powershell
& "tools/stellarisplus-quality-gate.ps1"
```

### 7. Report summary

| # | Error | File | Action |
|---|-------|------|--------|

Group skipped errors by category with counts.

---

## Decision Rules

| Situation | Rule |
| --------- | ---- |
| Vanilla error, no mod override | Skip unless user asks to create override |
| Ambiguous ownership | Check if file exists in workspace before fixing |
| Cascading errors | Fix at root cause, not each symptom |
