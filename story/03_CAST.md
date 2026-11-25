# Story Bible 03: Cast

> Ace Pokémon are **concepts**. The balance team has final say on species, levels and movesets. Per SPINE Revision 2 the base project includes the Gen 9 pack (1,025 species), so validate species against `/home/claude/ref/ebdx/PBS`. Every character here is original. The sister-fangame cameos are optional sidequests (`design/CAMEOS.md`). Trainer type IDs follow SPINE (`LEADER_<FIRSTNAME>`, `RIVAL_KESTREL`, `RIVAL_JUNO`, `CHAMPION_VALEN`, `HOLLOW_*`, `MERIDIAN_*`, `FESTIVAL_<NAME>`).

---

## THE PROTAGONIST (PC)

- **Name/gender:** player-chosen. Age 15. Born in Lower Crownhaven, AF 285. Raised abroad in a small fishing town across the Hallow Strait (deliberately left unnamed).
- **Status:** **Unimprinted.** Meridian scanners read them as `NULL`. They can enter Bleed zones unharmed, and Bleed-maddened Pokémon calm down near them. *Secret:* a splinter of the Legend Plate is lodged beneath their sternum. They have a small, star-shaped, colorless scar there that they've had "since forever".
- **Mother:** Ines, a former cantor in the Prism Choir. She fled Velmora with the five-year-old PC on the night ferry after the AF 290 Glassfall and wilted for ten years in exile (see 01_WORLD_LORE, "Wilting"). She died last winter. Her final letter, which the player can reread from the Key Items pocket, reads:
  > *"Go to Imelda Larch at Ferrow's Landing, before they close the strait. Don't let anyone scan you. Don't go to Crownhaven. I'm sorry I never told you why. I wanted one of us to have an ordinary life. — Mum."*
  The PC is scanned within five minutes of landing. They go to Crownhaven anyway.
- **Voice and choices:** The PC is mostly silent, but every major scene offers 2–3 choices, usually a **kind** option, a **blunt** option and a **silent** option. Silence is a real choice that some characters read as strength and others as coldness. Choices move relationship variables (see FLAGS.md). The PC speaks full, authored lines in four places:
  1. **Ch13, the Mindscape:** their five-year-old self speaks, and the PC answers.
  2. **Ch15, after K6:** the player picks one of three things to say to Kestrel, and each one is a complete authored line.
  3. **Ch20, Valen's audience:** the PC answers Valen's confession.
  4. **Ch21, before Arceus:** the final choice is spoken aloud.
- **Arc:** The PC goes from object to agent. Every faction treats them as a key, a weapon, a vessel or a vote. The arc completes when they stop being carried and choose what they carry.

---

## RIVALS

### Kestrel Vane — `RIVAL_KESTREL`
- **Age 16.** Lean, sharp-featured, black coat that's a size too big because it was his mother's. He has a habit of tapping two fingers against his sternum when he's angry. (Late echo: the PC's scar is in the same spot.)
- **Background:** Son of **Morwen Vane**, Ghost Warden of Gravenmoor, who was stripped of her seat in AF 290 for "the negligence that caused the Glassfall" and died in exile in AF 296. Since then he has been raised by his grandmother Hesper in the Ferrow's Landing lighthouse. He was six at the last Festival and has a recurring nightmare about "a kid made of light" that he has never told anyone about.
- **Personality:** Aggressive, proud, funny in a cutting way, and allergic to pity. He picks the starter with the type advantage because "I don't do fair fights. Fair fights are for people who can afford to lose." Underneath he is desperate to make the name *Vane* mean something other than *disgrace*.
- **Voice:**
  - *(K1)* "You came in on the last ferry? Great. Velmora's sinking and they're still letting tourists on."
  - *(K3)* "Everyone keeps telling me to let it go. My mother had a seat, and a Plate, and a city that loved her. Then one night she had nothing. Let *what* go?"
  - *(K8, tearing off the gauntlet)* "No. Not like this. If I beat you, I beat *you*."
- **Motivation:** Clear his mother's name. He spends Acts I–II convinced that the Mourner *is* his mother, alive and hiding. The rumor runs all over Velmora, and Kestrel half hopes and half dreads it's true.
- **Arc by slot:**
  - **K1** (Ferrow's Landing, lv 6): crashes the starter ceremony and grabs the counter-starter.
  - **K2** (before Gym 3, the Ebbmouth causeway): he's hunting Hollow cells and wants the PC out of his way.
  - **K3** (after Gym 5, Duneholt): reveals the Mourner rumor and why it matters to him.
  - **K4** (Ironreach Open final): fights the PC for a Colosseum title and then fights alongside them in the Conclave attack. He is crushed when the unmasked Mourner turns out *not* to be his mother.
  - **K5** (Skyreach): now Meridian-sponsored. Voss has promised him "the full AF 290 file". He steals the Gale Post's dead letters.
  - **K6** (Gravenmoor): learns the truth in the Hollow Cathedral echo. His mother destroyed her own name to protect the PC. The battle is raw and furious.
  - **K7** (Gloaming): has registered for the Festival as Meridian's sponsored challenger. He tries to stop the PC from going: "They all want to *use* you. Stay out of Crownhaven and let me end it."
  - **K8** (Festival semifinal): fights with Meridian's Resonance Gauntlet, then tears it off mid-battle. Afterward he finally reads his mother's letter.
  - **Finale:** turns on Voss when Voss admits Meridian cracked the Crown. He fights beside the PC in the hijack tag battle.
- **Team concept:** the counter-starter; **Aegislash** line (a Honedge his grandmother gives him in Ch4: "It was your mother's blade's child"); **Staraptor** (namesake raptor); **Scizor** (his duelist from K4 at Ironreach; it Mega Evolves only through Morwen's Ring, at K8, if the PC gave it to him in Ch18); later **Mismagius** (Morwen's partner, inherited from Ysolde after K6); **Hydreigon** or **Weavile** as a late power pick. **Ace: Aegislash.** The sword-and-shield is the son defending his mother.
- **Epilogue:** He becomes Ghost Warden of Gravenmoor if `KESTREL_ACCEPTED_SEAT` is set (Ysolde offers it after the Festival); otherwise he becomes a wandering trainer.

### Juno Hale — `RIVAL_JUNO`
- **Age 15.** Freckled, with frizzy auburn hair under a tilted wreath of white-and-pink blossoms from her aunt's Bride Tree, and a long veil of them trailing behind her to the ground. They're Imprinted, so they never wilt, and she has worn them every day since she was three: the flower girl of a wedding that never ended (SPINE Revision 12, Ever-Bloom). Underneath: an outgrown flower-girl dress with the hem let down, gardening gloves clipped to the sash, and a satchel of seed packets she labels in tiny handwriting. Professor Larch's assistant at Tidewatch Station. The costume carries the sadness. Juno doesn't: she's the warmest, chattiest person in any room.
- **Background:** Her parents, **Wenna and Coll Hale**, run Hale's Bramble, a berry farm outside Ferrow's Landing. They are warm, ordinary and alive, the homey anchor the PC never had. Wenna's sister **Elin** married **Rowan Ashby**, the Grass Warden, and Juno spent every childhood summer in Verdance. Elin was Fixed in AF 288, when Juno was three. Juno was told Aunt Elin "went away" until AF 293, when Rowan walked her to the Bride Tree and told her the truth. She splits her time between Larch's station and Verdance. "Uncle Rowan" is her hero.
- **Personality:** Earnest, curious, kind and talkative. She picks the starter weak to the PC's "because somebody should give the underdog a chance. Also it was looking at me." Her anxiety hides under a constant stream of plant facts. She is braver than she knows. Strangers ask which play her flowers are from; she tells them cheerfully that they're her aunt.
- **Voice:**
  - *(Ch1)* "Did you know larches are the only conifers that drop their needles? Every winter they look dead. They're not! They're just... letting go so they don't snap. Professor says that's the most sensible thing a tree's ever done."
  - *(J3, as Warden)* "I didn't want this seat. I wanted *him* in it. But the city's drowning in flowers and nobody else is coming, so. Hi. I'm the Warden of Verdance. Please don't go easy on me — I'll cry either way."
  - *(J4)* "We started on the same dock. Let's see who's grown more."
- **Motivation:** Make the people she loves proud, and later, become someone worth the seat she inherited.
- **Arc by slot:**
  - **J1** (Ch2, Saltmere, before Gym 1): a cheerful spar on the promenade green, then the loudest seat in the Playhouse, then salt-caramel on the breakwater, where she tells the PC about the blossoms. She walks on with the PC to Briarwick in Ch3 (silk-moth eggs for Rowan) and is there for both of the badge case's first notes.
  - **J2** (Mirefen): she finds Rowan's name in Corvin's ledger and refuses to believe it.
  - **Ironreach:** watches the Mourner's mask break.
  - **J3** (Gym 9): her Warden trial and gym battle, the most emotionally loaded gym in the game.
  - **Acts III–IV:** an increasingly confident Warden who leads the anti-Meridian "Greenward" bloc. She carries her guilt over visiting Rowan in prison.
  - **J4** (Festival R16): a joyful, bittersweet battle between equals.
  - **Finale:** the first Warden to release her Plate. "Verdance has never had an autumn. I'd like to see one."
- **Team concept:** the starter weak to the PC's; **Bounsweet → Steenee → Tsareena** (grown from a seed-pod in Act I, so it rises from a sweet fruit to a queen); **Whimsicott**; **Lilligant**; **Gardevoir "Veil"** (a Ralts that hid in her blossom veil at Lucent, Ch13; it's her Festival Mega once Rowan's ring answers her); **Shiinotic**. **Ace: Tsareena.**
- **Epilogue:** In Homecoming, Elin wakes under Juno's first autumn, and the wreath finally wilts.

---

## THE THREE POWERS

### Aurelian Voss — CEO of Meridian Concord (`MERIDIAN_VOSS`; final battle ~lv 98 on `:PRISM_ARENA`)
- **Age 47.** Tall and silver at the temples. Bespoke charcoal suit with a single gold pin of Meridian's sunburst. He never raises his voice. Warm handshake, perfect memory for names. He drinks tea from a chipped company mug he's had since he was a linesman.
- **Public story:** Born in Halden's Reach, a Bleed-adjacent Nadir mining town, to a poor branch of a Zenith founding house that lost its Council seat generations ago. He started as a Lattice linesman and built Meridian into the company that "lit Velmora". He won his family's seat back and now **chairs the Zenith Council**, which makes him the city-state's head of government. He still visits job sites in person. Topside loves him, and Nadir remembers he was once one of them, which is the only reason they tolerate him at all.
- **True story:** The last heir of **House Aurel**, the line of the Gilded King. ("Aurelian" is a family name that hides in plain sight.) His family survived 300 years under the name Voss and helped found Zenith in AF 118, deliberately *on top of* drowned Aurelia. They passed down fragments of the Gilders' science and one belief: *the god owes us.* In AF 290, as Meridian's head of research, he installed the "monitoring array" in the Crownhaven Basilica, which drew on the converged Plates and cracked the Crown. He watched the Glassfall and understood what he was looking at: the power of eighteen Plates in one place.
- **Philosophy:** "Gods are absentee landlords. Arceus dropped its furniture on our heads three hundred years ago and never came back to collect it. Every generation since has paid the rent in blood. I'm not trying to become a god. I'm trying to make sure we never need one again."
- **Voice:**
  - *(Prologue, ferry)* "First crossing? Take the badge case — Meridian makes them for the League anyway. Call it a welcome gift from a fellow traveler. No, I insist. Somebody should be kind to you on a day like this."
  - *(Ch5, Lumen Gala)* "They'll tell you light is a gift. Light is *work*. Every lamp in this city was lit by someone who was told to be grateful for the dark."
  - *(Ch17, throne room)* "Twelve people in the Lowlight. I've lost more to the Bleed in a quiet week. I made those twelve *mean* something."
  - *(Festival, hijack)* "You carried my key through eighteen doors. Let me show you what it opens."
- **Motivation:** Sincere, terrible conviction, plus inheritance. He genuinely wants to end the Bleed, end Velmora's dependence on Wardens, and give power "to those who make it". The binding of Arceus is his family's unfinished sentence, and he means to finish it.
- **Arc:** Patron (Act I) → protector (the Mandate, Act II) → embattled reformer (Act III) → revealed heir (Act IV) → hijacker (Act V).
- **Fate:** Arceus's Judgment strikes him when he tries to command it. If `PC_SPARED_VOSS` is set (the PC chooses to shield him with the shard in the final moment), he survives, crippled and imprisoned. He has one epilogue scene: he asks to see the sunrise. If not, he is Fixed into light at the center of the arena.
- **Team concept:** "Things men made." **Silvally** (ace; Meridian's "Project NULL", a replica of what the PC is. On the Prism Arena its type follows the active field via Meridian memory discs). **Porygon-Z**, **Golurk** (an Aurel family automaton dredged from Aurelia), **Duraludon**, **Magnezone**, **Klinklang**.

### Valen Corrigan — Sovereign of the Accord (`CHAMPION_VALEN`; Festival final ~lv 96)
- **Age 58.** Broad-shouldered, close-cropped white hair, a soldier's posture. He wears white Sovereign's robes and **always one grey glove on his left hand**. Under it, the arm is crystal to the shoulder.
- **History:** Won the AF 270 Festival at 28 and defended it in AF 280 (against Brann) and AF 290. He was briefly married to Lucent scholar Edith Marr. Their daughter **Ilsa** took her mother's name after he chose the Seat over them.
- **What he knows:** Everything. The Tuning. The Crown. The depleting shard. The Quiet Towns sealed off the maps. Meridian's hand in AF 290 he only suspects, because he never let himself investigate. He scapegoated Morwen Vane so the world wouldn't learn the ceremony could fail, and has spent ten years searching for "the child". Since the Fracture, every Tuning has cost him far more. He will not survive another.
- **Personality:** Grave, gentle, exhausted, and capable of terrible decisions made calmly. He loves Velmora the way a man loves a house he's holding up with his back. He doesn't defend his lies; he explains them.
- **Voice:**
  - *(Ch5, after the Shatter)* "You were in the Lowlight when it went? And you're... standing." *(He looks at them a beat too long.)*
  - *(Ch9)* "Come to Verdance. There's a seat to fill, and I think you should see what it costs."
  - *(Ch20, audience)* "Every ten years I bring the Plates home to Crownhaven, and every ten years Velmora *endures*. You noticed I never said 'thrives'. Nobody ever notices."
  - *(Ch21, holding the ring)* "Go. Free it. I'll hold the door — I've had thirty years of practice."
- **Arc:** A remote authority (Acts I–II), then a judge (Act III), then exposed as a liar (Act IV), and finally a confessor and sacrifice (Act V). He dies holding the Concordance Ring during the Arceus battle. If `ILSA_RECONCILED`, Ilsa is at his side and he calls her "little owl", a name the player heard in her Mindscape.
- **Team concept:** **Zygarde** (ace; the Order Pokémon. Lore: Zygarde cells threaded through Velmora's crust have been helping hold the land together, and Zygarde chose Valen in AF 270. "Order, not justice. I chose order."); **Bronzong** (the Crownhaven bells); **Gallade**; **Lapras** (the ferry motif: "she carried me out of a flood once"); **Volcarona**; **Kingdra**.

### The Mourner / Rowan Ashby — leader of the Hollow (`HOLLOW_MOURNER`); former Grass Warden of Verdance
- **Age 52.** Rangy and weathered, with soil permanently under his nails and a soft burr of a voice. As the Mourner he wears a grey cowl and a carved **ash-bark mask with one white lily**. A Chimecho-resonance plate inside the mask doubles his voice.
- **Background:** Grass Warden for 24 years. His wife **Elin** (Juno's aunt) was Fixed in AF 288 while tending the Heartgarden. The Bleed turned her into a flowering tree that has never stopped blooming. Verdancers call it "the Bride Tree", and Rowan waters it every dawn. He attended three Tunings and asked Valen what they really did. Valen told him to tend his garden.
- **Why him** (full justification in 02_FACTIONS):
  - He is the man who loves the land most, and so the one who sees the Imprint as a sickness.
  - He knows the Accord from the inside.
  - His unmasking is what makes the SPINE-locked Juno succession happen.
  - It turns the friendly rival's story into the emotional core of Act III.
- **Personality:** Gentle, patient, funny with children, devastating when grieving. As the Mourner he is theatrical and liturgical, because grief needs ritual.
- **Voice:**
  - *(Rowan, Ch1)* "Everything that grows must be allowed to die, Juno. That's not sad. That's what *makes* room."
  - *(The Mourner, Ch2, Saltmere stage)* "Three hundred years of pageantry. Ask your Warden why nothing in Verdance ever rots. Ask your Sovereign why the old capital is underwater. Let the land grieve."
  - *(The Mourner, Ch5, holding the cracked Zap Plate, hand burning)* "No — no — what did you *do*?" *(He is speaking to Sable. The player will assume he means the PC or himself.)*
  - *(Unmasked, Ch9)* "Juno. Don't look at me like that. Look at the flowers. Look at what they're standing on."
- **Arc:** Gentle uncle (Act I) → masked zealot (Acts I–II, with fair clues) → unmasked and imprisoned (end of Act II) → tribunal (Ch13), where the PC's testimony matters → escapes in the Fault and leads the reformed "Lantern Hollow" as uneasy allies (Act IV) → in disguise at the Festival → in Homecoming, he is under the Bride Tree when Elin wakes.
- **Team concept (as the Mourner):** **Trevenant** (ace; as Rowan in Ch1 he shows Juno and the PC a sickly Phantump he rescued from the Glasswood, which is a fair clue); **Shiftry**; **Cacturne**; **Gourgeist**; **Abomasnow**; **Breloom**. As Warden, his public team was gentler: Leavanny, Roserade, Sunflora.

---

## MENTORS & ALLIES

### Professor Imelda Larch — Tidewatch Station, Ferrow's Landing
- **Age 56.** Wiry, grey braid, oilskin coat, reading glasses on a chain. She constantly drinks a bitter kelp tea nobody else can stand.
- **Secret:** She was **Meridian's Chief Engineer and invented the Lattice.** She left in AF 292 when her models showed the drain was accelerating the Bleed, and Voss buried the report. She was Ines's friend and knew the child was "hurt at the Fracture" and "different", but not about the Legend Plate.
- **Why she has every starter:** Tidewatch's **Wayfarer Sanctuary** studies how foreign Pokémon resist Imprinting. For twenty years professors abroad sent her starter-line Pokémon, which explains the Reborn-style any-starter choice.
- **Voice:** "I lit up this whole region, you know. Eleven cities on my design. And I think I'm killing it. Drink your tea." / "Science is just refusing to be lied to by things that can't talk."
- **Arc:** Mentor (Act I) → investigator (Act II) → publishes the **Larch Papers** and is framed (Ch12) → hides in Cragholm and explains the badge-case telemetry (Ch14) → at the Festival she reads the Engine's live output (Act V).

### Captain Edda Morrow — the ferry *Dovetail*
- **Age 64.** Squat and weathered, with a gold tooth and a Lapras tattoo. Gruff with a hidden tenderness.
- **Secret:** In AF 290 she ran the **night ferry** that smuggled Ines and the five-year-old PC out of Velmora on Morwen Vane's coin. Bringing them back on the last ferry is a coincidence that she doesn't believe is one.
- **Voice:** *(Prologue)* "Don't look down at the strait at night, sprog. The old city's lamps still burn under there." / *(Ch1)* "You stand at the rail like somebody I used to know." / *(Ch15)* "I took you out on the night ferry. Brought you back on the last one. Tide's got a sense of humour."
- **Role:** After the quarantine impounds the *Dovetail*, she turns smuggler. She runs the PC to the outer islands and to Underveil, and evacuates Crownhaven in the finale.

### Brother Wick — Hollow theologian (`HOLLOW_WICK`)
- **Age 70.** A defrocked Prism Choir priest, blind in one eye, gentle, who quotes scripture he was excommunicated for reading. He co-founded the Hollow with Rowan and is the source of the "Return" doctrine.
- **Voice:** "The Choir teaches that the Plates were a gift. Child, nobody bleeds for three hundred years from a *gift*."
- **Role:** Hollow admin (Ch7). Later he becomes the bridge to Celestine's Hymn of Return.

### Calla Wren — Voss's executive assistant
- **Age 26.** Immaculate and polite. She runs the scanner at the dock in the Prologue.
- **Arc:** She becomes increasingly uneasy. She leaks Voss's itinerary to Nyx (Ch17) and smuggles Larch the arena's power schematics in Act V. She is a quiet defector, never a fighter.

---

## THE EIGHTEEN WARDENS

Format: look/age · personality · voice · motivation · secret · plot role · arc & reappearances · ace concept.

### 1. Dorian Pell — Normal — Saltmere — `LEADER_DORIAN` — `:GRAND_STAGE`
- **56.** Former matinee idol in a velvet coat with a silver-topped cane he doesn't need. His laugh fills rooms on purpose.
- **Personality:** Flamboyant, vain, and generous. He speaks in stage directions ("*Enter, stage left, our brave challenger!*") and is a devoted father-figure to his troupe. As the first Warden most challengers meet, he makes them look good on purpose: a first gym "should be an occasion".
- **Voice:** "Saltmere is the only city in Velmora where nothing is a miracle, darling. So we *built* our own." / "Every pageant is a lie. The trick is choosing which lie to tell." / *(Act V)* "Tonight, for one night only, the truth. Lights, please."
- **Motivation:** Keep the stage alive in a city with nothing else.
- **Secret:** As the Accord's Pageant-Master he stages the official *Pageant of the Prismfall* and knows it's propaganda. He owns the last copy of **"The Gilded King"**, a banned play by Ansel Crewe, a playwright executed in AF 52, that tells the true story.
- **Plot role:** The first Warden (Ch2). His gym is a simple, handsome theater (a walk up the aisle, three actors, one curtain rope) and a **single battle** on the PC's first gym field: the house loves a show. The badge case first hums in his hands, in the one city where nothing strange ever happens. The Mourner hijacks his pageant the same night (Ch2), and he slips the PC the play's prologue page, the first written clue. Saltmere is Elowen's free port, chartered to answer to no king, and Dorian guards that charter jealously against Queen Maelis's tax-collectors (he conducts the weekly booing of her barge himself).
- **Arc:** His troupe gives the PC the gift Eevee "Understudy" right after Gym 1 (Ch2). In Act III Elowen's crown shuts his Lantern Theatre at Meridian's request for a satire about Meridian. On the Festival's Night of Masques (Act V) he stages "The Gilded King" in Crownhaven in front of Voss, which turns public opinion. He casts **Celestine**, who cannot lie, as the voice of Princess Maren's lament.
- **Ace:** **Meloetta** (the Prima Donna — Aria the singer, Pirouette the dancer; a wandering muse who joined the Pell Playhouse years ago and draws no salary; she holds back to Act One tempo in Gym 1 and is never catchable there; full power in the post-game Crownhaven Encore and the Festival Pageant Bout); also **Smeargle** (set painter), **Chatot** (diva), **Hisuian Zorua** (phantom understudy), **Ditto** (body double), **Kecleon** (quick-change artist; Color Change is a costume change), and later **Mega Lopunny** / **Exploud**.

### 2. Tamsin Loom — Bug — Briarwick — `LEADER_TAMSIN` — `:SILKWOOD`
- **19.** Ink-stained fingers, a measuring tape around her neck, and a moth-wing shawl woven by her late grandmother. She became Warden last spring when Old Mother Loom died.
- **Personality:** An anxious perfectionist who apologizes constantly. She thinks in thread and turns ferocious the moment her people are threatened.
- **Voice:** "Sorry — sorry — the Silkwood's a bit tangled today. Like me." / "A thread holds because it's twisted with others. Alone it's just... string." / *(battle start)* "We spun this whole hollow together, the Bugs and me. Don't you dare tear it."
- **Motivation:** Keep Briarwick's looms running and live up to a legend.
- **Secret:** Briarwick is bankrupt. She secretly signed a Meridian Lattice contract alone, and the Lattice is pushing the Glasswood (a crystallizing Bleed) toward the silk-moth groves.
- **Plot role:** The second Warden (Ch3). After the Mourner's public question in Saltmere ("Ask your Warden"), she is the first Warden the PC sees who has an answer to hide. She gives the PC their first look at Meridian's double edge (the free light works, and so does the glass) and the first Hollow sabotage (Thistle's cut survey flags). Her gym is the first real puzzle and a **double battle**: "a thread holds because it's twisted with others."
- **Arc:** Confesses after the gym and either tears up the contract publicly (`TAMSIN_PUBLIC_CONFESSION`) or renegotiates it quietly. Reappears in Ch10 at the Verdance succession as the first small-town Warden to join Juno's Greenward bloc, and again in Act V weaving the Festival's eighteen banners. During the hijack, her Galvantula nets catch falling arena debris.
- **Ace:** **Leavanny** line (the tailor; Swadloon at Gym 2, cap 19), fighting beside a partner in doubles; later **Galvantula**, **Masquerain**.

### 3. Marisol Reyes — Water — Ebbmouth — `LEADER_MARISOL` — `:WATER_SURFACE`
- **34.** Broad-shouldered dockworker in rolled sleeves and a union pin, with a laugh like a foghorn. Ebbmouth is Isenmar's southern port and the only city whose Warden is **elected** (by the Ebb Guild). The Guild has fought Thane Eirik's harbor taxes for a generation.
- **Personality:** Brash, warm and profane ("tides take it"). She would die for her crews.
- **Voice:** "The Ebb runs both ways. Always has. Lately it can't decide." / "Meridian pays my people. Meridian's killing my river. Pick one, kid, I dare you." / *(Ch9 or Ch13, if Teo died)* "He was nineteen. *Nineteen.* Tell me again how the Hollow are the monsters."
- **Motivation:** Jobs versus the river: she needs both.
- **Secret:** Her little brother **Teo** runs Ebbmouth's Hollow cell. She has been tipping him off about Meridian patrols.
- **Plot role:** K2 happens on her causeway. Teo is a recurring Hollow admin.
- **Arc:** At Ironreach the PC's choice decides whether Teo lives (`TEO_SAVED`). Either way, in Act III she leads the **Ebbmouth strike** and cuts the tidal Lattice. In Act V her fishing fleet evacuates Crownhaven's lower city during the hijack.
- **Ace:** **Gyarados** (raised from a Magikarp on her first day on the docks: "Everyone laughed at it too."); also **Floatzel**, **Pelipper**, **Lanturn**.

### 4. Rook Calder — Electric — Lumen City — `LEADER_ROOK` — `:NEON_GRID`
- **20.** Bleached undercut, holo-jacket and a Rotom camera drone always recording. Lumen's celebrity Warden and the face of every Meridian billboard.
- **Personality:** Hyper and charismatic, with catchphrases ("Stay *charged*, Lumen!") and deep insecurity. He has never been offline long enough to know who he is.
- **Voice:** "Chat says you're cute. Chat also says you're gonna lose. Chat's wrong a lot." / *(after the Shatter, off-camera)* "...Turn it off. Rotom. Turn it *off*."
- **Motivation:** Stay loved.
- **Secret:** **He doesn't hold the Zap Plate.** It sits in Meridian Spire's Plate Vault. Rook is a contractual figurehead whose family's debts Meridian paid off.
- **Plot role:** His city is where the Shatter happens. Dex, the soda-seller kid the PC met earlier, is one of the twelve Fixed.
- **Arc:** The Shatter breaks him open. In Act III he quietly visits the glass victims every night. In Act IV he leaks raw Spire security footage of Sable entering with a Meridian keycard. In Act V he cuts Lumen's grid from the arena feed during the hijack, starving the Engine and blacking out his own city. "First time Lumen's been dark in ten years. Kinda pretty."
- **Ace:** **Rotom** (his camera drone, in a battle form); later **Toxtricity** (punk idol), **Luxray**, **Electivire**.

### 5. Sahar Ostrand — Ground — Duneholt — `LEADER_SAHAR` — `:DESERT`
- **58.** Archaeologist-Warden in a sand-colored keffiyeh and wire spectacles. She has a dry cough from forty years in the dunes.
- **Personality:** Measured and patient. A teacher at heart, with very dry humor.
- **Voice:** "The desert keeps everything. It just doesn't keep it where you left it." / "I buried the truth once because I was told to. The sand dug it up. I'd rather not argue with sand twice."
- **Motivation:** Duneholt's aquifer is collapsing under Meridian's deep drills, which Ossaria's **Prince-Elector Idris Kassan** licensed without asking her. She also runs the **Dig Lab**, the game's fossil-revival service.
- **Secret:** In AF 281 she uncovered the **Aurel murals** beneath the Old Caravanserai, reported them to Valen, and sealed them on his order.
- **Plot role:** First concrete Prismfall clue. She gives the PC the **Duneholt Rubbing** (key item).
- **Arc:** Confesses after the gym. In Act IV she reads the Year of Two Weathers in Groudon's glyphs and knows where the war will end ("The sand remembers the sea. It doesn't want it back."), then leads the expedition into the Drowned Crown (Ch17). In Act V she testifies before the Accord Council.
- **Ace:** **Claydol** (an ancient effigy, the archaeologist's partner); also **Hippowdon**, **Krookodile**, **Sandaconda**.

### 6. Corvin Mott — Poison — Mirefen — `LEADER_CORVIN` — `:CORROSIVE_MIRE`
- **41.** Gaunt, in a long oilcloth coat and a plague-doctor half-mask he wears "for the smell, mostly". He runs the Mirefen Infirmary in Nadir's runoff marsh, where Zenith's Lattice slag drains into the Toxic Plate's mire. His apprentice **Wenlow** (17) is cheerful, clumsy and doomed: Wenlow is killed in the Sump Purge (Ch16), and the player can't prevent it.
- **Personality:** Sardonic, morbid and wickedly funny, and he hasn't slept properly since AF 288.
- **Voice:** "Everything's poison, dear. Dose makes the cure." / "I've a ward of forty patients slowly turning into garden furniture. Forgive me if I don't stand for the Sovereign's anthem." / *(battle)* "Don't worry. I'm a doctor. I know exactly how much this hurts."
- **Motivation:** Keep his Fixing patients alive.
- **Secret:** He treats Hollow wounded off the books, and he **treated the Mourner's burned hand** the night of the Lumen Shatter. He knows exactly who Rowan is.
- **Plot role:** The **Quiet Ward** shows the human cost of the Bleed. His ledger is where Juno finds the clue (J2).
- **Arc:** In Act III he is arrested under the Mandate for aiding terrorists, and an optional sidequest frees him (`CORVIN_FREED`). In Act IV he runs the field hospital in Cragholm. In Act V he privately treats Valen and is the one who tells the PC, "He has weeks. Maybe."
- **Ace:** **Toxapex** (the patient defender); also **Amoonguss**, **Drapion**, **Crobat**.

### 7. Brann Holloway — Fire — Cindervault — `LEADER_BRANN` — `:VOLCANIC`
- **63.** A giant with a braided beard, forge apron and hands like anvils. Valen's oldest friend and his AF 280 Festival final opponent.
- **Personality:** Booming, jovial and sentimental. He cries at weddings and tells terrible jokes.
- **Voice:** "Some things you forge to last. Some things you forge to *break* right — that's the harder craft." / "Valen and I nearly killed each other in the Festival of '80. Best day of my life." / *(Act IV)* "Aye. I reset the Crown's stone myself after the Fracture. It was smaller than it should've been. I never asked where the rest went."
- **Motivation:** Protect his friend and his forge.
- **Secret:** He is **"the Sovereign's Hand"**, the one Warden who knows about the Tuning and that Valen is dying.
- **Plot role:** The Caldera Crisis (Ch8). He is a commoner in a feudal kingdom: Ashkaar's Dragon-Lord, **Dominar Hrothgar Ashfall**, treats Cindervault's forges as his armory and demands the **Light Stone** (Reshiram) that Brann's guild has kept for centuries. Brann refuses. He confirms the truth about the Tuning when confronted in Act IV.
- **Arc:** He stands guard beside Valen through the Festival. After Valen dies, he forges the memorial from the Crown's broken setting.
- **Ace:** **Coalossal** (a walking forge); also **Arcanine** (loyalty), **Magmortar**, **Camerupt**.

### 8. Kaito Ren — Fighting — Ironreach — `LEADER_KAITO` — `:COLOSSEUM`
- **39.** Ex-Wardguard captain, close-cropped hair, a burn scar along his jaw, training wraps always on. Ironreach is Nadir's pit-fighting quarter, carved into the old Aurel-era mine shafts. Its Warden is whoever wins the **Iron Trial**, and he has held the seat for nine years. He is the only ex-Accord soldier Nadir trusts.
- **Personality:** Disciplined and laconic. He speaks in short declarative sentences and is fiercely honest about everything except one thing.
- **Voice:** "Stand up. Again." / "A fist is a promise. Don't make one you won't keep." / *(Act III, testimony)* "Marrowgate. Fifteen years ago. My orders. My unit. I sealed the gate. They were still knocking."
- **Motivation:** Atone.
- **Secret:** In AF 285 he led the Wardguard detachment that **sealed Marrowgate**, a Bleed-struck town, with Fixing survivors still inside, on Valen's order. His Lucario could feel them.
- **Plot role:** Gym 8, and his Colosseum hosts the Conclave attack.
- **Arc:** In Act III he testifies publicly about Marrowgate if the PC encourages him (`KAITO_TESTIFIED`), which shatters the Accord's credibility and makes him the Wardens' conscience. In Act V he is a Festival entrant (opponents per the Festival draw, NARRATIVE_KEYS §6) and fights with the PC in the hijack.
- **Ace:** **Lucario** ("It remembers for me."); also **Conkeldurr**, **Hawlucha**, **Machamp**.

### 9. Juno Hale — Grass — Verdance — `LEADER_JUNO` / `RIVAL_JUNO` — `:FLOWER_GARDEN`
See Rivals. She succeeds **Rowan Ashby** in Ch10. Her trial ends with bonding to the Meadow Plate at the foot of the Bride Tree. Gym 9 is **J3**. Her Warden-era ace is **Tsareena**, and the `:FLOWER_GARDEN` growth stages track her confidence.

### 10. Anja Sorrel — Ice — Rimeholt — `LEADER_ANJA` — `:FROZEN_LAKE`
- **46.** Ice-fisher matriarch with a Mamoswine-hide coat, rime in her eyebrows, and a pipe she never lights indoors.
- **Personality:** Blunt and pragmatic, with a sense of humor so dry it squeaks. She is contemptuous of southerners who moralize from warm houses.
- **Voice:** "You want me to choose between my principles and my grandchildren's toes? Easy choice. Toes." / "Ice remembers. Every crack. Every weight. You walk on my lake, it knows your name by spring." / *(after the Thaw)* "I read the numbers. I *read* them. And I signed anyway, because the heaters were warm."
- **Motivation:** Rimeholt's people survive an endless winter. Meridian's heat keeps children alive. She is the younger sister of **Thane Eirik Sorrel**, Isenmar's ruler, who signed the kingdom-wide heat contract. She signed Rimeholt's Lattice out of loyalty to him as much as to her people.
- **Secret:** She knew the Lattice readings showed the lake cracking and suppressed them.
- **Plot role:** The leading pro-Meridian Warden in Act III's political split.
- **Arc:** **The Thaw** (Ch11): the Lattice overdraws and the lake breaks, and part of the city sinks (`:FROZEN_LAKE` → `:WATER_SURFACE`). She breaks with Meridian publicly (or the PC exposes her, `ANJA_EXPOSED`). In Act IV she brings a column of Rimeholt's refugees east to Cragholm under the Ossarian bone-carters' banner, then goes to the front at Skaldfast and is taken prisoner by Ashkaar (`:war_prisoner`). In Act V she casts the deciding Conclave vote to strip Meridian of Festival security. The vote fails anyway, because Hollis has bought enough Wardens.
- **Ace:** **Mamoswine** (matriarch of the herd); also **Avalugg**, **Walrein**, **Weavile**.

### 11. Odessa Gale — Flying — Skyreach — `LEADER_ODESSA` — `:STORMFRONT`
- **27.** Aviator goggles, scarf, a scar through one eyebrow, and a laugh carried off by the wind. Captain of **the Gale Post**, the airship-and-wing courier guild based in Skyreach, Zenith's airship spire. Its mail runs through the permanent storm wall, the Stormfront, to every kingdom and the outer islands.
- **Personality:** Irreverent, quick, flirtatious, reckless and brave. She hates rules she didn't write.
- **Voice:** "Skyreach's got one law: the wind doesn't care. Everything else is negotiable." / "I've flown letters through three storms and a Bleed. You want me to hand them to Meridian because a clerk said 'please'?" / *(battle)* "Hold onto something. No, really."
- **Motivation:** Keep the post flying, and keep people *free*.
- **Secret:** She smuggles refugees past the quarantine through the Stormfront to the outer islands. She has carried Hollow messages. Her **dead-letter archive** holds undeliverable mail from ten years back, including letters from Morwen Vane to "I." (Ines) abroad.
- **Plot role:** K5. Larch broadcasts the Larch Papers through her relays.
- **Arc:** Meridian raids the Post in Act III. In Act IV she flies the PC over the siege lines in Ossaria to the Ashkaar Siege Camp (`:war_prisoner`). In Act V she airlifts civilians during the hijack. She is a Festival entrant (R16 vs Valen, and loses with style).
- **Ace:** **Corviknight** (the air-taxi); also **Pelipper** (the old mail carrier), **Swanna**, **Noivern**.

### 12. Ilsa Marr — Psychic — Lucent — `LEADER_ILSA` — `:MINDSCAPE`
- **31.** Provost of the Lucent Athenaeum. Silver-blonde hair pinned with a pencil, high-collared academic robes, noise-cancelling earmuffs she wears around anyone emotional.
- **Personality:** Cool, precise and unnervingly perceptive. She can read surface thoughts involuntarily and finds crowds unbearable. She is wry, lonely and secretly kind.
- **Voice:** "You're thinking very loudly. Please stop." / "The truth is a weapon. I've kept it sheathed for ten years. Don't mistake that for mercy." / *(Act V, to Valen)* "You chose a country over a daughter. Fine. Then *save the country*, Father. Don't make a child pay for it."
- **Motivation:** Know everything; risk nothing.
- **Secret:** She is **Valen's estranged daughter**. She has read the Tuning, his dying and his plan for "the child" out of his mind and kept silent.
- **Plot role:** Guides the PC through the Mindscape (Ch13), where they recover the AF 290 memory. She hosts Rowan's tribunal at the Athenaeum.
- **Arc:** In Act IV she sends the PC the **Concordance's Secret Articles**. In Act V, if the player completes her sidequest ("Little Owl"), she reconciles with Valen before the final (`ILSA_RECONCILED`). In the finale she holds the panicking crowd's minds calm and gives Arceus's voice to everyone in the arena.
- **Ace:** **Hatterene** (it attacks emotions that are too loud); also **Reuniclus**, **Espeon**, **Bronzong**.

### 13. Bastian Ore — Rock — Cragholm — `LEADER_BASTIAN` — `:CRYSTAL_CAVERN`
- **74.** The oldest Warden. Stooped, with a miner's lamp on his hat, a clay pipe and enormous hands. He is half-deaf and pretends to be fully deaf when it suits him.
- **Personality:** Folksy, stubborn and kind. He tells long stories that turn out to be important.
- **Voice:** "Rock's patient. Rock'll wait for you to make a mistake for a thousand years. I'm only seventy-four, so I'll wait for about ten minutes." / "I've seen three Festivals, two Sovereigns and one crown break. Sit down, I'm telling you about the crown."
- **Motivation:** Protect the people under his mountain.
- **Secret:** He shelters fugitives in Cragholm's deep seams (Larch, Hollow, Rimeholt refugees). At the AF 290 Fracture he **saw Meridian technicians at the Crown's mount** and kept silent for ten years after the purge.
- **Plot role:** The first eyewitness account of the Fracture (Ch14).
- **Arc:** Defends Cragholm during the Meridian raid. In Act V he is too old to compete but stands at the ceremony carrying the Stone Plate. In Homecoming he dies peacefully in the epilogue, "the first Warden in three hundred years to die with nothing in his keeping".
- **Ace:** **Gigalith** (crystal); also **Carbink**, **Rhyperior**, **Golem**, and his old **Aerodactyl "Amber"**, his Mega (SPINE Rev 21). He keeps Brann's odd ring under his mountain for ten years and gives it to the PC (the Ring-Day, Ch14).

### 14. Ysolde Ashgrave — Ghost — Gravenmoor — `LEADER_YSOLDE` — `:HOLLOW_CATHEDRAL`
- **37.** Pale, in layered black lace and a veil, with a lantern always lit. She speaks very softly. She was **Morwen Vane's apprentice and partner**, and Kestrel's step-parent in all but law.
- **Personality:** Melancholy, tender and quietly unbreakable. She talks to the dead as easily as to the living.
- **Voice:** "The dead aren't gone here. They're just very bad at conversation." / "Kestrel thinks I stole her seat. I *kept* it — from the man Valen wanted in it. There's a difference, but you can't explain it to a grieving boy." / *(K6 aftermath)* "She made me swear. 'When he's ready.' I don't think anyone is ever ready. I'm sorry I waited."
- **Motivation:** Keep Morwen's promise and win back Morwen's son.
- **Secret:** She holds Morwen's sealed letter to Kestrel. She knows Morwen's echo still lingers in the Hollow Cathedral.
- **Plot role:** Gym 14, K6, and the Fracture echo.
- **Arc:** At the Festival she watches over Kestrel. If `KESTREL_YSOLDE_RECONCILED`, she offers him the Ghost seat in the epilogue.
- **Ace:** **Chandelure** (the cathedral candles); also **Gengar**, **Dusknoir**, **Sableye**. Morwen's **Mismagius** lives with her and goes to Kestrel after K6.

### 15. Magnus Strade — Steel — Cogsworth — `LEADER_MAGNUS` — `:FACTORY`
- **52.** Immaculate grey waistcoat, pocket watch, prosthetic left hand he built himself. A Meridian board member and Cogsworth's Warden.
- **Personality:** Calm, exact and unflappable. He holds a utilitarian code he will not break: engineering ethics as religion.
- **Voice:** "Faith gave us three hundred years of the Bleed. Engineering will give us the next three hundred without it." / "I don't build weapons. I build tolerances." / *(Act V, if `MAGNUS_KEPT_FAITH`)* "No machine I have built will kill a child. Governor's off. Go."
- **Motivation:** Replace miracles with machines.
- **Secret:** **He built the Arbiter Engine's core.** He believed it was a "Plate stabilizer", but by Act IV he knows exactly what it does.
- **Plot role:** Gym 15. The PC finds the Arbiter blueprints in his foundry (`:FACTORY` → `:SCRAPYARD` in the infiltration battle).
- **Arc:** The PC chooses to **expose him** to the Conclave (`MAGNUS_EXPOSED`: he is arrested, and Meridian loses a board vote) or to **appeal to his conscience** (`MAGNUS_KEPT_FAITH`: he stays in place and sabotages the Engine's safety governor at the finale, which weakens Voss's binding).
- **Ace:** **Metagross** (the supercomputer); also **Klinklang** (his first machine), **Bisharp**, **Excadrill**.

### 16. Nyx Calloway — Dark — Underveil — `LEADER_NYX` — `:NEW_MOON`
- **33.** Information broker and undercity queen. Velvet and smoke, a crescent-moon earring, eyes that are always amused.
- **Personality:** Silky, theatrical and dangerous. She treats secrets as currency and mercy as an expensive luxury she occasionally buys.
- **Voice:** "Underveil isn't on the Accord's maps, sweetheart. That's the *point* of Underveil." / "Everything has a price. Yours just went up." / *(Ch17)* "Oh. Oh, darling. You're the missing piece."
- **Motivation:** Survive, profit, and keep a promise her family made 300 years ago that she has privately decided is stupid.
- **Secret:** Her house descends from Princess Maren's guard. They are the **Keepers of the Drowned Truth** and have always known the real Prismfall. She **sold Voss the location of the Gilded Chain's remains** two years ago.
- **Plot role:** Gym 16. Underveil is Nadir's heart, built in the upper towers of drowned Aurelia beneath Zenith. Zenith claims sovereignty, but Nadir has no recognized government, so Nyx is its de facto queen and the Sump Barons pay her tithes. She guides the PC into drowned Aurelia.
- **Arc:** Offers the PC a bargain: their secret for the Engine schematics (`NYX_BARGAIN_TAKEN`). After the Sump Purge she declares Nadir independent of Zenith (Ch17). In Act V she cuts Meridian's comms during the hijack. She is a Festival entrant (opponents per the Festival draw).
- **Ace:** **Zoroark** (illusion); also **Honchkrow**, **Grimmsnarl**, **Weavile**.

### 17. Celestine Aubade — Fairy — Gloaming — `LEADER_CELESTINE` — `:FAIRY_TALE`
- **Looks 20, is 61.** Gloaming's dusk Imprint slows aging. Gown of moth-silk and twilight, flowers that open only at dusk woven in her hair, barefoot.
- **Personality:** Whimsical and riddling, speaking in fairy-tale cadence. Gloaming's oath-binding means **she cannot lie**, so she has become an artist of the true-but-misleading.
- **Voice:** "Once upon a time — which is the only time there ever is, here —" / "I've been waiting for you for forty years, little colorless thing. You took the long way. Everyone does." / "I cannot lie. I can, however, *phrase*."
- **Motivation:** See the Hymn fulfilled before she dies.
- **Team note (SPINE Rev 23):** her Mimikyu holds the **Mimikium Z**, tuned by her dusk-chapels' singing ("one true thing in a borrowed costume"). It's a Z-move, not a Mega; her ace stays Sylveon.
- **Secret:** She keeps the **Hymn of Return**, the Accord's original liturgy, suppressed since AF 140. It says the Plates must go home when "one of no color walks the eighteen roads".
- **Plot role:** Gym 17 and K7. Gives the PC the Hymn.
- **Legendary tie:** Gloaming's Great Tree holds the Pixie Plate in its roots. The Ogre's masks in Elowen's folklore (Ogerpon) were carved from its fallen bark. Celestine is the one person who has always told the true version of the Ogre story, in rhyme, to anyone who'd listen.
- **Arc:** At the Festival she is an entrant (opponents per the Festival draw). She voices Princess Maren in Dorian's Night of Masques. In the finale she sings the Hymn as the chains break. In Homecoming, her dusk ends with her Imprint. She sees her first full night sky in sixty years and ages gracefully in the epilogue.
- **Ace:** **Sylveon** (ribbons that read intent: a creature of bonds for a woman bound by oaths); also **Mimikyu**, **Togekiss**, **Alcremie**.

### 18. Sigrun Ashfall — Dragon — Wyrmrest — `LEADER_SIGRUN` — `:DRAGONS_DEN`
- **29.** Tall, with a burn-scarred left cheek and neck, a braided crown of red hair and dragonhide armor. She is the strongest Warden and **Valen's protégé**. She is also the **Dominar's daughter**. She renounced her claim to the Ashkaar throne to take the Warden's oath, and her father has never forgiven her or the Accord.
- **Personality:** Fierce, proud, blunt and honorable. She has no patience for lies, which makes her guilt unbearable.
- **Voice:** "Wyrmrest is the last gate. Dragons don't let anything through they haven't weighed." / "He trained me to be his successor. Then he told me I'd never survive the Crown, and I was *relieved*. Do you understand? Relieved. And then he went looking for *you*."
- **Motivation:** Honor, and atonement for her relief.
- **Secret:** She knows Valen's plan for the PC, and she let it happen because it meant the Crown wouldn't be hers.
- **Plot role:** Gym 18 makes the PC prove they choose the Festival with full knowledge. She refuses to give the badge until the PC says aloud what they intend.
- **Arc:** In Ch19 she defies her father, whose legions are at war in Ossaria's sands and who means to march on Zenith afterward, by keeping Wyrmrest's pass open to the PC. Then she flies the PC to the Glass Dunes. Reshiram wakes for the PC's spoken truth during her trial. At the Festival she fights her way to the semifinal (opponents per the draw). She loses the semifinal to Valen after entering to win the Crown herself and spare the PC. In the hijack, her dragons hold the sky over Crownhaven against Meridian's airships, and if `DOMINAR_SWAYED`, her father's legions fly with her.
- **Ace:** **Salamence** (it dreamed of wings until it grew them); also **Haxorus**, **Flygon**, **Kommo-o**.

---

## IMPORTANT SIDE CHARACTERS

- **Hesper Vane** (78): Kestrel's grandmother and keeper of the Ferrow's Landing lighthouse. Bitter, sharp-tongued, and secretly sends the PC care packages after she learns who they are (Act IV). Gives Kestrel the Honedge.
- **Teo Reyes** (19): Marisol's brother and Ebbmouth Hollow cell leader (`HOLLOW_TEO`). Idealistic, angry and funny. His survival at Ironreach is a player choice. If he lives, he becomes the Lantern Hollow's youngest organizer.
- **Mara Thistlewood "Thistle"** (40): Hollow Pallbearer (`HOLLOW_THISTLE`), a former Briarwick weaver whose village of Lowmarsh was Fixed. She cuts the Lantern Theatre's curtain ropes during the Mourner's hijack (Ch2) and is the PC's first admin battle at Briarwick's pylon (Ch3). Fierce and grieving, and careful: "I know where a thread will fall." She is captured at Lumen and returns in Act IV on the PC's side.
- **Sable / Sabine Kroll** (35): the Hollow's "Hammer" (`HOLLOW_SABLE`, later `MERIDIAN_KROLL`), secretly a Meridian Special Accounts operative. Cold, cheerful and professional. She caused the Lumen Shatter and the Ironreach attack. Exposed in Ch13 and fought again in Act V.
- **Dr. Percival Quent** (44): Meridian Head of R&D and lead on the Arbiter Project (`MERIDIAN_QUENT`). Larch's former protégé. Giggly, brilliant and morally weightless. Fought in Ch8, Ch16 and the Festival tag battle. Post-game villain hook.
- **Director Helene Marchetti** (50): Meridian Security Directorate, the Mandate's enforcer (`MERIDIAN_MARCHETTI`). Ex-Wardguard. Cold, loyal and competent, with no illusions. Fought in Ch12, Ch14 and the Festival tag battle. If `MARCHETTI_TURNED` (the PC shows her Kroll's file), she stands down in the hijack.
- **Chancellor Ambrose Hollis** (61): the Accord's chief administrator, a smooth bureaucrat who is quietly on Meridian's payroll. He passes the Mandate and gives Meridian Festival security. He is arrested in the epilogue.
- **Elin Ashby** (Fixed, AF 288): Rowan's wife and Juno's aunt, the **Bride Tree** in Verdance's Heartgarden. She wakes in Homecoming.
- **Dex** (11): street kid who sells Fizzbolt soda outside Meridian Spire in Lumen. Talkative and lovely. Fixed in the Lowlight Shatter mid-wave. His glass figure becomes a shrine. He wakes in Homecoming and finishes the sentence he was saying.
- **Morwen Vane** (deceased AF 296): former Ghost Warden, Kestrel's mother. She appears only as an echo (Ch15) and in her letter (Festival). Her echo's line to the PC: "Little one. You came back. I told her not to let you."
- **Ines** (deceased): the PC's mother. She appears in the Ch13 memory, singing in the Choir.
- **Hierophant Maud Ellery** (68): head of the Prism Choir, which performs the Tuning. A true believer who learns in Act V that the hymn she sings is half of a song.
- **Pip Ore** (14): Bastian's granddaughter and his ears. A fast-talking lamp-runner who guides the PC through the deep seams.

## KINGDOM RULERS & POLITICAL FIGURES

The Wardens answer to the Accord, but their cities sit inside kingdoms whose rulers resent that. Each ruler wants something from the Plates in their land.
- **Queen Maelis Thorne of Elowen** (82): an ancient, fairy-tale-cunning monarch who holds court in Briar Keep, the castle crowning Verdance. Her doctrine is "the Plates are the Crown's by right of soil." She claims the Meadow Plate when Rowan falls (Ch10) and later signs a "Forest Compact" with Meridian. Her heir **Prince Caedmon** (34) is a smiling modernizer and quietly Meridian's man. Maelis outlives her usefulness to him in Act V.
- **Archseer Imre Dask and the Veiled Synod of Antumbra**: Antumbra's rulers are a theocratic council of seers (Lucent) and lantern-priests (Gravenmoor) who mediate with Giratina. Dask (60s, two different-colored eyes, speaks in mirrored sentences) fears the Bleed is thinning the Glass. He refuses to open the Veil Gate for this Festival ("I won't open a door in a wall that's falling down"). On the Ruin Route, Dask is the Synod's champion who claims the Renegade in the QF: "Behind, welcome. Welcome, behind." (Team: Psychic/Ghost on `:INVERSE`.)
- **Thane Eirik Sorrel of Isenmar** (52): Anja's older brother. Practical and proud, he is drowning in debt to Meridian for heat. He declares martial law after the Thaw (Ch11) and sends Isenmar's refugees south into Elowen, which causes a border crisis. Then he takes his host east over the Mast Glacier to Skaldfast and the war in Ossaria's sands.
- **Dominar Hrothgar Ashfall of Ashkaar** (64): Dragon-Lord and Sigrun's father. A warlord-king who believes "dragons bow to no Accord." He threatens war after the Cindervault caldera crisis (Ch8), on Isenmar first and Zenith second, and from Act III he masses his legions in the Ashkaar Siege Camp on Ossaria's western dunes. He can be swayed (`DOMINAR_SWAYED`) to fly for Crownhaven instead of marching across Elowen against Zenith.
- **Prince-Elector Idris Kassan of Ossaria** (45): elected for life by the caravan houses. Charming and venal, he sells Meridian drilling and mining rights (Duneholt's aquifer, Cragholm's seams) and pays the Bone Sands' fossil-hunters to look the other way. When the war comes he declares Ossaria neutral and rents it a battlefield: **the Elector's Lease** leases the western dunes to both crowns and to Meridian at once. "The Bone Sands have buried every army that ever marched into them. I only charge for the plot." The caravan houses that elected him for life can't unseat him, so they stop listening to him (14_WAR_AND_BLESSING Part B).
- **The Zenith Council**: Zenith's governing council of founding houses, chaired by **Voss**. Notables include **Councillor Renata Sallow** (old-money airship house, Voss's rival, who becomes a reluctant ally in Act IV) and **Magnus Strade** (Cogsworth).
- **The Sump Barons of Nadir**: the chem-lords and pit-bosses who actually run the City Below, chief among them **Mother Gutter** (an ancient sludge-baron with a Muk the size of a cart). They pay tithes to Nyx and hate Zenith. They are also the Hollow's most reliable source of recruits and money.
- **Envoy Delphine Okoro of the Concert of Regions**: the neighboring realms across the strait. She attends the Festival to decide whether the quarantine lifts or becomes **Severance**, meaning permanent abandonment. She can be persuaded (`ENVOY_PERSUADED`), which affects the epilogue's international outcome.
- **Chancellor Ambrose Hollis**: see above. He is the hinge between the kingdoms' grievances and Meridian's money.
- **Vesper Lindqvist** (24): cantor of **the Eevee Octave**, eight Glassfall orphans raised by the Prism Choir and sent, once grown, to live beside a Plate each, one per kingdom (Carol stays in Crownhaven). Her own Eevee, **Amen**, never decided. Gentle and devout, and a little in love with the idea of the Festival. In Ch2 she asks the PC to look in on the singers; in Ch20 she hosts the gauntlet that thanks and tests the PC (SPINE Rev 19, `design/EEVEE_OCTAVE.md`).
  - **The singers** (gym order of first meeting): **Lyra** (Elowen, Leafeon "Moss"; hums at plants, stubborn about her patience), **Aria** (Isenmar, Vaporeon "Brine"; loud, swims in ice water at dawn), **Cadence** (Zenith, Jolteon "Snare"; fast-talking drummer on Meridian night shifts), **Sona** (Ossaria, Espeon "Noon"; answers before you ask, keeps a buried sun temple's noon bell), **Noct** (Nadir, Umbreon "Wick"; the marsh's lamplighter, few words, guards the lamp-runner kids), **Forte** (Ashkaar, Flareon "Bellows"; loud and brave, wants the Legion to stop pitying her), **Lento** (Antumbra, Glaceon "Hush"; says everything twice, once for her reflection) and **Carol** (Crownhaven, Sylveon "Ribbon"; the storyteller who never leaves, met last).

## SISTER-GAME CAMEOS (optional sidequests, Revision 4)

Lin, Amaria, Shelly, Alexandra, Venam, Shiv, Garret, Melia and Titania (and Nova, on the Ruin Route only) appear in small optional sidequests across the kingdoms, as Rejuvenation handles Reborn's Aya and Adrienn. **None appear in the Festival or the finale. **Revision 5:** every Festival opponent is a character the player has met at least twice by Act IV.** Antumbra's Glass is leaking, and that is the in-universe reason they're here. The full roster is in **`design/CAMEOS.md`**.

## HISTORICAL FIGURES

- **King Aurelius Aurel, "the Gilded King"** (d. AF 0; Ruin Route hijacker `[GILDED_AURELIUS,Aurelius]`, Lv 100 on `:PRISM_ARENA` running Inverse; art: Graphics/Trainers/GILDED_AURELIUS, Portraits/AURELIUS_*, EBDX/VS/AURELIUS): First Sovereign of drowned Aurelia and architect of the Gilded Chain. Imperious, proud and effortlessly theatrical: he tried to collar Arceus not out of pious terror but out of royal fury that heaven let blight touch *his* kingdom. Frozen behind Antumbra's Glass at the instant of the Calling, he survives on the Ruin Route as a grinning sovereign who despises counterfeits (his kneeling descendant Voss first of all) and respects only a mortal who looks a god in the eye without flinching. He calls the PC "mongrel" until Gilt falls, and never again. He never says Fate's names; his words are "my treasury", "the Chain", "counterfeit", "know your station". (Gemini rework 2026-11-23.)
- **Princess, later Sovereign, Maren Aurel**, called "Maren Ilse" after renouncing her house (AF −19 to 61): founded the Accord and set the Legend shard in the Crown.
- **Ansel Crewe** (executed AF 52): playwright of "The Gilded King".
- **Sovereign Adela Wyndham** (d. AF 270): Valen's predecessor. She died months after her last Tuning.
