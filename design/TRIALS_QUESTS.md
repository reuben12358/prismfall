# TRIALS_QUESTS — every Trial quest, and the full script of the implemented ones

> **Generated** by `ruby tools/trials_docs.rb` from `plugins/Prismfall Trials/1xx_*.rb`. Edit the plugin data, not this file.
> Design of the institutions, ranks and boards: `design/TRIALS.md`. Event Pokémon: `design/EVENT_POKEMON.md`.
> Map IDs are current `maps.json` IDs (names change; IDs don't). Chapters and order follow SPINE Revision 14.
> **Status:** *wired* = scenes written and testable (map events in `design/TRIAL_EVENTS.yaml`); *designed* = `:stub`, off the boards until wired.

**80 quests** (22 wired, 58 designed) across 8 Trials.

| Trial | Quests | Wired |
|---|---|---|
| The Quiet Way (Elowen) | 19 | 14 |
| The Tally (Isenmar) | 10 | 4 |
| The Prize Exchange (Zenith) | 9 | 3 |
| The Gutter Book (Nadir) | 9 | 0 |
| The Trial by Flames (Ashkaar) | 9 | 1 |
| The Rolls of Unearthing (Ossaria) | 8 | 0 |
| The Rite of Reflection (Antumbra) | 8 | 0 |
| The Hall of Petitions (Crownhaven) | 8 | 0 |

## Part 1. Catalogue

### The Quiet Way — Elowen

| Quest | Ch | Unlock | Giver · where (map) | Rank · Rec Lv | What happens | Reward | Touches | Status |
|---|---|---|---|---|---|---|---|---|
| **The First Lesson** `EL_FIRST_LESSON` | 1 | `switch(103)` | Brother Teasel · the wayshrine by the Accord plaque (100) | ★ · 5 | Do one kind thing in Ferrow's Landing that nobody asked you to do. Then go back to Brother Teasel. | ORANBERRY x2; silent: RES+1; +2 pts | Resonance (Harmony +1 for keeping quiet); starts the realm-wide Quiet Deeds tally | wired |
| **The Tart Thief** `EL_TART_THIEF` | 1 | `switch(103)` | Wenna Hale · the tart stall on the quay (100) | ★ · 7 | Someone keeps stealing Wenna Hale's bramble tarts. Brother Teasel's note on the lantern: "The thief is hungry, not wicked." | $200, ORANBERRY x3; told: KESTREL-1; +2 pts | Kestrel bond (+1 if you split the evidence, -1 if you tell on him) | wired |
| **The Scarecrow Walks** `EL_SCARECROW` | 1 | `switch(103)` | Coll Hale · the Hale farmhouse (523) | ★ · 9 | Coll Hale's scarecrow keeps moving to a different field. Coll did not build a scarecrow. | caught: $300; spared: MIRACLESEED, RES+1; +2 pts | Resonance (Harmony +1 if you leave it be) | wired |
| **Master of Nothing** `EL_MASTER_OF_NOTHING` | 1 | `switch(101) && switch(103)` | the Dockmaster · the Dockmaster's House (107) | ★ · 6 | The Dockmaster wants to close the Dovetail's ledger properly. Something is still aboard. | POTION x2; +2 pts | none (a quiet one) | wired |
| **The Last Plank** `EL_LAST_PLANK` | 1 | `switch(103)` | the lantern rope (Brother Teasel's hand) · the empty ferry berth (100) | ★ · 6 | Every morning a Timburr carries a plank down to the empty berth and nails it in. Every night the tide takes it. Teasel's note: "Help it finish." | POTION x2; +2 pts | none (Fighting type before the Normal Gym 1) | wired |
| **The Tide-Pool Feud** `EL_TIDE_POOL_FEUD` | 2 | `switch(103)` | Dobbs the shell-gatherer · the shell-gatherers' steps on Lacecliff Walk (527) | ★ · 12 | A Crabrawler and a Clobbopus have been fighting over one rock for three days. The shell-gatherers can't reach the pools. | SUPERPOTION x2; +2 pts | none; the side you help punches open a sea-cave under the cliff (flag :sea_cave, items inside) | wired |
| **The Borrowed Lanterns** `EL_LANTERNS` | 2 | `switch(103)` | Sister Hollin · the Saltmere Lantern House (140) | ★ · 12 | The theatre district keeps 'borrowing' the Lantern House's lanterns as props. Five are missing before the Night of Floating. | SILKSCARF; left_one: $400, RES+1; +3 pts | Resonance (Harmony +1 if you leave the stagehand her lantern) | wired |
| **A Hole in the Sky** `EL_PAINT_LOFT` | 2 | `badges >= 1 && switch(108)` | Marguerite Fane · the Lantern Theatre paint loft (145) | ★ · 13 | The Mourner walked straight through the Pageant's painted sky. The scene-painter needs a new backdrop, and a second opinion. | +1 pts | none; the colours you pick decide the Smeargle's moves (Water, Fire, Grass or Ghost coverage) | wired |
| **The Sound of Saltmere** `EL_SOUND_OF_SALTMERE` | 2 | `badges >= 1; after EL_LANTERNS` | Sister Hollin · the Saltmere Lantern House (140) | ★ · 14 | A koan: find the sound Saltmere makes when nobody is performing. | +3 pts | Resonance (Harmony +1) | wired |
| **The Orchard Sings** `EL_GLASS_FOAL` | 2 | `badges >= 1 && switch(105)` | Brother Teasel · the Ferrow's Landing wayshrine (100) | ★ · 15 | Since your badge, folk on the orchard lane hear chiming at night, like hooves on glass. | MOONSTONE; +3 pts | Resonance (Harmony +1 if you approach slowly) | wired |
| **Three Loyal, Three Knots** `EL_THREE_KNOTS` | 3 | `badges >= 1` | Mother Aldreth · the Briarwick Lantern House (120) | ★ · 16 | A pilgrimage: re-tie the silk knots at the three wayshrines of the Loyal Three, and answer what each shrine asks. | MAGICALSEED x2; +3 pts | Lore seed for the Loyal Three / Ogerpon arc (story/04_ACT_I, Elowen legendary arc) | wired |
| **The Horn and the Pincer** `EL_HORN_AND_PINCER` | 3 | `badges >= 1` | the lantern rope (no one signed it) · the sap tree on the old trail, Gossamer Wood (524) | ★ · 15 | Two great Bug Pokémon are fighting over the sap tree on the old trail. The trail has been blocked for a week. | HONEY x2; +2 pts | none; the one you help clears a shortcut (Heracross tears a silk wall, Pinsir crushes a log) | wired |
| **The Silkthief** `EL_SILKTHIEF` | 3 | `badges >= 2` | Hett · the Weavers' Guildhall (123) | ★★ · 20 | Somebody is stealing finished silk straight off the drying racks at night. Hett has a theory, and it has eight legs. | $800; guardian: SILVERPOWDER, RES+1; +3 pts | Resonance (Harmony +1 if you leave the Spidops guarding the moths); Briarwick's moth tally board | wired |
| **Someone Apologising to Bugs** `EL_SHELLY` | 3 | `badges >= 2` | Mother Aldreth · the Briarwick Lantern House (120) | ★★ · 21 | A stranger with pink hair is lost in the Gossamer Deepwood, apologising to the Bug Pokemon. The spirits of the wood are uneasy. **Twist:** Board pointer to CAMEOS.md 'Lost in the Gossamer'. The cameo event calls Prismfall.cameo_battle(:FESTIVAL_SHELLY, "Shelly", 1, double: true) and then pf_quest_complete(:EL_SHELLY). Moved from 'after Gym 1' to 'after Gym 2' by SPINE Rev 14. | SILVERPOWDER; +3 pts | Ledger cameo record (FESTIVAL_SHELLY); CAMEOS.md #1 | designed |
| **The Rehearsal** `EL_REHEARSAL` | 4 | `badges >= 2` | Sister Maelon · the Half-Tally, Frostwick (573) | ★★ · 20 | Off the Frostflat Causeway, a stretch of road replays five seconds of a wagon crash, over and over. Something out there is practising a tragedy. | SPELLTAG; +3 pts | Resonance (Harmony +1) | wired |
| **Gerald** `EL_GERALD` | 10 | `badges >= 8 && switch(126)` | the Queen's Keeper of Small Creatures · the Royal Chase (682) | ★★★ · 44 | Queen Maelis's named Scatterbugs have escaped into the Royal Chase. Each one has a personality file. Gerald's is four pages long. **Twist:** Six hide-and-seek finds, each solved by reading its file (Doris likes warm stones, Percival hates the colour blue...). Gerald hides inside the Queen's own crown on its stand in the hunting lodge. Reward: Gerald, a Fancy-pattern Scatterbug. | SHINYSTONE, Scatterbug "Gerald" Lv 40 (COMPOUNDEYES); +3 pts | Elowen Crown favour (flavour); Queen Maelis comedy (15_COMEDY 'The Royal We') | designed |
| **The Rootward Wake** `EL_ROOTWARD_WAKE` | 10 | `badges >= 8` | a Rootward laundress · the Rootward slums, Verdance (296) | ★★★ · 44 | In Verdance nothing rots, so nothing is ever properly buried. The Rootward wants one funeral done right. **Twist:** Fetch a candle that's allowed to burn out, a flower picked from outside Verdance (it wilts on the way: that's the point) and a song nobody's sung since the Bleed. A Phantump comes to the wake and sits with the mourners. If Rowan's arc has turned (S124), one mourner is a Hollow sympathiser and says so. | CLEANSETAG, TM20; +3 pts | Resonance; Rowan's theme ('everything that grows must be allowed to die') | designed |
| **What the Bride Tree Hears** `EL_EVER_BLOOM` | 10 | `badges >= 8 && switch(125)` | Juno · the Heartgarden, Verdance (294) | ★★★ · 46 | Juno wants to know whether her Aunt Elin can still hear her. The Quiet Way says the Root carries voices. Juno says she'd like proof. **Twist:** A Mindscape-light puzzle under the Heartgarden: the roots repeat whatever you place against them, late, like an echo. Juno places a seed packet. Nothing. She places her bouquet. The roots hum the counting rhyme. Juno laughs and cries at once. Reward: a white Floette grown from the Bride Tree's blossoms (Juno names it Ever-Bloom). | Floette "Ever-Bloom" Lv 44 (FLOWERVEIL), JUNO+2; +4 pts | Juno bond (+2); Elin / Homecoming foreshadowing | designed |
| **The Twilight Cloister** `EL_TWILIGHT_CLOISTER` | 18 | `badges >= 16` | the Abbess · the Twilight Cloister, Gloaming (440) | ★★★★★ · 78 | The last trial of the Quiet Way: walk the dusk-chapels from end to end without saying anything at all. **Twist:** Every chapel stages a scene that begs a response (a child asks the way, a Thornguard insults you, a ghost of someone you failed). Each choice list has a silent option, worded differently each time. Speaking costs nothing but resets you to the first chapel. Celestine watches from the eighth and finally speaks to you as herself. | MAGICALSEED x3; +5 pts | Resonance (Harmony +2); unlocks the Quiet Way's Evergreen rank | designed |

### The Tally — Isenmar

| Quest | Ch | Unlock | Giver · where (map) | Rank · Rec Lv | What happens | Reward | Touches | Status |
|---|---|---|---|---|---|---|---|---|
| **Two Hearths, One Pot** `IS_TWO_HEARTHS` | 4 | `badges >= 2` | Brenna and Sigvald · the Two Hearths inn, Frostwick (573) | ★ · 16 | The Two Hearths has two fireplaces, two cooks and one cooking contest that has lasted nineteen years. Both cooks want you to fetch their secret ingredient. | HONEY x3, LAVACOOKIE x2; one_pot: RARECANDY; +2 pts (+2 The Quiet Way) | Joint Trial (Elowen + Isenmar points); WORLD.md's Frostwick sidequest 'The Two Hearths' | wired |
| **The Oathbound Parcel** `IS_OATH_PARCEL` | 4 | `badges >= 2` | Ingrith · the Half-Tally, Frostwick (573) | ★ · 17 | Carry a sealed oath-parcel from Frostwick to the Net Loft in Ebbmouth. In Isenmar a carried oath is not opened. Not ever. | $500; +3 pts | Isenmar 'oath' flavour: opening it costs a Trial point and earns you a very rude verse | wired |
| **A Deed for the Skald** `IS_SKALDS_SAGA` | 4 | `badges >= 2` | Bersi Gullsong · the Ebbmouth Net Loft (160) | ★ · 19 | The Ebb Guild feast is tonight and Bersi has no new saga. He needs a deed. Any deed. He'll handle the exaggerating. | MYSTICWATER; bully: MARISOL+1; tall_tale: POTION; +2 pts | Marisol bond (+1 for flattening Gorm, who she can't touch because he's Guild) | wired |
| **The Egg Thief of Gullcry** `IS_EGG_THIEF` | 4 | `badges >= 3` | Old Asta · the egg-gatherers' hut on the Gullcry Cliffs (561) | ★★ · 24 | Something is taking eggs off the Gullcry ledges. Old Asta wants it stopped. Then she wants it stopped harder. | $1000; let_go: EXPCANDYM x2, RES+1; +3 pts | Resonance (Harmony +1 if you let the Bombirdier keep its route) | wired |
| **The White Stag** `IS_WHITE_STAG` | 11 | `badges >= 9` | the lodge-keeper · Snowbriar (710) | ★★ · 48 | A white stag has been seen in the royal hunting woods. Elowen law says it's the Crown's. The trappers say it's nobody's. **Twist:** Four-sighting chase in deep snow; it only appears at dawn. At the end: battle and catch (EVENT IS_WHITE_STAG), report it to the Crown's lodge (Elowen points), or let the trappers' children see it once and let it go (Harmony). | $4000; +3 pts | Elowen vs Isenmar clan rights (WORLD.md 'The White Stag'); Thane's standing flavour | designed |
| **The Harpoon Rite** `IS_HARPOON_RITE` | 11 | `badges >= 9` | Old Halla Brinesdottir · the Great Tally, Rimeholt (306) | ★★★ · 50 | Every Harpooner earns the rank by facing the Old Bull on the ice. The Old Bull is a Cetitan. It has never once been harpooned. **Twist:** Boss Cetitan (3 bars) on :FROZEN_LAKE; the field cracks to :WATER_SURFACE at bar 2. Nobody harpoons it: the rite is to stand your ground. Win and it slaps the ice twice and swims under you (no catch). The calf that follows it out joins you (EVENT IS_CETODDLE). | NEVERMELTICE; +4 pts | Before the Thaw only (expires on S128 CH11_THAW) | designed |
| **Eleven Years at One Hole** `IS_ELEVEN_YEARS` | 11 | `badges >= 9` | Old Torstein · the ice-fishing flats, Rimeholt (300) | ★ · 47 | Old Torstein has fished one ice-hole for eleven years waiting for a single bite. He has not noticed he is sitting on an Avalugg. **Twist:** You fish his hole; a Tatsugiri has been nibbling the bait for eleven years without ever taking the hook. When Torstein stands up to cheer, his 'seat' stands up too. 'How long has that been there?' 'About eleven years, sir.' Reward: the Tatsugiri. | Tatsugiri Lv 48 (COMMANDER); +2 pts | 15_COMEDY Isenmar bit | designed |
| **The Sinking Quarter** `IS_SINKING_QUARTER` | 11 | `switch(128)` | a net-mender of Net Row · the Sinking Quarter, Rimeholt (309) | ★★★ · 52 | After the Thaw, the lower town is going under. Three families won't leave without their boat, their grandmother and their Lapras, in that order. **Twist:** Timed escort over breaking ice (floes sink after N steps); at the gate the checkpoint officer is an ISENMAR_OFFICER battle or a bribe or Anja's word if her bond is good. | EXPCANDYL x2; +4 pts | Refugee arc (S168 ISENMAR_MARTIAL_LAW); Thane / Anja politics | designed |
| **Crystal Sleep** `IS_ALEXANDRA` | 11 | `badges >= 10 && switch(128)` | Old Halla Brinesdottir · the sunken lower town, Rimeholt (309) | ★★★ · 56 | Something sleeps in a block of ice in the sunken quarter: a woman, very much alive, very annoyed about it. **Twist:** Board pointer for the Alexandra cameo; her event completes the quest. | ICYROCK; +3 pts | CAMEOS.md #5 'Crystal Sleep' (FESTIVAL_ALEXANDRA) | designed |
| **The Saga of the Shattered Ice** `IS_SAGA_OF_THE_ICE` | 15 | `badges >= 13` | Bersi Gullsong · Skaldfast (921) | ★★★★★ · 70 | Bersi wants to sing the war. Truthfully, for once. He needs a witness who stood on the ice. **Twist:** Bersi sings the war straight, no exaggeration, and it's the first time the hall goes silent for him. His verses use the war choice keys, so the saga is different on every war outcome. | Lapras "Saga" Lv 45 (WATERABSORB); +5 pts | War choices (war_climax / war_terms): the saga's words follow what you chose | designed |

### The Prize Exchange — Zenith

| Quest | Ch | Unlock | Giver · where (map) | Rank · Rec Lv | What happens | Reward | Touches | Status |
|---|---|---|---|---|---|---|---|---|
| **Form 7-B** `ZE_FORM_7B` | 1 | `switch(103)` | Grant Kiosk P-3NNY · the Quarantine Customs Hall, Ferrow's Landing (108) | ★ · 5 | CALL FOR PROPOSALS #0001: DISPOSAL OF UNCLAIMED LIVESTOCK, CRATE 7-B. BOUNTY: $500. | disposed: $500, MERIDIAN+1; adopted: POTION x2; +2 pts | Meridian standing (+1 if you sign the disposal form) | wired |
| **Field Survey: Coastal** `ZE_FIELD_SURVEY` | 2 | `switch(103)` | Grant Kiosk P-3NNY · any P-3NNY kiosk (Ferrow's Landing, Saltmere, Ebbmouth) (108) | ★ · 10 | CALL FOR PROPOSALS #0002: RECORD BATTLES ON THREE (3) DIFFERENT FIELDS. DATA IS THE CURRENCY OF THE FUTURE. SO IS CURRENCY. | EXPCANDYS x3; +2 pts | Field Notes (fields_seen) | wired |
| **The Lattice Hums Wrong** `ZE_LATTICE_HUM` | 4 | `badges >= 2` | Grant Kiosk P-3NNY/2 · the tidal Lattice station, Ebbmouth (160) | ★ · 20 | CALL FOR PROPOSALS #0003: ACOUSTIC SURVEY OF THE EBBMOUTH TIDAL LATTICE DURING 'STUTTER EVENTS'. RECORDER PROVIDED. | $300; meridian: $1500, MERIDIAN+1; guild: MARISOL+1; larch: EXPCANDYS x2; +3 pts | Meridian standing or Marisol bond, depending on who gets the recordings (foreshadows Larch's tide data in Ch4) | wired |
| **Customer Support** `ZE_CUSTOMER_SUPPORT` | 5 | `badges >= 3` | Helpdesk Rotom · Meridian Spire lobby, Lumen City (185) | ★ · 24 | Walk a form through nine offices. The form is to cancel the form. **Twist:** Each office wants a different stamp first (circular dependency the player has to break by noticing office 4 has two doors). When the form is finally cancelled, it cancels itself out of existence. What's left on the desk is a Porygon, who was the form all along. | Porygon Lv 24 (DOWNLOAD); +3 pts | 15_COMEDY Zenith bit 'Customer Support' | designed |
| **The Machine Wants Compliments** `ZE_FIZZBOLT` | 5 | `badges >= 3` | a Fizzbolt vending machine · Lumen City Concourse (180) | ★ · 24 | A Lumen vending machine has gained sentience from the free current and only sells Fizzbolt to people who compliment it. **Twist:** Five compliments across five visits; each needs a fresh one (choice lists rotate). Repeat a compliment and it sulks for a day. On the fifth it dispenses everything at once and a Rotom flies out to thank you, then back in. | CELLBATTERY; +2 pts | none | designed |
| **Product Recall** `ZE_ROTOM_RECALL` | 5 | `badges >= 3` | the Lumen Arcade floor manager · Lumen Arcade Dept. Store (183) | ★★ · 26 | Five display appliances have walked off the shop floor. They were not supposed to be able to walk. **Twist:** A hide-and-seek in the department store; each appliance (fan, mower, fridge, washer, oven) dashes between counters when you look away. Reward: a voucher the Sluiceworks Rotom can use to change form at the Arcade. | EXPCANDYM x2; +3 pts | Teaches Rotom forms before the Sluiceworks Rotom | designed |
| **Ten Years of Light** `ZE_LOWLIGHT_LAMPS` | 6 | `switch(114)` | a Lowlight lamp-tender · the Lowlight (Shattered) (608) | ★★ · 28 | After the Shatter, someone has been lighting small lamps at the feet of the glassed people. Nobody admits to it. **Twist:** It's Dex's Pichu, who escaped the Shatter and has been carrying spark-lamps to every glassed figure, starting with his. If you sit by the shrine it comes to you. No battle; it chooses you. It knows Volt Tackle. | Pichu "Spark" Lv 25 (LIGHTNINGROD); +3 pts | Dex shrine (S164); Homecoming foreshadowing | designed |
| **Cut Loose** `ZE_COURIER` | 12 | `badges >= 10` | a pilot at the anchor-smithy · Anchorhold (730) | ★★★ · 52 | Deliver a sealed key-ring to an airship before the embargo inspectors board. The key-ring jingles by itself. **Twist:** The key-ring is a Klefki carrying the airship's ignition keys. Give it up and Meridian thanks you; hide it in your bag and the ship cuts loose, and the Klefki, having nobody left to hold keys for, holds yours. | Klefki Lv 50 (PRANKSTER); +4 pts | Meridian standing (handing it to the inspectors) vs the smugglers (WORLD 'Cut Loose') | designed |
| **The Laureate's Prize** `ZE_LAUREATE` | 16 | `badges >= 14` | Registrar Odalys Venn · the Prize Exchange, Lumen City (194) | ★★★★★ · 72 | The Exchange's highest prize: enter a machine of your own design in the Cogsworth Invention Bout. Your machine is your team. **Twist:** Rounds: Steel-only, no items, and Factory-to-Scrapyard mid-battle. The Registrar admits the prize was always rigged for Meridian entrants and that you won anyway. | ABILITYPATCH; +5 pts | Magnus / Meridian politics (MAGNUS_KEPT_FAITH flavour) | designed |

### The Gutter Book — Nadir

| Quest | Ch | Unlock | Giver · where (map) | Rank · Rec Lv | What happens | Reward | Touches | Status |
|---|---|---|---|---|---|---|---|---|
| **Clean Water** `NA_CLEAN_WATER` | 7 | `badges >= 5` | a char-burner · Charwell (630) | ★ · 32 | Ossarian bone-char filters clean Nadir's poison. Someone is skimming the filter carts. Find who, then decide who you tell. **Twist:** The skimmer is a sump-folk grandmother selling filters to families the cart route skips. Tell Meridian (MERIDIAN+1), tell the Hollow (HOLLOW+1), or reroute the carts yourself (a puzzle on the canal locks; Harmony). | $3000; +3 pts | Hollow vs Meridian standing (WORLD 'Clean Water') | designed |
| **A Five Out of Ten** `NA_NOODLE_SCORE` | 7 | `badges >= 5` | the noodle-cart cook · Mirefen (220) | ★ · 32 | Mirefen's noodle cart rates its customers out of ten. Nobody has scored above a four. Corvin has a two and comes daily. **Twist:** The score isn't about manners: it's about whether you notice the cook's Alolan Grimer cleaning the pots. Thank the Grimer and you get a five (the first ever). The cook, overcome, gives you one of its babies. Corvin demands a recount. | Alolan Grimer Lv 30 (POISONTOUCH); +2 pts | 15_COMEDY Nadir bit; Corvin (Ch7) | designed |
| **Sewer Royalty** `NA_VENAM` | 7 | `badges >= 6 && switch(118)` | Six-Fingers Ottoline · the Miasma Caverns under Mirefen (644) | ★★ · 38 | Somebody has crowned herself queen of the Miasma Caverns. Ottoline wants to know who's charging tolls on her sumps. **Twist:** Board pointer for the Venam cameo; her event completes the quest. | BLACKSLUDGE; +3 pts | CAMEOS.md #2 'Sewer Royalty' (FESTIVAL_VENAM) | designed |
| **Pit Ringer** `NA_PIT_RINGER` | 9 | `badges >= 7` | the Iron Pit announcer · the Iron Pit, Ironreach (263) | ★★ · 41 | An unlicensed pit in the old mine shafts: six fights, no breaks, and the house brings a brass formation for the last one. **Twist:** Gauntlet on :COLOSSEUM with crowd-mood effects; the last bout is a boss Falinks whose break summons the rest of the troop. Win and the troop's runt follows you out. | Falinks Lv 38 (DEFIANT); +4 pts | Kaito / Ironreach Open foreshadowing; the announcer narrates everything (15_COMEDY) | designed |
| **Lamplighter Kids** `NA_LAMPLIGHTER_KIDS` | 9 | `badges >= 7` | Pip's friend from the lamp-runners · Ironreach (260) | ★★ · 40 | Three lamp-runner children went into the old sumps after a rumour of treasure. Their lamps are running out. **Twist:** Darkness puzzle: each found child carries a lamp that lights a radius; you choose the route by which shafts their lamps can reach. The 'treasure' is a Sableye's gem hoard, which the Sableye would like back. | EXPCANDYM x3; +3 pts | none | designed |
| **Two Lucarios** `NA_GARRET` | 9 | `switch(123)` | Six-Fingers Ottoline · Ironreach's lower shafts (263) | ★★★ · 46 | A foreign trainer is asking every pit-fighter in Ironreach the same question about his Lucario. **Twist:** Board pointer for the Garret cameo; his event completes the quest. | BLACKBELT; +3 pts | CAMEOS.md #3 'Two Lucarios' (FESTIVAL_GARRET) | designed |
| **The Lift Strike** `NA_LIFT_STRIKE` | 16 | `badges >= 14` | the lift-workers' union · Midstair (830) | ★★★ · 70 | The cable-lift workers have stopped every lift between Zenith and Nadir. The Directorate wants them moving by morning. **Twist:** A vertical map of stalled lift cages; you climb between them. The Directorate officer is a MERIDIAN_DIRECTORATE battle if you side with the union. | $6000; +4 pts | Meridian vs Hollow standing; Mandate (S115) state | designed |
| **Mother Gutter's Ledger** `NA_GUTTER_DEBTS` | 17 | `badges >= 15` | Mother Gutter · the Moon Market, Underveil (423) | ★★★ · 72 | Collect five debts for the oldest sump-baron in Nadir. Or don't collect them. She'll know either way. **Twist:** Each debtor has a reason (a sick Pokemon, a Mandate fine, a lie). You can pay one debt yourself, forgive one, fight one. Mother Gutter rewards whatever you did, as long as you did it on purpose. Her Muk is the size of a cart and attends the meeting. | $8000; +4 pts | Nadir independence arc (S149); Nyx bond flavour | designed |
| **Sweetrot** `NA_SWEETROT` | 18 | `switch(150)` | a Sweetrot vendor · the Moon Market, Underveil (423) | ★★★★ · 76 | The Sweetrot vendors woke from Pecharunt's spell craving tea. Terrible tea. One cup in particular. **Twist:** The only tea bitter enough is Larch's kelp tea. Bring a cup (mailed from Tidewatch at your request, with a furious note). A Poltchageist climbs into the cup and refuses to leave. | Poltchageist Lv 72 (HOSPITALITY); +4 pts | Running gag 1 (Larch's kelp tea) | designed |

### The Trial by Flames — Ashkaar

| Quest | Ch | Unlock | Giver · where (map) | Rank · Rec Lv | What happens | Reward | Touches | Status |
|---|---|---|---|---|---|---|---|---|
| **The Little Crucible** `AS_LITTLE_CRUCIBLE` | 2 | `badges >= 1` | Sergeant Brakka Emberhide · the Legion recruiting barge, Saltmere harbour (146) | ★ · 17 | WRIT OF FLAME: three bouts, back to back, no healing. Then the barge's mascot. Win and the Legion respects you. Lose and the Legion respects you less. | $1200, QUICKCLAW; +3 pts | Ashkaar flavour: honesty is law; signing up (flag :recruited) changes how later Legion NPCs greet you | wired |
| **Seven Bouts** `AS_SEVEN_BOUTS` | 8 | `badges >= 6` | Legate Varra Kosk · the Crucible, Cindervault (240) | ★ · 38 | The Crucible's entry rite: seven legion fighters, back to back, on the caldera floor. No items. No healing. No complaining. **Twist:** Volcanic field; each bout raises the field's heat stage. Bout 4 is a double. Bout 7 is the Legate's adjutant on a Dragon's Den preview. The Herald introduces you with whatever the Saltmere barge called you. | CHARCOAL, FIRESTONE; +4 pts | Ashkaar recruitment flag from the Saltmere barge is honoured here (skip bout 1) | designed |
| **The Lava-Tube Terror** `AS_DRUDDIGON` | 8 | `badges >= 6` | a Hearthguild smith · Mt. Cinder (664) | ★★ · 40 | A Druddigon has made the Mt. Cinder lava tubes its own. Three smiths' Pokemon came back scorched. The Legion wants it beaten, not killed. **Twist:** Boss Druddigon (Rough Skin, 2 bars) on :VOLCANIC; it joins after. Back at the Crucible the Herald asks how it went. Exaggerate (Isenmar-style) and you're fined for lying. | Druddigon Lv 37 (ROUGHSKIN); +4 pts | Honesty law: report how the fight really went (lying costs the reward) | designed |
| **Adequate Swords** `AS_ADEQUATE_SWORDS` | 8 | `badges >= 6` | the owner of ADEQUATE SWORDS · Cindervault market (240) | ★ · 38 | A rival shop has opened across the street: EXCELLENT SWORDS. The owner of ADEQUATE SWORDS suspects a lie. Lying is a crime. **Twist:** You test the swords (a battle against the rival smith's Honedge on a 'sharpness' rule). The swords are excellent. ADEQUATE SWORDS loses the case, renames itself ADEQUATE SWORDS (STILL), and is happier. | METALCOAT; +2 pts | 15_COMEDY Ashkaar honest-signs bit | designed |
| **Afraid of Heights** `AS_AFRAID_OF_HEIGHTS` | 8 | `badges >= 6` | Recruit Tamm · the Dragon Roosts, Cindervault (248) | ★★ · 40 | A dragon-rider recruit is afraid of heights and has been assigned a Trapinch 'until he's ready'. He has been not-ready for two years. **Twist:** Three training battles with Tamm's Trapinch in your party as a guest. When it becomes a Vibrava it takes Tamm three feet off the ground and he screams with joy. He gives you the Noibat he was also assigned, because 'it looks at me like it knows'. | Noibat Lv 36 (INFILTRATOR); +3 pts | 15_COMEDY Ashkaar bit | designed |
| **Ashes Home** `AS_ASHES` | 8 | `badges >= 6` | the Legion quartermaster · Scaldwater (650) | ★★ · 37 | A Nadir-born legionnaire died at the caldera. His Houndour won't leave his urn. Somebody has to carry both of them home to Scaldwater. **Twist:** No battles unless you take the short road (Legion deserters who want the urn's silver). At the door the mother takes the urn and tells the Houndour to go and keep marching, with someone who will come back. | Houndour Lv 34 (FLASHFIRE); +4 pts | War arc: Ashkaar recruiting Nadir youths (WORLD border E); Harmony | designed |
| **The Trial of Truth** `AS_TRIAL_OF_TRUTH` | 8 | `badges >= 6 && switch(120)` | Herald Pyke · the Hall of Oaths, Cindervault (247) | ★★★ · 41 | Ashkaar judges a lie by combat. A Hearthguild officer swears the caldera crisis wasn't the Legion's fault. You were there. **Twist:** Whatever you say is a choice with consequences; contradicting the officer starts an ASHKAAR_OFFICER duel on :VOLCANIC under 'oath rules' (if you switch, you concede). Win and the Legion admits fault publicly, which nobody in the hall has seen before. | FLAMEORB; +4 pts | Caldera result (V110) and Brann's bond flavour; Ashkaar war politics (S121) | designed |
| **The Egg Run** `AS_EGG_RUN` | 9 | `badges >= 7` | the Roost-mistress · the Dragon Roosts, Cindervault (248) | ★★★ · 42 | Carry a warm dragon egg across Mt. Cinder to the far roost. Egg-hunters know the route. The egg must not get cold. **Twist:** A warmth meter (steps since the last vent) instead of a timer; egg-hunter ambushes (trainer battles) at the vents. At the far roost the egg hatches early in your hands. It decides you're its roost. | Axew Lv 1; +4 pts | none; earliest Axew (wild only from Badge 17) | designed |
| **Dragonsworn** `AS_DRAGONSWORN` | 19 | `badges >= 17` | Legate Varra Kosk · the Wyrmrest proving ground (460) | ★★★★★ · 83 | The highest brand in Ashkaar. Stand in the Dragon's Den and fight the Legate's own dragon while the legions watch. **Twist:** ASHKAAR_OFFICER Legate team ending in a boss Haxorus. Afterwards you're offered the Dragonsworn oath (to the Dominar). Refusing is also honoured: 'Strength that won't kneel. Good.' | LIFEORB; +5 pts | DOMINAR_SWAYED flavour; Sigrun bond (she watches) | designed |

### The Rolls of Unearthing — Ossaria

| Quest | Ch | Unlock | Giver · where (map) | Rank · Rec Lv | What happens | Reward | Touches | Status |
|---|---|---|---|---|---|---|---|---|
| **Kevin** `OS_KEVIN` | 6 | `badges >= 4` | the Dig Lab interns · the Dig Lab, Duneholt (209) | ★ · 29 | The interns revived a fossil they can't identify. They call it Kevin. Kevin is a rock. Kevin is in the staff photo. **Twist:** Three tests (light, sound, being talked to kindly) over three visits. On the third Kevin turns out to be a Carbink that was asleep, and it has been listening to the interns' gossip for a month. It knows everything. | Carbink "Kevin" Lv 28 (STURDY); +2 pts | 15_COMEDY Ossaria bit | designed |
| **The Riddle Trader** `OS_RIDDLE_CARAVAN` | 6 | `badges >= 4` | a caravan trader · Copperdune caravanserai (610) | ★ · 27 | A caravan trader only barters in riddles. She doesn't know the answers either. She wants you to find them. **Twist:** The riddles have real answers hidden in Copperdune (a buried locomotive, a mural, a Sandile who only comes out at noon). When you give her the third answer she says 'Oh! I always thought it was a goat,' and pays you in a Trapinch. | Trapinch Lv 27 (SHEERFORCE); +2 pts | 15_COMEDY Ossaria bit | designed |
| **Tomb Freight** `OS_TOMB_FREIGHT` | 6 | `badges >= 4` | the freight-depot foreman · Copperdune (610) | ★★ · 30 | A locked railway car bound for Lumen is heavier than its manifest. Meridian says machine parts. The tomb-guild says grave goods. **Twist:** Stealth into the depot at night; the car holds an Elector's sarcophagus with an Unown inscription that names the Prismfall. | $3500; +3 pts | Meridian vs Ossarian Electors (WORLD 'Tomb Freight'); Prince-Elector Kassan | designed |
| **The Mural Gallery's Missing Letter** `OS_UNOWN_MURALS` | 6 | `switch(116)` | Curator-Elect Nasrin Vael · the Mural Gallery, Duneholt (207) | ★★ · 30 | One Unown is missing from the gallery's great inscription, and the sentence is wrong without it. **Twist:** Catch the Unown form the sentence needs (the inscription tells you which by grammar). The corrected sentence reads differently from the one Sahar teaches: 'nineteen fell'. | TM28; +3 pts | Lore (Prismfall, Legend Plate seed) | designed |
| **Something in the Sinkholes** `OS_SINKFIELD` | 7 | `badges >= 5` | a Sinkwells water-carrier · Sinkfield (628) | ★★ · 31 | Something flat and grinning is dragging water-carriers' Pokemon into the Sinkfield sinkholes. **Twist:** Boss Galarian Stunfisk (trap-jaw) on :DESERT/:BLEED that hides in random sinkholes between turns of a little overworld puzzle; beaten, it gives back the carriers' Pokemon and joins. | Galarian Stunfisk Lv 31 (MIMICRY); +4 pts | Bleed zone; Imprinted variant | designed |
| **The Unquiet Elector** `OS_UNQUIET_ELECTOR` | 14 | `badges >= 12` | an embalmer of Vigil · Vigil (770) | ★★★ · 62 | A dead Elector keeps walking out of his tomb-mirror to vote. The Veiled Synod says the dead are theirs. Vigil says the dead are Vigil's. **Twist:** A mirror-mystery across the Obsidian Barrows; the Elector never got to cast the vote that would have stopped the Prince-Elector's grandfather. You stage it. He votes, and rests. His Galarian Yamask stays with you. | Galarian Yamask Lv 60 (WANDERINGSPIRIT); +4 pts | Tomb-law vs the Synod (WORLD 'The Unquiet Elector'); Antumbra joint points | designed |
| **Where the Well Went** `OS_UNDERSANDS` | 14 | `badges >= 12 && switch(137)` | Sahar's foreman · the Duneholt Undersands (783) | ★★★★ · 62 | Duneholt's well is dry. The diggers think the water went down. They want someone to follow it. **Twist:** Strength-boulder escort through collapsing galleries; the crew can fall behind. At the bottom: warm stone breathing like something asleep. | TELLURICSEED x2, EXPCANDYL x2; +4 pts | Groudon arc prelude (S140); V109 DUNEHOLT_WELL | designed |
| **The Bonewright's Rite** `OS_BONEWRIGHT` | 14 | `badges >= 13` | Curator-Elect Nasrin Vael · Cragholm (360) | ★★★★★ · 64 | Reassemble a whole fossil skeleton from the pieces the Rolls have collected across Ossaria, in the right order, in front of the Curators. **Twist:** A drag-and-place puzzle; wrong orders produce a creature that the Curators politely call 'Kevin II'. | ABILITYCAPSULE; +5 pts | Cragholm fossil revival (POKEMON_AVAILABILITY §2) | designed |

### The Rite of Reflection — Antumbra

| Quest | Ch | Unlock | Giver · where (map) | Rank · Rec Lv | What happens | Reward | Touches | Status |
|---|---|---|---|---|---|---|---|---|
| **Your Other Half** `AN_OTHER_HALF` | 13 | `badges >= 11` | a Glassmere fisherwoman · Glassmere (753) | ★ · 56 | Her husband came back from the Mere reversed: left-handed, kinder, and worse at fishing. She'd like the old one back. Probably. **Twist:** Swap through the Mere twice; the reflection doesn't want to go back. The fisherwoman chooses (you can influence it). The couple's Indeedee also came back reversed, and stays with you. | Indeedee Lv 55 (PSYCHICSURGE); +3 pts | WORLD 'Your Other Half'; mirror gag (running gag 8) | designed |
| **It Keeps the Rain In** `AN_UMBRELLA` | 13 | `badges >= 11` | a man with an umbrella · the Antumbra Threshold (743) | ★ · 55 | His umbrella keeps the rain in. He'd like it to keep the rain out. He's tried holding it the other way up. That keeps the rain up. **Twist:** The answer is to open it indoors (which is outdoors here). The tiny storm inside it was a Hatenna that hates noise and was hiding from the Threshold's echoes; it comes with you. | Hatenna Lv 54 (MAGICBOUNCE); +2 pts | 15_COMEDY Antumbra bit | designed |
| **Better Marks** `AN_STUDENT` | 13 | `badges >= 11` | a Lucent student · the Athenaeum, Lucent (344) | ★★ · 58 | Her reflection has been attending lectures for her. It gets better marks. She is furious and wants to sit the final herself. **Twist:** Battle the REFLECTION trainer type (her team, mirrored). She passes with a lower mark than her reflection got, and is prouder of it. | TWISTEDSPOON; +3 pts | 15_COMEDY Antumbra bit | designed |
| **The Echo That Answers First** `AN_ECHO_HALL` | 13 | `badges >= 12` | Lector Saffi Ivarne · the Speculum, Lucent (346) | ★★★ · 60 | An echo in the Speculum answers questions before they're asked. The Lectors would like to ask it one. **Twist:** A reverse-dialogue puzzle: answers come first and you assemble the question from them. | TM48; +4 pts | Mindscape lore; Ilsa (Ch13) foreshadowing | designed |
| **Shadows Fall Upward** `AN_SHADOWS_UP` | 13 | `badges >= 12` | a Vigil medium · the Obsidian Barrows (760) | ★★★ · 60 | In the Barrows, shadows fall upward. Somebody's shadow has fallen all the way up and got stuck on the inverted desert in the sky. **Twist:** Light-source puzzle on the Inverse field: move lamps so the stuck shadow is cast back down onto the sand. | ELEMENTALSEED x2; +4 pts | Antumbra / Ossaria borderland I | designed |
| **Nine Hundred and Ninety-Nine** `AN_GIMMIGHOUL_COINS` | 15 | `badges >= 13` | a lantern-priest · Gravenmoor (380) | ★★ · 64 | Gimmighoul coins keep turning up in the Gravenmoor collection plates. The priests want to know where they're coming from. **Twist:** Wraps the existing Gimmighoul coins hunt in a Trial quest; the chest is a Gimmighoul who has been tithing. | RELICGOLD; +3 pts | POKEMON_AVAILABILITY §3 Gimmighoul hunt | designed |
| **Behind the Glass** `AN_BEHIND_THE_GLASS` | 15 | `badges >= 14 && switch(143)` | Archseer Dask's reflection · the Palace of Glass, Lucent (347) | ★★★★★ · 70 | Antumbra's last rite: spend one night as your own reflection. **Twist:** A short playable stretch as the PC's reflection, which sees everything the PC did and has opinions. No joke after this one is safe in a mirror. | ABILITYPATCH; +5 pts | Mirror gag payoff (running gag 8); Ruin Route seed | designed |
| **Dreamwalker** `AN_SHIV` | 18 | `badges >= 17` | Lector Saffi Ivarne · the dusk-chapels of Gloaming (440) | ★★★★ · 82 | A stranger has been walking through other people's dreams in Gloaming and leaving them better rested. The Lectors want a word. **Twist:** Board pointer for the Shiv cameo; her event completes the quest. | MAGICALSEED; +3 pts | CAMEOS.md #7 'Dreamwalker' (FESTIVAL_SHIV) | designed |

### The Hall of Petitions — Crownhaven

| Quest | Ch | Unlock | Giver · where (map) | Rank · Rec Lv | What happens | Reward | Touches | Status |
|---|---|---|---|---|---|---|---|---|
| **Eighteen Shrines** `CR_EIGHTEEN_SHRINES` | 20 | `badges >= 18` | the Pilgrim's Rest keeper · Pilgrim's Rest (890) | ★ · 85 | Eighteen roadside shrines on the Pilgrim Pass, one per Plate. Ashkaar charges a toll at six of them. **Twist:** Each shrine asks one line of the counting rhyme; the eighteenth asks for the line nobody sings ('...and one that no one counted'). The keeper's prism-coated Eevee follows you down the Pass. | Eevee "Prism" Lv 50 (ADAPTABILITY); +4 pts | Ashkaar tolls (pay, fight or talk); WORLD 'Eighteen Shrines' | designed |
| **Lost Property** `CR_LOST_PROPERTY` | 20 | `switch(155)` | the lost-property clerk · the Court of Eight Pavilions (499) | ★ · 88 | The Festival lost-property tent has one item. Every day. It's an eel receipt. **Twist:** It's Kestrel's, from Ebbmouth, from Chapter 4. He has been carrying it for sixteen chapters. He denies it until you show him the date. Then he takes it back very carefully. | RARECANDY x2; +2 pts | Kestrel bond (+1); 15_COMEDY Crownhaven bit; Ebbmouth's 'THE BOY (4 EELS, DAILY)' | designed |
| **The Pavilion Line** `CR_DELEGATION_DISPUTE` | 20 | `switch(155)` | Clerk-Superior Amadeus Fenwright · the Court of Eight Pavilions (499) | ★★ · 88 | Ashkaar's pavilion is four inches over the line into Isenmar's. Neither delegation will speak to the other. Both will speak to you. **Twist:** Every message gets ruder in translation. The fix is to move the line, not the pavilion; Fenwright is appalled and then promoted. | PPMAX; +3 pts | War outcome flavour (war_terms); Dominar / Thane | designed |
| **Invitations to the Masque** `CR_MASQUE_INVITES` | 20 | `switch(156)` | the Basilica steward · the Basilica Close (483) | ★★ · 88 | Deliver eight invitations to the Night of Masques. One recipient doesn't exist. One is dead. One is you. **Twist:** A social route through the capital meeting every delegation; the dead recipient is Morwen Vane, and Kestrel sees you holding it. | RARECANDY x2; +3 pts | Night of Masques (S157) staging | designed |
| **The Chancellor's Other Ledger** `CR_HOLLIS_LEDGER` | 20 | `switch(155)` | an anonymous petition · the Accord Palace (486) | ★★★ · 90 | An unsigned petition, sealed with all eighteen kingdom seals: Chancellor Hollis keeps a second ledger. **Twist:** Palace stealth during a reception; the petition was written by Clerk Fenwright, who has been waiting thirty years for someone to answer it. | $12000; +4 pts | Hollis's arrest in the epilogue; ACCORD / MERIDIAN standing | designed |
| **An Old Man's Errand** `CR_VALENS_ERRAND` | 20 | `switch(158)` | Valen Corrigan · the Memorial Garden (489) | ★★★ · 90 | Valen asks you, not as Sovereign, to fetch something from the Memorial Garden that he can't bend down to pick up any more. **Twist:** The stone is the AF 290 marker; the name on it is the PC's mother's. He doesn't explain. He says thank you twice. | PPMAX, VALEN+2; +4 pts | Valen bond (+2) before the Final | designed |
| **Hand of the Accord** `CR_ACCORD_CHAMPIONS` | 21 | `switch(160)` | Clerk-Superior Amadeus Fenwright · the Hall of Petitions (496) | ★★★★★ · 95 | Answer one petition from every kingdom in a single day. Each is a battle. Each Warden who still speaks to you sends one. **Twist:** Requires rank 4+ in at least five Trials. The gauntlet's order is the eight Trials' halls; between bouts, each Trial's keeper says one line about what you did in their kingdom. | MASTERBALL; +5 pts | Postgame Warden's Gauntlet (S160); every Trial's rank 5 counts | designed |
| **The Meteor Champion** `CR_LIN` | 22 | `switch(160)` | a petition in a hand nobody recognises · Ferrow Lighthouse (105) | ★★★★ · 100 | A petition arrives from nowhere: 'Come back to where you landed.' **Twist:** Board pointer for the Lin postgame cameo; her event completes the quest. | ABILITYPATCH; +5 pts | CAMEOS.md #8 (FESTIVAL_LIN superboss) | designed |

## Part 2. Full scripts of the wired quests (Chapters 1–4)

Conventions: *italics* = narration box; **Name** _(expression)_ = a line under a portrait bubble (`pf_say`);
[stage] = what the map event shows (the map builder stages it); [if ...] = a `Prismfall::Conditions` check; `> option` = a choice.

### The Quiet Way

#### The First Lesson (`EL_FIRST_LESSON`)

*Chapter 1 · Brother Teasel, the wayshrine by the Accord plaque (map 100) · rank 1 · 2 points · unlock `switch(103)`*

Do one kind thing in Ferrow's Landing that nobody asked you to do. Then go back to Brother Teasel.

**Quest log steps:** `listen`: Do one kind thing nobody asks of you. Don't tell Brother Teasel what it was. · `return`: You did something. Go back to the wayshrine.

**Reward:** ORANBERRY x2; silent: RES+1; +2 pts. **Touches:** Resonance (Harmony +1 for keeping quiet); starts the realm-wide Quiet Deeds tally.

**Scene `offer`** (event: `pf_quest_run(:EL_FIRST_LESSON, :offer)`)

- [stage] A young monk in grey stands by the wayshrine, a rope of paper lanterns strung over his head. His lips move.
- *Brother Teasel is saying something. You can't hear a word of it.*
- **Brother Teasel** _(neutral)_: ...I SAID, WELCOME TO THE QUIET WAY.
- **Brother Teasel** _(shocked)_: Oh no. Oh, I'm so sorry. That's the loudest I've been in four years.
- **Brother Teasel** _(neutral)_: I keep the wayshrine. Folk hang their troubles on the rope, and somebody takes one down and makes it lighter.
- **Brother Teasel** _(neutral)_: But the first lesson isn't on the rope. The first lesson is: do one kind thing nobody asked you to do.
- **Brother Teasel** _(happy)_: Then come back. Don't tell me what it was. The Root will have heard.
- **CHOICE:** **Brother Teasel**: Will you take the first lesson?
  - > I'll try.
    - [quest accepted]
    - **Brother Teasel** _(happy)_: Go gently. Most people need three goes.
    - [if `deeds >= 1`]
      - **Brother Teasel** _(shocked)_: ...Oh. You already have, haven't you. I can tell.
      - [quest step: return]
  - > Not now.
    - **Brother Teasel** _(neutral)_: The rope will still be here. So will I. Quietly.

**Scene `return`** (event: `pf_quest_run(:EL_FIRST_LESSON, :return)`)

- [if `deeds >= 1`]
  - **Brother Teasel** _(happy)_: Oh. You did something. You've got the look. Like you just put a stone down.
  - **CHOICE:** Tell him what you did?
    - > Tell him everything.
      - *You tell him. All of it. With gestures.*
      - **Brother Teasel** _(neutral)_: Mm. Mm-hm. And then you hung it all back up. Mm.
      - **Brother Teasel** _(deadpan)_: That's called boasting. Half a lantern.
      - [-1 The Quiet Way points]
      - [quest complete: boasted]
    - > Say nothing.
      - *You say nothing. Teasel nods as if you'd said a great deal.*
      - **Brother Teasel** _(happy)_: Good. That's the whole lesson. You only needed one go.
      - [quest complete: silent]
  - **Brother Teasel** _(neutral)_: The Quiet Way keeps counting, wherever you go. Mother Aldreth in Briarwick keeps the tally. She'll know.
  - **Brother Teasel** _(neutral)_: And the rope's yours now. Anything hanging there, you may take down.
- [else]
  - **Brother Teasel** _(neutral)_: Not yet. You'll know when. So will I, somehow. It's a bit unsettling.

**Scene `deed_washing`** (event: `pf_quest_run(:EL_FIRST_LESSON, :deed_washing)`)

- *A shirt has blown off the washing line and wrapped itself round a kelp rack.*
- **CHOICE:** Hang it back up?
  - > Hang it up.
    - *You peg the shirt back on the line. Nobody sees.*
    - [quiet deed recorded: fl_washing]
    - [if `quest_step(:SELF) == :listen`]
      - [quest step: return]
  - > Leave it.

**Scene `deed_rope`** (event: `pf_quest_run(:EL_FIRST_LESSON, :deed_rope)`)

- **Rope-skipping girl** _(sad)_: We need a third to turn the rope. We can't finish the rhyme with two.
- [stage] The rope-skipping girls hold out the loose end.
- **CHOICE:** Turn the rope?
  - > Turn it.
    - *You turn the rope. The girls skip all the way through the counting rhyme, to the very last Plate.*
    - *"...and one that no one counted!" They collapse, laughing.*
    - [quiet deed recorded: fl_rope]
    - [if `quest_step(:SELF) == :listen`]
      - [quest step: return]
  - > Not now.

**Scene `deed_sailor`** (event: `pf_quest_run(:EL_FIRST_LESSON, :deed_sailor)`)

- *The old sailor sits facing the empty berth where the ferries used to come in.*
- **CHOICE:** Sit with him?
  - > Sit.
    - *You sit. He doesn't say anything. After a while he pats your knee twice and gets up.*
    - [quiet deed recorded: fl_sailor]
    - [if `quest_step(:SELF) == :listen`]
      - [quest step: return]
  - > Walk on.

**Scene `deed_kelp`** (event: `pf_quest_run(:EL_FIRST_LESSON, :deed_kelp)`)

- *A basket of drying kelp has tipped into a puddle. The kelp-drier is at the far end of the racks, not looking.*
- **CHOICE:** Rinse and re-hang it?
  - > Do it.
    - *It takes a while. Your hands smell of the sea for an hour.*
    - [quiet deed recorded: fl_kelp]
    - [if `quest_step(:SELF) == :listen`]
      - [quest step: return]
  - > Leave it.

#### The Tart Thief (`EL_TART_THIEF`)

*Chapter 1 · Wenna Hale, the tart stall on the quay (map 100) · rank 1 · 2 points · unlock `switch(103)`*

Someone keeps stealing Wenna Hale's bramble tarts. Brother Teasel's note on the lantern: "The thief is hungry, not wicked."

**Quest log steps:** `ask`: Wenna's tarts keep vanishing. Watch the stall. · `chase`: A Nickit with jam on its whiskers! Follow it round Ferrow's Landing. · `loft`: The crumbs lead up into Tidewatch Station's loft. · `return`: Tell Wenna what happened to her tarts.

**Reward:** $200, ORANBERRY x3; told: KESTREL-1; +2 pts. **Touches:** Kestrel bond (+1 if you split the evidence, -1 if you tell on him).

**Scene `offer`** (event: `pf_quest_run(:EL_TART_THIEF, :offer)`)

- **Wenna** _(worried)_: Twelve tarts this morning. Nine by the time I'd turned round. Six by the time I'd turned back.
- **Wenna** _(angry)_: It's not the gulls. Gulls don't take the paper cases with them.
- **Wenna** _(neutral)_: Watch the stall for me? I'll pay you in tarts. Well. In whatever tarts survive.
- **CHOICE:** Watch the stall?
  - > Of course.
    - [quest accepted]
    - **Wenna** _(happy)_: You're a treasure. Stand by the barrels, look casual. Not that casual.
  - > Maybe later.
    - **Wenna** _(neutral)_: I'll be here. Getting robbed.

**Scene `sighting`** (event: `pf_quest_run(:EL_TART_THIEF, :sighting)`)

- [if `chase(:SELF) == 0`]
  - *Something small and russet slips out from under the stall with a tart in its jaws.*
  - *It's a Nickit! It sees you, freezes, and bolts for the kelp racks.*
  - [chase advance]
  - [quest step: chase]
  - [end scene]
- [if `chase(:SELF) == 1`]
  - [stage] Kelp racks. The kelp-drier yelps as a russet streak tears through the hanging kelp.
  - *The Nickit leaves a trail of pastry flakes and vanishes under the pier.*
  - [chase advance]
  - [end scene]
- [if `chase(:SELF) == 2`]
  - *Under the pier: crumbs, a paper case, and two bright eyes. The Nickit squeezes out the far side.*
  - *It scampers up the lighthouse steps.*
  - [chase advance]
  - [end scene]
- [if `chase(:SELF) == 3`]
  - **Hesper** _(angry)_: THAT ANIMAL IS EATING MY GERANIUMS.
  - *The Nickit leaps the lighthouse wall and makes for Tidewatch Station, tail high.*
  - [chase advance]
  - [quest step: loft]

**Scene `loft`** (event: `pf_quest_run(:EL_TART_THIEF, :loft)`)

- [if `quest_flag(:SELF, :talked)`]
  - *The Nickit peers down from the rafters. Kestrel pretends to be asleep.*
  - [continue: nickit]
  - [end scene]
- [stage] The Nickit dives into the hay. Kestrel sits up in his bedroll with a bramble tart in each hand.
- **Kestrel** _(angry)_: What.
- **Kestrel** _(annoyed)_: ...It brings them. I don't ask it to. It just turns up with pastry like I'm some kind of— don't look at me like that.
- **Kestrel** _(annoyed)_: They're Wenna's? Of course they're Wenna's. Nobody else in this dump can bake.
- **CHOICE:** Kestrel has been eating stolen tarts.
  - > You could have just asked her.
    - **Kestrel** _(angry)_: Asked. Asked Wenna Hale for charity. While her daughter watches. No.
  - > Split the evidence?
    - *You hold out a hand. Kestrel stares at it, then puts a tart in it.*
    - **Kestrel** _(deadpan)_: ...Fine. You're an accessory now.
    - [effects: KESTREL+1]
  - > I'm telling Wenna.
    - **Kestrel** _(angry)_: Go on, then. Tell her the Vane boy's a thief. She'll love that. Everyone does.
- *The Nickit plants itself in front of its hoard and growls at you, every hair on end.*
- **Kestrel** _(smug)_: It thinks you're after the stash. Fight it if you want it. It likes winners.
- **Kestrel** _(deadpan)_: Clearly it has awful taste. It picked me.
- [continue: nickit]

**Scene `nickit`** (event: `pf_quest_run(:EL_TART_THIEF, :nickit)`)

- [battle] Nickit Lv 7 (STAKEOUT)
  - on caught:
    - **Kestrel** _(neutral)_: Huh. It went with you.
    - **Kestrel** _(annoyed)_: Feed it. It gets mean when it's hungry. So do I. Unrelated.
    - [quest step: return]
  - on won:
    - *The Nickit scrambles up into the rafters to sulk. It'll come down when it's hungry.*
    - **Kestrel** _(deadpan)_: You knocked out the pastry thief. Real heroic.
  - on lost:
    - **Kestrel** _(smug)_: You lost to a pastry thief.
    - **Kestrel** _(deadpan)_: ...Don't tell anyone. They'd think less of both of us.

**Scene `return`** (event: `pf_quest_run(:EL_TART_THIEF, :return)`)

- **Wenna** _(neutral)_: Well? Who's my thief?
- [if `quest_flag(:SELF, :told)`]
  - *You tell her about the Nickit, and the loft, and Kestrel.*
  - **Wenna** _(sad)_: Kestrel. Oh, that boy.
  - **Wenna** _(neutral)_: He's been sleeping in that loft since he was twelve. And I've been baking two dozen too many since about then.
  - **Wenna** _(neutral)_: I thought it was the gulls getting the extras. Turns out it was the right mouth all along.
  - [quest complete: told]
- [else]
  - *You tell her about the Nickit. Just the Nickit.*
  - **Wenna** _(deadpan)_: Mm. And this Nickit's about Kestrel's height, is it? Scowls a lot?
  - **Wenna** _(happy)_: Don't fret, love. I've known for years. I bake two dozen too many on purpose.
  - [quest complete: kept]
- **Wenna** _(neutral)_: I'll leave a plate by the station door from now on. Nobody has to ask anybody for anything.

#### The Scarecrow Walks (`EL_SCARECROW`)

*Chapter 1 · Coll Hale, the Hale farmhouse (map 523) · rank 1 · 2 points · unlock `switch(103)`*

Coll Hale's scarecrow keeps moving to a different field. Coll did not build a scarecrow.

**Quest log steps:** `ask`: Look at the 'scarecrow' in the Hale orchard on Windfall Row. Don't let it see you looking. · `bottle`: It hates the rain. Ask Wenna in Ferrow's Landing for her Squirt Bottle. · `water`: Water the scarecrow.

**Reward:** caught: $300; spared: MIRACLESEED, RES+1; +2 pts. **Touches:** Resonance (Harmony +1 if you leave it be).

**Scene `offer`** (event: `pf_quest_run(:EL_SCARECROW, :offer)`)

- **Coll** _(deadpan)_: Scarecrow's moved again.
- **Coll** _(neutral)_: Monday it was in the plum rows. Tuesday, the pears. This morning it was in my chair.
- **Coll** _(deadpan)_: I didn't build a scarecrow.
- **CHOICE:** Look into it?
  - > I'll look.
    - [quest accepted]
    - **Coll** _(neutral)_: Have a look at it. Don't let it see you looking.
  - > Not now.
    - **Coll** _(deadpan)_: Fine. It'll be in the kitchen by supper, I expect.

**Scene `watch`** (event: `pf_quest_run(:EL_SCARECROW, :watch)`)

- *It's a scarecrow. Probably. It has a lot of very green hands.*
- *A drop of rain lands on it. The scarecrow shudders, and edges sideways under the nearest tree.*
- *Scarecrows don't do that. Wenna keeps a Squirt Bottle for her window boxes...*
- [quest step: bottle]

**Scene `bottle`** (event: `pf_quest_run(:EL_SCARECROW, :bottle)`)

- [if `has_item(:SQUIRTBOTTLE)`]
  - **Wenna** _(happy)_: You've got it already! Go on, give it a good soak.
  - [end scene]
- **Wenna** _(shocked)_: Coll's scarecrow? We haven't got a scarecrow.
- **Wenna** _(neutral)_: Take the bottle. If it's a Pokémon, it'll thank you. If it's a scarecrow, nobody's lost anything but water.
- [receive SQUIRTBOTTLE x1]
- [quest step: water]

**Scene `water`** (event: `pf_quest_run(:EL_SCARECROW, :water)`)

- *The scarecrow stands very, very still. It is trying extremely hard to be a tree.*
- **CHOICE:** Water the scarecrow?
  - > Give it a squirt.
    - *You give it a squirt.*
    - *The 'scarecrow' screams, rips its roots out of the ground and charges!*
    - [battle] Sudowoodo Lv 10 (ROCKHEAD)
      - on caught:
        - **Coll** _(deadpan)_: ...It was a Sudowoodo.
        - **Coll** _(neutral)_: Best scarecrow I ever had. Look after it.
        - [quest complete: caught]
      - on won:
        - *The Sudowoodo bolts into the plum rows, sobbing dry tears. It'll be back. It always comes back to the plums.*
      - on lost:
        - *The Sudowoodo stops attacking and goes back to being a tree, looking smug.*
  - > Leave it be.
    - *You put the bottle away. The scarecrow relaxes so hard that a leaf falls off.*
    - *The Rookidee stay out of the orchard all afternoon.*
    - **Coll** _(neutral)_: ...Leaving it, are you. All right. It's a better scarecrow than a scarecrow, I'll give it that.
    - [quest complete: spared]

**Scene `rematch`** (event: `pf_quest_run(:EL_SCARECROW, :rematch)`)

- *The Sudowoodo is guarding the plum rows. It eyes your Squirt Bottle warily.*
- **CHOICE:** Challenge it?
  - > Challenge it.
    - [battle] Sudowoodo Lv 10 (ROCKHEAD)
      - on caught:
        - **Coll** _(neutral)_: Taking the scarecrow, then. Fair enough. I'll build a real one. Probably.
  - > Leave it.

#### Master of Nothing (`EL_MASTER_OF_NOTHING`)

*Chapter 1 · the Dockmaster, the Dockmaster's House (map 107) · rank 1 · 2 points · unlock `switch(101) && switch(103)`*

The Dockmaster wants to close the Dovetail's ledger properly. Something is still aboard.

**Quest log steps:** `ask`: Search the laid-up Dovetail for whatever is still living aboard. · `ledger`: Take what you found back to the Dockmaster.

**Reward:** POTION x2; +2 pts. **Touches:** none (a quiet one).

**Scene `offer`** (event: `pf_quest_run(:EL_MASTER_OF_NOTHING, :offer)`)

- **Dockmaster** _(neutral)_: Every ship gets a last line in the ledger. 'Laid up. Crew discharged. Nothing aboard.'
- **Dockmaster** _(sad)_: I can't write it for the Dovetail. Something's aboard. Every night, a crackle in the rigging, like a kettle that can't decide.
- **Dockmaster** _(neutral)_: I'm too old for ropes. Would you look? Then I can close the book.
- **CHOICE:** Search the Dovetail?
  - > I'll look.
    - [quest accepted]
    - **Dockmaster** _(neutral)_: Captain Morrow's left the gangplank down. She says it's for the gulls. It isn't.
  - > Not now.

**Scene `rigging`** (event: `pf_quest_run(:EL_MASTER_OF_NOTHING, :rigging)`)

- [stage] On the Dovetail's deck, under the furled mainsail: a nest of tarred rope fibre and fishing line.
- *A Wattrel peers out of the nest. Its feathers crackle with static.*
- *It's been waiting for the ferry to sail, so it can follow it home. The ferry is never going to sail.*
- *The Wattrel looks at the empty sea, then at you. It hops onto your shoulder and settles there, crackling.*
- [quest step: ledger]

**Scene `ledger`** (event: `pf_quest_run(:EL_MASTER_OF_NOTHING, :ledger)`)

- **Dockmaster** _(neutral)_: A Wattrel. Of course. They follow ships. That one followed the last one in and had nowhere left to follow.
- [stage] He dips his pen and writes slowly.
- **Dockmaster** _(neutral)_: 'Dovetail. Laid up. Crew discharged. One Wattrel, rehomed.'
- **Dockmaster** _(happy)_: There. The first ledger line I've liked in a year.
- [receive Wattrel "Mast" Lv 7 (VOLTABSORB)]
- [quest complete]

#### The Last Plank (`EL_LAST_PLANK`)

*Chapter 1 · the lantern rope (Brother Teasel's hand), the empty ferry berth (map 100) · rank 1 · 2 points · unlock `switch(103)`*

Every morning a Timburr carries a plank down to the empty berth and nails it in. Every night the tide takes it. Teasel's note: "Help it finish."

**Quest log steps:** `ask`: Find the Timburr at the empty ferry berth at dawn. · `planks`: Carry the three loose planks from the boatyard to the berth. · `finish`: The berth is mended. Tell the Timburr.

**Reward:** POTION x2; +2 pts. **Touches:** none (Fighting type before the Normal Gym 1).

**Scene `berth`** (event: `pf_quest_run(:EL_LAST_PLANK, :berth)`)

- [stage] Dawn at the empty berth. A Timburr with a plank on its shoulder hammers it into the jetty, steps back, and stares at the sea.
- **Dockmaster** _(neutral)_: The ferry carpenters left it when they went home. It mends the berth for a ferry that isn't coming. Every morning.
- **Dockmaster** _(sad)_: I haven't the heart to tell it. Haven't got the planks either. The boatyard has a few loose ones.
- **CHOICE:** Help the Timburr?
  - > Fetch the planks.
    - [quest accepted]
    - [quest step: planks]
  - > Not now.

**Scene `plank`** (event: `pf_quest_run(:EL_LAST_PLANK, :plank)`)

- [if `quest_count(:SELF, :planks) >= 3`]
  - *That's three. Enough to finish the berth properly, end to end.*
  - [quest step: finish]
- [else]
  - *You heft a loose plank onto your shoulder. The Timburr would do this one-handed.*

**Scene `finish`** (event: `pf_quest_run(:EL_LAST_PLANK, :finish)`)

- *You and the Timburr nail the last three planks in, end to end. For the first time in a year, the berth is whole.*
- *The Timburr looks at the sea for a long time. No ferry. It looks at you.*
- **Dockmaster** _(neutral)_: It's done. Nothing left to mend here. Except, I suppose, whatever you're off to break.
- *The Timburr puts its last plank on its shoulder and falls in beside you.*
- [receive Timburr "Plank" Lv 8 (GUTS)]
- [quest complete]

#### The Tide-Pool Feud (`EL_TIDE_POOL_FEUD`)

*Chapter 2 · Dobbs the shell-gatherer, the shell-gatherers' steps on Lacecliff Walk (map 527) · rank 1 · 2 points · unlock `switch(103)`*

A Crabrawler and a Clobbopus have been fighting over one rock for three days. The shell-gatherers can't reach the pools.

**Quest log steps:** `ask`: Settle the feud at the big tide-pool below Lacecliff Walk.

**Reward:** SUPERPOTION x2; +2 pts. **Touches:** none; the side you help punches open a sea-cave under the cliff (flag :sea_cave, items inside).

**Scene `offer`** (event: `pf_quest_run(:EL_TIDE_POOL_FEUD, :offer)`)

- **Dobbs** _(worried)_: Don't go down to the big pool. There's a fight on.
- **Dobbs** _(neutral)_: Three days now. A Crabrawler and a Clobbopus. Over a rock.
- **Dobbs** _(neutral)_: It's a nice rock, to be fair. Flat. Sun on it all afternoon. I'd fight for it.
- **Dobbs** _(worried)_: But the good pools are past it, and I can't gather shells with a war on.
- **CHOICE:** Settle the feud?
  - > I'll sort it.
    - [quest accepted]
    - **Dobbs** _(happy)_: Pick a side. They respect that. Neither of them respects me.
  - > Not now.

**Scene `pool`** (event: `pf_quest_run(:EL_TIDE_POOL_FEUD, :pool)`)

- *The Crabrawler and the Clobbopus circle the flat rock, fists up, tentacles up, neither blinking.*
- **CHOICE:** Whose side are you on?
  - > Help the Clobbopus.
    - *The Clobbopus slaps the rock with a tentacle, delighted. The Crabrawler turns on you!*
    - [battle] Crabrawler Lv 12 (IRONFIST)
      - on caught:
        - [continue: victory_clob]
      - on won:
        - [continue: victory_clob]
  - > Help the Crabrawler.
    - *The Crabrawler clacks its claws, delighted. The Clobbopus turns on you!*
    - [battle] Clobbopus Lv 12 (TECHNICIAN)
      - on caught:
        - [continue: victory_crab]
      - on won:
        - [continue: victory_crab]
  - > Leave them to it.
    - *You back away. Neither of them noticed you were there.*

**Scene `victory_clob`** (event: `pf_quest_run(:EL_TIDE_POOL_FEUD, :victory_clob)`)

- *The Clobbopus climbs onto its rock, sunbathes for a moment... then punches the cliff behind it, out of sheer joy.*
- *The cliff caves in. Behind it: a sea-cave nobody's seen in a hundred years, full of driftwood and old smugglers' crates.*
- [quest complete: clobbopus]

**Scene `victory_crab`** (event: `pf_quest_run(:EL_TIDE_POOL_FEUD, :victory_crab)`)

- *The Crabrawler climbs onto its rock, then, to celebrate, punches the cliff behind it.*
- *The cliff caves in. Behind it: a sea-cave nobody's seen in a hundred years, full of driftwood and old smugglers' crates.*
- [quest complete: crabrawler]

#### The Borrowed Lanterns (`EL_LANTERNS`)

*Chapter 2 · Sister Hollin, the Saltmere Lantern House (map 140) · rank 1 · 3 points · unlock `switch(103)`*

The theatre district keeps 'borrowing' the Lantern House's lanterns as props. Five are missing before the Night of Floating.

**Quest log steps:** `search`: Find the five borrowed lanterns around Saltmere. · `return`: Take the lanterns back to Sister Hollin.

**Reward:** SILKSCARF; left_one: $400, RES+1; +3 pts. **Touches:** Resonance (Harmony +1 if you leave the stagehand her lantern).

**Scene `offer`** (event: `pf_quest_run(:EL_LANTERNS, :offer)`)

- [stage] The Saltmere Lantern House shares a wall with the Lantern Theatre. Through it, someone is rehearsing a death scene. Loudly.
- *Sister Hollin has earplugs in. She writes on a slate and holds it up.*
- *"THEY TOOK MY LANTERNS. AGAIN."*
- *She wipes it and writes again. "FIVE. NIGHT OF FLOATING IS IN THREE DAYS. HELP."*
- **Sister Hollin** _(angry)_: THE QUIET WAY HAS KEPT A HOUSE HERE FOR NINETY YEARS AND I HAVE NOT HAD ONE QUIET— sorry. Sorry.
- **CHOICE:** Find the lanterns?
  - > I'll find them.
    - [quest accepted]
    - *Sister Hollin writes: "BLESS YOU. CHECK THE PROP ROOM FIRST. IT'S ALWAYS THE PROP ROOM."*
  - > Not now.
    - *Sister Hollin writes: "COWARD." Then, smaller: "(lovingly)"*

**Scene `prop_room`** (event: `pf_quest_run(:EL_LANTERNS, :prop_room)`)

- *The prop room is a forest of crowns, swords and painted trees. On a shelf sits a paper lantern.*
- *...The lantern blinks.*
- **CHOICE:** Poke the lantern?
  - > Poke it.
    - *The lantern turns green, grows a tongue and licks your hand. It's a Kecleon!*
    - [battle] Kecleon Lv 13 (PROTEAN)
      - on caught:
        - *Behind where the Kecleon was sitting is the real lantern, slightly licked.*
        - [continue: found]
      - on won:
        - *The Kecleon flees up into the fly loft, turning the colour of embarrassment.*
        - *Behind where it was sitting is the real lantern, slightly licked.*
        - [continue: found]
      - on lost:
        - *The Kecleon goes back to being a lantern. A smug lantern.*
  - > Leave it.

**Scene `stall`** (event: `pf_quest_run(:EL_LANTERNS, :stall)`)

- **Caramel seller** _(neutral)_: This? It's my display lamp. Makes the caramel glow. Sales went up forty percent.
- **Caramel seller** _(sad)_: ...It's the Lantern House's, isn't it. She wrote me a note. In capitals.
- *The caramel seller hands over the lantern and a bag of broken caramel 'for your trouble'.*
- [continue: found]

**Scene `boat`** (event: `pf_quest_run(:EL_LANTERNS, :boat)`)

- *A fishing boat at the harbour wall has a paper lantern tied to its bow, glowing in the fog.*
- *A note on the tiller: "Borrowed for luck. Bring it back by Floating, sister. - G."*
- *Luck can be borrowed back. You untie it.*
- [continue: found]

**Scene `ropewalk`** (event: `pf_quest_run(:EL_LANTERNS, :ropewalk)`)

- *Halfway down the Old Town ropewalk, a lantern hangs from a hook where the rope-makers can see their twists.*
- *The rope-makers argue for a while about whose turn it was to return it, then about rope, then about each other's mothers.*
- *Nobody notices you take it.*
- [continue: found]

**Scene `stagehand`** (event: `pf_quest_run(:EL_LANTERNS, :stagehand)`)

- [stage] The empty Lantern Theatre, after hours. A young stagehand stands centre stage with a paper lantern at her feet, murmuring lines.
- **Ottilie** _(shocked)_: Oh! I— nobody's meant to be in here. Ottilie. Stagehand. Understudy. Very understudy.
- **Ottilie** _(sad)_: I freeze when there's an audience. So I practise with this. I pretend the light is one face. Just one.
- **Ottilie** _(neutral)_: It's the Lantern House's, isn't it. You can take it. I'll... pretend harder.
- **CHOICE:** Take the lantern?
  - > Take it back.
    - **Ottilie** _(neutral)_: Of course. Thank you for not laughing.
    - [continue: found]
  - > Leave it with her.
    - **Ottilie** _(happy)_: Really? I'll— I'll bring it back after opening night. I promise.
    - [continue: found_left]

**Scene `found`** (event: `pf_quest_run(:EL_LANTERNS, :found)`)

- [if `quest_count(:SELF, :lanterns) + quest_count(:SELF, :left) >= 5`]
  - [quest step: return]
- [else]
  - *That's one more lantern. Sister Hollin will be pleased, in capitals.*

**Scene `found_left`** (event: `pf_quest_run(:EL_LANTERNS, :found_left)`)

- [if `quest_count(:SELF, :lanterns) + quest_count(:SELF, :left) >= 5`]
  - [quest step: return]

**Scene `return`** (event: `pf_quest_run(:EL_LANTERNS, :return)`)

- [if `quest_flag(:SELF, :left_one)`]
  - *You hand Sister Hollin four lanterns and explain about the fifth.*
  - *She reads your face for a long moment. Then she writes, very small: "then it is doing what lanterns are for."*
  - **Sister Hollin** _(happy)_: Four is plenty. Floating's about letting go, after all. I'm told.
  - [quest complete: left_one]
- [else]
  - *Sister Hollin counts the lanterns twice, hugs them, and writes: "FIVE. I COULD KISS YOU. I WON'T. VOW."*
  - [quest complete: all_five]

#### A Hole in the Sky (`EL_PAINT_LOFT`)

*Chapter 2 · Marguerite Fane, the Lantern Theatre paint loft (map 145) · rank 1 · 1 points · unlock `badges >= 1 && switch(108)`*

The Mourner walked straight through the Pageant's painted sky. The scene-painter needs a new backdrop, and a second opinion.

**Quest log steps:** `ask`: Help Marguerite Fane and her Smeargle choose the colours for the new backdrop.

**Reward:** +1 pts. **Touches:** none; the colours you pick decide the Smeargle's moves (Water, Fire, Grass or Ghost coverage).

**Scene `offer`** (event: `pf_quest_run(:EL_PAINT_LOFT, :offer)`)

- [stage] The paint loft. A torn backdrop of the Plates falling hangs from the rigging with a person-shaped hole in it.
- **Marguerite Fane** _(angry)_: Eleven weeks, that sky took. Eleven. And a man in a bark mask walks through it like a curtain.
- **Marguerite Fane** _(sad)_: Brush won't paint since. Sulks. Look at him.
- *A Smeargle sits in the corner with its tail-brush in its mouth, glaring at the hole.*
- **Marguerite Fane** _(neutral)_: He paints whatever moves him. Nothing's moved him since. Tell him what Saltmere looks like to you. Maybe he'll listen to a stranger.
- **CHOICE:** Help pick the colours?
  - > Let's paint.
    - [quest accepted]
    - [continue: choose]
  - > Not now.

**Scene `choose`** (event: `pf_quest_run(:EL_PAINT_LOFT, :choose)`)

- *Brush looks at you, tail-brush raised.*
- **CHOICE:** What does Saltmere look like to you?
  - > Fog on the breakwater.
    - *Brush slaps on grey-blue and white. The new sky is all fog and lamplight.*
    - [continue: finish_sea]
  - > Footlights.
    - *Brush paints in amber and red. The new sky is the inside of a lantern.*
    - [continue: finish_ember]
  - > The road inland.
    - *Brush paints green. The new sky is the forest seen from underneath.*
    - [continue: finish_grove]
  - > After the show.
    - *Brush paints violet and black and one small star.*
    - [continue: finish_night]

**Scene `finish_sea`** (event: `pf_quest_run(:EL_PAINT_LOFT, :finish_sea)`)

- [continue: finish]
- [receive Smeargle "Brush" Lv 12 (TECHNICIAN) (sea palette)]
- [quest complete: sea]

**Scene `finish_ember`** (event: `pf_quest_run(:EL_PAINT_LOFT, :finish_ember)`)

- [continue: finish]
- [receive Smeargle "Brush" Lv 12 (TECHNICIAN) (ember palette)]
- [quest complete: ember]

**Scene `finish_grove`** (event: `pf_quest_run(:EL_PAINT_LOFT, :finish_grove)`)

- [continue: finish]
- [receive Smeargle "Brush" Lv 12 (TECHNICIAN) (grove palette)]
- [quest complete: grove]

**Scene `finish_night`** (event: `pf_quest_run(:EL_PAINT_LOFT, :finish_night)`)

- [continue: finish]
- [receive Smeargle "Brush" Lv 12 (TECHNICIAN) (night palette)]
- [quest complete: night]

**Scene `finish`** (event: `pf_quest_run(:EL_PAINT_LOFT, :finish)`)

- **Marguerite Fane** _(shocked)_: He's... he's painted Dorian's face in the corner. He always paints Dorian's face in the corner.
- **Marguerite Fane** _(happy)_: That's how I know he's better.
- *Brush finishes, puts down his tail, and walks over to stand beside you. He doesn't walk back.*
- **Marguerite Fane** _(neutral)_: Oh, I see. He's moving on. Painters do.
- **Marguerite Fane** _(happy)_: Take him. Saltmere's painted. Paint something bigger.

#### The Sound of Saltmere (`EL_SOUND_OF_SALTMERE`)

*Chapter 2 · Sister Hollin, the Saltmere Lantern House (map 140) · rank 1 · 3 points · unlock `badges >= 1`*

A koan: find the sound Saltmere makes when nobody is performing.

**Quest log steps:** `ask`: Find three true silences in Saltmere. Stand still in each and listen. · `breakwater`: Take the three silences to the very end of the breakwater.

**Reward:** +3 pts. **Touches:** Resonance (Harmony +1).

**Scene `offer`** (event: `pf_quest_run(:EL_SOUND_OF_SALTMERE, :offer)`)

- *Sister Hollin takes her earplugs out. Slowly. It seems to hurt.*
- **Sister Hollin** _(neutral)_: You found my lanterns. So you can find things. Here's a harder one.
- **Sister Hollin** _(neutral)_: Every town has a sound it makes when nobody's watching. Saltmere is always watched. Always performing.
- **Sister Hollin** _(neutral)_: Find three places where it stops. Stand in each. Listen. Then take what you heard to the end of the breakwater.
- **Sister Hollin** _(deadpan)_: Don't ask me what happens then. I've never managed it. Too loud in here.
- **CHOICE:** Take the koan?
  - > I'll listen.
    - [quest accepted]
    - *Sister Hollin puts her earplugs back in, with visible relief.*
  - > Not now.

**Scene `silence_stage`** (event: `pf_quest_run(:EL_SOUND_OF_SALTMERE, :silence_stage)`)

- [if `quest_flag(:SELF, :stage)`]
  - *You've already listened here. The sea is still breathing.*
  - [end scene]
- *The Lantern Theatre after the last bow. The seats creak as they cool.*
- **CHOICE:** Stand still and listen?
  - > Listen.
    - [pause]
    - *...Under everything, so faint you'd never hear it with a crowd: the sea, breathing in and out against the stones.*
    - [if `quest_count(:SELF, :silences) >= 3`]
      - *You've heard it three times now. The same breath, everywhere. You think you know where it's coming from.*
      - [quest step: breakwater]
  - > Move on.

**Scene `silence_ropewalk`** (event: `pf_quest_run(:EL_SOUND_OF_SALTMERE, :silence_ropewalk)`)

- [if `quest_flag(:SELF, :ropewalk)`]
  - *You've already listened here. The sea is still breathing.*
  - [end scene]
- *The Old Town ropewalk, empty. A rope on the long frame turns very slightly in a draught, by itself.*
- **CHOICE:** Stand still and listen?
  - > Listen.
    - [pause]
    - *...Under everything, so faint you'd never hear it with a crowd: the sea, breathing in and out against the stones.*
    - [if `quest_count(:SELF, :silences) >= 3`]
      - *You've heard it three times now. The same breath, everywhere. You think you know where it's coming from.*
      - [quest step: breakwater]
  - > Move on.

**Scene `silence_stall`** (event: `pf_quest_run(:EL_SOUND_OF_SALTMERE, :silence_stall)`)

- [if `quest_flag(:SELF, :stall)`]
  - *You've already listened here. The sea is still breathing.*
  - [end scene]
- *The caramel stall, shuttered. Sugar ticks as it sets in the cold pans.*
- **CHOICE:** Stand still and listen?
  - > Listen.
    - [pause]
    - *...Under everything, so faint you'd never hear it with a crowd: the sea, breathing in and out against the stones.*
    - [if `quest_count(:SELF, :silences) >= 3`]
      - *You've heard it three times now. The same breath, everywhere. You think you know where it's coming from.*
      - [quest step: breakwater]
  - > Move on.

**Scene `breakwater`** (event: `pf_quest_run(:EL_SOUND_OF_SALTMERE, :breakwater)`)

- [stage] The very end of the breakwater. Fog. The lamps of Saltmere behind you, the dark sea ahead.
- *You stand still. You breathe out when the sea does.*
- [pause]
- *Something small steps out of the fog and stands beside you. It is breathing out when you do.*
- *A Ralts. Its horn glows faintly, the colour of the lamps behind you.*
- *Ralts feel what people feel. In Saltmere everyone's feelings are performed. This one has been hiding out here, where the only feeling is the sea's.*
- *It looks up at you as if you're the first quiet thing it's met in a long time.*
- [receive Ralts Lv 12 (TRACE)]
- [effects: RES+1]
- [quest complete]

#### The Orchard Sings (`EL_GLASS_FOAL`)

*Chapter 2 · Brother Teasel, the Ferrow's Landing wayshrine (map 100) · rank 1 · 3 points · unlock `badges >= 1 && switch(105)`*

Since your badge, folk on the orchard lane hear chiming at night, like hooves on glass.

**Quest log steps:** `ask`: Go into the Glassed Orchard (only you can) and follow the chiming. · `follow`: Follow the glass hoofprints deeper into the Orchard. · `foal`: The hoofprints end at the oldest glassed tree.

**Reward:** MOONSTONE; +3 pts. **Touches:** Resonance (Harmony +1 if you approach slowly).

**Scene `offer`** (event: `pf_quest_run(:EL_GLASS_FOAL, :offer)`)

- **Brother Teasel** _(neutral)_: The orchard lane folk say the glass has started singing. Not the wind-chime apples. Something walking.
- **Brother Teasel** _(worried)_: None of us can go past the Veil. You can. I don't know why. I'm not asking why. Out loud.
- **CHOICE:** Go and listen?
  - > I'll go.
    - [quest accepted]
    - **Brother Teasel** _(neutral)_: Whatever it is, it's frightened. Glass is a frightening thing to become.
  - > Not now.

**Scene `hoofprint`** (event: `pf_quest_run(:EL_GLASS_FOAL, :hoofprint)`)

- [if `chase(:SELF) == 0`]
  - *Hoofprints in the glass dust, each one ringing faintly. Something pale moves between the trees and is gone.*
  - [chase advance]
  - [quest step: follow]
  - [end scene]
- [if `chase(:SELF) == 1`]
  - *A foal-shaped shimmer, mane like spun sugar, looks back at you once, then trots off through a glass hedge without breaking it.*
  - [chase advance]
  - [end scene]
- [if `chase(:SELF) == 2`]
  - *The chiming stops. The hoofprints circle the oldest tree in the orchard, the one that glassed first.*
  - [chase advance]
  - [quest step: foal]

**Scene `foal`** (event: `pf_quest_run(:EL_GLASS_FOAL, :foal)`)

- *A Ponyta stands under the glassed tree. Not a fire Ponyta. Its mane is pale and full of light, like the inside of a soap bubble.*
- *It was born in here. It has never seen a tree that wasn't glass.*
- [if `quest_flag(:SELF, :approached)`]
  - *It lowers its horn again. It remembers you.*
  - [continue: fight]
  - [end scene]
- **CHOICE:** How do you approach?
  - > Slowly, palms open.
    - *You walk so slowly it takes a full minute. The Ponyta lets you get close enough to see your face in its eyes... then lowers its horn, curious, testing.*
    - [effects: RES+1]
    - [continue: fight]
  - > Quickly, before it runs.
    - *You lunge. It doesn't run. It rears, and the glass around you rings like a struck bell.*
    - [continue: fight]

**Scene `fight`** (event: `pf_quest_run(:EL_GLASS_FOAL, :fight)`)

- [battle] Galarian Ponyta Lv 15 (PASTELVEIL)
  - on caught:
    - *The Ponyta's mane dims to a gentle glow inside the ball. Outside the Orchard, for the first time, it will see a tree that moves.*
    - [quest complete]
  - on won:
    - *The Ponyta skitters back into the glass trees. Its hoofprints still ring. It isn't gone. It's waiting to see if you come back.*
  - on lost:
    - *You stagger out past the Veil. Behind you, faintly, the glass is still singing.*

#### Three Loyal, Three Knots (`EL_THREE_KNOTS`)

*Chapter 3 · Mother Aldreth, the Briarwick Lantern House (map 120) · rank 1 · 3 points · unlock `badges >= 1`*

A pilgrimage: re-tie the silk knots at the three wayshrines of the Loyal Three, and answer what each shrine asks.

**Quest log steps:** `ask`: Tie a silk knot at the river shrine at the Dyers' Ford, the shrine in Gossamer Wood, and the Loyal Three shrine in Briarwick. · `return`: All three knots are tied. Go back to Mother Aldreth.

**Reward:** MAGICALSEED x2; +3 pts. **Touches:** Lore seed for the Loyal Three / Ogerpon arc (story/04_ACT_I, Elowen legendary arc).

**Scene `offer`** (event: `pf_quest_run(:EL_THREE_KNOTS, :offer)`)

- [stage] The Briarwick Lantern House is a hollow tree. Mother Aldreth sits at a lantern-loom, weaving paper and silk without looking.
- **Mother Aldreth** _(neutral)_: You walked in here the way the Saltmere children walk. All elbows. Sit.
- **Mother Aldreth** _(neutral)_: Three shrines, three knots. The Loyal Three walked this road when they came home with the ogre's... with their prize.
- **Mother Aldreth** _(neutral)_: Every spring someone ties the knots again. This spring the Glasswood got there first, and nobody's young enough to walk it.
- **Mother Aldreth** _(deadpan)_: Each shrine asks a question. Answer honestly. They can tell. So can I.
- **CHOICE:** Walk the pilgrimage?
  - > I'll walk it.
    - [quest accepted]
    - *Mother Aldreth gives you three lengths of silk cord.*
  - > Not now.

**Scene `shrine_river`** (event: `pf_quest_run(:EL_THREE_KNOTS, :shrine_river)`)

- *A stone shrine by the ford, carved with a hound. Its collar is carved as a chain. The dyers' runoff has stained it blue.*
- *Words on the plinth: "WHAT DID THE FIRST OF THE THREE WEAR AT ITS THROAT?"*
- **CHOICE:** Your answer?
  - > A chain of poison.
    - *The old cord falls away at your touch. You tie the new knot.*
    - [continue: knot]
  - > A golden collar.
    - *Nothing happens. The hound's carved eyes seem disappointed in you.*
  - > Nothing. It was free.
    - *Nothing happens. The carved chain is right there.*

**Scene `shrine_wood`** (event: `pf_quest_run(:EL_THREE_KNOTS, :shrine_wood)`)

- *A shrine in a hollow of Gossamer silk, carved with a monkey clutching something to its chest.*
- *"WHAT DID THE SECOND OF THE THREE CARRY HOME?"*
- **CHOICE:** Your answer?
  - > A mask that wasn't theirs.
    - *The silk sighs. You tie the new knot.*
    - [continue: knot]
  - > The ogre's head.
    - *Nothing happens. A Spinarak somewhere tuts.*
  - > A basket of peaches.
    - *Nothing happens. It's a lovely thought, though.*

**Scene `shrine_square`** (event: `pf_quest_run(:EL_THREE_KNOTS, :shrine_square)`)

- *The Loyal Three shrine in Briarwick's square. Children's ogre masks hang around it on pegs.*
- *"WHO WEPT IN THE WOOD WHEN THE THREE CAME HOME?"*
- **CHOICE:** Your answer?
  - > The ogre.
    - *The masks on their pegs turn, very slightly, in no wind. You tie the knot.*
    - [continue: knot]
  - > The villagers, for joy.
    - *Nothing happens. That's the story they tell. It isn't what the shrine asked.*
  - > Nobody.
    - *Nothing happens.*

**Scene `knot`** (event: `pf_quest_run(:EL_THREE_KNOTS, :knot)`)

- [if `quest_count(:SELF, :knots) >= 3`]
  - [quest step: return]

**Scene `return`** (event: `pf_quest_run(:EL_THREE_KNOTS, :return)`)

- **Mother Aldreth** _(neutral)_: Three knots. I felt each one pull tight. Here.
- [stage] She taps her own throat, then her chest, then her eyes.
- **Mother Aldreth** _(neutral)_: A chain. A stolen face. And the one who wept was the one they called the monster.
- **Mother Aldreth** _(deadpan)_: You heard the true story. Don't tell the children. They like the other one.
- **Mother Aldreth** _(neutral)_: An old woman sang it to me better than that once. Never saw her again. Never saw anything again, mind you.
- [quest complete]

#### The Horn and the Pincer (`EL_HORN_AND_PINCER`)

*Chapter 3 · the lantern rope (no one signed it), the sap tree on the old trail, Gossamer Wood (map 524) · rank 1 · 2 points · unlock `badges >= 1`*

Two great Bug Pokémon are fighting over the sap tree on the old trail. The trail has been blocked for a week.

**Quest log steps:** `ask`: Find the sap tree on the old trail in Gossamer Wood and end the fight.

**Reward:** HONEY x2; +2 pts. **Touches:** none; the one you help clears a shortcut (Heracross tears a silk wall, Pinsir crushes a log).

**Scene `tree`** (event: `pf_quest_run(:EL_HORN_AND_PINCER, :tree)`)

- *A Heracross and a Pinsir are locked horn-to-pincer at the foot of a weeping sap tree, shoving each other in slow circles.*
- *Both of them stop and look at you. Then at each other. Then at you.*
- **CHOICE:** Who do you stand with?
  - > Stand with the Heracross.
    - *The Heracross bows. The Pinsir's mandibles open wide.*
    - [battle] Pinsir Lv 15 (MOXIE)
      - on caught:
        - [continue: hera_helps]
      - on won:
        - *The Pinsir crashes away into the undergrowth.*
        - [continue: hera_helps]
  - > Stand with the Pinsir.
    - *The Pinsir clacks once, approving. The Heracross lowers its horn.*
    - [battle] Heracross Lv 15 (MOXIE)
      - on caught:
        - [continue: pinsir_helps]
      - on won:
        - *The Heracross buzzes away over the canopy.*
        - [continue: pinsir_helps]
  - > Back away.

**Scene `hera_helps`** (event: `pf_quest_run(:EL_HORN_AND_PINCER, :hera_helps)`)

- *The Heracross drinks from the sap tree, then hooks its horn into the silk wall behind it and tears it down in one heave.*
- *A shortcut through the Gossamer opens toward Briarwick. The Heracross bows appreciatively and flies off.*
- [quest complete: heracross]

**Scene `pinsir_helps`** (event: `pf_quest_run(:EL_HORN_AND_PINCER, :pinsir_helps)`)

- *The Pinsir drinks from the sap tree, then grips the fallen log across the trail and crushes it to splinters.*
- *A shortcut through the Gossamer opens toward Briarwick. The Pinsir nods appreciatively and stalks off.*
- [quest complete: pinsir]

#### The Silkthief (`EL_SILKTHIEF`)

*Chapter 3 · Hett, the Weavers' Guildhall (map 123) · rank 2 · 3 points · unlock `badges >= 2`*

Somebody is stealing finished silk straight off the drying racks at night. Hett has a theory, and it has eight legs.

**Quest log steps:** `ask`: Find out where Briarwick's silk is going. Hett thinks the Deepwood. · `nest`: Silk threads lead to the old moth nests in Gossamer Deepwood. · `report`: Tell Hett what you found.

**Reward:** $800; guardian: SILVERPOWDER, RES+1; +3 pts. **Touches:** Resonance (Harmony +1 if you leave the Spidops guarding the moths); Briarwick's moth tally board.

**Scene `offer`** (event: `pf_quest_run(:EL_SILKTHIEF, :offer)`)

- **Hett** _(angry)_: Three bolts last night. Four the night before. Finished silk, dyed, ready for the barge.
- **Hett** _(neutral)_: No footprints. Just a thread, one thread, running off the rack into the dark. Toward the Deepwood.
- **Hett** _(worried)_: Tamsin's got enough on her plate. Will you follow the thread? I'd go myself but I'm a weaver, not an idiot.
- **CHOICE:** Follow the thread?
  - > I'll follow it.
    - [quest accepted]
  - > Not now.

**Scene `nest`** (event: `pf_quest_run(:EL_SILKTHIEF, :nest)`)

- [stage] Deep in the Deepwood, the old silk-moth nests hang like paper lanterns. Each one is wrapped in fresh, dyed Briarwick silk.
- *Inside the nests, the cocoons of the dying silk-moths are warm. Someone has been keeping them warm.*
- [quest step: nest]
- [battle] Spidops "Silkthief" Lv 20 (STAKEOUT)
  - on caught:
    - [continue: after]
  - on won:
    - [continue: after]
  - on lost:
    - *The Silkthief hauls itself back up into the canopy and keeps watch over its nests.*

**Scene `after`** (event: `pf_quest_run(:EL_SILKTHIEF, :after)`)

- *The Spidops crouches between you and the nests, legs shaking. It isn't guarding the silk. It's guarding the moths.*
- *The Glasswood's cold has been killing the cocoons. The Spidops has been stealing silk to wrap them warm.*
- **CHOICE:** What do you do?
  - > Take it with you.
    - *The Spidops looks back at its nests once, then follows you.*
    - [Spidops "Silkthief" Lv 20 (STAKEOUT) joins]
    - [quest step: report]
  - > Leave it guarding the nests.
    - *You leave it. It settles back over the cocoons like a hen.*
    - [quest step: report]

**Scene `report`** (event: `pf_quest_run(:EL_SILKTHIEF, :report)`)

- **Hett** _(shocked)_: It was keeping the moths alive? With our silk?
- [if `quest_flag(:SELF, :guardian)`]
  - **Hett** _(neutral)_: Then it can have the offcuts. Every night, on the end rack. Tell no one I'm soft.
  - [quest complete: guardian]
- [else]
  - **Hett** _(neutral)_: And now it's yours. Well. We'll wrap the nests ourselves. Should've been doing it all along.
  - [quest complete: took]

#### The Rehearsal (`EL_REHEARSAL`)

*Chapter 4 · Sister Maelon, the Half-Tally, Frostwick (map 573) · rank 2 · 3 points · unlock `badges >= 2`*

Off the Frostflat Causeway, a stretch of road replays five seconds of a wagon crash, over and over. Something out there is practising a tragedy.

**Quest log steps:** `ask`: Go into The Rehearsal (only you can) and watch the loop. Find out what doesn't belong. · `loop`: Watch the loop three times. Each time, something is a little different. · `finish`: You know who is playing every part. Finish the scene.

**Reward:** SPELLTAG; +3 pts. **Touches:** Resonance (Harmony +1).

**Scene `offer`** (event: `pf_quest_run(:EL_REHEARSAL, :offer)`)

- **Sister Maelon** _(worried)_: Twelve years ago a wagon went over on the causeway road. Everyone lived. Everyone. I checked.
- **Sister Maelon** _(worried)_: Then the Bleed came, and that stretch of road started doing it again. The wagon, the horse, a little girl in the road. Five seconds. Again.
- **Ingrith** _(neutral)_: It's a ghost.
- **Sister Maelon** _(neutral)_: It's not a ghost. Nobody died. It's something rehearsing. Something that saw it once and keeps practising it, because it never saw how it ended.
- **Sister Maelon** _(sad)_: We can't go past the Veil. You can. Will you watch it for me?
- **CHOICE:** Watch the Rehearsal?
  - > I'll watch.
    - [quest accepted]
  - > Not now.

**Scene `watch`** (event: `pf_quest_run(:EL_REHEARSAL, :watch)`)

- [quest step: loop]
- [if `quest_count(:SELF, :loops) == 1`]
  - *The wagon tips. The horse screams. The girl in the road turns her head. Five seconds. Silence. It begins again.*
  - *The horse's scream is a little late. As if it's waiting for its cue.*
- [if `quest_count(:SELF, :loops) == 2`]
  - *The wagon tips. This time the driver's face is the horse's face, for a moment. Then it fixes itself.*
  - *Everyone in the scene is the same shade of pale pink at the edges.*
- [if `quest_count(:SELF, :loops) >= 3`]
  - *The wagon tips. The girl in the road turns her head... and looks straight at you. She has your face for a frame.*
  - *It's one thing. One small, pink thing, playing the wagon and the horse and the girl, because it saw them once and liked the story.*
  - [quest step: finish]

**Scene `finish`** (event: `pf_quest_run(:EL_REHEARSAL, :finish)`)

- *You walk into the scene as it starts again. You take the girl's hand and step her out of the road.*
- *The wagon stops tipping. It doesn't know what to do. Nobody ever showed it what happens next.*
- *The girl, the horse and the wagon melt into one wobbling pink blob. A Ditto. It looks at you, delighted.*
- *Then it becomes you.*
- [battle] Ditto Lv 20 (IMPOSTER)
  - on caught:
    - *The Rehearsal's road is quiet. Just frost, and an old wheel-rut, and nothing happening at all.*
    - [effects: RES+1]
    - [quest complete]
  - on won:
    - *The Ditto puddles away into the frost. Somewhere down the road, faintly, a horse screams on cue. It's started again.*
  - on lost:
    - *Your double bows. The Rehearsal begins again.*

### The Tally

#### Two Hearths, One Pot (`IS_TWO_HEARTHS`)

*Chapter 4 · Brenna and Sigvald, the Two Hearths inn, Frostwick (map 573) · rank 1 · 2 points · unlock `badges >= 2`*

The Two Hearths has two fireplaces, two cooks and one cooking contest that has lasted nineteen years. Both cooks want you to fetch their secret ingredient.

**Quest log steps:** `ask`: Brenna wants wild honey from the Rimewood hives. Sigvald wants smoked eel from Halvard's Smokehouse. · `cook`: You have the honey and the eel. Go back to the Two Hearths.

**Reward:** HONEY x3, LAVACOOKIE x2; one_pot: RARECANDY; +2 pts (+2 The Quiet Way). **Touches:** Joint Trial (Elowen + Isenmar points); WORLD.md's Frostwick sidequest 'The Two Hearths'.

**Scene `offer`** (event: `pf_quest_run(:IS_TWO_HEARTHS, :offer)`)

- [stage] Two fireplaces face each other across the inn. At the left, Brenna (Elowen, flour to the elbows). At the right, Sigvald (Isenmar, smoke in his beard).
- **Brenna** _(happy)_: A traveller! Settle something. Whose stew is better?
- **Sigvald** _(deadpan)_: Don't answer that. She's been asking travellers for nineteen years. They all lie to her.
- **Brenna** _(angry)_: They lie to YOU.
- **Sigvald** _(neutral)_: Midwinter cook-off's tonight. I need smoked eel from Halvard. Proper eel. Black as a boot.
- **Brenna** _(neutral)_: And I need wild honey from the hives in the Rimewood. Frost honey. It tastes like the forest's asleep.
- **Sigvald** _(deadpan)_: Fetch both. Then choose. Then never come back. That's the tradition.
- **CHOICE:** Fetch both ingredients?
  - > Both. Fine.
    - [quest accepted]
    - **Brenna** _(happy)_: A diplomat!
    - **Sigvald** _(deadpan)_: A coward. Same thing.
  - > Not tonight.

**Scene `hive`** (event: `pf_quest_run(:IS_TWO_HEARTHS, :hive)`)

- [if `quest_flag(:SELF, :honey)`]
  - *The hive hums contentedly. You've already been tipped.*
  - [end scene]
- *A hive hangs from a frost-glazed oak, humming. A Combee peers out and looks you up and down.*
- *It drops a frozen comb of honey into your hands, like a tip, and goes back inside.*
- [continue: check]

**Scene `smokehouse`** (event: `pf_quest_run(:IS_TWO_HEARTHS, :smokehouse)`)

- [if `quest_flag(:SELF, :eel)`]
  - **Halvard** _(neutral)_: Go on. Tell Sigvald I smoked it twice. He'll know what that means.
  - [end scene]
- **Halvard** _(neutral)_: Eel for Sigvald? Sit. Nobody leaves my smokehouse without hearing about my father's boat.
- **CHOICE:** Sit and listen?
  - > Sit.
    - *Halvard tells you about his father's boat. It sank. Then it sank again, somehow. It takes a long time.*
    - **Halvard** _(happy)_: Good listener. Here. Black as a boot.
    - [continue: check]
  - > Pay instead ($300).
    - [if `money >= 300`]
      - [pay $300]
      - **Halvard** _(sad)_: Money. Fine. The boat story's free next time.
      - [continue: check]
    - [else]
      - **Halvard** _(deadpan)_: You haven't got it. Sit down.

**Scene `check`** (event: `pf_quest_run(:IS_TWO_HEARTHS, :check)`)

- [if `quest_flag(:SELF, :honey) && quest_flag(:SELF, :eel)`]
  - [quest step: cook]

**Scene `cook`** (event: `pf_quest_run(:IS_TWO_HEARTHS, :cook)`)

- **Brenna** _(happy)_: You've got my honey!
- **Sigvald** _(neutral)_: And my eel. Now. Choose.
- **CHOICE:** Who gets their ingredient?
  - > Brenna gets the honey.
    - *Brenna's honey-cake stew wins. Sigvald says nothing for an hour, then asks for the recipe in a whisper.*
    - [quest complete: brenna]
  - > Sigvald gets the eel.
    - *Sigvald's eel stew wins. Brenna throws a ladle, then a second ladle, then asks for seconds.*
    - [quest complete: sigvald]
  - > Put both in one pot.
    - *You tip the honey and the eel into the same pot. Both cooks scream in two accents.*
    - *The pot bubbles. The whole inn goes quiet. Someone tastes it.*
    - *Honey-glazed smoked eel. Sweet and black and salt-bitter. The room erupts.*
    - **Brenna** _(shocked)_: ...That's good.
    - **Sigvald** _(shocked)_: That's very good. I hate it.
    - **Brenna** _(happy)_: One pot. Nineteen years and nobody thought of one pot.
    - [quest complete: one_pot]
- *A rune is cut in the Half-Tally and a lantern is hung beside it. Both sides of the board claim you now.*

#### The Oathbound Parcel (`IS_OATH_PARCEL`)

*Chapter 4 · Ingrith, the Half-Tally, Frostwick (map 573) · rank 1 · 3 points · unlock `badges >= 2`*

Carry a sealed oath-parcel from Frostwick to the Net Loft in Ebbmouth. In Isenmar a carried oath is not opened. Not ever.

**Quest log steps:** `carry`: Carry Ingrith's sealed parcel to Bersi Gullsong at the Ebbmouth Net Loft. Do not open it. · `deliver`: Deliver the parcel (or what's left of it) to Bersi in Ebbmouth.

**Reward:** $500; +3 pts. **Touches:** Isenmar 'oath' flavour: opening it costs a Trial point and earns you a very rude verse.

**Scene `offer`** (event: `pf_quest_run(:IS_OATH_PARCEL, :offer)`)

- **Ingrith** _(neutral)_: This goes to the Net Loft in Ebbmouth. Sealed with my rune. You carry it, you swear on it.
- **Sister Maelon** _(worried)_: Ingrith, it's moving.
- **Ingrith** _(deadpan)_: It's settling.
- **Sister Maelon** _(worried)_: It's settling with its teeth.
- **Ingrith** _(neutral)_: Whatever it does, you don't open it. A carried oath is a carried oath. Swear?
- **CHOICE:** Swear on the parcel?
  - > I swear.
    - [quest accepted]
    - **Ingrith** _(happy)_: Good. Hold it the right way up. That way.
    - **Sister Maelon** _(deadpan)_: That way is upside down.
  - > What's in it?
    - **Ingrith** _(deadpan)_: An oath. Swear or don't.

**Scene `rattle`** (event: `pf_quest_run(:IS_OATH_PARCEL, :rattle)`)

- [if `quest_flag(:SELF, :rattled)`]
  - [end scene]
- *On the cliff path, the parcel lurches in your arms. Something inside it says "snom" in a small, offended voice.*
- *A corner of the wrapping has been chewed through. Frost is creeping out of the hole.*
- **CHOICE:** Open the parcel?
  - > Open it.
    - *You tear open the parcel. A Snom tumbles out, coughing up rime-silk, and stares at you with enormous eyes.*
    - *It has decided you are its mother. It climbs into your bag and refuses to leave.*
    - [receive Snom Lv 15 (ICESCALES)]
    - [quest step: deliver]
  - > Keep your oath.
    - *You hold the parcel tighter. It says "snom" again, sulkily, and goes back to chewing.*
    - [quest step: deliver]

**Scene `deliver`** (event: `pf_quest_run(:IS_OATH_PARCEL, :deliver)`)

- [if `quest_step(:SELF) == :carry`]
  - [quest step: deliver]
- [if `quest_flag(:SELF, :opened)`]
  - **Bersi Gullsong** _(shocked)_: You OPENED it?
  - **Bersi Gullsong** _(angry)_: OATH-BREAKER! Oath-breaker in my loft! I'll sing of this! I'll sing of this for YEARS!
  - *The Snom peeks out of your bag.*
  - **Bersi Gullsong** _(deadpan)_: ...Well, it ate the oath anyway. Ingrith always seals them in rime-silk. Snom love rime-silk.
  - **Bersi Gullsong** _(neutral)_: Keep it. It's bonded. Taking it off you now would be crueller than the verse I'm going to write.
  - [-1 The Tally points]
  - [quest complete: opened]
- [else]
  - **Bersi Gullsong** _(happy)_: Ingrith's rune, unbroken! Ha! A true carrier!
  - *Bersi slits the seal. A Snom falls out, fat with rime-silk, and immediately crawls back toward you.*
  - **Bersi Gullsong** _(neutral)_: Ingrith seals her oaths in rime-silk. And Snom eat rime-silk. Every year. Every year she forgets.
  - **Bersi Gullsong** _(happy)_: It's imprinted on the hands that carried it. Those are yours. Take it, oath-keeper.
  - [receive Snom Lv 15 (ICESCALES)]
  - [quest complete: kept]

#### A Deed for the Skald (`IS_SKALDS_SAGA`)

*Chapter 4 · Bersi Gullsong, the Ebbmouth Net Loft (map 160) · rank 1 · 2 points · unlock `badges >= 2`*

The Ebb Guild feast is tonight and Bersi has no new saga. He needs a deed. Any deed. He'll handle the exaggerating.

**Quest log steps:** `ask`: Do something saga-worthy in Ebbmouth: beat Gorm the dock bully, or out-fish Old Gudrun (catch 3 Water-type Pokemon). · `feast`: Go back to the Net Loft for the feast.

**Reward:** MYSTICWATER; bully: MARISOL+1; tall_tale: POTION; +2 pts. **Touches:** Marisol bond (+1 for flattening Gorm, who she can't touch because he's Guild).

**Scene `offer`** (event: `pf_quest_run(:IS_SKALDS_SAGA, :offer)`)

- **Bersi Gullsong** _(sad)_: A skald with no saga is just a man shouting in a loft.
- **Bersi Gullsong** _(neutral)_: Feast's tonight. Nothing's happened in Ebbmouth for a month except the river stopping, and nobody wants a song about that.
- **Bersi Gullsong** _(happy)_: So. Do something! Anything! I'll make it bigger. That's the job.
- **CHOICE:** What deed will you do?
  - > Flatten Gorm the dock bully.
    - [quest accepted]
    - **Bersi Gullsong** _(happy)_: Gorm! He charges the net-menders a toll to walk past his crates. Nobody stops him, he's Guild.
  - > Out-fish Old Gudrun.
    - [quest accepted]
    - **Bersi Gullsong** _(happy)_: Catch three water beasts before the feast! Gudrun caught two in a morning, once, in her prime. In AF 261.
  - > I already did something great.
    - [quest accepted]
    - **Bersi Gullsong** _(shocked)_: You did? What?
    - **CHOICE:** Your great deed:
      - > I punched a Gyarados.
      - > I walked through a Bleed Veil.
      - > I ate Larch's kelp tea.
    - **Bersi Gullsong** _(happy)_: MAGNIFICENT. A skald never checks his sources. To the feast!
    - [quest step: feast]
    - [continue: feast]

**Scene `gorm`** (event: `pf_quest_run(:IS_SKALDS_SAGA, :gorm)`)

- **Gorm** _(smug)_: Toll's ten. Twenty for you. You look like you've got pockets.
- [trainer battle] SAILOR Gorm (v50)
  - on won:
    - **Gorm** _(angry)_: Fine! FINE. Walk past my crates. Walk on them. See if I care.
    - *The net-menders cheer from the quay. Somebody throws a fish. It might be a celebration.*
    - [quest step: feast]
  - on lost:
    - **Gorm** _(smug)_: That'll be twenty.

**Scene `feast`** (event: `pf_quest_run(:IS_SKALDS_SAGA, :feast)`)

- [if `quest_flag(:SELF, :deed) == :fish && quest_count(:SELF, :fish) < 3`]
  - **Bersi Gullsong** _(neutral)_: Not enough fish yet! Gudrun's watching. Catch more!
  - [end scene]
- [stage] The Ebb Guild feast. Long tables, eel pies, Marisol at the head of one table with her boots on it. Bersi climbs onto a barrel.
- [if `quest_flag(:SELF, :deed) == :bully`]
  - **Bersi Gullsong** _(happy)_: HEAR, Ebbmouth! The saga of the one who came off the last ferry and met GORM OF THE CRATES!
  - **Bersi Gullsong** _(happy)_: Gorm, whose shoulders blot the sun! Gorm, who eats a net a day! Gorm, who was taller then than he is now!
  - **Bersi Gullsong** _(happy)_: And with ONE command the traveller cast him down, and the crates were free, and the gulls wept!
  - **Marisol** _(smug)_: Gorm's about five foot four.
  - **Bersi Gullsong** _(angry)_: IN THE SAGA HE IS NINE FOOT.
  - **Marisol** _(happy)_: To the traveller! Somebody had to. I'm not allowed. He pays dues.
  - [quest complete: bully]
- [if `quest_flag(:SELF, :deed) == :fish`]
  - **Bersi Gullsong** _(happy)_: HEAR, Ebbmouth! The saga of the angler who drained the Ebb itself!
  - **Bersi Gullsong** _(happy)_: Three beasts from the black water, each one heavier than the last, the third one heavier than the harbour!
  - **Old Gudrun** _(deadpan)_: Two of mine were bigger.
  - **Bersi Gullsong** _(neutral)_: Gudrun, you caught a boot in AF 270 and I sang that as a sea-serpent. Let me work.
  - [quest complete: fish]
- [if `quest_flag(:SELF, :deed) == :tale`]
  - **Bersi Gullsong** _(happy)_: HEAR, Ebbmouth! A saga, freshly told to me by its hero, and therefore completely true!
  - [if `quest_flag(:SELF, :tale) == :gyarados`]
    - **Bersi Gullsong** _(happy)_: They punched a Gyarados! With a fist! The Gyarados apologised!
    - **Marisol** _(deadpan)_: ...My Gyarados is right there. He's very confused.
  - [if `quest_flag(:SELF, :tale) == :veil`]
    - **Bersi Gullsong** _(happy)_: They walked through a Bleed Veil, where no living soul may pass, and came out humming!
    - *The hall laughs. Marisol doesn't. She looks at you for a long moment over her cup.*
  - [if `quest_flag(:SELF, :tale) == :tea`]
    - **Bersi Gullsong** _(happy)_: They drank the kelp tea of Imelda Larch! The whole cup! And lived!
    - *Three separate people at the feast put their cups down and stare at you in horror.*
  - **Bersi Gullsong** _(neutral)_: ...A good saga. Short on witnesses. Half a notch.
  - [quest complete: tall_tale]

#### The Egg Thief of Gullcry (`IS_EGG_THIEF`)

*Chapter 4 · Old Asta, the egg-gatherers' hut on the Gullcry Cliffs (map 561) · rank 2 · 3 points · unlock `badges >= 3`*

Something is taking eggs off the Gullcry ledges. Old Asta wants it stopped. Then she wants it stopped harder.

**Quest log steps:** `ask`: Climb to the high egg ledges on the Gullcry Cliffs and find the egg thief. · `report`: Tell Old Asta what was really happening to her eggs.

**Reward:** $1000; let_go: EXPCANDYM x2, RES+1; +3 pts. **Touches:** Resonance (Harmony +1 if you let the Bombirdier keep its route).

**Scene `offer`** (event: `pf_quest_run(:IS_EGG_THIEF, :offer)`)

- **Old Asta** _(angry)_: Forty years I've gathered off these ledges. Forty! Never lost more than the gulls could spare.
- **Old Asta** _(angry)_: This month: a dozen a night. Gone. And then they turn up in the wrong nests! Wingull eggs under Ducklett! It's chaos!
- **CHOICE:** Find the egg thief?
  - > I'll climb up.
    - [quest accepted]
    - **Old Asta** _(neutral)_: Take the high path. Mind the wind. Mind the thief. Mind my eggs. In that order.
  - > Not now.

**Scene `ledge`** (event: `pf_quest_run(:IS_EGG_THIEF, :ledge)`)

- [stage] The highest ledge. A Bombirdier lands with an egg under each wing, inspects a Ducklett nest, swaps an egg in, and takes one out.
- *It isn't stealing them. It's delivering them. Very carefully. To completely the wrong nests.*
- *It sees you, sees you seeing it, and drops into a dive.*
- [battle] Bombirdier "Postmaster" Lv 24 (ROCKYPAYLOAD)
  - on won:
    - [continue: after]
  - on lost:
    - *The Bombirdier circles once, drops a pebble on your head with great precision, and goes back to work.*

**Scene `after`** (event: `pf_quest_run(:IS_EGG_THIEF, :after)`)

- *The Bombirdier lands on the ledge, puffs up, and offers you an egg. Then it waits for a tip.*
- **CHOICE:** What do you do with it?
  - > Take it with you.
    - *The Bombirdier hops onto your arm. It looks pleased. It looks like it has always wanted a proper route.*
    - [Bombirdier "Postmaster" Lv 24 (ROCKYPAYLOAD) joins]
    - [quest step: report]
  - > Let it keep its route.
    - *You leave it to its deliveries. It salutes with one wing and dives off the cliff with an egg.*
    - [quest step: report]

**Scene `report`** (event: `pf_quest_run(:IS_EGG_THIEF, :report)`)

- **Old Asta** _(shocked)_: Delivering them? It's a Bombirdier, of course it's delivering them. That's all they think about.
- **Old Asta** _(deadpan)_: ...Wingull, Ducklett. They're all eggs. The birds don't seem to mind whose they sit on.
- **Old Asta** _(neutral)_: Eggs is eggs.
- [if `quest_flag(:SELF, :let_go)`]
  - [quest complete: let_go]
- [else]
  - [quest complete: took]

### The Prize Exchange

#### Form 7-B (`ZE_FORM_7B`)

*Chapter 1 · Grant Kiosk P-3NNY, the Quarantine Customs Hall, Ferrow's Landing (map 108) · rank 1 · 2 points · unlock `switch(103)`*

CALL FOR PROPOSALS #0001: DISPOSAL OF UNCLAIMED LIVESTOCK, CRATE 7-B. BOUNTY: $500.

**Quest log steps:** `ask`: Read Crate 7-B's paperwork at the customs kiosk. · `stamps`: Form 7-C (adoption) needs three stamps: Tidewatch Station, the Dockmaster, and the customs duty officer. · `warm`: The Charcadet in Crate 7-B is freezing. Take it up to the lighthouse lamp.

**Reward:** disposed: $500, MERIDIAN+1; adopted: POTION x2; +2 pts. **Touches:** Meridian standing (+1 if you sign the disposal form).

**Scene `offer`** (event: `pf_quest_run(:ZE_FORM_7B, :offer)`)

- [stage] A brass kiosk by the scanner gates. Inside the glass, a Rotom has made itself at home in the ticket machine.
- **P-3NNY** _(happy)_: WELCOME TO THE PRIZE EXCHANGE. I AM GRANT KIOSK P-3NNY. YOU MAY CALL ME PENNY. MOST PEOPLE CALL ME 'THE MACHINE'.
- **P-3NNY** _(neutral)_: CALL FOR PROPOSALS #0001: DISPOSAL OF UNCLAIMED LIVESTOCK, CRATE 7-B.
- **P-3NNY** _(neutral)_: THE OWNER WAS ON THE WRONG SIDE OF THE BORDER WHEN IT CLOSED. THE CRATE WILL BE SHIPPED BACK. NOBODY IS THERE TO RECEIVE IT.
- **P-3NNY** _(happy)_: BOUNTY: $500. PLEASE SIGN FORM 7-B.
- *Under the kiosk, a stencilled crate shivers. Through the slats, two small flames flicker, very low.*
- **CHOICE:** Form 7-B?
  - > Sign it.
    - **P-3NNY** _(happy)_: FORM 7-B ACCEPTED. THANK YOU FOR YOUR EFFICIENCY.
    - *A Meridian tech wheels the crate away. As it passes, she murmurs: "I'll make sure it's somewhere warm. Somewhere."*
    - [quest accepted]
    - [quest complete: disposed]
  - > Are there other forms?
    - **P-3NNY** _(neutral)_: FORM 7-C: ADOPTION OF UNCLAIMED LIVESTOCK. REQUIRES THREE STAMPS: RESEARCH, LIVESTOCK AND CUSTOMS.
    - **P-3NNY** _(neutral)_: PROCESSING TIME: SIX TO EIGHT WEEKS.
    - **P-3NNY** _(happy)_: I AM JOKING. I HAVE BEEN PROGRAMMED WITH ONE (1) JOKE. THAT WAS IT.
    - [quest accepted]
    - [quest step: stamps]
  - > Walk away.

**Scene `stamp_larch`** (event: `pf_quest_run(:ZE_FORM_7B, :stamp_larch)`)

- [if `quest_flag(:SELF, :larch)`]
  - **Larch** _(neutral)_: I've stamped it. Go.
  - [end scene]
- **Larch** _(angry)_: A Charcadet. In a crate. In a sea fog. Who signs these things?
- **Larch** _(neutral)_: Research stamp. Here. It's the station seal. It's also the lid of the teapot. Don't ask.
- [continue: stamp_check]

**Scene `stamp_dock`** (event: `pf_quest_run(:ZE_FORM_7B, :stamp_dock)`)

- [if `quest_flag(:SELF, :dock)`]
  - [end scene]
- **Dockmaster** _(neutral)_: Livestock, arriving? Arriving. Something's arriving.
- [stage] He stamps the form with great ceremony, three times, to be sure.
- **Dockmaster** _(happy)_: First arrival I've stamped since the ferries stopped.
- [continue: stamp_check]

**Scene `stamp_customs`** (event: `pf_quest_run(:ZE_FORM_7B, :stamp_customs)`)

- [if `quest_flag(:SELF, :customs)`]
  - [end scene]
- **Customs officer** _(deadpan)_: Form 7-C? Nobody files 7-C. 7-C is the form we keep so we can say there's a form.
- **CHOICE:** Convince the officer.
  - > Ask nicely.
    - **Customs officer** _(neutral)_: ...Fine. You asked nicely. Nobody asks nicely in customs.
  - > It'll freeze to death.
    - **Customs officer** _(sad)_: ...Yeah. Yeah, it will. Give it here.
  - > Penny said I could.
    - **Customs officer** _(deadpan)_: The machine said. Wonderful. Now I've got to stamp it or explain myself to a ticket dispenser.
- [continue: stamp_check]

**Scene `stamp_check`** (event: `pf_quest_run(:ZE_FORM_7B, :stamp_check)`)

- [if `quest_flag(:SELF, :larch) && quest_flag(:SELF, :dock) && quest_flag(:SELF, :customs)`]
  - *Three stamps. You take Form 7-C back to the kiosk.*
  - **P-3NNY** _(happy)_: FORM 7-C ACCEPTED. CRATE 7-B RELEASED TO APPLICANT. ADVISORY: CONTENTS ARE COLD.
  - **P-3NNY** _(neutral)_: ADVISORY, UNOFFICIAL: THE LIGHTHOUSE LAMP IS THE WARMEST PLACE IN FERROW'S LANDING. I HAVE A THERMAL MAP. I HAVE NOTHING ELSE TO DO.
  - [quest step: warm]

**Scene `warm`** (event: `pf_quest_run(:ZE_FORM_7B, :warm)`)

- [stage] The lighthouse lamp room. Hesper Vane is polishing the lens. She does not turn round.
- **Hesper** _(angry)_: Out.
- *You set the crate down by the lamp. The two small flames inside it sway toward the light.*
- **Hesper** _(deadpan)_: ...Put it nearer, then. Not touching the lens. Nobody touches the lens.
- **Hesper** _(neutral)_: Fire-types used to winter up here when I was a girl. The lamp was better company than most people.
- *The flames climb, steadier, brighter. Something in the crate sits up and looks at you.*
- **Hesper** _(angry)_: Now take it and go. And shut the door. You're letting the warm out.
- [receive Charcadet Lv 6 (FLAMEBODY)]
- [quest complete: adopted]

#### Field Survey: Coastal (`ZE_FIELD_SURVEY`)

*Chapter 2 · Grant Kiosk P-3NNY, any P-3NNY kiosk (Ferrow's Landing, Saltmere, Ebbmouth) (map 108) · rank 1 · 2 points · unlock `switch(103)`*

CALL FOR PROPOSALS #0002: RECORD BATTLES ON THREE (3) DIFFERENT FIELDS. DATA IS THE CURRENCY OF THE FUTURE. SO IS CURRENCY.

**Quest log steps:** `ask`: Battle on three different fields (your Field Notes count them), then report to any P-3NNY kiosk.

**Reward:** EXPCANDYS x3; +2 pts. **Touches:** Field Notes (fields_seen).

**Scene `report`** (event: `pf_quest_run(:ZE_FIELD_SURVEY, :report)`)

- [if `fields_seen >= 3`]
  - **P-3NNY** _(happy)_: DATA RECEIVED. THREE FIELDS. THE REGISTRY THANKS YOU. THE REGISTRY HAS NEVER THANKED ANYONE BEFORE. THIS IS NEW.
  - [quest complete]
- [else]
  - **P-3NNY** _(neutral)_: DATA INSUFFICIENT. PLEASE BATTLE ON MORE FIELDS. THE COAST, THE STAGE, THE FOREST. ANYWHERE THAT IS NOT HERE.

#### The Lattice Hums Wrong (`ZE_LATTICE_HUM`)

*Chapter 4 · Grant Kiosk P-3NNY/2, the tidal Lattice station, Ebbmouth (map 160) · rank 1 · 3 points · unlock `badges >= 2`*

CALL FOR PROPOSALS #0003: ACOUSTIC SURVEY OF THE EBBMOUTH TIDAL LATTICE DURING 'STUTTER EVENTS'. RECORDER PROVIDED.

**Quest log steps:** `ask`: Record the Lattice's hum at the three mill-wheels on the Ebb (the upper wheel, the Guild wheel, the Mill Quay wheel). · `choose`: You have three recordings. Decide who gets the data.

**Reward:** $300; meridian: $1500, MERIDIAN+1; guild: MARISOL+1; larch: EXPCANDYS x2; +3 pts. **Touches:** Meridian standing or Marisol bond, depending on who gets the recordings (foreshadows Larch's tide data in Ch4).

**Scene `offer`** (event: `pf_quest_run(:ZE_LATTICE_HUM, :offer)`)

- **P-3NNY** _(happy)_: HELLO AGAIN. I AM P-3NNY/2. I AM NOT THE SAME KIOSK. I HAVE BEEN TOLD TO SAY THAT.
- **P-3NNY** _(neutral)_: THE LATTICE MAKES A SOUND WHEN THE RIVER STUTTERS. MERIDIAN WOULD LIKE TO KNOW WHAT SOUND. FOR SCIENCE. AND FOR LIABILITY.
- **CHOICE:** Take the recorder?
  - > Take it.
    - [quest accepted]
    - **P-3NNY** _(happy)_: PLEASE DO NOT DROP IT IN THE RIVER. THE RIVER HAS ENOUGH PROBLEMS.
  - > Not now.

**Scene `wheel_upper`** (event: `pf_quest_run(:ZE_LATTICE_HUM, :wheel_upper)`)

- [if `quest_flag(:SELF, :upper)`]
  - [end scene]
- *The upper mill-wheel groans to a stop mid-turn. Under the silence: a low electric whine from the river-mouth pylons.*
- [continue: recorded]

**Scene `wheel_guild`** (event: `pf_quest_run(:ZE_LATTICE_HUM, :wheel_guild)`)

- [if `quest_flag(:SELF, :guild)`]
  - [end scene]
- *The Guild wheel stops. The dockworkers hold their breath. The whine rises, then drops, like something drinking.*
- [continue: recorded]

**Scene `wheel_quay`** (event: `pf_quest_run(:ZE_LATTICE_HUM, :wheel_quay)`)

- [if `quest_flag(:SELF, :quay)`]
  - [end scene]
- *The Mill Quay wheel stops dead. The recorder's needle jumps at the exact moment the whine peaks.*
- [continue: recorded]

**Scene `recorded`** (event: `pf_quest_run(:ZE_LATTICE_HUM, :recorded)`)

- [if `quest_count(:SELF, :recordings) >= 3`]
  - *Three recordings. The stutters and the whine line up every time. You don't know what that means. Someone will.*
  - [quest step: choose]

**Scene `choose`** (event: `pf_quest_run(:ZE_LATTICE_HUM, :choose)`)

- **P-3NNY** _(neutral)_: PLEASE SELECT A RECIPIENT. ALL RECIPIENTS ARE EQUALLY VALUED.
- **P-3NNY** _(neutral)_: (MERIDIAN IS MORE EQUALLY VALUED.)
- **CHOICE:** Who gets the recordings?
  - > Meridian, through the kiosk.
    - **P-3NNY** _(happy)_: TRANSMITTED. A BONUS HAS BEEN APPLIED. NOBODY WILL LISTEN TO THEM, PROBABLY.
    - [quest complete: meridian]
  - > The Ebb Guild.
    - *You take the recorder to the Guild hall. Marisol listens to all three, very still.*
    - **Marisol** _(angry)_: It drinks. When the river stops, it's drinking. Pick one, kid. I know which I'd pick.
    - [quest complete: guild]
  - > Professor Larch, by Gale Post.
    - *You post the recordings to Tidewatch Station.*
    - *A reply comes back by the next Gale Post: "I had this already. Thank you. Please stop doing my job. - I.L."*
    - [quest complete: larch]

### The Trial by Flames

#### The Little Crucible (`AS_LITTLE_CRUCIBLE`)

*Chapter 2 · Sergeant Brakka Emberhide, the Legion recruiting barge, Saltmere harbour (map 146) · rank 1 · 3 points · unlock `badges >= 1`*

WRIT OF FLAME: three bouts, back to back, no healing. Then the barge's mascot. Win and the Legion respects you. Lose and the Legion respects you less.

**Quest log steps:** `ask`: Fight the barge's three recruits in a row (no healing between bouts). · `mascot`: The recruits are beaten. Now face Cinderpaw, the barge's mascot.

**Reward:** $1200, QUICKCLAW; +3 pts. **Touches:** Ashkaar flavour: honesty is law; signing up (flag :recruited) changes how later Legion NPCs greet you.

**Scene `offer`** (event: `pf_quest_run(:AS_LITTLE_CRUCIBLE, :offer)`)

- [stage] A black-hulled barge moored at the free harbour, a fire pit on deck ringed with rope. A banner: JOIN THE LEGION. MOST RECRUITS SURVIVE.
- **Sergeant Brakka** _(smug)_: In Ashkaar nobody asks who your mother was. They ask how hard you hit.
- **Sergeant Brakka** _(neutral)_: Saltmere's a free port, so we can hold bouts here. The Elowen crown hates it. That's a bonus.
- **Sergeant Brakka** _(neutral)_: Writ of Flame: three of my recruits, one after another, no potions between. Then you face Cinderpaw.
- **CHOICE:** Ask Brakka something?
  - > Will I get hurt?
    - **Sergeant Brakka** _(neutral)_: Yes.
    - **Sergeant Brakka** _(deadpan)_: Lying's a crime where I'm from. You'd be amazed how much faster recruitment goes.
  - > What's Cinderpaw?
    - **Sergeant Brakka** _(happy)_: Our mascot. A Litleo. Too wild to keep, too proud to leave. Bit three officers. Promoted twice.
  - > Let's fight.
- **CHOICE:** Take the Writ of Flame?
  - > Brand me.
    - [quest accepted]
    - **Sergeant Brakka** _(happy)_: Good. HERALD! Ring the pit!
    - [continue: bouts]
  - > Not yet.
    - **Sergeant Brakka** _(neutral)_: Honest answer. I respect that. Come back when it changes.

**Scene `bouts`** (event: `pf_quest_run(:AS_LITTLE_CRUCIBLE, :bouts)`)

- **Barge herald** _(happy)_: BOUT ONE! From the Cinder Cape, with a punch like a bad decision: RECRUIT REKK!
- [gauntlet, no healing] ASHKAAR_SOLDIER_M Rekk (v50) -> ASHKAAR_SOLDIER_F Vasha (v50) -> ASHKAAR_OFFICER Brakka (v50) on `:COLOSSEUM`
  - on won:
    - **Sergeant Brakka** _(smug)_: Three for three. You hit like an Ashkaari. That's the nicest thing I know how to say.
    - [quest step: mascot]
    - [continue: mascot]
  - on lost:
    - **Sergeant Brakka** _(neutral)_: Down. No shame in it. Some shame in it. Heal up and come back; the Writ stays yours.

**Scene `mascot`** (event: `pf_quest_run(:AS_LITTLE_CRUCIBLE, :mascot)`)

- **Barge herald** _(happy)_: AND NOW! UNDEFEATED ON THIS DECK! BITER OF OFFICERS! CINDERPAW!
- [battle] Litleo "Cinderpaw" Lv 17 (MOXIE)
  - on won:
    - *Cinderpaw shakes its smoking mane, looks at the crew, looks at you... and trots over to sit at your feet.*
    - **Sergeant Brakka** _(shocked)_: Huh. It's picked you. It's never picked anybody. It bit the last person who tried to pick it.
    - **Sergeant Brakka** _(neutral)_: Take it. In the Legion, strength chooses strength. Even the little ones.
    - [continue: sign]
  - on lost:
    - **Sergeant Brakka** _(deadpan)_: Cinderpaw remains undefeated. Cinderpaw is insufferable about it.

**Scene `sign`** (event: `pf_quest_run(:AS_LITTLE_CRUCIBLE, :sign)`)

- **Sergeant Brakka** _(neutral)_: One more thing. Recruitment papers. Sign and you're Legion-in-waiting. Means nothing yet. Means something later.
- **CHOICE:** Sign the papers?
  - > Sign.
    - **Sergeant Brakka** _(happy)_: Ha! Ember-recruit, then. Show that paper in Cindervault and someone will buy you a drink. Or fight you.
  - > Decline.
    - **Sergeant Brakka** _(neutral)_: Honest. Fine. The offer stands as long as you keep winning.
- *The Herald strikes the gong. Your brand goes up on the barge's little Wall of the Proven.*
- [quest complete]
