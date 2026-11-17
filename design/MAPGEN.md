# MAPGEN — generated RPG Maker XP maps for Prismfall

The map generator turns readable YAML specs into real RMXP map files (`Data/MapNNN.rxdata`) for Essentials v21.1 + EBDX, using
the base project's stock tilesets. Code and specs live in `mapgen/`, output in `maps_out/`.

## 1. What's built (Act I, in story order)
| IDs | Maps | Story / mechanics |
|---|---|---|
| 109–110 | The Dovetail: deck and cabin (prologue) | FINAL script (§2f): title card, appearance, manifest name, difficulty; Edda's rail scene, Voss and `:pro_fellowship`, checkpoint, gangway opens on S101; six passengers, cook, trunk, letter |
| 100–108 | Ferrow's Landing and interiors | FINAL script (§2f): docking, Edda's last call (GO_HOMEWARD), the NULL scan and title card, Larch/Sanctuary/starter/Kestrel, K1, Rowan, Juno's errand, Ch1 end at the inn, Larch's send-off, Wingull and Lamplighter sidequests, Hesper |
| 520, 521 (+523) | Route 1, Route 2 (+ Hale Farmhouse) | The Route 2 cordon guard lets you through once K1 is done |
| 522 | The Glassed Orchard (:BLEED) | Bleed Veil scene with Juno: GO-02 choice, the Wurmple calm, Larch's Field Notes line (S105) |
| 524–526 | Gossamer Wood, Deepwood, Woodward's Hut (:SILKWOOD) | Silk-wall loop, Cut tree to Deepwood |
| 120–125 | Briarwick and interiors | Thistle at the pylon (HOLLOW_THISTLE, S106), Loyal Three shrine, poster, Celestine (S170) |
| 130–133 | Loomhouse Gym (Gym 1) | Heddle planks, spool ziplines, then `Prismfall.gym_battle(1)` → `award_badge(1)`. Tamsin's confession and the `CH2_TAMSIN` choice |
| 540–542, 548 | Route 3, Route 4 (:BEACH), rest house, Cocoonfall Hollow (:BLEED) | Crystal silk opens once `pf_choice(:CH2_TAMSIN)` is set. Glass Matriarch: `Prismfall::Bosses.wild_battle(:GLASS_MATRIARCH)` (S107, V105=1, V102=3) |
| 544–545 | Brinecut Mine 1F/B1F (:CAVE) | Built on the Rock Cave templates. Links Route 3's mine mouth with Route 4's back door. Salt miner gives TM98 after Badge 2 |
| 546–547 | Thistledown Manor + Attic (haunted house) | Mansion tileset (`palettes/mansion.yaml`): checker foyer with a grand staircase, arched-window portrait hall, dust-sheeted dining room, ruined cobwebbed attic. DarkMap. Three ghost scenes (wrong line → ghost battle). Lady Thistledown's offer: GO-03 or Spell Tag + Litwick (S176). Greavard in the attic |
| 560, 561, 564 | Route 5 (salt flats), Route 6 (sea cliffs, landslide detour), Gullcry Caves | K2 (Trainer(4) sight event, `Prismfall.rival_battle(:RIVAL_KESTREL, "Kestrel", 2)`), `CH4_KESTREL_MOURNER` choice, S111, V114=1. Gullcry reuses the Rock Cave template |
| 160–165 | Ebbmouth and interiors | Rain. River Ebb with footbridges, Meridian tidal Lattice. Teo night scene (after K2): HOLLOW_TEO battle, `CH4_TEO` choice, S112. Good Rod (Anglers' Guild). Ice-fishers' whale song. Larch's tide-data revelation after Badge 3 |
| 170–174 | Tidelock Gym (Gym 3, :WATER_SURFACE) | Harbour tileset (`palettes/harbour.yaml`). Low/Mid/High basin variant maps. Sluice wheels W/C/E transfer to the same x,y on another level. Mid: raft events (passable plank tile) to the bell-rope. High: current lanes (forced moves). The north lane reaches the exit only with the tide bell ON (S315). Marisol `gym_battle(3)` → Badge 3, TM03 |
| 140–145 | Saltmere and interiors | J1 and the `CH3_JUNO_TALK` choice (S109). After Badge 2, the Pageant: Mourner speech, grunt double battle, Gilded King page (S108, V102=4). Kestrel's exit, the royal notice |
| 150–154 | Pell Playhouse (Gym 2, :GRAND_STAGE) | Revolving-stage wheel (scene order, actor battles, CUT), fly-loft spotlights with coupled rigging, Comedy door. Dorian double battle → Badge 2, TM42, Eevee "Understudy" (S110) |
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
  - Gym 1: V305–307 heddles, S305–307 cords.
  - Gym 2: V310 scene, V311 acts, V312–314 spotlights; S310 ladder, S311 mask, S312 trapdoor, S313 spotlights initialised.
  - Gym 2 actor-beaten flags are self switches B/C/D on the wheel event.
  - Gym 3: S315 tide bell (ON = currents run inland/north). Water level = which variant map you're on (no variable).
  - Story IDs also used now: S111 CH4_K2_DONE, S112 CH4_TEO_MET, V114 KESTREL_STAGE (set to 1 after K2).
- The base project's System.rxdata defines 100 switches and 100 variables. Raise the maximum in Database → System to see names for the higher IDs.

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
  its Route 4 (N, offset 44) and Route 5 (W, offset 32) connections. Districts are joined by touch warps: harbour
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
- Deviation from maps.json: Route 4's north edge joins Route 3's **south** edge at x=2–9. maps.json paired 540-west with
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
