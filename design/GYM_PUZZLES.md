# GYM PUZZLES — all 18 Wardens

Room IDs follow WORLD.md §2: gym n lives at **100 + 20n + 10 …** (entrance first, Warden arena last). Every battle inside a gym uses that gym's field (map default in `FieldEffects::MAP_FIELDS`).
Gym trainers sit at **cap −4 … cap −1**. Classes are stock Essentials unless marked *(new)*. Once a trainer is beaten, it stays beaten (self-switch A).

**Puzzle state:** gym n uses **Switches & Variables `300+5n … 300+5n+4`** (Gym 1 = 305–309 … Gym 18 = 390–394). This is outside the story's 101–300 block and is requested for FLAGS.md (see SPINE_FEEDBACK). Use self-switches wherever a flag is local to one event.

**RMXP techniques used (all event-only, no new scripts unless noted):**
- **Tile-graphic events change passability.** An event whose graphic is a tileset tile (bridge plank, raft, ice block) uses that tile's passage. Use this to make "void"/water walkable when a page is active.
- **Variant maps.** Copies of one room with identical walls and different water/floor states. Transfer to the same x,y with a fade. Use them when a whole room's floor changes.
- **Forced moves.** Player Touch event → Set Move Route (player, Through ON, Ignore if can't move OFF) → steps or jumps. Use for ziplines, conveyors, currents and wind.
- **Reset tiles.** Player Touch → message → fade → transfer to the room's start. Use for shocks, pitfalls and "seen" guards.

---
## Gym 1 — Briarwick, Loomhouse Gym · Tamsin Loom (Bug, :SILKWOOD, cap 15)
**Idea:** "Every thread has to line up." Tamsin is young, patient and quietly over her head. She has re-threaded the ancient loom with Meridian wire, and an apprentice whispers about it. The puzzle is a loom: you pull heddles until the threads align, then ride the shuttles. Rooms 130 → 131 → 132 → 133.

**130 Foyer (15×13).** The gym guide hands over a "pattern card" (sign text: *"Red lifts the warp and the weft. Gold lifts the weft and the woof. Green lifts the woof and the warp."*).

**131 Weaving Hall (25×21): Heddle Bridges.**
```
 y0   ###########[EXIT x12]###########
 y1-2 =========== ledge N (full) =====
 y3-6 vvvvvvvv gap A vvvvvvvvvvvvvvvv     <- plank A at x3 | x12 | x21 (var V305)
 y7-8 ==[x3 pad]#silk#[x12 ...... x21]=   ledge 2: wall between x3 and x12
 y9-11 vvvvvvv gap B vvvvvvvvvvvvvvvvv    <- plank B at x3 | x12 | x21 (var V306)
 y12-13 [x3 ...... x12]#silk#[x21 pad]    ledge 1: wall between x12 and x21
 y14-17 vvvvvvv gap C vvvvvvvvvvvvvvvvv   <- plank C at x3 | x12 | x21 (var V307)
 y18-20 ===== ledge S: RED(3,19) GOLD(12,19) GREEN(21,19) levers, entrance x12 =====
```
- Gaps are void tiles (impassable, dark canopy below). Each gap has **3 candidate plank columns** (x=3, 12, 21). Each column is a stack of plank events (one per gap row) whose page condition is "Variable V30x == k" and whose graphic is the bridge tile. Inactive columns are blank, so the void shows through.
- The levers are coupled like heddles (all values mod 3): **Red: A+1, B+1 · Gold: B+1, C+1 · Green: C+1, A+1.** Start A=B=C=0 (all planks at x3).
- Geometry: the exit is at x12, so A must be 1. Ledge 2's wall means B must land on the {12–21} side. Ledge 1's wall isolates x21. The valid end states are **(A,B,C) = (1,1,0), (1,1,1) or (1,2,2)**. One solution is Red×2, Gold×2, Green×2 → (1,1,1).
- A soft reset is the levers themselves (no fall). Bug Catcher on ledge 1 (x12), Lass on ledge 2 (x21), both with sight 3.

**132 Canopy Lofts (25×25): Shuttle Ziplines.** There are six platforms P1–P6 joined by silk lines. Each platform has one **spool** (a Player Touch event on its edge) that slings you to another platform by forced move (Through ON, a 1-tile jump at each end). Its destination depends on a switch.
| Spool | OFF → | ON → | Flipped by |
|---|---|---|---|
| s1 (P1 start, 2,22) | P2 (12,20) | P3 (4,12) | cord α on P1 |
| s2 (P2) | P4 (20,14) | P1 | cord γ on P2 |
| s3 (P3) | P5 (12,6) | P4 | cord β on P3 |
| s4 (P4) | P2 | **P6 exit (22,2)** | cord β |
| s5 (P5) | P3 | P6 | cord γ (starts ON) |
- Switches S305–S308 hold s1, s2/s5, s3/s4. Intended route: pull α, ride s1 to P3, pull β, ride s3 to P4, ride s4 to P6. P5 holds an item (Silver Powder) and also exits if γ is set right.
- Every platform has a rope ladder, "Climb down to the loft floor?", which takes you back to P1. This prevents soft-locks such as the P2↔P4 loop.
- Trainers: Bug Catcher (3 mons) on P2, Pokémon Ranger ♂ on P4.

**133 The Spindle (15×15).** Tamsin, single battle. After the win: Badge 1, TM89 U-turn. The Cutter's House in town then gives HM01.
**Trainers (4):** Bug Catcher ×2 (Lv 11–13), Lass ×1 (12–13), Pokémon Ranger ♂ ×1 (13–14).

---
## Gym 2 — Saltmere, Pell Playhouse · Dorian Pell (Normal, :GRAND_STAGE, cap 19)
**Idea:** "The stage tells the truth the throne won't." Tonight's play is *The Gilded King* (story tie: the Prismfall truth), and the player is cast as the understudy. The puzzles are stagecraft: scene order, where the light falls, and which mask truth wears. Rooms 150 → 151 → 152 → 153 → 154.

**150 Foyer (19×13).** The usher gives the **Script** (sign/readable item): *"Act I, the Shipwreck. Act II, the Forest. Act III, the Throne. At the curtain, every light upon the Beast. Tonight the truth wears a smile."*

**151 Revolving Stage (25×19): Scene Order.**
```
   [door L]     [door C]     [door R]        y1   upstage doors (decor, locked)
  +-----------------------------------+
  |   REVOLVE: set-piece events with  |       y4-13  set pieces change per V310
  |   3 pages (0 Shipwreck/1 Forest/  |
  |   2 Throne); passability per page |
  +-----------------------------------+
  [ladder 2,2 - fly loft, locked]   lamps I II III (stage-left wall)   WHEEL (22,16)
                     entrance (12,18)
```
- The **stage-manager's wheel** cycles V310 (scene 0→1→2→0). Each page swaps the set-piece events (ship flats, tree flats, throne and pillars). They change both look and walkable lanes.
- The first time each scene is set **in Script order**, an "actor" trainer walks onstage and battles you (the performance), and that act's lamp lights (V311 = acts completed, 0–3).
- Setting a scene **out of order**: the director's voice yells "CUT!", the lamps go dark and V311 = 0. Actors you already beat don't re-battle; they just bow, which lights the lamp again.
- At V311 = 3 the wing ladder unlocks (S310) and leads to the 152 Fly Loft.

**152 Fly Loft (25×15): Spotlights.** The north catwalk (y2–4) is walkable. Below it is a non-walkable "stage view" (y6–14) showing the three marks **Hero (x5) · King (x12) · Beast (x19)**.
- There are three spotlights on the catwalk. Interacting rotates each one's aim Hero→King→Beast→Hero (V312/V313/V314, values 0/1/2). Each spotlight has 3 beam events in the stage view, one per target, shown by page condition.
- **Rigging coupling:** turning spotlight 2 also turns spotlight 3. Start (0,1,1). Target "every light upon the Beast" = (2,2,2). Solution: Spot 1 ×2, Spot 2 ×1.
- When all three aim at the Beast: a curtain-rise SE plays, a trapdoor opens at (12,3) and leads to 153. One Gentleman trainer patrols the catwalk.

**153 Dressing Rooms (27×11): The Mask.** Four doors: Comedy, Tragedy, Crown, Fool. The Script says "truth wears a smile", so **Comedy** is correct.
- The correct door unlocks the corridor's east exit (S311). A wrong door holds an actor trainer (Lady, Juggler). After that battle the room says "Wrong costume!" and you're back in the corridor. Wrong doors don't lock anything.

**154 The Grand Stage (21×15).** Dorian, **double battle** (curtain call; the gym-double trope), with an audience of NPC sprites. Badge 2 + TM42 Facade.
**Trainers (5):** Juggler ×2 (15–18), Beauty ×1 (16–17), Gentleman ×1 (16–17), Lady ×1 (17).

---
## Gym 3 — Ebbmouth, Tidelock Gym · Marisol Reyes (Water, :WATER_SURFACE, cap 23)
**Idea:** "The river runs both ways." Marisol is disciplined and protective, and her brother runs a Hollow cell. The gym is a lock system: you control the level and direction of the water.
**Rooms:** 170 Lock Hall → **171/172/173 Basins (variant maps: Low / Mid / High water)** → 174 Warden's Pool.
- The three basin maps share identical walls. **Low:** a mud floor you can walk, with rocks blocking some lanes. **Mid:** water at walkway height, and floating **raft events** (tile graphic = raft, so passable) bridge the gaps. **High:** channels full, with **current tiles** (forced 1-step moves) pushing along lanes. Only High reaches the north exit (14,0).
- **Sluice wheels** W (3,20), C (14,10) and E (25,20) exist on every variant. Turning one raises or lowers the level by one (wheel W: −1, wheel E: +1, wheel C: toggles Low↔High) and fades to the **same x,y** on the other variant. If that tile is water on the target variant, the player is placed on the nearest raft or walkway (a per-wheel landing tile is fixed in each variant).
- **Tide Bell** (High only, 14,2) flips the current direction (S315) to mirror Ebbmouth's day/night river. The exit lane needs the north current. The bell is two tiles from the exit, but the lane leading to it only flows north when S315 is OFF. So: ring at Mid via the bell-rope (a 2nd bell event reachable on Mid), then raise to High.
- Intended route: Low (walk to wheel C), toggle to High (ride a current east to wheel E's landing), drop to Mid with wheel W, cross the rafts to the bell-rope, ring it, rise with wheel E, ride the north current to the exit.
- Trainers stand on different variants (`on` = which level): Swimmer ♀ (Low), Swimmer ♂ (Mid), Sailor (High), Fisherman ×2 (Lock Hall/Mid). **5 trainers, Lv 19–22.** Marisol: single battle. Badge 3 + TM03 Water Pulse.

## Gym 4 — Lumen City, Circuit Gym · Rook Calder (Electric, :NEON_GRID, cap 27)
**Idea:** Rook is a hacker-engineer who thinks in circuits and treats the gym as a test bench. You route power, then cross a dark grid where only live current glows.
**190 Switchroom → 191 Breadboard Hall → 192 Blackout Grid → 193 Core.**
- **191 Breadboard (27×21):** a 3×3 grid of **conduit nodes** (V320–V324 hold rows/cols as needed; or 9 self-tracked vars via Core helper `Prismfall.var_ring`). Each node is an event with 4 pages (straight ─/│, corner ┌┐└┘ shown by rotation). Interact: rotate 90°. The generator is on the W wall and the door lamp on the N wall. The mapper fixes one target rotation per node along a printed path, and a parallel-process event checks all 9 against the targets. The door opens on a match (S320). Wrong nodes don't matter if they aren't on the path. Use 2 corner + 1 straight decoys.
- **192 Blackout Grid (27×25, dark):** the room uses Essentials' darkness (map metadata `DarkMap`; the player has a small radius, no Flash needed). **Neon floor lines A/B/C** are tile events that glow when live. **Breakers A, B, C** on the W wall toggle S321–S323. Stepping on a live line = shock: a message, then a forced push back 2 tiles. Dead lines are dark but safe. You navigate by the glow of the live lines next to the dark ones. The exit corridor needs A dead, B live (it lights the far bridge) and C dead. Engineer ×1 sits mid-room.
- **Trainers (6):** Engineer ×2, Scientist ×1, Rocker ×1, Super Nerd ×1, Gym Guide's rival "Circuit Tester" (Engineer) ×1, Lv 23–26. Rook: single. Badge 4 + TM43 Volt Switch + TM70 Flash.

## Gym 5 — Duneholt (210–213) · Sahar Ostrand (Ground, :DESERT, cap 31)
**Idea:** Sahar is an archaeologist-Warden and the gym is her dig site. Two stacked floors: **211 Dunes** and **212 Under-Dig**, the same footprint one floor down.
- **Sinking sand:** marked pit tiles (Player Touch) drop you to the same x,y on 212 with a fall animation. 212 has ladders up at fixed points. This is the classic two-layer pitfall maze: you reach the arena door by dropping through the right pits.
- **Sun-mirror:** a rotatable mirror on 211 sets V330 (4 directions). Its "shadow" event points at one of 4 sealed sand pits. Only the pointed pit opens (S330), and it leads to the 212 chamber with the arena ladder.
- Sandstorm overlay (fog) cuts visibility on 211. **Trainers (5):** Ruin Maniac ×2, Hiker ×2, Picnicker ×1 (27–30). Sahar: single. TM83 Bulldoze.

## Gym 6 — Mirefen (230–233) · Corvin Mott (Poison, :CORROSIVE_MIRE, cap 35)
**Idea:** Corvin is a chemist-physician with gallows wit, and he runs a ward for the Fixing sick. The puzzle is reagent mixing.
- **231 Vat Room:** three valves (Red, Blue, Yellow; S335–S337) feed a central vat. Its colour (V335) is the mix of any two open valves: purple, green or orange. Opening three makes brown and triggers a fume reset. **Sludge doors** in 232 each dissolve only for one colour (door events check V335 when you return with a filled flask item flag).
- **232 Sludge Gallery:** a toxic floor. Each step on sludge adds 1 to a filter counter (V336). At 12 steps: "Your mask filter is spent!" and you're reset to the gallery start. Filter refills (step resets) sit in 3 alcoves. Three coloured doors in sequence: green, purple, orange, so you go back to the vat twice.
- **Trainers (5):** Scientist ×2, Burglar *(Nadir scavenger)* ×2, Nurse-themed Aroma Lady ×1 (31–34). Corvin: single. TM84 Poison Jab.

## Gym 7 — Cindervault (250–253) · Brann Holloway (Fire, :VOLCANIC, cap 39)
**Idea:** Brann is a gruff foundry-master who secretly fears the caldera tap. The puzzle is minecart rails and magma timing.
- **251 Rail Yard:** ride a **minecart** (forced move route) along tracks. Four junction levers (S340–S343) set each fork. The cart route event branches on those switches (one move route per branch). Routes end at the next platform, a dead end with a trainer, or slag (bounce back to the start).
- **252 Geyser Walk:** magma geysers on a 3-beat cycle (parallel process with V340 timer 0–2, which switches their graphic and passability). You cross on the cool beat. Touching an active geyser = burn message + reset.
- **Trainers (5):** Worker *(Engineer)* ×2, Black Belt ×1, Kindler-style Camper ×1, Ace (Cool Trainer ♂) ×1 (35–38). Brann: single. TM35 Flamethrower.

## Gym 8 — Ironreach (270–274) · Kaito Ren (Fighting, :COLOSSEUM, cap 43)
**Idea:** Kaito is a pit-fighter turned Warden whose code is "discipline over rage". The gym is three trials, then the pit.
- **271 Strength Trial:** a Sokoban room. Push 3 boulders (Strength) onto plates within **24 pushes** (V345 counts pushes; over the limit = boulders reset).
- **272 Discipline Trial:** a memory path. A scroll shows a 6-step stance sequence, and you walk the stepping stones in that order. A wrong stone drops you to a pit trainer, then back.
- **273 Endurance Trial:** three back-to-back trainer battles with no healing between (a scripted chain). A nurse sits at the trial's entrance only.
- **274 The Pit:** Kaito, **tag battle** (partner Kestrel, K4 arc; story team confirms) or single on Standard. TM31 Brick Break.
- **Trainers (6):** Black Belt ×2, Crush Girl ×2, Battle Girl-style Crush Kin ×1, Pit Brawler *(new)* ×1 (39–42).

## Gym 9 — Verdance (290–293) · Juno Hale (Grass, :FLOWER_GARDEN, cap 47)
**Idea:** Juno, the new Warden, is restoring her uncle's overgrown garden-maze. Watering plots grows or shrinks vine walls.
- **291 Hedge Garden:** 6 seed plots, each with a growth stage V350–V354 (0–4) shown by 5 event pages. **Watering a plot (+1) also grows its two neighbours**, so vine walls between rows rise and fall (a lights-out variant on a ring of 6). Hedge "gates" open when the plots on either side are both at stage 2.
- **Field tie-in:** the arena (293) starts at **FLOWER_GARDEN stage = number of plots left at stage 4** (min 1). Over-watering helps Juno, and the gym guide warns you. Story-friendly: she wanted your help, but it costs you.
- **Trainers (5):** Aroma Lady ×2, Pokémon Breeder ×1, Picnicker ×1, Gardener *(Lass)* ×1 (43–46). Juno = J3, **double battle**. TM53 Energy Ball.

## Gym 10 — Rimeholt (310–313) · Anja Sorrel (Ice, :FROZEN_LAKE, cap 51)
**Idea:** Anja is a stoic lake-keeper whose lake is thawing under a Meridian Lattice. Ice sliding (native v21 `Ice` terrain tag) with melt/refreeze.
- **311 & 312 Ice Halls:** classic slide puzzles. **Braziers** (S355–S357) melt marked ice tiles into water stoppers (tile-graphic events switch between ice and water). Water stops a slide one tile early. Re-lighting refreezes. 312 adds a cracked-ice tile that breaks after one pass and drops you to 311.
- **Trainers (5):** Skier-style Cool Trainer ♀ ×2, Hiker ×1, Swimmer ♂ (ice diver) ×1, Boarder *(new)* ×1 (47–50). Anja: single. TM13 Ice Beam.

## Gym 11 — Skyreach (330–333) · Odessa Gale (Flying, :STORMFRONT, cap 55)
**Idea:** Odessa is an irreverent airship captain. The gym is a storm-lashed spire of wind tunnels.
- **331 Gust Deck:** fans (forced-move tiles) push you across gaps. **Weather vanes** (V360–V362, 4 directions) rotate the fans' push direction. This is a slide puzzle with steerable arrows.
- **332 Updraft Shaft:** updraft tiles carry you to upper catwalks (transfer to the same x on the floor above). Lightning flashes on a 4-second timer briefly light the dark shaft (screen flash + map events visible during the flash only).
- **Trainers (6):** Bird Keeper ×2, Pilot *(Cool Trainer ♂)* ×2, Sky Courier *(new)* ×1, Gambler (stormchaser) ×1 (51–54). Odessa: **double battle** (tailwind theme). TM51 Roost.

## Gym 12 — Lucent (350–354) · Ilsa Marr (Psychic, :MINDSCAPE, cap 59)
**Idea:** Ilsa reads every truth and chooses silence (she is Valen's daughter). There are three "memory rooms", each a different perception trick.
- **351 Teleport Atrium:** a pad network. A **focus mirror** (S365) swaps the whole network's destinations, so there are two pad graphs on one map (each pad event has 2 pages).
- **352 Unseen Floor:** an invisible path over a void. Footprint events appear only while you hold the **Lens of Truth**-style item (*prov.* key item from Ilsa's aide) or only in the mirror's reflection on the wall (a mirror-image strip shows the safe tiles).
- **353 The Quiet Room:** a riddle room where answering truthfully to an NPC's question opens the door. Ilsa's theme: honesty isn't always kind, and the "kind lie" choice also opens a door but leads to an extra trainer.
- **Trainers (6):** Psychic ♂ ×2, Psychic ♀ ×2, Channeler ×1, Scholar *(Super Nerd)* ×1 (55–58). Ilsa: single, **multi-bar boss style intro (EBDX boss module)** optional on Hard. TM29 Psychic.

## Gym 13 — Cragholm (370–373) · Bastian Ore (Rock, :CRYSTAL_CAVERN, cap 63)
**Idea:** Bastian is the oldest Warden, folksy, and a witness to the Crown's cracking. A light-beam puzzle through crystals.
- **371 Prism Gallery:** a light source at the entrance. **Rotatable crystals** (2 states, / or \, S370–S373) redirect the beam. Beam-segment events are shown by condition (the mapper precomputes the lit segments for each crystal state along the intended route). The beam must reach the arena door's crystal lock.
- **372 Quarry:** Strength boulders + Rock Smash rocks + one Rock Climb wall. Trainers are hidden in the rock face.
- **Arena twist:** the battle starts on CRYSTAL_CAVERN. If Bastian's ace uses a darkening move, it shifts to DARK_CRYSTAL (a SPINE transition).
- **Trainers (5):** Hiker ×2, Ruin Maniac ×1, Worker ×1, Gemcutter *(Lady)* ×1 (59–62). TM76 Stealth Rock.

## Gym 14 — Gravenmoor (390–394) · Ysolde Ashgrave (Ghost, :HOLLOW_CATHEDRAL, cap 67)
**Idea:** a cathedral that exists twice, living and dead. This is Morwen Vane's old seat, and the AF 290 truth (K6) surfaces here.
- **Bell toggle:** ringing the nave bell swaps the player between twin maps **391 Living Nave** and **392 Dead Nave**, at the same x,y. They have different walls and pews. Ghost trainers exist only in the Dead Nave.
- **393 Requiem Crypt:** light 6 candles in the order the gravestone verses give (V390 sequence check). A wrong order snuffs them all.
- **Trainers (6):** Channeler ×3, Gentleman (revenant) ×1, Lady ×1, Mourner-acolyte *(HOLLOW)* ×1 (63–66). Ysolde: **double battle**. TM30 Shadow Ball.

## Gym 15 — Cogsworth (410–413) · Magnus Strade (Steel, :FACTORY, cap 71)
**Idea:** Magnus is a foundry-master torn between Meridian contracts and his workers. Conveyors, presses and a crane.
- **411 Assembly Line:** **conveyor belts** (forced moves). Lever groups reverse belt directions (S395–S397). **Presses** on a timer (like gym 7's geysers) reset you if they hit.
- **412 Crane Bay:** move a crane (directional controls via a choice menu) to lift crates onto plates. 3 crates, 3 plates.
- **Arena twist:** a Wrecking-ball event in the battle (Field Effects: FACTORY→SCRAPYARD) if a crate falls (Core story hook optional).
- **Trainers (6):** Engineer ×2, Worker ×2, Scientist ×1, Meridian Foreman *(MERIDIAN_*)* ×1 (67–70). Magnus: single; the **partner battle** with his apprentice vs. Meridian enforcers happens just before (story). TM91 Flash Cannon.

## Gym 16 — Underveil (430–433) · Nyx Calloway (Dark, :NEW_MOON, cap 75)
**Idea:** Nyx is an information broker. The puzzle is a stealth heist in total darkness.
- **431 Gallery of Shadows:** a dark map. **Patrol guards** walk fixed move routes with sight-cone trainer events (sight 3). Being seen = battle, then "Caught!" and a reset to the room start. Shuttered lanterns (S400–S402) light corridors but make the nearest guard turn toward the light.
- **432 Vault:** steal 3 "secrets" (event items). Each one changes which shadow doors are open (doors open only when the room's lights are OFF).
- **Trainers (6):** Burglar ×2, Gambler ×1, Rocker ×1, Hollow Defector *(HOLLOW)* ×1, Informant *(Lady)* ×1 (71–74). Nyx: **double battle** ("two shadows"). TM79 Dark Pulse.

## Gym 17 — Gloaming (450–454) · Celestine Aubade (Fairy, :FAIRY_TALE, cap 80)
**Idea:** the keeper of the Hymn of Return. The gym is a storybook, and each room is a page with a tale's rule.
- **451 Red Path:** "never stray from the path". Only path tiles are safe; off-path = wolf trainer battle + reset.
- **452 Midnight Ballroom:** reach the stair before the clock strikes 12. A step counter (V410) allows 40 steps.
- **453 The Eight Princesses (Eeveelution Gauntlet):** 8 alcoves, each guarded by a trainer with one **Eeveelution ace** (Vaporeon … Sylveon) plus support. Beat all 8 in any order. Sylveon's alcove is last and unlocks the arena. This is the Rejuvenation-style Eeveelution gauntlet trope.
- **Trainers:** 8 gauntlet + Lady ×1 + Beauty ×1 (76–79). Celestine: single, **multi-bar boss style** (EBDX boss module) on Hard. TM21 Dazzling Gleam.

## Gym 18 — Wyrmrest (470–474) · Sigrun Ashfall (Dragon, :DRAGONS_DEN, cap 85)
**Idea:** Sigrun is Valen's chosen heir, stern, and makes you prove you choose with open eyes. The gym is a summit trial that recalls every journey skill.
- **471 Wyrm's Spine:** a field-move gauntlet (Rock Smash, Strength, Rock Climb, Waterfall) up the spire.
- **472 Statue Court:** 5 dragon statues face N/E/S/W (V385–V389). **Rotating one also rotates its two neighbours** (a ring lights-out). All 5 must face the central altar.
- **473 Magma Bridge:** lava pulses (the gym 7 timer pattern) on a narrowing bridge. Two dragon-tamer battles mid-bridge.
- **Trainers (6):** Dragon Tamer-style Cool Trainer ♂/♀ ×4, Ace Trainer ×2 (81–84). Sigrun: single, field DRAGONS_DEN. TM59 Dragon Pulse.
