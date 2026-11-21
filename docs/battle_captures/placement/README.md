# Battler placement: feet on the base

Real engine (mkxp-z 2.4.2 + Essentials v21.1 + EBDX + Prismfall plugins), wild battles held on the first
command phase. `before_after_sheet.png`: 16 rooms, each at the battle camera (foe side, 1:1) and the send-out
pull-back (1/2), before and after. Cyan = the base painted in the room (through that frame's camera), red + =
where EBDX stands the battler, yellow = the sprite's lowest opaque row (its feet). Species: Joltik, Bidoof
(small), Tauros, Snorlax, Wailord (large), Gyarados (tall), Gastly, Bronzong (floating), Torkoal (wide), Lucario.
`meadow_battle_start.gif` and `frozen_lake_battle_start.gif` (`_keys.png`: 8 numbered key frames with the bases
marked): the first ~7 s of a battle, every 2nd engine frame, half speed, captioned. `ally_before_after.png`: the
ally side in 6 rooms at the send-out pull-back and the battle camera, original vs v1 (item 5);
`ally_v2_before_after.png`: v1 vs v2 (smaller player bases; MEADOW and FROZEN_LAKE tuned on their own).
`doubles_before_after.png`: double battles in 6 rooms (item 6).

## What was wrong

1. **Species metrics (most rooms).** EBDX hangs each sprite from the room anchor (foe room 234,152, player
   116,252; every Prismfall platform is centred there) by its bitmap bottom, shifted by the base project's
   `PBS/EBDX/pokemon.txt` BattlerEnemyY / BattlerPlayerY / BattlerAltitude. Those numbers don't fit the
   bundled sprites: for 90% of the 1020 front sprites the feet land 2 px above to 26 px below the base centre
   (median 14 px below: Tauros +22, Gyarados +24..38, Galvantula +32), back sprites 20 px above to 8 px below, and
   "floating" species at random heights (Bronzong 9 px *below* the centre, Gastly on it, Golbat 18 px above).
   So Pokemon stood on the front rim or in front of their platform.
2. **MEADOW (room).** The painted worn patch came with the Magiscarf panel and sat 34 px left of and 18 px above
   the foe anchor (Tauros stood on the grass beside it); its mirror image showed in the right margin; there
   was no ground at all under the player.
3. **Props on player bases (room).** WATER_SURFACE: a piling standing in the player's pool. WASTELAND: a barrel
   lying on the player's platform. BEACH: a rock and rock pool over the platform's edge. MINDSCAPE stage 2: a
   nightmare hand growing out of the player's platform.
4. **Camera (checked, no fault).** Battlers are room sprites: through the whole battle start (intro sweep,
   send-out pull-back, return to the battle camera) both stay within 1 px of the room anchor. Sprites scale by
   `zoom^0.75` and the room by `zoom^0.6`, so a battler is up to ~10% larger or smaller relative to its base in
   the close-ups; with the feet on the anchor that changes size only, never position.
5. **Ally side (all rooms).** Every player base was the foe base drawn 2x (4x the area). Rejuvenation, also EBDX,
   draws its player base 1.77x as wide as its enemy base, but only the far half of it ever shows (a 64 px strip at
   the screen bottom): ~1.6x the enemy base's area on screen. EBDX's send-out pull-back shows ours whole, so it
   read as a huge disc taking half the screen with the ally standing on its back half, lunging out of the scene.
   And the player point (116,252) is 33 px below the screen bottom at the battle camera, so a small ally
   (Joltik, Bidoof, the starters) showed only 69-79% of itself.

Every other room's foe and player platform is centred on the anchors (checked on all 53 room images).

6. **Double battles (all rooms).** Rooms paint one base per side, sized for one battler. EBDX's double points
   (foe room 198,152 / 256,164, player 92,240 / 192,262) put the near foe's feet past its base's front rim and the
   right-hand ally off its base; two big battlers overhang a singles base anyway.

## What changed

- `plugins/Prismfall EBDX Bridge/007_Bridge_Placement.rb` (the project's battler metric source now): when EBDX
  loads a battler bitmap, the lowest opaque row of each animation frame is measured (cached per file) and the
  median is put on the base (`FOOT_LINE`: foe +16 bitmap px = 16 screen px in front of the centre at the battle
  camera, where the foe base is 25 px deep each way; player +2 = 4 screen px in front of its centre). Floating species (EBDX altitude > 0, or
  Levitate for species EBDX has no metrics for; `FLOATING` overrides 12 EBDX "hoppers" such as Skitty and
  Politoed to grounded) hover a constant `HOVER` = 20 px above that line; EBDX's ground shadow stays on the base.
  Measured after the change (16 rooms, every camera): grounded foes' feet typically 64% of the way from the base
  centre to its front edge (9-88% with the animation's bob), never on or past the rim; player feet typically 10% of
  the way to its base's front edge (30% behind to 40% in front with the animation). Only
  the vertical origin changes; send-out / recall / Substitute keep it; floaters don't shake the screen landing.
- Player point: in Prismfall rooms the Bridge raises EBDX's single-battle player point 8 room px (116,252 ->
  116,244, `PLAYER_RAISE`): 18 px at the battle camera, so 84-94% of a small ally shows; EBDX's stock rooms and
  doubles keep EBDX's points.
- Player bases: `bblib.PLAYER_SCALE` = 1.3 (v1 1.5, originally 2): every builder's player base (platforms,
  stumps, ring stones, silk, scaled vanilla bases, MEADOW's patch) is the foe base's size x 1.3 (1.7x the area:
  Rejuvenation's on-screen ratio, ~1.6x), centred on the raised point `bblib.PLAYER` (261,549 HD). Per-room
  exceptions live in `bblib.ROOM_PLAYER` (field -> extra raise in room px, scale): MEADOW 1.2x (the soft worn
  patch with its pale rim reads bigger than a platform), FROZEN_LAKE 1.15x and 8 room px higher (its ripple ring
  read big, at the screen's edge). The build writes a room's extra raise into its Bridge profile
  (`:player_raise`), and `007_Bridge_Placement.rb` stands the ally there too, so its feet stay just in front of
  the base's centre. Rim, texture and colours unchanged; ring stones a little smaller and fewer. Only the
  player-base band (HD y 495-640) of the rooms changed; layers that sit there followed (a few re-cropped).
- `art/battlebacks/bases.py` + `fields_h.meadow`: MEADOW's worn patch moved onto the foe point (its own pixels,
  whole art pixels), the spot refilled from the same rows, its mirror cleared, the same patch 1.2x under the
  player, no wildflowers on the worn cores; the two tall-grass clumps that stood there frame it instead.
- `fields_b` (WATER_SURFACE piling, BEACH rock), `fields_f` (WASTELAND barrel), `fields_d` (MINDSCAPE stage-2
  hands): moved off the player bases. Only the base areas of these rooms changed.
- Doubles: `art/battlebacks/doubles.py` widens each room's own bases into stadiums for two (its exact pixels, found
  by rebuilding the room with that side's base off the canvas; left half out left, right half out right, the
  centre slab repeated between, so rims, rings, stones and silk carry on): `elements/dbl_<room>_foe.png` /
  `_ally.png`, 53 rooms. `007_Bridge_Placement.rb` lays them over the room (z 1, after its sky-less cut-out) when a
  side has two battlers and stands them on them: foes at room 205,151 / 263,153 (centred on the foe base, 58 px
  apart), allies at 91,243 / 175,246 (84 px apart; FROZEN_LAKE's extra raise applies); with two opposing
  trainers, their intro sprites stand there too. Singles and triples are unchanged (triples keep EBDX's points).
  Re-run `python3 -I art/battlebacks/doubles.py` after rebuilding rooms.

Rebuild: `RUN=<capture copy> PP_CASES="MEADOW:TAUROS/LUCARIO;..." PP_VECTORS=1 bash tools/harness/visual/placement/run_placement.sh`
(`PP_GROUND=0` = EBDX's own metrics, `PP_FOOT=16,-2 PP_RAISE=0 PP_ROOM_RAISE=0` = an earlier tuning,
`PP_GRAPHICS=<dir>` = older art, `PP_PLUGINS=<dir>` = another plugin tree, `PP_INTRO=<case#>[,...]` = frame dumps +
camera logs), then
`python3 -I tools/harness/visual/placement/make_placement_sheet.py sheet|ally|gif ...`.

Not verified: triple battles, 1v2 / 2v1 battles in the engine, Windows / real GPU.
