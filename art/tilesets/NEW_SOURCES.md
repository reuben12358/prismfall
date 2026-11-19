> **PORTRAITS:** see `/home/claude/fangame/art/PORTRAIT_SOURCES.md` (2026-11-19). Short version: the 360 VS busts in
> `ref/games/{rejuvenation,reborn,desolation}/Graphics/Transitions/vs*.png` are x2 and in the target style; a 96×96
> crop at 1:1 is a dialogue face. Boards in `/home/claude/ref/art/renders/portraits/`.

# New art sources (hunt of 2026-11-17)

All downloads are **untrusted data**: images only (archives deleted after extraction), never run anything in them.
Every folder has a `_sources.tsv` or `_source.tsv` (origin URL, artist, terms). Preview boards for everything below:
`/home/claude/ref/art/renders/new_sources/` (`sprites_*.png` for characters, `<artist>.png` for tiles).

**Pixel density key.** `x2` = 16-px-grid art already doubled (every 2×2 block one colour), the same density as
Rejuvenation, Reborn, Desolation, Tectonic and our PF sheets. `16` = 16-px art at 1× (double it with nearest-neighbour
on import). `1x` (sprites) = native size, double for Essentials. `hi` = drawn at 32 px with 1-px detail: finer than
our maps. Keep `hi` art in its own map family, or halve-then-double it (tested on PeekyChew's castle and TerribleJared's
harbour, boards `halve_double_test_*.png`: buildings still read, but small text and window mullions need a touch-up).

---

## TRAINER SPRITES (for the sprite artist: kitbash bases, read this first)

Battle fronts in Essentials are 160×160 (80-px art doubled). All `x2` sets below drop straight in. Showdown's are 1×:
double them first.

| # | Path | Count | Size | Style | Density | Terms | Best use |
|---|---|---|---|---|---|---|---|
| T1 | `/home/claude/ref/art/sprites_showdown/trainers/` (+ `credits.tsv`, file → artist for 850 files) | 1500 | 80×80 | **Gen 5 battle-sprite style throughout.** ~317 official BW/B2W2 fronts (plain names) and 62 DPPt/HGSS fronts (`-gen4`, `-gen4dp`); 619 by **kyledove**; 185 **Masters-style** (`*-masters*`, flashy outfits, capes, dynamic poses); 12 Pokémon Conquest (`-conquest`); Gen 6–9 classes redrawn in BW style (`-gen6`…`-gen9`). Skip `-gen1/2/3` (off-style). | 1x | Credit the artist in `credits.tsv` (kyledove, Brumirage, Beliot419, ZacWeavile, Gnomowladny, Horo, Grapo…); official ones © Nintendo/Game Freak | **The main kitbash library**: heads, hair, coats, capes, poses. Masters set for Wardens and royals. Board: `sprites_showdown_masters.png`, `sprites_showdown_kyledove.png`, `sprites_showdown_gen4.png` |
| T2 | `/home/claude/ref/art/sprites_kyledove_xy/sprites/`, `…_oras/sprites/`, `…_swsh/sprites/` | 50 + 50 + 37 | 160×160 | kyledove's BW-style remakes of XY, ORAS and SWSH trainer classes (Butler, Maid, Hex Maniac, Furisode Girls, Rangers, Punks, Psychic, Chef, Artist…) | x2 | Credit kyledove | Ready-sized bodies with strong silhouettes; Essentials file names. Boards: `sprites_kyledove_xy.png`, `sprites_kyledove_oras_swsh.png` |
| T3 | `/home/claude/ref/art/sprites_muffyang/extracted/` | 64 | 160×160 | Hand edits of official sprites: Dragon Rider, Fire Breather, Snow Ninja M/F, Winter-camo Rangers, Snowboarder, Witches, Punk, Construction Workers, Gamblers, Gyaru | x2 | No credit required (we credit Muffyang anyway) | Isenmar (winter classes), Ashkaar (Dragon Rider, Fire Breather), Nadir (Punk, Gambler). Board: `sprites_muffyang.png` |
| T4 | `/home/claude/ref/art/sprites_gen5_vs_tech/extracted/` | 49 busts + 5 bars | 256×128 | **Official B2W2 VS busts**: expressive half-body cut-ins (Grimsley, Caitlin, Shauntal, Colress, Ghetsis, N, Iris, Skyla, Elesa, Drayden…) | x2 | Official art; pack by TechSkylander151 | **Best bases for Rejuvenation-style speech portraits**: crop to 96×96 and add the ring. Board: `sprites_gen5_vs_busts.png` |
| T5 | `/home/claude/ref/art/sprites_pt_vs_tech/extracted/` | 25 | 192×128, 512×128 | Official Platinum VS busts and bars | x2 | Official; pack by TechSkylander151 | Gen 4 bust bases |
| T6 | `/home/claude/ref/art/sprites_chakra_clinic/extracted/` | 218 (191 at 160×160) | 160×160, 80×80 | Chakra Clinic jam pack: each character in 3–7 **expression and pose variants** (smug, shocked, crying…) plus some Pokémon | x2 | Free to use (TechSkylander151) | How to vary one body across expressions. Board: `sprites_chakra_clinic_expressions.png` |
| T7 | `/home/claude/ref/art/sprites_jinxed_pbr/extracted/Colosseum Leaders/` | 12 | 160×160 | jinxed's BW-style Battle Revolution colosseum leaders (bold costumes, normal and shiny palettes) | x2 | Credit jinxed | Costume-heavy leader designs |
| T8 | `/home/claude/ref/art/sprites_gen4_partner_backs/extracted/` | 6 strips | 800×160 | HGSS-style partner back-sprite strips (Barry, Buck, Cheryl…) | x2 | Credit Sylvecario | Back-sprite bases for partner battles |
| T9 | `/home/claude/ref/art/sprites_wergan/` | 316 | 256×256 (4×4 walk sheet) | **Overworld charsets** for trainer classes and characters from every region (Kanto to Paldea, Horizons, Let's Go) in HGSS/BW overworld style | x2 | No terms stated on the posts: credit Wergan, ask before shipping | Overworld kitbash library (heads, hair, outfits at OW scale). Board: `sprites_wergan_ow_sample.png` |
| T10 | `/home/claude/ref/art/sprites_gen4_ow_vanillasunshine/extracted/` | 234 | 256×256 | Every official Gen 4 overworld (+ a few custom) | x2 | Official; credit VanillaSunshine | OW bases, Gen 4 look. Board: `sprites_gen4_ow.png` |
| T11 | `/home/claude/ref/art/sprites_gen5_ow_radicalraptr/extracted/` | 133 | 240×256 | Official BW overworlds formatted for RMXP | x2 | Official; credit Radical Raptr | OW bases, Gen 5 look. Board: `sprites_gen5_ow.png` |
| T12 | `/home/claude/ref/art/sprites_salyadarken_ocs/extracted/` | 6 | mixed | Three OCs, front + OW | mixed | Credit SalyaDarken | Low quality; reference only |

**Already on disk (no download needed), the style target itself:**
- Rejuvenation custom trainers: `/home/claude/ref/games/rejuvenation/Graphics/Characters/trainer*.png`, 357 at 180×180
  (90-px art, x2). Board: `sprites_rejuvenation_trainers.png`. Reborn: `…/reborn/Graphics/Characters/trainer*.png`, 297 at
  160×160. Desolation: `…/desolation/Graphics/Characters/trainer*.png`, 179. Study only (their characters are theirs).
- Portrait busts: Desolation `…/desolation/Graphics/Faces/` (90, 96×96, x2; board `sprites_desolation_faces.png`),
  Rejuvenation `…/rejuvenation/Graphics/Faces/` (13). Base project trainers: `/home/claude/ref/ebdx/Graphics/Trainers/` (72 at 128×128).

**Portrait gap.** No free bust pack in the Rejuvenation/Desolation style was found. The B2W2 VS busts (T4) and Platinum
VS busts (T5) are the best bases. Pokémon Conquest portraits and the Fire-Type Emblem faces are only on blocked hosts.
PMD portraits (Pokémon, not people): `github.com/PMDCollab/SpriteCollab` (not cloned).

---

## TILESETS (for the map builder)

Ranked by value to Prismfall. "Gap" names the ART_DIRECTION priority each one closes.

### C1. TerribleJared (DeviantArt, 2026 uploads): harbour, ships, undercity, graveyard, desert, dragon culture
`/home/claude/ref/assets/da_terriblejared/` · density `hi` (32-px native, 1-px detail) · free and public, credit TerribleJared.
Board: `renders/new_sources/terriblejared.png`. Muted, cohesive Gen 4/5 palette; his Newport map shows the look in use.
| File | Best pieces | Gap |
|---|---|---|
| `Big Boats_ Small Boats_ Ferry_ Yacht_ and more.png` (640×6400) | Cargo ships with cranes, ferries, tugs, patrol boats, yachts, fishing boats, sailboats, rowboats | **Harbour and ships** (Ferrow's Landing, Saltmere, Ebbmouth, Skaldfast) |
| `Quay and Harbor Stuff.png` | Lighthouse, Fat Angler shop, warehouse, fish crates, buoys, nets, catamarans, chain-link | Harbour |
| `Sewer Tileset.png` (256×2048) | Brick sewer walls and arches, green sump water, rusted shanties, shipping containers, tyre walls, machines, mushrooms, Sump-Rat flag | **Undercity / sewer / slum** (Underveil, Sump Docks) |
| `Graveyard and Mausoleum Tileset.png` | Gravestones, gargoyles, mausoleums, dead lamps, skeleton, gothic brick house, mossy floor | Gravenmoor, Thorn Crypts, Necropolis |
| `Desert Town _w_ Gym and Pokemon Center_.png` | Adobe houses with awnings, crescent-domed palace, cacti, palms, oasis, bone fountain | **Desert canyon city** (Duneholt bazaar) |
| `_Tiles_ Dragon Keepers Mini Pack.png`, `…_of the north_….png` | Sandstone and blue-tarp dragon-keeper houses, dragon statues, nests on columns, arches, incubators, banners | **Ashkaar** (Dragon Roosts, Wyrmrest), Ossaria |
| `Stantler Sleighs and Some Snowy Stuff.png` | Sleighs, snowy pines, igloo, snowed cottage | Isenmar sled roads |
| `Machines and Power Plant Stuff.png`, `City Transportation _underground subway platform_.png` | Generators, pipes; subway platform | Cogsworth, Nadir |
| `Swamp Stuff.png`, `Campground….png`, `Log Cabin style Buildings.png`, `Ruin Maniac Stuff.png`, `Mixed Forest Trees.png` | Swamp props, tents, cabins, dig-site props | Mirefen, Dig Lab |

### C2. WesleyFG's DPPt Tileset (Eevee Expo 295): DPPt landmark buildings, RMXP-ready
`/home/claude/ref/assets/ee_wesleyfg_dppt/sheets/Wesley-FG-DPPt.png` (256×26752, 8 columns) · density `x2` (matches our
maps) · credit WesleyFG. Board: `wesleyfg_dppt_overview.png`; crop `wesleyfg_dppt_cathedral_crop.png`.
Best: the **Pokémon League hall with four red spires** (~y 24600–25300: recolour for the Basilica of First Light or the
Hollow Cathedral), Canalave-style library mansion, Sunyshore glass towers, Veilstone store, domed contest hall,
Galactic-style HQ, stadium, **ferries, yachts, crane, lighthouses**, fountains, rock statue. Gaps: cathedral (partial),
city blocks, harbour.

### C3. PkmnAlexandrite (DeviantArt): civic landmarks
`/home/claude/ref/assets/da_pkmnalexandrite/` · density: Cathedral `x2`, the rest `16` · non-commercial, credit
PkmnAlexandrite (edits of Magiscarf, WesleyFG, Zeo254, Rata, Red-eX, SailorVicious tiles). Board: `pkmnalexandrite.png`.
Best: `Cathedral Tile.png` (domed civic cathedral with clock), `Clock Tower Tile.png` (Zenith, Cogsworth), `Town Hall
Tile.png` (blue mansard **guildhall**), `Bank Tile.png`, `Library Tile.png` (Athenaeum), `Neocity Tiles.png` (glass hotel,
hospital, mall, planetarium: **Zenith**), `Hotel Tile.png`, `City Decorations Tiles.png`, `Food Trucks Tiles.png` (markets),
`Residential Building Tiles.png`. Skip `Fairy Tail Guild Building Tile.png` (another franchise's logo). Gaps: guildhalls, city blocks.

### C4. Magiscarf extra sheets (DeviantArt): frozen forests, white-stone castle pieces
`/home/claude/ref/assets/da_magiscarf/` · density `16` · non-commercial, free to edit. Board: `magiscarf.png`.
Best: `Bunch o_ free tiles.png` (**snow-capped trees in six colours** for the Rimewood, white-stone castle towers, bridges
and arches, Victorian mansion, pink townhouses), `_Free_ New Tiles Mastersheet.png` (four-season trees, grey castle towers
and bridges, modular houses), `Snow and Stone.png` (stone townhouses with snowy window boxes: Rimeholt, Crownhaven),
`City Tiles.png`, `Buildings Tiles w_ Snow.png` (snowed shops), `Crystal Caves Tiles.png` (light sandy crystal cave),
`Art Deco Building.png`.
**Credit fix:** morgebby's unnamed sheets are Magiscarf's: `dbf3bkq` = "Tileset ver.3 [Free*]", `ddpuooa` = "Revamped
Tiles", `ddejpun` = "Fields Backgrounds" (checked against DeviantArt's IDs). Both say non-commercial use only.

### C5. PeekyChew (DeviantArt): castle, snow, desert, lava
`/home/claude/ref/assets/da_peekychew/` · density: castle `hi`, dumps `16` · free to use and edit; contact the artist
for commercial use; credit PeekyChew and the artists named on each post. Board: `peekychew.png`.
Best: `Medieval Castle.png` (**full Bodiam-style castle**: curtain wall, six towers, gatehouse, keep, courtyard: a
kingdom-seat stamp; halve-then-double test: `halve_double_test_peekychew_castle.png`), `Public Tileset Dump 1_4 - Snow.png` (snowy pines, ice,
fences), `…2_4 - Desert.png`, `…3_4 - Beach and Sea.png`, `Lava and Cave Tileset.png` (lava autotile frames, cave
variants), `Animated Lava Tiles.gif`, `Cafe_ Restaurant and Bar Tiles.png` (interiors), `Platinum Gatehouse Tiles.png`,
`Stone Slab Tiles.png`, `Winter Retreat.png` (map, reference).

### C6. Phyromatical "December of Tilesets" (DeviantArt): mirror world, drowned temple, ice caves
`/home/claude/ref/assets/da_phyromatical/` · density mixed (`16` and `hi`) · credit Phyromatical and the artists named
on each post (Bridgeton's buildings are The-Red-eX's). Board: `phyromatical.png`.
Best: `DoT Day21 - Distortion World Remake Tiles.png` (**floating islands, distortion trees: Antumbra**), `DoT Day18 -
Dark Ruins tileset.png`, `DoT Day4 - Water Dungeon Tileset.png` (**drowned Aurelia**), `DoT Day22 - Deep Ice Cave.png`,
`DoT Day17 - Evolina Ice Cave.png`, `Tons of Tileset 8_10 - Ice Floe Tileset.png`, `DoT Day6 - Bridgeton Tileset.png`
(slate-roof half-timber houses, close to Rejuvenation), `Heaven Realm Tileset _XY-Styled_.png` (cloud islands, gold
rails: Skyreach), `DoT Day23 - Alternate Volcano Tiles.png`, `Volcano Cave _ Tileset-Test _2.png` (map, reference).

### C7. UltimoSpriter BW tiles (DeviantArt): dark towers and industry
`/home/claude/ref/assets/da_ultimospriter/` · density `16` · public, credit UltimoSpriter. Board: `snow_crystal_industrial.png`.
Best: `Black City Tiles.png` (black glass towers: **Zenith by night, Nadir**), `Virbank City Tileset.png` (pipes,
warehouses, lock gates: Cogsworth, Sump Docks), `Cold Storage Tileset.png` (cranes, containers: harbours), `Driftveil
City Tileset.png`, `Misc B_W Tiles - Seasons Edit.png`, `Starter Kit Tileset.png`, `Random Interiors Tileset.png`.

### C8. Pokémon Gaia tileset, compiled (Eevee Expo 1377)
`/home/claude/ref/assets/ee_gaia_compiled/sheets/` (`GaiaCompiled.png` 256×8192 + 10 city/road autotiles) · `x2`,
RMXP-ready · credit zetavares852 and the Gaia credit list. Board: `gaia_overview.png`. Bright modern Gen 4 city:
apartment blocks, glass offices, domed hall, small cathedral, arches. Lumen City districts.

### C9. Smaller fills
| Source | Path | Density | Best pieces | Gap | Terms |
|---|---|---|---|---|---|
| carchagui | `assets/da_carchagui/` | `16` | `Snow village tiles.png`: snowed chalets with fairy lights, Pokémon Center and Mart chalets | Frostwick, Snowbriar | Credit |
| J-Treecko252 | `assets/da_j-treecko252/Crystal Tiles.png` | `x2` | Crystal clusters in eight colours | **Crystal caves**, Glassed land | Credit |
| aveontrainer | `assets/da_aveontrainer/` | `16` | `Sewer Tileset.png`, `Airport.png` (terminal: Skyport), `Hospital Tileset.png`, `Fisherman_s Hut Tileset.png`, `Desert House.png` | Undercity, airship port | Non-commercial; credit (+ Magiscarf, Kyle Dove, Kane89) |
| princess-phoenix | `assets/da_princess-phoenix/` | `16` | `Fossil Museum Tileset.png` (Dig Lab, Mural Gallery), `Pokeball Factory Tileset.png` (Strade Works), `Swampy Gatehouse Tileset.png` | Ossaria interiors, Cogsworth | Credit |
| Akizakura16 | `assets/da_akizakura16/` | `x2` | `4th gen Indoor Tileset.png` (256×17056), `4th gen Outdoor Tileset.png` | Interiors | Non-commercial only, **no Patreon/donations**, no redistribution |
| moca Public Gen 4 | `assets/ee_moca_public_gen4/extracted/Gen 4 Pack/` | `x2` | Stone ruins, cliffs, houses + 6 autotiles | General | Credit list in `_source.tsv` |
| SirMalo HGSS | `assets/ee_sirmalo_hgss/sheets/` | `16` | Every HGSS building (S.S. Aqua, Ecruteak towers, Olivine lighthouse, Goldenrod) on wide sheets: recut | Harbour, pagodas | Official rips |
| ChaoticCherryCake | `assets/da_chaoticcherrycake/` | mixed | `Pokemon Tileset From Public Tiles 32x32.png` (256×20832 compilation), indoor sheet, `_Free_ Tileset v0.1.8.png` | General | Non-commercial, credit |
| KingTapir | `assets/da_kingtapir/` | `16` | Desert Deluxe and Sandstream (cliffs, quicksand pits, oases), Tower of Darkness/Waters | Ossaria routes | Credit |
| Hek-el-grande | `assets/da_hek-el-grande/` | `16` | `Volcanic tiles.png`; `BIIIG tileset.png` (**not the tower**, it is private) | Volcanic | Credit |
| Kyle Dove | `assets/da_kyle-dove/` | mixed | `DP tiles for public.png`, `Biome Tiles Public.png` (**not the red lava panel**, private), `NEW Undersea Tiles_.png` (underwater mockup) | Underwater, biomes | Credit Kyle Dove + Speedialga |
| Rayquaza-dot | `assets/da_rayquaza-dot/` | `16` | Platinum-style magma autotile | Volcanic | Credit |
| The-Red-eX, WesleyFG | `assets/da_the-red-ex/`, `assets/da_wesleyfg/` | `16` | Public tilesets; WesleyFG city maps (reference) | General | Credit |

### Dropped or blocked
- **Off-style or weak:** figyberries exterior (chunky, not Pokémon style), alexvond HGSS dump (8 buildings), CoreBear
  (no tiles), ORAS/XY EBDX battlebacks (blurry 3D renders), Orre battlebacks (flat and bland), Elinthind crystal cave
  (Gen 3 look), Ekat99 extras (Emerald scale; her main pack is in morgebby), KingTapir Gateon/Agate/Galar sheets,
  Rayquaza-dot maps (watermarked), itch.io Pokémon-tagged packs (GB-style or AI-generated).
- **Private or permission-only:** The-Red-eX's Pokémon Dawn tiles, aveontrainer's Church, Phyromatical's Lava Cavern
  (commission), Hek's tower and two Hek sheets, DirtyWiggles' sheets (ask first), chimcharsfireworkd's BW Citrine
  (no permission stated). All deleted.
- **Unreachable:** Relic Castle is gone (placeholder page). PokéCommunity and The Spriters Resource answer with a
  Cloudflare challenge (403). MediaFire is blocked (KingTapir's ready-to-use sets, Scizor's sewer, the Ultimate Gen 4/5
  OW packs, Taiga's trainers, Lucas and Dawn, ORAS Hoenn leaders, HGSS VS pack, most game-jam packs, Fire-Type Emblem
  faces). Dead MEGA links: CinnaYva Distortion World, doof HGSS trainers. Eevee Expo attachments need a login.
  GitHub search needs a login.

### Still missing
Grand interiors (throne room, great hall, cathedral nave), airships, a true mirror/glass world, a dragon citadel,
obsidian glass-desert, neon signage, and Rejuvenation-style portrait busts. These stay custom work (ART_DIRECTION §5),
built from the pieces above.
