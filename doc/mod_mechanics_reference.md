# StellarisPlus — Mod Mechanics Reference

This document is the consolidated reference for core gameplay/script
mechanics used by this mod.

---

## Core Mechanic: Dynamic Zone Slots (BPV Reborn)

Slot counts are controlled via scripted variables defined in
`common/scripted_variables/zz_bpv_defines.txt`:

- `@BPV_CITY_SLOT = 24` — building slots in the main city/government zone
- `@BPV_ZONE_SLOT = 6` — building slots in all other zones
- `@BPV_CITY_ZONES = 4` — number of auxiliary zones in the main city district

The engine default for zone slot counts is additionally overridden in
`common/defines/zzzz_bpv_zone_slots_override.txt`:

- `NGameplay.DEFAULT_MAX_PLANET_BUILDINGS_PER_ZONE = 6`

Zones set building slots using these variables:

- `max_buildings = @BPV_CITY_SLOT` (main city/government zone)
- `max_buildings = @BPV_ZONE_SLOT` (other zones)

Districts generate `zone_slots` using inline scripts:

- Districts pass `GOVERNMENT` + `SLOT1`–`SLOT10` parameters to
  `inline_script = { script = districts/BPV_district_slots ... }`
- Variants exist for different max slot counts (`BPV_district_slots2/4/6/8`).

Third-party compatibility variables from the integrated BPV presets are kept in
`common/scripted_variables/zzzz_bpv_merged_overrides.txt` (`@KZ_VOY_default_bs`,
`@ag_num_zone_buildings`, `@KZ_VOY_zone_fake_bs`).

---

## Core Mechanic: Expanded Traditions (Plentiful Traditions)

Plentiful Traditions expands the tradition system with many additional
tradition trees. The mod raises the maximum number of tradition trees
via a paired constant:

- `NGameplay.TRADITION_CATEGORIES_MAX = 24` in `common/defines/plentiful_traditions_defines.txt`
- `@max_tradition_trees = 24` in `common/scripted_variables/07_scripted_variables_machine_age.txt`

These two values must be kept in sync whenever the tradition tree count changes.

Other key defines in `common/defines/plentiful_traditions_defines.txt`:

- `NGameplay.ASCENSION_PERKS_SLOTS = 48` — maximum ascension perk slots
- `NGameplay.EMPIRE_SIZE_TRADITION_COST_PENALTY = 0.002` —
  empire size scaling for tradition costs
- `NGameplay.TRADITION_COST_TRADITION = 6` — per-tradition cost tuning
- `NGameplay.TRADITION_COST_TRADITION_EXP = 1.600` — per-tradition cost exponent
- `NGameplay.TRADITION_COST_MULT_TRADITION_GROUP = 0.001` — per-group cost multiplier
- `NEconomy.TRADITION_COST_RESOURCES = { "unity" }` — tradition cost resource type
- `NEconomy.TRADITION_COST_AMOUNTS = { 265 }` — tradition base cost (unity)
- `NAI.NUM_TRADITIONS_FOR_EDICTS = 150` — AI delay for unity edicts

Tradition content files live under `common/traditions/` and `common/tradition_categories/`.
Events for tradition effects are in `events/plentiful_traditions_*.txt`.

---

## Core Mechanic: More Zones (District Specializations)

More Zones adds new specialization zone types that can appear in districts
via district-swap events.

Zone types added:

- Medical / Genomic Specialization (`zone_MZ_medical`,
  plus arcology and ring-world variants)
- Enforcer Hub (`zone_MZ_enforcer`, plus variants)
- Telepath Spire (`zone_MZ_telepath`, plus variants)
- Patrol Drone Hub (`zone_MZ_patrol`, plus variants)
- Dual-research zones: Physics/Society,
  Society/Engineering, Engineering/Physics (plus variants)
- Elite zone (`zone_MZ_elite`)
- Urban support zones: Energy/Minerals, Minerals/Food, Food/Energy, Basic (`zone_MZ_urban_*`)
- Origin-specific zones: Payback, Starlit Citadel, Default, Primal Calling

In total, 30 `zone_MZ_*` definitions across four files, most with
arcology and ring-world variants.

Zone definitions live in `common/zones/more_zones_*.txt`.
Shared job/effect fragments are in `common/inline_scripts/more_zones/`.
District-swap logic is in `events/MZ_events.txt`.
BPV compatibility is handled directly by
`common/scripted_variables/zz_bpv_defines.txt`, which sets
`@BPV_compatibility_load = 1`. StellarisPlus ships with BPV integrated,
so the old no-BPV fallback variable file is no longer needed.

---

## Core Mechanic: Simple Traditions

Simple Traditions adds a small set of additional tradition trees focused
on role-play flavour.
Content files are integrated alongside Plentiful Traditions content:

- `events/simpletraditions_events.txt`
- `interface/simpletraditions.gfx`
- `localisation/simple_traditions_l_english.yml`

---

## Integrated Mod: Reworked Planetary Ascension

Reworked Planetary Ascension overhauls the planetary ascension system
with new jobs, scripted modifiers, and UI elements.

Content files (prefixed `PRA_`):

- `common/pop_jobs/PRA_jobs.txt` — Custom jobs
- `common/script_values/PRA_sv.txt` — Script value computations
- `common/scripted_loc/PRA_sloc.txt` — Scripted localisation
- `common/scripted_modifiers/PRA_smod.txt` — Scripted modifiers
- `interface/PRA_ui_MISC.gfx` — UI sprite definitions

---

## Integrated Mod: NoSkullOnlyNumber

Removes skull icons from fleet power displays and replaces them with
numeric values. Runs via a yearly pulse event.

Content files:

- `common/on_actions/00_nson_on_actions.txt` — Yearly pulse hook
- `events/zz_nson_events.txt` — Fleet iteration event

---

## Integrated Mod: Permanent Decisions

Adds permanent planet decisions for Encourage Planetary Growth and
Distribute Luxury Goods, with hidden deposit-based upkeep scaling.

Content files:

- `common/decisions/permanent_decisions_resource_decisions.txt` — Decision definitions
- `common/deposits/permanent_decisions_deposits.txt` — Hidden deposits for upkeep
- `events/permanent_decisions_events.txt` — Periodic update events
- `localisation/english/permanent_decisions_l_english.yml` — Localisation

---

## Integrated Mod: Longer Ship Names

Increases the maximum length of generated ship names via an engine
define override.

Content files:

- `common/defines/zz_longer_ship_names.txt` — Ship name length define
