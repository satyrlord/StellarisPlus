# StellarisPlus Development Guidelines

## Scope

- **Root mod:** `descriptor.mod` (name = "StellarisPlus") --
  metadata only (name, tags, version, Workshop id).
- Gameplay source of truth is the root mod; changes live under `common/` and `interface/`.
- Integrated Workshop mods are credited in `credits.md`.
- User instructions always override this file.

## Approach & Efficiency

- Read existing files before writing. Do not re-read unless the file may have changed.
- Prefer editing over rewriting. One focused coding pass;
  no write-delete-rewrite cycles.
- Be concise in output but thorough in reasoning. No
  sycophantic openers or closing fluff. No emoji.
- Keep solutions simple and direct. No over-engineering.
- If unsure: say so. Never guess or invent file paths.
- Test your code before declaring done. Test once, fix if needed, verify once.
- Budget: 50 tool calls maximum.
- When a task can be split into independent investigations, use sub-agents in parallel.

## Naming Conventions

- Filename prefixes must match load-order strategy (see `doc/mod_load_reference.md`).
- LIOS overrides use `zz_sp_` prefix. `_replace` files only
  for replacing vanilla objects.
- Override prefixes (`zz_`, `zzzz_`) must be documented in
  the file, `doc/changelog.md`, or relevant repo doc.
- Variables: `@UPPER_SNAKE_CASE`. Inline script params: `$PARAM$`.
- Keep key names consistent with existing patterns; do not
  rename without updating all references.
- FIOS folders: `events/`, `common/solar_system_initializers/`.
  Localisation override: `localisation/replace/`.

## Code Style & Encoding

- Tabs for indentation, CRLF line endings. Do not reformat unchanged lines.
- Match brace/indentation style of neighbours. Prefer existing
  patterns over new abstractions.
- No effects inside trigger blocks (`potential`, `allow`, `limit`, `any_*`).
- Conditionals: `if` needs `limit`; `else_if` before `else`;
  no `else_if` after `else`.
- Reversible modifiers/effects must have a matching remove path.
- Events: declare namespace, use unique `<namespace>.<number>` IDs.
- Localisation: language header, `:0` formatting, no duplicate keys.
- GFX: `GFX_` prefix for sprites; `textureFile` (capital F) in `.gfx` files.
- `.txt`/`.gfx`/`.gui`/`.asset`: UTF-8 without BOM.
  `.yml` localisation: UTF-8 with BOM.

```paradox
# Correct -- tabs, consistent bracing
ap_example = {
  potential = {
    NOT = { has_ascension_perk = ap_example }
  }
  modifier = {
    country_base_defense_armies_add = 4
  }
}

# Incorrect -- collapsed braces, reformatted neighbours
ap_example = {
  potential = { NOT = { has_ascension_perk = ap_example } }
  modifier = { country_base_defense_armies_add = 4 }
}
```

## Error Handling

- Collect logs into `tmp/_logs_inbox` **only** on explicit user
  request or `/stellaris-log-fix`:

  ```powershell
  & "tools/stellarisplus-collect-logs.ps1" -NoLaunch -IncludeException
  ```

- Run `spcollect` **only** when the user explicitly asks.
- Missing assets: check
  `C:\Program Files (x86)\Steam\steamapps\workshop\content\281990`
  or `...\common\Stellaris`.

## Testing

- Create a TODO list for each major change.
- Cross-check assumptions against actual vanilla/DLC/original mod files. No speculation.
- Consult `doc/mod_load_reference.md` before judging conflicts
  or merge safety.
- After editing gameplay files, verify brace balance and scope correctness.
- Verify cross-file references: localisation keys, `GFX_`
  sprites, `textureFile` paths, `inline_script` paths/params,
  `@variable` declarations/usages.
- For zones, zone slots, traditions, buildings, districts,
  topbar/slot UI: cross-check `doc/mod_mechanics_reference.md`
  and `doc/mod_ui_reference.md`.
- Validation baseline: `tools/stellarisplus-quality-gate.ps1` and VS Code Problems.
- Expected duplicate keys in additive folders:
  `ambient_objects/`, `component_sets/`, `component_templates/`,
  `defines/`, `on_actions/`, `special_projects/`,
  `species_names/`. Dotted sprite names, scoped-flag suffix
  duplicates, and multiline quoted inline-script payloads can
  also be valid.

## Security

- Integrated mods must be added to `credits.md` with attribution.
- No external URLs, API keys, or credentials in mod files.

## Reference Documentation

Detailed domain knowledge lives in dedicated docs -- do not duplicate here.

| Topic | File |
| --- | --- |
| Load order, FIOS/LIOS/DUPL/MERGE, prefixes | `doc/mod_load_reference.md` |
| File/folder conventions | `doc/mod_defines_reference.md` |
| Core mechanics (slots, inline scripts, traditions, integrated mods) | `doc/mod_mechanics_reference.md` |
| UI layout, GFX/GUI modding | `doc/mod_ui_reference.md` |
| Paradox Script review rules | `.github/skills/stellaris-code-review/references/paradox-script-rules.md` |
