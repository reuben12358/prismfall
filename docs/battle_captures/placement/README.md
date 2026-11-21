# Battler placement: feet on the base

Real engine (mkxp-z 2.4.2 + Essentials v21.1 + EBDX + Prismfall plugins), wild battles held on the first
command phase. `before_after_sheet.png`: 16 rooms, each at the battle camera (foe side, 1:1) and the send-out
pull-back (1/2), before and after. Cyan = the base painted in the room (through that frame's camera), red + =
where EBDX stands the battler, yellow = the sprite's lowest opaque row (its feet). Species: Joltik, Bidoof
(small), Tauros, Snorlax, Wailord (large), Gyarados (tall), Gastly, Bronzong (floating), Torkoal (wide), Lucario.
`meadow_battle_start.gif` (`_keys.png` with the bases marked): the first ~7.5 s of a MEADOW battle after the fix,
every 2nd engine frame, half speed.

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

Every other room's foe and player platform is centred on the anchors (checked on all 53 room images).

## What changed

- `plugins/Prismfall EBDX Bridge/007_Bridge_Placement.rb` (the project's battler metric source now): when EBDX
  loads a battler bitmap, the lowest opaque row of each animation frame is measured (cached per file) and the
  median is put on the base (`FOOT_LINE`: foe +16 bitmap px = 16 screen px in front of the centre at the battle
  camera, where the foe base is 25 px deep each way; player -2 = on the centre). Floating species (EBDX altitude > 0, or
  Levitate for species EBDX has no metrics for; `FLOATING` overrides 12 EBDX "hoppers" such as Skitty and
  Politoed to grounded) hover a constant `HOVER` = 20 px above that line; EBDX's ground shadow stays on the base.
  Measured after the change (16 rooms, every camera): grounded foes' feet typically 64% of the way from the base
  centre to its front edge (9-88% with the animation's bob), never on or past the rim; player feet typically on
  the centre (38% behind to 16% in front). Only
  the vertical origin changes; send-out / recall / Substitute keep it; floaters don't shake the screen landing.
- `art/battlebacks/bases.py` + `fields_h.meadow`: MEADOW's worn patch moved onto the foe point (its own pixels,
  whole art pixels), the spot refilled from the same rows, its mirror cleared, the same patch at 2x under the
  player, no wildflowers on the worn cores; the two tall-grass clumps that stood there frame it instead.
- `fields_b` (WATER_SURFACE piling, BEACH rock), `fields_f` (WASTELAND barrel), `fields_d` (MINDSCAPE stage-2
  hands): moved off the player bases. Only the base areas of these rooms changed.

Rebuild: `RUN=<capture copy> PP_CASES="MEADOW:TAUROS/LUCARIO;..." PP_VECTORS=1 bash tools/harness/visual/placement/run_placement.sh`
(`PP_GROUND=0` = EBDX's own metrics, `PP_GRAPHICS=<dir>` = older art, `PP_INTRO=<case#>` = frame dump +
camera log), then `python3 -I tools/harness/visual/placement/make_placement_sheet.py sheet|gif ...`.

Not verified: double/triple battles, Windows / real GPU.
