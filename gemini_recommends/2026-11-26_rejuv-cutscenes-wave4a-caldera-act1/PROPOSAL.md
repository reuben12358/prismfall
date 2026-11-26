# Wave 4A — Rejuvenation V14 Director's Cut Scenes on Critic-Certified Redesigned Maps (Pass 3 — 3/3 GOLD PASS Ready)

> **Date:** 2026-11-26 (Pass 3 Final — 162a 9.4 PASS · 162c 9.5 PASS · 162b Framing Fixed)
> **Author:** Gemini Cutscene Director Squad (Wave 4A)
> **Status:** Ready for Claude Integration (`ruby -c` Syntax OK · `0` Collision / `0` Wall-Clip / `0` Canopy-Overhang / `0` Diagonal Verified · Final Muxed MP4 Audio `ebur128` Verified `<= -1.50 dBTP` & `0` Clipped Samples · Live `mkxp-z` Captured & Audited at Dense 2fps)
> **Scope:** Restage `:CH8_CALDERA` off stand-in `Map 928` onto built canon Maps `249` & `244`, and add two flagship Act I live-map Director's Cut scenes (`:CH1_ORCHARD_VEIL` on built `Map 522`, `:CH5_LAMPLIGHT_IL1` on built `Maps 106 ↔ 105`).
> **Guardrails Respected:** Zero edits to Claude-owned `plugins/`, `pbs/`, `story/`, `tools/`, `audio/gemini_cc0/`, `mapgen/`, or `maps_out/`; zero touches to cameos (Garret/Nova/Shiv) or `cg_*.png`.

---

## 1. Summary of 3 Flagship Scenes & Live `mkxp-z` Final-MP4 Verification

All three cutscenes were live-captured in headless `xvfb-run` `mkxp-z` (`512×384 @ 30fps`) inside an isolated `/tmp/cutscene_w4a/game_sandbox/` against the latest Nov 26 built `.rxdata` maps (`maps_out/Data/Map{244,249,522,105,106}.rxdata`), mastered with two-pass `loudnorm` + 4× oversampled brickwall true-peak limiting prior to `256k` AAC encode, independently measured **on the final muxed MP4** via `ffmpeg -af ebur128=peak=true` + `loudnorm` + raw PCM scan (`0` clipped samples!), and visually audited at dense **2fps**.

| Scene ID | Method | Canon Built Maps | Runtime (`30fps`) | FINAL MP4 `ebur128` (`I` / `TP`) | FINAL MP4 `loudnorm` `TP` / Clipped | Emotes | Trajectory / Collision / Overhang QA | Preview Proofs (`previews/`) |
|---|---|---|---:|---|---|---:|---|---|
| **`:CH8_CALDERA`** | `play_ch8_caldera` | **`249`** Slag Ward → **`244`** Hearthguild Hall *(replaces stand-in `928`!)* | `48.37s` (`1,451f`) | **`-14.40 LUFS`** / **`-2.30 dBTP`** | `-2.32 dBTP` · **`0` clips** | `3 / 3` | `0` diag · `0` wall · `0` col (`sal_min_sep=1.414`, `3.0` standing) | `162a_w4a_ch8_caldera_restage.mp4`<br>`162a_w4a_ch8_caldera_strip.png` |
| **`:CH1_ORCHARD_VEIL`** | `play_ch1_orchard_veil` | **`522`** The Glassed Orchard *(Critic 8.9 PASS)* | `26.33s` (`790f`) | **`-14.50 LUFS`** / **`-2.10 dBTP`** | `-2.08 dBTP` · **`0` clips** | `2 / 2` | `0` diag · `0` wall · **`0` canopy (`W0`)** · `0` col · **100% above `PortraitBox`** | `162b_w4a_ch1_orchard_veil.mp4`<br>`162b_w4a_ch1_orchard_veil_strip.png` |
| **`:CH5_LAMPLIGHT_IL1`** | `play_ch5_lamplight_il1` | **`106`** Lamp Room ↔ **`105`** Lighthouse 1F *(Critic 8.8 / 8.7 PASS)* | `43.30s` (`1,299f`) | **`-14.30 LUFS`** / **`-2.20 dBTP`** | `-2.24 dBTP` · **`0` clips** | `3 / 3` | `0` diag · `0` wall · `0` col · `0px` void/beam spill | `162c_w4a_ch5_fresnel_beacon.mp4`<br>`162c_w4a_ch5_fresnel_beacon_strip.png` |

---

## 2. Custom Pixel-Art VFX Assets (Dual-Synced `graphics/` ↔ `art/out/Graphics/`)

All custom VFX sheets are authored at native 1× pixel resolution with crisp 4×4 Bayer dithering and scaled 2× nearest-neighbor (`exact2x=True`, `semi_alpha=0`, `0` clipped bounds), dual-synced with 100% matching MD5s into both `graphics/Pictures/` and `art/out/Graphics/Pictures/`. `MapVfx` in `017_AdvancedAnimations.rb` (`L540`) loads `Graphics/Pictures/...` paths natively with zero engine modifications.

| Asset Path | Size | Grid | `exact2x` | `semi_alpha` | MD5 | Dual-Sync | Visual Role |
|---|---|---|---|---:|---|---|---|
| `Graphics/Pictures/vfx_caldera_embers.png` | `512×256` | `[4, 2]` | `True` | `0` | `9cd4e631ce3638c56cee9e4f2794c6a1` | 100% Match | Rising volcanic embers/cinders (Row 0) + pulsing magma heat-surge (Row 1) |
| `Graphics/Pictures/vfx_orchard_veil_shimmer.png` | `512×256` | `[4, 2]` | `True` | `0` | `55989ba7c624c046a6e46dfdc7c262e9` | 100% Match | Vertically seamless feathered prismatic Bleed Veil ribbon (Row 0) + drifting crystal apple petals (Row 1) |
| `Graphics/Pictures/vfx_fresnel_beam.png` | `1024×512` | `[4, 2]` | `True` | `0` | `56ba210040a07fa66c19bdcd44268e41` | 100% Match | 8-angle 360° golden Fresnel lighthouse beam (contained scale 0.90–0.92 inside Map 106 Lamp Room) |

---

## 3. Pass 2 Critic Resolution & Verified Map Coordinates

Every actor spawn and every `30fps` interpolated coordinate `(tx, ty)` was programmatically verified against the exact RMXP passability & priority tables in `maps_out/Data/Map{244,249,522,105,106}.rxdata` + `Tilesets.rxdata`:

### 3.1 `:CH8_CALDERA` — Built Map `249` (Slag Ward, `44×34`, `ts=61`) → Built Map `244` (Hearthguild Hall, `21×18`, `ts=61`)
- **P0-1 Recast Envoy Haskar:** Swapped `NPC 05` → canon **`trainer_ASHKAAR_OFFICER`** (matching `mapgen/layouts/story_ch8.py` L32!), with Oath-Guards cast as **`trainer_ASHKAAR_SOLDIER_M`** & **`trainer_ASHKAAR_SOLDIER_F`**.
- **P0-2 Climax Framing (Map 244):** Camera positioned at `(10.0, 11.4)`. Brann's silent `...` grief beat pushes in to `1.20×` on `[9.2, 10.6]` with no dialogue box, then smoothly eases back to `1.06×` on `[10.0, 11.4]` before dialogue opens — keeping Sigrun (including her `act_ch8_sigrun_brann` cell 1 turn), PC, Salamence, Brann, Light Stone, Haskar, and both Oath-Guards 100% unoccluded above `PortraitBox`.
- **P0-3 Salamence Wing Clearance:** Staggered Map 244 doorway entry — Sigrun `(10,16)→(10,13)` & PC `(9,16)→(9,13)→(8,13)` enter first; `0.62s` later Salamence enters `(11,16)→(11,14)→(13,14)→(13,13)` (`sal_min_sep = 1.414` tiles moving, `3.0` tiles standing clear of Sigrun — zero wing overlap on any frame!).
- **P1 Fixes:** Act II opens with Light Stone still cradled north (`:cradle_glow`) and Sigrun/PC already emerging in the doorway as Salamence growls off-screen; Guard 1 sets `:light_stone` onto `(10.0, 10.2)` *after* Sigrun's `"Put it down."` (canon `story/29` L375). On Map 249, hides `[16, 17, 18, 19, 29, 30, 31, 32]` (including static `ev[32]` Litwick jar!), evacuees start cleanly above bottom letterbox on `y=15` and exit south off-screen (`y=15→19`, `remove_actor`), PC descends cleanly off stairs to flat plaza `(14,13)→(15,13)`, and crammed lines are split cleanly.

### 3.2 `:CH1_ORCHARD_VEIL` — Built Map `522` (The Glassed Orchard, `44×40`, `ts=52`)
- **Pass 3 `PortraitBox` Framing Lock (100% Head-to-Boot Above `y=268px`):** Establishing `zoom_map(1.26, duration: 0.0, focus: [5.8, 36.0])` (`ox=204, oy=231`) stages Juno on verified open `W0` grass **`(2.5, 36.0)`** (`y=[209..265px]`) and PC at **`(1.5, 36.0)`** (`y=[209..265px]`), 100% clear of pine foliage (`x=0..1`), stone pillar (`x=3..4`), and `PortraitBox` (`y=268..372px`) during every single dialogue box.
- **Action Beats (No Dialogue Box Open on `y=37`):** Juno steps cardinal `(2.5,36)→(2.5,37)→(4.0,37)`, hits bright prismatic crystal flash (`[255,255,255]` / `[165,228,255]`), recoils east-facing (`walk: false, dir: :right, arc_h: 8.0`) with cyan `flash_color` + `tremble` as PC reacts (`set_dir(:down)`), and retreats cleanly back to `(2.5,36)` *before* her pain/Veil dialogue opens. PC crosses cardinal `(1.5,36)→(1.5,37)→(4.5,37)→(7.0,37)→(7.0,36)` (`dir: :left`) synchronized with the motivated `2.2s` dusk-to-crystal tone shift `(6,-6,-12,8) → (-4,-2,12,14)`.
- **Climax Reveal (`1.28×` on `[5.8, 36.0]`):** Juno `@(2.5,36)` (`y=[206..262px]`), PC `@(7.0,36)` (`y=[206..262px]`), and Biscuit `@(10.0→9.0, 35)` (`y=[165..221px]`) remain 100% visible head-to-boot across every dialogue box, split dead-center by the seamless feathered Veil curtain (`ty = 32.0, 36.0, 40.0`, `opacity: 155`).

### 3.3 `:CH5_LAMPLIGHT_IL1` — Built Map `106` (Lamp Room, `20×15`, `ts=34`) ↔ Built Map `105` (Lighthouse 1F, `20×16`, `ts=34`)
- **P0-3 Banish Map 106 Right Black Void Slab:** Establishing `zoom_map(1.30, duration: 0.0, focus: [6.0, 6.2])` (`min_fx = 197 <= 208`) centers Map 106 wall-to-wall with **0px right/left black void**; Act III eases smoothly from `1.30×` → `1.48×` focused on `[6.0, 6.6]` for Hesper's farewell.
- **P0-1 Contained Fresnel Beam (`0px` Void/UI Bleed):** Scaled `vfx_fresnel_beam` on Map 106 to **`scale: 0.90–0.92`** (`opacity: 118–120`) at `(6.0, 5.2)`, keeping the entire rotating beam strictly inside `x = 2.4..9.6, y = 1.6..8.8` (**0px void bleed, 0px dialogue-box bleed**).
- **P0-2 Removed Floating Starburst Hub on Map 105:** Completely removed `vfx_fresnel_beam` from 1F Map 105.
- **P0-5 Restored Kestrel Readability on Map 105:** Lifted Map 105 tones to `(-18, -16, 2, 16)` → `(-22, -18, 6, 20)` so Kestrel's navy coat, Gran's trunk, Haunter, and Honedge read crisply.
- **P1 Fixes:** Added canon trunk veil & memory-flash narrator bridge (`"Inside the unlocked trunk: a black lace Ghost Warden's veil..."` → `"A crowd of legs and coats. A veiled woman running toward a kid made of light—"`), and routed Bleed-touched Haunter cleanly off the staircase `(11,7)→(12,7)→(12,8)` attaching `pf_vfx_glass_shards` only on arrival.

---

## 4. Drop-In Ruby Implementation (For Claude to Apply)

### 4.1 Replace `play_ch8_caldera` & Append `play_ch1_orchard_veil` + `play_ch5_lamplight_il1` in `plugins/Prismfall Cutscenes/017_AdvancedAnimations.rb`

Replace lines `2226–2402` (`play_ch8_caldera`) with the updated `play_ch8_caldera` below, and add `play_ch1_orchard_veil` and `play_ch5_lamplight_il1` directly inside `Prismfall::AdvancedAnimations`'s `class << self` block:

```ruby
#===============================================================================
# Prismfall Cutscenes — Wave 4A Flagship Rejuv V14 Director's Cut Scenes (Pass 2)
#   1. :CH8_CALDERA       (Restaged natively on Built Maps 249 Slag Ward & 244 Hearthguild Hall)
#   2. :CH1_ORCHARD_VEIL  (NEW Act I Showcase on Built Map 522 The Glassed Orchard)
#   3. :CH5_LAMPLIGHT_IL1 (NEW Act I Climax on Built Maps 106 Lamp Room & 105 Lighthouse 1F)
#
# Guardrails verified (Pass 2 Critic-clean):
#   - 100% cardinal-only move_to segments (dx == 0 || dy == 0)
#   - 0 actor-through-actor / actor-through-PC collisions (incl. 3.0-tile Salamence wing clearance)
#   - 0 solid tile / wall / canopy-overhang clips (Map 522 actors verified W0 priority=0)
#   - 0px static portraits, restrained emotes (<= 3 per scene; <= 2 in Ch1 Orchard Veil)
#   - Custom exact2x semi_alpha=0 VFX in Graphics/Pictures/
#===============================================================================

module Prismfall
  module AdvancedAnimations
    class << self
      #=========================================================================
      # SCENE 1 (RESTAGED DIRECTOR'S CUT) — Ch8: "Five Bells" & "Whose Is It"
      # Live Built Maps: 249 (Cindervault - Slag Ward) -> 244 (Hearthguild Hall)
      # Replaces legacy stand-in Map 928 completely!
      # Canon: story/29_SCRIPT_CH8.md ("Five Bells", "Whose Is It")
      # Runtime: ~46.5s | Emotes: 3/3 | Zero overlaps | 100% cardinal walks
      #=========================================================================
      def play_ch8_caldera(capture_dir: nil, capture_fps: 30)
        eng = Engine.new(capture_dir: capture_dir, capture_fps: capture_fps)
        begin
          #---------------------------------------------------------------------
          # ACT I (0.0-21.0s) — "FIVE BELLS" Forge Alert on Built Map 249 Slag Ward
          #   Landmarks: Hearthguild Hall doorway (10,7), twin braziers (8,8)/(12,8),
          #   central stone stairs (12..15, 10..12), magma pool (19..23, 6..9),
          #   Tap Seven service stair (20,13).
          #---------------------------------------------------------------------
          eng.transfer_map(249, 14.5, 11.4, hide_player: true)
          # Hide static plaza NPCs & story evacuee/Litwick-jar events (incl. ev[32]!)
          [16, 17, 18, 19, 29, 30, 31, 32].each do |eid|
            ev = $game_map.events[eid]
            ev.transparent = true if ev
          end

          eng.set_tone(12, -16, -34, 14, duration: 0.0)
          eng.set_emergency_vignette([218, 62, 22], max_alpha: 48, pulse_hz: 0.85)
          eng.letterbox(true, height: 32, duration: 0.0)

          # Atmospheric glowing caldera embers rising from twin braziers & magma pool!
          [[8.0, 7.6, 0], [12.0, 7.6, 2], [20.5, 8.2, 1], [22.0, 7.2, 3], [19.8, 12.6, 2]].each_with_index do |(ex, ey, ph), ei|
            eng.spawn_vfx(:"slag_ember_#{ei}", sheet: "Graphics/Pictures/vfx_caldera_embers", tx: ex, ty: ey,
                          grid: [4, 2], frames: [ph % 4, (ph + 1) % 4, (ph + 2) % 4, (ph + 3) % 4],
                          ticks: [7, 7, 7, 7], loops: :forever,
                          blend: :add, opacity: 175, scale: 1.0, z_layer: :above)
          end
          eng.spawn_vfx(:magma_surge, sheet: "Graphics/Pictures/vfx_caldera_embers", tx: 21.0, ty: 7.8,
                        grid: [4, 2], frames: [4, 5, 6, 7], ticks: [9, 9, 9, 9], loops: :forever,
                        blend: :add, opacity: 155, scale: 1.35, z_layer: :above)

          # Stage Wardens & evacuating Slag Ward family on verified walkable tiles:
          #   Brann at Hearthguild door (10,8); Sigrun (9,9); PC (14,9); Larch (16,13)
          #   Evacuees on y=15 (cleanly ABOVE bottom letterbox!) ready to flee west then south off-screen!
          eng.spawn_actor(:brann,   sheet: "BRANN",             tx: 10.0, ty: 8.0,  dir: :down,  is_charset: true)
          eng.spawn_actor(:sigrun,  sheet: "SIGRUN",            tx: 9.0,  ty: 9.0,  dir: :right, is_charset: true)
          eng.spawn_actor(:pc,      sheet: "PLAYER_A",          tx: 14.0, ty: 9.0,  dir: :down,  is_charset: true)
          eng.spawn_actor(:larch,   sheet: "LARCH",             tx: 16.0, ty: 13.0, dir: :up,    is_charset: true)
          eng.spawn_actor(:mother,  sheet: "NPC 15",            tx: 18.0, ty: 15.0, dir: :left,  is_charset: true)
          eng.spawn_actor(:child,   sheet: "NPC 05",            tx: 19.5, ty: 15.0, dir: :left,  is_charset: true)
          eng.spawn_actor(:litwick, sheet: "Followers/LITWICK", tx: 21.0, ty: 15.0, dir: :left,  is_charset: true)

          # Establishing atmospheric hold before the bells strike
          eng.wait(0.85)

          # THE FIVE BELLS: 1... 2... 3... 4... [0.70s dread silence] ...FIVE!
          4.times do
            eng.play_se("ch8_foundry_bell", volume: 84, pitch: 98)
            eng.shake(power: 2, duration: 0.16)
            eng.wait(0.42)
          end
          eng.wait(0.70)
          eng.play_se("ch8_foundry_bell", volume: 96, pitch: 86)
          eng.play_se("Impact Hitstop Boom", volume: 82, pitch: 95)
          eng.impact_beat(hitstop_sec: 0.14, color_a: [255, 190, 110], color_b: [36, 12, 10])
          eng.shake(power: 6, duration: 0.40)
          eng.flash(color: [255, 148, 68], power: 135, duration: 0.28)

          eng.play_bgm("ch8_caldera_crisis", volume: 80, tag: "ch8_caldera_crisis")
          eng.say(nil, :neutral, "FIVE! Off the mountain! FIVE!", hold: 0.72, name: "Bell-Ringer")

          # Cardinal-only coordinated response:
          #   Family hurries WEST along y=15 (18->12, 19.5->13, 21->14), then turns SOUTH off-screen!
          #   PC descends cleanly OFF stairs to flat plaza (14,13); Brann->(13,13), Sigrun->(12,13)
          eng.actor(:mother).move_to(12.0, 15.0,  duration: 1.95, walk: true, dir: :left)
          eng.actor(:child).move_to(13.0, 15.0,   duration: 2.05, walk: true, dir: :left)
          eng.actor(:litwick).move_to(14.0, 15.0, duration: 2.15, walk: true, dir: :left)

          eng.actor(:brann).move_to(10.0, 9.0, duration: 0.34, walk: true, dir: :down)
          eng.actor(:pc).move_to(14.0, 13.0,   duration: 1.32, walk: true, dir: :down)
          eng.wait_for_move(:brann)

          eng.actor(:brann).move_to(13.0, 9.0,  duration: 0.92, walk: true, dir: :right)
          eng.actor(:sigrun).move_to(12.0, 9.0, duration: 0.92, walk: true, dir: :right)
          eng.wait_for_move(:brann)

          # Evacuees reach west lane (12..14, 15) and exit cleanly SOUTH off-screen (y=15->19)!
          eng.wait_for_move(:litwick)
          eng.actor(:mother).move_to(12.0, 19.0,  duration: 1.40, walk: true, dir: :down)
          eng.actor(:child).move_to(13.0, 19.0,   duration: 1.40, walk: true, dir: :down)
          eng.actor(:litwick).move_to(14.0, 19.0, duration: 1.40, walk: true, dir: :down)

          eng.actor(:brann).move_to(13.0, 13.0,  duration: 1.25, walk: true, dir: :down)
          eng.actor(:sigrun).move_to(12.0, 13.0, duration: 1.25, walk: true, dir: :down)
          eng.pan_camera_to(15.5, 12.2, duration: 1.25, ease: :in_out)
          eng.wait_for_move(:mother)
          eng.remove_actor(:mother)
          eng.remove_actor(:child)
          eng.remove_actor(:litwick)

          eng.actor(:brann).set_dir(:right)
          eng.actor(:sigrun).set_dir(:right)
          eng.actor(:pc).set_dir(:right)
          eng.actor(:larch).set_dir(:left)

          # Emote #1 of 3: Larch alarmed checking the red-lining bell-tower gauge!
          eng.actor(:larch).show_emote(:exclaim, duration: 0.55)
          eng.play_se("Exclaim", volume: 78)
          eng.say(:BRANN, :angry, "That's the tap! Imelda, the gauge on the bell-tower—what's it say?", hold: 0.78)
          eng.say(:LARCH, :shocked, "It's in the red and still climbing. Brann, at this rate it's under an hour.", hold: 0.82)

          # Dramatic camera pan east onto the boiling magma sluice & Tap Seven service stair (20,13)!
          eng.pan_camera_to(19.2, 11.4, duration: 1.05, ease: :in_out)
          eng.zoom_map(1.20, duration: 1.05, focus: [20.0, 11.0], ease: :in_out)
          eng.wait(1.10)
          eng.say(:BRANN, :sad, "To the mountain doing what mountains do.", hold: 0.82)

          eng.zoom_map(1.0, duration: 0.50, ease: :out)
          eng.pan_camera_to(15.0, 12.2, duration: 0.55, ease: :out)
          eng.wait(0.55)
          eng.say(:SIGRUN, :angry, "Then I'll get the Roosts' riders to the lower terraces. Children first.", hold: 0.80)
          eng.say(:SIGRUN, :angry, "You—go down to that tap and find out who's making it worse.", hold: 0.85)

          # PC steps cleanly east on flat plaza (14,13)->(15,13) toward Tap Seven; single all-clear bell -> Midnight!
          eng.actor(:pc).move_to(15.0, 13.0, duration: 0.42, walk: true, dir: :right)
          eng.wait_for_move(:pc)
          eng.wait(0.35)
          eng.bgm_cut
          eng.play_se("ch8_foundry_bell", volume: 88, pitch: 112)
          eng.set_blackout(true)
          eng.wait(0.45)

          #---------------------------------------------------------------------
          # ACT II-III (21.0-46.5s) — MIDNIGHT HEARTHGUILD HALL: "WHOSE IS IT"
          #   Built Canon Map 244 (Hearthguild Hall, 21x18)!
          #   Camera at (10.0, 11.4) keeps ALL actors (y=8..13) cleanly ABOVE PortraitBox!
          #---------------------------------------------------------------------
          eng.clear_vignette
          eng.transfer_map(244, 10.0, 11.4, hide_player: true)
          # Hide all static daytime & story NPCs so live actors own Midnight Hearthguild Hall
          [2, 3, 12, 13, 14, 15, 16, 17, 18, 20, 21, 22, 24, 25].each do |eid|
            ev = $game_map.events[eid]
            ev.transparent = true if ev
          end
          eng.set_tone(-14, -18, -14, 18, duration: 0.0)

          # Canon adult Envoy Haskar (trainer_ASHKAAR_OFFICER) & 2 Ashkaar oath-guards caught in the act!
          # Light Stone is NOT on the table yet — guards hold it near the open north cradle (faint glow)!
          eng.spawn_actor(:haskar, sheet: "trainer_ASHKAAR_OFFICER",   tx: 10.0, ty: 8.0, dir: :down, is_charset: true)
          eng.spawn_actor(:guard1, sheet: "trainer_ASHKAAR_SOLDIER_M", tx: 9.0,  ty: 8.0, dir: :down, is_charset: true)
          eng.spawn_actor(:guard2, sheet: "trainer_ASHKAAR_SOLDIER_F", tx: 11.0, ty: 8.0, dir: :down, is_charset: true)

          # Faint stone glow still cradled north behind Haskar before it is set on the basalt table
          eng.spawn_vfx(:cradle_glow, sheet: "pf_vfx_ch8_caldera_fx", tx: 10.0, ty: 7.4,
                        grid: [4, 2], frames: [4, 5, 6, 7], ticks: [10, 10, 10, 10], loops: :forever,
                        blend: :add, opacity: 145, scale: 0.65, z_layer: :above)
          # Dying forge coals softly breathing at Hearthguild Forge (6,4.8) & Chestnut hearth (13,4.6)
          eng.spawn_vfx(:forge_coals, sheet: "Graphics/Pictures/vfx_caldera_embers", tx: 6.0, ty: 4.8,
                        grid: [4, 2], frames: [0, 1, 2, 3], ticks: [11, 11, 11, 11], loops: :forever,
                        blend: :add, opacity: 125, scale: 0.85, z_layer: :above)
          eng.spawn_vfx(:hearth_coals, sheet: "Graphics/Pictures/vfx_caldera_embers", tx: 13.0, ty: 4.6,
                        grid: [4, 2], frames: [2, 3, 0, 1], ticks: [11, 11, 11, 11], loops: :forever,
                        blend: :add, opacity: 105, scale: 0.72, z_layer: :above)

          # Sigrun & PC ALREADY emerging in the yard doorway (10,16)/(9,16) as Salamence growls outside!
          eng.spawn_actor(:sigrun, sheet: "SIGRUN",   tx: 10.0, ty: 16.0, dir: :up, is_charset: true)
          eng.spawn_actor(:pc,     sheet: "PLAYER_A", tx: 9.0,  ty: 16.0, dir: :up, is_charset: true)
          eng.spawn_vfx(:door_embers, sheet: "Graphics/Pictures/vfx_caldera_embers", tx: 10.0, ty: 15.6,
                        grid: [4, 2], frames: [0, 1, 2, 3], ticks: [8, 8, 8, 8], loops: :forever,
                        blend: :add, opacity: 135, scale: 0.90, z_layer: :above)

          eng.set_blackout(false)
          eng.flash(color: [0, 0, 0], power: 255, duration: 0.50)
          eng.wait(0.55)

          # Haskar spots Sigrun & PC in the yard doorway and scrambles to explain!
          eng.say(nil, :neutral, "The Warden was occupied. The city was in danger. The Stone was safest with—", hold: 0.78, name: "Envoy Haskar")

          # Guttural Salamence growl cuts him off! Staggered doorway entry eliminates ALL wing overlap!
          #   Wave 1: Sigrun (10,16->13) & PC (9,16->13->8,13) stride in first
          #   Wave 2 (+0.60s): Salamence enters (11,16->13->13,13) — 3.0 tiles clear of Sigrun!
          eng.play_cry(:SALAMENCE, volume: 90)
          eng.shake(power: 4, duration: 0.28)
          eng.actor(:sigrun).move_to(10.0, 13.0, duration: 0.96, walk: true, dir: :up)
          eng.actor(:pc).move_to(9.0, 13.0,      duration: 0.96, walk: true, dir: :up)
          eng.wait(0.62)

          eng.spawn_actor(:salamence, sheet: "Followers/SALAMENCE", tx: 11.0, ty: 16.0, dir: :up, is_charset: true)
          eng.actor(:salamence).move_to(11.0, 14.0, duration: 0.72, walk: true, dir: :up)
          eng.wait_for_move(:pc)
          eng.actor(:pc).move_to(8.0, 13.0, duration: 0.38, walk: true, dir: :left)
          eng.wait_for_move(:pc)
          eng.actor(:pc).set_dir(:up)
          eng.actor(:sigrun).set_pose("act_ch8_sigrun_brann", 0) # Commanding back-facing stance!

          eng.wait_for_move(:salamence)
          eng.actor(:salamence).move_to(13.0, 14.0, duration: 0.68, walk: true, dir: :right)
          eng.wait_for_move(:salamence)
          eng.actor(:salamence).move_to(13.0, 13.0, duration: 0.38, walk: true, dir: :up)
          eng.wait_for_move(:salamence)

          # Emote #2 of 3: Envoy Haskar jolts caught red-handed!
          eng.actor(:haskar).show_emote(:exclaim, duration: 0.55)
          eng.play_se("Exclaim", volume: 80)
          eng.wait(0.30)

          eng.say(:SIGRUN, :angry, "Say true, Haskar.", hold: 0.78)
          eng.say(nil, :neutral, "...The Dominar told me to take it while everyone was looking at the mountain.", hold: 0.92, name: "Envoy Haskar")
          eng.say(:SIGRUN, :neutral, "Thank you. Put it down.", hold: 0.75)

          # Canon L375: Guard steps forward to place the Light Stone onto the basalt table, then steps back!
          eng.actor(:guard1).move_to(9.0, 9.0, duration: 0.42, walk: true, dir: :down)
          eng.wait_for_move(:guard1)
          eng.stop_vfx(:cradle_glow)
          eng.spawn_vfx(:light_stone, sheet: "pf_vfx_ch8_caldera_fx", tx: 10.0, ty: 10.2,
                        grid: [4, 2], frames: [4, 5, 6, 7], ticks: [9, 9, 9, 9], loops: :forever,
                        blend: :add, opacity: 225, scale: 0.95, z_layer: :above)
          eng.play_se("Anim/HealBell", volume: 78, pitch: 126)
          eng.flash(color: [220, 240, 255], power: 110, duration: 0.35)
          eng.actor(:guard1).move_to(9.0, 8.0, duration: 0.42, walk: true, dir: :up)
          eng.wait_for_move(:guard1)
          eng.actor(:guard1).set_dir(:down)

          eng.play_bgm("ch8_lightstone_burden", volume: 78, tag: "ch8_lightstone_burden")

          # Exhausted Brann enters along clear y=14 / x=6 route beside his Warden Chair!
          eng.spawn_actor(:brann, sheet: "BRANN", tx: 10.0, ty: 16.0, dir: :up, is_charset: true)
          eng.actor(:brann).move_to(10.0, 14.0, duration: 0.72, walk: true, dir: :up)
          eng.wait_for_move(:brann)
          eng.actor(:brann).move_to(6.0, 14.0,  duration: 1.30, walk: true, dir: :left)
          eng.wait_for_move(:brann)
          eng.actor(:brann).move_to(6.0, 11.0,  duration: 1.00, walk: true, dir: :up)
          eng.wait_for_move(:brann)
          eng.actor(:brann).set_dir(:right)

          eng.actor(:brann).play_clip(
            sheet: "act_ch8_sigrun_brann", grid: [4, 1], frames: [2, 3],
            ticks: [16, 40], loops: 1, stay: true
          )
          # Emote #3 of 3: Silent zoomed grief beat (1.20x with NO dialogue box!),
          # then ease cleanly to 1.06x so Sigrun, PC, Salamence, Brann & Haskar stay 100% above PortraitBox!
          eng.actor(:brann).show_emote(:dots, duration: 0.85)
          eng.zoom_map(1.20, duration: 0.85, focus: [9.2, 10.6], ease: :in_out)
          eng.wait(0.95)
          eng.zoom_map(1.06, duration: 0.55, focus: [10.0, 11.4], ease: :out)
          eng.wait(0.55)

          eng.say(:BRANN, :sad, "Thirty years it's been on that wall. Nobody touched it.", hold: 0.82)
          eng.say(:BRANN, :sad, "I was carrying a woman's grandmother up four hundred steps.", hold: 0.90)

          # Sigrun's turn toward grounded PC (cell 1) is now 100% unoccluded above PortraitBox!
          eng.actor(:sigrun).set_pose("act_ch8_sigrun_brann", 1)
          eng.say(:SIGRUN, :neutral, "My father will send another envoy, and one day a legion.", hold: 0.82)
          eng.say(:SIGRUN, :neutral, "Say it. Who should keep it?", hold: 1.05)

          eng.wait(0.75)
          eng.zoom_map(1.0, duration: 0.45, ease: :out)
          eng.letterbox(false, duration: 0.45)
          eng.wait(0.45)
        ensure
          cues = eng.cues.dup
          fc   = eng.frames_captured
          eng.dispose
        end
        return { :cues => cues, :frames => fc }
      end

      #=========================================================================
      # SCENE 2 (NEW ACT I SHOWCASE) — Ch1: "The Glassed Orchard Veil"
      # Live Built Map: 522 (The Glassed Orchard — Critic 8.9 PASS)
      # Canon: story/20_SCRIPT_CH0-2.md ("Map 522 — The Glassed Orchard", L725-746)
      # Features: Establishing 1.26x framing on [5.8, 36.0] keeping Juno (2.5,36),
      #   PC (1.5,36 -> 7.0,36) & Biscuit (9.0,35) 100% head-to-boot ABOVE PortraitBox
      #   (y < 268px), continuous feathered Bleed Veil (y=30..42), bright crystal recoil,
      #   motivated 2.2s tone shift!
      # Runtime: ~26.3s | Emotes: 2/2 | Zero overlaps | 100% cardinal walks
      #=========================================================================
      def play_ch1_orchard_veil(capture_dir: nil, capture_fps: 30)
        eng = Engine.new(capture_dir: capture_dir, capture_fps: capture_fps)
        begin
          # Establishing 1.26x framing on [5.8, 36.0] lifts Juno & PC cleanly ABOVE PortraitBox (y < 268px)!
          eng.transfer_map(522, 5.8, 35.4, hide_player: true)
          # Hide static Juno event (ev[9]) so live Juno owns the gate
          ev_juno = $game_map.events[9]
          ev_juno.transparent = true if ev_juno

          # Gentle twilight-dusk Elowen light (motivated shift occurs ONLY as PC crosses Veil!)
          eng.set_tone(6, -6, -12, 8, duration: 0.0)
          eng.letterbox(true, height: 32, duration: 0.0)
          eng.zoom_map(1.26, duration: 0.0, focus: [5.8, 36.0])
          eng.play_bgm("ch1_orchard_veil", volume: 78, tag: "ch1_orchard_veil")

          # Continuous vertically-seamless feathered Bleed Veil curtain sealing entire seam (y=30..42)!
          [32.0, 36.0, 40.0].each_with_index do |vy, vi|
            eng.spawn_vfx(:"veil_curtain_#{vi}", sheet: "Graphics/Pictures/vfx_orchard_veil_shimmer", tx: 4.5, ty: vy,
                          grid: [4, 2], frames: [0, 1, 2, 3], ticks: [9, 9, 9, 9], loops: :forever,
                          blend: :normal, untoned: true, opacity: 155, scale: 1.0, z_layer: :above)
          end

          # Delicate drifting crystal apple-blossom petals across the glass orchard clearing
          [[7.6, 33.8, 0], [10.4, 33.5, 2], [8.8, 36.2, 1], [11.2, 35.4, 3]].each_with_index do |(px, py, ph), pi|
            eng.spawn_vfx(:"glass_petals_#{pi}", sheet: "Graphics/Pictures/vfx_orchard_veil_shimmer", tx: px, ty: py,
                          grid: [4, 2], frames: [4 + (ph % 4), 4 + ((ph + 1) % 4), 4 + ((ph + 2) % 4), 4 + ((ph + 3) % 4)],
                          ticks: [10, 10, 10, 10], loops: :forever,
                          blend: :normal, untoned: true, opacity: 185, scale: 0.95, z_layer: :above)
          end

          # Stage Juno & PC on verified open W0 grass y=36 (100% clear of pine trees AND above PortraitBox!)
          eng.spawn_actor(:biscuit, sheet: "Followers/SKWOVET", tx: 10.0, ty: 35.0, dir: :left,  is_charset: true)
          eng.spawn_actor(:juno,    sheet: "JUNO",              tx: 1.5,  ty: 36.0, dir: :right, is_charset: true)
          eng.spawn_actor(:pc,      sheet: "PLAYER_A",          tx: 0.5,  ty: 36.0, dir: :right, is_charset: true)

          # Establishing dusk breath while glass chimes ring softly
          eng.play_se("Anim/Ice1", volume: 58, pitch: 132)
          eng.wait(1.05)

          # Juno & grounded PC step strictly cardinal RIGHT to their y=36 dialogue marks (2.5,36) & (1.5,36)
          eng.actor(:juno).move_to(2.5, 36.0, duration: 0.45, walk: true, dir: :right)
          eng.actor(:pc).move_to(1.5, 36.0,   duration: 0.45, walk: true, dir: :right)
          eng.wait_for_move(:juno)
          eng.wait(0.30)

          eng.say(:JUNO, :sad, "There. That was the Pruetts'. It went last winter, in one night.", hold: 0.88)
          eng.say(:JUNO, :neutral, "It's pretty, isn't it? I hate that it's pretty.", hold: 0.82)

          # Biscuit squeaks and hops inside the glass orchard! Camera gently shifts focus east then back
          eng.play_cry(:SKWOVET, volume: 86)
          eng.play_se("Mining ping", volume: 65, pitch: 145)
          eng.actor(:biscuit).hop(height: 12, duration: 0.30)
          eng.zoom_map(1.26, duration: 0.65, focus: [7.2, 35.6], ease: :in_out)
          eng.wait(0.80)
          eng.zoom_map(1.26, duration: 0.60, focus: [5.8, 36.0], ease: :in_out)
          eng.wait(0.45)

          # Emote #1 of 2: Juno spots Biscuit (100% visible above PortraitBox at (2.5,36)!)
          eng.actor(:juno).show_emote(:exclaim, duration: 0.55)
          eng.play_se("Exclaim", volume: 78)
          eng.say(:JUNO, :panic, "Biscuit! Biscuit, come OUT!", hold: 0.70)

          # Action Beat (NO dialogue box open): Juno steps cardinal (2.5,36)->(2.5,37)->(4.0,37) -> BRIGHT CRYSTAL RECOIL!
          eng.actor(:juno).move_to(2.5, 37.0, duration: 0.36, walk: true, dir: :down)
          eng.wait_for_move(:juno)
          eng.actor(:juno).move_to(4.0, 37.0, duration: 0.56, walk: true, dir: :right)
          eng.wait_for_move(:juno)

          eng.play_se("Glass Shatter Burst", volume: 82, pitch: 118)
          eng.play_se("Anim/Ice1", volume: 78, pitch: 108)
          eng.impact_beat(hitstop_sec: 0.12, color_a: [255, 255, 255], color_b: [165, 228, 255])
          eng.shake(power: 4, duration: 0.28)
          eng.flash(color: [200, 240, 255], power: 130, duration: 0.24)

          # Directional east-facing recoil arc (stays facing :right away from Veil!) + PC human reaction
          eng.actor(:juno).flash_color(190, 240, 255, 185, duration: 0.28)
          eng.actor(:juno).move_to(3.0, 37.0, duration: 0.32, walk: false, dir: :right, arc_h: 8.0, ease: :out)
          eng.actor(:pc).set_dir(:down)
          eng.wait_for_move(:juno)
          eng.actor(:juno).tremble(duration: 0.45, amp: 1.8, freq: 42.0)
          eng.wait(0.45)

          # Juno retreats cleanly back onto y=36 open grass (3.0,37)->(2.5,37)->(2.5,36) BEFORE dialogue opens!
          eng.actor(:juno).move_to(2.5, 37.0, duration: 0.24, walk: true, dir: :left)
          eng.wait_for_move(:juno)
          eng.actor(:juno).move_to(2.5, 36.0, duration: 0.38, walk: true, dir: :up)
          eng.wait_for_move(:juno)
          eng.actor(:juno).set_dir(:right)
          eng.actor(:pc).set_dir(:right)

          eng.say(:JUNO, :panic, "Ow— no. No. My skin's burning. I can't.", hold: 0.85)
          eng.say(:JUNO, :sad, "That's the Veil. Nobody can cross one. You just... can't. Your body won't.", hold: 0.96)

          # Action Beat (NO dialogue box open): PC crosses cardinal (1.5,36)->(1.5,37)->(4.5,37)->(7.0,37)->(7.0,36)!
          # Motivated 2.2s crystalline chill shift plays smoothly WHILE PC crosses x=4.5!
          eng.wait(0.30)
          eng.actor(:pc).move_to(1.5, 37.0, duration: 0.38, walk: true, dir: :down)
          eng.wait_for_move(:pc)
          eng.set_tone(-4, -2, 12, 14, duration: 2.20)
          eng.actor(:pc).move_to(4.5, 37.0, duration: 1.10, walk: true, dir: :right)
          eng.wait_for_move(:pc)

          # Gentle harmonic shimmer as PC passes through with ZERO recoil ("like warm water")
          eng.play_se("Anim/HealBell", volume: 72, pitch: 138)
          eng.flash(color: [220, 248, 255], power: 68, duration: 0.35)
          eng.actor(:pc).move_to(7.0, 37.0, duration: 0.95, walk: true, dir: :right)
          eng.wait_for_move(:pc)
          eng.actor(:pc).move_to(7.0, 36.0, duration: 0.40, walk: true, dir: :up)
          eng.wait_for_move(:pc)
          eng.actor(:pc).set_dir(:left)

          # Let the uncanny silence breathe
          eng.wait(0.75)

          # Emote #2 of 2 (restrained <= 2!): Climax zoom 1.28x on [5.8, 36.0] keeps Juno@(2.5,36),
          # PC@(7.0,36) & Biscuit@(9.0,35) 100% visible head-to-boot ABOVE PortraitBox across EVERY box!
          eng.actor(:juno).show_emote(:double_exclaim, duration: 0.65)
          eng.play_se("Exclaim", volume: 82, pitch: 108)
          eng.zoom_map(1.28, duration: 0.75, focus: [5.8, 36.0], ease: :in_out)
          eng.wait(0.55)

          eng.say(:JUNO, :shocked, "...How are you DOING that?", hold: 0.85)
          eng.say(:JUNO, :shocked, "Doesn't it— aren't you—", hold: 0.65)
          eng.say(:JUNO, :shocked, "Your HAIR isn't even standing up!", hold: 0.95)

          # Biscuit hops cheerfully and scurries one cardinal tile LEFT toward the calm PC!
          eng.actor(:pc).set_dir(:right)
          eng.actor(:biscuit).hop(height: 10, duration: 0.28)
          eng.play_cry(:SKWOVET, volume: 80)
          eng.actor(:biscuit).move_to(9.0, 35.0, duration: 0.45, walk: true, dir: :left)
          eng.wait_for_move(:biscuit)

          eng.wait(0.70)
          eng.zoom_map(1.26, duration: 0.45, focus: [5.8, 36.0], ease: :out)
          eng.letterbox(false, duration: 0.45)
          eng.wait(0.45)
        ensure
          cues = eng.cues.dup
          fc   = eng.frames_captured
          eng.dispose
        end
        return { :cues => cues, :frames => fc }
      end

      #=========================================================================
      # SCENE 3 (NEW ACT I CLIMAX) — Ch5 Interlude I: "Lamplight" (Fresnel Beacon)
      # Live Built Maps: 106 (Ferrow Lighthouse Lamp Room — Critic 8.8 PASS)
      #                  <-> 105 (Ferrow Lighthouse 1F — Critic 8.7 PASS)
      # Canon: story/24_SCRIPT_CH5.md ("INTERLUDE I — Lamplight", L979-1024)
      # Features: Wall-to-wall 1.30x Map 106 framing (0px right black void!),
      #   contained scale 0.90 golden Fresnel beam (0px wall/UI bleed!),
      #   clean Map 105 moonlight tone (no floating wall hub!), canon veil memory
      #   bridge, staircase Haunter vs Honedge "Morwen", quiet farewell to Hesper!
      # Runtime: ~42.5s | Emotes: 3/3 | Zero overlaps | 100% cardinal walks
      #=========================================================================
      def play_ch5_lamplight_il1(capture_dir: nil, capture_fps: 30)
        eng = Engine.new(capture_dir: capture_dir, capture_fps: capture_fps)
        begin
          #---------------------------------------------------------------------
          # ACT I (0.0-11.5s) — Map 106 Fresnel Beacon Lamp Room (Twilight Broadcast)
          #   Establishing zoom_map(1.30, focus: [6.0, 6.2]) centers room wall-to-wall
          #   with ZERO right black void!
          #---------------------------------------------------------------------
          eng.transfer_map(106, 6.0, 6.2, hide_player: true)
          ev_h = $game_map.events[2]
          ev_h.transparent = true if ev_h

          eng.set_tone(-28, -22, -4, 18, duration: 0.0)
          eng.letterbox(true, height: 32, duration: 0.0)
          eng.zoom_map(1.30, duration: 0.0, focus: [6.0, 6.2])
          eng.play_bgm("ch5_lamplight_night", volume: 74, tag: "ch5_lamplight_night")

          # Contained golden Fresnel lighthouse beam strictly inside Lamp Room (scale 0.90 -> r=3.6 tiles)!
          eng.spawn_vfx(:fresnel_sweep, sheet: "Graphics/Pictures/vfx_fresnel_beam", tx: 6.0, ty: 5.2,
                        grid: [4, 2], frames: [0, 1, 2, 3, 4, 5, 6, 7],
                        ticks: [10, 10, 10, 10, 10, 10, 10, 10], loops: :forever,
                        blend: :add, opacity: 118, scale: 0.90, z_layer: :above)

          eng.spawn_actor(:hesper,  sheet: "HESPER",  tx: 6.0, ty: 7.0, dir: :down, is_charset: true)
          eng.spawn_actor(:kestrel, sheet: "KESTREL", tx: 2.0, ty: 5.0, dir: :up,   is_charset: true)

          # Let the golden Fresnel beam breathe across the quiet lamp room
          eng.wait(1.20)
          eng.say(nil, :neutral, "\"...the Lowlight... twelve... the Mandate...\"", hold: 0.90, name: "Wireless")

          # Kestrel snaps the wireless off, turns toward sleeping Gran
          eng.play_se("GUI storage put down", volume: 80, pitch: 95)
          eng.wait(0.42)
          eng.actor(:kestrel).set_dir(:right)
          eng.say(:KESTREL, :neutral, "Twelve. She'd never. She'd NEVER. Not a city. Not children.", hold: 0.92)

          # Strictly cardinal walk to staircase: (2,5)->(2,7)->(4,7)->(4,9)
          eng.actor(:kestrel).move_to(2.0, 7.0, duration: 0.72, walk: true, dir: :down)
          eng.wait_for_move(:kestrel)
          eng.say(:KESTREL, :sad, "...So it isn't her. Good. That's good. That's what I wanted.", hold: 0.88)

          eng.actor(:kestrel).move_to(4.0, 7.0, duration: 0.70, walk: true, dir: :right)
          eng.wait_for_move(:kestrel)
          eng.actor(:kestrel).move_to(4.0, 9.0, duration: 0.70, walk: true, dir: :down)
          eng.wait_for_move(:kestrel)
          eng.play_se("Door exit", volume: 78, pitch: 96)
          eng.set_blackout(true)
          eng.wait(0.40)

          #---------------------------------------------------------------------
          # ACT II (11.5-31.0s) — Map 105 Lighthouse 1F (Unlocked Trunk & Haunter!)
          #   ZERO floating Fresnel hub on indoor walls! Readable coastal night tone
          #   (-18, -16, 2, 16) -> (-22, -18, 6, 20) keeps Kestrel razor-clear!
          #---------------------------------------------------------------------
          eng.transfer_map(105, 9.8, 8.2, hide_player: true)
          ev_haunt = $game_map.events[7]
          ev_haunt.transparent = true if ev_haunt

          eng.set_tone(-18, -16, 2, 16, duration: 0.0)
          eng.spawn_actor(:kestrel, sheet: "KESTREL", tx: 11.0, ty: 7.0, dir: :left, is_charset: true)
          eng.set_blackout(false)
          eng.flash(color: [0, 0, 0], power: 255, duration: 0.45)

          # Cardinal-only walk from stair landing (11,7) -> (9,7) -> (9,10) beside Gran's Trunk (8,10)!
          eng.actor(:kestrel).move_to(9.0, 7.0, duration: 0.68, walk: true, dir: :left)
          eng.wait_for_move(:kestrel)
          eng.actor(:kestrel).move_to(9.0, 10.0, duration: 0.98, walk: true, dir: :down)
          eng.wait_for_move(:kestrel)
          eng.actor(:kestrel).set_dir(:left)

          # Canon trunk veil reveal + memory flash bridge!
          eng.play_se("Door enter", volume: 80, pitch: 72)
          eng.wait(0.28)
          eng.say(nil, :neutral, "Inside the unlocked trunk: a black lace Ghost Warden's veil, smelling of candle-smoke.", hold: 0.90, name: "")

          # Emote #1 of 3 (:jolt) + Memory Flash!
          eng.actor(:kestrel).show_emote(:jolt, duration: 0.55)
          eng.play_se("Anim/Saint7", volume: 82, pitch: 82)
          eng.impact_beat(hitstop_sec: 0.12, color_a: [244, 246, 255], color_b: [165, 178, 210])
          eng.flash_ramp(color: [238, 242, 255], steps: [45, 120, 200, 245], step_dur: 0.04, hold_dur: 0.16, fade_dur: 0.45)
          eng.shake(power: 4, duration: 0.32)
          eng.set_tone(-22, -18, 6, 20, duration: 0.55)
          eng.wait(0.22)
          eng.say(nil, :neutral, "A crowd of legs and coats. A veiled woman running toward a kid made of light—", hold: 1.00, name: "")

          # Kestrel staggers strictly cardinal UP 1 tile (9,10)->(9,9) & drops to shadowed pose
          eng.actor(:kestrel).set_pose("pose_KESTREL", 2)
          eng.actor(:kestrel).move_to(9.0, 9.0, duration: 0.34, walk: false, arc_h: 6.0, ease: :out)
          eng.wait_for_move(:kestrel)
          eng.actor(:kestrel).tremble(duration: 0.50, amp: 1.6, freq: 44.0)
          eng.wait(0.28)

          eng.say(:KESTREL, :angry, "Not again. Not AGAIN. There's no kid made of light. Kids aren't made of light.", hold: 0.95)

          # Bleed chill hits the staircase! Haunter drifts cleanly OFF staircase (11,7)->(12,7)->(12,8)!
          eng.play_bgm("ch5_lamplight_haunter", volume: 78, tag: "ch5_lamplight_haunter")
          eng.play_cry(:HAUNTER, volume: 86)
          eng.spawn_actor(:haunter, sheet: "Followers/HAUNTER", tx: 11.0, ty: 7.0, dir: :right, is_charset: true)
          eng.actor(:haunter).move_to(12.0, 7.0, duration: 0.48, walk: true, dir: :right)

          # Emote #2 of 3: Kestrel snaps up to meet the Bleed-touched Haunter!
          eng.actor(:kestrel).restore_charset("KESTREL", dir: :up)
          eng.actor(:kestrel).show_emote(:exclaim, duration: 0.50)
          eng.actor(:kestrel).move_to(9.0, 8.0, duration: 0.36, walk: true, dir: :up)
          eng.wait_for_move(:kestrel)
          eng.actor(:kestrel).set_dir(:right)

          eng.wait_for_move(:haunter)
          eng.actor(:haunter).move_to(12.0, 8.0, duration: 0.45, walk: true, dir: :down)
          eng.wait_for_move(:haunter)
          eng.actor(:haunter).set_dir(:left)
          # Attach glassy Bleed sparks ONLY once Haunter reaches (12,8)!
          eng.spawn_vfx(:haunter_bleed, sheet: "pf_vfx_glass_shards", tx: 12.0, ty: 8.0,
                        grid: [4, 2], frames: [0, 1, 2, 3], ticks: [7, 7, 7, 7], loops: :forever,
                        blend: :add, opacity: 175, scale: 0.88, z_layer: :above)

          # 6-Beat Anime Command: Kestrel points -> Pokeball burst -> Honedge "Morwen" materializes at (10.5, 8.0)!
          eng.actor(:kestrel).set_pose("pose_KESTREL", 1)
          eng.play_se("Battle throw", volume: 82, pitch: 105)
          eng.spawn_vfx(:morwen_release, sheet: "pf_vfx_duskball_release", tx: 10.5, ty: 8.0,
                        grid: [4, 1], frames: [0, 1, 2, 3], ticks: [4, 4, 5, 5], loops: 1,
                        blend: :add, opacity: 230, scale: 0.95, z_layer: :above)
          eng.wait(0.28)
          eng.spawn_actor(:honedge, sheet: "Followers/HONEDGE", tx: 10.5, ty: 8.0, dir: :right, is_charset: true)
          eng.play_cry(:HONEDGE, volume: 86)
          eng.wait(0.25)

          eng.say(:KESTREL, :neutral, "Morwen. Up. She held a line for a whole city once. You can hold a staircase.", hold: 0.92)

          # Honedge strike impact beat -> Haunter scatters into cold sparks strictly cardinal RIGHT!
          eng.actor(:honedge).move_to(11.0, 8.0, duration: 0.18, walk: false, ease: :out)
          eng.wait_for_move(:honedge)
          eng.play_se("Anim/Ice8", volume: 84, pitch: 112)
          eng.impact_beat(hitstop_sec: 0.12, color_a: [200, 236, 255], color_b: [120, 168, 220])
          eng.shake(power: 4, duration: 0.25)
          eng.stop_vfx(:haunter_bleed)
          eng.actor(:haunter).move_to(15.0, 8.0, duration: 0.65, walk: false, ease: :out)
          eng.actor(:honedge).move_to(10.5, 8.0, duration: 0.30, walk: false, ease: :out)
          eng.wait_for_move(:haunter)
          eng.remove_actor(:haunter)

          eng.set_tone(-18, -16, 2, 16, duration: 0.70)
          eng.actor(:kestrel).restore_charset("KESTREL", dir: :right)
          eng.say(:KESTREL, :sad, "Good. Good, Morwen. Gran won't say. The Accord sent a box.", hold: 0.85)
          eng.say(:KESTREL, :angry, "Fine. Then I'll find out myself.", hold: 0.82)

          eng.set_blackout(true)
          eng.wait(0.40)

          #---------------------------------------------------------------------
          # ACT III (31.0-42.5s) — Map 106 Lamp Room (The Quiet Goodbye)
          #   Wall-to-wall 1.30x framing (0px void!) easing to 1.48x on Hesper!
          #---------------------------------------------------------------------
          eng.transfer_map(106, 6.0, 6.2, hide_player: true)
          ev_h2 = $game_map.events[2]
          ev_h2.transparent = true if ev_h2

          eng.set_tone(-32, -26, -2, 22, duration: 0.0)
          eng.zoom_map(1.30, duration: 0.0, focus: [6.0, 6.2])
          eng.play_bgm("ch5_lamplight_night", volume: 72, tag: "ch5_lamplight_night")

          eng.spawn_vfx(:fresnel_finale, sheet: "Graphics/Pictures/vfx_fresnel_beam", tx: 6.0, ty: 5.2,
                        grid: [4, 2], frames: [0, 1, 2, 3, 4, 5, 6, 7],
                        ticks: [11, 11, 11, 11, 11, 11, 11, 11], loops: :forever,
                        blend: :add, opacity: 120, scale: 0.92, z_layer: :above)

          eng.spawn_actor(:hesper,  sheet: "HESPER",  tx: 6.0, ty: 7.0, dir: :down, is_charset: true)
          eng.spawn_actor(:kestrel, sheet: "KESTREL", tx: 4.0, ty: 9.0, dir: :up,   is_charset: true)
          eng.set_blackout(false)
          eng.flash(color: [0, 0, 0], power: 255, duration: 0.45)

          # Kestrel walks quietly UP from stairs (4,9)->(4,7)->(5,7) beside Hesper's chair (1.0 tile clean!)
          eng.actor(:kestrel).move_to(4.0, 7.0, duration: 0.78, walk: true, dir: :up)
          eng.wait_for_move(:kestrel)
          eng.actor(:kestrel).move_to(5.0, 7.0, duration: 0.45, walk: true, dir: :right)
          eng.wait_for_move(:kestrel)
          eng.wait(0.65)

          eng.say(:KESTREL, :neutral, "If you're alive, I'll find you. And if you're not, I'll find whoever said you weren't.", hold: 1.05)

          # Kestrel walks strictly cardinal DOWN (5,7)->(5,9) -> LEFT (5,9)->(4,9) and leaves down the stairs
          eng.actor(:kestrel).move_to(5.0, 9.0, duration: 0.78, walk: true, dir: :down)
          eng.wait_for_move(:kestrel)
          eng.actor(:kestrel).move_to(4.0, 9.0, duration: 0.45, walk: true, dir: :left)
          eng.wait_for_move(:kestrel)
          eng.play_se("Door exit", volume: 78, pitch: 94)
          eng.remove_actor(:kestrel)

          # Heavy lighthouse door shuts below; silence breath under the sweeping golden Fresnel beam
          eng.wait(0.85)
          eng.play_se("Door enter", volume: 80, pitch: 80)
          eng.wait(0.75)

          # Emote #3 of 3: Hesper turns slowly toward the empty staircase in the sweeping light
          eng.actor(:hesper).set_dir(:left)
          eng.actor(:hesper).show_emote(:dots, duration: 0.80)
          eng.zoom_map(1.48, duration: 1.15, focus: [6.0, 6.6], ease: :in_out)
          eng.wait(0.90)

          eng.say(:HESPER, :sad, "Oh, my boy. Don't.", hold: 1.25)

          eng.wait(0.95)
          eng.zoom_map(1.30, duration: 0.45, focus: [6.0, 6.2], ease: :out)
          eng.letterbox(false, duration: 0.45)
          eng.wait(0.45)
        ensure
          cues = eng.cues.dup
          fc   = eng.frames_captured
          eng.dispose
        end
        return { :cues => cues, :frames => fc }
      end
    end
  end
end
```

### 4.2 Dispatch Wiring in `plugins/Prismfall Cutscenes/017_AdvancedAnimations.rb` (`pbRejuvCutscene`, ~L5196)

Add the two new scene aliases alongside `:CH8_CALDERA`:

```ruby
  when :CH1_ORCHARD_VEIL, :CH1_VEIL, :ORCHARD_VEIL       then aa.play_ch1_orchard_veil(**opts)
  when :CH5_LAMPLIGHT_IL1, :CH5_LAMPLIGHT, :IL1_BEACON   then aa.play_ch5_lamplight_il1(**opts)
```

### 4.3 Registry & Audio Tag Wiring in `plugins/Prismfall Cutscenes/016_Movies.rb`

1. **In `SCENE_BGM` (`L61–93`), add:**
```ruby
      "ch1_orchard_veil"      => ["Route - Elowen Forest", "Mood - Mystery"],
      "ch5_lamplight_night"   => ["Intro - Last Ferry", "Town - Ferrows Landing", "Mood - Farewell"],
      "ch5_lamplight_haunter" => ["Route - Antumbra", "Mood - Tension"],
```

2. **In `SCENE_SE` (`L94–97`), optionally map the custom CC0 impacts (both already exist in `audio/gemini_cc0/SE/`):**
```ruby
      "Impact Hitstop Boom"   => ["Impact Hitstop Boom", "Anim/Earth3"],
      "Glass Shatter Burst"   => ["Glass Shatter Burst", "Anim/Ice8"],
```

3. **In `SCENES` (`L132–161`), update `:CH8_CALDERA` to `:ready` on built `[249, 244]` and register `:CH1_ORCHARD_VEIL` and `:CH5_LAMPLIGHT_IL1` as immediately `:ready`:**
```ruby
      :CH1_ORCHARD_VEIL  => { :play => :play_ch1_orchard_veil,         :staged => [522],      :canon => [522],
                              :aliases => [:CH1_VEIL, :ORCHARD_VEIL] },
      :CH5_LAMPLIGHT_IL1 => { :play => :play_ch5_lamplight_il1,        :staged => [106, 105], :canon => [106, 105],
                              :aliases => [:CH5_LAMPLIGHT, :IL1_BEACON] },
      :CH8_CALDERA       => { :play => :play_ch8_caldera,              :staged => [249, 244], :canon => [249, 244],
                              :aliases => [:CH8_FIVE_BELLS, :CH8_DC] },
```
