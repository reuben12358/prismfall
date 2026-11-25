# Pokémon Prismfall — Act III–V, Post-Game & Ruin Route Playscript & Restrained Rejuv Expressions Spec (Chapters 10–21, Fallmorn & Gilded King)

**Date:** 2026-11-24  
**Scope:** Pillars 4 & 5 — *Play-Style Multi-Box Dialogue* + *Restrained Rejuv-Style Expressions* across all **14 late-game script files** (`Chapters 10–21`, `Post-Game "Fallmorn"`, and `Ruin Route R1–R7`, plus Interludes III & IV).  
**Location:** `gemini_recommends/2026-11-24_playscript-dialogue-and-expressions/act3_5/`  
**Repo Safety:** Zero edits to canonical `story/*.md`, `graphics/`, `mapgen/`, or `act1_2/`. All 14 converted files are drop-in recommendations ready for Claude/Reuben merge review.  
**Interactive Studio:** `/tmp/prismfall_playscript_act3_5_studio.html` (6 iconic climax playable Before-vs-After scenes with real `96×96` static `0px`-bob portraits from `graphics/Portraits/`).

---

## 1. Design Laws Enforced

### Pillar 4 — Play, Not Book (Multi-Box Theatrical Pacing)
1. **1–2 Line RPG Boxes (`<= ~85 chars` per box):** Dense literary monologue blocks (originally up to **`309` chars** per single box in `story/38_SCRIPT_CH19.md` and **`289` chars** in `story/30_SCRIPT_CH11.md`) are broken into crisp, stage-paced 1–2 line dialogue boxes (`median 86 → 44 chars`, `p90 169 → 65 chars`), punctuated by natural pauses (`...`), cut-ins (`—`), and reactive timing.
2. **100% Canonical Fidelity (`0` Dropped Tokens):** Automated diffing across all 14 scripts confirms **zero** dropped switches (`S###`), variables (`V###`), narrative choice keys (`pf_choose`), Game Overs (`GO_*`), battle directives (`BATTLE:`), Key Items, EventMons, Quest Log updates, or Map/Trainer appendix rows.
3. **Zero Rewritten Character Voices:** Every character's exact cadence is preserved — Valen's quiet dignity, Voss's clinical urbanity, Nyx's razor-edged charm, Magnus's watchmaker brevity, Wenlow's bright clumsiness turning still in the doorway, and Aurelius's imperial stillness.

### Pillar 5 — Restrained Rejuv-Style Expressions (`014_Portraits.rb` & `018_ExpressiveDialogue.rb` v2)
1. **70–80%+ Neutral / Held Portrait Discipline (`82.6%` overall):** `[portrait: CAST_ID, expr]` opens a speaker's turn or marks a **genuinely earned emotional turn** (`349` non-neutral shifts across `2,007` spoken boxes = **`1` shift per `5.8` boxes**). Intervening boxes in the same beat use `[name: Speaker]` to hold the anchored `96×96` portrait with **`0px` vertical bob**.
2. **Ultra-Rare Overworld Emotes (`0–2` per scene):** `[emote: dots|exclaim|question]` appears only **`59` times** across `2,007` dialogue boxes (**`2.9%`**) — and **strictly `0` times** inside zero-joke grief windows (Operation Clear Air through Wenlow's Stand in Interlude IV, Morwen's Cathedral echo, and Valen's quiet departure).
3. **100% Verified Portrait Asset Parity (`0` Invalid Portraits):** Every `[portrait: SPEAKER, expr]` and `\pf[PLAYER, expr]` across all 14 files resolves to an existing `graphics/Portraits/<ID>_<expr>.png` (`0` missing IDs, `0` invalid expressions).

### Source-Script Portrait Bugs Fixed During Conversion
Auditing `story/30..38*.md` against `plugins/Prismfall Cutscenes/014_Portraits.rb` (`CAST`) and `graphics/Portraits/` caught and repaired **4 canonical asset mismatches**:
- **Ch14 (`33_SCRIPT_CH14.md`):** Fixed invalid `[portrait: LARCH, worried]` → `[portrait: LARCH, sad]` (`worried` is not in the 11-expression sheet).
- **Ch15 (`34_SCRIPT_CH15.md`) & Ch19 (`38_SCRIPT_CH19.md`):** Wired Dominar Hrothgar to his verified 11-expression portrait sheet **`[portrait: HROTHGAR, neutral]`** (retaining `[name: Dominar]` on continuation beats); source scripts had marked him plain pending art, which is already complete on disk.
- **Ch16 (`35_SCRIPT_CH16.md`):** Fixed invalid `[portrait: SALLOW, neutral]` → canonical `CAST` ID **`[portrait: RENATA, neutral]`** (Councillor Renata Sallow's sheet is `RENATA_*.png`, 11 expressions).
- **Ch17 (`36_SCRIPT_CH17.md`):** Fixed invalid `[portrait: SAHAR, worried]` → `[portrait: SAHAR, sad]` (retaining `[portrait: SAHAR, panic]` on the earned Gilded Throne warning).

---

## 2. Act III–V, Post-Game & Ruin Quantitative Transformation Scorecard (All 14 Files)

All metrics below are computed directly from fenced script blocks comparing `story/*.md` (**Before**) against `act3_5/*.md` (**After**) via automated Python audit.

| Script File | Arc / Chapters | Status | Boxes (`Before → After`) | Median Chars | p90 Chars | Max Chars | `<= 85` Chars | `[portrait:]` / `\pf` | Earned Shifts | Restraint (`neutral`+hold) | `[emote:]` | Verified Cast | Errors (`Port / Tok`) |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `28_SCRIPT_CH10.md` | Ch10 — Verdance, Bride Grove, Ogerpon, Gym 9 | Pre-existing | `166 → 324` (`+158`) | `90 → 50` | `177 → 69` | `241 → 141`* | `98.8%` | `82` | `52` | `84.0%` | `10` | `8` | `0 / 0` |
| `30_SCRIPT_CH11.md` | Ch11 — Rimeholt, The Thaw, Kyogre, Gym 10 | **Converted** | `121 → 266` (`+145`) | `90 → 46` | `194 → 65` | `289 → 75` | **`100.0%`** | `70` | `42` | **`84.2%`** | `7` | `8` | `0 / 0` |
| `31_SCRIPT_CH12.md` | Ch12 — Skyreach, Dead Letters, K5, Int. III | **Converted** | `77 → 162` (`+85`) | `88 → 45` | `182 → 67` | `223 → 84` | **`100.0%`** | `60` | `31` | **`80.9%`** | `5` | `5` | `0 / 0` |
| `32_SCRIPT_CH13.md` | Ch13 — Lucent, Glass Court, Sable, Voss, Gym 12 | Pre-existing | `73 → 168` (`+95`) | `85 → 41` | `162 → 63` | `257 → 81` | **`100.0%`** | `49` | `25` | `85.1%` | `13` | `10` | `0 / 0` |
| `33_SCRIPT_CH14.md` | Ch14 — Cragholm, Deep Seams, Groudon, Gym 13 | **Converted** | `86 → 173` (`+87`) | `93 → 47` | `176 → 65` | `268 → 76` | **`100.0%`** | `69` | `37` | **`78.6%`** | `4` | `11` | `0 / 0` |
| `34_SCRIPT_CH15.md` | Ch15 — Gravenmoor, Cathedral Echo, K6, Giratina | **Converted** | `64 → 126` (`+62`) | `82 → 40` | `146 → 63` | `245 → 74` | **`100.0%`** | `43` | `21` | **`83.3%`** | `2` | `9` | `0 / 0` |
| `35_SCRIPT_CH16.md` | Ch16 — Cogsworth, Zekrom, Magnus, Int. IV Wenlow | **Converted** | `56 → 118` (`+62`) | `94 → 42` | `167 → 63` | `210 → 73` | **`100.0%`** | `33` | `13` | **`89.0%`** | `3` | `6` | `0 / 0` |
| `36_SCRIPT_CH17.md` | Ch17 — Underveil, Sun Court, PC 4th Line, Voss | **Converted** | `67 → 157` (`+90`) | `105 → 45` | `183 → 60` | `240 → 74` | **`100.0%`** | `56` | `29` | **`81.5%`** | `3` | `10` | `0 / 0` |
| `37_SCRIPT_CH18.md` | Ch18 — Lightless Deep, Pecharunt, Gloaming, K7 | **Converted** | `48 → 92` (`+44`) | `84 → 43` | `167 → 60` | `230 → 68` | **`100.0%`** | `29` | `12` | **`87.0%`** | `1` | `6` | `0 / 0` |
| `38_SCRIPT_CH19.md` | Ch19 — Wyrmrest Oath, Glass Dunes War, Gym 18 | **Converted** | `49 → 93` (`+44`) | `77 → 44` | `174 → 63` | `309 → 70` | **`100.0%`** | `35` | `12` | **`87.1%`** | `2` | `6` | `0 / 0` |
| `39_SCRIPT_CH20.md` | Ch20 — Festival of Champions, Semifinals, K8 | Pre-existing | `56 → 128` (`+72`) | `80 → 36` | `150 → 59` | `218 → 72` | **`100.0%`** | `47` | `26` | `79.7%` | `4` | `21` | `0 / 0` |
| `40_SCRIPT_CH21.md` | Ch21 — Sovereign, Engine Hijack, Valen & Arceus | Pre-existing | `32 → 53` (`+21`) | `37 → 27` | `73 → 47` | `167 → 64` | **`100.0%`** | `28` | `11` | `79.2%` | `2` | `11` | `0 / 0` |
| `41_SCRIPT_POSTGAME.md` | Post-Game — *"Fallmorn"* (Epilogue & Lighthouse) | Pre-existing | `15 → 38` (`+23`) | `98 → 38` | `186 → 60` | `214 → 68` | **`100.0%`** | `12` | `7` | `81.6%` | `1` | `5` | `0 / 0` |
| `42_SCRIPT_RUIN_KING.md` | Ruin Route R1–R7 — *"Every Type and None"* | Pre-existing | `57 → 109` (`+52`) | `76 → 49` | `143 → 71` | `168 → 78` | **`100.0%`** | `37` | `31` | `71.6%` | `2` | `5` | `0 / 0` |
| **Subtotal (New 8)** | **Ch11, 12, 14, 15, 16, 17, 18, 19** | **Complete** | **`568 → 1,187` (`+619`)** | **`90 → 44`** | **`176 → 64`** | **`309 → 84`** | **`100.0%`** *(was `46.7%`)* | **`395`** | **`197`** (`1/6.0`) | **`83.4%`** | **`27`** (`2.3%`) | **`36`** | **`0 / 0`** |
| **Total Act III–V (14)** | **Ch10–Ch21 + Post-Game + Ruin Route** | **Complete** | **`967 → 2,007` (`+1,040`)** | **`86 → 44`** | **`169 → 65`** | **`309 → 141`** | **`99.8%`** *(was `49.7%`)* | **`650`** | **`349`** (`1/5.8`) | **`82.6%`** | **`59`** (`2.9%`) | **`47`** | **`0 / 0`** |

- **Walls of text (`> 120` chars per single box) eliminated:** `270` in `story/` → **`1`** across all 14 files (**`0`** across all 8 newly converted files; the sole remaining `141`-char line is in pre-existing `28_SCRIPT_CH10.md`).

---

## 3. Expression & Emote Restraint Distribution (All 14 Files)

### Expression Distribution (`650` `[portrait:]` + `\pf` tags across `2,007` spoken boxes)
| Expression | Count | Share of Portrait Tags | Editorial Role in Act III–V |
|---|---:|---:|---|
| `neutral` | `301` | `46.3%` | Composed gravity: Magnus, Valen, Voss, Corvin, Sigrun, Hrothgar, Wenlow's quiet stand |
| `sad` | `109` | `16.8%` | Earned late-game weight: Morwen's echo, Nyx's Calloway door, Brann's confession, Rook after Mirefen |
| `happy` | `77` | `11.8%` | Warmth & contrast: Wenlow's evening rounds, Sahar's barge excitement, Sigrun's first laugh, Fallmorn |
| `angry` | `55` | `8.5%` | Sharp confrontation: Kestrel at K5–K7, Nyx on Underveil, Mother Gutter at the barricade, Marchetti |
| `smug` | `35` | `5.4%` | Controlled poise: Celestine's riddles, Kassan's armistice, Nyx's bargains, Aurelius (`REFLECTION`) |
| `shocked` | `30` | `4.6%` | Major revelations: Rook reading `UNIMPRINTED-01`, Nyx at the Sun Court cradle, Sigrun at the oath |
| `panic` | `18` | `2.8%` | True physical crisis only: Anja at Kyogre, Rook at the Core Breach countdown, Sahar at the Gilded Throne |
| `deadpan` | `14` | `2.2%` | Dry understatement: Edda, Sigrun, Nyx refusing a bargain, Larch |
| `crying` | `11` | `1.7%` | Ultra-rare breaking points only (never spammed) |

### Overworld Emote Distribution (`59` `[emote:]` tags across `2,007` boxes = `2.9%`)
- `dots`: `31` · `exclaim`: `20` · `question`: `8`.
- **Zero emotes** inside Wenlow's Stand (`35_SCRIPT_CH16.md` Interlude IV), Operation Clear Air broadcast, Morwen's Cathedral echo (`34_SCRIPT_CH15.md`), and Valen's quiet departure (`40_SCRIPT_CH21.md`).

---

## 4. Verified Portrait Cast Inventory (`47` Unique Verified Sheets Across Act III–V)

Every cast ID below was verified directly against `graphics/Portraits/<ID>_<expr>.png`:

`ANJA, BASTIAN, BRANN, CALLA, CELESTINE, CORVIN, DASK, DORIAN, EDDA, EIRIK, GUTTER, HESPER, HROTHGAR, ILSA, JUNO, KAITO, KASSAN, KESTREL, KROLL, LARCH, MAELIS, MAGNUS, MARCHETTI, MARISOL, MORWEN, NYX, ODESSA, OKORO, PIP, PLAYER (PLAYER_A/PLAYER_B), QUENT, REFLECTION, RENATA, ROOK, ROWAN, SAHAR, SIGRUN, TAMSIN, TEO, THEODRIC, THISTLE, VALEN, VESPER, VOSS, WENLOW, WICK, YSOLDE`

Plain NPCs without portrait sheets (`Tage`, `Bryn`, `Zainab`, `Kit`, `Elder Ossa`, `Hallgerd`, `Tavi`, `Thornguard Captain`, `Officer Tull`, `Lieutenant`, `Courier`, `Gate-guard`, `Rider`, `Worker`, `Sled-runner`, `Caravan-mother`) remain strictly `[name: ...]`.

---

## 5. Chapter-by-Chapter Theatrical Highlights (8 Newly Converted Scripts)

- **Ch11 (`30_SCRIPT_CH11.md` — *The Thaw*):** Anja's terse ice-ledger rhythm, Kyogre's harbour breath (`[emote: exclaim]` on `"That's not a Pokémon—that's WEATHER."`), the Ebbmouth Strike war choice, and Anchorhold's dusk tension.
- **Ch12 (`31_SCRIPT_CH12.md` — *Dead Letters*):** Skyreach's high-altitude mailroom cadence, Larch's dead-letter reveal (`"I."`), the Meridian Raid, K5's sharp rivalry turn, Interlude III, and Conductors' Causeway.
- **Ch14 (`33_SCRIPT_CH14.md` — *The Deep Seams*):** Cragholm's cavern acoustics, Bastian's eye-witness account, Ring-Day's quiet reveal, Badge Case telemetry choice (`:ch14_telemetry`), Duneholt, and Primal Groudon. Fixed `LARCH, worried` → `sad`.
- **Ch15 (`34_SCRIPT_CH15.md` — *The Hollow Cathedral*):** War Convoy (`:war_convoy`), Vane Hall's hush, **Cathedral Echo CE-1** (Morwen's translucent `neutral`/`sad` replay of AF 290, zero jokes/emotes), K6, Morwen's Ring, War 3 Prisoner (`HROTHGAR` wired), Giratina, and the Hush.
- **Ch16 (`35_SCRIPT_CH16.md` — *Clear Air*):** Rook off-camera in the canteen, Magnus's clipped watchmaker timing (`"Within tolerance. Yours, not mine."`), Casting Floor tag fight, Drafting Vault (`UNIMPRINTED-01`), Zekrom's cable break, `RENATA` wired for Councillor Sallow, Operation Clear Air broadcast, and **Interlude IV — Wenlow's Stand** (strictly held `WENLOW, neutral`, zero emotes, cutting straight to black on `"You have to —"`).
- **Ch17 (`36_SCRIPT_CH17.md` — *The Drowned Crown*):** Mother Gutter's barricade (`GUTTER`), Nyx's Underveil independence speech, Brann's Accord Archive / Sump Docks confessions, **the Sun Court reveal** (Nyx's `"Oh, darling. You're the missing piece."`, Sahar reading the Legend Plate inscription, the PC's 4th authored line `\pf[PLAYER,neutral]`), **Voss naming House Aurel**, Ysolde's forty-one lanterns, and Edda's Act IV closer. Fixed `SAHAR, worried` → `sad`.
- **Ch18 (`37_SCRIPT_CH18.md` — *Once Upon a Time*):** Corvin's flat, mask-on restraint at the Throat, Mother Gutter's eerie Pecharunt thralldom and three-century awakening, Celestine's truth-law entrance, the envoys (`:war_legend`), the complete **Hymn of Return** (`"It says walker."`), and K7 under the Great Tree roots with Morwen's Ring.
- **Ch19 (`38_SCRIPT_CH19.md` — *The Last Gate*):** Sigrun's quiet confession in the Wyrmscar Rift, the five-choice Draco brazier oath (`:ch19_oath` / `GO_LIARS_PYRE`), the Battle of the Glass Dunes (`WAR-1`), the truce and Observers' Mesa reveal, **Dominar Hrothgar** wired with `HROTHGAR`, Reshiram bowing to Sigrun, Gym 18's full eighteen-tone chord, and Crownhaven's gate.

---

## 6. Interactive Climax Theater Studio Verification & Claude Adoption Guide

`/tmp/prismfall_playscript_act3_5_studio.html` renders **6 iconic Act III–V & Ruin climax scenes** side-by-side (**Before: Book Wall-of-Text** vs. **After: Playscript Multi-Box + Restrained Rejuv Expressions**) directly from `story/*.md` and `act3_5/*.md`:
1. **Ch10 — Bride Grove (`28_SCRIPT_CH10.md`)** — Juno's trial, Ogerpon & the Bride Tree
2. **Ch13 — Glass Court Tribunal (`32_SCRIPT_CH13.md`)** — Rowan's tribunal, Sable exposed & Voss broadcast
3. **Ch16 — Quiet Ward Doorway (`35_SCRIPT_CH16.md`)** — Interlude IV: Wenlow's Stand (zero-emote restraint showcase)
4. **Ch17 — Drowned Aurelia Sun Court (`36_SCRIPT_CH17.md`)** — Keystone cradle, Nyx `"missing piece"`, PC's 4th line & Voss reveal
5. **Ch21 — Prismatic Apex Finale (`40_SCRIPT_CH21.md`)** — Valen holds the Ring, Arceus speaks & `:ch21_final`
6. **Ruin R7 — Gilded Throne Sanctuary (`42_SCRIPT_RUIN_KING.md`)** — Mirror breach, Voss flung aside & Gilded King Aurelius

### SHA-256 Manifest (`act3_5/*.md`)
| File | SHA-256 (12-char) | Bytes |
|---|---|---:|
| `28_SCRIPT_CH10.md` | `d91173056c24` | `65,017` |
| `30_SCRIPT_CH11.md` | `af849c1e6d82` | `69,105` |
| `31_SCRIPT_CH12.md` | `b92137b2d9dc` | `43,636` |
| `32_SCRIPT_CH13.md` | `8e3f37d9f98b` | `42,859` |
| `33_SCRIPT_CH14.md` | `fd9ecdee6554` | `55,537` |
| `34_SCRIPT_CH15.md` | `5de6ab3e8a32` | `50,530` |
| `35_SCRIPT_CH16.md` | `25dde934e6db` | `40,970` |
| `36_SCRIPT_CH17.md` | `c726e8869361` | `42,122` |
| `37_SCRIPT_CH18.md` | `6d606ccf51e1` | `32,568` |
| `38_SCRIPT_CH19.md` | `ec495efd719a` | `38,523` |
| `39_SCRIPT_CH20.md` | `fcefa6761796` | `39,191` |
| `40_SCRIPT_CH21.md` | `0a1bd03cde9b` | `26,313` |
| `41_SCRIPT_POSTGAME.md` | `09d7095cd901` | `17,033` |
| `42_SCRIPT_RUIN_KING.md` | `aff5b23c57b7` | `21,314` |

### Drop-In Adoption for Claude (Post-Review)
Once Reuben signs off via `/tmp/prismfall_playscript_act3_5_studio.html`, all 14 scripts can replace their `story/` counterparts 1:1 with zero mechanical diff to flags, variables, PBS rosters, or map specs:
```bash
cp gemini_recommends/2026-11-24_playscript-dialogue-and-expressions/act3_5/*.md story/
```
All portrait tags target `plugins/Prismfall Cutscenes/014_Portraits.rb` and `018_ExpressiveDialogue.rb` v2 (`0px` anchored portrait stage).
