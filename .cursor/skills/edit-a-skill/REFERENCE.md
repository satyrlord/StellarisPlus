# Editing Skills Reference

## Description Requirements

The description is **the only thing your agent sees** when deciding which skill
to load. It's surfaced in the system prompt alongside all other installed
skills. Your agent reads these descriptions and picks the relevant skill based
on the user's request.

**Goal**: Give your agent just enough info to know:

1. What capability this skill provides
2. When/why to trigger it (specific keywords, contexts, file types)

**Format**:

- Max 1024 chars
- Write in third person
- First sentence: what it does
- Second sentence: "Use when [specific triggers]"

**Good example**:

```text
Extract text and tables from PDF files, fill forms, merge documents.
Use when working with PDF files or when the user mentions PDFs, forms, or
document extraction.
```

**Bad example**:

```text
Helps with documents.
```

When editing, treat description changes as trigger changes. Update routing docs
if the skill's role or invocation wording changed materially.

## When to Add Scripts

Add or update utility scripts when:

- Operation is deterministic (validation, formatting)
- Same code would be generated repeatedly
- Errors need explicit handling

Scripts save tokens and improve reliability vs generated code.

## When to Split Files

Split into separate files when:

- SKILL.md exceeds 100 lines
- Content has distinct domains (finance vs sales schemas)
- Advanced features are rarely needed

When splitting during an edit, move content out of `SKILL.md` instead of letting
it keep growing.

## Edit Checklist

After editing, verify:

- [ ] Existing triggers still work, or routing/docs were updated intentionally
- [ ] Description includes triggers ("Use when...")
- [ ] `SKILL.md` under 100 lines, or overflow moved to bundled files
- [ ] No time-sensitive info
- [ ] Consistent terminology with the rest of the skill folder
- [ ] Concrete examples still match the edited workflow
- [ ] References stay one level deep
- [ ] Bundled files and scripts match the updated instructions
- [ ] Repo routing mentions the skill correctly when its role changed

For net-new skills rather than edits, use
[write-a-skill](../write-a-skill/SKILL.md).
