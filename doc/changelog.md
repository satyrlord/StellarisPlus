# StellarisPlus -- Changelog

Date: 2026-10-04

- BPVR More Building Slots 1.2.0 (read-only dry run, then a minimal port): added `common/inline_scripts/zones/` with the 28 vanilla
  `shared_*_zone` scripts, each a vanilla 4.5 copy whose only change is `zone_building_slots_add = @BPV_ZONE_SLOT` (was `3`).
  Everything else in 1.2.0 was deliberately not taken: our 24/6/4 presets, 10-slot district template, district and zone BPV lines are
    unchanged; its subject-holding agreements use a modifier that does not exist in 4.5 and its district, zone and capital-building
    copies are partly pre-4.5.
- Combat computer overrides (`common/component_templates/zz_sp_component_templates.txt`, a `zz_sp_` override of vanilla `00_utilities_roles.txt` and `00_biogenesis_utilities.txt`):
  - The vanilla 4.5 auto-design bug (`COMBAT_COMPUTER_DEFAULT` has no `upgrades_to` chain) is still present, so the fix stays.
    The 14 "Component template key used multiple times" log lines are this intended override.
  - Restored two 4.5 `potential` conditions our copies had lost: `NOT = { is_ship_size = paladin_ship }` on
    `COMBAT_COMPUTER_DEFAULT` and `is_arkship_ship = no` on the seven bio combat computers.
- Namelist localisation: added the ten leader-name keys the 4.5.1 log reported as missing (Chikako, Eija,
  Getrelaudia, Kallio, Martutasios, Mazi, Mozgu, Thraevan, Ukkaissehs, Yamawaki).
- Economic categories rebased onto vanilla 4.5 in `common/economic_categories/zz_sp_economic_categories.txt` (`zz_sp_` override of vanilla 00/01/02 files):
  - 38 of the 41 vanilla-overriding categories were stale pre-4.5 copies (36 of them Plentiful Traditions' own)
    that silently replaced the 4.5 parents, `modifier_category` lines and triggered modifiers; for example
    `starbases` had lost its outpost cost modifier and `planet_telepaths` its inherited modifiers.
  - Each is now the vanilla 4.5 definition plus only our additive `generate_add_modifiers` and
    `generate_mult_modifiers` entries, so every modifier name the mod already used still exists. Six of them
    (`planet_soldiers`, `planet_telepaths`, `planet_districts_cities`, `planet_entertainers`, `rivalries`,
    `station_observers`) turned out to need no additions and now equal vanilla exactly.
- Runtime log fixes from the first Stellaris 4.5.1 launch (1,612 `error.log` entries, 191 mod-owned and fixed):
  - Technology: removed 35 `ai_update_type` lines from the Echoes of the Fallen fallen-empire tech
    overrides in `common/technology/zz_sp_technology.txt` (not valid in 4.5) and restored the
    `ai_weight` that `tech_dark_matter_deflector` lost from vanilla.
  - Traditions: removed the stray `name` key in `tr_plentiful_mysticism_adopt`, the three
    category-level `tradition_swap` blocks (4.5 only allows them inside traditions, and they pointed at
    categories that do not exist), and gave Malice nodes 1 and 3 a `custom_tooltip_with_modifiers`
    because their pop-category-only modifiers were reported as "Missing effects".
  - Plentiful Traditions decisions and events: removed the `carrier_event` calls to
    `plentiful_traditions_transformation_pedict.101-106,150`, which upstream never defines; repaired the
    harvest chain (`event` is not an effect, now `planet_event`) and dropped its carrier duplicates, which
    would have fired the destructive follow-up twice; turned `plentiful_traditions_aspiration.2` (a global
    monthly event) from a planet event into a plain event; removed 20 empty `if`/`else_if` blocks
    from the affinity, anguish, experimentalism and robotics events (no behaviour change).
  - Starbase modules: removed the five `station_gatherers_*_produces_mult` entries from `orbit_modifier`
    (not allowed there in 4.5; the `system_modifier` entries remain) and corrected the Malice finish text.
  - `ap_plentiful_traditions_slave_complex` and `_slave_nation` are not defined by any perk, which
    logged 90 errors. The checks were replaced by `always = no` and the four building modifiers that
    could never fire were removed.
  - `08_unity_buildings.txt`: removed a `has_tradition` check in federation scope (invalid in 4.5).
  - Localisation: repaired `tr_plentiful_malice_finish_desc` and `_5_desc` in all seven languages (my
    earlier rewrite had stored real line breaks instead of the escape sequence) and removed nine namelist keys that
    contain spaces.
  - Orphaned Matrix: `orphan_matrix_events.145` now uses the existing `GFX_evt_astral_rift_corridors`.
  - Planet view: `pop_job_info` in `interface/zz_planet_view.gui` is now UI Overhaul Dynamic's 4.5
    version, adding `pop_factions` and `wanted_factions` (and the shifted rows).
- BPV Reborn Zone Single Row updated to the 2026-08-24 upstream in `interface/zz_planet_view.gui`
  (three-way merge against the absorbed copy; upstream is tagged v4.4.*, so this is untested on 4.5):
  - Took upstream's Arkship header, Arkship panel and management window, which adds
    `ARKSHIP_CONTROLS` (a child of UI Overhaul Dynamic's 4.5 `planet_view`) and a 4-column
    slot layout. The old panel's `orbitals_background` is gone; UI Overhaul Dynamic does
    not define it.
  - Kept the local district-card positions that use `@district_card_title_x`,
    `@district_card_title_y`, `@district_card_triggered_name_y` and
    `@district_card_build_button_x`.
  - New from upstream without conflict: the `decision_progress` bar,
    `cancel_decisions_button`, the `holding_type_entry` and `holding_per_country_entry`
    windows, `sidebar_list_height` 830 to 870 and `district_rows` 10 to 12. The
    `@portrait_window_*` variables are now defined locally with the same values as
    UI Overhaul Dynamic.
  - Still missing against UI Overhaul Dynamic's window: `pop_factions` and `wanted_factions`.
  - Not taken: `zzzz_bpvr_giga_gui_birch_districts_uiod.gui` (compatibility layer for a mod
    that is not loaded here).
- Restored BPV zone-slot support that had been lost from two districts, using the
  same `districts/BPV_district_slots` line the BPVR More Building Slots upstream applies:
  - `district_resort` in `common/districts/00_urban_districts.txt` (lost when the
    absorbed BPV district files were replaced by the Plentiful Traditions copies).
  - `district_hab_housing` in `common/districts/03_habitat_districts.txt` (same cause,
    2026-03-22).
  - Not restored: `district_crashed_slaver_ship`, which upstream no longer gives BPV
    slots (it has a single zone).
  - Re-indented the 10 `inline_script` slot lines in `00_urban_districts.txt` and
    `04_ringworld_districts.txt` that the Plentiful Traditions update had left
    flush-left.
- Orphaned Matrix Origin updated to the 2026-08-17 upstream (v4.5 checked):
  - Taken from upstream where the integrated copy was unchanged: traits, concepts,
    system initializer, digsite events, four `.gfx` files, English and French
    localisation (merged), and two new modifier icons. Added the new Introspection
    Complex upgrade events (`orphan_matrix_events.143`-`.145`) and the upstream
    rebalance of the Introspection Complex buildings, Delve the Old Codex situation
    and decisions.
  - Merged into the `zz_sp_` files: buildings, decisions, situations, economic
    categories (`modifier_category = colony`), civics (adds
    `ship_archaeological_site_clues_add`), the `introspective_calculator` job
    (`job_total_output_modifier`, new upkeep modifier) and the script values.
    The event file kept the local fixes (country-scope `orphan_matrix_events.1`
    trigger, `capital_scope` situation targets, carrier flags) and now uses
    upstream's `create_pop_group` loop in `orphan_matrix_events.102`.
  - Restored logic lost to earlier cleanups. Commit a3d4f22 had deleted the real
    Orphaned Matrix script values and e02cdb4 replaced them with `base = 1`
    placeholders, so the research and unity level bonuses, the memorialist,
    custodian and dead-empire output scaling, assimilator energy and the
    Introspection Complex job count were all inert. They now match upstream.
    Commit 6fd39f2 had removed the `on_entering_system_first_time`
    (`orphan_matrix_events.52`) and `on_country_destroyed`
    (`orphan_matrix_events.140`) hooks; both are back in
    `common/on_actions/zz_sp_on_actions.txt`.
  - `common/static_modifiers/zz_sp_static_modifiers.txt` now keeps only the five job
    workforce modifiers Orphaned Matrix changes (researcher, physicist, biologist,
    engineer, bureaucrat), rebuilt from vanilla 4.5 plus
    `pop_introspective_calculator_bonus_workforce_mult`. The other copies of
    vanilla's `24_static_modifiers_jobs.txt` were stale 4.4 duplicates and were
    dropped so vanilla 4.5 applies (it adds ark harvester, cruise passenger and
    evaluator entries).
  - Removed the unused `everyone_but_dystopian_specialist_workforce_mult` static
    modifier (an old Orphaned Matrix copy that upstream and vanilla 4.5 no longer have)
    and its compatibility localisation.
  - Kept local: the archaeology site `potential` and `visible` triggers (country
    scope, verified against the 4.4.6 log), the superset `has_precursor_intro`
    trigger, the origin event picture, and the Introspection Complex slot count.
  - Fixed upstream's French localisation, which defined
    `orphan_matrix_events.95.accept` twice (the second is `.96.accept`).
- Added `map/setup_scenarios/{tiny,small,medium,large,huge}.txt` from Plentiful
  Traditions. They are identical to vanilla 4.5 except for higher
  `fallen_empire_max` and `marauder_empire_max` (tiny 2/2, small 4/4, medium 6/4,
  large 8/6, huge 8/6; vanilla 1/1, 2/2, 3/2, 4/3, 6/3).
- Removed all Malice and Mutagenesis events (`plentiful_traditions_malice.*`,
  `plentiful_traditions_mutagenesis.*`) and everything that existed only for them:
  - Deleted `events/plentiful_traditions_malice_events.txt` and
    `events/plentiful_traditions_mutagenesis.txt`.
  - Removed their `on_actions` hooks (`on_monthly_pulse_country`, `on_purge_complete`,
    and the `on_pop_enslaved` and `on_pop_emancipated` blocks, which only held them).
  - Removed the `plentiful_traditions_mutagenesis_transformation` decision pair, the
    `modifier_mutagenesis_transformation` and `modifier_plentiful_traditions_slave1`
    static modifiers, the unused `pm_mutagenesis_transformation.dds` icon and their
    localisation keys in all seven languages.
  - The Malice and Mutagenesis traditions, categories, agendas and the Mutagenesis
    Universalis ascension perk are kept; they run on their own modifiers.
- Malice tradition descriptions now match what the script does (all seven languages):
  - Adoption lists only the +50% insult efficiency (the slave happiness and consumer
    goods bonuses came from the removed events).
  - Spite no longer promises the removed recently-conquered effect.
- Reworked Malice traditions that had lost their slave-specific effects (the old
  `pop_cat_slave_*` and `planet_jobs_slave_*` modifiers are gone in 4.x), using
  modifiers vanilla 4.5 still uses:
  - Despair: slave happiness +20% and slave political power -25% (was an empty node).
  - Dread: slave job efficiency +10% (`pop_slave_bonus_workforce_mult`) instead of
    +10% on every planet job.
  - Wrath: miners' minerals +15% (`planet_miners_minerals_produces_mult`) instead of
    every mineral job; rivalries +4 unchanged.
  - Finish text lists the refinery module's real effects (alloys, planet jobs +5%,
    station gatherers +10%).
  - German adoption text moved from the unused `_adopt_effect` key to `_adopt_desc`;
    removed the unused "Slave Complex activated/deactivated" keys.
- `common/defines/zz_sp_defines.txt`: added `MAX_PLANET_SUBJECT_HOLDING_BUILDING_SLOTS = 5`
  (vanilla 4) from the updated Plentiful Traditions defines, which its
  subject-holdings agreement terms expect.
- `tools/credits_date_probes.json`: the Orphaned Matrix probe also matches "Orphan Matrix",
  the spelling used in commit messages. Hyper Relay's credits date was set to 2026-10-04
  after confirming its only game file (`HYPERLANE_THICKNESS_RELAY = 1.4`) already matches
  the 2026-09-24 upstream; the refresh script never moves a date backwards, so it stays.
- `tools/stellarisplus-refresh-credits-dates.py`: the script now reads the existing
  `Last updated` date, so `--check` no longer reports every entry as stale, and it
  never moves a date backwards.
- Plentiful Traditions updated to the 2026-10-04 upstream (v4.5):
  - Taken from upstream where the integrated copy was unchanged: eight event
    files, the agreement term values, the ascension-perk and persiancats sprite
    files, the topbar arrow GUI, and 15 tradition tree icons (30x30, replacing
    oversized 306x218 images). Added the missing Blood and Iron perk icon.
  - Clean three-way merges: starbase modules, war events, English and German
    localisation. Faith events now use the carrier-flag API; kept the local
    topbar GUI change, the `experimentalism` event removal and the pop-group
    `transformation` events.
  - Vanilla-path copies refreshed for 4.5: `01_pop_assembly_buildings`,
    `08_unity_buildings` and the four `common/districts/*_districts.txt` files.
    The BPV `districts/BPV_district_slots` lines (7 urban, 3 ringworld) were
    re-applied over upstream's `zone_slots`; local necrophage tooltips and the
    `job_bureaucrat_add` fixes were kept; the clone vats perk now uses
    `ap_organo_machine_interfacing_assimilator`.
  - Removed the three `has_district = district_*_uncapped` checks in
    `zz_sp_decisions.txt`; upstream folded those districts into the base
    districts with `is_uncapped`.
  - Block-level updates in the merged `zz_sp_*` files: 24 decisions, 6 buildings,
    3 tradition categories, 1 tradition and 1 trigger, plus new `carrier_event`
    variants `.101`-`.110` in `events/plentiful_traditions_adaptive_foundry_events.txt`
    (event `.9`, missing upstream, was kept).
  - `common/pop_jobs/zz_sp_gestalt_jobs.txt` reduced to the `replicator` job:
    4.5 vanilla now provides the toxic-bath jobs. Removed the two unused
    bath-attendant triggers.
  - Trimmed 92 sprites from `interface/zz_plentiful_traditions_traditions.gfx`
    that the updated `plentiful_traditions_persiancats.gfx` now defines, and
    restored the `GFX_tradition_hex_bg_plentiful_malice` name that upstream
    renamed by mistake.
  - Not applied: upstream's new malice and mutagenesis events (they use
    `every_owned_pop`, `any_owned_pop` and `has_job`, which do not exist in 4.5),
    the galaxy setup caps, and the unused Vest system.
  - `on_actions`: added `faith.1`, `faith.2` and `transformation_pedict.11`
    hooks.

- Scion Origin Expanded updated to upstream 1.3.1 (upstream commit 1cfedf4):
  - `events/soe_events.txt`, `common/scripted_variables/soe_scripted_variables.txt`
    and `localisation/english/soe_l_english.yml` replaced with the upstream
    versions: War in Heaven transmission rework, gift balance changes
    (fleet gift 10 to 20 years, tech gift 40 to 45) and text fixes.
  - Merged blocks updated in `zz_sp_scripted_triggers.txt` (Mind over Matter
    now keys on `tr_psionics_adopt`, War in Heaven checks) with five new
    `soe_eligible_for_wih_*` triggers, and `decision_soe_request_autonomy` now
    needs Good opinion instead of Excellent.
  - Removed the `on_ascension_perk_picked` hook from `zz_sp_on_actions.txt`;
    `soe.90` is now fired from the tradition event chain.
  - Kept the existing `textureFile` casing in
    `interface/soe_origin_eventpictures.gfx`.

- Stellaris 4.5 compatibility fixes for stale copies of vanilla files:
  - `common/scripted_variables/07_scripted_variables_machine_age.txt`: refreshed
    from the updated Plentiful Traditions copy, restoring the 18
    `@arc_furnace_*` variables that 4.5 vanilla deposits, overclock types,
    megastructures and static modifiers use. `@max_tradition_trees = 24` is
    kept.
  - `common/strategic_resources/00_strategic_resources.txt`: refreshed from the
    updated Plentiful Traditions copy, restoring the `integrity` resource that
    4.5 vanilla references and picking up the 4.5 market-gate documentation,
    `culling_conversion_value` and nomad mining prerequisites.
  - Removed `common/inline_scripts/colony_types/colony_type_planet_modifier.txt`,
    a StellarisPlus-added override that no mod file called. Vanilla 4.5
    colony-type files call the inline script, so it now resolves to the vanilla
    version (15% instead of 10%).

Date: 2026-07-28

- Runtime log fixes for Orphaned Matrix and integrated namelists:
  - Replaced stale custom archaeology visibility calls with direct country-scope
    origin checks, eliminating repeated invalid `from.planet` context switches.
  - Changed both `situation_delve_old_codex` starts to target `capital_scope`.
  - Replaced the Introspection Complex planet-flag calls with the carrier-flag
    API across event creation and recovery, zones, buildings, inline job logic,
    and cleanup.
  - Added the 121 integrated leader-name localisation keys reported by the
    current runtime log.
  - Documented the `zz_sp_` archaeological-site and building merge overrides in
    their file headers.
  - Replaced the raw `NO_POSSIBLE_OPTION` preview on Subterfuge asset costs with
    an explicit tooltip while preserving vanilla asset-selection behavior.

Date: 2026-07-12

- Runtime log fixes for Stellaris 4.4.6:
  - Fixed `zone_MZ_elite` checking a planet-only flag from ship scope by using
    the current zone API's `has_carrier_flag` in both `potential` and `unlock`.
  - Restored the integrated CANS ship-name limit under `unchecked_defines/`,
    where Stellaris reads `NInterface.SHIP_NAME_SIZE_MAX`.
  - Replaced four literal sequential army names with their existing
    localisation keys and added the two leader-name keys seen in the log.
  - Restored the Arkship header, focus button, management window, and tabs in
    `interface/zz_planet_view.gui`, preserving the BPVR layout while matching
    the current vanilla/UI Overhaul Dynamic `planet_view` child contract.

Date: 2026-06-22

- UI fix: Diplomacy proposal overlap and text spillover with UI Overhaul Dynamic
  - Root cause: interface/zzzz_sp_uiod_diplomacy_compat.gui used vanilla Stellaris
    4.4.4 positionType values (diplo_full_width=1280, target_selector_full_position=
    1100,16) that conflict with UIOD's wider layout (view width 1300, dropdown at
    894,29). The game code uses these positionTypes to dynamically reposition
    elements, overriding UIOD's explicit positions and causing the target empire
    selector to overlap the proposal text area.
  - Updated all four positionType values to match UIOD's actual layout:
    diplo_full_width 1280→1300, diplo_compact_width 990→1300,
    target_selector_full_position (1100,16)→(894,29),
    target_selector_compact_position (821,16)→(894,29).

Date: 2026-06-21

- Bug fix: Introspection Complex (zone_introspective_laboratory) had only 3 building
  slots — a vanilla remnant — instead of the mod-standard 6 (@BPV_ZONE_SLOT).
  Changed max_buildings from hardcoded 3 to @BPV_ZONE_SLOT in
  common/zones/zz_sp_zones.txt.

- Feature: Machine Empire Food District Zone Retrofit
  - Added two machine-empire-only zones (zone_sp_machine_food_energy,
    zone_sp_machine_food_minerals) that fit in slot_food and use swap_type
    to transform farming districts into generator or mining districts via
    the zone-swap UI.
  - Overrode slot_food unlock in zone_slots/zz_sp_specialization_unlocks.txt
    to allow machine empire access without food_processing_1 tech.
  - Added to common/zones/zz_sp_zones.txt and
    common/zone_slots/zz_sp_specialization_unlocks.txt.

- Bug fix: Orphaned Matrix event chain never triggered — archaeological site not created
  - Two independent bugs prevented site creation:
    1. `orphan_matrix_events.1` (a country_event) had a `trigger` block wrapping
       conditions in an invalid `owner = { ... }` scope. From a country scope,
       `owner` does not exist, so the trigger always evaluated to false, silently
       preventing the event from firing.
    2. The archaeological site type `ancient_buried_vault_digsite` had a `potential`
       trigger depending on `@from.planet` to resolve a per-planet country flag.
       During site creation via `create_archaeological_site`, `from` is unset
       (no scanning ship exists yet), so `@from.planet` resolved to nothing,
       the flag check always failed, and the creation effect silently did nothing.
  - Fixed by: (a) removing the `owner` wrapper in the event trigger; (b) replacing
    the fragile `@from.planet` flag check in the site's `potential` and `visible`
    triggers with a direct origin check (`is_machine_empire = yes` +
    `has_origin = origin_orphan_matrix`), matching the pattern used by the other
    Orphaned Matrix site (`om_ancient_ecu_digsite`) and all EOTF sites.
  - Removed the now-unused `set_country_flag = ancient_buried_vault_arcsite_owner`
    from the event.

- Bug fix: CTD when opening diplomacy with fallen empires
  - Root cause: UI Overhaul Dynamic's diplomacy_view.gui omits 4 vanilla
    positionTypes (diplo_full_width, diplo_compact_width,
    target_selector_full_position, target_selector_compact_position);
    when the diplomacy UI tries to look them up, the null gui_type
    causes a crash-to-desktop.
  - Created interface/zzzz_sp_uiod_diplomacy_compat.gui to restore
    the missing positionTypes with vanilla values.
  - Load order note: StellarisPlus should be placed AFTER UI Overhaul
    Dynamic in the launcher so its zz_/zzzz_ file-level overrides win.

- Bug fix: Deferred key reference crashes from gpm_has_other_mod_relic
  - Replaced 14 references to non-existent external mod relic keys
    (r_aspmod_*, r_scfe_*) with always = no in
    common/scripted_triggers/zz_sp_scripted_triggers.txt.
  - StellarisPlus ships no custom relics; the trigger now correctly
    always returns false.

Date: 2026-06-10

- Bug fix: Missing effects tradition errors for 7 traditions
  - Added `custom_tooltip_with_modifiers` to `tr_plentiful_anguish_5`,
    `tr_plentiful_biogenesis_adopt`, `tr_plentiful_malice_1`,
    `tr_plentiful_mysticism_1_machine` (tradition_swap),
    `tr_plentiful_order_3`, `tr_plentiful_robotics_adopt`, and
    `tr_plentiful_robotics_hive_adopt` (tradition_swap) in
    `common/traditions/zz_sp_traditions.txt`
  - Uncommented and simplified localisation keys
    `tr_plentiful_robotics_adopt_desc`,
    `tr_plentiful_robotics_hive_adopt_desc`, and
    `tr_plentiful_biogenesis_adopt_desc` in
    `localisation/plentiful_traditions_l_english.yml`

- Bug fix: Invalid scripted effect create_pop in orphan_matrix_events.txt
  - Replaced deprecated `create_pop` with `create_pop_group` (4.0+ API)
    in both option blocks of `orphan_matrix_events.102`
  - Fixed cascading "Unexpected token: custom_tooltip" and
    "Corrupt Event Table Entry" errors caused by the invalid effect

- Bug fix: Invalid scope for event target 'planet' in
  plentiful_traditions_malice_events.txt
  - Removed `exists = planet` from pop_event triggers (lines 17, 56)
  - Replaced `planet = { owner = { ... } }` with `owner = { ... }`
    in immediate blocks (lines 26, 63) since planet scope switch is
    invalid from pop scope in 4.0+

- Bug fix: Invalid context switch [orbit] in zz_sp_zones.txt
  - Removed `orbit = { }` scope wrapper in zone potential and unlock
    blocks (lines 2096, 2109) since orbit scope is invalid from colony
    scope; check `has_planet_flag` directly

Date: 2026-06-09

- Documentation: UI Overhaul Dynamic (ID 1623423360) is now a required
  external dependency
  - Added "UI Overhaul Dynamic" to `dependencies` in `descriptor.mod`
  - Added UIOD section to `doc/mod_mechanics_reference.md`
  - Listed UIOD under a new "Expected Dependencies" heading in
    `credits.md`

- UI fix: Planet View tabs now use UIOD long-tab sprites
  (`GFX_ui_tab_1_long_*`, `GFX_ui_tab_2_long_*`) with font_text_16
  in `interface/zz_planet_view.gui`, matching UIOD layout coordinates

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
