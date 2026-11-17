# CHARACTER ART: trainer sprites, overworlds, portraits

Owner: Character Artist. Status date: 2026-11-16.

## 0. Status

| Character | Battle front | Overworld | Portraits | State |
|---|---|---|---|---|
| PLAYER_A (protagonist, look A) | done | done | 10 expressions | v2 frankensprite, awaiting user review |
| PLAYER_B (protagonist, look B) | done | done | 10 expressions | v2 frankensprite, awaiting user review |
| LARCH | done | done | 10 expressions | v2 frankensprite, awaiting user review |
| KESTREL (`RIVAL_KESTREL`) | done | done | **on hold** | batch 2, sheet `03_kestrel_juno_player_backs.png` |
| JUNO (`RIVAL_JUNO`, `LEADER_JUNO`) | done | done | **on hold** | batch 2 |
| Player back sprites | `PLAYER_A_back`, `PLAYER_B_back` done | | | batch 2 |
| Everyone else | stand-in (`STAND_INS`) | stand-in | engine fallback | **paused** until the user approves v2 |

Review sheet: `art/previews/02_frankensprite_protagonist_larch.png`. It shows the stock sprites beside ours at 1× and 4×, the overworlds at 1× and 3×, and every portrait at 2× and 1×.

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
