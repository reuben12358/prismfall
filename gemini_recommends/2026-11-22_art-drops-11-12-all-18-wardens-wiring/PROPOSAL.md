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
