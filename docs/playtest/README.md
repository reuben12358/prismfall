# First playable build: real-engine playtest (2026-11-17, Chapter 1 added 2026-11-18, the Strand Road to Saltmere 2026-11-19/20)

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

### Round 3 (2026-11-19/20): Gym 1/Gym 2 swap, fresh installs, the Strand Road into Saltmere
Before the runs: the swap checklist's plugin items (Cut at 2 badges, the Debug Tools gym table, the encounter
validator's fallback; `ruby -c` clean on every plugin) and Core's narrative self-check in the engine (Debug > Prismfall
Core > Show Core status: "Data check: OK"; all 151 conditions also evaluated on a live save without an error).

Three fresh installs (new base copy, kit as packaged, first Debug boot, installer on New Game), no level shortcuts:
| Run | Kit | Got to | Team at the end | Blackouts |
|---|---|---|---|---|
| 1 | 17:11 | Prologue → starter → K1 → Ferrow (lab, Poké Center, Mart in and out) → Ferrymen's Mile → Windfall Row → Glassed Orchard → Hale Farmhouse → stile send-off (still the pre-swap "Briarwick's first" text). Stopped by design at the end of Ch1: the Strand Road (527) was not in that kit | Mudkip L11, Wooloo L7 | 2 (Wim, Ada) |
| 2 | 17:55 | Ferrymen's Mile, then nowhere: the kit caught builder 9 mid-rebuild (new 520, old 521), so Windfall Row could not be reached. Abandoned | Mudkip L7 | 1 |
| 3 | 22:11 | The whole of Chapter 1 on the rebuilt maps, the farmhouse rest and send-off ("Saltmere's first", Town Map, "Eighteen Roads"), Lacecliff Walk (527), Marram Down (528), Saltmere's East Gate (arrival scene), its Poké Center, **J1** on the green (Juno won), the Old Town outside the Pell Playhouse. Gyms not attempted: Gym 1's crowd logic and Gym 2's redesign are in progress | Mudkip L15 (the cap), Skwovet L3 | 11 |

Run 3's levels: Mudkip L7 after the Ferrymen's Mile, L13 after the orchard, L15 (Gym 1 cap) on Lacecliff Walk.
Blackouts: Lass Wren 1, Picnicker Ada 5, Fisherman Bryn 1, Picnicker Moll 1, Juggler Hounds 1, wild 2. The AI team
enters each trainer at whatever HP the last fight left and heals only by blacking out, so this measures a careless
player; still, **Picnicker Ada (Oddish 6, Budew 7) beat the Water starter in 7 of 8 fights** across the segments
(a Grass pair against Mudkip L9-11), the Ch1 wall. J1 (Cottonee, Petilil, Bounsweet 13, Torchic 15) beat Mudkip L15.

Every battle got its map's field and that field's own EBDX room (+ HD layer): MEADOW on 520/521 and for J1
(`29`, `36`), BLEED in the orchard (`30`), BEACH on 527/528 (`31`). The one exception is K1, :NONE on purpose (`32`).
Run 3 is one game but not one process: the environment restarted twice and the bot was fixed five times, and each
time it carried on from its own autosave (logged; no story flag was set by hand). `strand_road.gif` covers run 3.

The bot uses only ordinary input:
- Use on finished messages, choices picked by their text with Up/Down, letters on the on-screen keyboard;
- the arrow keys along BFS paths; F9 for the Debug menu;
- Debug **Ctrl** walk-through, only to step off a tile the player can't leave (the two map bugs below; not needed in round 3);
- after a blackout it walks back from the Poké Center to the step it lost on, over the plan's own map links; after
  losing to a trainer it trains in that map's grass (up to 2 levels, never past the level cap) before trying again.

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
| Larch Research Station (103): the arrival tile (14, 14) is under `barrel_b`, so the player can't move after entering (`11`) | **Fixed by the map builder.** Verified in the engine on 2026-11-19 (three fresh installs, no Debug walk-through). |
| Ferrow's Landing on the Rejuvenation tileset (51): all 7 door tiles are fully impassable, so leaving any building strands the player on the door (`15`) | **Fixed by the map builder.** Verified in the engine on 2026-11-19: in and out of the lab, Poké Center and Mart, no Debug walk-through. |
| Em dash, en dash and ₽ draw as boxes (no stock font has them): 69 event lines on 15 maps, and the quest-log format in `006_MapStory.rb` (`10`) | **Fixed.** `~Prismfall Base Fixes/002_Font_Glyphs.rb` draws them as `--`, `-`, `$`, `->` at display time (`18`, `19`); map text is unchanged. |
| Route 2 crashed the engine as soon as it was drawn (also from Route 1): events 8–10 "Accord barrier" on map 521 and "Crystal silk" on 525 use tile graphics that tileset 53 doesn't have | **Fixed by the map builder.** `export_tilesets_rxdata.py` warns about nothing; on 2026-11-19 Windfall Row (521) drew with nothing blanked. |
| Blacking out before the first Poké Center visit sent the player to the base project's sample house (map 3) | **Fixed.** New Game sets the respawn to Ferrow's Landing's HealingSpot. |
| No trainer sprites for Prismfall types (RIVAL_KESTREL here; Brann and Tamsin earlier) | Not a crash: EBDX logs a warning and shows no trainer. Still open for Kestrel on 2026-11-19 (Dorian, Tamsin and Larch kitbash sprites are in progress in art/). |
| **2026-11-19 (Revision 14 swap):** Cut gated at 1 badge; the Debug Tools fallback gym table had Tamsin first; `validate_encounters.py` gave the old segments to maps missing from maps.json | **Fixed.** Core `FIELD_MOVE_BADGES[:CUT] = 2`; fallback table Dorian (1), Tamsin (2); the validator's fallback swaps the 120/140 blocks and has the Rev 14 exceptions (132–134, 151–153, 524–526, 548), matching maps.json for every Act I map. |
| Narrative self-check after the Consent rows 1–2 edit (`012_Narrative_Data.rb`) | **OK in the engine.** Debug > Prismfall Core > Show Core status: "Data check: OK". The bot also evaluated all 151 conditions on a live save: none raised; Consent row 1 is Dorian (GYMS 1), row 2 Tamsin (GYMS 2). |
| The 17:55 kit had builder 9's new Ferrymen's Mile (520, 64×110) with the old Windfall Row (521): every open tile on 520's north edge lands on a blocked 521 tile, so Windfall Row could not be reached | **Fixed by the 21:56 rebuild of 521** (REQUESTS 14). Seen because the kit was packaged mid-rebuild. Every seam on 100–520–521 and 520–527–528–140 is now checked offline before a run (`tools/harness/playtest/seam_check.py`). |
| 17:55 kit: J1 on Saltmere's green was gated on S107 (the Matriarch, Ch3), and Windfall Row's forest road to Briarwick opened after Chapter 1 | **Fixed in the 21:56 build** (J1 opens on S105 + arrival; 521 has the forest-road cordon). The stale J1 page is still in `layouts/saltmere_events.yaml` (REQUESTS 12). |
| 17:11 kit: the stile send-off still said "Briarwick's first… Tamsin Loom" and the quest "Earn the first badge in Briarwick" | **Fixed in the later builds** (the new 520 says "Saltmere's first"). |
| K1 at the lab gate shows EBDX's stock grassy "Field" room in a harbour town. The field is :NONE on purpose (TRAINER_FIELDS: the tutorial battle) | Cosmetic, open (field defaults). A plain backdrop rule (no field) such as a dock/beach room would fit the place. |
| `tools/package.sh` once failed with a Python `TypeError` while a map build was being written; the next run was fine | Note: package between builds (wait until `maps_out/` stops changing). |
| **Open (map 520):** the Hale Bell roadblock leaks. The barrier events (3,71), (2,73)–(2,75) leave row 72 and (1–2,68–76) open, and in the engine the bot walked from the stile to Lacecliff Walk with S105 off, i.e. before the Glassed Orchard | REQUESTS 15 (map builder 9). Suggested: barrier events on the four edge tiles (0,72)–(0,75). |
| **Open (maps 523/520):** Chapter 1 only closes if the player rests in the Hale Farmhouse bed (`33`; V102 = 2 → night cutscene → send-off), nothing asks them to, and the Hale Bell barrier opens on S105 alone. Run 3 first reached Lacecliff Walk with no send-off, Town Map or "Eighteen Roads" | REQUESTS 16. Gate the barrier on V102 ≥ 2 (guard points back to the farm), or have Wenna/Juno offer the night. |
| Playtest bot: after a blackout it ran the rest of the plan as "no way from map 101"; a resume crashed on `@spot_i`; after a blackout it rewound to Route 1 and replayed all of Chapter 1; it skipped unfinished steps when it arrived on a map with a later step; walking back counted against the step's time budget | **Fixed (bot).** It waits for the rewind, resets its counters on resume, walks back to the same step over the plan's own map links and never skips while doing so, and checkpoints after every beaten trainer. New: training after a trainer loss (capped at the level cap). |
| This Linux engine build leaves stock script methods private, so stock `Kernel.pbShowCommands` (every choice box) fails | Capture environment only. The bot makes it public, as on Windows. |

Map bugs are also in `mapgen/REQUESTS.md` for the map builders.

## Files
- `01`–`17` `*.png`: prologue key frames, in story order; `18`–`19` the glyph fallback; `20`–`28` Chapter 1;
  `29`–`37` round 3 (three fields, K1's room, the farmhouse bed, the send-off, Saltmere, J1, the Old Town).
- `chapter1.gif`: Chapter 1 beats, same format. `strand_road.gif`: round 3, prologue to Saltmere's Old Town (every
  12th–24th engine frame, so the later segments run faster).
- `first_minutes.gif`: about 50 s, 512×384 frames at real speed (every 12th engine frame at 200 ms), shared 128-colour palette.

## Re-running
```bash
cd tools/harness/playtest
bash run_playtest.sh assemble   # package + fresh base copy + kit as README says + dev-only bot
bash run_playtest.sh install    # first Debug boot, New Game -> install offer -> quit
bash run_playtest.sh play       # restart, Debug installer re-run, prologue and Chapter 1 (over an hour)
bash run_playtest.sh ch1        # or resume at Route 1 and play Chapter 1 to Briarwick (about 10 min)
bash run_playtest.sh checks     # glyph lines, quest log, every trainer added on 2026-11-17
bash run_playtest.sh narrative  # Core's narrative self-check in the engine + every condition on a live save
bash run_playtest.sh resume     # Continue the bot's autosave (after a restart or a bot fix) and carry on
bash run_playtest.sh update     # mid-run kit update over the game; then `reinstall` (Debug installer, quit), `resume`
python3 -I make_playtest_media.py RUN_OUT_DIR ../../../docs/playtest --shot FILE:"caption" ... --gif A-B,C-D
```
- Needs the mkxp-z build from `tools/harness/visual/run_engine_capture.sh build`.
- Runs use their own copy (`$RUN/playtest_game`), save folder ("Prismfall Playtest") and Xvfb display (:147);
  round 3 used `RUN=/home/claude/run_pt PLAY_APP="Prismfall Playtest PT" PLAY_DISPLAY=157`.
- Package between map builds (wait until `maps_out/` stops changing) and check the seams of the maps you will walk.
- `bash run_playtest.sh stop` stops only this copy's engine.

Test-copy-only changes:
- the bot plugin;
- `mkxp.json`: Ruby stdlib path, no vsync, own save folder;
- the Linux binary;
- silenced audio (no audio device);
- public `pbShowCommands` (see above).

## Not verified
- Windows, a real GPU, audio, or a human player.
- Maps are being rebuilt in parallel. The prologue run used the kit as packaged at 10:17 on 2026-11-17, Chapter 1 the kit of 2026-11-17 11:20, round 3 the kit of 2026-11-19 22:11.
- Gyms 1 and 2 since the swap (held back for the puzzle rework), the remaining Windfall Row and Marram Down trainers
  (Ada and Juggler Hounds stayed unbeaten), and the Ferrow inn (104) as the script's other place to rest.
- The Twins double battles on the map (the bot's path missed their line of sight; both started in the `checks` session).
