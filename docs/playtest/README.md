# First playable build: real-engine playtest (2026-11-17, Chapter 1 added 2026-11-18)

**These are real game frames.** The engine is mkxp-z 2.4.2, built from source on Linux. Each PNG is unmodified output
of the engine's own `Graphics.screenshot`. The only additions are the caption strip below each frame and, in the GIF,
black "time skip" cards between trimmed segments.

## What was tested
1. A fresh copy of the EBDX Renovation base project (commit 452d27ca) got `dist/Prismfall_DevKit.zip` exactly as the
   kit README says: `Plugins/`, `PBS/`, `Data/` and `Graphics/` copied in, nothing else touched.
2. **First Debug boot**: plugins and PBS compiled; Essentials imported our 71 map files (as `MAP100`...).
3. **New Game** offered the installer: 8 tilesets, 141 switch/variable names, 71 maps renamed and nested, with three
   `*.prismfall-bak` backups (`01`). Then the game quit and restarted, as a user would.
4. **Second boot, New Game**: Debug → Files options → Install Prismfall maps reported "Everything was already
   installed" (`02`). Then the dev-only bot played on:
   - the Dovetail prologue: title card, appearance, name on the on-screen keyboard (`03`), difficulty (`04`), the cabin
     (`06`), Edda and Voss at the rail (`05`, `07`), docking;
   - Ferrow's Landing: Edda's last call, the customs NULL scan (`09`);
   - Larch's station and the starter table (`11`, `12`), then K1 against Kestrel (`13`, `14`; the AI lost, so the
     lose branch played);
   - Route 1: Juno's catching tutorial, a wild battle, Lass Dory (`16`, `17`).
5. A short dev-only `route1` session re-checked the Route 1 trainers after the PBS fix (`17`).

`first_minutes.gif` covers about 50 s of those minutes in eight segments.

### Chapter 1 (2026-11-18, kit rebuilt and freshly installed)
The `ch1` session resumes at Route 1's south edge with the state the prologue run had there (story switches, Pokédex,
a level 10 Mudkip) and plays on with the same real input:
- Route 1: Juno's tutorial, a wild battle, Lass Dory; then Route 2 (`20`);
- the Glassed Orchard: Juno at the Bleed Veil (`21`), the Glassed Wurmple on the BLEED field (`22`), Biscuit, then
  Larch's Lecture One and the Field Notes (`23`);
- Hale Farmhouse: Biscuit home to Wenna, quest complete (`24`);
- the stile send-off on Route 1: Town Map, "Eighteen Roads", Chapter 1 closes (`25`);
- Route 2 again: Bug Catcher Wim (`26`), the opened Accord barrier, Gossamer Wood (`27`) and Briarwick (`28`).

`chapter1.gif` covers those beats. A second prologue run on the rebuilt maps got as far as the starter scene before the
machine restarted; the lab arrival tile was free, but the rebuilt door step-out was not re-tested in the engine.

The bot uses only ordinary input:
- Use on finished messages, choices picked by their text with Up/Down, letters on the on-screen keyboard;
- the arrow keys along BFS paths; F9 for the Debug menu;
- Debug **Ctrl** walk-through, only to step off a tile the player can't leave (the two map bugs below).

The AI plays the player's side of battles. The engine clock was set to about 13:00 (TZ) so Essentials' day/night
tint shows the maps by day.

## Bugs found
| Bug | Status |
|---|---|
| Fresh install crashed on New Game: maps use tilesets 30/33/34/40 (now also 50–53), which the kit didn't ship | **Fixed.** `package.sh` ships `Graphics/{Tilesets,Autotiles,Fogs}`, plus `Data/Tilesets_prismfall.rxdata` (written by `mapgen/export_tilesets_rxdata.py`). The installer merges it into `Tilesets.rxdata`: backup first, padded slots, never overwrites a differently named tileset, idempotent. |
| The installer added no maps after a Debug boot: Essentials had already imported them as `MAP100`..., which it reported as collisions | **Fixed.** Those compiler placeholders get our names and tree; parents now come before children. |
| **Every event page conditioned on story switches S101+ was dead**, e.g. the Dovetail gangway stayed roped off after docking. Cause: Essentials v21.1 `Game_Event#switchIsOn?` returns false for a switch with no `System.rxdata` entry, and the base defines only 100 | **Fixed.** The installer names our switches and variables from FLAGS.md (`Data/system_prismfall.txt`) and raises the maximum. |
| Boot stopped with `superclass mismatch for class PokemonSprite` (EBDX `UI Fixes.rb:4`). It's a base-project bug: the untouched base fails the same way | **Fixed on our side.** `Plugins/~Prismfall Base Fixes` loads first and patches that line in memory. The manual one-line fix is in SETUP.md §6. |
| New Game start (109: 8, 6) was under deck barrels, so the player couldn't move | **Fixed.** `PRISMFALL_START = [109, 7, 6]`; the export script now warns when the start tile is boxed in. |
| Prologue and Act I title cards showed as plain text: Prismfall Maps loaded before Cutscenes | **Fixed.** `Optional = Prismfall Cutscenes` in the Maps meta. |
| Route 1 crashed when Lass Dory spotted the player: the map names Pim/Dory (new script), PBS still had Pip/Wren | **Fixed.** Pim and Dory added (3 difficulty variants) in `pbs/trainers.txt` and `tools/trainer_gen/routes.py`. |
| 16 more trainers used by maps were missing from PBS (maps 131, 521, 524, 525, 560, 562, 563). Each crashed when it battled | **Fixed.** All added (BALANCE §4b levels, 3 variants); all 18 new trainers started a battle in the engine (`checks` session). `tools/validate_map_trainers.py` now cross-checks every battle a map starts. |
| Larch Research Station (103): the arrival tile (14, 14) is under `barrel_b`, so the player can't move after entering (`11`) | **Fixed by the map builder** (arrival tile free in the 2026-11-18 run). |
| Ferrow's Landing on the Rejuvenation tileset (51): all 7 door tiles are fully impassable, so leaving any building strands the player on the door (`15`) | **Fixed by the map builder** (passages re-exported; not re-tested in the engine). |
| Em dash, en dash and ₽ draw as boxes (no stock font has them): 69 event lines on 15 maps, and the quest-log format in `006_MapStory.rb` (`10`) | **Fixed.** `~Prismfall Base Fixes/002_Font_Glyphs.rb` draws them as `--`, `-`, `$`, `->` at display time (`18`, `19`); map text is unchanged. |
| Route 2 crashed the engine as soon as it was drawn (also from Route 1): events 8–10 "Accord barrier" on map 521 and "Crystal silk" on 525 use tile graphics that tileset 53 doesn't have | **Open** (map builder; REQUESTS item 10). The bot blanks them in the test copy only; `export_tilesets_rxdata.py` now warns. |
| Blacking out before the first Poké Center visit sent the player to the base project's sample house (map 3) | **Fixed.** New Game sets the respawn to Ferrow's Landing's HealingSpot. |
| No trainer sprites for Prismfall types (RIVAL_KESTREL here; Brann and Tamsin earlier) | Not a crash: EBDX logs a warning and shows no trainer. No placeholder mapping added. |
| This Linux engine build leaves stock script methods private, so stock `Kernel.pbShowCommands` (every choice box) fails | Capture environment only. The bot makes it public, as on Windows. |

Map bugs are also in `mapgen/REQUESTS.md` for the map builders.

## Files
- `01`–`17` `*.png`: prologue key frames, in story order; `18`–`19` the glyph fallback; `20`–`28` Chapter 1.
- `chapter1.gif`: Chapter 1 beats, same format.
- `first_minutes.gif`: about 50 s, 512×384 frames at real speed (every 12th engine frame at 200 ms), shared 128-colour palette.

## Re-running
```bash
cd tools/harness/playtest
bash run_playtest.sh assemble   # package + fresh base copy + kit as README says + dev-only bot
bash run_playtest.sh install    # first Debug boot, New Game -> install offer -> quit
bash run_playtest.sh play       # restart, Debug installer re-run, prologue and Chapter 1 (over an hour)
bash run_playtest.sh ch1        # or resume at Route 1 and play Chapter 1 to Briarwick (about 10 min)
bash run_playtest.sh checks     # glyph lines, quest log, every trainer added on 2026-11-17
python3 -I make_playtest_media.py RUN_OUT_DIR ../../../docs/playtest --shot FILE:"caption" ... --gif A-B,C-D
```
- Needs the mkxp-z build from `tools/harness/visual/run_engine_capture.sh build`.
- Runs use their own copy (`$RUN/playtest_game`), save folder ("Prismfall Playtest") and Xvfb display (:147).
- `bash run_playtest.sh stop` stops only this copy's engine.

Test-copy-only changes:
- the bot plugin;
- `mkxp.json`: Ruby stdlib path, no vsync, own save folder;
- the Linux binary;
- silenced audio (no audio device);
- public `pbShowCommands` (see above).

## Not verified
- Windows, a real GPU, audio, or a human player.
- Maps are being rebuilt in parallel. The prologue run used the kit as packaged at 10:17 on 2026-11-17, Chapter 1 the kit of 2026-11-17 11:20.
- The Twins double battles on the map (the bot's path missed their line of sight; both started in the `checks` session).
