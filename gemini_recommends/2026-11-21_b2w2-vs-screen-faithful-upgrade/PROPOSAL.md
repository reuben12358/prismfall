# Proposal: Making Prismfall's B2W2 VS Intro Match Official Black 2 / White 2 Quality (`010_Bridge_VersusIntro.rb`)

- **Context:** After reviewing `docs/battle_captures/intro/b2w2_vs_comparison.png` alongside the creator's feedback (*"can u see how bad our version is vs pokemon's official version?"*) and studying the actual open-source **Pokémon Black 2 / White 2 decompilation** (`fuddlesworth/pokebw2`, `src/field/encounter/fld3d_ci.c` & `event_encounter_cutin.c`), we identified **both** halves of the gap:
  1. **Art/VFX half (Gemini's lane — actively being replaced right now!):**
     - All 7 dedicated `256x136` dynamic VS busts (`Graphics/EBDX/VS/{PLAYER_A,PLAYER_B,JUNO,KESTREL,LARCH,DORIAN,TAMSIN}.png`) and all 6 true one-shot B2W2 PWT intro poses (`RIVAL_JUNO`, `LEADER_JUNO`, `RIVAL_KESTREL`, `LARCH`, `LEADER_DORIAN`, `LEADER_TAMSIN`) are **already pushed** (`a099494`, `930776c`).
     - All 29 procedural placeholder VFX PNGs (`bolt0..2.png`, `tunnel_*.png`, `bandfoe_*.png`, `bandplayer_*.png`, `emblem.png`, `spark.png`) are actively being replaced with genuine Gemini anime VFX art right now and will be pushed directly into `graphics/EBDX/VS/`.
  2. **Motion / Camera / Compositing half (Claude's Ruby lane — `plugins/Prismfall EBDX Bridge/010_Bridge_VersusIntro.rb`):**
     - Why B2W2 (`fld3d_ci.c`) looks so visceral on DS: Game Freak runs a NitroSystem 3D scene (`Fld3DCi`) with UV-scrolling additive ribbons, Z-axis billboard slams, layered ghost echoes, and a 3D warp cone. In RGSS/mkxp-z 2D Ruby, **6 small surgical upgrades** replicate that exact 3D B2W2 feel cleanly!

---

## Six Surgical Ruby Upgrades for `plugins/Prismfall EBDX Bridge/010_Bridge_VersusIntro.rb`

### 1. Fix `V` and `S` Center Pivot (`ox`/`oy`) + True Giant Slam (Panel 4)
- **Current issue (`lines 155–158, 255–262`):** `@s["V"]` and `@s["S"]` keep `ox = 0, oy = 0`, so scaling by `z = 3.4 -> 1.0` shifts them awkwardly off-center and makes them look small/crooked in Panel 4 compared to B2W2's massive screen-filling `S` & `V` crash.
- **B2W2 fix:**
  - Set centered anchors:
    - `@s["V"].ox = VS_SPLIT / 2; @s["V"].oy = @vs_h / 2`
    - `@s["S"].ox = (@vs_w - VS_SPLIT) / 2; @s["S"].oy = @vs_h / 2`
  - Adjust `@v_home` and `@s_home` by `+ox / +oy`, start `z = 4.6 -> 1.0` with a snappy **ease-in** drop (`e.ease_in` feels like heavy impact instead of floaty ease-out!), plus a **3-frame 4px camera punch/shake** (`@top.ox`, `@bot.ox`, `@over.ox`) right at `t = 2.78..2.92` when `V` and `S` lock!

### 2. High-Speed Horizontal UV-Scroll + Additive Glow on Lightning Bolts (Panels 2–3)
- **Current issue (`lines 230–240`):** `@s["boltT"]` and `@s["boltB"]` stay horizontally frozen after growing in, only flipping 3 frames with ±1px vertical jitter. In B2W2 (`vs_line_a/b`), the lightning tears horizontally across the frame!
- **B2W2 fix:**
  - Set `blend_type = 1` (additive glow) on both bolt sprites so Gemini's new organic orange-gold lightning blazes brightly over the darkened overworld.
  - Once revealed (`t > 1.52`), wrap-scroll a doubled `1024x88` bolt bitmap rapidly horizontally (top right-to-left, bottom left-to-right at `~650 px/s`) while cycling `bolt0 -> bolt1 -> bolt2` at `24 Hz`.

### 3. Living Energy Bands + Enlarged Ghost Bust Echo + Slow Parallax Drift (Panel 5)
- **Look closely at Panel 5 Left (`b2w2_vs_comparison.png`):** Official B2W2's hold screen feels alive because of 3 subtle layers that currently sit completely frozen in `010_Bridge_VersusIntro.rb`:
  1. **Enlarged translucent ghost echo behind the foe (and optionally player):** Duplicate `@s["bustT"]` at `z = 3`, `zoom_x = zoom_y = 1.45`, `opacity = 55`, `blend_type = 1`, offset ~`60px` toward the center, drifting slowly in the opposite direction — reproduces that iconic glowing Shauntal double-image in Panel 5!
  2. **Slow continuous bust parallax drift during hold (`t = 2.80..5.20`):** Instead of freezing dead still for 2.4 seconds, creep `@s["bustT"].x -= (t - 2.8) * 6` and `@s["bustB"].x += (t - 2.8) * 6` (only ~14px total, subtle cinematic drift!).
  3. **Scrolling diagonal sheen / speed-streak overlay on both bands:** Mirror-tile or wrap-scroll `bgT` / `bgB` (or a subtle additive streak layer) across `t = 2.80..5.20` so the bands crackle with energy rather than standing still.
  4. **Crisp slanted/bold name treatment:** Give the foe/player names a bold drop-shadow or dark gradient underline strip (matching B2W2's `Shauntal` / `Rosa` crisp readability against bright bands).

### 4. True 3D-Style Rush Vortex Collapse Instead of Flat Spinning Wheel (Panel 6)
- **Current issue (`lines 268–273, 289–293`):** Spinning a single flat `tunnel` slowly at `26°/s` while expanding a hard black circle looks 2D. In B2W2 (`vs_w.png` on a 3D cone), energy waves rush continuously outward/inward from the dark center!
- **B2W2 fix:**
  - Use **3 layered `tunnel` sprites** (`tunnel0`, `tunnel1`, `tunnel2`) with staggered phase `p_i = ((t * 1.4 + i / 3.0) % 1.0)`:
    - Each layer smoothly scales `zoom = 0.45 + 2.2 * (p_i ** 1.6)` (perspective acceleration toward the viewer!), rotates smoothly (`angle = spin * dir`), and fades in-then-out (`opacity = 255 * Math.sin(p_i * Math::PI)` with `blend_type = 1` on layers 1–2)!
  - During collapse (`t >= HOLD_END`), crank spin speed 3× and accelerate zoom rush into the black core (`hole` with soft-edged radial gradient instead of a hard binary circle!).

### 5. Dramatic Darkened Spotlight Mood During Silhouette Close-Up Reveal (Panel 7)
- **Current issue (`lines 340–351`):** In Panel 7 right of `b2w2_vs_comparison.png`, Dorian's black silhouette stands in bright full daylight over the stage, losing the dramatic reveal punch of Panel 7 left (Shauntal's silhouette emerging out of dark atmospheric lighting!).
- **B2W2 fix:**
  - While `PrismfallVS.hold_pose` is true (during the zoomed-in silhouette camera sweep), dim the battle room viewport tone briefly (`Tone.new(-75, -75, -60, 0)`) and lerp cleanly back to `Tone.new(0, 0, 0, 0)` over the last ~15 frames right as the trainer's silhouette pops into vivid color and fires their one-shot PWT intro pose!

### 6. Update `THEMES` & `VS_IDS` Check
- All 7 dedicated `256x136` VS busts are now installed & pushed (`930776c`) at `Graphics/EBDX/VS/{PLAYER_A,PLAYER_B,JUNO,KESTREL,LARCH,DORIAN,TAMSIN}.png` — note that `BAND_H = 136`, so `s.y = BAND_H - 136 = 0` seats all 7 cleanly flush inside both bands with zero clipping!
- Check if `VS_IDS` needs entries for any trainer whose in-battle display name differs from their bust filename (e.g. `:LARCH => "LARCH"` if her trainer display name is `"Prof. Larch"` -> `"PROFLARCH"` won't match `"LARCH"` unless mapped in `VS_IDS`!). Good catch to add `:LARCH => "LARCH"` (and `:RIVAL_JUNO => "JUNO"`, `:LEADER_JUNO => "JUNO"`, `:RIVAL_KESTREL => "KESTREL"`, `:LEADER_DORIAN => "DORIAN"`, `:LEADER_TAMSIN => "TAMSIN"`) explicitly to `VS_IDS`!

---

## Summary Division of Labor
- **Gemini (Art Owner):** All 7 VS busts (`930776c`) & all 6 PWT one-shot poses (`a099494`, `930776c`) are already pushed; all 29 replacement VS VFX files (`bolt0..2`, `tunnel_*`, `bandfoe_*`, `bandplayer_*`, `emblem`, `spark`) are finishing visual QC right now and will push cleanly right into `graphics/EBDX/VS/`.
- **Claude (Code Owner):** Applying the 6 small Ruby upgrades above to `010_Bridge_VersusIntro.rb` (plus adding `:LARCH => "LARCH"` in `VS_IDS`) will turn the live capture from "2D approximation" into a dead-ringer for official B2W2 Elite Four quality!
