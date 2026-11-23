# Chapter density standard (adopted 2026-11-22)

Source: `gemini_recommends/2026-11-22_bigjra-chapter-density-benchmark`. It benchmarks Prismfall against the BigJRA 100% guides for Reborn, Rejuvenation and Desolation. Act I (Ch0–4) is the reference slice. Every chapter from Ch5 on is brought up to it.

## Per-chapter floor (every script from Ch14 on is written to this; Ch5–13 get it as retrofit passes)
| Item | Floor |
|---|---|
| Route, gym and dungeon trainers | 12–20 (a PBS block per trainer, with the 3 difficulty versions) |
| Story, boss and rival fights | ≥ 4 |
| EventMons (gift, static, trade, weather/time-gated) | ≥ 3 |
| Optional hangouts and town banter (`pf_hangout`) | 2–4 |
| Glassfall Slivers (100 total) | 4–6 |
| Trial quests wired (no stubs on built maps) | ≥ 3 |
| Badge-tier encounter overlay | one per new badge |
| Optional mini-dungeon | where the benchmark table lists one (Ch7, 12, 13, 16, 19) |

The script's own "Density" section lists these, so map and PBS agents can build straight from it.

## Systems adopted
- **Glassfall Slivers:** 100 hidden shards, exchanged at Larch's Lab and Lumen Arcade at 10/25/50/75/100 for stones, seeds, mints, Ability Patch, and an EventMon. They fit the lore: they are shards of the same Glassfall the scar answers to.
- **Velmora Trading Chain**, 6 steps: Ch2 → 5 → 8 → 12 → 16 → 20.
- **Mystery Egg** in Briarwick (Ch3), from 12 curated lines.
- **World Refresh Waves** at Badges 4, 8/9, 13 and 16, plus `encounters_badgetiers.txt` overlays for Badges 5–18.
- **Lumen Grand Arcade floor passes** and the Battle Pavilion (940), shared with CODEX_SPEC.
- **Economy:** as already decided in the Wednesday audit (stone/evo clerk, seeds, EXP Share, Relearner in Saltmere and Lumen).

## Not adopted as written
- "Imprint Relics" (Crest clones): deferred. Megas, Z-moves and fields already carry the buff layer, and a fourth species-specific power system dilutes them. Revisit after Ch21.
- Grade letters stay in the benchmark doc. The floor above is the working target.
