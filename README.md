# Pokémon Prismfall — Dev Kit (work in progress)

A Reborn/Rejuvenation-style fangame for **Pokémon Essentials v21.1 + Elite Battle: DX**: 18 gyms across seven
kingdoms, 31 field effects, choice-driven Festival of Champions, multiple endings, game overs and a secret Ruin Route.

This kit is an **overlay**: copy its folders into an Essentials + EBDX project. It never overwrites stock files.

## Quick start (Windows)
1. **Base project + RPG Maker XP** — follow `Docs/SETUP.md` §1–3 (recommended base: the EBDX Renovation fork, pinned
   commit; fallback: Manurocker95's Essentials 21 + EBDX project).
2. **Close RPG Maker XP**, then copy this kit's `Plugins/`, `PBS/`, `Data/` and `Graphics/` folders into your project
   root (merge folders; no stock file is replaced — PBS files are `*_prismfall.txt` additions, graphics are new names).
3. Run the game in **Debug** mode (it recompiles PBS + plugins). The first boot also says our map files were imported:
   click through. If the boot used to stop with "superclass mismatch for class PokemonSprite", that is a base-project
   bug: the kit's `Plugins/~Prismfall Base Fixes` works around it (details and the manual fix: `Docs/SETUP.md` §6).
4. Start a **New Game**. The first time, it asks to install the Prismfall tilesets and maps: say **Yes**. It backs up
   `Data/Tilesets.rxdata`, `MapInfos.rxdata` and `System.rxdata`, adds our tilesets, map tree and switch/variable names
   (needed: Essentials ignores event pages on unnamed switches above 100), and carries on into the prologue.
   The same installer is **Debug → Files options → Install Prismfall maps** (safe to re-run: it changes nothing twice).
5. New games start on the Dovetail's deck (`Plugins/Prismfall Maps/004_NewGameStart.rb`), so RMXP's
   "Set Starting Position" isn't needed. RPG Maker XP shows the maps and tilesets the next time you open the project.
6. Try things fast with **Debug → Prismfall tools…** (field battles, any Warden on their field, badges, party level)
   and **Debug → Prismfall Core…** (difficulty, starter, caps, Festival, narrative state, game overs, endings).
   Warp to the **Test Arena** (map 990) to battle on all 31 fields.

## What's in the kit
| Folder | Contents |
|---|---|
| `Plugins/Prismfall Core` | 18 badges + Trainer Card, level caps, difficulty modes, rival starter swap (Gen 1–9), Festival tournament + choice-driven draw, bonds/standing/resonance/choices, game overs + cross-save Ledger, endings, passwords, Rock Climb |
| `Plugins/Prismfall Field Effects` | Field engine (data-driven DSL, AI-aware), 31 fields, 4 seeds, Field Notes encyclopedia |
| `Plugins/Prismfall EBDX Bridge` | Field backdrops + transitions + ambient FX in EBDX (vanilla fallback) |
| `Plugins/Prismfall Bosses` | Rejuvenation-style multi-bar boss battles (if present in this build) |
| `Plugins/Prismfall Debug Tools` | Debug menu shortcuts for testing |
| `Plugins/Prismfall Map*` | Map + tileset installer, New Game start, per-map default fields, tones, fogs, story helpers |
| `Plugins/~Prismfall Base Fixes` | Loads first: works around the EBDX base projects' `PokemonSprite` boot error (SETUP §6), and draws characters the stock fonts lack (— – ₽ arrows) as look-alikes |
| `PBS/*_prismfall.txt` | Trainers (Wardens ×3 difficulties, rivals, Festival), trainer types, seed items, encounters, map metadata/connections |
| `Data/Map*.rxdata` | Generated maps (Act I slice in progress + Test Arena), plus `mapinfos_prismfall.txt`, `Tilesets_prismfall.rxdata` and `system_prismfall.txt` for the installer |
| `Graphics/Tilesets`, `Autotiles`, `Fogs` | The maps' tileset sheets (IDs 30, 33, 34, 40), their autotiles and fog pictures |
| `Design/`, `Story/`, `Docs/` | Spine, story bible, choices/endings, world & gym puzzles, field compendium, systems docs, art asset list, setup, map previews |
| `Tools/` | Validators (incl. `validate_map_trainers.py`: every trainer a map battles exists in PBS), standalone map merge tool, map generator specs |

## Status
The packaged kit has now been installed into a fresh copy of the EBDX Renovation base project and played in the real
engine (mkxp-z, Linux): the installer, the Dovetail prologue, Ferrow's Landing, the starter and the first rival battle.
See `Docs/playtest/` for screenshots, a GIF and the open issues. Not yet verified on Windows, with audio, or by a human
player. Art is mostly stock Essentials (see `Docs/ART_ASSETS.md`). Report crashes with the error log text and they'll be fixed.
