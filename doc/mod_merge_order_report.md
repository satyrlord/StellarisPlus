# Mod Merge Order Report

## 2026-05-03 Low-Risk Merge Pass

Scope approved by user:

- common/megastructures
- common/on_actions

| Folder | Strategy | Consolidated Filename | Source Files Removed |
| --- | --- | --- | --- |
| common/megastructures | LIOS | zz_sp_megastructures.txt | README.txt, aspmod_megastructures.txt |
| common/on_actions | MERGE | zz_sp_on_actions.txt | !zz_sp_scfe_on_actions.txt, vfb_on_actions.txt, zzz_sp_scfe_on_actions.txt |

Notes:

- common/on_actions was merged in ASCII filename order.
- Existing content inside each source block was preserved unchanged.
- Section separators were added as: # === merged from <original_filename> ===
- Files in events/ and common/solar_system_initializers/ remain unmerged by policy.

## 2026-05-31 Component Templates Merge

Scope approved by user:

- common/component_templates

| Folder | Strategy | Consolidated Filename | Source Files Removed |
| --- | --- | --- | --- |
| common/component_templates | LIOS | zz_sp_component_templates.txt | zz_sp_combat_computer_fix.txt |

Notes:

- Existing content inside each source block was preserved unchanged.
- Section separators were added as: # === merged from <original_filename> ===

## 2026-05-31 SOE Integration Merge

Scope approved by user:

- common/decisions
- common/on_actions
- common/opinion_modifiers
- common/scripted_effects
- common/scripted_triggers
- common/static_modifiers
- common/special_projects
- common/start_screen_messages

| Folder | Strategy | Consolidated Filename | Source Files Removed |
| --- | --- | --- | --- |
| common/decisions | LIOS | zz_sp_decisions.txt | soe_decisions.txt |
| common/on_actions | MERGE | zz_sp_on_actions.txt | soe_on_actions.txt |
| common/opinion_modifiers | LIOS | zz_sp_opinion_modifiers.txt | 00_soe_opinions.txt, soe_opinion_modifiers.txt |
| common/scripted_effects | LIOS | zz_sp_scripted_effects.txt | soe_scripted_effects.txt |
| common/scripted_triggers | LIOS | zz_sp_scripted_triggers.txt | 00_soe_chain_triggers.txt, soe_triggers.txt, zzz_soe_just_researched_fe_tech.txt |
| common/static_modifiers | LIOS | zz_sp_static_modifiers.txt | soe_static_modifiers.txt |
| common/special_projects | MERGE | zz_sp_special_projects.txt | soe_projects.txt |
| common/start_screen_messages | LIOS | zz_sp_start_screen_messages.txt | 00_soe_start_screen_messages.txt |

Notes:

- Empty placeholder files (00_soe_opinions.txt, 00_soe_chain_triggers.txt,
  00_soe_start_screen_messages.txt) were removed after merge.
- common/on_actions and common/special_projects: SOE content prepended to
  preserve pre-merge ASCII load order (`soe_*` sorted before `zz_sp_*`).
- common/scripted_triggers: SOE triggers prepended; zzz_soe FE-tech
  override appended last inside zz_sp_scripted_triggers.txt.
- Vanilla exact-path files kept separate: 00_resource_decisions.txt,
  01_personality_opinions.txt.
- Section separators were added as: # === merged from <original_filename> ===

## 2026-05-31 EOTF Consolidation Merge

Scope approved by user:

- common/ascension_perks
- common/on_actions
- common/scripted_effects
- common/scripted_triggers
- common/special_projects
- common/start_screen_messages
- common/static_modifiers
- common/technology

| Folder | Strategy | Consolidated Filename | Source Files Removed |
| --- | --- | --- | --- |
| common/ascension_perks | LIOS | zz_sp_ascension_perks.txt | 00_eotf_ascension_perks.txt, plentiful_traditions_ascension_perks.txt |
| common/on_actions | MERGE | zz_sp_on_actions.txt | eotf_on_actions.txt |
| common/scripted_effects | LIOS | zz_sp_scripted_effects.txt | 00_eotf_chain_markers.txt, 00_eotf_homeworld_ambient.txt, 00_eotf_infra_unlocks.txt, zzz_eotf_ancient_legacy_fe_grants.txt |
| common/scripted_triggers | LIOS | zz_sp_scripted_triggers.txt | 00_eotf_chain_triggers.txt |
| common/special_projects | MERGE | zz_sp_special_projects.txt | 00_eotf_divine_hulk_projects.txt, 00_eotf_projects.txt |
| common/start_screen_messages | LIOS | zz_sp_start_screen_messages.txt | 00_eotf_start_screen_messages.txt |
| common/static_modifiers | LIOS | zz_sp_static_modifiers.txt | 00_eotf_modifiers.txt |
| common/technology | LIOS | zz_sp_technology.txt | zzz_eotf_ancient_legacy_fe_tech_gate.txt, zzz_eotf_dark_matter.txt |

Notes:

- Existing content inside each source block was preserved unchanged.
- Section separators were added as: # === merged from <original_filename> ===
- common/ascension_perks created a new consolidated LIOS target because no
  existing zz_sp_ascension_perks.txt file was present.
- common/on_actions, common/scripted_triggers, common/special_projects,
  common/start_screen_messages, and common/static_modifiers had EOTF content
  prepended to preserve pre-merge ASCII load order.
- common/scripted_effects prepended the 00_eotf_* sources and appended
  zzz_eotf_ancient_legacy_fe_grants.txt after the existing zz_sp target.
- common/technology appended the two zzz_eotf_* technology files after the
  existing zz_sp_technology.txt content.

## 2026-05-31 Manual Classification Merge

Scope approved by user:

- common/archaeological_site_types
- common/event_chains
- common/global_ship_designs
- common/governments/civics
- common/situations

| Folder | Strategy | Consolidated Filename | Source Files Removed |
| --- | --- | --- | --- |
| common/archaeological_site_types | LIOS | zz_sp_archaeological_site_types.txt | 00_eotf_arc_sites.txt |
| common/event_chains | LIOS | zz_sp_event_chains.txt | 00_eotf_event_chains.txt |
| common/global_ship_designs | MERGE | zz_sp_global_ship_designs.txt | 00_eotf_event_ships.txt, ASP_ship_designs.txt |
| common/governments/civics | LIOS | zz_sp_civics.txt | 00_eotf_origins.txt |
| common/situations | LIOS | zz_sp_situations.txt | 00_eotf_divine_hulk_situations.txt, 99_orphan_matrix_situation.txt |

Notes:

- Existing content inside each source block was preserved unchanged.
- Section separators were added as: # === merged from <original_filename> ===
- common/archaeological_site_types, common/event_chains, and
  common/governments/civics prepended the `00_eotf_*` content into existing
  late-loading LIOS targets.
- common/situations created a new late-loading LIOS target,
  zz_sp_situations.txt, and preserved the original `00_` then `99_` ordering
  inside the merged file.
- common/global_ship_designs created zz_sp_global_ship_designs.txt and
  preserved the original `00_` then `ASP` ordering of anonymous `ship_design`
  blocks inside the merged file.
