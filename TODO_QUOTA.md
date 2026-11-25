# To-do: plan-quota work (not usage credits)

**The rule (from Reuben):** usage credits are only for story progress: new chapter scripts, plus the key-events GIF after each one. Everything on this list waits for **plan quota** (the agents resume after the weekly reset, Wed Nov 25, 10am PT). Don't spend credits on it.

**Who reads this:** Claude, the Claude agents, **Gemini** and Reuben. It's the one list. Tick items off (`[x]`) in the same commit that does them. Add new deferred work here, not in a new file. The detail stays in the linked docs.

**Gemini:** the items marked **(Gemini)** are yours. The rest are for Claude's agents, so please don't start them. If a recommend adds work for later, the verdict in `gemini_recommends/REVIEW.md` puts it on this list.

---

## 1. Maps
- [ ] **Pass 2 (Claude refines Claude's own maps):** every row in `mapgen/REFINE_QUEUE.md`. That includes Tap Chamber 255 and the stage-direction pass: bracketed narration becomes move routes, emotes and screen effects (`design/MAPGEN.md`).
- [ ] **(Gemini) Pass 3:** after pass 2, Gemini refines each map in that queue.
- [ ] **(Gemini) Fixes in Gemini-owned layouts** (Wednesday audit): A11 Marram Down 528 (stairs, Headbutt trees), plus the routes_craft, saltmere, lumen and briarwick fixes in Parts A–J.
- [ ] A9 Thistledown Manor 546 and A10 Pageant Hall 145 (Claude-built; Wednesday audit).
- [ ] `mapgen/build.py`: a post-paint BFS reachability check, and gate packaging on `export_tilesets_rxdata.py --check`.

## 2. Bosses and battle engine
- [x] **No-legendary-captures safety net** (Gemini Part B.2): Core `027_LegendaryGate.rb` (`Prismfall.legendary_catch_allowed?` / `story_legendary_locked?`; Legendary / Mythical / UB / Paradox flags + Type: Null, Silvally, Kubfu, Urshifu) deflects every wild ball before S160 (Bosses 004 `pbThrowPokeBall`); `:LOYAL_THREE` registered (Bosses 112: three `:catch => false` bosses + `Prismfall::Bosses.loyal_three`, PARTNER_OGRE if `:ch10_ogre == :ogre`). `PARTNER_OGRE` ("Gossamer Ogre", Ogerpon Lv 48) in PBS; harnessed (winrates_r4 cells L3O/L3M/L3F/L3OA/L3FA: Standard 53–98%, Hard prepared 90–100%). 2026-11-23. Still to do: Hard's "second Pokémon at its side" when alone.
- [x] **Gym 1 Dorian redesign** (Gemini Part C; Reuben's locked Meloetta ace): gen.py + PBS (v0/100/200, and the Pageant Bout v90 Kecleon → Lv 90 Meloetta), Grand Stage `:not_moves => [:RELICSONG]`, Bosses `111_Boss_DorianMatinee.rb` (0.80/0.85/0.78), native Smeargle Sketch rule in `validate_trainers.py`, C.6 story/design text. G1 harness: Casual 93–100%, Standard 42 / 62 / 75% (sparse / good / full), Hard realistic 2–5% after tuning (BALANCE.md §9). 2026-11-23.
- [x] **EBDX sprite fixes** (Gemini Part A.3): Bridge `011_Bridge_SpriteFixes.rb` (FrontShiny/BackShiny → "Front shiny"/"Back shiny" fallback, .PNG retry, scale 1 for single-frame statics ≥160 px with no SpriteScale, 22 Gen 6–9 floaters in `PrismfallEBDX::FLOATING`); `tools/normalize_png_ext.py` (117 renamed in the local engine; run it on `pf_engine_run` too). Real-engine smoke: Juno intro battle OK. 2026-11-23.
- [ ] **EBDX sprite work, rest** (Gemini Part A.4–A.5): stale single-frame files in `Graphics/EBDX/Battlers/Front` (172_1, 483_1, 999: Gemini's engine; ours has none), (the animated-strip importer landed from Gemini in c000368).
- [ ] Register the missing multi-bar bosses (Groudon, Giratina, Pecharunt and Wyrmrest Reshiram `:RESHIRAM_WYRMREST` done with the Ch14/15/18/19 scripts; Loyal Three (Ch10) registered 2026-11-23): the R1 Origin trial (Ruin Route) Valen's Zygarde Complete (Ch21), Silvally's conduit bar (Ch21).
- [ ] Arceus `:gym_order` field rotation on `:PRISM_ARENA` (and fix the `:prism_turn` bug).
- [ ] Tag battles: one Mega per *trainer* (engine change, plus a harness check).
- [x] Groudon `:GROUDON_UNDERSANDS` balance at cap 67 with 13 badges (first capture: Precipice Blades after bar 1 swept a Lv 66 party; the capture had 12 badges, so some of the party disobeyed). Harness it like Kyogre.
- [x] Kyogre `:KYOGRE_ISENMAR` balance at cap 55 (`design/BALANCE.md` §9d; AI parties at Lv 54–55 lose).

## 3. Teams and hooks
- [ ] Ch15 engine hooks: `pf_echo_follow` (a recorded-path follower shared by the War Convoy's sledges and Gym 14's crypt echo); K6's one-turn `:BLEED` overload (`battle.change_field`); map-level audio mute for the Hush (808); cutscene `CE-1` "AF 290, Through Her Eyes" (letterbox, sepia tone, Glassfall sweep).
- [x] Pattern across the Ch14–16 key-event captures: Groudon, Giratina and Zekrom each swept a cap-level AI-played party after their first bar. Check whether the post-break buffs stack too hard for bosses, or whether the demo AI just never switches. Run the Kyogre-style harness on all three. **Ruling 2026-11-24 (Reuben): hard on purpose; only Casual is eased.** The 11-23 rebuild was reverted; Standard / Hard are the original designs, Casual has ×0.5–0.6 offence and no setup move (82–100%). Harness cells BKYO/BGRO/BGIR/BZEK; BALANCE.md §9.
- [x] Balance-check Giratina `:GIRATINA_DEPTHS` at cap 71 with 14 badges. In the first capture, after bar 1 the INVERSE field's "The Reverse World answers the wild Giratina's call!" fired every turn, and a Lv 70 party never reached the Origin bar. Check that hook vs bosses.
- [ ] Partner teams: Redeemed Kestrel (Ch21), `[RIVAL_KESTREL,Kestrel,21]` (the script registers version 21).
- [ ] Ch21 staging: the hijack cutscene, the allies montage (Larch's 11-lamp overlay from `tally(:ENGINE_BREAKS)`), Valen's crystal-spread hook in the Final, the 18 pylon release/refusal kneels, Valen into light, and the ending vignettes keyed by ending ID.
- [ ] Ch20: the Grounds Ladder (12 challengers, Lv 88–90); Valen playable (Interlude V, V119 = 5); the ceremony procession (18 Warden events plus the pylon animation); the white vision; the Night of Masques stage; the consent banners (white/grey by NS §6.2); Kestrel's Gauntlet tear-off battle hook at K8.
- [ ] Ch19 PBS: Sigrun and Marisol partner v19; the war pairs (Isenmar trenchers/hirdmen: new types if missing; Ashkaar soldiers/ember-riders); the Dominar's Toll guard; WAR-1's `legends: false` variant (the Wardens' aces); the badge-case 18-tone chord; the Skaldfast great-hall interior.
- [ ] Ch18: new trainer type `THORNGUARD` (Captain Rowe); the Ogerpon follower (S223, never in the party); Gloaming's permanent-dusk tone and the lantern-moth market.
- [ ] Ch17 PBS and types: new trainer types `SUMP_BARON` (Mother Gutter: partner v17, ledger fight) and `GILDER_AUTOMATON` (the Terrace Warden); Directorate Mallory and Kade; the Sun Court glow sequence (18 lamps, a PC glow overlay). (Rook's Ch16 partner `[LEADER_ROOK,Rook,16]` is done.)
- [x] **The Interlude party/charset swap (shared helper, all five Interludes):** Core `028_Interludes.rb`. `pf_interlude_start(n)` / `pf_interlude_end` / `pf_interlude?(n)` / `pf_interlude_heal` / `pf_interlude_title(n)`; loadouts I–V in `Prismfall::Interlude::LOADOUTS` (I and III load Kestrel's K2+2 / K5 PBS teams, II Rowan, IV Wenlow, V Valen without Zygarde); stash in `Prismfall.state.custom[:interlude]` (save-safe), V119 set/cleared, loadout Pokémon purged from party and boxes on end. Interlude builders: use this, don't write another. 2026-11-25.
- [ ] Ch16 engine pieces: Wenlow's interlude charset and loadout (V119 = 4); the `GO_OVERTIME` timed prompts (3 s each, defaulting to Go); the night-shift foreman patrols on 403 (reuse the Gym 16 sight cones).
- [ ] Ogerpon into Juno's J4 team when `OGERPON_TRUSTED` (a load hook).
- [ ] Aurelia 824–826 `:WATER_SURFACE` overrides for Amaria and Titania.
- [ ] Ruin Route Inverse overlays: Nyx, Celestine, Aurelius.
- [x] **Gilded King rename + rework** (Gemini 2026-11-23, Path B "Aurelius", ids and art renamed THEODRIC → GILDED_AURELIUS / AURELIUS on 2026-11-24): text across story/design/tools, `[GILDED_AURELIUS,Aurelius]` with the treasury nicknames and new LoseText, Festival display "Gilded King Aurelius", the R3 / R6 / R7 scenes (`story/42_SCRIPT_RUIN_KING.md`), mid-battle barks (Z-Power 006), and the wiring: VS_IDS + THEMES (AURELIUS gold; TEO, WICK, ROWAN, MORWEN, DASK, VENAM), Portrait CAST (AURELIUS, VENAM, COLL) and the charset alias guard. 2026-11-23. Open: `mapgen/REQUESTS.md:1118` still says Theodric (another agent's uncommitted file); Reuben's BGM pick (Cosmic Air / Zoltraak / #133).
- [ ] Ch11 harpooners at Lv 48–52.

## 4. Wednesday master audit
- [ ] Work through Parts A–J in order (P0 → P1 → P2), skipping what `gemini_recommends/REVIEW.md` marks done and the Gemini-owned layouts (section 1). Part D (staged transitions) belongs to the transitions agent. The economy follows REVIEW.md: a stone/evo clerk, seeds in Marts and an EXP Share, but Rare Candy past the cap only as a password.

## 5. Content density (`design/DENSITY_STANDARD.md`)
- [x] **Wave 0, the Ch5 rescue** (2026-11-23): the 3 softlocks (Valen at the Veil sets CH5_STEP 10; 608's service door leads back into the vault from step 11; `pfm_cutscene(:SH1)` is real: Cutscenes `016_Movies.rb` plays the Mourner's acting sheets and `Movies/pf_ch5_spire_shatter(_safe).ogv`); the 5 Gala/Lift trainers (Juno partner v13, Thistle v1, Pallbearer v5, Bereaved v5/v6) and the 6 Circuit Gym trainers (routes.py); the Glide Cycles Bicycle (`pfm_has?(:GALAINVITATION)`). Real-engine check: `tools/harness/visual/ch5/009_Ch5VaultCapture.rb` (Shatter → step 9, 608 door → vault, Larch → step 12).
- [ ] **Wave 0, rest:** Interlude I (105/106, V125 12 → 13) isn't built; Lumen Fly point. *(Done 2026-11-25: the Lock Road trainers are in PBS, 30 across 580, 592, 590, 581, 595, 594, 593 and 584; their maps are unbuilt, so they have no events yet.)*
- [ ] **Wave 1 systems:** Glassfall Slivers (100, counter and exchange), the 6-step Trading Chain, the Mystery Egg (Ch3), and `encounters_badgetiers.txt` overlays for Badges 5–9.
- [x] **Retrofit Ch6–13, trainers** (2026-11-25): 25–34 route, gym and dungeon trainers per chapter in `routes.py` and PBS (3 versions each); counts per stretch are in `design/TRAINER_COVERAGE.md`. PBS only: none of those maps is built, so every one still needs its event.
- [ ] **Retrofit Ch6–13, rest:** ≥3 EventMons, hangouts and Slivers per chapter.
- [x] **Trainer species coverage** (Reuben's rule, 2026-11-25): every non-legendary species (900) is on a generic trainer at a plausible level; `python3 -I tools/trainer_gen/coverage.py` checks it and rewrites `design/TRAINER_COVERAGE.md`. Re-run it after any trainer edit. Open: regional forms (0 of 55 on generic trainers; the report lists them).
- [ ] **Build from each new script's "Density" section** (Ch14 onward): the PBS trainer blocks in 3 versions, EventMons and hangouts.

## 5b. Post-game build (`story/41_SCRIPT_POSTGAME.md`)
- [ ] The `:POSTGAME` Trials category and the Registry board; the Tier 1 cards first (the T1-1 … T1-8 boss registrations with `:catch => :last_bar`; Gemini Part B.3 with the script's continuity fixes); Hesper's lighthouse scene; the Zygarde memorial; the Gauntlet's empty pedestals; the Concord Zero sub-basement.

## 6. Cutscenes, audio and Codex
- [x] Cutscene P0 engine fixes from the cinematics spec §2.0 (2026-11-23): `hitstop` / `slowmo(0)` on the wall clock (no more deadlock), `bgm_cut` / `bgs_cut` and BGS memorize/restore, captions clear the letterbox bars; selftest 159/159 (the no-art portrait checks now use Delphine / Kassan: Martin and Wenna have art). Plus `016_Movies.rb` (play_movie, acting sheets).
- [ ] Cutscene P0, rest (Wednesday audit wording): bust lifecycle, input lock, fade/tint stacking. The two-pillar laws are the style rule. Rewriting existing scenes needs Reuben's sign-off, one scene at a time.
- [ ] Audio v4.3 wiring: `design/MAP_AUDIO.yaml` → mapgen BGS, the 67 trainer-type BGMs, the ME/SE hooks, a selftest-safe `VoiceTicker`, then the cutscene audio matrix.
- [ ] Anime OST pool (`gemini_recommends/2026-11-23_anime-ost-situational-bgm`): Reuben auditions and locks, then the audio agent masters and slots the locked picks. Gemini needs to commit the audition page first.
- [ ] Codex: the class line on cards (CODEX_SPEC), post-game rematch tables (STORY_REMATCHES), gauntlets (G1 in the Ch14+ hub).

## 7. Captures and GIFs
- [ ] Ch14+ key-events GIFs need built maps. Until the maps exist, chapter GIFs use the cast/VS/backdrop harness.
- [x] Drop 13 villain VS GIFs re-shot with class plates (`cast/villains_1..2.gif`).
- [ ] Re-shoot older Warden VS GIFs (`docs/battle_captures/cast/wardens_*.gif`) so they show the new two-line class plates.

## Status: finale bosses agent (Bosses 113–115, Arceus rotation, Mega per trainer)
*Running note, so the work can be picked up if the agent is cut off (2026-11-25).*
- **Committed checkpoint 1:** `:prism_turn` / `:prism_interval` fix (Bosses 005 `prism_state` returns the arena's live Hash); `:PRISM_ARENA` `:set_order` / `:gym_order` (Field Effects 136, 004 `borrow_pool` override); Arceus 103 (bars by story variant, `:prism_order`, forced locks, HARMONY_BUFF, bar-7 Legend / Inverse phase); new boss keys `:prism_order`, `:end_of_round`, `:follow_prism[:items]`; Bosses 113 Valen's Zygarde, 114 Voss / Quent's Silvally, 115 Giratina Origin trial; `Prismfall::Festival::Draw` alias (Core 015); `tools/harness/run_finale_bosses.rb` (48/60 at the checkpoint: the failures are test-script bugs listed below, plus the Silvally `forced_form` fix just made in Bosses 005 `change_form`).
- **Next:** (1) `run_finale_bosses.rb`: `fresh` must replace `$prismfall` (state leaks between runs), restore PP in the scripted chooser, read boss ids before the battle strips them; get to 60/60. (2) Mega: `PrismfallMega::LIMIT = :trainer`, pass the partner's ring through `pbRegisterPartner`, `run_mega.rb` section 5 + a tag-battle check, `design/MEGA_EVOLUTION.md` §3.2. (3) `winrates_r4.rb` cells (VALEN / VOSS / QH rerun, new VOSSC, BORI, ARC*) and `design/BALANCE.md`. (4) Tick the three §2 lines.

---
*Done items stay ticked for a week, then get cleared. Started 2026-11-22. This file replaces the old `design/WED_SPRINT_QUEUE.md`, which now just points here.*

## Status note: trainer coverage agent (2026-11-25)
- Done: `tools/trainer_gen/coverage.py` + `design/TRAINER_COVERAGE.md`; 263 new generic trainers (Ch5 30, Ch6–13 231, two Ch19 roster rows: Isolde, Hjal & Ama) in `routes.py` and spliced into `pbs/trainers.txt`; coverage 175 → 900 / 900; validate 0 errors.
- Left: map events for all of them (maps unbuilt); regional forms as a bonus pass (`m(..., form=n)` works in routes.py now); the Ch14–18 script rosters and the rest of Ch19's are still unbuilt (TODO §5 "Build from each new script's Density section").

## Agent status: Ch15–21 + post-game engine hooks (Claude, engine-backlog agent)
*Running note so the work can be picked up; updated at each checkpoint.*
- **Committed:** Core `028_Interludes.rb` (the shared swap), `029_TimedPrompts.rb` (`pf_timed_choice`, `pf_overtime`), `030_Ceremony_Ladder.rb` (`Prismfall::Ceremony.procession` / `.banner`, `Prismfall::GroundsLadder`); Field Effects `013_FieldEffects_StoryHooks.rb` (K6 one-turn `:BLEED` overload, K8 Gauntlet tear-off, Valen crystal stage + `:prismfall_valen_crystal`); `mapgen/ruby/013_EchoFollow.rb` (`pf_echo_follow`: convoy + crypt record/replay), `014_Hush.rb` (map 808 mute + ripples).
- **Grounds Ladder PBS contract:** `GroundsLadder::ROSTER` expects version 20 blocks: PAINTER Linnet, FISHERMAN Brynjar, ROCKER Vix, ENGINEER Dobbin, GAMBLER Quill, TAMER Asgerd, YOUNGSTER Tam, RUINMANIAC Nasrin, CHANNELER Osric, SCIENTIST Thessaly, COOLTRAINER_M Halvard, LADY Liesl (Lv 88–90, two Pokémon each). Other names/types: edit ROSTER (a same-name block under another type is found automatically). Missing blocks are skipped, never a crash.
- **Next, in order:** (1) `mapgen/ruby/018_Crownhaven.rb` ceremony walk + pylon lighting + the white vision; (2) Core `031_Finale.rb` (hijack hook points, allies montage + Larch's 11 lamps, tag foes/partner, the 36 kneel lines on `:prismfall_arceus_locks`, ending vignette table) and Cutscenes scenes for them; (3) Trials `:POSTGAME` category + Registry board (`115_Quests_Postgame.rb`), tier switches S279/S285; (4) `tools/harness/run_story_hooks.rb` (headless checks) and the Cutscenes selftest.

## Status: Ch16–21 + post-game trainer PBS (agent, 2026-11-25)
*Running note so the work can be picked up. Source of every block: `tools/trainer_gen/gen.py`, the section "CH16-CH21 STORY FIGHTS, THE GROUNDS LADDER AND THE WARDEN'S GAUNTLET". Check with `python3 -I tools/check_script_trainers.py` (scripts vs PBS) and `python3 -I tools/validate_trainers.py`.*
- [x] Ch16: Officers Grane and Tull (Interlude IV, Lv 60–62, no Bag).
- [ ] Next, in order: Ch17 (SUMP_BARON, GILDER_AUTOMATON, Mallory/Kade), Ch18 (THORNGUARD Rowe), Ch19 (partners v19, the lines, the Toll, Thornwatch), Ch20 (the Grounds Ladder), Ch21 (Redeemed Kestrel partner), post-game (the Warden's Gauntlet).

## Agent status: Interlude I + Map Pass 2 (Lamplight agent)
- 2026-11-25: Interlude I "Lamplight" is written and builds (commit 4674a4e): `mapgen/layouts/story_interlude1.py` (a story layer that upserts its events into the specs of 952 / 182 / 105 / 106 by name; run it again after any layout regenerates one of those specs), `mapgen/ruby/016_Staging.rb` (pfm_fade_out / pfm_flash / ... for stage directions), `mapgen/ruby/017_Lamplight.rb` (pfm_il1_*). It uses Core `028_Interludes.rb` loadout 1. **Next:** real-engine capture (`tools/harness/visual/ch5/010_LamplightCapture.rb`), then 255 Tap Chamber, then the bracketed-narration pass.

## Status: Ch16–21 + post-game trainer PBS agent (2026-11-25)
*Running note so the work can be picked up. Source of every block: `tools/trainer_gen/gen.py`, the section "CH16-CH21 STORY FIGHTS, THE GROUNDS LADDER AND THE WARDEN'S GAUNTLET". Check with `python3 -I tools/check_script_trainers.py` (scripts vs PBS) and `python3 -I tools/validate_trainers.py`.*
- [x] Ch16: `[MERIDIAN_DIRECTORATE,Grane]` / `[...,Tull]` (Interlude IV, Lv 60–62, no Bag).
- [x] Ch17: `SUMP_BARON` Mother Gutter (partner v17 + the ledger fight v0), `[MERIDIAN_DIRECTORATE,Mallory]` + `[...,Kade]` (the barricade tag double), `GILDER_AUTOMATON` the Terrace Warden.
- [x] Ch18: `THORNGUARD` Captain Rowe (`[THORNGUARD,Captain Rowe]`, Lv 75–77).
- [x] Ch19: partners `[LEADER_SIGRUN,Sigrun,19]` / `[LEADER_MARISOL,Marisol,19]` rebuilt to the script; the lines (`ISENMAR_TRENCHER` Ulfa, Bersi; `ISENMAR_HIRDMAN` Hjalmar + Torunn, Styr; `ASHKAAR_SOLDIER` Garrok, Senna; `ASHKAAR_EMBER_RIDER` Vharn + Ashild, Kessa); the Toll `[ASHKAAR_OFFICER,Orrin]`; `[THORNWATCH,Brome]`. Maps 920–926 (mapgen/layouts/war.py) still call the Rev 18 "Soldier"/"Captain" blocks and stage the partner double on 926: re-wire them to the script.
- [x] Ch20: the Grounds Ladder, 12 challengers Lv 87–90 with 12 new classes (WEAVER, HARPOONER, STREAMER, FOREMAN, MOON_BROKER, WYRM_RIDER, LAMP_RUNNER, WELL_KEEPER, LANTERN_ACOLYTE, EMBALMER, WARDGUARD, CANTOR); roster table in story/39.
- [ ] Next, in order: Ch21 (Redeemed Kestrel partner), post-game (the Warden's Gauntlet).

## Status: Audio v4.3 wiring agent (2026-11-25)
*Running note so the work can be picked up. Checks: `python3 -I mapgen/map_audio.py --check`, `ruby "plugins/Prismfall Cutscenes/selftest/voice.ruby_stub"`, the Cutscenes selftest.*
- [x] Checkpoint 1 (commit 43a6ec2): `design/MAP_AUDIO.yaml` (117 maps) → `mapgen/map_audio.py` → `maps_out/Plugins/Prismfall Maps/013_MapAudio.rb` (run-time, installed files only); `Prismfall Core/031_AudioCues.rb` (cues, stock stand-ins for trainer BGMs, title, boss / field SE); badge / trial-rank / game-over jingles; default wild boss music; the nine v5 field-audio BGS in `audio/gemini_cc0/BGS`. Trainer-type BGMs are in `pbs/trainer_types.txt` (went in with f0c31c3); the VS lightning cue is in `010_Bridge_VersusIntro.rb` (went in with afad6dd).
- [ ] In the tree, not committed yet: `plugins/Prismfall Cutscenes/014_Portraits_Voice.rb` (VoiceTicker) + `selftest/voice.ruby_stub`, the AUDIO cue matrix in `001_Config.rb`. Then: one real-engine check (a map's BGS, a trainer battle's BGM), the v5 BGS verdict in `gemini_recommends/REVIEW.md`, tick §6.
