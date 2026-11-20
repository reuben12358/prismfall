# EEVEE_OCTAVE — the Eevee quest (SPINE Revision 19)

> User: "because we have 7 kingdoms, there should be an eevee trainer dedicated to each kingdom. fire one gets flareon,
> water one gets vaporeon, the piltover place gets jolteon, the place with dark types gets umbreon. figure out where the
> rest go and then eventually in crownfall (or any other place of ur choice) you encounter the last trainer. upon
> completion of the quest of all the trainers, a trainer spawns in crownfall that says that all the eeveelution trainers
> wanted to thank you for helping them throughout your journey and wanted to test your mettle to see if you are worthy of
> carrying the power of eevee, they then challenge you in a gauntlet battle where each trainer uses an eeveelution
> starting from the first one you helped and going all the way to the last one in order. All the eeveelution trainers
> have a z move they will use during battle [...] Once u beat all the eeveelution trainers, you will then fight this
> trainer who uses eevee with the z move: extreme-evoboost to finish the gauntlet. Once u beat him, he will give you an
> eevee alongside the eevee z crystal."

This reshapes the Eevee Octave of the Prism Choir (story/03_CAST.md, 04_ACT_I.md, 08_ACT_V.md). The Octave was a
Festival-week exhibition (eight singers back to back, then Vesper's full Eeveelution team); it is now a quest line across
the whole game that ends in that gauntlet. **Vesper Lindqvist** is the host who "spawns" in Crownhaven.

Code: `plugins/Prismfall Trials/012_Trials_Octave.rb` (help order, gauntlet, conditions, debug menu),
`113_Quests_Octave.rb` (the ten quests' data and dialogue), `151_Talk_Octave.rb` (map-event rows),
`plugins/Prismfall Z-Power/` (Z-moves). Map events: `design/TRIAL_EVENTS.yaml`. Full dialogue: `design/TRIALS_QUESTS.md`
(generated). Teams: `pbs/trainers_trials.txt` (provisional). Test: `tools/harness/run_trials.rb` sections 7–8, and the
real engine: `tools/harness/playtest/run_zpower.sh`.

## 1. The eight singers

Glassfall orphans the Choir raised; when they were grown it sent each to live beside one kingdom's Plate, and each Eevee
became what it lived beside. They meet once a year to sing at the Saltmere Pageant. Each has a quest on **their kingdom's
Trial board** (points and rank in that Trial), ending in a duel. Placement follows the gym order (first kingdom visit).

| # (gym order) | Singer · partner | Kingdom · Trial | Who they are | Their quest | Ch · map | Gauntlet field · crystal |
|---|---|---|---|---|---|---|
| 1 | **Lyra** · Leafeon "Moss" | Elowen · the Quiet Way | Soft-spoken gardener, hums without noticing, apologises to plants; stubborn about her patience | *The Moss Hymn*: Moss won't come down from the moss-stone in Gossamer Wood. Singing at it fails; sitting in silence lets it listen, and it steps down a Leafeon (Mother Aldreth's koan) | 3 · 120, 524 | Flower Garden (stage 3) · Grassium Z |
| 2 | **Aria** · Vaporeon "Brine" | Isenmar · the Tally | Loud, sunny, swims in ice water at dawn, sings shanties wrong on purpose | *The Drowned Note*: Brine melted into the Ebb when the river stuttered. Listen for its note at three places, find it under the Mill Quay wheel; Bersi carves the saga | 4 · 160, 167 | Water Surface · Waterium Z |
| 3 | **Cadence** · Jolteon "Snare" | Zenith · the Prize Exchange | Fast-talking drummer, counts in fours, works Meridian night shifts; cynical, secretly sentimental | *Off the Beat*: a Call for Proposals to fine "the source" of Lowlight blackouts: her. Shift three Lattice junctions off her beat; file the report as "unknown" or as a Lattice fault (Meridian +1) | 5 · 181 | Neon Grid · Electrium Z |
| 4 | **Sona** · Espeon "Noon" | Ossaria · the Rolls of Unearthing | Calm and dry; answers before you ask ("I heard that coming"); keeps the noon bell of a buried sun temple | *The Noon Bell*: dig the sand out of the temple's light-shaft so the noon light reaches Noon's dull jewel again (by day only) | 6 · **215 (new)** | Mindscape · Psychium Z |
| 5 | **Noct** · Umbreon "Wick" | Nadir · the Gutter Book | Lamplighter of the marsh ferries; few words, tired, wry; protects the lamp-runner children | *Lamps Out*: Ottoline's chalk job — who puts out the ferry lamps? Wick, hiding the kids from Sweetrot runners. Tell the truth or cover for him | 7 · 220 (night) | New Moon · Darkinium Z |
| 6 | **Forte** · Flareon "Bellows" | Ashkaar · the Trial by Flames | Loud, blunt, brave; wants the Legion to stop seeing "a poor Choir orphan" | *Too Loud for the Choir*: stand as her second before Legate Varra Kosk; she must tell the truth (Ashkaar law), then fight you: win, or lose well | 8 · 240 | Volcanic · Firium Z |
| 7 | **Lento** · Glaceon "Hush" | Antumbra · the Rite of Reflection | Slow, says everything twice ("once for her"); patient, eerie, kind | *The Still Water*: Hush froze the Mirror Mere so her reflection couldn't wander. Walk the three cracks backwards (the Rite) and let it go | 13 · 742 (Rite read at 753) | Frozen Lake · Icium Z |
| 8 | **Carol** · Sylveon "Ribbon" | Crownhaven · the Hall of Petitions | The storyteller; never leaves Crownhaven ("someone has to sing to the ones who didn't get out"); thinks she's the one without an Imprint | *The Ninth Verse*: she is writing the Octave's Festival song and needs the stories: you tell the seven verses **in the order you helped them**; the bond was her Imprint. Then the fight "in the middle of the story" | 20 · 489 | Fairy Tale · Fairium Z |

**Carol is always last.** She is first met in Crownhaven (Festival week, S155); her quest only opens once the other seven
are helped (before that she lists who she hasn't heard from, and where). No quest expires: a singer missed on the road can
be helped on a later visit, so the order of the first seven is the player's own.

## 2. Vesper Lindqvist, the thread

- **Ch2, Saltmere backstage (map 145):** the existing optional duet (Vesper v0 + now **Lyra v0**, not Carol, who never
  leaves Crownhaven). Afterwards Vesper asks the PC to look in on the singers ("they're very good at singing and very bad at
  being alone") and names where each one lives. This starts **"The Eevee Octave"** (`CR_OCTAVE`, step `:road`). Skipping
  her is fine: helping any singer starts it.
- **Ch13, Lucent cloister:** after her sparring double, a few lines on how the letters about you are going, and a nudge
  toward Lento if she hasn't been found.
- **Ch20, the Glassfall Memorial Garden (489):** once all eight are helped, Vesper appears there (the "trainer spawns in
  Crownhaven"), the seven others in a half-circle behind her: they want to thank you, and the Choir's custom is that
  whoever carries the power of Eevee proves they can.

## 3. The help order and the gauntlet

- `{ :octave_help => :ID }` in each singer's winning duel branch appends them to `Prismfall.state.trials[:octave]`
  (once). That list **is** the gauntlet order. Conditions: `octave_helped`, `octave_has(:ID)`, `octave_pos(:ID)`,
  `octave_ready`.
- **The gauntlet** (`{ :octave_gauntlet => true }`): nine trainer battles back to back, **no healing between them** (the
  party's HP and PP carry over, as in Reborn's and Rejuvenation's chained battles; bag items in battle are allowed):
  the eight singers in the order helped (`OCTAVE_SINGER <name> v60`, Lv 87), each with **one Eeveelution holding its type's
  Z-crystal and an attacking move of that type**, each on the field its Eeveelution was raised beside; then **Vesper's
  Eevee "Amen"** (`OCTAVE_VESPER Vesper v60`, Lv 89) with the **Eevium Z** (Last Resort → Extreme Evoboost) on the **Grand
  Stage**, where the Octave was first met. A Z-move lifts the Grand Stage's applause a stage (section 5.4).
- A loss ends the run; the party is healed (quest losses never black out) and Vesper waits to be asked again.
- **Available:** from the moment Carol is helped (Festival week, after S155) and after, including the post-game.
- **Reward:** an **Eevee** (Lv 70, Adaptability; knows Last Resort, Stored Power, Shadow Ball, Quick Attack; can still
  become any Eeveelution), the **Eevium Z**, and Vesper's **Z-Power Ring** (key item) so the player can use it. If
  Understudy is still an Eevee, Vesper points out the crystal works for it too. S177 `EEVEE_OCTAVE_DONE` is set.
  The Eighteen Shrines' "Prism" Eevee (`CR_PRISM_EEVEE`) is gone: one Eevee gift in Crownhaven, not two; that quest
  now gives the five Imprint stones.

## 4. Levels (the trainer designer owns them; as in `pbs/trainers.txt` after round 3, 2026-11-20)

| Fight | Version (Std; Hard = +100, Casual = +200) | Level (Std / Hard / Casual) | Notes |
|---|---|---|---|
| Ch2 duet, Saltmere backstage (145) | `OCTAVE_VESPER Vesper 0` + **`OCTAVE_SINGER Lyra 0`** | Amen 18; Lyra's Moss 17 (still an Eevee: it becomes a Leafeon in Ch3) | double on the Grand Stage. **Lyra v0 is Vesper's partner** (it replaces the retired Carol v0: Carol never leaves Crownhaven) |
| Ch13 cloister sparring, Lucent | `OCTAVE_VESPER Vesper 1` | 56–58 | optional double on the Mindscape |
| Kingdom duels | `OCTAVE_SINGER <name> 50` | Lyra 17/18, Aria 21/22, Cadence 25/26, Sona 29/30, Noct 33/34, Forte 37/38, Lento 57/58, Carol 87/88 | a local partner + the Eeveelution at the next Warden's cap − 1 |
| Gauntlet bouts 1–8 | `OCTAVE_SINGER <name> 60` | **87** / 88 / 83 | one Eeveelution with its type's Z-crystal and an attacking move of that type, on its home field |
| Gauntlet finale | `OCTAVE_VESPER Vesper 60` | **Eevee "Amen" 89** / 90 / 85 | Eevium Z; Last Resort / Stored Power / Shadow Ball / Quick Attack, on the Grand Stage |

**Retired** (no longer in `pbs/trainers.txt`; don't reintroduce them): **Carol v0** (the old Ch2 duet partner), the
**singers' v1–8** (the old Festival-week exhibition sets, which the v60 gauntlet sets replace) and **Vesper v2** (the old
exhibition's full Eeveelution team). Vesper v0 and v1 stay.

The Festival-week cap is 90 (Core `FESTIVAL_CAP`), so the gauntlet sits just under it. **Harness finding (at the old
90/92 levels, before the round-3 retune to 87/89):** an AI-played Lv 100 team of six (Snorlax, Garchomp, Metagross,
Tyranitar, Volcarona, Togekiss, EV-trained) won the nine bouts with **146 of 2,334 HP left**; six Lv 100 Snorlax lost at
bout 4. A Z-move on its home field is a near one-shot: Moss's Bloom Doom (Flower Garden stage 3) took 73% of a Lv 100
Snorlax; Forte's Inferno Overdrive on Volcanic, with Flash Fire lit by the field, one-shot a Lv 95 Vaporeon **through the
resist** in the real engine (round 3 gave Flareon Guts instead of Flash Fire; TRAINER_FIELD_PLAYBOOK). In the real engine
(AI on both sides) the same Lv 100 team lost at bout 6, and six EV-trained Lv 100 legendaries (Arceus, Mewtwo, Kyogre,
Groudon, Rayquaza, Lugia) won with four of them fainted. Re-check with `run_winrates.rb` at 87/89.

## 5. Z-Power (`plugins/Prismfall Z-Power`)

### 5.1 Why our own plugin
The known v21.1 Z-move implementation is Lucidious89's **Z-Power add-on for the Deluxe Battle Kit**; it requires the
Deluxe Battle Kit, a battle framework with its own UI layer, which this game does not use (the battle UI is Elite Battle
DX Renovation). Running both battle UIs, or porting DBK's UI hooks onto EBDX, was a larger and riskier change than the
quest needs, and downloaded plugin code is not run in this workspace. So Z-Power is a small native plugin (four files,
~400 lines with comments) that hooks only `Battle#pbRegisterMove`, `Battle::AI#pbGetMoveScores`, `Battle::Battler#pbUseMove` and
`#unlosableItem?` (all alias-chained), plus two move classes.

### 5.2 Rules
- **Type crystals** (Waterium, Electrium, Firium, Icium, Grassium, Psychium, Darkinium, Fairium Z): a damaging move of
  the crystal's type becomes that type's Z-move (Hydro Vortex, Gigavolt Havoc, Inferno Overdrive, Subzero Slammer, Bloom
  Doom, Shattered Psyche, Black Hole Eclipse, Twinkle Tackle). Power from the base move by the Gen 7 table (≤55 → 100 …
  80 → 160, 90 → 175, 120 → 190, ≥140 → 200); physical/special and contact from the base move; never misses; goes
  through Protect, King's Shield, Spiky Shield, Baneful Bunker, Obstruct, Silk Trap, Burning Bulwark and Mat Block for
  1/4 damage. Status moves don't become Z-moves (no Z-status effects; out of scope).
- **Eevium Z**: Eevee's Last Resort becomes **Extreme Evoboost** (+2 Attack, Defense, Sp. Atk, Sp. Def, Speed), usable
  from turn 1 (Last Resort's own condition doesn't apply).
- **The shipped base's Generation 9 Pack runs with `Settings::CHAMPIONS_MECHANICS = true`**, which locks Last Resort until
  the user's other moves have been used. A base move that is about to become a *status* Z-move may still be chosen (only
  that rule is skipped: the plugin calls the chain below it, `paldea_pbCanChooseMove?`); if the player then answers No,
  the choice is undone with the pack's own "This move can't be used!". Found in the real engine, where Amen first never
  chose Extreme Evoboost; the headless harness's older Gen 9 Pack lacks the rule, so the test emulates it.
- Once per trainer per battle; the Z-Power is spent when the Z-move is actually unleashed (a flinch, sleep or
  disobedience keeps it). The base move pays 1 PP. Encore, Disable, Choice lock, Copycat and Last Resort see the base move.
- Crystals are held, never used up, and can't be knocked off, stolen, swapped or flung.
- The **player** needs the **Z-Power Ring**; NPC trainers only need the crystal. Wild Pokémon never use Z-Power.

### 5.3 Choosing one
- **Player:** choosing an eligible move in the Fight menu opens a Yes/No box: *"Unleash Vaporeon's Z-Power? (Scald becomes
  Hydro Vortex)"*. It works on Elite Battle DX's own command box (real-engine screenshot:
  `run_zpower.sh zpower`, `zpower_out/zpower/shots/004_zp_prompt_unleash_z_power.png`). A button on the Fight menu like
  EBDX's Mega button would be nicer; it needs EBDX UI work (noted for the EBDX Bridge owner).
- **AI:** eligible moves score ×1.6 when they already score at least the base score; Last Resort scores 260 for an
  Eevee with the Eevium Z while it is above half HP and has gained fewer than six stages. Any eligible move the AI then
  picks becomes the Z-move. So it doesn't waste a Z-move on an immune target (Jolteon into Garchomp, Espeon into
  Tyranitar held theirs back in the test run).

### 5.4 Fields
1. A Z-move **is its type**: every type rule applies (Water Surface's Water ×1.5 powers Hydro Vortex; Volcanic halves
   Subzero Slammer; Bloom Doom grows a Flower Garden like any Grass attack; transform strikes ×1.3).
2. Rules naming a **base move** don't follow it into the Z-move (Dive's ×1.3 and Underwater plunge, Lava Plume's
   eruptions, Fairy Tale's Draining Kiss). A field can name a Z-move in `:moves`, or match all of them with
   `:flags => ["ZMove"]`.
3. **Showpiece:** on the Grand Stage a Z-move raises the applause one stage after it resolves (`004_ZPower_Fields.rb`).

## 6. Tests

- Headless (`ruby tools/harness/run_trials.rb`, report `docs/trials_test/REPORT.md`): section 7 (Z data; power table;
  AI with/without the ring; once per battle; base PP; Protect at 1/4; the player's Fight-menu box, Yes and No; wild
  Pokémon; crystals unlosable; field rules 1–2; every gauntlet singer's Z-move against a neutral target) and section 8
  (all ten quests driven through their map-event rows, out of gym order; Carol locked, then "not yet", then last; the
  verses told in help order; a lost and a won 9-bout gauntlet with order, fields, Z-moves and carried-over HP checked;
  the reward; the reward Eevee's Extreme Evoboost on the Grand Stage).
  Plus the Champions rule (Amen still opens with Extreme Evoboost; the player's locked Last Resort -> Yes -> Extreme
  Evoboost; No -> undone). **142/142.**
- Real engine (`tools/harness/playtest/run_zpower.sh`, mkxp-z + EBDX, own game copy and display, the bot only presses
  buttons): `zpower`: the player's Fight menu -> Scald -> the "Unleash ... Z-Power?" box on EBDX -> Yes -> Hydro Vortex
  (won vs Lento). `zgauntlet`: Vesper's event script with the help order Noct > Lyra > Sona > Aria > Lento > Cadence >
  Forte > Carol: every bout on its field, HP carried over, Black Hole Eclipse, Bloom Doom, Shattered Psyche, Hydro Vortex,
  Gigavolt Havoc, Twinkle Tackle unleashed (Glaceon and Flareon chose theirs and fainted first); with
  `PLAYBOT_ZP_TEAM=legends` all nine won and the reward arrived (Eevee Lv 70 with Last Resort, nickname prompt, the Eevium
  Z, the ring, S177). `zevo` (Champions rule live): the player's Eevee and Amen both open with Extreme Evoboost.
  Screenshots: `$RUN/zpower_out/<session>/shots/`.
