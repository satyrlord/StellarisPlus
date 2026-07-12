---
name: handoff
description: 'Handoff current work to another agent in a concise tmp/ artifact. Use when the user or another local skill requires resumable session context.'
---

# Handoff

## Steps

1. Inspect the current task, worktree, plans, verification evidence, and durable
   artifacts. Finish only when every relevant item is classified as confirmed,
   hypothetical, complete, remaining, or blocked.
2. Write a concise handoff under repository-root `tmp/`, not OS `/tmp`.
   Finish only when it states the exact scope, current state, remaining work,
   next executable step, validation commands, and blockers.
3. Link existing PRDs, plans, ADRs, issues, commits, diffs, and evidence instead
   of copying their contents. Finish only when every relevant durable artifact
   is linked or explicitly recorded as absent.
4. Re-read the handoff. Finish only when every path and command resolves, every
   suggested skill exists in `.github/skills/SKILLS.md`, and API keys,
   passwords, and personally identifiable information are absent.

If the user passed arguments, treat them as a description of what the next
session will focus on and tailor the doc accordingly.

Example handoff filename: `tmp/handoff-import-parity.md`.

Minimal structure example:

```markdown
# Session Handoff

- Scope: isolate a runtime regression in a Stellaris script
- Current state: failing log signature captured; root cause unconfirmed
- Remaining work: ablate the two candidate change groups
- Next step: reproduce the failure with one candidate change set
- Validation: `tools/stellarisplus-quality-gate.ps1`; repeat the captured repro
- Blockers: none
- Artifacts: `tmp/verify-runtime-regression/evidence.md`
- Suggested skills: ablation-test, stellaris-log-fix
```

## Completion Criteria

The handoff is complete only when all four step criteria are satisfied and a
fresh agent can resume from the next executable step without this conversation.
