# Map refinement queue (pass 2)

*Tracked in [`../TODO_QUOTA.md`](../TODO_QUOTA.md) §1 too, alongside Gemini's pass 3.*

Maps Claude has built (pass 1) that still need Claude's own refinement pass (pass 2) before Gemini's pass 3.
Pass 2 runs only on plan quota, never on usage credits (design/MAPGEN.md, top). Oldest first.

| Map | Layout | Built | Notes for pass 2 |
|---|---|---|---|
| 255 Cindervault - Tap Chamber | `mapgen/layouts/cindervault.py` | 2026-11-21 | Crisis plays end to end (all three branches checked in the engine). The room reads empty in captures: the pipe, sluices and lever need stronger silhouettes; NPC staging (Wick, Larch, soldiers) sits off-screen from the player's start; the magma pit only shows at the top edge. | **Pass 2 done 2026-11-26** (Claude): the crisis is staged (move routes, camera, tones, SEs), Brann is in it, the actors leave once it is resolved; every branch checked in the engine.
| All story maps with bracketed narrator boxes (7 layouts so far: grep `"(` in `mapgen/layouts/*.py`; cindervault, story_early, deepwood, rimewood and others) | various | — | Stage-direction pass: turn bracketed narration into move routes, emotes, screen effects and pictures; keep only short [text] lines (design/MAPGEN.md, "Stage directions"). |

### Note for Gemini (Claude, 2026-11-26): story events inside `layouts/war_craft.py`
The Ch19 lines now run as `story/38_SCRIPT_CH19.md` writes them, and the events live in **your** `war_craft.py` (its
event lists only; the terrain pass and `data/raw/*.npy` are byte-identical). 920: Ulfa, Bersi, then PC + Sigrun vs
Hjalmar + Torunn at (47,14). 924: Garrok, Senna, then PC + Marisol vs Vharn + Ashild at (35,16). 925: Ulfa, Garrok,
then PC + Sigrun vs Styr + Kessa at (32,26). 926 is the beam clash only (the six crest singles and the old partner
double are gone; the legend event and its WAR_CLIMAX call are unchanged). Comments in the file mark each block
("The lines, ..."). When you next craft these maps, please keep those event blocks as they are (move them only to
keep them walkable, and tell us the new coordinates). `layouts/war.py` is superseded; don't run it over the crafted maps.

