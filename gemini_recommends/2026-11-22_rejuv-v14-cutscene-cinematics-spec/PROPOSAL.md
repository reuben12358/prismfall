# Proposal: Authentic Pokémon Rejuvenation V14–Grade Animated Cutscenes & `Prismfall Cutscenes` v2 Blueprint

- **Date:** 2026-11-23 *(Ground-Up Rewrite v2 — Replaces the Scrapped Ken-Burns / Battleback Slideshow Spec & Scrapped HTML Canvas Mockup)*
- **Author:** Gemini (Cutscene Craft Researcher & Cinematics Director)
- **Status:** Ready for Creator Sign-Off & Claude Engine Sprint — zero edits made to `.rb`, `mapgen/`, `pbs/`, or `story/`
- **Benchmark Standard:** Pokémon Rejuvenation V14 (specifically **Maria/Melia impaling Vitus** in Ch16/Renegade, **Kaina vs. Melia**, **Xenpurgis**, **Renegade M2 / Zenos End of Night**, **Aelita / Rift**), Reborn E19 (**Zygarde**), Sea of Stars, Eastward, CrossCode, Chained Echoes, Deltarune, Omori, and Pokémon Black 2 / White 2.

---

> ### Honest Post-Mortem on v1 (Why We Burned It Down)
> Our first pass (`PROPOSAL.md` v1 and the scrapped `prismfall_cutscene_director.html` Canvas mockup) completely missed what makes animated 2D RPG cutscenes unforgettable. Pasting static front-facing battle sprites onto battlebacks, wiggling them with tweens, or zooming 1-frame still illustrations with Ken Burns slides looks cheap, lifeless, and amateurish — **nothing** like Rejuvenation V14.
>
> **Permanent Project Laws Adopted From This Point Forward:**
> 1. **ZERO battlebacks as cutscene stages.** Every map scene plays on the **real tileset map** the player is standing on (`on_map: true`).
> 2. **ZERO front-facing battle sprites slid across scenes.** Characters and Legendaries on maps use **custom per-scene overworld acting sheets** drawn in 3/4 overworld scale and perspective.
> 3. **ZERO static-picture slideshows pretending to be animation.** Full-screen cut-ins are **true frame-by-frame animated sequences** (12–24 fps `anim_cg_sequence` or native MKXP-Z `.ogv` movies) with changing camera angles, facial expressions, hair/cloak physics, weapon arcs, smear frames, and impact frames.
> 4. **ZERO fake HTML Canvas previews.** Every future cutscene review reel is recorded **directly inside our real `mkxp-z` game engine** via `plugins/Prismfall Cutscenes/tools/engine_capture/capture.sh`.

---

## Part 1 — Hard Rule #1: What Makes an Animated Pixel-RPG Cutscene Real vs. Garbage

### 1.1 The Anti-Pattern vs. Authentic Rejuvenation V14 Craft

| Dimension | ❌ The Failed Anti-Pattern (BANNED) | ✅ Authentic Rejuvenation V14 Two-Pillar Craft |
|---|---|---|
| **Stage** | Battleback image or procedural code-drawn background detached from gameplay | **Pillar 1:** The **live RPG Maker XP tileset map** the player just walked onto (`on_map: true`), with real tile collisions, ambient props, and post-scene map state transforms (`181 → 608`, `309`, `926`) |
| **Character Acting** | Static 4-direction walk cycles sliding across tiles, or pasted 160×160 battle sprites hopping/rotating | **Bespoke per-scene overworld acting flipbooks** (`Graphics/Characters/act_<scene>_<actor>.png`, 16–64 custom pixel frames drawn for ONE dramatic action: lunging, conjuring/drawing a blade, impaling, staggering, dropping to knees, unmasking, cloak billowing) |
| **Legendaries** | Front-facing battle sprites scaled 2× onto a side stage (perspective & scale mismatch) | **Overworld-scale 3/4-perspective acting sheets** (like Reborn's `pkmn_zygarde5.png` `138×90` cells & Prismfall's `pfw_kyogre_rise.png`) matching the map's pixel density and palette |
| **Full-Screen Cut-Ins** | 1 static illustration panned slowly with Ken Burns zoom | **Pillar 2: True frame-by-frame animated sakuga** — either native MKXP-Z `Graphics.play_movie("Movies/pf_<scene>.ogv")` (`512×384` @ 24/30fps) OR rapid RGSS `anim_cg_sequence` (`12–24fps` multi-frame pixel/anime plates with pose changes, smear frames, expression snaps, and hair/cloth motion) |
| **Timing & Weight** | Uniform linear tweens (`duration: 0.5`) with every frame held equally | **Variable `frameData` timing** (Rejuvenation `AdvancedAnimations.rb` — e.g. `[30, 8, 4, 2, 2, 4, 24]` ticks): **long anticipation hold → 1–2f smear → impact freeze/hitstop → slow shuddering recovery** |
| **VFX & Lighting** | Thick code-drawn outlines over bright flat backgrounds | **Darkened map screen tone first** (`[-70, -75, -55, 60]`), then **sparse, thin, 4-color additive VFX cells** (`blend_type = 1`) instanced along motion arcs + ramped screen flashes (`17 → 51 → 136 → 221 → 255`) + directional lighting/fog overlays |
| **Audio Direction** | Continuous BGM playing loudly under generic explosion SFX | **Dead-silence vacuum drops** (`bgm_cut` to 0ms silence for `0.25–0.45s` right before a blade pierces, a mask splits, or a Plate shatters), followed by ONE razor-sharp dry SE + long quiet aftermath hold |
| **Review Proof** | Fake HTML5 Canvas slideshow | **100% real `mkxp-z` in-game footage** captured directly off the actual engine + map + Ruby plugin |

---

### 1.2 Forensic Research Findings: How Rejuvenation V14 & Elite Pixel RPGs Actually Do It

#### A. Pokémon Rejuvenation V14 & Reborn E19 (Verified from Engine Data in `design/CUTSCENE_RESEARCH.md` + V14 Analysis)
Forensic inspection of Rejuvenation V14's actual maps and scripts reveals there is **no fake separate slideshow engine**. Rejuvenation V14 delivers cinema-grade moments (`99,856` Move Routes, `69,240` Waits, `31,130` Screen Tones, `19,533` Show Animations, `2,871` Flashes, `2,461` Shakes, `3,243` Map Scrolls) by fusing **two pillars seamlessly**:

1. **Pillar 1 — Live-Map Event Choreography + Custom Acting Sheets (`Scripts/Camera/` + `Scripts/AdvancedAnimations.rb`):**
   - **Camera lives on the map:** The player becomes transparent or locked while `Scripts/Camera/` drives `pbCameraToEvent(id, speed)`, `pbCameraScrollTo`, `pbCameraShake(power)`, and **`pbZoomMap(goal, speed)`** (which grabs `Graphics.snap_to_bitmap` every frame and scales that single sprite smoothly with lerp + `ease_in_out` so tile layers and autotiles never tear or desync!).
   - **Per-scene hand-drawn acting flipbooks:** Instead of stiff walk cycles, Rejuvenation swaps characters into dedicated charset-grid acting sheets (`Arc_Renegade_Anim`, `DimensionalAelita_1/_2`, `DimensionPortal_5`, `MC_Cella3_Crying`, `FriendBlast`) driven by **`AdvancedAnimations.rb`** with per-frame `frameData` holds (e.g., `[30, 8, 4, 8, 4]` — a 1.5s coiled anticipation hold followed by rapid 0.1–0.2s strike frames!). Reborn does the same for Legendaries (`pkmn_zygarde5.png`: `552×360`, 4×4 cells of `138×90` in 3/4 overworld perspective, stepped at 1/20s per frame with staggered additive `PRAS- Core Enforcer` bursts and ramped flashes).
   - **Why *Maria/Melia impales Vitus* (Ch16 "Who should deal with Vitus" / Renegade) and *Kaina vs. Melia* hit so hard:**
     - **Setup on the real map:** Tension builds directly in the room you just fought in — tightened camera framing (`pbZoomMap`), darkened tone isolating the two figures, small tense overworld step-ins and head-turns.
     - **The audio vacuum:** Music cuts dead. A beat of breathless stillness before the blade moves.
     - **Custom acting frames + visceral impact:** The strike is NOT a generic hop — it has bespoke coiled wind-up frames, a blistering 2-frame dash/lunge smear, a stark high-contrast impact beat (flash/silhouette + tiny crisp camera jolt + dry stab/pierce SE), and **custom impaled / staggering / collapsing overworld poses** held on the real map so the shock lands with physical weight!
     - **Emotional brutality in the aftermath:** In Renegade (e.g., M2's crowbar scene, Zenos casting *End of Night*, and the Vitus executions), the engine refuses to rush past the aftermath — lingering in dead silence on the changed map and characters' stunned stillness, and sometimes keeping the player trapped in micro-control during horror beats so the dread feels personal.
2. **Pillar 2 — True Full-Screen Frame-by-Frame Animated Cut-Ins & `.ogv` Movies:**
   - When an action demands cinematic angles impossible from a 3/4 top-down camera (a blade driving through a chest in profile, a face shattering in close-up, the **Xenpurgis** tower descending over Grand Dream City, **End of Night** erasing a victim), Rejuvenation V14 breaks into **full-screen `512×384` / `1024×768` animated plates** or native MKXP-Z **`Movies/*.ogv`** video clips — then drops the player straight back onto the visibly scarred live map!

#### B. Cross-Game Technical Craft Matrix (6 Gold-Standard 2D Pixel RPGs)

| Reference Game | Signature Cutscene Technique | Exact Lesson Adopted for Prismfall |
|---|---|---|
| **Sea of Stars** *(Sabotage Studio)* | Bespoke custom overworld pixel animation frames for every story gesture (bracing, crouching, reaching, panting), real-time dynamic map lighting darkening surroundings so magical rim-light pops, subtle camera zoom/framing, and rare hand-animated full-screen key-art cut-ins | **Keep 85% of drama ON the live map** using bespoke acting sheets + lighting contrast (`tone` dim + additive lantern/rim overlays) so the 15% full-screen animated sakuga bursts hit like lightning |
| **Eastward** *(Pixpil)* & **CrossCode** *(Radical Fish)* | Rich custom per-event overworld poses (weapon draws, recoil staggers, comic double-takes) paired with rapid expressive dialogue portraits; snappy event pacing. *(Cautionary critique of Eastward: players hated slow unskippable camera pans while waiting for NPCs to walk across maps.)* | **Never drag slow walk-ins or empty camera pans.** Cut briskly between beats (`cut` / fast `map_pan`), pack acting personality into bespoke pose frames, and pair live-map acting with `014_Portraits.rb` face swaps |
| **Chained Echoes** *(Matthias Linda)* | Rapid parallel cross-cutting across live maps (cutting between war fronts/factions), bespoke kneeling/sword/collapse sprite rows, moody scene-specific color grading, and respectful skip/fast-forward controls | Use brisk multi-map cross-cuts for Prismfall's **Ch5 Lowlight**, **Ch11 War Declaration**, and **Ch21 11-Lamp Ally Montage**; keep every scene cleanly skippable after first viewing |
| **Deltarune** *(Toby Fox)* | Hyper-economical 1-scene custom sprite sheets (Roaring Knight slash, Kris/Susie clashes), dead-silence audio drops right before shock beats, abrupt anime/high-detail style shifts when reality breaks, and playable micro-moments of dread | Reserve **1-scene custom acting sheets** for every chapter's peak turn; cut BGM to total zero before impact; in Ruin Route (`R1`/`R4`/`R7`), pair cutscenes with eerie trapped-input micro-beats (like `GO_STAY_OUT`'s locked cursor) |
| **Omori** *(OMOCAT, RPG Maker MV)* | Built in RPG Maker! Proves the exact technical ceiling via **`setPictureAnimation` full-screen frame-by-frame sprite sheets** (`640×480` → our `512×384`), boiling hand-drawn line loops, strict pixel-scale consistency, and **disciplined restraint** (saving full-screen animated sequences for ~8–12 devastating emotional peaks so each feels sacred) | Adopt Omori's exact packed-sheet / sequential-frame **`anim_cg_sequence`** architecture directly in RGSS for crisp 2–5s sakuga cut-ins with zero video-codec blur, while reserving full `.ogv` movies for our 5 Peak Climaxes |
| **Pokémon Black 2 / White 2** *(Game Freak)* | Seamless transition from live 2D/2.5D tile overworld → **full-screen animated cut-in/FMV** (Plasma Frigate freezing Opelucid City, Kyurem vs. Reshiram/Zekrom fusion & Glaciate in Giant Chasm, N's Castle rising) → immediate return onto the **visibly transformed live map** (Opelucid encased in ice!) | Mirror B2W2's exact **Live Map → Full-Screen Animated Sequence → Visibly Transformed Live Map** bridge on Ch5 (`181 → 608` Glassed Lowlight), Ch9 (`264` broken mask + glass floor), Ch11 (`309` Sinking Quarter), Ch19 (`926` permanent steam-glass dunes), and Ch21/R7 (`491 → 963`) |

---

### 1.3 The 5 Laws of Sakuga Pixel Timing & Audio Direction

Every Prismfall animated beat — whether an on-map `act_play` sheet or a full-screen `.ogv` / `anim_cg_sequence` — MUST obey this five-part rhythm:

1. **Law 1 — Coil the Spring (Anticipation Hold: `0.30–0.60s`):** Hold the coiled pose (hand hovering over Splitter, Mourner's crouched launch, Reflection's fingers gripping glass-shard, Kyogre's dark eye closed under ice) for 18–36 frames while `map_zoom` tightens (`1.0 → 1.35`). The player's gut must tighten *before* the strike happens.
2. **Law 2 — Pull the Air Out (Audio Vacuum Drop: `0.25–0.45s`):** Call `bgm_cut` (instant zero-tail silence, NOT a soft 1.5s fade!) right at the end of anticipation. Let one tiny dry cue sound in the vacuum — a Splitter *click*, a glove leather *creak*, a sharp intake of breath.
3. **Law 3 — Break the Silhouette (Smear + Impact Frame: `0.04–0.08s`):** Never animate a violent strike cleanly at steady speed. Use **1–2 stretched pixel smear frames** (`0.04s` each) bridging distance instantaneously, followed by **1–2 stark high-contrast impact frames** (pure black ink silhouette on stark white, or single-accent inverted flash).
4. **Law 4 — Lock the Blow (Real-Clock Hitstop: `0.10–0.18s`):** Freeze world time (`hitstop(0.14)`) on the exact frame the blade pierces, the mask fractures, or the Plate shatters. Fire the dry, heavy SE (`Field Shatter`, branch-snap, crystal pierce) and crisp directional `shake` (`4–8 px`) on frame 0 of the hitstop.
5. **Law 5 — Let the Wound Breathe (Silent Aftermath Hold: `1.0–2.5s`):** After recoil/collapse, **DO NOT immediately restart upbeat music or pop a busy dialogue box.** Hold on the transformed live map in near-silence (wind BGS, a single distant glass chime, falling ash or snow, two halves of an ash-bark mask sliding across glass tiles) for at least `1.5–2.5s` (`WAIT 30–50` in Rejuvenation ticks).

> **Photosensitive Accessibility Law (`Prismfall::Cutscene.photosensitive?`):**
> Following Rejuvenation V14 & Reborn (`$Settings.photosensitive`) and W3C WCAG 2.3.1 (≤3 flashes/sec): whenever `photosensitive?` is true, **zero** full-screen B&W strobe frames fire (degraded to a single calm dark-vignette hold at `opacity <= 55`), screen flashes cap at `25%` power with zero hold, shake scales to `20%`, and `play_movie` loads `Movies/pf_<scene>_safe.ogv` (clamped inter-frame luminance delta ≤ 15%) or degrades cleanly to the safe `anim_cg_sequence` fallback — while preserving 100% of the acting frames, hitstop timing, and audio silence!

---

## Part 2 — Exact Engine Spec for Claude (`Prismfall Cutscenes` v2 + `mkxp-z` Native Video & Live-Map Acting)

All additions preserve 100% backwards compatibility with existing `plugins/Prismfall Cutscenes/001..015`, `:WAR_CLIMAX`, Festival Highlights (`011_Highlights.rb`), Portraits (`014_Portraits.rb`), and `selftest/suite.ruby_stub`. Every sprite coordinate and `src_rect` stays strict `Integer` (`selftest/harness.ruby_stub`).

### 2.0 P0 Engine Fixes (Mandatory Day-1 Sprint Foundation)

1. **`slowmo(0.0)` Real-Clock `hitstop` Deadlock Fix (`006_Scene.rb`, `012_Cinematic.rb`, `selftest/suite.ruby_stub`):**
   - **Root Cause Verified:** `Scene#update(dt)` (`006_Scene.rb:201–217`) scales `dt *= @timescale` before `@time += dt`, and `op_slowmo` (`012_Cinematic.rb:544–550`) checks `lt >= @d` where `lt = @time - e.t0`. Passing `scale = 0.0` freezes `@time` forever (permanent deadlock), and `selftest/suite.ruby_stub:52` divides by `e.args[:scale]`, raising `ZeroDivisionError`/`Infinity`.
   - **Fix:** Capture `raw_dt = dt` and accumulate `@real_time += raw_dt` before `dt *= @timescale`; expose `attr_reader :raw_dt, :real_time`. Allow effects implementing `def real_clock?; true; end` to tick on `raw_dt`. Replace anonymous `op_slowmo` with `class SlowmoEffect < Effect` (defaults `real: true` when `scale <= 0.001`, restores `@timescale = 1.0` in `Scene#dispose`). Add `Builder#hitstop(duration = 0.14, **o)` and guard `suite.ruby_stub:52` with a regression test verifying `hitstop(0.14)` completes cleanly in `~0.14s` wall clock.
2. **Dead-Silence Audio Drop (`bgm_cut` / `bgs_cut`) & BGS Restore Symmetry (`003_DSL.rb`, `006_Scene.rb`, `001_Config.rb`):**
   - Add `bgm_cut` and `bgs_cut` (`Audio.bgm_stop` / `Audio.bgs_stop` with zero fade tail — essential for Rejuvenation V14 impact vacuums!).
   - Mirror `@memo_bgm` with `@memo_bgs` (`$game_system.bgs_memorize` / `bgs_restore`) in `006_Scene.rb:192–194,740–743`.
   - Add v4.3 CC0 audio cue aliases to `AUDIO` in `001_Config.rb`: `:field_shatter`, `:boss_shield`, `:glass_quench`, `:prism_swell`, `:vs_lightning`, `:blade_pierce`, `:mask_crack`, `:bell_break`, `:bgs_bleed`, `:bgs_harbor`, `:bgs_isenmar`, `:bgs_machinery`, `:bgs_drip`.
3. **Letterbox Safe-Zone for Captions (`006_Scene.rb:698`, `010_Text.rb:66–70`):**
   - Expose `attr_reader :bar` on `Scene` and offset bottom/top `Caption` by `scene.bar.round + 6` so speaker lines never clip into widescreen bars (`36–44px`).

---

### 2.1 Pillar 1 Engine Primitives — Live-Map Camera, Custom Overworld Acting & Lighting (`012_Map_Camera.rb` & `012_Map_Acting.rb`)

Replaces battleback staging permanently with **true Rejuvenation V14 on-map direction**:

#### A. Live-Map Camera Zoom, Pan & Focus (`012_Map_Camera.rb` — Rejuvenation `Scripts/Camera/pbZoomMap` Architecture)
Because RPG Maker XP's `Tilemap` does not natively zoom cleanly without tearing autotiles and z-sorted events, Rejuvenation V14's `Scripts/Camera/pbZoomMap` captures the live rendered map frame via `Graphics.snap_to_bitmap` and scales that single unified sprite smoothly around the focal event (`design/CUTSCENE_RESEARCH.md:48–55`). We implement this cleanly both inside `Prismfall::Cutscene` (`on_map: true`) AND as standalone overworld script calls for normal RMXP events:

```ruby
# Inside any `on_map: true` cutscene DSL:
map_zoom to: 1.45, focus: :event_mourner, duration: 0.55, ease: :in_out   # live map zoom onto any event or :player or [sx, sy]
map_pan  to: :event_juno, duration: 0.45, ease: :out_cubic                # smooth focus glide while zoomed (or map scroll)
map_shake power: 5, duration: 0.35, decay: true                           # crisp directional impact shake
map_zoom to: 1.0, duration: 0.40, ease: :out                              # seamless return to 1:1 live tilemap!

# Standalone overworld event calls (usable in ANY map event without even opening a full cutscene!):
pbZoomMap(1.35, focus: 12, duration: 0.45)       # event 12, :player, or "Mourner"
pbCameraToEvent(12, speed: 0.15)                 # frame-rate independent lerp follow
pbResetMapZoom(duration: 0.35)
```

**Implementation Contract:**
- While `map_zoom > 1.001`, a dedicated `MapZoomLayer` (at `VIEWPORT_Z - 2`) hides itself for 1 micro-step, calls `Graphics.snap_to_bitmap` of the live updating `Spriteset_Map` (keeping map animations, moving NPCs, water autotiles, and custom acting sheets 100% live!), blits into a single reused `Bitmap` (zero per-frame allocation leak!), sets integer `ox`/`oy` on the focal point, and draws scaled cleanly with nearest-neighbor crispness (optional smooth float zoom during rapid push-ins).
- When `map_zoom` returns to `1.0`, `MapZoomLayer` disposes its snapshot and hands directly back to native `Spriteset_Map` with zero seam.
- Under `Cutscene.photosensitive?`, `map_shake` drops to 20% and abrupt zoom snaps clamp to smooth `>= 0.35s` eases.

#### B. `AdvancedAnimations`-Style Overworld Acting Sheets (`act_play` / `pf_act_event` in `012_Map_Acting.rb`)
Rejuvenation V14's `Scripts/AdvancedAnimations.rb` lets any event on the live map play an arbitrary-grid hand-drawn acting sheet with variable per-frame anticipation/smear/impact `holds`. We wire this directly into our DSL **and** into standard RMXP map events:

```ruby
# 1. Inside an `on_map: true` cutscene:
act_play :mourner,
         swap_event: "Mourner",                           # hides live RMXP event on frame 0, locks to its exact tile [screen_x, screen_y]!
         sheet:      "Graphics/Characters/act_ch9_mourner_dive",
         grid:       [6, 4],                              # arbitrary grid: 4x4 (16f), 6x4 (24f), 8x4 (32f), 8x8 (64f)
         frames:     0..23,
         # Variable holds (seconds, or use `ticks: [24, 6, 4, ...]` multiplied by TICK = 0.05s!):
         holds:      [0.45, 0.12, 0.08, 0.05, 0.04, 0.04, # crouch anticipation -> explosive lunge smear
                      0.14, 0.08, 0.08, 0.10, 0.12, 0.30, # impact wall-drop -> brace against Bleed wave
                      0.05, 0.04, 0.16, 0.10, 0.10, 0.12, # mask blast -> crack -> halves flying
                      0.14, 0.16, 0.20, 0.25, 0.30, 0.60],# knees buckling -> slow tree-fall collapse
         offset:     [0, 0],                              # foot-anchored at bottom-center of event tile
         se:         { 4 => :beam_fire, 6 => :rumble, 13 => :mask_crack },
         hitstop:    { 14 => 0.14 },                      # real-clock freeze on exact mask-split frame!
         shake:      { 6 => 6, 14 => 7 },
         flash:      { 14 => { color: [255, 255, 255], power: 190, duration: 0.16 } },
         fx:         { 6 => { sheet: "Graphics/Animations/fx_ch9_roots", grid: [5, 2], blend: :normal } },
         after_graphic: ["act_ch9_rowan_collapsed", 0, 0],# swaps live RMXP event to aftermath pose when done!
         wait:       true

# 2. Inline helper callable straight from any RMXP map event Script command (no cutscene wrapper needed!):
pf_act_event("Mourner", "act_ch9_mourner_dive", grid: [6, 4], ticks: [9, 2, 2, 1, 1, 1, 3, ...], after: "rowan_kneeling")
```

- **Optional Sidecar JSON (`act_<scene>_<actor>.json`):** If `holds:` / `ticks:` is omitted, `act_play` automatically loads `{ "grid": [6, 4], "ticks": [...], "se": {...}, "hitstop": {...} }` alongside the PNG (matching Rejuvenation's `animsheettext.rb` / PNG `tEXt` metadata workflow!) so artists can tune timing without touching Ruby.
- **Scale & Anchor Guarantee:** Standard human acting sheets use **`64×64` or `96×96` per cell at 2×** (giving generous canvas headroom around a B2W2 `32×48` character for lunges, raised blades, billowing coats, and ground collapses without clipping, while keeping feet pinned to `[cell_w / 2, cell_h - 8]` on the exact tile!). Oversized Legendaries use `128×96` to `192×144` cells at 2× in 3/4 overworld view.

#### C. Live-Map Lighting, Fog, Shadows & Sparse Additive VFX (`012_Map_Acting.rb`)
- **`map_light`** — Places warm lantern pools, sunbeams (`sunbeamwhite` style), Bleed prism rim-glows, or flickering hearth/emergency lamps on `@viewport` (`z = 1050`, `:add` or `:normal` blend) anchored to map coordinates or events so darkened map tones (`tone to: [-72, -78, -56, 65]`) create Sea-of-Stars / Rejuvenation dramatic contrast.
- **Sparse Additive VFX Sheets (`play_sheet` / `fx_sheet` already in `012_Sheet_Effects.rb`):** Keep cells **thin, sparse, 4-color, additive (`blend: :add`)**, chained along motion paths with `at(t)` (like Reborn's *Dragonball Z* / `PRAS- Core Enforcer` and Rejuvenation's `anim_beam.png`) + RMXP database `anim id, at:` calls.
- **Inline Event Triggers:** Add `def pf_cutscene(id, **vars)` alias in `003_DSL.rb`, intercept `\cutscene[ID]` in `014_Portraits.rb` (`pbMessageDisplay`), and map `[cutscene: ID]` in `mapgen/layouts/scriptpour.py` so story scripts drop seamlessly into live-map choreography.

---

### 2.2 Pillar 2 Engine Primitives — True Frame-by-Frame Animated Full-Screen Sequences (`012_Animated_Sequences.rb`)

When a moment must break out of the top-down map into full-screen anime/pixel cinema (a blade thrust, a mask shattering in slow motion, a Plate fracturing, Kyogre's eye opening beneath black ice, Valen's crystal arm racing to his collarbone), Claude implements **two clean, complementary Pillar 2 playback modes**:

#### A. Native MKXP-Z Video Playback (`play_movie`) — For 6–25s Peak Sakuga Setpieces
Verified directly against the official MKXP-Z RGSS documentation (`roza-gb.gitbook.io/mkxp-z/extensions/rgss`):
- **Verified Engine Behavior:** `Graphics.play_movie(filename, volume = 100, skippable = true)` decodes Ogg Theora (`.ogv`) + Vorbis audio natively on CPU via TheoraPlay. MKXP-Z renders its letterbox at `z = 4999` and the video frame at `z = 5001` — meaning **custom RGSS sprites at `z = 5002+` render cleanly on top of live video** (for Prismfall's hold-to-skip indicator or styled caption ribbons!).
- **CPU Budget Guardrail:** Because TheoraPlay decodes on CPU, high resolutions (1080p/60fps) cause lag. Encoding strictly at Prismfall's **native `512×384` @ `24 fps`** (anime standard, or `30 fps` for fast VFX) uses `< 12%` CPU on a 10-year-old laptop, produces **pixel-crisp zero-scaling artifacts**, and keeps a 15-second peak cutscene under **`~2.5–3.8 MB`** on disk!

```ruby
# DSL call inside any cutscene (transitions directly from live map -> movie -> transformed live map!):
play_movie "Movies/pf_ch9_unmasking.ogv",
           volume:       90,                 # syncs with $PokemonSystem.bgmvolume / Master audio
           skippable:    :after_first,       # :always | :never | :after_first (checks $game_switches / Seen registry)
           transition:   :hard_cut,          # :hard_cut (2f black) | :flash_white | :step_fade (steps: 5)
           pause_bgm:    true,               # silences map BGM cleanly while .ogv's mastered audio track plays
           safe_movie:   "Movies/pf_ch9_unmasking_safe.ogv", # auto-selected when Cutscene.photosensitive?
           fallback:     :CH9_UNMASKING_SEQ, # auto-runs anim_cg_sequence fallback if .ogv absent or ENV["PF_NO_MOVIE"]
           on_end:       proc { |scene| scene.call_map_swap } # transform map underneath before returning!
```

**Technical Guardrails for `play_movie`:**
- Always verify `File.file?(path)` and `!ENV["PF_NO_MOVIE"]` and `Graphics.respond_to?(:play_movie)` before invoking, with `rescue StandardError` cleanly logging and triggering `fallback:`.
- Before calling `Graphics.play_movie`, execute the map-state switch underneath (e.g., switch Map `181` to `608`, or swap Rowan's event to unmasked kneeling pose on Map `264`) so the exact millisecond the movie ends, **the player lands directly on the scarred, transformed map** (exact Pokémon B2W2 & Rejuvenation V14 magic!).
- Respect `skip` cleanly: on first viewing of key plot moments (`skippable: :after_first`), pass `skippable = false` to `Graphics.play_movie`; on replays / Dream Mist theater / second runs, allow skip cleanly.

#### B. Native RGSS Frame-by-Frame Animated Cut-In (`anim_cg_sequence`) — For 2–5s Explosive Sakuga Bursts
For punchy **2–5 second full-screen animated close-ups** (12–48 bespoke frames at `512×384` — e.g., the Ring singing in Ch14, a mask cracking, an eye snapping open, a gauntlet tearing off, a 16-frame blade slash), native RGSS frame playback has **zero Theora compression artifacts, zero color-subsampling (`yuv420p`) bleed on crisp pixel art, and frame-accurate DSL sync** with `se:`, `hitstop:`, `shake:`, `flash:`, and dialogue!

```ruby
anim_cg_sequence :ch14_ring_sings,
  # Supports ANY of 3 storage formats automatically:
  #   1. Folder of crisp 512x384 PNGs: "Graphics/Pictures/Cutscenes/ch14_ring/f001.png..f024.png"
  #   2. Omori-style packed atlas PNG: sheet: "Graphics/Pictures/Cutscenes/ch14_ring_atlas.png", grid: [4, 4] (2048x1536)
  #   3. MKXP-Z native multi-frame GIF/animated Bitmap: gif: "Graphics/Pictures/Cutscenes/ch14_ring.gif"
  frames_dir: "Graphics/Pictures/Cutscenes/ch14_ring",
  count:      24,
  holds:      [0.12, 0.10, 0.08, 0.08, 0.08, 0.14,  # gold ring drops into palm & settles
               0.06, 0.06, 0.05, 0.05, 0.05, 0.06,  # chip catches lamplight -> 18-hue prism fan blooms!
               0.06, 0.06, 0.06, 0.08, 0.10, 0.14,  # 18 hues gather back to clear glass
               0.04, 0.12, 0.08, 0.08, 0.12, 0.35], # colorless sternum star-pulse -> lamps flare across room!
  se:         { 0 => :chime, 6 => :glass_quench, 18 => :prism_swell },
  hitstop:    { 18 => 0.10 },                       # crisp 1-frame sternum flash hold
  impact_frames: [18],                              # auto-skipped/softened when Cutscene.photosensitive?
  overlay:    { sheet: "Graphics/Animations/fx_prism_fan", blend: :add, at: [256, 192] },
  enter:      { kind: :step_fade, steps: 4, duration: 0.18 },
  exit:       { kind: :step_fade, steps: 4, duration: 0.22 },
  wait:       true
```

**Memory & Performance Contract for `anim_cg_sequence`:**
- Preloads frames into a local `@frames` array **before** frame 0 starts ticking (eliminating mid-animation disk stutter).
- `24` frames × `512×384×4` bytes = **`18.9 MB` VRAM** (`48` frames = `37.7 MB`), **100% disposed in `Effect#dispose`** the instant the sequence finishes — zero memory leak across a 60-hour playthrough.
- If art frames aren't on disk yet (during Wave 0 engine testing), auto-synthesizes numbered storyboard wireframe frames (`SEQ ch14_ring F07/24`) so `selftest/suite.ruby_stub` and `--render` pass immediately on every scene!
- Supports MKXP-Z's native multi-frame `Bitmap` (`Bitmap#animated?`, `frame_rate`, `goto_and_play`) when a `.gif` is provided for lossless 256-color pixel loops.

---

### 2.3 Scoped Transitions & Battle Juice (Strictly Separated From Story Cutscenes)

To prevent v1's mistake from ever creeping back:
- **`shatter_screen` (Voronoi Glass Fracture):** Implemented via `Graphics.snap_to_bitmap` triangulated into 20–28 scanline-blitted triangle shards on `@ui` (`< 8 ms` cut cost). **Strictly restricted to narrative glass-shatter events** (Ch5 Zap Plate Shatter, Ch9 Fist Plate burst, Ch11 Rimeholt ice breach, Ruin R1 Mirror Divergence) — NEVER used as a generic scene transition!
- **`glitch_tear` (Horizontal Scanline Slice / Chromatic Split):** 1 shared snapshot sliced across `strips` integer `src_rect` bands (`freq <= 4 Hz` in photosensitive mode). **Strictly restricted to** Ch0 NULL scanner, Ch7 Sable's Mirefen broadcast hijack, and Ruin Route Reverse Depths (`R1–R7`).
- **Battle-Only Anime Juice (`012_Anime_Juice.rb` — 0 New Art, Reusing All 31 `Graphics/EBDX/VS/*.png` Busts):**
  - `cutin_flash` (`:eye_strip` / `:full_bust` + `band*` + `bolt0..2` + `VS Cutin Lightning.ogg`) is wired **exclusively into battles** (Warden/Boss Ace send-outs, Mega Evolution, Z-Move, Multi-Bar Shield Break, Field Shatter) — **NEVER used as a substitute for animated story cutscenes!**
  - `chapter_card` renders a crisp `2.5s` prismatic chapter title eyecatch (or inverted glass card on Ruin `R1–R7`) on chapter transitions (`Prismfall::Story.advance_chapter`).

---

## Part 3 — Complete 22-Chapter + Ruin Route Production Slate (Redesigned Around REAL Rejuvenation V14 Craft)

### 3.1 Master Full-Game Slate (Every Chapter Ch0–Ch21 + Ruin R1–R7)

Every single chapter in Prismfall has:
1. **Pillar 1 — A Live-Map Choreographed Acting Beat** directly on its verified canonical map (`design/maps.json`), driven by a bespoke overworld acting sheet (`act_*.png`), `map_zoom`, darkened tone/lighting contrast, sparse additive VFX, and dead-silence audio drops; AND
2. **Pillar 2 — Either a crisp 2–4s Frame-by-Frame Animated Sakuga Cut-In (`anim_cg_sequence`, 12–24f) OR one of our 5 Full Peak `.ogv` Sakuga Setpieces (`★ PEAK #1–#5`).**

*(Zero battlebacks. Zero front battle sprites. Zero Ken Burns stills.)*

| Ch | Scene ID | Canonical Map(s) | Pillar 1 — Live-Map Acting Choreography (`on_map: true`) | Pillar 2 — True Animated Cut-In (`anim_cg_sequence` / `.ogv`) |
|---|---|---|---|---|
| **Ch0** | `:PRO_DOVETAIL_NULL` | `109` *Dovetail Deck* → `100` *Ferrow's Landing* | `act_ch0_voss_rail.png` (16f: Voss leaning on rail, raising chipped mug as 18 light-pillars shimmer on dark water via `map_light`) → live customs gate scan on `100` (`fx_scanner_sweep` green/blue on NPCs, dead blank on PC; `act_ch0_calla_snap.png` 12f double-take + secret camera click) | `anim_cg_sequence` (16f, `2.6s`): brass CRT monitor sweeping across 18 spectrum colors → hard `glitch_tear` snap to `IMPRINT: NULL` → Voss's smiling reflection stepping into the glass |
| **Ch1** | `:CH1_VEIL_CROSSING` | `522` *Glassed Orchard* → `103` *Larch Station* | Live Bleed Veil wall on `522`; `act_ch1_juno_recoil.png` (16f: Juno reaching out, snatching burned hand back) + `act_ch1_pc_walkveil.png` (16f: PC stepping cleanly through shimmering Veil as glassed Wurmple calms at their boots); `map_zoom 1.35` on Larch lowering her pen | `anim_cg_sequence` (18f, `3.0s`): night oil-lamp flame flickering over Larch's open journal on `103` — ink hand writing *"Second such reading in my life. Crownhaven, AF 290."* as the wick flares |
| **Ch2** | `:CH2_MOURNER_STAGE` | `145` *Lantern Theatre* | Warm pageant stage on `145` → `bgm_cut` dead silence → lights snap dark (`tone [-90,-90,-80,90]`) → `act_ch2_mourner_tear.png` (24f: painted backdrop rips down the center, Mourner steps through holding a white lily) + `act_ch2_thistle_shears.png` (16f: snipping fly-rope as banners drop) + `fx_cotton_spore` vanish | `anim_cg_sequence` (20f, `3.2s`): rapid push-in through ash petals as the Mourner's carved ash-bark eye-slits snap onto the PC (`hitstop 0.12s`, heartbeat `pulse`, colorless glint answering under PC's coat: *"...You."*) |
| **Ch3** | `:CH3_MATRIARCH_DRAIN` | `548` *Cocoonfall Hollow* | Live crystal-web cave on `548`; oversized 3/4 overworld `act_ch3_galvantula.png` (16f: thrashing in crystal shards); branches on `:ch2_matriarch` (`:soothe` = PC kneeling overnight as warm dawn light creeps across map; `:silence` = `act_ch3_pc_drain.png` palm press draining glowing Imprint into colorless void) | `anim_cg_sequence` (18f, `2.8s` — `:silence` branch): macro animated sequence of golden-violet Imprint filaments siphoning out of the Matriarch's eyes into the PC's palm like water down a drain, leaving its pupils dull grey |
| **Ch4** | `:CH4_EBB_SLUICE` | `167` *Ebbmouth Mill Quay* | Midnight on `167`: water autotiles freeze dead-still, distant intake erupts (`fx_water_blast` + `map_shake`), black tidal bore surges down mill-race toward child's punt; `act_ch4_sluice_team.png` (24f: PC, Marisol & masked Teo throwing weight onto iron wheel, slamming gate shut with `hitstop 0.10s`) | `anim_cg_sequence` (16f, `2.6s`): lantern swings across wet iron wheel — Teo's soaked mask slips up revealing his 19-year-old face in orange firelight as Marisol's grip opens to let him run |
| **Ch5** | `:CH5_SPIRE_SHATTER` **(★ PEAK #1)** | `186` *Gala* → `952` *Plate Vault* → `608` *Shattered Lowlight* | **★ FULL PEAK #1 STORYBOARD (§3.2.1):** Live Map `952` Mourner/Sable Splitter sabotage + smoking-glove aftermath + Map `608` walking through the Twelve in Glass + Valen pulling off his grey glove (`act_ch5_valen_glove.png`) | **★ `Movies/pf_ch5_shatter.ogv` (36f @ 24fps, `14s`):** Splitter lock → Mourner barehanded lunge → Zap Plate fracturing frame-by-frame → 2f B&W/violet impact + `0.14s` hitstop → Bleed wave erupting through bedrock into Lowlight streets, glazing Dex mid-wave! |
| **Ch6** | `:CH6_OSSUARY_UNOWN` | `625` *Ossuary Script Vault* | Torchlit fossil vault on `625`; `act_ch6_sahar_unseal.png` (16f: brushing sand off carved wall) + Unown swarm peeling off stone (`fx_unown_swirl` additive gold) + `map_zoom 1.3` as Kestrel steps into doorway backlight | `anim_cg_sequence` (24f, `4.0s`): living torch-lit animation across the Four Carved Murals coming alive in glowing gold sand — Theodric's Chain locking a radiant beast until it shatters into rain over drowned Aurelia |
| **Ch7** | `:CH7_QUIET_WARD` | `220` *Mirefen* → `223` *Corvin's Infirmary* | Infirmary lamps snap dead on `223`; `glitch_tear` hijacks wall monitor (`Sable: "The Hammer hasn't."`); Bleed Veil slams across Quiet Ward doorway; `act_ch7_pc_carry_ama.png` (20f: PC walking calmly into Veil, lifting salt-haired 9-year-old Ama out to Corvin) | `anim_cg_sequence` (18f, `3.0s`): macro close-up of Ama's clear salt-crystal cheek in candlelight — dead silence — then her translucent eyelids twitch and **her irises drift gently sideways, dreaming under the glass** |
| **Ch8** | `:CH8_CALDERA_DROP` | `255` *Cindervault Tap Chamber* | Molten caldera chamber on `255`; tap spikes white-hot (`fx_magma_vent` + `map_shake`); branches on `:ch8_caldera` (`:vent` sweeps `:ASHEN_WASTE` steam across live map); `act_ch8_sigrun_land.png` (20f: Salamence swooping down across tiles as Sigrun leaps off between Dominar's envoys and the Light Stone) | `anim_cg_sequence` (18f, `2.8s`): low-angle shot looking up through drifting volcanic embers as Salamence's wings part the smoke and Sigrun drops into frame, dragonhide cloak snapping in the updraft |
| **Ch9** | `:CH9_MOURNER_UNMASK` **(★ PEAK #2)** | `263` *Iron Pit* → `264` *Reliquary Ring* | **★ FULL PEAK #2 STORYBOARD (§3.2.2):** Live Map `264` Splitter click, glass racing down stairs at Juno & Nell, Mourner & Trevenant root-wall dive (`act_ch9_mourner_dive.png` + `act_ch9_trevenant_roots.png`), dead-silence `WAIT 40` collapse | **★ `Movies/pf_ch9_unmasking.ogv` (32f @ 24fps, `12s`):** Crystal wave smashing Mourner → 2f stark ink impact + `0.14s` hitstop → slow-motion close-up of ash-bark mask splitting down the bridge, tumbling past lens with white lily, revealing Rowan Ashby in red emergency light! |
| **Ch10** | `:CH10_OGERPON_STAND` | `294` *Heartgarden* → `708` *Bride Grove* | Unrotting rose petals snowing over `294` (`act_ch10_juno_ring.png` trembling with Rowan's envelope) → sunken `708` roots where poison collars glow violet on Loyal Three → `act_ch10_ogerpon_drop.png` (20f: Ogerpon leaping from Bride Tree canopy, swinging emerald ivy cudgel between Three and Meadow Plate!) | `anim_cg_sequence` (18f, `2.8s`): Ogerpon's Teal Mask snapping up from shadow in emerald moonlight, wood-chime SE, ivy cudgel igniting in a sweeping green smear arc |
| **Ch11** | `:CH11_KYOGRE_THAW` **(★ PEAK #3A)** | `309` *Sinking Quarter* → `300` *Thane's Harbour* | **★ FULL PEAK #3A STORYBOARD (§3.2.3A):** Live Map `309` ice tearing like a page (`fracture`), lantern houses sliding on tilting slabs, dead-vacuum water inhale/exhale, live cracking-tile sprint to Tower 4 | **★ `Movies/pf_ch11_kyogre_eye.ogv` (28f @ 24fps, `10s`):** Top-down through black harbour ice under PC's boots → house-sized blue-and-gold eye ringed in red coastlines snaps open → upward ice shatter as Primal Kyogre breaches into sleet! |
| **Ch12** | `:CH12_STORMWATCH_FALL` | `746` *Stormwatch Roof* → `740` *Conductors' Causeway* | Midnight broadcast on `746`; Kroll's Splitter detonates relay mast (`act_ch12_mast_collapse.png` + `fx_arc_sparks` + `map_shake`); Odessa's skiff rips through Stormfront; then eerie quiet on `740`: PC walks past rainwater puddle where **reflection steps half a second late** (`act_ch12_puddle_lag.png`) | `anim_cg_sequence` (16f, `2.8s`): rain ripples on `740` puddle — PC stops walking and looks down — their reflection keeps walking 3 frames further, pauses, and slowly tilts its head up to stare back |
| **Ch13** | `:CH13_MINDSCAPE_FAULT` | `354` *Mindscape* → `343` *Tribunal* → `348/355` *Fault* | Memory-dream `354`: `act_ch13_child_pc.png` (5-year-old PC in Choir ribbon) + `act_ch13_morwen_shield.png` throwing black veil over child + Mismagius drawing memory-curtain closed; then `343` Tribunal silence on Kaito's Marrowgate confession → `355` Fault earthquake splitting floor | `anim_cg_sequence` (24f, `4.0s`): AF 290 Crown cracking in blinding colorless star-burst — splinter flying straight across the stands into the 5-year-old's sternum — Mismagius purple velvet curtain snapping shut over the lens |
| **Ch14** | `:RD_1` *The Ring Sings* | `363` *Cragholm Lift Galleries* (`783` *Undersands*) | Exact canon `13_CUTSCENES.md` RD-1 on live Map `363`: Bastian's lamp-room, Pip on crate, Larch lowering her book; `act_ch14_bastian_hand.png` dropping plain gold band into PC's palm; every hanging miner's lamp flaring simultaneously via `map_light` (`783` also gets overworld `act_ch14_groudon_wake.png` 16f magma fissure) | `anim_cg_sequence` (24f, `4.2s`): extreme close-up of colorless stone chip catching lamplight, fanning out 18 razor-thin spectral colors and gathering back to clear glass (`hitstop` sternum star-pulse) |
| **Ch15** | `:CH15_CATHEDRAL_ECHO` | `394` *Hollow Cathedral* → `806` *Reverse Depths* | Live Map `394`: Kestrel slamming Meridian Resonance Gauntlet onto Spooky Plate (`act_ch15_kestrel_overload.png` 20f); spectral AF 290 echoes replaying directly across cathedral tiles (`act_ch15_morwen_echo.png` turning impossibly across ten years to face PC) → `806` barrow door opening downward into inverted sky (`act_ch15_giratina_origin.png` 24f six-wing unfurl) | `anim_cg_sequence` (24f, `4.2s`): Morwen's translucent lantern-lit ghost in the vestry turning her head 180° through 10 years of ghost-fire directly toward camera (*"Little one. You came back."*) before dissolving into candle sparks |
| **Ch16** | `:CH16_ZEKROM_BREAK` | `403` *Strade Works* → `223` *Infirmary (Interlude IV)* | Live Map `403`: Lattice-glass cage cracking around half-emerged 3/4 overworld `act_ch16_zekrom_chains.png` (24f: each boss bar snaps a golden cable; final sequence tears foundry skylight open into lightning); Interlude IV on `223`: `act_ch16_wenlow_door.png` stepping calmly in front of Quiet Ward → hard `bgm_cut` black cut + single dry gunshot SE | `anim_cg_sequence` (20f, `3.2s`): Zekrom's tail-generator igniting cobalt blue-black, snapping the last golden harness chain with a 2f B&W electric impact frame and blasting straight through glass skylight into storm clouds |
| **Ch17** | `:CH17_AURELIA_CRADLE` | `826` *Aurelia Gilded Throne Vault* | Drowned golden vault on `826`; `act_ch17_cradle_sing.png` (16f: ancient empty keystone cradle lighting up in resonance as PC approaches, matching RD-1's note); Voss stepping down the dais calmly (`act_ch17_voss_offer.png`: extending open hand in warm golden shafts) | `anim_cg_sequence` (18f, `3.0s`): empty golden keystone socket in the Sun Court cradle vibrating in slow-motion ripples of water droplets — matching the exact shape of the PC's glowing sternum scar |
| **Ch18** | `:CH18_HYMN_AND_K7` | `845` *Lightless Deep* → `443` *Great Tree Roots* | Dusk-chapel beneath `443` Great Tree: Gloaming choir lighting dusk-lamps around PC (`map_light` twilight indigo→gold as complete Hymn verses illuminate); then `act_ch18_kestrel_k7.png` (16f: Kestrel's Gauntlet sparking erratically, flinching mid-command if Bond high, putting on Morwen's Ring if given) | `anim_cg_sequence` (18f, `3.2s`): dusk-moths swirling upward from the Great Tree roots as 18 faint spectral lights pass peacefully across the canopy toward the night sky |
| **Ch19** | `:WAR_CLIMAX` (`WAR-1` v2) **(★ PEAK #3B)** | `864/865` *Wyrmscar* → `926` *Glass Dunes* | **★ FULL PEAK #3B STORYBOARD (§3.2.3B):** Existing `013_Scenes_War_OnMap.rb` on live Map `926` (overworld-scale `pfw_kyogre_*`, `pfw_reshiram`, `pfw_fx_flood`, armies, bone-carters, `pfw_fx_glass_wave` — ZERO battle sprites!) upgraded with live `map_zoom` + dead-silence collapse | **★ `Movies/pf_ch19_war_clash.ogv` + 3 Micro-Sequences (`18s` total intercut):** (1) Primal Kyogre eye & flood wall, (2) Reshiram blue-white tail-turbine ignition, (3) PC walking onto glassing sand with sternum glow, (4) Dead-silence collapse into falling mote! |
| **Ch20** | `:CH20_EIGHTEEN_PLATES` | `491` *Altar Stage* → `483` *Basilica Close* → `487` *Sanctum* | Live Map `491`: 18 Wardens processing down Sovereign's Stair setting Plates into Concordance Ring pylons; K8 `act_ch20_kestrel_tear.png` (20f: Kestrel tearing Resonance Gauntlet off and hurling it across arena tiles!); `483` Night of Masques (`act_ch20_voss_applause.png` clapping alone) | `anim_cg_sequence` (22f, `3.8s`): white-out vision inside the Tuning — an enormous wheel of light with 18 empty sockets slowly turning as **one golden-white divine eye** opens straight onto the PC (*"Little light. You have carried me far."*) |
| **Ch21** | `:CH21_VALEN_ARCEUS` **(★ PEAK #4)** | `491` *Temple-Arena Altar Stage* | **★ FULL PEAK #4 STORYBOARD (§3.2.4):** Live Map `491` Valen ungloving crystal arm (`act_ch21_valen_glove.png`), Arbiter Engine golden locks erupting, 11-lamp ally montage cross-cuts, Valen holding the Concordance pylons (`act_ch21_valen_hold.png`) + Homecoming dawn release | **★ `Movies/pf_ch21_valen_zygarde.ogv` (36f) + `Movies/pf_ch21_arceus_convergence.ogv` (48f):** Crystal racing up Valen's arm → Zygarde Complete hexagonal assembly → Arceus dragged down through cracked sky → Valen burning into light → 18-Plate Convergence! |
| **R1–R2** | `:RUIN_R1_GRAVES` | `806` *Reverse Depths* (+ Graves) → `403` *Strade Works* | Live Map `806` 23 epitaph graves; Juno's reflection stepping aside; `act_ruin_reflection_rise.png` (24f: mirror-PC standing out of grave #23, speaking backwards, falling into step as second shadow); on `403` freed Zekrom recoiling in terror from the PC (`act_ruin_zekrom_recoil.png`) | `anim_cg_sequence` (24f, `4.0s`): black glass splitting outward in reverse Voronoi shards (`shatter_screen mode: :implode`) as the PC steps *through* the mirror and their badge case bleeds pitch-black |
| **R3–R6** | `:RUIN_R3_THEODRIC` | `826` *Aurelia* → `926` *Ruin Dunes* → `491` *Unfestival* | Live Map `826` mirror-wall showing frozen AF 0 Sun Court where **Theodric's eyes move** (`act_ruin_theodric_glass.png`) and Voss drops to his knees; `926` Ruin `WAR-1` (shard *eats* clash-ball black, both legends flee in terror); `491` Plates dimming as PC walks past every pylon | `anim_cg_sequence` (20f, `3.4s`): extreme close-up on the gilded reflection behind Aurelia's glass — frozen court around him — then his gilded eyes track straight onto the camera and his lips silently shape one word: *"Finish."* |
| **R7** | `:RUIN_R7_MIRROR_PIERCE` **(★ PEAK #5)** | `491` *Altar Stage* → `963` *Ruined Crown* → `106` *Lighthouse* | **★ FULL PEAK #5 STORYBOARD (§3.2.5 — Prismfall's Direct "Maria Impales Vitus" Moment):** Live Map `491` Theodric stepping through arena crystal casting Voss into Chain → PC/Reflection mirror-pierce choreography → Giratina turning arena inside out (`:INVERSE`) → dead-silent aftermath | **★ `Movies/pf_ruin_mirror_pierce.ogv` (40f @ 24fps, `16s`):** Coiled dark-mirror anticipation → 3f blistering lunge + razor-white diagonal glass-blade smear → 1f pure black-on-white silhouette impale + 1f crimson-cyan chromatic flash + `0.16s` dead-silence hitstop → porcelain-gold fracture recoil → Giratina 180° world inversion! |

---

### 3.2 Deep Frame-by-Frame Production Storyboards — Prismfall's 5 "Maria-Impales-Vitus" Tier Peak Sakuga Moments

Each peak sequence below is specified to **frame-level animator discipline**: live-map setup (`Pillar 1`) → frame-by-frame full-screen animated sakuga (`Pillar 2`) → live-map aftermath (`Pillar 1`).

---

#### ★ PEAK #1 — Chapter 5: Lumen Spire Plate Vault Shatter (`SH1`) & Lowlight Bleed Wave (`Maps 952 → 608`)

> **Emotional Core:** The moment Prismfall stops being a bright adventure and breaks the player's heart. Sable turns a rescue into an atrocity; the Mourner burns his own hand trying to catch a dying Plate; twelve ordinary people (including 11-year-old Dex mid-wave) freeze into clear glass under the Spire.

##### Phase A — Live-Map Acting (`Map 952`, `on_map: true`, `~6.5s`)
- **Stage & Lighting:** Round subterranean Plate Vault cut into Spire bedrock (`952`). Lattice conduits pulse gold across floor tiles toward the crazed crystal cradle (`map_light` golden glow + subtle white heat shimmer).
- **Acting Sheets:**
  1. `act_ch5_mourner_vault.png` (`4×4` = 16f, `64×64` cells at 2×): Mourner kneeling/reaching gently with both gloved hands around the blazing Zap Plate (`holds: [0.35, 0.20, 0.20, 0.25...]`, gentle reverence — the player sees later he wasn't smashing it).
  2. `act_ch5_sable_splitter.png` (`4×4` = 16f): Sable crouching at cradle foot → springing upright in a jaunty half-skip (`frames 4..9`, fast `0.06s` holds) → tossing/clamping a blinking brass Splitter onto the Plate rim → stepping casually backward off the dais smiling (*"Light for everyone."*).
- **Camera & Audio Build:** `map_zoom to: 1.4, focus: :cradle, duration: 1.2` as `se :beam_charge` high-pitched rising whine climbs; Splitter LED ticks faster (4 ticks → solid white). At `t = 6.2s`, **`bgm_cut`** (instant total silence!). `act_ch5_mourner_vault` snaps into frames `12..15` (violent forward lunge toward the Plate) → **hard 2-frame cut straight into Pillar 2 `.ogv`!**

##### Phase B — Full-Screen Animated Sakuga (`Movies/pf_ch5_shatter.ogv`, `512×384` @ `24 fps`, 36 Keyframes / `~14s` with Holds)
| Frame Group | Timing / Holds | Camera Angle & Visual Action | Smear / Impact / Physics | Audio Track |
|---|---|---|---|---|
| **F01–F06** *(Anticipation)* | `1.1s` (held on 4s/3s) | Extreme macro close-up on brass Splitter clamped to golden Zap Plate rim. Red blink accelerates → snaps **blinding solid white** on F05. Fine pre-existing stress-cracks inside the Plate glow razor-violet. | Micro-vibration jitter on F05–F06; heat-mirage ripples | High-frequency sine whine cuts to **total dead silence** on F06 |
| **F07–F10** *(The Lunge)* | `0.25s` (on 1s/2s) | Low wide side-angle inside vault: the Mourner's grey cloak whips horizontally as he throws himself across the dais, bare gloved right hand lunging to cover the Splitter. | **F09 = 1-frame stretched pixel smear** of grey sleeve & white lily arcing across violet plasma | Single sharp leather snap + air rush |
| **F11–F14** *(The Shatter — B&W Impact + Hitstop)* | `0.42s` (`0.04s, 0.04s, 0.14s hitstop, 0.20s`) | **F11:** Pure stark **black ink silhouette on blinding white** — Mourner's hand gripping the Plate as jagged lightning forks across the entire 512×384 frame.<br>**F12:** Inverted **electric-violet & charcoal negative frame** showing the Zap Plate splitting straight across its core!<br>**F13 (`0.14s` real-clock hitstop):** Frozen fracture spiderweb radiating from the Plate through the vault floor.<br>**F14:** Vault shockwave blooms white-violet outward. | Genuine hand-drawn sakuga impact frames + hitstop; *(photosensitive `_safe.ogv`: skips F11–F12 strobe, holds high-contrast violet fracture with smooth vignette)* | **Dry thunderclap + "every bell in Lumen breaking at once"** (`bell_break` + `field_shatter`) |
| **F15–F22** *(Through Bedrock)* | `2.8s` (12–16fps) | Dynamic top-down pulling camera plunging **straight down through Spire stone & Lattice conduits** — a roaring ring of violet-prismatic Bleed racing outward down the cliff face toward dark rooftops below. | Parallax stone strata tearing past lens; trailing additive violet sparks | Deep subterranean bass roar fading into eerie glass-wind |
| **F23–F30** *(Lowlight Freezes)* | `4.5s` (slowing 16→8fps) | Street-level horizontal tracking cut across the Lowlight alley (`Map 608`): washing-line sheet mid-billow flashes iridescent translucent glass; cobbler's laugh crystallizes mid-frame; camera slows to a crawl onto **11-year-old Dex mid-wave** — the prism wave sweeps smoothly from his sneakers up to his smiling mouth, turning him clear glass while his Fizzbolt crate slides off his hip onto the cobbles! | Wave-front refraction shimmer sweeping cleanly left→right across character silhouettes; floating prism dust motes | Bass roar vanishes completely — **only one distant, fragile glass chime** |
| **F31–F36** *(Return to Vault)* | `2.4s` | Cross-fade through curling smoke back to close-up of the cracked Zap Plate in the Mourner's right hand — black smoke rising cleanly from his burnt leather glove, violet sparks sputtering erratically inside the fracture. | Delicate looping smoke curl (`12fps`); unsteady hand tremor | Faint sputtering static + heavy ragged breathing |

##### Phase C — Live-Map Aftermath (`Map 952` → `Map 608`, `on_map: true`)
- Instant return onto **transformed Map `952`** (cradle tile swapped to cracked state, smoke emitters rising). `act_ch5_mourner_burn.png` (16f) shows the Mourner clutching his smoking right hand away from his body, gently setting the cracked Plate back down like a dying bird, freezing when he spots the PC (*"...You. Not you. Not here. Get OUT—"*), and vanishing through the open south service door straight into **Overcharged Electivire** (`:NEON_GRID → :BLEED`).
- On stepping onto **Map `608`** (*Shattered Lowlight*, replacing `181` permanently): zero BGM, wind + single distant chime; PC walks untouched past all twelve glassed residents; Rook whispers *"...Turn it off. Rotom. Turn it off."* (`act_ch5_rook_drone.png` red LED clicking dark); Valen steps to the Veil (`act_ch5_valen_glove.png` 16f: pulling off grey glove, clear crystal hand pressing against the flinching Veil, snapping glove back on fast, locking eyes onto PC standing *inside*).

---

#### ★ PEAK #2 — Chapter 9: Ironreach Conclave — The Mourner Unmasking (`Map 264 / 263`)

> **Emotional Core:** The greatest Act II plot twist in Prismfall. The player just fought the Mourner thinking he was the terrorist — only to watch him throw his body in front of Juno and a child to stop Sable's Splitter, shatter his ash-bark mask in slow motion, and reveal **Uncle Rowan Ashby**.

##### Phase A — Live-Map Acting (`Map 264` Reliquary Upper Ring, `on_map: true`, `~6.0s`)
- **Stage & Lighting:** Iron Pit upper stone ring (`264`) bathed in pulsing **red emergency lamps** (`map_light` crimson wash over darkened stone tone `[-55, -75, -75, 45]`). Fist Plate burns crimson inside brass-clamped glass reliquary.
- **Audio Vacuum & Trigger:** Right after the Mourner battle ends, **`bgm_cut`** (total silence). `se` **a tiny metallic click**. The third Splitter on the reliquary flares pure white.
- **Choreographed Map Acting:**
  1. Red-to-grey Bleed wave shoots off the cracked reliquary across real map tiles (`play_sheet fx_ch9_glass_creep.png` chained tile-by-tile down the stairs via `at(t)`!).
  2. `map_pan` briskly (`0.4s`) down the stairs onto `act_ch9_juno_shield.png` (12f: Juno dropping to her knees wrapping arms around chalk-girl Nell: *"NELL. Get DOWN—"*).
  3. **Explosive Overworld Rescue:** `act_ch9_mourner_dive.png` (24f, `96×64` cells) launches down the real stairs at blinding speed alongside 3/4 overworld `act_ch9_trevenant_roots.png` (20f, `160×128` cells) — gnarled roots erupting straight through the stone tiles into a living timber wall inches in front of Juno! The glass wave slams into the roots, climbs them, and halts — while the full blast catches the Mourner square in the face → **hard cut straight into Pillar 2 `.ogv`!**

##### Phase B — Full-Screen Animated Sakuga (`Movies/pf_ch9_unmasking.ogv`, `512×384` @ `24 fps`, 32 Keyframes / `~12s`)
| Frame Group | Timing / Holds | Camera Angle & Visual Action | Smear / Impact / Physics | Audio Track |
|---|---|---|---|---|
| **F01–F05** *(Brace)* | `0.6s` | Tight over-the-shoulder profile behind Trevenant's surging roots: Mourner's grey hood whips back as the jagged grey-crimson Bleed wave rushes straight into his carved ash-bark mask. | Hair/hood cloth whip; flying bark splinters & stone grit | Low rushing vacuum roar |
| **F06–F08** *(The Crack — Impact + Hitstop)* | `0.36s` (`0.04s, 0.04s, 0.16s hitstop, 0.12s`) | **F06:** Stark **black-and-white ink impact frame** — jagged bolt splitting straight down the nose-bridge of the ash-bark mask.<br>**F07:** High-contrast red-emergency-lamp flash as the right side of the cowl rips away.<br>**F08 (`0.16s` hitstop):** Frozen hairline split down the mask center, glass crystallizing over the Mourner's right shoulder. | Pure B&W ink crack frame + `0.16s` hitstop freeze; *(photosensitive `_safe.ogv`: smooth red-amber rim glow, zero strobe)* | **`bgm_cut` silence → ONE razor-sharp dry branch-snap (`mask_crack`)** |
| **F09–F20** *(Slow-Motion Unmasking)* | `5.2s` (over-cranked `8–12fps` silk motion!) | **Extreme close-up straight into the mask:** the two ash-bark halves slowly peel apart left and right across the frame, tumbling lazily out of focus past the foreground lens. **The single white lily detaches and drifts slowly across the center of the screen** as warm red emergency lantern light washes across the face behind it — **bleeding brow, soil-stained cheeks, weary grief-lined eyes: Rowan Ashby!** | Multi-plane tumbling mask halves (large foreground silhouette blur-free pixel edges + mid-ground drifting white lily + slowly widening eyes) | **Complete dead silence** except two faint hollow clatters as the bark halves hit glass off-screen |
| **F21–F26** *(The Lightning Palm)* | `2.6s` | Tilts smoothly down past Rowan's half-glassed right collarbone onto his bare right hand bracing against the glassy floor — the bandage torn off, **revealing the jagged violet-white lightning burn scar across his palm** (paying off Ch7's ledger clue `R.A. — Bleed-burn, right palm`!). | Delicate glass-frost creeping 2px upward along his neck with faint crystalline glint | Single quiet crystalline ping |
| **F27–F32** *(Juno's Gaze)* | `2.8s` | Reverse tight close-up through the gap between Trevenant's dark roots: Juno's wide, tear-brimming eyes reflecting the red lamp and Rowan's unmasked face, Nell's small hand clutching her collar. | Trembling pupil micro-shift, blossom wreath petal drifting past cheek | Silence holds into live-map return |

##### Phase C — Live-Map Aftermath (`Map 264`, `on_map: true`)
- Returns seamlessly onto **transformed Map `264`** (glass tiles spread to the root-wall; **two real map sprites of the split mask halves + white lily lie on the stone floor**; Rowan swapped to `act_ch9_rowan_collapse.png`).
- **Exact Canonical Silence (`WAIT 40` = `2.0s`):** Nobody speaks. Only wind and glass hum.
- Juno whispers: *"...Uncle Rowan?"* → Rowan: *"Juno. Don't look at me like that. Look at the flowers. Look at what they're standing on."* → `act_ch9_rowan_collapse.png` (16f, slow heavy `0.16s` holds) folds slowly forward onto the glass *"like a tree going over."*
- Camera pans briskly across the Pit to Kestrel frozen over Honedge's hilt (*"...It's not her."*), then locks onto the PC walking calmly into the Bleed untouched to haul Rowan out — straight into the agonizing `:ch9_teo_sable` split choice!

---

#### ★ PEAK #3 — Chapters 11 & 19 Paired Kaiju Setpieces: Primal Kyogre Thaw (`Maps 309/300`) & Glass Dunes Beam Clash (`WAR-1` Upgraded on `Map 926`)

> **Emotional Core:** Scale and mythic awe — proving that Legendaries in Prismfall feel like **living weather systems**, not sprites standing in a battle menu. Both scenes obey our iron law: **overworld-scale 3/4 acting sheets on the real map + explosive full-screen animated sakuga close-ups.**

##### Part A — Ch11: *When the Lake Breathes* (`Maps 309 → 300`, `~16s` total)
- **Phase A (Live Map `309` Sinking Quarter, `on_map: true`):** Nighttime harbour lamps lit. `fracture` splits a slow black line across real ice tiles (*"the way a page tears"*). `act_ch11_slab_tilt.png` gently tilts the far street of timber houses as lamps slide. Suddenly **all screaming and harbour bells cut to dead silence (`bgm_cut`)**. The entire harbour subtly lifts (`map_zoom 1.0 → 1.06` slow 1.4s swell) and exhales back down (`1.06 → 1.0`) with a subterranean sigh.
- **Phase B (Full-Screen Animated Cut-In — `Movies/pf_ch11_kyogre_eye.ogv`, `512×384` @ `24fps`, 28 Keyframes / `~10s`):**
  - **F01–F08 (Abyss Stillness, `2.8s`):** Top-down angle looking straight down through translucent black harbour ice beneath the PC's snow-dusted boots. Darkness below. One slow underwater current ribbon drifts.
  - **F09–F16 (The Eye Opens, `2.6s`):** Faint bioluminescent red-and-cyan coastline markings ignite deep under the ice → **a house-sized blue-and-gold eye opens frame-by-frame**, golden iris contracting until it locks directly onto the tiny boots above it! Colorless glint flashes softly at the PC's pocket/chest (`se :glass_quench`).
  - **F17–F20 (Upward Breach — Impact + Hitstop, `0.45s`):** 1f cyan-white impact silhouette + `0.12s` hitstop + `shatter_screen mode: :inverse` blasting jagged black-ice slabs straight past the camera lens!
  - **F21–F28 (Primal Breach, `4.0s`):** Dramatic upward-tilting anime panorama of **Primal Kyogre** erupting through Rimeholt's broken harbour against sleet and red tower-lamps, Alpha symbols blazing cyan (`Boss - Kyogre` slams in on F23!) → cuts cleanly back to flooded Map `309` (*"That's not a Pokémon, that's WEATHER. TOWERS! EVERYBODY TO THE TOWERS!"*) straight into the live cracking-tile rescue sprint!

##### Part B — Ch19: *WAR-1 Upgraded — The Beam Clash on the Glass Dunes* (`Map 926`, `~68s` live-map + intercut sakuga)
`013_Scenes_War_OnMap.rb` ALREADY got the Pillar 1 foundation right (real bone-white desert map, overworld-scale `pfw_kyogre_rise` / `pfw_kyogre_primal` / `pfw_kyogre_side` / `pfw_reshiram`, `pfw_fx_flood`, `pfw_fx_glass_wave`, drilled army blocks, bone-carters — **zero battle sprites**!). We elevate `:WAR_CLIMAX` to true Rejuvenation V14 cinema by weaving **4 tight frame-by-frame animated sakuga cut-ins (`Movies/pf_ch19_war_clash.ogv` / 4 indexed micro-sequences)** directly into the live Map `926` choreography:

1. **Cut-In 1 — Kyogre Primal Eye & Flood Wall (replaces Shot 4A static zoom, 16f / `2.8s`):** Low-angle animated cut-in across the churning flood crest: blue-white **Origin Pulse** vortex spiraling inward inside Kyogre's jaws as its glowing Alpha markings pulse and a 40-foot black wave towers behind its fins!
2. **Cut-In 2 — Reshiram Tail-Turbine Ignition (replaces Shot 4B static zoom, 16f / `2.8s`):** Tight animated rear-three-quarter angle on Reshiram spreading massive feathered wings over the Siege Camp — tail-rings spin and snap open, **blue-white plasma jets roaring to life**, vitrifying bone-sand underneath into glowing orange-white molten glass sparks!
3. **Cut-In 3 — The Unimprinted Walks onto Glassing Sand (upgrades Shots 9A–10, 24f / `4.5s`):** Replaces tiny walking sprite with a breathtaking low-angle animated tracking cut-in: wind tearing backward through the PC's coat and hair, boots crunching across glowing steam-glass while a curling ocean wave freezes into translucent crystal right behind their shoulder; PC lifts one hand straight up into the blinding beam-dome as the colorless sternum shard flares white! *(Variants B/C swap cleanly to Sigrun's Salamence dive / Marisol's sled-boat prow cresting the flood!)*
4. **Cut-In 4 — The Dead-Silence Collapse (upgrades Shot 11, 20f / `3.8s`):**
   - **Standard (`:A` / `:B` / `:C`):** **`bgm_cut`** to absolute zero! The raging fire-and-sea clash-sphere desaturates frame-by-frame to pure pearl-white (`F01–F06`), implodes inward with a 1-frame razor-black core + `0.14s` hitstop (`F07–F09`), and collapses into **one single falling luminous glass mote** drifting down past the PC's upturned face (`F10–F16`) as pouring rain crystallizes into slow silent snow (`F17–F20`, one soft glass chime!).
   - **Ruin Route R5 Variant (`:ruin`):** The colorless shard turns **pitch-black ("the none")**, violently *swallowing* both beams into an inverted void sphere (`glitch_tear` + `0.16s` hitstop) — both Kyogre and Reshiram recoil and flee in silent terror!
- **Phase C (Live Map `926` Aftermath):** Returns seamlessly to live Map `926` where the permanent steam-glass plain and frozen glass wave stay on the ground (`stay: :forever`), Sigrun and Anja drop onto the glass beside the PC (*"Father. Enough."* / *"Eirik. Enough."*), Meridian's Dr. Quent folds his brass tripod on the mesa, and the bone-carters walk out under a fresh white banner.

---

#### ★ PEAK #4 — Chapter 21: Sovereign Valen's Crystal Arm, Zygarde Complete & 18-Plate Arceus Convergence (`Map 491`)

> **Emotional Core:** The emotional and mythic zenith of the entire 60-hour campaign. Valen's quiet thirty-year sacrifice becomes physical, visible horror and grace; Zygarde Complete assembles to defend order; Arceus descends in agony; and eighteen Wardens finally choose whether to let go.

##### Part A — Valen's Glove Off & Zygarde Complete (`Map 491` Final & FH-2)
- **Phase A (Live Map `491` Temple-Arena Altar Stage, `on_map: true`):** Dawn light spilling across the Concordance Ring. `act_ch21_valen_glove.png` (16f): Valen standing opposite the PC, calmly pulling his grey glove off with his teeth/left hand and letting it fall onto the arena stone (*"Come on, then. Show me there's another door."*). On Zygarde's final boss bar (`Order, not justice. I chose order.`), `map_zoom 1.45` snaps onto Valen as the arena tone drops deep emerald-charcoal.
- **Phase B (Full-Screen Animated Sakuga — `Movies/pf_ch21_valen_zygarde.ogv`, `512×384` @ `24fps`, 36 Keyframes / `~13s`):**
  - **F01–F10 (Crystal Creep, `3.2s`):** Extreme close-up on Valen's bared right arm — translucent white crystal fractures race visibly upward past his elbow, shattering his white sleeve cuff and climbing up to his collarbone with deep-water light pulsing inside. He doesn't flinch; his jaw sets.
  - **F11–F22 (The 100% Assembly, `3.6s`):** Swirling camera whips upward from the arena floor: hundreds of luminous emerald **Zygarde Cells** stream like fireflies out of every stand and sky-arch, slamming together in rapid mechanical anime snap-cuts (12–24fps interlocking armor plates, blazing crimson-blue-gold chest cores clicking shut with metallic chimes!).
  - **F23–F26 (Core Enforcer Impact + Hitstop, `0.45s`):** 2f stark black-on-emerald silhouette impact as Zygarde Complete's chest splits open and fires → `0.14s` hitstop → blazing emerald **Z** searing cleanly across the frame!
  - **F27–F36 (Hold & Return, `2.8s`):** Smoke parts on Zygarde Complete towering over the lone white-robed Sovereign; cuts cleanly back to live Map `491` / final boss bar!

##### Part B — The Hijack, Valen Holding the Ring & 18-Plate Arceus Convergence (`Map 491`)
- **Phase A (Live Map `491`, `on_map: true`):** As Valen lifts the Crown over the PC's head, the eighteen pylons *scream* (`bgm_cut` → golden hum). `act_ch21_engine_rise.png` (20f) splits the altar tiles as the golden Arbiter cradle rises from below; rapid 1.2s live-map cross-cuts fire **Larch's 11-Lamp Ally Montage** (Rook killing Lumen's grid, Magnus cutting the governor, Sigrun + Reshiram holding the sky, Marisol's boats, Tamsin's silk nets). After Voss drives the spike into the cradle:
- **Phase B (Full-Screen Animated Sakuga — `Movies/pf_ch21_arceus_convergence.ogv`, `512×384` @ `24fps`, 48 Keyframes / `~18s`):**
  - **F01–F12 (The Sky Opens, `4.2s`):** Looking straight up through Crownhaven's caldera cloud ring — the sky tears open pure white; **Arceus** is dragged downward into 18 golden chain-locks clamping onto the 18 empty slots of its wheel, writhing in silent blinding light as prismatic Bleed shockwaves roar toward forty thousand spectators.
  - **F13–F26 (Valen Holds the Door, `5.0s`):** Tight low-angle shot inside the Concordance Ring: Valen puts the cracked Crown back on, plants both feet, and clamps both hands around two blazing pylons (*"Go. Free it. I'll hold the door — I've had thirty years of practice."*). *(Conditional layer if `ILSA_RECONCILED`: Ilsa steps directly behind his back, palms pressed to his shoulders: "Little owl's got you.")* As the final lock breaks, **Valen's crystal arm burns from glass into pure warm golden-white light**, spreading gracefully across his smiling face before he dissolves cleanly into rising motes and the empty Crown clatters softly onto stone (`bgm_cut` silence!).
  - **F27–F38 (18-Plate Convergence, `4.8s`):** Sweeping 360° upward spiral: eighteen distinct type-colored ribbons (from Dorian's Blank silver through Sigrun's Draco violet) unchain from the pylons and weave upward into Arceus's wheel, locking home one by one with a rising 18-note harmonic chord!
  - **F39–F48 (The Heart Returns, `4.0s`):** Extreme calm close-up on the PC's chest: the colorless shard lifts painlessly out of their sternum in slow motion, floating up beside the Crown's chip until **the Legend Plate clicks whole for the first time since AF 0**, washing the screen gently into pure white dawn → returns cleanly onto peaceful Map `491` for Arceus's final words and `:ch21_final`!

---

#### ★ PEAK #5 — Ruin Route: Prismfall's Direct "Maria Impales Vitus" Moment (`R1/R2 Reflection Mirror-Pierce`, `R3 Theodric Behind the Glass`, `R7 Giratina Distortion Finale` — `Maps 806, 826, 491, 963`)

> **Emotional Core:** This is Prismfall's direct artistic answer to **Maria/Melia impaling Vitus** and **Kaina piercing Melia** in Rejuvenation V14. Cold, lucid, devastating, and razor-sharp. No heroic speechifying, no melodramatic villain laugh — just **surgical, breathless dread, one unforgettable frame-by-frame mirror-blade pierce in dead silence, and the horrific realization of what the player chose.**
>
> **Narrative Anchor (100% Canon `story/12_RUIN_ROUTE.md`):**
> - **R1 (`806` Reverse Depths):** Twenty-three epitaph graves; the Reflection rises from grave #23; Giratina grants **"the none"**.
> - **R3 (`826` Aurelia):** Theodric's gilded reflection moves behind the mirror-wall and mouths *"Finish."*
> - **R7 (`491 → 963` Crownhaven Unmaking):** Theodric steps out of the arena's crystal walls wearing the Gilded Chain, casts Voss aside into the Chain, and attempts to seize Arceus's Judgment — until the PC (carrying **"the none"**) and the Reflection drive a razor-shard of inverted mirror-glass straight through the Chain's keystone heart (and in the final choice `:ruin_walk`, either the Reflection steps into the blade's unmaking *on purpose* or the PC does!).

##### Phase A — Live-Map Choreography (`Map 491` Temple-Arena Inverted / `Map 806` Mirror Chamber, `on_map: true`, `~7.0s`)
- **Stage & Lighting:** Temple-Arena (`491`) drained of all 18 colors (`tone [-65, -70, -55, 190]` — stark cold silver-indigo monochrome). Every reflective crystal tile on the floor shows the upside-down golden court of drowned Aurelia. Only the Gilded Chain's central keystone lock glows cold gold.
- **Map Acting Build-Up:**
  1. `act_ruin_theodric_cast.png` (16f): Theodric's gilded reflection steps effortlessly out of the crystal floor, lifting Voss one-handed and casting him aside into the golden Chain.
  2. `map_zoom to: 1.45, focus: :pc, duration: 0.75, ease: :in_out`. The PC stands utterly still; **the Reflection** (`act_ruin_reflection_step.png`, 16f) steps silently out from *behind* the PC's shadow so both stand side-by-side — identical silhouettes, mirrored left-to-right.
  3. **The Coil:** `act_ruin_mirror_draw.png` (16f, `holds: [0.35, 0.25, 0.15, 0.10, 0.08, 0.06, 0.45]`): PC / Reflection raises one hand — a jagged sliver of pitch-black, mirror-edged glass (**"the none"**) crystallizes out of thin air along their forearm, dripping inverted silver ripples onto the arena tiles.
  4. **`bgm_cut`** — **EVERY SOUND IN THE GAME DIES.** `0.40s` absolute vacuum. Just one quiet footstep forward → **hard 0-fade cut directly into Pillar 2 `.ogv`!**

##### Phase B — Full-Screen Animated Sakuga (`Movies/pf_ruin_mirror_pierce.ogv`, `512×384` @ `24 fps`, 40 Keyframes / `~16s`)
*(Crafted beat-for-beat on the exact principles that make Rejuvenation V14's Maria/Vitus impale sequence breathtaking!)*

| Frame Group | Timing / Holds | Camera Angle & Visual Action | Smear / Impact / Physics | Audio Track |
|---|---|---|---|---|
| **F01–F08** *(The Cold Stillness — Anticipation)* | `2.2s` (slow `6–8fps` breath) | Tight two-shot profile across the dark-glass arena: left foreground = PC/Reflection's dark silhouette, eyes utterly calm and dead-lucid, jagged black-silver mirror-blade hovering low; right background = Theodric's gilded reflection smiling patronizingly behind his golden Chain, raising one hand (*"Kneel."*). | Subtle coat-hem stillness; microscopic glass dust drifting **upward** (gravity inverted!) | **Dead vacuum silence.** On F07, ONE dry crystalline chime like a scalpel touching glass. |
| **F09–F12** *(The Blistering Lunge & Smear)* | `0.20s` (pure `24fps` on 1s!) | **F09:** PC/Reflection drops 3 inches into an explosive coiled crouch, hair whipping forward.<br>**F10:** **Blistering 1-frame diagonal smear** — the entire figure stretches into a razor-white & pitch-black mirror streak tearing left-to-right across 400 pixels!<br>**F11:** Camera whips right behind Theodric's shoulder as the black-mirror edge slices straight through the golden Chain links in a burst of shattered gold sparks!<br>**F12:** Extreme close-up on Theodric's gilded eyes snapping wide open — zero time to raise a guard! | **True sakuga smear frames** (elongated motion streaks, dynamic diagonal speed-lines, shattered chain-links spinning toward lens) | Razor wind-tear + sharp metallic snap (`beam_break` pitched high + dry) |
| **F13–F15** *(THE PIERCE — Peak Sakuga Impact + Hitstop)* | `0.38s` (`0.04s, 0.04s, 0.18s hitstop, 0.12s`) | **F13 (1f Pure Ink Impact):** **Stark 2-color pure black silhouette on blinding white background** — the long razor-shard of "the none" driving **clean straight through the center of Theodric's gilded chest / the Chain's keystone heart**, erupting out his back in a fan of black glass splinters!<br>**F14 (1f Chromatic Flash):** Inverted **deep crimson-and-cyan negative silhouette**, hairline cracks spiderwebbing instantly from the entry wound across Theodric's entire gilded body.<br>**F15 (`0.18s` REAL-CLOCK HITSTOP):** **Total frozen tableau** — not a single pixel moves except a tiny razor-thin shock-ring expanding silently around the blade! | Signature Rejuvenation V14 / anime sakuga lethal impact frame pair + extended `0.18s` hitstop; *(photosensitive `_safe.ogv`: holds crisp high-contrast dark-indigo silhouette pierce with zero strobe flicker, full `0.18s` hitstop intact)* | **ZERO MUSIC.** One sickeningly crisp, dry **crystalline pierce + low sub-bass thud** (`blade_pierce` + `field_shatter` low-pass) |
| **F16–F26** *(The Porcelain Fracture & Quiet Horror)* | `5.0s` (slow `8–10fps`) | Camera drifts slowly closer to the impaled figure in complete stillness. **Black mirror-cracks crawl across Theodric's gilded face like ink on porcelain**, flaking away into silent grey dust rather than blood; his gilded hand rises half an inch, trembles, and drops limp. Camera slides past his shoulder onto the **PC's completely unmoved, tearless eyes** — and behind them, the Reflection whispering calmly: *"Twenty-three times. Let me do it once on purpose."* | Frame-by-frame flaking porcelain-gold shards floating upward; subtle hair drift; zero camera shake (cold stillness is ten times scarier than shaking!) | **Still dead silence** — only tiny glass flakes tinkling softly as they drift upward |
| **F27–F40** *(Giratina's Inversion — Arena Turns Inside Out)* | `5.2s` (`16–24fps`) | Behind the crumbling Gilded Chain, **six colossal black-and-crimson shadow wings** tear straight up through the mirror-floor! Giratina (Origin) shrieks silently as the horizon **literally rotates 180° upside-down** (`F31–F36` sweeping rotational frame animation, arena pylons falling upward into a black sky while Arceus descends overhead in cold white Judgment!) → hard step-fade straight into live `:INVERSE` battle! | Sweeping shadow-wing silhouette sweep + full-frame 180° horizon inversion + floating shattered arena stones | Low distorted organ chord + Giratina reversed cry slamming into final `:INVERSE` boss theme! |

##### Phase C — Live-Map Aftermath (`Map 491 → Map 963`, `on_map: true`)
- Returns directly onto **inverted Map `491` / `963` (*Crownhaven - Ruined Crown*)**: every gilded pillar cracked, zero BGM for 3 full seconds (`WAIT 60`), Voss either pulled out hollow (`:ruin_voss` *spare*) or dissolved inside the dead Chain (*abandon*), leading into the 7-bar **Arceus (Judgment)** finale with Giratina at the PC's side and the chilling `:ruin_walk` choice (*The Unmaking* vs. *The One Who Came Back*, ending on Hesper's cracked mirror in Map `106` with nothing behind it).

---

## Part 4 — Honest Art, Animation & Real-Engine Verification Pipeline

### 4.1 Hard Production Rules (Zero Cheating, Zero Mockups)

1. **All new pixel art & anime keyframes are 100% pure `generate_image`** (post-quota-reset), with Python strictly restricted to chroma-key transparency cleanup, exact 2× nearest-neighbor scaling, grid slicing/alignment, foot-anchor validation, and `ffmpeg` encoding.
2. **NO HTML Canvas fake cutscenes ever again.** Every reviewable preview sent to the creator MUST be a **real `.mp4` / `.gif` recorded inside our actual `mkxp-z` executable** via `plugins/Prismfall Cutscenes/tools/engine_capture/capture.sh`.
3. **Prove ONE Peak Cutscene First (Vertical Slice Gate):** Do NOT mass-produce 29 scenes blindly. Build **Wave 0 (Engine)** + **Wave 1 (1 Complete Peak Scene — Peak #1 `SH1` OR Peak #2 `Ch9 Unmasking`)** end-to-end and record it inside real `mkxp-z` for the creator's explicit thumbs-up BEFORE generating Waves 2–4!

---

### 4.2 Exact Pillar 1 Production Pipeline — Custom Overworld Acting Sheets (`act_<scene>_<actor>.png`)

How Gemini produces Rejuvenation V14–grade custom overworld acting sheets that match our exact B2W2 pixel art scale with zero proportion drift:

1. **Reference Lock (Mandatory `ImagePaths` Input):** Every acting-sheet generation passes **2 locked reference images**:
   - `b2w2_ow_ref_plate.png` (locks exact Gen 5 B2W2 16×24 native / 32×48 2× head-to-body ratio, `1×2` eye spacing, dark outline weight, and 3/4 top-down camera angle), AND
   - The character's approved `Graphics/Characters/<NAME>.png` overworld walk sheet (locks exact hair silhouette, coat/cloak palette, and costume details).
2. **Single-Call Unified Action Sheet (`4×4` = 16 frames or `6×4` = 24 frames):**
   - Never generate individual acting frames across 16 separate calls (costume and pixel density drift every call!).
   - Generate the entire action arc in **ONE structured grid call** on flat magenta (`#FF00FF`) background with uniform cell gutters:
     - **Row 0:** Idle → coiled anticipation crouch (4–6 frames)
     - **Row 1:** Explosive launch / weapon draw / **1–2 stretched pixel smear frames**
     - **Row 2:** Peak contact / impale / shield / shock pose
     - **Row 3:** Recoil / stagger / knees buckling / final aftermath pose (which doubles as `after_graphic:` on the live map!)
3. **Python Post-Processing & QA Gate (`tools/cutscene_art/pack_acting_sheet.py`):**
   - Chroma-key `#FF00FF` + despill to hard 1-bit alpha (zero fuzzy anti-aliased edges!).
   - Nearest-neighbor downscale to exact native art pixels (`32×32` or `48×32` native → **`64×64` or `96×64` at 2×** for humans; **`128×96`–`192×144` at 2×** for 3/4 overworld Legendaries).
   - Foot-anchor alignment pass locking every cell's grounded baseline `[cx, cell_h - 8]` so characters never jitter vertically unless intentionally jumping/falling.
   - Emits matching `act_<scene>_<actor>.json` containing exact variable `ticks:` (anticipation → fast smear → hitstop → slow recovery).

---

### 4.3 Exact Pillar 2 Production Pipeline — Frame-by-Frame Animated Sakuga (`anim_cg_sequence` & `.ogv`)

How Gemini produces genuine frame-by-frame animated anime/pixel cut-ins (changing angles, expressions, cloth/hair motion, weapon impacts) without face/palette drift:

1. **Step 1 — Character & Lighting Key Lock:** Pass the character's approved portrait / VS bust (`Graphics/EBDX/VS/<NAME>.png`) + scene palette key via `ImagePaths` so faces, hair colors, and outfits stay 100% on-model.
2. **Step 2 — Linked Storyboard-Grid Keyframe Sheets (`4×2` = 8 panels or `4×3` = 12 panels per call):**
   - Generate **8–12 sequential animation keyframes inside ONE grid image** (`16:9` or `4:3` clean thin-bordered panels, numbered top-left to bottom-right). Because Gemini renders all 8–12 panels inside a single latent pass, **character proportions, lighting direction, costume folds, and background geometry stay locked frame-to-frame!**
   - Specify exact pose progression per panel in the prompt (e.g., Panel 1: mask intact under red lamp → Panel 2: hairline crack appears → Panel 3: crack widens glowing white → Panel 4: right half breaks free → Panel 5: both halves peel outward revealing shadowed eyes → Panel 6: white lily floats across lens → Panel 7: red firelight illuminates Rowan's bleeding brow → Panel 8: eyes lock downward in grief).
3. **Step 3 — Continuity Chaining for Longer Peak `.ogv` Sequences (24–48 Frames):**
   - For multi-beat Peak sequences (`SH1`, `Ch9 Unmasking`, `Ch11/19`, `Ch21`, `R7 Mirror-Pierce`), feed the **final sliced panel of Sheet 1** back into `ImagePaths` as the opening frame reference for Sheet 2 (`K9→K16`, `K17→K24`, `K25→K32`).
4. **Step 4 — Smear Frames, Impact Frames & Pixel/Anime Finishing Pass:**
   - Slice grid panels to exact **`512×384`** (`4:3` native screen resolution).
   - Color-match palette continuity across sheets (eliminate exposure flicker).
   - Author/generate dedicated **1–2f smear frames** and **stark 2-color B&W / inverted impact frames** on the exact climax beat (`F11–F12` in Ch5, `F06–F07` in Ch9, `F13–F14` in R7).
   - Layer clean animated foreground dust, ash petals, glass shards, or additive prism flares at `24 fps` on-ones over `12 fps` on-twos character keyframes (authentic anime sakuga rhythm!).
5. **Step 5 — Native MKXP-Z `.ogv` Encoding via `/usr/bin/ffmpeg` (Verified Installed on VM):**
   - **Standard Master `.ogv`** (`512×384`, `24 fps`, crisp nearest-neighbor scaling, TheoraPlay-optimal CPU bitrate, Vorbis stereo audio):
     ```bash
     ffmpeg -y -framerate 24 -i work/frames/f%04d.png -i work/audio/pf_ch9_unmasking_mix.wav \
       -vf "scale=512:384:flags=neighbor" \
       -c:v libtheora -q:v 8 -pix_fmt yuv420p -g 24 \
       -c:a libvorbis -q:a 6 -ar 44100 -ac 2 \
       Movies/pf_ch9_unmasking.ogv
     ```
   - **Photosensitive-Safe `.ogv` (`*_safe.ogv`):** Same command after swapping B&W strobe frames for dark-vignette hold frames and verifying frame-to-frame luminance delta stays ≤ 15%.
   - **Short 2–4s Cut-Ins (`anim_cg_sequence`):** Skip `.ogv` completely — deploy crisp lossless `512×384` PNGs in `Graphics/Pictures/Cutscenes/<scene>/f001.png..f024.png` (or packed `2048×1536` `4×4` atlas PNGs) for zero compression artifacts!

---

### 4.4 Mandatory Real-Engine Verification Gate (`mkxp-z` Raw Capture)

Before ANY cutscene is presented to the creator:
1. **Run `selftest/suite.ruby_stub`** — verifies 0 memory leaks, real-clock `hitstop` completion, frame-rate independence (`20/40/60/144 FPS`), skip behavior, and photosensitive clamping.
2. **Capture Real Gameplay Inside `mkxp-z`:**
   ```bash
   bash "plugins/Prismfall Cutscenes/tools/engine_capture/capture.sh" assemble
   bash "plugins/Prismfall Cutscenes/tools/engine_capture/capture.sh" sync
   CUT_EVERY=1 bash "plugins/Prismfall Cutscenes/tools/engine_capture/capture.sh" run CH9_MOURNER_UNMASK
   ```
3. **Assemble Real In-Game Review `.mp4`:** Mux raw captured `mkxp-z` frames (`frames.tsv`) + actual game BGM/SE mix via `ffmpeg` into a clean review `.mp4` so the creator judges **100% authentic in-engine footage**, frame for frame!

---

### 4.5 Realistic Phased Production Rollout (Wave 0 → Wave 4)

| Wave | Scope | Art / Code Footprint | Verification Gate |
|---|---|---|---|
| **Wave 0 — Engine Sprint** *(Ready NOW for Claude — 0 New Art!)* | P0 `hitstop` deadlock fix, `bgm_cut`/`bgs_restore`, `012_Map_Camera.rb` (`map_zoom`/`pbZoomMap`), `012_Map_Acting.rb` (`act_play` event-swap + `map_light`), `012_Animated_Sequences.rb` (`play_movie` + `anim_cg_sequence`), `shatter_screen`/`glitch_tear`, battle-only `012_Anime_Juice.rb`, `selftest` | ~700–900 lines Ruby across 4 clean plugin modules + selftest checks | `selftest/suite.ruby_stub` 100% green + `capture.sh` smoke test |
| **Wave 1 — Vertical Slice Benchmark** *(1st Post-Quota-Reset Art Task)* | Build **ONE Peak Scene** end-to-end (**Peak #2 Ch9 Mourner Unmasking** on `Map 264` OR **Peak #1 Ch5 Vault Shatter `SH1`** on `Map 952→608`): bespoke acting sheets + 32–36f `.ogv` sakuga cut-in + synced dead-silence audio | 3 acting sheets (`act_ch9_*`) + 3 linked storyboard-grid sheets → `pf_ch9_unmasking.ogv` (+ `_safe.ogv`) | **Real `mkxp-z` `.mp4` capture signed off by Creator** ("YES, this is Rejuvenation V14 level!") before scaling |
| **Wave 2 — Acts I–II Complete** (`Ch0–Ch9`) | Remaining Peak #1 (`SH1` + Lowlight `608`) + all 8 standard chapters' live-map acting sheets & 16–20f `anim_cg_sequence` bursts | ~12 acting sheets + 8 short animated bursts + 1 Peak `.ogv` | Real `mkxp-z` capture reel of Act I–II |
| **Wave 3 — Acts III–V Complete** (`Ch10–Ch21`) | **Peak #3** (`Ch11 Kyogre Eye` + `Ch19 WAR-1` 4 sakuga cut-ins on `Map 926`) + **Peak #4** (`Ch21 Valen/Zygarde` + `18-Plate Arceus Convergence`) + all 10 standard chapters' live-map acting sheets & bursts (`RD-1`, Cathedral Echo, Zekrom, Aurelia) | ~16 acting sheets + 10 short animated bursts + 4 Peak `.ogv`s | Real `mkxp-z` capture reel of Acts III–V |
| **Wave 4 — Ruin Route Dark Mirror** (`R1–R7`) | **Peak #5** (`R7 Mirror-Pierce & Giratina 180° Inversion` — Prismfall's "Maria Impales Vitus" crown jewel) + R1 Graves Reflection, R3 Theodric Behind the Glass, R5 Ruin Dunes variant | 6 acting sheets + 2 short bursts + 1 Peak `.ogv` (`pf_ruin_mirror_pierce.ogv`) | Real `mkxp-z` capture reel of Ruin Route |

---

## Summary of Changes Required From Claude (Wednesday Sprint Checklist)

1. **`006_Scene.rb` + `012_Cinematic.rb` + `selftest/suite.ruby_stub`:** Fix `slowmo(0.0)` deadlock via `raw_dt` / `real_clock?`, add `hitstop(dur)`, add `bgm_cut` / `bgs_cut` + `bgs_memorize`/`bgs_restore`, expose `Scene#bar` for `010_Text.rb` safe-zone, add v4.3 audio aliases to `001_Config.rb`.
2. **New `012_Map_Camera.rb`:** Implement Rejuvenation V14 `pbZoomMap` / `map_zoom` / `map_pan` / `map_shake` via reused `Graphics.snap_to_bitmap` sprite over live `Spriteset_Map`.
3. **New `012_Map_Acting.rb`:** Implement `AdvancedAnimations`-style `act_play` (in-place `swap_event:` with arbitrary-grid foot-anchored sheets, variable `holds:`/`ticks:`, JSON sidecar support, inline `se:`/`hitstop:`/`shake:`/`flash:`/`fx:`, `after_graphic:` aftermath persistence) + `map_light` overlays + standalone `pf_act_event` & `\cutscene[ID]` / `[cutscene: ID]` event hooks.
4. **New `012_Animated_Sequences.rb`:** Implement MKXP-Z native `play_movie` (`.ogv` wrapper with `z=5002` skip HUD, map-swap `on_end`, `safe_movie:` photosensitive gate, `PF_NO_MOVIE` fallback) + native RGSS `anim_cg_sequence` (sequential `512×384` PNG folder / Omori packed atlas / MKXP-Z animated `Bitmap`, variable `holds:`, inline `hitstop:`/`se:`, preloaded & cleanly disposed) + scoped `shatter_screen` & `glitch_tear`.
5. **New `012_Anime_Juice.rb` (Battle & Chapter Cards ONLY):** Wire 31 existing `Graphics/EBDX/VS/*.png` busts into battle ace send-out / Mega / Z-Move / Shield Break `cutin_flash` + prismatic `chapter_card` — strictly separate from story cutscenes.
