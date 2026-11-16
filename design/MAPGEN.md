# MAPGEN — generated RPG Maker XP maps for Prismfall

The map generator turns readable YAML specs into real RMXP map files (`Data/MapNNN.rxdata`) for Essentials v21.1 + EBDX, using
the base project's stock tilesets. Code and specs live in `mapgen/`, output in `maps_out/`.

## 1. What's built (Act I, in story order)
| IDs | Maps | Story / mechanics |
|---|---|---|
| 109–110 | The Dovetail: deck and cabin (prologue) | The intro autorun runs `Prismfall.choose_difficulty`. Voss gives the badge case and the `PRO_FELLOWSHIP` choice, then a fade to the Ferrow's berth. The deck is pier planks and rails over the sea ([TODO art] ship) |
| 100–108 | Ferrow's Landing and interiors | Customs NULL scan (S102). Edda's GO-01. The Hales' stall, the counting rhyme, the Old Rod. Larch's letter scene, then the starter table (any Gen 1–9, plus Juno's and Kestrel's counter-picks). K1 autorun at the lab gate (`Prismfall.rival_battle`, S104). Rowan, Hesper |
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

**New game start:** `Plugins/Prismfall Maps/004_NewGameStart.rb` sets `PrismfallMaps::PRISMFALL_START = [109, 8, 6]`
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

**Keys the narrative spec must register / confirm** (used by events via `pf_choose` and `Prismfall.game_over`):
- `:PRO_FELLOWSHIP` → :accept / :decline / :silent (with `pf_standing_add(:MERIDIAN, 1)` and $1000, or `pf_bond_add(:VOSS, 1)`)
- `:CH2_TAMSIN` → :help_confess / :expose (MERIDIAN −1, ACCORD +1) / :keep_secret (MERIDIAN +1)
- `:CH3_JUNO_TALK` → :told (JUNO +1) / :deflect / :silent
- `:CH4_KESTREL_MOURNER` → :kind (KESTREL +1) / :blunt (KESTREL −1) / :silent
- `:CH4_TEO` → :report (MERIDIAN +1) / :keep_secret (HOLLOW +1) / :confront. Marisol has no Bond ID in Core yet, so her
  bond deltas aren't applied. Register `:MARISOL` if Narrative wants them.
- Game overs: GO-01 "Homeward" uses `:GO_LAST_FERRY`, GO-02 "Two in the Orchard" uses `:GO_BLEED_TIDE` (Core's registered
  IDs). GO-03 "Curtain Call" uses **`:GO_CURTAIN_CALL` (not registered yet; Core warns but still runs it)**. Rename both
  sides together if Narrative picks other IDs.

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
