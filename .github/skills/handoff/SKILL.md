---
name: handoff
description: 'Creates a concise continuation handoff document for another agent and stores it under tmp/. Use when the user asks to hand off current progress, preserve session context, prepare the next agent run, or when another local workflow explicitly requires a handoff artifact.'
argument-hint: "What will the next session be used for?"
---

# Handoff

## Purpose & Scope

Write a handoff document summarising the current conversation so a fresh agent
can continue the work. Save under `tmp/` at the repository root (not the OS
`/tmp` directory).

Include a "suggested skills" section in the document, which suggests skills that
the agent should invoke.

Do not duplicate content already captured in other artifacts (PRDs, plans, ADRs,
issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally
identifiable information.

If the user passed arguments, treat them as a description of what the next
session will focus on and tailor the doc accordingly.

Example handoff filename: `tmp/handoff-import-parity.md`.

Minimal structure example:

```markdown
# Session Handoff
- Scope: legacy mix parity mismatch for one song
- Current state: diff list captured, root cause still unconfirmed
- Next step: validate sample reference resolver mapping for affected product
- Suggested skills: debugging-and-error-recovery, planning-and-task-breakdown
```
