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

