# Prismfall: character art handoff (for Gemini or any outside artist)

This pack is everything an outside artist needs to make Prismfall's character art. In-house character art is on hold (SPINE Revision 24).

## The creator's taste (read this first)
- **Wants:** a clean, bright, big-eyed **Black 2/White 2-like pixel art** look, characters that are **not stiff** (real weight shift, a natural pose and personality in the silhouette), and art that reads like it came from a pro sprite artist, not like "someone drew it on Pictionary".
- **Direction he likes:** see `references/gemini_concepts/`. They're his own Gemini concepts for the player boy and girl. Note the dynamic stance, layered jackets, readable folds and confident pose.
- **Approved:**
  - Juno's **portraits** (`templates/portrait_96/JUNO_*.png`).
  - Juno's **overworld** sprite ("looks cool"; `templates/overworld_charset/JUNO.png`).
- **Rejected:**
  - Juno's **battle sprite**: "choppy, looks weird". This is the first job; see the queue.
  - The in-house player redo: "god awful", "stiff".
  - Dorian ("horrid"; portrait "off").
  - Tamsin's pixel art and portrait. Her *design* is liked: cream silk moth-wing shawl, indigo weaver's dress, needles in her bun, a red thread spool. Keep that concept and redraw it.
- **Never:** anything that looks like an existing official or famous character. One portrait was rejected because Juno "looked like Burgh wearing a wig".

## Exact file formats (the game loads these as they are)
All files are PNG with a transparent background, hard alpha only (each pixel fully opaque or fully clear), and no anti-aliased edges. Pixel art is drawn at **native size** and then scaled up **exactly 2x** (nearest-neighbour), so each art pixel is a 2x2 block in the file.

| Asset | File size | Native art | Layout | File name (goes in) |
|---|---|---|---|---|
| Battle front ("trainer sprite") | **160x160** | 80x80 | one pose, feet 2–3 px above the bottom, centred | `Graphics/Trainers/<TRAINERTYPE>.png` |
| Player back sprite (player only) | **800x160** | 5 frames of 80x80 | 5 frames left to right: idle, wind-up, ball cocked, throw, follow-through | `Graphics/Trainers/PLAYER_A_back.png`, `PLAYER_B_back.png` |
| Overworld walk sheet | **128x192** | 16x24 per frame | 4x4 grid of 32x48 frames. Rows: down, left, right, up. Columns: stand, step, stand, step | `Graphics/Characters/<NAME>.png` |
| Dialogue portrait | **96x96** | 48x48 | head and shoulders, facing right or forward, whole head in frame, eye line around rows 22–27 of the 48 | `Graphics/Portraits/<NAME>_<expression>.png` |

Portrait expressions the scripts call: `neutral, happy, sad, angry, surprised, shocked, smug, deadpan, panic, crying, blush`. Main characters need at least neutral/happy/sad/angry/surprised plus one signature expression. Keep every expression on one base face, changing only the brows, eyes and mouth.

There's a working example of every format in `templates/`. Copy their canvas size and placement exactly.

## Queue, in priority order
1. **Juno: new battle sprite** (`RIVAL_JUNO.png`; `LEADER_JUNO.png` for her Warden look). Match her approved portraits and overworld. Send for approval first; the creator will judge the rest by it.
2. **Player A (boy) and Player B (girl):** a battle front, a 5-frame back sprite, an overworld sheet and portraits for each. The creator's Gemini concepts are the direction.
3. **Kestrel Vane** (rival; `RIVAL_KESTREL`): collar-up black greatcoat a size too big, crimson lining, side-swept navy fringe, Honedge. Proud, guarded, grieving.
4. **Dorian Pell** (Gym 1 Warden; `LEADER_DORIAN`): a 56-year-old former matinee idol. Plum velvet coat, swept-back silver mane, a silver-topped cane he doesn't need, a top hat, a red rose. Theatrical, vain, generous.
5. **Tamsin Loom** (Gym 2 Warden; `LEADER_TAMSIN`): keep the liked design (see above).
6. **Professor Imelda Larch** (mentor; `LARCH`): grey braid, glasses, mustard oilskin field coat, fisherman's knit. Gruff and deadpan-funny.
7. **The rest of the story cast,** a few at a time: `cast_list.md` has every character, their trainer-type file name and their story description (from `story/03_CAST.md`).

## What's in this pack
- `README.md`: this file.
- `templates/`: working examples of every file format (Juno's approved portraits and overworld, the current battle and back sprites for size reference only).
- `references/gemini_concepts/`: the creator's two player concepts.
- `references/cast_overview.png`: where every character stands now. Most of this art is rejected; use it for size and context, not style.
- `story/03_CAST.md`: who everyone is.
- `cast_list.md`: the trainer-type file names for the named characters.
- `STYLE_GUIDE.md`: earlier in-house notes. Its file-format rules are correct; its art results were rejected, so treat its taste notes as optional.

## Delivering
Return PNGs with the exact names and sizes above, in a `Graphics/` folder tree (`Trainers/`, `Characters/`, `Portraits/`). Installing is then a straight copy.
