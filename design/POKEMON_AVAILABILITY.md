# POKÉMON AVAILABILITY — Velmora (Gen 1–9, base project PBS)

Source of truth for wild slots is `pbs/encounters.txt` (132 tables, 0 errors / 0 warnings under `python3 -I tools/validate_encounters.py`).
Regenerate §5–6 with `--summary`; list every answer to the early Wardens with `--gates`. This file adds what encounters can't express: gifts, statics, fossils, legendaries and design intent.
**SPINE Revision 16** governs distribution: `design/DISTRIBUTION_STUDY.md` (the Reborn/Rejuvenation study and rules R1–R9), numbers in `design/warden_gates.json`.

## 1. Rules used
- **No answers to the next Warden before the gym (R1–R5).** A Warden's *answers* are the types that hit it super-effectively or are immune to it. Gym 1 (Dorian, Normal): **no Fighting type at all before the badge** and Ghost only as a rare find (Marram Down Sandygast, 2–3%), Reborn's Julia rule. From Gym 2 on, the *gated* answers (those the Warden's field does not blunt: Tamsin Fire/Rock, Marisol Electric, Rook Ground) are **at most 5% of a table and 8% in total** on every table usable before that gym, counting evolutions reached by level under its cap. *Blunted* answers stay common because the field and team are built to beat them (Flying vs Silkwood, Grass vs Water Surface), as in both references. Nothing **handed over** (gift, egg, trade, duel, chase, boss reward) answers the next two Wardens; answers come right after the badge, as revisit quests. The validators and `tools/harness/run_trials.rb` enforce all of this.
- **Kingdom flavour:** Land/Cave tables on kingdom maps are ≥65% (target 70%) that kingdom's types. The validator enforces this. Borderland routes mix both kingdoms. Set pieces are exempt (Thistledown Manor, Unown Script Vault, Lantern Isle, Aurelia, Inverted Ward).
- **Borderlands (Rev 9):** borderland maps mix both kingdoms' types ≈50/50 and are the places where blend species live. Rimewood (Elowen/Isenmar): Snover, Snom, Cubchoo, Stantler, Deerling, Smoochum. Cinderglass Barrens/Petrified Ashwood (Ashkaar/Ossaria): Carkol, Magcargo, Vibrava, Sudowoodo. Rootdeep (Nadir/Elowen): Foongus, Parasect, Toedscruel. Thornwar Marches (Elowen/Ashkaar): Scovillain, Volcarona. Obsidian Barrows (Antumbra/Ossaria): Palossand, Golurk, Claydol, Runerigus. Full list: WORLD.md §10.
- **Power curve:** wild max ≤ the next level cap, accounting for when the map is reachable and when the encounter method unlocks (Good Rod 3, Rock Smash 2, Surf 6, Super Rod 10 badges). So early-map Water/Super Rod tables are level-30s/40s on revisit. An evolved form never appears more than 5 levels before its evolution level. Stone, trade and friendship evolutions don't appear wild before Lv 20. Early roads sit well under the cap, as in both references (Chapter 1: Lv 3–8 against a cap of 15).
- **Shape (R8):** 8–13 species per table; commons 10–20, uncommons 5–12, rares 2–5. Every badge adds two rare slots to maps already walked (`BADGE_TIERS.md`).
- **Pseudo-legends (R7):** wild only from **Badge 8**, rare, on side or revisit maps (both references: about Badge 13 of 18). Before that only as earned rewards, at most one per Act and never before Badge 4 (Act III: the Trial-by-Flames Deino egg). Badge-8 revisits: Gabite on the Rib Road, Pupitar and Metang in the Static Tunnels Depths, Sliggoo in the Weeping Fen, Shelgon in the Cinderhorn Caldera; base tables from Badge 8: Dratini (Prism Falls rods), Jangmo-o (Grudgestone), Frigibax and Bagon (Frostfang), Deino (Darkglass, 13), Dreepy (the Noonless Road as Drakloak, 14).
- **Imprinted variants** = regional forms, found only in Bleed zones or near their Imprint: Galarian Stunfisk and Alolan Diglett (Sinkfield), Alolan Grimer, Galarian Corsola and Galarian Weezing (Mirefen area), Alolan Marowak, Galarian Darumaka and Alolan Vulpix (Emberfall: "the fire burns cold"), Galarian Farfetch'd (The Rootdeep, for Sirfetch'd), Alolan Sandshrew/Vulpix (The Hoarwood), Galarian Mr. Mime (Frostfang/Stillwater), Galarian Slowpoke (Dreaming Quarter), Galarian Linoone (Hindmoor, for Obstagoon), Galarian Meowth (The Slag Mesa, for Perrserker), Pom-Pom Oricorio (Conductors' Causeway/Spire roof), Alolan Exeggutor (Lantern Isle, Bride Grove). Velmora must be town-map **region 0** (WORLD §1), or Essentials re-forms some species on evolution.
- **Paradox Pokémon** appear wild only postgame (Shardfall Isles, "Prism echoes").

## 2. Starters & gifts (story gifts; quest and event Pokémon are in `EVENT_POKEMON.md`)
| When | Where | Gift | Revision 16 |
|---|---|---|---|
| Prologue | Larch's lab | any Gen 1–9 starter (Core starter picker) | exempt (the one free pick, as in both references) |
| after B1 | Pell Playhouse | Eevee "Understudy" Lv 10; Eeveelution stones sold from Lumen on | Normal: no answer to Tamsin or Marisol |
| after B1 | Saltmere playhouse (stage magician) | Abra Lv 12 (no wild Abra line) | Psychic: no answer to Bug or Water |
| Ch3 | Thistledown Manor, after the three scenes | **Sinistea** Lv 14 (was Litwick: Fire is Tamsin's answer; `mapgen/REQUESTS.md`) | Litwick stays a Badge-2 overlay in the manor |
| Ch1 | the Glassed Orchard | Carbink: a glimpse only before Badge 2, catchable Lv 20 after it (map request) | Rock answers Tamsin |
| after B2 | the Dyers' Ford dye-master | Pansear (red vat) **or** Panpour (blue vat); Pansage (yellow vat) only after B5 | Pansear is Fire (Tamsin's answer), so the dyer waits for Badge 2; Pansage is Grass (Marisol, and Sahar once her gates are set, R9) |
| after B4 | Lumen Fossil Lab | revives Old Amber (Brinecut B1F) → Aerodactyl Lv 25. Dome/Helix found in Ossuary | |
| after B6 | Mirefen ward | starter egg: player picks any **Grass** starter not chosen | check against Wardens 7–8 when their gates are set (R9) |
| after B9 | Verdance (Juno) | starter egg: any **Fire** starter | (R9) |
| after B12 | Lucent (Ilsa's aide) | starter egg: any **Water** starter | (R9) |
| after B13 | Cragholm museum | revival of all 10 fossil items found in Act IV (Root/Claw/Skull/Armor/Cover/Plume/Jaw/Sail + Galar fossil halves → Dracozolt/Arctozolt/Dracovish/Arctovish) | |
| Act III branch | 699 Meridian Black Site (Meridian Standing) | Type: Null **promised** (NULL CRADLE KEY); **collected in the postgame** (`PG_TYPENULL`) (Meridian's artificial-Judgment prototype). Memories found across the Bleed zones | |
| Postgame | Ironreach dojo (`PG_KUBFU`) | Kubfu (moved out of Act IV: no legendary joins the party in the main story) | |
| Act III | Royal Chase warden | Riolu egg | |

Evolution notes: **trade evolutions** use the Linking Cord (Lumen Dept. 2F). Pawmot, Brambleghast and Rabsca are `Level,100` placeholders in the Gen 9 Pack PBS (their real walk/step methods are scripted), so they are also placed wild at s9–s11. Kingambit, Annihilape, Dudunsparce, Farigiraf, Archaludon, Dipplin/Hydrapple, Kleavor, Ursaluna and Wyrdeer come from evolving their wild pre-evolutions; Core must confirm those methods work (Gen 9 Pack).

Quest-reward and event Pokémon (chases, boss rewards, rival duels, kindness gifts; 44 in all, 9 in Chapters 0–2, only Nickit and Kecleon before Gym 1, plus a Sudowoodo spar you can't catch yet) are listed with the badge count each needs in `design/EVENT_POKEMON.md` (data: `plugins/Prismfall Trials/13x_EventMons_*.rb`). Badge-gated rarer spawns on revisited maps: `design/BADGE_TIERS.md` and `pbs/encounters_badgetiers.txt`.

### 2a. Chapters 0–4 at a glance (what the player can have before each Warden)
| Before | Wild answers (gated ≤5% each) | Common but blunted | Handed over (quests, gifts, bosses) |
|---|---|---|---|
| **Gym 1** Dorian (Normal; Fighting, Ghost) | Fighting: **none**. Ghost: Sandygast 2–3% (Marram Down) | — | Nickit (chase, Dark), Kecleon (lantern search, Protean, no Ghost moves), a Sudowoodo spar (can't be caught) |
| **Gym 2** Tamsin (Bug; Fire, Rock, Flying) | Litleo 3% (Windfall Row), Rolycoly 3% and Fletchling 4% (Ferrymen's Mile), Sizzlipede 3% (Gossamer), Ponyta 4% (Thistledown Lea), Nacli/Dwebble 4% (Marram Down, Grey Saltings), Nacli/Roggenrola/Aron 4% (Brinecut); the mine's Rock types are behind Rock Smash (Badge 2) | Flying: Pidove 17%, Hoothoot 20%, Pikipek 13–15%, Wingull 15%, Combee 45% (Headbutt) | after Badge 1: Timburr (Mach Punch), Crabrawler or Clobbopus, Smeargle (sea/night/dawn/earth), Ralts, Galarian Ponyta, Eevee, Abra |
| **Gym 3** Marisol (Water; Electric, Grass) | Shinx 4%, Blitzle 4%, Grubbin 4% (Charjabug at 20), Mareep 4–5%, Joltik 5%, Tynamo 4%; **Emolga 5% at night in the secret Rimewood Glade** (563, behind the Cut sapling; the Fire starter's earned answer) | Grass: all of Elowen (Gossamer, Briarwick, the Lea, the Ford) | after Badge 2: Charcadet, Litleo (boss), Sudowoodo, Heracross or Pinsir, Spidops (boss), Snom, Ditto |
| **Gym 4** Rook (Electric; Ground) | Diglett, Bunnelby, Sandygast, Silicobra, Nincada, Swinub, Wooper, Tympole, Barboach (rods), Stunfisk (Good Rod), Geodude (Rock Smash): each 2–5% | — | after Badge 3: Bombirdier (boss), Wattrel "Mast" (Ebbmouth mast) |

## 3. Statics (non-legendary)
Rotom Lv 25 (Sluiceworks Turbine Hall) · Greavard Lv 16 (Thistledown attic, after the ghost-girl quest) · Spiritomb Lv 33 (Ossuary, Odd Keystone + 32 Bleed-zone NPC talks) · Larvesta egg (The Cinderhorn Caldera hermit) · Carbink glimpse in the Glassed Orchard (scripted, not catchable) · Gimmighoul coins hunt (Antumbra) → Gholdengo.

## 4. Legendary arcs, one per kingdom (multi-bar boss battles; levels at or below the cap)
**Rule (Reuben, 2026-11-23):** no legendary, mythical, sub-legendary, UB or Paradox Pokémon is caught or gifted in the main story. Every story legendary is an uncatchable boss (`:catch => false`). Captures and gifts happen in the postgame legendary network (`gemini_recommends/2026-11-23_gen6-9-sprites-postgame-legendaries-dorian-meloetta`, Part B). Enforced in code: Prismfall Core `027_LegendaryGate.rb` (`Prismfall.legendary_catch_allowed?`) deflects every Poké Ball thrown at a wild Legendary / Mythical / Sub-Legendary / UB / Paradox (and Type: Null, Silvally, Kubfu, Urshifu) until S160 POSTGAME.
| Kingdom | Legendary | Where / when | Lv |
|---|---|---|---|
| Elowen | **Okidogi, Munkidori, Fezandipiti** (Act III, Royal Chase / Bride Grove) → **Ogerpon** (Act V, Gloamwood) | the "Masked Ogre and the Three Loyal" folktale (Briarwick old woman foreshadows) | 46 / 78 |
| Isenmar | **Kyogre** (Whalebone Keep Ice Vault 308, under Lake Rime, after the thaw) | Act IV revisit | 66 |
| Zenith | **Zekrom** (Stormwatch Spire roof, storm event) | Act III | 58 |
| Nadir | **Pecharunt** (Lightless Deep B1F; its poison chains mirror the Gilded Chain) | Act V | 78 |
| Ashkaar | **Reshiram** (Wyrmscar Depths; truth to Zekrom's ideals) | Act V | 84 |
| Ossaria | **Groudon** (Duneholt Undersands; boss, not catchable; `:GROUDON_UNDERSANDS`). Regirock (Stonesleep braille) moves to the postgame (`PG_REGIS`) | Act IV | 66 |
| Antumbra | **Giratina** (Reverse Depths 806, Act IV boss; Origin form postgame at the Distortion Core 910) | Act IV | 70 |
| Crownhaven | **Arceus** (true finale boss; catchable on the Good ending's postgame) | Festival | 100 |
Postgame (Hallow Strait, Shardfall Isles, Bleed rifts, Battle Tower rewards): the Kanto/Galar birds, the Beasts, Lugia/Ho-Oh, Latios/Latias (roaming), Regice/Registeel/Regieleki/Regidrago/Regigigas, the Lake trio (Lucent lakes), Dialga/Palkia, Heatran (The Cinderhorn), Cresselia/Darkrai, the Swords and Forces of Nature, Xerneas/Yveltal/Zygarde cells, Tapus, Cosmog → Solgaleo/Lunala, Necrozma, the Ultra Beasts ("Bleed rifts" lore), Zacian/Zamazenta/Eternatus, Calyrex + steeds, the Treasures of Ruin, Koraidon/Miraidon, Terapagos. Mythicals are event/password unlocks.

## 5. Wild families first available, by badges held (base tables; badge-tier overlays add more, see BADGE_TIERS.md)

- **0** (59): AIPOM, BOUNSWEET, BUNEARY, BUNNELBY, BURMY, CHERUBI, COMBEE, CORPHISH, CUTIEFLY, DWEBBLE, FIDOUGH, FINNEON, FLETCHLING, GOSSIFLEUR, HOOTHOOT, HOPPIP, HORSEA, ILLUMISE, KRABBY, KRICKETOT, LECHONK, LILLIPUP, LITLEO, MAGIKARP, MEOWTH, MINCCINO, MUNCHLAX, NACLI, NICKIT, NIDORANfE, NIDORANmA, NOIBAT, NYMBLE, ODDISH, PIDGEY, PIDOVE, PIKIPEK, PINECO, POOCHYENA, RATTATA, ROLYCOLY, ROOKIDEE, SANDYGAST, SHELLOS, SHINX, SILICOBRA, SKWOVET, SMOLIV, SPINARAK, SQUAWKABILLY, TANDEMAUS, TAROUNTULA, TENTACOOL, VOLBEAT, WIGLETT, WINGULL, WOOLOO, YUNGOOS, ZIGZAGOON
- **1** (63): ARON, AZURILL, BASCULIN, BIDOOF, BLIPBUG, BLITZLE, BUDEW, CATERPIE, COTTONEE, CRABRAWLER, DIGLETT, DODUO, DUCKLETT, DUSKULL, FLABEBE, FOONGUS, GASTLY, GOLDEEN, GREAVARD, GRUBBIN, HERACROSS, KARRABLAST, MACHOP, MANKEY, MAREEP, MAWILE, MEDITITE, MISDREAVUS, MORELULL, PANCHAM, PATRAT, PETILIL, PHANTUMP, PINSIR, PONYTA, PURRLOIN, REMORAID, ROGGENROLA, SABLEYE, SCATTERBUG, SEEDOT, SENTRET, SEWADDLE, SHELMET, SHROOMISH, SHUPPET, SINISTEA, SIZZLIPEDE, SKIDDO, SNUBBULL, SPEAROW, STUNKY, SUNKERN, SURSKIT, TIMBURR, TYMPOLE, VAROOM, VENONAT, WEEDLE, WHISMUR, WOOBAT, WURMPLE, ZUBAT
- **2** (68): AUDINO, BERGMITE, BINACLE, CASTFORM, CETODDLE, CHATOT, CLOBBOPUS, CORSOLA, CRAMORANT, CRYOGONAL, CUBCHOO, DEERLING, DELIBIRD, DEWPIDER, DITTO, DUNSPARCE, DURANT, EEVEE, EISCUE, EMOLGA, FURFROU, GEODUDE, GIRAFARIG, GLAMEOW, INDEEDEE, JOLTIK, KANGASKHAN, KECLEON, KLAWF, LARVESTA, LEDYBA, MAREANIE, MILTANK, MIMEJR, NINCADA, ORICORIO, PARAS, POLIWAG, PORYGON, RELLOR, SCYTHER, SEEL, SHUCKLE, SKITTY, SKORUPI, SLOWPOKE, SMEARGLE, SMOOCHUM, SNEASEL, SNOM, SNORUNT, SNOVER, SPHEAL, SPINDA, SPRITZEE, STANTLER, SWABLU, SWINUB, TAILLOW, TAUROS, TEDDIURSA, TYNAMO, VANILLITE, WIMPOD, WISHIWASHI, WOOPER, YANMA, ZORUA
- **3** (42): ALOMOMOLA, ARROKUDA, BARBOACH, BRUXISH, BUIZEL, CARVANHA, CHEWTLE, CHINCHOU, CLAMPERL, CLAUNCHER, CROAGUNK, CUFANT, DEDENNE, ELEKID, FEEBAS, FERROSEED, FINIZEN, FRILLISH, GRIMER, KLINK, KOFFING, LOTAD, LUVDISC, MAGNEMITE, MINUN, ORTHWORM, PACHIRISU, PAWMI, PLUSLE, PSYDUCK, QWILFISH, SHELLDER, SKRELP, STARYU, STUNFISK, TADBULB, TOGEDEMARU, TOXEL, TRUBBISH, VOLTORB, WATTREL, YAMPER
- **4** (19): BALTOY, BRONZOR, CACNEA, DRIFLOON, ELECTRIKE, FLAMIGO, GOLETT, HEATMOR, HIPPOPOTAS, LITWICK, PHANPY, PICHU, ROCKRUFF, RUFFLET, SANDILE, SANDSHREW, SIGILYPH, TRAPINCH, VULLABY
- **5** (17): CUBONE, DRILBUR, EKANS, GLIMMET, GULPIN, HELIOPTILE, HONEDGE, LUNATONE, MAKUHITA, MARACTUS, MASCHIFF, MUDBRAY, ONIX, SHROODLE, SOLROCK, UNOWN, YAMASK
- **6** (27): BELLSPROUT, CAPSAKID, CARNIVINE, CHARCADET, COMFEY, DRAMPA, EXEGGCUTE, FOMANTIS, HOUNDOUR, KOMALA, MANTYKE, MINIOR, NUMEL, ORANGURU, PANSEAR, PASSIMIAN, PYUKUMUKU, SALANDIT, SCRAGGY, SEVIPER, STUFFUL, TOEDSCOOL, TROPIUS, TURTONATOR, VENIPEDE, WAILMER, ZANGOOSE
- **7** (15): BONSLY, CYCLIZAR, DARUMAKA, DRUDDIGON, GLIGAR, GROWLITHE, MAGBY, MIENFOO, RHYHORN, SAWK, SKARMORY, SLUGMA, THROH, TORKOAL, VULPIX
- **8** (23): ANNIHILAPE, BOUFFALANT, BRAMBLIN, CHINGLING, CLEFFA, DRATINI, FALINKS, FARFETCHD, HAPPINY, IGGLYBUFF, IMPIDIMP, JANGMOO, KLEFKI, LARVITAR, LICKITUNG, MILCERY, PAWNIARD, RIOLU, STONJOURNER, SWIRLIX, TANGELA, TOGEPI, TYROGUE
- **9** (7): APPLIN, BAGON, BELDUM, DHELMISE, FRIGIBAX, LAPRAS, PUMPKABOO
- **10** (13): ABSOL, AERODACTYL, ARCTOVISH, ARCTOZOLT, BOMBIRDIER, CARBINK, HAWLUCHA, MURKROW, NATU, RELICANTH, STARLY, TATSUGIRI, VELUZA
- **11** (13): ARCHEN, ELGYEM, ESPURR, FLITTLE, GIMMIGHOUL, GOTHITA, HATENNA, INKAY, RALTS, SOLOSIS, SPOINK, TINKATINK, WYNAUT
- **12** (4): DROWZEE, DURALUDON, MUNNA, NOSEPASS
- **13** (11): AMAURA, ANORITH, CRANIDOS, DEINO, GIBLE, KABUTO, LILEEP, OMANYTE, SHIELDON, TIRTOUGA, TYRUNT
- **14** (3): DREEPY, MIMIKYU, POLTCHAGEIST
- **15** (2): DRACOVISH, PINCURCHIN
- **16** (2): MORPEKO, SLAKOTH
- **17** (3): AXEW, DRACOZOLT, GOOMY
- **18** (1): ROTOM
- **PG** (15): BRUTEBONNET, DONDOZO, FLUTTERMANE, GREATTUSK, IRONBUNDLE, IRONHANDS, IRONJUGULIS, IRONMOTH, IRONTHORNS, IRONTREADS, IRONVALIANT, ROARINGMOON, SANDYSHOCKS, SCREAMTAIL, SLITHERWING

## 6. Families with a member of each type, cumulative (badges 0 / 4 / 8 / 12 / 18)

- BUG: 11 / 39 / 40 / 40 / 41
- DARK: 5 / 18 / 24 / 28 / 30
- DRAGON: 2 / 5 / 11 / 16 / 24
- ELECTRIC: 1 / 25 / 26 / 27 / 31
- FAIRY: 2 / 12 / 20 / 24 / 25
- FIGHTING: 0 / 13 / 26 / 28 / 28
- FIRE: 3 / 10 / 23 / 23 / 23
- FLYING: 13 / 39 / 47 / 55 / 55
- GHOST: 1 / 16 / 21 / 24 / 28
- GRASS: 7 / 25 / 35 / 38 / 40
- GROUND: 6 / 21 / 31 / 31 / 32
- ICE: 0 / 19 / 19 / 23 / 24
- NORMAL: 22 / 53 / 66 / 67 / 68
- POISON: 5 / 23 / 31 / 31 / 31
- PSYCHIC: 0 / 15 / 22 / 37 / 37
- ROCK: 3 / 12 / 22 / 27 / 36
- STEEL: 3 / 16 / 23 / 28 / 29
- WATER: 9 / 50 / 53 / 58 / 62

## 7. Families with no wild slot (all covered by §2–4)
All 27 Gen 1–9 starter lines (starter picker + 3 starter eggs; the Festival bracket rival teams use others), Abra and the Pansage/Panpour monkeys (gifts), Spiritomb (static), and the evolution-only Gen 8–9 species listed in §2.
