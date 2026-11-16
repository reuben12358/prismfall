# Prismfall — Setup Guide (Windows, from nothing to a running field battle)

You'll end up with: an Essentials v21.1 + EBDX project that loads our four plugins and PBS, plus a working
**Debug → Prismfall tools...** menu for testing a battle on any field in about two minutes.

**Short version:** install RPG Maker XP → clone the base project → copy our `Plugins/` + `PBS/` (and later
the maps) in → playtest while holding **Ctrl** → Debug → **Prismfall tools...** → **Field test: wild battle**.

---

## 1. Install RPG Maker XP (the map editor)

Essentials runs on its own engine (mkxp-z). You only need RPG Maker XP (RMXP) to **edit maps and events**.

| Option | Notes |
|---|---|
| **Steam** — [RPG Maker XP, app 235900](https://store.steampowered.com/app/235900/) | $24.99, often discounted. It was free for a few days in Feb 2024 ([GamePressure](https://www.gamepressure.com/newsroom/create-your-own-rpg-for-free-rpg-maker-xp-available-on-steam/z4692c)), so check your library. The store page still says "64-bit OS is NOT supported". That text is stale: RMXP is in everyday use on 64-bit Windows 10/11 (based on community use, not tested here). |
| **Official trial** — [rpgmakerweb.com free trials](https://old.rpgmakerweb.com/download/free-trials/trial-rpg-maker-xp) | Windows only. Needs your name and email. The trial length isn't stated. |
| **macOS** | Run RMXP under a Windows-compatibility layer: [CrossOver](https://www.codeweavers.com/compatibility/crossover/media/rpg-maker-xp), PortingKit or Whisky. A community user [develops this way with PortingKit](https://www.pokecommunity.com/threads/pokemon-essentials-on-linux.529066). mkxp-z has native macOS builds for running the game. |
| **Linux / Steam Deck** | Run RMXP through Steam with Proton (try Proton GE if it misbehaves), or use Bottles/Wine. One user reported that RMXP's **Playtest** button doesn't launch under Proton ([thread](https://www.pokecommunity.com/threads/pokemon-essentials-on-linux.529066)). Run `Game.exe debug` through Wine or Bottles instead (see §4). |

You don't need the RTP: Essentials ships every graphic it uses.

## 2. Get the base project

Both options are full v21.1 projects with everything pre-installed. Our plugins work with either: the bridge and
Core were checked against both codebases.

### Option A (recommended): ChromeValiant's *Open-Source EBDX Renovation Project*

This is a fork of option B's repo ([Eevee Expo resource 1831](https://eeveeexpo.com/resources/1831/), whose download redirects here).
It ships with the v21 frame-rate fix already applied, rebuilt animation timing, animated Gen 1–9 sprites,
Gen 9 Pack 3.3.8, mouse support, SOS/HP-threshold scripting and built-in terrain visuals.

```
git clone https://github.com/ChromeValiant/Pokemon-Essentials-21-With-Unofficial-EBDX Prismfall
cd Prismfall
git checkout 452d27ca     # the commit we checked (2026-10-25); remove this line to take newer commits
```

| Component | Version (from each `meta.txt`) |
|---|---|
| Essentials + v21.1 Hotfixes | 21.1 / 1.0.9 |
| **Elite Battle: DX** (plugin Name unchanged) | **4.0** |
| Luka's Scripting Utilities | 3.3.2 |
| Generation 9 Pack | 3.3.8 |
| Also included | EBDX Stat Boost Overlay 1.3, Easy Mouse System 2.0, Pokémon World Tournament |

Caveats:
- It's young: v4.0 came out Oct 2026 and it has no tagged releases.
- GitHub issues are disabled; bug reports go to the [Eevee Expo thread](https://eeveeexpo.com/threads/9239/).
- The author is on hiatus until after Thanksgiving 2026.
- Open reports there:
  - Mouse quirks
  - Hidden Power
  - PC box sprite centering
  - Camera drift after trainer wins
  - A debug "advanced wild battle" error
  - A Route 1 sample-NPC IV error inherited from the base port
- If something breaks for you, use option B.

### Option B (fallback): Manurocker95's *Pokemon-Essentials-21-With-Unofficial-EBDX*

Eevee Expo's download button for the EBDX port ([resource 1338](https://eeveeexpo.com/resources/1338/)) redirects to this repo.
It's the original port that option A forks; last updated Sep 2024.

```
git clone https://github.com/Manurocker95/Pokemon-Essentials-21-With-Unofficial-EBDX Prismfall
```
(Or use GitHub's **Code → Download ZIP** / the latest release's Source.zip, then unzip it to a short path such as `C:\Games\Prismfall`.)

What's inside option B, read from each plugin's `meta.txt` in the repo:

| Component | Version | Plugin Name (for Requires lines) |
|---|---|---|
| Pokémon Essentials | 21.1 | — |
| v21.1 Hotfixes (Maruno) | 1.0.9 | `v21.1 Hotfixes` |
| Elite Battle: DX, unofficial port (Manurocker95) | 1.4.7.1 (E21) | **`Elite Battle: DX`** |
| Luka's Scripting Utilities | 3.3.2 | `Luka's Scripting Utilities` |
| Generation 9 Pack (Caruban) | 3.2.5 | `Generation 9 Pack` (it requires Hotfixes 1.0.9) |
| Pokémon World Tournament | — | — |

It also includes `PBS/EBDX/*.txt` (EBDX metrics, trainer and Pokémon data), `Graphics/EBDX/` (Gen 1–5 animated
battlers, backdrops and UI), the Gen 1–9 PBS and 71 sample maps.
The top commit is *"framerate setup and last item hotfix"*.

> **Alternative: build it by hand.**
> 1. Download [Essentials v21.1](https://eeveeexpo.com/essentials/download) (MediaFire).
> 2. Add the [v21.1 Hotfixes plugin](https://eeveeexpo.com/resources/1376/) into `Plugins/v21.1 Hotfixes/` ([direct link](https://www.mediafire.com/file/znhw2jk5judt3ga/v21.1_Hotfixes.zip/file)).
> 3. Add the original EBDX resources and LUTS from the port's mirror ([Google Drive](https://drive.google.com/drive/folders/16DH91kXF2_A3fd8ujiS71LfjEKJ67dJu)): unzip `EBDX_vanilla.zip` and `LUTS_v19.zip` into the project, keeping their folder structure.
> 4. Replace `Plugins/Elite Battle DX` and `Plugins/Luka's Scripting Utilities` (and its meta.txt) with the copies from the repo above.
>
> This is exactly what the repo already contains, so only do it if you need a clean v21.1 install.

## 3. Drop in Prismfall

Close RPG Maker XP first: it overwrites `Data/*.rxdata` when it saves. Back up the project folder.

1. **Plugins.** Copy these four folders into `<project>/Plugins/`:
   `Prismfall Core`, `Prismfall Field Effects`, `Prismfall EBDX Bridge`, `Prismfall Debug Tools`.
   Each folder must contain its `meta.txt` directly (`Plugins/Prismfall EBDX Bridge/meta.txt`), not a nested folder.
   Load order follows the dependencies automatically: EBDX → Field Effects → Bridge.
2. **PBS.** Copy our PBS files into `<project>/PBS/`. They ship with suffixes, so no stock file is edited:
   `trainer_types_prismfall.txt`, `trainers_prismfall.txt`, `items_prismfall.txt` (field seeds),
   `encounters_prismfall.txt` and `map_metadata_prismfall.txt`.
   Essentials v21.1 merges every `PBS/<base>_<suffix>.txt` with `PBS/<base>.txt` when it compiles
   (`Compiler.get_all_pbs_files_to_compile`). Our encounters use map IDs 100+, so the sample maps' encounters stay intact.
3. **Battle graphics (optional at first).** Put field backdrops in `Graphics/EBDX/Battlebacks/battlebg/` (see
   [ART_ASSETS.md](ART_ASSETS.md)). Until you do, every field uses a tinted stock EBDX room with its particle FX,
   so fields are playable on day one.
4. **Maps (when the Map Builder output ships).**
   1. Close RMXP and back up `Data/`.
   2. Copy the generated `Data/MapNNN.rxdata` files (IDs 100+) into `<project>/Data/`.
   3. Run the shipped **MapInfos merge step**. It adds our maps to `Data/MapInfos.rxdata` without touching existing entries.
      Its exact tool or file name comes with the map package; follow that README.
   4. Reopen RMXP: the new maps appear in the map tree. Maps use stock Essentials tilesets, so `Tilesets.rxdata` doesn't change.

## 4. Compile and launch in Debug mode

Debug mode is what compiles plugins and PBS and unlocks the Debug menu.

- **From RMXP:** open `Game.rxproj` and press **Playtest** (F12). This runs in debug mode.
- **Without RMXP (Linux/macOS/Proton):** run `Game.exe debug`.

**First launch:** hold **Ctrl** while the window opens (until the console shows *Compiling...*). Ctrl forces a full
recompile of the PBS, the plugins (`Data/PluginScripts.rxdata`) and EBDX's own data (`PBS/EBDX/*.txt` →
`Data/*.ebdx`, compiled by `CompilerEBDX.compile`, debug mode only).

**Later:** Essentials recompiles changed PBS and plugins automatically. To force a recompile, hold Ctrl on launch or use
**Debug menu (F9) → Files options... → Compile data**.

Check the console:
- It should list `Prismfall Core`, `Prismfall Field Effects`, `Prismfall EBDX Bridge` and `Prismfall Debug Tools` as loaded.
- Our bridge lists EBDX as `Optional`, so the project also runs **without EBDX**: the bridge then swaps vanilla
  `Graphics/Battlebacks/<backdrop>_bg/_base0/_base1/_message` instead.

## 5. Test a field battle quickly

Start or load a save, press **F9** (Debug) → **Prismfall tools...**:

| Entry | What it does |
|---|---|
| **Field test: wild battle** | Pick a field (or *[No field]*), a species and a level. Runs with `canLose`. |
| **Field test: trainer battle** | Pick a field, then any trainer from trainers.txt. |
| **Warden battle (1-18)** | Fight a Warden on their signature field. It offers to set your party to that gym's level cap and heal first. The difficulty variant follows the current mode. Needs our trainers PBS compiled. |
| **Set badge count (0-18)** / **Set whole party level** / **Heal party** | Setup helpers. |

**Live field changes in battle:** in any battle press **F9** → **Field effects...** → **Field effect** (added by Field
Effects) → change the field, change its stage, or rotate the borrowed effects. Each change fires
`:prismfall_field_changed`, and the bridge fades the backdrop to the new field. This is the quickest way to check
art, FX and transitions (e.g. VOLCANIC → ASHEN_WASTE, or FLOWER_GARDEN stages 1→5).

**From an event** (a test NPC):
```ruby
setBattleRule("field", :VOLCANIC)     # field for the next battle only
WildBattle.start(:CHARMANDER, 20)     # or TrainerBattle.start(:LEADER_BRANN, "Brann")
```
For a per-map default, add `FieldEffects::MAP_FIELDS[map_id] = :FIELD_ID` in any plugin that loads after Field Effects.
**Ctrl** held while a battle starts in debug mode *skips* the battle (vanilla behaviour), so don't hold it then.

---

## 6. Known EBDX-on-v21 issues and fixes

**Option A (Renovation) already fixes the first and third rows:** its `mkxp.json` ships with `"syncToRefreshrate": false, "fixedFramerate": 60`, and it has no trainer out-of-place hotfix or delta-time switches (the `Config.rb` constants named below exist only in option B). The other rows apply to both options.

Sources: the port's [discussion thread](https://eeveeexpo.com/threads/6958/), its
[update log](https://eeveeexpo.com/resources/1338/updates), its [reviews](https://eeveeexpo.com/resources/1338/reviews)
and the port's code (`Plugins/Elite Battle DX/[003] Config/Config.rb`).

| Symptom | Cause | Fix |
|---|---|---|
| **Battle animations too fast** on 120/144 Hz monitors, or intros and fades too slow | v21 timing is in seconds, but EBDX animates per frame. The repo's `mkxp.json` has `"syncToRefreshrate": true`, so the frame rate equals your monitor's refresh rate. | In `mkxp.json`, set `"syncToRefreshrate": false` and add `"fixedFramerate": 60` (option names from mkxp.json's own comments). Then try `USE_DELTA_TIME_HOTFIX` in Config.rb both ways (default `false` = frame-based with the SceoFlash13 hotfix; `true` = delta-time waits, added in the port's May 2024 updates). Option A is preconfigured this way. |
| **Crash at battle start:** `undefined method 'has_key?' for nil` in `Scene Backdrops.rb … adjustMetrics` (reported in the thread, no fix posted) | From the code: `adjustMetrics` reads `EliteBattle.get(:battlerMetrics)`, which is filled from `Data/metrics.ebdx`. If `PBS/EBDX/metrics.txt` is missing, never compiled, or lacks `[BATTLERPOS-0]` / `[BATTLERPOS-1]`, the hash is empty and the method crashes. | Make sure `PBS/EBDX/metrics.txt` exists (it's in the repo), then launch in **debug mode holding Ctrl** so `Data/metrics.ebdx` is rebuilt. Release builds must ship `Data/*.ebdx`, because EBDX only compiles in debug mode. |
| **Trainer sprite out of place / camera shows the void** after a trainer's end speech (option B) | Known port issue | `USE_TRAINER_OUT_OF_PLACE_HOTFIX` in Config.rb (default `true` in this repo). If trainers drift, set it to `false` (one user reported the camera fixed itself after one F12 reset). SceoFlash13's manual patch to `pbShowOpponent`/`pbHideOpponent` in `Battle Modifiers/Scripted Battles.rb` is in thread page 2. Option A removed this hotfix. |
| **Animated trainer sprites look small or slow** | Scale | `TRAINER_SPRITE_SCALE = 2` in Config.rb (confirmed by a user). |
| **White flashes and a 1–3 s delay** at wild encounters or faints (2025 reviews) | Unresolved in 1.4.7.1 | Try the frame-rate fix above. Option A reports fixing the pre-battle music delay and lag. |
| **`NameError: uninitialized constant EliteBattle::SKIP_CACHED_DATA`** | Your Config.rb is older than the scripts | Update the whole `Plugins/Elite Battle DX` folder (1.4.7.1 defines it). |
| **Crash when a Pokémon must use Struggle** (thread page 1) | Some EBDX code looks up Struggle's move data | If you hit it, add a `PBS/moves_ebdxfix.txt` with a `[STRUGGLE]` entry (`FunctionCode = Struggle`, Power 50, Type NORMAL, Physical, TotalPP 1, Target RandomNearFoe). Metronome already excludes the `Struggle` function code. Not reproduced here. |
| **Map `BattleEnv` in `PBS/EBDX/maps.txt` ignored** (thread page 2) | Unresolved | Doesn't affect fields: the bridge sets the room directly. For plain maps, call `EliteBattle.set(:nextBattleBack, {...})` before the battle. |
| **Plugins don't compile** | Folder layout | Every plugin needs its own folder with `meta.txt` directly inside it. Delete `Data/PluginScripts.rxdata` and relaunch while holding Ctrl. |
| **Static or blurry Gen 6+ sprites, oversized Gen 9 sprites** | The port bundles only Gen 1–5 animated sprites. Gen 6–9 use Gen 9 Pack statics with their own metrics. | Static sprites must match the animated frame size (the maintainer's advice). Use the Sprite Positioner port ([resource 1339](https://eeveeexpo.com/resources/1339/)) to fix metrics. See RESOURCES.md for animated packs. |
| **Following Pokémon EX** sendouts | — | Keep `USE_FOLLOWER_EXCEPTION = true` (EBDX Config.rb). |

**Incompatible with EBDX:**
- **Deluxe Battle Kit and its add-ons.** Lucidious89: *"I specifically made this plugin incompatible with EBDX"* ([thread](https://eeveeexpo.com/threads/7778/page-2)).
- **ZUD.** The EBDX port's page says it never will be compatible.

## 7. Bridge notes for developers

- The bridge hooks `Battle::Scene#loadBackdrop` and drives EBDX's own `BattleSceneRoom#reconfigure(data, transition)`,
  the same call EBDX's sample battle scripts use. EBDX never reads `battle.backdrop`, so vanilla battlebacks only matter without EBDX.
- If a script sets `EliteBattle.set(:nextBattleBack, ...)` for a battle, that backdrop is kept at battle start
  (`PrismfallEBDX::RESPECT_SCRIPTED_BACKDROP`). Later field changes still swap it.
- Tuning lives in `Plugins/Prismfall EBDX Bridge/001_Bridge_Config.rb`:
  - `AMBIENT_FX` / `FX_DENSITY` for low-end PCs
  - per-field transitions, tones and particle emitters
  - `TRANSITION_OVERRIDES` for specific A→B changes (e.g. steam grey for VOLCANIC→ASHEN_WASTE, distortion into BLEED)
- Bridge errors never stop a battle; a failing FX layer just switches itself off.
  - In debug mode they print as console warnings (`[Prismfall EBDX Bridge] ...`).
  - With `$INTERNAL` on, they also go to `Data/debuglog.txt` via `PBDebug.log`.
