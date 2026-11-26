# Script: Chapter 3 — "The Weaver's Debt" (the Weavers' Road, Briarwick, Gym 2 and its aftermath)

> **Final playable script** for Chapter 3 (SPINE Revisions 8 and 14). It covers the Weavers' Road out of Saltmere's North Gate (541 the Grey Saltings, 544/545 Brinecut Mine, 552 the Dyers' Ford, 540 Thistledown Lea, 546/547 Thistledown Manor), the Gossamer Wood 524 and Woodward's Hut 526, Briarwick 120–125, the Loomhouse 130–131 (Gym 2), then the Gossamer Deepwood 525 and Cocoonfall Hollow 548. It follows `story/20_SCRIPT_CH0-2.md` (Prologue, Chapter 1 and Chapter 2 in Saltmere) and uses its conventions. Structure follows the built events in `mapgen/specs`; where this file adds an event, it is marked **[NEW]**. Map 552 is new (cartographer, `tools/worldmap/world_data.py`), so all of its events are new.
> Sources: 04_ACT_I (outline), 15_COMEDY (scene Ch3, inlined), NARRATIVE_KEYS (choice keys), FLAGS (switches), GYM_PUZZLES (Gym 2), DUNGEON_PUZZLES (D4 Brinecut, D5 Thistledown), CAMEOS §1 (Shelly), BALANCE 4b (versions).
> **Before Revision 14 this was Chapter 2.** Keys and switches keep their old names: `:ch2_tamsin`, `:ch2_matriarch`, `CH2_THISTLE_DONE`, `CH2_MATRIARCH_DONE` are all Chapter 3 now. Events must test Tamsin's badge by Warden (`pfm_gym_won?(:LEADER_TAMSIN)`), never `badge_count >= 1`: the player arrives here already holding Dorian's badge.

## Conventions
Same as `20_SCRIPT_CH0-2.md`: **Portrait use** per SPINE Rev 22 (`story/13_CUTSCENES.md`): `[portrait: NAME, expression]` faces for the cast (first line and expression changes; later lines `[name: X]` keep the face), the rare `[bubble: NAME, expression, emote]`, and `[name: X]` for everyone else (generic NPCs, trainers, the cameo Shelly), `> option` choices, `MOVE:`/`SE:`/`WAIT n`, `[after X]` reactive variants. Gym numbers are written for readability (Tamsin is 2); events call `Prismfall.gym_battle(pfm_gym(:LEADER_TAMSIN))`.

**Juno travels with the PC for this whole chapter** (placed events per map) until she leaves at the Cocoonfall Veil.

---

# CHAPTER 3 — "The Weaver's Debt"

**Chapter start:** V102 = 3, set at Saltmere's North Gate (end of Chapter 2). The road inland is the one Briarwick's cloth comes down: salt marsh, the dyers' river, the dead House Thistledown's meadows, then silk.

## Map 541 — The Grey Saltings (`:BEACH`; BGM: route theme, fuller)
```
ROAD SIGN: THE GREY SALTINGS — The Weavers' Road. ↓ Saltmere (North Gate) · ↑ The Dyers' Ford, Thistledown Lea & Briarwick. Mind the pans. The pans do not mind you.
(Salt pans to the horizon, white stacks, the smoke of the boiling-house, and a chalk cliff behind with a mine mouth in it.)
[portrait: JUNO, neutral] This is where Saltmere's salt comes from.
[name: Juno] "Grey" is the salt before it's washed.
[name: Juno] ...And the weather. It's mostly the weather.
```
Route trainers and flavor:
```
[name: Sailor] Salt barge went down in the mud in '88. Still there. Still salty. (Battle. After:) You're heavier than you look. In battle, I mean.
[name: Tuber Pip] My floaty is a Wailmer!
[name: Tuber Pip] No it's not. It's a floaty.
(Battle.)
[name: Tuber Pip] [after] Waaah! My floaty popped!
[name: Salt Raker] You're the ones from the Pageant? Everyone's heard.
[name: Salt Raker] The rakers say the Mourner's a Saltmere man.
[name: Salt Raker] The boilers say he's from Verdance. Nobody says it loud.
[name: Samphire Picker] Pick from the edges. The middle's the Plate's.
[name: Samphire Picker] Don't ask me what that means. My mother said it.
[name: Children building Sandygast castles] Don't step on that one! That one's ALIVE.
[name: Children building Sandygast castles] ...That one too.
[portrait: JUNO, happy] (at the bird hide) Squawkabilly! Four colors!
[name: Juno] In the wild they argue about which one's the real one!
HIDDEN ITEM (in the salt-barge wreck): BIG PEARL. "Salt-crusted. The barge kept it for twelve years and isn't happy about letting go."
```
**Optional: "The Crabrawler Ring"** (a comic boxing errand on the mudflat)
```
[name: Ring Boss] Crabrawler ring! Three bouts, no biting, best of three, winner gets the bucket!
(Three wild Crabrawler battles in a row, Lv per segment 1. After:)
[name: Ring Boss] Champion! Here's the bucket.
(Received: a bucket. It contains a KING'S ROCK.)
```

## Maps 544 / 545 — Brinecut Mine (optional; puzzle per DUNGEON_PUZZLES D4; `:CAVE`)
```
(A working salt mine: white salt walls, minecart rails, lamps every ten paces.)
[name: Salt Miner Ebb] Salt mine. Mind your tongue on the walls.
[name: Salt Miner Ebb] Everyone licks the walls once.
[name: Salt Miner Ebb] That's Dorian's badge on you? Good enough for salt. Here.
(Received: TM98 ROCK SMASH.)
[name: Salt Miner Ebb] It'll break rock for you once a second Warden's signed off on you.
[name: Salt Miner Ebb] Briarwick's, likely.
[name: Salt Miner Ebb] The Accord likes two opinions about smashing things.
[name: Hiker Holt] Three days I've been down here.
[name: Hiker Holt] Nobody told me it was a shortcut.
(Battle.)
[name: Hiker Holt] [after] It IS a shortcut? To WHERE?
[name: Black Belt Saul] I train in the salt. Builds character. Also thirst.
(Battle.)
[name: Black Belt Saul] [after] I need a drink. Not salt.
```

## Map 552 — The Dyers' Ford [NEW map] (`:MEADOW`; BGM: route theme, fuller)
```
ROAD SIGN: THE DYERS' FORD — The Weavers' Road. Briarwick Dye-Works. Do not drink the river. Do not bathe in the river. Do not stand in the red.
(Below three vat-sheds, the River Selvedge runs in three bands: madder red, woad blue, weld yellow. Cloth dries on lines across the road, so you walk under it like corridors.)
[portrait: JUNO, happy] The Briarwick dyers wash their cloth here, so the river runs in three colors!
[name: Juno] There's a fourth band nobody's allowed to dye. It's just water.
[name: Juno] People leave ribbons for it.
```
**EV "Meridian Surveyor"** (beside the first orange flag; the survey line runs from here up into the Gossamer)
```
[name: Meridian Surveyor] Mind the orange flags. Survey line for the new Lattice.
[name: Meridian Surveyor] Straight up the river and through to the wood.
[name: Meridian Surveyor] Trees aren't in the plan, but trees rarely are.
[portrait: JUNO, neutral] (at the first flag) These go right toward the Glasswood.
[name: Juno] That's...
(She stops. Two nights ago a man in a mask asked a theater why nothing in Verdance ever rots.)
[portrait: JUNO, sad] ...That's probably fine. Isn't it?
```
Route trainers and flavor:
```
[name: Dyer Morwenna] Red's my color! Red's everyone's color, eventually, if you work the madder vat. (Battle. After:) Look at my hands. They'll be red till Fallmorn.
[name: Dyer Ash] Woad blue. The Queen's Elowen green is woad and weld together.
[name: Dyer Ash] She's never paid for a yard of it.
(Battle.)
[name: Dyer Ash] [after] Bill her. Somebody bill her.
[name: Dye Foreman] Step the stones in the order I hum. Red, blue, yellow.
[name: Dye Foreman] No — that's blue, red, yellow.
[name: Dye Foreman] I've been humming it wrong for thirty years and nobody's told me.
[name: Smeargle owner] My Smeargle paints a mark on the boundary stone for every trainer who passes.
[name: Smeargle owner] Yours is... it's left yours blank.
[name: Smeargle owner] It's never done that.
[name: Shearer] Briarwick's dyers, Saltmere's salt, Ferrow's fish.
[name: Shearer] Every town in Elowen's got a thing the Plate gives it.
[name: Shearer] We've got colors. Lovely colors. You can't eat them.
HIDDEN ITEM (base of the third flag): ANTIDOTE. "A surveyor dropped it. He'll want it in about ten minutes."
BERRY TREE: Juno: "Pecha! Pick it gently. It bruises if you look at it wrong. Like Kestrel."
SHRINE OF THE FOURTH COLOR: A plain white ribbon tied to a stake at the edge of the undyed band. Dozens more are tied beside it. A card in a child's hand: "for the color nobody gets".
```

## Map 540 — Thistledown Lea (`:MEADOW`)
```
ROAD SIGN: THISTLEDOWN LEA — The lands of House Thistledown (extinct). ← The Dyers' Ford · → Gossamer Wood & Briarwick · ↑ Thistledown Manor (PRIVATE. DECEASED.)
[portrait: JUNO, happy] Mum says the Thistledowns were actors. All of them. Even the dog.
[name: Juno] They played Saltmere for a hundred years and then they all died in the same winter.
[name: Juno] People say they're still up there. Rehearsing.
[name: Juno] I'd like to see that. From a distance. A long distance.
[name: Drover] Race you to the fence!
(He wins. He always wins. He has a Ponyta.)
[name: Fisherman on the bridge] Bridge toll's a copper.
[name: Fisherman on the bridge] Nobody's collected it since the house died.
[name: Fisherman on the bridge] I just tell people. Habit.
[name: Mower] Nobody's mown the Lea in sixty years.
[name: Mower] You can't buy land off a dead family. They won't come to the door.
[name: Picnicker Ada's cousin] Ada beat me on Windfall Row last year.
[name: Picnicker Ada's cousin] I've been training on the Lea all spring.
(Battle.)
[name: Picnicker Ada's cousin] [after] ...I'll write to Ada. I'll lie.
HIDDEN ITEM (under the bridge): GREAT BALL. "It's been here long enough to grow moss."
```
*[after S106]* `[name: Mower] Woman in grey came through at dawn with two others. Shears in her belt. Nodded to me. Mannerly. Went toward the wood.`

## Maps 546 / 547 — Thistledown Manor (optional haunted house; puzzle per DUNGEON_PUZZLES D5; field `:HOLLOW_CATHEDRAL`) — **Game over `GO_CURTAIN_CALL`**
```
(A sagging manor on the Lea's hill. Every window is lit. Inside: dust sheets, candles, and voices rehearsing.)
[portrait: JUNO, panic] [emote: sweat] I'm going to wait outside.
[name: Juno] I'm going to wait outside and be very supportive from outside. *(sweat drop)*
[name: Fenwick] *(bows)* The Players are rehearsing. Do come in.
[name: Fenwick] Do not, under any circumstances, do anything you are asked.
(Dame Rosamund Thistledown, the matriarch-ghost, sweeps out in a ruff.)
[name: Dame Rosamund] A visitor! An AUDIENCE! No — better! An ACTOR!
[name: Dame Rosamund] We're one short for the second act. Our Laertes passed on. Again.
[name: Dame Rosamund] Three scenes, darling. Hit your marks, say your lines.
[name: Dame Rosamund] Miss them, and the company gets... restless.
[name: Dame Rosamund] We heard there was trouble at the Lantern two nights ago.
[name: Dame Rosamund] Somebody stopped the show. *(a shudder that blows out three candles)* Unthinkable. Nobody stops the show.
```
**Scene 1, the Battlements**
```
[name: Ghost of the Old King] Remember me!
> "I will remember you." → The Old King bows and fades, satisfied.
> "Who are you again?" → [name: Ghost of the Old King] FORGOTTEN?! (Ghost battle.)
```
**Scene 2, the Play Within the Play**
```
[name: Player Queen] The lady doth protest too...?
> "...much, methinks." → The Player Queen curtsies.
> "...loudly." → [name: Player Queen] That is NOT the line! (Ghost battle.)
```
**Scene 3, the Graveyard** (a Yamask is holding up its mask)
```
[name: Gravedigger] Here's a mask. Whose was it?
> "Alas, poor Yamask. I knew him." → The Yamask is so delighted it nearly drops its own face.
> "That's just a mask." → [name: Yamask] *(furious crying)* (Ghost battle.)
```
**Attic (547), after the third scene**
```
[name: Dame Rosamund] Bravo. BRAVO. Darling, you have it. The thing.
[name: Dame Rosamund] We've been rehearsing for sixty years and never had it.
(Received: SPELL TAG, and a LITWICK that has been watching from the chandelier. "It wants to see the second act.")
Switch S176 THISTLEDOWN_CLEARED = ON.
Script: Prismfall.checkpoint     # NARRATIVE_KEYS §10: the attic stairs, before the offer
[name: Dame Rosamund] Stay. Join the company. Forever.
[name: Dame Rosamund] The run never closes here, you know. Not ever.
[name: Dame Rosamund] Nobody here has ever stopped a show.
(Behind her, Fenwick the butler mouths a single word, very slowly: *don't*.)
> Thank you, but I have a gym to get to.
  [name: Dame Rosamund] *(sighs)* They always do.
  [name: Dame Rosamund] The good ones always have somewhere to be.
> I'd love to.
  [name: Dame Rosamund] Wonderful! Wonderful! Places, everyone!
  [name: Fenwick] *(very quietly)* Oh, dear.
  (Fade. The candles all go out at once. When they come back up, the PC is on the attic stage in a ruff, and the dust sheets are an audience.)
  Script: Prismfall.game_over(:GO_CURTAIN_CALL)
```

## Map 524 — Gossamer Wood (`:SILKWOOD`; BGM: harp and wood-flute)
```
(Huge old trees hung with silver silk. The looms' clacking carries from far off. The orange survey flags go in ahead of you.)
FIELD NOTES pop-up: "SILKWOOD — Bug moves bite deeper. Webs slow the careless. Fire here is rude and effective."
[portrait: JUNO, happy] Silk-moths!
[name: Juno] The Insect Plate's somewhere under Briarwick, and it makes the silk never tangle. Ever!
[name: Juno] You could knot it for a week!
[name: Silk-picker] Don't cut the low strands, they're this year's.
[name: Silk-picker] Cut the high ones. No, higher.
[name: Silk-picker] No— you know what, I'll do it.
[name: Bug Catcher Twins Mo & Jo] We battle together!
(Double battle.)
[name: Bug Catcher Twins Mo & Jo] [after] We lose together.
[name: Bug Catcher Twins Mo & Jo] (again) The Warden fights in twos too. Twins taught her.
[name: Bug Catcher Twins Mo & Jo] That's not true. We say it anyway.
[name: Old Weaver resting] Sixty years I've walked this wood.
[name: Old Weaver resting] This spring it rings. Hear it? East.
[name: Old Weaver resting] Like someone tapping a glass.
SHRINE STONE (small, mossy): A carving of three beasts chasing a masked figure. Someone has left a honey bun in front of the masked one, not the three.
[portrait: JUNO, neutral] (at the shrine stone) That's the Pageant. That's the play we saw.
[name: Juno] ...Somebody likes the Ogre better.
HIDDEN ITEM (in a web): NET BALL ×2. "The web gave them up without a fight."
BLEED VEIL (east edge, a shimmer between two trees; beyond it the trunks are clear crystal):
  [portrait: JUNO, sad] That's the Glasswood.
  [name: Juno] It was three fields away at midwinter.
  (Entering leads to Cocoonfall Hollow through the Deepwood; blocked by a Cut tree. The Cutter in Briarwick gives Cut after Tamsin's badge.)
ACCORD CORDON (south lane, from the wood's side): The forest road back to Windfall Row and the Landing, taped off. A sign faces the farms: CLOSED BY ORDER OF THE ACCORD. From this side you can see the glass across the lane, a mile on.
  [portrait: JUNO, sad] That's the way I used to come. Four hours with Parsnip.
  [name: Juno] Now it's two days and a pageant.
```
**Woodward's Hut (map 526)**
```
[name: Woodward] Past my hut it's all glass, east.
[name: Woodward] I've stopped chopping. You can't burn it and it cuts the axe.
WOODWARD'S HUT bookshelf: "Tally of the east trees. Midwinter: 0 glass. Thaw: 40. Spring: 300. I have stopped counting. — W."
(Received from the Woodward: 3 POTIONS. "For whatever you think you're doing.")
BED (action): You could rest here. (Heals the party.)
```

## Map 120 — Briarwick (BGM: looms as percussion, fiddle)

### Arrival (autorun, first entry)
```
(A village lashed between tree trunks: rope bridges, treetop houses, bolts of silk drying like flags. At the east edge, orange survey flags march to a half-built brass pylon.)
[portrait: JUNO, happy] Briarwick! Smell that?
[name: Juno] That's mulberry and lanolin and— oh, the egg-seller's open.
[name: Juno] I'll find you at the gym!
[name: Juno] Don't start without me! Or do! I'll catch up!
MOVE: Juno runs off north. (She stops following.)
```

### Named residents
**Tamsin Loom** (first meeting, in the square, carrying too many bolts of silk)
```
MOVE: Tamsin walks into the PC. Silk everywhere. *(shock lines)*
[portrait: TAMSIN, panic] [emote: jolt] Sorry! Sorry — I wasn't — are you hurt?
[name: Tamsin] You're not hurt. Sorry.
[name: Tamsin] You've a Badge Case. Oh. Oh no.
[name: Tamsin] You're a challenger. TODAY?
[name: Tamsin] And that's Dorian's badge. You beat Dorian. *(shock lines)*
[name: Tamsin] Dorian makes everyone feel like they won even when they lose.
[name: Tamsin] Did he cry?
> He cried.
  [portrait: TAMSIN, happy] He always cries.
  [name: Tamsin] He cried at my grandmother's funeral. He cried at the wake.
  [name: Tamsin] He cried at the reading of the will, and he wasn't in it.
> ...
  [portrait: TAMSIN, happy] He cried. You don't have to say. He always cries.
[portrait: TAMSIN, panic] It's fine! It's fine. The gym's open.
[name: Tamsin] It's just a bit— the moths are— there was a meeting.
[name: Tamsin] I'm Tamsin. Loom. The Warden. Since spring.
[name: Tamsin] Come to the Loomhouse when you're ready.
[name: Tamsin] Take your time. Please take your time.
MOVE: Tamsin gathers the silk and hurries east, toward the pylon, not the gym.
```
**Guildmistress Hett** (Weavers' Guildhall, map 123)
```
[name: Hett] Old Mother Loom ran this guild forty years and never once missed a moth-count. The girl's missed three.
[name: Hett] I'm not saying she's hiding something.
[name: Hett] I'm saying the ledger's locked and it never used to be.
```
*[after Tamsin's badge]* `[name: Hett] She signed WHAT? Alone? ...Poor fool child. Her gran would've made the whole village sign it with her, and then it'd be all our fault. That's what a guild's FOR.`

**The Moth-keeper, Alder Finch** (grove fence)
```
[name: Finch] Fourteen dead this week.
[name: Finch] They fly east at dusk and come back with glass on their wings.
[name: Finch] Then they don't come back.
[name: Finch] Meridian says the Lattice will "stabilize" it.
[name: Finch] The line they've drawn for it goes straight through my grove.
```

### Flavor townsfolk
```
[name: Weaver at loom] Clack-clack. Sixty picks a minute.
[name: Weaver at loom] Don't talk to me on the downstroke.
[name: Weaver at loom] (again) That was the downstroke.

[name: Dyer] Elowen green, that's my vat. The Queen's own shade.
[name: Dyer] She's never paid for a yard of it.
[name: Dyer] "The Crown's by right of soil," says the taxman.
[name: Dyer] So's the mud, I said.

[name: Apprentice] I wove my first scarf! It's got eleven mistakes.
[name: Apprentice] Tamsin found a twelfth and then apologized for an hour.

[name: Rope-bridge Boy] If you jump on the bridge it goes BWOING.
[name: Rope-bridge Boy] I'm not allowed. You're a grown-up. YOU do it.
  > Jump.  → SE: bwoing. [name: Boy] HA!  [name: Voice below] WHO'S JUMPING?!
  > Don't.  → [name: Boy] Coward.

[name: Grandmother knitting] It's a jumper for my Caterpie. Sixteen sleeves.
[name: Grandmother knitting] I'm on the fourth. Don't rush me.

[name: Silk Merchant] Briarwick silk never tangles and never rots.
[name: Silk Merchant] That's why nobody ever buys a second one.
[name: Silk Merchant] Terrible business. Wonderful product.

[name: Meridian Linesman] Pylon'll be humming by month's end. Free light for the looms!
[name: Meridian Linesman] Folk here look at me like I'm selling plague.
[name: Meridian Linesman] (again) Truth is, I don't know what it does to the wood.
[name: Meridian Linesman] I just bolt the brass.

[name: Tired Mother] Three nights running somebody's cut the survey flags.
[name: Tired Mother] I'm not saying who.
[name: Tired Mother] I'm saying I slept very well through it.

[name: Old Man on bridge] The Loyal Three drove the Ogre out of this wood.
[name: Old Man on bridge] My grandfather told me. His grandfather told him.
[name: Old Man on bridge] Nobody's grandfather SAW it, mind.

[name: Girl in ogre mask] RAAH! I'm the Gossamer Ogre!
[name: Girl in ogre mask] I steal children and eat looms!
[name: Boy in dog mask] And I'm a Loyal Hound and I bite you!
[name: Boy in dog mask] ...Why does the Ogre mask look sad?

[name: Egg-seller] Silk-moth eggs, a copper each.
[name: Egg-seller] That loud girl in the flowers bought forty. FORTY.
[name: Egg-seller] For her uncle, she says. In a hatbox.

[name: Tax-barge Deserter] I rowed the Queen's tax-barge.
[name: Tax-barge Deserter] Jumped off at Saltmere when they booed us. You've heard them?
[name: Tax-barge Deserter] Then you know. Weaving's quieter. Nobody boos a scarf.

[name: Accord Chaplain] The chapel's open. The mural's older than the looms.
[name: Accord Chaplain] Mind the Crown in it — people say it's painted wrong.
[name: Accord Chaplain] It isn't. It's painted *before*.

[name: Youngster] The Warden cries in the gym at night.
[name: Youngster] I heard her through the wall. Then she apologized to the wall.

[name: Woman with basket] East wood rings like a bell now.
[name: Woman with basket] My mother says a ringing wood means a wedding.
[name: Woman with basket] I don't think this is a wedding.

[name: Cutter's Wife] You'll want my husband if there's a tree in your way.
[name: Cutter's Wife] He'll say no first. He always says no first.
[name: Cutter's Wife] Wait for the second answer.

[name: Bun-seller] A boy in a black coat came through yesterday asking about masks.
[name: Bun-seller] Who carves them, who wears them, who doesn't take them off.
[name: Bun-seller] Rude. Bought a bun. Went north.
```
*[after gym, village-wide variants]*
```
[name: Weaver at loom] She told us. All of it, or you did.
[name: Weaver at loom] Either way the looms stopped for a whole minute.
[name: Weaver at loom] First time since the funeral.
[name: Dyer] Contract's a contract, says the linesman.
[name: Dyer] So's a pitchfork, says I.
[name: Tired Mother] Still sleeping well.
```
*[after S107 Matriarch]* `[name: Finch] The ringing's stopped. The moths flew east at dusk and came back clean. Whatever you did in there: thank you. And don't tell me. I don't want to know.`

### Signs and objects
```
TOWN SIGN: BRIARWICK — Where the Thread Never Tangles. (Carved under it, smaller: "Unlike the Guild Accounts.")
LOOMHOUSE SIGN: LOOMHOUSE GYM. WARDEN: Old Mother Loom (painted over) TAMSIN LOOM. "A thread holds because it's twisted with others."
FESTIVAL POSTER (square): The same poster as the Landing and Saltmere. Here the dark fleck in the Crown's stone has been circled in charcoal. Someone has written: "SEE CHAPEL."
PYLON (east edge): Half a brass pylon. A plate reads: MERIDIAN CONCORD — LATTICE 15 (BRIARWICK) — "Light for Everyone." It is faintly warm, and the grass around it is stiff, like spun sugar.
SURVEY FLAGS: Orange cloth on stakes. Four of the stakes have been neatly cut. The cuts are very clean. A weaver's shears. (You saw ropes cut like that in the Lantern Theatre.)
OGRE MASK STALL: Carved bark masks for Fallmorn, rows of them. Every one has the same sad face. "That's how the Ogre looks," says the carver. "Always has." You've seen that face before, stepping out of a painted sky in Saltmere.
SILK RACKS: The silk moves in no wind at all.
HIDDEN ITEM (under the rope bridge): X ATTACK. "It fell out of someone's pocket mid-bwoing."
HIDDEN ITEM (behind the dye vats): TINY MUSHROOM. "Dyed Elowen green. Still a mushroom."
```

### EV "Old woman at the shrine" (S170; north edge, the Loyal Three shrine) — disguised Celestine
```
(A stone shrine: three carved beasts, a dog, a monkey and a pheasant, standing over a broken ogre mask. An old woman in a grey shawl is sweeping it. She is barefoot.)
[name: Old Woman] Three loyal hounds and an ogre so bold...
[name: Old Woman] ...but who was the thief, when the story was told?
> Who was?
  [name: Old Woman] Oh, I couldn't say.
  [name: Old Woman] I could *sing* it, but I couldn't say.
> That's not how the Pageant tells it.
  [name: Old Woman] No. The Pageant's had it that way since AF 140.
  [name: Old Woman] Somebody stood up and said otherwise, I hear, in Saltmere.
  [name: Old Woman] Good for somebody.
> ...
  [name: Old Woman] Quiet. Good. You'll hear more that way.
  [name: Old Woman] Most of it's under the floor.
[name: Old Woman] You've no color on you, child. Did you know?
[name: Old Woman] Like water in a glass.
[name: Old Woman] Walk carefully. Eighteen roads is a long way, and people will want to carry you.
(She goes back to sweeping. After Tamsin's badge she is gone; a single dusk-colored flower lies on the shrine. S170 OFF.)
ITEM: DUSK PETAL. "It's only open at twilight. It's open now. It's noon."
```

### Sidequest A — "Sixteen Sleeves"
```
(Grandmother knitting, second talk:)
[name: Grandmother] I've run out of green. The dyer won't sell me less than a bolt.
[name: Grandmother] Fetch me three Tiny Mushrooms from the wood and I'll boil my own.
QUEST LOG: "Sixteen Sleeves" — Bring three Tiny Mushrooms (0/3).
(On delivery:)
[name: Grandmother] Lovely. Smells dreadful.
[name: Grandmother] Here, I made this one first. It was meant for a Weedle.
[name: Grandmother] He evolved. Ungrateful.
(Received: SILK SCARF. "Two sleeves. A Kakuna has no use for it.")
(Post-game epilogue hook: a Caterpie in a sixteen-sleeved jumper walks through the square.)
```

### Sidequest B — "The Locked Ledger" (leads into the main reveal; optional early clue)
```
(Guildmistress Hett, second talk:)
[name: Hett] You're a stranger, so you can do what I can't.
[name: Hett] The guild ledger's in the Warden's loft and it's locked.
[name: Hett] Old Mother Loom kept the key in the gym.
[name: Hett] "Where the first thread starts," she used to say.
QUEST LOG: "The Locked Ledger" — Find the ledger key in the Loomhouse.
(Gym lobby, Mother Loom's first loom, action:) A small brass key is tied into the very first warp thread. (Received: LEDGER KEY.)
(Weavers' Guildhall loft:) LEDGER, last page: "Received of the Meridian Concord, for stewardship rights, Lattice 15: ₽400,000. Signed, T. Loom, Warden." One signature. The line for "Guild witnesses" is blank.
(Return to Hett before the gym:) [name: Hett] ...Alone. She signed it alone. Don't say anything yet. Let me think how to say it kindly. I'm out of practice.
(Reward after the chapter: ₽2000 and TM STRING SHOT, "from the guild's teaching chest".)
(If the player found the ledger first, Tamsin's confession scene opens with: [portrait: TAMSIN, sad] "You've read it. Hett has too. I can tell by how gently she's speaking to me.")
```

## Maps 121–125 — Briarwick interiors
```
POKÉMON CENTER:
[name: Nurse] We heal for free. The scanner at the door is new.
[name: Nurse] It told me I'm "Insect, Briarwick".
[name: Nurse] I've lived here forty years, I'd worked it out.
[name: Trainer] The gym's all webs. Step on the wrong one and it throws you into the net.
[name: Trainer] Tamsin apologises to you all the way down.
[name: Trainer 2] She fights two at once. Two!
[name: Trainer 2] Bring a partner that likes company.
GALE POST DESK [NEW]: A letter is waiting. "Lecture Two is now two lectures. Do not make me send them both. Eat something. — I.L." (Received: POTION ×2, and a second tea bag. "You have two now. That's a collection.")

MART:
[name: Clerk] Antidotes go fast here. The moths don't mean it.
[name: Customer] I asked for a Synthetic Seed and the old ladies in the queue went silent. I put it back.

TREETOP HOUSE (map 124):
[name: Retired Weaver] I wove Old Mother Loom's shroud.
[name: Retired Weaver] She'd picked the pattern at thirty. "Plan ahead," she said.
[name: Retired Weaver] Tamsin plans ahead too. She plans for everything to go wrong.
BOOKSHELF: "A Child's Pageant of the Loyal Three." The last page, where the Ogre is driven out, has been torn away. Someone has drawn the Ogre a little house instead.

CHAPEL [exterior door on map 120; interior tile set in 124's second room]:
MURAL: Eighteen colored stones falling from a white sky into green land. Above them, a silver crown with one clear stone. The stone is whole.
[name: Child in pew] Mum says the Crown got hurt once.
[name: Child in pew] She says don't ask the chaplain. So I'm asking you.
WINDOW: Eighteen panes of colored glass around one clear pane. The clear one has no lead around it, as if it were added first.

CUTTER'S HOUSE (map 125):
[name: Cutter] No.
[name: Cutter] (again) ...What's the tree?
[name: Cutter] (before Tamsin's badge) Saltmere's badge? That's a theater ticket.
[name: Cutter] Come back with ours. I don't hand Cut to people the wood hasn't met.
[name: Cutter] (after Tamsin's badge) Right. Here. Cut the dead ones.
[name: Cutter] If you cut a live one I'll know. I won't know how. I'll just know.
(Received: HM01 CUT.)
```

## Map 120 — **EV "Pallbearer Thistle"** (night event at the pylon; triggers when the PC approaches the pylon after meeting Tamsin)
```
(Night. Two grey-cowled figures in carved bark masks are cutting survey stakes. A third, a woman with weaver's shears in her belt, stands at the pylon with a hand flat on the brass.)
[name: Bereaved] That's the last of the south line.
[portrait: THISTLE, neutral] Leave soil where they stood. Bare.
[name: Thistle] Let something rot there for once.
MOVE: The PC steps on a twig. SE: snap. *(shock lines)* ×3.
[portrait: THISTLE, angry] [emote: exclaim] A watcher. Meridian's, or the Warden's?
> Neither.
  [portrait: THISTLE, angry] Everyone's somebody's.
  [name: Thistle] You just haven't been told whose yet.
> Who are you?
  [portrait: THISTLE, angry] The Hollow.
  [name: Thistle] We mourn what this land was. Somebody has to.
> ...
  [portrait: THISTLE, angry] No answer. Then I'll assume the worst. It saves time.
[portrait: THISTLE, neutral] ...I know you. You were in the stalls at the Lantern.
[name: Thistle] The one he looked at.
[name: Thistle] I cut the ropes that night. Nobody was hurt.
[name: Thistle] I'm a weaver, child. I know where a thread will fall.
[name: Thistle] I was a weaver once. Lowmarsh.
[name: Thistle] You won't find it on a map now. It had looms too.
[name: Thistle] He told the whole theater to ask their Warden.
[name: Thistle] I'll tell you what to ask yours. Ask her what she signed!
BATTLE: HOLLOW_THISTLE "Thistle", version 0 (her first battle; named admins count rematches from 0, BALANCE.md 4b). Field: Silkwood (map default). (Hollow admin 1; can't be fled.)
(WIN:)
  [portrait: THISTLE, shocked] ...Your partner doesn't fight like the Wood's got hold of it.
  [name: Thistle] It fights like it's standing nowhere at all.
  [name: Thistle] Let the land grieve, child.
  [name: Thistle] And look at the grass by that pylon in daylight.
  MOVE: The three vanish into the trees, north. A bark mask is left on the ground.
  ITEM: BARK MASK. "Carved to look like the Gossamer Ogre. It does look sad. It's the face from the Pageant."
Switch S106 CH2_THISTLE_DONE = ON.
```

## Map 130 — Loomhouse Gym, Lobby (Gym 2; the weavers' hall at the foot of the elder; no puzzle; GYM_PUZZLES Gym 2)
*(SPINE Revision 19: the weaver touches stay down here. The gym itself is up the stair, in the hollow of the elder: the Canopy, 131.)*
```
[name: Gym Guide] Challenger! This is the Loomhouse.
[name: Gym Guide] Bug-types, and the Silkwood field.
[name: Gym Guide] Fire and Flying do well. Grass does not.
[name: Gym Guide] I say this to everyone and half of them bring a Bulbasaur.
[name: Gym Guide] The gym's up the stair, in the hollow of the elder itself.
[name: Gym Guide] Tamsin's Bug Pokémon have strung it with webs.
[name: Gym Guide] Step on a tight one and it throws you, three good bounds, the way you stepped on.
[name: Gym Guide] Step on a sticky one and it keeps you.
[name: Gym Guide] The Joltik up there feed on the strands.
[name: Gym Guide] When one sparks, every web on its strand changes its mind.
[name: Gym Guide] And Tamsin fights two at a time.
[name: Gym Guide] A thread holds because it's twisted with others.
[name: Gym Guide] Old Mother Loom never once went up there. Said the Bugs had better hands than hers.
[name: Gym Guide] Tamsin added the safety nets. And the apology cards.
[name: Weaver Tibb] The looms down here are Granny Loom's.
[name: Weaver Tibb] The webs up there are the Bugs'.
[name: Weaver Tibb] Tamsin says that's the difference between a weaver and a Warden:
[name: Weaver Tibb] a weaver makes cloth, a Warden makes room for things to make themselves.
APOLOGY CARD (pinned by the stair): "The gym is UP. If a web throws you somewhere silly, the nets are soft. Sorry! — T.L."
PORTRAIT (wall): A fierce old woman at a loom. Brass plate: "Mother Loom, Warden AF 247–299. 'Twist it or lose it.'"
FIRST LOOM (action): Mother Loom's first loom. The warp stops mid-row: up, down, up, down, up — and then nothing, as if she meant to come back to it.
  (During "The Locked Ledger":) A small brass key is tied into the very first warp thread. (Received: LEDGER KEY.)
```
**Comedy scene Ch3, "The Apology Spiral"** (Tamsin is in the lobby the first time, re-threading a loom)
```
[portrait: TAMSIN, panic] Sorry — the gym's a bit tangled today — sorry —
> It's fine.
  [portrait: TAMSIN, panic] [emote: sweat] Sorry for saying sorry so much. That's annoying.
  [name: Tamsin] Sorry. *(sweat drop)*
> Stop apologizing.
  [portrait: TAMSIN, shocked] [emote: jolt] Right! Yes! Sorr— *(shock lines)*
  [name: Tamsin] I nearly did it again. I'm so sorry.
[portrait: TAMSIN, shocked] ...
[portrait: TAMSIN, deadpan] I'm going to go and stand in the web now.
MOVE: Tamsin goes up the stair into the tree.
```

## Map 131 — Loomhouse Gym, the Canopy (the hollow of the elder; web trampolines; variables V305–307 `CANOPY_WEB_A/B/C`, the Loomhouse's IDs since before the swap)
*(Layout and rules: GYM_PUZZLES Gym 2 §131. A taut web throws you three tiles the way you stepped on; a sticky web stops you; nothing under you means the net. The climb: the floor → ledge 1 → ledge 2 → the sticky turn → ledge 3 → the Joltik perch and back → Tamsin's ledge.)*
```
(First entry. The stair comes up into the hollow of the elder. Inside it's as tall as a cathedral and full of webs: silver drum-tight ones, sagging yellow ones beaded with dew, and far overhead a ledge with a lantern on it. Moths drift across the drop. Something small and yellow crackles along a strand.)
CARD: WEBS (on a twig at the foot of the hollow): "Tight webs THROW you, three bounds, the way you step on. Mind which way you're facing. — T.L."
[name: Pim] Pim. I mind the nets. Want the Joltik calmed down, or a nudge?
  > A nudge. (one hint per ask)
    [name: Pim] A Joltik's spark runs the whole strand.
    [name: Pim] Look at which webs hang on each one.
    [name: Pim] Up there you want to go up, stop, then go across.
    [name: Pim] Taut throws, sticky stops.
    [name: Pim] Spark both Joltik, once each: the one on the third ledge and the one on the west perch.
    [name: Pim] Then the bottom web throws you up, the middle one holds you, and the top one throws you across to Tamsin.
  > Calm the Joltik. (reset: V305–307 = 0, back to the foot of the hollow)
    [name: Pim] *(clicks his tongue; somewhere above, a Joltik yawns)* There. Every strand as Tamsin left it.
FALL (a web throws you onto nothing): ...and nothing there to land on. You drop into Tamsin's safety net, far below.
  The net lowers you, very gently, all the way back to the bottom of the hollow. A card is pinned to it: "Sorry! — T.L."
SPINARAK (floor): The Spinarak is spinning a very small web. It is very proud of it.
SWADLOON (by the stair): The Swadloon is wrapped in leaves for the night. It's the middle of the afternoon.
```
**Juno** (at the foot of the hollow, once the PC has beaten a trainer in here; she's holding a hatbox with great care)
```
[portrait: JUNO, happy] Forty eggs! In a hatbox! Don't knock the hatbox!
[name: Juno] And don't fall on me!
[name: Juno] Go on, I'll be loud. Quietly. I learned that in Saltmere.
(again:) [bubble: JUNO, happy, exclaim] *(a whisper you can hear from the top of the tree)* GO ON, \PN!
```
**Ledge 1** (one web, straight up from the floor)
```
LEAVANNY: Leavanny is tailoring a challenger's cloak out of leaf and silk. It holds the leaf up against you, decides you're the wrong colour, and starts again.
[name: Bug Catcher Nell] (optional) A thread alone is just string!
(Battle.)
[name: Bug Catcher Nell] [after] Two of us would've had you.
```
**Ledge 2** (a web that throws you onto a web; Orla watches the landing, so her battle can't be skipped)
```
[name: Lass Orla] Mind the webs. I bounced into the net twice.
[name: Lass Orla] It's very comfortable.
(Battle.)
[name: Lass Orla] [after] ...I'm going back to the net.
CARD: STICKY: "Sticky webs keep you. You can step off one any way you like. That's how you turn round up here. — T.L."
SEWADDLE: The Sewaddle is wearing a leaf hood that Leavanny made. It doesn't fit. It won't take it off.
```
**Ledge 3** (up through the sticky turn; the two webs either side of the first sticky web, and the one beside the start, throw you into the drop)
```
CARD: JOLTIK: "The Joltik eat the current in the strands. Spark one and every web on its strand changes. Gold strand here, blue strand on the perch. Sorry about the zaps. — T.L."
JOLTIK (ledge 3, gold strand / the west perch, blue strand): The Joltik sparks! The charge runs the whole gold (blue) strand, and every web hanging on it flips: slack snaps taut, taut sags slack.
KAKUNA: The Kakuna hangs from the deck by one thread. It does not appear to mind.
```
*(The obvious move is the trap: spark only the gold Joltik and the bottom two webs both go taut, so they throw you straight up the trunk and into the net. Spark both, once each: up, stop, across.)*
**Tamsin's ledge**
```
[name: Gentleman Bram] (optional) Granny Loom taught me the looms.
[name: Gentleman Bram] Tamsin taught me the webs. I prefer the looms.
(Battle.)
[name: Gentleman Bram] [after] They don't throw you, you see.
STAIR (behind Tamsin, before the badge): A silk rope across the stair, and a card: "Upper lofts: Gran's old practice rooms. After your badge. Sorry! — T.L."
```
**Warden battle** (double)
```
(Tamsin stands at the top of the hollow, among the webs. She has stopped fidgeting.)
[portrait: TAMSIN, neutral] Gran wove the looms downstairs. She never came up here.
[name: Tamsin] She said the Bugs had better hands than hers, and she was right.
[name: Tamsin] She held this village together for fifty years with thread and shouting.
[name: Tamsin] I've had it since spring. I can't shout.
[name: Tamsin] Dorian goes first because he makes people brave.
[name: Tamsin] I go second because by then you think you know what a gym is.
[portrait: TAMSIN, angry] But I can hold a thread. So can they.
[name: Tamsin] We spun this whole hollow together, the Bugs and me.
[name: Tamsin] Don't you dare tear it.
Script: Prismfall.gym_battle(2)     # LEADER_TAMSIN, :SILKWOOD, cap 19, DOUBLE battle (GYMS double: true)
(When her ace enters:) [portrait: TAMSIN, neutral] Twist with me. Hold.
(LOSE: standard whiteout to the Pokémon Center. Tamsin on retry: "Again? Good. I mean— sorry. I mean good.")
(WIN:)
[portrait: TAMSIN, happy] ...It held, and you still came through it.
[name: Tamsin] That's allowed.
[name: Tamsin] Gran said a good web always leaves one way through, for the right one.
[name: Tamsin] I didn't think I'd ever meet one.
(Received: the WEFT BADGE.)
(The PC opens the Badge Case and sets the badge beside Dorian's. SE: the first note, then a second, higher, in tune with it. The two hang in the air together. *(music note)* over Juno.)
[portrait: JUNO, shocked] [emote: music] It's doing a CHORD. *(shock lines)*
[name: Tamsin] I don't think they do that. ...Do they do that?
[name: Juno] It did one note in Saltmere!
[name: Juno] Dorian asked it to do it again and it wouldn't!
[name: Tamsin] It's a very sensible box.
(Received: TM89 U-TURN.)
[name: Tamsin] That's the Accord's word that Pokémon up to level twenty-three will heed you.
[name: Tamsin] And the Cutter will give you Cut now.
[name: Tamsin] He'll say no first. Wait for the second answer.
[portrait: TAMSIN, sad] \PN... could you come up to the loft?
[name: Tamsin] There's something I should say to someone, and you've an honest sort of silence.
```
*Tamsin, after the confession (her ledge):* `[portrait: TAMSIN, neutral] The Cutter in town owes me a favour. Tell him I sent you. And— thank you. Not sorry. Thank you.` / `[portrait: TAMSIN, neutral] The stair behind me goes up to Gran's practice lofts. They're open to you now. Mind the brass wire. It isn't hers.` *(the brass wire is Meridian's, stamped with a sunburst: GYM_PUZZLES §132)*
*If Granny's Knot is solved (S308):* `[portrait: TAMSIN, crying] You finished Gran's row. ...She'd have shouted. Happily. Sorry — I'm crying, that's the Silkwood, it's very dusty.`

## Map 130/131 loft — **EV "Tamsin's confession"** → **CHOICE `:ch2_tamsin`** (the key keeps its old name; staged in the Warden's loft, high in the elder above the webs, where Hett says the ledger is kept; or in the Guildhall loft 123: guard whichever copy is built with `pf_choice(:ch2_tamsin).nil? && pfm_gym_won?(:LEADER_TAMSIN)`)
```
(The Warden's loft, high in the elder above the webs: a ledger open on a table, a contract with a gold sunburst seal. Tamsin won't sit.)
[portrait: TAMSIN, sad] That woman at the pylon. With the shears. She was right.
[name: Tamsin] I signed it.
[name: Tamsin] Briarwick's bankrupt. It has been for three years. Gran hid it.
[name: Tamsin] I found the accounts the week I buried her.
[name: Tamsin] Meridian offered four hundred thousand for "stewardship rights".
[name: Tamsin] One pylon. Free light.
[name: Tamsin] I signed it by myself, at night, so nobody would have to know how bad it was.
[name: Tamsin] And it WORKS. That's the thing.
[name: Tamsin] The looms ran till midnight for a week. Everyone was so happy.
[name: Tamsin] Nobody had been happy since the funeral.
[portrait: TAMSIN, crying] And now the Glasswood's walking up the survey line like it was invited.
[name: Tamsin] Fourteen moths this week. I count them.
[name: Tamsin] I count them every morning.
[name: Tamsin] The man in Saltmere told everyone to ask their Warden.
[name: Tamsin] Nobody's asked me yet. They're all too kind. The guild meets tonight.
[name: Tamsin] Tell me what to do. Please. I've run out of thread.
> Tell them the truth. I'll stand next to you. (help_confess)
  Script: pf_choose(:ch2_tamsin, :help_confess)
  [portrait: TAMSIN, shocked] Next to me. Not in front?
  [name: Tamsin] ...A thread holds because it's twisted with others.
  [name: Tamsin] I've had that on the SIGN.
  → Scene: the guild meeting. Tamsin speaks; her voice cracks twice; Hett stands up first: "Then we sign it WITH you, girl, and then we tear it up together." The contract is renegotiated: a smaller pylon, off the grove.
> They deserve to know. If you won't say it, I will. (expose)
  Script: pf_choose(:ch2_tamsin, :expose)
  [portrait: TAMSIN, panic] No— wait— not like—
  → Scene: the guild meeting. The PC lays the contract on the table. Uproar. The looms stop. Tamsin stands very still, then tears the contract in half herself, in front of them: "I'm sorry. I'm so sorry. That's the last time I'll say it tonight."
  (Outcome flag TAMSIN_PUBLIC_CONFESSION is derived from this choice.)
> It's your secret. I won't tell. (keep_secret)
  Script: pf_choose(:ch2_tamsin, :keep_secret)
  [portrait: TAMSIN, panic] ...Thank you. I think.
  [name: Tamsin] I'll fix it quietly. I'll find the money somewhere.
  → No meeting. The pylon is finished within the week (map state). Hett's lines stay suspicious. (In Act V, Tamsin can't afford to let go of her Plate.)
(All branches:)
[portrait: TAMSIN, neutral] Whatever's making the wood ring, it's in Cocoonfall Hollow, at the Glasswood's heart.
[name: Tamsin] I can't cross the Veil. Nobody can.
[portrait: JUNO, neutral] *(from the stairs, hatbox in her arms)* ...They can.
[name: Tamsin] [emote: exclaim] *(shock lines)* What?
[name: Tamsin] Then take this. It was Gran's shuttle.
[name: Tamsin] It's only wood. But she never dropped a thread while she held it.
(Received: MOTHER LOOM'S SHUTTLE. Key Item. "Worn smooth by fifty years of one hand.")
QUEST LOG: "The Ringing Wood" — Get Cut from the Cutter, then cut through the Deepwood to Cocoonfall Hollow.
```

## Map 525 — Gossamer Deepwood (`:SILKWOOD`; Cut required; after Tamsin's badge)
```
[name: Bug Maniac Ferris] The bugs in here have gone STRANGE and I love them!
(Battle.)
[name: Bug Maniac Ferris] [after] That one hummed. Did you hear it hum?
HIDDEN ITEM (hollow stump): SUPER POTION. "The stump kept it dry."
CRYSTAL SILK (the mouth to the Hollow, east): A curtain of silk gone to glass. Mother Loom's shuttle catches in it, and the threads part like they recognize it. (Opens once `:ch2_tamsin` is chosen.)
```
**Optional thread: cameo sidequest "Lost in the Gossamer" (Shelly)** — CAMEOS.md §1; S181 on completion
```
(A dew-pond clearing. A pink-haired girl is crouched in front of a Caterpie, bowing to it.)
[name: Shelly] I'm so sorry, was this your leaf?
[name: Shelly] I didn't know it was your leaf.
[name: Shelly] [emote: sweat] Oh! A person! Um. Hello.
[name: Shelly] Is this— this isn't the Rhodochrine Jungle, is it. *(sweat drop)*
[name: Shelly] I looked into a pond at home and then I was looking OUT of this one.
[name: Shelly] That was three days ago. The paths keep re-weaving.
> I'll help you get back.
  [name: Shelly] Really? You don't have to.
  [name: Shelly] I mean please do. I mean thank you.
(She follows. The dew-pond she arrived through is behind a small Bleed Veil; a glassed Masquerain guards it. The PC enters alone, battles it (`:BLEED`, level per BALANCE §6), and it calms.)
[name: Shelly] You just... walked in.
[name: Shelly] Where I'm from, nobody walks into the sick places and comes out the same.
[name: Shelly] Before I go, could we have one practice battle? Doubles?
[name: Shelly] I'm supposed to be good at this and I don't want to be rusty when I get home.
BATTLE: FESTIVAL_SHELLY "Shelly", version 1 (double, `:SILKWOOD`; level per BALANCE §6, after Gym 2).
(After, win or lose:)
[name: Shelly] Your forest sounds like home used to, before the city got sick.
[name: Shelly] Look after it?
(Received: SILVER POWDER and TM STRUGGLE BUG.)
MOVE: She steps into the pond's reflection and is gone. One pink ribbon floats on the water.
```

## Map 548 — Cocoonfall Hollow (`:BLEED`)
```
(The Veil at the Hollow's mouth. Inside: a crater of crystal trees, and silk that has turned to glass thread, strung between them like a harp. It rings.)
(Juno and Tamsin stop at the Veil. Juno: "Shout if— no. You can't hear through it, can you. Just come back.")
INSPECT, glass cocoons: Dozens, hanging. Inside each, a moth, wings spread, perfectly still. One of them twitches.
```
**Boss: "The Glass Matriarch"** (multi-bar; `design/BOSSES.md`)
```
(At the center, a Galvantula the size of a cart, half crystal, sits on a nest of glass silk wound around something that glows faintly green beneath the roots.)
It turns eight eyes on you. Four of them are glass.
BOSS BATTLE: Glass Matriarch (GALVANTULA, 2 bars, level per BOSSES.md for the segment after Gym 2; field `:BLEED`; at the bar break it "re-strings the nest": the field borrows `:SILKWOOD` for 3 turns).
(WIN:)
The Matriarch collapses onto the nest. The ringing drops by half. It thrashes, shedding slivers of crystal.
```
**CHOICE `:ch2_matriarch`** (the key keeps its old name)
```
> Stay with it. (soothe)
  Script: pf_choose(:ch2_matriarch, :soothe)
  You sit down in the glass. You hold Mother Loom's shuttle because you don't know what else to hold.
  (Fade. Night passes. Fade in: dawn through crystal.)
  The Matriarch is asleep against your knee. Around you, half the grove has gone to glass in the night. The other half hasn't.
  The ringing has stopped.
> Put your hand on it. Make it stop. (silence)
  Script: pf_choose(:ch2_matriarch, :silence)
  You press your palm to its crystal side.
  Something goes out of it, like water down a drain. Through you. To nowhere.
  The crystal falls away as dust. The grove stops ringing at once. Not one more tree turns.
  The Matriarch stands. It is whole. Its eyes are dull as buttons. It doesn't look at you. It doesn't look at anything.
Switch S107 CH2_MATRIARCH_DONE = ON. V105 BRIARWICK_GLASSWOOD = 1. (The Accord cordon on the forest road to Windfall Row lifts: the shortcut home is open.)
ITEM (under the nest): a sliver of green light sinks back into the roots as you watch. FIELD NOTES: "Something under the Hollow is holding the wood together. I think I was standing on it. — note to self: ask Tamsin where the Plate is."
```
**EV "Outside the Veil"**
```
(soothe:) [portrait: TAMSIN, crying] Half the grove. ...Half. And the moths that are left are *singing*. I'll take half. I'll take it.
          [portrait: JUNO, happy] You stayed all night!
          [name: Juno] We could see you through the shimmer, just sitting there!
          [name: Juno] Kestrel would've hated it!
(silence:) [portrait: TAMSIN, shocked] It just... stopped. All of it.
          MOVE: the Matriarch walks out through the Veil, past them, into the wood. It doesn't react to anything.
          [portrait: TAMSIN, shocked] Oh. Oh, that's — thank you. I think.
          [portrait: JUNO, sad] ...It didn't look at me. They always look at me.
(Both:)
[portrait: TAMSIN, neutral] The next Warden's Marisol Reyes, in Ebbmouth.
[name: Tamsin] North over Spinners' Rise, through the Rimewood and over the border.
[name: Tamsin] She'll swear at you. It's a compliment.
[name: Tamsin] Come back, will you?
[name: Tamsin] I'd like to show you the room when it isn't tangled.
[portrait: JUNO, sad] I've got to take the eggs to Uncle Rowan in Verdance.
[name: Juno] Forty eggs, one hatbox, no running.
[name: Juno] I'm going to tell him about the Pageant.
[name: Juno] About what the man said about Verdance.
[name: Juno] I want to see his face when I tell him.
[name: Juno] Tell Kestrel— no. Don't tell Kestrel anything.
[name: Juno] He'll only be rude about it.
MOVE: Juno leaves by the east road toward Verdance, hatbox held in both arms.
```

## Chapter 3 close — Map 120
```
(On the way out of Briarwick, a child is standing at the Festival poster with a stick of charcoal.)
[name: Child] I circled it. The Crown in the chapel's got a whole stone.
[name: Child] This one's got a bit gone. See?
[name: Child] Mum says the Crown got hurt once.
[name: Child] How do you hurt a crown?
(No answer option. The PC's hand moves, unprompted, to their chest. WAIT 40.)
GALE POST (Pokémon Center desk): "Heard about the Hollow. Lecture Two enclosed. It is nine pages. Page nine says I'm proud of you. Do not skip to page nine. — I.L."
NORTH GATE: The Weavers' Road ends here. North of the gate the drove road climbs Spinners' Rise out of the trees. On the last trunk, the silk is white with frost.
QUEST LOG: "Eighteen Roads" — Earn the third badge in Ebbmouth, over the Rimewood border.
V102 STORY_CHAPTER = 4.
```

---

## Appendix: events added or changed versus the built specs
- **Moved here from `20_SCRIPT_CH0-2.md`** (Revision 14): Gossamer Wood, Briarwick and its interiors, Thistle, the Loomhouse, Tamsin's confession, the Deepwood, Shelly, Cocoonfall Hollow and the chapter close. Before the swap this was Chapter 2.
- **[NEW]** The Grey Saltings, Brinecut and Thistledown Manor lines (they were outline-only in 04); the Dyers' Ford (552, a new map: every event); the Gossamer Wood's south cordon; Tamsin's "you beat Dorian" opener; the bun-seller's Kestrel line; the ogre-mask stall; Thistle's shears and Lantern lines; the second badge note; the north-gate frost line.
- **Changed for Revision 19 (2026-11-20): Gym 2 is the Canopy.** The linked-heddle Weaving Hall is retired. 130 is the weavers' lobby (no puzzle; the Gym Guide explains the webs and the Joltik; the lobby weaver is **Weaver Tibb**, so he isn't confused with Pim, the net-minder upstairs). 131 is the hollow of the elder, with web trampolines, sticky webs, the two Joltik strands (V305–307) and Tamsin's ledge. All three trainers are in 131: Nell on ledge 1 (optional), Orla on ledge 2 (watches the landing), Bram on Tamsin's ledge (optional). Tamsin's lines now credit the Bugs with the webs ("We spun this whole hollow together"). The confession is in the Warden's loft. Pim's third hint names the Joltik by place, not by the letters A/B/C, and the Joltik line no longer says "the taut one... the slack one" (both start slack). Map requests: `mapgen/REQUESTS.md`, story editor 2026-11-20.
- **Changed for Revision 14:** Tamsin is a double battle at cap 19 and says "level twenty-three"; Cut comes from the Cutter after *her* badge (not any badge); the survey flags and Juno's flag line moved here from Windfall Row; the confession may stage in the Warden's loft or the Guildhall loft (guard as noted); Shelly and the Matriarch are levelled for the stretch after Gym 2; the Matriarch also lifts the forest-road cordon. The old `$player.badge_count >= 1` tests must become `pfm_gym_won?(:LEADER_TAMSIN)` (see `design/SWAP_GYM1_GYM2.md`).
- **Open items for other teams:** see `design/SWAP_GYM1_GYM2.md`. Portraits used here (parked by Revision 15; keep the tags): Juno, Tamsin, Thistle, Shelly.
