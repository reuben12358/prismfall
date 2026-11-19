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
