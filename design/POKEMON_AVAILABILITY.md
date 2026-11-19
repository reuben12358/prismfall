# POKÉMON AVAILABILITY — Velmora (Gen 1–9, base project PBS)

Source of truth for wild slots is `pbs/encounters.txt` (126 tables, 0 errors / 0 warnings under `python3 -I tools/validate_encounters.py`).
Regenerate the coverage lists below with `--summary`. This file adds what encounters can't express: gifts, statics, fossils, legendaries and design intent.

## 1. Rules used
- **Kingdom flavour:** Land/Cave tables on kingdom maps are ≥65% (target 70%) that kingdom's types. The validator enforces this. Borderland routes mix both kingdoms. Set pieces are exempt (Thistledown Manor, Unown Script Vault, Lantern Isle, Aurelia, Inverted Ward).
- **Borderlands (Rev 9):** borderland maps mix both kingdoms' types ≈50/50 and are the places where blend species live. Rimewood (Elowen/Isenmar): Snover, Snom, Cubchoo, Stantler, Deerling, Smoochum. Cinderglass Barrens/Petrified Ashwood (Ashkaar/Ossaria): Carkol, Magcargo, Vibrava, Sudowoodo. Rootdeep (Nadir/Elowen): Foongus, Parasect, Toedscruel. Thornwar Marches (Elowen/Ashkaar): Scovillain, Volcarona. Obsidian Barrows (Antumbra/Ossaria): Palossand, Golurk, Claydol, Runerigus. Full list: WORLD.md §10. Phanpy moved from Frostflat Causeway to the Brass Dunes, and Farfetch'd (both forms) and Lickitung from the Rootdeep to the Royal Chase.
- **Power curve:** wild max ≤ the next level cap, accounting for when the map is reachable and when the encounter method unlocks (Good Rod 3, Rock Smash 2, Surf 6, Super Rod 10 badges). So early-map Water/Super Rod tables are level-30s/40s on revisit. An evolved form never appears more than 5 levels before its evolution level. Stone, trade and friendship evolutions don't appear wild before Lv 20.
- **Variety (Reborn-like):** 61 families at 0 badges (Elowen's Bug/Normal/Grass/Flying, with Litleo/Sizzlipede/Rolycoly/Fletchling as the Gym 2 (Bug) answers; for the Normal Gym 1, Fighting types come from the Strand Road: the Tide-Pool Feud Crabrawler/Clobbopus on Lacecliff Walk (527) and the Last Plank Timburr in Ferrow's Landing, see design/EVENT_POKEMON.md) and about 330 by the end. By 4 badges every type has ≥6 families. See §6.
- **Pseudo-legends** are rare (2–5%) one act before they're usable: Goomy s3 (The Reedholms), Gible s4 (The Rib Road), Larvitar s4 (Static Depths), Beldum s4–5, Dratini s8 (Prism Falls rods), Jangmo-o s8 (Grudgestone), Frigibax s9 (Frostfang), Bagon s9–10, Deino s13 (Darkglass), Dreepy s14 (The Noonless Road as Drakloak).
- **Imprinted variants** = regional forms, found only in Bleed zones or near their Imprint: Galarian Stunfisk and Alolan Diglett (Sinkfield), Alolan Grimer, Galarian Corsola and Galarian Weezing (Mirefen area), Alolan Marowak, Galarian Darumaka and Alolan Vulpix (Emberfall: "the fire burns cold"), Galarian Farfetch'd (The Rootdeep, for Sirfetch'd), Alolan Sandshrew/Vulpix (The Hoarwood), Galarian Mr. Mime (Frostfang/Stillwater), Galarian Slowpoke (Dreaming Quarter), Galarian Linoone (Hindmoor, for Obstagoon), Galarian Meowth (The Slag Mesa, for Perrserker), Pom-Pom Oricorio (Conductors' Causeway/Spire roof), Alolan Exeggutor (Lantern Isle, Bride Grove). Velmora must be town-map **region 0** (WORLD §1), or Essentials re-forms some species on evolution.
- **Paradox Pokémon** appear wild only postgame (Shardfall Isles, "Prism echoes").

## 2. Starters & gifts
| When | Where | Gift |
|---|---|---|
| Prologue | Larch's lab | any Gen 1–9 starter (Core starter picker) |
| after B1 | Saltmere (Eevee breeder) | Eevee Lv 10, with Eeveelution stones sold from Lumen on (SPINE Rev 14: Eevee "Understudy" now comes with Badge 1) |
| after B1 | Saltmere playhouse (stage magician) | Abra Lv 12 (no wild Abra line) |
| Act I | Briarwick dyer | one of Pansage / Pansear / Panpour (Pansear also wild on Lake Sallow) |
| after B4 | Lumen Fossil Lab | revives Old Amber (Brinecut B1F) → Aerodactyl Lv 25. Dome/Helix found in Ossuary |
| after B6 | Mirefen ward | starter egg: player picks any **Grass** starter not chosen |
| after B9 | Verdance (Juno) | starter egg: any **Fire** starter |
| after B12 | Lucent (Ilsa's aide) | starter egg: any **Water** starter |
| after B13 | Cragholm museum | revival of all 10 fossil items found in Act IV (Root/Claw/Skull/Armor/Cover/Plume/Jaw/Sail + Galar fossil halves → Dracozolt/Arctozolt/Dracovish/Arctovish) |
| Act III branch | 699 Meridian Black Site (Meridian Standing) | Type: Null Lv 50 (Meridian's artificial-Judgment prototype). Memories found across the Bleed zones |
| Act IV | Ironreach dojo (any branch) | Kubfu Lv 60 (Undercity, i.e. Nadir, pit-fighting lineage) |
| Act III | Royal Chase warden | Riolu egg |

Evolution notes: **trade evolutions** use the Linking Cord (Lumen Dept. 2F). Pawmot, Brambleghast and Rabsca are `Level,100` placeholders in the Gen 9 Pack PBS (their real walk/step methods are scripted), so they are also placed wild at s9–s11. Kingambit, Annihilape, Dudunsparce, Farigiraf, Archaludon, Dipplin/Hydrapple, Kleavor, Ursaluna and Wyrdeer come from evolving their wild pre-evolutions; Core must confirm those methods work (Gen 9 Pack).

Quest-reward and event Pokémon (chases, boss rewards, rival duels, kindness gifts; 43 in all, 12 in Chapters 0-2 and 8 of those before Gym 1) are listed in `design/EVENT_POKEMON.md` (data: `plugins/Prismfall Trials/13x_EventMons_*.rb`). Badge-gated rarer spawns on revisited maps: `design/BADGE_TIERS.md` and `pbs/encounters_badgetiers.txt`.

## 3. Statics (non-legendary)
Rotom Lv 25 (Sluiceworks Turbine Hall) · Greavard Lv 16 (Thistledown attic, after the ghost-girl quest) · Spiritomb Lv 33 (Ossuary, Odd Keystone + 32 Bleed-zone NPC talks) · Larvesta egg (The Cinderhorn Caldera hermit) · Carbink glimpse in the Glassed Orchard (scripted, not catchable) · Gimmighoul coins hunt (Antumbra) → Gholdengo.

## 4. Legendary arcs, one per kingdom (multi-bar boss battles; levels at or below the cap)
| Kingdom | Legendary | Where / when | Lv |
|---|---|---|---|
| Elowen | **Okidogi, Munkidori, Fezandipiti** (Act III, Royal Chase / Bride Grove) → **Ogerpon** (Act V, Gloamwood) | the "Masked Ogre and the Three Loyal" folktale (Briarwick old woman foreshadows) | 46 / 78 |
| Isenmar | **Kyogre** (Whalebone Keep Ice Vault 308, under Lake Rime, after the thaw) | Act IV revisit | 66 |
| Zenith | **Zekrom** (Stormwatch Spire roof, storm event) | Act III | 58 |
| Nadir | **Pecharunt** (Lightless Deep B1F; its poison chains mirror the Gilded Chain) | Act V | 78 |
| Ashkaar | **Reshiram** (Wyrmscar Depths; truth to Zekrom's ideals) | Act V | 84 |
| Ossaria | **Groudon** (Duneholt Undersands) + **Regirock** (Stonesleep braille) | Act IV | 64 |
| Antumbra | **Giratina** (Reverse Depths 806, Act IV boss; Origin form postgame at the Distortion Core 910) | Act IV | 70 |
| Crownhaven | **Arceus** (true finale boss; catchable on the Good ending's postgame) | Festival | 100 |
Postgame (Hallow Strait, Shardfall Isles, Bleed rifts, Battle Tower rewards): the Kanto/Galar birds, the Beasts, Lugia/Ho-Oh, Latios/Latias (roaming), Regice/Registeel/Regieleki/Regidrago/Regigigas, the Lake trio (Lucent lakes), Dialga/Palkia, Heatran (The Cinderhorn), Cresselia/Darkrai, the Swords and Forces of Nature, Xerneas/Yveltal/Zygarde cells, Tapus, Cosmog → Solgaleo/Lunala, Necrozma, the Ultra Beasts ("Bleed rifts" lore), Zacian/Zamazenta/Eternatus, Calyrex + steeds, the Treasures of Ruin, Koraidon/Miraidon, Terapagos. Mythicals are event/password unlocks.

## 5. Wild families first available, by badges held (validator output)

- **0** (61): AIPOM, BLIPBUG, BOUNSWEET, BUDEW, BURMY, CATERPIE, CHERUBI, COMBEE, CUTIEFLY, FIDOUGH, FINNEON, FLETCHLING, FOONGUS, GOSSIFLEUR, GRUBBIN, HERACROSS, HOOTHOOT, KARRABLAST, KRICKETOT, LECHONK, LILLIPUP, LITLEO, MAGIKARP, MEOWTH, MORELULL, MUNCHLAX, NICKIT, NIDORANfE, NIDORANmA, NYMBLE, ODDISH, PETILIL, PHANTUMP, PIDGEY, PIDOVE, PIKIPEK, PINECO, PINSIR, POOCHYENA, RATTATA, ROLYCOLY, ROOKIDEE, SCATTERBUG, SEEDOT, SEWADDLE, SHELMET, SHINX, SHROOMISH, SIZZLIPEDE, SKWOVET, SMOLIV, SPINARAK, SQUAWKABILLY, TAROUNTULA, TENTACOOL, VENONAT, WEEDLE, WOOLOO, WURMPLE, YUNGOOS, ZIGZAGOON
- **1** (65): ARON, BIDOOF, BLITZLE, BUNEARY, BUNNELBY, COTTONEE, CRABRAWLER, DEERLING, DEWPIDER, DIGLETT, DODUO, DURANT, DUSKULL, DWEBBLE, EEVEE, FLABEBE, GASTLY, GEODUDE, GOLDEEN, GREAVARD, HORSEA, ILLUMISE, JOLTIK, LARVESTA, LEDYBA, MACHOP, MANKEY, MAWILE, MINCCINO, MISDREAVUS, NACLI, NINCADA, NOSEPASS, PANCHAM, PARAS, PATRAT, POLIWAG, PONYTA, PURRLOIN, RELLOR, REMORAID, ROGGENROLA, SABLEYE, SANDYGAST, SCYTHER, SENTRET, SHUCKLE, SHUPPET, SINISTEA, SKIDDO, SKORUPI, SNOM, SNUBBULL, SPEAROW, STUNKY, SUNKERN, SURSKIT, TANDEMAUS, TIMBURR, TYMPOLE, VOLBEAT, WHISMUR, WOOBAT, YANMA, ZUBAT
- **2** (55): AUDINO, AZURILL, BASCULIN, BERGMITE, BINACLE, CASTFORM, CETODDLE, CHATOT, CLOBBOPUS, CORSOLA, CRAMORANT, CRYOGONAL, CUBCHOO, DELIBIRD, DITTO, DUCKLETT, DUNSPARCE, EISCUE, FURFROU, GIRAFARIG, GLAMEOW, INDEEDEE, KANGASKHAN, KECLEON, KLAWF, KRABBY, MAREANIE, MILTANK, MIMEJR, ORICORIO, PORYGON, SEEL, SKITTY, SLOWPOKE, SMEARGLE, SMOOCHUM, SNEASEL, SNORUNT, SNOVER, SPHEAL, SPINDA, SPRITZEE, STANTLER, SWINUB, TAILLOW, TAUROS, TEDDIURSA, TYNAMO, VANILLITE, WIGLETT, WIMPOD, WINGULL, WISHIWASHI, WOOPER, ZORUA
- **3** (46): ALOMOMOLA, ARROKUDA, BARBOACH, BRUXISH, BUIZEL, CARVANHA, CHEWTLE, CHINCHOU, CLAMPERL, CLAUNCHER, CORPHISH, CROAGUNK, CUFANT, DEDENNE, ELEKID, FEEBAS, FERROSEED, FINIZEN, FRILLISH, GOOMY, GRIMER, KLINK, KOFFING, LOTAD, LUVDISC, MAGNEMITE, MINUN, ORTHWORM, PACHIRISU, PAWMI, PLUSLE, PSYDUCK, QWILFISH, SHELLDER, SHELLOS, SKRELP, STARYU, STUNFISK, TADBULB, TOGEDEMARU, TOXEL, TRUBBISH, VAROOM, VOLTORB, WATTREL, YAMPER
- **4** (25): BALTOY, BELDUM, BRONZOR, CACNEA, DRIFLOON, ELECTRIKE, FLAMIGO, GIBLE, GOLETT, HEATMOR, HIPPOPOTAS, LARVITAR, LITWICK, MAREEP, NOIBAT, PHANPY, PICHU, ROCKRUFF, RUFFLET, SANDILE, SANDSHREW, SIGILYPH, SILICOBRA, TRAPINCH, VULLABY
- **5** (17): CUBONE, DRILBUR, EKANS, GLIMMET, GULPIN, HELIOPTILE, HONEDGE, LUNATONE, MAKUHITA, MARACTUS, MASCHIFF, MUDBRAY, ONIX, SHROODLE, SOLROCK, UNOWN, YAMASK
- **6** (27): BELLSPROUT, CAPSAKID, CARNIVINE, CHARCADET, COMFEY, DRAMPA, EXEGGCUTE, FOMANTIS, HOUNDOUR, KOMALA, MANTYKE, MINIOR, NUMEL, ORANGURU, PANSEAR, PASSIMIAN, PYUKUMUKU, SALANDIT, SCRAGGY, SEVIPER, STUFFUL, TOEDSCOOL, TROPIUS, TURTONATOR, VENIPEDE, WAILMER, ZANGOOSE
- **7** (15): BONSLY, CYCLIZAR, DARUMAKA, DRUDDIGON, GLIGAR, GROWLITHE, MAGBY, MIENFOO, RHYHORN, SAWK, SKARMORY, SLUGMA, THROH, TORKOAL, VULPIX
- **8** (25): ANNIHILAPE, BOUFFALANT, BRAMBLIN, CHINGLING, CLEFFA, DRATINI, FALINKS, FARFETCHD, HAPPINY, HOPPIP, IGGLYBUFF, IMPIDIMP, JANGMOO, KLEFKI, LICKITUNG, MEDITITE, MILCERY, PAWNIARD, RIOLU, STONJOURNER, SWABLU, SWIRLIX, TANGELA, TOGEPI, TYROGUE
- **9** (6): APPLIN, BAGON, DHELMISE, FRIGIBAX, LAPRAS, PUMPKABOO
- **10** (13): ABSOL, AERODACTYL, ARCTOVISH, ARCTOZOLT, BOMBIRDIER, CARBINK, HAWLUCHA, MURKROW, NATU, RELICANTH, STARLY, TATSUGIRI, VELUZA
- **11** (14): ARCHEN, ELGYEM, EMOLGA, ESPURR, FLITTLE, GIMMIGHOUL, GOTHITA, HATENNA, INKAY, RALTS, SOLOSIS, SPOINK, TINKATINK, WYNAUT
- **12** (3): DROWZEE, DURALUDON, MUNNA
- **13** (10): AMAURA, ANORITH, CRANIDOS, DEINO, KABUTO, LILEEP, OMANYTE, SHIELDON, TIRTOUGA, TYRUNT
- **14** (3): DREEPY, MIMIKYU, POLTCHAGEIST
- **15** (2): DRACOVISH, PINCURCHIN
- **16** (2): MORPEKO, SLAKOTH
- **17** (2): AXEW, DRACOZOLT
- **18** (1): ROTOM
- **PG** (15): BRUTEBONNET, DONDOZO, FLUTTERMANE, GREATTUSK, IRONBUNDLE, IRONHANDS, IRONJUGULIS, IRONMOTH, IRONTHORNS, IRONTREADS, IRONVALIANT, ROARINGMOON, SANDYSHOCKS, SCREAMTAIL, SLITHERWING

## 6. Families with a member of each type, cumulative (badges 0 / 4 / 8 / 12 / 18)

- BUG: 21 / 39 / 40 / 40 / 41
- DARK: 5 / 19 / 24 / 28 / 30
- DRAGON: 0 / 6 / 13 / 18 / 24
- ELECTRIC: 2 / 24 / 25 / 27 / 31
- FAIRY: 3 / 12 / 20 / 24 / 25
- FIGHTING: 2 / 12 / 26 / 28 / 28
- FIRE: 4 / 10 / 23 / 23 / 23
- FLYING: 13 / 36 / 46 / 55 / 55
- GHOST: 1 / 16 / 21 / 24 / 28
- GRASS: 14 / 24 / 35 / 38 / 40
- GROUND: 2 / 23 / 32 / 32 / 32
- ICE: 0 / 19 / 19 / 23 / 24
- NORMAL: 18 / 52 / 66 / 67 / 68
- POISON: 10 / 23 / 31 / 31 / 31
- PSYCHIC: 1 / 15 / 23 / 37 / 37
- ROCK: 1 / 14 / 23 / 27 / 36
- STEEL: 4 / 18 / 25 / 28 / 29
- WATER: 3 / 50 / 53 / 58 / 62


## 7. Families with no wild slot (all covered by §2–4)
All 27 Gen 1–9 starter lines (starter picker + 3 starter eggs; the Festival bracket rival teams use others), Abra and the Pansage/Panpour monkeys (gifts), Spiritomb (static), and the evolution-only Gen 8–9 species listed in §2.
