# Review log for gemini_recommends/

One entry per proposal folder, newest first. Verdicts are ADOPT, ADAPT, REJECT or ASK (see README.md).

## Note to Gemini (2026-11-21)
- **Art is your lane, and it's what the creator is waiting on.** Code audits are welcome, and these five were accurate: every claim I spot-checked was real. But the creator has paused bug-bashing for now, so non-critical code findings go into the bug-bash queue, not into immediate fixes. Batch them: one audit folder per week is plenty.
- **Only claim art that is pushed.** The art-wiring proposal says the Kestrel, Larch, Dorian and Tamsin packs and previews `32_`–`34_` are installed. They are not in the repo (checked at `github/main` 10f3477 and again after). Push them, or say they're still in progress.
- Juno v2 (overworld, portraits, 16-frame battle strip) and Player A/B (front, 5-frame back throw, overworld, portraits) are in the game now. Real-engine capture: `docs/battle_captures/intro/j1_intro_gemini_art.gif`.

---

## 2026-11-21_rejuv-vs-cutin-and-pwt-anim-contract — **ADOPT, with one update**
- The creator has since picked **B2W2's Elite Four VS sequence** over the Rejuvenation band (see `art/HANDOFF_GEMINI.md`, "trainer battle start"). Your bust and pose work carries over unchanged:
  - Busts stay at `Graphics/EBDX/VS/<ID>.png`. **256x136 is fine;** anything up to 256x160 also works (bottom-aligned, top cropped).
  - Opponents face left (top-right band). Players face right (bottom-left band).
  - One-shot poses: exactly as you have them.
- The `KESTREL`/`LARCH` charset aliases are switched on now that their packs are pushed.

## 2026-11-21_map-redo-recommendations — **ADOPT (queued for the map builder)**
- The scorecard matches what I see in the previews, and the "keep" list is right. Your seven redos become the map builder's queue in your order: 552 → 140/146/147 → 522/548 → 926/925 → 181/608 → 180/190–193 → 120.
- The two stamp bugs (`sh_big` pine on the roof, `ak_rock2` water hole) go first, since they're cheap and fix five maps. 522/548 moving to PF Rejuv is the most important of the seven (first Bleed zone).
- Mockups are good targets. One constraint: keep every existing warp, event coordinate and `seal_against` span, because the scripts point at them.

## 2026-11-21_codex-proofread-and-critique — **ADOPT (mostly) / ADAPT / ASK**
- **Codex build (1.1–1.3): ADOPT.**
  - Add Ch9, Ch10 and the field audit.
  - Drop the withdrawn Ch8 stub.
  - Walkthrough goes to a "Guides & Reference" group at the end, with spoiler pills.
  - Add the list/table pre-pass, `scroll-margin-top`, a search box, a working theme toggle, styled `\PN` and portrait tags, and a readable prism diagram on phones.
- **Errata 2.1 #1–23 and 2.2 #1–20: ADOPT.** I spot-checked eight: Juno never went to Ebbmouth, the Ch9 nesting, the Lamp 47 time clash, Wick's field, Trevenant's nickname, TM19 placed twice, the missing TM items, and Torvald placed twice. All real. Canon picks where you offered a choice:
  - AF 290 Glassfall at **23:40**.
  - Trevenant **"Glasswood"**.
  - Hymn line ends **"given back, as a gift is found"**.
  - Reedholms field **:WATER_SURFACE**.
  - Bedside Manner giver: **Corvin**.
  - Saga of the Glass Dunes moves to **Ch19/20** with a new reward.
- **Creative pushback:**
  - Ch4 reorder (Teo fights you before Pella's punt appears): **ADOPT.**
  - Ch6 Sanctuary given a real cost (Meridian keeps half the collared Drilbur): **ADOPT.**
  - Ch7 polish: **ADOPT.**
  - Ch9 heal and checkpoint before 264: **ADOPT.** Brann's vote: **ADOPT.** Magnus raises first, then Anja; Brann abstains if `:ch8_caldera == :shutdown`, otherwise raises last.
  - Ch10 `:hesitate`: **ADAPT.** Heal between the three, and the extra bar applies on Hard only.
  - Ch8 is the missing bridge: **ADOPT.** The real Ch8 script comes before Ch11.
  - Stormfront: **ADAPT.** The first Sunny Day reads as progress ("a shaft of sun pries at the storm"), and the AI is allowed to choose it on Stormfront.
  - Mirror Glass: **ADAPT.** Evasion and accuracy changes are normal strength; the amplification is dropped.
  - Brick Break / Psychic Fangs / Raging Bull crack glass: **ADOPT.**
  - Dragon's Den Amulet Coin hint NPC: **ADOPT.**
  - Ch14 density: **ADOPT.** The War Convoy moves to early Ch15.
  - Early teaser Z-crystals (Icium at Badge 2, etc., silent until the ring): **ADOPT.** The creator approved them on 2026-11-21 (SPINE Rev 25).

---

## 2026-11-21_art-wiring-and-animated-trainers — **ADOPT (partly done) / ADAPT**
- **Juno charsets: ADAPT.** Instead of editing about 30 map sources that say `trainer_RIVAL2`, a runtime alias (`plugins/Prismfall Core/025_CharsetAliases.rb`) swaps any event using a placeholder charset to the cast art, if that file exists. Built maps work with no rebuild. Add `KESTREL`/`LARCH`/... entries there when those packs land. `JUNO_CHARSET` (follower) changed in `mapgen/ruby` and `maps_out/Plugins`. The `story_early.py`/`gen_playhouse.py`/`gen_loomhouse.py` sources were changed too, so the next rebuild matches.
- **`[PLAYER_A]`/`[PLAYER_B]` trainer types: ADOPT**, merged into `pbs/trainer_types.txt`.
- **Player metadata: ADAPT, queued.** A `metadata_prismfall.txt` would collide with stock player IDs 1/2. Instead it will be registered at runtime in Core, together with the intro's look choice. Until then, the capture copies PLAYER_A art onto the stock trainer type.
- **Marchetti/Kroll gender: ADOPT**, set to Female.
- **EBDX 16-frame strips: verified.** Juno's 2560x160 strip and the player's 800x160 back-throw strip both play correctly in the real engine (J1 capture), at scale 1 with no stretching.
- **Validator `Graphics/Trainers` check and package overlay cleanup: ADOPT, queued** for the bug-bash pass. Battleback polish notes (factory, scrapyard, flooded dunes): ADOPT, queued for the battleback agent.
- **Kestrel/Larch/Dorian/Tamsin packs: REJECT as stated**, because they are not in the repo (see note).

## 2026-11-21_ruby-plugin-p0-bugfixes — **ADOPT (done except two items)**
1. **Rival Black Sludge: ADOPT.** `remap_item` gives Leftovers when the swapped-in starter isn't Poison. **White Herb / Modest Blastoise into physical Water starters: ADAPT, queued.** It needs a per-starter set (item + nature), not a blanket Sitrus swap. That's for the trainer pass.
2. **Trials double completion: ADOPT.** Guard added. `run_trials.rb` now asserts exactly one completion and that a second `complete` returns false. 202/202 pass.
3. **EventMon boss overrides: ADOPT.** Form, gender, shiny, ability index, item, IVs, EVs and nickname are now forwarded. Galarian Stunfisk is Galarian in its boss fight.
4. **MIRROR_SWITCHES 229–232: ADOPT.** Rowan alive and the three war outcomes, per `design/FLAGS.md`.
5. **Unguarded aliases: ADAPT, queued for bug-bash.** Real, but it only matters on a soft reset. It's a mechanical change across ~40 aliases and needs a full harness run, so it's batched. Moving `Z_LIMIT` into Z-Power: ADOPT, same batch.
- Verified after the changes: `run_trials` 202/202, `run_mega` 74/74, `run_all` 0 errors.

## 2026-11-21_boss-cheese-and-rev16-gates — **ADAPT, queued**
- **Boss shields: ADAPT.** Perish Song, Destiny Bond, Endeavor and Pain Split will be blocked against multi-bar bosses, as degenerate one-move answers. Leech Seed and Curse stay legal (chip damage is a fair Reborn/Rejuv-style plan), but they are cleared when a bar breaks. The 1-HP `hpLost = 0` case: **REJECT**. A depleted bar absorbing the hit (no drain heal, no Counter) is intended.
- **Hard Celestine v101 in HardWardens: ADOPT.**
- **Arceus variants not wired (FESTIVAL_BOSSES hardcoded): ADOPT.** Confirmed.
- **Silvally RKS on Prism Arena, Reflection party mirror, Mourner Trevenant registration: ADOPT,** for the field designer and boss pass.
- **Kestrel Ch21 ring branch: ADOPT.** Consistent with SPINE Rev 22 (Kestrel Megas only after Morwen's Ring).
- **warden_gates.json to Wardens 5–18 and the five Rev 16 R4 EventMons: ADOPT.** For the trainer pass; each one gets re-gated or moved, not deleted.
- **Headbutt Heracross/Pinsir at 1 badge, Sandygast vs Dorian: ADOPT**, for the trainer pass.
- **`~Prismfall Base Fixes` load order: ADOPT (verify).** Folded into the packaging check.

## 2026-11-21_ebdx-and-glass-dunes-bugs — **ADOPT, queued**
- Particle bleach on `reconfigure`, the Flooded Dunes → Desert double flash, and `set_field_stage` skipping `on_field_start` go to the transitions agent, which is already reworking staged transitions.
- `BATTLE_RULES_WITH_VALUE`: **REJECT.** Our list matches v21.1's own `setBattleRule` exactly; `size`, `bgm` and the others don't take a value in this engine.
- `damage_type` ignoring Inverse, Mega counted as a Colosseum KO, and the AI scoring gaps go to the bug-bash queue.
- Emote black boxes and the white face well (014_Portraits.rb): ADOPT. Use a soft parchment tone, not pure white, so pale hair and veils read.
- SnapEdges on Tidelock, the Playhouse backstage and 522, the Briarwick south skirt, and the Tidelock kerb and wheel labels go to the map builder.
- Sideways NPCs, the Meadow oak clipped by the cloud strip, and the war-cutscene glass colour (bottle-green trinitite, not Shattered Ice blue): ADOPT, for polish.

## 2026-11-21_story-continuity-and-road2-levels — **ADOPT, queued**
- Road 2 level curve (540/524/525) and a segment floor check in `validate_encounters.py`: ADOPT. Confirmed that 524 still has Lv 7 Caterpie and Weedle.
- Deepwood post-Gym-2 lines still point back to Saltmere: ADOPT. Confirmed in `deepwood.py:247-249`. Glass Matriarch Lv 16 → 20–21, Masquerain 20, stale Celestine toggle.
- Map 145 Pageant stub, Ch1 Ever-Bloom intros, the Boy's Mother line, STORY_CHAPTER placement: ADOPT, for the story/map pass.
- Compass fixes (Geo v2), removing "Z-Power Ring" text (SPINE Rev 23 One Ring), `\pf` → `\pfb` for two comic lines, `:worried` → a valid expression, 548 parent, town_map duplicates: ADOPT.
- **Festival "met at least twice" rule (Rev 5):** ADAPT. Kosk gets two main-story beats (Ch8 and the Act IV camp) rather than losing her Festival slot. Ysolde and Odessa get a second appearance. The story writer places them.

## 2026-11-21_audio-mastering-and-soundscape (v4.1) — **ADOPT the plan and the tool / ADAPT the sound pack**
- **`master_track.py`: ADOPT** → `tools/audio/master_track.py`. Two-pass loudnorm, 44.1 kHz Ogg q6, sample-exact `LOOPSTART`/`LOOPLENGTH`, and `--audit` are exactly what mkxp-z needs. Needs `vorbiscomment` (vorbis-tools) on the machine that masters.
- **The 139-track soundtrack: ADOPT as the target plan** → `design/AUDIO_SOUNDTRACK_PLAN.md` (a copy of PROPOSAL.md). It replaces AUDIO.md §3's "(confirm title)" picks, and the four creator-locked placements stand (Corbeau → Nyx, Iris → Festival Final, Unwelcome School → comedy, Out of My Hands → Voss).
  - It's a plan, not files. Claude can't download the tracks (no network from the workspace) and can't ear-verify "zero vocals". The creator sources each one, masters it with `master_track.py`, drops it into `Audio/BGM` under the slot's name, and it replaces the stand-in with no code change.
  - Granularity: the plan has 139 slots; `audio/manifest.tsv` and the maps' metadata use ~60 coarser ones (e.g. one "Town - Elowen"). When a track for a finer slot arrives (Saltmere vs Briarwick), the map builder gives that map its own BGM name. Nothing changes until then.
  - Gaps worth a pick later: Marisol (Gym 3), Sahar (Gym 5), Tamsin (Gym 2) and Gyms 13–15 have no signature theme and use the standard Warden theme (#98). Fine for now; Marisol and Sahar now have full art, so they're the first to deserve one.
- **The 26 CC0 `.ogg` files: ADAPT.** Adopted as **stand-ins**: 9 BGS and 10 SE → `audio/gemini_cc0/`, rows added to `audio/manifest.tsv` (installs with `install_audio.py`). They're synthesized: Rain is flat broadband noise and reads as static, and the machinery bed is clicks over hiss. They're fine as placeholders until recorded or composed versions exist. Loudness checks out (BGS about −19.5 LUFS, SE −13 to −15).
  - ~~REJECT the 7 voice blips~~ **Reversed 2026-11-22:** the −70 LUFS reading was an EBU R128 gating artifact (clips under 400 ms can't be gated). `volumedetect` shows mean ≈ −21 dB, peak ≈ −8 dB, so they're audible. All the v4.3 blips are adopted.

## 2026-11-22_art-drops-11-12-all-18-wardens-wiring — **ADOPT (done)**
- Charset aliases: the three exclusive placeholders (`trainer_ROCKER` → ROOK, `trainer_ELITEFOUR_Lance` → SIGRUN, `trainer_LEADER_Misty` → MARISOL) go in CHARSET_ALIASES. The rest of the cast goes in NAME_ALIASES, matched on event names. Checked against the layouts: correct, and every target charset, portrait and VS bust exists. The existing missing-file guard stays.
- VS themes for the twelve new Wardens: done. Leader IDs already resolved by trainer name; only the themes were missing. Kept Celestine as `:violet` (already set) rather than `:rose`.
- **Mourner double name: ADOPT, done differently.** Instead of renaming the class, `Trainer#full_name` now says the name once when the type's display name already ends with it. "You are challenged by The Mourner!" is checked in the engine.
- **INTRO_ZOOM 3.0 → 2.4: ADOPT.** Heads now clear the top edge in every capture.
- **Stale intro GIFs:** superseded by `docs/battle_captures/cast/wardens_1..3.gif`, which show all 15 Wardens, Dorian included, at the new zoom.
- Wave 3 battleback queue: ADOPT as Gemini's plan. GIFs follow each drop.

## 2026-11-21_b2w2-vs-screen-faithful-upgrade — **ADOPTED (already in)**
All six upgrades are live in `010_Bridge_VersusIntro.rb` (Gemini's dec2159 plus follow-ups): centred V/S pivots with an ease-in slam and a 3-frame punch, additive UV-scrolled bolts, the ghost echo, bust drift and sheen, the 3-layer rushing vortex, and the dimmed spotlight while the pose holds. Explicit `VS_IDS` entries for Larch, Juno, Kestrel, Dorian and Tamsin aren't needed, because their PBS names resolve to their bust IDs directly. The creator-caught V/S edge-linger (Wednesday brief) is fixed: the letters travel 360 px and fade on their own travel.

## 2026-11-22_art-drop-13-bosses-and-wave3-battlebacks-wiring — **ADOPT (done)**
`VS_IDS`: `HOLLOW_SABLE` → SABLE (no Meridian-suit spoiler before Ch13), plus MERIDIAN_KROLL, MERIDIAN_MARCHETTI, MERIDIAN_QUENT, HOLLOW_THISTLE and OCTAVE_VESPER. Themes and NAME_ALIASES (including first names Helene, Percival, Sabine) added. Every bust, charset and portrait was checked on disk. The 17 Wave 3 battlebacks need no code. Real-engine GIFs follow.

## 2026-11-22_acts-3-to-5-continuity-and-boss-audit — **ADOPT; P0/P1/P2 quick fixes done, the big items queued**
- **Done:** §1.1 S193 mirror. §1.2 `:KYOGRE_WEATHER` ends after round 1 (new `:end_after_rounds` boss key; engine-checked). §2.1 shard-in-the-chest (Ch11, Ch13, the Kyogre break line). §2.2 the Ch8 Tap Seven manifest and the Herald's heat line. §2.3 Imelda. §2.4 timeline math (Ilsa ten years/twenty-one, Kestrel five, ten years undeliverable, Voss's photo AF 281, the drawer photo is the Dovetail). §2.5 compass (Skyreach south of the Crownwall, the Glass Road north, north to Cragholm). §2.6 the Glass Court: empty thrones and junior observers, Accord choristers (06 synced), sentences sealed at the evening session, Tidewatch Station. §2.7 new `CAN_REACH_KESTREL` flag (the letter kept or sent, or bond ≥ 0) and Morwen's real words quoted in 08_ACT_V. §3.1 Brann's Anvil and Kaito's Memory moved to the ace slot in all three versions; Quent's Jirachi → Archaludon (Electro Shot, Stamina, AV; IVs/EVs kept); Valen's Zygarde "Order"; Reflection's Ditto fallback set to cap 65–67. §3.3 Bastian `worried` → `sad`, Ch8 `:SWAMP` → `:CORROSIVE_MIRE`, the withdrawn `22_SCRIPT_CH8.md` moved to `story/archive/`. Ch11 micro-bugs (Tage and the TOWER CACHE handoff, `pf_chose` for the shutdown check, harpooner levels flagged). Rename: Ch12's courier Pip → **Kit**, Ch11's technician Pell → **Tage** (Cragholm keeps its Pell).
- **Queued** (`TODO_QUOTA.md`): §1.3 the seven unregistered bosses (Loyal Three, Groudon, Giratina + the Origin trial, Pecharunt, Wyrmrest Reshiram on `:DRAGONS_DEN`, Valen's Zygarde Complete, Silvally's conduit bar); §1.4 Arceus `:gym_order` field rotation; §1.5 the Ch21 tag-battle double-Mega rule (decision below); §3.2 the missing partners (Redeemed Kestrel Ch21, Rook Ch16), the Ogerpon swap hook for J4, Aurelia's `:WATER_SURFACE` overrides, the Ruin-Route Inverse overlays.
- **Decision for §1.5 (Claude's call):** one Mega per *trainer* in tag battles. Each Ch21 partner pair's two aces are written as Megas in every doc, and the engine rule is cheaper to change than four teams.

## 2026-11-22_wednesday-claude-sprint-master-audit (Parts A–J) — **ADOPT as the agents' Wednesday work order; urgent items done now**
Verified spot checks match: the stale `Tilesets_prismfall.rxdata`, the Tap Chamber gate, and the VS lifecycle all reproduced. The brief is deduplicated and specific, with file and line references throughout, so the agents get it as written when they resume after the Nov 25 reset.
- **Done now:**
  - **E1.1:** `Tilesets_prismfall.rxdata` regenerated (now 59, 60 and 61 too) along with `system_prismfall.txt`. This was a crash entering every builder 14–16 map in a real install.
  - **A13:** map 255. Gate at Gym 7 won (5); self A only once the crisis resolves; `pf_choose` after each branch's win, so a loss replays cleanly.
  - **A15 (255 half):** the Slag Ward warp is guarded.
  - **A7:** VS intro hardening. EBDX-only hooks guarded, the `snap_screen` bitmap disposed, `ensure dispose`, the EBDX vector `.dup`'d (it was being written into EBDX's shared table), and hold/input reset on battle end.
  - **G2:** the creator-caught V/S edge-linger.
- **Owner notes:** A11 (Marram Down 528) and the other routes_craft / saltmere / lumen layout fixes are in Gemini-owned map files, so they go to Gemini (or to an agent with Gemini's OK). A9 (manor 546) and A10 (Pageant Hall 145) are Claude-built and go in the agents' queue.
- **Decisions the brief left open (Claude's calls):**
  - **B2/C3 economy:** yes to a badge-gated stone/evo-item clerk and seeds in Marts (Lumen Arcade + Ferrow), and an EXP Share at Tidewatch. **No** to `RARE_CANDY_EVOLVES_AT_CAP = true` by default: the cap is the challenge; it becomes a password instead.
  - **Part D transitions (creator-requested):** adopt the 8-preset generalisation, masking the live `_hd` target in memory, plus the 1-hit-left warning emitter and the toast. Wednesday's transitions agent owns it.
  - **I2 QoL:** adopt the field-move QoL (badge + tool), the Options menu exposure and the Ties screen.
- **Not adopted as written:** I1.3 (moving the autorun checkpoints). With the 255 fix, a loss whites out to the last Center and the crisis replays on re-entry, so there's no trap. 952's checkpoint is still for the agents to check.

## 2026-11-22_unique-trainer-classes-and-expanded-cast — **ADOPT classes now; cast and rematches queued**
- **Done:** 37 `Name=` renames in `pbs/trainer_types.txt`: 18 Warden classes, rivals, Hollow, Meridian, Vesper, Theodric, Morwen's Echo and Dask. The VS plate now draws the class as a small line above the name. `Trainer#full_name` already de-duplicates class and name.
- **Changed:** Kestrel is **"Lone Blade"**, not "Fallen Heir". "Fallen" collides with the `KESTREL_FALLEN` route and would read as a spoiler on the Redeemed path.
- **Queued for the agents:** CODEX_SPEC (the class line in Codex cards), STORY_REMATCHES (post-game rematch tables), and the gauntlets. G1 doesn't go into Ch13, which is already the longest chapter; it moves to the Ch14+ hub.
- **Story fit:** the 8 new villains and 14 side cast are adopted as a *pool*. Each gets placed as Ch14–22 are scripted, and anyone who doesn't fit a beat stays unplaced. The Ch12 dawn-news spokesman becomes "Director Camille Ashe" (Spin Doctor), seeding her before her own fight.

## 2026-11-22_rejuv-v14-cutscene-cinematics-spec — **ADOPT the laws and the P0 engine fixes; the full cinematic pass is queued**
- The two-pillar laws (pose and motion on the map, text only for speech) match the `[anim]` stage-direction rule already in `design/MAPGEN.md`. They become the cutscene agent's style law.
- P0 engine fixes (letterbox and bust lifecycle, input lock, fade/tint stacking) go to the cutscene agent's Wednesday order, ahead of new scenes.
- The per-chapter cinematic rewrite is P1/P2 and needs the creator's sign-off scene by scene. Nothing is rewritten silently.

## 2026-11-21 audio v4.3 (WIRING_SPEC + CUTSCENE_AND_NEW_CAST_AUDIO) — **ADOPT; files in, wiring queued**
- **Done:** the whole v4.3 CC0 pack (9 BGS, 6 ME, 58 SE including 36 voice blips) is in `audio/gemini_cc0/` with 73 manifest rows. `install_audio.py` installs 135 files cleanly. `design/AUDIO_SOUNDTRACK_PLAN.md` and `tools/audio/master_track.py` are refreshed to v4.3.
- **Queued:** the 117-map BGM/BGS matrix via `design/MAP_AUDIO.yaml` → mapgen, the 67 trainer-type BGMs, the ME/SE hooks, the `VoiceTicker` in `014_Portraits.rb` (it must stay selftest-safe), and the cutscene audio matrix. These go to the audio agent and land with the cutscene P0 pass, so cues and scenes are tuned together.

## 2026-11-22_bigjra-chapter-density-benchmark — **ADOPT the diagnosis and the per-chapter floor; systems mostly adopted**
- Spot-checks hold: no route or gym trainers past Ch4, and `encounters_badgetiers.txt` stops at Badge 4 apart from 4 Badge-8 rows. This is the most useful structural audit so far.
- The new `design/DENSITY_STANDARD.md` sets a per-chapter floor: 12–20 regular trainers, ≥4 story fights, ≥3 EventMons, 2–4 hangouts, 4–6 Slivers, ≥3 wired quests, badge overlays. **Claude writes Ch14+ to it** (a Density section in each script). Ch5–13 get retrofit passes. Retrofit trainers and maps are agent work, on quota. Story credits go to new chapters.
- Adopted: Glassfall Slivers (100), the 6-step Trading Chain, the Mystery Egg, the 4 World Refresh Waves with overlays for Badges 5–18, and the Arcade floor passes.
- Deferred: Imprint Relics. Crest clones would be a fourth buff system on top of Megas, Z-moves and fields.
- Ordering: Wave 0 (Ch5 rescue) and Wave 1 (Codex, Slivers, the chain) go to the agents' Wednesday order. Wave 2's "scripts for Ch14–21" is Claude's ongoing story track.

## 2026-11-23_anime-ost-situational-bgm: **ADOPT as an audition pool. Reuben locks the picks; nothing is wired until he does**
- This is the creator's call, not mine: the picks are taste. The four v4.4 locks stay untouched, which the proposal already guarantees.
- Script cross-check (Ch14–16 are now scripted):
  - #4 *lit(var)* → `RD-1` "The Ring Sings" (Cragholm 363) fits the script's staging.
  - #5 *Decretum* → `CE-1`, the Cathedral echo. In `story/34_SCRIPT_CH15.md` it plays in the **Living Nave (391)**, not the arena (394). Retag the slot.
  - #20 *Never Coming Back* → Interlude IV, Wenlow's Quiet Ward (Ch16). It must cut to dead silence for the final gunshot SE: the script's cue is "a single gunshot, and nothing else".
  - #42 *You Say Run* is listed for "Ch16 turning the tide". Ch16 has no comeback beat (it ends on the Purge), so keep it for Ch10 and Ch21.
- The audition page `prismfall_anime_ost_audition.html` isn't in the bundle (only PROPOSAL.md arrived). **Gemini: please commit it** (or publish it) so Reuben can audition and export the lock-in report.
- After the lock-in: the audio agent masters the picks with `master_track.py` and adds the new `Mood - *` / `Cutscene - *` slots to `design/AUDIO_SOUNDTRACK_PLAN.md`. This is in TODO_QUOTA §6. Nothing goes into git without the lock-in.

## 2026-11-23_gen6-9-sprites-postgame-legendaries-dorian-meloetta: **ADOPT all three parts. The story rule is applied now; the engine, sprite and balance work is queued**
- **Part B, no main-story legendary captures (Reuben's rule).**
  - **Applied now:** Ch10's Type: Null is *promised*, not given. Calla hands over the NULL CRADLE KEY, S180 now means "promised", and `PG_TYPENULL` delivers it in the postgame. `story/28_SCRIPT_CH10.md`, `design/FLAGS.md` and `design/POKEMON_AVAILABILITY.md` are updated: Kubfu and Regirock move to the postgame, and the rule is written at the top of §4.
  - The Ch14–16 scripts already comply: Groudon, Giratina and Zekrom are `:catch => false` bosses, and Ch14–16's EventMons are all non-legendary.
  - Ch17+ will be written to the rule. It also means **Ogerpon stays a partner**, never party.
  - **Queued (TODO_QUOTA):**
    - the engine safety net (`Prismfall.legendary_catch_allowed?` gate in Bosses and catch);
    - registering `:LOYAL_THREE` and `:PECHARUNT_DEEP` as `:catch => false`;
    - the 3-tier postgame network as Act V / postgame design input. It gets scripted after Ch21, in story order.
- **Part A, sprites and the 4 EBDX bugs:** adopted and queued. The shiny-fallback path fix goes in the EBDX Bridge, not the vendor plugin. The `.PNG` case normalization and the oversized Gen 9 statics are engine-asset work. The importer `tools/install_ebdx_animated_sprites.py` goes to the art pipeline.
- **Part C, Dorian with a Meloetta ace:** adopt Reuben's locked four (Smeargle, Chatot, Hisuian Zorua and Meloetta, plus Spinda and Jigglypuff), with the **field cap** (`:not_moves => [:RELICSONG]` on Grand Stage's Sound row) and the **"Act One Matinee"** trainer-boss stat scale. The pure-PBS fallback is not adopted: it loses the Aria ↔ Pirouette dance. Gym 1 is balance-critical, so this lands only with a gym-1 harness run on quota (TODO_QUOTA §2).

## 2026-11-23 gilded-king-aurelian-gilgamesh-rework and 2026-11-24 aurelius-personality-not-gob — ADOPTED (Claude, 2026-11-25)
- Path B "Aurelius" applied everywhere; on 2026-11-24 Reuben asked for the internal ids too: `GILDED_THEODRIC` → `GILDED_AURELIUS`,
  `THEODRIC` → `AURELIUS` (trainer type, PBS, Festival key, VS id, portrait id, charset, every art file). Gemini: use the new
  names in scene code and art drops.
- Personality-only audit applied in full: the portal line, the Chain-from-the-crystal toss and the "thousand blades" bark are
  gone; §3.1–3.7 and §4.2 are in `story/42_SCRIPT_RUIN_KING.md` and Z-Power `006_ZPower_TrainerBarks.rb` (house punctuation;
  "hollow one" kept in the R6 closing line). `story/12_RUIN_ROUTE.md` team note synced.
- His battle music: on pause (Reuben), until the audio pass settles.


## 2026-11-24_cc0-bgs-v5-field-audio-upgrade — **ADOPT (files in; Reuben's ear still decides)** (Claude audio agent, 2026-11-25)
- **Checked, all nine loops:** Vorbis, 44.1 kHz stereo, exactly 882000 samples (20.000 s), `LOOPSTART=0` / `LOOPLENGTH=882000`,
  integrated loudness −19.4 to −19.7 LUFS (ffmpeg `ebur128`). The wrap is clean on every file: the jump from the last sample
  to the first is 0.001–0.03 full scale, inside the files' own sample-to-sample movement. The v4.3 loops jumped 0.10–0.25 at the
  wrap on six of nine (Wind, Drip, Deepwood, Lava, Harbor, Bleed), an audible click every 16 s. So this is a real fix as well as a
  better sound.
- **Done:** copied over `audio/gemini_cc0/BGS/*.ogg` under the same names (commit 43a6ec2). No manifest or code change;
  `design/MAP_AUDIO.yaml` (60 maps with ambience) and the `:bgs_*` cutscene cues already point at these names.
  `install_audio.py` keeps an existing file, so a project that installed the v4.3 loops needs `--force` once.
- **Notes for Gemini:**
  - `Drip - Nadir`: the first second sits at −29.9 dB RMS and the last at −18.2 dB, so the loop drops ~12 dB at the wrap.
    No click, but the cave bed will seem to duck every 20 s on the Tidelock / Brinecut / Gullcry maps. Even out the tail, or
    crossfade over a quieter stretch.
  - Sample peaks are −1.7 dBFS (Drip) and −1.9 dBFS (Deepwood); the proposal says TP ≤ −2.0 dBTP. Harmless at BGS volumes 35–80.
  - The proposal mentions `cc0_bgs_v5_audition.html`; it is not in the folder, so there is no A/B page for Reuben yet.
- **Not verified here:** the ear audit (no playback in the workspace) and the licences. The source list is all CC0 / public
  domain as written, but I could not open the Wikimedia / OpenGameArt pages from the workspace. The one to double-check before a
  public release is the xeno-canto gull (`XC707075`, in `Saltmere Harbor`): xeno-canto recordings are often CC BY-NC-SA.
  `docs/CREDITS.md` still describes the BGS as synthesized; update it once the licences are confirmed.

## 2026-11-24_art-drop15-npcs-and-ch17-21-wiring — **ADOPT the art wiring (done); the .ogv parts are superseded** (Claude wiring agent, 2026-11-25)
- **§1 charset aliases: adopted, with two changes.** `025_CharsetAliases.rb` now also swaps the stock `NPC nn` stand-ins, with
  the possessive guard ("Wenna's cousin" stays a cousin) and "Pip Ore" only. I re-ran the audit on all 120 built maps: Vesper
  (145), Edda, Wenna, Coll, Hesper, Dex, Maelis, Calla, Hollis, Rowan, Teo, Wick, plus Sallow (186) and Hrothgar (928), with no
  false positives. Added: Gutter, Kassan, Okoro, Renata/Sallow, Hrothgar, Eirik (his sheet has landed), Zara and the ten cameos.
  New: `TYPE_CHARSETS`. An event that battles as a uniformed class wears `trainer_<TYPE>` with no map rebuild, so the war maps
  920–926 pick up the Ashkaar/Isenmar soldier and officer sheets. Hollow and Meridian agents are left out on purpose: 145's
  "Pageant" is a grunt in a gentleman's coat.
- **§2 portraits: adopted.** `:surprised` is an expression; `OKORO`, `SALLOW` (art `RENATA`), `REFLECTION` are cast; `DELPHINE`
  borrows Okoro's files. One correction: the selftest was **not** safe as claimed. Its count check hard-coded 21 bubbles, and
  its "no art" fixture (Kassan) had been failing since Art Drop 15 gave him art. Both fixed in `selftest/suite.ruby_stub`.
- **§3, §4 (movies) and §7.2: not adopted.** Reuben's later directive is no `.ogv`: every cutscene is in-engine choreography,
  so nothing is wired to `Movies/` and `package.sh` does not ship it. The acting sheets stay useful to the cutscene agent.
- **§4 (EBDX animated sprite importer):** left with the art pipeline as already queued; it needs sprite sources that are not in the repo.
- **§5 types: adopted.** `[LARCH]` ("Professor") and `[WENLOW]` exist; Interlude IV now plays as `WENLOW` (it named a
  `PARTNER_WENLOW` type that never existed). During an Interlude the VS screen shows that character's bust.
- **§6 map fixes:** the map agent's; not touched here.
- **§7.1 Drops 15–17:** `SUMP_BARON`, `THORNGUARD`, `GILDER_AUTOMATON` have types and teams; the Reflection has a `VS_IDS` row
  (its PBS name is "???", so the name lookup could never find the bust) and a grey theme.

## Commit 5edcbd9, the 8 faction and war classes — **wired**
- All 8 fronts match existing PBS types. The five class busts (`ASHKAAR_OFFICER`, `ISENMAR_OFFICER`, `MERIDIAN_ADMIN`,
  `MERIDIAN_ASHE`, `OCTAVE_SINGER`) are in `VS_IDS` and `THEMES`, and their single portraits are in `Portrait::CAST`
  (`ASHE` is an alias for the Spin Doctor). Watch one thing: the Octave gauntlet now plays the VS screen before each singer.
  If that drags, set `PrismfallVS::OFF_SWITCH` for the gauntlet.

## 2026-11-24_cameo-venam-original-and-transfer — **ADOPT** (done)
- Checked by hash: `FESTIVAL_VENAM` / `VENAM` are the restored Rejuvenation look, and the punk set is byte-identical under
  `PUNK_ZARA` / `ZARA`. No text anywhere described Venam's old look, so nothing else needed fixing.
- **Zara is in:** type `PUNK_ZARA` ("Riot Punk"), VS id, rose theme, portrait cast, name alias. Her fights come from `gen.py`
  rather than the pasted PBS: `[PUNK_ZARA,Zara]` at Lv 35–37 (one under Venam's 38; the proposal's Overdrive and Boomburst
  aren't learnable at 38) and `[PUNK_ZARA,Zara,1]` at Lv 75–77, each with Hard and Casual versions.
- The cameo art rule and the corrected looks (Alexandra, Lin, Nova) are written into `design/CAMEOS.md`.

## 2026-11-24 cameo waves 1–3 (Shelly, Melia, Alexandra · Amaria, Titania, Garret · Shiv, Lin, Nova) — **ADOPT** (done)
- All three hooks per cameo are in (`VS_IDS` + `THEMES`, `Portrait::CAST`, `NAME_ALIASES`). The snippets named tables that
  don't exist (`TRAINER_TYPE_MAP`, `TRAINER_TO_CAST`, `BUST_THEMES`); the real ones are `VS_IDS` and `THEMES`.
- Types and teams already existed at CAMEOS.md's levels with their signature species; no legendary except Alexandra's Latias,
  which CAMEOS.md names. Nova's type was `Gender = Mixed`; it is Female now.
- **Shelly is live:** her event on 525 was already built and now wears her sheet and shows her portraits. The other eight
  venues are unbuilt maps; `design/CAMEOS.md` has the placement table (map, condition, battle call, flag) for the map builder.

## 2026-11-24_player-movement-charsets — **ADOPT Option B** (done)
- `026_PlayerLooks.rb` serves the run, bike, surf/dive and fishing sheets, each only when its file is installed. No
  `pbs/metadata.txt` fork. Interludes still win (Core 028 wraps the same methods).
- Not seen in the engine yet: the capture harness was in use. Worth one short capture of run, bike and fishing.

## 2026-11-24_gen5-b2w2-tileset-overhaul and commit 23b1125 — **ADOPT the reskin as shipped; the donor-swap blueprint stays a proposal**
- What landed is a recolour: all 43 sheets keep their size and alpha mask exactly (checked pixel for pixel), so no map,
  passability or tile id can break. The 22-donor slot-swap plan in the proposal is not what was pushed and is not adopted here:
  it needs Reuben's sign-off and a licence pass per pack.
- **Install path fixed.** `package.sh` shipped the reskin only by accident of copy order, while `run_intro.sh` copied the mapgen
  sheets last, so real-engine captures showed the old tiles with reskinned stock interiors. Both now call
  `tools/overlay_reskin.py`: the reskin goes on top, a sheet that no longer matches its mapgen source is skipped and listed
  (re-run `mapgen/gen5_reskin.py` after any tileset rebuild), and `PF_NO_GEN5=1` gives the mapgen look.
- The DevKit now overwrites four stock sheets (`Poke Centre interior`, `Mart interior`, `Interior general`, `Gyms interior`);
  `package.sh` says so.
- **Gemini, please check in a capture:** `PF Salt Lake`'s shore went from rose salt to dark violet. Does it still sit right
  against Brinecut's rose-salt floor (545)?

## Art still owed (from `python3 -I tools/check_art_wiring.py`, 2026-11-25)
- **Front strips, 17 classes that already have trainers** (they battle in a stand-in's sprite, Core `032_TrainerArtStandIns.rb`):
  `ASHKAAR_EMBER_RIDER`, `ISENMAR_HIRDMAN`, `ISENMAR_TRENCHER`, `THORNWATCH`, the genderless `ASHKAAR_SOLDIER`, and the twelve
  Grounds Ladder classes `WEAVER`, `HARPOONER`, `STREAMER`, `FOREMAN`, `MOON_BROKER`, `WYRM_RIDER`, `LAMP_RUNNER`, `WELL_KEEPER`,
  `LANTERN_ACOLYTE`, `EMBALMER`, `WARDGUARD`, `CANTOR`.
- **Overworld sheets** `trainer_<TYPE>.png`: `HOLLOW_GRUNT_M/F`, `MERIDIAN_AGENT_M`, `ASHKAAR_SOLDIER_M`, `ISENMAR_SOLDIER_M`
  (the four that would finish the war maps), `REFLECTION`, and the 16 classes above.
- **Back strips for Interlude leads:** `CHAMPION_VALEN_back` (Interlude V) and `LEADER_ROWAN_back` (Interlude II).
- **`EBDX/VS/WENLOW.png`** (his portrait stands in at 1.5x), `SUMP_BARON_back`, and Hrothgar has no battle strip or bust.
- **Rename:** `Characters/pose_THEODRIC.png` should be `pose_AURELIUS.png` (the rest of the King's set was renamed).

## 2026-11-24_rejuv-advanced-animations-engine and 2026-11-24_rejuv-cutscenes-rethink-and-expanded-slate — **ADOPT the engine and all 13 scenes; 1 wired, 3 more play on built maps, 9 wait for their maps** (Claude cutscene agent, 2026-11-25)
- **Installed:** `plugins/Prismfall Cutscenes/017_AdvancedAnimations.rb` = §6's engine and cut plates, §12's two engine patches, and
  the newest version of every scene: Ch2, Ch5 DC, Ch8, Ch10, Ch11 rethink, Ch16, Ruin R7 v2 from §6; **Ch9 v4** from
  `ch9_v4_scene.rb` (not §6's v3); **Ch19 / Ch15 / Ch21** from `wave3_ready_scenes.rb` (not §6's first versions, the ones the
  rethink proposal retires); Ch13 and Ch17 from `ch13_ch17_scenes_final.rb`. §6's first Ch5 and Ch11 scenes are left out.
  Claude's changes are marked `[PF]` in the file.
- **Code review:** no shell-outs, no network, no `eval`. The only file write is the capture screenshot, now refused outside the
  game folder. Nothing existing is patched: the engine lives in `Prismfall::AdvancedAnimations` and only prepends onto its own
  `Engine`. No collision with 006 / 012 / 014 / 016.
- **§5.1–5.2 done.** `016_Movies.rb` is the registry: `pfm_cutscene(:ID)` with the spec's aliases, `Cutscene.act` kept,
  `Cutscene.movie` and every `pf_*.ogv` reference removed. `pfm_cutscene` returns true only if the scene played, and never raises.
- **One real gap in the supplied code, fixed:** the scenes call `$game_map.setup` / `$game_player.moveto` and never put anything
  back (`dispose` only zeroed the tone). That is fine for a recording and wrong in play: after Ch5 the player would be left
  invisible at the camera tile. The engine now snapshots the map, tile, facing, transparency, tone and BGM and restores them in
  `dispose`, and hides followers meanwhile. Checked in the engine for five scenes (`restored=true`).
- **§5.4 done:** `say` waits for USE / BACK in play (a press while it types shows the line; a small arrow marks the wait); capture
  runs and `AdvancedAnimations.auto_advance = true` keep the timed hold. Also: lines page at three rows instead of overflowing,
  names come from `Prismfall::Portrait`, and the protagonist uses the player's own sheet, portrait and name (the scenes
  hard-code `PLAYER_A`, and Ch17 named them "Avery").
- **§5.5 done:** all 29 BGM tags and the two SE tags map to files in `audio/manifest.tsv` (`SCENE_BGM` / `SCENE_SE` in 016).
  The anime-OST titles in the spec are not wired (that pool is still Reuben's to lock). No bronze bell exists yet:
  `ch8_foundry_bell` falls back to `Anim/HealBell`. The King's "Cosmic Air" is **provisional** (→ `Theme - Accord`).
- **Photosensitive:** Gemini's guards (flash, flash_ramp, impact_beat, shake, plate shake) kept; additive VFX are now dimmed and
  actor colour flashes capped as well. The vault flow passes in that mode.
- **§5.6, what plays where.** A scene is `:ready` only when the maps it was staged on are the story's maps:
  - **Wired:** Ch5 on 952 (`pfm_cutscene(:SH1)`; `:SH1_BURN` is a no-op, `:SH1_EXIT` still clears the Mourner). The event falls
    back to the same beat as text if the scene can't play.
  - **Ready, not wired to an event:** `:CH2_PAGEANT` (145), `:WAR_CLIMAX` (926).
  - **Staged on a stand-in, so a logged no-op in play** (`preview: true` plays them): Ch8 (928 for 244), Ch9 (295 for 264),
    Ch10 (525 for 708), Ch11 (563 for 309), Ch13 (287 + 174 for 343), Ch15 (295 for 391), Ch16 (104 + 544 for 223 + 363),
    Ch17 (186 for 826), Ch21 (285 for 491), Ruin R7 (186 for 491). Swapping the id is not enough: every tile coordinate
    belongs to the stand-in. Restage on the real map, then set `:staged` = `:canon` in `SCENES`.
- **Canon, where the scenes and the scripts disagree:**
  - **Ch5.** `story/24` says of the Shatter "no streets shown" and saves Rook's "Turn it off" for 608; the Director's Cut
    cuts to Dex freezing and spends that line mid-vault, before the boss and before Rook works out that the Lowlight is under
    them. `:SH1` therefore plays the cut **without** the Lowlight cutaway (`SH1_LOWLIGHT_CUTAWAY = false`; one constant to flip;
    `:CH5_DC` is the full cut). **Reuben's call.** Four trimmed lines are back to the script's wording.
  - **Ruin R7.** `THEODRIC` sheet and portrait ids → `AURELIUS`; every line of the King's and Voss's is now `story/42`'s
    (2c3c22b), word for word. The staging was already personality-only (gauntlet toss, one Poké Ball, no portals). In the script
    the Kneel / Refuse choice and `:ruin_voss` sit between the audience and the challenge: the scene must be split there when
    it is staged on 491.
  - **Ch8** compresses the bells, the tap and the midnight hall into one piece; in play those are separate beats on 240, 255
    and 244 with the detonator choice between. It will need splitting too.
  - **WAR-1** has one outcome; 926's event plays the existing four-outcome `Cutscene.play(:WAR_CLIMAX)` (by `:war_climax`).
    Gemini's version is registered but does not replace it.
- **For Gemini:** stage new scenes on the story's map; take the cast from ids, not `PLAYER_A` / `THEODRIC`; the `pfw_*` sheets
  live in the plugin's own Graphics folder (the engine now looks there). Still missing: `Pictures/cut_ch2_pageant_tear_90deg`
  (the scene skips the plate) and a bronze bell SE.
- **Verified:** `ruby -c`; the Cutscenes selftest (13 new checks; 228 checks, 0 failed);
  real engine: the vault flow CH5_STEP 8 → 9 → 12 three ways (scene, photosensitive, scene removed), and `:CH2_PAGEANT`,
  `:CH8_CALDERA`, `:WAR_CLIMAX`, `:CH9_UNMASK` played to the end and handed control back. Frames looked at and deleted.

## 2026-11-25 — Expressive conversations, chapter opening cards, playscripts (Claude)

### `2026-11-24_expressive-conversations-system` — **adopted, reworked on install** (`plugins/Prismfall Cutscenes/018_ExpressiveDialogue.rb`)
- **Kept:** the three pillars, the tag names (`\pfe[...]`, `\pfp[...]`, `\pfa[...]`), the emote sheet and its ten rows, the
  six strip pose sheets and their pose names, the listener tone, the 0.10 s fade and cross-fade, the helper names (`pf_emote`,
  `pf_nod`, `pf_step_back`, `pf_lean_in`, `pf_turn_away`, `pf_face_each_other`, `pf_pose`, `pf_stage_clear`).
- **Changed, and why:**
  - *The stage owned sprites between message boxes.* As written, two portraits stayed on screen through walks, waits, battles
    and cutscenes until the event ended. Now a portrait exists only while its message box does; the stage remembers who
    stands where and rebuilds. The listener is kept through an unbroken exchange only (two face lines within 0.35 s).
  - *It bypassed 014.* The spec re-implemented 014's message hook and called the core directly, which also broke
    014's selftest. 018 now replaces `Portrait.open` for face lines (the view is a `FaceBox` subclass), so `014_Portraits.rb`
    is untouched and the audio agent's VoiceTicker hook still sits in the chain.
  - *4x4 sheets.* The 60 later `pose_*.png` are 128x192, a pose a row with four frames; the spec's slicer assumed the
    128x48 strip and would have drawn the whole column. Both layouts work; a row plays once and holds its last frame.
    Shared names for the rows: `crossed` / `point` / `brace` / `shrug`.
  - *Automatic stances only for a speaker standing still and facing the camera* (the art is front-facing); walking off or
    turning ends one.
  - *`AUTO_FACE_SPEAKER` is off by default* (`Prismfall::Expressive.auto_face = true` turns it on). Most lines are said to
    the silent player and map events already stage who faces whom; turning each speaker toward the previous speaker turned
    people away from the player. `[act: face]`, `pf_face_each_other` and `pf_turn_toward` do it on request, and never
    touch a character its event has walked into place.
  - *Who an emote lands on.* `Portrait.speaker` falls back to the event running the text, so a balloon for Juno could
    appear over a sign. A cast member is found by event name (prefix match: "Kestrel K1", "Juno (lab yard)") or as the
    follower; only a plain speaker falls back to the running event.
  - *Three balloons a conversation* is enforced (the creator directive), a fourth is dropped and logged. Balloons are
    cleared when the map screen goes away (a battle), so none hangs over the battle scene.
  - `[emote: kind]`, `[pose: name]`, `[act: name]` are accepted as the story-bible forms of the three tags.
  - Dropped: the voice blips (the audio agent's `014_Portraits_Voice.rb` does that), the "Battle damage normal" SE on a
    wince, the per-idle-frame `clear_all`.
- **Art:** present: `Animations/pf_emote_balloons.png` (128x320), strips for JUNO, KESTREL, LARCH, PLAYER_A, PLAYER_B, VOSS,
  4x4 sheets for 61 more of the cast. **No pose sheet:** REFLECTION, MERIDIAN_ASHE (Ashe) and the four class portraits
  (ASHKAAR_OFFICER, ISENMAR_OFFICER, MERIDIAN_ADMIN, OCTAVE_SINGER); a `\pfp` for them is a logged no-op.
  The 4x4 sheets have no written row map except Venam's; the four shared names above are what the rows look like.
- **Verified:** `ruby -c`; Cutscenes selftest, 36 new checks (no pixel of movement across fade, dim and cross-fade; sides;
  third speaker; gap; cap; acting offsets; nothing left alive after a box).

### `2026-11-24_rejuv-chapter-opening-cards` — **adopted** (`plugins/Prismfall Cutscenes/020_ChapterOpeningCards.rb`)
- **Kept:** the 24 paintings, the manifest (titles, acts, places, accents, camera), the particle emitter, the timeline,
  the skip after 1.5 s, `pbChapterOpeningCard` and the debug previewer (now under the Cutscenes debug menu).
- **Changed:** the map fades to black before the card and back after it (the spec cut straight in and out); the pan is
  clamped and a black sheet sits behind the painting (at the ends of some pans the map showed at the edge); the viewport is
  above message boxes and screen fades; the chime is the installed SE only (`Chapter Card Prismatic Wipe`,
  `Glitch Tear Static` for the Ruin card) — the "BP Fanfare" ME fallback is gone; timing on the game clock.
- **The hook:** `pf_chapter_card(n)` (no argument = the current V102) shows a chapter's card **once a save**
  (`$PokemonGlobal.pf_chapter_cards`); `force: true` repeats it. **Automatic:** when a map event sets V102, the card plays
  there and then; set from anywhere else it waits until the player stands free on the map. V102 0-21 = Prologue and
  Chapters 1-21, 23 = "Fallmorn"; 22 (the epilogue) has none. The Ruin Route does not move V102: its first event should
  call `pf_chapter_card(:RUIN)`. `Prismfall::ChapterCards.auto = false` turns the automatic card off; it is off under the
  capture harness (`DEMO_PLAN`).
- **For Reuben:** the existing "ACT I — THE LAST FERRY" title card (and the END OF ACT / next-act cards) still play; at
  the first chapter of an act the act title is followed by a chapter card that carries the act name too. Say if the act
  cards should go.
- **Verified:** `ruby -c`; selftest, 20 new checks (ids, the V102 map, every painting on disk, length, skip, no leak,
  once-a-save, the automatic paths).

### `2026-11-24_playscript-dialogue-and-expressions` — **presentation layer merged; the rewording was not**
- **What it is:** copies of all 22 story scripts with long lines cut into one- or two-line boxes, `[name: X]` holds in
  place of repeated `[portrait: ...]` tags, emote cues, and — despite "zero rewritten character voices" — **769 spoken
  lines changed** (285 punctuation only, 162 with a bracketed cue or aside dropped or rewritten, 322 with words changed),
  132 stage-direction or system lines reworded, and 38 lines added inside script blocks. It asked for
  `cp act3_5/*.md story/`. That was not done: the copies also predate the Aurelius rename and the 2c3c22b Ruin King rewrite.
- **What was merged** (`tools/playscript_merge.py`; commits c1138b3, fb66ff0, 12d6be2, b232adc, c2e7a45): the box cuts
  (2,187 more boxes), 1,584 holds, 104 `[emote: kind]` cues, 69 whole-sentence stage directions moved to
  their own lines, and Gemini's expression where it differs and the art exists (which also fixes `LARCH, worried` and
  `SAHAR, worried`). The words are the canon's: for every file the fenced text is token-for-token what it was, lines
  outside the blocks are untouched, and trainer references are unchanged (`check_script_trainers.py` gives the same result).
  A hold is written only in a straight run of lines; a choice or branch starts with the face spelled out.
- **Not taken:** every reworded line (kept as written, cut into boxes only where the cut could be placed exactly);
  a face for a line the canon keeps plain (14: Dominar → HROTHGAR, Coll, Calla, and single lines of Juno and Sahar);
  `THEODRIC` tags (26, the canon's AURELIUS tags stay); two new `[bubble: ...]` (Kestrel "Don't.", Larch "You did
  WHAT."); ten emote cues on lines of their own.
- **Examples of the rewording, for Reuben** (full list: `python3 -I tools/playscript_merge.py --check --report /tmp/div.txt`):
  - Ch14 Bastian: "I was carrying the Stone Plate in the procession. Wardens carry their Plates up the nave, you see, and
    then the Choir sings, and the Crown takes them." → "I carried the Stone Plate up the nave." (the Tuning set-up is gone)
  - Ch11 Voss: "...to every crown in the Accord, the Fellowship stands ready to provide logistics, heat and medical
    support..." → "...to every crown, we stand ready to assist."
  - Ch12 Kestrel: "It's the only thing of hers left in the world that isn't a lie somebody else told." → "The only thing
    of hers left that isn't somebody else's lie."
  - Ch2 Gym Guide: three sentences on the field and the type chart rewritten into one each.
  - Throughout: full stops and commas turned into dashes, "(a shrug)" asides rewritten as "(A shrug.)" sentences, the
    older `*(music note)*` / `*(shock lines)*` cues dropped.
- **Portrait check:** every `[portrait: ...]` / `[bubble: ...]` in the 22 scripts has its file (`SALLOW` uses RENATA's
  through 014's `art:` entry); every emote is one of the ten kinds; no block has more than three cues.
- **Docs:** `story/13_CUTSCENES.md` "Portrait use" has the emote cue, the one-box-a-line rule and the motionless stage.

## 2026-11-26 claude-integration-handoff and bgs-drip-nadir-loop-fix (Claude, 2026-11-26)
- **§1 chapter-card ribbon: ADOPTED.** RIBBON_H 110, ribbon raised 7 px, the four text anchors moved as proposed; the same
  anchors were also in `animate_text` (020 L1017–1020), which the proposal didn't list, so those moved too.
- **§1b set_pose: ADOPTED, adjusted.** Rows are detected from the sheet (4×4 when height ≥ 4 × cell width); on a 4×4 sheet
  a pose is a ROW, so `set_pose(n)` shows row n's last frame, the way 018 holds it (not column n).
- **§2c map hooks:** 593's wild table added to `pbs/encounters.txt` (the WORLD.md pool, Lv 21–25, Joltik / Voltorb at
  night). 244 / 249 Ch8 story hooks: in progress as a story layer over `cindervault_town.py` (Claude's Interlude/Map agent).
  MAP_AUDIO already covers all 120 maps with 0 warnings.
- **§3 art: ADOPTED.** The 17 stand-in rows are retired (own art wins anyway). `check_art_wiring.py`: 0 errors, 0 gaps.
  Hrothgar's strip and VS bust stay unwired: no script gives him a battle yet.
- **§4 legacy types: NOT ADOPTED.** `MERIDIAN_AGENT` and `ISENMAR_SOLDIER` are still the charset names in the war cutscenes
  (`013_Scenes_War*.rb`); they stay. The audition HTMLs are noted, thanks.
- **Drip - Nadir loop: ADOPTED.** Measured here: seam 0.1 dB (old file 4.3 dB in a mono mix), same peak. Installed in
  `audio/gemini_cc0/BGS/`. The 545 salt-lake fix answers our question.

### `2026-11-26_claude-integration-handoff` §2c items 1-2 (244 / 249 story hooks) — **adopted** (Claude, 2026-11-26)
- Built as a story layer, `mapgen/layouts/story_ch8.py`, on top of `cindervault_town.py` (tiles and Gemini's events
  untouched; pages added to the Mother, the child and the watchman). 244: My Father (V129 4), Whose Is It
  (`:ch8_lightstone`, V129 6 with S120 -> 7), Chestnuts (-> 8). 249: the Five Bells evacuation (V129 5-6) and the
  ward afterwards by V110. Checked in the real engine on all three choice paths (`tools/harness/visual/ch8/008_Ch8StoryCapture.rb`).
- Not done here: `AS_FORGE_REMEMBERS` (Ch17, the Trials owner's) and the MAP_AUDIO entries for 244 / 249.

## Chapter 6 on Gemini's maps: act2-duneholt-core-maps, act2-duneholt-gym5-ossaria-maps, act2-ossaria-routes-tunnels-maps, cutscenes-wave5a "Ch6" (Claude, 2026-11-27)
- **The maps (200-214, 600/601/604-606/610-613/620/624/625/628): ADOPTED** as Chapter 6's canon maps. The road
  612 -> 600 -> 610 -> 601 -> 613 -> 203 and Duneholt -> 208 -> 620 -> 624 are linked; the guarded exits to unbuilt
  maps (602, 603, 810) now speak a line instead of printing a bracketed box.
- **The story events written into the layouts (203 arrival, 209 Sahar, 213 Sahar, 612 checkpoint, 620 door / K3 /
  courier, 624 Sahar's rubbing, the murals as signs): PARTLY ADOPTED.** Their places and mechanisms stay (the S576
  barrier, the x 55 touch column on 620, the sundial seal); their pages are replaced by `mapgen/layouts/story_ch6.py`
  (a story layer, `set_pages`), because they merged and reworded the script's lines, printed its bracketed narration
  as boxes, and dropped beats (Sahar's calligrapher line, her ace line and the level-35 line, most of K3 and the letter,
  the murals' Sahar commentary). Re-run the layer after re-running these layouts.
- **Found and fixed in the layer:** 612 had no way in from Lumen (the script's "Mainline out of the Concourse"):
  warps 180 (0, 32-37) <-> 612 (54-60, 63). The checkpoint could be walked round through 612's open south fields, and
  set CH6_STEP 2 from step 0: it now plays as you join the queue (CH6_STEP 1 -> 2). 213's Sahar could be fought before
  the drill site, skipping `:ch6_drillsite`: the Dig's door on 200 opens at CH6_STEP 4. 207's open Mural Gallery
  showed the Ossuary's murals before the Ossuary: 206's door stays shut through Chapter 6, as the script writes it.
- **Gym 5 puzzle: ADOPTED, proved.** `mapgen/puzzles/dig.py` proves it on the built 210-212: 46 states, 5 moves (the
  entrance drop, lane c, M2 twice, lane b), no soft-locks, unsolvable without the falls or M2. V326 runs d / wall / c
  where GYM_PUZZLES says c / d / wall from 1: same cycle, same solution (GYM_PUZZLES can be updated to Gemini's order).
- **Left for Gemini / owners:** the raw ids S552-S555, S576-S581, V551 are not in `mapgen/flags.yaml` (register them);
  `[612]` / `[613]` encounter tables (encounters owner); art and staging notes in `mapgen/REFINE_QUEUE.md` (Ch6 note).
- **wave5a `:CH6_BRIAR_COURT`: NOT a Chapter 6 scene.** It is the Ch10 Verdance succession (`story/28_SCRIPT_CH10.md`,
  285-287); wave5a has nothing for Chapter 6 and nothing of it is installed for Ch6. Rename it `:CH10_*` if it is
  adopted for Ch10 (the Ch10 owner's call); no Ch6 beat plays twice (the 016 registry has no Ch6 scene).

## 2026-11-26_act2-cindervault-gym7-pyre-keep-maps (Claude, Gym 7 agent, 2026-11-27)
- **Gym 7, Cindervault Gym 250–253: ADOPTED as the canonical maps** (ours, `foundry_gym.py`, is superseded and refuses to
  run). The puzzle is GYM_PUZZLES Gym 7 as designed: same ids, aims, one shared quench (V338 0 ready / 1 dry, as
  `flags.yaml` already named it), drains, moulds and vault; trenches 5 wide, maps 29×27. Good additions: 252's ladders
  C1 / C2 back up beside the chute landings (fewer resets needed), Hessa's status / reset / hints / puzzleskip, the
  Mould-Runner. Proved by `puzzles/foundry.py` (rewritten as grids of your built floors) on the design and the built
  Map250–252: 250 in 2 moves; Pour + Mould Floor in 7 (pour K1, pour K2, quench X2, aim K3, pour K3, chute C1, chute C2),
  456 states, no soft-lock, unsolvable without C2 or a quench; vault in 3; both traps real. Your "418-state" count
  differs only in how states are counted.
- **What 253 lacked, now in `story_ch8.py` (story layer, your layout untouched):** the script's Brann scene. Your page
  had no portraits, played the seven notes as one bell plus a narrator box, replaced the four quench lines with an
  invented Flamethrower line, and had no Eighteen Roads quest line and no cut out into the square (the Five Bells
  waited until the player walked back out through 250; the script goes straight from the badge to the square at dusk). His fight is LOCKED: the battle call is yours, unchanged
  (`double: false` is a no-op for Brann; GYMS has no :double for him).
- **240's Foundry doors** still warped to our old 250 (10, 15); they now land on your arrival (12, 22).
- **Real engine:** `ch8/008_Ch8StoryCapture.rb` walks your gym (lever, wheel, the vault and the Mould-Runner's reset,
  then the 7-move route; Flint, Garran, Ivar and Brann fought) inside a full Ch8 run, CH8_STEP 3 -> 4 (243) -> 5 (253)
  -> 6 (240) -> 7 -> 8 (244) -> 9 (240) -> 10 (243), STORY_CHAPTER 9, no step set by hand. Frames looked at: the trench
  states read clearly (dark trough, magma, grate).
- Nits, no action needed: a crucible ends its menu after an aim (talk again to pour); Hessa's spoken solution is the
  8-move one. For later runs of your layout: run `layouts/story_ch8.py` after `cindervault_gym.py` (REFINE_QUEUE note).
- **Pyre Keep 245–248, 254: ADOPTED (wiring checked only; the map audit agent has the full pass).** Every warp lands on a
  walkable tile, 240's Rampart / Roosts doors open onto your arrivals (16, 22) / (12, 20), `CHANNELER,Thessaly` and the
  Gym 7 trainers exist in `pbs/trainers.txt`, and the Trials keys you call (`pf_trial_board(:ASHKAAR)`,
  `pf_trial_talk(:ROOST_KEEPER / :OLD_CINDER)`) are registered.

## Gemini's overnight 15 commits (5f233ad2..d543a354): integration audit (Claude, 2026-11-27)
Proposals not owned by a chapter agent. Tool: `python3 -I tools/check_map_events.py --range 5f233ad2..d543a354`
(trainers with every version, methods, items / species / moves, flag names and id collisions, registries, charsets,
transfers, ruby syntax): **86 specs, 1704 events, 995 script blocks: 0 errors**; the 73 warnings were unregistered
puzzle ids, now registered in `mapgen/flags.yaml` (G5_ / G6_ / G8_ / G9_ / D11_ / 576-581; the G7 ids are the Gym 7
agent's). Strict build of HEAD in a private copy: 217 maps, every committed `Map*.rxdata` reproduces byte for byte.
Our story layers re-run on the changed maps (interlude1, ch5's 608 sync, ch8 on 240 / 243 / 244 / 249, circuit_gym 193,
cindervault 255) change nothing; real engine: the Ch5 vault (CH5_STEP 8 → 9 → 12) and Interlude I (→ 13, Act 2)
still play.

### `2026-11-26_act1-frontier-complete-maps` (565, 580-595) — **ADOPTED as built; one P0 seam queued**
- Checker clean; exits to unbuilt maps are all behind `pbRgssExists?`. The Lock Road's script events are on your maps
  (Teo on the channel, the Ice-bound Satchel, the Ice Elevator, Lattice No. 4, the Crownwall view, Ebb Hollow's Field
  Notes) and 591's Gale Post clerk reads Juno's letter with story/24's V125 0 → 1. None of our layers stages these, so
  nothing plays twice.
- **P0, queued (REFINE_QUEUE):** nothing on 160 Ebbmouth leads into 580 (580 warps back to 160 (58, 36); 160's x = 59
  is solid), so the Lock Road can't be reached.
- Ours to do (not a fault of the maps): 594 Wallshadow Row has no "Juno rejoins at the Four Ways" (V125 1 → 2), so
  582's gate scene has Juno talking without having rejoined.

### c7be821c, the 109 / 108 overhaul — **ADOPTED**
Tiles only (`data/raw/108.npy`, `109.npy`); the specs keep story_early's events. In a private copy
`dovetail.py` → `wave14_setpieces_craft.py 109 110` reproduces both specs and both npy byte for byte. Real engine
(`tools/harness/visual/intro/012_Ch0FerryCapture.rb`, plan `ferry`): the Prologue autorun, the rail twice (Edda, then
Voss: PRO_FERRY_DONE), the gangway to 100 (34, 55) and the customs line there all play on the new deck.

### 505ab82c (193 G4_SPLICE, 525 / 541 win guards, 255 Pass 3) and f6c3dfae (tr_teal stamp column) — **ADOPTED**
193's S325 → S422 matches flags.yaml's G4_SPLICE, and `circuit_gym.py` (with your `puzzles/circuit.py`) regenerates 193
byte for byte. The win guards are right, but `WildBattle.start` is also true on a run: 541's crab ring and 525's
Masquerain can be won by running (queued: `cannotRun`). The stamp fix changes no committed map.

### `2026-11-26_claude-art-handoff-response` — **ADOPTED (all four)**
Venam's irises (384 px over the 16 frames), `PARTNER_GIRATINA` (check_art_wiring's last error gone), the seated
surf-fish sheets (now wired: Core 026 `:surf_fish` = `PLAYER_*_surffish_offset`, falling back to the fishing sheet),
the centred `speech hgss 1` (same 96 × 48 as stock; one real-engine frame of the Deckhand's message box: symmetric
border, no grey band). Real engine: both looks resolve `surf_fish` to the new sheets. check_art_wiring: 0 errors,
0 gaps (HROTHGAR's 2 files stay unwired, as noted 11-26).

### `2026-11-26_rejuv-cutscenes-wave4b-act1-climax` and `-wave5a-verdance-frostwick` — **per beat; nothing installed**
Neither proposal touches a map: the scenes are drop-in Ruby, unregistered and unwired, so nothing plays twice today.
Every VFX / CG name the code uses is a real file (`graphics/Pictures` = `art/out/Graphics/Pictures`, all seven synced;
the retired `vfx_customs_null_scan` is referenced nowhere). One version per beat:
- **`:CH0_LAST_FERRY` (109 → 108 → 100): ours stays.** The deck, the customs scan and the quay are played by
  story_early's events with the script's words and the player's own choices (style, name, difficulty, Voss's
  fellowship, Edda's questions). The scene is a 57-second summary with paraphrased lines that hides those events.
  Installing it beside them would play the prologue twice.
- **`:CH4_EBB_STOPPED` (160 → 167) and `:CH7_FROSTWICK_HEARTH` (570 → 573 → 579; story Ch4): neither plays.** Chapter 4
  has no story layer yet (V124 CH4_STEP is never set; 573's bard is not on the map). When it is built, your staging is
  the better base, with story/23's lines (yours merge and add some: "You'll fall in like your father") and split where
  the script splits (the strike vote is CH4_STEP 3, the Night the Ebb Stopped is 4).
- **`:CH5_LOWLIGHT_VALEN` (181 → 608): ours stays for now.** 608 plays the canon beats as the script stages them: the walk
  among the twelve glass residents, Rook / Voss / Valen at the Veil, the testimony. The scene opens on a 181 cutaway
  with a line the script doesn't have ("no streets shown"), paraphrases Juno, and would replay Rook's, Voss's and
  Valen's lines that 608's events already say. Its autorun staging (Juno at the Veil, Voss's crate, the glove CG) is
  better than ours: adopting it is a rework on 608 alone (drop the 181 act, story/24's words, retire the duplicated
  talk pages), queued for the cutscene pass.
- **`:CH5_ZENITH_COUNCIL` (194 → 197): not adopted.** story/24 has no Council Chamber scene.
- **`:CH6_BRIAR_COURT` (285 → 287; story Ch10):** the Ch9-10 agent's call.

### `2026-11-26_act3-rimeholt-whalebone-maps` (300-308) — **ADOPTED as built**
Checker clean; the maps only read S128 / V122 / V132; exits to 309 / 310 / 314 / 318 / 712 / 720 are guarded.

### `2026-11-26_act2-cindervault-gym7-pyre-keep-maps`, Pyre Keep 245-248 and 254 — **ADOPTED (full pass)**
Completing the Gym 7 agent's wiring check above: checker clean on all five (trainers, Trials keys, charsets, exits);
247 reads S120 only.
