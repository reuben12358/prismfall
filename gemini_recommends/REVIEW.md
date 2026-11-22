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
