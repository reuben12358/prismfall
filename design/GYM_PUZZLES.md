# GYM PUZZLES — all 18 Wardens (Revision 10 rewrite; Revision 14 order and difficulty curve in §0b)

Supersedes the previous GYM_PUZZLES.md. Research basis: `design/PUZZLE_STUDY.md` (decoded Reborn and Rejuvenation puzzles
and the 15 design principles). Dungeons: `design/DUNGEON_PUZZLES.md`.
Room IDs follow WORLD.md §2 and maps.json (gym in city c = rooms 100+20c+10 …). Every battle in a gym uses the gym's
field (map default in `FieldEffects::MAP_FIELDS`, plus `setBattleRule("field", …)` on each trainer).

**Bugs fixed from the previous version (found while re-checking it):**
- *Gym 1, 131 Weaving Hall.* Ledge N is full width and all three planks start in column x3, so the start state was
  already a solution: you could walk straight up the left side.
- *Gym 1, 131.* The levers stood on the plank landing tiles of ledge S (3/12/21, 18), so a plank landing on a lever was
  unreachable.

---
## 0b. The difficulty curve (SPINE Revisions 13 and 14) — supersedes every ★ rating below

The user: *"gym puzzles should range from simple to complicated (gym 1 should have a layout similar to Jasmine's gym from
HeartGold/SoulSilver, nothing too complicated, gym 2 onwards it gets more fun)"* and *"gym 1 should be normal type to ease the
player into the game"*. So Gyms 1 and 2 swapped towns (SPINE Rev 14), Gym 1 lost its puzzle, and every gym now has a
**rating (1–10)** and an **expected first-time solve time** (puzzle only, battles excluded). Reborn-level difficulty arrives in
the mid-to-late gyms, never before Gym 9.

**What a rating means, and the machine check.** `mapgen/puzzles/core.py` (`RATING_BUDGET`) caps each *required* room's
shortest solution (device uses: levers, ropes, rides) and its reachable state space. `build.py --strict` fails a room that is
harder than its rating, so an early gym cannot creep up.

| Rating | Feels like | Max moves | Max states | Rule budget |
|---|---|---|---|---|
| 1 | a walk-through (Jasmine) | 1 | 4 | at most one interaction, no way to fail |
| 2 | one obvious step | 3 | 16 | one rule, said aloud |
| 3 | first real puzzle | 4 | 64 | one coupled rule you can SEE; a 3-tier hint always works |
| 4 | a proper room | 8 | 256 | one rule + one twist |
| 5 | two systems | 12 | 1 024 | rule × second system |
| 6 | two systems, two rooms | 16 | 4 096 | cross-room cause and effect |
| 7 | Reborn mid-game | 20 | 16 384 | three systems, or one deep one |
| 8 | Reborn Lapis / Calcenon | 28 | 65 536 | composition, careful planning |
| 9 | Reborn late game | 36 | 262 144 | composition + one timing or information layer |
| 10 | the hardest in the game | 60 | 10 000 000 | everything; still provably fair |

Optional Mastery rooms may sit up to **two points above** their gym; they never block a badge.

| Gym | Warden · town | Type · field | Rating | Expected solve | Required puzzle (what you must do) | Moved out to stay in budget |
|---|---|---|---|---|---|---|
| 1 | Dorian · Saltmere (150, 154) | Normal · Grand Stage | **1** | 2 min | Walk up the aisle past three actors, pull one curtain rope, battle | The whole revolving stage → **D9 Playhouse Backstage** (optional, 4/10) |
| 2 | Tamsin · Briarwick (130, 131) | Bug · Silkwood (doubles) | **3** | 6–10 min | One heddle (teach), then three linked heddles: each lifts two loom beds | Spools + brass Meridian wire + Granny's Knot → **Upper Lofts** (optional, 4/10 and 3/10) |
| 3 | Marisol · Ebbmouth | Water · Water Surface | **4** | 10–15 min | Practice lock, then ONE basin: level wheel + drifting raft (≤ 8 actions) | Tide bell × lock gate combination → Overflow Culvert Mastery (6/10) |
| 4 | Rook · Lumen City | Electric · Neon Grid | **5** | 15 min | Rotate conduits, tees and the alarm lamp | Drone-as-wire + latches → Live Wire Hall stays, but the latch board is the Edit Bay Mastery |
| 5 | Sahar · Duneholt | Ground · Desert | **5** | 15–20 min | Sun-mirrors decide crust or sink; one drop is the way across | Two-floor loop of drops → Mural Gallery Mastery |
| 6 | Corvin · Mirefen | Poison · Corrosive Mire | **6** | 20 min | Measures with unmarked flasks (3 + 5 make 4), carried across the filter steps | — |
| 7 | Brann · Cindervault | Fire · Volcanic | **6** | 20 min | Pour, aim, quench; what you don't quench drains below | — |
| 8 | Kaito · Ironreach | Fighting · Colosseum | **6** | 20 min | Pursuers vs Strength boulders, checkpoints | — |
| 9 | Juno · Verdance | Grass · Flower Garden | **7** | 25 min | Watering rings; leftover overgrowth becomes the arena's field stage | — |
| 10 | Anja · Rimeholt | Ice · Frozen Lake | **7** | 25 min | Slides, cracks, the under-ice, plugs | — |
| 11 | Odessa · Skyreach | Flying · Stormfront | **8** | 30 min | Coupled vanes steer fans that push you and the mail | — |
| 12 | Ilsa · Lucent | Psychic · Mindscape | **8** | 30 min | Mirrored walker, swap pads | — |
| 13 | Bastian · Cragholm | Rock · Crystal Cavern | **8** | 30 min | Beams, prisms, colour gates, boulders as blocks | — |
| 14 | Ysolde · Gravenmoor | Ghost · Hollow Cathedral | **9** | 35 min | Twin naves, persistent pews, the echo | — |
| 15 | Magnus · Cogsworth | Steel · Factory | **9** | 35 min | Belts, presses, crates on one clock | — |
| 16 | Nyx · Underveil | Dark · New Moon | **9** | 40 min | Guards, lanterns, secrets that re-route the vault | — |
| 17 | Celestine · Gloaming | Fairy · Fairy Tale | **10** | 40 min | Truth-bound storybook logic | — |
| 18 | Sigrun · Wyrmrest | Dragon · Dragon's Den | **10** | 45 min | Scales, statues and the magma tide | — |

**Built and proven** (`python3 -I mapgen/puzzle_check.py`, and again on the built maps by `build.py`; re-proved after the
2026-11-19 art pass, which moved coordinates but no puzzle logic):
Gym 1 auditorium 1 move / 2 states (1/10) · Gym 2 foyer 1 / 2 (1/10) · Gym 2 Weaving Hall 3 / 27 (3/10) · Upper Lofts
7 / 93 (4/10, unsolvable without the brass wire) · Granny's Knot 3 / 32 (3/10, unique) · Playhouse Backstage stage + loft
5 / 39 (4/10, unsolvable without each scene and without the loft) · Trap Room 3 / 6 (3/10).
**Gym 3 needs a trim before it is rebuilt** (owner of `gen_gym3.py`): its spec'd basins take 16 actions, which is a 6/10 room.
The required route must fit 4/10 (≤ 8 actions); the bell × gate combination becomes the Culvert Mastery.

**ID blocks after the swap.** Switch/variable blocks belong to the *building*, not the gym number, so nothing was renumbered:
305–309 = the Loomhouse (now Gym 2), 310–314 = the Pell Playhouse (now Gym 1). Names in `mapgen/flags.yaml` are
`LOOM_*` and `STAGE_*`. Gym events never hard-code a gym number either: they call
`Prismfall.gym_battle(pfm_gym(:LEADER_DORIAN), double: false)` and `award_badge(pfm_gym(...))`
(`mapgen/ruby/008_GymOrder.rb`), which read Core's `Prismfall::GYMS` table, so the maps are right in either order.

---
## 0. Conventions (read once)

**Beats.** Every gym grows one core rule through **Teach → Twist → Combine → Mastery**. Mastery is an optional side room
with a real reward, usually the gym field's **seed** (Reborn-style) plus a held item.

**Coordinates** are (x, y), origin top-left. ASCII maps are true scale (1 char = 1 tile) unless marked *schematic*. In
schematic maps, the coordinates in the event tables are authoritative.

**Shared ASCII legend** (each gym adds its own symbols):

| Glyph | Meaning |
|---|---|
| `#` | wall / impassable art |
| `.` | floor |
| `v` | void / drop (impassable, nothing below) |
| `~` | water |
| `@` | entrance (arrival tile) |
| `E` | exit warp / door |
| `A` | the room's **apprentice** (reset and hint NPC) |
| `T` | gym trainer |
| `i` | item ball |
| `*` | Mastery reward chest |
| `o` | silk / curtain wall (Gym 1) |
| `x` | painted mark (always floor) |
| digits | numbered devices (levers, ropes, nodes), defined per room |

**Page notation in event tables:** `P0 [—] tile 3807 · action → commands`, `P1 [V305≥1] blank`. Rules:
- `[—]` means no condition. `[V≥k]`, `[S on]` and `[self A]` are RMXP page conditions. The last page whose conditions hold
  wins.
- An exact value k needs two pages: `[V≥k]` shows it, `[V≥k+1]` hides it (RMXP only tests ">="; MAPGEN §6).
- `blank` = no graphic, so the tile underneath decides passability.
- Triggers: `action` (default), `touch` (player touch), `auto` (autorun), `par` (parallel).

**Event naming.** Puzzle events carry stable names, for example `Plank A 12,4` or `Rope 2R`. The runtime helpers (§3)
find events by name, never by ID.

**Apprentice (every puzzle room).** One NPC, standing on a tile reachable from every state of the room. Menu:
1. **Reset the room**: restore the room's start state, fade, put the player on the room's start tile.
2. **Hint**: tier 1 (a nudge) → tier 2 (the key fact) → tier 3 (a full walkthrough). Each later tier unlocks after one
   more reset or failed check. Counter: `pfm_add(:g<N>_<room>_hint)`.
3. **Skip**: only with the `puzzleskip` password. It applies the room's solved state.
4. *Leave it.*
Apprentices are characters (a Warden's apprentice, a stagehand, a lock-keeper's kid). Their hint lines are written in
voice; the tier 3 text is the "Solution" paragraph of each room.

**Natural resets.** Leaving a room keeps switch and variable state, unless the room says otherwise. Moved events (pushed
crates, the drone, a follower) return to their start squares unless their positions are saved with `pfp_save` (§3).

**Trainers.** Levels sit at cap −4 … cap −1. Sight 3 unless stated. Stock classes, unless marked *(new)*. Once beaten, a
trainer stays beaten (self switch A, the stock Essentials pattern). Trainers are always placed so they never block a
device or a required tile.

**Difficulty scale** (shown in each header): ★ = Gym 1, ★★★★★★★★★★ = Gym 18. Casual difficulty halves every step
budget and timer. The puzzles themselves never change by difficulty.

---
## 1. State registry (Switches and Variables)

SPINE Rev 3 ruling: IDs **301–400** are reserved for puzzles, and gym n uses **300+5n … 300+5n+4** (Gym 1 = 305–309 …
Gym 18 = 390–394). Switch S305 and variable V305 are different objects. Five of each per gym is not enough for
Reborn-level rooms, so this spec **extends the block**. The builder adds the extension to `mapgen/flags.yaml`; the story
lead adds a pointer row to FLAGS.md. Essentials ignores pages on switches it has no name for (MAPGEN §2), so every ID
below needs a name in `system_prismfall.txt`, and the installer must raise the maximum to 600.

| IDs (S and V) | Owner |
|---|---|
| 301 | `PUZZLE_SKIP`: S = Core-written mirror of the `puzzleskip` password. V301 = scratch X |
| 302 | `PUZZLE_ASSIST`: S = "hints on" option. V302 = scratch Y |
| 303–304 | spare (global) |
| **305–394** | gym n **primary** block = 300+5n … +4 (unchanged) |
| 395–400 | spare |
| 401–404 | spare (global) |
| **405–494** | gym n **secondary** block = 400+5n … +4 (new) |
| 495–500 | spare |
| **501–600** | dungeons, 5 per dungeon (DUNGEON_PUZZLES.md §0) |

Complex boards (rotations, push positions, follower placement) keep their state in **`pfm` flags** through the `pfp_*`
helpers (§3). Flags are saved but cost no IDs. Switches and variables are used only where an RMXP page condition needs
them, or where a state crosses maps.

---
## 2. The 18 at a glance

| # | Warden · field | Core rule | Teach → Twist → Combine → Mastery | ★ (see §0b for the 1–10 ratings) |
|---|---|---|---|---|
| 1 | Dorian · Grand Stage | **A walk-through** (Rev 14): the house loves a show | aisle, three actors, raise the curtain (D9 Backstage keeps the old revolving-stage puzzle) | 1/10 |
| 2 | Tamsin · Silkwood | **Follow the thread**: each heddle moves what its silk ties to | one heddle → three linked heddles (Upper Lofts: spools + brass wire → Granny's Knot, optional) | 3/10 |
| 3 | Marisol · Water Surface | **Water lifts what floats, the current carries what's loose** | practice lock → three water levels × a drifting raft × the tide bell × a lock gate → snag culvert | 3 |
| 4 | Rook · Neon Grid | **Route the power, never the alarm** | rotate conduits → tees and an alarm lamp → Rotom drone as a portable wire + latching relays → the empty Plate socket | 4 |
| 5 | Sahar · Desert | **Sun hardens, shade sinks**: falling is a way across | one drop → sun-mirrors decide which lanes are crust and which sink → a two-floor loop where drops are transport → mural rubbing | 5 |
| 6 | Corvin · Corrosive Mire | **Dose makes the cure**: exact measures with unmarked flasks | one flask → 3+5 make 4 → doses carried across a filter-step budget → the Quiet Ward (4+9) | 5 |
| 7 | Brann · Volcanic | **Pour, then quench**: empty → molten → iron | one mould → aimed spouts and one quench → what you don't quench drains into the moulds below → the cracked-mould vault | 6 |
| 8 | Kaito · Colosseum | **Every step you take, they take**: pursuers vs Strength boulders | one sparring Machop → two pursuers and rope lines → boulders, plates and pursuers → the Marrowgate door | 6 |
| 9 | Juno · Flower Garden | **Water spreads**: each plot grows itself and its neighbours, and the leftover overgrowth becomes the arena's field stage | one plot → a ring of six → two rings sharing a junction → the Bride Bower | 7 |
| 10 | Anja · Frozen Lake | **Ice remembers weight**: slides, cracks and the under-ice | slide → cracked ice drops you to the under-ice → ice blocks plug holes and refreeze → the Sounding | 7 |
| 11 | Odessa · Stormfront | **The wind doesn't care**: vanes steer fans that push you and the mail | one lane → coupled vanes → letter sacks ride and stack → Dead-Letter Archive | 8 |
| 12 | Ilsa · Mindscape | **Your reflection keeps you honest**: a mirrored self walks your steps | mirrored walk → swap pads → thoughts only the reflection may stand on → the Quiet Room | 8 |
| 13 | Bastian · Crystal Cavern | **Light remembers its colour**: beams, prisms and colour gates | one mirror → filters and splitters → boulders as beam blocks + the prism-glow cycle → Bastian's long story | 9 |
| 14 | Ysolde · Hollow Cathedral | **The dead walk where you walked**: twin naves and Morwen's echo | living ⇄ dead bell → pews persist across worlds → the echo replays your path → Morwen's letter | 9 |
| 15 | Magnus · Factory | **Tolerances**: belts, presses and crates on one clock | belts → reversing lever groups → crane-placed crates jam presses → the Tolerance Lab | 10 |
| 16 | Nyx · New Moon | **Information is the key**: guards, lanterns and secrets that change the doors | sight lines → lanterns turn guards → each stolen secret re-routes the vault → the Ledger | 10 |
| 17 | Celestine · Fairy Tale | **She cannot lie, but she can phrase**: truth-bound storybook rules | the Red Path → the Midnight clock × dancers × truthful guests → the Eight Princesses' statements → the Ninth Door | 10 |
| 18 | Sigrun · Dragon's Den | **Nothing passes unweighed**: scales, statues and the magma tide | one scale → the coupled statue ring → hoard weights on magma-floated pans → say it aloud | 10 |

---
## 3. Runtime helpers the specs call (contract; BUILT as the plugin `plugins/Prismfall Puzzles/`, rooms in the generated `Plugins/Prismfall Maps/007_PuzzleRooms.rb`)

The builder writes this file next to `006_MapStory.rb` (§5 lists everything the toolchain needs). All helpers act on the
current map and find events by name. Each must be Ruby 3.1-safe and use only v21.1 APIs: `pbSet`, `pbGet`,
`$game_self_switches`, `pbMoveRoute`, `Followers.add/remove`, `pbPushThisEvent`, `EventHandlers`.

| Helper | Does |
|---|---|
| `pfp_ev(name)` | the `Game_Event` with that name on this map, or nil |
| `pfp_cycle(var, n, step = 1)` | `V = (V + step) % n`, then `$game_map.need_refresh = true` |
| `pfp_flip(sw)` / `pfp_flip_self(names, ch = "A")` | toggle a switch / the self switch of each named event |
| `pfp_save(key, names)` / `pfp_load(key)` | store / restore x, y and direction of the named events in `pfm` flags (Coral pattern) |
| `pfp_restore!` | called by each puzzle map's one-shot **Restorer** (a `par` event that runs once per map load, then sets its own self switch). Re-applies saved positions, directions and graphics |
| `pfp_state(name, k)` / `pfp_state_of(name)` | **one-hot multi-state events**: state 0 = no self switch, 1–4 = only self A/B/C/D on. Pages: P0 [—] state 0 · P1 [self A] · P2 [self B] · P3 [self C] · P4 [self D]. Saved, survives map loads, costs no IDs. Used for rotations, plot growth, statue facings |
| `pfp_rotate(name, n = 4)` | `pfp_state(name, (pfp_state_of(name) + 1) % n)`: a quarter-turn for one-hot rotation events |
| `pfp_swap_map(map_id, fix = {})` | fade-transfer to the same x,y on a twin map. `fix` maps landing squares that are solid on the twin to safe squares |
| `pfp_ride(dest_x, dest_y)` | jump the player along a line (Through ON, jump, Through OFF) |
| `pfp_push_line(dir, kind)` | forced movement: move the player while the tile ahead holds an event of `kind` (belt, wind, current), or while the tile being left is ice |
| `pfp_beam(source)` | trace a light beam from a named source through `Mirror*`, `Prism*`, `Filter*`, `Block*` events, light the `Beam x,y` events on its path (self A), and return the set of lit receptors |
| `pfp_power(board)` | trace power through `Node*` events by direction and port masks, light `Strip` events, and return the lit lamps |
| `pfp_metronome(var, frames, beats)` | parallel clock: `V = (V + 1) % beats` every `frames` frames, with refresh |
| `pfp_step_hook(map, &blk)` | register an `:on_player_step_taken` handler that is active only on that map (step budgets, mirrored walkers, pursuers) |
| `pfp_pursue(name, mode)` | move a pursuer one square toward the player (`:chase`) or mirror the player's last step (`:mirror`, `:echo`) |
| `pfp_check(id)` | run a registered checker. Returns `[:ok]` or `[:fail, :reason]`; events branch on it and print the per-reason line |
| `pfp_hint(id)` / `pfp_skip?` | apprentice support: hint tier, and the skip test (`$game_switches[301]`) |

---
## Gym 1 — Saltmere, the Pell Playhouse · Dorian Pell (Normal, `:GRAND_STAGE`, cap 15, single battle) · 1/10, 2 min

**SPINE Rev 14.** The first gym is a handsome walk-through in the spirit of Jasmine's HGSS gym. The only thing to learn is
the first field: the house loves a show.
**Layout and logic:** `mapgen/puzzles/playhouse.py` (`LOBBY`, `THEATRE`; authoritative coordinates), painted by
`mapgen/gen_playhouse.py` on tileset 54 "PF Rejuv Halls" (Rejuvenation's Goldenleaf Theatre tiles).

### 150 Lobby (25×15) — art pass 2026-11-19
A grand foyer on Rejuvenation's theatre tiles (Goldenleaf Theatre and the Nightbox Theater, tileset 54): mauve panelled
walls with purple pilasters; four framed bills (*Rain Fall*, *The Lady in Red*, a green one, and the oldest, pasted over
years ago with "...ED K..." showing through: the script's poster, not a *Gilded King* reveal); the comedy-and-tragedy crest
and a gilded beam over the auditorium doors, small chandeliers either side; a great chandelier over the red runner; velvet
ropes, gilded urns, flowers, velvet loveseats and a sofa; the box office (talk across the counter). People: the usher, the
**gym guide** (teaches the field: sound and dance moves get a cheer; Fighting is good, Ghosts don't care), a regular, the
box-office clerk and five theatregoers. Doors (12,5) → auditorium; exit mat (12,14) → Saltmere (`SM_GYM`, map 147).
`SnapEdges` is on for every gym room, so the camera never shows the black beyond a room's walls.

### 154 Auditorium — the gym (25×30) — art pass 2026-11-19
```
y2     the gilded proscenium beam, the comedy-and-tragedy crest
y3-5   the painted drop (Saltmere harbour at dusk) under the valance swag; the house curtain (V311) covers y3-10, x6-18
y2-10  box seats in both side walls (x1-3, x21-23), each with a couple in it; gilded pilasters x4 and x20; the curtain's
       gathered legs x5 and x19; the stage-left wing door (x1-3, y9-10; warp at (2,10)) and the dressing-room door (x21-23)
y6-10  the stage: polished boards, tape marks; Dorian (12,7) behind the curtain
y11    the apron, lit by the footlights; curtain rope (21,11), stagehand (22,11)
y12    the stage front: a footlight per tile; steps (12,12)
y13-15 the orchestra pit, a storey down: grand piano, five musicians at their stands, the conductor (10,15); crossed by
       the gangway x11-13
y16    the brass pit rail
y17-28 the stalls: two blocks of 4×9 velvet seats either side of the red runner (x11-13), about 40 seated audience
       members (the aisle seats talk), a great chandelier over the aisle, candelabra at the side aisles
y29    the lobby doors (12,29)
```
- **Trainers:** Juggler Florian (11,25) and Beauty Rosalind (13,20) stand in the aisle (sight 2), so walking up it means
  two battles; Juggler Ambrose (1,18) in the side aisle is optional. All use the Grand Stage field. Juno appears in the
  front row (10,18) once one actor is beaten.
- **Field Notes:** on the first step up the aisle, the Grand Stage pop-up from the script ("the audience reacts…", with
  Larch's margin note), once per save (`pfm(:fn_grand_stage)`).
- **The one interaction:** the curtain is in. The stagehand: "He won't come out till the curtain's up. That rope, there."
  Pull it: V311 = 1, a small screen shake, the curtain events vanish, the painted drop and Dorian appear.
- **Dorian:** `Prismfall.gym_battle(pfm_gym(:LEADER_DORIAN), double: false)`. Win → badge, TM42 Facade, Eevee
  "Understudy" (S110), the Pageant invitation.
- **Apprentice:** none needed (nothing can go wrong). The room is still registered (`:ph_theatre`) so Debug reset/solve work.
- **Proof:** 1 move, 2 states (rating 1), on the design grid and on the built map.
- **After Tamsin's badge,** Dorian points at the stage-left wing: the **Playhouse Backstage** (DUNGEON_PUZZLES D9),
  which is the Revision 10 Gym 2 puzzle, kept whole.

---
## Gym 2 — Briarwick, the Loomhouse · Tamsin Loom (Bug, `:SILKWOOD`, cap 19, double battle) · 3/10, 6–10 min

**SPINE Rev 14:** this was Gym 1; it is now the first real puzzle. The gym itself is two rooms (130 Foyer, 131 Weaving Hall);
Tamsin waits on the Weaving Hall's top ledge. The spools, the brass Meridian wire and Granny's Knot became the optional
**Upper Lofts** (132, 134), up the stairs behind her after the badge. Coordinates: `mapgen/puzzles/loomhouse.py`
(authoritative; the tables below give the design, the module gives the built positions). Painted by `mapgen/gen_loomhouse.py`
on tileset 54 (Rejuvenation timber-hall tiles + Prismfall looms, dye vats, silk bales, webs).
Rejected Rev 13 interim (one-room hall with the Warden at the top): superseded by Rev 14 the same day.

**Original design (Revision 10), adjusted:**

**Core rule: follow the thread.** Every lever (a *heddle*) is tied by visible silk to what it moves. One pull can lift two
things. Every pattern repeats after three pulls.
**Warden link:** "A thread holds because it's twisted with others." Tamsin's coupled levers *are* that line. Her apology
cards are the hint system. **The aha** belongs to the story: one cord in the Lofts is not silk but **brass Meridian wire**.
It is not on the pattern card, and it moves something nobody expects: Tamsin's secret contract, felt as a puzzle mechanic.
**Field link:** Silkwood (Electroweb runs the threads). Trainers carry Electroweb and Struggle Bug.
**Kingdom:** Elowen weavers' guild craft. Every device is a loom part.

### State
| ID | Name | Values | Room |
|---|---|---|---|
| V305 / V306 / V307 | `LOOM_A/B/C` | 0–2 (plank column of loom beds A, B, C) | 131 |
| V308 | `LOOM_FOYER` | 0–1 | 130 |
| V309 | `LOOM_BRIDGE` | 0 none · 1 P5→P6 · 2 P4→P6 | 132 |
| S305 | `LOOM_ALPHA` | spool s1 destination | 132 |
| S306 | `LOOM_BRASS` | spools s3/s4 destination (the brass wire also cycles V309) | 132 |
| S307 | `LOOM_GAMMA` | spools s2/s5 destination | 132 |
| S308 | `LOOM_KNOT` | Granny's Knot solved | 134 |
| S309 | spare | | |

Tiles: `PLANK` = 3807 (passable cross-board, used today). Hanging threads use the `custom` strand tiles (`CU['strand_*']`).

### 130 Foyer — TEACH "the first thread" (20×25 as built, art pass 2026-11-19)
**As built:** a straight hall, wall to wall: a four-row timber wall with two tall arched windows (their light falls across
the floor and on into the loom bed), yarn shelves, silk drying on frames, dye vats, looms in pairs either side of a red
runner, one loom bed across the room (its front beam, the floor a storey below, the warp over it). The plank starts at
x5–6 (left); the heddle frame beside the aisle (11,12) is tied by a visible silk thread to it; **one pull** slides it into
the aisle (V308 0/1). Bug Catcher Nell and Lass Orla flank the aisle; Tamsin's apology spiral; Pim (apprentice,
`:lh_foyer`); the first loom (Ledger key). Stairs (15,4) → 131. Proof: 1 move, 2 states.

*Revision 10 version (three balconies, period-3 heddle), kept for reference:*
```
     012345678901234
y0   vvvvvvvvvvvvvvv
y1   vvvvvvvvvvvvEvv    E (12,1) stair → 131 (12,19)
y2   vvv...v...v...v    balconies: A x3-5 · B x7-9 · C x11-13
y3   vvv.i.v.c.v...v    i (4,3) Potion · c (8,3) apology card
y4   vvvvvvvvvvvvvvv    gap, rows 4-5. Plank columns x4 / x8 / x12
y5   vvvvvvvvvvvvvvv
y6   v.............v
y7   v..1..........v    1 = Training heddle (3,7)
y8   v.........g...v    g gym guide (10,8)
y9   v...s.......L.v    s apology card (4,9) · L "First loom" (12,9)
y10  vvv.....A...vvv    A apprentice "Weaver Pim" (8,10)
y11  vvvvvv...vvvvvv
y12  vvvvvvv@vvvvvvv    @ exit mat (7,12), link BW_GYM
```
| Event | Pages |
|---|---|
| `Plank F 4,y` (y = 4, 5) | P0 [—] tile PLANK · P1 [V308≥1] blank |
| `Plank F 8,y` | P0 [—] blank · P1 [V308≥1] tile PLANK · P2 [V308≥2] blank |
| `Plank F 12,y` | P0 [—] blank · P1 [V308≥2] tile PLANK |
| `Training heddle` (3,7) | P0 [—] lever graphic · action → `pfp_cycle(308, 3)`, SE "Door exit", text "You pull the heddle. The silk thread running up from it twitches, and out over the gap a plank slides along." |
| `Tamsin` (7,8) | the existing apology spiral, then she walks off east and erases (self A) |
| `First loom` (12,9) | the existing Ledger-key branch. The `else` text adds the pattern: "The warp stops mid-row: *up, down, up, down, up* — and then nothing, as if she meant to come back to it." (This is the Mastery target, 134.) |
| Apology card c (8,3) | "Three pulls and it's back where it started. Sorry! I didn't design it. — T.L." |

**Solution:** pull twice: the plank goes x4 → x8 → x12. Walk the x12 plank to balcony C and climb the stairs. The first
pull is rewarded either way (balcony B holds the hint card, A the Potion).
**Teaches:** that a lever moves something far away, that a visible thread shows the link, and that the cycle has period 3.
There is no failure state.

### 131 Weaving Hall — TWIST "two threads per heddle" (25×24 as built) — the gym's puzzle
**As built (art pass 2026-11-19):** the grid below shifted down four rows (three loom beds at rows 7–10, 13–15, 18–21).
The north wall is four rows of timber with four tall arched windows; their light falls across the top walkway and into
loom bed A. Each loom bed shows its depth: the walkway's front beam with the warp tied over it, the hall's floor a storey
below in shadow (bolts of silk, yarn baskets, support posts at both ends), the warp stretched across, the back beam. The
two heddles that lift a bed are tied round its beam in their colours at the left and right ends. Heddles are frames
(colour + header), not posts. Tamsin stands on the top ledge at (11,5); the stairs behind her (12,3) go to the Upper
Lofts once you hold her badge. Gentleman Bram is on the top ledge; Nell and Orla are in the Foyer. Battle:
`Prismfall.gym_battle(pfm_gym(:LEADER_TAMSIN), double: true)`. Proof on the built map: 3 moves (Red, Gold, Green once
each), 27 states, no soft-lock.
```
     0123456789012345678901234
y0   ############E############    E (12,0) → 132 (2,22)
y1   #.T.....................#    T Gentleman Bram (2,1)
y2   #.......................#    ledge N (full)
y3   #vvvvvvvvvvvvvvvvvvvvvvv#    gap A rows 3-6: planks x3 / x12 / x21
y4   #vvvvvvvvvvvvvvvvvvvvvvv#
y5   #vvvvvvvvvvvvvvvvvvvvvvv#
y6   #vvvvvvvvvvvvvvvvvvvvvvv#
y7   #....oooooo...oooooo..T.#    ledge 2: segments x1-4 | x11-13 | x20-23 · T Lass Orla (22,7)
y8   #.n..oooooo...oooooo....#    n torn-net sign (2,8)
y9   #vvvvvvvvvvvvvvvvvvvvvvv#    gap B rows 9-11: planks x12 / x21 ONLY (x3 is torn)
y10  #vvvvvvvvvvvvvvvvvvvvvvv#
y11  #vvvvvvvvvvvvvvvvvvvvvvv#
y12  #....oooooo...oooooo....#    ledge 1: same three segments
y13  #....ooooooT..oooooo....#    T Bug Catcher Nell (11,13), facing east (x12 landings stay clear)
y14  #vvvvvvvvvvvvvvvvvvvvvvv#    gap C rows 14-17: planks x3 / x12 / x21
y15  #vvvvvvvvvvvvvvvvvvvvvvv#
y16  #vvvvvvvvvvvvvvvvvvvvvvv#
y17  #vvvvvvvvvvvvvvvvvvvvvvv#
y18  #.......................#    ledge S (plank landings x3 / x12 / x21 stay clear)
y19  #....R...G..@..A...N....#    heddles R (5,19) G (9,19) N=Green (19,19) · A apprentice (15,19)
y20  ############.############    entrance (12,20) from 130
```
- **Heddles** (mod 3): **Red lifts A and B · Gold lifts B and C · Green lifts C and A.** Each is a lever event,
  action → `pfp_cycle(305,3)` + `pfp_cycle(306,3)` (Red), and so on. Text: "The red heddle rises. Two threads lift with it."
  A strand of the heddle's colour runs up the east and west walls to the two gaps it lifts (decor, layer 2).
- **Planks**: for gap A at y = 3–6 and gap C at y = 14–17, the columns x3 / x12 / x21 use the same 2–3 page pattern as 130
  (column k shown at V == k). Gap B (y = 9–11) has columns x12 and x21 only. Column x3 of gap B is never drawn.
  Sign n: "The x3 warp snapped. Sorry! Use the other two. — T.L."
- **Geometry rule:** the silk walls split ledges 1 and 2 into three segments, one per column. So you can only climb when
  **all three planks share a column**. Column x3 is out (torn), so the targets are **(1,1,1) or (2,2,2)**.
- **Solution (verified, BFS):** pull **Red, Gold, Green once each** → (2,2,2). Climb the x21 column (Orla battles you on
  ledge 2). The longer alternative is each heddle twice → (1,1,1), the middle column.
- **The twist:** a player who fixes one row at a time breaks the row they just fixed. Pulling all three once lifts every
  thread exactly twice. That is the pattern card's own wording ("Red lifts the warp and the weft…").
- **Hints (Pim):** 1 "Every heddle lifts two rows. Count lifts, not pulls." 2 "Three heddles, three rows: what if
  each row got lifted the same number of times?" 3 the solution.
- **Reset:** Pim → V305–307 = 0. Pulls are also self-undoing (three pulls = no change).

### 132 Canopy Lofts — UPPER LOFTS, optional after the badge (4/10) "spools, cords and the brass wire" (25×26)
**As built:** P6's exit leads to Granny's Knot (134); there is no trunk door. Proof: **7** actions (the spec said 8; the
solver found the true minimum), unsolvable without the brass wire.
Platforms (4×3 decks, centre `(cx,cy)`): **P1 (2,22)**, **P2 (12,20)**, **P3 (4,12)**, **P4 (19,14)**, **P5 (12,6)**,
**P6 (20,3)**, with P6's deck extended to rows 2–5. Everything else is void with silk lines drawn between spool pairs
(the existing zip-tile loop).
```
     0123456789012345678901234     (schematic of decks; void elsewhere)
y2                       E...      P6 deck x19-22 y2-5 · E warp (22,2) → 133
y3                       ....
y4               D       ....      D (12,4) trunk door → 134 Granny's Knot (opens S/side path)
y5              ...i====....       P5 x11-14 y5-7 · bridge V309=1: x15-18 row 5
y6              ...s    |          s spool s5 (14,6) · | bridge V309=2: x20 rows 6-12
y7              L...    |
y11   b...              |          P3 x3-6 y11-13 · b BRASS cord (3,11)
y12   ...s              |          s spool s3 (6,12)
y13   L...            g...         P4 x18-21 y13-15 · g cord GAMMA (18,13)
y14                   ...s         spool s4 (21,14)
y15                   L.T.         T Ranger Ash (20,15)
y19             ....               P2 x11-14 y19-21
y20             ...s               spool s2 (14,20)
y21  a...       L.T.               T Bug Catcher Hollis (13,21) · a cord ALPHA (1,21)
y22  @..s                          P1 x1-4 y21-23 · @ (2,22) from 131 · spool s1 (4,22)
y23  ....                          L = rope ladder → P1 (on P2 (11,21), P3 (3,13), P4 (18,15), P5 (11,7))
```
**Spools** (touch, at the deck's east edge). Each throws you along its silk line (`pfp_ride`) to the destination deck's
centre:

| Spool | Switch | ON → | OFF → |
|---|---|---|---|
| s1 (4,22) on P1 | S305 α | P3 | P2 |
| s2 (14,20) on P2 | S307 γ | P5 | P4 |
| s3 (6,12) on P3 | S306 brass | P4 | P1 |
| s4 (21,14) on P4 | S306 brass | P2 | P3 |
| s5 (14,6) on P5 | S307 γ | P3 | P2 |

**Cords** (action, self-describing): α on P1 and γ on P4 toggle their switch ("You pull the α cord taut / let it go
slack"). The **brass cord** on P3: `pfp_flip(306)` **and** `pfp_cycle(309, 3)`. Text, first time only: "This one isn't
silk. It's brass wire, stamped with a little gold sunburst. Somewhere ahead, something heavy slides." The bridge planks
visibly swing (V309 pages, same pattern as the 130 planks).
**Bridge planks:** `Bridge 5 x,5` for x = 15–18, shown at V309 == 1. `Bridge 4 20,y` for y = 6–12, shown at V309 == 2.
**Solution (verified, BFS; shortest = 8 actions; impossible without the brass wire):**
pull α → ride s1 to P3 → pull brass (β on, bridge to P5) → ride s3 to P4 → pull γ → ride s4 (β on) to P2 → ride s2
(γ on) to P5 → walk the bridge to P6.
Other solutions exist (for example brass twice for the P4 bridge). All of them need the brass wire.
**Soft-lock proof:** every deck except P1 and P6 has a ladder to P1. Cords are reversible. No state strands you.
**Hints (apprentice "Mossy", on P1):** 1 "The pattern card lists three cords. Count the cords up here." 2 "The brass one
isn't Gran's. Pull it and watch the far side of the canopy." 3 the solution.
**Reset:** Mossy → S305–307 OFF, V309 = 0, back to P1.

### 133 The Spindle — retired (Rev 14): Tamsin battles on 131's top ledge. Map 133 is no longer built.
Tamsin, double battle, `:SILKWOOD`. Badge 2 (the Weft Badge), TM89 U-turn, then the confession scene (`:ch2_tamsin`). New
line if S308 is on: "You finished Gran's row. ...She'd have shouted. Happily. Sorry — I'm crying, that's the Silkwood,
it's very dusty."

### 134 Granny's Knot — UPPER LOFTS MASTERY (optional, 3/10; reached from P6)
```
     0123456789012
y0   #############
y1   #...S.......#     S sampler sign (4,1): "▲▽▲▽▲" (the foyer loom's unfinished row)
y2   #...........#
y3   #...12345...#     warp threads T1-T5 (4..8,3): down/up graphics (self A = up)
y4   #...........#
y5   #...........#
y6   #...abcde...#     treadles P1-P5 (4..8,6)
y7   #.*.......r.#     * chest (2,7) · r "Re-thread" lever (10,7)
y8   ######@######     @ (6,8) ← door D
```
- **Treadles flip threads:** P1 {T1,T2} · P2 {T1,T3} · P3 {T1,T4} · P4 {T1,T5} · P5 {T1,T2,T3}. Every treadle passes
  through T1, "the first warp thread", which is where the Ledger key was tied (foreshadowing).
- Each treadle: `pfp_flip_self(%w[T1 T2])` etc., then `pfp_check(:g1_knot)`. On `:ok` → S308 on, the chest unlocks.
- **Target ▲▽▲▽▲ (T1, T3, T5 up). Unique solution: P1 + P4 + P5**, in any order (each press is its own undo).
  Verified over Z₂: the 5 treadles have full rank, so every pattern has exactly one answer.
- **Reward:** Telluric Seed ×2 (on Silkwood: +1 Def and Ingrain) + Silk Scarf, plus a note in Mother Loom's hand:
  "Twist it or lose it."
- **Reset:** the "Re-thread" lever lowers every thread.

**Trainers (Rev 14):** Foyer: Nell, Orla. Weaving Hall: Bram. Upper Lofts: Hollis, Ash. *Original list:* Bug Catcher Nell (11–12), Lass Orla (12–13), Gentleman "Weaver Bram" (13), Bug Catcher Hollis
(12–13), Pokémon Ranger ♂ Ash (13–14). Nell and Bram are optional.

---

---
## Gym 3 — Ebbmouth, Tidelock Gym · Marisol Reyes (Water, `:WATER_SURFACE`, cap 23) · ★★★

**Core rule: water lifts what floats, and the current carries what's loose.** Three water levels (twin maps 171/172/173 at
identical x,y). One log raft whose position persists across the levels. A lock gate. The **tide bell** flips the current.
At **Low** the channel beds are walkable trenches; at **Mid** the raft is a bridge; at **High** the raft drifts to wherever
the current and the gate let it stop.
**Warden link:** "The Ebb runs both ways. Lately it can't decide." The bell flips the river, as Ebbmouth's Imprint does
nightly. Marisol is a union dock boss, so the apprentice is a lock-keeper's kid and the levers are union-stamped.
**Field link:** Water Surface. **Kingdom:** Isenmar's working port, where locks are labour.

### State
| ID | Name | Values |
|---|---|---|
| V315 | `G3_RAFT` | basin raft slot 0 (x3, west pier) · 1 (x14, island jetty) · 2 (x25, east pier) |
| V316 | `G3_PRACTICE_RAFT` | 0–6 (170) |
| V317 / V318 | `G3_CULVERT_A/B` | 0–4 (175) |
| S315 | `G3_BELL` | OFF = seaward (west in the south channel) · ON = inland (east, and north in the Race) |
| S316 | `G3_GATE` | basin lock gate closed |
| S317 | `G3_PRACTICE_GATE` | |
| S318 | `G3_PRACTICE_HIGH` | |
| S319 | `G3_CULVERT_SNAG` | snag post up |
The level is the map you are on (171 Low · 172 Mid · 173 High). No variable is needed.

### 170 Lock Hall — TEACH "drift, then stop" (21×17, harbour palette)
```
     012345678901234567890
y0   ##########E##########    E (10,0) → 171 (14,21)
y1   #########...#########    pier x9-11 rows 1-6 (the only way north)
y2   #########...#########
y3   #########...#########
y4   #########...#########
y5   #########...#########
y6   #########...#########
y7   #~r~~~~~~~~|~~~~~~~~#    practice channel rows 7-9 · r = raft (1x3), start slot 0 (x2) · | gate (x11)
y8   #~r~~~~~~~~|~~~~~~~~#
y9   #~r~~~~~~~~|~~~~~~~~#
y10  #...................#
y11  #..W.T.....g.....A..#    W practice wheel (3,11) · T Fisherman Gunnar (5,11) · g gate lever (11,11) · A "Tove" (17,11)
y12  #...........k.......#    k lock-keeper NPC (12,12)
y13  #...................#
y16  ##########@##########    @ (10,16) from Ebbmouth (rows 13-15 floor)
```
- **Practice slots** (raft column): 0 x2 · 1 x4 · 2 x6 · 3 x8 · 4 **x10** · 5 x13 · 6 x16. The gate at x11 sits between
  slots 4 and 5. Only slot 4 lands on the pier (x9–11); every other column meets wall at row 6.
- **Wheel W** (action):
  - Low → raise (S318 on). The raft drifts east: `V316 = S317 ? 4 : 6`.
  - High → lower (S318 off). The chain tows the raft home: V316 = 0. "The lock drains. A chain winds the raft back to
    its berth."
- **Gate lever:** `pfp_flip(317)`. The gate events at (11, 7–9) show closed or open.
- **Raft tiles:** `Practice raft x,y` for each slot column (rows 7–9), shown at V316 == slot. While S318 is on, the
  page uses the passable plank tile; while low, the grounded impassable art.
- **Solution:** close the gate, raise the water, and the raft drifts to the gate. Walk the raft (x10) up the pier to E.
  Raising first sends the raft past the gate; lower to tow it home and try again. Failure is free.
- Lock-keeper: "Water lifts what floats. Current takes what's loose. A gate stops what's drifting. That's the whole job,
  kid; the rest is overtime."

### 171 / 172 / 173 Basins — TWIST + COMBINE "three levels, one raft" (29×23 each, identical walls)
```
     01234567890123456789012345678          (Mid water shown; Low = mud in ~ areas, High = see notes)
y0   ##############E##############          E (14,0) → 174 (High map only; from ND)
y1   ###########.......###########          ND north dock x11-17 rows 1-3 · T Sailor Bjorn (16,2) [173]
y2   ###########.......###########
y3   ###########.......###########
y4   #~~~~~~~~~~~~~^~~~~~~~~~~~~~#          channel N "the Race" rows 4-6 · ^ lane x14 (High: current)
y5   #~~~~~~~~~~~~~^~~~~~~~~~~~~~#
y6   #~~~~~~~~~~~~~^~~~~~~~~~~~~~#
y7   #.....~~~~~.......~~~~~.....#          WP x1-5 rows 7-15 · IS x11-17 rows 7-12 · EP x23-27 rows 7-15
y8   #..G..~~~~~.......~~~~~..B..#          G gate lever (3,8) on WP · B bell rope (25,8) on EP
y9   #.....~~~~~...C...~~~~~.....#          C wheel C (14,9)
y10  #.....~~~~~.......~~~~~.....D          D (28,10) culvert grate → 175 (EP, Mid only)
y11  #.....~~~~~....i..~~~~~.....#          i Super Potion (15,11)
y12  #.T...~~~~~.......~~~~~...i.#          T Swimmer Leif (2,12) [172] · i Net Ball (26,12)
y13  #.....~~~~~~~~.~~~~~~~~.....#          IS jetty x14 rows 13-15
y14  #.....~~~~~~~~.~~~~~~~~.....#
y15  #.....~~~~~~~~.~~~~~~~~.H...#          H (24,15)-(24,16) EP ladder (Low only)
y16  #~~R~~~~~~~~~~R~~~~|~~~~~R~~#          channel S rows 16-18 · R = raft slot columns x3 / x14 / x25 · | gate x19
y17  #~~R~~~~~~~~~~R~~~~|~~~~~R~~#          T Swimmer Ingrid (16,17) [171, in the trench]
y18  #~~R~~~~H~~~~~R~~~~|~~~~~R~~#          H (8,18) SW ladder down to the trench (Low only)
y19  #...........................#          SW south walkway rows 19-21
y20  #..W.........A..........E...#          W wheel W (3,20) · A apprentice "Tove" (13,20) · E wheel E (24,20)
y21  #.....................T.....#          T Fisherman Oskar (22,21) [172]
y22  ##############@##############          @ (14,22) ← 170
```
**Per level:**
- **Low (171).**
  - The `~` areas are mud, walkable.
  - The piers, the island and ND are quays, too high to climb, except at the ladders H: SW↔trench at x8, EP↔trench at x24.
  - The raft lies grounded in the trench at its slot column and **blocks the trench** there.
  - The closed **gate** walls the trench at x19.
  - So the walk along the trench from SW to EP needs the gate open and the raft not at slot 1.
- **Mid (172).**
  - Water is level with the walkways. The raft (3 tiles, rows 16–18, at its slot column) is a bridge between SW and
    whatever pier it sits against: slot 0 → WP, 1 → the IS jetty, 2 → EP.
  - No other crossings exist.
- **High (173).**
  - The walkways stay dry. Channel S is white water (impassable).
  - The **Race lane** at x14 rows 4–6 is a current: touch it from the IS north edge → if S315 is on, you ride north to
    ND (14,3) (`pfp_push_line(:up, :current)`); if off, it shoves you back onto IS: "The current's running seaward. It
    spits you back."

**Drift rule** (applied by any wheel that *enters* High, before the transfer):
`if S315 (inland, east): V315 = (S316 && V315 <= 1) ? 1 : 2` · `else (seaward, west): V315 = (S316 && V315 == 2) ? 2 : 0`.
In words: the raft runs with the current until it hits the end or the closed gate.

| Device | Where | Action |
|---|---|---|
| Wheel W | SW (3,20), all maps | level −1: `pfp_swap_map(171/172)`. On Low: "The water's as low as it goes." |
| Wheel E | SW (24,20), all maps | level +1 (apply drift if → High) |
| Wheel C | IS (14,9) | Mid → High (drift) · High → Mid · on Low: "The chain hangs slack in the mud." |
| Bell rope | EP (25,8) | `pfp_flip(315)`. "DONG. The river turns: now it runs inland / seaward." |
| Gate lever | WP (3,8) | `pfp_flip(316)`. The gate events (x19, rows 16–18) show closed/open; on Low they block |
| Raft tiles | `Raft s,y` at x ∈ {3,14,25}, y = 16–18, on each map | shown at V315 == slot. Mid: passable plank · Low: impassable grounded raft · High: decor (drifting) |

**Landing fix-ups for `pfp_swap_map`:** wheels stand on walkways, which are dry on every level, so no fix-ups are needed.
Wheel C on IS: IS is dry on Mid and High.

**Solution (verified, BFS over the full state; shortest 16 actions):**
1. On SW: wheel E twice → High. Bell off: the raft drifts west to **slot 0**.
2. Wheel W twice → Low. Ladder H (x8) into the trench, walk east, ladder H (x24) onto EP. **Ring the bell** (now
   inland). Walk the trench back to SW.
3. Wheel E → Mid. Cross the raft (slot 0) to WP. **Close the gate.** Cross back to SW.
4. Wheel E → High. The raft drifts east and **stops against the gate at slot 1**.
5. Wheel W → Mid. Cross the raft (slot 1) to the island jetty. **Wheel C** → High. Take the Race lane north (bell on) to ND
   and door E.

**The aha moments:**
- *The tide moves the raft for you.* Step 1, discovered after one look at High.
- *The gate parks it mid-channel.* Step 4: the island is the only crossing the current can't deliver, until the gate
  says stop.
- Low water is not a dead level: the trench is the only way to the bell.

**Hints (Tove):** 1 "The raft goes where the river goes. Ring for inland, leave it for seaward." 2 "Ma closes the gate
when she wants a boat to stop halfway." 3 the solution.
**Reset:** Tove (on SW on every map) → V315 = 2, S315 and S316 off, transfer to 171 (14,21).

### 174 Warden's Pool — arena (19×17, unchanged)
Marisol, single battle. Badge 3 + TM03 Water Pulse. The existing quay scene follows.

### 175 Overflow Culvert — MASTERY (optional; 21×15; via grate D on EP at Mid, behind a Rock Smash rock (TM98, Badge 2))
One channel (rows 6–8), 5 slots (x4, 7, 10, 13, 16). Two 1×3 rafts: A (V317, starts 0) and B (V318, starts 1).
The **snag post** at slot 2 (x10) is a hook that catches only rafts drifting **seaward (west)**. Islet chest north of
slot 2.
```
     012345678901234567890
y0   #####################
y3   #########*###########    * chest on the islet (9,3), islet x9-11 rows 4-5
y5   #.......#...#.......#
y6   #~~~A~~B~~^~~~~~~~~~#    ^ snag post (10,5) seen from the islet · raft A at x4, B at x7
y7   #~~~A~~B~~~~~~~~~~~~#
y8   #~~~A~~B~~~~~~~~~~~~#
y9   #...................#
y10  #..V.....s.......A..#    V valve (3,10): [Flush east] / [Flush west] · s snag lever (9,10) · A apprentice
y14  ##########@##########
```
- A **flush** moves both rafts as far as they can go in that direction. They stack against the end or each other. A
  westward flush also stops the first raft that passes slot 2, if the snag is up.
- **Solution:** flush **east** (A, B → slots 3, 4). Raise the snag. Flush **west**: A is caught at slot 2 and B stacks at 3.
  Cross A at x10 to the islet chest.
- **The aha:** the hook only faces the sea. You have to send the rafts *past* it first.
- **Reward:** Elemental Seed ×2 (on Water Surface: +1 Speed and Aqua Ring) + Mystic Water.

**Gym 3 trainers (5):** Fisherman Gunnar (170), Swimmer ♀ Ingrid (171 trench), Swimmer ♂ Leif and Fisherman Oskar (172),
Sailor Bjorn (173 ND). Lv 19–22.

---
## Gym 4 — Lumen City, Circuit Gym · Rook Calder (Electric, `:NEON_GRID`, cap 27) · ★★★★

**Core rule: route the power, never the alarm.** Conduit nodes rotate. Power flows from a generator through matching ports
and lights whatever lamps the circuit reaches. **Twist:** tee nodes split power, and one lamp is Rook's camera
"alarm", which resets the board. **Combine:** Rook's **Rotom drone** is a *portable wire* (a follower you can dock into a
gap). Latching relays stay open after the power is cut, and live strips shock, so the circuit you need is also the wall
in your way. **Mastery:** light every node for the B-roll. **The aha** belongs to the story: in the Core, the Zap Plate's
cradle is cold. The gym runs on a Meridian main.
**Warden link:** Rook is a hacker-engineer who is always on camera ("Chat says you're gonna lose"). The drone and the
alarm are his streaming rig. Mechanically, the secret that "he doesn't hold the Plate" becomes the last power source you
splice. **Field:** Neon Grid (trainers run Volt Switch, Charge and Magnet Rise). **Kingdom:** Zenith's showcase city.

### State
| ID | Name | Use |
|---|---|---|
| S320 | `G4_190_DOOR` | 190 door lamp lit (recomputed by `pfp_power`) |
| S321 | `G4_LATCH_GATE` | 192 inner gate latched open (permanent) |
| S322 | `G4_LATCH_CORE` | 192 Core door latched open (permanent) |
| S323 | `G4_DRONE_DOCKED` | Rotom docked in socket g1 (192) |
| S324 | `G4_191_DOOR` | 191 door lamp lit (live: recomputed) |
| V320 | `G4_ALARMS` | alarm count in 191 (hint tiers) |
| S420 | `G4_191_SIDE` | 191 side lamp lit → Edit Bay door |
| S421 | `G4_EDITBAY_DONE` | Mastery chest |
Node rotations are one-hot self switches (`pfp_rotate`). **Port masks:** N=1, E=2, S=4, W=8. Base shapes at rotation 0:
`I` = N+S, `L` = N+E, `T` = N+E+S. Each rotation turns the shape clockwise. Power enters a node only through a port that
faces the source, and passes to a neighbour only if both facing ports exist (`pfp_power`).

### 190 Switchroom — TEACH (17×13)
```
     01234567890123456
y0   ########D########    D (8,0) door → 191 (13,19); passable while S320
y1   #...............#
y5   #...............#
y6   G===1===2===3==L#    G generator (0,6) · nodes 1 (4,6) I rot0 · 2 (8,6) I rot1 · 3 (12,6) I rot0 · L lamp (15,6) · = strip art
y7   #...............#
y10  #..A.........r..#    A apprentice "Spark" (3,10) · r Rook's drone hovering (13,10), talks
y12  ########@########
```
Each node: action → `pfp_rotate(name, 2)` (I has 2 states), then `pfp_power(:g4_190)`, which sets S320 when L is lit.
**Solution:** turn node 1 and node 3 once. The strip lights end to end and the door opens. Drone: "Chat says turn the
sideways ones. Chat is, for once, right."

### 191 Breadboard Hall — TWIST "tees, and the alarm" (27×21)
Nodes on a 4×3 grid at **x = 6, 11, 16, 21; y = 5, 10, 15** (named `Node c,r`). Strips (decor tiles) join neighbours.
The generator sits on the west wall at (1,10) and feeds node (0,1) from the west. **Lamps:**
- **DOOR**: the north door at (21,0), fed from node (3,0)'s N port; strip x21, rows 1–4. Passable while S324 is on.
- **ALARM**: Rook's camera flash on the east wall (26,10), fed from node (3,1)'s E port.
- **SIDE**: the Edit Bay door on the south wall (11,20), fed from node (1,2)'s S port. Passable while S420 is on.

Entrance @ (13,20). Apprentice "Spark" at (2,18). Trainers: Engineer (8,8), Super Nerd (19,13).

| Node (c,r) | Shape · start rotation |
|---|---|
| (0,0) | L · 1 |
| (1,0) | I · 0 |
| (2,0) | T · 2 |
| (3,0) | L · 3 |
| (0,1) | T · 0 |
| (1,1) | L · 2 |
| (2,1) | I · 1 |
| (3,1) | T · 1 |
| (0,2) | L · 0 |
| (1,2) | T · 3 |
| (2,2) | L · 1 |
| (3,2) | I · 0 |

- Node action: `pfp_rotate`, then `pfp_power(:g4_191)`. That updates S324 and S420. If ALARM is lit:
  - flash and SE "Thunder1", drone: "CHAT SAYS WRONG WIRE." V320 += 1;
  - every node returns to its start rotation (`pfp_state` reset).
- **Verified (exhaustive search over all rotations):**
  - **Door: 4 clicks.** Node (1,0) +1, node (2,0) +1, node (0,1) +2. That lights 8 of 12 nodes.
  - **The tempting middle-row route lights the ALARM** (also 4 clicks).
  - **Side door: 2 clicks.** Node (0,1) +1, node (1,2) +1. Door + side together: 6.
- **The twist:** the generator's tee wants to send power straight east along the middle row, which is where the alarm
  is. The door route bends north early.
- **Hints (Spark):** 1 "A tee sends power three ways. Make sure the third way's a wall." 2 "Go north at the
  generator, not east." 3 the solution.

### 192 Live Wire Hall — COMBINE "the drone is a wire; the latch remembers" (27×25, schematic)
```
     012345678901234567890123456
y0   #############|######E######    E (20,0) Core door → 193 (needs S322)
y1   #............|.....s.......#    s (20,1) last strip tile of circuit 2 = the door's approach tile
y2   #............|.....s.......#
y6   G===a===b....|...d==e......#   G1 (0,6) · a (4,6) I rot0 · b (8,6) L rot0 | east: d (17,6) L rot3 · e (20,6) L rot1
y7   #.......=....|...=.........#
y11  #.......=....|...=.........#    strip x8 rows 7-11 (b→g1) · strip x17 rows 7-11 (c→d)
y12  #.......g===[G]==c.........#    g1 socket (8,12) · strip x9-11 · [G] inner gate (13,12) latch L1 · strip x14-16 · c (17,12) T rot1
y13  #............|...!.........#    ! (17,13) ALARM (c's S port)
y23  #.....A......|.............#    A apprentice "Spark" (6,23)
y24  ######@######|##############    @ (6,24) ← 191 · | grille fence x13 (impassable)
```
**Circuits:**
- **Circuit 1 (west).** G1 → a → b → socket **g1** → the inner gate's lock **L1**. Docking the drone in g1 closes the
  gap.
- **Circuit 2 (east)** has no generator. It is fed *through* L1: the feed runs from L1 → c → d → e → the Core door's
  lock L2.
- So **circuit 2 is live only while circuit 1 is live.**

**Shock rule (this room only):**
- Strip tiles of a live circuit shock you: flash, SE "Paralyze1", you are pushed back 1 tile.
- The strips beside each lock (x9–11 row 12 for the gate; x20 rows 1–5 for the Core door) **are the approach tiles**.
  You cannot walk through a lock while it is powered.

**Devices:**
- **Drone (follower).** On entering, `Followers.add(drone, "RotomDrone")`. Socket g1 (action, from (7,12) or (8,13)):
  "Dock Rotom?" → `Followers.remove`, the socket shows the drone (S323 on), `pfp_power(:g4_192)`. Again: "Call Rotom
  back?" → S323 off, follower re-added, recompute. Leaving the room returns the drone (S323 off).
- **Latches.** When L1 is lit, S321 goes on *for good*; the gate events become passable. When L2 is lit, S322 goes on for
  good.
- **Alarm.** c's S port faces the alarm (17,13). If lit: the east nodes reset to their start rotations, plus the drone's
  line.

**Solution (6 + 3 clicks):**
1. West: turn a once (E–W) and b twice (W–S).
2. Dock the drone in g1. L1 latches (S321) and the gate unlocks, but its approach strip is live.
3. Call the drone back. The circuit dies and the gate stays open (**the latch remembers**).
4. Walk east. Turn **c → rotation 3** (W–N–E; its third port faces a wall), **d → 1** (S–E), **e → 3** (W–N).
5. Walk back west. **Dock the drone again.** Power runs through the open latch L1 into the east and lights L2 (S322).
6. Call the drone back, walk east, and the Core door is open.

**Two ahas:**
- *Power isn't needed once latched.* You must unplug the very circuit you just built.
- *Set the far side first, then power it from the near side.* If the east is wrong when you dock, the alarm resets it.

**Hints (Spark):** 1 "Latches hold. Wires don't have to." 2 "The east board has no generator. Where does its power
come from?" 3 the solution.
**Reset:** Spark → node states reset, S321–323 off, the drone back to you.

### 193 The Core — arena (19×15)
Before the arena door, the **Plate cradle** (action): "The Zap Plate's cradle is cold. There's dust in it. A thick
Meridian cable runs past it into the floor, warm to the touch." The arena door needs one splice node turned onto the
Meridian main (1 click). The drone films it, and Rook's voice comes over the PA: "...Turn it off. Rotom. Turn it *off*."
Rook, single battle. Badge 4 + TM43 Volt Switch + TM70 Flash.

### 950 Edit Bay — MASTERY (optional; via 191's side door; overflow ID 950 because 194–199 belong to Lumen districts)
A 3×3 board at x = 5, 9, 13; y = 4, 8, 12. Generator west of node (0,1). **Goal: every node lit** ("B-roll needs every
light on").
| | c0 | c1 | c2 |
|---|---|---|---|
| r0 | L · 1 | L · 3 | I · 1 |
| r1 | T · 0 | T · 3 | I · 1 |
| r2 | L · 1 | T · 0 | I · 1 |
**Verified solution (11 clicks, exhaustive search; the only other solution takes 12):** (1,0) +2 · (0,1) +2 · (1,1) +1 ·
(0,2) +3 · (1,2) +3.
**Reward:** Synthetic Seed ×2 (on Neon Grid: +1 Sp. Atk and Magnet Rise) + Cell Battery + "Rook's blooper reel" (a
comedy scene: Rook falling off his own stage).

**Gym 4 trainers (6):** Engineer ×2, Super Nerd, Scientist, Rocker, "Circuit Tester" (Engineer) in 192 east, at (23,18).
Lv 23–26.

---
## Gym 5 — Duneholt, the Dig · Sahar Ostrand (Ground, `:DESERT`, cap 31) · ★★★★★

**Core rule: sun hardens, shade sinks.** Sand lanes in direct sunbeam bake into glassy crust (walkable). Lanes left in
shade are soft and drop you to the **Under-Dig** below, at the same x,y. **Sun-mirrors** choose which lanes are lit.
**The aha:** falling is not failing; a drop is the fastest way *across*. **Combine:** a two-floor loop where you drop on
purpose to reach the mirror that controls the lane you need. **Mastery:** rub the mural that Sahar sealed.
**Warden link:** "The desert keeps everything. It just doesn't keep it where you left it." Sahar is a patient teacher,
so the first drop is a lesson, not a trap. **Field:** Desert (sandstorm fog on 211). **Kingdom:** Ossaria's tomb
country; the Under-Dig is an Elector-era necropolis.

### State
| ID | Name | Values |
|---|---|---|
| V325 | `G5_MIRROR_1` | 0 lights lane a · 1 lane b · 2 lights a wall |
| V326 | `G5_MIRROR_2` | 0 lane c · 1 lane d · 2 a wall |
| S325 | `G5_MURAL_DONE` | |
| S326 | `G5_FIRST_FALL` | first-drop message shown |
| V425–V428 | `G5_TABLET_A..D` | 0–3 (215) |

### 210 Entrance — TEACH "the first drop" (21×17)
A cracked sand floor (x8–12, y6–8) sits between the entrance and the far door. The far door is fake: a painted
mural. Sahar's aide: "Everyone tries the door. The way in is *down*." Touch the soft sand → it drops you to 212's
**cellar** (x10–18, y22–23), where a ladder at (14,22) climbs to 211 (14,22) on the entrance plaza.

### 211 The Dunes / 212 The Under-Dig — TWIST + COMBINE (29×25 each; twin footprints)
```
211 The Dunes (true scale)                       212 The Under-Dig (true scale; same footprint)
     0         1         2                             0         1         2
     01234567890123456789012345678                     01234567890123456789012345678
y0   ##############E##############                y0   #############################
y1   ####cccccc.........#dddddXXX#                y1   ####......##########.......D#
y2   ####cccccc.........#dddddXiX#                y2   ####......##########........#
y3   ####cccccc......T..#dddddXXX#                y3   ####......##########........#
y4   ####cccccc.........#dddddXXX#                y4   ####......##########........#
y5   ####cccccc##########dddddXXX#                y5   ####.........T.....#........#
y6   ####cccccc##########dddddXXX#                y6   ####...............#........#
y7   ####cccccc##########dddddXXX#                y7   ####......#######..#........#
y8   #.......#############....####                y8   #################..#####H####
y9   #.......#############.......#                y9   #################..##########
y10  #.......#############.......#                y10  #################..##########
y11  #.......#############.......#                y11  #################.......#####
y12  #.M.....#############.....M.#                y12  #################......H#####
y13  #.......#############.......#                y13  #############################
y14  #.......#############.......#                y14  ##H.#########################
y15  #.......#############.......#                y15  ##..#########################
y16  #.......#############.......#                y16  ##..#########################
y17  ####aaaaaa#########bbbbbb####                y17  ##........#########......####
y18  ####aaaaaa#########bbbbbb####                y18  ####......#########..T...####
y19  ####aaaaaa.........bbbbbb####                y19  ####..T...#########......####
y20  ####aaaaaa.........bbbbbb####                y20  ####......#H.............####
y21  ####aaaaaa.........bbbbbb####                y21  ####......#########......####
y22  ##########....@....##########                y22  ##########....H....##########
y23  ##########.......A.##########                y23  ##########.........##########
y24  #############################                y24  #############################
211: E (14,0) stairs → 213 · T3 x10-18 y1-4 (T Ruin Maniac (16,3)) · lanes a/b/c/d · X cistern x25-27 y1-7, i Max Ether (26,2)
     T1 x1-7 y8-16 with M1 (2,12) · T2 x21-27 y8-16 with M2 (26,12) · T0 x10-18 y19-23 · @ (14,22) cellar ladder arrival · A (17,23)
212: five sealed galleries, one ladder H each (verified by flood fill): Uc (under c, long dig) → H (23,12) → T2 ·
     Ud (under d + cistern vault) → H (24,8) → T2, D (27,1) Rock Smash door → 215 · Ua → H (2,14) → T1 ·
     Ub → H (11,20) → T0 · cellar (from 210) → H (14,22) → T0 · trainers T: Hiker (13,5), Picnicker (6,19), Hiker (21,18)
```
- **Terraces (always firm):** T0, T1, T2, T3 as drawn. The rock outcrop is impassable on both floors, except where
  212's tunnels run under it.
- **Lanes (sand):** **a** T1 ↔ T0 · **b** T0 ↔ T2 · **c** T1 ↔ T3 · **d** T2 ↔ the cistern X (dead end, Max Ether).
- **Lane tiles** are events `Sand <lane> x,y`.
  - Lit → tile CRUST (passable).
  - Soft → blank (sand) + `touch` → "The sand swallows you!" → fall animation → `pfp_swap_map(212)` at the same x,y.
  - The pages implement "a lit iff V325 == 0", etc. (two-page pattern).
- **Mirrors** (action, rotate the aim): **M1 on T1 (2,12)** cycles V325 0→1→2; **M2 on T2 (26,12)** cycles V326. Each aim
  draws a beam overlay (event tiles, `Beam M1 …`) across its lane.
- **212 ladders** (`touch` → `pfp_swap_map(211)` at the same x,y) are listed under the map. The galleries never connect, so
  where you fall decides where you come up.
- **Start:** V325 = 0 (lane a lit), V326 = 1 (lane d lit).

**Solution (verified, BFS; impossible without dropping):**
1. Walk lane **a** to T1.
2. Step onto lane **c**: it is soft, so you drop into Uc. Follow the long dig tunnel to ladder (23,12); up to **T2**.
3. Turn **M2 twice** (d → wall → c): lane c is now crust.
4. Step onto lane **b**: soft, drop to Ub, ladder (11,20) up to **T0**.
5. Walk lane **a** (still lit) to T1, then walk lane **c** (now lit) to T3 and the stairs.

**The aha:** the mirror for lane c is on the *far* terrace, and the only way to it is to fall through lane c itself.
**Hints (aide "Nadim", T0 (17,23)):** 1 "Sahar says the dig taught her more than the dunes ever did." 2 "Lane c's mirror is
on the east terrace. Fall into c and see where it takes you." 3 the solution.
**Reset:** Nadim → V325 = 0, V326 = 1, to T0. Falls are free and need no reset.

### 213 Warden Arena (21×17)
Sahar, single battle. Badge 5 + TM83 Bulldoze. Strength (HM04) comes from the excavators afterwards (WORLD §4).

### 215 Mural Gallery — MASTERY (optional, 21×15; via the Rock Smash door in Ud)
- Four pivoting tablets T_a–T_d (action: cycle V425–V428 through **Sun · Eye · Wave · Bone**).
- Each gallery of 212 has one Elector glyph carved over its ladder: **Ua: Wave, Ub: Sun, Uc: Bone, Ud: Eye** (sign
  events: "A carved Wave, worn by water that hasn't run here in 300 years").
- Caption: "Each road remembers what lies beneath it." Set every tablet to its own lane's glyph → `pfp_check(:g5_mural)`.
- Failure lines name the wrong tablet ("The b-tablet grinds and stops. The Sun doesn't sit there.").
- **Reward:** Telluric Seed ×2 (on Desert: +1 Def, +1 Sp. Def, −1 Speed) + Soft Sand, and a mural fragment (lore:
  sealed AF 281, on Valen's order).
- Sahar, afterwards: "I buried that. The sand dug it up. I'd rather not argue with sand twice."

**Gym 5 trainers (5):** Ruin Maniac ×2, Hiker ×2, Picnicker ×1. Lv 27–30.

---
## Gym 6 — Mirefen, the Infirmary · Corvin Mott (Poison, `:CORROSIVE_MIRE`, cap 35) · ★★★★★

**Core rule: dose makes the cure.** Unmarked flasks (3 and 5 measures). Funnels and basins accept *exact* doses. The tap
is the only place you can fill a flask. You can pour between flasks, or tip them into the sludge, anywhere.
**Twist:** make 4 from 3 and 5. **Combine:** the doses must be *carried* across a toxic gallery on a mask-filter step
budget, and one basin is cumulative, so you plan trips. **Mastery:** the Quiet Ward (4 and 9).
**Warden link:** "Everything's poison, dear. Dose makes the cure." Corvin is a physician, and his doomed apprentice
**Wenlow** is the apprentice NPC. His cheerful hints are written to land differently on a replay after Ch16. **Field:**
Corrosive Mire (Purify turns the field to water; trainers carry Acid Spray). **Kingdom:** Nadir's runoff marsh.

### State
| ID | Name | Values |
|---|---|---|
| V330 / V331 | `G6_FLASK_3 / G6_FLASK_5` | 0–3 / 0–5 |
| V332 | `G6_FILTER` | sludge steps used (0–10) |
| V333 | `G6_BASIN` | 0–7 (cumulative) |
| S330 | `G6_VALVE_4` | 231 purge valve dosed |
| S331 / S332 | `G6_SOCKET_A / G6_BASIN_B` | 232 doses delivered |
| S333 | `G6_QUIET_DONE` | 234 |
| V430 / V431 / V432 | `G6_FLASK_4 / G6_FLASK_9 / G6_PATIENTS` | 234 |

**The bench** (one event type, reused): action → choice menu `Fill the 3 · Fill the 5 · Pour 3→5 · Pour 5→3 · Tip the 3
out · Tip the 5 out · Look at the flasks` (pour = transfer until the source is empty or the target is full). Away from a
bench, the same menu without the two Fill options is on a **key item** "Corvin's Flask Case" (register it to Ready).
**Funnels** (action): `Pour the 3 / Pour the 5`. Exact → success. Wrong → the flask is wasted, and Wenlow names the
amount ("That's 2. The funnel wants 4. Dose makes the cure, sir says. Sir says it a lot.").

### 230 The Ward — TEACH (21×17)
Bench + a funnel needing **3**. Fill the 3, pour. The ward's inner door opens. Corvin's sign: "If you can count to three,
you can count to anything. Measure, don't guess."

### 231 Dispensary — TWIST "four from three and five" (29×25)
```
     0         1         2
     01234567890123456789012345678
y0   ##############E##############   E (14,0) → 232 (needs S330)
y2   #..........######...........#
y3   #..........#FFFF#...........#   F purge funnel needs 4 (14,3)
y8   #....B.................T....#   B bench (5,8) · T Scientist (23,8)
y12  #.......W...........T.......#   W Wenlow (8,12) apprentice · T Burglar (20,12)
y24  ##############@##############
```
**Solution (6 actions):** Fill 5 → pour 5→3 (5 holds 2) → tip 3 → pour 5→3 (3 holds 2) → fill 5 → pour 5→3 (5 holds 4)
→ pour the 5 into the funnel.
**Hints (Wenlow):** 1 "Sir always says: the empty space is a measure too." 2 "Get a 2 into the little one first." 3 the
solution.

### 232 Sludge Gallery — COMBINE "carry the cure" (29×25)
```
     0         1         2
     01234567890123456789012345678
y9   #############################   rows 0-8 / 14-24: the ward corridors (trainers) and walls
y10  #....~~~~~~...~~~~~~~~......#   tap end x1-4 · sludge 1 x5-10 (6 steps) · island A x11-13 · sludge 2 x14-21 (8 steps) · dais x22-27
y11  #BR..~~~~~~.a.~~~~~~~~..b...E   B bench (1,11) · R refill (2,11) · a socket A needs 1 (12,11) · b basin B needs 7 (24,11) · E exit (28,11)
y12  #....~~~~~~.r.~~~~~~~~......#   r refill (12,12) · no refill on the dais
y13  #############################
```
- **Sludge tiles** (`~`): walkable. A step hook (`pfp_step_hook`) adds 1 to V332 per sludge step. At 10: "Your mask
  filter is spent!" → fade → back to the tap end (V332 = 0). Flask contents and deliveries are **kept**.
- Refill stations set V332 = 0.
- **Socket A** takes exactly 1 (one pour).
- **Basin B** is cumulative: V333 += the pour. At exactly 7, S332 goes on. Above 7: "It overflows and drains." V333 = 0.
- **Why it's a combine:** you can't fill anywhere but the tap, 1 + 7 = 8 = both flasks full, and a flask holding
  exactly 1 can't be made without the tap.
- **Plan (two deliveries):**
  1. At the tap: fill 3 → pour into 5 → fill 3 → pour into 5 until full. The 3 holds **1**.
  2. Carry it to A (6 steps). Refill at A. Walk back (6).
  3. At the tap: fill 5 → pour 5→3 → tip 3 → pour 5→3 (3 holds 2) → fill 5. You carry **2 + 5**.
  4. Tap → A (refill) → B (8 steps). Pour both: 7.
- Wandering in the sludge costs a reset, never progress.
- **Hints (Wenlow):** 1 "You can pour between flasks anywhere, sir lets me. You can only *fill* at the tap."
  2 "Basin B adds up. Bring two flasks that add to seven." 3 the plan.

### 233 The Theatre — arena (21×17)
Corvin, single battle. Badge 6 + TM84 Poison Jab. Surf (HM03) comes from the ferrymen afterwards.

### 234 The Quiet Ward — MASTERY (optional, 21×15; door from 232's tap end)
- Flasks of **4 and 9** (V430/V431). A bench at the ward door.
- Three beds whose IV funnels need **1, 3 and 6** (V432 tracks the beds done).
- Verified sequences:
  - **1** = fill 9, pour into 4, tip 4, pour into 4: the 9 holds 1.
  - **3** = fill the 4 and pour it into the 9, three times: the 4 holds 3.
  - **6** = the 3 above, then tip the 9 and continue: fill 4 → 9 (7), fill 4 → 9 (9; the 4 holds 2), tip 9, pour 4 → 9
    (2), fill 4 → 9 (6).
- Patients are Fixing (turning to "garden furniture"), so this room is quiet and dim, with no comedy.
- **Reward:** Synthetic Seed ×2 (on Corrosive Mire: poisons the holder, +1 Atk and +1 Sp. Atk) + Black Sludge +
  Wenlow's note: "Thanks for helping with the Quiet ones. Sir pretends he doesn't cry. — W."

**Gym 6 trainers (5):** Scientist ×2, Burglar *(Nadir scavenger)* ×2, Aroma Lady ×1. Lv 31–34. None stand in sludge.

---
## Gym 7 — Cindervault, the Foundry · Brann Holloway (Fire, `:VOLCANIC`, cap 39) · ★★★★★★

**Core rule: pour, then quench.** A trench channel is *empty* (a gap). Pour a crucible into it and it is *molten*
(impassable, glowing). Quench it and it is *iron* (a bridge). **Twist:** crucibles pour once, through spouts aimed at one
of two channels, and the foundry has **one** quench. **Combine (cross-floor):** a channel still molten when you go down
the slag chute **drains into the mould below**, so it is a gap upstairs and a bridge downstairs. **Mastery:** "forge to
break right". Drain the channel everyone quenches and a cracked mould opens a vault.
**Warden link:** "Some things you forge to last. Some things you forge to *break* right — that's the harder craft."
The bridge you deliberately *don't* finish is the one that carries you. **Field:** Volcanic (Rock moves hit as Fire;
trainers lean on Lava Plume). **Kingdom:** Ashkaar's forge-guilds, commoners under a dragon-lord.

### State
| ID | Name | Values |
|---|---|---|
| V335 / V336 / V337 | `G7_AIM_K1 / K2 / K3` | K1: 0 → X1, 1 → X2 · K2: 0 → X2, 1 → X3 · K3: 0 → X1, 1 → X3 |
| V338 | `G7_QUENCH` | quench charges left (starts 1) |
| S335 / S336 / S337 | `G7_POURED_K1 / K2 / K3` | crucible spent |
| S338 | `G7_TEACH_DONE` | 250 bridge |
| S339 | `G7_VAULT_DONE` | vault chest |
| V435 / V436 / V437 | `G7_X1 / X2 / X3` | 0 empty · 1 molten · 2 iron (251 channels) |
| S435 / S436 / S437 | `G7_M1 / M2 / M3` | mould under X_k is iron (252) |

### 250 Gate Hall — TEACH (21×17)
One crucible, one channel (rows 8–9), one quench wheel. Pour → molten. Quench → iron → cross. The foreman points at a
floor grate: "And what you *don't* quench runs down to the moulds below. Waste not."

### 251 Pour Floor — TWIST (29×25)
```
     0         1         2
     01234567890123456789012345678
y0   ##############E##############   E (14,0) → 253
y1   #.............N band........#   N band rows 1-3 · ladder from 252 M3 side at (24,2)
y4   #XXXXXXXXXXXXX3XXXXXXXXXXXXX#   X3 rows 4-5 (channel)
y6   #...........mid2..........C2#   mid2 rows 6-9 · C2 chute (24,7) → 252
y10  #XXXXXXXXXXXXX2XXXXXXXXXXXXX#   X2 rows 10-11
y12  #...H.......mid1............#   mid1 rows 12-15 · H (4,13) ladder from 252 M1 side
y16  #XXXXXXXXXXXXX1XXXXXXXXXXXXX#   X1 rows 16-17
y19  #..K1...K2...K3.......A..Q1.#   S band rows 19-23 · crucibles K1 (3,19) K2 (7,19) K3 (11,19) · A apprentice (21,19)
y20  #......................Q2...#   quench valves Q1 (26,19) Q2 (24,20) Q3 (26,21) (one per channel, one shared charge)
y21  #.........................Q3#
y22  #.............C1............#   C1 chute (14,22) → 252
y24  ##############@##############
```
- **Channel tiles** `X<k> x,y`: P0 [—] blank (empty trench art, impassable) · P1 [V43k≥1] tile MOLTEN (impassable;
  `touch` from an adjacent tile: "Too hot!") · P2 [V43k≥2] tile IRON (passable).
- **Crucible K** (action): if spent: "Empty." Else choose `Aim the spout / Pour`. Aim cycles its two channels and the
  spout graphic turns. Pour: the target channel becomes molten if empty, re-melts if iron, and nothing happens if
  already molten. Then the crucible is spent.
- **Quench valve Q_k:** if V338 > 0 and channel k is molten → iron, V338 −= 1. Otherwise: "The cistern's dry." or
  "Nothing to quench."
- **Chutes C1/C2** (`touch`): first **drain**: for every molten channel k, X_k = empty and M_k = iron ("A roar below: the
  moulds fill."). Then `pfp_swap_map(252)`.

### 252 Mould Floor — COMBINE (29×25, below 251)
- **M1** (pit, rows 16–17) separates the chute-1 landing (S part) from the M1 side (rows 12–15). The ladder **H (4,13)**
  there goes up to 251's **mid1**.
- **M2** (rows 10–11) separates the M1 side from the **vault** (rows 6–9, centre): see Mastery.
- **M3** (rows 4–5) separates the chute-2 landing (24,7) from the north side. The ladder **(24,2)** goes up to 251's **N band**.
- Each `M<k>` tile: P0 [—] blank (pit) · P1 [S43k on] tile IRON_CAST (passable).
- Trainers: Worker (8,21), Black Belt (20,8).

**Solution (verified by hand; 3 pours, 1 quench, 2 drains):**
1. Pour **K3 → X1**, **K1 → X2**, **K2 → X3** (aim first).
2. **Quench X2** only.
3. Take chute C1: X1 and X3 drain, so M1 and M3 are iron.
4. Below: cross M1 → ladder H → 251 mid1 → cross X2 (iron) → mid2 → chute C2.
5. Below: cross M3 → ladder → N band → E.

**The aha:** the natural move, quenching X1 to cross it, leaves X2 un-quenchable and M1 a pit. "The bridge you don't
finish upstairs is the one that carries you downstairs."
**Hints (apprentice "Sooty", S band):** 1 "Brann never wastes a pour. Whatever's still hot when you go down, the moulds
get." 2 "You only need one bridge upstairs. Which one can't the moulds give you?" 3 the solution.
**Reset:** Sooty → crucibles refilled, aims 0, V338 = 1, X and M all reset, player to the S band.

**MASTERY "forge to break right" (in 252's vault; no extra map).** If X2 is *also* left molten when you take C1, M2 casts
across the pit and you can reach the **vault**. Its cracked mould has split under the pour and exposes Brann's
apprentice-piece hoard.
- **Reward:** Elemental Seed ×2 (on Volcanic: burns the holder, +1 Atk/Sp. Atk/Speed) + Charcoal + "Brann's first hammer"
  (lore: his AF 280 Festival match with Valen).
- That run can't finish, because X2 is gone upstairs. Sooty resets it and you take the main route.
- Brann, after: "Ha! Found the cracked one. Aye — some things you break *on purpose*."

### 253 Warden Arena (21×17)
Brann, single battle. Badge 7 + TM35 Flamethrower.

**Gym 7 trainers (5):** Worker *(Engineer)* ×2, Black Belt, Camper "Kindler", Cool Trainer ♂. Lv 35–38.

---
## Gym 8 — Ironreach, the Pit · Kaito Ren (Fighting, `:COLOSSEUM`, cap 43) · ★★★★★★

**Core rule: every step you take, they take.** Sparring partners are **pursuers**: after each of your steps, each one
steps one tile toward you (`pfp_pursue(:chase)`).
- **Movement:** they first try the axis with the larger gap; if that is blocked, the other axis; if both are blocked,
  they wait.
- **Blockers:** they cannot cross **rope lines**, boulders or each other.
- **Contact:** a partner stepping onto your tile ends the round. The first time, it is that trainer's battle; after
  that: "Stand up. Again." Partners and boulders return to their marks.

**Twist:** rope lines you can step over but they can't. **Combine:** Strength boulders block pursuers and hold plates.
**Mastery:** lure the pursuers *onto* the plates, because a sparring partner weighs as much as a boulder.
**Warden link:** "Stand up. Again." "A fist is a promise." Kaito's discipline is control, and the pit punishes rushing.
The Mastery door is his guilt, made physical. **Field:** Colosseum (knockouts power the crowd). **Kingdom:** Nadir's
pit-fighting quarter in old Aurel mine shafts.

### State
| ID | Name | Use |
|---|---|---|
| S340 / S341 / S342 | `G8_BELL_1 / BELL_2 / GAUNTLET` | rooms cleared |
| S343 | `G8_MARROWGATE` | 275 cleared |
| V340 | `G8_ROUNDS` | contacts this visit (hint tiers) |
Pursuer and boulder start squares come from the map. Boulders use `pbPushThisBoulder` (Strength; Badge 5 has passed). A
plate is "held" while a boulder or pursuer stands on it (`pfp_check`). Partners that have been battled stay as pursuers;
their battle simply isn't repeated.

### 271 Sparring Floor — TEACH + TWIST (29×25; two halves)
**West half "The Pillar" (TEACH, x1–13):** one partner (Machop, Black Belt "Daigo") at (7,4). A 3×3 pillar at (6–8, 9–11).
The bell is at (7,1), behind the partner. You start at (7,21).
- **Solution:** walk up the east side of the pillar until the partner commits to the east, then circle the pillar
  clockwise. A greedy chaser always chases the larger gap, so it follows you round and parks on the far side. Dash to
  the bell.
- Kaito's sign: "Don't fight the one in front of you. Move it."

**East half "Rope Line" (TWIST, x15–27):** two partners (Crush Girl "Mae" at (17,4), Black Belt "Ren" at (25,4)). A rope
line `r` across row 12 (x15–27) has one gap at x21. The bell is at (21,1). You start at (21,22).
- Ropes are passable to you only.
- **Solution:** step over the rope at x17 and draw Mae south to the rope. Walk back east along row 13 (below the rope).
  Mae is stuck behind the line and Ren comes through the gap. Lead Ren south-west, around and back over the rope at x26,
  and ring the bell.
- Builder: verify both halves with the pursuer BFS.

### 272 Rope Ring — TWIST, harder (29×25)
- Three partners. A ring of ropes around a central bell dais (x10–18, y8–16) with two gaps (N (14,8) and S (14,16)).
- Boulder-free. You must get all three partners on the *wrong* side of a rope at the same time.
- Intended: enter the ring through S, exit over the east rope, re-enter over the north rope, and ring the bell while the
  partners funnel through the gaps.

### 273 The Gauntlet — COMBINE (29×25)
```
     0         1         2
     01234567890123456789012345678
y0   ##############E##############   E (14,0) → 274 (gate opens while plates P1 and P2 are held)
y2   #.............P1..........r.#   P1 plate (14,2)
y6   #....O........###.....O.....#   O boulders (5,6), (22,6)
y10  #..p.....rrrrr.....rrrrr..p.#   p partners (3,10), (26,10) · rope segments
y14  #.........O...P2....O.......#   P2 plate (14,14) · O (10,14), (20,14)
y22  #.............@...A.........#   @ (14,22) · A apprentice "Hiro" (18,22)
```
- **Rule:** both plates must be held at the same time; you can't stand on two at once.
- **Solution shape:** push boulder (10,14) east four tiles onto P2. Use boulder (20,14) to wall off the east partner's
  greedy path. Then lure the west partner across the rope gap so it can't follow, and push boulder (5,6) along row 6 and
  up to P1.
- **Push budget:** 30 pushes (Kaito: "Discipline over rage"). V341 `G8_PUSHES` counts them; over budget, the boulders reset.
- Builder: verify with the BFS (boulders + pursuers; small grid).

### 274 The Pit — arena (21×17)
Kaito: **tag battle** with Kestrel (K4 arc), or a single battle on Standard (story team confirms). Badge 8 + TM31 Brick
Break.

### 275 Marrowgate Door — MASTERY (optional, 21×15; side door in 273)
- A sealed iron gate with three plates. Knocking sounds play from behind it (SE loop), and Lucario's aura flickers on the
  wall.
- **One** boulder. **Two** sparring partners.
- **The aha:** partners are heavy, so lure each one onto a plate. A greedy chaser stops on the plate if the next tile
  toward you is blocked: stand behind a rope, directly past the plate.
- **Reward:** Telluric Seed ×2 (on Colosseum: +1 Atk and Focus Energy) + Black Belt.
- A plaque: "MARROWGATE — SEALED AF 285 — BY ORDER." Kaito, after the badge: "You opened it. It was empty, wasn't it.
  ...I always hoped it would be."

**Gym 8 trainers (6):** Black Belt ×2, Crush Girl ×2, Battle Girl-style "Crush Kin" ×1, Pit Brawler *(new)* ×1. These
are the pursuers. Lv 39–42.

---
## Gym 9 — Verdance, the Heartgarden Gym · Juno Hale (Grass, `:FLOWER_GARDEN`, cap 47) · ★★★★★★★

**Core rule: water spreads.** Watering a plot grows it **and its neighbours** by one stage, mod 4:
- 0 bare bed
- 1 sprouts
- **2 vine bridge** (walkable over the canals)
- **3 hedge** (impassable overgrowth)
- watering a hedge collapses it to 0.

**Consequence:** the **arena's Flower Garden field starts at stage 1 + (number of hedges you leave in 291 and 292)**,
max 5. Overgrowth is literally Juno's strength. **Twist:** a ring of six. **Combine:** two rings sharing one junction
plot. **Mastery:** the Bride Bower's exact pattern.
**Warden link:** Juno, new Warden in a runaway bloom: "Please don't go easy on me — I'll cry either way." The gym
guide warns you plainly that over-watering helps her. That is a real, honest trade-off (fewer waterings vs a harder
fight). **Field:** Flower Garden stages (FIELDS.md), via `setBattleRule("fieldStage", n)`. **Kingdom:** Elowen's royal
gardens, the Evergreen Crown's pride.

### State
Plot stages are one-hot self switches (`pfp_state`, 4 states). No IDs are needed.
| ID | Name | Use |
|---|---|---|
| V345 | `G9_HEDGES` | hedges left, recomputed on leaving 291/292 (`pfp_check(:g9_hedges)`) → arena stage |
| S345 / S346 | `G9_RING_DONE / G9_EIGHT_DONE` | path complete (for gates and hint text) |
| S347 | `G9_BOWER_DONE` | |

**Plot event:** P0 [—] bed (impassable; canal below) · P1 [self A] sprouts · P2 [self B] **vine bridge (passable tile)**
· P3 [self C] **hedge (impassable)**. The watering can is a key item. Action on a plot → "Water it?" →
`pfp_water(name)` adds +1 to it and to the neighbours listed in the room. Plots are watered from the walkway beside them.

### 290 Gate — TEACH (21×17)
One plot over the entrance canal at stage 1. Water once → bridge. A second, decorative plot beside it also grows (its
neighbour), and Juno's sign points it out: "Gardens are gossips. Water one and the neighbours hear about it."

### 291 Hedge Garden — TWIST "the ring of six" (29×25)
- Six plots P1–P6 in a ring around a fountain, each spanning a canal.
- The path crosses the canals at **P1, P3, P5** (they must be 2). P2, P4, P6 are free, but any of them left at 3 is a
  hedge.
- Neighbours: P_i ↔ P_{i±1} (P6 ↔ P1).
- **Start: P1–P6 = 0, 0, 1, 2, 1, 2.**

**Verified (exhaustive, mod 4):**
- **Cheapest: 2 waterings** (P2 once, P6 once) → 2,1,2,2,2,**3** = one hedge (P6).
- **Clean: 5 waterings** (P4 once, P5 twice, P6 twice) → 2,0,2,1,2,2 = no hedges.
- The guide: "Every hedge you leave, she gets stronger. Your call, challenger."

**Hints (apprentice "Bram", Juno's cousin):** 1 "Water the plot *next* to the one you want." 2 "P6 is nearly
overgrown already; watering it collapses it, but it also feeds P1." 3 both solutions.

### 292 Glasshouse — COMBINE "two rings, one heart" (29×25)
- A figure-eight: ring A (J, A1, A2, A3, A4) and ring B (J, B1, B2, B3, B4) share the **junction J**.
- J has four neighbours (A1, A4, B1, B4). The others have two.
- The path needs **J, A2, A3, B2, B3 = 2**.
- **Start: J = 1; A1–A4 = 0, 3, 1, 2; B1–B4 = 2, 0, 3, 1.**
- **Verified (exhaustive, 256 solutions):**
  - **fewest waterings: 7** (J ×0, A1 ×2, A3 ×1, B1 ×1, B3 ×1, B4 ×2) → **2 hedges**.
  - **no hedges: 8** (J ×2, A1 ×2, A3 ×1, B3 ×2, B4 ×1).
- **The combine:** the junction couples both rings; fixing ring A through J disturbs ring B.
- Sun lamps (decor) and the glass roof.

### 293 Warden Arena (21×17)
Juno (J3), **double battle**. Field `:FLOWER_GARDEN` at stage `1 + min(V345, 4)`. Badge 9 + TM53 Energy Ball. Juno,
if the stage is 4+: "You let it grow? For me? ...That's either kind or tactical and I'm too nervous to ask which."

### 297 The Bride Bower — MASTERY (optional, 21×15; gate in 292, open after S346)
- Five plots in a row under an arch. Neighbours are left and right only (the ends have one).
- **Target 2,3,2,3,2** (bridge-hedge alternating, "the bridal arch").
- **Start 0, 2, 1, 3, 1.**
- **Verified minimum 6:** P2 ×2, P3 ×3, P5 ×1.
- Hedges here don't count toward the arena.
- **Reward:** Telluric Seed ×2 (on Flower Garden: +1 Sp. Def and Ingrain, and the garden grows) + Miracle Seed + a
  pressed Bride Tree petal (lore: Elin).

**Gym 9 trainers (5):** Aroma Lady ×2, Pokémon Breeder, Picnicker, Gardener *(Lass)*. Lv 43–46.

---
## Gym 10 — Rimeholt, the Lake Hall · Anja Sorrel (Ice, `:FROZEN_LAKE`, cap 51) · ★★★★★★★

**Core rule: ice remembers weight.** Native v21 ice sliding (terrain tag `Ice`: you slide until something stops you). A
**cracked** tile holds once: the first slide over it cracks it, and the second gives way. You drop into the under-ice
grotto and climb back to the room's start. **Twist:** a room where the shortest line uses a crack twice, so you plan
around your own footprints. **Combine:** **ice blocks** slide when pushed (stopped by rock, blocks or floor), and a block
that slides into a broken crack **plugs** it. The plug becomes rough ice: a stopper, and the room's built-in repair kit.
**Mastery:** a 33-move room.
**Warden link:** "Ice remembers. Every crack. Every weight. You walk on my lake, it knows your name by spring." Anja
signed the Lattice knowing the lake was cracking: the gym is her guilt in physics. **Field:** Frozen Lake (cracks →
Water Surface). **Kingdom:** Isenmar's ice-fishers.

### State
Crack states are one-hot self switches on each `Crack x,y` event: none = intact, A = cracked, B = broken (a hole; fall
`touch`), C = plugged (rough ice, stops slides). Block positions use `pbPushThisEvent` + `pfp_save(:g10_<room>)`.
| ID | Name | Use |
|---|---|---|
| S350 / S351 / S352 | `G10_HALL / CRACKWALK / SOUNDING` | rooms cleared (doors stay open) |
| V350 | `G10_FALLS` | falls this visit (hint tiers) |
**Fall:** touching a broken crack → "The ice gives way!" → 316 Under-ice Grotto (a short cave with a ladder) → back to
the room's start. The room's cracks are **kept** (they remember), so the apprentice reset matters here.
**Sliding blocks** are custom: the push moves the block until stopped (`pfp_push_line` applied to the event). A block
crossing a broken crack drops in: the crack goes to state C, the block is erased (self switch), and the block is saved.

### 310 Boathouse — TEACH (21×17)
A 7×5 ice pond with two rocks. Slide to the far side. One cracked tile sits on an *optional* line to a Pearl, so a
second visit drops you (Anja's net-mender: "Told you. It remembers.").

### 311 Ice Hall — TWIST "every crack once" (29×25; puzzle area 13×11 at offset (8,7))
```
     0123456789012       (local; room x = 8 + local x, y = 7 + local y)
y0   ######E######       E (6,0) → 312
y1   ##..........#
y2   #..#.#...c.##       c = cracked tile · # inside = rock
y3   #...#.c##...#
y4   #.....#.....#
y5   ##.c........#
y6   #.....c.....#
y7   #.#......#.##
y8   #...........#
y9   #...#....c.##
y10  ######F######       F (6,10) start floor (non-ice) ← 310
```
- **Verified (BFS, slide model, cracks hold once):** shortest **17 slides**:
  `U R U L U L D L D R U L D R U R U`. Ignoring cracks it would be 13, so the cracks *are* the puzzle.
- **Hints (apprentice "Liv", Anja's granddaughter, at room (22,22)):** 1 "Gran says you get one go over each crack.
  Plan where you've already been." 2 "The straight way up crosses the middle crack twice." 3 the slide list.
- **Reset:** Liv → all cracks intact (self switches cleared), player to F.

### 312 Crackwalk — COMBINE "blocks, cracks and plugs" (29×25; puzzle area 13×11 at offset (8,7))
```
     0123456789012
y0   ##########E##       E (10,0) → 313
y1   ##.....##...#
y2   #....##.#...#
y3   #.........#.#
y4   #....B...c.c#       B ice blocks at (5,4) and (5,7)
y5   #...#.......#
y6   #...........#
y7   #c..#B....#.#       (local (5,7) block; (4,7) and (10,7) rock)
y8   #.......#...#
y9   #c..........#
y10  ######F######       F (6,10) start
```
(Block glyphs `B` mark ice blocks standing on ice. The underlying tile is `.`.)
- **Push rule:** walk into a block from a standing tile and the block slides in that direction until it meets rock,
  another block, or floor. You stay put.
- **Verified (BFS):** **16 actions**, `U L U R D [push R] L D R U [push U] U L U R U`. It is **unsolvable without
  pushing**: the two blocks become the stoppers the room lacks.
- **The plug (the aha):** if you break a crack, push a block over the hole. It sinks in and leaves rough ice, *a new
  place to stop*. The apprentice's tier-2 hint teaches it as a repair, and players then use it on purpose in 315.
- **Hints (Liv):** 1 "A block's just a rock you can move." 2 "Broke one? Shove a block into the hole. Rough ice
  stops you." 3 the list.

### 313 Warden Arena (21×17)
Anja, single battle. Badge 10 + TM13 Ice Beam. Rock Climb TM100 comes from the ice-climbers afterwards.

### 315 The Sounding — MASTERY (optional; 21×17, puzzle area 15×13; door in 312)
```
     012345678901234
y0   ##########E####     E (10,0) → the Sounding hole (reward)
y1   #.#...........#
y2   #........#....#
y3   #...#...B.....#     B blocks at (8,3), (4,6), (6,9)
y4   #.......#c...##
y5   #....c........#
y6   #.#.B..#..#...#
y7   ##.........c###
y8   #.....#c...#..#
y9   #.#.c.B...c...#
y10  #....#...#....#
y11  #......c.....c#
y12  #######F#######
```
- **Verified (BFS): 33 actions**, 7 of them pushes:
  `U R U R D L [L] D L [L] L U [U] L D R U [U] [L] U L D R U R [R] D R D R U L U` (`[X]` = push).
  Unsolvable without pushing.
- **Reward:** Elemental Seed ×2 (on Frozen Lake: +1 Def, +1 Speed) + Never-Melt Ice. At the hole, Anja's family
  sounding-line: "Every name the lake has learned since AF 90." Yours is the newest.

**Gym 10 trainers (5):** Skier-style Cool Trainer ♀ ×2, Hiker, Swimmer ♂ (ice diver), Boarder *(new)*. All stand on
floor tiles off the slide lines. Lv 47–50.

---
## Gym 11 — Skyreach, the Gale Post · Odessa Gale (Flying, `:STORMFRONT`, cap 55) · ★★★★★★★★

**Core rule: the wind doesn't care.** **Gust lanes** are corridors where the wind carries you end to end
(`pfp_push_line(:wind)`). A lane can only be ridden *with* the wind. **Weather vanes** on the decks flip lanes, and every
vane is rigged to **two** lanes. **Twist:** coupled vanes on a five-platform deck; the vanes are on different platforms,
so you ride lanes to reach the vane that fixes the lane you need. **Combine:** the Mail Chute, where letter sacks ride
the same lanes, stack at lane ends and become stoppers. **Mastery:** deliver the dead letters.
**Warden link:** "Skyreach's got one law: the wind doesn't care. Everything else is negotiable." Odessa smuggles refugees
and letters, and the Mastery is literally her dead-letter archive (Morwen's letters to "I."). **Field:** Stormfront
(trainers use Tailwind and Hurricane). **Kingdom:** Zenith's airship spire.

### State
| ID | Name | Use |
|---|---|---|
| S355–S360 *(see below)* | `G11_L1..L6` | lane direction bits for 331 (OFF = a→b, ON = b→a) |
Lanes L1–L5 use S355–S359 and L6 uses S455 (secondary). Sack positions are saved with `pfp_save(:g11_chute)`.
| S456 | `G11_CHUTE_DONE` | |
| S457 | `G11_ARCHIVE_DONE` | |

### 330 Hangar — TEACH (21×17)
One gust lane across a gap, and one vane beside it. Ride it, flip the vane, ride back. A courier: "Wind goes one way at a
time. You don't argue with it; you just wait at the right end."

### 331 Gust Deck — TWIST "coupled vanes" (29×25, schematic)
```
           P4 (exit E (14,0))
            ^ L4
  P3 (20,6) ---L6--- P1 (8,6)
   |  \               |
   L3   (V2 on P3)    L1          P0 start (8,20) · P1 (8,6) · P2 (20,20) · P3 (20,6) · P4 (14,1)
   |                  |
  P2 (20,20) --L5-- P0 (8,20) --- L2 joins P1 (8,6) and P2 (20,20) diagonally (a long N-S then E-W lane)
```
| Lane | Joins | Start (bit) | Flipped by |
|---|---|---|---|
| L1 | P0–P1 | 1 (P1→P0) | V3 |
| L2 | P1–P2 | 0 (P1→P2) | — |
| L3 | P2–P3 | 1 (P3→P2) | V2 |
| L4 | P3–P4 | 0 (P3→P4) | V1 |
| L5 | P0–P2 | 0 (P0→P2) | V3 |
| L6 | P1–P3 | 1 (P3→P1) | V1, V2 |
**Vanes:** **V1 on P0** flips L4 and L6 · **V2 on P3** flips L3 and L6 · **V3 on P2** flips L1 and L5. Each vane's rods
are visible running to its two fans.
- **Lane entry** (`touch` at the lane mouth): with the wind → ride to the far platform. Against it: "The gale shoves you
  back."
- **Verified (BFS): 14 actions.**

| # | Action | Arrive / effect |
|---|---|---|
| 1 | V1 | L4, L6 flipped |
| 2 | L5 | P2 |
| 3 | V3 | L1, L5 flipped |
| 4 | L5 | P0 |
| 5 | L1 | P1 |
| 6 | L6 | P3 |
| 7 | V2 | L3, L6 flipped |
| 8 | L6 | P1 |
| 9 | L2 | P2 |
| 10 | L5 | P0 |
| 11 | V1 | L4, L6 flipped |
| 12 | L1 | P1 |
| 13 | L6 | P3 |
| 14 | L4 | P4 |

- **The aha:** L6 is on two vanes, so it is the "hinge" you flip twice. The final approach needs L4 forward *and* L6
  forward at the same time, which means using V1 a second time after V2 has spoiled L6.
- **Hints (courier "Pip"):** 1 "Every vane works two fans. Look up — the rods show which." 2 "The P1–P3 lane is on two
  vanes. Fix it last." 3 the table.

### 332 Mail Chute — COMBINE "sacks ride the wind" (29×25)
- Three gust lanes, each with a vane (4 directions here, not 2): a crossroads chute.
- Three letter sacks (pushable: `pbPushThisEvent`). A sack pushed into a lane mouth rides to the far end and stops
  against the end wall or another sack. **Sacks stack.**
- Three pigeonholes (plates) at lane ends must each hold a sack. A sack in a lane also **shortens the lane for you**:
  you stop one tile before it. That is the only way to land on the mid-lane ledge holding the third pigeonhole.
- **Intended order:**
  1. Sack 1 down the east lane (vane E) into pigeonhole A.
  2. Turn the north vane south. Push sack 2 so it stacks *before* the north wall.
  3. Ride the north lane: you stop at the ledge beside pigeonhole C.
  4. Push sack 3 off the ledge into C. Re-aim and deliver sack 2 to B.
- Builder: verify with the Sokoban BFS.

### 333 Captain's Deck — arena (21×17)
Odessa, **double battle** (Tailwind theme). Badge 11 + TM51 Roost. Waterfall (HM05) comes from the sky-river guides
afterwards.

### 334 Dead-Letter Archive — MASTERY (optional; 21×15; door in 332)
- Pigeonholes labelled by kingdom. Five dead letters on a gust carousel: one lane loop with four vanes.
- Route each letter to its kingdom by setting the vanes before each push. The addresses are written as riddles in
  Gale Post slang (a sign glossary).
- The Morwen letter (to "I.") cannot be delivered. Its hole is "Abroad — closed by quarantine". Leaving it in the
  carousel completes the room (Odessa: "Some letters you keep.").
- **Reward:** Elemental Seed ×2 (on Stormfront: +1 Speed and Charge) + Sharp Beak + the undelivered letter (key item,
  for K6/Ysolde).

**Gym 11 trainers (6):** Bird Keeper ×2, Pilot *(Cool Trainer ♂)* ×2, Sky Courier *(new)*, Gambler. Lv 51–54.

---
## Gym 12 — Lucent, the Athenaeum · Ilsa Marr (Psychic, `:MINDSCAPE`, cap 59) · ★★★★★★★★

**Core rule: your reflection keeps you honest.** Beyond a mirror wall walks your **reflection**. When you step left it
steps right; up and down match. Its side has **different walls**. If either of you is blocked, that one stays put while
the other moves: the only way to "desync" the pair. Plates and doors need you **both** in place. **Twist:** a hall where
the walls differ, so you steer two bodies with one stick. **Combine:** **swap pads** trade your places, and **thought
tiles** may be stood on only by the reflection. **Mastery:** the Quiet Room.
**Warden link:** "You're thinking very loudly. Please stop." Ilsa reads minds. The gym makes you think in two
directions at once, and the Quiet Room is about the truth she kept sheathed for eleven years. **Field:** Mindscape
(Topsy-Turvy → Inverse). **Kingdom:** Antumbra, the Kingdom Behind the Glass.

### State
| ID | Name | Use |
|---|---|---|
| S360 / S361 / S362 | `G12_HALL / ATRIUM / GALLERY` | rooms cleared |
| S363 | `G12_QUIET_DONE` | |
| V360 | `G12_RESETS` | hint tiers |
The reflection is an event moved by `pfp_pursue(:mirror)` after each player step, with its own pane's passability. On
leaving a room, it snaps back to its start.

### 350 Reading Room — TEACH (21×17)
Two identical 5×5 panes. You and the reflection start mirrored, with mirrored plates. Walk up three, step left (it
steps right), and both stand on plates. "See? It's only you, the other way round."

### 351 Mirror Hall — TWIST (29×25; two 9×9 panes: yours at (2,8), the reflection's at (18,8))
```
 your pane (local)     reflection pane (local; its x runs the other way to yours)
     012345678            012345678
y0   #########            #########
y1   #.##....#            #.......#     goals: you (6,1) · reflection (7,1) (plates)
y2   #...#...#            #...#..##
y3   #.....###            #.......#
y4   #.#.....#            #....##.#
y5   #...###.#            #.##..#.#
y6   #...#..##            #...##.##
y7   #...#...#            ###.....#     starts: you (1,7) · reflection (7,7)
y8   #########            #########
```
- **Verified (BFS): 26 steps**, `U U R R R R U R R U U U L L L L L L D R R U R U U L`. That is the longest of 4,000
  generated boards, and it uses three deliberate desyncs.
- **Hints (apprentice "Ada", an Athenaeum reader):** 1 "When it bumps a wall and you don't, you've gained a step on it."
  2 "Start by walking it into the wall at its row 7." 3 the sequence.

### 352 Swap Atrium — COMBINE (29×25)
- Two panes again. Each holds **swap pads**: step on one and you and the reflection trade places, mirrored. **Thought
  tiles** (shimmering) are walls to you and floor to the reflection.
- The door needs you on plate P and the reflection on plate Q. Q is ringed by thought tiles, so only the reflection
  can reach it. P is in a pocket of your pane that only the reflection's pane leads to (via a swap).
- **Intended:**
  1. Lead the reflection through the thought maze to the pad nearest Q.
  2. Swap: you are now in its pane, beside Q's maze; it is in yours, beside P.
  3. Walk *it* onto P (desync against a wall), then swap back, and walk yourself onto Q's neighbour.
- Builder: verify with the two-walker BFS (`mapgen/puzzles/reflection.py`).

### 354 Warden Arena (21×17)
Ilsa, single battle. On Hard: an EBDX multi-bar intro. Badge 12 + TM29 Psychic.

### 356 The Quiet Room — MASTERY (optional; 17×13; ID 356, as 355 is the Palace undercroft)
- Five sealed doors, and five Athenaeum readers in front of them. Each reader makes one statement about which door holds
  "the truth Ilsa kept".
- **Rule (on the wall):** "Exactly two readers lie."
- Statements (sign texts):
  - A: "It is behind door 2 or 4."
  - B: "C lies."
  - C: "It is behind door 5."
  - D: "A and C are both honest."
  - E: "It is not behind door 2."
- **Unique answer: door 4.** Check: if door 4, then A true, C false, B true, D false, E true → liars C and D, exactly two
  ✓. Every other door gives a liar count other than two.
- Choose a door: wrong → "A reader sighs. *That's what you wanted to be true.*" (reset).
- **Reward:** Magical Seed ×2 (on Mindscape: +2 Sp. Atk, confused) + Twisted Spoon + Ilsa's unsent letter to Valen (lore;
  feeds `:ILSA_RECONCILED` later).

**Gym 12 trainers (6):** Psychic ♂ ×2, Psychic ♀ ×2, Channeler, Scholar *(Super Nerd)*. Lv 55–58.

---
## Gym 13 — Cragholm, the Lamp Galleries · Bastian Ore (Rock, `:CRYSTAL_CAVERN`, cap 63) · ★★★★★★★★★

**Core rule: light remembers its colour.**
- A miner's lamp throws a beam. **Mirrors** (`/` or `\`, one-hot, 2 states) turn it.
- **Filter crystals** recolour it. **Gates** open only to their colour; an **alarm crystal** (red) cracks and resets the
  board.

**Twist:** the obvious route crosses a red filter, and the gate wants blue. **Combine:** Strength **boulders** block beams,
and **splitters** fork them. The cavern's own **prism glow** (the field's red → blue → green → amethyst cycle) sets the
lamp's starting colour, and it advances each time a gate opens. **Mastery:** Bastian's story *is* the code.
**Warden link:** "Rock's patient. Rock'll wait for you to make a mistake for a thousand years." Bastian tells long
stories that turn out to be important, and the Mastery code is in his story. **Field:** Crystal Cavern (Prism glow;
Light moves ×1.5). **Kingdom:** Ossaria's deep seams, where Bastian hides fugitives.

### State
Mirrors are one-hot (`pfp_state`, 2 states). Beam segments are events lit by `pfp_beam` (self A). Boulder positions use
`pfp_save`.
| ID | Name | Use |
|---|---|---|
| S365 / S366 | `G13_GATE_1 / GATE_2` | gates opened (latched) |
| V365 | `G13_GLOW` | 0 red · 1 blue · 2 green · 3 amethyst (the cavern's current glow) |
| S367 | `G13_STORY_DONE` | Mastery |

### 370 Lamp Room — TEACH (21×17)
One lamp, two mirrors, one white gate. Turn both mirrors and the beam bends around a pillar into the gate. Bastian's lamp
boy: "Light goes straight till it's told otherwise. Same as me."

### 371 Prism Gallery — TWIST "the colour the gate wants" (29×25; board 15×11 at offset (7,7))
```
     012345678901234          (local)
y0   .......A.......          A alarm crystal (7,0) — red
y1   ....M..R..M....          M2 (4,1) · R red filter (7,1) · M3 (10,1)
y4   ..........b....          b blue filter (10,4)
y5   L...M..M.......          L lamp (0,5) shines east · M1 (4,5) · M6 (7,5)
y8   ....M.....M...G          M5 (4,8) · M4 (10,8) · G blue gate (14,8) → 372
y10  ....S..........          S side crystal (4,10), white → side alcove (Max Revive)
```
- **Start:** M1 `/`, M2 `\`, M3 `/`, M4 `/`, M5 `\`, M6 `\` (state 0 = `/`). Nothing is lit.
- **Verified (exhaustive, 64 configurations):** **blue gate: 3 turns** (M2 → `/`, M3 → `\`, M4 → `\`).
  The path:
  1. Lamp → M1 up → M2 east → **red** filter → M3 down → **blue** filter → M4 east → gate.
  2. The beam turns red, then blue: the gate accepts it because the last filter wins.
- Other three-turn configurations hit the **alarm** (red) or the **side** crystal (white). The alarm flashes and returns
  every mirror to its start.
- **The twist:** the shortest-looking path runs along row 5 (M6) and never meets the blue filter.
- **Hints ("Pell", lamp boy):** 1 "A crystal takes the last colour that touched it." 2 "Go up first, then come down the
  east side." 3 the solution.

### 372 Quarry — COMBINE (29×25)
- Two lamps, one splitter (a beam entering it continues *and* forks left and right), two gates (green and amethyst),
  three Strength boulders, one Rock Climb wall to the upper gallery.
- **Glow:** the lamps shine in the cavern's current colour V365. The glow advances one step each time any gate opens:
  red → blue → green → amethyst.
- **Intended:**
  1. Open the green gate first, which needs the glow at green: open the 371 gate's twin "practice" gate here at the
     lower lamp to advance red → blue → green.
  2. Push boulder 1 into the splitter's west fork, so only the east fork reaches the green gate.
  3. Once it opens, the glow becomes amethyst. Pull boulder 1 back (Strength from the other side, via the Rock Climb
     wall), and push boulder 2 to block the east fork, so the amethyst beam reaches the amethyst gate.
- Builder: verify with `pfp_beam` + boulder BFS.

### 373 Warden Arena (21×17)
Bastian, single battle. The field can darken (Dark Pulse → Dark Crystal Cavern). Badge 13 + TM76 Stealth Rock.

### 374 Bastian's Seam — MASTERY (optional; 21×15)
- Bastian tells his crown story in 370: three "um, where was I" pauses, each naming a stone colour in order. The
  story is long on purpose, and a sign later quotes it.
- The seam's four colour crystals must be lit in **that order** (amethyst, red, green, blue) by turning a single lamp
  turret (4 positions).
- **Reward:** Telluric Seed ×2 (on Crystal Cavern: +1 Def, +1 Sp. Def) + Light Clay + a fugitive's thank-you (Larch is
  hiding here in Act IV, foreshadowed).

**Gym 13 trainers (5):** Hiker ×2, Ruin Maniac, Worker, Gemcutter *(Lady)*. Lv 59–62.

---
## Gym 14 — Gravenmoor, the Hollow Cathedral · Ysolde Ashgrave (Ghost, `:HOLLOW_CATHEDRAL`, cap 67) · ★★★★★★★★★

**Core rule: the dead walk where you walked.**
- Ringing the nave bell moves you between the **Living Nave** (391) and the **Dead Nave** (392): twin maps, same x,y,
  through `pfp_swap_map`.
- The Dead Nave has ghost walls and broken floors (open crypts).
- **Pews** are real in both worlds: push one in the Living Nave, where the floor is whole, and it stands in the same
  place in the Dead Nave, **bridging an open crypt**.

**Twist:** bridging the dead world from the living one. **Combine:** in the Requiem Crypt, **Morwen's echo** replays your
last 12 steps when you ring the hand-bell, then stays where those steps ended, holding a plate while you walk elsewhere.
**Mastery:** Morwen's chapel and the letter for Kestrel.
**Warden link:** "The dead aren't gone here. They're just very bad at conversation." Ysolde keeps Morwen's promise. The
echo *is* Morwen's lingering echo, and her chapel holds the sealed letter (story K6). **Field:** Hollow Cathedral
(Consecrated stage 2). **Kingdom:** Antumbra's mournful province.

### State
| ID | Name | Use |
|---|---|---|
| S370 | `G14_NAVE_DONE` | |
| S371 | `G14_CRYPT_DONE` | |
| S372 | `G14_CHAPEL_DONE` | |
| V370 | `G14_ECHO_LEN` | steps recorded (0–12) |
Pew positions: `pfp_save(:g14_pews)`, restored on **both** 391 and 392 (the twin rule). The echo's recorded path is an
array in `pfm`.

### 390 Narthex — TEACH (21×17)
The bell-rope toggles between two small twin rooms. A pew in the living room is pushed one tile over a crack, and in the
dead room that crack is an open grave the pew now spans. Ysolde: "Whatever you move among the living, the dead must
walk around."

### 391 / 392 Living and Dead Naves — TWIST (29×25 twins)
- Pews: 6 (pushable, horizontal 2-tile pews are two linked events moved together by the helper).
- Ghost walls (392 only) close the side aisles. Open crypts (392 only) cut the central aisle into three islands.
- The altar door (392 only) is at the north end.
- **Rule:** you can only *push* pews in 391 (the dead can't move wood). In 392 they are fixed.
- **Intended:**
  1. In the living nave, push pews 2 and 5 into the central aisle over the crypt marks: bridges in the dead nave.
  2. Push pew 3 *out* of the aisle where it would block the dead nave's only path round the ghost wall.
  3. Ring, then walk the dead nave over the pew bridges to the altar door.
- The trap: a pew pushed onto a crypt mark in the *wrong* orientation blocks the aisle in both worlds. The apprentice
  resets the pews.
- Builder: verify with the two-map BFS (positions × world).

### 393 Requiem Crypt — COMBINE "the echo" (29×25)
- **Echo rule:** ring the hand-bell to start recording (a chime). Each step is stored, up to 12. Ring again to stop:
  Morwen's echo appears at the start square and walks your recorded steps, then **stays** (and holds plates). Ringing
  again erases her. One echo at a time.
- The crypt door needs **three plates** held at once. You stand on one; the echo stands on another; the third is under
  the coffin lid that only the echo can pass (ghost wall).
- **Intended:**
  1. Record the walk through the ghost wall *in the dead nave* and onto plate C. Swap there, record 6 steps, and stop.
  2. Return to the living nave by ringing the main bell (the echo stays in the dead world, on C).
  3. Push the last pew onto plate B. Stand on A.
- Uses all three systems: worlds, pews, echo. Builder: verify with the BFS.

### 394 Warden Arena (21×17)
Ysolde, **double battle**. Badge 14 + TM30 Shadow Ball.

### 395 Morwen's Chapel — MASTERY (optional; 17×13)
- Six candles. Morwen's echo lights them **in the order you lit them last time you were here**, which on a first visit
  is none.
- The gravestone verses give the order. The aha: record your path past the candles with the echo, so the *echo* lights
  the last candle while you stand at the lectern (two candles are on opposite sides of a ghost wall).
- **Reward:** Magical Seed ×2 (on Hollow Cathedral: +1 Sp. Def, the holder becomes part Ghost) + Spell Tag + **Morwen's
  sealed letter** (story K6; Ysolde: "When he's ready. I don't think anyone is ever ready.").

**Gym 14 trainers (6):** Channeler ×3, Gentleman (revenant), Lady, Mourner-acolyte *(HOLLOW)*. Ghost trainers exist only in
392. Lv 63–66.

---
## Gym 15 — Cogsworth, Strade Works · Magnus Strade (Steel, `:FACTORY`, cap 71) · ★★★★★★★★★★

**Core rule: tolerances.** The whole works runs on **one clock that ticks when you step**. Every player step (or a press of
a **time-clock** punch, which spends a tick standing still) advances V375 (0–3).
- **Belts** move what stands on them 1 tile per tick: you, crates, Magnus's Klink.
- **Presses** slam on their beat (a press marked "2" is down on tick 2). Being under a press when it comes down = "Line
  stop!" → back to the room start.
- **Lever groups** reverse whole sets of belts.

It is turn-based: no reflexes, only precision. **Twist:** reversing groups shares belts between routes. **Combine:** the
**crane** drops a crate where you choose. A crate under a press when it slams **jams it open forever** (a permanently
safe tile). Crates ride belts, so you drop them *upstream* and let the line deliver them. **Mastery:** three crates, three
bays, the same tick.
**Warden link:** "I don't build weapons. I build tolerances." "Engineering will give us the next three hundred [years]."
Magnus believes in precision, and in the story he built the Arbiter core. The crane-jam is "breaking his machine
correctly", the same choice his Act V governor scene asks of him. **Field:** Factory (Explosion → Scrapyard). **Kingdom:**
Zenith's foundry district under martial law.

### State
| ID | Name | Use |
|---|---|---|
| V375 | `G15_TICK` | 0–3 (`pfp_step_hook` +1 per step; time-clock +1) |
| S375 / S376 / S377 | `G15_GROUP_A/B/C` | belt groups reversed |
| S378 | `G15_LINE_DONE` | 411 cleared |
| S379 | `G15_BAY_DONE` | 412 cleared |
| S475 | `G15_LAB_DONE` | 414 cleared |
Jammed presses are self switch A on each `Press` event. Crate positions use `pfp_save(:g15_<room>)`.
- **Belt events:** a `touch` page that calls `pfp_push_line(dir, :belt)` *on the tick* (the step hook moves everything on
  belts one tile per tick, in event-ID order: crates first, then you).
- **Press events:** page `[V375≥k]` shows the down graphic on beat k (two-page pattern). The step hook checks whether
  anyone is under a down press.

### 410 Gatehouse — TEACH (21×17)
One belt and one press (beat 2), and a time-clock beside the belt. Ride the belt; punch the clock once so the press
lifts before you arrive. Klink foreman: "The line moves when you move. Mr. Strade likes it that way."

### 411 Assembly Line — TWIST (29×25, schematic)
- Five belts in a serpentine to the exit (E (27,1)), crossed by three presses (beats 0, 1, 3).
- Groups: **A** = belts 1 and 3 · **B** = belts 2 and 3 · **C** = belts 4 and 5. Levers on side platforms.
- **The twist:** belt 3 is in two groups. The forward route needs belt 3 forward and belt 2 *backward* (to carry you to
  the lever for C). So pull **A then B** (belt 3 flips twice = forward, belt 2 backward, belt 1 backward). Ride 2 to the
  C platform, pull C, then use the time-clock twice before the beat-3 press on belt 5.
- Builder: verify with the tick BFS (state = position × tick × groups).

### 412 Crane Bay — COMBINE (29×25)
- Crane control (action menu: `← → Drop`) on a gantry over three belt lanes. Three crates in the hopper.
- Four presses guard the only route (beats 0–3, one per beat, so some press is always down).
- **Intended:** drop crate 1 on lane 2 two tiles upstream of press P2 so it arrives on P2's beat and jams it. Drop crate
  2 on lane 3 for P4 (the lane is reversed by group lever C first). P1 and P3 you time with the clock. The route then
  needs only two waits.
- **The aha:** you don't beat the machine, you *feed* it. A crate that arrives a tick late is crushed into scrap (Klink:
  "Tolerance exceeded.") and the crane refills after a reset.
- Builder: verify with the tick BFS.

### 413 Warden Arena (21×17)
Magnus, single battle. The partner battle with his apprentice comes just before, in the story. Badge 15 + TM91 Flash
Cannon. Dive (HM06) comes from the bathysphere works.

### 414 Tolerance Lab — MASTERY (optional; 21×15)
- Three belts converging on three bays. Each bay must receive its crate **on the same tick** (the bay doors close one
  tick after the first crate).
- Crates are placed by the crane at chosen distances. Belts have different lengths (5, 7, 8), so the drops must be
  staggered by the clock.
- **Reward:** Synthetic Seed ×2 (on Factory: +1 Atk, +1 Speed) + Metal Coat + Magnus's tolerance gauge (lore: the
  Arbiter core's spec sheet margin note, "±0. No exceptions.").

**Gym 15 trainers (6):** Engineer ×2, Worker ×2, Scientist, Meridian Foreman *(MERIDIAN_*)*. Lv 67–70.

---
## Gym 16 — Underveil, the Hall of Whispers · Nyx Calloway (Dark, `:NEW_MOON`, cap 75) · ★★★★★★★★★★

**Core rule: information is the key.**
- **Guards** walk fixed, step-driven patrols. They see 3 tiles ahead in the dark and **5 in lamplight** (essentials
  trainer sight, with lamplit tiles lengthening it). Seen = "Caught!" → back to the room start (no battle after the
  first).
- **Shuttered lanterns** light corridors, and a guard who sees a lantern open **turns to face it**.

**Twist:** use the lanterns to turn guards. **Combine:** in the Vault, every **secret** (dossier) you take **re-routes the
doors**, and taking one in the wrong order seals you in, until you **put it back** (taking is reversible). **Mastery:** the
Ledger: what will you sell?
**Warden link:** "Everything has a price. Yours just went up." Nyx trades in secrets. The Vault literally makes knowledge
change the building, and the Mastery is a moral choice about information (she sold Voss the Gilded Chain's location).
**Field:** New Moon (darkness lowers accuracy). **Kingdom:** Nadir's undercity, Underveil in drowned Aurelia's towers.

### State
| ID | Name | Use |
|---|---|---|
| S380–S383 | `G16_LANTERN_1..4` | 431 shutters open |
| S384 | `G16_GALLERY_DONE` | |
| S480–S484 | `G16_DOOR_1..5` | 432 doors d1–d5 open (the R1–R2 wall has no door) |
| V380 | `G16_CAUGHT` | hint tiers |

### 430 Vestibule — TEACH (21×17)
One guard walking a square loop and one lantern. Open the lantern: the guard turns to look at it, and you slip past
behind him. Nyx's voice over a speaking-tube: "Light is a lie you tell guards, darling."

### 431 Gallery of Shadows — TWIST (29×25)
- Three guards on loops of 8, 10 and 12 steps (all step-driven, so the loops are exact) and four lanterns.
- The exit is behind guard 3's loop, which watches it.
- **Intended:**
  1. Open lantern 2 to turn guard 1 north.
  2. Wait in the alcove (guards never look into alcoves) for guard 2's loop to reach its far end (5 steps).
  3. Open lantern 4 at the exit, which turns guard 3 to face it, *away from you*. Close lantern 2 behind you so guard
     1 resumes his loop without seeing the alcove.
- Builder: verify with the patrol BFS (state = position × step mod 120 × lanterns).

### 432 The Vault — COMBINE "knowledge moves the walls" (29×25)
Rooms: **H** (hall, start), **R1**, **R2**, **R3** (one dossier each: A, B, C; "held" = self switch A on the dossier
event), **X** (exit). Doors: d1 H–R1 · d2 H–R2 · d3 R2–R3 · d4 R3–X · d5 R1–R3.
- **Start open:** d1, d3, d5.
- **Taking (or returning) a dossier toggles two doors:** **A** (R1): d1, d5 · **B** (R2): d1, d2 · **C** (R3): d4, d5.
- **Goal:** reach X holding all three.
- **Verified (BFS): 12 actions.**

| # | Action | Doors open afterwards |
|---|---|---|
| 1–3 | d1 → R1, d5 → R3, d3 → R2 | d1, d3, d5 |
| 4 | **take B** | d2, d3, d5 |
| 5–6 | d3 → R3, d5 → R1 | |
| 7 | **take A** | d1, d2, d3 |
| 8–10 | d1 → H, d2 → R2, d3 → R3 | |
| 11 | **take C** | d1–d5 |
| 12 | d4 → X | |

- **The trap that teaches:** taking A first seals R1 (no open door). Nyx: "Caught with your hand in the drawer. Put it
  back, or stay." Returning it re-toggles the doors.
- Each dossier's text is a real secret (guard rotas, the Sump Barons' tithe, and one about *you*), so the information
  is the reward.
- **Hints (informant "Crow"):** 1 "Every secret changes who can walk where. Read before you take." 2 "Take the one
  that opens the way you came in." 3 the table.

### 433 Warden Arena (21×17)
Nyx, **double battle** ("two shadows"). Badge 16 + TM79 Dark Pulse.

### 434 The Ledger — MASTERY (optional; 17×13)
- A two-guard stealth room (lanterns only) leading to Nyx's ledger. At the ledger you choose which of the three
  dossiers to **sell back** to her: the price is one dossier.
- Each choice opens a different strongbox (one TM-rich, one seed-rich, one lore: the Gilded Chain bill of sale, which
  reveals her sale to Voss). Recorded as a Core choice key (narrative team: `:g16_ledger`, proposal).
- **Reward (any box):** Magical Seed ×2 (on New Moon: +1 accuracy and Focus Energy) + Black Glasses, plus the box's extra.

**Gym 16 trainers (6):** Burglar ×2 (guards), Gambler, Rocker, Hollow Defector *(HOLLOW)*, Informant *(Lady)*. Lv 71–74.

---
## Gym 17 — Gloaming, the Storybook Gym · Celestine Aubade (Fairy, `:FAIRY_TALE`, cap 80) · ★★★★★★★★★★

**Core rule: she cannot lie, but she can phrase.** Everyone in the storybook is truth-bound (Gloaming's oath). Every
statement is literally true, and the puzzles are about what the statements *don't* say: knights-and-knaves logic with
true-but-misleading phrasing.
- **Teach:** one door and one truthful sign.
- **Twist:** the Red Path. True signs mislead you off the path, and off the path is the wolf.
- **Combine:** the Midnight Ballroom. A 40-step clock, dancers on fixed loops, and truthful guests who each know one
  thing.
- **Gauntlet:** the Eight Princesses (the Eeveelution gauntlet), whose statements together locate the last key.
- **Mastery:** the Ninth Door.

**Warden link:** "I cannot lie. I can, however, *phrase*." The keeper of the Hymn has made true-but-misleading speech an
art. **Field:** Fairy Tale (Dragon moves wake the Dragon's Den). **Kingdom:** Elowen's twilight heart.

### State
| ID | Name | Use |
|---|---|---|
| V385 | `G17_CLOCK` | ballroom steps used (0–40) |
| S385 / S386 | `G17_PATH_DONE / G17_BALL_DONE` | |
| S387 | `G17_PRINCESSES` | all eight beaten (also S177 EEVEE_OCTAVE story flag) |
| S388 | `G17_NINTH_DONE` | |
Princess defeats use their trainer self switches.

### 450 Prologue Page — TEACH (21×17)
Two doors. The sign says: "*At least one of these doors leads on.*" The left door's plaque: "*The right door leads on.*"
- If the left plaque were false, both doors would be dead ends. That breaks the sign, and nothing here can lie.
- So the left plaque is true: the right door leads on. A wrong door opens onto a painted wall (harmless).

### 451 The Red Path — TWIST (29×25)
- A forest page with a red path. Stepping off it summons the wolf (a trainer battle once, then a reset to the page start).
- Three forks, each with a truthful signpost:
  - **Fork 1:** "*The left way is shorter.*" (true, but it ends at the wolf's den).
  - **Fork 2:** "*Grandmother lives at the end of a path.*" (true, but it doesn't say *this* path).
  - **Fork 3:** "*Not every red stone is the path.*" Three red stones; the path continues through the one that is *not*
    painted.
- **Solution:** right, right, the unpainted stone.
- Celestine's narration on each reset: "And the child thought: *but it was true!* And so it was."

### 452 Midnight Ballroom — COMBINE (29×25)
- The stair must be reached in ≤ 40 steps (V385; the clock strikes at 40 → "The spell breaks!" and you are back at the
  door). On Casual: 60.
- Six dancers on fixed loops: step-driven, and touching one costs 3 steps.
- Three truthful guests, each saying one thing:
  - "*The stair that isn't gold is behind a pillar.*"
  - "*I've never seen anyone leave by the silver stair.*" (true: nobody has, but it works)
  - "*The east stair is gold.*"
- Two stairs (gold east, silver west) and only the silver one leads on.
- **Intended route:** 32 steps through the dancers' gaps, west to the silver stair.
- Builder: verify with the step BFS (dancers deterministic).

### 453 The Eight Princesses — GAUNTLET (29×25)
Eight alcoves, each guarded by a princess trainer with one Eeveelution ace (the Rejuvenation trope; S177). Beat them in
any order. Each loser gives one true statement about where the **Sylveon key** is hidden among the eight alcoves.
- Together the statements locate it uniquely, but only after all eight.
- The tricky one is Umbreon's: "*It's not in an alcove I'd ever enter.*" She is afraid of light, so it's in a lit
  alcove.
- Walking to the right alcove opens the stair. Statements are listed in the event text; the unique answer is the
  Glaceon alcove (cold, lit, east).

### 454 Warden Arena (21×17)
Celestine, single battle (multi-bar boss on Hard). Badge 17 + TM21 Dazzling Gleam.

### 455 The Ninth Door — MASTERY (optional; 17×13)
- Three doors and three storybook guards: the Knight (always true), the Courtier (true but always *phrases* — never
  answers yes/no directly), and the Mirror (repeats the last true thing said).
- You may ask one question from a list. The only question that resolves it is to ask the Courtier "*Which door would
  the Knight tell me is the right one?*" The Courtier must answer with a phrasing that names a door: true.
- **Reward:** Magical Seed ×2 (on Fairy Tale: +1 Sp. Atk, +1 Sp. Def) + Fairy Feather + a page of the Hymn of Return in
  Celestine's hand.

**Gym 17 trainers:** 8 princesses + Lady + Beauty. Lv 76–79.

---
## Gym 18 — Wyrmrest, the Weighing Hall · Sigrun Ashfall (Dragon, `:DRAGONS_DEN`, cap 85) · ★★★★★★★★★★

**Core rule: nothing passes unweighed.** Dragons weigh what passes their gate. **Scales** lower bridges when balanced.
**Statues** turn on chains, and each chain drags its two neighbours (Gym 1's threads, grown up). The **magma tide**
rises and falls every 10 steps (`pfp_step_hook`), and crust paths exist only at low tide.
- **Teach:** one scale.
- **Twist:** the statue ring.
- **Combine:** hoard weights pushed across tide crust onto two scales.
- **Mastery:** the Weighing of the Heir, which uses all three.
- The gym also **recalls** the journey: chains (Gym 1), tide (Gym 3), Strength (Gym 8), Rock Climb and Waterfall
  (Gyms 10/11).

**Warden link:** "Wyrmrest is the last gate. Dragons don't let anything through they haven't weighed." Sigrun refuses the
badge until you say aloud what you intend (story). The final scale weighs *you*. **Field:** Dragon's Den (Wyrmfire stage
2). **Kingdom:** Ashkaar's holiest roost.

### State
| ID | Name | Use |
|---|---|---|
| V390 | `G18_TIDE` | 0 low · 1 high (toggled every 10 steps) |
| V391 / V392 | `G18_PAN_A / G18_PAN_B` | weight on each scale |
| S390 / S391 / S392 | `G18_RING / G18_SCALES / G18_HEIR` | rooms done |
Statues are one-hot `pfp_state` (4 facings: 0 N, 1 E, 2 S, 3 W). Hoard piles use `pfp_save`.

### 470 Gate — TEACH (21×17)
One scale needing 5 and two hoard piles (2 and 3). Push both onto the pan and the bridge lowers. A dragon-tamer: "The
roost counts. It always counts."

### 471 Wyrm's Spine — RECALL (29×25)
- A climbing gauntlet: Rock Smash, Strength (one Sokoban push), Rock Climb, Waterfall.
- The magma tide toggles every 10 steps; crust paths (`[V390≥1]` = magma, impassable) are open only at low tide.
- Teach the tide here with a counter brazier (it flares at 7, 8, 9).
- Two dragon-tamer battles mid-climb.

### 472 Statue Court — TWIST "the chained ring" (29×25)
- Five dragon statues around the altar. Chains (visible) link **S1–S2–S3–S4–S5–S1**.
- Turning a statue (action, 90° clockwise) also turns its two chained neighbours 90° clockwise.
- **Goal:** each faces the altar.
  - Positions: S1 north (faces S = 2), S2 east (faces W = 3), S3 south-east (faces N = 0), S4 west (faces E = 1), S5
    south-west (faces N = 0).
  - The chains cross the court, so ring order ≠ compass order, deliberately; follow the chains.
- **Start: S1–S5 = E, W, N, S, E (1, 3, 0, 2, 1). Target: 2, 3, 0, 1, 0.**
- **Verified (exhaustive, mod 4): unique solution, 9 turns:** S1 ×2, S3 ×2, S4 ×2, S5 ×3.
- **Hints (tamer "Ingrid"):** 1 "Follow the chains, not the compass." 2 "S2 needs no turn of its own." 3 the counts.

### 473 Hoard Scales — COMBINE (29×25)
- Two scales: **A needs 9**, **B needs 10**. Five hoard piles: **1, 2, 3, 5, 8** (Strength), total 19.
- Tide crust: piles can cross the magma channel only at low tide, and a push onto a crust tile when the tide turns
  sinks the pile. Sunk piles return to the hoard (fair reset). The 8-pile is slow (it moves 1 tile per 2 pushes).
- **Valid partitions (exhaustive):** A {1,8} + B {2,3,5}, or A {1,3,5} + B {2,8}.
- The geometry makes the 8 reachable only to B's side (it can't make the tide window to A), so **A {1,3,5}, B {2,8}**.
- **Intended:** push 2 and 8 to B during two low tides (the 8 needs both windows). Ferry 1, 3 and 5 to A across the
  short crust.

### 474 Warden Arena (21×17)
Sigrun, single battle on `:DRAGONS_DEN`. Before the badge, she asks you to say what you intend (story, S153). Badge 18 +
TM59 Dragon Pulse.

### 475 The Weighing of the Heir — MASTERY (optional; 21×17)
- One great scale, a three-statue chain ring, and the tide.
- The pan needs **your weight plus 3**. You stand on it yourself (the scale reads the player as 5), so you push the
  3-pile on and then step on.
- The statues must face the pan, and the chain ring can only be turned from tiles that are crust at low tide. Plan all
  three within one tide window.
- **Reward:** Elemental Seed ×2 (on Dragon's Den: +1 Atk, +1 Speed and Flash Fire) + Dragon Fang. Sigrun: "It weighed
  you and let you pass. It never let me."

**Gym 18 trainers (6):** Dragon Tamer-style Cool Trainer ♂/♀ ×4, Ace Trainer ×2. Lv 81–84.

---
## 4. What the map builder must add to the toolchain

1. **`mapgen/ruby/007_Puzzles.rb`** (runtime, copied to `Plugins/Prismfall Maps/`): every helper in §3. The big ones:
   - **one-hot state** (`pfp_state`);
   - **position save/restore + Restorer** (`pfp_save` / `pfp_restore!`);
   - **twin-map swap** with landing fix-ups (`pfp_swap_map`);
   - **forced-line movement** for belts, wind, currents and ice blocks (`pfp_push_line`);
   - **beam tracer** (`pfp_beam`) and **power tracer** (`pfp_power`);
   - **step hooks** (`pfp_step_hook`: tick clocks, filter budgets, tide, pursuers, mirror and echo walkers);
   - **checkers** (`pfp_check`) with per-reason failure text;
   - **apprentice** support (`pfp_hint`, `pfp_skip?`).
2. **Builder macros in the generator scripts** (like `plank_events` in `gen_gym1.py`):
   - multi-page exact-value events;
   - lettered state-maze tiles (Gym 2's `s/f/t/S/F/T`);
   - visit-once tiles;
   - lane/belt/wind tiles with a direction source;
   - press and hazard events on a tick;
   - pushable crates and ice blocks;
   - pursuer, mirror and echo events;
   - the apprentice NPC (menu + reset script).
3. **Followers:** a DSL hook for `Followers.add/remove` (the Gym 4 drone). Auto-remove followers on map exit.
4. **Pushable physics:**
   - `pbPushThisEvent` (crates) and `pbPushThisBoulder` (Strength);
   - **sliding blocks** (push → slide until stopped);
   - **2-tile objects** (pews) moved as one;
   - "drop into hole → plug" (Gym 10).
5. **Rotating tiles:** one-hot rotation events with charsets whose 4 rows are the 4 rotations (conduits, mirrors,
   statues, vanes). **Turntable ride** for Gym 2 153 (the player is moved with the floor).
6. **Light beams and power:** `Beam x,y` / `Strip x,y` overlay events generated on every cell a beam or strip can occupy,
   lit by the tracers.
7. **Conveyors, currents, wind:** forced movement with stacking (objects stop against objects) and a tick order.
8. **Twin maps:** spec support for "variant of map N" (shared walls, per-variant events), as Gym 3 already does by
   hand. Used by Gyms 3, 5, 10, 14 and several dungeons.
9. **Art the puzzles need** (Art Director): silk heddles and spools, stage flats (ship/forest/throne), rope rails,
   gangplank/log/dais, rafts and a lock gate, conduit pieces (I/L/T in 4 rotations) and lit strips, sun-mirrors and
   crust/soft sand, flasks and funnels, crucibles/molten/iron channels and moulds, rope lines, garden plots (4 stages),
   cracked/broken/plugged ice, gust lanes and vanes, mirror panes, beam segments in 5 colours (each colour also has a
   *pattern*, for colour-blind players), pews and an echo sprite, belts/presses/crane, lanterns and guards' sight-cone
   decals, storybook flats, hoard piles and scales.
10. **Verification:** a `mapgen/puzzles/` package of small Python state models (the ones used for this spec: heddles,
    spools, stage maze, raft drift, conduits, falls, rings, ice slides, mirror walker, vanes, beams, vault). The builder
    runs them in `build.py` and fails the build if a room's start state can't reach its goal or can reach a dead end
    without an apprentice.
11. **Registry:** extend `flags.yaml` with §1's blocks and raise the installer's switch/variable maximum to 600.
12. **Password:** Core gains `puzzleskip` (`:PUZZLE_SKIP`, writes S301). It's owned by the Systems team; this is the
    request.

## 5. Verification log (what was proven while writing this spec)
Exhaustive search or BFS in Python state models (scratch copies in `/tmp/pstudy/solve/`; the builder ports them):
- Gym 1 131 (3 pulls; start state no longer a solution), 132 (8 actions; unsolvable without the brass wire), 134
  (unique 3 treadles).
- Gym 2 151+152 (Script order forced; unsolvable without the loft), 153 (3 cranks).
- Gym 3 basins (16 actions), with the gate also blocking the Low trench.
- Gym 4 191 (door 4 / side 2 / alarm on the naive route), 950 (11 clicks).
- Gym 5 (drop required; flood-fill of the five Under-Dig galleries).
- Gym 9 291 (2 vs 5 waterings), 292 (7 vs 8), 297 (6).
- Gym 10 311 (17), 312 (16, pushing required), 315 (33).
- Gym 11 331 (14).
- Gym 12 351 (26).
- Gym 13 371 (3 turns; alarm and side configurations).
- Gym 16 432 (12).
- Gym 18 472 (unique, 9 turns); 473 partitions.
**Builder must still verify** (rules fixed here, exact boards to finalise with the solver): Gym 7 (hand-proved; small),
Gym 8 271–275 (pursuers), Gym 11 332, Gym 12 352, Gym 13 372, Gym 14 391–393, Gym 15 411–414, Gym 16 431, Gym 17 452,
Gym 18 473/475 geometry.
