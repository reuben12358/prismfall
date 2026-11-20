# DISTRIBUTION_STUDY — how Reborn and Rejuvenation hand out Pokémon (first six gyms)

> SPINE Revision 16: "we cant go around giving out strong fighting types before the gyms! the game is meant to be
> challenging!!! look at how reborn and rejuv distribute pokemon, do it like that."
> This file is the study (sections 1–4) and the rule set Prismfall takes from it (section 5, rules R1–R9). The rules are
> machine-checked: `design/warden_gates.json` → `tools/validate_encounters.py`, `tools/validate_badge_tiers.py`,
> `tools/harness/run_trials.rb`. Prismfall's own Chapters 0–4 are in `POKEMON_AVAILABILITY.md`, `BADGE_TIERS.md`,
> `EVENT_POKEMON.md`.

## 0. Sources and method

| What | Where | How it was read |
|---|---|---|
| Live wild tables | `ref/games/{reborn,rejuvenation}/Data/maps.dat` (`MapMetadata`: `Land`, `LandMorning/Day/Night`, `Cave`, `Water`, `RockSmash`, rods, `Headbutt`, Rejuvenation also `Lava`) | the project's `mapgen/rmarshal.py` under `python3 -I`, through a subclass that tolerates Array hash keys (Rejuvenation keys form-tagged species as `[:DEERLING, :Season]`). Reborn: 403 maps with wild tables, Rejuvenation: 195. Both games' `Scripts/Encounters.rb` confirm `setup` reads `$cache.mapdata` (maps.dat); `encounters.dat` is the older compiled copy. |
| Slot chances | `Scripts/Encounters.rb` | each species carries its own `[chance, min, max]`; rates below are chance / table total. |
| Level caps | `Scripts/{Reborn,Rejuv}/SystemConstants.rb` `LEVELCAPS` | Reborn `[20, 25, 35, 40, 45, 50, 55 …]`, Rejuvenation `[18, 25, 30, 35, 40, 45, 50 …]` (index = badges held). |
| Badges | `Map*.rxdata` events setting `$Trainer.badges[n] = true` | Reborn: 351 Peridot Gym (0), 127 Onyx Trainers' Arena (1), 182 Lapis Gym (2), 197 Yureyu Power Plant (3), 224 Wasteland Hideout (4), 506 Voclain Estate (5). Rejuvenation: 484 East Gearen Gym (0), 488 Amethyst Grotto (1), 389 The Final Trial, Chrysalis Courtyard (2), 400 Goldenleaf Theatre (3), 299 Mynori Sea (4), 410 Kakori Depths (5). |
| Gifts, statics, eggs, trades | every `Map*.rxdata` page and `CommonEvents.rxdata` scanned for `pbAddPokemon`, `pbAddToParty`, `PokeBattle_Pokemon.new`, `pbWildBattle`, `pbGenerateEgg`, `pbStartTrade`, boss calls (Reborn 2,135 hits, Rejuvenation 3,421) | species and levels below marked **(data)** were read from the event script itself. |
| Order and requirements | BigJra's walkthroughs (Reborn 19.5.18, Rejuvenation 14.0.28), downloaded to their own folders, converted to text, split at each badge | the walkthroughs are built from the same data: **56 of 65** (Reborn) and **59 of 69** (Rejuvenation) land/cave/Headbutt/Rock Smash tables of the first six segments match a `maps.dat` table species for species. The rest differ by version (a slot added or removed); fishing tables are split by rod in the walkthrough. |

"Segment *n*" = what you can reach while holding *n* badges, i.e. the stretch before gym *n*+1.

## 1. The gyms studied

| # | Reborn | Type · field | Cap (before → after) | Rejuvenation | Type · field | Cap |
|---|---|---|---|---|---|---|
| 1 | Julia (Volt) | Electric · Electric Terrain | 20 → 25 | Venam (PoisonHeart) | Poison · Concert Venue | 18 → 25 |
| 2 | Florinia (Canopy) | Grass · Desert | 25 → 35 | Keta (Diamond Punch), double | Fighting · Forest | 25 → 30 |
| 3 | Shelly (Cocoon), double | Bug · Forest | 35 → 40 | Marianette (Normality) | Normal · Blessed | 30 → 35 |
| 4 | Shade (Omen) | Ghost · Short-Circuit | 40 → 45 | Narcissa (Phantasm) | Ghost · Haunted on Forest | 35 → 40 |
| 5 | Aya (Blight), double | Poison · Wasteland | 45 → 50 | Valarie (Dewdrop) | Water/Fairy · Water Surface | 40 → 45 |
| 6 | Serra (Rime) | Ice · Mirror Arena | 50 → 55 | Crawli (Infested), double | Bug · Swamp | 45 → 50 |

Rejuvenation's gym 3 is a **Normal** gym, the closest match to our Dorian.


## 2. Pokémon Reborn

Wild tables: map, method, then *species level rate*; three rates are morning/day/night ("-" = absent). Every map is listed once, at the segment where it first opens.


### Before Gym 1 — Julia (Electric). Grand Hall, Opal Ward, Lower Peridot, Peridot Ward, the alleys and Railnet, Mosswater. Cap 20.

| Map | Method | Species, level, rate |
|---|---|---|
| Opal Ward | Grass | Pidgey 2-4 15%/15%/-, Rattata 2-4 32%, Ekans 2-5 6%/6%/20%, Meowth 2-5 7%/7%/15%, Hoothoot 3-5 -/-/19%, Spinarak 2-5 -/-/14%, Bidoof 2-4 25%/25%/-, Patrat 2-4 15%/15%/- |
| Lower Peridot Ward | Fishing (oldrod) | Grimer 2-9 100% |
| Lower Peridot Pool | Fishing (oldrod) | Goldeen 7-11 70%, Finneon 7-11 30% |
| Lower Peridot Ward | Grass | Caterpie 2-7 15%/32%/15%, Hoothoot 2-6 -/-/30%, Ledyba 2-6 32%/-/-, Spinarak 3-7 -/-/27%, Sunkern 2-10 8%/30%/8%, Wurmple 2-7 20%/25%/20%, Cherubi 2-7 25%/13%/- |
| Lower Peridot Alley | Cave | Poochyena 3-9 19%, Stunky 3-10 24%, Trubbish 3-9 57% |
| Underground Railnet | Cave | Stunky 3-9 9%, Woobat 3-8 20%, Noibat 2-9 71% |
| North Peridot Alley | Cave | Poochyena 9-13 36%, Purrloin 10-15 24%, Trubbish 9-14 40% |
| Lower Peridot Ward | Headbutt | Swablu 10-17 55%, Burmy 10-17 45% |
| Opal Ward | Headbutt | Spearow 10-15 30%, Pineco 10-16 40%, Combee 10-17 30% |


**Gifts, events, eggs, trades** (requirement in brackets):
- Starter: any of 21 (Grand Hall, Ame), hidden abilities at normal odds; Eevee, both Vulpix and Porygon sit on the same table as alternative picks (data: `pbAddPokemon(:TREECKO,5)` … `PokeBattle_Pokemon.new(:VULPIX,5)`).
- Pachirisu **or** Zigzagoon Lv 5 (win a street battle, random) (data, Opal Ward).
- Teddiursa Lv 14 (clear daytime; find it at three spots, then it battles) (data: `pbWildBattle(:TEDDIURSA,14)` ×4).
- Gulpin Lv 10 and Whismur Lv 5 (snax in the bag; a dumpster, a house) (data).
- Minccino **or** Espurr Lv 4 (pay a man, then snax; random) (data).
- Delibird (return the Gift Box found near the gym), Kricketot (an ailing one, just ask).
- Budew (clear/sunny weather and a Rose Incense), Tynamo (thunderstorm), Surskit Lv 10–12 (rain, the fountain), Pansear **or** Panpour (rain).
- Blitzle Lv 15 (thunderstorm only; the walkthrough warns it is "a bit too tough" for now) (data).
- Igglybuff (beat two thieves), Skitty (a house), Grubbin **or** Joltik (night + snax, random).
- Trades: Bibarel (Lv 15) → Munna. Headbutt opens with a Lv 13 Bidoof/Zigzagoon.

**Answers to Julia available before her:** none in normal play. No Ground type exists anywhere before Julia: not wild,
not a gift, not a trade. (Two exceptions prove the rule: a Mudkip starter becomes Marshtomp at 16, and the mono-Ground and
mono-Ice passwords swap the Lower Peridot victim event for a Swinub so that a monotype run can be played; data: variable
356 pages of map 42 event 1.) What the player does have is resistances (Grass: Sunkern 30%, Cherubi 25%, Grass starters) and tricks: the
walkthrough's plan is "Kricketune and Mightyena… your second stage starter" plus Zigzagoon's **Mud Sport, which
destroys the Electric Terrain**. Julia's team carries the answer to the obvious resist: Oricorio "punishes your
Grass-type starter".
**Right after the badge** ("1 Badge Quests"): **Numel** (rain + snax, Lower Peridot) and **Onyx** (follow a hiker), the
first Ground types in the game.


### Before Gym 2 — Florinia (Grass). Obsidia Ward and Slums, Coral Ward, Obsidia Park, Onyx Ward. Cap 25.

| Map | Method | Species, level, rate |
|---|---|---|
| Underground Railnet (Obsidia Side) | Cave | Woobat 12-17 20%, Klink 12-18 23%, Noibat 11-18 57% |
| Obsidia Slums B1F | Cave | Mankey 10-15 20%, Pidove 10-15 30%, Trubbish 9-14 15%, Pancham 9-14 12%, Yungoos 10-16 10%, Crabrawler 10-15 13% |
| Obsidia Slums 1F | Cave | Mankey 10-15 20%, Slakoth 10-15 13%, Pidove 10-15 30%, Trubbish 9-14 15%, Pancham 9-14 12%, Yungoos 10-16 10% |
| Obsidia Slums 2F | Cave | Meowth 10-15 13%, Mankey 10-15 20%, Pidove 10-15 30%, Trubbish 9-14 15%, Pancham 9-14 12%, Yungoos 10-16 10% |
| Coral Ward | Fishing (oldrod) | Grimer 12-20 100% |
| Obsidia Alleyway | Cave | Koffing 14-19 24%, Poochyena 13-17 14%, Trubbish 14-19 40%, Yungoos 15-17 22% |
| Obsidia Park | Grass | Oddish 14-16 22%, Venonat 15-17 20%, Bellsprout 14-16 15%, Sunkern 12-17 15%, Sunflora 12-14 5%, Slakoth 12-16 7%, Buneary 15-17 10%, Bonsly 13-17 6% |
| Obsidia Ward | Grass | Oddish 10-16 15%/20%/22%, Venonat 10-17 -/12%/19%, Bellsprout 11-15 15%, Sentret 11-15 5%/10%/-, Hoothoot 10-17 -/-/40%, Sunkern 10-15 22%/10%/-, Sunflora 10-20 6%/6%/-, Slakoth 10-17 7%/7%/-, Buneary 10-17 30%/10%/-, Bonsly 13-17 -/10%/4% |
| Onyx Ward | Grass | Spearow 14-17 10%, Venonat 15-20 13%, Bellsprout 15-20 30%, Pidove 16-19 22%, Tranquill 15-21 25% |


**Gifts, events, eggs, trades:**
- Numel (rain + snax), Onyx (hiker quest), Swirlix (sliding puzzle), Hoppip (windy weather), Lotad (rain + snax).
- An abandoned **egg**: Bronzor, Ducklett, Cacnea **or** Drowzee (random) (data: `pbGenerateEgg` ×4, Obsidia Slums).
- Electrike (night: beat the two Mightyena bullying it), Plusle **or** Minun (snax), Zangoose (trash, right time of day), Lillipup (chase quest), Bounsweet (win a battle), Spoink and Happiny (warehouses), Comfey (Laura's gauntlet).
- **Litleo Lv 18** (data: `pbAddPokemon(:LITLEO,18)`, Underground Railnet): beat a **Lv 35 Klinklang** with 52 EVs and 30 IVs while the cap is 25. The walkthrough: "If this is a bit too hard for now feel free to skip this one."
- Daycare **egg** for freeing the daycare couple: Clauncher, Seel, Remoraid, Spheal, Frillish **or** Clamperl (random).
- Trades: Watchog (Lv 20) → Nosepass; Furret (Lv 15) → **Castform** (Sunny Day sets up Fire).

**Answers to Florinia before her:** common wild Flying (Pidove 30%, Tranquill 25%, Hoothoot 30–40%, Swablu 55% by
Headbutt), Poison (Trubbish 57%, Koffing 24%, Grimer by Old Rod 100%) and Bug. **Fire is never wild**: it comes only as
the Litleo boss, the rain-and-snax Numel, rain Pansear, and the Castform trade chain. Florinia is built for the commons:
the Desert Field boosts her Needle Arm / Pin Missile / Sand Tomb, Cottonee's Prankster Sand Tomb traps, Cacnea gets Sand
Veil, Cradily tanks with Stockpile and Recover. The walkthrough's answers are Fury Cutter, Snover's hail, Castform or
Cherrim's sun, or a Flying core.


### Before Gym 3 — Shelly (Bug, doubles). Jasper Ward, Malchous Forest Park, Rhodochrine Jungle, the Underroot, Beryl Ward and Cemetery, North Obsidia, Lapis Ward, the Grand Stairway. Cap 35.

| Map | Method | Species, level, rate |
|---|---|---|
| Jasper Ward | Cave | Beedrill 17-20 25%, Pidgey 16-22 20%, Pidgeotto 18-22 4%, Carnivine 17-23 9%, Sewaddle 17-20 20%, Scatterbug 17-20 22% |
| Malchous Forest Park | Grass | Beedrill 17-21 20%/32%/-, Pidgey 18-23 12%/15%/-, Oddish 18-21 -/10%/-, Paras 18-23 -/-/20%, Bellsprout 18-22 -/10%/-, Hoothoot 18-23 -/-/22%, Ledyba 18-22 19%/-/-, Spinarak 20-22 -/-/15%, Carnivine 20-25 -/2%/6%, Pansage 20-26 2%/11%/7%, Sewaddle 19-22 15%/-/-, Scatterbug 18-22 22%/10%/20%, Fomantis 18-22 10% |
| Beryl Ward | Cave | Pidgeotto 18-22 15%, Spearow 18-21 17%, Oddish 19-22 10%, Bellsprout 18-21 14%, Pansage 19-22 20%, Sewaddle 19-23 12%, Scatterbug 18-21 12% |
| Rhodochrine Jungle | Grass | Spearow 21-24 12%/20%/-, Gloom 21-23 -/12%/10%, Paras 21-24 -/-/27%, Farfetch'd 22-30 2%/7%/4%, Doduo 21-23 -/5%/-, Tangela 22-28 -/6%/9%, Hoothoot 22-24 -/-/20%, Ledyba 21-24 9%/-/-, Ledian 20-23 20%/-/-, Spinarak 22-24 -/-/10%, Ariados 22-24 -/-/15%, Pachirisu 21-24 5%, Pansage 21-23 5%/15%/-, Sewaddle 22-24 25%/10%/-, Scatterbug 22-24 12%/10%/-, Dedenne 21-23 10%/10%/- |
| The Underroot | Grass | Psyduck 21-23 10%, Zigzagoon 22-24 20%, Spinda 21-23 10%, Kecleon 22-24 10%, Shuppet 21-23 5%, Woobat 23-25 5%, Bunnelby 21-23 6%, Phantump 22-25 7%, Noibat 21-23 12%, Morelull 21-23 15% |
| The Underroot | Fishing (oldrod) | Chinchou 10-20 30%, Barboach 10-20 70% |
| Beryl Ward | Grass | Spearow 21-25 15%/-/-, Fearow 21-25 20%/20%/-, Ekans 21-24 10%/20%/20%, Arbok 22-24 12%/12%/2%, Meowth 21-26 -/-/45%, Doduo 21-25 12%/15%/-, Hoothoot 21-25 -/-/12%, Noctowl 20-25 -/-/21%, Phanpy 21-25 15%/15%/-, Bunnelby 21-26 6%/6%/-, Fletchling 21-25 10%/12%/- |
| Beryl Ward | Headbutt | Aipom 20-25 10%, Pineco 22-26 55%, Burmy 22-26 35% |
| Beryl Cemetery | Grass | Spearow 21-25 15%/-/-, Fearow 21-25 20%/20%/-, Ekans 21-25 10%/20%/20%, Arbok 22-24 12%/12%/2%, Meowth 21-26 -/-/45%, Doduo 21-25 12%/15%/-, Hoothoot 21-25 -/-/12%, Noctowl 20-25 -/-/21%, Phanpy 21-25 15%/15%/-, Bunnelby 21-26 6%/6%/-, Fletchling 21-25 10%/12%/- |
| Beryl Cemetery | Headbutt | Aipom 20-25 10%, Pineco 22-26 55%, Burmy 22-26 35% |
| North Obsidia Alleyway | Cave | Poochyena 23-28 15%, Mightyena 22-27 4%, Stunky 22-27 25%, Trubbish 23-27 20%, Espurr 23-27 14%, Yungoos 22-26 22% |
| Lapis Alleyway | Cave | Rattata (Alolan) 23-28 15%, Raticate (Alolan) 24-26 2%, Meowth (Alolan) 22-26 22%, Persian (Alolan) 24-27 2%, Stunky 22-27 25%, Trubbish 23-27 20%, Espurr 23-27 14% |
| Grand Stairway B1F | Cave | Sandshrew 22-26 30%, Diglett 23-26 12%, Geodude 22-26 10%, Graveler 22-28 17%, Dunsparce 35-38 2%, Chingling 21-25 9%, Noibat 22-26 20% |
| Grand Stairway B2F | Cave | Sandshrew 22-26 30%, Diglett 23-26 12%, Geodude 22-26 15%, Graveler 22-27 20%, Unown 25-40 7%, Dunsparce 33-38 6%, Chingling 23-25 10% |
| Grand Stairway Crystal Room | Cave | Sandshrew 22-26 30%, Diglett 23-26 12%, Geodude 22-26 15%, Graveler 22-27 20%, Unown 25-40 7%, Dunsparce 33-38 6%, Chingling 23-25 10% |
| Grand Stairway B3F | Cave | Unown 20-45 100% |
| Lapis Alleyway | Fishing (oldrod) | Barboach 20-30 100% |


**Gifts, events, eggs, trades:**
- Makuhita (snax), Emolga Lv 20 (clear morning/day) (data), Mareep (snax + a quest), Drifloon (wind), Tropius (sun; "very strong for this point"), Taillow, Helioptile (sun + snax), Spritzee (puzzle), Pumpkaboo (night + Soul Candle) (data), Zorua (rooftop, clear night).
- **Egg** behind a hidden passage: Deerling, Skiddo, Girafarig **or** Nincada (random) (data).
- Trades: Sunkern → Carbink, Mime Jr., Cryogonal **or** Furfrou (random); Ledian and Farfetch'd kept for later trades.
- **Growlithe** (Jasper police chief) and the **Mystery Egg**: breed the police Growlithe, bring the egg back, and get one of 18 strong early lines at random: Azurill, Mareanie, Staryu, Togepi, Sneasel, Shroomish, Gastly, **Axew**, both Vulpix, Pawniard, Litwick, Trapinch, Cottonee, Elekid, Starly, Rockruff, **Larvesta**.

**Answers to Shelly before her:** Flying is everywhere (Noibat 71% in the Railnet since segment 0, Spearow, Fearow,
Pidgeotto, Doduo, Fletchling, Ledian, Noctowl) and Rock arrives in the Grand Stairway (Geodude 15%, Graveler 20%,
Bonsly 10% from segment 1). **Fire is still not wild**: Growlithe (quest), the Mystery Egg's Vulpix/Larvesta/Litwick
(1 in 18 each), Litleo and Numel. Shelly answers her answers: Illumise's 8-turn Prankster Rain Dance stops you burning
the forest and weakens Fire, Swift Swim Anorith outspeeds, Intimidate and Struggle Bug weaken doubles, Telluric seeds.


### Before Gym 4 — Shade (Ghost). Lapis Orphanage, the rival gang, Rock Smash exploration (Slums Playground, Railnet depths, Beryl Cave, Citrine Mountain), the Yureyu Power Plant. Cap 40.

| Map | Method | Species, level, rate |
|---|---|---|
| Underground Railnet | Cave | Geodude 29-32 12%, Graveler 29-32 10%, Mawile 28-36 11%, Skorupi 26-33 10%, Woobat 30-32 10%, Klink 30-32 15%, Klang 34-35 2%, Noibat 30-32 30% |
| Lapis Alleyway | Fishing (oldrod) | Barboach 20-30 100% |
| Slums Playground Entrance | Cave | Mankey 22-29 15%, Primeape 28-34 4%, Watchog 22-30 9%, Pidove 22-28 25%, Pancham 20-29 47% |
| Slums Playground | Cave | Mankey 22-29 15%, Primeape 28-34 4%, Watchog 22-30 19%, Pidove 22-27 15%, Trubbish 26-29 12%, Pancham 20-26 35% |
| Underground Railnet (Tracks Area) | Cave | Geodude 36-39 12%, Graveler 36-39 10%, Mawile 36-41 9%, Skorupi 36-39 5%, Drapion 36-43 2%, Woobat 37-39 10%, Klink 37-41 20%, Klang 36-43 2%, Noibat 37-39 30% |
| Underground Railnet (Narrow Path) | Cave | Geodude 36-39 12%, Graveler 36-39 10%, Mawile 36-41 9%, Skorupi 36-39 5%, Drapion 36-43 2%, Klink 37-41 20%, Klang 36-43 2%, Noibat 37-39 40% |
| Underground Railnet (Depths) | Cave | Geodude 36-39 12%, Graveler 36-39 10%, Mawile 36-41 9%, Skorupi 36-39 5%, Drapion 36-43 2%, Woobat 37-39 10%, Klink 37-41 20%, Klang 36-43 2%, Noibat 37-39 30% |
| Underground Railnet (Depths) | Headbutt | Aron 35-45 100% |
| Beryl Cave 1F | Cave | Bunnelby 28-33 17%, Diggersby 31-35 2%, Scatterbug 28-34 30%, Spewpa 30-33 5%, Vivillon 31-35 2%, Noibat 28-35 15%, Morelull 28-33 25%, Shiinotic 30-33 4% |
| Beryl Cave B1F | Cave | Bunnelby 28-33 17%, Diggersby 31-35 2%, Scatterbug 28-34 30%, Spewpa 30-33 5%, Vivillon 31-35 2%, Noibat 28-35 15%, Morelull 28-33 25%, Shiinotic 30-33 4% |
| Beryl Cave B2F | Cave | Bunnelby 28-33 17%, Diggersby 31-35 2%, Scatterbug 28-34 30%, Spewpa 30-33 5%, Vivillon 31-35 2%, Noibat 28-35 15%, Morelull 28-33 25%, Shiinotic 30-33 4% |
| Citrine Mountain 2F | Cave | Sandshrew (Alolan) 29-35 5%, Sandslash (Alolan) 30-50 2%, Phanpy 26-33 15%, Donphan 30-38 4%, Woobat 26-34 30%, Cubchoo 26-35 17%, Beartic 30-50 2%, Bergmite 26-34 25% |
| Yureyu Power Plant | Cave | Voltorb 32 32%, Duskull 32 14%, Yamask 32 15%, Klink 32 25%, Klang 32 2%, Togedemaru 32 12% |


**Gifts and events:** totem battles (one Ill-Fated Doll each) for Baltoy, Elgyem, Golett in a random order; Croagunk
(the Silver Ring); Aron by Headbutt in the Railnet depths (100%).

**Answers to Shade before him:** Dark has been common since segment 0 (Poochyena 36%, Purrloin 24%, Stunky 24%), Alolan
Rattata/Meowth 15–22% in the Lapis Alleyway, Ghosts (Phantump 7%, Shuppet 5%, then Duskull/Yamask 14–15% in his own
power plant). Shade answers with near-perfect IVs, Short-Circuit boosting his Ghost and Electric moves, Mimikyu's
Disguise and seeds.


### Before Gym 5 — Aya (Poison, doubles). Blacksteam Factory, Apophyll Beach and Cave, Pyrous Mountain, Azurine Island, the Byxbysion Wasteland and Tunnels. Cap 45.

| Map | Method | Species, level, rate |
|---|---|---|
| Apophyll Beach | Cave | Sandygast 31-35 96%, Palossand 36-37 4% |
| Apophyll Beach | Rock Smash | Krabby 31-35 75%, Corphish 31-35 15%, Binacle 31-36 10% |
| Apophyll Beach | Fishing (oldrod) | Grimer 27-36 100% |
| Apophyll Training Grounds | Rock Smash | Geodude 31-35 50% |
| Apophyll Cave 1F | Cave | Graveler 31-35 30%, Numel 31-34 19% |
| Apophyll Cave 1F | Rock Smash | Geodude 31-35 50% |
| Apophyll Cave 2F | Cave | Graveler 31-34 20%, Numel 31-34 14%, Dwebble 31-35 27%, Crustle 40 2% |
| Pyrous Mountain 1F/2F/3F/B1F | Cave | Diglett (Alolan) 30-34 20%, Dugtrio (Alolan) 33-37 4%, Graveler 30-35 7%, Slugma 33-35 12%, Magcargo 33-37 2%, Numel 30-35 20%, Throh 33-35 10%, Sawk 33-35 10%, Noibat 30-35 15% |
| Pyrous Mountain B2F | Cave | Slugma 30-37 53%, Numel 30-35 47% |
| Azurine Island | Grass | Zubat 32-34 -/-/10%, Golbat 32-35 -/-/4%, Gloom 30-35 10%/20%/15%, Paras 30-32 -/-/5%, Parasect 32-35 -/-/2%, Ariados 30-32 -/-/2%, Yanma 30-33 18%/-/-, Wooper 30-34 12%/12%/-, Quagsire 32-35 5%, Shellos 31-35 10%/10%/-, Skorupi 31-35 -/-/10%, Palpitoad 30-36 20%/20%/17%, Foongus 31-35 20%, Amoonguss 30-35 5%/5%/10%, Shelmet 30-35 -/8%/- |
| Azurine Island | Headbutt | Exeggcute 25-32 15%, Pineco 30-36 55%, Burmy 30-33 30% |
| Azurine Island | Fishing (oldrod) | Grimer 27-36 100% |
| Byxbysion Wasteland | Grass | Ekans 31-36 10%/10%/-, Arbok 31-40 20%/12%/-, Muk 31-47 -/27%/9%, Cubone 30-39 -/-/14%, Koffing 31-39 -/12%/10%, Weezing 33-40 -/9%/15%, Skorupi 31-39 32%/-/20%, Drapion 36-39 -/-/10% |
| Byxbysion Wasteland | Headbutt | Unown 40-55 15%, Pineco 36-39 75%, Inkay 30-39 10% |
| Byxbysion Wasteland | Rock Smash | Geodude 32-36 50%, Graveler 32-37 15%, Nincada 33-40 35% |
| Byxbysion Tunnels 1 | Cave | Zubat 31-38 25%, Golbat 30-39 5%, Onix 30-38 10%, Koffing 33-38 10%, Mawile 30-40 8%, Trubbish 33-38 20%, Solosis 31-38 22% |
| Byxbysion Tunnels 2 | Cave | Nidoran 25-36 15%, Nidorina 30-40 7%, Nidoran 25-36 15%, Nidorino 30-40 6%, Zubat 33-38 15%, Koffing 33-38 10%, Trubbish 33-38 20%, Solosis 33-38 12% |
| Byxbysion Grotto / Hidden Tunnel | Cave | Zubat 31-38 25%, Golbat 30-39 5%, Onix 30-38 10%, Koffing 33-38 10%, Mawile 30-40 8%, Trubbish 33-38 20%, Solosis 27-36 22% |


**Gifts and trades:** Corsola (storm + snax), Ledian → Shieldon trade, a Mint gift.

**Answers to Aya before her:** Ground and Psychic have been common since segment 2 (Sandshrew 30%, Phanpy 15%, Diglett,
Geodude; Espurr 14%, Chingling 10%, Unown) and fill this segment (Sandygast 96%, Numel 47%, Palpitoad 20%). Aya's
Wasteland **quarters Earthquake**, turns hazards into end-of-turn damage and boosts her spread Sludge Waves; Venusaur and
Drapion cover Ground and Psychic. This is also the first segment with **wild Fire** (Slugma 53%, Numel 47%, Pyrous
Mountain).


### Before Gym 6 — Serra (Ice). Strength exploration, the Yureyu Building, Tanzan Cove, Chrysolia Forest, Spinel Town. Cap 50.

| Map | Method | Species, level, rate |
|---|---|---|
| Tanzan Mountain | Cave | Sandshrew 36-41 22%, Geodude (Alolan) 37-40 20%, Onix 37-42 20%, Kecleon 37-46 15% |
| Tanzan Cove | Grass | Paras 38-39 -/-/10%, Parasect 39-45 -/-/2%, Poliwag 33-40 17%/-/-, Poliwhirl 40-45 2%/-/-, Ledian 38-41 14%/-/-, Ariados 35-44 -/-/5% |
| Tanzan Cove | Fishing (oldrod) | Goldeen 30-37 70%, Seaking 30-40 30% |
| Chrysolia Forest | Grass | Paras 38-39 -/-/10%, Ledian 38-41 14%/-/-, Volbeat 38-45 -/-/7%, Illumise 38-45 -/-/6%, Spinda 35-41 22%/26%/12%, Audino 36-40 5%, Minccino 25-28 5%/5%/-, Deerling 35-41 10%/12%/-, Furfrou 35-39 12%/10%/15%, Pikipek 35-38 15%/15%/20%, Trumbeak 37-41 -/10%/10%, Toucannon 36-48 2%/2%/-, Comfey 39-44 10%/10%/5%, Togedemaru 37-41 5%/5%/10% |
| Chrysolia Forest | Headbutt | Pineco 35-45 10%, Taillow 30-45 60%, Chatot 30-45 30% |
| Chrysolia Spring 1F | Cave | Onix 42-45 10%, Numel 37-40 15%, Camerupt 45-55 2%, Kecleon 40-48 10%, Gastrodon 45-55 2%, Pansear 36-41 10%, Simisear 40-50 5%, Panpour 36-41 12%, Simipour 40-50 4%, Noibat 37-40 20%, Oricorio 37-42 10% |
| Chrysolia Spring 1F | Fishing (oldrod) | Barboach 30-40 30%, Shellos 27-35 70% |
| Lost Railcave | Cave | Sandshrew 36-41 12%, Graveler (Alolan) 37-40 20%, Onix 37-41 10%, Swinub 33-44 10%, Smeargle 35-45 8%, Kecleon 35-45 25%, Noibat 37-40 15% |
| Chrysolia Forest (Clearing) | Grass | Ledyba 35-36 15%/-/- |
| Chrysolia Spring 1F | Fishing (goodrod) | Barboach 37-45 20%, Shellos 37-45 60%, Clauncher 35-45 20% |
| Tanzan Cove | Fishing (goodrod) | Luvdisc 30-40 20%, Mantyke 35-43 20%, Basculin 27-45 60% |
| Lapis Alleyway | Fishing (goodrod) | Carvanha 20-24 20%, Barboach 37-50 80% |
| Azurine Lake | Fishing (goodrod) | Tentacool 37-45 20%, Muk 40-50 60%, Skrelp 35-43 20% |
| Lower Peridot Pool | Fishing (goodrod) | Goldeen 37-45 60%, Seaking 40-50 20%, Finneon 40-50 20% |
| The Underroot | Fishing (goodrod) | Psyduck 27-45 60%, Whiscash 30-40 20%, Skrelp 35-43 20% |


**Gifts and trades:** Strength from Cal, Misdreavus (win a battle), **Squirtle** (rainy days, a fountain: the first
extra starter), **Chikorita** (show an evolved Chimecho), Mothim → Bruxish, Luvdisc → Darumaka, Shelmet/Karrablast swaps.

**Answers to Serra before her:** everything: Fire wild since segment 4, Fighting since segment 1 (Mankey 20%,
Crabrawler 13%, Pancham 12% in the Slums; Throh and Sawk 10% on Pyrous), Steel and Rock. Serra's Mirror Arena (accuracy
and evasion, Bright Powder, Snow Cloak) is what makes the fight hard, not a lack of counters.


## 3. Pokémon Rejuvenation

Wild tables: map, method, then *species level rate*; three rates are morning/day/night ("-" = absent). Every map is listed once, at the segment where it first opens.


### Before Gym 1 — Venam (Poison). S.S. Oceana, East Gearen City, the Gearen Alleyway, Gearen Park, the Abandoned Sewers. Cap 18.

| Map | Method | Species, level, rate |
|---|---|---|
| Gearen Alleyway | Cave | Rattata 11-13 20%, Drowzee 9-15 31%, Purrloin 10-11 35%, Klink 13-14 4%, Lechonk 11 10% |
| East Gearen City | Grass | Pidgey 3-7 15%/-/-, Rattata (Alolan) 4-6 25%/-/25%, Jigglypuff 3-7 -/-/29%, Paras 3-7 29%/29%/-, Hoothoot 4-6 -/-/15%, Poochyena 3-7 -/-/27%, Bidoof 4-6 -/25%/-, Patrat 3-7 27%/27%/-, Pidove 3-7 -/15%/-, Klink 5-8 4% |
| Chrisola Hotel Rooftop | Grass | Caterpie 5-6 22%/22%/-, Weedle 5-6 -/-/22%, Oddish 10 -/-/4%, Meowth 7-9 10%/10%/25%, Bellsprout 10 4%/4%/- |
| Gearen Park | Grass | Spearow 5-7 25%, Psyduck 6-7 15%, Mankey 5 2%, Seedot 6 2%, Kricketot 6-7 -/-/9%, Stunky 5-6 -/-/15%, Pansage 5-6 32%/-/-, Pansear 5-6 -/32%/-, Panpour 5-6 -/-/32%, Fomantis 6-7 9%/9%/-, Skwovet 5-6 15%/15%/- |
| Abandoned Sewers | Cave | Rattata (Alolan) 7-9 30%, Ekans 7-9 10%, Geodude 7-8 2%, Koffing 6-10 9%, Poochyena 7-8 15%, Gulpin 6-7 12%, Trubbish 7 15%, Noibat 5-7 7% |
| Abandoned Sewers | Fishing (oldrod) | Grimer 5-6 70%, Qwilfish 5-6 30% |


**Gifts, events, eggs, trades:**
- Starter on the S.S. Oceana; Nidoran♀ Lv 5 (chase it round East Gearen to four spots, then it battles) (data: `pbWildBattle(:NIDORANfE,5)`).
- Voltorb Lv 6 (buy four Poké Balls at $400 from a con man) (data), Pachirisu (night + Gourmet Treat), Shuppet (night, the hotel 3F), Maschiff (a static), Unown (night, a crack in the park), Wiglett (an item ball), Luvdisc (a quiz).
- **Boss Spidops Lv 18** (Spider-Gang) → you get **Tarountula Lv 10**, not the Spidops (data: `PokeBattle_Pokemon.new(:TAROUNTULA,10)`).
- **Seviper egg** (data: `pbGenerateEgg(:SEVIPER)`, Gearen Alleyway).
- Trade: Oinkologne (Lechonk Lv 18) → Aevian Sandygast (Rock/Ghost, Fire/Ghost or Ice/Ghost).

**Answers to Venam before her:** Psychic is common in one side area (Drowzee 31% in the Gearen Alleyway) and Ground is a
2% Geodude in the sewers. Rejuvenation is looser than Reborn here. Venam's Concert Venue boosts Acid, Fake Out and
Rollout; the walkthrough's advice is "power through… with raw stats and super effective Ground and Psychic moves".


### Before Gym 2 — Keta (Fighting, doubles). Route 1, Goldenwood Forest and Cave, Route 2, Gemstream Mine, Amethyst Cave, Sheridan Village. Cap 25.

| Map | Method | Species, level, rate |
|---|---|---|
| Route 1 | Grass | Caterpie 10-13 20%/-/-, Metapod 13 -/-/2%, Weedle 10-14 -/-/22%, Kakuna 13 -/-/4%, Pidgey 11-15 10%/15%/-, Paras 11-15 -/-/10%, Sentret 11-15 25%/9%/-, Furret 15-20 2%, Pidove 10-15 12%/22%/25%, Sewaddle 13-15 -/7%/10%, Deerling 13-15 11%/10%/-, Scatterbug 9-15 10%/25%/25%, Lechonk 11-14 10%/10%/- |
| Goldenwood Forest | Grass | Sentret 11-14 24%, Furret 15-20 2% |
| Goldenwood Forest | Fishing (oldrod) | Finneon 11-15 100% |
| Goldenwood Cave | Cave | Geodude 10-15 44%, Furret 15 4%, Woobat 11-15 17%, Noibat 11-15 35% |
| Goldenwood Cave | Fishing (oldrod) | Goldeen 11-16 100% |
| Route 2 | Grass | Pidgeotto 13-16 -/5%/-, Spearow 15-17 20%/-/-, Oddish 14-17 -/-/15%, Drowzee 15-16 -/-/20%, Hoothoot 15-16 -/-/9%, Spinarak 14-17 -/-/15%, Volbeat 17-18 -/15%/-, Illumise 15-16 -/-/12%, Combee 15-18 25%/32%/-, Cherubi 13-17 15%/44%/- |
| Route 2 | Headbutt | Metapod 16 4%, Butterfree 16 5%, Beedrill 16 1%, Aipom 16-17 40%, Pineco 17 10%, Burmy 16 5%, Crabrawler 17 20%, Tarountula 16 15% |
| Gemstream Mine | Cave | Onix 11-19 7%, Shuckle 11-21 2%, Dwebble 15-18 9%, Stunfisk 15-19 15%, Carbink 15-19 25%, Cufant 15-18 42% |
| Gemstream Mine | Rock Smash | Diglett 17 75%, Geodude 16 15%, Shuckle 10 10% |
| Route 2 | Fishing (oldrod) | Finneon 11-14 100% |
| Route 2 | Rock Smash | Diglett 15 7%, Geodude 16-17 90%, Shuckle 10 3% |
| Amethyst Cave | Cave | Sandshrew 12-15 15%, Diglett 12-15 10%, Geodude 12-15 29%, Woobat 12-15 42%, Carbink 5 4% |
| Amethyst Cave | Fishing (oldrod) | Remoraid 15 70%, Barboach 15 30% |
| Amethyst Depths | Cave | Sandshrew 19-21 15%, Diglett 16-21 10%, Geodude 17-19 29%, Natu 17-19 10%, Chingling 17-19 32%, Carbink 5 4% |
| Sheridan Village | Grass | Spearow 14-19 13.64%/13.64%/-, Hoothoot 14-19 -/-/17%, Ledyba 17-18 1.82%/1.82%/-, Zigzagoon 15-17 20.0%/20.0%/20%, Dustox 14-19 -/-/10%, Makuhita 15-19 26.37%/26.37%/12%, Kricketot 14-19 13.64%/13.64%/5%, Kricketune 15-18 6.37%/6.37%/5%, Chingling 16-19 -/-/21%, Pawmi 16-17 9.09%/9.09%/-, Shroodle 16-17 9.09%/9.09%/10% |
| Sheridan Village | Rock Smash | Diglett 16 7%, Geodude 15-17 93% |
| Sheridan Village | Fishing (oldrod) | Goldeen 15-16 70%, Finneon 14-15 30% |
| Sheridan Arena | Grass | Hoothoot 14-19 -/-/17%, Ledyba 17-18 1.82%/1.82%/-, Zigzagoon 15-17 27.27%/27.27%/30%, Dustox 14-19 -/-/10%, Makuhita 16-19 28.19%/28.19%/12%, Kricketot 14-19 13.64%/13.64%/5%, Kricketune 15-18 6.37%/6.37%/5%, Chingling 16-19 -/-/21%, Fletchinder 14-19 13.64%/13.64%/-, Pawmi 16-17 9.09%/9.09%/- |
| Sheridan Arena | Fishing (oldrod) | Goldeen 15-16 70%, Finneon 14-15 30% |
| Amethyst Grotto | Grass | Jigglypuff 20-21 27%, Meowth 20-21 27%, Dunsparce 20-22 37%, Glameow 20-22 9% |


**Gifts, events, eggs, trades:**
- Aevian Sewaddle Lv 10 (beat the Aevian trainers) (data), Shadow Pokémon to snag (Meowth, Finneon, Vanillite, Wooper, Pidove, Bonsly).
- Blitzle, Munna, Lunatone Lv 20 (each: a Gourmet Treat) (data), Minccino Lv 15 (an old woman's battle) (data), Shinx Lv 10 (a hotel guest) (data), Houndour Lv 10 (beat a trainer) (data), Solrock (a quest), Elgyem (a book puzzle), Varoom (ride Truck Guy 20 times).
- **Mystery Egg** at the end of a path: Skiddo, Mudbray **or** Galarian Ponyta, fixed when the save file is made (data: `pbGenerateEgg(:SKIDDO)`, `(:MUDBRAY)`, `(:PONYTA,1)`).
- Trades: Barboach → Aevian Pidove; breed Igglybuff from Jigglypuff → **Smoochum** with a Twisted Spoon; Aipom → **Pancham**.

**Answers to Keta before him:** plentiful and common: Flying (Spearow 25%, Pidgey, Pidove, Hoothoot, Combee 32%),
Psychic (Woobat 42%, Chingling 32%, Drowzee 31%, Natu 10%) and Fairy (Jigglypuff 29%). The walkthrough: "The next gym
is fighting type, so most of these are going to be decent options." Keta's answer is his team: "almost everything has a
Dark or Rock type move", Lucario, Combusken with Protect, doubles.


### Before Gym 3 — Marianette (Normal). Carotos Mountain, Cut backtracking, the Spring of Purification, River's End, Chrysalis Manor. Cap 30.

| Map | Method | Species, level, rate |
|---|---|---|
| Carotos Mountain | Cave | Onix 18-21 20%, Slugma 20-22 32%, Nosepass 20-21 4% |
| Carotos Mountain | Fishing (oldrod) | Slugma 20 30%, Numel 19-20 70% |
| Spring of Purification | Grass | Oddish 21 5%, Paras 20-21 10% |
| Spring of Purification | Fishing (oldrod) | Goldeen 15 100% |
| River's End | Grass | Butterfree 16-21 9%, Dustox 16-21 10%, Yungoos 18-19 10%, Oricorio (Pom-Pom Style) 17-19 57% |
| Chrysalis Courtyard | Grass | Meowth (Alolan) 23-25 28.07%, Porygon 24-27 3.5%, Hoppip 23-24 13.16%, Skiploom 24-25 8.77%, Plusle 24-25 13.16%, Minun 24-26 12.28%, Spinda 24-26 8.78%, Bombirdier 24-26 12.28% |


**Gifts and events:** HM01 Cut (after a Miltank fight), Marianette joins as a partner, a Gothitelle battle, a Purify
Chamber for snagged Shadow Pokémon.

**Answers to Marianette before her:** Fighting has been common for a whole gym: **Makuhita 26–28% in Sheridan Village
and the arena**, Crabrawler 20% by Headbutt on Route 2, a 2% Mankey in Gearen Park before gym 1, the Pancham trade.
None of them is a gift with a tailored move. Marianette's team is built against exactly that answer: Psychic Indeedee
(Psyshock), Hisuian **Zorua (Normal/Ghost, immune to Fighting)** with Focus Sash, **Chatot (Normal/Flying)** with Nasty
Plot, Bewear with **Fluffy and Aerial Ace**, Delcatty's Cosmic Power Baton Pass, and Plates turning Multipulse into
coverage.


### Before Gym 4 — Narcissa (Ghost). Route 3, Mirage Woods, Phasial Cave, Goldenleaf Town, the Wispy Path. Cap 35.

| Map | Method | Species, level, rate |
|---|---|---|
| Route 3 (North) | Grass | Doduo 25-26 9%, Zangoose 24-25 2%, Herdier 24-25 25%, Fletchinder 23-25 32%, Yamper 23-25 30%, Boltund 26-27 2% |
| Route 3 / Mirage Woods / Phasial Cave / Goldenleaf Town | Fishing (oldrod) | Wooper 15 100% |
| Route 3 (South) | Grass | Doduo 25-26 7%, Zangoose 24-25 2%, Herdier 24-25 25%, Fletchinder 23-25 32%, Nickit 23-25 30%, Thievul 26-27 4% |
| Mirage Woods | Grass | Doduo 25-26 5%, Stantler 24-25 25%, Zangoose 24-25 2%, Kecleon 23-27 32%, Spritzee 23-25 32%, Spidops 25-26 4% |
| Phasial Cave | Cave | Meowth (Galarian) 23-25 20%, Wooper 23-27 32%, Bibarel 25-26 9%, Venipede 24-25 2%, Chewtle 24-25 25%, Silicobra 23-24 12% |
| Wispy Ruins | Cave | Graveler (Alolan) 30-32 15%, Natu 26-33 9%, Xatu 32-35 2% |
| Forgotten Path | Fishing (oldrod) | Wooper 15 100% |
| Wispy Path | Grass | Phanpy 30-31 10% |
| Wispy Path | Fishing (oldrod) | Basculin (Red/Blue) 15 100% |
| Goldenwood Forest (Overgrown) | Grass | Furret 30-31 2%, Poochyena 30-31 20%, Mightyena 30-31 20%, Plusle 29 10%, Minun 29-30 10%, Pansage 28-30 10%, Pidove 30 12%, Tranquill 27-31 12%, Spewpa 29-30 4% |
| Goldenwood Forest (Overgrown) | Fishing (oldrod) | Goldeen 8 100% |
| Forsaken Laboratory | Grass | Diglett (Alolan) 30-31 32%, Dugtrio (Alolan) 29-31 9%, Geodude 31-32 10%, Graveler 29-31 14%, Dunsparce 29-31 35% |
| Backstage Theatre | Cave | Rattata 31 20%, Raticate 32-34 22%, Shuppet 32 25%, Banette 32-33 10%, Duskull 32-34 15%, Yamask 32-34 8% |


**Gifts and events:** Throh (a static; Sawk by trade), Teddiursa (a static), **Zorua Lv 25** (the Broken Bell quest; the
Dark, Unovan form with egg moves, so Rejuvenation does hand over an answer to the next gym, behind a quest) (data), Zubat (the Cranky Crobat quest), Espurr (friendship games), Fidough (Gourmet Treat), a Mystery Egg from C
(Sizzlipede, Blipbug **or** Joltik), Loudred (if the Exploud spots you).

**Answers to Narcissa before her:** Dark common since segment 0 (Purrloin 35%, Poochyena 27%, Alolan Rattata 30%),
Nickit 30% and Alolan Meowth 28% here; Ghosts in the Backstage Theatre. Narcissa answers with a defensive signature move,
a fast field-boosted Mismagius and Spectral Scream to restore her Haunted Field.


### Before Gym 5 — Valarie (Water/Fairy). Wispy Ruins and Chasm, Route 4, Akuwa Town, Blacksteeple Castle, Kakori Village, the Terajuma Jungle. Cap 40.

| Map | Method | Species, level, rate |
|---|---|---|
| Wispy Chasm | Cave | Graveler 32-35 15%, Zigzagoon (Galarian) 28-36 19%, Linoone (Galarian) 34-35 2%, Baltoy 35-37 5%, Claydol 32-35 2%, Yamask (Galarian) 30-35 15%, Golett 32-35 42% |
| Route 4 (South) | Grass | Meowth 31-34 17%/5%/30%, Sunkern 32-33 20%/-/-, Sunflora 32-34 20%/15%/-, Plusle 25 2%/-/2%, Minun 25 -/2%/-, Tranquill 31-34 14%/10%/19%, Fletchinder 31-32 -/12%/-, Bounsweet 31-34 20%/49%/42%, Togedemaru 32-34 5%, Bombirdier 25 2% |
| Route 4 (South) | Fishing (oldrod) | Finneon 8-9 100% |
| Route 4 (Central) | Grass | Meowth 31-34 17%/5%/30%, Sunkern 32-33 20%/-/-, Sunflora 32-34 20%/15%/-, Nuzleaf 25 2%, Plusle 25 2%/-/2%, Minun 25 -/2%/-, Tranquill 31-34 14%/10%/19%, Fletchinder 31-32 -/12%/-, Bounsweet 31-34 20%/49%/42%, Togedemaru 32-34 5% |
| Route 4 (Central) | Fishing (oldrod) | Finneon 8-9 100% |
| Route 4 (East) | Grass | Meowth 31-34 17%/5%/30%, Sunkern 32-33 20%/-/-, Sunflora 32-34 20%/15%/-, Nuzleaf 25 2%, Plusle 25 2%/-/2%, Minun 25 -/2%/-, Tranquill 31-34 14%/10%/19%, Fletchinder 31-32 -/12%/-, Bounsweet 31-34 20%/49%/42%, Togedemaru 32-34 5% |
| Route 4 (East) | Fishing (oldrod) | Finneon 8-9 100% |
| Route 4 (Northwest) | Grass | Meowth 31-34 17%/5%/30%, Sunkern 32-33 20%/-/-, Sunflora 33-34 15%/15%/-, Nuzleaf 25 2%, Plusle 25 -/-/2%, Minun 25 -/2%/-, Tranquill 31-34 14%/10%/19% |
| Route 4 (Northwest) | Fishing (oldrod) | Finneon 8-9 100% |
| Route 4 (Northeast) | Grass | Meowth 31-34 17%/5%/30%, Sunkern 32-33 20%/-/-, Sunflora 32-34 20%/15%/-, Nuzleaf 25 2%, Plusle 25 2%/-/2%, Minun 25 -/2%/-, Tranquill 31-34 10%/-/9%, Emolga 31-33 4%/10%/10%, Fletchinder 31-32 -/12%/-, Bounsweet 31-34 20%/49%/42%, Togedemaru 32-34 5% |
| Route 4 (Northeast) | Fishing (oldrod) | Finneon 8-9 100% |
| Akuwa Town | Grass | Lickitung 35-37 2%/2%/5%, Noctowl 34-35 -/-/15%, Skitty 36-37 15%/-/-, Delcatty 35-36 10%/-/-, Volbeat 35-36 -/-/10%, Illumise 36-37 -/-/15%, Spinda 34-37 15%, Buizel 35-38 22%, Floatzel 35-37 5%/5%/2%, Blitzle 34-35 15%/15%/-, Audino 35-37 6%, Wattrel 33-38 10%/35%/-, Kilowattrel 33-38 -/-/10% |
| Akuwa Town | Fishing (oldrod) | Seel 15 30%, Buizel 15 70% |
| Blacksteeple Castle | Grass | Tangela 33-35 45%, Teddiursa 35-36 22%, Ursaring 33-34 2%, Delibird 33-35 4%, Skorupi (Aevian) 31-37 5%, Drapion (Aevian) 34-37 2%, Abomasnow 35 5%, Cramorant 35-36 15% |
| Blacksteeple Garden | Grass | Tangela 33-35 45%, Teddiursa 35-36 27%, Ursaring 33-34 2%, Delibird 33-35 4%, Skorupi (Aevian) 31-37 5%, Drapion (Aevian) 34-37 2%, Abomasnow 35 5%, Cramorant 35-36 10% |
| Terajuma Shipyard | Fishing (oldrod) | Krabby 25-26 20%, Carvanha 25-26 60%, Wailmer 25-26 20% |
| Terajuma Jungle | Grass | Butterfree 35-36 -/6%/-, Beedrill 33-34 -/2%/-, Oddish 33-34 -/-/10%, Gloom 33-34 -/-/5%, Venonat 33-34 -/-/10%, Weepinbell 33-34 5%/-/-, Exeggcute 30 -/10%/-, Hoothoot 33-34 -/-/15%, Noctowl 33-34 -/-/2%, Spinarak 33-34 -/-/10%, Ariados 33-34 -/-/6%, Bibarel 33-34 12%/47%/-, Kricketune 33-34 -/-/5%, Foongus 33-34 -/30%/-, Trumbeak 33-34 29%/-/-, Grubbin 33-34 42%/-/-, Charjabug 33-34 2%/-/-, Morelull 33-34 -/-/37%, Smoliv 15-34 10%/5%/- |
| Terajuma Jungle | Fishing (oldrod) | Carvanha 25-26 100% |
| Kakori Village | Grass | Butterfree 34-39 -/6%/-, Beedrill 35-39 -/17%/-, Gloom 34-39 -/-/15%, Paras 36-37 9%/-/-, Venonat 34-35 -/-/10%, Weepinbell 34-37 15%/-/-, Exeggcute 35-38 -/15%/-, Hoothoot 33-38 -/-/15%, Spinarak 34-36 -/-/10%, Bibarel 33-35 12%/42%/-, Kricketune 35-39 -/-/5%, Foongus 35-36 -/10%/-, Amoonguss 39-41 -/10%/-, Trumbeak 35-38 20%/-/-, Grubbin 33-35 32%/-/-, Charjabug 35-38 12%/-/-, Morelull 33-38 -/-/30%, Shiinotic 36-40 -/-/5%, Salandit 33-35 -/-/10% |
| Kakori Village | Fishing (oldrod) | Carvanha 25-26 100% |
| Mynori Sea | Grass | Taillow 36-38 25%, Swellow 38-40 10%, Binacle 36-38 25%, Crabrawler 36-38 25%, Clobbopus 37-38 15% |
| Mynori Sea | Fishing (oldrod) | Remoraid 25-26 20%, Carvanha 25-26 80% |
| Deep Terajuma Jungle | Grass | Butterfree 38-41 -/6%/-, Beedrill 38-41 -/17%/-, Gloom 38-41 -/-/15%, Venonat 38-41 -/-/10%, Weepinbell 38-41 15%/-/-, Exeggcute 35 -/15%/-, Hoothoot 38-41 -/-/15%, Noctowl 39-41 -/-/2%, Spinarak 38-41 -/-/10%, Ariados 38-41 -/-/6%, Bibarel 38-41 12%/42%/-, Kricketune 39-41 -/-/5%, Foongus 38-41 -/10%/-, Amoonguss 39-41 -/10%/-, Trumbeak 38-41 29%/-/-, Grubbin 38-41 32%/-/-, Charjabug 38-41 12%/-/-, Morelull 38-41 -/-/32%, Shiinotic 39-41 -/-/5% |
| T. Excavation Site | Grass | Voltorb 33-34 20%, Electrode 33-34 15%, Ditto 33-34 10%, Nosepass 33-34 25%, Elgyem 33-34 -/-/5%, Grubbin 33-34 20%, Salandit 35-36 -/-/5%, Oranguru 33-34 5%/5%/-, Pincurchin 35-36 5%/5%/- |

*(6 more tables in this segment are Surf/fishing backtracking on earlier maps; omitted.)*


**Gifts and events:** Eevee (donate $7,000), Ducklett (an egg), Galarian Corsola (a dock event), Lotad (rain), the
**Mystery Egg** for a bred Phantump egg: one of 21 (Azurill, Impidimp, Nacli, Togepi, Sneasel, Dhelmise, Aevian Litwick,
**Axew**, Mienfoo, Pawniard, Trapinch, Hippopotas, Cottonee, Darumaka, Hatenna, Starly, **Tyrunt**, **Larvesta**,
Mareanie, Stufful, Rookidee), fixed at the start of the save.

**Answers to Valarie before her:** Grass and Electric common since segment 0–2 (Pansage 32% in Gearen Park, Cherubi 44%,
Pom-Pom Oricorio 57%, Plusle/Minun 12–13%, Yamper 30%, then Bounsweet 49%, Tangela 45%, Wattrel 35%). Valarie: "Ground
moves do nothing", three Swift Swimmers, Aquabatics. Electric moves are boosted on her field, which is the walkthrough's
advice.


### Before Gym 6 — Crawli (Bug, doubles). Jynnobi Pass, Mt. Terajuma, Helojak Island, Kakori help quests, Surf backtracking. Cap 45.

| Map | Method | Species, level, rate |
|---|---|---|
| Mynori Sea | Surfing | Mantine 35-36 10%, Carvanha 35-36 40%, Mantyke 35-36 50% |
| Mynori Sea | Fishing (goodrod) | Remoraid 35-36 20%, Octillery 35-36 10%, Carvanha 35-36 30%, Tynamo 35-36 30%, Eelektrik 35-36 10% |
| Route 5 | Grass | Krabby 37-38 35%, Exeggcute 30 10%, Beautifly 36-37 20%, Dustox 36 22% |
| Route 5 | Surfing | Krabby 35 14.56%, Carvanha 30-41 2.91%, Wailmer 35-36 6.8%, Mantyke 35-36 72.81%, Veluza 30-41 2.91% |
| Route 5 | Rock Smash | Binacle 35-38 10%, Chewtle 35 90% |
| Terajuma Jungle / Deep Terajuma Jungle | Surfing | Lotad 35-36 30%, Lombre 38-40 10%, Carvanha 35-36 50%, Sharpedo 38-40 10% |
| Terajuma Jungle / Deep Terajuma Jungle | Fishing (goodrod) | Carvanha 35-43 100% |
| Terajuma Shipyard / Terajuma Beach | Grass | Krabby 37-38 25%, Exeggcute 30-35 10%, Beautifly 36 10%, Dustox 36 10%, Pyukumuku 35-38 10%, Pincurchin 32-40 5%, Capsakid 30-36 30% |
| Terajuma Shipyard / Terajuma Beach | Surfing | Krabby 35 25%, Carvanha 30-41 5%, Wailmer 35-36 15%, Mantyke 35-36 25%, Wiglett 35-36 25%, Wugtrio 30-41 5% |
| Terajuma Shipyard / Terajuma Beach | Fishing (goodrod) | Carvanha 40-41 60%, Wailmer 40-41 20%, Wishiwashi 10 20% |
| Tyluric Temple | Surfing | Basculin (Red/Blue) 35-45 100% |
| Tyluric Temple | Fishing (goodrod) | Basculin (Red/Blue) 35-45 100% |
| Tyluric Temple (Upper Levels) | Grass | Voltorb (Hisuian) 38-43 20%, Tangela 35-43 20%, Spinarak 38-43 13.33%, Ariados 38-43 6.67%, Vigoroth 38-43 13.33%, Mawile 38-41 20%, Chatot 38-43 6.67% |
| Tyluric Temple (Upper Levels) | Surfing | Basculin (Red/Blue) 35-45 100% |
| Tyluric Temple (Upper Levels) | Fishing (oldrod/goodrod) | Basculin (Red/Blue) 35-45 100% |
| Jynnobi Pass | Grass | Corphish 33-36 10%, Crawdaunt 35-36 2%, Binacle 33-36 37%, Barbaracle 33-36 7%, Mudbray 33-36 25%, Cramorant 10-36 19% |
| Jynnobi Pass | Surfing | Mantine 35-36 3%, Carvanha 35-36 22%, Mantyke 35-36 75% |
| Jynnobi Pass | Fishing (oldrod/goodrod) | Carvanha 25-26 100%/-, Tynamo 35-36 -/100% |
| Mirimura Cave | Grass | Geodude 42-45 20%, Graveler 42-46 15%, Exeggcute 40-43 15%, Nincada 41-46 10%, Venipede 41-44 20%, Whirlipede 41-46 10%, Klawf 39-47 10% |
| Mt. Terajuma | Grass | Cubone 38-41 13.34%, Marowak 38-41 13.34%, Teddiursa 38-41 16.67%, Ursaring 38-41 13.33%, Rufflet 38-41 32.22%, Braviary 38-41 11.12% |
| Helojak Island | Grass | Farfetch'd (Galarian) 39-42 -/3.81%/15%, Tangela 39-42 4.55%/-/-, Wooper (Paldean) 39-42 13.64%/-/-, Misdreavus (Aevian) 39-42 -/1.9%/6%, Shellos (East Sea) 39-42 1.82%/1.9%/2%, Skorupi 39-42 13.64%/14.28%/32%, Croagunk 39-42 10.01%/-/5%, Carnivine 39-42 -/9.52%/-, Tympole 39-42 29.09%/-/-, Palpitoad 39-42 4.55%/9.52%/15%, Karrablast 39-42 -/35.24%/-, Stunfisk (Galarian) 39-42 13.64%/14.28%/-, Phantump 39-42 -/-/10%, Pumpkaboo 39-42 -/-/15%, Clodsire 39-42 9.1%/9.52%/- |
| Abandoned Sewers | Fishing (goodrod) | Grimer 15-16 60%, Qwilfish 15-16 20%, Skrelp 15-16 20% |
| Goldenleaf Town | Fishing (goodrod) | Wooper 25 80%, Basculin (Red/Blue) 25 20% |
| Forgotten Path | Fishing (goodrod) | Wooper 25 80%, Basculin (Red/Blue) 25 20% |

*(35 more tables in this segment are Surf/fishing backtracking on earlier maps; omitted.)*


**Gifts and events:** Riolu (a static beyond Jynnobi), Toedscool, Slakoth, a **Bulbasaur egg** (a Help Center
reward), the Aevian Mystery Egg (eight Aevian forms).

**Answers to Crawli before him:** everything is long available (Pansear 32% before gym 1, Fletchinder 14% from segment
1, Carbink and Rock from segment 1). Crawli: Sticky Web, Barbed Web poison, Swamp Field Speed drops, weakened Fire,
U-turn Golisopod, doubles.


## 4. What both games do (the principles)

**P1. The first gym's answer is withheld completely, and arrives right after the badge.**
- *Reborn:* in normal play there is no Ground type anywhere before Julia: not wild, not a gift, not an egg, not a trade
  (only a Mudkip starter evolved at 16, or a monotype password). The first two
  Ground types are "1 Badge Quests": Numel (rain + snax) and Onyx (follow the hiker). Before her you have only
  resistances (Grass) and tricks (Mud Sport deletes her Electric Terrain).
- *Rejuvenation:* looser: Drowzee (Psychic) is 31% in the Gearen Alleyway, a side area, and Geodude (Ground) is 2% in the
  sewers. Its first Normal gym (Marianette, gym 3) is the reverse case: see P2.

**P2. From the second gym on, ordinary counters exist in the wild, and the gym is built to beat them.**
- *Reborn:* Flying and Poison are common before Florinia (Grass); her Desert Field and Sand Tomb trap them. Flying and
  Rock are common before Shelly (Bug); her Prankster Rain stops Fire burning the forest. Ground is common before Aya;
  her Wasteland quarters Earthquake.
- *Rejuvenation:* Flying and Psychic are common before Keta; "almost everything has a Dark or Rock type move". Fighting
  (Makuhita 26–28%) is common a whole gym before Marianette's Normal gym; her team is Psychic Indeedee, Normal/Ghost
  Zorua, Normal/Flying Chatot and Fluffy Bewear with Aerial Ace. Ground is common before Valarie; on Water Surface
  "Ground moves do nothing".
- In both, these counters are **plain unevolved basics** at well below the cap; the gym leader is at the cap.

**P3. The best answer (the one the field doesn't blunt) is gated behind effort.**
- *Reborn:* Fire is never wild before Pyrous Mountain (segment 4, after Shade). Before Florinia and Shelly it comes only
  as Litleo (beat a Lv 35 Klinklang with the cap at 25), Numel (rain and snax), Pansear (rain), Growlithe (the police
  quest), Castform (a two-step trade chain), or a 1-in-18 Mystery Egg Vulpix or Larvesta.
- *Rejuvenation:* the strong Psychic answers to Keta come from a random Mystery Egg (Galarian Ponyta, one of three) or a
  breed-and-trade chain (Smoochum with a Twisted Spoon). Dark Zorua before the Ghost gym is a quest reward (Broken Bell).

**P4. Strong Pokémon are earned and late; early ones are random or behind a boss.**
- Pseudo-legends: **none wild in the first six gyms of either game.** Reborn's come at about Badge 14–16 (Gible, Larvitar,
  Deino, a Jangmo-o egg, Bagon, Dratini, the Beldum quest); Rejuvenation's at about Badge 12–15 (a Shadow Beldum raid at 12,
  Larvitar at 13, Gible, a Bagon gift and a Dreepy chase at 14, Deino from a quest at 15).
- The early exceptions are **random pools**: Reborn's Mystery Egg (18 lines, Axew and Larvesta among them, after a
  two-part quest at 2 badges), Rejuvenation's (21 lines incl. Axew, Tyrunt and Larvesta, fixed per save, at 4 badges).
  Reborn's guaranteed Axew egg sits in the Underroot from segment 2 but only opens with a green crystal at about Badge 8.
- **Boss fights are above the curve and pay out the baby:** Reborn's Litleo (Lv 18) after a Lv 35 Klinklang; Rejuvenation's
  Boss Spidops (Lv 18, cap 18) pays out a Lv 10 Tarountula.
- Extra starters come late and through a condition: Reborn's Squirtle (rainy fountain) and Chikorita (show a Chimecho)
  after Badge 5; Rejuvenation's Bulbasaur egg (Help Center) at 5.

**P5. Rarity tiers and conditions make finds effortful.**
- Commons 15–35%, uncommons 5–12%, rares 1–5%; evolved forms are rare (Reborn: Sunflora 5–6%, Furret 2%, Diggersby and
  Vivillon 2% in Beryl Cave; Rejuvenation: Furret 2%, Boltund 2%, Thievul 4%).
- Many early finds sit behind a condition rather than a percentage: weather (Reborn: Blitzle in thunderstorms at Lv 15,
  above the curve; Surskit, Pansear, Lotad in rain; Hoppip, Drifloon in wind; Helioptile, Tropius in sun), time of day
  (Teddiursa clear days, Grubbin/Joltik at night), an item (Reborn's snax, Rejuvenation's Gourmet Treat for Pachirisu,
  Blitzle, Munna, Lunatone, Fidough), Headbutt or Rock Smash, a chase (Reborn's Teddiursa, Rejuvenation's Nidoran).
- Several "gifts" are coin flips: Pachirisu or Zigzagoon, Minccino or Espurr, Pansear or Panpour, Grubbin or Joltik.

**P6. Variety per route, low wild levels, revisits.**
- Species per land/cave table, median by segment: Reborn 3, 6, 7, 8, 7, 6.5; Rejuvenation 8, 6, 3.5, 6, 9, 7. Most early
  maps have 6–10.
- Early wild levels sit far below the cap: Reborn segment 0 is Lv 2–15 against a cap of 20; Rejuvenation Lv 3–15 against
  18. A few rare finds sit above it (Reborn's Lv 15 Blitzle, Lv 35 Dunsparce in the Grand Stairway).
- Old maps get new things after badges: Reborn's walkthrough has "1 Badge Quests", "2 Badge Quests", "9 Badge Quests" and
  "11 Badge Quests" chapters; Rejuvenation has "14 Badge Quests" and "17 Badge Quests".


## 5. The Prismfall rule set (Chapters 0–4 applied; the same rules for the rest)

The user's direction is stricter than either reference game after their first gym, so Prismfall takes **P1 for every
gym's best answer** and P2–P6 as they are. The numbers live in `design/warden_gates.json`.

| Rule | What | Checked by |
|---|---|---|
| **R1** | **Gym 1 (Dorian, Normal): no Fighting type from any source before the badge** (Reborn's Julia rule). Ghost (immune to Normal) only as a rare wild find. The first Fighting types are "1 Badge Quests": the Timburr at the Ferrow's berth and the tide-pool duel on Lacecliff Walk. | validators (`zero`), harness |
| **R2** | **Gated answers** (a Warden's super-effective types that its field does *not* blunt) are at most **5% of a wild table and 8% in total**, on every table usable before that gym (map segment and method unlock), counting evolutions reached by level at or below the gym's cap (Fletchling → Fletchinder at 17 is a Fire answer to Tamsin; Tympole → Palpitoad at 25 is a Ground answer to Rook). | `validate_encounters.py`, `validate_badge_tiers.py` (base + every open overlay) |
| **R3** | **Blunted answers** (the field and team are built to beat them, as in P2) may stay common in the wild: Flying for Tamsin (non-Bug fliers ×0.8 on Silkwood, Joltik's spread Electroweb), Grass for Marisol (Water Surface slows grounded non-Water Pokémon, no Grassy Terrain; Pelipper, Araquanid, Gyarados). The trainer designer must keep each Warden's answer to them. | review |
| **R4** | **Nothing handed over** (gift, egg, trade, guaranteed duel, chase or static, boss reward) while the player holds *b* badges may be a type answer, gated *or* blunted, to Warden *b*+1 or *b*+2. A spar you can't catch hands nothing over. Exempt: the Prologue starter pick. | harness (recomputes *b* from quest unlocks, TALK rows and scene `:if` gates) |
| **R5** | **Answers arrive after the badge, as effort** (P1, P6): a revisit quest ("1/2 Badge Quests"), a boss above the curve, a puzzle, a weather or time condition. Moved here: Timburr, the tide-pool duel (after Badge 1); Charcadet, Litleo, the catchable Sudowoodo, Heracross/Pinsir (after Badge 2); the Wattrel (after Badge 3). | harness |
| **R6** | **Strong Pokémon are earned** (P4): a boss reward joins below the boss's level and the fight is at or above the cap; an event Pokémon carries something the area lacks (ability, move or line) but not a tailored answer (no Aerial Ace Heracross before a Bug gym, no Fire palette on a gift before Tamsin, no Ghost moves on a Protean Kecleon before Dorian). Random-pool eggs (P4) are allowed from Act II and may include one strong line among ~15. | harness (legality), review |
| **R7** | **Pseudo-legends** (Dratini, Larvitar, Bagon, Beldum, Gible, Deino, Goomy, Jangmo-o, Dreepy, Frigibax lines): **wild only from Badge 8** (the references: Badge 12–16 of 18; Prismfall meets them half-way), at most 5%, on a side or revisit map; before that only as an earned reward, **at most one per Act and never before Badge 4** (today: the Trial-by-Flames Deino egg, Chapter 8). The Act I sightings (Dratini, Beldum, Goomy at Badge 4) and the Act II base slots (Goomy, Gible, Larvitar, Beldum at Badges 3–7) became Badge-8 revisit overlays (Gabite on the Rib Road, Pupitar and Metang in the Static Tunnels, Sliggoo in the Weeping Fen). | both validators |
| **R8** | **Shape of a table** (P5, P6): 8–13 species; commons 10–20, uncommons 5–12, rares 2–5; evolved forms rare and no earlier than their evolution level − 5; early wild levels 6–12 under the cap (Chapter 1 roads Lv 3–8 under a cap of 15). Every badge adds two rare slots to old maps (`BADGE_TIERS.md`). | `validate_encounters.py` (levels, evolutions), review |
| **R9** | **Wardens 5–18:** when the trainer designer builds a Warden's team, add its `answers`, `gated` and `blunted` lists to `warden_gates.json` (gated = super-effective types its field and team do not neutralise; blunted = the kingdom's own types the Warden is built to beat, as P2). The validators and the harness then enforce R2 and R4 for it automatically. Known items for that pass: Sahar (Ground, Gym 5) meets common Isenmar Water (blunted: her team needs a Water answer), and the Bombirdier boss reward (Badge 3) is Flying, immune to Ground: blunt it (sand, Rock Slide) or move the reward. | `warden_gates.json` |


## 6. Prismfall before and after (Chapters 0–4)

"Before" = the previous Trials/early-distribution pass (Revision 14); "after" = this pass. Wild percentages are the share
of one table; every listed wild answer after the pass is the most common one on any table usable before that gym.

| Before… | Answers | Before this pass | After this pass |
|---|---|---|---|
| **Gym 1** Dorian (Normal, cap 15) | Fighting, Ghost | **Timburr gift** Lv 8 with Mach Punch and Guts (Ferrow's, Ch1); **guaranteed duel** for Iron Fist Crabrawler or Technician Clobbopus Lv 12, both with Power-Up Punch (Lacecliff Walk, Ch2); wild Heracross (Bug/Fighting) 1% by Headbutt; a Protean Kecleon with Shadow Sneak and Lick (it turns Ghost); a catchable Sudowoodo Lv 10 that "resists Normal before Dorian's gym" | **No Fighting type from any source** (Reborn's Julia rule). Ghost: Sandygast 2–3% on Marram Down. Kecleon keeps Protean but has no Ghost moves; the Sudowoodo is a spar you can't catch. Timburr and the duel are 1 Badge Quests (Lv 13–14). |
| **Gym 2** Tamsin (Bug, double, cap 19) | Fire, Rock (gated); Flying (blunted by Silkwood) | Gifts: **Charcadet** Lv 6 (Ch1), **Wattrel** Lv 7 (Ch1), **Sudowoodo** (Ch1), **Litleo** boss Lv 17 joining at 15 (Saltmere, after B1), Smeargle with an **Ember/Will-O-Wisp** palette, Moxie **Heracross with Aerial Ace** / Pinsir duel (Gossamer Wood, before the gym), **Litwick** from the manor (map). Wild: Fletchling 10%, Rolycoly 10%, Litleo 8%, Ponyta 8%, Sizzlipede 8%, Dwebble 10%, Nacli 8–12%, Brinecut Mine Rock 39% (1F) and 56% (B1F) | No Fire, Rock or Flying gift: Charcadet, Litleo, the catchable Sudowoodo and Heracross/Pinsir come after Badge 2, the Wattrel after Badge 3, the manor gives Sinistea (map request), Smeargle's palettes are sea/night/dawn/earth. Wild gated answers: 9 species, none above 4% (Litleo, Sizzlipede, Rolycoly 3%; Fletchling, Ponyta, Nacli, Dwebble, Roggenrola, Aron 4%); the mine's Rock types moved to Rock Smash (Badge 2) and its Badge-2 overlay. Flying stays common (Pidove 17%, Hoothoot 20%, Combee 45% by Headbutt). |
| **Gym 3** Marisol (Water, cap 23) | Electric (gated); Grass (blunted by Water Surface) | Gift: **Wattrel** (Electric/Flying, Ch1). Wild: Joltik 12% (Cocoonfall) and 10% (Rimewood Glade), Shinx 8%, Blitzle 8%, Grubbin 8% (Charjabug at 20), Tynamo 8% | No Electric gift (the Wattrel waits on the Ebbmouth mast until Badge 3). Wild Electric 4–5%: Joltik 5%, Mareep 4–5%, Shinx, Blitzle, Grubbin, Tynamo 4%. Grass stays common: it is Elowen's own type, and Marisol's field and team (Pelipper, Araquanid, Gyarados) are built for it. |
| **Gym 4** Rook (Electric, cap 27) | Ground | Wild: Geodude 50% (Brinecut Rock Smash) and 15% (Cave), Barboach 25–30% (Good Rods), Tympole 20% and Stunfisk 20% (Reedholms rods), Sandygast 8–15%, Nincada 15%, Wooper 10%, Swinub 6–8%, Diglett 8%, Bunnelby 7% | Ground 2–5% on every table before Rook (rods included). |
| **Pseudo-legends** | — | Badge-4 sightings in Act I (Dratini, Beldum, Goomy) and base slots from Badge 3 (Goomy, Reedholms), 4 (Gible, Larvitar, Beldum), 5–7 (Gible, Beldum, Goomy, Gabite) | Wild from Badge 8 only (R7); Act II's early slots became Badge-8 revisit overlays. |
| **New base tables** | — | 527, 528, 552, 566, 577, 578 had overlays but no base table | All six written to the rules (8–12 species, rare answers, levels under the cap). |

### Requests this pass makes
- **Map builder** (`mapgen/REQUESTS.md`): the Thistledown Manor's Litwick gift → Sinistea; the Glassed Orchard Carbink becomes a
  glimpse before Badge 2 and a catchable Lv 20 static after it; the Ebbmouth harbour-mast Wattrel event (`EBB_MAST`); the
  Gossamer sap-tree duel only after Badge 2; the Dovetail nest stays until the Wattrel leaves.
- **Trainer designer:** what is available when (table above and `POKEMON_AVAILABILITY.md` §2a); Dorian now meets no
  Fighting types but every Fighting starter (Monferno at 14); the Little Crucible gauntlet moved to the 2-badge band (cap 23);
  each Warden keeps an answer to its blunted counters (R3); gates for Wardens 5–18 when their teams are built (R9).
