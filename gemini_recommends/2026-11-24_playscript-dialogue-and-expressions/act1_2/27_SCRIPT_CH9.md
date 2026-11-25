# Script: Chapter 9 — "The Iron Conclave" (the Iron Road, Ironreach, Gym 8; K4; the Conclave; the Mourner unmasked; Interlude II)

> **Final playable script (Playscript & Restrained Rejuv Expressions Edition)** for Chapter 9, the end of Act II (`014_Portraits.rb` + `018_ExpressiveDialogue.rb` v2). It covers the Iron Road (660 the Ashmarch, 661 the Ironway, 602 Candle Down, 672 the Long Drop) down into Nadir, then Ironreach (260–263, two new rooms 264/265), the Ironreach Open and K4 in the Iron Pit (263), Kaito's gym (270–275, Gym 8), the Conclave and the attack (263/264/265), and Interlude II at the Heartgarden (294) as Rowan. None of these maps is built; the list at the end is what to build from.
> Follows `story/26_SCRIPT_CH7.md`. Chapter 8's script is `story/29_SCRIPT_CH8.md` (it replaced the withdrawn Ring-Day in `22_SCRIPT_CH8.md`); this chapter reads its results for continuity: `:ch8_caldera`, `:ch8_lightstone`, V110, S120/S121, Brann's chestnut slip and the Dominar's herald.
> Sources: 05_ACT_II Ch9 and Interlude II, 03_CAST (Kaito, Kestrel, Juno, Rowan, the Wardens), 09_MYSTERIES (#2, #2a, #4, #12, #16, #17, #27, #29), NARRATIVE_KEYS (`:ch9_teo_sable`, `:ch9_rowan_words`, GO_PULL_THE_NAIL), 14_WAR_AND_BLESSING (the Ch9 insert), 15_COMEDY (Ch9 "The Bracket"; running gag 3; the pit announcer), GYM_PUZZLES Gym 8, TRIALS_QUESTS (the Gutter Book, Ch9), CAMEOS (Garret), BALANCE and the trainer PBS (K4, Kaito, Sable + Brisk, the Mourner), `design/CHAPTER_BEATS.md`.

## Conventions
- **Playscript Multi-Box Rhythm:** Crisp 1–2 line RPG Maker message boxes (`<= ~85 chars`), separated onto consecutive lines for beats (`...`), cutoffs (`—`), and listener cut-ins.
- **Restrained Rejuv-Style Expressions** (`014_Portraits.rb` + `018_ExpressiveDialogue.rb` v2 — static `96×96` portraits, `0px` motion):
  - `[portrait: CAST_ID, expr]` ONLY on a cast speaker's **first line in a conversation** and on **earned emotional turning points** (~20–28% of cast spoken boxes; roll-call naturally introduces each of the 18 Wardens once on entrance). 11 expressions: `neutral, happy, angry, sad, surprised, smug, shocked, panic, blush, crying, deadpan`.
  - `[name: Display Name]` holds the speaker's current portrait/expression via `Portrait.carry` across **70–80%** of cast lines, and is used for all generic NPCs.
  - `\pfe[emote]` (`exclaim, double_exclaim, question, dots, anger, sweat, heart, idea, music, jolt`) and `[bubble: ...]` used sparingly (`0–2` per conversation).
- **Verified portrait cast here (`graphics/Portraits/`):** `LARCH, KESTREL, JUNO, KAITO, ROWAN, MOURNER, SABLE, TEO, MARISOL, VALEN, HOLLIS, MARCHETTI, VOSS, CALLA, BRANN, CORVIN, DORIAN, TAMSIN, ROOK, SAHAR, SIGRUN, ANJA, ODESSA, ILSA, BASTIAN, YSOLDE, MAGNUS, NYX, CELESTINE`. **Plain:** Nell the chalk-girl, the pit announcer, Captain Brisk, the envoys (the Dominar's, Kassan's), the Open's pit-fighters, Six-Fingers Ottoline, Garret (cameo), every townsperson, guard and trainer. Events call `Prismfall.gym_battle(pfm_gym(:LEADER_KAITO), double: false)`: Gym 8 is a **single** battle (Core `GYMS`; BALANCE). Kestrel's tag battle is the Sable + Brisk fight, not the gym.
- **Counter:** V130 **CH9_STEP** (design/FLAGS.md): 0 leaving Cindervault · 1 Larch's goodbye on the Ashmarch · 2 down the Long Drop into Ironreach · 3 the Conclave opens (the roll-call) · 4 the Open sign-up ("The Bracket") · 5 K4 won (S122) · 6 Gym 8 won (Fly) · 7 the vote and the attack (Sable + Brisk) · 8 the Mourner unmasked (S124) · 9 `:ch9_teo_sable` made · 10 the aftermath (Rowan led away; S123) · 11 Valen: "Come to Verdance" · 12 Interlude II done (V101 = 3, V102 = 10).

## The chapter's key events (design/CHAPTER_BEATS.md)
1. **The Mourner unmasked.** The Hammer rigs the Fist Plate's reliquary; the Mourner is there to *disarm* it; the charge goes off; his Trevenant's roots wall off the glass racing at Juno and the chalk-girl Nell, and his mask takes the burst. "...Uncle Rowan?" Build-up: Juno's ledger (Ch7), Rowan's bandaged right hand and bare ring finger at the roll-call, the Mourner's "get BACK". Payoff: the mask in two halves on the floor. Consequence: Rowan in Meridian custody (V113 = 1), Juno's seat (Ch10), Kestrel's "It's not her".
2. **`:ch9_teo_sable`.** Teo pinned and Fixing under the scaffolding; Sable running for the lift with the comm-device. One life against one proof. Build-up: Teo glimpsed in the shafts, Marisol at the roll-call not knowing where he is. Consequence: Teo alive with glassed fingers, or dead reaching for his sister; Kroll's public exposure (Ch13).
**No jokes** from the moment the galleries go dark until Valen leaves the Pit (15_COMEDY §1: Rowan's unmasking). The comedy scene "The Bracket" sits on the sign-up day, well before. Side content: the Open's undercard and the Gutter Book's board close at V130 == 6 (the gym won) until V130 >= 10, so nothing sends the player away between the gym and the vote.

---

# CHAPTER 9 — "The Iron Conclave"

**Chapter start:** V102 = 9, V130 = 0 (Ch8 close: the Dominar's herald; S121 CH8_WAR_DRUMS on). The PC leaves Cindervault by the west gate.

## Map 660 — The Ashmarch: **"Eight Years Late"** (autorun at the first mile-fort, V130 == 0 → 1)
```
ROAD SIGN: THE ASHMARCH — Ashkaar. ← the Ironway (to Elowen and Nadir) · → Cindervault. Sweep your boots at the mile-forts. The Legion will.
(The legions' marching road, grey with ash. At the mile-fort a recruiting table: a red banner, a brazier, and a queue of young men and women holding their own swords.)
[name: Legion Recruiter] Say true or say nothing. Do you want to fight for the Dominar?
[name: Forge Apprentice] ...I want to eat.
[name: Legion Recruiter] That's true. Sign here.

(Larch is sitting on the fort's mounting-block with her oilskin buttoned to the chin and a carpet-bag at her feet.)
[portrait: LARCH, neutral] There you are.
[name: Larch] I've been sitting on this block for an hour being looked at by soldiers.
[name: Larch] I'm told it's an honour.
[name: Larch] I'm not coming to Ironreach.
[name: Larch] I've a report to finish. I started it in AF 292.
[name: Larch] It's eight years late, and every time I look at it there's a new chapter.
[name: Larch] Ebbmouth's river. The Lowlight. Brann's caldera.
[name: Larch] It's all the same chapter, really.
[name: Larch] I just keep having to write it again with more people in it.
> Where are you going?
  [portrait: LARCH, deadpan] Somewhere with a transmitter and a Warden who doesn't do what she's told.
  [name: Larch] I'll write.
> Is it about the Lattice?
  [portrait: LARCH, sad] It's about the person who built it.
  [name: Larch] Which is worse, because I can't blame her.
> ...
  [portrait: LARCH, deadpan] Yes, I'll miss you too. Don't make it a whole thing.
[portrait: LARCH, neutral] Kaito Ren keeps the gym at Ironreach.
[name: Larch] He was Wardguard. He doesn't talk. You'll get on.
[name: Larch] And the Sovereign's called a Conclave there.
[name: Larch] Every Warden in the realm in one hole in the ground—
[name: Larch] —and a Hammer loose that's already broken one Plate.
[portrait: LARCH, angry] So if anything in Ironreach starts to hum, or glow, or go quiet in the wrong way—
[name: Larch] —you will walk AWAY from it.
[name: Larch] This is Lecture Eleven. I'm delivering it in advance to save postage.
(Received: KELP TEA BAG. "Six.")
[portrait: LARCH, sad] Look after Juno.
[name: Larch] She's going to need somebody who doesn't need anything back.
MOVE: Larch picks up the carpet-bag and walks east toward Cindervault's coaching-yard, not looking back, which is how she does it.
V130 = 1.
QUEST LOG: "Eighteen Roads" — Earn the eighth badge in Ironreach, down the Long Drop into Nadir.
```
*(Larch's report is the Larch Papers, Ch12. "A transmitter and a Warden who doesn't do what she's told" is Odessa. V115 LARCH_STATUS stays 0 until Ch12.)*
```
[name: Sweeper] (at the second mile-fort, with a broom taller than she is) Ash falls every day.
[name: Sweeper] We sweep it every night. The Dominar says it's discipline. I say it's ash.

[name: Legion Veteran] The passes are shut to Zenith.
[name: Legion Veteran] You'll be the last thing out of Ashkaar that isn't a soldier. Walk fast.
```

## Map 661 — The Ironway (borderland E, `:MOUNTAIN`)
```
ROAD SIGN: THE IRONWAY — the Sulfur Reach. ← Candle Down & the Crown Road (Elowen) · → the Ashmarch (Ashkaar). Ore down, money up. Keep off the incline.
(The ore-pass out of the Dominion: rails laid by Nadir, paid for by Ashkaar, down through burnt woods to the Leach ford. At the top, a Truce Post: a stone with two carved hands on it, one Ashkaar's, one Elowen's. Someone has chalked a hammer between them.)
TRUCE POST (inspect): "HERE NO BLADE IS DRAWN. AF 211." Under it, the chalk hammer, and smaller: "UNTIL THEY LISTEN."

[name: Ore-carter] The Hammer's been through. They chalk everything.
[name: Ore-carter] They chalked my cart. They chalked my Rhyhorn.
[name: Ore-carter] He's a peaceful Rhyhorn. He doesn't want to be political.

[name: Elowen Forester] (at the ford) Ashkaar's closed its passes and Nadir's under the Mandate.
[name: Elowen Forester] The only people who can cross this ford now are you and the ore.
[name: Elowen Forester] And the ore needs papers.
```
*Trainers on 661 (trainer designer): ore-carters and Legion deserters going the other way.*

## Map 602 — Candle Down (the Crown Road, east; second visit)
```
CAIRN (any, inspect; V130 >= 1): The twelve candles from the Lowlight are still here, burned to stubs. Somebody has added a thirteenth to every cairn, a fat red Ashkaar candle.

[name: Pilgrim] The thirteenth's for Cindervault. The caldera.
[name: Pilgrim] Nobody died, they say. So why does it feel like somebody did?

[name: Coaching-inn Keeper] Every Warden in Velmora's come through here this week, going down to Ironreach.
[name: Coaching-inn Keeper] The Grass Warden had a bandage on his hand and the best manners of any of them.
[name: Coaching-inn Keeper] Paid for a Lady in Briar Hall's dinner because she'd forgotten her purse.
[name: Coaching-inn Keeper] She hadn't. She just wanted to see if he would.
```
*(09 #2: Rowan's bandage, first mention on the road.)*

## Map 672 — The Long Drop: **"The Cage"** (the winding-tower at the Crown Road's south junction; V130 == 1 → 2)
```
ROAD SIGN: THE LONG DROP — Ironreach's front door. ↓ Ironreach (NADIR) · ↑ the Crown Road. One hour down. Two hours up. Nobody knows why it's an extra hour up. Everybody knows.
(A winding-tower over a shaft under Zenith's west rim. A cage lift clanks on its cable. At the cage gate, a brass barrier, a scanner plate on a post, and two officers in white-and-gold.)
[name: Directorate Officer] Mandate checkpoint. Nadir lifts are Lattice assets.
[name: Directorate Officer] Hand on the plate.
MOVE: the PC's turn. SE: chime... nothing. NULL.
[name: Directorate Officer] ...You're the null. You're on everybody's list.
[name: Directorate Officer] "Do not detain." I'd love to know why.
[name: Directorate Officer] *(to her partner, not quietly enough)* That's the one who walked in the Lowlight.
(The barrier goes up. The cage door rattles shut behind you.)
(The cage drops. The light goes amber, then red, then nothing but the lamp on the cage roof. Rock goes past. More rock. Somebody has scratched a tally on the cage wall: hundreds of little lines, and under them, "COUNT THEM. IT HELPS.")
WAIT 60.
(The cage stops with a bang. The gate opens onto noise.)
V130 = 2.
```
*Trainers on 672 (trainer designer): the shaft road's side galleries (miners, scrap-dealers); SCRAPYARD field.*

## Ironreach (260–265; Nadir; the pit-fighting quarter)

### Map 260 — Ironreach: arrival (autorun at the cage-foot, V130 == 2)
```
(Aurel-era mine shafts, hollowed into a town. Galleries on galleries, lit by lamps on chains. Everywhere you look, chalk circles on the ground, and in every circle two people arguing with their fists, and round every circle a crowd. It's loud, sweaty and honest.)
[name: Pit Announcer] *(from a gantry, through a brass trumpet)* AND HERE COMES A NEW ARRIVAL OFF THE LONG DROP, FOLKS!
[name: Pit Announcer] FIFTEEN, MAYBE SIXTEEN. GOOD SHOES.
[name: Pit Announcer] IT'S... THE NULL KID! THE NULL KID IS IN IRONREACH!
[name: Pit Announcer] AND THE NULL KID IS... LOOKING AT ME, FOLKS.
[name: Pit Announcer] THE NULL KID HAS A VERY STRAIGHT FACE.

[name: Miner] He does that. He narrates. He's done it for thirty years.
[name: Miner] He narrated my wedding. He narrated my divorce. It was the same speech.

[name: Chalk-circle Woman] Got an argument? Draw a circle. Settle it. Leave.
[name: Chalk-circle Woman] That's Ironreach. Topside they have courts, it takes three years, and nobody's happy.

[name: Nadir Boy] The Conclave's here! All the Wardens!
[name: Nadir Boy] I saw the fire one. He's as big as a door.
[name: Nadir Boy] He picked me up to see better and then forgot to put me down.

NOTICE (on the cage-foot): "BY MANDATE: A CONCLAVE OF THE ACCORD WILL SIT IN THE IRON PIT. THE IRONREACH OPEN WILL PROCEED AS ENTERTAINMENT. — A. HOLLIS, CHANCELLOR." Under it, chalked: "ENTERTAINMENT FOR WHO."
```
*(15_COMEDY §5, Nadir: the pit announcer narrates everything the PC does in town. Give him three more town lines on a page per V130: "AND THEY'RE OPENING THE DOOR, FOLKS." at the PC's door, "AND THEY'RE BUYING POTIONS. SENSIBLE. VERY SENSIBLE. BORING." at the Mart, "AND THEY'RE ASLEEP, FOLKS. LOOK AT THEM. LIKE A BABY." outside 261 after a heal.)*
*Trials in 260: the Gutter Book's chalk board (Six-Fingers Ottoline at the Last Rung): "Lamplighter Kids" (NA_LAMPLIGHTER_KIDS), "Pit Ringer" (NA_PIT_RINGER, posted by the announcer). Both close while V130 is 6–9.*

### Map 263 — the Iron Pit: **"The Conclave Opens"** (autorun on first entry, V130 == 2 → 3)
```
(The Iron Pit: a mined-out cavern the size of a cathedral, with a fighting floor of packed red earth at the bottom and tier on tier of galleries cut into the rock all the way up. Tonight the lowest gallery is hung with eighteen banners, one for every Plate. On the floor, under the lamps, a long table. At its head, a broad man in white with a grey glove, and beside him a smaller, smoother man with a ledger.)
(In the gallery above the Wardens, the observers' gallery: the kings' envoys, in a row, not quite looking at each other.)
[portrait: HOLLIS, smug] Chancellor Ambrose Hollis, for the Accord.
[name: Hollis] The Conclave of AF 300 is in session.
[name: Hollis] The first held in Nadir in a hundred and four years.
[name: Hollis] I'm told the acoustics are extraordinary.
[name: Hollis] I'm told a great many things down here. Most of them through a trumpet.
[name: Pit Announcer] *(from the gantry)* AND THE CHANCELLOR IS MAKING A JOKE, FOLKS.
[portrait: HOLLIS, deadpan] ...The roll of the Wardens.
```
**The roll-call** (one entrance per seat; Hollis reads the seat, the Warden answers. The PC watches from the challengers' bench at the floor's edge.)
```
[name: Hollis] Saltmere.
[portrait: DORIAN, happy] Present, darling, and lit from the left, if anybody's asking.
[name: Dorian] Nobody ever asks.

[name: Hollis] Briarwick.
[if :ch2_tamsin == :expose]
  [portrait: TAMSIN, neutral] Present. Sorry. Present.
  [name: Tamsin] ...Briarwick's books are open, if the Conclave wants to read them. Everyone else has.
[if :ch2_tamsin == :help_confess]
  [portrait: TAMSIN, panic] Present! Sorry.
  [name: Tamsin] I renegotiated a contract last spring and I've been apologising to paper ever since.
[if :ch2_tamsin == :keep_secret]
  [portrait: TAMSIN, sad] ...Present. *(She doesn't look up from her hands.)*

[name: Hollis] Ebbmouth.
[portrait: MARISOL, neutral] Present. For the Guild.
[name: Marisol] The Guild votes no on anything with "Mandate" in it—write that down before you ask.

[name: Hollis] Lumen.
(No drone. A young man in a plain hooded jacket at the end of the table.)
[portrait: ROOK, sad] Here. Chat's off. Don't ask.

[name: Hollis] Duneholt.
[portrait: SAHAR, neutral] Present, with a cough, and a well that's dropped four rungs since spring.
[name: Sahar] I'd like that in the minutes. Spell it with an H.

[name: Hollis] Mirefen.
[portrait: CORVIN, deadpan] Present. I've brought my apprentice's best friend as my plus-one.
[name: Corvin] Since my apprentice can't be trusted with stairs.

[name: Hollis] Cindervault.
[if :ch8_caldera == :vent]
  [portrait: BRANN, sad] HERE. With cold forges, a grumble—
  [name: Brann] —and a great deal of respect for the person who made them cold.
[if :ch8_caldera == :dampers]
  [portrait: BRANN, happy] HERE! Forges lit, all of them.
  [name: Brann] Ask me how. Ask the challenger how.
[if :ch8_caldera == :shutdown]
  [portrait: BRANN, happy] HERE. The tap's shut and the Dominar's still talking about who shut it.
  [name: Brann] Look at the bench, Ambrose.

[name: Hollis] Ironreach.
[portrait: KAITO, neutral] Here.
(That's all he says. Hollis waits for more. There isn't any.)

[name: Hollis] Verdance.
(A rangy man with soil under his nails, a soft burr of a voice, and a clean white bandage wound round his right hand from the knuckles to the wrist.)
[portrait: ROWAN, happy] Present. Forgive the hand. Kettle.

[name: Hollis] Rimeholt.
[portrait: ANJA, deadpan] Here. It's forty degrees and there's a ceiling.
[name: Anja] Southerners call this a city.

[name: Hollis] Skyreach.
SE: a propeller, very close. A courier skiff drops over the Pit's rim on a rope, hovers, and a woman in goggles and a scarf slides down the rope onto the table.
[portrait: ODESSA, happy] Present! Courier's privilege.
[name: Odessa] The cage queue was forty minutes. I'm not queueing for a vote.

[name: Hollis] Lucent.
(At the far end of the table a silver-haired woman in high-collared robes sits with noise-cancelling earmuffs on, as far from the Sovereign as the table goes. She lifts one hand and doesn't speak.)
[name: Hollis] The Provost is present. Cragholm.
[portrait: BASTIAN, happy] Eh?
[name: Hollis] Cragholm, Warden Ore.
[name: Bastian] No, I've had my supper, son. Thank you.

[name: Hollis] Gravenmoor.
(High in the lowest gallery a veiled woman with a lit lantern stands up, says "Present" so softly the trumpet doesn't catch it, and sits down. She is looking at the challengers' bench. Not at you. Past you.)

[name: Hollis] Cogsworth.
[portrait: MAGNUS, neutral] Present. Strade.
[name: Magnus] I have the Mandate's technical annex in front of me, Chancellor.
[name: Magnus] I've corrected the arithmetic on page nine.

[name: Hollis] Underveil.
[portrait: NYX, smug] Oh, I'm not on the table, darling. I'm in the gallery.
[name: Nyx] Underveil isn't seated. It just attends.

[name: Hollis] Gloaming.
(A barefoot young woman in moth-silk, with flowers in her hair that are just starting to open, though there's no sky down here to tell them it's dusk.)
[portrait: CELESTINE, happy] Present. I'm always present. That's rather the problem with me.

[name: Hollis] Wyrmrest.
[portrait: SIGRUN, neutral] Here. And my father's envoy is in the gallery.
[name: Sigrun] So if the Conclave hears shouting from up there, it isn't me.

[name: Hollis] Eighteen Wardens present.
[name: Hollis] Sixteen at the table, which is a quorum—
[name: Hollis] —and two who prefer the galleries. A tradition.
[portrait: VALEN, neutral] Thank you, Chancellor.
[name: Valen] We are here for one question.
[name: Valen] The Mandate was granted in Lumen, in a night, for Lumen.
[name: Valen] The Directorate asks for it everywhere, for as long as it takes.
[name: Valen] We'll hear it, and argue it, and vote when the Fist Plate is brought up for the oath.
[name: Valen] In the meantime, I'm told the Ironreach Open is the best thing in Nadir.
[name: Valen] Go and watch it.
[name: Valen] Not from the Accord—from a man who used to fight in it.
V130 = 3.
```
*(09 #2: the bandage and "Kettle"; the bare ring finger is in the free-roam lines below. #17: Ilsa as far from Valen as the table goes; she leaves whenever he stands. #2a: Ysolde looking past the PC at Kestrel. Rev 5: Ysolde, Nyx, Celestine, Anja, Bastian and Magnus are met here, which is the first of their two meetings before the Festival.)*

### Map 263 — the Iron Pit galleries (free roam; V130 >= 3, until V130 == 6)
```
JUNO (with Rowan, at the foot of the Wardens' stair; first talk):
(Juno has her arms round the Grass Warden's middle and hasn't let go.)
[if :ch7_ledger == :reassure]
  [portrait: JUNO, happy] \PN! Look who's here!
  [name: Juno] He came all this way and he didn't even write first!
  [name: Juno] *(holding his bandaged hand up, very gently)* The kettle. The famous kettle.
  [name: Juno] You've had forty years of kettles.
  [portrait: ROWAN, happy] Forty years and one bad morning. Leave it be, love.
[if :ch7_ledger == :name_him]
  [portrait: JUNO, neutral] Hello.
  (She is holding his bandaged hand. She is looking at it. She doesn't look at you.)
  [portrait: ROWAN, neutral] Juno says you've been to Mirefen.
  [name: Rowan] She says you were very honest with her there. She didn't say about what.
[if :ch7_ledger == :ask_corvin]
  [portrait: JUNO, happy] \PN! He's here!
  [name: Juno] Uncle Rowan, this is the one I write about!
  (Across the gallery, Corvin is watching the bandage. When he sees you see him, he looks at the ceiling.)
[portrait: ROWAN, happy] You've grown. Juno's letters are half seeds and half you, did you know?
[name: Rowan] I've been reading about your Pokémon for a season.
[name: Rowan] I feel I could pick them out of a crowd.
[name: Rowan] You held that Phantump at the station. It's grown too.
[name: Rowan] Still won't go near anyone else.
[name: Rowan] You're here for the Open. Good. Somebody down here should be here for a game.
(He lifts his left hand to tuck a blossom back into Juno's wreath. On the third finger there's a pale band of skin where a ring was.)
[name: Juno] Where's your ring?
[name: Rowan] Being sized.
```
*(09 #2: the ring's absence is the Interlude II payoff, where he seals it into his testament.)*
```
CORVIN (the Wardens' gallery):
[portrait: CORVIN, neutral] I'm a doctor.
[name: Corvin] I have one professional observation about the Grass Warden's hand—
[name: Corvin] —and I'm not making it.
[name: Corvin] Juno's been brilliant all week. She restarted my stills twice. Let her have tonight.

DORIAN (by the banners):
[portrait: DORIAN, happy] *Act Two, scene the last: the Wardens descend into the underworld.*
[name: Dorian] Oh, don't look at me like that.
[name: Dorian] Somebody has to say these things out loud, or they just happen.
[if :ch5_lowlight_testimony == :mourner]
  [portrait: DORIAN, neutral] I had your telegram's reply by heart before I sent it.
  [name: Dorian] The pageant version. Well. It sells.

MARISOL (by the water-butts):
[if :ch4_teo == :report]
  [portrait: MARISOL, angry] Kid. You told a Meridian guard my brother's name with me standing there.
  [name: Marisol] I'm not going to hit you, because Kaito's watching. Keep walking.
[else]
  [portrait: MARISOL, neutral] Teo's not here, before you ask. I don't know where he is.
  [name: Marisol] That's the truth, and I hate it. Last letter said "somewhere useful".
  [name: Marisol] Useful. He's nineteen. Nobody's useful at nineteen. You're just loud.

ANJA AND THE ENVOYS (the observers' gallery):
[name: Envoy of the Dominar] (a scarred woman in red lacquer, loud) Our fire warms our enemies' beds, Warden!
[name: Envoy of the Dominar] Every ember in Rimeholt's towers was dug out of the Cinderhorn.
[portrait: ANJA, angry] Then send me a bill.
[name: Anja] I'll send you a bill for every child who'd have died this winter without it.
[name: Anja] We'll see whose is longer.
[name: Envoy of the Dominar] You'll get a bill. It won't be written in ink.
MOVE: Anja stands up. The envoy stands up. Between them, a smiling man in caravan silk with a leather wallet in his lap stays seated.
[portrait: VALEN, neutral] *(from the floor, not loudly)* Warden Sorrel. Envoy. Sit down.
(They sit. The man in silk takes two papers out of his wallet and slides one to each of them.)
[name: Envoy of Ossaria] For your masters, with the Prince-Elector's compliments.
[name: Envoy of Ossaria] A small matter of land. Sand, really. Nobody's using it.
(Later, if the PC looks again: both papers are gone, and both envoys' seals are missing from their sashes. The man in silk has left.)
```
*(14_WAR_AND_BLESSING, the Ch9 insert: the first copies of the Elector's Lease. 09 #29.)*
```
NYX (the observers' gallery, end seat; she waves the PC over):
[portrait: NYX, smug] There it is. The child everyone's whispering about.
[name: Nyx] Sit. I've bought you a drink.
(It's a glass of milk.)
[name: Nyx] I'm told you're fifteen. I'm told everything about you, sweetheart.
[name: Nyx] It's very dull for me. Drink up.

CELESTINE (the lowest gallery, barefoot on the rock):
[portrait: CELESTINE, happy] We've met. You didn't know it yet.
> At Briarwick? The old woman at the shrine?
  [portrait: CELESTINE, smug] I can't lie, so I'll only say:
  [name: Celestine] She was very old, and she was very fond of you.
> I don't think so.
  [name: Celestine] That's the nicest thing about you. You'll find out anyway.

BASTIAN (asleep on a bench, or appearing to be):
[portrait: BASTIAN, happy] *(one eye open)* Hollis can't hear me if I can't hear him.
[name: Bastian] It's an old Cragholm law. I made it up.

MAGNUS (with the annex):
[portrait: MAGNUS, neutral] A null reading.
[name: Magnus] I've built machines that would give a great deal to be wrong in that particular way.
[name: Magnus] ...Good luck in the Open.

SIGRUN (at the rail, watching her father's envoy):
[portrait: SIGRUN, neutral] You again. Still small. Still standing in the middle of everything.
[name: Sigrun] Stop it. You'll get trampled.

ROOK (on the stair, hood up):
[portrait: ROOK, sad] I go down to the Lowlight every night.
[name: Rook] Then I came here and thought—it'll be different underground.
[name: Rook] It isn't. Everyone's still made of glass if you look long enough.

SAHAR (by the banners):
[if :ch6_drillsite == :sanctuary]
  [portrait: SAHAR, neutral] The child you made me shout for has started digging. Holes, mostly.
  [name: Sahar] He says he's looking for the red giant. I've told him to stop when it answers.
[else]
  [portrait: SAHAR, neutral] They'll vote the Mandate everywhere tonight. I'll vote no.
  [name: Sahar] The sand will vote with me. It always loses votes and always wins arguments.

ODESSA (on the table edge, swinging her boots):
[portrait: ODESSA, smug] I carry everybody's post, including the Directorate's, and I read none of it.
[name: Odessa] And I can tell you exactly what's in all of it. Ask me after the vote.

ILSA (far end of the table; if the PC approaches):
(She flinches, very slightly, before you're close enough to speak. Then she gets up and moves three seats further down. There aren't any further down. She stands at the end of the bench instead.)
[portrait: ILSA, deadpan] ...Not you. Them. All of them. Excuse me.

VOSS AND CALLA (the observers' gallery, the Zenith seats):
[portrait: VOSS, happy] Our ferry passenger.
[name: Voss] I keep finding you in the middle of history. Becoming a habit, for both of us.
[name: Voss] Zenith sits as an observer. Meridian, as a petitioner. I'm both.
[name: Voss] Means I don't get a vote, and I watch everyone's faces while they cast theirs.
[name: Voss] Best seat in the house.
[portrait: VOSS, neutral] Seven notes now, isn't it? In the case.
[name: Voss] It must be quite a chord.
[portrait: CALLA, neutral] *(not looking up from her ledger)* Sir, the Chancellor.
[name: Voss] Of course. Excuse me. Enjoy the Open.
```
*(09 #14: Voss knows how many notes the case plays. The PC has seven badges; nobody remarks on how he'd know.)*

### Map 263 — the Open's bracket board: comedy scene Ch9, **"The Bracket"** (sign-up; V130 == 3 → 4)
```
(A huge board of black slate at the Pit's floor, chalked in columns. A small girl with chalk to the elbows is standing on a crate writing names. Kaito sits at a table beside it with a form.)
[name: Nell] (the chalk-girl, to you) I'm Nell. I do the board. Done it since I was six.
[name: Nell] I've got the neatest S in Ironreach and I'll fight anyone who says I haven't.
[portrait: KAITO, neutral] Names for the bracket.
[portrait: JUNO, happy]\pfe[exclaim] *(arriving at a run, wreath askew)* Team Compost!
(At the far end of the bench, a boy in a black coat a size too big stands up very fast.)
[portrait: KESTREL, angry] We are NOT— it's a singles bracket!
[name: Kaito] Team Compost. Two entrants.
[portrait: KESTREL, panic] Don't write that down. Why are you writing that down?!
[portrait: KAITO, deadpan] A fist is a promise. So is a form.
(Nell chalks it on the board in her neatest hand: KESTREL VANE (TEAM COMPOST).)
[bubble: KESTREL, crying, sweat] My mother was a Warden.
[name: Nell] Is that with one L or two?
[name: Juno] *(to you)* I'm not entering. I'm the team.
[name: Juno] Every team needs someone who isn't in it to shout.
```
*(Running gag 3: the pit-fight bracket. Juno is happy here, on purpose: it is the last time in Act II.)*
```
EV "Kestrel" (after the bracket, by the Pit's wall):
[portrait: KESTREL, neutral] Don't. Whatever you're going to say about the board.
[name: Kestrel] I'm not here for a title.
[name: Kestrel] Word in every inn from Mirefen to here: the Mourner's going to hit the Conclave.
[name: Kestrel] Every Warden in one hole. He'd never get a better shot.
[name: Kestrel] So I'm here. Closest seat in the house.
[if :ch6_kestrel_rumor == :encourage]
  [portrait: KESTREL, happy] You said go. So I went. All the way down.
[if :ch6_kestrel_rumor == :warn]
  [portrait: KESTREL, angry] And before you say it might not be her: I know. I KNOW.
  [name: Kestrel] I'm still going to be standing there when the mask comes off.
[if :ch6_kestrel_rumor == :silent]
  [portrait: KESTREL, deadpan] You're doing the silence. Gran does the silence.
  [name: Kestrel] I can hear it from here.
(A Scizor unfolds itself from behind him, red and polished, one pincer chipped across the edge.)
[name: Kestrel] Won him off a pit-boss in the undercard on Tuesday.
[name: Kestrel] He was a Scyther with a cracked blade. Pit-boss said he was finished.
[name: Kestrel] He wasn't. See you in the final. Don't make me wait.
V130 = 4.
```
*(03_CAST: Scizor is "his duelist from K4 at Ironreach". It Megas only with Morwen's Ring, Ch18.)*

### Map 263 — the Ironreach Open (a gauntlet of three, then the final; V130 == 4 → 5)
*Each round is a single battle on `:COLOSSEUM` (the Pit's default; FIELD_DEFAULTS), with a heal between rounds at Nell's crate. The crowd's chant builds round by round.*
```
ROUND ONE — Pit Brawler Dunmore (a man with his shirt off, and his Machoke in matching shorts):
[name: Pit Brawler Dunmore] We're both wearing shorts. That's psychological.
(LOSE line, his:)
[name: Pit Brawler Dunmore] ...I'm going to need a shirt.
[name: Pit Announcer] AND THE NULL KID TAKES ROUND ONE, FOLKS!
[name: Pit Announcer] DUNMORE WILL BE LOOKING FOR A SHIRT!

ROUND TWO — Crush Kin Ysa (a girl of twelve with wrapped hands and her grandmother in the front row):
[name: Crush Kin Ysa] Gran's watching. If I lose, I've got to do the washing for a month.
(LOSE:)
[name: Crush Kin Ysa] GRAN. I did my BEST.
[name: Crush Kin Ysa] ...She's saying "the washing". I can't hear her, but I know.

SEMIFINAL — Old Gristle (a pensioner on a stick, who has fought in every Open since AF 262):
[name: Old Gristle] I fought Valen Corrigan in this Pit when he was nineteen.
[name: Old Gristle] He was a good boy. He cried when he won. Don't you cry.
(LOSE:)
[name: Old Gristle] You didn't cry. That's worse. Go on.
[name: Old Gristle] The boy in the coat's waiting, and he's been staring at you for three rounds.

(The crowd, all round the Pit, starting low:) NULL. KID. NULL. KID.

(In the undercard pens, between rounds: a gruff foreign trainer with a Lucario.)
[name: Garret?] You. Seen a girl, about this tall?
[name: Garret?] Eden. Brown hair. Never mind. Nobody has.
```
*(The undercard stranger is the Garret cameo's hook, CAMEOS #3; his quest NA_GARRET opens after S123. Plain name box "Stranger" until then.)*

### Map 263 — **K4: the Ironreach Open final** (V130 == 4 → 5)
```
(The floor cleared. Nell on her crate with the chalk ready. Every gallery full. In the Wardens' row, Juno on her feet. In the observers' gallery, Voss, applauding politely. High up, in the lowest gallery's shadow, the veiled woman with the lantern.)
[name: Pit Announcer] FOLKS. THE FINAL.
[name: Pit Announcer] ON THE LEFT: THE NULL KID!
[name: Pit Announcer] ON THE RIGHT: KESTREL VANE, OF TEAM COMPOST—
[portrait: KESTREL, angry] *(at the gantry)* I WILL COME UP THERE.
[name: Kestrel] *(to you)* Every one of those people is here to watch me lose to you.
[name: Kestrel] Let's disappoint them.
Script: Prismfall.rival_battle(:RIVAL_KESTREL, "Kestrel", 4)     # K4; version 40 + starter slot; field :COLOSSEUM (263)
(When Scizor enters:)
[name: Kestrel] Cracked blade. Still cuts.
(When his ace, Doublade, enters:)
[name: Kestrel] Both blades, Morwen.
[name: Kestrel] She's watching. I don't know who. Somebody.
(LOSE: whiteout to the Ironreach Pokémon Center. Kestrel on retry: "Again. The crowd's had its warm-up.")
(WIN:)
[name: Pit Announcer] THE NULL KID! THE NULL KID TAKES THE IRONREACH OPEN!
(The crowd comes down the galleries. Nell chalks your name at the top of the board, big, with a crown on it.)
[name: Kestrel] Keep the title. I told you I'm not here for a title.
(He looks up at the lowest gallery. The veiled woman with the lantern is gone. There's only a lantern-hook, swinging.)
[portrait: KESTREL, shocked]\pfe[question] ...Who was that?
[name: Kestrel] Never mind. Doesn't matter. Nothing matters till the vote.
Switch S122 CH9_K4_DONE = ON. V130 = 5.
(Received: OPEN CHAMPION'S CHALK. ITEM DESCRIPTION: "A stub of Nell's chalk, wrapped in a strip of red cloth. Ironreach's trophy. It's worth nothing, and nobody in Nadir would sell you one.")
```
*(The LoseText of `RIVAL_KESTREL` 40–42 and their Hard/Casual copies was "It wasn't her. It was never her. ...Don't. Just don't.", which gives the unmasking away an hour early. It's now "Keep the title. I'm not here for a title." This file's change list has it.)*
*(09 #2a: Ysolde watches Kestrel and leaves before he sees her.)*

## Maps 270–275 — Kaito's gym, "the Pit under the Pit" (Gym 8; GYM_PUZZLES Gym 8)
```
KAITO'S SIGN (270): "Don't fight the one in front of you. Move it."
[name: Gym Guide] Kaito's gym! Fighting-types on the Colosseum.
[name: Gym Guide] Every knockout gets the crowd going, and a roused crowd hits harder.
[name: Gym Guide] Psychic and Flying go over their heads. Fairies don't care how loud it gets.
[name: Gym Guide] The sparring partners chase you. Every step you take, they take one.
[name: Gym Guide] They can't cross a rope. You can.
[name: Gym Guide] That's the whole lesson, apparently. Kaito says it took him nine years.

[name: Apprentice Hiro] (273; hints) Discipline over rage. That's on the wall in his office.
[name: Apprentice Hiro] It's the only thing on the wall.
[name: Apprentice Hiro] Push the low boulder first. The partners are greedy.
[name: Apprentice Hiro] Let them be greedy at a rope. / (the solution)
```

### 274 — the Pit: Kaito
```
(A small square floor of red earth, roped, under one lamp. No galleries. No crowd. Just a man in training wraps with a burn scar along his jaw, and a Lucario sitting cross-legged against the far rope with its eyes shut.)
[portrait: KAITO, neutral] You won the Open.
[name: Kaito] That was for them. This isn't.
[name: Kaito] There's nobody watching this one.
[name: Kaito] Ironreach's Warden is whoever wins the Iron Trial.
[name: Kaito] I won it nine years ago. Every year somebody tries to take it off me.
[name: Kaito] Every year I'm still here.
[name: Kaito] Stand up. Again. That's all I teach. Ready?
Script: Prismfall.gym_battle(pfm_gym(:LEADER_KAITO), double: false)     # LEADER_KAITO, :COLOSSEUM, cap 43, single
(When his ace, Lucario "Memory", enters:)
[name: Kaito] Memory. It remembers for me.
(LOSE: whiteout. Kaito on retry: "Stand up. Again.")
(WIN:)
[name: Kaito] ...Good. Your Pokémon fight like they remember why.
(Received: the PROMISE BADGE.)
(SE: eight notes. The badge case's light runs along its seams and pools in the corners, like water finding the low places.)
[name: Kaito] It sings.
[name: Kaito] Memory heard it too. Look.
(The Lucario's eyes have opened. It's looking at you. Not at the case. At your chest.)
[name: Kaito] Lucario feel what's alive in a room.
[name: Kaito] Sometimes what's alive in a room is more than the people in it.
(Received: TM31 BRICK BREAK.)
[name: Kaito] Brick Break. It goes through walls.
[name: Kaito] And that badge says Pokémon up to level forty-seven will heed you.
[portrait: KAITO, sad] *(quietly, as you turn to go)* A fist is a promise.
[name: Kaito] Don't make one you won't keep.
V130 = 6.
```
*(09 #27: Kaito's promise line; the Mastery door is Marrowgate. Lucario looking at the PC's chest is 09 #1, with nobody saying why.)*

**After the badge: Fly** (the gym door, 270)
```
(Odessa is sitting on the gym's doorstep with a parcel on her knee and her goggles up.)
[portrait: ODESSA, happy] There you are. Eight badges, says the board.
[name: Odessa] Fly's allowed at eight, and I don't trust the post to deliver it.
(Received: HM02 FLY.)
[portrait: ODESSA, smug] Courier's privilege. I deliver. In person, when I like the address.
[name: Odessa] Come to Skyreach sometime.
[name: Odessa] We've got a gym, a storm, and the best dead-letter office in the realm.
[name: Odessa] Don't tell anyone I said "best". It's a sad sort of best.
```
*(Fly per WORLD.md §4, `BADGE_FOR_FLY = 8`, from the Skyreach courier at the Conclave. The dead-letter office is Ch12's K5.)*

**275 Marrowgate Door — Mastery (optional; side door in 273)**
```
PLAQUE: "MARROWGATE — SEALED AF 285 — BY ORDER."
(Behind the gate, faintly, knocking. Three knocks. A pause. Three knocks. On the wall, Lucario's blue aura flickers like a candle in a draught.)
(After the PC clears it:)
[portrait: KAITO, sad] You opened it. It was empty, wasn't it.
[name: Kaito] ...I always hoped it would be.
```
*(GYM_PUZZLES Gym 8, 275. Marrowgate is the Quiet Town he sealed (09 #27); the testimony is Ch13. Players who skip the Mastery still get the promise line.)*

## Map 265 — the Old Aurel Shafts [NEW]: **"Somewhere Useful"** (the way back up from the gym to the Conclave galleries; touch, V130 == 6)
```
(The old mine shafts under the Pit: timber props, abandoned ore carts, the Conclave's noise coming down through the rock like weather.)
(A young man in a Choir porter's grey coat comes round a prop the other way, a bucket in his hand with a Carvanha in it. His face is a face you know.)
[portrait: TEO, shocked] ...Oh, tides.
[if :ch4_teo == :report]
  [portrait: TEO, angry] You. You told them my name once, with Mari standing right there.
  [name: Teo] Don't do it twice. Not today.
[else]
  [name: Teo] You didn't see me. Mari can't see me. Not today.
[name: Teo] The Hammer's here. Sable's people.
[name: Teo] Came down with the Fist Plate's escort, in porters' coats, like me.
[name: Teo] Somebody I trust says they're going to do the reliquary during the vote.
[name: Teo] So somebody I trust is going to stop them. And I'm going to help.
[name: Teo] That's all. That's useful, isn't it?
[portrait: TEO, smug] Don't tell my sister I was useful. She'll never forgive me.
MOVE: Teo goes up the shaft stair two at a time, the Carvanha sloshing.
```
*(The build-up for `:ch9_teo_sable`. "Somebody I trust" is Rowan; the PC doesn't know that yet.)*

**[if `pf_cond("standing(:HOLLOW) >= 4")`] EV "Sable" (the next gallery up; GO_PULL_THE_NAIL)**
```
Script: Prismfall.checkpoint     # NARRATIVE_KEYS §10: GO_PULL_THE_NAIL's checkpoint, the Ironreach shafts
(A woman leans on an ore cart in the lamplight, eating an apple. Hollow grey. The top half of her face behind a half-mask, the bottom half smiling.)
[portrait: SABLE, happy] There you are. The one who walks in.
[name: Sable] I've been dying to meet you properly. Last time you were busy standing in my glass.
[name: Sable] You're a friend of ours. Word gets about.
[name: Sable] Wick likes you. The Ebbmouth boy owes you.
[name: Sable] I don't owe anybody anything, so I can be honest.
[name: Sable] In ten minutes, sixteen Wardens at that table are going to vote a leash on Nadir.
[name: Sable] Unless somebody gives them a reason to look somewhere else.
[name: Sable] The reliquary's warded. Nobody can get near it but a Warden.
[name: Sable] And you.
[name: Sable] You could walk right up to it. Put something on it where nobody else can reach.
(She holds out a small brass thing with a sunburst scratched off it, warm in her hand.)
[name: Sable] One little nail. Pull it. Let them listen.
> Take it.
  > ...It's a Splitter. It'll Shatter the Plate. Take it?
    > Take it.
      (You go up the stair with it in your pocket. It's warm the whole way. Nobody stops you. Nobody can.)
      (At the reliquary you lay it on the Fist Plate's case, and the light goes out of everything.)
      (Afterward, in the glass, at the edge of the gallery, there's a girl in a wreath of blossoms with her arms round a child. Neither of them moves. Neither of them will.)
      Script: Prismfall.game_over(:GO_PULL_THE_NAIL)
    > No.
  > No.
(If refused:)
[portrait: SABLE, deadpan] Shame. You'd have been so good at it.
[name: Sable] Then don't be standing under the gallery, sweetling.
MOVE: Sable walks into the dark between two props and isn't there any more.
```
*(GO_PULL_THE_NAIL: offered only if `standing(:HOLLOW) >= 4`. Foreshadowing: Wick's Ch7 line and Sable's broadcast. Epitaph in NARRATIVE_KEYS §9. On refusal the PC runs up the stair and arrives as the lights go out: the vote scene below, with no time to warn anyone.)*

## Map 263 — **"The Vote"** (autorun on returning to the galleries, V130 == 6 → 7) — **key event 1, build-up**
```
(The Conclave is in session. On the Pit's upper ring, high above the floor, the Fist Plate stands in its reliquary: a case of iron and glass on a stone plinth, lit from inside, warm red, like a coal held in a fist. Kaito stands below it with his hand on his chest.)
(The Wardens are seated. The galleries are full. Juno is in the Wardens' row beside Corvin, and in her lap, asleep, Nell the chalk-girl, worn out from the Open.)
[portrait: HOLLIS, neutral] The question before the Conclave.
[name: Hollis] That the Mandate granted at Lumen be extended to every land where a Lattice stands—
[name: Hollis] —and held by the Meridian Security Directorate until the Sovereign revokes it.
[portrait: MARCHETTI, neutral] *(standing in the petitioners' box)* The Directorate asks for the leash
[name: Marchetti] —so it can keep the dog off the children, Chancellor.
[name: Marchetti] That's all a leash is.
[portrait: CORVIN, deadpan] *(not standing)* I've treated a great many people who were kept off things with leashes.
[name: Hollis] The Warden of Mirefen is out of order and correct.
[name: Hollis] The Conclave will vote. Wardens, by hand.
[name: Hollis] For the Mandate—
(Hands start to go up. Magnus's, first and steady. Anja's, slowly. Not Marisol's. Not Sahar's. Not Kaito's. Rook's goes halfway and stops.)
[if :ch8_caldera == :shutdown]
  (Brann keeps both fists on the table. He looks at Valen, then at you, and doesn't raise either of them.)
[else]
  (Brann's goes up last, after a long look at Valen, like a man lifting something heavy he doesn't want.)
(And the lights go out.)
```
*(From here to Valen's exit: no jokes.)*
```
(Every lamp in the Iron Pit at once. Black. The crowd's noise drops to nothing, then comes back as a single sound, the sound of a thousand people breathing in.)
(Then the Pit's speakers crackle. A voice, cheerful, very close, in every gallery.)
[portrait: SABLE, happy] *(on the speakers)* Vote yes on the Mandate. Go on. Give them the leash.
[name: Sable] We'll give you a reason.
SE: something heavy hits the rock high up. The whole Pit shudders. Dust falls in sheets.
(Emergency lamps flicker on, red. On the upper ring, grey cowls are swarming the reliquary. On the Pit floor, a squad in porters' coats has thrown them off: Hammer badges on their chests. Two of them come straight for the challengers' bench.)
[portrait: KESTREL, angry] *(already moving, coat flying)* That's not him. That's NOT the Mourner.
[name: Kestrel] That's the Hammer.
[name: Kestrel] With me. Now. Don't argue.
```

**Partner battle: PC + Kestrel vs Sable + Captain Brisk**
```
(The Pit floor. A woman in a half-mask, and beside her a huge bald man with a hammer tattooed down his forearm.)
[portrait: SABLE, happy] Oh, it's the walking one, and the Vane boy.
[name: Sable] This is going to be a lovely story afterward.
[name: Sable] I'll tell it on every screen in Velmora.
[name: Captain Brisk] Until they listen.
BATTLE: tag battle — PC + Kestrel (RIVAL_KESTREL as partner, version 40 + slot's team) vs [HOLLOW_SABLE "Sable", version 0] + [HOLLOW_ADMIN "Brisk", version 0]. Field: Colosseum; the Hammer's quakes drop it into a Cave on the third (TRAINER_FIELD_PLAYBOOK, Ch9).
(At the field's change to Cave:)
[portrait: KESTREL, shocked] The roof's coming DOWN—
(LOSE: whiteout; the sequence restarts at "The Vote".)
(WIN:)
[name: Captain Brisk] Until they listen! ...They're not listening.
SE: a long, grinding roar. Half the gallery stair comes down between the floor and the upper ring in a slide of rock and timber.
(When the dust clears, Sable is gone. Kestrel is on the far side of the fall, on his knees, coughing.)
[portrait: KESTREL, angry] *(through the dust)* Go UP. Go, I'll find a way round. GO!
(Corvin climbs over the rubble with his bag open.)
[name: Corvin] Hold still. I'm not asking.
*(He sprays every Pokémon you have and slaps a field dressing on your arm.)*
[name: Corvin] There. Now go and get hurt somewhere else.
Script: $player.heal_party
Script: Prismfall.checkpoint     # losing upstairs restarts at the top of the stair, not at "The Vote" (Gemini review 2026-11-21)
V130 = 7.
```

## Map 264 — the Reliquary [NEW] (the Pit's upper ring): **"Get Back"** → the Mourner → the Shatter — **key event 1**
```
(The upper ring. The red emergency lamps. The reliquary on its plinth, the Fist Plate inside it glowing too bright, the glass case clamped round with brass: three Splitters, wired together, ticking.)
(Standing over the reliquary is a figure in a grey cowl and an ash-bark mask with one white lily. Its gloved hands are inside the clamp-wires. It isn't planting them. It's pulling them out, one at a time, very carefully.)
(Two Hammer grunts lie unconscious at its feet, wrapped in roots.)
[portrait: MOURNER, shocked] *(the doubled voice)* No. No — not you. Not now.
[name: The Mourner] Get back.
> Step away from the Plate.
  [portrait: MOURNER, angry] I'm trying to SAVE the— you don't understand.
  [name: The Mourner] Get BACK.
> What are you doing?
  [portrait: MOURNER, sad] Taking out what she put in. One wire at a time.
  [name: The Mourner] If you'd stand still, I'd have one fewer to take out.
> ...
  [name: The Mourner] Yes. Stay quiet. Stay there. Don't come closer.
(Behind him, a Trevenant uncurls out of the rock like a tree standing up.)
[name: The Mourner] I said get BACK!
Script: Prismfall::Bosses.trainer_battle(:HOLLOW_MOURNER, "Mourner", 0, boss: :MOURNER_TREVENANT, species: :TREVENANT)     # Shiftry, Cacturne, Gourgeist, Trevenant (multi-bar); field :COLOSSEUM; he fights defensively (Protect, Spiky Shield)
(Turn 2, or the first time the PC's Pokémon hits his:)
[name: The Mourner] Not now — you don't understand —
(At Trevenant's first bar break:)
[portrait: MOURNER, sad] Please. There isn't time. There isn't TIME!
(LOSE: whiteout; restart at the top of the stair into 264, from the checkpoint above.)
(WIN:)
[name: The Mourner] Not now. You don't understand.
[name: The Mourner] Get back. Get—
```
```
SE: a click. Very small.
(The last Splitter, the one he hadn't reached, lights up white.)
CUTSCENE IR-1 "The Partial Shatter" (Prismfall Cutscenes; ~8 s; storyboard below).
(The Fist Plate cracks. Not all the way. A sound like a bell struck once and held. Half of its light goes out through the case in a wave, red going to grey, and where it passes the stone turns to glass. The field in the reliquary chamber goes Bleed.)
(The glass runs. Down the stair, across the ring, toward the lowest gallery, toward the Wardens' row, fast as frost on a window. In its path, at the gallery's edge, a girl in a wreath of blossoms is on her knees with her arms round a child. Juno. And Nell.)
[portrait: JUNO, shocked]\pfe[exclaim] NELL. Get DOWN—
(The figure in the cowl moves before you can.)
(He throws himself down the stair between the glass and the gallery. The Trevenant goes with him, and its roots tear up through the stone floor in front of Juno, a wall of roots, bark, leaf, and the glass hits the roots and climbs them and stops.)
(The burst catches him full in the face.)
SE: a crack like a branch breaking.
(The mask splits down the middle. Two halves of ash-bark, one with the lily, fall onto the glass floor and slide.)
WAIT 40.
```
```
(The Bleed light is grey and comes from every direction. The man on his knees behind the root-wall has soil under his nails, and a soft, bleeding face, and the right side of his neck and shoulder are glass, clear as water, spreading. His right hand has lost its bandage. The palm is scarred in a pattern like lightning.)
(Juno is three metres away, behind the roots, with Nell in her arms.)
[portrait: JUNO, shocked]\pfe[dots] ...
[name: Juno] ...Uncle Rowan?
[portrait: ROWAN, sad] Juno.
[name: Rowan] Juno. Don't look at me like that.
[name: Rowan] Look at the flowers.
[name: Rowan] Look at what they're standing on.
(He looks down. The glass under his knees. Then he folds forward onto it, very slowly, like a tree going over.)
Switch S124 CH9_MOURNER_UNMASKED = ON. V130 = 8.
```
*(The Mourner's PBS LoseText was "Not now - you don't understand - ...Juno. Don't look at me like that.", which says Rowan's unmasked line while he's still masked; it is now "Not now - you don't understand - get BACK!" This file's change list has it.)*
```
(Nobody moves. All round the ring, people: Wardens, Directorate, Choir porters, the Sovereign. Not one of them can come in. The glass is still creeping, very slowly, up Rowan's shoulder.)
[portrait: CORVIN, angry] *(at the Bleed's edge, his hand out, snatched back burned)* Someone— someone get him OUT—
(You walk in.)
(The chime is everywhere. Your skin doesn't burn. Under your ribs, something is very still. You get your arms under Rowan's and pull. He's heavy the way a sleeping man is heavy, and the glass on his shoulder rings against the floor all the way to the edge.)
(At the edge, hands take him. Corvin's. Kaito's.)
(When you look up, everyone is looking at you. The Wardens. The envoys. Marchetti. Voss, very still, at the observers' rail. And the man in white, with one grey glove, who hasn't taken his eyes off you since you stepped in.)
```
*(The joke-free rule holds from "The Vote" to Valen's exit. The partial Shatter is smaller than the Lowlight: a ring of glass on the upper ring, no Fixed bystanders unless the choice below makes one.)*

**Cutscene IR-1 storyboard** (for the cutscenes owner; on map 264, `on_map: true`)
| # | Camera | Action | FX | Text |
|---|---|---|---|---|
| 1 | Close on the reliquary (1 s) | The last Splitter lights white | white flare, a click | — |
| 2 | Hold (2 s) | The Plate cracks half across; a red-to-grey wave leaves the case | ring wave; the stone turns glassy behind it | SE: one bell note, held |
| 3 | Pan down the stair (2 s) | The glass runs toward the gallery edge, Juno and Nell in its path | frost-spread sheet effect | — |
| 4 | Wide (2 s) | The Mourner and the Trevenant drop in front of them; roots burst up into a wall; the glass climbs the roots and stops | root particles; screen shake | — |
| 5 | Close (1 s) | The mask splits; two halves fall | crack SE; shards | — |

## Map 264 — **CHOICE `:ch9_teo_sable`** (MAJOR) — **key event 2**
*(Straight on from the rescue; the PC is still at the Bleed's edge.)*
```
(Through the dust and the grey light you see two things at once.)
(To the left, inside the glass, where the scaffolding on the ring has come down: a young man in a porter's grey coat, pinned under a timber at the waist, one arm out. The glass has his legs. It's at his hip. It's climbing. A Carvanha flops on the glass beside him, gasping.)
[portrait: TEO, crying] Help— somebody— MARI—
(To the right, across the ring: a woman in a half-mask, running for a Meridian service lift in the rock wall, a brass box clipped to her belt with a short aerial. She's laughing.)
[portrait: SABLE, happy] *(over her shoulder)* Lovely work, everyone!
(The glass on Teo is at his ribs. The service lift's grille is opening for Sable.)
(There's time for one.)
> Go to Teo. (save_teo)
  Script: pf_choose(:ch9_teo_sable, :save_teo)
  (You turn your back on the lift and walk into the glass.)
  (The timber is too heavy. Then it isn't: your Pokémon are at the other end of it, all of them, and it lifts, and you pull, and Teo comes out from under it with the glass ringing off his legs like ice off a rope.)
  (At the edge Marisol is there before anyone. She takes him out of your arms and goes down onto the floor with him.)
  [portrait: MARISOL, crying] Teo. Teo, you idiot. You IDIOT.
  [name: Marisol] Look at me.
  [portrait: TEO, sad] Hi, Mari. ...I was useful.
  (His left hand is glass from the knuckles to the fingertips. All four fingers. Clear as water. He looks at it like it belongs to someone else.)
  [name: Marisol] I don't care. I don't care, I don't CARE.
  (Across the ring, the service lift's grille clangs shut. The lift goes up into the rock. Sable is gone.)
> Go after Sable. (chase_sable)
  Script: pf_choose(:ch9_teo_sable, :chase_sable)
  (You run.)
  (Across the ring, through the dust, over the fallen stair. The lift grille is closing. You get your arm through it.)
  [portrait: SABLE, angry] Oh, for— LET GO, you little—
  BATTLE: HOLLOW_SABLE "Sable", version 1 [NEW] (a rearguard of one: her Drapion, fresh; field :CAVE after the roof-fall). Can't be fled.
  (LOSE: whiteout to the Ironreach Pokémon Center; the choice holds; the chase restarts at the lift.)
  (WIN:)
  (The Drapion goes down in the lift's doorway. Sable kicks the grille, drops the cage, and the lift lurches up. You have the brass box. It came off her belt in your hand.)
  [portrait: SABLE, deadpan] *(rising out of sight)* Keep it, then. It only plays one song.
  (The box crackles. Encryption bars scroll on its little screen: a sunburst, and under it, MERIDIAN SPECIAL ACCOUNTS. Then a voice, a man's, calm, very clear.)
  [name: Voice on the device] Kroll, report.
  (Received: COMM-DEVICE.) ITEM DESCRIPTION: "A brass radio-box with a sunburst on its screen and MERIDIAN SPECIAL ACCOUNTS under it. A man's voice asked for Kroll. Nobody has answered him."
  (You turn back.)
  (Behind you, at the glass's edge, Marisol is kneeling where the scaffolding fell. Inside, under the timber, the young man in the porter's coat is glass to the throat. One arm is still out. His hand is open, reaching toward his sister, and the glass has it too.)
  [portrait: MARISOL, crying] Teo. Teo. TEO.
  (She puts her hand on the Veil, and it burns her, and she keeps it there.)
  WAIT 60.
  [name: Marisol] *(without turning round)* He was nineteen.
V130 = 9.
```
*(NARRATIVE_KEYS §4.2: `:save_teo` MARISOL+4 HOLLOW+1 RES+1; `:chase_sable` MARISOL−4 ACCORD+1 RES−1. TEO_SAVED / IRONREACH_EVIDENCE are derived; Core mirrors S221. Marisol's full "He was nineteen. Nineteen. Tell me again how the Hollow are the monsters." is held for Ch11/13, where she says it to someone; here she can only say the first three words. The COMM-DEVICE is the only proof that exposes Kroll publicly at the Ch13 tribunal.)*

## Map 263 — **"Mandate Jurisdiction"** — the aftermath (autorun on returning to the Pit floor, V130 == 9 → 10)
```
(The emergency lamps. Dust. The Wardens' row is wrecked. On the Pit floor, Rowan lies on a stretcher with the glass on his shoulder wrapped in Corvin's coat, awake, looking at the roof.)
(A squad in white-and-gold has formed round the stretcher. Director Marchetti steps out of them.)
[portrait: HOLLIS, neutral] *(on the table, shouting over the noise)* In the matter before the Conclave, under the emergency articles:
[name: Hollis] The Mandate is carried by acclamation—
[portrait: SAHAR, angry] By WHOSE acclamation?! We were under the—
[name: Hollis] —by acclamation, and in force from this hour. Director.
[portrait: MARCHETTI, neutral] Rowan Ashby.
[name: Marchetti] You're detained under the Mandate for the Lumen Shatter—
[name: Marchetti] —and the attack on this Conclave.
[portrait: KAITO, angry] He was pulling the wires out. I saw him.
[name: Marchetti] Then he'll say so, Warden. In custody.
(She turns to the man in white.)
[name: Marchetti] Mandate jurisdiction, Sovereign.
(Valen looks at the stretcher a long time. At the bandage on the floor. At Juno, on the far side of the Pit.)
[portrait: VALEN, sad] ...Take him.
(The squad lifts the stretcher.)
V113 ROWAN_STATUS = 1. V111 NADIR_STATE = 1.
```

**Kestrel** (he comes in over the fallen stair, filthy, and pushes through to the stretcher)
```
(He stares down at Rowan's face for a long time. Rowan looks back at him and doesn't say anything.)
[portrait: KESTREL, shocked] ...
[portrait: KESTREL, sad] ...It's not her.
(He doesn't know what his face is doing. Neither do you.)
[if :ch6_kestrel_rumor == :encourage]
  Script: pf_bond_add(:KESTREL, -3)
  [portrait: KESTREL, angry] *(to you)* You said go. You said "go".
  [name: Kestrel] I went all the way down a hole for this.
  [name: Kestrel] It's a GARDENER.
[if :ch6_kestrel_rumor == :warn]
  Script: pf_bond_add(:KESTREL, 2)
  [name: Kestrel] You said it might not be.
  [name: Kestrel] I hate that you were right.
[if :ch6_kestrel_rumor == :silent]
  [name: Kestrel] Don't. Don't say anything now either.
MOVE: Kestrel walks away across the Pit, into the shafts, and the dark takes him.
```
*(NARRATIVE_KEYS §4.2, the deferred deltas of `:ch6_kestrel_rumor`.)*

**Juno** (on the Pit floor in the glass dust, where the roots came up; Nell has been taken by her mother)
```
[if :ch7_ledger == :name_him] Script: pf_bond_add(:JUNO, 2)
[if :ch7_ledger == :reassure] Script: pf_bond_add(:JUNO, -2)
(Juno is sitting in the glass dust with her knees up and her veil spread round her. The blossoms of the wreath have glass dust on them, and they're still perfect, and she's looking at them.)
[if :ch3_juno_talk == :told]
  [portrait: JUNO, sad] *(not looking up)* You told me a secret once. On the breakwater. About the scanner.
  [name: Juno] I kept it. I'm good at secrets. I just don't look it.
  [name: Juno] I didn't know he was keeping one too.
  [name: Juno] I didn't know everybody was.
[else]
  (For a long while she doesn't look up. Corvin sits down a little way off, with his mask in his hands, and doesn't try to make her talk.)
(Every player gets Juno's answer to Chapter 7, whether or not she was trusted on the breakwater.)
[if :ch7_ledger == :name_him]
  [portrait: JUNO, sad] You said his name in Mirefen and I ran away from you.
  [name: Juno] I knew then. I knew in the dispensary.
  [name: Juno] I just wanted one more week of not knowing.
[if :ch7_ledger == :reassure]
  [portrait: JUNO, sad] You said there were loads of R.A.s. You were being kind.
  [name: Juno] I know you were. I wish you hadn't been.
[if :ch7_ledger == :ask_corvin]
  [portrait: JUNO, sad] Dr Mott knew. Didn't he.
  [name: Juno] He treats hands. He doesn't ask whose.
[portrait: JUNO, crying] Don't go. Don't say anything. Just don't go.
(You sit down in the glass dust beside her. It doesn't cut you.)
```

**CHOICE `:ch9_rowan_words`** (the stretcher passes the PC on its way to the cage-lift; Rowan turns his head)
```
(The squad stops for him, which surprises everyone, including the squad.)
> "Why?" (why)
  Script: pf_choose(:ch9_rowan_words, :why)
  [portrait: ROWAN, neutral] Ask the Drowned Crown.
> "I'll look after her." (look_after)
  Script: pf_choose(:ch9_rowan_words, :look_after)
  [portrait: ROWAN, sad] I know.
  [name: Rowan] That's why I'm not afraid.
> ... (silent)
  Script: pf_choose(:ch9_rowan_words, :silent)
  [portrait: ROWAN, neutral] You saw what I saw. In the Lowlight. Didn't you?
MOVE: the squad carries him to the cage. The gate shuts. The cage goes up into the rock.
Switch S123 CH9_CONCLAVE_DONE = ON. V130 = 10.
```
*(NARRATIVE_KEYS: `:look_after` ROWAN+2 JUNO+1; `:silent` ROWAN+1. Each colours his tribunal, Ch13.)*

## Map 263 — **"A Seat to Fill"** (on the Pit floor after the cage goes up; V130 == 10 → 11)
```
(Valen crosses the ruined Pit to you. He walks slowly, and people get out of his way without being asked.)
(There is glass dust on your shoulder, from carrying Rowan. It glitters. It isn't hurting you. He looks at it. Then at you.)
[portrait: VALEN, neutral] ...
[portrait: VALEN, sad] Come to Verdance.
[name: Valen] There's a seat to fill.
[name: Valen] And I think you should see what it costs.
MOVE: Valen walks to the cage-lift. Brann goes after him, then stops at the Pit's edge and looks back.
(Brann looks at you with an expression you've never seen on him. Not anger. Not fear. Grief, as plain as if someone had died, and it was you.)
MOVE: Brann follows the Sovereign into the cage.
(In the observers' gallery Voss has already gone. Calla is the last of his party, gathering papers. She looks down at you once, and then away, fast.)
[portrait: NYX, neutral] *(from the gallery rail above you, to nobody, or to you)* Everything has a price, sweetheart.
[name: Nyx] Yours just went up.
V130 = 11.
QUEST LOG: "Eighteen Roads" — Go to Verdance, as the Sovereign asked. Up the Root Road.
```
*(09 #16: "There's a seat to fill." Brann is the Sovereign's Hand (03_CAST): he knows what Valen means to do with a child who walks in the Bleed. Nyx's line is her 03_CAST voice line, kept for the moment the whole realm watched the PC walk in.)*

## Map 261 — the Ironreach Pokémon Center that night (autorun on the first heal after V130 == 11)
```
(Every screen in the Center. The Velmora Gazette's night bulletin, read by a woman with a very steady voice.)
[name: Gazette Reader] ...unmasked as the Grass Warden, Rowan Ashby of Verdance.
[name: Gazette Reader] He is currently in Directorate custody.
[name: Gazette Reader] The Conclave has extended the Mandate to every Lattice in the realm.
[name: Gazette Reader] In Lumen, Chairman Voss said Meridian "will carry this responsibility—
[name: Gazette Reader] —with the seriousness it deserves".
[name: Gazette Reader] One unidentified member of the public was seen to enter the Bleed.
[name: Gazette Reader] Witnesses report they were unharmed.
GAZETTE HEADLINES (the board by the door): "MOURNER IS GRASS WARDEN" · and by `:ch9_teo_sable`: "EBBMOUTH BOY PULLED FROM GLASS" (`:save_teo`) or "WARDEN'S BROTHER LOST IN IRONREACH GLASS" (`:chase_sable`); both add "HAMMER BOMBER STILL AT LARGE" underneath
[name: Nurse] (at the counter, quietly) The one who walked in. That was you.
[name: Nurse] ...Here. Your Pokémon are fine.
[name: Nurse] I checked them twice. I don't know why I checked them twice.
```
*(10_CHOICES_ENDINGS §1.4: the Gazette, two headlines per chapter.)*

---

## Map 294 — the Heartgarden, Verdance, at dawn: **INTERLUDE II — "The Bride Tree"** (playable as Rowan; autorun on sleeping at 261 with V130 == 11)
```
V119 INTERLUDE_ACTIVE = 2. (The party is swapped for Rowan's Warden team: Trevenant "Glasswood", Leavanny, Roserade, Sunflora, at K4's levels. No battles are scripted; wild encounters are off.)
TEXT (white on black): Five days earlier. Verdance.
(Dawn in the Heartgarden. Verdance's walled garden on its terraces, ordinary-beautiful, not drowning in anything yet. Bees. A watering can on the path. In the centre, at the head of a stone stair that goes down into a sunken grove, a tree in the shape of a woman: arms raised, head back, in blossom from root to crown. White and pink. The same blossoms as Juno's wreath.)
(The player is Rowan. His right hand is bandaged. He picks up the watering can with his left.)
```
```
THE BRIDE TREE (action):
(He waters the roots, the way he has every dawn for twelve years. He talks while he does it, the way you talk to somebody making breakfast in the next room.)
[portrait: ROWAN, neutral] Morning, love.
[name: Rowan] The roses are coming in again. By the east wall.
[name: Rowan] They don't stop, love. They never stop.
[name: Rowan] Neither do you.
(A blossom comes down onto the back of his hand, and stays there. They don't fall, Elin's blossoms. They never fall. This one did.)
[portrait: ROWAN, shocked]\pfe[dots] ...
[name: Rowan] You've never done that before.
(He looks at it for a long time. He doesn't brush it off.)
```
```
TREVENANT (following him; action):
(The Trevenant leans down over him, bark and leaf, one red eye. It used to be a Phantump crying in a glass tree.)
[portrait: ROWAN, happy] Look at you.
[name: Rowan] In the spring you couldn't die and you couldn't grow. Now look.
[name: Rowan] You know what I'm going to do today. You've always known.
[name: Rowan] You never once said I shouldn't. Is that loyalty, or are you just a tree?
(The Trevenant reaches up into the Bride Tree's branches, very carefully, and picks one white lily from among the blossoms. It holds it out to him.)
[portrait: ROWAN, sad] ...Thank you.
(He tucks the lily into the band of his hat. Then, thinking better of it, into his coat.)
```
```
THE POTTING SHED (action):
(A bench. A seed-tin labelled NOT SEEDS. An envelope, already addressed in a careful hand: "To the Sovereign of the Accord. From the Warden of Verdance. To be opened if.")
[portrait: ROWAN, neutral] If.
(He pulls the ring off his finger. A plain band with a chip of stone in it, no colour at all. It comes off hard, over a knuckle that hasn't been without it for twenty-four years.)
[name: Rowan] A mask can't hide a Warden's ring.
[name: Rowan] Everybody in Velmora knows what one looks like.
[portrait: ROWAN, sad] And if I don't come back, it oughtn't to be on me.
[name: Rowan] It ought to be on somebody who'll stay.
(He drops the ring into the envelope with the folded testament. Seals it. Writes, under the address: "She's ready. She doesn't know it.")
SE: a Pidgey on the shed roof. The Gale Post's morning collection bell, down in the town.
(He takes the envelope out to the post-box by the Heartgarden gate and holds it over the slot a long time.)
(He posts it.)
```
```
THE STAIR (action, last):
(At the head of the stone stair, the sunken grove below: green, ordinary, the Meadow Plate lying in the Bride Tree's roots at the bottom, warm, humming. Anyone could see it from here. Anyone could walk down.)
(Rowan takes the mask out of his satchel. Ash-bark. One white lily, a carved one. He doesn't put it on. He looks at it. Then he folds it into his coat, lily-side in, next to the real one.)
[portrait: ROWAN, sad] One more.
[name: Rowan] Then I'll find the other way. I promise.
[name: Rowan] *(to the tree)* I promise, love.
(He goes down the terraces toward the gate, and the road, and the Long Drop, and Ironreach.)
(Behind him, in the Bride Tree's branches, where the blossom came off, a new bud is already opening.)
V119 = 0. V130 = 12. V101 STORY_ACT = 3. V102 STORY_CHAPTER = 10.
TITLE CARD: END OF ACT II.
TITLE CARD: III — FAULT LINES
```
*(05_ACT_II Interlude II. Changed from the outline: Rowan **packs** the mask instead of putting it on, because he walks into the Conclave unmasked as the Grass Warden. "Five days earlier" fits the Root Road to Ironreach. The ring in the testament is how the seat and the ring reach Juno in Ch10, and why the Mourner never Mega Evolves. The falling blossom is a Homecoming seed (09 #21), and nobody comments on it.)*

---

## Map events needed (Chapter 9)

None of these maps is built. **[NEW]** = a map or event not in maps.json. V130 = **CH9_STEP** (design/FLAGS.md).

**660 The Ashmarch** — road sign; the recruiting table at the first mile-fort (recruiter, apprentice, brazier, banner); **"Eight Years Late"** autorun (Larch on the mounting-block; KELP TEA BAG; V130 0 → 1); the sweeper and the veteran (second mile-fort). Trainers (designer).
**661 The Ironway** — road sign; the Truce Post (inspect, chalk hammer); the ore-carter and his Rhyhorn; the Elowen forester at the ford. Trainers.
**602 Candle Down** — a V130 >= 1 page on every cairn (the thirteenth candle); the pilgrim; the coaching-inn keeper's new line (Rowan's bandage).
**672 The Long Drop** — road sign; the winding-tower; **"The Cage"**: the Mandate checkpoint (barrier, scanner post, two officers; NULL scan), then the descent (a screen-tint fade to black, the tally on the cage wall; V130 1 → 2). Trainers in the side galleries.
**260 Ironreach** — arrival autorun at the cage-foot (V130 == 2): the pit announcer on a gantry (four extra lines by place, see the script), the miner, the chalk-circle woman, the Nadir boy, the Conclave notice (sign); chalk circles (decor, with pairs of NPCs). The Gutter Book board at the Last Rung (Six-Fingers Ottoline): NA_LAMPLIGHTER_KIDS and NA_PIT_RINGER, **closed while V130 is 6–9**.
**261 Ironreach Pokémon Center** — the night bulletin (autorun on the first heal after V130 == 11), the Gazette board, the nurse; **Interlude II starts from the bed here** (sleep → 294).
**262 Ironreach Mart** — the announcer's Mart line at the door.
**263 The Iron Pit** — the biggest map of the chapter. Needs: the fighting floor, the Wardens' table and benches, eighteen banners on the lowest gallery, the observers' gallery above, the challengers' bench, the announcer's gantry, the bracket slate with Nell's crate, the undercard pens, a stair up to the upper ring (264) that a scripted rockfall blocks after the tag battle, the cage-lift gate. Events: **"The Conclave Opens"** (autorun, first entry; Hollis at the table; the roll-call with eighteen Warden events in their seats, branch lines by `:ch2_tamsin`, `:ch8_caldera`; Odessa's skiff drops over the rim; V130 = 3); **free-roam Warden lines** (V130 3–5: Juno with Rowan, three pages by `:ch7_ledger`, the bare ring finger; Corvin; Dorian (+`:ch5_lowlight_testimony`); Marisol (by `:ch4_teo`); Anja, the Dominar's envoy and Kassan's envoy in the observers' gallery (the Lease papers, then the seals gone); Nyx (milk); Celestine (two options); Bastian; Magnus; Sigrun; Rook; Sahar (`:ch6_drillsite`); Odessa; Ilsa (moves away); Voss and Calla); **"The Bracket"** (comedy, Nell, Kaito with the form, Juno, Kestrel; one bubble line; V130 = 4); Kestrel and his Scizor; **the Open** (three pit-fighters in sequence with heals at Nell's crate: Pit Brawler Dunmore, Crush Kin Ysa, Old Gristle; the crowd-chant SE; the undercard stranger with a Lucario); **K4** (`RIVAL_KESTREL` version 40 + slot; the veiled woman in the gallery, gone after; OPEN CHAMPION'S CHALK; S122; V130 = 5); **"The Vote"** (autorun on returning from 265 with V130 == 6: Hollis, Marchetti in the petitioners' box, the hands, lights out, Sable on the speakers); **the tag battle** on the floor (PC + Kestrel vs `HOLLOW_SABLE` 0 + `HOLLOW_ADMIN,Brisk` 0; the rockfall; V130 = 7); **"Mandate Jurisdiction"** (autorun on returning from 264 with V130 == 9: the stretcher, Marchetti's squad, Hollis's acclamation; V113 = 1, V111 = 1); Kestrel's "It's not her" (three pages by `:ch6_kestrel_rumor`, with the Bond deltas); Juno in the glass dust (pages by `:ch3_juno_talk` and `:ch7_ledger`, with the Bond deltas); the stretcher and `:ch9_rowan_words` (S123, V130 = 10); **"A Seat to Fill"** (Valen, Brann's look, Calla, Nyx; V130 = 11). After V130 >= 10 the Pit shows its damage: the fallen stair, glass on the upper ring, the cut banners.
**264 The Reliquary [NEW]** (~25×19; the Pit's upper ring, reached by the 263 stair, or by the shafts after the rockfall) — the reliquary on its plinth with the Splitter clamp (event sprite); two root-wrapped Hammer grunts (decor); **the Mourner** (three-option opening; `Prismfall::Bosses.trainer_battle(:HOLLOW_MOURNER, "Mourner", 0, boss: :MOURNER_TREVENANT, species: :TREVENANT)`); **cutscene IR-1** (storyboard above); the field and tint go Bleed; the root-wall (event, after the cutscene); Juno and Nell at the gallery edge; the mask halves on the floor (two events, inspectable later: "Ash-bark. One half has a lily on it."); Rowan (S124, V130 = 8); the walk into the Bleed; **`:ch9_teo_sable`**: Teo under the scaffolding (an event inside the Bleed), Sable at the Meridian service lift in the rock wall, the lift grille, `HOLLOW_SABLE` v1 for the chase branch, COMM-DEVICE, Marisol at the edge; V130 = 9. Field `:COLOSSEUM` for the boss, `:BLEED` after IR-1, `:CAVE` for the chase.
**265 The Old Aurel Shafts [NEW]** (~40×30; under the Pit, between the gym and the galleries) — timber props, ore carts; **Teo** in a porter's coat with a Carvanha bucket (touch, once, V130 == 6; two pages by `:ch4_teo`); **Sable** (only if `standing(:HOLLOW) >= 4`; `Prismfall.checkpoint` first; the GO_PULL_THE_NAIL chain); the way up to 263 (it starts "The Vote" on arrival). After S123: Garret's cameo (NA_GARRET, CAMEOS #3) in the lower shafts, and the way into 264 round the rockfall.
**270–275 Kaito's gym (Gym 8)** — as GYM_PUZZLES Gym 8; Kaito's sign (270); the gym guide; Apprentice Hiro's hints (273); **Kaito (274), single battle**, the ace line, the PROMISE BADGE, TM31 Brick Break, the Lucario looking at the PC; V130 = 6; **Odessa at 270's door after the badge** (HM02 Fly); **275 Marrowgate Door** Mastery (plaque, knocking SE loop, Lucario aura) and Kaito's line after it.
**294 The Heartgarden (Interlude II, dawn)** — V119 = 2; the party swap to Rowan's team; the Bride Tree (action; the falling blossom); the Trevenant (action; the lily); the potting shed (the envelope; the ring; the Gale Post box at the gate); the head of the stair down to 708 (the mask); the title cards (V101 = 3, V102 = 10). The Heartgarden is in its **normal** state here (V106 = 0), before Ch10's runaway bloom.

**Trainer designer:** `HOLLOW_SABLE` **version 1** [NEW] (the chase: one Pokémon, Drapion, Lv 43, Sniper/Battle Armor, on `:CAVE`; LoseText "Keep it, then. It only plays one song."); the Open's three pit-fighters (Pit Brawler Dunmore: Machoke, Hariyama, Lv 39–40; Crush Kin Ysa: Mienfoo, Pancham, Lv 40; Old Gristle: Hitmonlee, Hitmonchan, Sawk, Lv 41, the old style); route trainers on 660, 661, 672. **String fixes made in `pbs/trainers.txt` (LoseText only):** `RIVAL_KESTREL` 40–42 / 140–142 / 240–242 → "Keep the title. I'm not here for a title."; `HOLLOW_MOURNER` 0 / 100 / 200 → "Not now - you don't understand - get BACK!". **BOSSES.md:** `:MOURNER_TREVENANT` still needs its config (PBS comment: "still to be written"); suggested 2 bars on Standard and 3 on Hard, the second bar's break making him use Protect on every turn he's below half ("he fights defensively"). **Items owner:** OPEN CHAMPION'S CHALK (Key Item, flavour), COMM-DEVICE (Key Item; `chose(:ch9_teo_sable, :chase_sable)`), KELP TEA BAG (flavour, "Six"). **Cutscenes owner:** IR-1 "The Partial Shatter" (5 shots, ~8 s). **Badge name (proposed):** the **Promise Badge** ("A fist is a promise").
- **Playscript & Restrained Rejuv Expressions pass (2026-11-24):** Multi-box playscript pacing (`<= ~85 chars/box`), restrained portrait tagging (70–80% `[name: Name]` carry outside the 18-Warden single-line roll-call), 29 verified portrait cast members checked against `graphics/Portraits/`, sparing `\pfe[...]` emotes (`0–2`/scene), strict zero-joke hold from "The Vote" lights-out through Valen's exit.
