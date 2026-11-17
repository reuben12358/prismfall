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
