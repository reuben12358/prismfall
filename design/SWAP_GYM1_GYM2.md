# SWAP_GYM1_GYM2 — Saltmere first, Briarwick second (SPINE Revision 14): the checklist by owner

Owner of this file: story editor. Status checked against the working tree on **2026-11-19, 11:20**. Several workstreams were
already part-way through the swap when this was written; each item is marked **✓ done** (seen in the tree), **To do**, or
**Confirm** (done, but it disagrees with another workstream).

**⚠ Urgent (build-breaking, found 11:38): `mapgen/layouts/story_early.py` line 306 no longer parses.** The 11:33 run of
`tools/rename_places.py --apply` rewrote the old route number in `'… old orchard on [route].'` as `'… on the Ferrymen's Mile.'`, and the apostrophe ends
the single-quoted string (SyntaxError, so `build.py` cannot import the layout). It is the only Python file broken
(all of `mapgen/layouts/*.py`, `mapgen/*.py` and `tools/trainer_gen/*.py` were scanned). The line is also wrong in content:
the orchard is on Windfall Row. Fix: `QUEST('biscuit', 'Biscuit', "Go with Juno to the old orchard on Windfall Row."),`.
**Cartographer:** `rename_places.py` should escape or skip names containing `'` (Ferrymen's, Dyers', Spinners', Hale's)
inside single-quoted Python strings.

**Three rules for everyone**
1. **Nothing renumbers.** Map IDs, switch and variable IDs and names, trainer IDs and versions, choice keys and puzzle
   blocks all stay as they are. Saltmere keeps block 140–159 and Briarwick keeps 120–139. `CH2_*` switches now mean
   Chapter 3 and `CH3_*` switches Chapter 2 (FLAGS.md header). `:ch3_juno_talk` is a Chapter 2 choice; `:ch2_tamsin` and
   `:ch2_matriarch` are Chapter 3 choices (NARRATIVE_KEYS §4).
2. **Look a Warden up instead of hard-coding the gym number.** Use `Prismfall.gym_battle(pfm_gym(:LEADER_DORIAN))` and
   `pfm_gym_won?(:LEADER_TAMSIN)` (`mapgen/ruby/008_GymOrder.rb`). Never write `$player.badge_count >= 1` to mean
   "after Tamsin": the player reaches Briarwick holding Dorian's badge.
3. **`segment` in maps.json sets the level cap, not the map ID.** For the Act I maps the ID no longer tells you the badge
   count.

---

## 0. The new order

| Gym | Town | Warden | Type · field | Cap | Battle | Chapter | Gym rooms | Puzzle block | Badge · TM |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Saltmere | Dorian Pell (`LEADER_DORIAN`) | Normal · `:GRAND_STAGE` | 15 | **single** | Ch2 "Curtain Call" | 150 Lobby, 154 Auditorium (door on Old Town 147). Optional Backstage 151–153 (D9), after Badge 2 | 310–314 (Playhouse) | Footlight Badge · TM42 Facade · gift Eevee "Understudy" (S110) |
| 2 | Briarwick | Tamsin Loom (`LEADER_TAMSIN`) | Bug · `:SILKWOOD` | 19 | **double** | Ch3 "The Weaver's Debt" | 130 Foyer, 131 Weaving Hall. Optional Upper Lofts 132/134, after Badge 2 | 305–309 (Loomhouse) | Weft Badge · TM89 U-turn · then HM01 Cut from the Cutter |

**Story order** (scripts: `story/20_SCRIPT_CH0-2.md` and the new `story/21_SCRIPT_CH3.md`; outline: `story/04_ACT_I.md`)
- **Ch1:** Ferrow's Landing → the Ferrymen's Mile → Windfall Row → the Glassed Orchard. The forest road north from Windfall Row into the Gossamer is corded off.
- **Ch2:** stile send-off → the Hale Bell (quarantine guard) → Lacecliff Walk → Marram Down → Saltmere East Gate → **J1** on the promenade green (before the gym) → Gym 1 (Juno in the stalls; the badge case hums one note) → Understudy → rehearsal (Tree #3) → breakwater (`:ch3_juno_talk`) → the Pageant: Mourner, grunt double battle (`HOLLOW_GRUNT_*` v0), Vesper (S190) → Dorian's dressing room (Gilded King prologue) → Kestrel → royal notice → North Gate opens (S108) → V102 = 3.
- **Ch3:** the Grey Saltings (Brinecut: TM98 handed over) → the Dyers' Ford (survey flags) → Thistledown Lea (Thistledown Manor, `GO_CURTAIN_CALL`) → Gossamer Wood (from the west) → Briarwick → Thistle at night (S106) → Gym 2 (Juno arrives after Bram; a second note, a chord) → confession (`:ch2_tamsin`) → Cutter gives Cut → Deepwood → Shelly (optional) → Cocoonfall Hollow, the Matriarch (`:ch2_matriarch`, S107, V105 = 1; the forest-road cordon lifts) → charcoal child → V102 = 4.
- **Ch4:** Briarwick North Gate → Spinners' Rise → Frostwick Pass → Frostwick → Rimewood Path → the Rimewood → Gullcry Cliffs (K2) → Ebbmouth. The Frostflat Causeway is the side road from Frostwick back to Saltmere.

**Map by map** (segment = badges held when the map is first reachable; cap follows from it)

| Map | Name (world_data) | Road · role | Segment / cap | Chapter | Note |
|---|---|---|---|---|---|
| 100–110, 520, 523 | Ferrow's Landing, Ferrymen's Mile, Hale Farmhouse | Road 1 | 0 / 15 | Ch1–2 | unchanged |
| 521 | Windfall Row | Road 1 branch | 0 / 15 | **Ch1** | keeps Ch1 trainers (Wim, Ada, 6–7). Its W forest road to 524 is corded |
| 522 | The Glassed Orchard | Road 1 branch | 0 / 15 | Ch1 | unchanged |
| 527 | Lacecliff Walk (**new**) | Road 1 | 0 / 15 | Ch2 | |
| 528 | Marram Down (**new**) | Road 1 | 0 / 15 | Ch2 | |
| 140–147 | Saltmere (and 146, 147) | Gym 1 town | **0** / 15 | Ch2 | was segment 1 |
| 150, 154 | Pell Playhouse Lobby, Auditorium | Gym 1 | 0 / 15 | Ch2 | |
| 151–153 | Playhouse Backstage (D9) | optional | **2** / 23 | after Badge 2 | was segment 1 |
| 541, 542, 544, 545 | Grey Saltings, Brinewife's Rest, Brinecut Mine | Road 2 | 1 / 19 | Ch3 | unchanged segment, new chapter |
| 552 | The Dyers' Ford (**new**) | Road 2 | 1 / 19 | Ch3 | |
| 540, 546, 547 | Thistledown Lea, Thistledown Manor | Road 2 | 1 / 19 | Ch3 | unchanged segment |
| 524, 526 | Gossamer Wood, Woodward's Hut | Road 2 | **1** / 19 | Ch3 | was segment 0 |
| 120–125 | Briarwick | Gym 2 town | **1** / 19 | Ch3 | was segment 0 |
| 130, 131 | Loomhouse Foyer, Weaving Hall | Gym 2 | **1** / 19 | Ch3 | was segment 0 |
| 132, 134 | Loomhouse Upper Lofts | optional | **2** / 23 | after Badge 2 | |
| 525 | Gossamer Deepwood | side of 524 (Cut) | **2** / 23 | Ch3, after Badge 2 | was segment 1 |
| 548 | Cocoonfall Hollow | side of 525 | **2** / 23 | Ch3, after Badge 2 | was segment 1 |
| 566, 577, 578 | Spinners' Rise, Frostwick Pass, Rimewood Path (**new**) | Road 3 | 2 / 23 | Ch4 | |
| 560, 568 | Frostflat Causeway, The Rehearsal | Road 3 side road | 2 / 23 | Ch4 | 560 is a side road now |
| 570–576, 562, 563, 561, 564, 565 | Frostwick, Rimewood, Gullcry | Road 3 | 2 / 23 | Ch4 | unchanged |

---

## 1. Map builder

### 1A. Route connections and warps (which town connects to which)
`maps_out/PBS/map_connections_prismfall.txt` and maps.json `connections` are still pre-swap. **To do:**
- **520 Ferrymen's Mile:** new **W exit at the Hale Bell → 527**. Move the quarantine roadblock ("Accord guard" and "Accord guard (aside)", lifts on S105) here from 521.
- **521 Windfall Row:** the W forest-path warp `R2_WOOD` ↔ 524 stays, but becomes the **corded forest road**: a "Forest-road cordon" event that blocks it from this side always, and from 524's side until `V105 BRIARWICK_GLASSWOOD >= 1`. Move the old Chapter 2 events on this map to 552: the survey flags, the Meridian Surveyor, "Juno flags 1–3" and the Antidote at the third flag. Keep the hay-cart driver, using the new line in the script. Replace the old "… Briarwick ahead" road sign with the Windfall Row sign.
- **527 Lacecliff Walk (new):** E ↔ 520, W ↔ 528.
- **528 Marram Down (new):** E ↔ 527, W ↔ **140 East Gate** (new edge on Saltmere).
- **140 Saltmere:** keep N → 541 as the **North Gate**, closed until S108 (a "Gate Warden" event; script, Chapter 2 close). Keep W → 560 as the **West Gate**: the Frostflat Causeway is chained at the Border Stones until the player reaches Frostwick.
- **541 Grey Saltings:** S → 140 is kept. Change **N → 540** to **N → 552**.
- **552 Dyers' Ford (new):** S ↔ 541, N ↔ 540.
- **540 Thistledown Lea:** connect to 552 (replacing the 541 edge) and add **E ↔ 524 (the Gossamer's west eaves)** in place of **E → 120**. **Remove the `R3_COCOON` warp to 548**: Cocoonfall is entered only through the Deepwood. Keep `R3_MANOR` and the Brinecut back door `R3_MINE`.
- **524 Gossamer Wood:** new **W edge ↔ 540**. Keep N → 120 and the E Cut tree → 525 (Cut now comes after Badge 2). The S warp to 521 is the corded road above.
- **120 Briarwick:** remove W → 540 and add a **North Gate → 566**. Keep the S warp from 524 (`WOOD_BRIAR`).
- **566 Spinners' Rise (new):** S ↔ 120, N ↔ 577. **577 Frostwick Pass (new):** ↔ 566, W ↔ **570 East Gate**.
- **570 Frostwick:** E edge → **577** (it was 560). Add a **S gate ↔ 560**. N edge → **578** (it was 562).
- **578 Rimewood Path (new):** S ↔ 570, N ↔ 562. **562 Rimewood:** S ↔ 578 (it was 570).
- **560 Frostflat Causeway:** the Saltmere end ↔ 140 W is kept. The other end ↔ **570 S gate** (it was 570 E). Put the chain at the Border Stones so it opens from the Frostwick side. The Rehearsal spur (568) is unchanged.

### 1B. Gym 1/2 map IDs
**Not renumbered.** Gym 1 is the Pell Playhouse: 150 + 154, the door on 147, Backstage 151–153 behind `pfm_gym_won?(:LEADER_TAMSIN)`. Gym 2 is the Loomhouse: 130 + 131, Upper Lofts 132/134. Puzzle switches follow the building (305–309 Loomhouse, 310–314 Playhouse).
**✓ done:** `gen_playhouse.py` and `gen_loomhouse.py` call `gym_battle(pfm_gym(...), double: false/true)` and `award_badge(pfm_gym(...))`, and specs 130 and 150 are regenerated. **To do:** update the MAPGEN.md table (rows 120–154 still describe the old order).

### 1C. Event scripts in specs and layouts (re-pour from the two scripts)
- **"After Tamsin" tests**, `$player.badge_count >= 1` → `pfm_gym_won?(:LEADER_TAMSIN)` and `== 0` → `!pfm_gym_won?(:LEADER_TAMSIN)`:
  `specs/120_briarwick.yaml` 96, 119, 569, 578, 698, 741 · `specs/121_briarwick_interiors.yaml` 3078, 3125, 5242 · `layouts/story_early.py` 704, 707, 771, 794, 848, 865. Covered by this: the S170 Celestine shrine, the Cutter's HM01, Hett's after-gym line, the village variants and the loft-manager guard on `:ch2_tamsin`.
- **Saltmere:** `specs/141_saltmere_interiors.yaml` 64 `!Prismfall.has_badge?(2)` → `!pfm_gym_won?(:LEADER_DORIAN)`; line 85 sets `STORY_CHAPTER 4` at Saltmere's close → **3**.
- **Chapter numbers:** `story_early.py` 782 and `121_briarwick_interiors.yaml` 807 set STORY_CHAPTER 3 at Briarwick's close → **4**. Page conditions on `STORY_CHAPTER 2` in 121 (6282) → **3**.
- **Brinecut:** `specs/544_brinecut_mine.yaml` 27 `Prismfall.has_badge?(2)` → hand TM98 over on `pfm_gym_won?(:LEADER_DORIAN)`. It is usable from Badge 2 (`BADGE_FOR_ROCKSMASH` stays 2; script, Ch3).
- **Send-off text:** `story_early.py` 429–432 (Larch/Juno "Briarwick! Silk-moth eggs! A GYM!") and `layouts/route1.py` 136–141 (the Chapter 2 opener: "Briarwick's first…", the quest line) → re-pour from `20_SCRIPT` "Chapter start". Saltmere is first, and Juno is going for the Pageant tarts.
- **Counting rhyme:** `layouts/ferrow_events.yaml` 147–149 and `specs/100_ferrows_landing.yaml` 1106/1125 → "One for the stage and two for the weave, / three for the river that won't take its leave".
- **Gossamer Wood** (`layouts/gossamer.py`): the map is entered from the west now. Kestrel's line at 159 ("Briarwick's just ahead") can stay, since he is a day ahead of the PC in Ch3, or go. The Twins Mo & Jo double is the warm-up for Tamsin's doubles.
- **Pell Playhouse** (`gen_playhouse.py`): use the script's Gym 1 lines (Juno appears in the stalls after the first actor; the hum; Facade; level nineteen; Understudy). **Replace the lobby poster "THE GILDED KING — closed by order of the Crown / TONIGHT"**: it gives away the dressing-room reveal. Use the script's pasted-over "...ED K..." poster instead.
- **Loomhouse** (`gen_loomhouse.py`): its win lines are still the old Gym 1 ones (one note; "level nineteen"; "you may use Cut"). Use the script's Gym 2 lines: the chord, "level twenty-three", Cut from the Cutter, Juno with the hatbox after Bram, and Tamsin's extra confession lines ("And it WORKS…", "The man in Saltmere told everyone to ask their Warden…").
- **Thistle:** the event uses version 0 (REQUESTS item 4). There are new lines about the shears and the Lantern Theatre, and she exits north.
- **New events:** all of 527, 528 and 552; Saltmere's new NPCs, sidequests, prop room, costumier, Inspector and Gate Warden; the Thistledown Manor scenes (546/547); and Juno as a placed follower from 520 to 140 (Ch2) and from 140 to 120 and Cocoonfall (Ch3).
- **✓ done (story editor):** `layouts/scriptpour.py` reads `story/20_SCRIPT_CH0-2.md` and then `story/21_SCRIPT_CH3.md`. `story_early.py`'s Briarwick townsfolk parse (`^### Flavor townsfolk$`) now finds its section in the Chapter 3 file. The import was checked: 17 Briarwick townsfolk, 14 Saltmere townsfolk (header `### Flavor townsfolk (Saltmere …)`, which matches neither old pattern).

## 2. Puzzle engineer
- **✓ done:** GYM_PUZZLES §0b and the Gym 1/2 sections. The theater is Gym 1 (1/10: the aisle, three actors, one curtain rope) and the Weaving Hall is Gym 2 (3/10: linked heddles, each lifting two beds). The revolving stage survives as D9 Backstage after Badge 2.
- **To do (DUNGEON_PUZZLES stale lines):** D2 "before / after Gym 1" → Gym 2. Line 88 "after Badge 1 and Cut" → after Tamsin's badge. Line 101 "Shuttle, from Tamsin after Badge 1" → after Badge 2. Line 103 "the coupling is Gym 1's" → Gym 2's. Line 136 "the salt miner gives TM98 after Badge 2" → handed over at Badge 1, usable at Badge 2. Lines 188/193, the Rimewood frozen heddle "callback to Gym 1" → Gym 2. D5 Thistledown is on the Ch3 road (cap 19).
- **Story conflict, D9 reward** (lines 235, 340): "the Gilded King's annotated script" and "the prop crown of the Gilded King". Dorian owns the *last* copy of "The Gilded King", has never staged it, and hands over only the prologue page (Ch2); the full play is staged at the Festival. Suggested reward: the Pageant's prompt-book with every line about the old capital struck out in red, or the old Crown prop with its original *whole* stone (a nice match for Saltmere's prop-room scene, Crown seed 2).
- Gym 1 has to teach fields gently: the Field Notes pop-up text in 154 is in the script, and Juno's cheering from the stalls is part of the joke.

## 3. Trainer designer
- **✓ done:** Core `GYMS` (Dorian 1, cap 15, `double: false`; Tamsin 2, cap 19, `double: true`) and `gym_battle` honouring it. BALANCE §4 rows, class row and bar 1 (Normal/Bug/Water). `validate_trainers.py` WARDENS swapped. J1 at 14. Thistle at 16–18. Shelly v1 at 21. The playbook's Gym 1/2 sections.
- **Confirm the stretch of each map** in `tools/trainer_gen/routes.py` `PLAN`; the §0 table is final:
  - **521 stays Chapter 1, cap 15.** PLAN shifts it +9 to cap 19; Windfall Row is walked in Ch1 to reach the Glassed Orchard, so keep Wim/Ada at 6–7.
  - **541, 544, 545 are Road 2, cap 19** (PLAN has them at cap 15 as "the coast road"; the cartographer's coast road is 527/528). The TRAINER_FIELD_PLAYBOOK §2 rows for 541/544/545 say "Gym 1" → Gym 2 stretch. BALANCE 4b's level line moves with them.
  - **New maps 527/528 are cap 15** (8–12, Strand Road). **552 is cap 19.** **566/577/578 are cap 23.**
  - **151–153 Backstage are cap 23** (optional, after Badge 2), not cap 15. **132/134 Upper Lofts are cap 23.**
  - 154 actors (Florian, Rosalind, Ambrose) are cap 15 at 10–13. 130/131 (Nell, Orla, Bram) are cap 19 at 15–17. 145 Pageant grunts v0 and **Vesper/Carol v0** fight after Gym 1, cap 19. 525 Deepwood is cap 23.
- **Glass Matriarch** (`mapgen/bosses.yaml`, BOSSES.md): it is fought after Gym 2, so Lv 16 → about 20 (cap 23). The script wants **2 bars** with a Silkwood-borrow at the break; the yaml has 3 on Standard (REQUESTS item 9).
- **J1:** before Gym 1, on `:MEADOW`, promenade green. SPINE's rival slot line still says "J1 Gym 2 arc" (see §9).
- **Fighting answers for Gym 1** are thin on the Strand Road (see §8): Dorian's team should not assume the player has one.

## 4. Playtest
- **To do:** `tools/harness/playtest/001_PlaytestBot.rb` `PLAN` stops at Briarwick. New path after the orchard: `[:to, 521, 520]`, send-off, `[:to, 520, 527]`, `[:to, 527, 528]`, `[:to, 528, 140]`, J1 on the green, `[:to, 140, 147]`, `[:to, 147, 150]`, `[:to, 150, 154]` (curtain rope, Dorian), the Lantern Theatre 145 (rehearsal; Pageant: the grunt double), 146 breakwater (`:ch3_juno_talk`), back to 140 (Kestrel, the notice, the North Gate), `541 → 552 → 540 → 524 → 120`, Thistle, `130 → 131` (Tamsin, double), the confession, 125 Cutter, `524 → 525 → 548` (Matriarch), the 120 close. Drop `[:to, 521, 524]` (the forest road is corded until V105 ≥ 1). `[:goto, 521, "Juno flags 1"]` moves to 552.
- **✓ done:** `002_PuzzleBot.rb` sessions gym1 (147 → 150 → 154) and gym2 (120 → 130 → 131), and the backstage session.
- **Checks to add:** the badge case plays one note after Gym 1 and two after Gym 2. Briarwick's after-gym lines do *not* fire on arrival with Dorian's badge (the badge_count bug in §1C). The North Gate stays shut until S108. Run `python3 -I tools/validate_map_trainers.py` after the rebuild.

## 5. Cartographer
- **✓ done:** `tools/worldmap/world_data.py`: Road 1 The Strand Road (520 → 521 branch, 527, 528), Road 2 The Weavers' Road (541, 552, 540, 524), Road 3 The Hoar Road (566, 577, 578, 562, 561; 560 as side road). Town positions. `CITY_ORDER`. WORLD.md §11 is generated. maps.json segments for Saltmere (0), Briarwick, 524 and the Loomhouse (1).
- **To do (maps.json):** segments **525 and 548 → 2** (only reachable after Tamsin's badge: Cut plus the shuttle). **151–153 and 132/134 → 2.** Drop 548 from 540's `side` list, since Cocoonfall belongs to 524/525. Rewrite `connections` per §1A (still pre-swap for 120, 140, 540, 541, 560, 570, 562; empty for the new maps). The Handfast Arch on 577 now also carries the bolted Meridian sunburst (the Ch4 border beat; the Border Stones stay on 560).
- **Names:** the scripts already use the world_data names (the Ferrymen's Mile, Windfall Row, Lacecliff Walk, Marram Down, the Grey Saltings, the Dyers' Ford, Thistledown Lea, Gossamer Wood, Spinners' Rise, Frostwick Pass, Rimewood Path, the Frostflat Causeway). Saltmere's gates are East (from Marram Down), North (to the Saltings) and West (to the Causeway); Briarwick's North Gate leads to Spinners' Rise.

## 6. Field defaults
- **✓ done:** FIELD_DEFAULTS.yaml has the new maps (527, 528 Beach; 552, 566 Meadow; 577 Snowy Mountain; 578 Silkwood).
- **To do:** in `exceptions.trainers`, the `why` text for OCTAVE_VESPER v0 and OCTAVE_SINGER v0 says "Ch3" → **"Ch2"**. Then regenerate `plugins/Prismfall Field Effects/011_FieldEffects_MapDefaults.rb` (its comments at 644–649 say Ch3) and `maps_out/Plugins/Prismfall Maps/002_MapFields.rb`. J1 stays `:MEADOW`, Thistle Silkwood (120 default), the Pageant grunts and Vesper Grand Stage (145 default).
- **Grand Stage is the first gym field.** Check that its intro message and Field Notes entry teach it in one line (the script's pop-up: "the audience reacts…"). The route fields before it are Meadow and Beach, both mild.

## 7. Event scripts and plugin code (Core, Debug Tools, Maps plugin)
`grep -rn "gym_battle(1)\|gym_battle(2)\|award_badge\|badge_count" plugins/` found no gym-1/2 literals left. Gym events live in mapgen (§1C).
- **✓ done:** Core `001_Config.rb` GYMS and `003_Badges_Gyms.rb` `gym_battle` (trainer workstream). Core `012_Narrative_Data.rb` (story editor): `WARDEN_CONSENT` rows 1–2 swapped to Dorian, then Tamsin, to match GYMS, and the three choice descriptions corrected. Keys are unchanged and `ruby -c` is OK. Run the Debug narrative check (`024_NarrativeCheck.rb`) once in the engine.
- **To do, Core `001_Config.rb` `FIELD_MOVE_BADGES`:** `:CUT => 1` → **2**, comment "HM01, Briarwick Cutter's House, after Tamsin's badge" (WORLD §4). With count gating this only matters if Cut can come from anywhere else, but it keeps the table honest. `:ROCKSMASH => 2` stays; change its comment to "handed over at Badge 1".
- **To do, `plugins/Prismfall Debug Tools/001_Prismfall_DebugMenu.rb` lines 13–14:** the fallback gym table still lists Bug/Tamsin/15 first. Swap to `[:NORMAL, "Dorian", :LEADER_DORIAN, :GRAND_STAGE, 15]`, then `[:BUG, "Tamsin", :LEADER_TAMSIN, :SILKWOOD, 19]`.
- **Switches and variables:** none renamed, `maps_out/Data/system_prismfall.txt` unchanged. Only FLAGS.md descriptions changed.
- **Validators:** `validate_encounters.py` `segment_from_id` is the fallback for maps missing from maps.json. It would put 120–139 at segment 0 and 140–159 at 1, the old order. Either special-case the two blocks or make sure every Act I map is in maps.json (it reads `segment` first). `UNLOCK["RockSmash"] = 2` is unchanged.
- **✓ done (story editor):** `tools/build_codex.py` adds `story/21_SCRIPT_CH3.md` as "Script: Chapter 3" and puts Saltmere first in the prism's gym list. It rebuilds (19 chapters).

## 8. World lead (encounters and availability)
- **An honest answer to a Normal gym at 0 badges.** The Strand Road (520, 527, 528) has Rock (Rolycoly, Nacli, Dwebble) and a Ghost (Sandygast), but no Fighting-type, and the Gym Guide's line is "Fighting-types, they fear". Add one Fighting family before Saltmere: Crabrawler in Lacecliff Walk's rock pools, or Mankey on Marram Down.
- POKEMON_AVAILABILITY: "after B2 · Saltmere (Eevee breeder)" and "Saltmere playhouse (stage magician) Abra" → **after B1**. The 0-badge note "Litleo/Sizzlipede/Rolycoly/Fletchling for Gym 1" are Bug answers, so they are now the Gym 2 answers.
- Encounter levels move with segment: 524 Gossamer Wood goes from 0 to 1, Saltmere's rod tables from 1 to 0, 525 and 548 from 1 to 2. 541–547 keep segment 1.
- **✓ done (story editor):** WORLD.md §1 schematic numbers, §2 Revision 14 note, §3 segment rows 0–2, §4 Cut/Rock Smash, §6 gym TMs (1 Facade, 2 U-turn), §7 Act I chain and layouts, §10 leg table and borderland A. §11 is the cartographer's generated block and was not touched.

## 9. Coordinator (SPINE)
- SPINE's LOCKED gym table (rows 1–2) and "Rival battle slots" ("J1 Gym 2 arc") still show the pre-swap order. Revision 14 at the top supersedes them, and story didn't edit SPINE. Suggested rows: `| 1 | Normal | Saltmere | Dorian Pell | :GRAND_STAGE | 15 |`, `| 2 | Bug | Briarwick | Tamsin Loom | :SILKWOOD | 19 |`, and "J1 Gym 1 arc (Ch2, Saltmere, before the gym)".

## 10. Story (✓ done, for reference)
- `story/04_ACT_I.md`: Act I rewritten for the new order. Ch2 "Curtain Call" (the hook: the Mourner asks the city), Ch3 "The Weaver's Debt" (the answer, in one village), Ch4's route and K2, and an escalation note at the top.
- `story/20_SCRIPT_CH0-2.md`: Prologue and Ch1 touch-ups (Ever-Bloom Juno, Rowan's Saltmere clue and wreath touch, the new rhyme, road names), and the **new Chapter 2 script** (Strand Road, Saltmere, Gym 1, J1, breakwater, Pageant, Vesper, dressing room, Kestrel, close).
- `story/21_SCRIPT_CH3.md` (**new**): the Briarwick material, revised for Gym 2 (double, cap 19, the chord, Cut after Tamsin), plus the Weavers' Road (Saltings, Brinecut, Dyers' Ford, Lea, Thistledown Manor).
- 00, 01 (Gym 1 Saltmere, Gym 2 Briarwick, the rhyme), 02, 03 (Dorian #1 and Tamsin #2 swapped and revised; Juno is Ever-Bloom; Thistle), 05, 06, 08 (procession and bar order), 09 (seeds re-sequenced), 10, 11 (rows 1–2 swapped), 15 (Ch2 Tree #3, Ch3 Apology Spiral); design/NARRATIVE_KEYS, FLAGS, CAMEOS (Shelly after Gym 2, ~21).
- Art (parked by Revision 15): CHARACTER_ART's JUNO row still describes the kerchief look. Story text now follows Ever-Bloom; the art row can wait.
