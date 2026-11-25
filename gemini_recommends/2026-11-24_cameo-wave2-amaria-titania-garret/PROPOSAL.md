# Cameo Pack Wave 2: Canonical Reborn Amaria & Titania + Desolation Garret (108 Dual-Synced Files)

**Date:** 2026-11-24  
**Scope:** `FESTIVAL_AMARIA` (*Pokémon Reborn*), `FESTIVAL_TITANIA` (*Pokémon Reborn*), and `FESTIVAL_GARRET` (*Pokémon Desolation*) — **54 unique pixel-art assets / 108 byte-identical dual-synced files** across `graphics/` and `art/out/Graphics/`.  
**Art Rule Compliance:** Strictly obeys **Reuben's Permanent Cameo Art Rule** — 100% faithful to each character's canonical original game art (*Pokémon Reborn* E19 / *Pokémon Desolation* Ep6), zero invented OC outfits, paired with custom restrained **Game Freak B2W2 16-frame battle animations** and **5-frame B/W back-throw strips**.

---

## 1. Canonical Design Verification (Original Game Art Fidelity)

Every sprite was anchored directly on the characters' verified official game sprites and official character art (no guesswork or OC redesigns):

| Cameo Slot | Source Game & Role | Canonical Visual Signatures Preserved 100% | Custom Restrained B2W2 16f Battle Animation |
|---|---|---|---|
| **`FESTIVAL_AMARIA`** (`AMARIA`) | *Pokémon Reborn* — Water Gym Leader (Fiore Mansion; Prismfall Ch17 Drowned Aurelia double battle, ace Lapras *Deliverer*) | Long wavy **seafoam-turquoise hair**, gentle teal eyes, **cobalt short-sleeve V-neck tunic + black midriff band**, dark charcoal leggings + **flowing royal-blue split side-panels**, azure cuffed boots, and iconic gleaming **Sapphire Bracelets**. | **Sapphire Bracelet & Gentle Tide Lift (`10` unique keys):** Anchored calm stance (`f0–f2`) -> graceful left-arm Poké Ball lift + ocean-current trailing hair sway (`f3–f8`) with crisp cyan-white Sapphire Bracelet (`f6`) & Poké Ball (`f7`) glints -> serene settle (`f9–f13`) -> gentle wistful blink (`f14`) -> poised ready hold (`f15`). |
| **`FESTIVAL_TITANIA`** (`TITANIA`) | *Pokémon Reborn* — Steel Gym Leader (Never After; Prismfall Ch17 Drowned Aurelia double battle, ace Aegislash) | Fiery **crimson-red long hair** with iconic **silver-white front bang streak**, piercing crimson eyes, **fitted white sleeveless tank top**, bare right arm on hip, **full articulated silver-steel knight armor LEFT arm & pauldron**, studded silver belt, **bold crimson trousers**, silver-steel combat boots. | **Steel Gauntlet Command & Metallic Glint Sweep (`10` unique keys):** Immovable knight stance (`f0–f2`) -> steel-armored left arm lifts decisively presenting Poké Ball (`f3–f9`) with a 3-beat white-silver specular steel sweep down **pauldron (`f6`) -> vambrace (`f7`) -> gauntlet/Ball (`f8`)** -> controlled guard return (`f10–f13`) -> sharp cold blink (`f14`) -> immovable guard hold (`f15`). |
| **`FESTIVAL_GARRET`** (`GARRET`) | *Pokémon Desolation* — Fighting Gym Leader (Cellia South; Prismfall Ch9 Ironreach shafts, ace Mega Lucario) | Weathered brown **wide-brimmed Lucario-ear cowboy hat** with black band & bronze crest, short shaggy **silver-white hair**, warm **dark bronze skin**, piercing **golden-amber eyes**, **ochre-tan duster jacket with thick charcoal-black fur collar**, lace-up dark brown shirt, **dark fingerless gloves**, dark brown trousers with right-thigh pouch, tan heeled boots. | **Cellia Fighter Poké Ball Toss & Catch (`8` unique keys):** Grounded brawler stance (`f0–f2`) -> `+1px` wrist anticipation dip (`f3`) -> crisp upward flick tossing Poké Ball (`f4–f7`) with **golden-amber apex glint (`f6`)** & subtle coat-tail sway -> clean cushioned catch (`f8–f9`) -> confident ready hold (`f10–f13`) -> stoic blink (`f14`) -> resolute battle hold (`f15`). |

---

## 2. Automated QA Gate Results (`108 / 108` Files PASS — `0` Failures)

| Cameo | Front 16f (`2560×160`) | Front Economy (`leg_lock / foot / head`) | Back 5f (`800×160`) | EBDX VS (`256×136`) | Portraits (`96×96` ×12) | Overworld (`128×192`) | Pose (`128×192`) |
|---|---|---|---|---|---|---|---|
| **`FESTIVAL_AMARIA`** | `21c`, `by=156`, `uniq=10`, `orphans=0` | `leg=97.1%` (mean `98.8%`), `ft=0.0px`, `hd=0.79px` | `21c`, `by=160`, `comps=[1, 1, 1, 2, 1]` | `19c`, `by=136`, `orphans=0` | `12/12` locked (`11/11` distinct, `max 16c`, `frameDiff=0`) | `15c`, `headDiff=0`, `col0==col2`, `L==mir(R)=0px`, `bot=22` | `17c`, `4/4` rows, `anchor=0px`, `bot=22` |
| **`FESTIVAL_TITANIA`** | `15c`, `by=156`, `uniq=10`, `orphans=0` | `leg=100.0%` (mean `100.0%`), `ft=0.0px`, `hd=0.13px` | `15c`, `by=160`, `comps=[1, 1, 1, 2, 1]` | `14c`, `by=136`, `orphans=0` | `12/12` locked (`11/11` distinct, `max 17c`, `frameDiff=0`) | `12c`, `headDiff=0`, `col0==col2`, `L==mir(R)=0px`, `bot=22` | `13c`, `4/4` rows, `anchor=0px`, `bot=22` |
| **`FESTIVAL_GARRET`** | `19c`, `by=156`, `uniq=8`, `orphans=0` | `leg=100.0%` (mean `100.0%`), `ft=0.0px`, `hd=0.91px` | `19c`, `by=160`, `comps=[1, 1, 1, 2, 1]` | `20c`, `by=136`, `orphans=0` | `12/12` locked (`11/11` distinct, `max 19c`, `frameDiff=0`) | `16c`, `headDiff=0`, `col0==col2`, `L==mir(R)=0px`, `bot=22` | `16c`, `4/4` rows, `anchor=0px`, `bot=22` |

Global invariants verified across **all 54 unique assets / 108 dual-synced files**:
- `exact2x == True` (100% pure `2×2` nearest-neighbor pixel blocks)
- `semi == 0` (alpha strictly `0` or `255`)
- `orphans == 0` (`0` isolated noise specks; `1` single connected component per cell across all 16 OW cells and all 16 Pose cells)
- `colors <= 24` on every single file (range: `12–21` curated B2W2 colors)
- `Portraits/<NAME>.png == Portraits/<NAME>_neutral.png` (byte-identical)
- `Characters/<NAME>.png == Characters/trainer_FESTIVAL_<NAME>.png` (byte-identical)
- `graphics/<rel> == art/out/Graphics/<rel>` (byte-identical SHA-256 across all 54 pairs = 108 files)

---

## 3. Drop-In Wiring Hooks (Non-Destructive)

`pbs/trainer_types.txt` **already defines** `[FESTIVAL_AMARIA]`, `[FESTIVAL_TITANIA]`, and `[FESTIVAL_GARRET]` (lines 323–384). Drop the following small additions into the three Prismfall Ruby plugins when enabling their cutscenes and EBDX VS cut-ins:

### A. `plugins/Prismfall Cutscenes/014_Portraits.rb` (`CAST` whitelist)
```ruby
# Append to Prismfall::Portraits::CAST:
AMARIA TITANIA GARRET
```

### B. `plugins/Prismfall EBDX Bridge/010_Bridge_VersusIntro.rb` (`TRAINER_TO_CAST` & `THEMES`)
```ruby
# Add to TRAINER_TO_CAST:
:FESTIVAL_AMARIA  => "AMARIA",
:FESTIVAL_TITANIA => "TITANIA",
:FESTIVAL_GARRET  => "GARRET",

# Add to THEMES:
"AMARIA"  => :teal,
"TITANIA" => :red,
"GARRET"  => :gold,
```

### C. `plugins/Prismfall Core/025_CharsetAliases.rb` (`NAME_ALIASES`)
```ruby
# Add to Prismfall::NAME_ALIASES:
"Amaria" => "AMARIA", "Titania" => "TITANIA", "Garret" => "GARRET",
```

---

## 4. Visual Proofs & Interactive Review Studio

- **Proof Sheet (Official Refs vs Restored 18-Asset Packs):** `140_cameos_wave2_amaria_titania_garret_proof.png` (saved in parent artifact preview dir)
- **Interactive Animated Cameo Studio:** `/tmp/prismfall_cameos_wave2_studio.html` (live 16f battle player, 5f back-throw player, EBDX VS banner preview, interactive 12-expression dialogue box, live 4-direction OW walker & 4-pose viewer, `< 2 MB`, Playwright-verified `0` errors)

---

## 5. Full Dual-Synced SHA-256 Manifest (54 Pairs = 108 Files)

Every entry below is byte-identical in both `graphics/<path>` and `art/out/Graphics/<path>`:

| # | Relative Asset Path | Bytes | SHA-256 (Synced Pair) |
|---:|---|---:|---|
| 1 | `Characters/AMARIA.png` | 3234 | `85b944b95aa5bb9c969b2d09804b2f6715bd5fc9a84418c1afec8977eecfaba4` |
| 2 | `Characters/GARRET.png` | 3402 | `56bcb7ca6ae393b04f2e0df3d1066519910c4c20e3e83876e8aad8de793539b8` |
| 3 | `Characters/TITANIA.png` | 2953 | `cd1b1100abb218f579e52bbdb46cb4d953e8b624e136fce9f3b4378d8ff28ddf` |
| 4 | `Characters/pose_AMARIA.png` | 2122 | `3a211f264e4d5167879313b3ee78bd442fc3905f6a7d396724bdb1c88086585e` |
| 5 | `Characters/pose_GARRET.png` | 2333 | `96eaca88ab9530bd3a9fc4e28e1ff823babdf90d94c942c40f902516c63e8cd7` |
| 6 | `Characters/pose_TITANIA.png` | 1980 | `2812819e73639ecefd01e7b14795a793939c0f76f937ce922f0ef41c8c228f8e` |
| 7 | `Characters/trainer_FESTIVAL_AMARIA.png` | 3234 | `85b944b95aa5bb9c969b2d09804b2f6715bd5fc9a84418c1afec8977eecfaba4` |
| 8 | `Characters/trainer_FESTIVAL_GARRET.png` | 3402 | `56bcb7ca6ae393b04f2e0df3d1066519910c4c20e3e83876e8aad8de793539b8` |
| 9 | `Characters/trainer_FESTIVAL_TITANIA.png` | 2953 | `cd1b1100abb218f579e52bbdb46cb4d953e8b624e136fce9f3b4378d8ff28ddf` |
| 10 | `EBDX/VS/AMARIA.png` | 3541 | `1978761527658c9388364c04ecf465d549627edd5873dffc4d8dc4719f906587` |
| 11 | `EBDX/VS/GARRET.png` | 3962 | `393a4e3295274e5219b4a88644b09fc265efdec03c04babd6a89d0f89d22d30f` |
| 12 | `EBDX/VS/TITANIA.png` | 3554 | `5255f742e7e31a1b292518aae8ecb932f5d5082581e4abc02a59e873f3b0a636` |
| 13 | `Portraits/AMARIA.png` | 1931 | `702e5ffc5bb9caaabee3e894b4f4c71bcc3f10d7bb6bc89c8a900cd36948d91c` |
| 14 | `Portraits/AMARIA_angry.png` | 1970 | `7fadaacad5d46ef659ef45377a747b0bf0e45f37fbe15682da023a46885d63af` |
| 15 | `Portraits/AMARIA_blush.png` | 2008 | `17fb0b42ef0e564860c77ed3b4b4713ff90343c37f2337db573c68db0a6b6a66` |
| 16 | `Portraits/AMARIA_crying.png` | 2044 | `4cf3f293355b78d13f5e0e0f2d30d73de7a34c373032315621b35083939b054c` |
| 17 | `Portraits/AMARIA_deadpan.png` | 1868 | `06bcf97643cc63a8fa5a73723a7a2d2ded2d0ff876cf0039c47b0ac59ee7584c` |
| 18 | `Portraits/AMARIA_happy.png` | 1877 | `b65c4f366c277a6f2240053efa98e2ed92aba68897d6b16b90a93b8690307e17` |
| 19 | `Portraits/AMARIA_neutral.png` | 1931 | `702e5ffc5bb9caaabee3e894b4f4c71bcc3f10d7bb6bc89c8a900cd36948d91c` |
| 20 | `Portraits/AMARIA_panic.png` | 1923 | `24147b9ccd1fe8cc4034c6266ecdfe367b4e4361de387ac85c68fcb35bf3341b` |
| 21 | `Portraits/AMARIA_sad.png` | 1926 | `58719363c877e94d1c8d25eff110b852e6f31939e660c60781ffcc3be1e87cce` |
| 22 | `Portraits/AMARIA_shocked.png` | 1879 | `c35fc97227403892ae3384e16364b6162123e154fbd63bae12b22442cbd3ac75` |
| 23 | `Portraits/AMARIA_smug.png` | 1868 | `ce9b29ae3608760af3c569769fa70c829fdeca6c552c0c8aad2203ebe3f2ded1` |
| 24 | `Portraits/AMARIA_surprised.png` | 1978 | `adf7945de1b938525a570f1b4f58c7e9c80830dca4051f3476188474eb80cd3d` |
| 25 | `Portraits/GARRET.png` | 2033 | `deaeb6c5605b1e693eb07f4d9ca1f0cc2ff445525a5f05180057da791859eb29` |
| 26 | `Portraits/GARRET_angry.png` | 2079 | `82c3dbbc5104abf93eee942a968873021a65d9cfb800860c8a21561c09016415` |
| 27 | `Portraits/GARRET_blush.png` | 2097 | `5df93d266fe3e6ad202edfa3610e3da8b8c8dc171b345ab7d8f45045954581db` |
| 28 | `Portraits/GARRET_crying.png` | 2091 | `05367095940c74244e5776150722504882afd5540aaa186bf1da8da9436f6a94` |
| 29 | `Portraits/GARRET_deadpan.png` | 1980 | `800d02bde43a8c6d8078063b8bed3545a7d7ac8abeaf09dfe64d2421d6fe3b1c` |
| 30 | `Portraits/GARRET_happy.png` | 2059 | `c6f5eb04f6552d2481f6b996b961df9351fc45a3aff1b9a7a435368134ca1f18` |
| 31 | `Portraits/GARRET_neutral.png` | 2033 | `deaeb6c5605b1e693eb07f4d9ca1f0cc2ff445525a5f05180057da791859eb29` |
| 32 | `Portraits/GARRET_panic.png` | 2040 | `168d22e3423fd60775a91226ff68dd702698a1da5e53263869cc2db0c56ac075` |
| 33 | `Portraits/GARRET_sad.png` | 2055 | `30a7ee809fc0c4c9f019fdd32180bc555027a024453f6dc1a60a394df1f25ef3` |
| 34 | `Portraits/GARRET_shocked.png` | 1998 | `c9f7b67258b1730c3893e03404f7ee1a78cc411238d7b0131f9237ca27b547a0` |
| 35 | `Portraits/GARRET_smug.png` | 2065 | `5432dc8d876b14ce35a5851b30bd2f594b4bdf2f996ab2171755024dbb2009e1` |
| 36 | `Portraits/GARRET_surprised.png` | 2054 | `1dd1e84e69ebb2770c80bb23a4e0e0681affdc561f0d90b9b579f3ba3ed11b7a` |
| 37 | `Portraits/TITANIA.png` | 2280 | `e0db7c62c6f795d7dd3b33b4799e088bbe1865734b09567373b2f30d84138405` |
| 38 | `Portraits/TITANIA_angry.png` | 2310 | `9189c0221ac09efdabf5a7fa7b901a92a6b42bedda6e8db001788fea53a3833c` |
| 39 | `Portraits/TITANIA_blush.png` | 2343 | `84f8b50fd047deadaa550021cc457b09fe271c81094afc5b61798b1911d30da1` |
| 40 | `Portraits/TITANIA_crying.png` | 2405 | `b6d07deab858f2f3a3b0a245bb4edd1ecf13ea71694bb2d0fe4331d90d90fbc7` |
| 41 | `Portraits/TITANIA_deadpan.png` | 2222 | `2a144a290e70170921eee17ef9abad7866b22a5d576a2aa6cb026c022085664d` |
| 42 | `Portraits/TITANIA_happy.png` | 2283 | `274b15b70cfca596a6b4bf62e697083ae529f68d5f3f605f7dd4368ec33f658c` |
| 43 | `Portraits/TITANIA_neutral.png` | 2280 | `e0db7c62c6f795d7dd3b33b4799e088bbe1865734b09567373b2f30d84138405` |
| 44 | `Portraits/TITANIA_panic.png` | 2298 | `e79601ad9e4f9c025bc7f8b3e789569f90ee63198ab851a96034f2905aa3acd4` |
| 45 | `Portraits/TITANIA_sad.png` | 2222 | `5a5c124127470b8a2dd57067a589ebec84b1a3da27374ba39103cc4e3ea40d73` |
| 46 | `Portraits/TITANIA_shocked.png` | 2231 | `8778e283863ee28bae7abf8d27e89038c130657651de6c3a058d4c7183e1c8b5` |
| 47 | `Portraits/TITANIA_smug.png` | 2214 | `fdf03ada0b191f0286fe922ee4a38cf967316b40a1e86b35d92314c7d0c32119` |
| 48 | `Portraits/TITANIA_surprised.png` | 2299 | `92387231995463c16d5b82b234458bde95629e455bdf56471fbf156f0c6df408` |
| 49 | `Trainers/FESTIVAL_AMARIA.png` | 10018 | `8dc7ebe14374de32141abebbe7d19487997ab18e9a04dd6896dc401e5d0cc255` |
| 50 | `Trainers/FESTIVAL_AMARIA_back.png` | 6148 | `e6fb994fe09bd35374467fbf521f43af1f9d37d5fc7e6ac59aaed3352fa1d934` |
| 51 | `Trainers/FESTIVAL_GARRET.png` | 8276 | `650e9a5c4b3998861f873215495d630078b4ae649359d4879aa2efa6a559c76d` |
| 52 | `Trainers/FESTIVAL_GARRET_back.png` | 6112 | `9df0b2582ce42eea93b956323baf7418e81fbb869e8b1810368444a85e7efb80` |
| 53 | `Trainers/FESTIVAL_TITANIA.png` | 8546 | `0083b911f0a110202bdff8845276320de5497247def07aaa5a14836f3aae47c8` |
| 54 | `Trainers/FESTIVAL_TITANIA_back.png` | 5966 | `4bde57c41b89b158cf7e2f06668bdfc03ba880561876c5eaf481d5f35b4b97ca` |
