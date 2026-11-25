# Final Canonical Cameo Pack - Wave 3 (`FESTIVAL_SHIV`, `FESTIVAL_LIN`, `FESTIVAL_NOVA`)

**Date:** 2026-11-25  
**Scope:** Completes **ALL 10 / 10 cameos in `design/CAMEOS.md`** (`#7 Shiv`, `#8 Lin`, `#9 Nova`) — **54 unique assets / 108 dual-synced PNGs** bit-identical across `graphics/` and `art/out/Graphics/`.  
**Visual Proof Sheet:** `previews/141_cameos_wave3_shiv_lin_nova_proof.png` (Official Home-Game Refs vs Restored Prismfall 18-Asset Suites)  
**Interactive Studio:** `/tmp/prismfall_cameos_wave3_studio.html` (100% offline self-contained animated review studio, Playwright-verified `0` errors)

---

## 1. Reuben's Permanent Cameo Art Rule — Canonical Provenance Verified

Every cameo was verified directly against official home-game sprites from *Pokémon Desolation* (`pokemon-desolation.fandom.com`) and *Pokémon Reborn* (`pokemon-reborn.fandom.com`) — **zero invented OC outfits**:

| Cameo Slot | Home Game | Official Verified Appearance (Overrides Older Unverified Notes) | Prismfall 16-Frame B2W2 Battle Animation |
|---|---|---|---|
| **`FESTIVAL_SHIV`** / **`SHIV`** | *Pokémon Desolation* (also *Reborn* postgame) | Spiky jet-black hair, dark eyes, sly smirk, charcoal-black Izaya-style zip parka with **fluffy silver-white fur trim** on collar, cuffs & bottom hem, dark trousers & boots (`Shiv_TS`, `Shiv_BS`, `VsTrainer122`, `Shiv_OW`, `ShivA..D`). | **Canonical Open-Arms (`F0-F3`) -> Iconic `VsTrainer122` Mocking Wave + Cool Hip Hand (`F6-F15`) + `F13` Blink** (`leg_lock=100.0%`, `foot_drift=0.0px`, `head_drift=0.0px`, `13` colors) |
| **`FESTIVAL_LIN`** / **`LIN`** | *Pokémon Reborn* (Meteor Champion Adult Avatar) | **Emerald-sage green hair** pulled up into a **high spiky windswept ponytail** with sweeping curtain bangs, **emerald-green eyes**, pale skin, dark charcoal fitted vest w/ silver trim over teal-sage tunic, split pleated teal overskirt over dark shorts, **metallic banded arm bracers & thigh bands**, tall teal boots (`Lin.png`, `VSLin.png`, `LinOverworld.png`). *(Corrects older placeholder note that assumed white hair / red-black attire!)* | **Chilling Stillness (`F0-F3`) -> Caitlin/Ghetsis-Grade Elevated Telekinetic Palm Command + Continuous Ponytail & Overskirt Breeze (`F6-F15`) + `F13` Blink** (`leg_lock=98.1%`, `foot_drift=0.0px`, `head_drift=0.0px`, `20` colors) |
| **`FESTIVAL_NOVA`** / **`NOVA`** | *Pokémon Desolation* (Team Crescent Leader) | **Long lush crimson-red hair tied into twin wavy pigtails** with a **single charcoal-black bow on her left pigtail**, crimson-red eyes, warm tan skin, **sleeveless black asymmetrical wrap shirt** (bare shoulders/arms), charcoal-grey pleated mini-skirt, black tights, **knee-high black boots with crimson-red front laces** (`Nova_TS`, `VsTrainer86`, `Nova_OW`, `NovaA..F`). *(Corrects older placeholder note that assumed pale indigo robes!)* | **Canonical Teasing Stance (`F0-F3`) -> Playful Raised Poké Ball Presentation (`F7` 1px specular glint) + Smooth Progressive-Shear Twin Pigtail Arc (`F6-F15`) + `F13` Blink** (`leg_lock=100.0%`, `foot_drift=0.0px`, `head_drift=0.0px`, `15` colors) |

---

## 2. QA Gate Summary (`54/54` Unique Assets / `108/108` Files PASS)

| Character | Front (`2560x160`) | Back (`800x160`) | VS (`256x136`) | Portraits (`96x96` x12) | OW (`128x192` x2) | Pose (`128x192`) | Hard Checks |
|---|---|---|---|---|---|---|---|
| **`SHIV`** | `13c`, `bot=156`, `lock=100.0%`, `foot=0.0px`, `head=0.0px` | `15c`, flush `y=160` | `15c`, flush `y=136` | `<=17c`, `alpha_diff=0`, `base==neutral` | `14c`, `bot=22`, `headDiff=0`, `L==mir(R)` | `14c`, `bot=22` | `exact2x=True`, `semi=0`, `orphans=0` |
| **`LIN`** | `20c`, `bot=156`, `lock=98.1%`, `foot=0.0px`, `head=0.0px` | `18c`, flush `y=160` | `18c`, flush `y=136` | `<=19c`, `alpha_diff=0`, `base==neutral` | `16c`, `bot=22`, `headDiff=0`, `L==mir(R)` | `16c`, `bot=22` | `exact2x=True`, `semi=0`, `orphans=0` |
| **`NOVA`** | `15c`, `bot=156`, `lock=100.0%`, `foot=0.0px`, `head=0.0px` | `14c`, flush `y=160` | `15c`, flush `y=136` | `<=16c`, `alpha_diff=0`, `base==neutral` | `12c`, `bot=22`, `headDiff=0`, `L==mir(R)` | `12c`, `bot=22` | `exact2x=True`, `semi=0`, `orphans=0` |

---

## 3. Drop-In Wiring Snippets (Verified Against Current Repo)

> `pbs/trainer_types.txt` ALREADY defines `[FESTIVAL_LIN]`, `[FESTIVAL_SHIV]`, and `[FESTIVAL_NOVA]` (lines 313-392). Only the 3 Ruby registry tables below need these drop-in additions:

### 3.1 `plugins/Prismfall Cutscenes/014_Portraits.rb` (`CAST`)
```ruby
      THEODRIC VENAM COLL
      SHIV LIN NOVA
```

### 3.2 `plugins/Prismfall EBDX Bridge/010_Bridge_VersusIntro.rb` (`TRAINER_TYPE_MAP` & `THEMES`)
```ruby
    # TRAINER_TYPE_MAP:
    :FESTIVAL_VENAM => "VENAM",
    :FESTIVAL_SHIV  => "SHIV",
    :FESTIVAL_LIN   => "LIN",
    :FESTIVAL_NOVA  => "NOVA"

    # THEMES:
    "THEODRIC" => :gold, "TEO" => :teal, "WICK" => :green, "MORWEN" => :violet, "DASK" => :grey, "VENAM" => :violet,
    "SHIV" => :grey, "LIN" => :green, "NOVA" => :red
```

### 3.3 `plugins/Prismfall Core/025_CharsetAliases.rb` (`NAME_ALIASES`)
```ruby
    "Aurelius" => "THEODRIC", "Theodric" => "THEODRIC",
    "Shiv" => "SHIV", "Lin" => "LIN", "Nova" => "NOVA"
```

---

## 4. Complete 54-Asset / 108-File SHA-256 Dual-Sync Manifest

Every single entry below is verified byte-identical (`SHA-256` match) in both `graphics/<path>` and `art/out/Graphics/<path>` (`54 x 2 = 108` files total):

| # | Asset Path (`graphics/` & `art/out/Graphics/`) | Size | Colors | SHA-256 (12) | Dual-Sync |
|---:|---|---|---:|---|---|
|  1 | `Trainers/FESTIVAL_SHIV.png` | `2560x160` | 13 | `f66287db5e95` | `graphics/` == `art/out/Graphics/` |
|  2 | `Trainers/FESTIVAL_SHIV_back.png` | `800x160` | 15 | `b755ab82a5ee` | `graphics/` == `art/out/Graphics/` |
|  3 | `EBDX/VS/SHIV.png` | `256x136` | 15 | `ec4be6da6062` | `graphics/` == `art/out/Graphics/` |
|  4 | `Portraits/SHIV.png` | `96x96` | 15 | `4e74fb6f524e` | `graphics/` == `art/out/Graphics/` |
|  5 | `Portraits/SHIV_neutral.png` | `96x96` | 15 | `4e74fb6f524e` | `graphics/` == `art/out/Graphics/` |
|  6 | `Portraits/SHIV_happy.png` | `96x96` | 14 | `cc402742b82d` | `graphics/` == `art/out/Graphics/` |
|  7 | `Portraits/SHIV_angry.png` | `96x96` | 15 | `dc668690fa06` | `graphics/` == `art/out/Graphics/` |
|  8 | `Portraits/SHIV_sad.png` | `96x96` | 15 | `2fe76b9c46bd` | `graphics/` == `art/out/Graphics/` |
|  9 | `Portraits/SHIV_surprised.png` | `96x96` | 14 | `6b5e359828c5` | `graphics/` == `art/out/Graphics/` |
| 10 | `Portraits/SHIV_smug.png` | `96x96` | 15 | `7b16297004fa` | `graphics/` == `art/out/Graphics/` |
| 11 | `Portraits/SHIV_shocked.png` | `96x96` | 14 | `e0595f10a62f` | `graphics/` == `art/out/Graphics/` |
| 12 | `Portraits/SHIV_panic.png` | `96x96` | 16 | `e225c29ae103` | `graphics/` == `art/out/Graphics/` |
| 13 | `Portraits/SHIV_blush.png` | `96x96` | 16 | `d949b785c095` | `graphics/` == `art/out/Graphics/` |
| 14 | `Portraits/SHIV_crying.png` | `96x96` | 17 | `3dfb9d9f9de0` | `graphics/` == `art/out/Graphics/` |
| 15 | `Portraits/SHIV_deadpan.png` | `96x96` | 15 | `d844bccdbbbb` | `graphics/` == `art/out/Graphics/` |
| 16 | `Characters/SHIV.png` | `128x192` | 14 | `655c9c4624f6` | `graphics/` == `art/out/Graphics/` |
| 17 | `Characters/trainer_FESTIVAL_SHIV.png` | `128x192` | 14 | `655c9c4624f6` | `graphics/` == `art/out/Graphics/` |
| 18 | `Characters/pose_SHIV.png` | `128x192` | 14 | `56101b3666a3` | `graphics/` == `art/out/Graphics/` |
| 19 | `Trainers/FESTIVAL_LIN.png` | `2560x160` | 20 | `630a89510212` | `graphics/` == `art/out/Graphics/` |
| 20 | `Trainers/FESTIVAL_LIN_back.png` | `800x160` | 18 | `90802b140f35` | `graphics/` == `art/out/Graphics/` |
| 21 | `EBDX/VS/LIN.png` | `256x136` | 18 | `b8c59430e5ef` | `graphics/` == `art/out/Graphics/` |
| 22 | `Portraits/LIN.png` | `96x96` | 18 | `0edafe73cf28` | `graphics/` == `art/out/Graphics/` |
| 23 | `Portraits/LIN_neutral.png` | `96x96` | 18 | `0edafe73cf28` | `graphics/` == `art/out/Graphics/` |
| 24 | `Portraits/LIN_happy.png` | `96x96` | 16 | `efe8473b4300` | `graphics/` == `art/out/Graphics/` |
| 25 | `Portraits/LIN_angry.png` | `96x96` | 18 | `b3289a1ea31d` | `graphics/` == `art/out/Graphics/` |
| 26 | `Portraits/LIN_sad.png` | `96x96` | 18 | `ed887f564225` | `graphics/` == `art/out/Graphics/` |
| 27 | `Portraits/LIN_surprised.png` | `96x96` | 17 | `9e36a70f0bc2` | `graphics/` == `art/out/Graphics/` |
| 28 | `Portraits/LIN_smug.png` | `96x96` | 18 | `1e6bc8898805` | `graphics/` == `art/out/Graphics/` |
| 29 | `Portraits/LIN_shocked.png` | `96x96` | 17 | `3ec183b2d50a` | `graphics/` == `art/out/Graphics/` |
| 30 | `Portraits/LIN_panic.png` | `96x96` | 18 | `415ffe13f489` | `graphics/` == `art/out/Graphics/` |
| 31 | `Portraits/LIN_blush.png` | `96x96` | 19 | `3240e3994226` | `graphics/` == `art/out/Graphics/` |
| 32 | `Portraits/LIN_crying.png` | `96x96` | 19 | `56d0ca791e35` | `graphics/` == `art/out/Graphics/` |
| 33 | `Portraits/LIN_deadpan.png` | `96x96` | 18 | `4d8c8d573770` | `graphics/` == `art/out/Graphics/` |
| 34 | `Characters/LIN.png` | `128x192` | 16 | `e42afb6986a0` | `graphics/` == `art/out/Graphics/` |
| 35 | `Characters/trainer_FESTIVAL_LIN.png` | `128x192` | 16 | `e42afb6986a0` | `graphics/` == `art/out/Graphics/` |
| 36 | `Characters/pose_LIN.png` | `128x192` | 16 | `9a658294d088` | `graphics/` == `art/out/Graphics/` |
| 37 | `Trainers/FESTIVAL_NOVA.png` | `2560x160` | 15 | `71f5d0c68e34` | `graphics/` == `art/out/Graphics/` |
| 38 | `Trainers/FESTIVAL_NOVA_back.png` | `800x160` | 14 | `78edc3502881` | `graphics/` == `art/out/Graphics/` |
| 39 | `EBDX/VS/NOVA.png` | `256x136` | 15 | `7b71466ee5a9` | `graphics/` == `art/out/Graphics/` |
| 40 | `Portraits/NOVA.png` | `96x96` | 15 | `c0685d70c2ed` | `graphics/` == `art/out/Graphics/` |
| 41 | `Portraits/NOVA_neutral.png` | `96x96` | 15 | `c0685d70c2ed` | `graphics/` == `art/out/Graphics/` |
| 42 | `Portraits/NOVA_happy.png` | `96x96` | 13 | `5683f86fd97e` | `graphics/` == `art/out/Graphics/` |
| 43 | `Portraits/NOVA_angry.png` | `96x96` | 15 | `b885cb0f8b82` | `graphics/` == `art/out/Graphics/` |
| 44 | `Portraits/NOVA_sad.png` | `96x96` | 14 | `c9de4426b568` | `graphics/` == `art/out/Graphics/` |
| 45 | `Portraits/NOVA_surprised.png` | `96x96` | 14 | `e538d529192f` | `graphics/` == `art/out/Graphics/` |
| 46 | `Portraits/NOVA_smug.png` | `96x96` | 14 | `0cd361fe4243` | `graphics/` == `art/out/Graphics/` |
| 47 | `Portraits/NOVA_shocked.png` | `96x96` | 14 | `648808fd8ff6` | `graphics/` == `art/out/Graphics/` |
| 48 | `Portraits/NOVA_panic.png` | `96x96` | 16 | `37d85a651a9c` | `graphics/` == `art/out/Graphics/` |
| 49 | `Portraits/NOVA_blush.png` | `96x96` | 16 | `492cd9efa9ab` | `graphics/` == `art/out/Graphics/` |
| 50 | `Portraits/NOVA_crying.png` | `96x96` | 16 | `6b2392b159d4` | `graphics/` == `art/out/Graphics/` |
| 51 | `Portraits/NOVA_deadpan.png` | `96x96` | 15 | `6cb890f911ab` | `graphics/` == `art/out/Graphics/` |
| 52 | `Characters/NOVA.png` | `128x192` | 12 | `eedb36d5c2ee` | `graphics/` == `art/out/Graphics/` |
| 53 | `Characters/trainer_FESTIVAL_NOVA.png` | `128x192` | 12 | `eedb36d5c2ee` | `graphics/` == `art/out/Graphics/` |
| 54 | `Characters/pose_NOVA.png` | `128x192` | 12 | `fc6dce6a243a` | `graphics/` == `art/out/Graphics/` |
