# ART DIRECTION — Pokémon Prismfall overworld

## 0. Hard requirements (SPINE Rev 5 + Rev 6) — read first
1. **Gen 4 / Gen 5 style only (DPPt / HGSS / BW).** No Gen 3 tiles and no Gen 3 palette anywhere. The stock Essentials
   FRLG/RSE tilesets (`Outside`, `Interior general`, `Caves`, all 25 base tilesets) are **banned** from every shipped map,
   interiors included. Everything comes from Gen 4/5-style packs or from custom tiles drawn to match them.
2. **Target look = Pokémon Rejuvenation's overworld** (Rev 6): tall timber-and-stone buildings with steep dark roofs, rows of
   townhouses, lush mixed foliage, textured dirt paths with pebbles, signboards, and a moody weather / time-of-day overlay.
3. **No generic tree walls.** Borders come from what the place is: cliffs, sea, city walls, rooftops, mountains, canals, ruins,
   and forest canopy only where the biome is forest.
4. **Real architecture at real scale.** Kingdom seats are castle cities: curtain walls, gatehouses, towers, keep or palace on
   high ground, cathedral, markets, harbour, slums, and grand interiors (throne room, great hall).

**Honest status.** Rejuvenation's, Reborn's and Desolation's own tilesets are **not reachable from this sandbox** (§2.4).
What we have is the next best thing: Pokémon Tectonic's sheets, a compilation from the same artist pool those games credit
(Kyledove, Magiscarf, Phyromatical, Hek-el-grande, Alucus, Speedialga, WesleyFG, Zetavares852, ThatsSoWitty and others).
It gets us the Gen 4/5 look and a castle kit today. It does **not** contain Rejuvenation's signature steep-roof timber
townhouses; those are either a user download (§2.4) or custom work (§5).

## 1. Target look
- 16-px pixel art doubled to 32-px tiles (verified: every 2×2 block in the Tectonic sheets is one colour). **All custom art
  is drawn on the 16-px logical grid and doubled with nearest-neighbour.** No anti-aliasing, no smooth scaling, no 1-px detail.
- Soft DPPt/HGSS ground palette, dark coloured outlines (never pure black), light from the top-left, 3–5 shades per material.
- Matches EBDX's Gen 5 battle sprites. Pure BW rips were rejected: none are reachable, and BW's tilted 3D buildings fight the
  RMXP grid and the community pieces.
- One style per map. Mixed styles are the most common fangame failure; a piece that looks off-style is cut, not "balanced".

## 2. Tileset decision

### 2.1 Primary: Pokémon Tectonic (cloned)
`/home/claude/ref/art/tectonic` — sparse, blobless clone of `github.com/Badagronk/Pokemon-Tectonic-Fork`
(upstream `xeuorux/Pokemon-Tectonic`). Repo licence: CC BY-NC-SA 4.0. Worktree 17 MB (.git 256 MB).

| File | Size | Covers |
|---|---|---|
| `Graphics/Tilesets/Outside.png` (tileset 24) | 256×32928, 8232 tiles | Outdoor town, route, city, cave, desert, snow, volcano, castle. Rough index by sheet row: 0–127 trees (round, pine, autumn, snow, palm, birch, dead, hollow stumps), bushes, tall grass, flowers, logs. 128–255 rocks, ponds, fences, bridges. 256–383 ground, cliffs, snow, sand, lava. 384–511 props, paving, **castle kit at 442–457** (curtain wall, crenellations, towers, stairs, arched gates and windows). 512–895 buildings (houses, shops, offices, towers, stadium, lighthouse, ships, trains, snow lodge). 896–1028 canyon rock, crystals, circuit lines, statues. |
| `Graphics/Tilesets/Inside.png` (tileset 25) | 256×19776 | Interiors: walls, floors, gym floors, furniture, lab, carpets, statues, stairs. |
| `Graphics/Tilesets/Outside_cloud.png` (23) | 256×31648 | Outside variant with cloud autotiles (sky areas: Skyreach). |
| `Graphics/Autotiles/*.png` | 60 files | water, sea, still water, ponds, waterfalls, currents, lava, lavafall, magma, tall grass variants, roads, brick/white paths, sand, snow and cave floors, clouds. None collide with base-project autotile names (checked the 9 used by tilesets 23–25). |
| `Data/Tilesets.rxdata` | | Passages, priorities, terrain tags for 23–25. JSON dump: `/home/claude/ref/art/dumps/tectonic/tilesets.json`. |
| `Data/Map*.rxdata` | 24 fetched of 443 | Reference maps (below). Fetch more: `git -C /home/claude/ref/art/tectonic sparse-checkout add '/Data/MapNNN.rxdata' && git -C ... checkout HEAD`. |

**Import** (MAPGEN §2b): `import_tileset.py` reads Tectonic's `Tilesets.rxdata` directly, so no passage data needs
authoring. Register as new IDs (suggest 30 Outside, 31 Inside, 32 Outside cloud). Tectonic defines its own terrain tags
above 16, so **remap on import**:

| Tectonic tag | → v21.1 | | Tectonic tag | → v21.1 |
|---|---|---|---|---|
| 0–16 | unchanged | | 25 SewerWater, 33 ActiveWater, 35–38 directional water | 7 Water (currents become events) |
| 17 Mud | 0 (v21's 17 is NoEffect) | | 26 RockClimb | 0; Core's Rock Climb is event-based |
| 18 Puddle | 16 | | 28 FishingContest | 6 StillWater |
| 19 SparseGrass, 21–23 flowery/tinted grass | 10 TallGrass | | 20, 24, 27, 29–32, 34, 39–43 | 0 |

**Gen 3 vetting (not finished).** `tools/gen3_vet.py` flags tiles sharing exact colours with the stock FRLG sheets:
1683 of 7701 tiles in Outside and 87 of 3753 in Inside. Some flags are shared neutral colours, some are real stock
Essentials pieces carried into the sheet. Nobody has looked at the flagged rows yet. **Rule: a palette may only reference
sheet rows that have been visually cleared; flagged rows are off-limits until then.** The trees, cliffs, castle kit and
city blocks seen in the renders are Gen 4/5 style.

**Reference maps** (rendered to `/home/claude/ref/art/renders/tectonic_NNN.png`). Use them to learn tiling rules with
`learn.py` and to mine building and prop stamps. **Do not copy layouts** (standing fangame etiquette; Rejuvenation's
asset rules say the same about its maps).

| ID | Map | Use as reference for |
|---|---|---|
| 217 | Sweetrock Harbor | Port on terraced cliffs, lighthouse, sea rocks: Ferrow's Landing, Saltmere |
| 187, 188 | Prizca East, Prizca Castle | Walled canal city, castle on the water: every kingdom seat, Crownhaven |
| 155 | Prizca West | Roads, towers, stadium: Zenith |
| 8, 56 | Velenz, Novo Town | Towns bounded by cliffs and ponds |
| 7 | Repora Forest | Dead-tree forest on terraces: Bleed zones, Gossamer Wood |
| 37 | Svait | Snow town: Isenmar |
| 130 | Canal Desert | Desert with canals: Ossaria |
| 211, 216 | Split Peaks, Highland Lake | Mountain and lake routes with waterfalls |
| 125, 218 | Volcanic Cave, Abyssal Cavern | Lava and cave-lake interiors |

### 2.2 Fallback: Pokémon Infinite Fusion (cloned, parts only)
`/home/claude/ref/art/pif` (`infinitefusion/infinitefusion-e18`, worktree 12 MB). Mixed styles with real Gen 3 content,
so **only** these, each after a visual check: `Graphics/Tilesets/caves.png` (dark crystal cave walls, shards),
`Underwater.png` (sunken temple columns: drowned Aurelia), `sky.png`, `sewers.png`. `Outdoor*.png` and `Indoor.PNG`
are not to be used wholesale.

### 2.3 Rejected
- `/home/claude/ref/art/valhalla` (Essentials-BES): its big sheet is RPG-Maker-style art, not Pokémon style.
- `/home/claude/ref/art/reborn-rebalance`, `/home/claude/ref/art/remix`: Reborn/Rejuvenation mods with no graphics.

### 2.4 Not reachable from here: Rejuvenation / Reborn / Desolation tilesets
Fourteen guessed GitHub paths for the three games do not exist, web search found no mirror, the GitHub API is blocked,
and rebornevo.com refuses automated fetches. These games ship only as downloads from rebornevo.com. If the user wants
the true Rejuvenation look, this is the one thing only they can do:
1. Download a game from its official page: Rejuvenation `https://www.rebornevo.com/forums/topic/53076-pokemon-rejuvenation-download/`
   (v14 notes: `https://rebornevo.com/rejuvdev/records/rejuvenation-v14-v1400-is-out-now-r77/`), Desolation
   `https://www.rebornevo.com/forums/topic/52360-pokemon-desolation-episode-51/`, Reborn via rebornevo.com's Reborn
   download page (URL not confirmed from here).
2. Send back three things from the game folder: `Graphics/Tilesets/`, `Graphics/Autotiles/`, `Data/Tilesets.rxdata`
   (plus `Graphics/Fogs/` for atmosphere). `import_tileset.py` then registers them with passages intact.
Rejuvenation's published asset rules: credit the Rejuvenation Team; maps may not be copied.

## 3. MAP QUALITY RUBRIC (the generator must pass this before a map ships)
Measured with `/home/claude/ref/art/tools/map_metrics.py` on 15 Tectonic outdoor maps versus 12 of ours:

| Metric | Tectonic | Ours today | **Required** |
|---|---|---|---|
| Tiles using layer 2 | 62–83% | 0–26% | **≥ 55%** |
| Tiles using layer 3 | 22–42% | 0.5–6% | **≥ 20%** |
| Bare tiles (ground only) | 10–31% | 73–97% | **≤ 35%** |
| Tiles inside a bare 3×3 patch | 0.3–13% | 27–80% | **≤ 10%** (≤ 13% with a paved plaza) |
| Distinct tile stacks per 100 tiles | 10–34 | 2–5 on routes | **≥ 10** |
| Left-right mirror match | mostly 2–16% | 14–44% | **≤ 15%** (open-sea maps exempt) |
| Size | towns 64–98 × 48–95 | 26–64 | towns ≥ 60×48, seats multi-map, routes ≥ 50 long |

1. **Density.** No empty lawns. Every 16×12 screen holds at least 3 decoration clusters (flowers, bushes, rocks, stumps,
   pebbled path edges, signs, lamps, crates) and at least one landmark visible from the main path.
2. **Organic composition.** No grids, no mirror symmetry, no straight 20-tile paths. Paths bend, widen into yards, and vary
   2–4 tiles in width. Buildings sit at offset rows and face streets. Formal symmetry is allowed only for palaces,
   cathedrals and arenas, and only locally.
3. **Elevation.** 2–3 height levels on every outdoor map that is not open water: cliff runs with inner and outer corners,
   stairs or ramps linking levels, ledges as one-way shortcuts on routes. The important building stands on the highest level.
4. **Borders from the place.** Allowed: stacked cliff terraces, sea with rocks, curtain walls, rooftops running off-map,
   canal walls, mountains, ruins. Forest canopy only in forest biomes, and then 2–4 trees deep, staggered edge, at least
   3 tree species, undergrowth at the foot. A single straight row of identical trees fails the map.
5. **Three layers.** Layer 1 ground and autotiles; layer 2 ground detail, cliff faces, building bodies, tree trunks;
   layer 3 canopies, roofs, overhangs, lamp tops (priority tiles the player walks behind).
6. **Water.** Shoreline autotile everywhere; 2+ depth tones on large water; rocks, reeds, lily pads or foam along edges;
   piers and quays on stone or timber, never bare grass meeting sea in a straight line.
7. **Town identity.** Each town has one signature landmark, its realm's banners and stone colour (§4), a market or square
   with props, and house types of at least 3 footprints. Kingdom seats follow §4's castle-city plan.
8. **Scale.** No dead space: nothing walkable is more than 6 tiles from something to look at or do. Maps grow for content,
   not for filler.
9. **Readability.** Walkable ground contrasts with blocked ground, doors and stairs are visible, paths are at least 2 wide,
   nothing important hides under a canopy. `build.py`'s reachability check still passes.
10. **Atmosphere (Rev 6).** Every map declares it in metadata: a weather (`Weather = Rain,…`), a base screen tone, and for
    outdoor maps the day/night tone. Forests, swamps, caves, the undercity and Bleed zones add a fog picture
    (`Graphics/Fogs/`, slow scroll, opacity 40–90). Cathedrals, great halls and forest clearings add a light-shaft picture.
    Realm defaults are in §4. A map with no weather, no tone and no fog needs a written reason.

## 4. Per-kingdom identity
Stone colour comes from recolouring Tectonic's castle kit (prototypes in §6). Banners use the realm cloth colour.

| Realm | Palette (stone / accent / cloth) | Seat and architecture | Signature props | Borders | Atmosphere | Tile source |
|---|---|---|---|---|---|---|
| **Elowen**, fairy forest | moss-grey stone / lantern gold, pink blossom / `#2F8A4A` | Gloaming: palace grown into giant trees, walled forest city; Briarwick: hollow-tree village | giant trunks, rope bridges, mushrooms, fairy lanterns, silk webs | old-growth canopy, root cliffs, rivers | green-gold tone, drifting-spore fog, light shafts | Tectonic trees and stumps; custom giant trees, webs |
| **Antumbra**, mirror world | violet stone / silver, teal glow / `#5A3A8A` | mirror-world palace over a void, floating islands, inverted stairs | broken mirrors, upside-down trees, floating rock | void and floating debris, never trees | cold violet tone, slow dark fog, no day/night | violet castle kit; custom void, mirrored set |
| **Isenmar**, frozen sea | ice-blue stone / white, aurora teal / `#3A7AB8` | fortress-ports: sea walls, ice-locked harbour, keep on a headland | ice floes, braziers, whale bones, ships in ice | sea ice, glaciers, sea walls | snow or rain, blue dusk tone, sea mist | Tectonic snow set, ships, lighthouse; ice castle kit |
| **Ashkaar**, dragonfire | basalt / ember orange, bronze / `#B02A20` | Wyrmrest: dragon citadel in a caldera, lava moats, causeways | dragon statues, braziers, obsidian spikes, lava falls | caldera walls, lava, ash slopes | ash fall, red-orange tone, heat-haze fog | Tectonic lava autotiles, cave walls; basalt castle kit, custom dragon pieces |
| **Ossaria**, bone sands | sandstone / bone white, turquoise / `#C8963A` | canyon cities cut into cliffs, tombs, fossil quarries | giant rib cages, obelisks, awnings, canals | canyon walls, dunes, mesas | sandstorm, warm bleached tone | Tectonic canyon rock, cacti, canals; sandstone castle kit, custom bones and tomb fronts |
| **Zenith**, the City Above | white marble / brass, teal glass / `#2A9A9A` | towering tech city: spires, sky-bridges, airship docks, plazas | airships, clock towers, pylons, trams | rooftops, cliff edge over cloud, city walls | clear by day, neon by night | Tectonic offices, roads, stadium, cloud set; custom night and neon variants, airships |
| **Nadir**, the City Below | rusted iron, dark brick / chem green, magenta neon / `#4A8A20` | vertical undercity: stacked walkways, shafts, sump canals, pit arenas | pipes, vents, scrap, neon signs, sump pools | shaft walls, pipework, the city's underside | permanent dusk tone, green smog fog | Tectonic sewer and factory pieces, PIF sewers; custom sump water, pipes, neon |
| **Crownhaven**, the capital | pale gold stone / royal blue, gold / `#2A3A9A` | grandest castle city: concentric walls, cathedral, market, harbour, slums, Festival arena, palace with throne room | 18 Plate banners, fountains, statues | curtain walls, river, rooftops | clear, warm tone; festival confetti | Tectonic castle kit, canals, townhouses; custom arena and grand interiors |

## 5. Gap list (art we lack) and how each is filled
All custom work derives from the Tectonic sheets with PIL, on the 16-px grid (§6).

| Gap | Fill |
|---|---|
| **Rejuvenation-style steep-roof timber townhouses** | Not in any reachable pack. Best: user download (§2.4). Otherwise custom: re-roof Tectonic house bodies with a drawn steep dark-green roof kit. Largest single custom job. |
| **Grand interiors** (throne room, great hall, cathedral nave) | Tectonic interiors are modest. Compose from castle-kit stone as interior walls, Outside paving rows 433–441 as marble floors, Inside carpets and statues; draw thrones, banners, columns, stained glass, chandeliers. |
| Kingdom fortresses in four stone colours | Palette remap of the castle kit. Done as prototype. |
| Giant-tree villages | Assemble 6×8 trees from canopy tiles and stump bark; doors and windows from house tiles; draw rope bridges. |
| Silk webs | Web overlays on trees (prototype), web curtains, cocoons, silk-floor autotile. |
| Neon city | Night remap of Tectonic city blocks with emissive windows, trims and signs (prototype). |
| Undercity sumps | Recoloured water autotiles (prototype), pipes and grates from Tectonic sewer and factory pieces, PIF `sewers.png`. |
| Crystal caves | Tectonic crystal clusters (rows ~955–975), PIF `caves.png` dark crystal walls, recoloured cave autotiles. |
| Glassed / Bleed land | Crystal remap of trees (prototype), grass and rocks. |
| Mirror world | Violet castle kit (prototype), flipped trees, void panorama, floating-island edges from cliff tiles. |
| Drowned Aurelia | PIF `Underwater.png` temple pieces after vetting, plus the castle kit toned blue-green. |
| Dragon citadel, bone-sand fossils, airships, the Dovetail's deck | Custom, built from the castle kit, canyon rock and Tectonic ship tiles. |

## 6. Custom-tile pipeline and prototypes
Scripts in `/home/claude/ref/art/tools/`, outputs in `/home/claude/ref/art/custom/`.
- `proto_tiles.py` → `crystal_tree_2x3.png`, `silk_tree_2x3.png`, `Sump water.png` (a complete autotile),
  `neon_tower_3x9.png`; preview `_preview.png`.
- `proto_castle.py` → `castle_kit_{ashkaar_basalt,ossaria_sandstone,isenmar_ice,antumbra_mirror}.png`,
  `banners_1x2_x8.png` (one per realm), `throne_2x3_{crownhaven,ashkaar}.png`; preview `_preview_castle.png`.
- Method: halve to 16-px, remap each source colour once (palette size is preserved), draw new pixels on that grid, double.
- Result, looked at: recolours and banners sit cleanly in the pack's style. The silk web, thrones and neon tower read
  correctly but are proofs, not final art; the neon windows and the Ashkaar kit (needs ember accents) want hand polish.
- Other tools: `sheet_grid.py` (row-numbered crops for cataloguing), `sheet_strip.py`, `render_ref.py`, `map_metrics.py`,
  `gen3_vet.py`.

## 7. Credits
Artist credits and usage terms are in `/home/claude/fangame/docs/CREDITS.md`. Tectonic's repo is CC BY-NC-SA 4.0, so
our derived tiles carry the same terms.
