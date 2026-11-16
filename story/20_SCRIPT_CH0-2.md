# Script: Prologue, Chapter 1, Chapter 2 (through Gym 1 and its aftermath)

> **Final playable script** for the game's first hour (SPINE Revision 8). It covers maps 109–110, 100–108, 520, 523, 522, 521, 524, 120–125, 130–131, 525, 548, 526. Structure follows the built events in `mapgen/specs`; where this file adds an event, it is marked **[NEW]**.
> Sources: 04_ACT_I (outline), 15_COMEDY (scenes Ch0–Ch2, inlined), NARRATIVE_KEYS (choice keys), FLAGS (switches), SYSTEMS (script calls), CAMEOS §1 (Shelly).

## Conventions
- `[portrait: NAME, expression]` precedes each portrait line. No tag = plain message box (narration, signs, generic NPCs use `[name: X]` with no portrait).
- *(italics)* = emote bubble or staging. `MOVE:` = movement route. `SE:` / `BGM:` = audio. `WAIT n` = frames.
- `> option` = a choice. `→` = what follows. `PC` = the player; `\PN` = player name.
- **Script calls:** `pf_choose(:key, :value)`, `pf_bond_add(:ID, n)`, `pf_standing_add(:FACTION, n)`, `pf_resonance_add(n)`, `Prismfall.rival_battle(...)`, `Prismfall.gym_battle(n)`, `Prismfall.game_over(:GO_X)`, `Prismfall.record_starter(...)`. Choice effects in NARRATIVE_KEYS §4.2 apply automatically on `pf_choose`; extra deltas are written out.
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
[name: Rope-skipping Girl 1] One for the weaver, two for the stage,
[name: Rope-skipping Girl 2] three for the river that won't turn its page!
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
(A cluttered station: tide charts, brass instruments, a stove with a blackened kettle. Juno is at a bench, labeling seed packets, back turned.)
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
[portrait: LARCH, deadpan] This is \PN. \PN, this is Juno Hale, my assistant. She'll tell you about larches now. I can't stop her. Nobody can.
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
[portrait: ROWAN, neutral] This is a Phantump. I found it up past Briarwick, in a wood that's gone to glass. It was sitting in a glass tree, crying.
[portrait: ROWAN, sad] Its tree couldn't die properly, you see. So it couldn't either.
[portrait: JUNO, sad] That's so sad...
[portrait: ROWAN, neutral] It's not sad that things die, Juno. Everything that grows must be allowed to. That's what makes room.
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
QUEST LOG: "Biscuit" — Go with Juno to the old orchard on Route 1.
(Juno becomes a follower.)
```

## Map 520 — Route 1 (farm lane; BGM: route theme, light)
```
ROUTE SIGN: ROUTE 1 — Ferrow's Landing ↔ Hale's Bramble ↔ Route 2. Mind the hedges. The hedges mind you.
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

# CHAPTER 2 — "The Weaver's Debt"

**Chapter start:** the morning after. Larch sees the PC off at the Route 1 stile.
```
[portrait: LARCH, neutral] Eighteen gyms. Briarwick's first, up through the Gossamer Wood. The Warden's a girl called Tamsin Loom. Go easy on her, she inherited the seat in spring and hasn't slept since.
[portrait: LARCH, neutral] Write to me. I mean it. Gale Post, every town. If I don't hear from you in a week I start Lecture Two by post.
[portrait: JUNO, happy] I'm coming as far as Briarwick! Uncle Rowan wants silk-moth eggs, and I want to see a gym!
(Received: TOWN MAP. "Larch has drawn a skull on the Glassed Orchard, and a smaller skull on her own kettle.")
QUEST LOG: "Eighteen Roads" — Earn the first badge in Briarwick.
```

## Map 521 — Route 2 (farmland into forest; BGM: route theme, fuller)
```
ROUTE SIGN: ROUTE 2 — Briarwick ahead. Travelers are reminded that the Gossamer Wood is the Crown's forest and the Warden's care. Litterers will be woven into something.
```
**EV "Accord guard"** (roadblock, lifts once S105 is on)
```
[name: Accord Guard] Hold. Quarantine order: nobody leaves the Landing without papers.
[name: Accord Guard] ...You've got a Badge Case. A challenger. Right. Challengers pass, that's older law than the quarantine.
[name: Accord Guard] "Eighteen in Concord, One in Keeping." On you go.
```
**EV "Accord guard (aside)"**
```
[name: Second Guard] *(low)* That's the null one from the dock. Captain said let them through, whatever happens.
[name: Accord Guard] Which captain?
[name: Second Guard] Didn't say. Came down from Crownhaven with a white seal on it.
(They notice the PC listening. *(sweat drop)* ×2.)
[name: Accord Guard] Lovely weather.
```
Route trainers and flavor:
```
[name: Bug Catcher Wim] I'm going to be Warden of Briarwick! (Battle. After:) ...Assistant Warden.
[name: Picnicker Ada] My Budew sneezes pollen when it's nervous. It's nervous now. (Battle. After:) Bless you. Bless both of us.
[name: Meridian Surveyor] Mind the orange flags. Survey line for the new Lattice. Straight through to the wood. Trees aren't in the plan, but trees rarely are.
[name: Hay-cart Driver] Used to take me a day to Briarwick and back. Now the east road's all glass and I go round. Day and a half. Glass doesn't pay my horse.
[portrait: JUNO, neutral] (follower chatter, at the first orange flag) These weren't here in winter. They go right toward the Glasswood. That's... probably fine?
HIDDEN ITEM (base of the third flag): ANTIDOTE. "A surveyor dropped it. He'll want it in about ten minutes."
BERRY TREE: Juno: "Pecha! Pick it gently. It bruises if you look at it wrong. Like Kestrel."
```

## Map 524 — Gossamer Wood (`:SILKWOOD`; BGM: harp and wood-flute)
```
(Huge old trees hung with silver silk. Looms' clacking can be heard far off.)
FIELD NOTES pop-up: "SILKWOOD — Bug moves bite deeper. Webs slow the careless. Fire here is rude and effective."
[portrait: JUNO, happy] Silk-moths! The Insect Plate's somewhere under Briarwick, and it makes the silk never tangle. Ever! You could knot it for a week!
[name: Silk-picker] Don't cut the low strands, they're this year's. Cut the high ones. No, higher. No— you know what, I'll do it.
[name: Bug Catcher Twins Mo & Jo] We battle together! (Double battle.) [after] We lose together.
[name: Old Weaver resting] Sixty years I've walked this wood. This spring it rings. Hear it? East. Like someone tapping a glass.
SHRINE STONE (small, mossy): A carving of three beasts chasing a masked figure. Someone has left a honey bun in front of the masked one, not the three.
HIDDEN ITEM (in a web): NET BALL ×2. "The web gave them up without a fight."
BLEED VEIL (east edge, a shimmer between two trees; beyond it the trunks are clear crystal): 
  [portrait: JUNO, sad] That's the Glasswood. It was three fields away at midwinter.
  (Entering leads to Cocoonfall Hollow via the Deepwood; blocked by a Cut tree until Badge 1.)
```

## Map 120 — Briarwick (BGM: looms as percussion, fiddle)

### Arrival (autorun, first entry)
```
(A village lashed between tree trunks: rope bridges, treetop houses, bolts of silk drying like flags. At the east edge, orange survey flags march to a half-built brass pylon.)
[portrait: JUNO, happy] Briarwick! Smell that? That's mulberry and lanolin and— oh, the egg-seller's open. I'll find you at the gym! Don't start without me! Or do! I'll catch up!
MOVE: Juno runs off north. (She stops following.)
```

### Named residents
**Tamsin Loom** (first meeting, in the square, carrying too many bolts of silk)
```
MOVE: Tamsin walks into the PC. Silk everywhere. *(shock lines)*
[portrait: TAMSIN, panic] Sorry! Sorry — I wasn't — are you hurt? You're not hurt. Sorry.
[portrait: TAMSIN, neutral] You've a Badge Case. Oh. Oh no. You're a challenger. TODAY?
[portrait: TAMSIN, panic] It's fine! It's fine. The gym's open. It's just a bit— the moths are— there was a meeting.
[portrait: TAMSIN, neutral] I'm Tamsin. Loom. The Warden. Since spring. Come to the Loomhouse when you're ready. Take your time. Please take your time.
MOVE: Tamsin gathers the silk and hurries east, toward the pylon, not the gym.
```
**Guildmistress Hett** (Weavers' Guildhall, map 123)
```
[name: Hett] Old Mother Loom ran this guild forty years and never once missed a moth-count. The girl's missed three.
[name: Hett] I'm not saying she's hiding something. I'm saying the ledger's locked and it never used to be.
```
*[after gym]* `[name: Hett] She signed WHAT? Alone? ...Poor fool child. Her gran would've made the whole village sign it with her, and then it'd be all our fault. That's what a guild's FOR.`

**The Moth-keeper, Alder Finch** (grove fence)
```
[name: Finch] Fourteen dead this week. They fly east at dusk and come back with glass on their wings. Then they don't come back.
[name: Finch] Meridian says the Lattice will "stabilize" it. The line they've drawn for it goes straight through my grove.
```

### Flavor townsfolk
```
[name: Weaver at loom] Clack-clack. Sixty picks a minute. Don't talk to me on the downstroke.
[name: Weaver at loom] (again) That was the downstroke.

[name: Dyer] Elowen green, that's my vat. The Queen's own shade. She's never paid for a yard of it. "The Crown's by right of soil," says the taxman. So's the mud, I said.

[name: Apprentice] I wove my first scarf! It's got eleven mistakes. Tamsin found a twelfth and then apologized for an hour.

[name: Rope-bridge Boy] If you jump on the bridge it goes BWOING. I'm not allowed. You're a grown-up. YOU do it.
  > Jump.  → SE: bwoing. [name: Boy] HA!  [name: Voice below] WHO'S JUMPING?!
  > Don't.  → [name: Boy] Coward.

[name: Grandmother knitting] It's a jumper for my Caterpie. Sixteen sleeves. I'm on the fourth. Don't rush me.

[name: Silk Merchant] Briarwick silk never tangles and never rots. That's why nobody ever buys a second one. Terrible business. Wonderful product.

[name: Meridian Linesman] Pylon'll be humming by month's end. Free light for the looms! Folk here look at me like I'm selling plague.
[name: Meridian Linesman] (again) Truth is, I don't know what it does to the wood. I just bolt the brass.

[name: Tired Mother] Three nights running somebody's cut the survey flags. I'm not saying who. I'm saying I slept very well through it.

[name: Old Man on bridge] The Loyal Three drove the Ogre out of this wood. My grandfather told me. His grandfather told him. Nobody's grandfather SAW it, mind.

[name: Girl in ogre mask] RAAH! I'm the Gossamer Ogre! I steal children and eat looms!
[name: Boy in dog mask] And I'm a Loyal Hound and I bite you! ...Why does the Ogre mask look sad?

[name: Egg-seller] Silk-moth eggs, a copper each. That loud girl bought forty. FORTY. For her uncle, she says.

[name: Tax-barge Deserter] I rowed the Queen's tax-barge. Jumped off at Saltmere when they booed us. Weaving's quieter. Nobody boos a scarf.

[name: Accord Chaplain] The chapel's open. The mural's older than the looms. Mind the Crown in it — people say it's painted wrong. It isn't. It's painted *before*.

[name: Youngster] The Warden cries in the gym at night. I heard her through the wall. Then she apologized to the wall.

[name: Woman with basket] East wood rings like a bell now. My mother says a ringing wood means a wedding. I don't think this is a wedding.

[name: Cutter's Wife] You'll want my husband if there's a tree in your way. He'll say no first. He always says no first. Wait for the second answer.
```
*[after gym, village-wide variants]*
```
[name: Weaver at loom] She told us. All of it, or you did. Either way the looms stopped for a whole minute. First time since the funeral.
[name: Dyer] Contract's a contract, says the linesman. So's a pitchfork, says I.
[name: Tired Mother] Still sleeping well.
```
*[after S107 Matriarch]* `[name: Finch] The ringing's stopped. The moths flew east at dusk and came back clean. Whatever you did in there: thank you. And don't tell me. I don't want to know.`

### Signs and objects
```
TOWN SIGN: BRIARWICK — Where the Thread Never Tangles. (Carved under it, smaller: "Unlike the Guild Accounts.")
LOOMHOUSE SIGN: LOOMHOUSE GYM. WARDEN: Old Mother Loom (painted over) TAMSIN LOOM. "A thread holds because it's twisted with others."
FESTIVAL POSTER (square): The same poster as the Landing. Here the dark fleck in the Crown's stone has been circled in charcoal. Someone has written: "SEE CHAPEL."
PYLON (east edge): Half a brass pylon. A plate reads: MERIDIAN CONCORD — LATTICE 15 (BRIARWICK) — "Light for Everyone." It is faintly warm, and the grass around it is stiff, like spun sugar.
SURVEY FLAGS: Orange cloth on stakes. Four of the stakes have been neatly cut. The cuts are very clean. A weaver's shears.
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
  [name: Old Woman] Oh, I couldn't say. I could *sing* it, but I couldn't say.
> That's not how the story goes.
  [name: Old Woman] Isn't it? I've only ever told it true. That's the trouble with me.
> ...
  [name: Old Woman] Quiet. Good. You'll hear more that way. Most of it's under the floor.
[name: Old Woman] You've no color on you, child. Did you know? Like water in a glass.
[name: Old Woman] Walk carefully. Eighteen roads is a long way, and people will want to carry you.
(She goes back to sweeping. After the gym she is gone; a single dusk-colored flower lies on the shrine. S170 OFF.)
ITEM: DUSK PETAL. "It's only open at twilight. It's open now. It's noon."
```

### Sidequest A — "Sixteen Sleeves"
```
(Grandmother knitting, second talk:)
[name: Grandmother] I've run out of green. The dyer won't sell me less than a bolt. Fetch me three Tiny Mushrooms from the wood and I'll boil my own.
QUEST LOG: "Sixteen Sleeves" — Bring three Tiny Mushrooms (0/3).
(On delivery:)
[name: Grandmother] Lovely. Smells dreadful. Here, I made this one first. It was meant for a Weedle. He evolved. Ungrateful.
(Received: SILK SCARF. "Two sleeves. A Kakuna has no use for it.")
(Post-game epilogue hook: a Caterpie in a sixteen-sleeved jumper walks through the square.)
```

### Sidequest B — "The Locked Ledger" (leads into the main reveal; optional early clue)
```
(Guildmistress Hett, second talk:)
[name: Hett] You're a stranger, so you can do what I can't. The guild ledger's in the Warden's loft and it's locked. Old Mother Loom kept the key in the gym. "Where the first thread starts," she used to say.
QUEST LOG: "The Locked Ledger" — Find the ledger key in the Loomhouse.
(Gym foyer, the first loom on the left, action:) A small brass key is tied into the very first warp thread. (Received: LEDGER KEY.)
(Weavers' Guildhall loft:) LEDGER, last page: "Received of the Meridian Concord, for stewardship rights, Lattice 15: ₽400,000. Signed, T. Loom, Warden." One signature. The line for "Guild witnesses" is blank.
(Return to Hett before the gym:) [name: Hett] ...Alone. She signed it alone. Don't say anything yet. Let me think how to say it kindly. I'm out of practice.
(Reward after the chapter: ₽2000 and TM STRING SHOT, "from the guild's teaching chest".)
(If the player found the ledger first, Tamsin's confession scene opens with: [portrait: TAMSIN, sad] "You've read it. Hett has too. I can tell by how gently she's speaking to me.")
```

## Maps 121–125 — Briarwick interiors
```
POKÉMON CENTER:
[name: Nurse] We heal for free. The scanner at the door is new. It told me I'm "Insect, Briarwick". I've lived here forty years, I'd worked it out.
[name: Trainer] The gym's all planks and looms. Pull the wrong lever and the floor leaves. I've met the basement twice.
GALE POST DESK [NEW]: A letter is waiting. "Lecture Two is drafted. Do not make me send it. Eat something. — I.L." (Received: POTION ×2, and a tea bag. ITEM: KELP TEA BAG. "You could throw it away. You don't.")

MART:
[name: Clerk] Antidotes go fast here. The moths don't mean it.
[name: Customer] I asked for a Synthetic Seed and the old ladies in the queue went silent. I put it back.

TREETOP HOUSE (map 124):
[name: Retired Weaver] I wove Old Mother Loom's shroud. She'd picked the pattern at thirty. "Plan ahead," she said. Tamsin plans ahead too. She plans for everything to go wrong.
BOOKSHELF: "A Child's Pageant of the Loyal Three." The last page, where the Ogre is driven out, has been torn away. Someone has drawn the Ogre a little house instead.

CHAPEL [exterior door on map 120; interior tile set in 124's second room]:
MURAL: Eighteen colored stones falling from a white sky into green land. Above them, a silver crown with one clear stone. The stone is whole.
[name: Child in pew] Mum says the Crown got hurt once. She says don't ask the chaplain. So I'm asking you.
WINDOW: Eighteen panes of colored glass around one clear pane. The clear one has no lead around it, as if it were added first.

CUTTER'S HOUSE (map 125):
[name: Cutter] No.
[name: Cutter] (again) ...What's the tree?
[name: Cutter] (before Badge 1) Come back with the Warden's badge. I don't hand Cut to people the wood hasn't met.
[name: Cutter] (after Badge 1) Right. Here. Cut the dead ones. If you cut a live one I'll know. I won't know how. I'll just know.
(Received: HM01 CUT.)
```

## Map 120 — **EV "Pallbearer Thistle"** (night event at the pylon; triggers when the PC approaches the pylon after meeting Tamsin)
```
(Night. Two grey-cowled figures in carved bark masks are cutting survey stakes with shears. A third stands at the pylon with a hand flat on the brass.)
[name: Bereaved] That's the last of the south line.
[portrait: THISTLE, neutral] Leave soil where they stood. Bare. Let something rot there for once.
MOVE: The PC steps on a twig. SE: snap. *(shock lines)* ×3.
[portrait: THISTLE, angry] A watcher. Meridian's, or the Warden's?
> Neither.
  [portrait: THISTLE, neutral] Everyone's somebody's. You just haven't been told whose yet.
> Who are you?
  [portrait: THISTLE, neutral] The Hollow. We mourn what this land was. Somebody has to.
> ...
  [portrait: THISTLE, neutral] No answer. Then I'll assume the worst. It saves time.
[portrait: THISTLE, sad] I was a weaver once. Lowmarsh. You won't find it on a map now. It had looms too.
[portrait: THISTLE, angry] Ask your Warden what she signed!
BATTLE: HOLLOW_THISTLE "Thistle", version 1. (Hollow admin 1; can't be fled.)
(WIN:)
  [portrait: THISTLE, shocked] ...Your partner doesn't fight like the Wood's got hold of it. It fights like it's standing nowhere at all.
  [portrait: THISTLE, neutral] Let the land grieve, child. And look at the grass by that pylon in daylight.
  MOVE: The three vanish into the trees. A bark mask is left on the ground.
  ITEM: BARK MASK. "Carved to look like the Gossamer Ogre. It does look sad."
Switch S106 CH2_THISTLE_DONE = ON.
```

## Map 130 — Loomhouse Gym, Foyer
```
[name: Gym Guide] Challenger! This is the Loomhouse. Bug-types, and the Silkwood field. Fire and Flying do well. Grass does not. I say this to everyone and half of them bring a Bulbasaur.
[name: Gym Guide] The puzzle: three looms, three colors of plank. Pull a shuttle and one color extends while another retracts. Old Mother Loom built it to teach patience. Tamsin added the safety nets. And the apology cards.
APOLOGY CARD (pinned by the trapdoor): "If you have fallen, I'm so sorry. Stairs are to your left. — T.L."
PORTRAIT (wall): A fierce old woman at a loom. Brass plate: "Mother Loom, Warden AF 247–299. 'Twist it or lose it.'"
```
**Comedy scene Ch2, "The Apology Spiral"** (Tamsin is in the foyer the first time, re-threading a loom)
```
[portrait: TAMSIN, panic] Sorry — the gym's a bit tangled today — sorry —
> It's fine.
  [portrait: TAMSIN, panic] Sorry for saying sorry so much. That's annoying. Sorry. *(sweat drop)*
> Stop apologizing.
  [portrait: TAMSIN, shocked] Right! Yes! Sorr— *(shock lines)*
  [portrait: TAMSIN, panic] I nearly did it again. I'm so sorry.
[portrait: TAMSIN, sad] ...
[portrait: TAMSIN, deadpan] I'm going to go and stand in the web now.
MOVE: Tamsin exits to the Weaving Hall.
```

## Map 131 — Loomhouse Gym, Weaving Hall (puzzle per GYM_PUZZLES.md; switches 301+ are World's)
```
[name: Bug Catcher Nell] A thread alone is just string! (Battle.) [after] Two of us would've had you.
[name: Lass Orla] I pulled the red shuttle. Don't pull the red shuttle first. (Battle.) [after] ...Did you pull the red shuttle?
[name: Weaver Trainer Bram] Granny Loom taught me this hall. Tamsin taught me to say sorry when I win. (Battle.) [after] I don't need to say it, then.
FALL (wrong plank): You drop into a net. A card is pinned to it: "Sorry! — T.L."
(Juno arrives at the hall's entrance once two trainers are beaten, eating a honey-silk bun.)
[portrait: JUNO, happy] I made it! Go on! I'll be loud!
```
**Warden battle**
```
(Tamsin stands at the great loom at the hall's end. She has stopped fidgeting.)
[portrait: TAMSIN, neutral] My grandmother wove this room. Every plank, every web. She held this village together for fifty years with thread and shouting.
[portrait: TAMSIN, sad] I've had it since spring. I can't shout.
[portrait: TAMSIN, angry] But I can weave. Granny Loom wove this room. Don't you dare tear it.
Script: Prismfall.gym_battle(1)     # LEADER_TAMSIN, :SILKWOOD, cap 15
(Mid-battle, when her ace enters:) [portrait: TAMSIN, neutral] Twist with me. Hold.
(LOSE: standard whiteout to the Pokémon Center. Tamsin on retry: "Again? Good. I mean— sorry. I mean good.")
(WIN:)
[portrait: TAMSIN, shocked] ...It held, and you still came through it.
[portrait: TAMSIN, happy] That's allowed. Granny said the room's meant to lose to the right person. I didn't think I'd ever meet one.
(Received: the WEFT BADGE.)
(The PC opens the Badge Case and sets the badge in. SE: a faint hum, one clear note. *(question mark)* over Juno.)
[portrait: JUNO, happy] Ooh. Is it supposed to do that?
[portrait: TAMSIN, neutral] I don't think they do that. ...Do they do that?
(Received: the gym TM. Species per BALANCE.md; it must not be Struggle Bug, which is Shelly's sidequest reward.)
[portrait: TAMSIN, neutral] That's the Accord's word that you may use Cut, and that Pokémon up to level nineteen will heed you.
[portrait: TAMSIN, sad] \PN... could you come up to the loft? There's something I should say to someone, and you've an honest sort of silence.
```

## Map 123 loft — **EV "Tamsin's confession"** → **CHOICE `:ch2_tamsin`**
```
(The loft: a ledger open on a table, a contract with a gold sunburst seal. Tamsin won't sit.)
[portrait: TAMSIN, sad] That masked woman at the pylon. She was right. I signed it.
[portrait: TAMSIN, sad] Briarwick's bankrupt. It has been for three years. Gran hid it. I found the accounts the week I buried her.
[portrait: TAMSIN, sad] Meridian offered four hundred thousand for "stewardship rights". One pylon. Free light. I signed it by myself, at night, so nobody would have to know how bad it was.
[portrait: TAMSIN, crying] And now the Glasswood's walking up the survey line like it was invited. Fourteen moths this week. I count them. I count them every morning.
[portrait: TAMSIN, sad] The guild meets tonight. Tell me what to do. Please. I've run out of thread.
> Tell them the truth. I'll stand next to you. (help_confess)
  Script: pf_choose(:ch2_tamsin, :help_confess)
  [portrait: TAMSIN, shocked] Next to me. Not in front?
  [portrait: TAMSIN, neutral] ...A thread holds because it's twisted with others. I've had that on the SIGN.
  → Scene: the guild meeting. Tamsin speaks; her voice cracks twice; Hett stands up first: "Then we sign it WITH you, girl, and then we tear it up together." The contract is renegotiated: a smaller pylon, off the grove.
> They deserve to know. If you won't say it, I will. (expose)
  Script: pf_choose(:ch2_tamsin, :expose)
  [portrait: TAMSIN, panic] No— wait— not like—
  → Scene: the guild meeting. The PC lays the contract on the table. Uproar. The looms stop. Tamsin stands very still, then tears the contract in half herself, in front of them: "I'm sorry. I'm so sorry. That's the last time I'll say it tonight."
  Flag: TAMSIN_PUBLIC_CONFESSION.
> It's your secret. I won't tell. (keep_secret)
  Script: pf_choose(:ch2_tamsin, :keep_secret)
  [portrait: TAMSIN, sad] ...Thank you. I think. I'll fix it quietly. I'll find the money somewhere.
  → No meeting. The pylon is finished within the week (map state). Hett's lines stay suspicious. (In Act V, Tamsin can't afford to let go of her Plate.)
(All branches:)
[portrait: TAMSIN, neutral] Whatever's making the wood ring, it's in Cocoonfall Hollow, at the Glasswood's heart. I can't cross the Veil. Nobody can.
[portrait: JUNO, neutral] *(from the stairs)* ...They can.
[portrait: TAMSIN, shocked] *(shock lines)* What?
[portrait: TAMSIN, neutral] Then take this. It was Gran's shuttle. It's only wood. But she never dropped a thread while she held it.
(Received: MOTHER LOOM'S SHUTTLE. Key Item. "Worn smooth by fifty years of one hand.")
QUEST LOG: "The Ringing Wood" — Cut through the Deepwood to Cocoonfall Hollow.
```

## Map 525 — Gossamer Deepwood (`:SILKWOOD`; Cut required)
```
[name: Woodward (at map 526, his hut)] Past my hut it's all glass. I've stopped chopping. You can't burn it and it cuts the axe.
WOODWARD'S HUT bookshelf: "Tally of the east trees. Midwinter: 0 glass. Thaw: 40. Spring: 300. I have stopped counting. — W."
(Received from the Woodward: 3 POTIONS. "For whatever you think you're doing.")
[name: Bug Maniac Ferris] The bugs in here have gone STRANGE and I love them! (Battle.) [after] That one hummed. Did you hear it hum?
HIDDEN ITEM (hollow stump): SUPER POTION. "The stump kept it dry."
```
**Optional thread: cameo sidequest "Lost in the Gossamer" (Shelly)** — CAMEOS.md §1; S181 on completion
```
(A dew-pond clearing. A pink-haired girl is crouched in front of a Caterpie, bowing to it.)
[portrait: SHELLY, panic] I'm so sorry, was this your leaf? I didn't know it was your leaf.
[portrait: SHELLY, shocked] Oh! A person! Um. Hello. Is this— this isn't the Rhodochrine Jungle, is it. *(sweat drop)*
[portrait: SHELLY, sad] I looked into a pond at home and then I was looking OUT of this one. That was three days ago. The paths keep re-weaving.
> I'll help you get back.
  [portrait: SHELLY, happy] Really? You don't have to. I mean please do. I mean thank you.
(She follows. The dew-pond she arrived through is behind a small Bleed Veil; a glassed Masquerain guards it. The PC enters alone, battles it (Lv 14, `:BLEED`), and it calms.)
[portrait: SHELLY, neutral] You just... walked in. Where I'm from, nobody walks into the sick places and comes out the same.
[portrait: SHELLY, happy] Before I go, could we have one practice battle? Doubles? I'm supposed to be good at this and I don't want to be rusty when I get home.
BATTLE: FESTIVAL_SHELLY "Shelly", version 1 (double, Lv ~17, `:SILKWOOD`).
(After, win or lose:)
[portrait: SHELLY, happy] Your forest sounds like home used to, before the city got sick. Look after it?
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
BOSS BATTLE: Glass Matriarch (GALVANTULA, Lv 16, 2 bars; field `:BLEED`; at the bar break it "re-strings the nest": the field borrows `:SILKWOOD` for 3 turns).
(WIN:)
The Matriarch collapses onto the nest. The ringing drops by half. It thrashes, shedding slivers of crystal.
```
**CHOICE `:ch2_matriarch`**
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
Switch S107 CH2_MATRIARCH_DONE = ON. V105 BRIARWICK_GLASSWOOD = 1.
ITEM (under the nest): a sliver of green light sinks back into the roots as you watch. FIELD NOTES: "Something under the Hollow is holding the wood together. I think I was standing on it. — note to self: ask Tamsin where the Plate is."
```
**EV "Outside the Veil"**
```
(soothe:) [portrait: TAMSIN, crying] Half the grove. ...Half. And the moths that are left are *singing*. I'll take half. I'll take it.
          [portrait: JUNO, happy] You stayed all night! We could see you through the shimmer, just sitting there! Kestrel would've hated it!
(silence:) [portrait: TAMSIN, shocked] It just... stopped. All of it.
          MOVE: the Matriarch walks out through the Veil, past them, into the wood. It doesn't react to anything.
          [portrait: TAMSIN, neutral] Oh. Oh, that's — thank you. I think.
          [portrait: JUNO, sad] ...It didn't look at me. They always look at me.
(Both:)
[portrait: TAMSIN, neutral] The next Warden's Dorian Pell, in Saltmere. He'll call you "darling" and mean it about a third of the time.
[portrait: TAMSIN, happy] Come back, will you? I'd like to show you the room when it isn't tangled.
[portrait: JUNO, happy] I've got to take the eggs to Uncle Rowan. Then Saltmere! There's a PAGEANT! Don't see it without me!
MOVE: Juno leaves south. 
```

## Chapter 2 close — Map 120
```
(On the way out of Briarwick, a child is standing at the Festival poster with a stick of charcoal.)
[name: Child] I circled it. The Crown in the chapel's got a whole stone. This one's got a bit gone. See?
[name: Child] Mum says the Crown got hurt once.
[name: Child] How do you hurt a crown?
(No answer option. The PC's hand moves, unprompted, to their chest. WAIT 40.)
GALE POST (Pokémon Center desk): "Heard about the Hollow. Lecture Two enclosed. It is nine pages. Page nine says I'm proud of you. Do not skip to page nine. — I.L."
V102 STORY_CHAPTER = 3.
```

---

## Appendix: events added or changed versus the built specs
- **[NEW]** Dovetail: rail sign, cabin trunk, cook. Ferrow's Landing: Edda's last call (`GO_HOMEWARD`), two sidequests, lighthouse mirror. Briarwick: Gale Post desk, chapel interior, two sidequests, the charcoal child. Deepwood: Shelly's clearing.
- **Changed:** the Bleed Veil event now carries the `GO_ORCHARD` prompt; the Glass Matriarch is followed by `:ch2_matriarch`; Tamsin's confession uses `:ch2_tamsin` with three guild-meeting variants.
- **Open items for other teams:** the gym TM (BALANCE.md decides); portraits needed here: Edda, Voss, Calla, Larch, Juno, Kestrel, Rowan, Wenna, Coll, Hesper, Tamsin, Thistle, Shelly.
