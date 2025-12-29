# Copilot instructions (Stellaris mod workspace)

## What this repo is
- This workspace contains the StellarisPlus mod:
  - Root mod: `descriptor.mod` (name = "StellarisPlus").
  - Archived Workshop mods under `backup/<workshop_id>/` (each has its own `descriptor.mod`, `common/`, `interface/`, `help/`).
- **Active gameplay source of truth is the root mod only** (folders under `backup/` are not active development targets).
- Treat each `backup/<id>/` folder as **self-contained reference material**; don’t mix files across IDs unless explicitly asked.

## What `descriptor.mod` is (and isn’t)
- `descriptor.mod` is the mod’s **metadata/description** (name, tags, supported version, Workshop id in snapshots).
- It is **not** gameplay/script logic; gameplay changes live under folders like `common/` and `interface/`.

## Load order and mod override reference
- Keep mod load order and override guidance out of this file.
- Use `help/mod_load_reference.md` for filename prefix conventions and related override notes.

## File types reference
- Keep file layout guidance out of this file.
- Use `help/mod_defines_reference.md` for file/folder conventions (common/, defines, scripted_variables, inline_scripts, etc.).

## Mechanics reference
- Keep gameplay/mechanics guidance out of this file.
- Use `help/mod_mechanics_reference.md` for core mechanics documentation (slot variables, inline scripts, and related patterns).

## UI reference
- Keep UI/layout guidance out of this file.
- Use `help/mod_ui_reference.md` as the consolidated reference for UI-related notes and other modding how-tos.

## When making changes, follow these repo-specific rules
- Never edit anything under `backup/` unless explicitly asked. That folder is intended to be deleted once work is done.
- Keep Paradox Script formatting stable (tabs/CRLF are common here); avoid “pretty reformatting”.
- Integrated mods should be added to credits.txt
- No emoji anywhere, neither in the code, nor in the documentation.
- Create a TODO list for each major change.
