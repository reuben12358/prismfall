# GYM PUZZLES — all 18 Wardens (Revision 10 rewrite)

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

| # | Warden · field | Core rule | Teach → Twist → Combine → Mastery | ★ |
|---|---|---|---|---|
| 1 | Tamsin · Silkwood | **Follow the thread**: each heddle moves what its silk ties to, and every pattern repeats in 3 pulls | one heddle → coupled heddles → spools + a brass Meridian wire that also moves a bridge → Granny's Knot | 1 |
| 2 | Dorian · Grand Stage | **The stage moves, the marks don't**: cues swap scenery, ropes only work from marks | one cue → three scenes in Script order → loft flats that leave the stage hang in the loft → ride the revolve | 2 |
| 3 | Marisol · Water Surface | **Water lifts what floats, the current carries what's loose** | practice lock → three water levels × a drifting raft × the tide bell × a lock gate → snag culvert | 3 |
| 4 | Rook · Neon Grid | **Route the power, never the alarm** | rotate conduits → tees and an alarm lamp → Rotom drone as a portable wire + latching relays → the empty Plate socket | 4 |
| 5 | Sahar · Desert | **Sun hardens, shade sinks**: falling is a way across | one drop → sun-mirrors decide which lanes are crust and which sink → a two-floor loop where drops are transport → mural rubbing | 5 |
| 6 | Corvin · Corrosive Mire | **Dose makes the cure**: exact measures with unmarked flasks | one flask → 3+5 make 4 → doses carried across a filter-step budget → the Quiet Ward (4+9) | 5 |
| 7 | Brann · Volcanic | **Pour, then quench**: empty → molten → iron | one mould → spout aims and limited quench → cross-floor drains with a rail cart → "forge to break right" | 6 |
| 8 | Kaito · Colosseum | **Every step you take, they take**: pursuers vs Strength boulders | one sparring Machop → two pursuers and rope lines → boulders, plates and pursuers → the Marrowgate door | 6 |
| 9 | Juno · Flower Garden | **Water spreads**: each plot grows itself and its neighbours, and the leftover overgrowth becomes the arena's field stage | one plot → a ring of six → sun lamps and pruning → the Bride Bower bloom | 7 |
| 10 | Anja · Frozen Lake | **Ice remembers weight**: slides, cracks and the under-ice | slide → cracked ice drops you to the under-ice → ice blocks plug holes and refreeze → the Sounding | 7 |
| 11 | Odessa · Stormfront | **The wind doesn't care**: vanes steer fans that push you and the mail | one fan → coupled vanes → updraft floors + lightning cycles → Dead-Letter Archive | 8 |
| 12 | Ilsa · Mindscape | **Your reflection keeps you honest**: a mirrored self walks your steps | mirrored walk → swap pads → thoughts only the reflection may stand on → the Quiet Room | 8 |
| 13 | Bastian · Crystal Cavern | **Light remembers its colour**: beams, prisms and colour gates | one mirror → filters and splitters → boulders as beam blocks + the prism-glow cycle → Bastian's long story | 9 |
| 14 | Ysolde · Hollow Cathedral | **The dead walk where you walked**: twin naves and Morwen's echo | living ⇄ dead bell → pews persist across worlds → the echo replays your path → Morwen's letter | 9 |
| 15 | Magnus · Factory | **Tolerances**: belts, presses and crates on one clock | belts → reversing lever groups → crane-placed crates jam presses → the Tolerance Lab | 10 |
| 16 | Nyx · New Moon | **Information is the key**: guards, lanterns and secrets that change the doors | sight lines → lanterns turn guards → each stolen secret re-routes the vault → the Ledger | 10 |
| 17 | Celestine · Fairy Tale | **She cannot lie, but she can phrase**: truth-bound storybook rules | the Red Path's rule → true-but-misleading guards → the Midnight clock × the dancers → the Eight Princesses | 10 |
| 18 | Sigrun · Dragon's Den | **Nothing passes unweighed**: scales, statues and the magma tide | one scale → the coupled statue ring → hoard weights on magma-floated pans → say it aloud | 10 |

---
## 3. Runtime helpers the specs call (`mapgen/ruby/007_Puzzles.rb`, contract)

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
## Gym 1 — Briarwick, the Loomhouse · Tamsin Loom (Bug, `:SILKWOOD`, cap 15) · ★

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
| V305 / V306 / V307 | `G1_HEDDLE_A/B/C` | 0–2 (plank column of gaps A, B, C) | 131 |
| V308 | `G1_FOYER_HEDDLE` | 0–2 | 130 |
| V309 | `G1_LOFT_BRIDGE` | 0 none · 1 P5→P6 · 2 P4→P6 | 132 |
| S305 | `G1_CORD_ALPHA` | spool s1 destination | 132 |
| S306 | `G1_CORD_BRASS` | spools s3/s4 destination (the brass wire also cycles V309) | 132 |
| S307 | `G1_CORD_GAMMA` | spools s2/s5 destination | 132 |
| S308 | `G1_KNOT_DONE` | Granny's Knot solved | 134 |
| S309 | spare | | |

Tiles: `PLANK` = 3807 (passable cross-board, used today). Hanging threads use the `custom` strand tiles (`CU['strand_*']`).

### 130 Foyer — TEACH "the first thread" (15×13, palette `loom`)
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

### 131 Weaving Hall — TWIST "two threads per heddle" (25×21)
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

### 132 Canopy Lofts — COMBINE "spools, cords and the brass wire" (25×25)
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

### 133 The Spindle — arena (15×15, unchanged)
Tamsin, single battle, `:SILKWOOD`. Badge 1, TM89 U-turn, then the existing confession scene (`:ch2_tamsin`). New
line if S308 is on: "You finished Gran's row. ...She'd have shouted. Happily. Sorry — I'm crying, that's the Silkwood,
it's very dusty."

### 134 Granny's Knot — MASTERY (optional, 13×9, new; door D on P5)
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

**Gym 1 trainers (5):** Bug Catcher Nell (11–12), Lass Orla (12–13), Gentleman "Weaver Bram" (13), Bug Catcher Hollis
(12–13), Pokémon Ranger ♂ Ash (13–14). Nell and Bram are optional.

---
## Gym 2 — Saltmere, Pell Playhouse · Dorian Pell (Normal, `:GRAND_STAGE`, cap 19) · ★★

**Core rule: the stage moves, the marks don't.** A cue rope changes the whole set: flats appear, bridges vanish. You can
only call a cue from a painted **mark**, because every rope post is boxed in so that the only tile beside it is a mark.
**Twist:** cues set *specific* scenes, and the geometry forces them in Script order. **Combine:** in the Fly Loft, a flat
flown *out* of the stage hangs *in* the loft. The two rooms share one set of scenery, and the counterweight ropes are
coupled. **Mastery:** ride the revolve (a turntable under the stage).
**Warden link:** "The stage tells the truth the throne won't." The only route through the stage performs *The Gilded King*
in order (Ship → Forest → Throne): Dorian's banned play, staged by the player. **Field link:** Grand Stage. Actors are
dancers and singers (Sound and Dance moves). **Kingdom:** Saltmere, Elowen's free port, where "nothing is a miracle, so
we built our own".

### State
| ID | Name | Values |
|---|---|---|
| V310 | `G2_SCENE` | 0 work lights · 1 Shipwreck · 2 Forest · 3 Throne |
| V311 | spare | |
| V312 | `G2_TURNTABLE` | 0–3 (153) |
| V313 | `G2_OVERTURE` | 0/1 (150) |
| S310 / S311 / S312 | `G2_FLAT_A/B/C_FLOWN` | ON = the flat hangs in the loft (off the stage) |
| S313 | spare | |
| S314 | `G2_TRAP_DONE` | 153 chest |

### 150 Foyer — TEACH "hit your mark" (19×13)
```
     0123456789012345678
y0   #########E#########    E (9,0) auditorium doors → 151 (12,16)
y1   #.......hhh.......#    h = Overture curtain-flat (wall while V313 = 0)
y2   #...#.............#
y3   #..x1#......u.....#    rope "Cue: Overture" (4,3), boxed by (4,2) (5,3) (4,4) · x mark (3,3) · u usher (12,3)
y4   #...#.............#
y5   #.................#
y6   #..S..........A...#    S the Script sign (3,6) · A apprentice "Stagehand Wren" (14,6)
...
y12  #########@#########    @ (9,12), link from Saltmere 147
```
- `Curtain h` (8–10, 1): P0 [—] tile CURTAIN (impassable) · P1 [V313≥1] blank.
- The rope (action, usable only from (3,3)): V313 = 1 − V313. "*Cue: Overture!* The curtain flies out."
- Usher: "On this stage, darling, the scenery moves and the marks don't. Call a cue from anywhere but your mark and
  you'll be wearing a forest." Script sign: *"Act I, the Shipwreck. Act II, the Forest. Act III, the Throne. Places,
  understudy."*

### 151 Revolving Stage — TWIST "three scenes, in order" (25×18)
```
     0123456789012345678901234
y0   ############E############    E (12,0) upstage door → 154 (10,13)
y1   #...s....###T###..#.....#    T (12,1) dais steps (passable only in Throne)
y2   #.L.s....#.....#.#3#..K.#    L (2,2) ladder → 152 left · K (22,2) ladder → 152 right · rope 3 (18,2)
y3   #...s....#AAAAA#..x.....#    A = flat A (wall while IN)
y4   #ssss....#.....#.....ttt#
y5   #....ffff#vvCvv#........#    C (12,5) = rostrum over the stage trap (walkable only while IN)
y6   #........#.....#fffff...#
y7   #......#.#.....#....f...#
y8   #.....x2##.....B....f...#    rope 2 (7,8) with mark (6,8) · B (15,8) = flat B (wall while IN)
y9   #......#.#.....#ttttf...#
y10  #fff.ffff#.....#....f...#
y11  #........#.....#....f...#
y12  #vvvSvvvvvvvFvvvvvvvTvvv#    orchestra pit: S (4) gangplank · F (12) log · T (20) dais steps
y13  #vvvSvvvvvvvFvvvvvvvTvvv#
y14  #.......................#    house
y15  ##x.....................#    mark (2,15)
y16  ##1#........@.....A.....#    rope 1 (2,16) · @ (12,16) · A apprentice "Stage manager Pip" (18,16)
y17  #########################
```
Legend: `s` Shipwreck flat (wall only in scene 1) · `f` Forest flat (wall only in 2) · `t` Throne flat (wall only in 3)
· `S/F/T` passable **only** in scene 1/2/3 (void or wall below) · `A/B` loft flats (wall while IN) · `C` rostrum
(floor while IN, void below).

| Event family | Pages |
|---|---|
| `s x,y` | P0 [—] blank · P1 [V310≥1] tile FLAT_SHIP · P2 [V310≥2] blank |
| `f x,y` | P0 blank · P1 [V310≥2] tile FLAT_FOREST · P2 [V310≥3] blank |
| `t x,y` | P0 blank · P1 [V310≥3] tile FLAT_THRONE |
| `S x,y` | P0 blank (pit void) · P1 [V310≥1] tile GANGPLANK · P2 [V310≥2] blank |
| `F x,y` | P0 blank · P1 [V310≥2] tile LOG_BRIDGE · P2 [V310≥3] blank |
| `T x,y` | P0 blank · P1 [V310≥3] tile DAIS_STEPS |
| `A x,3` | P0 [—] tile FLAT_A · P1 [S310 on] blank |
| `B 15,8` | P0 [—] tile FLAT_B · P1 [S311 on] blank |
| `C 12,5` | P0 [—] tile ROSTRUM (passable) · P1 [S312 on] blank |
| `Rope 1` (2,16), `Rope 2` (7,8), `Rope 3` (18,2) | action → if V310 == n: "The stage is already set." else V310 = n, screen shake (2, 8), SE "Earth1", text "*Cue: <scene>!* The revolve groans round." First time: the scene's actor enters |
| `L` / `K` | touch warps to 152 (2,2) / (22,2) |
| Actors | Juggler "Ferdie" [V310≥1] at (2,6), sight 3 · Beauty "Rosalind" [V310≥2] at (2,9) · Gentleman "Crewe" [V310≥3] at (21,6) |

**Solution (verified, BFS):**
1. From mark (2,15), cue **Shipwreck**. Cross gangplank S into stage-left.
2. Walk to mark (6,8) and cue **Forest**. The ship flats boxing in the ladder vanish, and the forest flats cut you off
   from the pit.
3. Climb L into the loft, walk the catwalk to the right rail, and set the flats (see 152): **pull rope 2, then rope 3**.
4. Climb down K. From mark (18,3), cue **Throne**. The forest flats vanish.
5. Walk through B (flown) → centre → onto the rostrum C (still in) → through A (flown) → up the dais T → door E.

Without the loft it is unsolvable (BFS), and it is unsolvable without Ship or without Forest.
**Why it reads well:** the Script order is never enforced by a rule; the stage *makes* it the only route.
**Hints (Pip):** 1 "Script order, love. The stage won't let you skip an act." 2 "The Throne cue's on the far side. Seen
the stage from above yet?" 3 the solution.
**Reset:** Pip → V310 = 0, S310–312 off, player to (12,15). Leaving the room keeps everything.

### 152 Fly Loft — COMBINE "a flat is in one place at a time" (25×15; rows 6–14 void: the stage seen from above)
```
     0123456789012345678901234
y0   #########################
y1   #.....a....b....c.......#    a / b / c: where flats A / B / C hang while FLOWN (they block the catwalk)
y2   #.L...a.i..b..p.c.....K.#    L (2,2) ↔ 151 L · K (22,2) ↔ 151 K · p (14,2) trapdoor → 153 · i (8,2) Super Potion
y3   #.....a....b....c.......#
y4   #.123.a....b....c...123.#    left rail: ropes 1-3 at (2..4,4) · right rail: ropes 1-3 at (20..22,4)
y5   #########################
```
- **Counterweight coupling:** rope 1 → A · rope 2 → B + C · rope 3 → A + C. Each rope pulls its flats out if they're in,
  and back in if they're out. The ropes on the two rails are the same three ropes.
- `a x,1-4`: P0 [—] blank · P1 [S310 on] tile HANGING_FLAT (impassable). Same for `b` [S311] and `c` [S312].
- **What the stage needs:** A out, B out, C in. Pulls: **rope 2** (B out, C out) then **rope 3** (A out, C back in). The
  natural try, rope 1 then rope 2, leaves C out, and the rostrum is gone.
- **The aha:** once flats are flown, they hang across the catwalk *behind you*. Set them at the **right** rail.
  Players who set them at the left rail find the loft blocked and must reset. The trapdoor p is reachable only while
  b or c is in.
- **Hints (stagehand "Dot", at (5,2)):** 1 "Whatever leaves the stage comes up here. Where do you want to be standing
  when it does?" 2 "Rope 2 drags two flats. Rope 3 also catches the rostrum." 3 the solution.

### 153 The Trap Room — MASTERY "ride the revolve" (optional; 11×11 puzzle, padded to 20×15; via trapdoor p)
Turntable 5×5 at (3–7, 3–7), crank post at its centre (5,5). Shown at rotation 0:
```
     01234567890
y0   ###########
y1   ########*##    * (8,1) prop chest
y2   #######..##
y3   ##...#...##
y4   ##..##...##
y5   ##.#.o...##    o crank (5,5)
y6   ##.#.##..##
y7   ##.#..#..##
y8   ####...####
y9   ####...####
y10  #####@#####    @ (5,10) ladder up to 152 p
```
- Turntable cells are 24 events, each with 4 pages (`[—]` rot 0, `[V312≥1]` rot 1, `[V312≥2]`, `[V312≥3]`). A cell is
  machinery (impassable tile) or blank (floor) according to the 5×5 pattern `..#.. / .##.. / #.o.. / #.##. / #..#.`
  rotated clockwise by V312 quarter-turns.
- **Crank** (action, only from the four tiles beside it): `pfp_cycle(312, 4)`, and **the player rides**: their offset from
  the centre (dx, dy) becomes (−dy, dx) (`pfp_turntable_ride(5,5)`). "You lean on the crank. The whole floor — and you
  with it — swings a quarter-turn."
- **Solution (verified, BFS):** walk to (4,5) and crank three times. You ride from west to north to east to south.
  Then walk east (6,6) → (7,6) → (8,6) and north up the right-hand corridor to the chest.
- **Reward:** Magical Seed ×2 (on Grand Stage: +1 Speed and Laser Focus), PP Up, and the prop crown of the Gilded King
  (flavour; Dorian comments in 154).
- **Reset:** the apprentice "Old Joss" (by the ladder) → V312 = 0.

### 154 The Grand Stage — arena (21×15)
Dorian, **double battle** (curtain call). Badge 2 + TM42 Facade. If S314 is on: "You found the old crown! Keep it. Every
understudy should own one thing that doesn't fit."

**Gym 2 trainers (6):** three actors (above, 15–17), Juggler ×1 on 152's catwalk (17–18; at (18,3), never blocking a
rail), Lady ×1 in 150 (16–17), Beauty ×1 (18).

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

<!-- GYMS 4-18 FOLLOW -->
