# Stellaris DDS Format Reference

Quick reference for DDS texture formats used in Stellaris modding.

## Common Stellaris Asset Dimensions

| Asset type | Typical size | Notes |
| --------- | ------------ | ----- |
| Tradition tree icon | 60x60 | `gfx/interface/icons/traditions/tree_icons/` |
| Tradition hex background | 370x300 | `gfx/interface/traditions/` |
| Tradition individual icon | 45x45 | `gfx/interface/icons/traditions/` |
| Building icon | 64x64 | `gfx/interface/icons/buildings/` |
| District icon | 64x64 | `gfx/interface/icons/districts/` |
| Modifier icon | 29x29 | `gfx/interface/icons/modifiers/` |
| Trait icon | 29x29 | `gfx/interface/icons/traits/` |
| Edict icon | 46x46 | `gfx/interface/icons/edicts/` |
| Technology icon | 46x46 | `gfx/interface/icons/technologies/` |
| Flag emblem | 128x128 | `gfx/models/emblems/` |
| Ship diffuse texture | 512-2048 | varies by hull size |
| Ship normal map | 512-2048 | same resolution as diffuse |
| Planet modifier icon | 29x29 | `gfx/interface/icons/planet_modifiers/` |

## DDS Format Arguments for image_dds

These are the format strings passed to `img2dds`:

| Format | Compression | Alpha | Best for |
| ------ | ----------- | ----- | -------- |
| `BC1RgbaUnorm` | DXT1 | 1-bit | Opaque textures, diffuse maps |
| `BC3RgbaUnorm` | DXT5 | Full 8-bit | Icons with transparency (most UI) |
| `BC5RgUnorm` | -- | N/A | Normal maps (two-channel) |
| `BC7RgbaUnorm` | -- | Full 8-bit | High-quality everything (larger files) |
| `Rgba8Unorm` | None | Full 8-bit | Tiny icons (under 32x32), uncompressed |

**Default recommendation**: `BC3RgbaUnorm` for most Stellaris UI assets.

> **DX10 header pitfall**: `image_dds` (`img2dds`) always writes a DX10
> extended-header DDS (20 extra bytes, fourcc = `DX10`). Stellaris requires
> the legacy DXT5 header (fourcc = `DXT5`). The `generate_portrait.py`
> pipeline calls `_dx10_to_legacy_dxt5()` automatically after every
> conversion. If producing DDS by any other tool, check bytes 84-88 of the
> file equal `b'DXT5'`; if they equal `b'DX10'`, the file will display as
> corrupted in-game.

## File Path Conventions

Stellaris expects specific naming patterns. Examples from vanilla:

- `gfx/interface/icons/modifiers/mod_<modifier_key>.dds`
- `gfx/interface/icons/buildings/building_<building_key>.dds`
- `gfx/interface/icons/traditions/tree_icons/tradition_icon_<category>.dds`
- `gfx/interface/icons/traits/trait_<trait_key>.dds`

The GFX sprite definition in `interface/*.gfx` links the game key to the file path:

```Paradox script
spriteType = {
    name = "GFX_<key>"
    texturefile = "gfx/interface/icons/modifiers/mod_<key>.dds"
}
```
