---
name: handoff
description: 'Handoff current work to another agent in a concise tmp/ artifact. Use when the user or another local skill requires resumable session context.'
argument-hint: "What will the next session be used for?"
---

# Handoff

## Steps

1. Inspect the current task, worktree, plans, verification evidence, and durable
   artifacts. Distinguish confirmed facts from hypotheses and unfinished work.
2. Write a concise handoff under repository-root `tmp/`, not OS `/tmp`.
3. Link existing PRDs, plans, ADRs, issues, commits, diffs, and evidence instead
   of copying their contents.
4. Re-read the handoff and verify every path, command, blocker, and suggested
   skill against the current repository.

Include a suggested-skills section containing only skills present in
`.github/skills/SKILLS.md`.

Redact any sensitive information, such as API keys, passwords, or personally
identifiable information.

If the user passed arguments, treat them as a description of what the next
session will focus on and tailor the doc accordingly.

Example handoff filename: `tmp/handoff-import-parity.md`.

Minimal structure example:

```markdown
# Session Handoff

- Scope: isolate a runtime regression in a Stellaris script
- Current state: failing log signature captured; root cause unconfirmed
- Next step: reproduce the failure with one candidate change set
- Suggested skills: ablation-test, stellaris-log-fix
```

## Completion Criteria

The handoff is complete only when a fresh agent can identify the exact scope,
confirmed state, remaining work, next executable step, validation commands,
blockers, and relevant existing artifacts without relying on this conversation;
all paths and suggested skills resolve; and sensitive information is absent.
