# Per-File-Type Review Checklists

Use these during Phase 1.2 of the code review. Read the full file; use diff to
focus, but validate surrounding context.

## Gameplay scripts (`common/**/*.txt`)

1. Brace balance (`{` == `}`)
2. Scope correctness (no invalid chains like `owner = { owner = { } }`)
3. No effects in trigger blocks (`potential`, `allow`, `limit`, `any_*`)
4. `@variable` refs defined in `scripted_variables`; check for shadowing
5. `inline_script` calls: params match template `$PARAM$`; `script =` resolves
6. Filename prefix matches intent per `doc/mod_load_reference.md`
7. Modifier symmetry: add has corresponding remove path
8. Conditional logic: `if` has `limit`, `else_if` before `else`, no
   `else_if` after `else`
9. Non-localisation script files (`.txt`, `.gfx`, `.gui`, `.asset`)
  must be UTF-8 without BOM; a BOM can cause the first parsed key to
  be rejected
10. When changes touch zones, zone slots, traditions, buildings, or
   districts, cross-check `doc/mod_mechanics_reference.md` for linked
   constraints and constants before flagging or approving the change

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
- UTF-8 with BOM

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
