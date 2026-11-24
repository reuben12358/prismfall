# Script: Chapter 10 — "The Seat That Blooms" (the Root Road, Verdance, the Bride Grove, Gym 9; J3)

> **Final playable script** for Chapter 10, the first chapter of Act III. It covers the Act III opener and the Root Road (692 the Tailings, 680 the Rootdeep and its Lift Road, 690 Lanternroot, 681 Prism Falls, 693 the Briarway; optional 684/685 Grudgestone Quarry, 688 Echo Coliseum), the Standing branch (698 the Hollow Sanctuary or 699 the Meridian Black Site), Verdance (280–289, 294–296), the Bride Grove 708 (Juno's trial, Ogerpon, the Loyal Three), the Heartgarden Gym (290–293, 297; Gym 9, J3) and the Royal Chase 682. None of these maps is built; the list at the end is what to build from.
> Follows `story/27_SCRIPT_CH9.md`. Sources: 06_ACT_III Ch10, 03_CAST (Juno, Rowan, Valen, Maelis, Caedmon, Tamsin, Wick, Quent, Calla), 09_MYSTERIES (#4, #14, #16, #19, #20, #21, #26), NARRATIVE_KEYS (`:ch10_null`, `:ch10_ogre`, `:ch10_succession_stance`, GO_LOYAL), 15_COMEDY (Ch10 "The Royal We"; the Wardens' Circular; the Elowen bits), GYM_PUZZLES Gym 9, TRIALS_QUESTS (`EL_GERALD`, `EL_ROOTWARD_WAKE`, `EL_EVER_BLOOM`, `EL_BRIDE_TREE_HEART`), CAMEOS (Melia; Venam's Testimony), BALANCE (J3), `design/CHAPTER_BEATS.md`.

## Conventions
As in the earlier scripts. **Portrait cast here:** Juno, Valen, Maelis, Tamsin, Wick, Calla, Quent, Kestrel, Corvin (one line by letter), Celestine (one line). **Plain:** Prince Caedmon (not in `Prismfall::Portrait::CAST`), the Meridian delegate, the Thornguard, the press, Bram, the Lowmarsh weavers, Lanternroot's growers, the refugees, Melia (cameo), every townsperson and trainer. Ogerpon and the Loyal Three are Pokémon: staging only, no portraits. Events call `Prismfall.gym_battle(pfm_gym(:LEADER_JUNO), double: false)`: J3 is a **single** battle (Core `GYMS`, BALANCE §5; GYM_PUZZLES 293 said double and is corrected).
**Counter:** V131 **CH10_STEP** (design/FLAGS.md): 0 the Act III opener · 1 the Lift Road branch · 2 Kestrel at the Lift's top station · 3 arrived in Verdance (the bloom) · 4 the testament (Juno named; the ring) · 5 the Bride Tree with Juno · 6 into the Bride Grove · 7 the Loyal Three done (S127) · 8 the Plate accepts Juno (S125; V106 = 2) · 9 Gym 9 won (J3) · 10 Juno's first act, and `:ch10_succession_stance` · 11 the Royal Chase opened (S126) and the Queen's garden · 12 "Dear Uncle Rowan" (chapter closed; V102 = 11).

## The chapter's key events (design/CHAPTER_BEATS.md)
1. **Juno becomes Warden.** Rowan's testament names her; Valen puts his ring in her hand; she walks the Bride Grove behind the PC to the Meadow Plate in the Bride Tree's roots, and the Plate accepts her. Build-up: Ironreach, Verdance drowning without a Warden, the three claimants, "I didn't want this seat". Payoff: the bloom goes quiet under her hand. Consequence: the Greenward, Juno's Act III–IV politics, J4.
2. **The Loyal Three and the truth about the Ogre** (`:ch10_ogre`, GO_LOYAL). The pageant's heroes come for the Plate in Sweetrot-pink collars; the Ogre that has guarded Elin since AF 288 roars at the PC. Build-up: the Ch2 pageant, the Mourner's "poison on their collars", Celestine's Ch3 rhyme, Ch7's peach smell. Consequence: Ogerpon with Juno (Festival), Pecharunt (Ch18).
Also: the first explicit "nobody" (`:ch10_succession_stance`). **No jokes** inside the Grove from the Veil to the Plate (the comedy scene is "The Royal We" in the Chase, after J3). **No side content** opens in Verdance between the testament (V131 == 4) and the Plate (V131 == 8): the Rootward and Chase boards wait.

---

# CHAPTER 10 — "The Seat That Blooms"

**Chapter start:** V101 = 3, V102 = 10, V131 = 0 (Interlude II's end). The PC wakes in the Ironreach Pokémon Center.

## Act III opener: every Pokémon Center door (from V101 >= 3)
```
(The Center's doors have a new frame round them: a brass arch with a scanner plate set into it, and a small screen.)
SE: a soft two-note chime as you walk through.
SCREEN: ◆ FELLOWSHIP PRIORITY GUEST ◆ Welcome back, \PN. Meridian is glad you're safe.
[if :pro_fellowship != :accept] SCREEN: ◆ PRIORITY GUEST ◆ Welcome back, \PN. Meridian is glad you're safe.
[name: Nurse] (the first time) They put them in every Center last week. Under the Mandate. It's very polite. It says hello to everyone by name. It says hello to me by name. I've never told it my name.
```
*(06_ACT_III's act-opening state: even being watched is courteous. The screen changes in Ch12, V133 >= 7: "SUSPENDED".)*

## Map 261 — the Ironreach Pokémon Center: **"Morning"** (autorun on waking, V131 == 0)
```
(Morning. The Center is quiet. On the bench by the door, a small girl with chalk to the elbows is waiting with her knees pulled up.)
[name: Nell] You're awake. Mum said not to wake you. I didn't. I just waited very loudly.
[name: Nell] The lady with the flowers. Juno. She went up with the Sovereign's people in the night. In the Sovereign's own cage. She didn't want to go and she didn't want to stay.
[name: Nell] She left you this.
(A folded page, green ink, the handwriting going downhill at the end of every line.)
"\PN — They're taking me to Verdance. The Sovereign says I have to be there when they open his letter. I don't know what letter. I don't know anything any more. Come the long way if you want. I'd understand. I'd come the long way. — J."
[name: Nell] (holding up her chalk) She saved me. The roots came up and she had her arms round me and I couldn't see anything but flowers. Tell her I've got the neatest S in Ironreach and she can have it.
V131 stays 0 until the Lift Road branch on 680 (0 → 1). QUEST LOG: "Eighteen Roads" — Go to Verdance. Up the Root Road: the Tailings, the Rootdeep's Lift Road, then the Crown Road west.
```

## Map 692 — The Tailings (`:SCRAPYARD`)
```
ROAD SIGN: THE TAILINGS — Nadir. ← Ironreach · → the Rootdeep & the Lift Road. Mind the cones. They move.
(Grey cones of mine-waste outside Ironreach. Kids sledge down them on shovels. A Directorate checkpoint has been put up at the bottom of the biggest cone, which the kids treat as a ramp.)
[name: Sledging Boy] They put a barrier at the bottom! It's the best jump in Nadir now!
[name: Directorate Officer] It is NOT a jump. ...It's quite a good jump.
NOTICE (on the barrier): "BY MANDATE OF THE ACCORD (CONCLAVE OF AF 300): THE DIRECTORATE OPERATES IN ALL LATTICE TERRITORIES." Under it, chalked: "NOT OURS. — the Hollow". Under that, a hammer, scrubbed half out.
```
*Trials off 692: Grudgestone Quarry (684/685) by the waste cones; the Hollow Sanctuary branch below starts there. Echo Coliseum (688) is off the Tailings' east end.*

## Map 688 — Echo Coliseum (optional; `:BLEED`)
```
FIELD NOTES pop-up: "ECHO COLISEUM — BLEED. An old pit, out past the Tailings. The Fist Plate's burst came down the seams to it and it hasn't stopped ringing. It plays back. (Larch, in the margin, older ink: 'It isn't a recording. Don't argue with it.')"
(An empty fighting pit, rimmed with glass. In the Bleed light, nothing moves. But the air is full of sound: a crowd, very far away, breathing in.)
ECHO (centre of the pit; action):
  (A man's voice, doubled through something in a mask:) "Not now — you don't understand — get back."
  (A crack like a branch breaking.)
  (A girl's voice:) "...Uncle Rowan?"
  (Then it starts again, from the crowd breathing in.)
(At the pit's edge, a glass-flecked Timburr is sitting with its log across its knees, listening, the way a dog listens at a door.)
WILD BATTLE (once): TIMBURR, Bleed-touched, Lv 42 (catchable; the field is Bleed).
```
*(06_ACT_III's Echo Coliseum. Fighting-type: Gym 8 is behind the player, so it's no counter to the next Warden (SPINE Rev 16). The distribution owner may change the species.)*

## Map 680 — The Rootdeep (borderland F, `:CAVE`) and **the Rootdeep Lift Road**
```
ROAD SIGN: THE ROOTDEEP — where Elowen's roots come through Nadir's roof. ← the Tailings · ↑ the Lift (to Lanternroot & the Crown Road).
(Mine shafts that turn, as you go, into a cathedral of roots: the Gossamer Wood's roots, as thick as towers, coming down through the rock overhead. Ore carts overgrown with moss. Fungus lamps.)
(At the far end, the great freight-lift: a cage the size of a house on four chains, hauling ore up the cliff to Elowen's downs.)
[name: Lift-hand] Up's free today. Up's been free all week. Everybody wants to go up. Nobody wants to come down.
```
### The Lift Road branch (autorun at the lift's foot, V131 == 0 → 1; one of three, by Standing, in this order)
**A. [if `standing(:MERIDIAN) >= 4`] "A Fellowship Privilege" → Map 699, the Meridian Black Site** (S172 BLACK_SITE_OPEN)
```
(A neat young woman in a charcoal suit is waiting by the lift with a clipboard and an umbrella she doesn't need underground.)
[portrait: CALLA, neutral] \PN. Calla Wren, from the Chairman's office. We met at the Landing. You won't remember. Nobody remembers the person holding the scanner.
[name: Calla] The Chairman asked me to offer you a tour. One of our research stations is just off the Lift Road. It's a Fellowship privilege. Very few people see it.
[portrait: CALLA, neutral] *(a pause that's slightly too long)* You can say no.
> Go with her.
  (Through a maintenance door in the root-wall. Behind it, a steel corridor, white light, and a smell of disinfectant.)
> Not today.
  [portrait: CALLA, neutral] Of course. *(She writes something down. She seems relieved.)*
  → the refugee scene (C) plays on the way up instead.
```
```
(699. A white room with a glass cradle in the middle, and in the cradle a Pokémon in a heavy iron helmet, bolted shut, its body like something made of three different animals by people who'd never met. Wires run from the cradle to a console. Behind the console, a giggling man in a white coat.)
[portrait: QUENT, smug] Oh, it's YOU. The null reading! I've still only got one probe, you know. You broke the other one at the caldera.
[name: Quent] This is Project NULL. Well. The first one. It's a Type: Null. Look at the helmet. That's to keep its strength in.
[portrait: QUENT, happy] And look what it does when you come in.
(In your bag, the badge case hums. Eight notes, low. The Type: Null's helmet turns toward the sound, slowly, and stays there.)
[portrait: QUENT, smug] Just like that. Every time. It's modelled on something, you see. We're not allowed to say what.
[portrait: CALLA, sad] *(very quietly, by the door)* Doctor.
[portrait: QUENT, happy] Not allowed! I said not allowed. Calla, I'm a model of discretion.
[name: Quent] The Chairman says it's yours, if you like. Not today: it can't leave the site uncalibrated before the Festival. But it's yours. It likes you. Or it likes something about you. It's very hard to tell with the helmet.
```
**CHOICE `:ch10_null`**
```
> Accept it. (take)
  Script: pf_choose(:ch10_null, :take)
  (Calla presses a small brass key into your hand, the cradle's.) (Received: NULL CRADLE KEY.) Switch S180 TYPE_NULL_GIFT = ON.
  (When you touch the cradle's glass, the badge case goes quiet. The Type: Null doesn't.)
  [portrait: QUENT, happy] After the Festival, then. Do come back. We'd love the detail.
> Leave it. (leave)
  Script: pf_choose(:ch10_null, :leave)
  [portrait: QUENT, sad] Oh. Well. It'll be here. It's always here.
  (As you go, the helmet turns to follow you, all the way to the door.)
[portrait: CALLA, neutral] *(at the lift, alone)* I'm sorry. It isn't a zoo. I don't know what it is.
V131 = 1.
```
*(09 #14: the Type: Null reacts the way the badge case does. Gated by NARRATIVE_KEYS §4.1; takes priority over B. Voss +2 on `:take`. **No legendary joins the party in the main story** (Reuben's rule, 2026-11-23): S180 now means "promised", and the NULL CRADLE KEY opens the postgame `PG_TYPENULL` chain (Project NULL, Unmasked).)*

**B. [else, if `standing(:HOLLOW) >= 4`] "The Leaderless" → Grudgestone Quarry 684/685 → Map 698, the Hollow Sanctuary** (S171 HOLLOW_SANCTUARY_OPEN)
```
(A boy in a grey cowl too big for him steps out from behind an ore cart. He has an Alolan Grimer in his arms and a bark mask pushed up on his head.)
[name: Hollow Runner] You're the one who walks in. Brother Wick wants you. Not for anything bad. He said to say "not for anything bad" twice. Not for anything bad.
(He leads you back down to the Tailings and into Grudgestone Quarry by a gap in the fence. At the bottom of the quarry's second level, behind a curtain of hanging roots: a cave full of lamps and people. The Hollow, leaderless. Bedrolls. A kettle. Children.)
[portrait: WICK, sad] Sit, child. You've seen the Gazette. Everyone has. He's in their cells, and they've written "terrorist" next to his name in letters a yard high.
[name: Wick] He was pulling her wires out. I know. You know. The roots know. The Gazette doesn't print roots.
[portrait: WICK, neutral] I was going to give you this at the end. There isn't going to be an end the way I thought, so you're having it now.
(He takes a fold of old paper out of his sleeve, soft as cloth.)
[portrait: WICK, neutral] The Hymn the Choir sings at every Festival is half a hymn. I was defrocked for reading the other half. This is the verse I could still remember after they took the book.
(Received: HYMN FRAGMENT.) ITEM DESCRIPTION: "...then one of no colour, the eighteen roads walked, / shall carry them home, as the old ones talked — / not chained, not broken, not bought, not crowned: / given back, as a gift is ________. (The last word is torn away.)"
[portrait: WICK, sad] I never found the last word. I used to think it was "kept". It isn't. It doesn't even rhyme. Kept things don't go home.
[name: Wick] And this. For whoever holds him. They'll read it before he does. That's all right. It's for them, too.
(Received: WICK'S LETTER.) ITEM DESCRIPTION: "Sealed with candle-wax. 'To the keepers of Rowan Ashby. Be kind to him; he's been kind to everything else.'"
[name: Hollow Woman] (at the kettle, a Lowmarsh weaver's shears on her belt) They took Mara at Lumen. Thistle. She'd want somebody to say thank you for the Ward, in Mirefen. So. Thank you.
V131 = 1.
```
*(06_ACT_III's Hollow branch: Wick's verse early. **Fixed:** the outline had Thistle hand over the letter here, but she was captured at Lumen (Ch5, `24_SCRIPT_CH5.md`); the letter is Wick's, and her people speak for her. WICK'S LETTER is delivered to Rowan's gaoler in Ch13. The verse completes in Ch18.)*

**C. [else] "Up"** (the refugees; also plays for A's "Not today")
```
(The lift-cage comes down empty and goes up full. A family with a cart of furniture lashed down with rope. An old man carrying a birdcage with a Pidove in it. A woman with a baby and a pit-fighter's championship belt over her shoulder, because it's the most valuable thing she owns.)
[name: Refugee Woman] They put the scanners on the cage-foot the morning after the Conclave. Hand on the plate, every time. They said it's for our safety.
[name: Refugee Woman] My husband's tint came up "Hollow-adjacent". He's never been Hollow anything. He sells noodles.
[name: Old Man with a Pidove] Sixty years in Nadir. Never been up. Is it true the sky's blue? My granddaughter says it's blue. I think she's having me on.
V131 = 1.
```

### The Lift's top station: **"The Envelope"** (touch on arrival at the top, V131 == 1 → 2)
```
(The top of the cliff. Elowen's downs, wide and green and windy after the Rootdeep, and a stone station-house where the ore is weighed.)
(On the station's bench, a boy in a black coat a size too big. He has an envelope in his hands: thick paper, a gold sunburst pressed into the wax. He's turning it over and over.)
(He sees you. He puts it inside his coat.)
[portrait: KESTREL, neutral] Don't.
[name: Kestrel] It's post. People get post.
[portrait: KESTREL, angry] I said don't.
MOVE: Kestrel gets up and walks away east along the edge of the downs, toward the Crown Road, the long way round to Zenith.
V131 = 2.
```
*(The envelope is Voss's: "the full AF 290 file" (K5, Ch12). The PC isn't told. Kestrel's coat pocket has a gold corner showing in his sprite until Ch12, if the art allows.)*

## Map 690 — Lanternroot (border F's town)
```
(A town of mushroom farms on terraces at the Lift's top, lit by lamp-moss. Ore comes up, ale and lamp-moss go down.)
[name: Fungus-grower] We grow on the roots. The miners dig past the roots. Every year we argue about it. Every year the roots win, because the roots don't come to the meeting.
[name: Miner's Wife] There's a root in the low field that bleeds when you cut it. Red. Real blood, near as anyone can tell. Nobody's cut it in thirty years. Somebody cut it last week.
```
*(The Rootdeep's secret, "The Root That Bleeds", is a local sidequest hook (WORLD.md, border F); the Trials owner may wire it.)*

## Map 681 — Prism Falls (`:RAINBOW`)
```
ROAD SIGN: PRISM FALLS — Elowen. ← the Crown Road · → the Briarway & Verdance. The rainbow is the Imprint. Do not try to stand at the end of it. People try.
(A waterfall coming off the Crownland edge into a gorge, and across the gorge, all day, every day, a rainbow so solid it casts a shadow. The Rainbow Stair climbs beside the falls.)
[name: Painter] Twenty years I've painted it. It's never the same rainbow twice. It's always the same colours.
[name: Pilgrim] They say Verdance is drowning in flowers. Roses through the cobbles. People wear masks for the pollen. You'd think, a city so sick it's blooming. You'd think that'd be the nice kind of sick.
```

## Map 693 — The Briarway (`:FAIRY_TALE`)
```
ROAD SIGN: THE BRIARWAY — the Queen's road. ↓ Prism Falls · ↑ the Kingsgate & Verdance. Do not trim the briar. The briar belongs to Her Majesty.
(The royal road, hedged on both sides with briar clipped flat as walls by gardeners for three hundred years. But the briar's out of hand now: shoots as thick as a wrist across the road, roses the size of plates, the clippers' ladders abandoned in the verge.)
[name: Royal Gardener] I clipped this hedge for forty years. Since the Warden went, it grows a yard in a night. I clip it at dusk, and at dawn the yard's back and it's brought a friend.
[name: Thornguard] (at a royal milestone, in thorn-green armour) The Heartgarden's under the Queen's protection, traveller. Pending the succession. You'll want a pollen mask.
```
*The gardeners' door in the hedge (WORLD.md's secret) opens onto the Royal Chase's back fence after S126.*

## Verdance (280–289, 294–296; Elowen's royal seat)

### Map 284 — the Kingsgate Barbican: arrival (autorun, V131 == 2 → 3)
```
(The Kingsgate: a barbican of old white stone, and through it, terraces climbing a hill to a castle of briar and white towers at the top. Verdance.)
(Verdance is drowning in flowers.)
(Roses through the cobbles. Vines pulling the gutters off the roofs. Lilies growing out of a horse trough. Window-boxes so heavy they've torn off and hang from their own stems. The air is gold with pollen, so thick it drifts like snow in the lamplight. It's beautiful. It's horrifying. People walk through it with cloth masks over their mouths and don't look up.)
[name: Gate Clerk] (handing you a cloth mask without being asked) Pollen. Wear it. It's not poison. It just won't stop.
[name: Gate Clerk] Since the Warden went, the Meadow Plate's had nobody to hold it in. It's... spilling. Three days, the whole city. The bakers can't keep the bread from sprouting.
(At the barbican's foot, a woman is kneeling, scraping at the bloom on the cobbles with a trowel. Under the flowers, the soil is grey. Dry. She lifts a dead leaf out of it. It isn't rotten. It isn't anything. It's exactly as it fell.)
[name: Woman with a Trowel] Nothing rots in Verdance. My nan used to say it like it was a blessing.
Switch S165 THORNGUARD_HEARTGARDEN = ON. V106 VERDANCE_BLOOM = 1. V131 = 3.
QUEST LOG: "Eighteen Roads" — The Sovereign is in the Heartgarden. Go up through the Market Terraces.
```
*(06_ACT_III: under the bloom, the soil is grey; nothing rots. 09 #2's old clue, "Ask why nothing in Verdance ever rots", lands here without anyone saying it.)*

### Map 280 — the Market Terraces · 281 PC · 282 Mart
```
[name: Florist] I'm the only florist in Velmora going out of business because of flowers.
[name: Rootward Boy] Mum says the old Warden was a bad man. Gran says he watered our street's trees every year for nothing. Mum says that's what bad men do, to make you like them. Gran says Mum's never watered anything.
[name: Thornguard] (at the Heartgarden stair) The Heartgarden's closed by order of Her Majesty, Queen Maelis Thorne, pending the succession. — Oh. You're expected. Go up.
281 WARDEN CIRCULAR (the Gale Post relay board by the counter; the first one the PC can read; see below).
```
**The Wardens' Circular** (15_COMEDY §2C; read at any Pokémon Center from Ch10; this is post one)
```
WARDEN CIRCULAR — GALE POST RELAY, WARDENS ONLY (somebody has left it on the public board)
ODESSA: relay test. is this thing on. who's still talking to who after ironreach
DORIAN: *Enter, stage left, seventeen Wardens, not looking at each other.*
ILSA: Corvin, stop composing that. We can all feel you composing it.
CORVIN: I wasn't going to send it.
CORVIN: I've sent it.
CORVIN: Disregard.
BASTIAN: Re: Saltmere harvest supper invitation (AF 299). Yes please.
ANJA: Toes.
```
*(The Circular grows by one or two posts per chapter. It never mentions Rowan by name.)*

### Map 294 — the Heartgarden: **"Three Claimants"** → the testament (autorun at the head of the Heartgarden stair, V131 == 3 → 4)
```
(The Heartgarden: Verdance's walled garden on the hill's shoulder, under the castle. Five days ago it was ordinary-beautiful. Now it is a jungle of blossom, roses as tall as men, and in the centre, at the head of a stone stair going down into a sunken grove, the Bride Tree: a tree in the shape of a woman, arms raised, head back, in blossom from root to crown.)
(The sunken grove at the stair's foot is gone under bloom so thick it's black. Across the stairhead, a shimmer like heat over a road. A Veil.)
(On the steps of the Heartgarden's little chapel, a scene like a painting: in white, the Sovereign, with a sealed envelope. On his left, the Thornguard in a line, and at their head an ancient woman in a gown of thorn-green and a crown of briar, leaning on a cane topped with a silver rose. On his right, a smiling man in Elowen's colours, and beside him a woman in a Meridian sunburst pin. And in front of them all, on the bottom step, alone, Juno, in her wreath and veil, with her gardening gloves twisted in her hands.)
[portrait: MAELIS, neutral] The Meadow Plate lies on Crown soil, Sovereign. It has done since my great-great-grandmother planted this garden. A Warden kept it for the Crown. There is no Warden. So the Crown will keep it.
[name: Meridian Delegate] With respect, Majesty, the Plate is overflowing. Meridian can offer temporary custody, for public safety. Our dampers held the Quiet Ward through worse. We'd ask nothing but the right to keep the city breathing.
[name: Prince Caedmon] Mother, it's a very generous offer. *(smiling at everyone, including the Plate)*
[portrait: MAELIS, deadpan] Caedmon, you've called everything Meridian offers generous since you were twelve. It's how I know what you're for.
[portrait: VALEN, neutral] A Warden's testament is law under the Concordance, Majesty. Older than either of us. Rowan Ashby left one. I'll read it now, in front of everyone, because nobody here trusts anybody to read it privately.
(He breaks the seal. Inside, a folded letter and a small ring, a plain band with a chip of stone in it, no colour at all. He reads aloud.)
```
```
[portrait: VALEN, neutral] "To the Sovereign of the Accord, from the Warden of Verdance. To be opened if."
[name: Valen] "If you are reading this, I didn't come back from Ironreach, or I came back in irons. Either way, the garden needs a gardener."
[name: Valen] "I name as my heir to the seat of Verdance and the keeping of the Meadow Plate my niece, Juno Hale."
(The garden goes very quiet. Even the bees.)
[name: Valen] "She has been talking to plants since she could talk, and they have been listening. She'll say she isn't ready. She is. She doesn't know it."
[name: Valen] "Rowan Ashby, Warden of Verdance, twenty-fourth year."
[portrait: VALEN, sad] There's a postscript.
[name: Valen] "Water Elin at dawn. She likes it before the bees are up."
(Juno makes a sound like someone stepping on a stair that isn't there.)
[portrait: JUNO, crying] ...
(Valen comes down the steps and holds out the ring. Juno doesn't take it. He takes her hand, opens it, puts the ring in her palm and closes her fingers over it.)
[portrait: VALEN, neutral] His ring. A Warden's ring, cut by the Hearthguild. It'll answer you, or it won't. Mine took a year.
[portrait: JUNO, sad] I didn't want this seat. I wanted HIM in it.
[portrait: VALEN, sad] I know.
[name: Valen] A Warden is confirmed when the Plate accepts them, Juno. The Plate is at the bottom of that stair, in the Bride Tree's roots, under that.
(He looks at the Veil across the stairhead. Then he looks at you, the way he did at Ironreach.)
[portrait: VALEN, neutral] And only one person in Verdance can walk through that.
V131 = 4.
```
**Tamsin and the Greenward** (straight on; MOVE: Tamsin comes up the garden path from the gate at a run, out of breath, with a moth-wing shawl and a satchel of thread)
```
[portrait: TAMSIN, panic] Sorry — sorry — the Briarwick coach lost a wheel in the briar — sorry. Am I late? I'm late.
[portrait: TAMSIN, neutral] Juno. Briarwick stands with Verdance. Whoever sits it. That's all. I came to say it in front of people.
[name: Tamsin] A thread holds because it's twisted with others. Alone it's just string.
[portrait: JUNO, sad] *(barely)* ...Thank you.
[name: Press Clerk] (at the garden wall, scribbling) "Small-town Warden backs the niece." Is it a bloc? Are you a bloc? Can I call it the Green Ward?
[portrait: TAMSIN, panic] I— it's not a— we're not—
[name: Press Clerk] "The Greenward." Lovely. That'll sell.
```
**[if `:ch2_tamsin == :keep_secret`] "You Knew"** (three people in Lowmarsh weavers' aprons push to the front of the crowd)
```
[name: Lowmarsh Weaver] Briarwick stands with Verdance? Briarwick signed with MERIDIAN. She signed alone. The Glasswood's at our looms because she signed.
[name: Lowmarsh Weaver] They took Mara at Lumen. She'd be stood here saying it. So we're saying it. You KNEW, Warden.
[portrait: TAMSIN, sad] ...
> Step between them.
  [portrait: TAMSIN, neutral] No. No, don't. *(She puts a hand on your arm and steps out past you.)*
> Let Tamsin answer.
  (You step back.)
[portrait: TAMSIN, sad] Yes. I knew. I signed it alone, in the spring, and I've been sorry every day, and being sorry hasn't moved the glass an inch.
[name: Tamsin] I'm not here because I'm good. I'm here because she is. Stand with her too. Then shout at me after. I'll be at the Briarwick coach. It's got three wheels.
(The weavers look at each other. One of them nods, once. They step back into the crowd.)
```
*(06_ACT_III: "Thistle's cell appears to heckle Tamsin." **Fixed:** Thistle is in custody since Ch5, so it's her people. No new key: Tamsin's Consent still reads `:ch2_tamsin`.)*

### Map 294 — **"She's Listening"** (the Bride Tree, with Juno; V131 == 4 → 5)
```
(Later. The crowd has gone down the hill. The Thornguard stand at the gate. Juno is sitting at the foot of the Bride Tree, on the roots, in the blossom, with the ring in her fist.)
[portrait: JUNO, neutral] You've heard about her. Everyone has. This is her.
[name: Juno] Aunt Elin. AF 288. She was weeding the Heartgarden and the Bleed came up through the roots like a spring, and she stood up, and she put her arms up, like this, and that's how she stayed.
[portrait: JUNO, sad] I was three. They told me she'd gone away. I believed them till I was eight, and then he walked me up here at dawn and showed me, and held my hand, and watered her.
[name: Juno] Every dawn. Twelve years. He never missed one. Not even for Ironreach. He must have gone the morning he left.
[portrait: JUNO, sad] Sometimes I think she's listening. Isn't that stupid?
[if switch(182)]   # S182 CAMEO_VENAM_DONE: the PC carries VENAM'S TESTIMONY
  > Play her Venam's Testimony.
    (The little recording crackles. A girl's voice, loud, a bit rough, Mirefen-sewer-echoey.)
    [name: Venam (recording)] I was stone for— I don't know how long. And I could hear everything. Everyone who sat with me. Every stupid joke. I could hear all of it.
    (Juno is very still.)
    [portrait: JUNO, crying] ...Everything?
    (She turns round on the roots and puts both hands flat on the bark.)
    [portrait: JUNO, crying] Aunt Elin. It's Juno. I'm fifteen. I've got a satchel of seeds and a friend who walks into things.
    [name: Juno] Uncle Rowan's in prison. He did something terrible and something brave on the same day and I don't know which one he is.
    [portrait: JUNO, sad] They want me to have your garden. I'm so frightened.
    (She talks to the tree for a long time. You sit with her. Petals come down on both of you. They don't fall, Elin's petals. They're falling now.)
  > Not now.
[else]
  > It isn't stupid.
    [portrait: JUNO, sad] Dr Mott said they dream. In the Ward. He said he'd never said it out loud before. He said it to you.
    [portrait: JUNO, neutral] So maybe she's dreaming. Maybe it's a nice one. I hope I'm in it, a bit.
  > ...
    [portrait: JUNO, sad] Yes. That's what I think too, mostly.
[portrait: JUNO, neutral] *(standing up, wiping her face with a gardening glove, which makes it worse)* Right. Right. Down the stairs. Into the horrible black flowers. You first, please. I'll be right behind you.
[portrait: JUNO, sad] I'll be RIGHT behind you.
V131 = 5.
```
*(09 #21. Venam's Testimony is the strong version; Corvin's line carries the idea without it. The falling petals echo Interlude II and nobody remarks on them.)*

## Map 708 — The Bride Grove: **Juno's trial** — key events 1 and 2
*(The sunken grove under the Bride Tree, reached by the stair from 294. `:BLEED` until the Plate accepts Juno, then `:FLOWER_GARDEN` stage 1.)*
### The Veil (touch at the stairhead, V131 == 5 → 6)
```
Script: Prismfall.checkpoint     # NARRATIVE_KEYS §10: GO_LOYAL's checkpoint, the Bride Grove gate
(You walk into the Veil. On the other side, the grove: blossom so thick it's black, petals in drifts to the knee, vines like cables, and the light grey and wrong from every direction.)
FIELD NOTES pop-up: "THE BRIDE GROVE — BLEED. A garden with nobody holding it. It grows into the space where a person should be. (Larch, in the margin: 'So does grief. Write that down somewhere else.')"
(Behind you, at the stairhead, Juno puts her hand to the shimmer and snatches it back.)
[portrait: JUNO, shocked] It burns. It — of course it burns. Sorry. I knew it would. I just hoped I'd be special.
[portrait: JUNO, neutral] Go on. Find the way. I'll come when it's quiet. Uncle Rowan says the garden always goes quiet for somebody who knows where they're going.
V131 = 6.
```
### The path (DUNGEON_PUZZLES: a "safe path" puzzle; the puzzle engineer owns the layout)
*Intent: the bloom parts round the PC as they walk, and where they've walked, the petals lie flat and pale and the Veil thins to nothing: a corridor of quiet. It closes again behind them after a set number of steps unless it reaches a **root-node** (six of them, glowing faintly in the bloom), which pins it open. The PC has to walk a route from the stair to the Plate through all the root-nodes needed, then go back to the stair for Juno, who follows the quiet corridor step for step as a follower event. Bleed-maddened Grass Pokémon (Bramblin, Shiinotic, Bellossom) calm near the PC and wander off; a few that don't are wild battles. Verify a unique shortest route with the puzzle BFS.*
```
ROOT-NODE (each, on reaching it): The root under your feet is warm. The bloom round it lies down, the way grass lies down for wind. It stays down.
(Halfway down, on the third node, the bloom ahead is torn, trampled, broken in a wide circle round the Bride Tree's deepest roots. In the middle of the circle, something is standing in the dark.)
```
### **"The Ogre"** (the root-hollow under the Bride Tree; touch, once)
```
(A Pokémon, small and fierce, in a mask carved out of bark: a face with a scowl and two horns. It has a club made of a branch. It stands between you and the roots, where a warm green light pulses under the soil. The Meadow Plate.)
(Round it, the bloom is broken in a ring. Nothing grows inside the ring. It's been standing here so long it's worn a circle.)
(It sees you, and it roars.)
SE: Ogerpon's cry.
(It doesn't charge. It plants the club and stays exactly where it is.)
FIELD NOTES pop-up: "The Ogre in the Mask. I've seen that mask. On every Hollow cowl in Nadir. On the shrine at Briarwick. It's been here the whole time. It's been guarding her."
(You come no closer. After a long time, it lowers the club an inch.)
```
*(09 #20: Ogerpon has guarded the Bride Tree since AF 288, which is why nothing got close enough to harm Elin.)*
### Juno comes down (the PC returns to the stairhead and leads her; V131 stays 6)
```
(At the stairhead, the quiet corridor runs all the way down, pale and flat. Juno looks at it.)
[portrait: JUNO, neutral] Oh. Oh, it's a path. You made a path.
(She steps onto it, and the Veil doesn't burn her. She lets out a breath she's been holding since Ironreach.)
[name: Juno] Step where you step. Right. Right. I can do that. I've done that my whole life, a bit.
MOVE: Juno follows the PC down the corridor, step for step.
(At the root-hollow the Ogre sees Juno, and something in it changes. It lowers the club all the way. It takes one step toward her, and stops.)
[portrait: JUNO, shocked] ...It knows me. How does it know me?
[portrait: JUNO, sad] I used to leave biscuits by the stair when I was little. For the fairies. They were always gone in the morning. Uncle Rowan said it was the badgers.
```
### **The Loyal Three** → **CHOICE `:ch10_ogre`** (key event 2)
```
(A sweet smell comes down the grove. Peaches. Peaches and something under the peaches.)
(Out of the bloom on the far side of the hollow step three Pokémon. A great hulking dog with a chain round its middle. A monkey with a sly painted face. A pheasant with a fan of tail feathers like a court lady's. Every one of them wears a collar that glows pink, Sweetrot pink, and their eyes are the same blissful blank as the vendors in the Sweet Market.)
(They don't attack. They kneel. All three, in a row, heads bowed, in front of Juno. Exactly the way the painted actors knelt in the pageant at Saltmere: the dog, the monkey and the bird, the loyal companions of the old story, who killed the wicked Ogre and saved the people's treasure.)
[portrait: JUNO, shocked] It's them. It's the Loyal Three. From the shrine. From the pageant—
[portrait: JUNO, happy] They're the heroes! They've come to help!
(The Ogre roars. Not at the Three. At you, and at Juno, and at the Plate between them, a terrible, pleading sound, and it brings its club down on the roots so hard the whole grove shakes.)
(The Three raise their heads. In the pink light, the dog's chain clinks. The monkey's eyes slide past Juno to the green light under the soil.)
[portrait: JUNO, panic] \PN— which— who do we—
```
```
> Stand with the Ogre. (ogre)
  Script: pf_choose(:ch10_ogre, :ogre)
  (You step across the hollow and stand beside it, between the Plate and the Three.)
  (The Ogre looks up at you through its mask. Then it turns to face the Three, shoulder to your knee.)
  (The Three stand up. The kneeling is over. Their collars blaze.)
> Stand with the Three.
  > ...They're the heroes of the story. Stand with them?
    > Stand with them.
      (You step aside. The Three rise. The dog walks past you to the roots, almost gently, and puts its paw on the green light.)
      (The pink spreads out of its collar into the soil like ink into water. Down into the roots. Up into the Bride Tree. Somewhere above you, very faintly, every blossom on the tree turns the colour of a peach.)
      (Juno screams. The Ogre, alone, throws itself at three, and goes down under them.)
      Script: Prismfall.game_over(:GO_LOYAL)
    > No.
> Hesitate. (hesitate)
  Script: pf_choose(:ch10_ogre, :hesitate)
  (You don't move. You can't tell. The Ogre looks at you, once, and then it turns its back on you and faces the Three alone.)
```
*(GO_LOYAL epitaph: NARRATIVE_KEYS §9. Foreshadowing: the Ch2 pageant and the Mourner's line about the collars, Celestine's Ch3 rhyme, Ch7's peach smell.)*
```
(The Three come for the Plate.)
[if :ch10_ogre == :ogre]
  BATTLE (boss sequence): Prismfall::Bosses, `:LOYAL_THREE` [NEW] — three battles in a row, each a multi-bar boss: Okidogi, then Munkidori, then Fezandipiti. A partner battle: PC + the Ogre (`PARTNER_OGRE` [NEW]: Ogerpon, Teal Mask, Lv 48, one Pokémon, AI-controlled). Field: Bleed.
[if :ch10_ogre == :hesitate]
  BATTLE (boss sequence): the same `:LOYAL_THREE`, the PC alone. Standard: the same bars as the partner fight; Hard: each boss +1 bar and a second Pokémon at its side. The party is healed between bosses (the Ogre drops a fistful of grove berries at your feet each time, without looking at you). The Ogre fights the other two in the background between battles (cutscene beats). *(Losing Ogerpon as a partner is the penalty; the fight stays hard, not tedious: Gemini review 2026-11-21.)*
(Between battles, if the Ogre is your partner:) (It looks back at you each time, to check you're still there.)
(At the third boss's last bar:) (Fezandipiti spreads its tail, and the peach smell comes off it so thick you can taste it. For a second you'd agree with anyone about anything. Then the Ogre's club comes down, and the smell breaks.)
(LOSE: whiteout to the Verdance Pokémon Center; the trial restarts at the stairhead, with the path still open.)
(WIN:)
(The three collars crack. All at once. The pink goes out of them like a lamp blown out.)
(The Three stand blinking in the bloom. The blank is gone out of their eyes, and what's in them instead is worse: confusion, and fear, and something that might be shame. Then they turn and run, the dog and the monkey and the bird, back up through the bloom and out of the grove, and nobody follows them.)
Switch S127 CH10_LOYAL_THREE_DONE = ON. V131 = 7.
```
*(The Three are thralls of something in the Lightless Deep (the Pecharunt seed, 09 #26); they're freed in Ch18. Their eyes match Corvin's Sweetrot addicts.)*
```
[if :ch10_ogre == :ogre]
  (The Ogre sits down hard in the petals, breathing like a bellows, and takes its mask off.)
  (Under it, a small, tired, ordinary face. It wipes its eyes with the back of a paw. It puts the mask back on.)
  (Then it walks to Juno, and stands beside her, and doesn't leave.)
  [portrait: JUNO, crying] You. You were down here the whole time. Every biscuit. Every single biscuit.
  [portrait: JUNO, sad] You kept everything away from her. Twelve years. By yourself. Because nobody would believe you weren't the monster.
[if :ch10_ogre == :hesitate]
  (The Ogre stands in the broken bloom, bleeding sap from a dozen cuts. It looks at you a long time.)
  (Then it walks past you, past Juno, and up the stair, and out of the grove, and you don't see where it goes.)
  [portrait: JUNO, sad] It saved her. It saved her for twelve years, and we didn't know whose side to be on.
```
*(`:ogre` OGERPON_TRUSTED: Ogerpon stays with Juno, appears at the Festival; Core mirrors S223. `:hesitate`: it leaves, distrustful.)*

### **"The Plate Accepts Her"** (the root-hollow; key event 1, payoff; V131 == 7 → 8)
```
(The green light under the roots. Juno kneels in front of it and pulls the soil back with her gloved hands. The Meadow Plate is lying in the roots of the Bride Tree like an egg in a nest: a tablet of green stone, warm, humming, too bright to look at for long.)
[portrait: JUNO, sad] I don't know how. Nobody told me how. Is there a — do I say something?
> Just hold it.
  [portrait: JUNO, neutral] Just hold it. Right.
> Say what you'd say to a plant.
  [portrait: JUNO, happy] *(a wet laugh)* Hello, you. Aren't you lovely. ...That's all I've got. That's all I've ever said to a plant.
> ...
  [portrait: JUNO, neutral] Yes. Quiet's better. Plants like quiet.
(She takes off one glove. She lays her bare hand on the Plate.)
(For a moment, nothing.)
(Then the grove breathes out. All of it. Every vine and rose and petal-drift. The bloom lies down, the way grass lies down for wind, all the way up the stair and out across the Heartgarden and on down the hill. The Veil goes. The light goes from grey to gold. Up above, in the city, a sound comes down the terraces like a crowd sighing.)
(Juno's hair is full of pollen. Her hand is still on the Plate. She looks down at it as if it belongs to someone else, and then as if it doesn't.)
[portrait: JUNO, shocked] ...Oh.
[portrait: JUNO, crying] Oh, it's heavy. Nobody said it was heavy. It's so heavy. It's like holding the whole hill.
[portrait: JUNO, sad] He held this for twenty-four years. And watered her every morning. And came down here and talked to it. And I never once asked him if it hurt.
(On her finger, Rowan's ring. She put it on at some point; she doesn't remember when. It stays dull. No colour. It doesn't answer.)
Switch S125 CH10_JUNO_WARDEN = ON. V106 VERDANCE_BLOOM = 2. Switch S165 THORNGUARD_HEARTGARDEN = OFF. V131 = 8.
```
```
(At the head of the stair, the Sovereign. Tamsin beside him with both hands over her mouth.)
[portrait: VALEN, neutral] Warden Hale.
(Juno looks up at him. She doesn't get up. She can't, quite, yet.)
[portrait: VALEN, neutral] *(to you, quietly, while Tamsin goes down to her)* Remember how she looked, just now, when it took her.
[name: Valen] Every seat looks like that from the inside. It takes the person who sits in it a little at a time, and it gives back a city. Most days it's a fair trade.
[portrait: VALEN, sad] I asked you to come and see what it costs. Now you've seen.
(He doesn't say why he wanted you to see. He pulls his glove tighter, though it's warm, and goes up into the garden.)
```
*(09 #16: Valen's plan for the PC; "a seat to fill" pays here as a lesson, and he doesn't say whose seat. #4: the glove.)*
**After S125: the Bride Grove** is `:FLOWER_GARDEN` stage 1, quiet, with wild Grass Pokémon at Gym 9's level. If OGERPON_TRUSTED, the Ogre sits by the Plate whenever Juno is in the Heartgarden.

## Maps 290–293, 297 — the Heartgarden Gym (Gym 9; GYM_PUZZLES Gym 9)
*(The gym doors open at V131 >= 8. Juno opens it the next morning: "I've watered every bed in it. That was a mistake. You'll see.")*
```
JUNO'S SIGN (290): "Gardens are gossips. Water one and the neighbours hear about it. — J.H., Warden (it still feels weird to write that)."
[name: Gym Guide] The Heartgarden Gym. Grass-types on a Flower Garden that grows while you fight. Fire, Ice, Flying, Poison and Bug go straight through them. Be honest with yourself about Fire: you'll burn the garden down at full bloom, and that's a strategy.
[name: Gym Guide] Every hedge you leave in the beds, the Warden's garden starts one stage taller. Fewer waterings, harder fight. Your call. She told me to say "your call". She feels very strongly about it being your call.
[name: Apprentice Bram] (Juno's cousin, 291; hints) Water the plot NEXT to the one you want. / P6 is nearly overgrown already. Watering it collapses it, but it feeds P1 too. / (both solutions)
[name: Apprentice Bram] (292) She's my cousin. She used to make me be the bee in games. I'm still the bee.
```
### 293 — the Warden Arena: Juno (J3)
```
(A round lawn under a glass roof, with beds round the edge that are already starting to grow. Juno stands in the middle with pollen in her hair, the ring on her finger, a Tsareena at her shoulder and her gloves clipped to her sash.)
[if V345 >= 3]   # three or more hedges left (stage 4+)
  [portrait: JUNO, shocked] You let it grow? For me?
  [name: Juno] ...That's either kind or tactical and I'm too nervous to ask which.
[portrait: JUNO, sad] I didn't want this seat. I wanted him in it.
[portrait: JUNO, neutral] But the city's drowning in flowers and nobody else is coming, so.
[portrait: JUNO, happy] Hi. I'm the Warden of Verdance. Please don't go easy on me. I'll cry either way.
Script: setBattleRule("fieldStage", 1 + [$game_variables[345], 4].min)
Script: Prismfall.gym_battle(pfm_gym(:LEADER_JUNO), double: false)     # J3: LEADER_JUNO version 30 + starter slot; :FLOWER_GARDEN; cap 47; single
(At her second Pokémon:)
[if :ch7_ledger == :name_him] [portrait: JUNO, angry] You knew before me. You KNEW.
[else] [portrait: JUNO, angry] He lied to me. Every summer.
(When the garden reaches stage 4:) [portrait: JUNO, neutral] There. Look. That's what it does when somebody's holding it properly. It's not drowning. It's growing.
(When her ace, Tsareena, enters:) [portrait: JUNO, neutral] You were a seed in a tin when I met \PN. Look at you now. Queen of the garden.
(LOSE: whiteout. Juno on retry: "Again! Sorry. That came out bossy. I'm practising being in charge.")
(WIN:)
[portrait: JUNO, crying] I'm crying. I said I would.
[portrait: JUNO, happy] ...Take it. The Meadow badge is yours.
(Received: the MEADOW BADGE.)
(SE: nine notes. The case's light runs along its seams and doesn't fade at the end. It just stays, softly, like a pilot light.)
[portrait: JUNO, neutral] It's singing. Mine never sang. I wrote to Uncle Rowan after Briarwick, about your case doing a chord. He wrote back: "That one'll sing in every gym in the realm, Juno, mark me." I didn't know what he meant.
[portrait: JUNO, sad] I still don't.
(Received: TM53 ENERGY BALL.)
[portrait: JUNO, neutral] Energy Ball. It's the first move I ever taught anything. And that badge means Pokémon up to level fifty-one will listen to you. I checked. Twice. I'm very nervous about getting the numbers wrong.
V131 = 9.
```
*(J3 per 03_CAST and BALANCE §5. Field stage per GYM_PUZZLES 293 (V345 hedges). The badge name "Meadow Badge" is already in `LEADER_JUNO`'s LoseText; it's proposed as final.)*
*Trials after J3: "The Bride Tree's Heart" (EL_BRIDE_TREE_HEART: Juno under the tree with the Venusaurite; the ring won't answer), "What the Bride Tree Hears" (EL_EVER_BLOOM; S125). The Mastery 297 (the Bride Bower) opens after S346.*

## Map 294 — **"Little Gardener"** (Juno's first act; autorun on leaving the gym, V131 == 9 → 10)
```
(The Heartgarden, tamed: still full of flowers, but flowers that know where they're meant to be. On the chapel steps, the Queen with her Thornguard, the Prince, the Meridian delegate with a folder, and half of Verdance's press.)
[name: Meridian Delegate] Warden Hale. Congratulations. Meridian's offer stands: a Lattice for Verdance, to draw the excess from the Plate. Verdance would never drown again. Free light for every terrace.
(Juno looks at the folder. She looks at the delegate. She looks at the ring on her finger.)
[portrait: JUNO, neutral] No, thank you.
[name: Meridian Delegate] I'm sorry?
[portrait: JUNO, neutral] I've been to Mirefen, where the Lattice runoff makes the marsh glow. I've been to Lumen, where it cracked the Plate. I've been to Briarwick, where it fed the Glasswood. I'm fifteen and I've seen three.
[portrait: JUNO, angry] Verdance doesn't need a Lattice to stop it drowning. It needed a Warden. It's got one. No, thank you.
(The delegate closes the folder. Prince Caedmon smiles at her, and at the delegate, and at his mother, warmly, at all of them.)
[portrait: JUNO, neutral] And Majesty. Your Thornguard are standing in my garden.
[portrait: MAELIS, neutral] Our garden, child. The Heartgarden is on Crown soil.
[portrait: JUNO, neutral] Then your soil's in my garden. Please take your men off it. They're standing on the tulips.
(A very long pause. The whole Heartgarden waits.)
[portrait: MAELIS, smug] *(and the Queen laughs, a dry little sound like a seed-pod)* Thornguard. Off the tulips.
(The Thornguard file out of the gate.)
[portrait: MAELIS, neutral] Little gardener. We'll see how long you bloom.
MOVE: the Queen goes down the hill on her cane, very slowly, with her son at her elbow. She doesn't lean on him.
```
**CHOICE `:ch10_succession_stance`** (the press, on the Heartgarden steps; they've been waiting for you)
```
[name: Press Clerk] You! You're the one from Ironreach. The one who walked into the glass. You were in the grove with her.
[name: Press Clerk] Everyone's asking. The Queen says the Plates are the Crown's. Meridian says they're everybody's, under Meridian. The Accord says they're the Wardens'. Who should own the Plates?
> The Wardens. The Accord. (accord)
  Script: pf_choose(:ch10_succession_stance, :accord)
  [name: Press Clerk] "Null Witness Backs Sovereign." Good. Solid. Boring. Thank you.
> The kingdoms. The land they're in. (kingdoms)
  Script: pf_choose(:ch10_succession_stance, :kingdoms)
  [name: Press Clerk] "Null Witness: Give Them to the Crowns." Oh, the Queen'll like that. The Thane'll like that. The Dominar'll LOVE that.
> Nobody. (nobody)
  Script: pf_choose(:ch10_succession_stance, :nobody)
  [name: Press Clerk] ...Nobody?
  [name: Press Clerk] You mean... nobody should HAVE them? Then who keeps them?
  (You don't answer. The clerk writes for a long time.)
  [name: Press Clerk] "Nobody," says the null. Well. That's a headline. I don't know what it means. I don't think I'm supposed to.
  (At the back of the crowd, an old woman in a moth-silk shawl with flowers in her hair is smiling at you as if you've said something she's been waiting a long time to hear. When you look again, she's gone.)
V131 = 10.
```
*(The first explicit "nobody" (NARRATIVE_KEYS §4.2: HOLLOW+1 VALEN−1 RES+1); the Return path reads it. The old woman is Celestine in her Ch3 disguise, seen and not heard.)*
```
GAZETTE HEADLINES (Verdance PC board, after V131 >= 10): "JUNO HALE CONFIRMED: PLATE ACCEPTS 15-YEAR-OLD" · and by the stance: "NULL WITNESS BACKS SOVEREIGN" / "NULL WITNESS: GIVE THEM TO THE CROWNS" / "'NOBODY', SAYS THE NULL"
```

## Map 682 — the Royal Chase (Safari-style reserve): **"The Gates"** and the Queen's garden (V131 == 10 → 11)
```
(The next morning, a royal herald on the Market Terraces, reading from a scroll with a lot of ribbon on it.)
[name: Royal Herald] Her Majesty Queen Maelis Thorne, in these troubled times, of Her great love for Her people, throws open to them the Royal Chase, Her Majesty's own hunting reserve, for their recreation and the catching of game. God save the Queen.
[name: Florist] (beside you) That's for the papers. It's still a lovely park.
Switch S126 CH10_ROYAL_CHASE_OPEN = ON.
(The Chase: a walled reserve of meadow, copse and ornamental lake beyond Briar Hall. Safari rules: Chase Balls, a step count, no battles of your own.)
[name: Chase Warden] Thirty Chase Balls, five hundred steps. Don't feed the Scatterbug. Don't name the Scatterbug. They've all got names already. Every one. It's a whole thing.
```
**The Queen's garden** (a gate in the Chase's inner wall, the first time the PC passes it; touch, once)
```
(A small private garden in the Chase's heart: a sundial, a bench, an old woman alone on it with her crown off in her lap. No Thornguard. Nobody at all.)
[portrait: MAELIS, neutral] Sit, child. I don't bite. I used to. My teeth aren't what they were.
[name: Maelis] You stood in that grove with her. The null child. Everyone in Velmora's heard of you, and everyone wants you to say something for them. I find I don't. I find I'd like to say something to you.
[portrait: MAELIS, neutral] I've sat on the Thorn Throne sixty-one years. I've buried four Sovereigns. Did you know that? Wyndham, and the three before her. Every one of them died tired.
[name: Maelis] Every Sovereign since Maren has died tired. They come to the Festival young and strong, and ten years later they're old men at fifty, and nobody asks why, because the Accord says it's the weight of the office.
[portrait: MAELIS, smug] It's a very heavy office, apparently. Heavier than mine. I'm eighty-two and I can still climb my own stairs.
[portrait: MAELIS, neutral] So ask yourself, little colourless thing, why the Accord needs a new champion so badly this year. And why its Sovereign looks at you the way he did on my chapel steps.
[name: Maelis] Then come and tell me what you find out. I'll pay well. I always pay well. It's how I've outlived everyone who didn't.
V131 = 11.
```
*(09 #4 and #16: "Every Sovereign since Maren has died tired"; "why the Accord needs a new champion". The Queen is shrewd here, not comic.)*

### Map 682 — comedy scene Ch10, **"The Royal We"** (on leaving the Chase with at least one Scatterbug caught there; or at the end of EL_GERALD)
```
(At the Chase gate, the Queen again, crown back on, Thornguard back round her, and a man in a tabard holding an enormous ledger.)
[portrait: MAELIS, smug] We are told you caught a number of Our Scatterbug.
> A few.
  [portrait: MAELIS, deadpan] We counted them every spring for sixty years, child. "A few" is not a number.
> They were all the same.
  [portrait: MAELIS, shocked] All the—
  [name: Maelis] Each has a UNIQUE WING PATTERN. Keeper!
[name: Keeper of Small Creatures] (reading from the ledger) The challenger's party includes: Doris. Percival. And... oh dear. Gerald.
[portrait: MAELIS, angry] You have Gerald in a BALL?
[bubble: MAELIS, angry, anger] GERALD has a FOUR-PAGE FILE.
> Give Gerald back.
  [portrait: MAELIS, neutral] ...Hm. Well. Thank you. We shall remember this.
  (Received: NUGGET. And, the Keeper whispers, the Queen's undying suspicion.)
> Keep Gerald.
  [portrait: MAELIS, deadpan] Then Gerald has chosen. We shall have his file sent on. All four pages. You'll want to read page three in particular. It concerns warm stones.
```
*(15_COMEDY Ch10 "The Royal We", adapted so it works whether the PC caught one Scatterbug or forty. The Trials quest "Gerald" (EL_GERALD) is the long version.)*
*Optional: "What Are You For?" (Melia's cameo, CAMEOS #4) in the Chase's copse: a blonde girl with a Togekiss looking for a friend who "fell through a sewer". Extra payoff if S182 (Venam) is set.*

## Map 294 — Chapter 10 close: **"Dear Uncle Rowan"** (autorun on sleeping at 281 with V131 == 11)
```
(Night. The Heartgarden. The flowers closed for the night, the way flowers are supposed to. The Bride Tree in moonlight. In the potting shed, a lamp is lit.)
(Juno is at the shed bench, in her nightdress and her wreath, with a pen. The same bench, though she doesn't know it. A seed-tin on the shelf above her says NOT SEEDS.)
(She writes three words. Stops. Crosses them out. Starts again.)
PAPER (shown on screen, in green ink): "Dear Uncle Rowan,"
(Under it, crossed out: "How could you" — "Are you hurt" — "I took your seat, I'm sorry" — "I watered her this morning. Before the bees.")
(She tears the page off, balls it up, and throws it into the dark outside the shed door. Then the next one. Then the next.)
(Where each page lands in the garden, a flower comes up through it. Pale, white, small. By morning there will be a little path of them from the shed door into the dark.)
(Juno puts her head down on the bench beside the lamp and stays there.)
(Under the Bride Tree, in the dark, if the Ogre is with her, a small masked shape sits down by the shed door, facing out, and keeps watch.)
V131 = 12. V102 STORY_CHAPTER = 11.
QUEST LOG: "Eighteen Roads" — Earn the tenth badge in Rimeholt, up the Hart Road through the Hoarwood into Isenmar. Juno wants to come.
```
*(06_ACT_III's cliffhanger. Juno travels with the PC in Ch11 to lobby the northern Wardens, unless `bond(:JUNO) <= -5`, when she goes ahead alone; `30_SCRIPT_CH11.md` has both.)*

---

## Map events needed (Chapter 10)

None of these maps is built. **[NEW]** = an event or map not in maps.json. V131 = **CH10_STEP** (design/FLAGS.md).

**Every Pokémon Center (from V101 >= 3)** — the Mandate scanner arch over the door (decor event) with the two-note SE and the "PRIORITY GUEST" screen (two texts by `:pro_fellowship`); the nurse's line the first time. From V133 >= 7 (Ch12) it says SUSPENDED.
**261 Ironreach Pokémon Center** — **"Morning"** autorun (Nell on the bench; Juno's note).
**692 The Tailings** — road sign; the sledging boy and the officer at the barrier (a sledge-on-shovel decor event); the Mandate notice (sign, two chalk lines). Trainers. The fence gap to 684.
**688 Echo Coliseum** (optional) — Field Notes; the echo (action, loops the three lines); the Bleed-touched Timburr (wild, once).
**680 The Rootdeep / the Lift Road** — road sign; root-cathedral decor; the lift-hand; **the branch autorun at the lift foot** (V131 == 0): **A** Calla (if `standing(:MERIDIAN) >= 4`; a maintenance door in the root-wall to 699, S172), **B** the Hollow runner (else if `standing(:HOLLOW) >= 4`; leads to 684, S171), **C** the refugees on the lift (else; three NPCs with a cart, a birdcage, a championship belt). All set V131 = 1. The lift ride up (fade).
**699 Meridian Black Site** — the white room; the glass cradle with Type: Null (event sprite, the helmet turns to face the PC on a move route); Quent at the console; Calla at the door; `:ch10_null` (TYPE: NULL Lv 45 on `:take`, S180).
**684/685 Grudgestone Quarry → 698 Hollow Sanctuary** — the gap in the fence; the second level; the root-curtain; the Sanctuary (bedrolls, kettle, lamps, 4–6 Hollow NPCs and children); Wick (HYMN FRAGMENT, WICK'S LETTER); the Lowmarsh woman at the kettle.
**The Lift's top station (on 690's edge)** — **"The Envelope"**: Kestrel on the bench with the sunburst envelope (touch on arrival; V131 = 2).
**690 Lanternroot** — the fungus-grower; the miner's wife (the bleeding root hook).
**681 Prism Falls** — road sign; the rainbow (an overlay/fog event that casts a shadow, if the art allows); the painter; the pilgrim.
**693 The Briarway** — road sign; overgrown briar across the road (decor, passable); abandoned clipping ladders; the royal gardener; the Thornguard at a milestone. The gardeners' door in the hedge to 682 (opens after S126).
**284 Kingsgate Barbican** — arrival autorun (V131 == 2): the gate clerk (gives a pollen mask, flavour), the woman with a trowel and the unrotted leaf; S165 on, V106 = 1. The city's bloom state (V106 1 → 2) changes tiles or overlays on 280–296: roses through cobbles, vines on roofs, pollen fog.
**280 Market Terraces / 281 PC / 282 Mart** — florist, Rootward boy, Thornguard at the Heartgarden stair (lets the PC up); **281 the Wardens' Circular** board (post one); the Gazette board (headlines after V131 >= 10); the royal herald (V131 == 10, S126).
**294 The Heartgarden** — the Bride Tree (big event sprite) at the head of the stair to 708; the Veil across the stairhead (V131 5–7); the chapel steps; **"Three Claimants"** (autorun at the garden gate, V131 == 3): Valen, Maelis, Caedmon, the Meridian delegate, 4 Thornguard, Juno, the press clerk; the testament and the ring (V131 = 4); Tamsin's arrival; **"You Knew"** (only if `:ch2_tamsin == :keep_secret`: three Lowmarsh weavers); **"She's Listening"** (Juno at the tree; the Venam branch on S182; V131 = 5); **"Little Gardener"** (autorun after Gym 9, V131 == 9: the delegate, the Queen, the Thornguard filing out; then `:ch10_succession_stance` with the press clerk and Celestine's disguise in the crowd; V131 = 10); the potting shed (**"Dear Uncle Rowan"** at night; the paper-flower path; V131 = 12, V102 = 11); the Ogre by the shed door if S223. Trials: EL_EVER_BLOOM, EL_BRIDE_TREE_HEART at the tree (after S125 / Gym 9).
**708 The Bride Grove** — `:BLEED` until S125, then `:FLOWER_GARDEN` stage 1. The stairhead Veil (touch: `Prismfall.checkpoint`, Field Notes; V131 = 6); **the safe-path puzzle** (six root-nodes; a quiet-corridor state on walked tiles that closes after N steps unless pinned; the puzzle engineer owns it; DUNGEON_PUZZLES); Bleed-maddened Grass Pokémon that wander off near the PC, plus a few wild battles; **the Ogre** in the root-hollow (Ogerpon sprite with club; its ring of broken bloom); Juno as a follower along the corridor; **the Loyal Three** (three event sprites with glowing collars; the kneel; `:ch10_ogre`; the GO_LOYAL chain; the boss sequence `:LOYAL_THREE` with `PARTNER_OGRE` on `:ogre`; S127, V131 = 7); **the Plate** in the roots (glow event; the bloom-lies-down effect up the stair; S125, V106 = 2, S165 off, V131 = 8); Valen and Tamsin at the stairhead.
**290–293, 297 the Heartgarden Gym (Gym 9)** — doors open at V131 >= 8; as GYM_PUZZLES Gym 9; Juno's sign; the gym guide; Bram's hints (291, 292); **Juno (293), single**, field stage `1 + min(V345, 4)`, the stage-4 opener (V345 >= 3), the mid-battle lines by `:ch7_ledger`, MEADOW BADGE, TM53; V131 = 9. Mastery 297 as GYM_PUZZLES.
**285–289 Briar Hall** — flavour only this chapter (the Queen's court is in the Chase; Thornguard at the doors). **296 Rootward** — EL_ROOTWARD_WAKE (Trials, after V131 >= 8). **283 Glasshouse Ward** — townsfolk.
**682 The Royal Chase** — opens at S126: the Chase warden (Safari rules); **the Queen's garden** (Maelis alone on the bench; touch once; V131 = 11); **"The Royal We"** at the gate (condition: any Scatterbug caught in the Chase, or EL_GERALD done; the Keeper with the ledger; one bubble line; NUGGET on returning Gerald); Melia's cameo in the copse (CAMEOS #4); EL_GERALD (Trials).

**Trainer designer:** `PARTNER_OGRE` [NEW] (a partner with one Pokémon: Ogerpon, Teal Mask, Lv 48, Ivy Cudgel, Horn Leech, Spiky Shield, Follow Me); Lowmarsh weavers aren't battles. **BOSSES.md:** `:LOYAL_THREE` [NEW] — Okidogi, Munkidori, Fezandipiti in sequence, Lv 46–48, 2 bars each on Standard (3 on Hard; +1 bar each on `:hesitate`), field Bleed; Fezandipiti's last bar uses the Sweetrot smell (a Confuse-or-Attract-style "you'd agree with anyone" message once); no catch (they flee; caught in Ch18). **Items owner:** HYMN FRAGMENT (Key Item; completes in Ch18), WICK'S LETTER (Key Item; delivered in Ch13), pollen mask (flavour, no item needed). **Puzzle engineer:** the Bride Grove's safe-path room (708). **Badge name (proposed):** the **Meadow Badge** (already in `LEADER_JUNO`'s LoseText).
