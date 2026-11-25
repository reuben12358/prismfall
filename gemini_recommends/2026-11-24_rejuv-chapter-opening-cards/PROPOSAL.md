# Pokémon Prismfall — Rejuvenation-Style Chapter Opening Pages (All 24 Chapters)

> **Status:** Ready for drop-in adoption (Art dual-synced & SHA-256 verified; Ruby engine `ruby -c` + 24-chapter runtime smoke-tested).
> **Engine Target:** Pokémon Essentials v21.1 / mkxp-z (`512×384` native viewport).
> **Companion Code:** [`020_ChapterOpeningCards.rb`](020_ChapterOpeningCards.rb)

---

## 1. Executive Summary

This package equips **every single chapter boundary in Pokémon Prismfall** — **Prologue, Chapters 1–21, Post-Game (*Fallmorn*), and Ruin Route (*Every Type and None*)** — with a **6.0-second Pokémon Rejuvenation-grade animated Chapter Opening Page**:

1. **24 bespoke textless `512×384` (4:3) RGB PNG artworks** drawn in one unified painterly anime JRPG aesthetic with **zero baked-in text, logos, or watermarks**, dual-synced byte-identically to both:
   - `graphics/Pictures/ChapterCards/<slug>.png`
   - `art/out/Graphics/Pictures/ChapterCards/<slug>.png`
2. **Drop-in Essentials v21.1 Ruby engine** ([`020_ChapterOpeningCards.rb`](020_ChapterOpeningCards.rb)) rendering:
   - Smooth sub-pixel Ken Burns pan & zoom across the `512×384` backdrop
   - 24 chapter-specific real-time particle emitters (`:fog`, `:seaspray`, `:stagedust`, `:silk`, `:stormrain`, `:neonrain`, `:sand`, `:fireflies`, `:embers`, `:duskrain`, `:petals`, `:snow`, `:cloudgale`, `:glassshards`, `:crystaldust`, `:spectralmist`, `:electricarcs`, `:bubbles`, `:lanternmoths`, `:warembers`, `:festivalmotes`, `:prismrays`, `:fallmorn`, `:gildeddust`)
   - Cinema letterbox framing breathing open/closed
   - Sweeping dark translucent obsidian gradient ribbon with metallic chapter-accent hairlines, diamond crests, and a moving specular sheen
   - Staggered serif typography reveal (**Act Eyebrow → Chapter Number → Italic Serif Chapter Title → Location Caption**)
   - Optional crystalline ME/SE chime (`Chapter Card Prismatic Wipe`, or `Glitch Tear Static` on Ruin `:CH23`) with graceful silent fallback if audio files aren't yet installed
   - Automatic `Prismfall::Cutscene.photosensitive?` compliance (disables storm/electric flashes automatically)
   - Graceful skip after `1.5s` (`Input::USE` / `Input::BACK` triggers a smooth `0.45s` curtain fade) and zero-leak `ensure` disposal of all bitmaps, sprites, and viewports
   - Built-in **F9 Debug Menu** previewer (`Chapter Opening Cards (24)`) for instant playtesting

---

## 2. Drop-In Installation for Claude (Zero Core Edits)

1. Copy [`020_ChapterOpeningCards.rb`](020_ChapterOpeningCards.rb) into:
   ```text
   plugins/Prismfall Cutscenes/020_ChapterOpeningCards.rb
   ```
   *(All 24 PNG artworks are ALREADY installed & dual-synced in `graphics/Pictures/ChapterCards/` and `art/out/Graphics/Pictures/ChapterCards/`.)*
2. Recompile plugins on next Essentials boot (or run the F9 Debug Menu → Playtest → **Chapter Opening Cards (24)** to audition any card immediately).

---

## 3. One-Line Hook Calls for Story Scripts & Map Events

Call **`pbChapterOpeningCard(id)`** (or alias **`pfm_chapter_card(id)`**) from any RMXP event script command or Ruby story transition:

```ruby
# Standard 6.0-second Rejuvenation opening page (skippable after 1.5s)
pbChapterOpeningCard(:CH00)            # Prologue — "The Last Ferry"
pbChapterOpeningCard(:CH01)            # Chapter 1 — "Tidewatch"
pbChapterOpeningCard(:CH12)            # Chapter 12 — "Dead Letters"
pbChapterOpeningCard(:CH21)            # Chapter 21 — "Sovereign"
pbChapterOpeningCard(:CH22)            # Post-Game — "Fallmorn"
pbChapterOpeningCard(:CH23)            # Ruin Route — "Every Type and None"

# Friendly aliases & integer chapter numbers also work:
pbChapterOpeningCard(:PROLOGUE)
pbChapterOpeningCard(5)                # => :CH05 ("Ten Years of Light")
pfm_chapter_card(:FALLMORN)            # => :CH22 ("Fallmorn")
pfm_chapter_card(:RUIN_ROUTE)          # => :CH23 ("Every Type and None")

# Optional overrides:
pbChapterOpeningCard(:CH21, duration: 6.8, skippable: false, duck_bgm: true)
```

### Recommended Hook Placement (`V102` Chapter Counter / Story Transitions)

| Transition Hook | Call | Story Trigger |
|---|---|---|
| New Game / Ferry Opening | `pbChapterOpeningCard(:CH00)` | Arrival at Ferrow's Landing (`20_SCRIPT_CH0-2.md`) |
| `V102` → `1`..`21` | `pbChapterOpeningCard(chapter_num)` | Immediately upon advancing chapter variable `V102` (after fade-to-black or on morning wake autorun) |
| Post-Game Wake (`V143 = 0`) | `pbChapterOpeningCard(:CH22)` | First morning load after credits (`41_SCRIPT_POSTGAME.md` §P0) |
| Ruin Route Crossing (`:ch15_look_back`) | `pbChapterOpeningCard(:CH23)` | Stepping through the black glass pane into the Ferrymen's Mile (`12_RUIN_ROUTE.md` / `42_SCRIPT_RUIN_KING.md`) |

*(If hooking inside a centralized `advance_chapter(n)` helper, a single line suffices: `pbChapterOpeningCard(n) if n.is_a?(Integer) && n.between?(0, 23)`.)*

---

## 4. Animation Timeline (6.00 Seconds Default)

| Window | Visual Layer | Motion / Behavior |
|---|---|---|
| `0.00s – 0.72s` | Curtain & Letterbox | Obsidian curtain lifts (`opacity 255 → 0`); cinema bars open `28px → 12px` |
| `0.00s – 6.00s` | `512×384` Artwork | Continuous sine ease-in-out slow Ken Burns pan & zoom (`1.015× ↔ 1.095×`) |
| `0.00s – 6.00s` | Particle Emitter | Real-time 30 FPS chapter-specific procedural particles |
| `0.88s` | Audio Cue | Plays `Chapter Card Prismatic Wipe` (ME/SE) or `Glitch Tear Static` (`:CH23` Ruin), non-fatal if absent |
| `0.88s – 1.60s` | Translucent Ribbon | Dark gradient ribbon + metallic hairlines & diamond crests sweep outward from center |
| `1.25s – 2.30s` | Prismatic Sheen | Translucent chapter-accent specular light gleam sweeps left-to-right across ribbon |
| `1.35s – 1.88s` | Act Eyebrow | Tracked uppercase Act label fades & glides up (`+5px → 0`) |
| `1.65s – 2.20s` | Chapter Number | Flanked Chapter Number (`— CHAPTER X —`) fades & glides up (`+6px → 0`) |
| `2.00s – 2.68s` | Chapter Title | Italic Serif Chapter Title blooms in with crisp drop-shadow (`+9px → 0`) |
| `2.52s – 3.12s` | Location Caption | Velmora locale caption settles softly beneath the title (`+4px → 0`) |
| `3.12s – 5.15s` | Atmospheric Hold | Full composition breathes with live camera drift & particles |
| `5.15s – 6.00s` | Curtain Close | Ribbon fades out, cinema bars close gently, obsidian curtain returns cleanly |

---

## 5. Complete 24-Chapter Asset & SHA-256 Manifest

All 24 assets are exact **`512×384` RGB PNG** (`8.96 MB` total), visually audited for zero baked-in text/logos, and **byte-identical** across `graphics/Pictures/ChapterCards/` and `art/out/Graphics/Pictures/ChapterCards/`:

| Key | Label | Title | Act | Filename | Particle FX | Size | SHA-256 |
|---|---|---|---|---|---|---|---|
| `:CH00` | PROLOGUE | *The Last Ferry* | Act I — The Last Ferry | `ch00_prologue.png` | `:fog` | 256.1 KB | `77519351f2cdd22996ec1886bc3afea3fe679c4516e5c887b49b39baeac1234e` |
| `:CH01` | CHAPTER 1 | *Tidewatch* | Act I — The Last Ferry | `ch01_tidewatch.png` | `:seaspray` | 372.1 KB | `0ae82d3ca9942fd32dfcfbfa71f36594d1418806e3635a5d37b46f9aaf4b3016` |
| `:CH02` | CHAPTER 2 | *Curtain Call* | Act I — The Last Ferry | `ch02_curtain_call.png` | `:stagedust` | 329.9 KB | `eec3042f2188a1f2e2cdedca71d679f07312afa22625e05704184fe81d18a172` |
| `:CH03` | CHAPTER 3 | *The Weaver's Debt* | Act I — The Last Ferry | `ch03_weavers_debt.png` | `:silk` | 432.8 KB | `e3189f2e2bbc73adbaadf89ef748fd26a9d8349c1aa2bc49a202eb56dfa4d33d` |
| `:CH04` | CHAPTER 4 | *Both Ways* | Act I — The Last Ferry | `ch04_both_ways.png` | `:stormrain` | 377.0 KB | `76e5f655b171692d880f741f00aeceee0ef905f127d768cd6f5652c5c9622883` |
| `:CH05` | CHAPTER 5 | *Ten Years of Light* | Act I — The Last Ferry | `ch05_ten_years_of_light.png` | `:neonrain` | 366.1 KB | `2e3715bb567754e48ed241424dd1a945e3d464106e00ab3bfb2a742a90db156b` |
| `:CH06` | CHAPTER 6 | *What the Sand Keeps* | Act II — Imprints | `ch06_what_the_sand_keeps.png` | `:sand` | 309.0 KB | `c4fa08f0a21f9e239a3db8cd6581be2092fbb8f85054ee15d22722d929c90b22` |
| `:CH07` | CHAPTER 7 | *The Quiet Ward* | Act II — Imprints | `ch07_quiet_ward.png` | `:fireflies` | 380.3 KB | `031df5f3fc2322053d12d8dd8f657dc4fc3501da6c5bc41c5b7d4c7adaa311ac` |
| `:CH08` | CHAPTER 8 | *The Light Stone* | Act II — Imprints | `ch08_light_stone.png` | `:embers` | 383.0 KB | `e51cf1b71dd9e8a1b4501c6524236ac2edb7b0e8e501547cc26c733bf8fba2ef` |
| `:CH09` | CHAPTER 9 | *The Iron Conclave* | Act II — Imprints | `ch09_iron_conclave.png` | `:duskrain` | 384.1 KB | `354e5df622d01dc692802f872871a1ba57698e14b5bd97aa36d836ac294b66e5` |
| `:CH10` | CHAPTER 10 | *The Seat That Blooms* | Act III — Fault Lines | `ch10_seat_that_blooms.png` | `:petals` | 438.7 KB | `83c9618bf648d2c4e0ccc5108b3d18c9a4060ba25c11cc9fc0c57ad640fada5c` |
| `:CH11` | CHAPTER 11 | *The Thaw* | Act III — Fault Lines | `ch11_the_thaw.png` | `:snow` | 390.3 KB | `b3184c8c0fce34331d1ecc6d142a3aa2ad620eaf6ac0b65aa9b902726fe74d1e` |
| `:CH12` | CHAPTER 12 | *Dead Letters* | Act III — Fault Lines | `ch12_dead_letters.png` | `:cloudgale` | 369.4 KB | `ca118d3b19b7ac887c29f7a51b6ae8e0c0809f0dbae0615738a53f67ba6fb29f` |
| `:CH13` | CHAPTER 13 | *Behind the Glass* | Act III — Fault Lines | `ch13_behind_the_glass.png` | `:glassshards` | 407.4 KB | `cc846ed6cd9f710296873a7c004aa8c92462b34ae0672690e6ef5f600d6d02d5` |
| `:CH14` | CHAPTER 14 | *The Deep Seams* | Act IV — The Drowned Crown | `ch14_deep_seams.png` | `:crystaldust` | 394.4 KB | `7e39818f06f0f1edab1e43a7c900198a28c70128f7d19c6015627b4b3ec994f2` |
| `:CH15` | CHAPTER 15 | *The Hollow Cathedral* | Act IV — The Drowned Crown | `ch15_hollow_cathedral.png` | `:spectralmist` | 379.4 KB | `1b14e22b60a40f024bb1e337d0725e34755751466f1d1548f2bf0379ada2f00d` |
| `:CH16` | CHAPTER 16 | *Clear Air* | Act IV — The Drowned Crown | `ch16_clear_air.png` | `:electricarcs` | 374.3 KB | `b4b277b67bb02c0a5814ebaa0c280803c56010799a7efe8543db1f7931648857` |
| `:CH17` | CHAPTER 17 | *The Drowned Crown* | Act IV — The Drowned Crown | `ch17_drowned_crown.png` | `:bubbles` | 441.9 KB | `9336e8a47f92a72325278829a8e2e8c8146aae07e905bfcfad67a79f33558d25` |
| `:CH18` | CHAPTER 18 | *Once Upon a Time* | Act V — Sovereign | `ch18_once_upon_a_time.png` | `:lanternmoths` | 430.0 KB | `de586c6329c4a57f47bc32d7962b03f69e1a881c254f49c82170599757448149` |
| `:CH19` | CHAPTER 19 | *The Last Gate* | Act V — Sovereign | `ch19_last_gate.png` | `:warembers` | 394.6 KB | `71332666db55c0169c9d19d62b06620eef8401ba9c1b86d2d26695ca86d46d1e` |
| `:CH20` | CHAPTER 20 | *The Festival of Champions* | Act V — Sovereign | `ch20_festival_of_champions.png` | `:festivalmotes` | 424.3 KB | `d63769de86bae523c868a939fc0a1e012a4404995b29d0adbda0eed4e5c8b64d` |
| `:CH21` | CHAPTER 21 | *Sovereign* | Act V — Sovereign | `ch21_sovereign.png` | `:prismrays` | 372.1 KB | `2ea5303982f6f926ff26880cf3d44e58ea0d9c246d7b6f4ac13da8270fb998f4` |
| `:CH22` | POST-GAME | *Fallmorn* | Post-Game | `ch22_postgame_fallmorn.png` | `:fallmorn` | 372.5 KB | `96891db0636ca23ab38cd5ef19a8d1db5472a18a98022afbf487b85347be9d9e` |
| `:CH23` | RUIN ROUTE | *Every Type and None* | Ruin Route | `ch23_ruin_route.png` | `:gildeddust` | 395.3 KB | `8bc2b5c360d31a4329953bd11191dfae2de3ab50ea9ff76b1284a6cdadeefd48` |

---

## 6. Interactive HTML Preview Studios & Verification

- **Part 1 Studio (Prologue & Ch 1–11):** `/tmp/prismfall_chapter_cards_part1_studio.html` (`5.81 MB`, Playwright-verified `0` console/page errors, `0` broken images)
- **Part 2 Studio (Ch 12–21, Post-Game & Ruin):** `/tmp/prismfall_chapter_cards_part2_studio.html` (Playwright-verified `0` console/page errors, `0` broken images)
- **Ruby Verification:** `ruby -c 020_ChapterOpeningCards.rb` → `Syntax OK`, plus headless 24-chapter mock-RGSS end-to-end runtime test (`24/24` chapters + aliases passed cleanly).
