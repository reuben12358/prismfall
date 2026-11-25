# Canonical Cameo Pack Wave 1 — Shelly (*Reborn*), Melia (*Rejuvenation*), & Alexandra (*Rejuvenation*)

- **Date:** 2026-11-24
- **Author:** Gemini (Canonical Cameo Sprite & Animation Specialist)
- **Governing Policy:** **Reuben's Permanent Cameo Art Rule** (*100% strictly faithful to canonical original Pokémon Reborn / Pokémon Rejuvenation home-game art — zero OC redesigns — paired with custom restrained B2W2 16-frame battle animations suiting each character*, matching the `VENAM` gold standard).
- **Visual Proof Sheet:** `previews/127_cameos_wave1_shelly_melia_alexandra_proof.png` (saved in artifact previews directory; 3-band side-by-side Official Home-Game Reference vs Restored 18-Asset Prismfall Pack).
- **Live Interactive Studio:** `/tmp/prismfall_cameos_wave1_studio.html` (Playwright-verified, `0` errors).
- **Deployment Scope:** **54 unique asset pairs = 108 dual-synced files** (`graphics/` ≡ `art/out/Graphics/`, 100% SHA-256 byte-identical, `108/108` QA Gate PASS).

---

## 1. Canonical Home-Game Design Verification (Zero OC Drift!)

Every single character was anchored directly against authentic official *Pokémon Reborn* (E19) and *Pokémon Rejuvenation* (V13.5) sprites and official character art before a single pixel was finalized:

### A. Shelly — `FESTIVAL_SHELLY` / `SHELLY` (*Pokémon Reborn*, Bug Gym Leader / Champion)
- **Cameo Slot:** [`design/CAMEOS.md`](../../design/CAMEOS.md) #1 — *"Lost in the Gossamer"* (Act I / Ch3, Elowen — Gossamer Deepwood, `:SILKWOOD`, double battle lv ~21 / post-game v2 lv 100).
- **Canonical Visual Anchor (Official Reborn E19 `Shelly.png` & `charshelly.png`):**
  - **Hair:** Pastel orchid-lavender-pink (`#D876F6` / `#A856DA`) messy shaggy bob sweeping across her right eye, with her iconic thick side-braid/ponytail hanging down her left side clasped with a dark metallic charcoal ring (`#424452`).
  - **Eyes & Expression:** Soft, earnest **violet** visible left eye, gentle timid bookworm demeanor (no glasses in E19 canon).
  - **Outfit:** Pastel sage/leaf-green short-sleeved collared shirt-dress (`#84B672`) with crisp white Peter-Pan collar & white chest ruffle bow, pleated green skirt with dark forest-green stripe detail, white thigh-high/knee-high socks, and purple laced strap shoes.
- **Custom Restrained B2W2 16-Frame Battle Animation (`Trainers/FESTIVAL_SHELLY.png`):**
  - Anchored shy ready stance (`f0–f2`, `f4`, `f12–f13`, `f15`) with natural 1-frame gentle eye blink (`f3`, `f14`), timidly raising her Poké Ball forward (`f5` Mid → `f6–f10` Peak with soft braid sway and bright Poké Ball sparkle glint on `f7–f8`, smooth return on `f11`).
  - **Metrics:** `21` colors, `by=156` all 16f, `leg_lock=90.1%`, `foot_drift=0.00px`, `head_drift=0.03px`.

### B. Melia — `FESTIVAL_MELIA` / `MELIA` (*Pokémon Rejuvenation*, Reserve Normal Leader)
- **Cameo Slot:** [`design/CAMEOS.md`](../../design/CAMEOS.md) #4 — *"What Are You For?"* (Act III / Ch10, Elowen — Royal Chase, lv ~50 w/ Ace **Hapi** the Togekiss / post-game v2 lv 100; cross-references Venam's quest).
- **Canonical Visual Anchor (Official Rejuvenation V13.5 GDC Key Art & Sprites):**
  - **Hair:** Warm **golden-honey blonde** (`#E0A65C` / `#FAD68A`) layered bob with side-swept bangs and a low side-ponytail tied with her signature **crimson-red ribbon** (`#CC283A`).
  - **Eyes & Expression:** Bright **slate-blue/grey-blue** (`#4A5C76` / `#8098B6`) eyes and warm determined heroine smile.
  - **Outfit:** Crisp **white button-up collared blouse** with rolled sleeves, **dark charcoal suspenders**, high-waisted dark charcoal corset-pleated mini-skirt adorned with two vertical rows of **crimson-red buttons**, opaque dark charcoal tights, and espresso-brown Mary Jane strap shoes.
- **Custom Restrained B2W2 16-Frame Battle Animation (`Trainers/FESTIVAL_MELIA.png`):**
  - Confident ready stance holding Poké Ball low (`f0–f2`, `f4`, `f12–f13`, `f15`) with crisp 1-frame blink (`f3`, `f14`), swinging her Poké Ball out with left hand planted on hip (`f5` Mid) and raising it high in a bright challenge (`f6–f10` Peak with Poké Ball specular sparkle on `f7–f8`, smooth return `f11`).
  - **Metrics:** `23` colors, `by=156` all 16f, `leg_lock=99.1%`, `foot_drift=0.00px`, `head_drift=0.47px`.

### C. Alexandra — `FESTIVAL_ALEXANDRA` / `ALEXANDRA` (*Pokémon Rejuvenation*, Elite 8 Acting Champion)
- **Cameo Slot:** [`design/CAMEOS.md`](../../design/CAMEOS.md) #5 — *"Crystal Sleep"* (Act III / Ch11, Isenmar — Rimeholt's sunken lower town after the Thaw, lv ~56 Dragon/Psychic Champion team w/ Ace **Latias** / post-game v2 lv 100).
- **CRITICAL CANON CORRECTION (Verified Directly Against Official `pokemonrejuvenation.com` V13.5 `Alexandra.png`):**
  - Earlier informal notes briefly guessed Alexandra was "blonde / silver-haired in white-gold". Per **Reuben's Permanent Cameo Art Rule**, direct inspection of official *Pokémon Rejuvenation* V13.5 artwork (`official_rejuv_10_Alexandra.png`, `official_rejuv_11_Alexandra.png`, `official_rejuv_17_Alexandra.png`) confirms **true canonical Alexandra** has:
    - **Skin:** Rich, luminous **warm deep chestnut-brown skin** (`#A06C52` / `#C28C6E` highlight / `#583428` shadow).
    - **Hair:** Very long, voluminous, layered **dark charcoal-black hair** (`#383644` / `#525062` / `#706E82` sheen) flaring into dramatic points behind her waist.
    - **Eyes & Pose:** Bright **amethyst-purple eyes** (`#502C86` / `#A26CE0` / `#D4AEFC`) and her signature composed **right-finger-on-chin thinking pose**.
    - **Outfit:** Dark plum-charcoal jagged-hem tailored open coat (`#503E6A`) lined in **vivid royal amethyst purple** (`#7A46BE`) with spiky pale-lavender cuff trim (`#D4AEFC`), dark charcoal inner tunic with double pale-lavender V-collar & waist stripes, sleek charcoal-black leggings, and royal-purple cuffed mid-calf boots with pale-lavender cuffs.
- **Custom Restrained B2W2 16-Frame Battle Animation (`Trainers/FESTIVAL_ALEXANDRA.png`):**
  - Regal composed chin-thinking ready pose (`f0–f2`, `f4`, `f12–f13`, `f15`) with serene 1-frame blink (`f3`, `f14`), smoothly unfurling her right arm to present her Poké Ball palm-up (`f5` Mid → `f6–f10` Peak with subtle coat poise & Poké Ball sparkle glint on `f7–f8`, smooth return `f11`).
  - **Metrics:** `19` colors, `by=156` all 16f, `leg_lock=74.5%`, `foot_drift=0.00px`, `head_drift=0.69px`.

---

## 2. QA Gate Scorecard (`108 / 108` Files PASS)

| Cameo | Battle 16f (`2560×160`) | Back 5f (`800×160`) | EBDX VS (`256×136`) | Portraits × 12 (`96×96`) | Overworld × 2 (`128×192`) | Pose (`128×192`) |
|---|---|---|---|---|---|---|
| **SHELLY** | `21c` · `by=156` · `lock=90.1%` · `foot=0.00px` · `head=0.03px` | `17c` · `by=160` | `21c` · `by=136` | `12/12` · `16–18c` · `base==neutral` | `16c` · `bot=22` · `headDiff=0` · `L==mR` | `19c` · `bot=22` |
| **MELIA** | `23c` · `by=156` · `lock=99.1%` · `foot=0.00px` · `head=0.47px` | `22c` · `by=160` | `22c` · `by=136` | `12/12` · `17–19c` · `base==neutral` | `17c` · `bot=22` · `headDiff=0` · `L==mR` | `17c` · `bot=22` |
| **ALEXANDRA** | `19c` · `by=156` · `lock=74.5%` · `foot=0.00px` · `head=0.69px` | `17c` · `by=160` | `13c` · `by=136` | `12/12` · `14–16c` · `base==neutral` | `15c` · `bot=22` · `headDiff=0` · `L==mR` | `17c` · `bot=22` |

- **Universal Invariants Verified Across All 108 Deployed Files:** `exact2x = True (108/108)`, `semi_alpha = 0 (108/108)`, `orphans = 0 (108/108)`, `colors <= 24 (108/108)`, `graphics/ == art/out/Graphics/` 100% SHA-256 byte-identical (`54/54` pairs), `Portraits/<NAME>.png == Portraits/<NAME>_neutral.png` (`3/3`), `Characters/<NAME>.png == Characters/trainer_FESTIVAL_<NAME>.png` (`3/3`), Overworld `col0 == col2` (`0px` diff), `Left == mirror(Right)` (`0px` diff), `headDiff = 0`, locked ground baseline `bot = 22` (`bottom_y = 45`, unified with all 55 main-cast overworld sheets!).

---

## 3. Drop-In Wiring Snippets (For Claude's Wiring Sprint)

`pbs/trainer_types.txt` **already registers** `[FESTIVAL_SHELLY]` (line 331), `[FESTIVAL_ALEXANDRA]` (line 339), and `[FESTIVAL_MELIA]` (line 371), and `plugins/Prismfall Core/012_Narrative_Data.rb` already maps all three display names! Only **3 tiny Ruby hooks** are needed to light up their portraits, EBDX VS cut-ins, and overworld event aliases:

### 1. `plugins/Prismfall Cutscenes/014_Portraits.rb` (`CAST` array, ~line 96)
```ruby
      THEODRIC VENAM COLL
      SHELLY MELIA ALEXANDRA
```

### 2. `plugins/Prismfall EBDX Bridge/010_Bridge_VersusIntro.rb` (`VS_IDS` & `THEMES`, ~lines 54 & 69)
```ruby
    # In VS_IDS:
    :FESTIVAL_SHELLY    => "SHELLY",
    :FESTIVAL_MELIA     => "MELIA",
    :FESTIVAL_ALEXANDRA => "ALEXANDRA",

    # In THEMES:
    "SHELLY" => :green, "MELIA" => :gold, "ALEXANDRA" => :violet,
```

### 3. `plugins/Prismfall Core/025_CharsetAliases.rb` (`NAME_ALIASES`, ~line 33)
```ruby
    "Shelly" => "SHELLY", "Melia" => "MELIA", "Alexandra" => "ALEXANDRA",
```

---

## 4. Complete 108-File Dual-Sync SHA-256 Manifest (`graphics/` ≡ `art/out/Graphics/`)

Every file listed below has been dual-synced and verified **100% byte-identical** across `graphics/<path>` and `art/out/Graphics/<path>`.

### A. Shelly (`FESTIVAL_SHELLY` / `SHELLY` — 18 Unique Assets · 36 Files)

| Relative Path (under `graphics/` & `art/out/Graphics/`) | Size | Colors | Bytes | Full SHA-256 (Dual-Synced Exact) |
|---|---:|---:|---:|---|
| `Trainers/FESTIVAL_SHELLY.png` | `2560×160` | 21 | 9,392 | `30e12162bc33d16489e24bfce62e8c3e37d4cb58de0c57187171f68178c7727f` |
| `Trainers/FESTIVAL_SHELLY_back.png` | `800×160` | 17 | 7,610 | `b403c5022e374908b92398ce7906b327a64b8db0405d63e74cdc690bee10e01c` |
| `EBDX/VS/SHELLY.png` | `256×136` | 21 | 3,852 | `7c19886f36277af3b6011f6c1bb31a6c1621806d8ebb8cd901a44fb031327bfd` |
| `Portraits/SHELLY.png` | `96×96` | 16 | 1,916 | `de7315a34b86352bc0c82cd0210ed38d98e5c8679e2bd31c9862fc9dc822a98c` |
| `Portraits/SHELLY_neutral.png` | `96×96` | 16 | 1,916 | `de7315a34b86352bc0c82cd0210ed38d98e5c8679e2bd31c9862fc9dc822a98c` |
| `Portraits/SHELLY_happy.png` | `96×96` | 18 | 1,927 | `f453bf86fe62b1596088250d74c5d16b9e7610304b0939eca814a13f92ed4816` |
| `Portraits/SHELLY_angry.png` | `96×96` | 16 | 1,951 | `1ae729527f075534d5f062b85e5272adddc3f0da3d4fa6fb305071cd4dfb0206` |
| `Portraits/SHELLY_sad.png` | `96×96` | 18 | 1,953 | `9c3c5b2b8162d10e249604b99a18d4d4a64012dcd774ff871ffa9d2cfdf08ced` |
| `Portraits/SHELLY_surprised.png` | `96×96` | 17 | 1,907 | `76c98fc46bf8a69654740b3eb931aac0f85c419e5b3f57f7801576bb1dc6ae41` |
| `Portraits/SHELLY_smug.png` | `96×96` | 16 | 1,916 | `2848248fa79b441be0adf3375d3f0267c660bde54dd582ce1ddef8f1638699a5` |
| `Portraits/SHELLY_shocked.png` | `96×96` | 17 | 1,890 | `39c77e23b68ce6056f486e7e56d00e59351cd613f8227090440c555b7d00333c` |
| `Portraits/SHELLY_panic.png` | `96×96` | 18 | 1,890 | `61afe87b6508bc91ec7eb093f8e2062f62c6bdd9f69a7d299e067fcb33a6cae9` |
| `Portraits/SHELLY_blush.png` | `96×96` | 17 | 1,923 | `305adbe572695a6de2282d8f0d57e6a20fb49ac67278571a9958d8ca6fa26b88` |
| `Portraits/SHELLY_crying.png` | `96×96` | 18 | 1,968 | `efd9fa7a83dbfb6d7c3081cb6888fbad83e7b8658d4a0079173f7c6016703288` |
| `Portraits/SHELLY_deadpan.png` | `96×96` | 16 | 1,897 | `a7d9fb0391255c174267745f947017a31bc49892f581bdcd3c91eaf2fc2c5a55` |
| `Characters/SHELLY.png` | `128×192` | 16 | 3,003 | `df268fa47d62ae7d01ed6344bbda1a7d9c8efe085f2433c3d582eba803316eb6` |
| `Characters/trainer_FESTIVAL_SHELLY.png` | `128×192` | 16 | 3,003 | `df268fa47d62ae7d01ed6344bbda1a7d9c8efe085f2433c3d582eba803316eb6` |
| `Characters/pose_SHELLY.png` | `128×192` | 19 | 2,131 | `c550b7f07a69f2170474bd659ac658cd8bdb1d4afae738ca38bfa89a9b1966cf` |

### B. Melia (`FESTIVAL_MELIA` / `MELIA` — 18 Unique Assets · 36 Files)

| Relative Path (under `graphics/` & `art/out/Graphics/`) | Size | Colors | Bytes | Full SHA-256 (Dual-Synced Exact) |
|---|---:|---:|---:|---|
| `Trainers/FESTIVAL_MELIA.png` | `2560×160` | 23 | 10,711 | `e7576585145f1e27ee31a8f85824d2aabc992424997db2e06aeb01a1406bd4e6` |
| `Trainers/FESTIVAL_MELIA_back.png` | `800×160` | 22 | 8,687 | `630ea3d62be97089aaf3523a9ec3622503f04d2992311fad2f919228a644f5ac` |
| `EBDX/VS/MELIA.png` | `256×136` | 22 | 3,482 | `3611fe4ef59f61d5201051e32cc43ee6e742e6c3f8d70a115276f42c7d1fb9e4` |
| `Portraits/MELIA.png` | `96×96` | 17 | 1,582 | `8e83bf36d2e99213e598fadfaafc68dc9302f05681cdb9c7259ac16c48cc6932` |
| `Portraits/MELIA_neutral.png` | `96×96` | 17 | 1,582 | `8e83bf36d2e99213e598fadfaafc68dc9302f05681cdb9c7259ac16c48cc6932` |
| `Portraits/MELIA_happy.png` | `96×96` | 17 | 1,562 | `d0ba78487552325f36f0c903dbf156b9baec795a910bcad0827832c6a5c0c7d4` |
| `Portraits/MELIA_angry.png` | `96×96` | 18 | 1,583 | `c323b65be165881b1f70bfa08925e32714c07fe7cade42cd4953dfbc281dd809` |
| `Portraits/MELIA_sad.png` | `96×96` | 19 | 1,576 | `bfa04490fd895d3fdaf00b63c727532f53b652816d01c8e17ae64575d5525603` |
| `Portraits/MELIA_surprised.png` | `96×96` | 19 | 1,583 | `869208c96414d65c9ed12dc44901e610dea94ed219e72f16d2c59cf199cdf5d8` |
| `Portraits/MELIA_smug.png` | `96×96` | 17 | 1,591 | `0331619ccf8b35070354dd166d58e6e3f5a88a770d88386a715ddaa6455a4cf8` |
| `Portraits/MELIA_shocked.png` | `96×96` | 17 | 1,553 | `d4749993f95d9f5cfe1e61043cf98adeb29c0d7b26a8ffdb19b7b027f17e94b4` |
| `Portraits/MELIA_panic.png` | `96×96` | 17 | 1,559 | `f55409a4fee91870bd7945141cb5d87e67b513db07f10cd73c422b482691de0a` |
| `Portraits/MELIA_blush.png` | `96×96` | 18 | 1,599 | `8d802f08995ba27601db139d78814c3012852b42059e38402026d872de3b2681` |
| `Portraits/MELIA_crying.png` | `96×96` | 19 | 1,628 | `06732803596be6c4409a6b67e2683a2f39fe869fd54d06fb7f49d3b2595712c9` |
| `Portraits/MELIA_deadpan.png` | `96×96` | 17 | 1,544 | `6c0b901343bcca90095964399da63143fbe5e2819305b036f4416a88a5129de3` |
| `Characters/MELIA.png` | `128×192` | 17 | 3,046 | `68c6a4db4df97f947cffdc13684d3d3e28fc7d6e5086cdb83182efa769875c06` |
| `Characters/trainer_FESTIVAL_MELIA.png` | `128×192` | 17 | 3,046 | `68c6a4db4df97f947cffdc13684d3d3e28fc7d6e5086cdb83182efa769875c06` |
| `Characters/pose_MELIA.png` | `128×192` | 17 | 2,005 | `7c1cbc2486212da7e9d5ca256905472d3e71a8ae5b939b97c5f1fc6d289735ae` |

### C. Alexandra (`FESTIVAL_ALEXANDRA` / `ALEXANDRA` — 18 Unique Assets · 36 Files)

| Relative Path (under `graphics/` & `art/out/Graphics/`) | Size | Colors | Bytes | Full SHA-256 (Dual-Synced Exact) |
|---|---:|---:|---:|---|
| `Trainers/FESTIVAL_ALEXANDRA.png` | `2560×160` | 19 | 10,401 | `2a4d81192055588327b19a4ee32b84e15d202ed3f52992b1a33d04628bcd7c90` |
| `Trainers/FESTIVAL_ALEXANDRA_back.png` | `800×160` | 17 | 6,762 | `c6ab683055a76569f68dab46016e40b84a57d395cea5dc59f02585a3e7a14564` |
| `EBDX/VS/ALEXANDRA.png` | `256×136` | 13 | 2,748 | `448cb4409f8b8ac487fa076f05e1bfad2beea73e7c9f219689cb3b54f337ffad` |
| `Portraits/ALEXANDRA.png` | `96×96` | 14 | 1,594 | `5ca9d5bdd6b744fc67895297a1333b57290b55fa4a5647711a1483628ef2dcc4` |
| `Portraits/ALEXANDRA_neutral.png` | `96×96` | 14 | 1,594 | `5ca9d5bdd6b744fc67895297a1333b57290b55fa4a5647711a1483628ef2dcc4` |
| `Portraits/ALEXANDRA_happy.png` | `96×96` | 14 | 1,610 | `ea92bb8d95f3f6c1247a5bcbe6b3e55e8c4cf050a9a66ef4edd68e80fccbefbd` |
| `Portraits/ALEXANDRA_angry.png` | `96×96` | 15 | 1,627 | `7234b244404327c492719169d79c80ed4b0a1fa4f92eeda6180e737070c6b03d` |
| `Portraits/ALEXANDRA_sad.png` | `96×96` | 15 | 1,601 | `868e75ad06f73df4ede250ac5355cb75a8e6c938f4d1fac6d2b9006e9a052bf4` |
| `Portraits/ALEXANDRA_surprised.png` | `96×96` | 16 | 1,585 | `aa7df2bdd5e2c9bfc88113d54b3412cee7d4cdd2bfbaf520f8f99c32ae3b2629` |
| `Portraits/ALEXANDRA_smug.png` | `96×96` | 14 | 1,610 | `08dbf315e4453170694d05cd478ca0e112c592feef9df276d9fadf54a003e2a1` |
| `Portraits/ALEXANDRA_shocked.png` | `96×96` | 14 | 1,571 | `843b9846e42c7905ed3a25ed6bf976a9e2797f6b1f1c7474f1f8a7636aa6aa47` |
| `Portraits/ALEXANDRA_panic.png` | `96×96` | 14 | 1,564 | `7862ca6ed9e1d0e901689260c0a2345471a8ec48be01b07ff83b838d13e4f369` |
| `Portraits/ALEXANDRA_blush.png` | `96×96` | 15 | 1,630 | `d90e2b91cbc9a84ebf216616cca17cc4bd35cf8756469e20948b67e03f951d07` |
| `Portraits/ALEXANDRA_crying.png` | `96×96` | 15 | 1,613 | `60da90da94d9d3e270a2a660241108f3852ba06b1fe2af211a97267be842b39d` |
| `Portraits/ALEXANDRA_deadpan.png` | `96×96` | 14 | 1,594 | `9970616fd72c83477d54cb3a7ae134a1190939f4ee5705927740a232f9871604` |
| `Characters/ALEXANDRA.png` | `128×192` | 15 | 2,949 | `8d65f446d5e48ec52be002f634583938a38807ea0f0cbf4a56f6ff2c95d29642` |
| `Characters/trainer_FESTIVAL_ALEXANDRA.png` | `128×192` | 15 | 2,949 | `8d65f446d5e48ec52be002f634583938a38807ea0f0cbf4a56f6ff2c95d29642` |
| `Characters/pose_ALEXANDRA.png` | `128×192` | 17 | 2,077 | `02f6f1cfdee787a8957f7228ece6e96d3edf2c276ccb2753dc80698f959ddfdb` |
