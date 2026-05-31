# StellarisPlus -- Portrait Reference

## Purpose & Scope

Reference for the current Stellar Legions portrait implementation in
StellarisPlus. This document summarizes where the portraits are wired,
which categories they use, and how expensive common portrait changes
are likely to be.

The exhaustive DDS manifest lives in
[mod_portrait_manifest.md](mod_portrait_manifest.md).

---

## Source Files

- `common/portrait_categories/slreup_portrait_categories.txt`
- `common/portrait_sets/zz_sp_portrait_sets.txt`
- `gfx/portraits/portraits/sl_*_portraits.txt`
- `gfx/models/portraits/sl_shared/_humanoid_portrait_entities.asset`

## Current Structure

- 32 Stellar Legions portrait groups are currently wired into the mod.
- Those groups reference 2,804 unique DDS texture paths.
- All current Stellar Legions portrait scripts use the shared entity
  `sl_humanoid_01_entity`.
- The shared entity is defined in
  `gfx/models/portraits/sl_shared/_humanoid_portrait_entities.asset`
  and currently uses the humanoid mesh `portrait_humanoid_01_mesh`.
- The portrait scripts consistently use
  `clothes_selector = "no_texture"` and
  `attachment_selector = "no_texture"`, so most work is texture- and
  script-driven rather than clothing-attachment-driven.
- Most groups use a dedicated texture root that matches the group
  name.

### Special Cases

- `sl_earthgiant` and `sl_diamondgiant` both reference the shared
  texture root `gfx/models/portraits/sl_giant/`.
- `sl_savagedespoiler` uses the plural texture directory
  `gfx/models/portraits/sl_savagedespoilers/`.
- Multi-category groups must be treated as cross-category content when
  reassigning, removing, or renaming them.

---

## Current Portrait Map

| Group | Categories | DDS count | Structure notes |
| --- | --- | ---: | --- |
| `sl_amazonian` | `humanoids` | 80 | standard two-gender pool with indeterminable variant |
| `sl_android` | `machines` | 76 | standard two-gender pool |
| `sl_banshee` | `humanoids`, `necroids` | 50 | multi-category, indeterminable variant |
| `sl_crystaloid` | `lithoids` | 59 | indeterminable variant |
| `sl_cyberpunk` | `humanoids` | 125 | large pool, scientist-specific split |
| `sl_darkelf` | `humanoids` | 106 | fighter and ruler splits |
| `sl_deathless` | `humanoids`, `necroids` | 119 | multi-category, governor/scientist/fighter splits |
| `sl_deathmachine` | `machines` | 20 | 10 male + 10 female MVP pool |
| `sl_demon` | `humanoids`, `infernals` | 74 | multi-category standard two-gender pool |
| `sl_diamondgiant` | `lithoids` | 40 | shared `sl_giant` texture root |
| `sl_dragon` | `reptilians` | 120 | very large pool |
| `sl_drow` | `humanoids`, `necroids` | 109 | multi-category large pool |
| `sl_earthgiant` | `humanoids`, `lithoids` | 40 | shared `sl_giant` texture root, multi-category |
| `sl_egypt` | `humanoids` | 133 | admiral/general/governor/scientist splits |
| `sl_fungoid` | `fungoids` | 62 | standard two-gender pool |
| `sl_harpy` | `avians` | 35 | simple single-pool structure |
| `sl_highelf` | `humanoids` | 159 | very large pool, ruler split |
| `sl_holy` | `humanoids` | 106 | ruler split |
| `sl_kitsune` | `mammalians` | 50 | simple single-pool structure |
| `sl_megacorp` | `humanoids` | 150 | governor/scientist/fighter splits |
| `sl_mermaid` | `aquatics`, `humanoids` | 80 | multi-category standard two-gender pool |
| `sl_militarium` | `humanoids` | 120 | admiral/general/governor/scientist splits |
| `sl_norse` | `humanoids` | 85 | standard two-gender pool |
| `sl_nymph` | `plantoids` | 45 | simple single-pool structure |
| `sl_oceanid` | `aquatics` | 49 | simple single-pool structure |
| `sl_savagedespoiler` | `humanoids` | 69 | standard two-gender pool, plural texture root |
| `sl_shogun` | `humanoids` | 125 | governor/scientist/fighter splits |
| `sl_snake` | `reptilians` | 65 | standard two-gender pool |
| `sl_toxic` | `toxoids` | 74 | standard two-gender pool |
| `sl_UNE` | `humanoids` | 240 | largest pool, admiral/general/governor/scientist splits |
| `sl_wakanda` | `humanoids` | 83 | standard two-gender pool |
| `sl_were` | `mammalians` | 40 | ruler split, compact pool |

---

## Effort Analysis

### Lowest-Cost Changes

These are usually texture-only or near-texture-only jobs:

- Repaint, cleanup, or replace DDS files without changing numbering,
  portrait keys, or group logic.
- Reassign an existing portrait group to a different category when no
  new portrait blocks are needed.
- Duplicate a simple single-pool portrait as a starting template.

Best low-effort templates in the current repo:

- `sl_harpy`
- `sl_nymph`
- `sl_oceanid`
- `sl_kitsune`
- `sl_deathmachine`

Why they are low effort:

- Small DDS pools.
- No leader-class specialization.
- No extra clothes or attachment layers.
- Same shared entity and mesh as the rest of the SL portrait family.

### Medium-Cost Changes

These typically require both DDS work and script updates, but still
stay inside the existing SL portrait pattern:

- Adding or replacing standard male/female pools.
- Renaming a group and keeping set/category mappings in sync.
- Moving a group between one or more existing categories.
- Cloning a regular two-gender portrait family into a new set.

Typical medium-effort templates:

- `sl_amazonian`
- `sl_android`
- `sl_banshee`
- `sl_crystaloid`
- `sl_demon`
- `sl_fungoid`
- `sl_mermaid`
- `sl_norse`
- `sl_savagedespoiler`
- `sl_snake`
- `sl_toxic`
- `sl_wakanda`

Why they land in the middle:

- They usually have one texture root and a single portrait group.
- They often have two-gender or indeterminable coverage that must stay
  coherent across `species`, `pop`, `leader`, and `ruler` blocks.
- Some also have multi-category exposure, so category edits affect
  more than one species setup menu.

### High-Cost Changes

These are the portrait families most likely to require careful script
maintenance, large texture batches, and deeper regression checks:

- `sl_cyberpunk`
- `sl_darkelf`
- `sl_deathless`
- `sl_dragon`
- `sl_drow`
- `sl_egypt`
- `sl_highelf`
- `sl_holy`
- `sl_megacorp`
- `sl_militarium`
- `sl_shogun`
- `sl_UNE`

Why they are expensive:

- They have large DDS inventories.
- Several split portraits by role, such as `admiral`, `general`,
  `governor`, `scientist`, `fighter`, or `ruler`.
- Script edits must preserve leader, ruler, species, and pop scope
  behavior together.
- A rename or folder move affects many more texture references.

### Special Risk Cases

- `sl_earthgiant` and `sl_diamondgiant` are not independent texture
  families. They share the same `sl_giant` DDS pool, so changes to
  that directory affect both portrait groups.
- Any multi-category group such as `sl_banshee`, `sl_deathless`,
  `sl_demon`, `sl_drow`, `sl_earthgiant`, or `sl_mermaid` needs both
  category and set mapping reviewed before changes are considered safe.
- `sl_savagedespoiler` is internally consistent now, but its texture
  folder remains pluralized. Future rename work should preserve that
  distinction unless the asset folder is also migrated.

---

## Creating New Portrait Sets

### Low Effort Path

Use this when the new set can follow the existing SL humanoid entity
pattern and only needs one compact portrait pool.

Good starting templates:

- `sl_harpy`
- `sl_nymph`
- `sl_oceanid`
- `sl_kitsune`

Expected work:

1. Add new DDS textures under a dedicated root in
   `gfx/models/portraits/`.
2. Clone a simple portrait script under
   `gfx/portraits/portraits/`.
3. Add a set entry in `common/portrait_sets/zz_sp_portrait_sets.txt`.
4. Wire the set into a category in
   `common/portrait_categories/slreup_portrait_categories.txt`.

### Medium Effort Path

Use this when the new set needs male/female pools or category reuse,
but not role-specific leader pools.

Good starting templates:

- `sl_demon`
- `sl_mermaid`
- `sl_snake`
- `sl_toxic`
- `sl_wakanda`
- `sl_savagedespoiler`

Expected work above the low-effort path:

- More DDS authoring.
- Two-gender scope coverage.
- More chances to break naming consistency between portrait keys,
  group names, set names, and folder names.

### High Effort Path

Use this when the new set needs dedicated leader-class pools or wants
the same level of specialization as the large humanoid families.

Good starting templates:

- `sl_egypt`
- `sl_militarium`
- `sl_UNE`
- `sl_megacorp`
- `sl_shogun`

Expected work above the medium-effort path:

- Role-specific portrait blocks for multiple leader classes.
- Many more DDS files to keep visually coherent.
- Higher maintenance cost when rebalancing group behavior later.

### Beyond Current SL Pattern

If a new portrait set cannot reuse `sl_humanoid_01_entity`, effort
increases beyond the current Stellar Legions baseline.

That work would likely require:

- A new entity definition in `gfx/models/portraits/*.asset`.
- Validation of mesh, scale, and animation behavior.
- Additional testing beyond the current texture-only workflow.

---

## Practical Edit Checklist

When changing an existing Stellar Legions portrait family:

1. Update DDS assets in the matching texture root.
2. Update the matching portrait script in
   `gfx/portraits/portraits/sl_*_portraits.txt` if any portrait key,
   scope block, or sound mapping changes.
3. Update `common/portrait_sets/zz_sp_portrait_sets.txt` if the group
   name or set membership changes.
4. Update `common/portrait_categories/slreup_portrait_categories.txt`
   if category placement changes.
5. Re-check any shared-root or multi-category side effects.

For the exhaustive DDS inventory, see
[mod_portrait_manifest.md](mod_portrait_manifest.md).
