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
  preserve pre-merge ASCII load order (soe_*sorted before zz_sp_*).
- common/scripted_triggers: SOE triggers prepended; zzz_soe FE-tech
  override appended last inside zz_sp_scripted_triggers.txt.
- Vanilla exact-path files kept separate: 00_resource_decisions.txt,
  01_personality_opinions.txt.
- Section separators were added as: # === merged from <original_filename> ===
