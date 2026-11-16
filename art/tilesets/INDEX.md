# Import-ready tilesets (art/tilesets)

Register one with `python3 -I mapgen/import_tileset.py art/tilesets/<key>.yaml`. Each sheet is 256 px wide, 32-px tiles.
Place stamps from `<key>_contact.png` (label = `name x,y WxH` in sheet tiles) or `<key>_stamps.json`
(`tile_rect` = [x, y, w, h], `first_tile_id` = 384 + y*8 + x; each stamp is a solid w×h block of consecutive rows).

| Key | ID | Sheet | Stamps | What is in it | State |
|---|---|---|---|---|---|
| `town_props` | 41 | `PF Town Props.png` | 80 | Magiscarf: crates, market tables, kilns, rug and laundry lines, plank paths, barrels, sheds, fence. Ekat: iron street lamps, flower planters, brick garden walls and arches, parasol tables, topiary, gazebo, fountain basin | Looked at; clean |
| `houses` | 42 | `PF Houses.png` | 89 | Magiscarf: timber and half-timber houses, 26 doors and arches (open and closed). Ekat: steep "pointy" roof kit in red, blue, olive, green; windows; Jonquil harbour pieces (lighthouse, boats, bollards, pier, tubs) | Looked at; clean. Pointy roofs are a modular kit, not whole houses |
| `landmarks` | 43 | `PF Landmarks.png` | 31 | Uranium: domed palace, glass-dome arena, brick opera house, black pagoda, gabled manor, tower block, cooling tower. Ekat: Dragonspiral columns and ruin walls | **Rough.** Uranium rectangles are hand-picked and include slivers of neighbouring buildings and marker tiles; trim before use |
| `forest` | 44 | `PF Forest.png` | 109 | Magiscarf: 4 green and 4 autumn trees, stumps, rocks, rock arches, bushes. Ekat: fairy-wood bushes, vines, crystals, big trees, haunted woods | Looked at first half; ground-patch stamps are decals, not trees |
| `interiors` | 45 | `PF Interiors.png` | 59 | Ekat: basic furniture, wine cellar, mansion, ship interior | Built, not looked at |

**Passage rules used** (check before trusting on a critical path): houses, doors and landmarks are solid except the top
row of stamps 4+ tiles tall, which is overhead. Props and trees are solid on their bottom row only; every row above is
overhead (priority = rows above the base, max 5). Flat decals inside prop stamps (plank paths, ground patches) therefore
come out wrong and need `passage 0, priority 0` by hand.

**Autotiles** (`autotiles/`, slots 1–7 in every descriptor): `water2`, `Sea`, `Dirt`, `Brick path`, `Gravel`,
`Light grass`, `Tall Grass` from Tectonic. Spares in the folder: `Road`, `Sand`, `Sand shore`, `Still water`, `Pond`,
`White path`, `Waterfall2`, and Rejuvenation's `DirtDark`. No cliff autotile exists in any source; cliffs are plain tiles
in Tectonic's Outside sheet (tileset 30).

**Style families.** Magiscarf's pieces are 32-px art with 1-px detail; Ekat's and Tectonic's are 16-px art doubled.
Side by side the difference shows. Prefer one family per map.

**`ekat_x2/`**: 69 of Ekat's 80 sheets doubled to 256 px wide, unused-tile markers cleared, with her `Credits.txt`.
No descriptors or passages yet. Eleven sheets with odd sizes were skipped (Silph City, Jonquil Town, Coral Tiles, others).

Rebuild: `python3 -I /home/claude/ref/art/tools/build_sheet.py all` (sheet recipes are the `SHEETS` table in that file).
