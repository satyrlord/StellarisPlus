# StellarisPlus — Changelog

Date: 2025-12-29
Order: reverse chronological (latest changes first)

- Documentation: moved Copilot guidance into dedicated references
  - Added help/mod_defines_reference.md (file layout / where changes go)
  - Added help/mod_load_reference.md (load order / filename prefix conventions)
  - Added help/mod_mechanics_reference.md (core mechanics: BPV slot variables + inline scripts)
  - Added help/mod_ui_reference.md (consolidated existing help guides)
  - Updated .github/copilot-instructions.md to only point to the above reference docs (keeps Copilot instructions short and repo-specific)

- Planet UI: removed redundant scrollbars and fixed district header text layout
  - Updated interface/zz_planet_view.gui
    - Removed thick right-side vertical scrollbars from the district containers and embedded zone containers
    - Fixed district name vs specialization overlap by splitting onto two lines
    - Aligned yellow specialization text directly under the white district type name
    - Tuned vertical spacing/offsets so descenders (y/g) do not collide with the first building row

- Gameplay merge: integrated BPV Reborn preset stack into the root mod (single combined mod)
  - Integrated mods (in original load order):
    - BPV Reborn - Zone Single Row Mode (Workshop ID: 3485762595)
    - BPVR - More Building Slots (Workshop ID: 3576125834)
    - BPVR - City 4 Zones (Workshop ID: 3575256162)
    - BPVR - City 24 Slot (Workshop ID: 3575256424)
    - BPVR - Zone 6 Slots (Workshop ID: 3575256652)
  - Key merged outputs (root mod):
    - common/districts/*and common/zones/* replace files to support the BPV dynamic slot system
    - common/inline_scripts/districts/BPV_district_slots*.txt (including BPV_district_slots.txt with 4 auxiliary zones)
    - common/scripted_variables/zz_bpv_defines.txt set to @BPV_CITY_SLOT=24, @BPV_ZONE_SLOT=6, @BPV_CITY_ZONES=4
    - common/defines/zzzz_bpv_zone_slots_override.txt sets DEFAULT_MAX_PLANET_BUILDINGS_PER_ZONE=6

- Credits: recorded integrated mods for attribution
  - Added credits.txt listing the integrated Workshop mods and their Workshop IDs
