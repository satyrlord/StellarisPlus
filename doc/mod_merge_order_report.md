# StellarisPlus -- Merge / Override Planning Report

This report applies the rules from [doc/mod_load_reference.md](mod_load_reference.md)
to the current StellarisPlus content layout so future integrations can be
sorted quickly without repeating the same full load-order audit.

The goal here is practical classification:

- which files are safe to move to ordinary late-loading override files
- which files must remain exact-path replacements
- which files should use fallback ordering instead of winning ordering
- which folders cannot express removal or replacement semantics at all

---

## Safe Late-Load Additive Files

These can live in new late-sorting files such as `zz_*` without using the
vanilla filename, as long as the contained keys keep the same object names.

| Area | Current / recommended pattern | Why it is safe |
| --- | --- | --- |
| `interface/*.gfx` extra sprite definitions | `interface/zz_plentiful_traditions_traditions.gfx`, `interface/zz_plentiful_traditions_council_agendas.gfx` | `interface/` is LIOS. Only the named sprites matter, not the source filename. |
| `common/defines/` additive override blocks | `common/defines/plentiful_traditions_defines.txt`, `common/defines/ow_defines@RPA.txt`, `common/defines/zz_*` | `defines` is LIOS. The last value for the same define key wins. |
| `common/traditions/`, `common/tradition_categories/`, `common/technology/`, `common/edicts/`, `common/council_agendas/` | Prefer normal late files instead of matching vanilla filenames unless a full-file replacement is required | These folders are LIOS keyed-object folders. Only object key precedence matters. |
| `common/districts/` override-only files | Candidate for future rename to `zz_*_districts.txt` if the file only contains existing vanilla district keys | `districts` is LIOS since v3.3. Exact filename matching is not required when overriding existing district keys. |

Practical rule: if a LIOS file only exists to provide later definitions for
named objects or sprites, prefer a late-sorting custom filename over a
same-path vanilla replacement.

---

## Safe Fallback Files

These should sort late specifically so they lose to any real provider.

| File pattern | Why it must stay fallback-oriented |
| --- | --- |
| `common/scripted_variables/~~*.txt` | `scripted_variables/` is FIOS. The first definition wins, so a late `~~` file acts as a fallback default only. |
| Similar fallback shims in other FIOS folders | Use the same logic whenever a definition should exist only if nothing earlier provided it. |

Current example:

- `~~*.txt` fallback files are still the right pattern for FIOS defaults,
  even though the old More Zones BPV fallback file has now been removed
  from StellarisPlus.

Practical rule: never rename FIOS fallbacks to early-sorting names unless you
intend them to become the winning provider.

---

## Merge-Only Files

These files can add content, but they cannot remove or replace existing
entries inside the same block.

| Folder | Guidance |
| --- | --- |
| `common/on_actions/` | Treat files as additive only. Use them to append events, never to imply that empty blocks suppress other hooks. |

Current rule for this repo:

- `common/on_actions/plentiful_traditions_on_actions.txt` is valid because it
  adds real hooks.
- `common/on_actions/plentiful_traditions_on_actions_neu.txt` was removed
  because its empty scaffold implied override behavior that MERGE cannot
  provide.

Practical rule: if you need to stop an inherited on_action effect, `common/on_actions/`
is the wrong mechanism. Solve that at the triggered effect or event layer.

---

## Exact-Path Replacement Candidates To Keep Narrow

These are load-order-sensitive surfaces where exact-path replacement is often
the most expensive option. Prefer splitting them unless structure forces a
full replacement.

| File / area | Current recommendation |
| --- | --- |
| `interface/traditions.gfx` | Already split out. Keep only the PT-specific sprite names in `interface/zz_plentiful_traditions_traditions.gfx`. |
| `interface/council_agendas.gfx` | Already split out. Keep only the PT-specific agenda icons in `interface/zz_plentiful_traditions_council_agendas.gfx`. |
| `common/districts/00_urban_districts.txt` | Future candidate for conversion into a late custom filename containing only the overridden district keys. |
| `common/districts/02_rural_districts.txt` | Future candidate for conversion into a late custom filename containing only the overridden district keys. |
| `common/districts/03_habitat_districts.txt` | Future candidate for conversion into a late custom filename containing only the overridden district keys. |
| `common/districts/04_ringworld_districts.txt` | Future candidate for conversion into a late custom filename containing only the overridden district keys. |

Practical rule: when a LIOS replacement file only overrides existing top-level
keys, it is usually safer to move those keys into a `zz_*` file than to keep a
full vanilla-path replacement.

---

## Exact-Path Replacements That Still Need Structural Review

These are not yet safe to classify as simple additive split-outs.

| File | Why it still needs caution |
| --- | --- |
| `interface/topbar_traditions_view.gui` | This file changes structural containers in the traditions UI. It is not just a bag of extra named sprites. Keep it as a deliberate compatibility surface and audit against other UI mods directly. |
| `common/inline_scripts/*` on vanilla filenames | `inline_scripts/` is DUPL. Selective override is impossible; same-path replacement is the only real override mechanism. |
| `common/traits/*` or `common/strategic_resources/*` when trying to replace an existing vanilla entry selectively | These folders are DUPL / no-selective-override surfaces. Treat them as whole-file replacement problems, not per-entry override problems. |

Practical rule: if the folder is DUPL or the file rewires structural UI layout,
assume exact-path replacement is still required until proven otherwise.

---

## GUI Name Collision Rules

`interface/` is LIOS by named definition, not by filename alone.

That means these are both true:

- different files can safely add different named templates
- different files cannot safely define the same named template unless one is
  intentionally meant to override the other

Current example resolved in this pass:

- `tree_11_11_21` now lives only in `interface/topbar_traditions_view.gui`
- `interface/topbar_traditions_view_arrow.gui` keeps only its unique helper
  layouts

Practical rule: when splitting GUI helpers, audit for duplicate `name = "..."`
blocks across all `.gui` files, not just inside one file.

---

## Recommended Triage Flow For Future Imports

1. Identify the folder load rule from [doc/mod_load_reference.md](mod_load_reference.md).
2. If the folder is FIOS, decide whether the file should win early or
  lose late as a fallback.
3. If the folder is MERGE, confirm the file only adds entries and does
  not pretend to remove them.
4. If the folder is LIOS, compare against vanilla and ask whether the
  file only overrides existing keyed objects.
5. If yes, prefer a late custom filename such as `zz_*` over a vanilla-path replacement.
6. If the file changes structural UI layout or the folder is DUPL, keep
  it on the exact path until a deeper compatibility plan exists.

---

## Current High-Value Follow-Ups

1. Convert the remaining district same-path overrides into late custom
  files if no hidden path-sensitive behavior turns up during validation.
2. Keep `interface/topbar_traditions_view.gui` under explicit
  compatibility review whenever another UI mod touches the traditions
  screen.
3. Reuse the `zz_*` late-load pattern for future PT sprite additions
  instead of restoring full vanilla-path `.gfx` replacements.
