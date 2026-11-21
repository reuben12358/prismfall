# TRIALS_QUESTS — every Trial quest, and the full script of the implemented ones

> **Generated** by `ruby tools/trials_docs.rb` from `plugins/Prismfall Trials/1xx_*.rb`. Edit the plugin data, not this file.
> Design of the institutions, ranks and boards: `design/TRIALS.md`. Event Pokémon: `design/EVENT_POKEMON.md`.
> Map IDs are current `maps.json` IDs (names change; IDs don't). Chapters and order follow SPINE Revision 14.
> **Status:** *wired* = scenes written and testable (map events in `design/TRIAL_EVENTS.yaml`); *designed* = `:stub`, off the boards until wired.

**106 quests** (48 wired, 58 designed) across 8 Trials.

| Trial | Quests | Wired |
|---|---|---|
| The Quiet Way (Elowen) | 25 | 20 |
| The Tally (Isenmar) | 12 | 6 |
| The Prize Exchange (Zenith) | 11 | 5 |
| The Gutter Book (Nadir) | 13 | 4 |
| The Trial by Flames (Ashkaar) | 13 | 5 |
| The Rolls of Unearthing (Ossaria) | 12 | 4 |
| The Rite of Reflection (Antumbra) | 10 | 2 |
| The Hall of Petitions (Crownhaven) | 10 | 2 |

## Part 1. Catalogue

### The Quiet Way — Elowen

| Quest | Ch | Unlock | Giver · where (map) | Rank · Rec Lv | What happens | Reward | Touches | Status |
|---|---|---|---|---|---|---|---|---|
| **The First Lesson** `EL_FIRST_LESSON` | 1 | `switch(103)` | Brother Teasel · the wayshrine by the Accord plaque (100) | ★ · 5 | Do one kind thing in Ferrow's Landing that nobody asked you to do. Then go back to Brother Teasel. | ORANBERRY x2; silent: RES+1; +2 pts | Resonance (Harmony +1 for keeping quiet); starts the realm-wide Quiet Deeds tally | wired |
| **The Tart Thief** `EL_TART_THIEF` | 1 | `switch(103)` | Wenna Hale · the tart stall on the quay (100) | ★ · 7 | Someone keeps stealing Wenna Hale's bramble tarts. Brother Teasel's note on the lantern: "The thief is hungry, not wicked." | $200, ORANBERRY x3; told: KESTREL-1; +2 pts | Kestrel bond (+1 if you split the evidence, -1 if you tell on him) | wired |
| **The Scarecrow Walks** `EL_SCARECROW` | 1 | `switch(103)` | Coll Hale · the Hale farmhouse (523) | ★ · 9 | Coll Hale's scarecrow keeps moving to a different field. Coll did not build a scarecrow. | spooked: $300; spared: MIRACLESEED, RES+1; +2 pts | Resonance (Harmony +1 if you leave it be); the Sudowoodo can be caught after Badge 2 | wired |
| **Master of Nothing** `EL_MASTER_OF_NOTHING` | 1 | `switch(101) && switch(103)` | the Dockmaster · the Dockmaster's House (107) | ★ · 6 | The Dockmaster wants to close the Dovetail's ledger properly. Something is still aboard. | POTION x2; +2 pts | none (a quiet one); the Wattrel joins you in Ebbmouth after Badge 3 | wired |
| **The Last Plank** `EL_LAST_PLANK` | 2 | `badges >= 1` | the lantern rope (Brother Teasel's hand) · the empty ferry berth (100) | ★ · 13 | Every morning a Timburr carries a plank down to the empty berth and nails it in. Every night the tide takes it. Teasel's note: "Help it finish." | POTION x2; +2 pts | none; a Fighting type only after Dorian's badge (Revision 16: no answer to the next Warden before the gym) | wired |
| **The Tide-Pool Feud** `EL_TIDE_POOL_FEUD` | 2 | `badges >= 1` | Dobbs the shell-gatherer · the shell-gatherers' steps on Lacecliff Walk (527) | ★ · 14 | A Crabrawler and a Clobbopus have been fighting over one rock for three days. The shell-gatherers can't reach the pools. | SUPERPOTION x2; +2 pts | none; the side you help punches open a sea-cave under the cliff (flag :sea_cave, items inside) | wired |
| **The Borrowed Lanterns** `EL_LANTERNS` | 2 | `switch(103)` | Sister Hollin · the Saltmere Lantern House (140) | ★ · 12 | The theatre district keeps 'borrowing' the Lantern House's lanterns as props. Five are missing before the Night of Floating. | SILKSCARF; left_one: $400, RES+1; +3 pts | Resonance (Harmony +1 if you leave the stagehand her lantern) | wired |
| **A Hole in the Sky** `EL_PAINT_LOFT` | 2 | `badges >= 1 && switch(108)` | Marguerite Fane · the Lantern Theatre paint loft (145) | ★ · 13 | The Mourner walked straight through the Pageant's painted sky. The scene-painter needs a new backdrop, and a second opinion. | +1 pts | none; the colours you pick decide the Smeargle's moves (Water/Ice, Ghost, Fairy or Ground coverage) | wired |
| **The Sound of Saltmere** `EL_SOUND_OF_SALTMERE` | 2 | `badges >= 1; after EL_LANTERNS` | Sister Hollin · the Saltmere Lantern House (140) | ★ · 14 | A koan: find the sound Saltmere makes when nobody is performing. | +3 pts | Resonance (Harmony +1) | wired |
| **The Orchard Sings** `EL_GLASS_FOAL` | 2 | `badges >= 1 && switch(105)` | Brother Teasel · the Ferrow's Landing wayshrine (100) | ★ · 15 | Since your badge, folk on the orchard lane hear chiming at night, like hooves on glass. | MOONSTONE; +3 pts | Resonance (Harmony +1 if you approach slowly) | wired |
| **Three Loyal, Three Knots** `EL_THREE_KNOTS` | 3 | `badges >= 1` | Mother Aldreth · the Briarwick Lantern House (120) | ★ · 16 | A pilgrimage: re-tie the silk knots at the three wayshrines of the Loyal Three, and answer what each shrine asks. | MAGICALSEED x2; +3 pts | Lore seed for the Loyal Three / Ogerpon arc (story/04_ACT_I, Elowen legendary arc) | wired |
| **The Horn and the Pincer** `EL_HORN_AND_PINCER` | 3 | `badges >= 2` | the lantern rope (no one signed it) · the sap tree on the old trail, Gossamer Wood (524) | ★ · 19 | Two great Bug Pokémon are fighting over the sap tree on the old trail. The trail has been blocked for a week. | HONEY x2; +2 pts | none; the one you help clears a shortcut (Heracross tears a silk wall, Pinsir crushes a log) | wired |
| **The Silkthief** `EL_SILKTHIEF` | 3 | `badges >= 2` | Hett · the Weavers' Guildhall (123) | ★★ · 20 | Somebody is stealing finished silk straight off the drying racks at night. Hett has a theory, and it has eight legs. | $800; guardian: SILVERPOWDER, RES+1; +3 pts | Resonance (Harmony +1 if you leave the Spidops guarding the moths); Briarwick's moth tally board | wired |
| **The Moss Hymn** `EL_OCTAVE_MOSS` | 3 | `badges >= 1` | Lyra of the Octave · under the Lantern House tree, Briarwick; the moss-stone in Gossamer Wood (524) (120) | ★ · 18 | A singer of the Octave has been singing to her Eevee for three days. It will not come down from the moss-stone in Gossamer Wood. | $800, BIGROOT; +3 pts | The Octave: Lyra (1 of 8 in gym order) | wired |
| **Someone Apologising to Bugs** `EL_SHELLY` | 3 | `badges >= 2` | Mother Aldreth · the Briarwick Lantern House (120) | ★★ · 21 | A stranger with pink hair is lost in the Gossamer Deepwood, apologising to the Bug Pokemon. The spirits of the wood are uneasy. **Twist:** Board pointer to CAMEOS.md 'Lost in the Gossamer'. The cameo event calls Prismfall.cameo_battle(:FESTIVAL_SHELLY, "Shelly", 1, double: true) and then pf_quest_complete(:EL_SHELLY). Moved from 'after Gym 1' to 'after Gym 2' by SPINE Rev 14. | SILVERPOWDER; +3 pts | Ledger cameo record (FESTIVAL_SHELLY); CAMEOS.md #1 | designed |
| **The Rehearsal** `EL_REHEARSAL` | 4 | `badges >= 2` | Sister Maelon · the Half-Tally, Frostwick (573) | ★★ · 20 | Off the Frostflat Causeway, a stretch of road replays five seconds of a wagon crash, over and over. Something out there is practising a tragedy. | SPELLTAG; +3 pts | Resonance (Harmony +1) | wired |
| **The Humming Lamp** `EL_LAMP_LENS` | 5 | `badges >= 3` | Hesper Vane · the Ferrow Lighthouse lamp room (106) | ★ · 23 | A paper lantern from the lighthouse: 'THE LAMP HUMS. MAKE IT STOP. - H.V.' | AMPHAROSITE; +1 pts | Kestrel's family: Morwen set the stone; it hums for the PC. | wired |
| **Gerald** `EL_GERALD` | 10 | `badges >= 8 && switch(126)` | the Queen's Keeper of Small Creatures · the Royal Chase (682) | ★★★ · 44 | Queen Maelis's named Scatterbugs have escaped into the Royal Chase. Each one has a personality file. Gerald's is four pages long. **Twist:** Six hide-and-seek finds, each solved by reading its file (Doris likes warm stones, Percival hates the colour blue...). Gerald hides inside the Queen's own crown on its stand in the hunting lodge. Reward: Gerald, a Fancy-pattern Scatterbug. | SHINYSTONE, Scatterbug "Gerald" Lv 40 (COMPOUNDEYES); +3 pts | Elowen Crown favour (flavour); Queen Maelis comedy (15_COMEDY 'The Royal We') | designed |
| **The Rootward Wake** `EL_ROOTWARD_WAKE` | 10 | `badges >= 8` | a Rootward laundress · the Rootward slums, Verdance (296) | ★★★ · 44 | In Verdance nothing rots, so nothing is ever properly buried. The Rootward wants one funeral done right. **Twist:** Fetch a candle that's allowed to burn out, a flower picked from outside Verdance (it wilts on the way: that's the point) and a song nobody's sung since the Bleed. A Phantump comes to the wake and sits with the mourners. If Rowan's arc has turned (S124), one mourner is a Hollow sympathiser and says so. | CLEANSETAG, TM20; +3 pts | Resonance; Rowan's theme ('everything that grows must be allowed to die') | designed |
| **What the Bride Tree Hears** `EL_EVER_BLOOM` | 10 | `badges >= 8 && switch(125)` | Juno · the Heartgarden, Verdance (294) | ★★★ · 46 | Juno wants to know whether her Aunt Elin can still hear her. The Quiet Way says the Root carries voices. Juno says she'd like proof. **Twist:** A Mindscape-light puzzle under the Heartgarden: the roots repeat whatever you place against them, late, like an echo. Juno places a seed packet. Nothing. She places her bouquet. The roots hum the counting rhyme. Juno laughs and cries at once. Reward: a white Floette grown from the Bride Tree's blossoms (Juno names it Ever-Bloom). | Floette "Ever-Bloom" Lv 44 (FLOWERVEIL), JUNO+2; +4 pts | Juno bond (+2); Elin / Homecoming foreshadowing | designed |
| **The Bride Tree's Heart** `EL_BRIDE_TREE_HEART` | 11 | `badges >= 9` | Juno Hale · the Heartgarden, Verdance, under the Bride Tree (after J3) (294) | ★ ·  | Juno is waiting under the Bride Tree. | VENUSAURITE; +0 pts | Sets up J4: the Grass Warden's ring won't answer Juno yet (it does by the Festival: her Mega Gardevoir). | wired |
| **The Old Pincer** `EL_OLD_PINCER` | 14 | `badges >= 12` | the Woodward · the Woodward's Hut, Gossamer Wood; the fight is in the Gossamer Heartwood (526) | ★★ · 62 | A lantern from the Woodward: 'THE OLD PINCER HAS TAKEN THE HEARTWOOD SAP. BRING SOMEONE STRONG.' | PINSIRITE; +3 pts |  | wired |
| **The Doll Who Waited** `EL_DOLL_WHO_WAITED` | 16 | `badges >= 14` | A doll in the attic · Thistledown Manor attic (547) | ★ · 68 | A lantern with a child's scrawl: 'SOMETHING KNOCKS IN THE THISTLEDOWN ATTIC. IT WANTS ITS BUTTONS.' | BANETTITE, GHOSTIUMZ; +2 pts |  | wired |
| **Encore** `EL_ENCORE` | 18 | `badges >= 16` | Dorian Pell · the Grand Stage, Pell Playhouse, Saltmere (154) | ★ · 80 | A gilt-edged lantern: 'ONE NIGHT ONLY. THE PLAYHOUSE REQUIRES A STAR. - D.P.' | LOPUNNITE, NORMALIUMZ; +2 pts |  | wired |
| **The Twilight Cloister** `EL_TWILIGHT_CLOISTER` | 18 | `badges >= 16` | the Abbess · the Twilight Cloister, Gloaming (440) | ★★★★★ · 78 | The last trial of the Quiet Way: walk the dusk-chapels from end to end without saying anything at all. **Twist:** Every chapel stages a scene that begs a response (a child asks the way, a Thornguard insults you, a ghost of someone you failed). Each choice list has a silent option, worded differently each time. Speaking costs nothing but resets you to the first chapel. Celestine watches from the eighth and finally speaks to you as herself. | MAGICALSEED x3; +5 pts | Resonance (Harmony +2); unlocks the Quiet Way's Evergreen rank | designed |

### The Tally — Isenmar

| Quest | Ch | Unlock | Giver · where (map) | Rank · Rec Lv | What happens | Reward | Touches | Status |
|---|---|---|---|---|---|---|---|---|
| **Two Hearths, One Pot** `IS_TWO_HEARTHS` | 4 | `badges >= 2` | Brenna and Sigvald · the Two Hearths inn, Frostwick (573) | ★ · 16 | The Two Hearths has two fireplaces, two cooks and one cooking contest that has lasted nineteen years. Both cooks want you to fetch their secret ingredient. | HONEY x3, LAVACOOKIE x2; one_pot: RARECANDY; +2 pts (+2 The Quiet Way) | Joint Trial (Elowen + Isenmar points); WORLD.md's Frostwick sidequest 'The Two Hearths' | wired |
| **The Oathbound Parcel** `IS_OATH_PARCEL` | 4 | `badges >= 2` | Ingrith · the Half-Tally, Frostwick (573) | ★ · 17 | Carry a sealed oath-parcel from Frostwick to the Net Loft in Ebbmouth. In Isenmar a carried oath is not opened. Not ever. | $500; +3 pts | Isenmar 'oath' flavour: opening it costs a Trial point and earns you a very rude verse | wired |
| **A Deed for the Skald** `IS_SKALDS_SAGA` | 4 | `badges >= 2` | Bersi Gullsong · the Ebbmouth Net Loft (160) | ★ · 19 | The Ebb Guild feast is tonight and Bersi has no new saga. He needs a deed. Any deed. He'll handle the exaggerating. | MYSTICWATER; bully: MARISOL+1; tall_tale: POTION; +2 pts | Marisol bond (+1 for flattening Gorm, who she can't touch because he's Guild) | wired |
| **The Egg Thief of Gullcry** `IS_EGG_THIEF` | 4 | `badges >= 3` | Old Asta · the egg-gatherers' hut on the Gullcry Cliffs (561) | ★★ · 24 | Something is taking eggs off the Gullcry ledges. Old Asta wants it stopped. Then she wants it stopped harder. | $1000; let_go: EXPCANDYM x2, RES+1; +3 pts | Resonance (Harmony +1 if you let the Bombirdier keep its route) | wired |
| **The Drowned Note** `IS_OCTAVE_DROWNED_NOTE` | 4 | `badges >= 2` | Aria of the Octave · the river steps, Ebbmouth; the Mill Quay wheel (167) (160) | ★ · 22 | A singer's Vaporeon melted into the Ebb when the river stuttered and hasn't come out. She can still hear it, sometimes. | $1200, SHELLBELL; +3 pts | The Octave: Aria (2 of 8 in gym order); a verse on the Tally Mast | wired |
| **The White Stag** `IS_WHITE_STAG` | 11 | `badges >= 9` | the lodge-keeper · Snowbriar (710) | ★★ · 48 | A white stag has been seen in the royal hunting woods. Elowen law says it's the Crown's. The trappers say it's nobody's. **Twist:** Four-sighting chase in deep snow; it only appears at dawn. At the end: battle and catch (EVENT IS_WHITE_STAG), report it to the Crown's lodge (Elowen points), or let the trappers' children see it once and let it go (Harmony). | $4000; +3 pts | Elowen vs Isenmar clan rights (WORLD.md 'The White Stag'); Thane's standing flavour | designed |
| **The Harpoon Rite** `IS_HARPOON_RITE` | 11 | `badges >= 9` | Old Halla Brinesdottir · the Great Tally, Rimeholt (306) | ★★★ · 50 | Every Harpooner earns the rank by facing the Old Bull on the ice. The Old Bull is a Cetitan. It has never once been harpooned. **Twist:** Boss Cetitan (3 bars) on :FROZEN_LAKE; the field cracks to :WATER_SURFACE at bar 2. Nobody harpoons it: the rite is to stand your ground. Win and it slaps the ice twice and swims under you (no catch). The calf that follows it out joins you (EVENT IS_CETODDLE). | NEVERMELTICE; +4 pts | Before the Thaw only (expires on S128 CH11_THAW) | designed |
| **Eleven Years at One Hole** `IS_ELEVEN_YEARS` | 11 | `badges >= 9` | Old Torstein · the ice-fishing flats, Rimeholt (300) | ★ · 47 | Old Torstein has fished one ice-hole for eleven years waiting for a single bite. He has not noticed he is sitting on an Avalugg. **Twist:** You fish his hole; a Tatsugiri has been nibbling the bait for eleven years without ever taking the hook. When Torstein stands up to cheer, his 'seat' stands up too. 'How long has that been there?' 'About eleven years, sir.' Reward: the Tatsugiri. | Tatsugiri Lv 48 (COMMANDER); +2 pts | 15_COMEDY Isenmar bit | designed |
| **The Sinking Quarter** `IS_SINKING_QUARTER` | 11 | `switch(128)` | a net-mender of Net Row · the Sinking Quarter, Rimeholt (309) | ★★★ · 52 | After the Thaw, the lower town is going under. Three families won't leave without their boat, their grandmother and their Lapras, in that order. **Twist:** Timed escort over breaking ice (floes sink after N steps); at the gate the checkpoint officer is an ISENMAR_OFFICER battle or a bribe or Anja's word if her bond is good. | EXPCANDYL x2; +4 pts | Refugee arc (S168 ISENMAR_MARTIAL_LAW); Thane / Anja politics | designed |
| **Crystal Sleep** `IS_ALEXANDRA` | 11 | `badges >= 10 && switch(128)` | Old Halla Brinesdottir · the sunken lower town, Rimeholt (309) | ★★★ · 56 | Something sleeps in a block of ice in the sunken quarter: a woman, very much alive, very annoyed about it. **Twist:** Board pointer for the Alexandra cameo; her event completes the quest. | ICYROCK; +3 pts | CAMEOS.md #5 'Crystal Sleep' (FESTIVAL_ALEXANDRA) | designed |
| **The Saga of the Glass Dunes** `IS_SAGA_OF_THE_ICE` | 15 | `badges >= 13` | Bersi Gullsong · Skaldfast (921) | ★★★★★ · 70 | Bersi wants to sing the war. Truthfully, for once. He needs a witness who stood on the glass. **Twist:** Bersi sings the war straight, no exaggeration, and it's the first time the hall goes silent for him: Skaldfast on the sand, the flood, the glass, the bone-carters. His verses use the war choice keys, so the saga is different on every war outcome. | Lapras "Saga" Lv 45 (WATERABSORB); +5 pts | War choices (war_climax / war_terms): the saga's words follow what you chose | designed |
| **The Causeway Matriarch** `IS_CAUSEWAY_MATRIARCH` | 18 | `badges >= 16` | the Matriarch · the Frostflat Causeway at low tide (560) | ★ · 78 | A Kangaskhan the size of a hut has taken the Frostflat Causeway. | KANGASKHANITE; +3 pts |  | wired |

### The Prize Exchange — Zenith

| Quest | Ch | Unlock | Giver · where (map) | Rank · Rec Lv | What happens | Reward | Touches | Status |
|---|---|---|---|---|---|---|---|---|
| **Form 7-B** `ZE_FORM_7B` | 1 | `switch(103)` | Grant Kiosk P-3NNY · the Quarantine Customs Hall, Ferrow's Landing (108) | ★ · 5 | CALL FOR PROPOSALS #0001: DISPOSAL OF UNCLAIMED LIVESTOCK, CRATE 7-B. BOUNTY: $500. | disposed: $500, MERIDIAN+1; adopted: POTION x2; +2 pts | Meridian standing (+1 if you sign the disposal form); the Charcadet is collected after Badge 2 | wired |
| **Field Survey: Coastal** `ZE_FIELD_SURVEY` | 2 | `switch(103)` | Grant Kiosk P-3NNY · any P-3NNY kiosk (Ferrow's Landing, Saltmere, Ebbmouth) (108) | ★ · 10 | CALL FOR PROPOSALS #0002: RECORD BATTLES ON THREE (3) DIFFERENT FIELDS. DATA IS THE CURRENCY OF THE FUTURE. SO IS CURRENCY. | EXPCANDYS x3; +2 pts | Field Notes (fields_seen) | wired |
| **The Lattice Hums Wrong** `ZE_LATTICE_HUM` | 4 | `badges >= 2` | Grant Kiosk P-3NNY/2 · the tidal Lattice station, Ebbmouth (160) | ★ · 20 | CALL FOR PROPOSALS #0003: ACOUSTIC SURVEY OF THE EBBMOUTH TIDAL LATTICE DURING 'STUTTER EVENTS'. RECORDER PROVIDED. | $300; meridian: $1500, MERIDIAN+1; guild: MARISOL+1; larch: EXPCANDYS x2; +3 pts | Meridian standing or Marisol bond, depending on who gets the recordings (foreshadows Larch's tide data in Ch4) | wired |
| **Off the Beat** `ZE_OCTAVE_OFF_BEAT` | 5 | `badges >= 3` | Grant Kiosk P-3NNY / Cadence of the Octave · the Lowlight steps, Lumen City (181) | ★ · 26 | CALL FOR PROPOSALS #0031: NOISE COMPLIANCE, LOWLIGHT BLOCK 9. A STREET DRUMMER'S JOLTEON BLACKS OUT THE BLOCK. BOUNTY: $800. | $800, CELLBATTERY x2; unknown: RES+1; fault: $800, MERIDIAN+1; +3 pts | The Octave: Cadence (3 of 8 in gym order); Meridian standing if you file it as a Lattice fault | wired |
| **Customer Support** `ZE_CUSTOMER_SUPPORT` | 5 | `badges >= 3` | Helpdesk Rotom · Meridian Spire lobby, Lumen City (185) | ★ · 24 | Walk a form through nine offices. The form is to cancel the form. **Twist:** Each office wants a different stamp first (circular dependency the player has to break by noticing office 4 has two doors). When the form is finally cancelled, it cancels itself out of existence. What's left on the desk is a Porygon, who was the form all along. | Porygon Lv 24 (DOWNLOAD); +3 pts | 15_COMEDY Zenith bit 'Customer Support' | designed |
| **The Machine Wants Compliments** `ZE_FIZZBOLT` | 5 | `badges >= 3` | a Fizzbolt vending machine · Lumen City Concourse (180) | ★ · 24 | A Lumen vending machine has gained sentience from the free current and only sells Fizzbolt to people who compliment it. **Twist:** Five compliments across five visits; each needs a fresh one (choice lists rotate). Repeat a compliment and it sulks for a day. On the fifth it dispenses everything at once and a Rotom flies out to thank you, then back in. | CELLBATTERY; +2 pts | none | designed |
| **Product Recall** `ZE_ROTOM_RECALL` | 5 | `badges >= 3` | the Lumen Arcade floor manager · Lumen Arcade Dept. Store (183) | ★★ · 26 | Five display appliances have walked off the shop floor. They were not supposed to be able to walk. **Twist:** A hide-and-seek in the department store; each appliance (fan, mower, fridge, washer, oven) dashes between counters when you look away. Reward: a voucher the Sluiceworks Rotom can use to change form at the Arcade. | EXPCANDYM x2; +3 pts | Teaches Rotom forms before the Sluiceworks Rotom | designed |
| **Ten Years of Light** `ZE_LOWLIGHT_LAMPS` | 6 | `switch(114)` | a Lowlight lamp-tender · the Lowlight (Shattered) (608) | ★★ · 28 | After the Shatter, someone has been lighting small lamps at the feet of the glassed people. Nobody admits to it. **Twist:** It's Dex's Pichu, who escaped the Shatter and has been carrying spark-lamps to every glassed figure, starting with his. If you sit by the shrine it comes to you. No battle; it chooses you. It knows Volt Tackle. | Pichu "Spark" Lv 25 (LIGHTNINGROD); +3 pts | Dex shrine (S164); Homecoming foreshadowing | designed |
| **Cut Loose** `ZE_COURIER` | 12 | `badges >= 10` | a pilot at the anchor-smithy · Anchorhold (730) | ★★★ · 52 | Deliver a sealed key-ring to an airship before the embargo inspectors board. The key-ring jingles by itself. **Twist:** The key-ring is a Klefki carrying the airship's ignition keys. Give it up and Meridian thanks you; hide it in your bag and the ship cuts loose, and the Klefki, having nobody left to hold keys for, holds yours. | Klefki Lv 50 (PRANKSTER); +4 pts | Meridian standing (handing it to the inspectors) vs the smugglers (WORLD 'Cut Loose') | designed |
| **Return to Sender** `ZE_RETURN_TO_SENDER` | 16 | `badges >= 14` | Postmaster Halloran · Gale Post Hall, Skyreach (325) | ★ · 68 | CALL FOR PROPOSALS #0412: DEAD LETTERS, THREE (3). DELIVER BY HAND. PRIZE: ONE (1) DRAWER, CLEARED. | PIDGEOTITE, ELECTRIUMZ; +2 pts |  | wired |
| **The Laureate's Prize** `ZE_LAUREATE` | 16 | `badges >= 14` | Registrar Odalys Venn · the Prize Exchange, Lumen City (194) | ★★★★★ · 72 | The Exchange's highest prize: enter a machine of your own design in the Cogsworth Invention Bout. Your machine is your team. **Twist:** Rounds: Steel-only, no items, and Factory-to-Scrapyard mid-battle. The Registrar admits the prize was always rigged for Meridian entrants and that you won anyway. | ABILITYPATCH; +5 pts | Magnus / Meridian politics (MAGNUS_KEPT_FAITH flavour) | designed |

### The Gutter Book — Nadir

| Quest | Ch | Unlock | Giver · where (map) | Rank · Rec Lv | What happens | Reward | Touches | Status |
|---|---|---|---|---|---|---|---|---|
| **Lamps Out** `NA_OCTAVE_LAMPS_OUT` | 7 | `badges >= 5` | Six-Fingers Ottoline (chalk job) / the marsh ferryman · the ferry steps on the runoff marsh, Mirefen (at night) (220) | ★ · 34 | Chalk job: someone keeps putting out the night-ferry lamps on the marsh. The ferrymen pay a cut to whoever stops it. | $1000, DUSKBALL x5; truth: $1000; covered: HOLLOW+1; +3 pts | The Octave: Noct (5 of 8 in gym order); the Gutter Book takes its cut either way | wired |
| **Clean Water** `NA_CLEAN_WATER` | 7 | `badges >= 5` | a char-burner · Charwell (630) | ★ · 32 | Ossarian bone-char filters clean Nadir's poison. Someone is skimming the filter carts. Find who, then decide who you tell. **Twist:** The skimmer is a sump-folk grandmother selling filters to families the cart route skips. Tell Meridian (MERIDIAN+1), tell the Hollow (HOLLOW+1), or reroute the carts yourself (a puzzle on the canal locks; Harmony). | $3000; +3 pts | Hollow vs Meridian standing (WORLD 'Clean Water') | designed |
| **A Five Out of Ten** `NA_NOODLE_SCORE` | 7 | `badges >= 5` | the noodle-cart cook · Mirefen (220) | ★ · 32 | Mirefen's noodle cart rates its customers out of ten. Nobody has scored above a four. Corvin has a two and comes daily. **Twist:** The score isn't about manners: it's about whether you notice the cook's Alolan Grimer cleaning the pots. Thank the Grimer and you get a five (the first ever). The cook, overcome, gives you one of its babies. Corvin demands a recount. | Alolan Grimer Lv 30 (POISONTOUCH); +2 pts | 15_COMEDY Nadir bit; Corvin (Ch7) | designed |
| **Sewer Royalty** `NA_VENAM` | 7 | `badges >= 6 && switch(118)` | Six-Fingers Ottoline · the Miasma Caverns under Mirefen (644) | ★★ · 38 | Somebody has crowned herself queen of the Miasma Caverns. Ottoline wants to know who's charging tolls on her sumps. **Twist:** Board pointer for the Venam cameo; her event completes the quest. | BLACKSLUDGE; +3 pts | CAMEOS.md #2 'Sewer Royalty' (FESTIVAL_VENAM) | designed |
| **Pit Ringer** `NA_PIT_RINGER` | 9 | `badges >= 7` | the Iron Pit announcer · the Iron Pit, Ironreach (263) | ★★ · 41 | An unlicensed pit in the old mine shafts: six fights, no breaks, and the house brings a brass formation for the last one. **Twist:** Gauntlet on :COLOSSEUM with crowd-mood effects; the last bout is a boss Falinks whose break summons the rest of the troop. Win and the troop's runt follows you out. | Falinks Lv 38 (DEFIANT); +4 pts | Kaito / Ironreach Open foreshadowing; the announcer narrates everything (15_COMEDY) | designed |
| **Lamplighter Kids** `NA_LAMPLIGHTER_KIDS` | 9 | `badges >= 7` | Pip's friend from the lamp-runners · Ironreach (260) | ★★ · 40 | Three lamp-runner children went into the old sumps after a rumour of treasure. Their lamps are running out. **Twist:** Darkness puzzle: each found child carries a lamp that lights a radius; you choose the route by which shafts their lamps can reach. The 'treasure' is a Sableye's gem hoard, which the Sableye would like back. | EXPCANDYM x3; +3 pts | none | designed |
| **Two Lucarios** `NA_GARRET` | 9 | `switch(123)` | Six-Fingers Ottoline · Ironreach's lower shafts (263) | ★★★ · 46 | A foreign trainer is asking every pit-fighter in Ironreach the same question about his Lucario. **Twist:** Board pointer for the Garret cameo; his event completes the quest. | BLACKBELT; +3 pts | CAMEOS.md #3 'Two Lucarios' (FESTIVAL_GARRET) | designed |
| **The Lift Strike** `NA_LIFT_STRIKE` | 16 | `badges >= 14` | the lift-workers' union · Midstair (830) | ★★★ · 70 | The cable-lift workers have stopped every lift between Zenith and Nadir. The Directorate wants them moving by morning. **Twist:** A vertical map of stalled lift cages; you climb between them. The Directorate officer is a MERIDIAN_DIRECTORATE battle if you side with the union. | $6000; +4 pts | Meridian vs Hollow standing; Mandate (S115) state | designed |
| **Dogs of the Moon Market** `NA_MOON_MARKET_DOGS` | 17 | `badges >= 15` | Six-Fingers Ottoline · the Moon Market, Underveil (423) | ★ · 74 | CHALK: BARONS' KENNEL. THREE CAGES. NOBODY SAW NOTHING. | HOUNDOOMINITE, DARKINIUMZ; +3 pts |  | wired |
| **Mother Gutter's Ledger** `NA_GUTTER_DEBTS` | 17 | `badges >= 15` | Mother Gutter · the Moon Market, Underveil (423) | ★★★ · 72 | Collect five debts for the oldest sump-baron in Nadir. Or don't collect them. She'll know either way. **Twist:** Each debtor has a reason (a sick Pokemon, a Mandate fine, a lie). You can pay one debt yourself, forgive one, fight one. Mother Gutter rewards whatever you did, as long as you did it on purpose. Her Muk is the size of a cart and attends the meeting. | $8000; +4 pts | Nadir independence arc (S149); Nyx bond flavour | designed |
| **Sweetrot** `NA_SWEETROT` | 18 | `switch(150)` | a Sweetrot vendor · the Moon Market, Underveil (423) | ★★★★ · 76 | The Sweetrot vendors woke from Pecharunt's spell craving tea. Terrible tea. One cup in particular. **Twist:** The only tea bitter enough is Larch's kelp tea. Bring a cup (mailed from Tidewatch at your request, with a furious note). A Poltchageist climbs into the cup and refuses to leave. | Poltchageist Lv 72 (HOSPITALITY); +4 pts | Running gag 1 (Larch's kelp tea) | designed |
| **The Memory Kata** `NA_MEMORY_KATA` | 19 | `badges >= 17` | Six-Fingers Ottoline · the Last Rung, Ironreach (260) | ★★ · 82 | CHALK: PAWN SHELF, TOP ROW. A WARDGUARD STONE. THE OWNER WANTS IT GONE TO SOMEONE WHO'LL USE IT. | LUCARIONITE, FIGHTINIUMZ; +4 pts |  | wired |
| **Bedside Manner** `NA_BEDSIDE_MANNER` | 21 | `badges >= 18` | Wenlow · Corvin Mott's Infirmary, Mirefen (223) | ★ · 86 | CHALK: INFIRMARY NEEDS VISITORS. NOT DOCTORS. JUST VISITORS. - W. | AUDINITE; +2 pts |  | wired |

### The Trial by Flames — Ashkaar

| Quest | Ch | Unlock | Giver · where (map) | Rank · Rec Lv | What happens | Reward | Touches | Status |
|---|---|---|---|---|---|---|---|---|
| **The Little Crucible** `AS_LITTLE_CRUCIBLE` | 4 | `badges >= 2` | Sergeant Brakka Emberhide · the Legion recruiting barge, Saltmere harbour (146) | ★ · 21 | WRIT OF FLAME: three bouts, back to back, no healing. Then the barge's mascot. Win and the Legion respects you. Lose and the Legion respects you less. | $1200, QUICKCLAW; +3 pts | Ashkaar flavour: honesty is law; signing up (flag :recruited) changes how later Legion NPCs greet you | wired |
| **Too Loud for the Choir** `AS_OCTAVE_TOO_LOUD` | 8 | `badges >= 6` | Forte of the Octave · the Crucible on the caldera rim, Cindervault (240) | ★ · 38 | Writ of Flame: a Choir singer wants a Writ. The Crucible will hear her if she brings a second. | $2000, HEATROCK; +3 pts | The Octave: Forte (6 of 8 in gym order); Ashkaar honesty (she must say who she is) | wired |
| **Seven Bouts** `AS_SEVEN_BOUTS` | 8 | `badges >= 6` | Legate Varra Kosk · the Crucible, Cindervault (240) | ★ · 38 | The Crucible's entry rite: seven legion fighters, back to back, on the caldera floor. No items. No healing. No complaining. **Twist:** Volcanic field; each bout raises the field's heat stage. Bout 4 is a double. Bout 7 is the Legate's adjutant on a Dragon's Den preview. The Herald introduces you with whatever the Saltmere barge called you. | CHARCOAL, FIRESTONE; +4 pts | Ashkaar recruitment flag from the Saltmere barge is honoured here (skip bout 1) | designed |
| **The Lava-Tube Terror** `AS_DRUDDIGON` | 8 | `badges >= 6` | a Hearthguild smith · The Cinderhorn (664) | ★★ · 40 | A Druddigon has made the Cinderhorn lava tubes its own. Three smiths' Pokemon came back scorched. The Legion wants it beaten, not killed. **Twist:** Boss Druddigon (Rough Skin, 2 bars) on :VOLCANIC; it joins after. Back at the Crucible the Herald asks how it went. Exaggerate (Isenmar-style) and you're fined for lying. | Druddigon Lv 37 (ROUGHSKIN); +4 pts | Honesty law: report how the fight really went (lying costs the reward) | designed |
| **Adequate Swords** `AS_ADEQUATE_SWORDS` | 8 | `badges >= 6` | the owner of ADEQUATE SWORDS · Cindervault market (240) | ★ · 38 | A rival shop has opened across the street: EXCELLENT SWORDS. The owner of ADEQUATE SWORDS suspects a lie. Lying is a crime. **Twist:** You test the swords (a battle against the rival smith's Honedge on a 'sharpness' rule). The swords are excellent. ADEQUATE SWORDS loses the case, renames itself ADEQUATE SWORDS (STILL), and is happier. | METALCOAT; +2 pts | 15_COMEDY Ashkaar honest-signs bit | designed |
| **Afraid of Heights** `AS_AFRAID_OF_HEIGHTS` | 8 | `badges >= 6` | Recruit Tamm · the Dragon Roosts, Cindervault (248) | ★★ · 40 | A dragon-rider recruit is afraid of heights and has been assigned a Trapinch 'until he's ready'. He has been not-ready for two years. **Twist:** Three training battles with Tamm's Trapinch in your party as a guest. When it becomes a Vibrava it takes Tamm three feet off the ground and he screams with joy. He gives you the Noibat he was also assigned, because 'it looks at me like it knows'. | Noibat Lv 36 (INFILTRATOR); +3 pts | 15_COMEDY Ashkaar bit | designed |
| **Ashes Home** `AS_ASHES` | 8 | `badges >= 6` | the Legion quartermaster · Scaldwater (650) | ★★ · 37 | A Nadir-born legionnaire died at the caldera. His Houndour won't leave his urn. Somebody has to carry both of them home to Scaldwater. **Twist:** No battles unless you take the short road (Legion deserters who want the urn's silver). At the door the mother takes the urn and tells the Houndour to go and keep marching, with someone who will come back. | Houndour Lv 34 (FLASHFIRE); +4 pts | War arc: Ashkaar recruiting Nadir youths (WORLD border E); Harmony | designed |
| **The Trial of Truth** `AS_TRIAL_OF_TRUTH` | 8 | `badges >= 6 && switch(120)` | Herald Pyke · the Hall of Oaths, Cindervault (247) | ★★★ · 41 | Ashkaar judges a lie by combat. A Hearthguild officer swears the caldera crisis wasn't the Legion's fault. You were there. **Twist:** Whatever you say is a choice with consequences; contradicting the officer starts an ASHKAAR_OFFICER duel on :VOLCANIC under 'oath rules' (if you switch, you concede). Win and the Legion admits fault publicly, which nobody in the hall has seen before. | FLAMEORB; +4 pts | Caldera result (V110) and Brann's bond flavour; Ashkaar war politics (S121) | designed |
| **The Egg Run** `AS_EGG_RUN` | 9 | `badges >= 7` | the Roost-mistress · the Dragon Roosts, Cindervault (248) | ★★★ · 42 | Carry a warm dragon egg across the Cinderhorn to the far roost. Egg-hunters know the route. The egg must not get cold. **Twist:** A warmth meter (steps since the last vent) instead of a timer; egg-hunter ambushes (trainer battles) at the vents. At the far roost the egg hatches early in your hands. It decides you're its roost. | Axew Lv 1; +4 pts | none; earliest Axew (wild only from Badge 17) | designed |
| **The Forge Remembers** `AS_FORGE_REMEMBERS` | 17 | `badges >= 15 && quest_done(:OS_RING_DAY); after OS_RING_DAY` | Brann Holloway · the Hearthguild Hall, Cindervault (after the Ring) (244) | ★ ·  | Brann found something in the slag. | CAMERUPTITE; +0 pts |  | wired |
| **Old Cinder** `AS_OLD_CINDER` | 17 | `badges >= 15` | Roost-keeper Tarn · Pyre Keep, the Dragon Roosts (248) | ★ · 72 | WRIT: The war-Charizard Old Cinder will not leave the high roost. Its rider fell at the front. Bring it down, honourably. | CHARIZARDITEX, DRAGONIUMZ; +3 pts |  | wired |
| **The Brazier Writ** `AS_BRAZIER_WRIT` | 17 | `badges >= 15` | Legate Varra Kosk · the Crucible, Cindervault (240) | ★★ · 75 | WRIT OF THE BRAZIER: the Crucible keeps one heartstone for one who earns it without being born to a dragon. | SALAMENCITE, FIRIUMZ; +4 pts |  | wired |
| **Dragonsworn** `AS_DRAGONSWORN` | 19 | `badges >= 17` | Legate Varra Kosk · the Wyrmrest proving ground (460) | ★★★★★ · 83 | The highest brand in Ashkaar. Stand in the Dragon's Den and fight the Legate's own dragon while the legions watch. **Twist:** ASHKAAR_OFFICER Legate team ending in a boss Haxorus. Afterwards you're offered the Dragonsworn oath (to the Dominar). Refusing is also honoured: 'Strength that won't kneel. Good.' | LIFEORB; +5 pts | DOMINAR_SWAYED flavour; Sigrun bond (she watches) | designed |

### The Rolls of Unearthing — Ossaria

| Quest | Ch | Unlock | Giver · where (map) | Rank · Rec Lv | What happens | Reward | Touches | Status |
|---|---|---|---|---|---|---|---|---|
| **The Noon Bell** `OS_OCTAVE_NOON_BELL` | 6 | `badges >= 4` | Sona of the Octave · the Temple of the Noon Sun, outside Duneholt (new map, off Sunbleach Flats 613) (215) | ★ · 30 | Clay tablet: the old sun temple's light-shaft has filled with sand. Its keeper needs diggers. Its keeper says she knew you'd read this. | $1500, SUNSTONE; +3 pts | The Octave: Sona (4 of 8 in gym order) | wired |
| **Kevin** `OS_KEVIN` | 6 | `badges >= 4` | the Dig Lab interns · the Dig Lab, Duneholt (209) | ★ · 29 | The interns revived a fossil they can't identify. They call it Kevin. Kevin is a rock. Kevin is in the staff photo. **Twist:** Three tests (light, sound, being talked to kindly) over three visits. On the third Kevin turns out to be a Carbink that was asleep, and it has been listening to the interns' gossip for a month. It knows everything. | Carbink "Kevin" Lv 28 (STURDY); +2 pts | 15_COMEDY Ossaria bit | designed |
| **The Riddle Trader** `OS_RIDDLE_CARAVAN` | 6 | `badges >= 4` | a caravan trader · Copperdune caravanserai (610) | ★ · 27 | A caravan trader only barters in riddles. She doesn't know the answers either. She wants you to find them. **Twist:** The riddles have real answers hidden in Copperdune (a buried locomotive, a mural, a Sandile who only comes out at noon). When you give her the third answer she says 'Oh! I always thought it was a goat,' and pays you in a Trapinch. | Trapinch Lv 27 (SHEERFORCE); +2 pts | 15_COMEDY Ossaria bit | designed |
| **Tomb Freight** `OS_TOMB_FREIGHT` | 6 | `badges >= 4` | the freight-depot foreman · Copperdune (610) | ★★ · 30 | A locked railway car bound for Lumen is heavier than its manifest. Meridian says machine parts. The tomb-guild says grave goods. **Twist:** Stealth into the depot at night; the car holds an Elector's sarcophagus with an Unown inscription that names the Prismfall. | $3500; +3 pts | Meridian vs Ossarian Electors (WORLD 'Tomb Freight'); Prince-Elector Kassan | designed |
| **The Mural Gallery's Missing Letter** `OS_UNOWN_MURALS` | 6 | `switch(116)` | Curator-Elect Nasrin Vael · the Mural Gallery, Duneholt (207) | ★★ · 30 | One Unown is missing from the gallery's great inscription, and the sentence is wrong without it. **Twist:** Catch the Unown form the sentence needs (the inscription tells you which by grammar). The corrected sentence reads differently from the one Sahar teaches: 'nineteen fell'. | TM28; +3 pts | Lore (Prismfall, Legend Plate seed) | designed |
| **Something in the Sinkholes** `OS_SINKFIELD` | 7 | `badges >= 5` | a Sinkwells water-carrier · Sinkfield (628) | ★★ · 31 | Something flat and grinning is dragging water-carriers' Pokemon into the Sinkfield sinkholes. **Twist:** Boss Galarian Stunfisk (trap-jaw) on :DESERT/:BLEED that hides in random sinkholes between turns of a little overworld puzzle; beaten, it gives back the carriers' Pokemon and joins. | Galarian Stunfisk Lv 31 (MIMICRY); +4 pts | Bleed zone; Imprinted variant | designed |
| **The Ring-Day** `OS_RING_DAY` | 14 | `badges >= 13 && !mega_ring` | Bastian Ore · Bastian's lamp-room, the lowest of the Cragholm Lift Galleries (after Gym 13) (363) | ★ ·  | Bastian wants you in his lamp-room. | MEGARING, AGGRONITE; +0 pts | Gives the Mega Ring (Mega Evolution and, SPINE Rev 23, Z-moves open) and the Aggronite. Foreshadows the PC's splinter: the ring sings. | wired |
| **Amber, Again** `OS_AMBER_AGAIN` | 14 | `badges >= 12` | Sahar Ostrand · Sahar's Dig Lab, Duneholt (209) | ★ · 60 | TABLET: The Old Amber held two things. The Warden kept one. Bring her the other, alive. | AERODACTYLITE; +2 pts |  | wired |
| **The Unquiet Elector** `OS_UNQUIET_ELECTOR` | 14 | `badges >= 12` | an embalmer of Vigil · Vigil (770) | ★★★ · 62 | A dead Elector keeps walking out of his tomb-mirror to vote. The Veiled Synod says the dead are theirs. Vigil says the dead are Vigil's. **Twist:** A mirror-mystery across the Obsidian Barrows; the Elector never got to cast the vote that would have stopped the Prince-Elector's grandfather. You stage it. He votes, and rests. His Galarian Yamask stays with you. | Galarian Yamask Lv 60 (WANDERINGSPIRIT); +4 pts | Tomb-law vs the Synod (WORLD 'The Unquiet Elector'); Antumbra joint points | designed |
| **Where the Well Went** `OS_UNDERSANDS` | 14 | `badges >= 12 && switch(137)` | Sahar's foreman · the Duneholt Undersands (783) | ★★★★ · 62 | Duneholt's well is dry. The diggers think the water went down. They want someone to follow it. **Twist:** Strength-boulder escort through collapsing galleries; the crew can fall behind. At the bottom: warm stone breathing like something asleep. | TELLURICSEED x2, EXPCANDYL x2; +4 pts | Groudon arc prelude (S140); V109 DUNEHOLT_WELL | designed |
| **The Bonewright's Rite** `OS_BONEWRIGHT` | 14 | `badges >= 13` | Curator-Elect Nasrin Vael · Cragholm (360) | ★★★★★ · 64 | Reassemble a whole fossil skeleton from the pieces the Rolls have collected across Ossaria, in the right order, in front of the Curators. **Twist:** A drag-and-place puzzle; wrong orders produce a creature that the Curators politely call 'Kevin II'. | ABILITYCAPSULE; +5 pts | Cragholm fossil revival (POKEMON_AVAILABILITY §2) | designed |
| **The Tyrant's Heart** `OS_TYRANT_HEART` | 17 | `badges >= 15` | Curator-Elect Nasrin Vael · the Cragholm lift-house rack; the dig is on the Vertebrae (360) | ★★ · 75 | TABLET: A tyrant's heart lies in the third vertebra. Dig it out whole. | TYRANITARITE, GROUNDIUMZ; +4 pts |  | wired |

### The Rite of Reflection — Antumbra

| Quest | Ch | Unlock | Giver · where (map) | Rank · Rec Lv | What happens | Reward | Touches | Status |
|---|---|---|---|---|---|---|---|---|
| **The Still Water** `AN_OCTAVE_STILL_WATER` | 13 | `badges >= 11` | Lento of the Octave (the Rite, read at Glassmere) · the frozen Mirror Mere, past Glassmere (753) (742) | ★ · 58 | Mirror-writing in the reading-pool: the Mirror Mere froze in summer. Its singer won't leave the ice. Her reflection is under it. | $4000, MIRRORHERB; +4 pts | The Octave: Lento (7 of 8 in gym order); the Rite of Reflection | wired |
| **Your Other Half** `AN_OTHER_HALF` | 13 | `badges >= 11` | a Glassmere fisherwoman · Glassmere (753) | ★ · 56 | Her husband came back from the Mere reversed: left-handed, kinder, and worse at fishing. She'd like the old one back. Probably. **Twist:** Swap through the Mere twice; the reflection doesn't want to go back. The fisherwoman chooses (you can influence it). The couple's Indeedee also came back reversed, and stays with you. | Indeedee Lv 55 (PSYCHICSURGE); +3 pts | WORLD 'Your Other Half'; mirror gag (running gag 8) | designed |
| **It Keeps the Rain In** `AN_UMBRELLA` | 13 | `badges >= 11` | a man with an umbrella · the Antumbra Threshold (743) | ★ · 55 | His umbrella keeps the rain in. He'd like it to keep the rain out. He's tried holding it the other way up. That keeps the rain up. **Twist:** The answer is to open it indoors (which is outdoors here). The tiny storm inside it was a Hatenna that hates noise and was hiding from the Threshold's echoes; it comes with you. | Hatenna Lv 54 (MAGICBOUNCE); +2 pts | 15_COMEDY Antumbra bit | designed |
| **Better Marks** `AN_STUDENT` | 13 | `badges >= 11` | a Lucent student · the Athenaeum, Lucent (344) | ★★ · 58 | Her reflection has been attending lectures for her. It gets better marks. She is furious and wants to sit the final herself. **Twist:** Battle the REFLECTION trainer type (her team, mirrored). She passes with a lower mark than her reflection got, and is prouder of it. | TWISTEDSPOON; +3 pts | 15_COMEDY Antumbra bit | designed |
| **The Echo That Answers First** `AN_ECHO_HALL` | 13 | `badges >= 12` | Lector Saffi Ivarne · the Speculum, Lucent (346) | ★★★ · 60 | An echo in the Speculum answers questions before they're asked. The Lectors would like to ask it one. **Twist:** A reverse-dialogue puzzle: answers come first and you assemble the question from them. | TM48; +4 pts | Mindscape lore; Ilsa (Ch13) foreshadowing | designed |
| **Shadows Fall Upward** `AN_SHADOWS_UP` | 13 | `badges >= 12` | a Vigil medium · the Obsidian Barrows (760) | ★★★ · 60 | In the Barrows, shadows fall upward. Somebody's shadow has fallen all the way up and got stuck on the inverted desert in the sky. **Twist:** Light-source puzzle on the Inverse field: move lamps so the stuck shadow is cast back down onto the sand. | ELEMENTALSEED x2; +4 pts | Antumbra / Ossaria borderland I | designed |
| **The Smile Behind the Glass** `AN_SMILE_BEHIND_GLASS` | 15 | `badges >= 13` | Lector Saffi Ivarne · the Speculum, Lucent (346) | ★★ · 64 | MIRROR-WRITING: Somebody's reflection in the Speculum is smiling with too many teeth. | MAWILITE; +3 pts |  | wired |
| **Nine Hundred and Ninety-Nine** `AN_GIMMIGHOUL_COINS` | 15 | `badges >= 13` | a lantern-priest · Gravenmoor (380) | ★★ · 64 | Gimmighoul coins keep turning up in the Gravenmoor collection plates. The priests want to know where they're coming from. **Twist:** Wraps the existing Gimmighoul coins hunt in a Trial quest; the chest is a Gimmighoul who has been tithing. | RELICGOLD; +3 pts | POKEMON_AVAILABILITY §3 Gimmighoul hunt | designed |
| **Behind the Glass** `AN_BEHIND_THE_GLASS` | 15 | `badges >= 14 && switch(143)` | Archseer Dask's reflection · the Palace of Glass, Lucent (347) | ★★★★★ · 70 | Antumbra's last rite: spend one night as your own reflection. **Twist:** A short playable stretch as the PC's reflection, which sees everything the PC did and has opinions. No joke after this one is safe in a mirror. | ABILITYPATCH; +5 pts | Mirror gag payoff (running gag 8); Ruin Route seed | designed |
| **Dreamwalker** `AN_SHIV` | 18 | `badges >= 17` | Lector Saffi Ivarne · the dusk-chapels of Gloaming (440) | ★★★★ · 82 | A stranger has been walking through other people's dreams in Gloaming and leaving them better rested. The Lectors want a word. **Twist:** Board pointer for the Shiv cameo; her event completes the quest. | MAGICALSEED; +3 pts | CAMEOS.md #7 'Dreamwalker' (FESTIVAL_SHIV) | designed |

### The Hall of Petitions — Crownhaven

| Quest | Ch | Unlock | Giver · where (map) | Rank · Rec Lv | What happens | Reward | Touches | Status |
|---|---|---|---|---|---|---|---|---|
| **The Eevee Octave** `CR_OCTAVE` | 2 | `` | Vesper Lindqvist · backstage at the Lantern Theatre, Saltmere (asked); the Glassfall Memorial Garden, Crownhaven (489) (145) | ★ · 90 | Vesper asked you to look in on the eight singers of the Octave as your road takes you through the kingdoms. | EEVIUMZ, Eevee Lv 70 (ADAPTABILITY); +5 pts | The gauntlet runs in the order you helped the singers (each Eeveelution uses its Z-move); S177 EEVEE_OCTAVE_DONE | wired |
| **The Ninth Verse** `CR_OCTAVE_NINTH_VERSE` | 20 | `switch(155) && octave_helped >= 7` | Carol of the Octave · the Glassfall Memorial Garden, Crownhaven (489) | ★ · 88 | Petition, sealed in eight waxes: a singer is writing the Octave's Festival song and needs someone who has met them all. | $6000, PPUP x3; +4 pts | The Octave: Carol (always 8 of 8); she sends for Vesper | wired |
| **Eighteen Shrines** `CR_EIGHTEEN_SHRINES` | 20 | `badges >= 18` | the Pilgrim's Rest keeper · Pilgrim's Rest (890) | ★ · 85 | Eighteen roadside shrines on the Pilgrim Pass, one per Plate. Ashkaar charges a toll at six of them. **Twist:** Each shrine asks one line of the counting rhyme; the eighteenth asks for the line nobody sings ('...and one that no one counted'). The keeper gives you the five Imprint stones the shrines kept (the Octave's Eevee, SPINE Rev 19, replaced the old 'Prism' Eevee here). | FIRESTONE, WATERSTONE, THUNDERSTONE, LEAFSTONE, ICESTONE; +4 pts | Ashkaar tolls (pay, fight or talk); WORLD 'Eighteen Shrines' | designed |
| **Lost Property** `CR_LOST_PROPERTY` | 20 | `switch(155)` | the lost-property clerk · the Court of Eight Pavilions (499) | ★ · 88 | The Festival lost-property tent has one item. Every day. It's an eel receipt. **Twist:** It's Kestrel's, from Ebbmouth, from Chapter 4. He has been carrying it for sixteen chapters. He denies it until you show him the date. Then he takes it back very carefully. | RARECANDY x2; +2 pts | Kestrel bond (+1); 15_COMEDY Crownhaven bit; Ebbmouth's 'THE BOY (4 EELS, DAILY)' | designed |
| **The Pavilion Line** `CR_DELEGATION_DISPUTE` | 20 | `switch(155)` | Clerk-Superior Amadeus Fenwright · the Court of Eight Pavilions (499) | ★★ · 88 | Ashkaar's pavilion is four inches over the line into Isenmar's. Neither delegation will speak to the other. Both will speak to you. **Twist:** Every message gets ruder in translation. The fix is to move the line, not the pavilion; Fenwright is appalled and then promoted. | PPMAX; +3 pts | War outcome flavour (war_terms); Dominar / Thane | designed |
| **Invitations to the Masque** `CR_MASQUE_INVITES` | 20 | `switch(156)` | the Basilica steward · the Basilica Close (483) | ★★ · 88 | Deliver eight invitations to the Night of Masques. One recipient doesn't exist. One is dead. One is you. **Twist:** A social route through the capital meeting every delegation; the dead recipient is Morwen Vane, and Kestrel sees you holding it. | RARECANDY x2; +3 pts | Night of Masques (S157) staging | designed |
| **The Chancellor's Other Ledger** `CR_HOLLIS_LEDGER` | 20 | `switch(155)` | an anonymous petition · the Accord Palace (486) | ★★★ · 90 | An unsigned petition, sealed with all eighteen kingdom seals: Chancellor Hollis keeps a second ledger. **Twist:** Palace stealth during a reception; the petition was written by Clerk Fenwright, who has been waiting thirty years for someone to answer it. | $12000; +4 pts | Hollis's arrest in the epilogue; ACCORD / MERIDIAN standing | designed |
| **An Old Man's Errand** `CR_VALENS_ERRAND` | 20 | `switch(158)` | Valen Corrigan · the Memorial Garden (489) | ★★★ · 90 | Valen asks you, not as Sovereign, to fetch something from the Memorial Garden that he can't bend down to pick up any more. **Twist:** The stone is the AF 290 marker; the name on it is the PC's mother's. He doesn't explain. He says thank you twice. | PPMAX, VALEN+2; +4 pts | Valen bond (+2) before the Final | designed |
| **Hand of the Accord** `CR_ACCORD_CHAMPIONS` | 21 | `switch(160)` | Clerk-Superior Amadeus Fenwright · the Hall of Petitions (496) | ★★★★★ · 95 | Answer one petition from every kingdom in a single day. Each is a battle. Each Warden who still speaks to you sends one. **Twist:** Requires rank 4+ in at least five Trials. The gauntlet's order is the eight Trials' halls; between bouts, each Trial's keeper says one line about what you did in their kingdom. | MASTERBALL; +5 pts | Postgame Warden's Gauntlet (S160); every Trial's rank 5 counts | designed |
| **The Meteor Champion** `CR_LIN` | 22 | `switch(160)` | a petition in a hand nobody recognises · Ferrow Lighthouse (105) | ★★★★ · 100 | A petition arrives from nowhere: 'Come back to where you landed.' **Twist:** Board pointer for the Lin postgame cameo; her event completes the quest. | ABILITYPATCH; +5 pts | CAMEOS.md #8 (FESTIVAL_LIN superboss) | designed |

## Part 2. Full scripts of the wired quests (Chapters 1–4, and the Eevee Octave across the game)

Conventions: *italics* = narration box; **Name** _(expression)_ = a character line (`pf_say`: the face beside the box for the story cast with portrait art, else a name label); _(expression, bubble)_ = the rare speech-bubble beat;
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

**Reward:** spooked: $300; spared: MIRACLESEED, RES+1; +2 pts. **Touches:** Resonance (Harmony +1 if you leave it be); the Sudowoodo can be caught after Badge 2.

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
      - on won:
        - *The Sudowoodo bolts into the plum rows, sobbing dry tears. It was far too frightened to stay in a ball.*
        - **Coll** _(deadpan)_: ...It was a Sudowoodo.
        - **Coll** _(neutral)_: It'll be back. It always comes back to the plums. Come and try again when you've a couple of badges and it's calmed down.
        - [quest complete: spooked]
      - on lost:
        - *The Sudowoodo stops attacking and goes back to being a tree, looking smug.*
  - > Leave it be.
    - *You put the bottle away. The scarecrow relaxes so hard that a leaf falls off.*
    - *The Rookidee stay out of the orchard all afternoon.*
    - **Coll** _(neutral)_: ...Leaving it, are you. All right. It's a better scarecrow than a scarecrow, I'll give it that.
    - [quest complete: spared]

**Scene `rematch`** (event: `pf_quest_run(:EL_SCARECROW, :rematch)`)

- *The Sudowoodo is guarding the plum rows. It has stopped shaking. It eyes your badge case, then your Squirt Bottle.*
- **CHOICE:** Challenge it?
  - > Challenge it.
    - [battle] Sudowoodo Lv 20 (ROCKHEAD)
      - on caught:
        - **Coll** _(neutral)_: Taking the scarecrow, then. Fair enough. I'll build a real one. Probably.
      - on won:
        - *The Sudowoodo retreats to the plums, sulking. It'll be back. It always is.*
  - > Leave it.

#### Master of Nothing (`EL_MASTER_OF_NOTHING`)

*Chapter 1 · the Dockmaster, the Dockmaster's House (map 107) · rank 1 · 2 points · unlock `switch(101) && switch(103)`*

The Dockmaster wants to close the Dovetail's ledger properly. Something is still aboard.

**Quest log steps:** `ask`: Search the laid-up Dovetail for whatever is still living aboard. · `ledger`: Tell the Dockmaster what you found.

**Reward:** POTION x2; +2 pts. **Touches:** none (a quiet one); the Wattrel joins you in Ebbmouth after Badge 3.

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
- *The Wattrel looks at the empty sea, then at you. It crackles, once, and tucks its head back under its wing. It's waiting for a ship. Any ship.*
- [quest step: ledger]

**Scene `ledger`** (event: `pf_quest_run(:EL_MASTER_OF_NOTHING, :ledger)`)

- **Dockmaster** _(neutral)_: A Wattrel. Of course. They follow ships. That one followed the last one in and had nowhere left to follow.
- [stage] He dips his pen and writes slowly.
- **Dockmaster** _(neutral)_: 'Dovetail. Laid up. Crew discharged. One Wattrel aboard, waiting for a ship.'
- **Dockmaster** _(happy)_: There. The first ledger line I've liked in a year. The Gale Post boats still run north. It'll find one.
- [quest complete]

**Scene `homecoming`** (event: `pf_quest_run(:EL_MASTER_OF_NOTHING, :homecoming)`)

- [stage] A Wattrel is perched on the Ebbmouth harbour mast, crackling. It has a strand of tarred rope in its beak.
- *It's the Dovetail's rigging. It followed the first boat north out of Ferrow's Landing.*
- *Your badge case hums its three-note chord. The Wattrel's feathers stand up with static, and it drops onto your shoulder like it was always going to.*
- [receive Wattrel "Mast" Lv 20 (VOLTABSORB)]
- *(Somewhere in Ferrow's Landing, a ledger line just changed: 'One Wattrel, rehomed.')*

#### The Last Plank (`EL_LAST_PLANK`)

*Chapter 2 · the lantern rope (Brother Teasel's hand), the empty ferry berth (map 100) · rank 1 · 2 points · unlock `badges >= 1`*

Every morning a Timburr carries a plank down to the empty berth and nails it in. Every night the tide takes it. Teasel's note: "Help it finish."

**Quest log steps:** `ask`: Find the Timburr at the empty ferry berth at dawn. · `planks`: Carry the three loose planks from the boatyard to the berth. · `finish`: The berth is mended. Tell the Timburr.

**Reward:** POTION x2; +2 pts. **Touches:** none; a Fighting type only after Dorian's badge (Revision 16: no answer to the next Warden before the gym).

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
- [receive Timburr "Plank" Lv 13 (GUTS)]
- [quest complete]

#### The Tide-Pool Feud (`EL_TIDE_POOL_FEUD`)

*Chapter 2 · Dobbs the shell-gatherer, the shell-gatherers' steps on Lacecliff Walk (map 527) · rank 1 · 2 points · unlock `badges >= 1`*

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
    - [battle] Crabrawler Lv 14 (IRONFIST)
      - on caught:
        - [continue: victory_clob]
      - on won:
        - [continue: victory_clob]
  - > Help the Crabrawler.
    - *The Crabrawler clacks its claws, delighted. The Clobbopus turns on you!*
    - [battle] Clobbopus Lv 14 (TECHNICIAN)
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

**Reward:** +1 pts. **Touches:** none; the colours you pick decide the Smeargle's moves (Water/Ice, Ghost, Fairy or Ground coverage).

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
  - > Morning over the salt lake.
    - *Brush paints pink and gold. The new sky is the minute before the lamps go out.*
    - [continue: finish_dawn]
  - > The dunes on the way in.
    - *Brush paints ochre and sand. The new sky has a road in it, going somewhere.*
    - [continue: finish_earth]
  - > After the show.
    - *Brush paints violet and black and one small star.*
    - [continue: finish_night]

**Scene `finish_sea`** (event: `pf_quest_run(:EL_PAINT_LOFT, :finish_sea)`)

- [continue: finish]
- [receive Smeargle "Brush" Lv 14 (TECHNICIAN) (sea palette)]
- [quest complete: sea]

**Scene `finish_dawn`** (event: `pf_quest_run(:EL_PAINT_LOFT, :finish_dawn)`)

- [continue: finish]
- [receive Smeargle "Brush" Lv 14 (TECHNICIAN) (dawn palette)]
- [quest complete: dawn]

**Scene `finish_earth`** (event: `pf_quest_run(:EL_PAINT_LOFT, :finish_earth)`)

- [continue: finish]
- [receive Smeargle "Brush" Lv 14 (TECHNICIAN) (earth palette)]
- [quest complete: earth]

**Scene `finish_night`** (event: `pf_quest_run(:EL_PAINT_LOFT, :finish_night)`)

- [continue: finish]
- [receive Smeargle "Brush" Lv 14 (TECHNICIAN) (night palette)]
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
- [receive Ralts Lv 13 (TRACE)]
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

*Chapter 3 · the lantern rope (no one signed it), the sap tree on the old trail, Gossamer Wood (map 524) · rank 1 · 2 points · unlock `badges >= 2`*

Two great Bug Pokémon are fighting over the sap tree on the old trail. The trail has been blocked for a week.

**Quest log steps:** `ask`: Find the sap tree on the old trail in Gossamer Wood and end the fight.

**Reward:** HONEY x2; +2 pts. **Touches:** none; the one you help clears a shortcut (Heracross tears a silk wall, Pinsir crushes a log).

**Scene `tree`** (event: `pf_quest_run(:EL_HORN_AND_PINCER, :tree)`)

- *A Heracross and a Pinsir are locked horn-to-pincer at the foot of a weeping sap tree, shoving each other in slow circles.*
- *Both of them stop and look at you. Then at each other. Then at you.*
- **CHOICE:** Who do you stand with?
  - > Stand with the Heracross.
    - *The Heracross bows. The Pinsir's mandibles open wide.*
    - [battle] Pinsir Lv 19 (MOXIE)
      - on caught:
        - [continue: hera_helps]
      - on won:
        - *The Pinsir crashes away into the undergrowth.*
        - [continue: hera_helps]
  - > Stand with the Pinsir.
    - *The Pinsir clacks once, approving. The Heracross lowers its horn.*
    - [battle] Heracross Lv 19 (MOXIE)
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

#### The Moss Hymn (`EL_OCTAVE_MOSS`)

*Chapter 3 · Lyra of the Octave, under the Lantern House tree, Briarwick; the moss-stone in Gossamer Wood (524) (map 120) · rank 1 · 3 points · unlock `badges >= 1`*

A singer of the Octave has been singing to her Eevee for three days. It will not come down from the moss-stone in Gossamer Wood.

**Quest log steps:** `ask`: Go with Lyra to the moss-stone in Gossamer Wood. · `stone`: Lyra's Eevee won't come down from the moss-stone. Mother Aldreth says: stop singing at it. · `duel`: Moss came down a Leafeon. Lyra wants a duel so it knows it can stand on its own.

**Reward:** $800, BIGROOT; +3 pts. **Touches:** The Octave: Lyra (1 of 8 in gym order).

**Scene `offer`** (event: `pf_quest_run(:EL_OCTAVE_MOSS, :offer)`)

- [stage] A girl in Choir grey sits under the Lantern House tree with her knees up, humming the same four notes over and over.
- **Lyra** _(sad)_: Oh. Sorry. Was I humming? I'm always humming. The plants don't mind.
- **Lyra** _(neutral)_: I'm Lyra. Of the Octave. Vesper's Octave. I came home to Briarwick after the Pageant, and my Eevee, Moss, went straight up the old moss-stone in Gossamer Wood and won't come down.
- **Lyra** _(sad)_: Three days. I've sung it everything I know. Mother Aldreth says I should stop singing at it. I don't know what that means. I'm a singer.
- [if `party_has(:EEVEE)`]
  - **Lyra** _(happy)_: Is that an Eevee? Hello. Has yours decided yet? Mine is trying to.
- **CHOICE:** Go with Lyra to the moss-stone?
  - > I'll come.
    - [quest accepted]
    - [quest step: stone]
    - **Lyra** _(happy)_: Thank you. It's past the silk walls, where the moss grows on the north side of everything.
  - > Not now.
    - **Lyra** _(neutral)_: That's all right. I'll be here. Humming.

**Scene `stone`** (event: `pf_quest_run(:EL_OCTAVE_MOSS, :stone)`)

- [stage] The moss-stone: a grey boulder furred green to the top. A small brown Eevee sits on the summit with its eyes shut. Lyra is already there, mid-note.
- **Lyra** _(neutral)_: Moss. Moss, please. I'll sing the one you like.
- *The Eevee's ears flatten a little more with every note.*
- **CHOICE:** What do you do?
  - > Sing along.
    - *You join in. The Eevee curls up tighter. Lyra stops, and looks at you, and laughs at herself.*
    - **Lyra** _(sad)_: It's not working when two of us do it either.
  - > Sit down by the stone and say nothing.
    - *You sit. After a while, Lyra stops singing and sits down next to you.*
    - *The wood is very loud when nobody is singing: leaves, water somewhere, the moss creaking as it drinks.*
    - *The Eevee opens its eyes. It listens too.*
    - [stage] Moss climbs down the stone. The green on the stone is the green on its fur, then all of it: a Leafeon steps off the last ledge.
    - **Lyra** _(happy)_: Oh. Oh, look at you. You weren't stuck. You were listening.
    - **Lyra** _(neutral)_: And I was too loud to hear it. Mother Aldreth is going to be unbearable.
    - [quest step: duel]
    - [continue: duel]
  - > Tell Lyra to stop singing.
    - **Lyra** _(sad)_: Everyone keeps telling me that. Fine. Fine. I'll stop.
    - *She stops for almost three seconds, then starts humming again without noticing.*

**Scene `duel`** (event: `pf_quest_run(:EL_OCTAVE_MOSS, :duel)`)

- **Lyra** _(neutral)_: Will you duel us? Moss has never stood on its own feet in a fight. I want it to know it can.
- [trainer battle] OCTAVE_SINGER Lyra (v50)
  - on won:
    - **Lyra** _(happy)_: It stood. It stood the whole time. Thank you.
    - **Lyra** _(neutral)_: I'll write to Vesper tonight. She'll say she knew. She always knew.
    - [the Octave remembers that you helped Lyra: the gauntlet order]
    - [quest complete]
  - on lost:
    - **Lyra** _(neutral)_: Moss liked that. Come back and try again? We'll be at the Lantern House tree.

**Scene `after`** (event: `pf_quest_run(:EL_OCTAVE_MOSS, :after)`)

- **Lyra** _(happy)_: Moss sits in the Lantern House now and listens to Mother Aldreth not talking. They get on very well.

#### The Humming Lamp (`EL_LAMP_LENS`)

*Chapter 5 · Hesper Vane, the Ferrow Lighthouse lamp room (map 106) · rank 1 · 1 points · unlock `badges >= 3`*

A paper lantern from the lighthouse: 'THE LAMP HUMS. MAKE IT STOP. - H.V.'

**Quest log steps:** `ask`: Hesper's lamp hums at night. Look behind the great lens.

**Reward:** AMPHAROSITE; +1 pts. **Touches:** Kestrel's family: Morwen set the stone; it hums for the PC..

**Scene `offer`** (event: `pf_quest_run(:EL_LAMP_LENS, :offer)`)

- **Hesper** _(deadpan)_: You again. The lamp's been humming every night since you came back down the coast. Like a kettle that won't boil.
- **Hesper** _(neutral)_: My daughter set a stone in the lens when she was a girl. Lumen lamp-glass, she said. An Ampharos's heart. It never made a sound in thirty years.
- **CHOICE:** Look behind the lens?
  - > Look.
    - [quest accepted]
    - *Behind the great lens, a yellow stone sits in a brass claw. When you lean close, the hum climbs a note.*
    - **Hesper** _(shocked)_: ...It's you it's humming at.
    - **Hesper** _(deadpan)_: Take it. Take it out of my lamp before it hums me into the sea. Some Warden down the road can tell you what it's for. I won't.
    - [quest complete]
    - [if `!mega_ring`]
      - *The stone is warm, and it hums faintly in your hand... then goes quiet, as if it were waiting for something.*
    - **Hesper** _(sad)_: Morwen's ring used to make it glow. I'd forgotten that.
  - > Not now.
    - **Hesper** _(deadpan)_: Then don't stand in my light.

#### The Bride Tree's Heart (`EL_BRIDE_TREE_HEART`)

*Chapter 11 · Juno Hale, the Heartgarden, Verdance, under the Bride Tree (after J3) (map 294) · rank 1 · 0 points · unlock `badges >= 9`*

Juno is waiting under the Bride Tree.

**Quest log steps:** `ask`: Juno is under the Bride Tree.

**Reward:** VENUSAURITE; +0 pts. **Touches:** Sets up J4: the Grass Warden's ring won't answer Juno yet (it does by the Festival: her Mega Gardevoir)..

**Scene `heart`** (event: `pf_quest_run(:EL_BRIDE_TREE_HEART, :heart)`)

- **Juno** _(happy)_: You came! Sit, sit. Mind the roots, they've got opinions.
- **Juno** _(neutral)_: Uncle Rowan kept a seed-tin in the potting shed. Label says NOT SEEDS. Guess what was in it.
- *She opens her hand: a stone the green of new leaves, with a pink flower caught inside it.*
- **Juno** _(neutral)_: It grew in the Bride Tree's roots. A Venusaur's heart, the Listening Root says. Aunt Elin's been in bloom for twelve years. I suppose she had to put the extra somewhere.
- **Juno** _(sad)_: He left me his ring, too. It was in with his testament. The Grass Warden's ring. It won't answer me. I hold it and it's just... his.
- **Juno** _(happy)_: It hummed when you sat down, though. The stone, I mean. Don't look at me like that, I can hear it from here. So you take it. Somebody should.
- [script]
- [if `!mega_ring`]
  - *The stone is warm, and it hums faintly in your hand... then goes quiet, as if it were waiting for something.*
- **Juno** _(happy)_: And next time we fight, I'll have the ring talking to me. You'll see. Probably. Hopefully.

#### The Doll Who Waited (`EL_DOLL_WHO_WAITED`)

*Chapter 16 · A doll in the attic, Thistledown Manor attic (map 547) · rank 1 · 2 points · unlock `badges >= 14`*

A lantern with a child's scrawl: 'SOMETHING KNOCKS IN THE THISTLEDOWN ATTIC. IT WANTS ITS BUTTONS.'

**Quest log steps:** `ask`: Something knocks in the Thistledown Manor attic. · `buttons`: The doll's three buttons are somewhere in the manor. · `return`: You have all three buttons. Take them back to the attic.

**Reward:** BANETTITE, GHOSTIUMZ; +2 pts. **Touches:** .

**Scene `offer`** (event: `pf_quest_run(:EL_DOLL_WHO_WAITED, :offer)`)

- *In the attic dust sits a rag doll with a zipped mouth and no buttons for eyes. As you step closer, it turns its head toward you. Knock. Knock. Knock.*
- **CHOICE:** The doll waits.
  - > Find its buttons.
    - [quest accepted]
    - [quest step: buttons]
    - *The doll's head tilts. Downstairs, something small rolls across a floorboard.*
  - > Back away slowly.
    - *The doll keeps watching you all the way down the stairs.*

**Scene `button`** (event: `pf_quest_run(:EL_DOLL_WHO_WAITED, :button)`)

- *A black button, the size of a coin, still warm.*
- [if `quest_count(:SELF, :buttons) >= 3`]
  - [quest step: return]
  - *That's three. Upstairs, the knocking has stopped.*

**Scene `return`** (event: `pf_quest_run(:EL_DOLL_WHO_WAITED, :return)`)

- *You press the buttons on. The doll blinks. It looks at the attic window, at the road below, for a long time.*
- *Then it lets go of something it has held for a very long time: a grey stone drops from its stitched hands into yours.*
- *And sewn into its chest, in newer stitches than the rest: a sliver of dark glass, cold as a cellar.*
- [quest complete]
- *When you look back, it is only a doll, sitting in the sun.*

#### The Old Pincer (`EL_OLD_PINCER`)

*Chapter 14 · the Woodward, the Woodward's Hut, Gossamer Wood; the fight is in the Gossamer Heartwood (map 526) · rank 2 · 3 points · unlock `badges >= 12`*

A lantern from the Woodward: 'THE OLD PINCER HAS TAKEN THE HEARTWOOD SAP. BRING SOMEONE STRONG.'

**Quest log steps:** `ask`: The Woodward wants the Old Pincer out of the Heartwood's sap tree. · `fight`: Face the Old Pincer at the sap tree in the Gossamer Heartwood.

**Reward:** PINSIRITE; +3 pts. **Touches:** .

**Scene `offer`** (event: `pf_quest_run(:EL_OLD_PINCER, :offer)`)

- **The Woodward** _(neutral)_: There's a Pinsir in the Heartwood older than my hut. Old Pincer, we call it. This spring it took the great sap tree and nothing gets near it.
- **The Woodward** _(worried)_: The silk-moths need that sap. So does the Loomhouse. I'd ask Tamsin, but she's got half of Isenmar's refugees sleeping in the Loomhouse.
- **CHOICE:** Take on the Old Pincer?
  - > I'll go.
    - [quest accepted]
    - [quest step: fight]
    - **The Woodward** _(happy)_: Bless you. Bring a Fire type. Bring two.
  - > Not yet.
    - **The Woodward** _(neutral)_: It's not going anywhere. That's the problem.

**Scene `fight`** (event: `pf_quest_run(:EL_OLD_PINCER, :fight)`)

- *The sap tree weeps amber. Wrapped around its trunk, a Pinsir the size of a cart clacks its horns at you.*
- [battle] Pinsir "Old Pincer" Lv 62 (MOXIE)
  - on won:
    - *The Old Pincer lets go of the trunk and sits down heavily in the moss. Something drops from between its horns: a stone the brown of old bark.*
    - *It watches you pick it up, then wanders off into the Heartwood to sleep.*
    - [quest complete]
  - on lost:
    - *The Old Pincer clacks once, satisfied, and wraps itself around the tree again.*

#### Encore (`EL_ENCORE`)

*Chapter 18 · Dorian Pell, the Grand Stage, Pell Playhouse, Saltmere (map 154) · rank 1 · 2 points · unlock `badges >= 16`*

A gilt-edged lantern: 'ONE NIGHT ONLY. THE PLAYHOUSE REQUIRES A STAR. - D.P.'

**Quest log steps:** `ask`: Dorian needs a star for one last show before the Festival.

**Reward:** LOPUNNITE, NORMALIUMZ; +2 pts. **Touches:** .

**Scene `offer`** (event: `pf_quest_run(:EL_ENCORE, :offer)`)

- **Dorian** _(happy)_: Enter, stage left, our returning hero! Sixteen badges! Darling, you've been practically everywhere. Saltmere is so proud. I am so proud. I've had posters made.
- **Dorian** _(neutral)_: One last show before the Festival. My leading lady retired, and the house wants a closing number. You. A spotlight. A Pokemon. Something unforgettable.
- [quest accepted]
- **CHOICE:** Your closing number?
  - > A dance.
    - **Dorian** _(happy)_: A dance! Bold! Ancient! The audience weeps!
  - > A fight scene.
    - **Dorian** _(happy)_: Violence! The audience adores violence, it's very Ashkaari of them.
  - > Stand very still.
    - **Dorian** _(shocked)_: ...Avant-garde. Terrifying. The critics will call it 'a meditation'. Brilliant.
- *The curtain rises. The house is full. For three minutes, the whole of Saltmere forgets there is a war.*
- **Dorian** _(sad)_: Lovely. Lovely. Here. My leading lady's heartstone. Her Lopunny could kick a chandelier and land on the beat. She'd want it on a stage, not in my drawer.
- **Dorian** _(happy)_: And for the encore of the encore: a sliver of Choir glass the Pageant has worn as a prop jewel since the Glassfall. Ten years I called it paste. It was real all along. Of course it was.
- [quest complete]
- **Dorian** _(happy)_: Bow, darling. Always bow. They remember the bow.

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

#### The Drowned Note (`IS_OCTAVE_DROWNED_NOTE`)

*Chapter 4 · Aria of the Octave, the river steps, Ebbmouth; the Mill Quay wheel (167) (map 160) · rank 1 · 3 points · unlock `badges >= 2`*

A singer's Vaporeon melted into the Ebb when the river stuttered and hasn't come out. She can still hear it, sometimes.

**Quest log steps:** `listen`: Listen for Brine's note at three places on the Ebb: the river steps, the fish-market slip and the Mill Quay steps. · `wheel`: Aria thinks Brine is hiding under the Mill Quay wheel. · `duel`: Brine is back. Bersi wants a fight for the saga.

**Reward:** $1200, SHELLBELL; +3 pts. **Touches:** The Octave: Aria (2 of 8 in gym order); a verse on the Tally Mast.

**Scene `offer`** (event: `pf_quest_run(:IS_OCTAVE_DROWNED_NOTE, :offer)`)

- [stage] On the river steps a young woman in a wet Choir robe is sitting in the shallows up to her waist, singing a sea-shanty with the words wrong on purpose.
- **Aria** _(happy)_: Morning! It's lovely in. The cold's just the sea saying hello.
- **Aria** _(neutral)_: I'm Aria. Octave. My Vaporeon, Brine, melted into the river three days ago, when it did that stutter. They do that, Vaporeon. Go to water.
- **Aria** _(sad)_: It always comes back. It hasn't come back. But I can hear it. A note in the water, here and there, like it's calling from a long way down.
- **Aria** _(happy)_: You've got young ears. Will you listen with me? Bersi says if I find it he'll carve it on the Tally Mast.
- **CHOICE:** Help Aria listen for Brine?
  - > Let's listen.
    - [quest accepted]
    - **Aria** _(happy)_: Try here on the steps, at the fish-market slip, and down at the Mill Quay steps. Put your ear right to the water.
  - > Later.
    - **Aria** _(neutral)_: I'll stay in. I'm warm now. Don't tell me if I'm not.

**Scene `note`** (event: `pf_quest_run(:IS_OCTAVE_DROWNED_NOTE, :note)`)

- [stage] You kneel and put your ear to the water. Somewhere under the noise of the river, a long, low note.
- [if `quest_count(:SELF, :notes) >= 3`]
  - *The third note is lower than the others, and it comes from upstream, where the Mill Quay wheel turns.*
  - **Aria** _(happy)_: The wheel! It's hiding under the wheel. The Lattice hum is quieter there. It never liked the hum.
  - [quest step: wheel]
- [else]
  - *The note fades. It came from further up the river.*

**Scene `wheel`** (event: `pf_quest_run(:IS_OCTAVE_DROWNED_NOTE, :wheel)`)

- [stage] Under the Mill Quay wheel the water is black and slow. Aria wades in to her chest and sings one note, the same one you heard.
- **Aria** _(neutral)_: Come on, then. I know it's loud up here. I'm loud too. You like me anyway.
- [stage] The water stands up, gathers into a shape, and becomes a Vaporeon, coughing.
- **Aria** _(happy)_: Brine! You great puddle!
- [quest step: duel]
- [continue: duel]

**Scene `duel`** (event: `pf_quest_run(:IS_OCTAVE_DROWNED_NOTE, :duel)`)

- **Aria** _(happy)_: Bersi says a saga needs a fight in it or the Tally won't take it. Fight us? He'll make it sound bigger than it was.
- [trainer battle] OCTAVE_SINGER Aria (v50)
  - on won:
    - **Aria** _(happy)_: Ha! Wrong note, right song. Bersi's already carving.
    - [stage] At the Net Loft, Bersi Gullsong cuts a notch on the Tally Mast beside your name.
    - **Bersi Gullsong** _(happy)_: 'And the stranger heard the river's sorrow, and the drowned beast rose.' Something like that. I'll fix it later. I never fix it later.
    - [the Octave remembers that you helped Aria: the gauntlet order]
    - [quest complete]
  - on lost:
    - **Aria** _(happy)_: Ha! The river wins today. Come back, we'll be on the steps.

**Scene `after`** (event: `pf_quest_run(:IS_OCTAVE_DROWNED_NOTE, :after)`)

- **Aria** _(happy)_: Brine goes back in the river every morning now, and comes out every morning. That's all I wanted.

#### The Causeway Matriarch (`IS_CAUSEWAY_MATRIARCH`)

*Chapter 18 · the Matriarch, the Frostflat Causeway at low tide (map 560) · rank 1 · 3 points · unlock `badges >= 16`*

A Kangaskhan the size of a hut has taken the Frostflat Causeway.

**Quest log steps:** `ask`: Prove yourself to the Causeway Matriarch.

**Reward:** KANGASKHANITE; +3 pts. **Touches:** .

**Scene `offer`** (event: `pf_quest_run(:IS_CAUSEWAY_MATRIARCH, :offer)`)

- *On the causeway's crown, where the old cairn stands, a Kangaskhan as big as a fishing hut stands between you and the road. Behind her, half a dozen young ones are fishing.*
- *She doesn't charge. She waits, the way the Tally waits: for you to prove you're worth the road.*
- **CHOICE:** Face her?
  - > Face her.
    - [quest accepted]
    - [battle] Kangaskhan "The Matriarch" Lv 78 (SCRAPPY)
      - on won:
        - *The Matriarch snorts, and steps aside. From the stones of the cairn she digs out something she has kept warm a long time, and drops it at your feet.*
        - [quest complete]
        - *A skald would cut this into the Tally Mast. You do it yourself, in the frost on the cairn.*
      - on lost:
        - *The Matriarch pushes you, gently, all the way back down the causeway.*
  - > Wait for the tide.
    - *The young ones splash. The Matriarch doesn't move.*

### The Prize Exchange

#### Form 7-B (`ZE_FORM_7B`)

*Chapter 1 · Grant Kiosk P-3NNY, the Quarantine Customs Hall, Ferrow's Landing (map 108) · rank 1 · 2 points · unlock `switch(103)`*

CALL FOR PROPOSALS #0001: DISPOSAL OF UNCLAIMED LIVESTOCK, CRATE 7-B. BOUNTY: $500.

**Quest log steps:** `ask`: Read Crate 7-B's paperwork at the customs kiosk. · `stamps`: Form 7-C (adoption) needs three stamps: Tidewatch Station, the Dockmaster, and the customs duty officer. · `warm`: The Charcadet in Crate 7-B is freezing. Take it up to the lighthouse lamp. Hesper keeps it there until you hold two badges.

**Reward:** disposed: $500, MERIDIAN+1; adopted: POTION x2; +2 pts. **Touches:** Meridian standing (+1 if you sign the disposal form); the Charcadet is collected after Badge 2.

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
- [if `badges >= 2`]
  - **Hesper** _(neutral)_: It's walking about on its own now. Been sitting by my lens every night, watching the road you went down.
  - **Hesper** _(angry)_: Now take it and go. And shut the door. You're letting the warm out.
  - [receive Charcadet Lv 18 (FLAMEBODY)]
  - [quest complete: adopted]
- [else]
  - **Hesper** _(deadpan)_: It'll not last a day on the coast road in this fog. It stays by the lamp till it can walk on its own.
  - **Hesper** _(angry)_: Come back when you've two of those badges rattling in your pocket. Not before. And shut the door.
  - *(Hesper will keep the Charcadet by the lamp until you hold two badges.)*

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

#### Off the Beat (`ZE_OCTAVE_OFF_BEAT`)

*Chapter 5 · Grant Kiosk P-3NNY / Cadence of the Octave, the Lowlight steps, Lumen City (map 181) · rank 1 · 3 points · unlock `badges >= 3`*

CALL FOR PROPOSALS #0031: NOISE COMPLIANCE, LOWLIGHT BLOCK 9. A STREET DRUMMER'S JOLTEON BLACKS OUT THE BLOCK. BOUNTY: $800.

**Quest log steps:** `ask`: Find the drummer on the Lowlight steps. · `junctions`: Cadence's Jolteon syncs to her drumming, and the Lattice syncs to it. Shift the three Lattice junction boxes on Block 9 off her beat. · `duel`: The block stayed lit. Cadence wants to play it out properly.

**Reward:** $800, CELLBATTERY x2; unknown: RES+1; fault: $800, MERIDIAN+1; +3 pts. **Touches:** The Octave: Cadence (3 of 8 in gym order); Meridian standing if you file it as a Lattice fault.

**Scene `offer`** (event: `pf_quest_run(:ZE_OCTAVE_OFF_BEAT, :offer)`)

- [stage] The Lowlight steps after dark. A woman in a cut-down Choir robe drums on a stack of paint tins, fast, in fours. A Jolteon bristles beside her in time. Every fourth beat, the streetlamps on the block flicker.
- **Cadence** _(deadpan)_: If you're from Meridian, I've got a permit. If you're not, I haven't got a permit.
- **Cadence** _(neutral)_: Cadence. Octave. Yes, that Octave. The Choir pays in hymns. Meridian pays in money. I tune their Lattice junctions on nights. Guess which one buys noodles.
- **Cadence** _(sad)_: Snare picks up my beat and the Lattice picks up Snare. One-two-three-four, blackout. They've posted a bounty on 'the source'. The source is me.
- **CHOICE:** Help Cadence?
  - > How do we fix it?
    - **Cadence** _(neutral)_: Three junction boxes on this block. They're tuned to a four-count, because some engineer liked a four-count. Shift each one off the beat and Snare can't drive them.
    - **Cadence** _(deadpan)_: I'd do it myself but I'm the source. They'd notice the source fiddling with the junctions.
    - [quest accepted]
    - [quest step: junctions]
  - > Not tonight.
    - **Cadence** _(deadpan)_: Nobody's ever free tonight. That's why it's always tonight.

**Scene `junction`** (event: `pf_quest_run(:ZE_OCTAVE_OFF_BEAT, :junction)`)

- [stage] A brass Lattice junction box, humming. A dial on the front ticks in fours, exactly in time with Cadence's drumming.
- *You turn the dial to a three-count. The hum stumbles and finds a new, lopsided rhythm. Down the steps, Snare's fur settles a little.*
- [if `quest_count(:SELF, :shifted) >= 3`]
  - [stage] Cadence plays a long roll. Snare crackles. The streetlamps stay on.
  - **Cadence** _(happy)_: Ha. Listen to that. It's terrible. It's the best thing I've ever heard.
  - [quest step: duel]
  - [continue: duel]

**Scene `duel`** (event: `pf_quest_run(:ZE_OCTAVE_OFF_BEAT, :duel)`)

- **Cadence** _(neutral)_: Snare's never been allowed to go flat out on this block. Let's find out what it's got. One, two, three, four.
- [trainer battle] OCTAVE_SINGER Cadence (v50) on `:NEON_GRID`
  - on won:
    - **Cadence** _(happy)_: Off the beat. Mine, not yours. Again tomorrow?
    - **Cadence** _(neutral)_: P-3NNY still wants a report on 'the source'. Your name, your report.
    - **CHOICE:** File the report as...
      - > 'Source unknown.'
        - **P-3NNY** _(neutral)_: REPORT FILED: SOURCE UNKNOWN. BOUNTY WITHHELD. THE REGISTRY IS DISAPPOINTED. THE REGISTRY WILL LIVE.
        - [the Octave remembers that you helped Cadence: the gauntlet order]
        - [quest complete: unknown]
      - > 'A Lattice tuning fault.'
        - **P-3NNY** _(happy)_: REPORT FILED: TUNING FAULT, BLOCK 9. MERIDIAN WILL CORRECT IT. BOUNTY RELEASED.
        - **Cadence** _(deadpan)_: They'll send someone to fix it. It'll be me. On nights. Fine.
        - [the Octave remembers that you helped Cadence: the gauntlet order]
        - [quest complete: fault]
  - on lost:
    - **Cadence** _(deadpan)_: Off your beat, that. Come back when you've got one.

**Scene `after`** (event: `pf_quest_run(:ZE_OCTAVE_OFF_BEAT, :after)`)

- **Cadence** _(neutral)_: Snare still drums. The lamps don't. Best of both.

#### Return to Sender (`ZE_RETURN_TO_SENDER`)

*Chapter 16 · Postmaster Halloran, Gale Post Hall, Skyreach (map 325) · rank 1 · 2 points · unlock `badges >= 14`*

CALL FOR PROPOSALS #0412: DEAD LETTERS, THREE (3). DELIVER BY HAND. PRIZE: ONE (1) DRAWER, CLEARED.

**Quest log steps:** `ask`: Postmaster Halloran has three dead letters for Skyreach. · `letters`: Deliver the three dead letters to their doors in Skyreach. · `return`: All three are delivered. Go back to the Postmaster.

**Reward:** PIDGEOTITE, ELECTRIUMZ; +2 pts. **Touches:** .

**Scene `offer`** (event: `pf_quest_run(:ZE_RETURN_TO_SENDER, :offer)`)

- **Postmaster Halloran** _(deadpan)_: Three letters. No stamps. Addresses in a hand I'd call 'enthusiastic'. The Gale Post delivers everything. Eventually.
- **Postmaster Halloran** _(neutral)_: Our couriers are all flying for the war. You've got legs. And a ring, I see. Hm.
- **CHOICE:** Deliver the dead letters?
  - > I'll take them.
    - [quest accepted]
    - [quest step: letters]
    - **Postmaster Halloran** _(neutral)_: Mast Ward, the Lower Gantries, the Skybridge. Knock twice. Nobody in Skyreach answers one knock.
  - > Not today.
    - **Postmaster Halloran** _(deadpan)_: They've waited eleven years. They'll wait.

**Scene `letter`** (event: `pf_quest_run(:ZE_RETURN_TO_SENDER, :letter)`)

- *You knock twice. A hand takes the letter, then the door shuts.*
- [if `quest_count(:SELF, :letters) >= 3`]
  - [quest step: return]
  - *That's the last one.*

**Scene `return`** (event: `pf_quest_run(:ZE_RETURN_TO_SENDER, :return)`)

- **Postmaster Halloran** _(happy)_: All three! The Post thanks you. The Post also owes you a drawer.
- **Postmaster Halloran** _(neutral)_: In it: the heartstone the Post's first courier-bird wore. Odessa says it's wasted in a drawer. Odessa says that about most things in drawers.
- **Postmaster Halloran** _(neutral)_: And a sliver of Choir glass someone posted in AF 290 and never collected. It crackles when the drawer opens. Take that too, before it shorts the franking machine.
- [quest complete]

### The Gutter Book

#### Lamps Out (`NA_OCTAVE_LAMPS_OUT`)

*Chapter 7 · Six-Fingers Ottoline (chalk job) / the marsh ferryman, the ferry steps on the runoff marsh, Mirefen (at night) (map 220) · rank 1 · 3 points · unlock `badges >= 5`*

Chalk job: someone keeps putting out the night-ferry lamps on the marsh. The ferrymen pay a cut to whoever stops it.

**Quest log steps:** `lamps`: At night, watch the three ferry lamps on the marsh. · `noct`: Something with gold rings in the dark put the lamps out. Find the lamplighter. · `duel`: Noct wants to know if you can be trusted with the dark.

**Reward:** $1000, DUSKBALL x5; truth: $1000; covered: HOLLOW+1; +3 pts. **Touches:** The Octave: Noct (5 of 8 in gym order); the Gutter Book takes its cut either way.

**Scene `offer`** (event: `pf_quest_run(:NA_OCTAVE_LAMPS_OUT, :offer)`)

- [stage] The ferry steps on the runoff marsh. A ferryman with a pole and a grudge.
- **Marsh ferryman** _(angry)_: Every night. Every lamp on the crossing, out, one after another. I've had two boats on the mud this week.
- **Six-Fingers Ottoline** _(neutral)_: (Chalked on the board above him, in Ottoline's hand:) LAMPS OUT. FERRYMEN PAY. MY CUT'S A FIFTH. IT'S YOURS. DON'T MAKE IT MINE.
- **CHOICE:** Take the job?
  - > I'll watch the lamps.
    - [quest accepted]
    - [quest step: lamps]
    - **Marsh ferryman** _(neutral)_: Nights only. In the day they behave.
  - > Not my business.
    - **Marsh ferryman** _(angry)_: Nobody's business. That's the business down here.

**Scene `lamp`** (event: `pf_quest_run(:NA_OCTAVE_LAMPS_OUT, :lamp)`)

- [if `!night`]
  - *The lamp is unlit and harmless in the daylight. Come back after dark.*
  - [end scene]
- [stage] A ferry lamp on a pole over the black water. As you watch, two gold rings blink in the reeds, and the flame folds down and goes out.
- [if `quest_count(:SELF, :lamps) >= 3`]
  - *The gold rings slip away across the boardwalk, toward the old lamplighter's hut at the end of the steps.*
  - [quest step: noct]
- [else]
  - *The gold rings are gone. Another lamp, further out, is still lit. For now.*

**Scene `noct`** (event: `pf_quest_run(:NA_OCTAVE_LAMPS_OUT, :noct)`)

- [stage] The lamplighter's hut. A young man in a soot-black Choir robe, a pole with a hook, and an Umbreon with its rings glowing. Behind him, under a sail, four sleeping children.
- **Noct** _(neutral)_: ...Shh.
- **Noct** _(neutral)_: Noct. Octave. The lamps are mine. So is putting them out.
- **Noct** _(sad)_: Sweetrot runners come up the crossing at night looking for lamp-runners. Kids who'll carry for them. They look where it's lit.
- **Noct** _(neutral)_: Wick puts the lamps out when they come. Dark's the only thing down here that's free.
- **CHOICE:** What do you tell the Gutter Book?
  - > The truth. The ferrymen should know why.
    - **Noct** _(neutral)_: ...Fine. Tell them. Then they can keep a lookout instead of a grudge.
  - > Marsh gas. It happens.
    - **Noct** _(neutral)_: ...Marsh gas. Ottoline will know. She'll take her fifth anyway.
- [quest step: duel]
- [continue: duel]

**Scene `duel`** (event: `pf_quest_run(:NA_OCTAVE_LAMPS_OUT, :duel)`)

- **Noct** _(neutral)_: Wick wants to know if you're safe in the dark. Show it.
- [trainer battle] OCTAVE_SINGER Noct (v50)
  - on won:
    - **Noct** _(neutral)_: ...Good. Now you know where the dark is.
    - **Noct** _(neutral)_: Corvin has beds at the infirmary. I'll take them in the morning. Thank you.
    - [the Octave remembers that you helped Noct: the gauntlet order]
    - [if `quest_flag(:SELF, :told) == :covered`]
      - [quest complete: covered]
    - [else]
      - [quest complete: truth]
  - on lost:
    - **Noct** _(neutral)_: ...Again. When you can see better.

**Scene `after`** (event: `pf_quest_run(:NA_OCTAVE_LAMPS_OUT, :after)`)

- **Noct** _(neutral)_: The lamps stay lit now. The kids sleep at Corvin's. Wick sulks. ...It's fine.

#### Bedside Manner (`NA_BEDSIDE_MANNER`)

*Chapter 21 · Wenlow, Corvin Mott's Infirmary, Mirefen (map 223) · rank 1 · 2 points · unlock `badges >= 18`*

CHALK: INFIRMARY NEEDS VISITORS. NOT DOCTORS. JUST VISITORS. - W.

**Quest log steps:** `ask`: Wenlow wants someone to sit with the Quiet Ward's patients. · `beds`: Sit with three of the Quiet Ward's patients. · `return`: Tell Wenlow how the visits went.

**Reward:** AUDINITE; +2 pts. **Touches:** .

**Scene `offer`** (event: `pf_quest_run(:NA_BEDSIDE_MANNER, :offer)`)

- **Wenlow** _(happy)_: You're back! Hi! Sorry. Hi. I'm doing rounds and I've got forty patients and two hands, and the Doctor says talking helps.
- **Wenlow** _(neutral)_: Their eyes move under the glass, did he tell you? Like they're dreaming. So I talk to them. Will you? Just three. They like new voices.
- **CHOICE:** Sit with the patients?
  - > Of course.
    - [quest accepted]
    - [quest step: beds]
    - **Wenlow** _(happy)_: Thank you! Start with Missus Garrow by the window, she likes the weather.
  - > Not now.
    - **Wenlow** _(neutral)_: That's all right. They're not going anywhere. Sorry. Doctor's joke.

**Scene `bed`** (event: `pf_quest_run(:NA_BEDSIDE_MANNER, :bed)`)

- *You sit and talk for a while: the weather, the road, the Festival. Under the glass, an eye moves.*
- [if `quest_count(:SELF, :beds) >= 3`]
  - [quest step: return]

**Scene `return`** (event: `pf_quest_run(:NA_BEDSIDE_MANNER, :return)`)

- **Wenlow** _(happy)_: They liked you. I can tell. Mister Coyle's hand twitched, that's practically a party.
- **Wenlow** _(neutral)_: Here. Matron, the Ward's Audino, came in with this round her neck. A heartstone, the Doctor says. She's too old for fighting, and you've got a ring now.
- **Wenlow** _(happy)_: Bring it back and show her sometime! She'd like that.
- [quest complete]

**Scene `corvin`** (event: `pf_quest_run(:NA_BEDSIDE_MANNER, :corvin)`)

- **Corvin** _(sad)_: Ah. You. He left something for you. Labelled, of course. He labelled everything.
- *A pink stone on a loop of bandage, and a tag in round handwriting: FOR THE ONE WITH THE SINGING RING. SHOW MATRON SOMETIME!*
- **Corvin** _(deadpan)_: Matron's heartstone. She's too old for fighting. I'm too old for most things. Take it before I get sentimental. It's bad for the patients.
- [quest complete]

#### Dogs of the Moon Market (`NA_MOON_MARKET_DOGS`)

*Chapter 17 · Six-Fingers Ottoline, the Moon Market, Underveil (map 423) · rank 1 · 3 points · unlock `badges >= 15`*

CHALK: BARONS' KENNEL. THREE CAGES. NOBODY SAW NOTHING.

**Quest log steps:** `ask`: Ottoline has a job at the Barons' kennel. · `cages`: Open the three kennel cages behind the Moon Market. · `return`: The cages are open. See Ottoline.

**Reward:** HOUNDOOMINITE, DARKINIUMZ; +3 pts. **Touches:** .

**Scene `offer`** (event: `pf_quest_run(:NA_MOON_MARKET_DOGS, :offer)`)

- **Six-Fingers Ottoline** _(neutral)_: The Barons starve Houndoom for the pit fights. Starved dogs bite harder. I want the dogs out and the Barons embarrassed. Mostly the second.
- **Six-Fingers Ottoline** _(smug)_: There's a prize in the kennel-master's lockbox. You get it. I get the story.
- **CHOICE:** Take the job?
  - > Open the cages.
    - [quest accepted]
    - [quest step: cages]
  - > Not my business.
    - **Six-Fingers Ottoline** _(deadpan)_: Everything down here is your business. You just don't know it yet.

**Scene `cage`** (event: `pf_quest_run(:NA_MOON_MARKET_DOGS, :cage)`)

- *The latch gives. A thin Houndoom looks at you, then at the open door, then it's gone into the dark.*
- [if `quest_count(:SELF, :cages) >= 3`]
  - [quest step: return]
  - **Kennel-master Grisk** _(angry)_: HEY! Those were Baron property! ...You know what, I'm not paid enough. Take the box. Take the whole thing.

**Scene `return`** (event: `pf_quest_run(:NA_MOON_MARKET_DOGS, :return)`)

- **Six-Fingers Ottoline** _(happy)_: The whole market saw. The Barons will be furious for a week. Beautiful.
- **Six-Fingers Ottoline** _(neutral)_: Your cut. A pit champion's heartstone. Don't sell it down here; everyone will know where you got it.
- *Under the kennel-master's stool, wrapped in a betting slip: a sliver of black glass. Nobody comes to claim it.*
- [quest complete]

#### The Memory Kata (`NA_MEMORY_KATA`)

*Chapter 19 · Six-Fingers Ottoline, the Last Rung, Ironreach (map 260) · rank 2 · 4 points · unlock `badges >= 17`*

CHALK: PAWN SHELF, TOP ROW. A WARDGUARD STONE. THE OWNER WANTS IT GONE TO SOMEONE WHO'LL USE IT.

**Quest log steps:** `ask`: Buy the Wardguard heartstone off Ottoline's pawn shelf ($20,000).

**Reward:** LUCARIONITE, FIGHTINIUMZ; +4 pts. **Touches:** .

**Scene `offer`** (event: `pf_quest_run(:NA_MEMORY_KATA, :offer)`)

- **Six-Fingers Ottoline** _(neutral)_: Top shelf. A Wardguard unit's ring-stone. Pawned here the winter after Marrowgate. The man who pawned it comes in every year to look at it.
- **Six-Fingers Ottoline** _(neutral)_: This year he said sell it. To someone who'll use it. Twenty thousand. I'm sentimental, not stupid.
- **CHOICE:** Pay $20,000?
  - > Pay.
    - [if `money >= 20000`]
      - [quest accepted]
      - [pay $20000]
      - [continue: kata]
    - [else]
      - **Six-Fingers Ottoline** _(deadpan)_: Come back with twenty thousand. The stone isn't going anywhere.
  - > Not yet.
    - **Six-Fingers Ottoline** _(deadpan)_: It's waited fifteen years.

**Scene `kata`** (event: `pf_quest_run(:NA_MEMORY_KATA, :kata)`)

- [stage] Kaito is at the bar, wraps on, a cup of something he isn't drinking.
- **Kaito** _(neutral)_: It was my unit's. Memory's mother wore it, at Marrowgate. She could feel them through the gate. So could I.
- **Kaito** _(neutral)_: It remembers for me. Now it can remember for you. Use it on someone who deserves it.
- *Wrapped with the stone in the unit's old armband, and newer than both: a sliver of glass that hums like a struck gong. Someone has added it on one of those yearly visits.*
- [quest complete]
- **Kaito** _(neutral)_: Stand up. Again. That's the whole kata.

### The Trial by Flames

#### The Little Crucible (`AS_LITTLE_CRUCIBLE`)

*Chapter 4 · Sergeant Brakka Emberhide, the Legion recruiting barge, Saltmere harbour (map 146) · rank 1 · 3 points · unlock `badges >= 2`*

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
- [battle] Litleo "Cinderpaw" Lv 21 (MOXIE)
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

#### Too Loud for the Choir (`AS_OCTAVE_TOO_LOUD`)

*Chapter 8 · Forte of the Octave, the Crucible on the caldera rim, Cindervault (map 240) · rank 1 · 3 points · unlock `badges >= 6`*

Writ of Flame: a Choir singer wants a Writ. The Crucible will hear her if she brings a second.

**Quest log steps:** `ask`: Find the singer outside the Crucible. · `legate`: Stand as Forte's second before Legate Varra Kosk. · `duel`: The Legate's trial: Forte fights her own second, in the Crucible.

**Reward:** $2000, HEATROCK; +3 pts. **Touches:** The Octave: Forte (6 of 8 in gym order); Ashkaar honesty (she must say who she is).

**Scene `offer`** (event: `pf_quest_run(:AS_OCTAVE_TOO_LOUD, :offer)`)

- [stage] Outside the Crucible's gate a young woman in a scorched Choir robe is arguing with a herald twice her size, and winning on volume.
- **Forte** _(angry)_: I can fight! Look at me! LOOK at me!
- [stage] The herald walks away. She turns on you, still shouting, then sees your badges and stops.
- **Forte** _(happy)_: Oh! You're a challenger. Brilliant. Forte. Octave. That's Bellows. Bellows, say hello. Not like that. Not on fire.
- **Forte** _(neutral)_: I want a Writ of Flame. The Legion. They won't hear a 'Choir child' without a second to stand for her. Will you stand for me?
- **CHOICE:** Stand as Forte's second?
  - > I'll stand for you.
    - [quest accepted]
    - [quest step: legate]
    - **Forte** _(happy)_: YES. The Legate's inside. Don't let me talk.
  - > Why do you want to join the Legion?
    - **Forte** _(neutral)_: Because everyone looks at us like we're sad. The Glassfall orphans. Poor things. I'm not a poor thing. I'm loud.
    - **Forte** _(neutral)_: Ask me again when you'll stand for me.

**Scene `legate`** (event: `pf_quest_run(:AS_OCTAVE_TOO_LOUD, :legate)`)

- [stage] The Crucible: a sand ring on the caldera rim. Legate Varra Kosk sits on the steps with a ledger on her knee.
- **Legate Varra Kosk** _(neutral)_: You told my herald you were twenty, from the Cinder Cape, and a Legion family. Which of those was true?
- **Forte** _(sad)_: ...None of them.
- **Legate Varra Kosk** _(neutral)_: Lying is a crime here. Not a large one. It ends the conversation. Unless your second has something to say.
- **CHOICE:** What do you say?
  - > Tell her who you are, Forte.
    - **Forte** _(neutral)_: ...I'm a Choir orphan. From the Glassfall. I sing. I'm also the strongest person in this ring, and I'm not sorry.
    - **Legate Varra Kosk** _(happy)_: There. That's a Writ's worth of truth. Now show me the strong part.
  - > She's the strongest singer you'll ever meet.
    - **Legate Varra Kosk** _(neutral)_: That's your truth, second. I asked for hers.
    - **Forte** _(neutral)_: ...I'm a Choir orphan. I sing. And I'm strong. That's all of it.
    - **Legate Varra Kosk** _(happy)_: Better. Now show me.
- **Legate Varra Kosk** _(neutral)_: The trial is simple. Fight your second. Win, or lose well. Both are honest.
- [quest step: duel]
- [continue: duel]

**Scene `duel`** (event: `pf_quest_run(:AS_OCTAVE_TOO_LOUD, :duel)`)

- **Forte** _(happy)_: Don't go easy. If you go easy I'll know and I'll shout.
- [trainer battle] OCTAVE_SINGER Forte (v50) on `:VOLCANIC`
  - on won:
    - **Forte** _(happy)_: Too loud? ...No. Just right. You were louder.
    - **Legate Varra Kosk** _(neutral)_: Lost well. Honestly. That is a Writ.
    - [stage] The Legate brands an iron token with Forte's mark. Forte holds it up to Bellows, who sneezes on it.
    - [the Octave remembers that you helped Forte: the gauntlet order]
    - [quest complete]
  - on lost:
    - **Legate Varra Kosk** _(neutral)_: She won. That's also a Writ, but not for you. Come back when your second can stand.

**Scene `after`** (event: `pf_quest_run(:AS_OCTAVE_TOO_LOUD, :after)`)

- **Forte** _(happy)_: I'm a Legion recruit AND I'm in the Octave. Vesper cried. Happy crying. I think.

#### The Forge Remembers (`AS_FORGE_REMEMBERS`)

*Chapter 17 · Brann Holloway, the Hearthguild Hall, Cindervault (after the Ring) (map 244) · rank 1 · 0 points · unlock `badges >= 15 && quest_done(:OS_RING_DAY)`*

Brann found something in the slag.

**Quest log steps:** `ask`: Brann wants a word at the Hearthguild.

**Reward:** CAMERUPTITE; +0 pts. **Touches:** .

**Scene `spare`** (event: `pf_quest_run(:AS_FORGE_REMEMBERS, :spare)`)

- **Brann** _(happy)_: There you are! War on the doorstep and you still come by. Sit. No, not there, that's hot.
- **Brann** _(shocked)_: ...That's my ring. The odd one. So old Ore finally gave it away. Ten years it sulked in his lamp-room.
- [if `choice(:ch8_lightstone) == :dominar`]
  - **Brann** _(sad)_: I haven't forgotten the Light Stone, mind. 'It's his people's,' you said. ...No. I'm not going to talk about it. The ring doesn't hold it against you, so I won't. Not today.
- **Brann** _(neutral)_: Kiln, my Camerupt. If you've met her, you remember her. She likes to erupt on people.
- **Brann** _(neutral)_: Every heartstone's got a twin somewhere. Hers turned up in the slag this spring, still warm. The caldera makes them like other mountains make gravel.
- **Brann** _(smug)_: I'd give it to a Warden. You'll do better than most Wardens.
- [script]
- **Brann** _(deadpan)_: Your ring still singing? ...No. Don't tell me. I sleep badly enough.

#### Old Cinder (`AS_OLD_CINDER`)

*Chapter 17 · Roost-keeper Tarn, Pyre Keep, the Dragon Roosts (map 248) · rank 1 · 3 points · unlock `badges >= 15`*

WRIT: The war-Charizard Old Cinder will not leave the high roost. Its rider fell at the front. Bring it down, honourably.

**Quest log steps:** `ask`: Roost-keeper Tarn wants Old Cinder brought down from the high roost. · `fight`: Face Old Cinder on the high roost.

**Reward:** CHARIZARDITEX, DRAGONIUMZ; +3 pts. **Touches:** .

**Scene `offer`** (event: `pf_quest_run(:AS_OLD_CINDER, :offer)`)

- **Roost-keeper Tarn** _(sad)_: Old Cinder's rider died on the Rimed Sands. Since then it won't come down. It won't eat. It burns anyone who climbs.
- **Roost-keeper Tarn** _(neutral)_: In Ashkaar we don't put a dragon down for grief. We give it a fight worth having. Then it remembers it's alive.
- **CHOICE:** Climb to the high roost?
  - > I'll fight it.
    - [quest accepted]
    - [quest step: fight]
    - **Roost-keeper Tarn** _(neutral)_: Say true or say nothing, up there. It can tell.
  - > Not yet.
    - **Roost-keeper Tarn** _(neutral)_: It's not going anywhere. That's the trouble.

**Scene `fight`** (event: `pf_quest_run(:AS_OLD_CINDER, :fight)`)

- *On the high roost, a scarred black-eyed Charizard lifts its head. A cracked Legion harness still hangs from its neck.*
- [battle] Charizard "Old Cinder" Lv 72 (SOLARPOWER)
  - on won:
    - *Old Cinder folds its wings and lowers its head to you, the way it must once have lowered it to its rider.*
    - *From the harness, Tarn unclips a stone as black as the Pyre Road, with a blue flame caught in it.*
    - **Roost-keeper Tarn** _(neutral)_: Its war-stone. It hasn't worn it since. It wants you to have it. Don't argue with a dragon.
    - *Sewn into the harness strap beside the stone is a sliver of blue-black glass. A rider's keepsake from the Glassfall.*
    - [quest complete]
  - on lost:
    - *Old Cinder turns its back and curls around the empty saddle again.*

#### The Brazier Writ (`AS_BRAZIER_WRIT`)

*Chapter 17 · Legate Varra Kosk, the Crucible, Cindervault (map 240) · rank 2 · 4 points · unlock `badges >= 15`*

WRIT OF THE BRAZIER: the Crucible keeps one heartstone for one who earns it without being born to a dragon.

**Quest log steps:** `ask`: Answer the brazier's question before Legate Kosk.

**Reward:** SALAMENCITE, FIRIUMZ; +4 pts. **Touches:** .

**Scene `offer`** (event: `pf_quest_run(:AS_BRAZIER_WRIT, :offer)`)

- **Legate Varra Kosk** _(neutral)_: The Crucible keeps a heartstone for a dragon-rider who wasn't born to a dragon. In forty years nobody has taken it.
- **Legate Varra Kosk** _(neutral)_: The oath is one question, at the brazier. Lie and the writ burns. Ashkaar law.
- [quest accepted]
- **CHOICE:** **Legate Varra Kosk**: Why do you fight?
  - > For the people I've met.
    - [continue: sworn]
  - > Because I'm good at it.
    - [continue: sworn]
  - > I don't know yet.
    - **Legate Varra Kosk** _(smug)_: The first honest answer in forty years.
    - [continue: sworn]
  - > For the glory of Ashkaar.
    - **Legate Varra Kosk** _(deadpan)_: ...No. The brazier says otherwise. The writ burns. Come back when you'll say true.

**Scene `sworn`** (event: `pf_quest_run(:AS_BRAZIER_WRIT, :sworn)`)

- **Legate Varra Kosk** _(neutral)_: Say true, and the fire keeps you. The writ is yours.
- *She takes a blue stone with a red heart from a niche above the brazier. It is hot enough that she hands it over in tongs.*
- **Legate Varra Kosk** _(neutral)_: And the brazier's own sliver. The Choir tuned it to our fire after the Glassfall. Your Warden's ring will hear it.
- [quest complete]

### The Rolls of Unearthing

#### The Noon Bell (`OS_OCTAVE_NOON_BELL`)

*Chapter 6 · Sona of the Octave, the Temple of the Noon Sun, outside Duneholt (new map, off Sunbleach Flats 613) (map 215) · rank 1 · 3 points · unlock `badges >= 4`*

Clay tablet: the old sun temple's light-shaft has filled with sand. Its keeper needs diggers. Its keeper says she knew you'd read this.

**Quest log steps:** `ask`: Find the keeper of the Temple of the Noon Sun. · `dig`: Dig the three sand drifts out of the temple's light-shaft. · `noon`: The shaft is clear. Be in the temple at noon (any time of day, not at night).

**Reward:** $1500, SUNSTONE; +3 pts. **Touches:** The Octave: Sona (4 of 8 in gym order).

**Scene `offer`** (event: `pf_quest_run(:OS_OCTAVE_NOON_BELL, :offer)`)

- [stage] A round sandstone temple, half swallowed by a dune. Inside, in the gloom, a woman in Choir grey sits beside a sleeping Espeon whose forehead jewel has gone dull. She speaks before you do.
- **Sona** _(neutral)_: Yes, I'm the keeper. Yes, the sand. No, it isn't dangerous. You were going to ask all three.
- **Sona** _(neutral)_: Sona. Of the Octave. Noon sleeps here, where the light used to fall at midday. The dune came down the shaft in the spring and the light stopped.
- **Sona** _(sad)_: Its jewel has been dark for a month. It still knows when noon is. It wakes, and looks up, and goes back to sleep.
- **Sona** _(deadpan)_: You're going to say yes. I'll get the spade.
- **CHOICE:** Dig out the light-shaft?
  - > Yes.
    - [quest accepted]
    - [quest step: dig]
    - **Sona** _(neutral)_: Three drifts. I heard you'd be quick.
  - > No.
    - **Sona** _(neutral)_: Hm. I didn't hear that coming. I'm glad. It's boring, being right.

**Scene `drift`** (event: `pf_quest_run(:OS_OCTAVE_NOON_BELL, :drift)`)

- [stage] A drift of sand packed into the light-shaft. You dig until a broken clay tablet slides out of it and the sand runs away under your feet.
- [if `quest_count(:SELF, :drifts) >= 3`]
  - *Daylight falls down the shaft for the first time in a month and lies on the temple floor in a hot white circle.*
  - **Sona** _(happy)_: There. Now we wait for noon. Noon will wait too. It's very good at it.
  - [quest step: noon]
- [else]
  - *A little more light gets in. The shaft is not clear yet.*

**Scene `noon`** (event: `pf_quest_run(:OS_OCTAVE_NOON_BELL, :noon)`)

- [if `night`]
  - **Sona** _(neutral)_: It's night. Even I can't make it noon. Come back in the day.
  - [end scene]
- [stage] Noon. The circle of light slides onto the sleeping Espeon. Its jewel lights red, then white, and it opens its eyes.
- **Sona** _(happy)_: Hello, Noon.
- **Curator-Elect Nasrin Vael** _(neutral)_: (From the doorway, out of breath:) The Rolls will want that tablet, you know. And a full record of the dig. ...It's lovely, though.
- **Sona** _(neutral)_: Noon wants to stretch. It hasn't fought in a month. You knew I'd ask.
- [trainer battle] OCTAVE_SINGER Sona (v50)
  - on won:
    - **Sona** _(happy)_: I heard that coming. I still couldn't stop it. That's the nice kind.
    - **Sona** _(neutral)_: Ring the bell on your way out. It's been a long time since anyone rang it at noon.
    - [the Octave remembers that you helped Sona: the gauntlet order]
    - [quest complete]
  - on lost:
    - **Sona** _(neutral)_: I knew you'd want another go. It'll be noon again tomorrow.

**Scene `after`** (event: `pf_quest_run(:OS_OCTAVE_NOON_BELL, :after)`)

- **Sona** _(neutral)_: You're going to ask if Noon is happy. Yes. You're going to ask if I am. ...Come back another day and ask that.

#### The Ring-Day (`OS_RING_DAY`)

*Chapter 14 · Bastian Ore, Bastian's lamp-room, the lowest of the Cragholm Lift Galleries (after Gym 13) (map 363) · rank 1 · 0 points · unlock `badges >= 13 && !mega_ring`*

Bastian wants you in his lamp-room.

**Quest log steps:** `ask`: Bastian is waiting in his lamp-room in the deep seams.

**Reward:** MEGARING, AGGRONITE; +0 pts. **Touches:** Gives the Mega Ring (Mega Evolution and, SPINE Rev 23, Z-moves open) and the Aggronite. Foreshadows the PC's splinter: the ring sings..

**Scene `ringday`** (event: `pf_quest_run(:OS_RING_DAY, :ringday)`)

- [stage] The lowest gallery of the deep seams. Bastian's lamp-room: a cot, a kettle and forty years of lamps. Pip is perched on a crate; Larch sits by the door with a book she isn't reading.
- **Bastian** _(happy)_: Sit, sit. Flawless cut, that was. Don't tell the cavern I said so. It sulks.
- **Bastian** _(neutral)_: You'll have seen a few of those by now. Anja's Glalie. Odessa's bird. That Directorate woman's dog. My old Amber, just now. Nobody's told you properly what it is, I'd wager. Every Warden's seat has a ring. 'Mega Ring', the Accord calls it. The Hearthguild's cut one for every seat since the Concordance.
- **Bastian** _(neutral)_: A gold band, and a chip of the Crown's own stone. No colour of its own, so it takes any colour you put to it. That's how it opens a heartstone.
- **Bastian** _(neutral)_: Heartstones. 'Mega Stones', if you're Accord. Leave an Imprint in one kind of Pokemon long enough and it pearls. Your partner holds the stone, you wear the ring, and for one fight it carries its whole Imprint.
- **Bastian** _(deadpan)_: One heart at a time, mind. Two rings on the same side ring against each other. One Mega to a side, always. Remember it in a double.
- **Bastian** _(neutral)_: And if you come by a Choir crystal, a sliver of Glassfall glass, it'll answer that too. The chip's grind off the Crown's stone, and the glass came out of the night it cracked. Same crown, one way or another. One Z-move a fight, and one to a side, same as the hearts.
- *He unwraps an oilcloth: a plain gold band, and set in it a chip of stone with no colour at all.*
- **Bastian** _(neutral)_: Holloway cut this one. The forge-man in Cindervault. Ten years back. He sent it to me in a sock, with a note: 'It sulks. Keep it where nobody asks questions.' So it's been under my mountain.
- **Bastian** _(deadpan)_: Two old men who don't ask each other things. That's how you get to seventy-four.
- **Bastian** _(neutral)_: Rock's patient. I reckon this has waited long enough. Hold out your hand.
- *He drops the ring into your palm. The colourless chip catches the lamplight... and sings: one clear note, like a wet finger round the rim of a glass.*
- *Somewhere under your ribs, something answers it.*
- **Pip** _(shocked)_: Grandad. Grandad, it's SINGING.
- **Bastian** _(neutral)_: Is it? Can't hear a thing. Half-deaf, me.
- **Bastian** _(sad)_: ...I can feel it in the table, though. Holloway swore they don't sing. Thirty years at his anvil, and not one of them ever sang.
- [stage] Larch has lowered her book.
- **Bastian** _(worried)_: Well. It isn't sulking, anyway. Here: an iron heart to start you off. The Aron down the east seam wear these like warts.
- [script]
- [if `mega_stones > 1`]
  - *The other stones in your Bag are warm now, and quiet, as if they had stopped waiting.*
- **Bastian** _(happy)_: Wear it. If the Directorate comes down my lifts tonight, I'd like them to meet a ferry child with a Warden's ring.

#### Amber, Again (`OS_AMBER_AGAIN`)

*Chapter 14 · Sahar Ostrand, Sahar's Dig Lab, Duneholt (map 209) · rank 1 · 2 points · unlock `badges >= 12`*

TABLET: The Old Amber held two things. The Warden kept one. Bring her the other, alive.

**Quest log steps:** `ask`: Show Sahar an Aerodactyl revived from the Old Amber.

**Reward:** AERODACTYLITE; +2 pts. **Touches:** .

**Scene `offer`** (event: `pf_quest_run(:OS_AMBER_AGAIN, :offer)`)

- **Sahar** _(deadpan)_: The Old Amber from the Brinecut mine. Lumen's lab woke the Aerodactyl in it for you, then sent me the rest for the Rolls. The rest had this in it. I kept it.
- **Sahar** _(neutral)_: Shameful. I'm a curator. Curators keep things. Show me the Aerodactyl alive and well, and this is yours.
- [quest accepted]
- [if `party_has(:AERODACTYL)`]
  - [continue: show]
- [else]
  - **Sahar** _(neutral)_: No Aerodactyl with you. The amber waited a hundred thousand years; I can wait an afternoon.

**Scene `show`** (event: `pf_quest_run(:OS_AMBER_AGAIN, :show)`)

- *Your Aerodactyl sniffs at Sahar's coat, then at the drawer she unlocks.*
- **Sahar** _(sad)_: ...It remembers. Look at that. Here. The amber's other half. Its heart, set hard.
- [quest complete]
- **Sahar** _(deadpan)_: The desert keeps everything. It just doesn't keep it where you left it. Neither do I, apparently.

#### The Tyrant's Heart (`OS_TYRANT_HEART`)

*Chapter 17 · Curator-Elect Nasrin Vael, the Cragholm lift-house rack; the dig is on the Vertebrae (map 360) · rank 2 · 4 points · unlock `badges >= 15`*

TABLET: A tyrant's heart lies in the third vertebra. Dig it out whole.

**Quest log steps:** `ask`: Dig the tyrant's heart out of the third vertebra on the Vertebrae. · `return`: Take the heartstone to Curator-Elect Nasrin.

**Reward:** TYRANITARITE, GROUNDIUMZ; +4 pts. **Touches:** .

**Scene `offer`** (event: `pf_quest_run(:OS_TYRANT_HEART, :offer)`)

- **Curator-Elect Nasrin Vael** _(neutral)_: A commission for a Delver, not a Sandsifter. The Vertebrae are a Tyranitar's spine, a mountain of it. The third vertebra has a heart in it.
- **Curator-Elect Nasrin Vael** _(neutral)_: Dig it out whole and the Rolls will write your name in the good ink.
- **CHOICE:** Take the commission?
  - > Take it.
    - [quest accepted]
    - **Curator-Elect Nasrin Vael** _(happy)_: Wonderful. Bring a shovel and something that can carry a mountain.
  - > Not yet.
    - **Curator-Elect Nasrin Vael** _(neutral)_: It's been there a while.

**Scene `dig`** (event: `pf_quest_run(:OS_TYRANT_HEART, :dig)`)

- *Under the third vertebra, the rock is warm. You dig until your hands are raw, and there it is: a stone the green of old armour, with a dark heart.*
- [quest step: return]

**Scene `return`** (event: `pf_quest_run(:OS_TYRANT_HEART, :return)`)

- **Curator-Elect Nasrin Vael** _(happy)_: Whole! Not a crack! The Rolls thank you. The Rolls also say you keep it; we only wanted it written down.
- *On the vertebra's crown above your dig, where some Choir pilgrim must have left it to soak: a sliver of Glassfall glass, humming with the earth. The Rolls say finders keepers.*
- [quest complete]

### The Rite of Reflection

#### The Still Water (`AN_OCTAVE_STILL_WATER`)

*Chapter 13 · Lento of the Octave (the Rite, read at Glassmere), the frozen Mirror Mere, past Glassmere (753) (map 742) · rank 1 · 4 points · unlock `badges >= 11`*

Mirror-writing in the reading-pool: the Mirror Mere froze in summer. Its singer won't leave the ice. Her reflection is under it.

**Quest log steps:** `ask`: Find the singer on the frozen Mirror Mere. · `cracks`: Lector Saffi: in Antumbra you free a thing by holding it backwards. Walk the three cracks in the ice from their ends to their starts. · `duel`: The ice is thin and Lento is ready to let go.

**Reward:** $4000, MIRRORHERB; +4 pts. **Touches:** The Octave: Lento (7 of 8 in gym order); the Rite of Reflection.

**Scene `offer`** (event: `pf_quest_run(:AN_OCTAVE_STILL_WATER, :offer)`)

- [stage] The Mirror Mere, frozen white in high summer. In the middle of the ice a woman in Choir grey stands perfectly still beside a Glaceon. Under the ice, her reflection stands upside down, beating softly on it.
- **Lento** _(neutral)_: Hello. Hello.
- **Lento** _(neutral)_: I'm Lento. Lento. Of the Octave. I say things twice. Once for me, once for her. Habit. Habit.
- **Lento** _(sad)_: Reflections wander here. Mine wanted to go. Hush froze the mere so she couldn't. I didn't ask it to. I didn't ask it not to.
- **Lento** _(sad)_: Now she's under there and I'm up here, and neither of us can leave. Slowly, slowly, I've noticed this is worse.
- **CHOICE:** Help Lento?
  - > How?
    - **Lento** _(neutral)_: Lector Saffi would know. She reads the Rite at Glassmere. She'll tell you backwards. Listen backwards.
    - **Lector Saffi Ivarne** _(neutral)_: (Her mirror-writing in the reading-pool, read in the glass:) TO FREE A THING IN ANTUMBRA, HOLD IT BACKWARDS. WALK EACH CRACK FROM ITS END TO ITS START.
    - [quest accepted]
    - [quest step: cracks]
  - > I'll come back.
    - **Lento** _(neutral)_: Slowly. Slowly. We'll be here.

**Scene `crack`** (event: `pf_quest_run(:AN_OCTAVE_STILL_WATER, :crack)`)

- [stage] A long crack across the ice. You find where it ends and walk it back to where it began. Under your feet, the reflection walks it with you, upside down, the other way.
- [if `quest_count(:SELF, :cracks) >= 3`]
  - *On the third crack the ice sighs. It does not break. It just stops holding on.*
  - [stage] Lento's reflection rises to the underside of the ice, presses one hand to it, and lets go. It drifts off across the mere, slowly, toward the Glass.
  - **Lento's reflection** _(happy)_: (Faint, from under the ice, said once:) Thank you.
  - **Lento** _(sad)_: She only said it once. She's never done that.
  - **Lento** _(neutral)_: It's all right. It's all right. She'll come back. Slowly.
  - [quest step: duel]
  - [continue: duel]
- [else]
  - *The ice creaks. It is still holding on.*

**Scene `duel`** (event: `pf_quest_run(:AN_OCTAVE_STILL_WATER, :duel)`)

- **Lento** _(neutral)_: Hush is upset. Hush is upset. It thinks it did something wrong. Duel us? It needs to do something right.
- [trainer battle] OCTAVE_SINGER Lento (v50) on `:FROZEN_LAKE`
  - on won:
    - **Lento** _(happy)_: Slowly, slowly. You got there first anyway.
    - **Lento** _(neutral)_: I'm going to write to Vesper. I'm going to write to Vesper. She'll be cross I didn't write sooner. Once.
    - [the Octave remembers that you helped Lento: the gauntlet order]
    - [quest complete]
  - on lost:
    - **Lento** _(neutral)_: Again. Again. When the ice is kinder.

**Scene `after`** (event: `pf_quest_run(:AN_OCTAVE_STILL_WATER, :after)`)

- **Lento** _(happy)_: She comes back some evenings and stands beside me in the water. Then she goes. That's what reflections are for. For.

#### The Smile Behind the Glass (`AN_SMILE_BEHIND_GLASS`)

*Chapter 15 · Lector Saffi Ivarne, the Speculum, Lucent (map 346) · rank 2 · 3 points · unlock `badges >= 13`*

MIRROR-WRITING: Somebody's reflection in the Speculum is smiling with too many teeth.

**Quest log steps:** `ask`: A reflection in the Speculum smiles with too many teeth. Face it. · `return`: Tell Lector Saffi what was behind the glass.

**Reward:** MAWILITE; +3 pts. **Touches:** .

**Scene `offer`** (event: `pf_quest_run(:AN_SMILE_BEHIND_GLASS, :offer)`)

- **Lector Saffi Ivarne** _(neutral)_: In the third pane of the Speculum, every reflection smiles. Including the people who don't. Particularly them.
- **Lector Saffi Ivarne** _(deadpan)_: It's a Rite. You stand there until it stops. Most people leave. Will you stay?
- **CHOICE:** Face the third pane?
  - > I'll stay.
    - [quest accepted]
    - **Lector Saffi Ivarne** _(neutral)_: Don't smile back. It counts as an answer.
  - > No thank you.
    - **Lector Saffi Ivarne** _(neutral)_: Wise. Rare, but wise.

**Scene `pane`** (event: `pf_quest_run(:AN_SMILE_BEHIND_GLASS, :pane)`)

- *Your reflection smiles. Behind it, a second mouth opens, wider than the first, full of steel teeth.*
- *You don't smile back. You wait. After a long time, the second mouth closes, and something falls out of the glass onto the floor: a stone, pink and grey.*
- [quest step: return]

**Scene `return`** (event: `pf_quest_run(:AN_SMILE_BEHIND_GLASS, :return)`)

- **Lector Saffi Ivarne** _(happy)_: A Mawile's heart. It was hiding in the glass, eating everyone's smiles. Now it has nothing to hide behind.
- [quest complete]

### The Hall of Petitions

#### The Eevee Octave (`CR_OCTAVE`)

*Chapter 2 · Vesper Lindqvist, backstage at the Lantern Theatre, Saltmere (asked); the Glassfall Memorial Garden, Crownhaven (489) (map 145) · rank 1 · 5 points · unlock ``*

Vesper asked you to look in on the eight singers of the Octave as your road takes you through the kingdoms.

**Quest log steps:** `road`: Look in on the Octave's singers as you travel: Lyra (Briarwick), Aria (Ebbmouth), Cadence (Lumen City), Sona (Duneholt), Noct (Mirefen), Forte (Cindervault), Lento (the Mirror Mere). Carol never leaves Crownhaven. · `garden`: All eight singers have had your help. Vesper is waiting in the Glassfall Memorial Garden in Crownhaven.

**Reward:** EEVIUMZ, Eevee Lv 70 (ADAPTABILITY); +5 pts. **Touches:** The gauntlet runs in the order you helped the singers (each Eeveelution uses its Z-move); S177 EEVEE_OCTAVE_DONE.

**Scene `saltmere`** (event: `pf_quest_run(:CR_OCTAVE, :saltmere)`)

- [stage] After the duet backstage (S190). Vesper is folding Amen's ribbon back into her sleeve.
- **Vesper** _(neutral)_: We sing together once a year, for the Pageant. Tomorrow we scatter again. Each of us lives beside a Plate now, one each, in all seven kingdoms.
- **Vesper** _(happy)_: Except Carol. Carol never leaves Crownhaven. Someone has to sing to the ones who didn't get out.
- **Vesper** _(neutral)_: They're very good at singing and very bad at being alone. If your road takes you past any of them... would you look in on them?
- **CHOICE:** Look in on the Octave?
  - > I will.
    - **Vesper** _(happy)_: Thank you. Lyra's going home to Briarwick, so she's first, if you go that way.
    - [quest accepted]
  - > Why me?
    - **Vesper** _(neutral)_: Because you looked at Understudy the way they look at their Eevee. Like it was a person.
    - **Vesper** _(happy)_: And because nobody else asked. That's usually how.
    - [quest accepted]
- **Vesper** _(neutral)_: Lyra in Briarwick. Aria in Ebbmouth. Cadence in Lumen City. Sona in Duneholt. Noct in Mirefen. Forte in Cindervault. Lento at the Mirror Mere.
- **Vesper** _(happy)_: I'll be at the Festival. We always are.

**Scene `lucent`** (event: `pf_quest_run(:CR_OCTAVE, :lucent)`)

- [stage] Chapter 13, the Athenaeum cloister, after Vesper's sparring double (S191).
- **Vesper** _(neutral)_: Carol writes to me every week. The others write when something has gone wrong.
- [if `octave_helped >= 5`]
  - **Vesper** _(happy)_: So I've had a lot of letters about you. Good letters. Forte's had three exclamation marks in it.
- [else]
  - **Vesper** _(neutral)_: None of them has mentioned you yet. That's all right. Roads are long.
- [if `!octave_has(:LENTO)`]
  - **Vesper** _(sad)_: Lento hasn't written at all. She's at the Mirror Mere, past Glassmere. It's frozen, they say. In summer.

**Scene `garden`** (event: `pf_quest_run(:CR_OCTAVE, :garden)`)

- [stage] The Glassfall Memorial Garden. White stone, a ring of glass figures among the roses, and eight singers standing in a half-circle with their Eeveelutions. Vesper steps out to meet you.
- **Vesper** _(happy)_: You came. Everyone, it's them.
- **Vesper** _(neutral)_: All eight of them have written to the Choir about you. Lyra's Eevee came down off its stone. Aria got Brine back out of the river. Cadence still has her job, somehow.
- **Vesper** _(neutral)_: Sona's bell rings at noon again. Noct's lamp-runners sleep in a bed. Forte has a Writ of Flame. Lento's reflection comes and goes as it likes. And Carol finished her song.
- **Vesper** _(happy)_: They wanted to thank you. Properly. And the Choir has a custom: before we pass on the power of Eevee, someone has to prove they can carry it.
- **Vesper** _(neutral)_: So: all eight of them, in the order you helped them, one after another. Then me, and Amen. No rest between.
- **CHOICE:** **Vesper**: Will you sing with all of us?
  - > Begin.
    - **Vesper** _(happy)_: Then from the first note.
    - [gauntlet, no healing: the eight singers (`OCTAVE_SINGER` v60) in the order you helped them, each on their Eeveelution's home field, each using its Z-move -> `OCTAVE_VESPER` Vesper (v60), Eevee with the Eevium Z, on `:GRAND_STAGE`]
      - on won:
        - [stage] The last note. Amen sits down in the grass, very pleased with itself. The singers clap, out of time, on purpose.
        - **Vesper** _(happy)_: That was every note we have. You were worth all of them.
        - **Vesper** _(neutral)_: This Eevee was born in the garden this spring. It hasn't decided anything yet. We'd like it to grow up with you.
        - **Vesper** _(neutral)_: And this. We sang over it together: a sliver of Glassfall glass, from the night we lost everything, tuned to every Imprint at once.
        - **Vesper** _(neutral)_: You won't need a cantor's ring for it. That Warden's ring of yours hears it. Its chip is off the Crown's stone, and our glass came out of the night the Crown broke. They know each other.
        - [if `party_has(:EEVEE)`]
          - **Vesper** _(happy)_: It works for Understudy too, if it's still undecided. An Eevee who knows Last Resort and holds that crystal can become everything at once, for a moment.
        - [script]
        - [quest complete]
        - **Vesper** _(happy)_: Whatever it becomes, it'll become it because of you. I said that once before, didn't I?
      - on lost:
        - **Vesper** _(neutral)_: Rest. Sing it again when you're ready. We aren't going anywhere. We never miss a Festival.
  - > Not yet.
    - **Vesper** _(neutral)_: Then we'll wait. We're good at it.

**Scene `after`** (event: `pf_quest_run(:CR_OCTAVE, :after)`)

- **Vesper** _(happy)_: The Octave sings at dusk, here, every day of the Festival. You know all the words now.

#### The Ninth Verse (`CR_OCTAVE_NINTH_VERSE`)

*Chapter 20 · Carol of the Octave, the Glassfall Memorial Garden, Crownhaven (map 489) · rank 1 · 4 points · unlock `switch(155) && octave_helped >= 7`*

Petition, sealed in eight waxes: a singer is writing the Octave's Festival song and needs someone who has met them all.

**Quest log steps:** `ask`: Tell Carol about the other seven singers of the Octave. · `duel`: Carol has every verse but the one in the middle, where the fight goes.

**Reward:** $6000, PPUP x3; +4 pts. **Touches:** The Octave: Carol (always 8 of 8); she sends for Vesper.

**Scene `not_yet`** (event: `pf_quest_run(:CR_OCTAVE_NINTH_VERSE, :not_yet)`)

- [stage] Among the glass figures of the Memorial Garden a young woman in Choir white is writing on a slate, with a Sylveon's ribbons wrapped round her wrist.
- **Carol** _(happy)_: Hello! You're the one Vesper writes about. I'm Carol. I'm the one who never leaves.
- **Carol** _(neutral)_: I'm writing the Octave's song for the Festival. A verse for everyone. But I can only write what I know, and I don't know what happened to them out there.
- **Carol** _(sad)_: Some of them haven't written. Have you met them? These ones I haven't heard about:
- [if `!octave_has(:LYRA)`]
  - *Lyra, in Briarwick.*
- [if `!octave_has(:ARIA)`]
  - *Aria, in Ebbmouth.*
- [if `!octave_has(:CADENCE)`]
  - *Cadence, on the Lowlight steps in Lumen City.*
- [if `!octave_has(:SONA)`]
  - *Sona, at the Temple of the Noon Sun outside Duneholt.*
- [if `!octave_has(:NOCT)`]
  - *Noct, at the ferry steps in Mirefen.*
- [if `!octave_has(:FORTE)`]
  - *Forte, at the Crucible in Cindervault.*
- [if `!octave_has(:LENTO)`]
  - *Lento, on the Mirror Mere past Glassmere.*
- **Carol** _(happy)_: Come back when you've met them all. I'll be here. I'm always here.

**Scene `offer`** (event: `pf_quest_run(:CR_OCTAVE_NINTH_VERSE, :offer)`)

- [stage] Carol, among the glass figures, with her slate. She has written eight titles on it and nothing else.
- **Carol** _(happy)_: You've met them all! Everyone's written about you. Sit down, sit down. Tell me everything, in the order it happened.
- [quest accepted]
- [for each singer you helped, in that order:]
  - Lyra:
    - [continue: verse_lyra]
  - Aria:
    - [continue: verse_aria]
  - Cadence:
    - [continue: verse_cadence]
  - Sona:
    - [continue: verse_sona]
  - Noct:
    - [continue: verse_noct]
  - Forte:
    - [continue: verse_forte]
  - Lento:
    - [continue: verse_lento]
- **Carol** _(neutral)_: That's seven. And me, the eighth: the one with no Plate. Ribbon became a Sylveon because it loved me, and I've always thought that meant I was the one without an Imprint.
- **Carol** _(happy)_: But listening to you, I think the bond is the Imprint. Everyone you met was saved by somebody staying.
- **Carol** _(neutral)_: Every story needs a fight in the middle, though. That's the verse I can't write. Will you help me with that one too?
- [quest step: duel]
- [continue: duel]

**Scene `verse_lyra`** (event: `pf_quest_run(:CR_OCTAVE_NINTH_VERSE, :verse_lyra)`)

- **Carol** _(happy)_: Lyra! 'And the moss came down when no one sang.' Oh, that's good. I'm keeping that.

**Scene `verse_aria`** (event: `pf_quest_run(:CR_OCTAVE_NINTH_VERSE, :verse_aria)`)

- **Carol** _(happy)_: Aria and the river. 'The drowned note rose.' Bersi wrote me eleven pages about that. Eleven.

**Scene `verse_cadence`** (event: `pf_quest_run(:CR_OCTAVE_NINTH_VERSE, :verse_cadence)`)

- **Carol** _(happy)_: Cadence kept her job? Cadence kept a JOB? 'And the lamps stayed lit on Block Nine.'

**Scene `verse_sona`** (event: `pf_quest_run(:CR_OCTAVE_NINTH_VERSE, :verse_sona)`)

- **Carol** _(happy)_: Sona said you'd tell me that. She said you'd tell it well. 'The bell rang at noon.'

**Scene `verse_noct`** (event: `pf_quest_run(:CR_OCTAVE_NINTH_VERSE, :verse_noct)`)

- **Carol** _(neutral)_: Noct doesn't write. Noct sent a lamp wick in an envelope. Now I know what it meant. 'Dark is the only thing that's free.'

**Scene `verse_forte`** (event: `pf_quest_run(:CR_OCTAVE_NINTH_VERSE, :verse_forte)`)

- **Carol** _(happy)_: Forte's letter was all capitals. 'TOO LOUD FOR THE CHOIR.' I'm putting it in exactly like that.

**Scene `verse_lento`** (event: `pf_quest_run(:CR_OCTAVE_NINTH_VERSE, :verse_lento)`)

- **Carol** _(neutral)_: Lento's reflection. 'She said it once.' ...Oh. I'll write that one slowly.

**Scene `duel`** (event: `pf_quest_run(:CR_OCTAVE_NINTH_VERSE, :duel)`)

- **Carol** _(happy)_: Ribbon, the middle of the story. Your favourite part.
- [trainer battle] OCTAVE_SINGER Carol (v50) on `:FAIRY_TALE`
  - on won:
    - **Carol** _(happy)_: And they all lived. That's the whole ending. They all lived.
    - **Carol** _(neutral)_: The song's finished. I have to show Vesper. VESPER!
    - [stage] Carol runs off between the roses. Across the garden, the other seven singers are arriving for the Festival, one by one.
    - [the Octave remembers that you helped Carol: the gauntlet order]
    - [quest complete]
  - on lost:
    - **Carol** _(happy)_: The middle's always the hard part. Try again? I'll keep the ending warm.

**Scene `after`** (event: `pf_quest_run(:CR_OCTAVE_NINTH_VERSE, :after)`)

- **Carol** _(happy)_: We sing it at dusk. You're in every verse, you know. You're the one who stayed.
