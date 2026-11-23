# Proposal: Story Rematches, Mid-Game Evolutions & Reborn-Style Gauntlet Escalation

- **Target Project:** Pokémon Prismfall (`/home/antigravity/reuben12358/prismfall`)
- **Author Role:** Story Rematches & Gauntlet Escalation Architect
- **Scope:** Design-only architectural specification & PBS-ready battle data (zero live edits to `.rb`, `pbs/`, or `story/`).
- **Verified Sources:** `pbs/trainers.txt` (754 entries), `pbs/trainers_trials.txt` (4 entries), `pbs/trainer_types.txt`, `plugins/Prismfall Core/001_Config.rb`..`008_Festival_Data.rb`, `plugins/Prismfall Field Effects/` (`110`, `111`, `116`, `140`), `story/03_CAST.md`..`08_ACT_V.md`, `story/12_RUIN_ROUTE.md`, `story/14_WAR_AND_BLESSING.md`, `design/BALANCE.md`, `design/MEGA_EVOLUTION.md`, `design/Z_MOVES.md`, `design/TRAINER_FIELD_PLAYBOOK.md`, `design/maps.json`.

---

## Executive Summary

A full Python parse of `pbs/trainers.txt` and `pbs/trainers_trials.txt` exposes a stark pacing gap across Prismfall's core cast: while **Kestrel** is an eight-fight gold standard (`K1–K8/K9`), **17 of the 18 Wardens** are fought **exactly once** as mandatory opponents across the entire 19-chapter pre-Festival campaign (`Ch1–Ch19`). Worse:
- **7 Wardens** (**Tamsin, Sahar, Corvin, Ilsa, Bastian, Magnus, Nyx**) have **zero rematch or Festival battles** anywhere in `pbs/trainers.txt` (their Festival `v50` tags in `008_Festival_Data.rb` are NPC-only placeholders with no PBS data).
- **2 early Wardens** (**Dorian** Lv 15, **Rook** Lv 27) disappear for **15–17 chapters** and only reappear as 3-Pokémon halves of one optional Festival exhibition (*Pageant Bout*).
- **6 Wardens** (**Marisol, Brann, Kaito, Anja, Odessa, Ysolde**) only reappear if the player trips rare conditional Festival bracket flags (most playthroughs never see them fight again).
- **2 beloved core cast members** (**Professor Imelda Larch** and **Apprentice Wenlow**) have **0 battles** in the entire game; **Aurelian Voss** and **Sovereign Valen** have **0 pre-Festival battles**; and **Hollow Keepers Thistle, Teo, Wick, and Rowan/Mourner** are all 1-and-done early/mid-game fights.

This proposal closes every drop-off with four interlocking pillars:
1. **10 Organic Mid-Story Rematches (`M1–M10`, Ch7–Ch18):** Rejuvenation-style (Venam/Aelita/Ren) upgraded rematches slotted directly into existing canon chapters, maps, and level caps — including **Professor Larch's full-power mentor check** right after the Ch14 Ring-Day (`OS_RING_DAY`) so the player tests their new Mega Ring against their own mentor!
2. **4 Signature Reborn-Style Story Gauntlets (`G1–G4`):**
   - **G1 (Ch13):** *The Glass Court / Mindscape Refraction Gauntlet* (3-wave Reborn Glass Workstation endurance streak with no heal Wave 1→2, ally swap to Ilsa, full psychic auto-heal Wave 2→3, shifting `:MINDSCAPE` → `:INVERSE` → `:MINDSCAPE` Nightmare).
   - **G2 (Ch16):** *The Nadir Blackout / Directorate Siege Gauntlet* (3-wave urban blackout clash branching dynamically on `:ch16_rook` and `:ch16_magnus`, spotlighting Rook, Magnus, Marchetti, Kroll, Nyx & Kaito).
   - **G3 (Ch19):** *The Glass Dunes War-Front Clash* (branching Isenmar/Ashkaar/Peace battlefield commander rematches vs **Anja & Marisol** / **Sigrun & Brann**, capped by a surprise **Voss & Quent** tactical tag boss on Map `929` *The Observers' Mesa*!).
   - **G4 (Ruin Route R4–R7):** *The Oathbreakers' Last Stand* (4 heartbreaker endurance gauntlets across R4–R7 where **Dorian, Tamsin, Marisol, Rook, Professor Larch, Sahar, Corvin, Brann, Kaito**, and finally **Juno & Kestrel together** throw fully competitive Lv 83–95 Mega + Z-Move squads in your path!).
3. **Zero-Collision PBS Architecture:** 63 new base trainer entries (189 total with `+100` Hard / `+200` Casual variants) strictly verified via Python to have **0 collisions** against `pbs/trainers.txt`, `pbs/trainers_trials.txt`, Trials `v50–69`, and Festival `v90–99`.
4. **`Prismfall::Codex` & Lumen Battle Pavilion Hub Sync:** Clearing any story rematch or gauntlet wave automatically logs the encounter in `$prismfall.custom[:codex]` and unlocks that trainer's **Tier-2 / Tier-3** upgraded squad for repeatable practice and BP/Seed farming in the **Lumen Battle Pavilion** (bridging into Crownhaven's post-game **Concordance Spire**, Maps `493/494`).

---

## 1. Current Core-Cast Battle Audit Matrix

> **Audit Methodology:** Parsed programmatically from `pbs/trainers.txt` (754 entries) and `pbs/trainers_trials.txt` (4 entries). Counts exclude `+100` (Hard) and `+200` (Casual) difficulty duplicates and rival starter-slot triplets (`10/11/12` counts as 1 encounter). Partner-only ally entries (`pbRegisterPartner`), Ruin-only gym replacements (`v1`), and Festival bracket/exhibition entries (`v90/v92/v96/v99`) are broken out explicitly.

### 1.1 The 18 Wardens (Gym Leaders)

| # | Warden | PBS Type & Name | Ch1–19 Opponent Fights | Partner-Only Versions | Festival / Ruin / Exhibition | Level Gap & Drop-Off Diagnosis |
|---|---|---|---|---|---|---|
| 1 | **Dorian Pell** | `LEADER_DORIAN`, `Dorian` | **1** (`v0`, Ch2, Lv 10–15, 5m) | None | `v90` (Opt. *Pageant Bout* half, Lv 88–90, 3m) | **SEVERE:** 17-chapter / 75-level gap; never fights full 6-mon squad. |
| 2 | **Tamsin Loom** | `LEADER_TAMSIN`, `Tamsin` | **1** (`v0`, Ch3, Lv 14–19, 4m) | None | **None** (`v50` NPC-only) | **CRITICAL (#1 Worst):** 1-and-done at Lv 19 forever; Swadloon/Joltik never evolve on screen. |
| 3 | **Marisol Reyes** | `LEADER_MARISOL`, `Marisol` | **1** (`v0`, Ch4, Lv 19–23, 4m) | `v1` (Ch11, Lv 50–51, 3m), `v19` (Ch19, Lv 83–85, 3m) | `v90` (Cond. R16 if Teo died & Bond ≤ 2 / Opt. Exhib., Lv 87–90, 6m) | **SEVERE:** Never fought as opponent in Ch5–Ch19 despite huge Act III/IV arc. |
| 4 | **Rook Calder** | `LEADER_ROOK`, `Rook` | **1** (`v0`, Ch5, Lv 25–27, 4m) | None *(Ch16 Strade Works partner not in PBS!)* | `v90` (Opt. *Pageant Bout* half, Lv 88–90, 3m) | **SEVERE:** 15-chapter gap; never has a full 6-mon battle or Ch16 urban showdown. |
| 5 | **Sahar Ostrand** | `LEADER_SAHAR`, `Sahar` | **1** (`v0`, Ch6, Lv 29–31, 4m) | None | **None** (`v50` NPC-only) | **CRITICAL:** 1-and-done at Lv 31 despite leading Ch14 Groudon & Ch17 Aurelia expedition. |
| 6 | **Corvin Mott** | `LEADER_CORVIN`, `Corvin` | **1** (`v0`, Ch7, Lv 33–35, 5m) | None | **None** (`v50` NPC-only) | **CRITICAL:** 1-and-done at Lv 35 despite Ch11–14 arrest/hospital & Ch16 Wenlow arc. |
| 7 | **Brann Holloway** | `LEADER_BRANN`, `Brann` | **1** (`v0`, Ch8, Lv 37–39, 5m, Mega) | None | `v96` (Ultra-rare Final ONLY if `VALEN_COLLAPSED`, Lv 92–96, 6m) | **HIGH:** 90%+ of runs never rematch Valen's strongest Warden friend after Lv 39. |
| 8 | **Kaito Ren** | `LEADER_KAITO`, `Kaito` | **1** (`v0`, Ch9, Lv 41–43, 5m) | None | `v92` (Cond. QF ONLY if oath = Keep, Lv 88–92, 6m) | **HIGH:** Ex-Wardguard captain never rematched in Ch10–19 unless picking Keep oath. |
| 9 | **Juno Hale** | `RIVAL_JUNO` / `LEADER_JUNO`, `Juno` | **3** (`J1 v10–12` Ch2 Lv 13–15; `J2 v20–22` Ch7 Lv 33–35; `J3 v30–32` Ch10 Lv 45–47) | `v50–52` (Ch11, Lv 50–51, 3m), `v70–72` (Ch21, Lv 95–97, 3m) | `J4 v40–42` (Ch20 R16 fallback, Lv 86–90, 6m, Mega Gardevoir) | **MODERATE:** Best Warden count, yet has a **10-chapter / 43-level opponent drought** (Ch10→Ch20). |
| 10 | **Anja Sorrel** | `LEADER_ANJA`, `Anja` | **1** (`v0`, Ch11, Lv 49–51, 6m, Mega) | `v1` (Ch11 alt if Juno estranged, Lv 50–51, 3m) | `v90` (Cond. R16 ONLY if exposed in Ch11, Lv 86–90, 6m) | **HIGH:** Major Isenmar war leader has 0 war-front fights in Ch19. |
| 11 | **Odessa Gale** | `LEADER_ODESSA`, `Odessa` | **1** (`v0`, Ch12, Lv 53–55, 6m, Mega) | None | `v92` (Cond. QF if 5+ Bonds & Harmony, Lv 88–92, 6m) | **MODERATE:** Appears in Ch12 & conditional QF; needs Pavilion Tier-3 sync. |
| 12 | **Ilsa Marr** | `LEADER_ILSA`, `Ilsa` | **1** (`v0`, Ch13, Lv 57–59, 6m, Mega) | None | **None** (`v50` NPC-only) | **HIGH:** Provost of Lucent & Valen's daughter has 0 rematches or ally battles. |
| 13 | **Bastian Ore** | `LEADER_BASTIAN`, `Bastian` | **1** (`v0`, Ch14, Lv 61–63, 6m, Mega) | None | **None** (`v50` NPC-only) | **MODERATE:** Oldest Warden (retired from Festival by lore), needs Pavilion Tier-3 spar. |
| 14 | **Ysolde Ashgrave** | `LEADER_YSOLDE`, `Ysolde` | **1** (`v0`, Ch15, Lv 65–67, 6m, Mega) | None | `v92` (Cond. QF ONLY if Kestrel Fallen, Lv 88–92, 6m) | **MODERATE:** Solid Ch15 + rare QF; Pavilion sync completes coverage. |
| 15 | **Magnus Strade** | `LEADER_MAGNUS`, `Magnus` | **1** (`v0` Main OR `v1` Ruin, Ch16, Lv 69–71, 6m, Mega) | None | **None** (`v50` NPC-only) | **HIGH:** Engine architect has 0 post-gym raid/blackout clash or Festival team. |
| 16 | **Nyx Calloway** | `LEADER_NYX`, `Nyx` | **1** (`v0` Main OR `v1` Ruin, Ch17, Lv 73–75, 6m, Mega) | None | **None** (`v50` NPC-only) | **HIGH:** Nadir's queen has 0 Sump Purge barricade clash or Festival team. |
| 17 | **Celestine Aubade** | `LEADER_CELESTINE`, `Celestine` | **1** (`v0` Main OR `v1` Ruin, Ch18, Lv 78–80, 6m, Z-Move) | None | `v92` (Ch20 QF fallback, Lv 88–92, 6m, Mimikium Z) | **HEALTHY:** Late-game Gym 17 + guaranteed Festival QF fallback. |
| 18 | **Sigrun Ashfall** | `LEADER_SIGRUN`, `Sigrun` | **1** (`v0` Main OR `v1` Ruin, Ch19, Lv 83–85, 6m, Mega) | `v19` (Ch19 Glass Dunes ally, Lv 83–85, 3m) | `v92` (Cond. QF if Ruin/Isenmar won, Lv 88–92, 6m) | **MODERATE:** Strong Ch19 presence, but never fought as opposing war commander on `:back_isenmar` / Peace tracks. |

### 1.2 Rivals, Mentors, Faction Leaders & Key Cast (19 Characters)

| # | Character | PBS Type & Name | Ch1–19 Opponent Fights | Endgame / Festival / Ruin | Drop-Off Diagnosis |
|---|---|---|---|---|---|
| 19 | **Kestrel Vane** | `RIVAL_KESTREL`, `Kestrel` | **7** (`K1–K7`: `v10–72`, Lv 5→79) | `K8 v80–82` (SF Redeemed, Lv 90–94) OR `K9 v90–92` (Fallen, Lv 91–94) | **GOLD STANDARD (8 fights).** Still benefits from Ch13 Mindscape Refraction & R7 tag finale with Juno! |
| 20 | **Prof. Imelda Larch** | *(None — missing!)* | **0** | **0** | **CRITICAL:** Main mentor & ex-Meridian Chief Engineer NEVER battles once in the entire game! |
| 21 | **Sovereign Valen** | `CHAMPION_VALEN`, `Valen` | **0** | `v0` (Ch21 Final Lv 92–96), `v1` (Ruin Final Lv 92–96) | **INTENTIONAL (Late Boss):** Dignity preserved until Festival Final; Ruin `v1` already differentiates him. |
| 22 | **Aurelian Voss** | `MERIDIAN_VOSS`, `Aurelian` | **0** | `v0` (Ch21 Hijack Lv 96–100, 6m, Mega + Silvally) | **SEVERE:** Main antagonist has **0 pre-Ch21 fights**! Adding a Ch19 Glass Dunes Mesa tactical tag (`v19`) fixes this! |
| 23 | **Dr. Percival Quent** | `MERIDIAN_QUENT`, `Percival` | **3** (`v0` Ch8 Lv 37–39; `v1` Ch16 tag Lv 69–71; `v2` Ch17 alt Lv 73–75) | `v21` (Ch21 tag Lv 95–97), `v99` (Cond. Hijack Lv 96–100) | **GOOD (3–5 fights).** Pairing him with Voss in Ch19 Mesa elevates both! |
| 24 | **Helene Marchetti** | `MERIDIAN_MARCHETTI`, `Helene` | **3** (`v0` Ch12 Lv 53–55; `v1` Ch14 Lv 61–63; `v2` Ch16 tag Lv 69–71) | `v21` (Ch21 tag Lv 95–97) | **GOOD (3–4 fights).** Anchors Ch16 Blackout Siege Gauntlet (`v16`). |
| 25 | **Sabine Kroll / Sable** | `HOLLOW_SABLE` + `MERIDIAN_KROLL` | **3** (`Sable v0` Ch9 Lv 41–43; `Kroll v0` Ch13 Lv 57–59; `v1` Ch17 Lv 73–75) | `v21` (Ch21 tag Lv 95–97) | **GOOD (3–4 fights).** Adds ruthless wetwork wave in Ch16 Blackout Siege (`v16`). |
| 26 | **Vesper Lindqvist** | `OCTAVE_VESPER`, `Vesper` | **2** (`v0` Ch2 Lv 18 1m; `v1` Ch13 Lv 56–58 4m) | `v60` (Ch20 Octave Gauntlet Lv 89 1m Eevium Z) | **SOLID (3 fights).** Codex/Pavilion sync lets players rematch her full Eeveelution chorus. |
| 27 | **Rowan / The Mourner** | `HOLLOW_MOURNER` + `LEADER_ROWAN` | **1** (`Mourner v0`, Ch9, Lv 42–43, 4m) | `LEADER_ROWAN v90` (Rare R16 ONLY if alive + mercy + Hollow ≥ 4, Lv 86–90) | **SEVERE:** Unmasked Rowan never fights in Ch10–19 despite leading Lantern Hollow! |
| 28 | **Mara "Thistle"** | `HOLLOW_THISTLE`, `Thistle` | **1** (`v0`, Ch3, Lv 16–18, 3m) | **0** | **CRITICAL:** 1-and-done at Lv 18 despite defecting in Ch14 and co-leading Lantern Hollow! |
| 29 | **Brother Wick** | `HOLLOW_WICK`, `Wick` | **1** (`v0`, Ch7, Lv 33–35, 5m — skippable!) | **0** | **HIGH:** Co-founder of Hollow can finish the whole game with 0 battles fought! |
| 30 | **Teo Reyes** | `HOLLOW_TEO`, `Teo` | **1** (`v0`, Ch4, Lv 19–21, 3m) | **0** | **CRITICAL:** 1-and-done at Lv 21 even if saved at Ironreach (`TEO_SAVED`)! |
| 31 | **Apprentice Wenlow** | *(None — missing!)* | **0** | **0** *(playable only in Interlude IV before dying)* | **HIGH EMOTIONAL MISS:** One Ch14 battle before his unavoidable Ch16 death multiplies Interlude IV's gut-punch 10×! |
| 32 | **King Theodric** | `GILDED_THEODRIC`, `Theodric` | **0** | `v0` (Ruin R7 Hijack Lv 97–100) | **INTENTIONAL (Ruin Finale Boss).** |
| 33 | **Morwen Vane (Echo)** | `ECHO_MORWEN`, `Morwen` | **0** | `v90` (Cond. Ch20 Exhib. Lv 86–90) | **INTENTIONAL (Secret Echo).** |
| 34 | **Archseer Imre Dask** | `ARCHSEER_DASK`, `Imre` | **0** | `v92` (Ruin R6 QF ONLY Lv 88–92) | **INTENTIONAL (Ruin Judge)** — unlockable in Pavilion post-game for main-route players. |
| 35 | **Hammer Capt. Brisk** | `HOLLOW_ADMIN`, `Brisk` | **1** (`v0`, Ch9 tag, Lv 40–42, 3m) | **0** | Minor sub-admin (acceptable). |
| 36 | **Meridian Ashe** | `MERIDIAN_ASHE` *(orphan class)* | **0** | **0** | Orphan trainer type in `trainer_types.txt` (`BALANCE.md` notes unscripted). |
| 37 | **Capt. Edda Morrow** | *(Generic `SAILOR,Morrow` Lv 15)* | **0** *(named story battle)* | **0** | Non-combatant ferry captain/smuggler (stays non-combatant by cast design). |

### 1.3 Worst "1-and-Done" Priority Targets

| Priority Tier | Characters | Why Fixing Them Transforms Prismfall |
|---|---|---|
| **P0 — Critical Void** | **Tamsin** (Lv 19), **Dorian** (Lv 15), **Rook** (Lv 27), **Sahar** (Lv 31), **Corvin** (Lv 35), **Prof. Larch** (0 fights), **Aurelian Voss** (0 pre-Ch21 fights) | These 7 characters carry huge Act II–V story arcs yet vanish from gameplay for 10–18 chapters (or never battle at all). |
| **P1 — Major Mid-Game Gaps** | **Marisol** (Lv 23), **Brann** (Lv 39), **Kaito** (Lv 43), **Rowan** (Lv 43), **Thistle** (Lv 18), **Teo** (Lv 21), **Wick** (Lv 35), **Wenlow** (0 fights), **Juno** (10-ch gap) | Gives Act I–II allies evolving 6-Pokémon teams that track the player's own growth across Acts III–V. |
| **P2 — Late-Game / Endgame Depth** | **Anja** (Lv 51), **Ilsa** (Lv 59), **Magnus** (Lv 71), **Nyx** (Lv 75), **Sigrun** (war enemy), **Bastian** (Lv 63) | Fills Ch13/Ch16/Ch19 setpiece gauntlets and unlocks every single Warden at Tier 3 (`v92`) in the Lumen Battle Pavilion. |

---

## 2. Organic Mid-Story Leader, Mentor & Officer Rematches (`M1–M10`, Ch7–Ch18)

Modeled after **Pokémon Rejuvenation's** organic mid-story rematches (Venam post-Ch8, Aelita, Ren, Crawli), each encounter below drops straight into an **existing canon chapter beat**, respects `001_Config.rb`'s hard Level Cap, strictly honors `design/MEGA_EVOLUTION.md` §1.2 (only ring-holders Mega Evolve; Megas at cap ≥ 50 or weak Megas only) and `design/Z_MOVES.md` §4 (story-grounded Z-Crystals only), and evolves each character's actual PBS roster and nicknames.

| ID | Ch | Map ID & Location | Cap | Opponent(s) & PBS Key | Format & Field | Mega / Z-Move | Story Trigger & Narrative Stakes |
|---|---|---|---|---|---|---|---|
| **M1** | **Ch7** | `220` Mirefen (Runoff Docks) | **35** | **Teo Reyes** (`HOLLOW_TEO,Teo,7`) | Single (5m, Lv 33–35) · `:CORROSIVE_MIRE` | None *(cap < 50, no ring)* | Teo is running smuggled Hollow medicine to Corvin's Quiet Ward (`05_ACT_II.md`). If you reported him in Ch4 (`:ch4_teo == :report`), it's a furious ambush; if you covered for him, it's a tense reliability check before letting you near Brother Wick. |
| **M2** | **Ch10** | `294` Verdance — The Heartgarden | **51** *(post-J3)* | **Tamsin Loom** (`LEADER_TAMSIN,Tamsin,10`) | **Double** (6m, Lv 48–51) · `:SILKWOOD` *(woven into Heartgarden!)* | **Mega Beedrill "Spindle"** (`BEEDRILLITE`, weak Mega; Warden ring) | Right after Juno's J3 confirmation, Tamsin — standing beside Juno as the Greenward's first recruit (`06_ACT_III.md` L35) — refuses to let you march north without seeing how her newly evolved bugs fight. If `:ch2_tamsin == :keep_secret`, her dialogue carries sharp guilt; if `:confess`, warm steeliness. |
| **M3** | **Ch10–11** | `154` Pell Playhouse (unlocked w/ Fly after Badge 8/9!) | **51** | **Dorian Pell** (`LEADER_DORIAN,Dorian,10`) | Single (6m, Lv 48–51) · `:GRAND_STAGE` | **Mega Lopunny "Prima"** (`LOPUNNITE`; Warden ring) | Directly plays out the canon Act III beat (`03_CAST.md` L155): Elowen's crown padlocks the Lantern Theatre (`145`) at Meridian's request over Dorian's satire. Dorian stages a defiant private dress-rehearsal duel on the Grand Stage ("They locked the doors, darling — good thing my best understudy knows the stage door!"). |
| **M4** | **Ch11** | `167` Ebbmouth — Mill Quay | **55** *(post-Anja)* | **Marisol Reyes** (`LEADER_MARISOL,Marisol,11`) | Single (6m, Lv 52–55) · `:WATER_SURFACE` | **Mega Gyarados "Lucky"** (`GYARADOSITE`; Warden ring) | Immediately follows the Ch11 Ebbmouth Strike (`06_ACT_III.md` L105–111). If `TEO_SAVED`, Teo cheers from the dock crane while Marisol unleashes Lucky's true power; if Teo died (`!TEO_SAVED`), it's a raw, grieving tempest where she tests whether your hands are strong enough to stop what killed him. |
| **M5** | **Ch14** | `363` Cragholm — Lift Galleries (Deep Seams) | **63** *(right after Ring-Day!)* | **Prof. Imelda Larch** (`PROFESSOR_LARCH,Imelda,14`) | Single (6m, Lv 60–63) · `:CRYSTAL_CAVERN` | **Electrium Z** on **Magnezone "Coil-0"** *(AF 290 Choir sliver she preserved; no Warden ring!)* | **The Mentor Check!** Minutes after Bastian gives you the singing Warden's Ring (`OS_RING_DAY`) and Larch opens your badge case (`:ch14_telemetry`), Larch demands a real combat benchmark before Marchetti's raid so she can verify her telemetry spoof — giving the player their **very first Mega/Z test** against the woman who built the Lattice! |
| **M6** | **Ch14** | `363` Cragholm Deep Seams (Refugee Hospital) | **67** *(post-Bastian)* | **Corvin Mott** (`LEADER_CORVIN,Corvin,14`) *OR* **Apprentice Wenlow** (`APPRENTICE_WENLOW,Wenlow,14`) | **Double** (6m, Lv 64–67, `:CORROSIVE_MIRE` test ward) *OR* Single (5m, Lv 63–66, `:DARK_CRYSTAL`) | Corvin: **Mega Venusaur "Panacea"** (`VENUSAURITE`, brewed from Verdance stock). Wenlow: None. | Branches on `CORVIN_FREED` (`07_ACT_IV.md` L32)! If freed, Corvin tests your nerve in a brutal Poison double while Wenlow cheers beside the beds. If Corvin is still jailed, **17-year-old Wenlow** puts on Corvin's spare half-mask and battles you to prove he can hold the ward alone — making his unavoidable death in Ch16 Interlude IV *shattering*. |
| **M7** | **Ch14** | `783` Duneholt Undersands (Entrance) | **67** | **Sahar Ostrand** (`LEADER_SAHAR,Sahar,14`) | Single (6m, Lv 64–67) · `:DESERT` | **Mega Steelix "Stratum"** (`STEELIXITE`; Warden ring) | Right before descending to face **Groudon** (`07_ACT_IV.md` L91–95), Sahar bars the fossil stairwell: *"Nineteen years ago I buried a truth because I wasn't strong enough to stand in the sand. Show me you are."* |
| **M8** | **Ch15** | `804` Barrow of the Wardens | **71** *(post-Ysolde)* | **Rowan Ashby** (`LEADER_ROWAN,Rowan,15`) *OR* **Thistle & Wick** (`HOLLOW_THISTLE,15` + `HOLLOW_WICK,15`) | Single (6m, Lv 68–71) *OR* **1v2 Double** (3m+3m, Lv 68–71) · `:HOLLOW_CATHEDRAL` | None *(Rowan gave his ring to Juno; `MEGA_EVOLUTION.md` §6.3!)* | Branches on `:ch13_fault`! Leaving Gravenmoor for Giratina's Reverse Depths, **unmasked Rowan** (or **Thistle & Brother Wick** leading the Lantern Hollow if Rowan drowned!) demands to see if the child from AF 290 can carry the Hollow's grief without breaking. |
| **M9** | **Ch16** | `244` Cindervault — Hearthguild Hall | **75** *(post-Magnus)* | **Brann Holloway** (`LEADER_BRANN,Brann,16`) | Single (6m, Lv 72–75) · `:VOLCANIC` | **Mega Camerupt "Kiln"** (`CAMERUPTITE`; Warden ring) | Upgrades the existing 15-badge canon beat `AS_FORGE_REMEMBERS` (`07_ACT_IV.md` L216–228)! When Brann spots his singing odd ring on your hand, he refuses to hand over the twin `CAMERUPTITE` cold: *"A ring cut in Cindervault only sings true in forge-heat. Step to the anvil, kid!"* |
| **M10** | **Ch18** | `263` The Iron Pit (or `440` Gloaming Verge) | **80** *(or **85** post-Celestine)* | **Kaito Ren** (`LEADER_KAITO,Kaito,18`) | Single (6m, Lv 77–80) · `:COLOSSEUM` | **Mega Lucario "Memory"** (`LUCARIONITE`; Warden ring) | Upgrades `NA_MEMORY_KATA` (`Z_MOVES.md` §3)! With 17 badges and the complete Hymn of Return, Kaito — the Wardens' conscience after Marrowgate — demands one full-contact Colosseum duel before gifting his unit's `LUCARIONITE` + `FIGHTINIUMZ` for Crownhaven. |

> **Why M1–M10 Work Seamlessly:** Every single rematch hooks an existing canon presence (`Tamsin` in Ch10 Verdance, `Dorian`'s Ch10–11 Lantern closure, `Marisol`'s Ch11 strike, `Larch`/`Corvin`/`Wenlow`/`Sahar` in Ch14, `Rowan`/`Thistle`/`Wick` in Ch15, `Brann`'s Ch16 forge visit, `Kaito`'s Ch18 kata). Optional rematches (`M3`, `M9`, `M10`) reward key Mega Stones/BP/Codex unlocks, while story-path rematches (`M1`, `M2`, `M4`, `M5`, `M6`, `M7`, `M8`) slot cleanly right inside the chapter's natural level-cap climb.

---

## 3. Four Signature Reborn-Style Story Gauntlets (`G1–G4`)

### Gauntlet 1 — Ch13: "The Glass Court / Mindscape Refraction Gauntlet"
*Prismfall's direct homage to Pokémon Reborn's iconic **Glass Workstation Gauntlet**.*

- **Chapter & Map:** Chapter 13, inside **The Mindscape / Palace of Glass — Hall of Mirrors (`Map 348` / `355`)**, immediately after winning Gym 12 (Badge 12 → active Level Cap = **63**), when Provost **Ilsa Marr** opens Morwen's Mismagius seal on your AF 290 memory (`06_ACT_III.md` L190–204).
- **Narrative Setup:** Morwen's Mismagius didn't just lock the memory — it built a psychic immune system around it. As you walk toward the five-year-old version of yourself in Lower Crownhaven AF 290, the Mindscape twists the people who shaped your journey into **Refractions** trying to turn you back before the truth hurts you.
- **Reborn Glass Factory Endurance Rules:**
  - **3 Consecutive Waves** (18 total opposing Pokémon across 3 double battles; blacking out resets to Wave 1!).
  - **Wave 1 → Wave 2:** **ZERO party heal** on Standard & Hard (Casual applies a 50% HP/status "Mind-Mend"). Fainted Pokémon remain fainted!
  - **Wave 2 → Wave 3:** **Ilsa's Psychic Stabilizer** fires a **100% Full HP/PP/Status Auto-Heal** right before Wave 3 (*"Hold still — I'm stitching your aura back together. Don't let the glass wear their faces!"*).
  - **Ally Swap Cadence:** Wave 1 = **Solo 1v2 Double** → Wave 2 = **Partner 2v2 Double with Ally Ilsa Marr (`LEADER_ILSA,Ilsa,13`, 3m)** → Wave 3 = **Solo 1v2 Double** (exact Reborn Glass Factory cadence!).
- **Field Progression & Wave Breakdown (Cap 63):**
  1. **Wave 1 (Lv 59–61, Solo 1v2 Double, `:MINDSCAPE` Stage 1 Dream):** **Refracted Dorian (`LEADER_DORIAN,Dorian,13`, 3m, Mega Lopunny)** & **Refracted Tamsin (`LEADER_TAMSIN,Tamsin,13`, 3m, Sticky Web + Quiver Dance)**.
     - *Tactical Gimmick:* Dorian's Sound moves (`Hyper Voice`, `Boomburst`) get ×1.2 on `:MINDSCAPE` AND count toward the 3-sound-move shatter rule (`116_Field_Mindscape.rb` L16) that **cracks `:MINDSCAPE` into `:INVERSE`**! Tamsin webs & redirects while Dorian tries to break the dream early.
  2. **Wave 2 (Lv 60–62, Partner 2v2 Double w/ Ally Ilsa `v13`, NO HEAL, `:INVERSE`):** **Refracted Marisol (`LEADER_MARISOL,Marisol,13`, 3m, Mega Gyarados)** & **Refracted Rook (`LEADER_ROOK,Rook,13`, 3m, Rotom-Wash + Toxtricity)**.
     - *Tactical Gimmick:* Wave 1's broken glass drops you onto **`:INVERSE`** (`110_Field_Inverse.rb`). Suddenly Water & Electric's classic Grass/Ground answers are *inverted* into resistances, while Water's own resists turn into weaknesses! Ally Ilsa brings Trick Room `Bronzong`, `Reuniclus`, and `Hatterene "Hush"` (holding no Mega so player/foe 1-Mega-per-side stays crisp; Marisol takes the enemy side's 1 Mega).
  3. **Wave 3 (Lv 61–63, Solo 1v2 Double, FULL AUTO-HEAL, `:MINDSCAPE` Stage 2 Nightmare):** **Refracted Juno (`RIVAL_JUNO,Juno,60/61/62`, 3m, Mega Gardevoir "Veil" foreshadowing + Swapped Starter + Tsareena)** & **Refracted Kestrel (`RIVAL_KESTREL,Kestrel,13/14/15`, 3m, Aegislash "Morwen" + Swapped Starter + Hydreigon)**.
     - *Tactical Gimmick:* Starts in **`:MINDSCAPE` Stage 2 (Nightmare)** (`Dark/Ghost ×1.5`, `Fairy ×0.8`, Dark/Ghost heal 1/16/turn), supercharging Kestrel's Refracted Aegislash & Hydreigon while Juno's soothing `Moonlight`/`Calm Mind` threatens to flip it back to Stage 1 Dream for Mega Gardevoir's Psychic ×1.5! Both Gen 1 starters auto-swap via `006_RivalStarters.rb`!

---

### Gauntlet 2 — Ch16: "The Nadir Blackout / Directorate Siege Gauntlet"
*Multi-wave urban blackout clash during the opening night of **"Operation Clear Air"** (`07_ACT_IV.md` L177–215).*

- **Chapter & Maps:** Chapter 16, spanning **Cogsworth (`400`) → Strade Works Foundry Floor (`403`) → Zenith-Nadir Lift Junction (`181`/`425` Barons' Stair)**, right after Gym 15 (Badge 15 → active Level Cap = **75**), immediately before descending into Nadir for Chapter 17!
- **Branching Alliance Matrix:** Dynamically respects BOTH major Ch16 choices (`:ch16_rook` and `:ch16_magnus`), flipping who stands beside you vs who blocks your escape!
- **Endurance Rules:** 3 waves; **Wave 1 → Wave 2** gives a **50% Emergency Field-Med Drone heal** (Standard/Casual; **0% heal** on Hard!); **Wave 2 → Wave 3** triggers a **100% Full Auto-Heal** as the lift drops into Nadir's dark.
- **Wave Breakdown (Cap 75, Lv 70–75):**
  1. **Wave 1 — "Grid Collapse" (`Map 400`, `:NEON_GRID` → Blackout Stage 2, Lv 70–73):**
     - **If `:ch16_rook == :hold` (Undercover Cover-Check):** Solo 6v6 vs **Rook Calder (`LEADER_ROOK,Rook,16`, 6m, Mega Manectric "Amp")**. Directorate cameras are live on the lift deck; Rook yells *"Stay charged, citizen — you're under Mandate detention!"* while mouthing *"HIT ME FOR REAL, I'M SLIPPING YOU THE OVERRIDE!"*
     - **If `:ch16_rook == :leak_now` (Rebel Breakout):** 2v2 Tag Battle with **Ally Rook (`LEADER_ROOK,Rook,17`, 3m)** vs **Director Marchetti (`MERIDIAN_MARCHETTI,Helene,16`, 3m, Mega Houndoom) & Directorate Lieutenant Vell (`MERIDIAN_DIRECTORATE,Vell,16`, 3m)** trying to seal the lifts!
  2. **Wave 2 — "Clear Air Breach" (`Map 403`, `:FACTORY` → `:SCRAPYARD`, Lv 71–74):**
     - **If `:ch16_magnus == :expose` (Hostile Lockdown):** Solo 1v2 Double vs **Magnus Strade (`LEADER_MAGNUS,Magnus,16`, 3m, Mega Metagross "Engine") & Sabine Kroll (`MERIDIAN_KROLL,Sabine,16`, 3m, Life Orb/Focus Sash — Magnus takes the side's 1 Mega)**. Furious that you handed his foundry to Zenith politicians, Magnus locks the gantry with Kroll's wetwork squad!
     - **If `:ch16_magnus == :conscience` (`MAGNUS_KEPT_FAITH` — Ally Sabotage!):** 2v2 Tag Battle with **Ally Magnus (`LEADER_MAGNUS,Magnus,17`, 3m, no Mega so player keeps theirs)** vs **Marchetti (`MERIDIAN_MARCHETTI,Helene,16`, 3m, no Mega) & Sabine Kroll (`MERIDIAN_KROLL,Sabine,16`, 3m, Mega Sharpedo)**. Magnus pulls the foundry breakers mid-fight (`:FACTORY` → `:SCRAPYARD`)!
  3. **Wave 3 — "The Lift to Nadir" (`Map 425` Barons' Stair, `:NEW_MOON`, Full Auto-Heal, Lv 72–75):**
     - **Solo 1v2 Double (all branches):** As the blackout kills the lift lights and smoke pours out of Underveil, **Nyx Calloway (`LEADER_NYX,Nyx,16`, 3m, Mega Absol "Omen" + Illusion Zoroark "Nobody") & Kaito Ren (`LEADER_KAITO,Kaito,16`, 3m, Life Orb Lucario "Memory" + Flame Orb Conkeldurr)** ambush the arriving lift assuming you're the Directorate's vanguard! Winning proves your colors and leads seamlessly into Ch17's Underveil aftermath.

---

### Gauntlet 3 — Ch19: "The Glass Dunes War-Front Clash"
*Upgraded Lv 78–84 battlefield commander clashes + the surprise **Voss & Quent** tactical tag boss!*

- **Chapter & Maps:** Chapter 19, **The Glass Dunes (`Map 926`)** & **The Observers' Mesa (`Map 929`)**, between Sigrun's Wyrmscar Oath and Gym 18 (Badge 17 → active Level Cap = **85**).
- **Narrative Upgrade:** Currently in `pbs/trainers.txt`, Ch19's war only pits you against generic `ASHKAAR_OFFICER`/`ISENMAR_OFFICER` troops before the legendary fight, and **Aurelian Voss** has zero battles before Ch21 (`v0`). Gauntlet 3 elevates the war climax into a genuine Reborn-tier dual-front spectacle:
- **Stage 1 — "The Front Line Clash" (`Map 926`, `:GLASS_DUNES` ↔ `:FLOODED_DUNES`, Lv 78–82, Branching on `:war_climax`):**
  - **Track A (`:back_ashkaar`):** Partnered with **Sigrun (`LEADER_SIGRUN,19`, existing)** vs **Anja Sorrel (`LEADER_ANJA,Anja,19`, 3m, Mega Glalie) & Marisol Reyes (`LEADER_MARISOL,Marisol,29`, 3m, Drizzle Pelipper + Swift Swim Barraskewda)**!
    - *Field Play:* Anja's `Blizzard`/`High Horsepower` trigger thermal-shock cracks on Hot Glass (`140_Field_GlassDunes.rb`), scattering Rock-scaled glass shards on your side, while Marisol's `Drizzle` cools Hot Glass twice as fast and threatens to re-flood into `:FLOODED_DUNES`!
  - **Track B (`:back_isenmar`):** Partnered with **Marisol (`LEADER_MARISOL,19`, existing)** vs **Sigrun Ashfall (`LEADER_SIGRUN,Sigrun,29`, 3m, Mega Salamence) & Brann Holloway (`LEADER_BRANN,Brann,19`, 3m, Drought Torkoal + Lava Plume Coalossal)**!
    - *Field Play:* Brann's Sun & Fire moves lock `:GLASS_DUNES` in Stage 1 Hot Glass and anneal every crack, while powering up `Power Gem` / `Solar Beam` light-lances and setting up Sigrun's Dragon sweeps!
  - **Track C (`:stand_between` — Peace / True Hero Track):** Solo **2-Wave Consecutive Standoff** (50% field-triage heal between waves on Standard/Casual, 0% on Hard): Wave 1A vs **Anja (`v19`) & Marisol (`v29`)** → Wave 1B vs **Sigrun (`v29`) & Brann (`v19`)**! Breaking both command vanguards earns the truce directly on the battlefield!
- **Stage 2 — "The Reading on the Mesa" (`Map 929` The Observers' Mesa, Full Auto-Heal, `:GLASS_DUNES` Stage 2 Mirror Glass → `:BLEED`, Lv 81–84):**
  - **Surprise Tactical Tag Boss (Solo 1v2 Double):** Right after the beam clash (`14_WAR_AND_BLESSING.md` L103), you intercept the Meridian calibration crew packing their sensors on Map `929` — and **Aurelian Voss (`MERIDIAN_VOSS,Aurelian,19`, 3m, Mega Ampharos "Lumen" + Power Herb Archaludon + Golurk "Gilder")** steps out beside **Dr. Percival Quent (`MERIDIAN_QUENT,Percival,19`, 3m, Trick Room Bronzong + Magnezone + Porygon-Z)**!
  - *Field Play:* Fought on **`:GLASS_DUNES` Stage 2 (Mirror Glass)** (`140_Field_GlassDunes.rb` L208–210), where `Flash Cannon`, `Ice Beam`, `Hyper Beam`, and `Signal Beam` ricochet at **×1.5 and never miss**, and `Reflect`/`Light Screen` last +3 turns! Voss deliberately withholds `Silvally "NULL"` for Crownhaven, treating this fight as a live calibration stress-test of your Legend Plate splinter.

---

### Gauntlet 4 — Ruin Route (R4–R7): "The Oathbreakers' Last Stand"
*Pure Rejuvenation Renegade / Undertale Genocide emotional devastation: every Act I–II friend and mentor rallies with Lv 83–95 fully competitive **Mega + Z-Move** Field-Control squads to stop you from unmaking Velmora.*

> **Engine Compliance Note:** Under `plugins/Prismfall Mega/002_Mega_Battle.rb`, a side may legally deploy **one Mega Evolution AND one Z-Move** in the same battle (on two different Pokémon). In the Ruin Route's desperate final stand, the loyal Wardens break open the Choir's sealed Glassfall slivers (`pbs/items_zpower.txt`) alongside their Warden's rings — giving each Heartbreaker wave BOTH a Mega and a Z-Move!

| Wave | Ruin Ch | Map ID & Location | Cap | Opponents & PBS Keys | Format & Field | Mega + Z-Move Combo | Heal Rule & Heartbreaker Dialogue |
|---|---|---|---|---|---|---|---|
| **G4-A** | **R4** | `440` Gloamwood Verge (post-Ruin Celestine) | **85** | **Wave 1:** **Dorian Pell** (`LEADER_DORIAN,Dorian,44`, 6m, Lv 83–85)<br>**Wave 2:** **Tamsin Loom** (`LEADER_TAMSIN,Tamsin,44`, 6m, Lv 83–85) | 2-Wave Consecutive Singles/Double (`:GRAND_STAGE` → `:SILKWOOD`) | **W1:** Mega Lopunny + `NORMALIUMZ` Exploud<br>**W2:** Mega Beedrill + `BUGINIUMZ` Leavanny | **NO HEAL** between Dorian & Tamsin! Dorian: *"I staged a hundred tragedies, darling. I never thought I'd be the fool who opened the curtain for you."* Tamsin: *"I won't apologize this time!"* |
| **G4-B** | **R5** | `868` Rainbow Scar / Sovereign's Ascent (post-Ruin Sigrun) | **90** | **Wave 1:** **Marisol** (`LEADER_MARISOL,Marisol,45`, 3m) & **Rook** (`LEADER_ROOK,Rook,45`, 3m) (Lv 86–90)<br>**Wave 2:** **Prof. Imelda Larch** (`PROFESSOR_LARCH,Imelda,45`, 6m, Lv 87–90) | 2-Wave Consecutive (W1: 1v2 Double `:WATER_SURFACE` → W2: 6v6 Single `:RAINBOW` → `:BLEED`) | **W1:** Mega Gyarados (Marisol) + `ELECTRIUMZ` Rotom-Wash (Rook)<br>**W2:** Mega Blastoise *(Wayfarer Sanctuary starter!)* + `STEELIUMZ` Magnezone "Coil-0" | **50% Auto-Heal** (0% on Hard) between W1 & W2. Rook: *"Camera's off. Nobody's watching."* Larch: *"I promised Ines I'd keep you safe. I didn't know I was keeping the world safe from you."* |
| **G4-C** | **R6** | `482` Crownhaven — The Eighteen Gates | **92** | **Wave 1:** **Sahar** (`LEADER_SAHAR,Sahar,46`, 3m) & **Corvin** (`LEADER_CORVIN,Corvin,46`, 3m) (Lv 89–92)<br>**Wave 2:** **Brann** (`LEADER_BRANN,Brann,46`, 3m) & **Kaito** (`LEADER_KAITO,Kaito,46`, 3m) (Lv 90–92) | 2-Wave Consecutive 1v2 Doubles (W1: `:DESERT` / `:CORROSIVE_MIRE` → W2: `:VOLCANIC` / `:COLOSSEUM`) | **W1:** Mega Steelix (Sahar) + `POISONIUMZ` Toxapex (Corvin)<br>**W2:** Mega Camerupt (Brann) + `FIGHTINIUMZ` Lucario (Kaito) | **NO HEAL** between W1 & W2! Corvin: *"Wenlow died holding a door for forty strangers. I'm a doctor — I know a cancer when I see one."* Brann: *"I cut that ring. I'll break my anvil to take it back."* |
| **G4-D** | **R7** | `490` Hall of Eighteen Doors (before Theodric) | **100** | **Juno Hale** (`RIVAL_JUNO,Juno,80/81/82`, 3m) & **Kestrel Vane** (`RIVAL_KESTREL,Kestrel,23/24/25`, 3m) (Lv 93–95) | Climactic **1v2 Double** (`:PRISM_ARENA` cycling `:FLOWER_GARDEN` / `:HOLLOW_CATHEDRAL` / `:INVERSE`) | **Mega Gardevoir "Veil"** (Juno) + **`GHOSTIUMZ` Aegislash "Morwen"** (Kestrel) + BOTH Swapped Starters! | Full Heal before R7 threshold. Your two best friends stand side-by-side against you for the first and only time. Juno: *"You ate my mum's tarts. How can you just erase us?"* Kestrel: *"She died so you'd live — not so you'd turn off the lights!"* |

---

## 4. Full PBS-Ready Upgraded Team Specs, Level-Cap & Collision Verification

### 4.1 New Trainer Types (`pbs/trainer_types.txt` additions)

```ini
#-------------------------------
[PROFESSOR_LARCH]
Name = Professor
Gender = Female
BaseMoney = 120
SkillLevel = 100
BattleBGM = Battle Elite
VictoryBGM = Battle victory leader
#-------------------------------
[APPRENTICE_WENLOW]
Name = Apprentice
Gender = Male
BaseMoney = 60
SkillLevel = 64
BattleBGM = Battle Gym Leader
VictoryBGM = Battle victory leader
```

### 4.2 Collision-Free Version Reservation & Level-Cap Verification Matrix

> **Verified via Python:** All **63 proposed base entries** (`189` entries with `+100` Hard / `+200` Casual offsets) were cross-checked programmatically against all 758 existing entries in `pbs/trainers.txt` + `pbs/trainers_trials.txt`. **Result: 0 collisions.** Every non-rival story/gauntlet version stays strictly in `v7..v46` (below the `50–99` Trial/Festival zone) and strictly `< 100` so `Prismfall::Difficulty.resolve_trainer_version` (`004_Difficulty.rb`) automatically maps `v` → Standard, `v+100` → Hard, `v+200` → Casual!

| Band | Assigned Base Versions | Purpose | Active Level Cap(s) | Ace Lv Range (Std) | Collision Proof |
|---|---|---|---|---|---|
| **Mid-Story (`M1–M10`)** | `v7, v10, v11, v14, v15, v16, v18` | Chapter-numbered organic rematches | 35, 51, 55, 63, 67, 71, 75, 80 | At cap (35→80) | 0 existing entries use `v7/10/11/14/15/16/18` on these types. |
| **Gauntlet 1 (`G1`)** | `v13` (`RIVAL_JUNO v60–62`, `RIVAL_KESTREL v13–15`) | Ch13 Mindscape Refraction Gauntlet | 63 *(post-Ilsa)* | 61 / 62 / 63 | `RIVAL_JUNO` `60–62` & `RIVAL_KESTREL` `13–15` unused; Core starter swap fires on all `RIVAL_*`. |
| **Gauntlet 2 (`G2`)** | `v16` (opp), `v17` (ally partner) | Ch16 Nadir Blackout Siege Gauntlet | 75 *(post-Magnus)* | 73 / 74 / 75 | `Marchetti` (`0,1,2,21`), `Kroll` (`0,1,21`), `Vell` (`11`), `Rook/Magnus/Nyx/Kaito` clear. |
| **Gauntlet 3 (`G3`)** | `v19` (Anja, Brann, Voss, Quent), `v29` (enemy Marisol & Sigrun) | Ch19 Glass Dunes War-Front + Mesa Boss | 85 *(pre-Sigrun)* | 82 / 84 | Explicit `v29` avoids existing partner `LEADER_MARISOL,19` & `LEADER_SIGRUN,19`. |
| **Gauntlet 4 (`G4`)** | `v44` (R4), `v45` (R5), `v46` (R6), `RIVAL_JUNO v80–82`, `RIVAL_KESTREL v23–25` | Ruin Route R4–R7 Heartbreaker Gauntlets | 85 / 90 / 92 / 100 | 85 / 90 / 92 / 95 | Completely clear of Trials `50–69` & Festival `90–99`. |
| **Pavilion Tier-3** | `v92` for Dorian, Tamsin, Rook, Sahar, Corvin, Ilsa, Bastian, Magnus, Nyx | Completes full 6-mon Lv 92 squad for all 9 Wardens lacking Festival `v90–96` | 92 / 100 | 92 | All 9 verified to have 0 existing `v92` entries! |

### 4.3 Difficulty Scaling Rules (`Standard v` / `Hard v+100` / `Casual v+200`)

Every entry below adheres strictly to `design/BALANCE.md` §1 & `004_Difficulty.rb`:

| Parameter | Casual (`v + 200`) | Standard (`v`) | Hard (`v + 100`) |
|---|---|---|---|
| **Team Size** | Singles: −1 mon (min 4; Ruin/Pavilion keep 5–6). 1v2 Doubles: 2+2 or 3+3 −1 level band. | Full 5–6 mons (Singles) / 3+3 = 6 mons (1v2 & 2v2 Doubles). | Full 6 mons (Singles) / 3+3 = 6 mons (Doubles), zero cuts. |
| **Levels** | Standard −3 (caps 35–67) / −4 (caps 71–100). | Ace at cap (or wave tier cap−2..cap); support 1–3 below. | Non-aces +1 (never exceeding cap); aces at cap. |
| **IVs / EVs** | IV 14–20, EV 0. | IV 18 (cap 35) → 24 (51–55) → 28 (63–71) → 31 (75+); engine default EVs. | IV 31 (0 Spe on Trick Room mons); full 252/252/4 role EVs. |
| **Items & Gimmicks** | Keeps Mega Stone & story Z-Crystal (per Rev 21/23); swaps Choice/Life Orb for Sitrus/type boosters; 1–2 Hyper/Full Restores. | Full competitive items, Field Seeds, 1 Mega per side (and 1 Z in Ruin G4); 2 Hyper/Full Restores (0 in Partner doubles). | Upgraded Choice/Life Orb/Weakness Policy/Focus Sash, Hidden Abilities (`AbilityIndex = 2` on rivals), 3 Full Restores (and player Bag banned via `004_Difficulty.rb`). |
| **Gauntlet Heal Rules** | G1 W1→2: 50% Mind-Mend; G2/G3 mid-wave: 75% Triage; G4 W1→2: 50% Triage. | G1 W1→2: **0% heal**; G1 W2→3: **100% heal**; G2/G3/G4B mid-wave: 50% heal; G4A/C: **0% heal**. | G1/G2/G3(Peace)/G4A/B/C mid-waves: **0% heal** (pure endurance); full auto-heal only before G1 W3, G2 W3, G3 Mesa Boss, and G4-D. |

---

### 4.4 PBS-Ready Upgraded Team Specifications — Mid-Story Rematches (`M1–M10`)

#### M1 — Ch7: Teo Reyes (`Map 220` Mirefen · Cap 35 · `:CORROSIVE_MIRE`)
*Tactical Gimmick:* Evolved Ebbmouth Swift Swim core augmented with Mirefen Poison-types (`Qwilfish`, `Toxicroak`) that heal 1/16/turn on `:CORROSIVE_MIRE` and abuse `Venoshock` ×2!

```ini
#-------------------------------
# M1 - Ch7 Mirefen Rematch: Teo Reyes (Cap 35, :CORROSIVE_MIRE)
[HOLLOW_TEO,Teo,7]
Items = HYPERPOTION,HYPERPOTION
LoseText = Alright, alright — you're not Meridian's hound. Come on, Wick's down by the drowned chapel.
Pokemon = QWILFISH,33
    Moves = TOXIC,LIQUIDATION,POISONJAB,TAUNT
    Ability = INTIMIDATE
    Item = BLACKSLUDGE
    Nature = IMPISH
    IV = 18
Pokemon = SHARPEDO,33
    Moves = CRUNCH,AQUAJET,POISONFANG,PROTECT
    Ability = SPEEDBOOST
    Item = SITRUSBERRY
    Nature = JOLLY
    IV = 18
Pokemon = BARRASKEWDA,34
    Moves = LIQUIDATION,CRUNCH,BRICKBREAK,AQUAJET
    Ability = SWIFTSWIM
    Item = MYSTICWATER
    Nature = ADAMANT
    IV = 18
Pokemon = TOXICROAK,34
    Moves = FAKEOUT,VENOSHOCK,DRAINPUNCH,SUCKERPUNCH
    Ability = DRYSKIN
    Item = BLACKSLUDGE
    Nature = JOLLY
    IV = 18
Pokemon = DREDNAW,35
    Name = Snapper
    Moves = RAZORSHELL,ROCKTOMB,JAWLOCK,PROTECT
    Ability = STRONGJAW
    Item = SITRUSBERRY
    Nature = ADAMANT
    IV = 18
```

#### M2 — Ch10: Tamsin Loom (`Map 294` Verdance Heartgarden · Cap 51 post-J3 · **Double** · `:SILKWOOD`)
*Tactical Gimmick:* Tamsin's evolved thread-weaving Double squad! Lead `Masquerain` (`Intimidate` + `Rain Dance` wetting the silk for Electric ×1.2 and stopping Wildfire) + `Galvantula` (`Electroweb` spread ×1.5) → `Crustle` grounds birds (`Smack Down`) → **Mega Beedrill "Spindle"** + evolved ace **`Leavanny "Bobbin"`**!

```ini
#-------------------------------
# M2 - Ch10 Verdance Rematch: Warden Tamsin Loom (Cap 51, Double, :SILKWOOD)
[LEADER_TAMSIN,Tamsin,10]
Items = MEGARING,FULLRESTORE,FULLRESTORE
LoseText = Not one snapped thread... Juno's lucky to have you on the Greenward's side.
Pokemon = MASQUERAIN,48
    Moves = RAINDANCE,BUGBUZZ,SCALD,ICYWIND
    Ability = INTIMIDATE
    Item = DAMPROCK
    Nature = TIMID
    IV = 24
Pokemon = GALVANTULA,49
    Moves = ELECTROWEB,THUNDER,BUGBUZZ,ENERGYBALL
    Ability = COMPOUNDEYES
    Item = FOCUSSASH
    Nature = TIMID
    IV = 24
Pokemon = VIVILLON,49
    Moves = HURRICANE,RAGEPOWDER,POLLENPUFF,PROTECT
    Ability = COMPOUNDEYES
    Item = SITRUSBERRY
    Nature = TIMID
    IV = 24
Pokemon = CRUSTLE,50
    Moves = ROCKSLIDE,XSCISSOR,SMACKDOWN,PROTECT
    Ability = STURDY
    Item = HARDSTONE
    Nature = ADAMANT
    IV = 24
Pokemon = BEEDRILL,50
    Name = Spindle
    Moves = POISONJAB,UTURN,DRILLRUN,PROTECT
    Ability = SWARM
    Item = BEEDRILLITE
    Nature = JOLLY
    IV = 24
Pokemon = LEAVANNY,51
    Name = Bobbin
    Moves = LEAFBLADE,XSCISSOR,KNOCKOFF,PROTECT
    Ability = CHLOROPHYLL
    Item = TELLURICSEED
    Nature = JOLLY
    IV = 24
```

#### M3 — Ch10–11: Dorian Pell (`Map 154` Pell Playhouse · Cap 51 · Single · `:GRAND_STAGE`)
*Tactical Gimmick:* Rapidly escalates Grand Stage applause via `Ambipom` (`Fake Out` ×1.5), `Cinccino` (`Tail Slap` + `Echoed Voice`), `Exploud` (`Boomburst` sound surge), `Wigglytuff` (Standing Ovation `Sing` + `Hyper Voice`), **Mega Lopunny "Prima"** (Mega Showpiece = instant +1 applause stage per `003_Mega_Fields.rb`!), and Protean ace **`Kecleon`**!

```ini
#-------------------------------
# M3 - Ch10/11 Saltmere Rematch: Warden Dorian Pell (Cap 51, Single, :GRAND_STAGE)
[LEADER_DORIAN,Dorian,10]
Items = MEGARING,FULLRESTORE,FULLRESTORE
LoseText = Standing ovation, darling! Let the crown padlock the Lantern — they'll never silence this house!
Pokemon = AMBIPOM,48
    Moves = FAKEOUT,DOUBLEHIT,UTURN,KNOCKOFF
    Ability = TECHNICIAN
    Item = SILKSCARF
    Nature = JOLLY
    IV = 24
Pokemon = CINCCINO,49
    Moves = TAILSLAP,ROCKBLAST,BULLETSEED,ENCORE
    Ability = SKILLLINK
    Item = KINGSROCK
    Nature = JOLLY
    IV = 24
Pokemon = WIGGLYTUFF,49
    Moves = HYPERVOICE,DAZZLINGGLEAM,SING,WISH
    Ability = COMPETITIVE
    Item = LEFTOVERS
    Nature = MODEST
    IV = 24
Pokemon = EXPLOUD,50
    Moves = BOOMBURST,FLAMETHROWER,SHADOWBALL,SURF
    Ability = SCRAPPY
    Item = THROATSPRAY
    Nature = MODEST
    IV = 24
Pokemon = LOPUNNY,50
    Name = Prima
    Moves = FAKEOUT,RETURN,HIGHJUMPKICK,ICEPUNCH
    Ability = LIMBER
    Item = LOPUNNITE
    Nature = JOLLY
    IV = 24
Pokemon = KECLEON,51
    Moves = FAKEOUT,SHADOWSNEAK,SUCKERPUNCH,DRAINPUNCH
    Ability = PROTEAN
    Item = SYNTHETICSEED
    Nature = ADAMANT
    IV = 24
```

#### M4 — Ch11: Marisol Reyes (`Map 167` Ebbmouth Mill Quay · Cap 55 post-Anja · Single · `:WATER_SURFACE`)
*Tactical Gimmick:* Full Rain + Swift Swim offense on `:WATER_SURFACE` (`Pelipper` → `Floatzel`/`Kingdra`), `Lanturn` absorbing Electric answers, `Araquanid` soaking Fire/setting Sticky Web, culminating in **Mega Gyarados "Lucky"** (`Mold Breaker` breaks Levitate/Sturdy!).

```ini
#-------------------------------
# M4 - Ch11 Ebbmouth Strike Rematch: Warden Marisol Reyes (Cap 55, Single, :WATER_SURFACE)
[LEADER_MARISOL,Marisol,11]
Items = MEGARING,FULLRESTORE,FULLRESTORE
LoseText = Tides take it, kid — you really can stand against a flood. Don't let Skyreach break you.
Pokemon = PELIPPER,52
    Moves = HURRICANE,SCALD,UTURN,ROOST
    Ability = DRIZZLE
    Item = DAMPROCK
    Nature = MODEST
    IV = 24
Pokemon = LANTURN,53
    Moves = SCALD,THUNDER,VOLTSWITCH,ICEBEAM
    Ability = VOLTABSORB
    Item = LEFTOVERS
    Nature = MODEST
    IV = 24
Pokemon = FLOATZEL,53
    Moves = LIQUIDATION,ICEPUNCH,CRUNCH,AQUAJET
    Ability = SWIFTSWIM
    Item = LIFEORB
    Nature = ADAMANT
    IV = 24
Pokemon = ARAQUANID,54
    Moves = LIQUIDATION,LEECHLIFE,STICKYWEB,MIRRORCOAT
    Ability = WATERBUBBLE
    Item = SITRUSBERRY
    Nature = ADAMANT
    IV = 24
Pokemon = KINGDRA,54
    Moves = SURF,DRAGONPULSE,ICEBEAM,FLASHCANNON
    Ability = SWIFTSWIM
    Item = MYSTICWATER
    Nature = MODEST
    IV = 24
Pokemon = GYARADOS,55
    Name = Lucky
    Moves = WATERFALL,DRAGONDANCE,CRUNCH,ICEFANG
    Ability = INTIMIDATE
    Item = GYARADOSITE
    Nature = ADAMANT
    IV = 24
```

#### M5 — Ch14: Professor Imelda Larch (`Map 363` Cragholm Deep Seams · Cap 63 right after Ring-Day · Single · `:CRYSTAL_CAVERN`)
*Tactical Gimmick:* Your mentor's first battle — testing your brand-new Mega Ring! Her team blends **Tidewatch coastal biology** (`Dhelmise`, `Dragalge`, `Sawsbuck`, `Empoleon "Tidewatch"`) with **original Lattice engineering** (`Porygon2`, `Magnezone "Coil-0"` wielding `ELECTRIUMZ` Gigavolt Havoc from her AF 290 research). On `:CRYSTAL_CAVERN`, `Flash Cannon`, `Power Gem`, and `Signal Beam` refract through crystal light while `Empoleon` & `Magnezone` wall Rock sweeps!

```ini
#-------------------------------
# M5 - Ch14 Cragholm Mentor Check: Professor Imelda Larch (Cap 63, Single, :CRYSTAL_CAVERN)
[PROFESSOR_LARCH,Imelda,14]
Items = FULLRESTORE,FULLRESTORE
LoseText = Telemetry spoof holds. Your ring sang through every coil I threw at it. ...Ines would be furious, and very proud.
Pokemon = SAWSBUCK,60
    Moves = HORNLEECH,DOUBLEEDGE,JUMPKICK,SYNTHESIS
    Ability = SAPSIPPER
    Item = SITRUSBERRY
    Nature = JOLLY
    IV = 28
Pokemon = PORYGON2,61
    Moves = TRIATTACK,ICEBEAM,DISCHARGE,RECOVER
    Ability = DOWNLOAD
    Item = EVIOLITE
    Nature = MODEST
    IV = 28
Pokemon = DRAGALGE,61
    Moves = DRACOMETEOR,SLUDGEWAVE,FOCUSBLAST,FLIPTURN
    Ability = ADAPTABILITY
    Item = BLACKSLUDGE
    Nature = MODEST
    IV = 28
Pokemon = DHELMISE,62
    Name = Kelp
    Moves = POWERWHIP,POLTERGEIST,ANCHORSHOT,RAPIDSPIN
    Ability = STEELWORKER
    Item = ASSAULTVEST
    Nature = ADAMANT
    IV = 28
Pokemon = MAGNEZONE,62
    Name = Coil-0
    Moves = THUNDERBOLT,FLASHCANNON,VOLTSWITCH,BODYPRESS
    Ability = ANALYTIC
    Item = ELECTRIUMZ
    Nature = MODEST
    IV = 28
Pokemon = EMPOLEON,63
    Name = Tidewatch
    Moves = SURF,FLASHCANNON,ICEBEAM,ROOST
    Ability = COMPETITIVE
    Item = MAGICALSEED
    Nature = MODEST
    IV = 28
```

#### M6 — Ch14: Corvin Mott (`Map 363` Refugee Hospital · Cap 67 · **Double** · `:CORROSIVE_MIRE`) OR Apprentice Wenlow (`!CORVIN_FREED` · Single · `:DARK_CRYSTAL`)
*Tactical Gimmick:* If `CORVIN_FREED`, Corvin unleashes a brutal Double Poison/Medicine synergy with **Mega Venusaur "Panacea"** (Thick Fat neutralizes Fire/Ice!) alongside Galarian `Weezing` (never Misty Surge!), `Amoonguss` (`Rage Powder`), `Crobat` (`Tailwind`), `Drapion`, and Merciless ace **`Toxapex "Ward"`**. If `!CORVIN_FREED`, **Apprentice Wenlow** defends the hospital with Corvin's spare ward squad right before his tragic Ch16 fate!

```ini
#-------------------------------
# M6A - Ch14 Cragholm Field Hospital (if CORVIN_FREED): Warden Corvin Mott (Cap 67, Double, :CORROSIVE_MIRE)
[LEADER_CORVIN,Corvin,14]
Items = MEGARING,FULLRESTORE,FULLRESTORE
LoseText = Good pulse. Steady hands. You might actually survive what's coming down the lifts to Nadir.
Pokemon = WEEZING,64
    Form = 1
    Moves = STRANGESTEAM,SLUDGEBOMB,HEATWAVE,PROTECT
    Ability = LEVITATE
    Item = BLACKSLUDGE
    Nature = BOLD
    IV = 28
Pokemon = AMOONGUSS,65
    Moves = GIGADRAIN,SPORE,RAGEPOWDER,PROTECT
    Ability = REGENERATOR
    Item = ROCKYHELMET
    Nature = RELAXED
    IV = 28
Pokemon = CROBAT,65
    Moves = BRAVEBIRD,CROSSPOISON,TAILWIND,TAUNT
    Ability = INNERFOCUS
    Item = SYNTHETICSEED
    Nature = JOLLY
    IV = 28
Pokemon = DRAPION,66
    Moves = KNOCKOFF,CROSSPOISON,EARTHQUAKE,PROTECT
    Ability = SNIPER
    Item = SCOPELENS
    Nature = ADAMANT
    IV = 28
Pokemon = VENUSAUR,66
    Name = Panacea
    Moves = GIGADRAIN,SLUDGEBOMB,EARTHPOWER,PROTECT
    Ability = CHLOROPHYLL
    Item = VENUSAURITE
    Nature = MODEST
    IV = 28
Pokemon = TOXAPEX,67
    Name = Ward
    Moves = VENOSHOCK,SCALD,BANEFULBUNKER,RECOVER
    Ability = MERCILESS
    Item = BLACKSLUDGE
    Nature = BOLD
    IV = 28

#-------------------------------
# M6B - Ch14 Cragholm Field Hospital (if !CORVIN_FREED): Apprentice Wenlow (Cap 66, Single, :DARK_CRYSTAL)
[APPRENTICE_WENLOW,Wenlow,14]
Items = HYPERPOTION,HYPERPOTION
LoseText = Whew... Doctor Mott's mask is heavy, huh? Don't worry — I'll keep the Quiet Ward safe till he's back!
Pokemon = MUK,63
    Form = 1
    Moves = KNOCKOFF,POISONJAB,SHADOWSNEAK,PROTECT
    Ability = POISONTOUCH
    Item = BLACKSLUDGE
    Nature = ADAMANT
    IV = 24
Pokemon = ROSERADE,64
    Moves = GIGADRAIN,SLUDGEBOMB,DAZZLINGGLEAM,SYNTHESIS
    Ability = NATURALCURE
    Item = SITRUSBERRY
    Nature = TIMID
    IV = 24
Pokemon = AUDINO,64
    Moves = DAZZLINGGLEAM,HYPERVOICE,WISH,PROTECT
    Ability = REGENERATOR
    Item = LEFTOVERS
    Nature = CALM
    IV = 24
Pokemon = SALAZZLE,65
    Moves = FLAMETHROWER,SLUDGEWAVE,TOXIC,NASTYPLOT
    Ability = CORROSION
    Item = FOCUSSASH
    Nature = TIMID
    IV = 24
Pokemon = CLODSIRE,66
    Moves = EARTHQUAKE,POISONJAB,RECOVER,TOXIC
    Ability = WATERABSORB
    Item = BLACKSLUDGE
    Nature = CAREFUL
    IV = 24
```

#### M7 — Ch14 Transit: Sahar Ostrand (`Map 783` Duneholt Undersands · Cap 67 · Single · `:DESERT`)
*Tactical Gimmick:* Permanent Sandstorm via `Hippowdon` + `Sandaconda`, Sand Rush `Excadrill`, Moxie `Krookodile`, **Mega Steelix "Stratum"** (Sand Force ×1.3 on Ground/Rock/Steel on top of `:DESERT` Ground boost!), and `Rapid Spin`/`Earth Power` ace **`Claydol "Effigy"`**.

```ini
#-------------------------------
# M7 - Ch14 Duneholt Undersands Rematch: Warden Sahar Ostrand (Cap 67, Single, :DESERT)
[LEADER_SAHAR,Sahar,14]
Items = MEGARING,FULLRESTORE,FULLRESTORE
LoseText = Good. Then step onto the bone-road — the red giant's been turning in its bed long enough.
Pokemon = HIPPOWDON,64
    Moves = EARTHQUAKE,ROCKSLIDE,SLACKOFF,STEALTHROCK
    Ability = SANDSTREAM
    Item = SMOOTHROCK
    Nature = IMPISH
    IV = 28
Pokemon = SANDACONDA,65
    Moves = EARTHQUAKE,STONEEDGE,COIL,GLARE
    Ability = SANDSPIT
    Item = TELLURICSEED
    Nature = IMPISH
    IV = 28
Pokemon = EXCADRILL,65
    Moves = EARTHQUAKE,IRONHEAD,ROCKSLIDE,SWORDSDANCE
    Ability = SANDRUSH
    Item = LIFEORB
    Nature = ADAMANT
    IV = 28
Pokemon = KROOKODILE,66
    Moves = EARTHQUAKE,KNOCKOFF,FIREFANG,CLOSECOMBAT
    Ability = MOXIE
    Item = EXPERTBELT
    Nature = JOLLY
    IV = 28
Pokemon = STEELIX,66
    Name = Stratum
    Moves = HEAVYSLAM,EARTHQUAKE,ROCKSLIDE,CURSE
    Ability = STURDY
    Item = STEELIXITE
    Nature = BRAVE
    IV = 28
Pokemon = CLAYDOL,67
    Name = Effigy
    Moves = EARTHPOWER,PSYCHIC,ANCIENTPOWER,RAPIDSPIN
    Ability = LEVITATE
    Item = ASSAULTVEST
    Nature = MODEST
    IV = 28
```

#### M8 — Ch15: Rowan Ashby (`Map 804` Barrow of the Wardens · Cap 71 · Single · `:HOLLOW_CATHEDRAL`) OR Thistle & Brother Wick (`:ch13_fault == :marchetti` · **1v2 Double**)
*Tactical Gimmick:* Unmasked Rowan fights without a Mega Ring (strictly obeying `MEGA_EVOLUTION.md` §6.3 because Juno wears his ring!), running a Sun-Harvest hybrid on `:HOLLOW_CATHEDRAL` where ace **`Trevenant "Glasswood"`** receives Ghost ×1.5! If Rowan drowned at the Fault, **Thistle** (evolved `Dustox` → `Venomoth`/`Trevenant "Lowmarsh"`, `Amoonguss`, `Scolipede`) and **Brother Wick** (`Chimecho`, `Gardevoir`, `Dusknoir "Sexton"`) hold the barrow gate together!

```ini
#-------------------------------
# M8A - Ch15 Barrow of the Wardens (if Rowan survived): Rowan Ashby (Cap 71, Single, :HOLLOW_CATHEDRAL)
[LEADER_ROWAN,Rowan,15]
Items = FULLRESTORE,FULLRESTORE
LoseText = No masks left between us. Walk into the Glass, child — and remember what stands above it.
Pokemon = SUNFLORA,68
    Moves = SUNNYDAY,SOLARBEAM,EARTHPOWER,SLUDGEBOMB
    Ability = SOLARPOWER
    Item = HEATROCK
    Nature = MODEST
    IV = 28
Pokemon = LEAVANNY,69
    Moves = LEAFBLADE,XSCISSOR,KNOCKOFF,SWORDSDANCE
    Ability = CHLOROPHYLL
    Item = LIFEORB
    Nature = JOLLY
    IV = 28
Pokemon = ROSERADE,69
    Moves = LEAFSTORM,SLUDGEBOMB,SHADOWBALL,TOXICSPIKES
    Ability = NATURALCURE
    Item = FOCUSSASH
    Nature = TIMID
    IV = 28
Pokemon = BRELOOM,70
    Moves = MACHPUNCH,BULLETSEED,ROCKTOMB,SPORE
    Ability = TECHNICIAN
    Item = LIFEORB
    Nature = ADAMANT
    IV = 28
Pokemon = SHIFTRY,70
    Moves = LEAFBLADE,KNOCKOFF,SUCKERPUNCH,SWORDSDANCE
    Ability = CHLOROPHYLL
    Item = BLACKGLASSES
    Nature = JOLLY
    IV = 28
Pokemon = TREVENANT,71
    Name = Glasswood
    Moves = HORNLEECH,POLTERGEIST,WILLOWISP,LEECHSEED
    Ability = HARVEST
    Item = SITRUSBERRY
    Nature = IMPISH
    IV = 28

#-------------------------------
# M8B - Ch15 Barrow of the Wardens (if Rowan drowned): Thistle & Wick 1v2 Double (Cap 71, :HOLLOW_CATHEDRAL)
[HOLLOW_THISTLE,Thistle,15]
Items = FULLRESTORE
LoseText = Rowan believed in you. Make sure Lowmarsh wasn't fixed for nothing.
Pokemon = SCOLIPEDE,68
    Moves = MEGAHORN,POISONJAB,EARTHQUAKE,PROTECT
    Ability = SPEEDBOOST
    Item = LIFEORB
    Nature = JOLLY
    IV = 28
Pokemon = AMOONGUSS,69
    Moves = GIGADRAIN,SPORE,RAGEPOWDER,POLLENPUFF
    Ability = REGENERATOR
    Item = ROCKYHELMET
    Nature = RELAXED
    IV = 28
Pokemon = TREVENANT,71
    Name = Lowmarsh
    Moves = HORNLEECH,POLTERGEIST,WILLOWISP,PROTECT
    Ability = HARVEST
    Item = SITRUSBERRY
    Nature = ADAMANT
    IV = 28
#-------------------------------
[HOLLOW_WICK,Wick,15]
Items = FULLRESTORE
LoseText = You carry no color, yet every echo bows to you. Go with mercy.
Pokemon = CHIMECHO,68
    Moves = PSYCHIC,DAZZLINGGLEAM,HEALBELL,HELPINGHAND
    Ability = LEVITATE
    Item = LEFTOVERS
    Nature = CALM
    IV = 28
Pokemon = GARDEVOIR,69
    Moves = PSYCHIC,MOONBLAST,SHADOWBALL,PROTECT
    Ability = TELEPATHY
    Item = MAGICALSEED
    Nature = MODEST
    IV = 28
Pokemon = DUSKNOIR,71
    Name = Sexton
    Moves = POLTERGEIST,SHADOWSNEAK,WILLOWISP,PAINSPLIT
    Ability = PRESSURE
    Item = LEFTOVERS
    Nature = IMPISH
    IV = 28
```

#### M9 — Ch16: Brann Holloway (`Map 244` Hearthguild Hall · Cap 75 post-Magnus · Single · `:VOLCANIC`)
*Tactical Gimmick:* Upgrades `AS_FORGE_REMEMBERS`! Full 6-mon Volcanic Eruption machine: Drought `Torkoal` → **Mega Camerupt "Kiln"** (`Volcanic` Mega Showpiece primes an instant eruption!) → `Magmortar`, `Arcanine`, `Centiskorch`, and Cinderglass-ready ace **`Coalossal "Anvil"`**.

```ini
#-------------------------------
# M9 - Ch16 Hearthguild Forge Rematch: Warden Brann Holloway (Cap 75, Single, :VOLCANIC)
[LEADER_BRANN,Brann,16]
Items = MEGARING,FULLRESTORE,FULLRESTORE
LoseText = Ha! Hear that? That ring's singing loud enough to wake the Cinderhorn! Take Kiln's twin stone — you earned it.
Pokemon = TORKOAL,72
    Moves = LAVAPLUME,EARTHPOWER,WILLOWISP,CLEARSMOG
    Ability = DROUGHT
    Item = HEATROCK
    Nature = BOLD
    IV = 31
Pokemon = CAMERUPT,73
    Name = Kiln
    Moves = LAVAPLUME,EARTHPOWER,ROCKSLIDE,PROTECT
    Ability = MAGMAARMOR
    Item = CAMERUPTITE
    Nature = QUIET
    IV = 31
Pokemon = MAGMORTAR,73
    Moves = FLAMETHROWER,THUNDERBOLT,FOCUSBLAST,SCORCHINGSANDS
    Ability = FLAMEBODY
    Item = ELEMENTALSEED
    Nature = MODEST
    IV = 31
Pokemon = ARCANINE,74
    Moves = FLAREBLITZ,EXTREMESPEED,WILDCHARGE,CLOSECOMBAT
    Ability = INTIMIDATE
    Item = LIFEORB
    Nature = ADAMANT
    IV = 31
Pokemon = CENTISKORCH,74
    Moves = FIRELASH,LEECHLIFE,POWERWHIP,COIL
    Ability = FLASHFIRE
    Item = HEAVYDUTYBOOTS
    Nature = ADAMANT
    IV = 31
Pokemon = COALOSSAL,75
    Name = Anvil
    Moves = HEATCRASH,ROCKSLIDE,EARTHQUAKE,RAPIDSPIN
    Ability = STEAMENGINE
    Item = WEAKNESSPOLICY
    Nature = BRAVE
    IV = 31
```

#### M10 — Ch18: Kaito Ren (`Map 263` The Iron Pit · Cap 80 · Single · `:COLOSSEUM`)
*Tactical Gimmick:* Upgrades `NA_MEMORY_KATA`! Relentless Colosseum Frenzy engine: Synthetic Seed `Hawlucha`, No Guard `Machamp` (+1 Atk on entry!), Intimidate `Hitmontop`, Flame Orb Guts `Conkeldurr`, Pure Power `Medicham`, and **Mega Lucario "Memory"** (Colosseum Mega Showpiece counts as a knockout toward Frenzy!).

```ini
#-------------------------------
# M10 - Ch18 The Iron Pit Rematch: Warden Kaito Ren (Cap 80, Single, :COLOSSEUM)
[LEADER_KAITO,Kaito,18]
Items = MEGARING,FULLRESTORE,FULLRESTORE
LoseText = Good. You didn't flinch. Take my unit's stone and crystal — make Crownhaven listen.
Pokemon = HAWLUCHA,77
    Moves = CLOSECOMBAT,ACROBATICS,POISONJAB,UTURN
    Ability = LIMBER
    Item = SYNTHETICSEED
    Nature = JOLLY
    IV = 31
Pokemon = MACHAMP,78
    Moves = DYNAMICPUNCH,KNOCKOFF,STONEEDGE,BULLETPUNCH
    Ability = NOGUARD
    Item = SITRUSBERRY
    Nature = ADAMANT
    IV = 31
Pokemon = HITMONTOP,78
    Moves = FAKEOUT,CLOSECOMBAT,TRIPLEAXEL,SUCKERPUNCH
    Ability = INTIMIDATE
    Item = ASSAULTVEST
    Nature = ADAMANT
    IV = 31
Pokemon = CONKELDURR,79
    Moves = DRAINPUNCH,MACHPUNCH,FACADE,KNOCKOFF
    Ability = GUTS
    Item = FLAMEORB
    Nature = ADAMANT
    IV = 31
Pokemon = MEDICHAM,79
    Moves = HIGHJUMPKICK,ZENHEADBUTT,ICEPUNCH,BULLETPUNCH
    Ability = PUREPOWER
    Item = EXPERTBELT
    Nature = JOLLY
    IV = 31
Pokemon = LUCARIO,80
    Name = Memory
    Moves = CLOSECOMBAT,METEORMASH,BULLETPUNCH,SWORDSDANCE
    Ability = INNERFOCUS
    Item = LUCARIONITE
    Nature = JOLLY
    IV = 31
```

---

### 4.5 PBS-Ready Team Specifications — Gauntlet 1 (Ch13 Mindscape Refraction · Cap 63)

```ini
#===============================================================================
# GAUNTLET 1: Ch13 "The Glass Court / Mindscape Refraction Gauntlet" (Map 348/355, Cap 63)
# Wave 1 (Solo 1v2 Double, :MINDSCAPE Dream) -> NO HEAL ->
# Wave 2 (2v2 Partner w/ Ilsa v13, :INVERSE) -> FULL AUTO-HEAL ->
# Wave 3 (Solo 1v2 Double, :MINDSCAPE Stage 2 Nightmare)
#===============================================================================
# --- Wave 1: Refracted Dorian & Refracted Tamsin ---
[LEADER_DORIAN,Dorian,13]
Items = MEGARING,FULLRESTORE
LoseText = Act One closes... don't look behind the curtain, darling.
Pokemon = EXPLOUD,59
    Moves = BOOMBURST,HYPERVOICE,FLAMETHROWER,PROTECT
    Ability = SCRAPPY
    Item = THROATSPRAY
    Nature = MODEST
    IV = 28
Pokemon = LOPUNNY,60
    Name = Prima
    Moves = FAKEOUT,RETURN,HIGHJUMPKICK,PROTECT
    Ability = LIMBER
    Item = LOPUNNITE
    Nature = JOLLY
    IV = 28
Pokemon = KECLEON,61
    Moves = FAKEOUT,SUCKERPUNCH,SHADOWSNEAK,DRAINPUNCH
    Ability = PROTEAN
    Item = MAGICALSEED
    Nature = ADAMANT
    IV = 28
#-------------------------------
[LEADER_TAMSIN,Tamsin,13]
Items = FULLRESTORE
LoseText = The threads are snapping... please stop pulling!
Pokemon = GALVANTULA,59
    Moves = STICKYWEB,ELECTROWEB,BUGBUZZ,ENERGYBALL
    Ability = COMPOUNDEYES
    Item = FOCUSSASH
    Nature = TIMID
    IV = 28
Pokemon = VOLCARONA,60
    Moves = QUIVERDANCE,HEATWAVE,BUGBUZZ,PROTECT
    Ability = FLAMEBODY
    Item = SITRUSBERRY
    Nature = TIMID
    IV = 28
Pokemon = LEAVANNY,61
    Name = Bobbin
    Moves = LEAFBLADE,XSCISSOR,KNOCKOFF,HELPINGHAND
    Ability = CHLOROPHYLL
    Item = LIFEORB
    Nature = JOLLY
    IV = 28

# --- Wave 2 Partner: Ally Ilsa Marr (no Mega so Player/Enemy keep 1-per-side clarity) ---
[LEADER_ILSA,Ilsa,13]
LoseText = ...
Pokemon = BRONZONG,61
    Moves = TRICKROOM,GYROBALL,PSYCHIC,REFLECT
    Ability = LEVITATE
    Item = LIGHTCLAY
    Nature = RELAXED
    IV = 28
Pokemon = REUNICLUS,61
    Moves = PSYCHIC,FOCUSBLAST,SHADOWBALL,RECOVER
    Ability = MAGICGUARD
    Item = LIFEORB
    Nature = QUIET
    IV = 28
Pokemon = HATTERENE,62
    Name = Hush
    Moves = PSYCHICNOISE,DAZZLINGGLEAM,MYSTICALFIRE,PROTECT
    Ability = MAGICBOUNCE
    Item = SITRUSBERRY
    Nature = QUIET
    IV = 28

# --- Wave 2 Opponents: Refracted Marisol & Refracted Rook (:INVERSE) ---
[LEADER_MARISOL,Marisol,13]
Items = MEGARING,FULLRESTORE
LoseText = The tide's running backwards... hold on!
Pokemon = PELIPPER,60
    Moves = HURRICANE,SCALD,TAILWIND,PROTECT
    Ability = DRIZZLE
    Item = DAMPROCK
    Nature = MODEST
    IV = 28
Pokemon = BARRASKEWDA,61
    Moves = LIQUIDATION,CLOSECOMBAT,PSYCHICFANGS,PROTECT
    Ability = SWIFTSWIM
    Item = LIFEORB
    Nature = ADAMANT
    IV = 28
Pokemon = GYARADOS,62
    Name = Lucky
    Moves = WATERFALL,CRUNCH,ICEFANG,DRAGONDANCE
    Ability = INTIMIDATE
    Item = GYARADOSITE
    Nature = ADAMANT
    IV = 28
#-------------------------------
[LEADER_ROOK,Rook,13]
Items = FULLRESTORE
LoseText = Signal inverted... chat's gone static!
Pokemon = TOXTRICITY,60
    Moves = OVERDRIVE,SLUDGEBOMB,BOOMBURST,PROTECT
    Ability = PUNKROCK
    Item = THROATSPRAY
    Nature = MODEST
    IV = 28
Pokemon = ELECTIVIRE,61
    Moves = WILDCHARGE,ICEPUNCH,EARTHQUAKE,CROSSCHOP
    Ability = MOTORDRIVE
    Item = EXPERTBELT
    Nature = JOLLY
    IV = 28
Pokemon = ROTOM,62
    Form = 2
    Name = Camera
    Moves = HYDROPUMP,DISCHARGE,WILLOWISP,HEX
    Ability = LEVITATE
    Item = MAGICALSEED
    Nature = TIMID
    IV = 28

# --- Wave 3 Opponents: Refracted Juno (v60/61/62) & Refracted Kestrel (v13/14/15) (:MINDSCAPE Stage 2 Nightmare) ---
# Starter slots: Juno v60=Blastoise / v61=Venusaur / v62=Charizard (auto-swapped by 006_RivalStarters.rb)
# Kestrel v13=Charizard / v14=Blastoise / v15=Venusaur (auto-swapped by 006_RivalStarters.rb)
[RIVAL_JUNO,Juno,60]
Items = MEGARING,FULLRESTORE
LoseText = Don't wake up... if you remember, you'll leave me behind!
Pokemon = GARDEVOIR,61
    Name = Veil
    Moves = HYPERVOICE,PSYCHIC,MYSTICALFIRE,PROTECT
    Ability = TRACE
    Item = GARDEVOIRITE
    Nature = TIMID
    IV = 28
Pokemon = BLASTOISE,62
    Moves = HYDROPUMP,ICEBEAM,DARKPULSE,PROTECT
    AbilityIndex = 0
    Item = SITRUSBERRY
    Nature = MODEST
    IV = 28
Pokemon = TSAREENA,63
    Name = Sweetpea
    Moves = TROPKICK,PLAYROUGH,HIGHJUMPKICK,UTURN
    Ability = QUEENLYMAJESTY
    Item = LIFEORB
    Nature = JOLLY
    IV = 28
# (v61 swaps BLASTOISE -> VENUSAUR; v62 swaps BLASTOISE -> CHARIZARD; identical Veil & Sweetpea)
#-------------------------------
[RIVAL_KESTREL,Kestrel,13]
Items = FULLRESTORE
LoseText = My mother threw herself in the light for a ghost...
Pokemon = HYDREIGON,61
    Moves = DARKPULSE,DRAGONPULSE,FLAMETHROWER,PROTECT
    Ability = LEVITATE
    Item = MAGICALSEED
    Nature = TIMID
    IV = 28
Pokemon = CHARIZARD,62
    Moves = HEATWAVE,AIRSLASH,DRAGONPULSE,PROTECT
    AbilityIndex = 0
    Item = SITRUSBERRY
    Nature = TIMID
    IV = 28
Pokemon = AEGISLASH,63
    Name = Morwen
    Moves = SHADOWBALL,FLASHCANNON,SHADOWSNEAK,KINGSSHIELD
    Ability = STANCECHANGE
    Item = SPELLTAG
    Nature = QUIET
    IV = 28
# (v14 swaps CHARIZARD -> BLASTOISE; v15 swaps CHARIZARD -> VENUSAUR; identical Hydreigon & Morwen)
```

---

### 4.6 PBS-Ready Team Specifications — Gauntlet 2 (Ch16 Nadir Blackout Siege · Cap 75)

```ini
#===============================================================================
# GAUNTLET 2: Ch16 "The Nadir Blackout / Directorate Siege Gauntlet" (Maps 400/403/425, Cap 75)
#===============================================================================
# --- Wave 1A (:ch16_rook == :hold) - Rook Calder Staged Cover-Fight (Solo 6v6, :NEON_GRID) ---
[LEADER_ROOK,Rook,16]
Items = MEGARING,FULLRESTORE,FULLRESTORE
LoseText = ...Alright, cameras caught the dive. Override codes are in your badge case — RUN!
Pokemon = LUXRAY,70
    Moves = WILDCHARGE,CRUNCH,ICEPUNCH,VOLTSWITCH
    Ability = INTIMIDATE
    Item = ASSAULTVEST
    Nature = ADAMANT
    IV = 31
Pokemon = HELIOLISK,71
    Moves = THUNDERBOLT,HYPERVOICE,SURF,VOLTSWITCH
    Ability = DRYSKIN
    Item = LIFEORB
    Nature = TIMID
    IV = 31
Pokemon = ELECTIVIRE,71
    Moves = WILDCHARGE,ICEPUNCH,EARTHQUAKE,CROSSCHOP
    Ability = MOTORDRIVE
    Item = SYNTHETICSEED
    Nature = JOLLY
    IV = 31
Pokemon = TOXTRICITY,72
    Moves = OVERDRIVE,SLUDGEBOMB,BOOMBURST,VOLTSWITCH
    Ability = PUNKROCK
    Item = THROATSPRAY
    Nature = MODEST
    IV = 31
Pokemon = MANECTRIC,72
    Name = Amp
    Moves = THUNDERBOLT,FLAMETHROWER,VOLTSWITCH,SNARL
    Ability = LIGHTNINGROD
    Item = MANECTITE
    Nature = TIMID
    IV = 31
Pokemon = ROTOM,73
    Form = 2
    Name = Camera
    Moves = HYDROPUMP,THUNDERBOLT,WILLOWISP,HEX
    Ability = LEVITATE
    Item = LEFTOVERS
    Nature = TIMID
    IV = 31

# --- Wave 1B (:ch16_rook == :leak_now) - Ally Rook v17 vs Marchetti v16 & Vell v16 ---
[LEADER_ROOK,Rook,17]
LoseText = ...
Pokemon = TOXTRICITY,72
    Moves = OVERDRIVE,SLUDGEBOMB,BOOMBURST,PROTECT
    Ability = PUNKROCK
    Item = THROATSPRAY
    Nature = MODEST
    IV = 31
Pokemon = ELECTIVIRE,72
    Moves = WILDCHARGE,ICEPUNCH,EARTHQUAKE,PROTECT
    Ability = MOTORDRIVE
    Item = LIFEORB
    Nature = JOLLY
    IV = 31
Pokemon = ROTOM,73
    Form = 2
    Name = Camera
    Moves = HYDROPUMP,DISCHARGE,WILLOWISP,PROTECT
    Ability = LEVITATE
    Item = LEFTOVERS
    Nature = TIMID
    IV = 31
#-------------------------------
[MERIDIAN_MARCHETTI,Helene,16]
Items = MEGARING,FULLRESTORE
LoseText = Containment breached. Seal the lower shafts — now!
Pokemon = HOUNDOOM,71
    Moves = HEATWAVE,DARKPULSE,SLUDGEBOMB,PROTECT
    Ability = FLASHFIRE
    Item = HOUNDOOMINITE
    Nature = TIMID
    IV = 31
Pokemon = CORVIKNIGHT,72
    Moves = BRAVEBIRD,BODYPRESS,TAILWIND,ROOST
    Ability = MIRRORARMOR
    Item = LEFTOVERS
    Nature = IMPISH
    IV = 31
Pokemon = MABOSSTIFF,73
    Moves = CRUNCH,PLAYROUGH,PSYCHICFANGS,SNARL
    Ability = INTIMIDATE
    Item = ASSAULTVEST
    Nature = ADAMANT
    IV = 31
#-------------------------------
[MERIDIAN_DIRECTORATE,Vell,16]
Items = FULLRESTORE
LoseText = Lift locks failed! They're heading for Strade Works!
Pokemon = MAGNEZONE,71
    Moves = DISCHARGE,FLASHCANNON,BODYPRESS,PROTECT
    Ability = ANALYTIC
    Item = AIRBALLOON
    Nature = MODEST
    IV = 28
Pokemon = ARCANINE,72
    Moves = FLAREBLITZ,SNARL,EXTREMESPEED,WILLOWISP
    Ability = INTIMIDATE
    Item = SITRUSBERRY
    Nature = ADAMANT
    IV = 28
Pokemon = ALAKAZAM,73
    Moves = PSYCHIC,DAZZLINGGLEAM,SHADOWBALL,PROTECT
    Ability = MAGICGUARD
    Item = FOCUSSASH
    Nature = TIMID
    IV = 28

# --- Wave 2A (:ch16_magnus == :expose) - Magnus v16 & Kroll v16 (:FACTORY -> :SCRAPYARD) ---
# (Note: On Wave 2B :conscience, Ally Magnus v17 + PC fight Marchetti v16 [no Mega variant / Life Orb] & Kroll v16 [Mega Sharpedo]!)
[LEADER_MAGNUS,Magnus,16]
Items = MEGARING,FULLRESTORE
LoseText = You broke my tolerances. Now live with what falls out of them.
Pokemon = KLINKLANG,72
    Name = Mark One
    Moves = SHIFTGEAR,GEARGRIND,WILDCHARGE,PROTECT
    Ability = CLEARBODY
    Item = SITRUSBERRY
    Nature = ADAMANT
    IV = 31
Pokemon = KINGAMBIT,73
    Moves = KOWTOWCLEAVE,IRONHEAD,SUCKERPUNCH,PROTECT
    Ability = DEFIANT
    Item = BLACKGLASSES
    Nature = ADAMANT
    IV = 31
Pokemon = METAGROSS,74
    Name = Engine
    Moves = METEORMASH,ZENHEADBUTT,EARTHQUAKE,BULLETPUNCH
    Ability = CLEARBODY
    Item = METAGROSSITE
    Nature = JOLLY
    IV = 31
#-------------------------------
[LEADER_MAGNUS,Magnus,17]
LoseText = ...
Pokemon = FERROTHORN,72
    Moves = POWERWHIP,GYROBALL,LEECHSEED,PROTECT
    Ability = IRONBARBS
    Item = ROCKYHELMET
    Nature = RELAXED
    IV = 31
Pokemon = KLINKLANG,73
    Name = Mark One
    Moves = SHIFTGEAR,GEARGRIND,WILDCHARGE,MAGNETRISE
    Ability = CLEARBODY
    Item = SITRUSBERRY
    Nature = ADAMANT
    IV = 31
Pokemon = EXCADRILL,74
    Moves = EARTHQUAKE,IRONHEAD,ROCKSLIDE,PROTECT
    Ability = MOLDBREAKER
    Item = FOCUSSASH
    Nature = JOLLY
    IV = 31
#-------------------------------
[MERIDIAN_KROLL,Sabine,16]
Items = MEGARING,FULLRESTORE
LoseText = Oh, lovely — the lights went out! Saves me cleaning up the witnesses.
Pokemon = SHARPEDO,72
    Moves = CRUNCH,LIQUIDATION,ICEFANG,PROTECT
    Ability = SPEEDBOOST
    Item = SHARPEDONITE
    Nature = ADAMANT
    IV = 31
Pokemon = OBSTAGOON,73
    Moves = KNOCKOFF,FACADE,CLOSECOMBAT,OBSTRUCT
    Ability = GUTS
    Item = FLAMEORB
    Nature = JOLLY
    IV = 31
Pokemon = DRAPION,74
    Moves = KNOCKOFF,CROSSPOISON,EARTHQUAKE,ROCKSLIDE
    Ability = SNIPER
    Item = SCOPELENS
    Nature = ADAMANT
    IV = 31
# Engine note: When paired with Magnus v16 (Wave 2A), PrismfallMega's 1-Mega-per-side rule triggers Magnus's Metagross first;
# in Wave 2B (Marchetti + Kroll), Kroll's Sharpedo Megas while Marchetti's Houndoom holds Life Orb via event/sub-variant or natural side lock!

# --- Wave 3 (All Branches, FULL AUTO-HEAL, :NEW_MOON) - Nyx v16 & Kaito v16 barring Barons' Stair ---
[LEADER_NYX,Nyx,16]
Items = MEGARING,FULLRESTORE
LoseText = ...Wait. You're with Calder? Put the blades down, Kaito — wrong target.
Pokemon = GRIMMSNARL,73
    Moves = REFLECT,LIGHTSCREEN,SPIRITBREAK,FAKEOUT
    Ability = PRANKSTER
    Item = LIGHTCLAY
    Nature = CAREFUL
    IV = 31
Pokemon = ABSOL,74
    Name = Omen
    Moves = NIGHTSLASH,SUCKERPUNCH,PLAYROUGH,PROTECT
    Ability = SUPERLUCK
    Item = ABSOLITE
    Nature = JOLLY
    IV = 31
Pokemon = ZOROARK,75
    Name = Nobody
    Moves = NIGHTDAZE,FLAMETHROWER,SLUDGEBOMB,NASTYPLOT
    Ability = ILLUSION
    Item = LIFEORB
    Nature = TIMID
    IV = 31
#-------------------------------
[LEADER_KAITO,Kaito,16]
Items = FULLRESTORE
LoseText = Stand down. Rook's broadcast is real — they're bringing the Purge down the lifts.
Pokemon = HAWLUCHA,73
    Moves = CLOSECOMBAT,ACROBATICS,POISONJAB,PROTECT
    Ability = LIMBER
    Item = MAGICALSEED
    Nature = JOLLY
    IV = 31
Pokemon = CONKELDURR,74
    Moves = DRAINPUNCH,MACHPUNCH,ROCKSLIDE,PROTECT
    Ability = GUTS
    Item = FLAMEORB
    Nature = ADAMANT
    IV = 31
Pokemon = LUCARIO,75
    Name = Memory
    Moves = AURASPHERE,FLASHCANNON,DARKPULSE,VACUUMWAVE
    Ability = INNERFOCUS
    Item = LIFEORB
    Nature = TIMID
    IV = 31
```

---

### 4.7 PBS-Ready Team Specifications — Gauntlet 3 (Ch19 Glass Dunes War-Front & Voss/Quent Boss · Cap 85)

```ini
#===============================================================================
# GAUNTLET 3: Ch19 "The Glass Dunes War-Front Clash" (Maps 926 & 929, Cap 85)
#===============================================================================
# --- Isenmar Vanguard: Anja v19 & Marisol v29 (Map 926, :GLASS_DUNES <-> :FLOODED_DUNES) ---
[LEADER_ANJA,Anja,19]
Items = MEGARING,FULLRESTORE
LoseText = The sand's glassed under our boots... hold the line, Marisol!
Pokemon = NINETALES,80
    Form = 1
    Moves = AURORAVEIL,BLIZZARD,MOONBLAST,FREEZEDRY
    Ability = SNOWWARNING
    Item = LIGHTCLAY
    Nature = TIMID
    IV = 31
Pokemon = GLALIE,81
    Moves = DOUBLEEDGE,FREEZEDRY,EARTHQUAKE,PROTECT
    Ability = INNERFOCUS
    Item = GLALITITE
    Nature = JOLLY
    IV = 31
Pokemon = MAMOSWINE,82
    Name = Matriarch
    Moves = HIGHHORSEPOWER,ICICLECRASH,ICESHARD,ROCKSLIDE
    Ability = THICKFAT
    Item = LIFEORB
    Nature = ADAMANT
    IV = 31
#-------------------------------
[LEADER_MARISOL,Marisol,29]
Items = FULLRESTORE
LoseText = Tides take this whole war — pull the sleds back behind Skaldfast!
Pokemon = PELIPPER,80
    Moves = HURRICANE,SCALD,TAILWIND,WIDEGUARD
    Ability = DRIZZLE
    Item = DAMPROCK
    Nature = MODEST
    IV = 31
Pokemon = BARRASKEWDA,81
    Moves = LIQUIDATION,CLOSECOMBAT,PSYCHICFANGS,AQUAJET
    Ability = SWIFTSWIM
    Item = CHOICEBAND
    Nature = ADAMANT
    IV = 31
Pokemon = GYARADOS,82
    Name = Lucky
    Moves = WATERFALL,CRUNCH,ICEFANG,DRAGONDANCE
    Ability = INTIMIDATE
    Item = SITRUSBERRY
    Nature = ADAMANT
    IV = 31

# --- Ashkaar Vanguard: Sigrun v29 & Brann v19 (Map 926, :GLASS_DUNES Stage 1 Hot Glass) ---
[LEADER_SIGRUN,Sigrun,29]
Items = MEGARING,FULLRESTORE
LoseText = You held the ground between two armies... I won't burn past you.
Pokemon = FLYGON,80
    Moves = EARTHQUAKE,DRAGONCLAW,ROCKSLIDE,UTURN
    Ability = LEVITATE
    Item = CHOICESCARF
    Nature = JOLLY
    IV = 31
Pokemon = KOMMOO,81
    Moves = CLANGINGSCALES,AURASPHERE,FLAMETHROWER,PROTECT
    Ability = BULLETPROOF
    Item = THROATSPRAY
    Nature = TIMID
    IV = 31
Pokemon = SALAMENCE,82
    Name = Dreamwing
    Moves = DOUBLEEDGE,DRAGONDANCE,EARTHQUAKE,PROTECT
    Ability = INTIMIDATE
    Item = SALAMENCITE
    Nature = JOLLY
    IV = 31
#-------------------------------
[LEADER_BRANN,Brann,19]
Items = FULLRESTORE
LoseText = Ach... fighting you on a battlefield's a sight uglier than the anvil, kid.
Pokemon = TORKOAL,80
    Moves = ERUPTION,HEATWAVE,EARTHPOWER,SOLARBEAM
    Ability = DROUGHT
    Item = HEATROCK
    Nature = QUIET
    IV = 31
Pokemon = ARCANINE,81
    Moves = FLAREBLITZ,EXTREMESPEED,SNARL,HELPINGHAND
    Ability = INTIMIDATE
    Item = SITRUSBERRY
    Nature = ADAMANT
    IV = 31
Pokemon = COALOSSAL,82
    Name = Anvil
    Moves = HEATWAVE,POWERGEM,EARTHPOWER,PROTECT
    Ability = STEAMENGINE
    Item = WEAKNESSPOLICY
    Nature = MODEST
    IV = 31

# --- Stage 2 Surprise Tactical Boss: Voss v19 & Quent v19 (Map 929 Observers' Mesa, :GLASS_DUNES Stage 2 Mirror Glass) ---
[MERIDIAN_VOSS,Aurelian,19]
Items = MEGARING,FULLRESTORE
LoseText = Marvellous data. You're finally running at full tolerance — I'll see you at the coronation.
Pokemon = AMPHAROS,82
    Name = Lumen
    Moves = THUNDERBOLT,DRAGONPULSE,DAZZLINGGLEAM,PROTECT
    Ability = STATIC
    Item = AMPHAROSITE
    Nature = MODEST
    IV = 31
Pokemon = ARCHALUDON,83
    Moves = ELECTROSHOT,FLASHCANNON,DRACOMETEOR,BODYPRESS
    Ability = STAMINA
    Item = POWERHERB
    Nature = MODEST
    IV = 31
Pokemon = GOLURK,84
    Name = Gilder
    Moves = POLTERGEIST,HIGHHORSEPOWER,DYNAMICPUNCH,PROTECT
    Ability = NOGUARD
    Item = LIFEORB
    Nature = ADAMANT
    IV = 31
#-------------------------------
[MERIDIAN_QUENT,Percival,19]
Items = FULLRESTORE
LoseText = Oh, the beam refraction spikes! Aurelian, we HAVE to frame this printout!
Pokemon = BRONZONG,81
    Moves = TRICKROOM,REFLECT,LIGHTSCREEN,FLASHCANNON
    Ability = LEVITATE
    Item = LIGHTCLAY
    Nature = RELAXED
    IV = 31
Pokemon = MAGNEZONE,82
    Moves = FLASHCANNON,THUNDERBOLT,SIGNALBEAM,PROTECT
    Ability = ANALYTIC
    Item = AIRBALLOON
    Nature = MODEST
    IV = 31
Pokemon = PORYGONZ,83
    Moves = TRIATTACK,ICEBEAM,DARKPULSE,HYPERBEAM
    Ability = ADAPTABILITY
    Item = CHOICESPECS
    Nature = TIMID
    IV = 31
```

---

### 4.8 PBS-Ready Team Specifications — Gauntlet 4 (Ruin Route R4–R7 "Oathbreakers' Last Stand")

```ini
#===============================================================================
# GAUNTLET 4A: Ruin R4 "The Curtain & The Loom" (Map 440, Cap 85, 2-Wave NO HEAL)
#===============================================================================
[LEADER_DORIAN,Dorian,44]
Items = MEGARING,FULLRESTORE,FULLRESTORE
LoseText = Curtain down. ...Forgive me, Velmora. I cast the wrong lead.
Pokemon = AMBIPOM,83
    Moves = FAKEOUT,DOUBLEHIT,KNOCKOFF,UTURN
    Ability = TECHNICIAN
    Item = LIFEORB
    Nature = JOLLY
    IV = 31
Pokemon = CINCCINO,83
    Moves = TAILSLAP,ROCKBLAST,BULLETSEED,TRIPLEAXEL
    Ability = SKILLLINK
    Item = KINGSROCK
    Nature = JOLLY
    IV = 31
Pokemon = WIGGLYTUFF,84
    Moves = HYPERVOICE,DAZZLINGGLEAM,SING,PERISHSONG
    Ability = COMPETITIVE
    Item = FOCUSSASH
    Nature = TIMID
    IV = 31
Pokemon = EXPLOUD,84
    Moves = BOOMBURST,FLAMETHROWER,SURF,FOCUSBLAST
    Ability = SCRAPPY
    Item = NORMALIUMZ
    Nature = MODEST
    IV = 31
Pokemon = LOPUNNY,85
    Name = Prima
    Moves = FAKEOUT,RETURN,HIGHJUMPKICK,TRIPLEAXEL
    Ability = LIMBER
    Item = LOPUNNITE
    Nature = JOLLY
    IV = 31
Pokemon = KECLEON,85
    Moves = FAKEOUT,SUCKERPUNCH,SHADOWSNEAK,DRAINPUNCH
    Ability = PROTEAN
    Item = SYNTHETICSEED
    Nature = ADAMANT
    IV = 31
#-------------------------------
[LEADER_TAMSIN,Tamsin,44]
Items = MEGARING,FULLRESTORE,FULLRESTORE
LoseText = Even if you cut every last strand... Briarwick will remember we tried.
Pokemon = GALVANTULA,83
    Moves = STICKYWEB,ELECTROWEB,THUNDER,BUGBUZZ
    Ability = COMPOUNDEYES
    Item = FOCUSSASH
    Nature = TIMID
    IV = 31
Pokemon = MASQUERAIN,83
    Moves = RAINDANCE,QUIVERDANCE,BUGBUZZ,HYDROPUMP
    Ability = INTIMIDATE
    Item = DAMPROCK
    Nature = TIMID
    IV = 31
Pokemon = CRUSTLE,84
    Moves = SHELLSMASH,ROCKSLIDE,XSCISSOR,EARTHQUAKE
    Ability = STURDY
    Item = WHITEHERB
    Nature = JOLLY
    IV = 31
Pokemon = VOLCARONA,84
    Moves = QUIVERDANCE,HEATWAVE,BUGBUZZ,GIGADRAIN
    Ability = FLAMEBODY
    Item = HEAVYDUTYBOOTS
    Nature = TIMID
    IV = 31
Pokemon = BEEDRILL,85
    Name = Spindle
    Moves = POISONJAB,UTURN,DRILLRUN,PROTECT
    Ability = SWARM
    Item = BEEDRILLITE
    Nature = JOLLY
    IV = 31
Pokemon = LEAVANNY,85
    Name = Bobbin
    Moves = LEAFBLADE,XSCISSOR,KNOCKOFF,SWORDSDANCE
    Ability = CHLOROPHYLL
    Item = BUGINIUMZ
    Nature = JOLLY
    IV = 31

#===============================================================================
# GAUNTLET 4B: Ruin R5 "The Engineer's Reckoning" (Map 868, Cap 90, 2-Wave 50% Heal)
#===============================================================================
# --- Wave 1 (1v2 Double, :WATER_SURFACE): Marisol v45 (Mega) & Rook v45 (Z-Move) ---
[LEADER_MARISOL,Marisol,45]
Items = MEGARING,FULLRESTORE
LoseText = Go on then — drown the whole map. You won't drown us quietly!
Pokemon = PELIPPER,87
    Moves = HURRICANE,SCALD,TAILWIND,WIDEGUARD
    Ability = DRIZZLE
    Item = DAMPROCK
    Nature = MODEST
    IV = 31
Pokemon = BARRASKEWDA,88
    Moves = LIQUIDATION,CLOSECOMBAT,PSYCHICFANGS,AQUAJET
    Ability = SWIFTSWIM
    Item = CHOICEBAND
    Nature = ADAMANT
    IV = 31
Pokemon = GYARADOS,90
    Name = Lucky
    Moves = WATERFALL,DRAGONDANCE,CRUNCH,ICEFANG
    Ability = INTIMIDATE
    Item = GYARADOSITE
    Nature = ADAMANT
    IV = 31
#-------------------------------
[LEADER_ROOK,Rook,45]
Items = FULLRESTORE
LoseText = Camera's off. Nobody's watching. ...Why couldn't you stay the kid from the dock?
Pokemon = TOXTRICITY,87
    Moves = OVERDRIVE,SLUDGEBOMB,BOOMBURST,PROTECT
    Ability = PUNKROCK
    Item = THROATSPRAY
    Nature = MODEST
    IV = 31
Pokemon = ELECTIVIRE,88
    Moves = WILDCHARGE,ICEPUNCH,EARTHQUAKE,CROSSCHOP
    Ability = MOTORDRIVE
    Item = LIFEORB
    Nature = JOLLY
    IV = 31
Pokemon = ROTOM,90
    Form = 2
    Name = Camera
    Moves = HYDROPUMP,THUNDER,WILLOWISP,PROTECT
    Ability = LEVITATE
    Item = ELECTRIUMZ
    Nature = TIMID
    IV = 31

# --- Wave 2 (Full 6v6, :RAINBOW -> :BLEED): Professor Imelda Larch v45 ---
[PROFESSOR_LARCH,Imelda,45]
Items = MEGARING,FULLRESTORE,FULLRESTORE
LoseText = ...My tea's gone cold. Walk past me, then — I won't watch what you do to Ines's world.
Pokemon = SAWSBUCK,87
    Moves = HORNLEECH,DOUBLEEDGE,JUMPKICK,MEGAHORN
    Ability = SAPSIPPER
    Item = LIFEORB
    Nature = JOLLY
    IV = 31
Pokemon = DRAGALGE,88
    Moves = DRACOMETEOR,SLUDGEWAVE,FOCUSBLAST,SCALD
    Ability = ADAPTABILITY
    Item = ASSAULTVEST
    Nature = MODEST
    IV = 31
Pokemon = DHELMISE,88
    Name = Kelp
    Moves = POWERWHIP,POLTERGEIST,ANCHORSHOT,RAPIDSPIN
    Ability = STEELWORKER
    Item = LEFTOVERS
    Nature = ADAMANT
    IV = 31
Pokemon = BLASTOISE,89
    Name = Wayfarer
    Moves = SHELLSMASH,WATERPULSE,AURASPHERE,DARKPULSE
    Ability = TORRENT
    Item = BLASTOISINITE
    Nature = TIMID
    IV = 31
Pokemon = MAGNEZONE,89
    Name = Coil-0
    Moves = FLASHCANNON,THUNDERBOLT,VOLTSWITCH,BODYPRESS
    Ability = ANALYTIC
    Item = STEELIUMZ
    Nature = MODEST
    IV = 31
Pokemon = EMPOLEON,90
    Name = Tidewatch
    Moves = SURF,FLASHCANNON,ICEBEAM,ROOST
    Ability = COMPETITIVE
    Item = MAGICALSEED
    Nature = MODEST
    IV = 31

#===============================================================================
# GAUNTLET 4C: Ruin R6 "The Wardens' Oath" (Map 482 Eighteen Gates, Cap 92, 2-Wave NO HEAL)
#===============================================================================
# --- Wave 1 (1v2 Double, :DESERT): Sahar v46 (Mega) & Corvin v46 (Z-Move) ---
[LEADER_SAHAR,Sahar,46]
Items = MEGARING,FULLRESTORE
LoseText = The sand remembers everything, child. It won't forgive you for erasing it.
Pokemon = HIPPOWDON,89
    Moves = EARTHQUAKE,ROCKSLIDE,SLACKOFF,YAWN
    Ability = SANDSTREAM
    Item = SMOOTHROCK
    Nature = IMPISH
    IV = 31
Pokemon = STEELIX,90
    Name = Stratum
    Moves = HEAVYSLAM,HIGHHORSEPOWER,ROCKSLIDE,PROTECT
    Ability = STURDY
    Item = STEELIXITE
    Nature = BRAVE
    IV = 31
Pokemon = CLAYDOL,92
    Name = Effigy
    Moves = EARTHPOWER,PSYCHIC,ICEBEAM,ALLYSWITCH
    Ability = LEVITATE
    Item = TELLURICSEED
    Nature = MODEST
    IV = 31
#-------------------------------
[LEADER_CORVIN,Corvin,46]
Items = FULLRESTORE
LoseText = Wenlow died holding a door for strangers. You call this a cure?
Pokemon = WEEZING,89
    Form = 1
    Moves = STRANGESTEAM,SLUDGEBOMB,HEATWAVE,PROTECT
    Ability = LEVITATE
    Item = BLACKSLUDGE
    Nature = BOLD
    IV = 31
Pokemon = CROBAT,90
    Moves = BRAVEBIRD,CROSSPOISON,TAILWIND,TAUNT
    Ability = INNERFOCUS
    Item = FOCUSSASH
    Nature = JOLLY
    IV = 31
Pokemon = TOXAPEX,92
    Name = Ward
    Moves = SLUDGEBOMB,SCALD,BANEFULBUNKER,RECOVER
    Ability = MERCILESS
    Item = POISONIUMZ
    Nature = BOLD
    IV = 31

# --- Wave 2 (1v2 Double, :VOLCANIC): Brann v46 (Mega) & Kaito v46 (Z-Move) ---
[LEADER_BRANN,Brann,46]
Items = MEGARING,FULLRESTORE
LoseText = Take the ring off, kid. You've got no right to hear it sing anymore.
Pokemon = TORKOAL,90
    Moves = ERUPTION,HEATWAVE,EARTHPOWER,PROTECT
    Ability = DROUGHT
    Item = HEATROCK
    Nature = QUIET
    IV = 31
Pokemon = CAMERUPT,91
    Name = Kiln
    Moves = HEATWAVE,EARTHPOWER,ROCKSLIDE,PROTECT
    Ability = MAGMAARMOR
    Item = CAMERUPTITE
    Nature = QUIET
    IV = 31
Pokemon = COALOSSAL,92
    Name = Anvil
    Moves = HEATCRASH,ROCKSLIDE,EARTHQUAKE,PROTECT
    Ability = STEAMENGINE
    Item = WEAKNESSPOLICY
    Nature = BRAVE
    IV = 31
#-------------------------------
[LEADER_KAITO,Kaito,46]
Items = FULLRESTORE
LoseText = Marrowgate was a sin. What you're about to do is worse.
Pokemon = HAWLUCHA,90
    Moves = CLOSECOMBAT,ACROBATICS,POISONJAB,PROTECT
    Ability = UNBURDEN
    Item = ELEMENTALSEED
    Nature = JOLLY
    IV = 31
Pokemon = CONKELDURR,91
    Moves = DRAINPUNCH,MACHPUNCH,ROCKSLIDE,PROTECT
    Ability = GUTS
    Item = FLAMEORB
    Nature = ADAMANT
    IV = 31
Pokemon = LUCARIO,92
    Name = Memory
    Moves = CLOSECOMBAT,METEORMASH,EXTREMESPEED,PROTECT
    Ability = INNERFOCUS
    Item = FIGHTINIUMZ
    Nature = JOLLY
    IV = 31

#===============================================================================
# GAUNTLET 4D: Ruin R7 "The Last Two Who Loved You" (Map 490, Cap 100, :PRISM_ARENA)
#===============================================================================
# Juno v80/81/82 (Mega Gardevoir) & Kestrel v23/24/25 (Ghostium Z Aegislash) — BOTH Swapped Starters!
[RIVAL_JUNO,Juno,80]
Items = MEGARING,FULLRESTORE
LoseText = ...Even now, my wreath won't wilt. Please don't go through that door.
Pokemon = GARDEVOIR,93
    Name = Veil
    Moves = HYPERVOICE,PSYCHIC,MYSTICALFIRE,PROTECT
    Ability = TRACE
    Item = GARDEVOIRITE
    Nature = TIMID
    IV = 31
Pokemon = BLASTOISE,94
    Moves = WATERSPOUT,ICEBEAM,AURASPHERE,PROTECT
    AbilityIndex = 2
    Item = SITRUSBERRY
    Nature = MODEST
    IV = 31
Pokemon = TSAREENA,95
    Name = Sweetpea
    Moves = POWERWHIP,PLAYROUGH,HIGHJUMPKICK,TRIPLEAXEL
    Ability = QUEENLYMAJESTY
    Item = LIFEORB
    Nature = JOLLY
    IV = 31
# (v81 swaps BLASTOISE -> VENUSAUR; v82 swaps BLASTOISE -> CHARIZARD)
#-------------------------------
[RIVAL_KESTREL,Kestrel,23]
Items = FULLRESTORE
LoseText = She died so you'd live... not so you'd turn off the lights.
Pokemon = MISMAGIUS,93
    Moves = SHADOWBALL,DAZZLINGGLEAM,MYSTICALFIRE,DESTINYBOND
    Ability = LEVITATE
    Item = FOCUSSASH
    Nature = TIMID
    IV = 31
Pokemon = CHARIZARD,94
    Moves = HEATWAVE,AIRSLASH,SCORCHINGSANDS,PROTECT
    AbilityIndex = 2
    Item = LIFEORB
    Nature = TIMID
    IV = 31
Pokemon = AEGISLASH,95
    Name = Morwen
    Moves = SHADOWBALL,FLASHCANNON,SHADOWSNEAK,KINGSSHIELD
    Ability = STANCECHANGE
    Item = GHOSTIUMZ
    Nature = QUIET
    IV = 31
# (v24 swaps CHARIZARD -> BLASTOISE; v25 swaps CHARIZARD -> VENUSAUR)
```

### 4.9 Pavilion Tier-3 Completion Roster (`v92` for the 9 Wardens Missing Full Lv 90–92 Squads)

So that **18/18 Wardens** can be rematched at full Festival Tier-3 strength (`Lv 88–92`, 6 Pokémon, Mega or Z-Move) inside the **Lumen Battle Pavilion** and post-game **Concordance Spire**, nine `v92` entries mirror existing `gen.py` `promote()` logic (using the Warden's upgraded 6-mon roster from `M2/M3/M6/M7/G2` or `v0` promoted to Lv 88–92):
- `LEADER_DORIAN,Dorian,92` (Ambipom, Cinccino, Wigglytuff, Exploud, **Mega Lopunny**, Protean Kecleon — Lv 88–92)
- `LEADER_TAMSIN,Tamsin,92` (Masquerain, Galvantula, Vivillon, Crustle, **Mega Beedrill**, Leavanny "Bobbin" — Lv 88–92)
- `LEADER_ROOK,Rook,92` (Luxray, Heliolisk, Electivire, Toxtricity, **Mega Manectric "Amp"**, Rotom-Wash "Camera" — Lv 88–92)
- `LEADER_SAHAR,Sahar,92` (Hippowdon, Sandaconda, Excadrill, Krookodile, **Mega Steelix "Stratum"**, Claydol "Effigy" — Lv 88–92)
- `LEADER_CORVIN,Corvin,92` (Galarian Weezing, Amoonguss, Crobat, Drapion, **Mega Venusaur "Panacea"**, Toxapex "Ward" — Lv 88–92)
- `LEADER_ILSA,Ilsa,92` (Bronzong, **Mega Slowbro**, Espeon, Gothitelle, Reuniclus, Hatterene "Hush" — Lv 88–92)
- `LEADER_BASTIAN,Bastian,92` (Carbink, Alolan Golem, Aurorus, **Mega Aerodactyl "Amber"**, Rhyperior, Gigalith "Geode" — Lv 88–92)
- `LEADER_MAGNUS,Magnus,92` (Ferrothorn, Excadrill, Kingambit, Klinklang "Mark One", Scizor, **Mega Metagross "Engine"** — Lv 88–92)
- `LEADER_NYX,Nyx,92` (Grimmsnarl, Weavile, **Mega Absol "Omen"**, Umbreon, Zoroark "Nobody", Honchkrow — Lv 88–92)

---

## 5. `Prismfall::Codex` & Lumen Battle Pavilion Repeatable Hub Sync

### 5.1 Save-State Architecture (Zero Migration Breakage)

All Codex tracking and Battle Pavilion unlocks live inside `Prismfall.state.custom[:codex]` (`plugins/Prismfall Core/002_SaveState.rb` L26, explicitly reserved for later Core features so existing saves stay 100% loadable):

```ruby
# Stored inside Prismfall.state.custom[:codex]
{
  :encounters => {
    # trainer_key => { tier_sym => { cleared: true, wins: Int, best_difficulty: :HARD, first_chapter: Int, field: :SILKWOOD } }
    :LEADER_TAMSIN => {
      :tier1 => { cleared: true, wins: 1, best_difficulty: :STANDARD, first_chapter: 3,  field: :SILKWOOD },
      :tier2 => { cleared: true, wins: 2, best_difficulty: :HARD,     first_chapter: 10, field: :SILKWOOD },
      :tier3 => { cleared: false }
    }
  },
  :gauntlets => {
    :G1_MINDSCAPE   => { cleared: true, best_difficulty: :HARD, no_faint_streak: false },
    :G2_BLACKOUT    => { cleared: true, best_difficulty: :STANDARD },
    :G3_GLASS_DUNES => { cleared: false },
    :G4_OATHBREAKER => { cleared: false }
  },
  :pavilion_bp => 0
}
```

### 5.2 Automatic Post-Battle Logging (`Prismfall::Codex`)

Hook `EventHandlers.add(:on_end_battle, :prismfall_codex_rematch)` so EVERY story rematch and gauntlet wave automatically logs into `Prismfall::Codex` without needing fragile manual switches on every event map:

```ruby
module Prismfall
  module Codex
    # Maps [trainer_type, base_version] => { id:, tier:, label:, pavilion_version:, field:, double: }
    REMATCH_REGISTRY = {
      # Tier 1 (Initial Debuts) -> automatically unlock Tier 1 in Pavilion
      [:LEADER_DORIAN,  0]  => { id: :DORIAN,  tier: :tier1, label: "Matinee Opening",        pavilion_version: 0,  field: :GRAND_STAGE,      double: false },
      [:LEADER_TAMSIN,  0]  => { id: :TAMSIN,  tier: :tier1, label: "Loomhouse Debut",        pavilion_version: 0,  field: :SILKWOOD,         double: true  },
      # Tier 2 (Mid-Story & Gauntlet Upgraded Squads) -> unlock Tier 2 in Pavilion!
      [:HOLLOW_TEO,     7]  => { id: :TEO,     tier: :tier2, label: "Sump Runner",            pavilion_version: 7,  field: :CORROSIVE_MIRE,   double: false },
      [:LEADER_TAMSIN,  10] => { id: :TAMSIN,  tier: :tier2, label: "Greenward Weaver",       pavilion_version: 10, field: :SILKWOOD,         double: true  },
      [:LEADER_DORIAN,  10] => { id: :DORIAN,  tier: :tier2, label: "Closing Night Encore",   pavilion_version: 10, field: :GRAND_STAGE,      double: false },
      [:LEADER_MARISOL, 11] => { id: :MARISOL, tier: :tier2, label: "Ebb Strike Captain",     pavilion_version: 11, field: :WATER_SURFACE,    double: false },
      [:PROFESSOR_LARCH,14] => { id: :LARCH,   tier: :tier2, label: "Lattice Benchmark",      pavilion_version: 14, field: :CRYSTAL_CAVERN,   double: false },
      [:LEADER_CORVIN,  14] => { id: :CORVIN,  tier: :tier2, label: "Field Triage",           pavilion_version: 14, field: :CORROSIVE_MIRE,   double: true  },
      [:LEADER_SAHAR,   14] => { id: :SAHAR,   tier: :tier2, label: "Undersands Excavation",  pavilion_version: 14, field: :DESERT,           double: false },
      [:LEADER_ROWAN,   15] => { id: :ROWAN,   tier: :tier2, label: "Unmasked Warden",        pavilion_version: 15, field: :HOLLOW_CATHEDRAL, double: false },
      [:LEADER_BRANN,   16] => { id: :BRANN,   tier: :tier2, label: "Anvil Temper",           pavilion_version: 16, field: :VOLCANIC,         double: false },
      [:LEADER_ROOK,    16] => { id: :ROOK,    tier: :tier2, label: "Blackout Override",      pavilion_version: 16, field: :NEON_GRID,        double: false },
      [:LEADER_KAITO,   18] => { id: :KAITO,   tier: :tier2, label: "Memory Kata",            pavilion_version: 18, field: :COLOSSEUM,        double: false },
      [:MERIDIAN_VOSS,  19] => { id: :VOSS,    tier: :tier2, label: "Mesa Calibration",       pavilion_version: 19, field: :GLASS_DUNES,      double: true  },
      # Tier 3 (Festival / Ruin Oathbreaker Full-Power Squads) -> unlock Tier 3 in Pavilion!
      [:LEADER_DORIAN,  44] => { id: :DORIAN,  tier: :tier3, label: "Oathbreaker Stage",      pavilion_version: 44, field: :GRAND_STAGE,      double: false },
      [:LEADER_TAMSIN,  44] => { id: :TAMSIN,  tier: :tier3, label: "Oathbreaker Loom",       pavilion_version: 44, field: :SILKWOOD,         double: true  },
      [:PROFESSOR_LARCH,45] => { id: :LARCH,   tier: :tier3, label: "Final Lecture",          pavilion_version: 45, field: :RAINBOW,          double: false },
      [:LEADER_MARISOL, 90] => { id: :MARISOL, tier: :tier3, label: "Festival Delegation",    pavilion_version: 90, field: :WATER_SURFACE,    double: false },
      [:LEADER_KAITO,   92] => { id: :KAITO,   tier: :tier3, label: "Festival Delegation",    pavilion_version: 92, field: :COLOSSEUM,        double: false },
      [:LEADER_BRANN,   96] => { id: :BRANN,   tier: :tier3, label: "Sovereign's Hand",       pavilion_version: 96, field: :VOLCANIC,         double: false }
      # ...completed for all 18 Wardens (v90/v92/v96), Rivals (J4/K8/K9), Faction Admins, Vesper, and Dask
    }

    def self.record_victory(trainer_type, raw_version)
      base_v = raw_version % Prismfall::TRAINER_VARIANT_STRIDE   # strips +100 Hard / +200 Casual
      spec = REMATCH_REGISTRY[[trainer_type, base_v]]
      return unless spec
      entry = state[:encounters][spec[:id]] ||= {}
      tier  = entry[spec[:tier]] ||= { cleared: false, wins: 0, best_difficulty: nil }
      first_time = !tier[:cleared]
      tier[:cleared] = true
      tier[:wins] += 1
      cur_diff = Prismfall::Difficulty.current
      if tier[:best_difficulty].nil? || Prismfall::Difficulty.rank(cur_diff) > Prismfall::Difficulty.rank(tier[:best_difficulty])
        tier[:best_difficulty] = cur_diff
      end
      if first_time && spec[:tier] != :tier1
        pbMessage(_INTL("\\se[GUI naming confirm]Codex Updated! {1}'s {2} squad is now unlocked in the Lumen Battle Pavilion!",
                        spec[:id].to_s.capitalize, spec[:label]))
      end
    end
  end
end
```

### 5.3 The Lumen Battle Pavilion (`Map 940`, Wing off `Map 180` Lumen Concourse) & Concordance Spire Bridge

- **Location & Access:** Opens after **Badge 5** (returning via Fly after Badge 8 or walking through Lumen City Concourse `Map 180` → dedicated collision-free interior `Map 940: Lumen Battle Pavilion`). Post-game, the exact same `Prismfall::Codex.pavilion_roster` syncs automatically to Crownhaven's **Concordance Spire (`Map 493/494`)**!
- **3-Tier Repeatable Selection UI:**
  1. **Tier 1 (Original Encounter):** Replay any defeated Warden/Rival/Admin's debut battle (optional toggle: *Original Levels* vs *Flat Lv 50*).
  2. **Tier 2 (Mid-Story / Gauntlet Rematch):** Unlocked immediately upon clearing `M1–M10` or `G1–G3`! Allows replaying both **Singles** (`M1–M10`) and **Simulation Gauntlets** (re-running `G1 Mindscape Refraction`, `G2 Nadir Blackout`, or `G3 Glass Dunes` with all 3 waves intact for BP multipliers!).
  3. **Tier 3 (Full-Power / Festival / Ruin Oathbreaker):** Unlocked automatically for any Warden/Rival/Mentor upon reaching **18 Badges** (unlocking the 9 newly built `v92` Warden squads + Festival draws) OR upon clearing their **Ruin Oathbreaker (`v44–46`)** wave — even letting main-route post-game players opt into "Refraction Simulation: Oathbreaker Mode" once the Festival is cleared!
- **Level Cap Safety & Rewards:**
  - Pavilion battles respect `Prismfall::LevelCap.current` (EXP is still safely clamped by `005_LevelCap.rb`; optional `noExp` toggle for pure strategy testing!).
  - Clearing a Tier-2 or Tier-3 Pavilion rematch awards **Battle Points (BP)** exchangeable for **Field Seeds** (`ELEMENTALSEED`, `MAGICALSEED`, `TELLURICSEED`, `SYNTHETICSEED`), **Ability Patches/Capsules**, **Nature Mints**, and **EV Training Braces** — turning Prismfall's cast into the best training & teambuilding loop in any fangame!

### 5.4 Reusable Reborn-Style Gauntlet Runner Helper (`Prismfall::Gauntlet.run`)

So all four setpieces (`G1–G4`) require ~10 lines of RPG Maker event script each without duplicate healing/reset boilerplate:

```ruby
# Example event call for G1 (Ch13 Mindscape Refraction Gauntlet, Map 348/355)
Prismfall::Gauntlet.run(:G1_MINDSCAPE, [
  { foes: [[:LEADER_DORIAN, "Dorian", 13], [:LEADER_TAMSIN, "Tamsin", 13]],
    field: :MINDSCAPE, double: true, heal_after: { casual: 0.5, standard: 0.0, hard: 0.0 } },
  { foes: [[:LEADER_MARISOL, "Marisol", 13], [:LEADER_ROOK, "Rook", 13]],
    partner: [:LEADER_ILSA, "Ilsa", 13],
    field: :INVERSE, double: true, heal_after: { casual: 1.0, standard: 1.0, hard: 1.0 } },
  { foes: [[:RIVAL_JUNO, "Juno", 60 + Prismfall::Rival.starter_slot],
           [:RIVAL_KESTREL, "Kestrel", 13 + Prismfall::Rival.starter_slot]],
    field: :MINDSCAPE, field_stage: 2, double: true }
])
```
- **Failure Handling:** Losing any wave cleanly restores the pre-gauntlet snapshot and resets to Wave 1 (exact Reborn Glass Workstation rule, never soft-locking the player with a half-fainted party inside the Mindscape!).
- **Difficulty Hooks:** Automatically honors `004_Difficulty.rb` (`+100` Hard / `+200` Casual + Set style + No-Bag on Hard) and `006_RivalStarters.rb` (Gen 1–9 starter swap on Juno/Kestrel).
- **Codex Sync:** Clearing the final wave logs `:G1_MINDSCAPE` in `$prismfall.custom[:codex][:gauntlets]` and unlocks the **Refraction Gauntlet Simulation** inside the Lumen Battle Pavilion!

---

## Summary Impact: Before vs After

| Metric | Before Proposal | After Proposal |
|---|---|---|
| Wardens with 0 rematches / 0 Festival teams | **7 / 18** (Tamsin, Sahar, Corvin, Ilsa, Bastian, Magnus, Nyx) | **0 / 18** (18/18 have Tier-2 story/gauntlet + Tier-3 `v90–96` squads!) |
| Wardens with ≥ 2 pre-Festival story/gauntlet battles | **1 / 18** (Juno only) | **15 / 18** (all Act I–IV Wardens + Sigrun/Anja/Nyx/Magnus!) |
| Professor Larch / Wenlow battles | **0** / **0** | **2** (Ch14 Mentor Check + R5 Heartbreaker) / **1** (Ch14 Hospital if Corvin jailed) |
| Aurelian Voss pre-Ch21 battles | **0** | **1** (Ch19 Glass Dunes Mesa Tactical Tag w/ Quent) |
| Multi-wave Reborn-style Story Gauntlets | **0** (only post-Ch20 optional Octave gauntlet) | **4 Major Story Setpieces** (`G1` Ch13, `G2` Ch16, `G3` Ch19, `G4` Ruin R4–R7) |
| PBS Version Collisions (`v`, `v+100`, `v+200`) | — | **0 / 189** (100% Python-verified) |
