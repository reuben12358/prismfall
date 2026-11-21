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

## NEW (2026-11-21): trainer battle start, B2W2 Elite Four style (TOP PRIORITY after the current cast packs)
The creator chose **Pokemon Black 2/White 2's Elite Four VS sequence (Shauntal)** as "the perfect scenario". The engine already replays it beat for beat; only the art is placeholder.
- Captures: `docs/battle_captures/intro/juno_b2w2_intro.gif`, `dorian_b2w2_intro.gif`
- Side-by-side with the reference: `docs/battle_captures/intro/b2w2_vs_comparison.png`
- Code: `plugins/Prismfall EBDX Bridge/010_Bridge_VersusIntro.rb`
- Generated placeholders: `tools/vs/make_vs_assets.py`

Every file is PNG, hard alpha, drawn native and doubled 2x (2x2 blocks), unless a file below says otherwise.

**A. VS busts (most needed).** `Graphics/EBDX/VS/<ID>.png`, one per main cast member and both players. `<ID>` is the portrait ID (`JUNO`, `KESTREL`, `DORIAN`, `TAMSIN`, `LARCH`, `PLAYER_A`, `PLAYER_B`, then the other Wardens and rivals as they're drawn).
- **256x160**, 128x80 native. The band shows the bottom 136 px; the top 24 px may be cut, like Shauntal's hair in the reference.
- Big chest-up bust with a hand or prop: Rosa holds a Poké Ball, Shauntal her pen. Dorian: cane or hat. Tamsin: needle and spool. Juno: bouquet. Kestrel: Honedge hilt.
- **Opponents face left** (they sit top-right). **Players face right** (bottom-left).
- Transparent background. Expressive and in motion, not a stiff portrait.

**B. One-shot intro pose.** `Graphics/Trainers/<TRAINERTYPE>.png`, a horizontal strip of 160x160 frames.
- It plays **once**, over 1.6 s, while "You are challenged by ...!" shows, then **holds the last frame** for the rest of the battle.
- **Not a loop.** Shauntal's reference: she sits reading, stands, turns, then flings her arms open with book and pen.
- Frame 0 = a calm "before" pose (reading, arms folded, back turned). Middle frames = one big readable action. Last frame = the hero pose.
- **16–24 frames**, with whole-body movement visible at 1x.
- The current Juno, Dorian and Tamsin strips are subtle loops, so each needs this pass.

**C. VS lightning bolts (nice to have).** `Graphics/EBDX/VS/bolt0.png`, `bolt1.png`, `bolt2.png`: three crackle variants that cycle.
- **512x88**, transparent.
- Thick orange-gold electric bolts with a white-hot core and a soft orange glow, irregular and organic like the reference, not a regular diamond chain.
- They tile edge-to-edge horizontally.

**D. Optional polish.** The game generates these per colour theme; hand-drawn versions win if supplied:
- `tunnel_<theme>.png` (640x640, a radial warp of streaks around a dark centre; it is rotated in-engine)
- `bandfoe_<theme>.png` (512x136; dark on the left, bright on the right)
- `bandplayer_<theme>.png` (512x136; bright on the left, dark on the right)
- `emblem.png` (300x300, a faint Poké Ball outline)
- `spark.png`

Themes: `violet, rose, blue, teal, green, gold, red, grey`.

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
