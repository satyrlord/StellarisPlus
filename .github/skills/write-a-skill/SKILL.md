---
name: write-a-skill
description: 'Create new Agent Skills for GitHub Copilot with proper structure, progressive disclosure, frontmatter, and optional bundled resources. Use when user wants to create, write, build, scaffold, duplicate, or template a new skill.'
---

# Writing Skills

## Purpose & Scope

Create and scaffold Agent Skills for GitHub Copilot, including:

- skill folder setup
- `SKILL.md` with valid frontmatter
- optional bundled resources (`scripts/`, `references/`, `assets/`,
  `templates/`)

Use this skill when creating a skill from scratch or duplicating an
existing template.

Spec: <https://agentskills.io/specification>

## Process

1. **Gather requirements** - ask user about:
   - What task/domain does the skill cover?
   - What specific use cases should it handle?
   - Does it need executable scripts or just instructions?
   - Any reference materials to include?

2. **Draft the skill** - create:
   - SKILL.md with concise instructions
   - Additional reference files if content exceeds 500 lines
   - Utility scripts if deterministic operations needed

3. **Review with user** - present draft and ask:
   - Does this cover your use cases?
   - Anything missing or unclear?
   - Should any section be more/less detailed?

## Naming Conventions

- Folder name: lowercase with hyphens (e.g. `my-new-skill/`).
- `name` field in frontmatter must match folder name exactly.
- Subdirectory names: `scripts/`, `references/`, `assets/`,
  `templates/` (lowercase, plural).
- Script files: descriptive names matching their purpose (e.g.
  `magnific_generate.py`, `pdx_validate.py`).

## Code Style

- SKILL.md body: standard markdown with `#` title and `##` sections.
- Frontmatter: YAML between `---` fences at the top of the file.
- Prefer lists of guidelines over dense paragraphs.
- Include code examples where they clarify usage.
- Keep body under 500 lines.

## Frontmatter Spec

```yaml
---
name: <skill-name>
description: '<WHAT it does>. Use when <triggers, keywords users might say>.'
---
```

| Field | Required | Constraints |
| ----- | -------- | ----------- |
| `name` | Yes | 1-64 chars, lowercase a-z/0-9/hyphens, must match folder name |
| `description` | Yes | 1-1024 chars, must contain WHAT + WHEN + keywords |
| `license` | No | License name or ref to LICENSE.txt |
| `compatibility` | No | 1-500 chars, environment reqs |
| `metadata` | No | Key-value pairs |
| `allowed-tools` | No | Space-delimited tool list (experimental) |

`description` is the primary discovery mechanism. Include capabilities,
trigger phrases, and keywords.

## Skill Structure

```text
skill-name/
├── SKILL.md              # Required
├── REFERENCE.md          # Detailed docs (if needed)
├── EXAMPLES.md           # Usage examples (if needed)
├── scripts/              # Executable automation (Python, Bash, JS)
├── references/           # Docs the agent reads (API refs, schemas)
├── assets/               # Static files used AS-IS (images, fonts)
└── templates/            # Starter code the agent modifies
```

## Scaffold Procedure

1. Create folder: `skills/<skill-name>/`
2. Create `SKILL.md` with frontmatter (see spec above).
3. Write body in markdown: title, purpose & scope, procedure,
   references.
4. Add optional subdirectories as needed.

## Validation Checklist

- [ ] Folder name: lowercase with hyphens.
- [ ] `name` matches folder name exactly.
- [ ] `description` is 10-1024 chars, explains WHAT and WHEN,
  single-quoted.
- [ ] Body under 500 lines.
- [ ] Bundled assets under 5MB each.

## Deep Reference

Use [REFERENCE.md](REFERENCE.md) for the SKILL.md template, description
requirements, when to add scripts, when to split files, and the review
checklist.
