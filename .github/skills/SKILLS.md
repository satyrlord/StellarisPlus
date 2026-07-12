# StellarisPlus Skills Router

Thin dispatcher — read this first when deciding which skill to invoke.
For full workflows and step-by-step instructions, follow the link to the
individual skill.

## Quick-lookup table

| User says / needs | Skill to invoke |
|---|---|
| "absorb mod", "integrate mod", "merge mod", "import mod", "add Workshop mod", "include mod", "copy mod into StellarisPlus" | [absorb-mod](absorb-mod/SKILL.md) |
| "undo absorb", "remove mod", "revert mod", "unmerge mod", "de-integrate mod" | [absorb-mod](absorb-mod/SKILL.md) |
| "update mod", "refresh mod", "sync mod", "upgrade mod", "re-sync mod", "pull latest mod", "update Workshop mod", "update integrated mod" | [update-mod](update-mod/SKILL.md) |
| "scan updates", "check mod updates", "find outdated integrated mods", "refresh integrated mods", "update all outdated mods" | [scan-updates](scan-updates/SKILL.md) |
| "merge local files", "consolidate files", "reduce file count", "merge mod files", "file consolidation", "clean up files", "merge duplicate files" | [merge-local-files](merge-local-files/SKILL.md) |
| "fix errors", "check logs", "analyze logs", "spcollect", "log fix", "runtime errors", "error log", `/stellaris-log-fix` | [stellaris-log-fix](stellaris-log-fix/SKILL.md) |
| "code review", "full code review", "merge-readiness check", "pre-release audit", "comprehensive quality sweep", "review changes", "check script", "validate mod", "review mod", "review project", "script review" | [stellaris-code-review](stellaris-code-review/SKILL.md) |
| "full build", "full validation", "run everything", "pre-release sweep", "end-to-end check", "build and review" | [full-build](full-build/SKILL.md) |
| "ablation test", "which change actually fixed it", "what was unnecessary", "minimal fix" | [ablation-test](ablation-test/SKILL.md) |
| "hand off", "preserve session context", "prepare the next agent run", "handoff" | [handoff](handoff/SKILL.md) |
| "writing a skill", "editing a skill", "improving a skill", "skill design", "skill conventions", "skill vocabulary" | [writing-great-skills](writing-great-skills/SKILL.md) |

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

```
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
