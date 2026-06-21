# StellarisPlus -- File Types Reference

## Purpose & Scope

Describes every file type used by the StellarisPlus mod and where
changes should go. Use this document when adding new files, looking
up folder purposes, or onboarding new contributors.

- Supported Stellaris version: `v4.3.*` (see `descriptor.mod`).
- License: GPL-3.0 (see `LICENSE`).

---

## Naming Conventions

- Prefer filename prefixes that match the intended load-order strategy
  (see `doc/mod_load_reference.md` for FIOS/LIOS/DUPL/MERGE rules).
- Keep filenames consistent with the integrated-mod prefix patterns
  listed in `doc/mod_load_reference.md`.
- Scripted variable names use `@UPPER_SNAKE_CASE`.
- Inline script parameters use `$PARAM$`.

## Code Style

- Paradox Script files (`.txt`) use tabs for indentation and CRLF line
  endings.
- Localisation files (`.yml`) must be saved as UTF-8-BOM with CRLF.
- Prefer existing patterns over inventing new abstractions.

## Error Handling

- If a file path does not exist in the workspace, check
  `C:\Program Files (x86)\Steam\steamapps\common\Stellaris` and
  `C:\Program Files (x86)\Steam\steamapps\workshop\content\281990`
  before treating it as missing.
- Run `tools/stellarisplus-quality-gate.ps1` after structural changes
  to catch linting or type errors early.

## Testing

- After adding or moving files, verify brace balance and scope
  correctness before committing.
- Cross-check folder assignments against the per-folder load behaviour
  table in `doc/mod_load_reference.md`.

## Security

- Do not include or reference external URLs, API keys, or credentials
  in any mod file.
- Integrated mods must be credited in `credits.md`.

---

## Development Tools -- `tools/`

PowerShell scripts for development and CI workflows:

- `tools/stellarisplus-collect-logs.ps1` -- Collect Stellaris runtime
  logs into `tmp/_logs_inbox`
- `tools/stellarisplus-quality-gate.ps1` -- Run validation (Paradox
  Script linter, Pyright, markdownlint)
- `tools/stellarisplus-test.ps1` -- Run mod tests

---

## File Types And Where Changes Usually Go

### Gameplay data -- `common/`

Paradox Script (`.txt`). All gameplay logic lives here.

- `common/defines/*.txt` -- Engine constant overrides
  (`NGameplay`, `NEconomy`, etc.)
- `common/scripted_variables/*.txt` -- Global scripted variables
  (`@SYMBOL = value`), used as tunables
- `common/inline_scripts/**/*.txt` -- Parameterised script fragments
  invoked with `inline_script = { ... }`
  - `common/inline_scripts/districts/` -- BPV zone-slot templates
    (`BPV_district_slots*.txt`)
  - `common/inline_scripts/more_zones/` -- More Zones shared job/effect fragments
- `common/districts/*.txt` -- District definitions
  (city, rural, habitat, ring-world, arcology)
- `common/zones/*.txt` -- Zone definitions (building slot containers within districts)
- `common/zone_slots/*.txt` -- Zone slot type definitions
- `common/buildings/*.txt` -- Building definitions
- `common/pop_jobs/*.txt` -- Pop job definitions
- `common/traditions/*.txt` -- Tradition finish/adopt effects and modifiers
- `common/tradition_categories/*.txt` -- Tradition tree category definitions
- `common/ascension_perks/*.txt` -- Ascension perk definitions
- `common/traits/*.txt` -- Species and leader trait definitions
- `common/technology/*.txt` -- Technology definitions
- `common/edicts/*.txt` -- Edict definitions
- `common/decisions/*.txt` -- Decision definitions
- `common/policies/*.txt` -- Policy definitions
- `common/on_actions/*.txt` -- Event hook blocks
- `common/scripted_triggers/*.txt` -- Reusable named trigger blocks
- `common/scripted_modifiers/*.txt` -- Scripted modifier groupings
- `common/scripted_loc/*.txt` -- Scripted localisation functions
- `common/script_values/*.txt` -- Named script value computations
- `common/static_modifiers/*.txt` -- Static modifier definitions
- `common/game_rules/*.txt` -- Game rule overrides
- `common/deposits/*.txt` -- Deposit and resource tile definitions
- `common/armies/*.txt` -- Army type definitions
- `common/economic_categories/*.txt` -- Economic category definitions
- `common/starbase_modules/*.txt` -- Starbase module definitions
- `common/megastructures/*.txt` -- Megastructure definitions
- `common/council_agendas/*.txt` -- Council agenda definitions
- `common/opinion_modifiers/*.txt` -- Diplomatic opinion modifier definitions
- `common/strategic_resources/*.txt` -- Strategic resource definitions
- `common/terraform/*.txt` -- Terraforming definitions
- `common/name_lists/*.txt` -- Species and ship name lists
- `common/species_names/*.txt` -- Species name definitions
- `common/random_names/*.txt` -- Random name generation tables
- `common/portrait_sets/*.txt` -- Portrait set definitions
- `common/portrait_categories/*.txt` -- Portrait category definitions
- `common/diplo_phrases/*.txt` -- Diplomatic phrase definitions
- `common/solar_system_initializers/*.txt` -- System generation templates
- `common/agreement_term_values/*.txt` -- Diplomatic agreement term values

### Events -- `events/`

Paradox Script (`.txt`). Event chains and on-action hooks.

- `events/plentiful_traditions_*.txt` -- Plentiful Traditions event chains
- `events/simpletraditions_events.txt` -- Simple Traditions events
- `events/MZ_events.txt` -- More Zones district-swap events
- `events/permanent_decisions_events.txt` -- Permanent Decisions events

### Interface -- `interface/`

GFX sprite definitions (`.gfx`) and GUI layout files (`.gui`).

- `interface/*.gfx` -- Sprite and atlas definitions for UI icons and event pictures
- `interface/*.gui` -- Widget layout files
- `interface/zz_planet_view.gui` -- Planet view UI overrides
  (scrollbar and district header fixes)

### Graphics -- `gfx/`

Binary image assets and effect scripts.

- `gfx/**/*.dds` -- Texture and icon files (DDS format)
- `gfx/**/*.lua` -- Particle/shader effect scripts

### Flags -- `flags/`

Custom empire flag categories. Each subfolder contains `.dds` flag
textures grouped by theme.

### Localisation -- `localisation/`

YAML (`.yml`). Localisation key definitions, one file per language per
feature area.

- `localisation/english/*.yml` -- English localisation keys
- `localisation/<lang>/*.yml` -- Other language files
- Root-level `.yml` files (e.g.
  `localisation/plentiful_traditions_l_english.yml`) -- kept at their
  original paths from source mods to avoid breaking cross-mod key
  references
