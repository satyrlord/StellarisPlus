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
