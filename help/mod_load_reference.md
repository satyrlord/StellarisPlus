# StellarisPlus — Load / Override Reference

This document describes load-order and override conventions used in this workspace.

---

## Load-Order And Override Conventions

The codebase relies on **alphabetical load order** via filename prefixes:

- `zz_*.txt` / `z_*.txt` for “late” scripted variables/defines.
- `000_*.txt` for “early” compatibility variables.
- `!!!*.txt` for “very early” compatibility variables.

Preserve existing prefixes when editing, and choose a prefix intentionally when adding new override files.
