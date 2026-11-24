# Script: Chapter 18 — "Once Upon a Time" (the Blind Road; the Lightless Deep and Pecharunt; the Gloamwood Verge; Gloaming, Gym 17; the envoys; the Hymn of Return; K7)

> **Final playable script** for Chapter 18, the first chapter of Act V.
> - **Maps:** the Blind Road out of Underveil (852 the Throat, 840 the Blindwater, 844/845 the Lightless Deep, 848 the Inverted Ward (optional), 850 Mothwell, 841 the Gloamwood Verge), then Gloaming (440–455: the town 440, the lantern-moth market, Maelis's dusk-garden, the dusk-chapels, the Great Tree Roots 443, Gym 17 450–455).
> - **Status:** none of these is built. The list at the end is what to build from.
> - **Order:** follows `story/36_SCRIPT_CH17.md`. Chapter 19 ("The Last Gate") follows.
> - **Sources:**
>   - Story: 08_ACT_V Ch18; 03_CAST (Celestine, Kestrel, Juno, Maelis, Caedmon, Mother Gutter, Corvin, Ysolde, Sigrun, Marisol); 09_MYSTERIES; 14_WAR_AND_BLESSING (`:war_legend`; the Ch18 deserters); 15_COMEDY Ch18 "Phrasing".
>   - Keys: NARRATIVE_KEYS (`:ch18_kestrel_ring`, `:war_legend`, `GO_FAIR_BARGAIN`, `GO_STAY_OUT`, `OGERPON_TRUSTED`, `KESTREL_FALLEN`).
>   - Design: GYM_PUZZLES Gym 17; WALKTHROUGH Ch18; CAMEOS §7 "Dreamwalker"; `design/CHAPTER_BEATS.md`; `design/DENSITY_STANDARD.md`; POKEMON_AVAILABILITY §4 (no legendaries in the party).
>   - Quests: the Trials quests `NA_SWEETROT`, `EL_TWILIGHT_CLOISTER`, `EL_ENCORE`.

## Conventions
As in the earlier scripts.
- **Portrait cast:** Celestine, Kestrel, Juno, Mother Gutter, Corvin (if `CORVIN_FREED`), Maelis, Caedmon (one line), Shiv (cameo), and the PC (one authored line, to Kestrel).
- **Plain:** the thralls, the Thornguard captain, the lantern-moth vendors, the deserters, the two envoys (Isenmar's skald Hallgerd and Ashkaar's Ember-Captain Tavi), the Gloaming choir, and every trainer.
- **Gym 17** is a double: `Prismfall.gym_battle(17, double: true)` (GYM_PUZZLES: "the knight and the dragon").
- **K7:** `Prismfall.rival_battle(:RIVAL_KESTREL, "Kestrel", 7, field: :FAIRY_TALE)` (versions 70–72).
- **Pecharunt:** `Prismfall::Bosses.wild_battle(:PECHARUNT_DEEP)`. It's registered now (`plugins/Prismfall Bosses/109_Boss_Pecharunt.rb`) and is `:catch => false`.
- **Ogerpon** walks with the PC as a follower, never in the party (POKEMON_AVAILABILITY §4).

**Counter:** V139 **CH18_STEP** (new; design/FLAGS.md):
| Value | Meaning |
|---|---|
| 0 | the Throat |
| 1 | the Lightless Deep: the first thrall |
| 2 | Pecharunt (S150) |
| 3 | the Gloamwood Verge: Celestine |
| 4 | Gloaming |
| 5 | the envoys (`:war_legend`) |
| 6 | Gym 17 won |
| 7 | the Hymn (S151) |
| 8 | K7 (S152) |
| 9 | Kestrel leaves (chapter closed; V102 = 19) |

**State set here:**
- **Switches:** S150 CH18_PECHARUNT_DONE, S151 CH18_HYMN_GOT, S152 CH18_K7_DONE.
- **Variables:** V114 KESTREL_STAGE = 4.
- **Keys:** `:war_legend`, `:ch18_kestrel_ring`.
- **Game overs:** `GO_FAIR_BARGAIN`, `GO_STAY_OUT`.
- **Key Items:** THE HYMN OF RETURN (complete), ROYAL WRIT (optional, Maelis).

## The chapter's key events (design/CHAPTER_BEATS.md)
1. **Pecharunt in the Lightless Deep.**
   - The source of Sweetrot. Its fall frees the thralls across Nadir.
   - The old story turns over: the Loyal Three were Pecharunt's thralls, and the "Gossamer Ogre" drove them off.
   - **Build-up:** Sweetrot since Act II, Corvin's ledger, Wenlow's notes, the Ch10 Loyal Three.
   - **Consequence:** the Sweet Market wakes, and `NA_SWEETROT` opens.
2. **The Hymn of Return, then K7.**
   - Celestine has the Gloaming choir sing the whole Hymn: "It says *walker*."
   - At the Great Tree's roots, Kestrel begs you to stay out of Crownhaven (`:ch18_kestrel_ring`; `GO_STAY_OUT`).
   - **Build-up:** Wick's verse (Ch10), Maren's page (Ch17), Morwen's Ring (Ch15).
   - **Consequence:** the Return path, and Kestrel's Mega at K8.

## Density (design/DENSITY_STANDARD.md; agents build from this section)
| Item | This chapter |
|---|---|
| Story/boss/rival fights (≥4) | **Pecharunt** · **the Thornguard captain** (single, at the Verge; Celestine stops the second fight) · **Gym 17 Celestine** (double) · **K7** (all critical) · optional: Shiv ("Dreamwalker") |
| Route/gym/dungeon trainers (12–20) | 11 outside the gym (roster at the end): the Throat 2, the Blindwater 3, the Inverted Ward 2, Mothwell 2, the Gloamwood Verge 2; plus Gym 17's 10 (8 princesses as a gauntlet, a Lady and a Beauty; GYM_PUZZLES) = 21 |
| EventMons (≥3) | **Poltchageist** (`NA_SWEETROT` reward, as catalogued) · **Hatenna "Hush"** (gift, an Ashkaar deserter in Gloaming) · **Morelull "Lamp"** (static, Mothwell's lantern-pool) |
| Hangouts (2–4) | Celestine in the dusk-chapel · Juno at the bakery (dusk-honey cakes) · Corvin at the Deep's mouth (`CORVIN_FREED`) or Mother Gutter on the Moon Market steps (else) |
| Glassfall Slivers (4–6) | 5: the Throat's echo-ledge, the Blindwater's dry island, the Inverted Ward's ceiling (which is the floor), Mothwell's lantern-pool, the Great Tree's root-knot |
| Trials quests (≥3) | `NA_SWEETROT` (after S150) · `EL_TWILIGHT_CLOISTER` · `EL_ENCORE` (Dorian, Saltmere; available here) · the "Dreamwalker" cameo (CAMEOS §7, after Gym 17) |
| Badge overlay | Badge 17: `encounters_badgetiers.txt` tier for 840, 841, 848, 850 |

**No jokes** in the Lightless Deep (V139 0 → 2), or from the Hymn (V139 6 → 7) to the end of the chapter. "Phrasing" plays at V139 4–5.

---

# CHAPTER 18 — "Once Upon a Time"

**Chapter start:** V101 = 5, V102 = 18, V139 = 0. Morning in Underveil, the day after the docks. The quest log: "Eighteen Roads": *Two badges left. Gloaming, and then Wyrmrest. Then Crownhaven.* Also *Corvin has traced the Sweetrot down, not up.*

## The Moon Market steps: **down, not up** (touch, the Throat's gate, 852)
```
[if CORVIN_FREED]
  [portrait: CORVIN, neutral] (at the Throat's gate with a lamp and a satchel of sample-jars, the mask back on, his voice flat) I came down from Cragholm on the first lift. I wasn't going to stay away. Not now.
  [portrait: CORVIN, neutral] Sweetrot. Twenty years I've been treating it. Today I traced it. It doesn't come from the Barons. It comes from under them. Down. Wenlow worked it out first, from the ward notes. I didn't read them until — (He stops.) I read them.
[else]
  (A satchel left on the Throat's gate, with a note pinned to it in a cheerful, clumsy hand: *"Dr. C — the Sweetrot ISN'T from the Barons!!! It comes from UNDER. Down the Throat. I'll show you when you're back!!! — W."*)
  (Underneath, in a different hand, a Hollow runner's: "Found in the Infirmary. Thought someone should have it.")
```
*(Wenlow's notes are how the PC finds the Deep on both branches. Corvin's on-screen grief is restrained: he never says the name.)*

## Map 852 — the Throat (`:NEW_MOON`) and 840 the Blindwater (`:CAVE`)
- **The Throat:** a sinkhole stair below the drained Sump, so dark the PC's lamp shows only a step ahead. On an echo-ledge, a call answers the PC's footsteps one beat late. Behind it: **Glassfall Sliver**.
- **The Blindwater:** an underground lake, black and still. The wild Pokémon are blind (Rock Smash and Flash optional). On a dry island in the middle (reached by Surf in the dark): **Glassfall Sliver**.
- A lost Sump miner, holding a lamp: "Smell that? Sweet. You don't smell sweet down here. Not natural."

Trainers:
- the Throat (Lv 75): a punk, a hex maniac;
- the Blindwater (Lv 75–76): a fisher, a ruin maniac, a black belt meditating in the dark ("I came down to train without sight. I've learnt one thing. I miss sight.").

## Map 844 — the Lightless Deep (`:DARK_CRYSTAL`): **the first thrall** (touch, the cavern's mouth, V139 == 0 → 1)
```
(A cavern of pink crystal, lit from inside, warm, smelling of peaches. In rows across the floor, peach-shaped growths on vines, the size of a head, and between them, people: Nadir people, in their work-clothes, tending the growths with watering-cans, smiling. All of them smiling. None of them looking up.)
(Among them, in her waxed coat, her ledger under one arm, watering a growth with tender care: Mother Gutter.)
[portrait: GUTTER, happy] (not looking at you, smiling) Oh, it's you, topsider. Isn't it lovely down here. I come down every night. Have done for —
[portrait: GUTTER, neutral] (the smile not moving) — for a long time. Longer than the Barons. Longer than the Sump. I was the first, you know. The first one it asked.
[portrait: GUTTER, happy] It only wanted company. We all only wanted company.
(Behind her, deeper in the crystal, something in a peach-coloured shell, with chains for hair, turns round. It's smiling too.)
V139 = 1.
```
*(Mother Gutter in Ch17 is lucid by day. She's the Moon Market's oldest Baron. Every night she has gone down to the Deep for centuries; Pecharunt's sweetness is why she's lived so long. Ch17's "Mother Gutter's Ledger" quest foreshadows the dates.)*

### **Boss: Pecharunt** (touch, the shell, V139 == 1 → 2; key event 1)
```
BATTLE: Prismfall::Bosses.wild_battle(:PECHARUNT_DEEP) — Lv 77; bars Casual 2 / Standard 3 / Hard 4; `:DARK_CRYSTAL`, then `:NEW_MOON` at bar 2.
(LOSE: whiteout to Underveil's Center; the boss restarts at bar 1.)
```
*(The boss's own lines: "The pink crystals gutter out one by one..." at bar 2; "\"Mochi, mochi...\" The chant falters in the dark." at bar 3; and at the end, "All through the Deep, the thralls blink, and stop smiling, and start to cry.")*
```
(The chains come apart. The shell tumbles into a crack in the crystal and is gone, down, somewhere even deeper. The pink light goes out.)
(In the dark, the sound of watering-cans being put down. Then people crying, quietly, the way you cry when you wake up from a good dream into a bad week.)
(Mother Gutter is sitting on the cave floor with her ledger in her lap. In the light of your lamp, she looks very, very old.)
[portrait: GUTTER, sad] ...Three hundred and eleven years. It says so here. I wrote it down every night. I never read it back.
[portrait: GUTTER, neutral] (closing the ledger) Help me up, topsider. I've got a Market to run. For however long that is now.
Switch S150 CH18_PECHARUNT_DONE = ON. V139 = 2.
```
**The old story turns over** (a mural in the Deep, lit by the PC's lamp after the fight; plain story text):
*(Scratched into the crystal wall, very old: a shell with chains, and three beasts on chains walking away from it towards a forest. Then the three beasts running back, and in the forest behind them a little masked figure with a club.)*
[if OGERPON_TRUSTED] *(Ogerpon, waiting at the Deep's mouth when you come out, looks at the mural for a long time. Then it turns and walks south, and looks back to see if you're coming.)*

*(The pageants have had it backwards for 250 years: the Loyal Three were the thieves, and the "Gossamer Ogre" drove them off (Ch10). `OGERPON_TRUSTED`: Ogerpon walks with the PC as a follower to Gloaming (S223). It's never in the party.)*

- **Hangout, Corvin at the Deep's mouth** (`CORVIN_FREED`; from V139 >= 2): *Rounds.* He treats the waking thralls one at a time. He talks about everything except Wenlow, until the last visit, when he says one sentence about him. **Else, Mother Gutter on the Moon Market steps**: *the Ledger*, three hundred years of Nadir read back for the first time.
- **`NA_SWEETROT`** opens (as catalogued; reward **Poltchageist**, Lv 72).

## Optional: Map 848 — the Inverted Ward (`:INVERSE`)
An abandoned Choir hospital turned upside down by the thinning Glass. Beds hang from the floor, which is the ceiling. Lamps burn downwards.
- A Choir nurse's echo, doing rounds on the ceiling: "Cantor Ines, bed nine. Throat. She'll sing again. They always say that."
- **Glassfall Sliver** on the ceiling, which is the floor.

Trainers (Lv 76): a nurse, a psychic.

*(The Choir's hospital, where Ines was treated before AF 290. One line only. The PC can stand under bed nine for as long as they like.)*

## Map 850 — Mothwell
A lantern-moth hamlet where the Blind Road comes up into the Gloamwood. Moths the size of hands. A lantern-pool, a spring lit from below by Morelull: **Morelull "Lamp"** (static, Lv 74, Effect Spore), the brightest of them, and **Glassfall Sliver** under the brightest light.

Trainers (Lv 76): a bug catcher, a lass.

## Map 841 — the Gloamwood Verge: **"by royal order"** (autorun at the checkpoint, V139 == 2 → 3)
```
(The Gloamwood Verge. Meridian survey-flags on every third tree. A Thornguard checkpoint across the road: a barrier of woven thorn, lanterns, a dozen guards in green, a captain with a writ.)
[name: Thornguard Captain] Halt. By royal order of His Highness Prince Caedmon, under the Forest Compact, the Gloamwood is closed to Festival traffic. Turn back.
(It's noon. It's dusk. The dusk has come this far west.)
[name: Thornguard Captain] I said turn back. Don't make me prove it.
BATTLE: TrainerBattle.start(:THORNGUARD, "Captain Rowe") — single; `:FAIRY_TALE` (the dusk); Lv 77.
(WIN:)
[name: Thornguard Captain] (whistling up a second squad) Fine. Then twelve of us.
(From the dusk behind the checkpoint, someone walks through the thorn barrier as if it weren't there: a tall woman in a gown of moth-wing grey, crowned with dusk-flowers. The old woman from Briarwick's shrine, a long time ago, except she isn't old now, and she isn't pretending.)
[portrait: CELESTINE, neutral] Captain.
[portrait: CELESTINE, neutral] If you stop this child, the forest will remember your name, and it will say it wrong forever.
(Every guard at the checkpoint knows she can't lie. They also know what that means. The captain steps aside. The thorn barrier unweaves itself.)
[portrait: CELESTINE, happy] (to you, warmly) We've met. You were very rude about my soup. You were right, it was terrible. Come along. Gloaming's waited forty years; it can wait for you to walk.
[portrait: CELESTINE, neutral] One rule. In Gloaming, always ask what it costs *before* you say yes. Always. Even me.
V139 = 3.
```
*(Celestine's warning foreshadows `GO_FAIR_BARGAIN`. The Ch3 meeting is the Briarwick shrine.)*

Trainers on the Verge (Lv 77): a Thornguard, a Meridian surveyor.

## Gloaming (440): **arrival** (V139 == 3 → 4)
Elowen's oldest corner, in endless twilight. Lantern-moths. Houses grown, not built. Dusk-chapels where the whole Hymn is still sung.
- **Deserters from both armies** (14_WAR_AND_BLESSING, Ch18 row): they've walked the length of Velmora to the one town where nobody can lie to them. They can't lie here either, so they tell the truth about why they ran.
  - An Isenmar harpooner: "I ran because I liked it. The first one. I liked it. I'm not going back to find out if I'd like the second."
  - An Ashkaar dragon-rider: "My dragon wouldn't fly at children. I'm not braver than my dragon."
- **Gift: Hatenna "Hush"** (Lv 50, Magic Bounce), from an Ashkaar deserter: "She feels what people feel. In the camp, she screamed for a week. Here she's quiet. Take her somewhere quieter still. Is there anywhere?"
- **Kestrel is already here.** His Directorate skiff docked at dawn. He's in the bakery's corner booth with Juno, saying nothing and eating.
  - **Comedy scene Ch18, "Phrasing"** (15_COMEDY as written) is available at the bakery V139 4–5. Juno came south to shout at Prince Caedmon about the Compact: "He's my *cousin*. He's my cousin and an *idiot*."
  - Kestrel won't talk to the PC here ("Not here. At the roots. After."). That's the whole of it until K7.
- **Hangout, Juno at the bakery** (V139 4–8): *Dusk-Honey Cakes.* She gets a little better each visit. Celestine's verdicts get more carefully phrased.

### Optional: **Queen Maelis** (the dusk-garden, under polite guard)
```
[portrait: MAELIS, neutral] (pruning a rose that's been dusk for forty years) My son thinks the forest is a resource. I've been queen for sixty years. The forest is the *sovereign*. I'm just the gardener it tolerates.
[portrait: MAELIS, smug] He thinks I'm resting. I am. I'm resting the way a bow rests when it's strung.
[portrait: MAELIS, neutral] Take this. It opens the Wardguard's escort to Crownhaven, whatever the Accord thinks of you. When I disown his Compact, I want it known that I'd already chosen a side.
RECEIVE: ROYAL WRIT (Key Item).
```
*(Seeds Elowen's epilogue: Maelis disowns the Compact.)*

### ☠ **`GO_FAIR_BARGAIN` "Fair Bargain"** (the lantern-moth market)
```
(A stall of glass jars, a lantern-moth in each, glowing. The vendor is a woman with moth-wing eyelashes who never blinks.)
[name: Vendor] For you? Something special. The answer to your mother's last question.
(Your mother's letter. The last line. You've reread it a hundred times. "Did I do right by you?")
> Buy it.
  [name: Vendor] (holding out a jar) Lovely. No need to ask the price. You'll pay it either way.
  > Take the jar.  Script: Prismfall.game_over(:GO_FAIR_BARGAIN)
  > Ask the price first.
    [name: Vendor] (pouting) Oh, you've been talking to *her*. Your name, sweetheart. Just your name. ...No? Then no.
> Ask what it costs.
  (as above, "Your name". No.)
> Walk on.
```
*(NARRATIVE_KEYS §9 epitaph: "The price was your name. You are very happy now, as a lantern-moth, and you will glow at every dusk." Ines's last letter is the Prologue key item.)*

## The envoys: **`:war_legend`** (autorun at Gloaming's dusk-chapel steps, V139 == 4 → 5)
```
(Two people are waiting on the chapel steps, as far apart as the steps allow: a skald of Isenmar in whale-bone and furs, and an Ember-Captain of Ashkaar in dragon-scale. They've walked here separately. They've been watching each other for two days.)
[name: Hallgerd (skald)] Unimprinted. The Thane asks. The sea-beast sleeps in the Ice Vault under Lake Rime, where your Primal waking left it. Calm it for us, so it follows our horns east to the front, and the war ends in a morning.
[name: Tavi (Ember-Captain)] The Dominar asks. The white dragon sleeps in the Wyrmscar. Speak the oath with Sigrun early and wake it, and it will burn the sea back off our dunes, and the war ends in a morning.
(They can't lie. Not here. They both mean it. They both know what the other one's legend will do to their people.)
[name: Hallgerd] (to Tavi, the first thing she's said to her) A legend on the sands calls its opposite. You know the old song.
[name: Tavi] I know the old song. I asked anyway.
```
```
> Calm Kyogre (Isenmar's ask). (calm_kyogre)
  Script: pf_choose(:war_legend, :calm_kyogre)
  [name: Hallgerd] Then the sea comes east, gently. As gently as a sea can.
  [name: Tavi] (not angry, just tired) And the white one will answer it. Remember I said that.
> Wake Reshiram (Ashkaar's ask). (wake_reshiram)
  Script: pf_choose(:war_legend, :wake_reshiram)
  [name: Tavi] Then the fire comes west.
  [name: Hallgerd] And the sea will answer it. You've chosen both, Unimprinted. You just said one name.
> Neither. (neither)
  Script: pf_choose(:war_legend, :neither)
  (Both of them look at you. Then, for the first time, at each other.)
  [name: Hallgerd] ...Then we fight it with what we have.
  [name: Tavi] Which is each other. (A long pause.) That's the most honest thing anyone's said on these steps in a week.
V139 = 5.
```
*(14_WAR_AND_BLESSING War 4: `:calm_kyogre` RES+2 MARISOL−1; `:wake_reshiram` SIGRUN+1 RES−2; `:neither` keeps both legends off the Glass Dunes. Either of the first two puts both legends at the Ch19 climax.)*

## Gym 17 — the Storybook Gym (450–455, `:FAIRY_TALE`)
As GYM_PUZZLES Gym 17:
| Map | Room | Role |
|---|---|---|
| 450 | Prologue Page | teach |
| 451 | the Red Path | twist |
| 452 | Midnight Ballroom | combine |
| 453 | the Eight Princesses | gauntlet |
| 454 | the arena | — |
| 455 | the Ninth Door | Mastery, optional |

Gym trainers: the 8 princesses, plus a Lady and a Beauty (Lv 76–79).

### 454 — the Warden Arena (double: "the knight and the dragon")
```
[portrait: CELESTINE, neutral] Once upon a time — which is the only time there ever is, here —
[portrait: CELESTINE, happy] My dusk-chapels still sing the whole song: every verse the rest of Velmora stopped singing. They sang over a sliver of glass for me, a year of dusks, until it knew my little ghost by heart.
[portrait: CELESTINE, smug] Every story needs one true thing in a borrowed costume. Mine is wearing yellow.
BATTLE: Prismfall.gym_battle(17, double: true)
```
- **When the Z-move fires (Mimikyu, Let's Snuggle Forever):** "This is the part where it hugs you. Hold still. It's worse if you don't." `[bubble: CELESTINE, happy, sparkle]`
- **Win:**
```
[portrait: CELESTINE, happy] And they lived. That's the end of the sentence. It's a better ending than most people get.
RECEIVE: the DUSK BADGE (badge 17). RECEIVE: TM21 DAZZLING GLEAM.
V139 = 6.
```
*(The badge name is proposed: the **Dusk Badge**. The VS plate reads OATHBOUND above CELESTINE. Her one power play is a Z-move, not a Mega (SPINE Rev 23).)*

## The dusk-chapel at the Great Tree's roots: **the Hymn of Return** (touch, Celestine at the altar, V139 == 6 → 7; key event 2, first half)
```
(The dusk-chapel, grown inside the Great Tree's roots. A choir of Gloaming folk in moth-grey, thirty of them, children at the front. Lantern-moths on every root.)
[portrait: CELESTINE, neutral] I've been waiting for you for forty years, little colourless thing. Listen. They don't sing it for anyone else.
(The choir sings. The whole Hymn. Every verse.)
```
*Eighteen we borrowed, eighteen we keep*
*till the wounded land has learned to sleep;*
*then one of no color, the eighteen roads walked,*
*shall carry them home, as the old ones talked —*
*not chained, not broken, not bought, not crowned:*
*given back, as a gift is found.*
```
[if has MAREN'S HYMN PAGE || HOLLOW_SANCTUARY_OPEN]
  (In your Bag, the page Brann gave you, or Wick's scrawled verse, warms. Under your eyes the last line writes itself in, in a cramped old hand: "given back, as a gift is found.")
[portrait: CELESTINE, neutral] Valen reads "one of no color" as *vessel*. The Hollow read it as *hammer*. Meridian reads it as *key*.
[portrait: CELESTINE, neutral] It says *walker*.
[portrait: CELESTINE, smug] I cannot lie. I can, however, sing. These are the verses I sing.
RECEIVE: THE HYMN OF RETURN (Key Item; complete).
Switch S151 CH18_HYMN_GOT = ON. V139 = 7.
```
*(On the Ruin Route, Celestine admits there's a verse she stopped singing (12_RUIN_ROUTE). Here, her phrasing is exact: "These are the verses I sing." Wick teaches the missing verse on Ch10's Hollow Sanctuary branch, so S171 HOLLOW_SANCTUARY_OPEN stands for "has Wick's verse".)*

## The Great Tree's roots: **K7** (autorun as the PC leaves the chapel, V139 == 7 → 8; key event 2, second half)
```
(Outside, under the roots, in the dusk. Kestrel. His sponsor jacket open, eighteen badges on the lining like medals. Aegislash's ball in his hand. He's not eating now.)
[portrait: KESTREL, neutral] They all want to use you. Valen wants a lock. Voss wants a key. Your Hollow friends want a crowbar.
[portrait: KESTREL, angry] Stay out of Crownhaven and let me end it. I'll beat Valen in front of the whole world and make him say her name.
[portrait: KESTREL, neutral] In stories there's a knight and a dragon. I'm the knight. (He points the ball at you.) Guess.
BATTLE: Prismfall.rival_battle(:RIVAL_KESTREL, "Kestrel", 7, field: :FAIRY_TALE)
(LOSE: the rival rule: the story continues, and his line below becomes "Stay down. Please. For once in your life, stay down.")
```
- **The flinch** (at `bond(:KESTREL) >= 3`; on the turn his ace enters): Kestrel hesitates. He loses his first move that turn ("Kestrel hesitated!"). `[bubble: KESTREL, sad]` "...Stop looking at me like she did."
- **On his ace, Aegislash "Morwen":** "Knights are supposed to win. That's the deal. That's the whole deal."

**After K7: Morwen's Ring** (`:ch18_kestrel_ring`; only if the PC has MORWEN'S RING)
```
(He's sitting on a root with his back to you, his Pokémon recalled.)
> Give him Morwen's Ring now. (give_now)
  Script: pf_choose(:ch18_kestrel_ring, :give_now)
  (You hold it out: black glass and silver, the same colourless chip as yours, very faint.)
  \pf[PLAYER,neutral] (Your fifth authored line.) Edda kept it. Ten years. She said give it to you when you'd not throw it in the sea.
  (He looks at it for a long time. He doesn't say thank you. He puts it on. It fits.)
  (He turns his hand over and looks at the chip. It doesn't sing. Not yet.)
> Keep it for now. (keep)
  Script: pf_choose(:ch18_kestrel_ring, :keep)
  (You keep your hand in your pocket, round the ring. Not yet. Not here.)
```
*(NARRATIVE_KEYS: `:give_now` KESTREL+3 YSOLDE+2; the ring answers him at the semifinal, as his Scizor's first Mega (K8). `:keep` means it can be given at the semifinal for a bigger moment if he's Redeemed. Without MORWEN'S RING, skip the choice.)*

### ☠ **`GO_STAY_OUT` "Somebody Else's Story"**
```
[portrait: KESTREL, neutral] (standing) Last chance. Stay out of Crownhaven?
> Yes.
  [portrait: KESTREL, sad] (he looks at you as if he can't believe it worked) ...Okay. Okay. Good. Thank you.
  (He walks away into the dusk. You let him.)
  Script: Prismfall.game_over(:GO_STAY_OUT)
> No.
  [portrait: KESTREL, angry] Don't come. I mean it.
  [portrait: KESTREL, neutral] (a long breath) ...You're going to come. Fine. Then don't lose before you reach me.
Switch S152 CH18_K7_DONE = ON. Variable V114 KESTREL_STAGE = 4. V139 = 8.
```
*(The epitaph is in NARRATIVE_KEYS §9. The PC does what everyone has told them since the ferry, and the Engine takes Kestrel instead.)*

## Chapter close (autorun at Gloaming's south gate, V139 == 8 → 9)
```
(Gloaming's south gate. Dawn that isn't dawn: the dusk lifting a little, the way it does at the edge of the town. Kestrel's skiff going up off the dock, north, towards Crownhaven.)
[if OGERPON_TRUSTED] (Ogerpon sits down at the gate. It won't go further. It looks at you, then south-west, towards the Thornwar Marches and the dragons' country, then back at the Great Tree. Then it goes home.)
[portrait: CELESTINE, neutral] (at the gate, holding a lantern) One badge left, little walker. Sigrun's. She's the only Warden in Velmora who's harder to talk to than me.
[portrait: CELESTINE, neutral] I can't come with you. Gloaming is the only place I'm true. Everywhere else, I'm just old.
V139 = 9. Variable V102 STORY_CHAPTER = 19.
QUEST LOG: "Eighteen Roads" — South-west through the Thornwar Marches to Wyrmrest. Gym 18. Then Crownhaven.
```
*(Ch19 opens on the Gloamwood road into the Thornwar Marches.)*

## Optional: **"Dreamwalker"** (CAMEOS §7; Gloaming's dusk-chapels, after Gym 17)
As in CAMEOS §7. Shiv: "Met you already. You were standing on a ferry, glowing like a lighthouse." Three dream-errands for the townsfolk:
1. return a lost name;
2. finish a dead man's sentence;
3. find a child's Pokémon in a dream that isn't hers.

Then a battle with Shiv (CAMEOS team; Ambipom ace).

---

## Map events needed (Chapter 18)

None of this chapter's maps is built. **[NEW]** = an event or map not in maps.json. V139 = **CH18_STEP** (design/FLAGS.md). Maps go through the three-pass workflow (design/MAPGEN.md, top).

**852 The Throat** (`:NEW_MOON`):
- the lamp radius (darkness overlay);
- Corvin at the gate (`CORVIN_FREED`) or Wenlow's satchel and note;
- the echo-ledge (**Sliver #1**);
- 2 trainers.

**840 The Blindwater** (`:CAVE`):
- the black lake (Surf), the dry island (**Sliver #2**);
- 3 trainers.

**844/845 The Lightless Deep** (`:DARK_CRYSTAL` / `:NEW_MOON`):
- pink crystal (glow tiles);
- peach growths on vines;
- 20+ thrall events tending (looping move routes, the watering-can SE);
- **Mother Gutter** (V139 0 → 1);
- **Pecharunt** (`:PECHARUNT_DEEP`; S150; V139 1 → 2);
- after the fight: the light-out tone, thralls sitting and crying (event swaps);
- the mural (interact);
- Ogerpon at the mouth (`OGERPON_TRUSTED`; becomes a follower);
- Corvin's hangout at the mouth.

**848 Inverted Ward** (`:INVERSE`):
- upside-down hospital (ceiling beds);
- the nurse echo;
- bed nine;
- **Sliver #3**;
- 2 trainers.

**850 Mothwell:**
- the lantern-pool (**Morelull "Lamp"** static; **Sliver #4**);
- 2 trainers.

**841 Gloamwood Verge:**
- survey-flags on the trees;
- **the Thornguard checkpoint** (barrier event; Captain Rowe battle; Celestine's entrance through the barrier; the barrier unweaving: event fade; V139 2 → 3);
- 2 trainers.

**440 Gloaming** (`:FAIRY_TALE`, permanent dusk tone):
- grown houses;
- the deserters (2 truth-lines);
- **Hatenna "Hush"** gift;
- the bakery (Juno and Kestrel; "Phrasing"; Juno's hangout);
- **the lantern-moth market** (`GO_FAIR_BARGAIN` stall);
- **Maelis's dusk-garden** (ROYAL WRIT);
- **the chapel steps** (the envoys, `:war_legend`, V139 4 → 5);
- the south gate (the close, V139 8 → 9).

**450–455 Gym 17:** as GYM_PUZZLES; the 8 princesses, Lady and Beauty; Celestine double (454); V139 = 6.

**443 Great Tree Roots / the dusk-chapel:**
- the choir (30 events);
- the Hymn (S151; the Key Item completing);
- Celestine's hangout;
- **K7** under the roots (V139 7 → 8);
- `:ch18_kestrel_ring`;
- `GO_STAY_OUT`;
- the root-knot (**Sliver #5**);
- the Shiv cameo (dream overlays).

## Trainer roster (Ch18; regular trainers outside the gym; PBS blocks in 3 versions; ≤ 80)
| Map | Class (stock type) | Name | Lv | Team idea (field touch) |
|---|---|---|---|---|
| 852 | Punk *(Guitarist)* | Sallow-the-younger *(no relation)* | 75 | Skuntank, Overqwil, Grimmsnarl |
| 852 | Hex Maniac | Morwenna | 75 | Gengar, Polteageist, Ceruledge |
| 840 | Fisherman | Blind Tam | 75 | Lanturn, Quagsire, Seismitoad (Cave: echo boosts Sound) |
| 840 | Ruin Maniac | Pell-the-Younger | 76 | Golurk, Claydol, Gigalith |
| 840 | Black Belt | Master Oyuki | 76 | Lucario, Conkeldurr, Hitmontop |
| 848 | Nurse *(Lady)* | Sister Ama | 76 | Blissey, Hatterene, Indeedee (Inverse: Normal is weak here) |
| 848 | Psychic | Ottilie | 76 | Gardevoir, Espathra, Bronzong |
| 850 | Bug Catcher | Lantern-boy Fen | 76 | Volcarona, Frosmoth, Vikavolt |
| 850 | Lass | Posy | 76 | Comfey, Florges, Whimsicott |
| 841 | Thornguard *(Ace Trainer)* | Thornguard Ilsabet | 77 | Tsareena, Rillaboom, Decidueye |
| 841 | Meridian Surveyor *(Scientist)* | Surveyor Gant | 77 | Magnezone, Klinklang, Ferrothorn |
| **Gym 17** | 8 princesses + Lady + Beauty | (GYM_PUZZLES) | 76–79 | as GYM_PUZZLES |

**Story fights:**
- `THORNGUARD` Captain Rowe: a **new trainer type, "Thornguard"**. Lv 77: Rillaboom, Tsareena, Trevenant.
- K7 and Gym 17: existing PBS.
- **Boss:** `:PECHARUNT_DEEP` (109_Boss_Pecharunt.rb; `:catch => false`).

**Items owner:**
- **Key Items:** THE HYMN OF RETURN, ROYAL WRIT.
- **Badge and TM:** the DUSK BADGE (proposed), TM21.
- **Slivers:** Glassfall Slivers #1–5 of the Ch18 allotment.
- **Gym 17 Mastery:** Magical Seed ×2, Fairy Feather, and a Hymn page.

**EventMons:** Hatenna "Hush" (gift, Lv 50), Morelull "Lamp" (static, Lv 74), Poltchageist (`NA_SWEETROT`).

**Portrait requests (art, to Gemini):** **MOTHER GUTTER** `sad` (old), **MAELIS** (`neutral`, `smug`), **CELESTINE** in her true form (`neutral`, `happy`, `smug`), Shiv (cameo).
