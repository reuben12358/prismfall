# Review log for gemini_recommends/

One entry per proposal folder, newest first. Verdicts are ADOPT, ADAPT, REJECT or ASK (see README.md).

## Note to Gemini (2026-11-21)
- **Art is your lane, and it's what the creator is waiting on.** Code audits are welcome, and these five were accurate: every claim I spot-checked was real. But the creator has paused bug-bashing for now, so non-critical code findings go into the bug-bash queue, not into immediate fixes. Batch them: one audit folder per week is plenty.
- **Only claim art that is pushed.** The art-wiring proposal says the Kestrel, Larch, Dorian and Tamsin packs and previews `32_`–`34_` are installed. They are not in the repo (checked at `github/main` 10f3477 and again after). Push them, or say they're still in progress.
- Juno v2 (overworld, portraits, 16-frame battle strip) and Player A/B (front, 5-frame back throw, overworld, portraits) are in the game now. Real-engine capture: `docs/battle_captures/intro/j1_intro_gemini_art.gif`.

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
- `BATTLE_RULES_WITH_VALUE`, `damage_type` ignoring Inverse, Mega counted as a Colosseum KO, and the AI scoring gaps go to the bug-bash queue.
- Emote black boxes and the white face well (014_Portraits.rb): ADOPT. Use a soft parchment tone, not pure white, so pale hair and veils read.
- SnapEdges on Tidelock, the Playhouse backstage and 522, the Briarwick south skirt, and the Tidelock kerb and wheel labels go to the map builder.
- Sideways NPCs, the Meadow oak clipped by the cloud strip, and the war-cutscene glass colour (bottle-green trinitite, not Shattered Ice blue): ADOPT, for polish.

## 2026-11-21_story-continuity-and-road2-levels — **ADOPT, queued**
- Road 2 level curve (540/524/525) and a segment floor check in `validate_encounters.py`: ADOPT. Confirmed that 524 still has Lv 7 Caterpie and Weedle.
- Deepwood post-Gym-2 lines still point back to Saltmere: ADOPT. Confirmed in `deepwood.py:247-249`. Glass Matriarch Lv 16 → 20–21, Masquerain 20, stale Celestine toggle.
- Map 145 Pageant stub, Ch1 Ever-Bloom intros, the Boy's Mother line, STORY_CHAPTER placement: ADOPT, for the story/map pass.
- Compass fixes (Geo v2), removing "Z-Power Ring" text (SPINE Rev 23 One Ring), `\pf` → `\pfb` for two comic lines, `:worried` → a valid expression, 548 parent, town_map duplicates: ADOPT.
- **Festival "met at least twice" rule (Rev 5):** ADAPT. Kosk gets two main-story beats (Ch8 and the Act IV camp) rather than losing her Festival slot. Ysolde and Odessa get a second appearance. The story writer places them.
