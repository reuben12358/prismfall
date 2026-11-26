# Script: Chapter 8 — "The Light Stone" (the Sulfur Road, Cindervault, Gym 7; the Caldera Crisis)

> **Final playable script** for Chapter 8. It covers the Sulfur Road (640 Leechman's Walk, 641 Lake Sallow with 650/651 Scaldwater and the optional 658 Lantern Isle, 652 the Pyre Road), Cindervault (240–249, 254), the Foundry gym (250–253, Gym 7), the Caldera Crisis at the tap under the Slag Ward (new room 255), and the war drums in the caldera square. None of these maps is built yet; the list at the end is what to build.
> **Replaces `story/22_SCRIPT_CH8.md`** (the withdrawn Ring-Day; SPINE Revision 21 moved the ring to Ch14, Bastian, Cragholm). Nothing here gives a Mega Ring or a Mega Stone to the PC. What stays from the old plan is Brann's chestnut slip, the clue the Ring-Day pays off.
> Follows `story/26_SCRIPT_CH7.md`; `story/27_SCRIPT_CH9.md` follows this (its opening reads S120, S121, V110 and `:ch8_caldera`, `:ch8_lightstone`). Conventions of `story/20_SCRIPT_CH0-2.md`.
> Sources: 05_ACT_II Ch8, 03_CAST (Brann, Sigrun, Quent, Wick, Larch), 09_MYSTERIES (#4, #5, #6, #18), NARRATIVE_KEYS (`:ch8_caldera`, `:ch8_lightstone`, GO_LET_THEM_LISTEN), 15_COMEDY (Ch8 "The Hug"; Ashkaar's honest shop signs; the afraid-of-heights recruit), GYM_PUZZLES Gym 7, TRIALS_QUESTS (Ashkaar board, Ch8), BALANCE and the trainer notes (Quent v0 at the taps), `design/CHAPTER_BEATS.md` (Ch8), SPINE Revisions 21–25.

## Conventions
As in the earlier scripts. **Portrait cast here:** Larch, Brann, Sigrun, Quent, Wick, Sable (on screen, one line). **Plain:** the Dominar's envoys (Envoy Haskar and two oath-guards), the Dominar's herald, the Hammer bomber, Hearthguild smiths, Scaldwater's bath-keepers, every townsperson and trainer. Events call `Prismfall.gym_battle(pfm_gym(:LEADER_BRANN))`.
**Counter:** V129 **CH8_STEP** (design/FLAGS.md): 0 down Leechman's Walk · 1 Lake Sallow and Scaldwater · 2 the Pyre Road oath · 3 Cindervault and "The Hug" · 4 Hearthguild Hall (the envoys, Sigrun) · 5 Gym 7 won · 6 the Caldera Crisis (S120, V110) · 7 the Light Stone (`:ch8_lightstone`) · 8 chestnuts (the slip) · 9 the herald (S121, V122 = 1) · 10 chapter closed (V102 = 9).
**State set here:** V110 CINDERVAULT_STATE (0 normal, 1 ashen after `:vent`, 2 overdrawn after `:dampers`; `:shutdown` leaves it 0), S120 CH8_CALDERA_DONE, S121 CH8_WAR_DRUMS, V122 WAR_STATE = 1.
**Ashkaar's rule:** lying to a Dominion guard is a crime. Oath-braziers stand at every gate; a guard asks a question and the PC can answer true or say nothing. There is never a lying option in Ashkaar. (Comedy rides on it: shop signs are painfully honest.)

## The chapter's key events (design/CHAPTER_BEATS.md)
1. **The Caldera Crisis** (`:ch8_caldera`). Meridian's tap under the Slag Ward is overdrawing the Flame Plate's Imprint; the Hammer plants a Splitter on it; Wick's Hollow want to vent it with lake water; Quent wants to fit dampers and keep it running. Three answers, three costs. Build-up: the forges too hot to touch, the honest sign "WATER (BOILING)", Sable's "Cindervault's next" (Ch7). Consequence: V110 for the whole game, Brann's line at the Conclave, the Ashmarch's ash.
2. **The Light Stone and the war drums** (`:ch8_lightstone`). The Dominar's envoys try to take Reshiram's stone in the confusion; Sigrun stops them herself; the PC says who should keep it. Then the herald: Ashkaar closes the eastern passes to Zenith. Build-up: the envoys in Hearthguild Hall, Sigrun's "my father", the oath-braziers. Consequence: Sigrun's Bond, `DOMINAR_SWAYED`'s seed, Brann's Act V Consent, the war's first step (V122).
**The slip** (09 #5/#6): Brann, three cups of mulled cider in, "I reset the Crown's stone myself... it was smaller than it should've been." The shard answers. Larch sees the PC wince. Nobody explains anything.
**No jokes** from the moment the tap alarm sounds until the pressure gauge drops back to the green (15_COMEDY §1). "The Hug" and the shop signs are on arrival, well before.

---

# CHAPTER 8 — "The Light Stone"

**Chapter start:** V102 = 8, V129 = 0 (Ch7 close: Mirefen's chalked walls; Surf from the ferrymen). Larch travels with the PC this chapter (she left Lumen with the PC in Ch6 and has been "in the Infirmary library, being useful" through Ch7). Juno stays in Mirefen with Corvin until the Conclave.

## Map 640 — Leechman's Walk (east out of Nadir, `:CORROSIVE_MIRE` default)
```
ROAD SIGN: LEECHMAN'S WALK — ← Mirefen & the Sweet Market · → Lake Sallow & the Sulfur Road. Boards only. The boards know where the bottom is. You don't.
(Plank walks on stilts over a black peat-marsh. Lanterns on poles, every tenth one lit. The air smells of eggs and pennies.)
(Larch is waiting on the first platform with her carpet-bag, a fresh notebook and a thermos.)
[portrait: LARCH, neutral] There you are.
[name: Larch] I've borrowed six books from Corvin's library and told him about four of them.
[name: Larch] Brann's expecting me. I wrote to say I'd come with you.
[name: Larch] He wrote back in capitals. That's how he writes.
[name: Larch] That's also how he talks.
[portrait: LARCH, deadpan] He's going to hug you.
[name: Larch] I'm telling you now so you can make your peace with it.
V129 = 1.
[name: Leech-gatherer] Leeches for the Infirmary. Sixpence a jar.
[name: Leech-gatherer] The Doctor says they're medicine.
[name: Leech-gatherer] I say they're the only things in Nadir that work for food.
[name: Peat-cutter] (by a stack of black bricks) The Lattice runoff's in the peat now.
[name: Peat-cutter] Burns blue. Pretty. You wouldn't want to cook on it.
```
*Trainers on 640 (trainer designer): leech-gatherers, a Fisher on the stilt-dock, a Hex Maniac who "reads the bubbles". Wild: BALANCE segment 6.*

## Map 641 — Lake Sallow (borderland E, Surf) and Map 650 — Scaldwater
```
ROAD SIGN: LAKE SALLOW — Elowen's last water. ↑ Scaldwater (the baths) · → the Pyre Road & Ashkaar. Warm water. Do not drink. Do not boil. It's already boiling.
(A wide green lake that steams. In the shallows, sulfur crusts like yellow lace. Out in the middle, Lantern Isle's one tower, unlit.)
(The first Surf crossing of the game that matters: the road east runs out at the water, and the ferry-stage has a sign: FERRY SUSPENDED (HOT).)
[portrait: LARCH, neutral] Two years ago you could swim this in October.
[name: Larch] Now the fish come up cooked.
[name: Larch] Something's warming it from underneath.
[name: Larch] I'll take the Scaldwater barge round. You go across.
[name: Larch] Meet me at the bath-house, and don't fall in.
[name: Larch] You'll come out as soup.
SCALDWATER (650): terraced bath-houses on the north shore; Elowen hot-spring keepers; a Pokémon Center (651).
[name: Bath-keeper] The springs run hotter every week.
[name: Bath-keeper] Used to be you sat in them.
[name: Bath-keeper] Now you lower yourself in on a rope and pray.
[name: Bath-keeper] Cindervault's tap, they say. Up the mountain.
[name: Bath-keeper] Meridian put a pipe in the Flame and now the whole lake's a kettle.
[name: Elowen Pilgrim] There's a Hollow woman in the low bath, giving out cool cloths to anyone who walks in from the east.
[name: Elowen Pilgrim] She won't say her name. She smells of the Fen.
(Low bath, V129 == 1: a woman in a grey cowl with the hood down, wringing cloths into a bucket of lake water and cooling them on a slate. One of Wick's faithful from the Weeping Fen.)
[name: Hollow Faithful] You're the one Brother Wick talks about.
[name: Hollow Faithful] The one the Fen let through.
[name: Hollow Faithful] He's gone up to Cindervault.
[name: Hollow Faithful] He says the mountain's got a fever, and you don't cure a fever by stoking it.
[name: Hollow Faithful] ...He also says hello.
[name: Hollow Faithful] He said to say it like that: "hello". He's not good at messages.
V129 = 2 (at the bath-house, with Larch).
[portrait: LARCH, sad] Wick. Of course he's gone up.
[name: Larch] Everyone I ever liked is walking toward that mountain.
```
*Trials hook: "Ashes Home" (Scaldwater, the Ashkaar board, Ch8).*
**Optional: Lantern Isle (658, `:BEACH`)** — the unlit lighthouse; the keeper's logbook (its last entry: "Lake warm. Lamp oil sweating. Will light tomorrow."); a Lapras in the cove that follows the PC's boat to the island and back. No story; atmosphere and items.

## Map 652 — The Pyre Road: **"Say True"** (the oath-gate into Ashkaar; V129 == 2 → 3)
```
ROAD SIGN: THE PYRE ROAD — Ashkaar, the Dragonfire Dominion. ← Lake Sallow (Elowen) · ↑ Cindervault. At the gate, say true or say nothing.
(The land climbs out of the steam onto black basalt. Red lacquer banners on the cliffs. Overhead, too high to hear, a dragon-rider circles.)
(At the oath-gate: a brazier as tall as a door, two guards in red lacquer, and a stone plinth with a bronze hand on it.)
[name: Oath-Guard] Hand on the bronze. Say true or say nothing.
[name: Oath-Guard] Are you here to do harm in the Dominion?
> (Hand on the bronze.) No.
  (The bronze is warm. The brazier doesn't change. The guard nods.)
  [name: Oath-Guard] True. Walk on.
> (Say nothing.)
  [name: Oath-Guard] Nothing is allowed. Nothing is also noticed.
  [name: Oath-Guard] Walk on, and be watched.
  Script: pfm_set(:ashkaar_watched)     # two extra oath-guard lines in Cindervault; no other effect
[name: Oath-Guard] *(to Larch)* And you, Elowen woman. Are you here to do harm?
[portrait: LARCH, deadpan] I'm here to be hugged against my will. Does that count?
[name: Oath-Guard] ...True. Walk on.
V129 = 3.
[name: Legion Recruit] (on the road, holding a Trapinch like a baby) I'm a dragon-rider.
[name: Legion Recruit] They gave me a Trapinch until I'm ready.
[name: Legion Recruit] I'm afraid of heights. They don't know. Don't tell them.
[name: Legion Recruit] ...I just told you. I can't lie. It's the law. It's awful.
[name: Pilgrim Smith] Cindervault's bells used to ring the hours. Now they ring the heat.
[name: Pilgrim Smith] Three bells, you take your Pokémon off the forges.
[name: Pilgrim Smith] Four, you take yourself.
```
*Trials hook: "Afraid of Heights" (the Dragon Roosts, 248). Trainers on 652 (trainer designer): Legion recruits, a Kindler, an Ace Trainer pair on the switchbacks. Wild: BALANCE segment 6.*

## Map 243 — Cindervault, the Caldera Gate: **"The Hug"** (autorun at the gate, V129 == 3 → 4)
```
(Cindervault is a city in a crater. Smithies stacked up the caldera walls in red-roofed tiers; quench-channels of dull orange running down between them like streets; the Hearthguild's bell-tower on a spur of black rock; and below everything, on the caldera floor, a squat iron building with MERIDIAN STANDARD TAP No. 7 painted on its side and a pipe going down into the ground.)
SE: three bells.
[name: Gate Smith] Three bells! Off the forges! It's not even noon!
(A man the size of a doorframe comes up the gate stair two at a time: leather apron, beard braided with iron rings, a hammer on his belt that would be a weapon in anyone else's hand.)
[portrait: BRANN, happy] [emote: exclaim] IMELDA! *(a bear-hug that lifts her off the ground; shock lines)*
[portrait: LARCH, panic] Ribs. Brann. Those are my ribs.
[name: Brann] And THIS is the ferry child! Come here!
> (Dodge.)
  [portrait: BRANN, surprised] Quick! Good! A smith respects reflexes! *(hugs anyway)*
> (Accept your fate.)
  [portrait: BRANN, crying] So small! Imelda, they're so SMALL!
  [name: Brann] Are you feeding them? *(crying, happily)*
[portrait: LARCH, deadpan] I offer tea.
[portrait: BRANN, shocked] The kelp one?
[name: Brann] I quenched a blade in that once.
[portrait: LARCH, angry] You did WHAT. *(anger vein)*
[portrait: BRANN, smug] Best edge I ever got.
[portrait: BRANN, neutral] *(putting the PC down; quieter)* You picked a bad week. The mountain's running a fever, and two lots of people want to be the doctor, and neither of them's a doctor.
[name: Brann] Come up to the Hall.
[name: Brann] There's an Ashkaar envoy in my best chair and I'd like witnesses.
V129 = 4 (on arrival at 244).
```
*(15_COMEDY Ch8 "The Hug"; the last joke-heavy scene before the tap.)*

## Map 240 — Cindervault, the Forge Terraces (town)
```
SHOP SIGNS (inspect; lying is a crime, so the signs are honest): "ADEQUATE SWORDS." · "BREAD (YESTERDAY'S)." · "WATER (BOILING)." · "MART: PRICES HIGH BECAUSE OF THE WAR THAT ISN'T HAPPENING." · "SMITH. NOT VERY GOOD. CHEAP."
[name: Terrace Smith] I can't work. The quench-channels are running at a boil.
[name: Terrace Smith] You can't quench in boiling. A blade wants a shock, not a bath.
[name: Smith's Apprentice] The Meridian men say the tap's fine.
[name: Smith's Apprentice] They put a gauge on it. The gauge says fine.
[name: Smith's Apprentice] The gauge is also melting.
[name: Old Smith] (at a cold anvil) My grandmother used to say the Flame Plate's not a fire, it's a heart. You don't put a pipe in a heart.
[name: Hearthguild Bell-Ringer] Three bells this morning. Four yesterday.
[name: Hearthguild Bell-Ringer] We've never rung five. Five means leave the mountain.
[name: Hearthguild Bell-Ringer] I've got the rope for it. I've never had to touch it.
[if pfm_get(:ashkaar_watched)] [name: Oath-Guard] (following at a polite distance) Don't mind me. You said nothing at the gate. I'm the nothing's escort.
```
*Trials hooks: "Seven Bouts" (the Crucible on the caldera rim; the Octave singer AS_OCTAVE_TOO_LOUD's kingdom duel), "Adequate Swords" (Cindervault market), "The Lava-Tube Terror" (the Cinderhorn, 664).*

## Map 244 — Hearthguild Hall: **"My Father"** (V129 == 4)
```
(A long hall with a forge at one end and a table made from a single slab of basalt down the middle. On the wall over the forge, behind a grille: a white stone the size of a fist, giving off a light like a cold morning. The Light Stone.)
(In Brann's chair at the head of the table: a lean man in red lacquer with a gold dragon on his collar. Two oath-guards behind him.)
[name: Envoy Haskar] Warden. The Dominar's patience is a coal.
[name: Envoy Haskar] It glows a long while. It is not endless.
[portrait: BRANN, angry] And my answer's a hammer, Haskar. It doesn't glow at all.
[name: Brann] The Light Stone is the Hearthguild's.
[name: Brann] It's been the Hearthguild's since before your Dominar's great-grandmother learned to ride.
[name: Envoy Haskar] The Stone is Reshiram's. Reshiram is Ashkaar's.
[name: Envoy Haskar] The Hearthguild is in Ashkaar. You see how it follows.
[name: Brann] The Concordance says a Warden keeps what was put in their keeping.
[name: Brann] Say true, Haskar.
[name: Brann] Was the Stone put in your keeping?
[name: Envoy Haskar] ...No.
[portrait: BRANN, happy] There! See! Honesty! Isn't it marvellous!
SE: wingbeats, close, like a sail cracking. Dust comes down from the rafters.
(A woman walks in from the yard door with ash on her boots and riding leathers, pulling off a glove. At the door behind her, a Salamence folds its wings and puts its head on the step like a dog.)
[portrait: SIGRUN, neutral] Haskar. Get out of the Warden's chair.
(Haskar gets out of the chair.)
[name: Envoy Haskar] Wardeness. The Dominar sent me to—
[portrait: SIGRUN, angry] I know what my father sent you to do.
[name: Sigrun] I read the letter before he sealed it. Sit somewhere else.
(She looks at the PC for a long moment, the way a rider looks at a horse she's been told is fast.)
[name: Sigrun] So you're the ferry child everyone's whispering about.
[name: Sigrun] Hm. Smaller than I expected.
> I've been told.
  [portrait: SIGRUN, smug] By Brann, I imagine. Loudly.
> Smaller than what?
  [portrait: SIGRUN, smug] Than the whispering.
> ...
  [portrait: SIGRUN, smug] Good. You don't talk to fill the air. Neither do I.
[portrait: SIGRUN, smug] I'm Sigrun Ashfall. Wyrmrest. The Dragon Warden.
[name: Sigrun] I'm here to keep two stubborn men from starting a war over a rock, which is the most Ashkaar sentence anyone will say to you this week.
[portrait: BRANN, happy] She's very good. She's been doing it since she was nine.
[name: Sigrun] Since I was eleven. At nine I was starting them.
[portrait: LARCH, neutral] *(aside, to the PC)* Watch her.
[name: Larch] She's the only person in this room who isn't scared of the mountain.
[name: Larch] That's either very brave or she knows something.
SE: four bells.
[portrait: BRANN, sad] Four. That's four.
[name: Brann] *(to the PC)* Go and get your badge while I've still got a gym that isn't on fire.
[name: Brann] I'll be down in the Foundry.
[name: Brann] Sigrun, keep him out of my chair.
V129 = 4 (Gym 7 opens).
```
*(09 #18: Sigrun's appraisal, "smaller than I expected": she's measuring something she's heard of, not the child. Paid off in Ch17/Ch19.)*

## Maps 250–253 — the Foundry (Gym 7; GYM_PUZZLES Gym 7)
```
[name: Gym Guide] The Foundry! Fire-types on the Volcanic field.
[name: Gym Guide] Rock hits like fire here, and everybody leans on Lava Plume.
[name: Gym Guide] Bring Water. Bring a lot of Water.
[name: Gym Guide] The puzzle's simple. Pour, then quench.
[name: Gym Guide] Molten's a wall, iron's a bridge, and what you don't quench runs down to the moulds.
[name: Gym Guide] The Warden says the bridge you don't finish is the one that carries you.
[name: Gym Guide] He says it a lot.
[name: Foreman] (250) And what you don't quench runs down to the moulds below. Waste not.
[name: Apprentice Hessa] (251, hints, T0) Brann says pour where it hurts, not where it's easy. / The X3 channel won't bridge from up here. Let it run. / (the solution)
(Gym trainers per GYM_PUZZLES: two Workers, a Black Belt, Camper "Kindler", a Cool Trainer. Lv 35–38.)
```
### 253 — the Warden Arena: Brann
```
(The arena is the Foundry's casting floor: a ring of iron plates over a pit of slow orange light. Brann stands at the far side with his hammer over his shoulder and his sleeves rolled to the elbow.)
[portrait: BRANN, neutral] Some things you forge to last.
[name: Brann] Some things you forge to BREAK right.
[name: Brann] That's the harder craft. Took me thirty years to learn the second one.
[portrait: BRANN, happy] Let's see which one you are!
Script: Prismfall.gym_battle(pfm_gym(:LEADER_BRANN))     # Torkoal, Camerupt (Mega; LOCKED, creator 2026-11-21), Magmortar, Arcanine, Coalossal; field :VOLCANIC
(When Brann Mega Evolves Camerupt:) [portrait: BRANN, happy] A Warden's ring! Cut it myself! Don't ask me where the stone came from, I'll tell you, and it's a long story!
(At Coalossal, his ace:) [portrait: BRANN, neutral] Old girl. Show them what a mountain does when it's had enough.
(LOSE: whiteout to the Cindervault Pokémon Center.)
(WIN:)
[portrait: BRANN, crying] HA! *(crying, happily)* Broke me right! That's the harder craft!
(Received: the QUENCH BADGE.) ITEM DESCRIPTION: "A dark iron badge with a white line through it where it was plunged hot into water. Brann says the line is where it learned something."
(SE: seven notes. The case's light runs along its seams. Brann stops with his hand half-raised for a slap on the back.)
[portrait: BRANN, shocked] [emote: dots] ...Your case sings. Huh. *(He looks at it a beat too long.)* Don't let Imelda take it apart.
(Received: TM35 FLAMETHROWER.)
[name: Brann] The Quench Badge. Quench is the moment a blade decides what it's going to be.
[name: Brann] Too slow, it's soft. Too fast, it cracks.
[name: Brann] There's a joke in there about Wardens.
[name: Brann] I'm not going to make it, there's a Sovereign's man in town.
V129 = 5.
QUEST LOG: "Eighteen Roads" — Seven badges. The road west goes down to Ironreach and the Conclave.
```
*(The ring Brann Megas with is his own Warden's ring; it's no gift to the PC (SPINE Rev 21/22). The PC's ring comes from Bastian after Badge 13. Brann's line about the stone is a joke now and a clue later: it is the same craft as the Crown's reset, 09 #5.)*

## The Caldera Crisis (autorun on leaving 250, V129 == 5): **"Five Bells"**
```
(Out of the Foundry into the square. It's dusk, and the dusk is the wrong colour. The quench-channels are glowing up through their grates.)
SE: a bell. Two. Three. Four.
(Silence. Then, from the tower, slowly, as if someone is making themselves do it: five.)
[name: Bell-Ringer] *(from the tower, hoarse)* FIVE! Off the mountain! FIVE!
(People come out of every door at once. Not running yet. Looking at each other to see if they should run.)
[portrait: BRANN, angry] *(coming out of the Hall at a run, Sigrun behind him)* That's the tap. That's the TAP. Imelda, the gauge on the bell-tower, what's it say?
[portrait: LARCH, shocked] *(looking up)* It's in the red and still climbing.
[name: Larch] Brann, at this rate it's under an hour.
[portrait: SIGRUN, angry] Under an hour to what?
[portrait: BRANN, sad] To the mountain doing what mountains do.
[name: Sigrun] *(already moving)* Then I'll get the Roosts' riders to the lower terraces.
[name: Sigrun] Children first. Brann, your smiths.
[name: Sigrun] *(to the PC)* You. Can you fight?
[name: Brann] They just beat me.
[name: Sigrun] Then go down to that tap and find out who's making it worse.
V129 = 6 (begin).
```
*(No jokes from here until the gauge drops (15_COMEDY §1).)*

## Map 249 — the Slag Ward and Map 255 — the Tap Chamber [NEW]: **"Three Doctors"**
```
(The Slag Ward: shacks of slag-brick at the bottom of the caldera, where the city's poor live under the channels' run-off. Families coming up the stairs against you with bundles. A child carrying a Litwick in a jam jar like a lantern.)
(Down the tap's service stair. The Tap Chamber: a round iron room around a pipe the width of a well, going down into rock that glows. A ring of gauges. A heat that pushes on your face. Three groups, and nobody listening to anybody.)
(At the valves: Meridian engineers in scorched white coats around a crate of brass rings, and in the middle of them a man in round smoked spectacles, bouncing on his toes.)
[portrait: QUENT, happy] Oh, it's YOU! The null reading! *(giggling)*
[name: Quent] Hold still, I've only got one probe.
[name: Quent] Dr. Percival Quent, Meridian Applied Sciences. These are dampers.
[name: Quent] We fit them, the draw evens out, the pressure drops, and Tap Seven keeps running.
[name: Quent] Everyone keeps their lights. It's terribly simple.
(On the pipe's collar, under the soot, a brass plate. Brann wipes it with his sleeve and reads it out, slowly.)
[portrait: BRANN, angry] "TAP SEVEN. CINDERVAULT. DESTINATION: RIMEHOLT — HEAT TOWERS ONE TO FOUR. SECONDARY: LUMEN GRID."
[name: Brann] Rimeholt. Our fire, piped over the mountains to keep the Thane's people warm.
[name: Brann] And none of us was asked.
[name: Quent] Isn't it marvellous? One mountain, two kingdoms!
[name: Quent] It's the most efficient thing I've ever seen!
(At the old lava-channel sluices on the far wall: Wick, in his grey cowl with the hood back, and six Hollow faithful hauling a canvas hose that runs up the stair and out toward the lake pipe.)
[portrait: WICK, neutral] Hello. *(It's exactly the way the woman in Scaldwater said it.)*
[name: Wick] We open the old channels and run Lake Sallow down them, onto the Imprint.
[name: Wick] The fever breaks. The mountain sleeps. And the forges go cold for a season, and the ash comes down on the Ashmarch like snow.
[name: Wick] It isn't kind. It's only safe.
(And on the pipe itself, halfway up the iron ladder, a figure in a grey cowl and a bark mask with a painted hammer on it, strapping a brass-and-glass device to the pipe's collar. A Splitter. It's ticking.)
[name: Hammer Bomber] Stay back! All of you! The Hollow, the Meridian, the lot!
[name: Hammer Bomber] They'll cover up a fever. They'll cover up a crack.
[name: Hammer Bomber] They can't cover up a mountain.
[name: Hammer Bomber] When this goes, every screen in Velmora will show it, and THEN they'll listen.
[portrait: WICK, angry] There are families on the stairs, child.
[name: Hammer Bomber] There were families in the Lowlight!
BATTLE: double battle vs [HOLLOW_GRUNT_M "Hammer" + HOLLOW_GRUNT_F "Hammer"] (version 8). Field: Volcanic. (Their Pokémon guard the ladder.)
(LOSE: whiteout to the Cindervault Pokémon Center; restart at the top of the tap stair, Prismfall.checkpoint.)
(WIN:)
(The two Hammers' Pokémon go down. The bomber is cornered on the ladder, and the Splitter on the pipe is still ticking. He looks at it. He looks at you. Then he holds out his hand, and in it is a brass detonator with one red key.)
[name: Hammer Bomber] *(quietly)* You saw the Lowlight. I know you did. You were there.
[name: Hammer Bomber] Do it. They'll finally listen.
> (Take the detonator and turn the key.)
  Script: Prismfall.game_over(:GO_LET_THEM_LISTEN)
  (EPITAPH: "They listened. There was no one left to tell.")
> (Take the detonator and throw it into the glow.)
  (It goes down the pipe's throat without a sound. The bomber watches it go.)
  [name: Hammer Bomber] ...Coward.
  [portrait: WICK, sad] No. That was the brave one, child.
  [name: Wick] You'll understand in about ten years. I'm sorry it takes so long.
> (Don't take it.)
  [name: Hammer Bomber] *(his hand shaking)* ...No. No, I can't either.
  [name: Hammer Bomber] I can't either.
  (He drops it. Quent's engineer stamps on it, hard, three times.)
(The bomber goes up the stair and is gone. The Splitter on the pipe is dead without its key. Quent unstraps it with two fingers and puts it in his coat pocket, humming.)
(And the gauges keep climbing.)
[portrait: LARCH, shocked] [emote: exclaim] *(at the gauge ring)* The bomb was never the problem. The tap's still drawing. It's still going UP.
[portrait: QUENT, happy] Dampers, then! Help me fit them and we're done by supper!
[portrait: WICK, sad] Or help me open the channels and we're done by supper, and nobody's done anything to the mountain it didn't ask for.
(There's a third option nobody says out loud. Through the steam, on the Meridian side of the chamber, a big red lever under a glass cover: TAP 7 — EMERGENCY CLOSE — DIRECTORATE AUTHORISATION ONLY. Two Directorate soldiers stand in front of it.)
[name: Larch] *(to the PC, very low)* Three doctors.
[name: Larch] Your call, I'm afraid. I'm only a professor.
CHOICE :ch8_caldera
> Help Wick vent it. (vent)
  Script: pf_choose(:ch8_caldera, :vent)
  [portrait: QUENT, sad] Oh, don't. Don't.
  [name: Quent] Do you know what that'll do to my DATA?
  BATTLE: MERIDIAN_QUENT "Percival", version 0. Field: Volcanic. (His team guards the valves. At the end of turn 3 Wick's hose opens the channels and the field becomes Ashen Waste: `setBattleRule("fieldChange", [3, :ASHEN_WASTE, "Lake water roars down the old channels! The fire goes grey!"])`.)
  (Quent's note in the trainer data: his Rain Dances are dampers too. Rain quenches the field to Cinderglass at once, and rain-form Castform rides the geysers.)
  (WIN:)
  [name: Quent] *(wiping his spectacles)* Fine. Fine. I'll write it up as a natural experiment.
  [name: Quent] "Subject vents mountain." Do you know how rare that is?
  (Wick's faithful open the old channels. Lake water roars down the stone. Steam fills the chamber, white and then grey, and then the grey comes down as ash, soft, everywhere.)
  (The gauges fall. Out of the red. Through the amber. Into the green.)
  [portrait: WICK, sad] There. It's asleep. It'll be cross when it wakes up.
  V110 CINDERVAULT_STATE = 1.
> Help Quent fit the dampers. (dampers)
  Script: pf_choose(:ch8_caldera, :dampers)
  [portrait: WICK, sad] *(to the PC, without anger)* Then hold its mouth shut, if you must.
  [name: Wick] It'll still have a fever.
  (The Hollow don't fight. They pick up their hose and go up the stair. But the two Hammers you beat aren't gone: they come back down with a third, and this time they're after the dampers.)
  BATTLE: tag battle — PC + Quent (MERIDIAN_QUENT as partner, version 0 [NEW partner flag]) vs [HOLLOW_GRUNT_M "Hammer"] + [HOLLOW_GRUNT_F "Hammer"] (version 8). Field: Volcanic.
  (Quent's partner AI uses Rain Dance on turn 1; the field quenches to Cinderglass, which he narrates.)
  [portrait: QUENT, sad] *(in the battle, at the quench)* Look at that! Isn't that BEAUTIFUL!
  [name: Quent] Glass! Oh, I wish my mother could see this.
  (WIN:)
  (The engineers lock the brass rings round the pipe. The draw evens out. The gauges fall to the amber and stay there, humming.)
  [name: Quent] Done by supper. I said!
  [name: Quent] *(to the PC)* We should do this again. You're very good at holding things.
  V110 CINDERVAULT_STATE = 2.
> Shut the tap down. (shutdown)
  Script: pf_choose(:ch8_caldera, :shutdown)
  (You walk past both of them to the red lever. The Directorate soldiers step together.)
  [name: Directorate Lieutenant] That's Sovereign's property. Step back from it.
  [portrait: QUENT, shocked] Oh, you CAN'T, that's — that's a whole tap, that's MONTHS—
  BATTLE: double battle vs [MERIDIAN_QUENT "Percival", version 0] + [MERIDIAN_DIRECTORATE "Lieutenant", version 8]. Field: Volcanic. (The harder fight: two trainers, one of them an admin.)
  (WIN:)
  (You break the glass and pull. The lever takes your whole weight. Somewhere far down, something very large stops turning.)
  (The pipe groans. The gauges shudder, and drop, and keep dropping, and stop in the green. The forges up the walls stay lit.)
  [portrait: QUENT, sad] *(quietly, to his clipboard)* Seven taps in the realm. Now six.
  [name: Quent] Someone's going to be so cross with me.
  [name: Directorate Lieutenant] This goes to the Directorate. With your name on it.
  [portrait: WICK, sad] *(from the stair)* Spell it right.
  V110 CINDERVAULT_STATE = 0.
(All:)
(Up the stair, out into the night. From the bell-tower, slowly, a single bell: one. All clear.)
[portrait: BRANN, sad] *(at the top of the stair, soot to the eyebrows; he's been carrying people)* One bell. One bell.
[name: Brann] I've never been so glad to hear one bell.
[if :ch8_caldera == :vent] [portrait: BRANN, sad] And my forges are out. All of them. For a season. *(a long breath)* ...Better cold than gone. I'll grumble about it till spring. Let me.
[if :ch8_caldera == :dampers] [portrait: BRANN, happy] And my forges are lit! You kept my forges lit! *(hug)*
[if :ch8_caldera == :dampers] [portrait: LARCH, neutral] *(not looking at the PC)* For now. Ask me in a year how Emberfall's doing.
[if :ch8_caldera == :shutdown] [portrait: BRANN, shocked] You shut it. You actually shut it. With your hands. *(laughing, a little wild)* Sovereign's property! HA!
Switch S120 CH8_CALDERA_DONE = ON. V129 = 6.
```
*(Long-term: `:vent` (HOLLOW+2 MERIDIAN−1 RES+1) turns the Ashmarch to `:ASHEN_WASTE` and leaves Cindervault's forges cold until Ch11; `:dampers` (MERIDIAN+2 VOSS+1 RES−1) keeps the tap running and grows the Bleed at Emberfall (668 map state); `:shutdown` (ACCORD+2 MERIDIAN−3) and the Dominar hears who did it (DOMINAR respect +1). Brann's roll-call line at the Conclave reads this choice (27_SCRIPT_CH9).)*

## The Light Stone (autorun back at 244, V129 == 6): **"Whose Is It"**
```
(Hearthguild Hall, after midnight. The grille over the forge is open. Two oath-guards are lifting the Light Stone out of its cradle in a cloth, and Envoy Haskar is holding the yard door.)
[name: Envoy Haskar] The Warden was occupied. The city was in danger.
[name: Envoy Haskar] The Stone was safest with—
SE: a Salamence's growl, very close, from the yard.
[portrait: SIGRUN, angry] *(in the doorway behind him)* Say true, Haskar.
[name: Envoy Haskar] ...The Dominar told me to take it while everyone was looking at the mountain.
[name: Sigrun] Thank you. Put it down.
(The guards put it down on the basalt table. In the dark hall it lights everyone's faces from below, cold and white.)
(Brann comes in, sees it, and sits down heavily on the bench.)
[portrait: BRANN, sad] Thirty years it's been on that wall. Nobody touched it.
[name: Brann] And tonight I'd have let them, if they'd asked nicely.
[name: Brann] I was carrying a woman's grandmother up four hundred steps.
[name: Sigrun] This won't stop.
[name: Sigrun] My father will send another envoy, and another, and one day he'll send a legion.
[name: Sigrun] *(to the PC)* You've stood in three kingdoms' business this year.
[name: Sigrun] You might as well stand in a fourth.
[name: Sigrun] Say it. Who should keep it?
CHOICE :ch8_lightstone
> The Hearthguild. It's Brann's to keep. (hearthguild)
  Script: pf_choose(:ch8_lightstone, :hearthguild)
  [portrait: BRANN, crying] *(very quietly)* Thank you. *(He puts it back in the cradle and closes the grille himself.)*
  [portrait: SIGRUN, neutral] Then my father's grudge gets heavier, and Brann carries it.
  [name: Sigrun] He's strong. *(to Haskar)* Go home and say true.
> Wyrmrest. A Warden's neutral ground. (wyrmrest)
  Script: pf_choose(:ch8_lightstone, :wyrmrest)
  [portrait: SIGRUN, shocked] ...Mine?
  [portrait: BRANN, neutral] *(slowly)* Hers. Aye. Not the Dominar's. Not mine. A Warden's, with dragons round it. *(he nods)* That's the Concordance done properly. I'm too fond of the thing to have thought of it.
  [name: Sigrun] My father will hate it. He can't argue with it.
  [portrait: SIGRUN, smug] *(to the PC; something like a smile)* You think like a rider.
  (The choice itself seeds the Ch19 petition: the Dominar respects his daughter's claim more than Brann's, so `:ch8_lightstone == :wyrmrest` makes `:ch19_dominar == :swayed` reachable.)
> The Dominar. It's his people's. (dominar)
  Script: pf_choose(:ch8_lightstone, :dominar)
  (Brann doesn't say anything. He looks at the PC for a long time, and then at the stone, and then at his hands.)
  [portrait: BRANN, crying] ...Take it, then, Haskar.
  [name: Brann] Tell him the ferry child said.
  [portrait: SIGRUN, angry] *(to the PC, cold)* You've just told a man who wants a war that the war's right.
  [name: Sigrun] Remember you did.
  [portrait: LARCH, sad] *(later, on the steps)* He'll forgive you. He forgives everybody.
  [name: Larch] He won't forget, though. Smiths don't.
(All:)
V129 = 7.
```
*(SIGRUN+2 ACCORD+1 on `:wyrmrest`; SIGRUN−2 ACCORD−1 on `:dominar`, and Brann's Act V Consent refuses "for a man who gave the Light Stone away" (NARRATIVE_KEYS row 7); Reshiram's trial at Wyrmrest is harder on `:dominar`. `:hearthguild` costs nothing now and the Dominar's grudge in Ch11.)*

## Map 244 — Hearthguild Hall, later: **"Chestnuts"** (V129 == 7 → 8; the slip)
```
(Two in the morning. The Hall's forge, the one that's still lit (or, on :vent, a brazier somebody's carried in). Brann roasting chestnuts in an iron pan. Larch with her boots off. Mulled cider in a jug that has been refilled more than once.)
[portrait: BRANN, happy] *(peeling a chestnut with thumbs like spoons)* I'll tell you a thing about chestnuts, ferry child.
[name: Brann] You've to cut a cross in 'em first.
[name: Brann] Else they go off like a Voltorb.
[portrait: LARCH, deadpan] He told me that in AF 271. And AF 280. And AF 288.
[name: Brann] And it's still TRUE!
(He pours. He's three cups in. He looks at the forge for a while, the way people do at two in the morning.)
[name: Brann] Thirty years at this anvil. You know the best thing I ever made?
[name: Brann] Not a blade. A setting.
[name: Brann] A little gold setting for a little white stone.
[portrait: BRANN, sad] I reset the Crown's stone myself, y'know. After the accident. Ten years back.
[name: Brann] It was smaller than it should've been.
(The PC's chest goes tight, all at once, as if something under the ribs has been flicked with a fingernail. A single note, too low to hear. Then nothing.)
[portrait: LARCH, neutral] [emote: dots] *(her eyes on the PC, not on Brann)* ...
[portrait: BRANN, shocked] *(catching himself)* Ach. Ach, I'm an old fool.
[name: Brann] Forget it. Cider talking. Forget it.
[portrait: BRANN, neutral] Have a chestnut. Cross on top. *(He doesn't look at either of them for a while.)*
[portrait: LARCH, neutral] *(later, alone with the PC, at the door)* You flinched. Just then. When he said "smaller".
> It was nothing.
  [portrait: LARCH, neutral] It's always nothing.
  [name: Larch] I've got a notebook full of nothings. They're starting to rhyme.
> I don't know what it was.
  [portrait: LARCH, sad] No. Neither do I. That's the bit I don't like.
> ...
  [portrait: LARCH, sad] All right. Go to bed.
  [name: Larch] I'm going to write something down and then pretend I didn't.
FIELD NOTES: "Brann reset the Crown's stone ten years ago. It was 'smaller than it should've been'. Something in me answered when he said it. I don't know what that means. I'm writing it down so I can't pretend I didn't hear it."
V129 = 8.
```
*(09 #5 the reset, #6 the cracked Crown: one sentence, no explanation. The ring's payoff is Ch14 (Bastian); the Crown's is Ch15–17. Brann names neither the Legend Plate nor the reset's reason.)*

## Map 240 — the caldera square: **"The Herald"** (autorun next morning, V129 == 8 → 9; the cliffhanger)
```
(Morning. On :vent the square is grey with ash and the smiths are sweeping it into the cold channels. On :dampers and :shutdown it's busy and loud and the forges are going.)
SE: drums. Not the Hearthguild's bells: war-drums, big ones, coming up the Pyre Road.
(A column in red lacquer comes into the square: twelve oath-guards, a standard with the gold dragon of the Dominar, and a herald on a Rapidash who doesn't get off it.)
[name: Dominar's Herald] By the Dominar of Ashkaar, the Dragonfire, Keeper of the Flame and the Oath.
[name: Dominar's Herald] Say true, and hear true.
[name: Dominar's Herald] Last night the Sovereign of Zenith put a pipe into the Flame of Ashkaar and near-burned a city of the Dominion to the rock.
[if :ch8_caldera == :shutdown] [name: Dominar's Herald] It was shut by a child from Elowen with their own two hands, while Zenith's soldiers stood in front of the lever. The Dominar has marked it.
[if :ch8_caldera == :dampers] [name: Dominar's Herald] Zenith's engineers have since bound the Flame with brass and call it mended. The Dominar does not.
[if :ch8_caldera == :vent] [name: Dominar's Herald] The Flame was quenched by the Hollow's faithful to save the city, and Cindervault's forges are cold. The Dominar holds Zenith accountable for every one.
[name: Dominar's Herald] Therefore. The Dominar holds Zenith responsible for this assault upon the Flame.
[name: Dominar's Herald] From this hour the eastern passes of Ashkaar are closed to Meridian, to its rails, its taps and its soldiers.
[name: Dominar's Herald] And the Flame of Ashkaar will no longer warm the beds of Isenmar.
[name: Dominar's Herald] Let the Thane find his heat in his own cold lake.
[name: Dominar's Herald] Say true: this is not war. *(a pause)* It is the door to it.
(The drums start again. The column turns and goes down toward the Ashmarch. The square is very quiet.)
(Sigrun is on the bell-tower's balcony above the square, in her riding leathers, watching her father's banner go. The PC can see her face from the square. She says nothing at all.)
[portrait: BRANN, sad] *(beside the PC)* Well. There it is.
[name: Brann] I've seen that standard come up that road twice in my life.
[name: Brann] Both times it took ten years to go home.
[portrait: LARCH, neutral] The Sovereign's called the Wardens to Ironreach. A Conclave.
[name: Larch] Every Warden in the realm in one room.
[name: Brann] Aye. I'll see you there.
[name: Brann] Sigrun will too, if her father lets her, and he won't, and she'll come anyway.
Switch S121 CH8_WAR_DRUMS = ON. V122 WAR_STATE = 1. V129 = 9.
```
*(Ashkaar NPCs swap dialogue on S121: the passes, the Legion recruiting tables on the Ashmarch (27_SCRIPT_CH9 opens on one), Haskar's absence.)*

## Map 243 — the Caldera Gate (leaving; V129 == 9 → 10)
```
[name: Gate Smith] West gate's open. East's shut.
[name: Gate Smith] First time in my life the mountain's been on the right side of a door.
[if :ch8_lightstone == :wyrmrest] [name: Roost Rider] (at the Dragon Roosts' stair) The Wardeness flew the Light Stone to Wyrmrest at dawn. She held it like an egg. I've never seen her hold anything like that.
[if :ch8_lightstone == :dominar] [name: Hearthguild Smith] The Stone's gone east with the envoy. The Warden's been at the anvil since dawn. Not making anything. Just hitting it.
[if :ch8_lightstone == :hearthguild] [name: Hearthguild Smith] The Warden's put a second grille on the Stone. And a third. He's making a fourth. We've told him that's enough grilles.
QUEST LOG: "Eighteen Roads" — Earn the eighth badge in Ironreach. West out of Ashkaar, along the Ashmarch and down the Long Drop.
V129 = 10. V102 STORY_CHAPTER = 9.
```
*(27_SCRIPT_CH9 opens on the Ashmarch with Larch's goodbye at the first mile-fort.)*

---

## Side content in Chapter 8
- **The Ashkaar board** (TRIALS_QUESTS, Ch8, `badges >= 6`): "Seven Bouts" (the Crucible, 240; the Octave's Ashkaar duel), "The Lava-Tube Terror" (664), "Adequate Swords" (the market, 240), "Afraid of Heights" (the Dragon Roosts, 248), "Ashes Home" (Scaldwater, 650), "The Egg Run" (248), "The Trial of Truth" (the Hall of Oaths, 247; `switch(120)`).
- **Pyre Keep** (245–248, 254): the Dominar's seat in Cindervault. The Ember Throne (246) is empty: the Dominar is at the capital. The Hall of Oaths (247) holds the Trial of Truth. The Ancestor Crypts (254) are closed until Act IV.
- **Cameos:** none in Ch8 (CAMEOS.md).

## Maps to build (this chapter)
| Map | Needs |
|---|---|
| 640 Leechman's Walk | plank walks on stilts, every tenth lantern lit, Larch on the first platform (V129 0 → 1) |
| 641 Lake Sallow | steaming lake, sulfur crusts, the suspended ferry-stage, Surf east; Lantern Isle reachable |
| 650/651 Scaldwater + PC | terraced bath-houses, the Hollow faithful in the low bath (V129 1 → 2) |
| 658 Lantern Isle (opt.) | unlit lighthouse, the keeper's logbook, Lapras in the cove |
| 652 The Pyre Road | basalt switchbacks, red banners, the oath-gate with brazier and bronze hand (V129 2 → 3) |
| 243 Caldera Gate | the gate stair, the view down into the crater, "The Hug" autorun (V129 3 → 4) |
| 240 Forge Terraces | honest shop signs, quench-channels glowing at V129 ≥ 5, the square for the herald; ash on the ground when V110 == 1 |
| 244 Hearthguild Hall | basalt table, forge, the Light Stone behind its grille (grille count by `:ch8_lightstone`), Sigrun's entrance from the yard |
| 249 Slag Ward | slag-brick shacks, families on the stairs at V129 == 6, the tap's service stair |
| **255 Tap Chamber [NEW]** | round iron room, the pipe, gauge ring, Wick's hose at the sluices, Quent's valves, the red emergency lever under glass; field :VOLCANIC |
| 250–253 the Foundry | per GYM_PUZZLES Gym 7 |

## New data this chapter needs
- **Trainers:** in `pbs/trainers.txt` (2026-11-21): `HOLLOW_GRUNT_M/F "Hammer"` v8/108/208, `MERIDIAN_DIRECTORATE "Lieutenant"` v8/108/208. `MERIDIAN_QUENT` v0 doubles as the dampers partner (still needs a `MERIDIAN_QUENT_back.png` partner back sprite: Gemini art list).
- **Items:** QUENCH BADGE (badge 7 name; story docs only); TM35 from Brann (GYM_PUZZLES).
- **Flags:** V129 CH8_STEP is now used as above (design/FLAGS.md); `:ashkaar_watched` is a map-story flag (`pfm_set`/`pfm_get`).
- **Game over:** GO_LET_THEM_LISTEN (NARRATIVE_KEYS §9), checkpoint at the top of the tap stair.
