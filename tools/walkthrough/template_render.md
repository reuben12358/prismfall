# Pokémon Prismfall — Walkthrough (Prologue to the Festival of Champions)

> A chapter-by-chapter guide in the style of BIGJRA's Reborn, Rejuvenation and Desolation walkthroughs: the order of events, every Pokémon, item and trainer on each map, the big fights with their teams, the side quests and the gym puzzles.
> **Built from the project's own files, not from memory.** Story: `design/CHAPTER_BEATS.md`, `story/04`–`08` (the Act docs), the scripts `story/20`–`26` (Prologue to Ch7, and the withdrawn Ch8 Ring-Day), `10_CHOICES_ENDINGS`, `11_FINALE_LINES`, `12_RUIN_ROUTE`, `14_WAR_AND_BLESSING`, `15_COMEDY`, `NARRATIVE_KEYS`; SPINE Revisions 11–24 win where older text disagrees. Data: the compiled maps in `maps_out/Data` (every item, hidden item, trainer and gift below is read from the built events), `pbs/encounters*.txt`, `pbs/trainers.txt`, `design/maps.json`, `ROUTES.yaml`, `FIELD_DEFAULTS.yaml`, `GYM_PUZZLES.md`, `DUNGEON_PUZZLES.md`, `TRIALS_QUESTS.md`, `EVENT_POKEMON.md`, `BADGE_TIERS.md`, `MEGA_EVOLUTION.md`, `Z_MOVES.md`, `BALANCE.md` and the Core plugin's config.
> **Snapshot:** 2026-11-21. The game is being built chapter by chapter; this guide says what is playable and what is still a plan.

## How to read this walkthrough

Each chapter has the same parts, in the order you meet them:

1. **Key events** (bold): the one or two story turns that make the chapter matter (from `design/CHAPTER_BEATS.md`).
2. **Order of events**: a numbered route through maps, scenes, battles and choices.
3. **Areas**: per map, the wild Pokémon (method, levels, rate), the items and hidden items, the trainers and the map's default field.
4. **Key battles**: rival, Warden, villain and boss teams on Standard, with what changes on Hard and Casual, a field note and a tip.
5. **Side quests**: Trial quests and other optional threads that open this chapter, with rewards.
6. **Gym**: the puzzle and its solution, the badge, the TM, the new level cap and any field move it unlocks.

**Marks used throughout**

| Mark | Meaning |
|---|---|
| ⚑ `:key` | a named choice the game remembers (keys from `10_CHOICES_ENDINGS.md` / `NARRATIVE_KEYS.md`; old chapter prefixes are kept, so `:ch3_juno_talk` is a Chapter 2 choice) |
| ☠ `GO_X` | a story game over, recorded in the cross-save Ledger. Each is warned on screen and has a checkpoint just before it. Finding all 23 unlocks the Ruin Route |
| S1xx / V1xx | story switch / variable (`design/FLAGS.md`), given where a step sets one |
| (x,y) | the tile of an item or event on the built map, so it can be checked in the editor |
| *(planned)* | written in a design doc, not in the game yet |
| *(design only; map not built)* | the map exists only in `design/maps.json` |
| "+4" in an After Badge row | a rare slot added to the map's table once you hold that badge (weight 4 against a table of about 100, so about 4%) |
| Reward shorthand | `RES+1` = Resonance toward Harmony, `RES-2` = toward Ruin; `MERIDIAN+1` / `HOLLOW+1` = Standing; `JUNO+2`, `KESTREL-1` = Bond; `pts` = Trial points |

**What is built (2026-11-21)**

| Chapter | State | What that means |
|---|---|---|
| Prologue, Ch1, Ch2, Ch3 | **Playable** | Maps, events, trainers, gyms, puzzles and the final scripts (`20_SCRIPT_CH0-2.md`, `21_SCRIPT_CH3.md`) are in the build. Some maps still wait for an art pass (the Deepwood 525, the Rimewood 562/563). |
| Ch4 | **Mostly playable** | All Hoar Road maps, Ebbmouth, the Tidelock Gym, K2 and a short Teo scene are built. The final script (`23_SCRIPT_CH4.md`: the strike vote, "The Night the Ebb Stopped", the morning after, Larch's confession) landed on 2026-11-21 and isn't wired into the maps yet. Not built: Gullcry Caves B1F (565), the Reyes Cellar (166), the Overflow Culvert (175). |
| Ch5 | **Scripted; being built** | `24_SCRIPT_CH5.md` (scenes plus a full map-events list). Map builder 15's first Lumen maps (the Concourse, the Lowlight, the Circuit Gym and the Shattered Lowlight) are in the working tree but not committed or scripted yet; the Lock Road isn't built. |
| Ch6 | **Scripted; maps not built** | `25_SCRIPT_CH6.md` (2026-11-21): every scene plus a map-events list; none of the Brass Road or Duneholt maps is built. |
| Ch7 | **Scripted; maps not built** | `26_SCRIPT_CH7.md` (2026-11-21): every scene, with the Ward Night as canon, plus a map-events list; no Leach Road or Mirefen map is built. |
| Ch8–Ch18 | **Design only** | Outline in the Act docs; trainer teams, encounter tables, gym puzzles and Trial quests are designed. Verdance's market terraces, Briar Hall and the cathedral (280–287, 295) are built ahead of Ch10. |
| Ch19 | **Design, with the war theatre built** | The Glass Dunes battle maps (920, 924–926, 928–930) are built with their soldiers and the legendary boss event; Wyrmrest and the rest are design only. |
| Ch20–Ch21 | **Design only** | Every Festival team is in `pbs/trainers.txt`; Crownhaven's maps are not built. |

## Level caps

Prismfall Core enforces a hard cap on every difficulty: past it your Pokémon gain no Exp, Rare Candies stop working, and on Standard and Hard a Pokémon above the cap may disobey. Each Warden's ace is exactly at that gym's cap.

| Badges held | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Cap** | 15 | 19 | 23 | 27 | 31 | 35 | 39 | 43 | 47 | 51 | 55 | 59 | 63 | 67 | 71 | 75 | 80 | 85 | 90 |
| Next Warden | Dorian | Tamsin | Marisol | Rook | Sahar | Corvin | Brann | Kaito | Juno | Anja | Odessa | Ilsa | Bastian | Ysolde | Magnus | Nyx | Celestine | Sigrun | Festival |

**Festival of Champions:** the cap rises with each round to that round's ace: Round of 16 **90**, Quarterfinal **92**, Semifinal **94**, Final **96**, the Hijack and Arceus **100**.

## Difficulty modes

Chosen at the start; Core allows a change at any time (`DIFFICULTY_CHANGE_RULE = :any`). Trainer data uses one team per mode: version *v* is Standard, *v*+100 Hard, *v*+200 Casual (Core falls back to Standard when a variant is missing).

| | Casual | Standard | Hard |
|---|---|---|---|
| Feel (BALANCE §1) | learn the field, win on the second try at worst | fair but demanding: use the field and the matchups; arrive at the cap | Reborn-hard: the field is pointed at you; expect to build counter-teams |
| Teams | one Pokémon fewer (min 2; Festival always 6), 2–4 levels lower, the nastiest tool removed | ace at the cap, the rest 1–5 below; full sets and the field-synergy core | one Pokémon more (max 6), higher IVs and EV spreads, upgraded items and hidden abilities |
| Exp | ×1.5 | ×1.0 | ×1.0 |
| Bag in trainer battles | yes | yes | **no** |
| Battle style | your choice | your choice | Set (forced) |
| Above-cap disobedience | off | on | on |
| Trainer AI | the class's own | the class's own | floor 48 (high skill) |
| Megas on NPCs | as Standard | every important fight from an ace of about Lv 50, plus designed "weak" Megas below that (Brann's Camerupt) | as Standard |

Route and gym trainers follow a simpler rule: Hard +1 level, Casual −1 level, no bag items.

## Fields at a glance

Every battle has a field (SPINE Rev 10). The map's default is given in each **Areas** entry; gyms, bosses and set pieces set their own. Larch's **Field Notes** (key item, Chapter 1) fill in as you meet each one. Full rules: `design/FIELDS.md`.

| Field | The short version | How to play it |
|---|---|---|
| **Meadow** | Grass and Bug ×1.2; the breeze boosts Fairy Wind, Razor Leaf, Silver Wind; stampede moves ×1.2; Cut ×2 | Fire twice (once in sun) sets it ablaze into Wildfire |
| **Beach** | Water and Ground ×1.2; mud moves ×2; focused minds ignore accuracy drops | a big tide (Water ×3 or heavy rain) floods it into Water Surface |
| **The Bleed** | every 3 rounds it borrows another field's full effects; off-type attacks ×1.2 | bring coverage; Protean, Color Change and type-shifting moves shine |
| **Grand Stage** | an audience in three stages (Opening Night, Encore, Standing Ovation): Normal ×1.3–1.5, sound and dance moves ×1.3–1.5, crits raise it; stalling lowers it | keep moving; in Dorian's gym your own fans join in (see Ch2) |
| **Silkwood** | Bug ×1.5, Grass and Fire ×1.2; Electroweb ×1.5, never misses; webs slow the careless | Fire ×3 burns it into Wildfire; rain makes every Electric move ride the silk |
| **Cave** | Rock ×1.5, sound ×1.5; non-contact Flying ×0.5; Stealth Rock doubled | two quakes cave the ceiling in |
| **Hollow Cathedral** | Ghost ×1.5; Ghost and Normal hit each other; Fire also hits as Ghost | holy moves ×3 consecrate it |
| **Snowy Mountain** | Ice ×1.5, Rock and Flying ×1.2; Ice types take less from physical hits; Fire ×0.75 | sun or big Fire melts it to Mountain |
| **Mountain** | Rock ×1.5, Flying ×1.2, wind ×1.3; Tailwind lasts longer | hail or two blizzards bury it in snow |
| **Water Surface** | Water ×1.5; Electric ×1.5 on grounded targets; Fire ×0.5; Ground moves and hazards fail | Dive takes it Underwater; big Ice ×3 freezes it |
| **Neon Grid** | Electric ×1.5, Steel ×1.2; conductors hit as Electric; no sleep | Ground moves and floods black it out |
| **Desert** | Ground and Fire ×1.2; sand abilities always on; Ground types burrow (special ×0.67) | rain wakes a Superbloom; floods make Flooded Dunes; searing Fire makes Glass Dunes |
| **Corrosive Mire** | Poison ×1.5 and hits Steel; Grass and mud also hit as Poison | Misty Terrain or Purify cleans it |
| **Volcanic** | Fire ×1.5; Rock comes out superheated; quakes prime eruptions | big Water or Ice ×2, rain or sand quench it into Cinderglass |
| **Colosseum** | Fighting ×1.2 (×1.5 in a Frenzy); knockouts rally the crowd; mind games booed | three quakes collapse the pit to Cave |
| **Flower Garden** | five growth stages: Grass ×1.1 → ×2.0, Bug and Fire grow too | Fire, blades, frost and acid cut it back |
| **Frozen Lake** | Ice ×1.5; skaters build speed; quakes splinter ice into spikes | Fire or quakes ×3 crack it into Water Surface |
| **Stormfront** | Electric ×1.3, Flying ×1.2, wind ×1.2; Hurricane and Thunder never miss; hazards blow away | Sunny Day ×2 opens a Rainbow |
| **Mindscape** | Psychic ×1.5; Dark and Ghost ×1.2; rooms last longer | Dark moves curdle it to Nightmare; Topsy-Turvy flips it Inverse |
| **Crystal Cavern** | Rock ×1.3; the glow cycles Fire > Water > Grass > Psychic and Rock moves take its type | Dark moves or sand darken it; quakes ×3 make it Cave |
| **Factory** | Steel ×1.5, Electric and Fire ×1.2; Gear Grind ×2 | explosions or quakes ×3 wreck it into Scrapyard |
| **New Moon** | Dark ×1.5; non-Dark moves ×0.9 accurate; light and star moves pierce it | Night Daze deepens it to an Abyss; light relights the lamps |
| **Fairy Tale** | Fairy and Dragon ×1.5, Steel ×1.3; knights, spells and dragonfire | Dragon moves ×3 rouse it into a Dragon's Den |
| **Dragon's Den** | Dragon ×1.5, Fire ×1.3, Water/Ice ×0.7; Dragons armoured (×0.83 taken) | Water/Ice ×3 cool it to Cave; Fairy ×3 tames it |
| **Inverse** | the type chart is reversed; Ghost, Psychic, Dark ×1.2 | Topsy-Turvy returns it to the field it came from |
| **Prism Arena** | the Festival arena: every 3 turns it becomes the next gym field, announced a turn ahead | read the announcement and switch ahead of it |

## Field moves

From Prismfall Core's `FIELD_MOVE_BADGES` (badge counts: "at least N badges").

| Move | Where you get it | Usable from |
|---|---|---|
| Cut (HM01) | the Cutter's House, Briarwick, after Tamsin's badge (Ch3) | 2 badges |
| Rock Smash (TM98) | Salt Miner Ebb in Brinecut Mine, once you hold Dorian's badge (Ch3) | 2 badges |
| Flash (TM70) | Rook Calder, after Gym 4 (Ch5) *(planned)* | 4 badges |
| Strength (HM04) | Duneholt's excavators, after Gym 5 (Ch6) *(planned)* | 5 badges |
| Surf (HM03) | the Mirefen ferrymen, after Gym 6 (Ch7) *(planned)* | 6 badges |
| Fly (HM02) | Odessa Gale lands it at the Ironreach Conclave (Ch9) *(planned)* | 8 badges |
| Rock Climb (TM100) | Rimeholt's ice-climbers, after Gym 10 (Ch11) *(planned)* | 10 badges |
| Waterfall (HM05) | Skyreach's sky-river guides, after Gym 11 (Ch12) *(planned)* | 11 badges |
| Dive (HM06) | Cogsworth's bathysphere works, after Gym 15 (Ch16) *(planned)* | 15 badges |

Rods: Old Rod from Fisherman Odo (Ferrow's Landing, Ch1); Good Rod from the Anglers' Guild (Ebbmouth, Ch4); Super Rod from Rimeholt's ice-fisher (Ch11, *planned*). Mega Evolution and Z-moves share one ring, Bastian's, after Badge 13 (SPINE Revs 21 and 23); stones and crystals found earlier "hum and wait".

## Chapter index

| Ch | Title | Gym (badge) | Cap after | Key events | State |
|---|---|---|---|---|---|
| P | The Last Ferry | — | 15 | the NULL scan; Voss's badge case | playable |
| 1 | Tidewatch | — | 15 | the Glassed Orchard; Larch's journal | playable |
| 2 | Curtain Call | 1 Dorian, Saltmere (Footlight Badge) | 19 | the Mourner hijacks the Pageant; Dorian's banned page | playable |
| 3 | The Weaver's Debt | 2 Tamsin, Briarwick (Weft Badge) | 23 | Tamsin's secret contract; the Glass Matriarch | playable |
| 4 | Both Ways | 3 Marisol, Ebbmouth (Tideturn Badge) | 27 | the Night the Ebb Stopped; Larch's confession | mostly playable |
| 5 | Ten Years of Light | 4 Rook, Lumen City (Arclight Badge) | 31 | the Lowlight Shatter; Valen and the Mandate | scripted, being built |
| 6 | What the Sand Keeps | 5 Sahar, Duneholt (Sandglass Badge) | 35 | the Ossuary murals; K3 and the rumour | scripted, not built |
| 7 | The Quiet Ward | 6 Corvin, Mirefen (Remedy Badge) | 39 | J2 and the ledger; the Ward Night | scripted, not built |
| 8 | The Light Stone | 7 Brann, Cindervault | 43 | the Caldera Crisis; the Light Stone | design |
| 9 | The Iron Conclave | 8 Kaito, Ironreach | 47 | the Mourner unmasked; Teo or the proof | design |
| 10 | The Seat That Blooms | 9 Juno, Verdance | 51 | Juno becomes Warden; the Loyal Three | design (town partly built) |
| 11 | The Thaw | 10 Anja, Rimeholt | 55 | the Thaw and Kyogre; war is declared | design |
| 12 | Dead Letters | 11 Odessa, Skyreach | 59 | the Larch Papers; K5 and the letters | design |
| 13 | Behind the Glass | 12 Ilsa, Lucent | 63 | the Mindscape memory; the tribunal and the Fault | design |
| 14 | The Deep Seams | 13 Bastian, Cragholm | 67 | Bastian's account and the Ring-Day; the badge case opened | design |
| 15 | The Hollow Cathedral | 14 Ysolde, Gravenmoor | 71 | the Cathedral echo; K6 | design |
| 16 | Clear Air | 15 Magnus, Cogsworth | 75 | the Arbiter blueprints and Zekrom; the Sump Purge | design |
| 17 | The Drowned Crown | 16 Nyx, Underveil | 80 | Aurelia; Voss names himself | design |
| 18 | Once Upon a Time | 17 Celestine, Gloaming | 85 | Pecharunt; the Hymn and K7 | design |
| 19 | The Last Gate | 18 Sigrun, Wyrmrest | 90 | Sigrun's oath; the Battle of the Glass Dunes | design (war maps built) |
| 20 | The Festival of Champions | — | 90–94 | the opening ceremony; Valen's audience | design |
| 21 | Sovereign | — | 96–100 | the hijack; Arceus and the final choice | design |

# Act I — The Last Ferry

## Prologue (Ch0) — "The Last Ferry"

*Maps: the Dovetail deck (109) and cabin (110), Ferrow's Landing dock (100). Playable. Script: `story/20_SCRIPT_CH0-2.md`.*

### Key events

- **The NULL scan.** Meridian's new customs gate at the dock reads every passenger's tint. Yours comes back `NULL`. Aurelian Voss calls it a faulty unit and waves you through; the technician, Calla Wren, photographs the screen.
- **Voss's gift.** On the deck, Voss gives you the **Badge Case** and offers a Meridian Fellowship (⚑ `:pro_fellowship`). The case hums every time a badge goes in.

### Order of events

1. A title card (*Spring, AF 300... This is the final civilian crossing*). You start at the port rail of the **Dovetail** with **Mum's Letter** (key item: "Don't let anyone scan you. Don't go to Crownhaven.").
2. Lean on the rail and **Captain Edda Morrow** stomps over ("Do Not Lean", the chapter's comedy scene). She stops mid-shout when she sees your face.
3. *Optional:* talk to the passengers; examine the bow (a **hidden Potion** in the coiled rope); go below to the **cabin** (110): the cook gives **Old Chowder** (restores 20 HP), the bookshelf explains "wilting", and Edda's locked trunk is scratched *"I.A. + child, night crossing, 290"*.
4. Return to the rail: **Aurelian Voss** joins you. You receive the **Badge Case**. ⚑ `:pro_fellowship`: *accept* (Fellowship Card and ₽3000, +Meridian Standing) / *decline* (+Voss Bond: "Independent. Good.") / *say nothing* (he leaves the card on the rail; a Mart clerk can activate it later for the ₽3000). S101 opens the gangway.
5. **Ferrow's Landing dock (100).** Edda waits at the foot of the gangway. ☠ **`GO_HOMEWARD` "Homeward"**: tell her you want to go back, and say so twice. (A joke game over in the first five minutes; it teaches that game overs exist and are recorded.)
6. Walk into the **customs gate**: the bar stays dark, then reads `NULL`, twice. Voss: "Faulty unit. These things hate sea air." S102. The ferry is chained in; the crier announces the Hallow Strait is closed. Title card: **ACT I — THE LAST FERRY**.

### Areas

#### The Dovetail — Deck (109) and Cabin (110)

- **Field:** Water Surface (`:WATER_SURFACE`) (no battles here).
- **Items:** none on the map
- **Hidden items:** Potion (coiled rope, 27,12)
- **Gifts:** Badge Case and (by choice) Fellowship Card from Voss; Old Chowder from the cook (110).
- **Wild Pokémon:** none.

### Side quests

- **Master of Nothing** opens later (Ch1): the Dockmaster's ledger sends you back aboard the Dovetail to find what is still on it (a Wattrel's nest). See Chapter 1.

---

## Chapter 1 — "Tidewatch"

*Maps: Ferrow's Landing (100) and its interiors (101–108), the Ferrymen's Mile (520), Windfall Row (521), the Glassed Orchard (522), the Hale Farmhouse (523). Playable. Script: `story/20_SCRIPT_CH0-2.md`.*

### Key events

- **The Glassed Orchard.** The PC walks through a Bleed Veil that burns everyone else, and a maddened swarm calms when they come near.
- **Larch's journal.** That night: *"Subject reads NULL. Second such reading in my life. The first was in Crownhaven, AF 290. God help us, Ines."*

### Order of events

1. **Ferrow's Landing.** Wenna Hale gives a **Bramble Tart** (restores 30 HP) at her quay stall; Fisherman Odo gives the **Old Rod** at the pier end. The quest log reads *"Mum's Letter: find Imelda Larch at the research station on the headland."*
2. **Tidewatch Station (103).** Larch reads your mother's letter and pours kelp tea (three answers, all flavour). You meet **Juno Hale**.
3. **The starter.** In the Wayfarer Sanctuary, pick **any Gen 1–9 starter** (Lv 5; grouped Grass / Fire / Water). You also get the **Pokédex**. S103. Juno takes the starter weak to yours; **Kestrel Vane** drops out of the hayloft and takes the one strong against it.
4. **K1** outside the station (you may lose). Win: Kestrel Bond +1. Juno names the group "Team Compost". S104.
5. Back inside, **Rowan Ashby** (the Grass Warden, Juno's uncle) is sorting seed trays with a sickly Phantump he found in the Glasswood. He gives a **Miracle Seed** (103) and says "She'd have liked you."
6. **Juno's errand, "Biscuit":** her mother's Skwovet has run into the old Pruett orchard. Juno follows you.
7. **The Ferrymen's Mile (520).** At the first tall grass Juno runs the catching tutorial and gives **Poké Ball ×5**. Youngster Pim and Lass Dory are the first trainers. The road west at the Hale Bell is held by Accord guards until morning.
8. **Windfall Row (521)** to the orchard gate. The forest road north into the Gossamer is corded off: the Glasswood has crossed it.
9. **The Glassed Orchard (522, `:BLEED`).** Juno stops at the Veil ("My skin's burning"). You walk through. ☠ **`GO_ORCHARD` "Two in the Orchard"**: from inside, Juno asks you to pull her through; take her hand. Inside: the **Glassed Wurmple** (wild battle, Lv 6, the first Bleed field and the first Field Notes pop-up; win or flee, it calms), the glass farmhand, a **Glass Apple** (sells for ₽500), and Biscuit on a glass branch (he climbs onto your head).
10. Out through the Veil: **Larch's "Lecture One"** (comedy scene). You receive **Field Notes**. S105, Juno Bond +1.
11. *Optional, evening:* the **Ferrow Lighthouse** (105/106) is unlocked once S105 is on. Hesper Vane drops her lamp-rag when she sees you; the cracked mirror by the door "shows the truth crooked".
12. **Biscuit comes home** at Wenna (the farmhouse 523 or her quay stall): **Oran Berry ×3**. She won't let you sleep at the inn.
13. Sleep in Juno's bed at the **Hale Farmhouse**. Juno's goodnight from the hayloft ("You can see all eighteen from up here tonight"), then the end-of-chapter cutscene: **Larch's journal**. V102 = 2.

### Areas

#### Ferrow's Landing (100)

- **Field:** Beach (`:BEACH`). Interiors: Pokémon Center (101), Mart (102), Tidewatch Station (103), Tidewater Inn (104), Lighthouse 1F and lamp room (105/106), Dockmaster's House (107), Quarantine Customs Hall (108).
- **Wild Pokémon** (the harbour; you can fish from the pier with the Old Rod):

| Method | Pokémon (levels, rate) |
|---|---|
| Surf (Surf from Badge 6) | Tentacool 28–34 (35%), Wingull 28–33 (25%), Finizen 28–33 (15%), Wailmer 28–34 (15%), Pelipper 32–36 (5%), Tentacruel 32–36 (5%) |
| Old Rod | Magikarp 5–10 (60%), Finneon 5–10 (25%), Tentacool 6–10 (15%) |
| Good Rod (Ebbmouth, Ch4) | Krabby 18–24 (30%), Chewtle 18–24 (25%), Arrokuda 18–24 (25%), Wiglett 18–24 (15%), Staryu 20–25 (5%) |
| Super Rod (Rimeholt, Ch11; planned) | Kingler 45–50 (20%), Barraskewda 45–50 (20%), Lumineon 45–50 (20%), Staryu 45–50 (15%), Drednaw 45–50 (15%), Gyarados 46–50 (5%), Mantine 46–50 (5%) |
| **After Badge 1** (added) | Old Rod: Chinchou 13–16 (rare, +5) |
| **After Badge 2** (added) | Old Rod: Horsea 17–20 (rare, +4), Luvdisc 17–20 (rare, +3) |
| **After Badge 3** (added) | Good Rod: Clauncher 21–24 (rare, +4), Skrelp 21–24 (rare, +3) |
| **After Badge 4** (added) | Good Rod: Staryu 25–28 (rare, +3), Shellder 25–28 (rare, +2) |

- **Items:** none on the map
- **Hidden items:** Oran Berry (tart stall, 37,43) · Pearl (breakwater, 52,46)
- **Gifts:** Old Rod (Odo, pier end) · Bramble Tart (Wenna) · Miracle Seed (Rowan, 103) · starter, Pokédex (Larch, 103) · Sharp Beak and Charcoal (the two town quests below).
- **Mart (102):** Potions, Poké Balls and Meridian's new Synthetic Seeds. The clerk activates an unactivated Fellowship Card.

#### The Ferrymen's Mile (520)

- **Field:** Meadow (`:MEADOW`). The Hale Bell stands where the Strand Road turns west (the quarantine roadblock until Chapter 2). The Smuggler's Stair behind the toll booth needs Cut (after Briarwick) and leads to the Ferryman's Rest sea cave.

| Method | Pokémon (levels, rate) |
|---|---|
| Grass (morning / day) | Skwovet 3–5 (20%), Lechonk 3–5 (15%), Lillipup 3–5 (15%), Wooloo 4–6 (13%), Pikipek 4–6 (13%), Yungoos 3–5 (9%), Rookidee 3–5 (8%), Fletchling 4–6 (4%), Rolycoly 4–6 (3%) |
| Grass (night) | Skwovet 3–5 (20%), Hoothoot 3–5 (20%), Nickit 3–5 (15%), Tarountula 3–5 (15%), Lillipup 3–5 (15%), Rattata 3–5 (8%), Spinarak 3–5 (4%), Rolycoly 4–6 (3%) |
| **After Badge 1** (added) | Teddiursa 13–16 (rare, +4), Munchlax 13–16 (rare, +3); night: Zorua 13–16 (rare, +4) |
| **After Badge 2** (added) | Farfetch'd 17–20 (rare, +4), Audino 17–20 (rare, +3); night: Murkrow 17–20 (rare, +3) |
| **After Badge 3** (added) | Swablu 21–24 (rare, +4), Hawlucha 21–24 (rare, +2) |
| **After Badge 4** (added) | Stufful 25–28 (rare, +3), Togepi 25–28 (rare, +2) |
| **Act IV on** (Bleed-spread table, version 1) | Greedent, Oinkologne, Stoutland, Talonflame, Dubwool, Toucannon, Carbink, Minior (Lv 55–60) |

- **Items:** Poké Ball (50,12) · Potion (8,50) · Revive (10,97)
- **Hidden items:** Potion (Under the stile, 10,99) · Potion (hedge maze, 12,59) · Big Pearl (Ferryman's Rest, 8,98)
- **Trainers** (Standard; Hard +1 level, Casual −1):
    - **Youngster Pim**: Bidoof 5
    - **Lass Dory**: Fletchling 5
    - **Youngster Pip**: Lillipup 4, Skwovet 5
    - **Lass Wren**: Pikipek 4, Fletchling 5

#### Windfall Row (521)

- **Field:** Meadow (`:MEADOW`). Six orchards; every tree is a Headbutt tree (the Headbutt tutor is the farmhand in the Hale yard). The cordon west into the Gossamer opens only from the wood's side, after the Glass Matriarch (Ch3).

| Method | Pokémon (levels, rate) |
|---|---|
| Grass (morning / day) | Pidove 5–7 (17%), Bounsweet 5–7 (12%), Smoliv 5–8 (12%), Zigzagoon 5–7 (12%), Gossifleur 5–7 (10%), Fidough 5–7 (9%), Nidoran♀ 5–7 (8%), Nidoran♂ 5–7 (8%), Pidgey 5–7 (5%), Shinx 5–7 (4%), Litleo 6–8 (3%) |
| Grass (night) | Meowth 5–8 (15%), Hoothoot 5–7 (15%), Spinarak 5–7 (15%), Oddish 5–7 (15%), Nidoran♀ 5–7 (10%), Nidoran♂ 5–7 (10%), Poochyena 5–7 (10%), Nymble 5–7 (10%) |
| Headbutt (low trees) | Pineco 5–8 (40%), Combee 5–8 (30%), Burmy 5–8 (20%), Munchlax 6–8 (5%), Cherubi 5–8 (5%) |
| Headbutt (high trees) | Pineco 5–8 (40%), Combee 5–8 (30%), Squawkabilly 6–8 (20%), Aipom 5–8 (10%) |
| **After Badge 1** (added) | Applin 13–16 (rare, +4), Skiddo 13–16 (rare, +3) |
| **After Badge 2** (added) | Eevee 17–20 (rare, +4), Hoppip 17–20 (rare, +3); Headbutt (high): Shuckle 17–20 (rare, +3) |
| **After Badge 3** (added) | Toedscool 21–24 (rare, +4), Pawmi 21–24 (rare, +3) |
| **After Badge 4** (added) | Fomantis 25–28 (rare, +3), Scyther 25–28 (rare, +2) |
| **Act IV on** (Bleed-spread table, version 1) | Carbink, Minior, Glimmora, Boldore, Lilligant, Tsareena, Eldegoss, Arboliva (Lv 55–60) |

- **Items:** Poké Ball (14,36) · Potion (114,46) · Miracle Seed (91,62)
- **Hidden items:** Oran Berry (windfall, 80,20)
- **Trainers** (Standard; Hard +1 level, Casual −1):
    - **Bug Catcher Wim**: Spinarak 6, Combee 7
    - **Picnicker Ada**: Oddish 6, Budew 7
    - **Camper Joss**: Zigzagoon 6, Shinx 7
    - **Bug Catcher Dell**: Caterpie 6, Metapod 7
    - **Picnicker Mae**: Fidough 7, Smoliv 7

#### The Glassed Orchard (522)

- **Field:** The Bleed (`:BLEED`). No random encounters. Scripted battles: **Glassed Wurmple** Lv 6 (blocks the path) and an optional **Wild Carbink** Lv 20 licking a glass tree in the back row (catchable).
- **Puzzle (DUNGEON_PUZZLES D1, "the Chime Rows", optional, 2/10):** examine the wind-chime post at the gate (19,22) to hear low, middle, high. Walk past the cracked glass trees in that order: L (6,8), M (14,12), H (22,6). The glass hedge shatters; behind it is the lost child's satchel with **Bleed Shard #1**. A wrong note just resets (V501).
- **Items:** **Glass Apple** (38,24) · **Bleed Shard** (lost satchel, 38,1) · **Field Notes** (from Larch on the way out).
- After Badge 1, glass hoofprints lead to a **Galarian Ponyta** (quest *The Orchard Sings*, Chapter 2).

#### Hale Farmhouse (523)

- The bed heals you (before S105) and ends the chapter (after it). The yard's farmhand teaches Headbutt.

### Key battles

**K1 — Kestrel, outside Tidewatch Station** (`Prismfall.rival_battle(:RIVAL_KESTREL, "Kestrel", 1, can_lose: true)`, field: none — a tutorial fight)

| Pokémon | Lv | Item | Ability | Moves |
|---|---|---|---|---|
| **Starter**† | 5 | — | (slot 0) | (regenerated for the swapped species) |

*Bag: Potion; IV 12.*

- **Hard:** Starly 5, Starter 5 @Oran Berry
- **Casual:** Starter 3

† The rival's starter is written as the Gen 1 line in PBS; Prismfall Core swaps it at battle start for the same-generation counterpart of your starter (same stage).

*Tip:* he has the type advantage but no move of his type yet (BALANCE §1b); out-trade him with your starter's status move. Losing costs nothing.

**The Glassed Wurmple** (wild, Lv 6, `:BLEED`). The Bleed borrows another field's effects every 3 rounds; there is no penalty for running.

### Side quests
Quests from the Elowen Trial (the Quiet Way) start at the **lantern rope** by the Accord plaque and from townsfolk; the Zenith Trial's kiosk is in the customs hall.

- **The First Lesson** (`EL_FIRST_LESSON`, The Quiet Way; wired (playable)). Brother Teasel, the wayshrine by the Accord plaque (100). Unlock: S103 CH1_STARTER_GOT. Do one kind thing in Ferrow's Landing that nobody asked you to do. Then go back to Brother Teasel. Reward: Oran Berry x2; silent: RES+1; +2 pts.
- **The Tart Thief** (`EL_TART_THIEF`, The Quiet Way; wired (playable)). Wenna Hale, the tart stall on the quay (100). Unlock: S103 CH1_STARTER_GOT. Someone keeps stealing Wenna Hale's bramble tarts. Brother Teasel's note on the lantern: "The thief is hungry, not wicked." Reward: $200, Oran Berry x3; told: KESTREL-1; +2 pts.
- **The Scarecrow Walks** (`EL_SCARECROW`, The Quiet Way; wired (playable)). Coll Hale, the Hale farmhouse (523). Unlock: S103 CH1_STARTER_GOT. Coll Hale's scarecrow keeps moving to a different field. Coll did not build a scarecrow. Reward: spooked: $300; spared: Miracle Seed, RES+1; +2 pts.
- **Master of Nothing** (`EL_MASTER_OF_NOTHING`, The Quiet Way; wired (playable)). the Dockmaster, the Dockmaster's House (107). Unlock: S101 PRO_FERRY_DONE and S103 CH1_STARTER_GOT. The Dockmaster wants to close the Dovetail's ledger properly. Something is still aboard. Reward: Potion x2; +2 pts.
- **Form 7-B** (`ZE_FORM_7B`, The Prize Exchange; wired (playable)). Grant Kiosk P-3NNY, the Quarantine Customs Hall, Ferrow's Landing (108). Unlock: S103 CH1_STARTER_GOT. CALL FOR PROPOSALS #0001: DISPOSAL OF UNCLAIMED LIVESTOCK, CRATE 7-B. BOUNTY: $500. Reward: disposed: $500, MERIDIAN+1; adopted: Potion x2; +2 pts.
- **Captain Edda (the Wingull)** (town quest, after S102): the girl's Wingull, named after the captain, has fled to the lighthouse rocks. Bring it back: **Sharp Beak**.
- **The Lamplighter's Last Round** (town quest): light the six old quay lamps by hand with the **Lamplighter's Taper**: **Charcoal**.

**Event Pokémon this chapter** (`EVENT_POKEMON.md`): **Nickit** Lv 7 (Stakeout), cornered in the station loft at the end of *The Tart Thief* (catchable) · **Sudowoodo** Lv 10 spar during *The Scarecrow Walks* (can't be caught until after Tamsin's badge).

---

## Chapter 2 — "Curtain Call"

*Maps: the Hale Farmhouse (523), the Ferrymen's Mile (520), Lacecliff Walk (527), Marram Down (528), Saltmere: Promenade & Market (140), Harbour & Breakwater (146), Old Town (147), the Lantern Theatre / Pageant Hall (145), the Pell Playhouse (150, 154; Backstage 151–153 after Badge 2). Playable. Script: `story/20_SCRIPT_CH0-2.md`. Gym 1.*

### Key events

- **The Mourner hijacks the Pageant.** On opening night a masked figure steps out of the painted sky: "Ask your Warden why nothing in Verdance ever rots... Ask why the Loyal Three wore poison on their collars." He looks straight at you and goes still.
- **Dorian's banned page and a voice Kestrel knows.** Dorian gives you the prologue of *The Gilded King* ("If heaven will not kneel, we'll build a chain"); outside, Kestrel heard something in the Mourner's voice and runs north.

### Order of events

1. **The send-off** at the farmhouse breakfast table (523, autorun): Larch arrives sleepless and sends you west by the coast ("Saltmere's first"). You receive the **Town Map**. Quest *Eighteen Roads*: earn the first badge in Saltmere. Juno comes as far as Saltmere (forty bramble tarts for the Pageant).
2. **The Hale Bell** on the Ferrymen's Mile (520): the Accord guard lets a challenger through ("older law than the quarantine"). His partner whispers that "the null one" is to be let through "whatever happens", by a white seal from Crownhaven.
3. **Lacecliff Walk (527, `:BEACH`):** three chalk arches. Sit on the **Lacemakers' Bench** with Juno (heals the party). Trainers: Fisherman Bryn, Picnicker Moll, Hiker Dunstan.
4. **Marram Down (528, `:BEACH`):** the **Saltmere Beacon** on the highest dune (the keeper heals once; the first view of the free port). The Pageant's players are camped in their wagons. *Optional:* take the **Sand Shovel** from the prop-mistress and dig out the **Prompter's Box** in the buried barge: **Prompter's Script** (key item; its old page has the Ogre's struck-out last scene) and a **Normal Gem**.
5. **Saltmere (140).** The breakwater boos the Queen's tax-barge away. Juno runs off to deliver the tarts. Meet **Dorian Pell** at the end of the breakwater (146).
6. **Explore Saltmere** (see "The Saltmere audience" under Gym): every named townsperson you talk to takes a seat at your gym battle.
7. **J1** with Juno on the promenade green (140, `:MEADOW`, you may lose): **Oran Berry ×2**. S109.
8. **Gym 1, the Pell Playhouse** (Old Town 147 → lobby 150 → auditorium 154): walk up the aisle (two actors), pull the curtain rope, battle **Dorian**. **Footlight Badge**, **TM42 Facade**, and the troupe's gift **Eevee "Understudy"** (Lv 10). S110. The badge case hums one clear note.
9. **The Lantern Theatre rehearsal** (145): Understudy is cast as Tree Number Three and cut for pacing ("Tree #3", the chapter's comedy scene). The costumier asks Juno which play her blossoms are from. The prop room's Crown has a new, smaller, chipped stone (Crown seed 2 of 3).
10. **Sunset on the breakwater** (146) with salt-caramel. Juno tells you about Aunt Elin, the Bride Tree. ⚑ `:ch3_juno_talk`: *tell her the scan said NULL* (Juno Bond up; she keeps it secret forever) / *deflect* / *say nothing*.
11. **The Pageant** (145, opening night). The Mourner's speech; the Hollow drop banners; a grey-cowled woman cuts the curtain ropes. **Double battle vs two Hollow grunts** (Grand Stage). The Mourner looks at you: "...You." S108.
12. **Backstage: Vesper** of the Eevee Octave kneels to Understudy ("It hasn't decided which Imprint it belongs to yet. Neither have you, I think."). *Optional double battle* vs Vesper and Lyra. This opens **the Eevee Octave** (S190; eight singers to help, one per kingdom).
13. **Dorian's dressing room:** **Gilded King Prologue** (key item).
14. **Outside the theatre: Kestrel**, white-faced: "That's — the way she talks — no." He runs for the North Gate. V114 = 1.
15. **Next morning:** an Elowen herald posts the Queen's notice ("HER free port"); Dorian tears it down. Juno comes with you to Briarwick (forty silk-moth eggs for her uncle). The North Gate opens onto the Grey Saltings. V102 = 3.

### Areas

#### Lacecliff Walk (527)

- **Field:** Beach (`:BEACH`). The shell-gatherers' steps lead down to the big tide-pool (*The Tide-Pool Feud*, after Badge 1).

| Method | Pokémon (levels, rate) |
|---|---|
| Grass (morning / day) | Wingull 8–11 (15%), Pikipek 8–11 (15%), Skwovet 8–11 (12%), Buneary 8–11 (12%), Cutiefly 8–11 (10%), Squawkabilly 9–11 (9%), Minccino 8–11 (9%), Krabby 8–11 (7%), Shellos 8–11 (6%), Hoppip 8–11 (5%) |
| Grass (night) | Hoothoot 8–11 (20%), Skwovet 8–11 (15%), Spinarak 8–11 (15%), Meowth 8–11 (10%), Volbeat 8–11 (10%), Noibat 8–11 (10%), Wingull 8–11 (10%), Krabby 8–11 (10%) |
| Old Rod | Magikarp 8–12 (50%), Wiglett 8–12 (20%), Corphish 8–12 (20%), Finneon 8–12 (10%) |
| Good Rod (Ebbmouth, Ch4) | Corphish 18–24 (35%), Wiglett 18–24 (25%), Krabby 18–24 (20%), Shellder 18–24 (15%), Staryu 20–25 (5%) |
| **After Badge 1** (added) | Binacle 13–16 (rare, +3), Spearow 13–16 (rare, +3) |
| **After Badge 2** (added) | Pyukumuku 17–20 (rare, +3) |
| **After Badge 3** (added) | Wimpod 21–24 (rare, +3) |
| **After Badge 4** (added) | Cramorant 25–28 (rare, +3), Skarmory 25–28 (rare, +2) |

- **Items:** Potion (121,41) · Poké Ball (12,6) · Super Potion (97,48) · Ether (68,33)
- **Hidden items:** Pearl (third arch, 44,10) · Nugget (high down, 126,8) · Shell Bell (the Lost Thread, 73,46) · Pearl (Sea-cave crate 1, 26,44) · Big Pearl (Sea-cave crate 2, 26,46) · Super Potion (Sea-cave crate 3, 30,44)
- **Trainers** (Standard; Hard +1 level, Casual −1):
    - **Fisherman Bryn**: Magikarp 8, Finneon 9, Wingull 9
    - **Picnicker Moll**: Bunnelby 9, Sandygast 10
    - **Hiker Dunstan**: Rolycoly 9, Nacli 10

#### Marram Down (528)

- **Field:** Beach (`:BEACH`). The free port's charter stone stands by the stile ("SALTMERE ANSWERS TO THE ACCORD AND TO NO CROWN").

| Method | Pokémon (levels, rate) |
|---|---|
| Grass (morning / day) | Tandemaus 9–12 (16%), Gossifleur 9–12 (15%), Nymble 9–12 (13%), Wingull 9–12 (12%), Smoliv 9–12 (11%), Kricketot 9–12 (9%), Fidough 9–12 (8%), Nacli 10–12 (4%), Dwebble 10–12 (4%), Bunnelby 9–12 (3%), Silicobra 10–12 (3%), Sandygast 10–12 (2%) |
| Grass (night) | Spinarak 9–12 (18%), Volbeat 9–12 (15%), Nymble 9–12 (12%), Tandemaus 9–12 (12%), Hoothoot 9–12 (12%), Illumise 9–12 (10%), Kricketot 9–12 (10%), Sandygast 10–12 (3%), Silicobra 10–12 (3%), Nacli 10–12 (3%), Dwebble 10–12 (2%) |
| **After Badge 1** (added) | Helioptile 13–16 (rare, +3), Buneary 13–16 (rare, +3) |
| **After Badge 2** (added) | Rolycoly 17–20 (rare, +3), Cacnea 17–20 (rare, +3) |
| **After Badge 3** (added) | Maractus 21–24 (rare, +3) |
| **After Badge 4** (added) | Tropius 25–28 (rare, +2) |

- **Items:** Potion (8,64) · Great Ball (101,18) · Repel (24,24) · Escape Rope (36,15)
- **Hidden items:** Soft Sand (sledge run, 51,64) · Stardust (dune crest, 70,4)
- **Gifts:** Sand Shovel (prop-mistress, 66,46) · Prompter's Script + Normal Gem (the Prompter's Box, 22,59).
- **Trainers** (Standard; Hard +1 level, Casual −1):
    - **Juggler Hounds**: Lillipup 11, Yamper 11
    - **Bird Keeper Lark**: Pikipek 10, Rookidee 11
    - **Pokémon Ranger Sedge**: Dwebble 11, Nacli 11, Wooloo 12

#### Saltmere — Promenade & Market (140), Harbour & Breakwater (146), Old Town (147)

- **Field:** Promenade Beach (`:BEACH`); Harbour Beach (`:BEACH`); Old Town Grand Stage (`:GRAND_STAGE`). Interiors: Pokémon Center (141), Mart (142), Harbour Office (143), Saltwife's House (144), the Lantern Theatre (145), Saltmere Lantern House (148, the Quiet Way).
- **Wild Pokémon** (the salt lagoon, Old Rod):

| Method | Pokémon (levels, rate) |
|---|---|
| Surf (Surf from Badge 6) | Tentacool 28–34 (40%), Wingull 28–33 (30%), Wailmer 28–34 (20%), Pelipper 32–36 (10%) |
| Old Rod | Magikarp 10–14 (60%), Finneon 10–14 (25%), Horsea 10–14 (15%) |
| Good Rod (Ebbmouth, Ch4) | Horsea 18–25 (30%), Shellder 18–25 (30%), Carvanha 18–25 (25%), Chinchou 18–25 (15%) |
| Super Rod (Rimeholt, Ch11; planned) | Seadra 45–50 (30%), Sharpedo 45–50 (25%), Lanturn 45–50 (25%), Shellder 45–50 (20%) |
| **After Badge 1** (added) | Old Rod: Clamperl 13–16 (rare, +3) |
| **After Badge 2** (added) | Old Rod: Finizen 17–20 (rare, +3) |
| **After Badge 3** (added) | Good Rod: Bruxish 21–24 (rare, +3), Mantyke 21–24 (rare, +3) |
| **After Badge 4** (added) | Good Rod: Frillish 25–28 (rare, +3), Dhelmise 25–28 (rare, +2) |


*Promenade (140):*

- **Items:** none on the map
- **Hidden items:** Lemonade (31,39)

*Harbour & Breakwater (146):*

- **Items:** none on the map
- **Hidden items:** Stardust (23,61)

*Old Town (147):* no items on the map.

- **Gifts:** Saltmere Salt (Sella, 144; flavour) · Soothe Bell (*Hound Number Three*) · ₽1500 (*The Inspector's Text*) · Oran Berry ×2 (J1) · TM42, Eevee "Understudy" (Dorian). The script's Gale Post letter at the Pokémon Center (Potion ×2 and a kelp tea bag) is not placed on 141 yet.
- **Mart (142):** stock Potions and Poké Balls; nobody in Saltmere buys Antidotes.

#### Pell Playhouse — Lobby (150) and Auditorium (154): Gym 1

- **Field:** Grand Stage (`:GRAND_STAGE`). Trainers below; the gym guide in the lobby explains the field.
- **Trainers** (Standard; Hard +1 level, Casual −1):
    - **Juggler Florian**: Minccino 10, Spinda 11
    - **Beauty Rosalind**: Skitty 11, Flabébé 11
    - **Juggler Ambrose**: Aipom 11, Lillipup 12

### Key battles

**J1 — Juno, the promenade green** (`:MEADOW`, you may lose; before Gym 1)

| Pokémon | Lv | Item | Ability | Moves |
|---|---|---|---|---|
| Cottonee | 13 | Oran Berry | Prankster | Fairy Wind, Mega Drain, Grassy Terrain, Stun Spore |
| Petilil | 13 | Oran Berry | Own Tempo | Mega Drain, Growth, Aromatherapy, Stun Spore |
| Bounsweet "Sweetpea" | 13 | Oran Berry | Leaf Guard | Razor Leaf, Rapid Spin, Play Nice, Splash |
| **Starter**† | 15 | Oran Berry | (slot 0) | (regenerated for the swapped species) |

*Bag: Potion; IV 12.*

- **Hard:** Cottonee 13 @Oran Berry, Petilil 13 @Oran Berry, Bounsweet 13 @Eviolite, Fidough 13 @Oran Berry, Starter 15 @Oran Berry
- **Casual:** Bounsweet 11 @Oran Berry, Starter 13 @Oran Berry

† The rival's starter is written as the Gen 1 line in PBS; Prismfall Core swaps it at battle start for the same-generation counterpart of your starter (same stage).

*Field note:* Meadow boosts Grass and Bug ×1.2, so her Grass Pokémon hit a little harder; Juno's Grassy Terrain tends it toward a Flower Garden. *Tip:* her starter is the one weak to yours; lead with it.

**Gym 1 — Warden Dorian Pell** (Normal, `:GRAND_STAGE`, single battle, cap 15)

| Pokémon | Lv | Item | Ability | Moves |
|---|---|---|---|---|
| Aipom | 10 | Oran Berry | Pickup | Fake Out, Astonish, Scratch, Tail Whip |
| Minccino | 10 | Oran Berry | Cute Charm | Echoed Voice, Round, Encore, Baby-Doll Eyes |
| Spinda | 11 | Oran Berry | Own Tempo | Teeter Dance, Tackle, Copycat |
| Jigglypuff | 11 | Oran Berry | Cute Charm | Sing, Disarming Voice, Pound, Defense Curl |
| Kecleon | 15 | Sitrus Berry | Color Change | Fury Swipes, Shadow Sneak, Feint, Lick |

*Bag: Potion; IV 12.*

- **Hard:** Aipom 10 @Oran Berry, Minccino 10 @Oran Berry, Spinda 11 @Sitrus Berry, Whismur 12 @Oran Berry, Jigglypuff 11 @Sitrus Berry, Kecleon 15 @Synthetic Seed
- **Casual:** Aipom 8 @Oran Berry, Minccino 8 @Oran Berry, Kecleon 13 @Oran Berry

*Field note:* Grand Stage boosts Normal moves ×1.3 from turn one and builds applause with sound moves, dances, showpieces (Fake Out) and crits; Dorian's whole team is built to raise it. The crowd you gathered decides the starting stage and who basks in it (below). *Tip:* Fighting types are deliberately absent before this gym (SPINE Rev 16) and Ghosts are rare (Sandygast on Marram Down, 2–3%). A Ghost is immune to his Normal moves, but Kecleon carries Shadow Sneak and Lick for exactly that. Keep attacking: Protect, Substitute and Recover lower the applause. Kecleon's Color Change turns it into the type of the last move that hit it, so hit it once and follow up with something that beats that type. Talk to the town first: a full house turns Standing Ovation into your advantage.

**The Pageant — two Hollow grunts** (double battle, Grand Stage, Lantern Theatre)

| Pokémon | Lv | Item | Ability | Moves |
|---|---|---|---|---|
| Nickit | 15 | — | Unburden | (level-up moves) |
| Foongus | 16 | — | Effect Spore | (level-up moves) |

*IV 8.*

- **Hard:** Nickit 15, Foongus 16
- **Casual:** Nickit 14, Foongus 15

| Pokémon | Lv | Item | Ability | Moves |
|---|---|---|---|---|
| Phantump | 15 | — | Natural Cure | (level-up moves) |
| Morelull | 16 | — | Effect Spore | (level-up moves) |

*IV 8.*

- **Hard:** Phantump 15, Morelull 16
- **Casual:** Phantump 14, Morelull 15

**Optional — Vesper and Lyra** (double, Grand Stage, backstage after the Pageant)

Eevee 18 @Oran Berry / Eevee 17 @Oran Berry. Win or lose, it starts the Eevee Octave.

### Side quests

- **The Last Plank** (`EL_LAST_PLANK`, The Quiet Way; wired (playable)). the lantern rope (Brother Teasel's hand), the empty ferry berth (100). Unlock: Badges ≥ 1. Every morning a Timburr carries a plank down to the empty berth and nails it in. Every night the tide takes it. Teasel's note: "Help it finish." Reward: Potion x2; +2 pts.
- **The Tide-Pool Feud** (`EL_TIDE_POOL_FEUD`, The Quiet Way; wired (playable)). Dobbs the shell-gatherer, the shell-gatherers' steps on Lacecliff Walk (527). Unlock: Badges ≥ 1. A Crabrawler and a Clobbopus have been fighting over one rock for three days. The shell-gatherers can't reach the pools. Reward: Super Potion x2; +2 pts.
- **The Borrowed Lanterns** (`EL_LANTERNS`, The Quiet Way; wired (playable)). Sister Hollin, the Saltmere Lantern House (140). Unlock: S103 CH1_STARTER_GOT. The theatre district keeps 'borrowing' the Lantern House's lanterns as props. Five are missing before the Night of Floating. Reward: Silk Scarf; left_one: $400, RES+1; +3 pts.
- **A Hole in the Sky** (`EL_PAINT_LOFT`, The Quiet Way; wired (playable)). Marguerite Fane, the Lantern Theatre paint loft (145). Unlock: Badges ≥ 1 and S108 CH3_PAGEANT_DONE. The Mourner walked straight through the Pageant's painted sky. The scene-painter needs a new backdrop, and a second opinion. Reward: +1 pts.
- **The Sound of Saltmere** (`EL_SOUND_OF_SALTMERE`, The Quiet Way; wired (playable)). Sister Hollin, the Saltmere Lantern House (140). Unlock: Badges ≥ 1; after EL_LANTERNS. A koan: find the sound Saltmere makes when nobody is performing. Reward: +3 pts.
- **The Orchard Sings** (`EL_GLASS_FOAL`, The Quiet Way; wired (playable)). Brother Teasel, the Ferrow's Landing wayshrine (100). Unlock: Badges ≥ 1 and S105 CH1_ORCHARD_DONE. Since your badge, folk on the orchard lane hear chiming at night, like hooves on glass. Reward: Moon Stone; +3 pts.
- **Field Survey: Coastal** (`ZE_FIELD_SURVEY`, The Prize Exchange; wired (playable)). Grant Kiosk P-3NNY, any P-3NNY kiosk (Ferrow's Landing, Saltmere, Ebbmouth) (108). Unlock: S103 CH1_STARTER_GOT. CALL FOR PROPOSALS #0002: RECORD BATTLES ON THREE (3) DIFFERENT FIELDS. DATA IS THE CURRENCY OF THE FUTURE. SO IS CURRENCY. Reward: Exp. Candy S x3; +2 pts.
- **The Eevee Octave** (`CR_OCTAVE`, The Hall of Petitions; wired (playable)). Vesper Lindqvist, backstage at the Lantern Theatre, Saltmere (asked); the Glassfall Memorial Garden, Crownhaven (489) (145). Unlock: . Vesper asked you to look in on the eight singers of the Octave as your road takes you through the kingdoms. Reward: Eevium Z, Eevee Lv 70 (ADAPTABILITY); +5 pts.
- **Hound Number Three** (town quest): the actor's Lillipup ran off to watch "The Pageant of the Pageant" at the Little Lantern in the Old Town (147). Bring it back: **Soothe Bell**.
- **The Inspector's Text** (town quest, after the Pageant, S108): tell the Accord inspector what the Mourner said, or say nobody remembers. Either way: **₽1500**.
- **The Eevee Octave** (`CR_OCTAVE`, starts here; Vesper, S190): help the eight singers as the road goes through their kingdoms (Lyra in Briarwick, Ch3; Aria in Ebbmouth, Ch4; Cadence in the Lowlight, Ch5; Sona in Duneholt, Ch6; Noct in Mirefen, Ch7; Forte in Cindervault, Ch8; Lento at the Mirror Mere, Ch13; Carol in Crownhaven, Ch20). The gauntlet and its reward (an Eevee and the Eevium Z) come in Ch20.

**Event Pokémon this chapter:** **Kecleon** Lv 13 (Protean; the blinking prop lantern in the Lantern Theatre, *The Borrowed Lanterns*) · **Timburr "Plank"** Lv 13 (gift, *The Last Plank*, after Badge 1) · **Crabrawler** or **Clobbopus** Lv 14 (*The Tide-Pool Feud*, after Badge 1: side with one, catch the other) · **Smeargle "Brush"** Lv 14 (gift; your backdrop colours pick its moves) · **Ralts** Lv 13 (gift, *The Sound of Saltmere*) · **Galarian Ponyta** Lv 15 (the Glassed Orchard, *The Orchard Sings*). Fighting types arrive only after Dorian's badge (SPINE Rev 16).

### Gym 1 — the Pell Playhouse (Dorian Pell)

- **Puzzle (1/10, about 2 minutes):** a walk-through in the spirit of Jasmine's HGSS gym. From the lobby (150) go through the doors into the auditorium (154) and up the red aisle. Juggler Florian (11,25) and Beauty Rosalind (13,20) stand in the aisle and battle you; Juggler Ambrose in the side aisle (1,18) is optional. Juno appears in the front row once you've beaten one actor. The house curtain is down: the stagehand tells you to pull the **curtain rope** on the apron (21,11). The curtain flies out, the footlights come up, and Dorian is on stage.
- **The Saltmere audience** (SPINE Rev 19): V313 counts the named Saltmere townsfolk you have talked to (18 of them, once each) plus three seats for finishing Sister Hollin's *The Borrowed Lanterns*. **0–6:** a sparse house; Grand Stage opens at stage 1 (Opening Night). **7–13:** a good house, stage 2 (Encore), your Pokémon bask in the applause too (1/16 HP a round) and Dorian's troupe basks at half. **14+:** a full house, stage 3 (Standing Ovation), only your side basks, only your attacks get the +1 crit stage, and his Sing can miss. The box office sends up ₽150 a head afterwards. (Harness, a realistic Lv 15 team on Standard: 45% / 63% / 73% win rate by house size.)
- **Badge:** the **Footlight Badge**. **TM42 Facade.** **Gift:** Eevee "Understudy" Lv 10.
- **Level cap after:** **19** ("Pokémon up to level nineteen will heed you").
- **Field moves:** none yet; Dorian tells you Briarwick's badge comes with Cut.
- **Mastery, after Badge 2: the Playhouse Backstage** (DUNGEON_PUZZLES D9, optional, 4/10): a chalked door in the stage-left wing (154 (1,9)) opens once you hold Tamsin's badge. See Chapter 3.

---

## Chapter 3 — "The Weaver's Debt"

*Maps: the Grey Saltings (541) with the Brinewife's Rest (542) and Brinecut Mine (544/545), the Dyers' Ford (552), Thistledown Lea (540) and Thistledown Manor (546/547), Gossamer Wood (524) and Woodward's Hut (526), Briarwick (120–126), the Loomhouse Gym (130/131; Upper Lofts 132/134), then the Gossamer Deepwood (525) and Cocoonfall Hollow (548). Playable. Script: `story/21_SCRIPT_CH3.md`. Gym 2.*

### Key events

- **Tamsin's secret contract** (⚑ `:ch2_tamsin`): Briarwick's nineteen-year-old Warden signed Meridian's Lattice contract alone, at night, and the Lattice is feeding the Glasswood. The first Warden with something to hide.
- **The Glass Matriarch** (boss) and ⚑ `:ch2_matriarch`: the first time the efficient choice is the Ruin one.

### Order of events

1. **The Grey Saltings (541).** Salt pans, the boiling-house smoke, the chalk cliff of Brinecut. Trainers: Sailor Morrow, Tuber Pip, Camper Ned. *Optional:* the **Crabrawler Ring** on the mudflat (three wild Crabrawler bouts, Lv 15–16): a bucket with a **King's Rock**.
2. *Optional:* **Brinecut Mine (544/545).** Salt Miner Ebb sees Dorian's badge and gives **TM98 Rock Smash** (usable from Badge 2). The points-and-brine puzzle leads to the **Old Amber** (the first fossil) and a hidden **Nugget** on B1F.
3. **The Dyers' Ford (552).** The River Selvedge runs red, blue and yellow below the vats. A **Meridian Surveyor** plants the orange survey flags that run all the way to the Glasswood; Juno goes quiet at the first one. Trainers: Painter Morwenna, Painter Ash. *Optional:* step the sluice stones **red, blue, yellow** (the Dye Foreman's first hum, not his "correction") to free the white water.
4. **Thistledown Lea (540).** The dead House Thistledown's meadows and the old bridge. Five trainers.
5. *Optional:* **Thistledown Manor (546/547).** The ghost Players are rehearsing. Don't turn your back on the armchairs; play three scenes (right lines, or a ghost battle each). In the attic the matriarch-ghost offers you a place in the company. ☠ **`GO_CURTAIN_CALL` "Curtain Call"**: accept ("Join the company"). Bow out instead: **Spell Tag** and a **Sinistea** (Lv 14) that follows you off the mantel. S176.
6. **Gossamer Wood (524, `:SILKWOOD`).** Silver silk, silk-moths, and the survey flags going in ahead of you. Bug Catcher twins Mo & Jo fight as a pair ("The Warden fights in twos too"). **Woodward's Hut** (526): **Potion ×3** and a bed. The shrine stone has a honey bun left in front of the Ogre, not the hounds. The Bleed Veil to the east is the Glasswood (Cut needed).
7. **Briarwick (120).** Juno runs off to buy silk-moth eggs. **Tamsin Loom** walks into you carrying too much silk, apologises four times and hurries off toward the pylon, not the gym. Meet Guildmistress Hett (the guild ledger is locked) and moth-keeper Alder Finch (fourteen dead moths this week). At the Loyal Three shrine an old barefoot woman (Celestine, unnamed) sings *"...but who was the thief, when the story was told?"*
8. **Night at the pylon: Pallbearer Thistle** (`HOLLOW_THISTLE`, the first admin battle, `:SILKWOOD`, can't flee). She cut the Lantern Theatre's curtain ropes: "Ask her what she signed!" She leaves a **Bark Mask**. S106.
9. **The Loomhouse (130/131), Gym 2.** Tamsin's apology spiral in the lobby ("The Apology Spiral", the comedy scene), then the web Canopy, then **Tamsin** in a double battle. **Weft Badge**, **TM89 U-turn**. The badge case plays a second note in tune with the first ("It's doing a *chord*").
10. **Tamsin's confession** in the loft: Briarwick is bankrupt; she signed for ₽400,000. ⚑ `:ch2_tamsin`: *help her confess* (the guild signs with her and renegotiates a smaller pylon off the grove) / *expose her* at the guild meeting (the contract is torn up; Hollow and Accord Standing up, Meridian down) / *keep her secret* (the pylon is finished; Thistle's cell comes back angrier in Ch10; in Act V Tamsin can't afford to release her Plate). She gives you **Mother Loom's Shuttle**. Quest *The Ringing Wood*.
11. **The Cutter** (125): "No." Then: **HM01 Cut**.
12. *Optional:* the **Upper Lofts** (132, 134) behind Tamsin's ledge: spools, cords and the brass wire, then Granny's Knot.
13. **The Gossamer Deepwood (525),** through the Cut tree. Lantern cocoons and one-way silk. *Optional:* Shelly's cameo (below) and *The Silkthief*.
14. **Cocoonfall Hollow (548, `:BLEED`).** Juno and Tamsin stop at the Veil. Inside: three crystal-silk bridges (the anchors puzzle), then the **Glass Matriarch** boss. ⚑ `:ch2_matriarch`: *stay with it all night* (it calms at dawn; half the grove has gone to glass; Harmony) / *put your hand on it* (the Imprint drains out through you; the grove is saved and the Matriarch is left dull-eyed; Ruin −2). S107, V105 = 1: the Glasswood recedes and the corded forest road to Windfall Row opens as a shortcut home.
15. Outside the Veil, Tamsin names the next Warden (Marisol Reyes, in Ebbmouth), and Juno leaves for Verdance with the hatbox of eggs.
16. **Chapter close.** A child has circled the chip in the Festival poster's Crown: "How do you hurt a crown?" (Crown seed 3 of 3.) The Gale Post desk has Lecture Two, nine pages. The North Gate leads to Spinners' Rise; the last trunk's silk is white with frost. V102 = 4.

### Areas

#### The Grey Saltings (541)

- **Field:** Beach (`:BEACH`). Door: the Brinewife's Rest (542). Secret: the **Drowned Lane** at night, an old cart road to a tidal islet.

| Method | Pokémon (levels, rate) |
|---|---|
| Grass (morning / day) | Nymble 12–15 (13%), Buneary 12–15 (13%), Minccino 12–15 (13%), Crabrawler 12–15 (12%), Tandemaus 12–15 (12%), Squawkabilly 12–15 (12%), Surskit 12–15 (9%), Dwebble 12–15 (4%), Nacli 12–15 (4%), Sandygast 12–15 (4%), Bunnelby 12–15 (4%) |
| Grass (night) | Tarountula 12–15 (17%), Volbeat 12–15 (13%), Spinarak 12–15 (13%), Hoothoot 12–15 (13%), Minccino 12–15 (12%), Tandemaus 12–15 (12%), Illumise 12–15 (8%), Nacli 12–15 (4%), Dwebble 12–15 (4%), Sandygast 12–15 (4%) |
| Surf (Surf from Badge 6) | Tentacool 28–34 (30%), Wingull 28–33 (25%), Shellos 28–33 (25%), Mantyke 28–33 (15%), Gastrodon 33–36 (5%) |
| Old Rod | Magikarp 12–16 (50%), Remoraid 12–16 (30%), Finneon 12–16 (20%) |
| Good Rod (Ebbmouth, Ch4) | Krabby 18–25 (30%), Corphish 18–25 (30%), Remoraid 18–25 (25%), Skrelp 18–25 (15%) |
| Super Rod (Rimeholt, Ch11; planned) | Kingler 45–50 (25%), Crawdaunt 45–50 (25%), Octillery 45–50 (25%), Dragalge 48–52 (15%), Sharpedo 45–50 (10%) |
| Rock Smash (from Badge 2) | Dwebble 14–18 (50%), Nacli 14–18 (30%), Binacle 14–18 (20%) |
| **After Badge 2** (added) | Krabby 17–20 (rare, +4), Ducklett 17–20 (rare, +3) |
| **After Badge 3** (added) | Cramorant 21–24 (rare, +3), Pyukumuku 21–24 (rare, +3) |
| **After Badge 4** (added) | Mareanie 25–28 (rare, +3), Wimpod 25–28 (rare, +2) |

- **Items:** Big Pearl (3,85) · Potion (10,34) · Great Ball (60,12)
- **Hidden items:** Big Pearl (salt-barge wreck, 16,22) · Stardust (the Drowned Lane, 5,82) · Nugget (Brinecut top, 52,6) · Pearl (salt pans, 14,100)
- **Gifts:** King's Rock (the Crabrawler Ring, 45,101).
- **Trainers** (Standard; Hard +1 level, Casual −1):
    - **Sailor Morrow**: Finneon 15, Remoraid 15, Crabrawler 15
    - **Tuber Pip**: Surskit 14, Minccino 15
    - **Camper Ned**: Bunnelby 14, Nacli 15

#### Brinecut Mine 1F (544) and B1F (545)

- **Field:** Cave (`:CAVE`). B1F is dark: light the lamps.
- **Puzzle (DUNGEON_PUZZLES D4, "points and brine", 3/10):** the depot cart follows three points levers P1–P3. Ride with P1 left to the blind drift, crawl through under the chalk X, throw P2 in the points gallery, drop down the rib's ledge, throw P1 and ride again: the cart stops at the ladder to B1F (end B). On B1F the pump wheel drains the salt lake only while the cart is parked at B, which opens the path to the Old Amber.

*1F:*

| Method | Pokémon (levels, rate) |
|---|---|
| Cave | Zubat 12–15 (18%), Whismur 12–15 (15%), Woobat 12–15 (13%), Machop 13–16 (13%), Timburr 13–16 (13%), Meditite 13–16 (8%), Varoom 13–16 (8%), Nacli 12–16 (4%), Roggenrola 12–16 (4%), Diglett 12–15 (4%) |
| Rock Smash (from Badge 2) | Nacli 14–18 (45%), Roggenrola 14–18 (30%), Shuckle 15–18 (15%), Klawf 16–18 (5%), Geodude 14–18 (5%) |
| **After Badge 2** (added) | Drilbur 17–20 (rare, +4), Carbink 17–20 (rare, +2) |
| **After Badge 3** (added) | Bronzor 21–24 (rare, +3), Glimmet 21–24 (rare, +3) |
| **After Badge 4** (added) | Stonjourner 25–28 (rare, +2) |

- **Items:** Hard Stone (4,5) · Escape Rope (37,29) · Ether (43,34)
- **Hidden items:** Revive (45,13)
- **Gift:** TM98 Rock Smash (Salt Miner Ebb, 7,30; once you hold Dorian's badge).
- **Trainers** (Standard; Hard +1 level, Casual −1):
    - **Hiker Bram**: Geodude 14, Roggenrola 15, Nacli 15
    - **Black Belt Taro**: Machop 15, Timburr 16
    - **Black Belt Saul**: Machop 16, Crabrawler 17

*B1F:*

| Method | Pokémon (levels, rate) |
|---|---|
| Cave | Zubat 14–17 (14%), Woobat 14–17 (12%), Machop 14–17 (12%), Timburr 14–17 (12%), Sableye 15–17 (12%), Mawile 15–17 (12%), Whismur 14–17 (10%), Meditite 14–17 (8%), Nacli 14–17 (4%), Aron 14–17 (4%) |
| Surf (Surf from Badge 6) | Barboach 30–35 (50%), Wooper 30–35 (30%), Quagsire 32–36 (20%) |
| **After Badge 2** (added) | Onix 17–20 (rare, +3), Tinkatink 17–20 (rare, +3), Nosepass 17–20 (rare, +3) |
| **After Badge 3** (added) | Carkol 21–24 (rare, +3) |
| **After Badge 4** (added) | Naclstack 25–28 (rare, +2) |

- **Items:** Old Amber (32,14) · Super Potion (37,26)
- **Hidden items:** Nugget (31,17)
- **Trainers** (Standard; Hard +1 level, Casual −1):
    - **Hiker Gorse**: Aron 16, Nosepass 17
    - **Hiker Holt**: Roggenrola 16, Nacli 16, Woobat 17

#### The Dyers' Ford (552)

- **Field:** Meadow (`:MEADOW`). The sluice stones are at (49,18) red, (51,18) blue, (53,18) yellow (V602). A Pecha berry tree; the shrine of the Fourth Colour.

| Method | Pokémon (levels, rate) |
|---|---|
| Grass (morning / day) | Flabébé 12–15 (18%), Cottonee 12–15 (14%), Azurill 12–15 (12%), Sentret 12–15 (10%), Bidoof 12–15 (10%), Surskit 12–15 (8%), Ducklett 12–15 (8%), Skiddo 12–15 (8%), Smoliv 12–15 (8%), Mareep 12–15 (4%) |
| Grass (night) | Volbeat 12–15 (15%), Illumise 12–15 (15%), Oddish 12–15 (15%), Hoothoot 12–15 (12%), Spinarak 12–15 (10%), Kricketot 12–15 (10%), Morelull 12–15 (10%), Bidoof 12–15 (8%), Mareep 12–15 (5%) |
| Surf (Surf from Badge 6) | Marill 28–33 (40%), Ducklett 28–33 (30%), Psyduck 28–34 (20%), Azumarill 30–35 (10%) |
| Old Rod | Magikarp 12–15 (45%), Goldeen 12–15 (30%), Basculin 12–15 (25%) |
| Good Rod (Ebbmouth, Ch4) | Goldeen 18–24 (35%), Basculin 18–24 (35%), Poliwag 18–24 (20%), Chewtle 18–24 (5%), Barboach 18–24 (5%) |
| Super Rod (Rimeholt, Ch11; planned) | Seaking 45–50 (35%), Basculin 45–50 (35%), Whiscash 45–50 (15%), Poliwhirl 45–50 (15%) |
| **After Badge 2** (added) | Wooper 17–20 (rare, +3), Smeargle 17–20 (rare, +3) |
| **After Badge 3** (added) | Lotad 21–24 (rare, +3), Spritzee 21–24 (rare, +3) |
| **After Badge 4** (added) | Flaaffy 25–28 (rare, +3), Dewpider 25–28 (rare, +2) |

- **Items:** TM44 Rest (57,3) · Potion (10,50) · Super Potion (69,45)
- **Hidden items:** Antidote (base of the third flag, 44,3)
- **Trainers** (Standard; Hard +1 level, Casual −1):
    - **Painter Morwenna**: Ledyba 15, Litleo 16
    - **Painter Ash**: Oddish 15, Marill 16

#### Thistledown Lea (540)

- **Field:** Meadow (`:MEADOW`). Secret: the **Ha-ha**, a sunken wall round the manor hill (a hidden Rare Bone in its ditch).

| Method | Pokémon (levels, rate) |
|---|---|
| Grass (morning / day) | Flabébé 10–13 (12%), Doduo 10–13 (12%), Sentret 10–13 (12%), Sunkern 10–13 (12%), Bidoof 11–13 (10%), Spearow 10–13 (10%), Cottonee 10–13 (10%), Mankey 11–14 (8%), Pancham 11–14 (6%), Ponyta 11–14 (4%), Blitzle 11–14 (4%) |
| Grass (night) | Stunky 10–13 (10%), Purrloin 10–13 (10%), Mankey 11–14 (10%), Hoothoot 10–13 (10%), Oddish 10–13 (10%), Venonat 10–13 (10%), Kricketot 10–13 (10%), Patrat 10–13 (10%), Morelull 10–13 (10%), Snubbull 10–13 (10%) |
| Surf (Surf from Badge 6) | Psyduck 28–34 (40%), Buizel 28–33 (25%), Marill 28–33 (20%), Floatzel 32–36 (10%), Golduck 33–36 (5%) |
| Old Rod | Magikarp 10–14 (60%), Goldeen 10–14 (35%), Tympole 10–14 (5%) |
| Good Rod (Ebbmouth, Ch4) | Goldeen 18–24 (40%), Basculin 18–24 (25%), Chewtle 18–24 (20%), Poliwag 18–24 (10%), Barboach 18–24 (5%) |
| Super Rod (Rimeholt, Ch11; planned) | Seaking 45–50 (30%), Whiscash 45–50 (30%), Drednaw 45–50 (20%), Gyarados 46–50 (10%), Basculin 45–50 (10%) |
| **After Badge 2** (added) | Deerling 17–20 (rare, +4), Hoppip 17–20 (rare, +3); night: Misdreavus 17–20 (rare, +3) |
| **After Badge 3** (added) | Tauros 21–24 (rare, +3), Girafarig 21–24 (rare, +3) |
| **After Badge 4** (added) | Bouffalant 25–28 (rare, +3), Riolu 25–28 (rare, +1) |

- **Items:** Super Potion (118,27) · Poké Ball (4,34) · Great Ball (70,52)
- **Hidden items:** Great Ball (under the bridge, 26,59) · Rare Bone (the Ha-ha, 86,3)
- **Trainers** (Standard; Hard +1 level, Casual −1):
    - **Picnicker Edie**: Oddish 16, Budew 16, Smoliv 17
    - **Picnicker Bryony**: Flabébé 15, Cottonee 16, Sunkern 16
    - **Fisherman Hale**: Magikarp 15, Goldeen 16, Tympole 16
    - **Twins Bel & Bea** (double): Mankey 16, Pancham 16
    - **Youngster Corin**: Sentret 15, Bidoof 16, Doduo 17

#### Thistledown Manor (546) and Attic (547)

- **Field:** Hollow Cathedral (`:HOLLOW_CATHEDRAL`). Optional haunted house.
- **Puzzle (DUNGEON_PUZZLES D5, "don't turn your back", 3–4/10):** after each step, an armchair strictly behind you and more than a tile away creeps one tile toward you; one that reaches you starts a ghost battle (Gastly, Shuppet or Duskull, Lv 15) and resets the room. **Stair hall:** sidestep early and pass the chair with a clear tile between you. **Portrait gallery:** set the portraits in the curtain-call order from Rosamund's diary (the Fool, Laertes, Rosamund, the Old King = wall positions 3, 1, 4, 2); first walk down past the east case and back up so the wedged chair follows you into the east alcove. **Dining room:** draw both chairs out of the nook, lead each over a trapdoor, then pull the cord.
- **The three scenes** (a wrong line starts a ghost battle): "I will remember you." · "...much, methinks." · "Alas, poor Yamask. I knew him." The scene ghosts are Gastly, Misdreavus and Duskull (Lv 13).

| Method | Pokémon (levels, rate) |
|---|---|
| Cave | Shuppet 12–15 (20%), Greavard 12–15 (18%), Phantump 12–15 (15%), Duskull 13–16 (15%), Sinistea 13–16 (12%), Gastly 12–15 (12%), Misdreavus 13–16 (8%) |
| **After Badge 2** (added) | Litwick 17–20 (rare, +3) |
| **After Badge 3** (added) | Honedge 21–24 (rare, +3) |
| **After Badge 4** (added) | Drifloon 25–28 (rare, +2) |

*Manor (546):*

- **Items:** Cleanse Tag (16,35)
- **Hidden items:** none

*Attic (547):*

- **Items:** Spell Tag (19,5)
- **Hidden items:** none
- **Gifts:** Spell Tag and Sinistea Lv 14 (Lady Thistledown, when you bow out). **Wild:** a Greavard (Lv 16) digging in the attic.
- **Trainers** (Standard; Hard +1 level, Casual −1):
    - **Channeler Mireille**: Gastly 16, Shuppet 16, Sinistea 17

#### Gossamer Wood (524)

- **Field:** Silkwood (`:SILKWOOD`). The Weft Bridge and Woodward's Hut (526). South: the Accord cordon on the forest road to Windfall Row (open once V105 ≥ 1). East: the Deepwood (Cut). Secret: the **Unpicked Seam**, a silk wall that opens only at night (*The Horn and the Pincer*).

| Method | Pokémon (levels, rate) |
|---|---|
| Grass (morning / day) | Caterpie 7–9 (12%), Weedle 7–9 (12%), Scatterbug 7–9 (10%), Wurmple 7–9 (10%), Blipbug 7–10 (8%), Sewaddle 8–10 (8%), Cutiefly 8–10 (8%), Shroomish 8–10 (8%), Petilil 8–10 (8%), Seedot 8–10 (5%), Budew 8–10 (4%), Grubbin 8–10 (4%), Sizzlipede 8–10 (3%) |
| Grass (night) | Spinarak 7–10 (15%), Venonat 8–10 (15%), Tarountula 7–9 (12%), Hoothoot 8–10 (10%), Morelull 8–10 (10%), Foongus 8–10 (10%), Kricketot 7–9 (10%), Oddish 8–10 (10%), Phantump 9–11 (5%), Sizzlipede 8–10 (3%) |
| Headbutt (low trees) | Pineco 8–10 (40%), Burmy 8–10 (30%), Karrablast 8–10 (15%), Shelmet 8–10 (15%) |
| Headbutt (high trees) | Combee 8–10 (45%), Pineco 8–10 (33%), Burmy 8–10 (16%), Heracross 9–11 (3%), Pinsir 9–11 (3%) |
| **After Badge 2** (added) | Joltik 17–20 (rare, +4), Venipede 17–20 (rare, +3) |
| **After Badge 3** (added) | Scyther 21–24 (rare, +3), Surskit 21–24 (rare, +3) |
| **After Badge 4** (added) | Bramblin 25–28 (rare, +3), Larvesta 25–28 (rare, +2) |
| **Act IV on** (Bleed-spread table, version 1) | Galvantula, Leavanny, Vikavolt, Centiskorch, Ribombee, Orbeetle, Lokix, Spidops (Lv 56–61) |

- **Items:** TM19 Giga Drain (78,14) · Repel (8,82) · Potion (74,50) · Ether (33,36)
- **Hidden items:** Net Ball ×2 (18,12)
- **Gifts:** Potion ×3 (the Woodward, 526).
- **Trainers** (Standard; Hard +1 level, Casual −1):
    - **Twins Mo & Jo** (double): Karrablast 17, Shelmet 17
    - **Bug Catcher Tobin**: Spinarak 17, Venonat 18
    - **Bug Catcher Reed**: Dottler 16, Grubbin 17
    - **Aroma Lady Petra**: Cutiefly 16, Petilil 17, Budew 17
    - **Camper Bram**: Nuzleaf 16, Shroomish 17, Sizzlipede 18

#### Briarwick (120)

- **Field:** Silkwood (`:SILKWOOD`). Interiors: Pokémon Center (121; the Gale Post desk: **Potion ×2** and a second kelp tea bag), Mart (122), Weavers' Guildhall (123), Treetop House (124, with the chapel mural), Cutter's House (125), Briarwick Lantern House (126, the Quiet Way). No wild Pokémon.

- **Items:** none on the map
- **Hidden items:** X Attack (rope bridge, 28,21) · Tiny Mushroom (dye vats, 14,38)
- **Gifts:** Bark Mask (Thistle) · Dusk Petal (the shrine, after Tamsin's badge) · Silk Scarf (*Sixteen Sleeves*) · Ledger Key, TM String Shot (*The Locked Ledger*) · Mother Loom's Shuttle (Tamsin) · HM01 Cut (the Cutter).
- **Battles:** Pallbearer Thistle at the pylon (63,30), at night (see Key battles).

#### Loomhouse Gym — Lobby (130), the Canopy (131), Upper Lofts (132, 134)

- **Field:** Silkwood (`:SILKWOOD`).

*Lobby (130):*

- **Items:** Potion (17,7)
- **Hidden items:** none

*The Canopy (131):*

- **Trainers** (Standard; Hard +1 level, Casual −1):
    - **Gentleman Bram**: Venonat 16, Sewaddle 17
    - **Bug Catcher Nell**: Sewaddle 15, Spinarak 16
    - **Lass Orla**: Ledyba 15, Vivillon 16

*Upper Lofts (132, optional after the badge):*

- **Items:** Silver Powder (11,5)
- **Hidden items:** none
- **Trainers** (Standard; Hard +1 level, Casual −1):
    - **Bug Catcher Hollis**: Spidops 20, Spinarak 20
    - **Pokémon Ranger Ash**: Dottler 20, Beautifly 21
- **Granny's Knot (134):** the chest holds **Telluric Seed ×2** and a **Silk Scarf**.

#### Gossamer Deepwood (525)

- **Field:** Silkwood (`:SILKWOOD`). Cut required; after Tamsin's badge.
- **Puzzle (D2, "silk leans one way", 2/10):** silk curtains let you through only the way their threads lean. Touch post **α** (25,7) first, then post **β** (33,9) inside the thicket: cocoons 1 and 3 light, their curtains flip, and the island (the Silver Powder and TM19) opens.

| Method | Pokémon (levels, rate) |
|---|---|
| Grass | Yanma 10–12 (12%), Ledyba 10–12 (12%), Deerling 10–12 (12%), Paras 10–12 (12%), Kricketot 10–12 (11%), Rellor 10–12 (11%), Skiddo 10–12 (11%), Scyther 11–13 (5%), Pinsir 11–13 (5%), Eevee 10–12 (5%), Nincada 10–12 (4%) |
| Surf (Surf from Badge 6) | Surskit 28–33 (40%), Lotad 28–33 (30%), Lombre 30–35 (20%), Masquerain 32–36 (10%) |
| Old Rod | Magikarp 8–12 (50%), Poliwag 8–12 (30%), Goldeen 8–12 (20%) |
| Good Rod (Ebbmouth, Ch4) | Poliwag 18–24 (40%), Goldeen 18–24 (30%), Basculin 18–24 (20%), Lotad 18–24 (10%) |
| Super Rod (Rimeholt, Ch11; planned) | Poliwhirl 45–50 (30%), Seaking 45–50 (30%), Basculin 45–50 (25%), Lombre 45–50 (15%) |
| **After Badge 3** (added) | Tangela 21–24 (rare, +3), Fomantis 21–24 (rare, +3) |
| **After Badge 4** (added) | Phantump 25–28 (rare, +3), Shiinotic 25–28 (rare, +2) |

- **Items:** Silver Powder (35,5) · Great Ball (3,5) · Ether (16,6) · TM19 Giga Drain (31,2)
- **Hidden items:** Super Potion (40,31) · Tiny Mushroom (fern bank, 5,29)
- **Gifts:** Silver Powder and TM Struggle Bug (Shelly, 15,26). **Wild:** the glassed Masquerain (Lv 14) at Shelly's dew-pond.
- **Trainers** (Standard; Hard +1 level, Casual −1):
    - **Bug Catcher Linden**: Nincada 19, Ledian 19, Rellor 20
    - **Poké Maniac Ferris**: Paras 19, Nincada 19, Yanma 20
    - **Pokémon Ranger Sorrel**: Deerling 19, Skiddo 20

#### Cocoonfall Hollow (548)

- **Field:** The Bleed (`:BLEED`). Through the crystal silk at the Deepwood's east mouth (opens once `:ch2_tamsin` is chosen).
- **Puzzle (D3, "the shuttle re-threads", 2/10):** three anchors each flip two of the three crystal bridges (a: the TM81 cocoon-house, b: the Shard house, c: the Matriarch's nest). Bridges a and b start taut, so **visit both houses first**, then pull an anchor that tightens c (it slackens a or b; you can never have all three).

| Method | Pokémon (levels, rate) |
|---|---|
| Grass | Dewpider 14–17 (13%), Snom 14–17 (12%), Volbeat 14–17 (10%), Illumise 14–17 (10%), Skorupi 14–17 (10%), Rellor 14–17 (10%), Nymble 14–17 (10%), Durant 15–17 (8%), Shuckle 15–17 (6%), Joltik 14–17 (5%), Nincada 14–17 (4%), Larvesta 16–17 (2%) |
| **After Badge 3** (added) | Bergmite 21–24 (rare, +3), Carbink 21–24 (rare, +2) |
| **After Badge 4** (added) | Cryogonal 25–28 (rare, +3), Charjabug 25–28 (rare, +2) |

- **Items:** TM81 X-Scissor (25,6)
- **Hidden items:** none

### Key battles

**Pallbearer Thistle** (`HOLLOW_THISTLE`, Briarwick's pylon at night, `:SILKWOOD`, can't flee)

| Pokémon | Lv | Item | Ability | Moves |
|---|---|---|---|---|
| Dustox | 16 | Oran Berry | Shield Dust | Gust, Struggle Bug, Poison Powder, Confusion |
| Foongus | 17 | Oran Berry | Effect Spore | Mega Drain, Stun Spore, Growth, Astonish |
| Phantump "Lowmarsh" | 18 | Sitrus Berry | Natural Cure | Branch Poke, Astonish, Leech Seed, Will-O-Wisp |

*Bag: Super Potion; IV 12.*

- **Hard:** Dustox 16 @Oran Berry, Whirlipede 17 @Oran Berry, Foongus 17 @Oran Berry, Phantump 18 @Sitrus Berry
- **Casual:** Dustox 14 @Oran Berry, Phantump 16 @Sitrus Berry

*Field note:* her team is built for the silk: Bug moves ×1.5 and Grass ×1.2. *Tip:* Fire and Flying both hit all three super-effectively. Fire is scarce before Tamsin by design, so a bird (Pidove, Rookidee, Fletchling) is the practical answer; a Fire move here is ×1.2 on top of the type bonus.

**Gym 2 — Warden Tamsin Loom** (Bug, `:SILKWOOD`, **double battle**, cap 19)

| Pokémon | Lv | Item | Ability | Moves |
|---|---|---|---|---|
| Joltik | 14 | Oran Berry | Compound Eyes | Electroweb, Absorb, String Shot, Fury Cutter |
| Surskit | 15 | Oran Berry | Swift Swim | Rain Dance, Water Gun, Struggle Bug, Quick Attack |
| Dwebble | 16 | Oran Berry | Sturdy | Smack Down, Rock Tomb, Bug Bite, Fury Cutter |
| Swadloon "Bobbin" | 19 | Telluric Seed | Overcoat | Razor Leaf, Bug Bite, Struggle Bug, Protect |

*Bag: Super Potion; IV 12.*

- **Hard:** Joltik 14 @Focus Sash, Surskit 15 @Damp Rock, Vivillon 18 @Silver Powder, Dwebble 16 @Sitrus Berry, Swadloon 19 @Eviolite
- **Casual:** Joltik 12 @Oran Berry, Surskit 13 @Oran Berry, Swadloon 17 @Oran Berry

*Field note:* the lead pair sets up **Rain Dance** so the wet silk carries **Electroweb** (spread, ×1.5 on Silkwood, never misses, and every Electric move rides wet silk ×1.2). Dwebble is her answer to birds (Smack Down, Rock Tomb). *Tip:* take out the Joltik first; Fire or Flying spread moves are ideal, and three Fire moves burn Silkwood into Wildfire, which rain then douses. Swadloon "Bobbin" holds a Telluric Seed.

**Boss — the Glass Matriarch** (Galvantula, multi-bar, `:BLEED`, Cocoonfall Hollow; `mapgen/bosses.yaml`)

- **Standard:** Lv 20, 2 bars, Electroweb / Bug Bite / String Shot / Screech; HP ×1.1, Def and Sp. Def ×1.15. **Hard:** Lv 22, 3 bars, Electroweb / Bug Buzz / Sticky Web / Thunder Wave. **Casual:** Lv 18, 2 bars, Absorb instead of Screech.
- **At the first bar break** it "re-strings the nest": Defense +1, and the Bleed borrows **Silkwood** for 3 rounds (Electroweb ×1.5 and sure-hit, Bug ×1.5). Plan to break the bar when you can tank three rounds of that, or switch to a Ground type (immune to Electroweb) for the window.
- *(If the boss plugin isn't loaded, the event falls back to a plain Lv 16 Galvantula.)*

**Optional — Shelly** (cameo, `FESTIVAL_SHELLY` v1, **double**, `:SILKWOOD`, the Deepwood dew-pond)

| Pokémon | Lv | Item | Ability | Moves |
|---|---|---|---|---|
| Masquerain | 20 | Sitrus Berry | Intimidate | Struggle Bug, Bubble Beam, Quick Attack, Sticky Web |
| Joltik | 20 | Oran Berry | Compound Eyes | Electroweb, Struggle Bug, Bug Bite, Thunder Wave |
| Larvesta | 21 | Oran Berry | Flame Body | Flame Charge, Struggle Bug, Leech Life, String Shot |
| Scyther | 21 | Eviolite | Technician | Fury Cutter, Wing Attack, Quick Attack, Focus Energy |

*Bag: Super Potion; IV 12.*

- **Hard:** Masquerain 20 @Sitrus Berry, Joltik 20 @Oran Berry, Araquanid 21 @Sitrus Berry, Larvesta 21 @Oran Berry, Scyther 21 @Eviolite
- **Casual:** Masquerain 18 @Sitrus Berry, Larvesta 19 @Oran Berry, Scyther 19 @Eviolite

*Tip:* a Bug core with Scyther and Larvesta at Lv 20–21; bring Rock or Fire spread moves (Larvesta resists Fire, so Rock is safer).

### Side quests

- **Three Loyal, Three Knots** (`EL_THREE_KNOTS`, The Quiet Way; wired (playable)). Mother Aldreth, the Briarwick Lantern House (120). Unlock: Badges ≥ 1. A pilgrimage: re-tie the silk knots at the three wayshrines of the Loyal Three, and answer what each shrine asks. Reward: Magical Seed x2; +3 pts.
- **The Horn and the Pincer** (`EL_HORN_AND_PINCER`, The Quiet Way; wired (playable)). the lantern rope (no one signed it), the sap tree on the old trail, Gossamer Wood (524). Unlock: Badges ≥ 2. Two great Bug Pokémon are fighting over the sap tree on the old trail. The trail has been blocked for a week. Reward: Honey x2; +2 pts.
- **The Silkthief** (`EL_SILKTHIEF`, The Quiet Way; wired (playable)). Hett, the Weavers' Guildhall (123). Unlock: Badges ≥ 2. Somebody is stealing finished silk straight off the drying racks at night. Hett has a theory, and it has eight legs. Reward: $800; guardian: Silver Powder, RES+1; +3 pts.
- **The Moss Hymn** (`EL_OCTAVE_MOSS`, The Quiet Way; wired (playable)). Lyra of the Octave, under the Lantern House tree, Briarwick; the moss-stone in Gossamer Wood (524) (120). Unlock: Badges ≥ 1. A singer of the Octave has been singing to her Eevee for three days. It will not come down from the moss-stone in Gossamer Wood. Reward: $800, Big Root; +3 pts.
- **Someone Apologising to Bugs** (`EL_SHELLY`, The Quiet Way; designed (not wired yet)). Mother Aldreth, the Briarwick Lantern House (120). Unlock: Badges ≥ 2. A stranger with pink hair is lost in the Gossamer Deepwood, apologising to the Bug Pokemon. The spirits of the wood are uneasy. Reward: Silver Powder; +3 pts.
- **Sixteen Sleeves** (town quest): bring the knitting grandmother three **Tiny Mushrooms** (one is hidden behind Briarwick's dye vats): **Silk Scarf**.
- **The Locked Ledger** (town quest, Hett): the ledger key is tied into the first warp thread of Mother Loom's first loom in the gym lobby (130 (6,7)). The ledger in the Guildhall loft shows one signature. Reward after the chapter: **₽2000** and **TM String Shot**; Tamsin's confession opens differently if you read it first.
- **Lost in the Gossamer** (cameo, Shelly; CAMEOS §1): see Key battles. S181.
- **The Eevee Octave, singer 1 of 8: Lyra** (*The Moss Hymn* above): her duel in Gossamer Wood is Skiddo 17 @Oran Berry, Leafeon 18 @Oran Berry (Silkwood).

**Event Pokémon this chapter:** **Heracross** or **Pinsir** Lv 19 (Moxie; the sap tree on the old trail, after Badge 2: side with one, fight and catch the other) · **Spidops "Silkthief"** Lv 20 (boss, then it joins; *The Silkthief*) · **Sinistea** Lv 14 (Thistledown Manor) · **Leafeon "Moss"** is Lyra's (a duel, not a gift).

### Gym 2 — the Loomhouse Canopy (Tamsin Loom)

- **Puzzle (3/10, 6–10 minutes; SPINE Rev 19 "web trampolines"):** the hollow of Briarwick's elder. A **taut** web (drum-tight silver) throws you three tiles the way you stepped on; a **sticky** web (sagging, yellow) stops you; nothing under you drops you into Tamsin's safety net, which lowers you back to the floor (a free reset).
    - *Teach:* one web straight up to ledge 1; then a web that throws you onto a web and on to ledge 2 (Lass Orla watches the landing, so her battle can't be skipped).
    - *Twist:* bounce onto a sticky web, step sideways onto a taut one to be thrown onto the next sticky web, walk up to ledge 3. The webs either side of the first sticky web, and the one beside the start, throw you into the drop.
    - *Combine:* two Joltik. Joltik 1 (ledge 3, gold strand) flips webs A and B; Joltik 2 (the west perch, blue strand) flips B and C. All three start slack. Joltik 1 alone makes A and B taut and throws you straight up into the net (the trap). **Solution: spark both Joltik once each** → A taut (up), B sticky (stop), C taut (across) to Tamsin's ledge.
    - Hints from Pim (the net-minder) at the foot: three tiers, the last is the solution; he also resets the strands.
- **Badge:** the **Weft Badge**. **TM89 U-turn.**
- **Level cap after:** **23**.
- **Field moves unlocked:** **Cut** (HM01 from the Cutter, now) and **Rock Smash** (TM98, usable from 2 badges).
- **Mastery (optional): the Upper Lofts** (132, 4/10) up the stair behind Tamsin. Spools throw you along silk lines; cords switch them. The brass cord isn't Gran's: it's Meridian wire with a sunburst stamp, and the loft is unsolvable without it. One solution: pull α → ride s1 to P3 → pull brass → ride s3 to P4 → pull γ → ride s4 to P2 → ride s2 to P5 → walk the bridge to P6. Then **Granny's Knot** (134, 3/10): press treadles **P1, P4 and P5** (any order) to match the sampler ▲▽▲▽▲; the chest gives **Telluric Seed ×2** and a **Silk Scarf**.
- **Also open now: the Playhouse Backstage in Saltmere** (D9, 4/10, back through the stage-left wing of 154). The revolve plays three scenes in script order: from mark (2,15) cue **Shipwreck**, cross the gangplank, from mark (6,8) cue **Forest**, climb into the Fly Loft and at the **right** rail pull **rope 2, then rope 3** (A out, B out, C in), climb down, from mark (18,3) cue **Throne** and walk B → centre → the rostrum C → A → the dais → the upstage door: an old prompt-book with every line about the old capital struck out, **Magical Seed ×2** and a **PP Up**. A trapdoor in the Fly Loft leads to the Trap Room (3/10): stand at (4,5) and crank three times, then walk east and up to the chest: **Magical Seed ×2**, **PP Up** and the old Crown prop with its original stone still whole. Trainers: Juggler Pierrot, Lady Odette, Gentleman Reginald (Lv 20–21). The Fly Loft also has a **Super Potion** (152).

---

## Chapter 4 — "Both Ways"

*Maps: Spinners' Rise (566), Frostwick Pass (577), Frostwick (570–576), Rimewood Path (578), the Wolfsrime (579), the Rimewood (562) and Rimewood Glade (563), Gullcry Cliffs (561) and Gullcry Caves (564; B1F 565 not built), Ebbmouth (160–168), the Tidelock Gym (170–174). Side road: the Frostflat Causeway (560) and the Rehearsal (568). Script: `story/23_SCRIPT_CH4.md` (final). **Mostly playable:** every map above except 565 and the Reyes Cellar (166) is built, with its trainers, items, puzzles, K2 and the gym. The script's new scenes (marked "scripted, not wired yet" below) are listed in its "Map events needed" section and haven't been added to the built events. Gym 3. The PC travels alone this chapter (Juno has gone home to Verdance). The script tracks it with V124 `CH4_STEP` (0–7).*

### Key events

- **The Night the Ebb Stopped.** Meridian's night export draw kills the river for an hour (the cause); a masked Hollow cell blows the intake to stop the draw, without looking at the water; the river comes back all at once and drags a little girl's punt toward the Guild Mill's race, the same race that killed the Reyes siblings' father. The masked boy who helps you haul the race gate down is **Teo Reyes**, Marisol's brother, and a Meridian guard asks you who it was with Marisol standing there (⚑ `:ch4_teo`).
- **Larch's confession.** Over the Ebbmouth tide tables: every stutter is a Lattice draw peak and the full stop is the night export, so Meridian stopped the river; the Hollow brought it back, recklessly, with a child on the water ("Both of those are true. That's the trouble with being right in a hurry."). "It's not the Hollow stopping the river. It's us. It's my design. I lit up this whole region, you know. Eleven cities on my design."

### Order of events

1. **Spinners' Rise (566),** north out of Briarwick's gate. The Fleece Cross on the ridge; the shepherd saw a boy in a black coat run past without stopping, and someone tied a grey ribbon at the Ribbon-tier (scripted, not wired yet). *Optional:* the shepherds' **Ram Race** (finish within the step limit: **Quick Claw**), and the Shearing Cave behind the sheep-wash waterfall (Soft Sand, a lost Wooloo lamb).
2. **Frostwick Pass (577, `:SNOWY_MOUNTAIN`).** Wind gusts push you along lanes on the open slope. Trainers: Twins Kari & Kaia (double), Ranger Liv, Camper Eirik, and Huscarl Hrodgar at the **Handfast Arch** (half whale-jaw, half living briar, a brass Meridian sunburst bolted over its keystone). Walking under it: "For a step you are in neither kingdom" (scripted). Behind the frozen waterfall at the tarn: the Hollow of the Handfast and a **Soothe Bell**. With Rock Smash, the avalanche gully hides the **Icium Z**.
3. **Frostwick (570),** the borderland village under six ice-glazed giant trees. At the **Border House** (575) a Meridian clerk's scanner plate stays dark ("I'll put 'pending'") and the sunburst is stamped over both kingdoms' seals. The Pokémon Center's Gale Post desk (571, scripted) has **Juno's letter** (Rowan said "Did he, now" about the Mourner) and Larch's note with a third **Kelp Tea Bag**. **The Two Hearths** (573) is the Tally's inn: the bard sings the Sleeping Whale song (scripted), and Ingrith, Brenna and Sigvald and Sister Maelon give Trial quests. Shop at **The Exchange** (572); the Rime-silk Loft (574) has a **Silk Scarf**.
4. *Optional side road:* **the Frostflat Causeway (560)** out of Frostwick's South Gate (the customs chain unhooks from this side): the salt road back down the coast to Saltmere, five trainers, the Border Stones. Off it through a Bleed Veil, **the Rehearsal (568)**: five seconds of a wagon crash on loop (TM10 Work Up, Bleed Shard #3, an Imposter **Ditto**). The Causeway is also how you reach the Legion barge in Saltmere's harbour (*The Little Crucible*).
5. **Rimewood Path (578, `:SILKWOOD`),** out of Frostwick's North Gate. The blaze-trees and the **Lantern Birch** (**Never-Melt Ice**; the note under the lamp now reads "Not late. Ahead." and "Mind the boy in the coat"). Five trainers. The Long Ice slide. *Secret:* at the blue blaze leave the path ("the Unblazed") and follow the Stantler tracks to a **Stantler stag** (wild, Lv 19).
6. *Optional:* **the Wolfsrime (579)** off the Rimewood's east edge: the hanging bell, the old den, and a snow bank that drops you back onto Frostwick Pass (one way).
7. **The Rimewood (562).** A cold camp by the fallen giant (scripted): three sleeping hollows, survey flags burned as kindling, half a carved bark mask, and a fourth set of boot prints in a hurry. The **Frost Loom** side path (pull left, then right: the trapper's cache, **Snowball ×2**). Through a Cut sapling: **Rimewood Glade (563)** and its slide puzzle (**Never-Melt Ice**, hidden **Revive**).
8. **Gullcry Cliffs (561, `:MOUNTAIN`).** A landslide blocks the cliff road: go through **Gullcry Caves (564)**, where the tide turns every 24 steps. Back on the cliffs: Old Asta's egg ledges, a Cramorant with something in its throat (**Big Pearl**).
9. **K2:** Kestrel in the gap between two tors near Ebbmouth (561 (11,7)), watching the road through a cracked spyglass. Three grey cloaks went into Ebbmouth last night. His Honedge is from his grandmother; he named it Morwen. After the battle, ⚑ `:ch4_kestrel_mourner`: *"Do you think the Mourner is your mother?"* (kind: "Thanks for asking it quiet. I suppose."; he leaves you a note at the chapter's end) / *"He sounds just like her, doesn't he."* (blunt: he shoves past; Bond down) / *silence* ("She'd never wear a mask. She hated masks."). S111, V124 = 1.
10. **Ebbmouth (160).** On arrival the river stops for forty seconds and every mill-wheel freezes (scripted; V108 = 1). The Tidelock is shut: Marisol is at the Guild vote. The war seeds are on the quay: a teamster's news of an Ashkaar rider burning an Isenmar sled-caravan west of Duneholt, a Meridian heat-contract poster showing Ashkaar's forges, the Thane's war levy. A fishwife says Larch gets letters with a sunburst seal. Get the **Good Rod** at the Anglers' Guild (163).
11. **"He Followed You Here"** at the eel stall (scripted; the chapter's comedy scene): Kestrel is hiding behind the barrels "conducting surveillance" with four eels. **Marisol Reyes** finds him first. She invites you to the strike vote. V124 = 2.
12. **The Strike Vote** on the Mill Quay (167, scripted): two hundred dockworkers, Marisol on a barrel, and **Teo** heckling from the wheel platform ("Strike or drown!"). The river stops for a full minute. Afterwards Teo introduces himself ("The disaster in the family") and tells you to count the stutters: they're always on the hour. V124 = 3.
13. **The Night the Ebb Stopped** (160, the Guild Mill race; scripted, replacing the shorter built "Teo" scene at (29,31)). At night the river stops and doesn't come back; little **Pella** paddles her punt into the dead-still channel after her toy boat; three grey cowls at the intake, one cutting cable with shears. A bang, and the river comes back all at once, spinning the punt toward the race. Marisol goes into the water after it with her Floatzel and sends you to the race gate's chain.
    - **Battle:** a double vs two Hollow Bereaved on the towpath (`:WATER_SURFACE`; their Ebbmouth teams aren't in PBS yet). Then the masked boy at the jammed chain: **Teo Reyes** (`HOLLOW_TEO`, can't flee).
    - He sees the punt, and you haul the chain together; the gate drops and holds. His mask is pushed up: Marisol: "...Teo?" "Same race, Teo." She tells him to go.
    - A Meridian guard runs up and asks you. ⚑ **`:ch4_teo`**: *"It was Teo Reyes."* (report: Meridian Standing up, Marisol's Bond down hard, Teo hunted) / *"I didn't see his face."* (keep_secret: Marisol's Bond up; "I owe you") / *say nothing and find Marisol after* (confront). Kestrel arrives too late and finds a cable cut clean by shears. S112, V124 = 4.
    - *Built today:* a shorter version of this scene (the boat, the Teo battle and the same three-way choice, on S111).
14. **The same night** (164 Reyes House, scripted): *confront*: Marisol at the kitchen table tells you about their father, admits she tells Teo where the Lattice patrols walk, and gives you the **Cellar Key**; *keep_secret*: the key is in the teapot; *report*: the house is dark. The **Reyes Cellar** (166, the Hollow cell; not built): two Bereaved and Teo's note (`:confront`/`:keep_secret`: **Net Ball ×2**), or Meridian guards boxing up the cell (`:report`).
15. **The morning after** (160, scripted): wanted posters for Teo (report), or Mrs Reyes with a **Smoked Char** from Marisol (otherwise). Pella's father gives you a **Big Pearl**. The vote went seven halls to six: no strike, for now. The Tidelock opens (V124 ≥ 5).
16. **Gym 3, the Tidelock Gym** (170–174): **Marisol Reyes**. Her opening lines follow `:ch4_teo`. The **Tideturn Badge** and **TM03 Water Pulse**; the badge case adds a third, lower note ("Your box is singing."). V124 = 6.
17. **"Pick One"** on the quay with smoked eel (scripted): "Meridian pays my people. Meridian's killing my river. Pick one, kid. I dare you."
18. **Larch's Tide Tables** at the Pokémon Center (161, scripted; replaces the two built Larch lines): Lecture Three (with a diagram), a cup of kelp tea, the two charts laid over each other, and the confession. She was Meridian's Chief Engineer and left eight years ago. V124 = 7.
19. **Chapter close** (scripted): Hesper Vane's unsigned letter on lighthouse paper at the Gale Post desk: *"Stay away from my grandson."* A note from Kestrel if you were kind ("The eel was good. Don't tell anyone."). The towpath gate east of the Mill Quay opens to the Lock Road. V102 = 5.

### Areas

#### Spinners' Rise (566)

- **Field:** Meadow (`:MEADOW`). The Ram Race: from the start line to the finish at (47–53,33); the shortest walk is 60 steps and the limit 73.

| Method | Pokémon (levels, rate) |
|---|---|
| Grass (morning / day) | Wooloo 15–18 (18%), Skiddo 15–18 (15%), Deerling 15–18 (14%), Sewaddle 15–18 (12%), Swablu 15–18 (10%), Flabébé 15–18 (8%), Snom 16–18 (6%), Tauros 17–19 (5%), Mareep 15–18 (4%), Nincada 15–18 (4%), Swinub 16–18 (4%) |
| Grass (night) | Hoothoot 15–18 (20%), Spinarak 15–18 (18%), Wooloo 15–18 (12%), Kricketot 15–18 (10%), Snom 16–18 (10%), Sewaddle 15–18 (8%), Noctowl 20–21 (5%), Kricketune 16–18 (5%), Mareep 15–18 (4%), Nincada 15–18 (4%), Swinub 16–18 (4%) |
| **After Badge 3** (added) | Ponyta 21–24 (rare, +3), Hoppip 21–24 (rare, +3) |
| **After Badge 4** (added) | Dubwool 25–28 (rare, +3), Miltank 25–28 (rare, +2) |

- **Items:** Soft Sand (15,61) · Potion (60,91) · Super Potion (24,40) · Repel (70,20)
- **Hidden items:** Stardust (hill fort, 36,10)
- **Gifts:** Quick Claw (the Ram Race).

#### Frostwick Pass (577)

- **Field:** Snowy Mountain (`:SNOWY_MOUNTAIN`). Gusts push you along marked lanes on the open slope. The **Icium Z** is a hidden find in the avalanche gully at (69,57), behind a Rock Smash rock, with 2+ badges ("a sliver of glass so clear you only see it by its frost"; it rings and waits until you have Bastian's ring, after Badge 13).

| Method | Pokémon (levels, rate) |
|---|---|
| Grass (morning / day) | Snorunt 16–19 (16%), Snom 16–19 (14%), Cubchoo 16–20 (14%), Deerling 16–20 (12%), Delibird 16–20 (10%), Vanillite 16–20 (10%), Bergmite 16–20 (10%), Stantler 18–20 (6%), Teddiursa 16–20 (4%), Swinub 16–20 (4%) |
| Grass (night) | Snorunt 16–19 (18%), Smoochum 16–20 (14%), Cubchoo 16–20 (14%), Snom 16–19 (14%), Hoothoot 16–20 (12%), Vanillite 16–20 (10%), Spinarak 16–19 (8%), Delibird 16–20 (6%), Swinub 16–20 (4%) |
| **After Badge 3** (added) | Sneasel 21–24 (rare, +3), Absol 21–24 (rare, +2) |
| **After Badge 4** (added) | Bouffalant 25–28 (rare, +3), Cetoddle 25–28 (rare, +2) |

- **Items:** Soothe Bell (59,20) · Ice Heal (8,56) · Super Potion (64,45)
- **Hidden items:** Never-Melt Ice (tarn, 47,28)
- **Trainers** (Standard; Hard +1 level, Casual −1):
    - **Twins Kari & Kaia** (double): Swinub 17, Snom 18
    - **Pokémon Ranger Liv**: Deerling 18, Cubchoo 18
    - **Camper Eirik**: Snorunt 18, Swinub 19
    - **Black Belt Hrodgar**: Cubchoo 19, Snorunt 19, Stantler 20

#### Frostwick (570) and its interiors

- **Field:** Snowy Mountain (`:SNOWY_MOUNTAIN`). Interiors: Pokémon Center (571), The Exchange (572, the Mart), The Two Hearths (573, the Tally's inn), Rime-silk Loft (574), Border House (575), Halvard's Smokehouse (576).

| Method | Pokémon (levels, rate) |
|---|---|
| Old Rod | Magikarp 15–20 (50%), Goldeen 15–20 (30%), Basculin 15–20 (20%) |
| Good Rod (Ebbmouth, Ch4) | Goldeen 20–26 (35%), Arrokuda 20–26 (30%), Spheal 20–26 (30%), Barboach 20–26 (5%) |
| Super Rod (Rimeholt, Ch11; planned) | Seaking 45–50 (30%), Barraskewda 45–50 (25%), Whiscash 45–50 (25%), Sealeo 45–50 (20%) |
| **After Badge 3** (added) | Good Rod: Feebas 21–24 (rare, +3) |
| **After Badge 4** (added) | Good Rod: Veluza 25–28 (rare, +2) |

- **Items:** none on the map
- **Hidden items:** Snowball (40,41) · Never-Melt Ice (22,10)

*Rime-silk Loft (574):*

- **Items:** Silk Scarf (11,10)
- **Hidden items:** none

#### Frostflat Causeway (560) and the Rehearsal (568) — optional side road

- **Field:** Causeway Snowy Mountain (`:SNOWY_MOUNTAIN`); the Rehearsal The Bleed (`:BLEED`). The causeway is chained at the Border Stones by Isenmar customs until you reach Frostwick by the Pass; then it is the quick road back to Saltmere. *Secret:* the Old Causeway under the ice beside the new one (an ice-slide run to a cairn).
- **The Rehearsal (D8, 4/10):** a "second" is your step; the wagon crash advances one frame per step and the frozen salt gusts are solid on even frames. Cross the salt flat through the gaps that are open on the frame you'll reach them; the onlookers name the open lane each visit. Reward: TM10 Work Up and Bleed Shard #3.

*Frostflat Causeway (560):*

| Method | Pokémon (levels, rate) |
|---|---|
| Grass (morning / day) | Glameow 15–18 (12%), Snorunt 15–18 (10%), Spheal 15–18 (10%), Skitty 15–18 (8%), Spinda 15–18 (8%), Dunsparce 15–18 (8%), Cetoddle 15–18 (8%), Wiglett 15–18 (8%), Snom 15–18 (6%), Delibird 16–19 (6%), Tauros 16–19 (5%), Miltank 16–19 (5%), Swinub 15–18 (4%), Kangaskhan 17–19 (2%) |
| Grass (night) | Snorunt 15–18 (15%), Spheal 15–18 (10%), Glameow 15–18 (10%), Spinda 15–18 (10%), Snom 15–18 (10%), Hoothoot 15–18 (10%), Smoochum 15–18 (10%), Cetoddle 15–18 (10%), Dunsparce 15–18 (10%), Wiglett 15–18 (5%) |
| **After Badge 3** (added) | Eiscue 21–24 (rare, +3), Sneasel 21–24 (rare, +3) |
| **After Badge 4** (added) | Bouffalant 25–28 (rare, +3), Absol 25–28 (rare, +2) |

- **Items:** Super Potion (56,6) · Ice Heal (3,8) · Heal Powder (45,23)
- **Hidden items:** Soft Sand (56,23)
- **Trainers** (Standard; Hard +1 level, Casual −1):
    - **Picnicker Sela**: Skitty 16, Phanpy 17
    - **Hiker Torvald**: Binacle 19, Clobbopus 20
    - **Lass Tilde**: Swinub 16, Snom 17
    - **Sailor Haakon**: Spheal 17, Cetoddle 18
    - **Bird Keeper Ailsa**: Wingull 17, Delibird 18

*The Rehearsal (568):*

| Method | Pokémon (levels, rate) |
|---|---|
| Grass | Ditto 18–21 (12%), Kecleon 18–21 (10%), Smeargle 18–21 (10%), Zorua 18–21 (10%), Minccino 18–21 (10%), Audino 18–21 (10%), Mime Jr. 18–21 (8%), Porygon 19–21 (5%), Furfrou 19–21 (5%), Indeedee 19–21 (5%), Castform 19–21 (5%), Girafarig 19–21 (5%), Tandemaus 18–21 (5%) |
| **After Badge 3** (added) | Impidimp 21–24 (rare, +3) |
| **After Badge 4** (added) | Mimikyu 25–28 (rare, +2) |

- **Items:** TM10 Work Up (31,9)
- **Hidden items:** Stardust (salt flat, 29,4)

#### Rimewood Path (578)

- **Field:** Silkwood (`:SILKWOOD`). The Lantern Birch (41,40); the blue blaze and the Stantler stag (67,3, `WildBattle.start(:STANTLER, 19)`, once).

| Method | Pokémon (levels, rate) |
|---|---|
| Grass (morning / day) | Snover 16–20 (16%), Cubchoo 16–20 (14%), Teddiursa 16–20 (12%), Deerling 16–20 (12%), Buneary 16–20 (12%), Vanillite 16–20 (10%), Snom 16–19 (8%), Sewaddle 16–19 (6%), Spinarak 16–19 (6%), Swinub 16–20 (4%) |
| Grass (night) | Snorunt 16–20 (18%), Morelull 16–20 (14%), Cubchoo 16–20 (12%), Teddiursa 16–20 (12%), Spinarak 16–19 (12%), Snover 16–20 (10%), Hoothoot 16–20 (10%), Buneary 16–20 (5%), Swinub 16–20 (4%), Sneasel 18–20 (3%) |
| **After Badge 3** (added) | Smoochum 21–24 (rare, +3), Delibird 21–24 (rare, +3) |
| **After Badge 4** (added) | Cryogonal 25–28 (rare, +2), Stantler 25–28 (rare, +2) |

- **Items:** Silk Scarf (70,35) · Revive (17,50) · Ice Heal (70,2) · Charcoal (10,52) · Super Potion (66,73)
- **Hidden items:** Never-Melt Ice (birch hollow, 20,27) · Pearl (fall pool, 3,49)
- **Gifts:** Never-Melt Ice (the Lantern Birch).
- **Trainers** (Standard; Hard +1 level, Casual −1):
    - **Hiker Ottar**: Teddiursa 18, Swinub 18
    - **Pokémon Ranger Ketil**: Buneary 19, Cubchoo 19
    - **Camper Brand**: Snover 19, Vanillite 19, Carkol 19
    - **Picnicker Hild**: Combee 19, Teddiursa 19, Deerling 20
    - **Cool Trainer Ragna**: Sneasel 20, Snover 20, Morelull 21

#### The Wolfsrime (579) — optional

- **Field:** Silkwood (`:SILKWOOD`).

| Method | Pokémon (levels, rate) |
|---|---|
| Grass (morning / day) | Snover 16–20 (14%), Cubchoo 16–20 (14%), Deerling 16–20 (12%), Buneary 16–20 (12%), Snom 16–19 (12%), Hoothoot 16–20 (12%), Spinarak 16–19 (8%), Vanillite 16–20 (8%), Swinub 16–20 (4%), Teddiursa 16–20 (4%) |
| Grass (night) | Snorunt 16–20 (20%), Hoothoot 16–20 (18%), Cubchoo 16–20 (14%), Spinarak 16–19 (14%), Morelull 16–20 (12%), Teddiursa 16–20 (12%), Snom 16–19 (10%) |
| **After Badge 3** (added) | Sneasel 21–24 (rare, +3), Delibird 21–24 (rare, +3) |
| **After Badge 4** (added) | Stantler 25–28 (rare, +2), Bergmite 25–28 (rare, +2) |

- **Items:** Snowball (60,16) · Ether (18,48) · Super Potion (66,72)
- **Hidden items:** Big Mushroom (birch hollow, 28,24) · Tiny Mushroom (the den, 64,20)

#### The Rimewood (562) and Rimewood Glade (563)

- **Field:** Rimewood Silkwood (`:SILKWOOD`); Glade Frozen Lake (`:FROZEN_LAKE`). *(Both still wait for an art pass, REQUESTS map builder 13–14.)*
- **The Frost Loom (D7, 3/10):** on the east edge's dead-end side path, three frozen threads (trappers' pegs at (40,19) left, (41,19) middle, (42,19) right) hold three icicle curtains. Left cracks 1 and 2, middle 2 and 3, right 3. **Pull left, then right** (middle would refreeze curtain 2). Behind: the trapper's cache (44,12), **Snowball ×2**.
- **The Glade's slide puzzle:** from the start (6,8) slide **Up, Right, Up, Left, Down, Right, Down, Left, Up** to the islet with the **Never-Melt Ice**. Ranger Sigurd's hint: "Ice doesn't stop you. Rocks do. Pick your rocks."

*The Rimewood (562):*

| Method | Pokémon (levels, rate) |
|---|---|
| Grass (morning / day) | Snover 16–20 (14%), Snom 16–19 (12%), Cubchoo 16–20 (8%), Bergmite 16–20 (8%), Vanillite 16–20 (8%), Deerling 16–20 (8%), Teddiursa 16–20 (8%), Delibird 16–20 (8%), Buneary 16–20 (7%), Tarountula 16–19 (6%), Smoochum 16–20 (6%), Swinub 16–20 (4%), Stantler 18–20 (3%) |
| Grass (night) | Snorunt 16–20 (15%), Snom 16–19 (15%), Snover 16–20 (10%), Cubchoo 16–20 (10%), Hoothoot 16–20 (10%), Spinarak 16–19 (10%), Teddiursa 16–20 (10%), Morelull 16–20 (10%), Sneasel 18–20 (5%), Stantler 18–20 (5%) |
| **After Badge 3** (added) | Absol 21–24 (rare, +2), Eiscue 21–24 (rare, +3) |
| **After Badge 4** (added) | Cryogonal 25–28 (rare, +3), Milcery 25–28 (rare, +2) |

- **Items:** Ice Heal (41,47) · Great Ball (8,34) · Ice Stone (26,33)
- **Hidden items:** TM07 Hail (37,7)
- **Gifts:** Applewood Log (35,9) · Snowball ×2 (the trapper's cache).
- **Trainers** (Standard; Hard +1 level, Casual −1):
    - **Bug Catcher Pell**: Snom 18, Tarountula 19
    - **Pokémon Ranger Orla**: Deerling 18, Snover 19, Stantler 20
    - **Hiker Ulf**: Teddiursa 18, Bergmite 19
    - **Camper Rook**: Cubchoo 18, Sneasel 19
    - **Twins Ana & Ida** (double): Morelull 19, Snorunt 19

*Rimewood Glade (563):*

| Method | Pokémon (levels, rate) |
|---|---|
| Grass (morning / day) | Snom 17–20 (18%), Smoochum 17–20 (12%), Vanillite 17–20 (10%), Snover 17–20 (10%), Spritzee 17–20 (8%), Flabébé 17–20 (8%), Cubchoo 17–20 (8%), Deerling 17–20 (8%), Joltik 17–20 (5%), Stantler 18–20 (5%), Eiscue 18–20 (5%), Cryogonal 20 (3%) |
| Grass (night) | Snom 17–20 (18%), Vanillite 17–20 (12%), Snover 17–20 (10%), Cubchoo 17–20 (10%), Smoochum 17–20 (10%), Spritzee 17–20 (8%), Deerling 17–20 (8%), Cryogonal 20 (6%), Stantler 18–20 (5%), Eiscue 18–20 (5%), Emolga 17–19 (5%), Joltik 17–20 (3%) |
| **After Badge 3** (added) | Milcery 21–24 (rare, +3) |
| **After Badge 4** (added) | Hatenna 25–28 (rare, +2) |

- **Items:** Never-Melt Ice (19,14)
- **Hidden items:** Revive (28,10)
- **Trainers** (Standard; Hard +1 level, Casual −1):
    - **Pokémon Ranger Sigurd**: Stantler 19, Cryogonal 20

#### Gullcry Cliffs (561) and Gullcry Caves (564)

- **Field:** Cliffs Mountain (`:MOUNTAIN`); Caves Cave (`:CAVE`). The cliff road is shut by a landslide; the caves' south mouth is at the foot of the slide crag (about (6,72)) and the north mouth at about (6,49).
- **Gullcry Caves (D6, 4/10):** the tide toggles every **24 steps** (gull cries count down the last three; the tide-mark rock changes colour). The west gallery is always open; the sand-bar crossing is a 19-step shortcut, so start it right after the tide turns (scare the gull roost to hear the timing). A weed curtain on the east shelf is a crawlway to a grotto. *B1F (565, the sea arch, TM55 Brine and a Shell Bell) is not built yet.*

*Gullcry Cliffs (561):*

| Method | Pokémon (levels, rate) |
|---|---|
| Grass | Wingull 16–19 (17%), Ducklett 16–19 (12%), Surskit 16–19 (10%), Azurill 16–19 (10%), Bergmite 16–19 (9%), Cramorant 17–20 (8%), Snorunt 16–19 (8%), Taillow 16–19 (8%), Oricorio 17–20 (8%), Chatot 17–20 (6%), Wooper 16–19 (4%) |
| Surf (Surf from Badge 6) | Tentacool 28–34 (30%), Wingull 28–33 (30%), Ducklett 28–33 (20%), Cramorant 28–33 (10%), Swanna 35–37 (10%) |
| Old Rod | Magikarp 16–20 (50%), Finneon 16–20 (30%), Wishiwashi 16–20 (20%) |
| Good Rod (Ebbmouth, Ch4) | Staryu 18–25 (30%), Shellder 18–25 (25%), Clauncher 18–25 (25%), Carvanha 18–25 (20%) |
| Super Rod (Rimeholt, Ch11; planned) | Staryu 45–50 (25%), Clawitzer 45–50 (25%), Corsola 45–50 (25%), Sharpedo 45–50 (15%), Relicanth 45–50 (10%) |
| **After Badge 3** (added) | Flamigo 21–24 (rare, +3), Wattrel 21–24 (rare, +3) |
| **After Badge 4** (added) | Pelipper 25–28 (rare, +3), Drampa 25–28 (rare, +2) |

- **Items:** Great Ball (5,120) · Mystic Water (52,52) · Ether (40,28)
- **Hidden items:** Never-Melt Ice (tor, 38,6) · Pearl (shingle, 48,116) · Ice Heal (slide toe, 34,84)
- **Gifts:** Big Pearl (the Cramorant, 46,26).
- **Trainers** (Standard; Hard +1 level, Casual −1):
    - **Bird Keeper Wren**: Taillow 17, Ducklett 18, Chatot 18
    - **Sailor Haldor**: Wingull 18, Spheal 19
    - **Cool Trainer Astrid**: Oricorio 19, Cramorant 19, Snorunt 19
    - **Fisherman Kjell**: Magikarp 17, Finneon 18, Wooper 18

*Gullcry Caves (564):*

| Method | Pokémon (levels, rate) |
|---|---|
| Cave | Zubat 16–20 (15%), Spheal 16–20 (12%), Krabby 16–20 (10%), Seel 16–20 (10%), Wimpod 16–20 (10%), Binacle 16–20 (10%), Slowpoke 16–20 (9%), Clobbopus 16–20 (8%), Corsola 16–20 (8%), Dewpider 16–20 (8%) |
| Surf (Surf from Badge 6) | Tentacool 28–34 (40%), Seel 28–33 (30%), Spheal 28–33 (20%), Sealeo 32–36 (10%) |
| Old Rod | Magikarp 16–21 (60%), Tentacool 16–21 (40%) |
| Good Rod (Ebbmouth, Ch4) | Shellder 20–25 (35%), Clamperl 20–25 (30%), Corsola 20–25 (20%), Qwilfish 20–25 (15%) |
| Super Rod (Rimeholt, Ch11; planned) | Clamperl 45–50 (30%), Qwilfish 45–50 (25%), Dewgong 45–50 (20%), Relicanth 46–50 (15%), Corsola 45–50 (10%) |
| **After Badge 3** (added) | Clauncher 21–24 (rare, +3), Eiscue 21–24 (rare, +3) |
| **After Badge 4** (added) | Relicanth 25–28 (rare, +2) |

- **Items:** Revive (44,17) · Big Pearl (27,17) · Potion (36,31) · Heart Scale (26,34)
- **Hidden items:** Pearl (27,33)
- **Trainers** (Standard; Hard +1 level, Casual −1):
    - **Hiker Torvald**: Binacle 19, Clobbopus 20

#### Ebbmouth (160) and the Mill Quay (167)

- **Field:** Water Surface (`:WATER_SURFACE`) (the town and its quays). Interiors: Pokémon Center (161), Mart (162), Anglers' Guild (163), Reyes House (164), Net-mender's House (165), the Net Loft (168). The Reyes Cellar (166, the Hollow cell) is not built.

| Method | Pokémon (levels, rate) |
|---|---|
| Surf (Surf from Badge 6) | Psyduck 28–34 (25%), Tentacool 28–34 (25%), Buizel 28–33 (20%), Chewtle 28–33 (15%), Wooper 28–33 (10%), Drednaw 33–36 (5%) |
| Old Rod | Magikarp 17–22 (60%), Goldeen 17–22 (25%), Finneon 17–22 (15%) |
| Good Rod (Ebbmouth, Ch4) | Basculin 20–26 (35%), Corphish 20–26 (30%), Arrokuda 20–26 (30%), Barboach 20–26 (5%) |
| Super Rod (Rimeholt, Ch11; planned) | Whiscash 45–50 (25%), Crawdaunt 45–50 (25%), Barraskewda 45–50 (25%), Gyarados 46–50 (10%), Seaking 45–50 (10%), Feebas 45–50 (5%) |
| **After Badge 4** (added) | Good Rod: Corsola 25–28 (rare, +3), Feebas 25–28 (rare, +2) |

*Ebbmouth (160):*

- **Items:** Fresh Water (6,48)
- **Hidden items:** Net Ball (57,43)

*Mill Quay (167):*

- **Items:** Super Potion (37,28)
- **Hidden items:** Heart Scale (2,17)
- **Gifts:** Good Rod (the Guildmaster, 163) · TM03 Water Pulse (Marisol) · scripted, not wired yet: Kelp Tea Bag (Frostwick's Gale Post, 571), Cellar Key (164), Smoked Char (Mrs Reyes), Big Pearl (Pella's father), Net Ball ×2 (the cellar).

### Key battles

**K2 — Kestrel, Gullcry Cliffs** (`:MOUNTAIN`, before Gym 3)

| Pokémon | Lv | Item | Ability | Moves |
|---|---|---|---|---|
| Staravia | 21 | Telluric Seed | Intimidate | Wing Attack, Quick Attack, Aerial Ace, Endeavor |
| Sandile | 21 | Oran Berry | Moxie | Bite, Rock Tomb, Sand Tomb, Hone Claws |
| Honedge "Morwen" | 21 | Oran Berry | No Guard | Slash, Shadow Sneak, Aerial Ace, Fury Cutter |
| **Starter**† | 23 | Oran Berry | (slot 0) | (regenerated for the swapped species) |

*Bag: Super Potion; IV 12.*

- **Hard:** Staravia 21 @Telluric Seed, Sandile 21 @Oran Berry, Deino 21 @Oran Berry, Honedge 21 @Eviolite, Starter 23 @Sitrus Berry
- **Casual:** Honedge 19 @Oran Berry, Starter 21 @Oran Berry

† The rival's starter is written as the Gen 1 line in PBS; Prismfall Core swaps it at battle start for the same-generation counterpart of your starter (same stage).

*Field note:* Mountain gives Rock ×1.5 and Flying ×1.2, so Staravia's Aerial Ace and Wing Attack hit harder; Sandile's Rock Tomb too. *Tip:* Staravia's Intimidate and Sandile's Moxie punish a slow physical team. Honedge "Morwen" (No Guard) is immune to Normal and Fighting; hit it with Fire, Ground, Ghost or Dark. An Ice or Electric type handles Staravia.

**The night: two Bereaved** (double, the towpath, `:WATER_SURFACE`) *(their Ebbmouth teams aren't in PBS yet; the script asks for Lv 20–22 Water/Dark/Poison, no Electric or Grass).*

**Teo Reyes** (`HOLLOW_TEO`, the race gate's chain platform, `:WATER_SURFACE`, can't flee)

| Pokémon | Lv | Item | Ability | Moves |
|---|---|---|---|---|
| Carvanha | 19 | Oran Berry | Rough Skin | Aqua Jet, Bite, Poison Fang, Scary Face |
| Arrokuda | 20 | Oran Berry | Swift Swim | Aqua Jet, Bite, Fury Attack, Agility |
| Chewtle "Snapper" | 21 | Sitrus Berry | Swift Swim | Bite, Headbutt, Water Gun, Protect |

*Bag: Super Potion; IV 12.*

- **Hard:** Carvanha 19 @Focus Sash, Basculin 20 @Sitrus Berry, Arrokuda 20 @Mystic Water, Chewtle 21 @Eviolite
- **Casual:** Arrokuda 18 @Oran Berry, Chewtle 19 @Sitrus Berry

*Field note:* on Water Surface, Water moves are ×1.5 and Electric ×1.5 against grounded targets; his Swift Swim cell plays the river. *Tip:* the Water Surface counts as rain for **Swift Swim**, so Arrokuda and Chewtle move at double speed. Grass is your answer and it's common in Elowen (Oddish, Budew, Smoliv, Petilil, Gossifleur...); Electric is deliberately rare before Marisol (Shinx on Windfall Row, Mareep on the Dyers' Ford, Joltik after Badge 2). Carvanha's Rough Skin punishes contact.

**Gym 3 — Warden Marisol Reyes** (Water, `:WATER_SURFACE`, single battle, cap 23)

| Pokémon | Lv | Item | Ability | Moves |
|---|---|---|---|---|
| Pelipper | 19 | Oran Berry | Keen Eye | Water Gun, Wing Attack, Supersonic, Protect |
| Chinchou | 20 | Oran Berry | Volt Absorb | Water Gun, Spark, Confuse Ray, Supersonic |
| Buizel | 20 | Oran Berry | Swift Swim | Water Pulse, Bite, Quick Attack, Swift |
| Gyarados "Lucky" | 23 | Oran Berry | Intimidate | Whirlpool, Brine, Twister, Bite |

*Bag: Super Potion; IV 12.*

- **Hard:** Pelipper 19 @Sitrus Berry, Lanturn 20 @Sitrus Berry, Dewpider 21 @Oran Berry, Floatzel 20 @Oran Berry, Gyarados 23 @Sitrus Berry
- **Casual:** Pelipper 17 @Oran Berry, Buizel 18 @Oran Berry, Gyarados 21 @Oran Berry

*Field note:* "a current that changes direction mid-fight." Water ×1.5, Electric ×1.5 into grounded targets (her Gyarados and Pelipper are airborne, so they don't take the bonus), Fire ×0.5, and Ground moves fail outright. Lucky's Whirlpool is ×2 and traps. *Tip:* bring Grass (and Electric if you found one). Chinchou's Volt Absorb eats Electric moves, and Pelipper and Lucky are airborne, so they dodge the field's Electric bonus. Buizel's **Swift Swim** is always on here.

### Side quests

- **The Rehearsal** (`EL_REHEARSAL`, The Quiet Way; wired (playable)). Sister Maelon, the Half-Tally, Frostwick (573). Unlock: Badges ≥ 2. Off the Frostflat Causeway, a stretch of road replays five seconds of a wagon crash, over and over. Something out there is practising a tragedy. Reward: Spell Tag; +3 pts.
- **Two Hearths, One Pot** (`IS_TWO_HEARTHS`, The Tally; wired (playable)). Brenna and Sigvald, the Two Hearths inn, Frostwick (573). Unlock: Badges ≥ 2. The Two Hearths has two fireplaces, two cooks and one cooking contest that has lasted nineteen years. Both cooks want you to fetch their secret ingredient. Reward: Honey x3, Lava Cookie x2; one_pot: Rare Candy; +2 pts (+2 The Quiet Way).
- **The Oathbound Parcel** (`IS_OATH_PARCEL`, The Tally; wired (playable)). Ingrith, the Half-Tally, Frostwick (573). Unlock: Badges ≥ 2. Carry a sealed oath-parcel from Frostwick to the Net Loft in Ebbmouth. In Isenmar a carried oath is not opened. Not ever. Reward: $500; +3 pts.
- **A Deed for the Skald** (`IS_SKALDS_SAGA`, The Tally; wired (playable)). Bersi Gullsong, the Ebbmouth Net Loft (160). Unlock: Badges ≥ 2. The Ebb Guild feast is tonight and Bersi has no new saga. He needs a deed. Any deed. He'll handle the exaggerating. Reward: Mystic Water; bully: MARISOL+1; tall_tale: Potion; +2 pts.
- **The Egg Thief of Gullcry** (`IS_EGG_THIEF`, The Tally; wired (playable)). Old Asta, the egg-gatherers' hut on the Gullcry Cliffs (561). Unlock: Badges ≥ 3. Something is taking eggs off the Gullcry ledges. Old Asta wants it stopped. Then she wants it stopped harder. Reward: $1000; let_go: Exp. Candy M x2, RES+1; +3 pts.
- **The Drowned Note** (`IS_OCTAVE_DROWNED_NOTE`, The Tally; wired (playable)). Aria of the Octave, the river steps, Ebbmouth; the Mill Quay wheel (167) (160). Unlock: Badges ≥ 2. A singer's Vaporeon melted into the Ebb when the river stuttered and hasn't come out. She can still hear it, sometimes. Reward: $1200, Shell Bell; +3 pts.
- **The Lattice Hums Wrong** (`ZE_LATTICE_HUM`, The Prize Exchange; wired (playable)). Grant Kiosk P-3NNY/2, the tidal Lattice station, Ebbmouth (160). Unlock: Badges ≥ 2. CALL FOR PROPOSALS #0003: ACOUSTIC SURVEY OF THE EBBMOUTH TIDAL LATTICE DURING 'STUTTER EVENTS'. RECORDER PROVIDED. Reward: $300; meridian: $1500, MERIDIAN+1; guild: MARISOL+1; larch: Exp. Candy S x2; +3 pts.
- **The Little Crucible** (`AS_LITTLE_CRUCIBLE`, The Trial by Flames; wired (playable)). Sergeant Brakka Emberhide, the Legion recruiting barge, Saltmere harbour (146). Unlock: Badges ≥ 2. WRIT OF FLAME: three bouts, back to back, no healing. Then the barge's mascot. Win and the Legion respects you. Lose and the Legion respects you less. Reward: $1200, Quick Claw; +3 pts.

- **The Eevee Octave, singer 2 of 8: Aria** (*The Drowned Note* above): her duel at the Mill Quay wheel is Spheal 21 @Oran Berry, Vaporeon 22 @Oran Berry.
- **The Little Crucible** sends you back down the Frostflat Causeway to the Legion recruiting barge in Saltmere's harbour (146): three bouts, no healing, then the barge's mascot.

**Event Pokémon this chapter:** **Litleo "Cinderpaw"** Lv 21 (boss of *The Little Crucible* on the Legion barge in Saltmere's harbour) · **Charcadet** Lv 18 (collect from Hesper after Badge 2, if you adopted crate 7-B in Ch1) · **Sudowoodo** Lv 20 (the scarecrow's rematch on Windfall Row, after Badge 2) · **Snom** Lv 15 (Ice Scales; the oath-parcel) · **Ditto** Lv 20 (Imposter; the Rehearsal) · **Bombirdier "Postmaster"** Lv 24 (after Gym 3, *The Egg Thief of Gullcry*) · **Wattrel "Mast"** Lv 20 (Ebbmouth's harbour mast after Badge 3, if you closed the Dovetail's ledger in Ch1).

**Mega Stones and Z-crystals (they hum and wait until the ring, Badge 13):**

- **Icium Z** (Z-crystal, from Badge 2): Frostwick Pass, the avalanche gully (Rock Smash). hidden; "rings and waits".

### Gym 3 — the Tidelock Gym (Marisol Reyes)

- **When:** the Lock Hall door opens the morning after the night (V124 ≥ 5 in the script; the built door is always open).
- **Puzzle (4/10, 10–15 minutes; "the trim", map builder 13):** two rules carry both rooms. **Raise the water and the raft drifts inland (east)** until the end of the channel or a shut lock gate stops it; **lower the water and the chain winds the raft home** to its berth.
    - *Lock Hall (170), practice:* the wheel (3,13) raises and lowers; the gate lever (14,13) shuts the gate. **Shut the gate, then turn the wheel**: the raft stops at the only slot that meets the pier to the basin door. (Fisherman Gunnar; Apprentice Tove has hints.)
    - *The Basins (171/172/173, one map at three water levels; the door always opens on Low):* wheels W (3,22) and E (25,22) on the south walkway, wheel C (14,11) on the island (mid ↔ high), the gate lever on the west pier (3,10). **Solution (6 moves):** turn E (to mid) → cross to the west pier and shut the gate → turn E (to high: the raft parks at the island) → turn W (to mid) → cross to the island and turn C (to high) → ride **the Race** (14,9) to the north dock and the Warden's door. Raising twice with the gate open parks the raft at the east pier, where a **Net Ball** waits at low water. Nothing soft-locks: low water always winds the raft home.
    - *Warden's Pool (174):* Marisol. A Meridian intake is bolted into the lock wall.
- **Badge:** the **Tideturn Badge** (named by the creator, 2026-11-21; badge names for Gyms 7–18 aren't decided yet). **TM03 Water Pulse.**
- **Level cap after:** **27**.
- **Field moves:** none new (Rock Smash and Cut are already usable).
- **Mastery (optional), not built:** the **Overflow Culvert** (175, 6/10), through a grate on the east pier at mid water, behind a Rock Smash rock. Two rafts and a snag post that only catches rafts drifting seaward: flush **east**, raise the snag, flush **west**; cross raft A to the islet chest: **Elemental Seed ×2** and **Mystic Water**.

*Gym trainers* (`:WATER_SURFACE`; Hard +1 level, Casual −1):

- **Fisherman Gunnar**: Goldeen 18, Barboach 19 *(map 170)*
- **Swimmer Ingrid**: Buizel 19, Chewtle 19 *(map 171)*
- **Swimmer Leif**: Arrokuda 20, Psyduck 20 *(map 172)*
- **Fisherman Oskar**: Barboach 20, Corphish 20 *(map 172)*
- **Sailor Bjorn**: Wingull 20, Chinchou 21 *(map 173)*

*Gym items, Basins at low water (171):*

- **Items:** Net Ball (26,11)
- **Hidden items:** none

*Basins at mid water (172):*

- **Items:** Super Potion (16,10)
- **Hidden items:** none

---

## Chapter 5 — "Ten Years of Light"

*Maps: the Lock Road (580 the Reedholms, 592 the Icecutters' Haul, 590 Brassfall, 581 the Icefall Locks, 595 Coppice Ride, 594 Wallshadow Row, 593 the Arc-Lamp Mile, 582 Lumen West Gate; optional 584/585 the Voltaic Sluiceworks and 588 Ebb Hollow), Lumen City (180 the Concourse, 181 the Lowlight, the Circuit Gym 190–193, Meridian Spire 185/186 and two new rooms below it, 951 and 952), the Lowlight (Shattered) 608, and Interlude I at the Ferrow Lighthouse (105/106). **Scripted; partly built** — `story/24_SCRIPT_CH5.md` has the scenes and a full map-events list. Map builder 15 is building these maps now: at this snapshot the Concourse (180), the Lowlight (181), the Circuit Gym (190–193, with Rook's battle wired in the Core, 193) and the Shattered Lowlight (608) exist in the working tree, not yet committed and without the script's scenes; the Lock Road and the Spire are not built. Gym 4. End of Act I. The PC travels alone until Wallshadow Row.*

### Key events

- **The Lowlight Shatter.** Sable's Splitter cracks the Zap Plate in Meridian's vault; twelve named people in the Lowlight are Fixed in glass mid-motion, Dex among them.
- **Valen sees you standing in the glass.** He takes off his glove at the Veil (crystal underneath), then grants Meridian **the Mandate**; a Directorate officer asks what you saw (⚑ `:ch5_lowlight_testimony`).

### Order of events
*The script tracks this chapter with V125 `CH5_STEP` (0–13).*

1. **Ebbmouth's towpath gate** (east of the Mill Quay) opens once Marisol's badge is won and Chapter 4 has closed (V124 ≥ 7). V125 = 0.
2. **The Reedholms (580):** reed channels and punt hops. If you didn't report Teo (`:ch4_teo` ≠ report), he crosses the channel on a punt; if you did, his wanted poster is on the smoke hut. Doors to the optional **Voltaic Sluiceworks** (584/585, Rook's graffiti, a static Rotom) and, through a Bleed Veil, **Ebb Hollow** (588, the drowned village of Holmsby: TM49 and Bleed Shard #4). Six trainers (Lv 20–23).
3. **The Icecutters' Haul (592):** the icecutters' union picket (Picket Captain Hulda), a Meridian heat-contract recruiter, and a dropped ice block that gives the **Ice-Bound Satchel** (key item).
4. **Brassfall (590),** the lock-town. The Lockmaster and the union steward argue at the lift; the company store takes scrip only. At the **Gale Post desk** (591): **Juno's letter** (V125 → 1). In the **Union Hall** (596, new) the boiler swaps the satchel for the **Heat Contract (Draft)**. *Optional:* restart the stuck **Ice Elevator** with an Electric type (or a Cell Battery) for a shortcut to the top of the falls.
5. **The Icefall Locks (581):** up the frozen falls past **Extraction Lattice No. 4** and its thaw ring; the border post at the top (an Elowen forester and a Meridian guard). Six trainers.
6. **Coppice Ride (595):** at the ride-side shrine, **the first view of the Crownwall**, the ring of white peaks with Crownhaven inside. The PC's scar aches. The Kingsferry punt; the uncut panel (a Miracle Seed).
7. **Wallshadow Row (594):** at the Four Ways inn, **Juno rejoins** (V125 → 2) for the rest of the road and the city. The other exits are closed for now: west to Prism Falls (Act III), north to Kingsmead (Act III), south to the Long Drop (Ch9), east to Candle Down (opens after Rook's badge: the Act II road). The Southgate shrine's eighteen-and-one window.
8. **The Arc-Lamp Mile (593, `:NEON_GRID`):** a hundred numbered lamps into Lumen; hoardings for TEN YEARS OF LIGHT and **THE MERIDIAN PRISM ARENA**. Lamp 47 has something under its base plate.
9. **Lumen West Gate (582):** the Meridian scanner reads `NULL`; the guard calls upstairs and hands you a **Gala Invitation** (key item). V125 → 3.
10. **Lumen City, the Concourse (180):** airships, holograms, Rotom couriers. The Circuit Gym is closed (Rook is filming). Down every alley, grilles and lift-shafts to Nadir; a Zenith officer moves a Nadir kid along.
11. **The Lumen Pokémon Center (182):** Larch's letter and a fourth **Kelp Tea Bag**. **The Lowlight (181):** meet **Dex** and his Pichu "Spark" at the top of the stairs; he sells you **Fizzbolt ×2** (₽60) (V125 → 4), and the eleven other Lowlight people you will see again in glass: Marta Vell, Old Jory, Nessa, Hob Carrow, Linesman Aldo Fisk, Sukie, Ilo and Mattie, Gran Osk, Benno, Mr Imrie.
12. **The blackout:** the lights die on Rook's film set. Three junction boxes hold **wild Rotom** (Lv 24, catchable) and the feed-line box a fourth (Lv 26). Fix all four and the gym opens (V125 → 5). Comedy scene: "Chat Has Opinions".
13. **Gym 4, the Circuit Gym** (190–193): Rook Calder. The **Arclight Badge**, **TM43 Volt Switch** and **TM70 Flash**. The badge case's fourth note; Rook films it ("Ooh, special edition?"). The Core's Plate cradle is cold: the Zap Plate isn't here. V125 → 6.
14. **The Tenth Year Gala** (Meridian Spire 185 → 186, V125 → 7): free roam among Voss, Valen, Calla, Quent, Chancellor Hollis, Larch, Rook and Juno; the **Dark Stone core** glows black in the atrium shaft; Voss's speech ("Light is work"). Larch: "The Zap Plate's not in Rook's gym. It's *here*. In their vault."
15. **The raid:** the lights go grey, the same grey as the Lantern Theatre's; the service-lift doors burst and the Hollow pour in, led by Thistle. **Tag battle: you + Juno vs Thistle and a Pallbearer** (`:NEON_GRID`). Thistle is captured: "Ask what's in the vault. Ask why it's warm." Juno holds the lift. Down the **Service Lifts** (951, two Bereaved singles; Rook catches up) to the **Plate Vault** (952). V125 → 8.
16. **The Shatter** (cutscene SH-1; a checkpoint at the vault door): the Mourner reaches for the Plate ("we give this city back its river and its dark"); Sable clamps a brass Splitter to it ("Light for everyone") and skips away. The blast; the Plate cracks; the Mourner holds it with smoking gloves, sees you ("Not you. Not here."), lays it back down and flees. ☠ **`GO_LIVE_WIRE` "Live Wire"**: at the boss's bar-break prompt, choose "Grab the cracked Plate and run" (Rook: "Don't touch it with your HANDS!").
17. **Boss: "Overcharged"**, a Bleed-maddened Electivire on the cradle dais. The field flips from Neon Grid to the Bleed at the bar break (the game's first scripted any → Bleed). V125 → 9.
18. **The Lowlight (Shattered) (608), "Twelve":** out through the vault's service door. Twelve glass figures where the twelve people stood. You are the only one who can stand inside the Veil. Rook, off camera: "...Turn it off. Rotom. Turn it *off*." Voss carries a glassed soda crate out himself. **Valen** touches the Veil barehanded and sees you inside it.
19. ⚑ **`:ch5_lowlight_testimony`**, asked by **Director Helene Marchetti** as you step out of the Veil: *"The Mourner broke the Plate"* (Meridian Standing up, Hollow down; next morning Dorian's telegram: "So you told them the pageant version.", his Act V Consent) / *"Someone else was there. A woman."* (Hollow Standing up; Marchetti underlines your name; Larch: "Good.") / *"I don't know."* V125 → 11. That night Valen's broadcast grants Meridian the Mandate (S115).
20. **Larch at 3 a.m.** in the ruined vault with a borrowed scanner: the Plate was *already* cracking. "Something's been drinking from it for ten years. Something I built." V125 → 12.
21. **Interlude I, "Lamplight"** (play as **Kestrel**, Ferrow Lighthouse 105/106): his mother's veil in the trunk, a memory flash, a wild Bleed-touched **Haunter** on the stairs (K2's level + 3, can't be caught), the bag packed. Edda's boat slips the harbour chain (S162). Title card: **II — Imprints**. V125 → 13.

### Areas *(the Lock Road is design only; Lumen's first maps are being built)*

| Map (ID) | Field | Built? | Wild Pokémon (from `pbs/encounters.txt`) |
|---|---|---|---|
| The Reedholms (580) | Snowy Mountain (`:SNOWY_MOUNTAIN`) | no | Grass: Lotad 19–23, Psyduck 19–23, Buizel 19–23, Azurill 19–23, Croagunk 20–24, Shellos 19–23, Surskit 19–23, Wiglett 19–23, Tympole 19–23, Wooper 19–23; Surf: Lotad 28–34, Wooper 28–34, Surskit 28–34, Tympole 28–34, Palpitoad 30–36; Old Rod: Magikarp 18–23, Goldeen 18–23, Barboach 18–23, Tympole 18–23; Good Rod: Basculin 21–26, Goldeen 21–26, Chewtle 21–26, Stunfisk 21–26, Barboach 21–26 |
| The Icecutters' Haul (592) | Snowy Mountain (`:SNOWY_MOUNTAIN`) | no | _no wild table yet_ |
| Brassfall (590) | Snowy Mountain (`:SNOWY_MOUNTAIN`) | no | _no wild table yet_ |
| The Icefall Locks (581) | Snowy Mountain (`:SNOWY_MOUNTAIN`) | no | Grass: Snover 21–25, Magnemite 21–25, Pawmi 21–24, Wattrel 21–24, Voltorb 21–25, Yamper 21–24, Pachirisu 21–25, Dedenne 21–25, Togedemaru 22–25, Tadbulb 21–25, Bergmite 21–25, Diglett 21–25, Plusle 21–25, Minun 21–25 |
| Coppice Ride (595) | Meadow (`:MEADOW`) | no | _no wild table yet_ |
| Wallshadow Row (594) | Meadow (`:MEADOW`) | no | _no wild table yet_ |
| The Arc-Lamp Mile (593) | Neon Grid (`:NEON_GRID`) | no | _no wild table yet_ |
| Lumen West Gate (582) | none | no | _no wild table yet_ |
| Voltaic Sluiceworks (584) | Scrapyard (`:SCRAPYARD`) | no | Cave: Magnemite 21–25, Klink 21–25, Tadbulb 21–25, Voltorb 21–25, Joltik 21–25, Ferroseed 21–25, Grimer 21–25, Toxel 21–25, Koffing 21–25, Trubbish 21–25; Surf: Chinchou 28–34, Tynamo 28–34, Psyduck 28–34, Lanturn 32–36; Old Rod: Magikarp 20–25, Tynamo 20–25; Good Rod: Chinchou 21–26, Tynamo 21–26, Basculin 21–26 |
| Sluiceworks Turbine Hall (585) | Scrapyard (`:SCRAPYARD`) | no | Cave: Magnemite 23–26, Klink 23–26, Ferroseed 23–26, Toxel 23–26, Cufant 23–26, Togedemaru 23–26, Orthworm 23–26, Varoom 23–26, Porygon 23–26, Elekid 23–26 |
| Ebb Hollow (588) | The Bleed (`:BLEED`) | no | Grass: Frillish 23–26, Wishiwashi 23–26, Magikarp 23–26, Luvdisc 23–26, Chinchou 23–26, Finneon 23–26, Clamperl 23–26, Feebas 23–26, Alomomola 24–26, Bruxish 24–26, Horsea 23–26, Castform 23–26, Finizen 23–26 |
| Lumen City - Concourse (180) | Neon Grid (`:NEON_GRID`) | yes | _no wild table yet_ |
| Lumen City - Lowlight (181) | Neon Grid (`:NEON_GRID`) | yes | _no wild table yet_ |
| The Lowlight (Shattered) (608) | The Bleed (`:BLEED`) | yes | Grass: Charjabug 26–30, Litwick 26–30, Kilowattrel 26–30, Elekid 26–30, Pikachu 26–30, Luxio 26–30, Flaaffy 26–30, Drifloon 26–30, Shuppet 26–30, Magneton 26–30, Tadbulb 26–30, Porygon 26–30 |

- **Items placed so far** on the maps being built: X Speed (Concourse, 94,61); a hidden Cell Battery (the Lowlight, 55,38). The script's item list is longer; this will change as the build lands.

- **The Voltaic Sluiceworks (584/585, optional, DUNGEON_PUZZLES "water carries current", 5/10, `:SCRAPYARD` in the dungeon doc):** a dead turbine hall; the static Rotom stays on 585.
- **New maps the script asks for:** 596 Brassfall Union Hall, 951 Meridian Spire Service Lifts, 952 Plate Vault (not in `maps.json` yet).
- **New key items:** Gala Invitation, Ice-Bound Satchel, Heat Contract (Draft) (not in the item data yet). The Heat Contract is Meridian's Contract 7-B, the same heat terms sold to Ashkaar as to Isenmar (war seed).

### Key battles

**Gym 4 — Warden Rook Calder** (Electric, `:NEON_GRID`, single battle, cap 27)

| Pokémon | Lv | Item | Ability | Moves |
|---|---|---|---|---|
| Luxio | 25 | Magnet | Intimidate | Spark, Bite, Charge, Roar |
| Electabuzz | 25 | Synthetic Seed | Static | Shock Wave, Low Sweep, Quick Attack, Charge |
| Toxtricity | 26 | Oran Berry | Punk Rock | Shock Wave, Venoshock, Eerie Impulse, Charge |
| Rotom "Camera" | 27 | Sitrus Berry | Levitate | Shock Wave, Hex, Hydro Pump, Thunder Wave |

*Bag: Super Potion, Super Potion; IV 18.*

- **Hard:** Luxio 26 @Sitrus Berry, Electabuzz 26 @Synthetic Seed, Heliolisk 26 @Sitrus Berry, Toxtricity 27 @Throat Spray, Rotom 27 @Sitrus Berry
- **Casual:** Luxio 23 @Magnet, Toxtricity 24 @Oran Berry, Rotom 25 @Sitrus Berry

*Field note:* "circuits you complete with your own body." Neon Grid boosts Electric ×1.5 and Steel ×1.2, makes conductors (Flash Cannon, Surf, Muddy Water) hit as Electric, and nobody can fall asleep. *Tip:* Ground is the answer, and **Ground moves short out the grid** (BALANCE: the "honest answer"); Charge reboots a blackout, so finish the job. Ground types are gated before Rook (rare), so plan ahead: Diglett on the Icefall Locks.

**The Gala raid — you + Juno vs Thistle (version 1) and a Pallbearer** (tag, `:NEON_GRID`) *(Thistle's v1, the Lumen grunts and Juno's partner team are not in `pbs/trainers.txt` yet; her v0 from Ch3 is Dustox 16 @Oran Berry, Foongus 17 @Oran Berry, Phantump 18 @Sitrus Berry).*

**Boss — "Overcharged" Electivire** *(planned: 2 bars, levelled for the stretch after Gym 4, `:NEON_GRID` → `:BLEED` at the break; not registered in Prismfall Bosses yet).*

**Interlude I — Kestrel vs a Bleed-touched Haunter** (wild, on the lighthouse stairs, K2's level + 3, uncatchable) *(planned).*

**The blackout's Rotom** (wild, `:NEON_GRID`): three at Lv 24 and the feed-line box's at Lv 26, all catchable. They are the only Pokémon on offer this chapter besides the Sluiceworks Rotom (no gifts before Sahar or Corvin, SPINE Rev 16).

### Side quests

- **The Humming Lamp** (`EL_LAMP_LENS`, The Quiet Way; wired (playable)). Hesper Vane, the Ferrow Lighthouse lamp room (106). Unlock: Badges ≥ 3. A paper lantern from the lighthouse: 'THE LAMP HUMS. MAKE IT STOP. - H.V.'. Reward: Ampharosite; +1 pts.
- **Off the Beat** (`ZE_OCTAVE_OFF_BEAT`, The Prize Exchange; wired (playable)). Grant Kiosk P-3NNY / Cadence of the Octave, the Lowlight steps, Lumen City (181). Unlock: Badges ≥ 3. CALL FOR PROPOSALS #0031: NOISE COMPLIANCE, LOWLIGHT BLOCK 9. A STREET DRUMMER'S JOLTEON BLACKS OUT THE BLOCK. BOUNTY: $800. Reward: $800, Cell Battery x2; unknown: RES+1; fault: $800, MERIDIAN+1; +3 pts.
- **Customer Support** (`ZE_CUSTOMER_SUPPORT`, The Prize Exchange; designed (not wired yet)). Helpdesk Rotom, Meridian Spire lobby, Lumen City (185). Unlock: Badges ≥ 3. Walk a form through nine offices. The form is to cancel the form. Reward: Porygon Lv 24 (DOWNLOAD); +3 pts.
- **The Machine Wants Compliments** (`ZE_FIZZBOLT`, The Prize Exchange; designed (not wired yet)). a Fizzbolt vending machine, Lumen City Concourse (180). Unlock: Badges ≥ 3. A Lumen vending machine has gained sentience from the free current and only sells Fizzbolt to people who compliment it. Reward: Cell Battery; +2 pts.
- **Product Recall** (`ZE_ROTOM_RECALL`, The Prize Exchange; designed (not wired yet)). the Lumen Arcade floor manager, Lumen Arcade Dept. Store (183). Unlock: Badges ≥ 3. Five display appliances have walked off the shop floor. They were not supposed to be able to walk. Reward: Exp. Candy M x2; +3 pts.

**Event Pokémon:**

- **Porygon Lv 24 (DOWNLOAD)**: gift, Meridian Spire lobby. Cancel the form that cancels the form. *(designed, not implemented)*

**The Eevee Octave, singer 3 of 8: Cadence** (*Off the Beat*, the Lowlight steps): Klink 25 @Oran Berry, Jolteon 26 @Sitrus Berry. Because 181 is replaced by 608 after the Shatter, the Trials owner still has to close or move this quest (24_SCRIPT note).

**Mega Stones and Z-crystals:**

- **Manectite** (Mega Stone, from Badge 2): The Prize Exchange, rank 3 (Fellow). Trial rank reward ZENITH. *(planned: map not built)*
- **Ampharosite** (Mega Stone, from Badge 3): Ferrow Lighthouse lamp room: Hesper's lamp lens. quest EL_LAMP_LENS.

### Gym 4 — the Circuit Gym (Rook Calder) *(design only; map not built)*

- **Puzzle (5/10, about 15 minutes): "route the power, never the alarm."** Conduit nodes rotate; power flows from a generator through matching ports to whatever lamps it reaches.
    - *Switchroom (190):* turn node 1 and node 3 once. "Chat says turn the sideways ones. Chat is, for once, right."
    - *Breadboard Hall (191):* tee nodes split the power, and one lamp is Rook's camera "alarm", which resets the board. The tempting middle-row route lights the alarm; the door route bends north at the generator: node (1,0) +1, node (2,0) +1, node (0,1) +2 (4 clicks). The side door to the Edit Bay: node (0,1) +1, node (1,2) +1.
    - *Live Wire Hall (192):* Rook's **Rotom drone** is a portable wire you dock into a gap, and latching relays stay open after the power is cut. Turn a once and b twice; dock the drone in g1 (latch L1 opens); call it back (the latch remembers); walk east and set c → 3, d → 1, e → 3; walk back and dock the drone again (power runs through L1 and lights L2); call it back and walk through to the Core.
    - *The Core (193):* Rook, with Juno and Larch in the gallery. The Plate's empty cradle.
- **Badge:** the **Arclight Badge**. **TM43 Volt Switch** and **TM70 Flash**.
- **Level cap after:** **31**. **Field move:** Flash (4 badges).
- **Mastery (optional):** the **Edit Bay** (950), through 191's side door.

# Act II — Imprints

*Act II is design only: the outline is `story/05_ACT_II.md` (with `14_WAR_AND_BLESSING.md` inserts), the teams and encounter tables are in the PBS, and the gym puzzles are designed in `GYM_PUZZLES.md`. No Act II map is built. The act opens with the PC leaving Lumen through the Shattered Lowlight (608): a shrine of soda cans has grown around Dex's glass figure, and Mandate checkpoints stand at every lift down to Nadir.*

## Chapter 6 — "What the Sand Keeps"

*The Act II opener in the Lowlight (608), then the Brass Road: the Meridian Mainline (612), Candle Down (602), the Highwold (603), the Brass Dunes (600) with Copperdune (610) and the Static Tunnels (604/605, Flash), the Rib Road (601), Sunbleach Flats (613), Duneholt (200–209, 214, Ossaria) and the Dig (210–213, Gym 5). Past the city: the Marrow Road (620) with the Ossuary of Dunes (624/625) and Sinkfield (628). Scripted (`story/25_SCRIPT_CH6.md`, counter V126 CH6_STEP 0–9); no map built. Gym 5.*

### Key events

- **The Ossuary murals and Sahar's confession.** A dune-shift uncovers the door in a giant fossil skull that Sahar opened in AF 281, reported to the Sovereign and resealed on Valen's order ("Seal it, Sahar. For the realm."). The murals show a golden king with his face chiselled out, two titans tearing the land, a chain of eighteen golden locks around a beast of eighteen lights, and the beast breaking apart over a city tipping into the sea (S116).
- **K3: Kestrel says the rumour out loud,** with his mother's Warden's veil from Gran's trunk in his hand: the Mourner is Morwen Vane, and she was "made to disappear" (⚑ `:ch6_kestrel_rumor`, S117). Around them, the Mandate's first arrests at the drill site (⚑ `:ch6_drillsite`).

### Order of events

1. **The Lowlight at dawn, two weeks on** (608, the Act II opener): a shrine of soda cans, candles and twelve chalked names round the glass ring, a Directorate barrier, and Rook on the vault step with no lights and no drone ("I'm not filming. I'm just sitting."). You can still walk through the Veil: put a hand on **Dex**'s glass shoulder and it is warm, barely, for a moment (no text says what that means). Marlo lights candles at the shrine; the Trials quest *Lowlight Lamps* (Dex's Pichu, S164) starts here.
2. **Juno's goodbye** at the top of the stairs: she is taking Rowan's seed stock down to Dr Mott's glass ward in Mirefen herself. "Write to me! Gale Post. 'Juno, Mirefen, the one wearing a tree.'" Quest log: the fifth badge is north in Duneholt.
3. **Lumen after the Shatter** (180): Mandate men on every lift down to Nadir; the lift grille has a Directorate seal with a grey ring chalked on it.
4. **The Meridian Mainline** (612): **the Checkpoint** at the signal gantries. Your hand on the scanner plate reads NULL; the officer finds you in her ledger. If you named someone else in Marchetti's Ch5 testimony you're flagged "Do not obstruct. Report movements." by the Director herself; otherwise you're on the Chair's Gala guest list ("You were THERE?"). Either way the barrier lifts.
5. **Candle Down** (602): every pilgrim cairn has twelve candles in it; through the Crownwall's one gap the **Glassfall Scar** glitters ("Nobody lights candles for those"). **The Highwold** (603): eighteen Wold Stones round a blank centre stone nobody touches.
6. **The Brass Dunes** (600), where Meridian's viaduct simply stops over a dune; **Copperdune** (610), the rail-junction caravanserai (prices in bones; Trials: the Riddle Trader, Tomb Freight, the tablet rack). A caravan child: "the sleeping red giant's turning over in his bed" (a Groudon seed). **The Static Tunnels** (604/605, Flash). **The Rib Road** (601, sandstorm) and **Sunbleach Flats** (613), with the side path to the Temple of the Noon Sun (Octave singer Sona).
7. **Duneholt, the Sandgate** (203): Kassan's licence for the Concord deep-works with the Mandate notice pasted over a corner of it; a caravan-mother says the western wells changed hands twice this year, "both times the new owners had an accent" (the war seed). Water is a bone a cup. The Pokémon Center's Gale Post has Larch's note and **Kelp Tea Bag** "Five".
8. **Sahar's Dig Lab** (209): first meeting, and warning 1 of 3: "Walk the bones, never the sand. The desert keeps everything. It just doesn't keep it where you left it." Fossil revival opens here; Trials: Kevin, the Hall of Unearthing board.
9. **The Deep-works** (204, the Aquifer Quarter, autorun after meeting Sahar): the shaft blows, three Drilbur and an Excadrill in sunburst collars scramble out, the Hollow cut their cables and caravan children herd them toward the dunes, and a Directorate squad grabs a caravan boy. ⚑ **`:ch6_drillsite`**:
    - *Help the Hollow* (`:hollow`): battle a Directorate **Sergeant**, the game's first Directorate fight; the Excadrill ("Ochre") digs away last. Directorate ambushes follow in Ch7.
    - *Help the Directorate* (`:directorate`): battle a Hollow **Bereaved**; you get the **Mandate Pass** (opens checkpoints later). They take the boy anyway. Costs Sahar's Consent in Act V.
    - *Shout for Sahar* (`:sanctuary`): she invokes the Warden's right of sanctuary ("two hundred and ninety-six years old") and the sergeant lets go. Accord Standing up.
10. **Gym 5, the Dig** (210–213): Sahar. The **Sandglass Badge**, **TM83 Bulldoze**; her excavators teach **Strength** at the gym door.
11. **The Door in the Skull** (620, the Marrow Road, after the badge): Sahar's confession (AF 281, nine diggers, four months, the burned rubbings; "I buried the truth once because I was told to. The sand has dug it up."), and warning 2.
12. **The Ossuary of Dunes** (624/625): the Unown *are* the inscription and drift through the walls; Strength boulders; the four murals in order, with Sahar at each (at the second she traces the coastline: "That's our western dunes. Before the Dry Tide was dry."). She rubs the chain mural: **Duneholt Rubbing** (key item, signed "AF 300" and, smaller, "AF 281"). *Optional:* the Unown glyph-swarm guardian in the Script Vault (625) for an **Unown** and the **Unown Report**; the Spiritomb static and the Odd Keystone are here too.
13. **The Ossuary's mouth:** comedy scene "Lecture, Archaeological" (adapted: "You leaned on it." "It was loose." "Things are not 'loose' around you. Things give up."), then Kestrel drops off the skull's brow: **K3** (`:DESERT`).
14. ⚑ **`:ch6_kestrel_rumor`**: *"Then go and find out."* (Bond +2 now, −3 at Ironreach when it isn't her) / *"It might not be her, Kestrel."* (−1 now, +2 at Ironreach: "You said it might not be. I hate that you were right.") / *silence*. He heads east after the Hollow cell, toward Mirefen.
15. *Optional:* **Sinkfield** (628, `:BLEED`; checkpoint at the entrance): warning 3 is pinned to the first rib. ☠ **`GO_SINKFIELD` "Sinkfield"**: step off the bones for the glint on the sand (three confirmations).
16. **Cliffhanger:** a Gale Post courier with Juno's letter from Mirefen (green ink): Rowan "burned his hand on the kettle" the night of the Lowlight, right palm, and "He's been 'away on Warden business' every time something happens. Every time. I counted. ... Come to Mirefen? Bring snacks." V102 = 7.

### Areas *(design only; maps not built)*

| Map (ID) | Field | Built? | Wild Pokémon (from `pbs/encounters.txt`) |
|---|---|---|---|
| The Meridian Mainline (612) | Mountain (`:MOUNTAIN`) | no | _no wild table yet_ |
| Candle Down (602) | Meadow (`:MEADOW`) | no | _no wild table yet_ |
| The Highwold (603) | Meadow (`:MEADOW`) | no | _no wild table yet_ |
| The Brass Dunes (600) | Desert (`:DESERT`) | no | Grass: Sandshrew 23–27, Silicobra 23–27, Rufflet 23–27, Electrike 23–27, Cacnea 23–27, Hippopotas 23–27, Trapinch 23–27, Phanpy 23–27, Vullaby 23–27, Wattrel 23–27, Flamigo 24–27, Orthworm 24–27 |
| Copperdune (610) | Desert (`:DESERT`) | no | _no wild table yet_ |
| Static Tunnels (604) | Cave (`:CAVE`) | no | Cave: Zubat 24–28, Noibat 24–28, Magnemite 24–28, Klink 24–28, Durant 24–28, Joltik 24–28, Orthworm 24–28, Golett 24–28, Tynamo 24–28, Pawmi 24–28 |
| Static Tunnels Depths (605) | Cave (`:CAVE`) | no | Cave: Golbat 26–29, Noibat 26–29, Golett 26–29, Gastly 26–29, Bronzor 26–29, Magneton 26–29, Klink 26–29, Durant 26–29, Pawmo 26–29, Tynamo 26–29, Aron 26–29 |
| The Rib Road (601) | Desert (`:DESERT`) | no | Grass: Sandile 25–29, Trapinch 25–29, Hippopotas 25–29, Silicobra 25–29, Sandshrew 25–29, Baltoy 25–29, Nacli 25–29, Klawf 25–29, Rockruff 25–29, Sigilyph 26–29, Heatmor 26–29 |
| Sunbleach Flats (613) | Desert (`:DESERT`) | no | _no wild table yet_ |
| Duneholt - Terrace Bazaar (200) | Desert (`:DESERT`) | no | Surf: Barboach 30–36, Wooper 30–36, Quagsire 32–36, Lotad 30–36; Old Rod: Magikarp 22–28, Barboach 22–28; Good Rod: Barboach 24–30, Goldeen 24–30, Basculin 24–30 |
| The Marrow Road (620) | Desert (`:DESERT`) | no | Grass: Krokorok 27–31, Hippopotas 27–31, Mudbray 27–31, Silicobra 27–31, Cacnea 27–31, Trapinch 27–31, Sandshrew 27–31, Naclstack 27–31, Sigilyph 28–31, Helioptile 27–31, Klawf 27–31, Maractus 28–31 |
| Ossuary of Dunes (624) | Cave (`:CAVE`) | no | Cave: Sandygast 28–32, Yamask 28–32, Baltoy 28–32, Golett 28–32, Cubone 28–32, Rolycoly 28–32, Diglett 28–32, Onix 28–32, Bronzor 28–32, Unown 28–32, Greavard 28–32, Lunatone 28–32 |
| Ossuary of Dunes - Script Vault (625) | Cave (`:CAVE`) | no | Cave: Unown 30–33, Baltoy 30–33, Golett 30–33, Sandygast 30–33, Carkol 30–33, Bronzor 30–33, Honedge 30–33, Onix 30–33, Lunatone 30–33, Solrock 30–33 |
| Sinkfield (628) | The Bleed (`:BLEED`) | no | Grass: Palpitoad 30–34, Gastrodon 30–34, Quagsire 30–34, Galarian Stunfisk 30–34, Alolan Diglett 30–34, Golett 30–34, Sandygast 30–34, Whiscash 30–34, Nincada 30–34, Sandaconda 32–34, Mudsdale 30–34, Dwebble 30–34 |

### Key battles

**Gym 5 — Warden Sahar Ostrand** (Ground, `:DESERT`, single battle, cap 31)

| Pokémon | Lv | Item | Ability | Moves |
|---|---|---|---|---|
| Hippopotas | 29 | Smooth Rock | Sand Stream | Sand Tomb, Bite, Yawn, Stealth Rock |
| Sandaconda | 30 | Telluric Seed | Sand Spit | Bulldoze, Brutal Swing, Glare, Rock Tomb |
| Krokorok | 30 | Eviolite | Moxie | Crunch, Dig, Sand Tomb, Fire Fang |
| Claydol "Effigy" | 31 | Soft Sand | Levitate | Earth Power, Extrasensory, Ancient Power, Rapid Spin |

*Bag: Super Potion, Super Potion; IV 18.*

- **Hard:** Hippopotas 30 @Smooth Rock, Dugtrio 29 @Focus Sash, Sandaconda 31 @Telluric Seed, Krokorok 31 @Eviolite, Claydol 31 @Sitrus Berry
- **Casual:** Hippopotas 27 @Smooth Rock, Krokorok 28 @Eviolite, Claydol 29 @Soft Sand

Her pre-battle line changes with `:ch6_drillsite`; her ace is Claydol "Effigy".

*Field note:* "dig down, because what you need is buried." Desert boosts Ground and Fire ×1.2, dulls Water (×0.8) and Ice (×0.75), keeps sand abilities on without weather, and her Ground types burrow (special attacks against them ×0.67). *Tip:* physical Water and Grass attacks; rain or three Water moves wake a Superbloom, which is the field's own answer. Sandstorm or Fire Fang bakes it back.

**The Deep-works** (`:DESERT`, one of two by your choice): a Directorate **Sergeant** (a new Duneholt version of `MERIDIAN_DIRECTORATE`: Magnemite, Pawniard, Klefki, Lv 28–30) or a Hollow **Bereaved** (a Duneholt `HOLLOW_GRUNT_M`: Sandile, Drilbur, Nickit). *Neither team is in PBS yet; the script's trainer-designer note gives these species.*

**K3 — Kestrel, the Ossuary's mouth** (`:DESERT`)

| Pokémon | Lv | Item | Ability | Moves |
|---|---|---|---|---|
| Staravia | 33 | Sharp Beak | Intimidate | Aerial Ace, Quick Attack, Take Down, Double Team |
| Scyther | 33 | Eviolite | Technician | Aerial Ace, Bug Bite, Quick Attack, Swords Dance |
| Krokorok | 33 | Soft Sand | Moxie | Crunch, Dig, Sand Tomb, Swagger |
| Doublade "Morwen" | 34 | Eviolite | No Guard | Slash, Shadow Sneak, Iron Head, Aerial Ace |
| **Starter**† | 35 | Oran Berry | (slot 0) | (regenerated for the swapped species) |

*Bag: Hyper Potion, Hyper Potion; IV 18.*

- **Hard:** Staravia 34 @Sharp Beak, Scyther 34 @Eviolite, Krokorok 34 @Eviolite, Doublade 35 @Eviolite, Starter 35 @Sitrus Berry
- **Casual:** Staravia 31 @Sharp Beak, Doublade 32 @Eviolite, Starter 33 @Oran Berry

† The rival's starter is written as the Gen 1 line in PBS; Prismfall Core swaps it at battle start for the same-generation counterpart of your starter (same stage).

*Tip:* Krokorok's Moxie snowballs; Scyther (Technician) and Staravia hit hard on Desert's Fire-and-Ground slant. Doublade (Eviolite) is a wall: Fire, Ghost or Dark.

**Optional — the Unown glyph guardian** *(planned multi-bar boss; not in the data yet).*

### Side quests

- **Ten Years of Light** (`ZE_LOWLIGHT_LAMPS`, The Prize Exchange; designed (not wired yet)). a Lowlight lamp-tender, the Lowlight (Shattered) (608). Unlock: S114 CH5_SHATTER. After the Shatter, someone has been lighting small lamps at the feet of the glassed people. Nobody admits to it. Reward: Pichu "Spark" Lv 25 (LIGHTNINGROD); +3 pts.
- **The Noon Bell** (`OS_OCTAVE_NOON_BELL`, The Rolls of Unearthing; wired (playable)). Sona of the Octave, the Temple of the Noon Sun, outside Duneholt (new map, off Sunbleach Flats 613) (215). Unlock: Badges ≥ 4. Clay tablet: the old sun temple's light-shaft has filled with sand. Its keeper needs diggers. Its keeper says she knew you'd read this. Reward: $1500, Sun Stone; +3 pts.
- **Kevin** (`OS_KEVIN`, The Rolls of Unearthing; designed (not wired yet)). the Dig Lab interns, the Dig Lab, Duneholt (209). Unlock: Badges ≥ 4. The interns revived a fossil they can't identify. They call it Kevin. Kevin is a rock. Kevin is in the staff photo. Reward: Carbink "Kevin" Lv 28 (STURDY); +2 pts.
- **The Riddle Trader** (`OS_RIDDLE_CARAVAN`, The Rolls of Unearthing; designed (not wired yet)). a caravan trader, Copperdune caravanserai (610). Unlock: Badges ≥ 4. A caravan trader only barters in riddles. She doesn't know the answers either. She wants you to find them. Reward: Trapinch Lv 27 (SHEERFORCE); +2 pts.
- **Tomb Freight** (`OS_TOMB_FREIGHT`, The Rolls of Unearthing; designed (not wired yet)). the freight-depot foreman, Copperdune (610). Unlock: Badges ≥ 4. A locked railway car bound for Lumen is heavier than its manifest. Meridian says machine parts. The tomb-guild says grave goods. Reward: $3500; +3 pts.
- **The Mural Gallery's Missing Letter** (`OS_UNOWN_MURALS`, The Rolls of Unearthing; designed (not wired yet)). Curator-Elect Nasrin Vael, the Mural Gallery, Duneholt (207). Unlock: S116 CH6_OSSUARY_DONE. One Unown is missing from the gallery's great inscription, and the sentence is wrong without it. Reward: TM28 Dig; +3 pts.

**Event Pokémon:**

- **Pichu "Spark" Lv 25 (LIGHTNINGROD)**: gift, Dex's shrine in the Shattered Lowlight. Sit with the shrine at dusk. *(designed, not implemented)*
- **Carbink "Kevin" Lv 28 (STURDY)**: gift, the Dig Lab, Duneholt. Wake Kevin. *(designed, not implemented)*
- **Trapinch Lv 27 (SHEERFORCE)**: gift, Copperdune. Answer the riddle trader's riddles. *(designed, not implemented)*

**The Eevee Octave, singer 4 of 8: Sona** (the Temple of the Noon Sun, off Sunbleach Flats; its map ID is unsettled: EEVEE_OCTAVE says 606 (new), TRIALS_QUESTS says 215, which GYM_PUZZLES uses for the Gym 5 Mastery, and the Ch6 script asks for one of 606, 607, 609 or 614–619): Baltoy 29 @Oran Berry, Espeon 30 @Sitrus Berry.

**Mega Stones and Z-crystals:**

- **Steelium Z** (Z-crystal, from Badge 4): Static Tunnels Depths, the magnetite seam (Flash). hidden; "rings and waits". *(planned: map not built)*

### Gym 5 — the Dig (Sahar Ostrand) *(design only)*

- **Puzzle (5/10, 15–20 minutes): "sun hardens, shade sinks."** Sand lanes in a sunbeam bake into walkable crust; lanes in shade are soft and drop you to the **Under-Dig** below, at the same tile. Sun-mirrors choose which lanes are lit. Falling isn't failing: a drop is the fastest way across.
    - **Solution (verified):** walk lane a to T1 → step onto lane c (soft), drop into the Under-Dig and follow the dig tunnel to the ladder (23,12), up to T2 → turn mirror M2 twice (lane c is now crust) → step onto lane b (soft), drop, take the ladder (11,20) up to T0 → walk lane a to T1, then the now-lit lane c to T3 and the stairs.
- **Badge:** the **Sandglass Badge**. **TM83 Bulldoze.** **Level cap after: 35.** **Field move:** Strength (HM04, the excavators at the gym door; 5 badges).
- **Hints:** Aide Nadim ("Lane c's mirror is on the east terrace. Fall into c and see where it takes you.").
- **Mastery (optional):** the Mural Gallery (215), behind a Rock Smash door: rub the mural Sahar sealed.

---

## Chapter 7 — "The Quiet Ward"

*The Leach Road: the Marrow Road's east end (620), the Kneeling Stones (632), the Leach Canyons (621) with Charwell (630), Wormwood Lea (634), the Gutterfall (633) down into Nadir; Mirefen (220–223) with the Sweet Market and Corvin's Infirmary (223), the Weeping Fen (648), the Infirmary gym (230–233, Gym 6); optional: the Miasma Caverns (644/645). Scripted (`story/26_SCRIPT_CH7.md`, counter V127 CH7_STEP 0–7, Sweetrot counter V128); no map built. Gym 6.*

### Key events

- **J2 and the ledger.** Alphabetising Corvin's ledgers, Juno finds an entry from the night of the Shatter: *"R.A. Second-degree Bleed-burn, right palm and fingers. Lightning pattern. Discretion."* Her uncle wrote that he burned his right hand on the kettle that night. (⚑ `:ch7_ledger`, S118)
- **The Ward Night** (creator-approved canon, 2026-11-21). The night of Sable's broadcast the Hammer cuts the Infirmary's current, the Quiet Ward's Bleed rises into a Veil across the door, and only you can walk in: you carry out **Ama**, the nine-year-old with salt-white hair, and under the glass her eyes are moving. Corvin: "They're not dying. They're *dreaming*."

### Order of events

1. **The Kneeling Stones** (632, Ossaria's crossroads: Vigil is closed "BY ORDER OF THE EMBALMERS. WE'RE BUSY."), **the Leach Canyons** (621; Lumen's foundry runoff in the river) and **Charwell** (630, a cliff-cave town of char-burners; Trials: *Clean Water*, the chalk wall). If you helped the Hollow at Duneholt (`:ch6_drillsite` = hollow), **"Escort"**: two Directorate officers try "an arrest with good manners" at the narrows (a double battle).
2. **Wormwood Lea** (634, Elowen's wormwood stills) and **the Gutterfall** (633): **"Down"**, the lift-cage beside the blue waterfall into **Nadir**, where the sky becomes a ceiling of pipes and girders and the air tastes of pennies. "Down's a copper. Up's a silver."
3. **Mirefen** (220): stilt-houses over a marsh that glows blue at the edges, and on every wall the Hollow Ring beside a painted Ogre in a sad mask (Nadir's folk-saint: "HE TALKED. HE DIDN'T STEAL."). The noodle-cart cook rates everyone out of ten and saw a boy in a black coat two days ago (three out of ten). Trials: *A Five Out of Ten* (Corvin has a two), *Lamps Out* (Noct of the Octave), the Gutter Book's chalk board.
4. **Sweetrot, offer 1** in the Sweet Market: pastel sweets, peaches and something under the peaches, and every vendor with the same smile. ☠ **`GO_SWEET_TOOTH` "Sweet Tooth"**: accept all three offers (the market, again after J2, and "the pink" outside the Pokémon Center the evening before the gym, behind a checkpoint); Wenlow warns you after the first and panics after the second.
5. **The Infirmary** (223): **Wenlow** introduces you to every patient in the Quiet Ward by name (Mister Garrod who hums, Old Fen who cheats at cards, the Tull twins, and **Ama**, nine, whose hair has turned to salt). **Corvin Mott**: "I've a ward of forty patients slowly turning into garden furniture."
6. **"R.A."** in the dispensary, then **J2** on the stilt-walk ("I need to hit something that isn't a thought."; mid-battle: "He wouldn't. He WOULDN'T."). ⚑ **`:ch7_ledger`**: *"Rowan Ashby."* (Juno's Bond −3 now, +2 at Ironreach: she already knew) / *"There's loads of R.A.s."* (+2 now, −2 at Ironreach) / *ask Corvin later, alone* ("I'm a doctor. I treat hands. I don't ask whose.").
7. **The Weeping Fen** (648, `:BLEED`; rain falls *up*): **Brother Wick** in a drowned chapel, blessing four dying Bereaved from the Lowlight's edge. He doesn't fight if your Hollow Standing is ≥ 4 or you told the Directorate "somebody else" in Ch5; otherwise a short battle. The **Wound Doctrine** ("nobody bleeds for three hundred years from a gift"), the Mourner came back from Lumen with his hand burned, and *"He doesn't want to break them any more. He wants to carry them home."* He looks at the scar on your chest and says nothing. (S119)
8. Comedy scene **"Invoice"** back at the Infirmary: Corvin's first bill (every invoice totals ₽0; a running gag).
9. **Gym 6, the Infirmary:** Corvin, a double battle ("nobody in Nadir ever has only one thing wrong with them"). The **Remedy Badge**, **TM84 Poison Jab**; the ferrymen teach **Surf**.
10. **The Ward Night** (above), on the Infirmary roof over bog coffee: Sable on every screen in Nadir ("The Mourner's gone soft. ... The Hammer hasn't. ... Cindervault's next."), the lamps die, the dampers fail, and Juno and Wenlow run the peat-fired seed-medicine stills to the damper coils while you carry Ama out. The Veil sinks back, Mister Garrod starts humming again, and Old Fen winks. Corvin: "You saw it too. So now there's two of us. Two's a study." Juno: "She doesn't sound sad. She sounds like she's enjoying it." **No jokes from the lights going out to the dampers coming back.**
11. **Morning** (the chapter close): every Hollow Ring in Mirefen painted over with a hammer, and under one, chalked, "NOT OURS. — the Hollow". Juno stays with Corvin until the Conclave. Quest log: the seventh badge, across Lake Sallow in Cindervault. V102 = 8.

### Areas *(design only; maps not built)*

| Map (ID) | Field | Built? | Wild Pokémon (from `pbs/encounters.txt`) |
|---|---|---|---|
| The Kneeling Stones (632) | Desert (`:DESERT`) | no | _no wild table yet_ |
| The Leach Canyons (621) | Wasteland (`:WASTELAND`) | no | Grass: Ekans 29–33, Gulpin 29–33, Shroodle 29–33, Maschiff 29–33, Skorupi 29–33, Croagunk 29–33, Trubbish 29–33, Drilbur 29–33, Krokorok 29–33, Makuhita 29–33, Grimer 29–33, Mudbray 29–33, Glimmet 29–33 |
| Charwell (630) | Wasteland (`:WASTELAND`) | no | _no wild table yet_ |
| Wormwood Lea (634) | Meadow (`:MEADOW`) | no | _no wild table yet_ |
| The Gutterfall (633) | Corrosive Mire (`:CORROSIVE_MIRE`) | no | _no wild table yet_ |
| Mirefen (220) | Corrosive Mire (`:CORROSIVE_MIRE`) | no | Surf: Wooper 31–37, Lombre 31–37, Skrelp 31–37, Mareanie 31–37, Quagsire 31–37; Old Rod: Magikarp 26–31, Qwilfish 26–31, Barboach 26–31; Good Rod: Qwilfish 27–34, Skrelp 27–34, Barboach 27–34 |
| Miasma Caverns (644) | Corrosive Mire (`:CORROSIVE_MIRE`) | no | Cave: Golbat 32–37, Grimer 32–37, Koffing 32–37, Trubbish 32–37, Whirlipede 32–37, Skrelp 32–37, Croagunk 32–37, Haunter 32–37, Foongus 32–37, Nidorina 32–37, Nidorino 32–37, Glimmet 32–37; Surf: Grimer 32–37, Skrelp 32–37, Mareanie 32–37 |
| Miasma Caverns B1F (645) | Corrosive Mire (`:CORROSIVE_MIRE`) | no | Cave: Golbat 34–37, Salandit 34–37, Skorupi 34–37, Toxel 34–37, Alolan Grimer 34–37, Ariados 34–37, Gloom 34–37, Muk 36–37, Weezing 35–37, Garbodor 36–37, Scolipede 34–37, Glimmet 34–37 |
| The Weeping Fen (648) | The Bleed (`:BLEED`) | no | Grass: Galarian Corsola 34–38, Koffing 34–38, Mareanie 34–38, Shiinotic 34–38, Salandit 34–38, Skuntank 34–38, Gloom 34–38, Toxel 34–38, Skrelp 34–38, Galarian Weezing 35–38 |

- **Miasma Caverns** (644/645): Venam's cameo (after Gym 6 and J2). **Lake Sallow** (641) opens with Surf after the badge (Chapter 8's road).

### Key battles

**J2 — Juno, Mirefen's stilt-walk** (`:CORROSIVE_MIRE`)

| Pokémon | Lv | Item | Ability | Moves |
|---|---|---|---|---|
| Whimsicott | 33 | Sitrus Berry | Prankster | Leech Seed, Energy Ball, Misty Terrain, Moonblast |
| Floette "Everbloom" | 33 | Sitrus Berry | Flower Veil | Petal Blizzard, Magical Leaf, Wish, Fairy Wind |
| Lilligant | 33 | Miracle Seed | Own Tempo | Energy Ball, Teeter Dance, Sleep Powder, Quiver Dance |
| Steenee "Sweetpea" | 34 | Eviolite | Leaf Guard | Razor Leaf, Stomp, Rapid Spin, Play Nice |
| **Starter**† | 35 | Oran Berry | (slot 0) | (regenerated for the swapped species) |

*Bag: Hyper Potion, Hyper Potion; IV 18.*

- **Hard:** Whimsicott 34 @Sitrus Berry, Floette 34 @Sitrus Berry, Lilligant 34 @Miracle Seed, Steenee 35 @Eviolite, Starter 35 @Sitrus Berry
- **Casual:** Whimsicott 31 @Sitrus Berry, Steenee 32 @Eviolite, Starter 33 @Oran Berry

† The rival's starter is written as the Gen 1 line in PBS; Prismfall Core swaps it at battle start for the same-generation counterpart of your starter (same stage).

*Field note:* on Corrosive Mire, Grass moves also hit as Poison, so her Grass team is more dangerous than it looks; Juno's Misty Terrain can cleanse the field. *Tip:* Fire and Flying; Floette "Everbloom" has Flower Veil, so lower-stat tricks on her Grass partners fail.

**Brother Wick** (`HOLLOW_WICK`, the drowned chapel; only if you can't talk him down; the script says `:BLEED`, FIELD_DEFAULTS gives Wick `:HOLLOW_CATHEDRAL`)

| Pokémon | Lv | Item | Ability | Moves |
|---|---|---|---|---|
| Chimecho | 33 | Sitrus Berry | Levitate | Heal Bell, Echoed Voice, Extrasensory, Yawn |
| Bronzong | 33 | Sitrus Berry | Levitate | Gyro Ball, Extrasensory, Confuse Ray, Safeguard |
| Musharna | 34 | Sitrus Berry | Forewarn | Dazzling Gleam, Psybeam, Moonlight, Yawn |
| Gardevoir | 34 | Sitrus Berry | Synchronize | Dazzling Gleam, Psychic, Heal Pulse, Calm Mind |
| Dusclops "Sexton" | 35 | Eviolite | Pressure | Night Shade, Shadow Sneak, Will-O-Wisp, Pain Split |

*Bag: Hyper Potion, Hyper Potion; IV 18.*

- **Hard:** Chimecho 34 @Sitrus Berry, Bronzong 34 @Sitrus Berry, Musharna 35 @Sitrus Berry, Gardevoir 35 @Sitrus Berry, Dusclops 35 @Eviolite
- **Casual:** Chimecho 31 @Sitrus Berry, Musharna 32 @Sitrus Berry, Dusclops 33 @Sitrus Berry

**"Escort"** (the Leach Canyons, only after `:ch6_drillsite` = hollow): two Directorate Officers, a double (a Leach version of `MERIDIAN_DIRECTORATE`, Lv 31–33; not in PBS yet).

**Gym 6 — Warden Corvin Mott** (Poison, `:CORROSIVE_MIRE`, cap 35, **double battle**)

| Pokémon | Lv | Item | Ability | Moves |
|---|---|---|---|---|
| Weezing | 33 | Black Sludge | Levitate | Strange Steam, Sludge, Heat Wave, Protect |
| Amoonguss | 34 | Black Sludge | Effect Spore | Giga Drain, Clear Smog, Stun Spore, Protect |
| Crobat | 33 | Synthetic Seed | Inner Focus | Cross Poison, Wing Attack, Bite, Tailwind |
| Drapion | 34 | Scope Lens | Sniper | Poison Fang, Knock Off, Fell Stinger, Protect |
| Toxapex "Ward" | 35 | Black Sludge | Merciless | Venoshock, Scald, Baneful Bunker, Recover |

*Bag: Hyper Potion, Hyper Potion; IV 18.*

- **Hard:** Weezing 34 @Black Sludge, Amoonguss 35 @Black Sludge, Crobat 34 @Synthetic Seed, Salazzle 34 @Black Sludge, Drapion 35 @Life Orb, Toxapex 35 @Rocky Helmet
- **Casual:** Weezing 31 @Black Sludge, Amoonguss 32 @Black Sludge, Drapion 32 @Scope Lens, Toxapex 33 @Black Sludge

*Field note:* "poison is a dose; the right amount heals." Poison ×1.5 and its added effects ×1.5 as likely; Poison hits Steel; Grass and mud moves also hit as Poison. Galarian Weezing's Heat Wave twice turns it to Wasteland. *Tip:* Ground and Psychic; Steel is no longer safe here. Misty Terrain or Purify cleans the field into Water Surface.

### Side quests

- **Lamps Out** (`NA_OCTAVE_LAMPS_OUT`, The Gutter Book; wired (playable)). Six-Fingers Ottoline (chalk job) / the marsh ferryman, the ferry steps on the runoff marsh, Mirefen (at night) (220). Unlock: Badges ≥ 5. Chalk job: someone keeps putting out the night-ferry lamps on the marsh. The ferrymen pay a cut to whoever stops it. Reward: $1000, Dusk Ball x5; truth: $1000; covered: HOLLOW+1; +3 pts.
- **Clean Water** (`NA_CLEAN_WATER`, The Gutter Book; designed (not wired yet)). a char-burner, Charwell (630). Unlock: Badges ≥ 5. Ossarian bone-char filters clean Nadir's poison. Someone is skimming the filter carts. Find who, then decide who you tell. Reward: $3000; +3 pts.
- **A Five Out of Ten** (`NA_NOODLE_SCORE`, The Gutter Book; designed (not wired yet)). the noodle-cart cook, Mirefen (220). Unlock: Badges ≥ 5. Mirefen's noodle cart rates its customers out of ten. Nobody has scored above a four. Corvin has a two and comes daily. Reward: Alolan Grimer Lv 30 (POISONTOUCH); +2 pts.
- **Sewer Royalty** (`NA_VENAM`, The Gutter Book; designed (not wired yet)). Six-Fingers Ottoline, the Miasma Caverns under Mirefen (644). Unlock: Badges ≥ 6 and S118 CH7_J2_DONE. Somebody has crowned herself queen of the Miasma Caverns. Ottoline wants to know who's charging tolls on her sumps. Reward: Black Sludge; +3 pts.
- **Something in the Sinkholes** (`OS_SINKFIELD`, The Rolls of Unearthing; designed (not wired yet)). a Sinkwells water-carrier, Sinkfield (628). Unlock: Badges ≥ 5. Something flat and grinning is dragging water-carriers' Pokemon into the Sinkfield sinkholes. Reward: Galarian Stunfisk Lv 31 (MIMICRY); +4 pts.
- **Sewer Royalty** (cameo, Venam; CAMEOS §2): after Gym 6 and J2, a punk girl with a Seviper is dragging Sweetrot addicts out of the Miasma Caverns. A tunnel crawl with her as a partner, then her farewell fight: Toxtricity 35 @Throat Spray, Garbodor 35 @Rocky Helmet, Muk 36 @Assault Vest, Salazzle 36 @Black Sludge, Toxicroak 37 @Synthetic Seed, Seviper 38 @Life Orb (`:CORROSIVE_MIRE`). Reward: **Venam's Testimony** ("I could hear everything") — one of the three proofs for Envoy Okoro in Ch20, playable for Juno in Ch10 — and Black Sludge.

**Event Pokémon:**

- **Alolan Grimer Lv 30 (POISONTOUCH)**: gift, the Mirefen noodle cart. Score a five out of ten. *(designed, not implemented)*
- **Galarian Stunfisk Lv 31 (MIMICRY)**: boss battle, then it joins, Sinkfield. Beat the sinkhole boss. *(designed, not implemented)*

**The Eevee Octave, singer 5 of 8: Noct** (*Lamps Out*, the night ferry steps): Murkrow 33 @Oran Berry, Umbreon 34 @Sitrus Berry.

**Mega Stones and Z-crystals:**

_None placed for this chapter._

### Gym 6 — the Infirmary (Corvin Mott) *(design only)*

- **Puzzle (6/10, about 20 minutes): "dose makes the cure."** Unmarked flasks of 3 and 5 measures; funnels and basins accept exact doses; the tap is the only place to fill.
    - *The Ward (230):* one flask, one dose.
    - *Dispensary (231):* make 4 from 3 and 5. **Solution (6 actions):** fill 5 → pour 5 into 3 (5 holds 2) → tip the 3 → pour 5 into 3 (3 holds 2) → fill 5 → pour 5 into 3 (5 holds 4) → pour the 5 into the funnel. Wenlow's hints: "the empty space is a measure too"; "get a 2 into the little one first".
    - *Sludge Gallery (232):* carry the doses across a toxic gallery on a mask-filter step budget; one basin is cumulative, so plan your trips.
- **Badge:** the **Remedy Badge**. **TM84 Poison Jab.** **Level cap after: 39.** **Field move:** Surf (HM03, the ferrymen; 6 badges).
- **Mastery (optional):** the gym's Quiet Ward room (234): the same rule with 4 and 9. (The story's Ward Night is staged on the Infirmary's own top floor, 223, not here.)

---

## Chapter 8 — "The Light Stone"

*The Sulfur Road: Leechman's Walk (640), Lake Sallow (641, Surf) with Scaldwater (650) and Lantern Isle (658, optional), the Pyre Road (652) into Ashkaar; Cindervault (240–254) inside the Cinderhorn's caldera, the Cinderhorn (664–666) and Emberfall (668). Design only. Gym 7. Script: `story/29_SCRIPT_CH8.md` (the withdrawn Ring-Day draft is archived at `story/archive/22_SCRIPT_CH8_withdrawn.md`; SPINE Rev 21 moved the Ring-Day to Ch14).*

### Key events

- **The Caldera Crisis** (⚑ `:ch8_caldera`): three factions on one caldera floor, and the first Meridian admin fight (Dr. Quent).
- **The Light Stone** (⚑ `:ch8_lightstone`) and the Dominar closing the eastern passes: the war starts walking.

### Order of events

1. **Leechman's Walk** out of Mirefen, then **Lake Sallow**'s sulfur shallows by Surf (**Scaldwater**; optional **Lantern Isle**). The **Pyre Road** climbs into **Ashkaar, the Dragonfire Dominion**: black basalt, red lacquer banners, oaths sworn over braziers. An early NPC teaches the law: "Say true or say nothing, stranger."
2. **Cindervault:** a forge-city inside the caldera. Warden **Brann Holloway** drops his hammer to bear-hug Larch, then you ("The Hug", the comedy scene). Two crises: Meridian's geothermal tap is overdrawing the Flame Plate (the forges run too hot), and the **Dominar's envoys** demand the **Light Stone** (Reshiram's) from the Hearthguild. The tap's manifest says *Rimeholt*: "Our fire warms our enemies' beds."
3. **Sigrun Ashfall** arrives on a Salamence to mediate: "So you're the ferry child everyone's whispering about. Hm. Smaller than I expected."
4. **Gym 7, the Foundry:** Brann. Badge 7, **TM35 Flamethrower**.
5. **The Caldera Crisis:** the tap's pressure spikes. On the caldera floor, **Wick's faithful** want to vent it with Lake Sallow water, **Dr. Percival Quent's** Meridian team wants dampers (admin battle: Quent, `:VOLCANIC`), and **the Hammer** wants a Splitter on the tap. ⚑ `:ch8_caldera`: *help Wick vent* (the field goes Volcanic → Cinderglass; the forges go cold for a season; Hollow up, Meridian down) / *help Quent's dampers* (the tap keeps running; the Bleed at Emberfall grows; Brann's Bond up) / *shut the tap down by force* (a harder fight vs Quent and the Directorate; Accord up; the Dominar is impressed; Meridian down hard). ☠ **`GO_LET_THEM_LISTEN` "Let Them Listen"**: take the Hammer bomber's detonator.
6. **The Light Stone:** the envoys try to seize it in the confusion; Sigrun stops them. ⚑ `:ch8_lightstone`: *keep it under the Hearthguild* (the Dominar's grudge grows) / *send it to Sigrun at Wyrmrest* (Sigrun's Bond and Accord up; seeds `DOMINAR_SWAYED`) / *give it to the Dominar* (Ashkaar's favour up, Accord down; Brann is hurt and won't release the Flame Plate in Act V; Reshiram's trial is harder).
7. **Brann's chestnut slip,** drunk: "I reset the Crown's stone myself, y'know. After the accident. Ten years back. It was smaller than it should've been." The PC's shard throbs; Larch notices. *(The Mega Ring is **not** given here any more; it comes after Badge 13, Ch14.)*
8. *Optional, after the badge:* the war road north from the north gate (the Cinderglass Barrens 662, Glasswake 670, the Wyrmtongue 673) shows legions drilling under Cinder Cape Warfort.
9. **Cliffhanger:** the Dominar's herald: Ashkaar holds Zenith responsible for the "assault on the Flame" and **closes the eastern passes**. War-drums. Sigrun says nothing.

### Areas *(design only; maps not built)*

| Map (ID) | Field | Built? | Wild Pokémon (from `pbs/encounters.txt`) |
|---|---|---|---|
| Leechman's Walk (640) | Corrosive Mire (`:CORROSIVE_MIRE`) | no | Grass: Ekans 31–35, Gulpin 31–35, Stunky 31–35, Salandit 31–35, Bellsprout 31–35, Foongus 31–35, Shroodle 31–35, Toedscool 31–35, Croagunk 31–35, Seviper 31–35, Zangoose 31–35, Lombre 31–35, Carnivine 32–35; Surf: Wooper 31–36, Lombre 31–36, Skrelp 31–36, Mareanie 31–36, Quagsire 31–36; Old Rod: Magikarp 30–34, Qwilfish 30–34; Good Rod: Qwilfish 31–35, Skrelp 31–35, Corphish 31–35 |
| Lake Sallow (641) | Cinderglass (`:ASHEN_WASTE`) | no | Grass: Salandit 32–36, Numel 32–36, Scraggy 32–36, Charcadet 32–36, Pansear 32–36, Croagunk 32–36, Maschiff 32–36, Grimer 32–36, Houndour 32–36, Marill 32–36, Capsakid 32–36, Buneary 32–36; Surf: Surskit 32–36, Ducklett 32–36, Buizel 32–36, Marill 32–36, Masquerain 32–36, Psyduck 32–36; Old Rod: Magikarp 30–34, Goldeen 30–34; Good Rod: Goldeen 31–35, Poliwhirl 31–35, Basculin 31–35, Feebas 31–35 |
| Scaldwater (650) | Cinderglass (`:ASHEN_WASTE`) | no | _no wild table yet_ |
| Lantern Isle (658) | Beach (`:BEACH`) | no | Grass: Trumbeak 33–37, Steenee 33–37, Rockruff 33–37, Fomantis 33–37, Passimian 33–37, Oranguru 33–37, Comfey 33–37, Stufful 33–37, Minior 33–37, Tropius 33–37, Komala 33–37, Alolan Exeggutor 34–37, Turtonator 34–37, Drampa 34–37; Surf: Tentacool 33–37, Wingull 33–37, Pyukumuku 33–37, Mareanie 33–37, Wishiwashi 33–37, Mantyke 33–37; Old Rod: Magikarp 30–35, Wishiwashi 30–35; Good Rod: Wishiwashi 33–38, Bruxish 33–38, Corsola 33–38, Alomomola 33–38 |
| The Pyre Road (652) | Cinderglass (`:ASHEN_WASTE`) | no | _no wild table yet_ |
| Cindervault - Forge Terraces (240) | Volcanic (`:VOLCANIC`) | no | _no wild table yet_ |
| The Cinderhorn 1F (664) | Volcanic (`:VOLCANIC`) | no | Cave: Slugma 36–40, Numel 36–40, Carkol 36–40, Torkoal 36–40, Magby 36–40, Heatmor 36–40, Geodude 36–40, Golbat 36–40, Lairon 36–40, Charcadet 36–40, Durant 36–40, Larvesta 36–40 |
| The Cinderhorn 2F (665) | Volcanic (`:VOLCANIC`) | no | Cave: Magcargo 38–41, Charcadet 38–41, Coalossal 38–41, Camerupt 38–41, Magmar 38–41, Lairon 38–41, Graveler 38–41, Heatmor 38–41, Centiskorch 38–41, Durant 38–41, Turtonator 38–41, Druddigon 38–41, Larvesta 38–41 |
| The Cinderhorn Caldera (666) | Volcanic (`:VOLCANIC`) | no | Grass: Salandit 39–42, Magmar 39–42, Camerupt 39–42, Torkoal 39–42, Centiskorch 39–42, Magcargo 39–42, Turtonator 39–42, Lairon 39–42, Houndoom 39–42, Druddigon 39–42, Carkol 39–42, Larvesta 39–42 |
| Emberfall (668) | The Bleed (`:BLEED`) | no | Grass: Lampent 41–42, Alolan Marowak 39–42, Houndoom 39–42, Galarian Darumaka 39–42, Alolan Vulpix 39–42, Salandit 39–42, Oricorio 39–42, Larvesta 39–42, Heatmor 39–42, Magmar 39–42, Torkoal 39–42, Turtonator 39–42, Drampa 39–42 |

- **The Cinderhorn** (664–666, DUNGEON_PUZZLES "drain the mountain, mind the pressure", 6/10).

### Key battles

**Gym 7 — Warden Brann Holloway** (Fire, `:VOLCANIC`, single battle, cap 39)

| Pokémon | Lv | Item | Ability | Moves |
|---|---|---|---|---|
| Torkoal | 37 | Sitrus Berry | Drought | Lava Plume, Earth Power, Will-O-Wisp, Clear Smog |
| Camerupt | 37 | Cameruptite | Magma Armor | Lava Plume, Earth Power, Rock Slide, Amnesia |
| Magmortar | 38 | Charcoal | Flame Body | Flamethrower, Thunderbolt, Clear Smog, Confuse Ray |
| Arcanine | 38 | Sitrus Berry | Intimidate | Flare Blitz, Crunch, Extreme Speed, Roar |
| Coalossal "Anvil" | 39 | Sitrus Berry | Steam Engine | Tar Shot, Heat Crash, Smack Down, Rock Slide |

*Bag: Mega Ring, Hyper Potion, Hyper Potion; IV 24.*

- **Hard:** Torkoal 38 @Heat Rock, Camerupt 38 @Cameruptite, Centiskorch 38 @Charcoal, Magmortar 39 @Elemental Seed, Arcanine 39 @Sitrus Berry, Coalossal 39 @Weakness Policy
- **Casual:** Torkoal 35 @Sitrus Berry, Magmortar 36 @Charcoal, Arcanine 36 @Sitrus Berry, Coalossal 37 @Sitrus Berry

*Field note:* "a forge you can stoke or quench." Fire ×1.5, Ice ×0.5; Rock comes out superheated; quakes and eruption moves prime an eruption at the end of the round. **Mega Camerupt** (a designed "weak" Mega, Standard and Hard only, kept exactly as the user asked) primes the volcano when it Mega Evolves. *Tip:* two big Water or Ice moves, rain or sand quench the field into **Cinderglass**, where Coalossal "Anvil" is built to fight; Lava Plume ×3 re-melts it. Bring Water and Ground, and quench early.

**Dr. Percival Quent** (`MERIDIAN_QUENT`, the caldera taps, `:VOLCANIC`)

| Pokémon | Lv | Item | Ability | Moves |
|---|---|---|---|---|
| Bronzong | 37 | Damp Rock | Heatproof | Rain Dance, Gyro Ball, Extrasensory, Confuse Ray |
| Magneton | 37 | Eviolite | Sturdy | Thunder, Flash Cannon, Thunder Wave, Rain Dance |
| Castform | 38 | Sitrus Berry | Forecast | Rain Dance, Weather Ball, Thunder, Ice Beam |
| Rotom | 38 | Sitrus Berry | Levitate | Hydro Pump, Thunder, Rain Dance, Hex |
| Porygon2 "Probe" | 39 | Eviolite | Download | Tri Attack, Ice Beam, Thunderbolt, Recover |

*Bag: Hyper Potion, Hyper Potion; IV 24.*

- **Hard:** Bronzong 38 @Damp Rock, Magneton 38 @Eviolite, Castform 39 @Sitrus Berry, Rotom 39 @Sitrus Berry, Porygon2 39 @Eviolite
- **Casual:** Bronzong 35 @Sitrus Berry, Magneton 35 @Sitrus Berry, Porygon2 37 @Sitrus Berry

*Field note:* his Rain Dances are "the dampers": they quench the Volcanic field into Cinderglass.

### Side quests

- **Too Loud for the Choir** (`AS_OCTAVE_TOO_LOUD`, The Trial by Flames; wired (playable)). Forte of the Octave, the Crucible on the caldera rim, Cindervault (240). Unlock: Badges ≥ 6. Writ of Flame: a Choir singer wants a Writ. The Crucible will hear her if she brings a second. Reward: $2000, Heat Rock; +3 pts.
- **Seven Bouts** (`AS_SEVEN_BOUTS`, The Trial by Flames; designed (not wired yet)). Legate Varra Kosk, the Crucible, Cindervault (240). Unlock: Badges ≥ 6. The Crucible's entry rite: seven legion fighters, back to back, on the caldera floor. No items. No healing. No complaining. Reward: Charcoal, Fire Stone; +4 pts.
- **The Lava-Tube Terror** (`AS_DRUDDIGON`, The Trial by Flames; designed (not wired yet)). a Hearthguild smith, The Cinderhorn (664). Unlock: Badges ≥ 6. A Druddigon has made the Cinderhorn lava tubes its own. Three smiths' Pokemon came back scorched. The Legion wants it beaten, not killed. Reward: Druddigon Lv 37 (ROUGHSKIN); +4 pts.
- **Adequate Swords** (`AS_ADEQUATE_SWORDS`, The Trial by Flames; designed (not wired yet)). the owner of ADEQUATE SWORDS, Cindervault market (240). Unlock: Badges ≥ 6. A rival shop has opened across the street: EXCELLENT SWORDS. The owner of ADEQUATE SWORDS suspects a lie. Lying is a crime. Reward: Metal Coat; +2 pts.
- **Afraid of Heights** (`AS_AFRAID_OF_HEIGHTS`, The Trial by Flames; designed (not wired yet)). Recruit Tamm, the Dragon Roosts, Cindervault (248). Unlock: Badges ≥ 6. A dragon-rider recruit is afraid of heights and has been assigned a Trapinch 'until he's ready'. He has been not-ready for two years. Reward: Noibat Lv 36 (INFILTRATOR); +3 pts.
- **Ashes Home** (`AS_ASHES`, The Trial by Flames; designed (not wired yet)). the Legion quartermaster, Scaldwater (650). Unlock: Badges ≥ 6. A Nadir-born legionnaire died at the caldera. His Houndour won't leave his urn. Somebody has to carry both of them home to Scaldwater. Reward: Houndour Lv 34 (FLASHFIRE); +4 pts.
- **The Trial of Truth** (`AS_TRIAL_OF_TRUTH`, The Trial by Flames; designed (not wired yet)). Herald Pyke, the Hall of Oaths, Cindervault (247). Unlock: Badges ≥ 6 and S120 CH8_CALDERA_DONE. Ashkaar judges a lie by combat. A Hearthguild officer swears the caldera crisis wasn't the Legion's fault. You were there. Reward: Flame Orb; +4 pts.

**Event Pokémon:**

- **Deino Lv 1**: egg, The Crucible, Cindervault. Reach Pyre in the Trial by Flames.
- **Druddigon Lv 37 (ROUGHSKIN)**: boss battle, then it joins, The Cinderhorn lava tubes. Beat the lava-tube boss. *(designed, not implemented)*
- **Noibat Lv 36 (INFILTRATOR)**: gift, the Dragon Roosts, Cindervault. Train Tamm's Trapinch until it flies. *(designed, not implemented)*
- **Houndour Lv 34 (FLASHFIRE)**: gift, Scaldwater. Carry a legionnaire's urn home. *(designed, not implemented)*

**The Eevee Octave, singer 6 of 8: Forte** (*Too Loud for the Choir*, the Crucible): Carkol 37 @Oran Berry, Flareon 38 @Sitrus Berry.

**Mega Stones and Z-crystals:**

_None placed for this chapter._

### Gym 7 — the Foundry (Brann Holloway) *(design only)*

- **Puzzle (6/10, about 20 minutes): "pour, then quench."** A trench is *empty* (a gap); pour a crucible into it and it is *molten* (impassable); quench it and it is *iron* (a bridge). Crucibles pour once through spouts aimed at one of two channels, and there is **one** quench. A channel still molten when you take the slag chute drains into the mould below: a gap upstairs, a bridge downstairs.
    - **Solution (verified):** pour K3 → X1, K1 → X2, K2 → X3 (aim first) → quench X2 only → take chute C1 (X1 and X3 drain, so M1 and M3 are iron) → below, cross M1 → ladder H → back up on 251 at mid1 → cross X2 (iron) → mid2 → chute C2 → below, cross M3 → ladder → the north band → the arena door.
- **Badge:** Badge 7. **TM35 Flamethrower.** **Level cap after: 43.**
- No Mastery room is designed for this gym.

---

## Chapter 9 — "The Iron Conclave"

*The Iron Road: the Ashmarch (660), the Ironway (661), Candle Down (602), the Long Drop (672) under Zenith's west rim; optional war road (662, 670, 673); Ironreach (260–275, Nadir) with the Iron Pit (263) and the Aurel-era mine shafts. Design only. Gym 8.*

### Key events

- **The Mourner unmasked.** At the Conclave the Hammer's Splitter half-Shatters the Fist Plate; the Mourner throws himself between the glass and Juno and the child she is shielding, and his mask cracks in half: **Rowan Ashby**.
- **⚑ `:ch9_teo_sable`:** through the smoke, Teo pinned and Fixing at the Bleed's edge, and Sable running for a Meridian lift with a comm-device. You have time for one.

### Order of events

1. West out of the Dominion over the **Ashmarch** (`:ASHEN_WASTE` if Wick vented the caldera) and the **Ironway**, back across **Candle Down**, then down the shaft road of **the Long Drop** under Zenith's west rim.
2. **Ironreach:** Nadir's pit-fighting quarter in the old Aurel mine shafts; arguments are settled in chalk circles. Warden **Kaito Ren** is the only ex-Accord soldier Nadir trusts.
3. **The Accord Conclave**, the first in Nadir in a century, to vote on making the Mandate realm-wide. Every Warden you have met is here, plus first sightings of the rest (Ysolde, Nyx, Celestine "openly herself this time", Anja, Bastian pretending to be deaf). **Odessa Gale** lands a skiff on the Pit's rim and hands you **Fly** in person. Anja and the Dominar's envoy nearly come to blows; Kassan's envoy leaves with both their seals (the first copies of the Elector's Lease).
4. **The Ironreach Open** (a trainer gauntlet through the brackets; comedy scene "The Bracket" at sign-up) to the **final vs Kestrel (K4)**, `:COLOSSEUM`. The crowd chants for "the null kid".
5. **Gym 8, the Pit:** Kaito. Badge 8, **TM31 Brick Break**. "A fist is a promise. Don't make one you won't keep."
6. **The attack:** during the Mandate vote the galleries go dark; Sable's voice on the speakers. **Partner battle: you + Kestrel vs Sable + Hammer Captain Brisk** (`:COLOSSEUM`). Sable escapes into the shafts.
7. **The Mourner** (`HOLLOW_MOURNER`) over the reliquary, trying to *disarm* the charge: "Not now — you don't understand — get BACK." His ace **Trevenant "Glasswood"** is a multi-bar boss that roots itself into the pit floor at each break.
8. **The partial Shatter:** the reliquary chamber flips to the Bleed; glass races toward the gallery where Juno shields a child. The Mourner's Trevenant walls it off with roots, and his mask cracks: Rowan. *"Juno. Don't look at me like that. Look at the flowers."* Only you can walk into the Bleed to pull him out; Valen watches you do it.
9. ⚑ **`:ch9_teo_sable`** (the act's big choice): *save Teo* (`TEO_SAVED`: he lives with glassed fingers; Marisol's Bond way up; Sable's Meridian link must be proven later and harder) / *chase Sable* (`IRONREACH_EVIDENCE`: a chase battle through the shafts; you tear a comm-device with Meridian Special Accounts encryption from her belt ("Kroll, report"); **Teo dies** in the Bleed, reaching for his sister).
10. **Aftermath:** Meridian takes Rowan into its own custody under the Mandate, which just passed. Kestrel stares at Rowan's face: "...It's not her." (If you warned him in Ch6: "You said it might not be. I hate that you were right.") ⚑ `:ch9_rowan_words` as he is led away: *"Why?"* ("Ask the Drowned Crown.") / *"I'll look after her"* / *silence* ("You saw what I saw. In the Lowlight. Didn't you?").
11. ☠ **`GO_PULL_THE_NAIL` "Pull the Nail"** (only offered at high Hollow Standing): before the attack, Sable asks you to plant the charge where only you can walk.
12. **Valen** crosses the ruined Pit: *"Come to Verdance. There's a seat to fill — and I think you should see what it costs."*
13. **Interlude II, "The Bride Tree"** (play as **Rowan**, the dawn before the Conclave): he waters Elin, shows the healed Phantump (now a Trevenant), seals his Warden's ring and testament into an envelope for the Sovereign, and puts on the mask. **END OF ACT II.**

### Areas *(design only; maps not built)*

| Map (ID) | Field | Built? | Wild Pokémon (from `pbs/encounters.txt`) |
|---|---|---|---|
| The Ashmarch (660) | Cinderglass (`:ASHEN_WASTE`) | no | Grass: Slugma 35–39, Numel 35–39, Growlithe 35–39, Houndour 35–39, Fletchinder 35–39, Carkol 35–39, Sizzlipede 35–39, Capsakid 35–39, Torkoal 35–39, Skarmory 36–39, Magby 35–39, Heatmor 35–39, Charcadet 35–39 |
| The Ironway (661) | Mountain (`:MOUNTAIN`) | no | Grass: Teddiursa 37–41, Mienfoo 37–41, Primeape 37–41, Gligar 37–41, Pancham 37–41, Scraggy 37–41, Salandit 37–41, Torkoal 37–41, Flamigo 37–41, Throh 37–41, Sawk 37–41, Cyclizar 37–41, Noibat 37–41, Druddigon 38–41 |
| The Long Drop (672) | Scrapyard (`:SCRAPYARD`) | no | _no wild table yet_ |
| The Cinderglass Barrens (662) | Cinderglass (`:ASHEN_WASTE`) | no | Grass: Numel 36–40, Carkol 36–40, Krokorok 36–40, Torkoal 36–40, Vibrava 36–41, Camerupt 36–41, Heatmor 36–40, Sandaconda 36–41, Hippopotas 36–40, Magcargo 38–41, Naclstack 36–40, Druddigon 37–41, Turtonator 36–41, Larvesta 36–40 |
| Glasswake (670) | Cinderglass (`:ASHEN_WASTE`) | no | _no wild table yet_ |
| The Wyrmtongue (673) | Volcanic (`:VOLCANIC`) | no | _no wild table yet_ |
| Ironreach (260) | New Moon (`:NEW_MOON`) | no | _no wild table yet_ |
| The Iron Pit (263) | Colosseum (`:COLOSSEUM`) | no | _no wild table yet_ |

### Key battles

**K4 — Kestrel, the Ironreach Open final** (`:COLOSSEUM`)

| Pokémon | Lv | Item | Ability | Moves |
|---|---|---|---|---|
| Staraptor | 41 | Sharp Beak | Intimidate | Close Combat, Aerial Ace, Retaliate, Quick Attack |
| Krookodile | 41 | Sitrus Berry | Intimidate | Crunch, Earthquake, Rock Slide, Swagger |
| Scizor | 41 | Metal Coat | Technician | Bullet Punch, X-Scissor, Aerial Ace, Swords Dance |
| Doublade "Morwen" | 42 | Eviolite | No Guard | Night Slash, Shadow Claw, Iron Head, Swords Dance |
| **Starter**† | 42 | Sitrus Berry | (slot 0) | (regenerated for the swapped species) |

*Bag: Hyper Potion, Hyper Potion; IV 24.*

- **Hard:** Staraptor 42 @Choice Band, Zweilous 41 @Eviolite, Krookodile 42 @Life Orb, Scizor 42 @Life Orb, Doublade 43 @Eviolite, Starter 43 @Life Orb
- **Casual:** Staraptor 37 @Sharp Beak, Scizor 37 @Metal Coat, Doublade 38 @Eviolite, Starter 38 @Sitrus Berry

† The rival's starter is written as the Gen 1 line in PBS; Prismfall Core swaps it at battle start for the same-generation counterpart of your starter (same stage).

*Field note:* Colosseum: Fighting ×1.2, punches and kicks ×1.2, throws ×1.5, and every knockout rallies the crowd (+1 Attack or Sp. Atk for the finisher). *Tip:* Krookodile's Intimidate and Scizor's Technician Bullet Punch; Fire handles Scizor and Doublade. Don't give him early knockouts to snowball on.

**Gym 8 — Warden Kaito Ren** (Fighting, `:COLOSSEUM`, cap 43; GYM_PUZZLES leaves it open whether this is a tag battle with Kestrel or a single battle; Core's table gives no double rule)

| Pokémon | Lv | Item | Ability | Moves |
|---|---|---|---|---|
| Hawlucha | 41 | Synthetic Seed | Limber | Brick Break, Acrobatics, U-turn, Aerial Ace |
| Machamp | 42 | Sitrus Berry | No Guard | Dynamic Punch, Knock Off, Rock Slide, Bullet Punch |
| Hitmontop | 42 | Assault Vest | Intimidate | Fake Out, Triple Kick, Rapid Spin, Sucker Punch |
| Conkeldurr | 42 | Flame Orb | Guts | Hammer Arm, Mach Punch, Rock Slide, Bulk Up |
| Lucario "Memory" | 43 | Sitrus Berry | Inner Focus | Aura Sphere, Flash Cannon, Dark Pulse, Nasty Plot |

*Bag: Hyper Potion, Hyper Potion; IV 24.*

- **Hard:** Hawlucha 42 @Synthetic Seed, Medicham 41 @Choice Band, Machamp 43 @Sitrus Berry, Hitmontop 43 @Assault Vest, Conkeldurr 43 @Flame Orb, Lucario 43 @Life Orb
- **Casual:** Hawlucha 37 @Sitrus Berry, Machamp 38 @Sitrus Berry, Conkeldurr 38 @Sitrus Berry, Lucario 39 @Sitrus Berry

*Field note:* "the crowd's roar is a stat; earn it." Knockouts build to a **Frenzy** (Fighting ×1.5). Psychic mind games are booed (special Psychic ×0.8), so Flying and Fairy are the cleaner answers. *Tip:* Hawlucha holds the Synthetic Seed; Conkeldurr's Flame Orb Guts; Lucario "Memory" closes. Three quakes collapse the pit into a Cave.

**Sable + Hammer Captain Brisk** (tag double with Kestrel as your partner, `:COLOSSEUM`; Kestrel's partner team isn't in PBS yet)

Skuntank 41 @Sitrus Berry, Toxicroak 42 @Black Sludge, Drapion 43 @Scope Lens / Mightyena 40 @Sitrus Berry, Banette 41 @Spell Tag, Scolipede 42 @Sitrus Berry. Brisk's Bulldoze counts toward the cave-in.

**The Mourner** (`HOLLOW_MOURNER`, the reliquary, `:COLOSSEUM`, then the Bleed)

| Pokémon | Lv | Item | Ability | Moves |
|---|---|---|---|---|
| Shiftry | 42 | Sitrus Berry | Chlorophyll | Fake Out, Leaf Blade, Sucker Punch, Protect |
| Cacturne | 42 | Sitrus Berry | Water Absorb | Spiky Shield, Payback, Seed Bomb, Leech Seed |
| Gourgeist | 42 | Leftovers | Frisk | Seed Bomb, Shadow Sneak, Will-O-Wisp, Leech Seed |
| Trevenant "Glasswood" | 43 | Sitrus Berry | Harvest | Horn Leech, Shadow Claw, Will-O-Wisp, Protect |

*Bag: Hyper Potion, Hyper Potion; IV 24.*

- **Hard:** Shiftry 43 @Focus Sash, Cacturne 43 @Sitrus Berry, Gourgeist 43 @Leftovers, Trevenant 43 @Sitrus Berry
- **Casual:** Shiftry 38 @Sitrus Berry, Trevenant 39 @Sitrus Berry

*Boss:* his ace Trevenant "Glasswood" has **2 bars** (Hard 3; `MOURNER_TREVENANT`). Each break cures it, clears its stat drops, raises Defense and roots it (Ingrain heals). He fights defensively (Protect, Spiky Shield). No Mega: his ring is in an envelope in Verdance.

### Side quests

- **Pit Ringer** (`NA_PIT_RINGER`, The Gutter Book; designed (not wired yet)). the Iron Pit announcer, the Iron Pit, Ironreach (263). Unlock: Badges ≥ 7. An unlicensed pit in the old mine shafts: six fights, no breaks, and the house brings a brass formation for the last one. Reward: Falinks Lv 38 (DEFIANT); +4 pts.
- **Lamplighter Kids** (`NA_LAMPLIGHTER_KIDS`, The Gutter Book; designed (not wired yet)). Pip's friend from the lamp-runners, Ironreach (260). Unlock: Badges ≥ 7. Three lamp-runner children went into the old sumps after a rumour of treasure. Their lamps are running out. Reward: Exp. Candy M x3; +3 pts.
- **Two Lucarios** (`NA_GARRET`, The Gutter Book; designed (not wired yet)). Six-Fingers Ottoline, Ironreach's lower shafts (263). Unlock: S123 CH9_CONCLAVE_DONE. A foreign trainer is asking every pit-fighter in Ironreach the same question about his Lucario. Reward: Black Belt; +3 pts.
- **The Egg Run** (`AS_EGG_RUN`, The Trial by Flames; designed (not wired yet)). the Roost-mistress, the Dragon Roosts, Cindervault (248). Unlock: Badges ≥ 7. Carry a warm dragon egg across the Cinderhorn to the far roost. Egg-hunters know the route. The egg must not get cold. Reward: Axew Lv 1; +4 pts.
- **Two Lucarios** (cameo, Garret; CAMEOS §3): after the Conclave, in the shafts below the Pit, a gruff stranger asks every pit-fighter about a missing girl named Eden. Fight: Hariyama 42 @Flame Orb, Scrafty 43 @Leftovers, Breloom 44 @Life Orb, Pangoro 44 @Assault Vest, Sirfetch'd 45 @Leek, Lucario 46 @Life Orb.

**Event Pokémon:**

- **Falinks Lv 38 (DEFIANT)**: boss battle, then it joins, the Iron Pit, Ironreach. Win six bouts, then beat the Brass Formation. *(designed, not implemented)*
- **Axew Lv 1**: egg, the far roost, the Cinderhorn. Keep the egg warm across the Cinderhorn. *(designed, not implemented)*

**Mega Stones and Z-crystals:**

_None placed for this chapter._

### Gym 8 — the Pit (Kaito Ren) *(design only)*

- **Puzzle (6/10, about 20 minutes): "every step you take, they take."** Sparring partners are pursuers: after each of your steps each steps one tile toward you (larger gap first).
    - *Sparring Floor (271), west half:* walk up the east side of the pillar until the partner commits east, then circle the pillar clockwise; it parks on the far side. Dash to the bell. *East half:* step over the rope at x17, draw Mae south to the rope, walk back east below it (she is stuck behind the line while Ren comes through the gap), lead Ren south-west and back over the rope at x26, and ring the bell.
    - *Rope Ring (272):* three partners round a central bell dais with two gaps.
    - *The Gauntlet (273):* push boulder (10,14) east four tiles onto P2, use boulder (20,14) to wall off the east partner's path, lure the west partner across the rope gap, then push boulder (5,6) along row 6 and up to P1. Budget: 30 pushes ("Discipline over rage").
- **Badge:** Badge 8. **TM31 Brick Break.** **Level cap after: 47.** **Field move:** Fly (HM02 from Odessa at the Conclave; 8 badges).
- **Mastery (optional):** the Marrowgate Door (275), a side door in 273.

# Act III — Fault Lines

*Design only (outline: `story/06_ACT_III.md`, with `14_WAR_AND_BLESSING.md`). The Mandate is realm-wide now: Directorate checkpoints at every border, and every Pokémon Center scanner greets your NULL reading with a polite "Fellowship Priority Guest" banner. Verdance's market terraces, Pokémon Center, Mart, Briar Hall and the Cathedral of the Evergreen (280–287, 295) are built; nothing else in the act is.*

## Chapter 10 — "The Seat That Blooms"

*The Root Road: the Tailings (692) outside Ironreach, the Rootdeep (680) and its freight-lift up to Lanternroot (690), Prism Falls (681), the Briarway (693) to Verdance (280–297, Elowen's royal seat) with Briar Keep, the Heartgarden (294), the Bride Grove (708) and the Royal Chase (682). Side: Grudgestone Quarry (684/685), Echo Coliseum (688). Branch maps by Standing: the Hollow Sanctuary (698) or the Meridian Black Site (699). Design only (town partly built). Gym 9 (J3).*

### Key events

- **Juno becomes Warden.** Rowan's sealed testament names her heir; in the Bride Grove the Meadow Plate accepts her.
- **The Loyal Three** (multi-bar boss) and the truth about the Ogre (⚑ `:ch10_ogre`; ☠ `GO_LOYAL`).

### Order of events

1. **The Root Road:** the Tailings, then the **Rootdeep** freight-lift that hauls Nadir's ore up to Elowen's downs (**Lanternroot**).
2. **Branch scene on the Lift Road:** *high Hollow Standing:* Wick's runner leads you to the **Hollow Sanctuary** in Grudgestone Quarry; Wick teaches the missing verse of the Hymn early and Thistle asks you to carry a letter to Rowan's jailers. *High Meridian Standing:* Calla invites you to the **Meridian Black Site**: **Project NULL**, a Type: Null in a cradle that reacts to you like the badge case; you may leave with it (S180). *Neither:* refugees climbing the Lift Road from Nadir.
3. **Prism Falls** (`:RAINBOW`) and **the Briarway** to Verdance.
4. **Verdance is drowning in flowers:** roses through the cobbles, pollen so thick the Pokémon Center hands out masks, and grey soil underneath where nothing rots. Three claims on the Meadow Plate: **Queen Maelis**'s Thornguard occupy the Heartgarden (S165); Meridian offers "temporary custody" (Prince Caedmon smiles beside the delegate); and **Rowan's testament**, opened by Valen, names **Juno**, with his Warden's ring sealed inside. "I didn't want this seat. I wanted *him* in it." **Tamsin** comes up from Briarwick to stand with her (the "Greenward"); if you kept Tamsin's secret in Ch3, Thistle's cell heckles her ("You *knew*").
5. **The Bride Tree:** Aunt Elin, Fixed in AF 288. With **Venam's Testimony** (Ch7 cameo) you can play it to Juno under the tree ("I could hear everything").
6. **Juno's Warden trial** in **the Bride Grove** (708, Bleed-adjacent): clear the way inside the Veil and guide Juno along the one safe path. **Ogerpon**, the "Gossamer Ogre", has guarded the tree since AF 288.
7. **Boss: the Loyal Three** (Okidogi, Munkidori, Fezandipiti), their collars glowing Sweetrot-pink. ⚑ `:ch10_ogre`: *stand with the Ogre* (`OGERPON_TRUSTED`: Ogerpon fights beside you, later joins Juno and appears at the Festival) / *stand with the Three* (☠ **`GO_LOYAL` "Loyal"**: they seize the Plate and poison the Bride Tree's roots) / *hesitate* (the Ogre fights alone, the fight is harder, and Ogerpon leaves distrustful). S127.
8. **Gym 9: J3**, Juno as Warden (S125). The **Flower Garden** grows during the fight with her confidence. Badge 9, **TM53 Energy Ball**.
9. **Juno's first act:** she refuses Meridian's Lattice and orders the Thornguard out in front of the Queen ("Little gardener. We'll see how long you bloom."). Under the Bride Tree she gives you the **Venusaurite** (*The Bride Tree's Heart*); Rowan's ring won't answer her yet.
10. **The Royal Chase** opens to the public (S126; a Safari-style reserve). In her private garden the Queen: "Every Sovereign since Maren has died tired... Ask yourself why the Accord needs a *new* champion so badly this year." Comedy scene: "The Royal We".
11. ⚑ **`:ch10_succession_stance`** (the press on the Heartgarden steps): should the Plates belong to *the Wardens/Accord*, *the kingdoms*, or *nobody* (the first "nobody", which the Return path checks).
12. **Cliffhanger:** Juno writes "Dear Uncle Rowan" and can't finish; the pages she throws away bloom where they land.

### Areas *(design only; Verdance partly built)*

| Map (ID) | Field | Built? | Wild Pokémon (from `pbs/encounters.txt`) |
|---|---|---|---|
| The Tailings (692) | Scrapyard (`:SCRAPYARD`) | no | _no wild table yet_ |
| The Rootdeep (680) | Cave (`:CAVE`) | no | Cave: Machoke 39–43, Gurdurr 39–43, Scraggy 39–43, Foongus 39–43, Parasect 39–43, Shiinotic 39–43, Golbat 39–43, Amoonguss 39–43, Breloom 39–43, Toxicroak 39–43, Liepard 39–43, Toedscruel 39–43, Bramblin 39–43, Drapion 40–43, Mabosstiff 39–43 |
| Lanternroot (690) | Cave (`:CAVE`) | no | _no wild table yet_ |
| Prism Falls (681) | Rainbow (`:RAINBOW`) | no | Grass: Swirlix 41–45, Spritzee 41–45, Clefairy 41–45, Jigglypuff 41–45, Impidimp 41–45, Altaria 41–45, Jumpluff 41–45, Milcery 41–45, Chimecho 41–45, Klefki 41–45, Girafarig 41–45, Sawsbuck 41–45, Ribombee 41–45, Togepi 41–45, Snorlax 42–45; Surf: Poliwhirl 41–45, Golduck 41–45, Floatzel 41–45, Azumarill 41–45, Masquerain 41–45; Old Rod: Magikarp 30–40, Goldeen 30–40; Good Rod: Goldeen 40–45, Poliwhirl 40–45, Seaking 40–45, Dratini 40–45 |
| The Briarway (693) | Fairy Tale (`:FAIRY_TALE`) | no | _no wild table yet_ |
| Verdance - Market Terraces (280) | Flower Garden (`:FLOWER_GARDEN`) | yes | _no wild table yet_ |
| The Heartgarden (294) | Flower Garden (`:FLOWER_GARDEN`) | no | _no wild table yet_ |
| The Royal Chase (682) | Meadow (`:MEADOW`) | no | Grass: Stantler 40–45, Skiddo 40–45, Galarian Farfetch'd 40–45, Lickitung 40–45, Sawsbuck 40–45, Exeggcute 40–45, Tangela 40–45, Audino 40–45, Lokix 40–45, Spidops 40–45, Dolliv 40–45, Bouffalant 40–45, Oinkologne 40–45, Farfetch'd 40–45, Heracross 40–45, Pinsir 40–45, Scyther 40–45, Chansey 40–45 |
| Grudgestone Quarry (684) | Cave (`:CAVE`) | no | Cave: Machoke 40–44, Gurdurr 40–44, Scraggy 40–44, Boldore 40–44, Graveler 40–44, Mienfoo 40–44, Pawniard 40–44, Pawmo 40–44, Croagunk 40–44, Glimmet 40–44, Hariyama 40–44, Stonjourner 41–44, Jangmo-o 40–44 |
| Grudgestone Quarry B1F (685) | Cave (`:CAVE`) | no | Cave: Pawniard 42–45, Machoke 42–45, Gurdurr 42–45, Graveler 42–45, Scrafty 42–45, Mienfoo 42–45, Toxicroak 42–45, Mabosstiff 42–45, Onix 42–45, Jangmo-o 42–45, Pupitar 42–45, Skuntank 42–45, Glimmora 42–45, Hakamo-o 42–45 |
| Echo Coliseum (688) | The Bleed (`:BLEED`) | no | Grass: Falinks 43–46, Hitmonlee 43–46, Hitmonchan 43–46, Hitmontop 43–46, Passimian 43–46, Medicham 43–46, Mienshao 45–46, Pangoro 43–46, Crabominable 43–46, Sawk 43–46, Throh 43–46, Grapploct 43–46, Annihilape 43–46, Lucario 43–46, Sirfetch'd 43–46 |
| The Bride Grove (708) | The Bleed (`:BLEED`) | no | Grass: Amoonguss 47–50, Shiinotic 47–50, Lurantis 47–50, Carnivine 47–50, Eldegoss 47–50, Ferrothorn 47–50, Cacturne 47–50, Trevenant 47–50, Gourgeist 47–50, Victreebel 47–50, Tsareena 47–50, Alolan Exeggutor 47–50, Dhelmise 47–50, Brambleghast 47–50, Sawsbuck 47–50 |
| Hollow Sanctuary (698) | Silkwood (`:SILKWOOD`) | no | _no wild table yet_ |
| Meridian Black Site (699) | Factory (`:FACTORY`) | no | _no wild table yet_ |

- **Built in Verdance:** Market Terraces (280), Pokémon Center (281), Mart (282), Briar Hall's Upper Court, Great Hall and Throne Room (285–287), the Cathedral of the Evergreen (295). The Heartgarden (294), the gym (290–293) and the Rootward (296) aren't built.
- **The Royal Chase** is a Safari-style reserve: no move battles, so no field applies (FIELD_DEFAULTS).

### Key battles

**Gym 9 — J3, Warden Juno Hale** (Grass, `:FLOWER_GARDEN`, cap 47; `LEADER_JUNO` uses the rival versions 30–32; GYM_PUZZLES calls it a double battle, Core's gym table sets no double rule)

| Pokémon | Lv | Item | Ability | Moves |
|---|---|---|---|---|
| Whimsicott | 45 | Telluric Seed | Prankster | Leech Seed, Growth, Energy Ball, Moonblast |
| Florges "Everbloom" | 45 | Sitrus Berry | Flower Veil | Moonblast, Petal Blizzard, Grassy Terrain, Wish |
| Lilligant | 46 | Miracle Seed | Own Tempo | Petal Dance, Giga Drain, Aromatherapy, Quiver Dance |
| **Starter**† | 46 | Sitrus Berry | (slot 0) | (regenerated for the swapped species) |
| Tsareena "Sweetpea" | 47 | Sitrus Berry | Queenly Majesty | Trop Kick, Play Rough, Acrobatics, U-turn |

*Bag: Hyper Potion, Hyper Potion; IV 24.*

- **Hard:** Whimsicott 46 @Telluric Seed, Florges 46 @Sitrus Berry, Roserade 46 @Miracle Seed, Lilligant 47 @Miracle Seed, Starter 47 @White Herb, Tsareena 47 @Life Orb
- **Casual:** Whimsicott 41 @Leftovers, Lilligant 42 @Miracle Seed, Starter 42 @Sitrus Berry, Tsareena 43 @Sitrus Berry

† The rival's starter is written as the Gen 1 line in PBS; Prismfall Core swaps it at battle start for the same-generation counterpart of your starter (same stage).

*Field note:* "a garden you grow during the fight." The garden starts at stage 1 + the overgrowth you left in the gym puzzle (up to 5); Grass goes ×1.1 → ×1.2 → ×1.3 → ×1.5 → ×2.0, Bug and Fire grow too. Growth, Leech Seed, Aromatherapy, Grassy Terrain and her Telluric Seed (Whimsicott) grow it. *Tip:* leave little overgrowth in the puzzle, cut the garden back with Fire (stages 1–4), blades, frost or acid (acid resets it to stage 1), and burn it down at stage 5 (Fire ×2 turns it into Wildfire). If you told her about the ledger in Ch7: "You knew before me. You *knew*."

**Boss — the Loyal Three** *(planned triple multi-bar sequence; not registered in Prismfall Bosses yet; Ogerpon is your partner if you stand with it).*

### Side quests

- **Gerald** (`EL_GERALD`, The Quiet Way; designed (not wired yet)). the Queen's Keeper of Small Creatures, the Royal Chase (682). Unlock: Badges ≥ 8 and S126 CH10_ROYAL_CHASE_OPEN. Queen Maelis's named Scatterbugs have escaped into the Royal Chase. Each one has a personality file. Gerald's is four pages long. Reward: Shiny Stone, Scatterbug "Gerald" Lv 40 (COMPOUNDEYES); +3 pts.
- **The Rootward Wake** (`EL_ROOTWARD_WAKE`, The Quiet Way; designed (not wired yet)). a Rootward laundress, the Rootward slums, Verdance (296). Unlock: Badges ≥ 8. In Verdance nothing rots, so nothing is ever properly buried. The Rootward wants one funeral done right. Reward: Cleanse Tag, TM20 Safeguard; +3 pts.
- **What the Bride Tree Hears** (`EL_EVER_BLOOM`, The Quiet Way; designed (not wired yet)). Juno, the Heartgarden, Verdance (294). Unlock: Badges ≥ 8 and S125 CH10_JUNO_WARDEN. Juno wants to know whether her Aunt Elin can still hear her. The Quiet Way says the Root carries voices. Juno says she'd like proof. Reward: Floette "Ever-Bloom" Lv 44 (FLOWERVEIL), JUNO+2; +4 pts.
- **What Are You For?** (cameo, Melia; CAMEOS §4): in the newly opened Royal Chase, after J3, a blonde girl with a Togekiss is looking for a friend who "fell through a sewer" (extra payoff if Venam's quest is done). Fight: Snorlax 47 @Leftovers, Lopunny 48 @Life Orb, Mimikyu 48 @Life Orb, Dudunsparce 49 @Leftovers, Zoroark 49 @Life Orb, Togekiss 50 @Leftovers.

**Event Pokémon:**

- **Comfey Lv 35 (TRIAGE)**: gift, Hall of the Listening Root, Verdance. Reach Heartwood in the Quiet Way.
- **Scatterbug "Gerald" Lv 40 (COMPOUNDEYES)**: gift, the Royal Chase. Find all six royal Scatterbugs; Gerald last. *(designed, not implemented)*
- **Floette "Ever-Bloom" Lv 44 (FLOWERVEIL)**: gift, the Heartgarden, Verdance. Carry Juno's message to the Bride Tree. *(designed, not implemented)*

**Mega Stones and Z-crystals:**

- **Sceptilite** (Mega Stone, from Badge 8): The Royal Chase, the old hunting lodge's mantel. item. *(planned: map not built)*
- **Blastoisinite** (Mega Stone, from Badge 8): Prism Falls, behind the falls (Surf). hidden item. *(planned: map not built)*
- **Rockium Z** (Z-crystal, from Badge 8): Grudgestone Quarry B1F, the gem seam. hidden; "rings and waits". *(planned: map not built)*
- **Grassium Z** (Z-crystal, from Badge 8): The Rootdeep, a root-wrapped ledge (Surf). hidden; "rings and waits". *(planned: map not built)*

### Gym 9 — the Heartgarden Gym (Juno Hale) *(design only)*

- **Puzzle (7/10, about 25 minutes): "water spreads."** Watering a plot grows it **and its neighbours** by one stage, mod 4: bare → sprouts → **vine bridge** (walkable over the canals) → **hedge** (impassable); watering a hedge collapses it to bare. The arena starts at Flower Garden stage **1 + the hedges you leave in 291 and 292** (max 5), and the gym guide tells you so.
    - **290 Gate:** water the one plot once; the decorative plot beside it grows too ("Gardens are gossips").
    - **291 Hedge Garden** (ring of six; the path needs P1, P3, P5 as bridges; start 0,0,1,2,1,2): *cheapest* 2 waterings (P2 once, P6 once) leaves one hedge (P6); *clean* 5 waterings (P4 once, P5 twice, P6 twice) leaves none.
    - **292 Glasshouse** (two rings of five sharing the junction J; the path needs J, A2, A3, B2, B3 as bridges): *fewest* 7 waterings (A1 ×2, A3, B1, B3, B4 ×2) leaves 2 hedges; *no hedges* 8 (J ×2, A1 ×2, A3, B3 ×2, B4).
    - **Hints:** apprentice Bram, Juno's cousin.
- **Badge:** Badge 9. **TM53 Energy Ball.** **Level cap after: 51.**
- **Mastery (optional):** the Bride Bower (297; five plots in a row, target bridge-hedge-bridge-hedge-bridge from 0,2,1,3,1): P2 ×2, P3 ×3, P5 ×1. Reward: Telluric Seed ×2, Miracle Seed and a pressed Bride Tree petal.
- **Gym trainers:** 5 (Aroma Lady ×2, Pokémon Breeder, Picnicker, Gardener), Lv 43–46. *(Team data not in PBS yet.)*

---

## Chapter 11 — "The Thaw"

*The Hart Road: the Hart's Run (700), the Hoarwood (701) with Snowbriar (710), the Gossamer Heartwood (703, a Silkwood revisit), Frostfang Pass (704/705), the Whalebone Road (712) to Rimeholt (300–315, Isenmar) on Lake Rime, with Whalebone Keep and its Ice Vault (305–308) and the Sinking Quarter (309). After the Thaw: a detour to Ebbmouth, the Ebbmouth Sea Grotto (723), then the Mast Road out: the Thane's Sled-Road (720), the Mast Glacier (721), Anchorhold (730); optional Stillwater (728). Design only. Gym 10.*

### Key events

- **The Thaw.** Rimeholt's heat-towers overdraw, the lake ice breaks, a quarter of the lower town sinks, and **Kyogre** wakes under the ice (boss).
- **War is declared.** Kyogre's Primal rain rolls east for three days and floods the Dominar's forward camps on Ossaria's dunes; on the third day Isenmar and Ashkaar go to war on every screen. ⚑ `:ch11_anja`, ⚑ `:ch11_strike`.

### Order of events

1. **Juno travels with you,** lobbying the northern Wardens for the Greenward (she practises speeches on your Pokémon).
2. The **Hart's Run**, the **Hoarwood** (`:SNOWY_MOUNTAIN`) and **Snowbriar**; the **Gossamer Heartwood** revisit (DUNGEON_PUZZLES "the forest is a loom", 7/10).
3. **Frostfang Pass:** from the top on a clear morning you can see north-east across the Mast Glacier to the bone sands: cookfire smoke and a dragon-column. The Dominar's legions are already camped on Ossaria's western dunes, on sand Kassan has leased them. ⚑ **`:war_warning`**: warn Isenmar / warn Ashkaar they've been seen / warn both through Valen / stay silent. Juno: "Those aren't caravans, are they."
4. **Rimeholt:** timber and whalebone on the ice of Lake Rime, kept alive by **Meridian heat-towers**; the ice under them is grey and thin. Warden **Anja Sorrel** to Juno: "You want me to choose between my principles and my grandchildren's toes? Easy choice. Toes." (comedy scene "Toes").
5. **Gym 10, the Lake Hall:** Anja. Badge 10, **TM13 Ice Beam**; the ice-climbers give **Rock Climb** (TM100) and the ice-fisher the **Super Rod**.
6. **The Thaw** at night: the towers' readings red and climbing; the ice breaks; the field goes Frozen Lake → Water Surface mid-battle. **Partner battle: you + Juno vs Directorate officers** "securing the Lattice" while people drown. ☠ **`GO_THIN_ICE` "Thin Ice"**: go back for the Lattice's data core when the technician begs.
7. **The lake breathes.** Prompt: *Fight it now* (☠ **`GO_WEATHER` "Weather"**: an unwinnable Lv 80 Kyogre; Anja has told you all chapter "When the lake breathes, you run") / *Get to the towers*: a sprint across breaking ice to the heat-tower platform.
8. **Boss: Kyogre** on breaking ice, in Primal rain. Mid-fight the shard resonates; on a Harmony lean its last bar *calms* instead of fainting. It sinks back to sleep, but the sea is no longer fully frozen. S129.
9. Anja on a fishing hut's roof in the rain: "I read the numbers. I *read* them. And I signed anyway." ⚑ **`:ch11_anja`**: *expose her* to the Thane's court (`ANJA_EXPOSED`: Accord up; she won't release the Icicle Plate in Act V) / *let her confess* (a key Act V swing vote; she lets go at the end). Either way she breaks with Meridian publicly.
10. **Martial law:** Thane Eirik evacuates the lower town south into Elowen (a border crisis with the Thornguard). Kyogre's rain floods the Dominar's camps; on the third day **war is declared** (S128), and the Thane's host goes east along the Sled-Road to Skaldfast.
11. **Detour: Ebbmouth** (Isenmar, second visit), with the evacuation column. **The Ebbmouth Strike:** Marisol's Guild cuts Meridian's tidal Lattice with dockworkers' saws and refuses the Thane's war levy; the Ebb runs both ways again (S130). Teo is organising if he lived; otherwise his photograph is nailed to the banner pole and Marisol says "He was nineteen" here. ⚑ **`:ch11_strike`** when the strikebreakers come: *stand* (a tag battle with Marisol; her Bond up a lot, the only Act III way back to her after Teo's death) / *mediate* (peaceful; she notes you didn't pick a side). The **Ebbmouth Sea Grotto** (723) opens with Surf.
12. **The Mast Road:** back through Rimeholt and east along **the Thane's Sled-Road** past war-sleds, up **the Mast Glacier** to **Anchorhold**, where Skyreach's airships are anchored in the ice.
13. **Cliffhanger:** a Gale Post mail-ship loading in a hurry under a banner, **"LARCH SPEAKS TONIGHT."** You go aboard; below, Isenmar's host is strung east across the sands toward Skaldfast, and then the Crownwall passes under the keel.

### Areas *(design only; maps not built)*

| Map (ID) | Field | Built? | Wild Pokémon (from `pbs/encounters.txt`) |
|---|---|---|---|
| The Hart's Run (700) | Meadow (`:MEADOW`) | no | Grass: Kricketune 43–47, Pumpkaboo 43–47, Bramblin 43–47, Ariados 43–47, Leavanny 43–47, Lurantis 43–47, Breloom 43–47, Applin 43–47, Combee 43–47, Toedscool 43–47, Capsakid 43–47, Dolliv 43–47, Spidops 43–47, Lokix 43–47, Tsareena 43–47, Vespiquen 43–47 |
| The Hoarwood (701) | Snowy Mountain (`:SNOWY_MOUNTAIN`) | no | Grass: Snover 45–49, Swinub 45–49, Snorunt 45–49, Cubchoo 45–49, Vanillite 45–49, Bergmite 45–49, Sneasel 45–49, Alolan Sandshrew 45–49, Alolan Vulpix 45–49, Ursaring 45–49, Stantler 45–49, Sawsbuck 45–49 |
| Snowbriar (710) | Snowy Mountain (`:SNOWY_MOUNTAIN`) | no | _no wild table yet_ |
| Gossamer Heartwood (703) | Silkwood (`:SILKWOOD`) | no | Grass: Butterfree 44–49, Beedrill 44–49, Vivillon 44–49, Charjabug 44–49, Leavanny 44–49, Scolipede 44–49, Ribombee 44–49, Shiinotic 44–49, Amoonguss 44–49, Forretress 44–49, Galvantula 44–49, Ninjask 44–49, Parasect 44–49, Beautifly 44–49, Dustox 44–49, Orbeetle 44–49, Centiskorch 44–49, Masquerain 44–49 |
| Frostfang Pass (704) | Snowy Mountain (`:SNOWY_MOUNTAIN`) | no | Cave: Snorunt 45–49, Piloswine 45–49, Bergmite 45–49, Sneasel 45–49, Cryogonal 45–49, Sealeo 45–49, Vanillish 45–49, Golbat 45–49, Jynx 45–49, Galarian Darumaka 45–49, Abomasnow 45–49, Eiscue 45–49, Frigibax 45–49, Beldum 45–49 |
| Frostfang Pass 2F (705) | Snowy Mountain (`:SNOWY_MOUNTAIN`) | no | Cave: Piloswine 47–50, Sealeo 47–50, Vanillish 47–50, Cryogonal 47–50, Sneasel 47–50, Jynx 47–50, Beartic 47–50, Avalugg 47–50, Glalie 47–50, Frosmoth 47–50, Delibird 47–50, Galarian Mr. Mime 47–50, Bagon 47–50, Arctibax 47–50 |
| The Whalebone Road (712) | Snowy Mountain (`:SNOWY_MOUNTAIN`) | no | _no wild table yet_ |
| Rimeholt - Thane's Harbour (300) | Frozen Lake (`:FROZEN_LAKE`) | no | Surf: Seel 45–50, Spheal 45–50, Sealeo 45–50, Dewgong 45–50, Eiscue 45–50, Lapras 45–50; Old Rod: Goldeen 25–30, Magikarp 25–30; Good Rod: Goldeen 40–46, Seel 40–46, Spheal 40–46, Shellder 40–46 |
| Whalebone Keep - Ice Vault (308) | Frozen Lake (`:FROZEN_LAKE`) | no | _no wild table yet_ |
| Rimeholt - Sinking Quarter (309) | Frozen Lake (`:FROZEN_LAKE`) | no | _no wild table yet_ |
| Stillwater (728) | The Bleed (`:BLEED`) | no | Grass: Froslass 51–54, Cryogonal 51–54, Sneasel 51–54, Galarian Darumaka 51–54, Vanilluxe 51–54, Avalugg 51–54, Eiscue 51–54, Beartic 51–54, Glalie 51–54, Galarian Mr. Mime 51–54, Absol 51–54, Banette 51–54, Arctozolt 51–54, Arctovish 51–54 |
| Ebbmouth Sea Grotto (723) | Cave (`:CAVE`) | no | Cave: Sealeo 47–53, Dewgong 47–53, Clawitzer 47–53, Barbaracle 47–53, Quagsire 47–53, Wugtrio 47–53, Cetoddle 47–53, Golbat 47–53, Golisopod 47–53, Araquanid 47–53, Slowbro 47–53, Finizen 47–53, Cryogonal 47–53, Lapras 47–53; Surf: Tentacruel 47–53, Dewgong 47–53, Finizen 47–53, Lapras 47–53, Veluza 47–53, Tatsugiri 47–53 |
| The Thane's Sled-Road (720) | Snowy Mountain (`:SNOWY_MOUNTAIN`) | no | Grass: Abomasnow 47–51, Piloswine 47–51, Beartic 47–51, Snorunt 47–51, Delibird 47–51, Sneasel 47–51, Cetoddle 47–51, Absol 47–51, Alolan Sandslash 47–51, Noctowl 47–51, Frosmoth 47–51, Honchkrow 47–51, Arctibax 47–51, Frigibax 47–51, Eiscue 47–51; Surf: Seel 47–51, Spheal 47–51, Dewgong 47–51, Sealeo 47–51, Lapras 47–51 |
| The Mast Glacier (721) | Snowy Mountain (`:SNOWY_MOUNTAIN`) | no | Grass: Cryogonal 49–53, Avalugg 49–53, Beartic 49–53, Piloswine 49–53, Glalie 49–53, Skarmory 49–53, Kilowattrel 49–53, Corvisquire 49–53, Magneton 49–53, Delibird 49–53, Frosmoth 49–53, Staravia 49–53, Braviary 54 |
| Anchorhold (730) | Snowy Mountain (`:SNOWY_MOUNTAIN`) | no | _no wild table yet_ |

### Key battles

**Gym 10 — Warden Anja Sorrel** (Ice, `:FROZEN_LAKE`, single battle, cap 51)

| Pokémon | Lv | Item | Ability | Moves |
|---|---|---|---|---|
| Ninetales | 49 | Sitrus Berry | Snow Warning | Aurora Veil, Ice Beam, Moonblast, Freeze-Dry |
| Cloyster | 49 | White Herb | Skill Link | Shell Smash, Icicle Spear, Razor Shell, Ice Shard |
| Glalie | 50 | Glalitite | Inner Focus | Double-Edge, Ice Shard, Crunch, Taunt |
| Walrein | 50 | Sitrus Berry | Thick Fat | Ice Beam, Surf, Encore, Protect |
| Avalugg | 50 | Rocky Helmet | Sturdy | Avalanche, Body Press, Rapid Spin, Recover |
| Mamoswine "Matriarch" | 51 | Elemental Seed | Thick Fat | High Horsepower, Icicle Crash, Ice Shard, Knock Off |

*Bag: Mega Ring, Full Restore, Full Restore; IV 24.*

- **Hard:** Ninetales 50 @Light Clay, Cloyster 50 @White Herb, Glalie 51 @Glalitite, Walrein 51 @Leftovers, Avalugg 51 @Rocky Helmet, Mamoswine 51 @Life Orb
- **Casual:** Ninetales 45 @Sitrus Berry, Glalie 46 @Glalitite, Walrein 46 @Sitrus Berry, Avalugg 46 @Rocky Helmet, Mamoswine 47 @Never-Melt Ice

*Field note:* "ice that remembers every weight." Ice ×1.5; Rock moves freeze into ice boulders (also Ice); skaters build speed; Fire or quake hits ×3 crack the lake into Water Surface, and Ice moves refreeze it. **Mega Glalie** (every mode; Refrigerate Double-Edge) seals the lake's cracks once when it Mega Evolves (the crack meter resets). *Tip:* the crack is your plan (Body Press and High Horsepower count, and the sun melts the lake at once), so save the third crack until after Glalie has Mega Evolved; Mamoswine "Matriarch" holds an Elemental Seed (+2 Speed). MEGA_EVOLUTION says Walrein, not Glalie, is the lever if the fight needs easing.

**Boss — Kyogre** (`KYOGRE_ISENMAR`, Prismfall Bosses, on `:FROZEN_LAKE`)

- Lv 55; bars Casual 2 / Standard 3 / Hard 3.
- **Break 1:** the lake cracks to Water Surface; it learns Water Spout; Sp. Atk +1. **Break 2:** Primal Reversion, Origin Pulse, and the shard hums.
- **Last bar:** on a Harmony lean (Resonance band) it is *calmed* (no faint, result `:calmed`); otherwise it faints.
- *Tip:* Electric and Grass; Primal Kyogre's Primordial Sea means Fire does nothing at all.

**The Thaw — you + Juno vs Directorate officers** and **the Strike — you + Marisol vs strikebreakers** *(partner and officer teams aren't in PBS yet).*

### Side quests

- **The Bride Tree's Heart** (`EL_BRIDE_TREE_HEART`, The Quiet Way; wired (playable)). Juno Hale, the Heartgarden, Verdance, under the Bride Tree (after J3) (294). Unlock: Badges ≥ 9. Juno is waiting under the Bride Tree. Reward: Venusaurite; +0 pts.
- **The White Stag** (`IS_WHITE_STAG`, The Tally; designed (not wired yet)). the lodge-keeper, Snowbriar (710). Unlock: Badges ≥ 9. A white stag has been seen in the royal hunting woods. Elowen law says it's the Crown's. The trappers say it's nobody's. Reward: $4000; +3 pts.
- **The Harpoon Rite** (`IS_HARPOON_RITE`, The Tally; designed (not wired yet)). Old Halla Brinesdottir, the Great Tally, Rimeholt (306). Unlock: Badges ≥ 9. Every Harpooner earns the rank by facing the Old Bull on the ice. The Old Bull is a Cetitan. It has never once been harpooned. Reward: Never-Melt Ice; +4 pts.
- **Eleven Years at One Hole** (`IS_ELEVEN_YEARS`, The Tally; designed (not wired yet)). Old Torstein, the ice-fishing flats, Rimeholt (300). Unlock: Badges ≥ 9. Old Torstein has fished one ice-hole for eleven years waiting for a single bite. He has not noticed he is sitting on an Avalugg. Reward: Tatsugiri Lv 48 (COMMANDER); +2 pts.
- **The Sinking Quarter** (`IS_SINKING_QUARTER`, The Tally; designed (not wired yet)). a net-mender of Net Row, the Sinking Quarter, Rimeholt (309). Unlock: S128 CH11_THAW. After the Thaw, the lower town is going under. Three families won't leave without their boat, their grandmother and their Lapras, in that order. Reward: Exp. Candy L x2; +4 pts.
- **Crystal Sleep** (`IS_ALEXANDRA`, The Tally; designed (not wired yet)). Old Halla Brinesdottir, the sunken lower town, Rimeholt (309). Unlock: Badges ≥ 10 and S128 CH11_THAW. Something sleeps in a block of ice in the sunken quarter: a woman, very much alive, very annoyed about it. Reward: Icy Rock; +3 pts.
- **Crystal Sleep, the cameo fight** (Alexandra; CAMEOS §5). Act III and CAMEOS stage it as a tall woman with a Latias sitting among Rimeholt's half-Fixed fishers after the Thaw, asking whether they can hear her; the Trials entry above has her asleep in a block of ice instead (the docs disagree; the fight is the same). Fight: Sigilyph 52 @Life Orb, Starmie 53 @Life Orb, Altaria 54 @Leftovers, Garchomp 54 @Rocky Helmet, Dragonite 55 @Lum Berry, Latias 56 @Soul Dew.
- **The Doctor's Cell** (Act III, Ch11–13, S174): Corvin was arrested under the Mandate for treating Hollow wounded; free him from a Directorate holding barge on Lake Sallow (`CORVIN_FREED`, which decides who runs the Cragholm field hospital in Ch14 and one Festival seat).

**Event Pokémon:**

- **Lapras "Saga" Lv 45 (WATERABSORB)**: gift, Mead Hall of Rimeholt. Reach Sagaborn in the Tally.
- **Sawsbuck Lv 48 (SAPSIPPER)**: wild battle, catch it, the Northern Rimewood. Corner the white stag at dawn. *(designed, not implemented)*
- **Cetoddle Lv 46 (THICKFAT)**: gift, Lake Rime. Stand your ground against the Old Bull. *(designed, not implemented)*
- **Tatsugiri Lv 48 (COMMANDER)**: gift, the ice-fishing flats, Rimeholt. Land the bite Torstein waited eleven years for. *(designed, not implemented)*

**Mega Stones and Z-crystals:**

- **Glalitite** (Mega Stone, from Badge 2): The Tally, rank 3 (Harpooner). Trial rank reward ISENMAR. *(planned: map not built)*
- **Venusaurite** (Mega Stone, from Badge 9): The Heartgarden, Verdance: Juno, after J3. story gift EL_BRIDE_TREE_HEART. *(planned: map not built)*
- **Beedrillite** (Mega Stone, from Badge 9): Gossamer Heartwood, inside the old hive. hidden item. *(planned: map not built)*

### Gym 10 — the Lake Hall (Anja Sorrel) *(design only)*

- **Puzzle (7/10, about 25 minutes): "ice remembers weight."** Native ice sliding; a **cracked** tile cracks the first time you slide over it and gives way the second, dropping you to the under-ice grotto (316) and back to the room's start. The cracks are kept, so ask the apprentice (Liv, Anja's granddaughter) to reset.
    - **310 Boathouse:** slide across; the crack sits on an optional line to a Pearl.
    - **311 Ice Hall** ("every crack once"): 17 slides, `U R U L U L D L D R U L D R U R U` (13 if cracks didn't matter).
    - **312 Crackwalk:** unsolvable without pushing the two ice blocks; 16 actions, `U L U R D [push R] L D R U [push U] U L U R U`. A block pushed into a broken crack plugs it with rough ice, a new place to stop.
- **Badge:** Badge 10. **TM13 Ice Beam.** **Level cap after: 55.** **Field move:** Rock Climb (TM100, the ice-climbers; 10 badges). **Super Rod** from the ice-fisher.
- **Mastery (optional):** the Sounding (315): 33 actions with 7 pushes, `U R U R D L [L] D L [L] L U [U] L D R U [U] [L] U L D R U R [R] D R D R U L U`. Reward: Elemental Seed ×2 and Never-Melt Ice, and your name on Anja's family sounding-line.
- **Gym trainers:** 5 (Cool Trainer ♀ ×2, Hiker, Swimmer, Boarder), Lv 47–50. *(Not in PBS yet.)*

---

## Chapter 12 — "Dead Letters"

*The Mast Road's air leg: the Tetherline (732) under Skyreach's mooring cables, the Cloudstair (724–726, Rock Climb), Skyreach (320–334, Zenith's airship spire) with the Gale Post Hall (325), the dead-letter archive and Stormwatch Spire (744–746). Design only. Gym 11.*

### Key events

- **The Larch Papers.** At midnight Larch broadcasts her AF 292 report from Stormwatch Spire to every screen in Velmora: Lattice extraction is accelerating the Bleed. "I designed the Lattice. I was wrong." Within the hour a bomb kills the broadcast, and by dawn she is "Hollow sympathiser Larch" (S131, S132).
- **K5 and the dead letters.** Kestrel, now in Meridian's sponsor jacket with a Resonance Gauntlet, steals a bundle of Morwen's letters from the dead-letter archive (⚑ `:ch12_letter`).

### Order of events

1. The mail-ship moors low on **the Tetherline** (the Directorate searches the upper docks), and you climb **the Cloudstair** the back way in (Rock Climb).
2. **Skyreach:** docking masts and skybridges climbing into **the Stormfront**, the Sky Plate's permanent storm wall, under a Mandate curfew (searchlights from 9 p.m.). Larch hides in the **Gale Post** sorting halls as Warden **Odessa Gale**'s guest. Larch explains Meridian's keystones (steel Lattice-glass bands that "pry a heartstone open"). Airship crews whisper about a black dragon in the lightning, "the Stormfront Wyrm" (a Zekrom seed).
3. Comedy scene: "Flight Safety" (Odessa's skiff, before the raid).
4. **Gym 11, the Gale Post:** Odessa, a double battle. Badge 11, **TM51 Roost**; the sky-river guides give **Waterfall**.
5. **The Larch Papers** broadcast (the two heat contracts are side by side in it; nobody reads that page).
6. **The raid:** Director **Marchetti**'s Directorate storms the Gale Post; a bomb tears through Stormwatch's relay mast. In the wreckage, a **Splitter Casing** identical to Lumen's (key item; useful in Ch13 and Ch14). **Admin battle: Marchetti** on the sorting-hall catwalks (`:STORMFRONT`): her **Mega Manectric** is the first Meridian Mega. "You're not under arrest. You're under *protection*." Odessa gets Larch out on a skiff through the Stormfront, to Cragholm. A Mart terminal pings: *"Fellowship status: SUSPENDED."*
7. **K5** in the dead-letter archive (`:STORMFRONT`): the Gauntlet makes the field surge whenever his Pokémon attack. He flees with the bundle; one letter falls: *"I. — You must not let the child come back... If Valen learns what lodged in that little chest, he will put a crown on it... I'll carry the name. — M."* ⚑ **`:ch12_letter`**: *keep it* (leverage or a gift in Ch15) / *send it to Kestrel* by Gale Post (Bond up; K6 opens "You sent me a *letter*. Hers.") / *burn it* (Resonance −2 toward Ruin; Odessa won't release the Sky Plate in Act V). S133.
8. **Interlude III, "Dead Letters"** (play as **Kestrel**): Voss's office at night; tea in a chipped mug; the AF 290 folder (real, mostly: it proves Valen scapegoated Morwen and leaves out Meridian's array); a model of the new Prism Arena; Kestrel signs the **Festival sponsorship contract**. ☠ **`GO_FINE_PRINT` "Read the Fine Print"**: open Voss's private drawer when he steps out (a file titled *UNIMPRINTED-01: KEYSTONE*).
9. **Cliffhanger:** on Conductors' Causeway, your reflection in a puddle moves half a second late.

### Areas *(design only; maps not built)*

| Map (ID) | Field | Built? | Wild Pokémon (from `pbs/encounters.txt`) |
|---|---|---|---|
| The Tetherline (732) | Stormfront (`:STORMFRONT`) | no | _no wild table yet_ |
| Cloudstair - Lower (724) | Mountain (`:MOUNTAIN`) | no | Grass: Staravia 49–53, Kilowattrel 49–53, Corvisquire 49–53, Skarmory 49–53, Noibat 49–53, Gligar 49–53, Murkrow 49–53, Braviary 54, Mandibuzz 54, Hawlucha 49–53, Lycanroc 49–53, Bombirdier 49–53, Bagon 49–53, Flamigo 49–53, Aerodactyl 50–53 |
| Cloudstair - Inner (725) | Mountain (`:MOUNTAIN`) | no | Cave: Noibat 51–54, Swoobat 51–54, Lairon 51–54, Boldore 51–54, Skarmory 51–54, Minior 51–54, Klang 51–54, Magneton 51–54, Orthworm 51–54, Bagon 51–54, Bronzong 51–54, Carbink 51–54, Shelgon 51–54 |
| Cloudstair - Summit (726) | Mountain (`:MOUNTAIN`) | no | Grass: Altaria 52–54, Staraptor 52–54, Swellow 52–54, Braviary 54, Mandibuzz 54, Sigilyph 52–54, Xatu 52–54, Dodrio 52–54, Corvisquire 52–54, Honchkrow 52–54, Noivern 52–54, Aerodactyl 52–54, Shelgon 52–54, Talonflame 52–54 |
| Skyreach - Mast Ward (320) | Stormfront (`:STORMFRONT`) | no | _no wild table yet_ |
| Gale Post Hall (325) | none | no | _no wild table yet_ |
| Stormwatch Spire 1F (744) | Stormfront (`:STORMFRONT`) | no | Cave: Magneton 52–56, Electrode 52–56, Eelektrik 52–56, Galvantula 52–56, Drifblim 52–56, Klang 52–56, Vikavolt 52–56, Honchkrow 52–56, Bronzong 52–56, Luxray 52–56, Manectric 52–56, Boltund 52–56, Bellibolt 52–56, Porygon2 52–56, Heliolisk 52–56 |
| Stormwatch Spire 2F (745) | Stormfront (`:STORMFRONT`) | no | Cave: Magneton 54–57, Kilowattrel 54–57, Varoom 54–57, Electrode 54–57, Eelektrik 54–57, Skarmory 54–57, Corvisquire 54–57, Bronzong 54–57, Galvantula 54–57, Zebstrika 54–57, Klinklang 54–57, Pawmot 54–57, Magnezone 54–57 |
| Stormwatch Spire Roof (746) | Stormfront (`:STORMFRONT`) | no | Grass: Kilowattrel 55–58, Skarmory 55–58, Staraptor 55–58, Braviary 55–58, Emolga 55–58, Oricorio (Pom-Pom Style) 55–58, Drifblim 55–58, Altaria 55–58, Corviknight 55–58, Noivern 55–58, Talonflame 55–58, Pelipper 55–58, Archen 55–58 |

### Key battles

**Gym 11 — Warden Odessa Gale** (Flying, `:STORMFRONT`, **double battle**, cap 55)

| Pokémon | Lv | Item | Ability | Moves |
|---|---|---|---|---|
| Pelipper | 53 | Sitrus Berry | Keen Eye | Tailwind, Wide Guard, Air Slash, Scald |
| Noivern | 54 | Life Orb | Infiltrator | Hurricane, Hyper Voice, Air Slash, Sunny Day |
| Pidgeot "Post" | 53 | Pidgeotite | Big Pecks | Hurricane, Heat Wave, Roost, Protect |
| Oricorio | 54 | Elemental Seed | Dancer | Revelation Dance, Air Slash, Helping Hand, Roost |
| Kilowattrel | 54 | Sharp Beak | Wind Power | Thunderbolt, Air Slash, Volt Switch, Protect |
| Corviknight "Taxi" | 55 | Leftovers | Mirror Armor | Brave Bird, Iron Head, Bulk Up, Roost |

*Bag: Mega Ring, Full Restore, Full Restore; IV 28.*

- **Hard:** Pelipper 54 @Sitrus Berry, Noivern 55 @Life Orb, Pidgeot 54 @Pidgeotite, Oricorio 55 @Elemental Seed, Kilowattrel 55 @Magnet, Corviknight 55 @Leftovers
- **Casual:** Pelipper 49 @Sitrus Berry, Noivern 50 @Sitrus Berry, Pidgeot 49 @Pidgeotite, Kilowattrel 50 @Sharp Beak, Corviknight 51 @Leftovers

*Field note:* "wind lanes that redirect moves and Pokémon." Electric ×1.3, Flying ×1.2, wind moves ×1.2 (so Hurricane is ×1.44 and never misses; the field owner has a proposal to stop that stacking); Tailwind lasts two turns longer; hazards blow off the deck. **Mega Pidgeot "Post"** (No Guard Hurricane). *Tip:* Electric and Rock; Smack Down is ×2 here. Two Sunny Days turn the Stormfront into a Rainbow (Noivern does it for her).

**Director Helene Marchetti** (`MERIDIAN_MARCHETTI` v0, Skyreach catwalks, `:STORMFRONT`)

| Pokémon | Lv | Item | Ability | Moves |
|---|---|---|---|---|
| Mabosstiff | 53 | Sitrus Berry | Intimidate | Crunch, Wild Charge, Play Rough, Roar |
| Manectric | 54 | Manectite | Lightning Rod | Thunderbolt, Flamethrower, Snarl, Volt Switch |
| Arcanine | 54 | Sitrus Berry | Intimidate | Flare Blitz, Wild Charge, Extreme Speed, Crunch |
| Corviknight | 55 | Leftovers | Mirror Armor | Brave Bird, Iron Head, Tailwind, Roost |

*Bag: Mega Ring, Full Restore, Full Restore; IV 28.*

- **Hard:** Mabosstiff 54 @Sitrus Berry, Manectric 55 @Manectite, Arcanine 55 @Sitrus Berry, Magnezone 54 @Air Balloon, Corviknight 55 @Leftovers
- **Casual:** Manectric 50 @Manectite, Arcanine 50 @Sitrus Berry, Corviknight 51 @Leftovers

**K5 — Kestrel, the dead-letter archive** (`:STORMFRONT`)

| Pokémon | Lv | Item | Ability | Moves |
|---|---|---|---|---|
| Staraptor | 52 | Sharp Beak | Intimidate | Brave Bird, Close Combat, Double-Edge, U-turn |
| Krookodile | 52 | Life Orb | Moxie | Knock Off, Earthquake, Smack Down, Close Combat |
| Scizor | 53 | Life Orb | Technician | Bullet Punch, U-turn, Dual Wingbeat, Swords Dance |
| Zweilous | 52 | Eviolite | Hustle | Dragon Rush, Crunch, Body Slam, Work Up |
| **Starter**† | 54 | Sitrus Berry | (slot 0) | (regenerated for the swapped species) |
| Aegislash "Morwen" | 54 | Leftovers | Stance Change | King's Shield, Shadow Ball, Sacred Sword, Shadow Sneak |

*Bag: Full Restore, Full Restore; IV 28.*

- **Hard:** Staraptor 53 @Choice Band, Krookodile 53 @Life Orb, Scizor 54 @Life Orb, Zweilous 53 @Eviolite, Starter 55 @Life Orb, Aegislash 55 @Weakness Policy
- **Casual:** Staraptor 48 @Sitrus Berry, Scizor 49 @Metal Coat, Zweilous 48 @Eviolite, Starter 50 @Sitrus Berry, Aegislash 50 @Leftovers

† The rival's starter is written as the Gen 1 line in PBS; Prismfall Core swaps it at battle start for the same-generation counterpart of your starter (same stage).

*Tip:* no Mega yet (he has no ring of his own); the Gauntlet's field surges are a visual tell only. Aegislash "Morwen" (his Ch4 Honedge, fully evolved now; Stance Change) is the ace: hit it with status, or hard when it's in Blade Forme.

### Side quests

- **Cut Loose** (`ZE_COURIER`, The Prize Exchange; designed (not wired yet)). a pilot at the anchor-smithy, Anchorhold (730). Unlock: Badges ≥ 10. Deliver a sealed key-ring to an airship before the embargo inspectors board. The key-ring jingles by itself. Reward: Klefki Lv 50 (PRANKSTER); +4 pts.

**Event Pokémon:**

- **Klefki Lv 50 (PRANKSTER)**: gift, Anchorhold. Hide the key-ring from the embargo inspectors. *(designed, not implemented)*

**Mega Stones and Z-crystals:**

- **Altarianite** (Mega Stone, from Badge 10): The Tetherline, a cloud-nest on a tether pylon. item. *(planned: map not built)*
- **Slowbronite** (Mega Stone, from Badge 10): Ebbmouth Sea Grotto, the tide-pool shelf. hidden item. *(planned: map not built)*
- **Flyinium Z** (Z-crystal, from Badge 10): Cloudstair Summit, the wind-scoured ledge. hidden; "rings and waits". *(planned: map not built)*

### Gym 11 — the Gale Post (Odessa Gale) *(design only)*

- **Puzzle (8/10, about 30 minutes): "the wind doesn't care."** Gust lanes carry you end to end, only *with* the wind; weather vanes flip lanes, and every vane is rigged to **two** lanes (the rods show which).
    - **330 Hangar:** ride the lane, flip the vane, ride back.
    - **331 Gust Deck** (14 actions; V1 is on P0, V2 on P3, V3 on P2): V1, L5, V3, L5, L1, L6, V2, L6, L2, L5, V1, L1, L6, L4. The P1–P3 lane (L6) is on two vanes: fix it last.
    - **332 Mail Chute:** sacks ride the lanes and stack, and a sack in a lane stops you one tile short. Sack 1 down the east lane into pigeonhole A; turn the north vane south and push sack 2 so it stacks short of the north wall; ride the north lane to the ledge beside C; push sack 3 into C; re-aim and deliver sack 2 to B. *(Design says the builder still has to verify this room.)*
- **Badge:** Badge 11. **TM51 Roost.** **Level cap after: 59.** **Field move:** Waterfall (HM05, the sky-river guides; 11 badges).
- **Mastery (optional):** the Dead-Letter Archive (334): route five dead letters to their kingdoms by the vanes (addresses are Gale Post riddles; a sign has the glossary). Morwen's letter to "I." can't be delivered: leave it in the carousel. Reward: Elemental Seed ×2, Sharp Beak and the undelivered letter (key item, for K6/Ysolde).
- **Gym trainers:** 6 (Bird Keeper ×2, Pilot ×2, Sky Courier, Gambler), Lv 51–54. *(Not in PBS yet.)*

---

## Chapter 13 — "Behind the Glass"

*The Glass Road: Conductors' Causeway (740), the Wired Wood (741) with Verdigris (750), the Crown Road (Candle Down 602, the Highwold 603, Kingsmead 756), the Looking-Glass Wood (752) with Glassmere (753), the Mirror Mere (742), the Antumbra Threshold (743, `:INVERSE`), Widdershins Walk (755), Lucent (340–356, Antumbra) and the Athenaeum. Optional: Stormwatch Spire revisit, the Shattered Sky (748). Design only. Gym 12. The densest chapter: keep the gym short.*

### Key events

- **The Mindscape memory.** Ilsa opens a memory sealed in you: Lower Crownhaven at the AF 290 Festival, your mother singing in the Choir, the Crown blazing on Valen, brass machines with sunburst plates behind the loft, a crack, light, pain in your five-year-old chest, and Morwen Vane throwing herself over you (⚑ `:ch13_remember`; the first authored PC dialogue).
- **The tribunal and the Fault.** At Rowan's tribunal Sable may be exposed as **Sabine Kroll**, Meridian Special Accounts; that night Meridian test-fires the Arbiter Engine's first core, the ground moves across the realm, the sea pulls back from the south coast, and the Glass Court floods (⚑ `:ch13_rowan_testimony`, ⚑ `:ch13_fault`).

### Order of events

1. North off the plateau: **Conductors' Causeway**, **the Wired Wood** and **Verdigris**, then the Crown Road round the Crownwall to **Kingsmead**: the **Glassfall Scar** glitters high on the wall where forty people were Fixed in AF 290, and your scar aches the whole way past it.
2. **The Looking-Glass Wood** and **Glassmere**, then **the Mirror Mere:** Archseer **Imre Dask** of the Veiled Synod ("Welcome, behind. Behind, welcome.") grants passage because Ilsa sent for you. His one rule: *never look back through the Glass once you've crossed.* ☠ **`GO_LOOKING_BACK` "Looking Back"**: on the Threshold the Mere shows Juno calling your name; turn round.
3. **The Antumbra Threshold** (`:INVERSE`): rivers run uphill and type matchups flip; every reflection holds a shadow with six black wings (a Giratina seed). S134. A wild **Ralts** rides in Juno's veil from here (she names it "Veil"; it becomes her Festival Mega Gardevoir).
4. **Lucent:** the living city and its upside-down reflection in the sky, where the Mind Plate lives. Provost **Ilsa Marr** wears earmuffs against other people's thoughts ("You're thinking very loudly. Please stop.", comedy scene "Thinking Loudly").
5. **Gym 12, the Athenaeum:** Ilsa. Badge 12, **TM29 Psychic**.
6. **The Mindscape** (S135). ⚑ **`:ch13_remember`**, to your five-year-old self ("Do you want to see the light? It's going to hurt."): *"Show me."* / *"I'm scared too."* (the memory plays) / *"...Not yet."* (it plays in Ch15's Cathedral echo instead, harder). Ilsa: "The man in white was my father." (This opens her *Little Owl* quest, S175.)
7. **Juno and the Ralts** in the cloister garden the night before the tribunal (a warm scene).
8. **The tribunal** in the Glass Court (S136). Hierophant Ellery attends with the Eevee Octave; *optional* sparring double with Vesper in the cloister. ⚑ **`:ch13_kaito`**: encourage Kaito to testify about **Marrowgate** (`KAITO_TESTIFIED`: "My orders. My unit. I sealed the gate. They were still knocking.") or tell him it isn't his burden. ⚑ **`:ch13_rowan_testimony`**: *condemn* (Rowan to the Pale Gaol; Juno's Bond down; Accord up) / *plead for mercy* (a lesser sentence, house arrest in Verdance) / *refuse to testify*.
9. **Sable exposed:** with `IRONREACH_EVIDENCE` (the comm-device from Ch9), Ilsa reads the court and says it aloud: **"Sable is Sabine Kroll. Meridian Special Accounts."** Kroll attacks from the gallery: **admin battle, Kroll** (`:MINDSCAPE`). Without it, Ilsa tells only you, and the public learns in Act IV and believes it less. Voss on every screen within the hour: "acted alone"; his approval rises.
10. **The Fault** (S137): Meridian test-fires the Arbiter Engine's Dark Stone core under Cogsworth; a tremor runs through every Imprint and the Bleed leaps forward everywhere (from Act IV, early maps use the Bleed-spread encounter tables). On the south coast the sea pulls back from Zenith's cliffs, the Sump drains, and drowned **Aurelia**'s spires stand naked below Underveil. The Glass Court's floor gives way into the flooded undercroft: Rowan chained in the dock with the water rising, Director Marchetti pinned under the orrery's brass ring. You can reach one. ⚑ **`:ch13_fault`** (who lives): *Rowan* (he escapes with Wick: "*Ask the Drowned Crown.*") / *Marchetti* (Rowan drowns; Juno's Bond drops; Marchetti: "I owe you a life", and she stands the Directorate down at the hijack).
11. *Optional:* **the Shattered Sky** (748, `:BLEED`): pieces of the upside-down city hang between earth and sky; the first **Zygarde Core**.
12. **Cliffhanger:** Ilsa at dawn hands you her father's **Secret Articles** sealed: "Go and find Bastian Ore first. He was *there*." **END OF ACT III.**

### Areas *(design only; maps not built)*

| Map (ID) | Field | Built? | Wild Pokémon (from `pbs/encounters.txt`) |
|---|---|---|---|
| Conductors' Causeway (740) | Stormfront (`:STORMFRONT`) | no | Grass: Unfezant 51–55, Emolga 51–55, Pelipper 51–55, Drifblim 51–55, Kilowattrel 51–55, Altaria 51–55, Corvisquire 51–55, Zebstrika 51–55, Ampharos 51–55, Swanna 51–55, Oricorio (Pom-Pom Style) 51–55, Skarmory 51–55, Bombirdier 51–55, Cramorant 51–55 |
| The Wired Wood (741) | Silkwood (`:SILKWOOD`) | no | Grass: Granbull 53–57, Floette 53–57, Clefairy 53–57, Jigglypuff 53–57, Dachsbun 53–57, Maushold 53–57, Oinkologne 53–57, Tinkatuff 53–57, Luxray 53–57, Manectric 53–57, Boltund 53–57, Heliolisk 53–57, Bronzong 53–57, Klang 53–57, Staraptor 53–57, Herdier 53–57 |
| Verdigris (750) | Silkwood (`:SILKWOOD`) | no | _no wild table yet_ |
| Kingsmead (756) | Meadow (`:MEADOW`) | no | _no wild table yet_ |
| The Looking-Glass Wood (752) | Mindscape (`:MINDSCAPE`) | no | _no wild table yet_ |
| Glassmere (753) | Mindscape (`:MINDSCAPE`) | no | _no wild table yet_ |
| Mirror Mere (742) | Mindscape (`:MINDSCAPE`) | no | Grass: Floette 53–57, Ribombee 53–57, Shiinotic 53–57, Masquerain 53–57, Sawsbuck 53–57, Breloom 53–57, Comfey 53–57, Ledian 53–57, Vivillon 53–57, Kirlia 53–57, Flittle 53–57, Rabsca 53–57, Azumarill 53–57, Dustox 53–57, Espathra 53–57; Surf: Azumarill 53–57, Masquerain 53–57, Lombre 53–57, Golduck 53–57, Swanna 53–57 |
| Antumbra Threshold (743) | Inverse (`:INVERSE`) | no | Grass: Misdreavus 53–57, Duskull 53–57, Flittle 53–57, Gothorita 53–57, Duosion 53–57, Inkay 53–57, Bramblin 53–57, Hattrem 53–57, Meowstic 53–57, Maschiff 53–57, Liepard 53–57, Banette 53–57, Spoink 53–57, Wynaut 53–57, Gimmighoul 53–57, Espathra 53–57 |
| Widdershins Walk (755) | Inverse (`:INVERSE`) | no | _no wild table yet_ |
| Lucent - Athenaeum Quarter (340) | Mindscape (`:MINDSCAPE`) | no | _no wild table yet_ |
| The Shattered Sky (748) | The Bleed (`:BLEED`) | no | Grass: Minior 55–58, Staraptor 55–58, Kilowattrel 55–58, Beheeyem 55–58, Bronzong 55–58, Drifblim 55–58, Sigilyph 55–58, Altaria 55–58, Carbink 55–58, Noivern 55–58, Clefairy 55–58, Archeops 55–58, Shelgon 55–58, Metang 55–58, Reuniclus 55–58 |

### Key battles

**Gym 12 — Warden Ilsa Marr** (Psychic, `:MINDSCAPE`, single battle, cap 59)

| Pokémon | Lv | Item | Ability | Moves |
|---|---|---|---|---|
| Bronzong | 57 | Mental Herb | Levitate | Trick Room, Gyro Ball, Payback, Stealth Rock |
| Slowbro | 57 | Slowbronite | Regenerator | Psychic, Scald, Calm Mind, Slack Off |
| Espeon | 58 | Life Orb | Magic Bounce | Psychic, Shadow Ball, Dazzling Gleam, Calm Mind |
| Gothitelle | 58 | Leftovers | Competitive | Psychic, Thunderbolt, Trick Room, Calm Mind |
| Reuniclus | 58 | Leftovers | Magic Guard | Psychic, Focus Blast, Shadow Ball, Recover |
| Hatterene "Hush" | 59 | Sitrus Berry | Magic Bounce | Psychic Noise, Dazzling Gleam, Mystical Fire, Trick Room |

*Bag: Mega Ring, Full Restore, Full Restore; IV 28.*

- **Hard:** Bronzong 58 @Mental Herb, Slowbro 58 @Slowbronite, Espeon 59 @Life Orb, Gothitelle 59 @Leftovers, Reuniclus 59 @Life Orb, Hatterene 59 @Life Orb
- **Casual:** Bronzong 53 @Mental Herb, Slowbro 53 @Slowbronite, Espeon 54 @Sitrus Berry, Reuniclus 54 @Sitrus Berry, Hatterene 55 @Sitrus Berry

*Field note:* "the arena reshapes itself to the challenger's memories." Psychic ×1.5, Dark and Ghost ×1.2 (nightmares lurk), rooms last longer, sleepers wake fast. **Mega Slowbro** (Shell Armor) is her Trick Room Mega; Bronzong, Gothitelle and Hatterene set the room. Dark moves curdle the field into a Nightmare; Topsy-Turvy or three damaging sound moves crack it into Inverse; Hatterene's Psychic Noise is a sound move, so three of them flip it too. *Tip:* Dark and Ghost hit harder here for you too, and her Calm Minds soothe a Nightmare back to a dream; Inner Focus, Own Tempo and Oblivious Pokémon take less from Psychic. On Hard her last Pokémon is a 2-bar boss (`WARDEN_ACE_2BAR`).

**Sabine Kroll** (`MERIDIAN_KROLL` v0, the Glass Court, `:MINDSCAPE`; only with `IRONREACH_EVIDENCE`)

| Pokémon | Lv | Item | Ability | Moves |
|---|---|---|---|---|
| Sharpedo | 57 | Sharpedonite | Speed Boost | Crunch, Waterfall, Ice Fang, Protect |
| Toxicroak | 57 | Life Orb | Dry Skin | Drain Punch, Gunk Shot, Sucker Punch, Swords Dance |
| Honchkrow | 58 | Scope Lens | Super Luck | Night Slash, Brave Bird, Sucker Punch, Roost |
| Drapion | 59 | Black Glasses | Sniper | Knock Off, Cross Poison, Earthquake, Swords Dance |

*Bag: Mega Ring, Full Restore, Full Restore; IV 28.*

- **Hard:** Sharpedo 58 @Sharpedonite, Toxicroak 58 @Life Orb, Crawdaunt 58 @Sitrus Berry, Honchkrow 59 @Scope Lens, Drapion 59 @Black Glasses
- **Casual:** Sharpedo 53 @Sharpedonite, Honchkrow 54 @Scope Lens, Drapion 55 @Black Glasses

**Optional — Vesper** (cloister double, `:MINDSCAPE`): Espeon 56 @Twisted Spoon, Umbreon 56 @Leftovers, Sylveon 57 @Sitrus Berry, Eevee 58 @Eviolite.

### Side quests

- **The Still Water** (`AN_OCTAVE_STILL_WATER`, The Rite of Reflection; wired (playable)). Lento of the Octave (the Rite, read at Glassmere), the frozen Mirror Mere, past Glassmere (753) (742). Unlock: Badges ≥ 11. Mirror-writing in the reading-pool: the Mirror Mere froze in summer. Its singer won't leave the ice. Her reflection is under it. Reward: $4000, Mirror Herb; +4 pts.
- **Your Other Half** (`AN_OTHER_HALF`, The Rite of Reflection; designed (not wired yet)). a Glassmere fisherwoman, Glassmere (753). Unlock: Badges ≥ 11. Her husband came back from the Mere reversed: left-handed, kinder, and worse at fishing. She'd like the old one back. Probably. Reward: Indeedee Lv 55 (PSYCHICSURGE); +3 pts.
- **It Keeps the Rain In** (`AN_UMBRELLA`, The Rite of Reflection; designed (not wired yet)). a man with an umbrella, the Antumbra Threshold (743). Unlock: Badges ≥ 11. His umbrella keeps the rain in. He'd like it to keep the rain out. He's tried holding it the other way up. That keeps the rain up. Reward: Hatenna Lv 54 (MAGICBOUNCE); +2 pts.
- **Better Marks** (`AN_STUDENT`, The Rite of Reflection; designed (not wired yet)). a Lucent student, the Athenaeum, Lucent (344). Unlock: Badges ≥ 11. Her reflection has been attending lectures for her. It gets better marks. She is furious and wants to sit the final herself. Reward: Twisted Spoon; +3 pts.
- **The Echo That Answers First** (`AN_ECHO_HALL`, The Rite of Reflection; designed (not wired yet)). Lector Saffi Ivarne, the Speculum, Lucent (346). Unlock: Badges ≥ 12. An echo in the Speculum answers questions before they're asked. The Lectors would like to ask it one. Reward: TM48 Skill Swap; +4 pts.
- **Shadows Fall Upward** (`AN_SHADOWS_UP`, The Rite of Reflection; designed (not wired yet)). a Vigil medium, the Obsidian Barrows (760). Unlock: Badges ≥ 12. In the Barrows, shadows fall upward. Somebody's shadow has fallen all the way up and got stuck on the inverted desert in the sky. Reward: Elemental Seed x2; +4 pts.
- **The Eevee Octave, singer 7 of 8: Lento** (*The Still Water*, the frozen Mirror Mere past Glassmere): Froslass 57 @Sitrus Berry, Glaceon 58 @Leftovers.

**Event Pokémon:**

- **Indeedee Lv 55 (PSYCHICSURGE)**: gift, Glassmere. Choose between two husbands. *(designed, not implemented)*
- **Hatenna Lv 54 (MAGICBOUNCE)**: gift, the Antumbra Threshold. Open the umbrella indoors (which is outdoors). *(designed, not implemented)*

**Mega Stones and Z-crystals:**

_None placed for this chapter._

### Gym 12 — the Athenaeum (Ilsa Marr) *(design only)*

- **Puzzle (8/10, about 30 minutes): "your reflection keeps you honest."** Beyond a mirror wall walks your reflection: when you step left it steps right; up and down match; its side has different walls, and a blocked body stays put while the other moves (the only way to desync the pair). Plates and doors need you both in place.
    - **350 Reading Room:** up three, one step left; both on plates.
    - **351 Mirror Hall:** 26 steps with three deliberate desyncs, `U U R R R R U R R U U U L L L L L L D R R U R U U L` (hint: start by walking it into the wall on its row 7).
    - **352 Swap Atrium:** swap pads trade your places; thought tiles are walls to you and floor to it. Lead the reflection through the thought maze to the pad nearest Q, swap, walk *it* onto P by desyncing against a wall, swap back and walk yourself next to Q. *(To be verified by the builder.)*
- **Badge:** Badge 12. **TM29 Psychic.** **Level cap after: 63.**
- **Mastery (optional):** the Quiet Room (356): five readers, exactly two lie. **Door 4.** Reward: Magical Seed ×2, Twisted Spoon and Ilsa's unsent letter to Valen.
- **Gym trainers:** 6 (Psychic ×4, Channeler, Scholar), Lv 55–58; on Hard Ilsa gets an EBDX multi-bar intro. *(Not in PBS yet.)*

# Act IV — The Drowned Crown

*Design only (outline: `story/07_ACT_IV.md`, with `14_WAR_AND_BLESSING.md`); no Act IV map is built except two war-theatre maps (928, 930) that Ch19 uses. From the start of Act IV, revisited early maps use the **Bleed-spread** encounter tables (version 1 in `pbs/encounters.txt`): the Areas tables in Acts I–II show them in their "Act IV on" rows. If Rowan drowned at the Fault, his Act IV–V lines go to the Lantern Hollow's leader (Teo if saved, otherwise Thistle with Wick).*

**Act-opening state:** Briarwick's Glasswood has reached the looms, the Lowlight's glass has spread a block, and Saltmere has a glass puddle on the promenade that Dorian has roped off as "our first miracle, darlings". The screens show the south coast: the sea pulled back from Zenith's cliffs and drowned Aurelia's spires in the mud below Underveil. The Concert of Regions will decide on **Severance** at the Festival.

## Chapter 14 — "The Deep Seams"

*The Grave Road out of Antumbra: Yesterday's Road (772), Vigil and the Grave Glass, the Obsidian Barrows (760, `:INVERSE`), Spinefall Gorge (761, Waterfall), the Vertebrae (773) up to Cragholm (360–374, Ossaria) and its Lift Galleries (363). Optional: Geode Hollow (764/765), the Dreaming Quarter (768). Transit: Duneholt at the war's edge, the Duneholt Undersands (783, Groudon), Stonesleep (788), the Dry Tide (810) and the bone-carters' camp (930). Design only. Gym 13. One of the densest chapters: keep side content short.*

### Key events

- **Bastian's account** of AF 290 (brass behind the Choir loft, men in white coats with little gold suns on their pockets watching dials, "They weren't surprised. They were *pleased*.") and **the Ring-Day**: Bastian gives you a Warden's ring (the Mega Ring) cut by Brann ten years ago, and it *sings* in your palm.
- **The badge case opened.** Larch finds a sliver of Lattice-glass and a transmitter in its lining: "Voss isn't watching you. He's **tuning** you." (⚑ `:ch14_telemetry`), then the raid, and **Groudon** under Duneholt.

### Order of events

1. **The Grave Road:** Yesterday's Road (milestones that count down, then up), out through the Grave Glass at Vigil, the **Obsidian Barrows** (`:INVERSE`; tomb-mirrors and a desert hanging in the sky), **Spinefall Gorge** (Waterfall) and **the Vertebrae** up to Cragholm's lift towers.
2. **Cragholm:** a canyon wall of lamplit galleries and lift-cages. Kassan has sold the seams to Meridian, whose new Lattice-drill chews into the Stone Plate's crystal halls; the miners are refugees from the Thaw, the western dunes and the Mandate raids. Warden **Bastian Ore** (74, a miner's lamp on his hat, deaf to Directorate questions): "Ilsa sent you? Sit down, I'm telling you about the crown." His granddaughter **Pip** (14) guides you through the deep seams.
3. **The deep seams** (the hidden refuge): Larch (smuggled in by Odessa), Rimeholt refugees, the Lantern Hollow (Rowan, gaunt, with Wick and Thistle, or their new leader), and **Corvin's field hospital** if you freed him in *The Doctor's Cell* (otherwise a frightened Wenlow runs it alone). On screens: **the Steamline**, steam-glass across Ossaria's western dunes between the two armies; a Meridian convoy carries identical Prism lances for both sides (the manifests are evidence for later, not a choice).
4. **Anja** arrives on day two with Rimeholt refugees under the bone-carters' white banner (she won't meet your eyes if you exposed her; she shakes your hand if she confessed). She leaves west for Skaldfast. Warm scene: date-bread and miners' stew at one table.
5. **Bastian's account** (above). Comedy scene "Selectively" (Bastian vs a Directorate officer, before the raid).
6. **Gym 13, the Lamp Galleries:** Bastian. Badge 13, **TM76 Stealth Rock**. His Aerodactyl "Amber" Mega Evolves: the last Mega you face without a ring.
7. **The Ring-Day** (Bastian's lamp-room in the Lift Galleries, 363; the hidden Trials quest `OS_RING_DAY`, no gong): **Mega Ring** and **Aggronite**. The ring opens Mega Evolution *and* Z-moves (one of each per side); any stones already in your Bag "stop waiting". Brann cut it and posted it to Bastian "in a sock" because it sulked on every hand; it sings for you. (Nobody says why until Ch17.)
8. **Larch and the badge case.** ⚑ **`:ch14_telemetry`** (major; feeds the endings): *destroy it* (Voss loses the stream, the Engine is under-calibrated, but he moves faster) / *feed it false data* (`TELEMETRY_SABOTAGED`: the strongest single weakening of the finale; every later badge has a "did he notice?" beat) / *leave it* (the road to the Bad ending if other safeguards fail too).
9. **The raid:** Marchetti's Directorate comes down the lifts for Larch and Rowan. ☠ **`GO_WILLING` "Willing"**: let Dr Quent "remove the faulty device painlessly" (Larch warned you a scene earlier: "Never, ever let them examine you"). **Admin battle: Marchetti** in the Darkglass gallery (she shoots the lamps out: `:DARK_CRYSTAL`), the first fight where both sides can Mega Evolve. **Thistle defects openly** and holds the lift-shaft (earlier and warmer at high Hollow Standing).
10. ⚑ **`:ch14_marchetti`**: show her the **Splitter Casing** (Ch12) or the Ironreach comm-device (Ch9): "Your own Special Accounts bombed Skyreach." With either, `MARCHETTI_TURNED` becomes possible: she goes very still now and stands down at the hijack. Without evidence she stays loyal.
11. **Transit through Duneholt** at the war's edge: the great well is a dry shaft, and the drill has punched into something hot. **Kassan** receives you in the Hall of Audience between a Meridian paymaster and two quartermasters who aren't speaking, and shows you **the Elector's Lease** ("The Bone Sands have buried every army that ever marched into them. I only charge for the plot."). The bone-carters' elder asks you to bring out the dead in the steam-glass (optional, from their camp on the Dry Tide).
12. ⚑ **`:war_convoy`** (War 2; offered by Gale Post from Marisol): the caravan-mothers lead her sledges west to the Steamline and you walk point through the glass into Isenmar's lines: *relief* (food) / *arms* (harpoon-guns) / *refuse* (the food goes to Duneholt's refugees).
13. **The Duneholt Undersands** (783): **boss: Groudon**, woken by the drills, in a chamber of Unown glyphs recording the "Year of Two Weathers". Sahar reads them between bars: *"The King woke the red one and the blue one to remake the land. When they would not obey, he turned his eyes to heaven."* Groudon sinks back and the aquifer starts, slowly, to refill (the first good news in an act). **Stonesleep** (788, `:BLEED`) opens: rare fossils for the Dig Lab.
14. **Cliffhanger:** on Hindmoor, Kestrel's Meridian sponsor airship passes overhead toward Gravenmoor. Pip: "Who'd sponsor a *graveyard*?"

### Areas *(design only; maps not built except the bone-carters' camp)*

| Map (ID) | Field | Built? | Wild Pokémon (from `pbs/encounters.txt`) |
|---|---|---|---|
| Yesterday's Road (772) | Inverse (`:INVERSE`) | no | _no wild table yet_ |
| The Obsidian Barrows (760) | Inverse (`:INVERSE`) | no | Grass: Xatu 55–59, Inkay 55–59, Claydol 55–59, Liepard 55–59, Mightyena 55–59, Misdreavus 55–59, Palossand 55–59, Bronzong 55–59, Golurk 55–59, Gothitelle 55–59, Musharna 55–59, Absol 55–59, Zoroark 55–59, Houndstone 55–59, Runerigus 55–59, Gardevoir 55–59 |
| Spinefall Gorge (761) | Desert (`:DESERT`) | no | Grass: Donphan 57–61, Rhydon 57–61, Mudsdale 57–61, Sandslash 57–61, Lycanroc 57–61, Hippowdon 57–61, Krookodile 57–61, Garganacl 57–61, Klawf 57–61, Flygon 57–61, Gogoat 57–61, Ursaring 57–61, Sudowoodo 57–61, Orthworm 57–61; Surf: Poliwhirl 55–61, Golduck 55–61, Floatzel 55–61, Azumarill 55–61, Swanna 55–61, Gyarados 55–61; Old Rod: Magikarp 30–40, Goldeen 30–40; Good Rod: Seaking 50–58, Poliwhirl 50–58, Basculin 50–58 |
| The Vertebrae (773) | Mountain (`:MOUNTAIN`) | no | _no wild table yet_ |
| Cragholm (360) | Desert (`:DESERT`) | no | _no wild table yet_ |
| Cragholm - Lift Galleries (363) | Cave (`:CAVE`) | no | _no wild table yet_ |
| Geode Hollow (764) | Crystal Cavern (`:CRYSTAL_CAVERN`) | no | Cave: Carbink 56–61, Boldore 56–61, Sableye 56–61, Crustle 56–61, Lairon 56–61, Mawile 56–61, Nosepass 56–61, Minior 56–61, Metang 56–61, Klefki 56–61, Shuckle 56–61, Naclstack 56–61, Probopass 56–61, Steelix 56–61, Glimmora 56–61 |
| Geode Hollow B1F (765) | Crystal Cavern (`:CRYSTAL_CAVERN`) | no | Cave: Carbink 58–61, Graveler 58–61, Minior 58–61, Crustle 58–61, Pupitar 58–61, Metang 58–61, Aggron 58–61, Bronzong 58–61, Lunatone 58–61, Solrock 58–61, Klefki 58–61, Sableye 58–61, Garganacl 58–61, Duraludon 58–61, Steelix 58–61, Glimmora 58–61 |
| The Dreaming Quarter (768) | The Bleed (`:BLEED`) | no | Grass: Musharna 59–62, Hypno 59–62, Mr. Mime 59–62, Meowstic 59–62, Dusclops 59–62, Jynx 59–62, Gothitelle 59–62, Reuniclus 59–62, Malamar 59–62, Slowking 59–62, Galarian Slowpoke 59–62, Banette 59–62, Bruxish 59–62, Hatterene 59–62, Grimmsnarl 59–62, Indeedee 59–62 |
| Duneholt Undersands (783) | Desert (`:DESERT`) | no | Cave: Cofagrigus 60–65, Palossand 60–65, Golurk 60–65, Claydol 60–65, Sandaconda 60–65, Hippowdon 60–65, Krookodile 60–65, Dugtrio 60–65, Runerigus 60–65, Flygon 60–65, Gabite 60–65, Unown 60–65, Garganacl 60–65, Marowak 60–65 |
| Stonesleep (788) | The Bleed (`:BLEED`) | no | Grass: Sudowoodo 63–66, Stonjourner 63–66, Relicanth 63–66, Golurk 63–66, Runerigus 63–66, Cursola 63–66, Gigalith 63–66, Probopass 63–66, Garganacl 63–66, Omastar 63–66, Kabutops 63–66, Cradily 63–66, Armaldo 63–66, Rampardos 63–66, Bastiodon 63–66, Carracosta 63–66, Archeops 63–66, Tyrantrum 63–66, Aurorus 63–66, Aerodactyl 63–66 |
| The Dry Tide (810) | Desert (`:DESERT`) | no | _no wild table yet_ |
| The Bone-Carters' Camp (930) | Desert (`:DESERT`) | yes | _no wild table yet_ |

### Key battles

**Gym 13 — Warden Bastian Ore** (Rock, `:CRYSTAL_CAVERN`, single battle, cap 63)

| Pokémon | Lv | Item | Ability | Moves |
|---|---|---|---|---|
| Carbink | 61 | Light Clay | Sturdy | Stealth Rock, Power Gem, Dazzling Gleam, Reflect |
| Golem | 61 | Sitrus Berry | Galvanize | Double-Edge, Stone Edge, Earthquake, Explosion |
| Aurorus | 62 | Sitrus Berry | Refrigerate | Hyper Voice, Ancient Power, Earth Power, Flash Cannon |
| Aerodactyl "Amber" | 62 | Aerodactylite | Pressure | Rock Slide, Dual Wingbeat, Crunch, Ice Fang |
| Rhyperior | 62 | Assault Vest | Solid Rock | Stone Edge, Earthquake, Megahorn, Ice Punch |
| Gigalith "Geode" | 63 | Magical Seed | Sturdy | Stone Edge, Earthquake, Body Press, Power Gem |

*Bag: Mega Ring, Full Restore, Full Restore; IV 28.*

- **Hard:** Carbink 62 @Light Clay, Golem 62 @Sitrus Berry, Aurorus 63 @Choice Specs, Aerodactyl 63 @Aerodactylite, Rhyperior 63 @Assault Vest, Gigalith 63 @Weakness Policy
- **Casual:** Carbink 57 @Light Clay, Aurorus 58 @Sitrus Berry, Aerodactyl 58 @Aerodactylite, Rhyperior 58 @Assault Vest, Gigalith 59 @Sitrus Berry

*Field note:* "light through crystal; darken it and the whole field turns." Rock ×1.3, Dragon ×1.2, sound ×1.2; the glow cycles red → blue → green → amethyst each round (Fire, Water, Grass, Psychic) and Rock moves hit as the glow's type too; light moves (Power Gem, Flash Cannon, Dazzling Gleam, Ancient Power...) ×1.5; screens last two turns longer. Dark Pulse, Night Daze or a sandstorm darken it to the **Dark Crystal Cavern**; an explosion or three quakes shatter it to a plain Cave. **Mega Aerodactyl "Amber"** (Tough Claws; no sand, so his crystals stay lit). *Tip:* Water, Grass, Fighting, Ground and Steel; Dark Pulse turns his light-move field into one that favours Dark and Ghost.

**Director Marchetti, the Darkglass gallery** (`MERIDIAN_MARCHETTI` v1, `:DARK_CRYSTAL`)

| Pokémon | Lv | Item | Ability | Moves |
|---|---|---|---|---|
| Houndoom | 61 | Houndoominite | Flash Fire | Dark Pulse, Flamethrower, Sludge Bomb, Nasty Plot |
| Arcanine | 62 | Sitrus Berry | Intimidate | Flare Blitz, Crunch, Extreme Speed, Wild Charge |
| Corviknight | 62 | Leftovers | Mirror Armor | Brave Bird, Body Press, Bulk Up, Roost |
| Mabosstiff | 63 | Black Glasses | Intimidate | Crunch, Jaw Lock, Play Rough, Psychic Fangs |

*Bag: Mega Ring, Full Restore, Full Restore; IV 28.*

- **Hard:** Houndoom 62 @Houndoominite, Arcanine 63 @Sitrus Berry, Kingambit 62 @Black Glasses, Corviknight 63 @Leftovers, Mabosstiff 63 @Black Glasses
- **Casual:** Houndoom 57 @Houndoominite, Corviknight 58 @Leftovers, Mabosstiff 59 @Sitrus Berry

*Field note:* Dark ×1.5, Ghost ×1.3; Dark and Ghost contact moves +1 crit; your non-Dark/Ghost/Rock moves are ×0.9 accurate. Two light moves (Flash Cannon, Dazzling Gleam...) or sun relight the crystals, and one Dark Pulse darkens them again. *Tip:* Fighting and Ground for Mega Houndoom; relight the cavern if your team isn't Dark.

**Boss — Groudon** (Duneholt Undersands, `:DESERT`) *(planned multi-bar boss; not registered in Prismfall Bosses yet; the plugin already knows Groudon's Red Orb for a Primal form).*

### Side quests

- **The Old Pincer** (`EL_OLD_PINCER`, The Quiet Way; wired (playable)). the Woodward, the Woodward's Hut, Gossamer Wood; the fight is in the Gossamer Heartwood (526). Unlock: Badges ≥ 12. A lantern from the Woodward: 'THE OLD PINCER HAS TAKEN THE HEARTWOOD SAP. BRING SOMEONE STRONG.'. Reward: Pinsirite; +3 pts.
- **The Ring-Day** (`OS_RING_DAY`, The Rolls of Unearthing; wired (playable)). Bastian Ore, Bastian's lamp-room, the lowest of the Cragholm Lift Galleries (after Gym 13) (363). Unlock: Badges ≥ 13 and !mega_ring. Bastian wants you in his lamp-room. Reward: Mega Ring, Aggronite; +0 pts.
- **Amber, Again** (`OS_AMBER_AGAIN`, The Rolls of Unearthing; wired (playable)). Sahar Ostrand, Sahar's Dig Lab, Duneholt (209). Unlock: Badges ≥ 12. TABLET: The Old Amber held two things. The Warden kept one. Bring her the other, alive. Reward: Aerodactylite; +2 pts.
- **The Unquiet Elector** (`OS_UNQUIET_ELECTOR`, The Rolls of Unearthing; designed (not wired yet)). an embalmer of Vigil, Vigil (770). Unlock: Badges ≥ 12. A dead Elector keeps walking out of his tomb-mirror to vote. The Veiled Synod says the dead are theirs. Vigil says the dead are Vigil's. Reward: Galarian Yamask Lv 60 (WANDERINGSPIRIT); +4 pts.
- **Where the Well Went** (`OS_UNDERSANDS`, The Rolls of Unearthing; designed (not wired yet)). Sahar's foreman, the Duneholt Undersands (783). Unlock: Badges ≥ 12 and S137 CH13_FAULT. Duneholt's well is dry. The diggers think the water went down. They want someone to follow it. Reward: Telluric Seed x2, Exp. Candy L x2; +4 pts.
- **The Bonewright's Rite** (`OS_BONEWRIGHT`, The Rolls of Unearthing; designed (not wired yet)). Curator-Elect Nasrin Vael, Cragholm (360). Unlock: Badges ≥ 13. Reassemble a whole fossil skeleton from the pieces the Rolls have collected across Ossaria, in the right order, in front of the Curators. Reward: Ability Capsule; +5 pts.
- **The bone-carters' dead** (optional, 14_WAR_AND_BLESSING): from their camp on the Dry Tide, bring out the dead the carts can't reach inside the steam-glass. *(No quest entry yet.)*

**Event Pokémon:**

- **Galarian Yamask Lv 60 (WANDERINGSPIRIT)**: gift, Vigil. Hold the dead Elector's last election. *(designed, not implemented)*
- **Pinsir "Old Pincer" Lv 62 (MOXIE)**: boss battle (guards a reward; doesn't join), Gossamer Heartwood, the great sap tree. Free the Heartwood's sap tree (the Woodward's request).

**Mega Stones and Z-crystals:**

- **Aggronite** (Mega Stone): the Ring-Day, with the Mega Ring (Bastian's lamp-room, `OS_RING_DAY`).

- **Alakazite** (Mega Stone, from Badge 12): Lucent Athenaeum, the Sealed Stacks: the Unread Shelf. **puzzle**. *(planned: map not built)*
- **Aerodactylite** (Mega Stone, from Badge 12): Sahar's Dig Lab, Duneholt: bring her a revived Aerodactyl. quest OS_AMBER_AGAIN. *(planned: map not built)*
- **Pinsirite** (Mega Stone, from Badge 12): Gossamer Heartwood: the Old Pincer. **boss** EL_OLD_PINCER. *(planned: map not built)*

### Gym 13 — the Lamp Galleries (Bastian Ore) *(design only)*

- **Puzzle (8/10, about 30 minutes): "light remembers its colour."** A miner's lamp throws a beam; mirrors (`/` or `\`) turn it; filter crystals recolour it, and a crystal takes the **last** colour that touched it; gates open only to their colour; the red alarm crystal resets the board.
    - **370 Lamp Room:** turn both mirrors to bend the beam round the pillar into the white gate.
    - **371 Prism Gallery** (blue gate): **3 turns: M2 → `/`, M3 → `\`, M4 → `\`.** The beam goes lamp → M1 up → M2 east → red filter → M3 down → blue filter → M4 east → gate (the last filter wins). The path along row 5 looks shorter and never meets the blue filter. Hints: lamp boy Pell.
    - **372 Quarry:** two lamps, a splitter, Strength boulders and a Rock Climb wall; the lamps shine in the cavern's current glow, which advances one step each time a gate opens. Open the practice gate to bring the glow to green, block the splitter's west fork with boulder 1 for the green gate, then (glow now amethyst) pull boulder 1 back from the upper gallery and block the east fork with boulder 2 for the amethyst gate. *(To be verified by the builder.)*
- **Badge:** Badge 13. **TM76 Stealth Rock.** **Level cap after: 67.** Then the Mega Ring (above).
- **Mastery (optional):** Bastian's Seam (374): light the four colour crystals in the order his crown story names them, **amethyst, red, green, blue**. Reward: Telluric Seed ×2, Light Clay and a fugitive's thank-you.
- **Gym trainers:** 5 (Hiker ×2, Ruin Maniac, Worker, Gemcutter), Lv 59–62. *(Not in PBS yet.)*

---

## Chapter 15 — "The Hollow Cathedral"

*The Moor Road back along the ridge: the Jawbone Ridge (780, the Darkglass Mine headframe 784/785), Vigil, Hindmoor (781, fog), the Downflame Road (790) to Gravenmoor (380–395, Antumbra) with Vane Hall (383) and the Lantern Hospice (384). On the way out: the Noonless Road (800) with the Barrow of the Wardens (804/805), Giratina's Reverse Depths (806, `:INVERSE`) and the Hush (808). Design only. Gym 14.*

### Key events

- **The Cathedral echo.** Kestrel forces the Spooky Plate to replay AF 290 through **Morwen's eyes**: Voss young at the dials behind the Choir loft, a splinter of colourless light flying from the Crown into a five-year-old's chest, Morwen throwing herself over the child as the Glassfall turns forty people to glass, Valen's "**Find the child.** Whatever it costs.", and Morwen sending the child away on **Edda's** night ferry. Then her echo looks at you: *"Little one. You came back. I told her not to let you."*
- **K6.** Kestrel learns his mother ruined her own name to save you (⚑ `:ch15_kestrel`), then **Giratina** in the Reverse Depths.

### Order of events

1. **The Jawbone Ridge:** the war's smoke on the western sky. At Vigil a Gale Post courier brings news of **the Siege of Skaldfast**, with Anja's name on the list of the taken (⚑ `:war_prisoner`, below).
2. **Hindmoor** (standing pools that show what is behind you) and the **Downflame Road** to Gravenmoor: fog, barrows, lanterns, and echoes of the dead (a woman sweeping a step that isn't there). **Archseer Dask** has come himself ("The echoes are louder. Louder, the echoes."; his second encounter, needed for the Ruin Route). Warden **Ysolde Ashgrave**: "The dead aren't gone here. They're just very bad at conversation." She has been waiting for you, and for Kestrel. Comedy scene "The Dead Are Bad at This" (before the Cathedral; nothing after).
3. **Vane Hall** (the sad haunted house): Kestrel's childhood home, dust-sheeted, with echoes of his family; a puzzle path through rooms replaying AF 290 from the household's side (a clock stopped at 11:40). "That's my room. That's — don't touch that."
4. **Gym 14, the Hollow Cathedral:** Ysolde. Badge 14, **TM30 Shadow Ball**.
5. **The Cathedral echo** (above). If you chose "Not yet" in Ch13 this is your first time, and it's harder. ☠ **`GO_ECHO` "Echo"**: afterwards an echo of Ines keeps singing in the loft; choose "Stay and listen?" three times (your hand turns translucent on the second).
6. **K6** (raw and furious; the Gauntlet overloads and the field flickers to `:BLEED` for a turn). If you sent him the letter in Ch12: "You sent me her *letter*, and you still came here."
7. ⚑ **`:ch15_kestrel`** (an authored PC line): *"I'm sorry. I didn't know. I'd give it back if I could."* (Bond up a lot, delayed) / *"I was five. She chose. Don't you dare make her choice my crime."* (Bond down now; unlocks his Redeemed path at K8) / *"...Your mother saved my life. I'm going to make it worth it."* (Bond up; Resonance toward Harmony). Ysolde follows him to the moor and gives him **Morwen's Mismagius**; he refuses **Morwen's sealed letter**, and she keeps it for the Festival semifinal.
8. **Edda at Morwen's grave** (the barrows below the Lantern Hospice): "I took you out on the night ferry. Brought you back on the last one. Tide's got a sense of humour. ... She paid me in her Warden's ring. I never sold it." Key item **Morwen's Ring** (for Kestrel in Act V).
9. ⚑ **`:war_prisoner`** (War 3, Ch15–16): Odessa flies you over the lines by Gale Post to Anja in the Ashkaar Siege Camp. *Free* her through the Steamline / broker an *exchange* at a caravan well under the bone-carters' banner (the Thane holds the Dominar's nephew) / *leave* it. In the cage: "Tell my brother I'd have signed for the heaters again."
10. **The Barrow of the Wardens** (804/805, off the Noonless Road): Wardens buried with replica Plates, and a barrow-door that opens *downward into the sky*.
11. **Giratina's Reverse Depths** (806, `:INVERSE`): **boss: Giratina** (Altered, then Origin on the last bar), furious and wounded by the Fault and the Gauntlet. Afterwards it looks at you the way Kyogre did (*it has been guarding the hole your god left for three hundred years*) and closes the tear. Its wound is why other-world visitors keep slipping into Velmora (the cameo quests).
12. ⚑ **`:ch15_look_back`** (only with a full Ledger, `ruin_unlocked`): a black pane shows Juno calling your name, the exact image of `GO_LOOKING_BACK`. *Yes:* the reflection steps aside and you walk into **the Ruin Route** (`story/12_RUIN_ROUTE.md`). *No:* the door never reopens on that save.
13. **The Hush** (808, `:BLEED`): no sound at all; your footsteps show as ripples.

### Areas *(design only; maps not built except the Siege Camp pavilion)*

| Map (ID) | Field | Built? | Wild Pokémon (from `pbs/encounters.txt`) |
|---|---|---|---|
| The Jawbone Ridge (780) | Mountain (`:MOUNTAIN`) | no | Grass: Rhydon 59–63, Graveler 59–63, Lycanroc 59–63, Donphan 59–63, Sudowoodo 59–63, Sandslash 59–63, Krookodile 59–63, Coalossal 59–63, Drapion 59–63, Excadrill 59–63, Hippowdon 59–63, Sandaconda 59–63, Garganacl 59–63, Steelix 59–63, Pupitar 59–63, Gligar 59–63, Flygon 59–63 |
| Darkglass Mine (784) | Dark Crystal Cavern (`:DARK_CRYSTAL`) | no | Cave: Boldore 60–65, Carbink 60–65, Sableye 60–65, Onix 60–65, Lairon 60–65, Golurk 60–65, Krookodile 60–65, Crustle 60–65, Glimmora 60–65, Steelix 60–65, Excadrill 60–65, Doublade 60–65, Deino 60–64, Zweilous 60–65 |
| Darkglass Mine B1F (785) | Dark Crystal Cavern (`:DARK_CRYSTAL`) | no | Cave: Bisharp 62–66, Steelix 62–66, Golurk 62–66, Carbink 62–66, Krookodile 62–66, Garganacl 62–66, Rhydon 62–66, Boldore 62–66, Pupitar 62–66, Glimmora 62–66, Sableye 62–66, Excadrill 62–66, Zweilous 62–66, Deino 62–63, Dugtrio 62–66, Tyranitar 62–66 |
| Hindmoor (781) | Inverse (`:INVERSE`) | no | Grass: Mightyena 61–65, Liepard 61–65, Misdreavus 61–65, Houndoom 61–65, Honchkrow 61–65, Mandibuzz 61–65, Skuntank 61–65, Dusclops 61–65, Banette 61–65, Gourgeist 61–65, Drifblim 61–65, Thievul 61–65, Houndstone 61–65, Zoroark 61–65, Trevenant 61–65, Sneasel 61–65, Galarian Linoone 61–65; Surf: Tentacruel 60–66, Pelipper 60–66, Wailmer 60–66, Wailord 60–66, Mantine 60–66, Lapras 60–66, Sharpedo 60–66; Old Rod: Magikarp 30–40, Finneon 30–40; Good Rod: Kingler 55–63, Lumineon 55–63, Crawdaunt 55–63, Octillery 55–63 |
| Downflame Road (790) | Inverse (`:INVERSE`) | no | _no wild table yet_ |
| Gravenmoor (380) | Hollow Cathedral (`:HOLLOW_CATHEDRAL`) | no | _no wild table yet_ |
| Vane Hall (383) | none | no | _no wild table yet_ |
| Lantern Hospice (384) | none | no | _no wild table yet_ |
| The Noonless Road (800) | Inverse (`:INVERSE`) | no | Grass: Gourgeist 63–67, Sinistea 63–67, Phantump 63–67, Misdreavus 63–67, Trevenant 63–67, Alolan Marowak 63–67, Mimikyu 63–67, Drifblim 63–67, Banette 63–67, Honchkrow 63–67, Mandibuzz 63–67, Absol 63–67, Houndstone 63–67, Poltchageist 63–67, Lampent 63–67, Drakloak 63–67 |
| Barrow of the Wardens (804) | Cave (`:CAVE`) | no | Cave: Dusclops 64–69, Golbat 64–69, Golurk 64–69, Banette 64–69, Sableye 64–69, Doublade 64–69, Lampent 64–69, Haunter 64–69, Misdreavus 64–69, Cofagrigus 64–69, Palossand 64–69, Runerigus 64–69, Drakloak 64–69, Mimikyu 64–69 |
| Barrow Sanctum (805) | Hollow Cathedral (`:HOLLOW_CATHEDRAL`) | no | Cave: Dusclops 66–70, Doublade 66–70, Lampent 66–70, Golurk 66–70, Banette 66–70, Haunter 66–70, Cofagrigus 66–70, Sableye 66–70, Drakloak 66–70, Sinistea 66–70, Mimikyu 66–70, Palossand 66–70 |
| Giratina's Reverse Depths (806) | Inverse (`:INVERSE`) | no | Grass: Gothitelle 66–70, Reuniclus 66–70, Malamar 66–70, Bronzong 66–70, Claydol 66–70, Beheeyem 66–70, Dusclops 66–70, Hypno 66–70, Sigilyph 66–70, Espathra 66–70, Houndstone 66–70, Dusknoir 66–70, Gengar 66–70 |
| The Hush (808) | The Bleed (`:BLEED`) | no | Grass: Mismagius 67–70, Gourgeist 67–70, Trevenant 67–70, Banette 67–70, Gengar 67–70, Dusknoir 67–70, Chandelure 67–70, Jellicent 67–70, Dhelmise 67–70, Polteageist 67–70, Cofagrigus 67–70, Alolan Marowak 67–70, Cursola 67–70, Aegislash 67–70, Drakloak 67–70, Runerigus 67–70, Dragapult 67–70 |
| Ashkaar Siege Camp - Command Pavilion (928) | none | yes | _no wild table yet_ |

### Key battles

**Gym 14 — Warden Ysolde Ashgrave** (Ghost, `:HOLLOW_CATHEDRAL`, cap 67; GYM_PUZZLES says double battle, Core's gym table sets no double rule)

| Pokémon | Lv | Item | Ability | Moves |
|---|---|---|---|---|
| Sableye | 65 | Sablenite | Prankster | Will-O-Wisp, Foul Play, Recover, Shadow Sneak |
| Spiritomb | 65 | Sitrus Berry | Infiltrator | Sucker Punch, Shadow Sneak, Will-O-Wisp, Curse |
| Dusknoir | 66 | Leftovers | Pressure | Shadow Sneak, Shadow Punch, Brick Break, Pain Split |
| Cofagrigus | 66 | Magical Seed | Mummy | Shadow Ball, Will-O-Wisp, Body Press, Pain Split |
| Gengar | 66 | Sitrus Berry | Cursed Body | Shadow Ball, Sludge Bomb, Focus Blast, Destiny Bond |
| Chandelure "Vigil" | 67 | Spell Tag | Flash Fire | Shadow Ball, Mystical Fire, Energy Ball, Calm Mind |

*Bag: Mega Ring, Full Restore, Full Restore; IV 28.*

- **Hard:** Sableye 66 @Leftovers, Spiritomb 66 @Sitrus Berry, Dusknoir 67 @Leftovers, Cofagrigus 67 @Magical Seed, Gengar 67 @Gengarite, Chandelure 67 @Choice Specs
- **Casual:** Sableye 61 @Sablenite, Dusknoir 62 @Leftovers, Cofagrigus 62 @Sitrus Berry, Gengar 62 @Sitrus Berry, Chandelure 63 @Spell Tag

*Field note:* "echoes of earlier turns replay; the dead fight beside the living." Haunted: Ghost ×1.5, sound ×1.3; Ghost and Normal hit each other; Fire also hits as Ghost and Will-O-Wisp never misses. Three holy moves (Sacred Sword, Dazzling Gleam, Heal Bell...) **consecrate** it: Ghost and Dark ×0.8, Fairy ×1.2, and Normal moves strike Ghosts super effectively; two Ghost rites (Curse, Spite, Grudge, Destiny Bond...) bring the spirits back. *Tip:* Dark and Ghost hit her hard on the Haunted field. If your team is Normal or Fairy instead, consecrate it (three of Dazzling Gleam, Heal Bell or Sacred Sword), which also weakens her Ghost moves; Spiritomb's Curse is a Ghost rite and can undo it. On Hard her Mega is Gengar (Shadow Tag) instead of Sableye, and BALANCE gives the Perish Song trap to Hard only.

**K6 — Kestrel, the Hollow Cathedral** (`:HOLLOW_CATHEDRAL`; flickers to `:BLEED` for a turn)

| Pokémon | Lv | Item | Ability | Moves |
|---|---|---|---|---|
| Staraptor | 64 | Sharp Beak | Intimidate | Brave Bird, Close Combat, Double-Edge, U-turn |
| Krookodile | 64 | Life Orb | Moxie | Knock Off, Earthquake, Stone Edge, Close Combat |
| Scizor | 65 | Life Orb | Technician | Bullet Punch, U-turn, Knock Off, Swords Dance |
| Hydreigon | 65 | Choice Specs | Levitate | Draco Meteor, Dark Pulse, Flamethrower, U-turn |
| **Starter**† | 66 | Sitrus Berry | (slot 0) | (regenerated for the swapped species) |
| Aegislash "Morwen" | 66 | Spell Tag | Stance Change | King's Shield, Shadow Ball, Sacred Sword, Shadow Sneak |

*Bag: Full Restore, Full Restore; IV 28.*

- **Hard:** Staraptor 65 @Choice Band, Krookodile 65 @Life Orb, Scizor 66 @Life Orb, Hydreigon 66 @Choice Specs, Starter 67 @Life Orb, Aegislash 67 @Weakness Policy
- **Casual:** Staraptor 60 @Sitrus Berry, Scizor 61 @Metal Coat, Hydreigon 61 @Sitrus Berry, Starter 62 @Sitrus Berry, Aegislash 62 @Spell Tag

† The rival's starter is written as the Gen 1 line in PBS; Prismfall Core swaps it at battle start for the same-generation counterpart of your starter (same stage).

*Tip:* no Mega (no ring of his own). Hydreigon has replaced Zweilous; Aegislash is still the ace.

**Boss — Giratina** (Reverse Depths, `:INVERSE`) *(planned multi-bar boss, Altered then Origin; not registered in Prismfall Bosses yet).*

### Side quests

- **The Saga of the Glass Dunes** (`IS_SAGA_OF_THE_ICE`, The Tally; designed (not wired yet)). Bersi Gullsong, Skaldfast (921). Unlock: Badges ≥ 13. Bersi wants to sing the war. Truthfully, for once. He needs a witness who stood on the glass. Reward: Lapras "Saga" Lv 45 (WATERABSORB); +5 pts.
- **The Smile Behind the Glass** (`AN_SMILE_BEHIND_GLASS`, The Rite of Reflection; wired (playable)). Lector Saffi Ivarne, the Speculum, Lucent (346). Unlock: Badges ≥ 13. MIRROR-WRITING: Somebody's reflection in the Speculum is smiling with too many teeth. Reward: Mawilite; +3 pts.
- **Nine Hundred and Ninety-Nine** (`AN_GIMMIGHOUL_COINS`, The Rite of Reflection; designed (not wired yet)). a lantern-priest, Gravenmoor (380). Unlock: Badges ≥ 13. Gimmighoul coins keep turning up in the Gravenmoor collection plates. The priests want to know where they're coming from. Reward: Relic Gold; +3 pts.
- **Behind the Glass** (`AN_BEHIND_THE_GLASS`, The Rite of Reflection; designed (not wired yet)). Archseer Dask's reflection, the Palace of Glass, Lucent (347). Unlock: Badges ≥ 14 and S143 CH15_GIRATINA_DONE. Antumbra's last rite: spend one night as your own reflection. Reward: Ability Patch; +5 pts.

**Event Pokémon:**

_None this chapter._

**Mega Stones and Z-crystals:**

- **Gardevoirite** (Mega Stone, from Badge 13): The Looking-Glass Wood, the heart of the mirror maze. **puzzle**. *(planned: map not built)*
- **Mawilite** (Mega Stone, from Badge 13): The Speculum, Lucent: the smile behind the glass (Rite of Reflection rank 2). quest AN_SMILE_BEHIND_GLASS. *(planned: map not built)*
- **Scizorite** (Mega Stone, from Badge 13): Vane Hall, Gravenmoor: Morwen Vane's trophy case. item. *(planned: map not built)*
- **Abomasite** (Mega Stone, from Badge 13): The Hoarwood, under the frost-giant pine. hidden item. *(planned: map not built)*
- **Psychium Z** (Z-crystal, from Badge 13): Hindmoor, the humming standing stone. hidden. *(planned: map not built)*
- **Buginium Z** (Z-crystal, from Badge 13): The Jawbone Ridge, in a dead tree's resin. hidden. *(planned: map not built)*
- **Fairium Z** (Z-crystal, from Badge 13): Darkglass Mine B1F, under the shot-out lamps. hidden. *(planned: map not built)*
- **Mimikium Z** (Z-crystal, from Badge 13): Lantern Hospice, Gravenmoor: sewn into a Pikachu-shaped rag doll. item. *(planned: map not built)*

### Gym 14 — the Hollow Cathedral (Ysolde Ashgrave) *(design only)*

- **Puzzle (9/10, about 35 minutes): "the dead walk where you walked."** Ringing the nave bell moves you between the **Living Nave** (391) and the **Dead Nave** (392), same tile. Pews are real in both worlds: push one among the living (you can't move wood among the dead) and it bridges an open crypt in the Dead Nave.
    - **390 Narthex:** push the pew one tile over the crack; in the dead room it spans the grave.
    - **391/392 Naves:** push pews 2 and 5 into the central aisle over the crypt marks, push pew 3 *out* of the aisle, ring, and cross the dead nave on the pew bridges to the altar door. A pew in the wrong orientation blocks both worlds: ask the apprentice to reset. *(To be verified by the builder.)*
    - **393 Requiem Crypt:** ring the hand-bell to record up to 12 steps; Morwen's echo walks them and stays (and holds a plate). Record the walk through the ghost wall onto plate C, ring back to the living nave (the echo stays), push the last pew onto plate B and stand on A.
- **Badge:** Badge 14. **TM30 Shadow Ball.** **Level cap after: 71.**
- **Mastery (optional):** Morwen's Chapel (395): the echo lights six candles in the order you lit them last time; use it to light the last one while you stand at the lectern. Reward: Magical Seed ×2, Spell Tag and **Morwen's sealed letter** (the Act IV outline has Ysolde keeping that letter for Kestrel instead).
- **Gym trainers:** 6 (Channeler ×3, Gentleman, Lady, Mourner-acolyte), Lv 63–66; the ghost trainers stand only in the Dead Nave. *(Not in PBS yet.)*

---

## Chapter 16 — "Clear Air"

*The Slag Road: the Slag Mesa (801, `:WASTELAND`) and the Slagglass, the Smokestack Parade (811) into Cogsworth (400–414, Zenith's foundry district), Strade Works (403) and the Engine core chamber. Design only. Gym 15.*

### Key events

- **The Arbiter blueprints and Zekrom freed.** In Strade Works' drafting vault: a ring of eighteen locks built *into the new Festival arena*, a keystone cradle "to be recovered from site AURELIA", and **"Calibration subject: UNIMPRINTED-01. Retention: indefinite."** In the core chamber the Dark Stone has cracked open around a half-emerged **Zekrom** in golden cable.
- **The Sump Purge begins, and Wenlow dies** (Interlude IV): "Operation Clear Air" sends the Directorate down into Nadir.

### Order of events

1. **Cogsworth** runs three shifts under Directorate banners; "Unity Rallies" in the plazas ("Order. Light. Unity."). Nadir workers commute up the lifts to build something they can't name.
2. **Rook** in a workers' canteen, off camera and unshaven: "I've got Sable on tape. With a Meridian keycard. I've had it for months. I was scared." Comedy scene "Off Camera" (before the infiltration). ⚑ **`:ch16_rook`**: *leak it now* (Kroll exposed realm-wide even without Ch13 evidence; Rook is fired and blacklisted, so he can't cut the grid in Ch21 or release the Zap Plate unless Marchetti turns) / *hold it for the Festival* (he leaks it at the Ch20 opening ceremony and stays in position: `ROOK_CUTS_GRID`).
3. **Gym 15, Strade Works:** **Magnus Strade** (prosthetic hand, pocket watch): "Faith gave us three hundred years of the Bleed. Engineering will give us the next three hundred without it." Badge 15, **TM91 Flash Cannon**; **Dive** suits from the bathysphere works.
4. **Infiltration** with Rook's keycards: **partner battle, you + Rook vs Marchetti + Quent** on the casting floor (`:FACTORY` → `:SCRAPYARD` as the floor is wrecked). Key item **Arbiter Blueprints** (above).
5. **The core chamber:** **boss: Zekrom.** Each bar snaps a containment cable: you are freeing it, not beating it. It tears out through the foundry roof into the Stormfront (`ZEKROM_FREED`): the Engine's original core is lost, and Voss must reroute through Lumen's grid. ☠ **`GO_OVERTIME` "Overtime"**: stay to "finish copying the blueprints" while the klaxon counts down from 3 (Rook warns you twice: "We go when the whistle goes, no heroics").
6. **Magnus** finds you in the vault and doesn't call security: "I don't build weapons. I build tolerances." ⚑ **`:ch16_magnus`**: *expose him* to the Zenith Council through Councillor Sallow (`MAGNUS_EXPOSED`: a board vote lost, the design leaks, but nobody is left inside) / *appeal to his conscience*, "Will you let it take a child?" (`MAGNUS_KEPT_FAITH`: in the finale he disables the Engine's safety governor: "No machine I have built will kill a child.").
7. **The Sump Purge:** every screen shows "Operation Clear Air". A worker beside you: "My mum lives down there."
8. **Interlude IV, "Clear Air"** (play as **Wenlow**, Corvin's apprentice): the Directorate comes up Mirefen's stilt-walks; move patients, hide the Sweetrot addicts among the glass patients ("Nobody ever looks at the glass ones."), and fight two officers with Corvin's spare Pokémon. The last scene ends on a single gunshot. **This death cannot be prevented.**
9. **Cliffhanger:** dawn, you, Rook and the blueprints on a supply-lift down into Nadir; smoke rises from Underveil.
10. *Optional, from 15 badges until the Festival:* **Brann's forge** (Cindervault's Hearthguild anvil, 244; most players find him on the way to Wyrmrest in Ch19): he knows his ring on your hand, says so if you told him the Light Stone was the Dominar's, and gives the **Cameruptite** (hidden Trials quest `AS_FORGE_REMEMBERS`).

### Areas *(design only; maps not built)*

| Map (ID) | Field | Built? | Wild Pokémon (from `pbs/encounters.txt`) |
|---|---|---|---|
| The Slag Mesa (801) | Wasteland (`:WASTELAND`) | no | Grass: Muk 65–69, Weezing 65–69, Garbodor 65–69, Magneton 65–69, Klang 65–69, Sandaconda 65–69, Hippowdon 65–69, Krookodile 65–69, Galarian Meowth 65–69, Copperajah 65–69, Durant 65–69, Ferrothorn 65–69, Galarian Stunfisk 65–69, Revavroom 65–69, Excadrill 65–69 |
| The Smokestack Parade (811) | Factory (`:FACTORY`) | no | _no wild table yet_ |
| Cogsworth (400) | Factory (`:FACTORY`) | no | Surf: Tentacruel 63–69, Pelipper 63–69, Sharpedo 63–69, Wailord 63–69, Mantine 63–69; Old Rod: Magikarp 35–45, Remoraid 35–45; Good Rod: Remoraid 60–68, Octillery 60–68, Kingler 60–68, Clawitzer 60–68 |
| Strade Works - Foundry Floor (403) | Factory (`:FACTORY`) | no | _no wild table yet_ |

### Key battles

**Gym 15 — Warden Magnus Strade** (Steel, `:FACTORY`, single battle, cap 71)

| Pokémon | Lv | Item | Ability | Moves |
|---|---|---|---|---|
| Ferrothorn | 69 | Rocky Helmet | Iron Barbs | Stealth Rock, Leech Seed, Power Whip, Gyro Ball |
| Excadrill | 69 | Life Orb | Mold Breaker | Drill Run, Iron Head, Rock Slide, Swords Dance |
| Kingambit | 70 | Black Glasses | Defiant | Kowtow Cleave, Iron Head, Sucker Punch, Swords Dance |
| Klinklang "Mark One" | 70 | Sitrus Berry | Clear Body | Shift Gear, Gear Grind, Wild Charge, Magnet Rise |
| Scizor | 70 | Metal Coat | Technician | Bullet Punch, U-turn, Knock Off, Swords Dance |
| Metagross "Engine" | 71 | Metagrossite | Clear Body | Meteor Mash, Zen Headbutt, Hammer Arm, Bullet Punch |

*Bag: Mega Ring, Full Restore, Full Restore; IV 28.*

- **Hard:** Ferrothorn 70 @Rocky Helmet, Excadrill 70 @Focus Sash, Kingambit 71 @Leftovers, Klinklang 71 @Sitrus Berry, Scizor 71 @Life Orb, Metagross 71 @Metagrossite
- **Casual:** Ferrothorn 64 @Rocky Helmet, Kingambit 65 @Black Glasses, Klinklang 65 @Sitrus Berry, Scizor 65 @Metal Coat, Metagross 66 @Metagrossite

*Field note:* "conveyor-belt arena; machines you can jam or overdrive." Steel ×1.5, Electric and Fire ×1.2; Fire may soften a Steel target's plating (30%, Def −1); indoor weather can't start except sun. An explosion, or three quakes, wreck it into a **Scrapyard** (rust makes Water super effective on Steel; three charging moves restart the line). **Mega Metagross "Engine"**: the foundry hammers its plating home (+1 Def). *Tip:* Fire (Ferrothorn and Scizor take it ×4) and Ground; three Earthquakes wreck the floor into a Scrapyard, where rust makes Water super effective against his Steel types and takes away his ×1.5.

**You + Rook vs Marchetti and Quent** (tag double, casting floor, `:FACTORY` → `:SCRAPYARD`; Rook's partner team isn't in PBS yet)

| Pokémon | Lv | Item | Ability | Moves |
|---|---|---|---|---|
| Houndoom | 69 | Houndoominite | Flash Fire | Dark Pulse, Flamethrower, Sludge Bomb, Protect |
| Corviknight | 70 | Leftovers | Mirror Armor | Brave Bird, Iron Head, Tailwind, Roost |
| Mabosstiff | 71 | Sitrus Berry | Intimidate | Crunch, Play Rough, Wild Charge, Protect |

*Bag: Mega Ring, Full Restore, Full Restore; IV 28.*

- **Hard:** Houndoom 70 @Houndoominite, Corviknight 71 @Leftovers, Mabosstiff 71 @Sitrus Berry
- **Casual:** Houndoom 64 @Houndoominite, Corviknight 65 @Leftovers, Mabosstiff 66 @Sitrus Berry

| Pokémon | Lv | Item | Ability | Moves |
|---|---|---|---|---|
| Bronzong | 69 | Sitrus Berry | Heatproof | Gyro Ball, Trick Room, Protect, Explosion |
| Magnezone | 70 | Sitrus Berry | Magnet Pull | Thunderbolt, Flash Cannon, Protect, Volt Switch |
| Porygon-Z | 71 | Life Orb | Download | Tri Attack, Discharge, Ice Beam, Protect |

*Bag: Full Restore, Full Restore; IV 28.*

- **Hard:** Bronzong 70 @Sitrus Berry, Magnezone 71 @Sitrus Berry, Porygon-Z 71 @Life Orb
- **Casual:** Bronzong 64 @Sitrus Berry, Magnezone 65 @Sitrus Berry, Porygon-Z 66 @Sitrus Berry

*Tip:* Mega Houndoom is the pair's one Mega. Quent's Bronzong may Explode and wreck the floor; three of Porygon-Z's Discharges restart the line.

**Boss — Zekrom** (`ZEKROM_ENGINE`, Prismfall Bosses, on `:FACTORY`)

- Lv 72; bars Casual 2 / Standard 3 / Hard 4. Opens with Hone Claws.
- Each break "snaps a containment cable" and gives Atk +1; break 2 wrecks the floor (`:FACTORY` → `:SCRAPYARD`) and it learns Bolt Strike.
- Last bar: it **breaks free** (result `:freed`), no faint and no catch.
- *Tip:* Ground, Ice, Dragon and Fairy; on the Scrapyard its Electric moves may paralyse your Steel types.

### Side quests

- **The Doll Who Waited** (`EL_DOLL_WHO_WAITED`, The Quiet Way; wired (playable)). A doll in the attic, Thistledown Manor attic (547). Unlock: Badges ≥ 14. A lantern with a child's scrawl: 'SOMETHING KNOCKS IN THE THISTLEDOWN ATTIC. IT WANTS ITS BUTTONS.'. Reward: Banettite, Ghostium Z; +2 pts.
- **Return to Sender** (`ZE_RETURN_TO_SENDER`, The Prize Exchange; wired (playable)). Postmaster Halloran, Gale Post Hall, Skyreach (325). Unlock: Badges ≥ 14. CALL FOR PROPOSALS #0412: DEAD LETTERS, THREE (3). DELIVER BY HAND. PRIZE: ONE (1) DRAWER, CLEARED. Reward: Pidgeotite, Electrium Z; +2 pts.
- **The Laureate's Prize** (`ZE_LAUREATE`, The Prize Exchange; designed (not wired yet)). Registrar Odalys Venn, the Prize Exchange, Lumen City (194). Unlock: Badges ≥ 14. The Exchange's highest prize: enter a machine of your own design in the Cogsworth Invention Bout. Your machine is your team. Reward: Ability Patch; +5 pts.
- **The Lift Strike** (`NA_LIFT_STRIKE`, The Gutter Book; designed (not wired yet)). the lift-workers' union, Midstair (830). Unlock: Badges ≥ 14. The cable-lift workers have stopped every lift between Zenith and Nadir. The Directorate wants them moving by morning. Reward: $6000; +4 pts.

**Event Pokémon:**

_None this chapter._

**Mega Stones and Z-crystals:**

- **Cameruptite** (Mega Stone): Brann, the Hearthguild anvil in Cindervault (`AS_FORGE_REMEMBERS`, from 15 badges).

- **Absolite** (Mega Stone, from Badge 14): The Slag Mesa, under the warning-cairn on the mesa's lip. hidden item. *(planned: map not built)*
- **Sablenite** (Mega Stone, from Badge 14): Barrow of the Wardens, a looted grave-niche the Sableye mine for its gems. hidden item. *(planned: map not built)*
- **Banettite** (Mega Stone, from Badge 14): Thistledown Manor attic: the doll who waited. quest EL_DOLL_WHO_WAITED.
- **Pidgeotite** (Mega Stone, from Badge 14): Gale Post Hall, Skyreach: the dead-letter bag. quest ZE_RETURN_TO_SENDER. *(planned: map not built)*
- **Metagrossite** (Mega Stone, from Badge 14): Strade Works Foundry Floor, the sorting-line puzzle. **puzzle**. *(planned: map not built)*
- **Gengarite** (Mega Stone, from Badge 14): Barrow Sanctum, the altar of the nameless Warden. item. *(planned: map not built)*
- **Poisonium Z** (Z-crystal, from Badge 14): The Smokestack Parade, a soot-black vent. hidden. *(planned: map not built)*
- **Ghostium Z** (Z-crystal, from Badge 14): Thistledown Manor attic: the doll who waited. quest EL_DOLL_WHO_WAITED (with the Banettite).
- **Electrium Z** (Z-crystal, from Badge 14): Gale Post Hall, Skyreach: the dead-letter drawer. quest ZE_RETURN_TO_SENDER (with the Pidgeotite). *(planned: map not built)*

### Gym 15 — Strade Works (Magnus Strade) *(design only)*

- **Puzzle (9/10, about 35 minutes): "tolerances."** One clock ticks when you step (or punch a time-clock to spend a tick standing still). Belts move whatever stands on them a tile per tick; presses slam on their beat (being under one = "Line stop!", back to the room start); lever groups reverse sets of belts; a crate under a press when it slams **jams it open for good**.
    - **410 Gatehouse:** ride the belt and punch the clock once so the beat-2 press lifts before you arrive.
    - **411 Assembly Line:** belt 3 is in two lever groups. Pull **A, then B** (belt 3 forward, belts 1 and 2 backward), ride belt 2 to the C platform, pull **C**, then punch the clock twice before the beat-3 press on belt 5. *(To be verified by the builder.)*
    - **412 Crane Bay:** you don't beat the machine, you *feed* it. Drop crate 1 on lane 2 two tiles upstream of press P2 so it arrives on P2's beat and jams it; reverse lane 3 with lever C and drop crate 2 for P4; time P1 and P3 with the clock. A crate a tick late is scrap ("Tolerance exceeded.").
- **Badge:** Badge 15. **TM91 Flash Cannon.** **Level cap after: 75.** **Field move:** Dive (HM06, the bathysphere works; 15 badges).
- **Mastery (optional):** the Tolerance Lab (414): three crates into three bays on the same tick, belts of 5, 7 and 8. Reward: Synthetic Seed ×2, Metal Coat and Magnus's tolerance gauge ("±0. No exceptions.").
- **Gym trainers:** 6 (Engineer ×2, Worker ×2, Scientist, Meridian Foreman), Lv 67–70. *(Not in PBS yet.)* GYM_PUZZLES also puts a partner battle with Magnus's apprentice just before the gym; the Act IV outline has none (its partner battle is the one with Rook, after the gym).

---

## Chapter 17 — "The Drowned Crown"

*The Drowned Road: the Brink (832) on the plateau's south-east rim, the Hanging Stair (820, `:SCRAPYARD`), the Drownings (821, the drained south coast) and Under the Drownings (822, Dive), to Underveil (420–433, Nadir's heart in drowned Aurelia's towers) with the Moon Market (423), Midstair (830), and Aurelia below: the Drowned Spires (824, `:UNDERWATER`), the Air Halls (825) and the Gilded Throne Vault with the Sun Court (826). Optional: Ironbloom (828, `:BLEED`); branch map: the Accord Archive (838, high Accord Standing). Design only. Gym 16.*

### Key events

- **Aurelia.** The Sun Court murals tell the real Prismfall (the Blight, the Two Weathers, the Chain, the Calling, the god breaking itself, the city falling, Princess Maren pulling a colourless shard from the cradle's wreck). At the keystone cradle your chest glows with eighteen colours. Nyx: **"Oh. Oh, darling. You're the missing piece."** Sahar reads: *"Here rests the One that is every color and none."* You carry a splinter of the Legend Plate.
- **Voss names himself.** House Aurel: "We changed the name and kept the grudge." He admits AF 290 ("My array. My dials."), calls the Lowlight's twelve dead *meaningful*, and makes his offer (⚑ `:ch17_voss_offer`).

### Order of events

1. **The Brink**, **the Hanging Stair** and **the Drownings** down to Underveil the morning after the Purge: smoke, broken lanterns, Directorate barricades, dozens dead; Mother Gutter's Muk holds one barricade. ☠ **`GO_INTO_THE_LINE` "Into the Line"**: step between the advancing Directorate line and the unarmed protestors (Nyx's courier warns you twice: "You're the one thing they want alive.").
2. **Nyx Calloway** in the Moon Market, who has been carrying bodies: "Underveil isn't on the Accord's maps, sweetheart. That's the point of Underveil." That afternoon **Nadir declares independence** from the Moon Market steps (legally meaningless; everyone cheers). Comedy scene "The Price" (before the gym).
3. **Gym 16, the Hall of Whispers:** Nyx, an illusion double battle. Badge 16, **TM79 Dark Pulse**. Afterwards, unprompted: "Two years ago I sold Voss the way into the Sun Court. ... I'm the one who opened it."
4. ⚑ **`:ch17_nyx`**: she has the Engine's arena schematics. *Trade your own secret* (`NYX_BARGAIN_TAKEN`: in Ch21 she cuts Meridian's comms precisely) / *refuse* (she helps anyway, sloppily, and is injured).
5. *Branch (high Accord Standing):* **the Accord Archive** (838), a sealed Coastwatch vault on the Drownings: the Concordance's Secret Articles in Maren's hand (the Tuning, the Hymn of Return). Brann confesses here, early and gently, and gives you Maren's original Hymn page.
6. **The dive into Aurelia** (Dive): Sahar leads ("Three hundred years. I've waited my whole *life*."), Edda pilots the support boat. Golden terraces under green water, Gilder machines in coral, the Gilded King's statues with their faces chiselled off.
7. **The Sun Court** (above). ☠ **`GO_THE_THRONE` "The Throne"**: sit on the Gilded King's throne (Sahar: "Don't touch anything gold. *Anything*."; the armrests are open hands).
8. **Voss in the Sun Court**, helmet off in an air pocket, come for the cradle: "Gods are absentee landlords. ... I'm trying to make sure we never need one again." ⚑ **`:ch17_voss_offer`**: *refuse* / *feign agreement* (`VOSS_FEIGNED`: he lets you close in the finale; risky with high Meridian Standing and live telemetry) / *accept* (`VOSS_ACCEPTED`: opens the Concord Dawn ending path).
9. **Admin battle: Kroll** holds the Sun Court (`:CAVE`), or **Quent** if Kroll was beaten publicly in Ch13, while Voss's team lifts the cradle out through the wall. He leaves by submarine: "Win your badges. I'll see you at the coronation."
10. **Ysolde in Underveil** lights a Gravenmoor lantern for each of the Purge's dead: "Is he eating? Kestrel. You'd know better than I would."
11. **Brann's confession** at the Underveil docks (if not given in the Archive): the Tuning is real; the Crown kills Sovereigns; he reset the Crown's stone after the Fracture, knew it was short and never asked where the rest went; Valen's arm is crystal to the shoulder: "He has weeks. Maybe the Festival." Valen's message: "Win your last two badges. Then come to me, and I'll tell you everything."
12. **Cliffhanger** on the docks: Nyx counts on her fingers every power that wants you in that arena. "Thirty days, sweetheart." Edda: "Then we'd best make sure you walk in on your own feet." **END OF ACT IV.**

### Areas *(design only; maps not built)*

| Map (ID) | Field | Built? | Wild Pokémon (from `pbs/encounters.txt`) |
|---|---|---|---|
| The Brink (832) | Stormfront (`:STORMFRONT`) | no | _no wild table yet_ |
| The Hanging Stair (820) | Scrapyard (`:SCRAPYARD`) | no | Grass: Magneton 67–71, Klinklang 67–71, Klang 67–71, Metang 67–71, Scrafty 67–71, Muk 67–71, Bronzong 67–71, Bisharp 67–71, Excadrill 67–71, Copperajah 67–71, Perrserker 67–71, Duraludon 67–71, Toxicroak 67–71, Garbodor 67–71, Skarmory 67–71, Skuntank 67–71, Scizor 67–71 |
| The Drownings (821) | Water Surface (`:WATER_SURFACE`) | no | Grass: Skuntank 68–72, Kilowattrel 68–72, Pelipper 68–72, Cramorant 68–72, Wugtrio 68–72, Scrafty 68–72, Honchkrow 68–72, Alolan Muk 68–72, Corviknight 68–72, Pincurchin 68–72; Surf: Tentacruel 68–72, Pelipper 68–72, Wailord 68–72, Sharpedo 68–72, Mantine 68–72, Barraskewda 68–72, Drednaw 68–72, Jellicent 68–72, Staryu 68–72, Dragalge 68–72, Seadra 68–72, Wishiwashi 68–72, Lapras 68–72; Old Rod: Magikarp 40–50, Finneon 40–50; Good Rod: Lumineon 65–72, Seadra 65–72, Kingler 65–72, Clawitzer 65–72 |
| Under the Drownings (822) | Underwater (`:UNDERWATER`) | no | Grass: Lanturn 68–73, Lumineon 68–73, Relicanth 68–73, Dhelmise 68–73, Mantine 68–73, Octillery 68–73, Huntail 68–73, Gorebyss 68–73, Cursola 68–73, Corsola 68–73, Alomomola 68–73, Bruxish 68–73, Pyukumuku 68–73, Jellicent 68–73, Kingdra 70–73 |
| Underveil - Lantern Tiers (420) | New Moon (`:NEW_MOON`) | no | _no wild table yet_ |
| Underveil - Moon Market (423) | New Moon (`:NEW_MOON`) | no | _no wild table yet_ |
| Underveil - Sump Docks (424) | Corrosive Mire (`:CORROSIVE_MIRE`) | no | _no wild table yet_ |
| Underveil - Barons' Stair (425) | New Moon (`:NEW_MOON`) | no | _no wild table yet_ |
| Underveil - Bell Tower of Aurel (426) | Hollow Cathedral (`:HOLLOW_CATHEDRAL`) | no | _no wild table yet_ |
| Drowned Cathedral of Aurel (429) | Hollow Cathedral (`:HOLLOW_CATHEDRAL`) | no | _no wild table yet_ |
| Midstair (830) | Scrapyard (`:SCRAPYARD`) | no | _no wild table yet_ |
| Aurelia - Drowned Spires (824) | Underwater (`:UNDERWATER`) | no | Grass: Relicanth 69–73, Dhelmise 69–73, Jellicent 69–73, Lanturn 69–73, Clawitzer 69–73, Omastar 69–73, Kabutops 69–73, Carracosta 69–73, Gorebyss 69–73, Huntail 69–73, Mantine 69–73, Bruxish 69–73, Barbaracle 69–73, Dracovish 69–73, Arctovish 69–73 |
| Aurelia - Air Halls (825) | Cave (`:CAVE`) | no | Cave: Crawdaunt 70–74, Toxapex 70–74, Skuntank 70–74, Drapion 70–74, Scrafty 70–74, Toxicroak 70–74, Bisharp 70–74, Golbat 70–74, Clawitzer 70–74, Barbaracle 70–74, Quagsire 70–74, Seismitoad 70–74, Alolan Muk 70–74, Honchkrow 70–74 |
| Aurelia - Gilded Throne Vault (826) | Cave (`:CAVE`) | no | Cave: Golurk 71–74, Bronzong 71–74, Claydol 71–74, Sigilyph 71–74, Cofagrigus 71–74, Carbink 71–74, Klefki 71–74, Runerigus 71–74, Doublade 71–74, Metang 71–74, Duraludon 71–74, Aegislash 71–74, Gigalith 71–74, Stonjourner 71–74 |
| Ironbloom (828) | The Bleed (`:BLEED`) | no | Grass: Ferrothorn 71–74, Klefki 71–74, Ferroseed 71–74, Aggron 71–74, Steelix 71–74, Scizor 71–74, Metang 71–74, Corviknight 71–74, Skarmory 71–74, Excadrill 71–74, Duraludon 71–74, Bisharp 71–74, Mawile 71–74, Copperajah 71–74, Magnezone 71–74, Aegislash 71–74, Metagross 72–74 |
| Accord Archive (838) | Mindscape (`:MINDSCAPE`) | no | _no wild table yet_ |

### Key battles

**Gym 16 — Warden Nyx Calloway** (Dark, `:NEW_MOON`, **double battle**, cap 75)

| Pokémon | Lv | Item | Ability | Moves |
|---|---|---|---|---|
| Grimmsnarl | 73 | Light Clay | Prankster | Reflect, Light Screen, Spirit Break, Fake Out |
| Weavile | 73 | Magical Seed | Pressure | Fake Out, Night Slash, Knock Off, Ice Shard |
| Absol "Omen" | 74 | Absolite | Super Luck | Night Slash, Sucker Punch, Play Rough, Protect |
| Umbreon | 74 | Leftovers | Inner Focus | Foul Play, Snarl, Helping Hand, Wish |
| Zoroark "Nobody" | 75 | Life Orb | Illusion | Night Daze, Flamethrower, Sludge Bomb, Nasty Plot |
| Honchkrow | 74 | Sitrus Berry | Super Luck | Night Slash, Brave Bird, Sucker Punch, Heat Wave |

*Bag: Mega Ring, Full Restore, Full Restore; IV 31.*

- **Hard:** Grimmsnarl 74 @Light Clay, Weavile 74 @Magical Seed, Absol 75 @Absolite, Umbreon 75 @Leftovers, Zoroark 75 @Choice Specs, Honchkrow 75 @Life Orb
- **Casual:** Grimmsnarl 68 @Light Clay, Weavile 68 @Sitrus Berry, Absol 69 @Absolite, Umbreon 69 @Leftovers, Zoroark 70 @Sitrus Berry

*Field note:* "nothing on the field is what it looks like; illusions mask both sides." Dark ×1.5, shadow moves ×1.2; non-Dark/Ghost moves are ×0.9 accurate; Swift ×1.5 and light moves ×1.3 pierce it; Moonblast is ×0.75. Three Dark Pulses (or Dark Void) deepen it to the **Abyss**; three light moves relight Nadir's gaslamps (**Lamplight**: normal accuracy, Fire and Electric ×1.2). **Mega Absol "Omen"** (Magic Bounce guards the Illusion games). *Tip:* Fighting, Bug and Fairy (but not Moonblast); three Dazzling Gleams or Flash Cannons give you Lamplight. Zoroark's Illusion can hide as any of her team.

**Sabine Kroll, the Sun Court** (`MERIDIAN_KROLL` v1, `:CAVE`), or **Dr Quent** (v2) if Kroll was beaten publicly in Ch13

| Pokémon | Lv | Item | Ability | Moves |
|---|---|---|---|---|
| Sharpedo | 73 | Sharpedonite | Speed Boost | Crunch, Liquidation, Ice Fang, Protect |
| Toxicroak | 73 | Life Orb | Dry Skin | Drain Punch, Gunk Shot, Sucker Punch, Earthquake |
| Honchkrow | 74 | Scope Lens | Super Luck | Night Slash, Brave Bird, Sucker Punch, Roost |
| Obstagoon | 74 | Flame Orb | Guts | Obstruct, Knock Off, Facade, Close Combat |
| Drapion | 75 | Scope Lens | Battle Armor | Knock Off, Cross Poison, Earthquake, Rock Slide |

*Bag: Mega Ring, Full Restore, Full Restore; IV 31.*

- **Hard:** Sharpedo 74 @Sharpedonite, Toxicroak 74 @Life Orb, Honchkrow 75 @Scope Lens, Obstagoon 75 @Flame Orb, Kingambit 74 @Black Glasses, Drapion 75 @Scope Lens
- **Casual:** Sharpedo 68 @Sharpedonite, Honchkrow 69 @Scope Lens, Obstagoon 69 @Sitrus Berry, Drapion 70 @Scope Lens

- **Quent instead:** Bronzong 73 @Leftovers, Magnezone 73 @Air Balloon, Metagross 74 @Metagrossite, Porygon-Z 75 @Life Orb.
- *Field note:* Cave: Rock ×1.5 and sound ×1.5; the low ceiling halves non-contact Flying moves and lets Ground hit fliers (Honchkrow). Kroll's play (the Hammer's) is the cave-in: one quake cracks the ceiling and the next brings it down on everyone (1/8, Rock-type; Rock Head, Bulletproof and Overcoat are safe). Two Power Gems turn it into a Crystal Cavern.

### Side quests

- **Dogs of the Moon Market** (`NA_MOON_MARKET_DOGS`, The Gutter Book; wired (playable)). Six-Fingers Ottoline, the Moon Market, Underveil (423). Unlock: Badges ≥ 15. CHALK: BARONS' KENNEL. THREE CAGES. NOBODY SAW NOTHING. Reward: Houndoominite, Darkinium Z; +3 pts.
- **Mother Gutter's Ledger** (`NA_GUTTER_DEBTS`, The Gutter Book; designed (not wired yet)). Mother Gutter, the Moon Market, Underveil (423). Unlock: Badges ≥ 15. Collect five debts for the oldest sump-baron in Nadir. Or don't collect them. She'll know either way. Reward: $8000; +4 pts.
- **The Forge Remembers** (`AS_FORGE_REMEMBERS`, The Trial by Flames; wired (playable)). Brann Holloway, the Hearthguild Hall, Cindervault (after the Ring) (244). Unlock: Badges ≥ 15 and quest_done(:OS_RING_DAY); after OS_RING_DAY. Brann found something in the slag. Reward: Cameruptite; +0 pts.
- **Old Cinder** (`AS_OLD_CINDER`, The Trial by Flames; wired (playable)). Roost-keeper Tarn, Pyre Keep, the Dragon Roosts (248). Unlock: Badges ≥ 15. WRIT: The war-Charizard Old Cinder will not leave the high roost. Its rider fell at the front. Bring it down, honourably. Reward: Charizardite X, Dragonium Z; +3 pts.
- **The Brazier Writ** (`AS_BRAZIER_WRIT`, The Trial by Flames; wired (playable)). Legate Varra Kosk, the Crucible, Cindervault (240). Unlock: Badges ≥ 15. WRIT OF THE BRAZIER: the Crucible keeps one heartstone for one who earns it without being born to a dragon. Reward: Salamencite, Firium Z; +4 pts.
- **The Tyrant's Heart** (`OS_TYRANT_HEART`, The Rolls of Unearthing; wired (playable)). Curator-Elect Nasrin Vael, the Cragholm lift-house rack; the dig is on the Vertebrae (360). Unlock: Badges ≥ 15. TABLET: A tyrant's heart lies in the third vertebra. Dig it out whole. Reward: Tyranitarite, Groundium Z; +4 pts.
- **Deliverer** (cameo, Amaria and Titania; CAMEOS §6): after Gym 16, Edda's divers report a woman swimming without a suit in Aurelia's lower galleries, singing to a Lapras, and a knight pacing the drained shallows. Dive a short maze to Amaria in a flooded Gilder hall ("it isn't dead, it's *waiting*": a Ruin Route hint). **Double battle** on `:WATER_SURFACE`: Ludicolo 76 @Life Orb, Milotic 76 @Leftovers, Kingdra 77 @Damp Rock, Lapras 78 @Leftovers and Corviknight 76 @Leftovers, Mawile 76 @Life Orb, Kingambit 77 @Black Glasses, Aegislash 78 @Weakness Policy. Reward: a Liquidation TM, an Assault Vest and a Lapras of your own (Deliverer's calf).

**Event Pokémon:**

- **Charizard "Old Cinder" Lv 72 (SOLARPOWER)**: boss battle (guards a reward; doesn't join), Pyre Keep, the Dragon Roosts (high roost). Climb to the high roost and fight the grieving war-Charizard.

**Mega Stones and Z-crystals:**

- **Sharpedonite** (Mega Stone, from Badge 15): Underveil Sump Docks, a harpooned Sharpedo jaw in the net-loft. hidden item. *(planned: map not built)*
- **Swampertite** (Mega Stone, from Badge 15): The Drownings, a mud-bank islet (Surf). hidden item. *(planned: map not built)*
- **Charizardite Y** (Mega Stone, from Badge 15): The Brink, the wind-scoured ledge above the drop. hidden item. *(planned: map not built)*
- **Cameruptite** (Mega Stone, from Badge 15): Hearthguild Hall, Cindervault: Brann's spare. quest AS_FORGE_REMEMBERS. *(planned: map not built)*
- **Charizardite X** (Mega Stone, from Badge 15): Pyre Keep Dragon Roosts: Old Cinder, a retired Legion war-Charizard. **boss** AS_OLD_CINDER. *(planned: map not built)*
- **Gyaradosite** (Mega Stone, from Badge 15): Aurelia - Drowned Spires, the flooded bell (Dive). hidden item. *(planned: map not built)*
- **Houndoominite** (Mega Stone, from Badge 15): Underveil Moon Market: the Barons' kennel (Gutter Book). quest NA_MOON_MARKET_DOGS. *(planned: map not built)*
- **Tyranitarite** (Mega Stone, from Badge 15): Cragholm rack: the tyrant's heart (Rolls of Unearthing rank 2). quest OS_TYRANT_HEART. *(planned: map not built)*
- **Garchompite** (Mega Stone, from Badge 15): The Dry Tide, a sand-sunk caravan. hidden item. *(planned: map not built)*
- **Salamencite** (Mega Stone, from Badge 15): The Crucible, Cindervault: the brazier writ (Trial by Flames rank 2). quest AS_BRAZIER_WRIT. *(planned: map not built)*
- **Firium Z** (Z-crystal, from Badge 15): The Crucible: the brazier's own sliver. quest AS_BRAZIER_WRIT (with the Salamencite). *(planned: map not built)*
- **Groundium Z** (Z-crystal, from Badge 15): Cragholm rack, the tyrant's heart dig. quest OS_TYRANT_HEART (with the Tyranitarite). *(planned: map not built)*
- **Darkinium Z** (Z-crystal, from Badge 15): Underveil Moon Market, the Barons' kennel. quest NA_MOON_MARKET_DOGS (with the Houndoominite). *(planned: map not built)*
- **Dragonium Z** (Z-crystal, from Badge 15): Pyre Keep: sewn into Old Cinder's harness. **boss** AS_OLD_CINDER (with the Charizardite X). *(planned: map not built)*
- **Waterium Z** (Z-crystal, from Badge 15): Under the Drownings, a drowned shrine (Dive). hidden. *(planned: map not built)*

### Gym 16 — the Hall of Whispers (Nyx Calloway) *(design only)*

- **Puzzle (9/10, about 40 minutes): "information is the key."** Guards walk fixed, step-driven patrols and see 3 tiles in the dark, 5 in lamplight (caught = back to the room start). A guard who sees a shuttered lantern open **turns to face it**.
    - **430 Vestibule:** open the lantern; the guard turns to look and you slip past behind him.
    - **431 Gallery of Shadows:** open lantern 2 to turn guard 1 north; wait in the alcove (guards never look into alcoves) for guard 2's loop to reach its far end; open lantern 4 at the exit to turn guard 3 away from you; close lantern 2 behind you. *(To be verified by the builder.)*
    - **432 The Vault** ("knowledge moves the walls"): taking or returning a dossier toggles two doors (A: d1 and d5; B: d1 and d2; C: d4 and d5). **12 actions:** d1 → R1, d5 → R3, d3 → R2, **take B**, d3 → R3, d5 → R1, **take A**, d1 → H, d2 → R2, d3 → R3, **take C**, d4 → X. Taking A first seals you in: put it back.
- **Badge:** Badge 16. **TM79 Dark Pulse.** **Level cap after: 80.**
- **Mastery (optional):** the Ledger (434): past two guards, sell one dossier back to Nyx; each opens a different strongbox (TMs, seeds, or the Gilded Chain bill of sale). Reward: Magical Seed ×2, Black Glasses and the box's extra.
- **Gym trainers:** 6 (Burglar ×2, Gambler, Rocker, Hollow Defector, Informant), Lv 71–74. *(Not in PBS yet.)*

### Aurelia (Dive) *(design only; DUNGEON_PUZZLES 9/10, about 40 minutes)*

- **Breath:** 30 steps underwater; at 0 you surface where you dived. Sunken air bells refill it.
- **824 Drowned Spires:** the route to the Air Halls is 41 steps; ring the west bell's rope to tip its air to the middle spire and split the swim 20 + 21.
- **825 Air Halls:** each floodgate you open drains a hall into 824 (a new air pocket appears there) and opens a dry path; alternate drain, dive, surface three times to reach the vault.
- **826 Gilded Throne Vault:** the three alcoves need light at once, but floodgate 2 floods alcove 3's stair. Open gates 1 and 3, walk up alcove 3's stair, then open gate 2 from inside the alcove. Nyx's hints.

# Act V — Sovereign

*Design only (outline: `story/08_ACT_V.md`; the Festival draw and endings: `story/10_CHOICES_ENDINGS.md` and `design/NARRATIVE_KEYS.md`; the war: `14_WAR_AND_BLESSING.md`). The only built Act V maps are the Ch19 war theatre (920, 924–926, 928–930), with its soldiers, partner battle and legendary boss event wired. Every Festival team is in `pbs/trainers.txt`; Crownhaven is not built.*

## Chapter 18 — "Once Upon a Time"

*The Blind Road out of Underveil: the Throat (852, `:NEW_MOON`), the Blindwater (840, `:CAVE`), the Lightless Deep (844 `:DARK_CRYSTAL` / 845 `:NEW_MOON`), the Inverted Ward (848, `:INVERSE`), Mothwell (850), the Gloamwood Verge (841) to Gloaming (440–455, Elowen's twilight corner) and the Great Tree Roots (443). Design only. Gym 17.*

### Key events

- **Pecharunt** in the Lightless Deep: the source of Sweetrot. Beating it frees the thralls across Nadir, and the old story turns over: Pecharunt enthralled the **Loyal Three** centuries ago and sent them to steal Elowen's Plates, and the "Gossamer Ogre" drove them off.
- **The Hymn of Return and K7.** Celestine has the choir sing you the whole Hymn ("It says *walker*."), then Kestrel begs you to stay out of Crownhaven (⚑ `:ch18_kestrel_ring`; ☠ `GO_STAY_OUT`).

### Order of events

1. **Down, not up:** below the drained Sump into **the Lightless Deep**, following Corvin's trace of Sweetrot (or Wenlow's notes if Corvin was never freed): pink crystal, smiling thralls tending peach-shaped growths, and **Mother Gutter**, the first thrall.
2. **Boss: Pecharunt** (its "mochi" poison spreads Sweetrot across the field). The Sweet Market's vendors blink awake in the street. If `OGERPON_TRUSTED`, Ogerpon waits at the Deep's mouth and walks with you to Gloaming.
3. *Optional:* **the Inverted Ward** (848), an abandoned Choir hospital turned upside down by the thinning Glass.
4. **The Gloamwood Verge:** Prince Caedmon has signed the **Forest Compact**, Meridian survey-flags line the wood, and the Thornguard turns you back "by royal order". The dusk is spreading west (Briarwick's looms work by lamplight at noon). **Celestine**, in her true form (you met her disguised at Briarwick's shrine in Ch3), dissolves the checkpoint with one sentence: "If you stop this child, the forest will remember your name, and it will say it wrong forever."
5. *Optional:* **Queen Maelis**, "resting" under polite guard in a dusk-garden: "The forest is the *sovereign*. I'm just the gardener it tolerates." She gives you a **Royal Writ** (key item: the Wardguard escort to Crownhaven even at low Accord Standing).
6. ☠ **`GO_FAIR_BARGAIN` "Fair Bargain"**: at the lantern-moth market, accept "the answer to your mother's last question" without asking the price (Celestine warned you on arrival: "always ask what it costs *before* you say yes").
7. Comedy scene "Phrasing" (Celestine, who cannot lie, asked about Juno's cooking).
8. **Gym 17, the Storybook Gym:** Celestine. Badge 17, **TM21 Dazzling Gleam**. Her one power play is a **Z-move, not a Mega**: Mimikyu with the Mimikium Z ("This is the part where it hugs you. Hold still. It's worse if you don't.").
9. **The Hymn of Return** in the dusk-chapel at the Great Tree's roots. If you have Wick's verse (Ch10) or Maren's page (the Accord Archive, Ch17), the last verse visibly completes in the key item.
10. **K7** at the Great Tree's roots on `:FAIRY_TALE`: Kestrel, Meridian's sponsored entrant with 18 badges, insists he's the knight and you're the dragon (at high Bond he flinches mid-battle). "Valen wants a lock. Voss wants a key. Your Hollow friends want a crowbar."
11. ⚑ **`:ch18_kestrel_ring`** (if you have Morwen's Ring): *give it now* (Bond up, Redeemed path more likely; it answers him at the semifinal as his Scizor's first Mega) / *keep it* (give it at the semifinal instead).
12. ☠ **`GO_STAY_OUT` "Somebody Else's Story"**: answer *Yes* to "Stay out of Crownhaven?" and then let him walk away. On *No*: "You're going to come. Fine. Then don't lose before you reach me."
13. ⚑ **`:war_legend`** (Ch17–18, 14_WAR_AND_BLESSING): Isenmar asks you to *calm Kyogre* in the Ice Vault, Ashkaar to *wake Reshiram* early with the oath; or *neither* (the only answer that keeps both legends off the Glass Dunes).

### Areas *(design only; maps not built)*

| Map (ID) | Field | Built? | Wild Pokémon (from `pbs/encounters.txt`) |
|---|---|---|---|
| The Throat (852) | New Moon (`:NEW_MOON`) | no | _no wild table yet_ |
| The Blindwater (840) | Cave (`:CAVE`) | no | Cave: Golbat 71–76, Amoonguss 71–76, Weavile 71–76, Malamar 71–76, Sableye 71–76, Drapion 71–76, Krookodile 71–76, Zweilous 71–76, Honchkrow 71–76, Absol 71–76, Zoroark 71–76, Parasect 71–76, Shiinotic 71–76, Thievul 71–76, Breloom 71–76, Deino 71–76, Obstagoon 71–76; Surf: Whiscash 71–77, Quagsire 71–77, Crawdaunt 71–77, Gyarados 71–77, Seismitoad 71–77; Old Rod: Magikarp 40–50, Barboach 40–50; Good Rod: Barboach 70–76, Whiscash 70–76, Crawdaunt 70–76, Basculin 70–76 |
| Lightless Deep (844) | Dark Crystal Cavern (`:DARK_CRYSTAL`) | no | Cave: Weavile 72–77, Sableye 72–77, Malamar 72–77, Drapion 72–77, Bisharp 72–77, Zweilous 72–77, Crobat 72–77, Grimmsnarl 72–77, Honchkrow 72–77, Noivern 72–77, Dusclops 72–77, Zoroark 72–77, Deino 72–77, Tyranitar 72–77, Pupitar 72–77, Morpeko 72–77, Hydreigon 72–77 |
| Lightless Deep B1F (845) | New Moon (`:NEW_MOON`) | no | Cave: Zweilous 74–78, Weavile 74–78, Honchkrow 74–78, Mandibuzz 74–78, Krookodile 74–78, Absol 74–78, Tyranitar 74–78, Skuntank 74–78, Shiftry 74–78, Cacturne 74–78, Mightyena 74–78, Obstagoon 74–78, Scrafty 74–78, Sableye 74–78, Hydreigon 74–78 |
| The Inverted Ward (848) | Inverse (`:INVERSE`) | no | Grass: Malamar 75–79, Ditto 75–79, Zoroark 75–79, Kecleon 75–79, Sableye 75–79, Shuckle 75–79, Inkay 75–79, Spinda 75–79, Smeargle 75–79, Mr. Mime 75–79, Castform 75–79, Absol 75–79, Blissey 75–79, Snorlax 75–79, Slaking 75–79, Porygon2 75–79 |
| Mothwell (850) | Cave (`:CAVE`) | no | _no wild table yet_ |
| The Gloamwood Verge (841) | Silkwood (`:SILKWOOD`) | no | Grass: Whimsicott 73–78, Floette 73–78, Lilligant 73–78, Aromatisse 73–78, Slurpuff 73–78, Granbull 73–78, Azumarill 73–78, Ribombee 73–78, Shiinotic 73–78, Comfey 73–78, Grimmsnarl 73–78, Alcremie 73–78, Clefable 73–78, Wigglytuff 73–78, Dedenne 73–78, Mimikyu 73–78, Hatterene 73–78, Gardevoir 73–78, Togekiss 73–78; Surf: Tentacruel 73–78, Azumarill 73–78, Swanna 73–78, Pelipper 73–78, Lapras 73–78, Mantine 73–78; Old Rod: Magikarp 40–50, Luvdisc 40–50; Good Rod: Luvdisc 72–78, Alomomola 72–78, Staryu 72–78, Corsola 72–78 |
| Gloaming (440) | Fairy Tale (`:FAIRY_TALE`) | no | _no wild table yet_ |
| Great Tree Roots (443) | Silkwood (`:SILKWOOD`) | no | _no wild table yet_ |

### Key battles

**Gym 17 — Warden Celestine Aubade** (Fairy, `:FAIRY_TALE`, cap 80; Core and the Act V outline make it a double battle, GYM_PUZZLES a single)

| Pokémon | Lv | Item | Ability | Moves |
|---|---|---|---|---|
| Tinkaton | 79 | Sitrus Berry | Mold Breaker | Fake Out, Gigaton Hammer, Play Rough, Knock Off |
| Alcremie | 78 | Magical Seed | Aroma Veil | Helping Hand, Dazzling Gleam, Protect, Recover |
| Mimikyu | 78 | Mimikium Z | Disguise | Play Rough, Shadow Claw, Shadow Sneak, Swords Dance |
| Azumarill | 79 | Sitrus Berry | Thick Fat | Aqua Jet, Play Rough, Liquidation, Superpower |
| Togekiss "Vigilant" | 79 | Leftovers | Serene Grace | Follow Me, Air Slash, Dazzling Gleam, Aura Sphere |
| Sylveon "Vow" | 80 | Pixie Plate | Pixilate | Hyper Voice, Draining Kiss, Psyshock, Calm Mind |

*Bag: Full Restore, Full Restore; IV 31.*

- **Hard:** Tinkaton 80 @Sitrus Berry, Alcremie 79 @Magical Seed, Mimikyu 79 @Mimikium Z, Azumarill 80 @Sitrus Berry, Togekiss 80 @Leftovers, Sylveon 80 @Leftovers
- **Casual:** Tinkaton 73 @Sitrus Berry, Alcremie 72 @Leftovers, Mimikyu 72 @Mimikium Z, Togekiss 73 @Leftovers, Sylveon 74 @Pixie Plate

*Field note:* "the arena is a storybook: choose your role (knight, dragon or thief), and the story's rules change who's strong." Fairy, Dragon ×1.5, Steel ×1.3; blade moves ×1.3 (and Steel strikes Dragons ×1.5, like a dragonslayer); Fire also hits as Dragon; Draining Kiss ×2 and wakes a sleeper; Magic Bounce, Mirror Armor and Pastel Veil +1 Sp. Def on entry. Three Dragon attacks wake the dragon under the castle: **Dragon's Den**. *Tip:* Steel and Poison; three Dragon moves turn her Fairy field into one that favours Dragons and Fire. On Hard her last Pokémon is a 2-bar boss (`WARDEN_ACE_2BAR`).

**K7 — Kestrel, the Great Tree's roots** (`:FAIRY_TALE`)

| Pokémon | Lv | Item | Ability | Moves |
|---|---|---|---|---|
| Staraptor | 77 | Sharp Beak | Intimidate | Brave Bird, Close Combat, Double-Edge, U-turn |
| Mismagius | 77 | Life Orb | Levitate | Shadow Ball, Mystical Fire, Thunderbolt, Nasty Plot |
| Scizor | 78 | Life Orb | Technician | Bullet Punch, U-turn, Knock Off, Swords Dance |
| Hydreigon | 78 | Life Orb | Levitate | Dragon Pulse, Dark Pulse, Flash Cannon, Flamethrower |
| **Starter**† | 79 | Sitrus Berry | (slot 0) | (regenerated for the swapped species) |
| Aegislash "Morwen" | 79 | Leftovers | Stance Change | King's Shield, Shadow Ball, Sacred Sword, Shadow Sneak |

*Bag: Full Restore, Full Restore; IV 31.*

- **Hard:** Staraptor 78 @Choice Band, Mismagius 78 @Life Orb, Scizor 79 @Life Orb, Hydreigon 79 @Life Orb, Starter 80 @Life Orb, Aegislash 80 @Weakness Policy
- **Casual:** Mismagius 72 @Sitrus Berry, Scizor 73 @Metal Coat, Hydreigon 73 @Sitrus Berry, Starter 74 @Sitrus Berry, Aegislash 74 @Leftovers

† The rival's starter is written as the Gen 1 line in PBS; Prismfall Core swaps it at battle start for the same-generation counterpart of your starter (same stage).

*Tip:* still no Mega. Morwen's Mismagius (from Ysolde, Ch15) has taken Krookodile's place.

**Boss — Pecharunt** (the Lightless Deep) *(planned multi-bar boss; not registered in Prismfall Bosses yet).*

### Side quests

- **Encore** (`EL_ENCORE`, The Quiet Way; wired (playable)). Dorian Pell, the Grand Stage, Pell Playhouse, Saltmere (154). Unlock: Badges ≥ 16. A gilt-edged lantern: 'ONE NIGHT ONLY. THE PLAYHOUSE REQUIRES A STAR. - D.P.'. Reward: Lopunnite, Normalium Z; +2 pts.
- **The Twilight Cloister** (`EL_TWILIGHT_CLOISTER`, The Quiet Way; designed (not wired yet)). the Abbess, the Twilight Cloister, Gloaming (440). Unlock: Badges ≥ 16. The last trial of the Quiet Way: walk the dusk-chapels from end to end without saying anything at all. Reward: Magical Seed x3; +5 pts.
- **The Causeway Matriarch** (`IS_CAUSEWAY_MATRIARCH`, The Tally; wired (playable)). the Matriarch, the Frostflat Causeway at low tide (560). Unlock: Badges ≥ 16. A Kangaskhan the size of a hut has taken the Frostflat Causeway. Reward: Kangaskhanite; +3 pts.
- **Sweetrot** (`NA_SWEETROT`, The Gutter Book; designed (not wired yet)). a Sweetrot vendor, the Moon Market, Underveil (423). Unlock: S150 CH18_PECHARUNT_DONE. The Sweetrot vendors woke from Pecharunt's spell craving tea. Terrible tea. One cup in particular. Reward: Poltchageist Lv 72 (HOSPITALITY); +4 pts.
- **Dreamwalker** (`AN_SHIV`, The Rite of Reflection; designed (not wired yet)). Lector Saffi Ivarne, the dusk-chapels of Gloaming (440). Unlock: Badges ≥ 17. A stranger has been walking through other people's dreams in Gloaming and leaving them better rested. The Lectors want a word. Reward: Magical Seed; +3 pts.
- **Dreamwalker, the cameo fight** (Shiv; CAMEOS): in Gloaming's dusk-chapels a grinning stranger keeps appearing in the townsfolk's dreams; he says he's met you before, on a ferry. Fight: Sableye 80 @Leftovers, Liepard 81 @Focus Sash, Hypno 82 @Leftovers, Malamar 82 @Sitrus Berry, Cinccino 83 @King's Rock, Ambipom 84 @Silk Scarf.

**Event Pokémon:**

- **Poltchageist Lv 72 (HOSPITALITY)**: gift, the Moon Market, Underveil. Brew Larch's kelp tea for the Sweetrot vendors. *(designed, not implemented)*
- **Kangaskhan "The Matriarch" Lv 78 (SCRAPPY)**: boss battle (guards a reward; doesn't join), the Frostflat Causeway, the old cairn (low tide). Talk to her on the causeway's crown and prove you're worth the road.

**Mega Stones and Z-crystals:**

- **Galladite** (Mega Stone, from Badge 16): The Gloamwood Verge, the knight's barrow. item. *(planned: map not built)*
- **Medichamite** (Mega Stone, from Badge 16): The Iron Pit, the meditation shelf above the top tier (Rock Climb). hidden item. *(planned: map not built)*
- **Heracronite** (Mega Stone, from Badge 16): Gossamer Wood, the old sap tree. hidden item.
- **Lopunnite** (Mega Stone, from Badge 16): Pell Playhouse, the Grand Stage: Dorian's encore. quest EL_ENCORE.
- **Kangaskhanite** (Mega Stone, from Badge 16): Frostflat Causeway: the Causeway Matriarch. **boss** IS_CAUSEWAY_MATRIARCH.
- **Normalium Z** (Z-crystal, from Badge 16): Pell Playhouse: Dorian's encore, the Pageant's "prop jewel". quest EL_ENCORE (with the Lopunnite).
- **Snorlium Z** (Z-crystal, from Badge 16): Mothwell, the hay barn with a Snorlax-sized dent. item. *(planned: map not built)*

### Gym 17 — the Storybook Gym (Celestine Aubade) *(design only)*

- **Puzzle (10/10, about 40 minutes): "she cannot lie, but she can phrase."** Everyone in the storybook is truth-bound; every statement is literally true, and the puzzles are about what the statements *don't* say.
    - **450 Prologue Page:** the sign says at least one door leads on; the left door's plaque says the right door leads on. If the plaque were false the sign would be false too, so **take the right door**.
    - **451 The Red Path** (stepping off the path calls the wolf): **right, right, then the stone that isn't painted.** "The left way is shorter" is true, and it ends at the wolf's den.
    - **452 Midnight Ballroom:** reach a stair within 40 steps (60 on Casual) past six looping dancers (touching one costs 3 steps). Only the **silver (west) stair** leads on, though nobody has ever been seen leaving by it; the intended route is 32 steps. *(To be verified by the builder.)*
    - **453 The Eight Princesses:** beat the eight princess trainers (one Eeveelution each) in any order; their eight true statements locate the Sylveon key in the **Glaceon alcove** (cold, lit, east).
- **Badge:** Badge 17. **TM21 Dazzling Gleam.** **Level cap after: 85.**
- **Mastery (optional):** the Ninth Door (455): ask the Courtier "Which door would the Knight tell me is the right one?" Reward: Magical Seed ×2, Fairy Feather and a page of the Hymn in Celestine's hand.
- **Gym trainers:** 8 princesses, a Lady and a Beauty, Lv 76–79. *(Not in PBS yet.)*

---

## Chapter 19 — "The Last Gate"

*The Truce Road: the Gloamwood (860, `:FAIRY_TALE`), the Thornwar Marches (861) with Thornwatch (870), the Wyrmspine (872) to Wyrmrest (460–475, Ashkaar), the Wyrmscar Rift (864 `:CAVE` / 865 `:DRAGONS_DEN`). The war theatre on Ossaria's western dunes (**built**): the Rimed Sands (920), the Ashkaar Siege Camp (924) and its Command Pavilion (928), the Steamline (925), the Glass Dunes (926), the Observers' Mesa (929) and the bone-carters' camp (930). Then the Rainbow Scar (868) and the Pilgrim Road: Dominar's Toll (892), the Pilgrim Pass (880), Pilgrim's Rest (890), the Coronation Road (893), the Sovereign's Ascent (884–886) or the Glassfall Scar (888). Gym 18.*

### Key events

- **Sigrun's trial and oath.** She won't let you challenge her until you walk the Wyrmscar Rift to the Draco Plate with her and say aloud what you mean to do at the Festival (⚑ `:ch19_oath`). On the walk, her confession: "He told me I'd never survive the Crown, and I was relieved. ... For two years I knew, and I let it happen, because it meant it wasn't me."
- **The Battle of the Glass Dunes** (WAR-1, ⚑ `:war_climax`): Kyogre drags a flood-sea across the desert, Reshiram wakes in the Dominar's hand, and their beams meet over the flooded dunes.

### Order of events

1. **The Gloamwood**, **the Thornwar Marches** and **the Wyrmspine** to Wyrmrest. The Dominar is at the front; he has ordered the pass closed to everything Zenith-tainted (your Fellowship, your badge case). **Sigrun Ashfall** keeps it open anyway, standing on the gate with her Salamence: "*I* do the weighing, Father. Not you."
2. **Sigrun's trial** in the Wyrmscar Rift, and her confession (above).
3. ⚑ **`:ch19_oath`** at the brazier over the Draco Plate (an authored PC line): *"I'm going to give them back."* (Return) / *"I'm going to keep them safe. Whatever it costs me."* (Keep) / *"I don't know yet. I'm going to find out with my eyes open."* (Open) / *(only at Resonance ≤ −2)* *"I'm going to end it. All of it."* ☠ **`GO_LIARS_PYRE` "Liar's Pyre"**: the fifth option, "Whatever you want to hear." Comedy scene "Weighed" (the night before the oath; the only joke in the chapter).
4. **To the front:** word comes that Kyogre has risen and the Dominar has carried the Light Stone to the dunes. Sigrun flies you there overnight and sets you down at dawn on the Dry Tide by the bone-carters' camp (930).
5. **The lines** (the side you didn't choose; both, by way of the Steamline, if you stand between): Isenmar's trench-lines on **the Rimed Sands** (920) or the Siege Camp's earthworks (**924**), and **the Steamline** (925).
6. ⚑ **`:war_climax`** (MAJOR) on **the Glass Dunes** (926): *stand between* (switch 607) / *back Ashkaar* (605) / *back Isenmar* (606).
7. **Partner battle** on the crest of the Glass Dunes (by your choice; see Key battles).
8. **The legend:** you fight whichever legendary is about to fire on the other army: **Reshiram** by default, **Kyogre** if you back Ashkaar. Then the cutscene **WAR-1 "The Beam Clash on the Glass Dunes"**. If `:war_legend` was *neither*, no legend comes (the clash is between the Wardens' aces) and Reshiram's fight happens at Wyrmrest after the truce, as below.
9. **The outcome:** `WAR_STOPPED` (stood between with War Trust ≥ 4: the beams part over you) / `WAR_BOTH_BROKEN` (stood between without that trust: both front lines are glassed, both kingdoms lose a Festival seat) / `WAR_ASHKAAR_WON` or `WAR_ISENMAR_WON` (the loser forfeits a seat). Meridian observers on **the Observers' Mesa** (929) pack up before the steam clears; Larch by radio: "That wasn't a battle to them. That was a *reading*." The Glass Dunes stay glass: Ossaria's newest necropolis.
10. ⚑ **`:war_terms`** (only if one side won), at the armistice table in Skaldfast's great hall with Kassan uninvited at the end of it: *mercy* / *reparations* / *occupation* (occupation poisons the Good ending).
11. *Optional:* **the Dominar's petition** in the Command Pavilion (928; lies are a capital crime, the oath-brazier is lit). ⚑ **`:ch19_dominar`**: he flies *for* Crownhaven (`DOMINAR_SWAYED`) if you sent the Light Stone to Wyrmrest in Ch8 **and** bring proof (the Arbiter Blueprints or the Larch Papers), or if Sigrun's Bond is ≥ 4 and she speaks for you. Not possible if Isenmar won without mercy terms.
12. **Reshiram** (when the fight happens at Wyrmrest): any true oath wakes the Light Stone in the Rift-shrine (or a Hearthguild runner brings it). Its fire is the truth of your oath: Return and Open lean Harmony, Keep is neutral, Ruin makes the fight savage. It bows to **Sigrun**, not to you, and flies to Crownhaven ahead of you.
13. **Gym 18, the Weighing Hall:** Sigrun at her absolute best ("If you can't beat me, you can't survive him."). The **18th badge**, **TM59 Dragon Pulse**, and the badge case sings all eighteen tones together. With the telemetry intact a Meridian airship turns toward Crownhaven within the minute; sabotaged, Larch on the radio: "He bought it. God help us, he bought it."
14. **The Rainbow Scar** (868, `:RAINBOW`; all eighteen Imprints bleeding together into light) and the Pilgrim Road. At high Accord Standing or with the Royal Writ the Wardguard escort takes you up the **Sovereign's Ascent**; otherwise Edda's smugglers take you through **the Glassfall Scar** (888), among the forty Fixed of AF 290, to the place where you stood at five.

### Areas

| Map (ID) | Field | Built? | Wild Pokémon (from `pbs/encounters.txt`) |
|---|---|---|---|
| The Gloamwood (860) | Fairy Tale (`:FAIRY_TALE`) | no | Grass: Florges 76–80, Whimsicott 76–80, Gardevoir 76–80, Hatterene 76–80, Grimmsnarl 76–80, Alcremie 76–80, Shiinotic 76–80, Amoonguss 76–80, Breloom 76–80, Trevenant 76–80, Leavanny 76–80, Ribombee 76–80, Klefki 76–80, Comfey 76–80, Togekiss 76–80, Gallade 76–80, Vespiquen 76–80, Mimikyu 76–80 |
| The Thornwar Marches (861) | Mountain (`:MOUNTAIN`) | no | Grass: Flygon 77–82, Fraxure 77–82, Talonflame 77–82, Dragonair 77–82, Shelgon 77–82, Gabite 77–82, Hakamo-o 77–82, Scovillain 77–82, Leavanny 77–82, Centiskorch 77–82, Noivern 77–82, Drampa 77–82, Druddigon 77–82, Cyclizar 77–82, Volcarona 77–82, Flapple 77–82, Appletun 77–82 |
| Thornwatch (870) | Mountain (`:MOUNTAIN`) | no | _no wild table yet_ |
| The Wyrmspine (872) | Dragon's Den (`:DRAGONS_DEN`) | no | _no wild table yet_ |
| Wyrmrest (460) | Cinderglass (`:ASHEN_WASTE`) | no | _no wild table yet_ |
| Wyrmscar Rift (864) | Cave (`:CAVE`) | no | Cave: Fraxure 77–83, Gabite 77–83, Druddigon 77–83, Shelgon 77–83, Zweilous 77–83, Hakamo-o 77–83, Dragonair 77–83, Sliggoo 77–83, Drakloak 77–83, Turtonator 77–83, Duraludon 77–83, Noivern 77–83, Camerupt 77–83, Dracozolt 77–83, Dracovish 77–83, Garchomp 78–83, Dragonite 78–83, Flygon 77–83 |
| Wyrmscar Depths (865) | Dragon's Den (`:DRAGONS_DEN`) | no | Cave: Fraxure 79–83, Gabite 79–83, Shelgon 79–83, Dragonair 79–83, Haxorus 79–83, Zweilous 79–83, Hakamo-o 79–83, Sliggoo 79–83, Drakloak 79–83, Duraludon 79–83, Garchomp 79–83, Salamence 79–83, Dragonite 79–83, Hydreigon 79–83, Kommo-o 79–83, Goodra 79–83, Dragapult 79–83, Flygon 79–83 |
| The Bone-Carters' Camp (930) | Desert (`:DESERT`) | yes | _no wild table yet_ |
| The Rimed Sands (920) | Desert (`:DESERT`) | yes | _no wild table yet_ |
| Ashkaar Siege Camp (924) | Cinderglass (`:ASHEN_WASTE`) | yes | _no wild table yet_ |
| The Steamline (925) | The Bleed (`:BLEED`) | yes | _no wild table yet_ |
| The Glass Dunes (926) | Desert (`:DESERT`) | yes | _no wild table yet_ |
| Ashkaar Siege Camp - Command Pavilion (928) | none | yes | _no wild table yet_ |
| The Observers' Mesa (929) | Desert (`:DESERT`) | yes | _no wild table yet_ |
| The Rainbow Scar (868) | Rainbow (`:RAINBOW`) | no | Grass: Sylveon 79–83, Clefable 79–83, Florges 79–83, Togekiss 79–83, Aromatisse 79–83, Slurpuff 79–83, Alcremie 79–83, Gardevoir 79–83, Azumarill 79–83, Wigglytuff 79–83, Granbull 79–83, Mr. Mime 79–83, Ribombee 79–83, Comfey 79–83, Mimikyu 79–83, Hatterene 79–83, Dedenne 79–83 |
| Dominar's Toll (892) | Mountain (`:MOUNTAIN`) | no | _no wild table yet_ |
| The Pilgrim Pass (880) | Mountain (`:MOUNTAIN`) | no | Grass: Ursaring 80–85, Braviary 80–85, Mandibuzz 80–85, Staraptor 80–85, Honchkrow 80–85, Rhydon 80–85, Aggron 80–85, Zoroark 80–85, Donphan 80–85, Hippowdon 80–85, Gogoat 80–85, Steelix 80–85, Piloswine 80–85, Lucario 80–85, Gliscor 80–85, Tyranitar 80–85, Garchomp 80–85, Metagross 80–85, Dragonite 80–85 |
| Pilgrim's Rest (890) | Mountain (`:MOUNTAIN`) | no | _no wild table yet_ |
| The Coronation Road (893) | Grand Stage (`:GRAND_STAGE`) | no | _no wild table yet_ |
| Sovereign's Ascent 1F (884) | Cave (`:CAVE`) | no | Cave: Excadrill 81–86, Steelix 81–86, Gigalith 81–86, Hariyama 81–86, Lucario 81–86, Aggron 81–86, Noivern 81–86, Duraludon 81–86, Claydol 81–86, Bronzong 81–86, Lycanroc 81–86, Crobat 81–86, Rhydon 81–86, Conkeldurr 81–86, Machamp 81–86, Tyranitar 81–86, Metagross 81–86, Garchomp 81–86 |
| Sovereign's Ascent 2F (885) | Cave (`:CAVE`) | no | Cave: Rhyperior 82–87, Mamoswine 82–87, Golem 82–87, Machamp 82–87, Conkeldurr 82–87, Gigalith 82–87, Tyranitar 82–87, Metagross 82–87, Garchomp 82–87, Steelix 82–87, Excadrill 82–87, Crobat 82–87, Aggron 82–87, Lucario 82–87, Salamence 82–87, Dragonite 82–87, Hydreigon 82–87, Kommo-o 82–87 |
| Sovereign's Ascent Summit (886) | Mountain (`:MOUNTAIN`) | no | Grass: Braviary 84–88, Staraptor 84–88, Corviknight 84–88, Talonflame 84–88, Skarmory 84–88, Altaria 84–88, Dragonite 84–88, Salamence 84–88, Noivern 84–88, Aerodactyl 84–88, Honchkrow 84–88, Mandibuzz 84–88, Pidgeot 84–88, Togekiss 84–88, Xatu 84–88, Archeops 84–88 |
| The Glassfall Scar (888) | The Bleed (`:BLEED`) | no | Grass: Kingdra 84–88, Slaking 84–88, Milotic 84–88, Magnezone 84–88, Electivire 84–88, Magmortar 84–88, Rhyperior 84–88, Tangrowth 84–88, Togekiss 84–88, Yanmega 84–88, Gliscor 84–88, Mamoswine 84–88, Porygon-Z 84–88, Rotom 84–88, Gallade 84–88, Froslass 84–88, Probopass 84–88, Dusknoir 84–88 |

**The war theatre (built maps):** items, and the soldiers who stand on them.

**The Rimed Sands (920)**

- **Items:** Never-Melt Ice (51,9) · Full Restore (5,28)
- **Hidden items:** Stardust (rimed dune, 26,30)

**The Ashkaar Siege Camp (924)**

- **Items:** Charcoal (52,36) · Hyper Potion (3,36)
- **Hidden items:** Stardust (dune, 30,5)

**The Steamline (925)**

- **Items:** Ice Stone (2,24) · Fire Stone (60,28)
- **Hidden items:** Stardust (the glass, 33,3)

**The Glass Dunes (926)**

- **Items:** Full Restore (22,35) · Hyper Potion (55,18) · Max Revive (58,46)
- **Hidden items:** Stardust (dunes, 2,43) · Big Nugget (the crest, 38,4) · Never-Melt Ice (behind the wave, 7,14)

**The Observers' Mesa (929)**

- **Items:** Rare Candy (30,20)
- **Hidden items:** Stardust (mesa, 5,20)

**The Bone-Carters' Camp (930)**

- **Items:** Full Restore (40,28)
- **Hidden items:** Stardust (dune, 6,5)

**The Command Pavilion (928):** no items; the Dominar, Anja's cage (the `:war_prisoner` scene of Ch15–16), the map table and the oath-brazier.

**Soldiers** (Standard; Hard +1 level; Casual is about 4–5 levels lower with one Pokémon fewer). The last three lines are the Glass Dunes partner battle's three variants.

- **Isenmar Soldier**: Mamoswine 79, Seismitoad 80 *(map 920)*
- **Isenmar Soldier**: Pelipper 79, Ludicolo 80 *(map 920)*
- **Isenmar Officer Captain**: Politoed 82, Ludicolo 83, Mamoswine 83, Lapras 84 *(map 920)*
- **Ashkaar Soldier**: Magcargo 79, Druddigon 80 *(map 924)*
- **Ashkaar Soldier**: Ninetales 79, Flygon 80 *(map 924)*
- **Ashkaar Officer Captain**: Torkoal 82, Coalossal 82, Arcanine 83, Garchomp 84 *(map 924)*
- **Isenmar Soldier**: Walrein 80, Gastrodon 81 *(map 925)*
- **Ashkaar Soldier**: Camerupt 80, Tyrantrum 81 *(map 925)*
- **Ashkaar Soldier**: Talonflame 80, Turtonator 81 *(map 926)*
- **Isenmar Soldier**: Politoed 80, Kingdra 81 *(map 926)*
- **Isenmar Officer Captain** + **Ashkaar Officer Captain** (double): Pelipper 82, Kingdra 83, Lapras 83, Arctovish 84 / Torkoal 82, Coalossal 83, Arcanine 83, Garchomp 84 *(map 926)*
- **Isenmar Officer Captain** + **Isenmar Soldier** (double): Pelipper 82, Kingdra 83, Lapras 83, Arctovish 84 / Mamoswine 81, Seismitoad 82 *(map 926)*
- **Ashkaar Officer Captain** + **Ashkaar Soldier** (double): Torkoal 82, Coalossal 83, Arcanine 83, Garchomp 84 / Charizard 81, Haxorus 82 *(map 926)*

### Key battles

**Partner battle on the Glass Dunes** (double; your partner by `:war_climax`):

- *Stand between* (S607): you + **Sigrun** vs an Isenmar Captain and an Ashkaar Captain ("Both captains are coming. Back to back.").
- *Back Ashkaar* (S605): you + **Sigrun** vs an Isenmar Captain and Soldier ("The Isenmar line breaks here or nowhere.").
- *Back Isenmar* (S606): you + **Marisol** vs an Ashkaar Captain and Soldier ("Stand on my left; the sea's on my right.").
- Partners: Sigrun Flygon 83 @Soft Sand, Dragonite 84 @Lum Berry, Salamence 85 @Sitrus Berry; Marisol Pelipper 83 @Damp Rock, Lanturn 84 @Sitrus Berry, Gyarados 85 @Sitrus Berry.

**Boss — Reshiram** (`RESHIRAM_GLASS_DUNES`, Prismfall Bosses; map 926 on its default Desert field)

- Lv 85 Calm; bars Casual 2 / Standard 3 / Hard 3. Bar 1: Flamethrower, Dragon Pulse, Earth Power, Extrasensory.
- **Break 1:** Kyogre's flood-sea pours in (`:FLOODED_DUNES`, rain) and it learns **Blue Flare**, which glasses the flood in one (`:GLASS_DUNES`). **Break 2:** Fusion Flare, Sp. Def +1.
- **Last bar:** it **turns back** (result `:turned_back`): no faint, no catch.
- *Tip:* Ground, Rock and Dragon. On the Flooded Dunes its Flamethrower is hissed down to ×0.5 but Blue Flare and Fusion Flare are not, and Blue Flare turns the flood to glass, where Fire is ×1.2: switch to Water-resistant, Fire-resistant Pokémon once it learns Blue Flare.

**Boss — Kyogre** (`KYOGRE_GLASS_DUNES`, if you back Ashkaar)

- Lv 85 Calm, Drizzle (the dunes bloom); Surf, Ice Beam, Thunder, Aqua Ring; bars Casual 2 / Standard 3 / Hard 3.
- **Break 1:** the flood-sea (`:FLOODED_DUNES`); the rain passes (so rain and flood don't stack); Origin Pulse and Calm Mind. **Break 2:** Def and Sp. Def +1 (Hard: Sp. Atk +1 too). No Primal Reversion in this fight.
- **Last bar:** it turns back (`:turned_back`).
- *Tip:* Electric (×1.3 against grounded targets in the flood) and Grass; Blue Flare or Fusion Flare (or two other searing moves) fuse the flood into the Glass Dunes.

**Boss — Reshiram at Wyrmrest** (`:DRAGONS_DEN`; only when `:war_legend` is *neither*) *(planned; only the Glass Dunes version is registered).*

**Gym 18 — Warden Sigrun Ashfall** (Dragon, `:DRAGONS_DEN`, single battle, cap 85)

| Pokémon | Lv | Item | Ability | Moves |
|---|---|---|---|---|
| Flygon | 83 | Soft Sand | Levitate | Earthquake, Dragon Claw, U-turn, Stone Edge |
| Kommo-o | 83 | Sitrus Berry | Bulletproof | Clanging Scales, Aura Sphere, Flash Cannon, Flamethrower |
| Dragonite | 84 | Lum Berry | Multiscale | Roost, Dragon Claw, Extreme Speed, Fire Punch |
| Haxorus | 84 | Lum Berry | Mold Breaker | Protect, Dragon Claw, Earthquake, Poison Jab |
| Dragapult | 84 | Dragon Fang | Clear Body | Dragon Darts, Draco Meteor, Flamethrower, U-turn |
| Salamence "Dreamwing" | 85 | Salamencite | Intimidate | Dragon Dance, Double-Edge, Earthquake, Dragon Claw |

*Bag: Mega Ring, Full Restore, Full Restore; IV 31.*

- **Hard:** Flygon 84 @Choice Scarf, Kommo-o 84 @Throat Spray, Dragonite 85 @Elemental Seed, Haxorus 85 @Lum Berry, Dragapult 85 @Life Orb, Salamence 85 @Salamencite
- **Casual:** Flygon 77 @Soft Sand, Kommo-o 77 @Sitrus Berry, Haxorus 78 @Sitrus Berry, Dragapult 78 @Sitrus Berry, Salamence 79 @Salamencite

*Field note:* "the den's heat rises each turn, and the dragons grow stronger the longer you hesitate." Dragon ×1.5, Fire ×1.3, Water and Ice ×0.7; Dragon types take ×0.83 (lair armour) and Multiscale makes their weaknesses neutral; nothing can be frozen. Four Dragon attacks wake **Wyrmfire** (Dragon ×2, Fire ×1.5, Water and Ice ×0.5); three Water or Ice attacks cool it to a Cave; three Fairy attacks tame it into a **Fairy Tale**. **Mega Salamence "Dreamwing"**. *Tip:* Fairy is the plan twice over: it hits her whole team and three Fairy moves take the den away from her.

### Side quests

- **The Memory Kata** (`NA_MEMORY_KATA`, The Gutter Book; wired (playable)). Six-Fingers Ottoline, the Last Rung, Ironreach (260). Unlock: Badges ≥ 17. CHALK: PAWN SHELF, TOP ROW. A WARDGUARD STONE. THE OWNER WANTS IT GONE TO SOMEONE WHO'LL USE IT. Reward: Lucarionite, Fightinium Z; +4 pts.
- **Dragonsworn** (`AS_DRAGONSWORN`, The Trial by Flames; designed (not wired yet)). Legate Varra Kosk, the Wyrmrest proving ground (460). Unlock: Badges ≥ 17. The highest brand in Ashkaar. Stand in the Dragon's Den and fight the Legate's own dragon while the legions watch. Reward: Life Orb; +5 pts.

**Event Pokémon:**

_None this chapter._

**Mega Stones and Z-crystals:**

- **Steelixite** (Mega Stone, from Badge 17): Wyrmscar Rift, an iron-snake's shed skin in the rift wall. hidden item. *(planned: map not built)*
- **Blazikenite** (Mega Stone, from Badge 17): Thornwatch, the war-brazier on the gate tower. hidden item. *(planned: map not built)*
- **Lucarionite** (Mega Stone, from Badge 17): The Last Rung, Ironreach: the Memory Kata (Gutter Book rank 2). quest NA_MEMORY_KATA. *(planned: map not built)*
- **Fightinium Z** (Z-crystal, from Badge 17): The Last Rung, Ironreach: in Kaito's unit's armband. quest NA_MEMORY_KATA (with the Lucarionite). *(planned: map not built)*

### Gym 18 — the Weighing Hall (Sigrun Ashfall) *(design only)*

- **Puzzle (10/10, about 45 minutes): "nothing passes unweighed."** Scales lower bridges when balanced; statues turn on chains, and each chain drags its two neighbours; the **magma tide** rises and falls every 10 steps, and crust paths exist only at low tide.
    - **470 Gate:** push both hoard piles (2 and 3) onto the pan that needs 5.
    - **471 Wyrm's Spine** (recall): Rock Smash, one Strength push, Rock Climb and Waterfall, timing the tide (a brazier flares at steps 7, 8, 9); two dragon-tamer battles.
    - **472 Statue Court:** follow the chains, not the compass. **9 turns: S1 ×2, S3 ×2, S4 ×2, S5 ×3** (S2 needs no turn of its own).
    - **473 Hoard Scales** (A needs 9, B needs 10; piles 1, 2, 3, 5, 8): the 8 can only reach B, so **A = 1 + 3 + 5, B = 2 + 8**. Push the 2 and the 8 to B over two low tides (the 8 needs both windows), then ferry 1, 3 and 5 to A across the short crust.
- **Badge:** Badge 18. **TM59 Dragon Pulse.** **Level cap after: 90** (the Festival cap).
- **Mastery (optional):** the Weighing of the Heir (475): push the 3-pile onto the great pan and stand on it yourself (the scale reads you as 5), with the three chained statues facing the pan, all within one low tide. Reward: Elemental Seed ×2 and Dragon Fang ("It weighed you and let you pass. It never let me.").
- **Gym trainers:** 6 (Cool Trainer ×4, Ace Trainer ×2), Lv 81–84. *(Not in PBS yet.)*

---

## Chapter 20 — "The Festival of Champions"

*Crownhaven (480–499) in its caldera: Lower Crownhaven and its Market Ring and Pilgrims' Quarter, the Eighteen Gates, Upper Crownhaven's Basilica Close, the Basilica of First Light and its crypts, the Accord Palace (Court of Wardens, Throne Room, Gallery of Plates), the Glassfall Memorial Garden (489), the Festival Grounds' Court of Eight Pavilions (499), the Concordance Spire (493/494/498, a teaser), and the Temple-Arena of the Blessing, the Meridian Prism Arena (490/491/495, `:PRISM_ARENA`). Design only. Festival week, Days 0–6. Caps: R16 90, QF 92, SF 94.*

### Key events

- **The opening ceremony.** Eighteen Wardens carry their Plates down the Sovereign's Stair into the Concordance Ring; Valen performs the Tuning with his crystal arm bare; and your shard sees **Arceus**: *"...Little light. You have carried me far."*
- **Valen's audience** (⚑ `:ch20_audience`): "I chose a country over a woman's name. I'd do it again. I hate that I'd do it again." Then the Night of Masques and **K8**.

### How the Festival works

- **Sixteen stand in the arena:** you and fifteen **kingdom delegates**, two per kingdom and the Sovereign; every possible opponent is someone you have met at least twice. A kingdom that lost the war (or both, if the clash broke both armies) forfeits its second seat, and the Accord lends it to a seatless Warden (Dorian first, then Tamsin, Rook, Odessa, Ilsa, Nyx, Corvin).

| Kingdom | Seat A | Seat B (what decides it) |
|---|---|---|
| Elowen | Juno | Celestine (Juno gives *her* seat to "the Gardener" if you earned it) |
| Antumbra | Ysolde | Kestrel if Gravenmoor names him (Redeemed, and the ring given or Ysolde's Bond ≥ 4), else Ilsa |
| Zenith | Rook if he held the footage and is still Meridian's face, else Odessa | Kestrel under Meridian's sunburst if Gravenmoor didn't claim him; else Magnus unless exposed; else Odessa or Rook |
| Nadir | Kaito | Nyx, or Corvin if you freed him and refused Nyx's bargain |
| Ossaria | Sahar | Bastian, unless the raid came in on your beacon (telemetry left) |
| Isenmar | Marisol (or Anja) | Anja, or forfeit (the war) |
| Ashkaar | Sigrun | Brann, or forfeit (the war) |
| The Accord | Valen | — |

- **Your opponent at each stage** is the first matching name (the last line is the fallback). The bowl is honest; the Accord's customs (the Right of Grievance, yielded invitations) bend it on screen.

| Stage (cap) | Opponent | When |
|---|---|---|
| **R16** (90) | Marisol, by Right of Grievance | she holds a seat, Teo died, her Bond ≤ 2 |
| | Anja | she holds a seat and you exposed her in Ch11 |
| | Rowan, "the Gardener" | Rowan lived, you pleaded mercy, Hollow Standing ≥ 4 |
| | **Juno (J4)** | fallback |
| **QF** (92) | Archseer Dask | Ruin Route |
| | Sigrun | Resonance ≤ −3, or you helped Isenmar break her father's legions |
| | Kaito | your oath was Keep |
| | Ysolde | Kestrel has fallen |
| | Odessa | she holds a seat, five close Bonds, Harmony-leaning |
| | **Celestine** | fallback |
| **SF** (94) | Kestrel (Fallen, K9) | `KESTREL_FALLEN` |
| | **Kestrel (Redeemed, K8)** | fallback |
| **Final** (96, Day 7) | Valen, the Last Tuning / Brann | Ruin Route / Valen collapsed |
| | **Valen** | fallback |

- **Your colours** (⚑ `:ch20_colors`, Day 0): Queen Maelis, the Zenith Council and Nyx each offer theirs; Larch offers none (the old clause for "the Unsworn").
- Matches between other entrants resolve by rule, and you can watch the notable ones as highlight cutscenes (e.g. Kestrel beats Kaito: "That isn't him fighting.").

### Order of events

1. **Day 0, arrival:** white stone and bells; **Tamsin's eighteen banners** in Upper Crownhaven, hanging **white** (that Warden would let go of their Plate) or **grey** (won't) by Day 1: the Consent count, made visible. Meridian runs security; the Lantern Hollow are disguised as Choir porters; the kings are in the observers' gallery; **Envoy Delphine Okoro** of the Concert is deciding on Severance. Dask refuses to reopen the Veil Gate: "I won't open a door in a wall that's falling down." In the Glassfall Memorial Garden you meet **Carol**, the Octave's Crownhaven singer. **The Draw** at the Basilica steps.
2. **Day 1, the opening ceremony** (above), in gym order to the Choir's counting rhyme (Rook's cracked Zap Plate in a cradle, or carried by a Meridian officer if he was fired; Corvin's by a porter unless freed; Magnus under guard if exposed; Bastian leaning on Pip). The whole arena sees Valen's crystal arm. You collapse in the stands; Ilsa takes off her earmuffs and flinches. **Rook's leak** if he held the footage (`:ch16_rook` = hold): Kroll with a Meridian keycard on the arena's own screens; Voss doesn't blink.
3. **Day 2, Round of 16** ("someone from your past"; see the draw). After the match, **the garden court**: if Rowan lives, Juno and Rowan on the same bench; Teo (if he lived) or Venam's Testimony: *"I could hear everything while it had me."* Rowan cries, and Juno takes his good hand.
4. **Day 3, exhibitions and the Festival Grounds:** the **Eevee Octave** gauntlet (once all eight singers are helped), the **Pageant Bout** (Dorian and Rook, "a duet for the cameras"), **Juno's Garden Match** (if she wasn't your R16), the **Ebb Guild match** with Marisol (Teo saved and close). The Concordance Spire teaser, street food from every kingdom, Dorian rehearsing in secret with Celestine.
5. ⚑ **`:ch20_envoy`**: *proof* needs two of three, the **Larch Papers**, the **Arbiter Blueprints**, and testimony that the Fixed still dream (Teo's, Corvin's Quiet Ward records, or Venam's Testimony): Okoro recommends against Severance (`ENVOY_PERSUADED`). A *plea* alone: she drafts Severance "with regret".
6. **Day 4, Quarterfinal** ("the honest view"). Default: **Celestine** confirms the Return as an oath: *"Give them back. I've waited forty years to say that to someone who could."*
7. **Day 5:** Corvin, after treating Valen: "He's holding the Plates quiet *right now*, with his body." **The Night of Masques:** Dorian stages Ansel Crewe's banned play *The Gilded King* for the first time in 248 years, Celestine voices Maren's lament, the Wardguard won't push past Kaito, and when the King says *"If heaven will not kneel, we'll build a chain"* every head turns to the Meridian box. Voss stands and applauds, alone: "Bravo. They finally cast the king correctly." Comedy scene "The Good Tea" (before the audience).
8. ⚑ **`:ch20_calla`** (only if someone inside is already moving: Rook holding the footage, or `MAGNUS_KEPT_FAITH`): Calla Wren, shaking in her lanyard ("I scanned you on the dock."). *Shelter her* on Edda's boat (one crack in the Engine; she lives) / *send her back* for the full schematics (two cracks; Kroll finds her in the Spire stairwell) / *turn her away*.
9. **Valen's audience** in the Sovereign's Sanctum. ⚑ **`:ch20_audience`** (authored PC line): *"There's another door. The Hymn. We give them back."* (Return; answer with the Hymn if you hold it complete: "...Maren wrote that. I thought it was a poem.") / *"Then I'll wear it. Somebody has to."* (Keep) / *"You don't get to decide that for me. Nobody does."* (Refuse; with a cold Bond, no Little Owl and live telemetry this sets `VALEN_COLLAPSED`). ☠ **`GO_EARLY_CROWN` "Early Crown"**: accept his desperate offer to crown you tonight (Ilsa warned you: "Don't let him hand you anything tonight.").
10. **Little Owl** (`:sq_little_owl`, Ilsa's quest culmination): if you carried her messages through Acts III–V, she comes to the Sanctum: "Then save the country, Father. Don't make a child pay for it." "...Little owl." (`ILSA_RECONCILED`.)
11. **Morwen's Echo** (exhibition: Kestrel and Ysolde reconciled and the K6 line was Resolve): after midnight Ysolde lights the Cathedral's lantern in a Crownhaven chapel, and Morwen fights you once, gently, "to see what I bought".
12. **Interlude V, "The Last Night"** (play as **Valen**): three letters (to Ilsa, to Morwen's son, to "whoever wears it next"), and a question to a single Zygarde Cell on the sill: "Order, not justice. I chose order. Was I wrong?"
13. **Day 6, Semifinal: K8.** *Redeemed* (fallback): at the first field cycle he tears the Gauntlet off ("If I beat you, I beat *you*."); with Morwen's Ring his Scizor Mega Evolves ("Mum. Just this once. Answer me."). *Fallen:* he keeps the Gauntlet on, it burns his hand, and Voss's men carry him off. Afterwards Ysolde gives him **Morwen's sealed letter** on the arena floor (*"I didn't fail. I chose."*). Other semifinal: Valen beats Sigrun to protect her.

### Areas *(design only; maps not built)*

| Map (ID) | Field | Built? | Wild Pokémon (from `pbs/encounters.txt`) |
|---|---|---|---|
| Lower Crownhaven (480) | Grand Stage (`:GRAND_STAGE`) | no | _no wild table yet_ |
| Lower Crownhaven - Market Ring (496) | Grand Stage (`:GRAND_STAGE`) | no | _no wild table yet_ |
| Lower Crownhaven - Pilgrims' Quarter (497) | Grand Stage (`:GRAND_STAGE`) | no | _no wild table yet_ |
| Crownhaven - The Eighteen Gates (482) | Grand Stage (`:GRAND_STAGE`) | no | _no wild table yet_ |
| Upper Crownhaven - Basilica Close (483) | Grand Stage (`:GRAND_STAGE`) | no | _no wild table yet_ |
| Basilica of First Light (484) | Hollow Cathedral (`:HOLLOW_CATHEDRAL`) | no | _no wild table yet_ |
| Basilica Crypts (485) | Hollow Cathedral (`:HOLLOW_CATHEDRAL`) | no | _no wild table yet_ |
| Accord Palace - Court of Wardens (486) | Grand Stage (`:GRAND_STAGE`) | no | _no wild table yet_ |
| Accord Palace - Sovereign's Throne Room (487) | Grand Stage (`:GRAND_STAGE`) | no | _no wild table yet_ |
| Accord Palace - Gallery of Plates (488) | Grand Stage (`:GRAND_STAGE`) | no | _no wild table yet_ |
| Glassfall Memorial Garden (489) | Flower Garden (`:FLOWER_GARDEN`) | no | _no wild table yet_ |
| Festival Grounds - Court of Eight Pavilions (499) | Grand Stage (`:GRAND_STAGE`) | no | _no wild table yet_ |
| Concordance Spire - Lobby (Battle Tower) (493) | none | no | _no wild table yet_ |
| Concordance Spire - Arena (494) | Grand Stage (`:GRAND_STAGE`) | no | _no wild table yet_ |
| Concordance Spire - Exterior (498) | Grand Stage (`:GRAND_STAGE`) | no | _no wild table yet_ |
| Temple-Arena of the Blessing - Processional Plaza (495) | Grand Stage (`:GRAND_STAGE`) | no | _no wild table yet_ |
| Temple-Arena of the Blessing - Hall of Eighteen Doors (490) | Grand Stage (`:GRAND_STAGE`) | no | _no wild table yet_ |
| Temple-Arena of the Blessing - Altar Stage (491) | Prism Arena (`:PRISM_ARENA`) | no | _no wild table yet_ |

### Key battles

**R16 fallback — J4, Juno** (`:PRISM_ARENA`; with **Ogerpon** in her party if `OGERPON_TRUSTED`)

| Pokémon | Lv | Item | Ability | Moves |
|---|---|---|---|---|
| Florges "Everbloom" | 86 | Leftovers | Flower Veil | Moonblast, Giga Drain, Wish, Synthesis |
| Whimsicott | 87 | Leftovers | Prankster | Leech Seed, Energy Ball, Moonblast, Tailwind |
| Lilligant | 87 | Magical Seed | Own Tempo | Petal Dance, Giga Drain, Sleep Powder, Quiver Dance |
| Gardevoir "Veil" | 88 | Gardevoirite | Trace | Hyper Voice, Psychic, Mystical Fire, Calm Mind |
| **Starter**† | 89 | Sitrus Berry | (slot 0) | (regenerated for the swapped species) |
| Tsareena "Sweetpea" | 90 | Life Orb | Queenly Majesty | Power Whip, High Jump Kick, Knock Off, U-turn |

*Bag: Mega Ring, Full Restore, Full Restore; IV 31.*

- **Hard:** Florges 87 @Leftovers, Whimsicott 88 @Leftovers, Lilligant 88 @Life Orb, Gardevoir 89 @Gardevoirite, Starter 90 @White Herb, Tsareena 90 @Choice Band
- **Casual:** Florges 80 @Leftovers, Whimsicott 81 @Leftovers, Lilligant 81 @Miracle Seed, Gardevoir 82 @Gardevoirite, Starter 83 @Sitrus Berry, Tsareena 84 @Sitrus Berry

† The rival's starter is written as the Gen 1 line in PBS; Prismfall Core swaps it at battle start for the same-generation counterpart of your starter (same stage).

*Tip:* her Gardevoir "Veil" Mega Evolves the first time she fights at the Festival ("...Oh. There you are."): Rowan's ring answers her at last.

**Other R16 draws:**

- **Marisol** (Grievance; also the Ebb Guild match): Pelipper 87 @Damp Rock, Floatzel 87 @Life Orb, Lanturn 88 @Leftovers, Araquanid 88 @Sitrus Berry, Barraskewda 89 @Choice Band, Gyarados 90 @Gyaradosite.
- **Anja** (exposed): Ninetales 86 @Light Clay, Cloyster 87 @White Herb, Glalie 88 @Glalitite, Walrein 88 @Leftovers, Avalugg 89 @Rocky Helmet, Mamoswine 90 @Life Orb.
- **Rowan, "the Gardener"** (a sun team): Sunflora 86 @Heat Rock, Leavanny 87 @Life Orb, Roserade 88 @Focus Sash, Breloom 88 @Life Orb, Shiftry 89 @Life Orb, Trevenant 90 @Sitrus Berry.

**QF fallback — Celestine** ("the wrong key")

| Pokémon | Lv | Item | Ability | Moves |
|---|---|---|---|---|
| Tinkaton | 88 | Sitrus Berry | Mold Breaker | Fake Out, Gigaton Hammer, Play Rough, Knock Off |
| Alcremie | 89 | Magical Seed | Aroma Veil | Calm Mind, Draining Kiss, Mystical Fire, Recover |
| Mimikyu | 90 | Mimikium Z | Disguise | Play Rough, Shadow Claw, Shadow Sneak, Swords Dance |
| Azumarill | 90 | Sitrus Berry | Huge Power | Aqua Jet, Play Rough, Superpower, Belly Drum |
| Togekiss "Vigilant" | 91 | Leftovers | Serene Grace | Follow Me, Air Slash, Dazzling Gleam, Aura Sphere |
| Sylveon "Vow" | 92 | Leftovers | Pixilate | Hyper Voice, Draining Kiss, Psyshock, Calm Mind |

*Bag: Full Restore, Full Restore; IV 31.*

- **Hard:** Tinkaton 89 @Sitrus Berry, Alcremie 90 @Magical Seed, Mimikyu 91 @Mimikium Z, Azumarill 91 @Sitrus Berry, Togekiss 92 @Leftovers, Sylveon 92 @Leftovers
- **Casual:** Tinkaton 82 @Sitrus Berry, Alcremie 83 @Leftovers, Mimikyu 84 @Mimikium Z, Azumarill 84 @Sitrus Berry, Togekiss 85 @Leftovers, Sylveon 86 @Leftovers

**Other QF draws:**

- **Sigrun:** Flygon 88 @Choice Scarf, Kommo-o 89 @Throat Spray, Dragonite 90 @Elemental Seed, Haxorus 90 @Lum Berry, Dragapult 91 @Life Orb, Salamence 92 @Salamencite.
- **Kaito:** Hawlucha 88 @Synthetic Seed, Machamp 89 @Sitrus Berry, Hitmontop 90 @Assault Vest, Conkeldurr 90 @Flame Orb, Lucario 91 @Lucarionite, Medicham 92 @Choice Band.
- **Ysolde:** Sableye 88 @Sablenite, Spiritomb 89 @Sitrus Berry, Dusknoir 90 @Leftovers, Cofagrigus 90 @Magical Seed, Gengar 91 @Life Orb, Chandelure 92 @Choice Specs.
- **Odessa:** Pelipper 88 @Sitrus Berry, Noivern 89 @Life Orb, Pidgeot 90 @Pidgeotite, Oricorio 90 @Elemental Seed, Kilowattrel 91 @Magnet, Corviknight 92 @Leftovers.
- **Archseer Dask** (Ruin Route; suggested field `:INVERSE`): Bronzong 88 @Light Clay, Sableye 89 @Leftovers, Espeon 90 @Life Orb, Umbreon 90 @Leftovers, Gothitelle 91 @Magical Seed, Malamar 92 @Leftovers.

**SF — K8, Kestrel (Redeemed)**

| Pokémon | Lv | Item | Ability | Moves |
|---|---|---|---|---|
| Staraptor | 90 | Sharp Beak | Intimidate | Brave Bird, Close Combat, Double-Edge, U-turn |
| Mismagius | 91 | Life Orb | Levitate | Shadow Ball, Mystical Fire, Thunderbolt, Nasty Plot |
| Scizor | 92 | Life Orb | Technician | Bullet Punch, U-turn, Knock Off, Swords Dance |
| Hydreigon | 92 | Life Orb | Levitate | Draco Meteor, Dark Pulse, Flamethrower, Earth Power |
| **Starter**† | 93 | Sitrus Berry | (slot 0) | (regenerated for the swapped species) |
| Aegislash "Morwen" | 94 | Magical Seed | Stance Change | King's Shield, Shadow Ball, Sacred Sword, Shadow Sneak |

*Bag: Full Restore, Full Restore; IV 31.*

- **Hard:** Staraptor 91 @Choice Band, Mismagius 92 @Life Orb, Scizor 93 @Life Orb, Hydreigon 93 @Life Orb, Starter 94 @Life Orb, Aegislash 94 @Weakness Policy
- **Casual:** Mismagius 85 @Sitrus Berry, Scizor 86 @Metal Coat, Hydreigon 86 @Sitrus Berry, Starter 87 @Sitrus Berry, Aegislash 88 @Magical Seed

† The rival's starter is written as the Gen 1 line in PBS; Prismfall Core swaps it at battle start for the same-generation counterpart of your starter (same stage).

- **With Morwen's Ring** (given in Ch18, `:ch18_kestrel_ring` = give_now): Core adds the ring and a Scizorite at battle start, and his Scizor Mega Evolves: his only Mega. If you kept the ring, no Mega.
- **K9, Kestrel (Fallen):** Genesect 91 @Burn Drive, Mismagius 91 @Life Orb, Scizor 92 @Life Orb, Hydreigon 92 @Life Orb, Starter 93 @Life Orb, Aegislash 94 @Weakness Policy. No Mega: Genesect "Gauntlet" replaces Staraptor.
- *Tip:* the Prism Arena rests for 3 turns, then every 3 turns the Plates turn and the arena takes on the next gym field, announced a turn ahead, in a fixed order: Fire, Water, Grass, Electric, Ice, Fighting, Ground, Poison, Flying, Psychic, Bug, Rock, Ghost, Dark, Fairy, Steel, Dragon, Normal. Super-effective hits on Pokémon of the ascendant type are ×1.2.

**Exhibitions:**

- **The Pageant Bout** (2-vs-1 double): Dorian Lopunny 88 @Lopunnite, Exploud 89 @Throat Spray, Kecleon 90 @Synthetic Seed; Rook Toxtricity 88 @Throat Spray, Electivire 89 @Life Orb, Rotom 90 @Leftovers.
- **Morwen's Echo:** Spiritomb 86 @Leftovers, Dusknoir 87 @Leftovers, Jellicent 88 @Leftovers, Houndstone 88 @Life Orb, Gengar 89 @Life Orb, Chandelure 90 @Choice Specs.
- **Juno's Garden Match** uses her J4 team; **the Ebb Guild match** uses Marisol's Festival team.

### Side quests

- **The Ninth Verse** (`CR_OCTAVE_NINTH_VERSE`, The Hall of Petitions; wired (playable)). Carol of the Octave, the Glassfall Memorial Garden, Crownhaven (489). Unlock: S155 CH20_VEIL_GATE_OPEN and octave_helped >= 7. Petition, sealed in eight waxes: a singer is writing the Octave's Festival song and needs someone who has met them all. Reward: $6000, PP Up x3; +4 pts.
- **Eighteen Shrines** (`CR_EIGHTEEN_SHRINES`, The Hall of Petitions; designed (not wired yet)). the Pilgrim's Rest keeper, Pilgrim's Rest (890). Unlock: Badges ≥ 18. Eighteen roadside shrines on the Pilgrim Pass, one per Plate. Ashkaar charges a toll at six of them. Reward: Fire Stone, Water Stone, Thunder Stone, Leaf Stone, Ice Stone; +4 pts.
- **Lost Property** (`CR_LOST_PROPERTY`, The Hall of Petitions; designed (not wired yet)). the lost-property clerk, the Court of Eight Pavilions (499). Unlock: S155 CH20_VEIL_GATE_OPEN. The Festival lost-property tent has one item. Every day. It's an eel receipt. Reward: Rare Candy x2; +2 pts.
- **The Pavilion Line** (`CR_DELEGATION_DISPUTE`, The Hall of Petitions; designed (not wired yet)). Clerk-Superior Amadeus Fenwright, the Court of Eight Pavilions (499). Unlock: S155 CH20_VEIL_GATE_OPEN. Ashkaar's pavilion is four inches over the line into Isenmar's. Neither delegation will speak to the other. Both will speak to you. Reward: PP Max; +3 pts.
- **Invitations to the Masque** (`CR_MASQUE_INVITES`, The Hall of Petitions; designed (not wired yet)). the Basilica steward, the Basilica Close (483). Unlock: S156 CH20_CEREMONY_DONE. Deliver eight invitations to the Night of Masques. One recipient doesn't exist. One is dead. One is you. Reward: Rare Candy x2; +3 pts.
- **The Chancellor's Other Ledger** (`CR_HOLLIS_LEDGER`, The Hall of Petitions; designed (not wired yet)). an anonymous petition, the Accord Palace (486). Unlock: S155 CH20_VEIL_GATE_OPEN. An unsigned petition, sealed with all eighteen kingdom seals: Chancellor Hollis keeps a second ledger. Reward: $12000; +4 pts.
- **An Old Man's Errand** (`CR_VALENS_ERRAND`, The Hall of Petitions; designed (not wired yet)). Valen Corrigan, the Memorial Garden (489). Unlock: S158 CH20_AUDIENCE_DONE. Valen asks you, not as Sovereign, to fetch something from the Memorial Garden that he can't bend down to pick up any more. Reward: PP Max, VALEN+2; +4 pts.
- **The Eevee Octave gauntlet** (`design/EEVEE_OCTAVE.md`; opens in the Glassfall Memorial Garden once Carol is helped, and stays open into the post-game): nine battles back to back with **no healing**, the eight singers **in the order you helped them**, each with one Eeveelution and its type's Z-crystal on its home field, then Vesper on the Grand Stage. Reward: an **Eevee** and the **Eevium Z** (your Warden's ring wakes it).
    - Lyra (Flower Garden stage 3): Leafeon 87 @Grassium Z · Aria (Water Surface): Vaporeon 87 @Waterium Z · Cadence (Neon Grid): Jolteon 87 @Electrium Z · Sona (Mindscape): Espeon 87 @Psychium Z
    - Noct (New Moon): Umbreon 87 @Darkinium Z · Forte (Volcanic): Flareon 87 @Firium Z · Lento (Frozen Lake): Glaceon 87 @Icium Z · Carol (Fairy Tale): Sylveon 87 @Fairium Z
    - **Vesper**, Eevee "Amen" (Extreme Evoboost opens): Eevee 89 @Eevium Z.
    - Carol's own duet first (*The Ninth Verse*: tell her the seven verses in the order you helped the singers): Florges 87 @Leftovers, Sylveon 88 @Sitrus Berry.

**Event Pokémon:**

- **Eevee Lv 70 (ADAPTABILITY)**: gift, the Glassfall Memorial Garden, Crownhaven. Win the Octave's gauntlet: all eight singers in the order you helped them, then Vesper's Eevee.

**Mega Stones and Z-crystals:**

- **Audinite** (Mega Stone, from Badge 18): Corvin Mott's Infirmary, Mirefen: Wenlow (post-game). quest NA_BEDSIDE_MANNER. *(planned: map not built)*

---

## Chapter 21 — "Sovereign"

*Day 7 in the Prism Arena (491, `:PRISM_ARENA`). Design only. Caps: Final 96, hijack 100, Arceus 100.*

### Key events

- **The hijack.** As Valen raises the Crown over you, the Meridian Prism Arena wakes: it *is* the **Arbiter Engine**. The keystone cradle rises in a golden hand, the Concordance Ring sprouts eighteen golden locks, the Crown is torn into the cradle, and Voss descends in an Engine-harness: *"You carried my key through eighteen doors. Let me show you what it opens."*
- **Arceus**, Valen's death and the final choice (⚑ `:ch21_final`).

### Order of events

1. **The Final: Valen Corrigan** ("Come on, then. Show me there's another door."). His crystal spreads from shoulder to throat each time the field cycles. If `VALEN_COLLAPSED`, you fight his successor instead: **Sigrun** (Bond ≥ 5) or **Brann**, in tears ("He asked me to. Last thing he asked."). "Velmora has a new champion."
2. **The Coronation.** ⚑ **`:ch21_crown`**: *kneel* / *stand* / *step back* (flavour the endings may read). The eighteen Plates *scream*.
3. **The hijack** (above). The hijacker is **Voss**, or **Dr Quent** if Voss was discredited (`MAGNUS_EXPOSED` + Rook's leak + the Night of Masques), or Aurelius on the Ruin Route.
4. **His hand** (Larch warned you that morning: "Don't let him make you a part."). ⚑ **`:ch21_hand`** with `VOSS_ACCEPTED`: *take* it (**Concord Dawn** begins here; Arceus is never fought) / *refuse* ("You promised."). Without it, ☠ **`GO_HIS_HAND` "His Hand"**: take his hand.
5. **The allies move** (one line each, only if earned: Larch's eleven lamps): Rook cuts Lumen's grid (`ROOK_CUTS_GRID`); Nyx blacks out Meridian's comms (surgical with her bargain); Magnus disables the governor (`MAGNUS_KEPT_FAITH`); Marchetti stands the Directorate down (`MARCHETTI_TURNED`); Larch reads the miscalibration (`TELEMETRY_SABOTAGED`); Calla's schematics (one lamp or two); Sigrun and Reshiram hold the sky (with the Ashkaar legions if `DOMINAR_SWAYED`); Marisol's fleet and Edda evacuate Lower Crownhaven; Tamsin's silk nets catch the debris; the Lantern Hollow guard the pylons (`LANTERN_HOLDS`); Kaito holds the gate.
6. **Tag battle** on the cracking arena floor: you + **Kestrel** (Redeemed) or **Juno** (J7) vs two of Marchetti, Quent and Kroll (whichever aren't turned, dead or hijacking).
7. **Voss** (multi-bar for his ace, Silvally "Project NULL", whose type follows the active field). "I'm the only adult in this arena who'll say the true thing out loud: *we don't need it*." Between bars 2 and 3, if `KESTREL_FALLEN`, Kestrel is revealed harnessed into the Engine: ⚑ **`:ch21_reach_kestrel`**: *reach* him (needs Morwen's Ring or her words from a kept letter: *"Be the kind that's nearest when it matters."*) / *burn* the Gauntlet off (he lives, scarred; Ruin −3) / *let go* (`KESTREL_LOST`: the road to *The Empty Lighthouse*). On defeat Voss drives his harness-spike into the cradle: "Then *I'll* hold it."
8. **Arceus descends,** dragged into the golden chains; the arena turns to `:BLEED` across the caldera. Its Judgment strikes the harness: ⚑ **`:ch21_spare_voss`**: *shield* him with the shard (`PC_SPARED_VOSS`) / *let it judge*.
9. **Valen holds the Ring:** he puts the cracked Crown back on and holds the surge with his bare hands on two pylons (Ilsa at his back if reconciled: "Little owl's got you."). *"Go. Free it. I'll hold the door — I've had thirty years of practice."*
10. **The True Finale: Arceus** (below). Between bars the three Wardens of that bar's gyms kneel at their pylons and **release** their Plate or **refuse** (every refusal makes the next lock forced: +1 to all Arceus's stats for that bar). All 36 lines are in `story/11_FINALE_LINES.md`. Celestine sings the Hymn's last verse as her lock breaks, and the arena picks it up.
11. **Valen's death** (every main-route path except Gilded): as the last lock breaks his crystal burns through to light; he says your name (or "Little owl").
12. **Arceus speaks** (through Ilsa if reconciled): *"I will not take what is not given. I learned that here."* ⚑ **`:ch21_final`**: **Return** "Go home. Take them with you." (always) / **Keep** "I'll keep them. I'll keep everyone safe." (always) / **Borrowed** (Kestrel Redeemed and devoted, or Sigrun's Bond ≥ 6: they take the Crown instead: "Not you. Let me be nearest.") / **Concord** (`VOSS_ACCEPTED`, or the governor never switched off) / **Unmake** (Resonance ≤ −6, or Hollow Standing ≥ 4 with Rowan radicalised or Kroll never publicly exposed). Comedy scene "Lecture Forty" belongs to the epilogue only.

### Key battles

**The Final — Sovereign Valen Corrigan** (`CHAMPION_VALEN`, `:PRISM_ARENA`, cap 96)

| Pokémon | Lv | Item | Ability | Moves |
|---|---|---|---|---|
| Bronzong | 92 | Leftovers | Levitate | Stealth Rock, Gyro Ball, Psychic, Trick Room |
| Volcarona | 94 | Sitrus Berry | Flame Body | Quiver Dance, Fiery Dance, Bug Buzz, Giga Drain |
| Kingdra | 94 | Mystic Water | Swift Swim | Draco Meteor, Hydro Pump, Ice Beam, Rain Dance |
| Gallade | 94 | Galladite | Justified | Close Combat, Psycho Cut, Leaf Blade, Swords Dance |
| Lapras "Ferry" | 93 | Assault Vest | Water Absorb | Freeze-Dry, Hydro Pump, Thunderbolt, Sparkling Aria |
| Zygarde | 96 | Leftovers | Power Construct | Thousand Arrows, Outrage, Dragon Dance, Stone Edge |

*Bag: Mega Ring, Full Restore, Full Restore; IV 31.*

- **Hard:** Bronzong 93 @Leftovers, Volcarona 95 @Heavy-Duty Boots, Kingdra 95 @Life Orb, Gallade 95 @Galladite, Lapras 94 @Assault Vest, Zygarde 96 @Leftovers
- **Casual:** Bronzong 86 @Leftovers, Volcarona 88 @Sitrus Berry, Kingdra 88 @Scope Lens, Gallade 88 @Galladite, Lapras 87 @Assault Vest, Zygarde 90 @Leftovers

*Tip:* Zygarde reaches Complete Forme on its last bar ("Order, not justice. I chose order."); on the Ruin Route's Last Tuning (v1) it is Complete from bar 1. Mega Gallade is his one Mega.

- **Brann, stand-in** (if Valen collapsed): Torkoal 92 @Heat Rock, Camerupt 93 @Cameruptite, Magmortar 94 @Elemental Seed, Arcanine 94 @Sitrus Berry, Coalossal 95 @Weakness Policy, Centiskorch 96 @Charcoal.

**Tag battle — the arena floor** (partner: Kestrel if Redeemed, else Juno J7: Whimsicott 95 @Leftovers, Starter 96 @Sitrus Berry, Tsareena 97 @Life Orb)

- Marchetti: Mabosstiff 95 @Sitrus Berry, Manectric 96 @Manectite, Corviknight 97 @Leftovers
- Quent: Bronzong 95 @Leftovers, Metagross 96 @Metagrossite, Porygon-Z 97 @Life Orb
- Kroll: Obstagoon 95 @Flame Orb, Sharpedo 96 @Sharpedonite, Kingambit 97 @Black Glasses

**The hijack — Aurelian Voss** (`MERIDIAN_VOSS`, `:PRISM_ARENA`, cap 100)

| Pokémon | Lv | Item | Ability | Moves |
|---|---|---|---|---|
| Ampharos "Lumen" | 96 | Ampharosite | Static | Thunderbolt, Dragon Pulse, Focus Blast, Agility |
| Archaludon | 97 | Power Herb | Stamina | Electro Shot, Flash Cannon, Draco Meteor, Body Press |
| Magnezone | 96 | Magical Seed | Magnet Pull | Thunderbolt, Flash Cannon, Volt Switch, Body Press |
| Golurk "Gilder" | 97 | Life Orb | No Guard | Dynamic Punch, Earthquake, Poltergeist, Stone Edge |
| Porygon-Z | 99 | Choice Scarf | Adaptability | Tri Attack, Dark Pulse, Ice Beam, Thunderbolt |
| Silvally "NULL" | 100 | Steel Memory | RKS System | Multi-Attack, Crush Claw, Flame Charge, Swords Dance |

*Bag: Mega Ring, Full Restore, Full Restore; IV 31.*

- **Hard:** Ampharos 97 @Ampharosite, Archaludon 98 @Power Herb, Magnezone 97 @Choice Specs, Golurk 98 @Life Orb, Porygon-Z 100 @Choice Specs, Silvally 100 @Steel Memory
- **Casual:** Ampharos 90 @Ampharosite, Archaludon 91 @Sitrus Berry, Magnezone 90 @Sitrus Berry, Golurk 91 @Sitrus Berry, Porygon-Z 93 @Sitrus Berry, Silvally 94 @Steel Memory

*Tip:* Mega Ampharos "Lumen" ("light for everyone"); Silvally's type follows the active field, so watch the Plate announcements and switch a turn early.

- **Dr Quent instead** (Voss discredited): Bronzong 96 @Leftovers, Metagross 97 @Metagrossite, Jirachi 97 @Leftovers, Porygon-Z 98 @Choice Specs, Magnezone 99 @Magical Seed, Silvally 100 @Steel Memory.

**True Finale — Arceus** (`ARCEUS_FINALE`, Prismfall Bosses, Lv 100 on `:PRISM_ARENA`; BALANCE §7)

- Multitype, Timid, IV 31, 252 Sp. Atk / 252 Speed; uncatchable, status immunities. Boss boost (HP / other stats): Casual 1.5 / 1.1, Standard 2.0 / 1.25, Hard 2.5 / 1.3.
- **Bars by story variant** (NARRATIVE_KEYS §6.6, BALANCE §7): **Bound** (default) 6 bars, bar *k* holding the Plates of gyms 3k−2 to 3k (bar 1 Dorian, Tamsin, Marisol ... bar 6 Nyx, Celestine, Sigrun), and Arceus cycles only among those three Plates and fields; **Miscalibrated** (telemetry sabotaged) 5 bars; **Gilded** (Engine calibrated) 6 bars, the last refilling three times (the Bad ending); **War** (Resonance ≤ −6) 7 bars with every lock forced; **Judgment** (Ruin Route) 7 bars with Giratina-Origin as your partner. BOSSES.md still lists the registered boss as 3/3/4 bars by difficulty.
- Every break: "The Plates answer their god!", a forced Plate turn to the field best against your active Pokémon, negative stages reset, status cured, and a new moveset. The Plate is telegraphed 2 turns ahead on Casual, 1 on Standard and Hard; Recover is off on Casual.
- **The last phase, the Legend Plate:** Arceus becomes ??? type, Judgment turns typeless, the field stops cycling and settles by your Resonance: Harmony `:RAINBOW`, Ruin `:BLEED`, otherwise none.

### The endings *(conditions matrix: `10_CHOICES_ENDINGS.md` §6.3; scenes: `08_ACT_V.md`)*

- **Good, "Homecoming"** (Return with enough Consent and Harmony): Arceus ascends with the Plates; the Bleed recedes; the Fixed who still dream wake (Elin under Verdance's first falling leaves, Dex finishing his wave, the Quiet Ward, the forty of the Glassfall Scar); the land imprints you at last. Epilogue: "One Year Later", the first Festival of Seasons.
- **Bad, "The Gilded Chain"** (Engine calibrated): Arceus bound above Crownhaven as a second sun, and you asleep in the cradle as "the Sovereign Who Sleeps". No post-game.
- **Grey:** "The Long Vigil" (Keep), "Homecoming, Unfinished" (Return with Consent < 12 or Resonance < 2: the refusing Wardens' cities suffer a Last Shatter), "The Empty Lighthouse" (Return, but `KESTREL_LOST`), "The Hollow Spring" (Unmake), "Concord Dawn", "The Borrowed Crown" (Kestrel or Sigrun).
- **Ruin:** "The Unmaking" / "The One Who Came Back" (`story/12_RUIN_ROUTE.md`).
- **Post-game** (full after most endings, partial after the Hollow Spring and Concord Dawn, none after the Gilded Chain): the Concordance Spire and the Warden's Gauntlet (all eighteen at Lv 100), Zygarde at Valen's memorial, the Distortion Core (Giratina), legendary rematches and captures, the Shardfall Isles and the Hallow Strait, Concord Zero (Quent), the cameo superbosses (Lin; Garret's Eden rumour), and Hesper Vane at the lighthouse.

- **Bedside Manner** (`NA_BEDSIDE_MANNER`, The Gutter Book; wired (playable)). Wenlow, Corvin Mott's Infirmary, Mirefen (223). Unlock: Badges ≥ 18. CHALK: INFIRMARY NEEDS VISITORS. NOT DOCTORS. JUST VISITORS. - W. Reward: Audinite; +2 pts.
- **Hand of the Accord** (`CR_ACCORD_CHAMPIONS`, The Hall of Petitions; designed (not wired yet)). Clerk-Superior Amadeus Fenwright, the Hall of Petitions (496). Unlock: S160 POSTGAME. Answer one petition from every kingdom in a single day. Each is a battle. Each Warden who still speaks to you sends one. Reward: Master Ball; +5 pts.

---

# Appendix

## The 23 game overs (the Ledger)

Every game over is a deliberate choice, warned at least once on screen in the same chapter, with `Prismfall.checkpoint` directly before it, and each epitaph is written to a Ledger that survives new games. All 23 unlock the Ruin Route (`10_CHOICES_ENDINGS.md` §4–5).

| # | Ch | Game over | Trigger |
|---|---|---|---|
| 1 | 0 | Homeward | go back on the ferry |
| 2 | 1 | Two in the Orchard | pull Juno through the Veil |
| 3 | 3 | Curtain Call | join the ghost company "forever" |
| 4 | 5 | Live Wire | grab the cracked Zap Plate barehanded |
| 5 | 6 | Sinkfield | step off the bones for the glint |
| 6 | 7 | Sweet Tooth | take the Sweetrot a third time |
| 7 | 8 | Let Them Listen | take the Hammer's detonator |
| 8 | 9 | Pull the Nail | plant Sable's charge where only you can walk |
| 9 | 10 | Loyal | stand with the Loyal Three |
| 10 | 11 | Weather | fight Kyogre the moment it wakes |
| 11 | 11 | Thin Ice | go back for the data core |
| 12 | 12 | Read the Fine Print | (as Kestrel) open Voss's drawer |
| 13 | 13 | Looking Back | look back through the Glass |
| 14 | 14 | Willing | let Quent "examine" you |
| 15 | 15 | Echo | stay for your mother's echo three times |
| 16 | 16 | Overtime | keep copying past the klaxon |
| 17 | 17 | Into the Line | step between the Directorate and Nadir |
| 18 | 17 | The Throne | sit on the Gilded King's throne |
| 19 | 18 | Fair Bargain | buy an answer without asking the price |
| 20 | 18 | Somebody Else's Story | agree to stay out of Crownhaven |
| 21 | 19 | Liar's Pyre | tell the brazier "Whatever you want to hear." |
| 22 | 20 | Early Crown | accept the Crown the night before the Final |
| 23 | 21 | His Hand | take his hand at the hijack |
| R1 | Ruin | Welcome, Behind | accept Dask's offer to stay behind the Glass |
| R2 | Ruin | Long Live the King | kneel to Aurelius |


## The Ruin Route

With all 23 game overs in the Ledger (`ruin_unlocked`), the black pane in Giratina's Reverse Depths (Ch15) offers *Look back?* once more, and *Yes* walks you into the Ruin Route ("Every Type and None", `story/12_RUIN_ROUTE.md`): it replaces the rest of Ch15 through Ch21, with the Ferrymen's Mile, Archseer Dask in the quarterfinal, Valen's Last Tuning in the final, Aurelius the Gilded Reflection as the hijacker, and Arceus's Judgment variant. This walkthrough doesn't cover it chapter by chapter yet.

