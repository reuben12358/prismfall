# Puzzle rooms in the real engine (puzzle engineer, 2026-11-19)

Real mkxp-z frames (Linux, Xvfb), captured by the dev-only bot (`tools/harness/playtest/002_PuzzleBot.rb`, ordinary input
only) in a private game copy; media made by `make_puzzle_media.py <session> --step 4 --ms 200` (slow: about real speed;
battles cut, a card between rooms; `--skip-maps` drops the bot waiting in the town outside).

| Files | What |
|---|---|
| `gym1_*`, `gym1_solve.gif` | Gym 1, the Pell Playhouse (art pass): lobby, the Field Notes pop-up, both aisle actors, the curtain rope, the painted drop, Dorian |
| `gym1_house_empty_good_full.png`, `gym1_house_battle_starts.png` | SPINE Rev 19: the house with 0 / 7 / 21 Saltmere townsfolk met; Dorian's show opening at stage 1 / 2 / 3 |
| `gym2_*`, `gym2_solve.gif` | Gym 2 redo (SPINE Rev 19): the weavers' lobby, then the Canopy: web trampolines, a web onto a web, sticky webs, two Joltik, Tamsin |
| `d2_*`, `d2_solve.gif` | D2 the Deepwood's lantern hollow: one-way silk, post α outside, post β inside, TM19 |
| `d7_*`, `d7_solve.gif` | D7 the Rimewood's Frost Loom: left + right thread, the trapper's cache |
| `artpass_gym1_*.png` | Gym 1 before / after the art pass |
| `artpass_gym2_*.png` | Gym 2 before / after the art pass **of the Weaving Hall, which SPINE Rev 19 then replaced** (kept for the record) |

Re-run: `bash tools/harness/playtest/run_puzzles.sh assemble|install|gym1|gym2|house0|house7|house21|d2|d7` (set `RUN` to
your own folder if someone else is using the rig).
