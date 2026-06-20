---
description: Collect Stellaris logs and diagnose reported issues
---

# stellaris-log-fix

1. Run the log collection script to gather fresh logs into `tmp/_logs_inbox`:

   ```powershell
   & "tools/stellarisplus-collect-logs.ps1" -NoLaunch -IncludeException
   ```

   // turbo

2. Read the collected logs from `tmp/_logs_inbox/` -- prioritize `error.log`,
   then `exception.txt` (if present), then `game.log` and `setup.log`.

3. Identify errors, warnings, or anomalies related to StellarisPlus mod files. Cross-check against:
   - Vanilla/DLC files for expected behavior
   - `doc/mod_load_reference.md` for load-order conflicts
   - `doc/mod_mechanics_reference.md` and `doc/mod_ui_reference.md` for mechanics/UI issues
   - `doc/changelog.md` for recent changes that may have introduced the issue

4. Diagnose the root cause. If the issue is in a mod file, propose and implement a minimal fix.

5. After applying any fix, run the quality gate:

   ```powershell
   & "tools/stellarisplus-quality-gate.ps1"
   ```

   Fix any reported errors, then re-run to confirm clean output.

6. Summarize findings and any changes made to the user.
