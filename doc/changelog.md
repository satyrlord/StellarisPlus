# StellarisPlus -- Changelog

Date: 2026-03-22
Order: reverse chronological (latest changes first)

- Bug fix: combat-computer auto-design stuck on Default Combat Computer
  - Added common/component_templates/zz_sp_combat_computer_fix.txt (LIOS)
  - Hides COMBAT_COMPUTER_DEFAULT and BIO_COMBAT_COMPUTER_DEFAULT, which
    have no upgrades_to chain on upgrade_path = default
  - Restores visible role-specific default computers (Swarm, Picket, Line,
    Artillery, Torpedo, Carrier, Buffer, Debuffer) so AI and auto-design
    can upgrade through combat-computer tech tiers again

- Bug fix: More Zones urban support zones now use BPV slot counts
  - Added @BPV_compatibility_load = 1 to
    common/scripted_variables/zz_bpv_defines.txt so integrated BPV
    always drives More Zones urban support slot counts in StellarisPlus
  - Previously, urban support zones multiplied slot counts by 0
    (vanilla behavior) despite BPV being integrated

- Cleanup: removed obsolete BPV fallback scripted variable file
  - Deleted common/scripted_variables/~~more_zones_BPV_compatibility.txt
    because StellarisPlus always includes BPV in the root mod
  - This removes the duplicate FIOS variable warning from the quality gate

- Documentation audit: fixed conflicts, gaps, and stale references
  - Fixed changelog references: credits.txt -> credits.md,
    help/ -> doc/ (matching actual file locations)
  - mod_mechanics_reference.md: used full NGameplay. prefix for
    TRADITION_COST_TRADITION and TRADITION_COST_TRADITION_EXP defines
  - mod_mechanics_reference.md: added three missing defines
    (EMPIRE_SIZE_TRADITION_COST_PENALTY, TRADITION_COST_MULT_TRADITION_GROUP,
    TRADITION_COST_RESOURCES)
  - mod_mechanics_reference.md: expanded More Zones zone type list
    from 4 to all 30 zone_MZ_* definitions with category groupings
  - mod_mechanics_reference.md: updated BPV compatibility note to
    reflect @BPV_compatibility_load = 1 in zz_bpv_defines.txt
  - mod_mechanics_reference.md: added sections for Reworked Planetary
    Ascension, NoSkullOnlyNumber, Permanent Decisions, and Longer Ship
    Names
  - mod_defines_reference.md: added tools/ section documenting
    development scripts and supported Stellaris version
  - mod_load_reference.md: removed unused !!! and 000_ prefix rows
    from load-order table (no files use these prefixes)
  - credits.md: updated header to reflect that backup/ archives have
    been cleaned up

Date: 2026-03-22
Order: reverse chronological (latest changes first)

- Documentation: updated all four doc/ reference files to reflect
  current codebase state
  - mod_defines_reference.md: expanded to cover all common/ subfolders, events/,
    interface/, gfx/, flags/, and localisation/ layout
  - mod_load_reference.md: added zzzz_ and ~~ prefix entries,
    per-folder FIOS/LIFO note,
    and naming convention table for integrated mod files
  - mod_mechanics_reference.md: added sections for Plentiful Traditions, More Zones,
    and Simple Traditions alongside the existing BPV Reborn section
  - mod_ui_reference.md: corrected all stale file paths (z_bpv_defines.txt ->
    zz_bpv_defines.txt, z_bpv_zone_slots_override.txt -> zzzz_bpv_zone_slots_override.txt,
    backslashes to forward slashes) and updated default values to match integrated
    preset (24/6/4 instead of 6/3/2)

- Maintenance: fixed cross-reference comments to use full relative paths
  - common/defines/plentiful_traditions_defines.txt: TRADITION_CATEGORIES_MAX comment
    now references common/scripted_variables/07_scripted_variables_machine_age.txt
  - common/scripted_variables/07_scripted_variables_machine_age.txt: @max_tradition_trees
    comment now references common/defines/plentiful_traditions_defines.txt

Date: 2026-01-01
Order: reverse chronological (latest changes first)

- Gameplay merge: integrated two additional Workshop mods into the root mod
  - Simple Traditions (Workshop ID: 2436408502) by Drassi
  - More Zones (district specializations) (Workshop ID: 3513435391) by Nobody
  - Note: content was moved from backup/<workshop_id>/ into the live
    root folders (common/, events/, gfx/, interface/, localisation/)

- Compatibility fixes: updated integrated scripts for current
  StellarisPlus/BPV environment
  - More Zones:
    - Fixed multiple outdated tokens/syntax issues
    - Corrected wrong-scope trigger usage (planet vs country scope)
    - Stabilized zone placement logic to avoid add_zone failures on
      planets lacking required districts
  - Simple Traditions:
    - Removed/adjusted deprecated leader trait fields and scripted effects
    - Updated building/tradition modifiers to valid job modifiers for this environment
    - Removed invalid AI-weight triggers and missing designations

- Credits: updated integrated mod attributions
  - Updated credits.md to include both newly integrated Workshop mods

- Warning cleanup:
  - Added building_sets to Simple Traditions Galactic University buildings
  - Removed references to a missing
    gfx/FX/buttonstate_onlydisable.lua in Simple Traditions gfx
    definitions
  - Added missing localisation keys for a tradition swap tooltip

Date: 2025-12-29
Order: reverse chronological (latest changes first)

- Documentation: moved Copilot guidance into dedicated references
  - Added doc/mod_defines_reference.md (file layout / where changes go)
  - Added doc/mod_load_reference.md (load order / filename prefix conventions)
  - Added doc/mod_mechanics_reference.md (core mechanics: BPV slot
    variables + inline scripts)
  - Added doc/mod_ui_reference.md (consolidated existing help guides)
  - Updated .github/copilot-instructions.md to only point to the above
    reference docs (keeps Copilot instructions short and repo-specific)

- Planet UI: removed redundant scrollbars and fixed district header text layout
  - Updated interface/zz_planet_view.gui
    - Removed thick right-side vertical scrollbars from the district
      containers and embedded zone containers
    - Fixed district name vs specialization overlap by splitting onto two lines
    - Aligned yellow specialization text directly under the white
      district type name
    - Tuned vertical spacing/offsets so descenders (y/g) do not
      collide with the first building row

- Gameplay merge: integrated BPV Reborn preset stack into the root mod
  (single combined mod)
  - Integrated mods (in original load order):
    - BPV Reborn - Zone Single Row Mode (Workshop ID: 3485762595)
    - BPVR - More Building Slots (Workshop ID: 3576125834)
    - BPVR - City 4 Zones (Workshop ID: 3575256162)
    - BPVR - City 24 Slot (Workshop ID: 3575256424)
    - BPVR - Zone 6 Slots (Workshop ID: 3575256652)
  - Key merged outputs (root mod):
    - common/districts/*and common/zones/* replace files to support
      the BPV dynamic slot system
    - common/inline_scripts/districts/BPV_district_slots*.txt
      (including BPV_district_slots.txt with 4 auxiliary zones)
    - common/scripted_variables/zz_bpv_defines.txt set to
      @BPV_CITY_SLOT=24, @BPV_ZONE_SLOT=6, @BPV_CITY_ZONES=4
    - common/defines/zzzz_bpv_zone_slots_override.txt sets DEFAULT_MAX_PLANET_BUILDINGS_PER_ZONE=6

- Credits: recorded integrated mods for attribution
  - Added credits.md listing the integrated Workshop mods and their Workshop IDs
