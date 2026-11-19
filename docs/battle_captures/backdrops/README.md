# Field backdrops: real-engine stills

One still per field and stage (49: 33 fields + 16 extra stages; Cave 2 and Colosseum 2 now have their own art), taken in the real engine (mkxp-z 2.4.2 + Essentials v21.1 + Elite Battle: DX +
the Prismfall plugins): a wild battle started with `setBattleRule("field", ...)`, held on the first command phase
for 150 frames so the animated layers and particles are running, then `Graphics.screenshot`. Daytime forced.
`contact_sheet.png` shows them all at half size; `<field>[_s<stage>].png` are the full frames.

Rebuild:
```bash
python3 -I art/battlebacks/build_backdrops.py            # art -> graphics/EBDX/Battlebacks + 006_Bridge_Art.rb
bash tools/harness/visual/backdrops/run_backdrop_stills.sh   # BD_FIELDS=VOLCANIC,NEW_MOON:3  BD_VECTORS=1  BD_TIME=night
python3 -I tools/harness/visual/backdrops/make_contact_sheet.py <shots> docs/battle_captures/backdrops/contact_sheet.png --cols 6
```
Live transitions (`transition_*.gif`, half speed, with `_keys.png` strips): Volcanic -> Cinderglass and
Meadow -> Wildfire -> Embers, driven by the field plugin's own `Battle#change_field` / `#set_field_stage`
(`BD_TRANSITIONS="VOLCANIC>ASHEN_WASTE;MEADOW>WILDFIRE>WILDFIRE:2"`), not by moves.

Move-triggered transitions (`move_*.gif`, half speed): real battles where the AI player keeps using one move until
the field's own rule fires. Surf x2 quenches Volcanic into Cinderglass; Flamethrower sets Meadow ablaze into Wildfire
(`BD_MOVES="VOLCANIC:VAPOREON:SURF;MEADOW:ARCANINE:FLAMETHROWER"`). Doubles: `double_prism_arena.png`,
`double_silkwood.png` (`BD_DOUBLE=1`). Night: `*_night.png` (`BD_TIME=night`).

Not verified: Windows / real GPU, double battles, night tint on outdoor rooms; other transition pairs.
