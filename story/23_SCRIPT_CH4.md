# Script: Chapter 4 — "Both Ways" (the Hoar Road, Frostwick, Gullcry, Ebbmouth, Gym 3; K2)

> **Final playable script** for Chapter 4. It covers the Hoar Road north out of Briarwick (566 Spinners' Rise, 577 Frostwick Pass, 570 Frostwick and its interiors 571–576, 578 Rimewood Path, 562 the Rimewood), 561 Gullcry Cliffs (K2) and 564 Gullcry Caves, then Ebbmouth (160 and 167 the Mill Quay, interiors 161–166 and 168 the Net Loft) and the Tidelock Gym 170–174 (Gym 3). It follows `story/21_SCRIPT_CH3.md` and uses the conventions of `story/20_SCRIPT_CH0-2.md`.
> **These maps are built** (map builders 10–14). Their flavour events stand as built; this script adds the story events and the lines that change, and marks every event that isn't on the built map **[NEW]**. Where a built event's text changes, the new text is here and the event is marked **[CHANGED]**. The list at the end says exactly what to wire.
> Sources: 04_ACT_I Ch4, 03_CAST (Marisol, Teo, Kestrel, Larch, Hesper), 09_MYSTERIES (#2a, #3, #10, #14, #22, #29), 10_CHOICES_ENDINGS and NARRATIVE_KEYS (`:ch4_kestrel_mourner`, `:ch4_teo`), 14_WAR_AND_BLESSING (the Ch4 seed), 15_COMEDY (Ch4 "He Followed You Here"; running gags 1–3), TRIALS / TRIALS_QUESTS (the Tally and Prize Exchange quests of Ch4), GYM_PUZZLES Gym 3 (the trim), BALANCE (K2, Marisol), `design/CHAPTER_BEATS.md` (proposal A).

## Conventions
As in `20_SCRIPT_CH0-2.md`: `[portrait: NAME, expression]` faces for the story cast in `Prismfall::Portrait::CAST` (tagged on a speaker's first line in a conversation and where the expression changes; later lines `[name: X]`), the rare `[bubble: NAME, expression, emote]` for a marked comic beat, and `[name: X]` for everyone else. `> option` choices, `MOVE:` / `SE:` / `BGM:` / `WAIT n`, `[after X]` and `[if ...]` variants. Gym numbers are for reading; events call `Prismfall.gym_battle(pfm_gym(:LEADER_MARISOL), double: false)` and `pfm_gym_won?(:LEADER_MARISOL)`.
**In the cast list here:** Kestrel, Marisol, Teo, Larch, Juno (letters only), Thistle (seen, not heard). **Plain:** Aria and the other Octave singers, Bersi, Pella, Mrs Reyes, every townsperson and trainer.
**Counter:** V124 **CH4_STEP** (design/FLAGS.md): 0 the Hoar Road · 1 K2 · 2 Marisol met · 3 the strike vote · 4 the night · 5 the morning after · 6 Gym 3 won · 7 Larch's confession (chapter closed).

## The chapter's key events (design/CHAPTER_BEATS.md)
1. **The Night the Ebb Stopped.** Meridian's night export draw kills the river for an hour (the cause); the masked cell blows the intake to stop the draw, and in doing it brings the river back all at once, recklessly, without looking at the water; the river comes back and drags a child's punt at the Guild mill-race, the same race that killed the Reyes siblings' father; the masked boy who helps haul the gate is Teo; the PC answers a Meridian guard with Marisol standing there (`:ch4_teo`). Build-up: Teo by day at the strike vote, and the river stuttering longer each time. Payoff: the morning after shows the choice on the quay. Consequence: Teo hunted or hidden in Ch5 and Ch9, Marisol's bond and Consent.
2. **Larch's confession.** The tide tables prove the stutters, and the full stop, are Meridian's draw. "I lit up this whole region, you know. Eleven cities on my design." The first time the PC learns their mentor built the machine (the red herring "Larch works for Meridian" starts here; it resolves in Ch12).
**Nothing comic** inside the night from the moment the river stops until the guard leaves, or in Larch's confession once the tide tables come out (15_COMEDY §1: jokes before, a full scene after).

---

# CHAPTER 4 — "Both Ways"

**Chapter start:** V102 = 4 (set by Briarwick's charcoal child, Ch3 close). Juno has gone home to Verdance with the hatbox; the PC travels alone this chapter. V124 = 0.

## Map 566 — Spinners' Rise (`:MEADOW`; built)
*Built events stand: road sign, the Fleece Cross, the Ribbon-tier, the Shepherd, the third cottage, the shepherd boy's Ram Race, the sheep-wash, the hill-fort ring, Road Stone III.*
```
[CHANGED] Shepherd (second talk):
[name: Shepherd] Boy in a black coat came up the drove road yesterday at a run. Didn't stop at the Cross.
[name: Shepherd] Everybody stops at the Cross. Even the Wooloo stop at the Cross.
[NEW] Ribbon-tier (after the Fleece Cross is read):
[name: Ribbon-tier] Three women in grey tied a ribbon here two nights back. Grey ribbon. Nobody ties grey.
[name: Ribbon-tier] One of them cut it off the spool with shears so sharp the end didn't fray. You don't see that outside Briarwick.
```

## Map 577 — Frostwick Pass (`:SNOWY_MOUNTAIN`; built)
*Built events stand: road sign, the Handfast Arch, the toll hut ledgers, the bothy keeper, the wind gap and gusts, the frozen fall, the Snorunt among the snowmen, the avalanche fence, the buried signpost, the Icium Z gully. Trainers: Kari & Kaia (double), Liv, Eirik, Hrodgar (trainer designer, round 4).*
```
[NEW] EV "Under the Arch" (touch strip in the arch's gap, once):
(The wind drops. On one side of you the arch is whale-jaw, white and smooth as soap. On the other it's briar, alive, with frost on every thorn. Bolted across the keystone, very shiny, is a brass sunburst.)
You walk under it. For a step you are in neither kingdom.
(The PC's hand goes to their chest. It doesn't hurt. It's just there.)
[CHANGED] Toll hut ledgers (second page, after the first read):
The Elowen ledger has a new entry, two days old: "Three on foot. Grey cloaks. Paid in silk."
The Isenmar ledger, same day: "Nobody."
[NEW] Hrodgar, the huscarl at the Arch (trainer lines; BLACKBELT "Hrodgar"):
[name: Huscarl Hrodgar] I keep the arch. The Elowen forester keeps the other half. We've never agreed which half is which. (Battle.)
[name: Huscarl Hrodgar] [after] Pass. You've a thaw in you. Isenmar respects a thaw. It doesn't trust one.
```

## Map 570 — Frostwick (built) and interiors 571–576

### Arrival (autorun, first entry by the East Gate) [NEW]
```
(Six giant trees glazed in clear ice, with Elowen treehouses in their arms. Under them, turf-roofed longhouses with whalebone gables. A frozen brook runs through the square; children are fishing through holes in it. Over everything hang curtains of silk that froze years ago and never thawed.)
[name: Huscarl at the gate] Wipe your boots. Declare any honey.
[name: Forester at the gate] He means welcome. We both mean welcome. We just say it in two languages and neither of them is "welcome".
```
*Built events stand: the Hearth Stone, Brannagh and Halvard, the honey-seller, the fishmonger, the children in ogre and whale masks, the ice-fisher, the brazier woman, the Swinub herder, the rime-silk weaver, the South Gate sign.*
```
[CHANGED] Fishmonger (second talk):
[name: Fishmonger] Boy in a black coat bought one smoked eel and asked had anyone seen a woman in a mask.
[name: Fishmonger] I said, in Frostwick? It's Thawfeast in a fortnight, love. Everyone's in a mask. He didn't laugh. Then he bought a second eel.
[CHANGED] Old woman by the brazier (third talk):
[name: Old Woman] Three women in grey slept by my brazier two nights back. One had shears on her belt.
[name: Old Woman] I woke and my old shawl was mended. Twelve years I've had that hole. She didn't take a thing. Didn't leave a name.
[name: Old Woman] Hollow, the huscarl says. I said, then the Hollow darn better than the huscarls.
```

### 571 — Frostwick Pokémon Center: Gale Post desk [NEW]
```
GALE POST DESK: Two letters are waiting.
(First letter, in green ink with a pressed blossom inside:)
"Dear \PN,
Forty eggs, forty caterpillars. One is a Spewpa already and very rude.
Uncle Rowan cried. He says he didn't. He did.
I told him about the Pageant, and what the man in the mask said about Verdance. He went quiet and said, 'Did he, now.' Then he went out to water Aunt Elin and he was out there until dark. I've never seen him angry before. I think he's angry with the man.
He's off on Warden business next week, so I'm minding the Heartgarden by myself, which means I'm minding a tree. Write back! The Gale Post knows where I am. Everyone knows where I am. I'm the one wearing a tree.
— Juno
P.S. Don't let Kestrel be rude to you.
P.P.S. Is he being rude to you?"
(Second letter, on brown paper that smells of the sea:)
"You're in Isenmar. Wear a hat. Lecture Three is postponed on account of weather. — I.L."
(Received: KELP TEA BAG. "Three. You have a set.")
```
*(Juno's letter carries a fair clue for 09 #2: Rowan's "Did he, now", and "Warden business" in the week before Lumen.)*

### 573 — The Two Hearths (inn; built: Brannagh, Halvard, a guest)
```
[NEW] Bard (by the Isenmar hearth; maps.json "bard"):
[name: Bard] A song for the stranger? It's the only one I know all the way through. Everybody in Isenmar does.
♪ Sleep, old whale, under the ice.
  We salted the sea, and we've paid the price.
  Keep your eyes shut and your great heart slow,
  for the day you wake, all the ice will go. ♪
[name: Bard] My gran said the frozen sea's a blanket, and there's something asleep under it. When the whale wakes, the sea remembers it's a sea.
[name: Bard] The southerners think it's a lullaby. It's a warning. We just sing it gently.
HALF-TALLY BOARD (Ingrith, the rune-carver; Trials): one board, runes on the Isenmar side, lanterns on the Elowen side.
  → "Two Hearths, One Pot" (IS_TWO_HEARTHS) and "The Oathbound Parcel" (IS_OATH_PARCEL), as TRIALS_QUESTS.
```

### 575 — Border House [CHANGED: the three clerks]
```
(Three desks in a row: an Elowen forester-clerk with a briar seal, an Isenmar huscarl-clerk with a whale seal, and between them, a Meridian clerk with a brass scanner and a sunburst stamp.)
[name: Elowen Clerk] Name and town, please.
[name: Isenmar Clerk] Name and hall.
[name: Meridian Clerk] Name and tint. Hand on the plate, please.
(SE: chime. Then nothing. The plate stays dark.)
[name: Meridian Clerk] ...
[name: Meridian Clerk] I'll put "pending".
[name: Elowen Clerk] There's no box for "pending".
[name: Isenmar Clerk] There's no box for anything. Stamp it and let them through.
(Stamp. Stamp. And then the sunburst, right across both.)
Your travel paper now has three seals on it. The sunburst covers half of each of the others.
```

### 572, 574, 576 — the Exchange, the Rime-silk Loft, Halvard's Smokehouse
*Built events stand.* `[NEW] Rime-silk weaver (574), after the gift: [name: Weaver] Briarwick silk drifts west on the wind and freezes in the Rimewood. We've been weaving Tamsin Loom's wood for a hundred years and she's never once sent a bill. Don't tell her.`

### The Frostflat Causeway (560) and The Rehearsal (568) — optional side road
*Built: the customs chain at the Border Stones unhooks from the Frostwick side; the Rehearsal is the Trials quest "The Rehearsal" (EL_REHEARSAL, Ditto). No story events. The Causeway is the road back to Saltmere and the Legion barge ("The Little Crucible").*

## Map 578 — Rimewood Path (`:SILKWOOD`; built) and Map 562 — The Rimewood (built)
*Built events stand: the frozen silk curtains, the Unblazed and its wrong turns, the Lantern Birch, the charcoal kiln and burner, the trapper and the snare line, the honey-stump hives, the woodcutter, the Long Ice, the Stantler stag (578); the lost trapper child, the trapper, the Frost Loom (D7), the fallen giant, the applewood log, the frosted sapling to the Glade, the Wolfsrime (562). Trainers on 578: Ottar, Ketil, Brand, Hild, Ragna.*
```
[NEW] EV "Cold camp" (562, a clear spot by the fallen giant; action):
A camp, two nights cold. Three sleeping hollows in the snow, close together. Strips of orange cloth in the dead fire: Meridian survey flags, used as kindling.
Beside the ash, half a carved bark mask with the same sad face as the masks in Briarwick. Someone stopped carving it halfway.
Over the three sets of footprints going north, a fourth set, newer, bigger strides. Boots. In a hurry.
[NEW] Lantern Birch (578), second page (after the built Never-Melt Ice gift):
[name: Trapper's note, nailed under the lamp] "For whoever's late. — the trappers." Somebody has added under it in a sharp hand: "Not late. Ahead." Then, in a third hand, very neat: "Mind the boy in the coat. He walks like he's angry at the snow."
```

## Map 561 — Gullcry Cliffs (`:MOUNTAIN`; built) and Map 564 — Gullcry Caves (built)
*Built events stand: the landslide (the caves are the way north), the cave mouths, the whalebone waymarkers, the cod-skull cairn, the signal-fire platform, Road Stone III-c, the gull stacks, the gannet feather and the Cramorant, the net-mender, the stilt-hut fisher; in 564 the tide clock, the gull roost, Old Asta's board (Trials "The Egg Thief of Gullcry", after Badge 3) and the weed curtain.*

### EV "Kestrel K2" (561, the gap between the tors at (11,7); touch) [CHANGED: replaces the built lines]
```
(The cliff path narrows between two tors. A boy in a too-big black coat stands in the gap with his back to you, watching the road to Ebbmouth through a cracked brass spyglass. Gulls wheel below. He doesn't turn round.)
[portrait: KESTREL, neutral] Don't. Whatever you're about to say. Don't.
[name: Kestrel] Three of them. Grey cloaks. Over the pass two days ago, into that town last night. I've been one day behind them since Saltmere.
[portrait: KESTREL, angry] And now there's you. Standing in my one gap. Breathing loudly.
> I'm going to Ebbmouth too.
  [portrait: KESTREL, deadpan] Of course you are. Everyone's going to Ebbmouth. It's very popular, for a town that smells of eel.
> Who are they?
  [portrait: KESTREL, neutral] Hollow. The ones who cut the ropes in Saltmere. One of them talks to the Mourner. I'm going to find out what he says back.
> ...
  [portrait: KESTREL, angry] Gran does that. I told you. The staring.
MOVE: Kestrel turns round and lowers the spyglass. At his hip, one of his Poké Balls is humming, steel on steel.
[portrait: KESTREL, neutral] Gran gave me something before I left. She came down the lighthouse stairs at four in the morning, put it in my hands and went back up. Didn't say a word.
[name: Kestrel] Then she shouted down the stairs: "It was your mother's blade's child. Don't you dare lose it."
[name: Kestrel] Honedge. Most she's said to me in a year.
[portrait: KESTREL, smug] I named it Morwen. Gran hasn't spoken to me since.
[portrait: KESTREL, angry] Move. Or don't, and I'll move you.
Script: Prismfall.rival_battle(:RIVAL_KESTREL, "Kestrel", 2)     # K2; version 20 + starter slot (SPINE); Staravia, Honedge "Morwen", the counter-starter (BALANCE); field :MOUNTAIN (561 default)
(When Honedge enters:) [portrait: KESTREL, neutral] Go on, Morwen. Show them how she held a line.
(LOSE: standard whiteout to the Frostwick Pokémon Center. Kestrel on retry: "Back again. Good. I needed the practice of beating you.")
(WIN:)
[portrait: KESTREL, shocked] ...
[portrait: KESTREL, angry] Morwen held. It HELD. It's the rest of them that — tch.
MOVE: Kestrel recalls Honedge and holds the Ball against his chest a moment too long. Two fingers tap his sternum, twice.
[portrait: KESTREL, neutral] You were in the Lantern. You heard him. Under the doubling.
```
**CHOICE `:ch4_kestrel_mourner`**
```
> Do you think the Mourner is your mother? (kind)
  Script: pf_choose(:ch4_kestrel_mourner, :kind)
  [portrait: KESTREL, angry] Don't.
  [portrait: KESTREL, sad] ...Don't ask it like that. Like it's a thing you can just ask.
  [name: Kestrel] She died in Gravenmoor six years ago. They sent Gran a box. There was a veil in it and a form. The form said "personal effects".
  [portrait: KESTREL, neutral] So I don't think anything. I'm just going to look at his face.
  [name: Kestrel] ...Thanks for asking it quiet. I suppose.
> He sounds just like her, doesn't he. (blunt)
  Script: pf_choose(:ch4_kestrel_mourner, :blunt)
  [portrait: KESTREL, angry] You never heard her. You don't get to say what she sounds like.
  MOVE: Kestrel shoves past, shoulder to shoulder, hard enough to rock you.
  [name: Kestrel] Stay out of Ebbmouth, ferry kid.
> ... (silent)
  Script: pf_choose(:ch4_kestrel_mourner, :silent)
  [portrait: KESTREL, sad] ...She'd never wear a mask. She hated masks.
  [name: Kestrel] Gravenmoor's all veils. Everybody in mourning all the time. She said a face is the only honest thing a Warden owns.
  [portrait: KESTREL, neutral] So it isn't her. It can't be. I just need to see that it isn't.
(All:)
MOVE: Kestrel goes north toward Ebbmouth, fast, coat flapping.
Switch S111 CH4_K2_DONE = ON. V114 KESTREL_STAGE = 1 (already 1 since Saltmere). V124 = 1.
```
*`:kind` also earns his curt note at the chapter's end; `:blunt` gives the "didn't pay for his eel" line instead.*

## Map 160 — Ebbmouth (built; BGM "Lerucean Town"; rain and sea-mist)

### Arrival (autorun, first entry from Gullcry Cliffs, V124 == 1) [NEW]
```
(Fog off the sea. Gulls. Stilt houses, canals, footbridges, smoked-eel stalls, union halls with painted signs. Through the middle of the town the River Ebb runs fast toward the harbour.)
(Then it stops.)
SE: the river's noise cuts out. Every mill-wheel on the Ebb freezes mid-turn. On the quay, a dockworker stops with a crate half-lifted. Nobody moves. WAIT 90.
SE: the river comes back with a slap against the pilings. The wheels lurch and turn. The dockworker breathes out and puts the crate down.
[name: Dockworker] Forty seconds. That's the longest this week.
[name: Dockworker] Welcome to Ebbmouth. The river runs both ways. Lately it can't decide.
V108 EBB_STATE = 1.
QUEST LOG: "Eighteen Roads" — Earn the third badge at the Tidelock Gym. (The gym is on the river, east.)
```
*Built events stand: the Upper Mill and Guild Mill wheels, the harbour mast, the ice-fisher's song, the Guild striker, the dockworker, the Guild organiser, the eel-smoker, the lock-keeper, the Meridian surveyor, the child with the toy boat, the old whaler, the gull, the signs. Lines that change:*
```
[CHANGED] Child with a toy boat (17,41) → name her Pella:
[name: Pella] I race my boat down the race! When the river stops, it stops too. Then it's a draw.
[name: Pella] (again) My da says never go on the water when it's stopped. It's stopped all the time now. What's the point of a rule that's on all the time?
[CHANGED] Lock-keeper (43,20), before V124 >= 5:
[name: Lock-keeper] Tidelock's shut today. The Warden's at the Guild vote on the Mill Quay, up the towpath. North.
[name: Lock-keeper] She's the Guild's Warden, see. Elected. When the Guild calls, she goes, and the gym waits. You can go and watch. Everybody watches.
[NEW] Teamster, just back from the south (by the harbour; war seed, 14_WAR Ch4):
[name: Teamster] Ashkaar rider burned a sled-caravan on the dune road west of Duneholt. Isenmar sleds, Isenmar furs, Isenmar men.
[name: Teamster] Ossaria says it's none of their business. It happened on their sand.
[NEW] Meridian recruiter (by a poster on the Lattice station wall):
[name: Meridian Recruiter] Heat contracts! Meridian Contract Seven! Warm for life, and your grandchildren's lives!
POSTER: "HEAT FOR ISENMAR — Meridian Concord." The picture is of great forges glowing in a crater. They're in Ashkaar. Somebody has written under it: "THEIRS."
[CHANGED] Guild organiser (22,30), second line:
[name: Guild Organiser] And the Thane's raising a war-levy on the catch. "Just in case." In case of what? He won't say. Everyone knows.
[NEW] Fishwife (at the eel stall's end):
[name: Fishwife] The Professor? Larch? The one with the tea? She gets letters from the Meridian Spire. Sunburst seal and everything. I've seen the postman's face.
```
*(The fishwife plants the red herring "Larch works for Meridian" an hour before Larch's confession.)*

**Trials hooks on this map (Ch4 quests; TRIALS_QUESTS):**
- **The Drowned Note** (IS_OCTAVE_DROWNED_NOTE): Aria of the Octave in the shallows at the river steps, singing a shanty wrong on purpose. Octave encounter 2 of 8 (gym order). *Plain name box: Aria is not in the portrait cast.*
- **The Lattice Hums Wrong** (ZE_LATTICE_HUM): P-3NNY/2 at the Lattice station; the three mill-wheel recordings. It foreshadows Larch's tide data: the "larch" answer earns her "I had this already."
- **A Deed for the Skald** (IS_SKALDS_SAGA): Bersi Gullsong in the Net Loft (168).
- **Master of Nothing**'s Wattrel "Mast" on the harbour mast after Badge 3 (EL_MASTER_OF_NOTHING).

### EV "He Followed You Here" (the eel-smoker's stall, (13,29); touch, V124 == 1) — comedy scene Ch4 [NEW]
```
(The smoked-eel stall. Behind it, wedged between two barrels with a spyglass, is a black coat.)
[name: Eel-smoker] Smoked eel! Smoked char! Smoked anything you hold still long enough!
(A woman comes down the quay in rolled sleeves, oilskin over one shoulder, a brass union pin on her collar. She has the walk of someone who's been on a deck all her life. She stops, looks at the barrels, and grins.)
[portrait: MARISOL, smug] That your friend, kid? The one who's been hiding behind my eel stall since noon?
MOVE: Kestrel stands up too fast and hits his head on the stall's awning.
[bubble: KESTREL, shocked, shock] I was conducting SURVEILLANCE!
[portrait: MARISOL, smug] You bought four eels.
[portrait: KESTREL, blush] ...They're good eels.
[portrait: MARISOL, happy] Tides take it, he's adorable. Does he bite?
> Yes.
  [portrait: KESTREL, angry] I do NOT—
> Only Juno.
  [portrait: KESTREL, panic] That was ONE TIME and she was HUGGING me!
> ...
  [portrait: MARISOL, happy] Silent type. And a biter. I've hired worse. I've hired worse this week.
[portrait: KESTREL, angry] Stay out of my way. Both of you. I work alone.
MOVE: Kestrel stalks off along the quay. He comes back, buys a fifth eel without looking at anyone, and stalks off again.
[portrait: MARISOL, happy] Marisol Reyes. I keep the Tidelock, and the Guild keeps me. You'll want a badge.
[portrait: MARISOL, neutral] Not today. Today the Guild votes on whether we strike, and the Warden's got to be on the quay when it does. That's the job here. They elected me. They can un-elect me.
[name: Marisol] Mill Quay, up the towpath, at the bell. Come and see what a Warden's for in Ebbmouth. Then come and lose to me tomorrow.
MOVE: Marisol goes north up the towpath.
V124 = 2.
```
*Eel-smoker, after:* `[name: Eel-smoker] I keep a ledger. "THE BOY: four eels, daily." It's day one and I've had to start a second page.` (15_COMEDY's Isenmar bit.)

## Map 167 — Ebbmouth, the Mill Quay (built)

### EV "The Strike Vote" (autorun on entering 167 with V124 == 2) [NEW]
```
BGM: fades out. SE: the Guild bell, three slow strokes.
(The Mill Quay at dusk. Two hundred dockworkers, millers, net-menders and ice-cutters packed between the union halls. The great Mill Quay wheel turns behind them. Marisol stands on an upturned eel barrel. High on the wheel's platform, a young man in a fisherman's jumper sits with his legs dangling.)
[portrait: MARISOL, neutral] Right. Shut up. Thank you.
[name: Marisol] The Thane wants a levy on the catch. Meridian wants a third of the mill crews gone by spring. The river stopped forty seconds this morning, and the Lattice man says that's "within tolerance".
[name: Marisol] I've a motion to strike. I've a motion not to. I'll hear both and then we'll vote like people, not gulls.
[name: Young Man on the Wheel] Ask her who pays the Warden's lamp oil!
(Laughter. Some of it isn't kind.)
[portrait: MARISOL, angry] Meridian pays for every lamp on this quay, Teo, yours included, and you know it.
[portrait: TEO, smug] Then turn yours off, sis. I have.
[name: Teo] (to the crowd) They take the river at night! Every night! You sleep and the Ebb stops and in the morning it's "within tolerance"! Strike! Strike or drown!
(Half the quay cheers. The other half looks at its boots.)
[name: Mrs Reyes (from the crowd)] TEODOR. Come down off that wheel. You'll fall in like your father.
[portrait: TEO, neutral] ...Hi, Ma.
(The river stutters. The great wheel stops dead. Two hundred people hold their breath. WAIT 60. SE: the slap of the river coming back. The wheel lurches on.)
[portrait: MARISOL, neutral] One minute. That's a minute now.
[name: Marisol] We don't vote in the dark. Every hall votes at first light, the way we always have. Go home. Kiss somebody. Count your nets.
(The crowd breaks up, muttering. Teo drops down off the wheel, lands like a cat, and walks straight up to you.)
[portrait: TEO, happy] You're the ferry kid. The null one. Yes, I know; the fishwives here write to the fishwives in Saltmere. Teo. Teo Reyes. The disaster in the family.
[name: Teo] Free lesson, since you came all this way. The Ebb runs in on the morning tide and out at night. Three hundred years. My da set his watch by it.
[portrait: TEO, angry] Now it stops when Meridian gets thirsty. Count it with me next time. One. Two. It's always on the hour. Rivers don't wear watches.
[portrait: TEO, smug] Don't tell my sister I was charming. She thinks I'm a lost cause. It's the one thing we agree on.
MOVE: Teo jogs off up the quay into the dusk, toward the river mouth. He doesn't go home.
[portrait: MARISOL, sad] *(watching him go)* He's nineteen. He thinks shouting is a plan.
[portrait: MARISOL, neutral] Gym's open at first light, after the vote. Get some sleep, kid. There's a bed at the Center.
V124 = 3.
```
*Built Mill Quay events stand (strikers, the union steward, the miller who hears "a note held too long" under the wheel, the carter). Aria's quest finishes under this wheel ("The Drowned Note").*

## Map 160 — **EV "The Night the Ebb Stopped"** (replaces the built "Teo" event; autorun on returning to 160 from 167 with V124 == 3, or on resting at the Center with V124 == 3) — **key event 1**
*Staging on 160's river: the Guild Mill and its race at (29,37), the brass intake by the Lattice sign at (27,40), the river channel through the town, the race gate's chain platform beside the Guild Mill, the Reyes House at (6,8). Night tone, rain. No jokes from here until the guard leaves.*
```
(Night. Rain on the canals. The lamps on the quay are lit. The town is asleep.)
SE: the river stops.
(Every wheel freezes. The silence is so complete you can hear the rain land on the water, and the water doesn't move.)
V108 EBB_STATE = 2. WAIT 120.
[name: Dockworker (from a window)] That's not a stutter. That's... it's not coming back.
(Doors open up and down the quay. People in nightshirts stand on their steps with lamps. From the river mouth, the brass intake by the Lattice station gives off a high, thin whine, like a finger round the rim of a glass, and it is climbing.)
[name: Pella's Father] PELLA! Pella, come back here!
(In the middle of the dead-still river, a small girl in a nightdress is paddling a punt toward a toy boat that has stopped exactly mid-channel.)
[name: Pella] It's FINE, Da! It's not moving! It's like a big puddle!
(On the far bank, at the intake, three figures in grey cowls and carved bark masks. One of them, a woman, is cutting cable at the intake's housing with a pair of shears, one clean cut, then another.)
MOVE: Marisol comes down the towpath at a dead run in her nightshirt and an oilskin, barefoot.
[portrait: MARISOL, shocked] Who's on the water? Who's — oh, tides take it. Pella.
[portrait: MARISOL, angry] Kid. With me. Whoever's at that intake—
SE: a flat, hard BANG from the intake. A shower of sparks. The whine stops dead.
(And the river comes back. All at once. A black wall of water heaves down the channel toward the harbour, and the punt spins and goes with it, straight for the Guild Mill's race.)
[portrait: MARISOL, shocked] The race. The RACE. She'll go under the wheel!
[name: Marisol] The race gate! The chain's on the platform by the Guild Mill! Drop it, kid, DROP IT! I'll get the punt!
MOVE: Marisol throws a Poké Ball into the river. A Floatzel hits the water and she goes in after it.
(Two grey cowls run down the towpath toward you, away from the intake. They see you and stop.)
[name: Bereaved] Out of the way!
BATTLE: double battle vs [HOLLOW_GRUNT_M "Bereaved"] + [HOLLOW_GRUNT_F "Bereaved"] (Ebbmouth version; levels per BALANCE for the segment before Gym 3). Field: Water Surface (160's river).
(WIN:)
MOVE: the two Bereaved scatter over the footbridge. The third, the woman with the shears, is already on the far roofs. She looks back once, at you. Then she's gone.
(At the race gate's platform a fourth figure is hauling at the chain alone. Grey cowl. Bark mask. The chain won't move. He turns, sees you, and puts himself between you and the gate.)
[name: Masked Boy] *(through the mask, muffled)* Stay out of it! You too, ferry kid—
[name: Masked Boy] It's jammed, it's not your business, GET BACK—
BATTLE: HOLLOW_TEO "Teo", version 0 (his first battle; BALANCE 4b). Field: Water Surface. (Hollow admin; can't be fled.)
(LOSE: whiteout to the Pokémon Center; the scene restarts at the race gate, the punt still spinning in the current.)
(WIN:)
[name: Masked Boy] You don't — you don't fight like— 
(He turns to the gate and sees the punt for the first time: a child in a nightdress, spinning toward the race, screaming for her father.)
[name: Masked Boy] ...No. No, no, no. I didn't — there wasn't anyone on the water—
[name: Masked Boy] Help me. HELP me. It's jammed at the pawl, it takes two!
> (Haul the chain with him.)
(Only one choice. The PC takes the chain beside him. SE: iron grinding. The pawl gives. The gate drops into the race with a boom that shakes the platform.)
(The punt hits the gate a breath later and holds. In the water below, Marisol's Floatzel noses it against the stones, and Marisol reaches up and lifts Pella out of it by the back of her nightdress.)
SE: the river, running, roaring, alive.
(On the platform, the boy has pushed his mask up onto his forehead to see the water. He is soaked, shaking, and very young. In the lamplight from the mill, his face is plain.)
(Marisol comes up the race steps with Pella in her arms. She sees him.)
[portrait: MARISOL, shocked] ...Teo?
[portrait: TEO, sad] Mari. I didn't know she was out there. I swear on Da. I swear on Da, I didn't know.
[portrait: MARISOL, sad] *(very quietly)* Same race. Same race, Teo.
[portrait: TEO, neutral] They take it every night. Every night, Mari. Somebody had to—
[portrait: MARISOL, angry] Go.
[name: Teo] Mari—
[name: Marisol] GO. Before the Lattice men come down. Go!
MOVE: Teo pulls the mask down, vaults the platform rail and drops into the black water. A Carvanha surfaces beside him. They're gone downriver into the dark.
(Marisol stands there holding the girl. Then she looks at you. She knows you saw.)
WAIT 60.
MOVE: a Meridian Security guard runs down from the Lattice station with a lamp, out of breath.
[name: Meridian Guard] The intake! They've blown the intake! Warden, are you hurt? Is the child—
[name: Meridian Guard] Who was it? You, challenger. You were on the platform. Did you see a face?
(Marisol says nothing. Pella has her face in Marisol's shoulder. Marisol is looking at you.)
```
**CHOICE `:ch4_teo`**
```
> "It was Teo Reyes." (report)
  Script: pf_choose(:ch4_teo, :report)
  [name: Meridian Guard] Reyes? The Warden's—
  [portrait: MARISOL, neutral] My brother. Write it down properly. R-E-Y-E-S.
  MOVE: Marisol walks past you with the girl without looking at you, toward Pella's father.
  [name: Meridian Guard] ...Thank you. Meridian appreciates it. Really. There'll be a reward.
> "I didn't see his face." (keep_secret)
  Script: pf_choose(:ch4_teo, :keep_secret)
  [name: Meridian Guard] Didn't see his — you were standing next to him!
  [name: Meridian Guard] Useless. Every one of you, useless.
  MOVE: Marisol passes you with the girl. She doesn't stop.
  [portrait: MARISOL, neutral] *(low, as she goes)* I owe you. I won't forget it.
> Say nothing to him. Find Marisol after. (confront)
  Script: pf_choose(:ch4_teo, :confront)
  [name: Meridian Guard] Well? Nothing? Tides, you people.
  MOVE: Marisol carries Pella to her father. Over the girl's head, she looks back at you, and nods once at the Reyes House.
(All:)
MOVE: Kestrel comes pounding down the towpath, coat flying, much too late. He looks at the dropped gate, the blown intake, the empty water.
[portrait: KESTREL, angry] Where? WHERE did they go?
[portrait: KESTREL, neutral] *(he fishes a length of cable out of the race, washed down from the intake, and turns the end to the light)* One cut. Clean as a ribbon. Shears.
[portrait: KESTREL, sad] It's her. The one from Saltmere. One of them talks to the Mourner, and she was right HERE—
MOVE: Kestrel runs east along the dark quay after nothing.
Switch S112 CH4_TEO_MET = ON. V108 EBB_STATE = 1. V124 = 4.
(Fade to black.)
```

### 164 — Reyes House, the same night **[if `:ch4_teo` == :confront]** [NEW]
```
(The Reyes kitchen. A lamp, a kettle not yet boiling, a net half-mended over a chair. Marisol sits at the table in her wet oilskin. Mrs Reyes has taken Pella home. A photograph on the dresser: a big man with a union pin and Marisol's grin, at the Guild Mill.)
[portrait: MARISOL, sad] Sit. You're going to anyway.
[name: Marisol] Our da worked the Guild Mill forty years. AF 297, the first time the Ebb stuttered, he was in the race clearing weed off the wheel.
[name: Marisol] It stopped. He thought it was done. Then it started.
[portrait: MARISOL, crying] Teo was fifteen. He was on the platform. He's been on that platform ever since, one way or another.
[portrait: MARISOL, angry] And yes. YES. I knew. I've known since winter. I tell him where the Lattice patrols are going to be. Every week. Tides take me, I'm the Warden and I tell a Hollow cell where the guards walk.
[name: Marisol] Because he's nineteen and furious and he's RIGHT about the river, and because if they catch him they'll put him in a Meridian cell, not an Accord one, and I don't know what happens in those.
[portrait: MARISOL, crying] And tonight he nearly put a little girl under my da's wheel. So you tell me which of us is the monster.
> Neither of you.
  [portrait: MARISOL, sad] That's kind. It's not true, but it's kind.
> Both of you.
  [portrait: MARISOL, neutral] Ha. Yes. That's the Ebbmouth answer. You'd make a good Guild steward.
> ...
  [portrait: MARISOL, sad] ...Yeah. Me neither.
[portrait: MARISOL, neutral] The cellar's his. The door's barred from below, but there's a key in the teapot. Go and look, if you want to know who my brother is. I can't.
[name: Marisol] Gym's open at first light. Come and fight me. I'll be better at it than this.
(Received: CELLAR KEY.)
```
*[if `:ch4_teo` == :keep_secret], the Reyes House that night:* `[portrait: MARISOL, neutral] Not tonight, kid. Tonight I'm sitting here till he comes home or doesn't. Cellar key's in the teapot if you're curious. I'm not.` (Received: CELLAR KEY.)
*[if `:ch4_teo` == :report]:* the house is dark, and the door is locked until morning.

### 166 — Reyes Cellar (the Hollow cell) [NEW map: maps.json has it, no spec yet]
```
[if :ch4_teo == :report] (Morning. The cellar door has been kicked in. Two Meridian guards are boxing up maps and wire.)
  [name: Meridian Guard] Nothing here. Cleared out before we came. Somebody tipped them. ...Not you. You're the one who told us. Thanks again.
  PHOTO (on the floor, boot-printed): two children on the Guild Mill's platform with a big man between them. On the back: "Da, Mari, Teo. AF 291."
[else] (A cellar under the house: a cold forge, wire, a map of the Lattice intake with the patrol times written in Marisol's hand. Two Bereaved are packing it into sacks.)
  [name: Bereaved] He said you'd come. He said you're all right. We're still not letting you through. (Battle: HOLLOW_GRUNT, single.)
  [name: Bereaved] (second, after the first) Teo's gone south. Don't ask where. (Battle: HOLLOW_GRUNT, single.)
  NOTE (pinned to the map): "Sis — they'll come here first. Don't lie for me. Don't stop lying for me either. Love to Ma. — T."
  PHOTO (on the forge's hood): two children on the Guild Mill's platform with a big man between them. On the back: "Da, Mari, Teo. AF 291."
  ITEM: NET BALL ×2 (in a sack). "Grey paint on them. Hollow-issue."
```

### The morning after (160; V124 == 4 → 5 on the first step outside the Center) [NEW]
```
(Morning. The river is running in from the sea on the morning tide, the way it's meant to. The blown intake is wrapped in Meridian canvas. The Guild Mill turns.)
[if :ch4_teo == :report]
  (Wanted posters on every post: a sketch of Teo, too handsome. "TEO REYES — WANTED — SABOTAGE OF THE MERIDIAN TIDAL LATTICE — REWARD ₽5000.")
  [name: Guild Striker] (tearing one down) He pulled Pella out of the race. Everybody knows. And somebody gave Meridian his name.
  [name: Guild Striker] (looking at you) ...Everybody knows that too.
  [name: Mrs Reyes] (on her step, arms folded, to nobody) The door's shut. It'll stay shut.
[if :ch4_teo == :keep_secret or :confront]
  [name: Mrs Reyes] (on her step) You. Ferry child. Here.
  (Received: SMOKED CHAR. "Wrapped in yesterday's Gale Post. Still warm.")
  [name: Mrs Reyes] From Marisol. She won't say it, so I'm saying it. Go and beat her. She needs to lose at something she can lose at.
(All:)
[name: Pella's Father] You dropped the gate. I saw. I saw you and— whoever it was.
[name: Pella's Father] There's no reward from me, I've nothing. Take this. It's the only thing on the boat that's worth anything.
(Received: BIG PEARL.)
[name: Pella] I'm not allowed on the water any more. Not even when it's stopped. ESPECIALLY not when it's stopped.
[name: Lock-keeper] Tidelock's open. Vote went seven halls to six: no strike, for now. The Warden didn't vote. She says a Warden doesn't. She went to the gym at five and she hasn't come out.
V124 = 5.
```
*Bersi in the Net Loft (168) [after S112]:* `[name: Bersi Gullsong] I'm already carving it: "The night the river died, and a stranger and a shadow hauled the gate." I don't know who the shadow was. A skald never checks his sources.`

## Maps 170–174 — Tidelock Gym (Gym 3; built per GYM_PUZZLES "The trim")
*Built and proven: the Lock Hall (170, practice lock, Tove the apprentice, Fisherman Gunnar), the Basins at low, mid and high water (171–173; Ingrid, Leif, Oskar, Bjorn; Tove's hints and reset), and the Warden's Pool (174, with Meridian's intake bolted into the lock wall). The Lock Hall door opens only at V124 >= 5.*
```
[CHANGED] Gym guide (170):
[name: Gym Guide] The Tidelock! Water-types, and the Water Surface field. Electric and Grass do well here. Fire doesn't. Fire never does, near a lock.
[name: Gym Guide] The puzzle's the lock itself. Raise the water and anything loose drifts inland, till the end of the channel or a shut gate stops it. Lower it and the chain winds the raft home. That's the whole job.
[name: Gym Guide] The Warden's been in since five. She's in a mood. A GOOD mood, mind. For Marisol, a fight's a good mood.
```

### 174 — the Warden's Pool: Marisol [CHANGED: replaces the built lines]
```
(The Warden's Pool: a lock basin full to the brim, timber galleries, and in the old stone wall a brass Meridian intake, humming. Marisol is standing on the lock gate's walkway with her sleeves rolled up. Her eyes are red. She's grinning anyway.)
[if :ch4_teo == :report]
  [portrait: MARISOL, neutral] You told them his name. Right. I've thought about it all night. I'd have done the same, maybe. If he weren't mine.
  [portrait: MARISOL, angry] I'm not going to throw this to make you feel bad. I'm going to win it to make ME feel better.
[if :ch4_teo == :keep_secret]
  [portrait: MARISOL, neutral] You kept your mouth shut last night. In Ebbmouth that's worth more than a badge.
  [portrait: MARISOL, smug] You're still not getting one free.
[if :ch4_teo == :confront]
  [portrait: MARISOL, neutral] You saw me at my worst last night. Swearing at a kitchen table with a teapot full of keys.
  [portrait: MARISOL, smug] Now come and see me at my best.
(All:)
[portrait: MARISOL, neutral] The Ebb runs both ways. Always has. Lately it can't decide.
[portrait: MARISOL, happy] My river, my rules. Water lifts what floats and drowns what doesn't. So float, kid!
Script: Prismfall.gym_battle(pfm_gym(:LEADER_MARISOL), double: false)     # LEADER_MARISOL, :WATER_SURFACE, cap 23, single
(When her ace enters:) [portrait: MARISOL, happy] Up you come, Lucky! They laughed at you on the docks too!
(LOSE: standard whiteout to the Pokémon Center. Marisol on retry: "Back in the water! That's the spirit. That's the ONLY spirit.")
(WIN:)
[portrait: MARISOL, shocked] ...
[portrait: MARISOL, happy] HA! Tides take it, you rode it both ways!
(Received: the TIDETURN BADGE.)
(The PC opens the Badge Case and sets the badge beside the other two. SE: the first note, the second, and then a third, low, under both of them, like a floor laid under a room.)
[portrait: MARISOL, shocked] ...Your box is singing.
[portrait: MARISOL, neutral] My da had a harmonium. Played three notes like that and called it a hymn. Never went to chapel in his life.
(Received: TM03 WATER PULSE.)
[portrait: MARISOL, happy] Water Pulse. Hits like a wave, leaves 'em seasick.
[name: Marisol] And that badge is the Guild's word, and the Accord's, that Pokémon up to level twenty-seven will heed you. Come up on the quay. I'm buying you an eel. I'm buying the whole quay an eel.
V124 = 6.
```

### EV "Pick One" (160, the quay by the eel stall, after Gym 3; autorun once) [NEW]
```
(Evening. Marisol and the PC on the quay's edge with their feet over the water, eating smoked eel out of newspaper. The Ebb runs out to sea, steady. For now.)
[portrait: MARISOL, neutral] Half this quay draws a Meridian wage. The other half fishes a river Meridian's drinking dry. Same families. Same kitchens.
[portrait: MARISOL, angry] Meridian pays my people. Meridian's killing my river. Pick one, kid. I dare you.
> The river.
  [portrait: MARISOL, neutral] Easy to say when it's not your people's wages.
> Your people.
  [portrait: MARISOL, neutral] Easy to say when it's not your river.
> I can't.
  [portrait: MARISOL, sad] No. Neither can I. That's the whole problem. That's why I swear so much.
[if :ch2_tamsin == :expose]
  [portrait: MARISOL, neutral] Briarwick's Warden signed with them, I hear. Then tore it up in front of her whole guild. Poor lamb.
  [name: Marisol] I'm not signing anything. I'm going to stand on this quay and swear till one of them blinks.
[if :ch2_tamsin == :help_confess]
  [portrait: MARISOL, neutral] Briarwick's Warden signed with them, I hear. Then walked into her guildhall, owned up to it, and made them rewrite the whole thing. Poor lamb.
  [name: Marisol] I'm not signing anything. I'm going to stand on this quay and swear till one of them blinks.
[if :ch4_teo == :confront]
  [portrait: MARISOL, sad] And I'd tell my little brother where the guards walk again. Every night. Don't look at me like that. You'd do it too.
[portrait: MARISOL, happy] Finish your eel. There's a woman at the Center with a box of papers asking for you, and she looks like she bites.
```

## Map 161 — Ebbmouth Pokémon Center: **EV "Larch's Tide Tables"** [CHANGED: replaces the built Larch event] — **key event 2**
*Plays on entering the Center after "Pick One" (V124 == 6). The built event's two lines become this scene.*
```
(Larch is at the corner table in her oilskin, salt in her grey braid, surrounded by rolled charts. A Gale Post satchel is on the floor. A pot of something brown and terrible steams beside her.)
[portrait: LARCH, neutral] There you are. Sit.
[portrait: LARCH, angry] No. First. You dropped a mill-race gate. At night. In Isenmar. During a Hollow sabotage. Four days after I said, in writing, "wear a hat".
[bubble: LARCH, angry, anger] This is LECTURE THREE. It has a DIAGRAM.
> You came all this way to tell me off?
  [portrait: LARCH, deadpan] I came all this way because of the river. Telling you off is on the way.
> I wore a hat.
  [portrait: LARCH, deadpan] You did not wear a hat.
> ...
  [portrait: LARCH, deadpan] Silence. Lovely. Your mother did that. It never worked on me either.
[portrait: LARCH, neutral] Drink this. It's disgusting.
(Received: a cup of kelp tea. You hold it. It holds you back.)
(She unrolls the first chart across the table and weighs the corners with sugar bowls.)
[portrait: LARCH, neutral] Tide tables. Ebbmouth, six months. Every stutter the Guild's logged since winter, by the minute. I've been collecting them by post.
[name: Larch] And this, on top: the tidal Lattice's draw, hour by hour. Don't ask how I got it. I trained half the linemen in Isenmar. Some of them still answer my letters.
(She lays the second sheet over the first. The paper is thin enough to see through. Every stutter sits exactly on a spike.)
[portrait: LARCH, sad] Every one. Every single stutter is a draw peak. On the hour, every hour they need the load.
[name: Larch] And last night. Midnight to five to one. That's the night export: Meridian runs the Lattice flat out while the Guild's asleep, fills the Prism Cells, and ships them south to the Concert of Regions on the night boats. The quarantine has an exemption for that. It always did.
[portrait: LARCH, neutral] The Hollow blew the intake at eight minutes to one. The river came back at eight minutes to one.
[portrait: LARCH, sad] They didn't stop your river, child. They started it.
[portrait: LARCH, neutral] All at once, in the dark, with a child on the water, because nobody looked. Both of those are true. That's the trouble with being right in a hurry.
WAIT 40.
[portrait: LARCH, sad] It's not the Hollow stopping the river. It's us.
[name: Larch] It's my design.
> Your design?
> You built it?
> ...
[portrait: LARCH, neutral] I was Meridian's Chief Engineer. The Lattice is mine. Pylon, intake, the cells, the switching. I drew the first one on a napkin in a Lumen tea-shop.
[portrait: LARCH, sad] I lit up this whole region, you know. Eleven cities on my design. And I think I'm killing it.
[name: Larch] I left them eight years ago. Don't ask me why yet. I'll tell you when I can say it without throwing something.
[portrait: LARCH, deadpan] Drink your tea.
> (Drink it.)
  [portrait: LARCH, shocked] ...You actually—
  [portrait: LARCH, deadpan] Don't tell anyone. They'll expect it of themselves.
  (The tea is warm, and vile, and you finish it. Somehow that's the worst part.)
> (Save it for later.)
  [portrait: LARCH, deadpan] That's what Kestrel says. He's had one "for later" since spring.
[portrait: LARCH, neutral] I'm going back to the Landing on the morning post-boat. Tidewatch doesn't run itself, and I need to put these somewhere Meridian doesn't read my letters.
[name: Larch] You go on up the Lock Road to Lumen. Rook Calder's the next Warden. Pretty boy, very loud, always being filmed. Try not to be filmed.
V124 = 7.
```
*(No portrait for Hesper: her letter is plain text.)*

### Chapter 4 close — 161 Gale Post desk, then 167 (V124 == 7) [NEW]
```
GALE POST DESK: A letter is waiting. No name on the envelope. The paper is cheap and heavy and smells of lamp-oil.
"Whoever you are —
stay away from my grandson.
Everyone who gets close to that boy's mother's ghost gets hurt."
(Unsigned.)
[portrait: LARCH, neutral] *(reading over your shoulder, because of course she is)* That's Hesper Vane's paper. She buys it from the Landing chandler by the ream and writes to nobody.
[portrait: LARCH, sad] ...Well. She wrote to you.
[if :ch4_kestrel_mourner == :kind]
  (A second note, folded small, pushed under the desk's blotter in a sharp hand:)
  "Ferry kid. Gone home. Gran wrote. Don't follow. — K.
   The eel was good. Don't tell anyone."
[else]
  [name: Nurse] Your friend in the black coat took the salt-sledge south at dawn. He left owing the eel stall for one eel. The eel stall's started a third page.
(Outside, 167 the Mill Quay: the towpath gate east is open. A gatekeeper leans on it.)
[name: Towpath Gatekeeper] The towpath east. The Reedholms, the Icecutters' Haul, the Locks, and up onto the Crownland. Lumen's four days on foot. Or one by airship, if you're rich. You're not rich.
SIGN: THE TOWPATH EAST — The Lock Road. The Reedholms · the Icecutters' Haul · Brassfall · the Icefall Locks · LUMEN CITY.
QUEST LOG: "Eighteen Roads" — Earn the fourth badge in Lumen City, up the Lock Road.
V102 STORY_CHAPTER = 5.
```
*(Kestrel goes home to the Ferrow Lighthouse because Hesper sent for him: that's where Interlude I finds him on the night of the Shatter, Ch5.)*

---

## Map events needed (Chapter 4)

For the map builders (these maps are built; this is what to add or change) and the owners named. "Once" = self switch A. V124 = **CH4_STEP** (design/FLAGS.md).

**566 Spinners' Rise** — Shepherd: add a second page (Kestrel line). Ribbon-tier: add a page after the Fleece Cross is read (the grey ribbon).

**577 Frostwick Pass** — [NEW] "Under the Arch": a touch strip in the Handfast Arch's gap, once. Toll hut ledgers: a second page. Hrodgar's intro and after lines (trainer event already placed by the trainer designer's round 4).

**570 Frostwick** — [NEW] arrival autorun at the East Gate (once; the huscarl and forester at the gate say it). Fishmonger: second page (Kestrel). Old woman by the brazier: third page (the mended shawl).
**571 Frostwick PC** — [NEW] Gale Post desk event: Juno's letter + Larch's note + KELP TEA BAG (once).
**573 The Two Hearths** — [NEW] the bard by the Isenmar hearth (the Sleeping Whale song; maps.json lists him). Half-Tally board as built (Trials).
**574 Rime-silk Loft** — weaver: one line after the gift.
**575 Border House** — [CHANGED] one event that runs the three clerks' exchange (a NULL on the scanner plate; three stamps).

**562 The Rimewood** — [NEW] "Cold camp" by the fallen giant (action; decor: three snow hollows, a dead fire, half a bark mask).
**578 Rimewood Path** — Lantern Birch: a second page (the note under the lamp).

**561 Gullcry Cliffs** — [CHANGED] K2 at (11,7): replace the built pages with the script (one pre-battle choice, the battle, the `:ch4_kestrel_mourner` choice). Sets S111, V124 = 1. Keep V114 = 1.

**160 Ebbmouth**
1. [NEW] Arrival autorun (once, entering from 561 with V124 == 1): a 90-frame river stop with every wheel frozen; V108 = 1; the quest-log line.
2. [CHANGED] Child with a toy boat → **Pella** (2 pages: before and after S112). [CHANGED] Lock-keeper: "gym shut, Warden at the vote" until V124 >= 5, then the morning-after line.
3. [NEW] Teamster, Meridian recruiter + poster (sign), Fishwife (the "Larch gets Meridian letters" line). [CHANGED] Guild organiser's second line (the war-levy).
4. [NEW] **"He Followed You Here"** at the eel-smoker's stall (13,29): touch, V124 == 1. Needs Kestrel's and Marisol's sprites; Kestrel hides behind the barrels. Sets V124 = 2. Eel-smoker: a page after it (the ledger).
5. **[CHANGED] "The Night the Ebb Stopped"** replaces the built "Teo" event at (29,31). Autorun on entering 160 from 167 with V124 == 3 (or after resting at the Center with V124 == 3). It needs: a night tone; Pella in a punt mid-channel (event sprite); three grey cowls at the intake (27,40) (one with shears: Thistle's sprite, no lines); a spark/explosion at the intake; the punt's move route down the channel to the race gate beside the Guild Mill (29,37); a double battle (two HOLLOW_GRUNT) on the towpath; Teo (HOLLOW_TEO v0) at the race gate's chain platform; the gate-drop SE; Marisol's Floatzel in the water; the Meridian guard; the `:ch4_teo` choice; Kestrel's arrival and exit. Sets S112, V108 2 → 1, V124 = 4.
6. [NEW] "The morning after" autorun (V124 == 4, the first step outside the Center): three variants by `:ch4_teo` (wanted posters as sign events, the Guild striker, Mrs Reyes on her step; or Mrs Reyes with the SMOKED CHAR); Pella's father (BIG PEARL); Pella; the lock-keeper. Sets V124 = 5.
7. [NEW] "Pick One" on the quay after Gym 3 (autorun once, V124 == 6, on leaving the gym).
8. Bersi (168 Net Loft): a page after S112.

**161 Ebbmouth PC** — [CHANGED] the built Larch event becomes **"Larch's Tide Tables"** (plays once on entering with V124 == 6; ends V124 = 7). Then [NEW] the Gale Post desk: Hesper's letter, then Kestrel's note (`:ch4_kestrel_mourner == :kind`) or the nurse's line.

**164 Reyes House** — [NEW] the night scene for `:confront` (Marisol at the kitchen table; the photograph on the dresser; CELLAR KEY), the short `:keep_secret` page (CELLAR KEY), and a locked-door page for `:report` until V124 >= 5. Mrs Reyes's day line: a page after S112 ("He hasn't come home. He'll come home.").
**166 Reyes Cellar [NEW map, in maps.json, ~17×13]** — the cellar door (164) opens with CELLAR KEY, or freely for `:report` after V124 >= 5. Two pages by `:ch4_teo`: the raid (two Meridian guards, the boot-printed photo), or the cell's rearguard (two HOLLOW_GRUNT singles, Teo's note, the photo, NET BALL ×2).

**167 Mill Quay** — [NEW] **"The Strike Vote"** autorun on entering with V124 == 2: a crowd (6–8 NPC events), Marisol on a barrel, Teo on the wheel platform, Mrs Reyes in the crowd, the bell SE, one stutter with the great wheel frozen. Sets V124 = 3. [NEW] the towpath gate east to 580 (shut until V124 >= 7; the gatekeeper and the sign). Aria's quest under the wheel as built.

**170–174 Tidelock Gym** — the Lock Hall door opens at V124 >= 5. [CHANGED] the gym guide (3 lines). [CHANGED] Marisol (174): the pre-battle lines by `:ch4_teo`, the ace line, the win, the TIDETURN BADGE, the third note (a 3-note SE), TM03. Sets V124 = 6.

**Cartographer (`tools/worldmap/world_data.py` → maps.json):** 160's NPC "Marisol's brother Tomas" and 166's "Tomas Reyes" are **Teo Reyes** (03_CAST). 167 connects to 580 by the towpath gate (Ch5).
**Items owner:** CELLAR KEY, SMOKED CHAR (Key Item / flavour food, heals like a Lemonade) are new. Badge name: the **Tideturn Badge** (creator, 2026-11-21).
**Trainer designer:** the two Ebbmouth `HOLLOW_GRUNT_M`/`_F` (the night, a double) and the cellar's two (singles) need Ebbmouth versions (version 0 is the Saltmere Pageant pair), Lv 20–22, Water/Dark/Poison with no Electric or Grass (Basculin, Buizel, Croagunk, Stunky). **HOLLOW_TEO v0** already exists (Carvanha, Arrokuda, Chewtle "Snapper"); please change its LoseText, because he is still masked when he loses and "Tell my sister—" gives the unmasking away a minute early. Suggested: "Not now — not NOW, it's jammed—". ("Tell my sister— no. Don't tell her anything." suits a later Teo version, after Ch4.)
