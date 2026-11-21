# Script: Chapter 5 — "Ten Years of Light" (the Lock Road, Lumen City, Gym 4, the Gala and the Lowlight Shatter)

> **Final playable script** for Chapter 5, the end of Act I. It covers the Lock Road out of Ebbmouth (580 the Reedholms, 592 the Icecutters' Haul, 590 Brassfall, 581 the Icefall Locks, 595 Coppice Ride, 594 Wallshadow Row, 593 the Arc-Lamp Mile, 582 Lumen West Gate; optional 584/585 the Voltaic Sluiceworks and 588 Ebb Hollow), Lumen City (180 the Concourse, 181 the Lowlight, the Circuit Gym 190–193, Meridian Spire 185/186 and two new rooms below it), the Lowlight (Shattered) 608, and Interlude I at the Ferrow Lighthouse (105/106). None of these maps is built yet (map builder 15 is building them); **the "Map events needed" list at the end is what to build from.**
> Follows `story/23_SCRIPT_CH4.md` and uses the conventions of `story/20_SCRIPT_CH0-2.md`.
> Sources: 04_ACT_I Ch5 and Interlude I, 05_ACT_II (the Act II opener), 03_CAST, 09_MYSTERIES (#2, #4, #8, #12–15, #17, #21, #23), 10_CHOICES_ENDINGS / NARRATIVE_KEYS (`:ch5_lowlight_testimony`, GO_LIVE_WIRE), 13_CUTSCENES (portraits), 15_COMEDY (Ch5 "Chat Has Opinions"), 14_WAR_AND_BLESSING, GYM_PUZZLES Gym 4, TRIALS_QUESTS (`ZE_OCTAVE_OFF_BEAT`, `ZE_CUSTOMER_SUPPORT`, `ZE_FIZZBOLT`, `ZE_ROTOM_RECALL`), ROUTES.yaml (the Lock Road), `design/CHAPTER_BEATS.md`.
> **Key events (CHAPTER_BEATS):** 1. **the Lowlight Shatter** (twelve named people Fixed in glass, Dex among them); 2. **Valen sees the PC standing in the glass** and grants Meridian the Mandate, and the PC testifies (`:ch5_lowlight_testimony`). Everything before the Gala is build-up for these: the twelve are met alive on 181 first, and the Plate's empty cradle is seen in Rook's gym. **Nothing comic after the raid starts** (15_COMEDY §1).

*(The chapter's scenes are written above the map list; see the sections below.)*

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

**New items** (items_prismfall.txt owner): `GALAINVITATION`, `ICEBOUNDSATCHEL`, `HEATCONTRACT` (Key Items, descriptions in the script). **New boss** (BOSSES.md owner): "Overcharged" Electivire, 2 bars, Lv per the segment after Gym 4, field `:NEON_GRID` → `:BLEED` at the bar break (the first scripted any → Bleed). **Trials owner:** `ZE_OCTAVE_OFF_BEAT` lives on 181, which is replaced by 608 after the Shatter: close it with a line if unfinished, or move its offer to the Concourse (180).
