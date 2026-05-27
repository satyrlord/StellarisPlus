# Conflict Patterns Reference

Common conflict patterns encountered when absorbing Stellaris mods into
StellarisPlus, with resolution strategies.

---

## File-Level Conflict Patterns

### Pattern 1: Duplicate Vanilla Override

Both mods override the same vanilla file (e.g., `common/buildings/00_capital_buildings.txt`).

**Detection**: Same relative path exists in both workspace and incoming mod.

**Resolution**:

1. Diff the two files against vanilla to identify each mod's changes.
2. If changes affect different blocks within the file, combine both.
3. If changes affect the same block, present the conflict to the user.

### Pattern 2: Same Custom Namespace

Both mods define events in the same namespace or use overlapping event
ID ranges.

**Detection**: `namespace = X` appears in both workspace and incoming
event files. Event IDs (e.g., `X.1`, `X.2`) collide.

**Resolution**:

1. Rename the incoming mod's namespace (e.g., append `_sp`).
2. Update all references to the renamed namespace across events,
   on_actions, and decisions.
3. Update localisation keys if they are namespace-prefixed.

### Pattern 3: Scripted Variable Shadowing

Both mods define the same `@variable` with different values.

**Detection**: Same variable name in `common/scripted_variables/` files.

**Resolution**:

1. If this mod's value is intentional (documented in
   `doc/mod_mechanics_reference.md`), keep it.
2. If the incoming mod's value is needed for its own content, create a
   separate variable (e.g., `@incoming_mod_value`).
3. Consider load-order prefix to control which value wins at runtime.

### Pattern 4: Inline Script Parameter Mismatch

The incoming mod calls an inline script with parameters that differ
from the StellarisPlus version of that script.

**Detection**: `inline_script = { script = X PARAM = val }` where
the StellarisPlus version of `X` expects different parameters.

**Resolution**:

1. Add the new parameter with a default fallback to the inline script
   template.
2. Update existing callers if the parameter is mandatory.

### Pattern 5: GFX Sprite Name Collision

Both mods define a sprite with the same `name = "GFX_..."`.

**Detection**: Duplicate `name` values across `.gfx` files.

**Resolution**:

1. If both reference the same texture, keep one and delete the other.
2. If they reference different textures, rename the incoming sprite
   and update all GUI/script references.

### Pattern 6: Localisation Key Collision

Both mods define the same localisation key with different text.

**Detection**: Same key in `localisation/**/*.yml` files.

**Resolution**:

1. Keep the StellarisPlus version by default.
2. If the incoming version adds meaningful content (e.g., a more
   descriptive tooltip), ask the user.
3. Never silently overwrite existing localisation.

---

## Load-Order Conflict Patterns

### Early Override Clash

Two files with `00_` or `000_` prefixes in the same `common/` subdirectory.

**Risk**: Unpredictable which loads first among same-prefix files.

**Resolution**: Differentiate prefixes (e.g., `000_` vs `001_`).

### Late Override Clash

Two files with `zz_` prefix targeting the same gameplay systems.

**Risk**: The incoming mod's override may undo StellarisPlus changes.

**Resolution**: Merge content into a single `zz_` file or use `zzzz_`
for the final override.

### Replace File Collision

Both mods include a file with `_replace` suffix for the same vanilla file.

**Risk**: Only one `_replace` file takes effect -- the other is ignored.

**Resolution**: Merge both replacement files into one, combining all
intended changes.

---

## Asset Conflict Patterns

### Texture Path Collision

Both mods place different `.dds` files at the same `gfx/` path.

**Resolution**: One must be renamed. Update all `.gfx` references to
the renamed texture.

### Sound Category Missing

Incoming mod defines sounds without a `category` field.

**Resolution**: Add the `category` field as required by the engine.
Refer to existing `sound/*.asset` files for the correct format.

---

## StellarisPlus-Specific Patterns

### Zone/Building Slot Variables

If the incoming mod touches `@BPV_CITY_SLOT`, `@BPV_ZONE_SLOT`, or
`@BPV_CITY_ZONES`, it directly conflicts with the core StellarisPlus
zone system documented in `doc/mod_mechanics_reference.md`.

**Resolution**: Always keep StellarisPlus values. Adapt the incoming
mod's content to use the existing variable system instead of hardcoded
values.

### District Inline Script Compatibility

If the incoming mod defines custom districts, check whether they use
`inline_script` calls for zone slots. If not, they may need to be
adapted to use the `BPV_district_slots` inline script family for
compatibility with the dynamic slot system.

**Resolution**: Follow the compatibility guide in
`doc/mod_ui_reference.md` (section "Guide For Mod Developers").
