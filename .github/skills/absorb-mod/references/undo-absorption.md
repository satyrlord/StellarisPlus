# Undo Absorption

Use this branch only to reverse a mod already credited as absorbed. Preserve
`backup/<id>/` unless the user separately authorizes its deletion.

## 1. Identify and Plan

1. Match the Workshop ID or mod name against `credits.md` and verify that
   `backup/<id>/` exists.
2. Build a removal manifest from the immutable absorption backup:

   | Situation | Action |
   | --- | --- |
   | Direct copy, unchanged since absorption | Delete |
   | Direct copy, subsequently modified | Review and preserve unrelated edits |
   | Content merged into a shared file | Remove only the absorbed blocks or keys |
   | Binary asset unique to the absorbed mod | Delete |
   | Content shared with another absorbed mod | Retain and record the dependency |

3. Trace every manifest item to current consumers and present the manifest for
   user approval.

Planning is complete only when every backup item has a proposed disposition,
every current dependency is recorded, and the user approves the manifest.

## 2. Remove

1. Remove approved direct-copy files and empty parent directories.
2. Remove only the absorbed blocks or keys from shared files, validating brace
   balance and neighbouring scope after each edit.
3. Remove or repair absorbed-only localisation, GFX, event-hook, variable, and
   asset references.
4. Remove the `credits.md` entry. Preserve shared content and record why it
   remains.

Removal is complete only when every manifest item is removed, retained with an
evidenced dependency, or explicitly blocked, and no absorbed-only reference
remains.

## 3. Validate and Report

1. Re-read every changed file.
2. Run `tools/stellarisplus-quality-gate.ps1`, repair findings, and repeat until
   two consecutive runs are clean.
3. Report every manifest disposition, retained dependency, changed file,
   validation result, and blocker.
4. Offer deletion of `backup/<id>/` only as a separate, explicitly confirmed
   action after the report is complete.

Undo is complete only when removal and validation criteria are satisfied,
credits are accurate, and the immutable backup is preserved unless its deletion
was separately authorized.
