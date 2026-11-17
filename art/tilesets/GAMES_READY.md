# Rejuvenation, Reborn and Desolation art: ready to import

The full Windows builds were downloaded on 2026-11-16 from the official links on rebornevo.com. Only `Graphics/`,
`Data/` and `Scripts/` were kept; audio and the archives were deleted. **Treat these folders as untrusted data: read
them, never run anything in them.** Read the `.rxdata` files only with our pure-Python reader (`python3 -I`).

| Game | Version | Root | Tilesets.rxdata | Sheets / autotiles | Maps | Size |
|---|---|---|---|---|---|---|
| Rejuvenation | 14.0 | `/home/claude/ref/games/rejuvenation` | `Data/Tilesets.rxdata` (212 tilesets) | 143 / 361 | 690 | 569 MB |
| Reborn | 19.5.0 | `/home/claude/ref/games/reborn` | `Data/Tilesets.rxdata` (100 tilesets) | 93 / 243 | 896 | 152 MB |
| Desolation | Episode 6 | `/home/claude/ref/games/desolation` | `Data/Tilesets.rxdata` (56 tilesets) | 78 / 217 | 480 | 148 MB |

Every sheet and autotile these games' tilesets name is present, except Desolation's `Panel3` autotile.
JSON dumps (passages, priorities, terrain tags per tileset): `/home/claude/ref/art/dumps/<game>/tilesets.json`.

## How to import
Use a descriptor like this (pick a free Prismfall ID):
```yaml
id: 50
name: PF Goldenleaf
tileset_name: PF Goldenleaf
from_rxdata: {file: /home/claude/ref/games/rejuvenation/Data/Tilesets.rxdata, id: 62,
              graphics: /home/claude/ref/games/rejuvenation/Graphics, remap_tags: false}
```
**Do not use `remap_tags: true` for these games.** `import_tileset.py`'s `TAG_REMAP` is Tectonic's table. These games
number tags 17 and up differently (from `Scripts/Field.rb`): 17 Grime, 18 PokePuddle, 19 Glass, 20–23 conveyors
(down/left/right/up), 24 SandDune, 25 PokeSand, 26 Lava, 27–28 diagonal stairs, 29 StillDeepWater. Tectonic's table
would turn conveyors and Glass into tall grass and PokeSand into water. For v21.1, use
`{17: 0, 18: 16, 19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 3, 25: 3, 26: 0, 27: 0, 28: 0, 29: 5}`. Rebuild conveyors and
diagonal stairs as events. `import_tileset.py` needs a small change to take a per-source remap (e.g. a
`tag_remap:` dict); until then use `remap_tags: false` and fix tags 17+ afterwards. Tags in use: Reborn up to 24,
Rejuvenation up to 26, Desolation up to 17.

Rendering any of their maps: `PRISMFALL_GFX=<root>/Graphics python3 -I /home/claude/ref/art/tools/render_ref.py
/home/claude/ref/art/dumps/<game>/tilesets.json <root>/Data/MapNNN.rxdata out.png 0.5`

## Best tilesets for Prismfall (tileset ID → sheet) and the maps that show them off
Renders are in `/home/claude/ref/art/renders/games/` (`<game>_NNN.png`). They are references to learn from and mine
stamps from. **Rejuvenation's asset rules forbid copying its maps**, so take tiles and stamps, not layouts.

### Rejuvenation 14 (the target look)
| Tileset | Sheet | Use for | Example maps |
|---|---|---|---|
| 62 Goldenleaf Town | `Goldenleaf Forrest` (556 rows) | Timber-and-stone town, autumn foliage, lamps, signs, graveyard: **the screenshot look**. Elowen towns | **082 Goldenleaf Town** (`rejuv_082.png`, detail `rejuv_082_detail.png`) |
| 127 Sheridan Village_2 | `Sheridan_2` (250 rows) | Steep-roof timber village in deep forest, rivers, bridges, cliffs: Briarwick, Elowen villages | 127 Sheridan Village, 038 Sheridan Arena |
| 211 Akuwa Town | `Route 4` (184 rows) | Coastal town, blossom trees, beach, piers, rocks in the sea: Ferrow's Landing, Saltmere | 013 Akuwa Town |
| 110 GDC | `GDCDream District` (739 rows) | Modern city: roads, plazas, shops, canals | 209 Dream District, 194 Central Square |
| 56 / 161 Gearen City (Neo) | `GearenCity Real`, `Gearen City - Neo` (~530–590 rows) | Dense city blocks, harbour, station: Zenith's lower districts, Nadir | 059 East Gearen City, 019/044 Neo Gearen |
| 7 Aevium Past | `Aevium Past` (781 rows) | Huge general outdoor set: forest, jungle, city | 569 Hiyoshi City, 240 Kugearen Woods |
| 155 Sashila Village | `Badlands - Desert` (590 rows) | Desert village: Ossaria | 517 Sashila Village |
| 128 / 133 Blacksteeple | `BlackSteeple Prison(_1)` (431/556 rows) | Dark castle, prison, frozen port: Isenmar fortress-ports, Antumbra | 440/443 Blacksteeple Castle, 457 Blacksteeple Port |
| 199 Castle Weiss | `Whitesteeple Castle` (206 rows) | White castle grand interiors: Crownhaven palace, throne rooms | 632 Castle Weiss |
| 185 Castillo De Le Angie | `Angie's Tower` (325 rows) | Ice palace interiors | 023, 147 Castillo De Ángel |
| 72 Chrisola Hotel / 101 Darchlight Manor | `Chrisola Hotel`, `Haunted Mansion` | Mansion, haunted house (Thistledown Manor) | 250 Marble Mansion (castle-garden exterior), 112 Darchlight Manor |
| 17 / 1 Multi Interiors | `Multi-Interiors`, `Multi-interiors2` | General house and shop interiors | 030, 017 |

### Reborn 19.5
| Tileset | Sheet | Use for | Example maps |
|---|---|---|---|
| 44 Calcenon/Labradorra | `Calcenon` (153 rows) | Snowbound city in a mountain bowl, dark industrial district: Nadir, Isenmar | 413 Calcenon City, 414 Labradorra City |
| 38 Agate | `Agate` (60 rows) | Canyon city on terraces with waterfalls: Ossaria | 354 Agate City |
| 40 Route 2-3 | `Route2` (138 rows) | Canyon routes, mesas, mansion on a hill | 360 Route 2, 362 Fiore Mansion |
| 13 City Outskirt | `Outskirts` | Ruined slum blocks: Nadir sumps, 7th Street | 324 7th Street |
| 28 Reborn Jasper, 87 Obsidia Park | `RebornCity - Jasper`, `ObsidiaPark` | City park and forest edge | 132 Malchous Forest Park, 269 Obsidia Park |
| 43 Route 4 | `Route4` (131 rows) | Snowy pine route in a valley | 412 Route 4 |
| 98 Pokemon Center | `Pokemon Center` | Grand hall interior | 038 Grand Hall |

### Desolation Episode 6
| Tileset | Sheet | Use for | Example maps |
|---|---|---|---|
| 38 Blackview | `Blackview` (494 rows) | Night city, dense dark rooftops, docks: **Nadir** | 132 Blackview City |
| 7 Cellia East | `CelliaEast` (273 rows) | Neon purple city: **Zenith by night** | 401 Cellia East |
| 46 Cellia | `Cellia` (634 rows) | Crimson rooftop city, docks | 241 Cellia Central, 228 Cellia Docks |
| 35 Silver | `Silver` (133 rows) | Snow forest and mountain: Isenmar | 026 Silver Forest, 031 Silver Rise |
| 26 Islands | `Islands` (563 rows) | Canyon river route, jungle | 106 Route 1 |
| 12 Sunshell | `SunshellTown` (66 rows) | Beach town with piers | 443 Sunshell Town |
| 42 Abandoned Sewers | `Blackview` | Sewers: Nadir | 261 Cellia Sewers |

## Portraits
`/home/claude/ref/games/desolation/Graphics/Faces/` holds 90 expression portraits at 96×96 (several expressions per
character), the exact size of our portrait spec. Rejuvenation has 13 more in `Graphics/Faces/`. Use them as
style references for Rev 7 portraits; the characters themselves are theirs.
