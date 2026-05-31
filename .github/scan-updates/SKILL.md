---
name: scan-updates
description: 'Scans integrated Workshop mods from credits.md, checks Steam for newer upstream update dates, updates only outdated mods, and validates/fixes quality gate issues after each update. Use when user says "scan updates", "check mod updates", "find outdated integrated mods", "refresh integrated mods", "update all outdated mods", or asks to compare credits.md entries against current Steam Workshop dates.'
argument-hint: >-
  Optional: "all" (default) or comma-separated Workshop IDs to limit scan scope
---

# Scan Integrated Mod Updates

## Purpose & Scope

Detect which already-integrated Workshop mods are outdated versus Steam,
then update only those mods one-by-one with validation after each update.

- Requires integrated mods to already exist in `credits.md`.
- Uses `credits.md` as the source of truth for managed Workshop IDs.
- Runs updates sequentially (never parallel) to keep merges auditable.

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
4. If page extraction fails, query by published file ID and use
   upstream update timestamp.
5. Compare:
   - If `steam_updated_date` > `local_last_updated`: mark **OUTDATED**.
   - Else: mark **CURRENT**.

If Steam date cannot be resolved after both methods, mark **UNKNOWN**
and do not auto-update.

---

## Update Execution Workflow

Process only `OUTDATED` mods, one at a time:

1. Invoke `/update-mod "<workshop-id>"`.
2. After update completes, run:

   ```powershell
   & "tools/stellarisplus-quality-gate.ps1"
   ```

3. If quality gate reports issues:
   - Fix all mod-owned errors introduced or exposed by the update.
   - Re-run quality gate.
   - Repeat until green or blocked by ambiguous ownership.
4. If blocked by ambiguous/conflicting intent, ask one concise user
   question and pause that mod only.
5. Continue to next outdated mod.

Never batch-update multiple mods in one merge pass.

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

---

## Decision Rules

| Situation | Rule |
| --------- | ---- |
| `steam_updated_date == local_last_updated` | Treat as CURRENT (no update) |
| Steam updated date is older than local | Treat as CURRENT and report anomaly |
| Steam page unavailable (429/5xx) | Retry with backoff, then fallback method |
| `update-mod` says no upstream changes | Mark as checked; do not force merge |
| Quality gate fails on pre-existing unrelated issues | Fix only issues in touched files; report remainder |
| More than 10 outdated mods | Process in deterministic ID order, reporting progress after each |

---

## Safety & Consistency

- Do not modify unrelated files while resolving update fallout.
- Preserve StellarisPlus load-order and naming conventions from
  `doc/mod_load_reference.md`.
- Keep `credits.md` accurate; if update changes mod identity metadata,
  refresh the affected entry.
- Use a single focused pass per mod: update -> quality gate -> fixes -> recheck.
