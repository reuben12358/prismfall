# How Rejuvenation, Reborn and Desolation build their animated scenes

Research for `Prismfall Cutscenes` (2026-11-17). All game data was decoded read-only with `mapgen/rmarshal.py`
(`python3 -I`). No Ruby from these games was executed. The helper scripts are in `/tmp/research/` (`events.py`,
`anims.py`, `anim_detail.py`, `routes.py`, `context.py`, `dump_scripts.py`).

## Sources

| Source | What it is | Used for |
|---|---|---|
| `/home/claude/ref/games/rejuvenation` | Rejuvenation 14 (Data, Graphics, plain-text Scripts) | Main source |
| `/home/claude/ref/games/reborn` | Reborn E19 (Data, Graphics, Scripts) | Main source |
| `/home/claude/ref/games/desolation` | Desolation (Data, Graphics, Scripts) | Cross-check |
| `ref/art/wll` (Where Love Lies Overhaul, `pbflo/Where-Love-Lies-Overhaul`) | A Rejuvenation-engine fan game; decoded `Scripts.rxdata` to `ref/src/wll_scripts/` | First look, before the games arrived |
| `ref/src/simonswu23_Scripts` (GitHub) | Rejuvenation 13.5.6 Scripts folder, inside a difficulty mod | Engine diff against v14 |
| `ref/src/fuyukai_reborn-rebalance` (GitHub) | Reborn rebalance tool; ships 10 real Reborn map files | Early Reborn samples |
| `ref/src/birblett_RemiX`, `ref/src/fclorenzo_pkreborn-access` (GitHub) | Gameplay and accessibility mods | Nothing cutscene-related |

Only these public GitHub repos turned up. I found no official script dump of any of the three games on GitHub. (One repo,
`rejuvena/rejuvena`, turned out to be a Terraria mod and was deleted.)

## 1. The headline: there is no cutscene engine

None of the three games has a cutscene class. Every animated scene, including Rejuvenation's set pieces, is an
**RPG Maker XP event on the real map**. It is built from move routes, Show Animation (database animations), screen
tone, flash and shake, and full-screen pictures. The script side only adds conveniences: Rejuvenation 14's camera
module, its frame-sheet extension and accessibility switches.

Event command counts across every map and common event:

| Command | Rejuvenation 14 | Reborn E19 | Desolation |
|---|---:|---:|---:|
| Move Route (acting, walking, **frame flipping**) | 99,856 | 32,193 | 12,341 |
| Wait | 69,240 | 19,373 | 16,241 |
| Change Screen Tone | 31,130 | 18,827 | 5,716 |
| Show Animation (database animation on an event) | 19,533 | 10,494 | 1,258 |
| Show / Move / Rotate Picture | 4,147 / 5,283 / 677 | 272 / 231 / 0 | 700 / 88 / 0 |
| Screen Flash / Shake | 2,871 / 2,461 | 1,546 / 392 | 391 / 271 |
| Scroll Map | 3,243 | 797 | 529 |

## 2. Techniques, with evidence

### 2.1 The map is the stage and the hidden player is the camera
Scenes run on the actual map with the real tileset art. The player is made invisible (`Transparent`) and moved or
teleported (`Transfer` / `Set Event Location`), which acts as a camera move or cut. "Scroll Map" pans; Rejuvenation
also uses the Wachunga *Map Autoscroll* script (`autoscroll(x, y, speed)`).

Rejuvenation 14 adds `Scripts/Camera/` with these calls:
- `pbCameraToEvent(id, speed)`: follow an event, smoothed.
- `pbCameraScrollTo`, `pbCameraOffset`, `waitForCamera`.
- `pbCameraShake(power)`.
- `pbZoomMap(goal, speed)`: zooms by grabbing `Graphics.snap_to_bitmap` every frame and scaling that one sprite, so
  zoom never breaks the tile layers.

Smoothing uses a lerp plus `ease_in_out`.

### 2.2 Acting is move routes
Characters "act" with turn commands (codes 16–19), jumps, speed changes and waits. A typical Reborn reaction beat is
four or five head turns in a row on two characters. Emotion lives in **per-scene pose sheets in charset format**.
For example, `MC_Cella3_Crying.png` (192×208, 4×4 cells) holds crying frames in place of walk frames.

### 2.3 Big moments are hand-drawn flipbooks played by move routes
A move route steps through cells with "Change Graphic (sheet, direction row, pattern column)" and "Wait n".

**Reborn's Zygarde set piece** (Map153, event 133, page 3):
- The flipbook is `pkmn_zygarde5.png`: 552×360, 4×4 cells of 138×90. The legendary is drawn at **overworld scale and
  3/4 overworld perspective**, with 16 acting frames of the wings spreading.
- It is stepped with "w1" (1/20 s per frame).
- It is followed by Show Animation 26 on an invisible "focus arrow" event, `Shake power 2, speed 2, 40`, and two
  sound effects (SEs).

**Rejuvenation** does the same with `DimensionPortal_5`, `DimensionalAelita_1/_2`, `Arc_Renegade_Anim` and
`FriendBlast`. Each frame is held for 2–6 ticks with SEs cued inline (`PRSFX- Dark Void`, `Freeze Shock1`).

**Rejuvenation 14 generalises this** in `Scripts/AdvancedAnimations.rb`:
- Any grid size, plus a `frameData` list of per-frame holds.
- The data lives in `Rejuv/Definitions/animsheettext.rb` or a PNG `tEXt` chunk.
- Example holds: `pkmn_quilava_3` is `[30, 8, 4, 8, 4]`, a long anticipation hold then quick action frames;
  `pkmn_quilava_4` is `[3, 6, 2, 2, 2, ...]`.

**Legendaries are never battle sprites in these scenes.** They are overworld-scale sheets drawn in the map's
perspective and palette.

### 2.4 VFX are RMXP database animations, instanced
Reborn plays 36 distinct database animations on maps. The most instructive is **"Dragonball Z"** (Animations #26,
graphic `PRAS- Core Enforcer`, 65 frames):
- **Five hand-drawn cells** (192 px cells, 5 per row) of a small green eruption growing from a spark to a burst.
- Each "impact" plays cells 0→4 at one point. Then cell 4 pops: zoom 100→120→140 (finale 150→300) while opacity
  steps 255→170→85.
- About 25 impacts are **staggered along a zig-zag path**, ending in a symmetric chain spreading outwards.
- Every cell uses **additive blend** (`b1`).
- Screen-scope flashes **ramp up**: alpha 17, 51, 136, 221, then 255 held for 20 frames.

Other animations:
- **"Beam 1/2"** (`VR-Beam`): one diagonal line cell slid along its own axis over three frames at opacity 160
  (additive), then faded 160→100→50.
- **"Black Hole"**: subtractive blend (`b2`), zoom 100→800 with opacity rising then falling.

The sheets themselves are **sparse and thin**. The beam is a 1–3 px line with a pale outline. The eruption is a few
dozen pixels, about four colours, on transparency. The drama comes from timing, instancing, additive blending and the
screen flash, not from big filled shapes.

**Rejuvenation's beam** (`Graphics/Characters/anim_beam.png`, 384×256) is a charset of **tileable beam segments**:
an almost-white core, faint pastel bands and rounded end caps. Several events are lined up along the path, each
cycling its frames. The scene is darkened with a screen tone first, so the beam reads by **brightness contrast**.

### 2.5 Screen effects
- **Cuts:** tone to black over 10–20 units, or `Flash (0,0,0,255) 2` as a hard black cut.
- **Mood:** tones with grey, e.g. Reborn `(0,-34,-34,187)`.
- **Heartbeat:** Reborn pulses the tone to `(-68,-102,-102,187)` for 3 units and back, as an impact beat.
- **Shakes are small** (power 2–5).
- **Weather and fog overlays** for light: `sunbeamwhite` fog, set via Change Map Settings.

### 2.6 Pictures are illustrations, not animation
- **Full-screen CGs and storyboards:** 512×384 (`CG_*.png`, `Storyboard_*`), or 1024×768 for Rejuvenation 14 CGs.
- **Boss intros:** a character poster plus `BlurOverlay` at opacity 130.
- **Letterbox:** a picture, `WidescreenEffect_1`, at opacity 155–233.
- **Hand-keyed stepped fades:** Rejuvenation and the WLL fan game use 5–6 opacity steps, one per tick. Desolation
  ramps opacity by 10 per tick.
- Rejuvenation 14 also ships a few `.ogv` videos (a CG scene, the credits).

### 2.7 Timing conventions
- Engines run at **40 FPS** and double every event duration, so 1 event unit = 2 frames = **1/20 s**.
- Flipbook frames are held 1–2 units (0.05–0.1 s), with longer holds on anticipation.
- CGs are held about 20 units (1 s). Tone cuts take 10–20 units.
- Their "turbo" mode raises the frame rate to 200, so cutscenes speed up with it (frame-based timing).

### 2.8 Accessibility
- Rejuvenation and Reborn gate every screen flash and shake behind `$Settings.photosensitive`.
- Rejuvenation 14 also has `cameraAccessibility`.
- Rejuvenation even shakes the OS window (`moveWindow`, Windows only), behind the same switch.

## 3. What this means for Prismfall Cutscenes

Our plugin is a full-screen, code-drawn, time-based scene player. They stage on the live map with hand-drawn sheets
and frame-based events. The war climax "looks weird" mostly for reasons this research explains:

1. **Scale and perspective mismatch.** We paste front-facing battle sprites at 2× onto a side-view stage. They
   always draw legendaries as overworld-scale 3/4-view acting sheets.
2. **Too much drawn by code, too thick.** Their effects are small, sparse, few-colour, additive, instanced in time and
   space, and sold by a darkened scene plus a flash ramp. Our thick outlined beams and dense procedural backdrops pull
   the other way.
3. **No real map.** Our procedural ice will never match tileset art. Their set pieces happen on the map the player
   just walked on.

### Done now (DSL compatible, all existing scenes still pass)
| Change | Borrowed from |
|---|---|
| `actor ..., sheet:, grid:, frame:`; `pose`; `flipbook frames:, hold:/holds:, loops:, se: {i => name}, end_frame:` | Charset flipbooks; Rejuvenation 14 `frameData` |
| `play_sheet path, at:, frames:, hold:, blend: :add` (one-shot, removes itself; chain with `at()`) | Reborn's instanced database-animation cells |
| `actor ..., blend: :add / :sub` | Additive cells, subtractive Black Hole |
| `anim id, at:` plays any database animation from `Animations.rxdata` | Show Animation |
| `still "Graphics/Pictures/...", dim:, fade:, steps:` | CG and storyboard pictures, poster plus blur overlay |
| `fade_in/fade_out/fade ... steps: 5` and `ease: :step3..:step8` | Hand-keyed stepped fades |
| `pulse tone:, duration:, times:` | Reborn's tone heartbeat |
| `define(:ID, on_map: true)`: no black curtain, map keeps updating; `actor ..., event: id, offset:` | Map-staged scenes |
| `follow :id, smooth:` (frame-rate independent; explicit camera moves end it) | `pbCameraToEvent` smoothing |
| `Prismfall::Cutscene.photosensitive` (also read from `$PokemonSystem.photosensitive`), plus a Debug toggle: flashes capped at ¼ strength, no impact frames, shake at 20% | `$Settings.photosensitive` |
| `TICK = 0.05` for porting event timings | 40 FPS × 2 convention |
| `:WAR_CLIMAX` uses `Graphics/Characters/pkmn_<species>_war.png` (4×4) for each legendary when present; rise and charge rows play as flipbooks | Zygarde set piece |

### Recommended next (not done; needs art or a bigger change)
1. **Draw the two legendary acting sheets** (the biggest win).
   - Files: `Graphics/Characters/pkmn_kyogre_war.png` and `pkmn_reshiram_war.png` (or whatever species the story
     team picks).
   - Layout: 4×4 cells, each about 140×100. Overworld scale and 3/4 perspective, dark outline, 24–32 colours.
   - Rows: 0 rise/enter, 1 charge (anticipation), 2 firing loop, 3 recoil/exit.
   - The scene already plays rows 0 and 1 when the files exist; rows 2 and 3 need two more `flipbook` lines.
2. **Stage the war climax on a real "Shattered Ice" map** with `on_map: true`. Soldiers would be map events, the hosts
   would come from tilesets, and the camera would follow events. Our procedural backdrops then become a fallback.
3. **Effect sheets instead of code-drawn bursts** for impacts and the clash point.
   - Hand-drawn 5–8 cell sheets (192 px cells, transparent, 4 colours) played with `play_sheet ... blend: :add` and
     chained along the beam.
   - Keep the code-drawn beam, but make it thinner and brighter. Rely on the anticipation dim and a ramped flash
     (`flash power:` 20, 50, 130, 220, then 255 with `hold:`).
   - Option: add a `beam style: :sheet` that tiles an `anim_beam`-style segment sheet.
4. **Author through events where possible.** Writers already think in event commands. A `\cutscene[...]` comment
   command or a Script call per beat would let them mix map-event acting with our effects.

Not worth copying:
- Frame-based timing (their turbo mode speeds up scenes).
- Moving the OS window.
- Hand-keying fades as dozens of Show Picture commands. `steps:` does the same in one line.
