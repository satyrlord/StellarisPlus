# Paradox Script Code Review Rules

Quick reference for Stellaris Paradox Script (Clausewitz engine) code review.
Informed by CWTools, Paradox Language Support, and the Stellaris modding
community.

Evidence-first rule: avoid speculation. When validating assumptions about
scripts, assets, overrides, references, or missing content, cross-check them
against the actual vanilla Stellaris files, relevant DLC files, or original
mod files before treating them as facts.

## StellarisPlus Review Context

- Load `doc/mod_load_reference.md` before judging filename prefixes,
    override safety, or per-folder load behavior.
- Load `doc/mod_merge_order_report.md` before flagging a `zz_sp_*`
    file as an accidental duplicate or unsafe merge.
- Scan `doc/changelog.md` when touched files look unusual; recent
    entries often explain why a merge, compatibility shim, or override
    exists.

---

## Syntax Fundamentals

### File Types

| Extension | Language | Location |
| --- | --- | --- |
| `.txt` | Paradox Script | `common/`, `events/` |
| `.gfx` | Paradox Script (GFX variant) | `interface/`, `gfx/` |
| `.gui` | Paradox Script (GUI variant) | `interface/` |
| `.yml` | Paradox Localisation (NOT valid YAML) | `localisation/` |
| `.asset` | Paradox Script (entity/audio variant) | `sound/`, `gfx/` |
| `.mod` | Paradox Script (metadata) | root |
| `.csv` | Semicolon-delimited CSV | `localisation/` (legacy) |

### Encoding

- Localisation `.yml` files must be UTF-8 with BOM.
- Non-localisation Paradox script files under `common/`, `events/`,
    `interface/`, `gfx/`, and `sound/` must be UTF-8 without BOM.
- A BOM at the start of a non-localisation script file can make the
    engine reject the first top-level key and misparse later nested
    keys.

### Block Structure

Every Paradox Script file is a tree of `key = { ... }` blocks.
Braces must balance.

```paradoxscript
district_example = {
    potential = {
        owner = { is_regular_empire = yes }
    }
    resources = {
        category = planet_districts
        cost = { minerals = 500 }
    }
}
```

Common block families by context:

| Context | Expected blocks |
| --- | --- |
| Districts/Buildings | potential, allow, resources, planet_modifier, triggered_planet_modifier, convert_to, inline_script |
| Decisions | owned_planets_only, potential, allow, effect, hidden_effect, ai_weight |
| Events | namespace, (country/planet/fleet)_event, trigger, mean_time_to_happen, immediate, option, after |
| Traditions | modifier, possible, on_enabled, tradition_swap, ai_weight |
| Edicts | potential, allow, modifier, resources (upkeep), ai_weight |
| Policies | option sub-blocks with policy_flags, modifier, ai_weight |
| Zones | potential, unlock, resources, zone_sets, include, inline_script, ai_priority |
| Scripted triggers | Named block with conditions only (no effects) |
| Scripted effects | Named block with effects only (may contain trigger sub-blocks via `limit`) |
| On actions | events = { ... } list |

### Separators and Operators

| Operator | Usage |
| --- | --- |
| `=` | Assignment or equality test (context-dependent) |
| `!=` | Not-equal comparison |
| `<` `>` `<=` `>=` | Numeric comparisons |
| `?=` | Conditional assignment (set only if not already set) |
| `OR`, `AND`, `NOT`, `NOR`, `NAND` | Logic combinators (always UPPERCASE) |
| `if`, `else_if`, `else` | Conditional blocks with `limit = { ... }` |

### Value Types

| Type | Examples | Notes |
| --- | --- | --- |
| Boolean | `yes`, `no` | |
| Integer | `10`, `-5`, `0` | Leading minus and leading zeros permitted |
| Float | `1.0`, `-0.5`, `0.25` | |
| String (unquoted) | `country`, `planet_districts` | Must not contain `# = { }` or whitespace |
| String (quoted) | `"text with spaces"` | Supports `\"` escape |
| Color | `rgb { 34 136 255 }`, `hsv { 0.6 0.75 1.0 }` | Also `hsv360 { ... }` |
| Block | `{ ... }` | Contains properties, values, nested blocks |

### Scripted Variables

| Form | Meaning | Example |
| --- | --- | --- |
| `@name = value` | Definition (compile-time constant) | `@BPV_CITY_SLOT = 6` |
| `@name` | Reference (substitutes the defined value) | `max = @BPV_CITY_SLOT` |
| `@[ expr ]` | Inline math expression | `@[ 1 + @base * 2 ]` |

Inline math supports: `+`, `-`, `*`, `/`, `%`, unary minus,
absolute value `|x|`, parentheses `(expr)`, and variable
references inside the expression.

### Parameters (Inline Scripts)

| Form | Meaning | Example |
| --- | --- | --- |
| `$NAME$` | Parameter placeholder | `$GOVERNMENT$`, `$SLOT1$` |
| `$NAME\|default$` | Parameter with default value | `$COUNT\|1$` |
| `[[PARAM] ... ]` | Parameter condition block (include if set) | `[[HAS_FEATURE] feature = yes ]` |
| `[[!PARAM] ... ]` | Negated parameter condition | `[[!DISABLED] enabled = yes ]` |

Parameters and parameter conditions are only evaluated inside inline
script templates (`common/inline_scripts/`).

---

## Scope Rules

Scopes define which game object a block operates on. Invalid scope
transitions cause Script Errors at runtime. CWTools and Paradox Language
Support both validate scope correctness using CWT config files that
define the full scope graph for each Stellaris version.

### Common Scopes

| Scope | Type | Typical parent |
| --- | --- | --- |
| `owner` | Country | Planet, Pop, Leader, Fleet |
| `from` | Caller context | Event, on_action |
| `fromfrom` | Caller's caller | Chained events |
| `capital_scope` | Planet | Country |
| `root` | Top-level object | Any nested scope |
| `prev` | Previous scope | Any nested scope |
| `prevprev` | Two scopes back | Deeply nested contexts |
| `this` | Current scope | Explicit self-reference |
| `solar_system` | System | Planet |
| `leader` | Leader | Country, Fleet |
| `space_owner` | Country | System |
| `controller` | Country | Planet |

### Iterator Scopes

| Iterator | Target | Context |
| --- | --- | --- |
| `every_owned_planet` | All planets owned by country | Effect |
| `random_owned_planet` | One random owned planet | Effect |
| `any_owned_planet` | True if at least one matches | Trigger |
| `count_owned_planet` | Count matching planets | Trigger |
| `every_owned_leader` | All hired leaders | Effect |
| `every_pool_leader` | All leaders in hire pool | Effect |
| `every_planet_within_border` | All planets in country borders | Effect |
| `every_owned_pop` | All pops on planet or in empire | Effect |
| `any_owned_pop` | True if at least one pop matches | Trigger |
| `every_owned_pop_group` | All owned pop groups | Effect |
| `any_owned_pop_group` | True if at least one pop group matches | Trigger |
| `every_system_within_border` | All systems in borders | Effect |

Pattern: `every_*` = effect iterator, `any_*` = trigger iterator,
`random_*` = effect (picks one), `count_*` = trigger (returns count).

Pop-group iterators use pop-group scope, not individual pop scope.
Do not assume that a trigger valid on `every_owned_pop` is also valid
on `every_owned_pop_group`; verify against vanilla, DLC, or upstream
mod source before reusing job or trait checks.

### Trigger vs Effect Context

This is a **critical** review item. Effects inside trigger blocks
(`potential`, `allow`, `any_*` iterators) cause runtime errors.

| Block type | Allows triggers | Allows effects |
| --- | --- | --- |
| `potential`, `allow`, `limit` | Yes | NO |
| `effect`, `immediate`, `option` | Yes (via `if/limit`) | Yes |
| `modifier`, `planet_modifier` | NO (static values only) | NO |
| `triggered_planet_modifier` | `potential = {}` trigger only | NO (static values only) |
| `mean_time_to_happen` | Yes (for `modifier` weight) | NO |
| `ai_weight` | Yes (for `modifier` weight) | NO |
| `every_*`, `random_*` iterators | `limit = {}` only | Yes (body) |
| `any_*`, `count_*` iterators | Yes (body) | NO |

### Scripted Triggers vs Scripted Effects

| Type | Location | Contains | Called from |
| --- | --- | --- | --- |
| Scripted trigger | `common/scripted_triggers/` | Trigger conditions only | Trigger context |
| Scripted effect | `common/scripted_effects/` | Effect commands | Effect context |

Calling a scripted trigger from an effect context is valid
(used inside `if/limit`). Calling a scripted effect from a
trigger context is a bug.

---

## Load Order

Stellaris loads files alphabetically within each
`common/<subfolder>/`. Filename prefixes control override priority:

| Prefix pattern | Load order position | Purpose |
| --- | --- | --- |
| `!!!_*` | Very early | Baseline compatibility variables |
| `000_*`, `00_*` | Early | Vanilla replacement files |
| `(no prefix)` | Middle | Normal additions |
| `z_*`, `zz_*` | Late | Override files |
| `zzzz_*` | Very late | Final override (highest priority) |

**Key rule**: For `scripted_variables`, the **first loaded** definition
of `@var` wins (FIOS -- First In, Only Served). Use early-sorting prefixes
(`07_`, `99_`, `zz_`) to control which definition takes effect. The `~~`
prefix sorts last and acts as a fallback default.

When reviewing:

- Check that override files have appropriate prefixes
- Verify `_replace` suffix files intend to fully replace vanilla objects
- Watch for accidental variable shadowing across files with different prefixes
- Do not assume one load strategy applies everywhere in this repo:
    `events/` is FIOS, `common/solar_system_initializers/` is FIOS,
    `interface/` is LIOS, and `localisation/replace/` is the guaranteed
    override path for localisation keys
- Consolidated `zz_sp_*` files listed in `doc/mod_merge_order_report.md`
    are intentional; review them against their target folder strategy,
    not as if they were arbitrary duplicates

---

## Inline Script Rules

Inline scripts are template files with `$PARAM$` placeholders. Call
sites must provide every parameter.

Template file (`common/inline_scripts/districts/BPV_district_slots.txt`):

```paradoxscript
zone_slots = {
    $GOVERNMENT$
    $SLOT1$
    $SLOT2$
}
```

Call site:

```paradoxscript
inline_script = {
    script = districts/BPV_district_slots
    GOVERNMENT = slot_city_government
    SLOT1 = slot_city_01
    SLOT2 = slot_city_02
}
```

Review checklist:

- Every `$PARAM$` in the template has a matching key at the call site
- No extra parameters at the call site that the template does not use
- `script =` path is relative to `common/inline_scripts/` (no file
    extension) and resolves in the mod, vanilla game, or relevant DLC files

---

## Localisation Rules

Files use Paradox Localisation syntax (NOT valid YAML despite the
`.yml` extension). Must be UTF-8 with BOM encoding.

```yaml
l_english:
 key_name:0 "Display text with $tokens$ and [scope.GetName]"
```

### File Format Requirements

- First non-comment line must be the language header (e.g., `l_english:`)
- File must be UTF-8 with BOM (byte order mark)
- Key format: `key_name:N "text"` where N is version number (typically 0)
- One space indent before each key
- No duplicate keys in the same file (last definition wins, earlier
    ones silently lost)
- Multiple language headers in one file are allowed (for compatibility
    with `localisation/languages.yml`)

When validating localisation references, cross-check the referenced keys in the
actual localisation files instead of assuming they are present from naming
conventions alone.

### Markup Inside Localisation Strings

| Markup | Syntax | Example |
| --- | --- | --- |
| Colour | `SECTION_CHAR_START X ... SECTION_CHAR_END !` | `SECTION_CHAR_START Y$value$SECTION_CHAR_END !` |
| Parameter | `$name$` or `$name\|argument$` | `$planet_name$` |
| Scripted var | `$@var$` | `$@base_cost$` |
| Icon | `POUND_SIGN icon\|frame POUND_SIGN` | `POUND_SIGN unity POUND_SIGN` |
| Command | `[scope.Method\|argument]` | `[Root.GetName]` |
| Concept | `['concept_key', rich_text]` | `['pop_growth', +10%]` |
| Newline | `\n` | `"Line 1\nLine 2"` |

Note: colour codes use section sign followed by a single
character ID (e.g., Y for yellow, G for green, R for red).
Concept commands are Stellaris-specific.

### Common Localisation Keys

Objects defined in script typically need matching localisation:

| Script object | Expected keys |
| --- | --- |
| Building `building_x` | `building_x`, `building_x_desc` |
| District `district_x` | `district_x`, `district_x_desc`, `district_x_plural` |
| Decision `decision_x` | `decision_x`, `decision_x_desc` |
| Tradition `tradition_x` | `tradition_x`, `tradition_x_desc`, `tradition_x_delayed` |
| Edict `edict_x` | `edict_x`, `edict_x_desc` |
| Event option | `name = event_ns.1.a` requires `event_ns.1.a` key |
| Trait `trait_x` | `trait_x`, `trait_x_desc` |

---

## GFX and GUI Rules

### GFX (.gfx files)

```paradoxscript
spriteTypes = {
    spriteType = {
        name = "GFX_sprite_name"
        textureFile = "gfx/interface/icons/example.dds"
    }
}
```

Review checklist:

- `name` follows `GFX_` prefix convention
- `textureFile` path exists (relative to mod root or vanilla)
- Key casing is consistent (`textureFile` not `texturefile`)
- No duplicate sprite names within the mod
- Dotted sprite names can be valid Stellaris naming conventions (for
    example `GFX_evt_asp.20`)

### Asset / Entity (.asset files)

```paradoxscript
entity = {
    name = "portrait_example_entity"
    pdxmesh = "portrait_example_mesh"
    default_state = "idle"
    state = { name = "idle" animation = "idle" }
}
```

Review checklist:

- Entity names are unique within the mod
- Referenced meshes exist and use the expected mesh variant
- Referenced animation IDs exist on the assigned mesh
- Asset files under `gfx/` are reviewed like script, not like audio-only data

### GUI (.gui files)

```paradoxscript
guiTypes = {
    containerWindowType = {
        name = "example_window"
        position = { x = 0 y = 0 }
        size = { width = 400 height = 300 }
    }
}
```

Review checklist:

- Every `spriteType` or `gfx_name` referenced exists in a `.gfx` file
- `@` constants used for positioning are defined
- `if_scaled_resolution` blocks cover expected resolutions
- For `topbar_*.gui` and zone or slot UI files, cross-check
    `doc/mod_ui_reference.md` and `doc/mod_mechanics_reference.md` for
    BPV slot-count consistency, fallback behavior, and paired constants
- `interface/topbar_traditions_view.gui` is an active compatibility
    surface in this repo; same-name GUI templates collide under
    interface LIOS rules even when they live in separate files

---

## StellarisPlus Quality Gate Notes

- Automated baseline: `tools/stellarisplus-quality-gate.ps1`.
- The local validator already consults detected vanilla and DLC roots
    before reporting missing sprites, textures, inline templates, or
    scripted variables; avoid reintroducing speculative "may be vanilla"
    findings.
- Duplicate-key findings can be expected in additive folders such as
    `common/ambient_objects/`, `common/component_sets/`,
    `common/component_templates/`, `common/defines/`,
    `common/on_actions/`, `common/special_projects/`, and
    `common/species_names/`.
- Scoped-flag suffixes can be valid in `@variable` checks.
- Multiline quoted inline-script payloads can be valid.

---

## Common Bugs

| Bug pattern | What to look for |
| --- | --- |
| Unclosed brace | Mismatched `{` and `}` count in a file |
| Effect in trigger | `add_modifier`, `remove_modifier`, `set_variable` inside `potential`/`allow`/`limit` |
| Trigger in effect-only | Using `any_*` iterator where `every_*` was intended |
| Wrong scope chain | `owner = { owner = { ... } }` (double scope) or planet trigger in country scope |
| Missing localisation | `_desc`, `_name`, `_tooltip` keys referenced but not defined |
| Shadowed variable | Same `@var` name in two `scripted_variables` files with different load-order prefixes |
| Orphaned sprite | GFX sprite defined but never referenced, or GUI references undefined sprite |
| Duplicate key | Same localisation key or object key defined twice (silent last-wins); confirm the folder is not an expected additive structure first |
| Wrong conditional | `else = {` without preceding `if`, or `else_if` after `else` |
| Missing namespace | Event file without `namespace = X` at top |
| Inline param mismatch | Call passes `SLOT1` but template uses `$SLOT_1$` (underscore difference) |
| Unclosed quote | Quoted string missing closing `"` (especially in localisation) |
| Wrong separator | Using `=` where `>=` or `<=` was intended in numeric comparisons |
| textureFile casing | `texturefile` (lowercase f) instead of `textureFile` (works but inconsistent) |
| Missing BOM | Localisation file saved as UTF-8 without BOM (engine ignores the file) |
| Unexpected BOM | Non-localisation script saved with UTF-8 BOM, causing the first top-level key to be rejected |

---

## External Tooling References

These tools provide automated validation complementary to manual review:

| Tool | Platform | What it validates |
| --- | --- | --- |
| `tools/stellarisplus-quality-gate.ps1` | Local PowerShell script | Repo-specific validator, Pyright, and markdownlint baseline |
| [CWTools](https://cwtools.github.io/) | VS Code extension | Syntax errors, scope correctness, attribute existence, type definitions, localisation keys, sprite/file references |
| [Paradox Language Support](https://github.com/DragonKnightOfBreeze/Paradox-Language-Support) | IntelliJ IDEA plugin | BNF-based parsing, CWT config-driven inspection, code navigation, DDS preview |
| [OldEnt trigger/effect/modifier lists](https://github.com/OldEnt/stellaris-triggers-modifiers-effects-list) | Data files | Canonical lists of all triggers, effects, modifiers, scopes per Stellaris version (up to 4.0.6) |

Both CWTools and Paradox Language Support use **CWT config files** to
define game semantics (valid triggers, effects, modifiers, scopes,
type definitions). The CWT format is a variant of Paradox Script with
`.cwt` extension and additional comment directives (`##` option
comments, `###` doc comments).
