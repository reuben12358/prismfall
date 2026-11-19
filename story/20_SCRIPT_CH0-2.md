# Script: Prologue, Chapter 1, Chapter 2 (Saltmere, through Gym 1 and the Pageant)

> **Final playable script** for the game's first hour (SPINE Revisions 8 and 14). It covers maps 109–110, 100–108, 520, 523, 522, 521 (Chapter 1), then the Strand Road 520 → 527 → 528 and Saltmere 140–147, the Pell Playhouse 150/154 (Gym 1) and the Lantern Theatre 145 (Chapter 2). Structure follows the built events in `mapgen/specs`; where this file adds an event, it is marked **[NEW]**. Maps 527 and 528 are new (cartographer, `tools/worldmap/world_data.py`), so all of their events are new.
> **Chapter 3** (the Weavers' Road, Briarwick, Gym 2) moved to **`story/21_SCRIPT_CH3.md`** when Revision 14 swapped the first two gyms.
> Sources: 04_ACT_I (outline), 15_COMEDY (scenes Ch0–Ch2, inlined), NARRATIVE_KEYS (choice keys), FLAGS (switches), SYSTEMS (script calls), GYM_PUZZLES (Gym 1), BALANCE 4b (versions).
> **Keys and switches keep their old names.** `:ch3_juno_talk`, `CH3_PAGEANT_DONE`, `CH3_J1_DONE` and `CH3_UNDERSTUDY_GOT` are all Chapter 2 now; IDs never renumber (FLAGS.md).

## Conventions
- `[portrait: NAME, expression]` precedes each portrait line. No tag = plain message box (narration, signs, generic NPCs use `[name: X]` with no portrait).
- *(italics)* = emote bubble or staging. `MOVE:` = movement route. `SE:` / `BGM:` = audio. `WAIT n` = frames.
- `> option` = a choice. `→` = what follows. `PC` = the player; `\PN` = player name.
- **Script calls:** `pf_choose(:key, :value)`, `pf_bond_add(:ID, n)`, `pf_standing_add(:FACTION, n)`, `pf_resonance_add(n)`, `Prismfall.rival_battle(...)`, `Prismfall.gym_battle(n)`, `Prismfall.game_over(:GO_X)`, `Prismfall.record_starter(...)`. Choice effects in NARRATIVE_KEYS §4.2 apply automatically on `pf_choose`; extra deltas are written out.
- **Gym numbers:** events look a Warden's number up instead of hard-coding it (`Prismfall.gym_battle(pfm_gym(:LEADER_DORIAN))`, `pfm_gym_won?(:LEADER_TAMSIN)`, from `mapgen/ruby/008_GymOrder.rb`). The script writes the number for readability: Dorian is 1, Tamsin is 2.
- **Switches/variables:** names from `design/FLAGS.md` (S101 = `PRO_FERRY_DONE`, etc.).
- **Reactive lines:** `[after X]` variants replace the default once switch X is on.

---

# PROLOGUE — "The Last Ferry"

**Set at start:** V101 STORY_ACT = 0, V102 STORY_CHAPTER = 0.

## Map 109 — The Dovetail, Deck (dusk; BGM: sea wind, low strings)

### EV "Prologue intro" (autorun)
```
(Black screen.)
SE: ship's horn, long.
TEXT (center, white on black): Spring, AF 300.
TEXT: The Concert of Regions has sealed the borders of Velmora.
TEXT: This is the final civilian crossing.
(Fade in: the deck. The PC stands at the port rail, one bag at their feet. Gulls. On the horizon, a low line of eighteen colored glows.)
[name: Deckhand] Twenty minutes to the Landing! Mind your bags, mind your feet, mind the Captain!
MOVE: Deckhand walks aft.
(Control to player. The PC can walk the deck. The gangway aft is roped off until S101.)
```

### Key Item (start inventory): Mum's Letter
```
ITEM DESCRIPTION: A letter in your mother's handwriting. The ink runs where the sea got at it.
USE →
"Go to Imelda Larch at Ferrow's Landing, before they close the strait.
Don't let anyone scan you. Don't go to Crownhaven.
I'm sorry I never told you why. I wanted one of us to have an ordinary life.
— Mum."
```

### EV "Rail sign" (action)
```
SIGN: DO NOT LEAN ON RAIL. — Capt. E. Morrow
(If the PC is facing the rail tile next to it:) You are leaning on it.
```

### EV "Captain Edda" (touch trigger at the rail; comedy scene Ch0, "Do Not Lean")
```
MOVE: Edda stomps in from the wheelhouse. *(anger vein)*
[portrait: EDDA, angry] Oi! Sprog! Can you read?
> Yes.
  [portrait: EDDA, deadpan] Then you're doing it on purpose. That's worse.
> No.
  [portrait: EDDA, shocked] ...Oh. Oh, stars. Right. That's a D. That one's an O. *(sweat drop)*
> ...
  [portrait: EDDA, deadpan] Strong silent type. Wonderful. I'll just talk to the rail, shall I?
  [portrait: EDDA, angry] Rail! Tell the sprog to get off you!
(All branches continue:)
MOVE: Edda steps closer, then stops dead. *("..." bubble)* WAIT 40.
[portrait: EDDA, shocked] Don't lean on my rail like that, you'll— huh.
[portrait: EDDA, neutral] ...Never mind. You stand how you like.
[portrait: EDDA, neutral] Mind the gap when we dock. And don't look down at the water after dark.
> Why not?
  [portrait: EDDA, deadpan] Because I said, and it's my boat.
> ...
  [portrait: EDDA, sad] ...Good. Somebody used to ask me that every crossing.
MOVE: Edda returns to the wheelhouse door and stays there, watching the PC.
```
*Reactive (talk to Edda at the wheelhouse):*
```
[portrait: EDDA, neutral] Thirty-one years on this strait. Never thought I'd see them close it.
[portrait: EDDA, deadpan] Don't touch the wheel. Don't touch the rail. Touch the horizon if you like, it's free.
```

### Flavor passengers (deck)
```
[name: Old Man] See the colors on the skyline? Eighteen of 'em. That's Velmora.
[name: Old Man] When I was a lad you only saw the Imprints on a clear night. Now you see 'em through fog.

[name: Woman with crate] I'm going home to Saltmere. My sister says don't. I said, where else would I go? I get ill anywhere else.
[name: Woman with crate] Three weeks abroad and I was grey as dishwater. They call it wilting. You'll see.

[name: Boy] Mum says when we land a machine tells you what color you are! I want to be red.
[name: Boy's Mother] You'll be green like the rest of us, love. We're Briarwick.
[name: Boy] ...Can I be green AND red?

[name: Sailor] Last crossing. After tonight the Concert's cutters turn back anything bigger than a gull.
[name: Sailor] Captain says she'll tie up at the Landing and learn to knit. She won't.

[name: Seasick Man] Don't talk to me. If I open my mouth, more than words come out.
```

### EV "Horizon" (action at the bow)
```
Eighteen lights sit low over the sea, each a different color.
One of them, far to the north, flickers.
(Hidden item on the coiled rope beside the bow: POTION. "Someone's seasick remedy. It's just a Potion with a lemon drawn on it.")
```

### EV "Aurelian Voss" (starts when the PC returns to the rail after talking to Edda)
```
MOVE: Voss walks up beside the PC and leans on the rail, right next to the sign. He holds a chipped white mug with a faded sunburst.
[portrait: VOSS, happy] First crossing? Everyone goes quiet when they see the lights.
[portrait: EDDA, angry] *(from the wheelhouse)* RAIL! *(anger vein)*
[portrait: VOSS, happy] I believe the rail has no objection, Captain.
[portrait: EDDA, angry] Nobody asked the passengers in the nice coats!
[portrait: VOSS, neutral] She's been shouting at me since I was a linesman. It's how I know I'm home.
[portrait: VOSS, neutral] I've spent a month in a marble room asking the Concert not to do this. They did it anyway. Politely.
[portrait: VOSS, neutral] So. You're coming *in* on the day everyone else wishes they could get out. That takes nerve or bad luck.
> Nerve.
  [portrait: VOSS, happy] Good. Velmora runs on it.
> Bad luck.
  [portrait: VOSS, happy] Then you'll fit right in.
> ...
  [portrait: VOSS, neutral] Or grief. Forgive me. I shouldn't guess.
[portrait: VOSS, neutral] Are you challenging the gyms? You've got the look. Eighteen Wardens, eighteen badges. Nobody's done all eighteen in ten years.
[portrait: VOSS, happy] Here. You'll want one of these.
(Received: BADGE CASE.)
ITEM DESCRIPTION: A slim brass case with eighteen empty settings. Stamped on the hinge: MERIDIAN CONCORD.
[portrait: VOSS, neutral] We make them for the League anyway. Call it a welcome from a fellow traveler.
[portrait: VOSS, neutral] And this, if you'll take it. A Meridian Fellowship. A little money each month, a discount at any Mart. We give them to young trainers with promise.
```
**CHOICE `:pro_fellowship`**
```
> Thank you. (accept)
  Script: pf_choose(:pro_fellowship, :accept)
  (Received: FELLOWSHIP CARD. ₽3000.)
  [portrait: VOSS, happy] No, I insist. Somebody should be kind to you on a day like this.
> No, thank you. (decline)
  Script: pf_choose(:pro_fellowship, :decline)
  [portrait: VOSS, happy] Independent. Good. Keep that. It's worth more than the card.
> ... (silent)
  Script: pf_choose(:pro_fellowship, :silent)
  [portrait: VOSS, neutral] Think about it.
  (He sets the card on the rail. Received: FELLOWSHIP CARD. It is not activated; a Mart clerk can activate it later for the ₽3000.)
```
```
SE: ship's horn.
[portrait: VOSS, neutral] That's the Landing. Aurelian Voss. If you ever need anything in Lumen City, ask for me by name. They'll laugh, and then they'll fetch me.
MOVE: Voss walks aft. At the gangway he looks back once.
Switch S101 PRO_FERRY_DONE = ON. (Gangway rope removed.)
```
*If the PC inspects the mug mark he left on the rail:* `A ring of cold tea. He drank it black.`

## Map 110 — The Dovetail, Cabin (optional before docking)
```
BUNK: Your bunk. You didn't sleep in it.
PORTHOLE: Dark water. Far down, for a moment, something glows. Then it doesn't.
[name: Cook] Last bowl of chowder on the last ferry. Historic chowder. Eat it slow.
  (Received: OLD CHOWDER. "Restores 20 HP. Tastes like the end of an era.")
BOOKSHELF: "Passenger Notice: Persons of Velmoran birth are advised that prolonged absence from one's home Imprint may cause fatigue, pallor and low spirits. The line accepts no liability for wilting."
LOCKED TRUNK (Edda's): It's locked. Scratched into the lid, very small: I.A. + child, night crossing, 290. Paid in full.
```
*(The trunk is the first Edda clue. No reaction is scripted.)*

## Map 100 — Ferrow's Landing, the dock (arrival; BGM: harbor morning, accordion)

### EV "Docking" (autorun on transfer)
```
(The gangway is down. Passengers queue toward a brass-and-glass gate bolted to the old stone pier. Beside it stands a green bronze plaque.)
[name: Calla] Welcome to Velmora. Step through one at a time, please. Hold still. It doesn't hurt.
MOVE: The Boy runs through the gate. SE: chime. A bar on the gate glows green.
[name: Calla] Insect tint. Briarwick. Thank you.
[name: Boy] MUM. I'M GREEN.
[name: Boy's Mother] I know, love.
MOVE: Woman with crate steps through. SE: chime. The bar glows white.
[name: Calla] Blank tint. Saltmere. Welcome home.
```

### EV "Edda's last call" (touch, at the foot of the gangway) — **Game over `GO_HOMEWARD`**
```
[portrait: EDDA, neutral] That's it, then. Once I cast off the Concert's cutters won't let me back across.
[portrait: EDDA, neutral] Last chance, sprog. Anyone who wants off this rock rides with me now.
> I'm staying.
  [portrait: EDDA, happy] Thought so. Go on. Mind the gap.
> I want to go back.
  [portrait: EDDA, neutral] ...You sure? I'll ask once more, because nobody asked her. Once I cast off, that's it.
  > I'm staying.
    [portrait: EDDA, happy] Good. Stars. Don't frighten an old woman.
  > Take me back.
    [portrait: EDDA, sad] Right. Get aboard, then.
    (Fade. SE: horn. The eighteen lights recede.)
    Script: Prismfall.game_over(:GO_HOMEWARD)
```

### EV "Accord plaque" (action)
```
A bronze plaque, green with age.
"EIGHTEEN IN CONCORD, ONE IN KEEPING."
— The Accord of Velmora, AF 4
Someone has bolted a Meridian sunburst to the post beside it. The bolts are new.
```

### EV "Customs scan" (touch, at the gate)
```
[portrait: CALLA, neutral] Next, please. Hold still.
MOVE: PC steps into the gate.
SE: chime... then nothing. The bar stays dark. WAIT 60.
[portrait: CALLA, neutral] One moment.
SE: chime. The bar flickers, and a word scrolls across it: NULL.
[portrait: CALLA, shocked] *(question mark)* ...That's not a tint.
[portrait: CALLA, neutral] I'm sorry, could you step out and in again?
MOVE: PC steps out, steps in. SE: chime. NULL.
[name: Boy] Mum, that one's got no color!
[name: Boy's Mother] Don't point.
(The queue behind murmurs. *("..." bubbles)* over three passengers.)
MOVE: Voss walks up from behind the queue.
[portrait: VOSS, happy] Faulty unit. These things hate sea air.
[portrait: VOSS, neutral] Let them through, Calla.
[portrait: CALLA, neutral] Sir, the protocol says—
[portrait: VOSS, neutral] The protocol was written by me, on a train. Let them through.
[portrait: CALLA, neutral] ...Yes, sir. Welcome to Velmora.
MOVE: PC walks through. Voss follows, pauses beside the PC.
[portrait: VOSS, happy] There. Ordinary as anyone. Enjoy the Landing. Try the bramble tarts.
MOVE: Voss exits north toward a waiting Meridian carriage. He glances back at the gate's dark bar. WAIT 30. He leaves.
(Background: Calla raises a small brass camera to the gate's screen. SE: quiet shutter. No text.)
Switch S102 PRO_SCANNED_NULL = ON.
SE: ship's horn, long. MOVE: the Dovetail sprite pulls back from the pier one tile and stops. A chain is drawn across the harbor mouth.
[name: Harbor Crier] By order of the Concert of Regions, the Hallow Strait is closed! The Hallow Strait is closed!
V101 STORY_ACT = 1. V102 STORY_CHAPTER = 1.
TITLE CARD: ACT I — THE LAST FERRY
```

*Calla, after the scan (action):*
```
[portrait: CALLA, neutral] The unit's been logged as faulty. Please don't worry about it.
[portrait: CALLA, neutral] ...Are you feeling well? No fatigue? No pallor?
> I'm fine.
  [portrait: CALLA, neutral] Good. That's good. Welcome to Velmora.
> Why?
  [portrait: CALLA, panic] No reason! It's a standard question. It's on the form. *(sweat drop)*
```
*Edda, after the chain goes up (she stands on the pier with her arms crossed):*
```
[portrait: EDDA, angry] Impounded! Thirty-one years and they chain her up like a stray Growlithe!
[portrait: EDDA, deadpan] I'm told I may apply for compensation. In writing. To the people who did it.
[portrait: EDDA, neutral] ...You've somewhere to go, sprog? Larch? Good. Up the headland. She'll feed you something terrible.
[portrait: EDDA, sad] You stand at the rail like somebody I used to know. That's all. Go on.
```

---
*(Chapter 1 continues below.)*

# CHAPTER 1 — "Tidewatch"

## Map 100 — Ferrow's Landing (town; BGM: harbor morning)

### Objective marker
```
QUEST LOG: "Mum's Letter" — Find Imelda Larch at the research station on the headland.
```

### Named residents

**Wenna Hale** (bramble-tart stall, quay)
```
[portrait: WENNA, happy] Tarts! Bramble tarts! Last of the— oh. You came off the ferry.
[portrait: WENNA, shocked] You're the one Imelda's been pacing about. Look at you. You're a coat hanger with a bag.
[portrait: WENNA, happy] Eat this. No, don't pay me. Eat it where I can see you.
(Received: BRAMBLE TART. "Restores 30 HP. Still warm. Tastes like somebody's kitchen.")
[portrait: WENNA, neutral] My Juno works up at the station. Talks like a kettle. You'll like her. Everyone does, it's exhausting.
[portrait: WENNA, happy] You'll know her by the flowers. She's worn her aunt's blossoms since she was three. They've never wilted. We stopped asking.
```
*[after S103]* `[portrait: WENNA, happy] She named your little group? Of course she did. She named the kettle.`
*[after S105]* `[portrait: WENNA, sad] She told me about the orchard. That was the Pruetts' place. They had apples when I was a girl.`

**Coll Hale** (mending nets beside the stall)
```
[portrait: COLL, neutral] Mm. Ferry child.
[portrait: COLL, neutral] Farm's up the lane if you need a bed. Wenna'll say the same but with more words.
[portrait: COLL, deadpan] ...Did she give you a tart? Then you're family. That's how it works. I didn't make the rules.
```
*[after S105]* `[portrait: COLL, neutral] Orchard went glass the same week my hens stopped laying. Don't know that it's connected. Don't know that it isn't.`

**Fisherman Odo** (pier end; gives the Old Rod)
```
[name: Odo] You fish? No? Everybody fishes. You just haven't yet.
(Received: OLD ROD.)
[name: Odo] Catch a Magikarp, throw it back, feel superior. That's the whole sport.
```
*[after S102]* `[name: Odo] Heard the gate went quiet on you. My rod goes quiet on me all the time. Doesn't mean there's nothing there.`

**The Harbor Crier**
```
[name: Crier] Hear ye! The Strait is closed! The Festival of Champions proceeds as planned, in the autumn, by grace of the Sovereign!
[name: Crier] ...I don't know how both of those are true either. I just read the card.
```

### Flavor townsfolk (each a separate event)
```
[name: Rope-skipping Girl 1] One for the stage and two for the weave,
[name: Rope-skipping Girl 2] three for the river that won't take its leave!
[name: Rope-skipping Girl 1] Four for the lantern, five for the dune,
[name: Rope-skipping Girl 2] six for the fen and its poison-blue moon!
(Talk again:)
[name: Rope-skipping Girl 1] ...and none for the cage, and none for the king! You're out!
[name: Rope-skipping Girl 2] I'm NOT out, you said "king" too fast!

[name: Kelp-drier] Kelp for the Professor's tea. I've offered to stop. She says no. I've offered to pay HER.

[name: Old Sailor] That chain across the harbor? My grandfather forged the links. He'd be proud and furious.

[name: Meridian Linesman] Don't mind the gate, it's just for counting. We're putting lamps along the quay next month. Free light. You'll like it.
[name: Meridian Linesman] (again) The old lamplighter? He's got a pension. ...I think he's got a pension.

[name: Lamplighter] Forty years I've lit this quay. Now a pole does it. The pole doesn't know the fishwives' names.

[name: Fishwife] The ferry child! Is it true you've no tint at all? Let me see your eyes. ...Huh. Like rain.

[name: Woman hanging washing] I went to my cousin's wedding across the strait. Nine days. Came back grey. Never again. I'll send a card.

[name: Boy with toy boat] When I'm big I'm getting all eighteen badges. Then I'll be Sovereign and make it illegal to have baths.

[name: Girl with Wingull] She's called Captain Edda. The real Captain Edda doesn't know. Don't tell her.

[name: Accord Clerk] Quarantine notices, form nine. You don't need one. Nobody needs one. I have four hundred.

[name: Drunk on the steps] They closed the sea. You can't close the sea. I've seen it. It's enormous.

[name: Old Woman on bench] The Festival poster's up already. They always paint the Sovereign's Crown a bit wrong these days. Fewer sparkles.

[name: Net-mender] Two ferry-loads of folk came home this month who swore they'd never. You can run from Velmora. You just can't stay run.

[name: Twin 1] We're the same tint!  [name: Twin 2] We're the same EVERYTHING.  [name: Twin 1] I'm taller.  [name: Twin 2] By a HAT.

[name: Meridian Recruiter] Fellowship cards for promising trainers! Oh, you have one. From whom? ...HIM? Personally? *(shock lines)* Excuse me, I need to sit down.
```

### Signs and objects
```
TOWN SIGN: FERROW'S LANDING — Elowen's Door on the Sea. Pop. 212 and one lighthouse.
FESTIVAL POSTER: "THE FESTIVAL OF CHAMPIONS, AF 300. All Kingdoms. One Blessing." A painted crown floats over eighteen colored banners. The stone in the crown has a tiny dark fleck. Probably a printing fault.
LANE SIGN: ↑ Tidewatch Station (Prof. I. Larch) · → Hale's Bramble · ← Lighthouse (KEEP OUT. THIS MEANS YOU, KESTREL.)
ROAD SIGN [NEW] (north gate): ↑ THE FERRYMEN'S MILE — Hale's Bramble, Windfall Row, and at the Hale Bell the Strand Road west to Saltmere. Briarwick by the forest road: CLOSED BY ORDER OF THE ACCORD.
NOTICE BOARD: "LOST: one Skwovet, answers to Biscuit. Last seen heading for the old Pruett orchard. Do NOT follow it in. — W. Hale"
FISH BARRELS: Magikarp. They look resigned.
HIDDEN ITEM (behind the tart stall): ORAN BERRY. "It rolled off the stall. Finders keepers is an old harbor law."
HIDDEN ITEM (end of the breakwater): PEARL. "Stuck in a mooring ring. The sea was saving it."
```

### Sidequest A — "Captain Edda (the Wingull)"
```
(Girl with Wingull, second talk, after S102:)
[name: Girl] Captain Edda flew off! The gate went BING and she got scared! She's on the lighthouse rocks and I'm not allowed there!
QUEST LOG: "Captain Edda" — Find the Wingull on the lighthouse rocks.
(Lighthouse rocks, west shore: a Wingull event.)
The Wingull eyes you. It has a bottle cap in its beak and is very proud of it.
> Hold out a Bramble Tart crumb.
  It hops onto your arm. It keeps the bottle cap.
> Just pick it up.
  It bites you. Then it hops onto your arm anyway.
(Return to the girl:)
[name: Girl] CAPTAIN! You're in so much trouble. Here, ferry person, she wants you to have this.
(The Wingull drops the bottle cap at your feet, then changes its mind and takes it back.)
(Received: SHARP BEAK. "A Wingull's idea of a fair trade.")
(The real Edda, nearby, [portrait: EDDA, deadpan]: "...What did she call that bird?")
```

### Sidequest B — "The Lamplighter's Last Round"
```
(Lamplighter, second talk:)
[name: Lamplighter] The pole lights itself tonight. Do an old man a kindness? Light the six quay lamps by hand, the proper way. Last time anyone will.
(Received: LAMPLIGHTER'S TAPER.)
QUEST LOG: "The Last Round" — Light the six old lamps along the quay (0/6).
(Each lamp, action: "You light it. The flame is small and yellow and smells of whale oil.")
(After six, at dusk the Meridian lamps switch on above them, white and humming.)
[name: Lamplighter] There. Look at that. You can hardly see mine under theirs.
[name: Lamplighter] ...But the gulls came to mine. Did you see? Here. I won't need it.
(Received: CHARCOAL. "It kept a harbor lit for forty years.")
```

## Map 101 — Pokémon Center / Map 102 — Mart / Map 104 — Tidewater Inn / Map 107 — Dockmaster's House
```
[name: Nurse] Welcome! We heal Pokémon for free. We can't do anything about feelings, but there's tea.
[name: Nurse] (no Pokémon yet) Oh, you don't have one yet! Come back when you do. I'll act surprised.
[name: Trainer at PC] They put a scanner on our door last week too. Mine says "Insect, Briarwick" every time I come in. I KNOW, door.

[name: Mart Clerk] Potions, Poké Balls, Synthetic Seeds. The Seeds are new. Meridian grows them in a lab. Don't plant one. A man planted one. We don't talk about his garden.
[name: Mart Clerk] (with an unactivated Fellowship Card) Want me to switch that card on? ...Signed by WHO? *(shock lines)* (Received: ₽3000.)

[name: Innkeeper] Rooms are full of people who came home on the last boat with nowhere to be. First time I've been full since the wedding of '91.
[name: Inn Guest] I left Velmora nine years ago to be a famous painter. I'm back to be a tired one.
[name: Inn Guest 2] The Concert says we carry the Bleed. We don't carry it. It's not a cold. It's the ground.

[name: Dockmaster] Thirty ferries a month, then one, then none. I'm the Dockmaster of a dock that's master of nothing.
DOCKMASTER'S LEDGER (bookshelf): "AF 290, night crossing, unscheduled. Capt. Morrow. Two passengers, one a child. Fare: paid in kind." The entry has been crossed out twice. You can still read it.
```

## Map 103 — Tidewatch Station (Larch Research Station)

### EV "Professor Larch" (first entry, autorun)
```
(A cluttered station: tide charts, brass instruments, a stove with a blackened kettle. Juno is at a bench, labeling seed packets, back turned. A wreath of white-and-pink blossoms sits crooked on her auburn hair, and a veil of them trails off the stool and across the floor, where it has collected some straw and one bewildered Wooper.)
[portrait: LARCH, neutral] If that's the kelp man, the answer is still yes, and I don't care what he's offering.
MOVE: Larch turns. Sees the PC. WAIT 40.
[portrait: LARCH, shocked] ...Oh.
[portrait: LARCH, neutral] You've got her chin. Give me the letter.
(The PC hands over Mum's Letter. Larch reads it. WAIT 90. She folds it very carefully and puts it on the bench.)
[portrait: LARCH, sad] Last winter. And nobody told me until you were already on a boat.
[portrait: LARCH, neutral] Your mother was the bravest coward I ever knew. Sit.
MOVE: Larch pours two cups from the kettle. The liquid is dark green.
[portrait: LARCH, neutral] Drink. It's disgusting.
> Drink it.
  It tastes like a harbor at low tide. You keep it down. Barely.
  [portrait: LARCH, happy] Ha! Nobody finishes the first one. Ines didn't.
> Pretend to drink it.
  [portrait: LARCH, deadpan] I've watched forty people pretend. You're the worst at it.
> ...
  [portrait: LARCH, deadpan] It doesn't get better if you stare at it. I've tried.
[portrait: LARCH, neutral] She told you nothing, I take it. "Go to Imelda." That's Ines. Hand me a child and a mystery and die before I can shout at her.
[portrait: LARCH, neutral] Did they scan you at the dock?
> Yes.
  [portrait: LARCH, angry] She wrote ONE instruction about that. *(anger vein)* ...Not your fault. What did it say?
> It said NULL.
  [portrait: LARCH, neutral] ...
(Both continue:)
[portrait: LARCH, neutral] Null. Right. Well. That's that, then.
MOVE: Juno has turned around and is staring. A seed packet slides off the bench.
[portrait: JUNO, shocked] Professor, is this— are they— is this the ferry person?!
MOVE: Juno stands up. The veil does not; the Wooper is still on it.
[portrait: LARCH, deadpan] This is \PN. \PN, this is Juno Hale, my assistant. She'll tell you about larches now. I can't stop her. Nobody can.
> (Look at the flowers.)
  [portrait: JUNO, happy] Oh! They're my aunt's. Aunt Elin's tree, in Verdance. They never wilt. Not once in twelve years. You can touch one. Gently. They're older than the Wooper.
> ...
  [portrait: JUNO, happy] You're looking at the flowers. Everyone does. They're my aunt's. I'll tell you about it some time when I'm not about to tell you about larches.
[portrait: JUNO, happy] Did you know larches are the only conifers that drop their needles? Every winter they look dead. They're not!
[portrait: JUNO, happy] They're just letting go so they don't snap. Professor says it's the most sensible thing a tree's ever done.
[portrait: LARCH, deadpan] I said it once. In 296.
[portrait: LARCH, neutral] Right. You can't walk Velmora with empty pockets. Come through to the Sanctuary. Both of you.
```

### EV "Starter table" (the Wayfarer Sanctuary annex)
```
(A glasshouse full of small Pokémon from every corner of the world, in pens and on perches.)
[portrait: LARCH, neutral] The Wayfarer Sanctuary. Twenty years of colleagues abroad sending me Pokémon that weren't born here, so I could watch how the Imprints take hold of them.
[portrait: LARCH, neutral] They all pick up a tint in a few weeks. Every one. I've never had one that didn't.
[portrait: LARCH, neutral] *(a look at the PC)* ...Never had one.
[portrait: LARCH, neutral] Pick a partner. Any of them. Take your time, it's the only decision today I trust you with.
(STARTER SELECTION UI: any Gen 1–9 starter, grouped Grass / Fire / Water.)
[portrait: LARCH, happy] (on confirm) Good. It liked you before you chose it. I was watching.
Script: Prismfall.record_starter($player.party[0])
Switch S103 CH1_STARTER_GOT = ON.
(Received: POKÉDEX — "Fitted with a Meridian Imprint Reader. Larch has put tape over half of it.")
[portrait: JUNO, happy] My turn! Um. Um um um.
MOVE: Juno walks the pens, stops at the starter weak to the PC's.
[portrait: JUNO, happy] This one. It was looking at me.
[portrait: LARCH, deadpan] That one's at a disadvantage against \PN's, Juno.
[portrait: JUNO, happy] Somebody should give the underdog a chance! Also it was LOOKING at me.
SE: a crash from the loft. Hay falls. *(shock lines)* on everyone.
MOVE: Kestrel drops from the loft ladder, brushing straw off a black coat that's too big for him.
[portrait: LARCH, angry] Kestrel Vane. How long have you been sleeping in my hayloft?
[portrait: KESTREL, deadpan] Since Gran changed the lighthouse lock. So, Tuesday.
[portrait: KESTREL, neutral] You're handing out partners to ferry tourists now? I've asked you for one for two years.
[portrait: LARCH, neutral] You asked me twice, and both times you'd just set something on fire.
[portrait: KESTREL, smug] One of those was an accident.
MOVE: Kestrel walks straight to the starter strong against the PC's and picks it up.
[portrait: KESTREL, smug] This one.
[portrait: JUNO, angry] You only picked that because it beats theirs!
[portrait: KESTREL, deadpan] Yes. Fair fights are for people who can afford to lose.
(Larch looks at him for a long moment. *("..." bubble)*)
[portrait: LARCH, sad] ...Take it. Your mother would've done the same thing, with the same face.
[portrait: KESTREL, angry] Don't talk about her. *(anger vein)*
MOVE: Kestrel exits. At the door: 
[portrait: KESTREL, neutral] Ferry kid. Outside. Let's see if you're worth the boat fare.
```

## Map 100 — outside the station: **EV "Kestrel K1"**
```
[portrait: KESTREL, neutral] You came in on the last ferry? Great. Velmora's sinking and they're still letting tourists on.
> I was born here.
  [portrait: KESTREL, shocked] ...Then you left, and came BACK? That's worse. *(question mark)*
> I'm not a tourist.
  [portrait: KESTREL, smug] Prove it.
> ...
  [portrait: KESTREL, angry] Say something! Gran does that. The staring. I hate the staring. *(anger vein)*
Script: Prismfall.rival_battle(:RIVAL_KESTREL, "Kestrel", 1, can_lose: true)
(WIN:)
  [portrait: KESTREL, shocked] ...With the type disadvantage. *(shock lines)*
  [portrait: KESTREL, angry] Fine. You're not a tourist. You're a problem.
  Script: pf_bond_add(:KESTREL, 1)
(LOSE:)
  [portrait: KESTREL, smug] Boat fare: wasted.
  [portrait: KESTREL, neutral] ...Your partner didn't quit, though. Mine would've bitten me. Huh.
(Both:)
MOVE: Juno runs out of the station.
[portrait: JUNO, happy] That was amazing! Both of you! We should have a team name!
[portrait: KESTREL, deadpan] There's no team.
[portrait: JUNO, happy] Team Compost! Because we break things down and make them better!
[portrait: KESTREL, deadpan] I'm not in it.
[portrait: JUNO, happy] He's in it.
MOVE: Kestrel leaves west, toward the lighthouse. *(anger vein)*
Switch S104 CH1_K1_DONE = ON.
```

## Map 103 — **EV "Rowan Ashby"** (appears in the station after S104)
```
(A tall, weathered man is sorting seed trays with Juno. Soil under his nails. A small, sickly Phantump sits on his shoulder.)
[portrait: JUNO, happy] Uncle Rowan! This is \PN! They came on the ferry and they beat Kestrel — or nearly — and we're a team now!
[portrait: ROWAN, happy] Are you, now. Rowan Ashby. I keep the garden at Verdance, and this one's aunt kept me.
[portrait: ROWAN, neutral] I came down for seed stock. And to check on the Professor's tea plants. They're thriving. I can't account for it.
[portrait: LARCH, deadpan] Spite.
[portrait: ROWAN, neutral] Came the long way, too. The forest road's glass past Briarwick, so it's round by the coast and Saltmere now.
[portrait: ROWAN, happy] They're putting the Pageant on early this year. Whole town's in rehearsal. Lot of fuss over a play.
[portrait: ROWAN, neutral] This is a Phantump. I found it up past Briarwick, in a wood that's gone to glass. It was sitting in a glass tree, crying.
[portrait: ROWAN, sad] Its tree couldn't die properly, you see. So it couldn't either.
[portrait: JUNO, sad] That's so sad...
[portrait: ROWAN, neutral] It's not sad that things die, Juno. Everything that grows must be allowed to. That's what makes room.
MOVE: Rowan reaches out and touches one of the blossoms in Juno's wreath, very lightly, the way you'd touch someone's hand.
[portrait: ROWAN, neutral] What's sad is when they're not let.
(The Phantump drifts off his shoulder and hovers in front of the PC. It stops shivering.)
[portrait: ROWAN, shocked] ...Well. It hasn't gone near anyone but me in a month.
[portrait: ROWAN, neutral] *(to the PC)* She'd have liked you.
> Who?
  [portrait: ROWAN, sad] My wife. Elin. ...She's still in the garden. Come and see it someday.
> ...
  [portrait: ROWAN, neutral] Hm. You're a good listener. It's rarer than badges.
(Received: MIRACLE SEED. "From the Warden of Verdance's own stock.")
```
*Rowan, later lines:* `[portrait: ROWAN, neutral] The gate at the dock gave me green, same as every year. Twenty-four years of green. A man could get tired of a color.`

## Map 100 — Juno's errand hook
```
[portrait: JUNO, panic] \PN! Mum's Skwovet's got out again. Biscuit. He's gone to the Pruett orchard and I'm not— nobody's supposed to go in there.
[portrait: JUNO, neutral] Will you come and look? Just LOOK. From the outside. I'll show you the way.
QUEST LOG: "Biscuit" — Go with Juno to the old orchard on Windfall Row.
(Juno becomes a follower.)
```

## Map 520 — The Ferrymen's Mile (coastal farm lane; BGM: route theme, light)
```
ROUTE SIGN: THE FERRYMEN'S MILE — Ferrow's Landing ↔ Hale's Bramble ↔ Windfall Row. Mind the hedges. The hedges mind you.
[name: Youngster Pim] A trainer! With a real partner! Fight me, I've got a Bidoof and a dream!
  (Trainer battle. After:) [name: Pim] The dream's fine. The Bidoof needs a minute.
[name: Lass Dory] My Fletchling only knows Tackle and judgment. (Trainer battle. After:) It's judging me now.
[name: Farmhand] Tall grass is where the wild ones are. Juno'll tell you their Latin names. Nobody asked her to learn those.
(First tall grass step, Juno:) [portrait: JUNO, happy] Catching tutorial! Weaken it, then throw. Don't throw the Ball AT it, throw it NEAR it. I learned that the hard way. Sorry, Biscuit.
  (Received: POKÉ BALL ×5.)
HIDDEN ITEM (under the stile): POTION. "Left by a farmhand with a guilty conscience."
SCARECROW (action): It's wearing a Meridian linesman's cap. Somebody has a sense of humor.
```

## Map 523 — Hale Farmhouse (Hale's Bramble)
```
KITCHEN TABLE: Six chairs. One has "JUNO" carved in it. One newer carving beside it says "\PN". The knife is still on the table.
[portrait: WENNA, happy] (if home) I had Coll carve it. Don't make it strange. Sit when you like.
BOOKSHELF: "Berries of the South Coast", annotated in tiny handwriting: "WRONG." "ALSO WRONG." "Ask Uncle Rowan."
JUNO'S ROOM: Seed packets pinned to the wall like butterflies. One is labeled "MYSTERY (do not eat) (I ate one) (do NOT eat)".
BED (action): You could rest here. (Heals the party.)
HEADBUTT TUTOR (farmhand in the yard): Want your partner to learn to headbutt trees? Things fall out. Usually Pokémon. Once, a boot.
```

## Map 522 — The Glassed Orchard (`:BLEED`; BGM cuts to wind chimes)

### EV "Bleed Veil" (touch, at the orchard gate)
```
(Rows of apple trees turned to clear glass. Glass apples chime in the wind. The air at the gate shimmers like heat.)
[portrait: JUNO, sad] There. That was the Pruetts'. It went last winter, in one night.
[portrait: JUNO, neutral] It's pretty, isn't it? I hate that it's pretty.
SE: a squeak from inside. A Skwovet is visible on a glass branch.
[portrait: JUNO, panic] Biscuit! Biscuit, come OUT!
MOVE: Juno steps toward the shimmer and stops hard. *(shock lines)*
[portrait: JUNO, panic] Ow— no. No. My skin's burning. I can't.
[portrait: JUNO, sad] That's the Veil. Nobody can cross one. You just... can't. Your body won't.
(The PC is prompted to step forward. MOVE: PC walks through the shimmer. Nothing happens. WAIT 40.)
[portrait: JUNO, shocked] *(shock lines)* ...How are you DOING that?
> I don't know.
> It doesn't hurt.
> ...
[portrait: JUNO, shocked] Doesn't it— aren't you— your HAIR isn't even standing up!
```
**Game over `GO_ORCHARD`** (prompt appears once the PC is inside and talks to Juno across the Veil)
```
[portrait: JUNO, neutral] Can you pull me through? Just for a second? I only want to grab him.
> No. Stay there.
  [portrait: JUNO, sad] ...Right. Yes. The Professor did say never. Sorry. Go on, I'll shout directions.
> Take her hand.
  [portrait: JUNO, happy] On three. One, two—
  (SE: glass ringing. Juno's sprite turns clear from the fingertips up. WAIT 60.)
  [portrait: JUNO, shocked] \PN, I can't feel my—
  Script: Prismfall.game_over(:GO_ORCHARD)
```
*(Foreshadowing already delivered: her "My skin's burning", and Larch's line in the station bookshelf below.)*

### Inside the orchard
```
EV "Glass farmhand": A man made of glass, mid-step, a glass basket on his arm. His mouth is open. He was calling someone.
  (Inspect again:) Inside the glass, very faintly, his eyes are moving.
EV "Glass apple" (item): GLASS APPLE. "It rings when you flick it. Don't bite it. (Sells for ₽500.)"
EV "Glassed Wurmple" (blocks the path; a swarm leader, half crystal):
  It hisses. Its body grinds like a jar of marbles.
  (Wild battle, Lv 6, field `:BLEED`. First FIELD NOTES pop-up: "THE BLEED — unstable. Borrows effects from other fields. Do not trust the ground.")
  (After the battle, win or flee:) The Wurmple stops grinding. It looks at you. Then it curls up against your shoe and goes to sleep.
  The rest of the swarm settles in the branches, one by one.
EV "Wild Carbink" (optional, back row): It is licking a glass tree. It seems very happy about the whole situation. (Catchable.)
EV "Lost Skwovet":
  Biscuit has stuffed his cheeks with glass apple seeds. He rattles when he moves.
  He climbs onto your head. This is apparently how this works.
```

### EV "Professor Larch" (at the gate, on exit) — comedy scene Ch1, "Lecture One"
```
(Larch is standing next to Juno with a notebook. She has clearly run the whole way.)
MOVE: PC walks out through the Veil with Biscuit on their head.
[portrait: LARCH, neutral] So. You walked through a Bleed Veil.
[portrait: LARCH, neutral] Into a Bleed zone. On your first day. To fetch a Skwovet.
> It was stuck.
[portrait: LARCH, angry] IT LIVES IN A TREE. IT IS ALWAYS STUCK. THAT IS ITS ENTIRE ARRANGEMENT WITH TREES. *(anger vein)*
[portrait: JUNO, happy] Technically Skwovet are scansorial, so—
[portrait: LARCH, angry] Juno.
[portrait: JUNO, panic] Shutting up! *(sweat drop)*
[portrait: LARCH, crying] Your mother wrote me one instruction. One! "Keep them out of trouble, Imelda." It has been NINE HOURS.
[portrait: LARCH, crying] I'm not crying. It's the tea. The tea is very strong.
(WAIT 30. Larch looks at the sleeping swarm in the glass trees, then at the PC.)
[portrait: LARCH, neutral] ...They calmed down. When you went near them.
[portrait: LARCH, neutral] Well. That's that, then.
MOVE: Larch writes in the notebook. 
[portrait: LARCH, neutral] Listen to me, both of you. Never take a tinted person past a Veil. Never. It isn't pain that stops them. It's the body knowing.
[portrait: LARCH, neutral] And you. This is Lecture One. I'm numbering them. I have a feeling.
(Received: FIELD NOTES — "Professor Larch's field encyclopedia. It fills in as you meet new fields.")
Switch S105 CH1_ORCHARD_DONE = ON. Quest "Biscuit" complete: Wenna gives 3 ORAN BERRIES and "another tart, for the nerves. Mine."
Script: pf_bond_add(:JUNO, 1)
```
*Station bookshelf (map 103), readable any time:* `"Field safety, rule one, underlined three times: NEVER TAKE A TINTED PERSON PAST A VEIL."`

## Map 105 / 106 — Ferrow Lighthouse (evening; optional but signposted)
```
DOOR (before S105): Locked. A note: "KESTREL. NO."
DOOR (after S105): Ajar.
1F: Coils of rope, a cot with a boy's coat on it, a cracked mirror by the door.
CRACKED MIRROR (action): Your reflection, split down the middle by an old crack.
  (Talk to Hesper about it:) [portrait: HESPER, angry] Leave it. It shows the truth crooked, same as everything.
TRUNK: Locked. A black lace veil is caught in the lid.
```
**EV "Hesper Vane"** (lamp room)
```
(An old woman is polishing the great lamp with a rag. She is shouting down the stairwell.)
[portrait: HESPER, angry] —and if I find straw in my good boots AGAIN, Kestrel Vane, I'll— 
MOVE: Hesper turns and sees the PC. The rag drops. *(shock lines)* WAIT 60.
[portrait: HESPER, shocked] ...
[portrait: HESPER, angry] Who let you up here? Get out. Lighthouse is closed. Sea's closed. Everything's closed.
> Do you know me?
  [portrait: HESPER, angry] I don't know anybody. I'm seventy-eight. I've forgotten more people than you've met.
> I'm sorry.
  [portrait: HESPER, sad] ...Don't be sorry. Sorry's no use to a lamp.
> ...
  [portrait: HESPER, sad] Stars. You even stand like— no.
[portrait: HESPER, neutral] You're the one the boy fought on the quay. He came home swearing. That means he liked it.
[portrait: HESPER, neutral] Keep away from him. Everyone who gets near that boy's mother's ghost gets hurt.
MOVE: Hesper picks up the rag and turns her back.
```

## End of Chapter 1 — cutscene (plays when the PC sleeps at the farmhouse or the inn after S105)
```
(Night. Tidewatch Station, one lamp. Larch alone at the bench with a cold cup and the notebook.)
TEXT (handwriting): "Subject reads NULL. Calms Bleed-struck fauna on approach. No tint after one day; I do not expect one after a hundred."
TEXT: "Second such reading in my life."
TEXT: "The first was in Crownhaven, AF 290."
TEXT: "God help us, Ines."
(She closes the notebook. Outside the window, far across the harbor, the lighthouse lamp turns. In its beam, for one frame, a figure in a too-big coat is standing on the gallery, looking at the station.)
V102 STORY_CHAPTER = 2.
```

---
*(Chapter 2 continues below.)*

# CHAPTER 2 — "Curtain Call"

**Chapter start:** the morning after (V102 = 2). Larch sees the PC off at the stile on the Ferrymen's Mile.
```
[portrait: LARCH, neutral] Eighteen gyms. Saltmere's first. The forest road to Briarwick's corded off — the Glasswood's walked across it — so you go round by the coast.
[portrait: LARCH, neutral] Two days on foot. Chalk cliffs, then dunes, then the free port. The Warden's Dorian Pell. He'll call you "darling" and mean it about a third of the time.
[portrait: LARCH, neutral] Write to me. I mean it. Gale Post, every town. If I don't hear from you in a week I start Lecture Two by post.
[portrait: JUNO, happy] I'm coming as far as Saltmere! Mum's promised forty tarts to the Pageant crowd and I'm the cart!
[portrait: JUNO, happy] And I've wanted to see the Pageant since I was six. There's a bit where the Plates fall and they use REAL glitter.
[portrait: LARCH, deadpan] They use salt.
[portrait: JUNO, shocked] ...Why would you tell me that. *(shock lines)*
(Received: TOWN MAP. "Larch has drawn a skull on the Glassed Orchard, a skull on the forest road, and a smaller skull on her own kettle.")
QUEST LOG: "Eighteen Roads" — Earn the first badge in Saltmere, west along the coast.
(Juno becomes a follower.)
```

## Map 520 — The Ferrymen's Mile: the Hale Bell and the quarantine line
**EV "Accord guard"** (roadblock at the Hale Bell, where the Strand Road turns west; lifts once S105 is on)
```
[name: Accord Guard] Hold. Quarantine order: nobody leaves the Landing without papers.
[name: Accord Guard] ...You've got a Badge Case. A challenger. Right. Challengers pass, that's older law than the quarantine.
[name: Accord Guard] "Eighteen in Concord, One in Keeping." On you go. Saltmere's two days west. Mind the cliff path in wind.
```
**EV "Accord guard (aside)"**
```
[name: Second Guard] *(low)* That's the null one from the dock. Captain said let them through, whatever happens.
[name: Accord Guard] Which captain?
[name: Second Guard] Didn't say. Came down from Crownhaven with a white seal on it.
(They notice the PC listening. *(sweat drop)* ×2.)
[name: Accord Guard] Lovely weather.
```
```
THE HALE BELL (action): A ship's bell on a post above the sea cliff. The ferrymen rang it once the last boat was in. A cloth has been tied round the clapper.
[portrait: JUNO, sad] Dad tied that. The night they closed the strait. He said there wasn't anything left to ring for.
[name: Hay-cart Driver] Used to take me four hours to Briarwick and back by the forest road. Now it's all glass and I go round by Saltmere. Two days. Glass doesn't pay my horse.
```

## Map 521 — Windfall Row: the forest-road cordon (Chapter 2 lines)
```
ROAD SIGN [NEW]: WINDFALL ROW — ← Gossamer Wood & Briarwick (ROAD CLOSED BY ORDER OF THE ACCORD). Orchard law: keep what has fallen, and nothing else.
```
**EV "Forest-road cordon"** (Accord tape across the lane into the Gossamer; opens from the wood's side once the Glass Matriarch is beaten, V105 ≥ 1)
```
(Tape across the forest lane. Beyond it, a mile into the trees, something catches the light the wrong way.)
[name: Cordon Warden] Forest road's shut. The Glasswood's across it. Nobody walks it till the Warden in Briarwick says so.
[name: Cordon Warden] Go round by the coast like everyone else. Saltmere, then the Weavers' Road up the river. It's two days. It's a nice two days.
[portrait: JUNO, sad] It used to be four hours. Uncle Rowan and I walked it every summer with a donkey called Parsnip.
[portrait: JUNO, neutral] Parsnip hated the forest. Parsnip was right, as it turns out.
```
*[after V105 ≥ 1, from the Gossamer side]* `[name: Cordon Warden] The glass went back a mile overnight. Road's open. Don't ask me how. I just roll up tape.`

## Map 527 — Lacecliff Walk [NEW map] (`:BEACH`; BGM: route theme with sea)
```
ROAD SIGN: LACECLIFF WALK — The Strand Road. → The Ferrymen's Mile · ← Marram Down & Saltmere. The arches are older than the Accord. Please do not improve them.
(Chalk cliffs worn by the sea into arches as fine as lace. The path goes through three of them.)
[portrait: JUNO, happy] The Briarwick weavers copy these cliffs for their lace. Not the other way round. The sea did it first.
[portrait: JUNO, happy] The sea does most things first. It's very annoying of it.
```
Route trainers and flavor (levels per BALANCE 4b, Gym 1 stretch):
```
[name: Fisher Bryn] The strait's closed and the fish haven't been told. (Battle. After:) The fish win again.
[name: Beachcomber Moll] I found a bottle with a letter in it! It's from my sister. She lives forty yards that way. (Battle.) [after] She writes every week. She's never once walked over.
[name: Painter at an easel] Hold still. No — you're in the light. No — you ARE the light. Hm. You don't really show up on the canvas, do you? Odd.
[name: Hiker Dunstan] Cliff path in a gale's a fine way to die. Cliff path in sun's a fine way to live. (Battle.) [after] Today's a sun day. Lucky you.
[name: Hermit at the Wrecker's Lamp] It's for the gulls. The lamp. Not for ships. I don't know anything about ships. Who said ships?
[name: Birder] Wingull nest on that stack. Two hundred of them. I've named eleven. The rest won't hold still.
```
**Comedy beat: "The Lacemakers' Bench"** (a carved stone seat at the second arch; touch)
```
[portrait: JUNO, happy] Sit! You have to sit! It's the Lacemakers' Bench. Everyone who walks the Strand sits here or the cliffs fall in.
> Is that true?
  [portrait: JUNO, deadpan] No. But they haven't fallen in, have they.
> (Sit.)
(The PC sits. Juno sits. A Wingull lands on the end of the bench. Nobody says anything for a while. The sea does most of the talking.)
[portrait: JUNO, neutral] ...This is nice. I don't get to sit. I'm always going somewhere with a basket.
[portrait: JUNO, happy] Right! That's enough nice! Saltmere!
(The party is healed.)
```
```
SMUGGLERS' SIGNAL POLE (action): A tall pole with a lantern hook. From here you can see the Ferrow lighthouse. Its beam sweeps past, then stops on you for a second longer than it should, then moves on.
HIDDEN ITEM (under the third arch): PEARL. "The tide left it. The tide will want it back."
```

## Map 528 — Marram Down [NEW map] (`:BEACH`; BGM: route theme with sea)
```
ROAD SIGN: MARRAM DOWN — Free Port of Saltmere, 1 mile. Pulling up the marram grass is fined. Yes, even that one.
FREE PORT CHARTER STONE (by the stile): "By grant of Sovereign Maren, AF 41: SALTMERE ANSWERS TO THE ACCORD AND TO NO CROWN." Someone has carved underneath, smaller: "AND BOOS THE REST."
```
**EV "The Saltmere Beacon"** (the highest dune; the keeper heals once)
```
(From the top of the dune, the free port opens below: a white town on a salt lake, striped awnings, lantern masts, and a theater on every second corner.)
[portrait: JUNO, happy] Saltmere! Look at it! Everything's ordinary! Isn't it WONDERFUL?
[portrait: JUNO, happy] The Blank Plate's under there somewhere. Nothing strange ever happens in Saltmere. No Bleed, no glowing rivers, nothing.
[portrait: JUNO, happy] So they make it all up instead. Every night. On purpose.
[name: Beacon Keeper] Tea? It's not kelp. I've heard about the kelp.
```
**EV "The players' camp"** (the Pageant's travelling company, rehearsing the companion piece among their wagons)
```
(Three actors in hound masks are chasing a fourth, in a sad bark mask, around a wagon. A fifth is holding a script and despairing.)
[name: Hound Number One] And SO the Loyal Three drove the Gossamer Ogre from the wood—
[name: Ogre] *(muffled)* Can I take the mask off? It's very hot in the Ogre.
[name: Director with script] The Ogre does NOT take the mask off. The Ogre has never taken the mask off. It's in the text.
[name: Ogre] *(muffled)* Why does he look so sad, though? He's the villain.
[name: Director with script] Because the carver was having a bad week in AF 140! Places!
[portrait: JUNO, happy] *(whispering)* I'm going to cry at this. I know I am. I cry at the Ogre every time and I've never even SEEN it.
[name: Actor (costume double, Battle)] A rehearsal audience! Quick, a scene! (Double battle vs two actors in hound masks.) [after] Notes: we were bitten. Again.
```
**Optional: "The Prompter's Box"** (the half-buried theater barge; dig with the camp's sand-shovel)
```
(A theater barge lies half-buried in the dune, its name board reading THE WANDERING CHORUS. Costume hampers. A prop throne with three legs.)
[name: Prop-mistress at the camp] If you're digging in the old barge, there's a shovel by the wagon. The prompter's box went down with it in '71. Nobody's had the heart.
(Dig at the stern: a sealed prompter's box.)
(Received: PROMPTER'S SCRIPT. Key Item. "The company's prompt-book for the Pageant, every cue in red. In the margin by the Grand Stage scenes: 'House loves a song. House loves a dance. House HATES a long face — keep them moving.'")
(Received: NORMAL GEM.)
PROMPTER'S SCRIPT (read): A page near the back is a different paper, older, folded in. It's the last scene of "The Loyal Three", and it doesn't match the one the actors are rehearsing.
  "OGRE: I only kept the wood. They wanted the stones.
   HOUND: Lies! Bite him, brothers!
   OGRE: Then bite. The wood will remember which of us bled."
  Across the top, in a clerk's hand: "Struck by order of the Reform, AF 140. Do not perform."
```
Route trainers and flavor:
```
[name: Kite Flier] Wind off the lake's the best in Elowen. (Battle.) [after] My kite won. You beat the kite-flier, which is different.
[name: Sand-sculptor] It's the Sovereign's Crown! In sand! ...Don't look at the stone. I ran out of the good sand.
[name: Dune Guard] Free port starts at the stile. Past that, the Queen's writ doesn't run, and neither do I. (Battle.) [after] I'm going to sit down now. That's allowed in a free port.
HIDDEN ITEM (in the sand-sledge run's end): SOFT SAND. "Yes. Very."
```

## Map 140 — Saltmere, the Promenade & Market (BGM: harbour waltz, accordion and glockenspiel)

### Arrival (autorun, first entry by the East Gate)
```
(Lamplit promenades along a white salt lagoon, striped awnings, salt-caramel smoke. On the lagoon, a long green barge flying Elowen's briar crown is rowing toward the harbour mouth.)
SE: a horn from the breakwater. Along the whole breakwater, a hundred people stand up at once.
[name: The Breakwater] BOOOOOOOOOOOO.
MOVE: the green barge turns, slowly, and rows away.
[portrait: JUNO, deadpan] That's the Queen's tax-barge. They do that every week. It's tradition. The barge comes, everyone boos, the barge goes.
[portrait: JUNO, neutral] Mum says it's the only time in history a tax has been defeated by noise.
[portrait: JUNO, happy] I'm taking the tarts to the Lantern Theatre! Find me on the green after. Don't go into the gym without me! I need to be AUDIENCE!
MOVE: Juno runs off east toward the Lantern Theatre. (She stops following.)
```
### EV "Dorian at the breakwater" (first meeting; the end of the breakwater, map 146)
```
(At the end of the breakwater, a man in a velvet coat lowers a silver-topped cane he very clearly does not need. He was conducting the booing.)
[portrait: DORIAN, happy] *Enter, stage left, a stranger!* No — a challenger. That's a Badge Case. On booing day! The gods of theater are kind.
[portrait: DORIAN, smug] Dorian Pell. Warden of Saltmere, Pageant-Master to the Accord, and for thirty-one consecutive years, Saltmere's Most Eligible Something.
[portrait: DORIAN, neutral] You saw the barge? The Queen sends it every week. Our charter says we answer to no crown. Every week we remind her, in the only language a crown understands.
> Booing?
  [portrait: DORIAN, happy] Volume, darling. Volume.
> Isn't that rude?
  [portrait: DORIAN, smug] Profoundly. That's what makes it diplomacy.
> ...
  [portrait: DORIAN, neutral] Ah. A critic. We get a few. We feed them to the Ogre.
[portrait: DORIAN, neutral] Saltmere is the only city in Velmora where nothing is a miracle, darling. So we built our own. Every night, at eight.
[portrait: DORIAN, neutral] The Playhouse is in the Old Town. Come when you're ready, not before. A first gym should be an occasion.
[portrait: DORIAN, happy] And the Pageant opens tonight at the Lantern Theatre. I wrote none of it and I'm in all of it.
```
*Reactive (after S108):* `[portrait: DORIAN, sad] I've stood on this breakwater for thirty years telling a queen she can't have us. Last night someone walked onto my stage and took us anyway.`

### Named residents
**The Woman from the ferry** (Prologue's "Woman with crate"; promenade)
```
[name: Woman from the ferry] You! From the Dovetail! I'm home! I'm not grey anymore. Look at me. I'm BEIGE.
[name: Woman from the ferry] Blank tint. Saltmere. The gate said so. My sister cried.
```
**Sella the Saltwife** (Saltwife's House, map 144)
```
[name: Sella] Saltmere salt tastes of nothing. That's how you know it's ours. Everyone else's salt tastes of where it's from.
[name: Sella] Take a pinch for your road. Put it on anything. It'll taste of whatever it was already. That's the Blank Plate for you: it never changes your mind.
(Received: a pinch of SALTMERE SALT. Flavor item. "It tastes of nothing at all.")
```
**Harbourmaster Quill** (Harbour Office, map 143)
```
[name: Quill] Free port means free. Meridian's ships pay the same dues as a fishing smack. Mr. Voss is very gracious about it.
[name: Quill] He has a lawyer who is less gracious. She's been in my office four times this spring. She brings biscuits. I don't trust the biscuits.
```
*[after S108]* `[name: Quill] The Queen's herald came by boat this morning. First time a Crown boat's tied up here in eighty years. Nobody booed. That's how frightened everyone is.`

### Flavor townsfolk (Saltmere promenade, harbour and Old Town)
```
[name: Caramel Seller] Salt-caramel! Fresh salt-caramel! Pageant tonight — the Loyal Three companion piece!
[name: Caramel Seller] (again) It's mostly salt. That's the secret. Don't tell anyone. Everyone knows.

[name: Busker] Saltmere's Plate makes everything ordinary — no Bleed, no miracles. So we make our own, on stage!
[name: Busker] (again) I've played this corner twenty years. Not one strange thing has happened to me. I find it very hard to write songs.

[name: Lamplighter] No Meridian lamps on the promenade. The Warden says these lamps are part of the set. Meridian can light the rest of Velmora; the set stays oil.

[name: Stagehand on a smoke break] Opening night's tonight. The Accord sends an inspector to make sure we say every line of the official text.
[name: Stagehand on a smoke break] (again) He sleeps through the second act. We've timed it. Eleven minutes in, every year.

[name: Fisherman] Ordinary fish. Ordinary sea. Fifty years and never seen a thing out of the way. I find that very restful.

[name: Child with an Ogre puppet] The Ogre steals the Plates and the Three bite him! Then everyone claps! Then there's caramel!
[name: Child with an Ogre puppet] (again) I like the Ogre. Don't tell anyone. He's got a nice face.

[name: Retired Actor on a bench] I played a king once. In a play they closed before the dress. I'm not allowed to say which.
[name: Retired Actor on a bench] (again) Better part than Ogre, I'll tell you that. The Ogre never gets a speech.

[name: Hound Number Two] I'm Hound Number Two! I bite on the beat! The beat is "GRR". I have to wait for Hound Number One's "GRR" and then I go "GRR".

[name: Grey Pilgrim] Lovely night for a play. Sit near the back, child. You'll see more from the back.

[name: Rival Theatre Barker] TONIGHT at the Little Lantern: "THE PAGEANT OF THE PAGEANT", a play about a man who stages a pageant! Starring nobody you'd know!
[name: Rival Theatre Barker] (again) Dorian's seen it nine times. He says it's "to gather evidence". He laughs at all the right parts.

[name: Fishwife] You've no tint at all? In Saltmere that's barely worth gossip. We're all Blank here. You're just Blanker.

[name: Accord Inspector] I have a copy of the official text. Every word approved. I will be following along. Closely. Until the second act.

[name: Meridian Clerk] We're not trying to light Saltmere. We're just asking. Every week. Politely.

[name: Old Sailor] Saltmere won't wilt you, they say. Born here, live anywhere. It's the one Plate that doesn't hold on. Kindest Plate there is.
```
*[after S108, town-wide variants]*
```
[name: Caramel Seller] Nobody's buying. Nobody wants anything sweet this morning.
[name: Busker] Strange thing happened to me last night. First time in twenty years. I'd like it back the way it was, please.
[name: Child with an Ogre puppet] The real Ogre came. He didn't steal anything. He just talked. Mum says don't talk about it.
[name: Grey Pilgrim] (gone. A grey cloak lies folded on the bench, with a lily on it.)
```

### Signs and objects
```
TOWN SIGN: SALTMERE — The Free Port. Answers to the Accord and to No Crown. (Booing Tuesdays.)
PAGEANT POSTER: "THE PAGEANT OF THE PRISMFALL — a Gift of Love from the Original One. Festival Year: Opening Night! With the companion piece THE LOYAL THREE. By leave of the Accord."
FESTIVAL POSTER: The same poster as the Landing. The painted Crown's stone has the same tiny dark fleck. Nobody here has bothered to circle it.
KESTREL AT THE POSTER (event, once, from the promenade): A boy in a too-big black coat is reading the Pageant poster very closely. When you look again, he's gone.
PROMENADE LAMPS: Oil lamps on iron posts. Each has a number, and a playbill pasted to it.
HIDDEN ITEM (under the caramel stall): LEMONADE. "Someone was saving it for the interval."
HIDDEN ITEM (end of the breakwater): STARDUST. "It blew in on the salt."
```

### Sidequest A — "Hound Number Three"
```
(Hound Number Two, second talk:)
[name: Hound Number Two] Hound Number THREE has run off! Not the actor, the actor's Lillipup! It does the real barking! We can't do the Loyal Three with two hounds! It'd be the Loyal Two! That's a different play!
QUEST LOG: "Hound Number Three" — Find the Lillipup that does the barking.
(The Lillipup is in the Old Town (147), sitting outside the Little Lantern, watching "The Pageant of the Pageant" through the door.)
[name: Lillipup] Rrrf.
> Bring it back.
  It comes. It looks back at the Little Lantern once, longingly.
[name: Hound Number Two] You found it! You're a hero! Here, this is from the costume trunk. Nobody's missed it in forty years.
(Received: SOOTHE BELL. "Off a costume called 'Shepherdess (Comic)'. It rings very sincerely.")
```

### Sidequest B — "The Inspector's Text"
```
(Accord Inspector, after S108, on the promenade with his copy of the official text open, staring at nothing:)
[name: Accord Inspector] Every word approved. I've followed every word for nineteen years. Last night a man said four sentences and none of them are in here.
[name: Accord Inspector] I've been asked to report what was said. Word for word. I didn't write it down. I was... I was listening.
> Tell him what the Mourner said.
  [name: Accord Inspector] *(writing)* "...ever rots." "...underwater." "...collars." Collars. Yes. Thank you.
  [name: Accord Inspector] I'm going to send this to Crownhaven, and then I am going to take a very long walk.
> Tell him you don't remember.
  [name: Accord Inspector] No. Nor do I. Nor does anyone. That's what I'll write. "Nobody remembers." It's the safest sentence in the language.
(Either way, received: ₽1500, "from the Accord's discretionary fund for cooperative citizens".)
```

## Map 141 — Pokémon Center / Map 142 — Mart / Map 147 — the Old Town
```
POKÉMON CENTER:
[name: Nurse] We heal for free. The scanner at the door says "Blank, Saltmere" for everyone. It's had a very dull spring.
[name: Trainer] The Playhouse is all aisle and no tricks. Dorian doesn't do puzzles. He says the play's the thing.
GALE POST DESK [NEW]: A letter is waiting. "Saltmere: eat a caramel, it's mostly salt, it's good for you. Lecture Two is drafted. — I.L." (Received: POTION ×2, and a tea bag. ITEM: KELP TEA BAG. "You could throw it away. You don't.")

MART:
[name: Clerk] Antidotes? Nobody here gets poisoned. Nobody here gets anything. Have a Potion, it's very ordinary.
[name: Customer] I asked for a Synthetic Seed and the clerk said "in Saltmere?" in a voice. I bought a Potion.

OLD TOWN (147):
SIGN: THE PELL PLAYHOUSE — SALTMERE GYM. WARDEN: DORIAN PELL. "Every pageant is a lie. The trick is choosing which lie to tell."
SIGN: THE LITTLE LANTERN — "THE PAGEANT OF THE PAGEANT." Held over. Held over again. Held over by D. Pell, who has bought every Thursday.
[name: Street Juggler] I juggle for coins. In Saltmere the coins are the only thing that falls the way you expect.
[name: Costumed Usher] Programmes! A copper! Dorian's face on every page, free of charge!
```

## Map 140 — **EV "Juno J1"** (the promenade green; S109)
```
(Juno is on the promenade green beside the planters, practising a victory pose with an empty tart basket.)
[portrait: JUNO, happy] There you are! Tarts delivered! Forty! I ate one. Thirty-nine!
[portrait: JUNO, neutral] Before you go in there... fight me?
[portrait: JUNO, happy] Not a FIGHT fight. A spar. I want to know if I'm any good before you go off and get good without me.
[portrait: JUNO, neutral] And I want to know if YOU are. I'm going to be in the audience. I'd like to know what I'm cheering for.
> Let's go.
> Are you sure?
  [portrait: JUNO, deadpan] My partner's weak to yours and I chose it on purpose. I've never been less sure of anything. Let's go!
Script: Prismfall.rival_battle(:RIVAL_JUNO, "Juno", 1, can_lose: true)     # J1; field :MEADOW (FIELD_DEFAULTS exceptions: the promenade green)
(WIN:)
  [portrait: JUNO, happy] You're good. You're REALLY good. *(music note)* That's so annoying. I'm so happy.
(LOSE:)
  [portrait: JUNO, shocked] I WON? *(shock lines)* ...Did you let me win? Don't tell me. I'm keeping it.
(Both:)
[portrait: JUNO, happy] Here, for your partner. They're from the farm.
(Received: ORAN BERRY ×2.)
[portrait: JUNO, happy] Go on, then. The Playhouse is in the Old Town. I'll be in the cheap seats. I'll be LOUD.
Switch S109 CH3_J1_DONE = ON.
```

## Map 150 — Pell Playhouse, Lobby
```
(Red plush, gilt urns, velvet ropes. Posters of past seasons. Dorian is on every one.)
[name: Usher] Ah, our challenger! Tonight's bill: Dorian Pell, in person. Through the doors, up the aisle, onto the stage.
[name: Usher] The cast may want a word on your way. Actors. They always want a word.
[name: Gym Guide] Your first Warden! Dorian uses Normal-types, on the Grand Stage field.
[name: Gym Guide] Here's the trick of a field: the house loves a show. Sound moves and dances get a cheer, and the cheer makes the next move hit harder. It works for you too.
[name: Gym Guide] Normal-types don't fear much. Fighting-types, they fear. Rock shrugs them off. And Ghosts just don't care, which Dorian finds very rude.
[name: Lady in the lobby] I come every night. Every. Night. He has never once taken a bow the same way twice.
POSTER: "THE LADY IN RED. Dorian Pell, Rosalind Vane. Held over by popular demand." (Popular demand: D. Pell.)
POSTER: "THE LOYAL THREE — the Festival-year companion piece to the Pageant of the Prismfall. Three faithful hounds! One wicked Ogre! Bring the children!"
POSTER (old, under the others): A title has been pasted over, years ago. Where the paste has lifted, two letters show through: "...ED K..."
```

## Map 154 — Pell Playhouse, Auditorium (Gym 1; layout per GYM_PUZZLES Gym 1)
```
(A small, handsome theater: velvet seats in rows, a red runner up the centre aisle, gilt boxes, and the house curtain down across the stage. The house is half full. The audience is real.)
FIELD NOTES pop-up (first battle here): "GRAND STAGE — the audience reacts. Sound moves and dances earn applause, and applause lifts the next move. Nothing on this stage is real, which is the point. (Larch, in the margin: 'Saltmere. The one place I never worry about you. Don't make me start.')"
[name: Juggler Florian] A challenger in the aisle! The show starts NOW! (Battle.) [after] I'll be in the bar. There is no bar. I'll be in the lobby.
[name: Beauty Rosalind] Every great entrance needs a rival. Tonight, that's me. (Battle.) [after] ...Upstaged. In my own aisle.
[name: Juggler Ambrose] Side aisle, cheap seats, best view! Let's have a scene! (Battle.) [after] Encore? No? No.
(Juno arrives in the stalls once one actor is beaten, with a paper cone of salt-caramel.)
[portrait: JUNO, happy] I made it! I'm AUDIENCE! *(music note)* Go on! I'll be loud!
[name: Audience Member] Shh!
[portrait: JUNO, happy] *(whispering)* I'll be loud quietly.
[name: Stagehand] Places! He won't come out till the curtain's up. That rope, there, on the apron. Give it a good haul.
CURTAIN ROPE (action): You haul on the rope. The house curtain flies out, the footlights come up — and there he is.
```
*(Once you hold Tamsin's badge, a chalked door in the stage-left wing opens on the optional Playhouse Backstage, DUNGEON_PUZZLES D9. Dorian's line for it is the puzzle engineer's; it should not hand over "The Gilded King", which Dorian keeps.)*

**Warden battle**
```
(Dorian stands center stage in a single spotlight, cane raised, as if he has been standing there for an hour. He may have.)
[portrait: DORIAN, happy] *Enter, stage left, our brave challenger!* To thunderous applause! *(the audience applauds, thunderously)*
[portrait: DORIAN, neutral] Your first Warden. Your first field. Your first audience. I envy you, darling. You only get one of each.
[portrait: DORIAN, smug] On my stage the house loves a show. Sing, dance, dazzle them, and they'll carry you. Bore them, and they'll let you fall.
[portrait: DORIAN, happy] Shall we give them something to remember?
Script: Prismfall.gym_battle(1)     # LEADER_DORIAN, :GRAND_STAGE, cap 15, single battle (GYMS double: false)
(Mid-battle, when his ace enters:) [portrait: DORIAN, smug] Costume change!
(LOSE: standard whiteout to the Pokémon Center. Dorian on retry: "Act Two! I adore an Act Two. Everyone's warmed up.")
(WIN:)
[portrait: DORIAN, shocked] ...They're standing. Look at them. They're on their FEET.
[portrait: DORIAN, crying] Bravo! BRAVO! Oh, I'm crying, don't look, it's the footlights.
(Received: the FOOTLIGHT BADGE.)
(The PC opens the Badge Case and sets the badge in. SE: a faint hum, one clear note. The whole house goes quiet. *(question mark)* over Juno.)
[portrait: JUNO, happy] Ooh. Is it supposed to do that?
[portrait: DORIAN, shocked] Darling, in Saltmere nothing is supposed to do ANYTHING. That's the whole charter. *(shock lines)*
[portrait: DORIAN, neutral] ...
[portrait: DORIAN, happy] Do it again.
(Nothing. The case is quiet.)
[portrait: DORIAN, deadpan] One night only. The best kind.
(Received: TM42 FACADE.)
[portrait: DORIAN, neutral] Facade. The art of turning a bad night into a standing ovation. You'll need it more often than you'd think.
[portrait: DORIAN, neutral] That badge is the Accord's word that Pokémon up to level nineteen will heed you. Briarwick's will let you cut the dead wood, when you've earned it. They have a man for that.
MOVE: the troupe files on from the wings. The smallest actor is carrying an Eevee in a ruff.
[portrait: DORIAN, happy] And one more gift, from the whole company. Forty auditions. Never cast. A tragedy in a ruff.
[portrait: DORIAN, neutral] You came off that ferry with no color at all, I hear, and this one's never picked one either. You two are a matched set.
(Received: EEVEE "UNDERSTUDY". Gift Pokémon, Lv 10, nickname "Understudy". Switch S110 CH3_UNDERSTUDY_GOT = ON.)
[portrait: DORIAN, happy] Rehearsal at the Lantern Theatre this afternoon, opening night at eight. Come to both. Bring Juno. Bring everyone.
```

## Map 145 — Lantern Theatre: rehearsal (after Gym 1) — **comedy scene Ch2, "Tree #3"**
```
(The Lantern Theatre: a painted forest of flats on stage, actors in hound masks, the sad-masked Ogre eating an apple on a ladder. Juno is at the edge of the stage with the empty tart basket.)
[portrait: DORIAN, happy] *Enter, stage left, our brave challenger!* And — ah! The understudy! Places, little one!
[portrait: DORIAN, happy] Forty auditions! Never cast! Tonight your luck changes. You shall play... TREE NUMBER THREE.
*(Understudy: music note)*
MOVE: a stagehand straps a cardboard tree to Understudy. It stands very proudly.
[name: Director (from the stalls)] Dorian. The tree.
[portrait: DORIAN, sad] ...Ah. The director informs me Tree Number Three has been cut for pacing.
*(Understudy: "..." bubble)*
[portrait: DORIAN, crying] Don't look at me like that! It's a cruel business! I was cut from my own biography!
[portrait: JUNO, angry] You cut a TREE? From a play about a FOREST? *(anger vein)*
[portrait: DORIAN, smug] There are still two trees, darling. It's a very efficient forest.
```
**EV "The costumier"** (same scene, after Tree #3)
```
[name: Costumier] Oh — and you! The blossoms! Is that from wardrobe? I didn't make that. Which play are you in, dear?
[portrait: JUNO, happy] It's not a costume! It's my aunt's.
[name: Costumier] Your aunt's a florist?
[portrait: JUNO, happy] My aunt's a tree. In Verdance. She blooms all year round. These are hers. They've never wilted. Not once in twelve years.
[name: Costumier] ...
[name: Costumier] Well. They're very good. I couldn't do better in silk.
[portrait: JUNO, happy] Nobody can! I've checked! *(music note)*
```
**EV "Prop room"** (backstage, action on the Crown prop)
```
(A prop Crown on a velvet stand: painted tin, eighteen glass stones round the rim, one clear stone at the top. The clear stone is new, and small. The old one lies beside it in a box, much larger.)
[name: Prop-master] The Accord's Pageant Office sends the drawings every Festival year. This year: smaller stone. Different shape. Chipped at the edge, if you can believe it. "As it is," the drawing says.
[name: Prop-master] As what is? I've made that Crown nine times. It's never been chipped.
```

## Map 146 — Harbour & Breakwater: **EV "Salt-caramel"** (sunset, before the Pageant) → **CHOICE `:ch3_juno_talk`**
```
(Sunset. The PC and Juno sit on the end of the breakwater with their feet over the lagoon, sharing a paper cone of salt-caramel. Understudy is asleep in Juno's veil.)
[portrait: JUNO, happy] It's mostly salt. Is that the point? I think that's the point.
[portrait: JUNO, neutral] Your first badge. And it HUMMED. I'm writing that down. I'm writing everything down.
[portrait: JUNO, neutral] ...Can I tell you something boring?
> Go on.
> Is it about larches?
  [portrait: JUNO, deadpan] It's not about larches. ...It's a bit about larches.
> ...
[portrait: JUNO, neutral] Everyone asks about the flowers. "Which play, dear?" "Are you a bride, dear?" I'm fifteen.
[portrait: JUNO, neutral] They're from Aunt Elin. She's the Bride Tree, in Uncle Rowan's garden. When I was three she went to glass, except she didn't, she went to blossom, and she never stopped.
[portrait: JUNO, happy] I'd worn some to her wedding party. She'd only been married a year. So I just... kept wearing them. They don't wilt. They don't even brown at the edges.
[portrait: JUNO, neutral] Uncle Rowan says that's the problem. I don't know what he means. I think it's the best thing in the world.
[portrait: JUNO, sad] ...Mostly I think that.
(She looks at you. *("..." bubble)*)
[portrait: JUNO, neutral] Your turn. That gate at the dock. It didn't give you a color. Mum heard from the fishwife. Everyone's heard.
```
**CHOICE `:ch3_juno_talk`** (the key keeps its old name; this is a Chapter 2 choice)
```
> Tell her what it said: NULL. (told)
  Script: pf_choose(:ch3_juno_talk, :told)
  [portrait: JUNO, shocked] Null. Like... nothing? *(shock lines)*
  [portrait: JUNO, neutral] ...
  [portrait: JUNO, happy] Well. I'm a walking bouquet and you're a blank page. We should start a club.
  [portrait: JUNO, neutral] I won't tell anyone. Not Mum. Not Kestrel. Not even Uncle Rowan. I'm good at secrets. I just don't look it.
  (Juno keeps it. She never tells.)
> It's nothing. A broken gate. (deflect)
  Script: pf_choose(:ch3_juno_talk, :deflect)
  [portrait: JUNO, sad] ...Okay. *(She doesn't believe you, and she lets you have it anyway.)*
  [portrait: JUNO, neutral] If it's ever not nothing, I'm here. I'm very easy to find. I'm the one wearing a tree.
> ... (silent)
  Script: pf_choose(:ch3_juno_talk, :silent)
  [portrait: JUNO, neutral] That's fine. Sitting's fine. Sitting is underrated.
  (She hands you the last caramel.)
(All:)
SE: a bell from the Lantern Theatre. Eight o'clock.
[portrait: JUNO, happy] Opening night! Come ON! If we're late Dorian will make us sit in the Ogre's row!
```

## Map 145 — Lantern Theatre: **EV "The Pageant"** (opening night; S108)
```
(The Lantern Theatre at eight. Every seat is full. Juno and the PC are in the stalls; Dorian, in a gold coat, has the box above them and leans out to wave. In the front row the Accord Inspector has the official text open on his knee.)
[name: Narrator (on stage)] Three hundred years ago, the Original One looked upon Velmora and loved it. And for love, It gave the land a gift...
(Eighteen colored lanterns descend on wires: the Plates falling. Salt glitters in the spotlight.)
[portrait: JUNO, happy] *(whispering)* It IS salt. It's still beautiful. I hate that it's still beautiful.
(Then the companion piece. Three actors in hound masks chase a figure in a sad bark Ogre mask across a painted wood.)
[name: Children in the gallery] BOOOO! BOOOO THE OGRE!
[portrait: JUNO, sad] *(whispering)* I always want him to get away.
[name: Hound Number One] And SO the Loyal Three drove the Gossamer Ogre from the wood, and the Plates were safe for ever!
(Applause. The Ogre exits. Then every stage light turns grey at once. SE: a low hum. The applause stops.)
(In the painted backdrop of the falling Plates, a canvas seam opens, and a figure in a grey cowl steps out of the picture. Ash-bark mask. One white lily.)
[name: Child in the gallery] Is that the Ogre? He's early!
[portrait: MOURNER, neutral] *(the voice is doubled: two voices a breath apart)* Three hundred years of pageantry.
[portrait: MOURNER, neutral] Ask your Warden why nothing in Verdance ever rots.
(Beside you, Juno's hand goes up to her wreath.)
[portrait: MOURNER, angry] Ask your Sovereign why the old capital is underwater.
[portrait: MOURNER, sad] Ask why the Loyal Three wore poison on their collars.
[portrait: MOURNER, neutral] Let the land grieve.
(Grey banners unroll from the flies: a grey ring, broken at the top. The Hollow Ring. In the wings a cowled woman with a weaver's shears cuts the curtain ropes, one, two, three, very neatly. The house curtain drops in front of the cast without touching a soul. Then the screaming starts.)
[name: Accord Inspector] This is not in the TEXT!
[portrait: DORIAN, angry] *(from the box)* House lights! HOUSE LIGHTS! Everybody walk, nobody run, the exits are where they've always been!
MOVE: two Bereaved drop from the flies into the aisle in front of the PC.
[name: Bereaved] Stay in your seat, little one. It's nearly over.
BATTLE: double battle vs [HOLLOW_GRUNT_M "Grunt"] + [HOLLOW_GRUNT_F "Grunt"], version 0 (BALANCE 4b: 0 = the Saltmere Pageant battle, the first Hollow battle in the game). Field: Grand Stage (map default).
(WIN:)
[name: Bereaved] ...You don't fight like the ones with color.
(Through the smoke, on the stage, the Mourner turns and looks straight at you across the whole theater. He goes completely still. WAIT 60.)
[portrait: MOURNER, shocked] ...You.
SE: a burst of Cotton Spore. White fluff everywhere. When it settles the stage is empty, the backdrop is torn, and a lily is lying on the boards.
Switch S108 CH3_PAGEANT_DONE = ON.
[portrait: JUNO, sad] He sounded sad. Isn't that weird? I thought he'd sound evil.
[portrait: JUNO, neutral] *(holding her veil in both hands)* Why would anyone say that about Verdance? Nothing rotting's GOOD. Isn't it?
```

## Map 145 — backstage: **EV "Vesper"** (Eevee Octave, encounter 1 of 3; S190)
```
(Backstage, after the panic. Chorus singers in Prism Choir white sit on prop crates with blankets round them. A young woman in the same white kneels on the boards — not to the PC. To Understudy.)
[portrait: VESPER, neutral] Oh. Hello, little one. You're new.
[portrait: VESPER, happy] I'm Vesper. Vesper Lindqvist. We're the Octave: eight of us, eight Eevee. The Choir lent us to the Pageant for the hymns.
[portrait: VESPER, neutral] *(to Understudy)* It hasn't decided which Imprint it belongs to yet.
[portrait: VESPER, neutral] *(to the PC, after a long look)* Neither have you, I think.
> What does that mean?
  [portrait: VESPER, neutral] Only what it says. I sing; I don't explain. The Hierophant says I'd make a terrible priest.
> ...
  [portrait: VESPER, happy] You don't have to answer. Nobody answers me. It's restful.
[portrait: VESPER, neutral] The eight of us lost our homes in the Glassfall. The Choir raised us beside the Plates, one each. They say an Eevee becomes what it lives beside.
[portrait: VESPER, happy] Would you sing a duet with us before we go? It helps, after a fright. Carol, come here.
> Sing (battle).
  BATTLE: double battle vs [OCTAVE_VESPER "Vesper", 0] + [OCTAVE_SINGER "Carol", 0]. Field: Grand Stage (FIELD_DEFAULTS exceptions).
  (After, win or lose:) [portrait: VESPER, happy] There. Your hands have stopped shaking. So have mine.
> Not tonight.
  [portrait: VESPER, happy] Then at the Festival. We'll all be there. We always are.
[portrait: VESPER, neutral] Look after it. Whatever it becomes, it'll become it because of you.
Switch S190 VESPER_MET_SALTMERE = ON.
```

## Map 145 — Dorian's dressing room: **EV "The Gilded King"** (after S108)
```
(A dressing room crowded with wigs, mirrors and telegrams. Dorian sits in front of the mirror with his gold coat off. Without it he looks every one of his fifty-six years.)
[portrait: DORIAN, sad] Shut the door, darling. Thank you.
[portrait: DORIAN, neutral] Thirty years I've staged that pageant for the Accord. Every word approved. Every comma blessed. And a man walks out of my backdrop and says the one thing I've never let anyone say on that stage.
[portrait: DORIAN, neutral] "Ask why the old capital is underwater."
MOVE: Dorian unlocks a drawer, takes out a yellowed page and holds it a moment too long.
[portrait: DORIAN, neutral] Ansel Crewe wrote this in AF 52. A play called "The Gilded King". They hanged him for it, and burned every copy but one.
[portrait: DORIAN, sad] I've never staged it. I'm a coward with excellent diction.
[portrait: DORIAN, neutral] This is the prologue. Take it. If anyone asks, you found it in a costume. Everything in this building is in a costume.
(Received: GILDED KING PROLOGUE. Key Item. "A yellowed page in an old hand. One line is underlined twice: 'If heaven will not kneel, we'll build a chain.'")
> Why give it to me?
  [portrait: DORIAN, neutral] Because he looked at you. Out of a whole theater, he looked at you. I've been looked at by audiences for forty years, darling. I know when someone's found the person they came for.
> Who was the Gilded King?
  [portrait: DORIAN, deadpan] A king who wanted something very badly. That's all of them. Read it somewhere I'm not.
> ...
  [portrait: DORIAN, neutral] Yes. That's the right response to it. I've been giving it that response for thirty years.
[portrait: DORIAN, neutral] Your next Warden is Tamsin Loom, up the Weavers' Road in Briarwick. She inherited the seat in spring and she hasn't slept since.
[portrait: DORIAN, happy] Be kind. She'll apologize to you for losing. Let her.
```

## Map 140 — outside the Lantern Theatre: **EV "Kestrel"** (after S108)
```
(The crowd is thinning. Against the wall by the stage door, a boy in a too-big black coat is breathing very fast.)
[portrait: KESTREL, shocked] You were in there. You heard him.
[portrait: KESTREL, angry] Did you hear his VOICE? *(anger vein)*
> I heard him.
> Kestrel? What are you doing here?
  [portrait: KESTREL, angry] Following a rumor. Shut up. That's not the point.
> ...
[portrait: KESTREL, neutral] Under the doubling. Under the second voice. The way he said "grieve". Like it had two syllables.
[portrait: KESTREL, shocked] That's — the way she talks — no.
[portrait: KESTREL, angry] *No.*
MOVE: Kestrel runs, shoving through the crowd, north toward the North Gate.
[portrait: JUNO, sad] ...Who talks like that?
V114 KESTREL_STAGE = 1.
```

## Chapter 2 close — Map 140
```
(Next morning. A herald in Elowen green is pasting a notice to the charter stone by the harbour. A small crowd watches without booing, which in Saltmere is a kind of booing.)
NOTICE: "HER MAJESTY QUEEN MAELIS notes with grief the Hollow outrage in HER free port of Saltmere, where the Crown's protection was refused. The Crown's protection remains available. — By Order, Briar Keep."
MOVE: Dorian walks up, reads it, and tears it down in one long rip.
[portrait: DORIAN, angry] "HER" free port. *(anger vein)*
[portrait: DORIAN, neutral] Somebody fetch the paste. We'll put the charter back up where it belongs.
[portrait: DORIAN, smug] And tell the breakwater to warm up. It's booing day on a Thursday this week.
[portrait: JUNO, neutral] Uncle Rowan wants silk-moth eggs from Briarwick. Forty. I was going to send for them.
[portrait: JUNO, neutral] I'm not sending for them. I'm not letting you walk into the Gossamer by yourself after last night.
[portrait: JUNO, happy] Also I've never seen a gym puzzle from the INSIDE.
(Juno becomes a follower.)
[name: Gate Warden (North Gate)] North Gate's open. Nobody leaves Saltmere on opening night, it's bad luck and worse for business. This morning everybody wants to.
GALE POST (Pokémon Center desk): "Heard about the Pageant. Are you hurt? Don't answer that, you'll lie. Lecture Two has grown a section. — I.L."
QUEST LOG: "Eighteen Roads" — Earn the second badge in Briarwick, up the Weavers' Road.
V102 STORY_CHAPTER = 3. (The North Gate opens onto the Grey Saltings.)
```

---

## Appendix: events added or changed versus the built specs
- **[NEW]** Dovetail: rail sign, cabin trunk, cook. Ferrow's Landing: Edda's last call (`GO_HOMEWARD`), two sidequests, lighthouse mirror, the north-gate road sign. Ferrymen's Mile: the Hale Bell, the quarantine roadblock moved here from Windfall Row (the Strand Road leaves westward at the bell). Windfall Row: the forest-road cordon. Lacecliff Walk (527) and Marram Down (528): every event (new maps). Saltmere: Dorian at the breakwater, the Woman from the ferry, Sella, Quill, two sidequests, the Kestrel-at-the-poster glimpse, the prop room, the costumier, the Inspector, the Gale Post desk, the North Gate warden.
- **Changed for Revision 14:** Chapter 2 is Saltmere now (it was Briarwick). The Chapter 1 opener's counting rhyme starts "One for the stage and two for the weave". Juno's look follows Ever-Bloom. Rowan mentions the Saltmere road and the Pageant. The gym-1 dialogue (Tamsin's) moved to `story/21_SCRIPT_CH3.md` and was rewritten for Gym 2. The Windfall Row survey flags, surveyor and Juno's flag line moved to Chapter 3's road (the Dyers' Ford).
- **Moved out:** everything from "Chapter 2 — The Weaver's Debt" is in `story/21_SCRIPT_CH3.md`.
- **Open items for other teams:** see `design/SWAP_GYM1_GYM2.md`. Portraits used here (parked by Revision 15; keep the tags): Edda, Voss, Calla, Larch, Juno, Kestrel, Rowan, Wenna, Coll, Hesper, Dorian, Mourner, Vesper.
