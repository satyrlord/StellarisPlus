# StellarisPlus -- Load / Override Reference

This document describes load-order and override conventions used in
this workspace.

Companion planning report: [doc/mod_merge_order_report.md](mod_merge_order_report.md)

Source: Paradox Wiki "Modding" page, section "Overwriting specific
elements" > "Common folder" (verified against Stellaris v4.x).

---

## How The Engine Loads Files

Files within a folder are processed in **ASCIIbetical order** of the
filename (based on the ASCII character table, not plain alphabetical).
The practical sort order is:

    ! (33)  <  0-9 (48-57)  <  A-Z (65-90)  <  _ (95)  <  a-z (97-122)  <  ~ (126)

This means `A_foo.txt` sorts before `a_foo.txt`, digits sort before
all letters, and `~` sorts after everything else.

When two **separate mods** provide a file with the same name in the
same folder, the mod load order configured in the Paradox Launcher (or
Irony Mod Manager) determines which copy is used.  Within a single
mod (like StellarisPlus), only filename order matters.

---

## FIOS, LIOS, DUPL And MERGE

The engine uses four override strategies depending on the folder:

| Strategy | Meaning | Override approach |
| --- | --- | --- |
| **FIOS** | First In, Only Served | First definition of a keyed object wins; duplicates silently discarded. Use an early-sorting filename to win, or a late-sorting one (`~~`) for fallback defaults. |
| **LIOS** | Last In, Only Served | Last definition wins; earlier definitions are overridden. Use a late-sorting filename (`zz_`, `zzzz_`) to take final precedence. |
| **DUPL** | Duplicated | Both definitions coexist. Overriding a single entry is impossible; the whole file must be replaced with the same filename. |
| **MERGE** | Merged | New entries are merged into existing blocks with the same key. Existing entries inside a block cannot be removed or modified, only new ones added. |

---

## Per-Folder Load Behaviour (folders used by this mod)

### `common/` subfolders

| Folder | Type | Duplicate error | Notes |
| --- | --- | --- | --- |
| `agreement_term_values/` | LIOS | Object key already exists | |
| `armies/` | LIOS | Object key already exists | |
| `ascension_perks/` | LIOS | (none since v3.0) | |
| `buildings/` | LIOS (since v3.3) | Object key already exists | |
| `council_agendas/` | LIOS | Object key already exists | |
| `decisions/` | LIOS | Object key already exists | |
| `defines/` | **LIOS** | (none) | The enclosing block (e.g. `NGameplay = {}`) must be included. |
| `deposits/` | LIOS | Object key already exists | |
| `diplo_phrases/` | LIOS | Object key already exists | |
| `districts/` | LIOS (since v3.3) | Object key already exists | |
| `economic_categories/` | LIOS | Object key already exists | |
| `edicts/` | LIOS | Object key already exists | |
| `game_rules/` | LIOS | (none) | |
| `inline_scripts/` | **DUPL** | -- | Only works when the file is fully replaced with the same path. |
| `megastructures/` | LIOS | Object key already exists | |
| `name_lists/` | **DUPL** | -- | Duplicates coexist. |
| `on_actions/` | **MERGE** | (none) | Cannot modify existing entries; new entries with the same block name are merged. Load order is top-first for merged entries. |
| `opinion_modifiers/` | DUPL / LIOS | (none) | `add_opinion_modifier` usage is LIOS. |
| `policies/` | LIOS | Object key already exists | Existing key can be overridden with `NAME = {}`. |
| `pop_jobs/` | LIOS (since v3.3) | Object key already exists | |
| `portrait_categories/` | LIOS | Object key already exists | |
| `portrait_sets/` | LIOS | Object key already exists | |
| `random_names/` | LIOS | -- | |
| `script_values/` | LIOS | -- | |
| `scripted_loc/` | **FIOS** | (none) | First definition wins. Existing key can be overridden with `name = key`. |
| `scripted_modifiers/` | LIOS | Object key already exists | |
| `scripted_triggers/` | LIOS | Object key already exists | |
| `scripted_variables/` | **FIOS** | Variable name taken | First file to define a variable wins. Use `~~` prefix for fallback defaults. |
| `solar_system_initializers/` | **FIOS** | Initializer already exists | First definition wins. |
| `species_names/` | LIOS | -- | |
| `starbase_modules/` | LIOS | Object key already exists | |
| `static_modifiers/` | LIOS | (none) | |
| `strategic_resources/` | **DUPL** | (none) | Must replace the whole file with the same filename. |
| `technology/` | LIOS | Object key already exists | |
| `terraform/` | LIOS | Object key already exists | |
| `tradition_categories/` | LIOS | Object key already exists | |
| `traditions/` | LIOS | Object key already exists | |
| `traits/` | **DUPL / NO** | (none) | Entire file override only -- cannot override individual traits. |
| `zone_slots/` | LIOS | -- | (since v4.0) |
| `zones/` | LIOS | -- | (since v4.0) |

### Other top-level folders

| Folder | Type | Notes |
| --- | --- | --- |
| `events/` | **FIOS** | First definition of an event ID wins. The error log may make it look LIOS, but it is FIOS. |
| `interface/` (`.gfx`, `.gui`) | **LIOS** | Last definition wins. Use `zz_` prefix for UI overrides. |
| `localisation/` | **LIOS** | Last loaded key wins. Place override keys in `localisation/replace/` to guarantee they load after all other localisation files. |

---

## Filename Prefix Conventions

| Prefix | Sort position | Purpose / effect |
| --- | --- | --- |
| `07_`, `08_`, `99_` | After `0-9` | Ordered files that must precede lettered files |
| *(no prefix)* | After digits | Standard load order |
| `z_` | Near end | Late-loading override (e.g. `z_aar_defines.txt`) |
| `zz_` | After `z_` | Late-loading override (e.g. `zz_bpv_defines.txt`, `zz_longer_ship_names.txt`) |
| `zzzz_` | After `zzz_` | Very-late override for merged preset stacks (e.g. `zzzz_bpv_zone_slots_override.txt`, `zzzz_bpv_merged_overrides.txt`) |
| `~~` | After `z` (`~` is ASCII 126) | Fallback default in FIOS folders; loads last, yields to all earlier definitions when a fallback provider is needed |

In LIOS folders, later-sorting prefixes (`zz_`, `zzzz_`) guarantee
the override wins.  In FIOS folders, later-sorting prefixes (`~~`)
guarantee the definition acts as a fallback that yields to any earlier
definition.

---

## Naming Conventions For Integrated Mod Files

- `plentiful_traditions_*` -- Files from the Plentiful Traditions integration
- `MZ_*` -- Files from the More Zones integration
- `zz_bpv_*`, `zzzz_bpv_*` -- BPV Reborn slot system files
- `BPV_district_slots*` -- BPV inline script templates
- `PRA_*` -- Reworked Planetary Ascension files
- `zz_nson_*`, `00_nson_*` -- NoSkullOnlyNumber files
- `permanent_decisions_*` -- Permanent Decisions files
- `simpletraditions_*` -- Simple Traditions files

Preserve existing prefixes when editing.  Choose a prefix
intentionally when adding new override files.
