# Story Bible 04: Act I — The Last Ferry (Prologue + Ch1–5, Gyms 1–4)

> **Tone:** Rejuvenation-warm. Cozy, funny and curious, with the Bleed eerie but *beautiful*. The first real wound comes at the very end (the Lowlight Shatter).
> **Conventions:**
> - **CHOICE** = a named decision. Keys and effects are owned by `story/10_CHOICES_ENDINGS.md`. Suggested keys are in `code`, and Bonds/Standing deltas are indicative.
> - **GO** = a proposed story game over (title / trigger / foreshadowing / epitaph) for the Ledger catalog.
> - Map and road names follow `design/WORLD.md` and the cartographer's `tools/worldmap/world_data.py`.
> **Revision 6:** this act carries beats of the Ashkaar–Isenmar War and the Blessing. See `14_WAR_AND_BLESSING.md` (timeline table) for the inserts per chapter; that file wins on conflicts.

> **Revision 7 (comedy):** each chapter here has a scripted funny scene in `15_COMEDY.md` §4 (Ch0–5), plus running gags (§3) and optional kingdom bits (§5). Place each scene where its heading says, and never inside the beats §1 lists as joke-free.

> **Revision 14 (gym order):** Gym 1 is Dorian's Normal gym in Saltmere and Gym 2 is Tamsin's Bug gym in Briarwick. The road runs Ferrow's Landing → west along the coast (the Strand Road) → Saltmere → inland up the Weavers' Road → the Gossamer Wood and Briarwick → north over the Hoar Road through the Rimewood and Frostwick → Ebbmouth. The direct forest road north from the Landing is corded off because the Glasswood has crossed it. Choice keys and switch names keep their old chapter prefixes (`:ch2_tamsin` is a Chapter 3 choice, `:ch3_juno_talk` a Chapter 2 one): IDs never renumber. The work other teams must do is listed in `design/SWAP_GYM1_GYM2.md`.

**How Act I escalates.** Each chapter turns the same question one notch tighter: *what is the land paying for its miracles, and who is billing it?*
- Ch1 shows the price as wonder: a glass orchard, and a child who can walk into it.
- Ch2 has the Hollow ask the question out loud, on a stage, to a whole city: "Ask your Warden."
- Ch3 answers it in miniature, quietly, in one village: a Warden signed, the light is real and so is the glass.
- Ch4 shows that the answer has a family: a brother in the Hollow, a sister with the badge.
- Ch5 sends the bill: twelve people Fixed in glass.

---

## PROLOGUE — "The Last Ferry" (the Hallow Strait → Ferrow's Landing)

**Open on black.** A ship's horn. Text: *Spring, AF 300. The Concert of Regions has sealed the borders of Velmora. This is the final civilian crossing.*

**Scene 1: the deck of the *Dovetail* at dusk.**
- The PC stands at the rail with one bag and their mother's letter. The player can read the letter (Key Item).
- **Captain Edda Morrow** stomps past: "Don't lean on my rail like that, sprog — you'll — huh." She stares a beat too long. "...Never mind. Mind the gap when we dock."
- On the horizon, **eighteen colored glows** sit low over the sea. A deckhand: "When I was a lad you could only see the Imprints on a clear night. Now you see 'em through fog."
- **Aurelian Voss** joins the PC at the rail in a plain coat, holding a chipped Meridian mug. He's warm and self-deprecating, a man coming home from a summit where he begged the Concert to keep Velmora's trade open. "First crossing? Everyone gets quiet when they see the lights."
- He gives the PC a **Meridian badge case**: "We make them for the League anyway. Call it a welcome from a fellow traveler." This is the telemetry device, so the player must receive it. He also offers a **Meridian Fellowship card** (₽ stipend, Mart discount).
- **CHOICE `:pro_fellowship`:** accept the Fellowship (+Meridian Standing, more money in Act I) / politely decline (+Voss Bond, because he respects it: "Independent. Good.") / say nothing (he leaves the card on the rail anyway).

**Scene 2: Ferrow's Landing dock.**
- A brand-new Meridian **customs gate** stands beside the old bronze Accord plaque ("Eighteen in Concord, One in Keeping").
- Every passenger is scanned and gets a colored tint bar. The PC's reads blank: `NULL`.
- The technician (**Calla Wren**) frowns and rescans. Same result.
- Voss, smoothly: "Faulty unit. These things hate sea air. Let them through, Calla." He glances back once. (Players who look closely will see Calla photograph the screen.)
- **Game over `GO_HOMEWARD` "Homeward".** Trigger: at the dock, the PC tells Edda they want to go back. Foreshadowing: Edda asks twice, "Last chance, sprog. Once I cast off, that's it." The ferry leaves. *Epitaph: "You went home. The lights went out one by one, and you watched them from the other shore."* (A Rejuvenation-style joke game over in the first five minutes. It teaches players that GOs exist and are recorded.)

---

## CHAPTER 1 — "Tidewatch" (Ferrow's Landing, the Ferrymen's Mile, Windfall Row)

**Beats:**
1. **Ferrow's Landing.** Tarred stilt-houses, drying kelp, gulls. Juno's parents, Wenna and Coll Hale, run a bramble-tart stall and adopt the PC on sight ("You're the Larch kid? Eat this. You're too thin.").
   - Children skip rope to the **counting rhyme** (01_WORLD_LORE §10). This is the first time players hear it.
   - The PC can collect the **Old Rod** from a fisherman.
   - The Festival poster on the quay shows the Sovereign's Crown with a tiny dark fleck in its stone. "Probably a printing fault." (Crown seed 1 of 3.)
2. **Tidewatch Station.** Professor **Imelda Larch** reads Ines's letter, sets it down very carefully, and pours two cups of kelp tea. "Your mother was the bravest coward I ever knew. Drink. It's disgusting." She doesn't explain. She takes the PC to the **Wayfarer Sanctuary**.
3. **Starter selection.** Any Gen 1–9 starter (SPINE). **Juno Hale** bounces in: Larch's assistant, cheerful, chatty, never not mid-plant-fact. She wears a tilted wreath and a long trailing veil of white-and-pink blossoms from her aunt's Bride Tree, which have never once wilted, over an outgrown flower-girl dress with the hem let down, gardening gloves and a satchel of seed packets. (SPINE Revision 12, Ever-Bloom: the costume carries the sadness, and Juno doesn't.) She picks the starter *weak* to the PC's ("It was looking at me. Also, underdogs.").
4. **Kestrel crashes the ceremony.** He has been sleeping in the Sanctuary's loft because his grandmother kicked him out again. He grabs the counter-starter: "Fair fights are for people who can afford to lose." Larch lets him take it with a look that says she has history with this family.
   - **K1** (lv 6), at the Sanctuary gate. Afterward, Kestrel: "You came in on the last ferry? Great. Velmora's sinking and they're still letting tourists on."
5. **Rowan Ashby visits.** Juno's Uncle Rowan, the Grass Warden, has come down from Verdance to collect seed stock. He's gentle and funny, with soil under his nails. He came "round by Saltmere: the forest road's glass now, and they're putting the Pageant on early this year. Lot of fuss over a play." (Fair clue: the Mourner hijacks that Pageant in Ch2.) He shows Juno and the PC a sickly **Phantump** he rescued "from the Glasswood up past Briarwick. It was sitting in a tree that had turned to glass, crying." (Clue: the Mourner's ace is Trevenant.)
   - He tells Juno about larches: "Everything that grows must be allowed to die, Juno. That's not sad. That's what makes room." He touches one of the blossoms in her wreath as he says it, very lightly, the way you'd touch someone's hand.
   - Of his wife: "She'd have liked you." He's talking to the PC, and it lands oddly.
6. **The Ferrymen's Mile → Windfall Row → the Glassed Orchard** (map 522, `:BLEED`, mandatory tutorial).
   - The Hales' neighbor's apple orchard turned to glass last winter. Glass apples chime in the wind.
   - Juno stops at the **Bleed Veil**: "My skin's burning. I can't — how are you *doing* that?"
   - The PC walks through. Inside, a Bleed-maddened Pokémon (a glassed Wurmple swarm leader) calms when the PC approaches. This is the first demonstration of Harmony.
   - The PC retrieves the farm's lost Skwovet for a reward.
   - Larch, waiting at the edge with a notebook, says very quietly: "Well. That's that, then." She records the first **Field Notes** entry (`:BLEED`).
   - **Game over `GO_ORCHARD` "Two in the Orchard".** Trigger: Juno asks "Can you pull me through? Just for a second?" and the PC says yes. Foreshadowing: the burning line, plus Larch's earlier warning, "Never take a tinted person past a Veil. Never." Juno's hand glasses in yours. *Epitaph: "She trusted you. That was the whole problem."*
   - On Windfall Row the Accord has corded off the old forest road north into the Gossamer Wood: the Glasswood is across it, a mile in. Briarwick, four hours away by that road, is now two days away by the coast. (This sets up why Saltmere comes first.)
7. **Evening.** Hesper Vane's lighthouse. The old woman shouts at Kestrel from the gallery while the PC passes below. She sees the PC and drops her lamp-rag. Inside the lighthouse door, visible if the PC knocks, hangs a **cracked mirror** Hesper refuses to replace: "Leave it. It shows the truth crooked, same as everything." (A Ruin Route seed: it is the last image of `END_REFLECTION`.)

**Cliffhanger:** Larch, at night, writes in her journal (a short cutscene): *"Subject reads NULL. Second such reading in my life. The first was in Crownhaven, AF 290. God help us, Ines."* Fade.

---

## CHAPTER 2 — "Curtain Call" (the Strand Road → Saltmere, Gym 1; J1)

**Location:** **the Strand Road** west along the chalk coast: the Ferrymen's Mile (520), **Lacecliff Walk** (527) and **Marram Down** (528), both `:BEACH`. Then **Saltmere** (Elowen's free port): the promenade (140), the Harbour & Breakwater (146), the Old Town (147), the **Pell Playhouse** (Gym 1, 150/154, `:GRAND_STAGE`) and the **Lantern Theatre** (145).

**Why this chapter comes first.** It is the hook. The player has just learned they're strange (Ch1). Now they learn the realm is arguing about the very thing that makes them strange, and that the argument has a masked face. The Hollow arrive as theater: a voice, a question, a mask. Ch3 turns the question into a person.

**The road.** The PC spends the night at the Hale Farmhouse (Wenna won't hear otherwise, and the Hale Bell guard won't let anyone onto the Strand Road before first light). In the morning Larch walks in to breakfast and sees the PC off: "Saltmere's first. The forest road's corded off, so you go round by the coast. The Warden's Dorian Pell. He'll call you 'darling' and mean it about a third of the time." Juno comes too: her mother has promised forty bramble tarts to the Pageant crowd, and Juno has wanted to see the Pageant since she was six.
- At the Hale Bell an Accord guard waves the PC through the quarantine line. Challengers pass, which is older law than the quarantine. His partner mutters that "the null one from the dock" is to be let through "whatever happens", by order of a white seal from Crownhaven. (Valen's people are already watching.)
- A hay-cart driver: "Used to take me four hours to Briarwick. Now the forest road's all glass and I go round by Saltmere. Two days. Glass doesn't pay my horse."
- On Marram Down, the Pageant's travelling players are camped in their wagons, rehearsing the companion piece in the dunes. A half-buried theater barge hides the **Prompter's Box** (optional): the prompter's script, which hints at how the Grand Stage works, with one page the Accord cut in AF 140 (a seed for the Loyal Three lie).
- The first view of the free port is from the Saltmere Beacon: a white town on a salt lake, every second building a theater.

**Arrival.** Saltmere is salt-caramel stalls, lamplit promenades and a breakwater where the Queen's tax-barges are turned back by tradition. Show it on arrival: an Elowen barge rows in, the whole breakwater stands up and boos, and the barge rows away. The man conducting the booing with a silver-topped cane is **Dorian Pell**, Warden of Saltmere.
- The Blank Plate makes Saltmere *ordinary*: nothing strange ever happens here, and the Bleed has never touched it, so the city makes its own miracles on stage. In a Festival year the **Pageant of the Prismfall** (the official myth, "a gift of love from the Original One") opens in spring and plays through Fallmorn. This year's companion piece is **"The Loyal Three"**: three faithful hounds drive the Gossamer Ogre from the wood.
- Saltmere keeps its own oil lamps along the promenade. They're part of the set, Dorian says, and Meridian may not have them.
- In the Lantern Theatre's prop room, the Accord's Pageant Office has sent new drawings for the Crown prop. The stone is smaller this year, and nobody says why. (Crown seed 2 of 3, between Ch1's "printing fault" and Ch3's chapel mural.)

**J1.** On the promenade green, before the PC's first gym, Juno challenges them to a cheerful spar (**J1**, on `:MEADOW`): "I want to know if I'm any good before you go in there. I want to know if *you* are." Win or lose, she promises to be the loudest person in the house.

**Gym 1 (`:GRAND_STAGE`), a single battle: "the house loves a show".** The Pell Playhouse is a simple, handsome theater: the lobby, the aisle between the velvet seats, three actors who step out of the rows to battle, and one gentle interaction at the end, the curtain rope that flies the house curtain out (GYM_PUZZLES Gym 1). Grand Stage is the PC's first gym field, and it teaches itself: the audience cheers flashy moves, and the cheer lifts the next one. Juno, in the stalls with a cone of salt-caramel, is part of the audience. **Dorian** in velvet: "Enter, stage left, our brave challenger! Your first Warden, your first field, your first audience." His ace is **Kecleon**, which changes "costume" with each type.
- On victory he awards the **Footlight Badge**, and the badge case **hums** faintly the first time a badge goes in: one clear note. (Seed.) Juno: "Ooh, is it supposed to do that?" Dorian has lived his whole life in the one city where nothing does anything: "Darling, in Saltmere nothing is supposed to do *anything*. ...Do it again." It doesn't.
- After the battle, his troupe gives the PC the gift **Eevee "Understudy"** ("forty auditions, never cast — you came off the ferry without a color and this one hasn't picked one either: you two are a matched set"). That afternoon at the Lantern Theatre it is cast in "The Loyal Three" as Tree Number Three and cut for pacing (comedy scene, 15_COMEDY Ch2). At the same rehearsal a costumier asks Juno which play her blossoms are from, and Juno explains, cheerfully, that they're her aunt.

**The breakwater.** At sunset, before opening night, the PC and Juno sit on the end of the breakwater eating salt-caramel. This is a quiet friendship scene, and it should be a breather.
- Juno tells the PC about her blossoms: Aunt Elin, Fixed into the Bride Tree when Juno was three, in permanent bloom ever since. Juno kept wearing the flowers from the wedding, and they've never wilted. "Uncle Rowan says that's the problem. I don't know what he means." (Three hours later, the Mourner says it to a whole theater.)
- **CHOICE `:ch3_juno_talk`:** tell Juno about the NULL scan (Juno Bond up. She promises to keep it secret, and she does) / deflect / say nothing.

**The Pageant.** The PC attends opening night with Juno and Dorian.
- The companion piece plays first. Three actors in hound masks chase a sad-masked, bark-faced Ogre off a painted wood while the children in the gallery boo.
- Mid-performance, the stage lights go **grey**. A child: "Is that the Ogre? He's early!" The **Mourner** steps out of the painted backdrop of the Plates falling. Ash-bark mask, single white lily, doubled voice:
  > *"Three hundred years of pageantry. Ask your Warden why nothing in Verdance ever rots. Ask your Sovereign why the old capital is underwater. Ask why the Loyal Three wore poison on their collars. Let the land grieve."*
- At "nothing in Verdance ever rots", Juno's hand goes to her wreath.
- Bereaved grunts drop Hollow Ring banners from the flies. One of them, a grey-cowled woman with a weaver's shears, cuts the curtain ropes very neatly, and the curtain comes down on the cast without touching a soul. (Thistle; the PC meets her in Ch3.) The crowd panics, and the PC fights two grunts at once.
- The Mourner looks straight at the PC across the theater and goes **still**. "...You." Then he's gone in a burst of Cotton Spore.
- Juno, shaken: "He sounded sad. Isn't that weird? I thought he'd sound evil."
- **First meeting with the Eevee Octave.** The Prism Choir's touring chorus sings the Pageant's hymns. It includes **the Eevee Octave**, eight Glassfall orphans each partnered with an Eevee-line Pokémon. Their leader **Vesper Lindqvist** (24, gentle, devout) finds the PC backstage after the panic and kneels to Understudy: "It hasn't decided which Imprint it belongs to yet. Neither have you, I think." Optional battle vs Vesper's Eevee and Lyra's Eevee (double; Lyra is the Octave's Elowen singer, going home to Briarwick). Encounter 1 of 3. Afterwards Vesper asks the PC to look in on the eight singers as their road goes through the kingdoms (SPINE Rev 19: the Eevee Octave quest line, `design/EEVEE_OCTAVE.md`). Carol, the eighth, never leaves Crownhaven.

**Aftermath and revelation.**
- Dorian, rattled and pale, pulls the PC into his dressing room and presses a yellowed page into their hands: the **prologue of "The Gilded King"** (Key Item). "Ansel Crewe wrote that in AF 52. They hanged him for it. I've never staged it. I'm a coward with excellent diction." The page includes the line: *"If heaven will not kneel, we'll build a chain."* Why the PC? "Out of a whole theater, he looked at you. I've been looked at by audiences for forty years, darling. I know when someone's found the person they came for."
- **Kestrel** is outside the theater, white-faced. He heard the Mourner's voice. "That's — the way she talks — no. *No.*" He runs north, out of the North Gate toward the Gossamer. This sets up the "Mourner = Morwen" rumor, and his hunt (K2, Ch4).
- Dorian, sending the PC on: "Your next Warden is Tamsin Loom, up the Weavers' Road in Briarwick. She inherited the seat in spring and hasn't slept since. Be kind. She'll apologize to you for losing. Let her." Juno decides she's coming too: Uncle Rowan wants silk-moth eggs, and she's not letting the PC walk into the Gossamer alone "after THAT".

**Cliffhanger:** An Elowen herald posts a royal notice on the free port's charter stone. Queen Maelis "notes with grief" the Hollow outrage in *her* free port, "where the Crown's protection was refused". Dorian rips it down in one long tear. "*Her* free port." The North Gate opens.

---

## CHAPTER 3 — "The Weaver's Debt" (the Weavers' Road → Briarwick, Gym 2)

**Location:** **the Weavers' Road** inland from Saltmere's North Gate: **the Grey Saltings** (541, `:BEACH`, with Brinecut Mine), **the Dyers' Ford** (552), **Thistledown Lea** (540, with Thistledown Manor 546/547, the haunted house), then **Gossamer Wood** (524, `:SILKWOOD`) and **Briarwick**. After the gym: the **Gossamer Deepwood** (525) and the Glasswood's heart, **Cocoonfall Hollow** (548, `:BLEED`).

**Why this chapter comes second.** Ch2 asked "Ask your Warden" in front of a thousand people. Ch3 is the same question asked of one tired nineteen-year-old in a loft, with no audience at all. The Hollow stop being a voice and become a grieving weaver with a pair of shears, and Meridian shows its double edge for the first time: the free light is real, and so is the glass.

**The road in.** This is the road Briarwick's cloth comes down. Salt marsh first, then the dyers' river running red, blue and yellow in three bands below the dye-works, then the dead House Thistledown's unmown meadows, then silk.
- A line of orange Meridian survey flags follows the road up into the wood: "Survey line for the new Lattice. Straight through to the wood. Trees aren't in the plan, but trees rarely are." Juno, at the first flag, quieter than she was two days ago: "These go right toward the Glasswood. That's... probably fine?"
- The **Brinecut** salt miner gives the PC TM98 Rock Smash on sight of Dorian's badge. The rocks can be smashed from the second badge on.
- In the Gossamer Wood, the Bug Catcher twins Mo and Jo fight as a pair: a preview of what Briarwick's Warden will do.

**Optional set piece: Thistledown Manor** (comic haunted house, on the Lea's hill). The dead **Thistledown Players**, a ghost acting family, are still rehearsing *Hamlet-but-with-Pokémon*. Two days after a pageant that was stopped mid-scene, here is a company that never let anything stop the show. The PC must "play a role" in three scenes (choose lines; wrong choices start ghost battles). Reward: Spell Tag and a Litwick. The Manor's matriarch-ghost wants the PC to stay for the second act.
- **Game over `GO_CURTAIN_CALL` "Curtain Call".** Trigger: accept her offer to "join the company forever". Foreshadowing: the butler-ghost mouths *don't* behind her. *Epitaph: "Your notices were excellent. The run has not closed. It never will."*

**Arrival.** Briarwick is a weaving village lashed between trees, with looms clacking and silk drying like flags. There is a **shrine to the Loyal Three**, the same story the Pageant told, carved in stone, and someone has left a honey bun in front of the Ogre, not the hounds. Children wear carved **ogre masks** at Fallmorn, and every mask has the same sad face the PC saw step out of a painted backdrop in Saltmere. (Seed for Elowen's legendary arc: the Hollow's masks are the Ogre's.) There is also a Meridian **survey line** of orange flags marching east, toward a half-built Lattice pylon.
- A youngster: a boy in a too-big black coat came through yesterday asking about masks, bought a honey-silk bun and was rude about it. (Kestrel, a day ahead and hunting.)

**Conflict.**
- The silk-moths are dying. The Glasswood, a crystallizing Bleed, is creeping toward the groves, and it is creeping fastest along the Lattice line.
- Warden **Tamsin Loom** (19, anxious, a measuring tape around her neck) is overwhelmed. She is polite, apologetic and lying about something.
- **The first Hollow sabotage.** Somebody is cutting the survey flags at night, and the cuts are very clean: a weaver's shears. The PC catches the saboteurs at the pylon base. This is the **first admin battle: Pallbearer Thistle** (`HOLLOW_THISTLE`), a grieving ex-weaver, and she is the woman who cut the Lantern Theatre's curtain ropes. In Saltmere the Mourner told a theater to ask its Warden. Thistle tells the PC which question: "Lowmarsh had looms too. Ask your Warden what she signed."
- On the way out, a wandering old woman at the Loyal Three shrine (actually **Celestine**, in disguise, unnamed) sings: *"Three loyal hounds and an ogre so bold — but who was the thief, when the story was told?"* After the Mourner's "poison on their collars", this is the second voice saying the pageant has it backwards. (A seed for Elowen's legendary arc and for Celestine's Act V reveal.)

**Gym 2 (`:SILKWOOD`), a double battle: "a thread holds because it's twisted with others."** The Loomhouse is the first real puzzle, and still a friendly one (GYM_PUZZLES Gym 2, SPINE Revision 19): above Granny Loom's looms, the gym is the hollow of Briarwick's elder, strung by Tamsin's Bugs with web trampolines. Taut webs throw you, sticky webs hold you, and two Joltik flip whole strands. Tamsin fights two at a time, because a thread on its own is just string. She battles with nervous fury: "We spun this whole hollow together, the Bugs and me. Don't you dare tear it." Her ace is the Leavanny line.
- On victory she awards the **Weft Badge**, and the badge case answers with a **second note**, in tune with the first. Juno: "It's doing a *chord*." Tamsin: "I don't think they do that. ...Do they do that?" (Each badge adds a tone. Rook films the fourth.)

**Aftermath and revelation.** Thistle's accusation sticks. Tamsin confesses to the PC in the loom-loft: Briarwick is bankrupt, and she signed the Lattice contract alone. The free light works, and the looms ran till midnight for a week. The Lattice is also feeding the Glasswood.
- **CHOICE `:ch2_tamsin`:**
  - **Expose her publicly** at the village meeting. Village trust is shaken and the contract is torn up. The Hollow and Accord gain Standing, and Meridian loses some.
  - **Help her confess herself.** The slow route: she renegotiates the contract, and Meridian keeps a smaller pylon. She never forgets who stood next to her.
  - **Keep her secret.** Meridian Standing goes up. The pylon keeps draining Briarwick, Thistle's cell comes back angrier in Ch10 ("You *knew*"), and in Act V Tamsin can't afford to release her Plate (her Consent condition).
  - Every branch leads to the same next beat.
- **Boss battle, "The Glass Matriarch" (multi-bar, Rejuvenation-style).** The Briarwick Cutter will now give the PC Cut ("Saltmere's badge is a theater ticket. Ours is a badge."). Past a Cut tree in the Gossamer Wood, through the Deepwood, lies **Cocoonfall Hollow**, where a giant glassed **Galvantula** has woven a nest of crystal silk at the Bleed's heart. Tamsin can't cross the Veil, so she gives the PC her grandmother's shuttle "for luck". Defeating the Matriarch slows the Glasswood's spread (map state change: the Hollow's edge recedes on return in Ch10, and the corded forest road back to Windfall Row opens as a shortcut home). The PC's presence calms the nest's Pokémon afterward.
- **CHOICE `:ch2_matriarch`:** the beaten Matriarch thrashes in the silk-moth grove, shedding crystal.
  - **Soothe:** stay with it all night. It calms at dawn, but half the grove crystallizes (Harmony).
  - **Silence:** press your hand to it, and the Imprint drains out of it like water down a drain. The grove is saved, and the Matriarch is left hollow and dull-eyed (Ruin −2). Tamsin, seeing it: "Oh. Oh, that's — thank you. I think."
  - This is the player's first lesson: the efficient choice is the Ruin one.

**Optional thread: cameo sidequest "Lost in the Gossamer" (Shelly).** See `design/CAMEOS.md`. After Gym 2, a pink-haired stranger is stuck in the Gossamer Deepwood, apologizing to the Bug Pokémon. It's the first cameo, and it teaches players that the Glass leaks.

**Cliffhanger:** A Festival poster in Briarwick's square shows the Crown. Its stone is drawn with a tiny chip missing, and someone has circled it in charcoal. The old mural in the chapel shows it whole: "It's painted *before*," says the chaplain. A child: "Mum says the Crown got hurt once. How do you hurt a crown?" The PC's hand moves, unprompted, to their chest. (Crown seed 3 of 3. The Landing's poster called it a printing fault and Saltmere's prop-maker shrank it. Here it's a wound.) Juno heads home to Verdance with forty silk-moth eggs in a hatbox, and the road goes north out of the Gossamer, where the silk on the last trees is already white with frost.

---

## CHAPTER 4 — "Both Ways" (the Hoar Road → Ebbmouth, Gym 3; K2)

**Location:** **the Hoar Road** north out of Briarwick: **Spinners' Rise** (566), **Frostwick Pass** (577), the borderland village **Frostwick** (570), **Rimewood Path** (578) and **the Rimewood** (562), then **Gullcry Cliffs** (561, K2), **Gullcry Caves**, and **Ebbmouth** (Isenmar's southern port). Side road: the **Frostflat Causeway** (560), the salt road back down the coast to Saltmere, chained at the Border Stones until the PC reaches Frostwick. Off it lies **The Rehearsal** (568, `:BLEED`), an optional zone where a stretch of road replays the same five seconds of a wagon crash forever.

**Borderland.** The PC climbs out of the Gossamer and crosses from Elowen into **Isenmar** through the Rimewood, where the same silk forest froze when the sea did. Mixed wild types, the first fur-coated NPCs, bone toggles. At the Handfast Arch on Frostwick Pass, half whale-jaw and half living briar, someone has bolted a Meridian sunburst over both halves. (Frostwick's Border House stamps the same sunburst over both kingdoms' seals.)

**K2 (Gullcry Cliffs, before Gym 3).** Kestrel has been hunting a Hollow cell since Saltmere: Thistle's people, running north out of the Gossamer to join the cell in Ebbmouth. He wants the PC out of his way. He is more raw than in K1. He has his new **Honedge** from his grandmother ("It was your mother's blade's child. Don't you dare lose it."). After the battle:
- **CHOICE `:ch4_kestrel_mourner`:** ask whether he thinks the Mourner is his mother.
  - Kind: Kestrel Bond up a little. He snaps, but later sends a curt note.
  - Blunt: Kestrel Bond down. He shoves past.
  - Silence: neutral. He fills the silence himself: "...She'd never wear a mask. She hated masks."

**Arrival.** Ebbmouth: fog, gulls, smoked-eel stalls and union halls. The **Ebb runs both ways**, but lately it **stutters**, stopping dead for minutes. Mill-wheels freeze mid-turn and dockworkers hold their breath. Meridian's tidal Lattice squats at the river mouth. A strike is brewing: the **Ebb Guild** is squeezed between **Thane Eirik**'s harbor taxes and Meridian's layoffs.
- Ice-fishers in the tavern sing about "**the Sleeping Whale under the ice**". This is a Kyogre seed. ("When the whale wakes, the sea remembers it's a sea.")
- Get the **Good Rod** at the Anglers' Guild.

**Conflict.** Warden **Marisol Reyes**, elected and brash, is caught in the middle. A Hollow cell spikes the tidal Lattice at night, and the river stops entirely for an hour. A child's boat drifts toward the stalled mill-race, and the PC and Marisol rescue the kid in a battle-and-chase. The cell leader is **Teo Reyes** (`HOLLOW_TEO` admin battle), 19 and furious, and he is Marisol's brother. Marisol lets him run. The PC sees it.
- **CHOICE `:ch4_teo`:**
  - Report Teo to the Meridian guard: Meridian Standing up, Marisol's Bond down hard, and Teo is hunted (his Act II arc gets harder).
  - Keep Marisol's secret: Marisol's Bond up, Hollow Standing up a little.
  - Confront Marisol privately: Marisol's Bond up. She admits it, crying and swearing.

**Gym 3 (`:WATER_SURFACE`).** Thematic note: *a current that changes direction mid-fight.* Marisol: "The Ebb runs both ways. Always has. Lately it can't decide." Her ace is **Gyarados** (from her first Magikarp on the docks). Afterward she buys the PC smoked eel and says the thing Act I needs said: "Meridian pays my people. Meridian's killing my river. Pick one, kid, I dare you." (Tamsin couldn't pick, and signed. Marisol won't, and swears.)

**Revelation.** Larch arrives by Gale Post with tide data. The stutters line up *exactly* with Meridian's Lattice draw peaks. "It's not the Hollow stopping the river. It's us. It's *my* design." This is the first crack in Larch's guilt.

**Cliffhanger:** Hesper Vane's letter reaches the PC via the post: *"Whoever you are — stay away from my grandson. Everyone who gets close to that boy's mother's ghost gets hurt."* Unsigned, but on lighthouse paper.

---

## CHAPTER 5 — "Ten Years of Light" (the Lock Road: The Icefall Locks → Wallshadow Row → Lumen City, Gym 4; the Lowlight Shatter)

**Location:** **the Lock Road** up the Ebb and round the Crownwall: **the Reedholms** (580), **the Icecutters' Haul** (592), the lock-town **Brassfall** (590) and **the Icefall Locks** (581, borderland B), then Elowen's Crownlands on **Coppice Ride** (595) and **Wallshadow Row** (594, the Crown Road's south-west arc), then **the Arc-Lamp Mile** (593, borderland G) into **Lumen West Gate** (582). Off the road: **Voltaic Sluiceworks** (`:SCRAPYARD`, Rotom) and **Ebb Hollow** (588, `:BLEED`). Then **Lumen City** (Zenith's capital district), the **Lowlight** district (181, replaced by 608 after the Shatter), **Meridian Spire**.

**The road.** Isenmar never touches Zenith, so the Lock Road crosses Elowen to get there. The PC climbs the frozen falls of the Icefall Locks, past Meridian's Extraction Lattice No. 4, onto the Crownland downs. At the ride-side shrine on Coppice Ride they see **the Crownwall** for the first time: a ring of white peaks with Crownhaven inside, where nobody goes without eighteen badges. The star-shaped scar on their chest aches, and they don't know why. Wallshadow Row's tithe barns and the Southgate shrine take the Crown Road round the wall's south side, and then the hundred numbered lamps of the Arc-Lamp Mile run out of the orchards to Lumen's West Gate.

**Arrival.** The first big-city wow moment: airships, holograms, Rotom delivery drones and a skyline of brass and glass. Everything is free-lit and humming. "Light for Everyone" banners celebrate **Lumen's Tenth Year of Light**, ten years since the first Lattice switched on.
- The PC meets **Dex** (11), a Fizzbolt soda seller outside the Spire. He's talkative and lovely, and he tells you which roof has the best airship view. He's halfway through a story about his sister when he waves the PC off: "Tell you the rest tomorrow!"
- Topside versus below. Down every alley there are grilles and lift-shafts into **Nadir**, with grimy air coming up and Hollow Ring graffiti. A Zenith officer moves a Nadir kid along: "Back downstairs."

**Rook's gym is closed** because he's filming. The PC helps **Rook Calder** with a blackout in the Sluiceworks (wild Rotom swarm) and earns his attention. He's hyper, a little lonely, and constantly on camera: "Chat says you're cute. Chat also says you're gonna lose."

**Gym 4 (`:NEON_GRID`).** Thematic note: *circuits you complete with your own body.* Rook's ace is **Rotom** (his camera drone, in battle form). After the badge, he gives the PC Flash. He's also the first person to notice the badge case pulse brighter on the fourth badge, the fourth note of a chord that started in Saltmere. He films it: "Ooh, special edition?"

**The Gala (main set piece).** Voss invites the PC, Juno, Rook and Larch (Larch refuses at first, then comes to keep an eye on things) to Meridian Spire's **Tenth Year Gala**.
- Champagne, airships outside the windows and the **Dark Stone core** glowing black in the atrium shaft. (Zekrom seed: guests swear it "breathes".)
- Voss's speech: *"They'll tell you light is a gift. Light is work. Every lamp in this city was lit by someone who was told to be grateful for the dark."* It's genuinely stirring.
- **Valen Corrigan** is present. White robes, grey glove, grave and courteous. He speaks briefly with Voss and with nobody else.
- Larch, murmuring to the PC: "The Zap Plate's not in Rook's gym, you know. It's *here*. In their vault." Rook, overhearing, goes very quiet.

**The raid.**
- Lights flicker. The **Hollow** breach the Spire through Nadir's service lifts. **Partner battle: PC + Juno vs two Bereaved Pallbearers' squads**, the first tag battle.
- The PC pursues them down to the **Plate Vault** and arrives in time to see it go wrong. The **Mourner** reaches the Zap Plate's cradle, but **Sable** (masked, Hollow-grey, cheerful) slaps a **Splitter** charge on the Plate. The Mourner lunges for it.
- **The Shatter.** A white-violet blast. The Plate cracks. The Mourner catches it barehanded and his glove *smokes*: "No — no — what did you *do*?" (To Sable. The player will read it as aimed at the PC or at himself.) Sable is gone. The Mourner sees the PC, drops the cracked Plate into its cradle, and flees.
- **Boss battle, "Overcharged" (multi-bar):** a Bleed-maddened **Electivire**, swollen with the Shatter's discharge, blocks the vault door. The field flips mid-battle from `:NEON_GRID` to `:BLEED`, the first scripted any→BLEED transition.
- **Game over `GO_LIVE_WIRE` "Live Wire".** Trigger: during the Electivire fight's interlude prompt, choose "Grab the cracked Plate and run". Foreshadowing: the Mourner's smoking glove a moment earlier, and Rook's shout, "Don't touch it with your hands!" *Epitaph: "Even you weren't made to hold lightning bare."*

**Aftermath: the Lowlight.**
- The Spire's shadow-district has been hit by the Shatter wave. **Twelve people are Fixed in glass mid-motion**: a woman hanging laundry, a man mid-laugh, and **Dex, mid-wave**, soda crate on his hip.
- The PC can walk through the Lowlight's Veil (map 608, `:BLEED`) when no one else can. They are the only one who can stand among the glass. NPCs watch them do it.
- Rook, off-camera, shaking: "...Turn it off. Rotom. Turn it *off*."
- **Voss restores the light.** Meridian crews reroute the grid in under an hour, and Lumen sees Voss on every screen, in shirtsleeves, carrying a glassed child's soda crate out of the Lowlight himself. He's a hero. (He means it, and he did it. Both are true.)
- **Valen** walks into the Lowlight's edge, removes his glove for a moment to touch the Veil, and the player glimpses crystal. Then he sees the PC standing *inside*. "You were in the Lowlight when it went? And you're... standing." He looks a beat too long, then turns away.
- Valen's broadcast that night grants Meridian **the Mandate**: security powers wherever Lattices stand. "Velmora endures."

**CHOICE `:ch5_lowlight_testimony`:** a Directorate officer asks what the PC saw.
- **"The Mourner broke the Plate"** (what it looked like): Meridian Standing up, Hollow Standing down, and the Mandate passes with a bigger majority (flavor).
- **"Someone else was there"** (the masked second figure): Hollow Standing up, Meridian Standing down a little. Marchetti makes a note of the PC's name. Larch quietly says "good".
- **"I don't know"**: neutral.
- If the PC said "The Mourner broke the Plate", **Dorian** reads it in the papers in Saltmere: "So you told them the pageant version. I know that one by heart." This seeds his Act V refusal: he keeps the lie he knows, and won't release the Blank Plate. (He was the first Warden who trusted the PC, which is why it stings.)

**Revelation.** Larch, in the ruined vault at 3 a.m. with a borrowed scanner: "That wasn't the Hollow's hammer. Look at the stress lines. The Plate was *already* cracking. Something's been drinking from it for ten years." She looks up at the Lattice conduits. "Something I built."

**INTERLUDE I — "Lamplight"** (playable as **Kestrel**).
- Ferrow's Landing lighthouse, the same night. The player controls Kestrel on the gallery while Hesper sleeps.
- He finds his mother's old Ghost Warden's veil in a trunk.
- A short memory plays: Kestrel, age 6, in a crowd, his mother in a veil running toward "a kid made of light". He wakes before he sees the rest.
- Mini-battle: Kestrel vs a wild Bleed-touched Haunter on the lighthouse stairs. He talks to his Honedge like a person.
- It ends with him packing a bag. "If you're alive, I'll find you."

**END OF ACT I.** Title card: *II — Imprints.*
