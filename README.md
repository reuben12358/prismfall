# Pokémon Prismfall — Dev Kit (work in progress)

A Reborn/Rejuvenation-style fangame for **Pokémon Essentials v21.1 + Elite Battle: DX**: 18 gyms across seven
kingdoms, 31 field effects, choice-driven Festival of Champions, multiple endings, game overs and a secret Ruin Route.

This kit is an **overlay**: copy its folders into an Essentials + EBDX project. It never overwrites stock files.

## Quick start (Windows)
1. **Base project + RPG Maker XP** — follow `Docs/SETUP.md` §1–3 (recommended base: the EBDX Renovation fork, pinned
   commit; fallback: Manurocker95's Essentials 21 + EBDX project).
2. **Close RPG Maker XP**, then copy this kit's `Plugins/`, `PBS/` and `Data/` folders into your project root
   (merge folders; no stock file is replaced — PBS files are `*_prismfall.txt` additions).
3. Run the game in **Debug** mode (it recompiles PBS + plugins). If asked to compile, say yes.
4. In game: **Debug → Files → Install Prismfall maps** (adds our maps to your MapInfos; backs it up first).
   Then restart the game.
5. In RPG Maker XP, open the map you want new games to start on (the Dovetail ferry prologue, or Ferrow's Landing
   for now), right-click a tile → **Set Starting Position**.
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
| `Plugins/Prismfall Map*` | Map installer + per-map default fields |
| `PBS/*_prismfall.txt` | Trainers (Wardens ×3 difficulties, rivals, Festival), trainer types, seed items, encounters, map metadata/connections |
| `Data/Map*.rxdata` | Generated maps (Act I slice in progress + Test Arena) |
| `Design/`, `Story/`, `Docs/` | Spine, story bible, choices/endings, world & gym puzzles, field compendium, systems docs, art asset list, setup, map previews |
| `Tools/` | Validators, standalone map merge tool, map generator specs |

## Status
Everything is syntax-checked and validated against the base project's data and exercised with mock tests, but it has
**not yet been run inside the real engine** — expect first-boot fixes. Art is stock Essentials only (see
`Docs/ART_ASSETS.md` for the field backdrops to source). Report crashes with the error log text and they'll be fixed.
