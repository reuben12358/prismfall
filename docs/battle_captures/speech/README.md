# Trainer speech when a trainer's Z-move fires

Real engine (mkxp-z 2.4.2 + Essentials v21.1 + EBDX + Prismfall plugins). Hook: `plugins/Prismfall Z-Power/005_ZPower_TrainerSpeech.rb`
(data: `PrismfallSpeech::LINES`; events `:prismfall_zmove_unleashed` and `:prismfall_mega_evolved`).

- `celestine_zmove_speech.gif`: Celestine's Mimikyu (Mimikium Z) on Fairy Tale, from the Z-move choice to ~3 s after
  her line, every 3rd engine frame, real time, captioned.
- `zmove_speech_keys.png`: top row, Celestine as she ships (no trainer sprite yet, so the line is a named battle
  message); bottom row, EBDX's slide-in path with a capture-only stand-in (a stock Beauty given a demo line by the
  capture plugin): trainers with a front sprite slide in and speak in EBDX's trainer dialogue.

Rebuild: `RUN=<capture copy> SP_CASES="celestine,ebdx_demo" bash tools/harness/visual/speech/run_speech.sh`, then
`python3 -I tools/harness/visual/speech/make_speech_sheet.py <RUN>/speech docs/battle_captures/speech`. The capture copy
needs the kit's current PBS (Z-Power moves and items) compiled. Headless: `tools/harness/run_mega.rb` section 9.
