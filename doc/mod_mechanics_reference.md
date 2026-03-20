# StellarisPlus — Mod Mechanics Reference

This document is the consolidated reference for core gameplay/script
mechanics used by this mod.

---

## Core Mechanic: Dynamic Zone Slots

Slot counts are controlled via scripted variables:

- `@BPV_CITY_SLOT`, `@BPV_ZONE_SLOT`, `@BPV_CITY_ZONES`

Zones set building slots using these variables:

- `max_buildings = @BPV_CITY_SLOT` (main city/government zone)
- `max_buildings = @BPV_ZONE_SLOT` (other zones)

Districts generate `zone_slots` using inline scripts:

- `inline_script = { script = districts/BPV_district_slots
  GOVERNMENT = slot_city_government SLOT1 = slot_city_01 ... }`
- Variants exist for different max slot counts (`BPV_district_slots2/4/6/8`).
