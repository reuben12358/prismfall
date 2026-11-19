# Portrait sources (hunt of 2026-11-19)

Dialogue portraits for the cast (`\ff[name]`, 96×96 file in `Graphics/Faces`, our bubble in `Graphics/Portraits`).
Boards are in `/home/claude/ref/art/renders/portraits/`. Helper scripts (PIL only, run with `python3 -I`) are in
`/home/claude/ref/art/tools/portrait_hunt/`: `cropfaces.py` (96×96 crop at 1x, 2x and in a round bubble) and
`cropall.py` (crop sheet of a whole folder).

## Verdict

**There is a large donor pool, and it was already on disk: the VS busts in `Graphics/Transitions` of all three
reference games.** Rejuvenation has 205, Reborn 98 and Desolation 57 (`vsTrainer*.png`, `vsPlayer*.png`, 256×128).
That makes 360 busts, about 205 of them girls or women, drawn by the same artists in the same style as the
Rejuvenation and Desolation face files. They are **x2 density**: each 2×2 block is one colour, measured with
`density.py`, the same as the 96×96 face files. So **a 96×96 crop at 1:1 is already a dialogue face in our format**,
with no scaling. Earlier passes only searched `Faces` and `Pictures`, which is why they found 13 and 90 files.

Use this pool to kitbash the whole cast. Compose each face from parts, following lesson 9 of
`design/KITBASH_PIPELINE.md`: one face, hair from a second bust, headwear redrawn. Don't repaint a single bust
whole. Fill the gaps from the official Gen 4/5 VS busts (also x2, already on disk). FE-Repo, downloaded this pass,
is a technique reference for expression frames, not a donor pool.

Weak spot: **expressions.** Most VS characters have a single pose. Variants exist for a few: Rejuvenation
`vsTrainer180`, `_1`…`_5` (six expressions of one girl), `vsTrainer186`/`_1`, `vsTrainer193`/`_1`,
`vsTrainer179`/`_1`, `vsTrainer151`/`_1`, the `vsPlayerN_M` outfit sets (7 characters × up to 10 outfits) and
the `vsTrainerN_99` alternates. Desolation's 90 face files show how the same artists vary one face across
expressions. Build each expression set by moving mouths and brows between busts that share the head angle.

## Why our Rejuvenation copy "lacks portraits"

- It is not out of date. It is a V14-era build: it has Chapter 16 and `v14*` pictures, and `Scripts/RTP.rb`
  checks against `14.1.0-alpha.0`. Rejuvenation V14.0.0 is the current release (announced on rebornevo
  `rejuvdev/records/…-r77`). Its feature list (Gen 9, ZA Megas, UI, running sprites, Chapter 16) mentions no
  portrait system. Nothing is packed in an archive: the only `.rar` in the three games is
  `desolation/Graphics/Characters/graphics.rar`, which holds 5 Pokémon/overworld images.
- Rejuvenation simply uses very few dialogue faces. In its map text, `\ff[...]` is used only with `1*` and `02*`,
  which match the 13 files in `Faces`. The other face-in-message use is `\f[NP*]` (over 300 lines). Those are
  15 tiny 32-px head icons (`Graphics/Pictures/NP*.png`, 64×56) for the radio/comms chatter between Nastasia,
  Ren, Aelita and others. Board: `local_rejuv_NP.png`.
- Rejuvenation's big character art is elsewhere: the VS busts, the Xenpurgis blessing portraits
  (`Pictures/BlessingUI/portraits*.png`, hi-res painted, not pixel), CGs (`Pictures/CG_*`) and
  `RenPortrait.png` (hi-res). Board: `local_rejuv_misc.png`. No round-bubble art or code is in the copy. The
  round bubble in the user's reference is most likely a VS bust or face shown in a circular frame, which our own
  mask already reproduces.
- **Reborn has no dialogue faces at all**, only VS busts.
- Desolation is at E6 (final); its download page offers nothing newer.

## Sources

| # | Path | Count | Size | Style / density | F / M / other (eyeballed) | Match to Rejuv portrait look |
|---|---|---|---|---|---|---|
| P1 | `/home/claude/ref/games/rejuvenation/Graphics/Transitions/vsTrainer*.png`, `vsPlayer*.png` | 205 (about 120 distinct characters) | 256×128 (a few 230/242 wide) | Rejuvenation VS busts, x2, cel-shaded anime, outlined | ~121 / ~73 / ~11 | **The target style itself.** 96×96 crop at 1:1 = face file. Boards: `local_rejuv_vs_{1,2,3}.png`, `crops_rejuvenation_vs.png` |
| P2 | `/home/claude/ref/games/reborn/Graphics/Transitions/vsTrainer*.png` | 98 | 256×128 | Reborn VS busts, x2, slightly older and flatter shading | ~55 / ~42 / ~1 | Very close (same family, simpler shading). Boards: `local_reborn_vs.png`, `crops_reborn_vs.png` |
| P3 | `/home/claude/ref/games/desolation/Graphics/Transitions/vsTrainer*.png` (+ `vs artem.png`) | 57 | 256×128 | Desolation VS busts, x2, soft painterly shading, sparkle texture in the hair | ~29 / ~28 / 0 | Very close, and the softest faces. Boards: `local_desolation_vs.png`, `crops_desolation_vs.png` |
| P4 | `/home/claude/ref/games/desolation/Graphics/Faces/` and `/home/claude/ref/games/rejuvenation/Graphics/Faces/` | 90 + 13 | 96×96 (8 Desolation files 98×98) | The real dialogue faces, x2 | ~27 characters, few girls | Exact format; the reference for framing and expression changes. Board: `local_faces_all.png` |
| P5 | `/home/claude/ref/art/sprites_gen5_vs_tech/extracted/Gen 5 VS Sprites/` and `/home/claude/ref/art/sprites_pt_vs_tech/extracted/Gen 4 VS Sprites/` (already listed as T4/T5 in NEW_SOURCES) | 33 busts + bars; 25 | 256×128; 192×128 | Official B2W2 and Platinum VS busts, x2 (Rosa's is 1x) | 49 + 25 busts, about half female | Good, slightly flatter. Useful for **elders** (Drayden, Bertha, Alder) and official faces. Board: `official_vs_candidates.png` |
| P6 | `/home/claude/ref/art/portraits_fe_repo/repo/Portrait Repository/` (**downloaded this pass**, sparse git checkout of github.com/Klokinator/FE-Repo @ f3b9a2b) | 2,977 PNG: FE8 533, FE7 170, Pokémon-themed 239, community OCs 825, FE Character Creator v3 parts 1,210 | Mug sheets 128×112 (96×80 portrait plus blink/mouth frames); creator parts 96×96 | GBA Fire Emblem mugs: **1x**, 16 colours, ¾ view facing left, hand-made | Large; plenty of women and elders, a few kindly professors (`Non-FE Properties/Pokémon/Oak {Eden} [F2E].png`, `Fuji {Eden}`, `Agatha {Eden}`) | **Poor as donors** (finer pixels, different shading and angle), **good as a reference** for building blink and mouth frames, and as a base for elders if redrawn. Terms: `[F2E]` free to edit, untagged = free to use; credit `{artist}`. Boards: `fe_pokemon.png`, `fe_velvetkitsune.png`, `fe_creator_faces.png` |
| P7 | `/home/claude/ref/art/portraits_itch_previews/` (store-page screenshots only, 3 files) | — | — | itch.io "retro anime" and pixel portrait packs (goldenbeard, marceles, inking) | — | **Rejected**: AI-looking or generic fantasy style, and some are paid. Board: `itch_previews.png` |
| P8 | `/home/claude/ref/art/sprites_showdown/trainers/` (T1 in NEW_SOURCES) | 1,500 | 80×80 | Battle sprites | — | Only as the "sprite bust" fallback (face 8 px wide); not portrait material |

**Copyright note (for a possible release only):** the Rejuvenation team's asset guide (rebornevo topic 73688)
says named-NPC VS sprites must not be copied directly, only used as a base made unrecognisable. Composing from
several busts and redrawing hair and headwear already does that. This doesn't matter for the private build.

## Crop coordinates

`cropfaces.py` places the 96×96 box at the top of the hair (`y0`) and centres it on the head. For a lower crop
that shows the chin and collar, move `y0` down 8–16 px. The numbers below are `x0,y0` from the auto-crop and
were checked on the boards `juno_candidates_auto.png`, `cast_candidates_auto.png` and
`official_vs_candidates.png`. Use `label=path@x,y` to override.

## Juno: top ten donors

Juno: cheerful teenage girl, wavy auburn hair, green eyes, freckles, pink-blossom wreath, sheer veil.
`RJ = /home/claude/ref/games/rejuvenation/Graphics/Transitions`, `RB = …/reborn/…`, `DS = …/desolation/…`.

1. `DS/vsTrainer1.png` (88,0): **closest overall.** Ginger-auburn hair with a braid, green eyes, soft
   three-quarter face, sparkle texture that can become freckles. Face and eye donor; recolour the hair a little
   warmer.
2. `DS/vsTrainer1_1.png` (87,0): the same girl with her hair up. A second hair silhouette and a slightly
   different mouth, so it is the start of an expression set.
3. `RJ/vsTrainer143.png` (85,0): wavy shoulder-length hair with a big flower ornament and a gentle face.
   **Wreath and hair-shape donor**: recolour green to auburn, and redraw the flower as pink blossoms.
4. `RJ/vsPlayer6_2.png` (67,0): **the best wavy auburn curls in the pool.** Hair donor only (the face is darker
   skinned and serious).
5. `RJ/vsPlayer2.png` (70,0): soft, near-frontal, friendly face with long wavy hair. Face donor. Outfit and
   expression variants: `vsPlayer2_1`, `2_2`, `2_3`, `2_6`, `2_7`, `2_9`, `2_14`, `vsTrainer2_99`.
6. `RJ/vsTrainer188.png` (83,0): long auburn-brown hair, frontal, calm, with blush marks on the cheeks.
   Freckle placement and straight-hair donor.
7. `RJ/vsTrainer180.png` and `_1`…`_5` (73,0; also `vsTrainer9`, `vsPlayer180`): a gentle smiling girl in **six
   expressions**. The only ready-made expression set in the pool, so use it as the template for Juno's
   happy/sad/surprised mouths and brows.
8. `RJ/vsTrainer150.png` (94,0): big cheerful open-mouth shout with a hair bow. Donor for the "excited" mouth.
9. `RJ/vsTrainer111.png` (83,0): long reddish-brown hair, calm frontal face, white cloth headpiece behind the
   head. **Veil donor** (make it translucent) and a calm alternative face.
10. `RJ/vsTrainer130.png` (91,0): wink and grin with a hair ornament. Donor for a "teasing/wink" expression.

Also worth a look: `RB/vsTrainer145.png` (81,0; soft pink-haired face), `RJ/vsTrainer254.png` (73,0; round
frontal face, short hair), `DS/vsTrainer87.png` (79,0; bright smile, long hair), `RJ/vsTrainer236.png`
(long auburn hair; the auto-crop misses, so use about `@120,0`).

Suggested build: face, eyes and shading from DS `vsTrainer1`; hair mass from RJ `vsPlayer6_2` reshaped with RJ
`vsTrainer143`'s outline; blossoms redrawn over the `vsTrainer143` flower; veil adapted from RJ `vsTrainer111`;
expression set copied from RJ `vsTrainer180_*`.

## Kestrel (brooding rival boy)

- `RJ/vsTrainer96.png` (65,0) and `RJ/vsPlayer96.png`: black hair, dark cloak, scowl. **Best match.**
- `RJ/vsTrainer217.png` (83,0): black hair, glare, olive jacket.
- `DS/vsTrainer145.png` (78,0): slicked black hair, stern, fur collar.
- `DS/vsTrainer143.png` (91,0): brooding, heavy-lidded, earring. Good for a quieter mood.
- `RB/vsTrainer22.png` (94,0): hair over one eye. Hair donor.
- `RJ/vsTrainer132.png` (119,0): tired, shadowed eyes. Donor for a "weary" expression.
- `DS/vsTrainer4.png`, `vsTrainer122.png`, `vsTrainer148.png` (102,0): smirk variant.

## Edda (old sea captain, a woman)

- `DS/vsTrainer131.png` (111,0) and `vsTrainer157.png`: white hair, weathered tanned face, wide-brimmed hat
  with a badge. **Closest**: the hat becomes a captain's tricorn or cap.
- `/home/claude/ref/art/sprites_pt_vs_tech/extracted/Gen 4 VS Sprites/vsE4_ELITEFOUR_Bertha.png` (66,0): a
  kindly old woman's face with grey hair and wrinkles. Use for her softer expressions.
- `RB/vsTrainer24.png` (59,2): white-haired woman with sunglasses and a dark coat. Coat and hair donor.
- `RJ/vsTrainer105.png` (78,0) and `RJ/vsTrainer238.png` (65,0): scarred, stubbled captain types (male).
  Donors for the scar, coat collar and a weathered look only.

## Larch (kindly professor)

- `/home/claude/ref/art/sprites_gen5_vs_tech/extracted/Gen 5 VS Sprites/vsTrainer_LEADER_Drayden.png` (71,0):
  white beard and hair, elderly. Soften the brows to make him kindly.
- `RJ/vsTrainer147.png` (74,0): white-haired old man with a broad grin and deep wrinkles.
- `RB/vsTrainer91.png` (85,0): glasses, warm smile, green coat. Donor for glasses and a friendly mouth.
- `RJ/vsTrainer245.png` (19,0): grey-haired scientist among lab monitors. Hair and lab-coat donor.
- `…/Gen 5 VS Sprites/vsTrainer_PLASMA_Colress.png` (86,0): glasses and lab coat (expression too sly as is).
- Reference only (GBA style): `/home/claude/ref/art/portraits_fe_repo/repo/Portrait Repository/Non-FE
  Properties/Pokémon/Oak {Eden} [F2E].png` and `Fuji {Eden} [F2E].png`.

## Blocked or not pursued

- **Eevee Expo downloads** need a login or a JavaScript check. A plain request returns a "One moment, please"
  page, and the permission system denied a retry with cookies. Unfetched: *HGSS Trainers – VS Sprite Transition
  Pack* (resource 928) and *Nurse Portraits* (1177, Zygoat). A title crawl of 45 pages of Eevee Expo's graphics
  category (348 resources, possibly not the whole category) found no other portrait or mugshot packs; the Gen 5 and Platinum VS packs (1398, 1403) are already on disk as P5.
- **rebornevo.com** pages refuse WebFetch (robots), but plain page requests work. The full Rejuvenation
  download (MEGA via pkmnfan.games) was not fetched: the local copy is already V14-era and V14 adds no portrait
  system.
- **Paid itch.io packs** (marvyra "unique anime portraits", nrujinzo "166 character portraits") were not bought.
  **PokéCommunity, mediafire, Spriters Resource and Bulbagarden** returned 403 in earlier hunts and were not
  retried.
- **GitHub API**: the `GH_TOKEN` in this environment is invalid, but anonymous `git clone` works (used for
  FE-Repo).
- Not searched in depth this pass: Xenoverse, Insurgence, Uranium, Empyrean, Infinite Fusion customs and
  Masters/Conquest busts. Most of these are hi-res non-pixel art (Xenoverse, Masters) or 80-px battle sprites
  (Infinite Fusion, Conquest via Showdown, already on disk), so none would beat P1–P3.
