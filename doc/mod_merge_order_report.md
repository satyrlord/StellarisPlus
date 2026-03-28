# StellarisPlus -- Merge Order Report

Generated: 2026-03-27

## Consolidated Files

| Folder | Merged filename | Source files merged | Strategy |
| --- | --- | --- | --- |
| common/defines | zz_sp_defines.txt | hrth_defines.txt, zzzz_sp_defines.txt | LIOS |
| common/diplo_phrases | zz_sp_diplo_phrases.txt | m_insults_00_diplo_phrases.txt, MAP_diplo_phrases.txt, saurischian_diplo_phrases.txt | LIOS |
| common/portrait_sets | zz_sp_portrait_sets.txt | 00_saurischian_portrait_sets.txt, slreup_portrait_sets.txt | LIOS |
| common/species_names | zz_sp_species_names.txt | 197 files (see git log for full list) | LIOS |
| common/anomalies | zz_sp_anomalies.txt | aspmod_anomaly_categories_administration.txt, aspmod_anomaly_categories_CO2.txt, aspmod_anomaly_categories_ddadda.txt, aspmod_anomaly_categories_sehui98.txt, eev_anomaly_categories.txt, scfe_anomaly_categories.txt, scfe_precursors_anomalies.txt | LIOS |
| common/archaeological_site_types | zz_sp_archaeological_site_types.txt | 36 files | LIOS |
| common/armies | zz_sp_armies.txt | plentiful-traditions_stormtrooper.txt, scfe_armies.txt | LIOS |
| common/component_sets | zz_sp_component_sets.txt | aspmod_sets_planet_killer.txt, scfe_component_sets.txt | LIOS |
| common/component_templates | zz_sp_component_templates.txt | aspmod_templates.txt, scfe_component_template.txt | LIOS |
| common/deposits | zz_sp_deposits.txt | 00_aspmod_planetary_deposits.txt, scfe_planetary_deposits.txt, previous zz_sp_deposits.txt | LIOS |
| common/event_chains | zz_sp_event_chains.txt | eev_chains.txt, scfe_event_chains.txt | LIOS |
| common/game_rules | zz_sp_game_rules.txt | plentiful_traditions_rules.txt, scfe_game_rules.txt | LIOS |
| common/on_actions | !zz_sp_scfe_on_actions.txt, zz_sp_on_actions.txt, zzz_sp_scfe_on_actions.txt | !scfe_on_actions.txt, aspmod_on_actions.txt, eev_on_actions.txt, z_scfe_on_actions.txt, previous zz_sp_on_actions.txt | MERGE |
| common/planet_classes | zz_sp_planet_classes.txt | aspmod_planet_classes.txt, scfe_planet_classes.txt | LIOS |
| common/policies | zz_sp_policies.txt | aspmod_policies.txt, scfe_policies.txt, simpletraditions_policies.txt | LIOS |
| common/relics | zz_sp_relics.txt | aspmod_relics.txt, scfe_relics.txt | LIOS |
| common/scripted_effects | zz_sp_scripted_effects.txt | !_scfe_placeholder_effects.txt, !placeholder_effects.txt, aspmod_scripted_effects.txt, scfe_scripted_effects.txt | LIOS |
| common/scripted_triggers | zz_sp_scripted_triggers.txt | ! asp_placeholder_triggers.txt, asp_triggers.txt, aspmod_scripted_triggers_planet_killers.txt, aspmod_scripted_triggers.txt, eev_event_trigger.txt, eev_triggers.txt, plentiful_scripted_triggers.txt, scfe_triggers.txt, previous zz_sp_scripted_triggers.txt, zzz_overwrite_triggers.txt | LIOS |
| common/special_projects | zz_sp_special_projects.txt | 16 files | LIOS |
| common/static_modifiers | zz_sp_static_modifiers.txt | aspmod_static_modifers.txt, scfe_static_modifiers.txt, previous zz_sp_static_modifiers.txt | LIOS |
| common/technology | zz_sp_technology.txt | aspmod_tech.txt, plentiful_traditions_tech_placeholder.txt, scfe_technology.txt | LIOS |

## Folders Skipped

| Folder | Reason |
| --- | --- |
| common/buildings | Vanilla exact-path overrides present |
| common/decisions | Vanilla exact-path overrides present |
| common/districts | Vanilla exact-path overrides present |
| common/inline_scripts | DUPL strategy (filename = call target) |
| common/megastructures | Mixed gameplay file and README; left separate for manual review |
| common/name_lists | DUPL strategy |
| common/opinion_modifiers | Vanilla exact-path override + ambiguous strategy |
| common/pop_jobs | Vanilla exact-path overrides present |
| common/scripted_variables | FIOS + vanilla exact-path override |
| common/solar_system_initializers | FIOS initializer folder protected by skill guidance |
| common/strategic_resources | DUPL strategy |
| common/tradition_categories | Vanilla exact-path overrides present |
| common/traits | DUPL strategy |
| events | FIOS (event ID shadowing risk) |
| interface | Vanilla exact-path override present |
| localisation | Multi-language YAML headers; unsafe to consolidate |
