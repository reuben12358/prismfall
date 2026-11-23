# Script: Chapter 14 — "The Deep Seams" (the Grave Road, Vigil, Cragholm, Gym 13; the Ring-Day; the badge case; the raid; Duneholt and Groudon)

> **Final playable script** for Chapter 14, the first chapter of Act IV. It covers the Grave Road (772 Yesterday's Road, 770/771 Vigil and the Grave Glass, 760 the Obsidian Barrows, 761 Spinefall Gorge, 773 the Vertebrae), Cragholm (360–363 and the deep seams), Gym 13 (370–374), the optional Geode Hollow (764/765) and Dreaming Quarter (768), the Darkglass Mine (784/785, the raid), and the transit south: Hindmoor's edge, the Dry Tide (810) and the bone-carters' camp (930), Duneholt (200–209, 214), the Duneholt Undersands (783), Stonesleep (788), and Hindmoor (781) for the cliffhanger. Only 930 is built. The list at the end is what to build from.
> Follows `story/32_SCRIPT_CH13.md`. Chapter 15 ("The Hollow Cathedral") follows, and opens with the War Convoy (CHAPTER_BEATS density note). Sources: 07_ACT_IV Ch14, 03_CAST (Bastian, Pip, Larch, Kassan, Sahar, Thistle, Wick, Rowan, Teo, Corvin, Wenlow, Anja, Marchetti, Quent, Kestrel), 09_MYSTERIES (#1, #5, #6, #14, #15, #24), 14_WAR_AND_BLESSING (Part B, Ossaria; the Ch14 row), NARRATIVE_KEYS (`:ch14_telemetry`, `:ch14_marchetti`, GO_WILLING, `TELEMETRY_SABOTAGED`, `MARCHETTI_TURNED`, `CORVIN_FREED`, `ANJA_EXPOSED`, `ROWAN_ALIVE`, `TEO_SAVED`), 15_COMEDY (Ch14 "Selectively"), 13_CUTSCENES RD-1, GYM_PUZZLES Gym 13, the Trials quests `OS_RING_DAY` (114, canonical strings), `OS_AMBER_AGAIN`, `OS_UNQUIET_ELECTOR`, `OS_UNDERSANDS`, `OS_BONEWRIGHT`, BALANCE (Bastian, Marchetti v1), WALKTHROUGH Ch14, `design/CHAPTER_BEATS.md`, **`design/DENSITY_STANDARD.md`** (the first script written to the floor), and Gemini's cast pool (`gemini_recommends/2026-11-22_unique-trainer-classes-and-expanded-cast`: Pip elevated, Zainab Darzi, rematches M5 and M7).

## Conventions
As in the earlier scripts. **Portrait cast here:** Bastian, Pip, Larch, Sahar, Kassan, Thistle, Wick, Rowan (if alive), Teo (if `TEO_SAVED` and Rowan drowned), Corvin (if `CORVIN_FREED`), Wenlow, Anja, Juno (if visiting), Marchetti, Quent, and the PC (a line at the badge case; `\pf[PLAYER,…]`). **Plain:** Zainab Darzi (Bone Chronicler: a portrait is requested; `[name: Zainab]` until it lands), the Directorate officer, the Meridian paymaster, the two quartermasters, Vigil's embalmers, the miners, the refugees, every trainer. Gym 13 is a single battle: `Prismfall.gym_battle(pfm_gym(:LEADER_BASTIAN), double: false)`. Marchetti is `TrainerBattle.start(:MERIDIAN_MARCHETTI, "Helene")` at **version 1** (WALKTHROUGH Ch14: Mega Houndoom; field `:DARK_CRYSTAL`). Groudon is the new boss key `:GROUDON_UNDERSANDS` (TODO_QUOTA §2 registers it).
**Counter:** V135 **CH14_STEP** (new; design/FLAGS.md): 0 on Yesterday's Road · 1 through the Grave Glass (Vigil) · 2 Cragholm: "Sit down" · 3 the deep seams (Larch's warning) · 4 day two: Anja's column and the meal · 5 Bastian's account · 6 "Selectively" (the gym opens) · 7 Gym 13 won · 8 the Ring-Day · 9 the badge case (S138) · 10 the raid done (S139) · 11 Duneholt: Kassan and the Lease · 12 Groudon (S140; V109 = 2) · 13 Hindmoor: the sponsor ship (chapter closed; V102 = 15).
**State set here:** S138 CH14_TELEMETRY_SCENE, S139 CH14_RAID_DONE, S140 CH14_GROUDON_DONE, V109 DUNEHOLT_WELL (1 at arrival, 2 after Groudon), V115 LARCH_STATUS stays 2 (fugitive). Keys: `:ch14_telemetry`, `:ch14_marchetti`. Game over: `GO_WILLING`. Key Items: MEGA RING (via `OS_RING_DAY`), LANCE MANIFESTS (evidence; a writer's note for `:ch20_envoy` `:proof`).

## The chapter's key events (design/CHAPTER_BEATS.md)
1. **Bastian's account and the Ring-Day.** The first eyewitness of AF 290 says it out loud: brass behind the Choir loft, white coats with little gold suns, dials, and "They weren't surprised. They were *pleased*." After Gym 13, the ring Brann cut "ten years back" sings in the PC's palm. Build-up: Ch8's chestnut slip, the Ch13 Mindscape (brass machines with sunburst plates), the Secret Articles still sealed in the Bag. Payoff: the Mega Ring, and Larch lowering her book. Consequence: Mega Evolution and Z-moves open, and three clues sit side by side for a player who wants them (Ch17 says it).
2. **The badge case opened.** Larch finds Lattice-glass and a transmitter in its lining: "Voss isn't watching you. He's **tuning** you." (`:ch14_telemetry`). Then the raid: Thistle holds the lift-shaft, Marchetti fights in the dark (`:ch14_marchetti`), and south in Duneholt, **Groudon** wakes under the dry well. Build-up: the case's chords at every badge since Ch1, the NULL scan, Ch12's broadcast. Consequence: the finale's Engine calibration, Marchetti's stand-down, the aquifer.

## Density (design/DENSITY_STANDARD.md; agents build from this section)
CHAPTER_BEATS: nine beats, "Ring-Day and the badge case are the heart". The War Convoy moves to the start of Ch15. Everything below is **optional except where marked critical**, so the critical path stays crisp.
| Item | This chapter |
|---|---|
| Story/boss/rival fights (≥4) | **Gym 13 Bastian** · **the lift-shaft tag (PC + Thistle)** · **Marchetti** · **Groudon** (all critical) · optional: Larch (M5), Sahar (M7), Pip's relay spar, Zainab |
| Route/gym/dungeon trainers (12–20) | 18 (roster at the end): Grave Road 5, Cragholm and the Vertebrae 3, Gym 13 5 (GYM_PUZZLES), Geode Hollow 2, the Undersands 3 |
| EventMons (≥3) | **Lairon "Wart"** (static, the east seam), **Komala** (static, the Dreaming Quarter), **Glimmet "Lampwick"** (gift, Pip's Tunnel Relay); the Stonesleep fossils feed the Dig Lab |
| Hangouts (2–4) | Pip at the lift-cages · Larch's bench · Zainab at the carters' fire · Sahar in the Dig Lab |
| Glassfall Slivers (4–6) | 5: the Obsidian Barrows tomb-mirror, behind Spinefall's falls, Geode Hollow B1F, a dreaming miner's hand (768), the glyph chamber (783) |
| Trials quests (≥3) | `OS_UNQUIET_ELECTOR` (Vigil), **`OS_UNDERSANDS` (now critical: the way to Groudon)**, `OS_BONEWRIGHT` (Cragholm), `OS_AMBER_AGAIN` (Dig Lab), new `OS_TUNNEL_RELAY` (Pip), new `OS_CARTERS_DEAD` (the bone-carters) |
| Badge overlay | Badge 13: `encounters_badgetiers.txt` tier for 760, 761, 764/765, 768 (Bleed-spread version 1 since S137) |
**No jokes** from the raid alarm (V135 9 → 10) to Thistle's last line at the shaft. "Selectively" is the day before. **No side content** opens in Cragholm between the badge case and the raid's end.

---

# CHAPTER 14 — "The Deep Seams"

**Chapter start:** V101 = 4, V102 = 14, V135 = 0. The PC leaves Lucent by the Grave Road. Quest log "Eighteen Roads": *North to Cragholm in the Bone Sands. Find Bastian Ore.*

## Map 772 — Yesterday's Road (`:INVERSE`)
Road sign: "YESTERDAY'S ROAD. Vigil 9." Every milestone after it counts **down** to 0 at the halfway stone, then up again, and the numbers are mirror-written until the PC passes them and looks back at their reflection in the wet stone. (Looking back at a milestone is allowed: Dask's rule is about the Glass, and a hiker says so.)
- A hiker on the halfway stone: "Zero. I like zero. Sit on it and you're nowhere for a minute. Don't worry, you can look back on this road. Only the Glass minds."
- A Synod novice with a broom: "We sweep yesterday's footprints off the road so nobody walks in them twice. Yes, it's a real job. No, it doesn't pay."
Trainers (Lv 57–58): the hiker, a psychic (Synod novice), a gravedigger.

## Map 770–771 Vigil and the Grave Glass (V135 == 0 → 1, a touch event at the Grave Glass)
Vigil is a town of embalmers and mirror-polishers at Antumbra's edge, where the dead of three kingdoms come to be put behind the Glass. The **Grave Glass** is a standing mirror the height of a house, framed in bone, at the north gate. Through it the road goes on into the Obsidian Barrows.
```
(The north gate. The Grave Glass stands across the road like a door with no handle. In it, the road goes on, under a darker sky.)
[name: Embalmer] North? Through there? Living folk go through now and then. Mind you come out the far side the same shape.
[name: Embalmer] (squinting at you) ...Huh. You don't show up right in it. Not wrong. Just thin. Like you've been through before.
(Under your collar, the scar is cool. For once, it's the glass that's warm.)
V135 = 1.
```
- **`OS_UNQUIET_ELECTOR`** (optional; promote the stub): an embalmer by the Center. "A dead Elector keeps walking out of his tomb-mirror to vote." The design stays as catalogued.
- Vigil's Center (771), the Wardens' Circular: Juno: "IS ANYONE ELSE'S MIRROR DOING THE WINGS THING." Kaito: "Yes. Ignore it." Then Celestine: "Do NOT ignore it."
Trainers: none in town.

## Map 760 — the Obsidian Barrows (`:INVERSE`)
Black glass tomb-mounds in rows, each with a mirror for a headstone. Above the Barrows, hanging upside down in the sky like Lucent's Speculum, is a **desert**: dunes, a caravan crawling along the underside of the clouds.
- A tomb-mirror shows the PC's reflection kneeling while the PC stands. Behind it, wedged in the frame: **Glassfall Sliver**.
- A caravan guide at a cairn: "That's Ossaria up there. The Bone Sands. When the Glass is thin you can see the caravans going home. Mine's the third camel. I'm not on it."
Trainers (Lv 58–59): a hex maniac, a medium, a pallbearer of Vigil (a mourner with Golurk).

## Map 761 — Spinefall Gorge (Waterfall)
A gorge cut through the Spinewall, the mirror-exit into Ossaria: after the falls the sky is right way up again and the air turns dry. Behind the falls (Waterfall, then a ledge): **Glassfall Sliver**.
- A fisher at the foot: "Water comes down this gorge out of the Glass and goes into Ossaria. Duneholt drank it for six hundred years. Now Duneholt's dry and the water still comes down. Ask yourself where it goes. I have. Nobody answers me either."
Trainers (Lv 59): a fisher, a black belt (training under the falls).

## Map 773 — the Vertebrae (`:MOUNTAIN`) up to Cragholm
A switchback road up a spine of rock with Cragholm's lift-towers at the top. Halfway up, a Meridian survey post: a white tent, a sunburst flag, and a drill-mast humming. A lineman with a clipboard: "Lattice-drill Nine. Kassan's lease. Everything under this mountain's Meridian's for a hundred years. ...Nobody told the mountain, mind."
Trainers (Lv 60): a worker (Meridian contractor), a hiker.

## Map 360 — Cragholm: **"Sit Down"** (autorun at the top lift-cage, V135 == 1 → 2)
```
(Cragholm. A canyon wall of lamplit galleries, one above another, linked by iron lift-cages that clank and sway on chains. Hundreds of little lamps, like a city built inside a lantern.)
(At the main lifts: Directorate guards in grey, Linesmen with clipboards. A hand-painted sign under a printed one. The printed one: MERIDIAN DEEP WORKS — AUTHORISED PERSONNEL. The painted one: MIND YOUR HEADS.)
(At the top cage, a stooped old man in a miner's hat with a lamp on it, smoking a clay pipe with enormous hands. A Directorate officer is talking at him.)
[name: Directorate Officer] —registered with the Deep Works office by sundown, Warden. Every miner. Every name.
[portrait: BASTIAN, neutral] Eh?
[name: Directorate Officer] (louder) EVERY NAME.
[portrait: BASTIAN, happy] Lovely weather for it.
(The officer gives up and stalks off. Bastian watches him go, then turns the lamp on his hat towards you.)
[portrait: BASTIAN, neutral] Ilsa sent you? Course she did. She sent word on a mirror, and the mirror sent it to me crooked, but I got the gist.
[portrait: BASTIAN, neutral] Sit down. No, there. That crate. I'm telling you about the crown.
(He opens his mouth. Shuts it. Looks at the guards on the lift.)
[portrait: BASTIAN, deadpan] ...Not here. The rock's got ears and so's that lot. Pip!
(A girl drops out of the lift-cage above on a rope, lands on the crate you were about to sit on, and doesn't fall off.)
[portrait: PIP, happy] Here! Is this them? The ferry one? You're shorter than on the screens. Everyone is. I'm Pip. I'm fourteen. I'm the fastest lamp-runner in Ossaria, and that's not bragging, there's a board.
[portrait: BASTIAN, neutral] Take them down. The long way. Not the lifts.
[portrait: PIP, smug] The long way's my favourite way. Keep up!
V135 = 2.
```
**Cragholm (360–362):** the Center (361), the Mart (362; Badge-13 stock plus **Field Seeds** and **Hard Stone**, per REVIEW.md's economy decision), the Rolls of Unearthing's board.
- **`OS_BONEWRIGHT`** (optional; promote the stub): Curator-Elect Nasrin Vael at the board, as catalogued.
- Townsfolk: a miner's wife: "Half the families down the seams aren't Ossarian. Isenmar folk off the Thaw. Well-folk off the western dunes. Nadir lot who ran from the raids. Bastian says a seam doesn't ask where you're from. The seam's never had to share its bread, though." A Linesman on a break: "Kassan sold them the mountain. Not the miners. They come with it. Like a chair."
Trainer (Lv 60): a gemcutter on the lift-landing (not the gym's).

## The deep seams: **the refuge** (Map 363, the Lift Galleries; then the lowest seam; V135 == 2 → 3)
The long way down: Pip leads the PC through a chain of ladders, a disused lift-shaft and a seam so low the PC crouches. *(A short follow-the-runner sequence: Pip waits at each landing and taps her foot.)* Below the Deep Works' lowest gallery, a wall of old timbers swings open on a counterweight.
```
(Beyond it, a long cavern lit by a hundred miners' lamps. Cots. Washing on lines strung between pit-props. Children. Someone playing a squeezebox badly. The smell of stew and wet stone.)
[portrait: PIP, neutral] Everyone the Accord and the sun-badge lot would rather didn't exist. Grandad collects them. Like stamps.
```
Who's here, in the order the PC meets them:
- **Larch**, at a miner's bench under a hooded lamp, in a borrowed coat, writing in a ledger. Odessa got her out of Skyreach on a skiff and up the canyon by night.
```
[portrait: LARCH, happy] There you are. Odessa said you'd be "along when you're along". She was right, which she'll be insufferable about.
[portrait: LARCH, neutral] You'll want to know what I've been doing. Hiding, mostly, and reading my own papers back to myself on the screens down here. They've cut it to pieces. I sound like a lunatic. I sound like a lunatic with excellent posture.
[portrait: LARCH, worried] One thing. Before anybody else gets to you, and they will try. If anyone from Meridian ever offers to "check you over", a Fellowship medical, a scan, a nice doctor with warm hands... no. Never, ever let them examine you. Not for any reason. Not even if I'm the reason.
[portrait: LARCH, neutral] Promise me you heard that. You don't have to say it. You just have to have heard it.
V135 = 3.
```
*(The GO_WILLING foreshadowing line; it must play before the badge case. 09 #14: the PC is what the Engine needs.)*
- **The Lantern Hollow**, in the far gallery:
  - `[if ROWAN_ALIVE]` **Rowan**, gaunt, in a blanket, a chain-gall on his wrist. He looks at the PC for a long time. "You broke a chain for me. I'm told I'm supposed to say something about debt. I'm too tired for debt. Sit, if you like."
  - `[if !ROWAN_ALIVE && TEO_SAVED]` **Teo**, leading now, too young for it, with Rowan's lantern: "He'd have known what to say to you. I don't. I just know where the bread is."
  - `[if !ROWAN_ALIVE && !TEO_SAVED]` **Wick** and **Thistle** share it, badly. Wick: "We lead by committee. The committee's two people who don't agree on anything. It's very Hollow."
  - **Thistle** (in every branch) is mending a rope, not looking at anyone. `[if standing(:HOLLOW) >= 3]` "You. Sit by me. Hold this end. Don't pull."
- **The field hospital:**
  - `[if CORVIN_FREED]` **Corvin**, mask round his neck: "You got me off a barge. I've been trying to work out how to pay that back. I've settled on 'keep people alive in a hole'. Will that do?" **Wenlow** waves with a bandage roll and drops it.
  - `[if !CORVIN_FREED]` **Wenlow**, alone, too cheerful: "Doctor Corvin's... away. I'm in charge! Of everything. I've read the book twice. The second time I understood about half."
- **The screens** (a salvaged Meridian set on a pit-prop, picking up three channels): **the Steamline**, steam-glass across Ossaria's western dunes, Isenmar's trenches on the Rimed Sands facing Ashkaar's Siege Camp, and between them a Meridian convoy with LATTICE DEFENCE SUPPLY painted on every wagon. A miner freezes the frame and points: the same crates going to both camps. A clerk among the refugees, who used to work the Duneholt depot, has the **manifests**: identical Prism lances, two buyers. RECEIVE: LANCE MANIFESTS. *(Evidence for Okoro, not a choice; 14_WAR_AND_BLESSING Ch14 row.)*
- **The bread line** (a flashpoint at the stew pot): an Ossarian well-woman and an Isenmar mother at the stew pot. "Your children eat our bread while your army drinks our wells." "My children didn't send the army." Bastian, from nowhere: "Seam doesn't ask. Seam doesn't care. Pot's big. Next."

### Day two: **Anja's column** (autorun on waking in 363's cot, V135 == 3 → 4)
```
(Morning, if it's morning; the lamps get turned up, so it must be. A commotion at the timber door.)
(A column of people in Rimeholt furs comes in out of the dark, frostbitten, carrying children, led by a broad woman with a white bone-flag on a pole, the one flag both armies let pass.)
[name: Zainab] Forty-one living. Six who weren't, by the Rimed Sands, and I carried those too, to the carters' ground. Zainab Darzi, Bone Chronicler. Somebody write that down, because I already did.
(Behind her, last, limping, pulling a sledge with two children asleep on it: Anja.)
[if ANJA_EXPOSED]
  [portrait: ANJA, sad] (she sees you. She looks at the floor, and keeps looking at it.)
  [portrait: ANJA, neutral] Rimeholt. Forty-one. I counted them twice. It's the only thing I'm still allowed to count.
[else]
  [portrait: ANJA, neutral] (she walks straight up to you, pulls off a mitten, and holds out her hand.) You let me say it myself. I've been saying it all the way here. To every one of them.
  (You shake it. Her hand is ice.)
[portrait: ANJA, angry] (at herself, not you) I sat on the readings. I sat on them and the sea came in. These are the ones the sea didn't take. That's my count now.
V135 = 4.
```
- She stays one night. When she goes, she goes **west**, to the front, to Skaldfast (`:war_prisoner`, Ch15–16): "Sigrun will want the readings I didn't sit on. All of them. Even the ones that make her look bad. Especially those."
- **Zainab** stays in the seams for a day, then goes back to the carters' camp on the Dry Tide (her hangout opens there; see Duneholt).

### **The meal** (touch, the long table, V135 == 4)
Date-bread and miners' stew at one long table: miners, refugees, Hollow, Larch, Pip, Anja, Bastian at the head carving with a knife bigger than Pip.
```
(Everybody at one table. It's too small. Nobody minds.)
[if ROWAN_ALIVE && JUNO visiting]
  (Juno came down on the night lift with Odessa's courier, to see him. She sits at the far end. Rowan sits at the near end. They don't speak.)
  (Halfway through, she passes the salt down the table without being asked. It gets to him. He uses it.)
[if !ROWAN_ALIVE && JUNO visiting]
  (Juno came down on the night lift. She sits next to Thistle, who was in the undercroft when they brought him up. Neither of them eats much. Thistle cuts Juno's bread for her, without asking, the way you would for a child.)
[portrait: BASTIAN, happy] Eat. All of you. The Deep Works can register my stew. Eh? What? Can't hear a thing.
```
*(`JUNO visiting` = `!flag(:JUNO_ESTRANGED)`. Otherwise Juno isn't here, and her chair is just a chair.)*

## Bastian's lamp-room: **Bastian's Account** (touch, Bastian, the evening of day two, V135 == 4 → 5)
```
(The lowest of the Lift Galleries. Bastian's lamp-room: a cot, a kettle and forty years of lamps. He closes the door, and then he closes a second door you didn't know was there.)
[portrait: BASTIAN, neutral] Ilsa says you went into your own head and came out with a church in it. Good. Then you'll know I'm not making this up.
[portrait: BASTIAN, neutral] I've seen three Festivals, two Sovereigns and one crown break. AF 290. I was carrying the Stone Plate in the procession. Wardens carry their Plates up the nave, you see, and then the Choir sings, and the Crown takes them. I was nearest the Choir loft.
[portrait: BASTIAN, sad] There was brass behind the loft that had no business in a church. Big brass, with dials. And men in white coats with little gold suns on their pockets, watching the dials.
(Under your collar, the scar stings: once, the way a cut stings when someone else says the word "cut".)
[portrait: BASTIAN, neutral] When the Crown cracked, the dials jumped. They weren't surprised.
[portrait: BASTIAN, angry] They were *pleased*.
[portrait: BASTIAN, sad] Then Valen said "find the child". And Morwen Vane threw herself over a little thing in a Choir ribbon. And the next week Morwen was ruined, and nobody ever asked me what I saw.
[portrait: BASTIAN, sad] I never told. I was afraid. I'm still afraid. Seventy-four, and I still sleep with a lamp lit.
[portrait: BASTIAN, neutral] I'm telling you anyway.
(He looks at your Bag, where the Secret Articles are, still sealed. He doesn't ask.)
[portrait: BASTIAN, deadpan] Ilsa's father's papers. Don't open them in here. Accord business in my lamp-room, and the ceiling falls in. That's a mining rule. I just made it up.
V135 = 5.
```
*(09 #24 eyewitness; the gold suns are the Meridian sunburst, which the Mindscape showed on the brass machines. Bastian says "um, where was I" three times in a longer cut of this story (Gym 13 Mastery, GYM_PUZZLES 374): amethyst, red, green, blue. The script keeps the short cut on the critical path. The long cut plays if the PC asks him to "tell it again" afterwards, and only that cut carries the colour words.)*

## Cragholm, the next morning: comedy scene Ch14, **"Selectively"** (autorun at the top lift-cage, V135 == 5 → 6)
The scene as written in `15_COMEDY.md` §4 (Bastian vs the Directorate officer; Pip and the ginger biscuits). After it:
```
[portrait: BASTIAN, neutral] (once the officer's gone, not deaf at all) Gym's open. Go and break your head on my lamps. I'll be along in ten minutes. Rock's patient. I'm only seventy-four.
V135 = 6.
```

## Gym 13 — the Lamp Galleries (370–374, `:CRYSTAL_CAVERN`)
As GYM_PUZZLES Gym 13: 370 Lamp Room (teach), 371 Prism Gallery (twist; the verified 3-turn solution), 372 Quarry (combine), 373 the arena, **374 Bastian's Seam** (Mastery; optional, the colour order from the long cut of his story). The lamp boy hints are **Pell** (Cragholm's own Pell; Ch11's technician was renamed Tage).
- **Pell at 370:** "Light goes straight till it's told otherwise. Same as me. Same as Mister Ore, except he's told otherwise all the time and doesn't hear it."
- **Gym 13 trainers (5):** Hiker ×2, Ruin Maniac, Worker, Gemcutter. Lv 59–62 (GYM_PUZZLES).

### 373 — the Warden Arena
```
[portrait: BASTIAN, happy] There you are. Nine minutes. I lost a bet with myself.
[portrait: BASTIAN, neutral] Light through crystal. Pretty. Darken it and the whole field turns, and then it's not pretty, it's mine.
[portrait: BASTIAN, deadpan] Rock's patient. Rock'll wait for you to make a mistake for a thousand years. I'm only seventy-four, so I'll wait about ten minutes.
BATTLE: Prismfall.gym_battle(pfm_gym(:LEADER_BASTIAN), double: false)
```
- **Mid-battle (Amber Mega Evolves):** "Rock's patient. So's this." `[bubble: BASTIAN, happy, sparkle]` *(The last Mega the PC faces without a ring. The VS plate reads PROSPECTOR above BASTIAN.)*
- **Win:**
```
[portrait: BASTIAN, happy] Flawless cut. Don't tell the cavern I said so. It sulks.
RECEIVE: the GEODE BADGE (badge 13). RECEIVE: TM76 STEALTH ROCK.
[portrait: BASTIAN, neutral] Come down to my lamp-room after. Not now. After. I want to wash my hands first. Old man's thing.
V135 = 7.
```
*(Badge name, proposed: the **Geode Badge**. `TELEMETRY_SABOTAGED` doesn't exist yet. The "did he notice?" beats start at badge 14.)*

## The Ring-Day (Map 363, Bastian's lamp-room; the hidden Trials quest **`OS_RING_DAY`**, V135 == 7 → 8)
**Canonical strings:** `plugins/Prismfall Trials/114_Quests_Megas.rb` `:ringday` (07_ACT_IV has the same text). Staging: Pip on a crate, Larch by the door with a book she isn't reading. Cutscene **RD-1** "The Ring Sings" (13_CUTSCENES) plays on the line "He drops the ring into your palm."
After the quest's last line, two additions (in this script, not the plugin):
```
(Larch has closed the book. She's looking at the ring the way she looked at the NULL scan, at the very beginning.)
[portrait: LARCH, neutral] (carefully, to nobody) Brann cut that ten years ago.
[portrait: BASTIAN, deadpan] Eh?
[portrait: LARCH, neutral] Nothing. An old woman doing sums.
V135 = 8.
```
*(Must not say "reset" or "Legend Plate" (09 #5/#6). Three clues now sit side by side: Brann's "Ten years back", Bastian's crown story an hour ago, and the ring that sings. Larch notices, says nothing, and we don't press it.)*
- **Hangout, Larch's bench (from V135 >= 8): the M5 Mentor Check** (optional; Gemini STORY_REMATCHES M5; `PROFESSOR_LARCH,Imelda,14`, single, `:CRYSTAL_CAVERN`, Lv 60–63, her **Electrium Z** on Magnezone "Coil-0"). "A ring nobody's ever heard sing, on a child nobody can scan. I'd like to see it *work* before somebody else does. Humour an old engineer." Win: "It works. Of course it works. I hate that it works." *(She has no ring: the Z-crystal is "Choir glass", which she kept from AF 281's line-work. Bastian said a Choir crystal answers the ring "too", and answers the person holding it, not a band.)*

## Larch's bench: **The Badge Case** (touch, Larch, V135 == 8 → 9; key event 2)
```
(Larch has your badge case open on the miner's bench under the hooded lamp. Thirteen badges in their slots. She's taken the lining out with a pen-knife and laid it flat.)
[portrait: LARCH, neutral] I've wanted to do this since Ferrow's Landing. The way it chords when you win. That's not a badge case. Badge cases don't have opinions.
(Inside the lining: a sliver of glass, rainbow-dark, no longer than a fingernail. Wired to it, a flat brass button with a sunburst stamped on the back.)
[portrait: LARCH, angry] Lattice-glass. And a transmitter.
[portrait: LARCH, neutral] Every badge you've won, it's recorded your... whatever it is in you. Resonating with that Warden's Plate. Thirteen Plates. And it's sent every one of them home.
[portrait: LARCH, angry] Voss isn't watching you. He's tuning you.
(She looks up at you. She's never looked old to you before.)
[portrait: LARCH, sad] They issued that case to every Fellowship child. I wrote the Fellowship's charter. I signed the form it came with.
\pf[PLAYER,neutral] (Your first words since the Mindscape.) What do we do with it?
[portrait: LARCH, neutral] "We." Good. Three ways. Choose. It's your case.
Switch S138 CH14_TELEMETRY_SCENE = ON.
```
```
> Smash it. (destroy)
  Script: pf_choose(:ch14_telemetry, :destroy)
  (You put a stone on it. Then you put the stone through it. The brass button cracks, the glass goes to sand.)
  [portrait: LARCH, neutral] He'll know by morning. He'll stop guessing and start hurrying. That's not nothing. That's not everything, either.
> Feed it lies. (sabotage)
  Script: pf_choose(:ch14_telemetry, :sabotage)
  (Larch puts the lining back with two new wires in it and a crumb of crystal from Bastian's seam where the glass was.)
  [portrait: LARCH, smug] It'll keep singing. Flat. A quarter-tone under every Plate, every badge, all the way to the Festival. He'll build his whole machine to a wrong note.
  [portrait: LARCH, worried] And every badge from here on, you'll wonder if he's heard it. So will I. Win them anyway.
> Leave it. (leave)
  Script: pf_choose(:ch14_telemetry, :leave)
  (You fold the lining back in. Larch watches you do it.)
  [portrait: LARCH, sad] ...All right. Your case. Your call. (A long pause.) I'd have liked to break something today. I'll find something else.
V135 = 9.
```
*(NARRATIVE_KEYS §4.2: `:destroy` VOSS−3 MERIDIAN−2; `:sabotage` → `TELEMETRY_SABOTAGED` (counts twice against ENGINE_CALIBRATED); `:leave` → `ENGINE_CALIBRATED` if the other safeguards fail, and Bastian's Plate condition fails ("you walked a Meridian beacon into his seams").)*

## **The Raid** (autorun on leaving Larch's bench, V135 == 9; no jokes until Thistle's last line)
```
(Somewhere above, a lift-cage comes down too fast. Then another. Then the lamps in the upper gallery go out, one after another, all the way down, like someone running a hand along them.)
[portrait: PIP, panic] (sliding down a rope) Grandad says they're on the lifts! Grey coats! All of them! He says get the doctor and the old lady and the... and the Hollow ones out the back seam, NOW.
[portrait: BASTIAN, angry] (from the gallery above, not deaf at all) NOBODY RUNS DOWN THE MAIN SHAFT. Pip, the back seam. You, child, with me.
Script: Prismfall.checkpoint
```
### The bench: **"Willing"** (GO_WILLING; autorun as the PC passes Larch's bench on the way to the shaft)
```
(At Larch's bench, a tall man in a pristine white coat, a black case at his feet, alone, unhurried, as if he'd been here for some time.)
[portrait: QUENT, neutral] Ah. You must be the young person with the unusual badge case. Doctor Percival Quent. Fellowship medical.
[portrait: QUENT, happy] Someone's interfered with your device. It may be dangerous, all that loose glass. I can remove it painlessly. Two minutes. And while you're here, a full Fellowship medical, since nobody seems to have given you one. You'd like to know what you are, surely?
> Let him look. (accept)
  [portrait: QUENT, happy] Sensible. Sit. This won't hurt at all.
  Script: Prismfall.game_over(:GO_WILLING)
> No. (refuse)
  [portrait: QUENT, neutral] (picking up the case) Of course. The offer stands. It always stands.
  (He walks away up the gallery between the Directorate troopers, and they make way for him without being told.)
```
*(GO_WILLING: NARRATIVE_KEYS §9, epitaph "The exam was painless, as promised. You've been asleep since. Meridian sends flowers." Foreshadowing: Larch's "Never, ever let them examine you" at V135 = 3. Quent doesn't fight here; his fight is Ch16/17.)*

### The lift-shaft: **Thistle holds** (touch at the shaft-head, critical; the tag battle)
```
(The main shaft. The refugees are going down the back seam in a line, children first, Pip counting them through. Above, lift-cages full of grey coats, coming down.)
(Thistle is standing at the shaft-head with her rope over her shoulder. She ties it off on a pit-prop, slowly, the way she ties everything.)
[portrait: THISTLE, neutral] I know where a thread will fall. This one falls here.
[if standing(:HOLLOW) >= 3]
  [portrait: THISTLE, happy] (to you, quickly, almost warm) You've been kind to my people when it cost you. I noticed. I notice everything that isn't said. Stand by me.
[else]
  [portrait: THISTLE, neutral] I don't owe you this. I'm doing it anyway. Stand there and don't get in my way.
(The first cage hits the landing. Two Directorate officers step out.)
Script: pbRegisterPartner(:HOLLOW_THISTLE, "Thistle", 14)
BATTLE: TrainerBattle.start(:MERIDIAN_DIRECTORATE, "Pruitt", :MERIDIAN_DIRECTORATE, "Vance") — double; the shaft-head (`:CAVE`); PC + Thistle.
(LOSE: whiteout to 361; the raid replays from the bench, the telemetry choice kept.)
(WIN:)
(Thistle cuts the cage's guide-rope with one stroke. It doesn't fall. It just won't come any lower.)
[portrait: THISTLE, neutral] Go. Larch went down the Darkglass side with the director's dogs after her. I'll hold this. I've held worse.
```
*(07_ACT_IV: Thistle defects openly, earlier and warmer at high Hollow Standing. Officers Pruitt and Vance are new (Mandate Officer class). Partner version 14: Thistle's Ch14 team, a new PBS block (3 mons, Lv 61–63, Ariados / Tsareena / Leavanny; she fights *with* the field, Sticky Web on a Cave).)*

### The Darkglass gallery: **Marchetti** (Map 784, the Darkglass Mine; touch, critical)
```
(The Darkglass Mine: a gallery of black crystal that drinks light. Larch has her back to the far wall. Between you and her, a Houndoom, and behind it, Director Helene Marchetti.)
[if choice(:ch13_fault) == :rowan]
  (She's on a cane. A steel brace from hip to ankle under the grey coat. She doesn't lean on it while she's looking at you.)
  [portrait: MARCHETTI, neutral] The undercroft. You looked at me and chose him. I've thought about that every day. I don't blame you. I'm just saying I've thought about it.
[if choice(:ch13_fault) == :marchetti]
  (She stands on her own. There's a white line of scar along her jaw that wasn't there in Lucent.)
  [portrait: MARCHETTI, neutral] I owe you a life. I know. I'm here anyway. Orders don't care what I owe.
[portrait: MARCHETTI, neutral] Professor Larch is a fugitive under the Mandate. You're obstructing. You're not under arrest. You're under —
[portrait: MARCHETTI, angry] — no. I'm not saying "protection" again. I've stopped believing it. Fight me or step aside.
(A Directorate trooper shoots out the gallery's work-lamps, one after another. The crystal goes dark, and in the dark, it starts to hum.)
BATTLE: TrainerBattle.start(:MERIDIAN_MARCHETTI, "Helene") — version 1; single; `:DARK_CRYSTAL`; her Mega Houndoom, and your ring.
(LOSE: whiteout to 361; the raid replays from the shaft, Thistle's battle kept.)
```
*(The first fight in which both sides can Mega Evolve, hours after the Ring-Day. Field: two light moves relight the crystals (WALKTHROUGH Ch14 field note).)*
**After the win: `:ch14_marchetti`**
```
[portrait: MARCHETTI, neutral] (Houndoom back in its ball. Her breathing loud in the dark.) Well. That's that.
[if has SPLITTER CASING || IRONREACH_EVIDENCE]
  > Show her the evidence. (show_evidence)
    Script: pf_choose(:ch14_marchetti, :show_evidence)
    (You hold it out. The Splitter casing from the Gale Post wreckage. [if IRONREACH_EVIDENCE] And the brass comm-box: MERIDIAN SPECIAL ACCOUNTS under its sunburst.)
    \pf[PLAYER,angry] Your own Special Accounts bombed Skyreach.
    (She takes it. She turns it over. She reads the stamp twice. Her face doesn't do anything at all.)
    [portrait: MARCHETTI, neutral] ...I was on those catwalks. I had people on those catwalks.
    (She goes very still. Then she hands it back.)
    [portrait: MARCHETTI, neutral] Keep that. Somewhere dry. (To the dark, louder:) Gallery's empty! Pull back to the lifts!
    (Her troopers go. She goes last. She doesn't look back.)
  > Say nothing. (none)
    Script: pf_choose(:ch14_marchetti, :none)
[if !(has SPLITTER CASING || IRONREACH_EVIDENCE)]
  Script: pf_choose(:ch14_marchetti, :none)
[if :none]
  [portrait: MARCHETTI, neutral] You're a good fighter in a bad cause, and I'm the reverse, and we're both very tired. (Louder:) Fall back. We'll come back with more lamps.
Switch S139 CH14_RAID_DONE = ON. V135 = 10.
```
*(NARRATIVE_KEYS: `:show_evidence` MERIDIAN−1 → `MARCHETTI_TURNED` (stands down at the hijack). If she was already turned at the Fault, `:show_evidence` still plays: now she knows *why* she'll stand down. Without evidence and without the Fault rescue, she stays loyal.)*

### Aftermath (autorun back in the refuge)
```
(The back seam. Everyone counted out and counted back in. Pip has counted them three times.)
[portrait: PIP, sad] All of them. Every one. And the grey coats got nobody.
[portrait: THISTLE, neutral] (sitting on a crate, a bandage round her hand, coiling the cut rope) I said I know where a thread will fall. I didn't say it wouldn't hurt.
[if ROWAN_ALIVE]
  [portrait: ROWAN, neutral] (to Thistle, quietly) That was well done. (To you:) The Directorate will be back. The Lantern Hollow moves tonight. West, to Gravenmoor. The dead don't inform on anyone.
[portrait: BASTIAN, neutral] They'll come back with more lamps. Good luck to them. I've got forty years of lamps.
[portrait: BASTIAN, sad] Go south, child. Duneholt. Sahar's well's gone dry, and the drill's found something hot under it, and she won't ask for help, so I'm asking for her. Then Gravenmoor. The dead have a lot to say this year.
QUEST LOG: "Eighteen Roads" — South to Duneholt. Sahar Ostrand's well is dry.
```

## Optional around Cragholm (from V135 >= 2; closed between the badge case and the raid's end)
- **Hangout, Pip at the lift-cages: `OS_TUNNEL_RELAY`** (new; Gemini SIDE_CAST E1). A lamp-run race through 363's ladders and lifts against Pip's board times; three heats. Beating all three gets the reward: **Glimmet "Lampwick"** (gift, Lv 34, Toxic Debris; "She glows when she's happy. She's always happy. It's exhausting.") plus Escape Ropes and a Star Piece. After that it's a repeatable relay for Hard Stone and Light Clay, and a spar double (`SIDE_LAMPRUNNER`, Pip, Lv 60–62: Glimmora / Boltund / Carbink). Pip keeps a tally of how many times Grandad "couldn't hear" the Directorate (Codex).
- **Geode Hollow (764/765, `:CRYSTAL_CAVERN`)**: a crystal cave off the Vertebrae. Trainers (Lv 61): a ruin maniac, a gemcutter. B1F: **Glassfall Sliver** in a geode. **The east seam (765):** among the wild Aron, an enormous one with a pearled lump on its back: **Lairon "Wart"** (static, Lv 58, Heavy Metal; holds a Hard Stone). Bastian, after the Ring-Day: "That's the big one. The others wear their stones like warts. That one wears it like a crown."
- **The Dreaming Quarter (768, `:BLEED`)**: a mining street on the canyon floor where the Fixed miners sleep, and their dreams play in the air as mirages: a wedding, a cave-in, a dog that died years ago. One mirage is a sleeping miner's open hand with a **Glassfall Sliver** in it, and it's real. In a hammock between two pit-props, a **Komala** (static, Lv 60, Comatose): "the only thing on the street that's asleep on purpose". *(The Fixed are Act II's Glassed sleepers; nobody in the Quarter knows how to wake them yet. Ch17 answers that.)*

## Transit: the Dry Tide (810) and the bone-carters' camp (930) → Duneholt
- **The Dry Tide**: a dead salt-shore where the Glass-sea once came in. Trainer (Lv 62): a camel-driver.
- **The bone-carters' camp (930, built)**: carts, a white bone-banner, a cook-fire. **Hangout, Zainab at the carters' fire** (from V135 >= 10).
  - **`OS_CARTERS_DEAD`** (new; given by **Elder Ossa**, whose lines are already on 930: "We carry out the dead the armies leave... If you walk where we can't, bring them home. One tally-stick each."). Zainab adds: "There are dead in the steam-glass west of Duneholt. The glass is too hot for wheels. You walk in the Glass. We don't care whose they were." Three remains markers at the Steamline's edge (the same map as Ch15's convoy, and it opens with it). Each returned tally-stick goes on the Tally-wall. The reward is the carters' **Spell Tag**, Zainab's spar (`SIDE_CARTER`, Lv 63: Runerigus / Cofagrigus / Mandibuzz / Palossand) and the Codex entry. *(Opens here; completes in Ch15.)*

## Duneholt at the war's edge (200–209, 214; V135 == 10 → 11)
```
(Duneholt. The Terrace Bazaar half-shuttered. A queue at the water-sellers' stall longer than the bazaar. Kassan's NOTICE OF NEUTRALITY pasted on the Sandgate over an older notice about the drilling, which is pasted over an even older one about the drilling.)
(The caravans are leaving by the east gate. One house at a time, camels roped nose to tail, the women of the caravan houses walking at the front, not looking back at the palace.)
Variable V109 DUNEHOLT_WELL = 1 (dry).
```
- **The Aquifer Quarter (204)**: the great well is a dry shaft, roped off. Hot air comes up out of it. A well-keeper: "Six hundred years, there was water at the bottom of that. Then Meridian put Drill Nine through the floor of it. Now there's something at the bottom that *breathes*." The Sinkwells (214): two more wells gone dry since Ch6.
- **Kassan, the Hall of Audience (206)** (touch; the palace guards wave the PC through: "The Elector's always pleased to see a celebrity."):
```
(A long hall of painted tiles. Prince-Elector Idris Kassan on a low divan, beautifully dressed, delighted. On one side, a Meridian paymaster with a strongbox. On the other, two quartermasters, one in Isenmar furs and one in Ashkaar black, standing as far apart as the room allows and not speaking to each other.)
[portrait: KASSAN, happy] The ferry child! Sit, sit. Have a date. Have two. I've been following your career. Everyone has. It's the only thing on the screens that isn't the war.
[portrait: KASSAN, smug] You'll have heard I've declared Ossaria neutral. Wise, everybody says. Then you'll have heard I've done something cleverer. Look.
(He unrolls a scroll with three seals on it: a whale, a forge-hammer and a sunburst.)
[portrait: KASSAN, happy] The Elector's Lease. The western dunes, let to the Isenmar crown, the Ashkaar crown and the Meridian Fellowship at once. Fifty years. Paid in advance. All three of them signed it without reading the other two.
[portrait: KASSAN, smug] The Bone Sands have buried every army that ever marched into them. I only charge for the plot.
(The Isenmar quartermaster looks at the Ashkaar quartermaster for the first time. Neither of them says anything.)
[portrait: KASSAN, neutral] (lightly, to you only) The well? Sahar's well? Regrettable. Meridian assures me the drill has found nothing but warm rock. Warm rock is very good for the economy.
V135 = 11.
```
*(14_WAR_AND_BLESSING Part B: Kassan rents a battlefield. The caravan houses ignore him from here on.)*
- **Gale Post (the Center): Marisol's letter** (a mail-call after Kassan; sets up War 2 for Ch15): "My sledges are in the bazaar, under the green awnings. Food or harpoon-guns, I haven't decided what goes on them, and I want you to walk them through the steam-glass into Skaldfast, because nobody shoots the Unimprinted. The caravan-mothers lead us out at first light. Come if you're coming. — M." *(`:war_convoy` itself is made at the start of Ch15; CHAPTER_BEATS density note.)*
- **Hangout, Sahar in the Dig Lab (209):** `OS_AMBER_AGAIN` (optional) is here. Sahar, sleeves rolled, sand in her hair: "Bastian sent you. He thinks I won't ask for help. He's right. I'm not asking. I'm *telling you* where the stairs are." The Stonesleep fossils come back here (see below).

## The Duneholt Undersands (783, `:DESERT`): **"Where the Well Went"** (`OS_UNDERSANDS`, **now critical**; V135 == 11)
Promote the stub to the critical path: Sahar's foreman and three diggers escort-climb down the dry well into the Undersands (Strength-boulder escort through collapsing galleries; the crew can fall behind, and the PC goes back for them). Trainers (Lv 63–64): a ruin maniac, a hiker, and a Meridian Deep Works engineer ("We were told it was warm rock. It's not warm rock. Warm rock doesn't have a pulse.").
- **The M7 rematch (optional; Gemini STORY_REMATCHES M7)** at the fossil stairwell above the glyph chamber: Sahar (`LEADER_SAHAR,Sahar,14`, single, `:DESERT`, Lv 64–67, Mega Steelix "Stratum"): "Nineteen years ago I buried a truth because I wasn't strong enough to stand in the sand. Show me you are." It's optional, and her sand turns the glyph chamber's field.
- **The glyph chamber**: a round hall of red stone, every inch cut with Unown glyphs, warm as an oven. A **Glassfall Sliver** sits in a glyph that's shaped like a sliver. In the middle, under the dry well's shaft, a hump of red rock rises and falls. It's breathing.

### **Boss: Groudon** (touch at the hump, critical; V135 == 11 → 12)
```
(The rock opens one eye. It's the size of a door, and the colour of the inside of a forge.)
(Sahar, beside you, has her hand on the wall, reading the glyphs by touch.)
[portrait: SAHAR, neutral] "The Year of Two Weathers." It's here. It's all here. It's been here the whole time, under the well, and I dug everywhere else.
(The Undersands shake. Sand pours from the ceiling. Groudon stands up, and the chamber is suddenly much smaller.)
BATTLE: Prismfall::Bosses — :GROUDON_UNDERSANDS (multi-bar, 3 bars, Lv 66; Drought; :DESERT, harsh sun from bar 2).
```
**Between bars (Sahar reads; story text, not dialogue boxes):**
- Bar 1 → 2: *"In the King's ninth year the red one and the blue one were woken out of the deep and the sea."*
- Bar 2 → 3: *"The King woke the red one and the blue one to remake the land. When they would not obey,"*
- Bar 3 broken: *"...he turned his eyes to heaven."*
```
(Groudon sags. The heat goes out of the chamber like a held breath going out of a chest.)
(It looks at you: a long look, as if it recognises something, and doesn't like it, and doesn't blame you for it either.)
(Then it lies down, and the red rock closes over it, and it sinks, slowly, into the floor of the Undersands, the way a stone sinks in deep water.)
(Silence. Then, very far off, a sound you haven't heard in Duneholt: water. A trickle. Somewhere down in the dark, running the right way.)
Switch S140 CH14_GROUDON_DONE = ON. Variable V109 DUNEHOLT_WELL = 2 (refilling). V135 = 12.
```
*(LOSE: whiteout to 201; the boss restarts at bar 1. 09 #15: Theodric's Year of Two Weathers. "He turned his eyes to heaven" seeds Rayquaza and the Sky Pillar.)*
```
(The well-head, an hour later. Duneholt has come out to look down it. A child drops a pebble. Everyone listens. A long way down: plink.)
(The crowd makes a sound you'll remember.)
(Sahar sits down in the dust by the well and looks west, towards the Steamline's haze on the horizon.)
[portrait: SAHAR, sad] The King woke the red one and the blue one. Somebody's going to bring the blue one here again, you know. The sand remembers the sea. It doesn't want it back.
[portrait: SAHAR, neutral] (getting up, dusting off) Right. That's enough feelings for one aquifer. The collapse has opened the old fossil beds east of town. Stonesleep. Bring me anything with teeth.
```
*(The first good news in an act. Ch11's Kyogre and this are the "red one and the blue one".)*

## Stonesleep (788, `:BLEED`; optional, from V135 >= 12)
The fossil beds the collapse exposed: a field of half-buried skeletons under a sky that flickers like a dream of the sea. Wild Pokémon are fossil species at Lv 63–66 (WALKTHROUGH). Rare fossils for the Dig Lab (the Bonewright pieces for `OS_BONEWRIGHT` too). A Dig Lab intern: "Professor Ostrand says don't touch anything that looks at you. Everything looks at you. I've stopped touching things."

## Hindmoor (781): **"Who'd Sponsor a Graveyard?"** (Chapter 14 close; autorun at the Antumbra border stones, V135 == 12 → 13)
Pip comes south with the PC as far as the border ("Grandad said see you to the edge. This is the edge. I checked.").
```
(Hindmoor: heather going grey, standing stones, the road north into Gravenmoor's fog. Wind.)
(A shadow goes over you. A big one. Overhead, low, an airship in Meridian white with a gold sunburst on the envelope, engines droning, heading north into the fog.)
(On its side, in letters a storey high: FELLOWSHIP CHAMPION SERIES — PROUDLY SPONSORING KESTREL VANE.)
[portrait: PIP, shocked] That's a sponsor ship.
[portrait: PIP, neutral] (watching it go into the fog, frowning) Who'd sponsor a *graveyard*?
(The fog closes behind it.)
V135 = 13. Variable V102 STORY_CHAPTER = 15.
QUEST LOG: "Eighteen Roads" — North to Gravenmoor. The dead have a lot to say this year. (First: Marisol's sledges, at first light, from Duneholt.)
```
*(Ch15 opens in Duneholt's bazaar with the War Convoy (`:war_convoy`), then north through the Jawbone Ridge to Gravenmoor. Kestrel's ship is K6's arrival.)*

---

## Map events needed (Chapter 14)

Only **930** is built. **[NEW]** = an event or map not in maps.json. V135 = **CH14_STEP** (design/FLAGS.md). Maps go through the three-pass workflow (design/MAPGEN.md, top).

**772 Yesterday's Road** (`:INVERSE`): mirror-written milestones counting down then up (decor; readable from the far side); the hiker on the halfway stone, the novice with the broom; 3 trainers.
**770 Vigil / 771 Center**: embalmers' town; **the Grave Glass** at the north gate (touch V135 0 → 1; the embalmer's "thin" line; a warm-glass screen tint); `OS_UNQUIET_ELECTOR` giver; the Circular.
**760 Obsidian Barrows** (`:INVERSE`): tomb-mirror headstones; the inverted desert in the sky (panorama); the kneeling-reflection mirror (a decor event that faces the opposite way) + **Sliver #1**; the caravan guide; 3 trainers.
**761 Spinefall Gorge**: the falls (Waterfall), the ledge behind with **Sliver #2**; the fisher; 2 trainers.
**773 The Vertebrae** (`:MOUNTAIN`): switchbacks; the Meridian survey post (tent, sunburst flag, drill-mast with a hum BGS); the lineman; 2 trainers.
**360 Cragholm / 361 Center / 362 Mart**: lamplit galleries and lift-cages (animated cages; MIND YOUR HEADS sign); Directorate guards at the main lift; **the arrival autorun** at the top cage (V135 1 → 2; Pip drops in on a rope: a jump move route); **"Selectively"** (V135 5 → 6) at the same cage; Mart Badge-13 stock + Field Seeds + Hard Stone; Nasrin (`OS_BONEWRIGHT`); townsfolk; 1 trainer.
**363 Lift Galleries + the deep seams [NEW interior, ~41×25]**: Pip's long-way route (ladders, a disused shaft, a crouch-seam); the timber counterweight door; the refuge cavern (cots, washing lines, pit-props, the squeezebox player); Larch's bench (V135 2 → 3; the badge case V135 8 → 9; the M5 spar after V135 >= 8); the Hollow gallery (Rowan / Teo / Wick, by flag; Thistle mending); the field hospital (Corvin + Wenlow, or Wenlow alone); **the screens** (the Steamline; the manifests clerk → LANCE MANIFESTS); the stew pot (the bread-line flashpoint); the long table (the meal, V135 == 4; Juno by `!JUNO_ESTRANGED`); the cot (the day-two autorun V135 3 → 4: Anja and Zainab's column); **Bastian's lamp-room** (the account V135 4 → 5; `OS_RING_DAY` V135 7 → 8 with RD-1); the shaft-head (the tag battle); Quent at the bench (GO_WILLING); Pip's lift-cages (`OS_TUNNEL_RELAY`).
**370–374 Gym 13**: as GYM_PUZZLES; Pell's hints; 5 trainers; Bastian (373); V135 = 7.
**764/765 Geode Hollow**: 2 trainers; **Sliver #3** (B1F geode); **Lairon "Wart"** static in the east seam (765).
**768 The Dreaming Quarter** (`:BLEED`): sleepers in doorways; mirage events (wedding, cave-in, a ghost dog) as picture/fog overlays that fade as the PC approaches; the sleeping miner's hand with **Sliver #4**; **Komala** static in the hammock.
**784/785 Darkglass Mine**: the gallery (`:DARK_CRYSTAL`); Larch against the far wall; Marchetti + Houndoom; the trooper shooting out lamps (a lamp event row turning off in sequence); `:ch14_marchetti`; S139.
**810 The Dry Tide**: salt flats; 1 trainer. **930 bone-carters' camp** (built): add Zainab at the fire (hangout; `OS_CARTERS_DEAD`; her spar).
**200–209, 214 Duneholt**: shuttered bazaar, the water queue, the notices on the Sandgate, caravans leaving by the east gate (looping move routes out of the map); 204 the dry well (V109 = 1; hot-air heat-shimmer); **206 Kassan** (V135 10 → 11; the Lease scroll as a picture); Gale Post at 201 (Marisol's letter); 209 Sahar (`OS_AMBER_AGAIN`, hangout).
**783 Duneholt Undersands** (`:DESERT`): the escort galleries (Strength boulders, collapse tiles); 3 trainers; the M7 stairwell (optional Sahar); **the glyph chamber** (Unown glyph walls, **Sliver #5**, the breathing hump: a move-route breathing loop); **Groudon** (`:GROUDON_UNDERSANDS`; S140; V109 = 2; V135 = 12); the well-head scene back at 204.
**788 Stonesleep** (`:BLEED`): fossil beds; Bonewright pieces; the intern.
**781 Hindmoor**: border stones; the airship (a large picture moving across the screen + shadow); Pip; V135 = 13, V102 = 15.

## Trainer roster (Ch14; 18 regular trainers; PBS blocks in 3 versions; levels before Badge 13 ≤ 63, after it ≤ 67)
| Map | Class (stock type) | Name | Lv | Team idea (field touch) |
|---|---|---|---|---|
| 772 | Hiker | Osgood | 57 | Golurk, Claydol (Inverse flips Ground's immunities: Levitate still holds) |
| 772 | Psychic | Novice Ilia | 57 | Gothitelle, Bronzong |
| 772 | Gravedigger *(Worker)* | Mott | 58 | Runerigus, Houndstone, Mudsdale |
| 760 | Hex Maniac | Severine | 58 | Mismagius, Banette, Polteageist |
| 760 | Medium *(Channeler)* | Agathe | 59 | Cofagrigus, Dusknoir |
| 760 | Pallbearer *(Hiker)* | Bram | 59 | Golurk, Palossand, Sandaconda |
| 761 | Fisherman | Teague | 59 | Golduck, Floatzel, Basculin |
| 761 | Black Belt | Kenji | 59 | Hitmonlee, Conkeldurr (Waterfall-trained: Focus Energy) |
| 773 | Worker | Deep Works Fitter Rhys | 60 | Excadrill, Probopass, Magnezone |
| 773 | Hiker | Marga | 60 | Rhydon, Garganacl |
| 360 | Gemcutter *(Lady)* | Opaline | 60 | Carbink, Klefki, Sableye (Crystal Cavern light moves) |
| 764 | Ruin Maniac | Fenwick | 61 | Claydol, Bronzong, Golett line |
| 765 | Gemcutter *(Lady)* | Beryl | 61 | Glimmora, Minior, Carbink |
| 810 | Camel Driver *(Backpacker)* | Hamid | 62 | Hippowdon, Mudsdale, Sandslash |
| 783 | Ruin Maniac | Tobiah | 63 | Unown ×2 (!), Cofagrigus, Sigilyph |
| 783 | Hiker | Dunstan | 63 | Krookodile, Flygon, Garganacl |
| 783 | Deep Works Engineer *(Worker)* | Engineer Lisle | 64 | Magnezone, Excadrill, Duraludon (sun + Steel) |
| **Gym 13** | Hiker ×2, Ruin Maniac, Worker, Gemcutter | (GYM_PUZZLES) | 59–62 | as GYM_PUZZLES |
**Story/optional fights (new PBS):** `MERIDIAN_DIRECTORATE` "Pruitt" and "Vance" (Ch14 versions, Lv 62–63, a Mightyena/Arcanine and a Magnezone/Corviknight pair); `HOLLOW_THISTLE` partner version 14; `PROFESSOR_LARCH,Imelda,14` (M5); `LEADER_SAHAR,Sahar,14` (M7); `SIDE_LAMPRUNNER` Pip; `SIDE_CARTER` Zainab. **Boss:** `:GROUDON_UNDERSANDS` (107_Boss_Groudon.rb).

**Items owner:** LANCE MANIFESTS (Key Item), the GEODE BADGE (proposed), TM76, MEGA RING + AGGRONITE (`OS_RING_DAY`), Glassfall Slivers #1–5 of the Ch14 allotment, the Spell Tag (`OS_CARTERS_DEAD`), Hard Stone/Light Clay (relay). **Portrait requests (art, to Gemini):** Zainab Darzi; Thistle `happy`; Marchetti with the brace (`neutral` variant) if art time allows, otherwise text only.
