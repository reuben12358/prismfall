# Script: Chapter 7 — "The Quiet Ward" (the Leach Road, Mirefen, Gym 6; J2)

> **Final playable script** for Chapter 7. It covers the Leach Road (620 the Marrow Road's east end, 632 the Kneeling Stones, 621 the Leach Canyons with 630 Charwell, 634 Wormwood Lea, 633 the Gutterfall) down into Nadir, then Mirefen (220–223; the Sweet Market), the Weeping Fen 648 (Wick), and the Infirmary gym (230–233, Gym 6). None of these maps is built; the list at the end is what to build from.
> Follows `story/25_SCRIPT_CH6.md`; conventions of `story/20_SCRIPT_CH0-2.md`.
> Sources: 05_ACT_II Ch7, 03_CAST (Corvin, Wenlow, Juno, Wick, Sable), 09_MYSTERIES (#2, #19, #20, #21, #26), NARRATIVE_KEYS (`:ch7_ledger`, GO_SWEET_TOOTH), 15_COMEDY (Ch7 "Invoice"; running gag 7; the Nadir bits), GYM_PUZZLES Gym 6, TRIALS_QUESTS (the Gutter Book, Ch7), CAMEOS (Venam), BALANCE (J2, Corvin), `design/CHAPTER_BEATS.md` (proposal B, approved by the creator 2026-11-21).
> **The Ward Night is canon** (CHAPTER_BEATS proposal B, approved by the creator 2026-11-21). It replaces 05_ACT_II's old roof scene, where Sable's broadcast was only a cliffhanger.

## Conventions
As in the earlier scripts. **Portrait cast here:** Juno, Corvin, Wenlow, Wick, Sable (on screen), Mother Gutter (`GUTTER`, one line). **Plain:** Noct and the Octave, Six-Fingers Ottoline, Venam (cameo), the Ward's patients, the Sweetrot vendors, every townsperson and trainer. Events call `Prismfall.gym_battle(pfm_gym(:LEADER_CORVIN), double: true)`.
**Counter:** V127 **CH7_STEP** (design/FLAGS.md): 0 east on the Marrow Road · 1 down the Gutterfall (the first descent into Nadir) · 2 the Infirmary and the Ward (Corvin, Wenlow, the patients by name) · 3 J2 and the ledger (S118) · 4 Wick at the Weeping Fen (S119) · 5 Gym 6 won · 6 the Ward Night · 7 chapter closed (V102 = 8).
**Sweetrot counter:** V128 **SWEETROT_TAKEN** (0–3). Every vendor offer adds 1 when accepted; the third acceptance is GO_SWEET_TOOTH.

## The chapter's key events (design/CHAPTER_BEATS.md)
1. **J2 and the ledger.** Juno, alphabetising Corvin's ledgers, finds "R.A. — Bleed-burn, right palm and fingers, lightning pattern" on the night of the Shatter. Build-up: her Ch6 letter (the right hand, the kettle, "every time"). `:ch7_ledger` decides how Ironreach hits her.
2. **The Ward Night.** The night of Sable's broadcast, the Hammer cuts the Infirmary's current; the Quiet Ward's Bleed rises into a Veil; the PC carries out Ama, the salt-haired girl Wenlow introduced by name, and under the glass her eyes are moving. Corvin: "They're not dying. They're *dreaming*." The Hammer becomes the Hollow's enemy on screen, and Wick's "he wants to carry them home" lands as a split.
**No jokes** inside the Ward Night from the moment the lights go out until the dampers are back on (15_COMEDY §1). Wenlow is cheerful all chapter: write every Wenlow line so it hurts on a replay after Ch16.

---

# CHAPTER 7 — "The Quiet Ward"

**Chapter start:** V102 = 7, V127 = 0 (Juno's letter, Ch6 close).

## Map 632 — The Kneeling Stones (Ossaria's crossroads)
```
ROAD SIGN (the crossroads post): ← DUNEHOLT · ↓ CHARWELL & THE LEACH · → VIGIL (closed: "BY ORDER OF THE EMBALMERS. WE'RE BUSY.").
(Nine standing stones bent forward in a ring, as if they'd all knelt at once to look at something on the ground.)
[name: Caravan Guide] They say they knelt when the Prismfall came over. Looked up, saw the sky breaking, and knelt. Stones aren't stupid.
```

## Map 621 — The Leach Canyons (borderland D) and Map 630 — Charwell
```
ROAD SIGN: THE LEACH CANYONS — ↑ the Kneeling Stones · ↓ Charwell & Wormwood Lea. Don't drink the river. The river's had a drink already.
(Red canyon walls. Down the middle runs the River Leach, and into it, from pipes in the cliff, Lumen's foundry runoff: streaks of blue and silver in the brown water.)
[name: Char-burner] Ossarian bone-char filters Nadir's poison. Burn the bones, pack the char, run the water through. Clean water. For now. The runoff's thicker every month.
CHARWELL (630): a cliff-cave town; Ossarian char-burners and Nadir sump-folk; filter carts on rails.
[name: Sump-folk Woman] Up top they say Nadir's dirty. Up top's where the dirt comes FROM, love. We just live under the tap.
```
**[if `:ch6_drillsite` == :hollow] EV "Escort"** (621, touch strip at the canyon's narrows, once)
```
(Two Directorate officers step out from behind a filter cart.)
[name: Directorate Officer] By Mandate. You're the obstruction from Duneholt. You're to be escorted to the nearest checkpoint for questioning.
[name: Directorate Officer] That's not a request. It's not even an escort. It's an arrest with good manners.
BATTLE: MERIDIAN_DIRECTORATE "Officer" ×2 (double; Leach version). Field: per 621.
(WIN:) [name: Directorate Officer] ...You'll be in another report.
(They let you through. They don't know what else to do.)
```
*Trials on 630: "Clean Water" (NA_CLEAN_WATER), the Charwell chalk wall.*

## Map 634 — Wormwood Lea (Elowen, east of the Crown)
```
ROAD SIGN: WORMWOOD LEA — ↑ Charwell · ↓ the Gutterfall (NADIR). The wormwood stills: bitters, tonics, and Mirefen's medicine.
(Water-meadows in strips along the Leach, grey-green with wormwood. Copper stills steam in a row by the ford.)
[name: Still-keeper] Mirefen's doctor buys half our wormwood. The other half goes in drinks that make you forget Mirefen. Same plant. That's medicine.
```

## Map 633 — The Gutterfall: **"Down"** (the first descent into Nadir; autorun at the lift-cage, V127 == 0 → 1)
```
(The edge of the Crownland. The Leach goes over it in a blue waterfall into a gulf of air, and beside the fall, from the cliffs above, Zenith's outfall pours in: grey, warm, steaming. A ladder-town of shacks clings to the rock beside the fall.)
[name: Lift-keeper] Down's a copper. Up's a silver. Don't ask why. Everybody asks why.
(The lift-cage rattles down the cliff beside the fall. The light changes as you go. Then the sky goes: you're under the overhang, and above you, instead of sky, there's a ceiling of pipes and girders dripping slag, a city's underside, a city on a lid.)
(The air tastes of pennies.)
[name: Lift-keeper] Welcome to Nadir. Mind the drips. Rebreathers at the bottom, two bones. Don't buy the cheap ones. The cheap ones are just masks.
V127 = 1.
```

## Mirefen (220–223; Nadir; the runoff marsh)

### Map 220 — Mirefen: arrival (autorun at the lift's foot)
```
(Stilt-houses over a marsh, joined by walkways. Grey cranes on the roofs. Hollow Ring graffiti on every wall, and beside it, over and over, a painted Ogre in a sad mask: Nadir's folk-saint. Under the walkways the water is brown, and at the edges of the lamplight it glows faintly blue.)
[name: Noodle-cart Cook] Slag-fried noodles! You're new. You look it. Sit. I rate everyone out of ten. Nobody's scored over four.
[name: Noodle-cart Cook] (again) Boy in a black coat came through two days back. Three out of ten. Ate like he was angry at the bowl. Asked about masks.
[name: Mirefen Woman] People up top think we're dirty. We're the cleanest people in Velmora. We have to be. Everything else isn't.
[name: Child with a Grimer] (an Alolan Grimer) Don't be scared of Gloop. Gloop eats the bad bits. That's his job. He's very good at his job.
GRAFFITI (a wall): A grey ring broken at the top, and an Ogre's sad face. Under it, chalked: "HE TALKED. HE DIDN'T STEAL."
```
*(09 #20: Nadir's Ogre is the saint, not the villain.)*
*Trials in 220: "A Five Out of Ten" (NA_NOODLE_SCORE; Corvin has a two), "Lamps Out" (NA_OCTAVE_LAMPS_OUT; Noct of the Octave at the night-ferry steps; Octave 5 of 8), the Gutter Book's chalk board (Six-Fingers Ottoline).*

### The Sweet Market (220, the lower walkways) — **Sweetrot, offer 1**
```
(Stalls of pastel sweets on the lowest walkway, round and soft as mochi, pink and white and pale green. A faint smell of peaches and something under the peaches. The vendors are smiling. All of them. The same smile.)
[name: Sweet Vendor] Sweetrot! Try one. First one's free. First one's always free, sweetling.
> Take one.
  Script: $game_variables[128] += 1
  (It's soft and cool and it tastes of peaches, and for a second everything is fine. Everything is so fine. You'd agree with anyone about anything.)
  (The feeling goes. You want another one. You don't know why.)
> No, thank you.
  [name: Sweet Vendor] Next time. There's always a next time, down here.
[name: Child on the walkway] (singing) ♪ One for the sweet and two for the tongue, the peach that keeps you, keeps you young... ♪
```
*(09 #26: the peach that keeps you.)*
*If the PC took it, Wenlow's warning comes at the Infirmary (below).*

### Map 223 — Corvin Mott's Infirmary: **EV "The Quiet Ward"** (first entry; V127 == 1 → 2)
```
(The Infirmary stands on the highest stilts: whitewashed planks, lamps on long poles, a smell of carbolic and wormwood. The front ward is full: coughs, burns, a man asleep with a cup of tea going cold on his chest.)
(A young man in an apron two sizes too big comes round a screen with a tray of bottles, sees you, and nearly drops all of it.)
[portrait: WENLOW, happy] Oh! Visitors! Hello! I'm Wenlow, I'm the apprentice, mind the tray, mind the — there. Saved it.
[name: Wenlow] You're Juno's friend, aren't you? She said you'd come. She said you'd come and stand in a doorway looking serious. You're doing it now!
[if V128 >= 1]
  [portrait: WENLOW, panic] Oh — oh no, you've had a Sweetrot. I can smell it. Peaches. Don't have another one. Please. Don't have another one.
  [portrait: WENLOW, sad] We've a whole ward of people who had another one.
[portrait: WENLOW, happy] Doctor's in the Quiet Ward. Come up. You can meet everyone. I'll introduce you. I always introduce people. It's polite.
(The Quiet Ward: the top floor, quiet as snow. Forty beds. In them, people at Fixing stage two and three: some humming, some half glass, perfectly still.)
[portrait: WENLOW, neutral] This is Mister Garrod. He hums. We don't know the tune. If you know it, tell us; he'd like that.
[name: Wenlow] That's Old Fen. Glass to the elbow on the left. Plays cards with his right. He cheats. We let him.
[name: Wenlow] And the Tull twins, both at stage two, in the beds together because they cried when we split them up.
[portrait: WENLOW, sad] And this is Ama. She's nine.
(A small girl asleep under a blanket. Her hair, spread out on the pillow, has turned to salt: white, crystalline, catching the lamplight.)
[portrait: WENLOW, happy] She likes being told about the weather up top. I tell her every morning. I make some of it up.
(At the end of the ward, a gaunt man in a long oilcloth coat and a plague-doctor's half-mask is writing in a ledger. He doesn't look up.)
[portrait: CORVIN, deadpan] Wenlow, you've introduced them to every patient on the floor, haven't you.
[portrait: WENLOW, happy] Yes, Doctor!
[portrait: CORVIN, deadpan] Good. Somebody should.
[portrait: CORVIN, neutral] Corvin Mott. Warden, doctor, and the reason the Sump Barons don't sleep well. The mask's for the smell, mostly.
[name: Corvin] I've a ward of forty patients slowly turning into garden furniture. Forgive me if I don't stand for the Sovereign's anthem.
[portrait: CORVIN, neutral] Your friend's in the dispensary, doing something devastatingly cheerful to my filing. Go and stop her. Or don't. She found a ledger I'd lost in AF 296.
V127 = 2.
```

### Map 223 — the dispensary: **EV "R.A."** → **J2** → **CHOICE `:ch7_ledger`** — key event 1 (V127 == 2 → 3)
```
(The dispensary: shelves of brown bottles, Juno at a desk under a lamp with ledgers stacked round her like a fort, sorting them by year with great happiness. Her blossoms are the only colour in the room.)
[portrait: JUNO, happy] You came! You brought — you didn't bring snacks. That's fine. I've had noodles. Three out of ten, he gave me. He said I talked to the bowl.
[portrait: JUNO, neutral] Dr Mott keeps every patient in these. Every burn, every Fixing, every Sweetrot. In no order at ALL. I'm putting them in order. He hates it. He hasn't stopped me.
[name: Juno] This one's this spring. The Shatter. The night of the gala. He was up all night, look, nineteen people—
(She turns a page. She stops.)
[portrait: JUNO, neutral] "R.A. Second-degree Bleed-burn, right palm and fingers. Lightning pattern. Discretion."
[portrait: JUNO, neutral] ...
MOVE: Corvin comes in from the ward, sees the open ledger, crosses the room in three strides and takes it out of her hands. He closes it. He's not quick enough.
[portrait: CORVIN, neutral] That one's not filed yet. My handwriting. You'd never read it.
MOVE: Corvin goes back into the ward with the ledger under his arm.
[portrait: JUNO, happy] *(too brightly)* R.A.! There's loads of R.A.s. Roberta Ash. Rufus... Ardley. There's a man on the stilt-walk called Ras. 
[portrait: JUNO, neutral] Right palm. Lightning.
[portrait: JUNO, angry] Fight me. On the stilt-walk. Now. I need to hit something that isn't a thought.
Script: Prismfall.rival_battle(:RIVAL_JUNO, "Juno", 2)     # J2; version 20 + starter slot; field per 220's default (the stilt-walk)
(Mid-battle, when her ace comes out:) [portrait: JUNO, angry] He wouldn't. He WOULDN'T.
(LOSE: whiteout. Juno on retry: "Again. Please. I'm not done not thinking.")
(WIN:)
[portrait: JUNO, sad] ...
[portrait: JUNO, sad] He burned his hand on the kettle. That's what he wrote. The right one. The same night.
[name: Juno] He's never burned himself on anything in his life. He picks up hot pots with his bare hands. Aunt Elin used to shout at him for it.
[portrait: JUNO, crying] Say it isn't. Say something.
```
```
> "Rowan Ashby." (name_him)
  Script: pf_choose(:ch7_ledger, :name_him)
  [portrait: JUNO, angry] Don't. Don't you DARE say his name like it's an answer.
  [portrait: JUNO, crying] You don't know him. You met him for ten minutes in a station with a sick Phantump. You don't KNOW him.
  MOVE: Juno runs off along the stilt-walk, veil catching on the rail. She doesn't look back.
> "There's loads of R.A.s." (reassure)
  Script: pf_choose(:ch7_ledger, :reassure)
  [portrait: JUNO, sad] ...There are. Aren't there. There are loads.
  [portrait: JUNO, happy] Thank you. I'm being silly. I said in my letter, I'm being silly. I just needed somebody else to say it.
  (She hugs you, too hard, and goes back to the ledgers. She doesn't open that one again.)
> Ask Corvin. Later, alone. (ask_corvin)
  Script: pf_choose(:ch7_ledger, :ask_corvin)
  [portrait: JUNO, neutral] ...Yes. Ask him. You ask him. I can't.
  (Later. The ward. Corvin is changing a dressing on Old Fen's good hand.)
  [portrait: CORVIN, neutral] I'm a doctor. I treat hands. I don't ask whose.
  [portrait: CORVIN, sad] And I'd thank you not to ask me twice, because the second time I might tell you, and then it'd be yours to carry. Not mine.
Switch S118 CH7_J2_DONE = ON. V127 = 3.
```
*(09 #2. NARRATIVE_KEYS: `:name_him` JUNO −3 now, +2 at Ironreach (she already knew); `:reassure` +2 now, −2 then.)*

**Sweetrot, offer 2** (the Sweet Market, after J2; the vendor walks up the walkway to you)
```
[name: Sweet Vendor] You look like you've had a day. Here. This one's half price. Because I like you.
> Take one.
  Script: $game_variables[128] += 1
  (Peaches. Everything is fine. Juno is fine. The ledger is fine. You'd agree with anyone.)
  (It goes. You want another one more than you wanted the last.)
  [if V128 >= 2] [portrait: WENLOW, panic] *(from the walkway above)* NO. No no no. That's two. Please. That's two.
> No.
  [name: Sweet Vendor] (smiling the same smile) Third time's the charm, sweetling.
```

## Map 648 — The Weeping Fen: **EV "Brother Wick"** (V127 == 3 → 4)
```
(A Hollow medicine-runner went into the Fen at dusk with a sack of Corvin's bandages; Corvin points you after him. Past the last walkway the marsh is a Bleed zone: rain falls UP out of the puddles, slowly, and every pool weeps.)
FIELD NOTES pop-up: "THE WEEPING FEN — BLEED. Rain falls upward here. The pools cry. I don't know why the pools cry. (Larch: 'Nobody knows why pools cry. Come out of the pools.')"
(A drowned chapel, half sunk, its roof open to the upward rain. Inside, an old man with one milky eye sits among four dying Bereaved on straw, with his hand on the forehead of the nearest one, murmuring.)
[portrait: WICK, neutral] Ah. The one who walks in. I hoped I'd meet you. I'm told I mustn't.
[name: Wick] Brother Wick. I was a priest of the Prism Choir until I read the wrong book. Now I'm the Hollow's, which is a smaller choir with worse hymns.
[portrait: WICK, sad] These four were in the Lowlight. Not inside the glass. At the edge. The edge is slower. I'm blessing them. They asked.
```
```
[if pf_cond("standing(:HOLLOW) >= 4 || choice(:ch5_lowlight_testimony) == :someone_else")]
  [portrait: WICK, neutral] You told the Directorate somebody else was in the vault. Word got down here. Or you've been kind to us, which is rarer. Either way, I don't have to fight you. Sit.
  (No battle.)
[else]
  [portrait: WICK, sad] I won't let you take them up into the Mandate's hands. Not tonight. Forgive me. I'm very bad at this.
  BATTLE: HOLLOW_WICK "Wick", version 0. Field: Hollow Cathedral (the Fen outside is :BLEED; the drowned chapel is consecrated ground).
  (WIN:) [portrait: WICK, neutral] There. You've beaten an old man in a chapel. Now sit, please, my knees are worse than my Pokémon.
(All:)
[portrait: WICK, neutral] The Choir teaches that the Plates were a gift. Child, nobody bleeds for three hundred years from a gift.
[name: Wick] A gift doesn't need eighteen Wardens to guard it. A gift doesn't need a Festival every ten years to keep it quiet. A wound does.
[portrait: WICK, sad] And the woman who broke the Zap Plate wasn't one of ours. Not the way she says. The Mourner came back from Lumen with his hand burned and didn't speak for three days.
[portrait: WICK, neutral] He doesn't want to break them any more. He wants to carry them home.
(He looks at you. Not at your face. At your chest, where the scar is, under your shirt.)
[portrait: WICK, sad] But you can't carry what you can't hold. And nobody can hold them. Nobody I've ever met.
(He doesn't say why he's looking. He looks away.)
Switch S119 CH7_WICK_DONE = ON. V127 = 4.
```
*(09 #19, the Wound Doctrine; 09 #1, Wick looks at the PC's chest. 02_FACTIONS: the split between the Mourner's "carry them home" and Sable's Hammer.)*

### Map 223 — comedy scene Ch7, **"Invoice"** (returning from the Fen)
```
[portrait: CORVIN, deadpan] Sit. Tongue out. Follow the finger. Lovely.
[portrait: CORVIN, deadpan] Your bill.
(Received: INVOICE. "Item: one (1) heart attack, mine. Item: gauze. Item: the look on Wenlow's face. TOTAL: ₽0.")
> I'm fine.
  [portrait: CORVIN, angry] You walked into a marsh that rains UPWARD. "Fine" is not on the menu, dear.
> The rain went up.
  [portrait: CORVIN, deadpan] I'm aware of the direction of the rain. I'm a Warden. I get a memo.
[portrait: WENLOW, happy] Doctor, they did bring back the medicine-runner's sack—
[portrait: CORVIN, deadpan] Wenlow, I'm having an emotion. Don't help.
[bubble: WENLOW, panic, sweat] Sorry, Doctor!
(Wenlow drops a tray.)
[portrait: CORVIN, sad] ...Item four. One tray.
```
*(Running gag 7, Corvin's bills, starts here. Every invoice totals ₽0.)*

**Sweetrot, offer 3** (outside the Mirefen Pokémon Center, the evening before the gym)
```
Script: Prismfall.checkpoint     # NARRATIVE_KEYS §10: GO_SWEET_TOOTH's checkpoint, the Mirefen Pokémon Center
(A vendor is waiting at the Center's steps with a little paper box tied with ribbon. The smile. The same smile.)
[name: Sweet Vendor] I saved you the best one. The pink. Nobody else gets the pink.
[if V128 >= 2]
  > Take it.
    > ...Really?
      > Take it.
        Script: $game_variables[128] += 1
        (Peaches. And then nothing is ever wrong again, and you never wonder why again, and you are so very happy, for the rest of your life.)
        Script: Prismfall.game_over(:GO_SWEET_TOOTH)
      > No.
  > No.
[else]
  > Take it. → Script: $game_variables[128] += 1 (as offer 1)
  > No.
[name: Sweet Vendor] (if refused) Mother Gutter will be so disappointed.
[portrait: GUTTER, happy] *(a vast shape on a barge passing under the walkway, with a Muk the size of a cart asleep beside her)* No she won't, dear. She's patient. Peaches are patient.
```
*(Mother Gutter's one line; she returns in Act IV. GO_SWEET_TOOTH: "the third offer is the sweetest", Wenlow's warning after the first.)*

## Maps 230–233 — the Infirmary gym (Gym 6; GYM_PUZZLES Gym 6; a double battle)
```
CORVIN'S SIGN (230): "If you can count to three, you can count to anything. Measure, don't guess."
[name: Gym Guide] The Infirmary! Poison-types on the Corrosive Mire. Ground and Psychic cut through it. Fairies melt. The Doctor fights two at once. He says it's because patients come in pairs.
[portrait: WENLOW, happy] (the apprentice, 231 and 232; hints) Sir always says: the empty space is a measure too. / Get a two into the little one first. / (the solution)
[portrait: WENLOW, happy] (232, on the filter steps) Mind your mask! Sir says I'll run this place one day. I say not till I can carry a tray.
```
### 233 — the Theatre: Corvin (double)
```
(The Infirmary's old operating theatre: tiered seats round a sunken floor flooded with glowing runoff. Corvin stands at the edge with his mask pushed up, two Poké Balls in one hand.)
[portrait: CORVIN, neutral] Everything's poison, dear. Dose makes the cure.
[portrait: CORVIN, deadpan] Two at once, because nobody in Nadir ever has only one thing wrong with them.
[portrait: CORVIN, smug] Don't worry. I'm a doctor. I know exactly how much this hurts.
Script: Prismfall.gym_battle(pfm_gym(:LEADER_CORVIN), double: true)     # LEADER_CORVIN, :CORROSIVE_MIRE, cap 35, double
(When his ace enters:) [portrait: CORVIN, neutral] Ward. The patient one. Hold them.
(LOSE: whiteout. Corvin on retry: "Back on the table. Good. Second opinions are healthy.")
(WIN:)
[portrait: CORVIN, deadpan] ...Well. That's the correct dose.
(Received: the REMEDY BADGE.)
(SE: six notes. The case's light runs along its seams like water in a channel.)
[portrait: CORVIN, neutral] Your case sings. I'd have that looked at. Not by me. I'm busy.
(Received: TM84 POISON JAB.)
[portrait: CORVIN, neutral] Poison Jab. Close in, quick, and they go home feeling worse. It's the bedside manner I was never taught. And that badge says Pokémon up to level thirty-nine will heed you.
[name: Corvin] The ferrymen will teach yours Surf. Lake Sallow's that way. Cindervault's past it. Don't drink the lake either.
V127 = 5.
```
*Surf (HM03) from the Mirefen ferrymen after the badge (Core config: Surf at 6 badges).*

## Map 223 — the Infirmary roof, then the Quiet Ward: **EV "The Ward Night"** — key event 2
*(Autorun the first time the PC returns to the Infirmary after Gym 6; V127 == 5 → 6.)*
```
(Night. The Infirmary roof, over the blue-glowing marsh. Corvin has two tin mugs of bog coffee and a lamp. He has taken the mask off. Without it he looks older and kinder and more tired than anyone you've met.)
[portrait: CORVIN, neutral] Sit. It's bog coffee. It tastes exactly like it sounds.
[name: Corvin] I haven't slept properly since AF 288. You get used to it. You don't, actually. You get used to saying you've got used to it.
(Down on the walkway, every lamp-screen in Mirefen flickers at once. The picture on all of them: grey static, then a face. A woman, the top half masked, the bottom half smiling.)
[portrait: SABLE, happy] *(on every screen in Nadir)* Evening, Nadir!
[name: Sable] The Mourner's gone soft. You can tell; he's stopped turning up. He wants to "carry them home". Bless.
[portrait: SABLE, happy] The Hammer hasn't gone soft. The Hammer doesn't carry things. The Hammer breaks them, until somebody up there listens.
[name: Sable] Cindervault's next. Light for everyone, right? Let's start with you.
(And the Infirmary's lamps go out.)
(Not the screens. Every lamp in the Infirmary, at once. And then a sound from the top floor, from the Quiet Ward: a long, rising chime, like a wet finger on a glass, getting louder.)
[portrait: CORVIN, shocked] The dampers.
[portrait: CORVIN, angry] The ward's dampers run on Zenith current off the Gutterfall junction. Somebody's CUT the junction—
(Wenlow bursts up the roof ladder, white.)
[portrait: WENLOW, panic] Doctor! Doctor, the ward, the Bleed's coming up off the beds, it's — it's a Veil, Doctor, it's a Veil across the door, I can't get IN—
```
```
(The Quiet Ward's doorway. Across it, a shimmer like heat over a road. Behind it, the ward in grey, wrong light, the beds, the patients. The glass on Old Fen's arm is climbing toward his shoulder as you watch. Mister Garrod has stopped humming. The chime fills everything.)
(Corvin puts his hand to the Veil and snatches it back, burned. Juno arrives at a run with a lamp, sees it, and stops.)
[portrait: JUNO, shocked] It's the same. It's the Lowlight. It's the—
[portrait: CORVIN, neutral] The dampers hold the ward's Bleed down. Without them it goes up like this, and in an hour every patient on that floor is stage four.
[portrait: CORVIN, sad] Stage four doesn't come back.
[name: Corvin] The stills. Juno. The seed-medicine stills run on peat, not current. If we can get the stills to the damper coils, the medicine might hold them — might—
[portrait: JUNO, neutral] I'll do it. I know where the stills are. I've been sorting this building for a week.
MOVE: Juno runs down the stairs with Wenlow.
(Corvin stays at the Veil. He looks at you.)
[portrait: CORVIN, neutral] I've heard about you. The Lowlight. You walked in.
[portrait: CORVIN, sad] The child nearest the window. Ama. She's the furthest along and she's the smallest. If anyone goes past three tonight, it's her.
[name: Corvin] I'm a doctor. I can't ask you to walk into that. So I'm not asking.
```
```
(You walk in.)
(Inside, the chime is everywhere. The light is grey and comes from every direction. Your skin doesn't burn. Under your ribs something is very still.)
(Ama's bed by the window. The salt in her hair has spread down onto the pillow and onto her cheek, and it's turning clear, the way the Lowlight turned clear.)
(You lift her. She's light as a lamp. Glass and salt crackle under your hands.)
(At the Veil's edge, with Ama in your arms, you look down.)
(Under the clear salt over her eyes, her eyes are moving. Side to side. Fast. The way eyes move when someone's dreaming.)
WAIT 60.
(You carry her out through the Veil.)
[portrait: CORVIN, shocked] ...
(He takes her. He puts two fingers to her throat, then lifts the lamp to her face, and holds it there a long time.)
[portrait: CORVIN, sad] You saw that. Tell me you saw that.
SE: from below, the clank of iron and a hiss of steam. The chime falters.
[portrait: JUNO, neutral] *(from the stairwell, shouting)* The stills are on the coils! It's — it's taking! Is it taking?
(The Veil across the door thins, wavers, and sinks back into the beds like mist going down into grass. The chime stops. In the ward, Mister Garrod starts humming again, the same tune nobody knows.)
(Old Fen's glass has stopped climbing. It's at his shoulder.)
[portrait: WENLOW, crying] Old Fen? Old Fen, can you hear me? ...He winked. Doctor, he WINKED.
```
```
(Later. The roof. The coffee is cold. Ama is back in her bed under three blankets, and Wenlow is sitting with her, telling her about the weather up top. Some of it is made up.)
[portrait: CORVIN, neutral] Do you know why nobody in my Ward is dead?
[portrait: CORVIN, sad] They're not dying. They're dreaming.
[name: Corvin] I've watched their eyes move under the glass for twelve years, and I've never said it out loud, because a doctor who says "dreaming" about a stage-three Fixing gets laughed out of the Accord's medical college.
[portrait: CORVIN, neutral] You saw it too. So now there's two of us. Two's a study.
[name: Corvin] Somebody should find out what they're dreaming about.
[portrait: JUNO, sad] *(sitting down on the roof's edge next to you, soot on her face, blossoms singed)* The Hammer did this. Sable did this. On purpose. To a ward full of people who can't run.
[portrait: JUNO, neutral] The man in the mask, in Saltmere. He never hurt anyone. He said "let the land grieve". He sounded sad.
[portrait: JUNO, angry] She doesn't sound sad. She sounds like she's enjoying it.
[portrait: CORVIN, deadpan] That's how you tell them apart, in my experience. The ones who are enjoying it.
(Received: INVOICE. "Item: one (1) ward, carried. Item: one (1) child, carried. Item: the look on my face. TOTAL: ₽0.")
V127 = 6.
```
## Chapter 7 close (220, the lift-foot; V127 == 6 → 7)
```
(Morning. The marsh is grey again. On every wall the Hollow Ring has been painted over in the night with a hammer. Under one of them, somebody has chalked: "NOT OURS. — the Hollow".)
[name: Mirefen Woman] The Hammer did the ward. The Hollow did the chalk. I didn't know there were two kinds. Now there's two kinds.
[name: Ferryman] Surf's yours, if the Doctor says so. Lake Sallow's east, past Leechman's Walk. Then up into Ashkaar. Mind the sulfur. Mind the dragons. Mind everything.
[portrait: WENLOW, happy] *(at the lift, waving with both arms)* Come back! Bring Juno! Bring snacks! Bring weather!
QUEST LOG: "Eighteen Roads" — Earn the seventh badge in Cindervault, across Lake Sallow into Ashkaar.
V127 = 7. V102 STORY_CHAPTER = 8.
```
*(Juno stays in Mirefen with Corvin until the Conclave (Ch9). Sable's "Cindervault's next" is the Ch8 hook: the Hammer's bomber at the caldera.)*

**Optional: "Sewer Royalty"** (Venam's cameo; CAMEOS.md #2; NA_VENAM on the Gutter Book, `badges >= 6 && S118`): Venam's Testimony ("I could hear everything") is the Envoy's proof in Ch20 and can be played for Juno in Ch10. The PC, who has seen Ama's eyes move, gets one extra line from Venam: `[name: Venam] Moving eyes? Yeah. Mine did that. Nobody believed me either.`

---

## Map events needed (Chapter 7)

None of these maps is built. V127 = **CH7_STEP**, V128 = **SWEETROT_TAKEN** (design/FLAGS.md).

**632 The Kneeling Stones** — the crossroads post (sign; Vigil closed); caravan guide.
**621 The Leach Canyons** — road sign; char-burner; **"Escort"** (touch strip at the narrows, once, only if `pf_choice(:ch6_drillsite) == :hollow`): two `MERIDIAN_DIRECTORATE` "Officer" (a double; Leach version). Route trainers.
**630 Charwell** — sump-folk woman; filter carts (decor); Trials (Clean Water, the chalk wall).
**634 Wormwood Lea** — road sign; still-keeper; the stills (decor).
**633 The Gutterfall** — the lift-cage (**"Down"** autorun once at the lift; V127 = 1; a screen-tint change as the cage descends under the overhang); the lift-keeper.
**220 Mirefen** — arrival lines (noodle-cart cook with a Kestrel page, Mirefen woman, child with an Alolan Grimer); the Ogre graffiti (sign); **the Sweet Market** on the lowest walkway (vendor 1 with offer 1; a singing child); **vendor 2** walks up after S118 (offer 2; Wenlow's panic line from above if V128 >= 2); Trials (A Five Out of Ten, Lamps Out, the Gutter Book board); the chapter-close morning (the overpainted rings, the chalk, the ferryman, Wenlow at the lift; V127 = 7, V102 = 8).
**221 Mirefen PC** — **vendor 3** on the steps outside (`Prismfall.checkpoint` first; the GO_SWEET_TOOTH chain if V128 >= 2); Mother Gutter's barge passing under the walkway (one-line event, a big sprite and a Muk).
**223 Corvin Mott's Infirmary** — the front ward (NPC patients); **the Quiet Ward** top floor: forty beds (decor), named patients as events (Mister Garrod, Old Fen, the Tull twins, **Ama** by the window); **"The Quiet Ward"** (first entry; Wenlow's introductions; Corvin; V127 = 2); **the dispensary** with Juno and the ledgers: **"R.A."** → J2 (`RIVAL_JUNO` version 20 + slot) → `:ch7_ledger` (S118, V127 = 3); "Invoice" on returning from the Fen; **the roof**; **"The Ward Night"**: a lights-out tone, a Bleed Veil event across the Quiet Ward's door, Ama's bed by the window (the PC carries her out: the PC's sprite with a carried-child pose, or a fade), the stills-to-coils SE, the Veil's fade, Old Fen's wink. Sets V127 = 6.
**648 The Weeping Fen** — Field Notes; upward rain (fog/particle); the drowned chapel; Wick with four Bereaved on straw; the talk-down check (`standing(:HOLLOW) >= 4 || choice(:ch5_lowlight_testimony) == :someone_else`) or `HOLLOW_WICK` v0 on `:HOLLOW_CATHEDRAL`. S119, V127 = 4.
**230–233 the Infirmary gym (Gym 6)** — as GYM_PUZZLES; Corvin's sign; the gym guide; Wenlow's hint lines; Corvin (233) double battle, the ace line, the REMEDY BADGE, the TM; the ferrymen teach Surf. V127 = 5.
**644/645 Miasma Caverns** — Venam's cameo (CAMEOS.md), NA_VENAM.

**Trainer designer:** a Leach-canyon version of `MERIDIAN_DIRECTORATE` "Officer" (a double, Lv 31–33). **Items owner:** INVOICE (Key Item, flavour; the text changes each time), Corvin's TM is TM84 Poison Jab (GYM_PUZZLES). **Badge name:** the Remedy Badge (creator, 2026-11-21).
