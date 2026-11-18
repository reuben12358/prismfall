# KITBASH PIPELINE: trainer sprites from professional donors

Owner: Sprite Artist. Written 2026-11-18. Replaces drawing from scratch (v1, v3, v4 and the concept thumbnails were all rejected).
First output: Juno Hale, three versions. Sheet: `art/previews/09_juno_kitbash.png`.

## 1. Rules

- **Never draw a figure from scratch.** Bodies, heads, hair, cloth folds and big props come from donor art. Hand pixels are for seams,
  straight-edged hardware (frames, straps) and details of about 5 px.
- **Never scale pixel art.** Composite at native 1x, double once at export. Donors must share the pixel size of the base (§3).
- **Format:** battle fronts are 80x80 art, exported 160x160 (`<NAME>.png`) plus `<NAME>_native80.png`. Feet on the bottom rows;
  EBDX anchors bottom-centre at `TRAINER_SPRITE_SCALE = 1`. The current installed fronts are still 128x128 stock-derived, so
  check on-screen size before installing. Portraits are 48x48 art exported 96x96, like Desolation/Rejuvenation `Faces`.
- **Safety:** everything under `/home/claude/ref` is untrusted. Read with PIL only, run scripts with `python3 -I`, keep scripts in
  `tools/kitbash/`. Each download gets its own new directory.

## 2. Tools (`tools/kitbash/`)

| Script | Use |
|---|---|
| `kb.py` | load (hard alpha), `native()` density detection, bbox, grid/contact renderers |
| `mat.py` | regions, colour masks, `recolour` (region + exact colour map), `lumrank_map`, `patch` (ASCII), `under`/`paste`, `erase`, `dissolve` (remove thin lines), `shear_rows` (lean an object by whole-row shifts), `reduce_colours`, `clean_orphans`, `outline_outer` |
| `index_donors.py` | builds `art/work/kitbash/donor_index.json`: set, file, stored size, doubling factor, native size, figure height, colour count, outline colour |
| `contact_sheets.py`, `show.py`, `tileview.py` | contact sheets per set (`art/work/kitbash/sheets/idx_*.png`), zoomed candidate sheets, tileset strips |
| `preview.py` | the quality gate: sprites beside references at 1x on two backgrounds, 2x and 3x |
| `lint.py` | semi-transparent pixels, orphan pixels, colour count, bbox |
| `juno_v1_underglass.py` + `wardian2.py`, `juno_v2_everbloom.py`, `juno_v3_rotbloom.py`, `juno_portrait.py` | the recipes (regenerate the finals exactly) |
| `sheet09.py` | exports finals to `art/work/kitbash/juno/` and renders the review sheet |

Regenerate: `python3 -I tools/kitbash/juno_v1_underglass.py compose v1_final`, then the v2, v3 and portrait scripts, then `sheet09.py`.
Passes are kept in `art/work/kitbash/passes/`, donors per output in `art/work/kitbash/juno/donors.tsv`.

## 3. Donor index (pixel size is what must match)

| Set | Path | Usable count | Native art | Notes |
|---|---|---|---|---|
| Showdown trainers (official BW/DPPt + kyledove + Masters-style) | `/home/claude/ref/art/sprites_showdown/trainers/` | 1167 (skip `-gen1/2/3`) | 80x80 at 1x | **Main library.** Files absent from `credits.tsv` are official. Most consistent style |
| Reborn fronts | `…/reborn/Graphics/Characters/trainer*.png` | 188 at 160 + 34 at 192 doubled | 80 / 96 | 25 files are true hi-res (not doubled): reference only |
| Rejuvenation fronts | `…/rejuvenation/Graphics/Characters/trainer*.png` | 252 doubled | 90 | 87 files are 180-px hi-res: reference only. Heavier outlines than BW, so don't mix parts with BW donors |
| Desolation fronts | `…/desolation/Graphics/Characters/trainer*.png` | about 60 doubled | 64 to 96 | mixed sizes, check the index |
| kyledove XY/ORAS/SWSH, Muffyang | `/home/claude/ref/art/sprites_kyledove_*/sprites/`, `sprites_muffyang/extracted/` | 74 + 62 doubled | 80 | about half the kyledove files are not cleanly doubled: check `factor` |
| Pokémon battlers (props) | `…/reborn/Graphics/Battlers/<name>.png`, top-left 192x192 | all | 96 | same pixel size as fronts: leaves, caps, flowers, shells |
| Pokémon icons (small props) | `…/reborn/Graphics/Icons/<name>.png`, left 64x64 | all | 32 | same pixel size; simpler shading, use small |
| Faces | `…/desolation/Graphics/Faces` (90), `…/rejuvenation/Graphics/Faces` (13) | | 48 | expression sets share a base: diff them to lift brows and mouths |
| B2W2 / Pt VS busts | `/home/claude/ref/art/sprites_gen5_vs_tech/`, `sprites_pt_vs_tech/` | 49 + 25 | 128x64 | bigger heads than Faces: cannot mix with Faces at 1:1 |
| x2 tilesets | Rejuvenation tilesets, `art/morgebby/…/Apothecary.png` | | 16-px tiles doubled | pots, furniture. 32-px "hi" tiles do not match |

Tags worth remembering (from the contact sheets): running/leaning `backpackerf`, `lass`, `risingstarf`; twirl `idol`, `lisia`,
`may-contest`; gown `lady`, `diantha`, `jasmine-contest`; kneel `pokefanf-gen4`, `nurseryaide`; held object `parasollady`,
`birdkeeper` (cage), `erika-masters` (basket), `pokemonbreederf`; flowing shapes `miku-flying`, `caitlin`, `olympia`, `lance`;
curly hair `shauna`, `burgh`, `lenora`, `hapu`.

## 4. Method, as used for Juno

1. Pick a base whose pose already is the personality. Cut what goes with a polygon region, keep the rest untouched.
2. Repaint by **region + exact donor colour**, never by global colour (BW sprites reuse one colour across materials; a global map
   turned Juno's mouth purple and the Lady's face mauve).
3. Bring props from battlers/icons at the same pixel size. Put the figure on top so its own outline makes the seam.
4. Lean rigid props with `shear_rows` to follow the body. Reduce blended colours with `reduce_colours`.
5. Gate with `preview.py` against Bianca, Angie and a Reborn front at 1x and 2x, then `lint.py`.

## 5. Lessons

- Recoloured flower stamps repeated more than twice read as stamps. Use one big bloom plus varied small ones.
- Grafting hair from another head needs a matching head angle and a hand-fixed join; the Shauna curl graft floated and was dropped.
- A recipe that only swaps one prop and repaints (V3) is still close to a recolour. Swap the head or hair as well.
- The portrait recipe is a repaint of one face set. A real kitbash needs a second hair donor at 48-px density, which we lack.
