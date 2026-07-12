---
name: scan-updates
description: 'Scan integrated Workshop mods against live Steam metadata and update only entries proven outdated.'
---

# Scan Integrated Mod Updates

## Purpose & Scope

Detect which already-integrated Workshop mods are outdated versus Steam, then
invoke `update-mod` only for entries proven OUTDATED.

- Requires integrated mods to already exist in `credits.md`.
- Uses `credits.md` as the source of truth for managed Workshop IDs.

---

## Inputs

- Primary input file: `credits.md`.
- Optional user filter: one or more Workshop IDs to scan.
- Steam metadata source:
  - Use each entry's `Workshop:` URL from `credits.md`.
  - If scraping fails, fall back to Steam published file details by ID.

---

## Parsing Rules (`credits.md`)

Build one record per integrated mod:

| Field | Parse rule |
| ----- | ---------- |
| `id` | Required. Extract digits from `Workshop ID: <id>` |
| `name` | Bullet title text for that record |
| `local_last_updated` | Parse `Last updated: YYYY-MM-DD` |
| `workshop_url` | Parse `Workshop: <https://...id=<id>>`; if missing, synthesize URL from `id` |

Parsing robustness requirements:

1. Treat a mod entry as complete only when `id` and `local_last_updated`
   are both present.
2. Support wrapped titles (name can span multiple physical lines).
3. Skip malformed entries and report them separately.

---

## Steam Date Check Workflow

For each parsed mod record:

1. Fetch the Workshop page listed in `workshop_url`.
2. Extract the page's **Updated** date (not Created date).
3. Normalize to `YYYY-MM-DD` in local timezone.
4. If page extraction fails, retry at most three times with exponential backoff,
   then query live published-file metadata by ID and use its upstream update
   timestamp. If neither live source is accessible, do not infer a date from the
   local Workshop folder.
5. Compare:
   - If `steam_updated_date` > `local_last_updated`: mark **OUTDATED**.
   - If the dates are equal: mark **CURRENT**.
   - If the Steam date is older: mark **CURRENT** and report the anomaly.

If Steam date cannot be resolved after both methods, mark **UNKNOWN**
and do not auto-update.

The date check is complete only when every valid in-scope ID is CURRENT,
OUTDATED, or UNKNOWN with the live evidence or failure record that produced the
classification.

---

## Update Execution Workflow

Process only `OUTDATED` mods, one at a time; when more than ten are outdated,
use deterministic Workshop-ID order and report progress after each:

1. Load and follow `.github/skills/update-mod/SKILL.md` for the Workshop ID.
2. Record the invoked skill's two final quality-gate runs instead of duplicating
   its validation workflow.
3. If `update-mod` reports no upstream changes, mark the entry checked and do
   not force a merge.
4. If a gate failure belongs to unrelated user work that cannot be repaired
   without expanding scope, mark the update BLOCKED and ask one concise user
   question; never report that update complete with a failing gate.
5. Continue only after the current ID is complete or explicitly blocked.

Update execution is complete only when every OUTDATED ID has an `update-mod`
completion record or an evidenced BLOCKED disposition.

---

## Required Output

Provide three concise tables:

1. **Scan Results**

   | Mod | ID | Local date | Steam date | Status |
   | --- | -- | ---------- | ---------- | ------ |

2. **Update Actions**

   | ID | Action | Result |
   | -- | ------ | ------ |

3. **Validation Results**

   | ID | Quality gate runs | Final status | Notes |
   | -- | ----------------- | ------------ | ----- |

Also list:

- malformed `credits.md` entries skipped
- mods with unresolved Steam dates (`UNKNOWN`)
- any manual decisions still needed

## Completion Criteria

The scan is complete only when the date-check and update-execution criteria are
satisfied; malformed and UNKNOWN entries are reported without mutation;
credits metadata is current; and all three required output tables account for
every in-scope ID and both gate runs for each completed update.
