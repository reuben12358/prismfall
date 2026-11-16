# MAPGEN — generated RPG Maker XP maps for Prismfall

The map generator turns readable YAML specs into real RMXP map files (`Data/MapNNN.rxdata`) for Essentials v21.1 + EBDX, using
the base project's stock tilesets. Code and specs live in `mapgen/`, output in `maps_out/`.

## 1. What's built (Act I slice, in progress)
| IDs | Maps | Notes |
|---|---|---|
| 100 | Ferrow's Landing (40×32) | Town: Lab, PC, Mart, Inn, Customs, Dockmaster, Lighthouse, pier and berth, linked doors, N edge to Route 1 |
| 101–108 | Ferrow's interiors | PC (nurse, healing balls, PC), Mart, Larch lab (starter table: any Gen 1–9 starter via `Prismfall::Rival.line` + `Prismfall.record_starter`), Inn (rest = heal), Lighthouse 1F/Lamp room (stairs), Dockmaster, Customs Hall (moored ship) |
| 120 | Briarwick (44×40) | Gym, PC, Mart, Guildhall, two houses, stream with a plank bridge, W edge to Route 3 (540), S warp to Gossamer Wood (524) |
| 121–125 | Briarwick interiors | Cutter's House gives HM01 once Badge 1 is held |
| 130–133 | Loomhouse Gym (Gym 1) | Foyer → Weaving Hall (heddle-lever plank puzzle, V305–V307) → Canopy Lofts (spool ziplines, S305–S307, rope ladders) → The Spindle (Tamsin; `Prismfall.award_badge(1)`, TM89) |
| 520 | Route 1 (26×48) | Tall grass, a south-only ledge, 2 trainers, Juno tutorial NPC, items, an Oran berry tree |
| 521, 523 | Route 2 (60×26) + Hale Farmhouse | Orchard hedgerows, 3 trainers, the NE quarantine cordon (Accord guard blocks the gap to 522), W warp to Gossamer Wood |
| 524, 526 | Gossamer Wood (48×48, :SILKWOOD) + Woodward's Hut | Forest maze, S↔Route 2 and N↔Briarwick warps, a silk wall forcing the west loop, a Cut tree, 4 trainers, Kestrel |
| 990 | Prismfall Test Arena (21×13) | One NPC per field in SPINE's roster (31), each offering a wild or trainer test battle with `setBattleRule("field", :ID)` and `canLose`; a healer; Exit → Ferrow's Landing |

Previews: `maps_out/previews/NNN_<name>.png`. Each is rendered from the written `.rxdata` file and shows the event pages active at game start.

## 2. Installing into your project (Windows, RPG Maker XP)
1. **Close RPG Maker XP.** It rewrites `MapInfos.rxdata` when it saves.
2. Copy `maps_out/Data/Map*.rxdata` and `maps_out/Data/mapinfos_prismfall.txt` into your project's `Data/`.
   Copy `maps_out/PBS/map_metadata_prismfall.txt` and `map_connections_prismfall.txt` into `PBS/`. v21.1 merges `<base>_<suffix>.txt` files.
3. Register the maps in `Data/MapInfos.rxdata` with **either** method:
   - **In-game (recommended, uses the game's own Marshal):** copy `maps_out/Plugins/Prismfall Map Installer/` into `Plugins/`.
     Start the game in Debug mode and run **Debug → Files → Install Prismfall maps**. The plugin backs up `MapInfos.rxdata` once,
     to `MapInfos.rxdata.prismfall-bak`. It adds each line of `mapinfos_prismfall.txt` with its name and parent, keeps every
     existing entry, and reports any ID collision (skipped) or missing map file.
   - **Standalone (needs Python 3 + numpy + PyYAML):** run `python3 -I mapgen/merge_mapinfos.py "C:\path\to\YourProject"`.
     The **merge tool** does steps 2 and 3 itself: it copies the maps and PBS files, then reads *your* MapInfos with a safe parser,
     adds our entries, warns on and skips collisions, and makes a backup. Add `--dry-run` to only report.
   - We never ship a prebuilt MapInfos. Both methods start from your own file.
   - If you skip this step, Essentials' compiler still imports the maps in Debug mode, but with names like `MAP100` and no tree.
4. Start the game in Debug mode so it **recompiles** (or use Debug → Compile data). Then open RMXP: the maps appear under their parents.
5. Field defaults: `maps_out/manifest.json` → `fields` lists `map_id → FIELD`. Those are the gym rooms and :SILKWOOD so far.
   The Field Effects owner adds them to `FieldEffects::MAP_FIELDS`. The gym battles also set the field explicitly.
6. Trainers used by map events are listed in `maps_out/trainers_needed.txt`, for example `:YOUNGSTER, "Pip"`.
   Each must exist in PBS. Missing ones crash at battle start; in Debug mode, compiling offers to create them.

**Game Switches / Variables used by map events** (name them in RMXP's database; we don't touch `System.rxdata`):
| ID | Kind | Use |
|---|---|---|
| 22 | Switch | stock Essentials `s:tsOff?("A")`, used by the animated door pattern (same as the base project) |
| 305 / 306 / 307 | Variable | Gym 1 Weaving Hall heddles A / B / C (0–2: which plank column is down) |
| 305 / 306 / 307 | Switch | Gym 1 Canopy Lofts cords α / β / γ |
The gym puzzle block is 300+5n … 300+5n+4. Gym 1 = 305–309, per GYM_PUZZLES.md and the SPINE_FEEDBACK request.
The base project's System.rxdata defines only 100 switches and 100 variables. The game works with higher IDs, but to see their names
in RMXP, raise the maximum in Database → System (or in the switch/variable picker).

## 3. Regenerating
```
cd fangame/mapgen
python3 -I build.py            # all specs  -> maps_out/ (runs gen_*.py spec generators first)
python3 -I build.py 100 520    # only some maps (links are still resolved against all specs)
python3 -I build.py --grid     # previews with a coordinate grid (yellow = every 5 tiles)
```
`build.py` checks itself as it goes. It reads every written map back, warns about unresolved door links, transfers to maps that
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
- Not built yet: 109/110 (Dovetail deck/cabin, Boat tileset), 522 Glassed Orchard, 525 Deepwood (the Cut tree leads to a
  `[TODO map]` sign), Route 3 onward (Briarwick's W edge connection to 540 is held back until 540 exists).
- Dialogue is placeholder `[TODO story]` text, except gym mechanics from GYM_PUZZLES.md.
- Trainers in `trainers_needed.txt` (route and gym trainers, Test Arena `YOUNGSTER Ben`, a base PBS trainer) must exist in PBS.
- RMXP can only test variable conditions with ">=", so each plank uses two pages (show at ≥k, hide at ≥k+1).
- Previews show the initial state. They don't show priority above the player or animated autotiles.
