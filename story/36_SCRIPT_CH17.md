# Script: Chapter 17 — "The Drowned Crown" (the Drowned Road; Underveil after the Purge; Nyx and Gym 16; Nadir's independence; the Archive branch; the dive into Aurelia; the Sun Court; Voss; Brann's confession. END OF ACT IV)

> **Final playable script** for Chapter 17, the last chapter of Act IV.
> - **Maps:** the Drowned Road (832 the Brink, 820 the Hanging Stair, 821 the Drownings, 822 Under the Drownings), Underveil (420–433: the Lantern Tiers 420, the Moon Market 423, the Sump Docks 424, the Barons' Stair 425, and Gym 16 430–434), Midstair (830), and Aurelia below: the Drowned Spires (824), the Air Halls (825), and the Gilded Throne Vault with the Sun Court (826). Optional: Ironbloom (828). Branch: the Accord Archive (838).
> - **Status:** none of these is built. The list at the end is what to build from.
> - **Order:** follows `story/35_SCRIPT_CH16.md`. Act V's Chapter 18 ("The Gloaming") follows.
> - **Sources:**
>   - Story: 07_ACT_IV Ch17; 03_CAST (Nyx, Sahar, Edda, Rook, Voss, Kroll, Quent, Ysolde, Brann, Mother Gutter, Valen); 09_MYSTERIES (#1, #5, #6, #11, #15, #20, #24); 10_CHOICES_ENDINGS; 15_COMEDY Ch17 "The Price".
>   - Keys: NARRATIVE_KEYS (`:ch17_nyx`, `:ch17_voss_offer`, `NYX_BARGAIN_TAKEN`, `VOSS_FEIGNED`/`VOSS_ACCEPTED`, `CONCORD_OPEN`, `KROLL_EXPOSED_CH13`, `GO_INTO_THE_LINE`, `GO_THE_THRONE`).
>   - Design: GYM_PUZZLES Gym 16; WALKTHROUGH Ch17; CAMEOS §6 "Deliverer"; `design/CHAPTER_BEATS.md`; `design/DENSITY_STANDARD.md`; `design/POKEMON_AVAILABILITY.md` §4 (the no-legendaries rule).
>   - Quests: the Trials quests `NA_DOGS_OF_THE_MOON_MARKET` and `NA_MOTHER_GUTTERS_LEDGER` (titles as catalogued), and `ZE_LETTERS_DOWN` (delivery).

## Conventions
As in the earlier scripts.
- **Portrait cast:** Nyx, Sahar, Edda, Rook, Voss, Kroll *or* Quent, Ysolde, Brann, Mother Gutter, Rowan (if `ROWAN_ALIVE`; he came down with the Hollow), and the PC (one authored line, at the cradle).
- **Plain:** the courier, the barricade fighters, the Sump Barons, the Directorate line, the Meridian salvage crew, Amaria and Titania (cameo; `[name: …]`), and every trainer.
- **Gym 16** is a double: `Prismfall.gym_battle(16, double: true)` (illusions on both sides; GYM_PUZZLES).
- **The Sun Court admin:** `TrainerBattle.start(:MERIDIAN_KROLL, "Sabine", 1)`, or `TrainerBattle.start(:MERIDIAN_QUENT, "Percival", 2)` if `KROLL_EXPOSED_CH13`. Both are on `:CAVE`.
- **No legendary joins the party** in this chapter (POKEMON_AVAILABILITY §4).

**Counter:** V138 **CH17_STEP** (new; design/FLAGS.md):
| Value | Meaning |
|---|---|
| 0 | the Drowned Road |
| 1 | Underveil's barricades |
| 2 | Nyx in the Moon Market |
| 3 | independence (S149) |
| 4 | Gym 16 won |
| 5 | Nyx's bargain and confession |
| 6 | the Archive (branch; skipped otherwise) |
| 7 | the dive |
| 8 | the Sun Court: the cradle (S148) |
| 9 | Voss's offer |
| 10 | the cradle taken (S147) |
| 11 | Ysolde's lanterns |
| 12 | Brann's confession |
| 13 | the docks: END OF ACT IV (V101 = 5; V102 = 18) |

**State set here:**
- **Switches:** S147 CH17_AURELIA_DONE, S148 CH17_SHARD_NAMED, S149 CH17_NADIR_INDEPENDENT.
- **Variables:** V111 NADIR_STATE = 3 (independent).
- **Keys:** `:ch17_nyx`, `:ch17_voss_offer`.
- **Game overs:** `GO_INTO_THE_LINE`, `GO_THE_THRONE`.
- **Key Items:** ARENA SCHEMATICS (on `:trade`), MAREN'S HYMN PAGE (Archive branch).

## The chapter's key events (design/CHAPTER_BEATS.md)
1. **Aurelia: "You're the missing piece."**
   - **What happens:** the Sun Court murals tell the real Prismfall. At the keystone cradle your chest glows with eighteen colours. Nyx: **"Oh. Oh, darling. You're the missing piece."** Sahar reads: *"Here rests the One that is every color and none."* You carry a splinter of the Legend Plate.
   - **Build-up:** the whole game. The NULL scan, the badge case's chords, the Ring that sings, the Mindscape, the Cathedral echo, UNIMPRINTED-01.
   - **Consequence:** S148. Dialogue swaps everywhere, and the shard has a name.
2. **Voss names himself.**
   - **What happens:** House Aurel ("We changed the name and kept the grudge"). He owns AF 290 ("My array. My dials.") and the Lowlight ("I made those twelve *mean* something"), and makes his offer (`:ch17_voss_offer`).
   - **Consequence:** the Act V finale's opening beat, and the Concord Dawn path.

## Density (design/DENSITY_STANDARD.md; agents build from this section)
| Item | This chapter |
|---|---|
| Story/boss/rival fights (≥4) | **Gym 16 Nyx** (double) · **Kroll or Quent** (Sun Court) · **the barricade** (PC + Mother Gutter vs a Directorate pair) · **the Drowned Spires guardian** (a Gilder-machine Golurk, trainer-boss) (all critical) · optional: **Amaria + Titania** ("Deliverer"), Mother Gutter's ledger fight |
| Route/gym/dungeon trainers (12–20) | 17 (roster at the end): the Brink 2, the Hanging Stair 3, the Drownings 3, Under the Drownings 2, Ironbloom 1, Gym 16 6 (GYM_PUZZLES) |
| EventMons (≥3) | **Morpeko "Market Day"** (gift, a Moon Market vendor) · **Relicanth "Old Gilder"** (static, the Drowned Spires, chained to a Gilder pillar) · **Klefki "Doorkeeper"** (static, the Calloway door in the Air Halls) |
| Hangouts (2–4) | Nyx in the Moon Market · Sahar on the dive barge · Edda at the Sump Docks · Ysolde on the lantern stair (after V138 >= 11) |
| Glassfall Slivers (4–6) | 5: the Brink's cairn, the Hanging Stair's scrap-tower, under a Moon Market stall (for a price), Under the Drownings' seabed, the heart of Ironbloom |
| Trials quests (≥3) | `ZE_LETTERS_DOWN` (delivery) · "Dogs of the Moon Market" · "Mother Gutter's Ledger" · the "Deliverer" cameo (CAMEOS §6) |
| Badge overlay | Badge 16: `encounters_badgetiers.txt` tier for 820, 821, 822, 824 |

**No jokes** from the barricade (V138 0 → 1) until Nyx's "The Price" (V138 3), and none from the cradle (V138 7 → 8) to Brann's confession. Edda's last line on the docks isn't a joke.

---

# CHAPTER 17 — "The Drowned Crown"

**Chapter start:** V102 = 17, V138 = 0. Dawn. The supply-lift sets the PC and Rook down at Midstair (830), on the plateau's rim. Quest log: "Eighteen Roads": *Down into Nadir. The Underveil is burning. Gym 16.*

## Midstair (830) and the Brink (832, `:STORMFRONT`)
Midstair: a scaffold of stalled lift-cages. The union's strike banner hangs torn. Directorate traffic only. Rook, at the cage: "I'm going back up. If I'm holding the footage I've got to be smiling on a screen by nine. If I leaked it — I've got nowhere to be. I'll go anyway. Somebody should be up there who saw this." *(He leaves on both branches; he's next on screen at the Festival.)*
- The Brink: the plateau's south-east lip, wind like a wall. To the south, the Drownings, the drained coast, mud flats to the horizon where the Sump used to be. In the mud, the tops of drowned towers: Aurelia's highest spires, which are Underveil.
- **Glassfall Sliver** in the cairn at the lip.
Trainers (Lv 70): a bird keeper, an ace trainer.

## Map 820 — the Hanging Stair (`:SCRAPYARD`)
A stair of scrap, chain and old lift-shafts bolted down the cliff. Refugees climbing *up* it with bundles, against the PC going down.
- A woman with a child on her back: "Don't go down. There's nothing down there but smoke and Nyx's people."
- **Glassfall Sliver** at the top of a scrap-tower (a climb puzzle of three chain-ladders).
Trainers (Lv 70–71): a worker, a punk, a Hollow runner going down with medicine.

## Map 821 — the Drownings (`:WATER_SURFACE`) and 822 Under the Drownings (Dive)
The drained south coast: mud, stranded boats, kelp drying in heaps, puddle-lakes. Fish-gutting sheds lean on stilts that used to stand in water. The tide-line is a hundred yards out and still going back.
- A mudlark: "Sump went in a night. Fault pulled the plug. Everything the Barons ever dropped in it's lying out here. Guns. Bones. A piano. I'm keeping the piano."
- **Under the Drownings (822):** the shallows where it's still deep enough to Dive. Kelp, old hulls, Relicanth. **Glassfall Sliver** on the seabed by a sunken barge.
- The **Accord Archive**'s sealed Coastwatch door is in the cliff here (the branch; see below).
Trainers (Lv 71): 821: a fisher, a swimmer (in the puddle-lakes), a mudlark *(Ruin Maniac)*. 822: 2 divers *(Swimmers)*.

## Underveil: **the barricades** (autorun at the Lantern Tiers gate, 420, V138 == 0 → 1)
```
(Underveil. A city of lanterns built in the upper towers of drowned Aurelia, in permanent night under the Dread Plate. This morning: smoke. Broken lanterns in the gutters. Directorate barricades of lift-cage grilles across the stairs.)
(Bodies under sheets along the Tier wall. A lot of them. People sitting next to them.)
(At the first barricade, a vast Muk fills the stair like a wall of tar. On top of the barricade, a fat old woman in a waxed coat with a ledger under one arm: Mother Gutter.)
[portrait: GUTTER, angry] Topsider! You're the ferry one. Good. Get up here. We've got a line coming and I've got one Muk.
```
**The barricade fight** (critical): PC + Mother Gutter vs a Directorate pair.
```
Script: pbRegisterPartner(:SUMP_BARON, "Mother Gutter", 17)
BATTLE: TrainerBattle.start(:MERIDIAN_DIRECTORATE, "Sergeant Mallory", :MERIDIAN_DIRECTORATE, "Officer Kade") — tag double; `:CORROSIVE_MIRE` (the Sump's mud); Lv 71–72.
(LOSE: whiteout to 421; the barricade restarts.)
[portrait: GUTTER, neutral] (the Muk oozing back over the stair) Held. For now. They'll come back with the line.
```
### ☠ **`GO_INTO_THE_LINE` "Into the Line"** (at the second barricade, 425, after the fight)
```
(Down the Barons' Stair: a Directorate line, shields locked, advancing on a crowd of unarmed Nadir protestors with lanterns and bedsheets painted with the names of the dead.)
(There's a gap between them. A few yards. Getting smaller.)
> Step between them? (1st)
  [name: Courier] (Nyx's, a boy with a moon earring, grabbing your sleeve) Not you. You're the one thing they want alive. Don't make them choose.
  > Step between them. (2nd)
    [name: Courier] (pulling) NOT YOU. Nyx said. Don't make them choose.
    > Step between them. (3rd)  Script: Prismfall.game_over(:GO_INTO_THE_LINE)
    > Stay back.
  > Stay back.
> Stay back.
(Stay back:) (The line stops a yard short of the lanterns. Nobody knows why. Then a bell rings from the Bell Tower of Aurel, once, and the line steps back. Somebody up there has a lot of people with lanterns.)
V138 = 1.
```
*(NARRATIVE_KEYS §9 epitaph: "They didn't choose. The bullet did. Meridian called it a tragic accident, and meant it.")*

## The Moon Market: **Nyx** (touch, the stall with no goods, 423, V138 == 1 → 2)
```
(The Moon Market: a cavern-street of stalls selling things that aren't there: secrets, names, the way into places. Half the stalls are shut today. The ones that are open are selling bandages.)
(At a stall with no goods at all, in silk with soot on it, a crescent-moon earring, sleeves rolled to the elbow and blood on them that isn't hers: Nyx Calloway.)
[portrait: NYX, neutral] Sweetheart. You came down. Everyone else went up.
[portrait: NYX, neutral] I've been carrying bodies since midnight. Forty-one. I've been counting, the way that ice-woman counts. It doesn't help. I thought it might.
[portrait: NYX, angry] Underveil isn't on the Accord's maps, sweetheart. That's the point of Underveil. Apparently it's also why nobody comes when they shoot us.
(She wipes her hands on a cloth, slowly, one finger at a time.)
[portrait: NYX, neutral] This afternoon we're doing something stupid. Come and watch. You'll like it. Everyone likes stupid when it's brave.
V138 = 2.
```
- **Hangout, Nyx in the Moon Market** (from V138 >= 2): *Secrets for Sale.* Each visit sells one rumour for money or for a secret of the PC's (Codex lore; the "secret" options are jokes until S148). After the Purge, she sells nothing for money.
- **`ZE_LETTERS_DOWN` delivery:** the letters carried from Cogsworth (Ch16) go to five doors on the Lantern Tiers. The last is "Mum, Underveil, the green door". The green door is open and the house is empty. A neighbour: "She went to the barricade with a frying pan. She's fine. She's at the barricade. With a frying pan." The PC gives the letter to the neighbour. Reward as catalogued.
- **"Dogs of the Moon Market"** and **"Mother Gutter's Ledger"** open (as catalogued; Mother Gutter's has her fight: `SUMP_BARON` Mother Gutter, Lv 73, Muk-line).
- **Gift: Morpeko "Market Day"** (Lv 45, Hunger Switch) from a vendor whose stall burned: "It eats when it's scared. It's been eating since midnight. Take it somewhere quieter. Is anywhere quieter?"

## The Moon Market steps: **independence** (autorun at 15:00, V138 == 2 → 3)
```
(The Moon Market steps. Every Sump Baron in Nadir, in their best coats, some of them bandaged. A crowd that fills the cavern-street to the walls, lanterns held up.)
(Nyx at the top of the steps, a sheet of paper in one hand, not reading from it.)
[portrait: NYX, neutral] Zenith says we're lawless. Fine. Then we'll have our own law.
[portrait: NYX, neutral] From this hour, Nadir is no part of Zenith. Not its Sump, not its slag, not its lifts, not its Directorate. We are the Undercity, and the Undercity is independent.
[portrait: NYX, smug] It means nothing. No crown will recognise it. The Accord won't read it. We know.
[portrait: NYX, angry] Say it anyway.
(The cavern says it back. It doesn't mean anything. It's the loudest sound you've ever heard.)
Switch S149 CH17_NADIR_INDEPENDENT = ON. Variable V111 NADIR_STATE = 3. V138 = 3.
```
- **Comedy scene Ch17, "The Price"** (15_COMEDY as written) is available at Nyx's stall from here until Gym 16. It's the chapter's first joke since the barricade, and it lands because of that.

## Gym 16 — the Hall of Whispers (430–434, `:NEW_MOON`)
As written in GYM_PUZZLES Gym 16:
| Map | Room | Role |
|---|---|---|
| 430 | Vestibule | teach: sight in the dark |
| 431 | Gallery of Shadows | twist |
| 432 | the Vault | combine: "knowledge moves the walls" |
| 433 | the arena | — |
| 434 | the Ledger | Mastery, optional |

Gym trainers (6): Burglar ×2, Gambler, Rocker, Hollow Defector, Informant (Lv 71–74).

### 433 — the Warden Arena (double; illusions on both sides)
```
[portrait: NYX, smug] Everything has a price, sweetheart. Yours just went up.
[portrait: NYX, neutral] Nothing on my field is what it looks like. Neither am I. Neither are you, I suspect. Let's find out which of us is better at it.
BATTLE: Prismfall.gym_battle(16, double: true)
```
- **Mid-battle (Zoroark's illusion breaks):** "Oh, look. The mask comes off. It always does." `[bubble: NYX, smug, sparkle]`
- **Win:**
```
[portrait: NYX, neutral] (laughing, tired, a hand over her eyes) Paid in full.
RECEIVE: the VEIL BADGE (badge 16). RECEIVE: TM79 DARK PULSE.
V138 = 4.
```
*(The badge name is a proposal: the **Veil Badge**. The VS plate reads SHADOW BROKER above NYX.)*

## After the gym: **Nyx's bargain and confession** (touch, Nyx at the Ledger door, V138 == 4 → 5)
```
[portrait: NYX, neutral] Business. I have something you want. Meridian's install plans for the new Festival arena. Every cable, every lock, every room under the stands. Somebody at Strade sold them to me last month, which tells you what Strade thinks of its future.
[portrait: NYX, smug] The price is a secret. Yours. The real one. The one you don't know yet, sweetheart, but you will by tonight. I want to know it first.
```
```
> Trade your secret. (trade)
  Script: pf_choose(:ch17_nyx, :trade)
  [portrait: NYX, happy] Lovely. I'll collect when you have it. You'll know when. (She gives you a roll of oilcloth.)
  RECEIVE: ARENA SCHEMATICS (Key Item).
  [portrait: NYX, neutral] Don't look so worried. I only sell secrets to people who deserve them. I've never once sold one to someone who didn't. (A pause.) I've never once *not* sold one.
> Refuse. (refuse)
  Script: pf_choose(:ch17_nyx, :refuse)
  [portrait: NYX, deadpan] (a shrug) Then I'll help anyway, badly, at the worst possible moment, and it'll cost me something. That's how it goes with people I like. Off you go.
```
*(NARRATIVE_KEYS: `:trade` NYX+4 → `NYX_PRECISE` (Ch21: she cuts Meridian's comms precisely); `:refuse` NYX−2 (Ch21: she helps sloppily and is injured).)*
```
(As you turn to go, she says it, not to you, to the Ledger door.)
[portrait: NYX, sad] Two years ago I sold Voss the way into the Sun Court. It's my family's door. The Calloways have kept that door shut for three hundred years. Not a lock. Just us, not telling.
[portrait: NYX, sad] I told myself it was just a door. Everything's just a door, if you're selling it. (A beat.) I'm the one who opened it.
V138 = 5.
```

## Branch: **the Accord Archive** (838, `:MINDSCAPE`; only if `standing(:ACCORD) >= 4`; the Coastwatch door on the Drownings, V138 == 5 → 6)
```
(A sealed Coastwatch vault in the cliff of the Drownings, dry for the first time in three hundred years. Inside: shelves of oilskin cases. At a reading-desk, by a lamp, waiting for you: a big man in a smith's leather apron over a Warden's coat. Brann Holloway.)
[portrait: BRANN, neutral] Ilsa said you'd be along, if you were the sort to be let in here. You're the sort. Sit. I'll tell you, and then you can hit me if you like.
```
**Brann's confession, early and gently** (the same facts as at the docks; this version is softer, and he says it first):
```
[portrait: BRANN, sad] The Concordance's Secret Articles. These are the originals. Maren's hand. Read them, or let me read them to you, it's quicker.
[portrait: BRANN, neutral] The Tuning is real. Every Festival, the Crown sings the Plates into tune, and it costs the one who wears it. It kills Sovereigns. Slowly. That's what the Accord's for. Not peace. Replacement.
[portrait: BRANN, sad] After the Fracture I reset the Crown's stone. I'm the only man alive who can. I knew it was short. A splinter short. I never asked where the rest went. I made very sure I never asked.
(He looks at your chest. You haven't told him. He looks anyway.)
[portrait: BRANN, sad] Valen's arm is crystal to the shoulder. He has weeks. Maybe the Festival.
[portrait: BRANN, neutral] (taking a page from an oilskin case: old vellum, a song in a cramped hand, the notes written as colours) The Hymn of Return. Maren's own copy. The Hollow have most of it. Nobody has all of it. Now you've got the first page. Keep it dry.
RECEIVE: MAREN'S HYMN PAGE (Key Item).
V138 = 6.
```
*(09 #5/#11. With the Archive branch done, the docks scene (V138 12) plays its short form. The Secret Articles in the PC's Bag (Ilsa's, Ch13) are the same text, so "Now you know what you've been carrying" is Brann's last line here. Don't name the Legend Plate yet: the cradle comes next.)*

## The dive into Aurelia (from the Sump Docks, 424; touch, Sahar on the barge, V138 >= 5 → 7)
```
(The Sump Docks. A dive barge with a Gale Post flag, Edda at the tiller, smoking. On the deck, in a brass-helmeted dive suit with the helmet under her arm and her hair tied up in a scarf: Sahar Ostrand.)
[portrait: SAHAR, happy] Three hundred years. I've waited my whole *life*. (She checks the suit's seals three times.) Bastian sends his love. He said "eh?" when I asked if he had a message, so I made one up.
[portrait: EDDA, neutral] Rules. You go down, you come up. Anybody who doesn't come up, I don't wait for. That's not cruelty, that's tide tables.
[portrait: SAHAR, worried] And don't touch anything gold. *Anything.* I'm serious. The Gilders made gold that *wants* things.
V138 = 7.
```
- **Hangouts:** Sahar on the dive barge (from V138 >= 7): *Field Notes*, Aurelian history in her voice, one site per visit. Edda at the Sump Docks: *Tide Tables*, and the smuggler's stock.

### Map 824 — the Drowned Spires (`:UNDERWATER`, Dive)
Golden terraces under green water. Gilder machines rusted into coral. Statues of the Gilded King, life-size and huge, with their faces chiselled off.
- **Relicanth "Old Gilder"** (static, Lv 72, Rock Head): chained by the tail to a golden pillar with a Gilder chain, alive, very old. Breaking the chain (interact) frees it. It stays and battles to be caught. *(It's not legendary. It's three hundred years old.)*
- **The spires' guardian** (critical): a **Gilder-machine Golurk** wakes on a terrace and blocks the throne-vault gate. It's a trainer-boss with no trainer: `TrainerBattle.start(:GILDER_AUTOMATON, "Terrace Warden")`, single, `:UNDERWATER`, Lv 73 (Golurk / Bronzong / Klinklang, all "Gilder-made"). Sahar: "It's still guarding. Three hundred years. Nobody told it." On defeat, it kneels and its eyes go out.

### Map 825 — the Air Halls (`:CAVE`)
Air pockets inside the flooded palace: dry halls where the sea never got in, smelling of three hundred years. Wild Pokémon at Lv 70–74.
- **The Calloway door**: a plain iron door in a golden wall, with no handle and no lock, scratched with a crescent moon. It's open. Beyond it is a short dry stair, the way Voss came. A Klefki hangs on the hinge: **Klefki "Doorkeeper"** (static, Lv 72, Prankster). "It's been holding the keys to a door with no lock for three hundred years. It doesn't understand that either."

### Map 826 — the Gilded Throne Vault: **the Sun Court** (V138 == 7 → 8; key event 1)
```
(The Sun Court. A round hall, dry, gold from floor to dome. On every wall, murals, gold and lapis and glass, three hundred years old and as bright as yesterday.)
(Sahar walks along them with her lamp, reading, not breathing.)
```
**The murals** (six panels, an interact each; Sahar reads; plain story text):
1. *The Blight: the fields of Velmora grey, the people starving.*
2. *The Two Weathers: a red giant and a blue giant under a king with a gold chain, the land torn between flood and drought.* Sahar: "The red one and the blue one. Duneholt's glyphs. Isenmar's sea. It was *him*."
3. *The Chain: a god of every colour, kneeling, bound in gold, under the same king.*
4. *The Calling: eighteen figures in Choir white singing, the god listening.*
5. *The god breaking itself: the colours flying out of it in eighteen directions, a city falling into the sea.*
6. *A girl in a torn crown, in the wreck of a golden hand, pulling something out of it: a splinter of no colour at all. Princess Maren.*

```
(In the middle of the throne room: a golden hand, open, palm up, the size of a door. The keystone cradle. Its fingers are broken at the tips, as if something was torn out of them.)
(You step towards it. Under your collar, the scar goes hot, then cold, then not a temperature at all.)
[anim: the PC's sprite glows from the chest; the throne room lights up with eighteen faint colours, one after another round the walls, like lamps being lit; a long chord SE]
(Your chest is glowing through your shirt. The Sun Court is lit in eighteen colours. The cradle's broken fingers are lit too, at the tips, where something used to be.)
(Behind you, on the stair from the Calloway door, someone breathes in.)
[portrait: NYX, shocked] (she came down after all, soaking wet, in somebody's borrowed dive suit) Oh.
[portrait: NYX, sad] Oh, darling. You're the missing piece.
(Sahar, on her knees at the cradle's base, holding her lamp up to an inscription in old Aurelian, reads it out in a voice that isn't quite working.)
[portrait: SAHAR, neutral] "Here rests the One that is every color and none."
[portrait: SAHAR, sad] It's the Legend Plate. The god's heart. The one that held the other eighteen together. (She looks up at you.) You've got a piece of it. In you. The piece that's missing from this hand.
\pf[PLAYER,neutral] (Your fourth authored line.) ...I know. I think I always knew. I just didn't have the word.
Switch S148 CH17_SHARD_NAMED = ON. V138 = 8.
```
*(The first time the game names the shard. S148 drives the dialogue swaps everywhere from here: the NULL scan, Larch's "sums", Brann's "short", the Wardens' Circular. Ilsa's "keep it" line (Ch13) pays off in Ch18. **Nyx collects here on `:trade`:** "...I'll take that secret now. I'm sorry. I'm keeping it anyway." No mechanical change.)*

### ☠ **`GO_THE_THRONE` "The Throne"** (an exploration prompt at the throne, any time while V138 is 8–9)
```
(The Gilded King's throne, behind the cradle. Gold. Its armrests are shaped like open hands, palm up.)
> Sit on the throne? (1st)
  [portrait: SAHAR, panic] Don't touch anything gold. *Anything*. Please. I mean it more than I've ever meant anything.
  > Sit. (2nd)
    (The armrests' fingers twitch.)
    > Sit. (3rd)  Script: Prismfall.game_over(:GO_THE_THRONE)
    > Don't.
  > Don't.
> Don't.
```
*(NARRATIVE_KEYS §9 epitaph: "You fit perfectly. That was the problem the Gilders were trying to solve.")*

## **Voss in the Sun Court** (autorun as the far wall is cut, V138 == 8 → 9; key event 2)
```
(A cutting-torch, white, through the far wall. A Meridian salvage crew in pressure suits steps through the hole into the air pocket. Among them, in a pressure suit with the helmet off under his arm, his hair perfect: Aurelian Voss.)
[portrait: VOSS, happy] (seeing you, lit up in eighteen colours, delighted) Oh, look at that. Oh, *look* at that. Ten years of telemetry and it's nothing to seeing it in person.
[portrait: VOSS, neutral] You'll want the story. Everyone does, at the end. Let me tell it properly.
[portrait: VOSS, neutral] House Aurel. My family. We changed the name and kept the grudge. When the Princess broke the chain, my ancestors were the King's engineers. We went up the cliffs with our tools and our notebooks and we waited.
[portrait: VOSS, neutral] I was eight when my grandfather showed me Theodric's notebooks. I was twenty-two when I realised he was right about everything except the chain. Metal was the wrong material.
[portrait: VOSS, neutral] AF 290. My array. My dials. I was trying to measure the convergence. I didn't know it would break the Crown. I was very sorry about the forty people.
[portrait: VOSS, happy] I was even sorrier when I understood what I'd learned.
[portrait: VOSS, neutral] The Lowlight? Twelve people. I've lost more to the Bleed in a quiet week. I made those twelve *mean* something.
[portrait: VOSS, neutral] Gods are absentee landlords. Arceus dropped its furniture on our heads three hundred years ago and never came back. I'm not trying to become a god. I'm trying to make sure we never need one again.
(He holds out his hand. Not to shake. Open, palm up, like the cradle.)
[portrait: VOSS, neutral] Stand with me at the Festival. When it's done, no child in Velmora will ever be Fixed again.
[portrait: VOSS, sad] Your mother wilted in exile because of a broken god. I can fix the god.
```
*("Your mother" is Ines. He knows, and has always known. The PC saw her singing in the Cathedral echo (Ch15); Ch18 tells them she was their mother.)*
```
> Refuse. (refuse)
  Script: pf_choose(:ch17_voss_offer, :refuse)
  (You don't take the hand.)
  [portrait: VOSS, neutral] (lowering it, not offended) Of course. You've only known for five minutes. I've known for twenty-five years. I'll ask again when you've caught up.
> Feign agreement. (feign)
  Script: pf_choose(:ch17_voss_offer, :feign)
  (You take the hand. His grip is warm and very steady.)
  [portrait: VOSS, happy] There. Was that so hard? (He doesn't let go for a second too long.) I know you might be lying. Everyone's lying, at the start. Come to the Festival anyway.
> Accept. (accept)
  Script: pf_choose(:ch17_voss_offer, :accept)
  (You take the hand, and you mean it. You can feel that you mean it. So can he.)
  [portrait: VOSS, sad] (very quietly, for a moment not performing at all) ...Thank you. Nobody's ever said yes before. (Then the smile comes back.) Win your badges. We'll talk about the details.
V138 = 9.
```
*(NARRATIVE_KEYS: `:refuse` VOSS−2; `:feign` VOSS+2 → `VOSS_FEIGNED` (he lets you close in the finale; risky with high Meridian Standing and live telemetry); `:accept` VOSS+3 MERIDIAN+3 NYX−2 RES−1 → `VOSS_ACCEPTED` (opens Concord Dawn; `:ch21_hand`).)*

### **Admin battle: Kroll, or Quent** (autorun as the crew rigs the cradle, V138 == 9 → 10)
```
(Behind Voss, the salvage crew is fitting cables to the golden hand. A winch on the far side of the hole starts to take up slack.)
[portrait: VOSS, neutral] I'll leave you with someone. Don't take it personally. They're holding the door, not you.
[if !KROLL_EXPOSED_CH13]
  (Out of the crew steps a woman in a pressure suit with a Hollow tattoo on her wrist, half-covered: Sabine Kroll.)
  [portrait: KROLL, smug] Still nobody knows. Not really. You'd be amazed what people won't believe, even on tape.
  BATTLE: TrainerBattle.start(:MERIDIAN_KROLL, "Sabine", 1) — `:CAVE` (one quake cracks the ceiling, the next brings it down: 1/8 Rock-scaled to all).
[if KROLL_EXPOSED_CH13]
  (Out of the crew steps a tall man in a pristine pressure suit, as if a pressure suit could be pristine: Percival Quent.)
  [portrait: QUENT, happy] Your readings are *astonishing* right now. Do hold still. Oh, you won't. Very well.
  BATTLE: TrainerBattle.start(:MERIDIAN_QUENT, "Percival", 2) — `:CAVE`.
(LOSE: whiteout to 421; the Sun Court restarts at Voss's arrival, the offer kept.)
(WIN:) (Behind them the cradle is gone: winched out through the hole, the hand closing as it went, broken fingers and all.)
[portrait: VOSS, neutral] (from the hole, helmet going on, his voice on the suit speaker now) Win your badges. I'll see you at the coronation.
(A Meridian submarine's lights, outside, in the green water, turning away.)
Switch S147 CH17_AURELIA_DONE = ON. V138 = 10.
```
*(The cradle is the Arbiter Engine's keystone cradle (Ch16's blueprints: "to be recovered from site AURELIA"). It's now Voss's.)*

## Optional: **"Deliverer"** (CAMEOS §6; after Gym 16, before leaving Underveil; Edda's divers' report)
As in CAMEOS §6: a short underwater maze in the Drowned Spires' lower galleries. Amaria sits in a flooded Gilder hall singing to her Lapras; Titania paces the shallows above. Amaria: "This city isn't dead. It's *waiting*." *(A Ruin Route hint about Theodric's reflection.)* **Fight:** a double vs Amaria and Titania (Lv ~78, `:WATER_SURFACE`; aces Lapras "Deliverer" and Aegislash). After it, they go home through the Glass. *(Cameo teams per CAMEOS. Cameos are trainers, so the no-legendaries rule doesn't apply.)*

## Optional: **Ironbloom** (828, `:BLEED`)
Rust that flowers: a flooded Gilder foundry where the iron has grown petals in the Bleed. Wild Pokémon at Lv 71–74. **Glassfall Sliver** at the heart of the biggest rust-flower. Trainer (Lv 73): a scientist cataloguing the flowers ("They're iron. They're also, measurably, alive. I've stopped writing 'impossible' in my notes. I just write 'Tuesday'.").

## Underveil, evening: **Ysolde's lanterns** (autorun on surfacing at the Sump Docks, V138 == 10 → 11)
```
(The Moon Market steps, at dusk. All the way up them, a lantern on every step, lit. At the top, with a cart of Gravenmoor lanterns and Nyx's people handing them up the line: Ysolde.)
[portrait: YSOLDE, neutral] One for each. Forty-one. The Hospice sent them down. We're good at this in Gravenmoor. It's the only thing we're good at.
[portrait: YSOLDE, sad] (lighting the last one, not looking at you) Is he eating? Kestrel. You'd know better than I would.
(You don't know. You tell her you don't know. She nods, as if that was an answer too.)
V138 = 11.
```
- **Hangout, Ysolde on the lantern stair** (from V138 >= 11).

## The Sump Docks: **Brann** (autorun, V138 == 11 → 12)
```
(The Sump Docks, night. A big man sitting on a bollard with his hands between his knees, waiting: Brann Holloway, come from Crownhaven on the night lift.)
[if made Archive branch]
  [portrait: BRANN, neutral] You've had it from me once, in the dry. I'll not make you hear it twice. One thing I didn't say.
  [portrait: BRANN, sad] I knew it was you. In the Archive. Before the cradle. I looked at you and I knew where the rest of my stone went. I should've said.
[else]
  [portrait: BRANN, sad] I'll tell you the truth. I should have done it in Cindervault. I'm a coward about the truth, it turns out. It's the only thing I'm a coward about.
  [portrait: BRANN, neutral] The Tuning is real. Every Festival, the Crown sings the Plates into tune, and it costs the one who wears it. It kills Sovereigns.
  [portrait: BRANN, sad] After the Fracture I reset the Crown's stone. I knew it was short. I never asked where the rest went. (He looks at your chest. It's still glowing faintly, under your coat.) I don't have to ask now.
[portrait: BRANN, sad] Valen's arm is crystal to the shoulder. He has weeks. Maybe the Festival.
[portrait: BRANN, neutral] He sent me with a message. Word for word, he said. So: "Win your last two badges. Then come to me, and I'll tell you everything."
V138 = 12.
```
*(09 #11/#24. Brann's forge thread (`AS_FORGE_REMEMBERS`) takes the confession as known from here: "Don't tell me" lands harder.)*

## The Underveil docks: **"Thirty days"** (END OF ACT IV; autorun, V138 == 12 → 13)
```
(Night on the docks. Lantern-light. Crates for chairs. Nyx, Sahar wrapped in a blanket, Edda with her pipe, and, if he came down, Rowan, at the edge of the light. [if ROWAN_ALIVE]) (The water black and still where the Sump used to be. Far down in it, faint: eighteen colours, very faint, and then nothing.)
[portrait: NYX, neutral] (counting on her fingers) Meridian wants you in that arena. The Accord wants you in that arena. The Hollow wants you in that arena.
[portrait: NYX, neutral] Two kings want you as *their* champion in that arena.
[portrait: NYX, sad] Thirty days, sweetheart. Every power in Velmora is waiting for you to walk into one room.
(Nobody says anything for a while. The lanterns on the steps above burn down one by one.)
[portrait: EDDA, neutral] (knocking out her pipe on the crate) Then we'd best make sure you walk in on your own feet.
V138 = 13. Variable V101 STORY_ACT = 5. Variable V102 STORY_CHAPTER = 18.
[anim: fade to black; title card]
END OF ACT IV.
V — SOVEREIGN
```
*(Act V opens in Ch18, "The Gloaming". The PC learns the name Ines, Kestrel takes Morwen's Ring (`:ch18_kestrel_ring`), and there's Pecharunt and the full Hymn.)*

---

## Map events needed (Chapter 17)

None of this chapter's maps is built. **[NEW]** = an event or map not in maps.json. V138 = **CH17_STEP** (design/FLAGS.md). Maps go through the three-pass workflow (design/MAPGEN.md, top).

**830 Midstair** (`:SCRAPYARD`): stalled cages, the torn strike banner; Rook's goodbye (on arrival).

**832 The Brink** (`:STORMFRONT`):
- wind gusts (screen shake 1, intermittent);
- the Drownings panorama;
- **Sliver #1** at the cairn;
- 2 trainers.

**820 The Hanging Stair** (`:SCRAPYARD`):
- chain-ladders;
- refugees climbing up (looping move routes);
- the scrap-tower climb (**Sliver #2**);
- 3 trainers.

**821 The Drownings** (`:WATER_SURFACE` in the puddle-lakes; mud elsewhere):
- stranded boats, the mudlark's piano;
- **the Coastwatch door** to 838 (opens only if `standing(:ACCORD) >= 4`; otherwise a sealed-door message);
- 3 trainers.

**822 Under the Drownings** (Dive):
- kelp, hulls;
- **Sliver #4** by the barge;
- 2 trainers.

**420 Lantern Tiers / 421 Center / 422 Mart:**
- smoke tint, broken-lantern decor, sheeted bodies along the wall (decor events);
- **the first barricade** (Mother Gutter; tag battle; V138 0 → 1, via 425);
- the `ZE_LETTERS_DOWN` doors ×5 (the green door);
- Mart: Badge-16 stock, Dusk Balls, Black Glasses.

**423 Moon Market:**
- the stall with no goods (Nyx: V138 1 → 2; her hangout; "The Price"; the bargain V138 4 → 5);
- the independence autorun on the steps (V138 2 → 3; a crowd of 30+ lantern events; S149, V111 = 3);
- the burned stall (**Morpeko "Market Day"** gift);
- "Dogs of the Moon Market" and "Mother Gutter's Ledger" givers;
- **Sliver #3** under a stall (sold by a vendor for one rumour);
- the lantern stair at dusk (Ysolde: V138 10 → 11; 41 lantern events lit in sequence).

**424 Sump Docks:**
- the dive barge (Sahar: V138 → 7; her hangout);
- Edda's hangout;
- Brann on the bollard (V138 11 → 12);
- **the closing scene** (V138 12 → 13; title card; V101 = 5, V102 = 18).

**425 Barons' Stair:**
- **the second barricade**: the Directorate line advancing (shield-wall events stepping forward on a timer), the protestors with lantern-sheets;
- **`GO_INTO_THE_LINE`** (three prompts, the courier's warnings);
- the bell (Bell Tower 426: an SE plus the line stepping back).

**430–434 Gym 16:** as GYM_PUZZLES; 6 trainers; Nyx double (433); V138 = 4.

**838 Accord Archive** [branch] (`:MINDSCAPE`):
- oilskin shelves;
- Brann at the reading desk (V138 5 → 6);
- MAREN'S HYMN PAGE.

**824 Drowned Spires** (`:UNDERWATER`):
- terraces, Gilder machines in coral, defaced statues;
- **Relicanth "Old Gilder"** chained to a pillar (break the chain, then a static battle);
- **the Terrace Warden** (a Gilder Golurk event that wakes on approach; the `GILDER_AUTOMATON` battle; it kneels on defeat);
- the "Deliverer" maze (cameo; after Gym 16).

**825 Air Halls** (`:CAVE`):
- dry halls;
- **the Calloway door** (crescent-moon scratch; open);
- **Klefki "Doorkeeper"** static on the hinge.

**826 Gilded Throne Vault / the Sun Court:**
- six **mural** interact panels (Sahar reads);
- **the keystone cradle** (a golden-hand event; the glow sequence: a PC tint and glow overlay, 18 coloured lamp events lit round the walls, a chord SE; S148; V138 7 → 8);
- **the throne** (`GO_THE_THRONE`, three prompts);
- the far wall cut by a torch (a picture/flash; the salvage crew and Voss enter: V138 8 → 9, the offer);
- **Kroll or Quent** (by `KROLL_EXPOSED_CH13`; V138 9 → 10; S147);
- the cradle winched out (a move route through the hole);
- the submarine lights (a picture).

**828 Ironbloom** (`:BLEED`):
- rust-flowers (animated tiles);
- **Sliver #5**;
- 1 trainer.

## Trainer roster (Ch17; 17 regular trainers; PBS blocks in 3 versions; ≤ 75)
| Map | Class (stock type) | Name | Lv | Team idea (field touch) |
|---|---|---|---|---|
| 832 | Bird Keeper | Wren-of-the-Brink *(no relation)* | 70 | Corviknight, Kilowattrel, Braviary (Stormfront: Flying and Electric loved) |
| 832 | Ace Trainer | Ottoline | 70 | Garchomp, Rotom-Wash, Kingambit |
| 820 | Worker | Lift-hand Cobb | 70 | Copperajah, Machamp, Excadrill |
| 820 | Punk *(Guitarist)* | Ruin | 71 | Skuntank, Toxtricity, Scrafty |
| 820 | Hollow Runner *(HOLLOW)* | Medic Iver | 71 | Amoonguss, Gardevoir, Hariyama |
| 821 | Fisherman | Old Sim | 71 | Gyarados, Barraskewda, Wishiwashi |
| 821 | Swimmer | Pell-the-Elder *(Cragholm's Pell's grandmother)* | 71 | Lapras, Cramorant, Drednaw |
| 821 | Mudlark *(Ruin Maniac)* | Garnet | 71 | Quagsire, Golurk, Gastrodon |
| 822 | Swimmer ×2 | Divers Nell and Ash | 72 | Kingdra, Dhelmise / Lanturn, Barbaracle |
| 828 | Scientist | Dr. Rennick | 73 | Ferrothorn, Magnezone, Klefki |
| **Gym 16** | Burglar ×2, Gambler, Rocker, Hollow Defector, Informant | (GYM_PUZZLES) | 71–74 | as GYM_PUZZLES |

**Story fights (new PBS unless noted):**
- `SUMP_BARON` Mother Gutter (**a new trainer type, "Sump Baron"**): a partner block, version 17 (Muk, Toxapex, Skuntank, Lv 71–72), and a ledger-fight block (Lv 73).
- `MERIDIAN_DIRECTORATE` Sergeant Mallory and Officer Kade (Lv 71–72: Arcanine, Corviknight / Magnezone, Mabosstiff).
- `GILDER_AUTOMATON` "Terrace Warden": a new trainer type, "Gilder Automaton", no sprite (an event-sprite VS). Lv 73: Golurk, Bronzong, Klinklang.
- Kroll v1 / Quent v2: existing.
- Gym 16: existing.

**Items owner:**
- **Key Items:** ARENA SCHEMATICS (`:trade`), MAREN'S HYMN PAGE (Archive).
- **Badge, TM, Slivers:** the VEIL BADGE (proposed), TM79, Glassfall Slivers #1–5 of the Ch17 allotment.
- **Mastery (434):** Magical Seed ×2 + Black Glasses.

**EventMons:** Morpeko "Market Day" (gift, Lv 45), Relicanth "Old Gilder" (static, Lv 72), Klefki "Doorkeeper" (static, Lv 72).

**Portrait requests (art, to Gemini):** **MOTHER GUTTER** (`neutral`, `angry`, `happy`); NYX `sad`; SAHAR `panic`; VOSS in a pressure suit (variant).
