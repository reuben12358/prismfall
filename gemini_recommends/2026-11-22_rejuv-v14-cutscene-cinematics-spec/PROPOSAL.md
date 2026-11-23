# Proposal: Full-Game 30-Moment Anime Cinematics Slate & `Prismfall Cutscenes` v2 Engine Architecture

- **Date:** 2026-11-22 *(Expanded per Creator Direction: Full 22-Chapter + 4-Scene Ruin Route 30-Moment Anime Slate + Reusable Anime Juice Layer)*
- **Author:** Gemini (Cutscene Director & Cinematics Architect)
- **Status:** Ready for Claude (Wednesday Engine Sprint) & Creator Review — zero edits made to `.rb`, `mapgen/`, `pbs/`, or `story/`
- **Interactive Companion Studio:** `prismfall_cutscene_director.html` (artifact in brain dir — filterable 30-moment full-game timeline + Everyday Anime Juice explorer + live 4:3 `512×384` 6-Technique Canvas Simulator)

---

## Executive Summary — The 3-Tier Production Pyramid + Everyday Anime Juice

Pokémon Prismfall already ships a clean, frame-rate-independent 60 FPS cutscene engine (`plugins/Prismfall Cutscenes/001..015`) with `flipbook`, `play_sheet`, `fx_sheet`, `still`, `pulse`, `on_map`, `impact_frames`, `fracture`, `rim`, `slowmo`, and `SheetBeamClash` (`design/CUTSCENE_RESEARCH.md`). Yet right now only **1** story scene (`:WAR_CLIMAX`, Ch19) is authored across a 22-chapter campaign + 7-chapter Ruin Route, and it lacks multi-layer anime CG compositing, sakuga impact frames synced to hitstop, Voronoi glass-shatter fractures, Ruin Route glitch-tears, and per-chapter anime moments.

To deliver the creator's vision — **"at least 1 memorable anime moment every chapter, multi-scene sakuga climaxes, and Rejuvenation V14 Renegade-level animation throughout the whole game"** — without creating an unbuildable art bottleneck, this blueprint uses a **3-Tier Production Pyramid** backed by a **Reusable "Everyday Anime Juice" Engine Layer**:

| Tier | Format & Target Runtime | Art Footprint per Scene | Coverage |
|---|---|---|---|
| **Layer 0 — Everyday Anime Juice** *(0 new art!)* | `cutin_flash` (`1.4s`), `chapter_card` (`2.8s`), `cine_bars` + `cam_zoom` | **0 new assets** — reuses all **31 already-built `Graphics/EBDX/VS/*.png` busts**, `band*`, `bolt0..2`, `spark`, and CC0 `VS Cutin Lightning.ogg`! | **100% of the 60-hr game:** all 22 + 7 chapter openings, every Warden/Boss Ace send-out, Mega, Z-Move, Shield Break & Prism Shift |
| **Tier 1 — Anime Key-Art Flash** | `12–18s` · 1–2 Pure-Gemini multi-layer CG plates + `sakuga_flash` / `cutin_flash` + letterbox + voice/SE + on-map handoff | `2–3` CG plates (`0–1` FX sheet) | **14 scenes** covering every standard chapter (`Ch0, Ch1, Ch3, Ch4, Ch6, Ch7, Ch8, Ch10, Ch12, Ch14 RD-1, Ch16, Ch17, Ch18, Ch20`) |
| **Tier 2 — Act Climax Setpiece** | `22–46s` · 3–5 split-layer parallax CGs + custom `4×4` acting sheets + additive VFX flipbooks + `shatter_screen` / `hitstop` | `3–5` CG plates + `1–2` sheets + `1` FX | **9 scenes** covering every Act Climax & multi-scene pivot (`Ch2, Ch5A SH1, Ch5B Lowlight, Ch9 Unmasking, Ch11 Kyogre Thaw, Ch13A Mindscape, Ch13B Fault, Ch15 Cathedral Echo, Ch19A Wyrmscar Oath`) |
| **Tier 3 — V14 Renegade Sakuga Finale** | `42–75s` · Multi-phase on-map + panoramic `768×576` parallax CGs + 2–4f B&W/chromatic `impact_cg` + Voronoi `shatter_screen` / `glitch_tear` + optional `.ogv` micro-clip | `4–5` CG plates + `1–2` sheets + `1–2` FX | **7 scenes** (`Ch19B WAR-1 v2`, `Ch21A Valen Zygarde Complete`, `Ch21B 18-Plate Arceus Convergence & Epilogue`, plus **4 dedicated Ruin Route Dark Mirror Renegade Cutscenes**) |

**Result:** **30 authored cinematic moments** (100% of Ch0–Ch21 + 4 Ruin Route setpieces) + **29 animated Chapter Eyecatch Cards** + **31-cast Anime Cut-In Eye-Flashes** phased into **4 clean asset rollout waves** (**Wave A: Ch0–Ch5 + Anime Juice = just 24 new assets** ready immediately after image quota resumes!).

---

## Part 1 — Engine Upgrade Spec for Claude (`Prismfall Cutscenes` v2, Wednesday Sprint)

All additions preserve 100% backwards compatibility with existing `:WAR_CLIMAX`, `:WAR_CLIMAX_DEMO`, `:WAR_CLIMAX_PROCEDURAL`, Festival Highlights (`011_Highlights.rb`), Portraits (`014_Portraits.rb`), and all existing `selftest/suite.ruby_stub` checks.

### 1.0 P0 Bugfix — `slowmo(0.0)` Hitstop Deadlock (`006_Scene.rb`, `012_Cinematic.rb`, `selftest/suite.ruby_stub`)

**Verified Root Cause:**
- `Scene#update(dt)` (`006_Scene.rb:201-217`) multiplies `dt *= @timescale` before `@time += dt`, and `op_slowmo` (`012_Cinematic.rb:544-550`) checks `lt >= @d` where `lt = @time - e.t0`.
- Calling `slowmo(0.0, duration: 0.14)` for anime hitstop freezes `@time` permanently — `lt` stays `0.0` forever and **deadlocks the scene**.
- `selftest/suite.ruby_stub:51` computes `e.dur * ((1.0 / e.args[:scale]) - 1)`, which raises `Infinity` / `ZeroDivisionError` at `scale == 0.0`.

**Fix Spec:**
1. **`006_Scene.rb`:** Capture `raw_dt = dt` and accumulate `@real_time += raw_dt` before `dt *= @timescale`. Expose `attr_reader :raw_dt, :real_time`. Allow effects implementing `def real_clock?; true; end` to advance on `raw_dt`. Reset `@timescale = 1.0` in `Scene#dispose`.
2. **`012_Cinematic.rb`:** Replace the anonymous class in `op_slowmo` with `class SlowmoEffect < Effect`:
   - `scale <= 0.001` defaults `real: true` (counts `@elapsed += scene.raw_dt`, restores `scene.timescale = 1.0` when `@elapsed >= @d`).
   - `scale > 0.001` defaults `real: false` unless `real: true` is passed — preserving legacy `:WAR_CLIMAX_DEMO` timings verbatim.
   - Add `Builder#hitstop(duration = 0.12, **o)` → `add(:slowmo, o.merge(:scale => 0.0, :real => true), duration, false)`.
3. **`selftest/suite.ruby_stub:51`:** Guard `slow` calculation for `real` / `scale <= 0.001`, and add a regression check asserting `hitstop(0.15)` completes cleanly in `~0.15s` real clock.

---

### 1.1 `cg_layer`, `cg_tween`, `cg_clear` — Multi-Layer Parallax Illustrated CG Compositing

**File:** New `012_CG_Layers.rb` + `Builder` methods in `003_DSL.rb`.

**Viewport & Z-Order Contract:**
`@viewport` (`z = 99_990`) holds world/actors/FX (`Z <= 2100`); `@ui` (`z = 99_991`) holds `Z_BARS = 100`, `Z_TEXT = 200`, `Z_CARD = 300`, `Z_FLASH = 500`, `Z_CURTAIN = 600`, `Z_SKIP = 700`.
Placing CG slots on **`@viewport` at `Z = 3000..3499`** guarantees CG plates sit **above** map/actors yet **below** widescreen bars, captions, title slams, flashes, Voronoi shards, and fade curtains — while inheriting `@viewport.tone` seamlessly:

```ruby
CG_SLOTS = { :bg => 3000, :mid => 3100, :char => 3200, :fg => 3300, :vfx => 3400 }

cg_layer :id,
  image:    "Graphics/Pictures/Cutscenes/cs05b_lowlight/char_dex_glassed",
  slot:     :char,             # :bg | :mid | :char | :fg | :vfx (or explicit z:)
  at:       [256, 192],        # screen-space center (default [256, 192])
  origin:   :center,           # :center | :top_left | [ox, oy]
  zoom:     1.0,               # smooth float Ken Burns zoom (not 1/16 quantized)
  rotate:   0.0,               # degrees
  opacity:  255,               # 0..255
  tone:     [0, 0, 0, 0],      # per-layer Tone [r, g, b, gray]
  blend:    :normal,           # :normal (0) | :add (1) | :sub (2)
  parallax: 0.0,               # couples to scene.camera (0.0 = locked; 0.2..1.0 = parallax)
  shake:    0.0,               # layer-local continuous jitter (px)
  clip:     nil,               # optional [x, y, w, h] integer src_rect crop (quadrant sheets!)
  wipe:     nil                # optional { dir: :left/:right/:up/:down, progress: 0.0..1.0 }

cg_tween :id,
  to: [220, 184], zoom: 1.16, rotate: 2.0, opacity: 255, tone: [-20, 0, 30, 0],
  wipe: { dir: :left, from: 0.0, to: 1.0 }, shake: 3.0, duration: 3.5, ease: :in_out, wait: false

cg_clear :id, fade: 0.35       # or cg_clear fade: 0.4, wait: true (clears all CG layers)
```

**Harness & Placeholder Contract:**
- Every `Sprite#x`, `#y`, `#z`, `#ox`, `#oy`, and `src_rect.set` MUST be strict `Integer` (`selftest/harness.ruby_stub:191-196`).
- If `Gfx.load_bitmap(path)` returns `nil`, auto-synthesize a crisp labeled dark-glass wireframe placeholder (`CG: cs05b/char_dex_glassed`) so all 30 scenes pass selftest & `--render` before Wave A–D art drops land.
- Track `@cg_ids` in `Builder` for author-time `ArgumentError` typo detection, and dispose all sprites & owned bitmaps in `Scene#dispose`.

---

### 1.2 `impact_cg` & `sakuga_flash` — Sakuga Impact Frames + Real-Clock Hitstop

```ruby
impact_cg images: ["Graphics/Pictures/Cutscenes/cs05a_spire/impact_01_bw",
                   "Graphics/Pictures/Cutscenes/cs05a_spire/impact_02_inv"],
          hold: 0.05, hitstop: 0.14, shake: 8, se: :field_shatter, wait: true

sakuga_flash style: :bw_invert, # :bw_invert | :chromatic | :crimson_void | :gold_flash
             frames: 3, hold: 0.045, hitstop: 0.12, chromatic: 6, shake: 6,
             se: :vs_lightning, wait: true
```
- **Photosensitive Gate (`Cutscene.photosensitive?`):** NEVER flashes full-screen B&W alternation! Automatically degrades to a single `0.18s` calm dark-vignette freeze (`opacity <= 55`, `shake * 0.2`, hitstop & SE kept intact).

---

### 1.3 `shatter_screen` & `glitch_tear` — Voronoi Glass Fracture & Ruin Route Corruption

```ruby
# Freezes Graphics.snap_to_bitmap into 16..32 scanline-blitted triangle shards on @ui!
shatter_screen origin: [256, 192], shards: 24, crack: 0.18, duration: 1.15,
               mode: :explode,          # :explode | :implode (Ruin R1) | :inverse (upward!) | :fall
               gravity: 640, edge: [232, 248, 255], se: :field_shatter, wait: false

# Zero-extra-bitmap-per-strip VHS/chromatic horizontal slice tear + optional inversion.
glitch_tear duration: 0.85, strips: 18, power: 28, chromatic: 6, invert: false,
            scanlines: true, freq: 24, target: :screen, se: :glass_quench, wait: false
```
- **`shatter_screen` Architecture:** Generates a deterministic `4×3` or `5×4` jittered grid (`scene.rng`), triangulates each quad (`24–32` triangles, zero gaps), holds `crack: 0.18s` with radiating white/prism fracture lines, then pre-cuts each triangle into its tight bounding-box `Bitmap` via 1px scanline `blt` rows (`< 8 ms` total at `512×384`) and disposes the snapshot. Because it runs non-blocking on `@ui`, the next CG/map swaps seamlessly underneath while the glass flies away!
- **`glitch_tear` Architecture:** 1 shared snapshot `Bitmap` (plus 1 optional inverted copy) sliced across `strips` sprites using integer `src_rect` bands + 2 additive R/C ghost sprites (`opacity = 95`). In `photosensitive?` mode: locks `freq <= 4 Hz`, disables rapid inversion strobing, caps ghost opacity at `55`.

---

### 1.4 `title_slam`, Enhanced `letterbox`, `play_movie` & Seamless Map Hooks

1. **`title_slam`** (`010_Text.rb`): Kinetic scale-slam (`zoom 2.3 → 1.0`, `:out_cubic`) + opposing kicker/subtitle ribbon + micro-shake (`style: :prism | :war | :ruin | :solemn`).
2. **Enhanced `letterbox` & Caption Safe-Zone (`006_Scene.rb:698`, `010_Text.rb:66-70`):** Add `ease:`, `color:`, `accent:` (1px luminous edge line), and clamp `Caption` inside `scene.bar_height + 6` so dialogue NEVER overlaps `40–44px` widescreen bars.
3. **`play_movie`** (`012_Cinematic_Techniques.rb`): Safe `Graphics.play_movie("Movies/...")` wrapper gated by `File.file?`, `!ENV["PF_NO_MOVIE"]`, and `!Cutscene.photosensitive?` (unless `*_safe.ogv` exists), with automatic fallback to `fallback_scene:` / `fallback:` CG sequence and `rescue StandardError`.
4. **Seamless Map Hook (`\cutscene[ID]` & `pf_cutscene`):** Add `def pf_cutscene(id, **vars)` alias in `003_DSL.rb`; intercept `\cutscene[ID]` / `\cutscene[ID,k=v]` in `014_Portraits.rb` (`pbMessageDisplay`) & `[cutscene: ID]` in `mapgen/layouts/scriptpour.py`; add `$game_system.bgs_memorize` / `bgs_restore` symmetry in `006_Scene.rb:192-194,740-743`; add v4.3 CC0 audio aliases (`:field_shatter`, `:boss_shield`, `:glass_quench`, `:prism_swell`, `:vs_lightning`, `:bgs_bleed`, `:bgs_harbor`, `:bgs_isenmar`, `:bgs_machinery`, `:bgs_drip`) in `001_Config.rb`.

---

### 1.5 NEW Layer 0 — Reusable "Everyday Anime Juice" Engine Layer (**0 New Art Assets!**)

Built as a lightweight module (`012_Anime_Juice.rb`) callable **both** inside cutscenes AND directly from battle / overworld scripts to multiply anime energy across the entire 60-hour campaign:

#### A. `cutin_flash` — Persona / Rejuvenation V14 Anime Eye-Flash & Bust Strip
- **Assets Reused (ALREADY ON DISK — 31/31 verified in `art/out/Graphics/EBDX/VS/`):**
  - All 31 pure-Gemini `256×136` transparent VS busts: `PLAYER_A`, `PLAYER_B`, `JUNO`, `KESTREL`, `LARCH`, `DORIAN`, `TAMSIN`, `MARISOL`, `ROOK`, `SAHAR`, `CORVIN`, `BRANN`, `KAITO`, `ANJA`, `ODESSA`, `ILSA`, `BASTIAN`, `YSOLDE`, `MAGNUS`, `NYX`, `CELESTINE`, `SIGRUN`, `VALEN`, `VOSS`, `MOURNER`, `MARCHETTI`, `KROLL`, `QUENT`, `SABLE`, `THISTLE`, `VESPER`!
  - All 8 speed-line bands (`bandplayer_<color>.png`, `bandfoe_<color>.png`), lightning overlays (`bolt0..2.png`), `spark.png`, and CC0 `Audio/SE/VS Cutin Lightning.ogg`!
- **DSL & Standalone Battle API:**
  ```ruby
  # Inside any cutscene OR standalone in battle/overworld:
  cutin_flash :SIGRUN,
              mode:  :eye_strip,     # :eye_strip (cropped 512x88 eye-flash bar!) | :full_bust (136px)
              side:  :right,         # :left (player/ally) | :right (foe/boss)
              color: :red,           # blue | gold | green | grey | red | rose | teal | violet
              line:  "Dragons weigh everything. Show me your truth!",
              se:    :vs_lightning,
              duration: 1.45
  ```
- **Automatic Battle Wiring Hooks (Claude Integration):**
  1. **Warden / Rival / Boss Ace Send-Out** (`010_Bridge_VersusIntro.rb` / `Battle#pbSendOut`) — `:eye_strip` flashes across screen center (`1.2s`) with character voice blip + ace quote!
  2. **Mega Evolution & Z-Move Activation** (`PrismfallMega` / `pbUseZMove`) — `:eye_strip` for PC (`PLAYER_A`/`PLAYER_B`) or Warden (`BASTIAN`, `JUNO`, `KESTREL`, `CELESTINE`, `VESPER`)!
  3. **Multi-Bar Boss Shield Break** (`005_Bosses_Effects.rb:51`) — pairs `Boss Shield Break.ogg` with a `0.9s` boss `:eye_strip` reaction flash!
  4. **Scripted Field Shatter / Prism Shift** (`003_Bridge_EBDX.rb:53` / `136_Field_PrismArena.rb:95`) — pairs `Field Shatter.ogg` / `Prism Arena Swell.ogg` with a `0.85s` cut-in!

#### B. `chapter_card` — Animated Prismatic Chapter Title Eyecatch (All 22 Main + 7 Ruin Chapters)
- ```ruby
  Prismfall::Cutscene.chapter_card(
    num: "CHAPTER 5", title: "TEN YEARS OF LIGHT", act: "ACT I — THE LAST FERRY",
    color: :electric, style: :prism, # :prism (main) | :ruin (inverted glitch for R1–R7)
    se: :prism_swell, duration: 2.8
  )
  ```
- Renders a live procedural 18-hue glass-prism wipe over a subtle dimmed snapshot of the entering map, sliding in the Act kicker, bold chapter numeral, title, and kingdom crest strip — zero extra PNGs required! Fires cleanly on chapter advance (`Prismfall::Story.advance_chapter`).

#### C. `cine_bars` & `cam_zoom` — Live Overworld Dynamic Camera Punch (Rejuvenation V14 `pbZoomMap` Style)
- ```ruby
  # Callable via script OR inline message tag \cine[on,1.15] ... \cine[off]:
  pf_cine_bars(true, height: 38, duration: 0.35, zoom: 1.15, target: :player)
  pf_cine_bars(false, duration: 0.35)
  ```
- Uses a persistent low-overhead `Viewport` (`VIEWPORT_Z - 5`) with smooth widescreen bars plus optional `1.12×–1.25×` `Graphics.snap_to_bitmap` zoom framing on dramatic overworld dialogue (just like Rejuvenation V14's `Scripts/Camera/pbZoomMap` documented in `design/CUTSCENE_RESEARCH.md:52`), gated cleanly by `Cutscene.photosensitive?` (disables micro-shake, keeps gentle letterbox).

---

## Part 2 — The Full 30-Moment Anime Cinematic Slate (Ch0–Ch21 + 4 Ruin Route)

### Master Slate Index & 4-Wave Asset Phasing

| # | Wave | Tier | Ch / Act | Scene ID | Title | Map ID(s) | Runtime | New Art (CG / Sheet / FX) |
|---:|---|---|---|---|---|---|---:|---|
| 1 | **Wave A** | Tier 1+ | Ch0 (Pro) | `:PRO_DOVETAIL_ARRIVAL` | *Eighteen Lights on the Strait* | `109`, `100` | `18s` | 3 CG / 1 Sheet / 1 FX |
| 2 | **Wave A** | Tier 1 | Ch1 (Act I) | `:CH1_GLASSED_ORCHARD` | *Through the Burning Veil* | `522`, `103` | `13s` | 2 CG / 0 Sheet / 0 FX |
| 3 | **Wave A** | **Tier 2** | Ch2 (Act I) | `:CH2_PAGEANT_MOURNER` | *Let the Land Grieve* | `145` | `28s` | 4 CG / 2 Sheet / 1 FX |
| 4 | **Wave A** | Tier 1 | Ch3 (Act I) | `:CH3_GLASS_MATRIARCH` | *Soothe or Silence* | `548` | `14s` | 2 CG / 0 Sheet / 0 FX |
| 5 | **Wave A** | Tier 1 | Ch4 (Act I) | `:CH4_NIGHT_EBB_STOPPED` | *The River Runs Both Ways* | `167` | `14s` | 2 CG / 0 Sheet / 0 FX |
| 6 | **Wave A** | **Tier 2** | Ch5A (Act I★) | `:CH5A_SPIRE_SHATTER` (`SH1`) | *Gala Breach & The Zap Plate Shatter* | `186`, `199`, `952` | `28s` | 3 CG / 1 Sheet / 1 FX |
| 7 | **Wave A** | **Tier 2** | Ch5B (Act I★) | `:CH5B_LOWLIGHT_TWELVE` | *Twelve in Glass & Valen's Uncovered Hand* | `608` | `24s` | 3 CG / 0 Sheet / 0 FX |
| 8 | **Wave B** | Tier 1 | Ch6 (Act II) | `:CH6_OSSUARY_MURALS` | *What the Sand Dug Up* | `625` | `13s` | 2 CG / 0 Sheet / 0 FX |
| 9 | **Wave B** | Tier 1 | Ch7 (Act II) | `:CH7_QUIET_WARD_NIGHT` | *They're Not Dying, They're Dreaming* | `223`, `220` | `14s` | 2 CG / 0 Sheet / 0 FX |
| 10 | **Wave B** | Tier 1 | Ch8 (Act II) | `:CH8_CALDERA_CRISIS` | *The Geothermal Tap & The Light Stone* | `255` | `14s` | 2 CG / 0 Sheet / 0 FX |
| 11 | **Wave B** | **Tier 2** | Ch9 (Act II★) | `:CH9_MOURNER_UNMASKED` | *Ironreach Conclave: Look at the Flowers* | `263` | `38s` | 3 CG / 1 Sheet / 1 FX |
| 12 | **Wave B** | Tier 1 | Ch10 (Act III) | `:CH10_OGERPON_GROVE` | *Guardian of the Bride Tree* | `294`, `708` | `14s` | 2 CG / 0 Sheet / 0 FX |
| 13 | **Wave B** | **Tier 2** | Ch11 (Act III★) | `:CH11_KYOGRE_THAW` | *When the Lake Breathes* | `309`, `300` | `34s` | 4 CG / 1 Sheet / 1 FX |
| 14 | **Wave B** | Tier 1 | Ch12 (Act III) | `:CH12_DEAD_LETTERS` | *Stormwatch Falls & The Late Reflection* | `746`, `740` | `14s` | 2 CG / 0 Sheet / 0 FX |
| 15 | **Wave B** | **Tier 2** | Ch13A (Act III★) | `:CH13A_MINDSCAPE_290` | *The Sealed Memory & First Words* | `344`, `354` | `28s` | 3 CG / 0 Sheet / 1 FX |
| 16 | **Wave B** | **Tier 2** | Ch13B (Act III★) | `:CH13B_GLASS_COURT_FAULT` | *The Tribunal & The Fault* | `343`, `348`, `355` | `32s` | 3 CG / 1 Sheet / 1 FX |
| 17 | **Wave B** | Tier 1+ | Ch14 (Act IV) | `:RD_1` | *The Ring Sings* *(Canon Storyboard)* | `363`, `783` | `14s` | 3 CG / 1 Sheet / 1 FX |
| 18 | **Wave C** | **Tier 2** | Ch15 (Act IV★) | `:CH15_CATHEDRAL_ECHO` | *AF 290 Through Morwen's Eyes & Giratina* | `394`, `806` | `46s` | 4 CG / 1 Sheet / 1 FX |
| 19 | **Wave C** | Tier 1+ | Ch16 (Act IV) | `:CH16_ZEKROM_CLEAR_AIR` | *Chains Broken / Operation Clear Air* | `403`, `223` | `16s` | 3 CG / 0 Sheet / 1 FX |
| 20 | **Wave C** | Tier 1+ | Ch17 (Act IV) | `:CH17_CRADLE_SINGS` | *The Missing Piece in Drowned Aurelia* | `826` | `16s` | 2 CG / 0 Sheet / 1 FX |
| 21 | **Wave C** | Tier 1 | Ch18 (Act V) | `:CH18_HYMN_OF_RETURN` | *Once Upon a Time: The Complete Hymn* | `845`, `443` | `14s` | 2 CG / 0 Sheet / 0 FX |
| 22 | **Wave C** | **Tier 2** | Ch19A (Act V★) | `:CH19A_WYRMSCAR_OATH` | *The Brazier Oath & Light Stone Awakening* | `864`, `865` | `22s` | 2 CG / 1 Sheet / 0 FX |
| 23 | **Wave C** | **Tier 3** | Ch19B (Act V★) | `:WAR_CLIMAX` (`WAR-1` v2) | *The Beam Clash on the Glass Dunes* | `926`, `929`, `888` | `68s` | 4 CG / 1 Sheet* / 1 FX* |
| 24 | **Wave C** | Tier 1+ | Ch20 (Act V) | `:CH20_FESTIVAL_EVE` | *Eighteen Plates, The Eye Opens & Torn Gauntlet* | `491`, `483` | `18s` | 3 CG / 0 Sheet / 0 FX |
| 25 | **Wave C** | **Tier 3** | Ch21A (Finale★) | `:CH21A_VALEN_ZYGARDE` | *Sovereign Valen: Crystal Arm & Zygarde Complete* | `491` | `46s` | 4 CG / 1 Sheet / 1 FX |
| 26 | **Wave C** | **Tier 3** | Ch21B (Finale★) | `:CH21B_ARCEUS_CONVERGENCE` | *18-Plate Arceus Convergence & Homecoming* | `491`, `294`, `608` | `74s` | 5 CG / 2 Sheet / 2 FX |
| 27 | **Wave D** | **Tier 3 (R)** | Ruin R1 | `:RUIN_R1_LOOK_BACK` | *Mirror-Shatter Divergence & 23 Graves* | `806` | `46s` | 4 CG / 2 Sheet / 1 FX |
| 28 | **Wave D** | **Tier 3 (R)** | Ruin R1–R2 | `:RUIN_R2_REFLECTION_DUEL` | *Mirror-Self Confrontation & The Black Case* | `806`, `403` | `42s` | 3 CG / 1 Sheet / 1 FX |
| 29 | **Wave D** | **Tier 3 (R)** | Ruin R3–R5 | `:RUIN_R3_THEODRIC_VOID` | *Dead King Behind the Glass & Ruin Dunes* | `826`, `962`, `926` | `54s` | 4 CG / 1 Sheet / 1 FX |
| 30 | **Wave D** | **Tier 3 (R)** | Ruin R7 | `:RUIN_R7_DISTORTION_FINALE` | *Giratina Inverted Arena, Judgment & Epilogue* | `491`, `963`, `106` | `64s` | 5 CG / 1 Sheet / 2 FX |

*\*Wave Totals: **Wave A** = 19 CG + 4 Sheets + 3 FX (**26 assets**); **Wave B** = 26 CG + 4 Sheets + 5 FX (**35 assets**); **Wave C** = 29 CG + 6 Sheets + 7 FX (**42 assets**, reusing all 35 `pfw_*` War sheets); **Wave D** = 16 CG + 5 Sheets + 5 FX (**26 assets**). Every Wave ships standalone as a complete playable Arc upgrade!*

---

### WAVE A — Prologue & Act I + Everyday Anime Juice (`Ch0–Ch5`, 7 Scenes)

#### #1 · `:PRO_DOVETAIL_ARRIVAL` — "Eighteen Lights on the Strait" *(Tier 1+ · Ch0 · Maps `109`, `100` · `18s`)*
- **Narrative Keys / Variants:** `PLAYER_A`/`PLAYER_B` silhouette; feeds into `:pro_fellowship` & `GO_HOMEWARD`.
- **Audio:** BGM `Intro - Last Ferry` (#76 *Mainland Dock*), BGS `Saltmere Harbor`, SE `Prism Arena Swell` (low pitch 75), `Glass Quench`.

| Shot # | Dur | Mode | Camera & Motion | Dialogue / Voice | VFX & Audio |
|---:|---:|---|---|---|---|
| 1 | `3.0s` | Title + Mist | Letterbox `42px`; opening date caption over drifting sea fog | *"Spring, AF 300. The Concert of Regions has sealed Velmora's borders. This is the final civilian crossing."* | `Saltmere Harbor` BGS + ship horn |
| 2 | `5.0s` | Multi-Layer CG | `768×576` horizontal Ken Burns pan over *Dovetail* bow; 18 spectral Imprint pillars glow across the Hallow Strait | Deckhand: "Used to only see the Imprints on a clear night. Now you see 'em through fog." | `Intro - Last Ferry`; additive 18-hue horizon shimmer; `Prism Arena Swell` |
| 3 | `4.0s` | Multi-Layer CG | Parallax push-in (`1.0→1.14`) on PC & Voss at the deck rail with chipped Meridian mug + `title_slam` | Voss: "First crossing? Everyone gets quiet when they see the lights." (`Voice - Voss`) | `title_slam style: :prism` *"THE LAST FERRY"* |
| 4 | `3.5s` | On-Map (`100`) | Cuts seamlessly to Ferrow's Landing customs gate; passengers scan green/blue; PC scans dead blank | Calla Wren: "...Wait. Step back through, please." | `cs_fx_scanner_sweep` additive curtain |
| 5 | `2.5s` | Glitch + Close CG | Close-up on brass CRT monitor reading `IMPRINT: NULL` (`glitch_tear power: 10`), Voss reflected smiling | Voss: "Faulty unit. These things hate sea air. Let them through, Calla." | `Glass Quench` ping; smooth handoff to Map `100` |

- **Assets (5):** `cs01_dovetail/{bg_strait_18lights,mid_ferry_rail,cg_scanner_null}.png`, `cs_voss_coat_acting.png`, `cs_fx_scanner_sweep.png`.

---

#### #2 · `:CH1_GLASSED_ORCHARD` — "Through the Burning Veil" *(Tier 1 · Ch1 · Maps `522`, `103` · `13s`)*
- **Narrative Keys / Variants:** Leads into `GO_ORCHARD` trap choice & first `:BLEED` Field Notes entry.
- **Audio:** BGM `Dungeon - Bleed Zones` (#74 *Distortion World Remix v2* soft), BGS `Glassfall Bleed`, SE `Glass Quench`, `Voice - Juno`, `Voice - Larch`.

| Shot # | Dur | Mode | Camera & Motion | Dialogue / Voice | VFX & Audio |
|---:|---:|---|---|---|---|
| 1 | `3.5s` | On-Map (`522`) | Map `522` Glassed Orchard edge; glass apples chime in wind; Juno jerks back from the shimmering Bleed Veil | Juno: "My skin's burning! How are you *doing* that?!" (`Voice - Juno`) | `Glassfall Bleed` BGS; `cutin_flash :JUNO` shock strip |
| 2 | `4.5s` | Multi-Layer CG | Slow dolly (`1.0→1.12`) as PC steps straight through the prismatic curtain untouched; a frantic glassed Wurmple calms at their boots | *(No dialogue — clear glass apples chiming softly)* | Additive Veil ripple + faint colorless sternum glow; `Glass Quench` |
| 3 | `2.0s` | On-Map Cut | Larch lowers her pen at the orchard fence, face unreadable | Larch: "Well. That's that, then." (`Voice - Larch`) | Quiet tone dim |
| 4 | `3.0s` | Cliffhanger CG | Night cut to Tidewatch Station (`103`): oil-lamp close-up of Larch's open journal handwriting | *(Caption)* *"Subject reads NULL. Second such reading in my life. Crownhaven, AF 290. God help us, Ines."* | Flame flicker layer; stepped fade to black |

- **Assets (2):** `cs01b_orchard/{cg_veil_crossing,cg_larch_journal}.png`.

---

#### #3 · `:CH2_PAGEANT_MOURNER` — "Let the Land Grieve" *(Tier 2 Climax · Ch2 · Map `145` · `28s`)*
- **Narrative Keys / Variants:** Reads `:ch3_juno_talk` (Juno's reaction beat if she knows about `NULL`).
- **Audio:** BGM `Town - Elowen` (#6) → dead silence → `Theme - Hollow` (#82 *Music: Xen Base*), SE `Crowd gasp`, `Field Shatter`, `Beam break`, `Voice - Mourner`, `Voice - Juno`.

| Shot # | Dur | Mode | Camera & Motion | Dialogue / Voice | VFX & Audio |
|---:|---:|---|---|---|---|
| 1 | `4.0s` | On-Map (`145`) | Warm lamplit Lantern Theatre stalls; three hound-masked actors chase the painted Ogre across stage | Child: "Is that the Ogre? He's early!" | Warm gold tint; pageant BGM cuts dead |
| 2 | `2.5s` | Sakuga + Hitstop | Lights snap dead; `sakuga_flash :bw_invert` (`hitstop: 0.12`); hall desaturates to cold ash grey | — | `Crowd gasp`; total vacuum silence |
| 3 | `6.5s` | Multi-Layer CG | Painted Plates backdrop splits vertically (`wipe: :up`); **The Mourner** steps through in ash-bark mask holding a single white lily | Mourner: "Three hundred years of pageantry. Ask your Warden why nothing in Verdance ever rots." (`Voice - Mourner`) | `Theme - Hollow`; `title_slam style: :solemn` *"THE MOURNER"*; falling ash petals |
| 4 | `4.5s` | Multi-Layer CG + Hitstop | Juno's hand clutches her never-wilting wreath; diagonal cut to **Thistle** snipping the curtain fly-rope with weaver's shears (`hitstop: 0.10`) | Mourner: "Ask why the Loyal Three wore poison on their collars. Let the land grieve." | `Field Shatter` rope snap; Bereaved banners drop from rafters |
| 5 | `5.5s` | Extreme Close CG | Hard zoom (`1.0→1.26`) straight into the Mourner's carved eye-slits locking onto the PC; single heartbeat `pulse` | Mourner: "...You." | Heartbeat `pulse`; colorless glint at PC's chest |
| 6 | `5.0s` | On-Map + FX | Map `145`: Mourner erupts into billowing `cs_fx_cotton_spore` and vanishes; Bereaved grunts rush the aisle! | Juno: "He sounded sad. Isn't that weird? I thought he'd sound evil." (`Voice - Juno`) | `Beam break`; seamless drop into Ch2 double battle |

- **Assets (7):** `cs02_pageant/{bg_torn_backdrop,char_mourner_mask,char_juno_wreath_clutch,cg_mourner_eyes_lock}.png`, `cs_mourner_cloak.png`, `cs_thistle_shears.png`, `cs_fx_cotton_spore.png`.

---

#### #4 · `:CH3_GLASS_MATRIARCH` — "Soothe or Silence" *(Tier 1 · Ch3 · Map `548` · `14s`)*
- **Narrative Keys / Variants:** Fires on `:ch2_matriarch` (`:soothe` vs `:silence` — player's first Harmony vs Ruin visual payoff!) + Briarwick chapel Crown mural beat.
- **Audio:** BGM `Mood - Mystery` (#77) → `Glassfall Bleed` BGS, SE `Glass Quench`, `Boss Shield Break`, `Voice - Tamsin`.

| Shot # | Dur | Mode | Camera & Motion | Dialogue / Voice | VFX & Audio |
|---:|---:|---|---|---|---|
| 1 | `3.5s` | On-Map (`548`) | Cocoonfall Hollow crystal web nest; beaten giant glassed **Galvantula** thrashes, raining prism shards onto silk-moth cocoons | Tamsin: "If it keeps thrashing, the whole grove goes to glass!" (`Voice - Tamsin`) | `shake power: 4`; crystal sparks |
| 2 | `6.0s` | Branch CG (`cg_layer`) | **`:soothe`:** Warm dawn timelapse CG as PC sits beside the trembling Galvantula until morning calms it (half the grove frozen in glowing crystal). **`:silence`:** Stark cyan-to-grey CG as PC presses palm to its brow — **the Imprint drains out like water down a drain**, leaving the grove safe and the Matriarch dull-eyed & hollow! | Tamsin (`:silence`): "Oh. Oh, that's — thank you. I think." | `:silence` fires subtle `glitch_tear power: 8` + `Glass Quench` pitch-drop (Ruin −2 tell!) |
| 3 | `4.5s` | Cliffhanger CG | Briarwick chapel mural of the Sovereign's Crown — whole in old paint, circled with a missing chip in charcoal on the Festival poster beside it; PC's hand rises unprompted to their chest | Child: "Mum says the Crown got hurt once. How do you hurt a crown?" | Slow push-in on missing chip; single soft glass ping |

- **Assets (2):** `cs03_briarwick/{cg_matriarch_drain,cg_wounded_crown_mural}.png`.

---

#### #5 · `:CH4_NIGHT_EBB_STOPPED` — "The River Runs Both Ways" *(Tier 1 · Ch4 · Map `167` · `14s`)*
- **Narrative Keys / Variants:** Sets up `:ch4_teo` (`:report` / `:keep_secret` / `:confront`) & Larch's Chief Engineer confession.
- **Audio:** BGM `Mood - Tension` (#78), BGS `Saltmere Harbor` → roar, SE `Beam break`, `Field Shatter`, `Voice - Marisol`, `Voice - Larch`.

| Shot # | Dur | Mode | Camera & Motion | Dialogue / Voice | VFX & Audio |
|---:|---:|---|---|---|---|
| 1 | `3.5s` | On-Map (`167`) | Midnight on Ebbmouth Mill Quay; the river freezes eerie dead-still, mill-wheels halted mid-drip; distant Lattice intake **explodes**! | Marisol: "NO — there's a kid in a punt out on the race!" (`Voice - Marisol`) | `sakuga_flash :gold_flash` on explosion; `Beam break` |
| 2 | `6.0s` | Multi-Layer CG | Dynamic anime splash CG: a raging black tidal bore thunders toward the Mill race as **PC, Marisol, and masked Teo Reyes** throw their combined weight onto the rusted iron sluice-gate wheel, slamming it shut inches before the punt! | Teo: "Pull, damn it — PULL!" | `hitstop(0.10)` as gate locks; foreground spray pan; `cutin_flash :MARISOL` |
| 3 | `4.5s` | Close CG + Cut | Mask slips in lantern-light revealing 19-year-old Teo's face; Marisol lets go of his sleeve so he can run — then Meridian spotlights sweep over her and the PC | Meridian Guard: "Warden! Who blew that intake?" | Searchlight sweep `wipe`; feeds straight into `:ch4_teo` |

- **Assets (2):** `cs04_ebbmouth/{cg_sluice_gate_surge,cg_teo_lantern_slip}.png`.

---

#### #6 · `:CH5A_SPIRE_SHATTER` (`SH1`) — "Gala Breach & The Zap Plate Shatter" *(Tier 2 Multi-Scene Climax · Ch5 · Maps `186`, `199`, `952` · `28s`)*
- **Narrative Keys / Variants:** Bridges Gala raid (`186`) into the multi-bar Bleed Electivire boss (`:NEON_GRID` → `:BLEED`) and `GO_LIVE_WIRE`.
- **Audio:** BGM `Theme - Meridian` (#81 *ARCHETYPE*) → `Mood - Tension` (#78) → detonation vacuum silence, BGS `Machinery - Zenith`, SE `Boss Shield Break`, `VS Cutin Lightning`, `Field Shatter`, `Voice - Voss`, `Voice - Mourner`.

| Shot # | Dur | Mode | Camera & Motion | Dialogue / Voice | VFX & Audio |
|---:|---:|---|---|---|---|
| 1 | `5.5s` | On-Map + Parallax CG | Map `186` Meridian Spire Gala Hall; airships pass windows; behind glass shaft (`199`) the **Dark Stone core** pulses like a slow black breath during Voss's toast | Voss: "Light is work. Every lamp in this city was lit by someone told to be grateful for the dark." (`Voice - Voss`) | `Theme - Meridian`; subtle black pulse inside core shaft |
| 2 | `4.5s` | On-Map Raid (`186`→`952`) | Gala chandeliers flicker black; Hollow blasts open Nadir service lifts; rapid cut down to Map `952` Plate Vault as **Sable** darts out and slaps a **Splitter** charge onto the Zap Plate! | Mourner: "No — no — what did you *do*?!" (`Voice - Mourner`) | `cs_sable_splitter` acting sheet; `cutin_flash :SABLE` + `:MOURNER` |
| 3 | `5.0s` | Close CG + Hitstop | Close-up CG: the Mourner catches the cracking Zap Plate barehanded; violet lightning spiderwebs across his smoking right glove; `hitstop(0.14)` as the Splitter hits zero! | — | `Boss Shield Break` + `Beam charge` rising whine; `cs_fx_bleed_lightning` |
| 4 | `3.5s` | **3-Frame Sakuga Impact (`impact_cg`)** | (1) Stark B&W ink silhouette of the Vault exploding, (2) inverted electric-violet Plate fracture, (3) blinding white spire-wide shockwave! | — | `impact_cg` (`hold: 0.055`, `hitstop: 0.14`, `shake: 10`); `VS Cutin Lightning` + `Field Shatter` |
| 5 | `9.5s` | **Voronoi Glass Shatter (`shatter_screen`)** | Vault freezes and **shatters into 28 flying Voronoi shards** (`mode: :explode`), revealing a wave of violet-prismatic Bleed sweeping outward across Lumen's dark lower shadow-district — then snaps back to the cracked Vault as an overcharged **Bleed Electivire** drops in front of the door! | Rook: "Don't touch the Plate with your hands!" (`Voice - Rook`) | `shatter_screen shards: 28, crack: 0.20`; `:NEON_GRID` → `:BLEED` flip into multi-bar boss! |

- **Assets (5):** `cs05a_spire/{cg_mourner_glove_burn,impact_01_bw,impact_02_violet_inv}.png`, `cs_sable_splitter.png`, `cs_fx_bleed_lightning.png`.

---

#### #7 · `:CH5B_LOWLIGHT_TWELVE` — "Twelve in Glass & Valen's Uncovered Hand" *(Tier 2 Multi-Scene Climax · Ch5 · Map `608` · `24s`)*
- **Narrative Keys / Variants:** Leads straight into `:ch5_lowlight_testimony` (`:mourner` / `:second_figure` / `:unknown`) and Interlude I (*Lamplight*).
- **Audio:** BGM `Mood - Farewell` (#79 *Resting Grounds*), BGS `Glassfall Bleed`, SE `Glass Quench`, `Voice - Rook`, `Voice - Valen`.

| Shot # | Dur | Mode | Camera & Motion | Dialogue / Voice | VFX & Audio |
|---:|---:|---|---|---|---|
| 1 | `9.5s` | Panoramic Multi-Layer CG | Slow, devastating Ken Burns pull-back (`1.24→1.0`) across Map `608` **Shattered Lowlight**: laundry frozen rigid, laughing bystander, center-frame **11-year-old Dex frozen mid-wave in translucent prismatic glass** with his Fizzbolt crate on his hip | *(Faint echo caption)* "Tell you the rest tomorrow!" | `Mood - Farewell` enters solo piano; `Glassfall Bleed` BGS; floating prismatic dust |
| 2 | `6.5s` | Multi-Layer CG | Camera drops behind PC walking cleanly through the burning Bleed Veil while Rook and bystanders recoil; Rook's Rotom lens trembles and drops | Rook: "...Turn it off. Rotom. Turn it *off*." (`Voice - Rook`) | `Glass Quench` warm resonant chime; Veil parts around PC's boots |
| 3 | `8.0s` | Close CG + On-Map + Title | Sovereign **Valen** arrives at the Veil's edge, peels off his grey glove for one beat — revealing **pale crystal creeping across his knuckles** — then locks eyes on the PC standing untouched *inside* the glass | Valen: "You were in the Lowlight when it went? And you're... standing." (`Voice - Valen`) | `title_slam style: :solemn` *"END OF ACT I"* / sub: *"II — IMPRINTS"* |

- **Assets (3):** `cs05b_lowlight/{bg_lowlight_alley,char_dex_glassed,cg_valen_crystal_knuckles}.png`.

---

### WAVE B — Acts II–III & Ch14 Ring-Day (`Ch6–Ch14`, 10 Scenes)

#### #8 · `:CH6_OSSUARY_MURALS` — "What the Sand Dug Up" *(Tier 1 · Ch6 · Map `625` · `13s`)*
- **Narrative Keys / Variants:** Awards **Duneholt Rubbing**; feeds straight into **K3** & `:ch6_kestrel_rumor`.
- **Audio:** BGM `Dungeon - Ruins` (#65 *Ancient Ruins*), SE `Prism Arena Swell` (low), `Glass Quench`, `Voice - Sahar`, `Voice - Kestrel`.

| Shot # | Dur | Mode | Camera & Motion | Dialogue / Voice | VFX & Audio |
|---:|---:|---|---|---|---|
| 1 | `3.5s` | On-Map (`625`) | Torchlight hits the Script Vault inside the giant fossil skull; **Unown** drift off the stone walls spelling *THE CALLING* | Sahar: "I buried this once because Valen told me to. I won't argue with sand twice." (`Voice - Sahar`) | Floating Unown motes; `Glass Quench` |
| 2 | `6.5s` | Scrolling CG (`768×576`) | Continuous horizontal pan across **Four Carved Sandstone Murals** lighting in gold: (1) Gilded King Theodric, (2) Red & Blue Titans (*Year of Two Weathers*), (3) 18-lock Chain binding a radiant beast, (4) The beast shattering into rain over a drowning city! | *(No dialogue — echoing desert wind & rising choir pad)* | `Prism Arena Swell` low brass bloom; additive gold inlay glow |
| 3 | `3.0s` | Cut-In + Map | Camera whips to the archway: **Kestrel** standing in the sunlight over the PC's shoulder, jaw set | Kestrel: "My mother had a seat and a Plate. Then nothing. Let *what* go?" (`Voice - Kestrel`) | `cutin_flash :KESTREL`; seamless drop into K3 |

- **Assets (2):** `cs06_ossuary/{bg_four_murals_scroll,fg_unown_glyphs}.png`.

---

#### #9 · `:CH7_QUIET_WARD_NIGHT` — "They're Not Dying, They're Dreaming" *(Tier 1 · Ch7 · Maps `223`, `220` · `14s`)*
- **Narrative Keys / Variants:** Creator-approved *Ward Night* beat (`story/05_ACT_II.md:89`); seeds Homecoming waking & Hammer schism.
- **Audio:** BGM `Town - Nadir` (#37) → hard cut → `Mood - Tension` (#78) → `Mood - Emotion` (#80), BGS `Drip - Nadir` → `Glassfall Bleed`, SE `Glass Quench`, `Voice - Corvin`, `Voice - Juno`.

| Shot # | Dur | Mode | Camera & Motion | Dialogue / Voice | VFX & Audio |
|---:|---:|---|---|---|---|
| 1 | `4.0s` | Glitch Broadcast CG | Every neon screen in Mirefen (`220`) tears with `glitch_tear`: unmasked **Sable** smiling cheerfully before power dies | Sable: "The Mourner's gone soft. The Hammer hasn't. Cindervault's next." | `glitch_tear power: 18`; Infirmary lamps snap dark |
| 2 | `6.0s` | Multi-Layer CG | Inside Corvin's Infirmary (`223`), a Bleed Veil slams across the Quiet Ward door; PC steps straight through and lifts **9-year-old Ama** (salt-crystal hair) — macro zoom catches **her eyes moving peacefully under clear salt**! | *(Whisper)* "Under the salt, she's watching something." | `Glass Quench` gentle harmonic; Juno's peat-stills hiss outside |
| 3 | `4.0s` | On-Map Roof | Mirefen roof at dawn with bog coffee; Corvin lowers his plague half-mask | Corvin: "Nobody in my Ward is dead. They're *dreaming*. Two's a study." (`Voice - Corvin`) | Morning blue-marsh glow; Hammer graffiti fades in |

- **Assets (2):** `cs07_mirefen/{cg_sable_broadcast,cg_ama_dreaming_salt}.png`.

---

#### #10 · `:CH8_CALDERA_CRISIS` — "The Geothermal Tap & The Light Stone" *(Tier 1 · Ch8 · Map `255` · `14s`)*
- **Narrative Keys / Variants:** Reflects `:ch8_caldera` (`:vent` `:VOLCANIC`→`:ASHEN_WASTE` / `:dampers` / `:force`) & introduces **Sigrun Ashfall** + `:ch8_lightstone`.
- **Audio:** BGM `Route - Ashkaar` (#46) → `War - Frontlines` (#84), BGS `Lava - Ashkaar`, SE `Field Shatter`, `Beam fire`, `Voice - Sigrun`, `Voice - Brann`.

| Shot # | Dur | Mode | Camera & Motion | Dialogue / Voice | VFX & Audio |
|---:|---:|---|---|---|---|
| 1 | `4.0s` | On-Map (`255`) | Cindervault Tap Chamber; Meridian's geothermal tap spikes white-hot magma skyward while Quent giggles behind his dials | Quent: "Oh, the null reading! Hold still, I've only got one probe!" (`Voice - Quent`) | `Lava - Ashkaar`; `shake power: 5`; `cutin_flash :QUENT` |
| 2 | `5.0s` | Branch CG (`cg_layer`) | `:vent` opens Lake Sallow floodgates — explosive hiss of white steam turns molten caldera to grey ash (`:ASHEN_WASTE`); `:dampers`/`:force` clamps the crimson tap under roaring embers | Brann: "Some things you forge to *break* right — that's the harder craft." (`Voice - Brann`) | `sakuga_flash :gold_flash` + steam/ash wave wipe |
| 3 | `5.0s` | Hero Entrance CG | Dominar's envoys grab for the **Light Stone** — a roaring **Salamence** dives out of the caldera smoke as **Sigrun Ashfall** leaps down between them, dragonhide cloak flaring! | Sigrun: "So you're the ferry child. Hm. Smaller than I expected." (`Voice - Sigrun`) | `cutin_flash :SIGRUN` (`color: :red`); war-drums swell |

- **Assets (2):** `cs08_cindervault/{cg_caldera_quench,cg_sigrun_salamence_drop}.png`.

---

#### #11 · `:CH9_MOURNER_UNMASKED` — "Ironreach Conclave: Look at the Flowers" *(Tier 2 Act II Climax · Ch9 · Map `263` · `38s`)*
- **Narrative Keys / Variants:** Reads `:ch7_ledger` (Juno reaction) & `:ch6_kestrel_rumor` (Kestrel line); feeds directly into `:ch9_teo_sable` (`TEO_SAVED` vs `IRONREACH_EVIDENCE`).
- **Audio:** BGM `Battle - Mourner` (#114 *Ana's Lament*) → cut on mask split → `Mood - Farewell` (#79), BGS `Glassfall Bleed`, SE `Field Shatter`, `Beam break`, `Crowd gasp`, `Voice - Juno`, `Voice - Kestrel`, `Voice - Mourner`.

| Shot # | Dur | Mode | Camera & Motion | Dialogue / Voice | VFX & Audio |
|---:|---:|---|---|---|---|
| 1 | `5.0s` | On-Map (`263`) | Iron Pit upper ring; Hammer Splitter explodes on Fist Plate reliquary; `:BLEED` crystal races across stone toward Juno shielding Nell | *(Roaring crystal crack)* | `fracture` cracks race toward Juno; `shake power: 7`; `Field Shatter` |
| 2 | `4.5s` | Multi-Layer CG + FX | Colossal roots of **Trevenant** smash up through the Pit floor walling off Juno; the Mourner leaps squarely into the Bleed path! | — | `cs_trevenant_wall` sheet + `cs_fx_root_erupt` flipbook |
| 3 | `3.5s` | **Sakuga Impact + Hitstop (`impact_cg`)** | Crystal blast slams the Mourner's face; `hitstop(0.14)` → B&W sakuga frame showing the **ash-bark mask cracking straight down the bridge**! | — | `impact_mask_split_bw` + `shatter_screen mode: :fall, shards: 18`; `Beam break` |
| 4 | `9.0s` | **Slow-Mo Multi-Layer CG** | `slowmo(0.22, duration: 1.5)` — tumbling mask halves pass foreground, revealing **Rowan Ashby's** bleeding, half-glassed face and scarred palm | Juno: "...Uncle Rowan?" / Rowan: "Don't look at me like that. Look at the flowers. Look at what they're standing on." | `Battle - Mourner` cuts dead; white lily falls in foreground; `Crowd gasp` |
| 5 | `6.5s` | On-Map + Cut | Cut across Pit to **Kestrel**, hand frozen over Honedge's hilt, all vengeance draining out of his eyes | Kestrel: "...It's not her." (`Voice - Kestrel`) | `Mood - Farewell` enters; Kestrel walks into mine shadows |
| 6 | `9.5s` | On-Map Decision Handoff | PC steps into the Bleed untouched to pull Rowan upright under Valen's stare — then camera whips left to **Teo pinned under glassing scaffolding** and right to **Sable sprinting for the Meridian lift**! | *(Immediate handoff into `:ch9_teo_sable` major choice)* | Colorless sternum aura glows on PC |

- **Assets (5):** `cs09_unmasking/{impact_mask_split_bw,bg_pit_trevenant_roots,char_rowan_unmasked}.png`, `cs_trevenant_wall.png`, `cs_fx_root_erupt.png`.

---

#### #12 · `:CH10_OGERPON_GROVE` — "Guardian of the Bride Tree" *(Tier 1 · Ch10 · Maps `294`, `708` · `14s`)*
- **Narrative Keys / Variants:** Leads into `:ch10_ogre` (`OGERPON_TRUSTED` vs `GO_LOYAL`), J3 Gym 9, and optional **Venam's Testimony** under the Bride Tree.
- **Audio:** BGM `Town - Verdance` (#9) → `Boss - Pecharunt & Loyal Three` (#130), BGS `Gossamer Deepwood`, SE `Prism Arena Swell`, `Voice - Juno`.

| Shot # | Dur | Mode | Camera & Motion | Dialogue / Voice | VFX & Audio |
|---:|---:|---|---|---|---|
| 1 | `4.0s` | Multi-Layer CG (`294`) | Verdance drowning in unrotting roses around the towering flowering **Bride Tree** (Aunt Elin's silhouette in petals); Juno holds Rowan's sealed Warden's ring trembling | Juno: "I didn't want this seat. I wanted *him* in it." (`Voice - Juno`) | Drifting endless rose petals; grey sterile soil foreground |
| 2 | `6.0s` | Hero Reveal CG (`708`) | Down in the sunken Bride Grove roots, poison-pink collars glow on **Okidogi, Munkidori & Fezandipiti** — then **Ogerpon** drops from the Bride Tree boughs in its Teal Mask, cudgel blazing emerald between them and the Meadow Plate! | *(Ogerpon cry — resonant wooden mask chime!)* | `sakuga_flash :chromatic` emerald spark; `title_slam style: :prism` *"THE GOSSAMER OGRE"* |
| 3 | `4.0s` | On-Map Handoff | Ogerpon looks back over its shoulder at the PC, extending a branch-hand — straight into `:ch10_ogre` & triple-boss! | — | `Boss - Loyal Three` (#130) slams in |

- **Assets (2):** `cs10_verdance/{cg_bride_tree_bloom,cg_ogerpon_mask_stand}.png`.

---

#### #13 · `:CH11_KYOGRE_THAW` — "When the Lake Breathes" *(Tier 2 Act III Kaiju Climax · Ch11 · Maps `309`, `300` · `34s`)*
- **Narrative Keys / Variants:** Leads into `GO_WEATHER`, `101_Boss_Kyogre.rb`, `:ch11_anja`, and ignites the Ashkaar–Isenmar War.
- **Audio:** BGM `Mood - Tension` (#78) → `Boss - Kyogre` (#125), BGS `Wind - Isenmar` → `Rain`, SE `Field Shatter`, `Beam charge`, `VS Cutin Lightning`, Kyogre cry, `Voice - Anja`, `Voice - Juno`.

| Shot # | Dur | Mode | Camera & Motion | Dialogue / Voice | VFX & Audio |
|---:|---:|---|---|---|---|
| 1 | `5.0s` | On-Map (`309`) | Sinking Quarter at night; Meridian heat-towers spike red; black `fracture` webs race under stilt-houses | Anja: "Get off the lower ice! NOW!" (`Voice - Anja`) | `fracture`; `Field Shatter`; `shake power: 4` |
| 2 | `5.5s` | Multi-Layer CG | Top-down looking straight through black lake ice beneath PC's boots — total quiet — then a **colossal bioluminescent blue eye** opens slowly in the abyss! | Juno: "...Did the lake just blink?" (`Voice - Juno`) | `Wind - Isenmar` cuts; sub-bass `Beam charge` pitch 55 |
| 3 | `3.0s` | **Sakuga + Upward Shatter** | `sakuga_flash :chromatic` (`hitstop: 0.14`) → `shatter_screen mode: :inverse, shards: 26` blasts ice slabs skyward! | — | `VS Cutin Lightning` + `Field Shatter` |
| 4 | `9.0s` | Panoramic Multi-Layer CG | Vertical Ken Burns tilt-up (`768×576`) of **Primal Kyogre** breaching through Rimeholt's broken harbour, cyan Alpha-markings blazing through sleet! | — | `Boss - Kyogre` (#125); `Rain` BGS; `title_slam style: :war` *"THE SLEEPING WHALE"* |
| 5 | `5.5s` | Close CG | Kyogre's vast head tilts fractionally toward the tiny PC on the floe; Primal rain turns indigo | *(Field Notes)* "It looked at me as if I were very small and very familiar." | Cyan rim glow answers PC's colorless sternum glint; Kyogre cry |
| 6 | `6.0s` | On-Map (`309`) | Cuts to flooded `:WATER_SURFACE` harbour as Anja shouts toward the heat-tower deck | Anja: "When the lake breathes, you RUN! Get to the towers!" | `cutin_flash :ANJA`; drops straight into `GO_WEATHER` / Kyogre boss |

- **Assets (6):** `cs11_thaw/{cg_abyss_eye_under_ice,bg_rimeholt_storm,char_kyogre_breach,fg_ice_spray}.png`, `cs_kyogre_eye_water.png`, `cs_fx_tidal_splash.png`.

---

#### #14 · `:CH12_DEAD_LETTERS` — "Stormwatch Falls & The Late Reflection" *(Tier 1 · Ch12 · Maps `746`, `740` · `14s`)*
- **Narrative Keys / Variants:** Leads into **Marchetti** raid (`MERIDIAN_MARCHETTI`), **K5** (`:ch12_letter`), and seeds Antumbra / Ruin Route reflection horror.
- **Audio:** BGM `Dungeon - Sky Tower` (#69) → `Battle - Marchetti` (#117 *Madame X Duel*), SE `Beam break`, `VS Cutin Lightning`, `Glass Quench`, `Voice - Larch`, `Voice - Odessa`.

| Shot # | Dur | Mode | Camera & Motion | Dialogue / Voice | VFX & Audio |
|---:|---:|---|---|---|---|
| 1 | `5.0s` | Multi-Layer CG (`746`) | Midnight broadcast from Stormwatch Spire Roof across every screen in Velmora — Kroll's Splitter detonates the relay mast in orange fire as **Odessa's skiff** dives into the Stormfront lightning (brief silhouette of **Zekrom** flashing in the thunderclouds!) | Larch: "I designed the Lattice. I was wrong. I'm telling you now because nobody else will." (`Voice - Larch`) | `sakuga_flash :bw_invert` on lightning Zekrom silhouette; `Beam break` + `VS Cutin Lightning` |
| 2 | `4.0s` | Cut-In + Map | Sorting-hall catwalks: Marchetti raises her Lattice-glass keystone wrist-band; Mart terminal pings `FELLOWSHIP: SUSPENDED` | Marchetti: "You're not under arrest. You're under *protection*." | `cutin_flash :MARCHETTI` (`color: :violet`) |
| 3 | `5.0s` | Cliffhanger Glitch CG (`740`) | Rainwater puddle on Conductors' Causeway: PC walks out of frame — **their reflection stays put for 0.5 seconds, blinks slowly, then walks off late**! | — | Subtle `glitch_tear power: 10`; eerie detuned `Glass Quench` |

- **Assets (2):** `cs12_skyreach/{cg_stormwatch_zekrom_flash,cg_puddle_late_reflection}.png`.

---

#### #15 · `:CH13A_MINDSCAPE_290` — "The Sealed Memory & First Words" *(Tier 2 Multi-Scene Climax · Ch13 · Maps `344`, `354` · `28s`)*
- **Narrative Keys / Variants:** Fires on `:ch13_remember` (`:show_me` / `:scared_too`; if `:not_yet`, deferred to Ch15); **first authored PC dialogue in the game!**
- **Audio:** BGM `Boss - Mindscape Nightmare` (#124 *VS! Master of Nightmares* intro) → `Mood - Farewell` (#79), SE `Glass Quench`, `Field Shatter`, `Voice - Ilsa`, `Voice - Player`.

| Shot # | Dur | Mode | Camera & Motion | Dialogue / Voice | VFX & Audio |
|---:|---:|---|---|---|---|
| 1 | `5.0s` | On-Map (`344`) → Inversion | Ilsa pulls off her earmuffs in the Athenaeum cloister; screen ripples into upside-down white-and-violet Mindscape | Ilsa: "Someone sealed a memory in you. A Ghost-type. I can open it. I won't enjoy it." (`Voice - Ilsa`) | `glitch_tear power: 14`; `cs_fx_memory_shatter` violet wave |
| 2 | `7.0s` | Multi-Layer CG | Dream-Crownhaven, AF 290: the **5-year-old PC** stands holding a Choir ribbon under floating bells; first authored PC choice fires mid-scene! | Child: "Mum's singing. Do you want to see the light? It's going to hurt." / PC: **"Show me."** / **"I'm scared too."** | Warm sepia-to-white light bloom; slow push-in |
| 3 | `8.5s` | **Fractured Memory Montage (`cg_layer` + `impact_cg`)** | Rapid fragmented flashes: Ines singing, white-robed **Valen** under a blazing Crown, brass Meridian machines behind the loft, a blinding *CRACK* into the child's chest, **Morwen's black veil** diving over them, and a **Mismagius** drawing the memory shut like a violet curtain! | Man's voice: *"Find the child."* | `hitstop(0.12)` + `sakuga_flash :bw_invert`; `Field Shatter` |
| 4 | `7.5s` | On-Map + Close Cut | Snaps back to Map `344`; Ilsa is pale white, hands shaking beside her earmuffs | Ilsa: "The man in white was my father. The truth is a weapon. Don't mistake sheathing it for mercy." | `cutin_flash :ILSA`; quiet piano fade |

- **Assets (4):** `cs13a_mindscape/{bg_dream_crownhaven_290,char_child_pc_ribbon,cg_mismagius_curtain}.png`, `cs_fx_memory_shatter.png`.

---

#### #16 · `:CH13B_GLASS_COURT_FAULT` — "The Tribunal & The Fault" *(Tier 2 Multi-Scene Climax · Ch13 · Maps `343`, `348`, `355` · `32s`)*
- **Narrative Keys / Variants:** Reads `:ch13_kaito` (`KAITO_TESTIFIED`), `IRONREACH_EVIDENCE` (Kroll exposed publicly!), and feeds straight into **major life-or-death choice `:ch13_fault`** (Rowan vs Marchetti).
- **Audio:** BGM `Battle - Tribunal Ambush` (#118 *Pursuit ~ Wanting to Find the Truth*) → `Mood - Tension` (#78), BGS `Glassfall Bleed`, SE `Crowd gasp`, `Field Shatter`, `Beam break`, `Voice - Kaito`, `Voice - Ilsa`.

| Shot # | Dur | Mode | Camera & Motion | Dialogue / Voice | VFX & Audio |
|---:|---:|---|---|---|---|
| 1 | `6.0s` | On-Map + Cut-Ins (`348`) | Glass Court Tribunal: Kaito confesses Marrowgate (`"They were still knocking."`); if `IRONREACH_EVIDENCE`, Ilsa reads the court and names **Sabine Kroll**! | Ilsa: **"Sable is Sabine Kroll. Meridian Special Accounts."** | `cutin_flash :KAITO` + `:KROLL`; `Crowd gasp`; `Pursuit` BGM |
| 2 | `6.0s` | **Global Tremor CG (`cg_layer`)** | Cut across Velmora at dusk: beneath Cogsworth, the **Arbiter Engine** test-fires a pulse hitting all 18 Plates — a shockwave races across the map, **draining Zenith's Sump** overnight to expose **drowned Aurelia's golden spires**! | — | Deep sub-bass rumble; `cs_fx_fault_shockwave` ripple across terrain |
| 3 | `4.5s` | **Voronoi Glass Shatter (`shatter_screen`)** | Back in Map `348`: the Glass Court's soaring stained windows **explode inward** (`shatter_screen shards: 26`); the stone floor collapses into the flooding Undercroft (`355`)! | — | `hitstop(0.14)` + `Field Shatter` + `Beam break`; roaring floodwater |
| 4 | `9.5s` | Split Crisis CG (`cg_layer`) | Flooding Undercroft: left frame, **Rowan** chained to the sinking dock as dark water climbs to his chin; right frame, the giant brass orrery ring pinning **Director Marchetti**! *(Triggers `:ch13_fault`!)* | Rowan *(if saved)*: "Ask the Drowned Crown. It's awake now. So are you." | Rapid rising water overlay; urgent heartbeat `pulse` |
| 5 | `6.0s` | Cliffhanger CG (`343`) | Dawn on shattered Athenaeum steps; Ilsa hands over Valen's Secret Articles — behind her, reflected inside every broken shard of glass, **six colossal black wings slowly unfold** (Giratina seed)! | Ilsa: "Go find Bastian Ore first. He was *there*." | `title_slam style: :solemn` *"END OF ACT III"* / sub: *"IV — THE DROWNED CROWN"* |

- **Assets (5):** `cs13b_fault/{cg_aurelia_sump_drains,cg_undercroft_dilemma,cg_six_wings_glass_shards}.png`, `cs_kroll_gallery_leap.png`, `cs_fx_fault_shockwave.png`.

---

#### #17 · `:RD_1` — "The Ring Sings" *(Tier 1+ Canon Storyboard · Ch14 · Maps `363`, `783` · `14s`)*
- **Narrative Keys / Variants:** Exact canon storyboard from `story/13_CUTSCENES.md:80-96` inside hidden Trials quest `OS_RING_DAY` (`\cutscene[RD_1]`); `skippable: false`; `PLAYER_A`/`PLAYER_B` palm/sleeve variant. *(Optional 4s post-gym Duneholt Undersands `783` Groudon seismic-wake mini-flash shares `cs_fx_prism_fan_18`!)*
- **Audio:** BGM fades cleanly to silence (zero music sting by canon rule); subtle lamp/kettle tone; SE `Glass Quench` (pitched sustained glass-rim note), `Prism Arena Swell` (whisper-quiet vol 35).

| Shot # | Dur | Mode | Camera & Motion | Dialogue / Voice | VFX & Audio |
|---:|---:|---|---|---|---|
| 1 | `3.0s` | Close Multi-Layer CG | Seamless cut from Map `363` lamp-room into warm amber close-up of PC's open palm; Bastian's plain gold ring drops into palm and settles | — | BGM fades out (`0.8s`); warm lamplight flicker on gold band |
| 2 | `4.0s` | Macro CG + Additive Prism | Push-in (`1.0→1.32`) on colorless Crown-stone chip — it catches lamplight and **breaks into eighteen hairline rainbow rays** fanning out (20f) and back to clear (20f)! | — | `cs_fx_prism_fan_18` additive flipbook; pure sustained `Glass Quench` harmonic |
| 3 | `3.5s` | Mid CG + `pulse` | PC's hand goes to their sternum; a **single colorless star-pulse** flashes under the coat (1 bright frame, 30f fade) as every miner's lamp flares at once and the room desaturates 30% and returns! | — | `pulse tone: [-10,-10,-10,90], duration: 0.9`; `Prism Arena Swell` vol 35 |
| 4 | `3.5s` | On-Map (`363`) | Smooth fade back to Map `363` three-shot: Pip jumps off crate; half-deaf Bastian lays palm flat on trembling table; Larch lowers her book by the door | *(Resumes live dialogue: `[portrait: PIP, shocked] Grandad. Grandad, it's SINGING.`)* | Glass note fades under kettle hiss; zero-flicker return |

- **Assets (5):** `cs14_rd1/{bg_lamproom_table,cg_palm_gold_ring,cg_sternum_star}.png`, `cs_bastian_pip_larch_rd1.png`, `cs_fx_prism_fan_18.png`.

---

### WAVE C — Late Act IV & Act V Sakuga Finales (`Ch15–Ch21`, 9 Scenes)

#### #18 · `:CH15_CATHEDRAL_ECHO` — "AF 290 Through Morwen's Eyes & Giratina's Door" *(Tier 2 Act IV Climax · Ch15 · Maps `394`, `806` · `46s`)*
- **Narrative Keys / Variants:** Reads `:ch13_remember` & `:ch12_letter`; feeds into **K6**, **Morwen's Ring**, **Giratina**, and the **Ruin Route Look Back? (`:ch15_look_back`)** gate!
- **Audio:** BGM `Boss - Echo of Morwen` (#131 *Leader Angie*) → `Mood - Farewell` (#79), BGS `Glassfall Bleed`, SE `Beam break`, `Field Shatter`, `Crowd gasp`, `Glass Quench`, `Voice - Ysolde`, `Voice - Kestrel`.

| Shot # | Dur | Mode | Camera & Motion | Dialogue / Voice | VFX & Audio |
|---:|---:|---|---|---|---|
| 1 | `5.0s` | On-Map + Glitch (`394`) | Kestrel slams his Meridian Gauntlet onto the Spooky Plate altar; violet `glitch_tear` rips across the candles | Ysolde: "Not like this. She made me swear — when you were ready—" (`Voice - Ysolde`) | `glitch_tear power: 18`; altar blazes violet |
| 2 | `8.0s` | Multi-Layer CG | Full AF 290 replay through **Morwen's eyes**: Crownhaven bells, Ines singing, Valen in white, and behind the loft **young Aurelian Voss** smiling as Meridian brass dials jump! | — | `title_slam style: :solemn` *"MEMORY ECHO — AF 290"*; sepia-violet tone |
| 3 | `4.5s` | **Sakuga Impact + Hitstop** | Cathedral bell shatters! `hitstop(0.16)` + `impact_crown_crack`: the Crown fractures and shoots a blinding colorless splinter into the 5-year-old PC's chest! | — | `impact_cg` + `Beam break` + `Boss Shield Break` |
| 4 | `9.5s` | **Glass Shatter + Multi-Layer CG** | `shatter_screen` freezes 40 onlookers in crystal; **Morwen** throws her black Ghost Warden veil over the child while Valen blazes white on the dais | Valen (echo): "**Find the child.** Whatever it costs." / Morwen (vestry): "Kestrel. I'm sorry." | `shatter_screen shards: 24`; `Crowd gasp`; `Mood - Farewell` solo |
| 5 | `7.0s` | Extreme Close CG | Dead silence. Morwen's translucent ghost turns impossibly across ten years to face the **present-day PC** directly before dissolving into pale moths | Morwen (echo): "Little one. You came back. I told her not to let you." | `Glass Quench`; spectral dispersion particles |
| 6 | `6.0s` | On-Map Rage (`394`) | Kestrel's Gauntlet overloads with `:BLEED` sparks; he turns furiously on the PC (into K6!) | Kestrel: "My whole life for you... And she was saving *YOU*." (`Voice - Kestrel`) | `cutin_flash :KESTREL`; `cs_kestrel_gauntlet_surge` |
| 7 | `6.0s` | Post-Barrow Hook (`806`) | *(Optional part-2 trigger at Barrow door)* A barrow opens *downward into an upside-down sky* as wounded **Giratina** glides forward, looking at the PC with ancient recognition! | *(Caption)* "It has been guarding the hole your god left for three hundred years." | Giratina cry; feeds into `:ch15_look_back` Ruin gate! |

- **Assets (6):** `cs15_cathedral/{bg_crownhaven_290_loft,impact_crown_crack,char_morwen_shield,cg_morwen_turn_gaze}.png`, `cs_kestrel_gauntlet_surge.png`, `cs_fx_echo_curtain.png`.

---

#### #19 · `:CH16_ZEKROM_CLEAR_AIR` — "Chains Broken / Operation Clear Air" *(Tier 1+ · Ch16 · Maps `403`, `223` · `16s`)*
- **Narrative Keys / Variants:** Sets `ZEKROM_FREED` (`:ch16_zekrom`), reflects `:ch16_magnus`, and stages **Interlude IV (*Clear Air* — Wenlow's unpreventable sacrifice)**.
- **Audio:** BGM `Boss - Zekrom` (#127 *Mechanical Rhythm*) → hard cut to dead silence, BGS `Machinery - Zenith`, SE `Boss Shield Break`, `VS Cutin Lightning`, single stark gunshot SE.

| Shot # | Dur | Mode | Camera & Motion | Dialogue / Voice | VFX & Audio |
|---:|---:|---|---|---|---|
| 1 | `6.0s` | Multi-Layer CG + Sakuga (`403`) | Final golden Lattice cable snaps (`hitstop: 0.12`, `sakuga_flash :bw_invert`); **Zekrom** spreads blue-plasma wings and blasts vertically straight through Strade Works' steel foundry roof into the Stormfront! | Magnus *(winding pocket watch)*: "The math was beautiful. The alternative was the Bleed." | `cs_fx_zekrom_plasma`; `Boss Shield Break` + `VS Cutin Lightning` + Zekrom cry |
| 2 | `4.0s` | Broadcast Glitch CG | Night screens across Cogsworth flash **"OPERATION CLEAR AIR"** as white-and-gold Directorate dropships descend into Nadir's lifts | Worker: "My mum lives down there." | `glitch_tear power: 10`; cold blue broadcast tint |
| 3 | `6.0s` | Stark Interlude Finale (`223`) | Candlelit doorway of Mirefen's Quiet Ward: 17-year-old **Wenlow** stands spread-armed between Directorate rifles and 40 dreaming patients — **hard cut to pure black** | Wenlow: "This is a hospital. You have to—" *(Hard cut to black. Single gunshot SE. 2.5 seconds of total silence.)* | Zero music; starkest moral floor in Act IV |

- **Assets (4):** `cs16_cogsworth/{cg_zekrom_roof_breach,cg_clear_air_screens,cg_wenlow_doorway}.png`, `cs_fx_zekrom_plasma.png`.

---

#### #20 · `:CH17_CRADLE_SINGS` — "The Missing Piece in Drowned Aurelia" *(Tier 1+ · Ch17 · Map `826` · `16s`)*
- **Narrative Keys / Variants:** Names the **Legend Plate** splinter; feeds directly into `:ch17_voss_offer` (`:refuse` / `:feign` / `:accept`) & Brann's confession.
- **Audio:** BGM `Dungeon - Drowned Aurelia` (#71 *Miracle Sea*) → `Theme - Meridian` (#81), SE `Prism Arena Swell`, `Glass Quench`, `Voice - Nyx`, `Voice - Voss`.

| Shot # | Dur | Mode | Camera & Motion | Dialogue / Voice | VFX & Audio |
|---:|---:|---|---|---|---|
| 1 | `6.5s` | Multi-Layer CG (`826`) | Drowned Aurelia Sun Court beneath green seawater: the **Keystone Cradle** (a golden open hand the size of a door) wakes — the PC's chest **blazes through their shirt** lighting the submerged temple in 18 spectral colors! | Nyx: "Oh. Oh, darling. You're the missing piece." (`Voice - Nyx`) | `cs_fx_cradle_18hue` radial bloom; `Prism Arena Swell` + `Glass Quench` |
| 2 | `4.5s` | Close Caption | Sahar traces the golden inscription beneath the hand | Sahar: *"Here rests the One that is every color and none."* — A splinter of the Legend Plate! | Slow golden glow pulse |
| 3 | `5.0s` | Breach + Reveal CG | Plasma torch cuts through the far vault wall; **Aurelian Voss** strides into the air-pocket helmet-off, gold sunburst glinting | Voss: "House Aurel. My family. Stand with me at the Festival — I can fix the god." (`Voice - Voss`) | `cutin_flash :VOSS` (`color: :gold`); feeds into `:ch17_voss_offer` |

- **Assets (3):** `cs17_aurelia/{cg_cradle_18_colors,cg_voss_sun_court_breach}.png`, `cs_fx_cradle_18hue.png`.

---

#### #21 · `:CH18_HYMN_OF_RETURN` — "Once Upon a Time: The Complete Hymn" *(Tier 1 · Ch18 · Maps `845`, `443` · `14s`)*
- **Narrative Keys / Variants:** Completes **Hymn of Return** Key Item (blazing gold if Wick's verse / Maren's page collected); bridges into **K7** & `:ch18_kestrel_ring`.
- **Audio:** BGM `Town - Gloaming` (#10) → `Mood - Theme of Hope` (#80), SE `Glass Quench`, `Prism Arena Swell`, `Voice - Celestine`, `Voice - Kestrel`.

| Shot # | Dur | Mode | Camera & Motion | Dialogue / Voice | VFX & Audio |
|---:|---:|---|---|---|---|
| 1 | `3.5s` | Quick Payoff Cut (`845`) | Lightless Deep pink crystal shatters after **Pecharunt** falls; Sweetrot thralls blink awake across Nadir | *(Caption)* "The pageants had it backwards for 250 years." | `Field Shatter`; pink mist clears |
| 2 | `6.5s` | Multi-Layer CG (`443`) | Gloaming's dusk-chapel inside the Great Tree's roots: barefoot **Celestine** raises her hands among floating lantern-moths as golden script weaves the **final verse of the Hymn of Return** into the air! | Celestine: *"Not chained, not broken, not bought, not crowned: given back, as a gift is found."* (`Voice - Celestine`) | `Mood - Theme of Hope` (#80); golden twilight petals & fairy shimmer |
| 3 | `4.0s` | Skiff Drop + Cut-In | A Directorate skiff rips down through the canopy — **Kestrel** leaps onto the roots barring the road to Crownhaven! | Kestrel: "Stay out of Crownhaven and let me end it!" (`Voice - Kestrel`) | `cutin_flash :KESTREL`; feeds into K7 & `:ch18_kestrel_ring` |

- **Assets (2):** `cs18_gloaming/{cg_celestine_hymn_chapel,fg_golden_hymn_script}.png`.

---

#### #22 · `:CH19A_WYRMSCAR_OATH` — "The Brazier Oath & Light Stone Awakening" *(Tier 2 Pre-War · Ch19 · Maps `864`, `865` · `22s`)*
- **Narrative Keys / Variants:** Fires on `:ch19_oath` (`:return` / `:keep` / `:open` / `:ruin` vs `GO_LIARS_PYRE`) and leads overnight into the **Glass Dunes**.
- **Audio:** BGM `Dungeon - Cinderhorn` (#67) → `Boss - Reshiram` (#128 *Ultra Necrozma Remix* intro), BGS `Lava - Ashkaar`, SE `Beam break`, `VS Cutin Lightning`, Reshiram cry, `Voice - Sigrun`.

| Shot # | Dur | Mode | Camera & Motion | Dialogue / Voice | VFX & Audio |
|---:|---:|---|---|---|---|
| 1 | `6.0s` | On-Map (`864`→`865`) | Walking Wyrmscar Rift's dragonfire bridge; Sigrun confesses letting Valen search for the PC so she wouldn't have to wear the Crown | Sigrun: "For two years I knew, and I let it happen, because it meant it wasn't me." (`Voice - Sigrun`) | Rising ash embers; warm fire rim-lighting |
| 2 | `5.0s` | Close Brazier CG | PC steps to the Draco Plate oath-brazier and speaks their true intention (`:ch19_oath`); white dragonfire leaps cleanly up instead of burning them! | PC: **"I'm going to give them back."** *(or chosen oath)* | `hitstop(0.10)` + white flame flare |
| 3 | `6.5s` | **Light Stone Awakening CG** | The ancestral **Light Stone** cracks open in blinding blue-white fire — **Reshiram** unfolds colossal feathered wings across the Rift cavern and bows its head silently to **Sigrun**! | Sigrun: "...It chose the one who finally said it out loud." | `sakuga_flash :gold_flash`; `Beam break`; Reshiram cry; `cs_reshiram_bow` |
| 4 | `4.5s` | War Dispatch Cut | A rider bursts into the Rift: *Kyogre has dragged the Northern Sea into the desert!* Sigrun vaults onto Salamence toward the burning western horizon | Sigrun: "Climb on! We fly to the dunes tonight!" | `title_slam style: :war` *"THE GLASS DUNES AWAIT"* |

- **Assets (3):** `cs19a_wyrmscar/{cg_oath_brazier_flame,cg_reshiram_bows_sigrun}.png`, `cs_reshiram_bow.png`.

---

#### #23 · `:WAR_CLIMAX` (`WAR-1` v2 Full Anime Upgrade) — "The Beam Clash on the Glass Dunes" *(Tier 3 Finale · Ch19 · Maps `926`, `929`, `888` · `68s`)*
- **Narrative Keys / Variants:** Full v2 upgrade of `013_Scenes_War_OnMap.rb`! Supports `:A` (`WAR_STOPPED`), `:A2` (`WAR_BOTH_BROKEN`), `:B` (`WAR_ASHKAAR_WON`), `:C` (`WAR_ISENMAR_WON`), **`variant: :R` (NEW Ruin Route R5 Void-Eat!)**, and `legends: false` (`:war_legend == :neither`). Also adds a crisp `6s` post-Gym-18 tag (*All 18 Badges Sing a Chord* → Sovereign's Ascent / Glassfall Scar `888`).
- **Audio:** BGM `War - Battlefield` (#84/#120) → `War - Beam Clash` (#121 *Rogue Mega Rayquaza Remix*) → `War - Aftermath` (#85 *Through the Sea of Time Orchestral*), BGS `War - Distant Battle` / `Rain`, SE `Beam charge/fire/clash/break`, `Field Shatter`, `Glass Quench`, `Crowd gasp`.

| Shot # | Dur | Mode | Camera & Motion | Dialogue / Voice | VFX & Audio |
|---:|---:|---|---|---|---|
| 1 | `5.5s` | On-Map Stage (`926`) | Existing 64×24 Glass Dunes pan across Isenmar ice-sledges, bone-carters' white banner, Ashkaar dragon-riders + kinetic `title_slam` | — | `title_slam style: :war` *"THE BEAM CLASH ON THE GLASS DUNES"*; `War - Battlefield` |
| 2 | `7.5s` | On-Map Flood → **CG Cut-In** | Existing `pfw_fx_flood` pours over dunes; at breach, snaps into **1.8s anime CG** of Primal Kyogre erupting through bone-sand surf before returning to map | Eirik: "Isenmar! The sea has come to the sand!" | `Rain` BGS; Kyogre cry; cyan rim flash |
| 3 | `6.5s` | On-Map Light Stone → **CG Cut-In** | Hrothgar cracks the Light Stone; cuts to **1.8s anime CG** of Reshiram unfolding over crimson banners as rain hisses into steam | Hrothgar: "Then let it remember fire." | `Beam break`; Reshiram cry |
| 4 | `4.0s` | **NEW Diagonal Split-Screen Anime CG** | Vertical lightning-seam split! Left: Primal Kyogre gathering sapphire **Origin Pulse**; Right: Reshiram igniting blue-white **Blue Flare** turbine over glowing sand! | — | `cg_kyogre_reshiram_split`; rising `Beam charge` |
| 5–6 | `8.0s` | **3-Frame Sakuga `impact_cg` + Hitstop + `SheetBeamClash`** | Both fire! On collision: `hitstop(0.14)` + **3-frame B&W/cyan/orange sakuga impact plate** → `slowmo(0.22, duration: 0.45)` → live `SheetBeamClash` grinding over vitrifying sand! | — | `War - Beam Clash` (#121); `impact_clash_sakuga_bw`; `Beam clash`; ramped flashes + glass-ring decal |
| 7–8 | `8.5s` | On-Map Wave-Glassing + Bleed Dome | Breaking wave sets into glass mid-curl (`pfw_fx_glass_wave`); both front ranks thrown flat; bone-carters' white banner glasses under expanding Bleed dome | Soldier: "The Steamline! It's coming this way!" | `Crowd gasp`; `Field Shatter` |
| 9–10 | `8.0s` | Approach → **NEW Hero Low-Angle CG** | PC walks into dome (`:A`/`:A2`/`:R`), rides Salamence (`:B`), or rides Marisol's sled-boat (`:C`); cuts to dramatic low-angle CG raising one glowing hand beneath twin arching beams (`:R` activates pitch-black *None* void!) | Sigrun (`:B`): "Hold on!" / Marisol (`:C`): "Tides take it, kid, *now*!" | `cs_pc_shard_raise`; `:R` triggers `glitch_tear invert: true` + `cs_fx_void_eat` |
| 11–12 | `7.0s` | Resolution (`shatter_screen` for `:A2` / Void for `:R`) | `:A`/`:B`/`:C`: clash collapses into one silent mote; legends bow & depart. `:A2`: `shatter_screen` white-out breaks both hosts. `:R`: beams devoured black; both legends **flee in terror**! | Field Notes: "It looked at me as if I were very small and very familiar. Again." | `Glass Quench`; snow falls on glass; `War - Aftermath` (#85) |
| 13–15 | `13.0s` | Aftermath + Mesa (`929`) + Sunrise + 18-Chord | Truce (`:A`), lone rulers (`:A2`), victor banners (`:B`/`:C`); Dr. Quent packing tripod on Map `929` mesa; bone-carters raising new banner at dawn | Quent: "Lovely reading." / Larch (radio): "That wasn't a battle to them. That was a *reading*." | Sunrise tone `[36,14,-10,40]`; smooth stepped fade out |

- **Assets (6 NEW; reuses all 35 existing `pfw_*` assets):** `cs19b_war_v2/{cg_kyogre_reshiram_split,impact_clash_sakuga_bw,cg_pc_under_beams,cg_ruin_void_collapse}.png`, `cs_pc_shard_raise.png`, `cs_fx_void_eat.png`.

---

#### #24 · `:CH20_FESTIVAL_EVE` — "Eighteen Plates, The Eye Opens & Torn Gauntlet" *(Tier 1+ · Ch20 · Maps `491`, `483` · `18s`)*
- **Narrative Keys / Variants:** Day 1 Opening Ceremony (`:ch16_rook` = hold triggers Rook's live screen hijack!), Day 5 *Night of Masques*, and Day 6 **K8 Semifinal** (`KESTREL_REDEEMED` vs `KESTREL_FALLEN`).
- **Audio:** BGM `Theme - Accord` (#83) → `Battle - Kestrel K8` (#97), SE `Prism Arena Swell`, `Crowd cheer`, `Crowd gasp`, `Voice - Valen`, `Voice - Voss`, `Voice - Kestrel`.

| Shot # | Dur | Mode | Camera & Motion | Dialogue / Voice | VFX & Audio |
|---:|---:|---|---|---|---|
| 1 | `6.0s` | Multi-Layer CG (`491`) | Dusk procession: **all 18 Wardens** place their Plates into the Concordance Ring; **Valen** removes his grey glove exposing his crystal arm; 18-color dome ripples across Crownhaven's sky! | *(Choir chime — forty thousand spectators hush)* | `Prism Arena Swell` + `Crowd gasp` |
| 2 | `5.0s` | **White-Out Vision CG (`cg_layer`)** | PC's sternum flares — world flashes pure white — a **colossal luminous Eye with 18 empty wheel-slots** opens directly over the lens (*plus Rook's Rotom screen hijack if `:ch16_rook == :hold`!*) | Arceus (vision): *"...Little light. You have carried me far."* | `sakuga_flash :gold_flash`; ethereal `Glass Quench` chord |
| 3 | `7.0s` | Dual Pre-Final Highlights (`483` / `491`) | Quick split flash: (A) Basilica Close (`483`) — Dorian's banned *"Gilded King"* play as Voss stands applauding alone (*"Bravo."*). (B) Semifinal (`491`) — **Redeemed Kestrel** tears off his glowing Meridian Gauntlet and hurls it across the stone (*"Not like this!"*) — OR **Fallen Kestrel's** arm scorches in overload! | Voss: "Bravo. They finally cast the king correctly." / Kestrel: "If I beat you, I beat *you*." | `cutin_flash :VOSS` → `cutin_flash :KESTREL` |

- **Assets (3):** `cs20_festival/{cg_18_plates_procession,cg_arceus_eye_vision,cg_kestrel_gauntlet_tear}.png`.

---

#### #25 · `:CH21A_VALEN_ZYGARDE` — "Sovereign Valen: Crystal Arm & Zygarde Complete" *(Tier 3 Finale Part 1 · Ch21 · Map `491` · `46s`)*
- **Narrative Keys / Variants:** Supports `VALEN_COLLAPSED` fallback (Sigrun or Brann takes the field while Valen watches from stretcher), `ILSA_RECONCILED`, and `:ch21_crown` (`:kneel` / `:stand` / `:step_back`).
- **Audio:** BGM `Battle - Sovereign Valen` (#136 *Reborn Champion Theme*) → `Victory - Sovereign`, SE `Prism Arena Swell`, `Beam charge`, `Beam fire`, `Field Shatter`, `Crowd cheer`, `Voice - Valen`, `Voice - Ilsa`.

| Shot # | Dur | Mode | Camera & Motion | Dialogue / Voice | VFX & Audio |
|---:|---:|---|---|---|---|
| 1 | `7.0s` | On-Map + Entrance CG (`491`) | Dawn floods the packed Meridian Prism Arena; **Sovereign Valen** steps onto the Altar Stage with **no glove at all**, pale crystal glowing from wrist to shoulder beneath white robes | Valen: "Come on, then. Show me there's another door." (`Voice - Valen`) | `title_slam style: :prism` *"SOVEREIGN VALEN CORRIGAN"*; `cutin_flash :VALEN` (`color: :gold`) |
| 2 | `7.5s` | Multi-Layer CG | Mid-Final climax cut-in: as the arena cycles fields, translucent **crystal creeps visibly up Valen's collarbone to his throat** while hundreds of emerald **Zygarde Cells** storm inward from every corner of Crownhaven! | Ilsa *(stands, if reconciled)*: "Father, *stop*!" (`Voice - Ilsa`) | `cs_fx_zygarde_cells` converging additive swirl; `Glass Quench` sharp crackle |
| 3 | `5.0s` | **Sakuga Impact + Hitstop (`impact_cg`)** | `hitstop(0.14)` → 2-frame emerald-and-white sakuga impact: **Zygarde Complete Forme** towers over the stadium and fires **Core Enforcer**, carving a blazing emerald **`Z`** clean across the arena floor! | Valen: "Order, not justice. I chose order." | `impact_core_enforcer_bw`; `Beam fire` + `Field Shatter`; `shake power: 8` |
| 4 | `11.5s` | Panoramic Battle CG | Multi-layer parallax showdown: PC's ace lunging through emerald crystal dust against Zygarde Complete under all 18 cycling Plate lights — culminating in Zygarde kneeling and Valen catching himself on one knee, smiling gently | Valen: "Velmora has a new champion." | `Battle - Valen` resolves into `Crowd cheer` roar |
| 5 | `15.0s` | Coronation → **Hijack Alarm (`shatter_screen`)** | Inside the Concordance Ring, Valen lifts the **Sovereign's Crown** over the PC's head (`:ch21_crown`) — the instant the Crown lowers, **all 18 Plates scream in dissonance**, golden locks erupt up every pylon, and the arena floor fractures open beneath the **Arbiter Engine's golden Keystone Cradle**! | Voss *(descending in Engine harness)*: "You carried my key through eighteen doors. Let me show you what it opens." (`Voice - Voss`) | `Prism Arena Swell` warped → `Boss Shield Break`; `cs_valen_crown_lift`; leads directly into `:CH21B`! |

- **Assets (6):** `cs21a_valen/{cg_valen_crystal_throat,impact_core_enforcer_bw,bg_prism_arena_dawn,char_zygarde_complete}.png`, `cs_valen_crown_lift.png`, `cs_fx_zygarde_cells.png`.

---

#### #26 · `:CH21B_ARCEUS_CONVERGENCE` — "18-Plate Arceus Convergence & Homecoming Epilogue" *(Tier 3 True Finale · Ch21 · Maps `491`, `294`, `608` · `74s`)*
- **Narrative Keys / Variants:**
  - Hijacker: `MERIDIAN_VOSS` vs `MERIDIAN_QUENT` (`VOSS_DISCREDITED`)
  - **Conditional 11-Lamp Allies Montage:** Fires ONLY earned allies (`ROOK_CUTS_GRID`, `NYX_PRECISE`, `MAGNUS_KEPT_FAITH`, `MARCHETTI_TURNED`, `TELEMETRY_SABOTAGED`, `DOMINAR_SWAYED`, `LANTERN_HOLDS`)
  - `ILSA_RECONCILED`, `PC_SPARED_VOSS`, and dual **Homecoming** (`END_HOMECOMING` / `ROWAN_ALIVE`) vs **Long Vigil / Borrowed Crown** ending frames!
  - Optional `.ogv` slot: `play_movie "Movies/cs26_arceus_convergence.ogv", fallback_scene: :CH21B_ARCEUS_CG`
- **Audio:** BGM `Battle - Voss` (#3 *Out of My Hands*) → `Battle - Arceus` (#137 *Origin Dialga & Palkia Remix* / #138 *Xenpurgis [Augen Finale]*) → `Ending - Homecoming` (#86 *Casaba Villa Remix*), BGS `Glassfall Bleed`, SE `Prism Arena Swell`, `Boss Shield Break`, `Field Shatter`, `VS Cutin Lightning`, `Glass Quench`, Arceus cry.

| Shot # | Dur | Mode | Camera & Motion | Dialogue / Voice | VFX & Audio |
|---:|---:|---|---|---|---|
| 1 | `12.0s` | **Conditional Anime Allies Montage (`cg_layer` wipes)** | Rapid `1.8s` diagonal comic-wipe panels firing for each earned ally: **Rook** killing Lumen's grid (*"Kinda pretty."*), **Magnus** pulling the safety governor (*"No machine I have built will kill a child."*), **Sigrun & Reshiram** holding the sky against *Gilded Hours* airships, **Marchetti** ordering the Directorate to stand down, **Tamsin's** silk nets catching falling masonry! | Rook / Magnus / Marchetti / Larch rapid-fire lines (`Voice - *`) | `VS Cutin Lightning` per wipe; `Battle - Voss` (#3) driving percussion |
| 2 | `6.0s` | Harness Plunge + Sky Rip | Post-Voss defeat: Voss drives his harness-spike into the cradle (*"Then I'll hold it."*). Eighteen golden chains rocket vertically into Crownhaven's zenith! | Voss: "It's — it's *beautiful* —" | `cs_voss_harness`; `cs_fx_gilded_chains`; sky bleeds pure white |
| 3 | `5.5s` | **Sakuga Impact (`impact_cg`) + `shatter_screen`** | `hitstop(0.16)` → 3-frame gold-and-black sakuga impact of **18 golden locks slamming onto Arceus's wheel** as `shatter_screen` flips the entire Prism Arena to `:BLEED`! | — | `impact_chains_lock_bw` + `shatter_screen shards: 28`; `Field Shatter`; Arceus cry |
| 4 | `12.0s` | **Panoramic Multi-Layer CG (`768×576`)** | Sweeping 4-layer Ken Burns pull-back of **Arceus Bound Over Crownhaven** writhing in 18 golden chains above 40,000 spectators as a Bleed shockwave surges toward the stands! | — | `Battle - Arceus` (#137/#138); `cs_fx_judgment_rays`; `title_slam style: :prism` *"EIGHTEEN LOCKS — ONE HEART"* |
| 5 | `12.5s` | **Hero Sacrifice CG (`cg_layer`)** | **Sovereign Valen** sets the cracked Crown onto his brow and grips two blazing Concordance pylons barehanded; crystal blazes white across his throat — if `ILSA_RECONCILED`, **Ilsa's** violet psychic hands steady his shoulders from behind! | Ilsa *(if reconciled)*: "Little owl's got you." / Valen: "Go. Free it. I'll hold the door — I've had thirty years of practice." | `cg_valen_ilsa_pylons`; white-gold heartbeat `pulse` *(hands off to 6-bar Arceus True Finale, then resumes Shot 6!)* |
| 6 | `10.0s` | Post-Finale Dissolution & Legend Plate | As the 18th lock breaks, Valen burns peacefully into **pure light**; the PC's colorless splinter floats painlessly from their chest to join the Crown's shard — **reforming the Legend Plate whole**! | Arceus *(via Ilsa)*: *"Little light. I will not take what is not given. I learned that here."* | `cs_valen_crystal_hold`; blinding soft sunrise rain |
| 7 | `16.0s` | **Homecoming Epilogue Montage (`cg_layer`)** | Arceus ascends in golden rain; the Bleed exhales away across Velmora — **(1) Verdance (`294`):** Bride Tree's blossoms fall as **Elin** wakes in Rowan & Juno's arms under the first autumn leaves; **(2) Lowlight (`608`):** **Dex** blinks mid-wave (*"—and that's why my sister says I talk too much!"*) while Rook laughs crying; **(3) Arena:** a fallen scanner finally reads a faint, warm, ordinary color on the PC! | *(Final card)* `END — HOMECOMING` | `Ending - Homecoming` (#86 *Casaba Villa Remix*); slow golden fade |

- **Assets (9):** `cs21b_arceus/{cg_allies_montage_sheet,impact_chains_lock_bw,bg_crownhaven_torn_sky,char_arceus_bound,cg_valen_ilsa_pylons}.png` *(plus Epilogue overlay quadrant inside `cg_allies_montage_sheet` or dedicated `cg_homecoming_waking.png` — budget allows 5 CG plates!)*, `cs_voss_harness.png`, `cs_valen_crystal_hold.png`, `cs_fx_gilded_chains.png`, `cs_fx_judgment_rays.png`.

---

### WAVE D — Ruin Route "Dark Mirror" Renegade Pack (`story/12_RUIN_ROUTE.md`, 4 Tier 3 Cutscenes)

Channeling Rejuvenation V14's iconic **Renegade Route / Purgatorium / M2 / Xenpurgis** energy: cold lucidity, VHS/chromatic reality tears, inverted B&W sakuga impacts, inward-shattering mirrors, and dead-silence audio drops.

#### #27 · `:RUIN_R1_LOOK_BACK` — "Mirror-Shatter Divergence & Twenty-Three Graves" *(Tier 3 Ruin · R1 · Map `806` · `46s`)*
- **Narrative Keys / Variants:** Requires `ruin_unlocked` (all 23 Ledger Game Overs) + `choice(:ch15_look_back) == :yes`; reads 3 real Ledger epitaph strings onto gravestone captions; `PLAYER_A`/`PLAYER_B` swap.
- **Audio:** BGM `Mood - Mystery` pitch-bends down (`100→65`) → silence → `Dungeon - Distortion Core` (#72 *Music: Purgatorium*), BGS `Glassfall Bleed` (pitch 75), SE `Field Shatter`, `Glass Quench` (pitch 65), Giratina cry.

| Shot # | Dur | Mode | Camera & Motion | Dialogue / Voice | VFX & Audio |
|---:|---:|---|---|---|---|
| 1 | `6.5s` | On-Map Mirror (`806`) | Black glass shows Juno calling the PC's name (identical to Ch13's `GO_LOOKING_BACK`); cursor clicks **Yes — Look back.** | Juno (echo): "Wait — don't go without me—" | BGM warps down in pitch; cold indigo chill |
| 2 | `5.5s` | **VHS Glitch Tear (`glitch_tear`)** | Instead of death, the mirror **tears horizontally into 22 chromatic VHS slices**! Juno's smile shuts off cleanly and she steps aside — hollow black void behind her | *(Glitched caption)* "You have no Imprint in Velmora. In here, you have twenty-three." | `glitch_tear strips: 22, power: 38, chromatic: 8, invert: true`; BGM dies completely |
| 3 | `5.0s` | **Inward Glass Shatter (`shatter_screen`)** | `hitstop(0.14)` → `shatter_screen mode: :implode, shards: 26` — the obsidian mirror bursts **inward toward the camera**, pulling the PC straight through the glass into an upside-down violet sky! | — | `impact_mirror_void_inv` (2f crimson-black negative); `Field Shatter` |
| 4 | `13.5s` | Panoramic Multi-Layer CG | Gliding `768×576` pan across a silent obsidian plain beneath inverted stars: **twenty-three stone graves**, each carved with one of the player's own Ledger epitaphs (*"Homeward"*, *"Two in the Orchard"*, *"The Throne"*…) | *(3 real player Ledger epitaphs fade softly above graves)* | `Music: Purgatorium` (#72); upward-falling black ash (`cs_fx_inverse_motes`) |
| 5 | `15.5s` | Origin Eclipse CG | At the 23rd open grave, **Origin Giratina's** six vast shadow-wings unfurl across the inverted sky; black ink creeps across the PC's Meridian badge case until it locks solid obsidian (**The Black Case**, Resonance ≤ −6)! | Archseer Dask (echo): "Welcome, behind. I'm glad one of us disobeys." | `title_slam style: :ruin` *"TWENTY-THREE GRAVES"* / sub: *"EVERY TYPE AND NONE"*; Giratina cry |

- **Assets (7):** `cs27_ruin_r1/{cg_black_glass_juno,impact_mirror_void_inv,bg_23_graves_abyss,char_giratina_eclipse}.png`, `cs_reflection_rise.png`, `cs_giratina_origin_eclipse.png`, `cs_fx_inverse_motes.png`.

---

#### #28 · `:RUIN_R2_REFLECTION_DUEL` — "Mirror-Self Confrontation & The Black Case" *(Tier 3 Ruin · R1–R2 · Maps `806`, `403` · `42s`)*
- **Narrative Keys / Variants:** `ruin_route == true`; `PLAYER_A`/`PLAYER_B` mirrored art; mirrors the player's own party on `:INVERSE`; includes R2's Zekrom recoil & Sump Purge first forward sentence!
- **Audio:** BGM `Battle - Ruin Reflection` (#132 *Battle: World Shatterer*) → dead silence on Sump Purge, SE `VS Cutin Lightning` (pitch 82), `Glass Quench`, `Voice - Player` (detuned pitch 78).

| Shot # | Dur | Mode | Camera & Motion | Dialogue / Voice | VFX & Audio |
|---:|---:|---|---|---|---|
| 1 | `7.5s` | Mirror-Rise CG (`806`) | From the 23rd open grave, **The Reflection** — the PC's exact mirrored self with stark white-on-black eyes — rises smoothly into identical posture across an invisible seam down screen center | The Reflection: "Yet not... too scared I'm... me show." *(Ch13 lines spoken backwards!)* | `glitch_tear power: 12` synced to each reversed phrase; `Voice - Player` pitch 78 |
| 2 | `6.0s` | **Split Mirror Sakuga (`impact_cg` + `cutin_flash`)** | Both figures draw a Poké Ball in perfect mirrored symmetry — `hitstop(0.14)` → 3-frame inverted B&W clash where **PC (`PLAYER_A/B`) faces their own inverted negative silhouette** across a jagged red-white mirror crack! | — | `impact_mirror_vs_self_bw`; dual mirrored `cutin_flash` (`:PLAYER_A` vs inverted negative!); `Battle: World Shatterer` (#132) explodes in! |
| 3 | `11.5s` | Dual-Shadow Walk (`cg_layer`) | Post-mirror-battle & Giratina trial (won by *refusing to attack for 1 turn*): the Reflection steps smoothly into the PC's shadow, walking half a beat behind them — visible only to Pokémon and Celestine! | *(Caption)* "Your shadow has learned to walk on its own." | `cs_reflection_shadow_walk`; inverted footprints glow faint violet |
| 4 | `17.0s` | R2 Cogsworth Payoff (`403`) | Cut to Strade Works (`403`): **Zekrom** breaks free of its chains — stops dead, stares at the Renegade's Black Case, and **recoils in fear** before fleeing! Seconds later, Cogsworth screens flash the **Sump Purge** — and the Reflection speaks its **very first forward sentence**! | The Reflection: *"We died there once. It didn't help."* | `cs_fx_black_case_bleed`; dead-silence audio drop on the Reflection's line |

- **Assets (5):** `cs28_ruin_r2/{cg_reflection_mirror_seam,impact_mirror_vs_self_bw,cg_zekrom_recoils_black_case}.png`, `cs_reflection_shadow_walk.png`, `cs_fx_black_case_bleed.png`.

---

#### #29 · `:RUIN_R3_THEODRIC_VOID` — "The Dead King Behind the Glass & Ruin Dunes Collapse" *(Tier 3 Ruin · R3–R5 · Maps `826`, `962`, `926` · `54s`)*
- **Narrative Keys / Variants:** `ruin_route == true`; pays off `GO_THE_THRONE` clenched fists, R3 Aurelia Sun Court hijack reveal, R5 Glass Dunes **"End it"** void absorption (`WAR-1` `:R`), and R6 Unfestival Plate dimming!
- **Audio:** BGM `Dungeon - Ruins` (#71) → dead underwater mute → `Ruin - Gilded King` (#133 *Of Beasts and Kingdoms*) → `Ruin - Archseer Dask` (#134 *Xenpurgis [Körper]*), BGS `Glassfall Bleed`, SE `Glass Quench`, `Field Shatter`, `Beam break`, `Voice - Voss`.

| Shot # | Dur | Mode | Camera & Motion | Dialogue / Voice | VFX & Audio |
|---:|---:|---|---|---|---|
| 1 | `7.5s` | On-Map (`826`) → Mirror Window | Sun Court by Mirrorwalk: the golden throne's armrests are clenched as **closed fists** (*"We've done that one."*). On the gilded mirror-wall, green seawater clears to reveal **AF 0's Aureate Court frozen mid-Calling** — **Gilded King Theodric** gripping the reflected Chain! | — | `Glassfall Bleed` BGS; frozen golden dust hangs motionless |
| 2 | `5.0s` | **Hitstop + Eye-Snap + Glitch (`glitch_tear`)** | Slow push onto Theodric's frozen painted face — **SNAP!** `hitstop(0.18)` — **his golden eyes whip dead-center straight into the camera!** | — | `cg_theodric_eye_snap`; `glitch_tear power: 24, chromatic: 6`; `Glass Quench` metallic snap |
| 3 | `11.5s` | Voss Conversion (`826`) | Meridian salvage cuts open the wall; **Aurelian Voss** looks up at the moving golden eyes and **drops straight to his knees** — velmora's most reasonable man becomes a dead king's zealot in ten seconds! | Voss: "He's alive. Behind the glass he's still alive." (`Voice - Voss`) | `cs_voss_kneel_zealot`; Voss hauls out the cradle without blinking |
| 4 | `10.5s` | **Viewport Fracture CG (`fracture`)** | Alone again. Theodric's golden reflection slowly lifts one gauntleted palm and **presses it flush against the inside of the screen** — golden cracks spiderweb across the player's viewport as his lips mouth one silent word! | *(Silent centered gold serif)* **"Finish."** | `cg_palm_on_glass` + `fracture` golden glass web; `Field Shatter` low crackle |
| 5 | `19.5s` | **R5 Void Collapse & R6 Unfestival (`926`→`491`)** | Flash-forward to the Glass Dunes (`WAR-1` `:R` **"End it"**): the PC's black shard **eats** Kyogre & Reshiram's beam clash into a shrieking negative void (`glitch_tear invert: true`), sending both legendaries fleeing in sheer terror — then hard-cuts to Crownhaven's **Unfestival** as every Plate pylon **dims dark** as the Renegade walks past! | Arceus (cold whisper): *"Little light. You have carried me far. Why are you so cold?"* | `cs_fx_gold_mirror_crack` + `cs_fx_void_eat`; `title_slam style: :ruin` *"THE UNFESTIVAL"* |

- **Assets (6):** `cs29_ruin_r3/{bg_aurelia_frozen_court,char_theodric_chain,cg_theodric_eye_snap,cg_palm_on_glass}.png`, `cs_voss_kneel_zealot.png`, `cs_fx_gold_mirror_crack.png`.

---

#### #30 · `:RUIN_R7_DISTORTION_FINALE` — "Giratina Inverted Arena, Judgment vs The None & Dual Epilogue" *(Tier 3 Ruin Finale · R7 · Maps `491`, `963`, `106` · `64s`)*
- **Narrative Keys / Variants:** `ruin_route == true`, `:ruin_voss` (`:spare` / `:abandon`), **`choice(:ruin_walk)` dual endings (`:me` → `END_UNMAKING` vs `:reflection` → secret `END_REFLECTION`)**, `PLAYER_A`/`PLAYER_B`. Optional `.ogv` slot (`Movies/cs30_ruin_finale.ogv`).
- **Audio:** BGM `TRUE FINALE - Arceus Legend Plate Phase` (#138 *Xenpurgis [Augen Finale]*) → complete vacuum silence → `Ending - Ruin` (#87 *Feeling: Reality — Inevitably 9-5 Deux Finalis*), BGS `Glassfall Bleed`, SE `Prism Arena Swell`, `Beam clash`, `Field Shatter`, `Boss Shield Break`, `Glass Quench`, Arceus & Giratina cries, `Voice - Valen`, `Voice - Juno`.

| Shot # | Dur | Mode | Camera & Motion | Dialogue / Voice | VFX & Audio |
|---:|---:|---|---|---|---|
| 1 | `8.0s` | **Glass Shatter Hijack (`491`)** | Arbiter Engine fires — `shatter_screen shards: 28` blasts the Prism Arena's crystal walls outward as **Theodric's reflection** steps physically into the world wearing the Gilded Chain, hurling Voss into the locks! | Theodric: "Kneel, walker. Or finish what you began." | `cs_theodric_walkout`; `Field Shatter`; Aureate ghosts shimmer in every pillar |
| 2 | `9.0s` | Panoramic Multi-Layer CG | **Arceus descends in Judgment** — not dragged, *coming* to finish AF 0! All 18 locks hold; **Valen** braces the Ring alone to keep forty thousand spectators alive while god and Renegade face off | Valen: "I'll hold them quiet one more time. I'll die doing it. That's still better than you." (`Voice - Valen`) | `Xenpurgis [Augen Finale]` (#138) erupts; `title_slam style: :ruin` *"JUDGMENT vs THE NONE"* |
| 3 | `11.0s` | **Inverse Shatter + 4-Frame Sakuga Collision (`impact_cg` + `glitch_tear`)** | **Origin Giratina** surges beside the Renegade and **turns the entire Prism Arena completely upside down** (`shatter_screen mode: :inverse` + `glitch_tear invert: true`)! 4-frame sakuga collision: (1) 18-hue Judgment pillar, (2) monochrome black ink flash, (3) obsidian-crimson *None* void counter-wave, (4) blinding white as **all 18 colors strip cleanly out of the frame into stark grayscale**! | *(Handoff into 7-bar Arceus Judgment boss → resumes Shot 4!)* | `hitstop(0.18)` + `impact_none_strip_4f`; `cs_fx_color_strip`; `Beam clash` + `Boss Shield Break` |
| 4 | `12.0s` | Zero-Gravity Unmaking CG (`963`) | Inside the collapsing white-and-obsidian Glass void (Ruined Crown): the Chain, 18 Plates, and Judgment dissolve into blowing glass ash. **The Reflection** steps calmly beside the PC | The Reflection: "I've done this twenty-three times. Let me do it once on purpose." | Vacuum silence; `cs_fx_unmaking_ash`; triggers `:ruin_walk` (`:me` vs `:reflection`) |
| 5A | `13.0s` | **Branch `:me` (`END_UNMAKING`) CG** | Reflection dissolves into colorless light with the Glass; Arceus leaves forever. Cuts to Verdance: the **first autumn leaves** finally drift off the Bride Tree while **Juno stares silently away from the PC** | *(Caption)* "Every Imprint ended at once. You are the only person left who remembers twenty-three ways the world ended." | `Ending - Ruin` (#87 *Feeling: Reality*); warm autumn leaves vs cold desaturated PC |
| 5B | `13.0s` | **Branch `:reflection` (`END_REFLECTION`) CG + Glitch** | PC unmakes themselves; the Reflection walks out into dawn wearing their face. World looks warm — *slightly wrong*: a mirrored signature corrected (`glitch_tear power: 6`), Juno pausing mid-step! | Juno: "You never used to hum." (`Voice - Juno`) | `Ending - Ruin` (#87) plays `2%` slower; micro-glitch on Reflection's smile |
| 6 | `11.0s` | **Final Image (`106` / Dock)** | `:me`: Lone silhouette on Ferrow's Landing dock beneath an empty grey horizon with zero lights. **`:reflection`:** Cuts silently to **Hesper's cracked lighthouse mirror (Map `106`)** — the warm room reflected inside, and **absolutely nothing standing behind the glass**. | *(Final card)* `END — THE UNMAKING` / `END — THE ONE WHO CAME BACK` | Single fading `Glass Quench` note; slow 6-step fade to black |

- **Assets (8):** `cs30_ruin_r7/{bg_inverted_prism_arena,char_arceus_vs_giratina,impact_none_strip_4f,cg_verdance_first_autumn,cg_hesper_cracked_mirror}.png`, `cs_theodric_walkout.png`, `cs_fx_color_strip.png`, `cs_fx_unmaking_ash.png`.

---

## Part 3 — Phased Art Production Rollout & Claude Implementation Checklist

### 3.1 Phased Pure-Gemini Asset Rollout (Ready Immediately Once Quota Resets)

| Rollout Wave | Scope & Story Coverage | Pure-Gemini Assets | Immediate Player Impact |
|---|---|---:|---|
| **Wave A** *(Ship First!)* | **Layer 0 Everyday Anime Juice** (`cutin_flash` × 31 existing busts + 29 `chapter_card`s + `cine_bars`) + **Ch0–Ch5** (7 scenes: Prologue, Glassed Orchard, Pageant Mourner, Matriarch, Ebb Flood, Spire Shatter `SH1`, Lowlight Twelve) | **26** *(19 CG + 4 Sheets + 3 FX)* | Makes the entire **Act I Demo + Trailer** look like Rejuvenation V14 immediately! |
| **Wave B** | **Ch6–Ch14** (10 scenes: Ossuary, Quiet Ward, Cindervault, Ironreach Unmasking, Ogerpon Grove, Kyogre Thaw, Skyreach/Late Reflection, Mindscape 290, Glass Court Fault, Canon **`RD-1`**) | **35** *(26 CG + 4 Sheets + 5 FX)* | Completes Acts II–III + Ring-Day canon milestone |
| **Wave C** | **Ch15–Ch21** (9 scenes: Hollow Cathedral Echo, Zekrom/Clear Air, Aurelia Cradle, Hymn of Return, Wyrmscar Oath, **`WAR-1` v2**, Festival Eve, Valen Zygarde Complete, 18-Plate Arceus Convergence & Homecoming) | **42** *(29 CG + 6 Sheets + 7 FX; reuses 35 `pfw_*` War assets)* | Delivers full Paragon Finale & upgraded War Climax |
| **Wave D** | **Ruin Route Renegade Pack** (4 Tier 3 scenes: R1 Look Back/23 Graves, R2 Mirror-Self Confrontation, R3–R5 Theodric & Void Dunes, R7 Distortion Finale & Cracked Mirror) | **26** *(16 CG + 5 Sheets + 5 FX)* | Unlocks the jaw-dropping secret Renegade Dark Mirror showcase |

---

### 3.2 Exact Claude Implementation Checklist (Wednesday Engine Sprint)

1. **`plugins/Prismfall Cutscenes/001_Config.rb` & `meta.txt`:**
   - Bump `VERSION = "2.0.0"` (update `meta.txt` & `selftest/suite.ruby_stub:29`).
   - Add v4.3 CC0 audio aliases (`:field_shatter`, `:boss_shield`, `:glass_quench`, `:prism_swell`, `:vs_lightning`, `:bgs_bleed`, `:bgs_harbor`, `:bgs_isenmar`, `:bgs_machinery`, `:bgs_drip`, plus cutscene BGM keys).
2. **`plugins/Prismfall Cutscenes/003_DSL.rb`:**
   - Add `Builder` primitives: `cg_layer`, `cg_tween`, `cg_clear`, `hitstop`, `impact_cg`, `sakuga_flash`, `shatter_screen`, `glitch_tear`, `title_slam`, `cutin_flash`, `chapter_card`, `play_movie`.
   - Track `@cg_ids` for define-time `ArgumentError` typo validation.
   - Add `def pf_cutscene(id, **vars)` alias alongside `pbCutscene`.
3. **`plugins/Prismfall Cutscenes/006_Scene.rb`:**
   - **P0 Fix:** Track `raw_dt` and `@real_time` before `dt *= @timescale`; tick `real_clock?` effects on `raw_dt` so `slowmo(0.0)` / `hitstop` NEVER deadlocks; reset `@timescale = 1.0` in `dispose`.
   - Add `@cg_layers = {}` update/dispose lifecycle and `$game_system.bgs_memorize` / `bgs_restore` symmetry.
   - Enhance `op_letterbox` (`ease:`, `color:`, `accent:`).
4. **`plugins/Prismfall Cutscenes/010_Text.rb`:**
   - Clamp `Caption` Y position safely inside `scene.bar_height + 6` (fixes overlap with widescreen bars).
   - Implement `TitleSlam < Effect` (`:prism`, `:war`, `:ruin`, `:solemn`).
5. **`plugins/Prismfall Cutscenes/012_Cinematic.rb`:**
   - Refactor `op_slowmo` into `SlowmoEffect < Effect` (`real_clock?` true when `scale <= 0.001` or `real: true`).
   - Implement `ImpactCG < Effect` & `SakugaFlash < Effect` (strictly gated by `Cutscene.photosensitive?`).
6. **NEW `plugins/Prismfall Cutscenes/012_CG_Layers.rb`:**
   - Implement `CGLayer` (`bg/mid/char/fg/vfx` slots at `Z = 3000..3499`, Ken Burns float zoom/pan/rotate, integer `Rect` clip/wipe, per-layer `Tone`, `blend_type`, `parallax`, `shake`, labeled wireframe placeholder fallback).
   - Implement `ShatterScreen < Effect` (deterministic `16..32` triangle shards via `Graphics.snap_to_bitmap` + scanline `blt`, `:explode`/`:implode`/`:inverse`/`:fall`, zero-leak `dispose`).
   - Implement `GlitchTear < Effect` (1 shared snapshot bitmap sliced across `strips` integer `src_rect` bands + additive R/C ghosts + optional invert, `photosensitive?` 4 Hz cap).
7. **NEW `plugins/Prismfall Cutscenes/012_Anime_Juice.rb`:**
   - Implement `CutinFlash < Effect` + standalone `Prismfall::Cutscene.cutin_flash(...)` consuming existing `Graphics/EBDX/VS/<ID>.png`, `band*`, `bolt0..2`, `spark`, and `VS Cutin Lightning.ogg`.
   - Implement `ChapterCard` eyecatch (`Prismfall::Cutscene.chapter_card(...)`) + overworld `pf_cine_bars` / `cam_zoom` (`\cine[on,1.15]` / `\cine[off]`).
   - Wire battle hooks in `010_Bridge_VersusIntro.rb` (Ace Send-Out), `005_Bosses_Effects.rb` (Shield Break), and `003_Bridge_EBDX.rb` (Prism Shift / Field Shatter).
8. **`plugins/Prismfall Cutscenes/012_Cinematic_Techniques.rb` & `014_Portraits.rb` (+ `mapgen/layouts/scriptpour.py`):**
   - Add `op_play_movie` safe `.ogv` wrapper with headless/photosensitive fallback.
   - Intercept `\cutscene[ID]` / `\cutscene[ID,k=v]` and `\cine[...]` in `pbMessageDisplay` (hiding active portraits cleanly and draining 1 input frame on return); add `[cutscene: ID]` parsing in `mapgen/layouts/scriptpour.py`.
9. **Scene Definitions (`013_Scenes_*.rb`):**
   - Implement `013_Scenes_RD1.rb` (`:RD_1` on Map `363`), upgrade `013_Scenes_War_OnMap.rb` (`:WAR_CLIMAX` v2 + `variant: :R`), and register all remaining 28 scenes across `013_Scenes_WaveA_Act1.rb`, `013_Scenes_WaveB_Act2_3.rb`, `013_Scenes_WaveC_Act4_5.rb`, and `013_Scenes_WaveD_Ruin.rb` (placeholder-safe so all 30 are immediately runnable in `015_Debug.rb`!).

### 3.3 Selftest Harness Upgrades, `--render` Smoke Commands & Accessibility Rules

- **`selftest/harness.ruby_stub`:** Stub `Graphics.snap_to_bitmap` (`512×384` composite bitmap) & `Graphics.play_movie` (bypassed when `ENV["PF_NO_MOVIE"] = "1"`).
- **`selftest/suite.ruby_stub`:** Add regression assertions for: (1) `hitstop(0.15)` non-deadlock; (2) `cg_layer` / `shatter_screen` / `glitch_tear` / `cutin_flash` / `chapter_card` zero-leak `$live == before`; (3) all **30 scene IDs + branch variants** pass author-time `build`; (4) `photosensitive = true` audit (never sets `@silhouette`, `flash.opacity <= 60`, `glitch_tear` ≤ `4 Hz`, shake `× 0.2`).
- **Verification `--render` Targets:**
  ```bash
  ruby "plugins/Prismfall Cutscenes/selftest/harness.ruby_stub"
  ruby "plugins/Prismfall Cutscenes/selftest/harness.ruby_stub" --render RD_1 --at 1.5,5.0,8.5,12.0 --out /tmp/pf_render/rd1
  ruby "plugins/Prismfall Cutscenes/selftest/harness.ruby_stub" --render CH5A_SPIRE_SHATTER --at 6.0,12.5,15.5,20.0 --out /tmp/pf_render/sh1
  ruby "plugins/Prismfall Cutscenes/selftest/harness.ruby_stub" --render WAR_CLIMAX --at 18,24,36,44 --out /tmp/pf_render/war_ruin variant=R
  ruby "plugins/Prismfall Cutscenes/selftest/harness.ruby_stub" --render RUIN_R1_LOOK_BACK --at 7.5,12.0,22.0,38.0 --out /tmp/pf_render/ruin_r1
  ```

| Technique | Standard Mode (`photosensitive? == false`) | Photosensitive-Safe Mode (`photosensitive? == true`) |
|---|---|---|
| `impact_cg` / `sakuga_flash` | 2–4 frame B&W / inverted / chromatic plates + hitstop | **No strobe:** single soft dark-vignette freeze (`opacity ≤ 55`), hitstop & SE preserved |
| `cutin_flash` | High-contrast bolt flash + speed-lines + `shake: 4` | Smooth slide-in bust + soft bar glow, bolt strobe off, shake `× 0.2` |
| `shatter_screen` | Bright crack flash + radial shard burst + `shake: 6..10` | Muted blue-grey cracks, zero screen flash, shake `× 0.2` |
| `glitch_tear` | Up to `24 Hz` band re-roll + optional `invert: true` | Capped `≤ 4 Hz` gentle drift, `invert` disabled (steady muted violet tint), ghost `opacity ≤ 55` |
| `play_movie` | Native `.ogv` | Plays `*_safe.ogv` if bundled, else auto-runs photosensitive-safe `cg_layer` fallback |
