# Script: Chapter 19 — "The Last Gate" (the Truce Road; Wyrmrest's gate; Sigrun's trial and the oath; the Battle of the Glass Dunes; the Dominar; Reshiram; Gym 18; the Rainbow Scar; the road to Crownhaven)

> **Final playable script** for Chapter 19.
> - **Maps:** the Truce Road (860 the Gloamwood, 861 the Thornwar Marches with Thornwatch 870, 872 the Wyrmspine), Wyrmrest (460–475, with Gym 18 at 470–475), and the Wyrmscar Rift (864/865). The war theatre is **built**: 920 the Rimed Sands, 924 the Siege Camp, 925 the Steamline, 926 the Glass Dunes, 928 the Command Pavilion, 929 the Observers' Mesa, 930 the bone-carters' camp. Then the Rainbow Scar (868) and the Pilgrim Road (892 Dominar's Toll, 880 the Pilgrim Pass, 890 Pilgrim's Rest, 893 the Coronation Road, then 884–886 the Sovereign's Ascent or 888 the Glassfall Scar) to Crownhaven's gate.
> - **Order:** follows `story/37_SCRIPT_CH18.md`. Chapter 20 ("The Festival of Champions") follows.
> - **Sources:**
>   - Story: 08_ACT_V Ch19; **14_WAR_AND_BLESSING Part B** (the Battle of the Glass Dunes: staging, choices, outcomes; it wins on conflicts); 03_CAST (Sigrun, Hrothgar, Anja, Marisol, Kassan, Larch, Edda); 13_CUTSCENES WAR-1; 15_COMEDY Ch19 "Weighed".
>   - Keys and rules: NARRATIVE_KEYS (`:ch19_oath`, `:ch19_dominar`, `:war_climax`, `:war_terms`, `WAR_TRUST`, the outcomes, `DOMINAR_SWAYED`, `GO_LIARS_PYRE`); POKEMON_AVAILABILITY §4.
>   - Design: GYM_PUZZLES Gym 18; WALKTHROUGH Ch19; `design/CHAPTER_BEATS.md`; `design/DENSITY_STANDARD.md`.
>   - Bosses: `:RESHIRAM_GLASS_DUNES` / `:KYOGRE_GLASS_DUNES` (106) and the new `:RESHIRAM_WYRMREST` (110).

## Conventions
As in the earlier scripts.
- **Portrait cast:** Sigrun, Anja (if `:war_prisoner != :leave`), Marisol, Larch (radio), Edda, Kassan, and the PC (the oath is an authored line).
- **Plain:** Dominar Hrothgar (`[name: Dominar]`; a portrait is requested), the gate-guard, the riders, the trench-hosts, Thornwatch's people, the bone-carters (Elder Ossa, Zainab), and every trainer.
- **Battles:**
  - **Gym 18:** single, `Prismfall.gym_battle(18)`, the den's heat rising each turn.
  - **The war legend:** whichever is about to fire on the other army. That's `:RESHIRAM_GLASS_DUNES` by default, or `:KYOGRE_GLASS_DUNES` if backing Ashkaar. On `:war_legend == :neither` there's no legend at the front, and the PC fights `:RESHIRAM_WYRMREST` at the Rift after the truce.
  - **No legendary is caught:** Reshiram goes to Sigrun, and Kyogre goes back to the sea.

**Counter:** V140 **CH19_STEP** (new; design/FLAGS.md):
- 0 the Truce Road
- 1 Wyrmrest's gate
- 2 "Weighed"
- 3 the oath (S153)
- 4 the word from the front, and the night flight
- 5 the Dry Tide at dawn (`:war_climax`)
- 6 the lines and the partner battle
- 7 the beam clash (WAR-1, the legend; S154 if a legend fought)
- 8 the truce, and the observers pack up
- 9 the Dominar (`:ch19_dominar`); the armistice (`:war_terms`, if one side won)
- 10 Wyrmrest again (Reshiram here on `:neither`; S154)
- 11 Gym 18 won: the badge case sings
- 12 the Rainbow Scar and the Pilgrim Road
- 13 Crownhaven's gate (chapter closed; V102 = 20)

**State set here:** S153 CH19_OATH_SPOKEN and S154 CH19_RESHIRAM_DONE. Keys: `:ch19_oath`, `:war_climax`, `:war_terms`, `:ch19_dominar`. The war outcome flags are computed by Core. Game over: `GO_LIARS_PYRE`.

## The chapter's key events (design/CHAPTER_BEATS.md)
1. **Sigrun's trial and the oath.** At the Draco brazier the PC says aloud what they'll do at the Festival (`:ch19_oath`, the PC's authored line). Reshiram wakes to the truth of it.
   - Build-up: "you never look back", "it says *walker*", Valen's message.
   - Consequence: the ending weight, Sigrun's consent, and Reshiram's arrival.
2. **The Battle of the Glass Dunes.** Kyogre's flood-sea meets Reshiram's fire over the dunes (WAR-1). The PC stands between, or backs a side (`:war_climax`).
   - Build-up: the six war choices since Ch11 (WAR_TRUST).
   - Consequence: the war's outcome, the Festival seats, and the hijack montage.

## Density (design/DENSITY_STANDARD.md; agents build from this section)
| Item | This chapter |
|---|---|
| Story/boss/rival fights (≥4) | All critical: **the lines** (1–2 gauntlet fights) · **the partner battle** · **the war legend** (or Reshiram at the Rift on `:neither`) · **Gym 18 Sigrun** · **the Dominar's Toll** (the pass-guard, single). Optional: the Thornwatch duel. |
| Route/gym/dungeon trainers (12–20) | 14 outside the gym (roster at the end) + Gym 18's 6 = 20 |
| EventMons (≥3) | **Goomy "Puddle"** (gift, the Thornwar Marches' rain-camp) · **Larvesta-free: Turtonator "Ember"** (static, the Wyrmspine's hot spring) · **Cufant "Patience"** (gift, the bone-carters, after the truce: "it pulled a cart of the dead across the glass and never complained") |
| Hangouts (2–4) | Sigrun on the Wyrmrest wall · Marisol at the Rimed Sands trench-head (after the truce) · Anja at the Siege Camp's well (if `:war_prisoner != :leave`) · Edda at Pilgrim's Rest |
| Glassfall Slivers (4–6) | 5: the Gloamwood's last lantern, Thornwatch's bell, the Wyrmspine's hot spring, the Rift's hoard, the Rainbow Scar's heart |
| Trials quests (≥3) | **New `AS_LIGHT_STONE_HOME`**: walk the Light Stone's empty cradle back to the Rift-shrine after the truce · Ashkaar's `AS_BRAZIER_WRIT` (if still open) · Elder Ossa's tomb-law registry: name 10 glassed dead on the new necropolis (new `OS_GLASS_NECROPOLIS`) · `AS_FORGE_REMEMBERS` (Brann, at Cindervault; most players find him here) |
| Badge overlay | Badge 18: `encounters_badgetiers.txt` tier for 860, 861, 872, 864 |

**No jokes** from the word from the front (V140 3 → 4) to the end of the truce (V140 8). "Weighed" (V140 1 → 2) is the chapter's only joke (15_COMEDY).

---

# CHAPTER 19 — "The Last Gate"

**Chapter start:** V102 = 19, V140 = 0. Gloaming's south gate. The quest log, "Eighteen Roads": *South-west through the Thornwar Marches to Wyrmrest. Gym 18. Then Crownhaven.*

## The Truce Road: 860 the Gloamwood (`:FAIRY_TALE`), 861 the Thornwar Marches, 870 Thornwatch
- **The Gloamwood's edge:** the dusk thins to day. The last Gloaming lantern hangs on a hawthorn at the wood's edge; behind it is a **Glassfall Sliver**.
- **The Thornwar Marches:** a border country of thorn hedges taller than houses, old Elowen–Ashkaar war-works overgrown, and rain.
  - **The rain-camp:** deserters from both armies (Ch18's are going the other way). **Gift: Goomy "Puddle"** (Lv 50, Hydration), from an Isenmar boy: "It followed me from the trenches. It likes the rain. Everybody here hates the rain. It's nice to have one of us who doesn't."
- **Thornwatch (870):** a watch-town on the border, with a bell in a hawthorn tower. Behind the bell is a **Glassfall Sliver**. The watch-captain: "Elowen's on one side of this hedge and Ashkaar's on the other. For three hundred years we've rung the bell when one side crossed. We've not rung it since the Accord. We nearly rang it last week. A dragon flew over. It was going *away*."
  - *Optional:* **the Thornwatch duel**, the watch-captain's spar (Lv 82).
- Trainers (Lv 80–81): the Gloamwood 2 (a lass, a pokéfan); the Marches 3 (a hiker, an ace trainer, an Ashkaar deserter); Thornwatch 1 (the bell-ringer).

## Map 872 — the Wyrmspine (`:MOUNTAIN`)
A spine of red rock, hot springs, dragons circling. At a hot spring in a cave mouth, a **Turtonator "Ember"** (static, Lv 80, Shell Armor) sleeps in the water with steam coming off its shell. The spring's ledge has a **Glassfall Sliver**.
Trainers (Lv 81–82): a dragon tamer, a black belt, a bird keeper.

## Wyrmrest: **the last gate** (autorun at the gate, 460, V140 == 0 → 1)
```
(Wyrmrest. A fortress-city carved into the red cliffs, dragon roosts on every ledge. At the great gate, a line of riders in dragonhide, barring it. Above them, standing on the gate itself in dragonhide with a Salamence coiled on the parapet beside her: Sigrun Ashfall.)
[name: Gate-guard] Halt. By the Dominar's order, the pass is closed to all things Zenith-tainted.
[name: Gate-guard] Meridian's Fellowship. Meridian's badge case.
(He looks at your case.)
[name: Gate-guard] Say true or say nothing.
[portrait: SIGRUN, neutral] (from the gate, without raising her voice; every rider hears it) Open it.
[name: Gate-guard] My lady, the Dominar —
[name: Sigrun] Wyrmrest is the last gate.
[name: Sigrun] Dragons don't let anything through they haven't weighed.
[name: Sigrun] *I* do the weighing. Not my father. Open it.
(The gate opens.)
[portrait: SIGRUN, neutral] (dropping down off the gate to stand in front of you) You don't challenge me yet. First you walk the Rift with me, to the Draco Plate, and you say out loud what you mean to do at the Festival. Then we'll see if you're worth a badge.
[portrait: SIGRUN, deadpan] Tomorrow. Tonight you eat. You look like a dragon's leftovers.
V140 = 1.
```
*(The gate-guard's "say true or say nothing" foreshadows `GO_LIARS_PYRE`. The Dominar is at the front: the Siege Camp, Ossaria's western dunes, the length of Ashkaar and half of Ossaria away.)*
- **Wyrmrest (460–462):** the Center, the Mart (Badge-17 stock, Dragon Fang, Elemental Seeds), the roosts. **Hangout, Sigrun on the Wyrmrest wall** (from V140 >= 1): *Weights and Measures*. She asks one honest question per visit and answers one.

### Comedy scene Ch19, **"Weighed"** (touch, Sigrun on the wall at night, V140 == 1 → 2)
As written in 15_COMEDY. It's the chapter's only joke. Then:
```
[portrait: SIGRUN, neutral] Sleep. The Rift doesn't care if you're tired.
[name: Sigrun] I do, a little. Don't tell anyone.
V140 = 2.
```

## The Wyrmscar Rift (864 `:CAVE` → 865 `:DRAGONS_DEN`): **Sigrun's trial** (touch, Sigrun at the Rift mouth, V140 == 2 → 3; key event 1)
A walk down into the Rift: a canyon of red glass and old dragon bones, with the den's heat rising. Sigrun walks beside the PC. The wild dragons stay back from her. Halfway, the hoard: a dragon's nest of gold and bones, with a **Glassfall Sliver** in it ("Take it. Dragons don't count glass.").
Trainers (Lv 82–83): 2 dragon tamers (Sigrun's own riders, testing).
```
(Halfway down, by an old roost, Sigrun stops. She doesn't look at you.)
[portrait: SIGRUN, neutral] He trained me to be his successor. Valen. Did you know that?
[name: Sigrun] I was going to wear it.
[portrait: SIGRUN, sad] Then he told me I'd never survive the Crown.
[name: Sigrun] And I was relieved. Do you understand? *Relieved.*
[name: Sigrun] And then he went looking for you. I knew. For two years I knew, and I let it happen, because it meant it wasn't me.
[portrait: SIGRUN, neutral] (walking on) I wanted you to know that before you swear anything in front of me.
```
**The Draco brazier** (the Rift's heart: a brazier of white fire over the Draco Plate's empty-looking niche):
```
[portrait: SIGRUN, neutral] Here. Say what you intend to do at the Festival.
[name: Sigrun] The fire hears. In Ashkaar, the fire is the court.
(The brazier burns white. It's waiting.)
> "I'm going to give them back." (return)
  Script: pf_choose(:ch19_oath, :return)
  \pf[PLAYER,neutral] I'm going to give them back.
> "I'm going to keep them safe. Whatever it costs me." (keep)
  Script: pf_choose(:ch19_oath, :keep)
  \pf[PLAYER,neutral] I'm going to keep them safe. Whatever it costs me.
> "I don't know yet. I'm going to find out with my eyes open." (open)
  Script: pf_choose(:ch19_oath, :open)
  \pf[PLAYER,neutral] I don't know yet. I'm going to find out with my eyes open.
> [if resonance <= -2] "I'm going to end it. All of it." (ruin)
  Script: pf_choose(:ch19_oath, :ruin)
  \pf[PLAYER,angry] I'm going to end it. All of it.
  (Sigrun's blade is out before you finish the sentence. She holds it there. Then, slowly, she lowers it.)
  [portrait: SIGRUN, shocked] ...The fire didn't burn you. You meant it.
  (She steps aside.)
  [name: Sigrun] Go. I'll weigh you in the hall. God help us both.
> "Whatever you want to hear."
  (The fire answers.)
  Script: Prismfall.game_over(:GO_LIARS_PYRE)
[on :return / :keep / :open]
  (The white fire leans towards you, and then up, like a candle when a door opens. Far away, somewhere, something answers it.)
  [portrait: SIGRUN, neutral] (very quietly) ...It heard. (She looks at you as if she's never weighed anyone before.) Good.
Switch S153 CH19_OATH_SPOKEN = ON. V140 = 3.
```
*(NARRATIVE_KEYS:)*
| Oath | Effect |
|---|---|
| `:return` | SIGRUN+3 RES+2 |
| `:keep` | SIGRUN−1 VALEN+3 ACCORD+1 |
| `:open` | SIGRUN+2 RES+1 |
| `:ruin` | SIGRUN−3 RES−3 |

*The fifth option is always offered. Its epitaph: "Ashkaar burns liars. It is the oldest law, and the dragons remember it even when men forget." The oath is what the Light Stone has been waiting for (14, "The battle").*

## **The word from the front** (autorun on leaving the Rift, V140 == 3 → 4; no jokes from here to the truce)
```
(The Rift mouth, at dusk. A rider coming in fast, his dragon lathered, before it's even landed.)
[name: Rider] My lady. The front.
[if :war_legend != :neither]
  [name: Rider] The sea-beast is up out of the Ice Vault.
  [name: Rider] It's dragging the Northern Sea across the Rimed Sands.
  [name: Rider] The Dry Tide's full again. And your father —
  (He looks at the Rift-shrine.)
  [name: Rider] Your father took the Light Stone to the front. While you were in the Rift.
  [name: Rider] He said, "if the god's fire won't come to me, I'll carry it."
[if :war_legend == :neither]
  [name: Rider] Both hosts are out of their lines.
  [name: Rider] Isenmar off the Rimed Sands, Ashkaar out over the Siege Camp's earthwork. On the dunes between.
  [name: Rider] Nobody's waiting for anyone's legend. They're going to do it themselves, at dawn.
[portrait: SIGRUN, angry] (already climbing onto her Salamence) Get on.
[portrait: SIGRUN, neutral] (holding a hand down to you) You swore something in there. Let's see if it holds in the open.
V140 = 4.
```
*(On `:war_legend == :neither` the Light Stone stays in its Rift-shrine. If `:ch8_lightstone` wasn't Wyrmrest, a Hearthguild runner is bringing it, and it arrives after the truce (V140 10).)*

## The night flight → the Dry Tide at dawn (930, built; V140 == 4 → 5)
```
[anim: night sky; Salamence's silhouette crossing the stars west to east; dawn breaking ahead; set down on the Dry Tide by the bone-carters' white banner]
(The bone-carters' camp on the Dry Tide, a mile behind the lines. Dawn.)
[if :war_legend != :neither]
  (Except the Dry Tide isn't dry. To the west, where the old seabed runs out to the Rimed Sands, there's water: grey, moving, rising. Over it, under a storm, something blue and enormous is swimming the sea it brought with it into the desert.)
(Ahead, the Glass Dunes between the two hosts. Isenmar's white trench-lines on one side, the Siege Camp's earthwork on the other. Both hosts out of their lines.)
[name: Elder Ossa] (at the banner, not looking at you) We'll be carrying out whoever's left, either way.
[name: Elder Ossa] I'd prefer fewer.
[portrait: SIGRUN, neutral] I'm Ashkaar.
[name: Sigrun] I'll stand with my father's riders unless you give me a reason not to.
(A beat.)
[name: Sigrun] Give me a reason.
```
**`:war_climax`** (MAJOR):
```
> Stand between them. (stand_between)
  Script: pf_choose(:war_climax, :stand_between)
  [portrait: SIGRUN, shocked] ...Between.
  (She looks at the dunes for a long time.)
  [portrait: SIGRUN, neutral] Then I'll stand between with you. My father can disown me after.
> Back Ashkaar. (back_ashkaar)
  Script: pf_choose(:war_climax, :back_ashkaar)
  [portrait: SIGRUN, neutral] (not pleased; not surprised) Then ride with me.
> Back Isenmar. (back_isenmar)
  Script: pf_choose(:war_climax, :back_isenmar)
  [portrait: SIGRUN, sad] (a long pause) Then I can't stand with you. Go to Marisol's lines.
  [name: Sigrun] If we meet on the glass —
  [portrait: SIGRUN, neutral] — we'll meet on the glass.
V140 = 5.
```
*(NARRATIVE_KEYS:)*
| Choice | Effect |
|---|---|
| `:stand_between` | RES+2 ACCORD+1 |
| `:back_ashkaar` | SIGRUN+2 MARISOL−4 RES−1 |
| `:back_isenmar` | MARISOL+3 SIGRUN−4 RES−1 |

*`WAR_STOPPED` = stand between with `tally(:WAR_TRUST) >= 4`. The tally is what both armies have seen the PC do: `:war_warning`, `:war_convoy`, `:war_prisoner`, `:war_legend`.*

## **The lines** (V140 == 5 → 6): a gauntlet through the side you didn't choose, then a partner battle
- **`:back_ashkaar`** goes through **Isenmar's trench-lines** (920). There are two trench fights (`ISENMAR_TRENCHER` ×2, Lv 83), then the partner battle **PC + Sigrun** against an Isenmar pair (Thane's Hirdmen, Lv 84) on `:FROZEN_LAKE` (the frozen sand).
- **`:back_isenmar`** goes through **the Siege Camp's earthworks** (924). There are two earthwork fights (`ASHKAAR_SOLDIER` ×2, Lv 83), then the partner battle **PC + Marisol** against an Ashkaar pair (Ember-Riders, Lv 84) on `:DESERT`.
- **`:stand_between`** goes **through the Steamline** (925), between both hosts. There's one fight on each side (an Isenmar trencher and an Ashkaar soldier, Lv 83). Then comes the partner battle **PC + Sigrun** against a *mixed* pair, an Isenmar hirdman and an Ashkaar ember-rider who've both decided the PC is the enemy, on `:BLEED` (the Steamline). Sigrun: "They agree on something. Wonderful. It's us."
```
Script: pbRegisterPartner(:LEADER_SIGRUN, "Sigrun", 19)   # or (:LEADER_MARISOL, "Marisol", 19) on :back_isenmar
BATTLE (`:back_ashkaar`):  TrainerBattle.start(:ISENMAR_HIRDMAN, "Hjalmar", :ISENMAR_HIRDMAN, "Torunn") — tag double; `:FROZEN_LAKE`; Lv 83–84.
BATTLE (`:back_isenmar`):  TrainerBattle.start(:ASHKAAR_EMBER_RIDER, "Vharn", :ASHKAAR_EMBER_RIDER, "Ashild") — tag double; `:DESERT`; Lv 83–84.
BATTLE (`:stand_between`): TrainerBattle.start(:ISENMAR_HIRDMAN, "Styr", :ASHKAAR_EMBER_RIDER, "Kessa") — tag double; `:BLEED`; Lv 83–84.
(The gauntlet singles before it: `[ISENMAR_TRENCHER,Ulfa]` and `[ISENMAR_TRENCHER,Bersi]` on 920; `[ASHKAAR_SOLDIER,Garrok]` and `[ASHKAAR_SOLDIER,Senna]` on 924; Ulfa and Garrok on 925.)
(On the built maps (mapgen/layouts/war_craft.py): the singles stand at the Rev 18 trench gaps and earthwork gates; each pair is a sight-4 trainer event at the last gap (920 47,14; 924 35,16; 925 32,26 on the road to the crest exit), which registers the partner, sets the field and on a win sets `pfm(:war_partner_done)` (926's legend waits for it) and V140 = 6.)
(LOSE: whiteout to 930; the lines restart, and the choice is kept.)
V140 = 6.
```

## **The beam clash** (the Glass Dunes, 926, built; V140 == 6 → 7; key event 2)
**[if `:war_legend != :neither`]** **Cutscene WAR-1 "The Beam Clash on the Glass Dunes"** (13_CUTSCENES, ~95 s) plays up to **shot 3**: the Light Stone wakes in the Dominar's hand, answering the PC's oath. Then the boss:
```
[if :back_ashkaar]
  (Kyogre rises out of its flood-sea, Origin Pulse gathering, turned on the Siege Camp's earthwork, on Sigrun's people, on you.)
  BATTLE: Prismfall::Bosses.wild_battle(:KYOGRE_GLASS_DUNES) — 3 bars; 926's own field (DESERT → FLOODED_DUNES → GLASS_DUNES).
[else]
  (Reshiram unfolds over the Siege Camp, the Light Stone's white fire in its throat, and turns towards the Isenmar lines.)
  BATTLE: Prismfall::Bosses.wild_battle(:RESHIRAM_GLASS_DUNES) — 3 bars; 926's own field (DESERT → FLOODED_DUNES → GLASS_DUNES).
(LOSE: whiteout to 930; the boss restarts at bar 1.)
Switch S154 CH19_RESHIRAM_DONE = ON (on either legend; the Reshiram story beat is "it chose Sigrun", below).
```
Then **WAR-1 plays from shot 4 to the end.** The outcome is chosen by the flags:
- **`WAR_STOPPED`:** both lines hold fire. The Origin Pulse and the Blue Flare meet over the PC, and the PC's shard (and Sigrun, and Anja or Marisol) holds them apart, and they part. The flood goes back to the sea with Kyogre, and the glass stops where it is.
- **`WAR_BOTH_BROKEN`:** nobody listens. The clash detonates over the dunes and glasses both front lines where they stand.
- **`WAR_ASHKAAR_WON` / `WAR_ISENMAR_WON`:** the loser's host breaks. Isenmar falls back behind Skaldfast's walls, or Ashkaar back over the Siege Camp's earthwork, and the winner's banners go up.

**[if `:war_legend == :neither`]** There is no legend, no flood and no fire, and no boss here. The clash is between the Wardens' aces instead, in a cutscene variant of WAR-1 (the cutscene plugin's `legends: false`): Sigrun's Salamence against Anja's Mamoswine (or Marisol's Gyarados), over the dunes, while both hosts watch. The outcome flags apply as above. The Light Stone stays dark in its shrine. Reshiram's fight happens at the Rift after the truce (V140 10).
```
V140 = 7.
```

## **The truce** (autorun after WAR-1, the Glass Dunes, V140 == 7 → 8)
```
(Silence on the dunes. Steam rising off new glass. The two hosts, what's left of them, standing in their lines and looking at the middle.)
(In the middle, on the glass: Sigrun, and Anja [if :war_prisoner != :leave] / Marisol [else], and you.)
[portrait: SIGRUN, neutral] (loud enough for both hosts) The legends have left. Reshiram to me. The sea-beast to the sea.
[name: Sigrun] Nobody won this morning that the dead would agree with.
[if :war_prisoner != :leave]
  [portrait: ANJA, neutral] (in her furs, thinner, on the glass beside her) Settle it at the Festival. By the Boon. Both crowns, one table.
  [name: Anja] I'll count the votes. I'm good at counting.
[else]
  [portrait: MARISOL, neutral] Settle it at the Festival. By the Boon.
  [name: Marisol] I'm sick of burying sailors in sand.
(Across the glass, both hosts lower their weapons. Not all at once. Enough.)
[name: Larch (radio)] (crackling, from your pack) Child. Child, are you there?
[name: Larch (radio)] Look at the mesa. Behind the Ashkaar lines.
(On a sandstone mesa behind the lines: tents, instruments, people in Meridian white. Packing up. Fast. Before the steam clears.)
[name: Larch (radio)] That wasn't a battle to them. That was a *reading*.
(The bone-carters walk out onto the glass under a new white banner, Elder Ossa at the front and Zainab with her book, to count the glassed dead standing in it.)
V140 = 8.
```
*The Glass Dunes stay glass: a steam-glass plain across the caravan road, with both armies' glassed dead standing in it. Ossaria claims it under tomb-law, the newest necropolis in the Bone Sands, and the only one with no Ossarians in it.*
- **New: `OS_GLASS_NECROPOLIS`** (optional; Zainab): name ten of the glassed dead for the tomb-law registry (each a short inscription found on the dead: a ring, a tag, a letter). The reward is **Cufant "Patience"** (Lv 55, Sheer Force), from the carters: "It pulled a cart of the dead across the glass and never complained. It wants a lighter job."
- **Hangouts after the truce:** **Marisol at the Rimed Sands trench-head**, and **Anja at the Siege Camp's well** (if `:war_prisoner != :leave`): *Counting the Living*.

## **The Dominar** (the Command Pavilion, 928, built; touch, V140 == 8 → 9)
```
(The Command Pavilion. The oath-brazier, white at the heart. The lacquer map table. The black-glass stand, empty, still dusty where something round sat. The Dominar of Ashkaar in a plain red coat, a burnt hand bandaged, the Light Stone's cradle-cloth on the table in front of him, empty.)
[portrait: HROTHGAR, neutral] My daughter flew the Unimprinted into my war.
[name: Dominar] She tells me you swore an oath at the Draco Plate and the fire believed you.
(A beat.)
[name: Dominar] Speak plainly. The brazier is lit.
[name: Dominar] I mean to march on Zenith the hour the Festival ends.
[name: Dominar] Meridian bought my sand from that fat Elector, armed my enemies and watched us bleed from a hill.
[name: Dominar] Give me a reason to fly *for* Crownhaven instead.
```
**`:ch19_dominar`:**
- It succeeds with (`:ch8_lightstone == :wyrmrest` **and** the ARBITER BLUEPRINTS or the LARCH PAPERS) **or** `bond(:SIGRUN) >= 4`:
```
[if proof]
  (You lay out the blueprints on his map table: the eighteen locks under the arena. CALIBRATION SUBJECT: UNIMPRINTED-01.)
  [name: Dominar] (reading, in silence, for a long time) ...And they were on the mesa this morning. Reading us.
[if bond(:SIGRUN) >= 4]
  [portrait: SIGRUN, neutral] (from the tent-flap) Father. I weighed them. They're light. They're true. Fly.
[portrait: HROTHGAR, neutral] If the god is in chains, then dragons will break them.
[name: Dominar] Not for the Accord. For the god.
Script: pf_choose(:ch19_dominar, :swayed)
```
- Otherwise:
```
[portrait: HROTHGAR, neutral] Words. Good words. The fire liked them.
(He turns the cradle-cloth over.)
[name: Dominar] My riders go home after the truce.
[name: Dominar] Crownhaven can defend itself. It always says it can.
Script: pf_choose(:ch19_dominar, :failed)
```
*(`DOMINAR_SWAYED` can't be set if Isenmar won without mercy terms. With it, his legions are present in the hijack. The black-glass stand is an Act V mystery (09); don't explain it.)*

**The armistice** (`:war_terms`; **only if one side won**; Skaldfast's great hall, by Gale Post skiff; a single scene)
```
(Skaldfast's great hall. A long table. The Thane at one end, the Dominar at the other, neither looking at the other. At the side of the table, uninvited, in silk, eating dates: Prince-Elector Kassan.)
[portrait: KASSAN, smug] Nobody signs anything about my sand without me. Do go on.
> Argue for mercy (both armies off the sands). (mercy)
  Script: pf_choose(:war_terms, :mercy)
> Argue for reparations (the loser pays). (reparations)
  Script: pf_choose(:war_terms, :reparations)
  [portrait: KASSAN, happy] And I bill them both. Lovely.
> Argue for occupation (the winner garrisons the dunes). (occupation)
  Script: pf_choose(:war_terms, :occupation)
  [portrait: KASSAN, happy] And I extend the Lease. For ever. How wonderful.
V140 = 9.
```
*(NARRATIVE_KEYS: `:mercy` RES+2; `:reparations` ACCORD+1; `:occupation` RES−2 ACCORD−1. Occupation poisons the Good ending: Arceus won't bless a land with a boot on its neck. The occupied ground is Skaldfast and the Mast Glacier road if Ashkaar won, or Glasswake and the Cinderglass Barrens if Isenmar won.)*

## Wyrmrest again (Sigrun flies the PC back; V140 == 9 → 10)
**[if `:war_legend == :neither`]** **Reshiram at the Rift-shrine** (the stone comes home):
```
(The Rift-shrine. The Light Stone back on its hook [or: carried in by a Hearthguild runner, red-faced, out of breath, "From Brann. He says sorry it's late. He says it was always late."].)
(It cracks. White fire, all the way up the Rift, and out of it, unfolding, a white dragon that looks first at the brazier, then at you.)
BATTLE: Prismfall::Bosses.wild_battle(:RESHIRAM_WYRMREST) — 3 bars; `:DRAGONS_DEN`. (Its fire is the truth of the oath: Return and Open lean Harmony, Keep is neutral, Ruin is savage.)
(LOSE: whiteout to 461; the boss restarts at bar 1.)
Switch S154 CH19_RESHIRAM_DONE = ON.
```
**On every path, Reshiram and Sigrun** (the Rift-shrine, or the Glass Dunes' edge if it fought there):
```
(Reshiram lands in front of Sigrun. Not you. It lowers its great white head until its brow touches the dragonhide on her shoulder.)
(Then it's gone, up, north, towards Crownhaven, ahead of everyone.)
[portrait: SIGRUN, shocked] (her hand still up where its head was) ...It chose the one who finally said it out loud.
[portrait: SIGRUN, neutral] (to you, roughly) Not me. You. I've been saying nothing for two years.
[name: Sigrun] You said it in front of the fire.
(She lets her hand drop.)
[name: Sigrun] Come to the hall. Let's see if you can beat me.
V140 = 10.
```
- **New: `AS_LIGHT_STONE_HOME`** (optional; the Rift-shrine keeper): the Light Stone's empty cradle-cloth goes back to the shrine from the Dominar's table, carried on foot down the Rift, with the keeper's three questions to answer truthfully (the Rift's version of a fetch quest). The reward is the Dragon Scale and the shrine's blessing (a Codex line).

## Gym 18 — the Weighing Hall (470–475, `:DRAGONS_DEN`)
As GYM_PUZZLES Gym 18:
| Room | Name | Type |
|---|---|---|
| 470 | Gate | teach |
| 471 | Wyrm's Spine | recall |
| 472 | Statue Court | twist: "the chained ring" |
| 473 | Hoard Scales | combine |
| 474 | the arena | |
| 475 | the Weighing of the Heir | Mastery, optional |

Gym trainers (6): Cool Trainers ×4, Ace Trainers ×2; Lv 81–84.

### 474 — the Warden Arena
```
[portrait: SIGRUN, neutral] The den's heat rises every turn.
[name: Sigrun] The dragons get stronger the longer you hesitate. So don't.
[name: Sigrun] If you can't beat me, you can't survive him.
[name: Sigrun] I'm not going easy. I've been easy for two years.
BATTLE: Prismfall.gym_battle(18)
```
- **Mid-battle (Salamence Mega Evolves):** "Weighed, and found wanting. That's what Father says when he loses. I've never heard it from this side." `[bubble: SIGRUN, smug, sparkle]`
- **Win:**
```
[portrait: SIGRUN, happy] (breathing hard, laughing, for the first time in the game) There. There it is. Eighteen.
RECEIVE: the WYRM BADGE (badge 18). RECEIVE: TM? DRACO METEOR (per the TM table; WALKTHROUGH).
(Your badge case, in your hands, sings. All eighteen tones together, the full chord. The hall's dragons lift their heads.)
[if :ch14_telemetry == :leave]
  (Through the hall's high window, on the horizon, a Meridian airship that has been sitting there all morning turns, within the minute, and heads north. Towards Crownhaven.)
[if :ch14_telemetry == :sabotage]
  [name: Larch (radio)] (crackling) ...He bought it. God help us, he bought it.
  [name: Larch (radio)] A quarter-tone flat, all eighteen.
  [name: Larch (radio)] Every lock in that arena is built to a wrong note.
[if :ch14_telemetry == :destroy]
  (The case sings, and nobody is listening but you. It's the first time it's only been yours.)
V140 = 11.
```
*(The badge name is a proposal: the **Wyrm Badge**. The VS plate reads VALKYRIE above SIGRUN. The TM is whatever WALKTHROUGH's TM table lists for Gym 18; agents should fill it in from there.)*

## The road to Crownhaven: the Rainbow Scar (868, `:RAINBOW`) and the Pilgrim Road (V140 == 11 → 12)
- **The Rainbow Scar:** a Bleed zone where all eighteen Imprints bleed together into light. It foreshadows the Prism Arena. Walking through it, the PC's sprite tints through the eighteen colours in sequence. At its heart, in the brightest light, is a **Glassfall Sliver**.
- **Dominar's Toll (892):** an Ashkaar toll-gate on the Pilgrim Road.
  - **The pass-guard**, a single battle (Lv 84). Before the fight: "The Dominar's toll. A battle. It's always a battle. It's a very old toll."
  - `DOMINAR_SWAYED`: he salutes and waves the PC through after the battle anyway: "Habit."
- **The Pilgrim Pass (880) and Pilgrim's Rest (890):** pilgrims and Festival crowds, and souvenir sellers selling eighteen-colour ribbons. **Hangout, Edda at Pilgrim's Rest** (from V140 >= 12): *Last Port*. She is staying for the Festival: "Wouldn't miss it. I've got a bet on."
- Trainers (Lv 84): the Pilgrim Pass 2 (a pilgrim, an ace trainer); the Coronation Road 1 (a Festival hopeful).

### The Ascent or the Scar (the last stretch; V140 == 12 → 13)
- **`standing(:ACCORD) >= 4` or has ROYAL WRIT: the Sovereign's Ascent** (884–886). The Wardguard escort takes the PC up the processional stair, with banners. A Wardguard sergeant: "Eighteen badges. You're the first in ten years to come up the stair with eighteen. Mind the forty-third step, it's loose. It's been loose for three hundred years. Tradition."
- **Otherwise: the Glassfall Scar** (888). Edda's smugglers take the PC through Lower Crownhaven, where the forty Fixed of AF 290 still stand where they fell.
```
(Lower Crownhaven. Old stone streets under the arena's shadow, roped off for ten years. Standing in them, glass, forty people, exactly where the light caught them. A man with his hat half off. A woman holding a child's hand; the child isn't there.)
(At the front of a broken stand: a Choir cantor with her mouth open mid-note. She isn't Ines. Ines got out.)
(Further on, a little space between two of them where nobody's standing. A child-sized space. The stone there is clean, where a five-year-old stood and glowed and didn't fall down.)
(You stand in it. You fit. You don't anymore; you're much bigger. You stand in it anyway.)
```
**Crownhaven's gate** (chapter close; autorun)
```
(Crownhaven. The capital above the clouds. The new Festival arena, eighteen-sided, gold and glass, built in ten years on top of the old one. Banners of every kingdom. The Peace of Plates posted on every wall: a truce for the Festival.)
(Somewhere in that arena, under the stands, eighteen locks.)
V140 = 13. Variable V102 STORY_CHAPTER = 20.
QUEST LOG: "Eighteen Roads" — Complete. Eighteen badges.
QUEST LOG: "The Festival of Champions" — Crownhaven. Seven days. Valen said he'd tell you everything.
```
*(Ch20 opens on Festival Day 1: the Veil Gate, the registration, the opening ceremony.)*

---

## Map events needed (Chapter 19)

**Built:** 920, 924, 925, 926, 928, 929, 930. **[NEW]** = an event or map not in maps.json. V140 = **CH19_STEP** (design/FLAGS.md). Maps go through the three-pass workflow (design/MAPGEN.md, top).

**860 Gloamwood / 861 Thornwar Marches / 870 Thornwatch:**
- the last lantern (**Sliver #1**)
- thorn-hedge mazes and rain
- the rain-camp (**Goomy "Puddle"** gift)
- Thornwatch's bell tower (**Sliver #2**) and the watch-captain (optional duel)
- 6 trainers

**872 Wyrmspine** (`:MOUNTAIN`):
- red rock and hot springs (steam animation)
- **Turtonator "Ember"** static, and **Sliver #3** on the spring ledge
- 3 trainers

**460 Wyrmrest / 461 Center / 462 Mart:**
- the gate, with riders barring it; Sigrun on the parapet; the gate-opening event (V140 0 → 1)
- dragon roosts with circling dragon events
- **the wall at night** ("Weighed": Salamence sits on the PC (a jump onto the player tile and a squash animation); V140 1 → 2; Sigrun's hangout)

**864/865 Wyrmscar Rift** (`:CAVE` → `:DRAGONS_DEN`):
- the walk with Sigrun as a follower NPC; her confession at the roost
- the hoard (**Sliver #4**)
- **the Draco brazier**: the oath menu with five options (`GO_LIARS_PYRE` on the fifth); the white fire leaning (picture/flash); S153; V140 2 → 3
- the rider arriving (V140 3 → 4)
- the Rift-shrine: the Light Stone hook; **Reshiram at the shrine** on `:neither` (V140 9 → 10); Reshiram's bow to Sigrun; `AS_LIGHT_STONE_HOME`
- 2 trainers

**930 bone-carters' camp** (built): the dawn landing; the flood to the west on non-`:neither` (a water overlay on the Dry Tide's edge); Elder Ossa; **`:war_climax`** (V140 4 → 5).

**920 / 924 / 925** (built): the gauntlet fights by branch (see "The lines"); **the partner battle** (V140 5 → 6).

**926 Glass Dunes** (built):
- **WAR-1** (cutscene; plugin `legends:` by `:war_legend`)
- **the legend boss** (`:RESHIRAM_GLASS_DUNES` or `:KYOGRE_GLASS_DUNES`; S154)
- the outcome swaps; **the truce on the glass** (V140 7 → 8)
- the bone-carters' new banner; `OS_GLASS_NECROPOLIS` (10 inscription events; **Cufant "Patience"**)

**929 Observers' Mesa** (built): the Meridian observers packing up (a move route out) during the truce.

**928 Command Pavilion** (built): **the Dominar** (`:ch19_dominar`; V140 8 → 9).

**Skaldfast's great hall** [NEW small interior]: the armistice (`:war_terms`; only if a side won).

**470–475 Gym 18:** as GYM_PUZZLES; 6 trainers; Sigrun (474); the badge case singing (a chord SE plus a screen flash in 18 colours); the telemetry variant (the airship picture, the Larch radio, or nothing); V140 = 11.

**868 Rainbow Scar** (`:RAINBOW`): the PC tint cycling through 18 colours; **Sliver #5**.

**892 Dominar's Toll:** the pass-guard battle.

**880 / 890 / 893:** pilgrim crowds; Edda's hangout at 890; 3 trainers.

**884–886 Sovereign's Ascent** *or* **888 Glassfall Scar:**
- the Ascent: banners, the Wardguard escort
- the Scar: the 40 Fixed as glass statues (decor events), the cantor, and **the child-sized space** (a stand-in event)

**Crownhaven gate** (the close): V140 = 13; V102 = 20.

## Trainer roster (Ch19; 14 regular trainers outside the gym; PBS blocks in 3 versions; ≤ 85)
| Map | Class (stock type) | Name | Lv | Team idea (field touch) |
|---|---|---|---|---|
| 860 | Lass | Bramble | 80 | Florges, Whimsicott, Comfey |
| 860 | Pokéfan | Mr. & Mrs. Hollin | 80 | Togekiss, Clefable (Fairy Tale: Fairy shines) |
| 861 | Hiker | Old Corran | 80 | Gigalith, Rhyperior, Avalugg |
| 861 | Ace Trainer | Isolde | 81 | Hydreigon, Volcarona, Kingambit |
| 861 | Ashkaar Deserter *(ASHKAAR_SOLDIER)* | Ex-Rider Brann-no-relation | 81 | Dragonite, Haxorus |
| 870 | Bell-ringer *(Gentleman)* | Mr. Peal | 81 | Bronzong, Noivern, Exploud |
| 872 | Dragon Tamer | Ysra | 82 | Garchomp, Kommo-o, Flygon |
| 872 | Black Belt | Master Ruo | 82 | Lucario, Hawlucha, Kommo-o |
| 872 | Bird Keeper | Kesh | 82 | Braviary, Talonflame, Noivern |
| 864 | Dragon Tamer ×2 *(Sigrun's riders)* | Riders Hjal and Ama | 83 | Salamence, Dragapult / Altaria, Baxcalibur |
| 880 | Pilgrim *(Hiker)* | Pilgrim Ennis | 84 | Golurk, Bronzong, Sigilyph |
| 880 | Ace Trainer | Corinne | 84 | Metagross, Gyarados, Volcarona |
| 893 | Festival Hopeful *(Ace Trainer)* | Dane | 84 | Garchomp, Rotom-Wash, Scizor, Gardevoir |
| **Gym 18** | Cool Trainer ×4, Ace Trainer ×2 | (GYM_PUZZLES) | 81–84 | as GYM_PUZZLES |

**Story fights (new PBS):**
- Partners (**in PBS**, one version each): `[LEADER_SIGRUN,Sigrun,19]` (Haxorus 83, Dragapult 84, Salamence "Dreamwing" 84) and `[LEADER_MARISOL,Marisol,19]` (Barraskewda 83, Kingdra 84 with Rain Dance, Gyarados "Lucky" 84).
- The war pairs, Lv 82–84 (**in PBS**, no Bag; new trainer types `ISENMAR_TRENCHER`, `ISENMAR_HIRDMAN` "Thane's Hirdman", `ASHKAAR_EMBER_RIDER` "Ember-Rider"): Trenchers Ulfa and Bersi, Hirdmen Hjalmar + Torunn, Soldiers Garrok and Senna (`ASHKAAR_SOLDIER`), Ember-Riders Vharn + Ashild, and the mixed pair Hirdman Styr + Ember-Rider Kessa.
- The Dominar's Toll pass-guard: `[ASHKAAR_OFFICER,Orrin]` (**in PBS**; Pyroar, Tyrantrum, Archaludon, Charizard 84; no Bag).
- The Thornwatch captain (optional): `[THORNWATCH,Brome]` (**in PBS**; new type "Watch-Captain"; Bronzong, Brambleghast, Ferrothorn, Hydrapple "Windfall" 82; no Bag).

**Bosses:** `:RESHIRAM_GLASS_DUNES` / `:KYOGRE_GLASS_DUNES` (existing), `:RESHIRAM_WYRMREST` (**new**, 110).

**Items owner:**
- the WYRM BADGE (proposed); Gym 18's TM (per WALKTHROUGH's table)
- Glassfall Slivers #1–5 of the Ch19 allotment
- Elemental Seed ×2 + Dragon Fang (Mastery)
- Dragon Scale (`AS_LIGHT_STONE_HOME`)

**EventMons:** Goomy "Puddle" (gift, Lv 50), Turtonator "Ember" (static, Lv 80), Cufant "Patience" (`OS_GLASS_NECROPOLIS`, Lv 55).

**Portrait requests (art, to Gemini):** **DOMINAR HROTHGAR** (`neutral`, `angry`), **SIGRUN** `happy` and `shocked`, ANJA thin (variant).
