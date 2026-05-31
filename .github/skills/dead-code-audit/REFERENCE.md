# Dead Code Audit Reference

## Deletion Standard

Delete a finding only when all of the following are true locally:

- no static references remain
- no framework entrypoint or config file needs it
- no dynamic lookup, reflection, or serialization contract relies on it
- no nearby test or generated artifact expects it

If any one of those points is unresolved, stop and report instead of deleting.

## False Positive Checklist

Treat a finding as alive when it is used through one of these paths:

- WinForms, XAML, or designer wiring
- WebView bridge payloads or string-routed API handlers
- JSON or XML serialization and deserialization contracts
- reflection, DI, `nameof`, or expression-tree access
- HTML, Vite, or tooling entry files
- test-only or fixture-only reachability that the scan intentionally excludes

## Reporting

Findings come first in the user-facing output. If cleanup was requested,
validate the deletion first and then report the validated deletion as the
finding before any summary.

Use this severity scale:

- `Critical` - blocks merge, violates a governing contract, or diverges from
  the user's stated intent
- `High` - must fix before ship
- `Medium` - should fix before ship
- `Low` - useful follow-up but not release-blocking

For each reported finding or false positive, include:

- the artifact that reported it
- the file and symbol when applicable
- the evidence that makes it dead or keeps it alive
- the smallest follow-up if config should be tightened later

If no live findings remain, say `No live dead-code findings`, list the scan
steps completed, and note verified false positives if any.

## Audit Validation

When you delete code, validate in this order before widening scope:

1. rerun `pwsh -File .\scripts\scan-dead-code.ps1`
2. run `get_errors` on edited files
3. run `dotnet build .\MixJam.Desktop\MixJam.Desktop.csproj -p:Platform=x64`
4. run focused tests when the deleted slice has them
5. run `markdownlint-cli2` on this skill file if you edited it

If any validation step fails, report the deletion attempt and the failed step,
stop further deletions, and leave the remaining findings unedited.
