# Proposal: Wire Art Drops 11–12 (All 18/18 Wardens Live!) into Charset Aliases & B2W2 VS Intro

**Date:** 2026-11-22  
**Live Commits Already Pushed on `origin/main`:** `925d68f`, `70dcbb8`, `925fa8b`, `52f802b`, `af2ace9`, `861cc37`, `152ffa7`, `456d3b7`, `baf79d6`

## Summary
All **18/18 Wardens of Velmora** plus **Fixed Kestrel Overworld**, both Players, Juno, Larch, The Mourner, Aurelian Voss, and Sovereign Valen (**25 complete pure-Gemini cast packs**) are now live on `origin/main`.

A full automated integrity scan confirmed **434/434 dual-synced PNGs** have **100% SHA-256 byte-for-byte parity** between `graphics/` and `art/out/Graphics/`, with **100% `exact2x=True`**, **`semi=0`**, **24/24 overworld mirrors**, **25/25 portrait mirrors**, and **25/25 flush-bottom VS busts**.

### Newly Shipped & Ready to Wire (388 Dual-Synced PNGs)
- **Art Drop 11 (`925d68f..af2ace9`):** `LEADER_CORVIN`, `LEADER_BRANN`, `LEADER_KAITO`, `LEADER_ANJA`, `LEADER_ODESSA`, `LEADER_ILSA` (192 PNGs) + **Pure-Gemini `KESTREL.png` Overworld Fix** (4 PNGs).
- **Art Drop 12 (`861cc37..baf79d6`):** `LEADER_BASTIAN`, `LEADER_YSOLDE`, `LEADER_MAGNUS`, `LEADER_NYX`, `LEADER_CELESTINE`, `LEADER_SIGRUN` (192 PNGs).

---

## Verified Engine-Wiring Changes (Zero Guesswork)

### 1. `plugins/Prismfall Core/025_CharsetAliases.rb`
Audited against all **117 compiled RXDATA maps** in `maps_out/Data/` and `mapgen/layouts/war.py`:
- `trainer_ROCKER` (4/4 events = Rook), `trainer_ELITEFOUR_Lance` (M926 War `"Partner"` = Sigrun), and `trainer_LEADER_Misty` (M926 War `"Partner"` = Marisol) are **100% exclusive** and MUST go in `CHARSET_ALIASES` (note: `NAME_ALIASES` would miss the M926 `"Partner"` event!).
- `trainer_GENTLEMAN` and `trainer_SWIMMER_F` are shared with generic NPCs, so `Marisol`, `Voss`/`Aurelian`, `Valen`, and the remaining Wardens/Mourner belong in `NAME_ALIASES`.

```ruby
  CHARSET_ALIASES = {
    "trainer_RIVAL2"          => "JUNO",      # Gemini pack, 2026-11-21
    "trainer_RIVAL1"          => "KESTREL",
    "trainer_PROFESSOR"       => "LARCH",
    "trainer_ROCKER"          => "ROOK",      # 4/4 events exclusive to Rook (M181/186/193/608)
    "trainer_ELITEFOUR_Lance" => "SIGRUN",    # M926 Glass Dunes "Partner" event (war.py:285)
    "trainer_LEADER_Misty"    => "MARISOL"    # M926 Glass Dunes "Partner" event (war.py:285)
  }
  NAME_ALIASES = {
    "Dorian"    => "DORIAN",
    "Tamsin"    => "TAMSIN",
    "Marisol"   => "MARISOL",   # M174 uses shared trainer_SWIMMER_F
    "Voss"      => "VOSS",      # M100/109/186/608 use shared trainer_GENTLEMAN
    "Aurelian"  => "VOSS",
    "Valen"     => "VALEN",     # M186/608 use shared trainer_GENTLEMAN
    "Rook"      => "ROOK",
    "Sahar"     => "SAHAR",
    "Corvin"    => "CORVIN",
    "Brann"     => "BRANN",
    "Kaito"     => "KAITO",
    "Anja"      => "ANJA",
    "Odessa"    => "ODESSA",
    "Ilsa"      => "ILSA",
    "Bastian"   => "BASTIAN",
    "Ysolde"    => "YSOLDE",
    "Magnus"    => "MAGNUS",
    "Nyx"       => "NYX",
    "Celestine" => "CELESTINE",
    "Sigrun"    => "SIGRUN",
    "Mourner"   => "MOURNER"
  }
```

### 2. `plugins/Prismfall EBDX Bridge/010_Bridge_VersusIntro.rb`
All 12 newly completed Wardens (`CORVIN`..`SIGRUN`) need explicit `VS_IDS` and bespoke `THEMES` (otherwise 10 default to `:violet`):

```ruby
  VS_IDS = {
    :RIVAL_JUNO       => "JUNO",
    :LEADER_JUNO      => "JUNO",
    :RIVAL_KESTREL    => "KESTREL",
    :LARCH            => "LARCH",
    :LEADER_DORIAN    => "DORIAN",
    :LEADER_TAMSIN    => "TAMSIN",
    :LEADER_MARISOL   => "MARISOL",
    :LEADER_ROOK      => "ROOK",
    :LEADER_SAHAR     => "SAHAR",
    :LEADER_CORVIN    => "CORVIN",
    :LEADER_BRANN     => "BRANN",
    :LEADER_KAITO     => "KAITO",
    :LEADER_ANJA      => "ANJA",
    :LEADER_ODESSA    => "ODESSA",
    :LEADER_ILSA      => "ILSA",
    :LEADER_BASTIAN   => "BASTIAN",
    :LEADER_YSOLDE    => "YSOLDE",
    :LEADER_MAGNUS    => "MAGNUS",
    :LEADER_NYX       => "NYX",
    :LEADER_CELESTINE => "CELESTINE",
    :LEADER_SIGRUN    => "SIGRUN",
    :HOLLOW_MOURNER   => "MOURNER",
    :MERIDIAN_VOSS    => "VOSS",
    :CHAMPION_VALEN   => "VALEN"
  }
  THEMES = {
    "PLAYER_A"  => :teal,   "PLAYER_B"  => :green,
    "JUNO"      => :rose,   "KESTREL"   => :blue,   "LARCH"     => :grey,
    "VOSS"      => :grey,   "VALEN"     => :gold,   "MOURNER"   => :green,
    "DORIAN"    => :violet, "TAMSIN"    => :gold,   "MARISOL"   => :blue,
    "ROOK"      => :blue,   "SAHAR"     => :gold,   "CORVIN"    => :violet,
    "BRANN"     => :red,    "KAITO"     => :red,    "ANJA"      => :teal,
    "ODESSA"    => :blue,   "ILSA"      => :rose,   "BASTIAN"   => :gold,
    "YSOLDE"    => :violet, "MAGNUS"    => :grey,   "NYX"       => :violet,
    "CELESTINE" => :rose,   "SIGRUN"    => :red
  }
```

### 3. Already Auto-Wired (Zero Changes Needed)
- `plugins/Prismfall Cutscenes/004_Actors.rb` resolves `Graphics/Trainers/<TTYPE>.png` and `Graphics/Characters/trainer_<TTYPE>.png` before `STAND_INS`.
- `plugins/Prismfall Cutscenes/014_Portraits.rb` already lists all 25 live cast IDs in `CAST`.

---

### 4. Real-Engine Cast GIF QA Audit & Wave 3 Battleback Queue
Inspected all 6 new live-engine cast captures (`docs/battle_captures/cast/{marisol,rook,sahar,mourner,voss,valen}.gif`) plus `docs/battle_captures/intro/{juno,dorian}_b2w2_intro.gif` and all 54 `graphics/EBDX/Battlebacks/battlebg/field_*_hd.png` variants:

- **Cast Art Fidelity (6/6 PASS):** `MARISOL`, `ROOK`, `SAHAR`, `MOURNER`, `VOSS`, and `VALEN` render with 100% disk parity, `0` semi-transparent edge pixels, clean nameplate clearance, and identical scale/boot grounding (`head y=44..50`, boots planted squarely at `y=212`).
- **3 Small Live-Engine Items for Claude:**
  1. **PBS Double-Name Bug on Mourner (`cast/mourner.gif`):** Renders `"You are challenged by The Mourner Mourner!"` / `"The Mourner Mourner sent out Shiftry!"` because `pbs/trainer_types.txt:241-242` sets `[HOLLOW_MOURNER] Name = The Mourner` while `pbs/trainers.txt:10560` uses trainer name `Mourner`. Suggest changing class `Name` to `Hollow` (with trainer name `The Mourner`) or blanking the duplicate prefix.
  2. **Silhouette Opening Headroom (`plugins/Prismfall EBDX Bridge/010_Bridge_VersusIntro.rb:61`):** `INTRO_ZOOM = 3.0` on full-proportion `160×160` sprites crops the top of every trainer's head/hat off the top edge (`y=0`) during the dramatic silhouette slide-in. Lowering `INTRO_ZOOM` to `~2.2–2.4` (or nudging the intro silhouette Y slightly down) frames full heads cleanly. *(Optional visual polish: a subtle translucent elliptical ground drop-shadow under enemy trainers helps ground boots on bright bases like `Prism Arena` and `Meadow`.)*
  3. **Stale Intro Captures:** `docs/battle_captures/intro/dorian_b2w2_intro.gif` still shows the old pre-Gemini non-hat VS bust, diamond bolts, and static 4-frame battle sprite; `juno_b2w2_intro.gif` still shows the old giant-bouquet VS bust and old Meadow backdrop. Both disk assets are already updated and ready for re-capture whenever convenient.
- **Wave 3 Pure-Gemini Battlebacks Queue (Post Image-Quota Reset):**
  - **23 / 54 variants (14 / 36 fields)** are already pure-Gemini upgraded (`Mindscape`, `Prism Arena`, `Dragon's Den`, `Meadow`, `Rainbow`, `Frozen Lake`, `Flower Garden 1–5`, `Hollow Cathedral`, `Water Surface`, `Corrosive Mire`, `Bleed`, `Factory`, `Scrapyard`, `Stormfront`).
  - **Tier 1 Priority Queue (19 variants / 12 fields — 139 default maps + 7 Gyms + Ch19 War):**
    - *Wave 3A (10):* `GRAND_STAGE` (1/2/3 — visible in 4/6 cast GIFs), `SILKWOOD` (Gym 1), `BEACH` (Ferrow's Landing/Saltmere), `NEW_MOON` (base/`_lamplight`/`_abyss`), `NEON_GRID` (base/`_blackout`).
    - *Wave 3B (9):* Shared-horizon Ossaria War set (`DESERT` base/`_bloom`, `FLOODED_DUNES`, `GLASS_DUNES` base/`_mirror`), shared-layout Ashkaar pair (`VOLCANIC`, `ASHEN_WASTE`), `INVERSE`, `FAIRY_TALE`.
  - **Tier 2 Nice-to-Have (7 variants / 5 fields):** `SNOWY_MOUNTAIN`, `CAVE` (base/`_cracked`), `COLOSSEUM` (base/`_frenzy`), `UNDERWATER`, `WILDFIRE_EMBERS`.
  - **Tier 3 Keep As-Is (5 variants / 5 fields — already cohesive):** `MOUNTAIN`, `CRYSTAL_CAVERN`, `DARK_CRYSTAL`, `WASTELAND`, `WILDFIRE`.

