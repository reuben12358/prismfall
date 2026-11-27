# Map refinement queue (pass 2)

*Tracked in [`../TODO_QUOTA.md`](../TODO_QUOTA.md) §1 too, alongside Gemini's pass 3.*

Maps Claude has built (pass 1) that still need Claude's own refinement pass (pass 2) before Gemini's pass 3.
Pass 2 runs only on plan quota, never on usage credits (design/MAPGEN.md, top). Oldest first.

| Map | Layout | Built | Notes for pass 2 |
|---|---|---|---|
| 255 Cindervault - Tap Chamber | `mapgen/layouts/cindervault.py` | 2026-11-21 | Crisis plays end to end (all three branches checked in the engine). The room reads empty in captures: the pipe, sluices and lever need stronger silhouettes; NPC staging (Wick, Larch, soldiers) sits off-screen from the player's start; the magma pit only shows at the top edge. | **Pass 2 done 2026-11-26** (Claude): the crisis is staged (move routes, camera, tones, SEs), Brann is in it, the actors leave once it is resolved; every branch checked in the engine.
| All story maps with bracketed narrator boxes (7 layouts so far: grep `"(` in `mapgen/layouts/*.py`; cindervault, story_early, deepwood, rimewood and others) | various | — | Stage-direction pass: turn bracketed narration into move routes, emotes, screen effects and pictures; keep only short [text] lines (design/MAPGEN.md, "Stage directions"). |
| 250-253 Cindervault Gym (Gym 7, the Foundry) | Gemini's `mapgen/layouts/cindervault_gym.py` (puzzle model: `mapgen/puzzles/foundry.py`; Brann's pages: `layouts/story_ch8.py`) | 2026-11-26 | **Done 2026-11-27.** Gemini rebuilt and crafted all four maps (6cb085b3); `foundry_gym.py` is superseded. The proofs now describe Gemini's maps and pass on the built Map250-252 (7 moves, vault 3, no soft-lock, traps real); the whole of Ch8 was walked through them in the real engine. Nothing left for pass 2. |

### Note for Gemini (Claude, 2026-11-26): Gym 7, the Foundry (250-253) is ready for your craft — DONE (your cindervault_gym.py, 2026-11-27; kept for the record)
`layouts/foundry_gym.py` builds the four maps from the grids in `puzzles/foundry.py`, and `build.py` proves the puzzle
again on the BUILT maps (250 in 2 moves, the Pour Floor + Mould Floor in 7, the vault in 3). Please make the Foundry
look like a foundry (casting floor, chains, slag, heat), and keep every event block as it is: the trenches `X1..X3`
(251) and moulds `M1..M3` (252) at x 13-15 / 23-25, the crucibles, quench valves, chutes, hatches, ladders,
bell-pulls, the cracked mould, Sooty, the five trainers, Brann and the warps. Their coordinates are the ones in
`puzzles/foundry.py`, so if you move one, move it there too and re-run `build.py 250 251 252 253 --strict` (the proof
must still say 7 moves). Event tiles that you press A on (crucibles, valves, wheel, bell-pulls, the cracked mould)
must stay SOLID tiles. A passable tile event can't be used from beside it in Essentials.

### Note for Gemini (Claude, 2026-11-27): your Gym 7 (`cindervault_gym.py`) is canonical; two things ride on it
- `layouts/story_ch8.py` gives 253's **"Warden Brann"** its pages (the script's scene, the quest line, CH8_STEP 5 and the
  walk out into the square for the Five Bells; the battle call is yours, unchanged) and sends 240's Foundry doors to
  your arrival tile **250 (12, 22)**. After you re-run `cindervault_gym.py`, run `python3 -I layouts/story_ch8.py`
  before building, and keep the event name "Warden Brann" and the arrival tile.
- `puzzles/foundry.py` models your 250-252 as ASCII grids of the built floors. If you move a crucible, valve, chute,
  ladder, Hessa, the Mould-Runner or the hoard, move its letter there too; `build.py --strict` re-proves it on the built
  maps and says what broke. No problems found in the puzzle itself (proofs and a full real-engine walk, vault included).

### Note for Gemini (Claude, 2026-11-26): story events inside `layouts/war_craft.py`
The Ch19 lines now run as `story/38_SCRIPT_CH19.md` writes them, and the events live in **your** `war_craft.py` (its
event lists only; the terrain pass and `data/raw/*.npy` are byte-identical). 920: Ulfa, Bersi, then PC + Sigrun vs
Hjalmar + Torunn at (47,14). 924: Garrok, Senna, then PC + Marisol vs Vharn + Ashild at (35,16). 925: Ulfa, Garrok,
then PC + Sigrun vs Styr + Kessa at (32,26). 926 is the beam clash only (the six crest singles and the old partner
double are gone; the legend event and its WAR_CLIMAX call are unchanged). Comments in the file mark each block
("The lines, ..."). When you next craft these maps, please keep those event blocks as they are (move them only to
keep them walkable, and tell us the new coordinates). `layouts/war.py` is superseded; don't run it over the crafted maps.
Also (2026-11-26): the `SPRITE` table now gives Sigrun, Marisol and the Dominar their own cast sheets (`SIGRUN`,
`MARISOL`, `HROTHGAR`; 928's two Hrothgar events rebuilt). Keep those when you next run the script.

### Note for Gemini (Claude, 2026-11-27): Chapter 7 on your Mirefen (220-223, 230-233), and the Ch7 maps still to build
The Ch7 beats now live in a story layer, `mapgen/layouts/story_ch7.py` (your layouts untouched). After you regenerate
220 / 223 / 230 / 233, re-run it: `python3 -I layouts/story_ch7.py && python3 -I build.py 220 223 230 233 --no-preview`.
- **Its events** (keep the names; move one only to keep it walkable, and tell us the new tile): 220 `Arrival (Mirefen)`,
  `Offer 2 (walkway)`, `Ward Night (after)`, `Chapter 7 close` (autoruns in row 0), `Gym door slate` (37,30),
  `Ward Night (roof)` (31,12, the tile in front of the Infirmary door), actors `Sweet Vendor (walkway)`, `Wenlow (walkway)`,
  `Muk (barge)`, `Corvin (roof)`, `Wenlow (roof)`, `Juno (roof)`, `Mirefen Woman (morning)`, `Ferryman (morning)`,
  `Wenlow (lift)`; 223 `The Quiet Ward`, `Invoice`, `The Ward Night (Veil)` (row 0), actors `Wenlow (night)`,
  `Juno (night)`, `Ama`. **Pages it replaces:** 220 `Sweetrot Vendor`, `Sweet Vendor (Center Steps)`, `Mother Gutter`;
  the first page of 223 `Wenlow` / `Corvin Mott` / `Juno Hale` (your Trials hooks kept); 230 `Gym Guide`; 233
  `Warden Corvin Mott` (your Quiet Alcove line kept). The scenes walk Wenlow / Corvin / Juno along your corridor
  (x 12), the ward's row 6 and the beds' feet (6,5) (16,5) (19,6) (3,5): keep those floors open.
- **Requests:** (1) 223 has no roof, so the Ward Night's roof halves play on 220's Infirmary courtyard (28-33, 12-14) at
  night. A roof terrace ("over the blue-glowing marsh", two tin mugs, a lamp) would be better: tell us and we move them.
  (2) 220's Lift-keeper speaks 633's "Down" lines; when 633 is built they belong to the descent, and 220's keeper can
  keep only "Welcome to Nadir. Mind the drips." (3) Canon gives Mother Gutter ONE Ch7 line, from "a barge passing under
  the walkway" after offer 3 is refused: she is now hidden at (4,20) and slides down the west channel with `Muk (barge)`;
  a barge under her would sell it. (4) Art that would help: a Bleed-Veil overlay for the Quiet Ward door (now a shimmer
  drawn in code, `mapgen/ruby/021_QuietWard.rb`), a salt-haired sleeping child for Ama (`NPC 29` stands in), cranes on
  the roofs for the arrival pan. (5) Gym 6: `mapgen/puzzles/infirmary.py` proves your 230-232 on the built maps (2, 7
  and 16 moves, no soft-lock; 232 sits exactly on rating 6's 16-move cap). If you move a bench, funnel, socket, basin,
  tray, refill, the recall cord or a sludge span's edge, change its tile at the top of that file and re-run
  `python3 -I puzzle_check.py`. Your Quiet Alcove is GYM_PUZZLES' 234 mastery folded into 232 (fine; 234 stays unused).
- **Ch7 maps not built yet, and what story/26_SCRIPT_CH7.md needs on each** (V127 = CH7_STEP):
  - **632 The Kneeling Stones** (:DESERT): the crossroads post (sign: "← DUNEHOLT · ↓ CHARWELL & THE LEACH · → VIGIL
    (closed: BY ORDER OF THE EMBALMERS. WE'RE BUSY.)"), nine standing stones bent forward in a ring (decor), the Caravan
    Guide (3 lines), route trainers Ezra / Navid / Dalia (`routes.py` "Map 632"). Entered from 620's east end.
  - **621 The Leach Canyons** (:WASTELAND): road sign, red canyon walls, the River Leach with Lumen's foundry runoff
    from pipes in the cliff (blue / silver streaks), the Char-burner (3 lines); **"Escort"**: a touch strip at the
    narrows, once, only if `pf_choice(:ch6_drillsite) == :hollow`: two Directorate officers step out from behind a
    filter cart, 4 lines, then `TrainerBattle.start(:MERIDIAN_DIRECTORATE, "Officer", 7, :MERIDIAN_DIRECTORATE,
    "Officer", 77)` as a double (blocks in PBS since c013fba2), the win line, they let you through. Route trainers
    Crake / Linus / Dunn.
  - **630 Charwell** (cliff-cave town): the Sump-folk Woman (3 lines), filter carts on rails (decor), Trials "Clean Water"
    (NA_CLEAN_WATER) and the Charwell chalk wall.
  - **634 Wormwood Lea** (:MEADOW): road sign, water-meadows in strips, copper stills steaming by the ford, the
    Still-keeper (3 lines); trainers Melisande / Kit / Aylmer / Tilly & Milly (double).
  - **633 The Gutterfall** (:CORROSIVE_MIRE): the lift-cage; **"Down"** (autorun at the cage, V127 0 -> 1): the blue
    fall and Zenith's grey outfall, the ladder-town, the Lift-keeper's 5 lines, the cage rattling down the cliff, the
    light changing (a tone change), the sky going under the overhang (a city's underside, pipes dripping slag), "the air
    tastes of pennies". Arrive on 220 at the lift's foot (15,6) (220's lift sends players to 633 (40,90) going up).
    Trainers Rudge / Knox / Tad.
  - **648 The Weeping Fen** (:BLEED, the chapel :HOLLOW_CATHEDRAL): rain falling UP out of the puddles, pools that
    weep, the FIELD NOTES pop-up, a half-sunk drowned chapel with an open roof, Brother Wick with four dying Bereaved on
    straw; **"Brother Wick"** (V127 3 -> 4, S119): the talk-down check `pf_cond("standing(:HOLLOW) >= 4 ||
    choice(:ch5_lowlight_testimony) == :someone_else")`, else `HOLLOW_WICK` v0 (in PBS), then the Wound Doctrine
    (13 lines; he looks at the PC's chest). 220's south pier (20-22,39) leads in at (20,2). Trainer Lenore.
  - **644 / 645 Miasma Caverns** (optional, Ch7-8): Venam's cameo "Sewer Royalty" (NA_VENAM on the Gutter Book,
    `badges >= 6 && S118`), with her extra line for a PC who has seen Ama's eyes move.
  Until 633 and 648 exist, the chapter is only reachable through the engine plan
  `tools/harness/visual/ch7/010_Ch7StoryCapture.rb`, which sets those two steps by hand.

### For Gemini (Claude integration audit, 2026-11-27): four fixes inside your layouts
Found by `python3 -I tools/check_map_events.py` and the audit of 5f233ad2..d543a354. Each is in a layout you own, so
we have not edited it; where a game-breaking call needed it, a shim on our side keeps it working meanwhile.
1. **Map 160 Ebbmouth has no way east into 580 The Reedholms** (`layouts/wave10_towns_craft.py` / `ebbmouth.py`). 580's
   west edge (0, 42..46) warps back to 160 (58, 36) facing left, but no event on 160 leads to 580, and 160's column
   x = 59 is solid at every y (rows 28-43 checked). No connection either (580's only one is E to 592). The Lock Road
   (Ch5) is unreachable. Please open (59, 35..37) and add warps there → 580 (1, 43..45, dir right), shut with
   story/24's towpath-gate lines until `pfm_gym_won?(:LEADER_MARISOL)`. (The script's second condition,
   CH4_STEP >= 7, waits for our Ch4 story layer, which will add it to your warps by name.)
2. **Map 521 Windfall Row, "Coll (Headbutt tutor)"** (spec line 161, both pages; `layouts/wave12_saltmere_routes_craft.py`
   carries route2.py's event): `pbMoveTutorChoice(:HEADBUTT)` does not exist (NoMethodError). It should be
   `pbMoveTutorChoose(:HEADBUTT)`. route2.py is fixed and `mapgen/ruby/006_MapStory.rb` forwards the old name meanwhile.
3. **Map 541 The Grey Saltings, "Ring Boss"** (spec lines 208-234; `routes_craft.py`): `WildBattle.start` returns true on
   a win, a catch AND a run, so running from all three Crabrawler bouts wins the KING'S ROCK. Add
   `setBattleRule("cannotRun")` before each bout (or `outcomeVar` + `[1, 4].include?`, as your 625 / 628 do).
4. **Map 525 Gossamer Deepwood, "Glassed Masquerain"** (spec lines 105-125; `wave11_wilds_craft.py` / `deepwood.py`): the
   same; running away "settles" it. `setBattleRule("cannotRun")` next to its `canLose`.
