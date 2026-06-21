# StellarisPlus -- Mod Mechanics Reference

## Purpose & Scope

Consolidated reference for core gameplay and script mechanics used by
StellarisPlus. Use this document when modifying integrated systems,
debugging cross-mod interactions, or verifying define/variable
relationships.

---

## Dependency: UI Overhaul Dynamic (ID 1623423360)

UI Overhaul Dynamic is a **required external dependency** -- it is not
integrated into the mod folder, but StellarisPlus expects it at runtime.

- **Why:** Our Planet View tab overrides in `interface/zz_planet_view.gui`
  reference UIOD-specific sprite names (`GFX_ui_tab_1_long_*`,
  `GFX_ui_tab_2_long_*`) and use UIOD's tab spacing coordinates.
- **Load order:** StellarisPlus must load *after* UIOD to override the
  tab definitions with the correct sprites.
- **Enforcement:** The `descriptor.mod` should list UIOD in
  `dependencies = { ... }` (Workshop ID 1623423360).

---

## Naming Conventions

- Scripted variables follow `@UPPER_SNAKE_CASE` (e.g.
  `@BPV_CITY_SLOT`, `@max_tradition_trees`).
- Integrated-mod files keep their upstream prefix (e.g. `PRA_`,
  `MZ_`, `zz_bpv_`). See `doc/mod_load_reference.md` for the full
  prefix table.
- Inline script parameters use `$PARAM$`.

## Code Style

- Paired constants (e.g. `TRADITION_CATEGORIES_MAX` and
  `@max_tradition_trees`) must always be updated together.
- When a mechanic spans defines, scripted variables, and inline
  scripts, keep all three in sync.
- Prefer referencing `@BPV_ZONE_SLOT` over hard-coding slot counts.

## Error Handling

- If a scripted variable is "not found", check whether another mod's
  file sorts earlier in a FIOS folder and claims the name first.
- Zone slot mismatches at runtime usually mean `@BPV_ZONE_SLOT` and
  `DEFAULT_MAX_PLANET_BUILDINGS_PER_ZONE` are out of sync.

## Testing

- After changing any define or scripted variable listed below, verify
  that its paired value is also updated.
- Cross-check tradition tree count changes against both
  `TRADITION_CATEGORIES_MAX` and `@max_tradition_trees`.

## Security

- Do not expose Workshop IDs, API keys, or credentials inside any
  script file.
- Integrated mods must be credited in `credits.md`.

---

## Core Mechanic: Dynamic Zone Slots (BPV Reborn)

Slot counts are controlled via scripted variables defined in
`common/scripted_variables/zz_bpv_defines.txt`:

- `@BPV_CITY_SLOT = 24` -- building slots in the main city/government zone
- `@BPV_ZONE_SLOT = 6` -- building slots in all other zones
- `@BPV_CITY_ZONES = 4` -- number of auxiliary zones in the main city district

The engine default for zone slot counts is additionally overridden in
`common/defines/zzzz_bpv_zone_slots_override.txt`:

- `NGameplay.DEFAULT_MAX_PLANET_BUILDINGS_PER_ZONE = 6`

Zones set building slots using these variables:

- `max_buildings = @BPV_CITY_SLOT` (main city/government zone)
- `max_buildings = @BPV_ZONE_SLOT` (other zones)

Districts generate `zone_slots` using inline scripts:

- Districts pass `GOVERNMENT` + `SLOT1`--`SLOT10` parameters to
  `inline_script = { script = districts/BPV_district_slots ... }`
- Variants exist for different max slot counts (`BPV_district_slots2/4/6/8`).

Third-party compatibility variables from the integrated BPV presets are
kept in `common/scripted_variables/zzzz_bpv_merged_overrides.txt`
(`@KZ_VOY_default_bs`, `@ag_num_zone_buildings`, `@KZ_VOY_zone_fake_bs`).

---

## Core Mechanic: Expanded Traditions (Plentiful Traditions)

Plentiful Traditions expands the tradition system with many additional
tradition trees. The mod raises the maximum number of tradition trees
via a paired constant:

- `NGameplay.TRADITION_CATEGORIES_MAX = 24` in
  `common/defines/plentiful_traditions_defines.txt`
- `@max_tradition_trees = 24` in
  `common/scripted_variables/07_scripted_variables_machine_age.txt`

These two values **must be kept in sync** whenever the tradition tree
count changes.

Other key defines in `common/defines/plentiful_traditions_defines.txt`:

| Define | Value | Description |
| --- | --- | --- |
| `NGameplay.ASCENSION_PERKS_SLOTS` | `48` | Maximum ascension perk slots |
| `NGameplay.EMPIRE_SIZE_TRADITION_COST_PENALTY` | `0.002` | Empire size scaling for tradition costs |
| `NGameplay.TRADITION_COST_TRADITION` | `6` | Per-tradition cost tuning |
| `NGameplay.TRADITION_COST_TRADITION_EXP` | `1.600` | Per-tradition cost exponent |
| `NGameplay.TRADITION_COST_MULT_TRADITION_GROUP` | `0.001` | Per-group cost multiplier |
| `NEconomy.TRADITION_COST_RESOURCES` | `{ "unity" }` | Tradition cost resource type |
| `NEconomy.TRADITION_COST_AMOUNTS` | `{ 265 }` | Tradition base cost (unity) |
| `NAI.NUM_TRADITIONS_FOR_EDICTS` | `150` | AI delay for unity edicts |

Tradition content files live under `common/traditions/` and
`common/tradition_categories/`.
Events for tradition effects are in `events/plentiful_traditions_*.txt`.

---

## Core Mechanic: More Zones (District Specializations)

More Zones adds new specialization zone types that can appear in
districts via district-swap events.

### Zone Types Added

- Medical / Genomic Specialization (`zone_MZ_medical`, plus arcology
  and ring-world variants)
- Enforcer Hub (`zone_MZ_enforcer`, plus variants)
- Telepath Spire (`zone_MZ_telepath`, plus variants)
- Patrol Drone Hub (`zone_MZ_patrol`, plus variants)
- Dual-research zones: Physics/Society, Society/Engineering,
  Engineering/Physics (plus variants)
- Elite zone (`zone_MZ_elite`)
- Urban support zones: Energy/Minerals, Minerals/Food, Food/Energy,
  Basic (`zone_MZ_urban_*`)
- Origin-specific zones: Payback, Starlit Citadel, Default, Primal
  Calling

In total, 30 `zone_MZ_*` definitions across four files, most with
arcology and ring-world variants.

### Key Files

- Zone definitions: `common/zones/more_zones_*.txt`
- Shared job/effect fragments: `common/inline_scripts/more_zones/`
- District-swap logic: `events/MZ_events.txt`
- BPV compatibility: `common/scripted_variables/zz_bpv_defines.txt`
  (sets `@BPV_compatibility_load = 1`). StellarisPlus ships with BPV
  integrated, so the old no-BPV fallback variable file is no longer
  needed.

---

## Core Mechanic: Simple Traditions

Simple Traditions adds a small set of additional tradition trees
focused on role-play flavour.

Content files are integrated alongside Plentiful Traditions content:

- `events/simpletraditions_events.txt`
- `interface/simpletraditions.gfx`
- `localisation/simple_traditions_l_english.yml`

---

## Integrated Mod: Reworked Planetary Ascension

Reworked Planetary Ascension overhauls the planetary ascension system
with new jobs, scripted modifiers, and UI elements.

Content files (prefixed `PRA_`):

- `common/pop_jobs/PRA_jobs.txt` -- Custom jobs
- `common/script_values/PRA_sv.txt` -- Script value computations
- `common/scripted_loc/PRA_sloc.txt` -- Scripted localisation
- `common/scripted_modifiers/PRA_smod.txt` -- Scripted modifiers
- `interface/PRA_ui_MISC.gfx` -- UI sprite definitions

---

## Integrated Mod: Permanent Decisions

Adds permanent planet decisions for Encourage Planetary Growth and
Distribute Luxury Goods, with hidden deposit-based upkeep scaling.

Content files:

- `common/decisions/permanent_decisions_resource_decisions.txt` --
  Decision definitions
- `common/deposits/permanent_decisions_deposits.txt` -- Hidden
  deposits for upkeep
- `events/permanent_decisions_events.txt` -- Periodic update events
- `localisation/english/permanent_decisions_l_english.yml` --
  Localisation

---

## Integrated Mod: Longer Ship Names

Increases the maximum length of generated ship names via an engine
define override.

Content files:

- `common/defines/zz_longer_ship_names.txt` -- Ship name length define
