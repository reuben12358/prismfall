# Story Bible 07: Act IV — The Drowned Crown (Ch14–17, Gyms 13–16)

> **Tone:** Desolation. Truth arrives in layers, and every layer costs something. A massacre the player can't stop, a rival's world shattering, a beloved mentor's complicity, a villain who is *reasonable*. Keep one warm scene per chapter (a meal, a joke, a Pokémon moment) so the dark has contrast.
> Conventions as in 04. Map names per WORLD.md (segments 12–15). From the start of Act IV, revisited early maps use **encounter version 1 (Bleed-spread)**.
> **If Rowan drowned at the Fault (`:ch13_fault` = marchetti):** every Rowan line in Acts IV–V goes to the Lantern Hollow's leader instead: **Teo** if `TEO_SAVED`, otherwise **Thistle** with **Wick**. Juno's scenes reference her uncle's death.
> **Revision 6:** this act carries beats of the Ashkaar–Isenmar War and the Blessing. See `14_WAR_AND_BLESSING.md` (timeline table) for the inserts per chapter; that file wins on conflicts.


**Act-opening state (after the Fault):**
- The Bleed has leapt forward everywhere. Briarwick's Glasswood has reached the looms. The Lowlight's glass has spread a block. Saltmere, never once touched by Bleed, has a glass puddle on the promenade, and Dorian has roped it off as "our first miracle, darlings".
- News screens show the **north coast**: the sea pulled back from Zenith's cliffs, and drowned Aurelia's golden spires standing in the mud below Underveil.
- The Concert of Regions announces it will decide on **Severance** at the Festival.

---

## CHAPTER 14 — "The Deep Seams" (R25 → R26 → Geode Hollow → Cragholm, Gym 13)

**Location:** R25 (`:INVERSE`, Antumbra exit), R26 (Waterfall, a mirror exit into Ossaria), **Geode Hollow** (`:CRYSTAL_CAVERN`), **Dreaming Quarter** (768, `:BLEED`: a mining street where the sleeping Fixed's dreams play as mirages), **Cragholm** (Ossaria), the **deep seams**.

**Arrival: Ossaria, second visit (escalation).**
- Cragholm is a canyon wall of lamplit galleries and lift-cages. **Prince-Elector Kassan** has sold its seams to Meridian. Linesmen and Directorate guards stand at the main lifts, and Meridian's new **Lattice-drill** chews into the Stone Plate's crystal halls.
- The miners are sullen and terrified. Many of them are refugees: Isenmar families from the Thaw, and Nadir families fleeing Mandate raids.
- Warden **Bastian Ore** (74, a miner's lamp on his hat, pretending to be deaf to Directorate questions) greets the PC like a grandson: "Ilsa sent you? Sit down, I'm telling you about the crown."
- **Pip Ore** (14), his granddaughter, runs lamp-errands and is the fastest talker in Ossaria. She's the PC's guide through the deep seams.

**The deep seams (hidden-refuge sequence).** Below Meridian's level, Bastian shelters everyone the Accord and Meridian would rather didn't exist:
- **Professor Larch**, smuggled in by Odessa.
- Rimeholt refugees.
- Lantern Hollow faithful: **Rowan**, gaunt (or their new leader, if he drowned), with **Wick** and **Thistle**.
- **Corvin's field hospital**, if `CORVIN_FREED`. That flag comes from the Act III side quest "The Doctor's Cell", available Ch11–13: Corvin was arrested under the Mandate for treating Hollow wounded, and the PC can free him from a Directorate holding barge on Lake Sallow. If he wasn't freed, the hospital is run by a frightened **Wenlow** alone, and Corvin's absence is felt.

**Anja** arrives on the second day with a column of Rimeholt refugees, frostbitten and furious at herself. If she was exposed in Ch11 she won't meet the PC's eyes, and if she confessed she shakes their hand. This is her second encounter before the Festival.

Warm scene: a communal meal of date-bread and miners' stew. If Rowan lives, he and Juno (if she's visited) don't speak, but they sit at the same table. If he drowned, Juno sits with Thistle, who was with him at the end.

**Bastian's account.**
> *"I've seen three Festivals, two Sovereigns and one crown break. AF 290. I was carrying the Stone Plate in the procession. I was nearest the Choir loft. There was brass behind the loft that had no business in a church, and men in white coats with little gold suns on their pockets, watching dials. When the Crown cracked, the dials jumped. They weren't surprised. They were *pleased*. Then Valen said 'find the child', and Morwen Vane threw herself over a little thing in a Choir ribbon, and the next week Morwen was ruined and nobody ever asked me what I saw. I never told. I was afraid. I'm still afraid. I'm telling you anyway."*

**Gym 13 (`:CRYSTAL_CAVERN`).** Thematic note: *light through crystal; darken it and the whole field turns.* (`:CRYSTAL_CAVERN` → `:DARK_CRYSTAL`.) Bastian: "Rock's patient. Rock'll wait a thousand years. I'm only seventy-four, so I'll wait about ten minutes." His ace is **Gigalith**.

**Larch and the badge case (revelation).** Larch takes the PC's **Meridian badge case** apart on a miner's bench. Inside the lining is a sliver of Lattice-glass and a transmitter.
- "Every badge you've won, it's recorded your — whatever it is in you — resonating with that Plate. And it's been sending it to Meridian. Voss isn't watching you. He's **tuning** you."
- **CHOICE `:ch14_telemetry`** (major; it feeds the endings):
  - **Destroy it.** Voss loses the stream. In the finale the Engine is under-calibrated, but Voss knows immediately and moves faster (Directorate pressure in Ch16–17).
  - **Feed it false data** (Larch's plan, `TELEMETRY_SABOTAGED`). The PC keeps the case and Larch rigs it to send corrupted resonance. Voss's Engine is *miscalibrated* in the finale, which is the strongest single weakening. It's risky: every remaining badge triggers a tense "did he notice?" beat.
  - **Leave it.** It keeps working. This is the road to the Bad ending if other weak points also fail.
- **Game over `GO_WILLING` "Willing".** Trigger: Dr. Quent arrives with the raid and offers to "remove the faulty device painlessly, and give you a full Fellowship medical". The PC agrees. Foreshadowing: Larch's flat instruction a scene earlier, "Never, ever let them examine you." *Epitaph: "The exam was painless, as promised. You've been asleep since. Meridian sends flowers."*

**The raid.**
1. **Marchetti's** Directorate raids the seams, hunting Larch and Rowan.
2. **Admin battle: Marchetti** in the Darkglass gallery (`:DARK_CRYSTAL` after the lamps are shot out).
3. **Thistle defects openly to the PC's side**, earlier and warmer at high Hollow Standing. Her Pokémon hold the lift-shaft while refugees escape.
4. **CHOICE `:ch14_marchetti`:** after her defeat, the PC can show Marchetti the **Splitter Casing** or the Ironreach comm-device: "Your own Special Accounts bombed Skyreach." With either item, `MARCHETTI_TURNED` becomes possible. She doesn't turn now. She just goes very still, and in the Festival hijack she stands down. Without the evidence, she remains loyal.

**Transit (segment 13), Ossaria: Duneholt Undersands and Groudon.**
- On the road to Gravenmoor, the PC passes back through Duneholt. The aquifer has *gone*, the great well is a dry shaft, and Meridian's deep drill has punched through into something hot.
- **Duneholt Undersands** (783, `:DESERT`) opens.
- **Boss battle: Groudon** (multi-bar), woken by the drills, in a chamber of Unown glyphs that record Theodric's "Year of Two Weathers".
- Sahar is with the PC, and she reads the glyphs mid-fight (story text between bars): *"The King woke the red one and the blue one to remake the land. When they would not obey, he turned his eyes to heaven."*
- After the battle, Groudon sinks back into the earth. The aquifer starts, very slowly, to refill. This is the first good news in an act.
- **Stonesleep** (788): the fossil beds exposed by the collapse. Rare fossils go to the Dig Lab.

**Cliffhanger:** At the Antumbra border on R28, Kestrel's Meridian airship passes overhead toward Gravenmoor. Pip: "That's a sponsor ship. Who'd sponsor a *graveyard*?"

---

## CHAPTER 15 — "The Hollow Cathedral" (R27 → R28 → Gravenmoor, Gym 14; K6; Vane Hall; Giratina)

**Location:** R27 (`:MOUNTAIN`), R28 (Antumbra moors, fog), **Gravenmoor** (Antumbra, `:HOLLOW_CATHEDRAL`), **Vane Hall** (haunted house), the **Lantern Hospice**, the barrows, then on the way out **Barrow of the Wardens** and **Giratina's Reverse Depths** (806, `:INVERSE`), **The Hush** (808).

**Arrival: Antumbra, second visit.** Gravenmoor is fog, barrows and lanterns. The Spooky Plate makes the dead *linger as echoes*: a woman sweeping a step that isn't there, two children playing a game that ended in AF 211.
- **Archseer Dask** has come to Gravenmoor himself (his second encounter, needed for the Ruin Route): "The echoes are louder. Louder, the echoes. Something behind the Glass is listening back."
- The Veiled Synod's lantern-priests are frightened. Since the Fault, the echoes have been getting **louder**, and some have started to notice the living.
- Warden **Ysolde Ashgrave**, lace and veil, lantern always lit, greets the PC softly: "The dead aren't gone here. They're just very bad at conversation." She knows who the PC is. She has been waiting for them, and for Kestrel.

**Vane Hall (haunted house set piece, the sad one).**
- Kestrel has arrived on Meridian's ship and gone straight up the hill to his childhood home. The PC follows.
- Vane Hall is dust-sheeted and haunted. The echoes are of *his family*: his grandmother younger and laughing, **Morwen** reading to a six-year-old Kestrel, Morwen at a desk writing a letter and crying.
- A puzzle path (World/puzzle team) through rooms that replay the night of AF 290 from the household's side: a servant's echo saying "the Warden's not back yet", a clock stopped at 11:40.
- Kestrel walks through it like a ghost himself. Short lines only. "That's my room. That's — don't touch that."

**Gym 14 (`:HOLLOW_CATHEDRAL`).** Thematic note: *echoes of earlier turns replay; the dead fight beside the living.* Ysolde: "Mind the candles. Some of them are people." Her ace is **Chandelure**.

**The Cathedral echo (the central revelation of the game).**
1. Kestrel's **Resonance Gauntlet** (Meridian-built) can amplify the Spooky Plate's echoes. Voss told him the full truth of AF 290 is "recorded in the Cathedral". He means to force the Plate to replay it.
2. Ysolde begs him not to: "Not like this. She made me swear — when you were ready—"
3. He does it anyway. **The Hollow Cathedral replays AF 290 in full**, through **Morwen's eyes**. The PC sees it whether or not they chose "Not yet" in Ch13. If they did, this is their first time, and it's harder.
   - The Crownhaven arena, bells, the Choir. **Ines** singing.
   - Behind the loft: brass machines, sunburst plates, and a young, eager **Aurelian Voss** in a white coat, watching the dials.
   - The Tuning begins. The Crown flares on Valen. A sound like a bell breaking.
   - A splinter of colorless light flies from the Crown, straight into the chest of a five-year-old in a Choir ribbon.
   - Morwen runs. She throws herself over the child as the **Glassfall** sweeps the lower stands, and forty people turn to glass around them.
   - Valen, through the light: "**Find the child.** Whatever it costs. *Find the child.*"
   - Morwen, hiding the child in a vestry, to Ines: "Take them. Edda's boat is at the Landing at midnight. I'll carry the name. Go."
   - Morwen's Mismagius gently closes the child's memory like a curtain.
   - The echo ends with Morwen alone in the vestry, kneeling, saying to no one: "Kestrel. I'm sorry."
4. Silence. Then Morwen's echo turns, impossibly, and looks at the PC across ten years:
   > *"Little one. You came back. I told her not to let you."*
   It fades.

**K6 (raw, furious).**
- Kestrel turns on the PC:
  > *"My whole life for you. Do you know what they called me in school? The Glassfall boy. My grandmother spat on her grave. And she was saving YOU."*
- If `:ch12_letter` was "sent to Kestrel": he opens with "You sent me her *letter*, and you still came here."
- The battle is **K6**. His Gauntlet surges with the Cathedral's grief. Mid-battle the field flickers to `:BLEED` for a turn, the Gauntlet overloading.
- **After K6: the PC speaks (authored line, CHOICE `:ch15_kestrel`).**
  1. **"I'm sorry. I didn't know. I'd give it back if I could."** Kind: Kestrel's Bond goes up a lot, delayed. He can't accept it now.
  2. **"I was five. She chose. Don't you dare make her choice my crime."** Blunt: his Bond drops now, but it unlocks his Redeemed path in K8, because he respects being fought back.
  3. **"...Your mother saved my life. I'm going to make it worth it."** The Resolve option: his Bond goes up, and Resonance leans Harmony.
- Kestrel leaves without a word. **Ysolde** follows him to the moor's edge and gives him **Morwen's Mismagius** and **Morwen's sealed letter**. He takes the Mismagius and refuses the letter. Ysolde keeps it for him (it returns in the Festival SF).

**Edda Morrow at Morwen's grave.** In the barrows below the Lantern Hospice, the PC finds **Captain Edda Morrow** laying kelp-flowers on a plain stone marked *M.V.*
> *"I took you out on the night ferry. Brought you back on the last one. Tide's got a sense of humour."* A beat. *"She paid me in her Warden's ring. I never sold it."*

She gives the PC the ring (Key Item **Morwen's Ring**; plot-relevant in Act V for Kestrel).

**Game over `GO_ECHO` "Echo".** In the Cathedral, after the replay, an echo of **Ines** keeps singing in the Choir loft. A prompt: "Stay and listen?" Choosing to stay *three times* triggers it. Ysolde warns that "echoes are a door that only opens one way", and the PC's own hand turns translucent on the second "stay". *Epitaph: "You stayed for the song. Gravenmoor has one more echo now. It sings harmony."*

**Transit (segment 14), Giratina's Reverse Depths.**
- Leaving Gravenmoor through the **Barrow of the Wardens**, where generations of Wardens are buried with replica Plates, the PC finds a barrow-door that opens *downward into the sky*: the **Reverse Depths** (806, `:INVERSE`).
- **Giratina** waits there. The Fault and the Gauntlet's abuse of the Spooky Plate have torn the Glass, and Giratina is furious and wounded.
- **Boss battle: Giratina** (multi-bar; Altered, then Origin on the last bar).
- After the fight it doesn't flee. It *looks* at the PC the way Kyogre did. Story text: *it knows what you carry. It has been guarding the hole your god left for three hundred years.* It lets the PC pass and closes the tear behind them.
- The Glass has been leaking since the Fault, and Giratina's wound is why visitors from other worlds keep slipping into Velmora (the cameo sidequests, `design/CAMEOS.md`). Post-game: the Distortion Core.
- **Ruin Route trigger** (only with a full Ledger, `ruin_unlocked`). A pane of black glass in the Depths shows Juno on the other side, calling the PC's name: the exact image of `GO_LOOKING_BACK`. The prompt appears again: **Look back?** (`:ch15_look_back`).
  - *Yes:* it no longer kills you. The reflection steps aside, and the PC walks *through* into `story/12_RUIN_ROUTE.md` (R1).
  - *No:* the main story continues, and the door never reopens on that save.
- **The Hush** (808): a Bleed zone where sound doesn't exist. The PC can see their own footsteps as ripples. Atmospheric breather.

---

## CHAPTER 16 — "Clear Air" (R29 → R30 → Cogsworth, Gym 15; the Arbiter blueprints; Zekrom; the Sump Purge begins)

**Location:** R29, R30 (`:WASTELAND`, Zenith's eastern waste), **Cogsworth** (Zenith's foundry district, `:FACTORY`), **Strade Works**, the **Engine core chamber**.

**Arrival: Zenith, third visit (escalation).**
- Cogsworth runs **three shifts**. Smokestacks never stop, and clock-towers chime every quarter-hour.
- Topside "**Unity Rallies**" fill the plazas. Voss on giant screens: "Order. Light. Unity." Directorate banners hang from every gantry.
- Workers are tired and proud. Many are from Nadir, commuting up the lifts. They know something huge is being built and don't know what.
- **Rook Calder** is here, off-camera and unshaven. Since the Lowlight he has been quietly collecting Meridian Spire security footage. He finds the PC in a workers' canteen: "I've got Sable on tape. With a Meridian keycard. I've had it for months. I was scared."
  - **CHOICE `:ch16_rook`:**
    - **Leak it now:** it's public, and Kroll's identity is confirmed realm-wide even without Ch13 evidence. Meridian fires Rook within the hour and blacklists him from the Spire, so he can't cut the grid in Ch21 and can't reach the Zap Plate to release it (unless Marchetti turns).
    - **Hold it for the Festival:** Rook stays inside, smiling for cameras. He leaks it at the worst possible moment for Voss (Ch20 opening ceremony), and he's still in position to cut Lumen's grid in the hijack (`ROOK_CUTS_GRID`).

**Gym 15 (`:FACTORY`).** Thematic note: *conveyor-belt arena; machines you can jam or overdrive.* **Magnus Strade** is immaculate, prosthetic hand, pocket watch. "Faith gave us three hundred years of the Bleed. Engineering will give us the next three hundred without it." His ace is **Metagross**. He gives Dive suits via the bathysphere works.

**Infiltration: Strade Works (set piece).**
1. With Rook's keycards, the PC and Rook infiltrate the deep foundry after the gym.
2. **Partner battle: PC + Rook vs Marchetti + Quent** on the casting floor. The field goes `:FACTORY` → `:SCRAPYARD` as the floor is wrecked mid-battle.
3. In the drafting vault the PC finds the **Arbiter Engine blueprints** (Key Item **Arbiter Blueprints**):
   - A ring of eighteen locks to be built *into the new Festival arena*.
   - A keystone cradle "to be recovered from site AURELIA".
   - The notation: **"Calibration subject: UNIMPRINTED-01. Retention: indefinite."**
4. The **core chamber**: the Dark Stone at the center of a cage of Lattice-glass. It has **cracked open**, and **Zekrom** is half-emerged and bound in golden cable. This was the Fault's test-fire.
5. **Boss battle: Zekrom** (multi-bar). Each bar breaks a containment cable, and the PC is *freeing* it, not beating it. On victory, Zekrom tears free through the foundry roof into the Stormfront. Story consequence: **the Engine's original core is lost** (`ZEKROM_FREED`), and Voss must reroute through Lumen's grid.
6. **Game over `GO_OVERTIME` "Overtime".** Trigger: during the core-chamber sequence, a prompt to "finish copying the blueprints" while the containment klaxon counts down from 3 (warned twice by Rook: "We go when the whistle goes, no heroics"). *Epitaph: "You stayed past the whistle. Strade Works issued a statement about an industrial accident."*

**Magnus (choice).** Magnus finds the PC in the ruined vault with the blueprints. He doesn't call security.
> *"I don't build weapons. I build tolerances. I was told it was a Plate stabilizer. I learned the truth two years ago and kept building, because the math was beautiful and the alternative was the Bleed."*

- **CHOICE `:ch16_magnus`:**
  - **Expose him** (`MAGNUS_EXPOSED`): the PC takes the blueprints to the Zenith Council via Councillor Sallow. Magnus is arrested, Meridian loses a board vote and some public trust, and the Engine's design leaks publicly. But nobody is inside to sabotage it later.
  - **Appeal to his conscience** (`MAGNUS_KEPT_FAITH`): "Will you let it take a child?" He says nothing. He winds his watch. In the finale, he disables the Engine's **safety governor**, which weakens Voss's binding: "No machine I have built will kill a child."

**The Sump Purge begins.** That night, every screen in Zenith shows **"Operation Clear Air."**
- Since the Fault drained the Sump and exposed Aurelia, Meridian claims Nadir's lower districts are "lawless": Sweetrot gangs and Hollow terror cells. The **Directorate descends into Nadir**.
- Topside watches it like weather. A Cogsworth worker beside the PC, quietly: "My mum lives down there."

**INTERLUDE IV — "Clear Air"** (playable as **Wenlow**, Corvin's apprentice).
- Mirefen, the same night. The player controls Wenlow in the Infirmary as the Directorate comes up the stilt-walks.
- Wenlow moves patients, hides Sweetrot addicts in the Quiet Ward ("They won't search the glass ones. Nobody ever looks at the glass ones."), and fights two officers with Corvin's spare Pokémon.
- The last scene: Wenlow standing in the Ward's doorway between a Directorate squad and forty dreaming patients. "This is a hospital. You have to—"
- Cut to black. A single gunshot sound-effect, and nothing else.
- If `CORVIN_FREED`, Corvin is in Cragholm and learns by radio. If not, he's in a Directorate cell and learns from a guard.
- **This death cannot be prevented.** It is the act's moral floor.

**Cliffhanger:** Dawn. The PC, Rook and the blueprints on a supply-lift heading down into Nadir. Through the grille below, smoke rises from Underveil.

---

## CHAPTER 17 — "The Drowned Crown" (R31 → R32 → Seabed → Underveil, Gym 16; Aurelia; Voss)

**Location:**
- R31 (`:SCRAPYARD`), R32 (`:WATER_SURFACE`, the drained north coast), **R32 Seabed** (`:UNDERWATER`, Dive).
- **Underveil** (Nadir's heart, `:NEW_MOON`), the **Moon Market**.
- **Aurelia** (824 `:UNDERWATER` / 825–826 `:CAVE`), the **Sun Court**.
- **Ironbloom** (828, `:BLEED`: rust that flowers).
- Branch map 838 **Accord Archive** (high Accord Standing).

**Arrival: Nadir, third visit (aftermath of the Purge).**
- Underveil is a city of lanterns in the upper towers of drowned Aurelia, in permanent night under the Dread Plate. This morning it is smoke, broken lanterns and Directorate barricades.
- **Dozens are dead.** Nadir's fighters have pushed the Directorate back to the lifts. Mother Gutter's Muk holds one barricade, and Lantern Hollow volunteers hold another.
- **Game over `GO_INTO_THE_LINE` "Into the Line".** Trigger: at a barricade, a Directorate line advances on unarmed Nadir protestors. The PC is offered "Step between them?" Nyx's courier warns the PC twice, "Not you. You're the one thing they want alive. Don't make them choose." *Epitaph: "They didn't choose. The bullet did. Meridian called it a tragic accident, and meant it."*

**Nyx Calloway.**
- Silk, smoke, a crescent-moon earring. She receives the PC in the **Moon Market** among sellers of secrets.
- Today she isn't amused. She has been carrying bodies. "Underveil isn't on the Accord's maps, sweetheart. That's the point of Underveil. Apparently it's also why nobody comes when they shoot us."
- **Nadir declares independence** from Zenith that afternoon, by Nyx's proclamation read from the Moon Market steps with every Sump Baron present. It's symbolic, defiant and legally meaningless, and everyone cheers.

**Gym 16 (`:NEW_MOON`), an illusion double battle.** Thematic note: *nothing on the field is what it looks like; illusions mask both sides.* Nyx: "Everything has a price. Yours just went up." Her ace is **Zoroark**.

**Nyx's bargain.**
- **CHOICE `:ch17_nyx`:** Nyx has the **Engine's arena schematics**, Meridian's install plans for the Prism Arena.
  - **Trade the PC's own secret** (`NYX_BARGAIN_TAKEN`). Nyx gets to *know* exactly what the PC is, and she will use it. The PC gets the schematics, and in Ch21 Nyx cuts Meridian's comms precisely.
  - **Refuse:** Nyx shrugs and helps anyway in Ch21, sloppily, at a cost to herself (she's injured).
- Nyx confesses, unprompted, after the gym: "Two years ago I sold Voss the way into the Sun Court. I told myself it was just a door. My family's kept that door shut for three hundred years. I'm the one who opened it."

**Accord Archive branch** (838, high Accord Standing only). **Brann** meets the PC in a sealed Coastwatch vault on R32. It holds the **Concordance's Secret Articles in Maren's handwriting**: the Tuning, and the Hymn of Return. Brann confesses everything here, gently and early (see below), and gives the PC Maren's original Hymn page.

**Aurelia (dive set piece).**
1. With Dive suits from Cogsworth, the PC descends from R32's drained shallows to the **Seabed** and into **drowned Aurelia**.
   - **Sahar Ostrand** leads the expedition. She's the expert, terrified and thrilled: "Three hundred years. I've waited my whole *life*."
   - **Edda Morrow** pilots the support boat.
2. Golden terraces lie under green water. Gilder machines are rusted into coral. The Gilded King's statues have had their faces chiseled off by his daughter's people.
3. **The murals of the Sun Court** tell the real Prismfall in full: the Blight, the Two Weathers, the Chain, the Calling, the god *breaking itself*, the city falling, and **Princess Maren** pulling a colorless shard from the wreck of the keystone cradle.
4. **The keystone cradle itself** sits in the throne room's center: a golden hand, open, the size of a door. **The PC's shard resonates violently.** The PC's chest *glows* through their shirt, and the drowned room lights up with eighteen faint colors.
5. Nyx, who came down after all: **"Oh. Oh, darling. You're the missing piece."**
6. **The truth, named.** Sahar reads the cradle's inscription: *"Here rests the One that is every color and none."* The PC carries **a splinter of the Legend Plate**, Arceus's heart.
7. **Game over `GO_THE_THRONE` "The Throne".** Trigger: an exploration prompt, "Sit on the Gilded King's throne?" Foreshadowing: Sahar ("Don't touch anything gold. *Anything*."), and the throne's armrests shaped like open hands. The cradle *closes*. *Epitaph: "You fit perfectly. That was the problem the Gilders were trying to solve."*

**Aurelian Voss in the Sun Court.**
1. A Meridian salvage team cuts in through the throne room's far wall, and **Voss** walks in among them in a pressure suit with his helmet off in an air-pocket. He's here to collect the cradle. He is delighted to see the PC.
2. **The reveal, his way:**
   > *"House Aurel. My family. We changed the name and kept the grudge. I was eight when my grandfather showed me Theodric's notebooks. I was twenty-two when I realized he was right about everything except the chain. Metal was the wrong material."*
3. He admits AF 290 plainly: "My array. My dials. I was trying to measure the convergence. I didn't know it would break the Crown. I was very sorry about the forty people. I was even sorrier when I understood what I'd learned."
4. On the Lowlight: *"Twelve people. I've lost more to the Bleed in a quiet week. I made those twelve *mean* something."*
5. His philosophy: "Gods are absentee landlords. Arceus dropped its furniture on our heads three hundred years ago and never came back. I'm not trying to become a god. I'm trying to make sure we never need one again."
6. **His offer** (**CHOICE `:ch17_voss_offer`**):
   > *"Stand with me at the Festival. When it's done, no child in Velmora will ever be Fixed again. Your mother wilted in exile because of a broken god. I can fix the god."*
   - **Refuse** (always available).
   - **Feign agreement** (`VOSS_FEIGNED`): Voss lets the PC close in the finale, and the hijack has a different opening beat. It's risky, because if Meridian Standing is high and telemetry is intact, it tips toward Concord Dawn or the Bad ending.
   - **Accept** (`VOSS_ACCEPTED`): this opens the Concord Dawn ending path. Narrative Systems owns the consequences.
7. **Meridian admin battle: Kroll** (`MERIDIAN_KROLL`), or **Quent** if Kroll was beaten publicly in Ch13. They hold the PC off while Voss's team lifts the **keystone cradle** out through the wall. Voss leaves on a Meridian submarine. His last words: "Win your badges. I'll see you at the coronation."

**Brann's confession** (if not already given in the Archive branch). Above water, at Underveil's docks, **Brann Holloway** is waiting. He has come from Crownhaven on Valen's behalf. Confronted with everything, he tells the truth at last:
- The Tuning is real.
- The Crown kills Sovereigns.
- He reset the Crown's stone after the Fracture and knew it was short, and never asked where the rest went.
- Valen's arm is crystal to the shoulder.
- "He has weeks. Maybe the Festival."

He delivers Valen's message:
> *"He says: 'Win your last two badges. Then come to me, and I'll tell you everything.'"*

**Optional thread: cameo sidequest "Deliverer" (Amaria and Titania).** See `design/CAMEOS.md`. Edda's divers report a woman swimming *without a suit* in drowned Aurelia's lower galleries, singing to a Lapras, and an armored knight pacing the drained shallows above, refusing to leave. After Gym 16, before the PC leaves Underveil.

**Cliffhanger:** Night on the Underveil docks. The PC, Nyx, Sahar, Edda and Rook (and Rowan, if he came down) sit on crates in the lantern-light. Nyx counts on her fingers:
> *"Meridian wants you in that arena. The Accord wants you in that arena. The Hollow wants you in that arena. Two kings want you as *their* champion in that arena. Thirty days, sweetheart. Every power in Velmora is waiting for you to walk into one room."*

Edda: "Then we'd best make sure you walk in on your own feet."

**END OF ACT IV.** Title card: *V — Sovereign.*
