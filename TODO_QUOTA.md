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
- [ ] Register the missing multi-bar bosses (Groudon `:GROUDON_UNDERSANDS` and Giratina `:GIRATINA_DEPTHS` done with the Ch14/15 scripts): Loyal Three (Ch10), the R1 Origin trial (Ruin Route), Pecharunt (Ch18), Wyrmrest Reshiram on `:DRAGONS_DEN` (Ch19), Valen's Zygarde Complete (Ch21), Silvally's conduit bar (Ch21).
- [ ] Arceus `:gym_order` field rotation on `:PRISM_ARENA` (and fix the `:prism_turn` bug).
- [ ] Tag battles: one Mega per *trainer* (engine change, plus a harness check).
- [ ] Groudon `:GROUDON_UNDERSANDS` balance at cap 67 with 13 badges (first capture: Precipice Blades after bar 1 swept a Lv 66 party; the capture had 12 badges, so some of the party disobeyed). Harness it like Kyogre.
- [ ] Kyogre `:KYOGRE_ISENMAR` balance at cap 55 (`design/BALANCE.md` §9d; AI parties at Lv 54–55 lose).

## 3. Teams and hooks
- [ ] Ch15 engine hooks: `pf_echo_follow` (a recorded-path follower shared by the War Convoy's sledges and Gym 14's crypt echo); K6's one-turn `:BLEED` overload (`battle.change_field`); map-level audio mute for the Hush (808); cutscene `CE-1` "AF 290, Through Her Eyes" (letterbox, sepia tone, Glassfall sweep).
- [ ] Balance-check Giratina `:GIRATINA_DEPTHS` at cap 71 with 14 badges. In the first capture, after bar 1 the INVERSE field's "The Reverse World answers the wild Giratina's call!" fired every turn, and a Lv 70 party never reached the Origin bar. Check that hook vs bosses.
- [ ] Partner teams: Redeemed Kestrel (Ch21) and Rook (Ch16 Casting Floor).
- [ ] Ogerpon into Juno's J4 team when `OGERPON_TRUSTED` (a load hook).
- [ ] Aurelia 824–826 `:WATER_SURFACE` overrides for Amaria and Titania.
- [ ] Ruin Route Inverse overlays: Nyx, Celestine, Theodric.
- [ ] Ch11 harpooners at Lv 48–52.

## 4. Wednesday master audit
- [ ] Work through Parts A–J in order (P0 → P1 → P2), skipping what `gemini_recommends/REVIEW.md` marks done and the Gemini-owned layouts (section 1). Part D (staged transitions) belongs to the transitions agent. The economy follows REVIEW.md: a stone/evo clerk, seeds in Marts and an EXP Share, but Rare Candy past the cap only as a password.

## 5. Content density (`design/DENSITY_STANDARD.md`)
- [ ] **Wave 0, the Ch5 rescue:** the 3 softlocks, the 5 missing Gala/Lift trainers, and 16–18 Lock Road and Circuit Gym trainers.
- [ ] **Wave 1 systems:** Glassfall Slivers (100, counter and exchange), the 6-step Trading Chain, the Mystery Egg (Ch3), and `encounters_badgetiers.txt` overlays for Badges 5–9.
- [ ] **Retrofit Ch6–13** to the per-chapter floor (12–20 trainers, ≥3 EventMons, hangouts, Slivers).
- [ ] **Build from each new script's "Density" section** (Ch14 onward): the PBS trainer blocks in 3 versions, EventMons and hangouts.

## 6. Cutscenes, audio and Codex
- [ ] Cutscene P0 engine fixes (letterbox and bust lifecycle, input lock, fade/tint stacking). The two-pillar laws are the style rule. Rewriting existing scenes needs Reuben's sign-off, one scene at a time.
- [ ] Audio v4.3 wiring: `design/MAP_AUDIO.yaml` → mapgen BGS, the 67 trainer-type BGMs, the ME/SE hooks, a selftest-safe `VoiceTicker`, then the cutscene audio matrix.
- [ ] Anime OST pool (`gemini_recommends/2026-11-23_anime-ost-situational-bgm`): Reuben auditions and locks, then the audio agent masters and slots the locked picks. Gemini needs to commit the audition page first.
- [ ] Codex: the class line on cards (CODEX_SPEC), post-game rematch tables (STORY_REMATCHES), gauntlets (G1 in the Ch14+ hub).

## 7. Captures and GIFs
- [ ] Ch14+ key-events GIFs need built maps. Until the maps exist, chapter GIFs use the cast/VS/backdrop harness.
- [x] Drop 13 villain VS GIFs re-shot with class plates (`cast/villains_1..2.gif`).
- [ ] Re-shoot older Warden VS GIFs (`docs/battle_captures/cast/wardens_*.gif`) so they show the new two-line class plates.

---
*Done items stay ticked for a week, then get cleared. Started 2026-11-22. This file replaces the old `design/WED_SPRINT_QUEUE.md`, which now just points here.*
