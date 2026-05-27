---
name: generate-asset
description: 'Generate, review, and integrate image assets for Stellaris mods using the Magnific HTTP API. Covers both portrait artwork (for named portrait packs) and general UI assets (icons, textures, sprites). USE WHEN: user says "generate portrait", "create portrait", "make portrait", "add female portrait", "prototype portrait", "generate art", "review portrait", "check portrait candidate", "integrate portrait", "install generated portrait", "fix missing asset", "generate texture", "create icon", "missing dds", "missing texture", "generate dds", "create sprite", or when stellaris-log-fix reports missing textures/sprites that need new artwork.'
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

- [Stellaris DDS formats](c:/Users/razva/Documents/Paradox%20Interactive/Stellaris/mod/StellarisPlusv2/.github/skills/generate-asset/references/stellaris-dds-formats.md)
- [Portrait reference](c:/Users/razva/Documents/Paradox%20Interactive/Stellaris/mod/StellarisPlusv2/.github/skills/generate-asset/references/mod_portrait_reference.md)
- [Portrait manifest](c:/Users/razva/Documents/Paradox%20Interactive/Stellaris/mod/StellarisPlusv2/.github/skills/generate-asset/references/mod_portrait_manifest.md)
- [Magnific API reference](c:/Users/razva/Documents/Paradox%20Interactive/Stellaris/mod/StellarisPlusv2/.github/skills/generate-asset/references/magnific-api.md)
- [Portrait Quality Report](c:/Users/razva/Documents/Paradox%20Interactive/Stellaris/mod/StellarisPlusv2/.github/skills/generate-asset/references/portrait_quality_report.md)
- [Review rubric](c:/Users/razva/Documents/Paradox%20Interactive/Stellaris/mod/StellarisPlusv2/.github/skills/generate-asset/references/review-rubric.md)
- [Review report template](c:/Users/razva/Documents/Paradox%20Interactive/Stellaris/mod/StellarisPlusv2/.github/skills/generate-asset/assets/review-report-template.md)
- [Example prompt](c:/Users/razva/Documents/Paradox%20Interactive/Stellaris/mod/StellarisPlusv2/.github/skills/generate-asset/assets/sl_deathmachine.prompt.md)
- [Portrait generation script](c:/Users/razva/Documents/Paradox%20Interactive/Stellaris/mod/StellarisPlusv2/.github/skills/generate-asset/scripts/generate_portrait.py)

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

- Read [Portrait reference](c:/Users/razva/Documents/Paradox%20Interactive/Stellaris/mod/StellarisPlusv2/.github/skills/generate-asset/references/mod_portrait_reference.md)
  for category wiring, effort, and special cases.
- Read [Portrait manifest](c:/Users/razva/Documents/Paradox%20Interactive/Stellaris/mod/StellarisPlusv2/.github/skills/generate-asset/references/mod_portrait_manifest.md) <!-- markdownlint-disable-line MD013 -->
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
  python '.github\skills\generate-asset\scripts\generate_portrait.py' `
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
Use the [Review rubric](c:/Users/razva/Documents/Paradox%20Interactive/Stellaris/mod/StellarisPlusv2/.github/skills/generate-asset/references/review-rubric.md) <!-- markdownlint-disable-line MD013 -->
and the [Review report template](c:/Users/razva/Documents/Paradox%20Interactive/Stellaris/mod/StellarisPlusv2/.github/skills/generate-asset/assets/review-report-template.md). <!-- markdownlint-disable-line MD013 -->

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

Use this workflow for icons, textures, sprites, and missing assets
reported by log analysis.

### Required UI Inputs

- **target path**: the final DDS path expected by the `.gfx` sprite
  definition
- **dimensions**: see the size table below
- **DDS format**: usually `BC3RgbaUnorm` (see
  [Stellaris DDS formats](c:/Users/razva/Documents/Paradox%20Interactive/Stellaris/mod/StellarisPlusv2/.github/skills/generate-asset/references/stellaris-dds-formats.md))
- **visual style**: what the icon or texture should depict

### Common Asset Dimensions

| Asset type | Size | Format |
| ---------- | ---- | ------ |
| Tradition tree icon | 60x60 | BC3RgbaUnorm |
| Tradition individual | 45x45 | BC3RgbaUnorm |
| Building/District icon | 64x64 | BC3RgbaUnorm |
| Modifier/Trait icon | 29x29 | BC3RgbaUnorm |
| Edict/Technology icon | 46x46 | BC3RgbaUnorm |
| Flag emblem | 128x128 | BC3RgbaUnorm |
| Ship texture (diffuse) | 512-2048 | BC1RgbaUnorm |
| Ship texture (normal) | 512-2048 | BC5RgUnorm |

Default format: **BC3RgbaUnorm** (DXT5, handles transparency).

### Naming Conventions

- Output DDS files must match the path declared in the `.gfx` sprite
  definition (`textureFile` / `texturefile`).
- Prefer lowercase filenames with underscores for new assets.
- GFX sprite names use the `GFX_` prefix.

### 1. Generate image via Magnific API

For UI assets, use a cost-efficient model. Flux 2 Turbo (0.008 EUR)
or Classic Fast (0.004 EUR) are recommended for small icons that will
be heavily resized.

```powershell
$body = @{
    prompt                = "<icon description>, centered on dark background"
    image_size            = @{ width = 1024; height = 1024 }
    enable_safety_checker = $false
    output_format         = "png"
} | ConvertTo-Json

$response = Invoke-RestMethod `
    -Uri "https://api.freepik.com/v1/ai/text-to-image/flux-2-turbo" `
    -Method Post -Headers $headers -Body $body

$taskId = $response.data.task_id
```

Then poll for completion (repeat until status is `COMPLETED` or
`FAILED`, sleeping 3 seconds between attempts):

```powershell
do {
    Start-Sleep -Seconds 3
    $status = Invoke-RestMethod `
        -Uri "https://api.freepik.com/v1/ai/text-to-image/flux-2-turbo/$taskId" `
        -Method Get -Headers $headers
} while ($status.data.status -notin @("COMPLETED", "FAILED"))

if ($status.data.status -eq "FAILED") {
    Write-Error "Generation failed for task $taskId"
} else {
    $imageUrl = $status.data.generated[0]
    $rawPath = "tmp/<name>_raw"
    Invoke-WebRequest -Uri $imageUrl -OutFile $rawPath
    # Re-encode through Pillow to guarantee a true PNG on disk.
    # The API may return JPEG bytes even when output_format="png" is
    # declared; saving the raw download as .png causes a media-type
    # mismatch when the file is later displayed to the model.
    uv run --with Pillow python -c "
import sys
from PIL import Image
Image.open(sys.argv[1]).save(sys.argv[2], format='PNG')
" "$rawPath" "tmp/<name>.png"
    Remove-Item $rawPath -ErrorAction SilentlyContinue
    Write-Host "Downloaded to tmp/<name>.png"
}
```

**MANDATORY: always include `enable_safety_checker = $false` in the
request body.** Flux Kontext Pro uses this parameter name. Omitting it
causes the default content filter to block adult portrait content.

Prompting tips:

- Always include "centered on dark background" (generation models do
  not reliably produce native transparency).
- Tradition icons: "circular frame, soft glow, symbolic imagery".
- Building/district: "isometric view, clean lines, sci-fi
  architecture".
- Modifier: "small symbolic icon, high contrast, simple shape".

If a request fails with HTTP 503, retry once after 10 seconds. If it
fails again or returns HTTP 4xx, stop and report the error to the
user.

### 2. Resize

```powershell
uv run --with Pillow python -c "
from PIL import Image
img = Image.open('tmp/<name>.png').resize((<W>, <H>), Image.LANCZOS)
img.save('tmp/<name>_resized.png')
"
```

### 3. Convert to DDS

First-time setup:

```powershell
if (-not (Test-Path "$env:USERPROFILE\.stellarisplus\image_dds")) {
    New-Item -ItemType Directory -Path "$env:USERPROFILE\.stellarisplus" -Force
    git clone https://github.com/ScanMountGoat/image_dds.git `
      "$env:USERPROFILE\.stellarisplus\image_dds"
    cargo build --release `
      --manifest-path "$env:USERPROFILE\.stellarisplus\image_dds\image_dds\Cargo.toml" `
      --examples
}
```

Convert:

```powershell
cargo run --release `
  --manifest-path "$env:USERPROFILE\.stellarisplus\image_dds\image_dds\Cargo.toml" `
  --example img2dds `
  "tmp/<name>_resized.png" "tmp/<name>.dds" <DDS_FORMAT>
```

### 4. Verify and place

```powershell
$dest = "<target_path>"
$destDir = Split-Path $dest -Parent
if (-not (Test-Path $destDir)) {
    New-Item -ItemType Directory -Path $destDir -Force | Out-Null
}
Move-Item "tmp/<name>.dds" $dest -Force
Remove-Item "tmp/<name>*.png" -ErrorAction SilentlyContinue
```

### 5. Register (if needed)

If fixing a "Missing GFX/Sprite" error, the GFX definition already
exists. For new assets, add a `spriteType` entry in the appropriate
`.gfx` file.

### 6. Validate

- After placing the DDS, verify the sprite loads via the quality gate.
- For new assets, confirm the `.gfx` `spriteType` entry exists and
  references the correct path.

---

## Error Handling

- If `cargo build` fails with "linker link.exe not found": install
  Visual C++ Build Tools
  (`winget install Microsoft.VisualStudio.2022.BuildTools`) and load
  MSVC env via `vcvars64.bat`.
- If conversion produces a 0-byte file: the input PNG may be corrupt;
  re-generate or verify with an image viewer.
- If the API returns HTTP 401: the API key is missing or invalid;
  verify `.env.local` contains a valid `MAGNIFIC_API_KEY`
  (or `FREEPIK_API_KEY` for backward compatibility).
- If the API returns HTTP 429: rate limit exceeded; wait and retry
  after the indicated cooldown period.

## Decision Rules

- Always use the Magnific HTTP API for generation.
- **`enable_safety_checker: false` is MANDATORY in every generation
  request body, without exception.** The Flux Kontext Pro endpoint
  uses this exact parameter name. Stellar
  Hordes is an adult portrait pack. A request missing this field must
  be treated as a bug and corrected before submission. Never rely on
  API defaults for content filtering.
- **Background removal is MANDATORY before any production DDS is
  produced.** Always prompt for a plain single-color background.
  Always run the remove-background API step. A portrait with a
  non-transparent background must never reach the final DDS stage.
  This rule applies to every portrait and every UI asset that
  requires transparency.
- If the target pack is role-split, multi-category, or shared-root,
  inspect the live files before promising a low-effort integration.
- Reject portrait candidates that break the pack's core visual
  identity.
- Reject candidates that cannot survive simple background removal or
  would create a poor silhouette after cutout.
- Do not overwrite live assets without a backup.
- Do not guess the destination filename when the live pack already has
  a numbering scheme; inspect the pack first.
- Prefer `BC3RgbaUnorm` (DXT5) as the default DDS format.
- Prefer cost-efficient models (Flux 2 Turbo, Classic Fast) for UI
  assets; use Flux Kontext Pro for portraits.
