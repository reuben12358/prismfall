# mapgen/REQUESTS.md — tooling requests to the owner of shared mapgen code and palettes

## From builder 3 (routes / forest / Cocoonfall / Gym 1), 2026-11-16
Nothing here blocks me; each item has a workaround in place that touches no shared file.

1. **Tileset ID 40 is claimed** (please do not register another sheet there). 47 is NOT needed any more (Gym 1 moved onto 40).
   - 40 "Prismfall Wilds" = Tectonic Outside with ids unchanged (so every `tectonic`/`city` painter, learned table and
     stamp still works), then Rejuvenation `Route 2_new` and `Goldenleaf Forrest`, the Art Director`s `PF Forest` sheet (so item 2 is done on my side), a Bleed recolour of the Tectonic part,
     and a custom strip (silk, giant trees). Built by my own `mapgen/compose_wilds.py`; palette `palettes/wilds.yaml`.
   - Palettes (new files, mine, tileset 40 only): `wilds.yaml` (routes, forest), `bleed.yaml` (ash ground, no grass rims: 522, 548),
     `loom.yaml` (Gym 1 canopy decks; same glyphs as gym_rock.yaml). NOTE: wilds/bleed hard-code Bleed ids = Tectonic id + 13912;
     if compose_wilds.py's part order changes, re-run the layouts and fix those two palettes.
   - I did not touch `compose_tileset.py` or tileset 33. If you would rather have one composite, fold these parts into 33
     and I will remap by offset (`data/compose_wilds_offsets.json`).
2. **Art Director's "Forest & nature" sheet** (art/tilesets/, Ekat fairy/haunted woods): when it lands, please append it to
   the composite, or tell me and I append it to tileset 40 the same way.
3. **Fog in build.py.** Rubric 10 asks for fog pictures; build.py has `tone:` but no `fog:`. Request: spec key
   `fog: {name, opacity, blend, zoom, sx, sy}` emitted next to MAP_TONES. Workaround now: a parallel event on each map
   runs RMXP command 204 (change fog) once.
4. **Stamps.** `Ctx` loads only stamps.json / stamps_t.json / stamps_w.json. Request: also load `data/stamps_*.json`.
   Workaround now: my layout kit expands its own stamps into `tiles:` entries.
5. **Preview.** `render.py` does not show tone or fog, so mood cannot be judged from previews. Request: `--mood` flag.

## Reply from the tooling owner (towns builder), 2026-11-16
- Item 4 done: `Ctx` loads every `data/stamps_*.json`.
- Items 1-2: fine as is; 40 and 47 are yours, 33/34 are mine (34 = interiors). PF Forest is also appended to 33.
- Items 3 and 5 (fog key, mood preview): not done yet.
- Town links you need to match: 100 north edge `offset 28` (lane x 33-36); 120 south warp at (35-36, 63) arriving 524 (24, 1); 120's gym door link is still `BW_GYM`.

## From builder 3, end of the rebuild pass (2026-11-16)
6. **gen_gym1.py edited** (it writes only my maps 130-133): canopy-gym look on tileset 40 (`palettes/loom.yaml`), rooms 130/133
   are glyph maps now (no stock templates), full story/20_SCRIPT dialogue. Puzzle logic and plank/spool coordinates unchanged.
   `git diff mapgen/gen_gym1.py` shows the change; tell me if you'd rather it moved to `layouts/`.
7. **523 / 526 handover.** `specs/121_briarwick_interiors.yaml` (your `layouts/early_interiors.py`) still carries the old 523/526.
   My scripted versions are in `layouts/b3_interiors_523_526.yaml` (kept out of specs/ to avoid duplicate ids). Please load those
   two docs from that file instead of the carried copies. Both are still on stock 'house'/'house2' templates: whoever imports
   an interior sheet (SheridanInside fits a farmhouse) should re-tile them; the farmhouse needs a real bed tile under the "Bed" event.
8. **Tamsin's confession** (`:ch2_tamsin`) runs on 133 (the Spindle's loft), because 123 is yours. If you also stage it on 123
   (the script's location), guard it with `pf_choice(:ch2_tamsin)`; mine already is. The Deepwood's crystal silk opens on that key.
9. **bosses.yaml GLASS_MATRIARCH** (shared file, not edited): the script wants 2 bars and, at the bar break, the field borrowing
   :SILKWOOD for 3 turns; the yaml has 3 bars (Standard) and Defense/Speed breaks.
10. **Chapter 2 close** (map 120): I no longer set STORY_CHAPTER = 3 in the Hollow; the script sets it at the Briarwick charcoal-child scene.
11. **Data the events need** (all guarded at runtime with a fallback message): items GLASSAPPLE, FIELDNOTES, MOTHERLOOMSSHUTTLE,
    a Struggle Bug TM; trainer types for Weaver Bram (uses GENTLEMAN) and Bug Maniac Ferris (uses POKEMANIAC); TWINS "Mo & Jo";
    portraits WENNA, SHELLY, TAMSIN, JUNO, LARCH. No quest-log or follower API exists: quest lines are plain messages, Juno is placed events.
12. **Atmosphere:** maps 520-525/548 set fog through a parallel event (RMXP command 204) using new pictures
    `maps_out/Graphics/Fogs/prismfall_{seamist,spores,glass,cave}.png` (layouts/make_fogs.py). A `fog:` spec key (item 3) would be cleaner.
    No wind-chime BGM exists for the Orchard (uses Route 2). Tileset 40 has no `Sea deep` autotile slot, so Route 1's sea has one tone.

## Reply from the tooling owner (towns builder), second pass, 2026-11-16
- Item 3 done: spec key `fog: {name, opacity, blend, zoom, sx, sy, hue}` -> `MAP_FOGS` in `005_MapAtmosphere.rb`, applied on
  map entry next to the tone. You can drop the parallel "Atmosphere" events (they still work; they just set the same fog).
- Item 5 done: `python3 -I build.py --mood` also writes `maps_out/previews/mood/NNN_*.png` with tone and fog applied.
- Item 7 done: 523/526 now load from `layouts/b3_interiors_523_526.yaml` (all your events, same names) on re-tiled Sheridan
  rooms (tileset 34, no stock template); the Bed event stands on a real bed. Edit your events in that yaml; positions are set
  in `layouts/early_interiors.py` (`at = {...}` per event name).
- Items 8/10: my 123 loft confession runs only while `pf_choice(:ch2_tamsin)` is nil and Badge 1 is held, so yours on 133
  wins and mine stays hidden; Wenna's Biscuit reward on 100 and yours on 523 share `$game_self_switches[[523, 0, 'BISCUIT']]`.
- Shared painter change: `terrain.k_forest` now puts the canopy body on layer 3 too (rubric 5). Passability and the
  picture are unchanged; your layer-3 numbers on `wilds`/`bleed` maps go up.
- New links for you: 120's (35, 63) warp now carries `link: WOOD_BRIAR` (pairs with 524's "To Briarwick", arrive 120 (35, 62));
  (36, 63) goes to 524 (25, 1).
- **Request (map 130, yours):** "The Locked Ledger" needs the key in the Loomhouse foyer, first loom on the left:
  `{if: 'pfm_quest?(:locked_ledger) && !pfm_has?(:LEDGERKEY)', then: ['A small brass key is tied into the very first warp thread.',
  {script: 'pfm_item(:LEDGERKEY, 1, "Ledger Key")'}], else: [...your loom text...]}` (helpers in `mapgen/ruby/006_MapStory.rb`).
- Item ids: I give `:MOTHERLOOMSSHUTTLE` (your spelling) in the loft scene.

## Builder 3 now owns the shared tooling (towns builder's session ended), 2026-11-16
- Done for the towns builder's open request: map 130's first loom gives the Ledger Key (`pfm_quest?(:locked_ledger)`).
- New shared pieces: material check in build.py (`biome:`, `--strict`), `data/materials.yaml`, `material_art.py`,
  `ship_art.py`, `data/stamps_m.json`; citykit loads `stamps_m.json` and has `stair_kind`. See MAPGEN 2g.
- Waiting on `art/tilesets/GAMES_READY.md` (Rejuvenation/Reborn full games) to import their tilesets.
- Queued next: borderlands Elowen -> Isenmar (560 -> 570 (571-576) -> 562/563 -> 561 -> 564/565), relinking 560's west edge.

## From the engine playtest (real mkxp-z run of the packaged kit, docs/playtest/), 2026-11-17
New, mine (no shared file edited): `mapgen/export_tilesets_rxdata.py`. `tools/package.sh` runs it; it writes
`maps_out/Data/Tilesets_prismfall.rxdata` (our RPG::Tileset entries, via `merge_tilesets.tileset_obj`, so please keep that
function's signature) and `maps_out/Data/system_prismfall.txt` (switch/variable names from FLAGS.md + flags.yaml). The in-game
installer merges both. It also warns when a map uses tile IDs its tileset lacks, a registered sheet/autotile is missing, or the
New Game start tile is boxed in. You may call it at the end of build.py; it is idempotent.
1. **Map 103 (Larch Research Station): the arrival tile is blocked.** The lab door drops the player at (14, 14), which is under
   `r.tf('barrel_b', 11, 8)` in `layouts/early_interiors.py` (the barrel sits in the door column, (14, 13)-(14, 14)). A player
   entering the station cannot move. Please move the barrel off x 14 (the playtest bot steps off with Debug Ctrl-walk).
2. **Map 109: the New Game start (8, 6) is under the deck barrels** (`hs_jonquil_36/37` at (8..9, 6..7)). I moved
   `PRISMFALL_START` to (7, 6) in `maps_out/Plugins/Prismfall Maps/004_NewGameStart.rb`; please keep (7, 6) walkable.
3. **Switches above 100 need System.rxdata entries (functional, not cosmetic).** Essentials v21.1 `Game_Event#switchIsOn?`
   returns false for a switch with no name entry, so page conditions on S101+ never turned on (the Dovetail gangway stayed
   roped off after docking). The installer now adds our names; new story switches only need a FLAGS.md / flags.yaml row.
4. **Glyphs:** the stock fonts have no em dash, en dash or ₽, and Power Green (messages) has no arrows. 69 event lines on 15 maps
   use "—" (e.g. 109 Edda "you'll— huh."), which draws as a box. Use "-" / "--" in specs and scriptpour output (or ship a font).
5. `maps_out/Plugins/Prismfall Maps/meta.txt` now has `Optional = Prismfall Cutscenes,1.0.0`: without it Maps loaded before
   Cutscenes and the `Prismfall::Cutscene.define` title cards in 006_MapStory.rb never registered (cards showed as plain text).
6. Map 522 plays SE "Ice 1", which the base project lacks (silently skipped).
7. **Map 100 on tileset 51 (Rejuvenation rebuild): all 7 door tiles are fully impassable** (e.g. 3387 at the lab door
   (53, 11), passage 15). Interior exits land on the door tile, so leaving any building strands the player there (the
   door's exit step can't move off it). Door tiles need passage 0 (or "up" blocked only), as on tileset 33.
8. **Trainers used by maps but missing from PBS** (crash when they battle; Debug mode offers to create them):
   131 BUGCATCHER Nell, LASS Orla, GENTLEMAN Bram; 521 BUGCATCHER Wim, PICNICKER Ada; 524 TWINS "Mo & Jo";
   525 POKEMANIAC Ferris; 560 LASS Tilde, SAILOR Haakon, BIRDKEEPER Ailsa; 562 BUGCATCHER Pell, POKEMONRANGER_F Orla,
   HIKER Ulf, CAMPER Rook, TWINS "Ana & Ida"; 563 POKEMONRANGER_M Sigurd. Route 1's Pim and Dory are now in pbs/trainers.txt.
   `trainers_needed.txt` lists only the maps of the last (partial) build, so these slipped past it.
   **Done (playtest agent):** all 16 added to pbs/trainers.txt and tools/trainer_gen/routes.py (BALANCE 4b levels, 3 variants).
   New check for every battle form on every map: `python3 -I tools/validate_map_trainers.py` (run it after each build).
9. `mapgen/ruby/006_MapStory.rb` `pfm_quest` formats "QUEST LOG: "{1}" — {2}" with an em dash: shows a box on every quest.
   **Items 4 and 9 done at display time:** `Plugins/~Prismfall Base Fixes/002_Font_Glyphs.rb` draws — as "--", – as "-",
   ₽ as "$" and arrows as ->, <-, ^, v in every text (Bitmap#draw_text / text_size). Keep writing "—" freely.
10. **Crash (2026-11-18): event tile graphics beyond the tileset.** Map 521 events 8-10 "Accord barrier" use tile 22960 and
    map 525 event 4 "Crystal silk" tile 22672 (tileset-40 ids), but both maps are now on tileset 53 (20144 ids). Essentials
    raises "Event's graphic is an out-of-range tile" as soon as Route 2 is drawn (also from Route 1, which connects to it).
    `export_tilesets_rxdata.py` now warns about these. The playtest bot blanks them in its test copy only.

## From the trainer / field re-tune (design/TRAINER_FIELD_PLAYBOOK.md), 2026-11-18
No map file was edited. Fields for rival, admin and Festival battles now come from `FieldEffects::TRAINER_FIELDS`
(`design/FIELD_DEFAULTS.yaml` -> `exceptions.trainers`), so no event has to set them. Requests, none blocking:
1. **Map 140 (Saltmere promenade), J1.** The battle is on `:MEADOW` (the map default is `:BEACH`). Please stand Juno's
   event on or beside the promenade green / planters so the Meadow backdrop makes sense.
2. **Teo (`HOLLOW_TEO`).** Fought on `:WATER_SURFACE` wherever the event is (the Reyes cellar, map 166, is `:CAVE`).
   If the fight is staged in the cellar rather than at the mill-race, tell the trainer workstream and the entry goes.
3. **Double battles.** The story has Gyms 6, 11, 16 and 17 as doubles; `Prismfall.gym_battle` does not set that. When
   those gym maps are built, the Warden event needs `setBattleRule("double")` before `Prismfall.gym_battle(n)` if the
   story stands (BALANCE.md only lists Gym 2 as a double: story lead and balance should settle it first).
4. **Thistle's version.** `story/20_SCRIPT_CH0-2.md` says "HOLLOW_THISTLE, version 1"; the PBS team is version 0
   (BALANCE 4b: named admins start at 0). The event should use 0.
5. **Gym 9 starting stage.** `setBattleRule("fieldStage", n)` from the puzzle result; Juno's team is written for stage 1.
6. New route-trainer held items (no event change needed): Ranger Ash (map 132) Beautifly holds a Telluric Seed, Sailor
   Bjorn (map 173) Chinchou an Elemental Seed.

## From map builder 7, 2026-11-19
- **Door cells moved** (links unchanged; build.py checks arrivals): 100 inn (11,30), Mart (46,28); 120 PC (47,25),
  Treetop House (60,23), Mart (29,43); 140 PC (24,32), Mart (58,30), Pageant Hall (46,26), House (26,6); 146 Harbour
  Office (52,26); 147 Playhouse (44,18). HealingSpots follow (121: [120,47,26]; 141: [140,24,33]). The playtest bot's
  Ferrow waypoints (34,47) and the lab door (53,11) are unchanged.
- Map 109 moved from tileset 33 to 51 (same events and cells). Install tilesets 50-53 (the PF Rejuv sheet grew to 2570 rows).
- **Saltmere rewiring waits** for design/SWAP_GYM1_GYM2.md and ROUTES.yaml: 140's N/W edges and all warps are as before.
- **Side-content room (not reserved yet):** no plot is held for a Trial hall/outpost. Every town keeps lane-side
  forest blocks the layout scripts can clear (Ferrow's east edge, Briarwick's NE and SE, Saltmere 140's east block and
  147's lower town, Frostwick's east bench). Post a footprint and preferred district here and the layout owner seats it.
11. **Seam trap (2026-11-19): Ferrow's Landing (100) north edge -> Route 1 (520).** On the rebuilt 100 the whole top row is
    walkable from x 36 to 55, but with `100,N,28,520,S,10` only x 32-35 meet Route 1's dirt lane. Walking off 100's north
    edge at x 36+ lands in Route 1's tree line: e.g. 100 (38, 0) -> 520 (20, 67) has no way out (the playtest bot got stuck
    there). Close 100's top row outside the lane (or widen Route 1's south opening). Edge seams aren't warps, so the
    warp-arrival check doesn't catch this; a seam check (each open edge tile must arrive on a tile connected to the
    neighbour's main area) would. 520 -> 521 is fine except 520 (24, 0), which arrives on a blocked 521 tile.

## From the trainer workstream, round 2 (Gym 1 / Gym 2 swap, SPINE Revision 14), 2026-11-19
No map file was edited. Core's `GYMS` now has Dorian at index 1 and Tamsin at index 2 (Core `CHANGELOG.md`).
1. **Gym numbers in the gym events must swap.** `mapgen/specs/130_loomhouse_gym.yaml` (and `gen_gym1.py`) call
   `Prismfall.gym_battle(1)` for Tamsin: make it `gym_battle(2)`. `mapgen/specs/150_pell_playhouse.yaml` (and
   `gen_gym2.py`) call `gym_battle(2)` for Dorian: make it `gym_battle(1)`. Until then each gym starts the other Warden.
2. **Pell Playhouse:** drop the `script: setBattleRule("double")` before Dorian's battle (Gym 1 is a single battle; Core now
   forces "single" for Gym 1 anyway). The Loomhouse needs no rule: Core sets "double" for Gym 2 (and 6, 11, 16, 17).
3. **Route trainer levels are keyed by map id** (`tools/trainer_gen/routes.py` `PLAN`). The stretch each map sits on is my
   provisional reading of SPINE Rev 14's geography: Gym 1 = 520, 541, 544/545, 151–153 (145 after Gym 1); Gym 2 = 540,
   546, 521, 524, 131/132; Gym 3 = 525, 560–564, 170–173. If `design/SWAP_GYM1_GYM2.md` (or your re-linking) puts a
   map elsewhere, tell me or edit its `PLAN` row; the generator re-levels and re-evolves that map's trainers.
4. **Thistle:** the Ch0–2 script now says version 0 (matches the PBS and your events, which pass no version). Briarwick is
   the Gym 2 town now, so her team is Lv 16–18.
5. **New fights with no event yet** (trainer data exists): Brother Wick (`HOLLOW_WICK`, 0), Quent at the caldera
   (`MERIDIAN_QUENT`, 0), Sable + Hammer Captain Brisk tag double (`HOLLOW_SABLE,Sable,0` + `HOLLOW_ADMIN,Brisk,0`),
   the Mourner (`HOLLOW_MOURNER,Mourner,0`), Marchetti 0/1/2, Kroll 0/1, Quent 1/2, the Eevee Octave
   (`OCTAVE_VESPER,Vesper` 0/1/2, `OCTAVE_SINGER` Carol 0 and Aria..Carol 1–8), war soldiers (`ASHKAAR_SOLDIER_M/F`,
   `ISENMAR_SOLDIER_M/F` "Soldier" 0/1, `*_OFFICER` "Captain" 0). Fields come from `TRAINER_FIELDS`; the Ch3 and Ch13
   Octave fights and the Sable/Brisk and Ch16 fights are doubles (`setBattleRule("double")` or a tag-battle start).

## From the story editor (Gym 1/Gym 2 swap, SPINE Revision 14), 2026-11-19
Full checklist by owner: **`design/SWAP_GYM1_GYM2.md`** (§1 is yours: connections, `badge_count` tests, chapter numbers, re-pours).
1. **Script split.** `story/20_SCRIPT_CH0-2.md` is now the Prologue, Ch1 and the new **Ch2 (Saltmere, Gym 1)**. The Briarwick
   material moved, revised for Gym 2, to **`story/21_SCRIPT_CH3.md`**. I edited `layouts/scriptpour.py` (shared) so `LINES`
   reads both files in order; nothing else in it changed. `story_early.py` imports cleanly, and its Briarwick
   `^### Flavor townsfolk$` section is found in the Ch3 file. Saltmere's townsfolk header is `### Flavor townsfolk (Saltmere …)`
   on purpose, so neither existing pattern matches it.
2. **Ch2 road events moved:** Route 2's survey flags, surveyor, Juno flag lines and third-flag Antidote belong to the Dyers'
   Ford (552) now. The quarantine roadblock moves to the Hale Bell on 520, and 521's forest path becomes the corded forest road.
3. **Thistle** uses version 0 in the new script (your item 4).


## From the Trials / side-quest workstream (SPINE Revisions 13-14), 2026-11-19
No map file was edited. Everything placeable is in **`design/TRIAL_EVENTS.yaml`** (74 events on 30 maps, keyed by map ID).
Each event is one call, `{script: 'pf_trial_talk(:KEY)'}`; the plugin (`plugins/Prismfall Trials/150_Trials_Talk.rb`)
picks the scene, so dialogue changes never need a re-pour. Objects that come and go carry their visibility as a first
command `{comment: 'Condition: ...'}` (the Trials plugin reads it; put an empty page first so the event is "nothing" while
false). Existing story NPCs get a branch instead of a new event:
`{if: 'pf_trial_ready?(:KEY)', then: [{script: 'pf_trial_talk(:KEY)'}], else: [their own lines]}`.
1. **Three small new interiors** (IDs are suggestions from the free slots in each block):
   - **148 Saltmere Lantern House** (door on 140 next to the Lantern Theatre; quiet grey room, lantern rope, Sister Hollin).
   - **126 Briarwick Lantern House** (a hollow-tree room under the Loyal Three shrine; lantern-loom, Mother Aldreth).
   - **168 the Net Loft**, Ebbmouth (nets, a carved Tally Mast, a long feast table; Bersi Gullsong).
2. **Exteriors:** a wayshrine with a lantern rope by the Accord plaque on 100; a brass Rotom kiosk in 108, 143 and by the
   Lattice station on 160; the Legion recruiting barge moored in 146 (rope ring, fire pit, gong); a sea-cave mouth behind
   the big tide-pool on 527 (opens on `quest_flag(:EL_TIDE_POOL_FEUD, :sea_cave)`: 2-3 item balls).
3. **The Dovetail (109) must be boardable after Chapter 1** (a gangplank event at the berth on 100) for *Master of Nothing*.
4. **Two shortcut obstacles in Gossamer Wood (524):** a silk wall and a fallen log, each gone on
   `quest_flag(:EL_HORN_AND_PINCER, :helper)` (`:heracross` tears the wall, `:pinsir` crushes the log).
5. **Overworld sprites wanted** (stock charsets are fine): Nickit, Sudowoodo, Timburr with a plank, Wattrel in a nest,
   Crabrawler + Clobbopus, Kecleon-as-lantern, Smeargle, Ralts, Galarian Ponyta, Heracross + Pinsir, Spidops, Combee hive,
   Bombirdier, a pink-edged wagon/horse/girl for the Rehearsal; NPCs: grey-robed monk (Teasel), nun with a slate (Hollin),
   blind weaver (Aldreth), legion sergeant (Brakka), skald (Bersi), rune-carver (Ingrith), lantern-sister (Maelon).
6. **Badge-tier encounters** need no map work. Optional: a "rustling grass" overlay on tier maps (`Condition: tier(map_id) >= 1`).
7. Trial trainers live in `pbs/trainers_trials.txt` (versions 50-99): `ASHKAAR_SOLDIER_M Rekk`, `ASHKAAR_SOLDIER_F Vasha`,
   `ASHKAAR_OFFICER Brakka`, `SAILOR Gorm`. They are started by the quest scenes, so they need no trainer events.

## From the world cartographer (names, routes, world map; SPINE Revisions 13-14), 2026-11-19
Sources: `tools/worldmap/world_data.py` (names, roads, town-map squares) -> `python3 -I tools/worldmap/gen_docs.py` writes
**`design/ROUTES.yaml`** (your input for every road leg: target size, fill list, landmark, exits, secret, field, segment),
`design/PLACE_NAMES.md`, WORLD.md section 11, `pbs/town_map.txt`, `mapgen/data/town_map_positions.json` and the maps.json
updates. Renames in sources: `python3 -I tools/rename_places.py` (dry run; `--apply`; `--grep`; `--selftest`).
Nothing below needs a shared file edited by me except the two small hooks marked **(done)**.
1. **Rebuild needed for the renames.** Names, display names and sign texts are already changed in the specs and layouts
   (520, 521, 522, 524, 525, 540/541/542, 544, 560, 561, 100, 160 and the `old_*.yaml` plans; `bgm:` values are audio
   file names and were kept). The generated `.rxdata`, `map_metadata_prismfall.txt`, `map_connections_prismfall.txt`,
   `mapinfos_prismfall.txt` and `002_MapFields.rb` still carry "Route N" until `build.py` runs. A private build of the
   current tree regenerates all of them with the new names and 0 "Route N" left.
2. **(done) MapPosition comes from the town map.** `build.py` `metadata_block` now overrides `MapPosition` with
   `mapgen/data/town_map_positions.json` (every map has a square on the Velmora town map, region 0). Spec values are
   ignored where the file has an entry; keep writing them for new maps if you like.
3. **(done) `mapgen/ruby/009_TownMap.rb`** (copied by build.py into Prismfall Maps; already copied to maps_out): when
   `PBS/town_map_prismfall.txt` exists, only it is compiled, so Velmora replaces Essen as region 0 without editing the
   stock file. `tools/package.sh` ships `pbs/town_map.txt` as `PBS/town_map_prismfall.txt`; the graphic is
   `graphics/UI/Town Map/prismfall_velmora.png`. Fly spots are the PC HealingSpots of the six built towns; when you build
   a town with a PC, re-run gen_docs.py and it gains a fly spot.
4. **Revision 14 relinks (early chain):** maps.json `connections` now follow SWAP_GYM1_GYM2.md 1A (`rev14_connections`
   marks them; new or moved edges have no spans: yours). In short: 520 W -> 527 (Hale Bell, quarantine roadblock moves
   here); 527 <-> 528 <-> 140 East Gate; 140 N (North Gate, S108) -> 541 -> **552** -> 540; 540 E -> **524 W** (was 120);
   540's R3_COCOON warp removed; 120 W edge removed, **North Gate -> 566** -> 577 -> 570 East Gate; 570 N -> **578** -> 562;
   570 **South Gate** <-> 560's west end (Essentials edges join opposite sides: turn the Causeway's last stretch north or
   use a warp); 521's R2_WOOD warp is the corded forest road (open from 524 when V105 >= 1).
5. **New maps to build** (ROUTES.yaml has everything): 527 Lacecliff Walk 140x64, 528 Marram Down 110x80 (Road 1);
   552 The Dyers' Ford 80x72 (Road 2); 566 Spinners' Rise 80x120, 577 Frostwick Pass 72x96, 578 Rimewood Path 80x88
   (Road 3). Later roads add 592, 593, 612, 613, 632, 633, 652, 672, 673, 692, 693, 712, 732, 752, 755, 772, 773, 790,
   810, 811, 832, 852, 872, 892, 893 (outline).
6. **Grow the built roads toward their targets** (maps.json `size` = target, `size_was` = old): 520 64x110 (was 44x68),
   521 120x70 (62x48), 541 70x110 (30x52), 540 130x64 (64x28), 524 90x110 (50x58), 562 96x110 (48x56), 561 64x130
   (30x60), 560 140x64 (64x30). Each leg's `fill` list in ROUTES.yaml is the density brief (about one feature per 400
   tiles, no empty corridor longer than 12 tiles, every dead end pays).
7. **Not mine, noticed:** `build.py --strict` currently stops on the new OLD SLAB STAIRS check (140, 146, 147: 111
   tiles). The commit before the rename (a36c784) builds strict-green; the slab check was added after it.

## From the Pokémon distribution pass (SPINE Revision 16), 2026-11-19
Study and rules: `design/DISTRIBUTION_STUDY.md` (Reborn/Rejuvenation data, rules R1–R9); numbers in `design/warden_gates.json`.
In one line: nothing that answers the next Warden is handed out before that gym, and gated answers are ≤5% in the wild.
No map file was edited. Encounter tables (`pbs/encounters.txt`, `encounters_badgetiers.txt`) and the Trials plugin data
were changed; everything below is map-side or for the trainer designer.

**Map builder**
1. **Thistledown Manor (546, spec in `544_brinecut_mine.yaml`), Lady Thistledown's "bow out" branch:** replace
   `pbAddPokemon(:LITWICK, 14)` with `pbAddPokemon(:SINISTEA, 14)` and the line "A small candle-flame drifts out of the
   footlights and follows you." with "A chipped teacup rattles off the mantel and follows you." Litwick is Fire, an answer
   to Tamsin, and this is before her gym. Litwick still turns up in the manor from Badge 2 (overlay `[546,102]`).
2. **The Glassed Orchard (522), event "Wild Carbink":** Carbink is Rock (Tamsin's answer) and the event has no condition.
   Page 1 (fewer than 2 badges): a glimpse only, no battle ("It licks a glass tree, sees you, and phases into the glass.").
   Page 2, condition `Condition: badges >= 2` or `$player.badge_count >= 2` (Prismfall `pfm_gym_won?(:LEADER_TAMSIN)` is
   better): `setBattleRule("field", :BLEED)` + `WildBattle.start(:CARBINK, 20)`.
3. **Ebbmouth (160): new event "Harbour mast Wattrel"** (`design/TRIAL_EVENTS.yaml`, key `EBB_MAST`): a Wattrel on the mast
   by the Gale Post jetty, `pf_trial_talk(:EBB_MAST)`, visible on
   `Condition: quest_done(:EL_MASTER_OF_NOTHING) && badges >= 3 && event_mon(:EL_WATTREL) != :gifted`.
4. **The Dovetail (109), Wattrel nest:** its condition is now
   `quest_step(:EL_MASTER_OF_NOTHING) == :ask || (quest_done(:EL_MASTER_OF_NOTHING) && badges < 3)` (the bird stays aboard
   until Badge 3).
5. **Gossamer Wood (524), sap-tree duel:** condition `badges >= 2 && !quest_done(:EL_HORN_AND_PINCER)` (after Tamsin). The
   silk wall and the log stay until it is done, so the two shortcuts open on a revisit.
6. **Quests whose map events now matter later** (no map change unless the event has its own condition): the Timburr at the
   Ferrow's berth and the tide-pool feud on Lacecliff Walk open after Badge 1; Hesper keeps the Charcadet crate by the lamp
   until Badge 2; the Legion barge in Saltmere (146) and the Sudowoodo rematch on Windfall Row open after Badge 2. Players
   reach them from Frostwick by the Frostflat Causeway, so please keep that road open from the start of Chapter 4.
7. **If you implement the dyer's monkeys** (POKEMON_AVAILABILITY §2, not built yet): the Dyers' Ford dye-master gives
   Pansear or Panpour after Badge 2, and Pansage only after Badge 5.

**Trainer designer** (what the player can have, by Warden; full lists: `python3 -I tools/validate_encounters.py --gates`)
- **Dorian (Gym 1, cap 15):** the player has **no Fighting type** except a Fighting starter (Monferno at 14, Combusken at
  16 is too late, Pignite at 17 too late). Ghost: a 2–3% Sandygast. He should be a fair but real fight at Reborn/
  Rejuvenation early-gym strength (SPINE Rev 16): raw stats, the Grand Stage applause and coverage, not type walls.
- **Tamsin (Gym 2, cap 19, double):** Fire and Rock only as rare wild finds (Litleo, Sizzlipede, Rolycoly 3%, Ponyta,
  Fletchling, Nacli, Dwebble, Roggenrola, Aron 4%) or a Fire starter. **Flying is common** (Pidove, Hoothoot, Pikipek,
  Wingull, Combee): keep her answer to it (Joltik's Electroweb in rain, Surskit's Rain Dance). Fighting is now common
  (Timburr gift, the duel, Brinecut's Machop/Timburr/Meditite, Crabrawler, Mankey, Pancham): Bug resists it already.
- **Marisol (Gym 3, cap 23):** Electric only 4–5% (Joltik, Mareep, Shinx, Blitzle, Grubbin, Tynamo); **Grass is common**
  (Elowen): keep Pelipper, Araquanid and Gyarados as its answer. After Badge 2 the player can also have Charcadet,
  Litleo, Sudowoodo, Heracross or Pinsir (Moxie), Spidops, Snom, Ditto.
- **Rook (Gym 4, cap 27):** Ground only 2–5% (Diglett, Bunnelby, Sandygast, Silicobra, Nincada, Swinub, Wooper, Tympole,
  Barboach and Stunfisk by rod, Geodude by Rock Smash). After Badge 3: Bombirdier, Wattrel.
- **The Little Crucible** (`pbs/trainers_trials.txt`: ASHKAAR_SOLDIER_M Rekk, ASHKAAR_SOLDIER_F Vasha, ASHKAAR_OFFICER Brakka)
  now opens at Badge 2: please move those three teams to the 2-badge band (cap 23); the mascot boss Litleo is Lv 21.
- **Wardens 5–18:** when you build a team, add its `answers`, `gated` and `blunted` lists to `design/warden_gates.json`
  (rule R9); the encounter validators and the Trials test then enforce the gates for it. Known item: the Bombirdier
  reward (Badge 3) is Flying, immune to Sahar's Ground.

**Story editor:** `design/SWAP_GYM1_GYM2.md` §8 still asks for "one Fighting family before Saltmere"; Revision 16 withdraws
it (`DISTRIBUTION_STUDY.md` R1). The Gym Guide's "Fighting-types, they fear" line still works as a hint about Dorian's
weakness, but the player can't act on it before the badge.
`story/21_SCRIPT_CH3.md` line 124 gives a LITWICK from the manor's chandelier: please make it a SINISTEA from the mantel (map
request 1), or keep the Litwick line and have it "follow you out" only after Badge 2.

**Cartographer:** WORLD.md §11 (from `tools/worldmap/world_data.py`) still lists Heracross in Windfall Row's Headbutt trees;
it is now in the Gossamer Wood only (3%), and Windfall Row's Litleo (3%) and Shinx (4%) are rare finds. The new base tables
for 527, 528, 552, 566, 577 and 578 follow the ROUTES.yaml fill lists, except Smeargle at the Dyers' Ford, which arrives with
Badge 2 (overlay) so that the Saltmere paint-loft gift comes first.

## From the engine playtest, round 3 (fresh installs of the 17:11 and 17:55 kits, 2026-11-19)
No map file was edited. Status of earlier playtest items: **1 (103 arrival tile) and 7 (100 door tiles) verified fixed in
the engine** (in and out of the lab, Poké Center and Mart with no Debug walk-through). **10 (event tiles beyond tileset)
fixed**: `export_tilesets_rxdata.py` warns about nothing and 521 draws without the bot blanking anything.
12. ~~J1 never appears (map 140)~~ **fixed in the 21:56 build** (seen in the 17:55 kit). The built event now opens on S105 +
    `pfm?(:sm_arrived)` (from `layouts/saltmere_rj.py`). Note: `layouts/saltmere_events.yaml` still has the old
    `cond: switch: CH2_MATRIARCH_DONE` J1 page; only the older `saltmere_city.py` reads it, but it is a stale copy that
    could come back if that layout is rebuilt.
13. ~~Windfall Row (521) still pre-swap~~ **fixed in the 21:56 build** (seen in the 17:55 kit, where the forest warp was
    open after S105). 521 now has the Forest-road cordon (lifts on V105 >= 1) and the Cordon Warden.
14. **Build snapshots: a kit packaged mid-rebuild can strand the player.** The 17:55 kit had the new 520 (64x110) with the
    old 521 (62x48): `520,N,30,521,S,58` put all four open tiles of 520's north row onto blocked 521 tiles, so Windfall
    Row was unreachable. Fixed by the 21:56 rebuild of 521. A seam check would catch it at build time: for every open
    edge tile, the arrival tile on the neighbour must be passable and connected (the playtest's offline checker,
    `tools/harness/playtest/seam_check.py`, reads Map*.rxdata + Tilesets_prismfall.rxdata; happy to move it into mapgen).
15. **The Hale Bell roadblock leaks (map 520, 22:11 build): Chapter 1 can be skipped.** The four "Accord barrier" events
    (3,71), (2,73), (2,74), (2,75) don't close the road to the west edge (the 520 W <-> 527 seam is rows 72-75 at x 0).
    Row 72 is open from x 0 to 11 with no barrier on (2,72), and (1,70)-(1,71), (2,68)-(2,70) and (1,76)-(2,76) are open
    too. In the engine the bot walked from the stile (18,109) to (0,75) and onto Lacecliff Walk (527) with S105 off, i.e.
    before the Glassed Orchard. Suggested: put the barrier events on the four edge tiles (0,72)-(0,75), or wall x 1-2 so
    that the barrier column is the only way through.
16. **Chapter 1 can close without the Chapter 1 close (maps 523/520, 22:11 build).** V102 = 2 is set only by the Bed in
    Hale Farmhouse (523, "You could rest here", S105 and V102 < 2 -> the night cutscene). Nothing tells the player to
    rest: Wenna's Biscuit lines don't, and the script's "plays when the PC sleeps at the farmhouse or the inn" has no
    inn event yet (104). But the Hale Bell barrier on 520 opens on S105 alone. In the engine the bot returned Biscuit,
    walked to the stile (the send-off needs V102 >= 2, so nothing played) and went on to Lacecliff Walk: no send-off,
    no Town Map, no "Eighteen Roads", still in Chapter 1. Suggested: gate the Hale Bell barrier on V102 >= 2 (with a
    guard line pointing back to the farm), or have Wenna/Juno ask "stay the night?" when Biscuit comes home.

## From the puzzle engineer: the Saltmere audience (SPINE Revision 19, item 3), 2026-11-19
**For map builder 9 (Saltmere 140/143/144/146/147 are yours; I have not edited them).** "The more people you meet around town,
the more audience shows up for your fight." The count lives in **V313 `STAGE_AUDIENCE`** (`mapgen/flags.yaml`). Runtime:
`plugins/Prismfall Puzzles/007_Puzzles_SaltmereCrowd.rb`. Map 154 already reads it: each person below has their own seat by the
aisle, the rest of the town fills four seats per head, and the count sets the Grand Stage's opening stage for Dorian
(0-6 sparse = stage 1, 7-13 good = stage 2, 14+ full = stage 3).
14. **Add one line to each of these events, as the first command of their talk page:** `{script: 'pfm_audience(:KEY)'}`
    (it counts each person once, so it is safe on every talk, and returns quietly afterwards). Keys are fixed: map 154's
    seats are named after them.

    | Key | Event (map, at) |
    |---|---|
    | `:caramel_seller` | Caramel Seller (140, 30,38) |
    | `:busker` | Busker (140, 54,33) |
    | `:ogre_child` | Child with an Ogre puppet (140, 36,34) |
    | `:retired_actor` | Retired Actor on a bench (140, 28,55) |
    | `:hound_two` | Hound Number Two (140, 49,52) |
    | `:fishwife` | Fishwife (140, 66,46) |
    | `:ferry_woman` | Woman from the ferry (140, 76,46) |
    | `:eevee_breeder` | Eevee breeder (140, 58,38) |
    | `:salt_raker` | Salt raker (140, 40,66) **and** Salt raker (146, 36,8): same key, either one counts |
    | `:harbourmaster` | Harbourmaster (143, 6,5) |
    | `:saltwife` | Saltwife (144, 7,4) |
    | `:stevedore` | Stevedore (146, 26,34) |
    | `:old_angler` | Old angler (146, 8,57) |
    | `:fisherman` | Fisherman (146, 4,45) |
    | `:old_sailor` | Old Sailor (146, 84,40) |
    | `:smoke_stagehand` | Stagehand on a smoke break (146, 38,27) |
    | `:costumier` | Costumier (147, 27,37) |
    | `:street_player` | Street player (147, 44,46) |

    Not counted on purpose: the Accord Inspector, the Meridian Clerk, the Gate Warden, the Legion recruiter (none of them would
    cheer you) and the Grey Pilgrim. The generic "Townsfolk N" don't count either; if you give any of them a name and a line
    of their own, they can join (tell me the key and I'll give them a seat).
15. **The Trial board needs nothing from you:** `EL_LANTERNS` (Sister Hollin) counts 3 when map 150 or 154 loads.
16. If an event above moves or is renamed, keep its key. If one is cut, tell me: its seat in 154 would stay empty.

**For the story editor (SPINE Revision 19, Gym 2 redo):** map 131 is now **The Canopy** (web trampolines in the elder's
hollow; GYM_PUZZLES Gym 2) and 130 the weavers' lobby. `story/21_SCRIPT_CH3.md` still describes the Weaving Hall: lines 307
(trainer: "planks and looms... the wrong heddle"), 361 (gym guide: heddles, "count lifts, not pulls"), 363-364 (apology cards
about the loom bed / "the Weaving Hall is upstairs"), 367 (Orla: "Mind the loom bed"), 379, 382 (map 131 heading), 392
("the great loom on the top ledge") and 537. The built maps already use web lines for these (gen_loomhouse.py: the gym
guide explains taut and sticky webs and the Joltik; Orla bounced into the net; the cards are about webs; Tamsin's first
line is "My grandmother wove the looms downstairs. The webs up here, the Bugs wove."). Tamsin's battle, win and confession
lines are unchanged. Nell and Orla are in the Canopy now (Orla on ledge 2, Nell on ledge 1), Bram on Tamsin's ledge.

## From the world cartographer, round 2 (Geography v2 and the land war, SPINE Revision 18), 2026-11-19
Elowen is now the middle of Velmora (Ossaria north, Isenmar west, Ashkaar east, Zenith/Nadir south) and the war is
fought on land in Ossaria. Sources and generated files as in my round 1 above; the geography in words is
`design/WORLD_MAP.md`, the borderlands and gym-order crossings are WORLD.md §10, the war theatre §9.
**No built map needs a change.** The start chain (100–578) did not move, every map ID is kept, and the 88 `MapPosition`
values in `maps_out/PBS/map_metadata_prismfall.txt` already match `mapgen/data/town_map_positions.json`.
1. **Revision 14 links are final in maps.json** (declarative, a second gen_docs run changes nothing): 540 S <-> 552;
   Cocoonfall Hollow 548 is entered only by DEEP_COCOON from Gossamer Deepwood 525 (your 525 specs already use that
   link; no R3_COCOON is left in the specs); 132 <-> 134 by warp; **134 "Loomhouse Upper Lofts - Granny's Knot"** (20x15,
   segment 2) is in maps.json; 133 is retired; Frostwick 570's duplicate south edges are gone. Segment 2 (after Badge 2):
   525, 548, 151–153, 132, 134.
2. **New planned maps** (outline; ROUTES.yaml has size, fill, exits, landmark): 595 Coppice Ride and 594 Wallshadow Row
   (Road 4), 602 Candle Down and 603 the Highwold (Road 5), 634 Wormwood Lea (Road 6), 756 Kingsmead (Road 12). With
   them the **Crown Road** rings the Crownwall; Roads 8 and 12 reuse Candle Down and the Highwold (ROUTES.yaml `via`).
   The Gutterfall 633 and the Long Drop 672 are now borderland F (Nadir/Elowen) maps.
3. **Renamed (not built):** 582 Lumen West Gate (was Lumen South Gate; Lumen is entered from the west off the Arc-Lamp
   Mile), 920 The Rimed Sands (was the Rime Narrows), 922 Skaldfast - Rime Keep (was Harbour Keep), 926 The Glass Dunes
   (was the Shattered Ice).
4. **The war theatre is land** (920–927, maps.json `war_theatre` and `connections_outline`): 920/924/925/926 use
   `G5_DESERT_CANYON`; Skaldfast 921–923 is Isenmar's border fortress on Ossaria's west edge at the foot of the Mast
   Glacier, not a port; Cinder Cape Warfort 927 stays on Ashkaar's coast. 926's default field is DESERT
   (FIELD_DEFAULTS.yaml synced; `011_FieldEffects_MapDefaults.rb` regenerated with `tools/field_defaults_to_rb.rb`).
5. **Road 11 has an air leg:** Anchorhold 730 -> airship -> the Tetherline 732 (Isenmar and Zenith share no border).
   When you build them, it is a warp/event from Anchorhold's mooring to the Tetherline, not a map edge.
6. **(done) Fly follows the live HealingSpot:** `mapgen/ruby/009_TownMap.rb` (copy in maps_out/Plugins/Prismfall Maps
   is identical) wraps `PokemonRegionMap_Scene#pbGetHealingSpot`, so when a rebuild moves a PC door, Fly uses the map
   metadata's `HealingSpot` instead of the coordinates in `town_map.txt`. Nothing to do on your side.

## From map builder 9 (2026-11-19)
**Doors and warps that moved** (links unchanged unless said; build.py checks every arrival and now every edge seam):
- **Saltmere 140:** PC (24,32) -> **(54,24)** (HealingSpot [140,54,25]), Mart (58,30) -> **(60,24)**, Pageant Hall / Lantern
  Theatre (46,26) -> **(34,24)**, Saltwife's House (26,6) -> **(23,49)**; **new** Lantern House door (25,24) `SM_LANTERN` -> 148.
  **146** Harbour Office (52,26) -> **(55,21)**. **147** Playhouse `SM_GYM` (44,18) -> **(44,33)**.
- **Saltmere districts:** 140 (56-61,71) <-> 146 (42-47,0); **new** 140 (9-14,71) <-> 147 (40-45,0) (the Players' Causeway).
  The old Players' Gate edge warp 140 E (87,42-45) <-> 147 W (0,36-39) is gone: 140's east edge is the East Gate to 528.
- **Connections (PBS):** 140 N 43 <-> 541 S 30; 140 W 31 <-> 560 E 12; 140 E 44 <-> 528 W 38; 100 N 28 <-> 520 S 11;
  520 N 30 <-> 521 S 58; 520 W 72 <-> 527 E 22; 527 W 18 <-> 528 E 30; 541 N 34 <-> 552 S 38; 552 N 39 <-> 540 S 20;
  540 E 30 <-> 524 W 50; 120 N 52 <-> 566 S 38; 566 N 42 <-> 577 S 30; 577 W 37 <-> 570 E 23; 570 N 27 <-> 578 S 40;
  578 N 36 <-> 562 S 26; 570 S 4 <-> 560 N 2. Removed: 120 W <-> 540, 540 S <-> 541, 560 W <-> 570 E, 570 N <-> 562 S.
- **Rebuilt roads:** 520, 521, 524, 540, 541 at ROUTES.yaml sizes. Doors: 521 farmhouse `R2_FARM` (30,35) -> **(50,44)**;
  521 forest-road warps (0,9-11) now land on 524 (40-42,108); 524 north warps (44-46,0) <-> 120 (35-36,63); 524 Woodward's Hut
  `WOOD_HUT` (42,25) -> **(58,51)**; 524 Deepwood warp `WOOD_DEEP` (49,27) -> **(89,48)** (Cut tree (82,48)); 540 manor
  `R3_MANOR` -> **(64,14)**, mine mouth `R3_MINE` (51,15) -> **(8,24)**; 541 mine back door `R4_MINE` (25,24) -> **(57,49)**,
  Brinewife's Rest `R4_REST` -> **(12,58)**. **Removed:** `R3_COCOON` (548's south warp is a "glass-choked" sign now).
- **Briarwick 120:** **new** Lantern House door (26,8) `BW_LANTERN` -> 126; "To Gossamer Wood b" lands on 524 (45,1).
- **Ebbmouth 160:** **new** Net Loft door (36,24) `EB_NETLOFT` -> 168.
- **Playtest bot:** waypoints on 520/521/524/540/541 changed with the rebuilds; the Saltmere entrance is the East Gate
  edge from 528, the North Gate is barred until S108 (events "North Gate bar 1-6" at 140 (43-48,6)).

**Done from the requests above:** distribution items 1 (Sinistea from the manor mantel), 2 (Carbink glimpse, battle Lv 20
after Tamsin), 3 (Ebbmouth mast Wattrel), 4 (the Dovetail's Wattrel nest condition), 5 (the sap-tree duel after Badge 2;
the silk wall and the fallen log on 524). Playtest 11 / 14: `build.py` has a SEAM check and `--strict` fails on it.
Puzzle engineer item 14: `pfm_audience(:KEY)` is the first command of all 18 named people (140, 143, 144, 146, 147).
Trials: 148 / 126 / 168 built; the Legion barge berth on 146 has Brakka and the herald; the Dovetail can be boarded from
the Ferrow berth after Chapter 1 (gangplank on the pier, 100 (34,52) -> 109 (9,14)). Not done: the Timburr gift and the
tide-pool duel (moving to the distribution agent), 167 Mill Quay and 568 the Rehearsal (not built).
7. **Bug, Frostwick's fly spot is stale (found in the real engine).** A private mkxp-z run of the current tree flew to all
   six towns from the Fly screen (Velmora region 0 compiled from `PBS/town_map_prismfall.txt`, 220 points; the scene's
   own `pbGetHealingSpot` returned the expected spot for every town). Saltmere, Ferrow's Landing, Briarwick, Ebbmouth
   and Verdance land on a free tile. **Frostwick lands at (13, 26), boxed in behind the market stalls** with no way out:
   `mapgen/layouts/rimewood_interiors.py` line 29 still gives 571 `HealingSpot: [570, 13, 26]`, but the rebuilt
   Frostwick has its Poke Center door (FW_PC) at (6, 34), so the spot should be **[570, 6, 35]** (the tile below the
   door, as in Saltmere and Briarwick). The same stale spot also sends a blacked-out player there. After you fix it,
   `python3 -I tools/worldmap/gen_docs.py` copies it into `pbs/town_map.txt` (and 009_TownMap.rb already reads it live).

**For map builder 9 (puzzle engineer, 2026-11-19 late):** puzzle events are now laid over three maps you own, through
`mapgen/puzzles/dungeons.py` `EVENTS` (your specs are untouched; `build.py --strict` proves them on your built maps):
17. **525 Deepwood (D2):** a silk-walled lantern hollow round the north-east pocket, x25-40, y4-10 (walls, three curtains,
    three cocoons, two Joltik posts, TM19 at (31,2), a sign at (25,9)). Please keep that pocket's terrain as it is, or tell
    me before you change it (the proof will fail the strict build if a wall lands on open ground or the pocket opens up).
    Also noticed: the "Crystal silk" gate (41,20) uses tile 17753, which is passable on tileset 53, so the gate can be
    walked through; a solid graphic (or a character sprite) would hold it.
18. **562 Rimewood (D7 Frost Loom):** the east edge's dead-end side path (x43-47, y12-19): icicle curtains (47,16-18),
    three pegs (40-42,19), the cache (44,12), a trapper (39,21). Same request: keep that corridor 1 wide.
19. **524 Gossamer Wood (D2 teach and twist), when your rebuild settles:** one silk curtain across the trail that leans
    north (teach), and a short one-way run between two loops (twist). The runtime is ready: an event with the charset
    `pf_silk_curtain` (rows: down = leans S, left = W, right = E, up = N; `dir_fix`), trigger touch, script
    `pfp_silk("N", 0)`. Send me the coordinates and I'll add them to the proof.
20. **548 Cocoonfall Hollow (D3 anchors):** the puzzle is proven (`dungeons.py` d3: start a and b taut, parity) but the
    crater floor has no glass ravine for its three crystal bridges. If you give the hamlet a ravine to the north with three
    1-wide crossings (to the NE cocoon-house, the NW Shard house and the Matriarch's nest), I'll lay the anchors and bridge
    events over it the same way as 525 and 562.

**For the story lead (FLAGS.md pointer rows, puzzle engineer 2026-11-19 late):** new IDs in `mapgen/flags.yaml` (the installer
names them from there): V305–V307 are now `CANOPY_WEB_A/B/C` (Gym 2's Joltik webs; the old `LOOM_A/B/C` heddles are retired,
V308 `LOOM_FOYER` is free); **V313 `STAGE_AUDIENCE`** (the Saltmere audience, SPINE Rev 19); **S531–S533 `D7_CURTAIN_1..3`**
(the Rimewood's Frost Loom). D2's cocoons keep S506–S508.

## From the Eevee Octave workstream (SPINE Revision 19, item 1), 2026-11-19
No map file and nothing in `pbs/trainers.txt` was edited. Design: **`design/EEVEE_OCTAVE.md`**. Every placeable event is in
**`design/TRIAL_EVENTS.yaml`** (maps 145, 120, 524, 160, 167, 181, 215, 220, 240, 340, 742, 489), one call each,
`{script: 'pf_trial_talk(:KEY)'}`; dialogue lives in the Trials plugin.
**For the map builder**
1. **New interior, suggested 215: the Temple of the Noon Sun** (Sona, Espeon). A small round sandstone temple half under a
   dune, door off Sunbleach Flats (613) or Duneholt's Sandgate (203): one room, a light-shaft in the roof that drops a circle
   of light on the floor, a bronze bell, three sand drifts in the shaft (events `SUN_DRIFT`).
2. **Map 145 backstage:** Vesper's duet partner becomes **Lyra** (`OCTAVE_SINGER,Lyra,0`, once the trainer designer adds
   it; Carol is now met only in Ch20). After her lines, add `{script: 'pf_trial_talk(:VESPER_SALTMERE)'}` (her request; it
   starts the quest line). **Lucent cloister** (Ch13, S191): add `{script: 'pf_trial_talk(:VESPER_LUCENT)'}` after her double.
3. **489 Glassfall Memorial Garden:** Carol (from S155) and Vesper (`Condition: octave_ready`; the user's "a trainer spawns
   in Crownhaven"). Optional decor: the seven other singers with their Eeveelutions in a half-circle behind Vesper, same
   condition.
4. **742 Mirror Mere** is frozen (ice tiles, Lento's reflection under it) until `quest_done(:AN_OCTAVE_STILL_WATER)`, then
   open water. **220 Mirefen:** the three ferry lamps exist only at night (their condition includes `night`).
5. Repeated objects (river notes, junction boxes, sand drifts, lamps, cracks) erase themselves with self switch A after their
   call, like the Ferrow's Landing planks. The singers stand where `near:` says; the moss-stone (524) shows Lyra beside it
   while `quest_step(:EL_OCTAVE_MOSS) == :stone`.
6. Sprites (stock charsets are fine): eight singers in Choir grey (Lyra, Aria, Sona, Lento), cut-down/scorched/soot robes
   (Cadence, Forte, Noct) and white (Carol, Vesper), each with an Eevee-line follower; Legate Varra Kosk; a marsh ferryman.
**For the trainer designer** (provisional teams in `pbs/trainers_trials.txt`; tune them, or move them into your files)
7. New: `OCTAVE_SINGER` Lyra/Aria/Cadence/Sona/Noct/Forte/Lento/Carol **v50** (kingdom duels: a local partner + the
   Eeveelution at the next Warden's cap − 1: 18, 22, 26, 30, 34, 38, 58, 88) and **v60** (gauntlet bouts: your Ch20 v1–8
   sets at Lv 90 with the type's Z-crystal instead of the seed; Carol has Moonblast for Fairium Z), `OCTAVE_VESPER Vesper`
   **v60** (Eevee "Amen" Lv 92, Adaptability, Eevium Z; Last Resort / Stored Power / Shadow Ball / Quick Attack).
8. **Ch2 double:** please add `OCTAVE_SINGER,Lyra,0` (an Eevee around Lv 17, Carol v0's role). **Retire** Carol v0, Aria..Carol
   v1–8 and Vesper v2 (and their `TRAINER_FIELDS` / `ENTRY_FIELDS` rows), or move the v60 sets into those slots and tell me:
   the versions are two constants in `plugins/Prismfall Trials/012_Trials_Octave.rb` (`GAUNTLET_VERSION`, `HOST`).
9. **Balance (headless harness, AI on both sides):** six Lv 100 Snorlax lost at bout 4; an EV-trained Lv 100 team (Snorlax,
   Garchomp, Metagross, Tyranitar, Volcarona, Togekiss) won the nine with 146 of 2,334 HP left. A home-field Z-move is a
   near one-shot: Moss's Bloom Doom (Flower Garden stage 3) took 73% of a Lv 100 Snorlax; in the real engine Forte's Inferno
   Overdrive (Volcanic + Flash Fire lit by the field + STAB) one-shot a Lv 95 Vaporeon through the resist. Suggestions: 88
   for bouts 1–8, no Flash Fire on Forte's Flareon (Guts?), a Leftovers/Sitrus on the frail ones instead of nothing. The
   player can use bag items between turns; there is no healing between bouts.
10. Z-crystals work for any trainer: the AI unleashes an eligible move as a Z-move once per battle (and holds it back against
    an immune target). Status moves don't become Z-moves.
**For the field workstream:** a Z-move counts as its type for every field rule; rules naming a base move don't carry over
(Dive, Lava Plume, Draining Kiss...). To give a Z-move a field effect, name it in `:moves` or match `:flags => ["ZMove"]`.
The Z plugin adds one showpiece itself: on the Grand Stage a Z-move raises the applause a stage (`004_ZPower_Fields.rb`).
**For the EBDX Bridge owner (optional):** the player's Z choice is a Yes/No box after picking the move (works on EBDX's box,
screenshot in `run_zpower.sh zpower`); a Z button on the Fight menu like the Mega button would be nicer. Z-moves show their
base move's animation; `:prismfall_zmove_unleashed (battle, user, z)` is there if you want a Z aura.
**For the art workstream:** EBDX logs "Could not find the Trainer sprite" for `OCTAVE_SINGER` and `OCTAVE_VESPER` in every
Octave fight (real-engine run); battle sprites for the singers and Vesper are wanted.
**Note for everyone touching moves:** the shipped base's Generation 9 Pack runs with `Settings::CHAMPIONS_MECHANICS = true`
(Last Resort, Fake Out after turn 1, Stockpile moves etc. become unselectable; every move's PP becomes 8/12/16/20). Our
harness run folder has an older Gen 9 Pack without it, so headless results can differ there. Z-Power handles Last Resort ->
Extreme Evoboost under it.
**Packaging:** new plugin folder `plugins/Prismfall Z-Power`; new `pbs/moves_zpower.txt` and `pbs/items_zpower.txt` (copied
as-is by `tools/package.sh`; v21.1 merges `PBS/moves_*.txt` / `items_*.txt`). Story docs edited for the reshape (story editor,
please review): `story/03_CAST.md` (Vesper + the singers), `04_ACT_I.md` and `20_SCRIPT_CH0-2.md` (Ch2: Lyra, Vesper's
request), `06_ACT_III.md` (Ch13), `08_ACT_V.md` (Ch20), `00_OVERVIEW.md`, `10_CHOICES_ENDINGS.md`, `12_RUIN_ROUTE.md`.

## From story editor (geo v2), 2026-11-19
SPINE Rev 18 moved the Ashkaar–Isenmar war onto land, into Ossaria's western dunes. The story is rewritten for it
(`story/14_WAR_AND_BLESSING.md` Part B, `story/13_CUTSCENES.md` WAR-1, the act files, 00–03, 09–12), and
`design/FLAGS.md`, `NARRATIVE_KEYS.md`, `TRIALS.md`, `CUTSCENES.md` (a §4 note and the §8 wishlist only) and
`ART_DIRECTION.md` are synced. **No ID, key or value was renamed or renumbered.** What is left is in files I don't own.

**Cutscenes owner (`plugins/Prismfall Cutscenes`): restage the war climax in the desert.**
1. **On-map `:WAR_CLIMAX`** (`013_Scenes_War_OnMap.rb`), per the rewritten WAR-1: a Glass Dunes stage instead of
   `pfw_shattered_ice.png` (export map 926 once it is built; until then a desert stage from the Rejuvenation/Reborn desert
   tiles: Skaldfast's rime-white walls far left (west), the Siege Camp's palisade right (east), the Steamline's steam along
   the top, the grey sea on the horizon, the bone-carters' white banner on a dune between the hosts). Kyogre rises out of a
   flood-sea that pours in over the sand (a flood-front sheet), Blue Flare leaves a glass trail on wet sand, shot 6's ring is
   sand glassing rather than ice cracking, shot 7 has a wave setting into glass, shot 12 the flood draining back out, and
   shot 15 the glass plain with the bone-carters raising a new banner. Legendaries stay overworld-scale acting sheets.
2. **Procedural version** (`013_Scenes_War.rb`): dunes instead of pack ice (`background :floes`, the `ice` palette, `ground`
   "the ice between the two hosts"); shot 1 has Eirik on the lead ice-sledge on frozen sand and the Dominar on the Siege
   Camp's earthwork (not the Warfort wall); shot 9C's `:prow` ship becomes Marisol's sled-boat riding the flood (the `:ship`
   prop, `004_Actors.rb:207`, and the sled-ship row, `005_Backdrops.rb:301`, can stay as land sledges); 13B/C put the
   winner's banners over Skaldfast (B) or over the Siege Camp (C), not Cinder Cape.
3. **Text:** "The Beam Clash on the Glass Dunes" in `013_Scenes_War.rb:4`, `013_Scenes_War_OnMap.rb:4`, `015_Debug.rb:15`
   and the example title card in `010_Text.rb:6`; `WAR_STAGE` and the stage comments; Eirik's line becomes
   "Isenmar! The sea has come to the sand!".
4. **No-legend variant:** your reading is confirmed (`legends: false` exactly when `choice(:war_legend) == :neither`). It has
   no flood: Mamoswine bursts up out of the Rimed Sands' frozen trench-line (or Gyarados out of its meltwater), and the
   glass in shot 7 comes from frost meeting fire.
5. Then bring `design/CUTSCENES.md` §4 up to date with the new build (I only added a "pending restage" note there).

**Core owner (`plugins/Prismfall Core`), strings only:**
6. `012_Narrative_Data.rb`: copy the new descriptions of `:war_warning` (:285), `:war_convoy` (:286), `:war_prisoner` (:287)
   and `:war_climax` (:289) from NARRATIVE_KEYS §4.3 (Frostfang Pass looking at Ossaria's dunes; siege-runners and sledges
   from Duneholt; Anja in the Siege Camp; "the beam clash on the Glass Dunes").
7. `015_Festival_Draw.rb:78`, the Anja vs Brann caption: "Two Wardens who were on opposite sides of the Steamline a season
   ago." (was "opposite shores").

**Trials owner (`plugins/Prismfall Trials`):**
8. `120_Quests_Catalogue.rb:102–105`: title "The Saga of the Glass Dunes" (the key `IS_SAGA_OF_THE_ICE` stays), summary
   "...a witness who stood on the glass", step `:ask` "Tell Bersi what really happened on the Glass Dunes." Then re-run
   `ruby tools/trials_docs.rb`: `design/TRIALS_QUESTS.md` is generated, and the regeneration overwrote my edit there.
   Bersi's verses should sing the land war (Skaldfast on the sand, the flood, the glass, the bone-carters).

**Trainers owner:**
9. `tools/trainer_gen/gen.py:1315–1336` → `pbs/trainers.txt` comments: "Skaldfast harbour (map 922, Frozen Lake)" →
   "Skaldfast - Rime Keep (map 922, Frozen Lake)"; "The Shattered Ice (map 926, Frozen Lake)" → "The Glass Dunes (map 926,
   Desert)"; "Isenmar ice-fleet officer" → "Isenmar sled-host officer". 926's default field is DESERT now, so the soldiers
   fought there should be built for sand (and for the flood), not for Frozen Lake.

**Cartographer (`tools/worldmap/world_data.py` → maps.json, WORLD.md, WORLD_MAP.md):**
10. maps.json still carries sea-war briefs. **921** Skaldfast - Outer Walls ("fortress-port frozen into the sea", "chained
    longships", "keep on the harbour mole", "sortie across the ice"); suggested: "rime-glazed granite walls on the sand's
    edge at the Mast Glacier's foot; sled-yards; keep over a frozen spring; set pieces: dragonfire run along the wall, sortie
    onto the Rimed Sands, hospital in the great hall". **926** the Glass Dunes ("cracked ice plain", "lava-breached floes",
    "flat white sea"); suggested: "bone-white dunes across the caravan road; Kyogre's flood-sea pouring in; glass where the
    fire passes; afterwards a glass plain of standing glassed soldiers and the bone-carters' banner".
11. War states. Change **160** Ebbmouth ("Isenmar blockade fleet in the roads") → "the Thane requisitions the Ebb Guild's
    sleds for the front and the Guild refuses; Thaw refugees; Ashkaar envoys expelled"; **460** Wyrmrest ("Dominar's legions
    camped on the slopes (Act V)") → "the legions gone to the war in Ossaria; Sigrun's riders hold the gate"; **660** the
    Ashmarch ("scorched ice-raider wrecks") → "supply and conscript columns north to the Cinderglass Barrens". Add war states
    the story now uses: **200** Duneholt (Kassan's neutrality notices on the Sandgate, caravans leaving by the east gate,
    foreign quartermasters in the Hall of Audience 206, bone-carters at the west gate), **360** Cragholm (Ossarian well-folk
    among the refugees), **670** Glasswake (apprentices taken by the levy), **662** the Cinderglass Barrens (legion columns
    west), **730** Anchorhold (sled-convoys by night, dragon patrols), **810** the Dry Tide (the bone-carters' camp). WORLD.md
    §9's list of maps with a `war` state grows to match.
12. WORLD_MAP.md §7 says "Cragholm (Gym 13) is the nearest gym city to the front". Duneholt (17, 3) is nearer the Siege Camp
    (15, 2) than Cragholm (21, 2), and the story now uses that: Duneholt is "a day's ride" from the front, and the Lease keeps
    armies out of it. Suggest: "Duneholt is the nearest city; in Act IV the PC reaches the front from Cragholm by way of
    Duneholt."
13. **Timing:** the story walks to the front from Duneholt in Ch14–16 (`:war_convoy` after Badge 13, then `:war_prisoner`), but
    the Dry Tide 810, the only drawn road from Duneholt to the Glass Dunes, is segment 14 (Road 15's side road). Either open
    it from segment 13, or give the convoy its own way in (a warp or event from Duneholt's west gate into the war maps). The
    story only names the Dry Tide where it is late enough (the bone-carters' camp, and Sigrun's landing in Ch19).
14. Small maps the story asks for (also in 13_CUTSCENES, "Renames"): the Dominar's command pavilion (924 interior), the
    observers' sandstone mesa (WAR-1 shot 14), and the bone-carters' camp on the Dry Tide (part of 810). New story names with
    no map: **the Elector's Lease** (Kassan's lease of the western dunes) and **the bone-carters** (Ossaria's burial guild).

**Fields team:**
15. 926 in the climax battle: the story beat is DESERT → Kyogre's flood-sea comes in (water over sand) → Reshiram's fire turns
    it to glass (steam-glass, Bleed-like). The transitions are yours; FIELDS.md's Desert note ("rain wakes a superbloom;
    searing heat makes glass") already fits. Please also check 925 the Steamline: the story treats it as a Bleed line that
    only the PC can cross, and FIELD_DEFAULTS has it as ASHEN_WASTE.

**Coordinator:** I left `design/SPINE.md:140` (Revision 5's "Isenmar (frozen sea fortress-ports)") alone. It is a historical
revision entry and is still true of Rimeholt and Ebbmouth.

## Reply from the world cartographer to the story editor (geo v2, items 10–14), 2026-11-19
All five are in `tools/worldmap/` and regenerated (maps.json, ROUTES.yaml, PLACE_NAMES.md, WORLD.md §3/§9/§11,
WORLD_MAP.md §6–§7, `pbs/town_map.txt`, positions, FIELD_DEFAULTS.yaml → `011_FieldEffects_MapDefaults.rb`, both map
images). A second gen_docs run changes nothing.
- **10. Briefs.** 921's and 926's `visual_brief` now describe the land war (your wording); 921 and 922 use
  `G4_SNOW_FORTRESS` instead of `G4_SNOW_COAST`.
- **11. War states.** Rewritten: 160, 460, 660, and 300 (its "harbour chained" became "sleds requisitioned for the front").
  New: 200, 360, 670, 662, 730, 810. WORLD.md §9 lists every map with a `war` state.
- **12.** WORLD_MAP §7 and WORLD.md §9 now say Duneholt is the nearest city, and that in Act IV the PC reaches the front
  from Cragholm by way of Duneholt.
- **13. Timing.** The Dry Tide 810 moved from Road 15 to **Road 14** (side road from Duneholt's west gate) and is now
  **segment 13** in maps.json (`SEG_FIX`; its ID no longer tells the badge count). The war maps 920–927 stay segment 10:
  the Isenmar side opens from the Mast Glacier on Road 11.
- **14. New maps (outline, for the map builder):** **928 Ashkaar Siege Camp - Command Pavilion** (interior of 924, 24x18,
  segment 13, field NONE), **929 The Observers' Mesa** (36x28, segment 17, DESERT, square 13,3), **930 The Bone-Carters'
  Camp** (44x32, segment 13, DESERT, square 14,3, at the Dry Tide's west end; Sigrun's landing in Ch19). Their records in
  maps.json carry `key_features` and `connections_outline`. The Elector's Lease and the bone-carters are named in
  WORLD.md §9 and WORLD_MAP §7 (no maps).

## From the field workstream: the Glass Dunes and the Steamline (SPINE Revisions 10 and 18), 2026-11-19
Answers story editor item 15. Two new fields, `:FLOODED_DUNES` (139) and `:GLASS_DUNES` (140); player-facing rules in
`design/FIELDS.md`, backdrop briefs in `design/FIELD_BACKDROPS_NEEDED.md`, harness proof in
`docs/battle_captures/glass_dunes/SUMMARY.md` (`tools/harness/run_glass_dunes.rb`).
**The 926 sequence:** DESERT (the map default) -> **Flooded Dunes** (Kyogre: Primordial Sea's heavy rain, or one Origin
Pulse) -> **Glass Dunes** (Reshiram: one Blue Flare or Fusion Flare, or two other searing moves, *even when the heavy rain
snuffs the flame*). Then it is a tug of war: heavy rain / 2 Origin Pulses / 3 floods re-flood the glass, Blue Flare glasses
it again, and in two rounds where opposing sides both land a great Water beam and a great Fire beam the Imprints tear
open into the **Bleed** (WAR-1's dome). On 925 and 926 the Bleed only echoes the war's fields (Volcanic, Cinderglass,
Frozen Lake, Snowy Mountain, Desert, Flooded Dunes, Glass Dunes). **The Steamline (925) now defaults to BLEED** (was
Cinderglass): the story calls it a Bleed line only the PC can cross.

**For the trainer designer (the 926 / 925 soldier teams):**
1. What changed under the plans in `tools/trainer_gen/gen.py`'s war block:
   - **Desert (920, 926):** rain is still the Superbloom. The *flood* is heavy rain, Origin Pulse, or 3 more floods
     (Surf, Muddy Water, Hydro Pump, Water Spout, Wave Crash, Water Pledge; Scald doesn't count) once it is in bloom.
     So "Isenmar brings the sea" is two steps: Drizzle, then three floods. Two searing moves now make the **Glass
     Dunes**, not Cinderglass, so "Ashkaar brings the glass" no longer gives obsidian Rock x1.3 / Stone Edge x1.3 / Steam
     Engine every turn.
   - **Flooded Dunes (Isenmar's ground):** Water x1.3, Ice x1.2, Electric x1.3 against grounded targets; Swift Swim,
     Torrent, Rain Dish, Hydration and Dry Skin work without rain; grounded non-Water/non-Ground Pokemon wade (x0.75
     Speed); grounded Pokemon can't be burned; damaging Ground moves also hit as Water; Whirlpool / Sand Tomb / mud moves
     x1.5; Spikes, Toxic Spikes, Stealth Rock fail; 3 big Ice moves freeze it into a **Frozen Lake** (Isenmar's second
     ground). Fire is halved against grounded targets except searing moves and Turboblaze. The tide drains it into a
     Superbloom after 5 rounds without rain unless Water attacks feed it, so Drizzle/Rain Dance holds it.
   - **Glass Dunes (Ashkaar's ground):** Fire x1.2, Fire types heal 1/16 a turn, Steam Engine +1 Speed on entry, Water
     attacks may burn grounded targets (Kyogre's side harnesses it too), nothing freezes, Dig fails, no sand or hail,
     light beams x1.3. Quakes, heavy stomps and big Ice moves **shatter** it (shards hit the user's grounded foes): 3
     shatters break it to the Desert, or back into the flood if it is raining; each damaging Fire move anneals a crack.
     Careful: Garchomp's Earthquake breaks Ashkaar's own glass; Mamoswine's Icicle Crash in Pelipper's rain is Isenmar's
     way back to the sea.
   - **The Steamline (925) is the Bleed:** every 3 rounds it echoes one of the seven war fields; off-type attacks x1.2;
     Protean / Libero / Color Change +1 Speed; Weather Ball, Terrain Pulse, Judgment, Techno Blast x1.3. The two
     925 soldiers (Ashkaar M 1, Isenmar M 1) were written for Cinderglass, which is now only one of the seven echoes.
2. **Suggested WANTS** for `plugins/Prismfall Field Effects/012_FieldEffects_TrainerPlays.rb` (your file, not edited):
   `:ISENMAR_SOLDIER_M`, `:ISENMAR_SOLDIER_F`, `:ISENMAR_OFFICER` => `{ :FLOODED_DUNES => 20, :FROZEN_LAKE => 16,
   [:DESERT, 2] => 8, :GLASS_DUNES => -20 }`; `:ASHKAAR_SOLDIER_M`, `:ASHKAAR_SOLDIER_F`, `:ASHKAAR_OFFICER` =>
   `{ :GLASS_DUNES => 20, :VOLCANIC => 16, :FLOODED_DUNES => -20, [:DESERT, 2] => -10 }`; and for the partners,
   `LEADER_SIGRUN` `:GLASS_DUNES => 14, :FLOODED_DUNES => -14`, `LEADER_MARISOL` `:FLOODED_DUNES => 18,
   :GLASS_DUNES => -14`. A positive want also lets the AI pick a searing move that heavy rain will snuff, since the snuffed
   move still glasses the flood (the transition is `:even_if_failed`). Harness (singles, AI vs AI, 926): without WANTS no
   captain changed the field (Isenmar Captain 1 bloomed the dunes with Drizzle and lost the bloom to Fire Fang; Ashkaar
   Captain 1's Torkoal chose Earth Power and Protect, never Eruption); with the suggested WANTS Torkoal opened with Eruption.
3. Playbook: `design/TRAINER_FIELD_PLAYBOOK.md` §5 says Sahar has no cross-field transition because "Cinderglass needs
   searing Fire moves". A player's searing moves now make the Glass Dunes instead, where her quakes shatter the glass
   back into her Desert (her existing `[:DESERT, 1] => 22` want already rewards that).
4. Field per battle (my suggestion, set in the events): the gauntlets on 920 / 924 / 925 use the map defaults; the 926
   singles and partner doubles start on the map default DESERT; the legendary fight starts on DESERT and changes through
   the boss script and the moves (below).

**For the Bosses owner (`plugins/Prismfall Bosses`) and the story team: the war legendaries on 926.**
5. Neither war boss is registered yet. Two harness-only definitions in `tools/harness/run_glass_dunes.rb` show a shape that
   works: leave `:field` unset so the fight starts on 926's DESERT. **Reshiram** (the default fight): break 1 brings the
   flood in (`:field => :FLOODED_DUNES`, a flood message, optionally `:weather => :Rain`); with Blue Flare in its set the
   AI glasses the flood on its own (AIField scores it +16; AI vs AI it reached DESERT > Superbloom > Flooded Dunes > Glass
   Dunes). **Kyogre** (backing Ashkaar): Primordial Sea floods the dunes at send-out; the player's searing moves still
   glass it while snuffed. Balance note: on the flood in heavy rain Origin Pulse runs x1.95 before STAB (the AI-piloted
   Lv.85 Reshiram in the harness was one-shot), so tune Kyogre's level/EVs, or open its first bar with Drizzle (rain
   blooms the dunes; Origin Pulse then floods them) and save the Primal reversion for a later break, as `KYOGRE_ISENMAR`
   does.

**For the mapgen owner / map builder:**
6. `design/FIELD_DEFAULTS.yaml` now has **925: BLEED** (source: hand) and a new optional map key `borrow:` (read only by the
   field plugin's generator; `build.py` can ignore it). Please re-run `mapgen/build.py` so
   `maps_out/Plugins/Prismfall Maps/002_MapFields.rb` writes `MAP_FIELDS[925] = :BLEED`: `MAP_FIELDS` wins over the field
   plugin's defaults, so until then a game build still loads Cinderglass on the Steamline. 926 stays DESERT.

**For the world cartographer:**
7. `tools/worldmap/gen_docs.py` still gives 925 `field='ASHEN_WASTE'` (so maps.json and the WORLD.md table say
   Cinderglass). FIELD_DEFAULTS has `source: hand` on 925 and 926, so gen_docs won't overwrite them, but please change it to
   `'BLEED'` so the docs agree. WORLD.md's 926 note ("the flood-then-glass transition is the fields team's") is done.

**For the EBDX Bridge owner:** two new backdrop keys with no art (`field_flooded_dunes`, `field_glass_dunes`), the new
transition colours, and profile suggestions are in `design/FIELD_BACKDROPS_NEEDED.md` §1, §2, §4. `[:DESERT, :ASHEN_WASTE]`
is no longer used.

## From the trainer designer, round 3 (SPINE Revisions 16, 18, 19), 2026-11-20
Data: `tools/trainer_gen/gen.py` → `pbs/trainers.txt` (generator-exact, 0 validator errors). Win rates and the
Reborn / Rejuvenation calibration: `design/BALANCE.md` §1b and §9; per-fight notes: `design/TRAINER_FIELD_PLAYBOOK.md`.
No map file was edited.

**For the puzzle engineer (the Saltmere audience) and the field owner (`102_Field_GrandStage.rb`):**
1. **Yes, a bigger crowd should favour the player, and today it doesn't.** Dorian's team is the same at every stage;
   with the fans rule in, a realistic Standard six wins **43% (sparse) / 52% (good) / 45% (full)** with a Lv 15 team
   (50 / 52 / 37% in a second run) and 37 / 25 / 35% with a Lv 14 team (60 runs each, `tools/harness/run_winrates.rb` fights G1, G1S2, G1S3, G1L14,
   G1S2L14, G1S3L14). Casual wins 100% at every stage, Hard (realistic) 0–7%. What keeps the full house from paying off is the
   Standing Ovation **bask**: his whole troupe is Normal, so from turn 1 every one of them heals 1/16 a round.
2. **Proposal:** with your fans in (7+ met), the bask is for **your side only** ("the house cheers you, not him"): add a
   battler condition to the two bask rules at stage 3, e.g. `:condition => proc { |_bt, b| !($game_temp&.pf_home_crowd && b.opposes?) }`.
   Harness result (Standard, harness-only patch `PRISM_EXP_HOUSE=nobask`): **sparse 50 / good 63 / full 73%**
   (Lv 14 team: 37 / 37 / 43%), so the crowd you gathered pays off and the sparse house is untouched. If that is too
   generous, halving Dorian's bask with fans in (`halfbask`) gives 45% at a full house, about even with sparse. Giving the
   +1 crit stage to your side only (`crit`) adds little on top. I'd ship `nobask`.
   **DONE 2026-11-20 (`nobask`, approved by main):** both Standing Ovation bask rules carry
   `:condition => not_house_foe` in `102_Field_GrandStage.rb`, which reads `FieldEffects.home_crowd_foe?` (new, in
   Puzzles `007_Puzzles_SaltmereCrowd.rb`: `$game_temp.pf_home_crowd` set by `pf_house_rules` and the battler is on
   Dorian's side). Standard, Lv 15 team, 60 a cell: 43 / 52 / 45% → **48 / 73 / 58%** (180 a cell: 46 / 68 / 64%);
   Lv 14 team 22 / 30 / 32% → 25 / 48 / 37%. Good and full house come out about level. Docs: BALANCE.md §9,
   GYM_PUZZLES.md Gym 1, FIELDS.md, TRAINER_FIELD_PLAYBOOK.md.
   **Follow-up 2026-11-20 (main: the win rate must rise with the crowd):** good and full came out level (68 / 64%)
   because a good house also reaches Standing Ovation and Jigglypuff's sure Sing hurt most at a full one. Now: good
   house = Dorian's troupe basks at half at Standing Ovation; full house = only your side basks, only your attacks get
   the +1 crit stage, his Sing can miss (`FieldEffects.home_crowd_full?`). The crowd procs are `:ai_safe` (new matcher
   key: the AI's field scores may call them). Standard, 180 a cell: **45 / 63 / 73%**.

**For the field owner:**
3. **Water Surface ↔ Underwater loop:** Dive into Underwater and Dive back to the surface are both transform strikes
   (×1.3, and Dive is ×1.5 underwater): 103 knockouts in 60 Gym 3 runs came from it, so Marisol no longer has Dive.
   Suggest: the return trip is not a strike (or one strike per battle).
   **DONE 2026-11-20:** one-way. Dive now moves the battle on the turn it strikes (new transition key `:strike_turn`,
   Reborn's timing: one Dive = one change, not down-and-back-up in one use), diving down is the transform strike (×1.3)
   and surfacing (Dive, Bounce, Fly, Sky Drop) is not (`:boost => false`). Harness: `tools/harness/regressions.rb`
   (run_all section 4): Surface Dive 63 dmg with the strike vs 49 without; Underwater Dive 56 = 56; two Dives = down, up.
4. `FIELD_DEFAULTS.yaml` `exceptions.trainers`: the `OCTAVE_SINGER` v1–8 and `OCTAVE_VESPER` v2 rows are dead (retired
   versions); `OCTAVE_SINGER` v0 is Lyra now (the row's text says Carol; the field, Grand Stage, is right). The v60 bouts
   need no rows (the quest sets the field). **DONE 2026-11-20:** singer 1–8 and Vesper 2 rows removed, v0 texts say Lyra,
   `011_FieldEffects_MapDefaults.rb` regenerated (`--check` clean). In `012_FieldEffects_TrainerPlays.rb` (mine) I emptied `ENTRY_FIELDS`
   (only Vesper v2 used it) and added the war WANTS exactly as you suggested, plus the partners'.
5. The war teams are rebuilt for your sequence: Desert on 920 / 926 (rain → Superbloom → flood; two searing moves →
   glass; no quakes in the Ashkaar glass line), the Bleed on 925, Cinderglass on 924. Harness: with the WANTS the
   Ashkaar line glasses the dunes in 6–8 of 8 partner doubles and the Isenmar line floods them (and freezes the flood)
   in 6 of 8. Partner versions `LEADER_SIGRUN` / `LEADER_MARISOL` 19 need no `TRAINER_FIELDS` row (926 is Desert).

**For the map builder / story (the Battle of the Glass Dunes, Ch19, cap 85):** versions are encounter numbers.
6. Gauntlets: back Ashkaar → 920 the Rimed Sands: `ISENMAR_SOLDIER_M,Soldier,0`, `ISENMAR_SOLDIER_F,Soldier,0`,
   `ISENMAR_OFFICER,Captain,0`. Back Isenmar → 924 the Siege Camp: `ASHKAAR_SOLDIER_M,Soldier,0`, `ASHKAAR_SOLDIER_F,Soldier,0`,
   `ASHKAAR_OFFICER,Captain,0`. Stand between → 925 the Steamline: `ASHKAAR_SOLDIER_M,Soldier,1`, `ISENMAR_SOLDIER_M,Soldier,1`.
   926 crest singles: `ASHKAAR_SOLDIER_F,Soldier,1`, `ISENMAR_SOLDIER_F,Soldier,1`.
7. Partner double on 926 (map default Desert):
   ```
   pbRegisterPartner(:LEADER_SIGRUN, "Sigrun", 19)     # back Ashkaar or stand between
   setBattleRule("double")
   TrainerBattle.start(:ISENMAR_OFFICER, "Captain", 1, :ISENMAR_SOLDIER_M, "Soldier", 2)
   #   stand between: TrainerBattle.start(:ISENMAR_OFFICER, "Captain", 1, :ASHKAAR_OFFICER, "Captain", 1)
   pbRegisterPartner(:LEADER_MARISOL, "Marisol", 19)   # back Isenmar
   TrainerBattle.start(:ASHKAAR_OFFICER, "Captain", 1, :ASHKAAR_SOLDIER_M, "Soldier", 2)
   ```
   (Clear `$PokemonGlobal.partner` afterwards as usual.) The partners have one version only, the same ally in every mode.
8. The legendary (Prismfall Bosses, taken over at the coordinator's request; `106_Boss_WarLegends.rb`, `design/BOSSES.md` §4):
   `Prismfall::Bosses.wild_battle(:RESHIRAM_GLASS_DUNES)` by default, `:KYOGRE_GLASS_DUNES` if backing Ashkaar; then
   `Prismfall::Bosses.last_result[:result] == :turned_back`. No catch. Both start on 926's Desert; Reshiram's first break
   brings the flood-sea (and teaches Blue Flare, which glasses it), Kyogre's first break floods the dunes and the rain
   passes. **Origin Pulse balance:** no Primal form in the fight (Primordial Sea over the flood one-shot everything: Hard
   0 of 8 with it), Calm natures and HP / Sp. Def EVs; neutral hits now run 60–90% (results in the playbook §6).

**For the Eevee Octave workstream / Trials owner:**
9. Done: all Octave teams live in `gen.py` now (removed from `pbs/trainers_trials.txt`, a pointer comment left).
   `OCTAVE_SINGER,Lyra,0` (Eevee "Moss" 17) partners `OCTAVE_VESPER,Vesper,0` (Eevee "Amen" 18) in the Ch2 double; Vesper 1
   (Ch13) kept; **retired** Carol 0, the singers' 1–8 and Vesper 2. Duels (50) at your levels (next cap − 1: 18, 22, 26, 30,
   34, 38, 58, 88; partner one below, not on Casual), real level-legal sets. `GAUNTLET_VERSION` 60 and `HOST` unchanged.
10. **Gauntlet levels (please copy into EEVEE_OCTAVE.md §4): bouts Lv 87 (Hard 88, Casual 83), Vesper's Eevee Lv 89
    (Hard 90, Casual 85)**, down from 90 / 92; no bag of their own; Forte's Flareon is Guts (no Flash Fire stacking on
    Volcanic). Harness (a well-built Lv 90 six, Full Restores carried, no healing between bouts, 10 help orders): a player
    who leads each bout with the Pokémon that takes its type best clears it 9 / 10 (Standard) and 8 / 10 (Hard); an
    unplanned team 1 / 10 and 0 / 10; Casual 9 / 10 unplanned. Z-moves are two thirds of the knockouts, so the lead is
    the plan: hard, but fair to a player who reads the order they chose.
11. **The Little Crucible** (`AS_LITTLE_CRUCIBLE`, after Badge 2): Rekk / Vasha / Brakka re-levelled to the cap-23 band
    in `pbs/trainers_trials.txt` (Sizzlipede 19 / Carkol 19; Capsakid 19 / Houndour 20; Salandit 20 / Numel 20 /
    Fletchinder 21, Super Potion). The quest already unlocks at `badges >= 2`.

**For the Base Fixes owner:**
12. Gen 9 Pack `[003] Moves/[000] Move Functions.rb`, the Psycho Shift override (`GiveUserStatusToTarget`, ~line 27)
    calls `paldea_pbEffectAgainstTarget` with no arguments: an ArgumentError whenever Psycho Shift is used without
    Drowsy / Frostbite. It should be `paldea_pbEffectAgainstTarget(user, target)`. **DONE 2026-11-20:**
    `plugins/~Prismfall Base Fixes/003_Gen9_PsychoShift.rb` restores the arguments in memory as the file loads (the
    001 hook now takes a table of line patches; no base file is changed; the Renovation fork's 3.3.8 is already fixed and
    is left alone). `tools/harness/boot.rb` loads Base Fixes when a run folder doesn't link it, and run_all checks Psycho
    Shift with a burn, with paralysis and with no status (0 exceptions; without the fix: ArgumentError).

**For the distribution owner:** Tamsin's answer to the common birds is Dwebble (Smack Down grounds them into the silk,
Rock Tomb), not a new Flying weakness; the Little Crucible is in the 2-badge band; K1's Standard starter has no type
move (Reborn / Rejuvenation do the same), so the realistic upset rate is about one in six.

## From the Mega Evolution workstream (SPINE Revision 20), 2026-11-20
Design: **`design/MEGA_EVOLUTION.md`** (the lore, a study of how Reborn and Rejuvenation hand out Megas, the mechanics,
the Ring-Day, all 47 stones, who Mega Evolves, the tests). No map file and nothing in `pbs/trainers.txt` was edited.
New plugin `plugins/Prismfall Mega` (no PBS: the Mega Ring, the stones and the forms are base data). Trials data:
`114_Quests_Megas.rb`, `132_EventMons_Megas.rb`, `152_Talk_Megas.rb`, plus two rank rewards in `001_Trials_Config.rb`.
Tests: `tools/harness/run_mega.rb` 59/59, `run_trials.rb` still 142/142, and an engine capture
(`docs/battle_captures/mega/mega_evolution_ebdx.gif`).

**Map builder**
1. **`design/TRIAL_EVENTS.yaml`, section "Mega Evolution"** (42 new map blocks, plus one event added to 524 Gossamer Wood).
   - **25 Mega Stone events.** Each is one call, `{script: 'pf_mega_stone(:ITEM, "line")'}`, with the visibility
     condition `badges >= N && !has_item(:ITEM)` and self switch A. 14 are hidden (no graphic, Itemfinder target) and
     8 are visible (item ball). The other 3 are puzzle rewards (item 3).
   - Some sit behind HMs, as `near:` says: Rock Smash (577), Flash (605), Surf (680, 681), Dive (824) and Rock Climb (263).
2. **Quest NPCs and objects** (pattern as in 151/152: one `pf_trial_talk(:KEY)`):
   - **The Ring-Day:** Brann at the Hearthguild anvil (244).
   - **Story gift:** Juno under the Bride Tree (294).
   - **The doll quest:** the attic doll (547) and three buttons (546).
   - **The Old Pincer:** the Woodward (526) and the Pincer (703).
   - **The Matriarch:** the Matriarch on the Frostflat Causeway (560), with two or three young Kangaskhan as decor.
   - **Return to Sender:** the Postmaster (325) and three dead-letter doors (320/323/324).
   - **Old Cinder:** Tarn and Old Cinder (248).
   - **Bedside Manner:** Wenlow (223, page on S179 `WENLOW_ALIVE`), Corvin (223, only once S179 is off) and three ward beds.
   - **Dogs of the Moon Market:** Ottoline and three kennel cages (423).
   - **The Memory Kata:** Ottoline at the Last Rung (260).
   - **The tyrant's heart:** Nasrin (360) and the third vertebra (773).
   - **The Speculum:** Saffi and the third pane (346).
   - **Patches:** Dorian (154) and Sahar (209). Hesper (106) and the Crucible Legate (240) need nothing: their talk keys
     gained rows.
3. **Puzzle team (optional wings):** the Alakazite (Lucent Sealed Stacks, 345, "the Unread Shelf"), the Gardevoirite
   (the Looking-Glass Wood's mirror maze, 752) and the Metagrossite (Strade Works sorting line, 403) sit behind
   puzzles. Their events are in the YAML. The puzzle itself is yours to design (`note:` says the idea).

**Trainer designer** (`design/BALANCE.md` §6b has the full table)
4. **Megas from the Ring-Day (7 badges) on.** Most are Standard and Hard; a few are Hard-only or all difficulties.
   - Brann: Mega Camerupt "Kiln".
   - Kestrel K4–K9: Mega Scizor (his mother's ring).
   - Kaito: Lucario (Lucarionite on Standard now).
   - Juno: her starter's stone at J4/J7, none at J3.
   - Anja: Glalie, **Hard only**.
   - Odessa: Pidgeot "Post".
   - Ilsa: Alakazam.
   - Ysolde: Sableye on Standard, Gengar on Hard.
   - Magnus: Metagross. Nyx: Absol. Celestine: Mawile. Sigrun: Salamence. Valen: Gallade. Marisol v90: Gyarados.
   - **No one before 7 badges.**
   Add `MEGARING` to each trainer's Items and the new stones to `tools/trainer_gen/gen.py` `MEGA_STONES`.
5. **Brann's Mega Camerupt needs tuning.** In the engine run, a Lv 56 Mega Camerupt on Volcanic beat a Lv 60 Mega
   Charizard X and a Snorlax: each eruption gives +1 Sp. Atk, and the Mega primes one. Suggested set: one primer, plus
   Yawn or Will-O-Wisp.
6. **Three wild bosses guard stones** (`132_EventMons_Megas.rb`): Old Cinder (Charizard Lv 58, 11 badges), the Old
   Pincer (Pinsir Lv 62, 12) and the Causeway Matriarch (Kangaskhan Lv 78, 16 badges, 3 bars). None of them joins.
   Tune them with the rest.

**Z-Power owner**
7. **One Z-move per side** (SPINE Rev 20). `Prismfall Mega` alias-chains `PrismfallZ.owner_key` to the side
   (`PrismfallMega::Z_LIMIT`). No Z-Power file was edited. Please move it into your config (one line), and the alias
   can go. The tests cover it: two foe trainers with crystals get one Z between them, and a Mega plus a Z on one side
   both work.
8. **Proposal: a shared Mega/Z "power" button on EBDX's Fight menu.** This is also for the EBDX Bridge owner; details
   in MEGA_EVOLUTION.md §9.
   - Reuse EBDX's Mega button slot. It shows Mega or Z depending on the battler (a stone holder can't hold a crystal).
   - Action toggles it. In Z mode the move buttons preview the Z-move names and power, and the Yes/No box goes away.
   - Hook points: `FightWindowEBDX#megaButton` and the `-2` toggle in the Fight menu block. `after_register` reads the
     pending Z.

**Story editor**
9. **The Ring-Day (Ch8, Cindervault, map 244).** It plays the morning after the Caldera Crisis, before the Dominar's
   herald. The scene is written in `114_Quests_Megas.rb` (`AS_RING_DAY`) and summarised in MEGA_EVOLUTION.md §4.
   Lore to review (§1):
   - A Mega Stone is a "heartstone": an Imprint that pearls inside one line of Pokémon.
   - A Mega Ring is a Warden's ring: grind from the Crown's stone, kept by the Hearthguild each time the stone is reset.
   - One Mega to a side: two rings on one side ring against each other.
   - The PC's ring sings. This foreshadows the splinter and lands Brann's chestnut line.
   - Kestrel wears Morwen's ring; it answers him for the first time at K4.
   - Juno inherits Rowan's ring, which won't answer at J3 (the Heartgarden scene) and does at J4.
   - The Mourner wears no ring while masked; Rowan's ring is on his hand at the unmasking.
   - Hesper's lighthouse lens holds Morwen's old Ampharosite (3 badges).
   - Wenlow leaves the Audinite to the PC; after Ch16, Corvin hands it over.
   No new story flags (the conditions use `has_item(:MEGARING)` and `made(:ch8_caldera)`).

**Trials owner**
10. My quest ids avoid your stubs: `AS_DRAGONSWORN` and `OS_BONEWRIGHT` stay untouched, and mine are `AS_BRAZIER_WRIT`
    and `OS_TYRANT_HEART`.
    - Rank rewards aren't badge-gated, so only Manectite (Zenith rank 3) and Sharpedonite (Isenmar rank 3) went into
      `RANK_REWARDS`. Both are reachable before the Ring-Day and safe at 7 badges.
    - Later "rank rewards" are commissions with `:rank => 2` plus a badge unlock (Mawilite, Tyranitarite, Salamencite,
      Lucarionite). Raise their `:rank` as more quests are wired.

**Field workstream:** nothing in `plugins/Prismfall Field Effects` was edited.
- `Prismfall Mega` fires a field's ability-keyed `:on_entry` rules for the ability a Pokémon gains when it Mega Evolves
  (it was an integration gap; Reborn does the same).
- It adds eight Mega showpieces (Grand Stage, Volcanic, Colosseum, Frozen Lake, Crystal Cavern, Hollow Cathedral,
  Factory, Bleed) and appends Field Notes lines through an alias on `FieldNotes.effect_lines`.
- When FIELDS.md is next generated, please include `PrismfallMega::FIELD_NOTES`.

**Bosses owner (proposal):** add an optional `:mega => true` break effect, so a trainer boss Mega Evolves when its first
shield breaks (Rejuvenation's Latios in its second bar). Wild bosses can't Mega Evolve in Essentials.

**Packaging:** add the new folder `plugins/Prismfall Mega`. `tools/package.sh` already copies `plugins/` wholesale.

## From the story editor (Ch1 close, the Ring-Day, Gym 2 lines), 2026-11-20
**Map builder (Ferrow's Landing 100/104, the Ferrymen's Mile 520, Hale Farmhouse 523).** Chapter 1 now closes with a
night at the Hale Farmhouse. The real lines replace your placeholders; they are all in `story/20_SCRIPT_CH0-2.md`
(search for the headings in quotes). This also fixes REQUESTS items 15–16 above (the Hale Bell leak, no send-off).
1. **"Biscuit comes home"** (Map 523 section; Wenna, first talk after S105). It is the same scene at her quay stall on 100,
   and both share the existing `[[523, 0, 'BISCUIT']]` self switch. It pays the 3 Oran Berries, completes "Biscuit", and
   has Wenna's offer of the night, Juno's hayloft lines and Coll's goat line. It ends with OBJECTIVE: "Sleep at the
   Hale Farmhouse." Wenna's and Coll's repeat lines are right under it (after S105, V102 < 2).
2. **BED (action, after S105 and V102 < 2)** on 523: a Sleep / Not yet choice. Sleep plays Juno's goodnight from the
   hayloft, heals the party, then plays the existing "End of Chapter 1" night cutscene (which sets V102 = 2). Before S105,
   the bed stays a plain heal.
3. **"The send-off"** (Chapter 2 start; 523, autorun when the night cutscene ends, V102 = 2, once). It gives the TOWN MAP,
   the "Eighteen Roads" quest and Juno as follower. It **replaces `SENDOFF_520`** (Larch at the stile, `routes_early.py`).
   Larch now walks in to the breakfast table, so retire the stile event, or keep it only as a fallback that runs if
   `:ch2_sendoff` is unset. Keep `pfm_set(:ch2_sendoff)` at the end of the new autorun.
4. **The Hale Bell barrier (520)** stays shut until V102 >= 2 (not S105). Its guard has two pages in the script's
   "Accord guard" block: before the send-off, a first-light curfew line plus one extra line after S105 that sends the
   PC back to the Hales; after the send-off, the existing pass lines. Please also close the gaps from item 15 (edge
   tiles (0,72)–(0,75)).
5. **Tidewater Inn (104):** one Innkeeper line after S105 and before the night, which sends the PC up the lane. The inn
   no longer ends the chapter: there is no inn bed.
6. **The Hale Bell (520), action:** Juno's second line changed ("He's never untied a knot in his life...").

**The Ring-Day (Ch8; review of the Mega Evolution workstream's item 9 above).** *Withdrawn by SPINE Revision 21 (the ring comes after Badge 13): **don't build items 8 and 9**. Item 7 (Kestrel) and item 10 (ring lore) still stand, wherever the scene moves.* Script: `story/22_SCRIPT_CH8.md`. The
plugin strings in `114_Quests_Megas.rb` now match it (string edits only; `run_trials.rb` 142/142).
7. **Trainer designer: no Kestrel Mega at K4–K7** (this replaces "Kestrel K4–K9: Mega Scizor" in item 4 above). His
   mother's ring is the Key Item **Morwen's Ring**. Edda holds it until Ch15 (07_ACT_IV), and it reaches Kestrel only
   through the PC (`:ch18_kestrel_ring`). Give him `MEGARING` at K8/K9 only when `choice(:ch18_kestrel_ring) ==
   :give_now` (BALANCE §6b row updated). Nothing to undo: there's no Kestrel Mega in `pbs/trainers.txt` yet.
8. **Trials owner:** add one `:if` entry to `AS_RING_DAY`, after the three caldera branches:
   `choice(:ch8_lightstone) == :dominar` → `[:BRANN, :sad, "And the Light Stone... no. Not today. Today I'm in a good
   mood, and I'm keeping it."]`. Also add Larch's idle line by the door (in the script).
9. **Map builder (Cindervault):** the morning after the Caldera Crisis, Larch at the inn sends the PC to the Hall ("Brann
   wants you at the Hall. He's sober. It's unsettling."). The Dominar's herald (the Ch8 cliffhanger) should wait for
   `quest_done(:AS_RING_DAY)`, so the ring always comes first.
10. **Mega Evolution workstream (lore, for your §1):** Brann names neither the Legend Plate nor the reset in Ch8 (those
    are 09_MYSTERIES #5/#6, Ch15–17). The PC's ring is the odd one out: he cut it ten years back, from the AF 290 grind.
    Rowan's ring went into his sealed testament before he first wore the mask; Juno gets it with the seat in Ch10.
    MEGA_EVOLUTION.md §1, §4 and §6 are updated.

**Gym 2, the Canopy (130/131; `gen_loomhouse.py`, `puzzles/canopy.py`, `layouts/story_early.py`).** The script is now
`story/21_SCRIPT_CH3.md` Maps 130 and 131, and it matches what you built except for these lines:
11. **130 lobby:** rename "Weaver Pim" to **Weaver Tibb** (Pim is the net-minder upstairs; there can't be one Pim in two
    places). Add a fifth Gym Guide line: "Old Mother Loom never once went up there. Said the Bugs had better hands than
    hers. Tamsin added the safety nets. And the apology cards."
12. **131 Tamsin, before the battle:** her first and last lines change, because "Granny Loom wove this room" contradicts
    "the webs up here, the Bugs wove". The new lines: "Gran wove the looms downstairs. She never came up here. She said
    the Bugs had better hands than hers, and she was right." ... "But I can hold a thread. So can they. We spun this
    whole hollow together, the Bugs and me. Don't you dare tear it." Her win line: "That's allowed. Gran said a good web
    always leaves one way through, for the right one. I didn't think I'd ever meet one."
13. **131 confession stage line:** "(The Warden's loft, high in the elder above the webs: ...)" instead of "The loft
    above the hall" (there's no hall now).
14. **131 Joltik:** "The Joltik sparks! The charge runs the whole gold/blue strand, and every web hanging on it flips:
    slack snaps taut, taut sags slack." The built line says "webs A and B", letters the player never sees, and "the taut
    one... the slack one", which isn't true at the start (all three are slack).
15. **Pim (`canopy.py` ROOMS hints[2]):** "Spark both Joltik, once each: the one on the third ledge and the one on the
    west perch. Then the bottom web throws you up, the middle one holds you, and the top one throws you across to
    Tamsin." The current hint says "the Joltik on this ledge", but Pim stands on the floor. There's also an optional
    reset line in the script.
16. **131 Juno, repeat line:** "(a whisper you can hear from the top of the tree) GO ON, \PN!"
17. **121 (Briarwick interiors) "Trainer":** still describes the retired heddle hall ("planks and looms... the floor
    leaves"). New line: "The gym's all webs. Step on the wrong one and it throws you into the net. Tamsin apologises to
    you all the way down."

**Sweep (Gym 1/2 swap, Geography v2, the land war).**
18. **Applied for you (strings only, keys and logic unchanged; `ruby -c` and `run_trials.rb` pass):** items 6–8 of "From
    story editor (geo v2)" above. Core `012_Narrative_Data.rb` (`:war_warning`/`:war_convoy`/`:war_prisoner`/
    `:war_climax` descriptions now match NARRATIVE_KEYS; no more "Marisol's fleet" or "Shattered Ice"), Core
    `015_Festival_Draw.rb` ("opposite sides of the Steamline"), and Trials `120_Quests_Catalogue.rb` ("The Saga of the
    Glass Dunes"; the key `IS_SAGA_OF_THE_ICE` stays). TRIALS_QUESTS.md has been regenerated.
19. **Cartographer (`tools/worldmap/world_data.py` → maps.json, PLACE_NAMES.md):** 130 is still "Loomhouse Gym - Foyer",
    131 "Loomhouse Gym - Weaving Hall" and 133 "Loomhouse Gym - The Spindle". The built names are "Loomhouse Gym - Lobby"
    and "Loomhouse Gym - The Canopy" (`gen_loomhouse.py`), and 133 is retired (GYM_PUZZLES §133). Please rename them and
    mark 133 as unbuilt.

**Portrait use (coordinator ruling, 2026-11-20; `story/13_CUTSCENES.md` "Portrait use").**
20. **Map builder:** portraits are for named story characters only, on their first line in a scene and where the
    expression changes (plus comedy beats with an emote). Other lines get a name box. In `20_SCRIPT_CH0-2.md` and
    `21_SCRIPT_CH3.md`, a portrait character's repeated same-expression lines are now `[name: X]` (58 and 6 lines). When
    you rebuild those events, put `\pf[...]` only where the script has a portrait tag. Generic NPCs, trainers and signs
    never get one, and none of the scripts give them one.

## From map builder 10 (2026-11-20)
**Doors and warps that moved** (links unchanged; build.py checks every arrival and seam):
- **541** mine back door `R4_MINE` -> **(52, ~35)** (on the Brinecut lip); Brinewife's Rest `R4_REST` (12,58).
- **540** mine mouth `R3_MINE` -> **(9, ~25)** (the west outcrop); manor `R3_MANOR` -> the sh_big front on the h2 terrace.
- **524** Woodward's Hut `WOOD_HUT` -> **(70,51)**; `WOOD_DEEP` (89,48), Cut tree (82,48), Briarwick warps (44-46,0) and
  the south warps (40-42,109) unchanged. **520**: events re-seated; the Hale Bell barrier is now at **(2,72)-(2,75)**.
- **Ebbmouth 160 rebuilt** (60x54, PF Rejuv Snow): PC (7,20), Mart (14,21), Anglers' Guild (9,35), Reyes House (6,8),
  Net-mender (14,8), Tidelock Gym `EB_GYM` **(46,13)**, Net Loft (52,26). HealingSpot **[160, 7, 21]** (161 spec and
  `pbs/town_map.txt` updated). S edge to 561 unchanged (x 20-23); **new N edge to 167 Mill Quay** (towpath x 28-31).
- **New maps:** 167 Ebbmouth - Mill Quay (40x30), 568 The Rehearsal (34x26, `:BLEED`; warp `R5_REHEARSAL` from 560 (30,29)
  to 568 (16,0)), 143/144/145 rebuilt (145 Pageant Hall is a real theatre now, tileset 54; exits `SM_PAGEANT` at (18-19,24)).
- **548 Cocoonfall Hollow:** the Matriarch's nest moved north to **(19,5)** behind the new glass ravine (rows 9-10).
**New data:** tileset **56 "PF Rejuv Shore"** (install with merge_tilesets like 50-55); flags **V601-604** (road
mechanics) and **V536 `D8_FRAME`** (the Rehearsal); `build.py` page keys `route:`/`speed:`/`freq:` (custom move routes) and a
spec key **`gates:`** (a story gate must really be shut; `--strict` fails on a leak). New art: `art/imports/` (J-Treecko252
crystals, x2, credited), pieces `cr_*`, `bl_veil*`, `bl_gust*`, `pf_wagon`, `eb_wheel0/1`, `eb_intake` (ndraw.py).

**For the puzzle engineer:**
- **Item 17 done:** 525's "Crystal silk" gate is the `pf_silk_curtain` charset (solid) in `layouts/old_525_wilds.yaml` (the
  reskin source); the north-east pocket's terrain is untouched.
- **Item 18:** 562 not touched. **Item 19:** 524's one-tile pinch points for the silk curtains: **teach (28,12)**, **twist
  (21,86)** (`routes_craft.build_524` keeps them 1 wide).
- **Item 20 done, and wired:** 548's ravine is rows 9-10 across the crater; crossings **a (28,9-10)** NE cocoon-house,
  **b (10,9-10)** NW Shard house, **c (19,9-10)** the nest. I laid D3 per DUNGEON_PUZZLES so the story isn't blocked:
  bridge events (tile 17743 while S511/S512/S513 or S107), anchors 1-3 at (8,22)/(16,22)/(24,22) flipping a+b / b+c / a+c
  (needs the Shuttle or `:ch2_tamsin`), and a first-entry autorun setting a and b taut. Replace them with yours if you
  prefer (same names: "Bridge a 1".., "Anchor 1"..), and please add the built-map proof.
- **D8 (568) built** with the design's frame rule: `D8_FRAME` (V536) is a step clock (`pfp_step_hook(568, :rehearsal)`
  from the map's parallel event), the Tauros and driver show one tile per frame (touch: "You pass through the moment..."),
  gust walls x 23 (even frames), x 26 (odd), pier rows 22 (even) / 24 (odd). TM10 (31,9), Bleed Shard #3 (pier end, a
  `pfm_set(:bleed_shard_3)` object: no shard item exists yet). `gates:` proves the TM is shut at frame 0; a rhythm proof is yours.
**For the playtest:** items 15-16 fixed: the barricade spans the road at x 2 with woods on both sides to the edge; it
opens on V102 >= 2. `build.py` prints `GATE ok 520 Hale Bell roadblock`; `tools/harness/playtest/seam_check.py` has
`--events` (first-page blockers stand solid): `520 527 16 108 --events` shows all four W-edge tiles NOT reachable.
Item 12: the stale J1 copy is gone from `layouts/saltmere_events.yaml`. The arrival text is narration now; the 140 east and
west edges have a green verge / salt-crust verge and hedges instead of buildings flush to the edge; 528 has gateposts and
drystone wall ends at the East Gate.
**For the story editor:** Ch1 close built from your script (523 "Biscuit comes home", the bed, the send-off at the
breakfast table with the Town Map and "Eighteen Roads"; the 520 guard pages; the Innkeeper on 104 (no inn bed now); the
Hale Bell's new Juno line). The stile and Hale Bell send-off lines on 520 stay only as fallbacks behind `!pfm?(:ch2_sendoff)`.
Not done: Juno as follower (no follower call exists yet), Coll's yard repeat line (no Coll event on 521), the 100 quay-stall
copy of the Biscuit scene, and items 11-17 (Gym 2's lines are the puzzle engineer's maps). I rewrote four scene-setting
parentheticals that read like stage directions as prose (528 the Beacon and the barge, 552 the Dyers' Ford, 541 the
Saltings): your scripts keep the parenthetical form, so those lines now differ from the script on purpose.
**For the distribution agent:** Spinners' Rise Ram Race sets `pfm_set(:ram_race_won)` (a Skiddo after Badge 3 can key on it).

## From the fields / balance pass (trainer designer's hand-offs 1–4 and 12, Gym 3, Picnicker Ada), 2026-11-20
No map file was edited. Done here (details in the items above and `design/BALANCE.md` §9): the Saltmere crowd rule
(Dorian's troupe doesn't bask when your fans are in), the Psycho Shift crash (Base Fixes 003), the Dive loop (one-way
strike, `:strike_turn`), the dead Octave rows, and Gym 3 for a Fire starter.

**For map builder 10 (one request, Rimewood Glade 563):**
1. **Gym 3's earned Electric answer.** `pbs/encounters.txt` gives the secret Rimewood Glade (563, behind the Cut sapling) a
   **LandNight** table: the day species plus **Emolga 5% (Lv 17–19)** and Joltik 3% (the 8% cap for Marisol's answers).
   It uses the glade's existing grass, so no tiles are needed, but the player should be told it is there. Please change
   Ranger Sigurd's `after:` line in `layouts/rimewood.py` (563) to something like *"...So you cut your way in. Fair.
   Stay till dark if you've the nerve. Something glides between the boles up here, and it crackles."*, and, if you have
   a spare villager, one rumour in Frostwick (570) or at the trapper's lean-to (562): *"Lights in the Glade after dark.
   Flying squirrels, my gran said. Shocking little things."* Nothing else changes on the map.

**For the trainer designer:**
2. Harness cells added to `tools/harness/run_winrates.rb`: `G3E` (a team that found the Glade's Emolga; Fire starter
   42% on Standard, 0 of 20 / 2 of 60 without it), `ADA` / `ADA1` (Picnicker Ada vs a sensible Ch1 player / the starter
   alone), `PRISM_FORCE=SPECIES` and `PRISM_STARTERS=Fire`. The prepared Ch4 list leads with Emolga now. Lucky (Gym 3)
   could have Dive back now that the loop is gone; I left the team as it is.
3. Picnicker Ada needs no change: a sensible Water-starter player wins 87% on Standard (alone: 50%).

**For the playtest:** Psycho Shift no longer crashes a battle (Base Fixes 003); Ada is a wall only for a team that never
heals or catches a bird (`BALANCE.md` §9).


## From map builder 10: the war theatre (2026-11-20)
**Built (`layouts/war.py`, PF Rejuv Shore + the war kit `wr_*` in ndraw.py):** 920 The Rimed Sands, 924 Ashkaar Siege Camp,
925 The Steamline (`:BLEED`), 926 The Glass Dunes, 928 the Command Pavilion (interior, tileset 54), 929 The Observers'
Mesa, 930 The Bone-Carters' Camp. **Not built:** Skaldfast 921-923 and Cinder Cape 927 (920's W road ends at a siege
barricade; 924's E war road at a guarded barricade; 930's E road to the Dry Tide 810 is open but unconnected).
**Graph:** 920 E <-> 925 W; 925 E <-> 924 W; 925 S <-> 926 N (the crest, x 28-31); 930 W <-> 926 E. Warps: 920 S (8,35)
`WAR_RIMED_DUNES` 926 (7,1); 924 S (8,39) `WAR_CAMP_DUNES` 926 (51,1); 924 war-tent door `WAR_TENT` 928 (11-12,16).
926 (30,46) "Goat-path" -> 929 (17,26) after `pfm?(:war_battle_done)`.
**Ch19 wiring (trainer designer round 3, items 6-8):** switches **S605-607 `WAR_SIDE_ASH/_ISE/_MID`** mirror
`pf_choice(:war_climax)` (each war map's "War front" parallel event). Gauntlets: 920 Isenmar M0/F0/Captain0 (back
Ashkaar, one per trench-line sally port); 924 Ashkaar M0/F0/Captain0 (back Isenmar, the two earthwork gates and the
war-tent); 925 Ashkaar M1 + Isenmar M1 (stand between). 926 crest singles (Ashkaar F1, Isenmar F1, every side). 926
"Partner" (30,4): Sigrun 19 vs Isenmar Captain1 + Soldier M2 (back Ashkaar) or both Captains1 (stand between); Marisol 19
vs Ashkaar Captain1 + Soldier M2 (back Isenmar); `pbDeregisterPartner` after. 926 "The legend" (30,2), after the partner
battle: `Prismfall::Bosses.wild_battle(:KYOGRE_GLASS_DUNES)` if backing Ashkaar else `:RESHIRAM_GLASS_DUNES` (skipped when
`:war_legend == :neither`); on `:turned_back` it plays `Prismfall::Cutscene.play(:WAR_CLIMAX)` and sets `:war_battle_done`.
The crest is reachable only from the Steamline: `gates:` proves it (`GATE ok 926`).
**For the story / cutscene owners:** the choice itself (`:war_climax`) and `:war_terms` are not asked on these maps (your
scenes); 928 has anchors "Dominar Hrothgar" (the petition, `:ch19_dominar`) and "Anja (cage)" (`:war_prisoner`) with
placeholder lines; 926's "Caravan well" is the exchange site; 930's "Elder Ossa" is the elder's quest giver (lines only).
WAR-1's stage picture (`Graphics/Pictures/pfw_glass_dunes.png`) is still the composed one: export 926's render if you
want the real map behind the scene (the crest is x 18-42, y 0-14; Isenmar west, Ashkaar east).
**For the sprite artist:** the war classes use base-project stand-ins (`war.py` SPRITE): Isenmar soldiers = Pokémon
Ranger M/F, Isenmar Captain = Cool Trainer M, Ashkaar soldiers = Black Belt / Crush Girl, Ashkaar Captain = Tamer, Sigrun =
Lance, Marisol = Misty, the Dominar = Giovanni. Overworld charsets for the real classes are wanted.
**Also (fixes agent, Emolga):** Ranger Sigurd's after-line on 563 now points at the night glade; Frostwick (570) has the
rumour ("Old woman by the brazier").
**Note for every layout author:** a priority-0 decal on the top layer over a solid prop makes the prop walkable (Essentials
reads the top tile first). `war.py decal()` and 568's veil now skip props; check your own decal passes.

## From the Mega Evolution workstream (SPINE Revision 21: the late Ring, Megas from Lv 50), 2026-11-20
Supersedes the Rev 20 entry above where they differ (its items 1, 2, 4, 5 and 9) and the story editor's Ring-Day items
7–9. Design: `design/MEGA_EVOLUTION.md` (§1 rings, §4 the new Ring-Day, §5 stones and what moved, §6 who Megas, §8
tests and win rates); trainer table also in `design/BALANCE.md` §6b. No map file was edited.

**Map builder**
1. **The Ring-Day moved to Cragholm** (13 badges): new event `BASTIAN_LAMPROOM` on **363 Cragholm - Lift Galleries**
   (Bastian in his lamp-room at the bottom of the lowest gallery; Pip on a crate and Larch by the door while
   `badges >= 13 && !quest_done(:OS_RING_DAY)`). Order in Ch14: Gym 13 → this scene → Larch takes the badge case apart →
   the raid. If you built the Ch8 pieces (Rev 20 item 2's Brann Ring-Day, the story editor's item 9 inn nudge), drop
   the Ring-Day part: Brann's Hearthguild event (244) now only carries his spare heartstone at 15 badges.
2. **Stone events moved** (`TRIAL_EVENTS.yaml` "Mega Evolution"). Remove, if built: 577 Frostwick Pass (Absolite), 605
   Static Tunnels Depths (Steelixite), 680 the Rootdeep (Swampertite), 685 Grudgestone Quarry B1F (Sablenite), 705
   Frostfang Pass 2F (Glalitite), 726 Cloudstair Summit (Charizardite Y). Add: 801 the Slag Mesa (Absolite, 14), 804
   Barrow of the Wardens (Sablenite, 14), 424 Underveil Sump Docks (Sharpedonite, 15), 821 the Drownings (Swampertite,
   15, Surf), 832 the Brink (Charizardite Y, 15), 864 Wyrmscar Rift (Steelixite, 17). Same one-call pattern.
3. **Conditions changed:** Corvin's gift on 223 is now `badges >= 18` (Bedside Manner is post-game); Old Cinder (248)
   opens at 15 badges and is Lv 72. Notes on 223, 244, 248, 325 and 547 give the new badge counts.

**Story editor**
4. **The new Ring-Day scene** (Ch14, Cragholm; lines in `plugins/Prismfall Trials/114_Quests_Megas.rb` `OS_RING_DAY`,
   summary in MEGA_EVOLUTION.md §4): Bastian gives the PC the odd ring Brann cut "ten years back" ("He sent it to me in
   a sock... 'It sulks. Keep it where nobody asks questions.'"), plus the Aggronite. The ring sings; Pip hears it,
   half-deaf Bastian feels it in the table; Larch lowers her book. No "reset", no Legend Plate (checked by run_mega.rb).
   Brann isn't in it, so the Light Stone choice doesn't touch it. Please write it into `story/07_ACT_IV.md` Ch14 (after
   Gym 13) and a script file if you keep one per chapter; `22_SCRIPT_CH8.md`'s withdrawn scene can point there; RD-1
   in `13_CUTSCENES.md` becomes the lamp-room (lamplight on the chip instead of forge-light); 09_MYSTERIES #1's
   "Ch8: the ring sings" clue is now Ch14.
5. **Brann's follow-up, 15 badges** (`AS_FORGE_REMEMBERS`): he knows his ring on the PC's hand ("That's my ring. The odd
   one. So old Ore finally gave it away"). **If `choice(:ch8_lightstone) == :dominar` he's hurt:** "I haven't forgotten
   the Light Stone, mind... I'm not going to talk about it." Then the Cameruptite and "Your ring still singing? ...No.
   Don't tell me."
6. **Kestrel** (the user: "dont make one off exceptions, keep it in theme/story"): **no Mega and no borrowed ring
   before Morwen's Ring reaches him.** If the PC gives it to him in Ch18, it answers him the first time he wears it:
   his K8 Megas his Scizor (`PrismfallMega::MORWEN_RING`, automatic at battle start). A `megaOpp` line for it: "Mum.
   Just this once. Answer me." Given at the SF instead, it first shows in the hijack tag battle (player's side). K9
   (fallen) has no Mega. (This replaces the coordinator's earlier "Meridian band from K5" idea; nothing was posted for
   it before this entry.)
7. **Juno:** the Heartgarden scene (9 badges) no longer says "Yours sings": the PC has no ring yet ("It hummed when you
   sat down, though. The stone, I mean."). At J4 Rowan's ring (hers with the seat) answers her and she Megas a
   **Gardevoir "Veil"** (it replaces Comfey). Please give her the Gardevoir somewhere between Ch11 and the Festival
   (Ralts are wild from 11 badges), ideally with a veil line.
8. **Who has a ring** (MEGA_EVOLUTION.md §1.2): Wardens (Accord officers), Valen, Juno, and Meridian's own people (Voss,
   Quent, Marchetti, Kroll, the Directorate Captain) on Lattice-glass keystones Meridian makes itself. **No ring, so no
   Mega** (§6.3): the Mourner and Rowan (his ring is in the testament, then Juno's), Archseer Imre Dask, Morwen's Echo,
   Theodric, the war officers. If the story would rather give any of them a ring, tell me and I'll add the Mega.
9. **Meridian's keystones** need one line somewhere before Marchetti's Ch12 fight (her Mega Manectric is the first
   Meridian Mega), e.g. a Larch or Rook remark that Meridian "makes its own heartstone keys out of Lattice-glass".
10. **Quests moved by badge** (rule R4 with the ring at 13): The Doll Who Waited and Return to Sender at 14, Old Cinder
    at 15 (its rider now died "on the Rimed Sands"), Bedside Manner post-game (18).
11. **SPINE Rev 21 text** still says "Nobody uses a Mega below that, which retires Brann's Gym 7 Mega Camerupt"; the
    user's amendment ("he could have one as long as its considered 'Weak'") is what's built: Brann (Gym 7) has a weak
    Mega on Standard and Hard (MEGA_EVOLUTION.md §6.1). The Mourner has none (no ring in the story, §6.3). [main, fixed] **Brann's fight is kept exactly as
    designed, per the user** (his set, Mega Camerupt, the Volcanic prime and its Sp. Atk boost): the Rev 20 entry's
    item 5 ("Brann's Mega Camerupt needs tuning") is withdrawn.

**Trainer designer (FYI, done in `gen.py`):** every Mega in BALANCE §6b; replaced slots and Casual cuts as listed there;
from K7 Kestrel's Mismagius takes Krookodile's place (so the Scizor stays for K8) and K9's Genesect takes Staraptor's.
Imre Dask's Rev 20 Hard-only Mega Sableye is removed (no ring in the story). Brann's team is untouched apart from the
stone. Garret's v1 cameo (ace 46) no longer Megas. No other balance changes. `run_winrates.rb` has prepared-team cells
G7, G10, M12, K5, G11 (`PRISM_PREPARED=1`) and `PRISM_FOE_NOMEGA=1` for the same fight without the foe's Mega; numbers
in MEGA_EVOLUTION.md §8.

**EBDX Bridge / battle speech (optional):** a `megaOpp` line per Mega fight (examples in MEGA_EVOLUTION.md §6.2).
**Field Effects owner:** nothing new; no field file changed.

## From the story editor: reply to the Mega Rev 21 entry, and SPINE Rev 22 portraits, 2026-11-20
**Mega workstream (items 4–9 done).**
1. **The Ring-Day** is written in `story/07_ACT_IV.md` Ch14, after Gym 13 and before Larch and the raid. Its lines match
   `OS_RING_DAY`. RD-1 in `13_CUTSCENES.md` is the lamp-room now, and 09_MYSTERIES #1's ring clue is Ch14. The withdrawn
   Ch8 versions (05_ACT_II, `22_SCRIPT_CH8.md`) point there.
   - **Strings polished in `114_Quests_Megas.rb`** (strings only; `run_trials.rb` passes).
   - Bastian's "You'll have been wondering what my old Amber did" read as the PC's first Mega, but by Gym 13 the PC
     has faced one in every gym since Rimeholt. It's now "You'll have seen a few of those by now. Anja's Glalie.
     Odessa's bird. That Directorate woman's dog. My old Amber, just now. Nobody's told you properly...". Brann is left
     out because Casual has no Camerupt.
   - "If Meridian's linesmen come down my lifts" is now "If the Directorate comes down my lifts": it's Marchetti's raid.
2. **Brann's forge** (15 badges) is written as an optional thread at the end of 07 Ch16; most players meet it on the
   Ch19 road. Two string changes:
   - The Light Stone line is now tighter and quotes the PC: "'It's his people's,' you said. ...No. I'm not going to
     talk about it."
   - "The one that tried to erupt on you" assumed the PC fought Kiln, who isn't on Casual. It's now "If you've met her,
     you remember her. She likes to erupt on people."
3. **Kestrel K8** (08_ACT_V): his Scizor Megas only with Morwen's Ring (*give_now*). His line is "Mum. Just this once.
   Answer me." Otherwise there's no Mega, and Fallen never has the ring. 10_CHOICES and the Ch18 give-now bullet say so.
4. **Juno's Gardevoir "Veil"** is introduced in 06_ACT_III Ch13. A Ralts has hidden in her blossom veil since the
   Antumbra Threshold, and she keeps it the night before Rowan's tribunal, in the Athenaeum's cloister garden. At J4,
   "...Oh. There you are." when Rowan's ring answers her. 03_CAST swaps Comfey for Veil.
5. **Meridian's keystones** line (Larch at the Gale Post, Ch12, before Marchetti's raid): "See the steel bands on their
   wrists? Lattice-glass. Meridian can't buy a Warden's ring off the Hearthguild, so it grows its own keystones...".
6. **Two small errors in your docs:** this entry's item 11 says the Mourner has a weak Mega, but §6.3 and
   `pbs/trainers.txt` say he has none (correct: no ring). MEGA_EVOLUTION.md §1.2 says Kestrel's Scizor dates from K3;
   the trainers file has it from K4 (v40).

**Map builder.**
7. **Ch13, Lucent:** one Juno event in the Athenaeum's cloister garden for the Ralts scene (night, before the tribunal;
   06_ACT_III).
8. **Ch12, Skyreach:** Larch's keystone line in the Gale Post sorting halls, before the raid.
9. **Ch14, Cragholm:** optionally, Pip fetches the PC to the lamp-room after Gym 13 (07_ACT_IV).
10. **Speech bubbles (SPINE Rev 22) are now marked per line** with `[bubble: NAME, expression, emote]`. Build them as
    `\pfb[NAME,expression,emote]`. So far: Larch's "IT LIVES IN A TREE" (Ch1), Wenna's "That's MY line." (the
    send-off), Juno's "GO ON" (131 repeat line), Bastian's "Pip! Those are the ginger ones!" (15_COMEDY Ch14).
    Everything else from the cast is a face (`\pf[...]`, first line and expression changes).
11. **Not in CAST, so plain:** Coll (the scripts are now `[name: Coll]`), the cameo Shelly, and generic officers.

**Cutscenes owner (`014_Portraits.rb`).**
12. Please add **WENLOW** to `Prismfall::Portrait::CAST`: a named story character, the player character of Interlude IV,
    with face tags in 15_COMEDY.

## From map builder 11 (2026-11-20)
**Done:** Juno follows on the script's three legs (`mapgen/ruby/010_JunoFollower.rb`, MAPGEN §2n); Wenna's quay stall on
100 plays "Biscuit comes home" (shared BISCUIT self switch); Coll's yard line on 521; Parsnip the Skiddo (521 yard, the
523 doorway at the send-off); story editor items 11-17 (Gym 2 lines) and 19 (130 Lobby, 131 The Canopy, 133 retired);
the passability guard (`passguard.py`, `PASS` in `--strict`, 99 cells fixed); the Glass Dunes kit (`gdraw.py`) and the
war theatre rework (926 rebuilt, 920/924/925/929/930 densified, 928 furnished; green rims gone on every war map).
**For the cutscene / portrait owner:** `010_JunoFollower.rb` wraps `Prismfall::Portrait.speaker` (guarded by
`defined?`): a `\pf[JUNO,...]` line with no Juno event on show points at the follower. If you move `speaker`, keep a
`speaker(spec)` method or tell me. Talking to the follower does nothing yet (no common event); a CommonEvents entry for
Juno's idle lines would be the next step if wanted.
**For the story editor:** Juno's follower legs are exactly the script's "(Juno becomes a follower.)" / "(She stops
following.)": the 100 errand -> the 522 gate (she waits there while you are inside; after Lecture One she falls in
again) -> the 523 bed; the 523 send-off -> the 140 arrival; the 140 chapter close -> the 120 arrival. 926 has new
flavour objects (the frozen wave, the causeway, a steaming pool, the broken trebuchet, two stragglers): lines are mine.
**For the playtest:** please walk 926 with the Ch19 states: the crest is still proved shut from the flats (`GATE ok
926`), the blue camp is reached by the sally-port causeway, the lookout ridges by their stairs.
**Mega Evolution Rev 21 (coordinator item):** no Mega Stone event exists on any built Chapter 0-4 map (the lowest stone
needs 8 badges), so nothing to move there. The Bastian Ring-Day event (363) and the later stones wait until those maps
are built.
**Not done (next builder):** Skaldfast 921-923 and Cinder Cape 927 (job 5). 925's west half and 920's north rim could
take more set pieces. Kit ideas left: a glass variant of the sand dune ledges when they cross glass, crest-side ridges
with a lit top surface, a stair kit in glass. Field plugin 011's comments are regenerated with
`ruby tools/field_defaults_to_rb.rb` whenever FIELD_DEFAULTS.yaml names change.

## From the Mega Evolution workstream (SPINE Revision 23: one ring for Megas and Z-moves), 2026-11-20
Design: **`design/Z_MOVES.md`** (the one ring, the 18 type crystals and 2 species crystals, where they are, who uses
Z-moves, tests). The Eevee Octave doc is updated (`design/EEVEE_OCTAVE.md`). No map file was edited.

**Map builder**
1. **12 Z-crystal events** in `design/TRIAL_EVENTS.yaml` ("Mega Evolution and Z-crystals"). Each is one call,
   `{script: 'pf_z_crystal(:ITEM, "line")'}`, with `badges >= N && !has_item(:ITEM)` and self switch A, like the
   stones. Five are back on maps whose stones moved in Rev 21: 577 Frostwick Pass (Icium Z, Rock Smash), 605 Static
   Tunnels Depths (Steelium Z, Flash), 685 Grudgestone Quarry B1F (Rockium Z), 680 the Rootdeep (Grassium Z, Surf),
   726 Cloudstair Summit (Flyinium Z). New: 781 Hindmoor (Psychium Z), 780 the Jawbone Ridge (Buginium Z), 785
   Darkglass Mine B1F (Fairium Z), 384 Lantern Hospice (Mimikium Z, an item ball by a rag doll on a cot), 811 the
   Smokestack Parade (Poisonium Z), 822 Under the Drownings (Waterium Z, Dive), 850 Mothwell (Snorlium Z, an item ball
   in a hay barn). The other 8 crystals are quest and boss rewards (no event needed).
2. **Vane Hall (383):** the Scizorite line no longer has apostrophes ("MUMS. DONT TOUCH. - K."), which would have
   broken the event's single-quoted script; please use the new text if you built it.

**Story editor**
3. **The Ring-Day** (Ch14, `OS_RING_DAY`): Bastian now adds one line before he unwraps the ring: "And if you come by a
   Choir crystal, a sliver of the Crown's glass from the Glassfall, it'll answer that too: the chip and the sliver came
   off the same crown. One Z-move a fight, and one to a side, same as the hearts." That's the lore for "one ring".
4. **The Eevee Octave** (`CR_OCTAVE`): the reward is the Eevee and the Eevium Z, **no ring**. Vesper's line is now "And
   this. We sang over it together: a sliver of the Crown's glass from the Glassfall, tuned to every Imprint at once." /
   "You won't need a cantor's ring for it. That Warden's ring of yours hears it. Its chip and our glass came off the
   same crown." (`113_Quests_Octave.rb`; the gauntlet is unchanged.)
5. **Eight quests now also give a crystal**, each with one new line before the reward (in `114_Quests_Megas.rb`): the
   Doll Who Waited (Ghostium), Return to Sender (Electrium, "posted in AF 290 and never collected"), the Brazier Writ
   (Firium, "the brazier's own sliver"), the Tyrant's Heart (Groundium), Dogs of the Moon Market (Darkinium), Old Cinder
   (Dragonium, sewn into the harness), Dorian's encore (Normalium, the Pageant's "prop jewel" that was real all along)
   and the Memory Kata (Fightinium, in the unit's armband). Please check the voices.
6. **Celestine (Gym 17) uses a Z-move instead of a Mega:** Mimikyu with the Mimikium Z (Let's Snuggle Forever). The
   story reason is Gloaming's dusk-chapels, which still sing the whole Hymn and tuned the crystal for her storybook's
   costume-ghost. If you'd like her to say so, one line before or after the gym fits (e.g. "The dusk-chapels sang
   over this one. Every story needs one true thing in costume."). No other NPC has a crystal reason yet.

**Z-Power owner (FYI):** `PrismfallZ::RING` is now `:MEGARING` (`player_ring?`; `ZPOWERRING` still counts for old saves),
10 type crystals and 2 species crystals are added (species Z-moves keep their PBS power), and `run_trials.rb`'s Z tests
use the Mega Ring. `playtest/run_zpower.sh` should put `MEGARING` in the Bag instead of `ZPOWERRING` next time it runs.

## From the story editor: reply to the Rev 23 entry (one ring, Z-crystals), 2026-11-20
**Mega/Z workstream (items 3–6 reviewed; strings only in 113/114, `run_trials.rb` passes).**
1. **Lore fix, Bastian and Vesper.** "A sliver of the Crown's glass" plus "the chip and the sliver came off the same
   crown" read as if crystals are pieces of the Crown's stone. That would scatter Legend Plate fragments across Velmora
   and undercut Ch17's "You're the missing piece" (#1, #5).
   - Bastian now says: "a sliver of Glassfall glass... The chip's grind off the Crown's stone, and the glass came out
     of the night it cracked. Same crown, one way or another."
   - Vesper now says: "a sliver of Glassfall glass, from the night we lost everything" and "Its chip is off the Crown's
     stone, and our glass came out of the night the Crown broke. They know each other."
   - #6 is safe: Bastian has told his crown-break story earlier in Ch14, and Vesper speaks after Ch15.
   - Z_MOVES.md §1, EEVEE_OCTAVE.md and MEGA_EVOLUTION.md quote the new wording. The lore is in 01_WORLD_LORE §3, "Choir
     glass": Choir pilgrims left slivers to soak where each Imprint runs strongest. That explains the wild finds.
2. **Four crystal lines had timeline slips** (Glassfall glass is ten years old):
   - Dorian's prop jewel "for thirty years" is now "since the Glassfall. Ten years I called it paste."
   - The Memory Kata armband was pawned around AF 286, before the Glassfall, so the sliver is now "newer than both...
     added on one of those yearly visits".
   - The Tyrant's Heart sliver was "in the spoil heap" of a dig into old rock. It's now on the vertebra's crown, "where
     some Choir pilgrim must have left it to soak".
   - The doll's "behind its button eyes all along" didn't fit, because it had no buttons until the PC brought them.
     The sliver is now "sewn into its chest, in newer stitches than the rest".
   - The other four lines fit as written: Postmaster, Old Cinder, Kosk and the Moon Market.

**Map builder / trainer designer: Celestine, Gym 17 (Gloaming).**
3. Her pre-battle lines, after "Once upon a time — which is the only time there ever is, here —" (08_ACT_V Ch18):
   "My dusk-chapels still sing the whole song: every verse the rest of Velmora stopped singing. They sang over a sliver
   of glass for me, a year of dusks, until it knew my little ghost by heart." / "Every story needs one true thing in a
   borrowed costume. Mine is wearing yellow."
4. Her Z-move line, if the Z-Power plugin gets a trainer-speech hook (like EBDX's `megaOpp`): "This is the part where it
   hugs you. Hold still. It's worse if you don't."

## From map builder 12 (2026-11-20)
**Job 1 (Chapter 2-4 audit):** grades and what was rebuilt are in MAPGEN.md 2o; before/after in
`maps_out/previews/ch2_4_compare/`. **578 Rimewood Path** and **561 Gullcry Cliffs** (now 64x130) are recrafted; 577 has the
Icium Z (Rev 23, the only Z-crystal on a Chapter 2-4 map) in a Rock Smash gully.
**For the playtest:** 561's cave mouths moved: south mouth at the foot of the slide crag (about (6,72)), north mouth at
(6,~49); arrivals follow the R6_CAVE_N/S links. The landslide is proved shut (`GATE ok 561`). K2 Kestrel stands in a
one-tile gap between two tors at (11,7): the road can't skirt him now. 578: the Long Ice is an ice slide (terrain tag 12)
from the burners' stair landing west; the Unblazed's wrong turns warp you back to the blue blaze.
**For the trainer designer:** ROUTES.yaml wants 5 trainers on 578 Rimewood Path (and 5 on 566 / 577); PBS has none, so the
maps carry none. Add them to PBS and tell the map builder where they belong (578 has room on every terrace).
**For the distribution agent:** 578's Stantler stag is `WildBattle.start(:STANTLER, 19)` once (self switch A).
**Not done (next map builder, worst first):** Tidelock Gym 170-174 (stock tiles; GYM_PUZZLES' trimmed design), the caves
544/545/564 (stock Rock Cave: needs a PF cave sheet built like tileset 54, or caves drawn from the `shs` cliff kit on a dark
floor), Thistledown Manor 546/547 (stock mansion), 525 Deepwood, 562/563 the Rimewood and Glade. 566 Spinners' Rise was
recrafted after job 3 (Ram Race unchanged: shortest walk 60 steps, limit 73).

**Job 3 (the Glass Dunes look, map builder 12):** glass redrawn (black-green, specular streaks, sky in the polish, crystal
shards and spires; MAPGEN 2o), dune slides become glass lips on glass, 926's open sand glassed, 925's west half (frozen
flood pools with a 3-slide puzzle to the Icestone) and 920's north rim (scarp, watch line, a 4-slide ice islet with the
Never-Melt Ice) filled. **For the playtest (Ch19 states):** the ice on 920/925 is terrain tag 12; `GATE ok` lines prove
both prizes are shut on foot. **For the backdrop owner:** the map's glass now matches `glass_dunes.png` (dark green body,
teal-white streaks); if you re-shoot WAR-1's stage picture, export 926's new render.

## From map builder 13 (2026-11-20)
**For the trainer designer: route trainers for 577 Frostwick Pass and 578 Rimewood Path** (ROUTES.yaml wants 4 on 577
and 5 on 578; PBS has none, so neither map carries a trainer yet). Suggestions below; the cells are open ground on the
built maps with 3 clear tiles round them and no event within 3, so a trainer with sight 3-4 fits as it stands. Add the
PBS entries (stock classes, or new ones if the sprite artists want them) and tell me which you used; I'll place the
events (field rules from FIELD_DEFAULTS: 577 `:SNOWY_MOUNTAIN`, 578 `:SILKWOOD`). Levels sit between Gym 2 (cap 19) and
Gym 3 (cap 23), with no Electric or Grass answer to Marisol handed over (SPINE Rev 16).
| Map | Cell | ROUTES role | Stock class | Lv | Team idea |
|---|---|---|---|---|---|
| 577 | (36, 82) | sledger, at the foot of the climb | TWINS (two sledgers, a double) | 17-18 | Swinub + Snom |
| 577 | (25, 66) | forester by the avalanche fences | POKEMONRANGER_F | 18 | Deerling, Cubchoo |
| 577 | (33, 37) | second sledger, below the wind gap | CAMPER | 18-19 | Snorunt, Swinub |
| 577 | (37, 16) | huscarl at the Handfast Arch | BLACKBELT (or a new HUSCARL) | 19-20 | Cubchoo, Snorunt, Stantler |
| 578 | (35, 79) | Frostwick woodcutter by the log sledge | HIKER | 18 | Teddiursa, Swinub |
| 578 | (36, 61) | trapper at the snare line | POKEMONRANGER_M | 19 | Buneary, Cubchoo |
| 578 | (43, 37) | charcoal burner at the kiln | CAMPER | 19 | Snover, Vanillite |
| 578 | (37, 30) | honey-gatherer at the hives | PICNICKER | 19-20 | Teddiursa, Deerling |
| 578 | (39, 9) | Rimewood scout at the last blaze | COOLTRAINER_F | 20-21 | Sneasel, Snover, Morelull |

**Built (job 1):** the PF cave kit (`cdraw.py`, tileset 57) and **544/545 Brinecut Mine** and **564 Gullcry Caves**
rebuilt on it (MAPGEN 2p). Brinecut is DUNGEON_PUZZLES D4 (points P1-P3 = S516-518, cart at B = S519, lake drained =
S520, V516 = where the cart stands); Gullcry is D6 (V526 steps / S526 high tide). 545-547 moved into their own spec
files (546/547 unchanged).
**For the playtest:** 544 - the Cut is crossed only by the depot cart (`GATE ok 544`); ride with P1 left to the blind
drift, crawl through under the chalk X, throw P2 in the points gallery, drop down the rib's ledge, throw P1 and ride:
the cart stops at the ladder. 545 is dark: light the lamps; the pump only drains the lake while the cart stands at B.
564: the caves stay the only way north; the west gallery is always open, the sand-bar crossing is a 19-step shortcut
that floods every 24 steps (watch the gulls). The weed curtain on the east shelf is a crawlway to a grotto.
**For the trainer designer:** the caves carry Bram, Taro and Saul (544), Gorse and Holt (545), Torvald (564), all from
PBS; Holt and Saul are placed now.
**Job 2 (Gym 3):** the Tidelock Gym 170-174 is trimmed as GYM_PUZZLES asked (practice lock + one basin, 8 moves, rating
4; proofs in `mapgen/puzzles/tidelock.py`) and rebuilt on tileset 58 in a timber lock-hall kit that matches Ebbmouth
(MAPGEN 2p, GYM_PUZZLES Gym 3 "The trim"). Gunnar, Ingrid, Leif, Oskar, Bjorn and Marisol (badge via
`pfm_gym(:LEADER_MARISOL)`, TM03) are all in place. **For the playtest:** the Lock Hall door always opens on low water;
shut the basin gate from the west pier at mid water, raise to high (the raft parks at the island), lower to mid, cross,
turn wheel C and ride the Race. **For the story editor:** the Warden's Pool has a Meridian intake bolted into the lock
wall (one sign line, mine).
**Not done (next map builder, in order):** Thistledown Manor 546/547 (still the stock mansion palette; a manor set is
the next job: tileset 54's Rejuvenation interiors or the Rejuvenation Haunted Mansion / Chrisola Mansion sheets, plus
D5's creeping armchairs), 525 Deepwood (the §2n spec-restore rule applies), 562/563 the Rimewood and Glade, the
577/578 trainers once PBS has them (cells above), the Overflow Culvert Mastery 175 (bell x gate, 6/10), Gullcry B1F 565,
then Skaldfast 921-923 and Cinder Cape 927.


## From map builder 14 (2026-11-21)
**Built:** the manor kit (`mapgen/mdraw.py`, tileset 59 "PF Rejuv Manor") and **Thistledown Manor 546/547** rebuilt with
DUNGEON_PUZZLES D5 proved (stair hall 3/10, gallery 4/10, dining room 4/10; MAPGEN 2q); **The Wolfsrime (579)**, the
first Rimewood Path layout restored as a one-way shortcut road from the Rimewood's east edge to Frostwick Pass (job 2b);
the nine **577/578 route trainers** placed. Previews: `maps_out/previews/ch2_4_compare/546_before_after.jpg`,
`547_before_after.jpg`, `579_wolfsrime_restored.jpg`.
**For the playtest (when runs resume):** 546: the front doors are at the bottom; the stair hall chair is beaten by
stepping aside early (pass it with a clear tile between you); the portrait gallery is upstairs, west off the landing
(diary in the parlour: the Fool, Laertes, Rosamund, the Old King = wall positions 3, 1, 4, 2; walk down past the east
curio case and back up first, so the loose chair backs into the empty alcove); the dining room (east off the
vestibule) unlocks when the portraits are set (`GATE ok 546`); draw both chairs out of the back-stair nook, lead each
over a trapdoor, then pull the attic cord. Being caught = a wild Gastly / Shuppet / Duskull Lv 15 and the room resets.
579: from 562's east edge at (47,26); the snow bank at the bottom drops you into 577 at (16-19,4) and has no way back.
**For the trainer designer:** the 577/578 events battle your round-4 PBS entries, which are still uncommitted in
`pbs/trainers.txt`; please commit them (validate_map_trainers: 0 errors against the working tree).
**For the story editor:** new manor lines are mine: Fenwick in the vestibule (the chair rule), Dame Rosamund's diary
(the curtain-call order), the gallery note, the nook card, the dining door, the hatch; the three scenes moved to the
landing (1), the parlour (2) and the conservatory (3, "Freshly turned earth on the conservatory tiles"), Lady
Thistledown to the parlour fire. Her finale still happens in the parlour, not the attic (the script's 547 beat): say if
you want it moved. 579's lines (the old drover, his grandson, the bothy, the bell) are mine too.
**For the Trials owner:** the doll quest's three buttons (546: under the dining table, the parlour fireplace, beside
the landing clock) and the rag doll (547) are placed (keys DOLL_BUTTON / ATTIC_DOLL). `validate_badge_tiers` warns
that [579,103] / [579,104] have no rumour in 140_BadgeTier_Rumours.rb.
**For the cartographer:** 579 is in maps.json, ROUTES.yaml, PLACE_NAMES, WORLD.md, world_data.py and the town map
(7,11); `tools/worldmap/gen_docs.py` has no 579 entry (warp links 562 (47,26) <-> 579 N end, 579 S end -> 577 one way).
**Not done (next map builder, in order):** **525 Gossamer Deepwood** to the crafted standard (still the old green
reskin; the D2 lantern-hollow events are fixed in `puzzles/dungeons.py` EVENTS at x 24-41, y 2-10, so carve round them
or move them with the proof; mind the MAPGEN 2n spec-restore rule), **562 the Rimewood / 563 the Glade** (C; keep
Ranger Sigurd's night-only Emolga hint on 563, 562's D7 Frost Loom at x 39-47, y 16-21, the glade warp at (47,24) and
the new Wolfsrime warp at (47,26)), then the Overflow Culvert Mastery 175, Gullcry B1F 565, Skaldfast 921-923 and
Cinder Cape 927.

## From the story editor: CHAPTER_BEATS.md (every chapter's 1–2 key events), 2026-11-21
User: "try not to make each chapter thin please... we want every chapter to be significant to some extent with either 1
or 2 key events happening each chapter." The audit is **`design/CHAPTER_BEATS.md`**: one table row per chapter (P, 1–21)
with its two key events, the consequence the player sees later, and a status.
- **Strong already (no change):** P, 1, 2, 3, 5, 6, 8–21.
- **Ch4 "Both Ways" (strengthened, proposal A):** the key event is **the Night the Ebb Stopped** on Ebbmouth 160: the
  river dies for an hour at Meridian's night export draw, the masked cell blows the Lattice intake, the river comes back
  and drags a child's punt at the Guild mill-race, the leader's mask comes up and it's Teo, and the PC answers a Meridian
  guard with Marisol watching (`:ch4_teo`). The second is **Larch's confession** (she designed the Lattice) as its own
  scene after the gym. Script: `story/23_SCRIPT_CH4.md` (coming next, with its map list).
- **Ch7 "The Quiet Ward" (proposal B, needs the creator's yes):** the night of Sable's broadcast the Hammer cuts the
  Infirmary's power, the Quiet Ward's Bleed rises, and the PC carries the salt-haired child out and sees its eyes move.
- **For side quests and map builders:** keep optional content *around* a key event, never between its build-up and its
  payoff, and keep the spot on the map clear (CHAPTER_BEATS "Notes").

## From the story editor: Script ready (map events first): Ch5 "Ten Years of Light", 2026-11-21
**For map builder 15 (building the Lock Road and Lumen now).** The full event list is the last section of
**`story/24_SCRIPT_CH5.md`, "Map events needed (Chapter 5)"**. The scene text above it is being written now; event names,
pages and switches in the list won't change. In short:
- **Counter:** new story variable **V125 CH5_STEP** (0–13, design/FLAGS.md). Events page on `>=`.
- **580 → 592 → 590 → 581 → 595 → 594 → 593 → 582 → 180** as ROUTES.yaml orders them. Story events per map: the
  Reedholms (Teo on a punt, or his wanted poster, by `:ch4_teo`), the Haul (union picket, a dropped ice block),
  Brassfall (Juno's letter at the PC, the Ice Elevator shortcut, the Union Hall boiler), the Locks (Extraction Lattice
  No. 4 and its builder's plate, the ice-cave ledger), Coppice Ride (**the first view of the Crownwall**), Wallshadow Row
  (**Juno rejoins at the Four Ways**; four closed exits with a guard each; the Southgate shrine), the Arc-Lamp Mile
  (Lamp 47, the Prism Arena hoarding), the West Gate (a NULL scan, then the GALA INVITATION).
- **181 the Lowlight before the Shatter carries twelve named residents** (Dex and his Pichu among them) at fixed spots,
  plus Rook's film crew and a four-box Rotom blackout that opens the gym. **608 has the same twelve as glass figures at
  the same spots.** Please copy the positions across.
- **Two new maps under the Spire:** **951 Service Lifts** (~21×17) and **952 Plate Vault** (~25×19; its south service
  door opens onto 608). Overflow IDs 951/952 are free (950 is the Edit Bay). **One new interior:** **596 Brassfall Union
  Hall** (~17×11; segment-3 interior slot).
- **Interlude I** reuses the Ferrow Lighthouse 105/106 (V119 = 1, Kestrel as the player).
**For the items owner:** three new Key Items, `GALAINVITATION`, `ICEBOUNDSATCHEL`, `HEATCONTRACT` (descriptions in the
script). **For BOSSES.md:** "Overcharged" Electivire (2 bars, the segment after Gym 4, `:NEON_GRID` → `:BLEED` at the bar
break). **For the trainer designer:** route trainers per ROUTES.yaml (580: 6, 592: 5, 581: 6, 595: 5, 594: 6, 593: 5),
Lv 20–26, and no Ground type handed over before Rook (they're foes, so only gifts matter). **For the Trials owner:**
`ZE_OCTAVE_OFF_BEAT` sits on 181, which 608 replaces after the Shatter; close or move it. **For the puzzle engineer
(GYM_PUZZLES Gym 4, 193):** Rook's PA line at the cold cradle changes, because "Turn it off. Rotom. Turn it *off*." is
his line in the Lowlight after the Shatter (03_CAST); the new line is in the script.

## From the story editor: Script ready: Ch4 "Both Ways", 2026-11-21
**`story/23_SCRIPT_CH4.md`**; the wiring list is its last section, "Map events needed (Chapter 4)". The maps are built,
so this is mostly new pages on existing events plus five scenes. Counter: **V124 CH4_STEP** (0–7, design/FLAGS.md).
- **The key event (CHAPTER_BEATS A): "The Night the Ebb Stopped"** replaces the built "Teo" event on **160** (29,31).
  It needs a night tone, Pella's punt with a move route down the channel to the Guild Mill's race gate (29,37), three
  grey cowls at the intake (27,40), an explosion SE, a Hollow double on the towpath, Teo (`HOLLOW_TEO` v0) at the gate's
  chain platform, the gate drop, Marisol's Floatzel in the water, a Meridian guard and the `:ch4_teo` choice, then
  Kestrel. It runs on returning from **167** after the new **"The Strike Vote"** autorun there (a crowd of 6–8, Teo on
  the wheel platform).
- **Other scenes:** "He Followed You Here" at the eel stall (160, comedy, Marisol's first meeting); "The morning
  after" (160, three variants by `:ch4_teo`); "Pick One" after the gym (160); **"Larch's Tide Tables"** in the Center
  (161; replaces the built two Larch lines); Hesper's letter at the 161 Gale Post desk; the Reyes House night page (164)
  and **166 Reyes Cellar** (in maps.json, no spec yet: please build it, ~17×13); the 167 towpath gate east to 580 (opens
  at V124 >= 7).
- **Changed built lines:** K2 on 561 (11,7), Marisol on 174, the Tidelock gym guide, the 160 lock-keeper, Pella (the
  built "Child with a toy boat"), and small second pages on 566, 577, 570, 573, 575, 578, 562 (all in the list).
- The Tidelock's Lock Hall door opens at **V124 >= 5** (the morning after the night), so the gym always follows the night.
**Cartographer:** maps.json still calls Marisol's brother "Tomas" on 160 and 166: he's **Teo**. **Trainer designer:**
Ebbmouth versions of `HOLLOW_GRUNT_M`/`_F` (a double on the towpath, two singles in the cellar), and please change
`HOLLOW_TEO` v0's LoseText (he's still masked when he loses; suggested "Not now — not NOW, it's jammed—").
**Items owner:** CELLAR KEY, SMOKED CHAR. Proposed badge name: **Tideturn Badge** (Gym 4's is proposed in the Ch5 script).

## From the story editor: Ch5 scenes complete, 2026-11-21
**`story/24_SCRIPT_CH5.md` is now the full script** (the scenes above its "Map events needed" list, which is unchanged
from the entry above). For map builder 15, the lines you'll want first: the twelve Lowlight residents (181) and their
glass figures (608), Juno at the Four Ways (594), the blackout's four junction boxes (181), the Gala free-roam guests
(186), and the vault (952: the Shatter, cutscene SH-1, the Electivire boss, Larch at 3 a.m.). The Circuit Gym's only
change is Rook's PA line at the cold cradle (193): "Rotom. Cut the feed. ...That bit's not for chat, buddy. Cut it."
**Cutscenes owner:** SH-1 "The Shatter" (5 shots, ~8 s) is storyboarded in the script's 952 section.

## From the story editor: Script ready: Ch6 "What the Sand Keeps", 2026-11-21
**`story/25_SCRIPT_CH6.md`**, with its "Map events needed (Chapter 6)" list at the end (none of the Brass Road or
Duneholt maps is built yet). Counter: **V126 CH6_STEP** (0–9). Key events (CHAPTER_BEATS): the **Ossuary murals and
Sahar's confession** (620/624/625), and **K3** with Morwen's veil at the Ossuary's mouth (620). The middle beat is the
Mandate's first arrests at Duneholt's deep-works (204, `:ch6_drillsite`). Also: the Act II opener on 608 (Dex's glass
warms under the PC's hand; Juno leaves for Mirefen; Rook sits with the glass), a Mandate checkpoint on 612 that reads
`:ch5_lowlight_testimony`, and GO_SINKFIELD on 628.
**Map ID clash for the Trials owner and the cartographer:** TRIALS_QUESTS puts Sona's Temple of the Noon Sun on map
**215**, which GYM_PUZZLES already uses for the Gym 5 Mural Gallery Mastery. Segment 4 has 606, 607, 609, 614–619 free.
**Trainer designer:** a Duneholt `MERIDIAN_DIRECTORATE` "Sergeant" (the first Directorate fight) and a Duneholt
`HOLLOW_GRUNT_M`. **Items owner:** MANDATE PASS, DUNEHOLT RUBBING. Proposed badge name: **Sandglass Badge**.
**15_COMEDY owner:** the Ch6 scene "Lecture, Archaeological" has Kestrel mention "a pit bracket last week", which is
Ch9; the script keeps the beat with a timeline-safe line ("Things give up around them. Rivers. Plates. Me. Twice.").

## From the story editor: Script ready: Ch7 "The Quiet Ward", 2026-11-21
**`story/26_SCRIPT_CH7.md`**, with "Map events needed (Chapter 7)" at the end (the Leach Road and Mirefen aren't built).
Counters: **V127 CH7_STEP** (0–7) and **V128 SWEETROT_TAKEN** (0–3, the GO_SWEET_TOOTH count). Key events: **J2 and
the ledger** (223's dispensary; `:ch7_ledger`) and **the Ward Night** (223's Quiet Ward), which is CHAPTER_BEATS
**proposal B** and waits on the creator's yes. It is written in and marked [PROPOSAL B], with the outline's roof scene
printed under it as the fallback, so a builder can wire either: both set V127 = 6 and nothing later reads which one ran.
Also: the first descent into Nadir at the Gutterfall (633), three Sweetrot offers (220, 220, 221 with the checkpoint),
Wick at the Weeping Fen (648; a talk-down check), a Directorate "Escort" ambush on 621 only if `:ch6_drillsite ==
:hollow`, and Gym 6 (233, double).
**Trainer designer:** a Leach version of `MERIDIAN_DIRECTORATE` "Officer" (a double). **Items owner:** INVOICE (Key
Item, flavour), Corvin's TM (Venoshock suggested). Proposed badge name: **Remedy Badge**.
