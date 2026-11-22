# Acts III–V, War Arc, Ruin Route, Scripts Ch8/11–13 & Late-Game Boss Audit

- **Date:** 2026-11-22
- **Author:** Gemini (Story, Continuity & Late-Game Systems Audit)
- **Scope:** `story/06_ACT_III.md`–`14_WAR_AND_BLESSING.md`, `story/22_SCRIPT_CH8.md`, `story/29_SCRIPT_CH8.md`–`32_SCRIPT_CH13.md`, `story/03_CAST.md`, `design/{FLAGS,NARRATIVE_KEYS,BOSSES,BADGE_TIERS,BALANCE,CAMEOS,GYM_PUZZLES,TRIALS_QUESTS,WALKTHROUGH,WORLD_MAP}.md`, `pbs/{trainers,encounters,encounters_badgetiers}.txt`, and `plugins/Prismfall {Core,Bosses,Cutscenes,Field Effects,Mega,Z-Power,Trials}/`.
- **Deduplication:** Cross-checked against `gemini_recommends/REVIEW.md` and all `2026-11-21_*` proposals (`codex-proofread-and-critique`, `boss-cheese-and-rev16-gates`, `story-continuity-and-road2-levels`, `ruby-plugin-p0-bugfixes`). Every item below is **newly surfaced and line-verified** (with two explicit residual doc-sync notes where code was already fixed).
- **Overall Assessment:** The newly written Ch8 & Ch11–13 scripts (`29`–`32`) maintain Ch4–10's voice discipline, use **100% valid `CAST` IDs & portrait expressions**, and Badges 9–18 feature a clean, monotonic level curve (`47 → 100`) with full Standard/Hard/Casual parity. Below are the concrete code/switch bugs, hard lore/timeline breaks, PBS/boss gaps, and surgical Acts III–V pacing opportunities.

---

## 1. P0 — Live Plugin, Switch & Boss Mechanics Bugs

### 1.1 Switch `S193 RUIN_ROUTE_ACTIVE` Is Never Set Anywhere by Core
- **Spec:** `design/FLAGS.md:188` — `S193 | RUIN_ROUTE_ACTIVE | Event-page mirror of Core's ruin_route (Core-written, read-only)`.
- **Bug:**
  - `plugins/Prismfall Core/012_Narrative_Data.rb:334-347` (`MIRROR_SWITCHES`) only mirrors `221..232`; `193` is omitted.
  - `plugins/Prismfall Core/016_Ledger.rb:140-143` (`start_ruin_route`) sets `Prismfall.state.narrative[:ruin_route] = true` and triggers `:prismfall_ruin_route_started`, without touching `$game_switches[193]` or calling `Prismfall.sync_mirrors`.
- **Impact:** Every RPG Maker map/NPC event page gated on Switch `193` silently stays inactive on the Ruin Route.
- **Suggested Fix:**
  1. Add `193 => "ruin_route"` to `MIRROR_SWITCHES` (`012_Narrative_Data.rb:334-347`).
  2. Call `Prismfall.sync_mirrors` inside `start_ruin_route` (`016_Ledger.rb:142`).
  3. Update the stale `# design/FLAGS.md S221-S228` comments in `012_Narrative_Data.rb:332` and `013_Narrative_State.rb:91`.

### 1.2 `:KYOGRE_WEATHER` Does Not Abort After Round 1 (`101_Boss_Kyogre.rb:45-61`)
- **Spec:** `story/30_SCRIPT_CH11.md:332` (`"the battle ends after one round whatever happens"`) and `story/10_CHOICES_ENDINGS.md:331` (`"one Primal-rain Origin Pulse"`).
- **Bug:** `:KYOGRE_WEATHER` registers `:bars => { :default => 5 }` with no turn-1 termination hook, forcing the player through a slow 6-Pokémon wipe (or an infinite Sturdy/Focus Sash/Water Absorb stall).
- **Suggested Fix:** Add an end-of-round-1 abort (`:end_battle => 2`) after Kyogre's first attack. *(Same file: `design/BALANCE.md:560-573` also notes `:KYOGRE_ISENMAR` is live-playtest overtuned at cap 55 due to 3 bars + Calm Mind + Aqua Ring + Ice Beam on `:FROZEN_LAKE`, and line `28` has the "shard in your pocket" lore error in §2.1 below.)*

### 1.3 Seven Unregistered Late-Game Multi-Bar Bosses in `plugins/Prismfall Bosses/`
Only 6 boss registration files exist (`101_Kyogre`–`106_WarLegends`). Missing registrations required by Acts III–V & Ruin Route:
1. **Ch10 Loyal Three** (Okidogi, Munkidori, Fezandipiti — triple multi-bar boss, `story/06_ACT_III.md:45`).
2. **Ch14 Groudon** (Duneholt Undersands `783` — multi-bar, `story/07_ACT_IV.md:92`).
3. **Ch15 Giratina** (Reverse Depths `806` — Altered → Origin multi-bar, `story/07_ACT_IV.md:159`).
4. **Ruin R1 `GIRATINA_ORIGIN_TRIAL`** (Inverse trial ending when the PC stops attacking for 1 turn, `story/12_RUIN_ROUTE.md:18`).
5. **Ch18 Pecharunt** (Lightless Deep `844/845` — multi-bar Sweetrot boss, `story/08_ACT_V.md:25`).
6. **Ch19 Wyrmrest Reshiram on `:DRAGONS_DEN`** (`story/08_ACT_V.md:103,105` when `:war_legend == :neither` — existing `:RESHIRAM_GLASS_DUNES` in `106_Boss_WarLegends.rb` hardcodes Glass Dunes field/Siege Camp copy).
7. **Ch21 Champion Valen's Zygarde** (Complete Forme on final bar, `story/08_ACT_V.md:292`) & **Ch21 Voss/Quent's Silvally** (multi-bar ace with bar-3 regen unless Fallen Kestrel conduit is broken, `08_ACT_V.md:343`, `NARRATIVE_KEYS.md:641-643`).

### 1.4 `:PRISM_ARENA` Field Rotation Clashes With Arceus's 6-Bar Gym-Order Warden Release
- **Spec:** `story/08_ACT_V.md:372` & `story/11_FINALE_LINES.md:3` structure Arceus's finale as **6 bars of 3 locks in Gym 1–18 order** (Bar 1 = Dorian/Tamsin/Marisol ... Bar 6 = Nyx/Celestine/Sigrun), with story-variant bar counts (`5` `ARCEUS_JUDGMENT`, `6` default, `7` `ARCEUS_MISCALIBRATED`).
- **Current code:**
  - `plugins/Prismfall Bosses/103_Boss_Arceus.rb:78` sets `:bars` to `3/3/4` by difficulty instead of `6/5/7` by story variant.
  - `plugins/Prismfall Field Effects/136_Field_PrismArena.rb:35-37` rotates `[:VOLCANIC, :WATER_SURFACE, :FLOWER_GARDEN, :NEON_GRID, :FROZEN_LAKE, :COLOSSEUM, ..., :GRAND_STAGE]` (starter triangle first, Normal last), decoupled from the 18 Wardens' bar breaks.
- **Suggested Fix:** Add a `:gym_order` rotation mode (or drive `:PRISM_ARENA` shifts directly from Arceus bar breaks) so each bar cycles that trio's exact 3 Gym fields as they speak their `11_FINALE_LINES.md` vows.

### 1.5 Ch21 Tag Battle Double-Mega Rule Collision (`pbs/trainers.txt:15307,15380,15453,15667`)
- All four Ch21 tag enemies carry `MEGARING` + a Mega Stone (`MERIDIAN_KROLL v21` `SHARPEDONITE`, `MERIDIAN_MARCHETTI v21` `MANECTITE`, `MERIDIAN_QUENT v21` `METAGROSSITE`, `MERIDIAN_DIRECTORATE Captain v21` `SCIZORITE`).
- Because they always fight in enemy pairs (`Quent+Kroll`, `Marchetti+Quent`, `Marchetti+Kroll`, `Kroll+Captain`) and `PrismfallMega::LIMIT = :side` (`plugins/Prismfall Mega/001_Mega_Config.rb:27`) allows **1 Mega per side**, one enemy partner's held item is a dead slot in every Ch21 tag fight (and `:side` likewise blocks both PC + Mega ally from Mega-Evolving together).
- **Suggested Fix:** Either allow 1 Mega per *trainer* in 2v2 tag battles, or give only the senior partner in each Ch21 pair a Mega Stone and swap the junior partner to a real held item.

---

## 2. P1 — Hard Continuity, Timeline, Geography & Glass Court Contradictions

### 2.1 "Shard in Your Pocket" vs Chest-Embedded Sternum Scar (Live Boss Code + Ch11 + Ch13)
- **Canon:** The Legend Plate splinter is embedded **inside the PC's chest beneath their sternum** under a colourless star-shaped scar (`story/03_CAST.md:10`, `06_ACT_III.md:175`, `07_ACT_IV.md:57,267`, `08_ACT_V.md:383`, `29_SCRIPT_CH8.md:327`, `32_SCRIPT_CH13.md:33,168`), and the PC does not even know it is a shard until Ch13/Ch17.
- **Contradictions (4 live sites):**
  1. `plugins/Prismfall Bosses/101_Boss_Kyogre.rb:28`: `"The shard in your pocket hums in time with the waves..."`
  2. `story/30_SCRIPT_CH11.md:319`: `(In your pocket, the shard goes cold, then warm.)`
  3. `story/30_SCRIPT_CH11.md:355`: `(The shard in your pocket is warm as a hand. You take it out without meaning to, and hold it up, in the rain.)`
  4. `story/32_SCRIPT_CH13.md:306`: `(In your pocket, the shard goes so hot it hurts.)` — contradicts `L33` (`"star-shaped scar under your collar"`) and `L168` (`"goes into the child's chest"`) inside the same file.
- **Suggested Fix:** Replace all four with sternum/collar-scar resonance (at `30_SCRIPT_CH11.md:355`, have the PC press a palm flat over their sternum as white-gold heat shines through the wet coat).

### 2.2 Ch8 Script Dropped the Rimeholt Tap Manifest That Ch11 Explicitly Pays Off
- **Spec:** `story/14_WAR_AND_BLESSING.md:68` (authoritative per `06_ACT_III.md:5`) specifies Ch8's causal domino: the Dominar's Envoy declares `"Our fire warms our enemies' beds"`, Brann shows the Meridian tap manifest (`destination: Rimeholt`), and the embargo cuts Isenmar's heat first, Zenith second.
- **Payoff assumed in Ch11:** `story/30_SCRIPT_CH11.md:12,193-195` explicitly calls back to it: *"The Ch8 manifest pays off here: Cindervault's tap fed Rimeholt; with the passes closed (V122 = 1) the towers draw on the lake's own Imprint."*
- **Gap:** `story/29_SCRIPT_CH8.md:118-145,348-360` never mentions Rimeholt, Isenmar, or any tap manifest; the Herald blames only `"the Sovereign of Zenith"`.
- **Suggested Fix:** Add 4–6 lines to `29_SCRIPT_CH8.md` (Envoy exchange `L118–145` + Brann's briefing) naming `RIMEHOLT — HEAT TOWERS` on the Meridian tap manifest so Ch11's Thaw lands as a direct continental consequence.

### 2.3 Professor Imelda Larch Misnamed "Imogen Larch" (`story/31_SCRIPT_CH12.md:221`)
- `31_SCRIPT_CH12.md:221`: `"—Hollow sympathiser Imogen Larch..."` → change to **`Imelda Larch`** (`03_CAST.md:120`, `31_SCRIPT_CH12.md:158,170`).

### 2.4 Five Hard Age / Date / Timeline Math Breaks in Ch12–13
| # | Location | Current Text | Contradiction | Fix |
|---|---|---|---|---|
| 1 | `31_SCRIPT_CH12.md:293` | `"You took milk when you were nine and you came to the Lumen Gala with your mother..."` | Kestrel is 16 in AF 300 (`03_CAST.md:26`), so he was **6** at the AF 290 Glassfall when Morwen was stripped/exiled (dying AF 296). At age 9 (AF 293) she was already exiled for 3 years. | Change `"when you were nine"` → **`"when you were five"`** (AF 289 Gala). |
| 2 | `31_SCRIPT_CH12.md:260` | `"It's been undeliverable for twelve years."` | AF 290 → AF 300 is **10 years**, matching `"ten years of letters"` 32 lines earlier (`L228`). | Change `"twelve"` → **`"ten"`**. |
| 3 | `31_SCRIPT_CH12.md:324` vs `:331` | `L324`: `"A five-year-old on the deck of a ferry..."` vs `L331`: `"The photograph is the PC on the Dovetail (the prologue), from the ferry's own camera"` | The PC is **15** on the Prologue Dovetail (and was smuggled on Edda's unmonitored night boat at age 5). | Change `L324` `"A five-year-old"` → **`"A fifteen-year-old"`**. |
| 4 | `31_SCRIPT_CH12.md:159,297`, `32_SCRIPT_CH13.md:25` | Larch designed Lattice 21 years ago (`AF 279`), yet Ferrow's Landing pilot photo is `AF 288` with Voss (`47` in AF 300 → already `35` in AF 288) as a `"young man in a linesman's overalls"`, then Head of Research in AF 290, CEO in AF 291. | 9-year gap between design & pilot + Voss too old to be a "young linesman" 2 years before leading Research. | Date the Ferrow's Landing pilot photo to **`AF 280–281`** (Voss age 27–28), keeping realm-wide rollout at AF 288–289. |
| 5 | `32_SCRIPT_CH13.md:180` (+ `03_CAST.md:252,254`) | Ilsa (age **31** in AF 300): `"I've known for eleven years. I read it out of him at my mother's funeral. I was nineteen."` | `19 + 11 = 30` (not 31), and 11 years before AF 300 is **AF 289** — one year *before* the AF 290 Glassfall/shattered Crown. | Change to **`"ten years"` / `"I was twenty-one"`** (AF 290, post-Glassfall) and sync `03_CAST.md:254`, or split what she read in AF 289 vs AF 290. |

### 2.5 SPINE Rev 18 (Geography v2) Compass Flips in Ch12–13
- `story/31_SCRIPT_CH12.md:24`: Skyreach rises `"out of the plain north of the Crownwall"` → Zenith/Skyreach is **south** of Elowen/Crownwall (`SPINE.md:73`, `WORLD_MAP.md:187`, `30_SCRIPT_CH11.md:132-133`). Change `"north of"` → **`"south of"`**.
- `story/31_SCRIPT_CH12.md:347,354`: `"The Glass Road south out of Zenith... South on the Glass Road to Lucent."` → Zenith is on the **south coast**; `06_ACT_III.md:171` & `WALKTHROUGH.md:2188` correctly travel **`north`** off the plateau. Change both `"south"` → **`"north"`**.
- `story/32_SCRIPT_CH13.md:361`: `QUEST LOG: "Eighteen Roads" — South to Cragholm in the Bone Sands.` → Ossaria/Cragholm is in the **north** (`WORLD_MAP.md:189`, `(21,2)`), reached via the Grave Glass at Vigil `(20,3)`. Change `"South to Cragholm"` → **`"Through the Grave Glass north to Cragholm"`**.

### 2.6 Four Ch13 Glass Court Self-Contradictions (`story/32_SCRIPT_CH13.md`)
1. **Empty kings' gallery vs active envoys (`L230` vs `L247`):** `L230` notes Isenmar and Ashkaar's chairs are empty (`14_WAR_AND_BLESSING.md:72`), then `L247` has `"the Thane's observer on his feet, the Dominar's envoy laughing"`. Clarify in `L230` that the *thrones* are vacant while junior observers sit at the back rail, OR have `L247` react via Crownhaven clerks & the Ossarian.
2. **Eevee Octave in two places at once (`32_SCRIPT_CH13.md:230`, `06_ACT_III.md:225`):** Places `"eight singers behind [Ellery]: the Eevee Octave"` in the Glass Court — violating SPINE Rev 19 (`03_CAST.md:44-45`, singers are scattered across the 7 kingdoms until Ch20) and contradicting `L208` of the same file (Lento still missing at Mirror Mere). Change to `"white-robed Accord choristers"` in both files.
3. **Morning sentencing vs unconditional evening session (`L258,263,268` vs `L303`):** Both `:condemn` (`L258`) and `:mercy` (`L263`) pronounce final sentence in the morning (only `:refuse` at `L268` defers to evening), yet `L303` unconditionally opens `"The evening session. Rowan back in the dock. Valen in the white chair, about to speak."` Have Valen reserve formal sealing of the sentence / Kroll Mandate ruling for the evening session in all three branches.
4. **"Phantump in the lighthouse" (`L262`):** Rowan never visited Hesper's lighthouse (`105/106`); he showed the sickly Phantump to the PC and Juno at **Tidewatch Station** (`Map 103`, `20_SCRIPT_CH0-2.md:505-518`). Change `"in the lighthouse"` → **`"at Tidewatch Station"`**.

### 2.7 Ch21 Fallen Kestrel `:ch21_reach_kestrel` Quotes Unread Letter & Gate Is Tautological
- **Wrong letter quoted (`story/08_ACT_V.md:272,278,348`, `WALKTHROUGH.md:3283`):** On the Fallen path, Kestrel never reads Ysolde's sealed SF letter (`L278`), so the PC is meant to quote Morwen from a kept `:ch12_letter`. Yet `L348` quotes **`"Be the kind that's nearest when it matters"`**, which is verbatim from **Ysolde's unread letter (`L272`)**, not `:ch12_letter` (`31_SCRIPT_CH12.md:248-249`).
- **Tautological gate (`NARRATIVE_KEYS.md:163` vs `012_Narrative_Data.rb:211`):** `:ch21_reach_kestrel` unlocks if `choice(:ch18_kestrel_ring) == :keep || choice(:ch12_letter) != :burn`. Because `KESTREL_FALLEN` requires `choice(:ch18_kestrel_ring) != :give_now` and `:ch18_kestrel_ring` only has `:give_now` / `:keep`, every Fallen Kestrel player who reached Ch15 automatically gets `:reach` for free (and `!= :burn` also passes on `:send` or unset).
- **Suggested Fix:** Quote `:ch12_letter`'s actual words in `08_ACT_V.md:348`, and tighten the gate to `choice(:ch12_letter) == :keep || (choice(:ch18_kestrel_ring) == :keep && bond(:KESTREL) >= 0)` (distinct visual beats for letter vs ring).

---

## 3. P2 — PBS Teams, Missing Partners, Field Overlays, Duplicate Names & Doc Syncs

### 3.1 Festival Ace & Team Fixes (`pbs/trainers.txt`)
- **`LEADER_BRANN v96` (`L13916`):** Last slot / Lv 96 ace is unnamed `CENTISKORCH` (Charcoal), demoting canonical ace `COALOSSAL "Anvil"` (`03_CAST.md:216`) to slot 5 Lv 95. Swap so `COALOSSAL "Anvil"` is slot 6 Lv 96.
- **`LEADER_KAITO v92` (`L14333`):** Last slot / Lv 92 ace is unnamed `MEDICHAM` (Choice Band), demoting canonical Mega ace `LUCARIO "Memory"` (`03_CAST.md:226`, `LUCARIONITE`) to slot 5 Lv 91. Swap so `LUCARIO "Memory"` is slot 6 Lv 92.
- **`MERIDIAN_QUENT v99` (`L14896`):** Carries mythical **`JIRACHI`** (Lv 97) with zero lore justification (Meridian's motif is "things men made"). Swap for a manufactured Steel/Psychic mon (e.g., `ARCHALUDON`, `KLINKLANG`, or `GOLURK`).
- **`CHAMPION_VALEN v0` (`L12944`):** Zygarde missing the `"Order"` nickname present on `CHAMPION_VALEN v1` (`L14052`).
- **`REFLECTION ??? v0` (`L16293`):** Even before wiring the `$player.party` mirror hook, the 3× Ditto fallback is **Lv 85** (+18 levels over Badge 14's cap 67). Lower fallback to Lv 65–67.

### 3.2 Missing Late-Game Partner Teams & Unwired Field/Party Hooks
- **Ch21 Tag Partner Redeemed Kestrel:** Missing from `pbs/trainers.txt` (needs 3-mon Lv 95–97 tag teams matching `RIVAL_JUNO v70–72` at `L6391–6541`).
- **Ch16 Casting Floor Partner Rook:** Missing from `pbs/trainers.txt` (also flagged in `WALKTHROUGH.md:2576`).
- **Juno J4 `OGERPON_TRUSTED` swap (`08_ACT_V.md:174`):** No Ruby hook injects Ogerpon into `RIVAL_JUNO v40–42` when `OGERPON_TRUSTED` is set.
- **Amaria + Titania (`CAMEOS.md:107`):** No `TRAINER_FIELDS` override in `011_FieldEffects_MapDefaults.rb` forces `:WATER_SURFACE` in drowned Aurelia (maps `824–826` default to `:UNDERWATER`/`:CAVE`).
- **Ruin Route Inverse Overlays (`12_RUIN_ROUTE.md:37,47,79`):** Ruin Gym 16 Nyx (`:NEW_MOON` + Inverse), Ruin Gym 17 Celestine (`:FAIRY_TALE` → `:INVERSE` on last mon), and Ruin R7 Theodric (`:PRISM_ARENA` + Inverse) are not yet wired in `011_FieldEffects_MapDefaults.rb:647-652` or `008_Festival_Data.rb:148`.

### 3.3 Micro-Bugs in Scripts, Portraits, Fields & Orphaned Files
- **Orphaned `story/22_SCRIPT_CH8.md`:** Withdrawn 64-line Rev 21 stub (still cites retired `AS_RING_DAY` & invalid `:worried`). Live Ch8 is `story/29_SCRIPT_CH8.md` (`tools/build_codex.py:37`). Archive/remove `22_SCRIPT_CH8.md` and clean `build_codex.py:37`'s stale comment.
- **Invalid portrait tag (`story/07_ACT_IV.md:63`):** `[portrait: BASTIAN, worried]` — `:worried` is not in `014_Portraits.rb:59-70`; change to `sad` or `neutral`.
- **Invalid field key (`story/29_SCRIPT_CH8.md:26`):** `:SWAMP` does not exist; Map `640` defaults to `:CORROSIVE_MIRE` (`011_FieldEffects_MapDefaults.rb:323`).
- **Ch11 script micro-bugs (`story/30_SCRIPT_CH11.md` & `pbs/trainers.txt:18689`):**
  1. `L305` → `L393`: Pell is still holding the cache at `L305`, then `L393` says it's in the PC's bag — add a 1-line hand-off after pulling him off the ice.
  2. `L195`: Replace fragile `V110 == 0` check (triggers on default/unset) with `pf_chose(:ch8_caldera, :shutdown)`.
  3. `L551`: Cites `ISENMAR_SOLDIER` Lv 48–52 on Map `720`, whereas PBS defines `ISENMAR_SOLDIER_M`/`_F` and current entries (`L12508–12846`) are Ch19 Lv 79–82.
  4. `pbs/trainers.txt:18689`: Stale comment on `[MERIDIAN_DIRECTORATE,Ostrander,11]` says `PC + Juno v31` instead of `RIVAL_JUNO` battle 5 (`v50–52`).
- **Duplicate NPC names across Ch11–14:**
  - **"Pip"** (3 NPCs): Ch12 Skyreach Gale Post boy (`31_SCRIPT_CH12.md:7,110,259`), Ch14 Bastian's granddaughter **Pip Ore** (`03_CAST.md:30`, `07_ACT_IV.md:26`), plus Ironreach `"Pip's friend"` (`TRIALS_QUESTS.md:100`). Rename Ch12's courier (e.g., **Kit**).
  - **"Pell"** (3 NPCs): Ch11 Rimeholt tower tech (`30_SCRIPT_CH11.md:7,180`), Ch14 Cragholm Gym 13 lamp-boy (`GYM_PUZZLES.md:1546`, `WALKTHROUGH.md:2397`), and Warden **Dorian Pell**. Rename Rimeholt tech (e.g., **Tage**) and Cragholm lamp-boy (e.g., **Cole**).
- **Residual retired-item comment (`plugins/Prismfall Trials/131_EventMons_Later.rb:92`):** Still reads `"given with the Eevium Z and the Z-Power Ring"` (retired by SPINE Rev 23 One Ring).
- **Static `BRACKET` (`008_Festival_Data.rb:99-100`):** Pre-draw static table shows Valen (8) vs Kestrel (9) in R16, whereas `015_Festival_Draw.rb:289-309` dynamically swaps Kestrel into slot 4 vs Zenith A at `Festival.start`.

### 3.4 Story Bible & Design Doc Sync Checklist
- **Retired Sigrun v96 Final stand-in:** `story/08_ACT_V.md:294-298` & `WALKTHROUGH.md:3277` still list Sigrun alongside Brann (`015_Festival_Draw.rb:44` & `NARRATIVE_KEYS.md:478` use Brann only).
- **Ruin Game Over R1 (`GO_R_SWEET_DREAMS` → `GO_R_WELCOME_BEHIND`):** `12_RUIN_ROUTE.md:58` & `CAMEOS.md:143` still reference retired `GO_R_SWEET_DREAMS` and omit `GO_R_WELCOME_BEHIND` (`012_Narrative_Data.rb:407`).
- **Phantom "Xerneas" in Ruin R4 (`story/10_CHOICES_ENDINGS.md:387`):** Replace `"Xerneas does not wake"` with **Ogerpon** leaving at the Verge (`12_RUIN_ROUTE.md:48`).
- **Stage/chapter typos:** `:ruin_voss` says `"R4"` instead of **`R7`** (`NARRATIVE_KEYS.md:145`, `012_Narrative_Data.rb:114`); Accord Archive says `"Ch20"` instead of **`Ch17`** (`NARRATIVE_KEYS.md:69`).
- **War Arc Ch21 omissions:** `08_ACT_V.md` never stages `:ch21_boon` (`14_WAR_AND_BLESSING.md:24`) or `WAR_OCCUPATION`; `10_CHOICES_ENDINGS.md:466` (Summary Matrix row 8) omits `or WAR_OCCUPATION without Kestrel/Sigrun relief` (present at `:150`).
- **Stale `03_CAST.md` / `WALKTHROUGH.md` / `GYM_PUZZLES.md` lines:**
  - `03_CAST.md:71` Voss final `~lv 98` → `lv 100`; `:248` Odessa loses R16 to Valen → **Kestrel**; `:268` Bastian `"too old to compete"` → Seat B entrant (`008_Festival_Data.rb:84`); `:288` expose Magnus `"to the Conclave"` → **Zenith Council via Renata Sallow**.
  - `WALKTHROUGH.md:2172` & `GYM_PUZZLES.md:1335`: still list Morwen's dead letters under Gym 11 Mastery (`334`), already moved to mandatory Ch12 K5 (`31_SCRIPT_CH12.md:281,372`).
  - `WALKTHROUGH.md:1972`: cites `S128` (`CH11_THAW`) on the day-3 war declaration (`V122 = 2`) instead of the Thaw itself (`FLAGS.md:67`).
  - **Residual `NA_BEDSIDE_MANNER` doc sync:** Code (`114_Quests_Megas.rb:385-387`) already swapped giver Wenlow → Corvin, but `001_Mega_Config.rb:110`, `MEGA_EVOLUTION.md:279`, `TRIALS_QUESTS.md:107,2522`, and `WALKTHROUGH.md:3353` still list Wenlow.
- **7 stale pre-§6b lines inside `design/BALANCE.md`:** `L189` (K7/K8 `Krookodile` → `Scizor`), `L193` (J4 `Comfey` → Mega `Gardevoir "Veil"`), `L197` (Valen Standard already has `GALLADITE`), `L200` (Voss `Klinklang` → Mega `Ampharos "Lumen"`), `L209` (Marisol `v90` Standard already has `GYARADOSITE`), `L224` (Dask `v92/v192` has no Mega Stone), `L230` (Garret `v1` Lv 46 has no Mega Stone; only `v2` Lv 100 has `LUCARIONITE`).
- **Wild floor & badge-tier watchouts:** 6 late-game maps in `pbs/encounters.txt` (`681, 761, 781, 821, 840/841, 900`) retain Lv 30–40 low-rod floors (verify `OldRod`/`GoodRod` vs Surf/SuperRod), and `pbs/encounters_badgetiers.txt` has zero Badge 9–18 revisit overlays yet (pending content per `BADGE_TIERS.md:95-99`).

---

## 4. High-Leverage Acts III–V Pacing & Narrative Polish (Optional Suggestions)

1. **Ch8 → Ch11 Causal Payoff:** Restoring the Rimeholt tap manifest in `29_SCRIPT_CH8.md` makes Ch11's Thaw land as the direct continental domino of Ch8's embargo.
2. **Ilsa–Valen Act IV Spine:** Ilsa drops her parentage reveal in Ch13 (`32_SCRIPT_CH13.md:180`) then vanishes from the main plot until an optional Act V quest. One short Ch16/17 mirror beat (handing over the Concordance's Secret Articles and asking one guarded question about how Valen looked at the tribunal) gives their Ch20–21 reconciliation an earned Act IV spine.
3. **Bridge Juno's 6-Chapter Absence (Ch13 → Ch20):** One Gale Post letter / short call-in opening Ch17 (reacting to Rowan's sentence and Wenlow's death, linking back to Mirefen) makes her Ch20 J4 line (*"We started on the same dock"*) land twice as hard.
4. **Tighten Ch19 → Ch20 Pivot:** Have the PC fly back to Wyrmrest *with* Sigrun after Glass Dunes (skipping a redundant transit hop) and add 3 dynamic lines in Crownhaven's opening plaza reflecting `:war_terms` so the War Arc visually carries into the Festival.
5. **Stage `:ch21_boon` & `WAR_OCCUPATION` Explicitly in `08_ACT_V.md`:** Invoke `:ch21_boon` right before Arceus Bar 1, and add 2 lines to Valen/Brann's epilogue when `WAR_OCCUPATION` triggers *Homecoming, Unfinished*.
