# Story Bible 08: Act V — Sovereign (Ch18–21, Gyms 17–18, the Festival of Champions)

> **Tone:** Desolation-dark, then a hard-won dawn. Everything planted pays off. The Festival week should feel like the whole game is in one city: every Warden, every faction, every Bond.
> **Mechanics ownership:** the Festival draw, game-over IDs and ending triggers belong to `story/10_CHOICES_ENDINGS.md` and `design/NARRATIVE_KEYS.md`. This file gives the **story content of every branch** they select from. "Default" means the SPINE Rev. 2 path, the fallback.
> Map names per WORLD.md (segments 16–18, Crownhaven 480–519). Caps: R16 90 · QF 92 · SF 94 · Final 96 · Hijack 100 · True Finale 100.
> **Revision 6:** this act carries beats of the Ashkaar–Isenmar War and the Blessing. See `14_WAR_AND_BLESSING.md` (timeline table) for the inserts per chapter; that file wins on conflicts.


> **Revision 7 (comedy):** each chapter here has a scripted funny scene in `15_COMEDY.md` §4 (Ch18–21), plus running gags (§3) and optional kingdom bits (§5). Place each scene where its heading says, and never inside the beats §1 lists as joke-free.

---

## CHAPTER 18 — "Once Upon a Time" (The Blindwater → Lightless Deep → The Gloamwood Verge → Gloaming, Gym 17; Pecharunt; K7; the Hymn)

**Location:**
- The Blindwater (`:CAVE`).
- **Lightless Deep** (844 `:DARK_CRYSTAL` / 845 `:NEW_MOON`).
- **Inverted Ward** (848, `:INVERSE`: an abandoned Choir hospital turned upside-down by the thinning Glass).
- **Gloamwood Verge**, **Gloaming** (Elowen's oldest corner, in the deep south-east, `:FAIRY_TALE`), the **Great Tree**.

### The Lightless Deep: Pecharunt (Nadir's legendary arc)
The road out of Underveil runs down, not up: below the drained Sump into the **Lightless Deep**, the oldest dark under the City Below.
1. Corvin (or Wenlow's notes, if Corvin was never freed) has traced **Sweetrot** to its source.
2. The Deep is a sweet-smelling cavern of pink crystal and docile, smiling thralls tending peach-shaped growths. **Mother Gutter**, the oldest Sump Baron, is here, blissed and centuries-old. She isn't the master. She's the *first thrall*.
3. **Boss battle: Pecharunt** (multi-bar). Its "mochi" poison spreads Sweetrot status-flavor across the field.
4. Defeating it frees the thralls across Nadir, and the Sweet Market's vendors blink awake in the street.
5. **Lore payoff:** Pecharunt enthralled the **Loyal Three** centuries ago and sent them to steal Elowen's Plates. The "Gossamer Ogre" drove them off. The pageants have had it backwards for 250 years.
6. If `OGERPON_TRUSTED`, Ogerpon appears at the Deep's mouth, waits for the PC and walks with them to Gloaming.

### Gloaming: Elowen, third visit (escalation)
- **Thornguard checkpoints.** Prince Caedmon (now effectively ruling Elowen, since his mother is "resting") has signed the **Forest Compact**. Meridian survey-flags line the Gloamwood. The Thornguard turns the PC back at the Verge "by royal order".
- The **dusk is spreading**: Gloaming's twilight has crept west across half the forest, and Briarwick's looms now work by lamplight at noon.
- **Optional scene, Queen Maelis:** in a dusk-garden she's "resting" in under polite guard. Shrewd and finally honest: "My son thinks the forest is a resource. I've been queen for sixty years. The forest is the *sovereign*. I'm just the gardener it tolerates." She gives the PC a **Royal Writ** (key item). It opens the Wardguard escort to Crownhaven even at low Accord Standing, and it seeds Elowen's epilogue: Maelis disowns the Compact.
- **Celestine** (in her true form; the PC met her disguised in Ch3, at Briarwick's shrine) dissolves the checkpoint with one sentence the Thornguard captain can't argue with, because she can't lie and everyone knows it: "If you stop this child, the forest will remember your name, and it will say it wrong forever."

### Gym 17 (`:FAIRY_TALE`), a double battle: "the knight and the dragon"
Thematic note: *the arena is a storybook. Choose your role (knight, dragon or thief), and the story's rules change who's strong.* Celestine: "Once upon a time — which is the only time there ever is, here —" Her ace is **Sylveon**.

### The Hymn of Return
In the dusk-chapel at the Great Tree's roots, Celestine gives the PC the **complete Hymn of Return**, sung for them by the Gloaming choir. If the PC received Wick's verse (Ch10) or Maren's page (Archive branch), the last verse visibly *completes* in the Key Item.

> *Eighteen we borrowed, eighteen we keep*
> *till the wounded land has learned to sleep;*
> *then one of no color, the eighteen roads walked,*
> *shall carry them home, as the old ones talked —*
> *not chained, not broken, not bought, not crowned:*
> *given back, as a gift is found.*

Celestine: "I've been waiting for you for forty years, little colorless thing. Valen reads 'one of no color' as *vessel*. The Hollow read it as *hammer*. Meridian reads it as *key*. It says *walker*. I cannot lie. I can, however, sing. These are the verses I sing." (Her phrasing is exact and deliberate. On the Ruin Route she admits there's a verse she stopped singing.)

### K7 (the Great Tree's roots)
1. Kestrel, Meridian's sponsored Festival entrant with 18 badges, arrives on a Directorate skiff. He's here to stop the PC going to Crownhaven, not for Meridian.
   > *"They all want to use you. Valen wants a lock. Voss wants a key. Your Hollow friends want a crowbar. Stay out of Crownhaven and let me end it. I'll beat Valen in front of the whole world and make him say her name."*
2. **K7** on the Fairy Tale field. Kestrel insists he's the knight and the PC is the dragon. If the PC's Bond with him is high, he flinches mid-battle.
3. After the battle:
   - **CHOICE `:ch18_kestrel_ring`:** if the PC has **Morwen's Ring** (Ch15), give it to him now or keep it for later.
     - Give it now: Kestrel's Bond goes up, and his Redeemed path becomes more likely. He doesn't say thank you. He puts it on.
     - Keep it: the ring can be given at the SF instead, for a bigger moment if he's Redeemed.
4. **Prompt: Stay out of Crownhaven?** (*Yes* / *No*.) *Yes* triggers **Game over `GO_STAY_OUT` "Somebody Else's Story"**: the PC does what everyone has told them since the ferry, and the Engine takes Kestrel instead.
5. On *No*, Kestrel leaves for Crownhaven: "Don't come. I mean it. ...You're going to come. Fine. Then don't lose before you reach me."

**Optional thread: cameo sidequest "Dreamwalker" (Shiv).** See `design/CAMEOS.md`. In Gloaming's dusk-chapels, a grinning stranger keeps appearing in the townsfolk's dreams. He says he's met the PC before, on a ferry.

### Game over `GO_FAIR_BARGAIN` "Fair Bargain"
Gloaming's lantern-moth market offers bargains. One stall promises "the answer to your mother's last question". Accepting without asking the price triggers it. Celestine has warned the PC on arrival: "In Gloaming, always ask what it costs *before* you say yes." *Epitaph: "The price was your name. You are very happy now, as a lantern-moth, and you will glow at every dusk."*

---

## CHAPTER 19 — "The Last Gate" (The Gloamwood → The Thornwar Marches → Wyrmscar Rift → Wyrmrest, Gym 18; Reshiram; Sigrun's trial)

**Location:** **Gloamwood** (`:FAIRY_TALE`), the Thornwar Marches (`:MOUNTAIN`), **Wyrmscar Rift** (864 `:CAVE` / 865 `:DRAGONS_DEN`), **Wyrmrest** (Ashkaar), **Rainbow Scar** (868, `:RAINBOW`).

### Arrival: Ashkaar, second visit (escalation)
- **Dominar Hrothgar** is at the front with his legions, in the Ashkaar Siege Camp on Ossaria's western dunes, the length of Ashkaar and half of Ossaria away (14_WAR_AND_BLESSING). Wyrmrest is held by Sigrun's own riders. The Dominar means to march on Zenith "the hour the Festival ends", and he has ordered his daughter to close the pass to everyone Zenith-tainted. That includes the PC: Meridian's Fellowship, Meridian's badge case.
- **Sigrun Ashfall** keeps the pass open anyway, in open defiance, standing on the gate in dragonhide with her Salamence. "Wyrmrest is the last gate. Dragons don't let anything through they haven't weighed. *I* do the weighing, Father. Not you."

### The Dominar (optional political scene, `DOMINAR_SWAYED`)
- The PC petitions the Dominar in his command pavilion at the Siege Camp, after the Battle of the Glass Dunes (Sigrun has flown them there; below). Lies are a capital crime in an Ashkaar court, and the oath-brazier is lit.
- Persuading him to fly *for* Crownhaven instead of *against* Zenith requires:
  - the Light Stone sent to Wyrmrest (`:ch8_lightstone` = wyrmrest) **plus** proof (the **Arbiter Blueprints** or the **Larch Papers**), **or**
  - Sigrun's Bond ≥ 4, so that she speaks for the PC (`:ch19_dominar`).
- Success: "If the god is in chains, then dragons will break them. Not for the Accord. For the god." His legions are present in the hijack.
- Failure: his riders go home after the truce and take no part in defending Crownhaven. (`DOMINAR_SWAYED` can't be set if Isenmar won the war without mercy terms.)

### Sigrun's trial (Wyrmscar Rift)
1. Sigrun won't let the PC challenge her until they walk the **Wyrmscar Rift** to the Draco Plate with her and **speak aloud what they intend to do at the Festival**.
2. **Sigrun's confession** on the walk:
   > *"He trained me to be his successor. Then he told me I'd never survive the Crown, and I was relieved. Do you understand? Relieved. And then he went looking for you. I knew. For two years I knew, and I let it happen, because it meant it wasn't me."*
3. At the Rift's heart, at the brazier over the Draco Plate, the PC speaks. This is an **authored line** and also a soft commitment that the ending checks (Narrative Systems owns how much weight it carries). **CHOICE `:ch19_oath`:**
   - **"I'm going to give them back."** (Return)
   - **"I'm going to keep them safe. Whatever it costs me."** (Keep)
   - **"I don't know yet. I'm going to find out with my eyes open."** (Open)
   - *(Only if Resonance ≤ −2:)* **"I'm going to end it. All of it."** Sigrun draws her blade but lets them pass, horrified.
4. **Game over `GO_LIARS_PYRE` "Liar's Pyre".** A fifth option is always offered: "Whatever you want to hear." Foreshadowing: the Ashkaar gate-guard's "say true or say nothing", and the brazier oath. The fire answers. *Epitaph: "Ashkaar burns liars. It is the oldest law, and the dragons remember it even when men forget."*

### The Battle of the Glass Dunes (between the oath and Gym 18)
After the oath, word comes that Kyogre has risen and is dragging a flood-sea across the desert, and that the Dominar has carried the Light Stone to the front. Sigrun flies the PC to Ossaria's western dunes overnight. The battle, its choices (`:war_climax`, `:war_terms`), WAR-1 and the legendary fight are in **14_WAR_AND_BLESSING Part B**; the Dominar's petition follows it. Then Sigrun flies the PC back to Wyrmrest for Gym 18.

### Reshiram (Ashkaar's legendary arc)
*(Unless `:war_legend` is `:neither`, the Light Stone wakes in the Dominar's hand on the Glass Dunes and the fight below happens there, on the dunes' field; see 14. With `:neither` the stone stays dark at the front, and the fight happens here, as written, after the truce, when the stone comes home.)*
1. Any true answer wakes the **Light Stone**, which has hung in Wyrmrest's Rift-shrine since Ch8 if it was sent there, or which arrives carried by a Hearthguild runner if it wasn't.
2. **Boss battle: Reshiram** (multi-bar) on `:DRAGONS_DEN`. Its fire is the truth of the PC's oath: Return and Open lean Harmony, Keep is neutral, and Ruin makes the fight savage.
3. After the battle, Reshiram bows to Sigrun, not to the PC: "the truth is hers to carry now." It flies to Crownhaven ahead of them.
4. Sigrun, stunned: "...It chose the one who finally said it out loud."

### Gym 18 (`:DRAGONS_DEN`)
Thematic note: *the den's heat rises each turn, and the dragons grow stronger the longer you hesitate.* Sigrun fights at her absolute best. "If you can't beat me, you can't survive him." Her ace is **Salamence**. On victory she gives the **18th badge**, and the badge case **sings**: all eighteen tones together.
- If the telemetry was left intact, a Meridian airship on the horizon turns toward Crownhaven within the minute.
- If it was sabotaged, Larch's voice on the radio: "He bought it. God help us, he bought it."

### Rainbow Scar and the road to Crownhaven
**Rainbow Scar** (868) is a Bleed zone where all eighteen Imprints bleed together into light. It foreshadows the Prism Arena. Then **The Pilgrim Pass** and the **Sovereign's Ascent**:
- At high Accord Standing or with the Royal Writ, the Wardguard escort takes the PC up the processional stair.
- Otherwise, Edda's smugglers take them through the **Glassfall Scar** (888), the forty Fixed of AF 290, still in Lower Crownhaven where they fell. The PC walks among them. One of them is a Choir cantor with her mouth open mid-note who is not Ines; Ines got out. The PC finds the place where they stood at five.

---

## CHAPTER 20 — "The Festival of Champions" (Crownhaven, Festival week)

> **Revision 4:** no sister-game cameos appear anywhere in Festival week. They are optional sidequests elsewhere (`design/CAMEOS.md`). The bracket, draw pools and exhibitions use **original characters only**, following `story/10_CHOICES_ENDINGS.md` §3 and NARRATIVE_KEYS §6. **Revision 5:** every possible opponent is someone the PC has met at least twice by Act IV.
> **Revision 6:** the Festival is the ceremony of **Arceus's Blessing**. Entrants are **kingdom delegations** (two per kingdom, Valen, and the PC), chosen by player choices: see `14_WAR_AND_BLESSING.md` Part A, which replaces the seed list here. The PC picks their colors on Day 0 (`:ch20_colors`). Companion-vs-companion matches can be watched as highlight cutscenes (`13_CUTSCENES.md`). The Coronation in Ch21 is "the Blessing", and Ch19's Dominar scenes play inside the Battle of the Glass Dunes.

### Day 0: Arrival
1. **Crownhaven** is white stone and bells in the caldera. Upper Crownhaven is festooned with **Tamsin's eighteen banners**, woven since Ch10. The **Meridian Prism Arena** gleams where the old grounds were, too new.
2. **The Consent display.** By Day 1 each Warden's banner hangs **white** (they would let go) or **grey** (they won't). It is Tamsin's private reading of her colleagues, and the player can read it. These are the Consent conditions made visible (NS §6.2).
3. Every faction is here:
   - Meridian runs security under a Council vote that Anja's swing vote couldn't stop.
   - The Lantern Hollow are disguised as Choir porters.
   - The kings are in the observers' gallery: Caedmon for Elowen, Eirik, the Dominar's herald, Kassan, Dask.
   - **Envoy Delphine Okoro** of the Concert, deciding on Severance.
4. **The Veil Gate stays shut.** The Festival used to host champions of other worlds, until the Synod sealed the Gate in AF 230 (01_WORLD_LORE). Archseer **Dask** refuses Hollis's request to reopen it "for prestige": "The Glass is leaking already. I won't open a door in a wall that's falling down." No foreign champions come this year. Every entrant is someone the PC has met on the road (Revision 5).
5. **The Draw.** The Hierophant draws lots from a crystal bowl at the Basilica steps.
   - **Sixteen stand in the arena:** the PC and fifteen kingdom delegates (10_CHOICES_ENDINGS §3.1; staging in 14_WAR_AND_BLESSING Part A). The war decides how many seats Isenmar and Ashkaar hold.
   - **The PC's colors (`:ch20_colors`).** Before the bowl, Queen Maelis, the Zenith Council and Nyx each offer the PC their colors, and Larch offers none: the old clause for "the Unsworn". Values `elowen / zenith / nadir / unsworn` (NARRATIVE_KEYS §4.3).
   - The lots are honest; the bowl isn't. The Accord's old customs (the Right of Grievance, yielded invitations, a Warden asking for a challenger's quarter, and Dorian, who has never once let the bowl ruin a good story) bend it on screen (NS §3.1).

### Day 1: The Opening Ceremony (the 18 Plates)
1. **The procession.** At dusk, eighteen Wardens descend the Sovereign's Stair into the Prism Arena, each carrying their Plate in a reliquary, in gym order to the counting rhyme sung by the Choir:
   - Dorian (Blank)
   - Tamsin (Insect)
   - Marisol (Splash)
   - Rook (Zap, still cracked, in a cradle; if Rook was fired in Ch16, a Meridian officer carries it, and Rook watches from the crowd)
   - Sahar (Earth)
   - Corvin (Toxic; carried by a Choir porter in his mask unless `CORVIN_FREED`)
   - Brann (Flame)
   - Kaito (Fist)
   - Juno (Meadow)
   - Anja (Icicle)
   - Odessa (Sky)
   - Ilsa (Mind)
   - Bastian (Stone, leaning on Pip)
   - Ysolde (Spooky)
   - Magnus (Iron; under guard if `MAGNUS_EXPOSED`)
   - Nyx (Dread)
   - Celestine (Pixie)
   - Sigrun (Draco)

   Each sets their Plate into a pylon of the **Concordance Ring**.
2. **The Tuning.** Valen in white, the Crown on his brow, the grey glove *off*. The arena sees his crystal arm for the first time, and a murmur runs through forty thousand people. The Choir sings the half-Hymn. The Ring lights in eighteen colors, and the sky over Crownhaven ripples.
3. **The PC's vision.** The shard resonates violently. The world goes white. In the white, a vast shape of light with eighteen empty places in its wheel opens one eye:
   > *"...Little light. You have carried me far."*

   The PC collapses in the stands. Valen sees. Ilsa, in the Warden ranks, takes her earmuffs off and *flinches* at her father's pain.
4. **Rook's leak** (if `:ch16_rook` = hold): the Spire footage of Kroll with a Meridian keycard plays on the arena's own screens, hijacked by Rook's Rotom. The crowd turns. Voss, in his box, doesn't blink: "Rogue contractor. The inquiry continues." Meridian's polling drops, and the Envoy takes notes.

### Day 2: Round of 16 ("someone from your past")
Story staging for each R16 candidate (draw rules: NS §3.2):
- **Marisol, by Right of Grievance** (she holds an Isenmar seat, Teo died, and her Bond ≤ 2). The old Accord custom lets a Warden claim a first-round match against a challenger who wronged their city, and the Hierophant reads it out. Marisol and Juno swap seeds: "Let's see you run past *me*."
- **Anja** (she holds an Isenmar seat, and was exposed in Ch11). She invokes the same right, and she and Juno swap seeds: "You threw me to the court. Fine. Ice remembers."
- **Rowan, "the Gardener"** (Rowan alive, mercy pleaded at the tribunal, Hollow Standing ≥ 4). Rowan enters masked under a false name. **Juno** gave him her own invitation: "One last garden, child. Then I'm done with masks." If Rowan drowned at the Fault, this candidate doesn't exist.
- **Juno (J4, fallback).** Joyful and nervous under the arena's lights: "We started on the same dock. Let's see who's grown more." The fields cycle on `:PRISM_ARENA`. Her ace is Tsareena, with **Ogerpon** in her party if `OGERPON_TRUSTED`. If she's displaced by Marisol or Anja, she plays on in their seed (Isenmar's: against Nadir's second delegate, or against Ashkaar's), and her **Garden Match** exhibition opens when she's out. If she gave her invitation to Rowan, she watches from the Wardens' box.

**After the match: the garden court.**
- If Rowan lives, the PC finds Juno and Rowan in the arena's garden court, sitting apart on the same bench. If **Teo** lived, he says it himself, holding up his glassed fingers: *"I could hear everything while it had me. Everyone who sat with me."* (If the PC carries Venam's Testimony from her optional sidequest, it can be played here instead.) Rowan sits down on the grass and cries, and Juno takes his good hand. It's the first time they've touched since Ironreach.
- Without the testimony, Juno does it herself, more slowly: "Corvin says they dream. I'm going to believe him."
- If Rowan drowned, Juno sits alone with Elin's pressed lily from the Bride Tree.

**Other R16 results** follow the companion match rules (NARRATIVE_KEYS §6), and each can be watched as a highlight (`13_CUTSCENES.md`). Story requirements:
- **Kestrel** advances with the Gauntlet, over Zenith's first delegate (Rook or Odessa).
- **Valen** and **Sigrun** advance.

### Day 3: Exhibitions and the Festival Grounds
- **The Eevee Octave** (SPINE Rev 19; `design/EEVEE_OCTAVE.md`). On arrival (Day 0) the PC meets **Carol**, the Octave's Crownhaven singer, in the **Glassfall Memorial Garden** (489); her quest *The Ninth Verse* opens once the PC has helped the other seven singers on the road (Lyra, Aria, Cadence, Sona, Noct, Forte, Lento). Once all eight are helped, **Vesper** waits in the garden with the others: they want to thank the PC and test whether they can carry the power of Eevee. The **gauntlet**: the eight singers in the order the PC helped them, back to back with no healing, each with one Eeveelution on its home field using its type's **Z-move**; then Vesper's Eevee **Amen** with **Extreme Evoboost** on the Grand Stage. Open from then on, through Festival week and after.
  - Vesper, gentle: "We were all born the year the Crown broke. The Choir says we're lucky. I think we're just... what was left."
  - Reward: an **Eevee**, the **Eevium Z** and Vesper's **Z-Power Ring**. If Understudy is still an Eevee, Vesper says the crystal works for it too; if it has evolved, she notes which Imprint "claimed" it.
- **Other exhibitions** (NS §3.6, original characters only):
  - **The Pageant Bout:** Dorian and Rook in a double battle staged as "a duet for the cameras", with Rook's Rotom filming it.
  - **Juno's Garden Match**, if she wasn't the PC's R16.
  - **The Ebb Guild match** with Marisol while Teo heckles from the stands, if Teo was saved and Marisol is close.
- **Festival grounds side content:** the **Concordance Spire** (Battle Tower) under construction, a teaser; street food from every kingdom; Dorian rehearsing in secret with Celestine.
- **Diplomacy with Envoy Okoro (`:ch20_envoy`).**
  - **Proof** needs **two of three**: the **Larch Papers**, the **Arbiter Blueprints**, and **testimony that the Fixed still dream** (any one of: Teo's, if he lived; Corvin's Quiet Ward records, if he's free; Venam's Testimony from her optional sidequest). Together they show the Bleed is *caused* and so curable, not contagious. Okoro recommends against Severance (`ENVOY_PERSUADED`).
  - **Plea:** she listens and drafts Severance anyway, "with regret".

### Day 4: Quarterfinal ("the honest view")
The story job is an honest view of the PC's choice from someone who isn't trying to use them, delivered in a hard fight at cap 92. Conditional candidates swap seeds with the fallback (NS §3.5).
- **Celestine (fallback, the headline).** She confirms the Return, and it counts as an oath because she cannot lie: "I cannot lie, so listen while we fight." After the match:
  > *"Give them back. I've waited forty years to say that to someone who could."*
- **Sigrun** (Resonance ≤ −3, or the PC helped Isenmar break her father's legions): "Dragons weigh things. You've gotten heavier."
- **Kaito** (the oath was Keep): "You'd keep them? Marrowgate's still knocking."
- **Ysolde** (Kestrel has fallen): "If I can't reach him, I'll find out what reached you."
- **Odessa** (she holds a seat; five close Bonds; Harmony-leaning): "Everyone keeps telling you what you're *for*. The wind doesn't care. What do *you* want?"
- *(Ruin Route: Archseer Dask. See 12_RUIN_ROUTE.)*

**Other QF** (default): **Kestrel** beats **Kaito**, whose Lucario felt it: "That isn't him fighting." **Valen** advances. **Sigrun** advances, unless she was drawn into the PC's quarter (then Celestine plays on in Ashkaar's seed).

### Day 5: The Night of Masques, the audience, Little Owl
- **Corvin**, privately, after treating Valen in the Sanctum: "He has weeks. Maybe. He's holding the Plates quiet *right now*, with his body, every hour since the ceremony. He'll fight you tomorrow on what's left."

**The Night of Masques: "The Gilded King."**
1. In the Basilica square, **Dorian** stages Ansel Crewe's banned play for the first time in 248 years. **Celestine**, who cannot lie, voices **Princess Maren's lament**, and the Saltmere Players wear the Hollow's ogre masks *as the chorus*.
2. The square watches the true Prismfall: the Blight, the chain, the god breaking itself, the city drowning, the daughter's penance.
3. Chancellor **Hollis** sends the Wardguard to stop it. **Kaito** (and, if alive, **Teo**'s strikers) stand in the way, and the guard doesn't push.
4. When the actor playing the Gilded King says *"If heaven will not kneel, we'll build a chain"*, every head in the square turns to the Meridian box.
5. **Voss** stands and applauds. Alone. Warmly.
   > *"Bravo. They finally cast the king correctly."*

**Calla's defection (`:ch20_calla`, who lives).** Only offered if someone inside is already moving (`:ch16_rook` = hold, or `MAGNUS_KEPT_FAITH`).
- In the crowd after the play, **Calla Wren** finds the PC, shaking, still in her Meridian lanyard. She can get the arena's power schematics to Larch.
  > *"I scanned you on the dock. I photographed the screen. I've been sending him your life for six months. Let me do one thing that isn't that."*
- **Shelter her** with Edda's boat. She brings the partial schematics she already has: one crack in the Engine. She lives.
- **Send her back** for the full set: two cracks. Kroll finds her in the Spire stairwell, and she doesn't come back. The schematics arrive by Gale Post at dawn, with a smear of blood on the envelope.
- **Turn her away:** "Then I'll just — go home, I suppose." She leaves, and nobody sees her again.

**Valen's audience (the PC speaks).** Valen summons the PC to the **Sovereign's Sanctum**: candlelight, a camp bed, his crystal arm resting on a cushion like something borrowed. He doesn't defend himself. He explains.
> *"Every ten years I bring the Plates home to Crownhaven, and every ten years Velmora *endures*. You noticed I never said 'thrives'. Nobody ever notices."*
>
> *"Morwen didn't cause the Glassfall. I let them say she did, because if the world knew the ceremony could fail, the kings would tear the Plates out of the ground and we'd all drown. I chose a country over a woman's name. I'd do it again. I hate that I'd do it again."*
>
> *"When you beat me tomorrow — and you will — I'll put the Crown on you. The splinter in your heart will make it whole. You'll hold the Plates quiet for a hundred years, and you won't age as fast as I did. You'll be... very lonely. I'm sorry. I have no other door."*

**The PC answers** (authored line, **CHOICE `:ch20_audience`**):
1. **"There's another door. The Hymn. We give them back."** (Return)
   - Valen: "And let eighteen cities go dark? Rimeholt drowns, Cindervault freezes, Verdance's fields fail in a year..."
   - The PC can answer with the Hymn ("given back, as a gift is found") if they hold the complete version.
   - Valen, very quietly: "...Maren wrote that. I thought it was a poem."
2. **"Then I'll wear it. Somebody has to."** (Keep) Valen weeps, once.
3. **"You don't get to decide that for me. Nobody does."** (Refuse) Valen: "Good. Then decide it yourself, tomorrow. That's all I ever wanted, and I never had the courage to want it out loud."
   - If the PC refuses with a cold Bond, Ilsa never came, and the telemetry still runs, this sets **`VALEN_COLLAPSED`**. Voss's pre-ignition drains him overnight, and he can't stand for the Final.

**Game over `GO_EARLY_CROWN` "Early Crown".** Valen offers, desperate, to crown the PC *tonight* and skip the Final, "so I don't have to hurt you first." Accepting triggers it. Foreshadowing: Ilsa's earlier warning, "Don't let him hand you anything tonight. He's not thinking, he's *drowning*." The Crown is incomplete without the Engine's cradle, which Voss has. The half-Tuning Fixes the PC in the Sanctum, and Voss's men collect the keystone from the Sanctum floor. *Epitaph: "The Crown was whole for one second. Then it was Meridian's."*

**"Little Owl"** (Ilsa's side quest culmination, `:sq_little_owl`). If the PC completed her quest steps, carrying her messages to her father through Acts III–V, Ilsa comes to the Sanctum after the audience.
> *"You chose a country over a daughter. Fine. Then save the country, Father. Don't make a child pay for it."*

Valen: "...Little owl." It's the name from her childhood, which the player heard in the Mindscape in Ch13. She stays the night. If not completed, she watches the Sanctum door from the colonnade and doesn't go in.

**Morwen's Echo** (conditional exhibition, NS §3.6: Kestrel and Ysolde reconciled, and the K6 line was Resolve). After midnight, Ysolde lights the Hollow Cathedral's lantern in a Crownhaven chapel. **Morwen's echo** fights the PC once, gently, "to see what I bought."

**INTERLUDE V — "The Last Night"** (playable as **Valen**).
1. Short and quiet. The player controls Valen in the Sanctum before dawn.
2. He writes three letters:
   - To Ilsa: if reconciled, he tears it up, because he doesn't need it.
   - To Morwen's son: "I'm not asking you to forgive me."
   - To "whoever wears it next".
3. He walks to the window and talks to **Zygarde** (a single Cell glowing on the sill): "Order, not justice. I chose order. Was I wrong?" The Cell pulses once. The player decides what that means.

### Day 6: Semifinal — Kestrel (K8)
**Kestrel's state** (`KESTREL_FALLEN` or not; NS rules):
- **Kestrel (Redeemed)** (fallback). He fights with the Gauntlet at first. Mid-battle, at the first field-cycle, he looks at the Gauntlet's light and **tears it off**, then throws it across the arena floor:
  > *"No. Not like this. If I beat you, I beat* you*."*

  He finishes with **Morwen's Mismagius** and his **Aegislash**, honest and ferocious.
- **Kestrel (Fallen).** He *keeps* the Gauntlet on. His Pokémon glow with stolen Imprint, the field cycles under his command, and he fights like someone drowning. After the loss, the Gauntlet overloads and burns his hand, and Voss's men carry him off "for medical attention". He reappears in the hijack harnessed into the Engine (Ch21).

**After the match, Morwen's letter.** **Ysolde** walks onto the arena floor and gives Kestrel the sealed letter at last. He reads it there, in front of forty thousand people, and the arena screens tactfully cut away. The text (Key Item, readable later):
> *"Kestrel. If you're reading this, you're ready, or Ysolde's given up waiting. Both are fine. I didn't fail. I chose. There was a child in the light and I was nearest, and I'd have wanted someone to choose you. They'll call me a disgrace. Let them. Be a Vane anyway — be the kind that's nearest when it matters. I love you more than my seat, more than my name, more than my Plate. That's the whole letter. — Mum."*

- **Redeemed:** Kestrel sits down on the arena floor. If the PC still has **Morwen's Ring**, they can give it now. Then:
  > *"...Then you take him. Take him for both of us."*

  If both Ysolde's and Kestrel's Bonds are high (`KESTREL_YSOLDE_RECONCILED`), he lets her sit beside him.
- **Fallen:** he doesn't read it. Ysolde keeps it. If the PC kept `:ch12_letter`, they can quote Morwen to him in the Engine instead.

**Other SF** (default; if Sigrun was the PC's QF, Valen's semifinal is a one-line result instead): **Valen beats Sigrun.** Sigrun entered to win the Crown herself and spare the PC, and Valen beat her *to protect her*. She leaves the arena without a word. The PC finds her on the Basilica roof: "He beat me with an arm made of glass. I've never been so angry in my life."

### Day 7: The Final, the Coronation, the Hijack
See Chapter 21.

---

## CHAPTER 21 — "Sovereign" (the Final, the Hijack, Arceus, the endings)

### The Final: Valen Corrigan (`CHAMPION_VALEN`, cap 96)
1. Dawn. The whole cast fills the arena.
2. Valen, with no glove at all now: "Come on, then. Show me there's another door."
3. **The battle** on `:PRISM_ARENA`, with fields cycling. His ace is **Zygarde** (Complete Forme on its last bar: "Order, not justice. I chose order.").
4. Mid-battle, every time the field cycles, his crystal visibly spreads, from shoulder to throat.
5. **Draw variant, "Valen or his successor":** if Valen has collapsed before the Final, the PC fights the Sovereign-designate instead.
   - This happens if `VALEN_COLLAPSED` is set (Ch20 audience).
   - **Sigrun** (Bond ≥ 5): "He beat me with an arm made of glass. Now he can't stand. So it's me."
   - Otherwise **Brann**, who fights in tears: "He asked me to. Last thing he asked."
   - Valen watches from a stretcher, which puts him in position for the Ring later.
6. **After the PC wins:** Valen yields, smiling. "Velmora has a new champion."

### The Coronation
1. Valen lifts the **Crown** from his head and walks to the PC at the arena's heart, inside the Concordance Ring.
2. The Choir sings, and the crowd is on its feet.
3. **CHOICE `:ch21_crown`:** kneel to receive it / stand / step back. Each is flavor that the Narrative Systems endings may read.
4. The moment the Crown is raised over the PC's head, the eighteen Plates in the Ring *scream*.

### The Hijack (default hijacker: Voss)
1. **The Meridian Prism Arena wakes.** Its rings (the **Arbiter Engine**, built into the venue) ignite in gold.
2. The keystone cradle, installed beneath the arena floor, *rises* in a golden hand.
3. The Concordance Ring's pylons sprout golden locks, the new Gilded Chain.
4. The Crown is torn from Valen's hand into the cradle. The PC is pinned by their own shard's pull, half-kneeling at the cradle's palm.
5. **Voss** descends from his box onto the arena floor in a Meridian Engine-harness. He's calm, almost apologetic, wearing his gold sunburst pin.
   > *"You carried my key through eighteen doors. Let me show you what it opens."*

**Hijacker variants** (NS §3.2):
- **Dr. Quent** (Voss discredited: `MAGNUS_EXPOSED` plus Rook's leak plus the Night of Masques). The board removed Voss in disgrace before Day 7. Quent giggles in the harness, with Voss's Silvally team. Voss watches from the gallery, appalled at his own machine in someone else's hands.
- **Ruin Route:** Theodric, the Gilded Reflection (`story/12_RUIN_ROUTE.md`, R7).

**His hand.** Larch has warned the PC that morning: "Don't let him make you a part. He's very good at parts." Voss offers his hand: "Stand up. Stand with me. It doesn't have to hurt."
- **With `VOSS_ACCEPTED`** (`:ch21_hand`):
  - *Take* it: **Concord Dawn** begins here, and Arceus is never fought.
  - *Refuse*: Voss, genuinely hurt: "You promised."
- **Without it,** taking his hand is **Game over `GO_HIS_HAND` "His Hand"**. Foreshadowing: Kestrel's K7 speech, and Celestine's "not chained, not bought". *Epitaph: "It didn't hurt. That was the cruelest part."*

**The allies move.** Each beat fires only if its condition holds. Show as a fast montage, one line each. These are Larch's eleven lamps (NS §6.2).
- **Rook** (`ROOK_CUTS_GRID`, which needs `:ch16_rook` = hold) cuts Lumen's grid from the arena feed: "First time Lumen's been dark in ten years. Kinda pretty." The Engine flickers.
- **Nyx** blacks out Meridian comms. With the bargain (`NYX_PRECISE`) it's surgical. Without it, it's bloody, and it doesn't count as an Engine break.
- **Magnus** (`MAGNUS_KEPT_FAITH`) in the arena's machine-gallery disables the safety governor: "No machine I have built will kill a child. Governor's off. Go."
- **Marchetti** (`MARCHETTI_TURNED`: Ch14 evidence, or saved at the Fault) orders the Directorate to stand down: "Not for this. Never for this."
- **Larch** reads the Engine's live output off her board of eleven lamps. With `TELEMETRY_SABOTAGED`: "It's miscalibrated! It's reaching for a shard that isn't where it thinks!"
- **Calla's schematics** (`:ch20_calla`) light one lamp, or two if she went back. If she went back, Larch touches the second lamp and says nothing.
- **Sigrun** and her dragons hold the sky against Meridian's *Gilded Hours* airships, with **Reshiram** beside her. With `DOMINAR_SWAYED`, the Ashkaar legions fly with her.
- **Marisol's** fishing fleet evacuates Lower Crownhaven across the caldera lake. **Edda** pilots the lead boat.
- **Tamsin's** silk nets catch falling arena debris over the stands.
- **The Lantern Hollow** (`LANTERN_HOLDS`), led by Rowan, Teo, or Thistle and Wick, guard the Ring's pylons against Directorate techs.
- **Kaito** holds the arena gate.

**Tag battle (story).** It's a short, desperate double battle on the cracking arena floor that clears the way to the hijacker.
- **Partner:** **Kestrel** if Redeemed, otherwise **Juno**.
- **Foes:** two of **Marchetti / Quent / Kroll**, whichever aren't turned, dead or hijacking (NS: "Ch21 tag foes v21").

### Voss (`MERIDIAN_VOSS`, cap 100) on `:PRISM_ARENA`
- **Boss battle** (multi-bar for his ace): **Silvally** (Project NULL), whose type *follows the active field* as the Prism Arena cycles through the eighteen gym fields. The rest of his team is "things men made" (see 03_CAST).
- Mid-battle lines:
  - "Your mother wilted for ten years because a god dropped its furniture on her."
  - "I'm not your enemy. I'm the only adult in this arena who'll say the true thing out loud: *we don't need it*."
- **Between bars 2 and 3, if `KESTREL_FALLEN`:** Kestrel is revealed harnessed into the Engine as Voss's conduit, Gauntlet fused to the cradle and burning. **CHOICE `:ch21_reach_kestrel`:**
  - **Reach** (needs Morwen's Ring or Morwen's words from a kept letter): the PC says her line, *"Be the kind that's nearest when it matters."* He comes back. The Gauntlet goes dark, and Kestrel tears himself loose.
  - **Burn:** the PC's shard tears the Gauntlet off by force. He lives, scarred across the arm (Ruin −3).
  - **Let go:** he burns out as the Engine fires (`KESTREL_LOST`). This is the road to **The Empty Lighthouse**.
- **On defeat:** the Engine doesn't stop. Voss drives his harness-spike into the cradle and becomes the conduit himself. "Then *I'll* hold it."

### Arceus Descends
1. The sky over Crownhaven opens, white.
2. **Arceus** is dragged down through it into the Engine's golden chains, eighteen locks closing on eighteen empty places in its wheel. It is enormous, half-bound and *in agony*. The **Prism Arena turns to `:BLEED`** across the whole caldera.
3. The hijacker, at the cradle, ecstatic and horrified: "It's — it's *beautiful* —"
4. **Arceus's Judgment strikes the harness.** **CHOICE `:ch21_spare_voss`:**
   - **Shield** him with the shard (`PC_SPARED_VOSS`): he lives, crippled.
   - **Let it judge:** he becomes light at the arena's heart.
5. The Bleed surge rolls out toward forty thousand people in the stands.

**Valen holds the Ring.**
1. Valen puts the **cracked Crown** back on, from the cradle's palm where the PC tore it loose, and walks into the Concordance Ring.
2. He grips two pylons and *holds the surge*. His crystal blazes white.
3. If `ILSA_RECONCILED`, Ilsa is at his back with her hands on his shoulders, pouring her mind into his: "I've got you. Little owl's got you."
   > *"Go. Free it. I'll hold the door — I've had thirty years of practice."*

(If Valen collapsed before the Final, he is carried to the Ring on his stretcher and stands up anyway.)

### The True Finale: Arceus (cap 100)
**Boss battle: Arceus**, multi-bar, type- and field-shifting. Variant by state (NS §6.6): **Bound** (default), **Miscalibrated** (telemetry sabotaged), **War** (Resonance ≤ −6), **Gilded** (Engine calibrated: the Bad ending), **Judgment** (Ruin Route only).
- **Six bars, three locks each, in gym order.** Bar 1 is Dorian, Tamsin and Marisol, and so on through bar 6: Nyx, Celestine and Sigrun. The Prism Arena shifts to the matching gym field for each lock.
- **Between bars**, those three Wardens kneel at their pylons and **release** their Plate, letting go of the bond they've carried their whole life, or **refuse**. Every refusal makes the next lock **forced**: Arceus gains +1 to every stat stage for that bar.
- **All 36 lines** (18 releases, 18 refusals, each refusal tied to the player's choice that caused it) are in **`story/11_FINALE_LINES.md`**.
- **Celestine** sings the Hymn's last verse as her lock breaks. The Gloaming choir in the stands picks it up, then the Prism Choir, then the crowd.
- **Harmony vs Ruin.** At high Harmony, the PC's Pokémon are steadied by the shard (systems: minor buffs). In the **War** variant, the shard *eats* Arceus's types instead of freeing them, and the battle is a war, not a liberation.
- **Gilded variant:** the PC fights *for* Arceus against the chains and loses the struggle anyway. The last bar can't be broken. This is **The Gilded Chain**.

**Valen's death** (all main-route paths except Gilded). As the final lock breaks, Valen's crystal burns through, not to glass but to *light*. He says the PC's name. If reconciled, he says "Little owl." Then he's gone, and the Crown falls empty to the arena floor.

### Arceus speaks
1. Freed, Arceus stands over the arena, whole except for its heart.
2. The PC's shard is pulled gently out of their chest, painless and luminous, and hangs between them and the god beside the Crown's shard.
3. The **Legend Plate is whole** for the first time since AF 0.
4. **Ilsa** (if reconciled) gives Arceus's voice to everyone in the arena:
   > *"Little light. You have carried me far. You may give my heart back, and the rest of me with it. Or you may keep what was borrowed, and wear it, and hold this land quiet in your two hands for a hundred years. I will not take what is not given. I learned that here."*

   (The last sentence is a Ruin Route hint: Arceus is talking about Judgment.)

**The final decision.** The PC speaks (authored), **CHOICE `:ch21_final`**. Availability per NS §6.1:
- **Return** (always): **"Go home. Take them with you."**
- **Keep** (always): **"I'll keep them. I'll keep everyone safe."**
- **Borrowed** (Kestrel Redeemed and devoted, or Sigrun Bond ≥ 6): the PC hesitates, and **Kestrel (or Sigrun) steps forward and takes the Crown**: "Not you. Let me be nearest."
- **Concord** (`VOSS_ACCEPTED`, or Magnus's governor never switched off): **"Stay. Stay and power the world."**
- **Unmake** (Resonance ≤ −6, or Hollow Standing ≥ 4 with Rowan radicalized or Kroll never publicly exposed): **"No. No more gods."**

---

## THE ENDINGS (scenes; the conditions matrix is NS §6.3)

### GOOD: "Homecoming"
1. Arceus takes the eighteen Plates and its heart, and ascends. Light rains on Crownhaven.
2. The Bleed **recedes** across the realm in one long exhale.
3. **The Fixed who still dream wake:**
   - In Verdance, the Bride Tree's blossom falls all at once, and **Elin** opens her eyes in Rowan's arms with Juno beside them, under the first falling leaves Verdance has ever seen. *If Rowan drowned at the Fault,* Juno holds her aunt alone and has to tell her.
   - In the Lowlight, **Dex** blinks, finishes his wave, and says, "—and *that's* why my sister says I talk too much." Rook, standing there in the dark city, laughs until he cries.
   - In Mirefen, Corvin's Quiet Ward sits up.
   - In Lower Crownhaven, the Glassfall Scar's forty breathe again.
4. **The Fixed who stopped dreaming** (Marrowgate's oldest, the long-Fixed of the Quiet Towns) dissolve into soft light. Kaito is there to watch it, at Marrowgate's sealed gate, with his Lucario. He opens the gate.
5. The PC, alone in the arena center, feels something they've never felt: *the ground*. The plain land, with no Imprint at all, **imprints them**. A Meridian scanner left on the floor reads a faint, ordinary color at last.
6. **Voss:** if shielded, he's alive, crippled, and asks to see the sunrise. Otherwise he is light at the arena's center, a man who reached for a god.

**Epilogue** ("One Year Later": Fallmorn, AF 301, the first **Festival of Seasons**). Slides:
- **Juno** in Verdance's first autumn, raking leaves with Elin, and with Rowan if he lived.
- **Kestrel**, Ghost Warden of Gravenmoor (`KESTREL_ACCEPTED_SEAT`), or a Gale Post wanderer.
- **Teo** on the Ebbmouth quay, or his photograph on the Guild wall.
- **Calla's name** on the new Spire memorial, if she went back.
- **Rimeholt** rebuilding on the southern shore, with Anja and Eirik and a thaw-fishery.
- **Cindervault's** forges on coal again. Brann has forged Valen's memorial from the empty Crown's setting.
- **Ossaria:** the caravans walk the western road again, round the Glass Dunes, where the bone-carters keep the newest necropolis in the Bone Sands. Kassan is arrested on the Sandgate steps, and the Elector's Lease is read out among the charges.
- **Lumen** with fewer lights and more stars, and the Zenith Council reformed with **Nadir's first elected seat**. Nyx is in it and hates it.
- **The quarantine:** it lifts now (`ENVOY_PERSUADED`) or a year late, grudgingly. **Edda's** ferry runs again.
- **Bastian** dies peacefully at home: "the first Warden in three hundred years with nothing in his keeping".
- **Celestine** sees her first full night sky in sixty years and starts to age, gladly.
- **The PC** stands at the Ferrow's Landing rail where they arrived, as the first ferry comes in. Edda: "Don't lean on my rail like that, sprog."

### BAD: "The Gilded Chain"
1. The Engine holds. Arceus is bound in gold above Crownhaven, a second sun.
2. The PC, the keystone, sleeps in the cradle, adored as "the Sovereign Who Sleeps", visited by schoolchildren.
3. Zenith blazes. Nadir is cleared. The Bleed stops.
4. The kingdoms kneel, because Meridian owns the light.
5. The final image is the chipped linesman's mug on a desk above the world, steaming. *Quent variant:* the mug is Quent's novelty mug, and **Voss** stands among the visiting schoolchildren's parents, looking up at the PC in the cradle.
6. Credits, then the title screen. There is no post-game.

### GREY: "The Long Vigil" (Keep)
The PC wears the Crown. The Plates sleep quiet. Arceus departs incomplete, sorrowing. The Bleed halts, the Fixed stay Fixed, and the miracles remain. The epilogue is the PC at the next Tuning, ten years later, with the first crystal on their hand. Juno and Kestrel are beside them, swearing to find another door. Post-game: the Warden's Gauntlet is framed as Sovereign's audiences.

### GREY: "Homecoming, Unfinished" (Return, Consent < 12 or Resonance < 2)
The Return happens without enough consent. The unreleased Plates are torn away, and those cities suffer a **Last Shatter**. The rest is Homecoming, but with funerals. The slides show one image per refusing Warden's city, in gym order, using the lines in `11_FINALE_LINES.md` §3. If Resonance was below Harmony, the PC's scar never takes the land's color. It's hard, it's free, and it's ash-grey and hopeful.

### GREY: "The Empty Lighthouse" (Return with Consent and Harmony, but `KESTREL_LOST`)
Everything in Homecoming happens, but Kestrel burned out as the Engine's conduit.
- Hesper climbs the lighthouse every night and lights a lamp nobody needs.
- Ysolde keeps the Ghost seat.
- The PC reads Morwen's letter aloud at Kestrel's grave in Gravenmoor, beside his mother's, for the boy who never opened it.
- Last slide: Kestrel's Aegislash, sheathed, on the PC's belt.

### GREY: "The Hollow Spring" (Unmake, main route)
The PC uses the shard to **break** the Plates. The Imprints die in one night of fire and glass. Arceus, with no Plates to receive, departs wounded forever. Velmora is ruined, and free: nobody will ever rule through a Plate again. Rowan plants the first seed in plain soil, or **Thistle** does if Rowan drowned. Juno doesn't speak to him, or to her. If Teo lived, he's the one who won't. Post-game: partial (Spire and Gauntlet only).

### GREY: "Concord Dawn"
- Arceus is "humanely" half-bound by Magnus's governor and powers the realm.
- The Bleed ends and prosperity booms. The PC sits on the Zenith Council.
- Over the last slide, Celestine speaks in fairy-tale cadence: "Once upon a time a god was kept in a box. It was quiet. For a while."
- **If reached through `:ch21_hand`,** the PC never fought Arceus. The last slide is the PC reading the arena's power output on a Council screen.
- Post-game: partial (Spire only; the Wardens are pensioned off; Quent's Concord Zero arc starts).

### GREY: "The Borrowed Crown"
Kestrel (`KESTREL_BEARS`) or Sigrun takes the Crown in the PC's place. The Plates sleep, and the bearer starts to crystallize. The PC sails home on the first ferry after the quarantine lifts, then comes back every Festival.
- With Kestrel, the last slide is his hand on the rail, beginning to turn to glass, and he's smiling.
- With Sigrun: "Ten years. Maybe twelve. I was relieved once. Never again."

### RUIN: "The Unmaking" / "The One Who Came Back"
Ruin Route only. See **`story/12_RUIN_ROUTE.md`** (R7) and NS §5.4.

---

## POST-GAME HOOKS
Scope by ending (NS §6.5): **full** after Homecoming, Unfinished (refusers are absent from the Gauntlet), Empty Lighthouse, Long Vigil, Borrowed Crown and both Ruin endings. **Partial** after the Hollow Spring and Concord Dawn. **None** after the Gilded Chain.
- **The Concordance Spire** (Battle Tower) in Crownhaven, and **the Warden's Gauntlet**: all eighteen Wardens back-to-back at level 100. In Homecoming their teams no longer use fields, because the Imprints are fading, so it's a "pure" gauntlet.
- **Zygarde chooses the PC** at Valen's memorial (`ZYGARDE_CHOOSES`: Valen Bond ≥ 3 or Ilsa reconciled), completing the Zygarde Cell quest.
- **The Distortion Core** (Antumbra, 910): Giratina's rematch and capture, and the leak in the Glass.
- **Legendary rematches and captures:** Kyogre (Lake Rime), Groudon (Undersands), Zekrom (Stormfront), Reshiram (Wyrmscar, if not with Sigrun), Pecharunt (Lightless Deep), Ogerpon and the Loyal Three (Bride Grove).
- **Shardfall Isles** (905) and the **Hallow Strait** (900/901): the outer islands, where the quarantine began. Bleed remnants are fading.
- **Concord Zero:** **Dr. Quent** escapes with an Engine fragment, the seed of a post-game villain arc.
- **Cameo superbosses** (`design/CAMEOS.md`), all optional: **Lin** (with her lines changed by ending), Garret's Eden rumor near Marrowgate (a deliberate dead end, and a kindness), and level-100 rematches with the earlier cameos.
- **The Ferrow's Landing lighthouse:** Hesper Vane, finally, asks the PC to tell her about her daughter's last night.
