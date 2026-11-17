# CHARACTER ART: trainer sprites, overworlds, portraits

Owner: Character Artist. Status date: 2026-11-16.

## 0a. v4 (2026-11-17): Juno drawn from scratch, pixel by pixel

- **Method:** read tutorials and dumped the references pixel by pixel, written up as a checklist in `design/PIXEL_ART_NOTES.md`. Then a
  flat block-in for pose and proportion (`art/tools/v4/juno_block.py`), a directional underpaint as a starting point (`underpaint.py`),
  and 9 rounds of hand edits. Every pixel was placed through patches (`art/work/v4/pat_r*.txt`) on a text canvas
  (`art/work/v4/juno.spr`, one char per pixel, rows numbered). Toolkit: `art/tools/v4/px4.py` (render beside references, lint, grid,
  patch).
- **Format:** 80×80 native (Reborn's size), stored doubled at 160×160, 25 colours, selective outlines, light from the upper left.
- **Design change:** bare hands, with the gardening gloves clipped to the waistband, as `story/03_CAST.md` says. Oversized gloves on the
  ball hand read as an ice-cream cone or a trophy at 80 px (rounds 5–6).
- **Files:** `art/out/v4/Trainers/JUNO_v4.png` (160×160) and `JUNO_v4_native80.png`. **Not installed**: `RIVAL_JUNO.png` is still v3.
  The v4 file is 160×160 while the current slots are 128×128, so check EBDX's on-screen size and alignment before swapping.
- **Review sheets:** `art/previews/07_v4_juno_final.png`, `art/previews/v4_rounds/` (every round, `progression_juno_v4.png`, and
  `test_rejuv_edit.png`).
- **Rejuvenation-edit test** (`art/tools/v4/rejuv_edit_test.py`): Rejuvenation `trainer002`, recoloured to Juno's palette, with the v4
  head. The body gains their more dynamic arms and sleeve folds, but it is recognisably trainer002's pose and outfit, the same
  problem as v2. Use their sprites as traced pose underdrawings, not as bases.

## 0. Status (v3, 2026-11-16)

User direction: stock sprites are **pose skeletons only**. Each character is redrawn to its design sheet (§8): head, face, hair,
proportions, outfit, props. Recolouring is not enough.

| Character | Battle front | Overworld | Portraits | State |
|---|---|---|---|---|
| KESTREL | **v3** hand-drawn on Lance's lunge | **v3** (new heads and coat on Lance's walk frames) | not started for v3 | sheets 04, 05 |
| JUNO | **v3** hand-drawn on May's stance | **v3** (new heads and dungarees on May's walk frames) | not started for v3 | sheets 04, 05 |
| PLAYER_A | **v3** hand-drawn on Red's throw (Red's legs and ball hand repainted) | v2 (recolour; to redo) | v2 (Blue-based; to redo for the v3 design) | sheet 06 |
| PLAYER_B, LARCH | v2 (recolour; to redo) | v2 | v2 | queued |
| Player back sprites | v2 (recolour; to redo for the v3 designs) | | | queued |
| TAMSIN, VOSS, ROWAN/MOURNER, EDDA, CALLA, THISTLE | stand-in | stand-in | fallback | designs in §8, queued |

v3 method: the head, upper body and outfit are hand-placed pixels in ASCII grids (`art/tools/fr/chars/<name>.py`: a legend plus
per-row spans), followed by an automatic edge-light pass (`shade.py`: light from the upper left). Limbs may be kept from the pose
source, but only repainted. Overworld heads are hand-drawn 16×16 stamps per direction (`ow3.py`), with right mirrored from left.
Review sheets: `04_kestrel_juno_v3_rebuild.png`, `05_kestrel_juno_v3_overworld.png`, `06_v3_kestrel_juno_player_a.png`.

**v1 was rejected.** The user rejected the first, parametric approach (characters drawn from scratch by code). Its output is quarantined in
`art/rejected_parametric_v1/` (files, previews and the old `art/tools/*.py` pipeline). **Do not install anything from it.**
The old `cast*.py` files are still useful as a design reference: they record each character's palette, outfit and signature details.

## 1. Method (v2): frankensprites from hand-drawn stock art

This is the standard fangame technique. Pick the closest hand-drawn stock bodies and poses, cut and combine their parts, repaint them to the
character's design (story/03_CAST.md), then fix seams and add signature details pixel by pixel. All source art is read-only in
`/home/claude/ref/ebdx_renovation/Graphics/`. Nothing there is modified; the scripts read it and write new files.

| Asset | Size on disk | Sources used |
|---|---|---|
| Battle front | 128×128 (64×64 art, doubled, like stock) | `Graphics/Trainers/*.png` (78 Gen 4/5 fronts) |
| Overworld | 128×192, 4×4 walk sheet (down, left, right, up × 4 frames) | `Graphics/Characters/trainer_*.png` |
| Portrait | **96×96 native** | HGSS VS busts `Graphics/Transitions/hgss_vs_*.png`, `vsE4_*.png` (96×64 art), Scale2x-upscaled to 96-native, then hand-patched |

Per-character recipes:
- **PLAYER_A**: Brendan's front body with RIVAL1's head. Hair recoloured ash-violet and eyes teal. Brendan's jacket recoloured to the
  off-white jacket with a teal scarf collar and cuffs, brown satchel strap, charcoal trousers and teal shoes. The overworld is RIVAL1's
  charset head on Brendan's charset body. The portrait is Blue's HGSS VS bust, recoloured to match.
- **PLAYER_B**: Leaf's front body and long back hair with LASS's head. Hair plum with a teal clip, a white top, a hand-drawn teal
  neckerchief, a charcoal skirt, teal socks and a leather satchel. The overworld is LASS's charset with the same recolour and a
  neckerchief pixel. The portrait is Misty's VS bust: plum hair, teal eyes, the jacket turned white with a teal collar, and rosier
  cheek shadows.
- **LARCH**: the SCIENTIST front, a running pose with glasses. Mustard oilskin coat, grey hair, slate shirt and green-grey trousers.
  The flask now holds green kelp tea with steam. A hand-drawn grey braid flies out behind her, with a sidelock framing the face. The
  overworld is SCIENTIST's charset recoloured, with a hand-placed braid in the left, right and up rows. The portrait is Erika's VS
  bust: grey hair (the headband repainted as hair), reading glasses on a chain, eye bags, a hand-drawn plaited braid with a red tie,
  and an oilskin collar.

- **KESTREL**: Lance's lunging, pointing pose. The cape becomes his oversized black coat with a wine lining, the bodysuit a dark crimson
  shirt, and the hair dark slate. The overworld is Lance's charset, recoloured the same way. Weakness: Lance's build is adult and broad,
  not a lean 16-year-old.
- **JUNO**: May's wide-stance pose. The bandana becomes a mustard kerchief; she has auburn hair, a green shirt, khaki and brown shorts,
  tan gardening gloves, a leather satchel (May's waist pack), freckles and brown boots. The overworld is May's charset recoloured.
- **Back sprites**: `PLAYER_A_back` is Brendan's back strip, with the beanie recoloured into spiky ash hair, a white jacket, teal trim
  and a brown pack. `PLAYER_B_back` is May's back strip with plum hair (the bandana painted as hair) and a white top. Both keep the
  stock format: 5 throw frames of 80×80, stored doubled at 800×160.

Portrait expressions (`art/tools/fr/exprs.py`) only touch the eyes, brows and mouth. Each face has a model (`models.py`) giving its
eye boxes, brow lines, mouth box, skin ramp and iris colours. Ops: erase a feature (refilled from neighbouring skin, row by row),
closed eyes (`^ u > <`), lowered lids, small pupils, panic eye rings, new brows (never drawn over hair), and drawn mouths (line,
smile, frown, smirk, o, shout, wail, grit, wobble, wavy), plus tears, blush hatching and gloom lines. Everything else in the image is
the original hand-drawn bust.

## 2. Regenerate

```
cd art/tools/fr
python3 export.py                 # writes art/out/Graphics/{Trainers,Characters,Portraits}
python3 sheet.py ../../previews/02_frankensprite_protagonist_larch.png   # review sheet
python3 zoom.py OUT.png 10 [crop=x0,y0,x1,y1] FILE.png ...              # pixel grid for planning edits
```
Scripts: `fs.py` (toolkit: load, palette, remap, ramp_map, masks, copy, ASCII `patch`), `pc_a.py`, `pc_b.py`, `larch.py` (fronts),
`ow_fr.py` (charsets), `up.py` (Scale2x), `busts.py` (bust bases), `exprs.py` + `models.py` (expressions),
`render_busts.py`, `sheet.py`, `export.py`.

## 3. Hand-editing

- Edit the PNGs in `art/out/Graphics/` directly in any pixel editor (Aseprite, GraphicsGale). Edit at native size: halve the fronts and
  charsets, which are stored doubled, then double them again with nearest-neighbour when you save. Portraits are already native.
- Add every hand-edited file's path relative to `Graphics/` (e.g. `Portraits/LARCH_crying.png`) to `art/tools/fr/locked.txt`.
  `export.py` never overwrites a locked file.
- Small edits can also go into the recipes as ASCII patches (`patch(a, x, y, rows, legend)`, where `.` keeps a pixel and `_` clears
  it). That keeps them regenerable.
- Keep each sprite within roughly 16 colours (stock is 11 to 17), with the black `#000000` outline on fronts and `#181820` on busts.

## 4. Install paths and naming

Copy `art/out/Graphics/*` into the game's `Graphics/`:

| File | Used by |
|---|---|
| `Graphics/Trainers/<TRAINERTYPE>.png` | battle front; Cutscenes actor art; portrait fallback crop |
| `Graphics/Characters/trainer_<TRAINERTYPE>.png` | trainer events / Cutscenes actors |
| `Graphics/Characters/<ID>.png` | same sheet under a plain name for NPC events (e.g. `LARCH.png`) |
| `Graphics/Portraits/<ID>_<expression>.png` + `<ID>.png` | `Prismfall Cutscenes` speech bubbles (`[portrait: ID, expr]`); 96×96, transparent background |

Expressions: `neutral happy smug angry crying shocked deadpan panic sad blush`. Own art always beats the `STAND_INS` table in
`plugins/Prismfall Cutscenes/001_Config.rb`.

## 5. Trainer type → file mapping

| Id / trainer type | Files | Status |
|---|---|---|
| `PLAYER_A` | `Trainers/PLAYER_A.png`, `Characters/trainer_PLAYER_A.png`, `Characters/PLAYER_A.png`, `Portraits/PLAYER_A_*.png` | done |
| `PLAYER_B` | same pattern | done |
| `LARCH` (not a trainer; NPC + portraits) | `Trainers/LARCH.png`, `Characters/LARCH.png`, `Characters/trainer_LARCH.png`, `Portraits/LARCH_*.png` | done |
| `RIVAL_JUNO`, `LEADER_JUNO` → `JUNO` | `Trainers/RIVAL_JUNO.png`, `Trainers/LEADER_JUNO.png` (same art), `Characters/trainer_RIVAL_JUNO.png`, `Characters/trainer_LEADER_JUNO.png`, `Characters/JUNO.png` | sprites done; portraits on hold |
| `RIVAL_KESTREL` → `KESTREL` | `Trainers/RIVAL_KESTREL.png`, `Characters/trainer_RIVAL_KESTREL.png`, `Characters/KESTREL.png` | sprites done; portraits on hold |
| player backs | `Trainers/PLAYER_A_back.png`, `Trainers/PLAYER_B_back.png` | done |
| `MERIDIAN_VOSS` → `VOSS`; `LEADER_TAMSIN` → `TAMSIN`; `LEADER_DORIAN` → `DORIAN`; `LEADER_ROWAN` → `ROWAN`; `HOLLOW_MOURNER` → `MOURNER`; `HOLLOW_THISTLE` → `THISTLE`; `HOLLOW_SABLE`/`MERIDIAN_KROLL` → `SABLE`; `HOLLOW_TEO` → `TEO`; `CHAMPION_VALEN` → `VALEN`; `FESTIVAL_SHELLY` → `SHELLY`; `LEADER_<NAME>` → `<NAME>` | `Trainers/<TYPE>.png`, `Characters/trainer_<TYPE>.png`, `Portraits/<ID>_*` | pending |
| Non-trainer speakers: `EDDA CALLA WENNA COLL HESPER WENLOW DEX` | `Characters/<ID>.png`, `Portraits/<ID>_*` | pending |

Integration notes for other plugins and PBS:
- `pbs/trainer_types.txt` has no `PLAYER_A`/`PLAYER_B` yet. The entries to merge, plus the matching `metadata.txt` player blocks, are in
  `art/out/PBS_trainer_types_players.txt`. The Character Artist does not edit `pbs/`.
- For portraits of the player, register the chosen look: `Prismfall::Portrait.register(:PLAYER, ...)` → `PLAYER_A` or `PLAYER_B`.
  The Reflection's portraits can mirror these files.
- **Not yet made for the player:** the run, bike, surf and fish charsets. Until they exist, use the stock `boy_*`/`girl_*` ones.

## 6. Credits

The frankensprites are derived from the base project's Gen 4/5-style trainer fronts and charsets and the HGSS VS busts (Pokémon ©
Nintendo / Game Freak; the sprite rips and edits belong to their respective rippers and artists). Credit them in the game's credits
the same way the base pack's own assets are credited, and add "Prismfall character edits".

## 8. Design sheets (v3: first-hour cast)

User direction (2026-11-16): stock poses may be reused, but **each character is redrawn**: head and face, hair, proportions,
outfit, props. The stock body is only a pose skeleton. The test: next to its stock source, nobody recognises the source character,
only the pose. Rules: a strong two-colour identity, one exaggerated feature that reads at 1×, a readable silhouette, and no two
characters sharing a silhouette or colour pair.
(Exception: PLAYER_A and PLAYER_B are two looks of the same person and never appear together, so they share the PC pair.)

| Character | Colour pair (dominant + accent) | Iconic shape (reads at 1×) | Silhouette | Outfit (faction / personality) | Memorable at a glance |
|---|---|---|---|---|---|
| **PLAYER_A** | chalk white + prism teal | a **long teal scarf** whose frayed tail streams out behind | compact, short spiky ash hair; the scarf tail breaks the outline | white hooded windbreaker (raised abroad, came on the ferry), dark slim trousers, teal-soled boots, beat-up satchel | the "colourless" kid: almost all white, with one teal streak |
| **PLAYER_B** | chalk white + prism teal | the same scarf, tied into the hair as a **long side tail** | long plum hair swept into one big side tail | white windbreaker cropped at the waist, dark shorts over leggings, teal boots, satchel | as A, with a big plum hair shape |
| **LARCH** | oilskin mustard + slate grey | a **rope-thick grey braid to the waist** | tall, thin, A-line knee coat with a big storm collar | fisherman's oilskin (Tidewatch station, sea air) over a slate engineer's shirt, reading glasses on a chain, mug of green kelp tea | yellow coat, a long braid, a steaming green mug |
| **JUNO** | leaf green + marigold | a **huge frizzy auburn hair-cloud** bursting out of a marigold kerchief | round head mass on a small body, wide boots | green dungarees with patched knees, rolled cream shirt, oversized gardening gloves, a satchel spilling seed packets (tiny coloured squares) | the hair cloud and the falling seed packets |
| **KESTREL** | black + crimson | an **oversized black greatcoat**: sleeves past the hands, collar flipped up, tails split like a raptor's tail | lean, sharp V shape; the coat tails flare behind | his mother's coat (a size too big), a crimson undershirt, a crimson feather pin (kestrel), boots; a long lock over one eye | the too-big coat and the split tails |
| **TAMSIN** | cream + moth rose-brown | a **moth-wing shawl** with two big eyespots that opens like wings | slight figure, wide wing-shawl, messy bun stabbed with needles | Briarwick weaver: cream smock, ink-stained fingers, yellow measuring tape round the neck, pincushion bracelet | the eyespot wings |
| **VOSS** | charcoal + gold | a **gold sunburst pin** on a long, sharp suit line | tallest of the cast, very narrow and vertical | bespoke charcoal three-piece with a long overcoat over the shoulders, slicked black hair with silver temples, a chipped white company mug | gold on charcoal; the cheap mug in an expensive hand |
| **ROWAN** | moss green + earth brown | a **wide-brimmed gardener's hat with one white lily** in the band (a fair clue) | lanky, hat brim wider than the shoulders | the Verdance Warden's work clothes: moss field coat, earth-brown trousers, soil-dark gloves, a watering can | the hat with the lily |
| **MOURNER** | ash grey + bone white | a **tall pointed cowl and a pale bark mask with one lily** | tall narrow triangle; the robe hem frays into strips | the Hollow's mourning robe, ash-bark mask, a lily over the brow | a white mask in a grey triangle |
| **EDDA** | navy + rust red | a **red knit watch cap** on a **barrel-shaped** body | squat and round, the widest silhouette | the *Dovetail* captain: navy pea coat with brass buttons, red neckerchief, rolled sleeve showing a Lapras tattoo, gold tooth | a round navy barrel with a red cap |
| **CALLA** | ivory + cobalt | a **severe asymmetric black bob** and a brass handheld scanner with a green lens | narrow pencil line: fitted jacket, pencil skirt | Meridian executive staff uniform (ivory with cobalt piping, sunburst lapel pin), tablet clipboard | the bob and the scanner's green light |
| **THISTLE** | ash grey + thistle purple | **huge weaver's shears** carried like a blade, and a thistle brooch | hooded, hunched forward, shears jutting out | Hollow Pallbearer grey hood and wrap, a purple thistle sash (Lowmarsh weavers), a torn survey flag in the belt | the shears |

Colour pairs in use (check against these before adding anyone): white/teal (PC), mustard/slate, green/marigold, black/crimson,
cream/rose-brown, charcoal/gold, moss/earth, ash/bone, navy/rust, ivory/cobalt, ash/thistle purple.

## 7. Honest assessment (v2)

- **Battle fronts and overworlds:** at 1× they are hard to tell from stock, because they are stock art: recoloured and recombined,
  with a few hand-placed edits. The flip side is recognisability. Brendan's pose, Leaf's body and the Scientist's pose will be familiar
  to Pokémon players. That is normal for fangames, but it is not original drawing.
- **Portraits:** much better than v1, because the base faces, hair and shoulders are hand-drawn HGSS art. The weak points are the
  code-drawn expression features. Brows hide under fringes, so angry and sad lean on lids and mouths. The panic and shocked eyes look
  pasted on. They are still below Rejuvenation's bubble art, which is drawn per expression. Larch reads as "older woman with glasses
  and a braid" but not clearly 56.
- **Scaling to the cast:** the stock pool is small (78 fronts, about 60 trainer charsets, 12 VS busts). With "no two characters share
  a pose", it covers roughly the first 15 to 20 characters before bases have to repeat with heavy repaints. Older characters,
  big-bodied ones (Brann, Coll) and armoured ones (Sigrun) have poor matches.
