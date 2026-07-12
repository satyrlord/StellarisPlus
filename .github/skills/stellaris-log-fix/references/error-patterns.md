# Log Error Patterns

Reference patterns for `.github/skills/stellaris-log-fix/SKILL.md`.
Use these rules to classify runtime log entries before deciding whether
to fix, skip, or only report them.

## Ownership First

Classify ownership before classifying the error type.

| Situation | Ownership | Action |
| --- | --- | --- |
| Logged file exists in this workspace | Mod-owned | Investigate and fix if valid |
| Logged asset or entity exists in this workspace | Mod-owned | Investigate and fix if valid |
| Logged file does not exist in this workspace | External or stale | Skip unless user asks for override |
| Logged file belongs to integrated Workshop content in `credits.md` | Mod-owned integration | Investigate and fix if valid |
| Vanilla error with no workspace override | Vanilla | Skip unless user asks for override |

## Pattern Table

| Log Pattern | Category | Typical Meaning | Default Action |
| --- | --- | --- | --- |
| `Wrong scope for trigger` | Script Error | Trigger used in invalid scope | Fix root cause in referenced script |
| `Error in scripted trigger, cannot find:` | Script Error | Invalid or obsolete trigger usage | Fix or remove stale logic |
| `Unexpected token` | Script Error | Invalid syntax or deprecated field | Fix syntax or remove key |
| `is not a valid property` | Script Error | Unsupported block key | Fix or remove invalid property |
| `Missing effects tradition` | Script Error | Empty or unsupported tradition effect | Restore valid modifier or tooltip |
| `Missing effects tradition swap` | Script Error | Empty swapped tradition effect | Restore valid swapped effect or tooltip |
| `Could not find animation` | Missing File/Asset | Entity points at missing mesh animation | Fix mesh or entity reference |
| `Duplicate of ... added to entity system` | Missing GFX/Sprite | Same entity declared twice | Remove duplicate definition |
| `No icon` | Missing GFX/Sprite | Missing modifier icon or sprite link | Add sprite or report if external |
| `No sprite` | Missing GFX/Sprite | Missing sprite definition | Add sprite to owned `.gfx` or `.asset` |
| `Missing localisation` | Missing Localisation | Localisation key absent | Add key to owned English localisation |
| `Could not find relic with key` | External Mod Noise by default | Compatibility probe for absent external relics | Skip unless support is owned here |
| `Duplicate Texture` | Duplicate Texture (INFO) | Benign duplicate texture registration | Report only |
| `Missing sound category` | Missing Sound Category | Missing audio category definition | Auto-fix if owned |

## High-Confidence Skip Rules

Skip without editing when any of the following are true.

| Pattern | Reason |
| --- | --- |
| Compatibility probe whose path is absent from this workspace and all credited integrations | External compatibility noise |
| `game.log` galaxy generation warnings with no workspace file | Non-actionable runtime noise |

## High-Confidence Fix Rules

Fix directly when any of the following are true.

| Pattern | Fix Strategy |
| --- | --- |
| Workspace file path appears in the log line | Read 20+ lines around the reference and fix the root cause |
| Workspace entity or mesh name appears in the log | Read the owning `.asset` or `.gfx` and repair the reference |
| Tradition or decision block is effectless or uses stale scope logic | Compare with upstream or vanilla pattern, then restore a valid form |
| Parser cascade follows an encoding issue | Fix encoding first, then reassess remaining errors |
