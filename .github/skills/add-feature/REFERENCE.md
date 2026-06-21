# Add Feature Reference — StellarisPlus

## Durable Decision Workflow

Paradox Script explains what exists. Documentation explains why the mod chose
this shape instead of a nearby alternative.

Write durable documentation for:

- load-order strategy changes (prefix choice, FIOS vs LIOS vs MERGE)
- override decisions (which vanilla file, why `zz_sp_` vs `zzzz_sp_`)
- slot system contracts (inline script params, scripted variable conventions)
- cross-mod dependency choices (UI Overhaul Dynamic, integrated Workshop mods)
- resolved terminology conflicts that should stay consistent across docs

## Decision-Record Threshold

Record a decision durably only when all three are true:

- hard to reverse (changing a prefix or override target ripples across files)
- surprising without context (why this file uses `zzzz_` when others use `zz_`)
- the result of a real trade-off (load-order position vs compatibility)

## Where Decisions Live

This project does not use standalone ADRs or a `specs/` directory. Capture
durable decisions in the owning reference doc:

- load-order and prefix decisions → `doc/mod_load_reference.md`
- mechanics and system contracts → `doc/mod_mechanics_reference.md`
- UI and GFX conventions → `doc/mod_ui_reference.md`
- file type and folder rules → `doc/mod_defines_reference.md`
- what changed and why (per version) → `doc/changelog.md`
- override rationale (per file) → top-of-file `# OVERRIDE:` comment

Use the lightest structure that still records the trade-off clearly: one
small block stating context, decision, and why this path won. Add
`Considered Options` or `Consequences` sections only when they add genuine
value for the decision at hand.
