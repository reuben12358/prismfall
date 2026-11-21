# Prismfall research index: where to look

Everything researched for this project, sorted by topic. Each line points to the doc that holds the findings. All external links are in [`LINKS.md`](LINKS.md), and the reference images we studied are in [`reference_images/`](reference_images/).

Before proposing anything, read the creator's decisions in [`design/SPINE.md`](../design/SPINE.md). Its revisions at the top override everything older.

## Art: characters, portraits, sprites
- **Character art handoff:** [`art/HANDOFF_GEMINI.md`](../art/HANDOFF_GEMINI.md). Exact file formats, templates, the creator's verdicts, and the priority queue. **Start here.**
- **Art study (2026-11-20):** [`art/research/SOURCES.md`](../art/research/SOURCES.md), 112 images from 9 artists, plus [`art/research/moodboard_*.png`](../art/research/).
  - The artists: Honnojis/Zumi (an official Rejuvenation artist) and VGen artists angeceleste, NoodlesXL, Princeloppy, Mossgrover, InkyFrosty, Nifast Greentail, Fiorne and SilverSrini.
  - The images are in [`reference_images/art_refs/`](reference_images/art_refs/); `SOURCES_REGISTRY.tsv` gives every file's URL.
- **What makes a sprite character memorable:** [`design/CHARACTER_DESIGN_STUDY.md`](../design/CHARACTER_DESIGN_STUDY.md), studied across Celeste, Chrono Trigger, Deltarune, Eastward, Hyper Light Drifter, Sea of Stars, Showdown sprites and more. The images are in [`reference_images/charrefs/`](reference_images/charrefs/).
- **Pixel technique checklist:** [`design/PIXEL_ART_NOTES.md`](../design/PIXEL_ART_NOTES.md), measured from official B2W2 trainer fronts: proportions, faces at small size, hair, cloth, outlines and poses.
- **In-house style guide:** [`art/STYLE_GUIDE.md`](../art/STYLE_GUIDE.md). Its format rules are correct; its art results were rejected, so its taste notes are optional.
- **The old kitbash method and the creator's reactions:** [`design/KITBASH_PIPELINE.md`](../design/KITBASH_PIPELINE.md), [`design/CHARACTER_ART.md`](../design/CHARACTER_ART.md) and [`design/ART_DIRECTION.md`](../design/ART_DIRECTION.md). Useful as a list of what **not** to repeat.
- **Approved art to match:** Juno's portraits and overworld sprite, in `art/out/Graphics/`.

## Spriting resources: Pokémon, trainers, overworlds, UI
- [`docs/RESOURCES.md`](../docs/RESOURCES.md): curated packs (Gen 5-style animated battle sprites, move animations, BW-style UI, tilesets and overworlds, music) and EBDX-compatible plugins.
- [`docs/CREDITS.md`](../docs/CREDITS.md): every third-party pack we use or may use, its usage terms, and how to credit it.

## Maps and tilesets
- **Community tile packs we hunted:** [`reference_images/assets/`](reference_images/assets/), with one folder per artist (`da_*` are DeviantArt and `ee_*` Eevee Expo). Each folder's `_sources.tsv` has the original URLs.
- **How our maps are built, and every map builder's notes:** [`design/MAPGEN.md`](../design/MAPGEN.md).
- **World and places:** [`design/WORLD.md`](../design/WORLD.md), [`design/WORLD_MAP.md`](../design/WORLD_MAP.md), [`design/PLACE_NAMES.md`](../design/PLACE_NAMES.md) and [`design/ROUTES.yaml`](../design/ROUTES.yaml).

## Music and sound
- [`design/AUDIO.md`](../design/AUDIO.md): the full soundtrack plan (every town, route, dungeon, battle and story beat), the artists we looked at and their terms, file formats and naming, and how to wire tracks in Essentials/EBDX.
- [`docs/CREDITS.md`](../docs/CREDITS.md) § Music and sound: the stand-in soundtrack and the planned final one.

## Battle fields, puzzles and game design
- **Fields:** [`design/FIELD_RESEARCH.md`](../design/FIELD_RESEARCH.md) (how Reborn and Rejuvenation fields work), [`design/FIELDS.md`](../design/FIELDS.md) (all our fields) and the battle-background captures in [`docs/battle_captures/`](../docs/battle_captures/).
- **Puzzles:** [`design/PUZZLE_STUDY.md`](../design/PUZZLE_STUDY.md) (twelve Reborn and Rejuvenation puzzles decoded), [`design/GYM_PUZZLES.md`](../design/GYM_PUZZLES.md) and [`design/DUNGEON_PUZZLES.md`](../design/DUNGEON_PUZZLES.md).
- **Pokémon distribution and difficulty:** [`design/DISTRIBUTION_STUDY.md`](../design/DISTRIBUTION_STUDY.md) (Reborn and Rejuvenation data), [`design/BALANCE.md`](../design/BALANCE.md) and [`design/BADGE_TIERS.md`](../design/BADGE_TIERS.md).
- **Cutscenes:** [`design/CUTSCENE_RESEARCH.md`](../design/CUTSCENE_RESEARCH.md) and [`design/CUTSCENES.md`](../design/CUTSCENES.md).

## Story
- [`story/`](../story/): the story bible (overview, lore, factions, cast, acts I–V, mysteries, choices and endings, the Ruin Route, comedy, cutscenes) and the chapter scripts.
- [`design/CHAPTER_BEATS.md`](../design/CHAPTER_BEATS.md): the 1–2 key events in each chapter.

## Not uploaded, and why
These stayed on Claude's machine. Ask if you need something specific from them.
- **The full game data of Reborn, Rejuvenation and Desolation** (about 870 MB): maps, scripts and graphics, used for measurements only. The findings are in the docs above.
- **The Essentials v21.1 and EBDX base projects** (about 1 GB): public downloads, linked in [`docs/SETUP.md`](../docs/SETUP.md).
- **Bulk sprite dumps** (about 1.1 GB): all Showdown BW fronts, 360 VS busts and similar. They're public at the sources in `LINKS.md`.

## Gemini's suggestions
Put proposals in [`gemini_recommends/`](../gemini_recommends/). That folder's README explains the format and how Claude reviews them.
