#!/usr/bin/env python3
"""
generate_portrait.py -- Full portrait generation pipeline for StellarisPlus.

Pipeline:
  1. Encode the reference image as base64
  2. Submit a generation task to Flux Kontext Pro
  3. Poll until complete
  4. Download the raw result and re-encode as PNG via Pillow
    5. Remove the background via the Magnific remove-background API
  6. Convert the transparent PNG to a BC3RgbaUnorm DDS via image_dds (cargo)
  7. Place the DDS at the target output path (with optional backup)

Usage:
  uv run --with Pillow --with requests python generate_portrait.py \
    --prompt "..." \
    --reference gfx/models/portraits/sl_deathmachine/deathmachine_01.dds \
    --output gfx/models/portraits/sl_deathmachine/female_deathmachine_01.dds

Required env:
    MAGNIFIC_API_KEY -- loaded automatically from .env.local if not already set
                      (falls back to FREEPIK_API_KEY)

Optional env:
  IMAGE_DDS_ROOT   -- path to the image_dds checkout
                      (default: %USERPROFILE%\\.stellarisplus\\image_dds)
"""

import argparse
import base64
import os
import random
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# Dependency: requests (via uv run --with requests) and Pillow
# ---------------------------------------------------------------------------
try:
    import requests
except ImportError:
    sys.exit("requests is required. Run via: uv run --with Pillow --with requests python generate_portrait.py ...")

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is required. Run via: uv run --with Pillow --with requests python generate_portrait.py ...")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
# Magnific rebrand uses the same API host.
BASE_URL = "https://api.freepik.com"
GENERATE_ENDPOINT = "/v1/ai/text-to-image/flux-kontext-pro"
REMBG_ENDPOINT = "/v1/ai/beta/remove-background"
POLL_INTERVAL_SECONDS = 5
MAX_POLL_ATTEMPTS = 60       # 5 min ceiling
RETRY_ON_503_ONCE = True
DDS_FORMAT = "BC3RgbaUnorm"
DEFAULT_IMAGE_DDS_ROOT = Path.home() / ".stellarisplus" / "image_dds"

# Content height as a fraction of canvas height, matching vanilla portrait proportions.
# Originals (uncompressed RGBA): 507-557 px content out of 1650 px canvas (30.7-33.8%).
# Generated portraits (DXT5, BC3): 520 px content out of 1650 px canvas (31.5%).
# Both values produce content bounding box rows ~1130-1650 on 825x1650 canvases.
# Validated in-game against all 20 sl_deathmachine portraits (10 male + 10 female).
CONTENT_HEIGHT_RATIO = 0.315

# Locked framing anchor prepended to every generation prompt.
# Enforces consistent camera position, zoom level, and perspective so that
# resize_to_canvas always receives consistently framed content and all portraits
# share the same spatial grammar in-game.
#
# Per-portrait variance -- skin tone, coloring, accessories, nudity -- belongs
# in the caller-supplied --prompt text, NOT here.
FRAMING_ANCHOR = (
    "centered bust portrait, straight-on front view, eye-level camera, "
    "head and upper chest filling the lower two-thirds of the frame, "
    "shoulders to crown clearly visible, "
    "no Dutch angle, no extreme perspective, no tilt, "
)

# Packs whose texture folder does not match their pack name
TEXTURE_ROOT_EXCEPTIONS: dict[str, str] = {
    "sl_earthgiant":     "gfx/models/portraits/sl_giant",
    "sl_diamondgiant":   "gfx/models/portraits/sl_giant",
    "sl_savagedespoiler": "gfx/models/portraits/sl_savagedespoilers",
}


# ---------------------------------------------------------------------------
# Portrait pack helpers
# ---------------------------------------------------------------------------

def resolve_texture_root(pack: str) -> str:
    """Return the texture folder path for a portrait pack name."""
    return TEXTURE_ROOT_EXCEPTIONS.get(pack, f"gfx/models/portraits/{pack}")


# ---------------------------------------------------------------------------
# API key loading
# ---------------------------------------------------------------------------

def load_api_key() -> str:
    """Return the Magnific API key from env or .env.local."""
    key = os.environ.get("MAGNIFIC_API_KEY", "").strip()
    if key:
        os.environ.setdefault("FREEPIK_API_KEY", key)
        return key

    key = os.environ.get("FREEPIK_API_KEY", "").strip()
    if key:
        os.environ.setdefault("MAGNIFIC_API_KEY", key)
        return key

    env_file = Path(".env.local")
    if env_file.is_file():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("MAGNIFIC_API_KEY="):
                key = line[len("MAGNIFIC_API_KEY="):].strip()
                if key:
                    os.environ["MAGNIFIC_API_KEY"] = key
                    os.environ.setdefault("FREEPIK_API_KEY", key)
                    return key
            if line.startswith("FREEPIK_API_KEY="):
                key = line[len("FREEPIK_API_KEY="):].strip()
                if key:
                    os.environ["FREEPIK_API_KEY"] = key
                    os.environ.setdefault("MAGNIFIC_API_KEY", key)
                    return key

    sys.exit(
        "No API key found. Set MAGNIFIC_API_KEY (preferred) or FREEPIK_API_KEY in env or .env.local.\n"
        "Example: MAGNIFIC_API_KEY=<your key>"
    )


# ---------------------------------------------------------------------------
# Reference image encoding
# ---------------------------------------------------------------------------

def encode_reference(ref_path: Path, tmp_dir: Path) -> str:
    """
    Return a base64 string for the reference image.

    If the reference is a DDS file, first convert it to PNG via image_dds,
    then re-encode through Pillow to guarantee a clean PNG byte stream.
    If the reference is already a PNG/JPG, encode it directly.
    """
    suffix = ref_path.suffix.lower()

    if suffix == ".dds":
        print(f"  Converting reference DDS to PNG: {ref_path}")
        png_path = tmp_dir / "reference.png"
        _dds_to_png(ref_path, png_path)
        src = png_path
    else:
        src = ref_path

    # Re-encode through Pillow to normalise the byte stream
    normalised = tmp_dir / "reference_normalised.png"
    with Image.open(src) as img:
        img.save(normalised, format="PNG")

    return base64.b64encode(normalised.read_bytes()).decode("ascii")


# ---------------------------------------------------------------------------
# Generation
# ---------------------------------------------------------------------------

def submit_generation(prompt: str, ref_b64: str, headers: dict, seed: int, image_size: dict) -> str:
    """Submit a generation task and return the task_id."""
    body = {
        "prompt": prompt,
        "image_size": image_size,
        "enable_safety_checker": False,
        "output_format": "png",
        "seed": seed,
    }
    if ref_b64:
        body["input_image"] = ref_b64

    url = BASE_URL + GENERATE_ENDPOINT
    print(f"  Submitting generation task (seed={seed}) ...")
    resp = _post_with_retry(url, body, headers)
    task_id = resp["data"]["task_id"]
    print(f"  Task submitted: {task_id}")
    return task_id


def poll_generation(task_id: str, headers: dict) -> str:
    """Poll until complete. Returns the image URL."""
    url = f"{BASE_URL}{GENERATE_ENDPOINT}/{task_id}"
    for attempt in range(1, MAX_POLL_ATTEMPTS + 1):
        time.sleep(POLL_INTERVAL_SECONDS)
        resp = requests.get(url, headers=headers, timeout=30)
        _raise_for_status(resp)
        data = resp.json()["data"]
        status = data["status"]
        print(f"  [{attempt:02d}] Status: {status}")
        if status == "COMPLETED":
            images = data.get("generated") or []
            if not images:
                sys.exit("Generation COMPLETED but no images were returned.")
            return images[0]
        if status == "FAILED":
            sys.exit(f"Generation FAILED for task {task_id}.")
    sys.exit(f"Timed out waiting for task {task_id} after {MAX_POLL_ATTEMPTS} polls.")


def download_and_clean(image_url: str, tmp_dir: Path) -> Path:
    """Download the raw generated file and re-encode as a clean PNG."""
    raw = tmp_dir / "candidate_raw"
    print(f"  Downloading result ...")
    resp = requests.get(image_url, timeout=60)
    resp.raise_for_status()
    raw.write_bytes(resp.content)

    png_path = tmp_dir / "candidate.png"
    with Image.open(raw) as img:
        img.save(png_path, format="PNG")
    raw.unlink(missing_ok=True)
    print(f"  Saved clean PNG: {png_path}")
    return png_path


# ---------------------------------------------------------------------------
# Background removal
# ---------------------------------------------------------------------------

def remove_background(image_url: str, tmp_dir: Path, headers: dict) -> Path:
    """
    Call the Magnific /v1/ai/beta/remove-background API.

    Accepts the publicly accessible CDN URL returned by poll_generation().
    The API is synchronous and returns temporary URLs that expire in 5 minutes,
    so the result is downloaded immediately.
    Returns the cutout PNG path.
    """
    import io
    cutout_path = tmp_dir / "candidate_cutout.png"
    body = {"image_url": image_url}

    # The beta remove-background endpoint expects form data, not JSON.
    # The API still expects the legacy x-freepik-api-key header.
    # Let requests set Content-Type automatically.
    rembg_headers = {k: v for k, v in headers.items() if k != "Content-Type"}
    url = BASE_URL + REMBG_ENDPOINT
    print("  Removing background ...")
    resp = requests.post(url, data=body, headers=rembg_headers, timeout=120)
    _raise_for_status(resp)
    payload = resp.json()

    # Response fields: original, high_resolution, preview, url
    # All URLs expire in 5 minutes -- download immediately.
    result_url = payload.get("url") or payload.get("high_resolution")
    if not result_url:
        sys.exit(f"remove-background response has no download URL.\nFull response: {payload}")

    r = requests.get(result_url, timeout=60)
    r.raise_for_status()
    with Image.open(io.BytesIO(r.content)) as img:
        img.save(cutout_path, format="PNG")

    print(f"  Cutout PNG saved: {cutout_path}")
    return cutout_path


# ---------------------------------------------------------------------------
# DDS conversion
# ---------------------------------------------------------------------------

def _dx10_to_legacy_dxt5(dds_path: Path) -> None:
    """
    Rewrite a DX10/BC3_UNORM DDS file to the legacy DXT5 fourcc format.

    Stellaris expects legacy DDS headers (fourcc ``DXT5``).  The image_dds
    ``img2dds`` tool always writes a DX10 extended header (extra 20 bytes),
    which causes the engine to misinterpret the pixel data and display
    corrupted / mangled portraits.  This function strips the DX10 extension
    and writes a standards-compliant legacy header instead.
    """
    data = dds_path.read_bytes()
    if data[:4] != b"DDS " or data[84:88] != b"DX10":
        return  # already legacy or unknown format -- leave untouched
    dxgi_fmt = struct.unpack_from("<I", data, 128)[0]
    if dxgi_fmt != 77:  # 77 = DXGI_FORMAT_BC3_UNORM
        return

    h   = struct.unpack_from("<I", data, 12)[0]
    w   = struct.unpack_from("<I", data, 16)[0]
    mip = struct.unpack_from("<I", data, 28)[0]
    pixel_data = data[148:]  # 128-byte base header + 20-byte DX10 extension

    linear_size = max(1, (w + 3) // 4) * max(1, (h + 3) // 4) * 16

    DDSD_CAPS        = 0x1
    DDSD_HEIGHT      = 0x2
    DDSD_WIDTH       = 0x4
    DDSD_LINEARSIZE  = 0x80000
    DDSD_MIPMAPCOUNT = 0x20000
    DDSD_PIXELFORMAT = 0x1000
    dwFlags = DDSD_CAPS | DDSD_HEIGHT | DDSD_WIDTH | DDSD_LINEARSIZE | DDSD_MIPMAPCOUNT | DDSD_PIXELFORMAT

    DDSCAPS_COMPLEX = 0x8
    DDSCAPS_MIPMAP  = 0x400000
    DDSCAPS_TEXTURE = 0x1000
    dwCaps = DDSCAPS_TEXTURE | DDSCAPS_COMPLEX | DDSCAPS_MIPMAP

    hdr = bytearray(128)
    struct.pack_into("<4sI", hdr, 0, b"DDS ", 124)
    struct.pack_into("<IIIII", hdr, 8,  dwFlags, h, w, linear_size, 0)
    struct.pack_into("<I",     hdr, 28, mip)
    # Pixel format at offset 76 (32 bytes)
    struct.pack_into("<II4sIIIII", hdr, 76, 32, 0x4, b"DXT5", 0, 0, 0, 0, 0)
    struct.pack_into("<III",   hdr, 108, dwCaps, 0, 0)

    dds_path.write_bytes(bytes(hdr) + pixel_data)


def convert_to_dds(png_path: Path, output_path: Path) -> None:
    """Convert a PNG to BC3RgbaUnorm DDS using image_dds (cargo)."""
    image_dds_root = Path(os.environ.get("IMAGE_DDS_ROOT", str(DEFAULT_IMAGE_DDS_ROOT)))
    manifest = image_dds_root / "image_dds" / "Cargo.toml"

    if not manifest.is_file():
        print(f"  Cloning image_dds into {image_dds_root} ...")
        _run(["git", "clone", "https://github.com/ScanMountGoat/image_dds.git", str(image_dds_root)])

    print("  Building image_dds examples (first run may take a minute) ...")
    _run(["cargo", "build", "--release", "--manifest-path", str(manifest), "--examples"])

    output_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"  Converting PNG -> DDS ({DDS_FORMAT}) ...")
    _run([
        "cargo", "run", "--release",
        "--manifest-path", str(manifest),
        "--example", "img2dds",
        str(png_path), str(output_path), DDS_FORMAT,
    ])

    if not output_path.is_file() or output_path.stat().st_size == 0:
        sys.exit(f"DDS conversion produced an empty or missing file: {output_path}")

    # image_dds always writes DX10 extended-header DDS; Stellaris requires
    # the legacy DXT5 fourcc format.  Rewrite the header in-place.
    _dx10_to_legacy_dxt5(output_path)

    print(f"  DDS written: {output_path}  ({output_path.stat().st_size:,} bytes)")


# ---------------------------------------------------------------------------
# Backup
# ---------------------------------------------------------------------------

def backup_existing(target: Path, backup_root: Path) -> None:
    """Back up an existing file before overwriting it."""
    if not target.is_file():
        return
    rel = target.relative_to(Path.cwd()) if target.is_relative_to(Path.cwd()) else target
    dest = backup_root / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(target, dest)
    print(f"  Backed up existing file to: {dest}")


# ---------------------------------------------------------------------------
# Dimensions
# ---------------------------------------------------------------------------

def compute_generation_size(target_w: int, target_h: int) -> dict[str, int]:
    """
    Derive a Magnific-compatible generation size that matches the target aspect ratio.

    The short side is anchored at 768 px; the long side is scaled and rounded
    to the nearest multiple of 8, capped at 2048.
    """
    BASE = 768
    if target_h > target_w:
        gen_w = BASE
        gen_h = min(round(BASE * target_h / target_w / 8) * 8, 2048)
    elif target_w > target_h:
        gen_h = BASE
        gen_w = min(round(BASE * target_w / target_h / 8) * 8, 2048)
    else:
        gen_w, gen_h = BASE, BASE
    return {"width": gen_w, "height": gen_h}


def detect_pack_dimensions(texture_root: Path) -> tuple[int, int] | None:
    """
    Infer portrait canvas dimensions from existing DDS files in the texture root.

    Reads DDS headers and returns the most common (width, height) pair found,
    or None if no valid DDS files are present.
    """
    import struct
    counts: dict[tuple[int, int], int] = {}
    for f in texture_root.glob("*.dds"):
        try:
            with open(f, "rb") as fh:
                header = fh.read(128)
            if len(header) < 24 or header[:4] != b"DDS ":
                continue
            h = struct.unpack_from("<I", header, 12)[0]
            w = struct.unpack_from("<I", header, 16)[0]
            if w > 0 and h > 0:
                counts[(w, h)] = counts.get((w, h), 0) + 1
        except Exception:
            continue
    return max(counts, key=lambda k: counts[k]) if counts else None


def resize_to_canvas(png_path: Path, target_w: int, target_h: int, tmp_dir: Path) -> Path:
    """
    Fit the portrait onto a transparent canvas of target_w x target_h.

    Content is scaled so its height does not exceed CONTENT_HEIGHT_RATIO of the
    canvas height (default 31.5%), matching the proportions used by existing
    vanilla-style pack portraits (measured at 30.7-33.8% for sl_deathmachine).
    The content is also capped to canvas width.  It is placed at the BOTTOM of
    the canvas (horizontally centered) so that empty/transparent space sits at
    the top.

    Stellaris portrait rendering is bottom-anchored: the bottom edge of the DDS
    is the fixed anchor point in the viewport.  Placing content flush with the
    bottom edge and leaving transparent space at the top ensures the character
    appears exactly where the engine expects it.

    Returns png_path unchanged if the image already has the correct dimensions.
    """
    out_path = tmp_dir / f"candidate_canvas_{target_w}x{target_h}.png"
    with Image.open(png_path).convert("RGBA") as img:
        iw, ih = img.size
        if iw == target_w and ih == target_h:
            return png_path
        max_content_h = round(target_h * CONTENT_HEIGHT_RATIO)
        scale = min(target_w / iw, max_content_h / ih)
        new_w = round(iw * scale)
        new_h = round(ih * scale)
        resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
        x = (target_w - new_w) // 2   # horizontally centered
        y = target_h - new_h           # bottom-anchored (empty space at top)
        canvas.paste(resized, (x, y))
        canvas.save(out_path, format="PNG")
    print(f"  Canvas {target_w}x{target_h}: inner {new_w}x{new_h} at ({x}, {y})  [bottom-anchored]")
    return out_path


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _post_with_retry(url: str, body: dict, headers: dict) -> dict:
    resp = requests.post(url, json=body, headers=headers, timeout=60)
    if resp.status_code == 503 and RETRY_ON_503_ONCE:
        print("  HTTP 503 received -- retrying once after 10 s ...")
        time.sleep(10)
        resp = requests.post(url, json=body, headers=headers, timeout=60)
    _raise_for_status(resp)
    return resp.json()


def _raise_for_status(resp: "requests.Response") -> None:
    if not resp.ok:
        sys.exit(
            f"API error {resp.status_code} from {resp.url}\n"
            f"Body: {resp.text[:400]}"
        )


def _run(cmd: list[str]) -> None:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        sys.exit(
            f"Command failed: {' '.join(cmd)}\n"
            f"stdout: {result.stdout}\nstderr: {result.stderr}"
        )


def _dds_to_png(dds_path: Path, png_path: Path) -> None:
    image_dds_root = Path(os.environ.get("IMAGE_DDS_ROOT", str(DEFAULT_IMAGE_DDS_ROOT)))
    manifest = image_dds_root / "image_dds" / "Cargo.toml"

    if not manifest.is_file():
        print(f"  Cloning image_dds into {image_dds_root} ...")
        _run(["git", "clone", "https://github.com/ScanMountGoat/image_dds.git", str(image_dds_root)])

    _run(["cargo", "build", "--release", "--manifest-path", str(manifest), "--examples"])
    png_path.parent.mkdir(parents=True, exist_ok=True)
    _run([
        "cargo", "run", "--release",
        "--manifest-path", str(manifest),
        "--example", "dds2img",
        str(dds_path), str(png_path),
    ])


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Generate a portrait, remove its background, and produce a mod-ready DDS."
    )
    p.add_argument(
        "--prompt", required=True,
        help="Generation prompt. Include species identity, skin/coloring, accessories, nudity, "
             "and a plain single-color background instruction. "
             "Do NOT include framing, zoom, angle, or perspective -- these are locked by "
             "FRAMING_ANCHOR and prepended by the script automatically.",
    )
    p.add_argument(
        "--reference", required=False, default="",
        metavar="PATH",
        help="Path to an existing DDS or PNG to use as visual reference (base64-encoded). "
             "Omit to generate without a reference.",
    )
    p.add_argument(
        "--output", required=False, default="",
        metavar="PATH",
        help="Destination DDS path, e.g. gfx/models/portraits/sl_deathmachine/female_01.dds. "
             "Required unless both --pack and --filename are given.",
    )
    p.add_argument(
        "--pack",
        metavar="PACK",
        help="Portrait pack name (e.g. sl_deathmachine). Resolves the texture root automatically, "
             "including special-case folders (sl_earthgiant/sl_diamondgiant -> sl_giant, "
             "sl_savagedespoiler -> sl_savagedespoilers). Used with --filename to derive --output.",
    )
    p.add_argument(
        "--filename",
        metavar="FILENAME",
        help="Destination DDS filename (e.g. female_deathmachine_01.dds). Used with --pack to derive --output.",
    )
    p.add_argument(
        "--preview", action="store_true",
        help="Print the resolved plan (output path, reference, prompt, seed) without calling the API.",
    )
    p.add_argument(
        "--tmp-dir", default="tmp/generate-asset",
        metavar="DIR",
        help="Temporary working directory (default: tmp/generate-asset).",
    )
    p.add_argument(
        "--backup-root", default="backup/generated-portrait",
        metavar="DIR",
        help="Root directory for backing up replaced live files (default: backup/generated-portrait).",
    )
    p.add_argument(
        "--seed", type=int, default=-1,
        metavar="INT",
        help="Generation seed (0-2147483647). Omit or pass -1 to use a fresh random seed.",
    )
    p.add_argument(
        "--skip-rembg", action="store_true",
        help="Skip background removal (use only when the source already has clean transparency).",
    )
    p.add_argument(
        "--size",
        metavar="WxH",
        help="Target DDS canvas dimensions, e.g. 825x1650. "
             "Auto-detected from existing files in the pack texture folder if omitted.",
    )
    return p


def main() -> None:
    args = build_parser().parse_args()

    # Resolve output path from --pack + --filename if --output not given
    if not args.output:
        if not args.pack or not args.filename:
            sys.exit(
                "Provide --output OR both --pack and --filename.\n"
                "Example: --pack sl_deathmachine --filename female_deathmachine_01.dds"
            )
        texture_root = resolve_texture_root(args.pack)
        output_path = Path(texture_root) / args.filename
    else:
        output_path = Path(args.output)

    # Resolve target canvas dimensions
    if args.size:
        try:
            target_w, target_h = (int(v) for v in args.size.lower().split("x", 1))
        except ValueError:
            sys.exit(f"--size must be in WxH format, e.g. 825x1650. Got: {args.size}")
    else:
        texture_root_path = Path(resolve_texture_root(args.pack)) if args.pack else output_path.parent
        detected = detect_pack_dimensions(texture_root_path)
        if detected:
            target_w, target_h = detected
            print(f"  Auto-detected pack dimensions: {target_w}x{target_h}")
        else:
            target_w, target_h = 768, 1024
            print(f"  No existing DDS found; using default dimensions: {target_w}x{target_h}")

    image_size = compute_generation_size(target_w, target_h)
    seed = args.seed if args.seed >= 0 else random.randint(0, 2147483647)

    # Prepend the locked framing anchor to the caller-supplied prompt.
    # The anchor fixes camera position, zoom, and perspective; the caller
    # supplies only the variable parts: skin, coloring, accessories, nudity.
    full_prompt = FRAMING_ANCHOR + args.prompt

    if args.preview:
        print("=== Preview (no API calls will be made) ===")
        print(f"  Pack:           {args.pack or '(not specified)'}")
        print(f"  Output:         {output_path}")
        print(f"  Canvas:         {target_w}x{target_h}")
        print(f"  Gen size:       {image_size['width']}x{image_size['height']}")
        print(f"  Reference:      {args.reference or '(none)'}")
        print(f"  Backup root:    {args.backup_root}")
        print(f"  Skip rembg:     {args.skip_rembg}")
        print(f"  Seed:           {seed}")
        print(f"  Framing anchor: {FRAMING_ANCHOR}")
        print(f"  User prompt:    {args.prompt}")
        print(f"  Full prompt:    {full_prompt}")
        return

    api_key = load_api_key()
    headers = {
        # Magnific currently uses legacy auth headers.
        "x-freepik-api-key": api_key,
        "Content-Type": "application/json",
    }
    tmp_dir = Path(args.tmp_dir) / (output_path.stem or "portrait")
    tmp_dir.mkdir(parents=True, exist_ok=True)

    # -- 1. Encode reference image ------------------------------------------
    ref_b64 = ""
    if args.reference:
        ref_path = Path(args.reference)
        if not ref_path.is_file():
            sys.exit(f"Reference file not found: {ref_path}")
        print(f"\n[1/6] Encoding reference image: {ref_path}")
        ref_b64 = encode_reference(ref_path, tmp_dir)
    else:
        print("\n[1/6] No reference image provided -- generating without one.")

    # -- 2. Submit generation task ------------------------------------------
    print(f"\n[2/6] Generating image via Flux Kontext Pro (seed={seed}, size={image_size['width']}x{image_size['height']}) ...")
    task_id = submit_generation(full_prompt, ref_b64, headers, seed, image_size)

    # -- 3. Poll and download -----------------------------------------------
    print("\n[3/6] Polling for completion ...")
    image_url = poll_generation(task_id, headers)
    candidate_png = download_and_clean(image_url, tmp_dir)

    # -- 4. Background removal ----------------------------------------------
    if args.skip_rembg:
        print("\n[4/6] Skipping background removal (--skip-rembg).")
        cutout_png = candidate_png
    else:
        print("\n[4/6] Removing background ...")
        cutout_png = remove_background(image_url, tmp_dir, headers)

    # -- 5. Resize to target canvas -----------------------------------------
    print(f"\n[5/6] Resizing to {target_w}x{target_h} canvas ...")
    final_png = resize_to_canvas(cutout_png, target_w, target_h, tmp_dir)

    # -- 6. DDS conversion and placement ------------------------------------
    print("\n[6/6] Converting to DDS and placing output ...")
    dds_tmp = tmp_dir / (output_path.stem + ".dds")
    convert_to_dds(final_png, dds_tmp)

    backup_existing(output_path, Path(args.backup_root))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(dds_tmp, output_path)
    print(f"\n  Final DDS placed at: {output_path}")
    print(f"  Seed used: {seed}  (pass --seed {seed} to reproduce this generation)")

    print("\nDone. Verify the DDS in-game and check that portrait scripts reference the correct path.")


if __name__ == "__main__":
    main()
