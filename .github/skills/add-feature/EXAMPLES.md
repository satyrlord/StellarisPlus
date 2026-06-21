# Add Feature Examples — StellarisPlus

## Example 1: Document a New Tradition Tree

- Prompt shape: "Add a new ascension tradition tree for psionic empires."
- Good behavior: record the tradition IDs, swap rules, and event namespace in
  `doc/mod_mechanics_reference.md`; add a `doc/changelog.md` entry under the
  current version; add `# OVERRIDE:` comments in any override files.
- Good result: the next agent or maintainer knows which files define the
  tree, which vanilla traditions it interacts with, and why specific prefixes
  were chosen.

## Example 2: Record a Load-Order Decision

- Prompt shape: "Why does this district file use `zzzz_` instead of `zz_`?"
- Good behavior: capture the decision, rationale (must load after two other
  mods that also override districts), and consequences in
  `doc/mod_load_reference.md` and as a top-of-file `# OVERRIDE:` comment.
- Good result: future prefix changes or mod integrations don't accidentally
  break the load order.

## Example 3: Document an Inline Script Contract

- Prompt shape: "Define the parameter contract for the new zone slot inline
  script."
- Good behavior: add the parameter list (`$SLOT1$`, `$GOVERNMENT$`, etc.),
  expected callers, and validation rules to `doc/mod_mechanics_reference.md`.
- Good result: future script edits don't break callers by changing parameter
  names or order.
