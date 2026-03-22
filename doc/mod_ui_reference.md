# StellarisPlus — Mod / UI Reference

This document covers BPV slot customization for end-users and
compatibility guidance for mod developers.

---

## Customize Slot Counts

If the preset slot numbers provided on the Workshop do not meet your
needs, you can customize them as follows:

Open the file `common/scripted_variables/zz_bpv_defines.txt` and edit the
values to the right of the equals signs. Specifically:

`@BPV_CITY_SLOT` — The number of building slots in the main city zone
(the central area of the city district). Default: `24`

`@BPV_ZONE_SLOT` — The number of building slots in other zones,
including the specialized zones to the right of the city district, as
well as other districts (such as generator, mining, and agriculture).
Default: `6`

`@BPV_CITY_ZONES` — The number of auxiliary zones in the main city
district. Default: `4`

**Important**: The defaults above (24/6/4) reflect the StellarisPlus integrated
preset. If you install additional mods that define these same variables with a
later load-order prefix, their values will take priority and may override your
edits here.

For auxiliary zone numbers and auxiliary zone slot counts, additional
edits are required:

To change the building slots for auxiliary zones, in addition to editing
@BPV_ZONE_SLOT, open the file
`common/defines/zzzz_bpv_zone_slots_override.txt` and change the value to the
right of `DEFAULT_MAX_PLANET_BUILDINGS_PER_ZONE`. This defines the
default slot count for zones that do not have an explicitly forced slot
number. Some zones in the game (such as industrial zones) do not have
predefined slot numbers, so the game will use this value at runtime.

To change the number of auxiliary zones in the main city district, in
addition to editing `@BPV_CITY_ZONES`, you also need to open
`common/inline_scripts/districts/BPV_district_slots.txt` and modify the code
inside the curly braces. Add lines according to the rule, one per
auxiliary zone, until you reach the desired number. For example, if you
want the main city to have four auxiliary zones, the modified content
should look like this:

```ParadoxScript
zone_slots = {
 $GOVERNMENT$
 $SLOT1$
 $SLOT2$
 $SLOT3$
 $SLOT4$
}
```

**Note**: The first line `$GOVERNMENT$` represents the main zone (the
government/central area). Do not remove it. The auxiliary zones must be
added sequentially in the format `SLOT` + number, starting from `1`,
one per line.

Due to game mechanics, this list must also match corresponding district
data in the game to function correctly. Currently, this mod adjusts all
vanilla districts to support up to 10 auxiliary zones. If your list
defines more than 10 items, the extra entries will have no effect. If
you want to increase the limit further, please refer to the Stellaris
modding documentation and review how this mod implements these changes
before making additional edits.

---

## Guide For Mod Developers (Compatibility)

If you are a mod developer and want your custom **districts** and
**zones** to support the dynamic slot system provided by this mod, you
can follow the methods below:

### Make Custom Zones Support Dynamic Slot Numbers

The simplest way is **not to set the `max_buildings` property** when
defining a zone.
In this case, the game will use the global default slot value at runtime.
This mod (and its sub-mods) override that global value with the number
chosen by the user, so your zone will automatically adapt to the user’s
preference.

If you **want to explicitly set this parameter**, or need to use the
user-defined slot number for other purposes, you can reference the
global variable `@BPV_ZONE_SLOT` and then use it for `max_buildings` or
any other logic.

**Note:** Users might not have installed any BPV-related mods. If you
reference `@BPV_ZONE_SLOT` directly, errors may occur. To avoid this,
please copy `common/scripted_variables/zz_bpv_defines.txt` from this mod into
your own one, or merge its contents into your own definition files,
placed at a **lower priority**. Under such circumstance, if the user
doesn’t have BPV installed, the parameter will default to `3`, matching
vanilla Stellaris behavior.

### Make Custom Districts Support Dynamic Zone Numbers

To make your **custom districts** support dynamic zones, add the
following after your original `zone_slots` definition:

```ParadoxScript
inline_script = {
    script = districts/BPV_district_slots
    GOVERNMENT = <main city zone type>
    SLOT1 = <first auxiliary zone type>
    ...
    SLOT10 = <tenth auxiliary zone type>
}
```

The actual number of zones visible in-game depends on the **user’s
settings**. For example, if the user sets 4 auxiliary zones, then only
`SLOT1`–`SLOT4` will appear. If you define fewer than 10 slots, the max
shown will be limited to what you defined. For example, if you only
define 4 slots, but the user sets 6, only 4 will appear.

**Note**: By default, vanilla city district only support 2 auxiliary
zones (extra ones won’t display). For better compatibility, it’s
recommended to repeat the same zone type from `SLOT2` to `SLOT10`.
Under such circumstance, the second auxiliary zone will automatically
repeat to match the user’s configured number. If you define more than
two different auxiliary zone types, vanilla users may not see them
unless you add extra compatibility logic.

For city districts with only **2 auxiliary zones**, you can use this shorter script:

```ParadoxScript
inline_script = {
    script = districts/BPV_district_slots2
    GOVERNMENT = <main city zone type>
    SLOT1 = <first auxiliary zone type>
    SLOT2 = <second auxiliary zone type, auto-repeat>
}
```

If the user does not have this mod installed, the `inline_script`
section will simply not execute (since the script file does not exist).
In that case, the game will fall back to your original `zone_slots`
definition, ensuring full compatibility.
