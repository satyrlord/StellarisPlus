# StellarisPlus Skills Router

Thin dispatcher — read this first when deciding which skill to invoke.
For full workflows and step-by-step instructions, follow the link to the
individual skill.

## Quick Lookup

This index uses one leading need per branch. Each linked skill description is
the source of truth for full model-invocation wording.

| Leading need | Skill |
| --- | --- |
| Absorb or remove an external mod | [absorb-mod](absorb-mod/SKILL.md) |
| Update one integrated mod | [update-mod](update-mod/SKILL.md) |
| Scan all integrated mods for updates | [scan-updates](scan-updates/SKILL.md) |
| Consolidate local files | [merge-local-files](merge-local-files/SKILL.md) |
| Diagnose explicitly requested runtime logs | [stellaris-log-fix](stellaris-log-fix/SKILL.md) |
| Review mod changes | [stellaris-code-review](stellaris-code-review/SKILL.md) |
| Run the complete release-validation sequence | [full-build](full-build/SKILL.md) |
| Isolate a minimal causal fix | [ablation-test](ablation-test/SKILL.md) |
| Preserve resumable session context | [handoff](handoff/SKILL.md) |
| Design or improve a skill | [writing-great-skills](writing-great-skills/SKILL.md) |

## Skill categories

### Mod lifecycle

- **Absorb** a new external mod → [absorb-mod](absorb-mod/SKILL.md)
- **Update** an already-integrated mod → [update-mod](update-mod/SKILL.md)
- **Scan** all integrated mods for upstream updates → [scan-updates](scan-updates/SKILL.md)
- **Merge** / consolidate internal files → [merge-local-files](merge-local-files/SKILL.md)

### Quality & validation

- **Quality gate + manual test + log-fix + code review** → [full-build](full-build/SKILL.md)
- **Code review** (Paradox Script, load order, loc, GFX, docs) → [stellaris-code-review](stellaris-code-review/SKILL.md)
- **Log fix** (collect + analyze + auto-fix runtime errors) → [stellaris-log-fix](stellaris-log-fix/SKILL.md)

### Debugging & meta

- **Ablation test** (isolate root cause of a hard bug) → [ablation-test](ablation-test/SKILL.md)
- **Handoff** (write continuation doc for the next agent) → [handoff](handoff/SKILL.md)
- **Skill authoring** (write or edit skills) → [writing-great-skills](writing-great-skills/SKILL.md)

## Decision flowchart

```text
User request
  ├─ Adding/removing a Workshop mod?         → absorb-mod
  ├─ Updating an already-integrated mod?     → update-mod
  ├─ Checking ALL integrated mods for updates? → scan-updates
  ├─ Consolidating internal files?           → merge-local-files
  ├─ Runtime errors after a test run?        → stellaris-log-fix
  ├─ Reviewing code/script quality?          → stellaris-code-review
  ├─ Full pre-release sweep?                 → full-build
  ├─ Isolating a hard-to-find bug?           → ablation-test
  ├─ Handing off to another agent?           → handoff
  ├─ Writing/editing a skill?                → writing-great-skills
  └─ None of the above?                      → no skill needed
```
