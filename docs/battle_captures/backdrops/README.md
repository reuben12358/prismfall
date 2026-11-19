# Field backdrops: real-engine stills

One still per field and stage (49: 33 fields + 16 extra stages), taken in the real engine (mkxp-z 2.4.2 + Essentials v21.1 + Elite Battle: DX +
the Prismfall plugins): a wild battle started with `setBattleRule("field", ...)`, held on the first command phase
for 150 frames so the animated layers and particles are running, then `Graphics.screenshot`. Daytime forced.
`contact_sheet.png` shows them all at half size; `<field>[_s<stage>].png` are the full frames.

Rebuild:
```bash
python3 -I art/battlebacks/build_backdrops.py            # art -> graphics/EBDX/Battlebacks + 006_Bridge_Art.rb
bash tools/harness/visual/backdrops/run_backdrop_stills.sh   # BD_FIELDS=VOLCANIC,NEW_MOON:3  BD_VECTORS=1  BD_TIME=night
python3 -I tools/harness/visual/backdrops/make_contact_sheet.py <shots> docs/battle_captures/backdrops/contact_sheet.png --cols 6
```
Not verified: Windows / real GPU, double battles, night tint on outdoor rooms, live transitions between every pair.
