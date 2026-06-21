# StellarisPlus — Original Features

New gameplay systems and mechanics designed and implemented specifically
for StellarisPlus (not integrated from external Workshop mods).

---

## 1. Machine Empire Food District Zone Retrofit

**Date:** 2026-06-21
**Status:** Implemented
**Files:** `common/zones/zz_sp_zones.txt`,
`common/zone_slots/zz_sp_specialization_unlocks.txt`

### Objective & Player-Facing Value

Allows machine empires to swap the zone inside a farming district's
`slot_food` for an energy or mineral production zone. The district
visually and functionally transforms into a generator or mining district
via the existing zone-swap UI — no demolishing, no rebuilding, no
terraforming.

### How It Works

1. Open the planet view and click the zone slot inside the food district
2. The zone selection menu shows two new machine-empire-only options:
   "Food → Energy" and "Food → Minerals"
3. Selecting one swaps the zone — the district icon changes to match
   the target type, jobs switch from agri-drones to technician/mining
   drones, and the economic category updates

### Design

**Decision: Zone-swap via `swap_type` instead of district conversion.**

The `convert_to` mechanic only activates during planet class changes.
The zone system's `swap_type` property changes the district visual and
economic category when a zone with a different swap_type is placed in
the slot. This is a live, in-game mechanic not tied to terraforming.

**Decision: Override `slot_food` unlock for machine empires.**

Vanilla `slot_food` requires `tech_food_processing_1`, anglers civic,
or agrarian idyll civic — none of which machine empires have. The
`slot_food` definition is overridden in `zz_sp_specialization_unlocks.txt`
(zone_slots/ is LIOS) to add `is_machine_empire = yes` as an unlock
condition.

**Decision: Use vanilla `jobs/technicians_add` and `jobs/miners_add`.**

These inline scripts already handle gestalt empires correctly, adding
`job_technician_drone` and `job_mining_drone` for machine empires.
No new job definitions needed.

### Zone Summary

| Zone | `swap_type` | Jobs | Unlock |
| --- | --- | --- | --- |
| `zone_sp_machine_food_energy` | `district_generator` | Technician drones (×2) | Machine empire, no tech gate |
| `zone_sp_machine_food_minerals` | `district_mining` | Mining drones (×2) | Machine empire, no tech gate |

### Non-Goals

- Does not change the district type at the engine level (still a
  `district_farming` internally — only the visual/economic category
  and jobs change via the zone).
- Does not affect non-machine empires (potential gated).
- Does not change vanilla zone behavior.

### Validation

```powershell
& "tools/stellarisplus-quality-gate.ps1"
```

### See Also

- `doc/changelog.md` — 2026-06-21
- Top-of-file comments in both modified files
