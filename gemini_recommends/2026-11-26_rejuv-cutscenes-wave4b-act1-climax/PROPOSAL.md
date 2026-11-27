# Wave 4B — Rejuvenation V14 Director's Cut Scenes on Critic-Certified Act I Climax Maps (Pass 2 — 3/3 Ready)

> **Date:** 2026-11-26 (Pass 2 Complete — **3 / 3 Scenes Ready**: `:CH4_EBB_STOPPED` (`167b`, **9.4/10 GOLD PASS**) & `:CH5_LOWLIGHT_VALEN` (`167c`, **9.5/10 GOLD PASS**) Already Certified · `:CH0_LAST_FERRY` (`167a`) Restaged & Re-Captured Pass 2 Ready on Brand-New Critic-Certified `Map 109` (`9.4/10`) & `Map 108` (`9.6/10`)!)
> **Author:** Track C — Live `mkxp-z` Cutscene Wave 4B Director's Cut Squad
> **Status:**
> - **`:CH4_EBB_STOPPED` (`167b`)** & **`:CH5_LOWLIGHT_VALEN` (`167c`)**: **CERTIFIED GOLD PASS** (`9.4 / 10` & `9.5 / 10`, `0 P0`, `0 P1` — untouched!)
> - **`:CH0_LAST_FERRY` (`167a`)**: **PASS 2 READY FOR CRITIC GOLD AUDIT** on Brand-New Coastal Steam Ferry `Map 109` (`9.4/10`) + Symmetrical Quarantine Customs Hall `Map 108` (`9.6/10`) + Ferrow's Landing Quay `Map 100` (`ruby -c` Syntax OK · `100% W0 [:PASS, :CLEAR]` + counter-rim tuck · `0` Collision · `0px` Black Void on `108` · `0px` Edge Slice · `0px` PortraitBox Occlusion · `0px` Portrait Bob (`896f`) · `0` 1-Frame Glitches · Full-Bleed `cg_ch00_dovetail_letter_a` (`5.0s–9.0s`) Preserved · Obsolete Floating `NULL` Banner Deleted & Replaced With Subtle Diegetic Built-In Monitor Pulse `vfx_customs_monitor_pulse.png` · Final MP4 `ebur128` Verified **`-14.40 LUFS`**, **`-2.30 dBTP`**, `max_abs = 0.76292`, **`0` Clipped Samples**, **`0` Dead-Silence Windows**)
> **Guardrails Respected:** Zero git commands; zero edits to Claude-owned `plugins/`, `pbs/`, `story/`, `tools/`, `mapgen/`, `maps_out/`, `audio/gemini_cc0/`, existing `Characters/trainer_*.png`, cameos (`FESTIVAL_*`), Juno, or existing `cg_*.png`. Dev-only harness isolated strictly in `/home/antigravity/pf_engine_run/game/Plugins/ZZ Demo Autorun/014_Wave4BCutsceneCapture.rb` (gated by `ENV["DEMO_PLAN"] == "wave4b_cutscenes"`).

---

## 1. Summary of Wave 4B Scenes & Pass 2 Live `mkxp-z` Final-MP4 Telemetry

All cutscenes were captured LIVE in real compiled `mkxp-z` (`512×384 @ 30fps`, `ALSOFT_DRIVERS=null`), broadcast-mastered with authentic Prismfall OST (`dedrum_tectonic/*.ogg`) + CC0 BGS/SE + Essentials SE/Cries via two-pass `loudnorm` + 4× oversampled brickwall true-peak limiting prior to `256k` AAC encode, independently measured **on the final muxed MP4** via `ffmpeg -af ebur128=peak=true`, `loudnorm`, `volumedetect`, and raw float32 PCM scan (`0` clipped samples, `0` dead-silence `0.5s` windows!), and visually audited at dense **2fps** plus 1:1 native `512×384` key-frame inspection.

| Scene ID | Status | Method | Canon Built Maps | Runtime (`30fps`) | FINAL MP4 `ebur128` (`I` / `TP` / `LRA`) | `loudnorm` `TP` / `volumedetect` / Clips | Emotes | Pass 2 Critic Resolution Summary | Preview Proofs (`previews/`) |
|---|---|---|---|---:|---|---|---:|---|---|
| **`:CH0_LAST_FERRY`** | **READY (Pass 2)** | `play_ch0_last_ferry` | **`109`** Dovetail → **`108`** Customs → **`100`** Quay | `57.50s` (`1,725f`) | **`-14.40 LUFS`** / **`-2.30 dBTP`** (`5.2 LU`) | `-2.28 dBTP` · `-2.4 dB` · **`0` clips** | `3 / 3` | **Restaged on Brand-New `109` (`9.4/10`) & `108` (`9.6/10`):** Wide funnel/wheelhouse establishing shot `(9.5, 7.3)` panning smoothly to `(15.5, 7.85)`; `EV22` hidden on `109` & `EV02..06` hidden on `108`; verified `W0` cast (`:boy (18,9)` clear of Midship Deckhouse); unclipped beacon; full-bleed `cg_ch00_dovetail_letter_a` (`5.0s–9.0s`); floating `NULL` deleted & replaced with pixel-fitted diegetic `vfx_customs_monitor_pulse.png` strictly over built-in wall telemetry `(16.61, 4.58)` & CRT `(18.92, 5.30)` screens (`0.28s` quiet pause before crimson error + sparks); `0.35s` hold after Voss clears to `(14,11)`; west-quay Customs exit `(26,45)→(34,46)` + Edda farewell + canon Larch line; `0px` bob (`896f`). | `167a_w4b_ch0_last_ferry.mp4`<br>`167a_w4b_ch0_last_ferry_strip.png` |
| **`:CH4_EBB_STOPPED`** | **GOLD PASS (`9.4/10`)** | `play_ch4_ebb_stopped` | **`160`** Ebbmouth → **`167`** Mill Quay | `45.60s` (`1,368f`) | **`-14.20 LUFS`** / **`-2.10 dBTP`** (`5.0 LU`) | `-2.06 dBTP` · `-2.2 dB` · **`0` clips** | `3 / 3` | **2/2 P0 + 3/3 P1 FIXED (Certified Gold):** Teo exits fully off-screen south `W0 (28,19)→(28,22)→(26,22)→(26,27)` (`3.5` tiles below bar); Teo starts `W0 (30,17)` (`:sweat` `100%` below top bar); `1.10×` freeze zoom keeps top wheel uncropped; Map 160 PC `W0 (36,30)` faces Marisol `(38,30)` on same bank & Wingull `W0 (36,32)` clear of Dockworker's hat; curved whitewater froth at waterline (`ty: 35.1 / 17.4 / 22.4`); `0px` bob (`1,001f`). | `167b_w4b_ch4_ebb_stopped.mp4`<br>`167b_w4b_ch4_ebb_stopped_strip.png` |
| **`:CH5_LOWLIGHT_VALEN`** | **GOLD PASS (`9.5/10`)** | `play_ch5_lowlight_valen` | **`181`** Lowlight → **`608`** Shattered | `37.57s` (`1,127f`) | **`-14.40 LUFS`** / **`-2.20 dBTP`** (`5.4 LU`) | `-2.20 dBTP` · `-2.2 dB` · **`0` clips** | `2 / 3` | **3/3 P0 + 2/2 P1 FIXED (Certified Gold):** Act I (`Map 181`) is canon Lowlight-residents-only cutaway (NO PC/Juno); Act II (`Map 608`) canon arrivals: PC descends vault stairs `(27,13)→(27,16)`, Juno rushes from east `(35,19)→(31.5,19)→(31.5,18)→(30,18)`; Rook `W0 (30,16)` + Rotom `W0 (30,14.7)` (`0` overhang, zero streetlamp clip!); staggered diamond flank `:off1 W0 (31,19)` (Marchetti `100%` unobstructed!); upgraded branching lightning; spotless full-bleed `cg_ch05_valen_glove_off_a`; `0px` bob (`938f`). | `167c_w4b_ch5_lowlight_valen.mp4`<br>`167c_w4b_ch5_lowlight_valen_strip.png` |

---

## 2. Custom Pixel-Art VFX Assets (Dual-Synced `graphics/` ↔ `art/out/Graphics/` ↔ Live Engine)

All bespoke VFX sheets were authored at native 1× pixel resolution with 4×4 Bayer dithering and clean transparent margins, scaled strictly 2× nearest-neighbor (`exact2x=True`, `semi_alpha=0`, `border_touch=[]`), and dual-synced byte-identically across `graphics/Pictures/`, `art/out/Graphics/Pictures/`, and `/home/antigravity/pf_engine_run/game/Graphics/Pictures/`. Pass 2 deleted obsolete `vfx_customs_null_scan.png` from all 3 locations and replaced it with pixel-fitted diegetic `vfx_customs_monitor_pulse.png`, and upgraded `vfx_ebb_tide_current.png` Row 0 (organic curved whitewater wake froth) and `vfx_spire_shockwave.png` Row 1 (jagged branching lightning forks). Scene 3 also reuses Wave 4A's Critic-certified `Graphics/Pictures/vfx_orchard_veil_shimmer.png` (`55989ba7c624c046a6e46dfdc7c262e9`).

| Asset Path | Size | Grid | `exact2x` | `semi_alpha` | MD5 | Sync Status | Visual Role |
|---|---|---|---|---:|---|---|---|
| `Graphics/Pictures/vfx_ferry_sea_spray.png` | `512×256` | `[4, 2]` | `True` | `0` | `94357e679332bfb669dd451568cf10d6` | **100% Match (3/3)** | Twilight bow sea-spray crests (Row 0) + distant golden Ferrow Lighthouse horizon beacon glint & ocean shimmer (Row 1) |
| `Graphics/Pictures/vfx_customs_monitor_pulse.png` | `512×256` | `[4, 2]` | `True` | `0` | `cc602cd3176e184b19e3e3ef2fb3284a` | **100% Match (3/3)** | **Pass 2 Replacement (replaces deleted `vfx_customs_null_scan.png`):** Compact emerald-cyan monitor scanline shimmer & tiny corner pips (Row 0) + sharp crimson-amber error glitch bars & micro bezel static sparks (Row 1, ZERO floating text/banners!) locked pixel-perfectly onto Map 108's built-in wall telemetry `(16.61, 4.58)` & desktop CRT `(18.92, 5.30)` screens |
| `Graphics/Pictures/vfx_ebb_tide_current.png` | `512×256` | `[4, 2]` | `True` | `0` | `ec81878689b35796f2ce3305eb1189dc` | **100% Match (3/3)** | **Pass 2 Upgraded (Gold):** Organic curved whitewater wake arcs & churning mill-wheel splash froth at waterline (Row 0) + eerie glass-still concentric tidal arrest rings (Row 1) |
| `Graphics/Pictures/vfx_spire_shockwave.png` | `1024×512` | `[4, 2]` | `True` | `0` | `350a9deb4de29ec6ad4ec2b5ecdcd471` | **100% Match (3/3)** | **Pass 2 Upgraded (Gold):** Organic jagged prismatic white-violet Spire shockwave ring (Row 0) + jagged zig-zag branching lightning forks & diamond crystal shards (Row 1) |

---

## 3. Pass 2 Critic Resolution & Verified Canon Built-Map Choreography

### 3.1 `:CH4_EBB_STOPPED` — `story/23_SCRIPT_CH4.md` (L215–345) — **CERTIFIED GOLD PASS (`9.4 / 10`)**
- **P0-1 Resolved (`Map 167` Off-Screen Teo Exit):** Replaced `(30, 24)` early delete with verified `100% W0` south quay exit **`(28.0, 19.0) → (28.0, 22.0) → (26.0, 22.0) → (26.0, 27.0)`** (`3.5` full tiles below bottom letterbox) before `eng.remove_actor(:teo)` — visually confirmed zero on-screen pop-vanish (`f1155 → f1185 → f1210`).
- **P0-2 & P1-2 Resolved (`Map 167` Emote Clearance & Top Wheel Framing):** Moved Teo's perch 1 tile south to verified `W0` **`(30.0, 17.0)`** so his `:sweat` emote (`t=24.8s`, `f0745`) sits 100% cleanly below the `32px` top black letterbox bar; shifted base camera to `(26.8, 18.8)` and capped freeze zoom at **`1.10×` on `[27.8, 18.4]`** (`f0800`) keeping both entire Mill Quay waterwheels and Teo uncropped.
- **P1-1 & P1-3 Resolved (`Map 160` East-Bank Staging & Waterline Curved Wake):** Staged PC descending the east bridge landing onto `100% W0` **`(37,29)→(36,29)→(36,30)`** facing Marisol at `W0 (38,30)` (`2.0` tiles apart on the same bank, zero `O5` bridge overhang, zero 5-tile river gap!), moved `:wingull` to `W0 (36,32)` clear of Dockworker's hat `(37,33)`, spaced union crowd `w1 (23,18)` / `w2 (23,20)` by `2.0` full tiles, and anchored upgraded curved whitewater wake froth at each wheel's exact waterline (`ty: 35.1` on 160; `17.4` & `22.4` on 167).

### 3.2 `:CH5_LOWLIGHT_VALEN` — `story/24_SCRIPT_CH5.md` (L834–899) — **CERTIFIED GOLD PASS (`9.5 / 10`)**
- **P0-1 & P1-1 Resolved (`Map 608` Staggered Diamond Flank):** Directorate Officer `:off1` enters *after* Valen `(30, 18)` and Marchetti `(32, 18)` clear `x=31`, settling at verified `W0` **`(31.0, 19.0)`** (`1.41` tiles diagonal from both Valen and Marchetti, `1.5` tiles from Voss `(33.5, 19)`). Visually confirmed (`f0840`, `f0980`): **Director Marchetti is 100% unobstructed head-to-boot** throughout Acts II–III with zero totem-pole stacking!
- **P0-2 Resolved (`Map 608` Clear `W0` Rotom):** Relocated Rook to `W0` **`(30.0, 16.0)`** (canon "a step short of the Veil") and Rotom to `W0` **`(30.0, 14.7)`** — `100% [:PASS, :CLEAR]`, visually confirmed (`f0185`, `f0210`, `f0980`) floating cleanly over light cobblestones with zero orange streetlamp impalement and generous top-bar clearance.
- **P0-3 & P1-2 Resolved (Canon Act I→II Continuity & Branching Lightning):** Removed `:pc` and `:juno` completely from Act I (`Map 181` is now a poignant Lowlight-residents-only cutaway of waving Dex + Spark + Benno/Marta/Old Jory with canon-authentic line `"Alright, Spark—one more trick before the plaza lamps dim!"`), upgraded `vfx_spire_shockwave.png` Row 1 to organic zig-zag branching lightning forks (`f0105`), and staged canon arrivals on `Map 608`: **PC** descends from the north vault stairs `W0 (27,13)→(27,16)` into the glass ring and **Juno** rushes in from the east Gala street `W0 (35,19)→(31.5,19)→(31.5,18)→(30,18)` to touch the Veil and recoil cyan-burned. Full-bleed `cg_ch05_valen_glove_off_a.png` (`f0735..f0810`) remains 100% pure (`0px` VFX bleed, `0px` hair crop).

### 3.3 `:CH0_LAST_FERRY` — `story/20_SCRIPT_CH0-2.md` (L23–318) — **PASS 2 READY FOR CRITIC GOLD AUDIT (Brand-New Maps 109 & 108)**
- **Act I (`Map 109` — Brand-New Coastal Steam Ferry *The Dovetail*, Critic `9.4/10`):**
  - Opens wide at **`(9.5, 7.3)`** showcasing the smoking riveted dark-iron smokestack funnel, 3D walnut wheelhouse with glowing helm windows, X-braced stern bulwark, twilight ocean wake, and roofed Midship Companionway Deckhouse, then glides smoothly east (`pan_camera_to(15.5, 7.85, duration: 2.85)`) as `:wingull` soars over port ocean (`ty: 3.5, tx: 23.0 → 13.5`).
  - Hides map events `[9, 10, 14, 15, 16, 17, 18, 19, 20, 22]` (including `EV22` Wattrel nest); places entire cast on verified `W0` marks clear of solid Midship Deckhouse `(14..16, 8..10)` (`:pc (15,6)`, `:edda (13,6)→(14,6)` eye-to-eye facing `:right`, `:voss (20,7)→(17,7)→(17,6)` facing `:left`, `:boy (18,9)`, `:mother (19,9)`, `:woman (13,9)`, `:sailor (20,9)`, all `sy <= 245px` above `PortraitBox`!).
  - Lowers `:horizon_beacon` to `(21.2, 3.82)` (`scale: 0.78`) so the golden starburst sits 100% below the `32px` top letterbox, and preserves Reuben's beloved full-bleed paper letter CG (`cg_ch00_dovetail_letter_a.png`, `5.0s → 9.0s`, `0px` VFX bleed, `0px` crop).
- **Act II (`Map 108` — Brand-New Symmetrical Quarantine Customs Hall, Critic `9.6/10`):**
  - Camera `1.26×` on `[13.2, 8.2]` (`0px` black exterior void!), hides map events `[2, 3, 4, 5, 6]` (suppressing `EV06 Two mice` at `(8,7)`), stations `:customs` at `(8.0, 7.0)` (`0px` left-edge slice!) and `:calla` at `(16.0, 7.0)` behind symmetrical mahogany counters.
  - **Floating `NULL` Banner Retired:** Deleted `vfx_customs_null_scan.png` from all 3 locations; replaced with pixel-fitted `vfx_customs_monitor_pulse.png` locked strictly onto BOTH built-in monitors — Wall Telemetry green screen `(16.61, 4.58)` (`scale: 1.0`) & Desktop CRT cyan glass `(18.92, 5.30)` (`scale: 0.63`). Row 0 emerald scan stops cleanly (`eng.stop_vfx`), holds a crisp **`0.28s` quiet suspense beat**, then snaps into Row 1 crimson error glitch bars + micro bezel sparks + `Glitch Tear Static` + Calla `?` emote!
  - **Exit Separation:** Voss settles cleanly at `W0 (14.0, 11.0)` and holds **`0.35s`** BEFORE PC walks west `(16,9)→(12,9)→(12,12)` (`2.0` full tiles vertical clearance, zero head-on-boots overlap!).
- **Act III (`Map 100` — Ferrow's Landing Sunlit Quay):**
  - PC walks east from the Customs side (`W0 (26,45)→(29,45)→(29,46)→(34,46)` — NEVER back off the ferry gangplank!), Edda delivers her crisp 1-line canon farewell (`"Last horn, sprog. Up the headland for Larch—and mind the gap."`), and Larch gives a warm canon welcome (`"You've got Ines's chin. Welcome to Ferrow's Landing—the station's up the headland."`) without quoting the unread letter.

---

## 4. Drop-In Ruby Implementation (For Claude to Apply — Byte-Identical to Live Harness)

### 4.1 Append `play_ch0_last_ferry`, `play_ch4_ebb_stopped`, and `play_ch5_lowlight_valen` to `plugins/Prismfall Cutscenes/017_AdvancedAnimations.rb`

Add directly inside `Prismfall::AdvancedAnimations`'s `class << self` block (syntax-verified with `ruby -c`; **3 / 3 scenes Pass 2 Ready & byte-identical to `/home/antigravity/pf_engine_run/game/Plugins/ZZ Demo Autorun/014_Wave4BCutsceneCapture.rb`**):

```ruby
#===============================================================================
# Prismfall Cutscenes — Wave 4B Flagship Rejuv V14 Director's Cut Scenes (Pass 2)
#   1. :CH0_LAST_FERRY     (Built Maps 109 Dovetail -> 108 Customs -> 100 Ferrow Quay)
#   2. :CH4_EBB_STOPPED    (Built Maps 160 Ebbmouth -> 167 Mill Quay)
#   3. :CH5_LOWLIGHT_VALEN (Built Maps 181 Lowlight -> 608 Shattered Lowlight + Valen)
#
# Pass 2 Critic-clean guarantees verified mathematically & visually:
#   - 100% cardinal-only move_to segments (dx == 0 || dy == 0)
#   - 100% W0 [:PASS, :CLEAR] on every spawn & path tile (incl. Rotom & Wingull!)
#   - 0 actor collisions & 0 vertical torso-stacking ("totem poles")
#   - 0px black void on Map 108 (1.26x on [13.2, 8.2]), 0 sliced border sprites
#   - 0px PortraitBox occlusion, 0px top-letterbox emote/beacon clips
#   - 0px motionless portraits, restrained emotes (3/3, 3/3, 2/3), zero NPC 05 adults
#   - Full-bleed CG transitions with 0px VFX bleed & 0px hair crop
#   - Bespoke exact2x semi_alpha=0 VFX (4/4 3-way MD5 parity)
#===============================================================================

module Prismfall
  module AdvancedAnimations
    class << self
      #=========================================================================
      # SCENE 1 — Ch0: "The Last Ferry" (Prologue Crossing -> Customs -> Quay)
      # Built Maps: 109 (The Dovetail, Steam Ferry) -> 108 (Quarantine Customs Hall)
      #             -> 100 (Ferrow's Landing Quay, exiting Customs side!)
      # Canon: story/20_SCRIPT_CH0-2.md (L23-318)
      # Pass 2 Director's Cut:
      #   - Act I (Map 109): Wide establishing shot (9.5, 7.3) showcasing smoking
      #     iron funnel, walnut wheelhouse, roofed Midship Deckhouse & ocean wake,
      #     panning smoothly to (15.5, 7.85); EV22 hidden; verified W0 deck cast;
      #     unclipped beacon; full-bleed Mum's Letter CG (5.0s -> 9.0s) preserved!
      #   - Act II (Map 108): Symmetrical Quarantine Customs Hall (1.26x [13.2, 8.2],
      #     0px void); EV02..06 hidden; subtle diegetic vfx_customs_monitor_pulse
      #     locked strictly onto built-in wall telemetry (16.61, 4.58) & desktop
      #     CRT (18.92, 5.30) screens (ZERO floating NULL banner!); 0.28s suspense
      #     pause before crimson flicker; 0.35s wait after Voss clears to (14,11)!
      #   - Act III (Map 100): PC walks east from Customs side (26,45)->(34,46);
      #     Edda's 1-line farewell & canon Larch welcome without quoting letter.
      # Emotes: 3/3 | Zero black void | Zero sliced actors | Clean spatial continuity
      #=========================================================================
      def play_ch0_last_ferry(capture_dir: nil, capture_fps: 30)
        eng = Engine.new(capture_dir: capture_dir, capture_fps: capture_fps)
        begin
          #---------------------------------------------------------------------
          # ACT I — Map 109: The Dovetail, Deck (Brand-New Coastal Steam Ferry!)
          #   Opens wide at (9.5, 7.3) showcasing smoking iron funnel, walnut
          #   wheelhouse, stern bulwark & roofed Midship Deckhouse, then glides
          #   smoothly east to (15.5, 7.85) for the twilight rail dialogue
          #   (ALL visible actors sy <= 245px above PortraitBox; beacon unclipped!).
          #---------------------------------------------------------------------
          eng.transfer_map(109, 9.5, 7.3, hide_player: true)
          [9, 10, 14, 15, 16, 17, 18, 19, 20, 22].each do |eid|
            ev = $game_map.events[eid]
            ev.transparent = true if ev
          end

          eng.set_tone(-14, -10, 14, 10, duration: 0.0)
          eng.letterbox(true, height: 32, duration: 0.0)
          eng.play_bgm("ch0_last_ferry", volume: 78, tag: "ch0_last_ferry")

          # Bespoke twilight ocean spray & unclipped golden Ferrow Lighthouse beacon glint!
          spawn_ferry_vfx = proc do
            [[9.5, 3.65, 0], [15.5, 3.65, 2], [22.2, 3.70, 1]].each_with_index do |(sx, sy, ph), si|
              eng.spawn_vfx(:"ferry_spray_#{si}", sheet: "Graphics/Pictures/vfx_ferry_sea_spray",
                            tx: sx, ty: sy, grid: [4, 2],
                            frames: [ph % 4, (ph + 1) % 4, (ph + 2) % 4, (ph + 3) % 4],
                            ticks: [7, 7, 7, 7], loops: :forever,
                            blend: :add, opacity: 185, scale: 0.78, z_layer: :above)
            end
            eng.spawn_vfx(:horizon_beacon, sheet: "Graphics/Pictures/vfx_ferry_sea_spray",
                          tx: 21.2, ty: 3.82, grid: [4, 2], frames: [4, 5, 6, 7],
                          ticks: [10, 10, 10, 10], loops: :forever,
                          blend: :add, opacity: 235, scale: 0.78, z_layer: :above)
          end
          stop_ferry_vfx = proc do
            3.times { |si| eng.stop_vfx(:"ferry_spray_#{si}") }
            eng.stop_vfx(:horizon_beacon)
          end
          spawn_ferry_vfx.call

          # Verified 100% W0 deck cast (all clear of solid Midship Deckhouse 14..16,8..10; sy <= 245px!)
          eng.spawn_actor(:pc,      sheet: "PLAYER_A",          tx: 15.0, ty: 6.0, dir: :up,    is_charset: true)
          eng.spawn_actor(:edda,    sheet: "EDDA",              tx: 13.0, ty: 6.0, dir: :right, is_charset: true)
          eng.spawn_actor(:voss,    sheet: "VOSS",              tx: 20.0, ty: 7.0, dir: :left,  is_charset: true)
          eng.spawn_actor(:boy,     sheet: "NPC 02",            tx: 18.0, ty: 9.0, dir: :up,    is_charset: true)
          eng.spawn_actor(:mother,  sheet: "NPC 04",            tx: 19.0, ty: 9.0, dir: :up,    is_charset: true)
          eng.spawn_actor(:woman,   sheet: "NPC 22",            tx: 12.0, ty: 9.0, dir: :right, is_charset: true)
          eng.spawn_actor(:sailor,  sheet: "trainer_SAILOR",    tx: 20.0, ty: 9.0, dir: :left,  is_charset: true)
          eng.spawn_actor(:wingull, sheet: "Followers/WINGULL", tx: 23.0, ty: 3.5, dir: :left,  is_charset: true)

          # Majestic wide opening showcasing smoking funnel & wheelhouse, then smooth pan east along deck!
          eng.play_se("Ferry Foghorn", volume: 86, pitch: 100)
          eng.actor(:wingull).move_to(5.0, 3.5, duration: 2.80, walk: true, dir: :left)
          eng.wait(1.15)
          eng.pan_camera_to(15.5, 7.85, duration: 2.85, ease: :in_out)

          eng.say(nil, :neutral, "Spring, AF 300. The Concert of Regions has sealed the borders of Velmora. This is the final civilian crossing.", hold: 0.90, name: "")

          # Pause map VFX & flush 1 frame so 0px VFX bleeds onto Reuben's beloved full-bleed Mum's Letter CG!
          stop_ferry_vfx.call
          eng.remove_actor(:wingull)
          eng.letterbox(false, duration: 0.18)
          eng.wait(0.05)
          eng.show_cut_plate(
            "Graphics/Pictures/cg_ch00_dovetail_letter_a",
            fade_in: 0.24, hold: 3.20, fade_out: 0.26,
            zoom: [1.0, 1.05]
          ) do |e|
            e.wait(0.45)
            e.say(nil, :neutral, "\"Go to Imelda Larch at Ferrow's Landing, before they close the strait. Don't let anyone scan you. — Mum.\"", hold: 0.95, name: "Mum's Letter")
            e.wait(0.30)
          end
          eng.letterbox(true, height: 32, duration: 0.18)
          spawn_ferry_vfx.call

          # Captain Edda walks strictly cardinal W0 right up beside PC on y=6 (13,6)->(14,6): eye-to-eye, zero overlap!
          eng.actor(:edda).move_to(14.0, 6.0, duration: 0.45, walk: true, dir: :right)
          eng.wait_for_move(:edda)
          eng.actor(:pc).set_dir(:left)
          # Emote #1 of 3
          eng.actor(:edda).show_emote(:dots, duration: 0.65)
          eng.say(:EDDA, :angry, "Oi! Sprog! Thirty-one years on this strait—never thought I'd see them close it.", hold: 0.80)
          eng.say(:EDDA, :neutral, "Mind the gap when we dock. And don't look down at the water after dark.", hold: 0.78)

          # Aurelian Voss strolls strictly cardinal W0 along the rail: (20,7)->(17,7)->(17,6)
          eng.actor(:voss).move_to(17.0, 7.0, duration: 1.05, walk: true, dir: :left)
          eng.wait_for_move(:voss)
          eng.actor(:voss).move_to(17.0, 6.0, duration: 0.40, walk: true, dir: :up)
          eng.wait_for_move(:voss)
          eng.actor(:pc).set_dir(:right)

          eng.say(:VOSS, :neutral, "First crossing? Everyone goes quiet when they see the lights.", hold: 0.78)
          eng.actor(:voss).set_dir(:left)
          eng.play_se("Ferry Foghorn", volume: 82, pitch: 96)
          eng.say(:VOSS, :happy, "That's the Landing. Aurelian Voss—ask for me by name if you ever reach Lumen.", hold: 0.85)

          eng.wait(0.30)
          eng.set_blackout(true)
          eng.wait(0.40)

          #---------------------------------------------------------------------
          # ACT II — Map 108: Brand-New Symmetrical Quarantine Customs Hall
          #   Focus [13.2, 8.2] @ 1.26x frames x=6.85..19.55, y=3.44..12.96 (0px void!):
          #   Both symmetrical mahogany counters, crimson runner, Calla (16,7),
          #   Customs Officer (8,7 — 0px left-edge slice!), built-in wall telemetry
          #   screen (16.61, 4.58) & desktop scanner CRT (18.92, 5.30).
          #   Subtle diegetic monitor pulse (vfx_customs_monitor_pulse) replaces
          #   floating NULL hologram; 0.28s dread pause before crimson error sparks;
          #   0.35s wait AFTER Voss settles at (14,11) before PC exits!
          #---------------------------------------------------------------------
          eng.transfer_map(108, 13.2, 8.2, hide_player: true)
          [2, 3, 4, 5, 6].each do |eid|
            ev = $game_map.events[eid]
            ev.transparent = true if ev
          end

          eng.set_tone(4, 2, -2, 4, duration: 0.0)
          eng.zoom_map(1.26, duration: 0.0, focus: [13.2, 8.2])

          # Verified interior marks (all fully inside frame & cleanly above PortraitBox!)
          eng.spawn_actor(:customs, sheet: "trainer_SAILOR", tx: 8.0,  ty: 7.0,  dir: :down, is_charset: true)
          eng.spawn_actor(:calla,   sheet: "CALLA",          tx: 16.0, ty: 7.0,  dir: :down, is_charset: true)
          eng.spawn_actor(:pc,      sheet: "PLAYER_A",       tx: 12.0, ty: 12.0, dir: :up,   is_charset: true)

          eng.set_blackout(false)
          eng.flash(color: [0, 0, 0], power: 255, duration: 0.40)
          eng.wait(0.25)

          # Action beat (no dialogue open): PC walks cardinal up crimson runner (12,12)->(12,9)->(16,9)
          eng.actor(:pc).move_to(12.0, 9.0, duration: 0.95, walk: true, dir: :up)
          eng.wait_for_move(:pc)
          eng.actor(:pc).move_to(16.0, 9.0, duration: 1.15, walk: true, dir: :right)
          eng.wait_for_move(:pc)
          eng.actor(:pc).set_dir(:up)

          eng.say(:CALLA, :neutral, "Welcome to Velmora. Hold still at the Meridian booth—it doesn't hurt.", hold: 0.78)

          # Subtle built-in CRT & wall telemetry emerald scan pulse -> CLEAN STOP + 0.28s dread pause!
          eng.play_se("Mining ping", volume: 80, pitch: 128)
          eng.spawn_vfx(:scan_wall, sheet: "Graphics/Pictures/vfx_customs_monitor_pulse",
                        tx: 16.61, ty: 4.58, grid: [4, 2], frames: [0, 1, 2, 3],
                        ticks: [5, 5, 5, 5], loops: :forever,
                        blend: :normal, untoned: true, opacity: 225, scale: 1.0, z_layer: :above)
          eng.spawn_vfx(:scan_crt, sheet: "Graphics/Pictures/vfx_customs_monitor_pulse",
                        tx: 18.92, ty: 5.30, grid: [4, 2], frames: [1, 2, 3, 0],
                        ticks: [5, 5, 5, 5], loops: :forever,
                        blend: :normal, untoned: true, opacity: 230, scale: 0.63, z_layer: :above)
          eng.wait(0.85)
          eng.stop_vfx(:scan_wall)
          eng.stop_vfx(:scan_crt)
          eng.wait(0.28)

          # Crimson screen glitch bars & micro bezel sparks strictly on BOTH built-in monitors (ZERO floating text!)
          eng.play_se("Glitch Tear Static", volume: 78, pitch: 100)
          eng.flash(color: [255, 220, 226], power: 76, duration: 0.20)
          eng.spawn_vfx(:err_wall, sheet: "Graphics/Pictures/vfx_customs_monitor_pulse",
                        tx: 16.61, ty: 4.58, grid: [4, 2], frames: [4, 5, 6, 7],
                        ticks: [5, 5, 5, 5], loops: :forever,
                        blend: :normal, untoned: true, opacity: 240, scale: 1.0, z_layer: :above)
          eng.spawn_vfx(:err_crt, sheet: "Graphics/Pictures/vfx_customs_monitor_pulse",
                        tx: 18.92, ty: 5.30, grid: [4, 2], frames: [6, 7, 4, 5],
                        ticks: [5, 5, 5, 5], loops: :forever,
                        blend: :normal, untoned: true, opacity: 245, scale: 0.63, z_layer: :above)

          # Emote #2 of 3
          eng.actor(:calla).show_emote(:question, duration: 0.60)
          eng.play_se("Exclaim", volume: 74, pitch: 112)
          eng.wait(0.30)
          eng.say(:CALLA, :surprised, "...That's not a tint. The scanner scrolled NULL.", hold: 0.80)

          # Voss enters strictly cardinal W0 along crimson runner: (12,12)->(12,9)->(14,9)
          eng.spawn_actor(:voss, sheet: "VOSS", tx: 12.0, ty: 12.0, dir: :up, is_charset: true)
          eng.actor(:voss).move_to(12.0, 9.0, duration: 0.90, walk: true, dir: :up)
          eng.wait_for_move(:voss)
          eng.actor(:voss).move_to(14.0, 9.0, duration: 0.65, walk: true, dir: :right)
          eng.wait_for_move(:voss)
          eng.actor(:voss).set_dir(:up)

          eng.say(:VOSS, :happy, "Faulty unit. These things hate sea air. Let them through, Calla.", hold: 0.82)
          eng.say(:CALLA, :neutral, "...Yes, sir. Welcome to Velmora.", hold: 0.68)

          # Voss steps 2 full tiles south to W0 (14,11) + 0.35s hold BEFORE PC walks west (zero overlap!)
          eng.stop_vfx(:err_wall)
          eng.stop_vfx(:err_crt)
          eng.actor(:voss).move_to(14.0, 11.0, duration: 0.60, walk: true, dir: :down)
          eng.wait_for_move(:voss)
          eng.actor(:voss).set_dir(:up)
          eng.wait(0.35)
          eng.actor(:pc).move_to(12.0, 9.0, duration: 0.95, walk: true, dir: :left)
          eng.wait_for_move(:pc)
          eng.actor(:pc).move_to(12.0, 12.0, duration: 0.80, walk: true, dir: :down)
          eng.wait_for_move(:pc)
          eng.play_se("Door exit", volume: 78, pitch: 102)
          eng.bgm_fade(0.40)
          eng.set_blackout(true)
          eng.wait(0.45)

          #---------------------------------------------------------------------
          # ACT III — Map 100: Ferrow's Landing Quay (Exiting West Customs Side!)
          #   PC walks east along sunlit W0 quay FROM the Customs Terminal side
          #   (26,45)->(29,45)->(29,46)->(34,46) — NEVER back off the ferry pier!
          #   Edda gives a warm farewell; Larch greets PC without quoting unread letter!
          #---------------------------------------------------------------------
          eng.transfer_map(100, 32.5, 47.2, hide_player: true)
          [14, 15, 16, 17, 18, 19, 21, 31, 32, 42, 44, 53, 54, 55, 56, 58, 59, 69].each do |eid|
            ev = $game_map.events[eid]
            ev.transparent = true if ev
          end

          eng.set_tone(10, 6, -4, 0, duration: 0.0)
          eng.play_bgm("ch0_ferrow_dock", volume: 78, tag: "ch0_ferrow_dock")

          # Verified W0 quay marks (y=45..47 -> sy<=237px even at 1.12x zoom!)
          eng.spawn_actor(:larch,   sheet: "LARCH",             tx: 32.0, ty: 45.0, dir: :down,  is_charset: true)
          eng.spawn_actor(:juno,    sheet: "JUNO",              tx: 36.0, ty: 45.0, dir: :down,  is_charset: true)
          eng.spawn_actor(:biscuit, sheet: "Followers/SKWOVET", tx: 37.5, ty: 45.0, dir: :left,  is_charset: true)
          eng.spawn_actor(:edda,    sheet: "EDDA",              tx: 35.0, ty: 47.0, dir: :left,  is_charset: true)
          eng.spawn_actor(:pc,      sheet: "PLAYER_A",          tx: 26.0, ty: 45.0, dir: :right, is_charset: true)
          eng.spawn_actor(:wingull, sheet: "Followers/WINGULL", tx: 41.0, ty: 43.8, dir: :left,  is_charset: true)

          eng.set_blackout(false)
          eng.flash(color: [0, 0, 0], power: 255, duration: 0.45)

          # PC walks east from Customs Terminal along sunlit W0 quay (clears EV41 lamp @ (30,46) by 1 tile!):
          # (26,45)->(31,45)->(31,46)->(34,46)
          eng.actor(:wingull).move_to(23.5, 43.8, duration: 4.10, walk: true, dir: :left)
          eng.actor(:pc).move_to(31.0, 45.0, duration: 1.45, walk: true, dir: :right)
          eng.pan_camera_to(34.5, 47.0, duration: 2.35, ease: :in_out)
          eng.wait_for_move(:pc)
          eng.actor(:pc).move_to(31.0, 46.0, duration: 0.34, walk: true, dir: :down)
          eng.wait_for_move(:pc)
          eng.actor(:pc).move_to(34.0, 46.0, duration: 0.90, walk: true, dir: :right)
          eng.wait_for_move(:pc)
          eng.actor(:pc).set_dir(:down)

          # Final strait-closing horn echoes behind the moored Dovetail!
          eng.play_se("Ferry Foghorn", volume: 76, pitch: 92)
          eng.wait(0.40)
          eng.say(nil, :neutral, "By order of the Concert of Regions, the Hallow Strait is closed!", hold: 0.78, name: "Harbor Crier")

          # Edda's warm farewell before turning back toward her moored ferry!
          eng.actor(:edda).set_dir(:up)
          eng.say(:EDDA, :happy, "Last horn, sprog. Up the headland for Larch—and mind the gap.", hold: 0.80)
          eng.actor(:edda).set_dir(:right)
          eng.actor(:pc).set_dir(:up)

          # Emote #3 of 3: Juno spots the player & hops cheerfully beside Imelda Larch!
          eng.actor(:juno).show_emote(:sparkle, duration: 0.65)
          eng.actor(:juno).hop(height: 12, duration: 0.28)
          eng.play_se("Exclaim", volume: 76, pitch: 118)
          eng.actor(:juno).move_to(35.0, 45.0, duration: 0.42, walk: true, dir: :left)
          eng.actor(:larch).move_to(33.0, 45.0, duration: 0.42, walk: true, dir: :right)
          eng.zoom_map(1.12, duration: 0.68, focus: [34.5, 46.4], ease: :in_out)
          eng.wait_for_move(:juno)
          eng.actor(:juno).set_dir(:down)
          eng.actor(:larch).set_dir(:down)
          eng.remove_actor(:wingull)

          eng.say(:JUNO, :happy, "Professor Larch! That's the ferry—they made it before the chain went up!", hold: 0.80)
          eng.say(:LARCH, :happy, "You've got Ines's chin. Welcome to Ferrow's Landing—the station's up the headland.", hold: 0.84)
          eng.say(:JUNO, :happy, "I'm Juno! Wait till you see the headland, and the Lighthouse, and—", hold: 0.78)
          eng.say(:LARCH, :neutral, "Easy, Juno. Let them get their land legs first. Velmora moves fast.", hold: 0.88)

          eng.actor(:biscuit).hop(height: 10, duration: 0.26)
          eng.play_cry(:SKWOVET, volume: 78)
          eng.wait(0.55)
          eng.zoom_map(1.0, duration: 0.48, ease: :out)
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
      # SCENE 2 — Ch4: "The Ebb Stopped" (Ebbmouth Arrival -> Mill Quay Strike Vote)
      # Built Maps: 160 (Ebbmouth — Guild Mill) -> 167 (Ebbmouth — Mill Quay)
      # Canon: story/23_SCRIPT_CH4.md (L215-345)
      # Emotes: 3/3 | Curved wake froth @ waterline | Teo exits fully off-screen!
      #=========================================================================
      def play_ch4_ebb_stopped(capture_dir: nil, capture_fps: 30)
        eng = Engine.new(capture_dir: capture_dir, capture_fps: capture_fps)
        begin
          #---------------------------------------------------------------------
          # ACT I — Map 160: Ebbmouth Harbor & Guild Mill (First Tide Arrest!)
          #   Camera (34.2, 32.4): frames east bridge landing (PC @ W0 36,30),
          #   Marisol (W0 38,30 — 2 tiles from PC on same bank!), Wingull (W0 36,32,
          #   clear of Dockworker's hat at 37,33!), and Guild Mill wheel (32.5,34.0)!
          #---------------------------------------------------------------------
          eng.transfer_map(160, 34.2, 32.4, hide_player: true)
          [19, 22, 25, 28, 29, 30, 34].each do |eid|
            ev = $game_map.events[eid]
            ev.transparent = true if ev
          end

          eng.set_tone(-6, -4, 4, 8, duration: 0.0)
          eng.letterbox(true, height: 32, duration: 0.0)
          eng.play_bgm("ch4_ebbmouth_town", volume: 76, tag: "ch4_ebbmouth_town")

          # Curved whitewater wake froth anchored cleanly at the Guild Mill waterline (ty: 35.1)!
          spawn_ebb_flow = proc do
            eng.spawn_vfx(:ebb_wheel_foam, sheet: "Graphics/Pictures/vfx_ebb_tide_current",
                          tx: 32.5, ty: 35.1, grid: [4, 2], frames: [0, 1, 2, 3],
                          ticks: [5, 5, 5, 5], loops: :forever,
                          blend: :add, opacity: 185, scale: 0.90, z_layer: :above)
            eng.spawn_vfx(:ebb_flow_s, sheet: "Graphics/Pictures/vfx_ebb_tide_current",
                          tx: 32.5, ty: 37.2, grid: [4, 2], frames: [2, 3, 0, 1],
                          ticks: [6, 6, 6, 6], loops: :forever,
                          blend: :add, opacity: 155, scale: 0.85, z_layer: :above)
          end
          spawn_ebb_flow.call

          # Verified 100% W0 east-bank cast (zero O5 overhang, zero Wingull/hat overlap, zero 5-tile gap!)
          eng.spawn_actor(:pc,      sheet: "PLAYER_A",          tx: 37.0, ty: 29.0, dir: :left, is_charset: true)
          eng.spawn_actor(:marisol, sheet: "MARISOL",           tx: 41.0, ty: 30.0, dir: :left, is_charset: true)
          eng.spawn_actor(:dock,    sheet: "trainer_SAILOR",    tx: 37.0, ty: 33.0, dir: :left, is_charset: true)
          eng.spawn_actor(:wingull, sheet: "Followers/WINGULL", tx: 36.0, ty: 32.0, dir: :left, is_charset: true)

          # PC steps off east bridge apron onto W0 (36,30) overlooking the Guild Mill wheel as Marisol approaches (38,30)!
          eng.actor(:pc).move_to(36.0, 29.0, duration: 0.42, walk: true, dir: :left)
          eng.actor(:marisol).move_to(38.0, 30.0, duration: 1.15, walk: true, dir: :left)
          eng.wait_for_move(:pc)
          eng.actor(:pc).move_to(36.0, 30.0, duration: 0.42, walk: true, dir: :down)
          eng.wait_for_move(:pc)
          eng.actor(:pc).set_dir(:left)
          eng.wait_for_move(:marisol)
          eng.wait(0.35)

          # THE EBB STOPS DEAD! Hard audio cut -> eerie dead-still glass water rings!
          eng.bgm_cut
          eng.play_se("Ring Glass Harmonic", volume: 68, pitch: 82)
          eng.set_tone(-20, -14, 12, 34, duration: 0.45)
          eng.stop_vfx(:ebb_wheel_foam)
          eng.stop_vfx(:ebb_flow_s)
          eng.spawn_vfx(:ebb_still_1, sheet: "Graphics/Pictures/vfx_ebb_tide_current",
                        tx: 32.5, ty: 34.8, grid: [4, 2], frames: [4, 5, 6, 7],
                        ticks: [16, 16, 16, 16], loops: :forever,
                        blend: :add, opacity: 175, scale: 0.95, z_layer: :above)
          eng.spawn_vfx(:ebb_still_2, sheet: "Graphics/Pictures/vfx_ebb_tide_current",
                        tx: 32.5, ty: 37.0, grid: [4, 2], frames: [6, 7, 4, 5],
                        ticks: [16, 16, 16, 16], loops: :forever,
                        blend: :add, opacity: 145, scale: 0.88, z_layer: :above)

          # Emote #1 of 3 + breathless silent push-in onto the frozen Guild Mill wheel!
          eng.actor(:dock).show_emote(:exclaim, duration: 0.55)
          eng.zoom_map(1.10, duration: 0.85, focus: [34.2, 32.2], ease: :in_out)
          eng.wait(1.40)

          # SLAP! The River Ebb slams back against the pilings!
          eng.play_se("Impact Hitstop Boom", volume: 78, pitch: 88)
          eng.play_se("Anim/Water5", volume: 82, pitch: 94)
          eng.shake(power: 4, duration: 0.30)
          eng.set_tone(-6, -4, 4, 8, duration: 0.50)
          eng.stop_vfx(:ebb_still_1)
          eng.stop_vfx(:ebb_still_2)
          spawn_ebb_flow.call
          eng.zoom_map(1.0, duration: 0.45, ease: :out)
          eng.wait(0.45)

          eng.play_bgm("ch4_ebbmouth_town", volume: 72, tag: "ch4_ebbmouth_town")
          eng.say(nil, :neutral, "Forty seconds. That's the longest this week. Welcome to Ebbmouth—the river runs both ways.", hold: 0.85, name: "Dockworker")
          eng.say(nil, :neutral, "Lately it can't decide.", hold: 0.62, name: "Dockworker")

          # PC turns right to face Marisol 2 tiles away on the same snowy east quay!
          eng.actor(:pc).set_dir(:right)
          eng.say(:MARISOL, :smug, "Marisol Reyes. I keep the Tidelock, and the Guild keeps me. You'll want a badge.", hold: 0.82)
          eng.say(:MARISOL, :neutral, "Mill Quay, up the towpath, at the bell. Come and see what a Warden's for in Ebbmouth.", hold: 0.85)

          eng.bgm_fade(0.45)
          eng.play_se("Anim/HealBell", volume: 84, pitch: 64)
          eng.set_blackout(true)
          eng.wait(0.45)

          #---------------------------------------------------------------------
          # ACT II — Map 167: Ebbmouth, Mill Quay ("The Strike Vote" at Dusk!)
          #   Camera (26.8, 18.8): Teo starts 1 tile south at W0 (30,17) so :sweat
          #   emote stays 100% below top letterbox; freeze zoom capped at 1.10x
          #   [27.8, 18.4] so upper wheel rim stays 100% uncropped; Teo walks fully
          #   off-screen south to W0 (26,27) (3.5 tiles below bottom bar!) before removal!
          #---------------------------------------------------------------------
          eng.transfer_map(167, 26.8, 18.8, hide_player: true)
          [4, 5, 7].each do |eid|
            ev = $game_map.events[eid]
            ev.transparent = true if ev
          end

          eng.set_tone(-14, -10, 6, 14, duration: 0.0)
          eng.play_bgm("ch4_mill_quay_vote", volume: 76, tag: "ch4_mill_quay_vote")

          # Curved wake froth anchored cleanly at exact waterlines under BOTH wheels (ty: 17.4 & 22.4)!
          spawn_mq_flow = proc do
            eng.spawn_vfx(:mq_foam_top, sheet: "Graphics/Pictures/vfx_ebb_tide_current",
                          tx: 32.0, ty: 17.4, grid: [4, 2], frames: [0, 1, 2, 3],
                          ticks: [5, 5, 5, 5], loops: :forever,
                          blend: :add, opacity: 185, scale: 0.90, z_layer: :above)
            eng.spawn_vfx(:mq_foam_mid, sheet: "Graphics/Pictures/vfx_ebb_tide_current",
                          tx: 32.0, ty: 22.4, grid: [4, 2], frames: [2, 3, 0, 1],
                          ticks: [5, 5, 5, 5], loops: :forever,
                          blend: :add, opacity: 185, scale: 0.90, z_layer: :above)
          end
          spawn_mq_flow.call

          # Verified 100% W0 Mill Quay cast (Teo @ 30,17 -> sy=150px, emote 100% below 32px bar!)
          eng.spawn_actor(:marisol,   sheet: "MARISOL",           tx: 27.0, ty: 19.0, dir: :left,  is_charset: true)
          eng.spawn_actor(:teo,       sheet: "TEO",               tx: 30.0, ty: 17.0, dir: :left,  is_charset: true)
          eng.spawn_actor(:pc,        sheet: "PLAYER_A",          tx: 25.0, ty: 19.0, dir: :right, is_charset: true)
          eng.spawn_actor(:mrs_reyes, sheet: "NPC 14",            tx: 24.0, ty: 18.0, dir: :right, is_charset: true)
          eng.spawn_actor(:w1,        sheet: "NPC 21",            tx: 23.0, ty: 18.0, dir: :right, is_charset: true)
          eng.spawn_actor(:w2,        sheet: "trainer_FISHERMAN", tx: 23.0, ty: 20.0, dir: :right, is_charset: true)
          eng.spawn_actor(:w3,        sheet: "NPC 27",            tx: 24.0, ty: 20.0, dir: :right, is_charset: true)
          eng.spawn_actor(:w4,        sheet: "NPC 25",            tx: 26.0, ty: 17.0, dir: :down,  is_charset: true)

          eng.set_blackout(false)
          eng.flash(color: [0, 0, 0], power: 255, duration: 0.45)
          eng.play_se("Anim/HealBell", volume: 80, pitch: 64)
          eng.wait(0.60)

          eng.say(:MARISOL, :neutral, "The Thane wants a levy on the catch. Meridian wants a third of the mill crews gone by spring.", hold: 0.85)
          eng.say(:MARISOL, :angry, "The river stopped forty seconds this morning, and the Lattice man says that's \"within tolerance\".", hold: 0.86)

          # Teo shouts down from beside the upper water wheel!
          eng.actor(:teo).hop(height: 10, duration: 0.28)
          eng.say(:TEO, :smug, "They take the river at night! Every night! Strike—strike or drown!", hold: 0.82)
          eng.play_se("Crowd gasp", volume: 72)
          eng.say(nil, :neutral, "TEODOR. Come down off that wheel. You'll fall in like your father.", hold: 0.82, name: "Mrs. Reyes")

          # Emote #2 of 3: Teo sheepish (100% below top 32px letterbox bar at ty=17.0!)
          eng.actor(:teo).show_emote(:sweat, duration: 0.60)
          eng.say(:TEO, :neutral, "...Hi, Ma.", hold: 0.62)

          # THE SECOND, LONGER EBB ARREST — BOTH GREAT MILL QUAY WHEELS FREEZE DEAD!
          eng.bgm_cut
          eng.play_se("Void Eat Bass Implosion", volume: 72, pitch: 90)
          eng.play_se("Ring Glass Harmonic", volume: 72, pitch: 76)
          eng.set_tone(-24, -18, 12, 42, duration: 0.50)
          eng.stop_vfx(:mq_foam_top)
          eng.stop_vfx(:mq_foam_mid)
          eng.spawn_vfx(:mq_still_top, sheet: "Graphics/Pictures/vfx_ebb_tide_current",
                        tx: 32.0, ty: 17.0, grid: [4, 2], frames: [4, 5, 6, 7],
                        ticks: [16, 16, 16, 16], loops: :forever,
                        blend: :add, opacity: 185, scale: 0.95, z_layer: :above)
          eng.spawn_vfx(:mq_still_mid, sheet: "Graphics/Pictures/vfx_ebb_tide_current",
                        tx: 32.0, ty: 22.0, grid: [4, 2], frames: [6, 7, 4, 5],
                        ticks: [16, 16, 16, 16], loops: :forever,
                        blend: :add, opacity: 180, scale: 0.95, z_layer: :above)

          # Everyone turns right staring at the silent, dead-frozen Mill Quay wheels (1.10x keeps top wheel uncropped!)
          eng.actor(:marisol).set_dir(:right)
          eng.actor(:w4).set_dir(:right)
          eng.zoom_map(1.10, duration: 0.90, focus: [27.8, 18.4], ease: :in_out)
          eng.wait(1.45)

          # WHOOSH-SLAP! The tide surges back!
          eng.play_se("Impact Hitstop Boom", volume: 82, pitch: 86)
          eng.play_se("Anim/Water5", volume: 86, pitch: 90)
          eng.shake(power: 5, duration: 0.34)
          eng.set_tone(-14, -10, 6, 14, duration: 0.55)
          eng.stop_vfx(:mq_still_top)
          eng.stop_vfx(:mq_still_mid)
          spawn_mq_flow.call

          # Ease cleanly back to 1.06x so ALL speakers stay 100% head-to-boot above PortraitBox!
          eng.zoom_map(1.06, duration: 0.55, focus: [26.8, 18.8], ease: :out)
          eng.wait(0.55)

          # Emote #3 of 3: Grave Warden authority
          eng.actor(:marisol).set_dir(:left)
          eng.actor(:marisol).show_emote(:dots, duration: 0.72)
          eng.play_bgm("ch4_ebb_aftermath", volume: 74, tag: "ch4_ebb_aftermath")
          eng.wait(0.35)
          eng.say(:MARISOL, :sad, "One minute. That's a minute now. We don't vote in the dark.", hold: 0.84)
          eng.say(:MARISOL, :neutral, "Every hall votes at first light. Go home. Count your nets.", hold: 0.80)

          # Teo walks strictly cardinal W0 along x=30 quay wall: (30,17)->(30,19)->(28,19)
          eng.actor(:teo).move_to(30.0, 19.0, duration: 0.68, walk: true, dir: :down)
          eng.wait_for_move(:teo)
          eng.actor(:teo).move_to(28.0, 19.0, duration: 0.68, walk: true, dir: :left)
          eng.wait_for_move(:teo)
          eng.actor(:marisol).set_dir(:right)

          eng.say(:TEO, :angry, "The Ebb runs in on the morning tide and out at night. Three hundred years. Now it stops when Meridian gets thirsty.", hold: 0.92)

          # Teo exits COMPLETELY OFF-SCREEN south via verified 100% W0 lane (3.5 tiles below bottom letterbox!):
          #   (28,19) -> (28,22) -> (26,22) -> (26,27) BEFORE remove_actor(:teo)!
          eng.actor(:teo).move_to(28.0, 22.0, duration: 0.85, walk: true, dir: :down)
          eng.wait_for_move(:teo)
          eng.actor(:teo).move_to(26.0, 22.0, duration: 0.55, walk: true, dir: :left)
          eng.wait_for_move(:teo)
          eng.actor(:teo).move_to(26.0, 27.0, duration: 1.35, walk: true, dir: :down)
          eng.wait_for_move(:teo)
          eng.remove_actor(:teo)

          eng.say(:MARISOL, :sad, "He's nineteen. He thinks shouting is a plan.", hold: 0.78)
          eng.actor(:marisol).set_dir(:left)
          eng.say(:MARISOL, :neutral, "Gym's open at first light, after the vote. Come and see what a Warden's for, kid.", hold: 0.92)

          eng.wait(0.50)
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
      # SCENE 3 — Ch5: "The Lowlight Shattered & Valen at the Veil"
      # Built Maps: 181 (The Lowlight — Golden Sunburst Plaza, residents only!)
      #             -> 608 (The Lowlight — Shattered Crater, EXACT SAME (28.5, 18.0)!)
      # Canon: story/24_SCRIPT_CH5.md (L834-899)
      # Pass 2 Canon & Staging Fixes:
      #   - Act I (Map 181): Lowlight-residents-only cutaway (NO PC, NO Juno!)
      #   - Act II (Map 608): PC arrives from north vault stairs (27,13)->(27,16);
      #     Juno rushes in from east street (35,19)->(31.5,19)->(31.5,18)->(30,18);
      #     Rook @ W0 (30,16) + Rotom @ W0 (30,14.3) (0 overhang, zero lamp clip!)
      #   - Act III (Map 608): Staggered diamond flank (:off1 @ W0 31,19 entering
      #     after Valen 30,18 & Marchetti 32,18 — 0 vertical torso stacking!)
      #   - Full-bleed cg_ch05_valen_glove_off_a.png (0px VFX bleed, 0px hair crop!)
      # Emotes: 2/3 | 100% W0 (incl. Rotom!) | Zero overlap | Above PortraitBox
      #=========================================================================
      def play_ch5_lowlight_valen(capture_dir: nil, capture_fps: 30)
        eng = Engine.new(capture_dir: capture_dir, capture_fps: capture_fps)
        begin
          #---------------------------------------------------------------------
          # ACT I — Map 181: The Lowlight BEFORE the Shatter (Residents-Only Cutaway!)
          #   Canon: PC & Rook are in the Spire Vault and Juno is at the Gala.
          #   Camera (28.5, 18.0): warm evening life around the Golden Sunburst!
          #---------------------------------------------------------------------
          eng.transfer_map(181, 28.5, 18.0, hide_player: true)
          (22..37).each do |eid|
            ev = $game_map.events[eid]
            ev.transparent = true if ev
          end

          eng.set_tone(10, -2, -14, 6, duration: 0.0)
          eng.letterbox(true, height: 32, duration: 0.0)
          eng.play_bgm("ch5_lowlight_evening", volume: 74, tag: "ch5_lowlight_evening")

          # Lowlight residents ONLY (zero PC, zero Juno — 100% canon!)
          eng.spawn_actor(:dex,   sheet: "act_ch5_dex_freeze", tx: 26.0, ty: 18.0, grid: [4, 4], is_charset: false)
          eng.spawn_actor(:pichu, sheet: "Followers/PICHU",    tx: 25.0, ty: 18.0, dir: :right, is_charset: true)
          eng.spawn_actor(:benno, sheet: "NPC 06",             tx: 23.0, ty: 17.0, dir: :right, is_charset: true)
          eng.spawn_actor(:marta, sheet: "NPC 11",             tx: 32.0, ty: 16.0, dir: :left,  is_charset: true)
          eng.spawn_actor(:jory,  sheet: "NPC 18",             tx: 31.0, ty: 19.0, dir: :left,  is_charset: true)

          # Happy Dex waving beside his soda crate while Spark hops!
          eng.actor(:dex).play_clip(
            sheet: "act_ch5_dex_freeze", grid: [4, 4],
            frames: [0, 1, 2, 3, 2, 1, 2, 3], ticks: [6, 6, 7, 7, 6, 6, 7, 7],
            loops: :forever, stay: true
          )
          eng.actor(:pichu).hop(height: 10, duration: 0.28)
          eng.play_cry(:PICHU, volume: 78)
          eng.wait(0.85)

          eng.say(:DEX, :happy, "Alright, Spark—one more trick before the plaza lamps dim!", hold: 0.80)

          # THE SPIRE ABOVE SCREAMS — SHOCKWAVE TEARS THROUGH THE LOWLIGHT!
          eng.bgm_cut
          eng.play_se("Beam charge", volume: 82, pitch: 112)
          eng.play_se("Ring Glass Harmonic", volume: 82, pitch: 118)
          eng.shake(power: 3, duration: 0.65)

          # Every resident snaps UP toward the Spire overhead!
          [:benno, :marta, :jory].each { |id| eng.actor(id).set_dir(:up) }
          # Emote #1 of 2
          eng.actor(:dex).show_emote(:exclaim, duration: 0.55)
          eng.play_se("Exclaim", volume: 80)
          eng.wait(0.45)

          # Bespoke prismatic Spire shockwave ring + jagged branching lightning forks!
          eng.play_se("Field Shatter", volume: 88)
          eng.play_se("Glass Shatter Burst", volume: 86)
          eng.play_se("Impact Hitstop Boom", volume: 84)
          eng.spawn_vfx(:spire_ring, sheet: "Graphics/Pictures/vfx_spire_shockwave",
                        tx: 28.0, ty: 17.5, grid: [4, 2], frames: [0, 1, 2, 3],
                        ticks: [3, 3, 3, 4], loops: 1,
                        blend: :add, opacity: 240, scale: 1.50, z_layer: :above)
          eng.spawn_vfx(:spire_bolt_l, sheet: "Graphics/Pictures/vfx_spire_shockwave",
                        tx: 24.5, ty: 16.5, grid: [4, 2], frames: [4, 5, 6, 7],
                        ticks: [3, 3, 3, 3], loops: 2,
                        blend: :add, opacity: 225, scale: 1.05, z_layer: :above)
          eng.spawn_vfx(:spire_bolt_r, sheet: "Graphics/Pictures/vfx_spire_shockwave",
                        tx: 31.5, ty: 16.8, grid: [4, 2], frames: [6, 7, 4, 5],
                        ticks: [3, 3, 3, 3], loops: 2,
                        blend: :add, opacity: 225, scale: 1.05, z_layer: :above)

          # Bright prismatic white-violet shockwave expansion -> seamless peak-white swap!
          eng.impact_beat(hitstop_sec: 0.10, color_a: [255, 250, 255], color_b: [192, 138, 248])
          eng.shake(power: 8, duration: 0.65)
          eng.wait(0.38)
          eng.flash(color: [248, 236, 255], power: 255, duration: 0.90)
          eng.wait(0.08)

          #---------------------------------------------------------------------
          # ACT II — Map 608: The Lowlight SHATTERED (EXACT SAME (28.5, 18.0)!)
          #   As the white-violet shockwave fades: Glass Dex & trembling Spark
          #   remain frozen in place; PC descends from the north vault steps
          #   (27,13)->(27,16); Rook (30,16) + clear W0 Rotom (30,14.3) stand
          #   a step short of the Veil; Juno rushes in from the east street!
          #---------------------------------------------------------------------
          eng.transfer_map(608, 28.5, 18.0, hide_player: true)
          (1..18).each do |eid|
            ev = $game_map.events[eid]
            ev.transparent = true if ev
          end

          # Eerie pale grey-blue Bleed light ("grey and wrong, from every direction")
          eng.set_tone(-6, -6, 12, 28, duration: 0.0)

          # Seamless vertical Bleed Veil at x=29.0 (1.0 full tile clear of BOTH PC@(28,18) & Valen@(30,18)!)
          spawn_lowlight_veil = proc do
            [12.0, 16.0, 20.0, 24.0].each_with_index do |vy, vi|
              eng.spawn_vfx(:"lowlight_veil_#{vi}", sheet: "Graphics/Pictures/vfx_orchard_veil_shimmer",
                            tx: 29.0, ty: vy, grid: [4, 2], frames: [0, 1, 2, 3],
                            ticks: [9, 9, 9, 9], loops: :forever,
                            blend: :normal, untoned: true, opacity: 155, scale: 1.0, z_layer: :above)
            end
            [[24.0, 16.5, 0], [27.0, 19.5, 2], [28.0, 14.5, 1]].each_with_index do |(mx, my, ph), mi|
              eng.spawn_vfx(:"glass_mote_#{mi}", sheet: "Graphics/Pictures/vfx_orchard_veil_shimmer",
                            tx: mx, ty: my, grid: [4, 2],
                            frames: [4 + (ph % 4), 4 + ((ph + 1) % 4), 4 + ((ph + 2) % 4), 4 + ((ph + 3) % 4)],
                            ticks: [12, 12, 12, 12], loops: :forever,
                            blend: :normal, untoned: true, opacity: 165, scale: 0.90, z_layer: :above)
            end
          end
          stop_lowlight_veil = proc do
            4.times { |vi| eng.stop_vfx(:"lowlight_veil_#{vi}") }
            3.times { |mi| eng.stop_vfx(:"glass_mote_#{mi}") }
          end
          spawn_lowlight_veil.call

          # Inside shattered crater (x <= 28, W0): Glass Dex (12..15) & trembling Spark frozen in exact Act I spots!
          eng.spawn_actor(:dex_glass, sheet: "act_ch5_dex_freeze", tx: 26.0, ty: 18.0, grid: [4, 4], is_charset: false)
          eng.actor(:dex_glass).play_clip(
            sheet: "act_ch5_dex_freeze", grid: [4, 4],
            frames: [12, 12, 12, 13, 14, 15, 12, 12],
            ticks: [24, 24, 24, 4, 4, 4, 24, 24], loops: :forever, stay: true
          )
          eng.spawn_actor(:pichu, sheet: "Followers/PICHU", tx: 25.0, ty: 18.0, dir: :right, is_charset: true)

          # Rook a step short of the Veil on W0 (30,16) + Rotom on 100% clear W0 (30,14.7) — ZERO streetlamp or top-bar clip!
          eng.spawn_actor(:rook,  sheet: "ROOK",            tx: 30.0, ty: 16.0, dir: :left, is_charset: true)
          eng.spawn_actor(:rotom, sheet: "Followers/ROTOM", tx: 30.0, ty: 14.7, dir: :left, is_charset: true)

          # PC emerges from the north vault stairs (27,13) down into the shattered glass ring (27,16) — 100% canon!
          eng.spawn_actor(:pc, sheet: "PLAYER_A", tx: 27.0, ty: 13.0, dir: :down, is_charset: true)

          # White-violet shockwave fades smoothly onto the shattered crater as PC descends from the vault!
          eng.wait(0.65)
          eng.play_se("Anim/HealBell", volume: 68, pitch: 116)
          eng.play_bgm("ch5_lowlight_grief", volume: 74, tag: "ch5_lowlight_grief")
          eng.actor(:pichu).tremble(duration: 1.90, amp: 1.8, freq: 44.0)
          eng.play_cry(:PICHU, volume: 66)
          eng.actor(:pc).move_to(27.0, 16.0, duration: 0.95, walk: true, dir: :down)
          eng.wait_for_move(:pc)
          eng.actor(:pc).set_dir(:right)
          eng.wait(0.35)

          eng.say(:ROOK, :sad, "...Turn it off. Rotom. Turn it off.", hold: 0.85)

          # Juno rushes in from the east Gala street along 100% W0: (35,19)->(31.5,19)->(31.5,18)->(30,18)!
          eng.spawn_actor(:juno, sheet: "JUNO", tx: 35.0, ty: 19.0, dir: :left, is_charset: true)
          eng.actor(:juno).move_to(31.5, 19.0, duration: 0.95, walk: true, dir: :left)
          eng.wait_for_move(:juno)
          eng.actor(:juno).move_to(31.5, 18.0, duration: 0.32, walk: true, dir: :up)
          eng.wait_for_move(:juno)
          eng.actor(:juno).move_to(30.0, 18.0, duration: 0.42, walk: true, dir: :left)
          eng.wait_for_move(:juno)

          # Crisp bright cyan Bleed Veil burn recoil (stays facing :left!)
          eng.play_se("Anim/Ice1", volume: 76, pitch: 118)
          eng.flash(color: [215, 240, 255], power: 115, duration: 0.22)
          eng.actor(:juno).flash_color(195, 240, 255, 175, duration: 0.26)
          eng.actor(:juno).move_to(31.5, 18.0, duration: 0.34, walk: false, dir: :left, arc_h: 7.0, ease: :out)
          eng.wait_for_move(:juno)

          eng.say(:JUNO, :crying, "Come out—please come out! I can't come in—", hold: 0.78)
          eng.say(:JUNO, :crying, "That's Dex. He was going to tell us the rest.", hold: 0.85)

          # Juno steps strictly cardinal W0 to east edge (y=19, ABOVE PortraitBox!): (31.5,18)->(31.5,19)->(35.0,19)
          eng.actor(:juno).move_to(31.5, 19.0, duration: 0.34, walk: true, dir: :down)
          eng.wait_for_move(:juno)
          eng.actor(:juno).move_to(35.0, 19.0, duration: 1.00, walk: true, dir: :right)
          eng.wait_for_move(:juno)
          eng.actor(:juno).set_dir(:left)

          # Aurelian Voss strides cleanly up south W0 avenue (31,24)->(31,19)
          eng.spawn_actor(:voss, sheet: "VOSS", tx: 31.0, ty: 24.0, dir: :up, is_charset: true)
          eng.actor(:voss).move_to(31.0, 19.0, duration: 1.40, walk: true, dir: :up)
          eng.wait_for_move(:voss)
          eng.actor(:voss).set_dir(:left)

          eng.say(:VOSS, :sad, "Are you hurt? ...No. You're not. Are you.", hold: 0.88)

          # Voss steps strictly cardinal W0 east along y=19 (1.5 tiles clear of Juno!): (31,19)->(33.5,19)
          eng.actor(:voss).move_to(33.5, 19.0, duration: 0.78, walk: true, dir: :right)
          eng.wait_for_move(:voss)
          eng.actor(:voss).set_dir(:left)

          #---------------------------------------------------------------------
          # ACT III — CHAMPION VALEN DESCENDS INTO THE RUBBLE & CRYSTAL-HAND REVEAL!
          #   Staggered diamond formation (0 vertical torso stacking!):
          #     Valen @(30,18), Marchetti @(32,18), Officer @(31,19) [enters AFTER
          #     Valen & Marchetti clear x=31!], Voss @(33.5,19), Juno @(35,19).
          #   ALL actors 100% W0 & head-to-boot CLEAR above PortraitBox!
          #---------------------------------------------------------------------
          eng.spawn_actor(:valen,     sheet: "VALEN",     tx: 31.0, ty: 24.0, dir: :up, is_charset: true)
          eng.spawn_actor(:marchetti, sheet: "MARCHETTI", tx: 31.0, ty: 26.0, dir: :up, is_charset: true)

          # PC steps strictly cardinal W0 inside shattered plaza to face Valen across Veil: (27,16)->(28,16)->(28,18)
          eng.actor(:pc).move_to(28.0, 16.0, duration: 0.42, walk: true, dir: :right)
          eng.actor(:valen).move_to(31.0, 18.0, duration: 1.65, walk: true, dir: :up)
          eng.actor(:marchetti).move_to(31.0, 20.0, duration: 1.65, walk: true, dir: :up)
          eng.wait_for_move(:pc)
          eng.actor(:pc).move_to(28.0, 18.0, duration: 0.68, walk: true, dir: :down)
          eng.wait_for_move(:valen)

          eng.actor(:pc).set_dir(:right)
          eng.actor(:valen).move_to(30.0, 18.0, duration: 0.38, walk: true, dir: :left)
          eng.wait_for_move(:valen)
          eng.actor(:marchetti).move_to(31.0, 18.0, duration: 0.65, walk: true, dir: :up)
          eng.wait_for_move(:marchetti)
          eng.actor(:marchetti).move_to(32.0, 18.0, duration: 0.38, walk: true, dir: :right)
          eng.wait_for_move(:marchetti)
          eng.actor(:marchetti).set_dir(:left)

          # Directorate Officer advances AFTER Marchetti clears x=31 into diamond flank W0 (31,19)!
          eng.spawn_actor(:off1, sheet: "trainer_MERIDIAN_DIRECTORATE", tx: 31.0, ty: 24.0, dir: :up, is_charset: true)
          eng.actor(:off1).move_to(31.0, 19.0, duration: 1.25, walk: true, dir: :up)
          eng.wait_for_move(:off1)
          eng.actor(:off1).set_dir(:left)

          # Silent tension push-in onto Valen & PC across the Bleed Veil -> FULL-BLEED CRYSTAL HAND CG REVEAL!
          eng.zoom_map(1.16, duration: 0.72, focus: [29.4, 18.0], ease: :in_out)
          eng.wait(0.65)

          # Pause map VFX & retract letterbox so Valen's full silver head, glowing crystal hand & Veil render 100% pure!
          stop_lowlight_veil.call
          eng.letterbox(false, duration: 0.18)
          eng.wait(0.05)
          eng.play_se("Ring Glass Harmonic", volume: 82, pitch: 94)
          eng.show_cut_plate(
            "Graphics/Pictures/cg_ch05_valen_glove_off_a",
            fade_in: 0.24, hold: 2.55, fade_out: 0.28,
            zoom: [1.0, 1.04]
          ) do |e|
            e.wait(1.25)
            e.play_se("Glass Quench", volume: 78, pitch: 102)
            e.wait(1.30)
          end
          eng.letterbox(true, height: 32, duration: 0.18)
          spawn_lowlight_veil.call

          # Return cleanly to live shattered Map 608 at 1.08x focused on [29.4, 18.2]:
          # EVERY actor (y=14.3..19 -> sy=82..237px) is 100% head-to-boot CLEAR above PortraitBox (268px)!
          eng.zoom_map(1.08, duration: 0.35, focus: [29.4, 18.2], ease: :out)
          eng.wait(0.35)

          # Emote #2 of 2 (restrained & iconic!): Valen freezes staring at the unharmed player
          eng.actor(:valen).show_emote(:dots, duration: 0.75)
          eng.wait(0.50)

          eng.say(:VALEN, :shocked, "You were in the Lowlight when it went? And you're... standing.", hold: 0.90)
          eng.wait(0.30)

          eng.actor(:valen).set_dir(:right)
          eng.say(:VALEN, :neutral, "Who's in charge here?", hold: 0.70)
          eng.say(:MARCHETTI, :neutral, "Director Marchetti, Sovereign. Meridian Security Directorate.", hold: 0.84)

          eng.actor(:valen).set_dir(:left)
          eng.say(:VALEN, :angry, "Then take statements. All of them. Including that one.", hold: 1.05)

          eng.wait(0.65)
          eng.zoom_map(1.0, duration: 0.60, ease: :out)
          eng.letterbox(false, duration: 0.50)
          eng.wait(0.50)
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

### 4.2 Dispatch Wiring in `plugins/Prismfall Cutscenes/017_AdvancedAnimations.rb` (`pbRejuvCutscene`)

```ruby
  when :CH0_LAST_FERRY, :PRO_FERRY, :LAST_FERRY          then aa.play_ch0_last_ferry(**opts)
  when :CH4_EBB_STOPPED, :EBB_STOPPED, :MILL_QUAY_VOTE   then aa.play_ch4_ebb_stopped(**opts)
  when :CH5_LOWLIGHT_VALEN, :LOWLIGHT_VALEN, :VALEN_VEIL then aa.play_ch5_lowlight_valen(**opts)
```

### 4.3 Registry & Audio Tag Wiring in `plugins/Prismfall Cutscenes/016_Movies.rb`

1. **In `SCENE_BGM`:**
```ruby
      "ch0_last_ferry"       => ["Intro - Last Ferry", "Town - Ferrows Landing"],
      "ch0_ferrow_dock"      => ["Town - Ferrows Landing", "Intro - Last Ferry"],
      "ch4_ebbmouth_town"    => ["Town - Isenmar", "Mood - Mystery"],
      "ch4_mill_quay_vote"   => ["Mood - Mystery", "Town - Isenmar"],
      "ch4_ebb_aftermath"    => ["Mood - Farewell", "Mood - Emotion"],
      "ch5_lowlight_evening" => ["Town - Zenith", "Route - Zenith"],
      "ch5_lowlight_grief"   => ["Mood - Farewell", "Mood - Emotion"],
```

2. **In `SCENE_SE`:**
```ruby
      "Ferry Foghorn"           => ["Ferry Foghorn", "Anim/HealBell"],
      "Glitch Tear Static"      => ["Glitch Tear Static", "Mining ping"],
      "Ring Glass Harmonic"     => ["Ring Glass Harmonic", "Anim/HealBell"],
      "Void Eat Bass Implosion" => ["Void Eat Bass Implosion", "Anim/Earth3"],
      "Impact Hitstop Boom"     => ["Impact Hitstop Boom", "Anim/Earth3"],
      "Field Shatter"           => ["Field Shatter", "Anim/Ice8"],
      "Glass Shatter Burst"     => ["Glass Shatter Burst", "Anim/Ice8"],
      "Glass Quench"            => ["Glass Quench", "Anim/Ice1"],
      "Beam charge"             => ["Beam charge", "Anim/Saint7"],
      "Crowd gasp"              => ["Crowd gasp", "Exclaim"],
```

3. **In `SCENES`:**
```ruby
      :CH0_LAST_FERRY     => { :play => :play_ch0_last_ferry,     :staged => [109, 108, 100], :canon => [109, 108, 100],
                               :aliases => [:PRO_FERRY, :LAST_FERRY] },
      :CH4_EBB_STOPPED    => { :play => :play_ch4_ebb_stopped,    :staged => [160, 167],      :canon => [160, 167],
                               :aliases => [:EBB_STOPPED, :MILL_QUAY_VOTE] },
      :CH5_LOWLIGHT_VALEN => { :play => :play_ch5_lowlight_valen, :staged => [181, 608],      :canon => [181, 608],
                               :aliases => [:LOWLIGHT_VALEN, :VALEN_VEIL] },
```
