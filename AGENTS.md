# StellarisPlus Development Guidelines

## Scope

- **Root mod:** `descriptor.mod` (name = "StellarisPlus") --
  metadata only (name, tags, version, Workshop id).
- Gameplay source of truth is the root mod; changes live under `common/` and `interface/`.
- Integrated Workshop mods are credited in `credits.md`.
- User instructions override procedural and stylistic guidelines in this file, but do not override
the honesty rule (Never lie or fabricate information). When a user instruction would require dishonesty,
refuse and explain why.

## Approach & Efficiency

- Read existing files before writing. After making edits (including quality-gate fixes), re-read the
changed files to verify correctness before proceeding. Do not re-read files that you know have not changed.
- After each code change, scan VS Code Problems for all open/changed files and fix any reported
warnings or errors before proceeding to the next task. Do not leave known problems unresolved.
- During the `/stellaris-log-fix` and code review workflows, fix all errors encountered regardless
of whether they are pre-existing or introduced by recent changes.
- Prefer editing over rewriting. One focused coding pass;
  no write-delete-rewrite cycles.
- Be concise in output but thorough in reasoning. No
  sycophantic openers or closing fluff. No emoji.
- Keep solutions simple and direct. No over-engineering.
- Never guess or invent file paths or directory structures. For all other uncertain claims (mechanics,
behavior, compatibility), follow the Ethics & Honesty section: research first,
then label any remaining uncertainty explicitly as speculation.
- If a referenced documentation file (e.g., `doc/mod_load_reference.md`) cannot be read, stop and
notify the user: "Required reference file path is missing or unreadable.
Please provide it before proceeding." Do not proceed with assumptions about its content.
If the user responds that the file is unavailable and asks you to proceed anyway, treat any
decisions that would normally rely on that file as requiring explicit user confirmation for
each affected choice before acting.
- Before declaring done, run `tools/stellarisplus-quality-gate.ps1`, fix any reported errors, then
run it once more to confirm clean output. Do not declare done until the gate reports no errors.
If `tools/stellarisplus-quality-gate.ps1` cannot be executed (script not found, execution policy
error, or non-zero exit unrelated to mod errors), stop immediately and notify the user: "Quality
gate script failed to run: [error]. Cannot confirm clean output. Please resolve the script issue
before I proceed."
- Budget: 50 tool calls maximum. Each discrete tool invocation (file read, file write, terminal
command, web search) counts as one tool call regardless of payload size. Concurrent calls issued
in the same turn each count individually.
- Reserve at least 10 tool calls for the quality-gate cycle (first run + fixes + confirmation run).
If fewer than 10 calls remain before starting the gate, stop and inform the user before proceeding.
- If fewer than 5 tool calls remain and the task is incomplete, stop, report what has been completed,
list what remains, and ask the user how to proceed before making further calls.
- When a task has independent sub-investigations, issue all relevant tool calls within the same
response turn before synthesizing results, rather than issuing one call, waiting for its result,
then issuing the next.

## Naming Conventions

- Filename prefixes must match load-order strategy (see `doc/mod_load_reference.md`).
- LIOS overrides use `zz_sp_` prefix. `_replace` files only
  for replacing vanilla objects.
- Override prefixes (`zz_`, `zzzz_`) must be documented in both the file (as a top-of-file
  comment) and in `doc/changelog.md`. Add a comment at the top of the file in the form
  `# OVERRIDE: zz_sp_ — <reason for override, target vanilla file>` and a corresponding
  entry in `doc/changelog.md` under the current version heading.
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

- `/stellaris-log-fix` is a slash command the user may type in the chat. When received, treat it as
  explicit confirmation to run the log collection script and begin diagnosing the reported issue
  without asking for further confirmation.
- Collect logs into `tmp/_logs_inbox` **only** on explicit user
  request or `/stellaris-log-fix`:

  If the user describes a runtime error or crash without explicitly requesting log
  collection, ask: "Should I run the log collection script to gather diagnostics?"
  Do not run it without explicit confirmation.

  ```powershell
  & "tools/stellarisplus-collect-logs.ps1" -NoLaunch -IncludeException
  ```

- Run `spcollect` **only** when the user explicitly asks.
- Missing assets: check
  `C:\Program Files (x86)\Steam\steamapps\workshop\content\281990`
  or `...\common\Stellaris`.

## Ethics & Honesty

- Never lie to the user. Do not make up false information or fictional sources.
- Research the Stellaris forums (<https://forum.paradoxplaza.com/forum/forums/stellaris.900/>) and
subreddit (<https://old.reddit.com/r/Stellaris/>) before speculating about any vanilla issue.
If web browsing is unavailable in the current session, skip the research step, state explicitly
that web research was not possible, and proceed directly to the **Uncertainty Protocol**.
- When you are speculating, make it clear it is speculation.
- If something is a known issue, output the source URL for that information.
- **Uncertainty Protocol:** If you do not know something: (1) first search the Stellaris forums and
  subreddit; (2) if web research is inconclusive and the answer is critical to proceeding, ask the
  user one targeted clarifying question; (3) if the answer is not critical, state explicitly that
  you do not know and proceed with clearly labeled assumptions. An answer is critical if proceeding
  without it would require writing or deleting game files, or would produce output the user cannot
  easily revert. Otherwise it is non-critical.

## Testing

- Create a TODO list for each major change.
- Cross-check assumptions against actual vanilla/DLC/original mod files. For vanilla behavior not
directly verifiable from game files, follow the **Uncertainty Protocol** in the Ethics & Honesty
section.
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
