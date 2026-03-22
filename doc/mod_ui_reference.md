# StellarisPlus -- Mod / UI Reference

## Purpose & Scope

Covers BPV slot customization for end-users and compatibility guidance
for mod developers who want their custom districts and zones to
integrate with the StellarisPlus dynamic slot system.

---

## Naming Conventions

- BPV scripted variables follow `@BPV_UPPER_SNAKE_CASE` (e.g.
  `@BPV_CITY_SLOT`, `@BPV_ZONE_SLOT`, `@BPV_CITY_ZONES`).
- Inline script parameters use `$PARAM$` (e.g. `$GOVERNMENT$`,
  `$SLOT1$`).
- BPV inline script variants are suffixed by max slot count:
  `BPV_district_slots`, `BPV_district_slots2`, `BPV_district_slots4`,
  etc.

## Code Style

- Prefer referencing `@BPV_ZONE_SLOT` over hard-coding slot numbers.
- Keep `zone_slots` block entries one per line, sequential (`$SLOT1$`,
  `$SLOT2$`, ...).
- Always include `$GOVERNMENT$` as the first entry in a `zone_slots`
  block.

## Error Handling

- If `@BPV_ZONE_SLOT` is "not found" at runtime, the user likely does
  not have a BPV-related mod installed. Ship a fallback definition at
  lower priority (see Compatibility section below).
- Slot count mismatches (e.g. zones showing fewer buildings than
  expected) usually mean `@BPV_ZONE_SLOT` and
  `DEFAULT_MAX_PLANET_BUILDINGS_PER_ZONE` are out of sync.

## Testing

- After changing slot variables, launch the game and verify building
  slot counts on a planet view.
- Confirm auxiliary zone visibility matches `@BPV_CITY_ZONES`.
- Test with and without BPV-related mods to verify fallback behaviour.

---

## Customize Slot Counts

Open the file `common/scripted_variables/zz_bpv_defines.txt` and edit
the values to the right of the equals signs:

| Variable | Default | Description |
| --- | --- | --- |
| `@BPV_CITY_SLOT` | `24` | Building slots in the main city zone (central area of the city district) |
| `@BPV_ZONE_SLOT` | `6` | Building slots in other zones (specialized, generator, mining, agriculture) |
| `@BPV_CITY_ZONES` | `4` | Number of auxiliary zones in the main city district |

**Important**: The defaults above (24/6/4) reflect the StellarisPlus
integrated preset. If you install additional mods that define these
same variables with a later load-order prefix, their values will take
priority and may override your edits here.

### Changing Auxiliary Zone Building Slots

In addition to editing `@BPV_ZONE_SLOT`, open
`common/defines/zzzz_bpv_zone_slots_override.txt` and change the value
to the right of `DEFAULT_MAX_PLANET_BUILDINGS_PER_ZONE`. This defines
the default slot count for zones that do not have an explicitly forced
slot number. Some zones in the game (such as industrial zones) do not
have predefined slot numbers, so the game will use this value at
runtime.

### Changing Auxiliary Zone Count

In addition to editing `@BPV_CITY_ZONES`, open
`common/inline_scripts/districts/BPV_district_slots.txt` and modify
the code inside the curly braces. Add lines according to the rule, one
per auxiliary zone, until you reach the desired number.

```ParadoxScript
# Example: four auxiliary zones
zone_slots = {
 $GOVERNMENT$
 $SLOT1$
 $SLOT2$
 $SLOT3$
 $SLOT4$
}
```

- The first line `$GOVERNMENT$` represents the main zone (the
  government/central area). Do not remove it.
- Auxiliary zones must be added sequentially in the format `SLOT` +
  number, starting from `1`, one per line.
- This mod adjusts all vanilla districts to support up to 10 auxiliary
  zones. Extra entries beyond 10 will have no effect.
- Refer to the Stellaris modding documentation before increasing the
  limit further.

---

## Guide For Mod Developers (Compatibility)

### Make Custom Zones Support Dynamic Slot Numbers

The simplest approach is **not to set the `max_buildings` property**
when defining a zone. The game will use the global default slot value
at runtime. This mod overrides that global value with the number
chosen by the user, so your zone will automatically adapt.

If you **want to explicitly set this parameter**, reference the global
variable `@BPV_ZONE_SLOT` and use it for `max_buildings` or any other
logic.

**Fallback for users without BPV**: Copy
`common/scripted_variables/zz_bpv_defines.txt` into your own mod at a
**lower priority**. If the user does not have BPV installed, the
parameter will default to `3`, matching vanilla Stellaris behaviour.

### Make Custom Districts Support Dynamic Zone Numbers

Add the following after your original `zone_slots` definition:

```ParadoxScript
inline_script = {
    script = districts/BPV_district_slots
    GOVERNMENT = <main city zone type>
    SLOT1 = <first auxiliary zone type>
    ...
    SLOT10 = <tenth auxiliary zone type>
}
```

- The actual number of zones visible in-game depends on the **user's
  settings**. If the user sets 4 auxiliary zones, only `SLOT1`--`SLOT4`
  will appear.
- If you define fewer than 10 slots, the max shown will be limited to
  what you defined.

**Best practice**: Repeat the same zone type from `SLOT2` to `SLOT10`.
The second auxiliary zone will automatically repeat to match the user's
configured number. Vanilla city districts only support 2 auxiliary
zones by default; extra ones won't display without compatibility logic.

For city districts with only **2 auxiliary zones**, use this shorter
script:

```ParadoxScript
inline_script = {
    script = districts/BPV_district_slots2
    GOVERNMENT = <main city zone type>
    SLOT1 = <first auxiliary zone type>
    SLOT2 = <second auxiliary zone type, auto-repeat>
}
```

### Advanced Tips & Edge Cases

- If the user does not have this mod installed, the `inline_script`
  section will simply not execute (since the script file does not
  exist). The game will fall back to your original `zone_slots`
  definition, ensuring full compatibility.
- If you define more than two different auxiliary zone types, vanilla
  users may not see them unless you add extra compatibility logic.
- The `zone_slots` list must match corresponding district data in the
  game to function correctly.
