# Proposal: Gilded King Aurelius — Archer Gilgamesh Character Rework & Migration Spec

> [!IMPORTANT]
> **CREATOR-APPROVED FINAL DECISION (`2026-11-23`):** Lock **Path B — `Gilded King Aurelius`** (*King Aurelius Aurel*, First Sovereign of Drowned Aurelia & founder of House Aurel).
> - **Zero repo collisions (`0` matches in `0` files)** — zero conflict with Meridian CEO **`Aurelian Voss`** (`[MERIDIAN_VOSS,Aurelian]`, `025_CharsetAliases.rb`).
> - **Authentic Latin etymology deepens Mystery #8:** *Aurelian* (*Aurelianus*) literally means ***"descendant / heir of Aurelius"*** — making `Gilded Heir Aurelian` (Voss) the literal patronymic shadow of `Gilded King Aurelius`!
> - **For Claude:** Use **`Aurelius`** (`[GILDED_THEODRIC,Aurelius]`, display **`Gilded King Aurelius`**) everywhere the King's given name appears below (never touching Voss's 238 `Aurelian` lines), and still apply the 3 Ruby wiring fixes (`010_Bridge_VersusIntro.rb`, `014_Portraits.rb`, `025_CharsetAliases.rb`).

- **What:** Rework the Gilded King (currently `Theodric` / `GILDED_THEODRIC`) into **Gilded King Aurelius** (*King Aurelius Aurel*, First Sovereign of Drowned Aurelia & founder of House Aurel), elevating his voice, lore, Ruin Route R3/R6/R7 scenes, PBS team presentation, and audio/VS cut-in wiring to an authentic **Archer Gilgamesh** (*Fate/stay night*, *Fate/Grand Order: Babylonia*, *Fate/strange Fake*) archetype grounded seamlessly in Velmora.
- **Why:** Currently `Theodric` reads as a passive, tragic footnote whose sole spoken battle line (`"Three hundred years and still the god will not kneel..."`) undercuts the Ruin Route's climax. Upgrading him into an effortless, mythic King of Heroes — simultaneously amused by counterfeits, scornful of his kneeling descendant Voss, and exhilarated by a Renegade mortal who stares heaven down without flinching — turns the Ruin Route Hijack into one of Prismfall's unforgettable peaks while making his existing Gate-of-Babylon-style team (`Golurk`, `Aegislash`, `Kyogre`, `Groudon`, `Regigigas`, `Gholdengo "Gilt"`) sing narratively.
- **Where it plugs in:** `story/` (9 files, 29 lines), `design/` (9 files, 24 lines), `tools/` (4 files, 9 lines), `pbs/trainers.txt` & `pbs/trainer_types.txt` (2 files, 5 lines), `plugins/` (4 files, 5 lines + 3 wiring guards in `010_Bridge_VersusIntro.rb`, `014_Portraits.rb`, `025_CharsetAliases.rb`), `mapgen/REQUESTS.md` (1 line), `TODO_QUOTA.md` (1 line), and 16 existing PNG assets in `graphics/` (mirrored in `art/out/Graphics/`).
- **Sources:**
  - Repo canon: `story/01_WORLD_LORE.md`, `story/03_CAST.md`, `story/07_ACT_IV.md`, `story/08_ACT_V.md`, `story/09_MYSTERIES_FORESHADOWING.md`, `story/10_CHOICES_ENDINGS.md`, `story/12_RUIN_ROUTE.md`, `story/20_SCRIPT_CH0-2.md`, `story/25_SCRIPT_CH6.md`, `story/33_SCRIPT_CH14.md`.
  - Engine/PBS/Audio: `pbs/trainers.txt`, `pbs/trainer_types.txt`, `tools/trainer_gen/gen.py`, `tools/validate_trainers.py`, `plugins/Prismfall Core/008_Festival_Data.rb`, `012_Narrative_Data.rb`, `015_Festival_Draw.rb`, `025_CharsetAliases.rb`, `plugins/Prismfall EBDX Bridge/010_Bridge_VersusIntro.rb`, `plugins/Prismfall Cutscenes/014_Portraits.rb`, `plugins/Prismfall Z-Power/005_ZPower_TrainerSpeech.rb`, `design/AUDIO_SOUNDTRACK_PLAN.md`, `gemini_recommends/2026-11-23_anime-ost-situational-bgm/PROPOSAL.md`.
  - Character archetype reference: Archer Gilgamesh across *Fate/stay night* (UBW/Fate routes), *Fate/Grand Order — Absolute Demonic Front: Babylonia*, and *Fate/strange Fake*.

---

## Section 1: Name Change, Critical Collision Audit & Zero-Breakage Migration Map

> [!WARNING]
> **CRITICAL CODEBASE COLLISION CAUGHT DURING AUDIT — `Aurelian` IS ALREADY VOSS'S FIRST NAME (`238` lines across `49` files)!**
>
> Before running a find-and-replace, Creator Reuben & Claude must know a hard repo fact:
> - Meridian CEO Voss's canon full name is **`Aurelian Voss`** (`story/03_CAST.md:71–74`, `story/09_MYSTERIES_FORESHADOWING.md:17` Mystery #8: *"★ P: his name, Aurelian."*).
> - In `pbs/trainer_types.txt:306–307` + `pbs/trainers.txt:13082`, Voss already battles as **`[MERIDIAN_VOSS,Aurelian]`** → in-battle display **`Gilded Heir Aurelian`**.
> - In `plugins/Prismfall Core/025_CharsetAliases.rb:23`, `"Aurelian" => "VOSS"` matches any `trainer_*` map event whose name contains the word `Aurelian` — meaning an unguarded event named `"Gilded King Aurelian"` would **silently render Voss's overworld sprite**!
> - In `story/35_SCRIPT_CH16.md:226`, Councillor Sallow refers to Voss simply as *"Oh, Aurelian. Oh, you fool."*
>
> **Two Clean Paths Forward (Both 100% Supported Below):**
> - **Path A — Keep Reuben's Approved Name `Gilded King Aurelian` (*King Aurelian Aurel*, First Sovereign) & Weaponize the Shared Name (PRIMARY TEXT USED IN THIS PROPOSAL):**
>   - **Narrative payoff:** Voss (`Gilded Heir Aurelian`) was literally named by House Aurel after his ancestor **`Gilded King Aurelian`**! That makes the Ruin Route R7 face-off (`Gilded King Aurelian` vs kneeling `Gilded Heir Aurelian`) **even more ruthlessly Gilgamesh**: *"House Aurel's last clerk — dressed in merchant's wool, wearing MY very name like a counterfeit stamp on tin."*
>   - **Mystery #8 protection:** Keep the King's given name *off* Dorian's Ch2 prologue page (refer to him solely as *"the Gilded King"* in Ch2, exactly as `20_SCRIPT_CH0-2.md` already does) and reveal his given name *Aurelian* only in Ch14/Ch17/Ch20 so Mystery #8 pays off as a chilling realization rather than an early spoiler.
>   - **Mandatory code guard (1 line):** Change `plugins/Prismfall Core/025_CharsetAliases.rb:23` from `"Aurelian" => "VOSS"` to `"Aurelian Voss" => "VOSS"` and add `"Gilded King" => "THEODRIC"` + `"King Aurelian" => "THEODRIC"`. (Essentials v21.1 natively permits two trainers named `Aurelian` under distinct trainer types `:MERIDIAN_VOSS` and `:GILDED_THEODRIC`.)
> - **Path B — Strict Zero-Collision 1-Letter Patronymic Alternative: `Gilded King Aurelius` (*King Aurelius Aurel*):**
>   - Audited across the entire repo: **`0` matches in `0` files** (`Aurelius` has true zero collision!).
>   - Etymologically authentic Latin: **`Aurelian`** (*Aurelianus*) literally means ***"descendant / heir of Aurelius"***! So founder **King Aurelius Aurel** (`Gilded King Aurelius`) raises **Aurelia** & **House Aurel**, and 300 years later his heir **Aurelian Voss** (`Gilded Heir Aurelian`) carries the literal patronymic of his ancestor — zero ambiguity in scripts, spreadsheets, `025_CharsetAliases.rb`, or dialogue.
>   - Every drop-in block below uses **Path A (`Aurelian`)** per Reuben's approval; switching to **Path B (`Aurelius`)** requires only replacing `Aurelian` → `Aurelius` on the King's own blocks (never touching Voss's 238 references).

### 1.1 Exact Codebase Audit Summary (Verified via Full Repo Scan)

Excluding `.git/` and `gemini_recommends/`:

| Scope | `Theodric` / `THEODRIC` / `GILDED_THEODRIC` Hits | Files | Notes |
|---|---:|---:|---|
| `story/` | **29 lines** | **9 files** | Lore, Cast, Acts IV–V, Choices/Endings, Ruin Route, Comedy, Ch14 Script |
| `design/` | **24 lines** | **9 files** | Narrative Keys, Balance, Walkthrough, Field Playbook, Audio, Mega, Cameos, Systems |
| `tools/` | **9 lines** | **4 files** | `trainer_gen/gen.py`, `harness/run_mega.rb`, `walkthrough/template*.md` |
| `pbs/` | **5 lines** | **2 files** | `pbs/trainer_types.txt` (1), `pbs/trainers.txt` (4) |
| `plugins/` | **5 lines** | **4 files** | `008_Festival_Data.rb`, `012_Narrative_Data.rb`, `015_Festival_Draw.rb`, `107_Boss_Groudon.rb` |
| `mapgen/` | **1 line** | **1 file** | `mapgen/REQUESTS.md:1118` |
| Root | **1 line** | **1 file** | `TODO_QUOTA.md:32` |
| **Total Text References** | **74 lines** | **30 files** | Plus **3 newly audited plugin guard gaps** (`010_Bridge_VersusIntro.rb`, `014_Portraits.rb`, `025_CharsetAliases.rb`) |
| `graphics/` (PNG assets) | **16 files** | **16 PNGs** | `Trainers/GILDED_THEODRIC.png`, `EBDX/VS/THEODRIC.png`, `Characters/` (2), `Portraits/` (12) |
| `art/out/Graphics/` (mirror) | **16 files** | **16 PNGs** | Exact build-output mirror of the 16 `graphics/` PNGs |
| `"Gilded King"` (title / play) | **77 lines** | **34 files** | Keep title *"Gilded King"* everywhere; only `design/AUDIO_SOUNDTRACK_PLAN.md:238` combines `"Gilded King Theodric"` |

---

### 1.2 Zero-Breakage Asset & Internal-ID Strategy (Dual Option for Claude)

#### Option 1 (Recommended — Zero Churn, Zero Broken Art, Save-Safe): Keep Internal IDs & Asset Filenames, Alias Display & Presentation
Keep the PBS TrainerType ID `[GILDED_THEODRIC]`, Festival entrant key `:THEODRIC`, and all **16 existing `graphics/` PNGs** untouched on disk, while migrating every player-facing name, trainer name, portrait display label, and story doc to **`Aurelian`** (or `Aurelius`):
- **Why this wins:** Zero `git mv` churn across 32 binary PNGs, zero broken in-progress Ruin saves referencing `:GILDED_THEODRIC` or `:THEODRIC`, and zero breakage in `tools/harness/run_mega.rb`.
- **Three Mandatory Ruby Wiring Fixes (Even BEFORE This Rework, Two of These Were Silent Bugs!):**
  1. **`plugins/Prismfall EBDX Bridge/010_Bridge_VersusIntro.rb`** (lines 28–60):
     - **Bug caught:** `:GILDED_THEODRIC` was missing from `VS_IDS` and `"THEODRIC"` was missing from `THEMES`. Previously, his B2W2 VS cut-in ONLY worked because `trainer.name.upcase` happened to equal `"THEODRIC"` — and it fell back to `:violet` instead of `:gold`! Changing his PBS trainer name to `Aurelian` **breaks his VS cut-in** unless we add:
       ```ruby
       # In PrismfallVS::VS_IDS (after line 46):
       :GILDED_THEODRIC => "THEODRIC",  # PBS name "Aurelian" (keeps Graphics/EBDX/VS/THEODRIC.png)

       # In PrismfallVS::THEMES (after line 59):
       "THEODRIC" => :gold,             # Imperial gold radial tunnel & bands
       ```
  2. **`plugins/Prismfall Cutscenes/014_Portraits.rb`** (lines 86–97):
     - **Bug caught:** `ONLY_CAST = true`, yet `:THEODRIC` / `:AURELIAN` / `:GILDED_KING` was **never added to `CAST`**! Even though all 12 `Graphics/Portraits/THEODRIC*.png` files already exist on disk, any `\pf[THEODRIC, smug]` dialogue line would silently suppress the face window! Add:
       ```ruby
       # In Prismfall::Portrait::CAST (line 95):
       THEODRIC GILDED_KING

       # And register clean display name + asset alias (below CAST or in init):
       Prismfall::Portrait.register(:THEODRIC, name: "Gilded King Aurelian", trainer: :GILDED_THEODRIC, cast: true)
       Prismfall::Portrait.register(:GILDED_KING, name: "Gilded King Aurelian", trainer: :GILDED_THEODRIC, cast: true)
       # Note: in map scripts, use [portrait: THEODRIC, smug] (or \pf[THEODRIC,smug,,Gilded King Aurelian])
       # so Portraits resolves Graphics/Portraits/THEODRIC_<expr>.png while displaying "Gilded King Aurelian".
       ```
  3. **`plugins/Prismfall Core/025_CharsetAliases.rb`** (line 23 — **mandatory for Path A `Aurelian`**):
     - Currently: `"Aurelian" => "VOSS"` matches any `trainer_*` event containing `\bAurelian\b`.
     - Replace with:
       ```ruby
       "Aurelian Voss" => "VOSS",
       "Gilded King"   => "THEODRIC",
       "King Aurelian" => "THEODRIC",
       ```
     - *(And verify no map event for Voss is named solely `"Aurelian"` without `"Voss"` — audited `mapgen/specs/109_dovetail.yaml`, `100_ferrows_landing.yaml`, and `design/maps.json`: Voss's events are named `"Aurelian Voss"` or `"Voss"`, so `"Voss" => "VOSS"` + `"Aurelian Voss" => "VOSS"` covers 100% of Voss events!)*

#### Option 2 (Optional Clean-Sweep Rename): Rename Internal IDs & Asset Files to `GILDED_AURELIAN` / `AURELIAN_KING`
Only if Claude prefers total symbol purity post-Ruin-freeze (note: use `AURELIAN_KING` rather than bare `AURELIAN` for portraits/VS/charsets so nothing can ever collide with Voss's PBS name `Aurelian`):
- Rename `[GILDED_THEODRIC]` → `[GILDED_AURELIAN]` in `pbs/trainer_types.txt`, `pbs/trainers.txt`, `tools/trainer_gen/gen.py`, `tools/harness/run_mega.rb`, `008_Festival_Data.rb`, `015_Festival_Draw.rb` (`:THEODRIC` → `:AURELIAN_KING`).
- `git mv` the 16 `graphics/` files (and 16 `art/out/Graphics/` mirrors):
  - `graphics/Trainers/GILDED_THEODRIC.png` → `graphics/Trainers/GILDED_AURELIAN.png`
  - `graphics/Characters/trainer_GILDED_THEODRIC.png` → `graphics/Characters/trainer_GILDED_AURELIAN.png`
  - `graphics/Characters/THEODRIC.png` → `graphics/Characters/AURELIAN_KING.png`
  - `graphics/EBDX/VS/THEODRIC.png` → `graphics/EBDX/VS/AURELIAN_KING.png`
  - `graphics/Portraits/THEODRIC{,_angry,_blush,_crying,_deadpan,_happy,_neutral,_panic,_sad,_shocked,_smug,_surprised}.png` → `AURELIAN_KING{...}.png`
- Still wire `:GILDED_AURELIAN => "AURELIAN_KING"` in `010_Bridge_VersusIntro.rb` and `:AURELIAN_KING` in `014_Portraits.rb`.

---

### 1.3 Complete File-by-File Migration Table (All 30 Text Files + 3 Plugin Guard Files)

*(Under Recommended Option 1: keep internal `:GILDED_THEODRIC` / `:THEODRIC` symbols & PNG filenames; migrate all narrative, display, and PBS trainer names to `Aurelian` [or `Aurelius` under Path B].)*

#### A. PBS & Trainer Generator (3 files, 6 lines)
| File | Lines | Current | Migration Action |
|---|---:|---|---|
| `pbs/trainer_types.txt` | 420–426 | `[GILDED_THEODRIC]` / `Name = Gilded King` | Keep `[GILDED_THEODRIC]` & `Name = Gilded King`; optionally update `BattleBGM` / `IntroBGM` (see §4–§5). |
| `pbs/trainers.txt` | 15061, 15063, 15104, 15151 | `[GILDED_THEODRIC,Theodric]` (+ `100`, `200`) + old `LoseText` | Drop in validated §4 blocks (`[GILDED_THEODRIC,Aurelian]`, new Gilgamesh `LoseText`, treasury nicknames). |
| `tools/trainer_gen/gen.py` | 1112–1127 | `X("Hijack (Ruin) - Theodric...", "GILDED_THEODRIC", "Theodric", ...)` | Update generator source identically to §4 so PBS regeneration never reverts the rework! |

#### B. Ruby Plugins & Harness (5 files, 7 lines + 3 guard files)
| File | Lines | Current | Migration Action |
|---|---:|---|---|
| `plugins/Prismfall Core/008_Festival_Data.rb` | 61 | `:THEODRIC => { :display => "Theodric", :trainer_type => :GILDED_THEODRIC, :name => "Theodric", ... }` | Update `:display => "Gilded King Aurelian"` and `:name => "Aurelian"` (keep key `:THEODRIC` & `:trainer_type => :GILDED_THEODRIC` under Option 1). |
| `plugins/Prismfall Core/012_Narrative_Data.rb` | 114, 415 | `:ruin_voss` desc (`"R4: Voss kneels to Theodric's reflection"`); `:GO_R_KNEEL` epitaph (`"...and Theodric finished his sentence."`) | Fix desc to `"R7: Voss kneels to Aurelian's reflection"` (also fixes R4→R7 typo!); update `:GO_R_KNEEL` epitaph to upgraded §3D2 text (`"...and King Aurelian finished his sentence."`). |
| `plugins/Prismfall Core/015_Festival_Draw.rb` | 47 | `{ :opponent => :THEODRIC, :condition => "ruin_route" }` | Keep `:THEODRIC` under Option 1 (add inline comment `# Gilded King Aurelian`); rename only under Option 2. |
| `plugins/Prismfall Bosses/107_Boss_Groudon.rb` | 4 | `# ...recording Theodric's "Year of Two` | Comment rename: `Theodric's` → `King Aurelian's`. |
| `plugins/Prismfall EBDX Bridge/010_Bridge_VersusIntro.rb` | 46, 59 | *(Missing entry — silent bug!)* | **ADD** `:GILDED_THEODRIC => "THEODRIC"` to `VS_IDS` and `"THEODRIC" => :gold` to `THEMES`. |
| `plugins/Prismfall Cutscenes/014_Portraits.rb` | 95 | *(Missing entry — silent bug!)* | **ADD** `THEODRIC GILDED_KING` to `CAST` + `Portrait.register(:THEODRIC, name: "Gilded King Aurelian", ...)`. |
| `plugins/Prismfall Core/025_CharsetAliases.rb` | 23 | `"Aurelian" => "VOSS"` | **CRITICAL PATH A GUARD:** Change to `"Aurelian Voss" => "VOSS"`, add `"Gilded King" => "THEODRIC"`, `"King Aurelian" => "THEODRIC"`. |
| `tools/harness/run_mega.rb` | 360, 366 | `GILDED_THEODRIC` regex & `no_ring` array | Keep `:GILDED_THEODRIC` under Option 1 (no change needed). |

#### C. Story Bible & Scripts (9 files, 29 lines)
| File | Lines | Current Reference | Migration Action |
|---|---:|---|---|
| `story/00_OVERVIEW.md` | 63, 125 | `King Theodric Aurel`, `Theodric tried to remake the land...` | Update to `King Aurelian Aurel` / `Aurelian` + brief royal-pride motive nuance. |
| `story/01_WORLD_LORE.md` | 20, 22, 24, 41 | `King Theodric Aurel`, `— Theodric`, `Theodric was not a monster...`, `Theodric's daughter Princess Maren Aurel` | Apply §3A drop-in lore upgrade (preserves Blight Years & Maren while locking in Archer Gilgamesh sovereignty). |
| `story/03_CAST.md` | 362 | `King Theodric Aurel, "the Gilded King" (d. AF 0)` | Replace with §3A expanded Historical Figure + Ruin Hijacker entry. |
| `story/07_ACT_IV.md` | 92, 275 | `Theodric's "Year of Two Weathers"`, Voss: `"...showed me Theodric's notebooks."` | Update to `King Aurelian's` / `"the Gilded King's notebooks — my namesake's notebooks"` (Path A) or `"Aurelius's notebooks"` (Path B). |
| `story/08_ACT_V.md` | 317 | `Ruin Route: Theodric, the Gilded Reflection` | Update to `Gilded King Aurelian, the Gilded Reflection`; optionally add §3A Night of Masques play excerpt at line 217. |
| `story/10_CHOICES_ENDINGS.md` | 242, 255, 278, 287, 327, 370, 383, 398, 399, 422 | 10 hits (`Theodric` in tables, Ruin summary, R3/R7 beats) | Update all 10 hits to `Aurelian` / `Gilded King Aurelian` (keep `Hijack {Aurelian (Gilded King), Quent, Voss}` unambiguous vs Voss). |
| `story/12_RUIN_ROUTE.md` | 38, 41, 76, 77, 78, 79, 93 | 7 hits (R3 mirror-wall, R3 cliffhanger, R7 entrance, `GO_R_KNEEL`, `:ruin_voss`, Hijack, Balance) | Update all 7 hits & adopt §3B–§3D scene beats (including R6 Night of Masques mirror interruption!). |
| `story/15_COMEDY.md` | 370 | `Theodric (reflection: neutral, angry, smug)` | Update to `Gilded King Aurelian (reflection: neutral, angry, smug, happy — uses THEODRIC_*.png)`. |
| `story/33_SCRIPT_CH14.md` | 391 | `09 #15: Theodric's Year of Two Weathers` | Update to `King Aurelian's Year of Two Weathers` + optionally adopt §3A glyph phrasing. |

#### D. Design Docs, Walkthrough Templates, Mapgen & Quota (13 files, 32 lines)
| File | Lines | Migration Action |
|---|---:|---|
| `design/NARRATIVE_KEYS.md` | 145, 445, 456, 481, 608, 613, 712, 747 | Update display/prose `Theodric` → `Gilded King Aurelian` (keep `:THEODRIC` / `GILDED_THEODRIC` IDs under Option 1; sync `:GO_R_KNEEL` epitaph with `012_Narrative_Data.rb`). |
| `design/BALANCE.md` | 217, 287, 588, 593 | Update `GILDED_THEODRIC,Theodric,0` → `GILDED_THEODRIC,Aurelian,0` and prose `Theodric` → `King Aurelian`. |
| `design/TRAINER_FIELD_PLAYBOOK.md` | 40, 411, 491 | Update `Theodric` → `King Aurelian` (keep all Inverse-chart tactical notes unchanged). |
| `design/MEGA_EVOLUTION.md` | 60, 388 | Update `Theodric` → `Gilded King Aurelian` (keep *"no ring: the rings came three centuries after him"* — pure Gilgamesh disdain for modern trinkets!). |
| `design/AUDIO.md` | 222 | Keep `GILDED_THEODRIC`, note dedicated `Battle - Gilded King` override (see §5). |
| `design/AUDIO_SOUNDTRACK_PLAN.md` | 238 | Update `Gilded King Theodric` → `Gilded King Aurelian` (and evaluate §5 brass-majesty BGM options). |
| `design/CAMEOS.md` | 105 | Update `Theodric's reflection` → `King Aurelian's reflection`. |
| `design/SYSTEMS.md` | 161 | Update `(Voss, Quent or Theodric)` → `(Voss, Quent or Gilded King Aurelian)`. |
| `design/WALKTHROUGH.md` | 3279, 3390, 3395 | Update `Theodric` → `Gilded King Aurelian` (regenerate from templates). |
| `tools/walkthrough/template.md` | 3279, 3390, 3395 | Update `Theodric` → `Gilded King Aurelian`. |
| `tools/walkthrough/template_render.md` | 3274, 3385, 3390 | Update `Theodric` → `Gilded King Aurelian`. |
| `mapgen/REQUESTS.md` | 1118 | Update `Theodric` → `King Aurelian`. |
| `TODO_QUOTA.md` | 32 | Update `Nyx, Celestine, Theodric.` → `Nyx, Celestine, King Aurelian.` |

---

## Section 2: Character Bible — Gilded King Aurelian (The Archer Gilgamesh Archetype in Velmora)

### 2.1 Core Identity & Philosophy
- **Full Name & Titles:** **King Aurelian Aurel**, First Sovereign of the Aureate Kingdom, called **"the Gilded King"** *(and in the Ruin Route: **Gilded King Aurelian, the Gilded Reflection**)*.
- **Visual Anchor (Existing Art Verified):** Tall, broad-shouldered sovereign in black-and-gold enameled plate, crimson-lined royal mantle, jagged sunburst crown, heavy golden chain-links across the cuirass, dark hair streaked with molten gold, holding a gilded Poké Ball in a languid, elevated palm (`graphics/Trainers/GILDED_THEODRIC.png`, `graphics/EBDX/VS/THEODRIC.png`, `graphics/Portraits/THEODRIC_smug.png`). His sprites already radiate effortless, golden-armored majesty.
- **How Archer Gilgamesh Reconciles with Prismfall's Canon Blight Years (`01_WORLD_LORE.md`):**
  - *Prismfall canon:* Aurelia suffered twenty years of crop-rot and wasting plague ("the Blight Years"). King Aurelian did not forge the Gilded Chain out of cartoonish evil — his city was starving, and he loved Aurelia fiercely.
  - *The Gilgamesh fusion (*FGO Babylonia* + *FSN* + *strange Fake*):* A true king does not love his people like a weeping caretaker (Valen) or an aggrieved utility executive (Voss). **He loves his kingdom the way Gilgamesh loved Uruk: as the crowning masterpiece of mortal hands, and HIS supreme treasure.** When blight rotted his golden terraces beneath Arceus's silent sky, he felt neither terror nor piety — he felt **imperial indignation**:
    > *"The heavens hung their light above MY kingdom without asking leave, and then let rot touch my granaries while they slept. A landlord who will not mend the roof loses the deed."*
  - He did not beg Arceus for mercy. First he collared **Groudon** and **Kyogre** to carve fresh seas and fertile soil by royal decree (*the Year of Two Weathers*); when the primordial beasts proved too crude for his gardens, he turned his eyes higher and had his Gilders forge the **Gilded Chain** to collar heaven itself.
  - Even when Arceus shattered itself rather than kneel and dropped Aurelia into the sea, Aurelian did not die weeping. Frozen behind Antumbra's Glass at the precise heartbeat of AF 0, he spent three hundred years **smiling with his hand still on the Chain** — waiting for an age with enough spine to be worth stepping back into.

### 2.2 Speech Cadence Rules (Staying Authentically *Prismfall* + *Fate*)

| DO (Authentic Archer Gilgamesh × Prismfall) | DON'T (Tonal Breaks & Cheap Parody to Avoid) |
|---|---|
| **Speak with effortless, unhurried amusement.** He never yells to sound big; his calmest sentences carry the weight of a decree. | **Never rant like an insecure shonen villain.** No `"Impossible!! How dare a child defeat me!!"` or panicked breakdowns. |
| **Use `"mongrel"` sparingly, with surgical sting.** Save it for counterfeits (Voss, imitators, kneeling crowds) and his opening appraisal of the PC — then **drop it** the moment the PC proves worthy! | **Never spam `"Zasshu!"`, Japanese honorifics, or meme catchphrases.** Keep 100% Velmoran literary English matching `03_CAST.md` and `08_ACT_V.md`. |
| **Use Velmoran equivalents for his Fate motifs:** *"my treasury"*, *"the Chain"*, *"counterfeit"*, *"know your station"*, *"my court"*, *"my Sun Court"*, *"borrowed plates"*, *"the original"*. | **Never name-drop Fate lore.** No `"Gate of Babylon"`, `"Ea"`, `"Enuma Elish"`, `"Enkidu"`, `"Heroic Spirit"`, `"Uruk"`, or `"Noble Phantasm"`. |
| **Frame his Pokémon as crown regalia & collared calamities.** Golurk is his original Sun Court sentinel; Aegislash is his royal blade; Kyogre & Groudon are unruly tools from the Year of Two Weathers; Gholdengo ("Gilt") is Aurelia's molten treasury made manifest. | **Never treat him as a sentimental Pokémon trainer.** He does not say `"I believe in the power of friendship!"` — he respects strength, craft, and sovereign will. |
| **Shift from lazy scorn → razor intrigue → grinning exhilaration.** When the Renegade PC walks through his Inverted Prism Arena without flinching, he *enjoys* the fight like *Babylonia* / *strange Fake* Gilgamesh encountering a worthy rival. | **Never turn him into a tragic apologizer at defeat.** He never says *"Perhaps I was wrong..."* — he laughs, salutes the mortal who broke his court, and tells them to go stare down heaven. |
| **Keep lines crisp and musical (Prismfall's prose standard).** 1–3 punchy sentences per box, rich rhythm, sharp imagery (gold, glass, wool, tin, crowns, collars). | **Never write 10-line RPG Maker monologue walls.** Every dialogue box should hit cleanly in 2–3 lines inside Essentials' speech window. |

### 2.3 Relationship Matrix

| Character / Entity | How Gilded King Aurelian Sees Them | Narrative Dynamic |
|---|---|---|
| **Aurelian Voss** (`MERIDIAN_VOSS`, *Gilded Heir*) | **A pathetic counterfeit.** A clerk in charcoal wool who built a neon shop-tower on Aurelia's drowned roof, stitched a tin harness from Gilder scraps, and crawled to the glass on his knees. *(Path A bonus: mocks him for wearing his ancestor's very name like a stamped imitation coin.)* | **Absolute thematic contrast.** Voss thinks he's carrying House Aurel's torch; the real King reveals Voss only inherited the *grudge* without the *sovereignty*. Casting Voss into the Chain in R7 breaks Voss's worldview in ten seconds. |
| **The Renegade PC** (Ruin Route) | **R3:** Mild curiosity — *"Why does this mortal's shadow stand upright behind the glass?"* **R6:** A worthy spectator in the front row. **R7 Opening:** Lazy test (`GO_R_KNEEL`). **R7 Mid/Post-Battle:** **Exhilarated royal recognition** — the first being in 300 years with the audacity to look a god in the eye and say *No more*. | The emotional arc of his boss fight: **Amused Contempt → Appraising Intrigue → Terrifying Joy → Sovereign Salute.** He calls them *"mongrel"* until Gilt falls — and never again afterward. |
| **Arceus** (*The Original One*) | **The only worthy rival.** Not a deity to pray to, nor a monster to hate — a peerless sovereign whose light trespassed on Aurelia's sky. He genuinely respects *one* thing Arceus did: breaking itself rather than wearing a collar. | *"A proud beast. It shattered its own ribs rather than kneel. I can respect that much — which is why I intend to finish the argument."* |
| **Dorian Pell & Ansel Crewe's Play** (*The Gilded King*) | **Delightful, slightly timid theater.** He is genuinely entertained that mortals hanged a playwright for remembering him, and critiques Dorian's actor on velvet, cadence, and courage in R6. | Gives the Ruin Route a chilling, unforgettable burst of *Fate/strange Fake* theatricality right before the bleak finale. |
| **Sovereign Valen Corrigan** | **Pitying, biting scorn.** A weary caretaker turning his own arm to crystal to hush eighteen pieces of a god he's too small to claim or break. | *"Ten generations of clerks polishing the bars of their own cage, and calling the bruise 'duty.' Maren's charity ruined you all."* |
| **Princess Maren Aurel** (his daughter, founder of the Accord) | **The one mortal he never calls a mongrel.** Sharp, private paternal sting beneath royal exasperation: she had Aurel iron in her spine when she stood against him in the Sun Court — and then wasted it founding an Accord of kneelers. | Reveals his buried humanity without softening his edge: *"My daughter was the only soul in Aurelia who dared tell me no without lowering her chin. Pity she built a monastery out of her backbone."* |
| **The Reflection & Giratina** | **Amused recognition behind the Glass.** He notices the PC's second shadow immediately in R3 (*"Twenty-three graves, and you carry your own corpse behind your heel. Now THAT is entertaining."*). | Ties his frozen three-century exile behind Antumbra's Glass directly into the Ruin Route's metaphysics. |

---

## Section 3: Complete Drop-In Dialogue & Scene Rewrites

> **Script Notation:** Matches Prismfall's canonical script format (`story/20_SCRIPT_CH0-2.md`, `story/25_SCRIPT_CH6.md`, `story/33_SCRIPT_CH14.md`). Under Option 1 asset wiring, `[portrait: THEODRIC, <expr>]` renders `Graphics/Portraits/THEODRIC_<expr>.png` while displaying the registered name **`Gilded King Aurelian`** (via `Portrait.register(:THEODRIC, name: "Gilded King Aurelian", ...)`). In YAML/mapgen specs, write `\pf[THEODRIC,<expr>,,Gilded King Aurelian]`.
> *(Under Path B, substitute `Aurelius` for the King's given name wherever it appears below.)*

---

### A. Lore Documents, Murals & Dorian's Banned Play (*The Gilded King*)

#### A1. `story/01_WORLD_LORE.md` §2 ("Before the Fall: the Aureate Kingdom" — replaces lines 17–25 & 41)
```markdown
### Before the Fall: the Aureate Kingdom
Before AF 0, one kingdom ruled the continent: **the Aureate Kingdom of House Aurel**. Its capital, **Aurelia**, rose in gold terraces up the southern sea-cliffs—a monument of clockwork aqueducts, sun-towers, and court alchemy built by **the Gilders**.

The kingdom's last two decades were **the Blight Years**: crop-rot, a wasting plague, and three failed harvests running. King **Aurelian Aurel**, later called **the Gilded King**, did not pray to heaven for relief. He treated the blight as an insult to his crown.
- **First he collared the world.** The Gilders woke Groudon beneath the Bone Sands and Kyogre off the western coast to carve fresh seas and fertile soil by decree. When the two titans nearly tore the continent in half rather than plow his fields, he drove them back to sleep—Ossaria's Unown records call this **"the Year of Two Weathers"**, and the Dry Tide west of Duneholt is the seabed Kyogre left behind.
- **Then he turned his eyes higher.** The Gilders forged **the Gilded Chain**: eighteen golden locks, one for each Plate, around a **keystone cradle** shaped for the Legend Plate. They meant to summon Arceus and bind it to the Sun Court's throne.
  - *"The heavens hung their light above my kingdom without asking leave, and then let rot touch my granaries. If heaven will not kneel, we'll build a chain."* — **King Aurelian**, as preserved in Ansel Crewe's banned play *The Gilded King*.

Aurelian was neither madman nor penitent. He loved Aurelia as the apex of mortal pride, and refused to watch his jewel starve beneath an indifferent sky. That grandeur—and that arrogance—is why Voss can quote him three hundred years later without knowing how small his own imitation looks beside the original.
```
*(Line 41 updates `Theodric's daughter` → `Aurelian's daughter **Princess Maren Aurel**`.)*

#### A2. `story/03_CAST.md` ("HISTORICAL FIGURES" — replaces line 362)
```markdown
- **King Aurelian Aurel, "the Gilded King"** (d. AF 0; Ruin Route hijacker `GILDED_THEODRIC`, lv 100 on `:PRISM_ARENA` Inverse): First Sovereign of drowned Aurelia and architect of the Gilded Chain. Imperious, fiercely proud, and effortlessly theatrical—he tried to collar Arceus not out of pious terror, but out of royal fury that heaven let blight touch *his* kingdom. Frozen behind Antumbra's Glass at the instant of the Calling, he survives in the Ruin Route as a grinning, terrifying sovereign who despises counterfeits (including his own kneeling descendant Voss) and respects only a mortal daring enough to look a god in the eye without flinching.
```

#### A3. `story/20_SCRIPT_CH0-2.md` — Dorian's Dressing Room & *Gilded King Prologue* Key Item (Ch2, Mystery #8 Safe!)
*(Note: Keep the King's given name **omitted** from the Ch2 prologue page so Mystery #8 — Voss's first name `Aurelian` — stays completely unspoiled until Act IV/V! Enhance the Key Item description & Dorian's answer to "Who was the Gilded King?":)*
```text
(Received: GILDED KING PROLOGUE. Key Item.
"A yellowed playbill page in Ansel Crewe's slanted ink, dated AF 52.
'PROLOGUE — SPOKEN BEFORE THE GOLD CURTAIN:
Three harvests rotted under a quiet sky.
The priests said kneel. The Gilded King laughed until the bells cracked.
"My terraces do not beg rain from an absentee roof," said he.
"If heaven will not kneel, we'll build a chain."'")

> Who was the Gilded King?
  [portrait: DORIAN, deadpan] A sovereign who looked up at the sky and decided it was trespassing on his skyline.
  [portrait: DORIAN, neutral] Read it somewhere I'm not, darling. My neck is far too handsome for a rope.
```

#### A4. `story/25_SCRIPT_CH6.md` & `story/33_SCRIPT_CH14.md` — Ancient Inscriptions (Murals & Groudon Undersands)
- **`story/25_SCRIPT_CH6.md` (Mural 1 inspect addition, line 312–313):**
  ```text
  MURAL 1: A king in gold, on a throne under a sun, one hand raised as if weighing the sky itself. Below him, his city: towers and domes and a harbour full of ships. His face has been scratched out, very carefully, by someone with a chisel and a lot of time—all except the corner of a smile they missed.
  [portrait: SAHAR, neutral] A golden king. Look at the posture—he isn't praying. He's giving the sun an order.
  ```
- **`story/33_SCRIPT_CH14.md` (Groudon bar-break Unown glyphs, lines 381–383):**
  ```text
  - Bar 1 → 2: *"In the King's ninth year he summoned the red titan and the blue, saying: 'Remake my soil, beasts, or be broken.'"*
  - Bar 2 → 3: *"The land split and the sea boiled, and still the King did not step back from his balcony. When the titans would not obey—"*
  - Bar 3 broken: *"...he laughed, turned his eyes to heaven, and called for his goldsmiths."*
  ```

#### A5. `story/08_ACT_V.md` — Night of Masques Stage Excerpt (Ch20 Main Route, enriches lines 213–219)
```text
(Crownhaven Basilica Square. Torchlight. Dorian's gilded proscenium towers beneath the Cathedral bells. The actor playing the Gilded King—clad in crimson-lined velvet and a jagged pasteboard crown—steps to the apron, lifting a prop chain of painted wood toward the real sky.)

[name: Actor (as the Gilded King)] "You ask why I do not bow before the eighteen lights, my daughter? Look down at Aurelia! Look at our aqueducts, our towers, our bread!"
[name: Actor (as the Gilded King)] "The sky hung its splendor above MY kingdom without asking leave—and when the blight came, heaven kept its hands folded!"
[name: Actor (as the Gilded King)] "Let priests measure their gratitude in crumbs. A king does not beg for what stands beneath his sun! If heaven will not kneel—WE'LL BUILD A CHAIN!"

(Every head in the square turns at once toward the Meridian box. Above them, Aurelian Voss rises slowly and claps. Alone. Warmly.)
[portrait: VOSS, happy] Bravo. They finally cast the king correctly.
```

---

### B. Ruin Route R3 — "The Sun Court Below" (Drowned Aurelia Mirror-Wall First Meeting)

**Plugs into:** `story/12_RUIN_ROUTE.md` §R3 (lines 34–42) — replaces the sparse 4-bullet summary with a full playable scene.

```text
## R3 — Drowned Aurelia: The Sun Court Below (Map 826 / Mirrorwalk)

(Under green sea-glass light, the drowned throne room stands silent. Ahead, the colossal throne of the Gilded King rises out of coral-crusted marble. Its armrests—which were open hands on the main route—are now clenched into solid golden fists.)

[portrait: REFLECTION, neutral] (quietly, from your shadow) We've done that one. The hands remember closing.
(Inspecting the throne: "Sit on the Gilded King's throne?" — If Yes: you sit. Nothing closes. Only a faint, amused scrape echoes from the polished mirror-wall at the throne's back.)

[portrait: THEODRIC, smug] (a dry, resonant voice vibrating THROUGH the glass, calm as poured wine)
...Oh? Already learned not to put your fingers in a king's seat?
[portrait: THEODRIC, happy] Pity. My artificers spent six months on those armrests.

(The PC steps toward the great mirror-wall behind the throne. It is not a reflection of the flooded ruins—it is a WINDOW into AF 0. Behind the glass, the Sun Court blazes in dry, impossible midsummer gold: banners taut in mid-air, Gilders frozen mid-chant, sparks hung motionless in the air like dust—and at the center, King Aurelian Aurel, holding the blazing Gilded Chain mid-command.)
(Nothing behind the glass moves. Not a banner. Not a mote of light.)
(Then his golden eyes slide sideways and lock straight onto you.)

[portrait: THEODRIC, neutral] Well, now. What wandered through the glass?
[portrait: THEODRIC, smug] No color in your chest. No tint in your step. And behind your heel...
(His gaze flicks down to the PC's Reflection, standing silently at your shoulder.)
[portrait: THEODRIC, happy] Ha. Twenty-three graves, and you wear your own corpse as a shadow. Three centuries of staring at drowned fish, and at last something mildly entertaining arrives.

(SFX: Heavy hydraulic hiss. The far wall's pressure-door shears open. Meridian floodlights cut across the marble. Aurelian Voss steps into the air-pocket, helmet tucked beneath his arm—and stops dead when he sees the blazing Sun Court behind the mirror-wall.)

[portrait: VOSS, shocked] ...No.
(His briefcase slips from his fingers and clangs on the marble. For the first time in the entire game, the calmest man in Velmora drops straight to both knees.)
[portrait: VOSS, crying] He's alive. Three hundred years—behind the glass, he's still *alive*...
[portrait: VOSS, neutral] My lord... Your Majesty... House Aurel kept the notebooks. I built the Spire on your foundations. I brought back the cradle—

(Behind the glass, King Aurelian slowly tilts his chin down to inspect the kneeling executive in charcoal wool and a pressure-collar. His smile never fades—it simply turns razor-cold.)

[portrait: THEODRIC, deadpan] ...Stand up, whatever you are. You're getting mud on my reflection.
[portrait: THEODRIC, smug] "House Aurel"? In THAT tailor's mourning-coat? You look like a royal tax collector who stole the silverware during a fire.
[portrait: VOSS, shocked] I—I built the Engine! Eighteen pylons in Crownhaven! Better than metal, my lord—it only needs the cradle—
[portrait: THEODRIC, neutral] (barely glancing at Voss now, waving two fingers dismissively)
Then fetch your little brass toy and set the stage, clerk. Even a stray hound can carry a bone to the right door.

(Voss doesn't hear the contempt—or refuses to. His eyes shine with terrible, broken zeal as his salvage team hoists the keystone cradle from the floor and retreats toward the submarine lock.)
[portrait: VOSS, happy] It will be ready at the Coronation, Your Majesty. Every lock. Every light.

(The lock seals. Silence returns to the drowned court. Only you, your Reflection, and the King behind the glass remain.)
(King Aurelian lifts his free hand and presses his golden-gauntleted fingertips against the inside of the mirror—directly opposite your chest.)

[portrait: THEODRIC, smug] Look at him. Three hundred years, and my bloodline prays to a ghost in a pane of glass.
[portrait: THEODRIC, neutral] You, however, did not kneel. You didn't even blink.
(A slow, dangerous grin spreads across his face—the smile of a king spotting a gladiator who might actually draw blood.)
[portrait: THEODRIC, happy] Bring that little tin crown to Crownhaven, hollow thing. Let the merchant finish building my door.
(His fingers curl around the blazing Gilded Chain inside the mirror. His lips form one crisp command, vibrating through the glass like struck gold:)
[portrait: THEODRIC, smug] *"Finish."*
```

---

### C. Ruin Route R6 — "The Unfestival" (Night of Masques — The Real King Behind the Stage Mirror)

**Plugs into:** `story/12_RUIN_ROUTE.md` §R6 beat 6 (line 68) — transforms a 1-sentence bullet into an iconic *Fate/strange Fake* theatrical scene!

```text
## R6 — Crownhaven Basilica Square: The Night of Masques (Ruin Variant)

(Midnight in Crownhaven. Fewer lanterns than on the main route; the crowd keeps an uneasy three-pace radius around the Renegade PC in the front row. On Dorian's stage, Celestine has just finished Princess Maren's lament—her eyes locked darkly on you—when the actor playing the Gilded King sweeps forward in crimson velvet.)
(Behind him, set into the painted Sun Court backdrop, stands Dorian's tallest dressing-room mirror—placed there to catch the torchlight.)

[name: Actor (as the Gilded King)] "Let priests measure their gratitude in crumbs! If heaven will not kneel, we'll—"

(The stage torches flicker VIOLENTLY. Every candle turns bright, metallic gold. The glass behind the actor stops reflecting the square—instead, a blazing golden throne room yawns open inside the frame, and a tall figure in black-and-gold armor strolls lazily up to the glass, right behind the actor's shoulder.)

(The actor freezes mid-breath. His painted wooden chain slips and clatters across the boards. In the wings, Dorian goes paper-white.)
[portrait: DORIAN, shocked] ...That isn't a lighting cue. Somebody drop the—drop the curtain!

(The velvet ropes won't budge. From inside the stage mirror, King Aurelian leans casually against the gilded frame, one elbow propped as if critiquing a rehearsal from the royal box.)

[portrait: THEODRIC, smug] Passable velvet, actor—though you play my laugh far too humbly.
[portrait: THEODRIC, deadpan] And tell whoever stitched that crown that my goldsmiths would have been thrown off the sea-cliffs for proportions that sloppy.

(Gasps ripple across the Basilica Square. Guards reach for Poké Balls and freeze—every reflective shield, every lantern pane, every Basilica window shows the same golden gaze looking down at them.)

[portrait: THEODRIC, neutral] Ansel Crewe, was it? The playwright they hanged for remembering my name?
[portrait: THEODRIC, happy] He wrote a decent second act. Cowardly third, though. He has me weeping as Aurelia sinks—how tedious. When the sky shattered above my head, I did not weep, mortals. *I applauded.*

(In the wings, Celestine steps forward—pale, trembling, unable to tell a lie even under a dead king's gaze.)
[portrait: CELESTINE, shocked] ...You're not a memory. The Glass kept you whole.
[portrait: THEODRIC, smug] (glancing at her with faint amusement) A truth-speaker? Oh, charming—Maren's little songbirds still keep their feathers. Sing your third verse if you've the stomach for it, little bird.

(Then his golden eyes slide past the stage lights—ignoring Dorian, ignoring the panicked Wardguard, ignoring Voss trembling in the Meridian box—and settle squarely on the PC in the front row.)

[portrait: THEODRIC, happy] Ah. There sits my real audience.
[portrait: THEODRIC, smug] Enjoy your final rehearsals tomorrow, hollow one. Beat the tired old caretaker with the crystal arm, pick up his little silver hoop... and try not to bore me when the curtain rises for real.

(He snaps two fingers inside the glass. Every torch in the square dies at once. When the lanterns relight a heartbeat later, the stage mirror shows only terrified faces—and a single hairline golden crack shaped like a crown.)

[portrait: DORIAN, panic] ...Thirty years in the theatre, darling, and I have NEVER had a review from the title character.
```

---

### D. Ruin Route R7 — "Every Type and None" (The Hijack Climax, `GO_R_KNEEL`, Battle Barks & Defeat)

**Plugs into:** `story/12_RUIN_ROUTE.md` §R7 (lines 74–80), `plugins/Prismfall Core/012_Narrative_Data.rb:414–415`, `pbs/trainers.txt:15061–15196`, and `plugins/Prismfall Z-Power/005_ZPower_TrainerSpeech.rb` (or EBDX battle script).

#### D1. The Mirror Breach & Casting Voss Aside
```text
## R7 — Crownhaven Temple-Arena: The Hijack (Map 491, :PRISM_ARENA + Inverse)

(Valen lies spent on the flagstones. No Warden lifts the Sovereign's Crown; the PC bends and picks it up off the arena floor themselves. The instant your fingers touch the metal, the Arbiter Engine's eighteen pylons roar awake—not in Meridian blue, but in blinding, ancient Aurelian GOLD.)
(Every crystal panel encircling the arena turns into a mirror. Inside every pane stands the frozen Sun Court—and then, in unison, every reflection MOVES.)

(SFX: Resonant glass shattering in reverse—like bells chiming upward. A golden armored boot steps cleanly OUT of the central crystal pylon, trailing eighteen links of radiant, humming gold chain. Behind him, the sky over Crownhaven splits into inverted gold-and-violet glass.)

[portrait: VOSS, happy] (stumbling onto the arena floor in his Meridian Engine-harness, arms open, voice cracking with reverence)
Your Majesty! Look—look upon what House Aurel built for you! Eighteen locks, calibrated to the splinter—no crude iron, pure current! The god will have nowhere left to—

(King Aurelian does not even break stride. He stops three paces from Voss, looks down at the Engine-harness, taps one steel conduit with the back of a gilded knuckle—producing a hollow, tinny *clink*—and laughs once, dry as desert salt.)

[portrait: THEODRIC, smug] ...That's it?
[portrait: THEODRIC, deadpan] Three hundred years, and THIS tin-plated parlor trick is what House Aurel calls ambition?
[portrait: VOSS, shocked] My—my lord? It draws on all eighteen Imprints—I spent thirty years—
[portrait: THEODRIC, angry] You built a shopkeeper's tower on my drowned roof, wired a clerk's harness out of scraps dredged from my sewers, and crawled to my glass on your knees!
# [PATH A SHARED-NAME LINE — omit or swap to "my house's name" under Path B:]
[portrait: THEODRIC, smug] And they even gave you *my* name. How obscene. A base copper coin stamped with the sovereign's face.
[portrait: THEODRIC, neutral] Know your place, mongrel.

(With a flick of his wrist, two golden links of the Gilded Chain lash out from the crystal wall like whips—snapping clean through Voss's harness straps and hurling the CEO of Meridian twenty feet across the arena floor into the blazing perimeter of the Chain.)

[portrait: VOSS, panic] N-no—Your Majesty—I'm your HEIR—!
[portrait: THEODRIC, deadpan] A king has no heirs while he is standing in the room.
```

#### D2. `GO_R_KNEEL` ("Long Live the King") & Choice `:ruin_voss`
```text
(King Aurelian turns his back completely on Voss—already bored with him—and faces the Renegade PC across the humming keystone cradle. The inverted light of the eighteen Plates dances across his crown.)

[portrait: THEODRIC, smug] Now, then. The clerk is out of the way, and the sky is already listening.
[portrait: THEODRIC, neutral] You walked through twenty-three graves to open my door. A fine errand—better than any servant I left behind in the salt.
(He extends one open, gold-gauntleted hand—not an offer of partnership like Voss's, but a monarch granting an audience.)
[portrait: THEODRIC, smug] Kneel, mongrel. Set that little hoop at my feet, and I will be generous. I am always generous to things that know their station.

(At your shoulder, Giratina's presence coils cold and sharp behind the Black Case—a silent warning in the glass.)
CHOICE:
> Kneel.          --> Triggers Game Over GO_R_KNEEL ("Long Live the King")
> Refuse.         --> Continues to :ruin_voss & Hijack Battle

--- [IF "Kneel" -> GO_R_KNEEL] ---
(You drop to one knee and lay the Crown on the gold flagstones. King Aurelian's smile widens—neither cruel nor kind, merely satisfied, as a collector closes a velvet box.)
[portrait: THEODRIC, happy] Good. You see how simple the world is when things return to their rightful owner?
(Every mirror in Crownhaven breaks inward at once. Golden banners pour out of the glass. Three hundred years of drowned, starving Aurelia step back into the sunlight—and the Chain closes around your ribs like an armrest.)
[GAME OVER — GO_R_KNEEL "Long Live the King"]
Epitaph (for 012_Narrative_Data.rb:415):
"You knelt. The Aureate Kingdom stepped through the Glass, golden and unrepentant, and King Aurelian finished his sentence."
--- [END GO_R_KNEEL] ---

--- [IF "Refuse"] ---
(You don't kneel. You don't drop the Crown—you toss it casually aside onto the flagstones, where it rings once and goes still. Behind you, the Black Case hums with colorless emptiness.)
(For one heartbeat, Aurelian's golden brows lift. Then he bursts out laughing—a bright, terrifying sound that shakes the stadium glass.)

[portrait: THEODRIC, happy] Ha! Look at those eyes—not a shred of fear, not a whisper of devotion!
[portrait: THEODRIC, smug] Wait a moment. Before I crush you—your little benefactor is burning in my chain.

(Near the southern pylon, Voss hangs tangled in radiant golden links, smoke curling off his charcoal sleeves, reaching blindly toward the floor.)
[portrait: VOSS, crying] ...Help... please... it wasn't supposed to be like this...

CHOICE `:ruin_voss`:
> Pull Voss out of the Chain.  (:spare)
  (You step into the golden arcs—your colorless shard eating the burn—and haul Voss clear. He collapses onto the marble, breathing hard, every trace of Meridian's poised CEO gone forever.)
  [portrait: THEODRIC, smug] Mercy for a counterfeit? Hmph. Soft—or merely tidy. Still, stepping bare-handed through my Chain without flinching... you do have nerve.

> Leave him to the Chain.      (:abandon)
  (You don't even turn your head. The Chain tightens and swallows Voss into the golden glare of the Engine.)
  [portrait: THEODRIC, happy] Cold as glass. Not even a glance for the man who handed you your little badge case on the ferry! Good. Kings do not trip over broken tools.
```

#### D3. Pre-Battle Challenge (Direct Lead-In to B2W2 Gold VS Cut-In)
```text
(King Aurelian steps back onto the arena's center ring. Eighteen golden portals ripple open in the air behind his cape like mirrored shields; the arena's Prism field violently INVERTS—strengths flipping to weaknesses, the sky turning inverted gold.)

[portrait: THEODRIC, neutral] Let us see what three hundred years of mortal mediocrity has produced.
[portrait: THEODRIC, smug] You intend to *unmake* the sky? To erase the Plates I shed a kingdom's blood to collar?
[portrait: THEODRIC, happy] Audacious! Unforgivable! Utterly *magnificent*!
[portrait: THEODRIC, angry] Come, then, mongrel—stand before the First Sovereign of Aurelia and show me whether you deserve to look heaven in the eye!

(BGM DROP -> B2W2 VS CUT-IN [:gold theme, Graphics/EBDX/VS/THEODRIC.png] -> Trainer Battle: Gilded King Aurelian on :PRISM_ARENA [Inverse]!)
```

#### D4. Mid-Battle Barks (Gate of Gold / Escalating Respect Arc)

Designed to plug cleanly into `PrismfallSpeech` (`005_ZPower_TrainerSpeech.rb`) or EBDX's `pbTrainerSpeak` battle-script triggers:

| Trigger | Expression | Battle Bark (EBDX `pbTrainerSpeak`) | Narrative Purpose |
|---|---|---|---|
| **Lead — `Sunguard` (Golurk)** | `smug` | `"Witness the original, mongrel! That corroded toy Voss dredged from the silt was merely my doorstep's dust."` | Contrasts Aurelian's pristine Sun Court sentinel directly against Voss's Golurk `"Gilder"`! |
| **Send-out — `Regalia` (Aegislash)** | `smug` | `"A thousand blades have been forged since Aurelia sank—every one of them a crude copy of mine. Regalia, show them royal steel!"` | Pure *Fate* treasury superiority (`King's Shield` / royal blade-and-shield). |
| **Send-out — `Deluge` (Kyogre) or `Sunder` (Groudon)** *(first titan out)* | `happy` | `"Before I forged a chain for heaven, I leashed the sea and the earth simply to plow my gardens! Let us see if you survive the Year of Two Weathers!"` | Lore payoff linking Ch6 Ossuary murals + Ch14 Groudon Undersands directly into battle! |
| **Send-out — `Colossus` (Regigigas)** | `neutral` | `"Even a sleeping titan stands when its king commands. Survive five heartbeats, mongrel, and earn the privilege of being crushed."` | Turns `Slow Start` + `Protect` into a terrifying, aristocratic flex! |
| **First Plate Turn on `:PRISM_ARENA` (Inverse)** | `smug` | `"Even heaven's own laws twist backward beneath my heels! Adapt or shatter!"` | Highlights the Ruin-exclusive `:PRISM_ARENA` + Inverse double-mechanic. |
| **Ace Entry — `Gilt` (Gholdengo, Lv 100)** | `happy` | `"Hmph...! You tore through my court and my titans alike?! Splendid! Then drown in the entire treasury of Aurelia—Gilt, MAKE IT RAIN!"` | **The turning point:** amused contempt snaps into genuine, electric Gate-of-Babylon exhilaration! |
| **Ace Low HP (< 33%)** | `angry` → `happy` | `"Hahaha! YES! That cold, unflinching glare—neither kneeling nor begging! Strike harder, challenger! Show me the fang that dares bite a god!"` | Drops `"mongrel"` completely! Pure *FGO Babylonia* / *strange Fake* kingly euphoria! |

#### D5. `LoseText` & Post-Battle Recognition Scene (Right Before Arceus Descends)

- **Battle `LoseText` (82 chars — verified under the 85-char `pbs/trainers.txt` ceiling!):**
  > **`Ha...! Magnificent! Three hundred years, and at last a challenger. Go—end the sky.`**

- **Post-Battle Scene (Overworld / Cutscene immediately after victory):**
```text
(Gilt shatters into a blinding cascade of ancient Aurelian gold coins that melt into light before hitting the marble. King Aurelian staggers half a step—stops himself—and straightens his spine with effortless pride. Hairline cracks of white light race across his armor and his crown.)

[portrait: THEODRIC, happy] ...Ha. Haha... *hahaha!*
(He wipes a fleck of golden glass-dust from his cheek, looking at you with zero bitterness—only fierce, blazing satisfaction.)
[portrait: THEODRIC, smug] Do you know how long I stood behind that mirror, watching ten generations of sheep polish the bars of my daughter's cage?
[portrait: THEODRIC, neutral] Voss wanted a better furnace. Valen wanted another decade of quiet. Even my own Maren only wanted the sky to forgive her.
[portrait: THEODRIC, happy] And then you walk in with nothing in your chest—no prayer, no crown, no pity—and break my court to pieces just to reach the throat of heaven.

(Above the arena, the clouds rip apart. Blinding white Judgment light pours straight down through the inverted sky—not dragged by the Chain, but DESCENDING of its own terrifying will. The eighteen locks howl.)
(Aurelian's reflection begins to dissolve from the heels up into swirling flakes of gold leaf. He does not flinch. He raises one gleaming gauntlet in a brief, mocking, utterly sincere royal salute.)

[portrait: THEODRIC, smug] Your turn, sovereign of nothing.
[portrait: THEODRIC, happy] Do not dare lose after beating *me*. Make the Original One remember what mortal defiance looks like!

(With a final chime of shattering gold, King Aurelian Aurel disperses back into the Glass—leaving you alone beneath the descending light of Arceus.)
```

---

## Section 4: Validated Drop-In `pbs/trainer_types.txt`, `pbs/trainers.txt`, & `tools/trainer_gen/gen.py` Blocks

### 4.1 Validation Checklist (Verified Against `tools/validate_trainers.py` & `design/TRAINER_FIELD_PLAYBOOK.md`)
- **TrainerType ID:** Kept `[GILDED_THEODRIC]` (Option 1 zero-breakage); `Name = Gilded King` → in-battle display **`Gilded King Aurelian`** (or **`Gilded King Aurelius`** under Path B).
- **Exact Mechanical Parity (Zero Balance Regression):** Every Species, Level (`97–100` Standard / `98–100` Hard / `90–93` Casual), Move, Ability, Held Item, Nature, IV, and EV spread is **100% preserved** from the Round 2 Inverse-chart harness-validated team (`design/TRAINER_FIELD_PLAYBOOK.md:491–492`).
- **Treasury Nicknames (`<= 10` chars enforced by `validate_trainers.py:487`, zero collisions across all 19,210 lines of `pbs/trainers.txt`):**
  1. `GOLURK` → **`Sunguard`** (8 chars) — pristine Sun Court automaton (originals Voss's `"Gilder"`).
  2. `AEGISLASH` → **`Regalia`** (7 chars) — floating royal sword & shield (`King's Shield`).
  3. `KYOGRE` → **`Deluge`** (6 chars) — Year of Two Weathers, collared ocean titan.
  4. `GROUDON` → **`Sunder`** (6 chars) — Year of Two Weathers, collared earth titan.
  5. `REGIGIGAS` → **`Colossus`** (8 chars) — continent-towing titan bound in gold (`Crush Grip`).
  6. `GHOLDENGO` → **`Gilt`** (4 chars) — **preserved canonical ace nickname** (`design/BALANCE.md:217`).
- **`LoseText` length:** **82 characters** (within `pbs/trainers.txt`'s 85-char proven ceiling).
- **Items verified:** `FULLRESTORE`, `LIFEORB`, `WEAKNESSPOLICY`, `CHOICESPECS`, `LEFTOVERS`, `MAGICALSEED` (confirmed in `pbs/items_fields.txt:13`), `SITRUSBERRY`. No Mega Ring (`design/MEGA_EVOLUTION.md:388`: *"the rings came three centuries after him"*).

### 4.2 Drop-In `pbs/trainer_types.txt` Block (Replaces lines 420–426)

```ini
#-------------------------------
[GILDED_THEODRIC]
Name = Gilded King
Gender = Male
BaseMoney = 0
SkillLevel = 100
IntroBGM = Theme - Gilded King
BattleBGM = Battle - Gilded King
VictoryBGM = Battle victory leader
```
*(Note: Keep `BattleBGM = Battle Champion` until the dedicated `Battle - Gilded King` / `Theme - Gilded King` audio files from §5 are installed in `Audio/BGM/`, so Essentials never logs a missing-BGM warning.)*

### 4.3 Drop-In `tools/trainer_gen/gen.py` Block (Replaces lines 1112–1127)

```python
X("Hijack (Ruin) - Gilded King Aurelian, the Gilded Reflection", "GILDED_THEODRIC", "Aurelian", 0, 100,
  "Ha...! Magnificent! Three hundred years, and at last a challenger. Go—end the sky.", [
    # PRISM_ARENA "running Inverse" (story/12_RUIN_ROUTE; the event layers the inverted chart). Reviewed for it: under the
    # inverted chart Fighting and Ghost hit what they could not touch before (No Guard Dynamic Punch into Ghosts,
    # Close Combat into Psychic / Fairy / Flying, Poltergeist into Normal and Dark), and Kyogre + Groudon share one team
    # on purpose: the "Year of Two Weathers". Regigigas keeps Slow Start and Protect.
    # Treasury nicknames (all <= 10 chars, zero collisions): Sunguard (original of Voss's Gilder), Regalia (royal blade),
    # Deluge & Sunder (Year of Two Weathers), Colossus (bound titan), Gilt (canonical golden treasury ace).
    P("GOLURK", 97, "NOGUARD", "LIFEORB", "ADAMANT", "DYNAMICPUNCH,EARTHQUAKE,POLTERGEIST,STONEEDGE", "HA", nick="Sunguard",
      casual={"item": "SITRUSBERRY"}),
    P("AEGISLASH", 97, "STANCECHANGE", "WEAKNESSPOLICY", "QUIET", "KINGSSHIELD,SHADOWBALL,CLOSECOMBAT,SHADOWSNEAK", "BS",
      nick="Regalia"),
    P("KYOGRE", 98, "DRIZZLE", "CHOICESPECS", "MODEST", "WATERSPOUT,ORIGINPULSE,ICEBEAM,THUNDER", "S", nick="Deluge",
      casual={"item": "LEFTOVERS"}),
    P("GROUDON", 98, "DROUGHT", "LIFEORB", "ADAMANT", "PRECIPICEBLADES,STONEEDGE,FIREPUNCH,SWORDSDANCE", "A", nick="Sunder",
      casual={"item": "LEFTOVERS"}),
    P("REGIGIGAS", 99, "SLOWSTART", "LEFTOVERS", "ADAMANT", "CRUSHGRIP,KNOCKOFF,DRAINPUNCH,PROTECT", "HA", nick="Colossus"),
    # Magical Seed on the arena (+1 Sp. Atk, +1 Sp. Def) with Nasty Plot instead of being locked by Specs: the chart
    # flips under him, so he needs to change moves.
    P("GHOLDENGO", 100, "GOODASGOLD", "MAGICALSEED", "TIMID", "MAKEITRAIN,SHADOWBALL,FOCUSBLAST,NASTYPLOT", "S", nick="Gilt",
      casual={"item": "LEFTOVERS"}, hard={"item": "CHOICESPECS", "moves": "MAKEITRAIN,SHADOWBALL,FOCUSBLAST,TRICK"}),
])
```
*(Under Path B zero-collision swap: change `"Aurelian"` on line 1 above to `"Aurelius"`.)*

### 4.4 Drop-In `pbs/trainers.txt` Blocks — Standard (`0`), Hard (`100`), Easy/Casual (`200`) (Replaces lines 15061–15196)

```ini
# Hijack (Ruin) - Gilded King Aurelian, the Gilded Reflection
#-------------------------------
[GILDED_THEODRIC,Aurelian]
Items = FULLRESTORE,FULLRESTORE
LoseText = Ha...! Magnificent! Three hundred years, and at last a challenger. Go—end the sky.
Pokemon = GOLURK,97
    Name = Sunguard
    Moves = DYNAMICPUNCH,EARTHQUAKE,POLTERGEIST,STONEEDGE
    Ability = NOGUARD
    Item = LIFEORB
    Nature = ADAMANT
    IV = 31
Pokemon = AEGISLASH,97
    Name = Regalia
    Moves = KINGSSHIELD,SHADOWBALL,CLOSECOMBAT,SHADOWSNEAK
    Ability = STANCECHANGE
    Item = WEAKNESSPOLICY
    Nature = QUIET
    IV = 31
Pokemon = KYOGRE,98
    Name = Deluge
    Moves = WATERSPOUT,ORIGINPULSE,ICEBEAM,THUNDER
    Ability = DRIZZLE
    Item = CHOICESPECS
    Nature = MODEST
    IV = 31
Pokemon = GROUDON,98
    Name = Sunder
    Moves = PRECIPICEBLADES,STONEEDGE,FIREPUNCH,SWORDSDANCE
    Ability = DROUGHT
    Item = LIFEORB
    Nature = ADAMANT
    IV = 31
Pokemon = REGIGIGAS,99
    Name = Colossus
    Moves = CRUSHGRIP,KNOCKOFF,DRAINPUNCH,PROTECT
    Ability = SLOWSTART
    Item = LEFTOVERS
    Nature = ADAMANT
    IV = 31
Pokemon = GHOLDENGO,100
    Name = Gilt
    Moves = MAKEITRAIN,SHADOWBALL,FOCUSBLAST,NASTYPLOT
    Ability = GOODASGOLD
    Item = MAGICALSEED
    Nature = TIMID
    IV = 31
#-------------------------------
[GILDED_THEODRIC,Aurelian,100]
Items = FULLRESTORE,FULLRESTORE,FULLRESTORE
LoseText = Ha...! Magnificent! Three hundred years, and at last a challenger. Go—end the sky.
Pokemon = GOLURK,98
    Name = Sunguard
    Moves = DYNAMICPUNCH,EARTHQUAKE,POLTERGEIST,STONEEDGE
    Ability = NOGUARD
    Item = LIFEORB
    Nature = ADAMANT
    IV = 31
    EV = 252,252,0,0,0,4
Pokemon = AEGISLASH,98
    Name = Regalia
    Moves = KINGSSHIELD,SHADOWBALL,CLOSECOMBAT,SHADOWSNEAK
    Ability = STANCECHANGE
    Item = WEAKNESSPOLICY
    Nature = QUIET
    IV = 31
    EV = 252,0,4,0,252,0
Pokemon = KYOGRE,99
    Name = Deluge
    Moves = WATERSPOUT,ORIGINPULSE,ICEBEAM,THUNDER
    Ability = DRIZZLE
    Item = CHOICESPECS
    Nature = MODEST
    IV = 31
    EV = 4,0,0,252,252,0
Pokemon = GROUDON,99
    Name = Sunder
    Moves = PRECIPICEBLADES,STONEEDGE,FIREPUNCH,SWORDSDANCE
    Ability = DROUGHT
    Item = LIFEORB
    Nature = ADAMANT
    IV = 31
    EV = 4,252,0,252,0,0
Pokemon = REGIGIGAS,100
    Name = Colossus
    Moves = CRUSHGRIP,KNOCKOFF,DRAINPUNCH,PROTECT
    Ability = SLOWSTART
    Item = LEFTOVERS
    Nature = ADAMANT
    IV = 31
    EV = 252,252,0,0,0,4
Pokemon = GHOLDENGO,100
    Name = Gilt
    Moves = MAKEITRAIN,SHADOWBALL,FOCUSBLAST,TRICK
    Ability = GOODASGOLD
    Item = CHOICESPECS
    Nature = TIMID
    IV = 31
    EV = 4,0,0,252,252,0
#-------------------------------
[GILDED_THEODRIC,Aurelian,200]
Items = FULLRESTORE
LoseText = Ha...! Magnificent! Three hundred years, and at last a challenger. Go—end the sky.
Pokemon = GOLURK,90
    Name = Sunguard
    Moves = DYNAMICPUNCH,EARTHQUAKE,POLTERGEIST,STONEEDGE
    Ability = NOGUARD
    Item = SITRUSBERRY
    Nature = ADAMANT
    IV = 20
    EV = 0
Pokemon = AEGISLASH,90
    Name = Regalia
    Moves = KINGSSHIELD,SHADOWBALL,CLOSECOMBAT,SHADOWSNEAK
    Ability = STANCECHANGE
    Item = WEAKNESSPOLICY
    Nature = QUIET
    IV = 20
    EV = 0
Pokemon = KYOGRE,91
    Name = Deluge
    Moves = WATERSPOUT,ORIGINPULSE,ICEBEAM,THUNDER
    Ability = DRIZZLE
    Item = LEFTOVERS
    Nature = MODEST
    IV = 20
    EV = 0
Pokemon = GROUDON,91
    Name = Sunder
    Moves = PRECIPICEBLADES,STONEEDGE,FIREPUNCH,SWORDSDANCE
    Ability = DROUGHT
    Item = LEFTOVERS
    Nature = ADAMANT
    IV = 20
    EV = 0
Pokemon = REGIGIGAS,92
    Name = Colossus
    Moves = CRUSHGRIP,KNOCKOFF,DRAINPUNCH,PROTECT
    Ability = SLOWSTART
    Item = LEFTOVERS
    Nature = ADAMANT
    IV = 20
    EV = 0
Pokemon = GHOLDENGO,93
    Name = Gilt
    Moves = MAKEITRAIN,SHADOWBALL,FOCUSBLAST,NASTYPLOT
    Ability = GOODASGOLD
    Item = LEFTOVERS
    Nature = TIMID
    IV = 20
    EV = 0
```
*(Under Path B zero-collision swap: replace `[GILDED_THEODRIC,Aurelian` with `[GILDED_THEODRIC,Aurelius` on all three headers.)*

---

## Section 5: Audio, Visual & Presentation Synergy

### 5.1 Leveraging Existing High-Craft Art Assets (Visually Inspected)
All 16 art files already exist in `graphics/` and fit the Archer Gilgamesh sovereign aesthetic seamlessly — they only needed proper engine registration:
- **Animated Battle Strip (`graphics/Trainers/GILDED_THEODRIC.png`):** Black-and-gold armored surcoat, crimson-lined mantle, jagged crown, golden chain draped over his chest; one-shot entry animation lifts a gleaming gilded Poké Ball in an imperious, relaxed palm — pure regal dominance.
- **B2W2 VS Cut-In (`graphics/EBDX/VS/THEODRIC.png`):** Crisp side-profile gold-armored bust cradling a golden Poké Ball with calm disdain. Wiring `"THEODRIC" => :gold` in `010_Bridge_VersusIntro.rb` gives him a **blazing golden radial warp tunnel and golden opponent banner** (contrasting sharply against Voss's cold corporate `:grey` theme in line 52!).
- **12 Dialogue Portraits (`graphics/Portraits/THEODRIC_*.png`):** Visually verified `THEODRIC_smug.png` (effortless half-smile, lidded golden eyes), `THEODRIC_happy.png` (open, dangerous sovereign grin — ideal for his mid-battle exhilaration!), `THEODRIC_angry.png` (imperial glare when casting Voss aside), and `THEODRIC_neutral.png` (cool appraisal). Registering `:THEODRIC` in `014_Portraits.rb` unlocks all 12 expressions immediately.

### 5.2 Audio & Musical Aura — Imperial Brass & Golden Majesty
Currently `design/AUDIO.md:222` shares Voss's BGM (`Battle - Voss`), while `design/AUDIO_SOUNDTRACK_PLAN.md:238` assigns **#133** (`Pokémon Rejuvenation — Battle! Of Beasts and Kingdoms` by GlitchxCity) and `gemini_recommends/2026-11-23_anime-ost-situational-bgm/PROPOSAL.md:103` proposes **#15** (*Frieren* — **`Zoltraak`** by Evan Call).

With the Archer Gilgamesh upgrade, Aurelian should **never** share Voss's corporate synth-metal theme (`Out of My Hands` / `Battle - Voss`). Give him an unmistakably **imperial brass + baroque strings + golden majesty** musical identity:

| Audio Slot | Primary Recommendation (Anime / Fate Synergy) | Existing Plan / Non-Anime Alt | Musical & Staging Notes |
|---|---|---|---|
| **Walk-In / Mirror Appearance Cue (`IntroBGM`: `Theme - Gilded King`)** | ***Fate/Zero* — "The King of Heroes" (*Eiyū-Ō*)** (Yuki Kajiura) *or* ***Fate/stay night [UBW]* — "Rule of the King"** (Hideyuki Fukasawa) | *Hunter x Hunter* — `Restriction and Pledge` (R3 cold glass dread) → hard-cut to golden brass flourish on R7 breach | Slow, arrogant brass fanfare & regal harpsichord/bell chimes as Aurelian strolls out of the crystal walls and flicks Voss aside. Immediate *aura* contrast against Voss's quiet corporate restraint. |
| **R7 Hijack Battle (`BattleBGM`: `Battle - Gilded King`)** | **Tier 1 (Pure Gilgamesh):** ***Fate/Grand Order: Babylonia* — "Cosmic Air ~ Grand Battle" / *Fate/stay night [UBW]* — "Cosmic Air" (Extended)** *(blazing imperial horns, relentless golden pomp, zero lyrics)*<br>**Tier 2 (Already Queued in Anime OST Proposal #15):** ***Frieren* — "Zoltraak"** (Evan Call — thunderous imperial brass & baroque strings) | **Existing Plan #133:** *Pokémon Rejuvenation* — `Battle! Of Beasts and Kingdoms` (GlitchxCity) | Loop drop timed straight to the B2W2 `:gold` VS screen shatter! If using `Cosmic Air` or `Zoltraak`, the soaring brass hits right as `:PRISM_ARENA` inverts and `Sunguard` Golurk materializes. |
| **Voice Blip SE (`SE/Voice - Gilded King.ogg`)** | Rich baritone resonance (~15–20% deeper, slower cadence, faint crystalline cathedral reverb tail vs `audio/gemini_cc0/SE/Voice - Voss.ogg`) | Reuse pitched-down `Voice - Voss.ogg` (−3 semitones + subtle metallic shimmer) | Subtly implies Voss's voice is a thinner, modern echo of his ancestor's royal timbre! |
| **Signature Cutscene SFX** | Reverse-glass chime (`Mirror Breach`) + heavy metallic chain clink (`Gilded Chain` whip) + cascading gold-coin shimmer (when `Gilt` enters and on `Make It Rain`) | Stock Essentials `Glass Break` + `Metal Claw` / `Pay Day` chime layered | Gives every appearance behind glass (R3 Sun Court, R6 Night of Masques mirror, R7 Arena Breach) a unified Pavlovian audio signature. |

---

## Summary of Immediate Decisions Needed from Creator Reuben / Claude
1. **Name Collision Ruling (Section 1 Warning):**
   - **Path A (Keep `Gilded King Aurelian`):** Shared ancestral name with `Aurelian Voss` (`Gilded Heir Aurelian`), weaponized into a lethal Gilgamesh "counterfeit wearing my name" beat + 1-line `025_CharsetAliases.rb` guard.
   - **Path B (Switch to `Gilded King Aurelius`):** True zero collision (`0` repo matches), exact Latin patronymic (*Aurelian* = "descendant of *Aurelius*"), 1-word swap on the King's blocks.
2. **Asset Strategy:** Adopt **Option 1** (keep internal `:GILDED_THEODRIC` & 16 existing PNG filenames + add the 3 missing plugin registrations in `010_Bridge_VersusIntro.rb`, `014_Portraits.rb`, `025_CharsetAliases.rb`) for zero breakage and immediate playability.
3. **Battle BGM Pick:** Confirm *Cosmic Air* (*Fate* brass perfection) vs *Zoltraak* (*Frieren*, already in Anime OST Proposal #15) vs *Of Beasts and Kingdoms* (Rejuvenation #133).
