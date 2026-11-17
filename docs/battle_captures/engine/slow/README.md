# Readable real-engine battle captures (slow-paced)

These are the same kind of captures as `../`: the real mkxp-z engine running Elite Battle: DX with the
Prismfall plugins, with the AI playing both sides. This time the battles were **paced for reading inside the
engine**; nothing was slowed down afterwards.

- **Text speed:** Essentials' slowest setting ("Slow", 0.05 s per character).
- **Message holds:** after a message finishes typing, it stays up **2.5 s**. Field and boss messages stay
  **3.5 s**: field intros, boosted-move lines, transition progress and transitions, field end-of-round
  effects, seeds, and boss bar breaks. Brief messages ("X used Y!") are held too. Yes/no prompts are answered
  only after the same hold.
- **Turn pause:** 1 s before each turn.
- **Animations:** move animations run at normal speed.
- **Clock:** game time is locked to 1/60 s per frame, so the recorded frames are true real-time.
- **Recording:** every 2nd frame (30 fps), straight from `Graphics.screenshot`.

Every file opens with a **title card** saying what to watch for. A caption strip under each frame says what
the footage is. The images themselves are untouched.

| Battle | MP4 (whole battle, real time) | GIF (key stretch, real time) |
|---|---|---|
| Volcanic Field → Ashen Waste (Gym 7, Brann) | `volcanic_to_ashen.mp4`, 2:46 | `volcanic_to_ashen.gif`, 6.6 MB: Surf #2 → flash → "The water quenched the magma!" |
| Silkwood → Ashen Waste (Gym 1, Tamsin) | `silkwood_to_ashen.mp4`, 5:21 | `silkwood_to_ashen.gif`, 3.9 MB: 3rd Ember → "The Silkwood burned down to ash!" |
| Zekrom boss, 3 HP bars (Factory → Scrapyard) | `zekrom_boss.mp4`, 3:11 | `zekrom_boss.gif`, 6.6 MB: bar 2 drains and breaks → (time skip) → "The Engine core buckles!" field change |

**MP4s:** H.264 (libx264, `-preset veryfast`, CRF 20), 30 fps, scaled 2× with nearest-neighbour so the pixel
text stays sharp. Each covers the whole battle, from the intro to one full turn after the field transition.

**GIFs:** native size, 128 colours, trimmed to the key stretch to stay under 8 MB. Every typing frame is kept.
While a message is fully shown and the screen is near-static, frames are merged into one, and that frame keeps
the summed duration, so each hold lasts as long as it did in the engine. Animation frames run at 15 fps in the
GIF (30 in the MP4). The Zekrom GIF has two segments joined by a labelled "time skip" card.

**Key frames:** `*_key_fNNNNN.png` (full colour, NNNNN = recorded frame number), chosen automatically by
message text. They show the field intro, on-entry and seed effects, boosted-move lines, transition progress,
the Bridge's flash, the transition message, and the new field's first effect. For Zekrom they also show the
bar pips and the bar breaks.

## Rebuild

```bash
cd tools/harness/visual
RUN=/path/to/own/copy PACKAGE=0 bash run_engine_capture.sh assemble
ISOLATE=1 DEMO_SLOW=1 RUN=/path/to/own/copy bash run_engine_capture.sh run volcanic,silkwood,zekrom
bash build_slow.sh /path/to/own/copy/captures_keep        # specs: slow_specs/*.json
```

- `ISOLATE=1` runs the engine on its own display under renamed process names. The first recording here was
  cut short when the virtual display under it was killed from outside the run.
- `PACKAGE=0` reuses the existing `dist/` instead of rebuilding it.
- Battles aren't seeded, so every run differs. The GIF markers and key frames are found by message text, so
  the specs usually still work.

## Not verified

Same as `../README.md`: no Windows, no real GPU, no audio, and stock EBDX rooms only (tinted by the Bridge).
