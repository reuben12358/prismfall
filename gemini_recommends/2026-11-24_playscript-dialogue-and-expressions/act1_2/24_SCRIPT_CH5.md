# Script: Chapter 5 — "Ten Years of Light" (the Lock Road, Lumen City, Gym 4, the Gala and the Lowlight Shatter)

> **Final playable script (Playscript & Restrained Rejuv Expressions Edition)** for Chapter 5, the end of Act I (`018_ExpressiveDialogue.rb` v2). It covers the Lock Road out of Ebbmouth (580 the Reedholms, 592 the Icecutters' Haul, 590 Brassfall, 581 the Icefall Locks, 595 Coppice Ride, 594 Wallshadow Row, 593 the Arc-Lamp Mile, 582 Lumen West Gate; optional 584/585 the Voltaic Sluiceworks and 588 Ebb Hollow), Lumen City (180 the Concourse, 181 the Lowlight, the Circuit Gym 190–193, Meridian Spire 185/186 and two new rooms below it), the Lowlight (Shattered) 608, and Interlude I at the Ferrow Lighthouse (105/106). None of these maps is built yet (map builder 15 is building them); **the "Map events needed" list at the end is what to build from.**
> Follows `story/23_SCRIPT_CH4.md` and uses the conventions of `20_SCRIPT_CH0-2.md`.
> Sources: 04_ACT_I Ch5 and Interlude I, 05_ACT_II (the Act II opener), 03_CAST, 09_MYSTERIES (#2, #4, #8, #12–15, #17, #21, #23), 10_CHOICES_ENDINGS / NARRATIVE_KEYS (`:ch5_lowlight_testimony`, GO_LIVE_WIRE), 13_CUTSCENES (portraits), 15_COMEDY (Ch5 "Chat Has Opinions"), 14_WAR_AND_BLESSING, GYM_PUZZLES Gym 4, TRIALS_QUESTS (`ZE_OCTAVE_OFF_BEAT`, `ZE_CUSTOMER_SUPPORT`, `ZE_FIZZBOLT`, `ZE_ROTOM_RECALL`), ROUTES.yaml (the Lock Road), `design/CHAPTER_BEATS.md`.
> **Key events (CHAPTER_BEATS):** 1. **the Lowlight Shatter** (twelve named people Fixed in glass, Dex among them); 2. **Valen sees the PC standing in the glass** and grants Meridian the Mandate, and the PC testifies (`:ch5_lowlight_testimony`). Everything before the Gala is build-up for these: the twelve are met alive on 181 first, and the Plate's empty cradle is seen in Rook's gym. **Nothing comic after the raid starts** (15_COMEDY §1).

## Conventions
- **Playscript Multi-Box Rhythm:** Dialogue is written to be *spoken on stage*, not read as a novel. Each line represents one crisp 1–2 line RPG Maker message box (`<= ~85 chars`), separated into consecutive lines for beats, pauses (`...`), cutoffs (`—`), and listener cut-ins.
- **Restrained Rejuv-Style Expressions** (`014_Portraits.rb` + `018_ExpressiveDialogue.rb` v2 — static `96×96` portraits, `0px` motion, smooth listener dimming):
  - `[portrait: NAME, expression]` = tagged ONLY on a cast speaker's **first line in a conversation** and on **earned emotional turning points** (~20–28% of cast spoken lines). Supported 11 expressions: `neutral, happy, angry, sad, surprised, smug, shocked, panic, blush, crying, deadpan`.
  - `[name: Name]` = **72–80% of cast lines** stay on `[name: Name]`, holding the speaker's current portrait/expression rock-solid via `Portrait.carry`. Also used for all generic NPCs, townsfolk, guards, and route trainers.
  - `\pfe[emote]` = opt-in overworld DS emote balloon (`exclaim, double_exclaim, question, dots, anger, sweat, heart, idea, music, jolt`), **ultra-rare (`0–2` per conversation, ONLY when genuinely earned)**.
  - `[bubble: NAME, expression, emote]` = rare dramatic/comic speech bubble (`0–2` per chapter; never used after the Gala raid begins).
  - **Verified portrait cast in this script** (`graphics/Portraits/` & `Prismfall::Portrait::CAST`): `TEO, JUNO, DEX, ROOK, LARCH, VOSS, VALEN, CALLA, QUENT, HOLLIS, RENATA, THISTLE, MOURNER, SABLE, MARCHETTI, KESTREL, HESPER`.
  - **Plain (`[name: ...]` only):** Cadence and the other Octave singers, P-3NNY, the Lowlight's residents except Dex, every townsperson, guard, and trainer.
- **Gym numbers:** written for readability; events call `Prismfall.gym_battle(pfm_gym(:LEADER_ROOK), double: false)`.
- **Counter:** `V125` **CH5_STEP** (0–13; `design/FLAGS.md` and the map list below).
- **Tone curve inside the chapter:** the road is warm and funny; Lumen is a wow and then a question (the cold cradle, Juno's "How did he know which road you'd come up?"); the Gala is champagne with a crack running under it; from the moment the Gala's lights go grey, **no jokes** until the interlude, which is dry, not funny.

---

# CHAPTER 5 — "Ten Years of Light"

**Chapter start:** V102 = 5 and V124 = 7 (Ebbmouth's towpath gate, Ch4 close). V125 = 0. The PC travels alone until Wallshadow Row.

## Map 580 — The Reedholms (`:SNOWY_MOUNTAIN`; rain)
```
ROAD SIGN: THE REEDHOLMS — The Lock Road. ← Ebbmouth · → the Icecutters' Haul · ↑ the Sluiceworks dam. The boardwalks are re-laid every spring. This spring they weren't.
(Reed islets across the Ebb's delta, joined by boardwalks. Eel-weirs of woven willow across the channels. Rain hisses on the water.)
[name: Eel-weir Keeper] Weirs catch eels when the river runs.
[name: Eel-weir Keeper] When it stops, the eels just sit in them and look at you.
[name: Eel-weir Keeper] (again) Since they blew the intake it's run like a clock.
[name: Eel-weir Keeper] Meridian's still fixing it. I hope they take their time.
```

### EV "A punt on the channel" (touch strip across the main boardwalk, once; only if `pf_choice(:ch4_teo) != :report`)
```
(A reed-cutter's punt slides out of the reeds. The punter has a cutter's hat pulled low, and a Carvanha noses along beside the hull.)
[portrait: TEO, smug] Don't wave.
[name: Teo] You'll make me look like I've got friends.
[if :ch4_teo == :confront]
  [name: Teo] Mari says you sat in the kitchen with her.
  [name: Teo] Nobody sits in the kitchen with her when she's like that.
  [name: Teo] Not even me. ...Thanks.
[if :ch4_teo == :keep_secret]
  [name: Teo] You told the Lattice man you didn't see my face.
  [name: Teo] You were a foot from my face.
  [name: Teo] I owe you. The Hollow pay their debts. Eventually.
  [name: Teo] In eels.
[portrait: TEO, sad] Tell her I'm eating.
[name: Teo] Don't tell her where.
MOVE: the punt slides back into the reeds.
```

**[if `pf_choice(:ch4_teo) == :report`]**
```
WANTED POSTER (smoke hut): "TEO REYES — WANTED — SABOTAGE OF THE MERIDIAN TIDAL LATTICE." Someone has drawn him a moustache. Under it, smaller: "HE PULLED PELLA OUT."
[name: Reed-cutter] Those went up on every hut from here to the Haul.
[name: Reed-cutter] They came down again on every hut, too.
[name: Reed-cutter] Wasn't me. Mostly.
```

```
BLEED VEIL (south bank): A shimmer over a sunken village. Through it, river water hangs in the air in slow round drops the size of houses, and fish swim through them.
[name: Fisher at the Veil] Holmsby. The Ebb took it in AF 296.
[name: Fisher at the Veil] Didn't flood it. Lifted the river clean off its bed and left it hanging.
[name: Fisher at the Veil] My sister's house is in there. Still dry, I'd bet.
[name: Fisher at the Veil] You'll go in? Nobody goes in.
SLUICEWORKS DOOR (sign): VOLTAIC SLUICEWORKS — MERIDIAN CONCORD — DECOMMISSIONED AF 291. DANGER: LIVE.
  Painted beside it in bright pink: "ROOK WAS HERE — EP. 112 'HAUNTED HYDRO' — STAY CHARGED!"
```

### Maps 584/585 — Voltaic Sluiceworks (optional, `:SCRAPYARD`)
```
BUILDER'S PLATE (on the dead turbine): "VOLTAIC SLUICE No. 1 — FIRST LIGHT, AF 289 — DESIGN: I. LARCH, CHIEF ENGINEER."
  Scratched underneath, very small, in no particular hand: SORRY.
CLAPPERBOARD (on the floor): "ROOK CALDER LIVE — EP. 112 — TAKE 41." Forty takes are crossed out.
```
*(The static Rotom on 585, the breaker doors and the Thunder Stone stay as maps.json has them.)*

### Map 588 — Ebb Hollow (optional, `:BLEED`)
```
FIELD NOTES pop-up (first entry): "EBB HOLLOW — BLEED. The Splash Plate's reach has lifted a river off its bed. Water hangs; fish swim in air; the field leans on water. (Larch, in the margin: 'If you're reading this inside it, I'm not speaking to you.')"
INSPECT, a kitchen: A table laid for four, perfectly dry. Above it, filling the room, a drop of river with a trout asleep in it.
INSPECT, a cradle: Empty. A single drop of water the size of a fist hangs over it, turning slowly, like a mobile.
INSPECT, a garden: The beans grew up toward the hanging water and into it. They're still growing, upside down, inside the drop.
INSPECT, a door: A house number, painted by hand: 9. Under it a child's chalk: "WE'LL BE BACK SATERDAY."
```

## Map 592 — The Icecutters' Haul (`:SNOWY_MOUNTAIN`)
```
ROAD SIGN: THE ICECUTTERS' HAUL — The Lock Road. ← the Reedholms · → Brassfall & the Icefall Locks. Sled road: give way to ice.
[name: Picket Captain Hulda] Ice-cutters' union.
[name: Picket Captain Hulda] No ice goes up the Locks to Lumen till Ebbmouth's wheel turns on its own.
[name: Picket Captain Hulda] Lumen puts Isenmar ice in its fancy drinks.
[name: Picket Captain Hulda] Lumen can drink them warm for a week.
[name: Striker] We're on strike for Ebbmouth. Ebbmouth's not even on strike.
[name: Striker] That's solidarity. Look it up.
[name: Mudsdale Driver] The Mudsdale don't strike. They just refuse. It's different.
SAWYER'S CROSS (north gate): FROSTFANG PASS — CLOSED BY ORDER OF THE THANE.
SAWYER'S CROSS (south gate): SNOWBRIAR — CLOSED BY ORDER OF THE QUEEN.
  Chalked between them: "THEY AGREE ON ONE THING."
[name: Meridian Recruiter] Contract Seven! Heat for life! Ask me about Contract Seven!
DROPPED ICE BLOCK (action, once): A block of cut ice that slid off a sled. Something is frozen in the middle of it: a leather satchel with a Meridian sunburst on the flap.
  (Received: ICE-BOUND SATCHEL.) ITEM DESCRIPTION: "Frozen solid. You'd need a boiler."
```

## Map 590 — Brassfall (lock-and-lift town) · 591 Pokémon Center · 596 Union Hall [NEW]

### Arrival (autorun at the lower lock, once)
```
(A town built up the face of a frozen waterfall: lock after lock of brass and timber, each one a step higher than the last, with lift-cages on chains between them. Isenmar ice-cutters in fur, Zenith engineers in brass-buttoned coats, and everyone's breath smoking.)
[name: Lockmaster Garrow] The Locks lift the Ebb's boats onto the Crownland.
[name: Lockmaster Garrow] Or they would, if the boats were moving.
[name: Union Steward Gunnhild] The Locks lift what we cut. Ice goes up, scrip comes down.
[name: Union Steward Gunnhild] Meridian pays us in scrip, and scrip's only good at Meridian's store.
[name: Lockmaster Garrow] It's perfectly good money!
[name: Union Steward Gunnhild] Try buying a pint with it in Ebbmouth.
[name: Lockmaster Garrow] ...I've never been to Ebbmouth.
[name: Union Steward Gunnhild] No. You haven't.
```

```
COMPANY STORE (sign): MERIDIAN COMPANY STORE — SCRIP ONLY.
[name: Store Clerk] Scrip only. ...You haven't got scrip.
[name: Store Clerk] Nobody who isn't from here has scrip.
[name: Store Clerk] I've sold one Potion this year, to myself.
[name: Ice-cutter] Lumen's getting a gala and we're getting frostbite.
[name: Ice-cutter] That's the Lock Road for you. Everything goes uphill.
```

**Optional: "The Ice Elevator"** (the foot of the falls)
```
THE ICE ELEVATOR: A brass lift-cage frozen to its rail. A board: OUT OF ORDER SINCE THE STRIKE.
[name: Lift-boy] It runs off a Cell—
[name: Lift-boy] —and Meridian took the Cells back when the union walked out.
[name: Lift-boy] Give the motor a jolt and it'll go. Anything with a spark in it.
[if an Electric-type is in the party]
  > Let your Pokémon jolt it. → SE: Thunder1. The cage shakes off its ice and grinds upward. (The shortcut to the top of the Locks opens.)
[elif CELL BATTERY in the bag]
  > Use a Cell Battery. → (You lose one CELL BATTERY. The cage shudders and climbs.)
[name: Lift-boy] (after) It goes all the way to the top of the Locks.
[name: Lift-boy] Don't tell the union I fixed a Meridian lift.
[name: Lift-boy] Don't tell Meridian the union let me.
```

**591 — Brassfall Pokémon Center, Gale Post desk** (V125 0 → 1)
```
GALE POST DESK: A letter is waiting, in green ink, with three exclamation marks on the envelope.
"\PN!!!
Uncle Rowan was invited to Meridian's gala in Lumen (the TENTH YEAR OF LIGHT, with AIRSHIPS) and he's got Warden business, again, so he gave me his invitation and said, 'Go and eat their little cakes for me, Juno. All of them.'
He's never once missed a chance to tell Meridian what he thinks of them. I think he's being nice to me. He's been very nice to me lately. It's a bit worrying.
I'm coming down the Prism Falls road. Meet me at the Four Ways on the Crown Road? It's the inn with the signpost that points at four kingdoms. You can't miss it. FOUR KINGDOMS.
— Juno
P.S. The Spewpa evolved. It's a Vivillon now, and it's still rude."
QUEST LOG: "Eighteen Roads" — Meet Juno at the Four Ways on Wallshadow Row, then go on to Lumen.
V125 = 1.
```
*(Fair clue for 09 #2: Rowan gives away his gala invitation for the night the Mourner raids the Spire.)*

**596 — Brassfall Union Hall [NEW]**
```
(Benches, a stove, a notice board, and a boiler that heats the whole hall and most of the street.)
NOTICE BOARD: "SOLIDARITY WITH THE EBB GUILD." · "SCRIP IS NOT MONEY." · "LOST: one (1) Mudsdale. Answers to Mudsdale."
BOILER (action with ICE-BOUND SATCHEL): You prop the satchel against the boiler. It drips for a long time.
  (Received: HEAT CONTRACT (DRAFT).) ITEM DESCRIPTION: "MERIDIAN CONCORD — HEAT SUPPLY CONTRACT 7-B (DRAFT). Party B: the Dominion of Ashkaar. Terms identical to Contract 7 (Isenmar)." In the margin, in pencil: "Don't let the Thane see B."
(Gunnhild reads over your shoulder.)
[name: Union Steward Gunnhild] Contract Seven. That's ours.
[name: Union Steward Gunnhild] That's what keeps Rimeholt's children warm.
[name: Union Steward Gunnhild] And this is the same contract. Word for word. For Ashkaar.
[name: Union Steward Gunnhild] They're selling the same fire to both of them.
[name: Union Steward Gunnhild] Keep that.
[name: Union Steward Gunnhild] Don't show it to an Isenmar man with a drink in him.
[name: Union Steward Gunnhild] Or an Ashkaar man with a sword. Or anybody, really.
```
*(War seed, 09 #29 and 14_WAR Ch12: the Larch Papers put the two heat contracts side by side. If the PC has this, Larch can cite "the draft you brought me from Brassfall" in Ch12.)*

## Map 581 — The Icefall Locks (`:SNOWY_MOUNTAIN`)
```
ROAD SIGN: THE ICEFALL LOCKS — The Lock Road. ↓ Brassfall · ↑ Coppice Ride & the Crownland. Isenmar ends at the top. So does the ice.
(The Ebb comes off the Crownland downs here and falls into Isenmar in a staircase of frozen falls. Zenith's engineers cut locks into the ice and brass sluices into the rock. A Lattice pylon stands on every terrace, humming.)
```

**Extraction Lattice No. 4** (the fenced terrace)
```
PLATE (sign): "MERIDIAN CONCORD — EXTRACTION LATTICE No. 4 (ICEFALL). COMMISSIONED AF 289. DESIGN: I. LARCH, CHIEF ENGINEER. LIGHT FOR EVERYONE."
[name: Linesman Tolly] Number Four. Eleven like her in the realm, and she was the second one built.
[name: Linesman Tolly] The Professor's own drawing. Larch. Before she went soft.
[name: Linesman Tolly] Know her? ...Course you do.
[name: Linesman Tolly] Everybody who comes up this road with that look on them knows her.
[name: Linesman Tolly] (again) They say she cried at the switch-on.
[name: Linesman Tolly] Happy tears, I always thought. I'm less sure now.
THE FALL UNDER THE PYLON (inspect): Everywhere else on the Locks the falls are frozen solid. Here, in a ring round the Lattice, the ice is clear as glass, and behind it the water is running. It's melting from the inside.
```

```
ICE CAVE (behind the third lock gate; secret): A maintenance ledger on a nail.
  "Lumen grid. Zap feed diverted to Spire vault for 'anniversary load test'. Draw x3 nominal, sustained. Cradle temperature: HIGH. Recommend inspection. — Inspection deferred. P.Q., R&D."
  Next line, a different pen: "Deferred again. P.Q."
  Next: "Deferred. P.Q. (Don't ask.)"
BORDER POST (top of the falls):
[name: Elowen Forester] Crown Road country from here. Elowen soil, the Accord's road.
[name: Meridian Guard] And Meridian's pylons. Welcome to all three.
```

## Map 595 — Coppice Ride (`:MEADOW`)
```
ROAD SIGN: COPPICE RIDE — The Crownlands (Elowen). ← the Icefall Locks · → Wallshadow Row & the Crown Road. Cut every seventh year since the Accord.
(Hazel coppice in panels, each a different age: fresh stumps, then shoulder-high, then over your head. The air is warmer. The ice is behind you.)
[name: Woodward] Seven panels, seven ages.
[name: Woodward] You cut one a year—
[name: Woodward] —and by the time you're back round to the first it's grown again.
[name: Woodward] That's coppice. It's the only kind of forever I trust.
[name: Kingsferry Ferryman] Kingsferry. A copper a crossing.
[name: Kingsferry Ferryman] Nobody's paid me in a copper since the Accord, but I still say it.
UNCUT PANEL (secret): A panel nobody has cut since AF 0. Inside, a ring of old stools as wide as tables, and in the middle a seed somebody dropped and never planted. (MIRACLE SEED.)
```

### EV "The First View of the Crownwall" (touch strip in front of the ride-side shrine, once) [NEW]
```
(The ride climbs out of the coppice onto a bare shoulder of down. A shrine stands at the edge: a stone post and an offering bowl with eighteen coloured pebbles in it, and one clear one.)
MOVE: the screen scrolls north, slowly.
(On the horizon a ring of white peaks stands up out of the green Crownland, sheer as a wall, enormous, snow on its rim. Inside the ring, very small and very far away, the glint of towers.)
[name: Pilgrim] The Crownwall. Crownhaven's inside it.
[name: Pilgrim] Every road in Velmora goes round it and none of them go in.
[name: Pilgrim] Not without eighteen badges, or a Sovereign's seal.
(Something under your ribs aches. Not a pain. Like a bell somebody struck a long way off, and you're only hearing it now.)
WAIT 40.
(The PC's hand goes to their chest.)
> (Read Mum's letter.)
  "...Don't let anyone scan you. Don't go to Crownhaven. I'm sorry I never told you why..."
  (You read the line twice. You fold the letter away.)
> (Look at the wall.)
  (You look at it for a long time. It doesn't look back. You're nearly sure.)
[name: Pilgrim] Ten years ago there was a light in there you could see from here.
[name: Pilgrim] Festival night. Then it went out and the stories started.
[name: Pilgrim] You look like you've heard them.
```

## Map 594 — Wallshadow Row (`:MEADOW`; the Crown Road)
```
ROAD SIGN: WALLSHADOW ROW — The Crown Road. ← Coppice Ride · ↓ the Arc-Lamp Mile & Lumen · → Candle Down · ↑ Kingsmead. Mind the tithe-reeve.
(Farms in the Crownwall's shadow: hedged fields that get sun for half the day, tithe barns with the Accord's eighteen-and-one carved over the doors, and the paved Crown Road with a numbered milestone every mile, running round the foot of the wall.)
MILESTONE XVII: "THE CROWN ROAD — XVII. Southgate 1."
MILESTONE XVIII: "XVIII. SOUTHGATE. Crownhaven: no road."
[name: Tithe-collector] A tithe for the Accord, a tithe for the Queen. Both take a tenth.
[name: Tithe-collector] Farmers here keep eight. They used to keep nine. Ask me how I sleep.
[name: Farmer] Half the sun, all the tithe.
[name: Farmer] My barley's the best in Elowen because it's had to try.
FOUR-KINGDOM SIGNPOST (the Four Ways): ← ISENMAR (THE LOCKS) · ↑ ELOWEN (VERDANCE, BY PRISM FALLS) · ↓ ZENITH (LUMEN) · ↘ NADIR (THE LONG DROP). A fifth arm has been nailed on, pointing at the Crownwall. It's blank.
```

### EV "Juno at the Four Ways" (touch, the inn yard; V125 <= 1 → 2) [NEW]
```
(Juno is sitting on the inn's mounting block in her blossoms and veil, with a hatbox on her knees, eating a pie with great concentration.)
[portrait: JUNO, happy] \PN! You got my letter! You came!
[name: Juno] I've been here two hours. I've had three pies.
[name: Juno] The innkeeper thinks I'm a bride waiting for someone who isn't coming.
[portrait: JUNO, deadpan] I didn't correct her. She gave me the third pie free.
[name: Juno] The hatbox isn't eggs this time. It's a dress for the gala.
[name: Juno] Mum made it out of a curtain. It's a very good curtain.
[name: Juno] Uncle Rowan says hello. And "be careful in Lumen".
[name: Juno] And "don't eat anything that glows". Which is all of Lumen, so.
> How is he?
  [name: Juno] Busy. Warden business.
  [name: Juno] He went off the morning I left with his Phantump and his big coat.
  [name: Juno] Wouldn't say where. He never says where.
  [portrait: JUNO, sad] He held my face before he went. Like this.
  MOVE: Juno puts both hands on your cheeks, very gently, the way you'd hold something that might spill.
  [name: Juno] And he said, "You're going to be braver than all of us."
  [name: Juno] Then he left.
  [name: Juno] He's very dramatic, for a gardener.
> Did you tell him about the Pageant?
  [name: Juno] I did. He laughed and said "Ask your Warden!"—
  [name: Juno] —because he IS a Warden, you see.
  [name: Juno] And then he stopped laughing in the middle.
  [portrait: JUNO, sad] I think everyone in Verdance is pretending not to know something.
  [name: Juno] I'm going to find out what.
> ...
  [name: Juno] You're doing the silence. I missed the silence.
  [name: Juno] Kestrel just shouts at it.
[portrait: JUNO, happy] Come on! Lumen! Ten years of light!
[name: Juno] I've never been anywhere with an airship!
(Juno becomes a follower.)
V125 = 2.
```

```
PRISM FALLS ROAD (west, closed):
[name: Royal Forester] The Verdance road. The Queen's road, by the Queen's leave.
[name: Royal Forester] Pass, or no passage.
[portrait: JUNO, deadpan] *(if follower)* I came DOWN it. It only works one way.
[name: Juno] That's Elowen for you.

KINGSMEAD (north, closed):
[name: Tithe-reeve] Kingsmead's the Accord's paddocks.
[name: Tithe-reeve] Nobody past the reeve without a seal. I'm the reeve.

THE LONG DROP (south-east, closed):
(A great lift-shaft dropping off the edge of the plateau into the dark. The cage is chained at the top.)
[name: Lift Guard] The Long Drop. Down to Nadir.
[name: Lift Guard] Nobody's going down this week. Gala week.
[name: Lift Guard] ...You don't want Nadir anyway. Nadir comes up to you.

CANDLE DOWN (east, closed until Rook's badge):
[name: Road-mender] Crown Road east is up for mending. Back in a month.
[name: Road-mender] It's been back in a month since spring.
```

**The Southgate shrine** (south junction)
```
(A small stone chapel where the Crown Road meets the road down to Lumen. Over the altar, a round window: eighteen panes of coloured glass around one clear pane.)
PRAYER BOARD: "...that the Eighteen keep their peace, and the land its shape, and the Sovereign his strength; and keep the One."
[name: Shrine-keeper] "And keep the One." Every prayer ends that way.
[name: Shrine-keeper] I've said it forty years. The Choir says it means the Sovereign.
[name: Shrine-keeper] My gran said it meant the Ogre. Nobody's ever told me to my face.
WINDOW (inspect): The clear pane in the middle catches the sun and throws it on the floor as a small colourless star.
[portrait: JUNO, neutral] *(if follower)* There's one of these in the Heartgarden chapel.
[name: Juno] The clear pane's the only one that never needs cleaning.
[name: Juno] Uncle Rowan says it's because there's nothing on it to see.
```

## Map 593 — The Arc-Lamp Mile (`:NEON_GRID`)
```
ROAD SIGN: THE ARC-LAMP MILE — ↖ Wallshadow Row · ↘ Lumen City (West Gate). One hundred lamps. Count them. Everybody does.
(A straight paved road out of the orchards toward a city on a cliff. An iron lamp every few yards on both sides, each with a brass number. Clockwork pickers tick through the apple rows.)
[portrait: JUNO, happy] The clockwork pickers! Little brass hands!
[name: Juno] They're — oh. They're picking the green ones too.
[name: Juno] That's wrong. Somebody should tell them.
HOARDING: "LUMEN — TEN YEARS OF LIGHT — AF 290–300 — MERIDIAN CONCORD."
HOARDING: "THE FESTIVAL OF CHAMPIONS — AF 300 — AT THE NEW MERIDIAN PRISM ARENA, CROWNHAVEN. EIGHTEEN PLATES. ONE CHAMPION. LIGHT FOR EVERYONE."
HOARDING: "THE MERIDIAN FELLOWSHIP — WE INVEST IN THE YOUNG." A painted young trainer holds up a badge case.
  [if :pro_fellowship == :accept] The painted badge case looks exactly like yours.
[name: Depot Keeper] We don't light them any more. They light themselves. We polish them.
[name: Depot Keeper] A lamplighter who only polishes is a polisher. I'm keeping the title.
TRAM STOP (sign): LUMEN TRAMWAY — STOP 3. There are no rails.
[name: Man at the Tram Stop] It's late.
[name: Man at the Tram Stop] (again) It's been late for six years.
[name: Man at the Tram Stop] I'm not leaving now. I've too much invested.
```

**LAMP 47** (action; two pages)
```
Lamp 47. The only dark one on the Mile. The glass is clean. Someone still polishes it.
> Look under the base plate?
  The plate unscrews. Inside, on a wire, an engineer's brass tag:
  "No. 47. FAULT: none found.
   Went dark 23:40, Festival night, AF 290. Every lamp on the Mile dipped at once for nine seconds. 46 came back. 47 didn't.
   Draw spike on every grid in Zenith, same second. Source: not ours?? Refer to Chief Engineer. — L.G."
  Under it, scratched in another hand: "Referred. Referred again. Stop asking. — Spire."
  [portrait: JUNO, sad] *(if follower)* Festival night, ten years ago. That's the Glassfall.
  [name: Juno] Everybody's mum remembers where they were.
  [name: Juno] Mine was in Verdance, holding me. I was five.
  [name: Juno] I don't remember it. I only remember her holding me too tight.
```
*(09 #9 mid clue, kept vague: something drew on every grid at the second the Crown cracked. L.G. is Lisle Garrow, Brassfall's lockmaster, who was the Mile's engineer then. Nobody says "Crown" or "cracked".)*

## Map 582 — Lumen West Gate
```
(A brass-and-glass gatehouse. A Meridian Security officer at a scanner plate.)
[name: Meridian Security] Lumen West Gate. Hand on the plate, please. Tint check.
[name: Meridian Security] It's the anniversary; we're being thorough.
MOVE: Juno puts her hand on the plate. SE: chime. The bar glows green.
[name: Meridian Security] Meadow tint, Verdance. Welcome.
MOVE: your turn. SE: chime... nothing. The bar stays dark. Then a word scrolls across it: NULL.
[name: Meridian Security]\pfe[question] ...That's a new one. Hold on.
(He speaks into a brass tube on the wall. A voice answers, small and tinny. He straightens up very fast.)
[name: Meridian Security] You're on the Chair's list. Personally.
[name: Meridian Security] Gala guest, tomorrow night, at the Spire.
[name: Meridian Security] And this came for you. It's been waiting a week.
[name: Meridian Security] I was told you'd come up the Lock Road.
(Received: GALA INVITATION.) ITEM DESCRIPTION: "Meridian Concord requests the pleasure of your company at the Tenth Year Gala, Meridian Spire, Lumen City. Guest of the Chair." Under the print, by hand: "I'd like to hear how you're finding the place. — A.V."
[bubble: JUNO, shocked, exclaim] You're on a LIST?
[name: Juno] I'm on Uncle Rowan's list.
[name: Juno] You're on a list with your own NAME on it.
[portrait: JUNO, neutral] ...How did he know which road you'd come up?
V125 = 3.
```
*(09 #14: nobody answers Juno. The badge case is the answer, in Ch14.)*

## Map 180 — Lumen City, the Concourse

### Arrival (autorun, first entry, V125 == 3)
```
BGM: Lumen's theme, brass and synth.
(White-stone boulevards between towers of glass and brass. Holograms of the Meridian sunburst turn slowly over the plaza. Rotom drones zip overhead with parcels. An airship slides across the sky, so low its shadow crosses the fountain. Every window is lit, and it's noon.)
[portrait: JUNO, shocked] ...
[name: Juno]\pfe[exclaim] Everything's ON. Everything's on at the same TIME.
[name: Juno] In Verdance you light a lamp when it gets dark and you're careful with it.
[name: Juno] Here they've just left everything on. Like it's free.
[name: Pin-seller] It IS free! Ten years of free! Light for Everyone!
[name: Pin-seller] Anniversary pins, only ₽200!
[portrait: JUNO, deadpan] The light's free. The pin's two hundred.
BANNER (over the plaza): TEN YEARS OF LIGHT.
```

```
CIRCUIT GYM (door, until V125 >= 5): CLOSED FOR FILMING. "Warden on location: THE LOWLIGHT. Stay charged! — R.C." A hologram of Rook winks at you. It's on a loop. It winks every four seconds.
```

**The grille** (one scene; touch near the grille, once)
```
LIFT-GRILLE (inspect): A grille in the pavement over a shaft that goes down out of sight. The air coming up is warm and tastes of pennies. Painted on the inside of the bars, where you'd only see it looking down: a grey ring, broken at the top.
(A Nadir kid in a cut-down boiler suit is sitting on the grille. A Zenith officer in white-and-gold walks up.)
[name: Zenith Officer] You. Back downstairs.
[name: Nadir Kid] I'm just sitting.
[name: Zenith Officer] Sit downstairs.
MOVE: the kid drops through a gap in the bars and is gone.
[portrait: JUNO, angry] He wasn't doing anything!
[name: Zenith Officer] It's the anniversary, miss.
[name: Zenith Officer] Nadir's very welcome to watch the fireworks. From Nadir.
```

**Flavour townsfolk**
```
[name: Office Worker] I haven't seen the stars in ten years. I don't miss them.
[name: Office Worker] I can see the Spire from my bed.

[name: Old Man] I remember Lumen before the Lattice. Gas lamps and smog.
[name: Old Man] It was worse. I just liked it more.

[name: Airship Spotter] That's the Sallow Line's Dauntless. Then the Meridian Courier.
[name: Airship Spotter] Then — no, that's a cloud. They're getting hard to tell apart.

[name: Rotom Drone] (bzzt) PARCEL FOR: NOT YOU. (bzzt)

[name: Tourist from Briarwick] Everything's so bright I keep thinking it's morning.
[name: Tourist from Briarwick] I've had four breakfasts.

[name: Meridian Lineman] The Spire's lit gold for the gala.
[name: Meridian Lineman] You can see it from the Crownwall, they say.
[name: Meridian Lineman] And the Sovereign's coming. Valen Corrigan. HERE.

[name: Street Performer] Neon Grid's in the pavement, kid. Every cobble's on the circuit.
[name: Street Performer] Electric moves sing here, and anything that conducts sings louder.
```
**Trials hooks in Lumen (TRIALS_QUESTS, Ch5):** The Machine Wants Compliments (`ZE_FIZZBOLT`, the Concourse vending machine) · Product Recall (`ZE_ROTOM_RECALL`, the Arcade 183) · Customer Support (`ZE_CUSTOMER_SUPPORT`, the Spire lobby 185) · **Off the Beat** (`ZE_OCTAVE_OFF_BEAT`, Cadence on the Lowlight steps, Octave 3 of 8; must be done before the Gala, see the map list).

## Map 182 — Lumen Pokémon Center: Gale Post desk (on arrival)
```
GALE POST DESK: "I've been invited to the Spire's gala. I am not going. There is nothing in that building I want to see again. — I.L."
(Received: KELP TEA BAG. "Four. She's not even pretending these are a joke any more.")
```

## Map 181 — Lumen City, the Lowlight (before the Shatter)
```
(The Lowlight: the streets at the Spire's foot, where its shadow falls all day. Stacked tenements with washing lines strung between them, steps going down, a noodle cart, a hopscotch chalked on the stones. It's dimmer down here. The Spire is so tall and so close that it's the whole sky.)
```

### EV "Dex" (top of the Lowlight stairs; touch, V125 == 3 → 4)
```
(A boy of about eleven with a soda crate on his hip and a Pichu on his shoulder, shouting at nobody in particular.)
[portrait: DEX, happy] FIZZBOLT! Fizzbolt, ice-cold, colder than the Thane's heart!
[name: Dex] You two! You're new! You've got new faces!
[name: Dex] I'm Dex. That's Spark. Spark makes them cold. Watch.
(The Pichu lays a paw on a bottle. SE: a tiny zap. Frost blooms up the glass.)
[portrait: JUNO, happy] That's AMAZING.
[name: Dex] Fifty a bottle. Thirty for you, because you said "amazing".
[name: Dex] Nobody says "amazing" down here. They say "how much".
(Received: FIZZBOLT ×2. You pay ₽60.)
[name: Dex] You want the best airship view in Lumen? Not the Skyport.
[name: Dex] Everyone goes to the Skyport. The laundry roof, there.
[name: Dex] You get the Spire's top and the Crownwall—
[name: Dex] —and the Dauntless coming in, all at once.
[name: Dex] My sister Marlo works the night lift down to Nadir.
[name: Dex] She says one night the cage didn't stop at the bottom.
[name: Dex] It went right on down past it, into the old—
SE: a bell from the Spire, striking the hour.
[portrait: DEX, shocked]\pfe[exclaim] That's the hour! The crew'll want their sodas!
[name: Dex] Rook's filming down here today, did you know?
[name: Dex] ROOK CALDER. In the LOWLIGHT.
[portrait: DEX, happy] Tell you the rest tomorrow!
MOVE: Dex runs down the steps with the crate, Spark clinging to his ear.
V125 = 4.
```

**The Lowlight's residents** (each a separate event; *these are the twelve, at the spots their glass figures will stand on 608*)
```
(Marta Vell is pegging out washing between two windows.)
[name: Marta Vell] Mind the sheets, love. Everything I own is on this line.
[name: Marta Vell] Including my husband's dignity.
(A pair of very large long johns.)

(Old Jory, the cobbler, laughing on his step.)
[name: Old Jory] Hah! Rook Calder in the Lowlight!
[name: Old Jory] Ten years that Spire's been up there, first time it's sent anybody DOWN.
(He laughs till he coughs.)

(Nessa, on the hopscotch.)
[name: Nessa] You can't stand on seven. Seven's the Spire.
[name: Nessa] Everybody knows you can't stand on the Spire.

(Hob Carrow, the lamp-tender, up a ladder.)
[name: Hob Carrow] These are the old gas lamps.
[name: Hob Carrow] The Lattice ones don't reach the Lowlight; the shadow eats them.
[name: Hob Carrow] So I light ours by hand, every dusk.
[name: Hob Carrow] Ten years of light! Not down here.

(Linesman Aldo Fisk, helmet under his arm.)
[name: Linesman Aldo Fisk] Twelve-hour shift on the Spire feeds.
[name: Linesman Aldo Fisk] They've had the Plate vault running hot all month for the gala.
[name: Linesman Aldo Fisk] My hands still hum. Listen.
(He holds out his hand. It does, faintly.)

(Sukie, the lift-girl at the Nadir grille.)
[name: Sukie] Lift down's at six, love, checkpoint or no checkpoint.
[name: Sukie] Tell your friend in the flowers to hold her skirts, the draught's terrible.

(Ilo and Mattie on a doorstep, holding hands.)
[name: Ilo] We got married Tuesday.
[name: Mattie] He keeps telling people.
[name: Ilo] I'll stop telling people when I stop being married.
[name: Mattie] ...That's a very long time.
[name: Ilo] That's the idea.

(Gran Osk, feeding a Pidove.)
[name: Gran Osk] Forty years I've fed the birds in the Spire's shadow.
[name: Gran Osk] Same birds, I'm sure of it.
[name: Gran Osk] Look at that one. He's got my late husband's face.

(Benno at the noodle cart.)
[name: Benno] Slag-fried noodles! Nadir recipe, topside prices!
[name: Benno] That's a joke. They're Nadir prices.
[name: Benno] Nobody topside buys noodles in the shadow.

(Mr Imrie, a schoolteacher on a bench, marking.)
[name: Mr Imrie] "What does light mean to you?" For the anniversary.
[name: Mr Imrie] Eleven of my pupils wrote "free".
[name: Mr Imrie] One wrote "my mum's face when she gets home".
[name: Mr Imrie] Guess which one gets the prize.
```

### EV "Rook's shoot" and the blackout (the crew's square; touch, V125 == 4 → 5)
```
(Floodlights on stands, cables everywhere, a boom mic, a director in a scarf. In the middle of it all, a young man with a bleached undercut in a jacket whose back scrolls STAY CHARGED in lights. A Rotom drone with a camera hovers at his shoulder. Dex is handing round sodas.)
[portrait: ROOK, happy] —and THIS is the Lowlight, chat! The REAL Lumen!
[name: Rook] Ten years of light, and tonight we've brought it all the way down here—
[name: Director] Rook. You're blocking the noodle cart.
[name: Rook] —brought it all the way down here AND we're supporting local noodles!
[name: Rook] Hi, Benno! Chat loves Benno!
[name: Benno] I don't know what that means!
[portrait: DEX, happy] Rook! Your sodas! That's eleven you owe me now.
[name: Dex] Chat owes me eleven.
[name: Rook] Chat, pay the man! ...Chat says it'll pay you in exposure.
[name: Rook] Chat is a terrible person, Dex.
(He sees you.)
[portrait: ROOK, neutral] Oh. Challengers. Hi. Gym's shut, sorry.
[name: Rook] The Spire wanted a "community special".
[name: Rook] And when the Spire wants a thing, the thing happens.
[name: Rook] Chat says you look tired. Chat says—
SE: a fizzing crackle. Every floodlight on the square flares white at once.
[name: Director] Rook, we're pulling too much off the—
(The floodlights die. Then the street lamps. Then every window, block by block. The Lowlight goes black. Somewhere a Pidove panics.)
[portrait: ROOK, panic]\pfe[jolt] —CHAT? Chat, are you there? Rotom, are we live?
[name: Rotom Drone] (bzzt) ...signal lost.
[name: Rook] We're not live. We're not LIVE.
[name: Rook] I haven't been not-live since I was fourteen.
(In the dark, the junction boxes on the street corners start to glow from the inside, one after another. Something in each of them is giggling.)
[name: Hob Carrow] *(from his ladder)* Rotom! The floods pulled 'em out of the Spire feed!
[name: Hob Carrow] They're in the boxes, they'll drink the whole block!
[name: Rook] Okay. Okay. I can do this. This is fine. This is content.
[name: Rook] I can't do this, my drone's dead.
[name: Rook] You. You've got Pokémon that aren't plugged into anything, right?
[name: Rook] Boxes. Corners. GO.
```
```
JUNCTION BOXES (four; action each → WILD BATTLE: ROTOM Lv 24, catchable, field :NEON_GRID; the fourth, the feed-line box by the Spire's service door: ROTOM Lv 26):
  (after each) The glow goes out. The box hums normally. Somewhere a window comes back on.
(When all four are done:)
SE: the hum of a whole block coming back. The floodlights flicker up, then the lamps, then the windows. The Lowlight cheers.
[portrait: ROOK, happy] We're back. WE'RE BACK. Chat! Chat, are you— (bzzt)
[name: Rook] —chat is saying "WHAT HAPPENED".
[name: Rook] Chat, you would not BELIEVE what happened.
(Quieter, with the drone pointed away:)
[portrait: ROOK, neutral] Thanks. Really. I'm not good in the dark.
[name: Rook] Nobody up there's good in the dark.
[name: Rook] That's kind of the whole problem with up there.
[name: Rook] Gym's open! Circuit Gym, west side of the Concourse.
[name: Rook] Come and lose on camera. It's the best way to lose!
[portrait: JUNO, happy] He's lovely! Is he always like that?
[portrait: ROOK, deadpan] Chat says yes. Chat says I'm "a lot".
V125 = 5.
```
**Optional: "Off the Beat"** (Trials; Cadence drumming on paint tins at the bottom of the steps; TRIALS_QUESTS scenes as written. Plain name box for Cadence.)
```
SERVICE DOOR (by the fourth junction box): A steel door in the cliff under the Spire. "MERIDIAN CONCORD — AUTHORIZED PERSONNEL." Locked. It's warm.
```

## Maps 190–193 — the Circuit Gym (Gym 4; built from GYM_PUZZLES Gym 4)
```
[name: Gym Guide] The Circuit Gym! Electric-types on the Neon Grid.
[name: Gym Guide] Ground-types laugh at Rook. He knows. He's made three videos about it.
[name: Gym Guide] The puzzle's power: turn the nodes, light the doors.
[name: Gym Guide] The tees split power three ways, so make sure the third way's a wall.
[name: Gym Guide] And never, ever light the camera lamp. Rook's camera is the alarm.
```
*(Spark the apprentice's hints, the Switchroom, the Breadboard Hall and the Live Wire Hall as GYM_PUZZLES; trainers as built.)*

**193 — the cold cradle** (before the arena door) [CHANGED PA line]
```
PLATE CRADLE: A cradle of brass and crystal on a plinth, where a Warden's Plate should sit. It's cold. There's dust in it. A thick Meridian cable runs past it into the floor, warm to the touch.
[portrait: JUNO, neutral] ...Where's the Plate?
[name: Juno] Uncle Rowan's sits in the Heartgarden where anyone can see it.
[name: Juno] It's warm. It hums at you.
[portrait: JUNO, sad] This is just a chair nobody sits in.
SPLICE NODE (action): You turn the last node onto the Meridian main. The arena door opens. In the corner of the ceiling, the drone's red light has been on the whole time.
PA (Rook's voice; not his stream voice): Rotom. Cut the feed. ...That bit's not for chat, buddy. Cut it.
```

**193 — Rook** (the Core)
```
(The Core: a round arena under a dome of live conduit, all of it lit. Rook stands on a glowing disc in the middle, his drone at his shoulder. In the viewing gallery behind the glass: Juno, waving with both arms, and a grey-braided woman in an oilskin with a flask, who is not waving.)
[portrait: LARCH, deadpan] *(in the gallery, on the PA)* I'm not here for the gala.
[name: Larch] I'm here to stop you licking a Lattice.
[name: Larch] Those are different things.
[portrait: ROOK, happy] Welcome to the stream! Chat, say hi to the challenger!
[name: Rook] Chat says hi. Chat says you look tired. Chat says drink water.
[name: Rook] Chat also says I'm gonna sweep you six-nil.
[name: Rook] Chat says you're cute. Chat also says you're gonna lose.
[name: Rook] Chat's wrong a lot. Let's see which bit.
[name: Rook] Neon Grid's live! Every circuit in this room is on my side.
[name: Rook] Stay charged, Lumen!
Script: Prismfall.gym_battle(pfm_gym(:LEADER_ROOK), double: false)     # LEADER_ROOK, :NEON_GRID, cap 27, single
(When his ace enters:)
[name: Rook] Camera, you're up! Get my good side!
[name: Rook] ...They're both good sides!
(LOSE: standard whiteout. Rook on retry: "The comeback arc! Chat LOVES a comeback arc!")
(WIN:) — comedy scene Ch5, "Chat Has Opinions"
[portrait: ROOK, deadpan] ...Chat is now saying they "always believed in the challenger".
[bubble: ROOK, angry, anger] You LIARS! I have the LOGS!
[name: Larch] He's arguing with a hat with a camera on it.
[portrait: ROOK, shocked] Chat, the tea lady's roasting me.
[name: Rook] Chat? Whose side are— CHAT.
(Received: the ARCLIGHT BADGE.)
(The PC sets it into the case. SE: the first note, the second, the third... and a fourth, and all four together. This time the case doesn't just hum. A thin, colourless light runs along every seam of it.)
[name: Rook]\pfe[exclaim] Whoa. WHOA. Rotom, get that. GET THAT.
(The drone swoops in close on the glowing case.)
[name: Rook] Is that a special edition? Chat wants one. Chat wants six.
[portrait: JUNO, shocked] It's never glowed before.
[name: Juno] It hummed in Saltmere. It did a chord in Briarwick—
[portrait: LARCH, neutral] *(very quietly, to nobody)* Four.
(Received: TM43 VOLT SWITCH. Received: TM70 FLASH.)
[portrait: ROOK, neutral] Volt Switch: hit and run, very me.
[name: Rook] Flash, so you can see in the places I can't.
[name: Rook] And that badge means Pokémon up to level thirty-one'll heed you.
[name: Rook] You're coming to the gala, right?
[name: Rook] I have to stand next to the Chair and smile for ninety minutes.
[name: Rook] Come and stand next to me so I've got somebody to smile AT.
V125 = 6.
```
*Larch, in the Core's lobby after:*
```
[portrait: LARCH, neutral] I'm going to the gala.
> You said you weren't.
  [name: Larch] I'm going to stand by the canapés and look disapproving.
  [name: Larch] It's a skill. It takes years.
> Why?
  [portrait: LARCH, sad] Because that case did something in there it's never done.
  [name: Larch] And the man who gave it to you is going to be in the room.
> ...
  [name: Larch] Don't look at me like that.
  [name: Larch] I own one formal oilskin and I'm going to wear it.
```

## Map 185 — Meridian Spire, Lobby (the Gala night)
```
[name: Receptionist] Invitation? ...Guest of the Chair. Of course.
[name: Receptionist] The lift's on the left; the Gala's at the top.
[name: Receptionist] Please don't touch the exhibits. Please don't touch anything.
PLAQUE: "MERIDIAN SPIRE. Raised AF 271 by Meridian Concord on the foundations of the old Aurelian sun tower, the first stone of Zenith."
ARENA MODEL (under glass): A great white bowl of an arena in a ring of mountains, a brass ring round its rim and eighteen slim pylons. "THE MERIDIAN PRISM ARENA. Crownhaven's ancient Temple-Arena of the Blessing, rebuilt for the Festival of AF 300 by Meridian Concord. Eighteen Plates. One stage."
[portrait: JUNO, neutral] Eighteen pylons. Like Lattices.
[name: Juno] ...Why does an arena need pylons?
```

## Map 186 — Meridian Spire, Gala Hall: **EV "The Tenth Year Gala"** (autorun on entry, V125 == 6 → 7)
```
BGM: a string quartet playing something expensive.
(The top of Meridian Spire: a hall of glass and gold with all of Lumen lit up below the windows and airships moored outside at eye level, their lamps blinking. On the east side a great window looks down into the Spire's atrium shaft, and far down at the bottom of it, something black glows. A replica of a golden Plate turns slowly in a glass case on a plinth.)
(Guests in Zenith brass, Elowen green and Isenmar fur. Rook in a suit that lights up. Juno in a dress made out of a very good curtain. Larch in her oilskin.)
[portrait: LARCH, deadpan] I was told "formal". This is my formal oilskin.
(Free roam. Talk to the guests; the speech starts when you've spoken to Voss and to Larch at the display case, or after a while.)
```

**Voss** (by the window, with his chipped mug)
```
[portrait: VOSS, happy] \PN. You came. I hoped you would.
[name: Voss] How are you finding the place? Honestly.
[name: Voss] Everyone tells me "wonderful"—
[name: Voss] —and I can never tell if they mean it.
> It's wonderful.
  [name: Voss] You mean it. Good.
  [name: Voss] I can tell, with you. I don't know why.
> It's very bright.
  [portrait: VOSS, neutral] It is. Too bright, my mother used to say.
  [name: Voss] She grew up downstairs.
  [name: Voss] She said up here we've forgotten what the dark is for.
> ...
  [name: Voss] The quiet ones always see the most. Keep doing that.
[if :pro_fellowship == :decline]
  [name: Voss] You turned the Fellowship down. I still think about that.
  [name: Voss] Nobody turns me down. It was refreshing.
[if :pro_fellowship == :accept]
  [name: Voss] The Fellowship's treating you well? Good.
  [name: Voss] Spend it on Potions, not pins.
[portrait: VOSS, neutral] How's the badge case holding up?
[name: Voss] We had complaints about the hinges on that batch.
> It's fine.
  [name: Voss] Good. Good. Tell me if it ever does anything odd.
> It sings.
  [name: Voss] ...Does it.
  [name: Voss] The brass does that, in the cold.
  [name: Voss] Isenmar, wasn't it? Lovely country. Terrible for brass.
[name: Voss] I have to go and make a speech.
[name: Voss] I hate making speeches. I'm very good at it, which is worse.
```

**Valen** (alone at the far window; grey glove on his left hand)
```
(A broad, white-haired man in white robes, with a soldier's back and a grey glove on one hand. People leave a space around him without meaning to.)
[portrait: VALEN, neutral] ...You're the challenger. Four badges, as of this afternoon.
[name: Valen] The Accord keeps a list.
[name: Valen] Valen Corrigan. You'll have seen my face on the posters.
[name: Valen] It's older than that now.
> Sovereign.
  [name: Valen] "Valen" will do, in a room this loud.
> Why are you here?
  [name: Valen] Because Lumen asked.
  [name: Valen] And the Accord doesn't refuse Lumen anything this year.
  [name: Valen] Draw your own conclusions. Quietly.
> ...
  [name: Valen] Hm. Good.
  [name: Valen] Most people talk at me as if I'm a statue that might answer.
(He looks at you a moment longer than he looks at anyone else in the room. Then he turns back to the window.)
[name: Valen] Enjoy the gala. These things end. They always end.
```

**The other guests**
```
[portrait: CALLA, neutral] Oh — it's you. From the dock. The... faulty unit.
[portrait: CALLA, panic]\pfe[sweat] I mean the UNIT was faulty! Not you!
[name: Calla] You're not faulty. You're a guest.
[name: Calla] Mr Voss asked me to make sure you had everything.
[name: Calla] Do you have everything? Please have everything. It's on my list.

(A thin man in a white lab coat over his evening suit, a gold sunburst pin, giggling at a canapé.)
[portrait: QUENT, happy] Imelda! Imelda Larch! You CAME.
[name: Quent] They said you'd never come. I had a bet on.
[portrait: LARCH, deadpan] Percival.
[name: Quent] She taught me everything I know!
[name: Quent] Well. Everything I knew in AF 288.
[name: Quent] I've learned a great deal since. You'd hate it.
[portrait: QUENT, smug] And you must be — oh! Oh, you're the null reading.
[name: Quent] From the dock. I've seen the file.
[name: Quent] I'd love a look at you sometime. Just a little look. No probes.
[portrait: LARCH, angry] Percival. Go away.
[name: Quent] Going! Going. Lovely to see you, Imelda. You look tired.
[name: Quent] The Lattice is doing beautifully, by the way. Beautifully.
(When he's gone:)
[portrait: LARCH, sad] The best student I ever had.
[name: Larch] I taught him that numbers don't lie.
[name: Larch] I forgot to teach him that people do.

[portrait: HOLLIS, smug] Chancellor Ambrose Hollis, the Accord's humble administrator.
[name: Hollis] You're the challenger the Sovereign keeps not looking at.
[name: Hollis] How interesting.
[name: Hollis] Do enjoy the champagne. It's Meridian's.
[name: Hollis] Everything's Meridian's tonight. I find that very restful.

[portrait: RENATA, neutral] Renata Sallow. The Sallow Line; you'll have seen the Dauntless.
[name: Renata] The Chair and I sit on the same Council.
[name: Renata] We agree on nothing but the wine.
[name: Renata] He'll say something moving about light in a minute.
[name: Renata] Everyone will clap, and tomorrow he'll own another city.
[name: Renata] Clap anyway. I do.

[name: Lucent Scholar] The Provost sent us in her place.
[name: Lucent Scholar] She said she'd rather be "anywhere that isn't a room with Him in it".
[name: Lucent Scholar] She didn't say who Him was.
[name: Lucent Scholar] (again) The Sovereign's walked past us four times.
[name: Lucent Scholar] He looks at the floor every time. You'd think we owed him money.

[portrait: JUNO, happy] I've had seven cakes.
[name: Juno] Uncle Rowan said all of them. I'm doing my best.
[name: Juno] He'd hate this.
[name: Juno] He'd stand in the corner with a glass of water—
[name: Juno] —and tell the potted palm it was being kept prisoner.

ATRIUM WINDOW (inspect): You look down the Spire's shaft. A long way below, something black sits in a brass cradle and glows, not with light but with a deeper dark the light bends round.
[name: Guest at the window] They say it breathes. Watch.
[name: Guest at the window] ...There. Did you see?
(You watch. You're almost sure you saw.)
```

**At the replica** (Larch joins you; this one is required before the speech)
```
REPLICA (display case): A golden Plate behind glass, turning. "THE ZAP PLATE (REPLICA). The original is kept safe by Meridian Concord."
[portrait: LARCH, neutral] That's a copy.
[name: Larch] The real one isn't in Rook's gym. You saw the cradle.
[name: Larch] It's here. Under our feet. In their vault.
[name: Larch] It's been there seven years.
[name: Larch] Every lamp in this city drinks straight off it.
(Behind you, Rook, who has come over with two glasses of something blue, stops. He looks at the replica for a long moment. He doesn't say anything. He puts the glasses down on the plinth and walks away.)
[portrait: JUNO, sad] ...Did he know?
[portrait: LARCH, sad] He knew. Since he was fourteen.
[name: Larch] That's why he never stops talking.
```

**Voss's speech**
```
(A chime. The quartet stops. Voss steps onto a low dais by the window with the whole lit city behind him, his chipped mug still in his hand. Rook stands beside him, smiling for the cameras. Valen stands at the back.)
[portrait: VOSS, neutral] Ten years ago this spring we switched on the first Lattice in Lumen.
[name: Voss] And the Lowlight saw electric light for the first time in its history.
[name: Voss] I was a linesman once. I climbed those pylons in the rain.
[name: Voss] I know exactly what one lamp costs.
[portrait: VOSS, happy] They'll tell you light is a gift. Light is work.
[name: Voss] Every lamp in this city was lit by someone—
[name: Voss] —who was told to be grateful for the dark.
[name: Voss] So I won't ask you to be grateful tonight.
[name: Voss] I'll ask you to look down, just once, at the city you built—
[name: Voss] —and be proud of it.
(Applause. It's real. Juno is clapping. You're clapping. Beside you Larch isn't, and then, after a moment, she is.)
[name: Voss] To ten years of light. And to the next hundred.
```
*(Hob Carrow told you the Lattice never reached the Lowlight. Voss believes it did.)*

### The raid (no jokes from here to the interlude)
```
(The lights flicker. Once. Twice. The quartet stops mid-bar.)
[name: Guest] Is that part of it?
(The lights go grey. A low hum. The same grey as the stage lights in the Lantern Theatre, in Saltmere.)
[portrait: JUNO, shocked]\pfe[jolt] \PN. That's the same — that's the same—
SE: a boom. The service-lift doors on the east wall bend outward and burst.
(Grey cowls pour out of the shaft. Carved bark masks with sad faces. Hollow Ring banners unroll down the glass. At the front, a woman with weaver's shears on her belt.)
[portrait: THISTLE, neutral] Nobody move. Nobody is going to be hurt.
[name: Thistle] We're not here for you.
[name: Thistle] We're here for what's under your feet.
(Screaming. Guests run for the main lift. Directorate guards draw. Voss steps in front of Rook and Calla without thinking about it. Valen doesn't move at all.)
[name: Thistle] You. Briarwick. The one he looked at—
(Juno steps up beside you, shaking, blossoms everywhere.)
[portrait: JUNO, angry] We're not letting you.
[name: Thistle] Girl. You don't know what you're standing in front of.
BATTLE: tag battle — PC + Juno (RIVAL_JUNO as partner, Lumen version) vs [HOLLOW_THISTLE "Thistle", version 1] + [HOLLOW_GRUNT_M "Pallbearer", Lumen version]. Field: Neon Grid (FIELD_DEFAULTS entry for 186).
(LOSE: whiteout; the scene restarts at the burst doors.)
(WIN:)
[portrait: THISTLE, shocked] ...Twice. Twice, now.
[name: Thistle] It doesn't matter. We were never the ones who mattered tonight.
[name: Thistle] He's already down there.
(Directorate guards seize her. She doesn't fight them. As they take her past you she says, very low:)
[portrait: THISTLE, sad] Ask what's in the vault. Ask why it's warm.
[portrait: JUNO, panic] "He"? Who's "he"? \PN—
(The service-lift shaft stands open, its cable still swinging. Far below, a grey light.)
[name: Juno] Go. GO. I'll hold the lift.
[name: Juno] I'll hold — I'll hold everyone. I'm very good at holding people.
V125 = 8.
```
*(Thistle is captured here, as 03_CAST says; she returns on the PC's side in Act IV.)*

## Map 951 — Meridian Spire, Service Lifts [NEW]
```
(A maintenance landing inside the Spire's wall, and a narrow iron stair spiralling down the cliff face. The lift cage hangs open, its gate wrenched. Through the gratings, Lumen glitters on one side; on the other, bare rock.)
LIFT GATE (inspect): The brass has been forced from below. Black grease on it, and boot prints. Nadir grease. They came up the service shafts from the City Below.
(On the stair:)
[name: Bereaved] Turn round, little one. You don't want to see this.
(Battle: HOLLOW_GRUNT_F, Lumen version.)
[name: Bereaved] [after] He said not to hurt anyone. He said it nine times.
[name: Bereaved] Why did he have to say it nine times?
(Lower down: Battle vs HOLLOW_GRUNT_M, Lumen version.)
[name: Bereaved] [after] The other one went down first. The cheerful one.
[name: Bereaved] I don't like the cheerful one.
MOVE: footsteps on the stair above. Rook comes clattering down in his light-up suit, without his drone.
[portrait: ROOK, neutral] I'm coming. Don't argue.
[name: Rook] That's MY Plate down there. ...It's supposed to be my Plate.
[name: Rook] I've never even seen it.
[name: Rook] Seven years. They never once let me see it.
(Rook follows you down.)
```

## Map 952 — Meridian Spire, Plate Vault [NEW]: **"The Shatter"** — key event 1
```
Script: Prismfall.checkpoint     # NARRATIVE_KEYS §10: GO_LIVE_WIRE's checkpoint, the Plate Vault door
(The vault: a round room cut into the cliff under the Spire. Thick Lattice conduits run across the floor into a brass-and-crystal cradle on a dais. In the cradle, a golden Plate blazes with a light that hurts to look at, and the air round it shimmers with heat. The cradle's crystal is crazed all over with fine white lines.)
(At the cradle, two figures. One in a grey cowl and an ash-bark mask with a single white lily, reaching for the Plate with both gloved hands. The other, a woman in Hollow grey, a half-mask over the top of her face and a smile under it, crouched at the cradle's foot.)
[portrait: MOURNER, neutral] *(the doubled voice)* Gently. We lift it out gently.
[name: The Mourner] We carry it out of here—
[name: The Mourner] —and give this city back its river and its dark.
[name: The Mourner] That's all. That's all tonight is.
[portrait: SABLE, happy] Mm-hm. Gently.
(She stands. Something small and brass is clamped to the Plate's edge, blinking.)
[portrait: MOURNER, shocked]\pfe[exclaim] What is that? What have you put on—
[name: Sable] Light for everyone.
(She steps back off the dais, almost skipping.)
SE: a high, rising whine.
```
**Cutscene SH-1 "The Shatter"** (`Prismfall Cutscenes`, on the map; ~8 s; skippable after the first viewing)
| # | Camera | Action | FX |
|---|---|---|---|
| 1 | Close on the Plate (1.5 s) | The brass Splitter's light goes from blinking to solid | Whine climbs; screen tint white-violet at the edges |
| 2 | Wide (1 s) | The Mourner throws himself at the cradle | — |
| 3 | Centre (2 s) | **The Shatter**: a white-violet blast; the vault inside it | Flash to white; shake 8 px; a sound like every bell in Lumen breaking at once |
| 4 | Pull back through the rock (2.5 s) | A ring of light runs out through the cliff, down and out, toward the streets below (no streets shown) | Ring sprite expanding; then silence |
| 5 | Fade up (1 s) | The vault: the cradle split, the Plate cracked across, the Mourner holding it in his right hand, that glove smoking | Smoke wisps; the light in the Plate stutters |
```
[portrait: MOURNER, shocked] No — no — what did you DO?
(He has caught the cracked Plate in his right hand. The glove on that hand is smoking. The woman is gone. There's only the vault's open service door and the smell of burnt brass.)
(The Mourner turns and sees you. He goes still, the way he did in the Lantern Theatre.)
[portrait: MOURNER, sad] ...You. Not you. Not here.
[name: The Mourner] Get out of here, child. Get OUT—
(He lays the cracked Plate back in its split cradle, very carefully, the way you'd put down something that's dying. Then he's gone through the service door, holding his right hand away from his body. It's still smoking.)
[portrait: ROOK, shocked] *(behind you)* That's it. That's the Zap Plate.
[name: Rook] That's — it's broken. It's BROKEN.
(Something huge unfolds from behind the cradle: an Electivire, swollen with the Plate's discharge, crackling white, its eyes empty. It plants itself between you and the door.)
[name: Rook] That's the vault guard! That's Meridian's—
[name: Rook] Look at it, it's drunk on the— get BACK—
```

**Boss: "Overcharged"**
```
BOSS BATTLE: "Overcharged" — ELECTIVIRE (2 bars; BOSSES.md, the segment after Gym 4). Field: Neon Grid.
(At the bar break the cracked Plate flares and the field breaks: battle.change_field(:BLEED, "The cracked Plate screams. The vault stops being sure what it's made of!") — the game's first scripted any → Bleed.)
(At the bar break, an interlude prompt:)
(The cracked Plate is spitting light on the dais, an arm's length away. The Electivire is reeling. If you had the Plate, it would have nothing to drink.)
[portrait: ROOK, panic] Don't touch it with your HANDS!
[name: Rook] You saw him, you saw his glove—
> Grab the cracked Plate and run.
  (You grab it. It's the most light you've ever held. For one second it doesn't hurt. Then it's the only thing in the world.)
  Script: Prismfall.game_over(:GO_LIVE_WIRE)
> Hold the line.
  (You stay where you are. The fight goes on.)
(LOSE: whiteout to the Lumen Pokémon Center; the vault door checkpoint reloads the scene at the door.)
(WIN:)
(The Electivire crashes down beside the cradle, and the light goes out of it. It's just a Pokémon, very tired, on a cold floor.)
(Rook crouches by it, then by the Plate, and doesn't touch either.)
[portrait: ROOK, sad] Hey. Hey, big guy. It's okay.
[name: Rook] The wave went out. When it broke.
[name: Rook] It went through the rock, that way. Down. Into the—
[portrait: ROOK, shocked]\pfe[jolt] The Lowlight's under us.
(The service door in the vault's south wall stands open. Beyond it, a stair down the cliff, grey light, and silence. No traffic. No music. Nobody shouting. Silence.)
Switch S113 CH5_GALA_DONE = ON. Switch S114 CH5_SHATTER = ON. V104 LOWLIGHT_STATE = 1 (608 replaces 181). V125 = 9.
```

## Map 608 — The Lowlight (Shattered): **"Twelve"** (autorun on arriving through the vault's service door, V125 == 9) — key events 1 and 2
```
BGM: none. Wind. A single chime, a long way off.
(You come out of the service door onto the Lowlight's upper steps.)
(The Lowlight is glass.)
(Not all of it. A ring as wide as four streets, under the Spire's foot. The tenements are glass to the second floor, and the washing lines, and the noodle cart, and the hopscotch. The light down here is grey and wrong and comes from every direction at once. Round the ring's edge a Bleed Veil shimmers like heat over a road, and on the other side of it, people. Hundreds. Not one of them is coming in.)
(And in the glass, people.)
```

**The twelve** (each an inspect event at the spot where that resident stood on 181)
```
DEX: A boy of eleven, glass, mid-wave, one arm up, his mouth open on a word. The soda crate has slid off his hip and lies at the Veil's edge, half glass. At his feet a Pichu is pressed against his glass ankle, shaking. It won't move.
MARTA VELL: A woman with her arms up to a washing line, a sheet half pegged. The sheet is glass too, caught mid-billow.
OLD JORY: The cobbler on his step, head thrown back, laughing. Glass. You can see the laugh in it.
NESSA: A girl on the hopscotch, one foot up, about to come down on seven.
HOB CARROW: The lamp-tender at the top of his ladder, his taper raised to the lamp. The lamp is lit. It's the only thing in the Lowlight still burning.
ALDO FISK: A linesman with his helmet under his arm and his hand held out, the way he showed you. Under the glass, very faintly, it still hums.
SUKIE: The lift-girl at the Nadir grille, her hand on the lever.
ILO AND MATTIE: Two people on a doorstep, holding hands. Glass.
GRAN OSK: An old woman with a handful of crumbs. The Pidove beside her is glass too, mid-peck.
BENNO: The noodle-cart man, ladle raised, mouth open on a joke.
MR IMRIE: A schoolteacher on a bench with a pen in his hand. On his knee, a glass page: "What does light mean to you?"
```

```
(You walk down into it. Nothing stops you. It's quiet. The glass is cold. Under your ribs something is very still, as if it's listening.)
(On the far side of the Veil the crowd goes silent. They're watching you walk among the glass.)
[name: Voice in the crowd] They're IN it. How are they in it?
(At the Veil's edge, a Directorate officer's arm across Marlo:)
[name: Marlo] That's my brother. That's my BROTHER.
[name: Marlo] Dex! DEX!
(Rook comes down the vault stair behind you and stops on the bottom step, a step short of the Veil. His drone has found him again; it hovers at his shoulder with its red light on.)
[portrait: ROOK, sad] ...
[name: Rook] Turn it off. Rotom. Turn it *off*.
(The red light goes out.)
(Juno has pushed to the front of the crowd in her curtain dress. She puts a hand out to the shimmer and snatches it back, burned.)
[portrait: JUNO, crying] \PN. \PN, come out. Please come out.
[name: Juno] I can't — I can't come in—
(She sees the boy with his hand up, and the Pichu at his feet.)
[name: Juno] That's Dex. From the stairs.
[name: Juno] He was going to tell us the rest.
```

**Voss restores the light**
```
(Floodlights. Meridian crews in hard hats run cable down the steps outside the Veil. In the middle of them, in shirtsleeves, jacket gone, sleeves rolled: Aurelian Voss.)
(He goes right up to the Veil's edge, where the soda crate lies half in the glass. He kneels and lifts it out, glass and all, in both arms, and carries it back through the crowd. Every screen on the street carries the picture.)
[name: Meridian Crew Chief] Grid's rerouted, sir! The block'll be back on in four minutes!
[portrait: VOSS, sad] Make it three.
(The lamps outside the ring come on, one street at a time. Inside the ring nothing comes on. Only Hob Carrow's lamp, still burning at the top of his ladder.)
[name: Voss] *(to you, across the Veil)* Are you hurt?
[name: Voss] ...No. You're not. Are you.
(He looks at you standing among the glass. Then down at the crate in his arms. He doesn't say anything else. Somebody takes the crate from him, and he lets them.)
```

**Valen at the Veil**
```
(The crowd parts. A man in white walks through it, and the Directorate officers step back for him. He doesn't stop at the edge of the crowd. He goes to the Veil itself.)
(Valen Corrigan pulls off his grey glove.)
(For a moment, in the grey light, his hand isn't a hand. It's clear: crystal, all the way up past the wrist, with something moving inside it like light in deep water. He lays it flat against the Veil.)
(The shimmer flinches from it.)
(He pulls the glove back on, fast. That's when he sees you, inside, standing among the glass.)
[portrait: VALEN, shocked]\pfe[dots] ...
[portrait: VALEN, neutral] You were in the Lowlight when it went?
[name: Valen] And you're... standing.
(He looks at you a beat too long. Two beats. Then he turns away.)
[name: Valen] Who's in charge here?
[portrait: MARCHETTI, neutral] Director Marchetti, Sovereign. Meridian Security Directorate.
[name: Valen] Then take statements. All of them. Including that one.
V125 = 10.
```

**The testimony** (on stepping out through the Veil)
```
(Stepping out through the Veil is like coming up out of cold water. The noise of the street comes back all at once.)
(A woman in a white-and-gold Directorate coat is waiting with a notebook. Close-cropped grey hair. She doesn't look as though she's ever been surprised.)
[portrait: MARCHETTI, neutral] Director Helene Marchetti.
[name: Marchetti] You were in the vault, and then you were in the glass.
[name: Marchetti] That makes you my best witness.
[name: Marchetti] What did you see?
```
**CHOICE `:ch5_lowlight_testimony`**
```
> "The Mourner broke the Plate." (mourner)
  Script: pf_choose(:ch5_lowlight_testimony, :mourner)
  [name: Marchetti] The Mourner, hands on the Plate.
  [name: Marchetti] That's what everyone will want to hear.
  [name: Marchetti] It also happens to be what you saw. Thank you.
  [name: Marchetti] It'll be on the Sovereign's desk within the hour.
> "Someone else was there. A woman. She put something on it." (someone_else)
  Script: pf_choose(:ch5_lowlight_testimony, :someone_else)
  [name: Marchetti] A woman. Masked. Cheerful.
  [name: Marchetti] Gone before my officers reached the door. ...Hm.
  (She writes for longer than you spoke. Then she writes your name at the top, and underlines it.)
  [name: Marchetti] Thank you. I'll remember you.
  [portrait: LARCH, neutral] *(behind you, very quietly)* Good.
> "I don't know." (unknown)
  Script: pf_choose(:ch5_lowlight_testimony, :unknown)
  [name: Marchetti] Nobody does, tonight. It'll come back.
  [name: Marchetti] Come and find me when it does.
V125 = 11.
```

**The broadcast** (182, the Pokémon Center, that night; every screen)
```
(Every screen in the Center shows the same picture: the Sovereign in white in front of the Spire, with the glass behind him.)
[portrait: VALEN, neutral] *(on the screen)* Tonight the Hollow broke a Plate in the heart of Lumen.
[name: Valen] Twelve of our people are in the glass.
[name: Valen] I have known Hollow men who were gentle.
[name: Valen] I have known Hollow women who were right.
[name: Valen] None of that matters tonight.
[name: Valen] Under the Accord's emergency articles—
[name: Valen] —I am granting the Meridian Security Directorate the Mandate:
[name: Valen] The powers of the Wardguard, wherever a Lattice stands, until this is over.
[name: Valen] We have come through worse. We always have.
[name: Valen] Velmora endures.
(The screen holds on him a moment after he stops. Then it cuts to Voss carrying the soda crate.)
[portrait: JUNO, crying] Twelve. He said "twelve" like it was a number.
[name: Juno] Uncle Rowan's going to be so angry.
Switch S115 CH5_MANDATE = ON.
```
*[if `pf_choice(:ch5_lowlight_testimony) == :mourner`] — the Gale Post desk, next morning:* `TELEGRAM: "So you told them the pageant version. I know that one by heart. — D.P."` *(Dorian's Act V Consent; NARRATIVE_KEYS §6.2.)*

## Map 952 — the Plate Vault, 3 a.m.: **"Already Cracking"** (V125 == 11 → 12)
```
(3 a.m. At the Center's desk, a note in a hand you know: "Vault. Now. Bring your Flash. — I.L.")
(952. The split cradle is roped off with Directorate tape. Larch is under the tape on her knees with a borrowed scanner and a torch in her teeth.)
[portrait: LARCH, neutral] Don't tell the Director. I told her I was a cleaner.
[name: Larch] She looked at my oilskin and believed me, which hurt.
[name: Larch] Look. Here. The stress lines in the crystal.
[name: Larch] A Splitter makes a star: one point, everything running out from it.
[name: Larch] There's the star, where she clamped it.
[name: Larch] But these. The long ones, the length of the cradle, under the star.
[name: Larch] They're old. Months. Years.
[name: Larch] That's not a blast. That's fatigue.
[name: Larch] The kind you get in a bridge that's carried too much for too long.
[portrait: LARCH, sad] That wasn't the Hollow's hammer. The Plate was already cracking.
[name: Larch] Something's been drinking from it for ten years.
(She looks up at the conduits running into the cradle: the thick Meridian cables, the ones she drew on a napkin.)
[name: Larch] Something I built.
WAIT 40.
[name: Larch] Twelve people, child. Twelve.
> It wasn't your hand on the Plate.
  [name: Larch] No. It was my hand on everything else.
> What do we do?
  [name: Larch] We write it down. All of it.
  [name: Larch] And one day we say it out loud, somewhere nobody can switch off.
> ...
  [name: Larch] Yes. That's about all there is to say.
[name: Larch] Go back to bed.
[name: Larch] I'm going to sit here and look at it until it stops being true.
V125 = 12.
```
*(09 #13. "Somewhere nobody can switch off" is the Larch Papers, Ch12.)*

## Maps 105/106 — Ferrow Lighthouse: **INTERLUDE I — "Lamplight"** (playable as Kestrel)
```
V119 INTERLUDE_ACTIVE = 1. (The party is swapped for Kestrel's: Honedge "Morwen", Staravia, the counter-starter, at K2's levels +2.)
TEXT (white on black): The same night. Ferrow's Landing.
(106, the lamp room. The great lamp turns. Hesper is asleep in her chair with a blanket over her knees and her pipe gone out in her hand. On the shelf, a wireless murmurs: "...the Lowlight... twelve... the Mandate..." The player is Kestrel.)
MOVE: Kestrel turns the wireless off.
[portrait: KESTREL, neutral] Twelve.
[name: Kestrel] She'd never. She'd NEVER. Not a city. Not children.
[name: Kestrel] ...So it isn't her. Good.
[name: Kestrel] That's good. That's what I wanted.
```
```
(105, the keeper's room below. Gran's trunk at the foot of her bed. It's been locked his whole life.)
TRUNK (action): It isn't locked. It hasn't been locked for years. He just never tried.
(Inside, folded small: a black lace veil, a Ghost Warden's veil, with Gravenmoor's ghost-lantern stitched in silver at the hem.)
[portrait: KESTREL, shocked]\pfe[jolt] ...
(He holds it up. It smells of candle-smoke, and something else, something he knew once.)
MEMORY (the screen goes white-grey; no control): A crowd, enormous, and lights. A small boy's height: everything is legs and coats. A woman in a veil running, away from him, toward something so bright you can't look at it. A kid. A kid made of light—
(It stops. Kestrel is on the floor with the veil in his hands. The lamp is still turning, high above.)
(Breathing hard:)
[portrait: KESTREL, angry] Not again. Not AGAIN.
[name: Kestrel] It's a dream. It's the same stupid dream.
[name: Kestrel] There's no kid made of light. Kids aren't made of light.
SE: a creak on the stair. The room goes cold.
(On the lighthouse stair a Haunter drifts up toward the lamp, its edges glassy and wrong.)
[name: Kestrel] Morwen. Up.
WILD BATTLE: HAUNTER (Bleed-touched; Lv at K2 + 3; cannot be caught; field per FIELD_DEFAULTS for 105).
(When Honedge is out:)
[name: Kestrel] Hold. Hold it.
[name: Kestrel] She held a line for a whole city once, everyone says.
[name: Kestrel] You can hold a staircase.
(LOSE: the interlude restarts at the stair.)
(WIN:) (The Haunter comes apart into cold sparks and drifts out through the window toward the sea.)
[portrait: KESTREL, sad] Good. Good, Morwen.
[name: Kestrel] Gran won't say. Ysolde won't answer my letters.
[name: Kestrel] The Accord sent a box.
[name: Kestrel] Fine. Then I'll find out myself.
(He packs: a coat, the veil, five smoked eels in newspaper, and a cup of cold kelp tea he's been saving for later since spring. He looks at the tea for a long time. He packs it.)
(From the gallery he sees a small boat slip out of the harbour with no lights, under the chain and past the Concert's cutters. A stocky shape at the tiller. A glint of gold tooth.)
[portrait: KESTREL, deadpan] Edda. Of course it's Edda.
Switch S162 EDDA_SMUGGLER = ON.
(Kestrel stops at Hesper's chair. He tucks the blanket up round her. She doesn't wake. Or she lets him think she doesn't.)
[portrait: KESTREL, neutral] If you're alive, I'll find you.
[name: Kestrel] And if you're not, I'll find whoever said you weren't.
(He goes down the stairs. The door shuts. In her chair, Hesper opens her eyes.)
[portrait: HESPER, sad] *(to the dark)* Oh, my boy. Don't.
V119 = 0. V125 = 13. V101 STORY_ACT = 2. V102 STORY_CHAPTER = 6.
TITLE CARD: END OF ACT I.
TITLE CARD: II — IMPRINTS
```
*(The Act II opener, the Lowlight shrine and Dex's glass warming under the PC's hand, belongs to Chapter 6: 05_ACT_II "Act-opening beat", S164 DEX_SHRINE, and the Trials quest `ZE_LOWLIGHT_LAMPS`, where Dex's Pichu chooses the PC.)*

---

## Notes for other teams
- **Mysteries seeded here (09):** #2 (Rowan gives away his gala invitation; the Mourner's smoking right glove), #4 (Valen's crystal hand at the Veil; "Velmora endures", and nobody in the script remarks on the word), #8 (the Spire's plaque: the Aurelian sun tower), #9 (Lamp 47's draw spike, vague), #12 (Sable cheerful, gone before Security), #13 (Larch's fatigue lines; the Locks ledger's "draw x3"), #14 (Rook films the case glowing; Voss asks about it; Juno's "How did he know which road?"), #15 (the Prism Arena hoarding and model, "eighteen pylons"), #17 (Valen avoids the Lucent delegation), #23 (the black core that breathes), #29 (Contract 7-B). **#5 and #6 are not touched**: the Southgate prayer and window are hints only, and nobody says the Crown is cracked.
- **Comedy (15_COMEDY):** Juno's pies, the scrip store, the tram stop, the vending and kiosk quests, Rook's blackout ("This is content"), "Chat Has Opinions", Larch's formal oilskin, Quent's bet. Nothing after the Gala's lights go grey; the interlude's "Edda. Of course it's Edda." is a dry line in a separate scene.
- **Running gags:** kelp tea bag four (182); Kestrel's tea "for later" (packed in the interlude).
- **Distribution (SPINE Rev 16):** the only Pokémon on offer are the blackout's wild Rotom (Electric/Ghost; no Ground answer to Rook) and the optional Sluiceworks Rotom. No gifts after Gym 4 (Sahar's and Corvin's answers stay locked).
- **Badge name:** the **Arclight Badge** (Gym 4; creator, 2026-11-21).
- **Playscript & Restrained Rejuv Expressions pass (2026-11-24):** Multi-box playscript pacing (`<= ~85 chars/box`), restrained portrait tagging (~22–28% of cast spoken boxes across the 17 verified portrait cast members in Ch5), sparing `\pfe[...]` emotes (`018_ExpressiveDialogue.rb` v2), and strictly zero comedy/bubbles after the Gala lights go grey.

---

## Map events needed (Chapter 5)

For map builder 15 (building these maps now) and the trainer designer. **[NEW]** = a map or event that isn't in maps.json yet. "Once" = self switch A after it plays. `V125` is the new chapter counter **CH5_STEP** (design/FLAGS.md): 0 leaving Ebbmouth · 1 Juno's letter read at Brassfall · 2 Juno rejoined on Wallshadow Row · 3 through Lumen West Gate · 4 met Dex · 5 the Lowlight blackout fixed (gym open) · 6 Gym 4 won · 7 Gala started · 8 raid, into the service lifts · 9 Shatter and boss done · 10 aftermath with Valen done · 11 testimony given · 12 Larch's 3 a.m. scene done · 13 Interlude I done (Act II starts).

**Ebbmouth 167 (or 160) — the way out**
- East exit to **580** (the towpath gate). Shut until `pfm_gym_won?(:LEADER_MARISOL)` **and** V124 CH4_STEP >= 7 (Chapter 4 closed). Gatekeeper line and sign are in the script ("Ebbmouth, the towpath gate").

**580 The Reedholms** (`:SNOWY_MOUNTAIN` per ROUTES; rain)
1. Road sign.
2. Eel-weir keeper (2 lines).
3. **Teo on the channel** (touch strip across the main boardwalk, once): plays only if `pf_choice(:ch4_teo) != :report`. A punt event with Teo's sprite crosses the channel during the line.
4. **Wanted poster** on the smoke hut (sign) and a reed-cutter NPC: only if `pf_choice(:ch4_teo) == :report`.
5. Reed-cutters' punt hops (short warps), heron islet, the day/night channels and the Sunk Holm secret as ROUTES.yaml lists.
6. Door to **584** (sign + Rook graffiti) and the Bleed Veil warp to **588** (a fisher NPC beside it).
7. 6 route trainers (trainer designer, Lv 20–23, no Ground hand-out).

**584/585 Voltaic Sluiceworks** (optional): the dead turbine's builder's plate (sign, text in script); Rook's clapperboard (item flavour); the static Rotom stays on 585.
**588 Ebb Hollow** (optional, `:BLEED`): Field Notes on first entry; 4 inspect lines (the drowned village of Holmsby); TM49 and Bleed Shard #4 as maps.json.

**592 The Icecutters' Haul** (`:SNOWY_MOUNTAIN`)
1. Road sign. 2. Union picket hut: Picket Captain Hulda + 2 strikers. 3. Mudsdale haul-team driver. 4. Sawyer's Cross gates N and S (closed, signs). 5. Meridian heat-contract recruiter by a poster (sign + NPC). 6. **The dropped ice block** (action, once): gives Key Item **ICE-BOUND SATCHEL** [NEW item]. 7. 5 route trainers.

**590 Brassfall** + 591 Pokémon Center + **596 Brassfall Union Hall [NEW interior, ~17×11]**
1. Arrival lines (autorun once at the lower lock). 2. The Lockmaster (Zenith engineer) and the union steward who argue at the lift. 3. Company store clerk ("SCRIP ONLY"). 4. **The Ice Elevator** (optional local quest): the stuck ice-lift at the falls' foot; with an Electric-type in the party (or a CELL BATTERY) it restarts and becomes a two-way shortcut warp to the top station on 581. 5. **591 Gale Post desk: Juno's letter** (V125 0 → 1). 6. **596 the union boiler** (action with ICE-BOUND SATCHEL): swaps it for Key Item **HEAT CONTRACT (DRAFT)** [NEW item]; Union boss Gunnhild reads it. 7. Union Hall flavour (2 NPCs, a notice board).

**581 The Icefall Locks** (`:SNOWY_MOUNTAIN`)
1. Road sign. 2. **Extraction Lattice No. 4** (fenced): its plate (sign), Linesman Tolly (2 pages), the thaw ring in the falls under it (inspect). 3. The Ice Elevator's top station (warp, open once fixed in 590). 4. **The third lock gate's ice cave** (secret; a small alcove on the map): the maintenance ledger (sign). 5. The top-of-the-falls border post: an Elowen forester + a Meridian guard (one line each). 6. 6 route trainers.

**595 Coppice Ride** (`:MEADOW`)
1. Road sign. 2. **"The First View of the Crownwall"** at the ride-side shrine: a touch strip in front of the shrine (once). Camera scroll north to the Crownwall on the horizon (parallax or a picture), the PC's scar ache, an optional re-read of Mum's Letter. A pilgrim NPC stays after. 3. The Kingsferry punt (ferryman; a short warp across the Ebb). 4. Woodward + charcoal clamp. 5. The uncut panel (secret; Miracle Seed). 6. 5 route trainers.

**594 Wallshadow Row** (`:MEADOW`)
1. Road sign; Crown Road milestones XVII and XVIII (signs). 2. **The Four Ways (west junction)**: the inn front and the four-kingdom signpost (sign). **Juno rejoins** here (touch on the inn yard, V125 == 1 or 0 → 2; Juno becomes the follower for the rest of the road and the city). 3. Closed exits with a guard each: **W Prism Falls** (Elowen forester; Act III), **N Kingsmead** (tithe-reeve; Act III), **S the Long Drop** (chained lift; Ch9), **E Candle Down** (road-menders; opens at `pfm_gym_won?(:LEADER_ROOK)`, the Act II road). 4. Tithe barns: the Accord's tithe-collector + a farmer. 5. **Southgate shrine** at the south junction: prayer board (sign), the eighteen-and-one window (inspect), the shrine-keeper. 6. 6 route trainers.

**593 The Arc-Lamp Mile** (`:NEON_GRID`)
1. Road sign. 2. Three hoardings (signs): TEN YEARS OF LIGHT · **THE MERIDIAN PRISM ARENA** (09 #15) · the Fellowship. 3. **Lamp 47** (action, two pages: the lamp, then "Look under the base plate?"). 4. Lamplighters' depot keeper. 5. The tram stop and the man waiting for the tram. 6. An orchard-hand and the clockwork pickers (decor events). 7. 5 route trainers.

**582 Lumen West Gate** — the Meridian scanner (touch): NULL, then the guard's call upstairs, then Key Item **GALA INVITATION** [NEW item]. V125 → 3.

**180 Lumen City — the Concourse**
1. Arrival autorun (once, V125 == 3). 2. Circuit Gym door: a closed sign and an attendant until V125 >= 5. 3. A Nadir lift-grille with Hollow Ring graffiti (inspect) and the Zenith officer moving a Nadir kid along (2 NPCs, one scene). 4. Flavour NPCs (script list). 5. P-3NNY kiosk and the Fizzbolt machine (Trials hooks). 6. Glide Cycle Shop (Bicycle) as maps.json. 7. The stairs east to 181.

**181 Lumen City — the Lowlight (before the Shatter)** — *the twelve must stand where 608's glass figures stand*
1. **Dex and his Pichu "Spark"** at the top of the Lowlight stairs (first meeting; V125 3 → 4).
2. **The twelve** (named NPCs, each with 1–2 lines; positions to copy onto 608): Dex · Marta Vell hanging laundry · Old Jory the cobbler (laughing) · Nessa (8) on the hopscotch · Hob Carrow the lamp-tender on his ladder · Linesman Aldo Fisk coming off shift · Sukie the Nadir lift-girl at the grille · Ilo and Mattie on a doorstep (married a week; two NPCs, one event is fine) · Gran Osk feeding a Pidove · Benno at the noodle cart · Mr Imrie the schoolteacher marking on a bench. *(That is twelve people: Ilo and Mattie are two.)*
3. **Rook's film crew** (Rook, his drone, a director, a boom operator) until V125 >= 5.
4. **The blackout** (autorun the first time the PC steps onto the crew's square with V125 == 4): the lights die; three junction boxes hold wild Rotom (action → `WildBattle.start(:ROTOM, 24)` each, catchable), then the feed-line box (Rotom Lv 26). When all four are done the lights come back (V125 → 5) and the gym opens.
5. Cadence's "Off the Beat" (Trials, optional; see the Trials note below).
6. The Spire's service door (locked; "MERIDIAN CONCORD — AUTHORIZED PERSONNEL"). On 608 it is the door the PC comes out of.
7. Hidden CELL BATTERY as maps.json.

**182 Lumen Pokémon Center** — Gale Post desk (Larch's letter on arrival; after the Shatter, Dorian's telegram if `pf_choice(:ch5_lowlight_testimony) == :mourner`); the news screen (Valen's Mandate broadcast, S115).

**190–193 the Circuit Gym** (built from GYM_PUZZLES Gym 4): gym guide and Spark lines as the script; **the Core's cold cradle** (action) with Rook's PA line **changed** (see the script: "Turn it off" is saved for the Lowlight); Juno and Larch in the Core's gallery for the battle; Rook; badge; the fourth note.

**185 Meridian Spire — Lobby**
1. Receptionist: the Gala door (to 186) opens with the GALA INVITATION and V125 >= 6. 2. The founding plaque (sign; 09 #8). 3. The Prism Arena model (exhibit; 09 #15). 4. The Imprint exhibit (existing). 5. The helpdesk Rotom (Trials `ZE_CUSTOMER_SUPPORT`). 6. After the Shatter: triage NPCs (two Directorate officers, a medic) until Act II.

**186 Meridian Spire — Gala Hall**
1. **The Gala** (autorun on entry, V125 6 → 7): free-roam window with ~10 guests (Voss, Valen, Calla, Quent, Hollis, Councillor Sallow, the Lucent delegation, Larch, Rook, Juno), then the speech, then the raid. 2. The atrium window onto the Dark Stone core shaft (inspect; 09 #23). 3. The **replica** Zap Plate in its display case (existing feature at (13,2)). 4. **The raid**: lights flicker, the service-lift door on the east wall bursts, Hollow grunts in; **tag battle PC + Juno vs two Pallbearer squads**. 5. The service-lift door then leads to 951 (V125 → 8).

**951 Meridian Spire — Service Lifts [NEW map, ~21×17, Spire/factory interior]** — the shaft landing and the maintenance stair down the cliff to the vault: 2 Hollow grunts (single battles), Rook catching up (one line), a lift that has been forced open from below (inspect: Nadir grease on the brass).

**952 Meridian Spire — Plate Vault [NEW map, ~25×19]** — under the Spire's foot, in the cliff above the Lowlight. North: the Zap Plate's cradle on a dais, Lattice conduits running into it. South: the vault's service door, which opens onto **608** (after the Shatter). Events: the Mourner + Sable + the Plate (the Shatter scene, cutscene SH-1 below); `Prismfall.checkpoint` at the vault door (GO_LIVE_WIRE, NARRATIVE_KEYS §10); the **Electivire boss** on the cradle dais; a second page for **Larch at 3 a.m.** (V125 == 11 → 12).

**181 → 608 The Lowlight (Shattered)** (`:BLEED`; V104 LOWLIGHT_STATE = 1 swaps 181 for 608)
1. Aftermath autorun (the PC comes out of the vault's service door; V125 == 9). 2. **Twelve glass figures** at the 181 positions, each with an inspect line (script). 3. The Bleed Veil at the district's edge: the PC inside, everyone else outside. 4. Rook (off camera), Juno, Voss with the glassed soda crate, Valen at the Veil, Director Marchetti and a Directorate officer (the testimony). 5. Dex's Pichu at his feet. 6. The screens at the edge carry Valen's broadcast that night. 7. From Act II: S164 DEX_SHRINE pages (candles and soda cans; `ZE_LOWLIGHT_LAMPS` is the Trials owner's).

**105/106 Ferrow Lighthouse — Interlude I "Lamplight"** (V119 = 1): the party swap to Kestrel; the trunk and the veil; the memory flash; a wild Bleed-touched Haunter on the stairs; the bag; Edda's boat slipping the harbour chain (S162 EDDA_SMUGGLER on); the title card II (V101 = 2, V102 = 6).

**New items** (items_prismfall.txt owner): `GALAINVITATION`, `ICEBOUNDSATCHEL`, `HEATCONTRACT` (Key Items, descriptions in the script). **New boss** (BOSSES.md owner): "Overcharged" Electivire, 2 bars, Lv per the segment after Gym 4, field `:NEON_GRID` → `:BLEED` at the bar break (the first scripted any → Bleed). **Trials owner:** `ZE_OCTAVE_OFF_BEAT` lives on 181, which is replaced by 608 after the Shatter: never close it (Cadence is Singer 3 of the Eevee Octave; closing it would lock the Octave and Eevium Z for the save): relocate her to the Concourse (180) after the Shatter).
