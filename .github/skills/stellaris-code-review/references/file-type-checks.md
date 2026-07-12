# Per-File-Type Review Checklists

Use these file-local checks during Phase 1.2. Apply parser and scope semantics
from `paradox-script-rules.md`, encoding rules from
`doc/mod_defines_reference.md`, and filename/load-order rules from
`doc/mod_load_reference.md`; those meanings are not duplicated here.

## Gameplay scripts (`common/**/*.txt`)

1. `@variable` references resolve and intentional shadowing is documented.
2. `inline_script` calls resolve and provide the template parameters.
3. Reversible modifiers and effects have matching remove paths.
4. When changes touch zones, zone slots, traditions, buildings, or
   districts, cross-check `doc/mod_mechanics_reference.md` for linked
   constraints and constants before flagging or approving the change.

## Events (`events/*.txt`)

All gameplay script checks above, plus:

- `namespace = <name>` declared
- IDs follow `<namespace>.<number>`, unique within file
- Event type matches scope context
- Options have `name` key with localisation
- `is_triggered_only = yes` events referenced somewhere

## Localisation (`.yml`)

- Language header present (`l_english:`)
- Keys use `:0` format, no duplicates
- `$key$` refs point to existing keys; `[Scope.Method]` uses valid methods
- Encoding matches `doc/mod_defines_reference.md`.

## GFX (`.gfx`)

- `GFX_` prefix on names; `textureFile` (capital F) paths exist; no
  duplicate names

## GUI (`.gui`)

- Sprite refs exist in `.gfx`; `@` constants defined before use;
  brace balance
- For `topbar_*.gui` and zone or slot UI files, cross-check
  `doc/mod_ui_reference.md` and `doc/mod_mechanics_reference.md` for
  BPV slot-count consistency and fallback behavior
- Check for GUI template name collisions on LIOS surfaces such as
  `topbar_traditions_view.gui`
