# Paradox Script Code Review Rules

Quick reference for Stellaris Paradox Script parser, scope, and inline-script
semantics during code review.

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

`doc/mod_load_reference.md` is the sole authority for prefix order, folder
strategy, exact-path overrides, and `_replace` behavior. Load it before judging
any of those properties. Load `doc/mod_merge_order_report.md` before flagging a
listed consolidated file. This reference supplies no competing load-order
table.

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

## StellarisPlus Quality Gate Notes

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
