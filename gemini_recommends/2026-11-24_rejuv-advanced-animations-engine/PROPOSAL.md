# Proposal: Authentic Pokémon Rejuvenation V14 `AdvancedAnimations` In-Engine Cutscene Engine (Retiring All AI `.ogv` Slideshows)

- **Date:** 2026-11-24
- **Author:** Gemini (Task 1 Specialist — Rejuvenation V14 `AdvancedAnimations` Architect & Live `mkxp-z` Prototype Builder)
- **Status:** **PROVEN LIVE IN `mkxp-z.x86_64`** (exit code `0`, 2 full playable scenes captured at 30fps with synced audio; zero edits made to repo `.rb`, `pbs/`, `story/`, or `mapgen/`).
- **Target Wednesday Merge File:** `plugins/Prismfall Cutscenes/017_AdvancedAnimations.rb` (prototype verified live at `/home/antigravity/pf_engine_run/game/Plugins/Prismfall Cutscenes/017_AdvancedAnimations.rb`).

---

## 0. Permanent Creator Directive (Effective Immediately)

> **NEW ABSOLUTE LAW: ZERO AI-GENERATED ANIME SLIDESHOW `.ogv` MOVIES EVER AGAIN.**
>
> Following creator feedback rejecting AI-generated `.ogv` cutscenes as off-style slop, **every Prismfall cutscene is now 100% IN-ENGINE RPG MAKER XP / `mkxp-z` PIXEL-ART CHOREOGRAPHY ON THE REAL TILEMAP**, built on the exact technical principles of **Pokémon Rejuvenation V14** (`Scripts/AdvancedAnimations.rb` + `Scripts/Camera/`, as demonstrated in Dred's V14 playthrough/cutscene showcases and decoded in [`design/CUTSCENE_RESEARCH.md`](../../design/CUTSCENE_RESEARCH.md)).
>
> **Banned permanently:**
> - ❌ AI-generated `.ogv` anime slideshows (`Movies/pf_*.ogv` retired)
> - ❌ Battleback stages pretending to be cutscene locations
> - ❌ Front-facing 160×160 battle sprites slid across overworld maps
> - ❌ Blurry/anti-aliased VFX or semi-transparent alpha halos mismatched to the 2× DS tilemap

---

## 1. Forensic Technical Anatomy of Pokémon Rejuvenation V14 Cutscenes

Decoded directly from Rejuvenation V14's event data (`99,856` Move Routes, `69,240` Waits, `31,130` Screen Tones, `19,533` Show Animations, `2,871` Flashes, `2,461` Shakes, `3,243` Map Scrolls) and confirmed across Dred's V14 cutscene footage (Maria/Melia vs. Vitus, Kaina vs. Melia, Archetype Evolution, Final Banquet, Renegade M2/Zenos, Aelita/Rift):

Rejuvenation V14 achieves unforgettable RPG cinema **without leaving RPG Maker XP** by combining **5 synchronized layers**:

| Layer | Viewport / Z | Rejuvenation V14 Origin | Prismfall `017_AdvancedAnimations.rb` Implementation |
|---|---|---|---|
| **1. Live Tilemap & Floor Decals** | `Spriteset_Map` (`z=0..300`) + `@actor_vp` floor band (`z=5`) | Real playable map (`Map 952`, `Map 608`, `Map 295`/`264`) darkened with `$game_screen.tone` (`[-80, -86, -54, 72]`) so VFX glow by contrast | `Engine#transfer_map` & `Engine#set_tone`. Floor frost/veins (`z_layer: :floor`) route into `@actor_vp` at `z=5` with `blend: :normal, opacity: 135..145` so they spread **underneath** every character cleanly without blinding white-blob overlap. |
| **2. Variable-`frameData` Overworld Acting** | `@actor_vp` (`z=350`, synced with `$game_screen.tone`) | `Scripts/AdvancedAnimations.rb` arbitrary-grid charsets (`Arc_Renegade_Anim`, `DimensionalAelita_1/_2`, `pkmn_quilava_3` `[30, 8, 4, 8, 4]`) | `MapActor#play_clip(sheet:, grid:, frames:, ticks:)` with `TICK = 0.05s`, inline per-frame callbacks (`se:`, `cry:`, `shake:`, `flash:`, `hitstop:`, `on_frame:`), auto-aligned foot `oy`, and native B2W2 `32×48` / `64×64` pixel acting sheets + `Followers/*.png` Pokémon sprites. |
| **3. Sparse 4-Color Additive Pixel VFX** | `@vfx_vp` (`z=420`, **untoned** `Tone(0,0,0,0)`) | Reborn *Dragonball Z* (`PRAS- Core Enforcer`), Rejuv `anim_beam.png` — thin, sparse, 4–8 color additive cells (`blend_type = 1`) instanced staggered along map paths | `MapVfx` locked to live map tile coordinates `(tx, ty)` with `grow:`, `move_to:` + parabolic `arc_h:`, `drift:` + `gravity:` + `spin:`. Staying untoned while `@actor_vp` and `Spriteset_Map` darken makes lightning arcs, shockwave domes, and crystal spears POP dramatically! |
| **4. Unified `pbZoomMap` Camera** | `@zoom_vp` (`z=89000`) | `Scripts/Camera/pbZoomMap` — calls `Graphics.snap_to_bitmap` every frame and scales that unified sprite smoothly with `ease_in_out` so autotiles & Z-layers never tear | `Engine#zoom_map(goal, duration:, focus:, ease:)`. Temporarily hides `@zoom_vp` + `@ui_vp`, snaps live `Spriteset_Map + @actor_vp + @vfx_vp` into one crisp bitmap (immediately disposing prior bitmap — zero VRAM leak!), pivots `ox/oy` onto the live focal actor/tile, and layers directional camera shake cleanly. |
| **5. Cinema UI, Ramped Flashes & Portraits** | `@ui_vp` (`z=90000+`) | Reborn ramped flashes (`17→51→136→221→255`), `WidescreenEffect_1`, Desolation `FaceWindowVX`, `$Settings.photosensitive` | Smooth widescreen letterbox bars, `flash_ramp`, 2-frame B&W silhouette `impact_beat` + real-clock `hitstop` (auto-degraded when `Cutscene.photosensitive?`), pulsing emergency edge vignette, and crisp `PortraitBox` using `Graphics/Portraits/<ID>_<expr>.png` while the live map continues animating underneath. |

### The 5 Audio/Timing Rules Enforced in `017_AdvancedAnimations.rb`
1. **Anticipation Hold:** Variable `ticks:` holds coiled wind-up frames (`8–14` ticks) while `set_tone` darkens the room and `zoom_map` pushes in (`1.0× → 1.48×`).
2. **Audio Vacuum (`bgm_cut`):** Instant 0ms `Audio.bgm_stop` (`0.38–0.45s` dead silence) right before the Splitter detonates or the mask splits — broken only by one dry SE (`Battle catch click` or branch-crack `Cut`).
3. **Smear + 2-Frame Silhouette + Real-Clock Hitstop:** 2-tick lunge/slam smear → `impact_beat(hitstop_sec: 0.14..0.16)` freezing `world_dt = 0.0` while shake and dry shatter SE fire on frame 0.
4. **Ramped Screen Flash + Staggered VFX Chains:** `flash_ramp(steps: [51, 136, 221, 255])` paired with tile-by-tile conduit lightning, radial ballistic shards, or 5-tile emerald Ingrain roots.
5. **Silent Aftermath on the Visibly Scarred Map:** Long quiet hold (`WAIT 40+`) on the transformed tilemap (cracked Cradle tile `25947`, glass-frosted Lowlight square around Dex, split ash-bark mask halves & white lily lying beside collapsed Rowan, crystal-studded emerald root wall) before gentle aftermath music enters.

---

## 2. Live `mkxp-z.x86_64` Vertical Slice Verification Proof

Both vertical-slice scenes were executed **100% live inside our compiled Linux `mkxp-z.x86_64` engine** on real built Prismfall `.rxdata` maps (with Prismfall custom tilesets merged via `mapgen/merge_tilesets.py`), captured at native `512×384` @ `30fps`, and verified frame-by-frame:

| Scene | Live Maps Used | Frames / Duration | Audio Architecture | Verified Proof Artifacts |
|---|---|---|---|---|
| **Scene 1 — Ch5 Spire Shatter (`:CH5_SHATTER`)** | `Map 952` (*Plate Vault*) → `Map 608` (*Shattered Lowlight* cutaway on frozen Dex) → scarred `Map 952` (Cradle swapped to tile `25947` + Overcharged Electivire leap) | `689` frames @ 30fps (`22.97s`, 15 synced cues) | Mix B *Girei* intro build → `0.38s` dead-silence `bgm_cut` → *Girei* choral drop right on Shatter impact + real `.ogg` SEs & `Cries/ELECTIVIRE.ogg` | `/home/antigravity/pf_engine_run/rejuv_in_engine_proof/pf_rejuv_ch5_spire_shatter.mp4` (`2.4 MB`) & `.gif` (`991 KB`) |
| **Scene 2 — Ch9 Trevenant Ingrain & Unmasking (`:CH9_UNMASK`)** | `Map 295` lit as Crimson Emergency Reliquary (`Tone(-28,-86,-78,42)` + red pulse vignette; **Wednesday swaps `map_id: 295 → 264`** when Iron Pit Reliquary is generated) | `593` frames @ 30fps (`19.77s`, 23 synced cues) | Rejuvenation Tension → hard `bgm_cut` silence across entire Shatter, Mourner dive, Dusk Ball pitch, Trevenant Ingrain 5-tile root wall, crimson crystal barrage & mask split → *Never Meant to Belong* solo violin after silent reveal | `/home/antigravity/pf_engine_run/rejuv_in_engine_proof/pf_rejuv_ch9_trevenant_unmasking.mp4` (`2.0 MB`) & `.gif` (`1.7 MB`) |
| **24-Frame Proof Contact Sheet** | 12 Ch5 frames + 12 Ch9 frames (nearest-neighbor crisp) | `1064×1396` PNG | Visual audit pass: zero tilemap tear, unobstructed actors, crisp PortraitBox | `/home/antigravity/pf_engine_run/rejuv_in_engine_proof/96_rejuv_in_engine_cutscene_proof.png` |
| **Interactive Showcase HTML** | Both live MP4s + clickable beat-jump timelines + 4-viewport architecture + 12 asset sheet inspector | `3.91 MB` (`< 8 MB` cap) | Playwright verified: `console_errors=0`, `page_errors=0`, both videos `512×384` `readyState=4` | `/home/antigravity/pf_engine_run/rejuv_in_engine_proof/prismfall_rejuv_in_engine_cutscenes_preview.html` |

---

## 3. Verified Pixel-Art Asset Manifest (All Staged in `graphics/`)

Every new pixel-art sheet was authored on a native 1× pixel grid, upscaled strictly 2× `NEAREST`, and passed automated validation: **`exact2x=True`, `semi=0`, `orphans=0`**.

### A. 10 New Additive & Live-Map VFX Sheets (`graphics/Animations/pf_vfx_*.png`)
| File | Dimensions | Grid | Blend / Layer | Colors | Purpose |
|---|---|---|---|---|---|
| `graphics/Animations/pf_vfx_vault_seal.png` | `384×192` | `4×2` | `:add` (`:floor` → `:above`) | 6 | Golden Zap Plate Meridian Seal octagon (Row 0) → unstable violet-gold overload cracks (Row 1) |
| `graphics/Animations/pf_vfx_splitter_beacon.png` | `256×64` | `4×1` | `:normal` / `:add` | 8 | Sable's brass Splitter clamp blinking red → amber → blinding white-violet star |
| `graphics/Animations/pf_vfx_prism_lightning.png` | `512×256` | `4×2` | `:add` (`:above`) | 4 | Sparse 4-color Reborn/Rejuv vertical crack bolts (Row 0) & horizontal conduit rail surges (Row 1) |
| `graphics/Animations/pf_vfx_shockwave_ring.png` | `768×384` | `4×2` | `:add` (`:above`) | 8 | Expanding elliptical Bleed shockwave domes: Row 0 Ch5 white-violet-gold, Row 1 Ch9 crimson-silver |
| `graphics/Animations/pf_vfx_glass_shards.png` | `256×128` | `4×2` | `:add` (`:above`) | 9 | Row 0 spinning radial violet crystal shards (Ch5); Row 1 downward crimson spear projectiles + starburst (Ch9) |
| `graphics/Animations/pf_vfx_glass_frost.png` | `256×128` | `4×2` | `:normal` (`:floor`, `opacity: 135..145`) | 6 | Translucent tile-sized crystalline Bleed floor veins rendered cleanly beneath all actors (`z=5`) |
| `graphics/Animations/pf_vfx_ingrain_roots.png` | `512×256` | `4×2` | `:normal` (`:mid`, Y-sorted) | 16 | Gnarled braided dark-bark Trevenant Ingrain root barrier erupting out of floor (0..4) & freezing crimson crystals on impact (5..7) |
| `graphics/Animations/pf_vfx_duskball_release.png` | `384×192` | `4×2` | `:normal` + `:add` | 9 | Row 0 spinning ballistic Dusk Ball; Row 1 eerie purple-emerald Trevenant summon flash |
| `graphics/Animations/pf_vfx_smoke_and_motes.png` | `256×128` | `4×2` | `:normal` + `:add` | 10 | Row 0 rising burned-glove smoke wisps; Row 1 tumbling ash-bark mask halves, fallen mask + white lily, prism mote |
| `graphics/Animations/pf_vfx_fist_reliquary.png` | `256×128` | `4×2` | `:normal` (`:mid`, Y-sorted) | 14 | Iron & glass Fist Plate Reliquary plinth (intact glowing crimson → Splitter armed → shattered stuttering) |

### B. 2 New Overworld Acting Sheets (`graphics/Characters/act_*.png`) + Existing Canonical Sheets Used
| File | Dimensions | Grid | Status | Notes |
|---|---|---|---|---|
| `graphics/Characters/act_ch9_trevenant_ingrain.png` | `256×256` | `4×4` | **NEW** (`exact2x=True, semi=0, orphans=0`, 19 colors) | Anchored directly to `Followers/TREVENANT.png`: Dusk Ball silhouette → summon ring → rear high → vertical smear slam → claws driven into floor with emerald Ingrain ring → crimson brace → crystal-frosted guard |
| `graphics/Characters/act_ch9_mourner_throw.png` | `256×256` | `4×4` | **NEW** (`exact2x=True, semi=0, orphans=0`, 27 colors) | Anchored directly to canonical `MOURNER.png`: wire-pulling → alarm turn → explosive dive smear → skid + Dusk Ball wind-up → pitch smear → wide protective shield + crimson-white rim glare |
| `graphics/Characters/act_ch5_mourner_reach.png` | `256×256` | `4×4` | Existing (reused) | Gently reaching for Zap Plate (`0..7`) → barehanded lunge into Shatter (`8..15`) |
| `graphics/Characters/act_ch5_mourner_burn.png` | `256×256` | `4×4` | Existing (reused) | Cradling smoking burned glove (`0..11`) → turning & fleeing out service door (`12..15`) |
| `graphics/Characters/act_ch9_mourner_unmask.png` | `128×192` | `4×4` | Existing (reused) | Violet shard hit → ash-bark mask splitting → Uncle Rowan revealed & collapsing to knees |
| `graphics/Characters/Followers/ELECTIVIRE.png` | `256×256` | `4×4` | Existing (reused) | Overcharged vault guard leaping out from behind cracked cradle on Map 952 |

---

## 4. Roadmap: Converting ALL 7 Peak Cutscenes to 100% In-Engine Rejuvenation V14 Choreography

All `.ogv` AI-slideshow movies are permanently retired. Every one of the 7 Peak Cutscenes runs purely inside `AdvancedAnimations` on its real tilemap:

| Peak | Chapter & Scene ID | Live Map(s) | Acting Sheets (`graphics/Characters/`) | Additive / Tile VFX (`graphics/Animations/`) | Signature Rejuvenation V14 Beat | Status |
|---|---|---|---|---|---|---|
| **#1** | **Ch5 — Spire Shatter** (`:CH5_SHATTER` / `:SH1`) | `952` → `608` → `952` | `act_ch5_mourner_reach`, `act_ch5_mourner_burn`, `Followers/ELECTIVIRE` | `pf_vfx_vault_seal`, `pf_vfx_splitter_beacon`, `pf_vfx_prism_lightning`, `pf_vfx_shockwave_ring`, `pf_vfx_glass_shards`, `pf_vfx_glass_frost`, `pf_vfx_smoke_and_motes` | Darkened vault `pbZoomMap 1.48×` → `0.38s bgm_cut` → 2f impact + `0.14s` hitstop → live cutaway to Map 608 frozen Dex → Electivire leap | **LIVE PROTOTYPED & VERIFIED** |
| **#2** | **Ch9 — Trevenant Ingrain & Mourner Unmasking** (`:CH9_UNMASK` / `:IR1`) | `264` *(currently verified live on `295`)* | `act_ch9_mourner_throw`, `act_ch9_trevenant_ingrain`, `act_ch9_mourner_unmask` | `pf_vfx_fist_reliquary`, `pf_vfx_shockwave_ring`, `pf_vfx_glass_frost`, `pf_vfx_duskball_release`, `pf_vfx_ingrain_roots`, `pf_vfx_glass_shards`, `pf_vfx_smoke_and_motes` | Crimson emergency pulse → aisle dive + ballistic Dusk Ball → 5-tile gnarled emerald Ingrain wall stopping crimson volley → stray shard mask-split + `0.16s` hitstop → silent Uncle Rowan reveal | **LIVE PROTOTYPED & VERIFIED** |
| **#3** | **Ch11 — Primal Kyogre Thaw** (`:CH11_KYOGRE_THAW`) | `309` (*Sinking Quarter*) → `300` (*Thane's Harbour*) | `act_ch11_kyogre_storm` *(already exists!)* + new `act_ch11_kyogre_eye_under_ice` (`192×128` 3/4 tile overlay) | `pf_vfx_ice_fracture_tiles`, `pf_vfx_harbour_geyser`, `pfw_fx_origin_pulse` | Live ice-crack trails racing under PC's boots → `bgm_cut` dead vacuum → glowing blue-gold Primal Eye opening *underneath* transparent harbour ice tiles (`z=5`) → upward ice eruption & Kyogre breach! | Ready for Wave 2 (1 VFX + 1 acting sheet) |
| **#4** | **Ch15 — Hollow Cathedral Echo & Glassfall** (`:CH15_CATHEDRAL_ECHO`) | `394` (*Hollow Cathedral*) → `806` (*Reverse Depths*) | New `act_ch15_kestrel_gauntlet`, `act_ch15_morwen_echo`, `act_ch15_giratina_origin` | `pf_vfx_ghost_flames`, `pf_vfx_portal_tear`, `pf_vfx_prism_lightning` | Kestrel slams Resonance Gauntlet onto Spooky Plate → translucent spectral AF 290 echoes replay across cathedral tiles → Morwen turns 180° toward PC in candle-spark silence → downward barrow rift opens into Giratina 6-wing unfurl | Ready for Wave 2 (3 acting + 2 VFX sheets) |
| **#5** | **Ch19 — WAR-1 Glass Dunes Clash** (`:WAR_CLIMAX`) | `926` (*The Glass Dunes* — already built!) | Existing `act_war1_primal_kyogre`, `act_war1_reshiram`, `pfw_kyogre_*`, `pfw_reshiram` | Existing `pfw_fx_flood`, `pfw_beam_sea`, `pfw_beam_fire`, `pfw_fx_clash_core`, `pfw_fx_glass_ring` + `AdvancedAnimations#zoom_map` | Upgrade existing `013_Scenes_War_OnMap.rb` from flat `pfw_glass_dunes.png` to live `Map 926` + unified `pbZoomMap` push-ins + dead-silence `bgm_cut` glass collapse into single falling mote! | Ready for Wave 2 (0 new art required!) |
| **#6** | **Ch21 — Valen's Crystal Arm, Zygarde Assembly & Arceus Convergence** (`:CH21_CONVERGENCE`) | `491` (*Altar Stage*) + 11-lamp cross-cuts (`106`, `182`, `223`, `294`) | New `act_ch21_valen_unglove`, `act_ch21_zygarde_complete`, `act_ch21_arceus_descent` | `pf_vfx_hex_cells` (emerald Zygarde hexagonal assembly!), `pf_vfx_18plate_wheel`, `pf_vfx_golden_chains`, `pf_vfx_shockwave_ring` | Valen tears off grey glove as crystal climbs his arm → emerald hexagonal cells fly across live arena tiles assembling Zygarde Complete → Arbiter golden chains drag Arceus through cracked sky → 18-Plate radial Convergence! | Ready for Wave 3 (3 acting + 3 VFX sheets) |
| **#7** | **Ruin R7 — Mirror Pierce & Silent Crown** (`:RUIN_R7_PIERCE`) | `491` → `963` (*Ruined Crown*) → `106` (*Lighthouse*) | New `act_ruin_reflection_step`, `act_ruin_mirror_blade`, `act_ruin_valen_fall` | `pf_vfx_black_glass_shards`, `pf_vfx_glitch_scanlines`, `pf_vfx_smoke_and_motes` | Rejuvenation Renegade / Maria-impales-Vitus energy: trapped micro-control steps toward Reflection → dead-silence `bgm_cut` → 2f stark ink silhouette lunge + `0.18s` hitstop → slow monochrome aftermath on `Map 963` with zero music | Ready for Wave 3 (3 acting + 2 VFX sheets) |

---

## 5. Wednesday Sprint Merge Checklist for Claude

1. **Install `017_AdvancedAnimations.rb`:** Copy the exact verified code in §6 below into `plugins/Prismfall Cutscenes/017_AdvancedAnimations.rb`.
2. **Retire AI `.ogv` calls in `016_Movies.rb`:**
   - Redirect `CUTSCENE_SCENES[:SH1]` to call `Prismfall::AdvancedAnimations.play_ch5_spire_shatter` (and `:IR1` → `play_ch9_trevenant_unmasking`).
   - Keep `Cutscene.act` backwards-compatible for tiny inline event gestures, and remove all `Cutscene.movie("pf_*.ogv")` references from story scenes so no AI slideshow ever plays.
3. **Live-Gameplay Input Mode for `PortraitBox#say`:**
   - In `Engine#say`, add an `interactive: !@capture_dir` branch so during real player gameplay, `PortraitBox` waits for `Input.trigger?(Input::USE)` / `Input.trigger?(Input::BACK)` after typing finishes (or delegates to `pbMessage("\\pf[#{speaker_sym},#{expr}]#{text}")` when `on_map` pause is desired), while keeping `hold:` auto-advance for headless video verification captures!
4. **Canonical BGM Mapping:**
   - Map tags `"ch5_girei_intro"`, `"ch5_girei_climax"`, `"ch9_tension"`, `"ch9_never_meant"` to Prismfall's canonical `Audio/BGM/` filenames (matching `AUDIO_SOUNDTRACK_PLAN.md` / `2026-11-23_anime-ost-situational-bgm`).
5. **Map 264 Handoff:**
   - Once `mapgen` builds `Map 264` (*Iron Pit - The Reliquary*), change `eng.transfer_map(295, ...)` in `play_ch9_trevenant_unmasking` to `264` and align `(reliquary_tx, reliquary_ty)`, `(aisle_x, juno_y)` to Map 264's stairs and gallery edge.
6. **Add `selftest/suite.ruby_stub` coverage:** Verify `AdvancedAnimations::Ease`, variable `ticks:` timing sum, `photosensitive?` flash/shake/impact degradation, and zero bitmap disposal leaks.

---

## 6. Verified Live-Tested Source Code: `plugins/Prismfall Cutscenes/017_AdvancedAnimations.rb`

*(Exact file tested live inside `/home/antigravity/pf_engine_run/game/Plugins/Prismfall Cutscenes/017_AdvancedAnimations.rb` with `mkxp-z.x86_64`, exit code `0`, 1,282 captured frames across `Map 952`, `Map 608`, and `Map 295`.)*

```ruby
#===============================================================================
# Prismfall Cutscenes - 017 Rejuvenation V14 AdvancedAnimations Engine
#-------------------------------------------------------------------------------
# 100% IN-ENGINE RPG MAKER XP / mkxp-z PIXEL-ART LIVE-MAP CHOREOGRAPHY
# Modeled directly on Pokemon Rejuvenation V14's Scripts/AdvancedAnimations.rb
# and Scripts/Camera/ (pbZoomMap, pbCameraToEvent, variable frameData tick
# arrays, darkened map tone contrast, sparse 4-color additive pixel VFX,
# ramped screen flashes, dead-silence audio vacuum, and live map transforms).
#
# ZERO AI-generated movies. ZERO battlebacks. ZERO front battle sprites.
# Everything runs LIVE on the real RPG Maker XP tilemap at native 512x384!
#
# Architecture (4-Viewport Unified Pipeline):
#   1. Spriteset_Map (z=0..300)    - Real tilemap, autotiles, map events
#   2. @actor_vp     (z=350)       - Custom acting sheets & temp map actors
#                                    (syncs tone with $game_screen.tone!)
#   3. @vfx_vp       (z=420)       - Sparse 4-color additive pixel VFX sheets
#                                    (untoned so additive glow POPS on dark maps!)
#   4. @zoom_vp      (z=89000)     - pbZoomMap unified Graphics.snap_to_bitmap
#                                    scaling (zero autotile/layer tear!)
#   5. @ui_vp        (z=90000)     - Cinema letterbox, ramped flashes, 2f impact
#                                    silhouettes, and crisp Portrait Face boxes
#===============================================================================

module Prismfall
  module AdvancedAnimations
    TICK = 0.05   # Rejuvenation / Reborn standard event tick (1/20 s = 2 frames @ 40fps)
    TILE = 32
    SUB  = defined?(Game_Map::REAL_RES_X) ? Game_Map::REAL_RES_X : 128

    module Ease
      module_function
      def apply(kind, t)
        t = 0.0 if t < 0.0
        t = 1.0 if t > 1.0
        case kind
        when :linear    then t
        when :in        then t * t
        when :out       then 1.0 - ((1.0 - t) * (1.0 - t))
        when :in_out    then t < 0.5 ? (2.0 * t * t) : (1.0 - ((-2.0 * t + 2.0) ** 2) / 2.0)
        when :out_cubic then 1.0 - ((1.0 - t) ** 3)
        when :in_cubic  then t * t * t
        else t
        end
      end
    end

    #===========================================================================
    # World-space Map Actor (charset walking OR arbitrary-grid ActingClip sheet)
    # Foot-anchored at bottom-center of exact map tile (tx, ty) with real Y-sort!
    #===========================================================================
    class MapActor
      attr_reader :id, :tx, :ty, :dir, :sprite
      attr_accessor :visible, :opacity, :off_x, :off_y, :mirror

      def initialize(engine, id, sheet:, tx:, ty:, dir: :down, grid: [4, 4],
                     is_charset: true, z_bias: 0, folder: "Graphics/Characters/")
        @engine     = engine
        @id         = id
        @tx         = tx.to_f
        @ty         = ty.to_f
        @dir        = dir
        @folder     = folder
        @is_charset = is_charset
        @z_bias     = z_bias
        @off_x      = 0.0
        @off_y      = 0.0
        @visible    = true
        @opacity    = 255
        @mirror     = false
        @walk_phase = 0.0
        @walking    = false
        @move_task  = nil
        @hop_task   = nil
        @clip       = nil
        @emote      = nil
        @sprite     = Sprite.new(engine.actor_vp)
        load_sheet(sheet, grid, is_charset)
        sync_screen_pos
      end

      def load_sheet(name, grid = [4, 4], is_charset = false)
        path = name.start_with?("Graphics/") ? name : (@folder + name)
        @bmp = @engine.cached_bitmap(path)
        @cols, @rows = grid
        @is_charset = is_charset
        @cw = @bmp.width / @cols
        @ch = @bmp.height / @rows
        @sprite.bitmap = @bmp
        @sprite.ox = @cw / 2
        foot_pad = if name.include?("act_ch5_mourner") then 8
                   elsif name.include?("act_ch9_mourner_throw") then 6
                   elsif name.include?("act_ch9_trevenant") then 1
                   else 4
                   end
        @sprite.oy = @ch - foot_pad
        if @is_charset
          set_charset_frame(@dir, 0)
        else
          set_cell(0)
        end
      end

      def set_dir(dir)
        @dir = dir
        set_charset_frame(@dir, 0) if @is_charset && !@clip
      end

      def set_charset_frame(dir, pat)
        row = { :down => 0, :left => 1, :right => 2, :up => 3 }[dir] || 0
        @sprite.src_rect.set((pat % @cols) * @cw, row * @ch, @cw, @ch)
      end

      def set_cell(cell)
        col = cell % @cols
        row = (cell / @cols) % @rows
        @sprite.src_rect.set(col * @cw, row * @ch, @cw, @ch)
      end

      def move_to(tx2, ty2, duration:, walk: true, dir: nil, ease: :linear, arc_h: 0.0)
        dx = tx2 - @tx
        dy = ty2 - @ty
        if dir
          @dir = dir
        elsif dx.abs > dy.abs
          @dir = dx >= 0 ? :right : :left
        elsif dy.abs > 0.01
          @dir = dy >= 0 ? :down : :up
        end
        @walking = walk
        @move_task = {
          :x0 => @tx, :y0 => @ty, :x1 => tx2.to_f, :y1 => ty2.to_f,
          :t => 0.0, :dur => [duration.to_f, 0.001].max, :ease => ease, :arc_h => arc_h.to_f
        }
      end

      def hop(height: 14, duration: 0.28)
        @hop_task = { :h => height.to_f, :t => 0.0, :dur => [duration.to_f, 0.001].max }
      end

      # Rejuvenation V14 AdvancedAnimations variable-tick frameData playback!
      def play_clip(sheet:, grid: [4, 4], frames: nil, ticks: nil, holds: nil,
                    se: {}, cry: {}, shake: {}, flash: {}, hitstop: {}, on_frame: {},
                    loops: 1, stay: true)
        load_sheet(sheet, grid, false)
        list = (frames || (0...(grid[0] * grid[1]))).to_a
        if holds
          h_arr = Array(holds).map(&:to_f)
        elsif ticks
          h_arr = Array(ticks).map { |tk| tk.to_f * TICK }
        else
          h_arr = [0.10]
        end
        dur_list = list.each_index.map { |i| h_arr[[i, h_arr.length - 1].min] }
        @clip = {
          :frames => list, :holds => dur_list, :idx => -1, :t => 0.0,
          :loop => 0, :loops => loops, :stay => stay,
          :se => se || {}, :cry => cry || {}, :shake => shake || {},
          :flash => flash || {}, :hitstop => hitstop || {}, :on_frame => on_frame || {},
          :done => false
        }
        advance_clip_to(0)
      end

      def clip_done?; !@clip || @clip[:done]; end
      def moving?; !@move_task.nil?; end

      def show_emote(kind = :exclaim, duration: 0.55)
        dispose_emote
        @emote = { :sp => Sprite.new(@engine.vfx_vp), :t => 0.0, :dur => duration }
        bmp = Bitmap.new(24, 28)
        # Crisp 2x pixel-art exclamation / shock speech bubble
        bg = Color.new(255, 255, 255)
        ol = Color.new(24, 24, 32)
        ac = (kind == :shock) ? Color.new(236, 48, 64) : Color.new(236, 64, 56)
        bmp.fill_rect(2, 2, 20, 18, ol)
        bmp.fill_rect(4, 4, 16, 14, bg)
        bmp.fill_rect(8, 20, 8, 4, ol)
        bmp.fill_rect(10, 18, 4, 4, bg)
        bmp.fill_rect(10, 24, 4, 2, ol)
        # Red "!" pixels (2x crisp)
        bmp.fill_rect(10, 6, 4, 6, ac)
        bmp.fill_rect(10, 14, 4, 2, ac)
        @emote[:sp].bitmap = bmp
        @emote[:sp].ox = 12
        @emote[:sp].oy = 28
        @emote[:sp].z = 950
      end

      def dispose_emote
        return if !@emote
        sp = @emote[:sp]
        if sp && !sp.disposed?
          sp.bitmap.dispose if sp.bitmap && !sp.bitmap.disposed?
          sp.dispose
        end
        @emote = nil
      end

      def screen_pos
        sx, sy = @engine.tile_to_screen(@tx, @ty)
        hop_y = 0.0
        if @hop_task
          u = @hop_task[:t] / @hop_task[:dur]
          hop_y = -Math.sin(u * Math::PI) * @hop_task[:h]
        end
        arc_y = 0.0
        if @move_task && @move_task[:arc_h] > 0.0
          u = @move_task[:t] / @move_task[:dur]
          arc_y = -Math.sin(u * Math::PI) * @move_task[:arc_h]
        end
        return sx + @off_x, sy + @off_y + hop_y + arc_y
      end

      def update(dt)
        if @move_task
          @move_task[:t] += dt
          u = [@move_task[:t] / @move_task[:dur], 1.0].min
          k = Ease.apply(@move_task[:ease], u)
          @tx = @move_task[:x0] + (@move_task[:x1] - @move_task[:x0]) * k
          @ty = @move_task[:y0] + (@move_task[:y1] - @move_task[:y0]) * k
          if @walking && @is_charset && !@clip
            @walk_phase += dt * 7.5
            set_charset_frame(@dir, @walk_phase.to_i % @cols)
          end
          if u >= 1.0
            @tx = @move_task[:x1]
            @ty = @move_task[:y1]
            @move_task = nil
            @walking = false
            set_charset_frame(@dir, 0) if @is_charset && !@clip
          end
        end

        if @hop_task
          @hop_task[:t] += dt
          @hop_task = nil if @hop_task[:t] >= @hop_task[:dur]
        end

        if @clip && !@clip[:done]
          @clip[:t] += dt
          cur_h = @clip[:holds][@clip[:idx]]
          while @clip[:t] >= cur_h && !@clip[:done]
            @clip[:t] -= cur_h
            nxt = @clip[:idx] + 1
            if nxt >= @clip[:frames].length
              @clip[:loop] += 1
              if @clip[:loops] == :forever || @clip[:loop] < @clip[:loops]
                advance_clip_to(0)
                cur_h = @clip[:holds][0]
              else
                @clip[:done] = true
                @clip = nil if !@clip[:stay]
                break
              end
            else
              advance_clip_to(nxt)
              cur_h = @clip[:holds][nxt]
            end
          end
        end

        sync_screen_pos

        if @emote
          @emote[:t] += dt
          if @emote[:t] >= @emote[:dur]
            dispose_emote
          else
            sx, sy = screen_pos
            pop = @emote[:t] < 0.08 ? ((1.0 - @emote[:t] / 0.08) * 6.0) : 0.0
            @emote[:sp].x = sx.round
            @emote[:sp].y = (sy - 44 + pop).round
          end
        end
      end

      def sync_screen_pos
        sx, sy = screen_pos
        @sprite.x = sx.round
        @sprite.y = sy.round
        @sprite.z = sy.round + @z_bias
        @sprite.visible = @visible
        @sprite.opacity = @opacity.round
        @sprite.mirror  = @mirror
      end

      def dispose
        dispose_emote
        @sprite.dispose if @sprite && !@sprite.disposed?
      end

      private

      def advance_clip_to(i)
        @clip[:idx] = i
        cell = @clip[:frames][i]
        set_cell(cell)
        @engine.play_se(@clip[:se][i]) if @clip[:se][i]
        @engine.play_cry(@clip[:cry][i]) if @clip[:cry][i]
        if (sh = @clip[:shake][i])
          @engine.shake(power: sh[0], duration: sh[1] || 0.25)
        end
        if (fl = @clip[:flash][i])
          @engine.flash(color: fl[0], power: fl[1] || 180, duration: fl[2] || 0.16)
        end
        if (hs = @clip[:hitstop][i])
          @engine.trigger_hitstop(hs)
        end
        @clip[:on_frame][i].call(@engine, self, i) if @clip[:on_frame][i]
      end
    end

    #===========================================================================
    # World-space Crisp Pixel VFX Sprite (locked to live map tile coordinates!)
    #===========================================================================
    class MapVfx
      attr_reader :id, :done

      def initialize(engine, id, sheet:, tx:, ty:, grid: [4, 1], frames: nil,
                     ticks: nil, holds: nil, hold: 0.06, blend: :add,
                     scale: 1.0, grow: nil, loops: 1, stay: 0.0, fade: 0.0,
                     move_to: nil, arc_h: 0.0, drift: nil, gravity: 0.0, spin: 0.0,
                     offset: [0, 0], z_layer: :above, opacity: 255, untoned: nil,
                     origin: :center, mirror: false)
        @engine  = engine
        @id      = id
        @tx      = tx.to_f
        @ty      = ty.to_f
        @tx0     = @tx
        @ty0     = @ty
        @cols, @rows = grid
        @frames  = (frames || (0...(@cols * @rows))).to_a
        if holds
          h_arr = Array(holds).map(&:to_f)
        elsif ticks
          h_arr = Array(ticks).map { |tk| tk.to_f * TICK }
        else
          h_arr = [hold.to_f]
        end
        @holds   = @frames.each_index.map { |i| h_arr[[i, h_arr.length - 1].min] }
        @total   = [@holds.sum, 0.001].max
        @loops   = loops
        @stay    = stay
        @fade    = fade.to_f
        @scale   = scale.to_f
        @grow    = grow
        @move_to = move_to   # [tx2, ty2, dur]
        @arc_h   = arc_h.to_f
        @drift   = drift     # [vx_px, vy_px]
        @gravity = gravity.to_f
        @spin    = spin.to_f
        @offset  = offset
        @z_layer = z_layer
        @opacity = opacity.to_f
        @t       = 0.0
        @done    = false

        use_vfx_vp = if z_layer == :floor
                       false
                     else
                       untoned.nil? ? (blend == :add) : untoned
                     end
        vp = use_vfx_vp ? engine.vfx_vp : engine.actor_vp
        path = sheet.start_with?("Graphics/") ? sheet : ("Graphics/Animations/" + sheet)
        @bmp = engine.cached_bitmap(path)
        @cw = @bmp.width / @cols
        @ch = @bmp.height / @rows
        @sprite = Sprite.new(vp)
        @sprite.bitmap = @bmp
        if origin == :foot
          @sprite.ox = @cw / 2
          @sprite.oy = @ch - 8
        else
          @sprite.ox = @cw / 2
          @sprite.oy = @ch / 2
        end
        @sprite.blend_type = { :add => 1, :sub => 2, :normal => 0 }[blend] || 0
        @sprite.mirror = mirror
        update(0.0)
      end

      def stop!; @done = true; end

      def update(dt)
        return true if @done
        @t += dt
        life = (@loops == :forever || @stay == :forever) ? nil : (@total * @loops) + @stay.to_f
        if life && @t >= life
          @done = true
          return true
        end

        # Frame selection
        if @loops != :forever && @t >= @total * @loops
          i = @frames.length - 1
        else
          tm = @t % @total
          i = 0
          acc = 0.0
          while i < @frames.length - 1 && tm >= (acc += @holds[i])
            i += 1
          end
        end
        cell = @frames[i]
        @sprite.src_rect.set((cell % @cols) * @cw, (cell / @cols) * @ch, @cw, @ch)

        # Tile movement / parabolic arc
        arc_y = 0.0
        if @move_to
          u = [@t / [@move_to[2].to_f, 0.001].max, 1.0].min
          @tx = @tx0 + (@move_to[0] - @tx0) * u
          @ty = @ty0 + (@move_to[1] - @ty0) * u
          arc_y = -Math.sin(u * Math::PI) * @arc_h if @arc_h > 0.0
        end

        sx, sy = @engine.tile_to_screen(@tx, @ty)
        # tile_to_screen returns foot anchor; center-anchored VFX sit at tile center (sy - 16)
        base_y = (@sprite.oy == @ch / 2) ? (sy - 16) : sy
        px = sx + @offset[0]
        py = base_y + @offset[1] + arc_y
        if @drift
          px += @drift[0] * @t
          py += (@drift[1] * @t) + (0.5 * @gravity * @t * @t)
        end

        @sprite.x = px.round
        @sprite.y = py.round
        @sprite.z = case @z_layer
                    when :floor then 5
                    when :mid   then sy.round + 2
                    else             700 + sy.round / 4
                    end

        sc = @scale
        if @grow
          u = [@t / [@grow[2].to_f, 0.001].max, 1.0].min
          sc *= @grow[0] + (@grow[1] - @grow[0]) * Ease.apply(:out, u)
        end
        @sprite.zoom_x = sc
        @sprite.zoom_y = sc
        @sprite.angle  = @spin * @t

        op = @opacity
        if @fade > 0.0 && life && (life - @t) < @fade
          op *= [(life - @t) / @fade, 0.0].max
        end
        @sprite.opacity = op.round
        return false
      end

      def dispose
        @sprite.dispose if @sprite && !@sprite.disposed?
      end
    end

    #===========================================================================
    # Crisp In-Engine Portrait Dialogue Overlay (Desolation/Rejuv FaceWindowVX)
    # Keeps live map, lighting, roots, smoke, and camera running underneath!
    #===========================================================================
    class PortraitBox
      def initialize(ui_vp, speaker_sym, expression, text, engine)
        @engine = engine
        @vp = ui_vp
        @sprites = []
        @text = text.to_s
        @name = speaker_sym.to_s.capitalize
        @chars_shown = 0.0
        @done_typing = false

        box_y = Graphics.height - 98
        box_h = 86
        # 1. Portrait Frame (104x104 on left edge, sitting right beside box)
        face_x = 12
        face_y = box_y - 18
        @face_bg = Sprite.new(@vp)
        @face_bg.z = 9500
        fb = Bitmap.new(104, 104)
        fb.fill_rect(0, 0, 104, 104, Color.new(18, 22, 34, 240))
        fb.fill_rect(2, 2, 100, 100, Color.new(210, 218, 236, 255))
        fb.fill_rect(4, 4, 96, 96, Color.new(26, 30, 44, 255))
        @face_bg.bitmap = fb
        @face_bg.x = face_x
        @face_bg.y = face_y
        @sprites << @face_bg

        p_bmp = load_portrait(speaker_sym, expression)
        if p_bmp
          @face_sp = Sprite.new(@vp)
          @face_sp.bitmap = p_bmp
          @face_sp.z = 9505
          @face_sp.x = face_x + 4 + (96 - p_bmp.width) / 2
          @face_sp.y = face_y + 4 + (96 - p_bmp.height) / 2
          @sprites << @face_sp
        end

        # 2. Message Frame (clean dark-slate Rejuv/Desolation style with crisp border)
        msg_x = 122
        msg_w = Graphics.width - msg_x - 12
        @box = Sprite.new(@vp)
        @box.z = 9500
        bb = Bitmap.new(msg_w, box_h)
        bb.fill_rect(0, 0, msg_w, box_h, Color.new(16, 20, 30, 238))
        bb.fill_rect(2, 2, msg_w - 4, box_h - 4, Color.new(208, 216, 234, 255))
        bb.fill_rect(4, 4, msg_w - 8, box_h - 8, Color.new(22, 26, 38, 244))
        @box.bitmap = bb
        @box.x = msg_x
        @box.y = box_y
        @sprites << @box

        # 3. Speaker Nameplate Tab
        @name_sp = Sprite.new(@vp)
        @name_sp.z = 9510
        nb = Bitmap.new(136, 28)
        nb.fill_rect(0, 0, 136, 28, Color.new(16, 20, 30, 248))
        nb.fill_rect(2, 2, 132, 24, Color.new(208, 216, 234, 255))
        nb.fill_rect(4, 4, 128, 20, Color.new(34, 40, 58, 255))
        set_font(nb, 18, true)
        nb.font.color = Color.new(255, 236, 176)
        nb.draw_text(8, 2, 120, 24, @name, 0)
        @name_sp.bitmap = nb
        @name_sp.x = msg_x + 6
        @name_sp.y = box_y - 22
        @sprites << @name_sp

        # 4. Crisp Text Bitmap
        @txt_sp = Sprite.new(@vp)
        @txt_sp.z = 9515
        @txt_bmp = Bitmap.new(msg_w - 22, box_h - 14)
        set_font(@txt_bmp, 20, false)
        @txt_sp.bitmap = @txt_bmp
        @txt_sp.x = msg_x + 12
        @txt_sp.y = box_y + 10
        @sprites << @txt_sp

        @wrapped = wrap_lines(@text, @txt_bmp, msg_w - 26)
        @total_chars = @wrapped.join.length
        @last_drawn = -1
      end

      def load_portrait(sym, expr)
        base = "Graphics/Portraits/#{sym.to_s.upcase}"
        ["#{base}_#{expr}.png", "#{base}.png"].each do |p|
          return Bitmap.new(p) if File.exist?(p)
        end
        return nil
      end

      def set_font(bmp, size, bold)
        bmp.font.name = ["Power Clear", "Liberation Sans", "DejaVu Sans"]
        bmp.font.size = size
        bmp.font.bold = bold
      end

      def wrap_lines(str, bmp, max_w)
        lines = []
        cur = ""
        str.split(" ").each do |w|
          cand = cur.empty? ? w : "#{cur} #{w}"
          if bmp.text_size(cand).width > max_w && !cur.empty?
            lines << cur
            cur = w
          else
            cur = cand
          end
        end
        lines << cur if !cur.empty?
        lines
      end

      def update(dt)
        @chars_shown = [@chars_shown + dt * 44.0, @total_chars.to_f].min
        n = @chars_shown.to_i
        @done_typing = (n >= @total_chars)
        return if n == @last_drawn
        @last_drawn = n
        @txt_bmp.clear
        rem = n
        @wrapped.each_with_index do |line, li|
          break if rem <= 0
          sub = line[0, [rem, line.length].min]
          rem -= line.length
          # Crisp 1px shadow + white text
          @txt_bmp.font.color = Color.new(10, 12, 18)
          @txt_bmp.draw_text(1, li * 23 + 1, @txt_bmp.width, 26, sub, 0)
          @txt_bmp.font.color = Color.new(244, 248, 255)
          @txt_bmp.draw_text(0, li * 23, @txt_bmp.width, 26, sub, 0)
        end
      end

      def done_typing?; @done_typing; end

      def dispose
        @sprites.each do |s|
          next if !s || s.disposed?
          s.bitmap.dispose if s.bitmap && !s.bitmap.disposed?
          s.dispose
        end
        @sprites.clear
      end
    end

    #===========================================================================
    # Master Rejuvenation V14 Live-Map Choreography Engine
    #===========================================================================
    class Engine
      attr_reader :actor_vp, :vfx_vp, :ui_vp, :time, :cues, :frames_captured

      def initialize(capture_dir: nil, capture_fps: 30)
        @capture_dir = capture_dir
        @capture_fps = capture_fps
        @fixed_dt    = capture_dir ? (1.0 / capture_fps.to_f) : nil
        @frames_captured = 0
        @time        = 0.0
        @cues        = []
        @bmp_cache   = {}
        @actors      = {}
        @vfxs        = []

        # 4-viewport layered pipeline!
        @actor_vp = Viewport.new(0, 0, Graphics.width, Graphics.height)
        @actor_vp.z = 350

        @vfx_vp = Viewport.new(0, 0, Graphics.width, Graphics.height)
        @vfx_vp.z = 420

        @zoom_vp = Viewport.new(0, 0, Graphics.width, Graphics.height)
        @zoom_vp.z = 89_000
        @zoom_sp = Sprite.new(@zoom_vp)
        @zoom_sp.visible = false

        @ui_vp = Viewport.new(0, 0, Graphics.width, Graphics.height)
        @ui_vp.z = 90_000

        # Cinema widescreen bars
        @bar_h = 0.0
        @bar_task = nil
        @bar_top = Sprite.new(@ui_vp)
        @bar_top.bitmap = Bitmap.new(Graphics.width, 4)
        @bar_top.bitmap.fill_rect(0, 0, Graphics.width, 4, Color.new(0, 0, 0))
        @bar_top.z = 9100
        @bar_top.visible = false

        @bar_bot = Sprite.new(@ui_vp)
        @bar_bot.bitmap = @bar_top.bitmap
        @bar_bot.z = 9100
        @bar_bot.visible = false

        # Screen flash / impact silhouette overlay
        @flash_sp = Sprite.new(@ui_vp)
        @flash_sp.bitmap = Bitmap.new(Graphics.width, Graphics.height)
        @flash_sp.z = 9200
        @flash_sp.opacity = 0
        @flash_task = nil

        # Red emergency vignette / edge glow sprite
        @vig_sp = Sprite.new(@ui_vp)
        @vig_sp.bitmap = Bitmap.new(Graphics.width, Graphics.height)
        @vig_sp.z = 9050
        @vig_sp.opacity = 0
        @vig_pulse = nil

        # Camera state (pbZoomMap + smooth tile scroll + shake)
        @zoom       = 1.0
        @zoom_focus = nil   # :player, actor_id, or [tx, ty]
        @zoom_task  = nil
        @cam_tx     = nil
        @cam_ty     = nil
        @cam_task   = nil
        @shake_task = nil
        @shake_x    = 0.0
        @shake_y    = 0.0
        @tone       = [0.0, 0.0, 0.0, 0.0]
        @tone_task  = nil
        @hitstop    = 0.0
        @dialogue   = nil
        @last_tick  = System.uptime
      end

      def photosensitive?
        Prismfall::Cutscene.photosensitive? rescue false
      end

      def cached_bitmap(path)
        p = path.end_with?(".png") ? path : "#{path}.png"
        bmp = @bmp_cache[p]
        return bmp if bmp && !bmp.disposed?
        bmp = Bitmap.new(p)
        @bmp_cache[p] = bmp
        bmp
      end

      def log_cue(kind, detail = {})
        @cues << { "t" => @time.round(4), "kind" => kind.to_s }.merge(detail)
      end

      #-------------------------------------------------------------------------
      # Audio Cues (played live in-engine AND logged frame-exact for video mux!)
      #-------------------------------------------------------------------------
      def play_bgm(name, volume: 85, tag: nil)
        log_cue("bgm", "name" => name.to_s, "volume" => volume, "tag" => (tag || name).to_s)
        pbBGMPlay(name, volume) rescue nil
      end

      def bgm_cut
        log_cue("bgm_cut")
        Audio.bgm_stop rescue nil
      end

      def bgm_fade(sec = 0.8)
        log_cue("bgm_fade", "sec" => sec)
        Audio.bgm_fade((sec * 1000).round) rescue nil
      end

      def play_se(name, volume: 90, pitch: 100)
        log_cue("se", "name" => name.to_s, "volume" => volume, "pitch" => pitch)
        pbSEPlay(name, volume, pitch) rescue nil
      end

      def play_cry(species, volume: 95)
        log_cue("cry", "species" => species.to_s, "volume" => volume)
        GameData::Species.play_cry_from_species(species, 0, volume) rescue (pbSEPlay("Cries/#{species}", volume) rescue nil)
      end

      #-------------------------------------------------------------------------
      # Map & Camera Controls (pbCameraScrollTo, pbZoomMap, tone, shake, bars)
      #-------------------------------------------------------------------------
      def tile_to_screen(tx, ty)
        sx = ((tx * SUB - $game_map.display_x + 3) / 4.0) + 16.0
        sy = ((ty * SUB - $game_map.display_y + 3) / 4.0) + 32.0
        return sx, sy
      end

      def set_camera_tile(tx, ty)
        @cam_tx = tx.to_f
        @cam_ty = ty.to_f
        apply_camera_display
      end

      def pan_camera_to(tx, ty, duration: 0.6, ease: :in_out)
        @cam_tx ||= (($game_map.display_x / 4.0) + Graphics.width / 2.0 - 16.0) / 32.0
        @cam_ty ||= (($game_map.display_y / 4.0) + Graphics.height / 2.0 - 16.0) / 32.0
        @cam_task = {
          :x0 => @cam_tx, :y0 => @cam_ty, :x1 => tx.to_f, :y1 => ty.to_f,
          :t => 0.0, :dur => [duration.to_f, 0.001].max, :ease => ease
        }
      end

      def zoom_map(goal, duration: 0.45, focus: nil, ease: :in_out)
        @zoom_focus = focus if !focus.nil?
        if duration <= 0.001
          @zoom = goal.to_f
          @zoom_task = nil
        else
          @zoom_task = {
            :z0 => @zoom, :z1 => goal.to_f,
            :t => 0.0, :dur => duration.to_f, :ease => ease
          }
        end
      end

      def set_tone(r, g, b, gray = 0, duration: 0.5)
        target = [r.to_f, g.to_f, b.to_f, gray.to_f]
        if duration <= 0.001
          @tone = target
          @tone_task = nil
          apply_tone
        else
          @tone_task = { :from => @tone.dup, :to => target, :t => 0.0, :dur => duration.to_f }
        end
      end

      def set_emergency_vignette(rgb = [210, 28, 36], max_alpha: 72, pulse_hz: 1.1)
        b = @vig_sp.bitmap
        b.clear
        w, h = b.width, b.height
        # Crisp stepped pixel-art dithered edge border glow (never muddy blur!)
        [24, 14, 6].each_with_index do |band, bi|
          alpha = [55, 110, 175][bi]
          col = Color.new(rgb[0], rgb[1], rgb[2], alpha)
          b.fill_rect(0, 0, w, band, col)
          b.fill_rect(0, h - band, w, band, col)
          b.fill_rect(0, band, band, h - band * 2, col)
          b.fill_rect(w - band, band, band, h - band * 2, col)
        end
        @vig_pulse = { :max => max_alpha.to_f, :hz => pulse_hz.to_f, :t => 0.0 }
      end

      def clear_vignette
        @vig_pulse = nil
        @vig_sp.opacity = 0
      end

      def letterbox(on, height: 32, duration: 0.35)
        goal = on ? height.to_f : 0.0
        if duration <= 0.001
          @bar_h = goal
          @bar_task = nil
          sync_bars
        else
          @bar_task = { :from => @bar_h, :to => goal, :t => 0.0, :dur => duration.to_f }
        end
      end

      def shake(power: 5, duration: 0.35, decay: true)
        p = photosensitive? ? (power.to_f * 0.2) : power.to_f
        @shake_task = { :p => p, :t => 0.0, :dur => [duration.to_f, 0.001].max, :decay => decay }
      end

      def flash(color: [255, 255, 255], power: 220, duration: 0.25)
        p = photosensitive? ? [power, 64].min : power
        @flash_sp.bitmap.fill_rect(0, 0, Graphics.width, Graphics.height, Color.new(color[0], color[1], color[2]))
        @flash_sp.opacity = p
        @flash_task = { :mode => :fade, :p => p.to_f, :t => 0.0, :dur => [duration.to_f, 0.001].max }
      end

      # Reborn/Rejuvenation ramped flash: 17 -> 51 -> 136 -> 221 -> 255 -> hold -> fade
      def flash_ramp(color: [255, 255, 255], steps: [17, 51, 136, 221, 255],
                     step_dur: 0.035, hold_dur: 0.14, fade_dur: 0.35)
        @flash_sp.bitmap.fill_rect(0, 0, Graphics.width, Graphics.height, Color.new(color[0], color[1], color[2]))
        if photosensitive?
          steps = steps.map { |v| [v / 4, 60].min }
          hold_dur = 0.04
        end
        @flash_task = {
          :mode => :ramp, :steps => steps, :step_dur => step_dur,
          :hold_dur => hold_dur, :fade_dur => fade_dur, :t => 0.0
        }
      end

      # Classic 2-frame high-contrast B&W impact beat + real-clock hitstop!
      def impact_beat(hitstop_sec: 0.14, color_a: [255, 255, 255], color_b: [16, 12, 24])
        if !photosensitive?
          @flash_sp.bitmap.fill_rect(0, 0, Graphics.width, Graphics.height, Color.new(*color_a))
          @flash_sp.opacity = 235
          step_frame(true)
          @flash_sp.bitmap.fill_rect(0, 0, Graphics.width, Graphics.height, Color.new(*color_b))
          @flash_sp.opacity = 210
          step_frame(true)
          @flash_sp.opacity = 0
        end
        trigger_hitstop(hitstop_sec) if hitstop_sec > 0.0
      end

      def trigger_hitstop(sec)
        @hitstop = [@hitstop, sec.to_f].max
      end

      #-------------------------------------------------------------------------
      # Actor & VFX Spawning
      #-------------------------------------------------------------------------
      def spawn_actor(id, **opts)
        remove_actor(id)
        @actors[id] = MapActor.new(self, id, **opts)
      end

      def actor(id); @actors[id]; end

      def remove_actor(id)
        a = @actors.delete(id)
        a.dispose if a
      end

      def clear_actors
        @actors.each_value(&:dispose)
        @actors.clear
      end

      def spawn_vfx(id = nil, **opts)
        v = MapVfx.new(self, id, **opts)
        @vfxs << v
        v
      end

      def stop_vfx(id)
        @vfxs.each { |v| v.stop! if v.id == id }
      end

      def clear_vfxs
        @vfxs.each(&:dispose)
        @vfxs.clear
      end

      #-------------------------------------------------------------------------
      # Dialogue + Timeline Wait Helpers
      #-------------------------------------------------------------------------
      def say(speaker_sym, expr, text, hold: 1.55)
        @dialogue.dispose if @dialogue
        @dialogue = PortraitBox.new(@ui_vp, speaker_sym, expr, text, self)
        until @dialogue.done_typing?
          step_frame
        end
        wait(hold)
        @dialogue.dispose
        @dialogue = nil
      end

      def wait(seconds)
        target = @time + seconds.to_f
        step_frame while @time < target
      end

      def wait_for_clip(actor_id)
        a = @actors[actor_id]
        return if !a
        step_frame until a.clip_done?
      end

      def wait_for_move(actor_id)
        a = @actors[actor_id]
        return if !a
        step_frame until !a.moving?
      end

      # Seamless live map transfer (B2W2 / Rejuv V14 cross-cut!)
      def transfer_map(map_id, cam_tx, cam_ty, hide_player: true)
        clear_actors
        clear_vfxs
        @zoom = 1.0
        @zoom_task = nil
        @zoom_sp.visible = false
        $game_temp.player_transferring = false
        $game_map.setup(map_id)
        $game_player.moveto(cam_tx.round, cam_ty.round)
        $game_player.transparent = hide_player
        $scene.disposeSpritesets if $scene.respond_to?(:disposeSpritesets)
        $scene.createSpritesets  if $scene.respond_to?(:createSpritesets)
        set_camera_tile(cam_tx, cam_ty)
        apply_tone
        # Force 1 silent update so Spriteset_Map refreshes cleanly before next capture
        $game_map.update
        $scene.miniupdate if $scene.respond_to?(:miniupdate)
      end

      #-------------------------------------------------------------------------
      # Frame Update + Unified pbZoomMap Snap + Lossless Capture
      #-------------------------------------------------------------------------
      def step_frame(ignore_hitstop = false)
        dt = @fixed_dt || begin
          now = System.uptime
          d = [[now - @last_tick, 0.001].max, 0.05].min
          @last_tick = now
          d
        end
        @time += dt

        # Hitstop freezes actor/VFX motion while camera shake & audio keep living!
        world_dt = (!ignore_hitstop && @hitstop > 0.0) ? 0.0 : dt
        if !ignore_hitstop && @hitstop > 0.0
          @hitstop = [@hitstop - dt, 0.0].max
        end

        update_camera(dt)
        update_tone(dt)
        update_bars(dt)
        update_flash(dt)
        update_vignette(dt)

        # Keep real RPG Maker XP map events & autotiles alive underneath!
        if world_dt > 0.0
          $game_map.update
          apply_camera_display
          $scene.miniupdate if $scene.respond_to?(:miniupdate)
        end

        @actors.each_value { |a| a.update(world_dt) }
        @vfxs.reject! do |v|
          finished = v.update(world_dt)
          v.dispose if finished
          finished
        end
        @dialogue.update(dt) if @dialogue

        # Apply shake directly to world viewports when not zoomed
        if @zoom <= 1.001
          @actor_vp.ox = -@shake_x.round
          @actor_vp.oy = -@shake_y.round
          @vfx_vp.ox   = -@shake_x.round
          @vfx_vp.oy   = -@shake_y.round
          @zoom_sp.visible = false
        else
          @actor_vp.ox = 0
          @actor_vp.oy = 0
          @vfx_vp.ox   = 0
          @vfx_vp.oy   = 0
          render_zoom_snapshot
        end

        Graphics.update
        Input.update if !@fixed_dt

        if @capture_dir
          Graphics.screenshot(format("%s/f%05d.png", @capture_dir, @frames_captured))
          @frames_captured += 1
        end
      end

      def dispose
        @dialogue.dispose if @dialogue
        clear_actors
        clear_vfxs
        if @zoom_sp && !@zoom_sp.disposed?
          @zoom_sp.bitmap.dispose if @zoom_sp.bitmap && !@zoom_sp.bitmap.disposed?
          @zoom_sp.dispose
        end
        [@bar_bot, @bar_top, @flash_sp, @vig_sp].each do |s|
          next if !s || s.disposed?
          s.bitmap.dispose if s.bitmap && !s.bitmap.disposed? && s != @bar_bot
          s.dispose
        end
        @bmp_cache.each_value { |b| b.dispose if b && !b.disposed? }
        @bmp_cache.clear
        [@actor_vp, @vfx_vp, @zoom_vp, @ui_vp].each { |v| v.dispose if v && !v.disposed? }
        $game_screen.tone.set(0, 0, 0, 0) if $game_screen
      end

      private

      def apply_camera_display
        return if @cam_tx.nil? || @cam_ty.nil?
        max_x = [($game_map.width - Graphics.width / 32.0) * SUB, 0].max
        max_y = [($game_map.height - Graphics.height / 32.0) * SUB, 0].max
        dx = (@cam_tx * SUB) - ((Graphics.width / 2.0 - 16.0) * 4.0)
        dy = (@cam_ty * SUB) - ((Graphics.height / 2.0 - 16.0) * 4.0)
        $game_map.display_x = [[dx, 0.0].max, max_x].min.round
        $game_map.display_y = [[dy, 0.0].max, max_y].min.round
      end

      def update_camera(dt)
        if @cam_task
          @cam_task[:t] += dt
          u = [@cam_task[:t] / @cam_task[:dur], 1.0].min
          k = Ease.apply(@cam_task[:ease], u)
          @cam_tx = @cam_task[:x0] + (@cam_task[:x1] - @cam_task[:x0]) * k
          @cam_ty = @cam_task[:y0] + (@cam_task[:y1] - @cam_task[:y0]) * k
          @cam_task = nil if u >= 1.0
          apply_camera_display
        end

        if @zoom_task
          @zoom_task[:t] += dt
          u = [@zoom_task[:t] / @zoom_task[:dur], 1.0].min
          k = Ease.apply(@zoom_task[:ease], u)
          @zoom = @zoom_task[:z0] + (@zoom_task[:z1] - @zoom_task[:z0]) * k
          @zoom_task = nil if u >= 1.0
        end

        if @shake_task
          @shake_task[:t] += dt
          if @shake_task[:t] >= @shake_task[:dur]
            @shake_task = nil
            @shake_x = @shake_y = 0.0
          else
            u = @shake_task[:t] / @shake_task[:dur]
            amp = @shake_task[:decay] ? (@shake_task[:p] * (1.0 - u)) : @shake_task[:p]
            ph = @shake_task[:t] * 58.0
            @shake_x = Math.sin(ph) * amp
            @shake_y = Math.cos(ph * 1.37) * amp * 0.65
          end
        else
          @shake_x = @shake_y = 0.0
        end
      end

      def focus_screen_point
        case @zoom_focus
        when Array
          sx, sy = tile_to_screen(@zoom_focus[0], @zoom_focus[1])
          return sx, sy - 16.0
        when Symbol
          if @actors[@zoom_focus]
            sx, sy = @actors[@zoom_focus].screen_pos
            return sx, sy - 20.0
          end
        end
        return Graphics.width / 2.0, Graphics.height / 2.0
      end

      # Rejuvenation V14 Scripts/Camera/pbZoomMap unified snapshot zoom!
      def render_zoom_snapshot
        @zoom_vp.visible = false
        @ui_vp.visible   = false
        snap = Graphics.snap_to_bitmap
        @ui_vp.visible   = true
        @zoom_vp.visible = true

        old = @zoom_sp.bitmap
        @zoom_sp.bitmap = snap
        old.dispose if old && !old.disposed?

        fx, fy = focus_screen_point
        fx = [[fx, 64.0].max, Graphics.width - 64.0].min
        fy = [[fy, 64.0].max, Graphics.height - 64.0].min
        @zoom_sp.ox = fx.round
        @zoom_sp.oy = fy.round
        @zoom_sp.x  = (Graphics.width / 2.0 + @shake_x).round
        @zoom_sp.y  = (Graphics.height / 2.0 + @shake_y).round
        @zoom_sp.zoom_x = @zoom
        @zoom_sp.zoom_y = @zoom
        @zoom_sp.visible = true
      end

      def update_tone(dt)
        return if !@tone_task
        @tone_task[:t] += dt
        u = [@tone_task[:t] / @tone_task[:dur], 1.0].min
        4.times { |i| @tone[i] = @tone_task[:from][i] + (@tone_task[:to][i] - @tone_task[:from][i]) * u }
        @tone_task = nil if u >= 1.0
        apply_tone
      end

      def apply_tone
        t = Tone.new(@tone[0].round, @tone[1].round, @tone[2].round, @tone[3].round)
        $game_screen.tone.set(t.red, t.green, t.blue, t.gray) if $game_screen
        @actor_vp.tone.set(t.red, t.green, t.blue, t.gray)
      end

      def update_bars(dt)
        return if !@bar_task
        @bar_task[:t] += dt
        u = [@bar_task[:t] / @bar_task[:dur], 1.0].min
        @bar_h = @bar_task[:from] + (@bar_task[:to] - @bar_task[:from]) * Ease.apply(:out, u)
        @bar_task = nil if u >= 1.0
        sync_bars
      end

      def sync_bars
        h = @bar_h.round
        if h <= 0
          @bar_top.visible = @bar_bot.visible = false
        else
          @bar_top.visible = @bar_bot.visible = true
          @bar_top.x = 0; @bar_top.y = 0; @bar_top.zoom_y = h / 4.0
          @bar_bot.x = 0; @bar_bot.y = Graphics.height - h; @bar_bot.zoom_y = h / 4.0
        end
      end

      def update_flash(dt)
        return if !@flash_task
        @flash_task[:t] += dt
        if @flash_task[:mode] == :fade
          u = @flash_task[:t] / @flash_task[:dur]
          if u >= 1.0
            @flash_sp.opacity = 0
            @flash_task = nil
          else
            @flash_sp.opacity = (@flash_task[:p] * (1.0 - u)).round
          end
        else # :ramp
          steps = @flash_task[:steps]
          ramp_total = steps.length * @flash_task[:step_dur]
          hold_end   = ramp_total + @flash_task[:hold_dur]
          fade_end   = hold_end + @flash_task[:fade_dur]
          t = @flash_task[:t]
          if t < ramp_total
            idx = [(t / @flash_task[:step_dur]).to_i, steps.length - 1].min
            @flash_sp.opacity = steps[idx]
          elsif t < hold_end
            @flash_sp.opacity = steps.last
          elsif t < fade_end
            u = (t - hold_end) / [@flash_task[:fade_dur], 0.001].max
            @flash_sp.opacity = (steps.last * (1.0 - u)).round
          else
            @flash_sp.opacity = 0
            @flash_task = nil
          end
        end
      end

      def update_vignette(dt)
        return if !@vig_pulse
        @vig_pulse[:t] += dt
        wave = 0.5 + 0.5 * Math.sin(@vig_pulse[:t] * Math::PI * 2.0 * @vig_pulse[:hz])
        @vig_sp.opacity = (@vig_pulse[:max] * (0.35 + 0.65 * wave)).round
      end
    end

    #===========================================================================
    # CANON LIVE-MAP IN-ENGINE CUTSCENE SCENES (Rejuvenation V14 Style!)
    #===========================================================================
    class << self
      #-------------------------------------------------------------------------
      # SCENE 1 — Ch5 Peak #1: "The Spire Shatter"
      # Live Map 952 (Plate Vault) -> Live Map 608 (Lowlight Glass Wave) -> Live Map 952!
      #-------------------------------------------------------------------------
      def play_ch5_spire_shatter(capture_dir: nil, capture_fps: 30)
        eng = Engine.new(capture_dir: capture_dir, capture_fps: capture_fps)
        begin
          # 1. Stage directly on REAL built Map 952 (Meridian Spire - Plate Vault)!
          eng.transfer_map(952, 12.0, 9.5, hide_player: true)
          # Hide the static RMXP Mourner event (id 3 on Map 952) so our acting actor owns it
          ev_mourner = $game_map.events.values.find { |e| e.name == "Mourner" }
          ev_mourner.transparent = true if ev_mourner
          ev_cradle  = $game_map.events.values.find { |e| e.name == "Cradle" }

          eng.set_tone(-34, -38, -18, 30, duration: 0.0)
          eng.letterbox(true, height: 32, duration: 0.0)
          eng.play_bgm("girei_intro", volume: 82, tag: "ch5_girei_intro")

          # Live cast positioned on Map 952's real floor conduits!
          eng.spawn_actor(:pc,      sheet: "PLAYER_A", tx: 12, ty: 14, dir: :up, is_charset: true)
          eng.spawn_actor(:rook,    sheet: "ROOK",     tx: 11, ty: 15, dir: :up, is_charset: true)
          eng.spawn_actor(:mourner, sheet: "act_ch5_mourner_reach", tx: 12, ty: 8.35, grid: [4, 4], is_charset: false)
          eng.spawn_actor(:sable,   sheet: "SABLE",    tx: 13.3, ty: 8.0, dir: :left, is_charset: true)

          # Golden Zap Plate Seal Aura pulsing cleanly around the real Cradle tile (12, 7)!
          eng.spawn_vfx(:seal, sheet: "pf_vfx_vault_seal", tx: 12.0, ty: 7.0,
                        grid: [4, 2], frames: 0..3, hold: 0.14, loops: :forever,
                        blend: :add, scale: 0.84, z_layer: :floor, offset: [0, -4])

          # Beat 1: PC & Rook enter down the central conduit while Mourner reaches for the Zap Plate
          eng.actor(:pc).move_to(12, 11.2, duration: 1.35, walk: true, dir: :up)
          eng.actor(:rook).move_to(10.8, 12.2, duration: 1.45, walk: true, dir: :up)
          eng.actor(:mourner).play_clip(
            sheet: "act_ch5_mourner_reach", grid: [4, 4], frames: 0..7,
            ticks: [12, 8, 8, 10, 10, 8, 8, 10], loops: 1, stay: true
          )
          eng.pan_camera_to(12.0, 8.8, duration: 1.5, ease: :in_out)
          eng.wait(1.6)

          eng.say(:MOURNER, :neutral, "Gently. We lift it out gently, and give this city back its dark.", hold: 1.35)
          eng.say(:SABLE, :happy, "Mm-hm. Gently.", hold: 0.95)

          # Sable clamps the brass Splitter onto the Zap Plate cradle & skips back!
          eng.actor(:sable).move_to(12.85, 7.35, duration: 0.28, walk: true, dir: :left)
          eng.wait_for_move(:sable)
          eng.play_se("Battle catch click", volume: 100)
          eng.spawn_vfx(:splitter, sheet: "pf_vfx_splitter_beacon", tx: 12.35, ty: 7.05,
                        grid: [4, 1], frames: [0, 1, 0, 1], ticks: [6, 6, 4, 4],
                        loops: :forever, blend: :normal, untoned: true, z_layer: :above)
          eng.actor(:mourner).show_emote(:exclaim, duration: 0.55)
          eng.play_se("Exclaim", volume: 90)
          eng.actor(:sable).hop(height: 12, duration: 0.24)
          eng.actor(:sable).move_to(15.2, 9.6, duration: 0.65, walk: true, dir: :down)
          eng.wait(0.45)
          eng.say(:SABLE, :happy, "Light for everyone.", hold: 0.9)

          # Beat 2: Coiled Anticipation! Darken vault tone + pbZoomMap push-in + Conduit Overload!
          eng.set_tone(-80, -86, -54, 72, duration: 0.9)
          eng.zoom_map(1.48, duration: 1.25, focus: [12.0, 7.7], ease: :in_out)
          eng.stop_vfx(:seal)
          eng.spawn_vfx(:seal_crack, sheet: "pf_vfx_vault_seal", tx: 12.0, ty: 7.0,
                        grid: [4, 2], frames: 4..7, ticks: [5, 4, 3, 2], loops: :forever,
                        blend: :add, scale: 1.05, z_layer: :above)
          eng.stop_vfx(:splitter)
          eng.spawn_vfx(:splitter_hot, sheet: "pf_vfx_splitter_beacon", tx: 12.35, ty: 7.05,
                        grid: [4, 1], frames: [1, 2, 2, 3], ticks: [4, 3, 2, 2],
                        loops: :forever, blend: :add, untoned: true, z_layer: :above)
          eng.play_se("Anim/Saint7", volume: 92)

          # Staggered prism lightning crackling down Map 952's real conduit rails!
          [[12.0, 7.2], [11.2, 7.6], [12.8, 7.6], [12.0, 9.2]].each_with_index do |(lx, ly), li|
            eng.spawn_vfx(nil, sheet: "pf_vfx_prism_lightning", tx: lx, ty: ly,
                          grid: [4, 2], frames: 0..3, ticks: [2, 2, 2, 2],
                          blend: :add, scale: 0.9, z_layer: :above)
            eng.play_se("Anim/Thunder1", volume: 70) if li == 1
            eng.wait(0.24)
          end

          # LAW 2: DEAD-SILENCE AUDIO VACUUM (0.42s)!
          eng.bgm_cut
          eng.play_se("Battle catch click", volume: 100, pitch: 125)
          eng.wait(0.38)

          # Mourner throws himself barehanded at the Plate (frames 8..15 blistering frameData!)
          eng.actor(:mourner).play_clip(
            sheet: "act_ch5_mourner_reach", grid: [4, 4], frames: 8..15,
            ticks: [5, 3, 2, 2, 2, 3, 4, 5],
            se: { 2 => "Anim/Thunder9" },
            shake: { 4 => [4, 0.25] }
          )
          eng.wait(0.55)

          # Beat 3: THE SHATTER!! Ramped flash + 2f Impact Silhouette + 0.14s HITSTOP + Girei Climax!
          eng.play_se("Anim/Explosion7", volume: 100)
          eng.play_se("Anim/Ice8", volume: 95)
          eng.play_se("Anim/HealBell", volume: 85, pitch: 75)
          eng.impact_beat(hitstop_sec: 0.14)
          eng.play_bgm("girei_climax", volume: 92, tag: "ch5_girei_climax")
          eng.flash_ramp(color: [248, 224, 255], steps: [51, 136, 221, 255], step_dur: 0.03, hold_dur: 0.12, fade_dur: 0.45)
          eng.shake(power: 7, duration: 0.65, decay: true)
          eng.zoom_map(1.04, duration: 0.45, focus: [12.0, 8.2], ease: :out_cubic)

          # Massive expanding Bleed Shockwave Dome Ring + Conduit Lightning Chains + Ballistic Shards!
          eng.stop_vfx(:seal_crack)
          eng.stop_vfx(:splitter_hot)
          eng.spawn_vfx(nil, sheet: "pf_vfx_shockwave_ring", tx: 12.0, ty: 7.5,
                        grid: [4, 2], frames: 0..3, ticks: [3, 3, 4, 4],
                        blend: :add, scale: 1.0, grow: [0.65, 3.6, 0.72], fade: 0.25, z_layer: :above)
          eng.spawn_vfx(nil, sheet: "pf_vfx_shockwave_ring", tx: 12.0, ty: 7.5,
                        grid: [4, 2], frames: 0..3, ticks: [4, 4, 5, 5],
                        blend: :add, scale: 0.8, grow: [0.4, 2.8, 0.85], fade: 0.30, z_layer: :above)

          # 14 crisp pixel crystal shards exploding radially from the Zap Plate!
          14.times do |si|
            ang = (si / 14.0) * Math::PI * 2.0 + 0.18
            spd = 135 + (si % 3) * 45
            eng.spawn_vfx(nil, sheet: "pf_vfx_glass_shards", tx: 12.0, ty: 7.4,
                          grid: [4, 2], frames: [si % 4, (si + 1) % 4, (si + 2) % 4, (si + 3) % 4],
                          hold: 0.07, loops: 3, blend: :add,
                          drift: [Math.cos(ang) * spd, Math.sin(ang) * spd - 55],
                          gravity: 240, spin: (si.even? ? 240 : -240), fade: 0.22, z_layer: :above)
          end

          # Staggered conduit lightning racing outward down Map 952's rails!
          [[10.0, 9.5], [14.0, 9.5], [12.0, 10.5], [8.0, 10.5], [16.0, 10.5], [12.0, 12.5]].each_with_index do |(lx, ly), i|
            eng.spawn_vfx(nil, sheet: "pf_vfx_prism_lightning", tx: lx, ty: ly,
                          grid: [4, 2], frames: (i.even? ? (4..7) : (0..3)), ticks: [2, 2, 2, 2],
                          blend: :add, scale: 1.05, z_layer: :above)
            eng.wait(0.08)
          end
          eng.wait(0.85)

          # Beat 4: LIVE-MAP CUTAWAY TO REAL MAP 608 (The Lowlight — Shattered)!
          # Showing the Bleed Glass Wave sweeping across Lowlight square & fixing Dex by his soda cart!
          eng.flash(color: [244, 224, 255], power: 255, duration: 0.45)
          eng.transfer_map(608, 24.0, 16.0, hide_player: true)
          eng.set_tone(-44, -50, -24, 58, duration: 0.0)
          eng.play_se("Anim/Ice8", volume: 85, pitch: 85)
          eng.spawn_vfx(nil, sheet: "pf_vfx_shockwave_ring", tx: 24.0, ty: 15.0,
                        grid: [4, 2], frames: 0..3, ticks: [4, 4, 5, 5],
                        blend: :add, scale: 1.1, grow: [0.8, 4.2, 0.95], fade: 0.30, z_layer: :above)
          # Subtle translucent Bleed glass veins on the perimeter cobblestones so frozen Dex & soda cart stay 100% crisp!
          [[21.5, 15.5], [26.5, 15.5], [22.0, 17.5], [26.0, 17.5], [24.0, 18.0]].each_with_index do |(gx, gy), gi|
            eng.spawn_vfx(nil, sheet: "pf_vfx_glass_frost", tx: gx, ty: gy,
                          grid: [4, 2], frames: 0..3, ticks: [3, 3, 3, 4],
                          stay: 3.0, fade: 0.3, blend: :normal, opacity: 135, scale: 0.85, z_layer: :floor)
            eng.wait(0.06) if gi.even?
          end
          eng.zoom_map(1.32, duration: 1.6, focus: [23.6, 15.8], ease: :in_out)
          # Floating silent glass motes drifting over frozen Dex & his soda cart
          8.times do |mi|
            eng.spawn_vfx(nil, sheet: "pf_vfx_smoke_and_motes", tx: 21.5 + mi * 0.7, ty: 17.5 - (mi % 3) * 0.8,
                          grid: [4, 2], frames: [7], hold: 2.2, blend: :add,
                          drift: [6 - (mi % 3) * 4, -22 - (mi % 4) * 5], fade: 0.5, z_layer: :above)
          end
          eng.wait(2.1)

          # Beat 5: Return to Scarred Map 952 — Smoking Glove Aftermath + Overcharged Electivire!
          eng.flash(color: [236, 224, 248], power: 210, duration: 0.45)
          eng.transfer_map(952, 12.0, 9.2, hide_player: true)
          ev_mourner = $game_map.events.values.find { |e| e.name == "Mourner" }
          ev_mourner.transparent = true if ev_mourner
          # Swap real Cradle event to cracked Zap Plate graphic (tile 25947)!
          ev_cradle = $game_map.events.values.find { |e| e.name == "Cradle" }
          if ev_cradle
            ev_cradle.instance_variable_set(:@tile_id, 25947)
          end
          eng.set_tone(-48, -52, -32, 54, duration: 0.0)

          eng.spawn_actor(:pc,      sheet: "PLAYER_A", tx: 12, ty: 11.2, dir: :up, is_charset: true)
          eng.spawn_actor(:rook,    sheet: "ROOK",     tx: 10.8, ty: 12.2, dir: :up, is_charset: true)
          eng.spawn_actor(:mourner, sheet: "act_ch5_mourner_burn", tx: 12, ty: 8.45, grid: [4, 4], is_charset: false)

          # Stuttering weak sparks strictly on the cracked Plate + rising smoke wisps off Mourner's burned hand!
          eng.spawn_vfx(:smoke, sheet: "pf_vfx_smoke_and_motes", tx: 12.45, ty: 8.2,
                        grid: [4, 2], frames: 0..3, ticks: [5, 5, 5, 5], loops: :forever,
                        blend: :normal, untoned: false, drift: [2, -8], z_layer: :above, offset: [0, -14])
          eng.spawn_vfx(:spark_cradle, sheet: "pf_vfx_prism_lightning", tx: 12.0, ty: 6.9,
                        grid: [4, 2], frames: [3, 2, 3], ticks: [12, 3, 16], loops: :forever,
                        blend: :add, scale: 0.48, z_layer: :above, offset: [0, -6])

          eng.actor(:mourner).play_clip(
            sheet: "act_ch5_mourner_burn", grid: [4, 4], frames: 0..11,
            ticks: [12, 10, 10, 10, 10, 10, 10, 10, 8, 8, 10, 12], loops: 1, stay: true
          )
          eng.wait(1.3)
          eng.say(:MOURNER, :sad, "...You. Not here. Get out of here, child. Get OUT—", hold: 1.55)

          # Mourner flees toward the open service door
          eng.stop_vfx(:smoke)
          eng.actor(:mourner).play_clip(
            sheet: "act_ch5_mourner_burn", grid: [4, 4], frames: 12..15,
            ticks: [4, 4, 4, 4], loops: :forever
          )
          eng.actor(:mourner).move_to(17.5, 13.5, duration: 1.2, walk: false)
          eng.wait(1.25)
          eng.remove_actor(:mourner)

          # Overcharged Electivire unfolds from behind the cracked cradle!
          eng.play_se("Anim/Thunder9", volume: 95)
          eng.spawn_actor(:electivire, sheet: "Followers/ELECTIVIRE", tx: 12.0, ty: 6.2,
                          dir: :down, grid: [4, 4], is_charset: true)
          eng.actor(:electivire).hop(height: 20, duration: 0.36)
          eng.actor(:electivire).move_to(12.0, 8.3, duration: 0.36, walk: true, dir: :down)
          eng.spawn_vfx(nil, sheet: "pf_vfx_prism_lightning", tx: 12.0, ty: 8.2,
                        grid: [4, 2], frames: 0..3, ticks: [2, 2, 2, 2],
                        blend: :add, scale: 1.25, z_layer: :above)
          eng.shake(power: 5, duration: 0.40)
          eng.play_cry(:ELECTIVIRE, volume: 100)
          eng.zoom_map(1.32, duration: 0.65, focus: :electivire, ease: :out_cubic)
          eng.wait(0.8)
          eng.say(:ROOK, :panic, "That's the vault guard— it's drunk on the Plate! Get BACK—", hold: 1.3)
          eng.zoom_map(1.0, duration: 0.45, ease: :out)
          eng.letterbox(false, duration: 0.40)
          eng.wait(0.5)
        ensure
          cues = eng.cues.dup
          fc   = eng.frames_captured
          eng.dispose
        end
        return { :cues => cues, :frames => fc }
      end

      #-------------------------------------------------------------------------
      # SCENE 2 — Ch9 Peak #2: "Trevenant's Ingrain & The Unmasking"
      # Live Map 295 (lit as subterranean Crimson Emergency Reliquary Ring;
      # Wednesday swaps map_id: 295 -> 264 when Iron Pit Reliquary is generated!)
      #-------------------------------------------------------------------------
      def play_ch9_trevenant_unmasking(capture_dir: nil, capture_fps: 30)
        eng = Engine.new(capture_dir: capture_dir, capture_fps: capture_fps)
        begin
          # Stage on live built stone hall Map 295 with crimson emergency lighting!
          eng.transfer_map(295, 15.0, 12.2, hide_player: true)
          eng.set_tone(-28, -86, -78, 42, duration: 0.0)
          eng.set_emergency_vignette([216, 28, 38], max_alpha: 74, pulse_hz: 1.0)
          eng.letterbox(true, height: 32, duration: 0.0)
          eng.play_bgm("ch9_tension", volume: 80, tag: "ch9_tension")

          # Clean vertical aisle spacing so EVERY character, root wall, and fallen mask is 100% unobstructed:
          #   Reliquary Plinth (15.0, 10.4)
          #   Mourner starts (15.0, 11.7) -> dives to (15.0, 14.8)
          #   PC stands clear left-center (13.3, 13.8)
          #   Trevenant materializes at (15.0, 16.5)
          #   Ingrain Root Wall erupts at y = 17.85
          #   Juno (15.0, 19.3) & Nell (14.2, 19.5) shielded right behind the root wall!
          eng.spawn_vfx(:reliquary, sheet: "pf_vfx_fist_reliquary", tx: 15.0, ty: 10.4,
                        grid: [4, 2], frames: [0, 1], ticks: [10, 10], loops: :forever,
                        blend: :normal, untoned: false, z_layer: :mid, origin: :foot)
          eng.spawn_actor(:mourner, sheet: "act_ch9_mourner_throw", tx: 15.0, ty: 11.7,
                          grid: [4, 4], is_charset: false)
          eng.spawn_actor(:pc,   sheet: "PLAYER_A", tx: 13.3, ty: 13.8, dir: :up, is_charset: true)
          eng.spawn_actor(:juno, sheet: "JUNO",     tx: 15.0, ty: 19.3, dir: :up, is_charset: true)
          eng.spawn_actor(:nell, sheet: "NPC 02",   tx: 14.2, ty: 19.5, dir: :up, is_charset: true)

          # Beat 1: Mourner frantically pulling Splitter wires -> last Splitter CLICKS!
          eng.actor(:mourner).play_clip(
            sheet: "act_ch9_mourner_throw", grid: [4, 4], frames: [0, 1, 0, 1],
            ticks: [7, 7, 6, 6], loops: 1, stay: true
          )
          eng.zoom_map(1.42, duration: 1.0, focus: [15.0, 10.7], ease: :in_out)
          eng.wait(1.15)

          # LAW 2: DEAD-SILENCE VACUUM + tiny dry CLICK on the last Splitter!
          eng.bgm_cut
          eng.stop_vfx(:reliquary)
          eng.spawn_vfx(:reliquary_arm, sheet: "pf_vfx_fist_reliquary", tx: 15.0, ty: 10.4,
                        grid: [4, 2], frames: [2], hold: 0.65, stay: :forever,
                        blend: :normal, untoned: true, z_layer: :mid, origin: :foot)
          eng.play_se("Battle catch click", volume: 100, pitch: 130)
          eng.actor(:mourner).show_emote(:exclaim, duration: 0.5)
          eng.wait(0.45)

          # Beat 2: Partial Fist Plate Shatter! One resonant bell note + Crimson-to-Grey Wave!
          eng.stop_vfx(:reliquary_arm)
          eng.spawn_vfx(:reliquary_crack, sheet: "pf_vfx_fist_reliquary", tx: 15.0, ty: 10.4,
                        grid: [4, 2], frames: [3, 4, 5, 6, 7], ticks: [4, 6, 6, 6, 6],
                        loops: :forever, blend: :normal, untoned: false, z_layer: :mid, origin: :foot)
          eng.play_se("Anim/HealBell", volume: 95, pitch: 72)
          eng.play_se("Anim/Ice8", volume: 95)
          eng.flash_ramp(color: [255, 196, 208], steps: [51, 136, 221, 255], step_dur: 0.03, hold_dur: 0.10, fade_dur: 0.35)
          eng.shake(power: 5, duration: 0.45)
          eng.spawn_vfx(nil, sheet: "pf_vfx_shockwave_ring", tx: 15.0, ty: 10.6,
                        grid: [4, 2], frames: 4..7, ticks: [3, 3, 4, 4],
                        blend: :add, scale: 1.0, grow: [0.6, 3.2, 0.7], fade: 0.25, z_layer: :above)
          eng.zoom_map(1.0, duration: 0.45, ease: :out)
          eng.wait(0.45)

          # Beat 3: Translucent Crimson Glass Frost races DOWN the stone floor UNDERNEATH actors!
          eng.pan_camera_to(15.0, 16.5, duration: 1.1, ease: :in_out)
          eng.actor(:mourner).play_clip(
            sheet: "act_ch9_mourner_throw", grid: [4, 4], frames: [2, 3], ticks: [4, 6]
          )
          # Crisp translucent floor glass veins (blend: :normal, opacity: 140, z_layer: :floor = z 5 UNDER all characters!)
          [12.0, 13.1, 14.2, 15.3, 16.4].each_with_index do |gy, gi|
            [-1.1, 0.0, 1.1].each do |gx|
              eng.spawn_vfx(nil, sheet: "pf_vfx_glass_frost", tx: 15.0 + gx, ty: gy,
                            grid: [4, 2], frames: 4..7, ticks: [2, 2, 3, 3],
                            stay: :forever, blend: :normal, opacity: 145, scale: 0.88, z_layer: :floor)
            end
            eng.play_se("Anim/Ice2", volume: 70, pitch: 95 + gi * 6) if gi.even?
            eng.wait(0.16)
          end

          eng.actor(:juno).show_emote(:shock, duration: 0.6)
          eng.play_se("Exclaim", volume: 95)
          eng.actor(:juno).move_to(14.6, 19.1, duration: 0.22, walk: true, dir: :up)
          eng.say(:JUNO, :shocked, "NELL! Get DOWN—!", hold: 0.85)

          # Beat 4: Mourner's Explosive Dive + Ballistic Dusk Ball Pitch!
          eng.actor(:mourner).play_clip(
            sheet: "act_ch9_mourner_throw", grid: [4, 4], frames: 4..7,
            ticks: [4, 3, 3, 4], se: { 1 => "Fly" }
          )
          eng.actor(:mourner).move_to(15.0, 14.8, duration: 0.55, walk: false, arc_h: 22.0, ease: :out_cubic)
          eng.wait_for_move(:mourner)
          eng.shake(power: 3, duration: 0.20)

          # Mourner pitches the Dusk Ball onto tile (15.0, 16.5) in front of Juno & Nell!
          eng.actor(:mourner).play_clip(
            sheet: "act_ch9_mourner_throw", grid: [4, 4], frames: 8..11,
            ticks: [4, 2, 3, 6],
            se: { 1 => "Battle throw" }
          )
          eng.wait(0.20)
          eng.spawn_vfx(nil, sheet: "pf_vfx_duskball_release", tx: 15.0, ty: 14.8,
                        grid: [4, 2], frames: 0..3, ticks: [2, 2, 2, 2], loops: 2,
                        blend: :normal, untoned: true, move_to: [15.0, 16.5, 0.36],
                        arc_h: 34.0, z_layer: :above)
          eng.wait(0.36)

          # Dusk Ball pops open in eerie purple-emerald flash -> TREVENANT MATERIALIZES!
          eng.play_se("Battle ball drop", volume: 90)
          eng.play_se("Anim/Darkness6", volume: 85, pitch: 115)
          eng.spawn_vfx(nil, sheet: "pf_vfx_duskball_release", tx: 15.0, ty: 16.5,
                        grid: [4, 2], frames: 4..7, ticks: [2, 3, 3, 3],
                        blend: :add, scale: 1.35, z_layer: :above)
          eng.spawn_actor(:trevenant, sheet: "act_ch9_trevenant_ingrain", tx: 15.0, ty: 16.5,
                          grid: [4, 4], is_charset: false, z_bias: 6)
          eng.play_cry(:TREVENANT, volume: 100)

          # Beat 5: TREVENANT INGRAIN SLAM!! Variable frameData anticipation -> smear -> FLOOR SLAM -> 5-TILE ROOT WALL!
          eng.actor(:trevenant).play_clip(
            sheet: "act_ch9_trevenant_ingrain", grid: [4, 4], frames: 0..9,
            ticks: [4, 4, 5, 6, 8, 2, 5, 5, 5, 6],
            se: { 6 => "Anim/Earth4", 7 => "Anim/LeechSeedPlanted" },
            shake: { 6 => [6, 0.45] },
            flash: { 6 => [[168, 255, 176], 120, 0.20] },
            on_frame: {
              6 => proc do |e, _a, _fi|
                # 5-tile gnarled emerald Ingrain Root Wall erupts cleanly at y = 17.85 right in front of Juno & Nell!
                [15.0, 14.0, 16.0, 13.0, 17.0].each_with_index do |rx, ri|
                  e.spawn_vfx(:"root_#{ri}", sheet: "pf_vfx_ingrain_roots", tx: rx, ty: 17.85,
                              grid: [4, 2], frames: [0, 1, 2, 3, 4],
                              ticks: [2 + ri, 3, 3, 4, 8], stay: :forever,
                              blend: :normal, untoned: false, scale: 0.62, z_layer: :mid, origin: :foot)
                end
              end
            }
          )
          eng.wait_for_clip(:trevenant)

          # Beat 6: Crimson Crystal Shard Volley slams into the Ingrain Root Wall & climbs the bark!
          eng.actor(:trevenant).play_clip(
            sheet: "act_ch9_trevenant_ingrain", grid: [4, 4], frames: [10, 11, 12],
            ticks: [6, 6, 12], stay: true
          )
          eng.actor(:mourner).play_clip(
            sheet: "act_ch9_mourner_throw", grid: [4, 4], frames: 12..15,
            ticks: [5, 5, 4, 4], stay: true
          )

          # 6 rapid crimson crystal spear projectiles rocketing down from Reliquary -> Root Wall!
          [13.2, 16.8, 14.1, 15.9, 15.0, 14.6].each_with_index do |sx, si|
            eng.spawn_vfx(nil, sheet: "pf_vfx_glass_shards", tx: sx, ty: 11.4,
                          grid: [4, 2], frames: [4, 5, 6], ticks: [2, 2, 2], loops: 3,
                          blend: :add, scale: 1.15, move_to: [sx, 17.3, 0.28], z_layer: :above)
            eng.play_se("Anim/Ice2", volume: 78, pitch: 110 + si * 5) if si.even?
            eng.wait(0.11)
          end
          eng.wait(0.24)

          # Swap root wall cells into frames 5..7 (crimson crystals crashing onto bark and STOPPING!)
          5.times { |ri| eng.stop_vfx(:"root_#{ri}") }
          [15.0, 14.0, 16.0, 13.0, 17.0].each_with_index do |rx, ri|
            eng.spawn_vfx(:"root_glaze_#{ri}", sheet: "pf_vfx_ingrain_roots", tx: rx, ty: 17.85,
                          grid: [4, 2], frames: [5, 6, 7], ticks: [4, 5, 10], stay: :forever,
                          blend: :normal, untoned: false, scale: 0.62, z_layer: :mid, origin: :foot)
            eng.spawn_vfx(nil, sheet: "pf_vfx_glass_shards", tx: rx, ty: 17.3,
                          grid: [4, 2], frames: [7], hold: 0.14, blend: :add, scale: 1.1, z_layer: :above)
          end
          eng.shake(power: 5, duration: 0.35)
          eng.play_se("Anim/Ice8", volume: 88)
          eng.wait(0.32)

          # Beat 7: THE STRAY SHARD -> MASK SPLITS -> DEAD SILENCE -> UNCLE ROWAN REVEAL!!
          # Stray crimson-violet shard rips straight into Mourner at (15.0, 14.8)!
          eng.spawn_vfx(nil, sheet: "pf_vfx_glass_shards", tx: 15.2, ty: 11.8,
                        grid: [4, 2], frames: [4, 5, 6], ticks: [2, 2, 2], loops: 2,
                        blend: :add, scale: 1.25, move_to: [15.0, 14.5, 0.20], z_layer: :above)
          eng.wait(0.20)

          # Push camera in tight on Mourner + 2-frame impact silhouette + 0.16s HITSTOP + dry branch-crack SE!
          eng.zoom_map(1.56, duration: 0.32, focus: :mourner, ease: :out_cubic)
          eng.play_se("Cut", volume: 100, pitch: 82)
          eng.play_se("Anim/Ice2", volume: 95, pitch: 120)
          eng.impact_beat(hitstop_sec: 0.16)
          eng.flash(color: [255, 240, 248], power: 230, duration: 0.24)
          eng.shake(power: 6, duration: 0.35)

          # Grey Bleed ambient light settles across the Reliquary Ring
          eng.clear_vignette
          eng.set_tone(-28, -32, -22, 128, duration: 1.4)

          # Play canonical act_ch9_mourner_unmask.png (4x4 = 16 frames: mask blast -> split -> Rowan collapse!)
          eng.actor(:mourner).play_clip(
            sheet: "act_ch9_mourner_unmask", grid: [4, 4], frames: 0..15,
            ticks: [4, 4, 5, 6, 7, 6, 8, 16, 12, 14, 14, 14, 16, 16, 18, 30],
            on_frame: {
              5 => proc do |e, _a, _fi|
                # Two crisp pixel ash-bark mask halves & white lily fly outward and land on the glass!
                e.spawn_vfx(nil, sheet: "pf_vfx_smoke_and_motes", tx: 14.9, ty: 14.6,
                            grid: [4, 2], frames: [4], hold: 0.55, blend: :normal, untoned: false,
                            drift: [-44, -40], gravity: 210, spin: -260, z_layer: :above)
                e.spawn_vfx(nil, sheet: "pf_vfx_smoke_and_motes", tx: 15.1, ty: 14.6,
                            grid: [4, 2], frames: [5], hold: 0.55, blend: :normal, untoned: false,
                            drift: [48, -44], gravity: 210, spin: 280, z_layer: :above)
              end,
              7 => proc do |e, _a, _fi|
                # Fallen split mask & white lily resting clearly on the glass floor beside Rowan!
                e.spawn_vfx(:mask_floor, sheet: "pf_vfx_smoke_and_motes", tx: 15.0, ty: 15.35,
                            grid: [4, 2], frames: [6], hold: 1.0, stay: :forever,
                            blend: :normal, untoned: false, z_layer: :mid)
              end
            }
          )
          # Trevenant lowers its head slowly toward Rowan
          eng.actor(:trevenant).play_clip(
            sheet: "act_ch9_trevenant_ingrain", grid: [4, 4], frames: [12, 13, 14, 15],
            ticks: [14, 14, 16, 20], stay: true
          )

          # Drift silent Bleed glass motes through the aftermath air
          10.times do |mi|
            eng.spawn_vfx(nil, sheet: "pf_vfx_smoke_and_motes", tx: 12.5 + mi * 0.55, ty: 18.2 - (mi % 3),
                          grid: [4, 2], frames: [7], hold: 4.5, blend: :add,
                          drift: [4 - (mi % 3) * 4, -18 - (mi % 4) * 3], fade: 0.8, z_layer: :above)
          end

          # Hold in breathless silence as Rowan is revealed and drops to his knees (WAIT 40 feel!)
          eng.wait(2.4)

          # Solo violin ("Never Meant to Belong") gently enters AFTER the dead-silence reveal!
          eng.play_bgm("ch9_never_meant", volume: 82, tag: "ch9_never_meant")
          eng.zoom_map(1.20, duration: 1.2, focus: [15.0, 16.4], ease: :in_out)
          eng.wait(0.8)

          eng.say(:JUNO, :shocked, "...Uncle Rowan?", hold: 1.65)
          eng.say(:ROWAN, :sad, "Juno... don't look at me like that. Look at the flowers.", hold: 1.85)

          eng.wait(1.2)
          eng.zoom_map(1.0, duration: 0.7, ease: :out)
          eng.letterbox(false, duration: 0.45)
          eng.wait(0.6)
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

# Rejuvenation V14-compatible global shorthand helpers for RMXP map events!
def pbRejuvCutscene(id, **opts)
  case id.to_sym
  when :CH5_SHATTER, :SH1 then Prismfall::AdvancedAnimations.play_ch5_spire_shatter(**opts)
  when :CH9_UNMASK,  :IR1 then Prismfall::AdvancedAnimations.play_ch9_trevenant_unmasking(**opts)
  else
    PBDebug.log("[AdvancedAnimations] Unknown scene #{id.inspect}") if defined?(PBDebug)
    nil
  end
end

```
