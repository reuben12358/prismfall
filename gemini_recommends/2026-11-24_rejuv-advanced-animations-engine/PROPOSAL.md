# Proposal: Authentic Pokémon Rejuvenation V14 `AdvancedAnimations` In-Engine Cutscene Engine (6/6 Complete Story Peak Suite — Zero AI `.ogv` Slideshows)

- **Date:** 2026-11-24
- **Author:** Gemini (Task 1 Specialist — Rejuvenation V14 `AdvancedAnimations` Architect & Live `mkxp-z` Prototype Builder)
- **Status:** **PROVEN LIVE IN `mkxp-z.x86_64` — WAVES 1 + 2 + 3 COMPLETE (6/6 FULL STORY PEAK SCENES)** (exit code `0`, `4,435` total native `512×384` @ 30fps live-map frames (including the **43.70s Ch9 Director's Cut v3 — Surgical Polish**) across 6 real built maps `Map 952`, `Map 608`, `Map 295`, `Map 563`, `Map 926`, `Map 285`, with `-14.0 LUFS` calibrated canon audio mixes; zero edits made to repo `.rb`, `pbs/`, `story/`, or `mapgen/`).
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
| **1. Live Tilemap & Floor Decals** | `Spriteset_Map` (`z=0..300`) + `@actor_vp` floor band (`z=5`) | Real playable maps (`Map 952`, `Map 608`, `Map 295`, `Map 563`, `Map 926`, `Map 285`) darkened/sepia-tinted with `$game_screen.tone` so VFX glow by contrast | `Engine#transfer_map` & `Engine#set_tone` (midnight, crimson emergency, sepia AF 290 `Tone(28,12,-26,95)`, Bleed-violet summit, golden sunrise). Floor frost, Lake Rime ice fissures, under-ice Kyogre eye, Trinitite glass crust, and Glassfall sheen (`z_layer: :floor`) route into `@actor_vp` at `z=5` cleanly **underneath** all actors. |
| **2. Variable-`frameData` Overworld Acting** | `@actor_vp` (`z=350`, synced with `$game_screen.tone`) | `Scripts/AdvancedAnimations.rb` arbitrary-grid charsets (`Arc_Renegade_Anim`, `DimensionalAelita_1/_2`, `pkmn_quilava_3` `[30, 8, 4, 8, 4]`) | `MapActor#play_clip(sheet:, grid:, frames:, ticks:)` with `TICK = 0.05s`, inline per-frame callbacks (`se:`, `cry:`, `shake:`, `flash:`, `hitstop:`, `on_frame:`), auto-aligned foot `oy`, native B2W2 `32×48` / `64×64` acting sheets, colossal overworld legendary acting sheets (`act_war1_primal_kyogre`, `act_war1_reshiram`, `act_ch21_arceus_bound`), and `Followers/*.png`. |
| **3. Sparse 4–10 Color Additive Pixel VFX** | `@vfx_vp` (`z=420`, **untoned** `Tone(0,0,0,0)`) | Reborn *Dragonball Z* (`PRAS- Core Enforcer`), Rejuv `anim_beam.png` — thin, sparse additive cells (`blend_type = 1`) instanced along live map paths | `MapVfx` locked to live map tile coordinates `(tx, ty)` with `grow:`, `move_to:` + parabolic `arc_h:`, `drift:` + `gravity:` + `spin:`, directional beam anchors (`origin: :left` / `:right`), and per-frame `set_tile`/`set_scale` for pixel-locked beam tug-of-war clashes and ascending 18-hue Prism Helices! |
| **4. Unified `pbZoomMap` Camera** | `@zoom_vp` (`z=89000`) | `Scripts/Camera/pbZoomMap` — calls `Graphics.snap_to_bitmap` every frame and scales that unified sprite smoothly with `ease_in_out` so autotiles & Z-layers never tear | `Engine#zoom_map(goal, duration:, focus:, ease:)`. Temporarily hides `@zoom_vp` + `@ui_vp`, snaps live `Spriteset_Map + @actor_vp + @vfx_vp` into one crisp bitmap (immediately disposing prior bitmap — zero VRAM leak!), pivots `ox/oy` onto the live focal actor/tile, and layers directional camera shake cleanly. |
| **5. Cinema UI, Ramped Flashes & Portraits** | `@ui_vp` (`z=90000+`) | Reborn ramped flashes (`17→51→136→221→255`), `WidescreenEffect_1`, Desolation `FaceWindowVX`, `$Settings.photosensitive` | Smooth widescreen letterbox bars, `flash_ramp`, 2-frame B&W silhouette `impact_beat` + real-clock `hitstop` (auto-degraded when `Cutscene.photosensitive?`), pulsing emergency edge vignette, and auto-sized `PortraitBox` (`name:` support for titles like `"Thane Eirik"`, `"Dominar Hrothgar"`, `"Young Voss"`, `"Echo Morwen"`, `"Arceus (via Ilsa)"`) while the live map keeps animating underneath. |

### The 5 Audio/Timing Rules Enforced Across All 6 Cutscenes
1. **Anticipation Hold:** Variable `ticks:` holds coiled wind-up frames (`8–18` ticks) while `set_tone` darkens the map and `zoom_map` pushes in (`1.0× → 1.48×`).
2. **Audio Vacuum (`bgm_cut`):** Instant 0ms `Audio.bgm_stop` (`0.28–0.45s` dead silence) right before the Spire Splitter detonates, Rowan's mask splits, Kyogre breaches Lake Rime, the WAR-1 clash collapses, the AF 290 Crown cracks, or Lock #18 shatters — broken only by one dry SE (`Battle catch click`, `Cut`, `Anim/Ice8`, or `Anim/HealBell`).
3. **Smear + 2-Frame Silhouette + Real-Clock Hitstop:** 2-tick lunge/slam/launch smear → `impact_beat(hitstop_sec: 0.12..0.16)` freezing `world_dt = 0.0` while shake and shatter SE fire on frame 0.
4. **Ramped Screen Flash + Staggered VFX Chains:** `flash_ramp(steps: [51, 136, 221, 255])` paired with conduit lightning, 5-tile Ingrain roots, radial Origin Pulse spheres, live tug-of-war beams, bottle-green Glassfall curtains, or the 18-hue Prism Helix.
5. **Silent / Scarred Aftermath on the Transformed Map:** Long atmospheric hold on the visibly altered tilemap (cracked Cradle tile `25947`, glass-frosted Lowlight square, fallen ash-bark mask beside Rowan, midnight tropical deluge over fissured Lake Rime, vitrified emerald Trinitite crust across `Map 926`, Echo Morwen turning across 10 years, Valen's empty cracked Crown on the summit flagstones beneath Freed Arceus & the Whole Legend Plate).

---

## 2. Live `mkxp-z.x86_64` Full-Suite Verification Proof (Waves 1 + 2 + 3 = 6/6 Scenes)

All **6 story peak cutscenes** were executed **100% live inside our compiled Linux `mkxp-z.x86_64` engine** on real built Prismfall `.rxdata` maps, captured at native `512×384` @ `30fps` (`4,435` total frames, incl. **Ch9 Director's Cut v3 (Surgical Polish)** `1,311f = 43.70s`), calibrated to **`-14.0 LUFS`**, and visually audited frame-by-frame:

| Scene | Live Maps Used | Frames / Duration | Audio Architecture | Verified Proof Artifacts |
|---|---|---|---|---|
| **Scene 1 — Ch5 Spire Shatter (`:CH5_SHATTER`)** | `Map 952` (*Plate Vault*) → `Map 608` (*Shattered Lowlight* cutaway on frozen Dex) → scarred `Map 952` (Cradle swapped to tile `25947` + Overcharged Electivire leap) | `689` frames @ 30fps (`22.97s`, 15 synced cues) | Mix B *Girei* intro build → `0.38s` dead-silence `bgm_cut` → *Girei* choral drop right on Shatter impact + real `.ogg` SEs & `Cries/ELECTIVIRE.ogg` | `/home/antigravity/pf_engine_run/rejuv_in_engine_proof/pf_rejuv_ch5_spire_shatter.mp4` (`2.4 MB`) & `.gif` (`991 KB`) |
| **Scene 2 — Ch9 Director's Cut v3 (`:CH9_UNMASK`)** | Live `Map 295` Crimson Reliquary (**Wednesday swaps `295 → 264`**) **+ 90° Banquet-Style Side-View Cathedral Cut** (`pf_vfx_ch9_sideview_hall` in `@actor_vp`) | **`1,311` frames @ 30fps (`43.70s`, 56 synced cues)** | **`-14.0 LUFS` (0 missing SEs):** Rejuvenation Tension → dry click vacuum → 3-Wave escalating barrage → razor `bgm_cut` **DEAD SILENCE** across 90° horizontal dive, `1.55×` face impact (`0.25s` hitstop), single-mask shatter, clatter, `"...Wait."` & `"...That voice..."` → *Never Meant to Belong* solo violin swell (zero cartoon `Exclaim` ping!) → `"...Uncle Rowan?"` → 3-box Rowan finale (`"Look at the flowers."` + `2.2s` hold) | `pf_rejuv_ch9_trevenant_unmasking.mp4` (`4.4 MB`), `pf_rejuv_ch9_directors_cut_v3.gif` (`3.9 MB`), **`96d_ch9_directors_cut_v3_proof.png`** (`24f`), **`prismfall_ch9_directors_cut_v3_studio.html`** (`5.78 MiB`) |
| **Scene 3 — Ch11 Kyogre Awakens at Lake Rime (`:CH11_KYOGRE`)** | `Map 563` (*Rimewood Glade* frozen lake & icefall, Tileset 52; **Wednesday swaps `map_id: 563 → 309/300`** when Rimeholt Harbour is built) | `589` frames @ 30fps (`19.63s`, 18 synced cues) | **`-14.0 LUFS`:** Rejuvenation Ominous → `0.35s` dead-silence `bgm_cut` on eye glint & `Anim/Ice8` → *The Rumble of Scientific Triumph* (Kevin Penkin) on Primal Kyogre breach + `Cries/KYOGRE_1.ogg` & water/ice/rain SEs | `/home/antigravity/pf_engine_run/rejuv_in_engine_proof/pf_rejuv_ch11_kyogre_awakens.mp4` (`3.4 MB`) & `.gif` (`2.1 MB`) |
| **Scene 4 — Ch19 WAR-1 Primal Kyogre vs Reshiram Beam Clash (`:WAR_CLIMAX`)** | **Real built `Map 926` (*The Glass Dunes*, Tileset 56)** — full central battlefront basin with Isenmar & Ashkaar armies, banners, Eirik, Hrothgar, Sigrun & Anja | `629` frames @ 30fps (`20.97s`, 24 synced cues) | **`-14.0 LUFS`:** *Elegy of the Dynast* → *Ashes on The Fire* (Kohta Yamamoto) during dual charge & 3.1s tug-of-war clash → `0.28s` dead-silence `bgm_cut` + solitary `Anim/HealBell` → Trinitite glass detonation → *Soundscape to Ardor* + `KYOGRE_1` & `RESHIRAM` cries | `/home/antigravity/pf_engine_run/rejuv_in_engine_proof/pf_rejuv_ch19_war_beam_clash.mp4` (`2.5 MB`) & `.gif` (`1.4 MB`) |
| **Scene 5 — Ch15 CE-1 AF 290 "Through Her Eyes" Glassfall (`:CH15_GLASSFALL`)** | `Map 295` (*Cathedral of the Evergreen* nave & altar dais, Tileset 33; **Wednesday swaps `map_id: 295 → 391`** when Living Nave is built) | `569` frames @ 30fps (`18.97s`, 14 synced cues) | **`-14.0 LUFS`:** Rejuvenation Ominous → `0.28s` dead-silence `bgm_cut` on Crown Bell Crack (`Anim/HealBell` + `Anim/Ice8`) → ***Decretum*** (*Madoka Magica*) across Glassfall shield & 10-year Echo Morwen turn + `Cries/MISMAGIUS.ogg` | `/home/antigravity/pf_engine_run/rejuv_in_engine_proof/pf_rejuv_ch15_ce1_glassfall.mp4` (`2.0 MB`) & `.gif` (`1.25 MB`) |
| **Scene 6 — Ch21 "The Ring & The Light" Arceus Finale (`:CH21_ARCEUS`)** | `Map 285` (*Briar Hall - Upper Court* white-stone summit terrace, Tileset 33; **Wednesday swaps `map_id: 285 → 491`** when Crownhaven Prism Arena is built) | `648` frames @ 30fps (`21.60s`, 13 synced cues) | **`-14.0 LUFS`:** *DARK ARIA <LV2>* (Bound Arceus & 18-hue Prism Helix) → `0.30s` dead-silence `bgm_cut` on Lock #18 Break → ***T-KT*** (*Attack on Titan*) across Valen's light ascension, empty Crown & Freed Arceus + `Cries/ARCEUS.ogg` | `/home/antigravity/pf_engine_run/rejuv_in_engine_proof/pf_rejuv_ch21_valen_arceus_finale.mp4` (`2.7 MB`) & `.gif` (`1.37 MB`) |
| **6× 24-Frame Proof Contact Sheets** | Wave 1 (`96`), Ch9 DC v1 (`96b`), Ch9 DC v2 (`96c`), **Ch9 DC v3 (`96d`)**, Wave 2 (`97`), Wave 3 (`98`) — nearest-neighbor crisp (`144` curated live frames total) | Visual QA pass | **v3 Surgical Polish:** 100% Row 3 UP-facing back-view Trevenant on ALL 16 top-down frames (zero green/red eyes!) + Row 1 LEFT-facing Trevenant in 90° side-view + restrained emote cadence (`21 → 3` earned beats, −86%) + full v2 physical acting & single-mask shatter | `96_rejuv_in_engine_cutscene_proof.png`, `96b_ch9_directors_cut_proof.png`, `96c_ch9_directors_cut_v2_proof.png`, **`96d_ch9_directors_cut_v3_proof.png`**, `97_rejuv_wave2_cutscene_proof.png`, `98_rejuv_wave3_cutscene_proof.png` (all copied to parent `previews/`) |
| **5× Interactive Showcase HTMLs** | **Ch9 Director's Cut v3 Studio (`5.78 MiB`)**, Ch9 DC v2 (`5.79 MiB`), Wave 1 (`5.53 MB`), Wave 2 (`4.60 MB`), Wave 3 (`4.32 MB`) — all strictly `< 8 MB` | Playwright verified | `console_errors=0`, `page_errors=0`, `0` JS syntax errors, all embedded live MP4s `512×384` `readyState=4`, `20/20` assets loaded | **`prismfall_ch9_directors_cut_v3_studio.html`**, `prismfall_ch9_directors_cut_v2_studio.html`, `prismfall_rejuv_in_engine_cutscenes_preview.html`, `..._wave2_preview.html`, `..._wave3_preview.html` |

---

## 3. Verified Pixel-Art Asset Manifest (33 New Crisp 2× Sheets — All 3-Way SHA-256 Synced)

Every new pixel-art sheet was authored on a native 1× pixel grid, upscaled strictly 2× `NEAREST`, and passed automated validation: **`exact2x=True`, `semi=0`, `orphans=0`**, with identical SHA-256 digests across `graphics/`, `art/out/Graphics/`, and live `pf_engine_run/game/Graphics/`.

### A. Wave 1 — 10 Additive & Live-Map VFX Sheets (`graphics/Animations/pf_vfx_*.png`)
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

### B. Wave 2 — 7 Crisp 2× Pixel VFX Sheets (`graphics/Animations/pf_vfx_*.png`)
| File | Dimensions | Grid | Blend / Layer | Colors | SHA-256 (12) | Purpose |
|---|---|---|---|---|---|---|
| `graphics/Animations/pf_vfx_ice_fissure.png` | `512×256` | `4×2` | `:normal` (`:floor`, `z=5`) + `:add` glow | 9 | `5acaa31f4eb6` | Row 0: Tearing black ice fissures across Lake Rime; Row 1: House-sized golden-blue Kyogre eye ringed in crimson Primal runes beneath dark ice |
| `graphics/Animations/pf_vfx_origin_pulse.png` | `512×256` | `4×2` | `:add` (`:above`) | 5 | `f78e0a92400a` | Row 0: Expanding cyan-gold Origin Pulse spheres & radiant bursts; Row 1: Towering ocean breach water geysers & crashing foam crowns |
| `graphics/Animations/pf_vfx_deluge_rain.png` | `512×256` | `4×2` | `:add` (`:above`) | 6 | `a0ba4b231cd3` | Row 0: Wind-driven diagonal torrential tropical deluge rain + splash pips; Row 1: Undulating emerald-cyan-indigo arctic aurora curtains |
| `graphics/Animations/pf_vfx_origin_beam.png` | `512×256` | `4×2` | `:add` (`:above`, `origin: :left`) | 5 | `eb93e00842e8` | Row 0: Tileable horizontal Origin Pulse ocean-energy beam segments (L→R) with golden helix ribbons; Row 1: Elliptical tidal muzzle charge collars |
| `graphics/Animations/pf_vfx_blue_flare_beam.png` | `512×256` | `4×2` | `:add` (`:above`, `origin: :right`) | 5 | `696e8871c154` | Row 0: Tileable horizontal Reshiram Blue Flare plasma beam segments (R→L) with amber flame tongues; Row 1: Jagged plasma flare charge collars |
| `graphics/Animations/pf_vfx_beam_clash_core.png` | `512×256` | `4×2` | `:add` (`:above`) | 6 | `39eec026520a` | Row 0: Split ocean/flame tug-of-war collision sphere with razor white vertical seam; Row 1: Emerald overload → implosion → single silent falling mote |
| `graphics/Animations/pf_vfx_trinitite_glass_wave.png` | `768×384` | `4×2` | `:add` (`:above`) & `:normal` (`:floor`, `z=5`) | 4 | `cb90ffbfa5d5` | Row 0: Expanding radioactive sea-green Trinitite shockwave dome ring; Row 1: Pentagonal vitrified emerald Trinitite fused-glass floor crust |

### C. Wave 3 — 6 New Crisp 2× Pixel VFX Sheets (`graphics/Animations/pf_vfx_*.png`)
| File | Dimensions | Grid | Blend / Layer | Colors | SHA-256 (12) | Purpose |
|---|---|---|---|---|---|---|
| `graphics/Animations/pf_vfx_sky_fracture.png` | `512×256` | `4×2` | `:add` (`:above`) | 6 | `6917ba33b8d8` | Row 0: Great Prism / Crown sky fracture tearing open overhead; Row 1: Colorless Splinter streaking into the five-year-old child's chest |
| `graphics/Animations/pf_vfx_glassfall_curtain.png` | `512×256` | `4×2` | `:add` (`:above`) & `:normal` (`:mid`/`:floor`) | 6 | `a8f4d9bcc511` | Row 0: Sweeping bottle-green Trinitite Glassfall wave curtain rolling across sanctuary pews; Row 1: Vitrified glass spires & floor sheen |
| `graphics/Animations/pf_vfx_sepia_echo_shimmer.png` | `512×256` | `4×2` | `:add` (`:above`) | 6 | `e898f376bba5` | Row 0: Warm AF 290 sepia memory shimmer ribbons & dust; Row 1: Spectral Echo Morwen 10-year turning halo & dissolving memory petals |
| `graphics/Animations/pf_vfx_arceus_18locks.png` | `768×384` | `4×2` | `:add` (`:above` / `:mid`) | 7 | `b00d007dd403` | Row 0: 18 Golden-Chain Locks wheel binding Arceus → Lock #18 blazing & shattering; Row 1: Golden Concordance Ring floor circle & Valen's light pillar |
| `graphics/Animations/pf_vfx_prism_helix_18.png` | `512×256` | `4×2` | `:add` (`:above`) | 10 | `70c6322d7d46` | Row 0: Tileable vertical ascending 18-Hue Prism Helix beam; Row 1: 18-hue impact starburst & 18 harmonious orbiting Plate jewels |
| `graphics/Animations/pf_vfx_legend_plate_burst.png` | `512×256` | `4×2` | `:add` (`:above`) & `:normal` (`:mid`) | 8 | `a89ee85cfb68` | Row 0: Whole Legend Plate clicking together & divine golden-prism sunburst; Row 1: Valen's empty cracked Sovereign Crown falling & resting on flagstones |

### D. Overworld Acting Sheets Used (`graphics/Characters/act_*.png`)
| File | Dimensions | Grid | Wave | Notes |
|---|---|---|---|---|
| `graphics/Characters/act_ch9_trevenant_ingrain.png` | `256×256` | `4×4` | **Wave 1 NEW** (`exact2x=True, semi=0, orphans=0`, 19 colors) | Anchored to `Followers/TREVENANT.png`: Dusk Ball silhouette → rear high → smear slam → Ingrain floor lock → frosted guard |
| `graphics/Characters/act_ch9_mourner_throw.png` | `256×256` | `4×4` | **Wave 1 NEW** (`exact2x=True, semi=0, orphans=0`, 27 colors) | Anchored to canonical `MOURNER.png`: wire-pulling → alarm turn → aisle dive smear → Dusk Ball pitch → wide protective shield |
| `graphics/Characters/act_ch21_arceus_bound.png` | `512×256` | `4×2` | **Wave 3 NEW** (`exact2x=True, semi=0, orphans=0`, SHA `cd15a76c46d7`) | Anchored directly to authentic `Followers/ARCEUS.png`: Row 0 Bound Arceus in golden Gilded Chains straining under Bleed → snapping; Row 1 Freed Radiant Arceus descending with golden halo & Whole Legend Plate heart glow |
| `graphics/Characters/act_ch5_mourner_reach.png` | `256×256` | `4×4` | Wave 1 (existing) | Reaching for Zap Plate (`0..7`) → barehanded lunge into Shatter (`8..15`) |
| `graphics/Characters/act_ch5_mourner_burn.png` | `256×256` | `4×4` | Wave 1 (existing) | Cradling smoking burned glove (`0..11`) → turning & fleeing (`12..15`) |
| `graphics/Characters/act_ch9_mourner_unmask.png` | `128×192` | `4×4` | Wave 1 (existing) | Violet shard hit → ash-bark mask splitting → Uncle Rowan revealed & collapsing |
| `graphics/Characters/act_ch11_kyogre_storm.png` | `128×192` | `4×4` | Wave 2 (existing) | Anja in fur-trimmed parka & windblown cyan scarf: storm approach → spotting eye → shouting `"TOWERS!"` → bracing against deluge |
| `graphics/Characters/act_war1_primal_kyogre.png` | `704×272` | `4×2` | Wave 2 (existing) | Colossal overworld Primal Kyogre (`176×136` cells): vertical lake/sea breach (`0..2`) → Alpha flare (`3`) → Origin Pulse charge & fire (`4..5`) → settle (`6..7`) |
| `graphics/Characters/act_war1_reshiram.png` | `512×256` | `4×2` | Wave 2 (existing) | Colossal overworld Reshiram (`128×128` cells): wing unfurl & golden ignition (`0..3`) → superheated Blue Flare turbine & torrent (`4..5`) → bank away (`6..7`) |


### E. Ch9 Masterclass Director's Cut — 7 New Crisp 2× B2W2/Rejuv Pixel Sheets (3-Way SHA-256 Synced)
Every Director's Cut sheet passed strict **`exact2x=True`, `semi=0`, `orphans=0`** validation and is 3-way SHA-256 synced across `graphics/`, `art/out/Graphics/`, and `pf_engine_run/game/Graphics/`:

| File | Dimensions | Grid | SHA-256 (12) | Purpose |
|---|---|---|---|---|
| `graphics/Characters/act_ch9_trevenant_ingrain_up.png` | `256×256` | `4×4` | `284627a3e282` | **v3 REBUILT:** 100% UP-facing Row 3 `Followers/TREVENANT.png` back view on ALL 16 frames (`17` colors, `exact2x=True, semi=0, orphans=0`): arms & emerald Ingrain beams surge NORTH behind unbroken smooth woody back & mossy crown (ZERO green eyes on Frame 7, ZERO front red eye/mouth on Frame 15!) |
| `graphics/Characters/act_ch9_mourner_throw_up.png` | `256×256` | `4×4` | `804a9ac0bd26` | UP-facing Row 3 `MOURNER.png` acting: wire-pull → aisle dive south → skid & spin-turn NORTH → UPWARD Dusk Ball whip-throw → wide north guard → breach glare |
| `graphics/Characters/act_ch9_mourner_dive_side.png` | `384×192` | `4×2` | `7f4a2e7b4822` | 90° side-profile Mourner acting (`generate_image` B2W2 pixel art anchored to `MOURNER.png` + `act_ch9_mourner_unmask.png`): leap → horizontal protective dive → crimson mask clip → crack → mask shearing off exposing Rowan → unmasked tumble → kneeling Rowan |
| `graphics/Animations/pf_vfx_ingrain_roots_breach.png` | `512×256` | `4×2` | `cb7f9acea0aa` | Top-down 3-wave progressive Ingrain root damage (Wave 1 emerald deflect → Wave 2 crimson cracks → deep fissure → Wave 3 blown-open smoking breach gap) + bark/leaf splinters + L→R horizontal crimson spear + 8-point anime starburst |
| `graphics/Animations/pf_vfx_ingrain_wall_side.png` | `512×192` | `4×1` | `213493681abd` | 90° side-profile tall vertical braided emerald Ingrain root barrier cracking & blowing open into a jagged chest-height breach gap |
| `graphics/Animations/pf_vfx_ch9_sideview_hall.png` | `512×384` | `1×1` | `ab6badcecf90` | Rejuvenation V14 Banquet-style 90° side-view `Map 295` crimson emergency gothic cathedral corridor backdrop (rendered in `@actor_vp` at `z=1` so tone, shake, and `pbZoomMap` apply seamlessly) |
| `graphics/Animations/pf_vfx_mask_shatter_side.png` | `512×256` | `4×2` | `4cd86e2592a2` | Slow-motion close-up ivory porcelain mask graze → spiderweb fracture → violent cleave → shearing halves + tumbling broken half-masks & drifting white lily flower petals |

---

## 4. Complete Story Peak Cutscene Roster (6/6 Main-Story Peaks LIVE VERIFIED!)

All `.ogv` AI-slideshow movies are permanently retired. **All 6 main-story peak cutscenes** are now live-tested inside `mkxp-z.x86_64` on real tilemaps (plus optional Ruin Route R7 bonus variant queued for post-merge expansion):

| Peak | Chapter & Scene ID | Live Map(s) | Acting Sheets (`graphics/Characters/`) | Additive / Tile VFX (`graphics/Animations/`) | Signature Rejuvenation V14 Beat | Status |
|---|---|---|---|---|---|---|
| **#1** | **Ch5 — Spire Shatter** (`:CH5_SHATTER` / `:SH1`) | `952` → `608` → `952` | `act_ch5_mourner_reach`, `act_ch5_mourner_burn`, `Followers/ELECTIVIRE` | `pf_vfx_vault_seal`, `pf_vfx_splitter_beacon`, `pf_vfx_prism_lightning`, `pf_vfx_shockwave_ring`, `pf_vfx_glass_shards`, `pf_vfx_glass_frost`, `pf_vfx_smoke_and_motes` | Darkened vault `pbZoomMap 1.48×` → `0.38s bgm_cut` → 2f impact + `0.14s` hitstop → live cutaway to Map 608 frozen Dex → Electivire leap | **LIVE VERIFIED (Wave 1)** |
| **#2** | **Ch9 Masterclass Director's Cut v2 (10/10 Polish) — Trevenant Ingrain, 3-Wave Breach & 90° Side-View Unmasking** (`:CH9_UNMASK` / `:IR1`) | `264` *(verified live on `295` + 90° side-view hall)* | `act_ch9_mourner_throw_up`, `act_ch9_trevenant_ingrain_up`, `act_ch9_mourner_dive_side`, `act_ch9_mourner_unmask`, `Followers/TREVENANT`, `JUNO`, `pose_JUNO`, `PLAYER_A`, `pose_PLAYER_A`, `NPC 02` (Nell) | `pf_emote_balloons`, `pf_vfx_fist_reliquary`, `pf_vfx_shockwave_ring`, `pf_vfx_glass_frost`, `pf_vfx_duskball_release`, `pf_vfx_ingrain_roots`, `pf_vfx_ingrain_roots_breach`, `pf_vfx_ingrain_wall_side`, `pf_vfx_ch9_sideview_hall`, `pf_vfx_mask_shatter_side` *(Row 1 face-matched shards/petals only!)*, `pf_vfx_glass_shards`, `pf_vfx_smoke_and_motes` | **v3 Surgical Polish (on top of all 5/5 v2 wins):** 100% Row 3 UP-facing back-view Trevenant on ALL 16 top-down frames (arms & Ingrain energy surging NORTH behind unbroken back; zero green/red eyes) + verified Row 1 LEFT-facing Trevenant in 90° side-view + restrained emote cadence (**21 → 3 earned balloons, −86%**: Mourner click `!`, Juno leap `!!`, Juno quiet `...`; zero balloon clutter across Waves 1–3, 90° mask shatter & solo violin!) (`43.70s`) | **LIVE VERIFIED (Director's Cut v3 — Surgical Polish)** |
| **#3** | **Ch11 — Kyogre Awakens at Lake Rime** (`:CH11_KYOGRE` / `:CH11_THAW`) | `309`/`300` *(verified live on `563`)* | `act_ch11_kyogre_storm`, `act_war1_primal_kyogre` | `pf_vfx_ice_fissure`, `pf_vfx_origin_pulse`, `pf_vfx_deluge_rain` | Arctic aurora midnight → jagged black ice fissures (`z=5`) → house-sized golden-blue Kyogre eye beneath ice → `0.35s bgm_cut` → ocean geyser breach + Origin Pulse spheres → warm midnight deluge | **LIVE VERIFIED (Wave 2)** |
| **#4** | **Ch19 — WAR-1 Primal Kyogre vs Reshiram Beam Clash** (`:WAR_CLIMAX` / `:WAR1`) | **`926` (*The Glass Dunes* — real built map!)** | `act_war1_primal_kyogre`, `act_war1_reshiram`, `EIRIK`, `HROTHGAR`, `SIGRUN`, `ANJA`, `pfw_soldier_*`, `pfw_banner_*` | `pf_vfx_origin_pulse`, `pf_vfx_origin_beam`, `pf_vfx_blue_flare_beam`, `pf_vfx_beam_clash_core`, `pf_vfx_trinitite_glass_wave`, `pf_vfx_smoke_and_motes` | Warm dawn frontline pan (Eirik vs Hrothgar) → darkened two-shot dual charge → pixel-locked Origin Pulse vs Blue Flare tug-of-war → `0.28s bgm_cut` pinpoint collapse → emerald Trinitite glass wave & crust sweeping live `Map 926` | **LIVE VERIFIED (Wave 2)** |
| **#5** | **Ch15 — CE-1 AF 290 "Through Her Eyes" Glassfall** (`:CH15_GLASSFALL` / `:CE1`) | `391` *(verified live on `295`)* | `KESTREL`, `YSOLDE`, `VALEN`, `VOSS`, `MORWEN`, `trainer_ECHO_MORWEN`, `Followers/MISMAGIUS`, AF 290 Choir & child | `pf_vfx_sky_fracture`, `pf_vfx_glassfall_curtain`, `pf_vfx_sepia_echo_shimmer` | Kestrel's Gauntlet → sepia memory `Tone(28,12,-26,95)` AF 290 Choir & young Voss → Great Prism sky fracture + `0.28s bgm_cut` → bottle-green Glassfall curtain as Morwen shields child → Echo Morwen turning across 10 years on *Decretum* | **LIVE VERIFIED (Wave 3)** |
| **#6** | **Ch21 — "The Ring & The Light" Arceus Finale** (`:CH21_ARCEUS` / `:THE_LIGHT`) | `491` *(verified live on `285`)* | `act_ch21_arceus_bound`, `VALEN`, `ILSA`, `VOSS`, `CELESTINE`, `KESTREL`, `PLAYER_A` | `pf_vfx_arceus_18locks`, `pf_vfx_prism_helix_18`, `pf_vfx_legend_plate_burst` | Bound Arceus suspended in 18 golden locks → Valen & Ilsa hold Concordance Ring → 18-hue Prism Helix shatters Lock #18 + `0.30s bgm_cut` → Valen dissolves into light leaving empty cracked Crown on flagstones → Freed Arceus & Whole Legend Plate on *T-KT* | **LIVE VERIFIED (Wave 3)** |
| *(Bonus)* | **Ruin R7 — Mirror Pierce & Silent Crown** (`:RUIN_R7_PIERCE`) | `491` → `963` → `106` | Optional Ruin Route post-merge expansion | Reuses `pf_vfx_glass_shards`, `pf_vfx_smoke_and_motes`, `pf_vfx_sky_fracture` | Trapped micro-control steps toward Reflection → dead-silence `bgm_cut` → 2f ink silhouette lunge + `0.18s` hitstop → silent monochrome aftermath | Optional Post-Merge Bonus |

---

## 5. Wednesday Sprint Merge Checklist for Claude

1. **Install `017_AdvancedAnimations.rb`:** Copy the exact verified code in §6 below into `plugins/Prismfall Cutscenes/017_AdvancedAnimations.rb`.
2. **Retire ALL AI `.ogv` calls in `016_Movies.rb`:**
   - Wire `pbRejuvCutscene` across all 6 story peaks: `:CH5_SHATTER` (`:SH1`), `:CH9_UNMASK` (`:IR1`), `:CH11_KYOGRE`, `:WAR_CLIMAX` (`:WAR1`), `:CH15_GLASSFALL` (`:CE1`), and `:CH21_ARCEUS` (`:THE_LIGHT`).
   - Keep `Cutscene.act` backwards-compatible for tiny inline event gestures, and remove all `Cutscene.movie("pf_*.ogv")` references from story scenes so no AI slideshow ever plays.
3. **Live-Gameplay Input Mode for `PortraitBox#say`:**
   - In `Engine#say`, add an `interactive: !@capture_dir` branch so during real player gameplay, `PortraitBox` waits for `Input.trigger?(Input::USE)` / `Input.trigger?(Input::BACK)` after typing finishes, while keeping `hold:` auto-advance for headless video verification captures!
4. **Canonical BGM Mapping (All 6 Scenes):**
   - Map tags `"ch5_girei_intro"`, `"ch5_girei_climax"`, `"ch9_tension"`, `"ch9_never_meant"`, `"ch11_ominous"`, `"ch11_kyogre_thaw"`, `"ch19_dynast"`, `"ch19_war_clash"`, `"ch19_aftermath"`, `"ch15_ominous"`, `"ch15_decretum"`, `"ch21_arceus_bound"`, `"ch21_tkt"` to Prismfall's canonical `Audio/BGM/` filenames (matching `AUDIO_SOUNDTRACK_PLAN.md` / `2026-11-23_anime-ost-situational-bgm`).
5. **Map Handoffs (Built vs. Pending):**
   - **`Map 952`, `Map 608`, `Map 926`:** Already built and running live! Zero coordinate changes needed.
   - **Map `295 → 264` (Ch9):** Swap `eng.transfer_map(295, ...)` → `264` once Iron Pit Reliquary is generated.
   - **Map `563 → 309/300` (Ch11):** Swap `eng.transfer_map(563, ...)` → `309` (*Sinking Quarter*) / `300` (*Thane's Harbour*) once Rimeholt Harbour is generated.
   - **Map `295 → 391` (Ch15):** Swap `eng.transfer_map(295, ...)` → `391` (*Hollow Cathedral - Living Nave*) once Hollow Cathedral is generated.
   - **Map `285 → 491` (Ch21):** Swap `eng.transfer_map(285, ...)` → `491` (*Crownhaven Prism Arena*) once Prism Arena is generated.
6. **Add `selftest/suite.ruby_stub` coverage:** Verify `AdvancedAnimations::Ease`, variable `ticks:` timing sum, `MapVfx` `:left`/`:right` origins and `set_tile`/`set_scale`, `PortraitBox` custom `name:` width scaling, `photosensitive?` degradation, and zero bitmap disposal leaks.

---

## 6. Verified Live-Tested Source Code: `plugins/Prismfall Cutscenes/017_AdvancedAnimations.rb`

*(Exact verbatim file tested live inside `/home/antigravity/pf_engine_run/game/Plugins/Prismfall Cutscenes/017_AdvancedAnimations.rb` with `mkxp-z.x86_64`, exit code `0`, `4,435` total captured frames across `Map 952`, `Map 608`, `Map 295` + 90° side-view hall, `Map 563`, `Map 926`, and `Map 285` — including the **43.70s Ch9 Director's Cut v3 (Surgical Polish)** (`1,311f`, `56` cues, `-14.0 LUFS`, `0` missing SEs, `3` sparse earned emotes, 100% Row 3 NORTH-facing Trevenant `sha:284627a3e282`) — 3119 lines, SHA-256 `7edb119cd2645390`.)*

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
      attr_accessor :visible, :opacity, :off_x, :off_y, :mirror, :scale

      EMOTE_ROWS = {
        :exclaim => 0, :alert => 0,
        :double_exclaim => 1, :shock => 1, :horror => 1, :panic => 1,
        :question => 2, :confused => 2,
        :dots => 3, :ellipsis => 3, :silent => 3,
        :anger => 4, :angry => 4,
        :sweat => 5, :nervous => 5, :tears => 5,
        :heart => 6, :blush => 6,
        :idea => 7, :sparkle => 7,
        :music => 8, :note => 8,
        :jolt => 9, :dread => 9
      }.freeze

      def initialize(engine, id, sheet:, tx:, ty:, dir: :down, grid: [4, 4],
                     is_charset: true, z_bias: 0, scale: 1.0, folder: "Graphics/Characters/")
        @engine     = engine
        @id         = id
        @tx         = tx.to_f
        @ty         = ty.to_f
        @dir        = dir
        @folder     = folder
        @is_charset = is_charset
        @z_bias     = z_bias
        @scale      = scale.to_f
        @off_x      = 0.0
        @off_y      = 0.0
        @visible    = true
        @opacity    = 255
        @mirror     = false
        @walk_phase = 0.0
        @walking    = false
        @move_task  = nil
        @hop_task   = nil
        @tremble_task = nil
        @crouch_task  = nil
        @clip       = nil
        @emote      = nil
        @color_flash = nil
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
                   elsif name.include?("act_ch9_mourner_dive_side") then 8
                   elsif name.include?("act_ch9_mourner_throw") then 6
                   elsif name.include?("act_ch9_trevenant") then 1
                   elsif name.include?("act_war1_primal_kyogre") then 8
                   elsif name.include?("act_war1_reshiram") then 8
                   elsif name.include?("act_ch21_arceus") then 12
                   elsif name.include?("pfw_banner") then 2
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

      # Instant swap to a 4-pose B2W2 acting strip (pose_JUNO.png, pose_PLAYER_A.png)
      def set_pose(sheet, pose_idx)
        @clip = nil
        @walking = false
        load_sheet(sheet, [4, 1], false)
        set_cell(pose_idx.to_i)
      end

      # Restore standard 4x4 walking charset seamlessly at identical foot baseline
      def restore_charset(sheet, dir: nil)
        @clip = nil
        @dir = dir if dir
        load_sheet(sheet, [4, 4], true)
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

      def tremble(duration: 0.65, amp: 2.0, freq: 44.0)
        @tremble_task = { :t => 0.0, :dur => [duration.to_f, 0.01].max, :amp => amp.to_f, :freq => freq.to_f }
      end

      def crouch_to(target_off_y, duration: 0.25)
        @crouch_task = { :y0 => @off_y.to_f, :y1 => target_off_y.to_f, :t => 0.0, :dur => [duration.to_f, 0.01].max }
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

      def show_emote(kind = :exclaim, duration: 0.65)
        dispose_emote
        sym = kind.to_sym
        sp = Sprite.new(@engine.vfx_vp)
        sp.z = 950
        sheet_path = "Graphics/Animations/pf_emote_balloons.png"
        if File.exist?(sheet_path)
          bmp = @engine.cached_bitmap(sheet_path)
          row = EMOTE_ROWS[sym] || 0
          sp.bitmap = bmp
          sp.src_rect.set(0, row * 32, 32, 32)
          sp.ox = 16
          sp.oy = 32
          @emote = { :sp => sp, :t => 0.0, :dur => duration.to_f, :sheet => true, :row => row, :kind => sym, :owned_bmp => false }
        else
          bmp = Bitmap.new(24, 28)
          bg = Color.new(255, 255, 255)
          ol = Color.new(24, 24, 32)
          ac = (sym == :shock || sym == :double_exclaim) ? Color.new(236, 48, 64) : Color.new(236, 64, 56)
          bmp.fill_rect(2, 2, 20, 18, ol)
          bmp.fill_rect(4, 4, 16, 14, bg)
          bmp.fill_rect(8, 20, 8, 4, ol)
          bmp.fill_rect(10, 18, 4, 4, bg)
          bmp.fill_rect(10, 24, 4, 2, ol)
          bmp.fill_rect(10, 6, 4, 6, ac)
          bmp.fill_rect(10, 14, 4, 2, ac)
          sp.bitmap = bmp
          sp.ox = 12
          sp.oy = 28
          @emote = { :sp => sp, :t => 0.0, :dur => duration.to_f, :sheet => false, :owned_bmp => true }
        end
        sx, sy = screen_pos
        sp.x = sx.round
        sp.y = [(sy - (44.0 * @scale)).round, 66].max
      end

      def dispose_emote
        return if !@emote
        sp = @emote[:sp]
        if sp && !sp.disposed?
          sp.bitmap.dispose if @emote[:owned_bmp] && sp.bitmap && !sp.bitmap.disposed?
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
        tremble_x = 0.0
        if @tremble_task
          raw = Math.sin(@tremble_task[:t] * @tremble_task[:freq]) * @tremble_task[:amp]
          tremble_x = (raw / 2.0).round * 2.0
        end
        return sx + @off_x + tremble_x, sy + @off_y + hop_y + arc_y
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

        if @tremble_task
          @tremble_task[:t] += dt
          @tremble_task = nil if @tremble_task[:t] >= @tremble_task[:dur]
        end

        if @crouch_task
          @crouch_task[:t] += dt
          u = [@crouch_task[:t] / @crouch_task[:dur], 1.0].min
          @off_y = @crouch_task[:y0] + (@crouch_task[:y1] - @crouch_task[:y0]) * Ease.apply(:out, u)
          @crouch_task = nil if u >= 1.0
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

        if @color_flash
          @color_flash[:t] += dt
          if @color_flash[:t] >= @color_flash[:dur]
            @sprite.color.set(0, 0, 0, 0)
            @color_flash = nil
          else
            u = 1.0 - (@color_flash[:t] / @color_flash[:dur])
            c = @color_flash[:col]
            @sprite.color.set(c[0], c[1], c[2], (c[3] * u).round)
          end
        end

        sync_screen_pos

        if @emote
          @emote[:t] += dt
          if @emote[:t] >= @emote[:dur]
            dispose_emote
          else
            if @emote[:sheet]
              t_e = @emote[:t]
              col = if @emote[:kind] == :dots || @emote[:kind] == :ellipsis || @emote[:kind] == :silent
                      step = [@emote[:dur] * 0.22, 0.14].min
                      [(t_e / step).to_i, 3].min
                    else
                      t_e < 0.06 ? 0 : (t_e < 0.14 ? 1 : (t_e < 0.28 ? 2 : 3))
                    end
              @emote[:sp].src_rect.set(col * 32, @emote[:row] * 32, 32, 32)
            end
            sx, sy = screen_pos
            pop = @emote[:t] < 0.08 ? ((1.0 - @emote[:t] / 0.08) * 6.0) : 0.0
            @emote[:sp].x = sx.round
            @emote[:sp].y = [(sy - (44.0 * @scale) + pop).round, 66].max
          end
        end
      end

      def flash_color(r, g, b, a = 180, duration: 0.16)
        @color_flash = { :col => [r, g, b, a], :t => 0.0, :dur => [duration.to_f, 0.01].max }
        @sprite.color.set(r, g, b, a)
      end

      def sync_screen_pos
        sx, sy = screen_pos
        @sprite.x = sx.round
        @sprite.y = sy.round
        @sprite.z = sy.round + @z_bias
        @sprite.visible = @visible
        @sprite.opacity = @opacity.round
        @sprite.mirror  = @mirror
        @sprite.zoom_x  = @scale
        @sprite.zoom_y  = @scale
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
        @scale_x = nil
        @scale_y = nil
        @grow    = grow
        @move_to = move_to   # [tx2, ty2, dur]
        @arc_h   = arc_h.to_f
        @drift   = drift     # [vx_px, vy_px]
        @gravity = gravity.to_f
        @spin    = spin.to_f
        @offset  = offset
        @z_layer = z_layer
        @opacity = opacity.to_f
        @origin_mode = origin
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
        case origin
        when :foot
          @sprite.ox = @cw / 2
          @sprite.oy = @ch - 8
        when :left
          @sprite.ox = 0
          @sprite.oy = @ch / 2
        when :right
          @sprite.ox = @cw
          @sprite.oy = @ch / 2
        else
          @sprite.ox = @cw / 2
          @sprite.oy = @ch / 2
        end
        @sprite.blend_type = { :add => 1, :sub => 2, :normal => 0 }[blend] || 0
        @sprite.mirror = mirror
        update(0.0)
      end

      def stop!; @done = true; end

      def set_tile(tx, ty)
        @tx = tx.to_f
        @ty = ty.to_f
      end

      def set_scale(sx, sy = nil)
        @scale_x = sx.to_f
        @scale_y = (sy || sx).to_f
      end

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
        # tile_to_screen returns foot anchor; center/left/right anchored VFX sit at tile center (sy - 16)
        base_y = (@origin_mode == :foot) ? sy : (sy - 16)
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
        @sprite.zoom_x = @scale_x ? @scale_x : sc
        @sprite.zoom_y = @scale_y ? @scale_y : sc
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
      def initialize(ui_vp, speaker_sym, expression, text, engine, name: nil)
        @engine = engine
        @vp = ui_vp
        @sprites = []
        @text = text.to_s
        @name = (name || speaker_sym.to_s.capitalize).to_s
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

        # 3. Speaker Nameplate Tab (auto-sized for titles like "Dominar Hrothgar" / "Arceus (via Ilsa)")
        @name_sp = Sprite.new(@vp)
        @name_sp.z = 9510
        nw = @name.length > 14 ? 210 : (@name.length > 10 ? 184 : 136)
        nb = Bitmap.new(nw, 28)
        nb.fill_rect(0, 0, nw, 28, Color.new(16, 20, 30, 248))
        nb.fill_rect(2, 2, nw - 4, 24, Color.new(208, 216, 234, 255))
        nb.fill_rect(4, 4, nw - 8, 20, Color.new(34, 40, 58, 255))
        set_font(nb, 18, true)
        nb.font.color = Color.new(255, 236, 176)
        nb.draw_text(8, 2, nw - 16, 24, @name, 0)
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

        # Optional 90-degree side-view cinematic backdrop in @actor_vp (z=1 below all actors!)
        @backdrop_sp = Sprite.new(@actor_vp)
        @backdrop_sp.z = 1
        @backdrop_sp.visible = false

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

      def screen_to_tile(sx, sy)
        tx = (((sx.to_f - 16.0) * 4.0) + $game_map.display_x - 3.0) / SUB.to_f
        ty = (((sy.to_f - 32.0) * 4.0) + $game_map.display_y - 3.0) / SUB.to_f
        return tx, ty
      end

      def set_backdrop(name, z: 1)
        path = name.start_with?("Graphics/") ? name : ("Graphics/Animations/" + name)
        @backdrop_sp.bitmap = cached_bitmap(path)
        @backdrop_sp.x = 0
        @backdrop_sp.y = 0
        @backdrop_sp.z = z
        @backdrop_sp.visible = true
      end

      def clear_backdrop
        @backdrop_sp.visible = false
        @backdrop_sp.bitmap = nil
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
      def say(speaker_sym, expr, text, hold: 1.55, name: nil)
        @dialogue.dispose if @dialogue
        @dialogue = PortraitBox.new(@ui_vp, speaker_sym, expr, text, self, name: name)
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
        @backdrop_sp.dispose if @backdrop_sp && !@backdrop_sp.disposed?
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
            a = @actors[@zoom_focus]
            sx, sy = a.screen_pos
            y_off = @backdrop_sp && @backdrop_sp.visible ? 52.0 : (20.0 * a.scale)
            return sx, sy - y_off
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
      # SCENE 2 — Ch9 Peak #2 (MASTERCLASS DIRECTOR'S CUT v3 — SURGICAL POLISH):
      # "Trevenant's Ingrain, The 3-Wave Breach & 90° Side-View Unmasking"
      # Live Map 295 (lit as Crimson Emergency Reliquary; Wednesday swaps
      # map_id: 295 -> 264) + 90-degree Banquet-style Side-View Cathedral Cut!
      # Target runtime: ~40-44s (~1,200-1,320 frames @ 30fps).
      #-------------------------------------------------------------------------
      def play_ch9_trevenant_unmasking(capture_dir: nil, capture_fps: 30)
        eng = Engine.new(capture_dir: capture_dir, capture_fps: capture_fps)
        begin
          # Helper lambdas for exact pixel staging during the 90-degree side-view cut
          s2t_foot = proc { |sx, sy| eng.screen_to_tile(sx, sy) }
          s2t_ctr  = proc { |sx, sy| eng.screen_to_tile(sx, sy + 16) }

          #=====================================================================
          # ACT I — Reliquary Sabotage, Protagonist Recoil & Sprint,
          #         and Juno's Heroic Leap to Shield Nell!
          #=====================================================================
          eng.transfer_map(295, 15.0, 11.8, hide_player: true)
          eng.set_tone(-28, -86, -78, 42, duration: 0.0)
          eng.set_emergency_vignette([216, 28, 38], max_alpha: 74, pulse_hz: 1.0)
          eng.letterbox(true, height: 32, duration: 0.0)
          eng.play_bgm("ch9_tension", volume: 80, tag: "ch9_tension")

          # Tactical vertical aisle layout (NORTH -> SOUTH, 100% spatial continuity):
          #   Reliquary Plinth (15.0, 10.4) — fires crimson crystal spears SOUTHWARD
          #   5-Tile Ingrain Root Wall (y = 14.65) — erupts NORTH of Trevenant!
          #   Trevenant (15.0, 16.35) — 100% Row 3 UP-facing (NORTH) back view on all 16 frames!
          #   Mourner (15.0, 18.02) — dives in front of Juno & Nell, spins NORTH, throws UPWARD!
          #   Nell starts exposed in center aisle (15.0, 19.55); Juno leaps from (13.5, 19.80)
          #   right in front of Nell (15.0, 19.12) to shield her with her body!
          eng.spawn_vfx(:reliquary, sheet: "pf_vfx_fist_reliquary", tx: 15.0, ty: 10.4,
                        grid: [4, 2], frames: [0, 1], ticks: [10, 10], loops: :forever,
                        blend: :normal, untoned: false, z_layer: :mid, origin: :foot)
          eng.spawn_actor(:mourner, sheet: "act_ch9_mourner_throw_up", tx: 15.0, ty: 11.7,
                          grid: [4, 4], is_charset: false)
          eng.spawn_actor(:pc,   sheet: "PLAYER_A", tx: 13.2, ty: 13.2, dir: :up, is_charset: true)
          eng.spawn_actor(:juno, sheet: "JUNO",     tx: 13.5, ty: 19.80, dir: :up, is_charset: true)
          eng.spawn_actor(:nell, sheet: "NPC 02",   tx: 15.0, ty: 19.55, dir: :up, is_charset: true)

          # Mourner frantically pulling Splitter wires; Protagonist creeps closer watching tensely!
          eng.actor(:mourner).play_clip(
            sheet: "act_ch9_mourner_throw_up", grid: [4, 4], frames: [0, 1, 0, 1],
            ticks: [7, 7, 6, 6], loops: 1, stay: true
          )
          eng.actor(:pc).move_to(13.2, 12.5, duration: 0.90, walk: true, dir: :up)
          eng.zoom_map(1.42, duration: 1.0, focus: [14.7, 10.9], ease: :in_out)
          eng.wait(1.10)

          # Audio Vacuum #1: dry CLICK on the last Splitter -> single crisp (!) on Mourner, PC jolts!
          eng.bgm_cut
          eng.stop_vfx(:reliquary)
          eng.spawn_vfx(:reliquary_arm, sheet: "pf_vfx_fist_reliquary", tx: 15.0, ty: 10.4,
                        grid: [4, 2], frames: [2], hold: 0.65, stay: :forever,
                        blend: :normal, untoned: true, z_layer: :mid, origin: :foot)
          eng.play_se("Battle catch click", volume: 100, pitch: 130)
          eng.actor(:mourner).show_emote(:exclaim, duration: 0.55)
          eng.actor(:pc).hop(height: 8, duration: 0.18)
          eng.wait(0.42)

          # Partial Fist Plate Shatter! Bell chime + crimson shockwave + Protagonist recoils!
          eng.stop_vfx(:reliquary_arm)
          eng.spawn_vfx(:reliquary_crack, sheet: "pf_vfx_fist_reliquary", tx: 15.0, ty: 10.4,
                        grid: [4, 2], frames: [3, 4, 5, 6, 7], ticks: [4, 6, 6, 6, 6],
                        loops: :forever, blend: :normal, untoned: false, z_layer: :mid, origin: :foot)
          eng.play_se("Anim/HealBell", volume: 95, pitch: 72)
          eng.play_se("Anim/Ice8", volume: 95)
          eng.play_bgm("ch9_tension", volume: 86, tag: "ch9_tension")
          eng.flash_ramp(color: [255, 196, 208], steps: [51, 136, 221, 255], step_dur: 0.03, hold_dur: 0.10, fade_dur: 0.35)
          eng.shake(power: 5, duration: 0.45)
          eng.spawn_vfx(nil, sheet: "pf_vfx_shockwave_ring", tx: 15.0, ty: 10.6,
                        grid: [4, 2], frames: 4..7, ticks: [3, 3, 4, 4],
                        blend: :add, scale: 1.0, grow: [0.6, 3.2, 0.7], fade: 0.25, z_layer: :above)
          # Protagonist recoils back a step in pose_PLAYER_A :recoil!
          eng.actor(:pc).set_pose("pose_PLAYER_A", 1)
          eng.actor(:pc).move_to(12.9, 13.4, duration: 0.28, walk: false, ease: :out)
          eng.zoom_map(1.0, duration: 0.42, ease: :out)
          eng.wait(0.42)

          # Crimson glass frost races SOUTH down the central carpet toward exposed Nell!
          eng.pan_camera_to(15.0, 15.9, duration: 1.05, ease: :in_out)
          eng.actor(:mourner).play_clip(
            sheet: "act_ch9_mourner_throw_up", grid: [4, 4], frames: [2, 3], ticks: [4, 6]
          )
          [11.9, 13.0, 14.1, 15.2, 16.3].each_with_index do |gy, gi|
            [-1.1, 0.0, 1.1].each do |gx|
              eng.spawn_vfx(nil, sheet: "pf_vfx_glass_frost", tx: 15.0 + gx, ty: gy,
                            grid: [4, 2], frames: 4..7, ticks: [2, 2, 3, 3],
                            stay: :forever, blend: :normal, opacity: 140, scale: 0.88, z_layer: :floor)
            end
            if gi == 1
              # Protagonist sees Juno & Nell in danger and SPRINTS SOUTH down the aisle!
              eng.actor(:pc).restore_charset("PLAYER_A", dir: :down)
              eng.actor(:pc).move_to(13.1, 17.8, duration: 1.05, walk: true, dir: :down)
            elsif gi == 3
              # Exposed Nell freezes trembling in the center aisle!
              eng.actor(:nell).tremble(duration: 1.35, amp: 2.0, freq: 48.0)
            end
            eng.play_se("Anim/Ice2", volume: 70, pitch: 95 + gi * 6) if gi.even?
            eng.wait(0.15)
          end

          # Multi-Box Sabotage & Shielding Beat:
          # Box 1 (Juno, shocked): "Wait—the glass—"
          eng.say(:JUNO, :shocked, "Wait—the glass—", hold: 0.62)
          eng.actor(:pc).set_dir(:right)
          eng.wait(0.16)

          # Juno spots Nell exposed in the center aisle (single earned !!), sprints & LEAPS right in front of Nell!
          eng.actor(:juno).show_emote(:double_exclaim, duration: 0.75)
          eng.play_se("Exclaim", volume: 95)
          eng.actor(:juno).set_dir(:right)
          eng.wait(0.14)
          eng.actor(:juno).move_to(14.15, 19.55, duration: 0.16, walk: true, dir: :right)
          eng.wait_for_move(:juno)

          # HEROIC JUMP ARC: Juno physically leaps across flagstones directly in front of Nell!
          eng.play_se("Player jump", volume: 92)
          eng.actor(:juno).move_to(15.0, 19.12, duration: 0.34, walk: false, dir: :right, arc_h: 24.0, ease: :out_cubic)
          eng.actor(:nell).move_to(14.85, 19.82, duration: 0.24, walk: true, dir: :up)
          eng.actor(:nell).crouch_to(3, duration: 0.20)
          eng.actor(:nell).tremble(duration: 0.90, amp: 2.0, freq: 46.0)
          # Protagonist slides into left flank guard trying to cover them!
          eng.actor(:pc).move_to(13.2, 18.45, duration: 0.32, walk: true, dir: :down)
          eng.wait_for_move(:juno)

          # Juno lands shielding Nell with her body (pose_JUNO :flinch + protective crouch)!
          eng.play_se("Player bump", volume: 78, pitch: 90)
          eng.shake(power: 2, duration: 0.12)
          eng.actor(:juno).set_pose("pose_JUNO", 1)
          eng.actor(:juno).crouch_to(4, duration: 0.12)
          eng.actor(:pc).set_pose("pose_PLAYER_A", 0)

          # Box 2 (Juno, panic): "NELL!!"
          eng.say(:JUNO, :panic, "NELL!!", hold: 0.48)
          eng.wait(0.14)
          # Box 3 (Juno, panic): "Get DOWN—!!"
          eng.say(:JUNO, :panic, "Get DOWN—!!", hold: 0.62)

          #=====================================================================
          # ACT II — Mourner's Dive South, Spin-Turn NORTH & UPWARD Dusk Ball Throw!
          #=====================================================================
          eng.actor(:mourner).play_clip(
            sheet: "act_ch9_mourner_throw_up", grid: [4, 4], frames: [3, 4, 4, 5],
            ticks: [3, 4, 4, 5], se: { 1 => "Fly" }
          )
          eng.actor(:mourner).move_to(15.0, 18.02, duration: 0.56, walk: false, arc_h: 24.0, ease: :out_cubic)
          eng.actor(:pc).restore_charset("PLAYER_A", dir: :right)
          eng.wait_for_move(:mourner)
          eng.shake(power: 3, duration: 0.18)
          eng.actor(:juno).restore_charset("JUNO", dir: :up)
          eng.actor(:pc).set_dir(:up)
          eng.wait(0.16)

          # Mourner faces UP (NORTH) & whips arm UPWARD launching Dusk Ball NORTHWARD!
          eng.actor(:mourner).play_clip(
            sheet: "act_ch9_mourner_throw_up", grid: [4, 4], frames: [6, 7, 8, 9],
            ticks: [5, 7, 3, 7],
            se: { 2 => "Battle throw" }
          )
          eng.wait(0.60) # Launch ball right on frame 8 upward whip smear!
          eng.spawn_vfx(nil, sheet: "pf_vfx_duskball_release", tx: 15.0, ty: 17.9,
                        grid: [4, 2], frames: 0..3, ticks: [2, 2, 2, 2], loops: 3,
                        blend: :normal, untoned: true, move_to: [15.0, 16.35, 0.42],
                        arc_h: 36.0, z_layer: :above)
          eng.wait(0.42)

          # Dusk Ball pops open at vanguard tile (15.0, 16.35) -> UP-FACING TREVENANT MATERIALIZES!
          eng.play_se("Battle ball drop", volume: 90)
          eng.play_se("Anim/Darkness6", volume: 88, pitch: 115)
          eng.spawn_vfx(nil, sheet: "pf_vfx_duskball_release", tx: 15.0, ty: 16.35,
                        grid: [4, 2], frames: 4..7, ticks: [2, 3, 3, 3],
                        blend: :add, scale: 1.4, z_layer: :above)
          eng.spawn_actor(:trevenant, sheet: "act_ch9_trevenant_ingrain_up", tx: 15.0, ty: 16.35,
                          grid: [4, 4], is_charset: false, z_bias: 8)
          eng.play_cry(:TREVENANT, volume: 100)

          #=====================================================================
          # ACT III — UP-FACING TREVENANT INGRAIN SLAM & 5-TILE NORTH ROOT WALL!
          #=====================================================================
          eng.actor(:trevenant).play_clip(
            sheet: "act_ch9_trevenant_ingrain_up", grid: [4, 4], frames: 0..8,
            ticks: [4, 4, 5, 7, 10, 2, 6, 6, 6],
            se: { 6 => "Anim/Earth4", 7 => "Anim/LeechSeedPlanted" },
            shake: { 6 => [6, 0.45] },
            flash: { 6 => [[168, 255, 176], 125, 0.22] },
            on_frame: {
              6 => proc do |e, _a, _fi|
                # 5-tile gnarled emerald Ingrain Root Wall erupts NORTH of Trevenant (y = 14.65)!
                [15.0, 14.0, 16.0, 13.0, 17.0].each_with_index do |rx, ri|
                  e.spawn_vfx(:"root_#{ri}", sheet: "pf_vfx_ingrain_roots", tx: rx, ty: 14.65,
                              grid: [4, 2], frames: [0, 1, 2, 3, 4],
                              ticks: [2 + ri, 3, 3, 4, 8], stay: :forever,
                              blend: :normal, untoned: false, scale: 0.65, z_layer: :mid, origin: :foot)
                end
                # Protagonist braces in determined guard stance on the shockwave!
                e.actor(:pc).set_pose("pose_PLAYER_A", 0)
              end
            }
          )
          # Mourner spreads both arms wide facing NORTH shielding Juno & Nell behind him!
          eng.actor(:mourner).play_clip(
            sheet: "act_ch9_mourner_throw_up", grid: [4, 4], frames: [10], ticks: [20], stay: true
          )
          eng.wait_for_clip(:trevenant)
          eng.wait(0.24)

          #=====================================================================
          # ACT IV — 3 ESCALATING BARRAGE WAVES (ACTIVE PROTAGONIST + MULTI-BOX!)
          #=====================================================================

          # --- WAVE 1: HOLD! (Two-volley 6 crimson spears -> emerald deflects -> breath) ---
          eng.actor(:trevenant).play_clip(
            sheet: "act_ch9_trevenant_ingrain_up", grid: [4, 4], frames: [8, 9, 8, 9, 8, 9, 8],
            ticks: [7, 6, 7, 6, 7, 6, 14], stay: true
          )
          eng.actor(:mourner).play_clip(
            sheet: "act_ch9_mourner_throw_up", grid: [4, 4], frames: [10, 11, 10, 11],
            ticks: [10, 12, 10, 20], stay: true
          )
          w1_pairs = [
            [13.0, 3], [17.0, 4], [15.0, 0],
            [14.0, 1], [16.0, 2], [15.0, 0]
          ]
          w1_pairs.each_with_index do |(sx, ri), si|
            eng.spawn_vfx(nil, sheet: "pf_vfx_glass_shards", tx: sx, ty: 10.5,
                          grid: [4, 2], frames: [4, 5, 6], ticks: [2, 2, 2], loops: 3,
                          blend: :add, scale: 1.15, move_to: [sx, 14.15, 0.28], z_layer: :above)
            eng.play_se("Anim/Ice2", volume: 78, pitch: 106 + si * 4) if si.even?
            eng.wait(0.22)
            eng.stop_vfx(:"root_#{ri}")
            eng.stop_vfx(:"root_w1_#{ri}")
            eng.spawn_vfx(:"root_w1_#{ri}", sheet: "pf_vfx_ingrain_roots_breach", tx: sx, ty: 14.65,
                          grid: [4, 2], frames: [0], hold: 0.45, stay: :forever,
                          blend: :normal, untoned: false, scale: 0.65, z_layer: :mid, origin: :foot)
            eng.spawn_vfx(nil, sheet: "pf_vfx_glass_shards", tx: sx, ty: 14.05,
                          grid: [4, 2], frames: [7], hold: 0.14, blend: :add, scale: 0.72, z_layer: :above)
            if si == 2 || si == 5
              eng.shake(power: 4, duration: 0.28)
              eng.play_se("Anim/hit", volume: 88, pitch: 112 + si * 2)
              eng.flash(color: [164, 255, 184], power: 82, duration: 0.16)
              eng.actor(:pc).set_pose("pose_PLAYER_A", si == 2 ? 1 : 0)
              eng.actor(:nell).tremble(duration: 0.35, amp: 2.0)
            end
            eng.wait(0.12) if si == 2
          end
          eng.play_se("Anim/Ice8", volume: 76, pitch: 120)
          eng.zoom_map(1.15, duration: 0.80, focus: [15.0, 15.7], ease: :in_out)
          eng.wait(0.88)

          # --- WAVE 2: OVERWHELMING! (Protagonist pushes forward -> forced back -> Multi-Box!) ---
          eng.set_tone(-42, -96, -84, 52, duration: 0.85)
          eng.set_emergency_vignette([232, 24, 38], max_alpha: 92, pulse_hz: 2.0)
          eng.play_se("Anim/Earth1", volume: 84, pitch: 88)
          # Protagonist pushes forward toward the wall trying to help reinforce the line!
          eng.actor(:pc).restore_charset("PLAYER_A", dir: :up)
          eng.actor(:pc).move_to(13.3, 17.15, duration: 0.42, walk: true, dir: :up)
          eng.wait(0.28)

          eng.actor(:trevenant).play_clip(
            sheet: "act_ch9_trevenant_ingrain_up", grid: [4, 4], frames: [10, 11, 10, 11, 10, 11, 10, 11],
            ticks: [6, 6, 6, 6, 6, 6, 6, 10], stay: true
          )
          eng.actor(:mourner).play_clip(
            sheet: "act_ch9_mourner_throw_up", grid: [4, 4], frames: [11, 12, 11, 12, 11, 12],
            ticks: [7, 7, 7, 7, 7, 14], stay: true
          )

          w2_specs_a = [
            [14.8, 13.0], [15.2, 17.0], [14.6, 14.0], [15.4, 16.0],
            [15.0, 15.0], [14.2, 13.4], [15.8, 16.6], [15.0, 15.0]
          ]
          w2_specs_a.each_with_index do |(x0, x1), si|
            eng.spawn_vfx(nil, sheet: "pf_vfx_glass_shards", tx: x0, ty: 10.5,
                          grid: [4, 2], frames: [4, 5, 6], ticks: [2, 2, 2], loops: 3,
                          blend: :add, scale: 1.24, move_to: [x1, 14.15, 0.24], z_layer: :above)
            eng.play_se("Anim/Ice2", volume: 84, pitch: 102 + si * 4) if si.even?
            if si == 3
              # Glowing crimson stress cracks spread across the emerald barrier!
              5.times { |ri| eng.stop_vfx(:"root_w1_#{ri}"); eng.stop_vfx(:"root_#{ri}") }
              [15.0, 14.0, 16.0, 13.0, 17.0].each_with_index do |rx, ri|
                eng.spawn_vfx(:"root_w2_#{ri}", sheet: "pf_vfx_ingrain_roots_breach", tx: rx, ty: 14.65,
                              grid: [4, 2], frames: [1], hold: 0.4, stay: :forever,
                              blend: :normal, untoned: false, scale: 0.65, z_layer: :mid, origin: :foot)
              end
              eng.shake(power: 5, duration: 0.34)
              eng.play_se("Anim/Ice8", volume: 82, pitch: 106)
              eng.actor(:trevenant).flash_color(255, 110, 140, 170, duration: 0.20)
            elsif si == 7
              # Center tiles crack deep crimson + emerald bark splinters force Protagonist back!
              [0, 1, 2].each { |ri| eng.stop_vfx(:"root_w2_#{ri}") }
              [15.0, 14.0, 16.0].each_with_index do |rx, ri|
                eng.spawn_vfx(:"root_w2b_#{ri}", sheet: "pf_vfx_ingrain_roots_breach", tx: rx, ty: 14.65,
                              grid: [4, 2], frames: [2], hold: 0.4, stay: :forever,
                              blend: :normal, untoned: false, scale: 0.65, z_layer: :mid, origin: :foot)
                eng.spawn_vfx(nil, sheet: "pf_vfx_ingrain_roots_breach", tx: rx, ty: 14.8,
                              grid: [4, 2], frames: [4, 5], ticks: [3, 4], blend: :normal, untoned: true,
                              scale: 0.56, drift: [(ri - 1) * 34, 68], gravity: 110, z_layer: :above)
              end
              eng.play_se("Anim/Ice8", volume: 92, pitch: 90)
              eng.play_cry(:TREVENANT, volume: 84)
              eng.shake(power: 6, duration: 0.42)
              eng.actor(:trevenant).flash_color(255, 180, 200, 200, duration: 0.24)
              # Protagonist gets forced back by flying splinters (:recoil + hop)!
              eng.actor(:pc).set_pose("pose_PLAYER_A", 1)
              eng.actor(:pc).hop(height: 8, duration: 0.20)
              eng.actor(:pc).move_to(13.2, 18.05, duration: 0.26, walk: false, ease: :out)
              # Juno ducks tighter shielding Nell (pose_JUNO :flinch + crouch):
              eng.actor(:juno).set_pose("pose_JUNO", 1)
              eng.actor(:juno).crouch_to(5, duration: 0.12)
            end
            eng.wait(0.17)
          end
          eng.wait(0.24)

          # Wave 2 Multi-Box Dialogue Beat:
          # Box 1 (Juno, panic): "The roots—they're splintering!!"
          eng.say(:JUNO, :panic, "The roots—they're splintering!!", hold: 0.75)

          # Wave 2 SLAMS HARDER between boxes!
          [[14.0, 14.0], [16.0, 16.0], [14.8, 14.8], [15.2, 15.2]].each_with_index do |(x0, x1), si|
            eng.spawn_vfx(nil, sheet: "pf_vfx_glass_shards", tx: x0, ty: 10.5,
                          grid: [4, 2], frames: [4, 5, 6], ticks: [2, 2, 2], loops: 3,
                          blend: :add, scale: 1.32, move_to: [x1, 14.15, 0.21], z_layer: :above)
            eng.play_se("Anim/Ice2", volume: 88, pitch: 112 + si * 6) if si.even?
            if si == 2
              eng.play_se("Anim/Ice8", volume: 92, pitch: 86)
              eng.shake(power: 6, duration: 0.36)
              eng.actor(:trevenant).flash_color(255, 196, 210, 210, duration: 0.22)
              eng.actor(:nell).tremble(duration: 0.65, amp: 2.0)
            end
            eng.wait(0.14)
          end
          eng.actor(:juno).restore_charset("JUNO", dir: :up)
          eng.actor(:pc).set_pose("pose_PLAYER_A", 0)
          eng.wait(0.16)

          # Box 2 (Juno, shocked): "Hold on! Please, hold on—"
          eng.say(:JUNO, :shocked, "Hold on! Please, hold on—", hold: 0.75)

          # --- WAVE 3: PENETRATION!! Center root wall BLOWS OPEN -> knocks Protagonist back! ---
          eng.zoom_map(1.28, duration: 0.70, focus: [15.0, 15.9], ease: :in_out)
          eng.actor(:trevenant).play_clip(
            sheet: "act_ch9_trevenant_ingrain_up", grid: [4, 4], frames: [11, 10, 12, 13],
            ticks: [6, 6, 10, 18], stay: true
          )
          w3_xs = [14.0, 16.0, 14.6, 15.4, 15.0, 14.8, 15.2, 15.0]
          w3_xs.each_with_index do |sx, si|
            eng.spawn_vfx(nil, sheet: "pf_vfx_glass_shards", tx: sx, ty: 10.5,
                          grid: [4, 2], frames: [4, 5, 6], ticks: [2, 2, 2], loops: 3,
                          blend: :add, scale: 1.32, move_to: [sx, 14.2, 0.21], z_layer: :above)
            eng.play_se("Anim/Ice2", volume: 88, pitch: 116 + si * 4) if si.even?
            if si == 4
              eng.spawn_vfx(nil, sheet: "pf_vfx_ingrain_roots_breach", tx: 15.0, ty: 14.7,
                            grid: [4, 2], frames: [4, 5], ticks: [3, 4], blend: :normal, untoned: true,
                            scale: 0.62, drift: [10, 75], gravity: 115, z_layer: :above)
              eng.shake(power: 5, duration: 0.25)
            end
            eng.wait(0.13)
          end
          eng.wait(0.12)

          # BLOWN-OPEN JAGGED BREACH GAP IN CENTER ROOT WALL (x = 15.0)!!
          eng.stop_vfx(:root_w2b_0)
          eng.spawn_vfx(:root_breach_center, sheet: "pf_vfx_ingrain_roots_breach", tx: 15.0, ty: 14.65,
                        grid: [4, 2], frames: [3], hold: 1.0, stay: :forever,
                        blend: :normal, untoned: false, scale: 0.65, z_layer: :mid, origin: :foot)
          3.times do |bi|
            eng.spawn_vfx(nil, sheet: "pf_vfx_ingrain_roots_breach", tx: 14.6 + bi * 0.4, ty: 14.8,
                          grid: [4, 2], frames: [4, 5], ticks: [3, 4], blend: :normal, untoned: true,
                          scale: 0.70, drift: [(bi - 1) * 48, 88], gravity: 130, z_layer: :above)
          end
          eng.spawn_vfx(nil, sheet: "pf_vfx_ingrain_roots_breach", tx: 15.0, ty: 14.4,
                        grid: [4, 2], frames: [7], hold: 0.22, blend: :add, scale: 0.95, z_layer: :above)
          eng.play_se("Anim/Explosion2", volume: 96)
          eng.play_se("Anim/Ice8", volume: 98, pitch: 84)
          eng.play_cry(:TREVENANT, volume: 92)
          eng.flash(color: [255, 196, 212], power: 190, duration: 0.22)
          eng.shake(power: 7, duration: 0.48)
          eng.actor(:trevenant).flash_color(255, 220, 232, 220, duration: 0.24)
          # Protagonist knocked back a step by Wave 3's breach shockwave!
          eng.actor(:pc).set_pose("pose_PLAYER_A", 1)
          eng.actor(:pc).move_to(13.3, 19.35, duration: 0.34, walk: false, arc_h: 10.0, ease: :out)
          eng.wait(0.42) # Horror beat letting the smoking breached center gap register!

          # Stray spear + FATAL JAGGED SPEAR punching STRAIGHT THROUGH THE BREACH toward Juno & Nell!
          eng.spawn_vfx(nil, sheet: "pf_vfx_glass_shards", tx: 14.7, ty: 13.8,
                        grid: [4, 2], frames: [4, 5, 6], ticks: [2, 2, 2], loops: 3,
                        blend: :add, scale: 1.25, move_to: [14.2, 18.4, 0.28], z_layer: :above)
          eng.play_se("Anim/Slash9", volume: 86, pitch: 115)
          eng.wait(0.18)
          eng.actor(:mourner).play_clip(
            sheet: "act_ch9_mourner_throw_up", grid: [4, 4], frames: [12, 14, 15],
            ticks: [3, 3, 4], stay: true
          )
          # Protagonist lunges desperately toward Juno & Nell; Juno throws arms over Nell!
          eng.actor(:pc).restore_charset("PLAYER_A", dir: :right)
          eng.actor(:pc).move_to(13.9, 19.35, duration: 0.26, walk: true, dir: :right)
          eng.actor(:juno).set_pose("pose_JUNO", 1)
          eng.spawn_vfx(nil, sheet: "pf_vfx_glass_shards", tx: 15.0, ty: 13.6,
                        grid: [4, 2], frames: [4, 5, 6], ticks: [2, 2, 2], loops: 4,
                        blend: :add, scale: 1.45, move_to: [15.0, 18.6, 0.36], z_layer: :above)
          eng.play_se("Anim/Ice2", volume: 96, pitch: 132)
          eng.wait(0.28)

          #=====================================================================
          # ACT V — 90-DEGREE SIDE-VIEW CATHEDRAL CUT! (100% CAST CONTINUITY!)
          #   - Trevenant (sx=148) facing LEFT (Row 1) toward root wall & spears!
          #   - Nell clearly visible behind shielding Juno on RIGHT!
          #   - Protagonist actively rushing in from FAR RIGHT!
          #   - ZERO emote balloon clutter — pure physical acting & cinema!
          #   - ZERO DOUBLE-MASK: ONLY the single mask on Mourner's own face
          #     shatters at 1.55x pbZoomMap with crisp face-matched shards!
          #=====================================================================
          eng.flash(color: [255, 224, 236], power: 195, duration: 0.12)
          eng.clear_actors
          eng.clear_vfxs
          eng.zoom_map(1.0, duration: 0.0)
          eng.set_tone(0, 0, 0, 0, duration: 0.0)
          eng.set_backdrop("pf_vfx_ch9_sideview_hall", z: 1)

          # LEFT (sx = 78): Vertical side-profile Ingrain Root Wall cracking -> blowing open!
          wx, wy = s2t_foot.call(78, 318)
          eng.spawn_vfx(:side_wall, sheet: "pf_vfx_ingrain_wall_side", tx: wx, ty: wy,
                        grid: [4, 1], frames: [1, 2], ticks: [10, 10], stay: :forever,
                        blend: :normal, untoned: false, scale: 1.15, z_layer: :mid, origin: :foot)

          # LEFT-MID (sx = 148): Side-profile Trevenant (Row 1 LEFT) bracing against the storm!
          ttx, tty = s2t_foot.call(148, 312)
          eng.spawn_actor(:side_trev, sheet: "Followers/TREVENANT", tx: ttx, ty: tty,
                          dir: :left, grid: [4, 4], is_charset: true, scale: 2.0, z_bias: 20)

          # RIGHT-MID (sx = 382): Juno crouched physically shielding right in front of Nell!
          jtx, jty = s2t_foot.call(382, 314)
          eng.spawn_actor(:side_juno, sheet: "JUNO", tx: jtx, ty: jty,
                          dir: :left, grid: [4, 4], is_charset: true, scale: 2.0, z_bias: 26)
          eng.actor(:side_juno).off_y = 6.0

          # RIGHT (sx = 428): Nell clearly visible crouched/trembling right behind Juno!
          ntx, nty = s2t_foot.call(428, 310)
          eng.spawn_actor(:side_nell, sheet: "NPC 02", tx: ntx, ty: nty,
                          dir: :left, grid: [4, 4], is_charset: true, scale: 2.0, z_bias: 18)
          eng.actor(:side_nell).off_y = 6.0
          eng.actor(:side_nell).tremble(duration: 2.2, amp: 2.0, freq: 44.0)

          # FAR RIGHT (sx = 514 -> 474): Protagonist rushing in urgently from right edge!
          ptx0, pty0 = s2t_foot.call(514, 316)
          ptx1, pty1 = s2t_foot.call(474, 316)
          eng.spawn_actor(:side_pc, sheet: "PLAYER_A", tx: ptx0, ty: pty0,
                          dir: :left, grid: [4, 4], is_charset: true, scale: 2.0, z_bias: 28)
          eng.actor(:side_pc).move_to(ptx1, pty1, duration: 0.65, walk: true, dir: :left)

          # Establish full 5-character 90-deg cathedral as 3 horizontal spears hammer left wall!
          [[14, 206, 78, 212, 0.24], [8, 256, 80, 254, 0.24], [10, 238, 86, 240, 0.23]].each_with_index do |(x0, y0, x1, y1, dur), si|
            stx0, sty0 = s2t_ctr.call(x0, y0)
            stx1, sty1 = s2t_ctr.call(x1, y1)
            eng.spawn_vfx(nil, sheet: "pf_vfx_ingrain_roots_breach", tx: stx0, ty: sty0,
                          grid: [4, 2], frames: [6], hold: dur, blend: :add, scale: 1.08,
                          move_to: [stx1, sty1, dur], z_layer: :above)
            eng.play_se("Anim/Ice2", volume: 88, pitch: 114 + si * 8)
            eng.shake(power: 4, duration: 0.18) if si == 1
            eng.wait(0.26)
          end

          # Side-profile vertical root wall BLOWS OPEN into Frame 3 jagged chest-height breach gap!
          eng.stop_vfx(:side_wall)
          eng.spawn_vfx(:side_wall_breach, sheet: "pf_vfx_ingrain_wall_side", tx: wx, ty: wy,
                        grid: [4, 1], frames: [3], hold: 1.0, stay: :forever,
                        blend: :normal, untoned: false, scale: 1.15, z_layer: :mid, origin: :foot)
          sp_x, sp_y = s2t_ctr.call(110, 240)
          eng.spawn_vfx(nil, sheet: "pf_vfx_ingrain_roots_breach", tx: sp_x, ty: sp_y,
                        grid: [4, 2], frames: [4, 5], ticks: [3, 4], blend: :normal, untoned: true,
                        scale: 0.85, drift: [95, -18], gravity: 110, z_layer: :above)
          eng.play_se("Anim/Ice8", volume: 96, pitch: 88)
          eng.shake(power: 6, duration: 0.30)
          eng.actor(:side_trev).flash_color(255, 190, 210, 200, duration: 0.22)
          eng.actor(:side_trev).tremble(duration: 0.28, amp: 2.0, freq: 42.0)
          # Protagonist strains forward helplessly as breach blows open!
          ptx2, pty2 = s2t_foot.call(462, 316)
          eng.actor(:side_pc).move_to(ptx2, pty2, duration: 0.32, walk: true, dir: :left)
          eng.wait(0.28)

          # ====================================================================
          # DEAD SILENCE (bgm_cut!) + FATAL SPEAR + SAKUGA SLOW-MO DIVE!!
          # ====================================================================
          eng.bgm_cut
          eng.play_se("Fly", volume: 90, pitch: 82)

          # Fatal horizontal blazing crimson spear rockets straight out of the breach!
          fsx0, fsy0 = s2t_ctr.call(90, 250)
          fsx1, fsy1 = s2t_ctr.call(264, 250)
          eng.spawn_vfx(:fatal_spear, sheet: "pf_vfx_ingrain_roots_breach", tx: fsx0, ty: fsy0,
                        grid: [4, 2], frames: [6], hold: 0.78, blend: :add, scale: 1.28,
                        move_to: [fsx1, fsy1, 0.74], z_layer: :above)

          # MOURNER LEAPS HORIZONTALLY INTO FRAME shielding BOTH Juno and Nell!
          mtx0, mty0 = s2t_foot.call(352, 312)
          mtx1, mty1 = s2t_foot.call(274, 312)
          eng.spawn_actor(:side_mourner, sheet: "act_ch9_mourner_dive_side", tx: mtx0, ty: mty0,
                          grid: [4, 2], is_charset: false, scale: 1.0, z_bias: 45)
          eng.actor(:side_mourner).play_clip(
            sheet: "act_ch9_mourner_dive_side", grid: [4, 2], frames: [0, 1, 2],
            ticks: [4, 6, 10], stay: true
          )
          eng.actor(:side_mourner).move_to(mtx1, mty1, duration: 0.76, walk: false, arc_h: 38.0, ease: :out_cubic)
          # Smooth 1.55x pbZoomMap centered directly onto Mourner's face for single-mask impact!
          eng.zoom_map(1.55, duration: 0.74, focus: :side_mourner, ease: :out_cubic)
          eng.wait(0.74)

          # 2-FRAME HIGH-CONTRAST B&W SILHOUETTE IMPACT + 0.25s HITSTOP FREEZE RIGHT ON HIS FACE!!
          eng.stop_vfx(:fatal_spear)
          eng.actor(:side_mourner).play_clip(
            sheet: "act_ch9_mourner_dive_side", grid: [4, 2], frames: [3], ticks: [20], stay: true
          )
          ix, iy = s2t_ctr.call(262, 254)
          eng.spawn_vfx(nil, sheet: "pf_vfx_ingrain_roots_breach", tx: ix, ty: iy,
                        grid: [4, 2], frames: [7], hold: 0.24, blend: :add, scale: 1.05, z_layer: :above)
          eng.play_se("Cut", volume: 100, pitch: 78)
          eng.play_se("Anim/Ice8", volume: 96, pitch: 118)
          eng.impact_beat(hitstop_sec: 0.25)
          eng.flash(color: [255, 242, 248], power: 235, duration: 0.22)
          eng.shake(power: 7, duration: 0.34)

          # SINGLE-MASK SLOW-MO SHATTER DIRECTLY OFF MOURNER'S FACE (ZERO DUPLICATE GIANT MASK!)
          eng.clear_vignette
          eng.set_tone(-44, -52, -40, 88, duration: 0.75)

          # Frame 4: Spiderweb crack right across the ONE mask on Mourner's own face!
          eng.actor(:side_mourner).play_clip(
            sheet: "act_ch9_mourner_dive_side", grid: [4, 2], frames: [4], ticks: [20], stay: true
          )
          mtx_c, mty_c = s2t_foot.call(282, 312)
          eng.actor(:side_mourner).move_to(mtx_c, mty_c, duration: 0.65, walk: false, ease: :out)
          eng.wait(0.32)
          eng.play_se("Anim/Ice2", volume: 84, pitch: 140) # Crisp porcelain crack in dead silence!
          gx, gy = s2t_ctr.call(266, 254)
          eng.spawn_vfx(nil, sheet: "pf_vfx_glass_shards", tx: gx, ty: gy,
                        grid: [4, 2], frames: [7], hold: 0.16, blend: :add, scale: 0.45, z_layer: :above)
          eng.wait(0.33)

          # Frame 5: Mask shears directly off Mourner's face exposing Rowan's bare eyes!
          eng.actor(:side_mourner).play_clip(
            sheet: "act_ch9_mourner_dive_side", grid: [4, 2], frames: [5], ticks: [16], stay: true
          )
          mtx_s, mty_s = s2t_foot.call(290, 312)
          eng.actor(:side_mourner).move_to(mtx_s, mty_s, duration: 0.55, walk: false, ease: :out)
          eng.wait(0.55)

          # Frame 6 -> Frame 7: Unmasked Rowan tumbles & drops to one knee!
          # Spawn ONLY crisp face-matched (scale 0.26) porcelain halves & lily petals flying OFF his face!
          eng.actor(:side_mourner).play_clip(
            sheet: "act_ch9_mourner_dive_side", grid: [4, 2], frames: [6, 7],
            ticks: [12, 40], stay: true
          )
          mtx2, mty2 = s2t_foot.call(302, 312)
          eng.actor(:side_mourner).move_to(mtx2, mty2, duration: 0.95, walk: false, ease: :out)

          # Spawn mask halves directly from Frame 5's sheared mask position (left of Rowan's bare face!)
          shx_l, shy_l = s2t_ctr.call(248, 254)
          shx_r, shy_r = s2t_ctr.call(262, 252)
          eng.spawn_vfx(nil, sheet: "pf_vfx_mask_shatter_side", tx: shx_l, ty: shy_l,
                        grid: [4, 2], frames: [4], hold: 1.55, blend: :normal, untoned: true,
                        scale: 0.26, drift: [-58, -18], gravity: 58, spin: -115, fade: 0.28, z_layer: :above)
          eng.spawn_vfx(nil, sheet: "pf_vfx_mask_shatter_side", tx: shx_r, ty: shy_r,
                        grid: [4, 2], frames: [5], hold: 1.55, blend: :normal, untoned: true,
                        scale: 0.26, drift: [26, -38], gravity: 54, spin: 96, fade: 0.28, z_layer: :above)
          [[244, 244, 6, -24, -12], [268, 240, 7, 22, -16], [254, 258, 6, -12, -4]].each_with_index do |(px, py, fr, vx, vy), pi|
            ptx, pty = s2t_ctr.call(px, py)
            eng.spawn_vfx(nil, sheet: "pf_vfx_mask_shatter_side", tx: ptx, ty: pty,
                          grid: [4, 2], frames: [fr], hold: 1.75, blend: :normal, untoned: true,
                          scale: 0.28 + (pi % 2) * 0.04, drift: [vx, vy], gravity: 14,
                          spin: (pi.even? ? 28 : -24), fade: 0.35, z_layer: :above)
          end
          # Smoothly ease zoom back 1.55x -> 1.12x so Trevenant, kneeling Rowan, Juno, Nell & PC all frame cleanly!
          eng.zoom_map(1.12, duration: 1.15, focus: :side_mourner, ease: :out)
          eng.wait(1.45)

          #=====================================================================
          # ACT VI — Cut Back to Top-Down Map 295 & 6-Box Emotional Gut-Punch!
          #=====================================================================
          eng.clear_backdrop
          eng.clear_actors
          eng.clear_vfxs
          eng.set_camera_tile(15.0, 16.5)
          eng.set_tone(-34, -56, -48, 86, duration: 0.0) # Dying crimson fading to cool twilight!
          eng.zoom_map(1.34, duration: 0.0, focus: [15.0, 18.2])

          # Restore live scarred Map 295 aftermath: cracked Reliquary, floor frost, breached root wall!
          eng.spawn_vfx(:reliquary_after, sheet: "pf_vfx_fist_reliquary", tx: 15.0, ty: 10.4,
                        grid: [4, 2], frames: [5, 6, 7], ticks: [10, 10, 10], loops: :forever,
                        blend: :normal, untoned: false, z_layer: :mid, origin: :foot)
          [11.9, 13.0, 14.1, 15.2, 16.3].each do |gy|
            [-1.1, 0.0, 1.1].each do |gx|
              eng.spawn_vfx(nil, sheet: "pf_vfx_glass_frost", tx: 15.0 + gx, ty: gy,
                            grid: [4, 2], frames: [7], hold: 1.0, stay: :forever,
                            blend: :normal, opacity: 120, scale: 0.88, z_layer: :floor)
            end
          end
          [[13.0, 1], [14.0, 2], [15.0, 3], [16.0, 2], [17.0, 1]].each_with_index do |(rx, fr), ri|
            eng.spawn_vfx(:"root_after_#{ri}", sheet: "pf_vfx_ingrain_roots_breach", tx: rx, ty: 14.65,
                          grid: [4, 2], frames: [fr], hold: 1.0, stay: :forever,
                          blend: :normal, untoned: false, scale: 0.65, z_layer: :mid, origin: :foot)
          end

          # Scarred Trevenant remaining rooted facing NORTH toward the breached wall (100% Row 3 back view!)
          eng.spawn_actor(:trevenant, sheet: "act_ch9_trevenant_ingrain_up", tx: 15.0, ty: 16.35,
                          grid: [4, 4], is_charset: false, z_bias: 6)
          eng.actor(:trevenant).play_clip(
            sheet: "act_ch9_trevenant_ingrain_up", grid: [4, 4], frames: [14, 14, 15],
            ticks: [18, 18, 80], stay: true
          )

          # Cast matching top-down/side-view spatial continuity!
          eng.spawn_actor(:pc,   sheet: "PLAYER_A", tx: 13.3, ty: 19.35, dir: :right, is_charset: true)
          eng.spawn_actor(:juno, sheet: "JUNO",     tx: 15.0, ty: 19.35, dir: :up, is_charset: true)
          eng.actor(:juno).off_y = 4.0
          eng.spawn_actor(:nell, sheet: "NPC 02",   tx: 14.65, ty: 19.85, dir: :up, is_charset: true)
          eng.actor(:nell).off_y = 3.0

          # Unmasked Rowan collapsing to his knees with head bowed deep (Frame 13)!
          eng.spawn_actor(:mourner, sheet: "act_ch9_mourner_unmask", tx: 15.0, ty: 18.0,
                          grid: [4, 4], is_charset: false, z_bias: 10)
          eng.actor(:mourner).play_clip(
            sheet: "act_ch9_mourner_unmask", grid: [4, 4], frames: [9, 10, 13],
            ticks: [10, 12, 90], stay: true
          )

          # Broken porcelain mask half tumbles & CLATTERS clearly beside Rowan at (15.75, 18.42)!
          eng.spawn_vfx(nil, sheet: "pf_vfx_mask_shatter_side", tx: 15.10, ty: 17.85,
                        grid: [4, 2], frames: [4], hold: 0.36, blend: :normal, untoned: true,
                        scale: 0.30, move_to: [15.75, 18.42, 0.36], arc_h: 18.0, spin: 180, z_layer: :above)
          eng.set_tone(-26, -30, -14, 112, duration: 2.1)
          eng.wait(0.36)

          # Dry ceramic clink as broken mask hits stone -> unobstructed split mask & white lily!
          eng.play_se("Anim/Ice8", volume: 74, pitch: 134)
          eng.spawn_vfx(:mask_floor, sheet: "pf_vfx_smoke_and_motes", tx: 15.75, ty: 18.42,
                        grid: [4, 2], frames: [6], hold: 1.0, stay: :forever,
                        blend: :normal, untoned: false, z_layer: :mid)

          # Subtle perimeter motes & drifting white lily petals (Rowan & lily 100% unobstructed!)
          6.times do |mi|
            mx = mi < 3 ? (12.2 + mi * 0.7) : (16.4 + (mi - 3) * 0.7)
            eng.spawn_vfx(nil, sheet: "pf_vfx_smoke_and_motes", tx: mx, ty: 19.2 - (mi % 3) * 0.9,
                          grid: [4, 2], frames: [7], hold: 12.0, blend: :add,
                          drift: [3 - (mi % 3) * 3, -10 - (mi % 4) * 2], fade: 1.2, z_layer: :above)
          end
          [[12.6, 16.5, 6], [16.9, 16.8, 7], [17.4, 18.4, 6]].each_with_index do |(px, py, fr), pi|
            eng.spawn_vfx(nil, sheet: "pf_vfx_mask_shatter_side", tx: px, ty: py,
                          grid: [4, 2], frames: [fr], hold: 12.0, blend: :normal, untoned: true,
                          scale: 0.28, drift: [4 - pi * 3, 7], gravity: 1.2,
                          spin: (pi.even? ? 16 : -14), fade: 1.4, z_layer: :above)
          end

          # Protagonist rushes down right beside Juno & Nell; Nell peeks out trembling behind Juno!
          eng.actor(:pc).move_to(13.85, 19.05, duration: 0.58, walk: true, dir: :right)
          eng.wait(0.58)
          eng.actor(:pc).set_dir(:up)
          eng.actor(:nell).crouch_to(0, duration: 0.35)
          eng.actor(:nell).move_to(14.30, 19.70, duration: 0.42, walk: true, dir: :up)
          eng.actor(:nell).tremble(duration: 0.75, amp: 2.0, freq: 38.0)

          # Complete the 1.6s pure dead-silence hold after mask clatter!
          eng.wait(1.02)

          # Juno slowly rises from her crouch with ONE quiet (...) emote balloon!
          eng.actor(:juno).crouch_to(0, duration: 0.42)
          eng.actor(:juno).move_to(15.0, 19.18, duration: 0.42, walk: true, dir: :up)
          eng.actor(:juno).show_emote(:dots, duration: 0.95)
          eng.wait(0.45)

          # === 6-BOX EMOTIONAL GUT-PUNCH REVEAL ===
          # Box 1 (Juno, shocked): "...Wait." (0.8s silent beat!)
          eng.say(:JUNO, :shocked, "...Wait.", hold: 0.85)
          eng.wait(0.80)

          # Box 2 (Juno, crying): "...That voice..."
          eng.say(:JUNO, :crying, "...That voice...", hold: 0.95)

          # Rowan slowly lifts his bare face; Never Meant to Belong solo violin softly enters!
          eng.actor(:mourner).play_clip(
            sheet: "act_ch9_mourner_unmask", grid: [4, 4], frames: [13, 14, 15, 12],
            ticks: [5, 9, 10, 120], stay: true
          )
          eng.play_bgm("ch9_never_meant", volume: 82, tag: "ch9_never_meant")
          eng.wait(0.58)

          # Box 3 (Juno, crying): "...Uncle Rowan?"
          eng.say(:JUNO, :crying, "...Uncle Rowan?", hold: 1.15)

          # 1.1s quiet violin pause — Nell shifts softly, Protagonist steps closer without cartoon balloons!
          eng.actor(:nell).hop(height: 5, duration: 0.18)
          eng.wait(0.32)
          eng.actor(:pc).move_to(14.0, 18.60, duration: 0.48, walk: true, dir: :up)
          eng.wait(0.78)
          eng.actor(:pc).set_dir(:right)

          # Box 4 (Rowan, sad): "Juno..." (0.6s pause)
          eng.say(:ROWAN, :sad, "Juno...", hold: 0.78)
          eng.wait(0.60)

          # Box 5 (Rowan, sad): "Don't look at me like that." (0.7s pause as white petals drift!)
          eng.actor(:mourner).play_clip(
            sheet: "act_ch9_mourner_unmask", grid: [4, 4], frames: [15], ticks: [80], stay: true
          )
          eng.say(:ROWAN, :sad, "Don't look at me like that.", hold: 1.08)

          # Fresh delicate white petals drift across the twilight hall as camera gently opens up!
          eng.zoom_map(1.16, duration: 1.65, focus: [15.0, 18.1], ease: :in_out)
          [[13.4, 16.8, 6], [16.5, 17.2, 7], [15.9, 18.2, 6]].each_with_index do |(px, py, fr), pi|
            eng.spawn_vfx(nil, sheet: "pf_vfx_mask_shatter_side", tx: px, ty: py,
                          grid: [4, 2], frames: [fr], hold: 6.5, blend: :normal, untoned: true,
                          scale: 0.28, drift: [3 - pi * 2, 7], gravity: 1.0,
                          spin: (pi.even? ? 14 : -12), fade: 1.2, z_layer: :above)
          end
          eng.wait(0.70)

          # Box 6 (Rowan, neutral): "Look at the flowers." (long 2.2s quiet hold on the violin!)
          eng.actor(:mourner).play_clip(
            sheet: "act_ch9_mourner_unmask", grid: [4, 4], frames: [12], ticks: [120], stay: true
          )
          eng.say(:ROWAN, :neutral, "Look at the flowers.", hold: 1.45)

          # Long 2.2s quiet hold on the solo violin, white lily, kneeling Rowan, Juno, Nell & Protagonist!
          eng.wait(2.20)
          eng.zoom_map(1.0, duration: 0.75, ease: :out)
          eng.letterbox(false, duration: 0.55)
          eng.wait(0.45)
        ensure
          cues = eng.cues.dup
          fc   = eng.frames_captured
          eng.dispose
        end
        return { :cues => cues, :frames => fc }
      end

      #-------------------------------------------------------------------------
      # SCENE 3 — Ch11 Peak #3: "Kyogre Awakens at Lake Rime"
      # Live Map 563 (Rimewood Glade frozen lake & icefall; Wednesday swaps
      # map_id: 563 -> 309/300 when Rimeholt Sinking Quarter Harbour is built!)
      #-------------------------------------------------------------------------
      def play_ch11_kyogre_awakens(capture_dir: nil, capture_fps: 30)
        eng = Engine.new(capture_dir: capture_dir, capture_fps: capture_fps)
        begin
          # 1. Stage on live built frozen-lake Map 563 under midnight arctic aurora darkness!
          eng.transfer_map(563, 18.0, 13.8, hide_player: true)
          # Hide static map pickup balls / ranger so Lake Rime belongs purely to the scene
          [1, 5, 7].each do |eid|
            ev = $game_map.events[eid]
            ev.transparent = true if ev
          end

          eng.set_tone(-62, -52, -16, 36, duration: 0.0)
          eng.letterbox(true, height: 32, duration: 0.0)
          eng.play_bgm("ch11_ominous", volume: 82, tag: "ch11_ominous")
          eng.play_se("Anim/Wind5", volume: 65)

          # Shimmering emerald-cyan-indigo arctic aurora ribbons rippling above the icefall!
          [[13.6, 9.5, 0], [18.0, 9.2, 1], [22.4, 9.5, 2]].each_with_index do |(ax, ay, ph), ai|
            eng.spawn_vfx(:"aurora_#{ai}", sheet: "pf_vfx_deluge_rain", tx: ax, ty: ay,
                          grid: [4, 2], frames: [4 + (ph % 4), 4 + ((ph + 1) % 4), 4 + ((ph + 2) % 4), 4 + ((ph + 3) % 4)],
                          ticks: [7, 7, 7, 7], loops: :forever,
                          blend: :add, opacity: 195, scale: 1.15, z_layer: :above)
          end

          # Cast positioned on the completely open south snow shore looking north across Lake Rime!
          eng.spawn_actor(:anja, sheet: "act_ch11_kyogre_storm", tx: 15.8, ty: 18.6,
                          grid: [4, 4], is_charset: false)
          eng.spawn_actor(:pc,   sheet: "PLAYER_A", tx: 18.0, ty: 18.9, dir: :up, is_charset: true)
          eng.spawn_actor(:juno, sheet: "JUNO",     tx: 20.2, ty: 18.6, dir: :up, is_charset: true)

          # Beat 1: Cold aurora stillness — trio walks up onto the south bank of frozen Lake Rime
          eng.actor(:anja).play_clip(
            sheet: "act_ch11_kyogre_storm", grid: [4, 4], frames: [0, 1, 2, 3],
            ticks: [10, 10, 8, 10], loops: 1, stay: true
          )
          eng.actor(:anja).move_to(15.8, 17.8, duration: 1.15, walk: false)
          eng.actor(:pc).move_to(18.0, 18.0, duration: 1.25, walk: true, dir: :up)
          eng.actor(:juno).move_to(20.2, 17.8, duration: 1.20, walk: true, dir: :up)
          eng.pan_camera_to(18.0, 14.4, duration: 1.4, ease: :in_out)
          eng.wait(1.6)

          # Beat 2: The ice sings and tears like a page across Lake Rime!
          eng.play_se("Anim/Earth3", volume: 88)
          eng.shake(power: 3, duration: 0.85, decay: false)
          [[14.2, 13.5], [18.0, 13.1], [21.8, 13.5]].each_with_index do |(fx, fy), fi|
            eng.spawn_vfx(:"fissure_#{fi}", sheet: "pf_vfx_ice_fissure", tx: fx, ty: fy,
                          grid: [4, 2], frames: 0..3, ticks: [4, 5, 6, 8],
                          stay: :forever, blend: :normal, untoned: false,
                          scale: 1.12, z_layer: :floor)
            eng.play_se(fi == 1 ? "Anim/Ice5" : "Anim/Ice2", volume: 85, pitch: 90 + fi * 8)
            eng.wait(0.24)
          end

          eng.actor(:anja).play_clip(
            sheet: "act_ch11_kyogre_storm", grid: [4, 4], frames: [4, 5, 6, 7],
            ticks: [6, 6, 6, 8], stay: true
          )
          eng.actor(:juno).show_emote(:exclaim, duration: 0.55)
          eng.actor(:pc).show_emote(:exclaim, duration: 0.55)
          eng.play_se("Exclaim", volume: 90)
          eng.pan_camera_to(18.0, 15.6, duration: 0.45, ease: :out)
          eng.wait(0.45)

          eng.say(:JUNO, :shocked, "The ice isn't cracking— it's tearing open! Something is breathing under the lake!", hold: 1.25)

          # Beat 3: Darken midnight contrast + pbZoomMap push-in -> GIANT GOLDEN EYE OPENS BENEATH THE ICE!
          eng.pan_camera_to(18.0, 13.4, duration: 0.65, ease: :in_out)
          eng.set_tone(-88, -78, -30, 58, duration: 0.9)
          eng.zoom_map(1.42, duration: 1.35, focus: [18.0, 13.0], ease: :in_out)
          eng.play_se("Anim/Water2", volume: 88, pitch: 76)
          eng.play_se("Anim/Saint7", volume: 72, pitch: 78)

          # Floor-layer abyssal pool + eye (z=5 under all actors) + additive luminous iris highlight!
          eng.spawn_vfx(:eye_floor, sheet: "pf_vfx_ice_fissure", tx: 18.0, ty: 13.0,
                        grid: [4, 2], frames: [4, 5, 6], ticks: [10, 10, 20],
                        stay: :forever, blend: :normal, untoned: false,
                        scale: 1.52, z_layer: :floor)
          eng.spawn_vfx(:eye_glow, sheet: "pf_vfx_ice_fissure", tx: 18.0, ty: 13.0,
                        grid: [4, 2], frames: [4, 5, 6], ticks: [10, 10, 20],
                        stay: :forever, blend: :add, opacity: 165,
                        scale: 1.52, z_layer: :mid)
          eng.wait(1.75)

          # Pull back onto Anja's urgent canon storm warning!
          eng.zoom_map(1.0, duration: 0.40, ease: :out)
          eng.pan_camera_to(18.0, 15.6, duration: 0.45, ease: :out)
          eng.actor(:anja).play_clip(
            sheet: "act_ch11_kyogre_storm", grid: [4, 4], frames: [7, 8, 9, 10],
            ticks: [6, 8, 6, 12], stay: true
          )
          eng.wait(0.45)
          eng.say(:ANJA, :panic, "That's not a Pokémon, that's WEATHER! TOWERS! EVERYBODY TO THE TOWERS!", hold: 1.35)

          # Beat 4: LAW 2 DEAD-SILENCE VACUUM (0.35s) -> EYE BLAZING GLINT -> KYOGRE ERUPTS!
          eng.pan_camera_to(18.0, 13.7, duration: 0.35, ease: :in_out)
          eng.stop_vfx(:eye_floor)
          eng.stop_vfx(:eye_glow)
          eng.spawn_vfx(:eye_glint_f, sheet: "pf_vfx_ice_fissure", tx: 18.0, ty: 13.0,
                        grid: [4, 2], frames: [7], hold: 0.5, stay: :forever,
                        blend: :normal, untoned: false, scale: 1.58, z_layer: :floor)
          eng.spawn_vfx(:eye_glint_a, sheet: "pf_vfx_ice_fissure", tx: 18.0, ty: 13.0,
                        grid: [4, 2], frames: [7], hold: 0.5, stay: :forever,
                        blend: :add, opacity: 225, scale: 1.58, z_layer: :above)
          eng.bgm_cut
          eng.play_se("Anim/Ice8", volume: 100, pitch: 90)
          eng.wait(0.35)

          # EXPLOSIVE UPWARD BREACH: 2f silhouette hitstop + Primal Kyogre cry + Kevin Penkin OST drop!
          eng.play_se("Anim/Water5", volume: 100)
          eng.play_se("Anim/Explosion7", volume: 95)
          eng.play_cry(:KYOGRE_1, volume: 100)
          eng.impact_beat(hitstop_sec: 0.14)
          eng.play_bgm("ch11_kyogre_thaw", volume: 90, tag: "ch11_kyogre_thaw")
          eng.flash_ramp(color: [188, 240, 255], steps: [51, 136, 221, 255],
                         step_dur: 0.03, hold_dur: 0.10, fade_dur: 0.42)
          eng.shake(power: 7, duration: 0.65, decay: true)

          # Clear under-ice eye & auroras as the abyssal storm takes the sky!
          eng.stop_vfx(:eye_glint_f)
          eng.stop_vfx(:eye_glint_a)
          3.times { |ai| eng.stop_vfx(:"aurora_#{ai}") }

          # Towering ocean breach water geysers erupting through Lake Rime!
          [[15.4, 14.1, 1.1], [18.0, 14.3, 1.35], [20.6, 14.1, 1.1]].each do |gx, gy, gsc|
            eng.spawn_vfx(nil, sheet: "pf_vfx_origin_pulse", tx: gx, ty: gy,
                          grid: [4, 2], frames: 4..7, ticks: [3, 4, 5, 5],
                          blend: :add, scale: gsc, z_layer: :above, origin: :foot)
          end

          # Spawn PRIMAL KYOGRE breaching vertically out of Lake Rime (frames 0->1->2->3)!
          eng.spawn_actor(:kyogre, sheet: "act_war1_primal_kyogre", tx: 18.0, ty: 15.1,
                          grid: [4, 2], is_charset: false, z_bias: 20)
          eng.actor(:kyogre).play_clip(
            sheet: "act_war1_primal_kyogre", grid: [4, 2], frames: [0, 1, 2, 3],
            ticks: [5, 5, 7, 18], loops: 1, stay: true
          )

          # Trio reels back on the snow shore as the gale slams them
          eng.actor(:anja).play_clip(
            sheet: "act_ch11_kyogre_storm", grid: [4, 4], frames: [9, 11, 12],
            ticks: [4, 6, 16], stay: true
          )
          eng.actor(:pc).move_to(18.0, 18.4, duration: 0.28, walk: false, dir: :up)
          eng.actor(:juno).move_to(20.4, 18.2, duration: 0.28, walk: false, dir: :up)
          eng.zoom_map(1.34, duration: 0.85, focus: [18.0, 13.3], ease: :out_cubic)
          eng.wait(1.35)

          # Beat 5: ORIGIN PULSE SPHERES + 2f Impact + pbZoomMap Shockwave + WARM TORRENTIAL DELUGE!
          eng.play_se("Anim/HyperBeam", volume: 90, pitch: 82)
          eng.play_se("Anim/Water3", volume: 95)
          eng.actor(:kyogre).play_clip(
            sheet: "act_war1_primal_kyogre", grid: [4, 2], frames: [4, 5, 3],
            ticks: [6, 10, 20], stay: true
          )
          # 5 radiant cyan-gold Origin Pulse spheres igniting around Primal Kyogre!
          [[15.2, 12.1], [20.8, 12.1], [18.0, 11.1], [15.8, 14.2], [20.2, 14.2]].each_with_index do |(ox, oy), oi|
            eng.spawn_vfx(nil, sheet: "pf_vfx_origin_pulse", tx: ox, ty: oy,
                          grid: [4, 2], frames: 0..3, ticks: [3, 3, 4, 4],
                          blend: :add, scale: 0.95 + (oi == 2 ? 0.22 : 0.0), z_layer: :above)
            eng.wait(0.08) if oi < 4
          end

          eng.impact_beat(hitstop_sec: 0.12)
          eng.flash(color: [184, 238, 255], power: 225, duration: 0.34)
          eng.shake(power: 6, duration: 0.55, decay: true)
          eng.spawn_vfx(nil, sheet: "pf_vfx_origin_pulse", tx: 18.0, ty: 13.1,
                        grid: [4, 2], frames: 0..3, ticks: [3, 4, 4, 5],
                        blend: :add, scale: 1.0, grow: [0.85, 3.2, 0.72], fade: 0.25, z_layer: :above)
          eng.zoom_map(1.0, duration: 0.55, ease: :out_cubic)

          # SUDDEN TORRENTIAL WARM DELUGE pouring out of the clear midnight sky onto the frozen lake!
          eng.set_tone(-46, -24, 18, 22, duration: 0.85)
          eng.play_se("Anim/Water1", volume: 82)
          [12.0, 16.0, 20.0, 24.0].each_with_index do |rx, xi|
            [10.0, 14.0, 18.0].each_with_index do |ry, yi|
              ph = (xi + yi) % 4
              eng.spawn_vfx(:"rain_#{xi}_#{yi}", sheet: "pf_vfx_deluge_rain", tx: rx, ty: ry,
                            grid: [4, 2], frames: [ph, (ph + 1) % 4, (ph + 2) % 4, (ph + 3) % 4],
                            ticks: [2, 2, 2, 2], loops: :forever,
                            blend: :add, opacity: 148, scale: 1.05, z_layer: :above)
            end
          end

          eng.wait(1.25)
          eng.pan_camera_to(18.0, 14.6, duration: 0.5, ease: :in_out)
          eng.actor(:anja).play_clip(
            sheet: "act_ch11_kyogre_storm", grid: [4, 4], frames: [13, 14, 15],
            ticks: [8, 8, 20], stay: true
          )
          eng.wait(0.45)
          eng.say(:ANJA, :shocked, "Warm rain... at midnight on a frozen sea. Hold the platform— the Deep is awake!", hold: 1.40)

          eng.wait(0.75)
          eng.letterbox(false, duration: 0.45)
          eng.wait(0.50)
        ensure
          cues = eng.cues.dup
          fc   = eng.frames_captured
          eng.dispose
        end
        return { :cues => cues, :frames => fc }
      end

      #-------------------------------------------------------------------------
      # SCENE 4 — Ch19 Peak #4 (WAR-1): "Primal Kyogre vs Reshiram Beam Clash"
      # 100% Live Built Map 926 (The Glass Dunes — central battlefront basin)!
      #-------------------------------------------------------------------------
      def play_ch19_war_beam_clash(capture_dir: nil, capture_fps: 30)
        eng = Engine.new(capture_dir: capture_dir, capture_fps: capture_fps)
        begin
          # 1. Stage directly on REAL built Map 926 (The Glass Dunes) at crisp warm dawn!
          eng.transfer_map(926, 25.8, 8.6, hide_player: true)
          # Hide static frontline line-trainers (events 3..8) so our choreographed hosts own the field
          (3..8).each do |eid|
            ev = $game_map.events[eid]
            ev.transparent = true if ev
          end

          eng.set_tone(12, 2, -10, 8, duration: 0.0)
          eng.letterbox(true, height: 32, duration: 0.0)
          eng.play_bgm("ch19_dynast", volume: 82, tag: "ch19_dynast")

          # Isenmar Host (Left / West): Thane Eirik, frost-host soldiers & unobstructed flank banners!
          eng.spawn_actor(:eirik, sheet: "EIRIK", tx: 23.5, ty: 11.3, dir: :right, is_charset: true)
          eng.spawn_actor(:is_s1, sheet: "pfw_soldier_isenmar", tx: 22.5, ty: 9.8,  dir: :right, is_charset: true)
          eng.spawn_actor(:is_s2, sheet: "pfw_soldier_isenmar", tx: 22.5, ty: 11.8, dir: :right, is_charset: true)
          eng.spawn_actor(:is_s3, sheet: "pfw_soldier_isenmar", tx: 23.9, ty: 12.4, dir: :right, is_charset: true)
          eng.spawn_actor(:is_b1, sheet: "pfw_banner_isenmar",  tx: 21.8, ty: 8.6,  grid: [1, 1], is_charset: false)
          eng.spawn_actor(:is_b2, sheet: "pfw_banner_isenmar",  tx: 21.7, ty: 12.1, grid: [1, 1], is_charset: false)

          # Ashkaar Host (Right / East): Dominar Hrothgar, ember-legion soldiers & unobstructed flank banners!
          eng.spawn_actor(:hrothgar, sheet: "HROTHGAR", tx: 36.5, ty: 11.3, dir: :left, is_charset: true)
          eng.spawn_actor(:as_s1, sheet: "pfw_soldier_ashkaar", tx: 37.5, ty: 9.8,  dir: :left, is_charset: true)
          eng.spawn_actor(:as_s2, sheet: "pfw_soldier_ashkaar", tx: 37.5, ty: 11.8, dir: :left, is_charset: true)
          eng.spawn_actor(:as_s3, sheet: "pfw_soldier_ashkaar", tx: 36.1, ty: 12.4, dir: :left, is_charset: true)
          eng.spawn_actor(:as_b1, sheet: "pfw_banner_ashkaar",  tx: 38.2, ty: 8.6,  grid: [1, 1], is_charset: false)
          eng.spawn_actor(:as_b2, sheet: "pfw_banner_ashkaar",  tx: 38.3, ty: 12.1, grid: [1, 1], is_charset: false)

          # Center foreground witnesses along Map 926's southern rim
          eng.spawn_actor(:pc,     sheet: "PLAYER_A", tx: 30.0, ty: 12.5, dir: :up, is_charset: true)
          eng.spawn_actor(:anja,   sheet: "ANJA",     tx: 28.6, ty: 12.7, dir: :up, is_charset: true)
          eng.spawn_actor(:sigrun, sheet: "SIGRUN",   tx: 31.4, ty: 12.7, dir: :up, is_charset: true)

          # Beat 1: Primal Kyogre breaches on the Isenmar flank + Thane Eirik's battle cry!
          eng.play_se("Anim/Water5", volume: 95)
          eng.shake(power: 4, duration: 0.45)
          eng.spawn_vfx(nil, sheet: "pf_vfx_origin_pulse", tx: 25.3, ty: 9.8,
                        grid: [4, 2], frames: 4..7, ticks: [3, 4, 4, 5],
                        blend: :add, scale: 1.25, z_layer: :above, origin: :foot)
          eng.spawn_actor(:kyogre, sheet: "act_war1_primal_kyogre", tx: 25.3, ty: 9.8,
                          grid: [4, 2], is_charset: false, z_bias: 20)
          eng.actor(:kyogre).play_clip(
            sheet: "act_war1_primal_kyogre", grid: [4, 2], frames: [0, 1, 2, 3],
            ticks: [4, 4, 5, 14], stay: true
          )
          eng.play_cry(:KYOGRE_1, volume: 100)
          eng.wait(0.85)
          eng.say(:EIRIK, :angry, "Isenmar! The sea has come to the sand!", hold: 1.15, name: "Thane Eirik")

          # Beat 2: Pan across the Glass Dunes to Ashkaar's flank -> Reshiram unfolds + Hrothgar answers!
          eng.pan_camera_to(34.2, 8.6, duration: 0.85, ease: :in_out)
          eng.wait(0.70)
          eng.flash(color: [255, 224, 172], power: 210, duration: 0.30)
          eng.play_se("Anim/Fire4", volume: 95)
          eng.shake(power: 4, duration: 0.45)
          eng.spawn_actor(:reshiram, sheet: "act_war1_reshiram", tx: 34.7, ty: 9.8,
                          grid: [4, 2], is_charset: false, z_bias: 20)
          eng.actor(:reshiram).play_clip(
            sheet: "act_war1_reshiram", grid: [4, 2], frames: [0, 1, 2, 3],
            ticks: [5, 4, 5, 14], stay: true
          )
          eng.play_cry(:RESHIRAM, volume: 100)
          eng.wait(0.75)
          eng.say(:HROTHGAR, :angry, "Then let it remember fire.", hold: 1.10, name: "Dominar Hrothgar")

          # Beat 3: Center Wide Two-Shot + Darkened Map Tone Contrast + Dual Charge!
          eng.pan_camera_to(30.0, 8.4, duration: 0.75, ease: :in_out)
          eng.set_tone(-76, -78, -56, 64, duration: 0.75)
          eng.play_bgm("ch19_war_clash", volume: 90, tag: "ch19_war_clash")
          eng.wait(0.55)

          # Both titans enter charge poses (frame 4) with spinning muzzle collars at exact mouth Y (-47 offset = -63px)!
          eng.actor(:kyogre).set_cell(4)
          eng.actor(:reshiram).set_cell(4)
          eng.play_se("Anim/Charge_Beam", volume: 95)
          eng.play_se("Anim/Fire5", volume: 82)
          eng.spawn_vfx(:muzzle_l, sheet: "pf_vfx_origin_beam", tx: 26.75, ty: 9.8,
                        grid: [4, 2], frames: 4..7, ticks: [3, 3, 3, 3], loops: :forever,
                        blend: :add, scale: 0.85, offset: [0, -47], z_layer: :above)
          eng.spawn_vfx(:muzzle_r, sheet: "pf_vfx_blue_flare_beam", tx: 33.45, ty: 9.8,
                        grid: [4, 2], frames: 4..7, ticks: [3, 3, 3, 3], loops: :forever,
                        blend: :add, scale: 0.85, offset: [0, -47], z_layer: :above)
          eng.zoom_map(1.18, duration: 0.90, focus: [30.0, 8.2], ease: :in_out)
          eng.wait(0.95)

          # Beat 4: ORIGIN PULSE vs BLUE FLARE LAUNCH & DEAD-CENTER BEAM CLASH!
          eng.actor(:kyogre).set_cell(5)
          eng.actor(:reshiram).set_cell(5)
          eng.play_se("Anim/HyperBeam", volume: 100)
          eng.play_se("Anim/Fire6", volume: 95)
          eng.impact_beat(hitstop_sec: 0.12)

          mouth_l = 26.75
          mouth_r = 33.45
          beam_l = eng.spawn_vfx(:beam_l, sheet: "pf_vfx_origin_beam", tx: mouth_l, ty: 9.8,
                                 grid: [4, 2], frames: 0..3, ticks: [2, 2, 2, 2], loops: :forever,
                                 blend: :add, origin: :left, offset: [0, -47], z_layer: :above)
          beam_r = eng.spawn_vfx(:beam_r, sheet: "pf_vfx_blue_flare_beam", tx: mouth_r, ty: 9.8,
                                 grid: [4, 2], frames: 0..3, ticks: [2, 2, 2, 2], loops: :forever,
                                 blend: :add, origin: :right, offset: [0, -47], z_layer: :above)

          # Rapid 10-frame (0.33s) launch extension across the desert to dead-center tx = 30.0!
          10.times do |fi|
            u = (fi + 1) / 10.0
            span_l = ((30.0 - mouth_l) * u * 32.0) / 128.0
            span_r = ((mouth_r - 30.0) * u * 32.0) / 128.0
            beam_l.set_scale([span_l, 0.08].max, 0.95)
            beam_r.set_scale([span_r, 0.08].max, 0.95)
            eng.step_frame
          end

          # DEAD-CENTER COLLISION!
          eng.play_se("Anim/Explosion7", volume: 100)
          eng.play_se("Anim/Ice8", volume: 88)
          eng.impact_beat(hitstop_sec: 0.14)
          eng.flash_ramp(color: [224, 248, 255], steps: [51, 136, 221, 255],
                         step_dur: 0.025, hold_dur: 0.08, fade_dur: 0.28)
          core = eng.spawn_vfx(:clash_core, sheet: "pf_vfx_beam_clash_core", tx: 30.0, ty: 9.8,
                               grid: [4, 2], frames: 0..3, ticks: [2, 2, 2, 2], loops: :forever,
                               blend: :add, scale: 1.25, offset: [0, -47], z_layer: :above)

          # SUSTAINED TUG-OF-WAR SCREEN SHAKE (3.1s = 93 frames) with live beam push-pull!
          eng.shake(power: 6, duration: 3.15, decay: false)
          eng.zoom_map(1.38, duration: 0.85, focus: [30.0, 8.2], ease: :in_out)

          90.times do |fi|
            u = fi / 90.0
            cx = 30.0 + Math.sin(u * 13.5) * 0.92 * (1.0 - 0.30 * u)
            core.set_tile(cx, 9.8)
            pulse_y = 0.96 + 0.14 * Math.sin(fi * 0.9).abs
            beam_l.set_scale(((cx - mouth_l) * 32.0) / 128.0, pulse_y)
            beam_r.set_scale(((mouth_r - cx) * 32.0) / 128.0, pulse_y)

            if fi == 26
              eng.zoom_map(1.12, duration: 0.95, focus: [30.0, 8.2], ease: :in_out)
              eng.flash(color: [215, 246, 255], power: 145, duration: 0.12)
              eng.play_se("Anim/Ice2", volume: 82)
              # Sand beneath the beam seam begins fusing into emerald Trinitite glass!
              eng.spawn_vfx(nil, sheet: "pf_vfx_trinitite_glass_wave", tx: 30.0, ty: 9.4,
                            grid: [4, 2], frames: 4..7, ticks: [5, 5, 6, 8], stay: :forever,
                            blend: :normal, untoned: false, opacity: 155, scale: 0.72, z_layer: :floor)
            elsif fi == 52
              eng.flash(color: [255, 234, 200], power: 155, duration: 0.12)
              eng.play_se("Anim/Fire5", volume: 85)
              # Upward/downward crystalline clash sparks
              eng.spawn_vfx(nil, sheet: "pf_vfx_origin_pulse", tx: cx, ty: 8.3,
                            grid: [4, 2], frames: 0..3, ticks: [2, 2, 3, 3],
                            blend: :add, scale: 0.85, z_layer: :above)
            elsif fi == 74
              eng.flash(color: [216, 255, 236], power: 185, duration: 0.14)
              eng.play_se("Anim/Saint7", volume: 88, pitch: 112)
            end
            eng.step_frame
          end

          # Beat 5: OVERLOAD -> 0.28s DEAD-SILENCE bgm_cut VACUUM (single collapsing mote!)
          eng.zoom_map(1.30, duration: 0.45, focus: [30.0, 8.2], ease: :in_out)
          eng.stop_vfx(:clash_core)
          eng.spawn_vfx(:implode, sheet: "pf_vfx_beam_clash_core", tx: 30.0, ty: 9.8,
                        grid: [4, 2], frames: [4, 5, 6, 7], ticks: [4, 4, 4, 9],
                        stay: 0.15, blend: :add, scale: 1.35, offset: [0, -47], z_layer: :above)
          eng.wait(0.55)

          # Cut both beams + muzzle collars + HARD 0ms DEAD-SILENCE bgm_cut!
          eng.stop_vfx(:beam_l)
          eng.stop_vfx(:beam_r)
          eng.stop_vfx(:muzzle_l)
          eng.stop_vfx(:muzzle_r)
          eng.bgm_cut
          eng.play_se("Anim/HealBell", volume: 95, pitch: 120)
          eng.wait(0.28)

          # Beat 6: TRINITITE GLASS WAVE SWEEPS ACROSS LIVE MAP 926!!
          eng.play_se("Anim/Ice8", volume: 100, pitch: 80)
          eng.play_se("Anim/Explosion7", volume: 95)
          eng.play_se("Anim/Saint7", volume: 88, pitch: 90)
          eng.impact_beat(hitstop_sec: 0.14)
          eng.flash_ramp(color: [188, 255, 224], steps: [64, 152, 232, 255],
                         step_dur: 0.025, hold_dur: 0.12, fade_dur: 0.46)
          eng.shake(power: 7, duration: 0.65, decay: true)
          eng.zoom_map(1.0, duration: 0.65, ease: :out_cubic)

          # Dual expanding radioactive sea-green Trinitite shockwave domes!
          eng.spawn_vfx(nil, sheet: "pf_vfx_trinitite_glass_wave", tx: 30.0, ty: 8.6,
                        grid: [4, 2], frames: 0..3, ticks: [3, 4, 4, 5],
                        blend: :add, scale: 1.0, grow: [0.65, 3.8, 0.85], fade: 0.25, z_layer: :above)
          eng.spawn_vfx(nil, sheet: "pf_vfx_trinitite_glass_wave", tx: 30.0, ty: 8.6,
                        grid: [4, 2], frames: 0..3, ticks: [4, 5, 5, 6],
                        blend: :add, scale: 0.85, grow: [0.45, 3.1, 1.05], fade: 0.30, z_layer: :above)

          # Staggered pentagonal Trinitite fused-glass crust crystallizing outward across the desert floor!
          [
            [[27.4, 9.2], [32.6, 9.2]],
            [[25.2, 9.8], [34.8, 9.8]],
            [[28.2, 11.1], [31.8, 11.1]]
          ].each_with_index do |pair, pi|
            pair.each do |gx, gy|
              eng.spawn_vfx(nil, sheet: "pf_vfx_trinitite_glass_wave", tx: gx, ty: gy,
                            grid: [4, 2], frames: 4..7, ticks: [3, 4, 5, 8], stay: :forever,
                            blend: :normal, untoned: false, opacity: 165, scale: 0.86, z_layer: :floor)
            end
            eng.play_se("Anim/Ice2", volume: 74, pitch: 88 + pi * 10)
            eng.wait(0.22)
          end

          # Legendaries recoil and settle back as the emerald glass silence falls over the battlefield!
          eng.actor(:kyogre).play_clip(
            sheet: "act_war1_primal_kyogre", grid: [4, 2], frames: [6, 7],
            ticks: [12, 24], stay: true
          )
          eng.actor(:reshiram).play_clip(
            sheet: "act_war1_reshiram", grid: [4, 2], frames: [6, 7],
            ticks: [12, 24], stay: true
          )
          eng.set_tone(-18, 6, -4, 68, duration: 1.4)
          eng.play_bgm("ch19_aftermath", volume: 78, tag: "ch19_aftermath")

          # Floating glass-dust motes drifting slowly over the vitrified Glass Dunes
          10.times do |mi|
            eng.spawn_vfx(nil, sheet: "pf_vfx_smoke_and_motes", tx: 24.0 + mi * 1.3, ty: 12.2 - (mi % 3) * 1.1,
                          grid: [4, 2], frames: [7], hold: 4.5, blend: :add,
                          drift: [4 - (mi % 3) * 3, -18 - (mi % 4) * 4], fade: 0.8, z_layer: :above)
          end

          # Sigrun & Anja step forward onto the newly fused emerald glass beside the PC
          eng.actor(:anja).move_to(29.0, 11.3, duration: 0.85, walk: true, dir: :up)
          eng.actor(:sigrun).move_to(31.0, 11.3, duration: 0.85, walk: true, dir: :up)
          eng.wait(1.0)

          eng.say(:SIGRUN, :neutral, "Father. Enough. Nobody won this morning that the dead would agree with.", hold: 1.35)
          eng.say(:ANJA, :sad, "Eirik. Enough. The glass stops here. The Boon will settle it.", hold: 1.35)

          eng.wait(0.9)
          eng.letterbox(false, duration: 0.45)
          eng.wait(0.55)
        ensure
          cues = eng.cues.dup
          fc   = eng.frames_captured
          eng.dispose
        end
        return { :cues => cues, :frames => fc }
      end

      #-------------------------------------------------------------------------
      # SCENE 5 — Ch15 Peak #5 (CE-1): AF 290 "Through Her Eyes" Glassfall Flashback
      # Live Map 295 (Cathedral of the Evergreen — nave, pews & altar dais;
      # Wednesday swaps map_id: 295 -> 391 Hollow Cathedral Living Nave once built!)
      #-------------------------------------------------------------------------
      def play_ch15_ce1_glassfall(capture_dir: nil, capture_fps: 30)
        eng = Engine.new(capture_dir: capture_dir, capture_fps: capture_fps)
        begin
          # 1. Stage on real built Cathedral Map 295 (hide static Evergreen Prior event 2)
          eng.transfer_map(295, 15.0, 14.0, hide_player: true)
          ev_prior = $game_map.events[2]
          ev_prior.transparent = true if ev_prior

          eng.set_tone(-46, -42, -18, 38, duration: 0.0)
          eng.letterbox(true, height: 32, duration: 0.0)
          eng.play_bgm("ch15_ominous", volume: 80, tag: "ch15_ominous")

          # Beat 1: Present-day Hollow Cathedral — Kestrel activates Resonance Gauntlet at the altar!
          eng.spawn_actor(:kestrel, sheet: "KESTREL",  tx: 15.0, ty: 11.4, dir: :down, is_charset: true)
          eng.spawn_actor(:ysolde,  sheet: "YSOLDE",   tx: 13.0, ty: 14.4, dir: :up,   is_charset: true)
          eng.spawn_actor(:pc,      sheet: "PLAYER_A", tx: 15.0, ty: 15.8, dir: :up,   is_charset: true)

          eng.wait(0.45)
          eng.play_se("Anim/HealBell", volume: 92, pitch: 112)
          eng.play_se("Anim/Saint7", volume: 85)
          eng.flash(color: [228, 240, 255], power: 185, duration: 0.25)
          eng.shake(power: 3, duration: 0.35)
          eng.spawn_vfx(nil, sheet: "pf_vfx_sepia_echo_shimmer", tx: 15.0, ty: 11.4,
                        grid: [4, 2], frames: 4..6, ticks: [3, 4, 5],
                        blend: :add, scale: 1.15, z_layer: :above)
          eng.wait(0.45)
          eng.say(:KESTREL, :angry, "Ten years, Ysolde. 'When he's ready.' I'm ready. Watch what really happened.", hold: 1.05)

          # Beat 2: Sepia Memory Dissolve -> AF 290 Choir, Valen, Young Voss, Child & Morwen!
          eng.flash_ramp(color: [255, 240, 206], steps: [40, 124, 212, 255],
                         step_dur: 0.03, hold_dur: 0.10, fade_dur: 0.42)
          eng.wait(0.22)
          eng.clear_actors
          eng.clear_vfxs
          # Iconic warm sepia memory tone (Tone.new(28, 12, -26, 95))!
          eng.set_tone(28, 12, -26, 95, duration: 0.0)

          # AF 290 Sanctuary Cast: Valen on dais, Choir row, Young Voss + Observer, Child & Morwen!
          eng.spawn_actor(:valen,  sheet: "VALEN",             tx: 15.0, ty: 10.6, dir: :down, is_charset: true)
          eng.spawn_actor(:ines,   sheet: "trainer_LADY",      tx: 13.6, ty: 11.5, dir: :down, is_charset: true)
          eng.spawn_actor(:ch1,    sheet: "trainer_LASS",      tx: 12.2, ty: 11.5, dir: :down, is_charset: true)
          eng.spawn_actor(:ch2,    sheet: "NPC 04",            tx: 16.4, ty: 11.5, dir: :down, is_charset: true)
          eng.spawn_actor(:ch3,    sheet: "NPC 11",            tx: 17.8, ty: 11.5, dir: :down, is_charset: true)
          eng.spawn_actor(:voss,   sheet: "VOSS",              tx: 19.4, ty: 11.1, dir: :left, is_charset: true)
          eng.spawn_actor(:obs,    sheet: "trainer_SCIENTIST", tx: 20.6, ty: 11.3, dir: :left, is_charset: true)
          eng.spawn_actor(:child,  sheet: "NPC 02",            tx: 15.0, ty: 14.5, dir: :up,   is_charset: true)
          eng.spawn_actor(:morwen, sheet: "MORWEN",            tx: 10.8, ty: 14.9, dir: :right, is_charset: true)

          # Warm sepia memory ribbons drifting gently across AF 290 sanctuary
          [[10.5, 11.5, 0], [15.0, 12.0, 1], [19.5, 11.5, 2], [12.5, 15.8, 3], [17.5, 15.8, 1]].each_with_index do |(sx, sy, ph), si|
            eng.spawn_vfx(:"sepia_#{si}", sheet: "pf_vfx_sepia_echo_shimmer", tx: sx, ty: sy,
                          grid: [4, 2], frames: [ph, (ph + 1) % 4, (ph + 2) % 4, (ph + 3) % 4],
                          ticks: [6, 6, 6, 6], loops: :forever, blend: :add, opacity: 145, z_layer: :above)
          end

          eng.zoom_map(1.24, duration: 0.95, focus: [17.8, 11.4], ease: :in_out)
          eng.wait(0.85)
          eng.say(:VOSS, :neutral, "The Choir's note is climbing. Hold the Crown steady— eighteen Plates, one reading.", hold: 1.15, name: "Young Voss")

          # Beat 3: GREAT PRISM SKY FRACTURE OVERHEAD + 0.28s DEAD-SILENCE bgm_cut VACUUM!
          eng.zoom_map(1.36, duration: 0.75, focus: [15.0, 10.6], ease: :in_out)
          eng.play_se("Anim/Saint7", volume: 88, pitch: 118)
          eng.play_se("Anim/Ice5", volume: 82)
          eng.spawn_vfx(:sky_crack, sheet: "pf_vfx_sky_fracture", tx: 15.0, ty: 9.7,
                        grid: [4, 2], frames: 0..3, ticks: [4, 4, 5, 10], stay: 0.55,
                        blend: :add, scale: 1.45, z_layer: :above)
          eng.wait(0.70)

          # LAW 2: 0.28s DEAD-SILENCE VACUUM + BELL BREAKING!
          eng.bgm_cut
          eng.play_se("Anim/HealBell", volume: 100, pitch: 70)
          eng.play_se("Anim/Ice8", volume: 92, pitch: 112)
          eng.wait(0.28)

          # THE COLORLESS SPLINTER FLIES FROM THE CROWN INTO THE CHILD'S CHEST!
          eng.impact_beat(hitstop_sec: 0.14)
          eng.flash(color: [248, 252, 255], power: 240, duration: 0.26)
          eng.shake(power: 6, duration: 0.45)
          eng.play_bgm("ch15_decretum", volume: 88, tag: "ch15_decretum")
          eng.zoom_map(1.0, duration: 0.45, ease: :out_cubic)

          eng.spawn_vfx(nil, sheet: "pf_vfx_sky_fracture", tx: 15.0, ty: 9.8,
                        grid: [4, 2], frames: [4, 5, 6], ticks: [2, 2, 2], loops: 2,
                        blend: :add, scale: 1.05, move_to: [15.0, 14.5, 0.34], z_layer: :above)
          eng.wait(0.34)
          eng.spawn_vfx(:child_glow, sheet: "pf_vfx_sky_fracture", tx: 15.0, ty: 14.5,
                        grid: [4, 2], frames: [7], hold: 1.6, fade: 0.4,
                        blend: :add, scale: 0.95, z_layer: :above)

          # Beat 4: BOTTLE-GREEN TRINITITE GLASSFALL CURTAIN SWEEPS SANCTUARY AS MORWEN SHIELDS THE CHILD!
          eng.actor(:morwen).move_to(14.3, 14.6, duration: 0.52, walk: true, dir: :right)
          eng.play_se("Anim/Ice8", volume: 95, pitch: 86)
          eng.shake(power: 5, duration: 0.90, decay: true)

          # Sweeping bottle-green Glassfall wave curtain rolling left -> right across pews & nave!
          [[9.2, 11.8], [9.2, 15.6]].each do |gx, gy|
            eng.spawn_vfx(nil, sheet: "pf_vfx_glassfall_curtain", tx: gx, ty: gy,
                          grid: [4, 2], frames: 0..3, ticks: [4, 4, 4, 5], loops: 2,
                          blend: :add, scale: 1.45, move_to: [21.2, gy, 1.05], z_layer: :above)
          end

          # Bottle-green vitrified glass spires & floor sheen crystallizing over outer pews behind the wave!
          [[10.2, 13.6], [19.8, 13.6], [10.4, 16.4], [19.6, 16.4]].each_with_index do |(cx, cy), ci|
            eng.spawn_vfx(:"gspire_#{ci}", sheet: "pf_vfx_glassfall_curtain", tx: cx, ty: cy,
                          grid: [4, 2], frames: [4, 5, 6], ticks: [4, 5, 10], stay: :forever,
                          blend: :normal, untoned: false, scale: 0.92, z_layer: :mid, origin: :foot)
            eng.spawn_vfx(:"gsheen_#{ci}", sheet: "pf_vfx_glassfall_curtain", tx: cx, ty: cy + 0.4,
                          grid: [4, 2], frames: [7], hold: 1.0, stay: :forever,
                          blend: :normal, untoned: false, opacity: 145, scale: 1.05, z_layer: :floor)
            eng.play_se("Anim/Ice2", volume: 74, pitch: 92 + ci * 8) if ci.even?
            eng.wait(0.22)
          end

          # Morwen's Mismagius rises gently beside the shielded child
          eng.spawn_actor(:mismagius, sheet: "Followers/MISMAGIUS", tx: 15.9, ty: 14.4,
                          dir: :left, grid: [4, 4], is_charset: true)
          eng.actor(:mismagius).opacity = 220
          eng.play_cry(:MISMAGIUS, volume: 82)
          eng.wait(0.45)
          eng.say(:MORWEN, :sad, "Take them to Edda's boat at midnight. I'll carry the name... Kestrel, I'm sorry.", hold: 1.25)

          # Beat 5: TEN YEARS LATER — GHOSTLY ECHO_MORWEN TURNS ACROSS THE NAVE TO LOOK STRAIGHT AT YOU!
          eng.flash(color: [192, 224, 255], power: 195, duration: 0.42)
          eng.clear_actors
          eng.clear_vfxs
          # Haunted twilight-indigo echo tone (half-returned across ten years!)
          eng.set_tone(-38, -28, 4, 62, duration: 0.85)
          eng.pan_camera_to(15.0, 14.8, duration: 0.6, ease: :in_out)

          eng.spawn_actor(:pc,          sheet: "PLAYER_A",            tx: 15.0, ty: 16.4, dir: :up,   is_charset: true)
          eng.spawn_actor(:kestrel,     sheet: "KESTREL",             tx: 12.6, ty: 13.0, dir: :down, is_charset: true)
          eng.spawn_actor(:ysolde,      sheet: "YSOLDE",              tx: 17.4, ty: 13.0, dir: :down, is_charset: true)
          eng.spawn_actor(:echo_morwen, sheet: "trainer_ECHO_MORWEN", tx: 15.0, ty: 13.8, dir: :up,   is_charset: true)
          eng.actor(:echo_morwen).opacity = 185

          eng.spawn_vfx(:echo_halo, sheet: "pf_vfx_sepia_echo_shimmer", tx: 15.0, ty: 13.8,
                        grid: [4, 2], frames: [4, 5], ticks: [8, 8], loops: :forever,
                        blend: :add, scale: 1.15, z_layer: :above)
          eng.wait(0.75)

          # Impossibly, across ten years, Echo Morwen turns her head straight :down at the PC!
          eng.actor(:echo_morwen).set_dir(:down)
          eng.stop_vfx(:echo_halo)
          eng.spawn_vfx(:echo_gaze, sheet: "pf_vfx_sepia_echo_shimmer", tx: 15.0, ty: 13.8,
                        grid: [4, 2], frames: [6], hold: 1.8, fade: 0.5,
                        blend: :add, scale: 1.25, z_layer: :above)
          eng.play_se("Anim/HealBell", volume: 84, pitch: 105)
          eng.zoom_map(1.30, duration: 0.90, focus: :echo_morwen, ease: :in_out)
          eng.wait(0.65)

          eng.say(:MORWEN, :neutral, "Little one. You came back. I told her not to let you.", hold: 1.40, name: "Echo Morwen")

          # Echo Morwen dissolves into silver memory petals across the quiet Cathedral
          eng.spawn_vfx(nil, sheet: "pf_vfx_sepia_echo_shimmer", tx: 15.0, ty: 13.8,
                        grid: [4, 2], frames: [7], hold: 0.95, fade: 0.45,
                        blend: :add, scale: 1.35, z_layer: :above)
          18.times do |fi|
            eng.actor(:echo_morwen).opacity = (185 * (1.0 - (fi + 1) / 18.0)).round
            eng.step_frame
          end
          eng.remove_actor(:echo_morwen)
          eng.zoom_map(1.0, duration: 0.65, ease: :out)
          eng.letterbox(false, duration: 0.45)
          eng.wait(0.50)
        ensure
          cues = eng.cues.dup
          fc   = eng.frames_captured
          eng.dispose
        end
        return { :cues => cues, :frames => fc }
      end

      #-------------------------------------------------------------------------
      # SCENE 6 — Ch21 Peak #6: "The Ring & The Light" Arceus Finale
      # Live Map 285 (Briar Hall - Upper Court white-stone summit terrace;
      # Wednesday swaps map_id: 285 -> 491 Crownhaven Prism Arena once built!)
      #-------------------------------------------------------------------------
      def play_ch21_valen_arceus_finale(capture_dir: nil, capture_fps: 30)
        eng = Engine.new(capture_dir: capture_dir, capture_fps: capture_fps)
        begin
          # 1. Stage directly on live white-stone summit terrace Map 285 (hide static Guard event 2)
          eng.transfer_map(285, 48.5, 22.8, hide_player: true)
          ev_guard = $game_map.events[2]
          ev_guard.transparent = true if ev_guard

          # Bleed-violet summit sky tone as Arceus is held bound above the Concordance Ring!
          eng.set_tone(-48, -64, -18, 46, duration: 0.0)
          eng.letterbox(true, height: 32, duration: 0.0)
          eng.play_bgm("ch21_arceus_bound", volume: 84, tag: "ch21_arceus_bound")

          # Golden Concordance Ring floor circle (z=5 under Valen, Ilsa & Voss!)
          eng.spawn_vfx(:conc_ring, sheet: "pf_vfx_arceus_18locks", tx: 48.5, ty: 24.4,
                        grid: [4, 2], frames: [4, 5], ticks: [10, 10], loops: :forever,
                        blend: :add, scale: 1.10, z_layer: :mid)

          # Cast positioned cleanly across the white-stone summit terrace
          eng.spawn_actor(:valen,     sheet: "VALEN",     tx: 48.5, ty: 24.4, dir: :up, is_charset: true)
          eng.spawn_actor(:ilsa,      sheet: "ILSA",      tx: 47.2, ty: 24.8, dir: :up, is_charset: true)
          eng.spawn_actor(:voss,      sheet: "VOSS",      tx: 51.8, ty: 23.8, dir: :up, is_charset: true)
          eng.spawn_actor(:pc,        sheet: "PLAYER_A",  tx: 48.5, ty: 26.2, dir: :up, is_charset: true)
          eng.spawn_actor(:celestine, sheet: "CELESTINE", tx: 44.6, ty: 25.4, dir: :up, is_charset: true)
          eng.spawn_actor(:kestrel,   sheet: "KESTREL",   tx: 52.4, ty: 25.4, dir: :up, is_charset: true)

          # BOUND ARCEUS suspended high above the sanctuary portal inside the 18 Golden-Chain Locks!
          eng.spawn_actor(:arceus, sheet: "act_ch21_arceus_bound", tx: 48.5, ty: 21.0,
                          grid: [4, 2], is_charset: false, z_bias: 35)
          eng.actor(:arceus).play_clip(
            sheet: "act_ch21_arceus_bound", grid: [4, 2], frames: [0, 1, 0, 1],
            ticks: [10, 10, 10, 10], loops: :forever
          )
          eng.spawn_vfx(:locks18, sheet: "pf_vfx_arceus_18locks", tx: 48.5, ty: 19.6,
                        grid: [4, 2], frames: [0, 1], ticks: [8, 8], loops: :forever,
                        blend: :add, scale: 1.02, z_layer: :above)

          # Beat 1: Arceus strains against the Gilded Chain — Voss marvels at the 18 locks!
          eng.play_cry(:ARCEUS, volume: 100)
          eng.shake(power: 4, duration: 0.50)
          eng.zoom_map(1.24, duration: 0.95, focus: [48.5, 20.5], ease: :in_out)
          eng.wait(1.05)
          eng.zoom_map(1.0, duration: 0.45, ease: :out)
          eng.pan_camera_to(48.5, 22.9, duration: 0.45, ease: :in_out)
          eng.wait(0.35)
          eng.say(:VOSS, :shocked, "Eighteen Plates. Eighteen golden locks. Look at it— it's magnificent!", hold: 1.10)

          # Beat 2: Valen & Ilsa hold the Concordance Ring together!
          eng.zoom_map(1.14, duration: 0.65, focus: [48.5, 23.6], ease: :in_out)
          eng.play_se("Anim/Saint7", volume: 84)
          eng.wait(0.45)
          eng.say(:ILSA, :neutral, "I've got you, Father. Little owl's got you.", hold: 1.00)
          eng.say(:VALEN, :neutral, "Go. Free it. I'll hold the door. I've had thirty years of practice.", hold: 1.10)

          # Beat 3: BLAZING 18-HUE PRISM HELIX SHATTERS LOCK #18!
          eng.pan_camera_to(48.5, 22.6, duration: 0.45, ease: :in_out)
          eng.zoom_map(1.0, duration: 0.45, ease: :out)
          eng.set_tone(-78, -80, -48, 66, duration: 0.50)

          # 17 locks released -> Lock #18 blazing white-hot at top apex!
          eng.stop_vfx(:locks18)
          eng.spawn_vfx(:lock_final, sheet: "pf_vfx_arceus_18locks", tx: 48.5, ty: 19.6,
                        grid: [4, 2], frames: [2], hold: 1.0, stay: :forever,
                        blend: :add, scale: 1.08, z_layer: :above)
          eng.actor(:arceus).play_clip(
            sheet: "act_ch21_arceus_bound", grid: [4, 2], frames: [2, 3],
            ticks: [14, 16], stay: true
          )

          # Launch vertical 18-Hue Prism Helix from Valen & PC's Ring straight into Lock #18!
          eng.play_se("Anim/Charge_Beam", volume: 95)
          eng.play_se("Anim/HyperBeam", volume: 90, pitch: 112)
          eng.shake(power: 5, duration: 1.45, decay: false)
          eng.spawn_vfx(:helix_bot, sheet: "pf_vfx_prism_helix_18", tx: 48.5, ty: 23.4,
                        grid: [4, 2], frames: 0..3, ticks: [2, 2, 2, 2], loops: :forever,
                        blend: :add, scale: 1.05, z_layer: :above)
          eng.spawn_vfx(:helix_top, sheet: "pf_vfx_prism_helix_18", tx: 48.5, ty: 20.6,
                        grid: [4, 2], frames: [2, 3, 0, 1], ticks: [2, 2, 2, 2], loops: :forever,
                        blend: :add, scale: 1.05, z_layer: :above)
          eng.zoom_map(1.22, duration: 1.05, focus: [48.5, 21.0], ease: :in_out)
          eng.wait(1.10)

          # LOCK #18 SHATTERS!! 2f Impact Silhouette + 18-Hue Starburst!
          eng.stop_vfx(:lock_final)
          eng.spawn_vfx(nil, sheet: "pf_vfx_arceus_18locks", tx: 48.5, ty: 19.6,
                        grid: [4, 2], frames: [3], hold: 0.45, fade: 0.2,
                        blend: :add, scale: 1.25, z_layer: :above)
          eng.spawn_vfx(nil, sheet: "pf_vfx_prism_helix_18", tx: 48.5, ty: 19.6,
                        grid: [4, 2], frames: [4, 5, 6], ticks: [3, 4, 5],
                        blend: :add, scale: 1.0, grow: [0.85, 2.55, 0.55], fade: 0.2, z_layer: :above)
          eng.play_se("Anim/Explosion7", volume: 95)
          eng.play_se("Anim/Ice8", volume: 95, pitch: 115)
          eng.impact_beat(hitstop_sec: 0.14)
          eng.flash_ramp(color: [255, 248, 224], steps: [64, 152, 232, 255],
                         step_dur: 0.025, hold_dur: 0.10, fade_dur: 0.35)
          eng.wait(0.35)

          # Beat 4: LAW 2 0.30s DEAD-SILENCE bgm_cut VACUUM -> VALEN DISSOLVES INTO PURE LIGHT!
          eng.stop_vfx(:helix_bot)
          eng.stop_vfx(:helix_top)
          eng.stop_vfx(:conc_ring)
          eng.bgm_cut
          eng.play_se("Anim/HealBell", volume: 98, pitch: 100)
          eng.wait(0.30)

          # T-KT enters gently as Valen's crystal turns to pure radiant light!
          eng.play_bgm("ch21_tkt", volume: 88, tag: "ch21_tkt")
          eng.set_tone(10, 6, -4, 18, duration: 1.0)
          eng.zoom_map(1.24, duration: 0.85, focus: [48.5, 24.4], ease: :in_out)
          eng.spawn_vfx(:valen_pillar, sheet: "pf_vfx_arceus_18locks", tx: 48.5, ty: 24.6,
                        grid: [4, 2], frames: [6, 7], ticks: [8, 8], loops: :forever,
                        blend: :add, scale: 0.95, origin: :foot, z_layer: :above)
          eng.wait(0.45)

          eng.say(:VALEN, :happy, "Little owl... Avery. Velmora is free.", hold: 1.10)

          # Valen dissolves into pure radiant light, leaving the empty cracked Crown on the flagstones!
          18.times do |fi|
            eng.actor(:valen).opacity = (255 * (1.0 - (fi + 1) / 18.0)).round
            eng.step_frame
          end
          eng.remove_actor(:valen)
          eng.stop_vfx(:valen_pillar)
          eng.spawn_vfx(:empty_crown, sheet: "pf_vfx_legend_plate_burst", tx: 48.5, ty: 25.0,
                        grid: [4, 2], frames: [4, 5, 6, 7], ticks: [4, 4, 5, 16], stay: :forever,
                        blend: :normal, untoned: false, scale: 0.90, z_layer: :mid)
          eng.play_se("Anim/HealBell", volume: 78, pitch: 126)
          eng.actor(:ilsa).move_to(47.4, 25.0, duration: 0.55, walk: true, dir: :right)
          eng.wait(0.80)

          # Beat 5: FREED RADIANT ARCEUS DESCENDS + WHOLE LEGEND PLATE BURST!
          eng.set_tone(24, 18, 4, 8, duration: 1.15)
          eng.zoom_map(1.0, duration: 0.70, ease: :out_cubic)
          eng.pan_camera_to(48.5, 22.9, duration: 0.70, ease: :in_out)

          eng.actor(:arceus).play_clip(
            sheet: "act_ch21_arceus_bound", grid: [4, 2], frames: [4, 5, 6, 7],
            ticks: [7, 8, 10, 24], stay: true
          )
          eng.actor(:arceus).move_to(48.5, 21.8, duration: 1.30, walk: false, ease: :out_cubic)
          # 18 harmonious Plate lights orbiting cleanly behind Freed Arceus!
          eng.spawn_vfx(:plates_free, sheet: "pf_vfx_prism_helix_18", tx: 48.5, ty: 20.5,
                        grid: [4, 2], frames: [7], hold: 1.0, stay: :forever,
                        blend: :add, scale: 1.68, spin: 18.0, z_layer: :above)
          eng.wait(1.05)

          # THE WHOLE LEGEND PLATE CLICKS TOGETHER CLEANLY BETWEEN ARCEUS & VALEN'S EMPTY CROWN!
          eng.play_cry(:ARCEUS, volume: 95)
          eng.play_se("Anim/Saint7", volume: 90, pitch: 108)
          eng.flash(color: [255, 248, 214], power: 195, duration: 0.38)
          eng.spawn_vfx(:legend_plate, sheet: "pf_vfx_legend_plate_burst", tx: 48.5, ty: 23.6,
                        grid: [4, 2], frames: [0, 1, 2, 3], ticks: [6, 7, 10, 24], stay: :forever,
                        blend: :add, opacity: 225, scale: 0.88, z_layer: :above)
          eng.wait(0.85)

          eng.say(:ILSA, :crying, "Little light. You have carried me far. I will not take what is not given.", hold: 1.50, name: "Arceus (via Ilsa)")

          eng.wait(0.85)
          eng.letterbox(false, duration: 0.45)
          eng.wait(0.55)
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
  when :CH5_SHATTER, :SH1                      then Prismfall::AdvancedAnimations.play_ch5_spire_shatter(**opts)
  when :CH9_UNMASK,  :IR1                      then Prismfall::AdvancedAnimations.play_ch9_trevenant_unmasking(**opts)
  when :CH11_KYOGRE, :CH11_THAW, :KYOGRE       then Prismfall::AdvancedAnimations.play_ch11_kyogre_awakens(**opts)
  when :CH19_WAR, :WAR_CLIMAX, :WAR1           then Prismfall::AdvancedAnimations.play_ch19_war_beam_clash(**opts)
  when :CH15_GLASSFALL, :CE1, :GLASSFALL       then Prismfall::AdvancedAnimations.play_ch15_ce1_glassfall(**opts)
  when :CH21_ARCEUS, :CH21_FINALE, :THE_LIGHT  then Prismfall::AdvancedAnimations.play_ch21_valen_arceus_finale(**opts)
  else
    PBDebug.log("[AdvancedAnimations] Unknown scene #{id.inspect}") if defined?(PBDebug)
    nil
  end
end
```
