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

## 6. Pass 2 (2026-11-18)

Sheet: `art/previews/10_juno_kitbash_pass2.png`. Scripts: `juno_v1_p2.py`, `juno_v2_p2.py`, `juno_v3_p2.py`, `juno_portrait_p2.py`,
`sheet10.py`. Exports carry `_p2`; pass-1 files are untouched.

- **Hair grafts work when the donor is flipped to match the head angle and the figure is drawn on top**: Sonia's ponytail on the
  Backpacker head, the Lass's whole head on the Parasol Lady body (offset found by lining up the eyes).
- **Translucency:** where a sheer layer crosses hair, blend 50% and re-run `reduce_colours`. A hand-built polygon veil looked like a
  stiff cone and was dropped for two lengths of the donor tail.
- **Expression lifts:** copy only teeth and lip-line colours from another face set; drop its skin.
- **Slot size:** EBDX draws trainers at `TRAINER_SPRITE_SCALE = 1`, anchored bottom-centre, with an optional per-trainer `SpriteScale`
  in `PBS/EBDX/trainers.txt`. A 160x160 front therefore shows 25% larger than the 128x128 stock fronts and keeps its feet on the
  base. Read from code only: no engine screenshot was taken, because the capture rig was running another job.

## 7. Ever-Bloom, the chosen Juno (2026-11-18)

Sheet: `art/previews/11_juno_everbloom.png`; engine frame: `art/previews/11_juno_everbloom_engine.png`.
Scripts: `juno_everbloom.py` (variants A/B/C; A is the pick), `juno_everbloom_portraits.py`, `juno_everbloom_ow.py`, `sheet11.py`.
Installed to `art/out/Graphics/` (Trainers `RIVAL_JUNO`/`LEADER_JUNO`, Characters `JUNO` + `trainer_*`, Portraits `JUNO_*`);
the v3 files they replaced are in `art/work/kitbash/passes/replaced_v3/`.

- **Cloth comes from cloth.** Diantha's cape gave the veil real folds; the Miku tail alone read as ribbon. Capes (`diantha`,
  `lance`, `olympia`, `wallace-masters`) are the veil/cloak library.
- **Head swaps carry the expression.** Line up the eyes, erase the old head down to the jaw, keep the base's back hair behind.
- **Slot size, confirmed in engine:** a 160x160 front at `TRAINER_SPRITE_SCALE = 1` sits on the base correctly in an EBDX intro. No
  `SpriteScale` entry is needed. Captured with a private rig copy: `RUN=/home/claude/run_juno` (build symlinked), `PACKAGE=0 …
  assemble`, graphic copied into the copy's `Graphics/Trainers`, a `juno` plan added to the copy's autorun, `ISOLATE=1 DISPLAY_NUM=93 … run juno`.
- **Overworld:** 30x32-px frames (file 240x256). At that size the wreath is 7 pixels and the veil a sheer strip; keep expectations low.

## 8. Ever-Bloom pass 2 (2026-11-19)

Sheet: `art/previews/12_juno_everbloom_p2.png`, engine frames `art/previews/12_engine_*.png`. Scripts: `juno_everbloom_p2.py`,
`juno_everbloom_portraits_p2.py`, `juno_everbloom_ow_p2.py`, `sheet12.py`. Installed over pass 1 in `art/out/Graphics/`.

- **Pick the face donor for temperament first.** Desolation's face set 08 is a cool, intense character and no repaint fixes that.
  The B2W2 VS busts are 128x64 native, so a 48x48 crop at 1:1 is already a portrait in our format. Burgh = warm open beam.
- **Charset convention is 128x192** (16x24-px frames doubled), as in the base project. Donors: `ebdx_renovation/Graphics/Characters/trainer_*.png`.
  The Gen 5 rips (30x32 frames) do not fit.
- **Portrait bubbles work in engine** through `pbMessage("[portrait: JUNO, happy] …")` with files in `Graphics/Portraits/`.
- **Arm grafts** need a donor arm at the same shoulder angle and sleeve; the Parasol Lady arm on the Lady torso failed.
- Not verified: charset on a map (setting the player's `character_name` in the autorun was overridden and the rig's start map
  renders black), and an EBDX VS-bar transition (a `BattleVS = trainerSM` line in the copy's `PBS/EBDX/trainers.txt` had no visible
  effect; only the default ball wipe played).

## 9. Portrait pass 3 and front pass 3 (2026-11-19)

Sheet: `art/previews/13_juno_portraits.png`. Scripts: `juno_portraits_p3.py` (candidates A/B/C, expressions on A), `sheet13.py`;
front `eb_P3` comes from `juno_everbloom_p2.py` (`build(False, ribbon=True)`). Front installed; **portraits not installed** (the
rejected Burgh-based set is still in `art/out/Graphics/Portraits/`).

- **A whole recognisable bust repainted is a wig job.** Compose instead: one face, back hair from another bust, headwear replaced.
- **Hats can be repainted as a hair crown** and hidden under the wreath, but the dome shape survives and reads as a bonnet.
- **Mouths do not transplant between busts** unless the head angles match; Skyla's and Iris's failed on a frontal face.
- **Charset in engine:** overriding `$game_player.character_name` with a singleton method makes the walker use the sheet, and
  128x192 frames display correctly. The rig's autorun does not draw map tiles, so "on a lit map" is still unverified.

## 10. How the reference games draw portraits, and sprite busts (2026-11-19)

Sheet: `art/previews/14_juno_portraits.png`. Script: `juno_portraits_p4.py`, `sheet14.py`.

- **Rejuvenation and Desolation both use the stock Essentials face tag**: `\ff[name,index]` in message text (`Scripts/Messages.rb`,
  class `FaceWindowVX`) loads `Graphics/Faces/<name>.png`, falls back to `Graphics/Pictures/<name>.png`, and shows a 96x96 cell in a
  square window to the left of the message box. `\f[name]` shows a whole picture from `Graphics/Pictures`. These are dedicated,
  hand-drawn portrait files, not crops of trainer or overworld sprites. No round-bubble code or art was found in either copy.
- **Pool size:** our Rejuvenation copy has 13 face files (2 characters), Desolation 90 (about 27 characters, few of them girls).
  `Graphics/Pictures` holds no further portrait sets in either game. There is no larger donor pool on disk.
- **Sprite busts** (32x32 crop of the 80-px front, x3): match the battle sprite exactly, but the face is 8 px wide, so expressions
  barely differ and the pixels are 1.5x coarser than a 48-px portrait. Usable as a consistent fallback, not as Rejuvenation-style art.
- Installed portraits: the pass-3 composite A set (stopgap, replaces the Burgh-based set).

## 11. Portrait pass 5, rejected (2026-11-19)

Sheet: `art/previews/15_juno_portraits.png`. Script: `juno_portraits_p5.py`, `sheet15.py`. Composite A's look was rebuilt on a
Rejuvenation VS-bust face (RJ `vsTrainer150` face/fringe, `vsTrainer143` bloom, `vsPlayer6_2` curls, hand mouths for five
expressions). It was installed and then reverted: the pass-3 set is back in `art/out/Graphics/Portraits/`, pass 5 is in
`passes/replaced_p5_portraits/`.

- **Taste lesson:** the user prefers the cleaner, brighter, bigger-eyed **official B2W2-VS look** of pass 3 ("she looks damn
  near cool in that") over the realistic, painterly Rejuvenation/Desolation faces. Matching the reference games' shading depth is
  not the goal on its own. Pass 5 "reads like Burgh" to him (the pass-2 Burgh set left a bad memory, and the 3/4 tilted grin
  with a big hair mass brought it back).
- **Anything that reads even slightly like a known character fails.** Before showing any face or sprite, ask "who does this look
  like?" and check against the obvious official characters (Burgh, Rosa, Hilda, Bianca...) as well as the donors.
- Polish of an accepted look stays inside that look: keep face, eyes and style exactly; only fix the listed faults.

## 12. Pass-3 hair fix (2026-11-19)

Sheet: `art/previews/16_juno_hair_fix.png`. Script: `juno_hair_fix.py` (`sheet16h.py`). Outputs `JUNO_<expr>_p3h.png`, installed;
the previous files are in `passes/replaced_p3_before_hairfix/`. Only hair pixels change (checked: 0 non-hair pixels differ).
- The choppy look came from Rosa's hat lines and Hilda's strand lines: black 1-px stripes inside the mass, two flat colours.
- Fix: classify hair (3 hair colours + black pixels that touch only hair), fill stair-step notches / cut spurs against empty space,
  then re-shade procedurally: locks radiate from a crown point above the frame with a slight wave, each lock lit on one side and
  falling into a crease (sawtooth profile), 4 shades (pass 3's own two plus one darker, one lighter), one highlight arc that
  follows the dome and breaks at the creases. Black stays only on the outer silhouette.
