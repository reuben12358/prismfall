# Script: Chapter 6 — "What the Sand Keeps" (the Brass Road, Duneholt, Gym 5, the Ossuary of Dunes; K3)

> **Final playable script** for Chapter 6, the first chapter of Act II. It covers the Act II opener in the Lowlight (Shattered) 608, the Brass Road north out of Lumen (612 the Meridian Mainline, 602 Candle Down, 603 the Highwold, 600 the Brass Dunes with 610 Copperdune and 604/605 the Static Tunnels, 601 the Rib Road, 613 Sunbleach Flats), Duneholt (200–209, 214) and its gym (210–213, Gym 5), then the Marrow Road 620, the Ossuary of Dunes 624/625 (K3) and Sinkfield 628. None of these maps is built; the list at the end is what to build from.
> Follows `story/24_SCRIPT_CH5.md`; conventions of `story/20_SCRIPT_CH0-2.md`.
> Sources: 05_ACT_II (the act opener and Ch6), 03_CAST (Sahar, Kestrel, Juno, Rook, Kassan), 09_MYSTERIES (#2, #2a, #7, #21, #24, #29), NARRATIVE_KEYS (`:ch6_drillsite`, `:ch6_kestrel_rumor`, GO_SINKFIELD), 14_WAR_AND_BLESSING (the Ch6 seed), 15_COMEDY (Ch6 "Lecture, Archaeological", adapted; the Ossaria bits), GYM_PUZZLES Gym 5, TRIALS_QUESTS (the Rolls of Unearthing, Ch6), BALANCE (K3, Sahar), `design/CHAPTER_BEATS.md`.

## Conventions
As in the earlier scripts. **Portrait cast here:** Juno, Rook, Sahar, Kestrel, Marchetti (only if met in Ch5's testimony; otherwise her officers are plain). **Plain:** Sona and the Octave, Nadim, the Dig Lab interns, the caravan-mothers, Directorate officers, every townsperson and trainer. Events call `Prismfall.gym_battle(pfm_gym(:LEADER_SAHAR), double: false)`.
**Counter:** V126 **CH6_STEP** (design/FLAGS.md): 0 leaving Lumen · 1 the Lowlight at dawn (Juno's goodbye) · 2 the Mandate checkpoint on the Mainline · 3 arrived in Duneholt · 4 the drill site and `:ch6_drillsite` · 5 Gym 5 won · 6 the Ossuary opened (Sahar's confession) · 7 the murals (S116) · 8 K3 (S117) · 9 Juno's letter (chapter closed).

## The chapter's key events (design/CHAPTER_BEATS.md)
1. **The Ossuary murals and Sahar's confession.** A dune-shift uncovers the door she sealed in AF 281 on Valen's order. Inside, the Gilded King, the two titans, the chain of eighteen locks and the city falling into the sea. Build-up: the warm ground, the "sleeping red giant", Sahar's three warnings, the drill site sinking the well. Payoff: the Duneholt Rubbing. Consequence: the Prismfall thread (Ch17), Sahar's Consent (by `:ch6_drillsite`), the war on the western dunes (her finger on the coastline).
2. **K3: Kestrel says the rumour out loud.** With his mother's veil from the lighthouse trunk in his hand. `:ch6_kestrel_rumor` decides how Ironreach hits him.
The Mandate's first arrests (the drill site) carry the chapter's middle: the Shatter's consequence, on screen, two weeks later.

---

# CHAPTER 6 — "What the Sand Keeps"

**Chapter start:** V101 = 2, V102 = 6, V126 = 0 (Interlude I's end). The PC wakes in the Lumen Pokémon Center.

## Map 608 — The Lowlight (Shattered), at dawn: the Act II opener (autorun on first entry, V126 == 0 → 1)
```
BGM: none. A wind-chime someone has hung on a glass washing line.
(Dawn in the Lowlight. Two weeks. The glass ring is still there under the Spire's foot, grey and silent. Round its edge, outside the Veil, a shrine has grown: soda cans, candles in jars, chalk on the stones. Twelve names, written over and over in twelve different hands.)
(At the Veil's edge, Mandate officers in white-and-gold stand by a new brass barrier. A sign on it: MERIDIAN SECURITY DIRECTORATE — BY MANDATE OF THE ACCORD — NO ENTRY.)
(Rook is sitting on the bottom step of the vault stair in a plain hooded jacket, no lights in it, no drone. He's holding a Fizzbolt he hasn't opened.)
[portrait: ROOK, sad] I'm not filming. I'm just sitting.
[name: Rook] I come down every night. The guards let me. I think they think I'm doing a segment.
[portrait: ROOK, neutral] Chat would say something. I don't know what chat would say. I haven't asked.
```
**DEX** (inspect his glass figure from inside the Veil; the PC can still walk in)
```
(You step through. The Directorate officers don't stop you. They don't know how to.)
(Dex is where he was: glass, mid-wave, his mouth open on a word. Someone outside the Veil has leaned a soda can against the shimmer as close to him as they could reach.)
(You stand with him. After a while you put your hand on his glass shoulder.)
SE: a single, very low note, from somewhere under your ribs.
(The glass is cold. And then, under your hand, it isn't. It's warm. Barely. Like a window with the sun on the other side.)
WAIT 60.
(You take your hand away. The warmth fades. Dex hasn't moved. Nothing has. But you felt it.)
```
*(09 #21, the Harmony seed for the Homecoming waking. No text says what it means. The Trials quest `ZE_LOWLIGHT_LAMPS` (Dex's Pichu at the shrine) runs from here: S164 DEX_SHRINE.)*
```
[name: Marlo] (lighting candles at the shrine, outside) You're the one who walks in. I saw you, that night.
[name: Marlo] Tell him— no. You can't tell him anything. ...Tell him anyway.
```
**Juno's goodbye** (at the top of the Lowlight stairs)
```
(Juno is waiting with her hatbox and a sack of seed packets. The curtain dress is gone; she's in her old flower-girl dress with the hem let down, and her eyes are red.)
[portrait: JUNO, sad] I'm not going home.
[portrait: JUNO, neutral] There's a doctor in Mirefen, down in Nadir. Dr Mott. He's got a whole ward of people turning to glass, slowly, and Uncle Rowan sends him seed stock every month for the medicine.
[name: Juno] I was going to send it by post this time. I'm not sending it by post. I'm taking it.
[portrait: JUNO, sad] I couldn't do anything for Dex. I can't even walk in there. But I can carry a sack.
> I'll come with you.
  [portrait: JUNO, happy] You can't, silly. You've got a badge to get. Duneholt's north, and Mirefen's down, and they're not letting anyone down the lifts any more.
  [portrait: JUNO, neutral] I'll find a way down. Verdancers always find the way down. It's up we're bad at.
> Be careful.
  [portrait: JUNO, neutral] I'm always careful. I'm careful about everything. It's very tiring.
> ...
  [portrait: JUNO, sad] I know. Me too.
[portrait: JUNO, happy] Write to me! Gale Post. "Juno, Mirefen, the one wearing a tree."
MOVE: Juno hugs you, hard and quick, and goes off along the Concourse toward the lift-shafts with the sack over her shoulder.
V126 = 1.
QUEST LOG: "Eighteen Roads" — Earn the fifth badge in Duneholt, up the Brass Road north (the Meridian Mainline out of the Concourse).
```

## Map 180 — Lumen City after the Shatter (state change; S115 on)
```
[name: Office Worker] They've put Mandate men on every lift down to Nadir. My cleaner lives down there. She hasn't been up in a week. The office is filthy and nobody's allowed to say why.
[name: Old Man] Gas lamps and smog. I said it was worse. I'd take it back now. I'd take it all back.
[name: Pin-seller] Anniversary pins, half price. ...Quarter price. ...Take one. Please. I can't look at them.
LIFT-GRILLE (inspect): A brass barrier over it now, and a Directorate seal. Someone has chalked a grey ring on the seal.
```

## Map 612 — The Meridian Mainline (`:MOUNTAIN`)
```
ROAD SIGN: THE MERIDIAN MAINLINE — The Brass Road. ↓ Lumen City · ↑ Candle Down & the Crown Road. Walk the service road. Do NOT walk the line.
(Zenith's first railway, running off the plateau's north lip on brass-and-iron trestles. Signal gantries clank. Trains go by full of crates stamped with the sunburst. You walk the service road beside the track.)
```
**EV "The Checkpoint"** (a Mandate barrier at the signal gantries; touch, V126 == 1 → 2)
```
(A brass barrier across the service road, a tent, a scanner plate on a post, and two officers in white-and-gold. A queue of drovers and pedlars waits with their hands out.)
[name: Directorate Officer] Mandate checkpoint. Papers and tint. Hand on the plate.
[name: Drover] Two weeks ago this was a road.
[name: Directorate Officer] It's still a road, sir. It's a road with a checkpoint on it.
MOVE: your turn. SE: chime... nothing. NULL.
[name: Directorate Officer] ...Hold on.
(She turns to a ledger on the tent pole and runs a finger down it. She stops.)
[if :ch5_lowlight_testimony == :someone_else]
  [name: Directorate Officer] You're flagged. By the Director herself. "Do not obstruct. Report movements." That's all it says.
  [name: Directorate Officer] So I'm not obstructing you. And I'm reporting that you went north. Have a nice trip.
[else]
  [name: Directorate Officer] You're on the Chair's guest list. Gala, Lumen. ...You were THERE?
  [name: Directorate Officer] Go on through. And — I'm sorry. About the Lowlight. My sister's on the Spire feeds. She was off that night. She's not been off since.
MOVE: the barrier swings up.
[name: Drover] (behind you) Oh, very nice. Very fair. Some of us have been here since six.
V126 = 2.
```
*Trainers on 612 (trainer designer): rail workers and Directorate cadets.*

## Map 602 — Candle Down (`:MEADOW`; the Crown Road, east)
```
ROAD SIGN: CANDLE DOWN — The Crown Road. ↙ Wallshadow Row · ↘ the Meridian Mainline · ↑ the Highwold. Light one for whoever you've lost.
(Open downs round the Crownwall's east face. Cairns of white stones every few hundred yards, each with a niche for a candle. Pilgrims walk the cairns.)
CAIRN (any; inspect): Twelve candles in the niche. Twelve on the next one. And the next.
[name: Pilgrim] News travels round the Crown Road faster than the Gale Post. Every cairn from here to Kingsmead's got twelve on it.
[name: Pilgrim] I didn't know any of them. I light them anyway. Somebody should be counting.
CAIRN, the big one at the gap: From here the Crownwall has one gap in it, a notch in the white, and through it, very far off, something glitters on the inside of the wall like frost on a window. [name: Old Pilgrim] That's the Scar. Where the Glassfall came down, ten years back. Forty of them, in there. Nobody lights candles for those. The Accord says it's "not encouraged".
[name: Coaching-inn Keeper] (the east junction's inn) Tea, bed, a horse if you've money. The road north's clear. The road east's full of Ashkaar envoys going to see the Sovereign about the Shatter. They've been very polite. It's frightening.
```
*(The Glassfall Scar is seen properly in Ch13 from Kingsmead; here it's only a glitter through the gap.)*

## Map 603 — The Highwold (`:MEADOW`)
```
ROAD SIGN: THE HIGHWOLD — The Crown Road, north. ↓ Candle Down · → the Brass Dunes & Ossaria · ← Kingsmead (closed).
(Chalk downland north of the Crownwall, all skylarks and sheep. The Wold Stones stand in a ring on the top.)
WOLD STONES (inspect): Eighteen standing stones in a ring, and in the middle a flat one with nothing carved on it. The eighteen are worn smooth by three hundred years of hands. The middle one isn't. Nobody touches the middle one.
[name: Shepherd] Sheep won't graze inside the ring. Never have. Not even the stupid ones, and I've some very stupid ones.
[name: Dew-pond Girl] The dew-pond fills itself every morning and nobody knows how. Grandad says the wold sweats. I say that's disgusting.
```

## Map 600 — The Brass Dunes (borderland C) and Map 610 — Copperdune
```
ROAD SIGN: THE BRASS DUNES — ← the Highwold (Elowen) · → Copperdune & the Rib Road (Ossaria). The railway ends here. Ask the sand why.
(Where the downs give out, the sand starts. The Meridian railway runs out into it on a brass viaduct and simply stops, its last span hanging over a dune with nothing under it. Beyond, fossil ribs as big as houses stick up out of the sand.)
[name: Rail Ganger] They laid it to Duneholt. Three times. The sand moved the dunes over it three times. Meridian says they'll lay it a fourth. The sand says nothing. The sand doesn't have to.
COPPERDUNE (610): a rail-junction caravanserai round the broken viaduct; Ossarian bone-traders and a Zenith freight depot.
[name: Bone-trader] Prices in bones, stranger. A Potion's two bones. A Super's five. A bone's a bone, don't ask me which.
[name: Freight Clerk] Meridian deep-drill crews come through here every week, north, with drill-heads the size of houses. They go out shiny and come back scraped.
[name: Caravan Child] My mum says the ground under Duneholt's warm. She says the sleeping red giant's turning over in his bed. I said, is he going to get up? She said not while I'm talking.
```
*Trials on 610: The Riddle Trader (OS_RIDDLE_CARAVAN), Tomb Freight (OS_TOMB_FREIGHT). Copperdune's tablet rack (the Rolls of Unearthing).*

## Maps 604/605 — The Static Tunnels (`:CAVE`; dark: Flash)
```
(The old tram tunnels Meridian dug under the dunes before the sand ate the railway. Dead tram cars, live cables, Joltik in the dark.)
TRAM CAR No. 9 (inspect): Destination board: DUNEHOLT. Underneath someone has scratched: "EVENTUALLY."
```

## Map 601 — The Rib Road (`:DESERT`; sandstorm) and Map 613 — Sunbleach Flats (`:DESERT`)
```
ROAD SIGN: THE RIB ROAD — Ossaria, the Bone Sands. ↓ the Static Tunnels · ↑ Sunbleach Flats & Duneholt. Keep to the ribs in a sandstorm.
(A red canyon road between the ribs of something that died before the Prismfall. Sandstorms come down it in walls.)
[name: Caravan Guide] Ribs on your left, ribs on your right. You can't get lost on the Rib Road. People do it every week.
ROAD SIGN (613): SUNBLEACH FLATS — ↓ the Rib Road · ↑ DUNEHOLT (the Sandgate). Linen, bones and everything else go white here in a season.
(White flats under a white sky. Frames of linen bleaching in rows, and Duneholt's Sandgate on the horizon, cut into the canyon mouth.)
[name: Linen-maker] We bleach Briarwick's cloth for the Zenith market. It goes white in a week here. So do you, if you stand still.
```
*Trials off 613: The Noon Bell (OS_OCTAVE_NOON_BELL), Sona of the Octave at the Temple of the Noon Sun (Octave 4 of 8; see the map list for its map ID).*

## Duneholt (200–209, 214; the Bone Sands)

### Map 203 — the Sandgate: arrival (autorun, V126 == 2 → 3)
```
(A canyon mouth walled across in sandstone, with gate-towers carved straight out of the cliff. Through the gate: terraces of sandstone houses climbing the canyon's sides round an enormous round well, the width of a town square, going down and down.)
NOTICE (on the gate): "By license of His Excellency Idris Kassan, Prince-Elector of Ossaria, the Concord deep-works are a protected enterprise. Interference is an offence against the Elector."
NOTICE (pasted over a corner of it, newer): "BY MANDATE OF THE ACCORD: MERIDIAN SECURITY DIRECTORATE OPERATES IN DUNEHOLT FOR THE PROTECTION OF LATTICE ASSETS."
[name: Caravan-mother] (spitting at the notices) Two notices. One from a man we elected for life and can't get rid of. One from a company we never elected at all.
[name: Caravan-mother] And the western wells have changed hands twice this year. Both times the new owners had an accent.
[name: Gate Guard] Welcome to Duneholt. Water's a bone a cup. It was free last year.
QUEST LOG: "Eighteen Roads" — Earn the fifth badge at the Dig, Duneholt's gym.
V126 = 3.
```
*(09 #29 and 14_WAR's Ch6 seed: "the new owners had an accent".)*

### Map 200 — the Terrace Bazaar · 201 PC · 202 Mart
```
[name: Spice-seller] The well drops a rung a week. My grandfather's name's on the third rung from the top, where he carved it as a boy. You need a rope to see it now.
[name: Water-seller] A bone a cup! Two for a cold one! The cold ones come from the deep-works pipe, and don't ask what they did to get it cold.
[name: Old Digger] The desert keeps everything. My wife used to say that. She'd lose her keys and say "the desert's got them". It never gave them back.
[name: Child] The ground's warm. Put your hand on it. See? Mum says the red giant's dreaming. I think he's having a bad one.
201 GALE POST: "Duneholt: drink water. Not their water. Bottled. Lecture Six is being written in the dark because the Mandate has rationed my lamp-oil. — I.L." (Received: KELP TEA BAG. "Five.")
```
*(Lecture numbers: Lecture Three was in Ebbmouth; Four and Five went by post in between. Larch's count is her own.)*

### Map 209 — Sahar's Dig Lab: Sahar (first meeting)
```
(A long room cut into the canyon wall, crowded with bones, crates, rubbings and three exhausted interns. At the back, a woman in a sand-coloured keffiyeh and wire spectacles is brushing dust off a skull the size of a cart, one stroke at a time.)
[portrait: SAHAR, neutral] Don't come any closer. You'll breathe on it.
[portrait: SAHAR, neutral] ...You're the challenger. The Lumen one. The one who walks in the glass. Everyone's heard.
[name: Sahar] Sahar Ostrand. I keep the Dig, and the Earth Plate, and a well that's falling into itself a rung a week while a man in a palace sells the water underneath it.
[portrait: SAHAR, deadpan] You'll have read his notice. He has a lovely hand. He should have been a calligrapher. We'd all be happier.
[portrait: SAHAR, neutral] One thing, before you go anywhere in Ossaria. Walk the bones, never the sand. Where there's a rib or a road of bone, walk on it. Where there's only sand, don't. The desert keeps everything.
[name: Sahar] It just doesn't keep it where you left it.
```
*(Warning 1 of 3 for GO_SINKFIELD.)*
*Trials in 209: Kevin (OS_KEVIN); the Hall of Unearthing board. The fossil revival service opens here (WORLD.md: "Fossil revival at Lumen Fossil Lab (Act II)" is the other site).*

### Map 204 — the Aquifer Quarter: **EV "The Deep-works"** → **CHOICE `:ch6_drillsite`** (autorun the first time the PC enters 204 after meeting Sahar; V126 == 3 → 4)
```
(The great well. Terraces of houses round it, caravanserai, washing, goats. On the far side, a Meridian deep-works: a brass derrick over a shaft beside the well, a fence, and a pipe running down into the dark.)
(As you come to the rail, the ground shakes. Under your feet, very deep, something shifts its weight. The water at the bottom of the well slops against the stone.)
SE: a heavy WHUMP from the deep-works. A gout of sand and steam from the shaft. The derrick leans.
(Out of the shaft come Pokémon: three Drilbur and an Excadrill, scrabbling up the shaft's side and out onto the terrace. Each one has a brass collar round its neck with a sunburst on it, and a cable trailing from the collar back down the shaft.)
[name: Meridian Foreman] The cores! The CORES are loose! Somebody's cut the collars—
(Grey cowls at the fence. Bark masks with sad faces. Hollow. They're cutting the cables, one by one, and the caravan children of the Quarter are running out to help them, laughing, herding the freed Drilbur away from the shaft toward the Sandgate and the open dunes.)
[name: Bereaved] Go on! Go on, you're free, GO!
[name: Caravan Boy] This way! This way, little one!
(And then the white-and-gold. A Directorate squad comes down the terrace steps at a run.)
[name: Directorate Sergeant] By Mandate of the Accord! Everyone STOP! Those are Meridian assets!
[name: Directorate Sergeant] Those children are aiding saboteurs. Take them.
(An officer grabs the caravan boy by the arm. The boy's mother screams from a terrace above. The Excadrill, collar still on, plants itself in front of the children and bares its claws.)
[name: Bereaved] (to you, across the terrace) You! The one from the Lowlight! Help us get them into the dunes!
[name: Directorate Sergeant] (to you) You! Guest of the Chair! Help us secure the site!
```
```
> Help the Hollow get the freed Pokémon into the dunes. (hollow)
  Script: pf_choose(:ch6_drillsite, :hollow)
  BATTLE: MERIDIAN_DIRECTORATE "Sergeant" (Duneholt version; the game's first Directorate battle; Lv per BALANCE for the segment before Gym 5). Field: Desert.
  (WIN:) [name: Directorate Sergeant] This is obstruction of the Mandate. You'll be in a report by tonight.
  (The Hollow and the children run the Drilbur out through the Sandgate. The Excadrill goes last, looks back once at the shaft, and digs.)
  [name: Bereaved] The red giant thanks you. So do we. ...So does Ochre, the big one. That was her name, before they put a number on her.
  (The sergeant lets the caravan boy go. Nobody's told her what else to do.)
> Help the Directorate secure the site. (directorate)
  Script: pf_choose(:ch6_drillsite, :directorate)
  BATTLE: HOLLOW_GRUNT_M "Bereaved" (Duneholt version). Field: Desert.
  (WIN:) (The Hollow scatter over the terrace walls. Meridian handlers loop new cables onto the Drilbur's collars and lead them back to the shaft. The Excadrill fights all the way down.)
  [name: Directorate Sergeant] Good work. Very good work. The Directorate remembers its friends.
  (Received: MANDATE PASS.) ITEM DESCRIPTION: "A brass card with the Directorate's seal. 'The bearer has assisted the Mandate. Extend every courtesy.' It's warm, as if somebody's still holding it."
  (They take the caravan boy anyway. His mother doesn't scream this time. She just watches you.)
> Shout for Sahar. (sanctuary)
  Script: pf_choose(:ch6_drillsite, :sanctuary)
  (You shout her name. It goes up the terraces and round the well and comes back to you three times.)
  MOVE: Sahar comes down the terrace stairs, not fast, with sand on her sleeves and her spectacles pushed up on her head. Everyone stops.
  [portrait: SAHAR, angry] Sergeant. Let go of that child.
  [name: Directorate Sergeant] Warden, with respect, the Mandate—
  [portrait: SAHAR, neutral] The Mandate is two weeks old. The Warden's right of sanctuary is two hundred and ninety-six years old. "Any child of the city who stands within sight of its Plate stands under its Warden." The Earth Plate is in that well. That child is in sight of it.
  [name: Sahar] Under the Concordance, Sergeant. Read it sometime. It's short. I'll lend you mine.
  (The sergeant looks at her squad. Her squad looks at the well. She lets go.)
  [name: Directorate Sergeant] This goes in my report.
  [portrait: SAHAR, deadpan] Spell my name right. It has an H in it nobody hears.
  (The Hollow are gone. The Drilbur are gone, and the Excadrill. The children stay where they are, very close to Sahar.)
(All:)
[portrait: SAHAR, sad] *(looking down the well)* It dropped again. Did you feel it? A whole rung, just now.
[name: Sahar] They put collars on diggers and sent them down to drink my well for a man in Lumen. And now the Hollow have let them go, and the shaft's open, and the water will run down it like a drain.
[portrait: SAHAR, neutral] Come to the Dig when you're ready. I'd like to hit something that's allowed to hit back.
V126 = 4.
```
*(Long-term: `:directorate` costs Sahar's Consent in Act V; `:hollow` brings Directorate ambushes in Ch7; `:sanctuary` gives Accord Standing. The Mandate Pass opens checkpoints later.)*

### Map 214 — the Sinkwells (slum) and the Elector's Palace (205–207, closed)
```
[name: Sinkwells Woman] Our well went in last month. The whole street went down two feet in a night. We're the lucky ones; we're still above it.
[name: Water-carrier] Something in the Sinkfield's been taking our Pokémon off the carrying-sledges. Something flat. It grins. (Trials, Ch7: OS_SINKFIELD.)
PALACE GATE (205): [name: Palace Guard] His Excellency is not receiving. His Excellency is in Lumen, receiving.
MURAL GALLERY DOOR (207): CLOSED FOR RESTORATION BY ORDER OF HIS EXCELLENCY. (The door is new. The lock is newer.)
NECROPOLIS OF THE ELECTORS (208): Rock-cut tombs in the canyon wall. The road through them goes out to the Marrow Road and the Ossuary. [name: Tomb-keeper] The Electors are buried facing the dunes. So they can see who's coming. Lately they've seen a lot of drill-heads.
```

## Maps 210–213 — the Dig (Gym 5; GYM_PUZZLES Gym 5)
```
[name: Sahar's Aide] Everyone tries the door. The door's painted on. The way in is down.
[name: Gym Guide] The Dig: Ground-types on the Desert field. Water, Grass and Ice dig in. Electric doesn't, ever, at all.
[name: Gym Guide] Sun hardens and shade sinks. The mirrors pick which lanes are in the sun. Falling isn't failing in here. Sahar says falling's how you find the second floor.
[name: Aide Nadim] (hints, T0) Sahar says the dig taught her more than the dunes ever did. / Lane c's mirror is on the east terrace. Fall into c and see where it takes you. / (the solution)
```
### 213 — the Warden Arena: Sahar
```
(The arena at the bottom of the dig: a pit of sand under a shaft of sunlight, the walls lined with labelled bones. Sahar stands in the light with a Claydol drifting at her shoulder. She coughs, once, into her sleeve.)
[if :ch6_drillsite == :sanctuary]
  [portrait: SAHAR, neutral] You shouted my name across the well. Nobody's shouted my name since I was a girl. It was very loud. Thank you.
[if :ch6_drillsite == :hollow]
  [portrait: SAHAR, neutral] You let the Hollow take Meridian's diggers into my dunes. I've been told to be angry about it. I'm working on it.
[if :ch6_drillsite == :directorate]
  [portrait: SAHAR, neutral] You helped them put the collars back on. I saw. I'm not going to say anything about it. The sand will.
(All:)
[portrait: SAHAR, neutral] The desert keeps everything. It just doesn't keep it where you left it.
[portrait: SAHAR, deadpan] Patience is a Ground-type's whole art. I'm fifty-eight and I have a cough. Let's see who runs out first.
Script: Prismfall.gym_battle(pfm_gym(:LEADER_SAHAR), double: false)     # LEADER_SAHAR, :DESERT, cap 31, single
(When her ace enters:) [portrait: SAHAR, neutral] Effigy. We've dug up older things than this one.
(LOSE: whiteout. Sahar on retry: "Again. Good. The second dig always finds more.")
(WIN:)
[portrait: SAHAR, shocked] ...
[portrait: SAHAR, neutral] Well. You found the bottom. Most people stop one layer short.
(Received: the SANDGLASS BADGE.)
(SE: the case's five notes, one after another and then together. The light along its seams is steadier now.)
[portrait: SAHAR, neutral] It sings. ...Of course it does. Everything you carry is strange, isn't it.
(Received: TM83 BULLDOZE.)
[portrait: SAHAR, neutral] Bulldoze. Shake the ground, slow whatever's standing on it. And that badge means Pokémon up to level thirty-five will heed you. My excavators will teach yours Strength. They've been waiting for an excuse.
V126 = 5.
```
*Strength (HM04) from the excavators at the gym's door after the badge (WORLD §4).*

## Map 620 — The Marrow Road: **EV "The Door in the Skull"** (autorun the first time past the dig terraces after Gym 5; V126 == 5 → 6)
```
ROAD SIGN: THE MARROW ROAD — Ossaria, the deep desert. ← Duneholt (the Necropolis) · → the Kneeling Stones. Walk the bones.
(Deep desert. Dig terraces cut into the dune faces. At the end of the terraces a skull lies half out of the sand, a skull the size of a house, and in the last night's dune-shift the sand has slid off its brow and uncovered a doorway carved into the bone: a square of dark with a lintel of glyphs.)
(Sahar is already there, with two diggers and a lamp. She's staring at the door. She has gone very pale.)
[portrait: SAHAR, shocked] ...
[portrait: SAHAR, sad] I know this door.
[name: Sahar] AF 281. I was thirty-nine. My team took four months and a Claydol to open it. Nine of us. I was so proud I couldn't sleep.
[portrait: SAHAR, neutral] I made rubbings. I wrote a report. I sent it to the Sovereign, because that's what you do when you find something that changes the history of the world. You tell the Accord.
[portrait: SAHAR, sad] He came himself. Valen. He walked through it with a lamp, all the way to the end, alone. And when he came out he said, "Seal it, Sahar. For the realm."
[name: Sahar] So we sealed it. I burned the rubbings. I told my team we'd found a collapsed granary. Two of them still don't speak to me.
[portrait: SAHAR, neutral] I buried the truth once because I was told to. The sand has dug it up.
[portrait: SAHAR, deadpan] I'd rather not argue with sand twice.
[name: Sahar] Walk the bones in there, the way I told you. The floor's older than the rules about floors. Come on.
V126 = 6.
```
*(Warning 2 of 3: "Walk the bones".)*

## Maps 624/625 — The Ossuary of Dunes (Unown ruins; Strength boulders; puzzles per the puzzle engineer)
```
(Inside the skull: a hall cut into bone and sandstone, running down. Strength boulders choke the side passages. In the walls, Unown drift like fish in a tank, in and out of the stone.)
FIELD NOTES pop-up: "THE OSSUARY OF DUNES — CAVE. Unown in the walls. They aren't hiding. They're the words." (Larch, in the margin: "Copy everything. Twice.")
[name: Sahar] The Unown are the inscription. They move. That's why nobody could read it, before. You have to wait for the sentence to come round.
```
**The four murals** (one inspect event each, in the order the hall reaches them; Sahar comments on each)
```
MURAL 1: A king in gold, on a throne under a sun, with his arms raised. Below him, his city: towers and domes and a harbour full of ships. His face has been scratched out, very carefully, by someone with a chisel and a lot of time.
[portrait: SAHAR, neutral] A golden king. There's only one golden king in the old songs. Nobody sings that verse any more.

MURAL 2: Two titans tearing at the land: one red, rising out of the earth with fire in its back; one blue, rising out of the sea with the tide in its arms. Between them, the king's armies, very small, holding chains.
[portrait: SAHAR, neutral] The Year of Two Weathers. The song says the sky and the earth went to war. This says somebody started it.
(Sahar steps closer and traces the coastline behind the two titans with one finger, very slowly.)
[portrait: SAHAR, sad] That's our western dunes. Before the Dry Tide was dry. The sea came that far once.

MURAL 3: A great beast with a ring of eighteen lights round its body, radiant, enormous, and round it a chain: eighteen golden locks, one on each light. The king's tiny figure holds the end of the chain.
[portrait: SAHAR, shocked] ...Eighteen locks. One for each.
[name: Sahar] He didn't pray to it. He tried to lock it up.

MURAL 4: The beast breaking apart. The eighteen lights falling out of it like rain, each one a different colour. Under them, the golden city tipping into the sea, towers first.
[portrait: SAHAR, neutral] And the lights fell. Eighteen of them. Onto all of us.
[portrait: SAHAR, sad] And the city went into the sea, and three hundred years later we built Zenith on its roof and called it progress.
```
```
(Sahar takes a sheet of paper and a block of red wax from her satchel and rubs the third mural, the chain, very fast, with her mouth set.)
(Received: DUNEHOLT RUBBING.) ITEM DESCRIPTION: "A wax rubbing of a chain of eighteen locks round a beast of eighteen lights. Signed in the corner, small: S.O., AF 300. And under it, smaller: AF 281."
[portrait: SAHAR, neutral] I made two. Keep yours. I burned the first one I ever made; I'm not burning a second.
Switch S116 CH6_OSSUARY_DONE = ON. V126 = 7.
```
*(09 #7: the first concrete clue. Nobody names Arceus, the Gilded King's family, the Legend Plate or the Crown.)*
**Optional guardian** (the deepest chamber, 625 the Script Vault): the Unown-swarm "glyph" formation, multi-bar (BOSSES.md), rewards an Unown and the UNOWN REPORT, as 05_ACT_II says. The Spiritomb static and the Odd Keystone stay as maps.json lists.

## Map 620 — the Ossuary's mouth: comedy scene Ch6, "Lecture, Archaeological" (adapted), then **K3**
*15_COMEDY's version has Kestrel mention a pit bracket, which is Ch9; the lines below keep the beat (Sahar's deadpan, Kestrel's smug ambush) and fix the timeline.*
```
(Outside, in the evening light. Sahar is looking at the inner seal-stone you came out past, now lying flat on the bone floor.)
[portrait: SAHAR, neutral] The seal on that inner door was three hundred years old.
[portrait: SAHAR, neutral] It took a team of nine and a Claydol four months to shift it in AF 281.
[portrait: SAHAR, deadpan] You leaned on it.
> It was loose.
  [portrait: SAHAR, deadpan] It was not loose. Things are not "loose" around you. Things give up.
> I was tired.
  [portrait: SAHAR, deadpan] You were tired, and a three-hundred-year-old seal fell over. I'll put that in the report. "The challenger was tired."
> ...
  [portrait: SAHAR, deadpan] Don't do the silence at me. I'm an archaeologist. I've been stared at by better skulls than you.
(A voice from the top of the skull.)
[portrait: KESTREL, smug] Told you. Things give up around them. Rivers. Plates. Me. Twice.
[portrait: SAHAR, shocked] ...Twice?
[portrait: KESTREL, deadpan] Don't.
```
**EV "Kestrel K3"**
```
MOVE: Kestrel drops down off the skull's brow onto the sand in front of you. He's thinner. The black coat is dusty to the knee. Round his neck, under the coat, something black and lace.
[portrait: KESTREL, neutral] I saw them. Over your shoulder. The king and the chain. I was in there before you, in the dark. I couldn't read it till you brought the lamp.
[name: Kestrel] I left the lighthouse the night of the Lowlight and I've been on the Hollow's trail ever since. They've got a cell out here. They came through Duneholt last week asking about old doors.
[portrait: KESTREL, angry] And everywhere I go there's you. In front of me. Getting there first. Leaning on things.
[portrait: KESTREL, neutral] Fight me. I need to know if I'm getting closer.
Script: Prismfall.rival_battle(:RIVAL_KESTREL, "Kestrel", 3)     # K3; version 30 + starter slot; field :DESERT (620)
(When Honedge's line enters, now a Doublade:) [portrait: KESTREL, neutral] Both blades, Morwen. Both.
(LOSE: whiteout to the Duneholt Pokémon Center. Kestrel on retry: "Again. I'm not done being right.")
(WIN:)
[portrait: KESTREL, shocked] ...
[portrait: KESTREL, sad] No. Not closer.
(He sits down on a rib of bone with his back to the skull. After a while he takes the lace out from under his coat: a black veil, with a ghost-lantern stitched in silver at the hem.)
[portrait: KESTREL, neutral] Gran's trunk. It was hers. Her Warden's veil. Gran kept it in a trunk that wasn't even locked, for six years, and never said.
[portrait: KESTREL, angry] Everyone keeps telling me to let it go. My mother had a seat, and a Plate, and a city that loved her. Then one night she had nothing. Let WHAT go?
[name: Kestrel] They say she died in exile. Of the wilting. They sent a box. Nobody saw a body. Nobody in Gravenmoor will say where she's buried.
[portrait: KESTREL, neutral] And now there's a man in a mask who talks like her, and the whole realm's saying it. Every inn from here to Ebbmouth. The Mourner's Morwen Vane. She didn't die. She was made to disappear, and she came back.
[portrait: KESTREL, sad] She wasn't killed by the Bleed. She was made to disappear.
```
**CHOICE `:ch6_kestrel_rumor`**
```
> Then go and find out. (encourage)
  Script: pf_choose(:ch6_kestrel_rumor, :encourage)
  [portrait: KESTREL, shocked] ...You think it's her.
  [portrait: KESTREL, happy] You think it could be her. Everyone else says "let it go". You said "go".
  [name: Kestrel] Then I'm going. All the way. Wherever he turns up next, I'll be closest.
> It might not be her, Kestrel. (warn)
  Script: pf_choose(:ch6_kestrel_rumor, :warn)
  [portrait: KESTREL, angry] I know it might not be her. I KNOW. Don't you think I know?
  [portrait: KESTREL, sad] ...I just need it not to be nobody.
  MOVE: he stands up and won't look at you.
> ... (silent)
  Script: pf_choose(:ch6_kestrel_rumor, :silent)
  [portrait: KESTREL, neutral] Yeah. That's what Gran says, too. Nothing, very loudly.
(All:)
[portrait: KESTREL, neutral] The cell's gone south and down, to Nadir. Mirefen, the char-burners said. I'm going after them.
[portrait: KESTREL, deadpan] Don't follow me. You will anyway. Just don't do it where I can see.
MOVE: Kestrel walks off east along the Marrow Road, toward the Kneeling Stones, the veil back under his coat.
Switch S117 CH6_K3_DONE = ON. V114 KESTREL_STAGE stays 1. V126 = 8.
```
*(Long-term: `:encourage` +2 now and −3 at Ironreach, when it isn't her; `:warn` −1 now and +2 at Ironreach: "You said it might not be. I hate that you were right." — NARRATIVE_KEYS.)*

## Map 628 — Sinkfield (optional, `:BLEED`) — **Game over `GO_SINKFIELD` "Sinkfield"**
```
(Off the Marrow Road, a field of what was farmland, where the collapsing aquifer and the Earth Imprint have made the sand behave like water. A path of fossil bones runs across it, a rib, a vertebra, a rib, like stepping stones.)
Script: Prismfall.checkpoint     # NARRATIVE_KEYS §10: the Sinkfield entrance
FIELD NOTES pop-up: "SINKFIELD — BLEED. The sand is pretending to be the sea. It's very convincing. Walk the bones."
[portrait: SAHAR, neutral] *(if she's with you at the edge, or a note pinned to the first rib in her hand)* Walk the bones. Never the sand. I'm saying it a third time because I've buried people who heard it twice.
(Halfway across, a caravan boy's sandal lies on the sand beside the path. As you watch, it sinks, very slowly, the way a leaf goes under in a pond. It's gone.)
GLINT (off the path, two tiles onto the sand; action): Something shines out there on the open sand. A coin? A ring?
> Step off the bones to get it.
  > Really? It's on the sand.
    > Step off.
      (Your foot goes in to the ankle. Then the knee. The sand is warm, and it's very patient.)
      Script: Prismfall.game_over(:GO_SINKFIELD)
    > Stay on the bones.
  > Stay on the bones.
```
*Trials (Ch7, `badges >= 5`): "Something in the Sinkholes" (OS_SINKFIELD, the Galarian Stunfisk boss).*

## Chapter 6 close — the Duneholt Pokémon Center (201) or the Marrow Road, after K3 (V126 == 8 → 9)
```
(A Gale Post courier in goggles, out of breath, sand to the eyebrows.)
[name: Gale Post Courier] \PN? Thought so. You're the only one in Ossaria nobody can describe. Letter. It's been chasing you since Lumen.
(The letter, in green ink, a little smudged:)
"\PN,
I found a way down! There was a ferryman on the Leach and he knew Dr Mott, and now I'm in Mirefen and it's BLUE at night, the whole marsh glows, and the noodles are the best I've ever had and Dr Mott says they'll kill me.
I'm helping him with his seed-medicine. His ward is very quiet. I'll tell you about it when you come. I don't want to write it.
Uncle Rowan wrote. He burned his hand on the kettle, he says, the same night as the Lowlight. His right hand, all across the palm. He's made tea every morning for forty years.
He's been "away on Warden business" every time something happens. Every time. I counted.
I'm being silly. I know I'm being silly.
Come to Mirefen? Bring snacks.
— Juno"
QUEST LOG: "Eighteen Roads" — Earn the sixth badge in Mirefen, down the Leach Road into Nadir.
V126 = 9. V102 STORY_CHAPTER = 7.
```
*(09 #2: the burned hand and the counting; Corvin's ledger in Ch7 says "right palm and fingers". Juno is the one doing the counting, which is what makes J2 hurt.)*

---

## Map events needed (Chapter 6)

None of these maps is built. **[NEW]** marks anything not in maps.json. V126 = **CH6_STEP** (design/FLAGS.md).

**608 The Lowlight (Shattered)** — the Act II opener autorun (once, V126 == 0): Rook on the vault step (plain hood sprite, no drone); the Directorate barrier and two officers; the shrine (decor: soda cans, candles, chalk names); **Dex's glass figure** (action from inside the Veil: the warmth scene, SE one low note); Marlo at the shrine (2 lines); Juno at the top of the stairs (her goodbye; V126 = 1). The Trials quest `ZE_LOWLIGHT_LAMPS` (S164) runs here too.
**180 Lumen Concourse (after S115)** — three changed townsfolk lines; the grille's Directorate seal (inspect).
**612 The Meridian Mainline** — road sign; **"The Checkpoint"** at the signal gantries (barrier, tent, scanner post, two officers, a queue of 2–3 NPCs; two variants by `:ch5_lowlight_testimony`; V126 = 2). Route trainers (designer).
**602 Candle Down** — road sign; candle-cairns (each "twelve candles"); the big cairn at the gap (the Scar's glitter; the old pilgrim); the coaching-inn keeper. Trainers.
**603 The Highwold** — road sign; the Wold Stones (inspect); shepherd; dew-pond girl. Kingsmead west closed (sign). Trainers.
**600 The Brass Dunes** — road sign; the hanging viaduct span (decor); rail ganger. **610 Copperdune** — bone-trader, freight clerk, caravan child; Trials hooks (Riddle Trader, Tomb Freight, tablet rack).
**604/605 Static Tunnels** — dark (Flash); tram car No. 9 (inspect).
**601 The Rib Road** — road sign; caravan guide. **613 Sunbleach Flats** — road sign; linen-maker; the side path to the Temple of the Noon Sun (Trials `OS_OCTAVE_NOON_BELL`). **Map ID clash:** TRIALS_QUESTS gives the temple as map **215**, but GYM_PUZZLES uses 215 for the Gym 5 Mural Gallery Mastery. Segment 4's free interior/optional IDs are 606, 607, 609, 614–619: please give the temple one of those.
**203 Duneholt Sandgate** — arrival autorun (V126 == 2 → 3); the two notices (signs, the Mandate one pasted over Kassan's); the caravan-mother; the gate guard.
**200 Terrace Bazaar / 201 PC / 202 Mart** — four townsfolk; 201 Gale Post (Larch's note, KELP TEA BAG).
**209 Sahar's Dig Lab** — Sahar (first meeting; warning 1); three interns; Trials (Kevin, the Hall of Unearthing board); fossil revival NPC.
**204 the Aquifer Quarter** — **"The Deep-works"** autorun (after Sahar is met, V126 == 3 → 4): the great well (decor, a water level that drops one rung per chapter state if the art allows), the deep-works derrick and shaft, three Drilbur and an Excadrill with collar-and-cable sprites, 2–3 Bereaved at the fence, 2 caravan children, a Directorate squad (sergeant + 2), the caravan boy's mother on a terrace, and Sahar for the `:sanctuary` branch. Battles: `MERIDIAN_DIRECTORATE` "Sergeant" (the type exists; a new Duneholt version, the first Directorate fight) for `:hollow`; `HOLLOW_GRUNT_M` (Duneholt version) for `:directorate`. Gives MANDATE PASS for `:directorate`.
**214 the Sinkwells** — two townsfolk (the water-carrier hooks OS_SINKFIELD). **205/207** closed doors (signs). **208 Necropolis** — tomb-keeper; the road to 620.
**210–213 the Dig (Gym 5)** — as GYM_PUZZLES; the aide, the gym guide, Nadim's hints; Sahar (213) with three pre-battle variants by `:ch6_drillsite`, the ace line, the SANDGLASS BADGE, TM83; the excavators teach Strength at the gym door after the badge. V126 = 5.
**620 The Marrow Road** — road sign; **"The Door in the Skull"** autorun (the first pass after Gym 5; Sahar, two diggers, a lamp; V126 = 6); the comedy scene and **K3** at the Ossuary's mouth on the way out (Kestrel drops from the skull's brow; `RIVAL_KESTREL` version 30 + slot; S117; V126 = 8). Trainers.
**624/625 The Ossuary of Dunes** — Field Notes on entry; drifting Unown (decor events); Strength boulders; **four mural events** in order (Sahar follows as a companion NPC and speaks at each); the rubbing (DUNEHOLT RUBBING; S116; V126 = 7); the optional glyph-swarm boss in 625 (BOSSES.md); the Spiritomb static and Odd Keystone as maps.json. Unown-script puzzles per the puzzle engineer (DUNGEON_PUZZLES).
**628 Sinkfield** — `Prismfall.checkpoint` at the entrance; Field Notes; Sahar's third warning (a note on the first rib if she isn't there); the bone path (stepping-stone events); the sinking sandal (a move route that lowers it); the glint (action, three confirms, GO_SINKFIELD). Trials OS_SINKFIELD as designed.
**Chapter close** — the Gale Post courier (an event in 201, or on 620 after K3): Juno's letter; V126 = 9, V102 = 7.

**Trainer designer:** a Duneholt version of `MERIDIAN_DIRECTORATE` (the type exists, with "Captain" v21; this one is "Sergeant", Steel/Electric per 02_FACTIONS: Magnemite, Pawniard, Klefki, Lv 28–30), Duneholt `HOLLOW_GRUNT_M` (Ground/Dark: Sandile, Drilbur, Nickit), K3 as BALANCE (cap 35). **Items owner:** MANDATE PASS, DUNEHOLT RUBBING (Key Items). **Badge name:** the Sandglass Badge (creator, 2026-11-21).
