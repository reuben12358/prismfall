# DUNGEON PUZZLES — early game first, then one signature dungeon per kingdom

Companion to `GYM_PUZZLES.md`. It reuses that file's §0 conventions (legend, page notation, apprentice, hints, skip), the
§3 `pfp_*` helpers and the §4 toolchain, and it follows the principles in `PUZZLE_STUDY.md` §3. Map IDs, sizes and fields
come from `maps.json` / WORLD.md. Dungeons are gentler than the gym of the same act, and none of them is required to
beat the game unless WORLD marks it mandatory (the Glassed Orchard, the Ossuary of Dunes).

**What dungeons do differently from gyms:**
- They are **hubs with shortcuts**: every solved piece opens a one-way shortcut back (Byxbysion principle).
- They have **one cross-map cause→effect** each (Pyrous principle).
- Their **rewards are items and lore**, not badges. Every optional room names its reward.
- **No apprentice NPC.** Resets are in-world instead: a lever, a bell, leaving the room, or a fall back to the room's
  start. Hints come from a local NPC, a sign or a companion's line.

## 0. State registry (IDs 501–600: Switches and Variables; see GYM_PUZZLES §1)
| Block | Dungeon (maps) | Act | Kingdom |
|---|---|---|---|
| 501–505 | D1 The Glassed Orchard (522) | I | Elowen |
| 506–510 | D2 Gossamer Wood + Deepwood (524, 525) | I | Elowen |
| 511–515 | D3 Cocoonfall Hollow (548) | I | Elowen |
| 516–520 | D4 Brinecut Mine (544, 545) | I | Elowen/Ossaria border |
| 521–525 | D5 Thistledown Manor (546, 547) | I | Elowen |
| 526–530 | D6 Gullcry Caves (564, 565) | I | Isenmar |
| 531–535 | D7 The Rimewood + Glade (562, 563) | I | Borderland A |
| 536–540 | D8 The Rehearsal (568), bonus | I | Elowen (Bleed) |
| (310–314) | D9 Pell Playhouse Backstage (151–153): uses the Playhouse block | I | Elowen |
| 541–545 | **Elowen** — Gossamer Heartwood (703) | III | Elowen |
| 546–550 | **Zenith** — Voltaic Sluiceworks (584, 585) | I (optional) | Borderland B / Zenith |
| 551–555 | **Ossaria** — Ossuary of Dunes (624, 625) | II | Ossaria |
| 556–560 | **Ashkaar** — The Cinderhorn (664, 665, 666) | II | Ashkaar |
| 561–565 | **Isenmar** — the Ice Vault under Whalebone Keep (308, + 318 new) | III | Isenmar |
| 566–570 | **Antumbra** — Mirror Mere + Giratina's Reverse Depths (742, 806) | III–IV | Antumbra |
| 571–575 | **Nadir** — Drowned Aurelia (824, 825, 826) | IV | Nadir |
| 576–600 | reserved (Static Tunnels, Miasma Caverns, Stormwatch Spire, Sovereign's Ascent…) | | |

## 0b. Difficulty curve (SPINE Revisions 13–14; same scale and machine check as GYM_PUZZLES §0b)
Dungeons sit **at or below** the gym that comes before them; optional ones may go up to two points higher. "Solve" = the
puzzle part only.

| Dungeon | Maps | When | Rating | Expected solve | Status |
|---|---|---|---|---|---|
| D1 The Glassed Orchard — chime rows | 522 | Ch1, before Gym 1 | **2** | 3 min | built (events over the Orchard), proven 3 moves / 4 states, engine-run |
| D2 Gossamer Wood + Deepwood — one-way silk, lantern cocoons | 524, 525 | Ch3: before / after Gym 2 | **2** | 5 min | proven (2 posts); map events not yet placed |
| D3 Cocoonfall Hollow — crystal-silk anchors | 548 | after Gym 2 | **2** | 5 min | proven; **design fix:** start with TWO bridges taut (a, b). The spec's start (one taut) let anchor 2 tighten all three in one pull, so the parity lesson never happened |
| D4 Brinecut Mine — points and brine | 544, 545 | Ch3 road (after Gym 1) | **3** | 10 min | spec |
| D5 Thistledown Manor — don't turn your back | 546, 547 | Ch3 road, cap 19 | **3** | 10 min | spec (runtime: `pfp_pursue(name, :creep)`) |
| D6 Gullcry Caves — the tide counts your steps | 564, 565 | Act I | **4** | 15 min | spec (runtime: `pfp_step_clock`) |
| D7 The Rimewood + Glade — frost loom, ice slide | 562, 563 | before Gym 3 | **3** | 10 min | spec; the Glade slide (9 slides) is optional 4/10 |
| D8 The Rehearsal — between the frames | 568 | bonus | **4** | 15 min | spec |
| D9 Pell Playhouse Backstage — the old revolve | 151–153 | after Gym 2 | **4** | 20 min | built, proven, engine-run (below) |
| Zenith — Voltaic Sluiceworks | 584, 585 | optional from Act I | **5** | 20 min | spec |
| Ossaria — Ossuary of Dunes | 624, 625 | Act II | **6** | 25 min | spec |
| Ashkaar — The Cinderhorn | 664–666 | Act II | **6** | 30 min | spec |
| Elowen — Gossamer Heartwood | 703 | Act III | **7** | 30 min | spec |
| Isenmar — the Ice Vault | 308, 318 | Act III | **8** | 35 min | spec |
| Antumbra — Mirror Mere / Reverse Depths | 742, 806 | Act III–IV | **9** | 40 min | spec |
| Nadir — Drowned Aurelia | 824–826 | Act IV | **9** | 40 min | spec |

---
# PART 1 — THE EARLY GAME (Act I)

## D1 The Glassed Orchard (522, 30×26, `:BLEED`, mandatory) — "the Bleed listens"
**Rule taught:** Bleed zones respond to you. Glass trees **chime** when you pass beside them, and the **Veil** stops
everyone but you. This is the Orchard's existing Veil scene (S105, GO-02), plus one gentle puzzle that every later Bleed
zone builds on.
- **The Chime Rows.** Three rows of glass apple trees. A wind-chime post at the gate (19,22) plays a three-note phrase
  (low, middle, high) when you examine it.
- Walking past a "loose" glass tree (a `touch` tile beside it, marked with a hairline crack) rings its note: tree L
  (6,8), tree M (14,12), tree H (22,6). Ring them in the phrase order and the glass hedge (24–26, 4) shatters. Behind it:
  the lost child's satchel (quest) and Bleed Shard #1.
- **State:** V501 `D1_CHIME` (0–3). Ringing the expected tree → +1; any other → V501 = 0 and a sour chord. The hedge
  page is `[V501≥3]` blank.
- **Teaching:** Juno, outside the Veil, hums the gate phrase back to you ("It's the bit before the chorus in Wingull
  Shanty!"). A wrong note costs nothing.
- **Why it matters later:** sound and order return in the Rehearsal (D8), the Ice Vault (Isenmar) and Gym 13's story
  code.

## D2 Gossamer Wood (524, 48×48) and the Deepwood (525, 36×36, Cut) — `:SILKWOOD`
**Rule: silk leans one way.** Silk curtains (the existing silk-wall events) are **one-way**. You can push through a
curtain only in the direction its threads lean (an arrow-shaped sag). From the other side it's a wall.
- **Teach (524 south loop).** One curtain across the trail at (24,38), leaning north. You pass north, and coming back
  you must take the side loop. A sign on Woodward's hut: "Silk only lets you go the way it's been pulled."
  Implementation: curtain event, `touch` from the south → `pfp_ride` 1 tile north (through); action from the north →
  "The silk holds fast."
- **Twist (524 north loops).** Five curtains between the two loops form a one-way maze. Its only route to the Briarwick
  edge (24,0) passes the Bug Catcher and Woodward's hut. The two side loops are shortcuts *back* south: the one-way silk
  makes them free return paths once you're north (shortcut principle).
- **Combine (525 Deepwood, after Tamsin's badge and Cut).** The pond hollow is dark (tone −60). Joltik nest on the silk lines.
  - Three **lantern cocoons** hang on threads.
  - Touching a thread's anchor post (action) sends a Joltik spark along it (Electroweb runs the threads, the field's own
    rule) and lights every cocoon on that thread. A lit cocoon makes its curtain lean the *other* way (the threads
    tighten).
  - Anchors: post α lights cocoons 1 and 2, post β lights 2 and 3.
  - The route to the Silver Powder island needs curtain 1 flipped and curtain 3 flipped: **α then β** (cocoon 2 flips
    twice, back to unflipped).
  - **State:** S506 / S507 / S508 = cocoons 1–3 lit.
- **Reward:** TM19 Giga Drain (WORLD §6; in the Deepwood's island hollow) + Silver Powder. Shelly's cameo sidequest
  ("Lost in the Gossamer") is stuck behind curtain 3. Freeing her is the reason most players come.

## D3 Cocoonfall Hollow (548, 32×28, `:BLEED`, optional) — "the shuttle re-threads"
**Rule:** Mother Loom's Shuttle (key item, from Tamsin after her badge, Gym 2) can **re-thread crystal silk**.
- Each of three **cocoon anchors** pulls its crystal threads taut or slack. A taut thread is a bridge; slack is void.
- The coupling is Gym 2's (the Weaving Hall), binary now: **anchor 1** toggles bridges a and b, **anchor 2** toggles b and c, **anchor 3**
  toggles a and c.
- **Layout:** the hamlet sits on a crater floor. Three bridges cross the glass ravine:
  - **a** to the TM81 cocoon-house (NE);
  - **b** to the Shard house (NW);
  - **c** to the Matriarch's nest (N centre).
  Anchors stand at the hamlet's south edge (8,22), (16,22), (24,22).
- **Start:** a and b taut, c slack (the design fix proved in `mapgen/puzzles/dungeons.py`; the first draft started with only
  a taut, and anchor 2 then tightened all three in one pull, so the parity lesson never happened).
- **The aha (parity):**
  - Every anchor flips *two* bridges, so the number of taut bridges stays even: two or none. You can never have all three.
  - The two houses are open on arrival: visit them first (a to the TM81 cocoon-house, b to the Shard house).
  - The nest (c) needs **c taut**, and every pull that tightens c slackens a or b: anchor 2 (b slack, c taut) or anchor 3
    (a slack, c taut). Opening the nest always costs a house, so the order matters: houses first, then the nest.
- Juno (outside the Veil): "Granny Loom always said three threads can't all be tight at once. I thought she meant
  feelings."
- **State:** S511 / S512 / S513 = bridges a/b/c taut.
- Boss: the Glass Matriarch (existing; S107). After the boss, the nest's crystal thread snaps all three bridges taut
  (shortcut home).

## D4 Brinecut Mine (544 1F 40×34, 545 B1F 34×30, `:CAVE`) — "points and brine"
**Rule:** a minecart runs where the points send it.
- **1F (TEACH → TWIST).**
  - The tracks fork three times. **Points levers** P1–P3 (S516–S518) each send the cart left or right.
  - The cart (action at the depot (6,22): "Ride the cart?") follows a precomputed move route per lever combination (8
    combinations, 4 distinct ends):
    - **A** dead end with Hard Stone;
    - **B** the ladder to B1F;
    - **C** the Thistledown Lea mouth (39,4);
    - **D** buffer stop: "BUMP." The cart rolls you back to the depot.
  - **Teach:** the first fork is visible from the depot; P1 alone decides A vs the rest.
  - **Twist:** P2 and P3 are behind the cart's path. You must ride to A, walk back past P2 (on foot through a crawlway),
    set it, then ride again.
  - The salt miner hands TM98 over once you hold Dorian's badge (Gym 1); Rock Smash is usable from Badge 2.
- **B1F (COMBINE, cross-map).** The salt lake (8–19, 12–19) is brine. A **pump wheel** on B1F lowers it only while the
  1F **cart is parked at end B** (it weighs down the pump lever; S519). The lake then drains to a salt flat, and the path
  to the Old Amber (30,26) appears.
  - You have to plan the cart's last ride: leave it at B, climb down, pump.
  - V516 = the lake level (0 full, 1 drained).
  - The Nugget (hidden) is on the drained flat.
- **Reward:** Old Amber (the first fossil) + Nugget.

## D5 Thistledown Manor (546 30×24, 547 attic 12×9) — "don't turn your back"
**Rule:** the furniture moves when you don't look at it. Three possessed armchairs (events) step one tile toward you
whenever you take a step **while facing away from them** (a step hook: compare each chair's direction to you).
Watched, they freeze. A chair that reaches you starts a ghost battle (Channeler) and every chair returns to its place.
- **"In view"** means the chair is not in the half-plane behind you. You face the way you walk, so stepping toward a
  chair or sideways past it keeps it in view; stepping away from it lets it creep.
- **TEACH (foyer):** one chair between you and the stairs. Walk toward it, then sidestep round it. Never walk *away*
  from it.
- **TWIST (portrait hall):**
  - Two chairs and the existing **portrait-order** puzzle: four portraits, with the order from the diary pages.
  - Each portrait you set turns you to face the wall, so the chairs creep.
  - Plan the order of portrait visits so each chair stays in view.
- **COMBINE (dining room):**
  - Two trapdoors (wine cellar, harmless).
  - Lead a chair onto a trapdoor by letting it creep while you stand beyond it. It falls through and is gone. The
    other chair you lure onto the second trapdoor; then the attic stair is clear.
  - Uses the creep rule against them.
- The existing **three ghost scenes** (role lines; wrong line → ghost battle) stay as written. The manor's matriarch
  offers GO-03 or the Spell Tag + Litwick (S176).
- **State:** S521 / S522 = trapdoors used. Chair positions reset on leaving the room.
- **Reward:** Cleanse Tag (existing), Spell Tag, Litwick; Greavard in the attic (existing).

## D6 Gullcry Caves (564 1F 40×40, 565 B1F 32×30, `:CAVE`) — "the tide counts your steps"
**Rule:** the sea breathes in and out. The tide toggles every **24 steps** (step hook; V526 = steps, S526 = high tide).
Gull cries count down the last 3 steps, and a tide-mark rock changes colour.
- **High tide:** the tide-pool basin (12–27, 14–25) floods (impassable).
- **Low tide:** the basin's sand bars are walkable, and a short cut through the basin opens.
- **If high tide comes while you're on a bar,** the surge washes you back to the nearest dry ledge. Harmless, but it
  costs you the shortcut.
- **TEACH (1F south):** a short bar crossing that 24 steps easily covers.
- **TWIST (1F centre):** the basin crossing is 19 steps on the bars, so you start it right after a turn of the tide.
  There's a **gull roost** you can scare (action) to "hear" the timing: the gulls lift exactly when the tide turns.
- **COMBINE (565 B1F, optional, Brine TM55):**
  - A sea arch (4–27, 10–21) is crossable only at low tide and is longer than one tide window.
  - A **barnacle rock** (Rock Smash, after Badge 2) halfway along can be smashed to open a dry ledge, which splits the
    crossing in two.
  - The cross-map link: the arch's tide is the *same* counter as 1F's. Taking the ladder resets nothing, so you arrive
    knowing the tide state.
- **Reward:** TM55 Brine + Shell Bell (existing B1F items) + Pearl (hidden, 1F).

## D7 The Rimewood (562, 48×56) and Rimewood Glade (563, 34×30, Cut) — borderland A
**Rule:** frost holds what silk holds. This is the first ice in the game, a preview of Gym 10, gentler.
- **The Frost Loom (562 centre).**
  - A frozen heddle frame (a callback to Gym 2, the Weaving Hall). Three frozen threads hold three icicle curtains over the trail's
    side path.
  - Pulling a thread (action) runs frost along it: it **cracks** each frozen curtain on its line and **refreezes** any
    broken one. **Left** → curtains 1 and 2 · **middle** → 2 and 3 · **right** → 3.
  - **Unique answer: left + right** (verified by hand over Z₂: middle would refreeze curtain 2).
  - A breather that rewards remembering Gym 2. **State:** S531–S533 = curtains broken.
  - Reward behind it: the trapper's cache (Snowball ×2).
- **The frozen Hoar Brook:** an ice slide shortcut (one-way, top to bottom) from the aurora clearing back to Frostwick's
  edge. Shortcut principle.
- **Rimewood Glade, the Silk-fall pond (563):** a 13×9 slide puzzle at (10,8).
  ```
  ##########E##     E (10,0) islet with NEVERMELTICE
  #....#..#...#
  #.......#...#
  #....#......#
  #...#...#...#
  #..#........#
  #..#..#.....#
  #.#.....##..#
  ######F######     F (6,8) start
  ```
  - **Verified (BFS): 9 slides,** `U R U L D R D L U`.
  - The Ranger (20,24) gives the hint: "Ice doesn't stop you. Rocks do. Pick your rocks."
  - **Reward:** Never-Melt Ice + Revive (hidden).

## D8 The Rehearsal (568, 34×26, `:BLEED`, bonus) — "between the frames"
**Rule:** five seconds replay forever. Here a "second" is your step: the wagon crash advances one frame per step
(V536 = frame 0–4, step hook).
- On each frame, the wagon, the driver and the bolting Tauros occupy known tiles: event pages `[V536≥k]` per frame.
  Touching them costs nothing ("You pass through the moment, and it shivers.").
- Frozen salt gusts are **solid on even frames** and gone on odd frames.
- **Puzzle:** cross the salt flat to the Shard (2,22) and the TM10 (30,22) by moving only through gaps that are open on
  the frame you'll reach them.
  - Effectively a 5-beat rhythm. The onlookers' changing words each visit name the open lane ("left, left, centre,
    right, left").
  - Standing still is impossible (there's no waiting), but stepping back and forth spends frames.
- **Reward:** TM10 Work Up + Bleed Shard #3.

## D9 Pell Playhouse Backstage (151 old revolve 25×20, 152 Fly Loft 25×15, 153 Trap Room 20×15; `:GRAND_STAGE`, optional, after the Gym 2 badge) — "the stage moves, the marks don't" · 4/10, ~20 min

The Revision 10 Gym 2 puzzle, kept whole when Gym 1 became a walk-through (SPINE Rev 14). Entered by the stage-left wing
steps on the Gym 1 auditorium's apron (154 (1,9)); the door checks `pfm_gym_won?(:LEADER_TAMSIN)`. Dorian, after Gym 2:
"The revolve back there hasn't turned since my debut. Get it through all three acts. There's a prompt-book in the prop room I'd rather you found than the Crown's inspectors."
**Built and proven** (`mapgen/puzzles/playhouse.py`, `mapgen/gen_playhouse.py`): stage + loft 5 moves / 39 states (4/10),
Script order forced, unsolvable without the loft; Trap Room 3 cranks (3/10) on a new pattern the solver found (the spec's
pattern opened after one crank). Actors: Juggler Pierrot, Lady Odette, Gentleman Reginald (one per scene). Apprentices Pip,
Dot and Old Joss (`:pb_stage`, `:pb_loft`, `:pb_trap`). IDs: the Playhouse block, `STAGE_SCENE` V310, `STAGE_FLAT_A/B/C`
S310–312, `STAGE_TURNTABLE` V312, `STAGE_TRAP_DONE` S314. Rewards (story editor's ruling: Dorian keeps *The Gilded King*):
behind the upstage door an old Pageant prompt-book with every line about the old capital struck out in red, + Magical Seed
×2 + PP Up; the Trap Room chest holds the old Crown prop with its original stone still whole (`pfm?(:old_crown_prop)`).

*Design text (from GYM_PUZZLES Revision 10, coordinates superseded by the module):*

#### 151 Revolving Stage — TWIST "three scenes, in order" (25×18)
```
     0123456789012345678901234
y0   ############E#############    E (12,0) upstage door → 154 (10,13)
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

#### 152 Fly Loft — COMBINE "a flat is in one place at a time" (25×15; rows 6–14 void: the stage seen from above)
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

#### 153 The Trap Room — MASTERY "ride the revolve" (optional; 11×11 puzzle, padded to 20×15; via trapdoor p)
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
y10  #####@######    @ (5,10) ladder up to 152 p
```
- Turntable cells are 24 events, each with 4 pages (`[—]` rot 0, `[V312≥1]` rot 1, `[V312≥2]`, `[V312≥3]`). A cell is
  machinery (impassable tile) or blank (floor) according to the 5×5 pattern `..#.. / .##.. / #.o.. / #.##. / #..#.`
  rotated clockwise by V312 quarter-turns.
- **Crank** (action, only from the four tiles beside it): `pfp_cycle(312, 4)`, and **the player rides**: their offset from
  the centre (dx, dy) becomes (−dy, dx) (`pfp_turntable_ride(5,5)`). "You lean on the crank. The whole floor — and you
  with it — swings a quarter-turn."
- **Solution (verified, BFS):** walk to (4,5) and crank three times. You ride from west to north to east to south.
  Then walk east (6,6) → (7,6) → (8,6) and north up the right-hand corridor to the chest.
- **Reward:** Magical Seed ×2 (on Grand Stage: +1 Speed and Laser Focus), PP Up, and the old Crown prop with its original
  stone still whole (`pfm?(:old_crown_prop)`; a match for Saltmere's prop-room scene, Crown seed 2). Not the Gilded King's
  crown: Dorian keeps *The Gilded King* and hands over only the prologue page (story editor's ruling, SWAP_GYM1_GYM2 §2).
- **Reset:** the apprentice "Old Joss" (by the ladder) → V312 = 0.

---
# PART 2 — ONE SIGNATURE PUZZLE DUNGEON PER KINGDOM

## ELOWEN — Gossamer Heartwood (703, 40×40, `:SILKWOOD`, Act III revisit) — "the forest is a loom"
**Core rule:** the Heartwood is Mother Loom's original "great loom".
- Four **warp roots** run north–south and four **weft vines** run east–west.
- Pulling a warp **lever** raises the whole column of root-bridges under it.
- Pulling a weft lever **sinks** the row of vine-walls on it.
- A tile is walkable when its root is up **and** its vine is down.

- **Teach (south glade):** one warp and one weft, crossing at the glade gate.
- **Twist (the Weave):**
  - 4×4 crossings; the path to the Ogerpon shrine needs a specific pattern.
  - Warp levers are at the north edge and weft levers at the west edge, so you can only reach a lever whose row and
    column you can already walk.
  - Bootstrap in order: **W1 → The Ferrymen's Mile → W3 → The Grey Saltings → W2** (verify with the builder's grid BFS).
- **Combine (cross-map):**
  - At **VERDANCE_BLOOM V106 = 1** (Act III runaway bloom), warp 2 is overgrown and can't be pulled. The Weave then
    needs a different pattern that uses **Cut** on two vine knots (permanent, S543/S544).
  - So the dungeon is solved differently depending on whether you've visited Verdance (story-reactive).
- **Mastery:** Ogerpon's mask cache. The four masks hang at the four corners, and each needs its corner tile walkable
  at once (a full-board pattern).
- **State:** S541–S542 (warps), V541 (weft bitmask written by `pfp_check`), S543/S544 (cut knots), S545 (shrine).
- **Ties:** the Loyal Three / Ogerpon arc (Elowen legendary); Tamsin's grandmother's pattern returns as the shrine
  sampler.

## ZENITH — Voltaic Sluiceworks (584, 40×32 and 585, 30×24, `:SCRAPYARD`, optional from Act I) — "water carries current"
**Core rule:** Meridian's first hydro plant. Turbines make power only while water flows through them, and **flooded
floor conducts**: when the generator runs, every flooded tile is live (shock push-back).
- **Teach (584 west):** one sluice and one turbine. Open the sluice, the turbine spins, and a door lamp lights.
- **Twist (584 spillway):**
  - Three sluices (S546–S548) route water through turbines T1 and T2, and through floor sections F1–F3:
    - sluice 1 → T1 + F1;
    - sluice 2 → T2 + F2;
    - sluice 3 → F3.
  - **F3's overflow spills into T2's race** (visible flow decor), so sluice 3 also spins T2.
  - The exit needs **both turbines spinning** and **F2 dry** (your path crosses it while the generator runs).
  - **Answer: sluices 1 and 3, not 2.** T1 spins from sluice 1, T2 from F3's overflow, and F2 stays dry. The aha: a
    turbine can be fed without its own sluice.
- **Combine (cross-map):**
  - 585 Turbine Hall's **breaker** decides where 584's power goes: to the floodgates (which drain flooded sections
    after use) or to the Rotom control desk.
  - The order: power the floodgates, drain F1 and F3 so you can walk them, *then* flip the breaker to the desk. The
    static Rotom (Lv 25) wakes.
- **Reward:** the Field-Effects custom item listed in maps.json + Rotom. Lore: the plant's flood log (Meridian knew the
  Lattice drains the Ebb).
- **State:** S546–S548 sluices, S549 breaker, V546 drained sections.

## OSSARIA — Ossuary of Dunes (624, 44×40 and 625 Script Vault, 34×30, `:CAVE`, Act II, mandatory; Strength) — "write the word"
**Core rule:** the Electors wrote on doors. Unown-glyph **blocks** (Strength) slide into a door's slots, and a door opens
when its slots spell its word.
- **Teach (antechamber):** a 3-slot door with the word cut on its lintel. Three blocks lie in an open room: push them in
  order. Wrong blocks just sit there; pull them back out from the other side.
- **Twist (the Ossuary galleries):**
  - The word isn't written: it's a **riddle** whose answer is a word, made from the **sundial**.
  - A sun shaft (the Ossaria sun-mirror idea, gentler than Gym 5) falls on one of five glyph tiles depending on a
    rotating capstone (V551).
  - Each capstone position lights one glyph. The lintel reads "Spell what the sun touches, from dawn to dusk."
  - Turn the capstone through its 4 positions in order and note each lit glyph: those are the letters. Then push the
    blocks.
- **Combine (cross-map, 625 Script Vault):**
  - The vault's **pulley wheels** raise or lower sand in 624's lower gallery (S552). Lowered sand exposes a second
    block set; raised sand lets you push blocks *across* the pit.
  - The final door needs blocks from both galleries, so the sand state is toggled twice.
- **Mastery:** the Unown chamber. All 28 forms are catchable here, and the Odd Keystone sits behind a 6-letter word
  (`HOLLOW`, a foreshadowing hint from Sahar's rubbing).
- **State:** V551 capstone, S552 sand, S553–S555 doors opened.
- **Ties:** S116 CH6_OSSUARY_DONE; the Duneholt Rubbing; the sealed murals.

## ASHKAAR — The Cinderhorn (664 1F 44×40, 665 2F 40×36, 666 Caldera 40×40, `:VOLCANIC`, Act II) — "drain the mountain, mind the pressure"
**Core rule (Pyrous homage):** opening a **vent** on one floor drains the lava pools of the floor *above* through the
rock. But every drain raises the **caldera pressure** gauge (V556, 0–5) on the Caldera floor.
- At 5, the Caldera vents. That is a screen-shake set piece: all lava returns and pressure resets to 0 (a fair reset
  with a scare).
- **Bleeder valves** (one per floor) lower pressure by 2, but a valve can only be reached from a floor whose lava is
  drained.

- **Teach (1F):** one vent on 1F drains 2F's first pool (pressure 1). Climb up and see the dry pool.
- **Twist (2F):**
  - Three vents on 2F drain three Caldera pools (pressure +1 each). Two 1F vents drain 2F pools (+1 each).
  - The Caldera route needs pools C2 and C3 dry; 2F needs pool B1 dry to reach the C-vents. That's 3 drains =
    pressure 3, fine.
  - The trap: draining everything "to be safe" hits 5 and the mountain refills.
- **Combine:**
  - The 2F **bleeder valve** stands in pool B2, so you must drain B2 to use it (+1), then bleed (−2): a net −1 that
    buys room for the Caldera's last pool.
  - Order: B1, B2, bleed, C2, C3 → pressure 3 at the summit.
- **Mastery:** the Caldera floor's **Earthquake TM26** ledge (WORLD §6) needs C1 drained as well. Exact budget: B1, B2,
  bleed, C1, C2, C3 = pressure 4. One more mistake and it vents.
- **Ties:** the Caldera Crisis (Ch8, V110 CINDERVAULT_STATE). If Brann vented the caldera (V110 = 1), the Cinderhorn
  starts at pressure 2 and the ash is thicker: the same puzzle with less slack, so the story choice changes the
  difficulty.
- **State:** V556 pressure, S556–S560 (pools B1, B2, C1, C2, C3 drained); the bleeder is self switch A.

## ISENMAR — The Ice Vault under Whalebone Keep (308, 33×33 + 318 Vault Depths, new, 33×33; Act III, Kyogre) — "whalesong"
**Core rule:** ice carries sound. **Song pillars** of old ice ring one of four notes when struck (action). A note
travels along the ice channels cut in the floor (drawn as frost lines) and **cracks the first ice wall of the same
pitch** it reaches.
- Walls are colour- and pattern-coded by pitch: wavy (low), double (mid), dotted (high), plain (whale).
- **Teach (vault antechamber):** one pillar, one channel, one wall.
- **Twist (the Ringing Hall):** channels cross. A note follows its channel straight through crossings, so you find
  which pillar's channel reaches which wall. Two walls of the same pitch sit on one channel: strike once, the nearer
  wall breaks; strike again for the farther.
- **Combine (cross-map + story state):**
  - At **RIMEHOLT_STATE V107 = 1** (the Thaw), half the channels are meltwater.
  - Sound carries *farther* in water (it skips the first wall), so the same notes break different walls after the
    Thaw.
  - The Depths (318) can only be reached after the Thaw, and its route needs the water rule.
  - The ice-fishers' **whale song** (heard in Ebbmouth in Act I, MAPGEN §1) is the note order for the Depths' sealed
    door: the player has been humming the solution for two acts.
- **Mastery:** wake-tones for Kyogre's chamber; three pillars struck in the whale-song order within one breath (a tide
  of 12 steps).
- **State:** V561 pillar progress, S561–S565 walls broken.
- **Ties:** S128 CH11_THAW, S129 CH11_KYOGRE_DONE; Anja's family sounding-line (Gym 10 Mastery).

## ANTUMBRA — Mirror Mere (742, 36×32) and Giratina's Reverse Depths (806, 40×40, `:INVERSE`, Act III–IV) — "the other side is upside down"
**Core rule:** Antumbra is the world reflected. At Mirror Mere, the lake's reflection shows a *different* shore path
(drawn on the water as a reflection overlay): the path that exists on the other side.
- **Teach (742):**
  - The near shore path dead-ends at the reeds. The reflection shows a path through them.
  - Walk the reflected path: tiles that are reeds here are passable where the reflection shows path, via invisible
    passable events that only exist where the reflection draws them.
  - The aha is that the reflection is a map.
- **Twist (806 Reverse Depths):**
  - A **reversal bell** flips the Depths upside down: `pfp_swap_map` to the twin 807 (new ID; or a page-state twin) at
    **(x, H − 1 − y)**. Ceilings become floors, so a ledge on the ceiling is a floor after the flip.
  - Where you stand matters: you land at your mirrored y. Fall hazards are void where the twin has void, with landing
    fix-ups to the nearest safe tile and a stumble message.
- **Combine:**
  - Pushable **mirror-stones** (Strength) exist in both orientations at mirrored positions. Push one on the floor and its
    twin moves on the ceiling, mirrored, so a stone pushed *down* below is pushed *up* above.
  - Two pressure plates (one per world) need stones at the same time.
  - Plan pushes so that a single stone covers one plate in each world: impossible by construction, so you need both
    stones. The second stone is reachable only from the flipped world.
- **Mastery:** the Distortion seal (post-game link to 910). Three flips, each landing you on a different ledge, in the
  order the Reverse Depths' graffiti gives (the first gym-like "read the room" puzzle in Antumbra).
- **State:** S566 world flipped, S567–S569 plates and seal, V566 stone positions via `pfp_save` (shared between twins).
- **Ties:** S143 CH15_GIRATINA_DONE; Ilsa's reflection mechanic (Gym 12) returns with gravity.

## NADIR — Drowned Aurelia (824 Drowned Spires 44×44 `:UNDERWATER`, 825 Air Halls 40×36, 826 Gilded Throne Vault 30×30, Act IV, Dive) — "breath and floodgates"
**Core rule:** underwater (Dive), you have **breath**: 30 steps (V571, a step hook; a bubble meter picture). At 0 you
surface where you dived: a fair reset. **Air bells** (sunken church bells with trapped air) refill breath.
- **Teach (824 west):** a dive between two air bells, 22 steps apart.
- **Twist (824 spires):**
  - The only route to the Air Halls is 41 steps: longer than one breath.
  - A sunken **bell rope** lets you ring a bell to *move* its air pocket. Ringing tips the bell, and the air rises to the
    next bell on the same chain (S571).
  - Ring the west bell to shift its air to the middle spire, which splits the swim 20 + 21.
- **Combine (cross-map):**
  - The **Air Halls (825)** are half-flooded palace corridors with **floodgates** (S572–S574).
  - Opening a floodgate drains a hall into 824 below, which **adds an air pocket** in 824 where that water came out (a
    new refill bell appears) and opens a dry path in 825.
  - You alternate: drain a hall (825), dive (824) through the new pocket to reach the next sluice wheel, surface, drain
    the next.
  - Three drains reach the Gilded Throne Vault.
- **Mastery (826):**
  - The **Sun Court** sequence (S147). The throne vault's light shafts come down through the drained halls above. Each
    open floodgate lets light into one vault alcove (the Gilded Chain's links).
  - The three alcoves need light at once, but floodgate 2 floods alcove 3's stair when open. So: open gates 1 and 3,
    walk alcove 3's stair, then open gate 2 for the last light while standing in the alcove.
- **Ties:** Nyx's Keepers of the Drowned Truth; Princess Maren; the Gilded Chain. Nyx is the companion here (hints in
  her voice).
- **State:** V571 breath, S571 west bell tipped, S572–S574 floodgates, S575 Sun Court done.

---
## Toolchain needs specific to dungeons (in addition to GYM_PUZZLES §4)
- **One-way tiles** (silk curtains, ice slides): a `touch` page that rides the player 1 tile in the allowed direction,
  and an action page that refuses.
- **Step-driven world clocks** (tide, frames, breath, pressure is event-driven) through `pfp_step_hook`, with a small
  HUD picture for breath and tide (a picture-based meter, no new UI scene).
- **Watched-or-not movers** (Thistledown chairs): a step hook comparing facing.
- **Coordinate-transform twins** (Reverse Depths): `pfp_swap_map(id, transform: :flip_y)`.
- **Story-reactive pages:** dungeon layouts that read V106, V107, V110 (story variables, FLAGS.md) so the puzzle changes
  with the world state.
- Verification: the same `mapgen/puzzles/` models as the gyms. Verified here:
  - D3 parity (by hand);
  - D7 Glade slide (BFS, 9 slides);
  - D7 Frost Loom (by hand).
  The builder must verify D2 Deepwood, D4 cart routes, D5 chairs, D6 tide timings and every kingdom dungeon's final
  boards.
