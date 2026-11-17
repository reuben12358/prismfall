# ART DIRECTION — Pokémon Prismfall overworld

## 0. Hard requirements (SPINE Rev 5–8) — read first
1. **No stock Essentials tiles.** The base project's FireRed/LeafGreen-looking tilesets (`Outside`, `Interior general`,
   `Caves` and the rest of the 25) are banned from every shipped map, interiors included.
2. **The only style test is beauty** (Rev 8). Rejuvenation/Reborn-style tiles with saturated greens are fine, and so are
   well-drawn Gen 3-derived community sets. Keep each map to one visual family so pieces do not clash.
3. **Target look = Pokémon Rejuvenation's overworld** (Rev 6): tall timber-and-stone buildings with steep dark roofs, rows of
   townhouses, lush mixed foliage, textured dirt paths with pebbles, signboards, and a moody weather / time-of-day overlay.
4. **No generic tree walls.** Borders come from what the place is: cliffs, sea, city walls, rooftops, mountains, canals, ruins,
   and forest canopy only where the biome is forest.
5. **Real architecture at real scale.** Kingdom seats are castle cities: curtain walls, gatehouses, towers, keep or palace on
   high ground, cathedral, markets, harbour, slums, and grand interiors (throne room, great hall).

**Status (2026-11-16).** The full **Rejuvenation 14, Reborn 19.5 and Desolation E6** games are downloaded (their
Graphics and Data only) to `/home/claude/ref/games/` and rank at the top of §2.0. That gives us the target look
directly: Rejuvenation's Goldenleaf and Sheridan sets are the screenshot look. Import guide for builders:
`/home/claude/fangame/art/tilesets/GAMES_READY.md`. The ten community sources below stay as supplements.

## 1. Target look
- 16-px pixel art doubled to 32-px tiles (verified: every 2×2 block in the Tectonic sheets is one colour). **All custom art
  is drawn on the 16-px logical grid and doubled with nearest-neighbour.** No anti-aliasing, no smooth scaling, no 1-px detail.
- Soft DPPt/HGSS ground palette, dark coloured outlines (never pure black), light from the top-left, 3–5 shades per material.
- Matches EBDX's Gen 5 battle sprites. Pure BW rips were rejected: none are reachable, and BW's tilted 3D buildings fight the
  RMXP grid and the community pieces.
- One style per map. Mixed styles are the most common fangame failure; a piece that looks off-style is cut, not "balanced".

## 2. Tileset decision

### 2.0 Ranked sources
**Tier A: the three games** (official Windows builds from rebornevo.com, downloaded 2026-11-16; Graphics, Data and
Scripts kept, audio and archives deleted; untrusted data, never run). All tileset sheets and autotiles their
`Tilesets.rxdata` names are present, so they import with passages, priorities and terrain tags intact
(`from_rxdata:`), with one caveat: their terrain tags 17+ differ from Tectonic's (see GAMES_READY.md).

| Rank | Game | Path | Contents | Verdict (renders in `/home/claude/ref/art/renders/games/`) |
|---|---|---|---|---|
| A1 | **Rejuvenation 14.0** | `/home/claude/ref/games/rejuvenation` (569 MB) | 212 tilesets, 143 sheets, 361 autotiles, 690 maps; 4913 Characters (357 trainer sprites), 2355 Battlers, 1829 Pictures, 26 Fogs, 63 Panoramas, 396 Transitions, 13 Faces | **The target.** Goldenleaf Town (082) is the screenshot look: timber-and-stone houses, autumn trees, lamps, signs, pebbled roads. Also Sheridan (127, 038), Akuwa coast town (013), modern cities (209, 194, 059), desert village (517), dark castle and frozen port (440, 457), white-castle grand interiors (632), ice palace (023), mansions (250, 112). Covers most kingdoms. |
| A2 | **Desolation E6** | `/home/claude/ref/games/desolation` (148 MB) | 56 tilesets, 78 sheets, 217 autotiles, 480 maps; 1478 Characters, 1423 Battlers, 622 Pictures, 22 Fogs, **90 Faces (96×96 expression portraits)** | Best night cities: Blackview (132) for Nadir, neon Cellia East (401) for Zenith by night, crimson Cellia (241), docks (228), sewers (261); snow forest (026), canyon river (106), beach town (443). Dense and moody. |
| A3 | **Reborn 19.5.0** | `/home/claude/ref/games/reborn` (152 MB) | 100 tilesets, 93 sheets, 243 autotiles, 896 maps; 1700 Characters (297 trainer sprites), 1326 Battlers, 539 Pictures | Snow city in a mountain bowl (413), dark industrial city (414), canyon city (354, Ossaria), canyon routes (360), slum blocks (324, Nadir), park and forest (132, 269), snowy route (412), grand hall (038). Its mountains are blocky stacked-cliff terraces; use them sparingly. |

**Tier B: community sources** (earlier finds; supplements, mostly loose sheets):

| Rank | Source | Path | Verdict |
|---|---|---|---|
| B1 | **Rejuvenation v13.5 sheets** (superseded by A1) via `pbflo/Where-Love-Lies-Overhaul` | `/home/claude/ref/art/wll` (17 MB) | The real thing: Sheridan's timber houses with steep dark roofs, vines, flower borders, signposts; Gearen's apartment blocks, scaffolds, museum facade. Partial set. |
| B2 | **Tectonic** | `/home/claude/ref/art/tectonic` | Clean Gen 4/5 look, widest coverage, castle kit, complete autotiles and passages. Plainer houses. |
| B3 | **Community packs inside `M0RGEBBY/pokemon-fan-game`** | `/home/claude/ref/art/morgebby/Graphics/Tilesets/Tilesets/` (13 MB repo) | The richest find for towns. Two mega-sheets (`dbf3bkq-…png` 1920×3360, `ddpuooa-…png` 3328×2752; identified as Magiscarf's "Tileset ver.3" and "Revamped Tiles", non-commercial): four-season trees and ground, timber houses, castle towers, stone bridges, fountains, canals, torii, windows and doors. Magiscarf's rustic tiles (timber houses, market stalls, washing lines, kilns, crates, rock arches) and concrete tiles. Also princess-phoenix (desert interior, Excello village, burrow), carchagui (city tiles, swamp village, mountains), aveontrainer (factory, machinery, log cabin), Phyromatical (Victory ruins), Zeo254. Beautiful, on target. **All 16-px native: double on import.** No passage data. |
| B4 | **Ekat's Public Tiles** (80 sheets, same folder, `Ekat's Public Tiles/`, with `Credits.txt`) | as above | Steep-roof "Pointy Buildings", Brick City, Jonquil Town, Silph City (sci-fi), Volcano Set, Haunted and Fairy Woods, Floating Cliffs, Wine Cellar, Ship Interior, Dragonspiral, Snowpoint Temple, Wild West, Coral, Deep Sea, garden and patio props. Charming and dense; Emerald-scale palette, so use as its own family. 16-px native, no passage data. |
| B5 | **Pokémon Uranium tiles** via `acedogblast/Project-Uranium-Godot` | `/home/claude/ref/art/uranium/Maps/tilesets/` (4 MB) | `PU_buildings+` is a strong Gen 4-style city set: towers, domed palace, brick mansion, pagoda, cooling towers, stadium, harbour. Plus ground, water, caves, indoors. Wide sheets (512–912 px), 32-px tiles; needs re-cutting to 8 columns. No RMXP passage data. |
| B6 | **Infinite Fusion 2: Hoenn** | `/home/claude/ref/art/pif-hoenn` (6 MB) | 22 sheets with `Tilesets.rxdata`: Rustboro, Slateport, Mauville, Dewford town sets (apartments, market stalls, fountains, lighthouse, shipyard), routes, caves, contest and power-plant interiors. Clean and attractive. Maps not fetched. |
| B7 | **`Aiwyn17/pokemon` sub-tilesets** | `/home/claude/ref/art/aiwyn/Graphics/Tilesets/` | Ice kingdom material: Freljord villages and port (4480 px), frozen routes, demigod sanctuary, trial cavern, an airship; plus Akizakura16's hi-res interior sheet (19168 px). Direct fit for Isenmar and Zenith's airships. Looks good at sheet level; no maps rendered. |
| B8 | Infinite Fusion (parts) | `/home/claude/ref/art/pif` | Caves, underwater temple, sewers only. |
| B9 | LPC (ElizaWy) | `/home/claude/ref/art/_probe/ElizaWy_LPC` (tree only, not checked out) | Open-licence 32-px walls, floors, furniture. Different proportions from Pokémon art; last resort for grand-interior furniture. |
| B10 | Kenney CC0 library | `/home/claude/ref/art/_probe/Tiddybub_2d-assets` (tree only) | CC0 but flat vector style; does not match. Not recommended. |

**Tier C: web hunt of 2026-11-17** (Eevee Expo and DeviantArt; full notes, file paths and best pieces in
`/home/claude/fangame/art/tilesets/NEW_SOURCES.md`; boards in `/home/claude/ref/art/renders/new_sources/`). Loose sheets
under `/home/claude/ref/assets/<source>/`, no passage data. Density: `x2` = doubled 16-px art like the games, `16` = double
on import, `hi` = 32-px art with 1-px detail (own map family, or halve-then-double and touch up).

| Rank | Source | Density | Verdict |
|---|---|---|---|
| C1 | **TerribleJared** (DeviantArt) | hi | Muted, cohesive, beautiful. Cargo ships, ferries, yachts and quay props; brick sewer and sump shanties; graveyard and mausoleums; adobe desert town with domed palace; dragon-keeper buildings and statues. Closes **harbour/ships, undercity, desert city, Ashkaar dragon culture**. |
| C2 | **WesleyFG's DPPt** (Eevee Expo 295) | x2 | RMXP-ready 256×26752 DPPt building library: four-spired League hall (recolour as basilica), library mansion, glass towers, stadium, ferries, cranes, lighthouses. Same density as our maps. |
| C3 | **PkmnAlexandrite** (DeviantArt) | x2 / 16 | Civic landmarks: domed cathedral, clock tower, mansard town hall (guildhall), bank, library, glass Neocity towers, food trucks. Closes **guildhalls, city blocks**. |
| C4 | **Magiscarf extra sheets** (DeviantArt) | 16 | Snow-capped trees in six colours (**frozen forests**), white-stone castle towers and bridges, snowy stone townhouses, crystal cave. |
| C5 | **PeekyChew** (DeviantArt) | hi / 16 | Full Bodiam-style **castle** stamp; snow, desert, beach dumps; animated lava and cave tiles. |
| C6 | **Phyromatical** "December of Tilesets" | 16 / hi | Distortion World floating islands (**mirror world**), dark ruins, water-dungeon temple (drowned Aurelia), two ice caves, slate-roof timber houses, cloud realm. |
| C7 | **UltimoSpriter** BW tiles | 16 | Black City towers (**neon/night city**), Virbank industry, cranes and containers. |
| C8 | **Pokémon Gaia, compiled** (Eevee Expo 1377) | x2 | RMXP-ready modern Gen 4 city with road autotiles. |
| C9 | Smaller fills | mixed | carchagui snow chalets; J-Treecko252 crystals in eight colours (**crystal caves**); aveontrainer sewer and airport; princess-phoenix fossil museum and factory interiors; Akizakura16 4th-gen indoor/outdoor; moca Public Gen 4; SirMalo HGSS rips; KingTapir desert; Kyle Dove biome tiles. |

Dropped as off-style: figyberries, CoreBear, ORAS/XY and Orre battlebacks (blurry 3D or bland), Elinthind crystal
cave, itch.io packs. Dropped as private or permission-only: The-Red-eX's Dawn tiles, aveontrainer's Church, Phyromatical's
Lava Cavern, Hek's tower, DirtyWiggles, chimcharsfireworkd. **Credit fix:** morgebby's unnamed mega-sheets `dbf3bkq` and
`ddpuooa` are Magiscarf's "Tileset ver.3" and "Revamped Tiles" (non-commercial).
**Trainer sprites** (kitbash bases, Showdown's 1500 BW-style fronts, kyledove classes, B2W2 VS busts, 316 Wergan
overworlds): see the TRAINER SPRITES section of NEW_SOURCES.md.

**What the new sources close.** Steep-roof townhouses and more house shapes (1, 3, 4), street props such as stalls,
washing lines, fountains, barrels and lamps (3, 4, 6), landmark buildings (5: domed palace, mansion; 3: towers), castle and
bridge stonework (2, 3), ice kingdom (7), sci-fi city (4, 5), volcano and haunted woods (4), desert interior (3).
Tier C adds ships and harbour props (C1, C2), sewer and slum pieces (C1, C7, C9), civic cathedral and guildhalls (C2, C3),
a castle stamp (C5), frozen-forest trees and chalets (C4, C9), mirror-world islands (C6) and crystals (C9).
**Still thin:** grand throne-room, great-hall and cathedral-nave interiors; airships; a full mirror/glass world; dragon
citadel; obsidian glass-desert; neon signage. Custom work (§5).

**Import cost.** Sources 1, 2 and 6 come with passages. Sources 3, 4, 5 and 7 are loose sheets: they must be cut into
256-px-wide RMXP sheets (16-px art doubled first) and given passages, priorities and terrain tags by hand or by rule.
Nothing from sources 3–7 has been rendered in a map yet; the judgements above are from the sheets.

**Rejuvenation sheets in `wll/Changed Files/Graphics/Tilesets/`** (passages, priorities, terrain tags in
`wll/Changed Files/Data/Tilesets.rxdata`; dump `/home/claude/ref/art/dumps/wll/tilesets.json`; 81 maps included):

| Sheet (tileset ID) | Size | Covers |
|---|---|---|
| `Sheridan_2` (37, 40, 41), `SheridanInside` (38) | 256×7072, ×1760 | Timber village, steep roofs, bridges, cliffs, arena; wooden interiors |
| `GearenCity Real` (1) | 256×16000 | City blocks, apartments, scaffolding, grand museum facade, port, trucks |
| `Route 2_new` (39), `Route 2_1` (7, 11), `Route 3` (8) | up to 256×10000 | Routes, forest, fields, ruined village |
| `Goldenleaf Forrest` (15, 23) | 256×9000 | Autumn forest town, haunted tower |
| `Amethyst Cave` (20), `Amethyst Grotto` (21), `Goldenwood Cave` (13), `CorruptedCave` (4) | up to 256×8000 | Crystal caves, corrupted cave with lava: Cragholm, Bleed zones |
| `Carotos Mountain` (12) | 256×2800 | Mountain, conveyors |
| `Chrisola Hotel` (3), `RoseTheatre` (36), `Help Centers` (29) | up to 256×6100 | Mansion and hotel interiors, theatre (Pell Playhouse), Pokémon Center |
| `Rejuvenation Integration/…/Aelita_rift_2` | 256×9088 | Rift area |

**Missing from that repo:** 36 of the 38 autotiles those tilesets name (only `BurntGrassSheridan`, `DirtDark` are
present). Renders therefore show black where Gearen's streets and some ground should be. To use these sheets, map each
missing autotile slot to a Tectonic autotile (`water2`, `Sea`, `Waterfall*`, `Road`, `Dirt`, `Light grass`, `Sand`) at
import. The terrain tags are Rejuvenation's own and need a check before trusting them. No castle, desert, ice or
sci-fi sheets are in this set; those still come from Tectonic and custom work.

Renders: `/home/claude/ref/art/renders/rejuv_wll_{002 Gearen, 038 Sheridan, 056 Route 2, 023, 043, 014}.png`
(render with `PRISMFALL_GFX=/home/claude/ref/art/_gfx_wll`). Reference only: Rejuvenation forbids copying its maps.

**Search log (this sandbox).**
- Third pass (2026-11-17, internet on): Eevee Expo's 348 Graphics resources and 100 game-jam packs listed by downloads;
  34 DeviantArt tile artists' galleries via RSS; DeviantArt keyword searches; itch.io. Reachable: Eevee Expo, DeviantArt
  (full-size images via oEmbed), MEGA file links, Google Drive, Dropbox, catbox, Pokémon Showdown. Blocked or gone:
  Relic Castle (placeholder page), PokéCommunity and The Spriters Resource (Cloudflare 403), MediaFire, Bulbagarden
  Archives (403), GitHub search (login). Results: Tier C above and NEW_SOURCES.md.
- Only `git clone` from github.com works. The GitHub API (`gh search`, `gh release`), codeload zips and raw files
  return 403. archive.org, itch.io, gamejolt, mediafire, mega, gitlab, deviantart, eeveeexpo and rebornevo.com all fail
  with "CONNECT tunnel failed, response 403" (one HEAD each).
- Second pass, 30 more repos probed by clone: hits are sources 3–7 above. Empty or stock-only: ten Essentials forks,
  `Dzitars/PkmnFanGame`, `Ethanol-Rouxy/PokEMT`, `omanoloneto/pokemon-essentials-enhanced-v20.1`,
  `kurayamiblackheart/kurayshinyrevamp` (same tiles as `pif`), Añil release repos (one README each), three Uranium
  repos, `ChimeraGaming/FanmakePokemonMaps_Android`, `Concave-World/mapmaking` (Gather.town art, wrong style).
- First pass, by web search plus clone: `Waynolt/SWM-modular-modpack` (scripts only), `fuyukai/reborn-rebalance`,
  `birblett/RemiX` (no graphics), `aleksjovcic/pokemon-alpine`, `starrcasm/pokemon-essentials-sesk`, three Essentials
  forks (stock tiles or none), `Aiwyn17/pokemon` (stock tiles plus 5 custom sub-tilesets, not examined),
  `espparki1/PokemonValhalla` (wrong style). No Reborn or Desolation graphics found anywhere on GitHub.

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

**Stock-tile check.** Tectonic's sheet still carries some stock Essentials pieces. `tools/gen3_vet.py` lists tiles that
share exact colours with the stock sheets (1683 of 7701, many false positives). It is a helper for spotting stock pieces,
not a blocker: judge by eye.

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
- `/home/claude/ref/art/_probe/*`: blobless probes from the search above; nothing usable.

### 2.4 Obtained (was: not reachable)
With internet access enabled, the three games came from their official pages: Reborn as a direct rebornevo.com zip,
Rejuvenation and Desolation from the official MEGA links (fetched with `/home/claude/ref/art/tools/mega_dl.py`).
MediaFire mirrors still return 403 and were not needed. Sources used:
- Reborn: `https://www.rebornevo.com/pr/download/` → `https://www.rebornevo.com/downloads/rebornremote/Reborn_19.5/Reborn-19.5.0-windows.zip` (656 MB)
- Rejuvenation: `https://www.rebornevo.com/rejuvdown/` → MEGA `Rejuvenation-14.0-windows.zip` (2.1 GB)
- Desolation: `https://www.rebornevo.com/deso/desodownloads/` → MEGA `Pokemon Desolation.zip` (841 MB)

Rejuvenation's published asset rules: credit the Rejuvenation Team; **maps may not be copied**. Treat the games' maps as
references only, and take tiles and stamps from them.

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
| **Rejuvenation-style steep-roof timber townhouses** | Now available: `Sheridan_2` in `wll` (§2.0). Recolour roofs per realm. |
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

## 7. Character portraits (Rev 7)
Rejuvenation-style round portraits with expressions in the speech bubble.
- **Spec.** 96×96 PNG (48×48 art doubled), transparent outside the disc; 2-px ring in the realm cloth colour (§4);
  head and shoulders, facing three-quarters toward the text. File `Graphics/Pictures/Portraits/<CHARACTER>_<expr>.png`.
  Expressions for main cast: `neutral, happy, angry, sad, surprised, hurt`; minor NPCs: `neutral` only.
- **Placeholders from trainer sprites.** Crop the top square of the trainer front sprite (`Graphics/Trainers/*.png`,
  128×128), mask to a disc, add the ring. Prototype looked at: `/home/claude/ref/art/custom/_preview_portraits.png`;
  it reads fine as a placeholder. Expressions need hand edits of eyes and mouth (a few pixels each).
- **Obtainable resources.** Pokémon portraits with emotion sets: `github.com/PMDCollab/SpriteCollab` (exists, clonable,
  not cloned; 40×40 PMD style, credit per its credits file). No trainer mugshot pack is on GitHub; the `wll` repo has
  only two Rejuvenation portrait pictures.

## 8. Credits
Artist credits and usage terms are in `/home/claude/fangame/docs/CREDITS.md`. Tectonic's repo is CC BY-NC-SA 4.0, so
our derived tiles carry the same terms.
