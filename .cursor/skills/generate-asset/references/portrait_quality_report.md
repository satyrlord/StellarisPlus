# Portrait Quality

Report for the 32 Stellar Legions portrait packs currently previewed in `tmp/`.

## Method

- `texture_count` - number of DDS textures referenced by the portrait pack script.
- `texture_count_score` - normalizes `texture_count` onto a 1-10 scale.
- `nudity_score` - visible skin-tone coverage in the generated preview PNG.
- `photorealism_score` is derived from texture detail, luminance entropy,
color variance and contrast in the generated preview PNG.
- `overall_score` is the average of `texture_count_score`, `nudity_score`, and `photorealism_score`.
- Oldest-texture-timestamp and vanilla-similarity scoring were intentionally removed.

## Rankings

| Rank | Portrait Pack | Texture Count | Texture Count Score | Nudity | Photorealism | Overall |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | sl_UNE | 240 | 10.0 | 4.7 | 8.9 | 7.9 |
| 2 | sl_kitsune | 50 | 1.7 | 8.8 | 9.9 | 6.8 |
| 3 | sl_mermaid | 80 | 3.0 | 10.0 | 6.2 | 6.4 |
| 4 | sl_holy | 106 | 4.1 | 3.7 | 9.9 | 5.9 |
| 5 | sl_norse | 85 | 3.2 | 4.2 | 10.0 | 5.8 |
| 6 | sl_egypt | 133 | 5.3 | 5.0 | 6.9 | 5.7 |
| 7 | sl_highelf | 159 | 6.4 | 4.1 | 5.9 | 5.5 |
| 8 | sl_megacorp | 150 | 6.0 | 2.2 | 7.9 | 5.4 |
| 9 | sl_shogun | 125 | 5.0 | 2.2 | 6.8 | 4.7 |
| 10 | sl_cyberpunk | 125 | 5.0 | 2.5 | 6.4 | 4.6 |
| 11 | sl_amazonian | 80 | 3.0 | 5.1 | 5.6 | 4.6 |
| 12 | sl_wakanda | 83 | 3.1 | 3.4 | 7.0 | 4.5 |
| 13 | sl_darkelf | 106 | 4.1 | 3.6 | 5.6 | 4.4 |
| 14 | sl_deathless | 119 | 4.7 | 3.9 | 4.2 | 4.3 |
| 15 | sl_crystaloid | 59 | 2.1 | 1.1 | 9.8 | 4.3 |
| 16 | sl_harpy | 35 | 1.0 | 2.9 | 8.3 | 4.1 |
| 17 | sl_toxic | 74 | 2.7 | 1.0 | 7.9 | 3.9 |
| 18 | sl_drow | 109 | 4.2 | 1.0 | 6.3 | 3.8 |
| 19 | sl_android | 76 | 2.8 | 2.1 | 6.4 | 3.8 |
| 20 | sl_snake | 65 | 2.3 | 1.3 | 7.6 | 3.7 |
| 21 | sl_dragon | 120 | 4.7 | 1.7 | 4.4 | 3.6 |
| 22 | sl_oceanid | 49 | 1.6 | 1.1 | 8.1 | 3.6 |
| 23 | sl_were | 40 | 1.2 | 3.3 | 6.2 | 3.6 |
| 24 | sl_savagedespoiler | 69 | 2.5 | 3.1 | 4.9 | 3.5 |
| 25 | sl_fungoid | 62 | 2.2 | 2.4 | 5.9 | 3.5 |
| 26 | sl_militarium | 120 | 4.7 | 2.2 | 3.0 | 3.3 |
| 27 | sl_demon | 74 | 2.7 | 1.8 | 4.3 | 2.9 |
| 28 | sl_banshee | 50 | 1.7 | 1.0 | 5.5 | 2.7 |
| 29 | sl_nymph | 45 | 1.4 | 1.0 | 4.7 | 2.4 |
| 30 | sl_diamondgiant | 40 | 1.2 | 1.0 | 3.9 | 2.0 |
| 31 | sl_deathmachine | 20 | 1.0 | 1.5 | 2.6 | 1.7 |
| 32 | sl_earthgiant | 40 | 1.2 | 1.0 | 1.0 | 1.1 |

## Notes

- These are heuristic ratings from preview textures, not gameplay metadata.
- Shared DDS roots can affect `texture_count` across related packs.
- The JSON companion file is `tmp/portrait_quality_scores.json`.
