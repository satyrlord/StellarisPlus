# UI Asset Workflow

Use this workflow for icons, textures, sprites, and missing assets
reported by log analysis.

## Required UI Inputs

- **target path**: the final DDS path expected by the `.gfx` sprite
  definition
- **dimensions**: see the size table below
- **DDS format**: usually `BC3RgbaUnorm` (see
  [Stellaris DDS formats](stellaris-dds-formats.md))
- **visual style**: what the icon or texture should depict

## Common Asset Dimensions

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

## Naming Conventions

- Output DDS files must match the path declared in the `.gfx` sprite
  definition (`textureFile` / `texturefile`).
- Prefer lowercase filenames with underscores for new assets.
- GFX sprite names use the `GFX_` prefix.

## 1. Generate image via Magnific API

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

## 2. Resize

```powershell
uv run --with Pillow python -c "
from PIL import Image
img = Image.open('tmp/<name>.png').resize((<W>, <H>), Image.LANCZOS)
img.save('tmp/<name>_resized.png')
"
```

## 3. Convert to DDS

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

## 4. Verify and place

```powershell
$dest = "<target_path>"
$destDir = Split-Path $dest -Parent
if (-not (Test-Path $destDir)) {
    New-Item -ItemType Directory -Path $destDir -Force | Out-Null
}
Move-Item "tmp/<name>.dds" $dest -Force
Remove-Item "tmp/<name>*.png" -ErrorAction SilentlyContinue
```

## 5. Register (if needed)

If fixing a "Missing GFX/Sprite" error, the GFX definition already
exists. For new assets, add a `spriteType` entry in the appropriate
`.gfx` file.

## 6. Validate

- After placing the DDS, verify the sprite loads via the quality gate.
- For new assets, confirm the `.gfx` `spriteType` entry exists and
  references the correct path.

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
  uses this exact parameter name. Stellar Hordes is an adult portrait
  pack. A request missing this field must be treated as a bug and
  corrected before submission. Never rely on API defaults for content
  filtering.
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
