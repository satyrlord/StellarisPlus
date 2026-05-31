---
name: edit-a-skill
description: >
  Updates existing agent skills with proper structure, progressive disclosure,
  and bundled resources. Use when user wants to edit, revise, update,
  refactor, or improve an existing skill.
---

# Editing Skills

## Process

1. **Read the existing skill first** - load the target skill folder:
   - `SKILL.md` and any bundled files (`REFERENCE.md`, `EXAMPLES.md`,
     `scripts/`)
   - nearby references the skill points to
   - repo routing that mentions the skill (for example `AGENTS.md`) when name,
     scope, or triggers change

2. **Gather change requirements** - ask user about:
   - What should change and what must stay the same?
   - New use cases, removed scope, or trigger wording updates?
   - Should instructions move into or out of bundled files or scripts?
   - Any reference materials to add, replace, or remove?

3. **Apply focused edits** - change only what the request needs:
   - update `SKILL.md` and bundled files in place
   - split or merge files when size or domain boundaries require it
   - add, update, or remove utility scripts when deterministic operations change
   - update repo routing docs when the skill's name, description, or role
     changes

4. **Review with user** - present the diff and ask:
   - Does this cover the requested changes without breaking existing use cases?
   - Anything missing, unclear, or over-edited?
   - Should any section be more or less detailed?

## Skill Structure

```text
skill-name/
├── SKILL.md           # Main instructions (required)
├── REFERENCE.md       # Detailed docs (if needed)
├── EXAMPLES.md        # Usage examples (if needed)
└── scripts/           # Utility scripts (if needed)
    └── helper.js
```

Preserve this layout unless the edit intentionally reorganizes the skill.

## Deep Reference

Use [REFERENCE.md](REFERENCE.md) for description requirements, when to add
scripts, when to split files, and the edit checklist.
