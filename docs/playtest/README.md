# First playable build: real-engine playtest (2026-11-17)

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
| 16 more trainers used by maps are missing from PBS (maps 131, 521, 524, 525, 560, 562, 563, e.g. Bug Catcher Wim and Picnicker Ada on Route 2). Each crashes when it battles | **Open** (trainer data owner). Debug mode offers to create them. |
| Larch Research Station (103): the arrival tile (14, 14) is under `barrel_b`, so the player can't move after entering (`11`) | **Open** (map builder; `layouts/early_interiors.py`). |
| Ferrow's Landing on the Rejuvenation tileset (51): all 7 door tiles are fully impassable, so leaving any building strands the player on the door (`15`) | **Open** (in-progress rebuild; tileset 51 door passages). |
| Em dash, en dash and ₽ draw as boxes (no stock font has them): 69 event lines on 15 maps, and the quest-log format in `006_MapStory.rb` (`10`) | **Open** (text: use "-", or ship a font). |
| No trainer sprites for Prismfall types (RIVAL_KESTREL here; Brann and Tamsin earlier) | Not a crash: EBDX logs a warning and shows no trainer. No placeholder mapping added. |
| This Linux engine build leaves stock script methods private, so stock `Kernel.pbShowCommands` (every choice box) fails | Capture environment only. The bot makes it public, as on Windows. |

Map bugs are also in `mapgen/REQUESTS.md` for the map builders.

## Files
- `01`–`17` `*.png`: key frames, in story order.
- `first_minutes.gif`: about 50 s, 512×384 frames at real speed (every 12th engine frame at 200 ms), shared 128-colour palette.

## Re-running
```bash
cd tools/harness/playtest
bash run_playtest.sh assemble   # package + fresh base copy + kit as README says + dev-only bot
bash run_playtest.sh install    # first Debug boot, New Game -> install offer -> quit
bash run_playtest.sh play       # restart, Debug installer re-run, prologue to Route 1 (about 25 min)
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
- Maps are being rebuilt in parallel. This run used the kit as packaged at 10:17 on 2026-11-17.
