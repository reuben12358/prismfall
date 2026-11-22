# Script: Chapter 11 — "The Thaw" (the Hart Road, Rimeholt, Gym 10, the Thaw and Kyogre; the war; the Ebbmouth Strike; the Mast Road)

> **Final playable script** for Chapter 11, the second chapter of Act III. It covers the Hart Road (700 the Hart's Run, 701 the Hoarwood, 710/711 Snowbriar, optional 703 the Gossamer Heartwood, 704/705 Frostfang Pass, 712 the Whalebone Road), Rimeholt (300–314: the Thane's Harbour, the Icewall Gate, the Sled Market, Whalebone Keep, Net Row and the Sinking Quarter), the Lake Hall (Gym 10, 310–313, 315–316), the Thaw and Kyogre, the court in the Thane's Seat (307), the detour south to Ebbmouth (160, 167; optional 723), and the Mast Road out (720 the Thane's Sled-Road, 721 the Mast Glacier, 730/731 Anchorhold; optional 728 Stillwater). None of these maps is built; the list at the end is what to build from.
> Follows `story/28_SCRIPT_CH10.md`; `story/31_SCRIPT_CH12.md` ("Dead Letters") follows this (its opening reads S128, V107, V122 = 2 and `:ch11_anja`). Sources: 06_ACT_III Ch11, 14_WAR_AND_BLESSING (the Ch11 insert; War 1 `:war_warning`), 03_CAST (Anja, Eirik, Juno, Marisol, Teo, Voss), 09_MYSTERIES (#21 the sleepers dream; #22 Kyogre and the Sleeping Whale), NARRATIVE_KEYS (`:war_warning`, `:ch11_anja`, `:ch11_strike`, GO_WEATHER, GO_THIN_ICE, `JUNO_ESTRANGED`, `ANJA_EXPOSED`), 15_COMEDY (Ch11 "Toes"; the Isenmar bits; the Wardens' Circular), GYM_PUZZLES Gym 10, DUNGEON_PUZZLES (the Ice Vault ties), BOSSES (`:KYOGRE_ISENMAR`, `KYOGRE_WEATHER`), TRIALS_QUESTS and WALKTHROUGH Ch11 (the Tally quests), CAMEOS #5 (Alexandra), `design/CHAPTER_BEATS.md`.

## Conventions
As in the earlier scripts. **Portrait cast here:** Juno, Anja, Eirik, Marisol, Teo, Voss (on screens only), Valen (one line, by relay), Larch (the banner only, no portrait). **Plain:** the Meridian technician Pell, the Directorate officers, the strikebreakers and their foreman, the pass-warden Bryn, the Ashkaar rider, Old Torstein, Liv (Anja's granddaughter), the ice-climbers, the ice-fisher, the skalds, the net-menders, Alexandra (cameo), every townsperson and trainer. Kyogre is a Pokémon: staging only. Events call `Prismfall.gym_battle(pfm_gym(:LEADER_ANJA), double: false)`: Gym 10 is a **single** battle.
**Counter:** V132 **CH11_STEP** (design/FLAGS.md): 0 leaving Verdance · 1 `:war_warning` made on Frostfang Pass · 2 through Rimeholt's Icewall Gate · 3 "Toes" (Anja meets Juno; the gym opens) · 4 Gym 10 won · 5 the Thaw (S128, V107 = 1; the partner battle) · 6 Kyogre (S129) · 7 `:ch11_anja` made in the Thane's Seat · 8 the third day: war declared (V122 = 2), the column leaves · 9 the Ebbmouth Strike (S130, V108 = 3) · 10 Anchorhold, "LARCH SPEAKS TONIGHT" (chapter closed; V102 = 12).
**State set here:** S128 CH11_THAW, S129 CH11_KYOGRE_DONE, S130 CH11_EBB_STRIKE, V107 RIMEHOLT_STATE = 1, V108 EBB_STATE = 3, V122 WAR_STATE = 2, S174 DOCTORS_CELL_QUEST (the hook only). Keys: `:war_warning`, `:ch11_anja`, `:ch11_strike`.

## The chapter's key events (design/CHAPTER_BEATS.md)
1. **The Thaw.** Rimeholt's heat-towers overdraw (the passes are closed, so they run the local Lattice past its limit), the lake breaks under the lower town, a quarter of the city goes under, and Kyogre wakes. Build-up: the Ch8 manifest ("destination *Rimeholt*"), the grey ice under the towers, the fishers' holes that don't refreeze, the Sleeping Whale song sung too often, Anja's "When the lake breathes, you run", and Gym 10's cracking tiles. Payoff: the ice going out from under the lamps, the partner battle as the field gives way, the eye under the water. Consequence: V107 for the rest of the game (the Sinking Quarter, the refugees in Ch14, the Ice Vault's meltwater channels), Anja's Act V vote, `:war_legend` in Ch17–18.
2. **War is declared.** Kyogre's Primal rain rolls east for three days and floods the Dominar's forward camps on Ossaria's western dunes. On the third morning every screen in Isenmar carries it: war. Build-up: Ch8's closed passes, Ch9's near-brawl at the Conclave, `:war_warning` from the top of Frostfang Pass. Payoff: the Thane's host leaving east along the Sled-Road while the evacuation column goes south. Consequence: V122 = 2, Isenmar's refugees in Elowen and Ossaria, the Siege of Skaldfast (Ch15), the war choices.
Also: `:ch11_anja` (expose her, or let her confess), and `:ch11_strike` at the Ebbmouth picket. **No jokes** from the first red reading on Pell's console (V132 == 4, at night) to Anja on the hut roof (15_COMEDY §1: the Thaw is joke-free). **No side content** opens in Rimeholt between Gym 10 (V132 == 4) and the court (V132 == 7): the Tally board, the ice-climbers' wall and Torstein's hole all wait until the morning after.

---

# CHAPTER 11 — "The Thaw"

**Chapter start:** V101 = 3, V102 = 11, V132 = 0 ("Dear Uncle Rowan" closed Ch10). The PC wakes in the Verdance Pokémon Center (281).
**Juno's two modes** (NARRATIVE_KEYS `JUNO_ESTRANGED` = `bond(:JUNO) <= -5`): normally she **travels with the PC** as a follower (`PrismfallMaps` Juno follower, leg `:hart_road`) from 284 to Rimeholt. If estranged, she has gone ahead alone by sled; every Juno line on the road is cut, the "Toes" scene still plays (she is already in Rimeholt), and **Anja** is the PC's partner in the Thaw. Lines marked `[estranged]` replace the default.

## Map 281 — the Verdance Pokémon Center: **"Walking Papers"** (autorun on waking, V132 == 0)
```
(Morning. The Center's window is full of white flowers: the little path from the potting shed reaches all the way across the Heartgarden now, and somebody has put a rope round it so the tourists don't step on it.)
(Juno is at the counter in a travelling coat over her Warden's sash, with a satchel so full it won't close. Her wreath is on top, in a hatbox. She is reading from a sheaf of paper under her breath.)
[portrait: JUNO, panic] "—the Greenward bloc believes that sustainable Imprint stewardship is—" no. "—believes in—" no. Hi. Morning. Hi.
[portrait: JUNO, neutral] I'm going north. The northern Wardens haven't answered a single letter, so I'm going to stand in their halls till they do. Anja Sorrel first. Rimeholt.
[portrait: JUNO, sad] She signed the heat contract. Her whole city runs on Meridian. If the Greenward can't talk to her, it can't talk to anybody.
[portrait: JUNO, happy] And your tenth badge is up there. So. Same road. If you want. You don't have to.
(She is already holding the door.)
[estranged] (Juno isn't here. On the counter there's a note in green ink, very short.)
[estranged] "Gone ahead to Rimeholt by the mail-sled. Don't wait for me. — J."
[estranged] [name: Nurse] She asked me if you'd slept well. Then she said not to tell you she asked.
V132 stays 0. QUEST LOG: "Eighteen Roads" — North up the Hart Road to Rimeholt, Isenmar's capital on the frozen lake.
```
*(Ch10's close set up this exit. The Ogre, if S223, sees them off at the Kingsgate and goes back to the Bride Tree.)*

## Map 284 — the Kingsgate Barbican (touch, once, on leaving north)
```
(The Thornguard on the north gate are new: twice as many as yesterday, with a sergeant who checks every pass twice.)
[name: Thornguard Sergeant] Isenmar? Hm. Her Majesty's compliments, Warden, and the border's open. For now. The Thane's been asking about grazing rights on our side of the Hart's Run, if he has to "move people". Move what people, I said. He didn't say.
[portrait: JUNO, neutral] (outside the gate, quietly) Move people. Why would you need to move people?
```
*(The first seed of the evacuation and the Thornguard border crisis. Cut if estranged; the sergeant says it to the PC alone.)*

## Map 700 — The Hart's Run (`:MEADOW`)
Road sign: "THE HART'S RUN. North to the Hoarwood and Isenmar. The Crown's deer have the right of way."
```
(Wide downs going pale with frost toward the north. Juno walks backwards in front of your lead Pokémon, holding her papers up.)
[portrait: JUNO, happy] Right. You're the Thane. Be the Thane. Look kingly.
(Your lead Pokémon looks at her.)
[portrait: JUNO, neutral] "Your Majesty. The Greenward bloc proposes that no Plate should be drawn past the point where its land can—" Do you think "drawn" sounds rude? It sounds rude. "—tapped"? "Milked"?
(Your Pokémon sits down.)
[portrait: JUNO, sad] That's what the Thane will do as well, isn't it.
```
*(One running gag this chapter: Juno practises on the PC's Pokémon at three spots on the road (700, 710, 712), each speech a little better. Joke-light, before the blow; 15_COMEDY §1 allows it. Cut if estranged.)*
Trainers (Lv 45–48): a deer-herd (Stantler, Sawsbuck), a Crown huntsman, two hikers. **Optional:** the deer-herd: "The white stag's been seen up in the Hoarwood. Crown says it's the Queen's. Trappers say it's nobody's. Stag says nothing, which is the most sensible position." (IS_WHITE_STAG starts at 710.)

## Map 701 — The Hoarwood (`:SNOWY_MOUNTAIN`, borderland A2) and **Map 710/711 — Snowbriar**
```
(The first snow. Juno stops in the middle of the road and holds her hand out.)
[portrait: JUNO, happy] Oh. Oh, it's— I've never— Verdance doesn't— It's COLD. Why didn't anyone tell me it was this cold? You told me. You told me twice. I know.
(The blossoms in her hair close up against the cold, one by one, like hands.)
```
**Snowbriar** (the lodge-town in the Hoarwood):
- The lodge-keeper: "Meridian's heaters? Not up here. We burn wood, like people. The wood doesn't send you a bill with a seal on it." (IS_WHITE_STAG giver.)
- A sledge-driver back from Rimeholt: "Ice under the harbour's grey as a gull. You can see the fish through it. You shouldn't be able to see the fish through it."
- The Wardens' Circular at the Center (281's board, here too): Odessa's post: "SKYREACH WEATHER: wind. FORECAST: wind. Mail's late because of the wind." Dorian replies: "*(Enter WIND, stage left.)*"
- **Juno's second speech** (at the lodge fire, to the PC's second Pokémon): "—so the bloc asks only that Isenmar's heat be drawn at a rate the lake can bear." (Your Pokémon nods off.) "That's better, right? It's shorter. Shorter's better."

## Map 703 — The Gossamer Heartwood (optional; `:SILKWOOD`; the Silkwood revisit)
As DUNGEON_PUZZLES "the forest is a loom" (7/10). Flavour only, no story beat. Juno, at the first silk curtain: "This is where you found the Matriarch's glass, isn't it. Everybody in Elowen tells that story wrong. I'd like to hear it right one day."

## Map 704/705 — Frostfang Pass: **"Those Aren't Caravans"** → **CHOICE `:war_warning`** (War 1; autorun at the watch-cairn on 705's summit, V132 == 0 → 1)
```
(The top of the pass. A cairn of black stones with a frozen flag on a pole, and a stone hut beside it with smoke from the chimney. The air is so clear it hurts.)
(North-east, beyond the Mast Glacier's white tongue, the land goes the colour of old bone: the sands. And along the horizon, very small, a line of thin grey threads going straight up. Twenty. Fifty. Too many to count.)
(Over them, high up, a slow ring of black specks, turning and turning, like a wheel of ash.)
[portrait: JUNO, neutral] Are those chimneys? There's no town out there. Larch's map says there's no town out there.
[portrait: JUNO, shocked] Those aren't caravans, are they.
(The hut door opens. A woman in a pass-warden's furs with a long brass glass under her arm. Bryn, the watch.)
[name: Bryn] Cookfires. Four days now. Dragons over them since yesterday. I've counted a hundred and sixty in that ring before the light went.
[name: Bryn] That's Ossarian sand, that. Western dunes. Kassan's land. Ashkaar's got no business on it unless somebody let them.
[name: Bryn] I sent it down the mountain. They sent back: "Thank you for your diligence. The Thane is aware of all troop movements." He isn't. Nobody is. You're the only two who've looked.
```
```
(Behind the cairn, out of the wind, sits a young man in a scorched leather coat, with a Flygon curled round him like a cat. His left wing-strap is cut. He was not expecting company.)
[name: Ashkaar Rider] Don't. Please. I'm not a spy. My Flygon threw a feather in the wind off the glacier and I came down where I could. I'll be gone when she can fly.
[name: Ashkaar Rider] (looking at the smoke) ...You saw them. Of course you did. Everyone can see them from here. That's why the Dominar said not to fly this way.
[portrait: JUNO, neutral] (to the PC, very low) I'm a Warden now. The Circular goes to every Warden and to the Sovereign. I could send it. Or you could tell her. Or him. Or... nobody.
```
```
> Tell Bryn to send it again, to the Thane's own hand. (warn_isenmar)
  Script: pf_choose(:war_warning, :warn_isenmar)
  [name: Bryn] To his hand. With a Warden's name on it, they'll have to open it. Right.
  (She writes it on the hut's slate, and then on paper, and gives it to her Corvisquire, who looks at the wind and sighs.)
  (The rider watches it go. He doesn't say anything. He puts his hand on his Flygon's neck.)
> Tell the rider to take word home: they've been seen. (warn_ashkaar)
  Script: pf_choose(:war_warning, :warn_ashkaar)
  [name: Ashkaar Rider] ...Seen. By an Isenmar watch, and a Warden of Elowen, and— you. He'll want to know that. He hates being seen before he's ready. It might make him wait.
  [name: Ashkaar Rider] Or it might make him hurry. I don't know which. I only carry things.
  [name: Bryn] (turning her back) I didn't hear any of that. I'm deaf on the east side. Always have been.
> Juno sends it on the Circular: every Warden, and the Sovereign. (warn_both)
  Script: pf_choose(:war_warning, :warn_both)
  (Juno kneels on the hut step and writes it on her knee, Warden's seal and all: what they saw, where, how many, and that Ashkaar's own rider is sitting on the mountain because his Flygon couldn't fly.)
  [portrait: JUNO, neutral] Everyone gets it. Isenmar. Ashkaar. The Sovereign. If anyone's going to start a war, they'll have to start it knowing everyone saw them come.
  (Hours later, at Snowbriar's Center or Rimeholt's, the Circular has one reply, in Valen's own hand:)
  [portrait: VALEN, neutral] Received, Warden Hale. Both crowns have it from me as well. Thank you for looking.
> Say nothing. (silent)
  Script: pf_choose(:war_warning, :silent)
  (You hand Bryn her glass back. Juno looks at you, and at the smoke, and doesn't send anything.)
  [portrait: JUNO, sad] It's not our war. Is it? It's not anyone's yet.
  (The rider gets up as soon as you've gone round the cairn. When you look back from the switchback, the Flygon is in the air, low and limping, heading east.)
V132 = 1.
[estranged] Bryn and the rider play the same; option 3 reads "Send it on the Wardens' Circular from the hut's relay" and the PC writes it, with Bryn's seal.
```
*(NARRATIVE_KEYS §4.3 War 1: `:warn_isenmar` MARISOL+2 SIGRUN−2, `:warn_ashkaar` SIGRUN+1 MARISOL−2, `:warn_both` ACCORD+2 SIGRUN+1 MARISOL+1 (counts toward War Trust), `:silent` RES−1. The consequence lines are in the Thane's hall after the Thaw (Map 307) and in the war declaration (Map 300, day three).)*
Trainers on 704/705 (Lv 47–50): a skier, an ice-climber pair (double), a pass-warden's apprentice, a monk of the Sleeping Whale. Wild per WALKTHROUGH.

## Map 712 — The Whalebone Road (`:SNOWY_MOUNTAIN`)
Road sign: "THE WHALEBONE ROAD. Rimeholt 2 leagues. Walk on the marked ice ONLY."
```
(The road comes down out of the mountains onto the lake. Not a lake: a sea, white to the horizon, with a city standing on it. Timber and whalebone, long halls with roofs like upturned boats, and in the middle of it, taller than anything, four slender steel towers with red lamps at the top, breathing steam.)
(Along the road, arches made of whale jaws, one every hundred paces.)
(At the third arch an old man is sitting on a sled, singing to nobody.)
OLD MAN (singing): "Sleep, old whale, under the white / Sleep while the Thane keeps the lamps alight / Wake when the ice remembers your name / Wake, and the sea will be yours again."
[name: Old Man] They used to sing that once a winter. At the long night. Now they sing it every night. Nobody says why. You don't say why about the whale.
```
**Juno's third speech** (to the PC's third Pokémon, under the last arch): "Your Majesty. Your sister's city is warm. I came to ask what it costs, and who pays." (Your Pokémon looks at her properly for the first time.) [portrait: JUNO, shocked] It listened. Did you see? It *listened*.
*(09 #22: the Sleeping Whale song is the note order for the Ice Vault's sealed door (DUNGEON_PUZZLES), and the player has heard it since Ebbmouth in Act I.)*

## Rimeholt (300–314; Isenmar's capital on Lake Rime, `:FROZEN_LAKE`)

### Map 303 — the Icewall Gate: arrival (autorun, V132 == 1 → 2)
```
(A wall of cut ice blocks as tall as a house, glittering. A gate of whale ribs. On the gate, a Meridian scanner arch, new brass on old bone.)
SE: the two-note chime.
SCREEN: ◆ PRIORITY GUEST ◆ Welcome to Rimeholt, \PN. Warmth is a right. Meridian Heat Services.
[name: Gate Skald] Mind the ice past the towers. It's thin. It's been thin since the summer. They say it's fine. They've got a machine that says it's fine.
(Inside the gate, the city. Sled-roads cut in the ice, children skating to school, fishing huts with smoking chimneys. And the four towers, each on its own platform of steel piles, with the ice round their feet grey and wet-looking, like old glass.)
(A fishing hole by the first tower is open, black water, and steaming. Nobody is fishing it.)
V132 = 2. QUEST LOG: "Eighteen Roads" — Find Warden Anja Sorrel. The Lake Hall is on the ice past the harbour.
```

### Map 300 — the Thane's Harbour: **"When the Lake Breathes"** (touch, the drill on the harbour ice, on the way to the Lake Hall; V132 == 2)
```
(A line of children in fur hoods stands on the harbour ice. A tall woman in a Mamoswine-hide coat walks down the line with an unlit pipe in her teeth, tapping each child on the hood.)
[portrait: ANJA, neutral] What do you do when the ice sings?
CHILDREN: Lie down flat!
[portrait: ANJA, neutral] What do you do when the ice cracks?
CHILDREN: Roll to the marker!
[portrait: ANJA, neutral] And what do you do when the lake breathes?
CHILDREN: RUN!
[portrait: ANJA, neutral] Run where?
CHILDREN: To the TOWERS!
[portrait: ANJA, smug] Good. You'll all live to be as ugly as me. Off to school.
(They scatter. She turns, and sees Juno, and her eyebrows, which have rime in them, go up very slowly.)
```
*(The drill is the set-up for the GO_WEATHER prompt. "When the lake breathes, you run" is said three more times this chapter: by Liv in the gym, by Anja after the badge, and by Anja at the moment itself.)*

### Map 300 — comedy scene Ch11, **"Toes"** (continues; V132 == 2 → 3)
```
[portrait: JUNO, happy] Warden Sorrel! I'm Juno Hale, Warden of Verdance, and the Greenward bloc believes that sustainable Imprint stewardship—
[portrait: ANJA, neutral] How many toes have you got, girl?
[portrait: JUNO, shocked] ...Ten?
[portrait: ANJA, neutral] Come back in February and tell me your policy.
[portrait: JUNO, panic] I had a second page!
[portrait: ANJA, smug] Read it to the fish. They've nowhere to be.
[portrait: ANJA, neutral] (to the PC) You're the badge-hunter. The one with no colour. I heard. Lake Hall's past the towers. Don't walk on the grey.
[portrait: ANJA, neutral] And you, Verdance. You want me to choose between my principles and my grandchildren's toes? Easy choice. Toes. Every time. The heaters stay on.
(She goes. Juno watches her go.)
[portrait: JUNO, sad] (to the PC) She's terrifying. I want her to like me so much.
[estranged] (Juno is already on the harbour ice with her papers when the PC arrives; the scene plays the same; afterwards she sees the PC, says "Oh. You came," and goes off toward the Keep without waiting.)
V132 = 3. The Lake Hall's doors open.
```
*(15_COMEDY Ch11 "Toes", placed as written: before the blow, never during. It also plants the chapter's argument: Anja's choice is real, and Juno doesn't have an answer to it yet.)*

### Map 300 — the Thane's Harbour · 301 PC · 302 Mart · 304 Sled Market · 314 Net Row (townsfolk, before the Thaw)
- **The heat-tower technician, Pell** (at the foot of the second tower, with a clipboard and a scarf knitted by somebody who loves him): "Tower Three's running at a hundred and twelve percent. It's fine. It's within tolerance. The tolerance was raised in the spring. Everything's within tolerance if you raise the tolerance." *(He is the technician of GO_THIN_ICE. Meeting him here first gives the player a face to say no to.)*
- **A fisher by an open hole:** "Thirty years I've cut holes. They close by morning. This one's been open since midsummer. Fish come up to look at me. Fish shouldn't be curious."
- **The Sled Market:** a sled-wright: "The Thane's buying every war-sled in the city. 'Just in case.' Just in case what, I said. He said 'just in case.'" A fur-trader from the Hoarwood: "Wood's dear this year. Nobody's buying it. Everyone's got the towers."
- **Net Row (314):** a net-mender: "My gran's house was on the harbour. Before the towers it was the coldest house in Rimeholt. Now it's the warmest, and it creaks at night like a ship."
- **Old Torstein** at his hole on the fishing flats (300): the Isenmar bit from 15_COMEDY §5, the Avalugg he's sitting on. He talks to the PC only about fish. (IS_ELEVEN_YEARS opens after the Thaw.)
- **The Center's Mandate arch** (301) and the Wardens' Circular: Marisol's post, a week old: "EBB GUILD VOTES TO STRIKE IF THE THANE'S LEVY COMES DOWN THE ROAD. If you're a Warden and you've got sleds, don't lend them to a war." Rook replies: "Rotom says hi." *(Seeds the Strike.)*

### Map 306 — Whalebone Keep, the Mead Hall: **Thane Eirik** (touch, once; optional before the gym, but it helps)
```
(A long hall like the inside of a ship, with a fire down the middle and whale jaws for rafters. At the end, a big tired man with a grey beard plaited in two, signing papers one after another without reading them.)
[portrait: EIRIK, neutral] Warden Hale's friend. Sit. Eat something. Everyone who comes in here wants a thing and nobody eats.
[portrait: EIRIK, neutral] I'll tell you what I tell all the southerners. Ten years ago a winter killed four hundred people in this city. Old people. Babies. I buried them on the ice because the ground was too hard to dig.
[portrait: EIRIK, neutral] Then Meridian came with the towers, and nobody has died of cold in Rimeholt in eight years. You can say what you like about Meridian. I will sign whatever they put in front of me, as long as nobody dies of cold.
[portrait: EIRIK, sad] (signing another paper) And now Ashkaar has closed the passes, and the forge-heat doesn't come up the pipe from Cindervault any more, so my towers run on the lake. Meridian says the lake can take it. My sister says the lake can take it. So the lake can take it.
```
*(The Ch8 manifest pays off here: Cindervault's tap fed Rimeholt; with the passes closed (V122 = 1) the towers draw on the lake's own Imprint. That's the mechanism of the Thaw, stated plainly before it happens. If V110 = 0 (`:shutdown` in Ch8) he adds: "And Cindervault shut its tap anyway. Somebody down there decided my city could do without. They were right, it turns out. We did without, by drinking the lake.")*

## Maps 310–313, 315–316 — the Lake Hall (Gym 10; GYM_PUZZLES Gym 10)
Doors open at V132 >= 3. Built as GYM_PUZZLES Gym 10 ("ice remembers weight"): 310 the Boathouse (teach), 311 the Ice Hall (twist), 312 the Crackwalk (combine), 313 the Warden Arena, 315 the Sounding (Mastery, optional), 316 the Under-ice Grotto (falls).
- **Gym sign:** "RIMEHOLT LAKE HALL. Warden: ANJA SORREL. 'Ice remembers.'"
- **Liv** (Anja's granddaughter, the hint apprentice in 311/312), on the first fall: "Gran says you get one go over each crack. She also says when the lake breathes you run. She says that about everything. She said it about my birthday."
- **The net-mender in 310** (on the optional Pearl line, second visit): "Told you. It remembers."

### 313 — the Warden Arena: Anja
```
(A round hall cut into the lake itself. Clear ice for a floor, and under it, very deep, dark shapes moving slowly.)
[portrait: ANJA, neutral] Ice remembers. Every crack. Every weight. You walk on my lake, it knows your name by spring.
[portrait: ANJA, neutral] Southerners think the ice is the enemy. It isn't. The ice is the only reason we're standing up. The water's the enemy. Always was.
[portrait: ANJA, smug] Show me how heavy you are.
BATTLE: Prismfall.gym_battle(pfm_gym(:LEADER_ANJA), double: false) — single; field `:FROZEN_LAKE` (cracks → `:WATER_SURFACE`; Mega Glalie seals the cracks once).
(Mid-battle, the lake's first crack:) [portrait: ANJA, neutral] Hear that? That's the lake learning you.
(Mega Glalie:) [portrait: ANJA, smug] The old ones knew how to close a crack. So does he.
(Her last Pokémon, Mamoswine "Matriarch":) [portrait: ANJA, neutral] Matriarch. Show them what's under the ice.
(WIN:)
[portrait: ANJA, neutral] The ice held for you. It doesn't hold for many.
[portrait: ANJA, neutral] Here. The SOUNDING BADGE. My family's line is a hundred fathoms of rope with a knot in it for every name the lake's ever learned. You're the newest knot.
RECEIVE: SOUNDING BADGE. RECEIVE: TM13 ICE BEAM.
[portrait: ANJA, neutral] One more thing, and I'll say it to you like I say it to the children. When the lake breathes, you run. You don't look. You don't help. You run, to the towers, and you help from there.
[portrait: ANJA, sad] (quietly, not to the PC) ...The towers are the only thing out there with legs in the bedrock.
V132 = 4.
```
*(**Badge name (proposed):** the **Sounding Badge**, after the Mastery room's family sounding-line; not in PBS or BADGE_TIERS, like the earlier names (CHAPTER_BEATS decision 7). LoseText as in `pbs/trainers.txt`. The ice-climbers' Rock Climb (TM100) and the ice-fisher's Super Rod wait until the morning after: no side content between V132 == 4 and 7.)*

---

## Map 301 → 309/300 — **The Thaw** (key event 1)

### "Red and Climbing" (autorun on sleeping at 301 with V132 == 4; night)
```
(Night. The Center's window rattles. Somewhere a dog is barking and won't stop.)
(Juno is shaking your shoulder in her coat and nightdress, her wreath crooked.)
[portrait: JUNO, panic] \PN. \PN, get up. The lamps on the towers. They've gone from red to white. Is that— is white normal? Nobody's out there. Why is nobody out there?
[estranged] (It's Anja at the door instead, coat over her nightshirt, pipe in her teeth, not lit.) [portrait: ANJA, neutral] Up. Boots. Now. Something's wrong with my towers and I want somebody who can walk on bad ice.
Script: Prismfall.checkpoint
(Fade. The harbour at night. The ice is wet. Your boots splash where yesterday they rang.)
```
### Map 300 — the second tower: Pell's console (autorun at the tower foot)
```
(Pell is at the console in the tower's hut, alone, in a coat over pyjamas. The screen is a column of numbers, and every one of them is red.)
[name: Pell] Don't— don't touch anything. I'm— it's fine. It's a spike. Tower Three's been spiking all week, it comes back down, it always comes back down.
SCREEN: DRAW 141% · 148% · 155% · ICE LOAD: — · — · —
[name: Pell] (very quietly) The ice load sensor stopped answering an hour ago. I thought it was the cold. It's built for cold.
[portrait: JUNO, neutral] Wake the city.
[name: Pell] I can't, I need authorisation from—
[portrait: JUNO, angry] I'm a Warden. That's authorisation. WAKE THE CITY.
(Pell's hand hovers over a big brass lever under a glass cap. He breaks the glass.)
SE: a horn, long and low, from every tower at once. Lights come on across Rimeholt, one window, ten, a hundred.
(Then, under the horn, another sound. Deep, and everywhere, and coming up through your feet.)
(The ice singing.)
[estranged] Anja says Juno's lines: "I'm the Warden of this lake. That's authorisation." She breaks the glass herself.
```
*(No jokes from here to the hut roof.)*
### Map 309 — the Sinking Quarter: **the ice goes** (autorun on stepping off the tower platform toward the lower town)
```
(The lower town: Net Row's far end, the fishing huts, the long halls on the harbour, all lit up now, people coming out of every door with lamps.)
(The ice cracks.)
(It doesn't break the way a window breaks. It breaks the way a page tears: a long black line across the harbour, slow, from the second tower's feet out to the far end of Net Row, and the ice on the far side of it tilts, just a little, the way a table tilts when one leg goes.)
(A whole street of houses is on the far side of the line.)
(The lamps on that side start, very gently, to slide.)
SCREEN SHAKE. SE: a sound like the world's biggest door being opened.
(Screaming. Somebody is ringing the harbour bell, over and over and over.)
(Across the black line, figures in Meridian grey are running the other way: toward the towers, not away from them, with crates.)
[portrait: JUNO, shocked] They're— they're not helping. Why aren't they helping?
Switch S128 CH11_THAW = ON. Variable V107 RIMEHOLT_STATE = 1.
```
### The partner battle: **"Securing the Lattice"**
```
(On the tower platform's stair, two Directorate officers with a handcart full of steel cases. One holds up a hand.)
[name: Directorate Officer] Platform's closed. Lattice asset recovery. Go back to the shelters.
[portrait: JUNO, angry] There are people in the WATER.
[name: Directorate Officer] And there are forty million crowns of Prism equipment on this platform, Warden, and our orders are very clear about which one we're here for.
[name: Directorate Officer] Step back, or be stepped back.
[if !JUNO_ESTRANGED]
  Script: pbRegisterPartner(:RIVAL_JUNO, "Juno", Prismfall::Rival.version_for(5))
  [portrait: JUNO, angry] \PN. With me.
[if JUNO_ESTRANGED]
  Script: pbRegisterPartner(:LEADER_ANJA, "Anja", 1)
  [portrait: ANJA, angry] My lake. My city. My platform. With me, southerner.
Script: setBattleRule("fieldChange", [2, :WATER_SURFACE, "The ice under the battlefield gives way!"])
BATTLE: TrainerBattle.start(:MERIDIAN_DIRECTORATE, "Ostrander", 11, :MERIDIAN_DIRECTORATE, "Vell", 11) — double, partner; field `:FROZEN_LAKE` → `:WATER_SURFACE` at the end of round 2 (the scripted fieldChange rule; the field can also crack earlier on its own).
Script: pbDeregisterPartner
(LOSE: whiteout to 301; the night restarts at Pell's console from the checkpoint.)
(WIN:)
(The officers' handcart goes over the edge of the stair into the black water, cases and all. One of them watches it go, and then sits down on the stair, and takes his helmet off.)
[name: Directorate Officer] (to nobody) It's not my equipment. I don't even know what's in them.
```
*(The partner battle is 06_ACT_III's beat 3. **Trainers (in PBS):** `[MERIDIAN_DIRECTORATE,Ostrander,11]` and `[MERIDIAN_DIRECTORATE,Vell,11]` (+100/200), Lv 50–51, built for an Ice-then-Water field: Ostrander Magnezone / Kingambit / Bronzong, Vell Pelipper (Drizzle) / Toxapex / Dragalge; partners `[RIVAL_JUNO,Juno,50–52]` (rival battle 5: Tsareena "Sweetpea", her starter, Florges; Lv 50–51; the starter swaps at load like every rival party) and `[LEADER_ANJA,Anja,1]` (Mamoswine, Walrein, Weavile; Lv 50–51). The fieldChange rule is the one Ch8 introduced (`003_FieldEffects_BattleState.rb`).)*
### **"It's Proof"** → GO_THIN_ICE (autorun as the platform shakes; same night)
```
(Pell comes running out of the tower hut with a tiny steel cylinder in his hand, and stops dead at the top of the stair. Behind him, the hut's floor is tilting.)
[name: Pell] The core! The data core, I've— no, this is the cache, the core's still in the rack, it's got everything, every reading, every override, who raised the tolerance, it's PROOF—
[name: Pell] Please. Please, I can't— my legs won't— it's two steps. It's right inside the door. It'll prove who's to blame. It'll prove it wasn't us. It wasn't ME.
(Inside the hut, through the door, you can see the rack. A green light on it. Two steps. The ice around the hut is grey and humming.)
```
```
> Go back for it.
  > The hut's on the grey ice. Go in anyway?
    > Go in.
      (Two steps. The green light. Your hand on the core.)
      (The ice remembers your weight. It has been remembering it since the Boathouse.)
      (The floor goes. Not a crack, this time. Just: gone. The hut, the rack, the green light, and you, into black water so cold it doesn't feel cold.)
      (Above you, very far up, a white square that was the door. It gets smaller.)
      Script: Prismfall.game_over(:GO_THIN_ICE)
    > No.
> Pull Pell off the platform. Leave it.
  (You get him by the scarf. Juno gets him by the coat. He's still holding the cache.)
  (Behind you, the hut leans, and leans, and goes into the lake with a long hiss of steam, and the green light goes down into the dark like a coin.)
  [name: Pell] (on his knees on the stair) That was everything. That was everything that happened.
  [portrait: JUNO, neutral] (shaking) You're everything that happened. You saw it. Remember it.
```
*(GO_THIN_ICE: NARRATIVE_KEYS §9, epitaph "You went back for the proof. The lake kept it, and you." Foreshadowing: Anja's "Ice remembers every weight", the Gym 10 crack tutorial, Pell's own "within tolerance". The cache Pell keeps is small and partial; it reaches the Larch Papers (Ch12) as one page that "nobody reads" (14_WAR_AND_BLESSING, the Ch12 insert).)*
### **"The Lake Breathes"** → GO_WEATHER (autorun, the harbour edge)
```
(The black line across the harbour has stopped widening. For a moment everything is still. The bell has stopped. Even the screaming has stopped.)
(The water in the broken ice rises. Not a wave. The whole harbour lifts, slowly, like a chest filling, and the floating slabs of ice lift with it, and the lamps on them, and the people on the lamps.)
(Then it lets out. The water sinks down through the cracks with a long, long sigh that you feel in your teeth.)
(In the black water beyond the second tower, something opens.)
(An eye. Blue and gold, with ridges of red light round it like coastlines on a map. It is bigger than a house. It looks at the city. It looks at the towers.)
(It looks at you.)
(In your pocket, the shard goes cold, then warm.)
[portrait: ANJA, panic] (from somewhere across the ice, a voice you know) That's not a Pokémon, that's WEATHER. TOWERS! EVERYBODY TO THE TOWERS!
```
```
> Fight it now.
  > Anja said run. Fight it here, on the broken ice?
    > Fight it.
      Script: Prismfall::Bosses.wild_battle(:KYOGRE_WEATHER)
      (It doesn't fight you. It doesn't notice you. It rolls over in the water the way a sleeper turns in bed, and the harbour turns over with it, and the slab you're standing on stands up on its end, and the lamps go out.)
      Script: Prismfall.game_over(:GO_WEATHER)
    > No.
> Get to the towers.
```
*(GO_WEATHER: NARRATIVE_KEYS §9 ("You tried to fight the sea. The sea didn't notice. In spring, Rimeholt carved your name on the ice wall, and the thaw took that too."). `:KYOGRE_WEATHER` is registered in `plugins/Prismfall Bosses/101_Boss_Kyogre.rb`: Lv 80, unwinnable, no catch, the battle ends after one round whatever happens.)*
### The sprint (309 → 300, the tower platform; a scripted crack-run)
- The player crosses about 30 tiles of breaking harbour ice from the harbour edge to the fourth tower's platform. It uses **Gym 10's own rules**: ice slides, and **cracked** tiles hold once. Here every tile the player leaves cracks behind them, so you can't go back.
- The route has three choices. Each choice is a family or a Pokémon on a tilting slab: a net-mender with a child, an old man on a sled, and a Lapras calf caught in a net.
  - Reaching one costs a slide or two.
  - Every one reached is carried to the platform: they follow the player and lift up the ladder at the end.
  - Missing one is allowed and isn't punished in keys. Their slab just goes under. The Sinking Quarter quest later counts who made it.
- There is no fail state: if the player slides into black water, they're pulled out at the last marker ("Roll to the marker!").
- **Puzzle engineer** owns the layout. Keep it short: one screen, under a minute.
- When the player reaches the platform, Juno is already at the top of the ladder, hauling people up. If she is estranged, Anja is there instead.
```
(The fourth tower's platform: steel, on piles that go down into the dark, into the bedrock. The only thing out here that doesn't move.)
(Everybody who can get here is here. Children in fur hoods lying flat, the way they were taught. Anja is at the ladder, hauling people up by their collars, one after another.)
[portrait: ANJA, neutral] (not looking at you) Good. You ran. Now help from here.
(The water at the platform's edge rises again. And this time it doesn't sigh out. It comes up, and up, a hill of black water with the eye in it, and rain starts falling out of a clear sky: warm, heavy, tropical rain, on a frozen sea at midnight.)
(The boss follows at once.)
```
### **Boss: Kyogre** (the tower platform)
```
Script: Prismfall::Bosses.wild_battle(:KYOGRE_ISENMAR)
— `:FROZEN_LAKE` → `:WATER_SURFACE` at break 1; Primal at break 2 (the shard hums); on a Harmony lean (resonance >= 2, NARRATIVE_KEYS) the last bar calms it. No catch.
(LOSE: whiteout to 301; the night restarts at the tower foot from the checkpoint, the partner battle already won.)
[if Prismfall::Bosses.last_result[:result] == :calmed]
  (The shard in your pocket is warm as a hand. You take it out without meaning to, and hold it up, in the rain.)
  (The great eye looks at it. Then at you. For a long moment it looks at you as if you were very small and very familiar, like somebody it knew a long time ago who has grown up strange.)
  (Then the eye closes. The hill of water goes down. The rain stops, here; you can see it going on, out east, a grey wall walking away across the ice.)
  FIELD NOTES: "It looked at me as if I were very small and very familiar."
[else]
  (Kyogre goes under. Not beaten: tired. The water closes over the eye like a lid.)
  (The rain doesn't stop. It moves east, a grey wall walking away across the ice, and the sea behind it isn't frozen any more.)
  FIELD NOTES: "It went back down. I don't think I won. I think it decided I wasn't worth staying up for."
Switch S129 CH11_KYOGRE_DONE = ON. V132 = 6.
```
*(06_ACT_III beat 5 and 09 #22. The sea is no longer fully frozen either way: V107 = 1 opens the Ice Vault's meltwater channels (DUNGEON_PUZZLES, the Ice Vault; Kyogre sleeps in 318 from now on, and `:war_legend` comes for it in Ch17–18).)*

---

## Map 314 — Net Row: **"Because the Heaters Were Warm"** (autorun at dawn, V132 == 6)
```
(Dawn, if you can call it that. Rain. The lower town is a quarter gone: the far end of Net Row ends in black water with roofs standing up out of it like the backs of whales. Slabs of ice turn slowly in the harbour. Boats are out, everywhere, pulling people off rooftops.)
(Anja is standing on the roof of a fishing hut that's half under, with her coat open in the rain, watching her city.)
[portrait: ANJA, sad] I read the numbers.
[portrait: ANJA, sad] Every month Meridian sent me the readings. Ice load. Draw. Every month the ice got thinner and the draw got bigger and they sent me a letter that said "within tolerance", and I signed it. I put my name under it.
[portrait: ANJA, sad] I read them. I *read* them. And I signed anyway, because the heaters were warm.
(She looks down at you. Rime has melted out of her eyebrows. She looks older than she did yesterday, and smaller.)
[portrait: ANJA, neutral] My brother's holding court at noon. In the Keep. He'll want to know whose fault it was. Everyone will want to know whose fault it was.
[portrait: ANJA, neutral] You were on that platform. You saw Pell's console. You'll be asked.
(Beside you, Juno is wet through, shaking, with somebody's baby still in her arms because she hasn't found anyone to give it to.)
[portrait: JUNO, sad] That's what Uncle Rowan meant. Isn't it. The flowers. The heaters. It's all the same thing.
[portrait: JUNO, crying] Everything's warm, and everything's growing, and nobody asks what it's drinking.
[estranged] (Juno is on the next roof over, alone, handing children down to a boat. She hears Anja. She says her line to the rain, not to the PC.)
```

## Map 307 — Whalebone Keep, the Thane's Seat: **the court** → **CHOICE `:ch11_anja`** (autorun at noon, V132 == 6 → 7)
```
(The Thane's hall is full: fishers in wet furs, skalds, the Meridian delegate in a dry coat, Directorate officers by the doors. Thane Eirik is on the whale-jaw seat. He hasn't slept. Anja stands alone in the middle of the floor.)
[portrait: EIRIK, angry] Two hundred and six. That is how many of my people are not in their beds this morning. Some of them are in other people's beds. Some of them are under the lake.
[name: Meridian Delegate] Your Majesty, Meridian Heat Services extends its deepest sympathy. The towers operated within the tolerances agreed with your Warden. Responsibility for the—
[portrait: EIRIK, angry] (to Anja, not looking at the delegate) Did you know?
(Anja doesn't answer. Eirik looks at you.)
[portrait: EIRIK, neutral] You were on the platform. With the technician. My sister says you saw his console before the ice went. Tell me what you saw.
(In your bag, Pell's cache. In Pell's head, every number. Anja is looking at the floor.)
```
```
> Tell the court what the console showed. Every number. (expose)
  Script: pf_choose(:ch11_anja, :expose)
  (You say it. Draw at a hundred and fifty-five percent. The ice load sensor dead for an hour. The tolerance raised in the spring. And the monthly readings, signed in the Warden's hand.)
  (Pell, at the back of the hall, stands up when you say his name and says, "Yes. That's right. I'll swear to it." His voice cracks on "swear".)
  (The hall goes very quiet.)
  [portrait: EIRIK, sad] ...Anja.
  [portrait: ANJA, neutral] It's true. All of it. I read them.
  [portrait: EIRIK, angry] Then hear me. My sister is stripped of her honours, her seat at this table, and her name on the harbour wall. Wardens can't be unmade by kings. But I can make sure no Isenmar hall ever opens its door to her again.
  [portrait: EIRIK, angry] (to the delegate) And Meridian. Meridian, who wrote "within tolerance" on two hundred and six graves. You'll hear from my lawyers. You'll hear from every hall on this coast.
  (The delegate leaves. Nobody stops him. Nobody bows.)
  (Anja walks out past you. She doesn't look at you. At the door she stops.)
  [portrait: ANJA, neutral] You did right. I'd have done the same. I'll never forgive you for it. Both of those.
> Say nothing. Let her answer. (let_confess)
  Script: pf_choose(:ch11_anja, :let_confess)
  (You look at Anja. The hall looks at you looking at Anja.)
  (She lifts her head.)
  [portrait: ANJA, neutral] I knew.
  [portrait: ANJA, neutral] Every month. The ice load and the draw. I read them, brother, and I signed them, and I told you the lake could take it. I told you because the babies were warm and I wanted them to stay warm. I'd tell you again if it was last winter.
  [portrait: ANJA, angry] But it isn't last winter. (She turns to the delegate.) Meridian Heat Services wrote "within tolerance" on that letter every month. Your tolerance. Your towers. Your lake, you thought. It's mine. Get out of my hall.
  (The delegate looks at the Thane. The Thane says nothing at all. The delegate leaves.)
  [portrait: EIRIK, sad] (after a long time) ...Sit down, Anja. Sit by me. We've a city to move.
  (On her way to the seat, she passes you, and she puts a hand on your shoulder for one second, hard, like a vice.)
```
*(NARRATIVE_KEYS §4.2 `:ch11_anja`: `:expose` ACCORD+1 MERIDIAN−1, `ANJA_EXPOSED` (Act V: she refuses to release the Icicle Plate, "Rimeholt drowns without it"; the Festival R16 grudge seat); `:let_confess` the Act V swing vote, she lets go at the end (WARDEN_CONSENT entry 10). **Either way Anja breaks with Meridian publicly.** V132 = 7.)*
```
[portrait: EIRIK, neutral] (to the hall) Martial law, from this hour. The lower town is gone. The upper town won't hold another freeze on this much water. Every family south of the second tower goes south. Over Frostfang, down the Icecutters' Haul, into Elowen, to my cousins in the Hoarwood and wherever the Queen will have them.
[portrait: EIRIK, neutral] Warden Hale. You'll walk with them. The Thornguard will want to count them at the border, and they'll count them slower if there's no Warden of Elowen standing there.
[portrait: JUNO, neutral] (straightening) I'll go. Of course I'll go.
[if :war_warning == :warn_isenmar]
  [portrait: EIRIK, neutral] (to the PC) And you. Your letter from Frostfang came to my hand last night, two hours before the horn. Fifty fires on Ossarian sand. My generals said nonsense. They are not saying nonsense this morning.
[if :war_warning == :warn_both]
  [portrait: EIRIK, neutral] (to the PC) The Sovereign's letter reached me with your Warden's name on it. Every hall has it. Ashkaar has it. So the Dominar can't say he wasn't seen. Good. Let him be seen.
[if :war_warning == :warn_ashkaar]
  [portrait: EIRIK, neutral] And there's a rumour from the pass that someone told an Ashkaar rider his camps had been spotted. If I find out who, I'll thank them for nothing.
[if :war_warning == :silent]
  (He doesn't mention the sands. Nobody does. Nobody knows.)
```
*(Thane Eirik's evacuation is 06_ACT_III's "martial law"; it causes the Thornguard border crisis that Juno goes to face (her Ch12 scenes are by Circular).)*

## Rimeholt, the three days (V132 == 7)
After the court the city is in its V107 = 1 state for good: the lower town (309) half under water, with boats and floating slabs; Net Row ends in the lake; the towers are dark (the Thane has them shut off); refugees in the Mead Hall; rain.
**Side content opens now** (V132 >= 7), all before the column leaves:
- **The ice-climbers** (303's wall): Rock Climb, TM100. "We're climbing down today, not up. Same rope."
- **The ice-fisher** (300): the Super Rod. "Water's open everywhere. Might as well fish it."
- **The Tally board** (306): IS_SINKING_QUARTER (counts the families carried to the platform), IS_HARPOON_RITE, IS_ELEVEN_YEARS (Old Torstein, still at his hole: "Something's moving under me. Fish, I expect."), the Lapras "Saga" gift via the Tally.
- **Cameo, "Crystal Sleep" (Alexandra; CAMEOS #5)** in the Sinking Quarter (309): a tall woman with a Latias among the half-Fixed fishers on the broken ice, asking each one if they can hear her. **Docs reconciled:** CAMEOS's staging wins (she is awake, among the Fixed); the Trials entry IS_ALEXANDRA is re-pointed to her (giver Old Halla, the same fight). Reward: Draco Meteor tutor, CELINE'S NOTES; Field Notes gains "the sleepers may be dreaming" (if not already from Ch7).
- **Hook, "The Doctor's Cell"** (S174 on, at 301's Circular): a letter in a child's careful capitals, signed WENLOW: "DR CORVIN WAS ARRESTED UNDER THE MANDATE FOR TREATING HOLLOW PEOPLE. THEY HAVE HIM ON A BARGE ON LAKE SALLOW. HE SAID NOT TO TELL YOU. I AM TELLING YOU." *(The quest runs Ch11–13; WALKTHROUGH.)*

### Map 301 → 300 — **the third day: war** (autorun on leaving 301 with V132 == 7 after any rest, or on talking to Juno at the column; V132 → 8)
```
(Morning of the third day. The rain has stopped over Rimeholt at last. Out east it hasn't: the whole eastern sky is a grey wall, three days thick.)
(Every screen in the harbour is on: the Center's, the Sled Market's, the big one on the Keep's gate. A crowd under each one, in the cold.)
SCREEN: (A newsreader, Meridian blue behind her.) "—catastrophic flooding in the western dunes of Ossaria, where, we can now confirm, the forward camps of the Ashkaar legions have been—"
SCREEN: (A great hall of black stone. A huge grey-bearded man in dragon-scale, Dominar Hrothgar Ashfall, standing.) "Isenmar sent its sea-beast against my soldiers sleeping in their tents. Four hundred of my sons drowned on dry land. The Thane will answer for every one."
SCREEN: (The Whalebone Keep's gate, this morning, in the rain.) [portrait: EIRIK, angry] "My city is under the lake because Ashkaar closed the passes and stopped our heat. Ashkaar starved Rimeholt, and the lake ate what was left. Ashkaar will answer for it."
SCREEN: (A white room. A silver-haired man in a beautiful grey coat, sitting easily, the sunburst pin on his lapel. Director Voss.)
[portrait: VOSS, happy] Meridian deeply regrets the hostilities. As a neutral partner to every crown in the Accord, the Fellowship stands ready to provide logistics, heat and medical support to both parties, on equal terms, for as long as they're needed.
SCREEN: ◆ ISENMAR AND ASHKAAR AT WAR ◆
(Nobody in the crowd says anything.)
(Down the Sled-Road, east, the Thane's host is already moving: war-sleds, harpooners, skalds with horns, a line of lamps going away along the ice toward the grey wall. Toward Skaldfast.)
(South, at the Icewall Gate, the other column: families with everything they own on hand-sleds, going the other way.)
[portrait: JUNO, neutral] (with her satchel and a borrowed fur, at the head of the south column) Both ways at once. Like the Ebb.
[portrait: JUNO, neutral] I'm going with them to the border. Somebody has to stand there with a Warden's sash on while the Thornguard count. Then I'll come and find you. Wherever you are.
[portrait: JUNO, sad] Don't do anything brave without me.
Variable V122 WAR_STATE = 2. V132 = 8.
QUEST LOG: "Eighteen Roads" — Walk the column south as far as Ebbmouth. Then back north, east on the Sled-Road, to Anchorhold and the airships.
[estranged] (Juno is at the head of the column and sees the PC across the gate. She lifts a hand. She doesn't come over.)
```
*(14_WAR_AND_BLESSING, the Ch11 insert: Kyogre's rain floods the Dominar's camps (and two Ossarian well-villages nobody mentions: a later Gazette line in Duneholt, Ch14); the Thane blames the embargo; the Dominar blames "Isenmar's sea-beast"; Voss offers both sides "neutral logistics". War is declared before the PC leaves Isenmar.)*

---

## The column south (704/705 back over Frostfang; a fade at the Icecutters' Haul fork)
```
(Frostfang Pass again, going down this time, in a line of hand-sleds a mile long. Children asleep on the bundles. Someone's grandmother on a sled pulled by a Mamoswine. At the watch-cairn Bryn stands by the flag and counts them through.)
[name: Bryn] (as you pass) Four hundred and twelve so far. I counted the fires on the sands, and now I'm counting these. I'd like to count something nice next.
(At the fork where the Icecutters' Haul goes down to Elowen and the coast road goes to Ebbmouth, the column splits: inland families after Juno, fishers' families toward the sea.)
[portrait: JUNO, neutral] This is me. (She hugs you, quickly, satchel and all.) Don't do anything brave without me. I mean it this time.
(Fade.)
```
*(If the PC has Fly, they may fly to Ebbmouth from the Rimeholt Center instead; the column scene plays as a short cutscene first.)*

## Ebbmouth (160, 167; Isenmar, second visit): **the Ebbmouth Strike** → **CHOICE `:ch11_strike`** (autorun on arrival at the Mill Quay, V132 == 8 → 9)
```
(Ebbmouth, the second time. The river's still stuttering: it runs, stops, runs. The Meridian Lattice intake on the far bank hums.)
(The Mill Quay is full: the whole Ebb Guild, a thousand people, dockworkers' saws over their shoulders, Rimeholt's refugees at the back with their bundles. Banners: THE EBB RUNS BOTH WAYS. NOT OUR SLEDS. NOT OUR WAR.)
(On the strike's banner pole, by the bell:)
[if TEO_SAVED]
  (Teo is up the pole on a rope, nailing a banner to it with his left hand. The fingers of his right are glass to the second knuckle, and he holds the nails in them like a clamp. He sees you and grins.)
  [portrait: TEO, happy] You came! Look at this. Look at all of them. I told her. I told her a thousand people would come out if she asked them properly.
[else]
  (A photograph is nailed to the pole under the banner, under glass to keep the rain off: a boy in a porter's coat, laughing at whoever was holding the camera. Under it, chalked: TEO REYES. FIXED AT IRONREACH. CARRIED HOME.)
(Marisol is on the bell-step with a speaking-trumpet.)
[portrait: MARISOL, angry] This morning the Thane's levy officers took forty of our sleds for his war. Forty. Off our quay, out of our barns, without a vote.
[portrait: MARISOL, angry] And for a year Meridian's been drinking our river at night and calling it "within tolerance". Well. Rimeholt was within tolerance. Ask them. (She points at the refugees.) Ask them how tolerant the lake was.
[portrait: MARISOL, neutral] So here's the motion. We cut the Lattice. Tonight. With our own saws. And the Guild runs food to Skaldfast for the families on the front: on our sleds, on our say. Not on Eirik's. All in favour.
(A thousand hands. More. The refugees' hands too.)
```
```
(Dusk. The whole quay goes down to the Lattice intake with saws. The cables are as thick as your arm. It takes forty people on each one.)
SE: a long screech of steel, then another, then a deep THUNK, and the hum stops.
(The river stops too, for one breath, the way it stopped the night in spring.)
(Then it turns. Out at the river mouth the tide comes in, and the Ebb runs backward, uphill, the way it's supposed to, past the mills, the first time in a year. The waterwheels on the Guild mills creak and start to turn the wrong way, which is the right way.)
(The quay cheers so loud the gulls go up off the whole coast.)
Variable V108 EBB_STATE = 3. Switch S130 CH11_EBB_STRIKE = ON.
```
```
(Lamps on the coast road. A column of grey coats, two dozen, with batons and a wagon of new cable. A foreman in front with a megaphone.)
[name: Directorate Foreman] By order of the Mandate, this is an unlawful obstruction of critical Fellowship infrastructure. Disperse, and nobody gets hurt.
(The Guild links arms across the intake. Marisol is in the middle.)
[if !TEO_SAVED]
  [portrait: MARISOL, angry] (to the foreman, very quietly, and everyone hears it) Nobody gets hurt. You'll want to look at that pole.
  [portrait: MARISOL, crying] He was nineteen. Nineteen. Tell me again how the Hollow are the monsters.
[if TEO_SAVED]
  [portrait: TEO, angry] (beside his sister, glass hand on the cable) Come and take it, then.
  [portrait: MARISOL, neutral] Teo. Shut up. (She doesn't take her eyes off the foreman.) He's right, though.
(The strikebreakers draw their batons. Marisol looks along the line, and finds you.)
```
```
> Stand on the line with Marisol. (stand)
  Script: pf_choose(:ch11_strike, :stand)
  (You take Marisol's arm. Her grip is like a rope.)
  [portrait: MARISOL, happy] (without looking at you) Thought you might.
  Script: pbRegisterPartner(:LEADER_MARISOL, "Marisol", 1)
  BATTLE: TrainerBattle.start(:MERIDIAN_AGENT_M, "Strikebreaker", 11, :MERIDIAN_DIRECTORATE, "Foreman", 11) — double, partner; field `:WATER_SURFACE` (the river running again).
  Script: pbDeregisterPartner
  (LOSE: the strikebreakers reach the intake but the Guild holds; whiteout to 161; the scene restarts at the line.)
  (WIN:)
  (The foreman's Pokémon go back into their balls. He looks at the line, a thousand people with saws, and the refugees behind them, and the photograph on the pole.)
  [name: Directorate Foreman] ...I'm writing this up as "infrastructure unrecoverable". (He turns the wagon round.)
  [portrait: MARISOL, sad] (when they've gone, sitting down on the quay edge with her boots in the river) You know what Teo used to say? That I'd stand up to anyone but never on anyone's side. (She looks at you.) You picked a side. I'll remember that till I'm old.
> Talk the foreman down. (mediate)
  Script: pf_choose(:ch11_strike, :mediate)
  (You step out between the lines with your hands open, and talk: about the river, the cables, the refugees, and what a megaphone sounds like in a report to Lumen when it's played back next to a thousand people's hands.)
  (The foreman lowers the megaphone. He's young under the helmet. He looks tired.)
  [name: Directorate Foreman] ...Fine. "Infrastructure under review." We'll come back with lawyers instead. That do?
  (He turns the wagon round. Nobody gets hurt. The quay doesn't cheer.)
  [portrait: MARISOL, neutral] (later, coiling a rope, not looking at you) That was clever. Polite. Nobody got a bruise.
  [portrait: MARISOL, neutral] And you never said which side you were on. Not once. I was listening.
V132 = 9.
```
*(NARRATIVE_KEYS §4.2 `:ch11_strike`: `:stand` MARISOL+2 MERIDIAN−1, and +1 more MARISOL if Teo didn't survive (the only Act III way back to her after Teo); `:mediate` MARISOL−1 MERIDIAN+1. **Trainers (in PBS):** `[LEADER_MARISOL,Marisol,1]` partner (Gyarados, Pelipper, Kingdra; Lv 50–51), `[MERIDIAN_AGENT_M,Strikebreaker,11]` (Machamp, Honchkrow) and `[MERIDIAN_DIRECTORATE,Foreman,11]` (Copperajah, Electivire) (+100/200; Lv 50–51). Marisol's full line was held back in Ch9 for here (27_SCRIPT_CH9, the note after `:ch9_teo_sable`).)*
**Optional:** the Ebbmouth Sea Grotto (723) is open to revisit with Surf. The eel stall's ledger ("THE BOY (4 EELS, DAILY)") has a new line: "THE BOY'S FRIEND (1 EEL, ON THE HOUSE)".

---

## The Mast Road (back north through Rimeholt; Road 11)

### Map 720 — The Thane's Sled-Road (`:SNOWY_MOUNTAIN`)
Road sign: "THE THANE'S SLED-ROAD. East to Skaldfast. MILITARY TRAFFIC HAS PRIORITY."
```
(A road of packed ice, wide as a river, going east. War-sleds pass you every few minutes: harpoon-guns lashed under tarpaulins, skalds asleep on the crates, a Mamoswine team with frost on their tusks.)
(A young harpooner on a resting sled, eating bread.)
[name: Harpooner] My nan's house went under in the Thaw. So I'm going to fight Ashkaar. (He thinks about it.) That doesn't really follow, does it. Everyone's going, though.
```
Trainers (Lv 48–52): skalds, harpooners (Isenmar soldiers; `ISENMAR_SOLDIER`), a war-sled driver. **Optional:** 728 **Stillwater** (`:BLEED`), just off the road outside Rimeholt: a waterfall hanging frozen in mid-fall without being ice. Field Notes: "Not frozen. Stopped. Like the Fixed. The water's still moving, just very, very slowly, inside itself."

### Map 721 — The Mast Glacier (`:SNOWY_MOUNTAIN`, borderland B2)
```
(Up onto the glacier. Tundra, then ice, then wind-carved ridges of permafrost dune, white sand frozen into waves.)
(From the top of the first ridge, far to the east: the grey wall of rain at last breaking up, and under it, brown, the dunes, with a white line drawn across them where the Thane's host has frozen the sand to march on.)
```
Trainers (Lv 50–53). Wild per WALKTHROUGH.

### Map 730 — Anchorhold: **"LARCH SPEAKS TONIGHT"** (Chapter 11 close; autorun at the moorings, V132 == 9 → 10)
```
(Anchorhold: a town of iron masts sunk into the glacier, and tied to them, rising and falling gently in the wind like moored whales, Skyreach's airships.)
(At the far mooring, a Gale Post mail-ship is loading in a hurry. Sacks thrown up hand to hand. A Pelipper on every rail. Off its stern, cracking in the wind, a long banner in red letters:)
BANNER: LARCH SPEAKS TONIGHT.
[name: Gale Post Loader] All of it! Every sack! Captain wants us over Skyreach by dark! (He sees you.) You! You're the one with no colour. The Professor's lot. Captain Gale said if you turned up to put you on. She didn't say why. She never says why.
> Go aboard.
(The ship slips its mooring. Anchorhold falls away. The glacier spreads out below like a white sheet with folds in it.)
(East, the sands. Isenmar's host strung out along its white road toward Skaldfast, tiny, like ants. And beyond it, the smoke of the Dominar's camps, still rising, fewer than before.)
(The ship turns south. Over Ossaria's dunes. Over Elowen's forest, green going on forever, and somewhere in it, on the border, a column of families, and a girl in a borrowed fur with a sash on.)
(And then, rising over the horizon: the Crownwall. A white ring, miles across, with a city inside it.)
V132 = 10. V102 STORY_CHAPTER = 12.
QUEST LOG: "Eighteen Roads" — Skyreach. Odessa Gale's eleventh badge, and whatever Larch is going to say.
```
*(06_ACT_III's cliffhanger. Ch12 "Dead Letters" opens aboard the mail-ship with the Larch Papers. The Gale Post's speed is why Fly isn't needed for the air leg.)*

---

## Map events needed (Chapter 11)

None of these maps is built. **[NEW]** = an event or map not in maps.json. V132 = **CH11_STEP** (design/FLAGS.md). Maps go through the three-pass workflow (design/MAPGEN.md, top): Claude's first pass, Claude's refinement on quota only, then Gemini.

**281 Verdance Pokémon Center** — **"Walking Papers"** autorun (V132 == 0): Juno at the counter, or her note if estranged.
**284 Kingsgate Barbican** — the Thornguard sergeant at the north gate (touch, once).
**700 The Hart's Run** — road sign; Juno's speech spot 1 (touch, once; follower dialogue); the deer-herd (IS_WHITE_STAG rumour); trainers.
**701 The Hoarwood / 710–711 Snowbriar** — the first-snow line (touch at the treeline, once); the lodge-keeper (IS_WHITE_STAG), the sledge-driver; the Circular board; Juno's speech spot 2 at the lodge fire.
**703 Gossamer Heartwood** (optional) — as DUNGEON_PUZZLES; Juno's one line at the first curtain.
**704/705 Frostfang Pass** — trainers; **the watch-cairn on 705's summit**: cairn and frozen flag, the stone hut, Bryn (pass-warden) with the brass glass, the Ashkaar rider and his grounded Flygon behind the cairn, the **east-view overlay** (the smoke threads and the dragon ring, a panorama or fog layer); `:war_warning` autorun (V132 0 → 1); Bryn's Corvisquire (move route, flies off) on `:warn_isenmar`; the Flygon's limping take-off (move route) on `:silent`. Later, Bryn counting the column (V132 >= 8).
**712 The Whalebone Road** — road sign; the whale-jaw arches (decor every 10 tiles); the old man on the sled singing the Sleeping Whale; Juno's speech spot 3.
**303 Icewall Gate** — arrival autorun (V132 == 1): the scanner arch over the rib gate (Mandate decor, text "Warmth is a right"); the gate skald; the steaming hole by the first tower. Later (V132 >= 7) the ice-climbers' wall (Rock Climb TM100).
**300 Thane's Harbour** — the four heat-towers on platforms (tall event sprites; red lamps until V132 == 4 night, white during the Thaw, dark after V132 >= 7); the drill (Anja and six children; touch, V132 == 2); "Toes" (V132 2 → 3); Pell at the second tower; the fisher at the open hole; Old Torstein on the flats (and his Avalugg); the ice-fisher (Super Rod, V132 >= 7); **the Thaw night**: Pell's console in the tower hut (a screen event with the red column), the alarm lever, the partner battle on the platform stair (two officers and the handcart), Pell and the core (GO_THIN_ICE), the harbour edge (GO_WEATHER and Kyogre's eye: a large animated event in the water, or a fog/picture overlay), the tower-four platform (Anja at the ladder; the boss); **day three**: the screens (Center, Sled Market, Keep gate) and the two columns (east on the Sled-Road, south at the gate).
**301 PC · 302 Mart · 304 Sled Market** — townsfolk as written; 301's Circular (Marisol's strike post; Valen's reply if `:warn_both`; Wenlow's letter, S174, V132 >= 7); the sleep trigger for "Red and Climbing" (V132 == 4).
**305–307 Whalebone Keep** — 306 the Mead Hall: Eirik signing papers (touch, once, before the Thaw); refugees after V132 >= 6; the Tally board (IS_SINKING_QUARTER, IS_HARPOON_RITE, IS_ELEVEN_YEARS, the Lapras "Saga" gift) from V132 >= 7. **307 the Thane's Seat**: the court (autorun V132 == 6 → 7): Eirik on the whale-jaw seat, Anja alone on the floor, the Meridian delegate, Pell at the back, 4 officers, 12 fishers/skalds; the `:ch11_anja` branches; the evacuation order. **308 Ice Vault**: locked this chapter (the Sleeping Whale door; DUNGEON_PUZZLES); its meltwater state follows V107.
**309 The Sinking Quarter** — **two states** by V107: frozen (0) and sunk (1: a quarter of the tiles to deep water, roofs as obstacles, boats as NPCs); the crack-line autorun (S128, V107 = 1); **the sprint** [NEW] (309 → 300, Gym 10 crack rules, three rescues; puzzle engineer); after the Thaw, Alexandra's cameo among the half-Fixed fishers (CAMEOS #5) and IS_SINKING_QUARTER.
**310–313, 315–316 Lake Hall** — as GYM_PUZZLES Gym 10; Liv; the net-mender; **Anja (313), single**, her three mid-battle lines; SOUNDING BADGE, TM13; V132 = 4.
**314 Net Row** — the net-mender's line; **"Because the Heaters Were Warm"** at dawn (V132 == 6): Anja on a half-sunk hut roof, Juno with the baby; the street ends in water after V107 = 1.
**Ebbmouth 160 / 167 Mill Quay** — the strike (V132 == 8 → 9): the banner pole (Teo on it if S221, else the photograph), Marisol on the bell-step, ~20 Guild NPCs and refugees (a crowd, not a thousand), the Lattice intake cables on the far bank (cut: three event sprites go to "cut" self-switch), the river's direction (V108 = 3: the current tiles flip; the mill wheels' animation reverses), the strikebreaker column (6 NPCs and a wagon), the `:ch11_strike` branches; the eel stall's ledger line. 723 Sea Grotto open.
**720 The Thane's Sled-Road** — road sign; war-sleds passing (looping move-route events on the road's centre lane, not blocking); the harpooner; trainers. The turn-off to **728 Stillwater** (optional, `:BLEED`, the hanging waterfall, Field Notes).
**721 The Mast Glacier** — permafrost dunes; the eastern view from the first ridge (overlay); trainers.
**730–731 Anchorhold** — the moorings with airships (big event sprites, a slow bob); the Gale Post loader; the LARCH SPEAKS TONIGHT banner; the boarding autorun (V132 9 → 10, V102 = 12) and the flight cutscene (glacier, the host on the sands, Elowen, the Crownwall).

**Trainer designer:** `[MERIDIAN_DIRECTORATE,Ostrander,11]`, `[MERIDIAN_DIRECTORATE,Vell,11]`, `[MERIDIAN_AGENT_M,Strikebreaker,11]`, `[MERIDIAN_DIRECTORATE,Foreman,11]` (each with 111/211); partners `[RIVAL_JUNO,Juno,50–52]` (+100/200), `[LEADER_ANJA,Anja,1]`, `[LEADER_MARISOL,Marisol,1]` (one version each; every mode falls back to it). **All seven are in `pbs/trainers.txt`** (2026-11-21; validate_trainers 0 errors). **BOSSES.md:** `:KYOGRE_WEATHER` (GO_WEATHER; registered). **Badge name (proposed):** the **Sounding Badge**. **Docs to reconcile:** the Trials IS_ALEXANDRA entry (asleep in a block of ice) is replaced by CAMEOS #5's staging (awake among the Fixed); WALKTHROUGH says S128 is set at the war declaration, but FLAGS says "the Thaw happened", and this script sets it at the Thaw.
