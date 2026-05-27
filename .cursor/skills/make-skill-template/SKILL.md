---
name: make-skill-template
description: >-
    Create new Agent Skills for GitHub Copilot from prompts or by
    duplicating this template. Use when asked to "create a skill", "make
    a new skill", "scaffold a skill", or when building specialized AI
    capabilities with bundled resources. Generates SKILL.md files with
    proper frontmatter, directory structure, and optional
    scripts/references/assets folders.
---

# Make Skill Template

## Purpose & Scope

Scaffold new Agent Skills for GitHub Copilot: create skill folder,
SKILL.md with frontmatter, and optional bundled resources. Use this
skill whenever creating a new skill from scratch or duplicating an
existing one.

Spec: <https://agentskills.io/specification>

---

## Naming Conventions

- Folder name: lowercase with hyphens (e.g. `my-new-skill/`).
- `name` field in frontmatter must match folder name exactly.
- Subdirectory names: `scripts/`, `references/`, `assets/`,
  `templates/` (lowercase, plural).
- Script files: descriptive names matching their purpose (e.g.
  `magnific_generate.py`, `pdx_validate.py`).

## Code Style

- SKILL.md body: standard markdown with `#` title, `##` sections.
- Frontmatter: YAML between `---` fences at the top of the file.
- Prefer lists of guidelines over dense paragraphs.
- Include code examples where they clarify usage.
- Keep body under 500 lines.

---

## Frontmatter Spec

```yaml
---
name: <skill-name>
description: '<WHAT it does>. Use when <triggers, keywords users might
say>.'
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

> `description` is the primary discovery mechanism. Include
> capabilities, trigger phrases, and keywords.

---

## Directory Structure

```text
<skill-name>/
  SKILL.md              # Required
  scripts/              # Executable automation (Python, Bash, JS)
  references/           # Docs the agent reads (API refs, schemas)
  assets/               # Static files used AS-IS (images, fonts)
  templates/            # Starter code the agent modifies
```

---

## Scaffold Procedure

1. Create folder: `skills/<skill-name>/`
2. Create `SKILL.md` with frontmatter (see spec above).
3. Write body in markdown: title, purpose & scope, procedure,
   references.
4. Add optional subdirectories as needed.

---

## Validation Checklist

- [ ] Folder name: lowercase with hyphens.
- [ ] `name` matches folder name exactly.
- [ ] `description` is 10-1024 chars, explains WHAT and WHEN,
  single-quoted.
- [ ] Body under 500 lines.
- [ ] Bundled assets under 5MB each.
