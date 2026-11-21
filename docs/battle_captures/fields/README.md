# Field captures: the Glass Dunes stages (SPINE Revision 24)

Real-engine captures (mkxp-z 2.4.2 + Essentials v21.1 + Elite Battle: DX + the Prismfall plugins, Linux, Xvfb), shot
2026-11-21. Both sides' moves are scripted turn by turn (`tools/harness/visual/fields/005_GlassStageCapture.rb`), so
each rule fires on cue; everything else (damage, messages, the field engine, the EBDX room and its stage swap) is the
real game code. GIFs are half speed with "time skip" cards between segments; the stills are single engine frames with a
caption bar below (the frames are never retouched).

| File | What it shows |
|---|---|
| `glass_cooling.gif` | Whismur vs a wild Bronzong on **Hot Glass**. Four rounds without a damaging Fire move: "The steam is thinning..." (round 2), "The glass has almost cooled..." (round 3), then the stage swap to **Mirror Glass** (`field_glass_dunes_mirror`: clear glass, sky and cirrus reflected in the dunes, still mirror ponds, no steam) and a Mirror Glass rule: Double Team raises evasion one stage more ("images multiplied in the mirrors"). |
| `glass_cooling_key_f00150.png` ... `_f00820.png` | Hot Glass at the start, the two cooling messages, the swap to Mirror Glass, Double Team. |
| `glass_sound_shatter.gif` | Whismur's Boomburst vs a wild Snorlax on **Mirror Glass**: "Boomburst set the glass ringing!", "The glass cracked! (2 more and it breaks apart)", shards hit the grounded foe and stay as broken glass on its side (an entry hazard); the second crack; the third Boomburst breaks the glass apart and the battle is back on the **Desert**. |
| `glass_sound_shatter_key_f00140.png` ... `_f00770.png` | The ringing, crack 1, the shards, the broken glass left on the ground, the third Boomburst, the Desert. |

Rules: `design/FIELDS.md` (Glass Dunes) and `design/FIELD_LOGIC_AUDIT.md`. Headless checks of the same rules (cooling,
sun and rain, reheating, sound cracks, cracks carried across the cooling, annealing, broken glass on switch-in, Rapid
Spin, insulation, ricochet): `tools/harness/field_checks.rb`, run by `run_all.rb` section 4.

Rebuild:
```bash
RUN=/home/claude/run_flcap bash tools/harness/visual/fields/run_glass_stages.sh assemble   # capture copy (~800 MB)
python3 -I tools/harness/visual/make_gif.py $RUN/frames/gs_cool docs/battle_captures/fields/glass_cooling \
  --ranges 140-175,355-400,525-565,655-760,800-850 --step 2 --ms 200 --title "..." --caption "..." --key IDX:"..."
python3 -I tools/harness/visual/make_gif.py $RUN/frames/gs_shatter docs/battle_captures/fields/glass_sound_shatter \
  --ranges 125-290,400-560,660-800 --step 2 --ms 200 --title "..." --caption "..." --key IDX:"..."
```
Frame indices are dump indices (every 3rd engine frame). The capture copy and its frames were deleted after the GIFs
were built.

Not shown here: the stage swap uses EBDX's colour fade (a short flash), not a staged transition like the flood/desert
-> glass one; Windows / real GPU not verified.
