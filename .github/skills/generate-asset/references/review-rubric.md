# Review Rubric

## Framing Consistency (hard requirement)

- Is the subject a centered bust portrait at eye level with no tilt or
  extreme perspective? (This is locked by `FRAMING_ANCHOR`; any
  candidate that deviates must be marked `reject`.)
- Are the shoulders to crown clearly visible, with the head and upper
  chest occupying the lower two-thirds of the generated frame?

## Visual Fit

- Does the candidate match the pack's existing species and material
  language?
- Does the candidate preserve the expected mood of the pack?
- Does the face remain readable in centered bust framing?

## Technical Fit

- Is the background simple enough for clean cutout work?
- Are edges, horns, ears, crowns, or neck details likely to survive DDS
  conversion and in-game scale?
- Are there anatomy or artifact issues that will become more obvious at
  portrait size?

## Integration Fit

- Does the candidate align with the pack's naming and numbering scheme?
- Does the pack have ruler or role splits that require a dedicated
  candidate rather than a generic one?
- Is the pack a shared-root or multi-category case that increases risk?

## Special Cases

- `sl_deathmachine`: keep the machine read strong and avoid soft organic
  facial cues
- `sl_demon`: preserve infernal identity without losing humanoid
  readability
- `sl_highelf`: keep ruler and standard pools distinct when reviewing
  candidates for production use
