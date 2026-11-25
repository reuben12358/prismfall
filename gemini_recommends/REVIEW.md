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
