# sl_deathmachine Prompt Template

## Pack Identity

- Category: `machines`
- Texture root: `gfx/models/portraits/sl_deathmachine/`
- Current state: 10 male (`male_deathmachine_01-10`) + 10 female
  (`female_deathmachine_01-10`), validated in-game
- Visual direction: compact machine portrait, polished or blackened
  metal skull, bright amber optics, severe symmetry, minimal organic
  cues

## Base Prompt

The script prepends `FRAMING_ANCHOR` automatically. Supply only the
variable parts (species identity, skin/color, accessories, nudity, background):

```text
female biomechanical skull, polished black metal plating, glowing amber eyes,
elegant mechanical neck assembly, hard-surface details, plain dark background,
crisp studio lighting, readable silhouette, no text, no watermark
```

## Negative Prompt Ideas

- human skin
- soft organic face
- generous chest
- uncensored body
- hair
- text
- watermark
- transparent background
- extra heads
- extra eyes
- asymmetrical broken jaw

## API One-Off Example

```text
front-facing female biomechanical commander portrait, centered bust,
polished black metal skull, amber optics, clean dark background, no text
```

## Shortlist Notes

- Good first use case for Mystic `editorial_portraits` model
- Good production shortlist candidate via `POST /v1/ai/mystic`
- If the result is approved, remove the background and convert to
  `BC3RgbaUnorm` DDS

## Naming Targets

- Next male variant: `male_deathmachine_11.dds`
- Next female variant: `female_deathmachine_11.dds`
- Follow zero-padded two-digit numbering (`_11`, `_12`, ...)
