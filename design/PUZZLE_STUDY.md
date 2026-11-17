# PUZZLE STUDY — how Reborn and Rejuvenation build their puzzles (and what Prismfall takes from them)

Owner: Puzzle Designer. Feeds `GYM_PUZZLES.md` (rewrite) and `DUNGEON_PUZZLES.md`. Answers SPINE Revision 10 item 6:
"Puzzles at Reborn's level. Gym and dungeon puzzles must be genuinely complex and satisfying."

**Method.** The Reborn and Rejuvenation games in `/home/claude/ref/games/` were read with our own safe Marshal reader
(`mapgen/rmarshal.py`, run as `python3 -I`; nothing from the reference folders was executed). Scratch tools in
`/tmp/pstudy/` dumped every event page (conditions, triggers, graphics, commands, move routes) with the game's own
switch and variable names from `System.rxdata`, summarised each map's state use, and rendered layouts with `mapgen/rref.py`.
The gym maps were found by searching every map for the leaders' `pbTrainerBattle(:NAME…)` calls. Map numbers below are the
games' own `MapNNN.rxdata` numbers.

**One honest gap.** For Rejuvenation's time-travel and mirror sequences, I found the maps: the "X" past-city family
(Dream District X 647/648/653, Scholar District X, Central Square X), Tower of Theolia 339 with its `MirrorWall1-3`
switches, and the Darchlight Mirror switch. Their events turned out to be mostly scripted story (camera moves, partner
battles), not self-contained puzzles. What they do show is the *pattern*: twin maps that share coordinates, plus a stored
player position (`WORLDCHANGE` / `PlayerPositionX/Y`, then a transfer by variables). Reborn's Coral Water Grid uses the same
pattern, and I decoded that one fully (§6). The Rejuvenation puzzles decoded in full are Crawli's Kakori obstacle courses,
the Chrysalis Soul Labyrinth and the Oblitus tactics gym.

---
## 1. Twelve puzzles, decoded

### 1. Julia's gym — Reborn, Peridot Gym (map 78, 65×26, 46 events) · Electric · *escort and detonate*
- **Mechanic.** Four Voltorb stand in side bays. Talking to one makes it a follower (`pbAddDependency2`). Walk it into a
  3×2 metal gate and the gate blows open (the gate's tiles are events whose pages switch from closed to rubble).
- **State.** One variable, `V54 Peridot Gym`, and its parity carries everything. Odd means "escorting Voltorb k"; even
  means "gate k open". Voltorb k sets it to 2k−1. Gate k accepts only `V54 % 2 == 1` and adds 1. Gate tiles show rubble at
  `V54 >= 2k`. Two extra numbers (a temp copy, `% 2`) do the job of four followers × four gates.
- **Reset.** Every exit door checks parity. If you leave mid-escort it removes all four followers and subtracts 1, so the
  Voltorb is back in its bay and nothing is lost.
- **Layout and curve.** A central N–S corridor with four stacked gates. Each Voltorb sits further from its gate than the
  last, and the last bay is behind a trainer.
- **Teaching.** The first Voltorb stands next to the first gate. A trainer's line names the rule out loud ("there are
  switches to the gates behind the gym… covered up by Julia herself"). The gym telecom explains the field.
- **Theme.** Julia runs city demolition. Her field boosts Explosion. The puzzle *is* her job.

### 2. Corey's gym — Reborn, Beryl Gym (map 162) · Poison · *coupled reactors (Lights Out)*
- **Mechanic.** Six reactor consoles in a 2×3 block. Each console toggles itself and its orthogonal neighbours
  (`Reactor 1-6`, switches 101–106). The console graphics are tile events, with columns of three tile events per reactor
  showing its state. Any console press sets `Beryl Door Check`, which re-evaluates the door on the next refresh.
- **Teaching.** None beyond the visible coupling: every press lights or darkens several columns at once. It works because
  the board is tiny (2^6 states).
- **Theme.** A toxic plant you must vent correctly.

### 3. Shelly's gym — Reborn, Lapis Gym (map 182, 35×35, 111 events) · Bug · *sliding bookcases*
- **Mechanic.** Seven bookcase heights (`Shelf1-7`, variables 0–4) and seven computers (`Comp1-7`). Each computer is a
  **reversible toggle**: switching it on adds 1 to two shelves, switching it off subtracts 1. A shelf at height 4 sets a
  `…Shelf up` switch and frees a corridor.
- **Hint system.** Two hidden variables, `Shelly Tracker` and `Shelly Guide`, record whether the player is following the
  intended order. A wrong press sets them to −1, which is what lets an NPC give a context-aware hint.
- **Reset.** A librarian NPC: "Would you like me to reset the puzzle to its original state?" She zeroes all 7 variables and
  3 switches behind a fade.
- **Teaching.** A trainer explains the rule ("Each computer lifts or raises a few different ones. The screens show which
  cases are affected!"). A second trainer half-solves it aloud ("Get the sides as high as possible, and the center low.
  Then when you're out, raise the center. I think.").
- **Theme.** The gym is a library. Shelly is shy and "one of the smartest girls around", so the puzzle is
  "college level".

### 4. Radomus's gym — Reborn, Vanhanen Castle (maps 313–318) · Psychic · *chess, mate-in-one with frozen pieces*
- **Mechanic.** The floor is a chessboard. Your pieces are events you push (move route `away`). The rules are spoken:
  pieces follow chess movement, the King's pieces never move, and you may not capture. A **check door** reads every
  piece's square into variables (`Free X / Free Y = event's x/y`, operand 6) and compares them against the solution set.
- **Feedback.** Each wrong board gets a specific diagnosis from Cain: "the King can still move out to those white
  spaces", "couldn't Black just capture that Knight?", "Is Black even in check right now?". You learn from every failure.
- **Curve.** Several boards in a row (316, 317, 318). Trainers between boards teach one rule each ("The Queen is the
  strongest piece", "The Pokémon out at the start are always Pawns!"). A butler in a side room answers rules questions.
- **Accessibility.** Pages test `Blindstep Accessibility` and `Puzzle Skip Password` switches.
- **Theme.** Radomus is a chess grandmaster. The field is the Chess Board.

### 5. Charlotte's gym — Reborn, Calcenon Gym (map 419, 20×65, 236 events) · Fire · *step on every tile exactly once*
- **Mechanic.** Three rooms of floor tiles. Each tile event has five pages:
  `cool → (touch) +1 Calc-n, self A` · `A: heated (tile 826) → (touch) self B` · `B: autorun: red flash, jump the player back
  to the room's start (jump distance precomputed per tile), set Calc reset-n` · `Calc reset-n: parallel: clear B, clear A` ·
  `Calc puzzle-n: solved look`.
- **Goal.** A goal tile activates only when the counter equals the room's tile count.
- **Curve.** The rooms grow: **19 → 40 → 75 tiles**, each a Hamiltonian path whose shape is set by pre-burnt orange tiles.
- **Reset.** Instant, local and free. A mistake costs only the walk back.
- **Theme.** Fire: the floor burns behind you.

### 6. Coral Water Grid — Reborn, maps 472 / 485 / 486 / 500 (25×30 each) · *water level + persistent floats*
- **Mechanic.** A switch (`Lower Level`) drops the water. At high water you hop stepping stones (`jump ±2`). At low water
  you walk the floor.
- **Persistence.** Floating blocks are pushed around and their positions are **saved in variables** (`l1x, l1y … l6y`,
  plus `jumps moved` and `block pair`). On map load each block is set back to its saved square. That is how block positions
  survive moving between four linked maps.
- **Lesson for us.** RMXP forgets moved events when you leave a map. Save positions explicitly whenever a puzzle spans maps.

### 7. Pyrous Mountain — Reborn, maps 33/34 (1F), 199 (B1F), 201–205 · *cross-floor causality*
- **Mechanic.** Opening a channel on one floor drains lava on the floor above ("The channel opens between the floors.
  The lava drains from the floor above!"). Switches `Pyrous B1 / 1 / 2 / 3`.
- **Why it works.** The cause and the effect are on different maps, so the "aha" is realising the mountain is one machine.
  A dependent partner (Victoria) and partner battles keep it story-driven.
- **Accessibility.** Later versions add a prompt: "Drain Pyrous Mountain lava on this file?"

### 8. Iolia Valley — Reborn, maps 333–350 · *colour crystals and keys*
- **Mechanic.** Crystal Plug key items let you activate crystals of one colour (Red, Green, Blue, Purple). Activating a
  colour flips a switch that summons dozens of tile events: bridges, walls, staircases (`IoliaBlue2-4`, `IoliaGreen5-8`).
- **Multi-stage objects.** A rock can be a state machine (`IoliaRed7`: 0 inert → 1 "the key reacted" → 2 smash once →
  3 smashed, now a portal).
- **One hole, two places.** The same hole leads to different rooms depending on another switch (`IoliaPurple4`).
- **Curve.** Each new plug re-opens old areas: Metroid-style backtracking with purpose.

### 9. Byxbysion Wasteland — Reborn, map 209 (130×80, 240 events) and children · *open hub*
- **Mechanic.** Five `Wasteland Reactor` switches, scattered tunnels and grottos, Tauros riding (smashes rocks), and
  shortcut switches (`Grotto Open`, `Bivouac Open`, `Tunnel Switch`).
- **Shape.** Nonlinear: you can attack the reactors in any order. Each one opens a shortcut back to the hub.
- **Lesson.** A big dungeon stays readable when every solved piece pays back a shortcut.

### 10. Saphira's gym — Reborn, Labradorra Gym (maps 779/780, 50×95) · Dragon · *King of the Hill (pursuit)*
- **Mechanic.** A huge Pokémon pursues you. Ruby lines compute the pursuer's next square from the player's facing.
  Contact triggers a battle.
- **State.** Checkpoints are stored in `Saphira Checkpoints` (0–3). A `Restart KotH` switch resets the pursuer.
- **Lesson.** A pursuer turns a maze into a timing puzzle. Checkpoints keep it fair.

### 11. Crawli's gym — Rejuvenation, Kakori Gym (maps 65/154) · *obstacle courses*
- **Mechanic.** Three courses: hopping rocks (`jump ±2` in all four directions), an `ElevationSwitch` that swaps which
  layer is solid, and lifts.
- **Tone.** The guide says it plainly: "Falling bears no real consequence". A failed hop just puts you back at the course
  start. Each course is a quest stage (`Quest | Course 1-3`).
- **Lesson.** Low-stakes failure makes players experiment, and experimenting is how they learn the rule.

### 12. The Soul Labyrinth — Rejuvenation, Chrysalis Courtyard (map 391) · *pursuers and a knowledge skip*
- **Mechanic.** Two Dusknoir patrol a hedge maze, their squares tracked in `Object1X/Y`, `Object2X/Y`. Caught means you
  are dragged back to the start (`Caught by Dusknoir`).
- **The real solution is information.** Servants in the manor hint at a hidden switch behind a sign
  ("DUSKNOIR MAZE DEACTIVATION"), and a bracketed hint says so (`\c[6]There's gotta be a trick to this place…`).
- **Lesson.** Clue-gathering elsewhere can unlock a puzzle, which rewards exploration over brute force.

**Also noted.**
- Rejuvenation's **Oblitus Gym** (661) is a full tactics minigame. It has unit selection, enemy phases and per-unit
  switches, and it proves a gym can change genre for one set piece.
- **Cyrela's Estate (R)** (671) locks progress behind *information*: letters on a table give a code, entered through a
  name-entry screen.
- Rejuvenation's **Goldenwood** uses an `ElevationSwitch` (map 25) to swap walkable layers.
- Reborn's **Agate Circus / Big Top** (355/356) is a hub. The Big Top's floor is "a panel system for the big High Striker".

---
## 2. What these puzzles have in common

| | Teaches the rule by… | State | Reset | Escalation |
|---|---|---|---|---|
| Julia | first follower beside first gate; trainer line | 1 var, parity | leaving the map | 4 gates, longer walks |
| Corey | visible coupling on a tiny board | 6 switches | re-press | none (single board) |
| Shelly | trainer states rule + half-hint | 7 vars, 7 switches | NPC, one line | 3 → 7 shelves |
| Radomus | trainer per rule; butler room | positions → vars | push back | several boards |
| Charlotte | the first room is tiny | self A/B + counter | instant, per tile | 19 → 40 → 75 |
| Coral | the switch is next to the first hop | positions in vars | re-enter | 4 maps |
| Pyrous | the message names the effect | 4 switches | none needed | floor by floor |
| Iolia | one colour at a time | switch per colour | none (monotonic) | colours re-open old areas |
| Kakori | a "harmless" first course | quest var | fall = restart | 3 courses |
| Soul Labyrinth | the chase *is* the lesson | object x/y | caught = start | a knowledge skip |

---
## 3. Design principles for Prismfall (every gym and dungeon spec is checked against these)

1. **One core rule, grown in four beats.** *Teach* (the rule alone, no way to fail) → *Twist* (one new fact that breaks
   the naive plan) → *Combine* (the rule meets a second system) → *Mastery* (an optional harder room with a real
   reward). Charlotte's 19/40/75 and Shelly's 3→7 shelves are the model.
2. **Show the coupling.** If pressing A moves B, the player must be able to *see* the link: Corey's lit columns, Shelly's
   screens, our silk threads and rope rails. Hidden couplings are allowed only as the planned "aha" of a Twist beat, and
   then they must be noticeable on a second look (something visibly moves when you act).
3. **Say the rule in-world, twice.** Once by a sign or guide (the rule), once by a trainer or apprentice (a half-hint
   that is slightly wrong or incomplete, as Shelly's trainer's is). Reborn never relies on the player guessing the rule.
4. **The "aha" must be a fact about the world, not a trick of the UI.** "The snag only catches seaward drift", "the flat
   that leaves the stage hangs in the loft", "the drone is a portable wire". When it lands, the player can explain it in
   one sentence.
5. **Reset is fair, local and fast.** Every puzzle room has an **apprentice** (a reset NPC, Shelly-style) plus natural
   resets (leaving the room, a fall back to the room's start). No reset ever costs more than walking back across one
   room. Failure is cheap (Kakori). Story-free fails never cost items or money.
6. **No soft-locks, provably.** Every state the player can reach must reach the apprentice or the room's start. Every
   gym spec ships a state model, and the map builder runs a BFS over it (`mapgen/puzzles/`, §5 of GYM_PUZZLES). Rope
   posts and levers are placed so they can only be used from safe tiles (Gym 2's "marks").
7. **Persist what the player built.** RMXP forgets moved events when you leave a map. If a puzzle spans maps or
   invites leaving to heal, store positions and rotations (Coral's `l1x…` pattern; our `pfp_*` helpers with `pfm` flags)
   and restore them on load.
8. **Feedback names the mistake.** Wrong answers get *diagnostic* text (Radomus/Cain), not just "nothing happened".
   Every check event in our specs lists its failure messages.
9. **Hints are tiered and earned.** Track resets or wrong checks (Shelly's Tracker/Guide). The apprentice offers
   nudge → strong hint → walkthrough. The `puzzleskip` password (Reborn's Puzzle Skip Password) lets the apprentice solve a
   room outright. Accessibility first: no puzzle needs colour vision alone (every colour also has a shape or label), and
   none needs fast reflexes on Standard difficulty.
10. **Tie it to the Warden, the field and the kingdom.** Julia's demolition, Charlotte's burning floor, Radomus's chess.
    In Prismfall the puzzle is *the Warden's job* (a loom, a stage, a lock system, a circuit bench, a dig site, a
    dispensary…), its solution often *changes the battle field* (Gym 9), and its "aha" usually reveals a story truth
    (Gym 1's brass wire, Gym 4's empty Plate socket).
11. **Cross-map cause and effect is the big-dungeon tool.** Pyrous's drains and Iolia's colours make a dungeon feel like
    one machine. Each kingdom dungeon has one such link.
12. **Every solved piece pays back a shortcut** (Byxbysion). Big dungeons are hubs with one-way shortcuts that open as
    you solve.
13. **Pursuers, timers and step budgets are spice, not the meal.** Use at most one per gym (Saphira, Soul Labyrinth),
    always with checkpoints and a cheap reset, and never on a puzzle that also needs careful thought. On Casual
    difficulty, timers and step budgets loosen by half.
14. **Escalate by composition, not by size.** Late gyms are harder because systems interact (water level × raft drift
    × gate; circuit × drone × latch), not because rooms are bigger. A 29×25 room is enough.
15. **Variety across the 18.** No core mechanic repeats. The gym roster in `GYM_PUZZLES.md` covers coupling, state-mazes,
    flow, routing, layered drops, measurement, heat, pursuit, growth, sliding, wind, reflection, light, twin worlds,
    conveyors, stealth, logic and balance.

---
## 4. Engine patterns we reuse (and their RMXP / Essentials v21.1 implementation)

| Pattern | Source | How we build it |
|---|---|---|
| Tile-graphic events toggle passability | everywhere | event page `graphic {tile}`. A walkable plank uses a passable tile; a wall uses an impassable tile |
| Exact-value pages | Iolia, Calcenon | RMXP tests variables only with ">=", so each state needs a page for `>=k` and a later page for `>=k+1` |
| Reversible toggles | Shelly | the press subtracts when the device is already ON. The player never has to undo a whole sequence |
| Parity / packed state | Julia | one variable holds "carrying" + "progress". Saves IDs; we use it for escort puzzles |
| Positions → variables | Radomus, Coral | `pbSet(v, event.x)` (RMXP operand 6). Our `pfp_save` writes them to `pfm` flags (saved, costs no IDs) |
| Visit-once tiles | Calcenon | 3-page tile events + a room reset switch read by a parallel page |
| Followers | Julia | Essentials v21.1 `Followers.add(event_id, name, common_event)` / `Followers.remove(name)` |
| Pushable objects | Radomus, Coral | Essentials `pbPushThisEvent` (or `pbPushThisBoulder` with Strength). `$PokemonMap.addMovedEvent` keeps them until you leave the map |
| Twin maps, same x,y | Coral, Rejuv X-maps | transfer to the twin at the player's x,y with a fade. Landing fix-ups for tiles that are solid on the twin |
| Pursuers | Saphira, Soul Labyrinth | a per-step hook moves the pursuer one square toward the player. Contact = battle or reset |
| Knowledge locks | Soul Labyrinth, Cyrela | NPC clue → a hidden switch, or a number/name entry (`pbMessageFreeText` / number input) |
| Accessibility skip | Reborn | Core password `puzzleskip` → the apprentice offers "Skip this room" |

---
## 5. What we deliberately do *not* copy

- **Blind trial and error** (unmarked invisible floors with no clue). Every invisible thing in our specs has a tell
  (a reflection, a sound, a glyph).
- **Huge rooms as difficulty** (Calcenon's 75-tile room is the ceiling we allow, and only on an optional path).
- **Puzzle state in dozens of switches.** Our block is 5 + 5 IDs per gym. Complex boards keep their state in `pfm` flags
  through the `pfp_*` helpers and use switches only where a page condition needs them.
- **Reset by leaving the gym.** Julia's reset is elegant, but our apprentice reset is one line and keeps the player
  where they are.
