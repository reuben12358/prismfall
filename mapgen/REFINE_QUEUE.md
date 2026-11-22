# Map refinement queue (pass 2)

Maps Claude has built (pass 1) that still need Claude's own refinement pass (pass 2) before Gemini's pass 3.
Pass 2 runs only on plan quota, never on usage credits (design/MAPGEN.md, top). Oldest first.

| Map | Layout | Built | Notes for pass 2 |
|---|---|---|---|
| 255 Cindervault - Tap Chamber | `mapgen/layouts/cindervault.py` | 2026-11-21 | Crisis plays end to end (all three branches checked in the engine). The room reads empty in captures: the pipe, sluices and lever need stronger silhouettes; NPC staging (Wick, Larch, soldiers) sits off-screen from the player's start; the magma pit only shows at the top edge. |
