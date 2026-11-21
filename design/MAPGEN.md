# MAPGEN — generated RPG Maker XP maps for Prismfall

The map generator turns readable YAML specs into real RMXP map files (`Data/MapNNN.rxdata`) for Essentials v21.1 + EBDX, using
the base project's stock tilesets. Code and specs live in `mapgen/`, output in `maps_out/`.

## 1. What's built (Act I, in story order)
| IDs | Maps | Story / mechanics |
|---|---|---|
| 109–110 | The Dovetail: deck and cabin (prologue) | FINAL script (§2f): title card, appearance, manifest name, difficulty; Edda's rail scene, Voss and `:pro_fellowship`, checkpoint, gangway opens on S101; six passengers, cook, trunk, letter |
| 100–108 | Ferrow's Landing and interiors | FINAL script (§2f): docking, Edda's last call (GO_HOMEWARD), the NULL scan and title card, Larch/Sanctuary/starter/Kestrel, K1, Rowan, Juno's errand, Ch1 end at the inn, Larch's send-off, Wingull and Lamplighter sidequests, Hesper |
| 520, 521 (+523) | The Ferrymen's Mile, Windfall Row (+ Hale Farmhouse) | The Windfall Row cordon guard lets you through once K1 is done |
| 522 | The Glassed Orchard (:BLEED) | Bleed Veil scene with Juno: GO-02 choice, the Wurmple calm, Larch's Field Notes line (S105) |
| 524–526 | Gossamer Wood, Deepwood, Woodward's Hut (:SILKWOOD) | Silk-wall loop, Cut tree to Deepwood |
| 120–125 | Briarwick and interiors | Thistle at the pylon (HOLLOW_THISTLE, S106), Loyal Three shrine, poster, Celestine (S170) |
| 130, 131 (+132, 134) | Loomhouse (**Gym 2** since SPINE Rev 14; tileset 54) | `gen_loomhouse.py` + `puzzles/canopy.py` (SPINE Rev 19): 130 the weavers' lobby at the elder's foot (looms, Granny Loom, the gym guide, Tamsin's apology spiral, the Ledger key); 131 **The Canopy**, the hollow of the elder: web trampolines (taut webs throw you 3 tiles, sticky webs hold you, two Joltik flip the webs on their strands), Orla, Nell, Bram, Leavanny, Juno with the hatbox, Tamsin on the top ledge: `gym_battle(pfm_gym(:LEADER_TAMSIN), double: true)`, the Weft Badge, TM89, the `:ch2_tamsin` confession, the Shuttle. Optional Upper Lofts after her badge: 132 spools + the brass Meridian wire, 134 Granny's Knot. 133 retired |
| 540–542, 548 | Thistledown Lea, the Grey Saltings (:BEACH), rest house, Cocoonfall Hollow (:BLEED) | Crystal silk opens once `pf_choice(:CH2_TAMSIN)` is set. Glass Matriarch: `Prismfall::Bosses.wild_battle(:GLASS_MATRIARCH)` (S107, V105=1, V102=3) |
| 544–545 | Brinecut Mine 1F/B1F (:CAVE) | Built on the Rock Cave templates. Links Thistledown Lea's mine mouth with the Grey Saltings's back door. Salt miner gives TM98 after Badge 2 |
| 546–547 | Thistledown Manor + Attic (haunted house) | Mansion tileset (`palettes/mansion.yaml`): checker foyer with a grand staircase, arched-window portrait hall, dust-sheeted dining room, ruined cobwebbed attic. DarkMap. Three ghost scenes (wrong line → ghost battle). Lady Thistledown's offer: GO-03 or Spell Tag + Litwick (S176). Greavard in the attic |
| 560–563, 570–576 | Borderland A (the Rimewood, §2h): Frostflat Causeway, Frostwick and interiors (PC, the Exchange, the Two Hearths, Rime-silk Loft, Border House, Halvard's Smokehouse), The Rimewood, Rimewood Glade (Cut) | Chain 140 → 560 → 570 → 562 → 561 → 160; 562 ↔ 563 by warp `RIME_GLADE` behind a Cut sapling. 11 new route trainers, Border Stones, lagoon ice, the Silk-fall, the Snowveil Shrine |
| 561, 564 | Gullcry Cliffs (sea cliffs, landslide detour), Gullcry Caves | K2 (Trainer(4) sight event, `Prismfall.rival_battle(:RIVAL_KESTREL, "Kestrel", 2)`), `CH4_KESTREL_MOURNER` choice, S111, V114=1. Gullcry reuses the Rock Cave template |
| 160–165 | Ebbmouth and interiors | Rain. River Ebb with footbridges, Meridian tidal Lattice. Teo night scene (after K2): HOLLOW_TEO battle, `CH4_TEO` choice, S112. Good Rod (Anglers' Guild). Ice-fishers' whale song. Larch's tide-data revelation after Badge 3 |
| 170–174 | Tidelock Gym (Gym 3, :WATER_SURFACE) | Harbour tileset (`palettes/harbour.yaml`). Low/Mid/High basin variant maps. Sluice wheels W/C/E transfer to the same x,y on another level. Mid: raft events (passable plank tile) to the bell-rope. High: current lanes (forced moves). The north lane reaches the exit only with the tide bell ON (S315). Marisol `gym_battle(3)` → Badge 3, TM03 |
| 140–145 | Saltmere and interiors | J1 and the `CH3_JUNO_TALK` choice (S109). After Badge 2, the Pageant: Mourner speech, grunt double battle, Gilded King page (S108, V102=4). Kestrel's exit, the royal notice |
| 150, 154 (+151–153) | Pell Playhouse (**Gym 1** since SPINE Rev 14; tileset 54) | `gen_playhouse.py` + `puzzles/playhouse.py`: Lobby (posters, usher, gym guide), Auditorium (aisle between the seat rows, Florian/Rosalind/Ambrose, Juno in the stalls, ONE curtain rope, Dorian: `gym_battle(pfm_gym(:LEADER_DORIAN), double: false)`, Footlight Badge, TM42, Eevee "Understudy"). Optional Playhouse Backstage (DUNGEON_PUZZLES D9) after Tamsin's badge: 151 old revolve, 152 Fly Loft, 153 Trap Room |
| 990 | Prismfall Test Arena | One NPC per SPINE field: wild or trainer test battle with `setBattleRule("field", :ID)` |

**New game start:** `Plugins/Prismfall Maps/004_NewGameStart.rb` sets `PrismfallMaps::PRISMFALL_START = [109, 7, 6]`
(nil = use RMXP's Player Starting Position). It alias-chains `Game.start_new` to override `$data_system.start_map_id/x/y`
in memory, so no RMXP edit is needed. The stock intro map is skipped, so the Dovetail intro does its jobs:
- appearance choice (`pbChangePlayer(1/2)`)
- name, entered as Edda's passenger manifest (`pbTrainerName` with a confirm loop)
- running shoes and `Prismfall.choose_difficulty`
Later scenes hand out the rest: Larch gives the Pokédex with the starter, and Wenna Hale gives the Pokégear.
The stock intro's controls tutorial is not reproduced.

## 2. Installing into your project (Windows, RPG Maker XP)
1. **Close RPG Maker XP.** It rewrites `MapInfos.rxdata` when it saves.
2. Copy `maps_out/Data/Map*.rxdata` and `maps_out/Data/mapinfos_prismfall.txt` into your project's `Data/`.
   Copy `maps_out/PBS/map_metadata_prismfall.txt` and `map_connections_prismfall.txt` into `PBS/`. v21.1 merges `<base>_<suffix>.txt` files.
3. Copy the runtime plugin `maps_out/Plugins/Prismfall Maps/` into `Plugins/`. It holds:
   - `003_StoryBosses.rb`, **generated** from `mapgen/bosses.yaml`: story boss definitions for the Prismfall Bosses plugin.
   - `002_MapFields.rb`, **generated** by build.py from the specs' `field:` entries. It fills `FieldEffects::MAP_FIELDS`
     (guarded with `if defined?(FieldEffects)`), so map → field defaults ship with the maps and nobody edits Field Effects by hand.
   - The Debug installer action from step 4.
   - Its `meta.txt` says `Optional = Prismfall Field Effects,1.0.0`, so it loads after Field Effects. Essentials **ignores
     Optional lines without a version** (PluginManager: "Optional dependencies must have a version given").
4. Register the maps in `Data/MapInfos.rxdata` with **either** method:
   - **In-game (recommended, uses the game's own Marshal):** with the plugin installed,
     Start the game in Debug mode and run **Debug → Files → Install Prismfall maps**. The plugin backs up `MapInfos.rxdata` once,
     to `MapInfos.rxdata.prismfall-bak`. It adds each line of `mapinfos_prismfall.txt` with its name and parent, keeps every
     existing entry, and reports any ID collision (skipped) or missing map file.
   - **Standalone (needs Python 3 + numpy + PyYAML):** run `python3 -I mapgen/merge_mapinfos.py "C:\path\to\YourProject"`.
     The **merge tool** does steps 2 and 3 itself: it copies the maps and PBS files, then reads *your* MapInfos with a safe parser,
     adds our entries, warns on and skips collisions, and makes a backup. Add `--dry-run` to only report.
   - We never ship a prebuilt MapInfos. Both methods start from your own file.
   - If you skip this step, Essentials' compiler still imports the maps in Debug mode, but with names like `MAP100` and no tree.
5. Start the game in Debug mode so it **recompiles** (or use Debug → Compile data). Then open RMXP: the maps appear under their parents.
6. Trainers used by map events are listed in `maps_out/trainers_needed.txt`, for example `:YOUNGSTER, "Pip"`.
   Each must exist in PBS. Missing ones crash at battle start; in Debug mode, compiling offers to create them.

**Game Switches / Variables used by map events.** We never touch `System.rxdata`; name them in RMXP's database.
- **Story IDs (101–300)** come from `design/FLAGS.md`. build.py parses its tables, and specs use the names (`switch: CH1_K1_DONE`,
  `var: [STORY_CHAPTER, 3]`, `@@NAME` inside scripts). Used so far:
  - Switches: S101–S110, S161 LARCH_AT_TIDEWATCH (switched on by the prologue intro), S170 GLOAMING_DISGUISED_CELESTINE.
  - Variables: V101 STORY_ACT, V102 STORY_CHAPTER, V105 BRIARWICK_GLASSWOOD.
  - Plus stock switch 22 `s:tsOff?("A")`, used by the door pattern.
- **Gym puzzle IDs (301–400)**, in `mapgen/flags.yaml`:
  - The blocks follow the building, not the gym number (SPINE Rev 14). **305–309 = the Loomhouse (Gym 2):** V305–307
    `CANOPY_WEB_A/B/C` (the Canopy's Joltik webs, Rev 19), S305–307 the Upper Lofts cords, S308 Granny's Knot, V309 the
    loft bridge. **310–314 = the Pell Playhouse (Gym 1):** V310 `STAGE_SCENE`, V311 `STAGE_CURTAIN`, V312
    `STAGE_TURNTABLE`, V313 `STAGE_AUDIENCE`; S310–312 the backstage flats, S314 the Trap Room chest. Names:
    `mapgen/flags.yaml`; story pointers: FLAGS.md "Pointer rows".
  - Gym 3: S315 tide bell (ON = currents run inland/north). Water level = which variant map you're on (no variable).
  - Story IDs also used now: S111 CH4_K2_DONE, S112 CH4_TEO_MET, V114 KESTREL_STAGE (set to 1 after K2).
- The base project's System.rxdata defines 100 switches and 100 variables. That is **not cosmetic**: Essentials v21.1's
  `Game_Event#switchIsOn?` treats a page condition on a switch with no System.rxdata entry as false, so pages on S101+ never
  turn on. The in-game installer adds our names from `Data/system_prismfall.txt` (written by `mapgen/export_tilesets_rxdata.py`
  from FLAGS.md + flags.yaml) and raises the maximum; projects you build by hand need the same.

**Narrative keys** follow design/NARRATIVE_KEYS.md and use the canonical lowercase choice keys:
`:pro_fellowship`, `:ch2_tamsin`, `:ch3_juno_talk`, `:ch4_kestrel_mourner`, `:ch4_teo`.
- Events call only `pf_choose(key, value)`. Core's CHOICE_EFFECTS applies the bond and standing deltas, so maps make no
  `pf_bond_add` / `pf_standing_add` calls. The Fellowship $1000 stipend is still given by the event.
- Game overs: `:GO_HOMEWARD` (Edda), `:GO_ORCHARD` (Veil), `:GO_CURTAIN_CALL` (Thistledown).

## 2b. New tilesets (tileset-agnostic pipeline)
- **Register a tileset:** `python3 -I mapgen/import_tileset.py mapgen/tilesets/<name>.yaml [--palette-skeleton]`. The
  descriptor sets the ID, name, PNG, up to 7 autotiles, and per-tile passages/priorities/terrain tags (ranges allowed,
  plus per-autotile-slot props). See `mapgen/tilesets/example_coast.yaml.example`. It copies the graphics to
  `maps_out/Graphics/`, records the tileset in `maps_out/tilesets_prismfall.json` (the renderer and the reachability
  QA read it, and imported graphics take precedence), and can write a palette skeleton `palettes/<name>.yaml`.
- **Install into the project:** `python3 -I mapgen/merge_tilesets.py <ProjectDir>` (close RMXP first). It backs up
  `Tilesets.rxdata`, copies the graphics, writes an `RPG::Tileset` at each registered ID, pads skipped slots with
  blank tilesets, and refuses ID collisions unless `--force`.
- **Specs** pick a tileset through their palette (`palette: <name>`, whose `tileset:` is the ID). Palettes so far:
  `outside` (1), `gym_rock` (14), `harbour` (15), `mansion` (16).
- Tested end to end with a dummy imported tileset (ID 30): import, build a map, render, merge into a copy of the
  Renovation project's Tilesets.rxdata, then load it with Ruby's Marshal.

## 2c. Tectonic tileset pilot (ART_DIRECTION.md)
- `tilesets/tectonic_outside.yaml` imports Tectonic's Outside sheet as **tileset 30 "Prismfall Outside"** straight from its
  `Tilesets.rxdata` (`from_rxdata:`; terrain tags above 16 are remapped per ART_DIRECTION §2.1). Install it into the
  project with `merge_tilesets.py`. Licence: CC BY-NC-SA 4.0 (docs/CREDITS.md).
- `palettes/tectonic.yaml` paints with **example-based rules learned from Tectonic's own maps** (`tlearn.py` →
  `data/learned/t_*.json`: 8-neighbour → tile, nearest-match fallback) and stamps mined with `textract.py`
  (`textract.yaml` → `data/stamps_t.json`; objects only, never layouts). `tprobe.py` is the research helper.
- New painter kinds:
  - `learned`: paving and fences.
  - `cliffline`: Gen 4 rim-line cliffs from a `heights:` grid, with stacked 3-row faces.
  - `sea`: water autotile on layer 2 with rock or quay showing under its shore.
  - `tpier`: timber piers.
  - `forest`: mixed-species staggered 2×3 trees with undergrowth.
  - `ground_table` pass: grass rims where grass meets rock, paving and water.
  - `scatter` pass: noise-patch flowers and tall grass plus single tufts on bare grass.
- Spec keys:
  - `rubric: true` prints the ART_DIRECTION §3 numbers and runs a walk-through flood fill (cut-off events and areas).
  - `heights:` gives the height grid for `cliffline`.
  - `tone: [r, g, b, gray]` goes to the generated `Plugins/Prismfall Maps/005_MapAtmosphere.rb` (applied on map entry).
  - Weather stays in `metadata`.
- Layout scripts (`layouts/saltmere.py`) build the height map, cliff lines, curving variable-width paths (`path()`),
  noise-edged blobs and the stamp list, then write them into the spec.
- The pilot layout `layouts/saltmere.py` is superseded by `layouts/saltmere_city.py` (§2d); do not run it.

## 2d. City pass: composite tileset 33, castle kit, city layouts (Saltmere, Verdance)
- **Tileset 33 "Prismfall City"** (`compose_tileset.py`): Tectonic's Outside sheet with ids unchanged, then the whole
  Rejuvenation `Sheridan_2` (offset 8616) and `GearenCity Real` (offset 10384) sheets, then a small custom sheet
  (offset 14384: realm banners 1x2, throne 2x3 from `ref/art/custom`). Offsets are in `data/compose_offsets.json`.
  Autotiles are Tectonic's (the Rejuvenation repo lacks its own). Appended terrain tags are zeroed. Re-run after
  `import_tileset.py tilesets/tectonic_outside.yaml`; install with `merge_tilesets.py`.
- **Stamps:** `tcatalog.py` makes a contact sheet of every building in a set of reference maps (connected components),
  `textract.yaml` gained the `h_*` houses, `wextract.py` / `wextract.yaml` mine the Sheridan timber houses (`w_*`) into
  `data/stamps_w.json` with ids remapped onto tileset 33. Not used: `h_olive`, `h_slant_o`, `h_flat_o`, `h_cabin`
  (their rects carry bits of neighbours).
- **Palette `city`** (`palettes/city.yaml`): everything in `tectonic` plus
  `k` cobble 2273, `g` flagstones 3910, `h` white-flower bed (autotile 240), `x` interior void, and the castle kit:
  `W`/`K`/`Q` parapet tops (wall, tower, keep; each joins only itself), `F`/`G`/`R` their south faces (buttresses, arrow
  slits, windows on faces 4+ rows tall), `S` castle stairs. Scatter is clumped (large patches, 7% singles).
- **`layouts/citykit.py`:** `City` grid with `wall_h`, `wall_v`, `tower`, `gate_arch`, `cliffs`, `stairs`,
  `quarter` (kerbed pad, packed house rows, beds, shrubs, clutter), `house_row`, `pits` (street trees), `groves`,
  `trees`, `inlay` (drain tiles 3859 / 3916), `sea_rocks`, `warp_line`, `write`.
- **Saltmere** (`layouts/saltmere_city.py`, 3 maps of 88x72): 140 Promenade & Market, 146 Harbour & Breakwater,
  147 Old Town. Story events of the pilot are in `layouts/saltmere_events.yaml` and are re-seated by name. 140 keeps
  its the Grey Saltings (N, offset 44) and Frostflat Causeway (W, offset 32) connections. Districts are joined by touch warps: harbour
  stairs 140 (48-53, 71) <-> 146 (42-47, 3), Players' Gate 140 (87, 42-45) <-> 147 (0, 36-39). Doors: PC, Mart,
  Pageant Hall, Saltwife on 140; Harbour Office on 146; Playhouse on 147. HealingSpot is 140 (19, 30).
- **Verdance** (`layouts/verdance_city.py`): 280 Market Terraces 104x88, 285 Briar Hall Upper Court 84x64, 286 Great
  Hall 33x25 and 287 Throne Room 27x27 (interiors built from the castle kit with `room()`). Placeholder events only.
- `walk_ignore:` (default wall, tower, keep) keeps unreachable parapet walks out of the cut-off warning.
- **Fix round (organic plans).** Layouts no longer use bands and rectangular quarters. `citykit` gained `hills` (noise-edged
  height blobs), `notch` (a straight step for a stairway), `front_place` / `frontage` (houses packed along the north side of
  every street), `backfill` (second rank), `greenfill` (leftover land becomes tree masses and beds), `edge_props`, `snap`
  (seat an event on the nearest street cell) and a **symmetry guard**: `write()` aborts when more than 40% of plan cells equal
  their mirror image (interiors pass `mirror_max=1.0`). Houses only front streets from the north, so a lane needs 7 clear
  rows above it; that spacing is why lanes sit where they do.
- Roofs: `textract.py` and `wextract.py` move the top 60% of each building's rows to layer 3 where it was empty, and
  `k_castle` puts the walk-behind south parapet on layer 3 (as Prizca Castle does). Rendering and passability are unchanged.
- Timber variants: `compose_tileset.py` appends slate and moss recolours of the Sheridan sheet; stamps `w_*_s`, `w_*_m`.
- Saltmere warps now: harbour stairs 140 (56-61, 71) <-> 146 (42-47, 3); Players' Gate 140 (87, 42-45) <-> 147 (0, 36-39).
  HealingSpot 140 (28, 30). Verdance: palace arch 280 (71, 9) <-> 285 south gate (22-27, 63); keep arch 285 (48, 21) -> 286.
- Interiors added: 281 / 282 (stock Poké Center and Mart templates, placeholders), 295 Cathedral (castle-kit room).
  `yards_ok: true` in a spec silences the cut-off-tiles warning for enclosed back gardens (events are still checked).
- **Open items:** 146 fails the mirror number (20.2 against 15) because 40% of it is open sea, which the rubric exempts;
  no column, chandelier, stained-glass, fountain, well or statue art; 283/284/289/294/296 districts not built; 540/560 still
  declare stale connection offsets to 140 (140's own win); Act I maps other than Saltmere are still on stock tilesets.

## 2e. Early-game towns (Revision 8): Ferrow's Landing, the Dovetail, Briarwick and their interiors
- **Tileset 33 additions** (`compose_tileset.py`, offsets in `data/compose_offsets.json`): `custom2` (17960, from
  `make_custom.py`: giant-tree boles and crowns built from Tectonic stump and canopy tiles, laundry line, rope bridge, dye
  vats, loom, net rack, silk lantern, light pool, silk awning), then the Art Director's `PF Town Props`, `PF Houses`,
  `PF Forest` sheets (`pf_*`). Autotile slot 3 is now Tectonic's `Dirt` (ids 144-191) instead of `Lavafall`.
- **Tileset 34 "Prismfall Interior"**: Tectonic `Inside` (ids unchanged) + Rejuvenation `SheridanInside`, `Help Centers`,
  `Chrisola Hotel`, `RoseTheatre`. Palette `interior`. Install both with `merge_tilesets.py`.
- **Palette `village`** = `city` plus `d` dirt lane (autotile), `s` sand, `w` wooden rail fence (learned `wfence`),
  `t` tall grass, `H` flower border, `D` ship deck; scatter uses Sheridan flowers, ferns, clover and mushrooms.
- **`layouts/villagekit.py`**: prop stamps in `data/stamps_v.json` (`g_tree6/4/4p/2` giant trees, `p_*` props, and every
  stamp of the curated sheets as `tp_*`, `hs_*`, `fo_*`), and `Village` with `dress` (scatter props, optionally only
  beside walls or paths), `borders` (flower beds along house walls), `meadow`, `fence_run`, `people` and `signs`.
- **`layouts/interiorkit.py`**: `Room(w, h)` builds a Sheridan timber room (walls, windows, plank floor, door notch and
  mat); `sf(name, x, y)` places furniture mined at run time from the Sheridan interior maps, `tf(...)` furniture listed
  from Tectonic's Inside sheet. Maps are padded to RMXP's 20x15 minimum. Spec key `take_events:` reuses a base-template
  event (Nurse, Healing balls, PC, Mart clerk) at a new position, so the Essentials event logic is kept.
- **`layouts/scriptpour.py`** parses `story/20_SCRIPT_CH0-2.md`: `[name: X]` / `[portrait: X, expr]` lines become NPC
  events (portraits as `\pf[NAME,expr]`, "(again)" lines as a second page), `LABEL: text` lines become signs,
  `HIDDEN ITEM` lines hidden items. `layouts/story_early.py` uses it for the flavour townsfolk only (§2f).
- **Scripts:** `ferrow.py` (100, 68x60), `briarwick.py` (120, 72x64), `dovetail.py` (109 deck 34x22 + calls
  `early_interiors.py`: 101-108, 110, 121-125, and builder 3's 523/526). Story events come from `layouts/story_early.py`;
  `layouts/old_*.yaml` / `*_events.yaml` now supply only map heads, the 105/106 stair warps and 108's two NPCs.
  Run `python3 -I layouts/ferrow.py && python3 -I layouts/briarwick.py && python3 -I layouts/dovetail.py && python3 -I build.py`.
- **Links:** 100 north edge `offset 28` (lane x 33-36); 120 west edge `offset 29` (the road crosses the stream on a raised
  walkway at rows 30-31); 120's south warp (35, 63) has link `WOOD_BRIAR` (pairs with 524's "To Briarwick"), (36, 63)
  goes to 524 (25, 1). Prologue arrival 100 (34, 55) on the pier. HealingSpots: 100 (19, 27), 120 (44, 27).

## 2f. Early towns, second pass: the whole script, the timber look, shared tooling
**Script (story/20_SCRIPT_CH0-2.md, maps 100-110, 120-125): `layouts/story_early.py`** writes every event by hand from the
FINAL script; layouts only seat them (`place(map, name, xy)`) and abort if any event is left unplaced (`unplaced(map)`).
- Portrait lines are `\pf[ID,expr,emotes,event]Name: text` (379 tags; the script's *(anger vein)* / *(sweat drop)* /
  *(shock lines)* / *(question mark)* / *("...")* become the emotes `anger sweat shock question dots`); the speaker's event is
  named so the bubble's tail points at it. Choices use NARRATIVE_KEYS' keys through `pf_choose` only (`:pro_fellowship`,
  `:ch2_tamsin`). Game over `:GO_HOMEWARD` with `Prismfall.checkpoint` after the badge-case scene.
- Built: Dovetail intro, Edda's rail scene (touch line at the port rail), Voss, the gangway; docking (passengers through the
  gate), Edda's last call, the NULL scan with Voss/Calla/the camera/the chain/Crier/`PF_ACT1_TITLE`; Calla and Edda after;
  Wenna (tart, Pokégear, [after S103], [after S105] + the Biscuit reward shared with 523's self switch), Coll, Odo, Crier,
  all flavour townsfolk with (again) pages; Larch's letter scene (autorun), the Sanctuary starter scene (Juno's and Kestrel's
  picks named from `Prismfall::Rival`), Kestrel's loft drop, K1 with both outcomes and Juno's "Team Compost", Rowan,
  Juno's errand; the end of Chapter 1 when resting at the inn (`PF_CH1_NOTEBOOK`, V102 = 2); Larch's send-off on the north
  lane (V102 >= 2; TOWN MAP); sidequests "Captain Edda" (Wingull on the lighthouse rocks, SHARP BEAK) and "The Last Round"
  (taper, six lamp events that change graphic, dusk tone, CHARCOAL); lighthouse locked until S105; Hesper's autorun.
  Briarwick: Juno's arrival, Tamsin bumping into you, Thistle's night scene at the pylon (after meeting Tamsin), Finch,
  the old woman (S170 on at arrival, off after Badge 1 by a parallel "Stage manager"), the Dusk Petal, the bridge boy,
  "Sixteen Sleeves", every townsfolk line with the after-gym variants, signs, hidden items, the charcoal child (after
  S107) and the Gale Post letters (V102 = 3). Interiors: nurses' script lines (`take_events` `replace_text`, plus the
  no-Pokémon line via `prepend`), Fellowship activation at the Mart, inn guests, Dockmaster's ledger, the lighthouse
  objects, Hett and "The Locked Ledger", the Warden's loft (ledger + Tamsin's `:ch2_tamsin` confession, guarded), the
  chapel (second room of 124, door `BW_CHAPEL` on 120), the Cutter's two-step HM01.
- **Runtime helpers** (`mapgen/ruby/006_MapStory.rb`, copied into `Plugins/Prismfall Maps/` by build.py): `pfm?` /
  `pfm_set` / `pfm_add` saved scene flags (no new switch ids), `pfm_item(:ID, n, "Name")` (real item if PBS has it, else a
  message + remembered story item), `pfm_has?`, `pfm_quest` / `pfm_quest_done` (a small quest log in `$PokemonGlobal`),
  `pfm_money`, `pfm_card(:SCENE, lines...)` (title cards defined there for the Cutscenes plugin, message fallback),
  `pfm_dusk` / `pfm_day`.
**DSL / build.py additions:** `who: "Event name"` in `move`, `%EV[Name]%` in scripts (event ids resolved per map),
`{anim: [who, id]}` (Show Animation), door `locked: {until: SWITCH, text}` (a locked page, then the door), `take_events`
`replace_text` / `prepend`, spec key **`fog: {name, opacity, blend, zoom, sx, sy, hue}`** (generated into
`005_MapAtmosphere.rb` next to MAP_TONES; REQUESTS item 3), **`build.py --mood`** writes `previews/mood/` with tone and fog
applied (`render.mood`, item 5).
**Tileset 33 additions (appended at the end; no earlier offset moved):** `sheridan_red` (red-roofed timber, stamps `w_*_r`,
for Poké Centers), `custom3` (Briarwick's elder tree `g_elder` 12x12 with door (6, 11); silk garland tiles: plain,
pennants, hanging lantern, tufts). `custom2` gained the quay oil lamp unlit/lit (C2+166/167) in two free cells.
**Painters:** `terrain.k_forest` now puts the canopy body ("mid" row) on layer 3 as well as the top (rubric 5); this also
lifts layer 3 on every palette using `kind: forest` (city, village, tectonic, wilds, bleed) without changing passability.
`villagekit.Village.lane()` paints smooth Catmull-Rom lanes 2-3 tiles wide; `villagekit.DECK` is Sheridan's raised timber
deck (9-slice with edge passages, solid stilts, plank stairs) used by `briarwick.deck()` / `walkway()`.
**interiorkit:** 30 more Tectonic Inside pieces (bookcases, paintings, clocks, dining set, sideboard, china cabinet, pens,
workshop clutter), `Room.rug()` (Sheridan 9-slice rug; furniture on it moves up a layer), `Room.floor()`, and
`combine(rooms, head, events)` for multi-room maps (103 annex, 123 loft, 124 chapel).
**Look:** Ferrow's Poké Center is a red timber longhouse, the Mart a slate-blue timber house, both with banners and a
Poké Ball plaque; Tidewatch is a moss timber cottage with a lantern turret and a brass sea-glass on the hill; the lighthouse
is Jonquil's octagonal tower on the west headland; lanes are 2-3 wide and wind; the Dovetail is a plank hull with rails,
a wheelhouse and a pennant mast (no sheet has a timber ship). Briarwick: the elder tree on its knoll is the Loomhouse, boles
of four sizes, a raised weavers' deck, two lantern decks joined by a walkway, a raised walkway over the stream, silk
garlands with lanterns overhead, dusk tone and spore fog. 523/526 are re-tiled Sheridan rooms with builder 3's events.
**Rubric (build output):** 100 layer2 67.8, layer3 23.4, bare 15.3, bare3x3 1.1, stacks 18.6, mirror 13.0;
120 layer2 63.9, layer3 39.8, bare 9.6, bare3x3 0.1, stacks 18.6, mirror 2.9. No reachability warnings on 100-125.
**Not built as written:** Juno as a following character (no follower API: she is placed events), Kestrel's figure on the
lighthouse gallery (text), the Dovetail sprite pulling back and the chain drawn across (text), "the PC's hand moves to
their chest" (text), the guild meetings (fade + text), the keep-secret "finished pylon" (pylon sign text changes, map art
does not), the ledger key in the Loomhouse foyer (map 130, builder 3: see REQUESTS), the Ch1 notebook scene at the
farmhouse bed (523's own event does it). Items without PBS data are given by `pfm_item` (BADGECASE, FELLOWSHIPCARD,
OLDCHOWDER, BRAMBLETART, LAMPTAPER, BARKMASK, DUSKPETAL, KELPTEABAG, MOTHERLOOMSSHUTTLE, LEDGERKEY, TMSTRINGSHOT).

## 2g. Material coherence (biomes), per-biome variants, the Dovetail ship
- **Every map declares `biome:`** (forest, route, village, harbour, bleed, canopy_gym, city, interior). `data/materials.yaml`
  tags tile-id ranges with a material (wood, stone, iron, metal, concrete, modern, fabric, crystal...; `shared` = the
  Tectonic part of tilesets 30/33/40, plus per-tileset ranges) and lists what each biome forbids. `build.py` warns
  `MATERIAL <mat> in a <biome> map` for map tiles and tile-graphic events; `build.py --strict` fails. Untagged tiles pass:
  tag new families as you meet them. All early maps pass `--strict`.
- **Variants** (`material_art.py`, appended last to tilesets 33 and 40 as part `materials`; stamps `<name>@33` / `<name>@40`
  in `data/stamps_m.json`, rewrite with `material_art.write_stamps()` after composing): `stairs_log` (earth-cut steps,
  log risers), `stairs_stone` (worn, mossy), `stairs_plank` (between log posts), `signpost`, `lantern`, `logbench`,
  `barricade`, deck `rail_h/w/e/nw/ne` (layer 3, priority 1, passage 0: the deck edge keeps its passages), `glow` (2x2 warm pool).
  `City.stair_kind` picks the stair per map (Wild default `stairs_log@40`); palettes village/wilds/bleed/loom use the
  wooden signpost for sign events. The blue-railed metal `t_stairs` (1389-1415) is tagged metal and banned outside cities.
- **The Dovetail** (`ship_art.py`, configs `dovetail` for 109 and `moored` for Ferrow's pier): painted hull with wale and
  waterline, bulwark, deck planking, bow with bowsprit, transom, two masts with crow's nests, furled sails on yards,
  shrouds and stays; sliced to tileset 33 parts `dovetail` / `ship_moored`, placements in `data/ship_*.json`.
- **Readability** (top-down contrast rule): paths carry almost no decals (`path_decor` <= 0.015); texture and contrast live
  in borders, undergrowth and props; wilds forest mixes species in small patches with dense layered undergrowth.

## 2h. The Rejuvenation pass (PF Rejuv composite, tilesets 50–53)
**Why:** the user wants the maps to look like Rejuvenation's Goldenleaf Town and Sheridan. The full games are in
`/home/claude/ref/games/` (GAMES_READY.md). Only tiles and stamps are taken from them: every layout here is our own.
Rejuvenation's asset rules forbid copying its maps.

**Tools (all read the games with the safe parser; nothing from `ref/` is executed):**
- `rref.py`: `render <game> <map> out.png [scale] [--crop x,y,w,h] [--grid]`, `stats`, `doors` (transfer events), `maps <tileset ids>`.
- `rcat.py`: a numbered contact sheet of a map's objects (connected layer-2/3 components) for picking stamps.
- `rcompose.py`: builds the sheet **`PF Rejuv`** from whole sheets. Parts are append-only, so ids never move:
  - gl Goldenleaf 384
  - sh Sheridan_2 4832
  - ak Akuwa `Route 4` 6832
  - kf Kristiline Town (Frozen) 8304
  - rb4 Reborn Route4 10448
  - ap Aevium Past 11496
  - pf (our own pieces) 17744

  A composite id is the part offset + (source id − 384). It registers four tilesets that share the sheet, each with its
  own 7 autotiles (copied as `RJ <name>` / `RB <name>` / `PF <name>`):

  | ID | Name | Autotiles |
  |---|---|---|
  | 50 | Village | Sea(Grass), DirtDark, waterfalls, Gravel Spring, Dirt |
  | 51 | Coast | Sea(Grass), DirtDark, Ocean, Sand shore_2, Sea deep, Gravel Spring, Dirt |
  | 52 | Snow | KristilineWatersFrozen, KristilineDirt, Sea deep, Sand shore(Terajuma), waterfalls (T), Still water snow |
  | 53 | Wild | Sea(Grass), DirtDark, Dirt, Gravel(G), Still water, Waterfall, Waterfall bottom |

  - Terrain tags 17+ use GAMES_READY's table.
  - These games leave water autotiles at tag 0 (they script surfing). `AUTO_TAG` gives them v21 tags 5–9, so Old Rod fishing and Surf work.
  - `Gravel Spring` is Goldenleaf's `Gravel(G)` with its autumn verge recoloured to Sheridan green.
  - Layouts never use autotile slots. They use *virtual* ids (`rcompose.vauto(game, name)`), resolved per tileset at write time.
- `import_tileset.py` gained `tag_remap:` (per-source table). Do not use `remap_tags: true` for these games.
- `rcustom.py` builds the `pf` part:
  - Prismfall's own art from tileset 33: giant trees and Briarwick's elder (greens re-graded to Sheridan's ramp), silk props, garlands, quay lamps, the moored Dovetail, material variants.
  - **snowified** copies: Sheridan cliffs, Akuwa sea cliffs, the Sheridan tree lattice, grass, a cave arch, and every giant tree (`pf_g_*_ice`).
  - Output: `data/stamps_rjc.json` (`pf_*`, `_snow`, `_singles`, `_ship_moored`).
- `rstamps.py` + `rstamps.yaml`: stamps mined from real maps by rect + source-row filter (`rows`, `deny`, `drop`, `clear`, `door`) or straight from the sheet (`sheet:`). Output `data/stamps_rj.json`:
  - Goldenleaf houses `gl_pc/gym/hall/mart/ell/emblem/cot/flat1/flat2/shed`, with the autumn bushes dropped
  - Sheridan `sh_big/help/inn/small/shop/ell/cot` and props `sh_campfire/crates/gate/arch`
  - Kristiline `kf_aframe/aframe2/flat/tree`
  - Akuwa `ak_boulder/rock2/fern`
  - trees `tr_oak/oak2/pine/pine2/teal/pink`, Reborn `pine2`
  - the striped `lighthouse`, `gl_lamp`, `gl_tables`
- `layouts/rkit.py` (`RMap`) paints the maps:
  - Plan classes: `.` grass, `t` tall grass, `d` lane, `g` gravel street, `w` water, `W` deep, `s` beach, `T` forest, `o` frozen water, `I`/`i` ice, `B` blocked.
  - Plus a height grid, stamps (with a building-overlap guard), events and over-tiles.
  - `paint()` runs, in order: ground, autotiles (water on layer 1, lanes/sand/deep on layer 2 so their edges blend), cliff kits, stairs, the tree lattice, stamps.
  - Cliff kits: `sh` / `sh3` Sheridan (lip + 3 or 2 face rows over grass, 1-wide sides, inner corners), `ak` Akuwa grass-capped sea cliffs, and the snow versions `shs` / `aks`.
  - Helpers: `front` (seat a building by its door), `street`, `lane`, `stairs`, `trees` (yard clusters; trunks never overlap), `greenfill` (leftover lawn ≥ n tiles from any lane, door or event becomes forest), `beds` (flowers at the foot of front walls), `fence`, `near`, `scatter` (edge-weighted decor), `preview`, `write`.
  - `write` emits `data/raw/NNN.npy` and a spec with `raw:` + `tileset:`. `build.py` now takes `raw:` specs.
- `compare.py <id> <ref png> out.png`: our build next to a reference at the same tile scale.
- `build.py`: spec key `walk_from: [[x, y], ...]` adds flood seeds, for maps whose halves join through another map (561 via the caves).

**Composition patterns learned from Goldenleaf (map 82), Sheridan (423, 214, 38), Akuwa (13) and Kristiline Frozen (328):**
1. *Ground is quiet, texture lives above it.* Each map uses one 2×2 grass checker (Sheridan 646/647/654/655) or plain snow. Contrast comes from layer-2/3 objects, lane edges and the dense decor at the foot of things, never from noisy ground.
2. *Streets are orthogonal and wide.*
   - Goldenleaf: gravel streets 3–4 wide on a rectilinear plan with T-junctions, one paved plaza with a landmark (fountain and statue).
   - Sheridan: dirt lanes 2–3 wide with right-angle jogs.
   - Never diagonal, never a 1-wide path.
3. *Buildings front the street.* The door sits 1–2 cells above the street with a stoop. Houses stand shoulder to shoulder, 1–3 tiles apart. Big buildings (Center, gym) get a timber porch pad or deck. Signboards stand beside doors, lamps at junctions, crates and barrels by shops, picnic tables in squares, fences at yard edges.
4. *No lawns.* Every cell that is not street, yard or water is tree mass:
   - Forest is a staggered lattice of 3×4 trees, period 3 horizontally, rows every 2, each row shifted.
   - Top two rows go on layer 3, trunks on layer 2. Two species are mixed.
   - Single yard trees stand at building corners, plus pines and blossoms for accents.
5. *Elevation:*
   - Goldenleaf rings the town with 3–4 concentric terraces, a waterfall off the top one, and wooden stairs 2–3 wide.
   - Sheridan cliffs are a lip row plus 3 face rows with 1-wide sides and inner corners.
   - Akuwa's grass-capped cliffs rise straight out of the sea onto a white beach, with 2×2 and 4×4 rocks offshore.
6. *Water:*
   - Sheridan rivers use the grass-edged `Sea(Grass)` autotile, crossed by plank walkways and bridges.
   - Kristiline's frozen sea is walkable ice (2476, tag 12) with dark holes of the `KristilineWatersFrozen` autotile; the autotile's rims carry the ice texture.
7. *Density:* roughly every 16×12 screen holds a building or landmark plus 3–5 prop clusters. Flowers grow in drifts, not singles.

**Maps on PF Rejuv:**
- **100 Ferrow's Landing** (`layouts/ferrow_rj.py`, tileset 51, 68×60):
  - Bluff (Akuwa cliffs), Tidewatch hill and north-west terraces (Sheridan cliffs), harbour beach, 3-wide pier at x 33–35 (water from row 48), the Dovetail moored east, striped lighthouse on the west headland.
  - Doors: PC (24,14), inn (11,27), Mart (39,22), lab (53,11), customs (22,44), Dockmaster (44,43), lighthouse (5,40).
  - HealingSpot is [100, 24, 15].
- **120 Briarwick** (`layouts/briarwick_rj.py`, tileset 50, 72×64):
  - Doors: elder-tree gym (36,12), Guildhall (17,26), Help Center (45,23), Treetop House (55,24), Mart (27,40), chapel (63,42), Cutter's House (42,50).
  - Thistledown Lea road on rows 30–31 over the stream walkway. HealingSpot is [120, 45, 24].
- **Borderland A** (`layouts/rimewood.py` + `rimewood_interiors.py`, tileset 52 / interiors on 34): 560 (64×30), 570 Frostwick (60×48), 562 (48×56), 563 (34×30), 561 (30×60), 571–576.
  - Fixed: 560's west edge now joins **570** (offset 10/18), no longer 561.
  - Edges: 570 N(20) ↔ 562 S(22); 562 N(12) ↔ 561 S(10); 561 N(12) ↔ 160; 560 E(12) ↔ 140 W(32); 560 W(10) ↔ 570 E(21) (see 2i).
  - 561's Gullcry mouths are now arches in south-facing outcrop faces at (5,22) and (5,37). The links are unchanged.
  - Old specs live in `layouts/old_560_route5_route6.yaml`, `old_561.yaml` and `specs/564_gullcry_caves.yaml`.
- **Re-skins** (`layouts/reskin.py`, tileset 53): 520, 521, 524, 525.
  - Each keeps its plan, heights, events and links from `layouts/old_<id>_wilds.yaml` and is repainted with the kit (Sheridan ground, lanes, 2-face cliffs, log stairs, lattice forest, yard trees, greenfill).
  - 524/525 also get silk webs and strands.
- `ferrow.py`, `briarwick.py`, `route1.py`, `route2.py`, `gossamer.py` and `deepwood.py` are superseded. Their `__main__` refuses to run, because it would overwrite the new specs.
  - deepwood.py also wrote 548: to change 548's plan, lift its guard and re-run `reskin.py 525`.
- **Not yet on PF Rejuv:**
  - 109/110: the Dovetail is custom ship art.
  - 101–108, 121–125, 523, 526: interiors on tileset 34, whose walls and floors are already Rejuvenation's SheridanInside.
  - 522/548: Bleed glass art.
  - 130–133: held until the GYM_PUZZLES.md rewrite lands; only a re-skin is allowed.
- Rubric and screenshots are in the step reports. Previews `maps_out/previews/compare_100_vs_rejuv082.png` and `compare_120_vs_rejuv082.png`.
- Run order:
  ```
  python3 -I rcustom.py && python3 -I rcompose.py && python3 -I rstamps.py
  python3 -I layouts/ferrow_rj.py && python3 -I layouts/briarwick_rj.py && python3 -I layouts/rimewood.py
  python3 -I layouts/reskin.py 520 521 524 525
  python3 -I build.py --strict
  ```
  Install tilesets 50–53 with `merge_tilesets.py`. The `PF Rejuv` sheet is 256×75840 px.

## 2i. Fix round after the first engine playtest and preview review (2026-11-18)
**Playtest blockers (all fixed; `build.py --strict` now fails on them):**
- *Door tiles.* Rejuvenation-family door tiles are solid in their own tilesets, but our interior exits land the player ON
  the door tile. `rcompose.door_tiles()` / `patch_doors()` set passage 0 on the top tile of every stamp's door cell
  (shared wall pieces under it stay solid; `DOOR_FORCE` for sh_big's second door, which gets a "barred" sign through
  `rkit.EXTRA_DOORS`). `rstamps.py` re-applies it. Tileset 33 has the same fix as `compose_tileset.DOOR33`.
- *Arrival check.* `build.check_arrivals`: every Transfer Player of every built map must land on a passable tile that no
  solid event or decor covers, and when it lands on a door the tile below must be free (ARRIVAL warnings).
  `rkit.incoming(mid)` gives a layout the cells other specs warp onto; `reskin.py` keeps them bare. `scatter` never puts
  decor on an event's four neighbours.
- 100's north lane is the Ferrymen's Mile's dirt (x 32-34) for 7 rows before the gravel street; 103 barrel, 123 loft arrival, 521
  arrival, 145/154 arena front wall (`tile_edits`).

**Crowns (the "box" bug).** `RMap.stamp` keeps the overhead-only cells of tree-like stamps (`TREELIKE`) free: masks
`overm` (crown) / `bodym`; greenfill and the lattice grow under crowns, `blend=True` turns crown cells into forest,
`put_stamps` no longer deletes lattice trunks under a crown. `free()` / `snap()` / `can_tree()` treat crowns as occupied
for props, events and yard trees. Every ported piece was checked on a transparent board: none carries ground tiles.

**Snow autotiles (tileset 52 slots 4 and 5, both were unused):** `PF Packed Snow` (Terajuma DirtSnow re-graded to trodden
snow; class `d` on snow maps) and `PF Frozen Pond` (Reborn Still water snow frozen: 16-periodic ice bands, snow-bank rim,
terrain tag 12, passable; class `p`). Class `e` is exposed earth (KristilineDirt) for doorsteps (`rimewood.apron`).
Snow maps have no second ground tone any more. `rcompose.DERIVED` entries take `fn` / `tag` / `pas`.

**`rdraw.py` (new): hand-drawn pieces on the 16-px grid, appended to the `pf` part by rcustom (CUSTOM_ROWS 300).**
`wb_long / wb_long2 / wb_short / wb_inn / wb_smoke` whalebone longhouses (turf under snow, rib crosses, rib door arch),
`wb_gate` briar-wrapped rib gate, `fw_walk_*` rope walkways, `fw_smoke_a/w`, `fw_stall_e/i`, `fw_rack`, `fw_sled`,
`fw_skull`, `fw_wood`, `fw_brazier`, `fw_stone`, `fw_ban_e/i`, `fw_drift*`, `fw_hole(_t)`, `fw_pal_h/v`, `fw_peg`,
`fw_reeds*`, `fw_crack*`, `fw_floe*`, `fw_icy*`, `fw_tracks*`, `fw_fall` (frozen waterfall 4x5), `fw_log_n/m/s`,
`pf_anchor`. `python3 -I rdraw.py out.png` draws a contact sheet.

**Maps.**
- **570 Frostwick** rebuilt: Elowen treehouse terrace (NW, lip row 12) with rope walkways; the north band (lip 8) with
  the frozen fall beside the stairs; the Hearth Elder (Exchange door) on the square with two stall rows and the Hearth
  Stone; five longhouses; rib gate; palisade; jetty. Doors: loft (5,9), inn (19,21), Exchange (40,21), Border House
  (49,21), PC (6,35), Smokehouse (55,35). The Hearth Road is rows 23-25, so **570 E offset is 21** (560 W 10).
- **562**: the slide is the Hoar Pond (lobed blob, smoothed; islet with an Ice Stone). `slide_puzzle` searches stopper
  layouts with `slide_solve` (Essentials ice rules) until the islet needs >= 4 slides and can be left again. The ravine
  is irregular and the bridge is the fallen giant (`fw_log_*`).
- **560** rebuilt as a raised causeway (embankment, three stair flights, jog), brine pans, frost-pans, pegs, reeds; sea
  ice is dressed with decals (`dress_ice`), never filled. **520**: denser heath and sea rocks (`reskin.DENSE`).
- **100**: anchor monument in the square, greenfill 2. `RMap.frontage()` (house infill along streets) exists but found no
  free frontage: the plan is full. **120**: pale Goldenleaf decks with back rails, shrine stairs on the right lip row.

**Open.** Ferrow and Briarwick still have a cross-shaped street plan and no new terrace tier; interiors 101-108,
121-125, 523, 526, the Dovetail 109/110 and 522/548 are not re-skinned; `design/FIELD_DEFAULTS.yaml` did not exist;
nothing from NEW_SOURCES.md is imported yet (carchagui chalets and Magiscarf snow-capped trees are the candidates; both
are 16-px sheets with a baked checker background that needs keying). Gym and dungeon interiors belong to the puzzle engineer.

## 2j. Second polish round (2026-11-18)
- **Fields:** `build.py` reads `design/FIELD_DEFAULTS.yaml` (source of truth; a spec `field:` only fills gaps) and writes
  all 424 `MAP_FIELDS` entries, `:NONE` included, plus `MAP_WILD_FIELDS` from `wild:`. Test arena 990 has Wildfire and Meadow.
- **rdraw additions:** `fw_stair_l/m/r` snowy timber stairs (snow maps set `m.STAIRS`), `fw_ice0-3` soft lagoon ice
  (terrain tag 12 through code `I`; `rimewood.ice_at`), `fw_boat`, `fw_boat_over`, brown-bark `fw_log_*` with a root
  plate and a snapped crown, longhouse options `porch / pc / skull / patch` and the stamps `wb_long3`, `wb_hut`, `wb_pc`.
  `PF Frozen Pond` uses the same soft ice tones.
- **570:** curved lanes of varying width into one plaza (`lane` + `blob` + `smooth`), `doorstep()` runs a trodden line
  from each door to the nearest lane, the Center is a longhouse (`wb_pc`), five different longhouse shapes, boats, the
  brook and lagoon ice dressed with cracks and drifts. Doors: loft (5,9), inn (19,21), Exchange (40,21), Border House
  (48,21), PC (6,34), Smokehouse (55,34).
- **562:** ravine banks smoothed and opened (`smooth` x3, ragged bank clearing), floes and reeds along them.
- **Still open:** Ferrow / Briarwick street plans, NEW_SOURCES imports, interior / Dovetail / 522 / 548 re-skins.

## 2k. Map builder 7 (2026-11-18/19): town layouts, Saltmere rebuild, Dovetail on PF Rejuv, imports
- **Kit (`layouts/rkit.py`):** `smooth()`, `plan_cliffs()` (marks cliff cells at plan time so props and events never
  land on faces), `doorpath()` (trodden line from a door down to the nearest lane), `autotrees()` (single trees packed
  into leftover lawn), `keep_under` (sand / gravel / dirt autotiles keep painting under props, so freight on a quay
  shows sand, not grass; `self.under` / `self.eff`). **Bug fix:** `frontage()` demanded the street row itself be free,
  so it never placed a house; it now checks the footprint above the street only.
- **Sheet:** `rcompose.CUSTOM_ROWS` 300 -> 400 (pf is the last part: no id moved). rcustom appends, in order after the
  rdraw pieces: `EXTRA33` (tileset-33 harbour/market props as `hb_*`: boats, bollards, buoys, tubs, fish stall, barrels,
  tables, rug/wash/dye lines, sheds), `rdraw.pieces_late()` (`pf_pcsign`, the `ch_*` chalets from `rimport.py`),
  `EXTRA33_B` + `_ship_dovetail` (the Dovetail's deck art), `rdraw.pieces_late2()` (`pf_playhouse`). Append new things
  at the END of the last block only. New rdraw pieces: `fw_bridge_n/m/s` (snowy plank bridge with rails),
  `pf_pcsign`, `pf_playhouse` (14x12, door (7, 11)).
- **`rimport.py`:** keys a baked checker background by flood fill from the sheet border (white snow inside outlines
  survives), crops pieces to the 16-px grid, rcustom doubles them exactly 2x. Imported: carchagui's snowed chalets
  (`ch_chalet_a/b/c/pc/shop`; one is the trapper's lodge in 562). Magiscarf's snow-capped trees were style-tested on
  Frostwick and rejected (flat scale-leaf shading, saturated greens: they read as another game beside the lattice).
- **100 Ferrow (`ferrow_rj.py`):** the Center terrace (h=2) with its own stair, curved valley road from the Ferrymen's Mile into
  a plaza above the harbour with the anchor at the overlook rail, the bay cut into the bluff, two quay stairs, a
  timber wharf along the waterline with bollards, boats moored, freight and stalls on the beach. Doors moved: inn
  (11,27) -> (11,30), Mart (39,22) -> (46,28); PC, lab, customs, Dockmaster, lighthouse, pier arrival and the north
  lane unchanged.
- **120 Briarwick (`briarwick_rj.py`):** lanes curve into an oval green round the Gathering Tree; the PC is a timber
  hall (`sh_inn` + `pf_pcsign`), not the blue Help Center; more houses, a weavers' row house in a clearing. Doors moved:
  PC (45,23) -> (47,25) (HealingSpot [120,47,26]), Treetop House (55,24) -> (60,23), Mart (27,40) -> (29,43).
- **140/146/147 Saltmere (`saltmere_rj.py`, replaces `saltmere_city.py`; old specs kept as `layouts/old_14x_*_city.yaml`,
  the events' source):** same sizes, connection openings (140 N x 43-48, W y 32-34), touch warps and door links.
  Door cells: 140 PC (24,32) (HealingSpot [140,24,33]), Mart (58,30), Pageant Hall (46,26), House (26,6); 146 Harbour
  Office (52,26); 147 Playhouse / SM_GYM (44,18). `blockfill()` packs houses into wooded blocks with paths to the lanes.
- **109 the Dovetail (`dovetail.py`):** now tileset 51 (Rejuvenation Ocean with swells), ship_art deck from the pf part,
  `hb_*` freight. Event cells and PRISMFALL_START (7,6) unchanged. 110's cabin and the other interiors are unchanged.
- **570:** the brook bridges use `fw_bridge_*` (rails solid north/south, passage 8 / 1).
- **build.py:** spec generators whose file name is not an identifier (staging copies like `gen_gym1.new.py`) are skipped.

## 2l. Map builder 9 (2026-11-19): Saltmere as a harbour city, real stairs, the Rev 14 chain, the Chapter 0-4 roads
- **Kit (`tdraw.py`, the city kit, appended to the `pf` part through `rdraw.pieces_late3`, deduplicated):** stone and
  timber stairs redrawn as real steps (`st_stair_l/m/r`, `tb_stair_l/m/r`: two treads per tile with nosing, shaded riser,
  cheek wall or log stringer); `rw_*` terrace kit (balustraded lip, coursed face, footing; solid side copings
  `rw_W0`/`rw_E0`; ivy faces `rw_ivy0/1` as `vines`), `rw_rail_w/m/e` stone balustrade and `qy_rail_*` iron railing for
  lips, `pf_hounds` (the Loyal Three monument), `pf_planter0-3`, `pf_well`, `hb_glint0-3` (wave crests over water),
  `pf_chalkarch` (Lacecliff's sea arches, 7x5, walk-through), `dye_red/blue/yellow0-1` (the Dyers' Ford bands),
  `pf_stepstone0-1`. `rkit.KITS['rw']` is the terrace kit. **`build.py` already rejects the old flat slab (OLD SLAB STAIRS,
  `--strict`)**; no map uses it now.
- **rkit:** tall grass now stands on layer 2 over the ground grass (rubric bare / layer2; terrain tag unchanged).
  `seal_edges()` / `seal_against(conns, spans=...)`: on every side that has a connection, all walkable border cells are
  closed except the crossing span (both maps of a connection carry matching spans), so no edge tile leads onto blocked
  ground next door. Snow maps use a snowy stone (`m.SEAL`).
- **`build.py`:** `check_seams()` (SEAM warnings; `--strict` fails): every edge tile of a connection is walked across with
  Essentials' passability (the playtest's request 11/14). `trial_overlay.py` is merged like the puzzle EVENTS (below).
- **Saltmere (`layouts/saltmere_rj.py`, tileset 55):** 140 Upper Town (North Gate gatehouse, barred until S108; High Town
  terrace with balustrade and three stone stairs; ranks of townhouses and shops wall to wall with alleys, walled back
  gardens and courts; the market square with the fountain and the Loyal Three; Lantern Theatre, Lantern House, PC, Mart,
  bell tower; the promenade with iron railing and plane trees; the salt lake with pans; causeways to 146 and 147), 146 Harbour
  (customs house on Harbour Square, warehouse rows, cranes, bollards, two ships at Quay Street, fish market on the West Mole,
  the Legion berth on the East Mole, the breakwater with the striped light), 147 Old Town (Players' Gate, three terraces
  and stairs, the Pell Playhouse above a 12-wide grand stair, the Little Lantern and the costumiers, Theatre Square with
  playbill columns, lantern strings, stalls and the crowd). Chapter 2 events re-poured from the script: J1 on the green
  before the gym, Dorian at the breakwater, Salt-caramel (`:ch3_juno_talk`) after the gym, Kestrel after S108, the
  Chapter 2 close (V102 = 3). The puzzle engineer's audience keys (`pfm_audience`) are on the 18 named townsfolk.
- **Roads (`layouts/routekit.py` + `layouts/routes_early.py`):** 520 (64x110), 521 (120x70), 527 (140x64), 528 (110x80),
  541 (70x110), 552 (80x72), 540 (130x64), 524 (90x110), 566 (80x120), 577 (72x96), 578 (80x88), every leg with its
  ROUTES.yaml landmark, side path, secret and the script's events. `routekit.Route` recipes: `road` (a lane with open
  land), `forest_band`, `copse`, `clearing`, `sea` (beach and cliff), `terraces` + `crossing`, `pocket` (a secret behind a
  Cut tree), `exit`, then `seat_events`, `dress`, `paint`, `write` (seals the edges, seeds the reachability check at every
  exit). The old `reskin.py` refuses 520/521/524 now; their previous specs are kept as `layouts/old_*_reskin.yaml`.
- **Rewired (SWAP_GYM1_GYM2 1A):** 100 N <-> 520 S; 520 N <-> 521 S; 520 W (Hale Bell, the quarantine roadblock) <-> 527 E;
  527 W <-> 528 E; 528 W <-> 140 E (East Gate); 140 N (North Gate) <-> 541 S; 541 N <-> 552 S; 552 N <-> 540 S; 540 E <-> 524 W;
  524 N warps <-> 120 S; 521 W warps <-> 524 S (the corded forest road, open from the wood when V105 >= 1); 120 N (North
  Gate) <-> 566 S; 566 N <-> 577 S; 577 W <-> 570 E; 570 N <-> 578 S; 578 N <-> 562 S; 570 S <-> 560 N (the Causeway's west
  end turned north; the Isenmar customs chain at the Border Stones unhooks from the Frostwick side); 560 E <-> 140 W. The
  `R3_COCOON` warp is gone (548 is entered from the Deepwood only). Gym checks use `pfm_gym_won?(:LEADER_...)`.
- **Trial events (`mapgen/trial_overlay.py`):** the Chapter 0-4 events of `design/TRIAL_EVENTS.yaml` laid over other
  scripts' maps at build time (seated on the nearest reachable free cell), and the `pf_trial_ready?` branches on the
  existing NPCs. Skipped on purpose: the Timburr gift and its planks, the tide-pool duel and its sea cave. New interiors
  (`layouts/trial_interiors.py`): 148 Saltmere Lantern House, 126 Briarwick Lantern House, 168 the Net Loft; 542 the
  Brinewife's Rest re-tiled.
- **Run order:** `rcustom.py && rcompose.py && rstamps.py`, then `ferrow_rj, briarwick_rj, rimewood, dovetail,
  saltmere_rj, routes_early, trial_interiors`, then `build.py`, then **the layouts and `build.py --strict` once more**
  (edge sealing of town maps reads the neighbours' built maps where no span is given).

## 2m. Map builder 10 (2026-11-19/20): crafted roads, the nature kit, Saltmere polish, Ebbmouth, the Rehearsal
- **Crafted roads** (`layouts/routes_craft.py` on `layouts/craftkit.py`; `routes_early.main()` dispatches 520, 524, 527,
  528, 540, 541, 552, 577, 568 there): elevation with cliffs, plateaus and stairs (`CK.plateau`, `CK.stair` protects its
  landings), one-way ledges (`CK.ledge`, terrain tag 1, faces grass / chalk / dune), mixed species woods (`CK.woods` lattice
  zones per palette ELOWEN / COAST / GOSSAMER / SNOWWOOD) with `fringe` trees and `undergrowth`, streams with stepping
  stones, ponds, falls, shore detail (`CK.shore`: wet sand, wrack, shallows, rock pools), meadows and grass fields, salt
  pans (`CK.pans_varied`, four brines), boardwalks, silk drapes. `CK.seat()` seats a building at the nearest legal spot.
  `CK.scatter_quiet` lays walkable decor only (solid bushes walled a talker in on 540 and a field on 568).
- **Nature kit** (`mapgen/ndraw.py`, appended to the `pf` part by `rdraw.pieces_late4`; rcustom dedups): ledges, coast,
  chalk sea arches and stacks, landmarks, drystone walls, silk, the road mechanics' pieces, salt / dye / boardwalk, the stone
  bridge, mill-wheels, the Lattice intake, Bleed veil and frozen gusts, the tipped wagon, and the imported J-Treecko252
  crystals (`art/imports/`, x2 halved to the 16-px grid). **Adding a piece shifts every later id: after any sheet change
  relay and rebuild every crafted map** (rcustom, rcompose, rstamps, then the layouts, then build.py), or SEAM warnings appear.
  New tileset **56 "PF Rejuv Shore"** (the `shore` route theme).
- **Mechanics** (flags V601-604, V536): 577 wind-gap gusts (`pfp_metronome`), 552 sluice stones and the cloth barge, 541's
  night Drowned Lane, 528 sledge run, 566 Ram Race (`$stats.distance_walked`), 568's frame clock (`pfp_step_hook` +
  `pfp_step_clock`). `build.py` event pages take `route:` (rpg.route_cmds DSL), `speed:`, `freq:`.
- **Story gates are proven:** a spec's `gates: [{name, from: [[x, y]..], sealed_edge / sealed: [[x, y]..]}]` makes build.py
  flood-fill with every first-page blocker standing solid and fail `--strict` on a leak (`GATE ok` lines in the log). 520's
  Hale Bell roadblock and 568's gust walls use it; `tools/harness/playtest/seam_check.py --events` agrees.
- **Saltmere** (`layouts/saltmere_rj.py`): curved and diagonal streets cut before the blocks (`street()`, `m.smask`; houses
  step down a slanting street with `stepped_rank`), 147 rebuilt off-centre (no mirror), salt works packed per field
  (`salt_works`, four brines, boardwalk jetties), green / salt-crust verges at the gates. Interiors 143-145
  (`layouts/saltmere_interiors.py`; 145 is a hallkit theatre on tileset 54).
- **Ebbmouth 160 + Mill Quay 167** (`layouts/ebbmouth.py`, PF Rejuv Snow with the Rimewood kit): open black river, lock,
  bridges, mill-wheels, quays, the frozen reach. **568 The Rehearsal** in routes_craft. **548** gets its glass ravine
  (`layouts/deepwood.py 548` writes 548 alone).
- **The war theatre** (`layouts/war.py`): 920, 924, 925, 926, 928, 929, 930 on PF Rejuv Shore with the war kit (`wr_*`:
  tents, the war-tent, trebuchet, pickets, sled-forts, banners, wells, burial carts, tally-wall, Meridian tripods and
  telegraph; trench, ember, frost, steam, ripple, rut and bone decals). Desert ground is the Dirt autotile with layer-1
  variants (`frozen_ground`, `ground_var`) and top-layer decals; dune crests are one-way sand ledges (plateaus on sand
  show the kit's grass rim). `gate_check` reads passage bits directionally, so one-way ledges count; a stepped ledge line
  leaks at every step, so story ledges run straight. Never lay a priority-0 decal over a solid prop.

## 2n. Map builder 11 (2026-11-20): Juno follows, the passability guard, the Glass Dunes kit
- **Juno as a follower** (`mapgen/ruby/010_JunoFollower.rb`, Essentials v21.1 Followers; doors already call
  `Followers.follow_into_door`): `pfm_juno_join(:leg[, "Event"])`, `pfm_juno_part(["Event"])`, `pfm_juno?`. The leg
  (`pfm :juno_leg`) is the record; `on_enter_map` re-syncs it (old saves), hides her in the Glassed Orchard after Lecture
  One (`JUNO_WAITS`: the map's Juno waits at the gate), erases her stand-ins on 100/103 (`JUNO_STANDINS`), and Juno's
  portrait bubbles point at the follower when none of her map events is on show. Legs: errand (100 lab yard -> 522 gate;
  after Lecture One -> the 523 bed), Saltmere (523 send-off -> the 140 arrival, she runs off), Weavers' Road (140
  chapter close -> the 120 arrival). Talking to the follower does nothing (no common event).
- **passguard** (`mapgen/passguard.py`): Essentials' `playerPassable?` stops at the first passable priority-0 tile,
  top layer first, so a decal over a solid tile makes it walkable. A *decoration* is a passable priority-0 sheet tile
  that is not a walking surface (kit names: `WALK` regex; unnamed tiles: coverage < 0.9; `SURFACE_IDS`). `hits()` = cells
  the player can walk onto only because of one; `build.py` warns `PASS` and `--strict` fails. `guard()` is the fix every
  raw writer applies (`rkit.Map.write`, `hallkit.Hall.write(mid, event_cells)`): the decoration moves down a layer and an
  invisible solid sheet tile (`blocker()`) goes on top, so the picture is unchanged; with no room the decal is lifted.
- **The Glass Dunes kit** (`mapgen/gdraw.py`, appended LAST in `ndraw.pieces()`; it shifts the chalk / snow / silk /
  dye copies after the pf part, so after any sheet change re-run every layout: ferrow_rj, briarwick_rj, dovetail,
  ebbmouth, rimewood, saltmere_rj, saltmere_interiors, orchard, trial_interiors, early_interiors, war, routes_early,
  `reskin.py 525`, then restore `specs/525_deepwood_cocoonfall.yaml` from git (reskin rewrites it; 548 is built by
  `deepwood.py 548` only) and build): glass floor `gd_g*`/`gd_gc*` (layer 1 ground), the glass sheet edge `gd_floor_NN`
  and flood water `gd_flood_NN` in the 48 autotile shapes, cliff kits **`gdc`** (glassed) and **`sdc`** (sandstone) with
  no grass anywhere (rkit `KITS`), one-way ledges `gdl_*` / `sdl_*` (`CK.ledge(face='glass'|'sand')`), fords, steaming
  pools, the frozen wave `gd_wave` (6x5), glass shards, rope / crack / spill decals, and war pieces (`wr_treb_broken`,
  `wr_tower_wreck`, palisades `wr_pal_h/hb/v`, `wr_stakes`, `wr_sandbags`, torn banners, `wr_supply`, `wr_sacks`,
  `wr_firering`, `wr_rack`, `wr_glasssled`). `python3 -I gdraw.py out.png` draws a contact sheet.
- **War maps** (`layouts/war.py`): the green rims had two causes, both fixed for every war map: the Rejuvenation
  road / dirt autotiles carry a grass edge, and the shore theme lays grass on layer 1 under everything. `trail()` plans
  roads as sand (road_mask still works: ruts, causeways); `sand_seams()` re-shapes the Dirt autotile so height changes
  don't cut it and puts sand (salt crust where hidden) under every piece. Desert edges are sealed with sandbags / stakes
  / sacks / glass clusters (`m.SEAL`), not green bushes. Helpers: `blob`, `band`, `paint_glass`, `plan_flood` /
  `paint_flood`, `ridge`. 926 is rebuilt (glassed crest and ridges, flood channels with one causeway, the frozen wave,
  steaming pools, broken siege engines, both armies' lines and camps, stake lines, dune slides, two lookout stairs);
  920/924/925/929/930 densified; 928 furnished. All map builder 10 event wiring is unchanged.
  Before/after: `maps_out/previews/war_compare/`.

## 2o. Map builder 12 (2026-11-20): the Chapter 2-4 audit, Rimewood Path and Gullcry Cliffs recrafted
**Audit** (every map from Saltmere's North Gate to Gym 4, graded against the map builder 10/11 roads and Saltmere/Ebbmouth;
A = that standard, F = stock FRLG tiles or bare). Ch3: 541 Grey Saltings B, 544/545 Brinecut Mine **F** (stock Rock Cave
template), 542 Brinewife's Rest C, 552 Dyers' Ford B- (the three dye bands are ruler-straight), 540 Thistledown Lea B,
546/547 Thistledown Manor **D** (stock mansion tileset), 524 Gossamer Wood B-, 526 C, 120 Briarwick B, 121-126 C+, Loomhouse
130-134 B- (puzzle engineer), 525 Gossamer Deepwood **D** (the old reskin: flat lattice and boxy lanes), 548 Cocoonfall B-.
Ch4: 566 Spinners' Rise C- (routekit: repeated straight terrace bands, noise grass), 577 Frostwick Pass C+, 570 Frostwick B,
571-576 C+, **578 Rimewood Path D -> B**, 562 The Rimewood C, 563 Glade C, **561 Gullcry Cliffs D -> B-**, 564 Gullcry Caves
**F** (stock Rock Cave), 565 not built, 560 Causeway C+, 568 Rehearsal B-, 160 Ebbmouth B, 167 Mill Quay B-, 161-165/168 C,
**170-174 Tidelock Gym F** (stock Harbour/Gym tiles, bare grey basins; GYM_PUZZLES also wants its puzzle trimmed and rebuilt).
Ch5 (580-595, Lumen 180-193, Gym 4) is not built. Worst left, in order: Tidelock Gym; the three caves (544, 545, 564; they need
a PF cave sheet, see below); 546/547; 525; 566. Before/after: `maps_out/previews/ch2_4_compare/`.
- **578 Rimewood Path** (`routes_craft.build_578`): three snow terraces with stairs, the Long Ice (the Hoar Brook frozen
  straight under the crag: step on by the stair and slide west to the frozen fall and the charcoal burners; an ice-block
  stopper drops the lower row at the snare nook), the Silk-fall glade behind a **frozen silk curtain** (Rock Smash:
  `pfm_smash_silk` in `ruby/006_MapStory.rb`, charset `graphics/Characters/pf_rime_curtain.png` from `mapgen/charsets.py`),
  the Unblazed (blue blaze -> glade A -> B -> the herd: wrong turns are touch warps across the whole trail width back to the
  blaze; the Stantler stag is a wild battle, Lv 19), a second curtain as the herd's shortcut, a snow-bank ledge, the lean-to,
  hives, woodcutters' yard. `gates:` proves the Silk-fall shut. No trainers: PBS has none for 578 (ROUTES wants 5).
- **561 Gullcry Cliffs** (`routes_craft.build_561`, now 64x130 as ROUTES.yaml says; `rimewood.py 561` refuses): cliff-top
  road, four headlands with south faces and coves, the stilt hamlet down a plank stair, the signal fire, whalebone
  waymarkers, frozen rock pools, the landslide (rows 55-70, heath to sea) with `gates:` proving the caves are the only way
  north, both cave mouths re-seated at the crag feet (564's arrivals follow the links), the Gannet Stair to the isolated
  rookery cove (Cramorant: Big Pearl), Kestrel (K2) in a one-tile gap between two tors. Connections and offsets unchanged
  (N x 10-13 -> 160, S x 10-13 -> 562). Trial anchors for Old Asta and the egg ledge moved in `trial_overlay.py`.
- **577**: the Icium Z (SPINE Rev 23) in an avalanche gully in the east wood behind a Rock Smash boulder (event from
  `trial_overlay.py` EVENTS[577], gate-proved).
- **Kit:** `gdraw.pieces()` gained (at its end) `lgs_w/m/e` snow ledges (`CK.ledge(face='snow')`), `gd_sheen0-3`,
  `gd_sky0-1`, `gd_spire`, `pf_whalebone`; `routes_craft.near_flat()` (r.near that keeps off cliff faces and roads);
  `CK.undergrowth` no longer stamps on cliff faces. **`mapgen/relayout.sh [--strict]`** runs the whole post-sheet-change
  order (rcustom, rcompose, rstamps, every layout, `reskin.py 525` + the 525 spec restore, build). Then re-run
  `rimewood.py 562` and build again when 561's edge moved (562 seals its N edge against the built 561).
- **Lesson:** a band of class `T` thinner than the 3x2 tree footprint leaves walkable gaps (and lattice canopies can close a
  lane next to a wood). Where a wall matters (a gate, a trail maze), fill unpainted `T` cells with a solid snowy shrub
  (10371/10551) and prove it with `gates:`.

## 2j. Puzzle interiors: tileset 54, the puzzle runtime and the solver (puzzle engineer)
- **Tileset 54 "PF Rejuv Halls"** (`compose_halls.py`; offsets in `data/halls.json`): only the sheet rows that Rejuvenation's
  own Sensei's House / Goldenleaf interiors (`Multi-Interiors`) and Goldenleaf Theatre / Backstage (`Multi-Gym Interior`) use,
  plus Prismfall's silk props from PF Rejuv's `pf` part and drawn puzzle pieces (heddle posts in five colours with shape-coded
  threads, warp beds, planks, scenery drops labelled wave / leaf / crown and flats lettered A/B/C for colour-blind players,
  marks, treadles, knot threads, gears, spools). 256×8704 px. Seats, curtain fringe, posters and loom tops are made solid.
- **`layouts/hallkit.py`** paints a glyph grid in three looks (`loom` timber hall, `stage`, `lobby`), with automatic frame
  edges, wall posts, doors, seat blocks, the stage lip, and helpers for exact-value tile events and the apprentice NPC.
- **`mapgen/puzzles/`**: the room models (`loomhouse.py`, `playhouse.py`, `dungeons.py`) hold the layouts the generators
  paint, so map and proof cannot drift. `build.py` runs every proof twice: on the design grid, and on the built
  `MapNNN.rxdata` with Essentials' passability and event-page rules (`built.py`). It also writes
  `Plugins/Prismfall Maps/007_PuzzleRooms.rb` (reset / solved state / hints) from the same data, and `--strict` fails on any
  unsolvable room, soft-lock, wrong minimum, or a room harder than its 1–10 rating. `python3 -I mapgen/puzzle_check.py`
  runs the design proofs alone. Events laid over maps another script owns (D1's chime rows on 522) come from a module's
  `EVENTS`, so the layout owner's script is untouched.
- **Runtime:** `plugins/Prismfall Puzzles/` (the `pfp_*` helpers of GYM_PUZZLES §3); Core's `puzzleskip` password (S301);
  `mapgen/ruby/008_GymOrder.rb` (`pfm_gym`, `pfm_gym_won?`).
- **Engine proof:** `tools/harness/playtest/run_puzzles.sh` (own game copy, own display) + `002_PuzzleBot.rb`;
  media in `docs/playtest/puzzles/`.

## 3. Regenerating
```
cd fangame/mapgen
python3 -I build.py            # all specs  -> maps_out/ (runs gen_*.py spec generators first)
python3 -I build.py 100 520    # only some maps (links are still resolved against all specs)
python3 -I build.py --grid     # previews with a coordinate grid (yellow = every 5 tiles)
```
`build.py` checks itself as it goes. It also warns when an event has no walkable neighbour, using Essentials'
`playerPassable?` rules (Neutral tag ignored, bridge tiles ignored off-bridge). It reads every written map back, warns about unresolved door links, transfers to maps that
aren't built yet or that land off-map, 1-tile-thin paths and snapped trees, and it writes `trainers_needed.txt`.
Extra checks:
```
python3 -I verify.py roundtrip ../maps_out/Data/Map*.rxdata             # write->read deep equality
python3 -I verify.py compare ../maps_out/Data/Map100.rxdata <ref Map002> # class/ivar structure vs a real RMXP map
ruby ruby_check.rb ../maps_out/Data/Map*.rxdata                          # Ruby's own Marshal loads OUR files
```
The one-time mining tools read the reference project read-only with the pure-Python parser:
`extract.py` (stamps and interior templates → `data/`), `dump_ref.py` (`data/tilesets.json` and friends), `learn.py` (tiling
rules), `probe.py` / `find_buildings.py` (research). They only need re-running to add stamps or templates.

## 4. Spec format (`mapgen/specs/*.yaml`, several maps per file with `---`)
```yaml
id: 100                      # map ID (WORLD.md scheme). 990-999 = dev/test. Avoid 999 (Essentials' random dungeon).
name: Ferrow's Landing       # RMXP map name; also the PBS Name unless metadata.Name is given
parent: 0                    # MapInfos parent (interiors -> their town)
palette: outside             # palettes/<name>.yaml (glyph legend + tiling rules for one tileset)
bgm: Lappet Town             # Audio/BGM name, autoplayed
metadata: {Outdoor: true, ShowArea: true, MapPosition: [0, 14, 26], BattleBack: field}   # -> map_metadata_prismfall.txt
connections: [{dir: N, offset: 17, to: 520, to_offset: 10}]   # -> map_connections_prismfall.txt (once per pair)
field: SILKWOOD              # -> manifest.json fields (FieldEffects::MAP_FIELDS); staged: field: [FLOWER_GARDEN, 3]
tone: [-18, -30, 4, 12]       # screen tone on entry; fog: {name: prismfall_spores, opacity: 46, blend: 1, sx: 1, sy: -1}
map: |                       # ASCII terrain, one char per tile (legend in the palette)
  TTTT....::::....
stamps:                      # multi-tile buildings at their top-left corner; a stamp with a door adds a door event
  - {stamp: pokecenter, at: [6, 11], link: FL_PC}
tiles: [{tile: gym_sign, at: [24, 9]}]          # single named tiles from the palette
events: [...]
```
**Interiors** use a template instead of `map:`. Set `template: pokecenter|mart|house|house2|lab|gym|arena|harbour|bigroom`,
`exit_link: FL_PC` (the template's Exit mat links back to that door), `drop_template_events: [names]`,
`stretch: [[x|y, index, count]]` (repeats a row or column to resize a room), and `tile_edits: [[layer, x, y, tile] | [layer, x, y, w, h, tile]]`.

**Layout scripts** (`mapgen/layouts/<town>.py`, so far Saltmere) write a spec's `map:` ASCII and its decoration lists between
`# LAYOUT-DECO-BEGIN/END` markers. Run one after editing it, then run build.py. `tileblocks:` places rectangles of tileset art by
top-left tile id: the fountain 1501 [3,4], the lighthouse 3941 [3,8], a ship 4349 [3,3], rowing boats 4318 [2,3],
benches 1437 [3,1], planters 1485 [3,2], lamps 1408 [1,3]. Single objects go in `tiles:`: barrels 1536–1538, crates 1376–1381,
rocks 1328/1329, saplings 1331, flower pots 1340/1341.

**Outside glyphs** (`palettes/outside.yaml`):
| Glyph | Terrain |
|---|---|
| `.` | grass (random detail) |
| `,` | tall grass (encounters) |
| `T` | forest (2×2 trees snapped to even coordinates, canopy overhang) |
| `:` | light path |
| `_` | sand path |
| `~` | sea / water (Sea autotile) |
| `W` | deep water |
| `s` | sand shore |
| `*` | flowers |
| `f` | fence |
| `L` | ledge (jump south) |
| `=` | wooden pier over water |
| `h` | water under a harbour stamp |
| `#` | building footprint (ground) |
| `c` | grey cobbles (blob rules mined from Cedolan City) |
| `C` | cliff face band (1187/1188/1193 faces; 1184/1185/1186 base lip on the row below) |
| `S` | stone stairs cut through a cliff band (1161) |
Paths and blobs should be at least 2 tiles wide.
**Gym (rock theme) glyphs** (`palettes/gym_rock.yaml`): `.` floor, `_` plank floor, `v` void (impassable), `o` boulder,
`#` wall (faces and side edges drawn automatically).
**Stamps** (`data/stamps.json`): pokecenter, mart, gym, lab, house_red, house_red2, house_blue_a/b (no door), fanclub,
condo, institute, daycare, harbour_pier, mailbox.

**Event types** (`at: [x, y]` on every event):
| Type | Fields | Becomes |
|---|---|---|
| `npc` | `sprite`, `dir`, `move: fixed\|random`, `text` or `commands` | action-button NPC |
| `sign` | `text`, `post` (default true: adds a sign tile) | |
| `item` | `item: POTION`, `hidden` | Essentials `pbItemBall` pattern: "Item" / "HiddenItem" |
| `trainer` | `trainer: [TYPE, Name, version?]`, `sight`, `dir`, `sprite`, `intro`, `after`, `rules: ['setBattleRule(...)']` (e.g. `'setBattleRule("fieldStage", 3)'` for a pre-grown Flower Garden) | the exact structure Essentials' compiler produces: `Trainer(N)`, `pbTrainerIntro`, `pbNoticePlayer`, `TrainerBattle.start`, self switch A, `pbTrainerEnd`, defeated page |
| `door` | `link` or `to: {map, x, y, dir}`, `gfx: [charset, pattern, dir]` | Essentials' animated door, 2 pages incl. switch 22 |
| `exit` | `link` | interior exit mat, "Door exit" SE |
| `warp` | `to: {...}` or `link`, `arrive: [x, y, dir]`, `se` | touch transfer |
| `berry` | `berry` | |
| `cut_tree` | | "CutTree" event: `pbCut` → `pbSmashEvent` |
Doors from stamps get the lowest event IDs on a map, so their arrival autorun runs before story autoruns.
| `mart` | `items` | |
| `pc` | | |
| `event` | raw `pages`: `cond {switch, switch2, var: [id, min], self}`, `graphic {sprite, dir, tile}`, `trigger action\|touch\|event_touch\|autorun\|parallel`, `move`, `through`, `commands` | full control |

**Command DSL** (inside `commands`):
- `"text"` → message. A `\n` adds a line to the same box.
- `{script: "..."}` → multi-line script.
- `{if: "ruby cond", then: [...], else: [...]}` → conditional branch. Also `if_switch: [id, on]`, `if_self: [A, on]`, `if_var: [id, value]`.
- `{choices: [...], cancel: n, branches: [[...], ...]}` → show choices.
- `{switch: [id, on]}`, `{var: [id, value]}`, `{selfswitch: [A, on]}`, `{transfer: {map, x, y, dir}}`.
- `{se: name}`, `{me: name}`, `{wait: n}`, `{heal: true}`, `{tone: [r, g, b, gray, frames]}`.
- `{move: {who: -1|0|id, route: ['up', 'wait 2', {jump: [dx, dy]}, 'through_on', ...]}}`.
- `{boss: {id: GLASS_MATRIARCH, species: GALVANTULA, level: 16, field: BLEED}}` → story boss (see §6).
- `{comment: ...}`, `{raw: [code, params]}`.
Door/warp `link` keys pair an exterior door with an interior `exit`. The builder computes both directions: you arrive one tile
above the mat facing up, and leave onto the door tile, where the door animates you out.

## 5. Base-project compatibility
- Verified identical between `ref/ebdx` and the **EBDX Renovation** fork: all 25 tilesets (IDs, names, graphic and autotile names,
  passages, priorities, terrain tags), every tileset and autotile PNG (md5), and System switch 22 = `s:tsOff?("A")`. The two
  `Tilesets.rxdata` files differ in bytes only (string encoding style), so the generated maps target both forks unchanged.
  The forks' `MapInfos.rxdata` differ, which is why the installer merges into the user's own file.
- Strings are written Ruby-1.9-style (`I"…"` + `:E => true`, UTF-8), as Essentials' own compiler writes maps. RMXP opens these
  (the base project's sample maps contain them). Strings read from the user's MapInfos keep their original style.
- Tile and terrain knowledge came from the sample maps: `learn.py` mined the 8-neighbour tiling rules for trees, light and sand
  paths, and ponds; `find_buildings.py` and `extract.py` took the buildings; I checked everything visually.
  Autotile shapes use Essentials' own `NEIGHBORS_TO_AUTOTILE_INDEX` table (map edges count as "same").

## 6. Known limitations / TODO
- Only stock base-project art. Briarwick's six giant hollow trees and rope bridges are drawn as forest clumps; Gym 1 uses the
  rock-gym theme of the Gyms tileset, with no silk/web art; there is no ship sprite, so the Customs Hall template's moored ship
  stands in for the Dovetail. Real art needs custom tiles.
- No cliffs or mountains yet. Outdoor barriers are trees, water, fences and ledges. The Lighthouse is a condo stamp.
- The stock ships and boats in the Outside tileset are cut at the sheet's right edge (the hulls continue off-sheet),
  so ships may only sit flush against a map's right edge. Saltmere's ship does.
- Not built yet:
  - Gullcry B1F (565) and The Rehearsal (568, :BLEED): signs.
  - Reyes Cellar (166): the cellar door is barred.
  - Routes 7–8 (580/581), Lumen City (180–193) with Gym 4, the Meridian gala and the Lowlight Shatter (Act I finale):
    Ebbmouth's east edge stays closed with trees until 580 exists.
- The River Ebb's day/night current flip in town is not done; the Outside tileset has no current autotiles. Gym 3 uses
  event-driven currents instead.
- The mine and Gullcry Caves share the base project's Rock Cave template, so they look alike: [TODO art].
- Deviation from maps.json: The Grey Saltings's north edge joins Thistledown Lea's **south** edge at x=2–9. maps.json paired 540-west with
  541-north, which isn't a legal Essentials edge pair.
- Story items without item data (Meridian badge case, Fellowship card, Gilded King page, Granny Loom's shuttle) are text
  only. Add key items, then swap the text for `pbReceiveItem`.
- Story bosses: `mapgen/bosses.yaml` → generated `Plugins/Prismfall Maps/003_StoryBosses.rb`, which calls
  `Prismfall::Bosses.register(:ID, {...})` behind `if defined?(Prismfall::Bosses)`. Events use the DSL command
  `{boss: {id, species, level, field}}`. That runs `Prismfall::Bosses.wild_battle(:ID)`, or a plain `WildBattle` with the same
  species, level, field and cannotRun when the plugin is absent. So far: `:GLASS_MATRIARCH` (Galvantula, 2/3/3 bars, :BLEED).
- Dialogue is placeholder `[TODO story]` text, except gym mechanics from GYM_PUZZLES.md.
- Trainers in `trainers_needed.txt` (route and gym trainers, Test Arena `YOUNGSTER Ben`, a base PBS trainer) must exist in PBS.
- RMXP can only test variable conditions with ">=", so each plank uses two pages (show at ≥k, hide at ≥k+1).
- Previews show the initial state. They don't show priority above the player or animated autotiles.
