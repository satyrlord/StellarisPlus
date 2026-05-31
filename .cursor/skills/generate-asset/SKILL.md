---
name: generate-asset
description: 'Generate, review, and integrate image assets for Stellaris mods using the Magnific HTTP API. Covers portrait artwork for named portrait packs and general UI assets (icons, textures, sprites). Use when user says "generate portrait", "create portrait", "make portrait", "generate art", "review portrait", "integrate portrait", "fix missing asset", "generate texture", "create icon", "missing dds", "generate dds", "create sprite", or when stellaris-log-fix reports missing textures/sprites that need new artwork.'
argument-hint: '<asset-type> [portrait-pack]'
metadata:
  requires:
    bins:
      - pwsh
      - uv
      - python
      - cargo
      - git
    env:
      - MAGNIFIC_API_KEY
---

# Generate Asset

## Purpose & Scope

Generate, review, and integrate image assets for Stellaris mods. This
skill covers two asset categories:

- **Portraits** -- artwork for named portrait packs (Stellar Legions
  families such as `sl_deathmachine`). These follow a pack-specific
  lifecycle: generation, candidate review, and live integration.
- **UI assets** -- icons, textures, and sprites for game elements
  (traditions, buildings, districts, modifiers, traits, edicts,
  technologies, flags, ships). These follow a generate-resize-convert
  pipeline.

All generation goes through the Magnific HTTP API
(`https://api.freepik.com`). Authentication uses the legacy
`x-freepik-api-key` header with the key stored in `.env.local`
(`MAGNIFIC_API_KEY` preferred, `FREEPIK_API_KEY` supported).

- All intermediate files go into `tmp/` (git-ignored).
- Only verified, approved files move to their final live paths.

Bundled resources:

- [Stellaris DDS formats](references/stellaris-dds-formats.md)
- [Portrait reference](references/mod_portrait_reference.md)
- [Portrait manifest](references/mod_portrait_manifest.md)
- [Magnific API reference](references/magnific-api.md)
- [Portrait Quality Report](references/portrait_quality_report.md)
- [Review rubric](references/review-rubric.md)
- [UI asset workflow](references/ui-asset-workflow.md)
- [Review report template](assets/review-report-template.md)
- [Example prompt](assets/sl_deathmachine.prompt.md)
- [Portrait generation script](scripts/generate_portrait.py)

---

## API Setup (UI Asset Workflow only)

The portrait workflow uses the bundled Python script, which loads
`MAGNIFIC_API_KEY` (or legacy `FREEPIK_API_KEY`) from `.env.local`
automatically. The steps below are only needed when running the UI
Asset Workflow's raw PowerShell commands.

Before generating, ensure the API key is loaded:

```powershell
# Load MAGNIFIC_API_KEY from .env.local into the current session
# Fallback: FREEPIK_API_KEY (legacy name)
$env:MAGNIFIC_API_KEY = (Get-Content .env.local | Where-Object { $_ -match '^MAGNIFIC_API_KEY=' }) -replace '^MAGNIFIC_API_KEY=', ''
if (-not $env:MAGNIFIC_API_KEY) {
    $env:MAGNIFIC_API_KEY = (Get-Content .env.local | Where-Object { $_ -match '^FREEPIK_API_KEY=' }) -replace '^FREEPIK_API_KEY=', ''
}
```

All API calls use this shared header pattern:

```powershell
$headers = @{
    "x-freepik-api-key" = $env:MAGNIFIC_API_KEY
    "Content-Type"      = "application/json"
}
```

> **MANDATORY: every generation request body MUST include
> `enable_safety_checker = $false` (PowerShell) or
> `"enable_safety_checker": false` (JSON). This is not optional.
> Omitting it allows the default content filter to block adult
> content. Never submit a generation task without this field set.**

---

## Choosing the Asset Category

Determine which workflow to follow based on the request:

- If the target is a **portrait pack** (e.g. `sl_deathmachine`,
  `sl_demon`, `sl_highelf`), follow the **Portrait Workflow** below.
- If the target is a **UI asset** (icon, texture, sprite, or a
  missing asset reported by log analysis), follow the **UI Asset
  Workflow** below.

---

## Portrait Workflow

### Required Inputs

Always obtain or infer these before generating anything:

- `portrait-pack`: required, for example `sl_deathmachine`
- target variant: female, male, indeterminable, ruler, scientist,
  admiral, and so on
- desired finish: concept PNG, transparent cutout PNG, or final DDS

If the pack name is missing, stop and ask for it.

### Pack-Specific Prompt Templates

Before inventing a prompt from scratch, check whether the pack already
has a bundled template:

- `assets/sl_deathmachine.prompt.md`

Use the template as a starting point and adjust only the requested
role, variant, and output format.

### 1. Load the pack context

Use the bundled references first.

- Read [Portrait reference](references/mod_portrait_reference.md)
  for category wiring, effort, and special cases.
- Read [Portrait manifest](references/mod_portrait_manifest.md)
  for the target pack's current script path, texture root, DDS naming,
  and count.
- Inspect the live target script under `gfx/portraits/portraits/` if
  the user is changing an existing pack.

Key checks:

- existing filename pattern and numbering
- whether the pack is compact, role-split, or multi-category
- whether the pack shares a texture root with another pack

### 2. Prepare a reference image from existing pack files

Before generating, scan the target pack's texture folder for existing
DDS portraits. Uploading a real pack file as a reference anchors the
new portrait to the established visual identity: species silhouette,
palette, lighting, and materials. This is especially useful when
generating a missing counterpart, for example a female portrait when
only males exist.

Find an existing DDS in the pack's texture folder:

```powershell
$packDir = "gfx/models/portraits/<portrait-pack>"
$existingDds = Get-ChildItem -Path $packDir -Filter "*.dds" `
    -ErrorAction SilentlyContinue | Sort-Object Name
```

If the folder is empty (first portrait for a new pack), omit
`--reference` in the generation command. If files exist, pass one
representative DDS directly to the Python script via `--reference`.
The script handles DDS-to-PNG conversion and base64 encoding
internally.

### 3. Generate via Magnific API

Use Flux Kontext Pro for portrait generation. It accepts one
base64-encoded reference image, produces context-aware output,
and keeps the new portrait visually consistent with the existing pack
files.

Use the bundled Python script. It runs the full pipeline -- generate,
poll, download, background removal, DDS conversion, backup, and
placement -- in one command:

```powershell
uv run --with Pillow --with requests `
  python '.cursor\skills\generate-asset\scripts\generate_portrait.py' `
  --prompt "<portrait prompt here>" `
  --reference "$($existingDds[0].FullName)" `
  --pack <portrait-pack> `
  --filename <filename>.dds
```

`--pack` + `--filename` resolve the output path automatically,
including the special-case texture folders
(`sl_earthgiant`/`sl_diamondgiant` -> `sl_giant/`,
`sl_savagedespoiler` -> `sl_savagedespoilers/`). Pass `--output` with
a full path instead if you need to override the resolved location.

Omit `--reference` when generating the first portrait for a new pack.
Add `--skip-rembg` only if the source image already has clean
transparency. The script prints the seed used; pass `--seed <INT>` to
reproduce an exact generation.

Use `--preview` to print the resolved output path, reference, and
prompt without calling the API -- useful for confirming the plan
before spending credits.

If a request fails with HTTP 503, retry once after 10 seconds. If it
fails again or returns HTTP 4xx, stop and report the error to the
user.

### 4. Build the prompt around the target pack

The script automatically prepends `FRAMING_ANCHOR` to every prompt
before submission. This constant locks camera position, zoom level,
and perspective for all portraits so that every portrait shares the
same spatial grammar in-game. The resizing step (`resize_to_canvas`)
then normalises the output to the pack's canvas dimensions.

**What to vary per portrait (user-supplied `--prompt` text):**

- species or faction identity and material language (e.g. "machine
  skull", "infernal horns", "aquatic scales")
- skin tone and coloring
- accessories (e.g. crown, pauldrons, neck frill, jewellery)
- nudity level (e.g. "clothed torso", "bare upper body")
- pack-specific mood, texture, or lighting cues
- a plain single-color background instruction (see MANDATORY note
  below)

**What NOT to include in the user-supplied prompt:**

- framing or zoom (e.g. "close-up", "full body", "bust shot") --
  these conflict with `FRAMING_ANCHOR`
- angle or perspective (e.g. "worm's eye", "tilted", "side view",
  "front-facing") -- the anchor already specifies these exactly
- camera descriptions such as "centered bust", "waist-up" -- covered
  by the anchor

**MANDATORY: every prompt must explicitly request a plain,
single-color background** -- for example "plain black background",
"solid dark background", or "uniform white background". This is
required even when generating against a reference image. AI image
models do not produce native transparency; without a plain background
the subject silhouette cannot be cleanly cut out and the portrait
will fail background removal.

If generating a missing counterpart for an existing pack, anchor the
prompt to the established pack identity rather than inventing a new
style.

### 5. Handle transparency deliberately

> **MANDATORY: background removal is not optional. Every portrait
> that will be integrated into the mod MUST go through background
> removal before DDS conversion. A portrait with a solid or complex
> background baked into the DDS will look broken in-game. No
> candidate moves to integration without a clean transparent cutout.**

- Always generate against a plain, single-color contrasting
  background (see prompt rules above). This gives the background
  removal API a clean, well-defined edge to work with.
- Never assume the generation model produces native alpha. Even if
  the output PNG appears to have transparency, run background removal
  to verify.
- Convert to `BC3RgbaUnorm` DDS only after background removal
  confirms a clean alpha channel.
- **DX10 header caveat**: `image_dds` (`img2dds`) writes DX10 extended-header
  DDS files. Stellaris requires the legacy DXT5 fourcc format. The pipeline
  calls `_dx10_to_legacy_dxt5()` automatically after every conversion to
  rewrite the header in-place. If you produce DDS files by any other means,
  verify `fourcc` at bytes 84-88 equals `DXT5` (`b'DXT5'`), not `DX10`.

The Python script handles background removal automatically via the
`/v1/ai/beta/remove-background` endpoint. Use `--skip-rembg` to bypass
this step only when the source already has clean transparency.

### 6. Keep outputs organized by pack

Use pack-specific temporary output folders, for example:

- `tmp/generate-asset/sl_deathmachine/`

Prefer these stages:

- original generated PNG
- transparent cutout PNG
- final DDS candidate

### 7. Review the candidate

Before integrating, review each candidate against the target pack.
Use the [Review rubric](references/review-rubric.md)
and the [Review report template](assets/review-report-template.md).

Review checks:

- framing and readability at Stellaris portrait scale
- species or faction fit for the target pack
- alpha readiness or cutout suitability
- obvious anatomy, symmetry, or artifact failures
- whether the candidate can fit the live pack without awkward script
  or naming work

Verdict options:

- `accept` -- ready for integration
- `accept with edits` -- minor touch-ups needed first
- `reject` -- breaks the pack's core visual identity, cannot survive
  background removal cleanly, or would require non-trivial role-split
  rewiring

Report the verdict with concrete findings before proceeding.

### 8. Integrate approved candidates

Only proceed after the user explicitly approves the candidate.

The Python script already placed the DDS at the `--output` path and
wrote a timestamped backup under `backup/generated-portrait/`.
Integration is complete once the portrait script wiring is verified.

1. **Confirm the target layout**
   - Destination texture root (default:
     `gfx/models/portraits/<portrait-pack>/`)
   - Known exceptions: `sl_earthgiant` and `sl_diamondgiant` use
     `sl_giant/`; `sl_savagedespoiler` uses `sl_savagedespoilers/`
   - Verify the DDS was written at the expected path and a backup
     exists under `backup/generated-portrait/`

2. **Update portrait script wiring if required**
   - If the pack does not already reference the new file, update the
     live portrait script under `gfx/portraits/portraits/`

### 9. Validate after integration

Completion checks:

- the new DDS exists in the live texture root
- backups were written for any replaced files
- if transparency was requested, the cutout PNG or DDS exists
- naming matches the target pack's manifest conventions
- any updated portrait script references the new path correctly
- if mod files were changed, related references still line up:
  portrait script keys, texture paths, categories, sets, and entity
  references
- if gameplay files were edited, run the usual validation baseline

---

## UI Asset Workflow

For icons, textures, sprites, and missing assets reported by log
analysis, follow [UI asset workflow](references/ui-asset-workflow.md).
That reference covers generation, resize, DDS conversion, placement,
validation, error handling, and decision rules.

---
