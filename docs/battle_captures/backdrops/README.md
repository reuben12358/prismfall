# Field backdrops: real-engine stills

One still per field and stage (51: 35 fields + 16 extra stages, including the Ch19 war fields Flooded Dunes and Glass Dunes), taken in the real engine (mkxp-z 2.4.2 + Essentials v21.1 + Elite Battle: DX +
the Prismfall plugins): a wild battle started with `setBattleRule("field", ...)`, held on the first command phase
for 150 frames so the animated layers and particles are running, then `Graphics.screenshot`. Daytime forced.
`contact_sheet.png` shows them all at half size; `<field>[_s<stage>].png` are the full frames.

Rebuild:
```bash
python3 -I art/battlebacks/build_backdrops.py            # art -> graphics/EBDX/Battlebacks + 006_Bridge_Art.rb
bash tools/harness/visual/backdrops/run_backdrop_stills.sh   # BD_FIELDS=VOLCANIC,NEW_MOON:3  BD_VECTORS=1  BD_TIME=night
python3 -I tools/harness/visual/backdrops/make_contact_sheet.py <shots> docs/battle_captures/backdrops/contact_sheet.png --cols 6
python3 -I tools/harness/visual/backdrops/make_contact_sheet.py <shots> docs/battle_captures/backdrops/contact_sheet_pullback.png --cols 6 --suffix _wide   # needs BD_VECTORS=1
```
Live transitions (`transition_*.gif`, half speed, with `_keys.png` strips): Volcanic -> Cinderglass and
Meadow -> Wildfire -> Embers, driven by the field plugin's own `Battle#change_field` / `#set_field_stage`
(`BD_TRANSITIONS="VOLCANIC>ASHEN_WASTE;MEADOW>WILDFIRE>WILDFIRE:2"`), not by moves.

Move-triggered transitions (`move_*.gif`, half speed): real battles where the AI player keeps using one move until
the field's own rule fires. Surf x2 quenches Volcanic into Cinderglass; Flamethrower sets Meadow ablaze into Wildfire
(`BD_MOVES="VOLCANIC:VAPOREON:SURF;MEADOW:ARCANINE:FLAMETHROWER"`). The war fields (one place in three states): `transition_desert_flood_glass.gif` (chain via `change_field`),
`move_originpulse_desert_to_flooded.gif` (Kyogre: Drizzle blooms the Desert, Origin Pulse floods it) and
`move_blueflare_flooded_to_glass.gif` (Reshiram: Blue Flare glasses the flood), all half speed with `_keys.png` strips.
Sky fix (Nov 20): clouds were a flat white strip drawn over the whole MEADOW room (in front of the oak and the
windmill) and the room's top margin was a mirror of the panel (upside-down trunks and rocks: the dark band seen
when the camera pulls back). Now the sky strip sits between the room and a sky-less cut-out of it, drifts slowly
and follows the camera by a fraction (Bridge `:parallax`); the top is sky plus the oak's crown. Same split for
STORMFRONT's scud (it crossed the mast and shrouds); DESERT, DESERT_S2, FLOODED_DUNES and GLASS_DUNES lost their
upside-down mesa (sky continues above the horizon). `meadow_clouds_before_after.png`: MAIN / ENEMY (intro start) /
SENDOUT framings, before, after, and after at night on an outdoor map. `meadow_battle_start.gif` (`_keys.png`): the
first 6.4 s of a MEADOW battle, every 2nd engine frame, half speed (`BD_INTRO=1` dumps every frame;
`BD_CAMLOG=1` logs the room camera and the parallax layer per frame; `BD_OUTDOOR=1` makes the map outdoor so
`*_night` rooms and EBDX's day/night tint apply).
Margins (Nov 20, round 5): every vanilla panel's surroundings were mirror images of it, so EBDX's send-out pull-back
and opening close-up showed upside-down crags, canopies, arcades and railings above the panels and "butterfly"
rocks at their sides. Those regions are now painted from each panel's own pixels at its own art-pixel size
(`art/battlebacks/margins.py`: patch quilting steered by a material layout, never flipped; per-panel plans in
`fields_i.py`, installed over every builder by `build_backdrops.py`), only above the panel and beside its upper
rows. MOUNTAIN (falls between two crag walls; a crag cut-out now hides the foam streaks that crossed both crags),
CAVE (+cracked), SNOWY_MOUNTAIN, CRYSTAL_CAVERN, DARK_CRYSTAL, DRAGONS_DEN (+Wyrmfire), VOLCANIC, ASHEN_WASTE (the
wall goes on; crystals, lava and tunnel mouths are never copied), FAIRY_TALE, SILKWOOD, WILDFIRE (+Embers),
WASTELAND (canopy), BEACH, STORMFRONT (clouds), UNDERWATER, FROZEN_LAKE, WATER_SURFACE (top row deepens to the
zenith), COLOSSEUM (+Frenzy), FLOWER_GARDEN 1-5, NEON_GRID (+Blackout) (structures repeat upright), RAINBOW (bands
carried round the arc), HOLLOW_CATHEDRAL (+Consecrated) (window, pillars, banner rod, crown), PRISM_ARENA (night
sky; the barrier continued in perspective), NEW_MOON (all stages: city lights instead of the hanging railing).
`contact_sheet_pullback.png`: every room at the SENDOUT camera (`BD_VECTORS=1`, the `_wide` shots;
`make_contact_sheet.py --suffix _wide`). Both contact sheets were shot with the battlers' feet on their bases
(`007_Bridge_Placement.rb`).
Doubles: `double_prism_arena.png`,
`double_silkwood.png` (`BD_DOUBLE=1`). Night: `*_night.png` (`BD_TIME=night`).

Not verified: Windows / real GPU, double battles, night tint on outdoor rooms other than MEADOW; other transition pairs.
