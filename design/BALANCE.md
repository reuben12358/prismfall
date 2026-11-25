# Prismfall — Battle Balance & Trainer Data

Owner: balance / trainer-data lead. Data: `pbs/trainer_types.txt`, `pbs/trainers.txt` (ship as `*_prismfall.txt`).
Validator: `python3 -I tools/validate_trainers.py [--summary] [--strict]` (reference = `/home/claude/ref/ebdx/PBS`, Gen 1–9).
`--learnset SPECIES[,FORM] [LEVEL]` prints every legal move — use it when editing sets.

Binding inputs: SPINE (Rev 1–3), `story/03_CAST.md` (ace concepts — all honoured), `design/FIELDS.md` (Gyms 1–7 fields
are defined; Gyms 8–18 fields are designed to their theme, assumptions marked **[assume]**), `design/SYSTEMS.md` (Core).

---

## 1. Difficulty philosophy

| | Casual (`v+200`) | Standard (`v`) | Hard (`v+100`) |
|---|---|---|---|
| Feel | Approachable: learn the field, win on the second try at worst | Fair but demanding: you must use the field and type matchups; overlevelling to the cap is expected | Reborn-hard: the field is a weapon pointed at you; expect to build counter-teams and lose a few times |
| Team size | Standard −1 (min 2); Festival always 6 | see §3 | Standard +1 (max 6) |
| Levels | Standard −2 (cap <40), −3 (<70), −4 (70+); the story's important fights (Wardens but Brann, rivals, villains, Festival) one more from cap 40, two from cap 80, three at the Festival (90+) (round 4) | Ace **at the cap**, others 1–5 below | Same as Standard through cap 23; from cap 27, others +1 (never above cap) (harness: +1 at Gyms 1–3 cost prepared teams 10–15 points) |
| IVs / EVs | IV 4→20 by tier, **EV 0** | IV 12 / 18 / 24 / 28 / 31 (caps ≤23 / ≤35 / ≤51 / ≤71 / 72+), default EVs (min(lv×1.5, 85) each) | IV Standard + 8 (20 to cap 23, 26 to cap 35), 31 from cap 39 (Trick Room mons Spe IV 0); 252/252/4-style EVs by role, **at most 6 × level per stat** (60 at Lv 10, the full 252 from Lv 42) |
| Sets | Standard sets minus the nastiest tool (setup / sleep / signature ability swapped, e.g. Toxapex Limber, Araquanid-free); from cap 40 no Life Orb or Choice item on the important fights (round 4) | Full sets: 4 moves, ability, item, nature; field-synergy core of each team is present. Round 4: no team carries more than two copies of its field's boosted signature attack, and the one-Pokémon sweep tools (Choice Band + Reckless, Scarf Outrage, Unburden + coverage, a seed on top of a setup move) are Hard's | Upgraded coverage, Hidden Abilities, Choice/Life Orb/Weakness Policy, one extra synergy piece. **Megas (all modes, §6b):** every important fight from ace 50 has one; below that only designed weak ones (Std + Hard) |
| Bag items | Standard −1 | 1 Potion (cap 15) → 1 Super (to 23) → 2 Super → 2 Hyper → 2 Full Restore | 2 Super → 2 Hyper → 2 → 3 Full Restore |
| AI skill | trainer type's own (Core sets no ceiling) | trainer type's own | Core floor 48 (`ai_skill_min`) |

Rules of thumb used when writing teams:
- **Every team has one "field engine"** (the mon that turns the field on or abuses it hardest) and **one honest answer** the
  player can learn from the field notes (e.g. Ground moves short out Neon Grid; Rain/Surf quench Volcanic).
- Standard never uses: OHKO moves, evasion abilities (Sand Veil/Snow Cloak), Moody, Baton Pass chains, sleep + Dream
  Eater loops, Shadow Tag. Hard may use Shadow Tag (Gothitelle) and Perish trapping (Mega Gengar) once each.
- Moves learned "early" (by level-up above the mon's level) are allowed only on Hard. The validator warns about them
  (28 Hard-only warnings at the moment, all intentional); Standard and Casual have zero.

## 1b. Calibration against Reborn and Rejuvenation (round 3)

Read from the games' own compiled data (`Data/trainers.dat`; Rejuvenation also `trainers_story.dat` / `bossdata*.dat`),
cross-checked with the BigJra walkthroughs. Version 0 = the normal-mode team.

| Fight | Reborn | Rejuvenation | Prismfall Standard (Hard / Casual) |
|---|---|---|---|
| First rival | Victoria: Litten Lv 5, Scratch / Growl | Ren: Froakie Lv 5, Pound / Growl, IV 4 | K1 Kestrel: the advantage starter Lv 5, **no type move** (Hard: type move + Starly; Casual Lv 3) |
| Gym 1 | Julia: **6**, Lv 12–15, 2 Potions, IV 10 (20–24 on three), real natures; Charge / Charge Beam on Electric Terrain, Explosion, Rollout | Venam: **6**, Lv 13–16, Potion, IV 20, three Oran Berries + a Normal Gem; Fake Out, Encore, Spikes | Dorian: **6**, Lv 9–14, Potion, IV 12 (Meloetta IV 0 / EV 0 and the ×0.80 Act One Matinee), Oran ×4 + Quick Powder; Fake Out, Pay Day, Encore, Illusion, Transform, Relic Song, Sing (Hard 6, IV 20, Sash / Synthetic Seed / Imposter / Protean; Casual 4) |
| Gym 2 | Florinia: 6, Lv 22–24, 2 Super, Telluric Seed, Spore, Leech Seed, Spikes, Sandstorm | Keta: 6, Lv 22–25, 2 Super, IV 20 (ace 31), Charcoal, Black Belt, Coba | Tamsin (**double**): 4, Lv 14–19, Super, IV 12, Telluric Seed; Rain Dance + Electroweb (Hard 5: + Vivillon, Focus Sash, Eviolite) |
| Gym 3 | Corey: 6, Lv 26–30, 2 Super, Focus Sash, Telluric Seed, Black Glasses | Marianette: 6, Lv 27–29, 2 Super, Plates, Focus Sash, Leftovers | Marisol: 4, Lv 19–23, Super, Oran Berries (Hard 5) |
| Gym 4 | Shelly: 6, Lv 31–35, 2 Hyper, Damp Rock, Silver Powder, Leftovers, Telluric Seed | Narcissa: 6, Lv 33–35, Super, Magical Seeds, Eviolite, a Plate | Rook: 4, Lv 25–27, 2 Super, Magnet, Synthetic Seed (Hard 5) |
| Second rival | Victoria 1: 4, Lv 18–19, 2 Potions, IV 30–31, Wise Glasses, Eviolite | Ren: 4, Lv 13–16, Potion (team id 7: 2 at Lv 19–20, IV 31, Sitrus, Wacan) | K2 Kestrel: 4, Lv 21–23, Super, Telluric Seed (Hard 5, Eviolite) |

**Reading.** The references bring six Pokémon from Gym 1 on, two to five levels under the ace, with real natures, a
berry or gem on most, and one or two field plays per team. Prismfall matches them on sets, items, natures and plays
(Standard IV 12 sits between Reborn's default 10 and Rejuvenation's 20), and runs **smaller teams at the same pace**,
because (1) our level cap is hard, so the player cannot out-level a six-Pokémon wall the way a Reborn player grinds
past Florinia; (2) our early fields are stronger per move (Grand Stage ×1.3–1.5 on every Normal move from turn 1,
Silkwood ×1.5 on spread Electroweb); and (3) in the harness a realistic team already wins only ~50 / 40 / 25% of
Gyms 1–3 on Standard, and a fifth Pokémon for Tamsin dropped hers to 13%. Hard goes past the references where they
are soft: perfect-ish IVs, EV spreads, the extra Pokémon, Focus Sash / Eviolite / seeds, and no Bag in trainer
battles; its team size matches Reborn at Gym 1 (6). Casual stays well under them on purpose.

## 1c. Calibration against Reborn and Rejuvenation, mid and late game (round 4)

Same sources and method as §1b (`Data/trainers.dat`, read with `python3 -I`; the leader that hands out the badge
at the same badge count; Rejuvenation's order from the BigJra walkthrough's badge lines). "Cap" = the level cap the
player holds going in (Reborn `[20, 25, 35, 40, 45, 50, 55, 60, 65, 70, 70, 75, 75, 80, 85, 90, 90, 95]`,
Rejuvenation `[18, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 85, 90, 90, 100]`). EV "def" = the engine's
default (min(1.5 × level, 85) each, the same rule in all three games); "508" = a 252/252/4-style spread.

| Badges held | Reborn (normal) | Rejuvenation (normal) | Prismfall Standard (Hard) |
|---|---|---|---|
| 3 (our Gym 4) | Shade: 6, Lv 35–38 / cap 40, IV 25–31, EV def, 6/6 held (2 seeds, Wide Lens), 2 Hyper | Narcissa: 6, 33–35 / 35, IV 20–31, def, 5/6 (2 Magical Seeds, Plate, Eviolite), 1 Super | Rook: 4, 25–27 / 27, IV 18, def, 4/4 (Synthetic Seed, Magnet), 2 Super (Hard 5, IV 26, 252s) |
| 5 (Gym 6) | Serra: 6, 47–50 / 50, IV 15–31, def + one 508, 6/6, 3 Hyper | Crawli (double): 6, 43–45 / 45, IV 31, def / 504, 6/6 (2 Telluric Seeds, a Crest), 2 Hyper | Corvin (double): 5, 33–35 / 35, IV 18, def, 5/5 (Synthetic Seed), 2 Hyper (Hard 6) |
| 7 (Gym 8) | Radomus: 6, 57–60 / 60, IV 31 (TR), def + 508, 6/6, 2 Ultra | Amber: 6, 53–55 / 55, IV 31, def / 504 / 508, 6/6 (seed, Gem, 2 Balloons) | Kaito: 5, 41–43 / 43, IV 24, def, 5/5 (Synthetic Seed, Assault Vest, Flame Orb), 2 Hyper (Hard 6, IV 31) |
| 9 (Gym 10) | Samson: 6, 66–71 / 70, IV 23–31, 508, 6/6 (3 Synthetic Seeds, Life Orb, Sash), 2 Ultra | Flora: 6, 64–68 / 65, IV 31, 488–512, 6/6 (2 Magical Seeds), **Mega Venusaur**, 2 Max | Anja: 6, 49–51 / 51, IV 24, def, 6/6, **Mega Glalie**, 2 Full Restore (Hard IV 31, 252s, 3 FR) |
| 12 (Gym 13) | Ciel: 6, 75–78 / 75, IV 31, 508, 6/6, **Mega Altaria**, 3 Ultra | Adam: 6, 79–83 / 80, IV 31, 504 / 508, 6/6 (seed, Gem, Sash), **Mega Aerodactyl** | Bastian: 6, 61–63 / 63, IV 28, def, 6/6 (Magical Seed, AV), **Mega Aerodactyl**, 2 FR |
| 15 (Gym 16) | Amaria: 6, 86–92 / 90, IV 31, 508, 6/6, a **Z-crystal** (her other team: **Mega Swampert**), 2–3 Ultra | Allen & Alice (double): 6 + 6, 90–92 / 90, IV 31, 508, **Mega Gardevoir / Grimmsnarl** | Nyx (double): 6, 73–75 / 75, IV 31, def, 6/6 (Magical Seed), **Mega Absol**, 2 FR |
| 16 (Gym 17) | Hardy: 6, 90–97 / 90, IV 31, 508, (rematch id 1: 6/6, **Mega Aerodactyl**, 2 FR) | — (18 badges; the finale is Damien: 6, 78–82, IV 31, 508, **Mega Tyranitar**) | Celestine (double): 6, 78–80 / 80, IV 31, def, Mimikyu's **Z-move**, 2 FR; Sigrun (17): 6, 83–85 / 85, **Mega Salamence** |
| Rival, mid game | Cain 4: 5, Lv 44–46, IV 15–31, 1 held; Victoria 4: 5, 37–41, IV 20–31, 4/5 held | Ren (Gym 6 stretch): 6, 42–44, IV 20–31, 6/6 (Sash, seed, Boots) | K4 Kestrel (7 badges): 5, 41–42 / 43, IV 24, def, 5/5 (Hard 6) |
| Rival, late game | Victoria 2: 6, 73–77, IV 31, 508, 6/6; Cain 6: 6, 81–83, 508 | Ren is a partner by then | K6 (13 badges): 6, 64–66 / 67, IV 28; K7 (16): 6, 77–79 / 80, IV 31 |

**Reading.** At every badge count from 3 on, both references bring **six** Pokémon at cap−5 .. cap+2 with **IV 31
from about Gym 5–6 and 508-EV spreads from about Gym 8–9**, almost every Pokémon holding something (seeds, Sash,
Assault Vest, Life Orb, Crests), two or three Hyper / Ultra / Max Potions, and a leader Mega from badge 9 (Rejuvenation)
or 12 (Reborn). Prismfall Standard sits **under** them on the stat side all the way (IV 18 → 24 → 28 → 31 by cap, never
an EV spread; 4–5 Pokémon until Gym 10) and **with** them on items, sets, the bag and the Mega timing (from Gym 10, as
Rejuvenation). Hard matches the references' normal mode on IVs, EVs and team size (IV 31 from cap 39, 252/252
spreads, six from Gym 6) and adds sharper sets and the Bag ban. So Standard is already a little softer than both
games' normal modes; what makes its late fights hard for an unprepared team is the field (every Warden's own type
×1.2–1.5 on the field, often with a second boost, e.g. Hurricane ×1.44 and never missing on the Stormfront), which is
also how the references' late leaders play.

## 2. Level curve

Double battles (story, SPINE Rev 14): **Gyms 2, 6, 11, 16, 17** (`GYMS[:double]`; `Prismfall.gym_battle` sets the rule).
Gym 1 (Dorian) is always a single battle. Doubles carry the same team sizes as the table below.

Wardens: ace = cap (validator-enforced on Standard/Hard). The curve between caps assumes ~4 levels per gym:
route trainers sit at **previous cap → cap−3**, gym trainers at **cap−4 → cap−2**, wild routes at **previous cap −3 → cap−5**.
The level cap (Core) means grinding past the cap is impossible, so Standard difficulty comes from sets, not levels.

| Gym | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Cap / ace | 15 | 19 | 23 | 27 | 31 | 35 | 39 | 43 | 47 | 51 | 55 | 59 | 63 | 67 | 71 | 75 | 80 | 85 |
| Std size | 5 | 4 | 4 | 4 | 4 | 5 | 5 | 5 | 5 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 6 |
| Hard size | 6 | 5 | 5 | 5 | 5 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 6 |
| Casual size | 3 | 3 | 3 | 3 | 3 | 4 | 4 | 4 | 4 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 |

Rival max levels (Standard; Hard same top, others +1 from cap 27): K1 5 · J1 15 (Saltmere, before Gym 1 since SPINE Rev 14) · K2 23 · K3 35 (round 4; was 33) · J2 35 (was 33) · K4 42 · J3 47 · K5 54 · K6 66 ·
K7 79. Festival aces (coordinator, SPINE Rev 3): R16 **90** · QF **92** · SF **94** · Final **96** · Hijack **100** · Arceus **100**;
rest of each team 1–4 below. (Casual Festival teams keep 6 mons at −4 levels.) Sister-game cameos are optional sidequest fights
(SPINE Rev 4) — see §6.

## 3. AI skill per trainer class (`trainer_types.txt`)

v21.1 tiers: 1–31 basic (uses Pokémon in order), 32+ adds switching + HP awareness, 48+ high-skill scoring, 100+ adds
ReserveLastPokemon. Skill is per **trainer type**, so difficulty scaling is done by Core (`ai_skill_min` 48 on Hard).

| Class | SkillLevel | BaseMoney |
|---|---|---|
| Wardens 1–18 (Dorian and Tamsin raised from 48 in round 3: ReserveLastPokemon keeps the ace for last), `LEADER_JUNO` | 100 | 100 |
| `RIVAL_KESTREL` | 100 | 60 |
| `RIVAL_JUNO` | 64 | 60 |
| `CHAMPION_VALEN`, `MERIDIAN_VOSS`, `FESTIVAL_*` | 100 | 150 |
| `HOLLOW_MOURNER` | 100 | 120 |
| Named admins `HOLLOW_WICK/THISTLE/TEO/SABLE`, `MERIDIAN_MARCHETTI/KROLL/ASHE` | 100 | 80 |
| `HOLLOW_ADMIN`, `MERIDIAN_ADMIN` | 64 | 70 |
| `HOLLOW_GRUNT(_M/_F)`, `MERIDIAN_AGENT(_M/_F)` | 32 | 40 |

Generic route trainers (from the base PBS) keep their stock skill. BGMs are stock base-project files
(`Battle Gym Leader`, `Battle Elite`, `Battle Champion`, `Battle trainer`, victory tracks) — swap for custom music later.

## 4. Warden teams and field play (Standard roster; **+Hard** = Hard-only mon, *(−C)* = cut on Casual)

**Revision 10 re-tune.** Every team below was rebuilt against the v1.1 fields (seeds, always-on abilities, transition
plays, an answer to the obvious flip). The reasoning for each team (game plan, transition play, counterplay) is in
**`design/TRAINER_FIELD_PLAYBOOK.md`**; this list is the roster. The old **[assume]** notes are gone: every field is
implemented. Cross-check with `python3 -I tools/trainer_gen/field_fit.py` (see the playbook).

Kingdoms (Rev 3): Elowen = Gyms 1, 2, 9, 17 · Isenmar = 3, 10 · Zenith = 4, 11, 15 · Ossaria = 5, 13 · Nadir = 6, 8, 16 ·
Ashkaar = 7, 18 · Antumbra = 12, 14.

| # | Warden, field, cap | Team (ace last) | Seed / field pick | Transition or stage play |
|---|---|---|---|---|
| 1 | **Dorian**, Grand Stage, 15, single (SPINE Rev 14); opening stage 1–3 from the Saltmere audience (Rev 19); Reuben's locked troupe (2026-11-23) | Smeargle 9, Chatot 11, Hisuian Zorua 11, Ditto 11 *(−C)*, Kecleon 12 *(−C)*, **Meloetta 14** (ace) | none on Standard (Hard: Smeargle Sash, Zorua Synthetic Seed, Imposter Ditto, Protean Kecleon) | Fake Out and Pay Day (showpieces), Relic Song (sound) raise the applause; Sing never misses at Standing Ovation; stalling lowers it. Relic Song takes the Normal boost only (no sound double stack); Meloetta is the 1-bar `:DORIAN_MELOETTA_MATINEE` (×0.80 / Hard ×0.85 / Casual ×0.78) |
| 2 | **Tamsin**, Silkwood, 19, **double** (Rev 14) | Joltik 14, Surskit 15, **+Hard** Vivillon (Rage Powder), Dwebble 16 *(−C)* (the bird answer: Smack Down, Rock Tomb), Swadloon "Bobbin" 19 | Bobbin: Telluric Seed (Hard: Eviolite) | lead pair: Rain Dance wets the silk for Electroweb (spread); Rain douses a Wildfire |
| 3 | Marisol, Water Surface, 23 | Pelipper 19 (Keen Eye; Hard Tailwind), Chinchou 20 *(−C)* (Hard Lanturn), **+Hard** Dewpider, Buizel 20 (Hard Floatzel), Gyarados "Lucky" 23 | none (Oran / Sitrus) | no Dive (the Water Surface ↔ Underwater loop strikes ×1.3 both ways: 103 knockouts in 60 runs); Lucky's Whirlpool ×2 traps |
| 4 | Rook, Neon Grid, 27 | Luxio, Electabuzz *(−C)*, **+Hard** Heliolisk, Toxtricity, Rotom-Wash "Camera" | Electabuzz: Synthetic Seed | Charge reboots a Blackout |
| 5 | Sahar, Desert, 31 | Hippopotas, **+Hard** Dugtrio, Sandaconda *(−C)*, Krokorok, Claydol "Effigy" | Sandaconda: Telluric Seed | sandstorm or Fire Fang bakes a Superbloom back |
| 6 | Corvin, Corrosive Mire, 35, **double** | Galarian Weezing (never Misty Surge), Crobat *(−C)*, **+Hard** Salazzle, Amoonguss, Drapion, Toxapex "Ward" | Crobat: Synthetic Seed | Weezing's Heat Wave ×2 → Wasteland |
| 7 | Brann, Volcanic, 39 | Torkoal, Camerupt *(−C)* (Magma Armor; **Mega**, Std + Hard, §6b: kept as designed, per the user), **+Hard** Centiskorch, Magmortar, Arcanine, Coalossal "Anvil" | Camerupt: Elemental Seed (the Cameruptite while it Megas) | Lava Plume ×3 re-melts Cinderglass; Anvil is built for Cinderglass |
| 8 | Kaito, Colosseum, 43 | Hawlucha, **+Hard** Medicham, Machamp, Hitmontop *(−C)*, Conkeldurr, Lucario "Memory" (Std Scope Lens; Hard Life Orb; Mega only at the Festival) | Hawlucha: Synthetic Seed (+ Unburden on Hard; Standard Limber since round 4) | Frenzy by knockouts |
| 9 | Juno (J3), Flower Garden, 47 | see §5 | Whimsicott: Telluric Seed | growth moves; regrow from Embers |
| 10 | Anja, Frozen Lake, 51 | Alolan Ninetales, Cloyster *(−C)*, **Glalie (Mega**, replaces Beartic), Walrein, Avalugg, Mamoswine "Matriarch" | Matriarch: Elemental Seed (Hard: Life Orb) | Body Press / High Horsepower crack the lake → Water Surface; Ice moves refreeze |
| 11 | Odessa, Stormfront, 55, **double** | Pelipper (Keen Eye, Tailwind), **Pidgeot "Post" (Mega**, replaces Swanna), Pom-Pom Oricorio *(−C)*, Noivern, **Kilowattrel** (replaces Talonflame), Corviknight "Taxi" | Oricorio: Elemental Seed | Noivern's Sunny Day ×2 → Rainbow |
| 12 | Ilsa, Mindscape, 59 | Bronzong, **Slowbro (Mega**, Trick Room; replaces Musharna), Espeon, Gothitelle *(−C)* (Hard: Shadow Tag), Reuniclus, Hatterene "Hush" | — | Hush's Psychic Noise ×3 → Inverse; Calm Mind ×2 calms a Nightmare |
| 13 | Bastian, Crystal Cavern, 63 | Carbink, Alolan Golem *(−C)*, Aurorus, **Aerodactyl "Amber" (Mega**, replaces Dusk Lycanroc), Rhyperior, Gigalith "Geode" (Sturdy, no Sand Stream) | Geode: Magical Seed (Hard: Weakness Policy + Meteor Beam) | Golem's Explosion or 3 quakes → Cave; light moves relight a Dark Crystal |
| 14 | Ysolde, Hollow Cathedral, 67 | Sableye (**Std/Casual Mega**), Spiritomb *(−C)*, Dusknoir, Cofagrigus, Gengar (**Hard Mega + Perish Song**), Chandelure "Vigil" | Cofagrigus: Magical Seed | Curse / Destiny Bond re-haunt a consecrated nave |
| 15 | Magnus, Factory, 71 | Ferrothorn, Excadrill *(−C)* (Mold Breaker), Kingambit, Klinklang "Mark One", Scizor, Metagross "Engine" (**Mega**, every mode) | none since round 4 (Mark One: Sitrus, Shift Gear) | Magnet Rise + Wild Charge restart a Scrapyard; nobody quakes |
| 16 | Nyx, New Moon, 75, **double** | Grimmsnarl, Weavile, **Absol "Omen" (Mega**, replaces Malamar), Umbreon (Wish), Zoroark "Nobody" (slot 5, Illusion of Honchkrow), Honchkrow *(−C)* | Weavile: Magical Seed (opens the Abyss) | Night Daze ×3 → Abyss; Dark attacks snuff the Lamplight |
| 17 | Celestine, Fairy Tale, 80, **double** | Alcremie, Mimikyu (**Z-move**: Mimikium Z, Rev 23), Azumarill *(−C)*, Tinkaton, Togekiss "Vigilant", **Sylveon "Vow"** (ace, per 03_CAST) | Alcremie: Magical Seed | Fairy attacks ×3 tame a roused Dragon's Den |
| 18 | Sigrun, Dragon's Den, 85 | Flygon, Kommo-o, **Dragonite** *(−C)* (Multiscale; replaces Goodra), Haxorus, Dragapult, Salamence "Dreamwing" (**Mega**, every mode) | Dreamwing: Amulet Coin (status-proof in the Den) | Draco Meteor reopens a cooled Cave; Dragon attacks retake a Fairy Tale |

## 4b. Route and gym trainers (stock trainer types)

Built from the Map Builder's events (`maps_out/Data/*.rxdata` / `trainers_needed.txt`). Rules: no bag items, level-up
movesets (always level-legal), IV 8 Standard / 20 Hard / 0 + EV 0 Casual, Casual −1 level, Hard +1 level.
**Field touches (Rev 10):** one or two per team for the map's default field (ability the field switches on, a boosted
level-up move, rarely a seed); see the table in TRAINER_FIELD_PLAYBOOK.md §2 and the per-map notes in `tools/trainer_gen/routes.py`.
Levels (SPINE Rev 14 order: Ferrow's Landing → coast → Saltmere (Gym 1) → inland → Briarwick (Gym 2) → north → Ebbmouth;
set per **map id** in `routes.py` `PLAN`, provisional until `design/SWAP_GYM1_GYM2.md`): 520 4–6 · 541 coast 8–10 ·
544/545 Brinecut Mine 9–12 · Pell Playhouse (Gym 1) 10–13 · Pageant Hall grunts 15–16 · 540 15–17 · 546 Thistledown 16–17 ·
521 15–16 · Gossamer Wood 16–18 · Loomhouse (Gym 2) 15–17 · Deepwood 19–20 · 560–564 and Tidelock unchanged; species from `encounters.txt` for that map,
leaning Bug/Grass/Normal/Fairy (Elowen). `[YOUNGSTER,Ben]` (map 990 test dummy, Snorlax Lv 50) collides with the base
project's sample Ben — ours normally compiles later and wins, but packaging should drop the base sample trainers.
**Generic villains** (`HOLLOW_GRUNT_M/F`, `MERIDIAN_AGENT_M/F`, name "Grunt"/"Agent"): version = encounter number
(0 = Saltmere Pageant Hall tag battle, then 1, 2, ... in story order; < 100), +100/+200 as usual. Map events must pass
the version. Named admins (Thistle v0 = Briarwick before Gym 2, Lv 16–18) use 0, 1, 2 ... per rematch.
Re-check map references any time with `python3 -I tools/validate_map_trainers.py` (every battle form: TrainerBattle.start,
rival/gym/cameo battles, trainer intros; also stock trainers and difficulty variants) or `tools/validate_trainers.py --maps maps_out/Data`.

## 5. Rivals (Prismfall Core swaps the Gen 1 starter; ability slot is kept, so `AbilityIndex = 2` = hidden ability)

Starter written per slot: **Kestrel** (advantage) slot 0→Charmander line, 1→Squirtle, 2→Bulbasaur; **Juno** (weak to
player) 0→Squirtle, 1→Bulbasaur, 2→Charmander. Stage: K1 base · K2–K3, J1–J2 middle · K4+, J3+ final. Std uses
`AbilityIndex = 0`; **Hard K5–K8 and J4 use `AbilityIndex = 2`** (hidden: Speed Boost / Protean / Libero / Intimidate ...).

| | Team (Standard; ace last) |
|---|---|
| K1 (6) | starter (Hard +Starly) |
| K2 (21) | Staravia *(−C)*, Honedge "Morwen" (Ch4 gift), starter — Hard +Sandile |
| K3 (35) | Staravia, Scyther *(−C)* (round 4: on Standard too), Krokorok *(−C)*, Doublade (Eviolite), starter |
| K4 (42) | Staraptor, Krookodile *(−C)*, Scizor, Doublade, starter — Hard +Zweilous |
| K5 (54) / K6 (66) | Staraptor, Krookodile *(−C)*, Scizor, Zweilous→Hydreigon (K6), starter, **Aegislash "Morwen"** |
| K7 (79) / K8 (94) | Staraptor, Krookodile *(−C)*, **Mismagius** (from Ysolde), Hydreigon, starter, **Aegislash** ace |
| J1 (14) | Cottonee *(−C)*, Bounsweet "Sweetpea", starter (unevolved) — Hard +Petilil. Saltmere, before Gym 1 (Rev 14) |
| J2 (35) | Whimsicott, Floette "Everbloom" *(−C)* (white, SPINE Rev 12; round 4: on Standard too), Lilligant *(−C)*, Steenee, starter |
| J3 (47, `LEADER_JUNO` 30–32) | Whimsicott (Telluric Seed), Florges "Everbloom" *(−C)* (white, Flower Veil), Lilligant, starter, ace **Tsareena** — Hard +Roserade "Rowan". Flower Garden: the seed, Growth, Leech Seed, Aromatherapy and Grassy Terrain grow the garden; burn it down with Fire at stage 5. |
| J4 (90) | Florges "Everbloom", Whimsicott, Lilligant, Comfey, starter, **Tsareena** |

**Rival partners (2026-11-25).** A rival who fights *beside* the player with a team of their own uses the spare versions
of a decade: `Prismfall::Rival.partner_version(n)` = n × 10 + 3 + starter slot, one version (no Hard / Casual block; Core
falls back to it). Redeemed Kestrel in the Ch21 tag battle is `partner_version(9)` = **93 / 94 / 95**: Staraptor 95
(Tailwind), his starter 96, Aegislash "Morwen" 97 (Wide Guard); no Mega (the side's one Mega is the player's). The Ch21
script first said "version 21", but 20–22 are K2. Juno's Ch21 partner is still her J7 (70–72). Validator: `RIVAL_PARTNERS`.

## 6. Festival of Champions

- **Valen** (`CHAMPION_VALEN,Valen`, ace 96): Bronzong, Lapras "Ferry", Kingdra, Gallade (**Hard Mega Gallade**), Volcarona,
  **Zygarde** (50%, **Power Construct** → Complete Forme below half HP). Field: `:PRISM_ARENA`; party order now follows the
  arena's Plate cycle (Bronzong, Volcarona, Kingdra, Gallade, Lapras, Zygarde), see the playbook §5.
- **Voss** (`MERIDIAN_VOSS,Aurelian`, ace **100**, `:PRISM_ARENA`): Klinklang, Magnezone, Golurk "Gilder", Archaludon,
  Porygon-Z, **Silvally "NULL"** (RKS System, starts with Steel Memory, form 8). **Field-team hook ("Project NULL"):** whenever
  `:PRISM_ARENA` cycles to a gym field, if Voss owns Silvally, set its item to that field's type Memory (form follows via the
  Silvally `getForm` handler) and show "NULL re-indexes to the X Memory!". Normal field (Grand Stage) = no Memory.
- **Choice-driven bracket (Rev 3):** every candidate/variant in `story/10_CHOICES_ENDINGS.md` gets a team at its round cap.
  Status: see the end of this file.
- **Choice-draw and story teams (NARRATIVE_KEYS §7) — all built**, each with +100/+200:
  | Key | Team (ace last) |
  |---|---|
  | `LEADER_MARISOL,Marisol,90` | Pelipper, Floatzel, Lanturn, Araquanid, Barraskewda, Gyarados "Lucky" (Hard Mega) — rain on Water Surface |
  | `LEADER_ANJA,Anja,90` | her Gym 10 team with Hard sets as Standard, 86–90 |
  | `LEADER_ROWAN,Rowan,90` | sun team: Sunflora (Solar Power, Sunny Day), Leavanny, Roserade, Breloom, Shiftry, Trevenant "Glasswood" (Harvest) |
  | `RIVAL_KESTREL,Kestrel,90/91/92` (K9, Fallen) | K8 with Hard sets on Standard; Krookodile replaced by Meridian's **Genesect "Gauntlet"** |
  | `LEADER_BRANN,Brann,96` | Gym 7 team, promoted sets, 92–96 |
  | `LEADER_SIGRUN,Sigrun,92` / `LEADER_ODESSA,Odessa,92` | QF draws: gym teams, promoted sets, 88–92 |
  | `CHAMPION_VALEN,Valen,1` (Last Tuning) | v0 with promoted sets; **Zygarde Form 2 (Complete)** from the start |
  | `MERIDIAN_QUENT,Percival,99` | Bronzong (TR), Metagross, Jirachi, Porygon-Z, Magnezone, Silvally "NULL" (same field hook as Voss) |
  | `GILDED_AURELIUS,Aurelius,0` | Golurk, Aegislash, Kyogre, Groudon, Regigigas, **Gholdengo "Gilt"** (100) |
  | `ECHO_MORWEN,Morwen,90` | Spiritomb, Dusknoir, Jellicent, Houndstone, Gengar, Chandelure "Lantern" (no Mismagius) |
  | `RIVAL_JUNO,Juno,70/71/72` (J7) | Ch21 tag partner: Whimsicott, starter, Tsareena (95–97) |
  | `MERIDIAN_KROLL,Sabine,21`, `MERIDIAN_MARCHETTI,Helene,21`, `MERIDIAN_QUENT,Percival,21`, `MERIDIAN_DIRECTORATE,Captain,21` | Ch21 tag foes, 3 mons each, ace 97 |
  | `LEADER_MAGNUS/NYX/CELESTINE/SIGRUN,…,1` | Ruin Gyms 15–18: Hard sets on Standard, new leads (Klinklang / Weavile / Tinkaton / Haxorus); Ruin Sigrun all Jolly/Timid |
  | `REFLECTION,???,0` | fallback only (3× Imposter Ditto, Lv 85) — Core mirrors `$player.party` |
- **More Festival teams (Rev 4 list):** `LEADER_CELESTINE/KAITO/YSOLDE,…,92` (QF: their gym teams with promoted sets, 88–92),
  `ARCHSEER_DASK,Imre,92` (Ruin QF; inversion team — Bronzong, Sableye (Hard Mega), Espeon, Umbreon, Gothitelle, Malamar
  "Behind" with Topsy-Turvy; suggested field `:INVERSE`), `LEADER_DORIAN,Dorian,90` + `LEADER_ROOK,Rook,90` (Pageant Bout
  2-vs-1 double, **3 Pokémon each**). Retired and removed per Rev 5/6: Isaura, Drey, Mireille, Thorne (never built),
  Bastian v90, Sigrun v96. List matches NARRATIVE_KEYS §7 (Revision 5/6).
- **Sister-game cameos = optional sidequests** (`Prismfall.cameo_battle`, design/CAMEOS.md): **v1** at the placement level,
  **v2** post-game at 100, each +100/+200. Shelly v1 21 (after Gym 2 since Rev 14; double; roster: Masquerain, Joltik, Larvesta, Scyther, Hard
  +Araquanid) · Venam 38 · Garret 46 (Mega Lucario on Standard too) · Melia 50 · Alexandra 56 · Amaria + Titania 78 (tag
  double, 4 each; full 6 at v2) · Shiv 84 (Core ×2 HP on Ambipom) · Lin v1 only, superboss with all six at 100 · Nova v1
  only, 90. Cameo visitors may run ahead of the level-up curve (the validator doesn't warn for `FESTIVAL_*`).
  Festival cameo versions 0/1/2/3/9 are gone.

## 6b. Mega Evolution (SPINE Revs 20–21) — trainer Megas (done in `gen.py`)

Design and reasons: `design/MEGA_EVOLUTION.md` §6. Engine rules (plugin `Prismfall Mega`): **one Mega per trainer per
battle** (since 2026-11-25: both trainers of a tag pair can Mega, and a partner with a ring; it was one per side) and
one Z-move per side; a side may use both. The AI Megas the first turn its Mega holder can act.
An NPC Megas only if its trainer's `Items` include `MEGARING`. A Pokémon with a Z-crystal can't Mega.

**SPINE Rev 21 (user):** the player's Mega Ring comes after Badge 13. **From an ace of about Lv 50 (Gym 10 on) every
important story fight has one Mega on every difficulty, if the story gives that fighter a ring** (Wardens, Valen,
Meridian's own tech, Juno; "keep it in theme/story", no one-off rings: the Mega-less list is MEGA_EVOLUTION.md §6.3) below that only a **weak** Mega (MEGA_EVOLUTION §6.1: Camerupt,
Glalie, Abomasnow, Banette, Audino, Steelix, Pidgeot, Beedrill, Sableye, Ampharos, Manectric, Houndoom, Absol, Sharpedo),
only where the design calls for it, on Standard and Hard. No theme exceptions; the Eevee Octave keeps Z.
This replaces the Rev 20 "Hard-only Megas" rule and the Rev 20 table.

**In `tools/trainer_gen/gen.py`:** `P(..., mega="STONE")` marks a team's Mega holder. The trainer Megas on every mode
when its cap is `MEGA_FROM` (50) or more; below that only with `mega_low=True` and a `WEAK_MEGA` stone, on Standard and
Hard. `mega_set` / `mega_hard` / `mega_casual` replace fields while it holds the stone; `mega_modes=(...)` overrides the
modes (Ysolde and Morwen's Echo: Sableye / Banette on Standard and Casual, Gengar on Hard, because Shadow Tag is
Hard-only). `render()` adds `MEGARING`, keeps the stone on Casual, and asserts at most one stone per team. `promote()`
carries the key, so Festival and Ruin copies Mega as their Wardens do. `tools/harness/run_mega.rb` checks the generated
`pbs/trainers.txt`: 39 Standard / 39 Hard / 39 Casual entries at ace 50+ with one Mega each, one below (Brann), the
story's ring-less fighters without one, no stone beside a Z-crystal, partners and the second trainer of a pair without one.

| Fight (cap) | Mega | Team change |
|---|---|---|
| Brann, Gym 7 (39) | Camerupt, **weak**, Std + Hard | **kept as designed, per the user**: his set as committed, only the stone added (`mega="CAMERUPTITE", mega_low=True`); the Volcanic showpiece primes the eruption for its Mega, Sp. Atk snowball and all. No nerf. |
| Kaito, Gym 8 (43) | none | Hard Lucario: Life Orb (Mega Lucario isn't weak); his Festival v92 Megas it |
| Anja, Gym 10 (51) | Glalie | replaces Beartic; Cloyster is the Casual cut |
| Marchetti Ch12 (55) / Ch14 (63) / Ch16 tag (71) / Ch21 (97) | Manectric / Houndoom / Houndoom / Manectric | Ch16: Houndoom replaces Arcanine; Ch21: Manectric replaces Arcanine; Casual cuts Mabosstiff (Ch12), Arcanine (Ch14) |
| Kestrel K5–K7, K9 / K8 | none (no ring of his own) / Scizor only with Morwen's Ring (Ch18) | from K7 Mismagius replaces Krookodile (Staraptor is the Casual cut), so the Scizor stays; K9's Genesect replaces Staraptor; K8's ring and stone come from `PrismfallMega::MORWEN_RING` at battle start |
| Odessa, Gym 11 (55) | Pidgeot "Post" | replaces Swanna; Oricorio is the Casual cut |
| Kroll Ch13 (59) / Ch17 (75) / Ch21 (97) | Sharpedo | replaces Skuntank / Skuntank / Crawdaunt; Ch13 Casual cuts Toxicroak |
| Ilsa, Gym 12 (59) | Slowbro (Trick Room) | replaces Musharna; Gothitelle is the Casual cut |
| Bastian, Gym 13 (63) | Aerodactyl "Amber" | replaces Lycanroc |
| Ysolde, Gym 14 (67) | Std/Casual Sableye, Hard Gengar | |
| Magnus, Gym 15 (71) | Metagross "Engine" | was Hard only |
| Quent Ch17 alt. (75), hijack (100), Ch21 (97) | Metagross | Ch16 Quent: none (Marchetti's) |
| Nyx, Gym 16 (75) | Absol "Omen" | replaces Malamar; Honchkrow is the Casual cut |
| Celestine, Gym 17 (80) | **Z-move instead of a Mega** (SPINE Rev 23): Mimikyu @ Mimikium Z (Let's Snuggle Forever) | Mimikyu is back in its slot (Rev 21's Mega Mawile is gone); Azumarill is the Casual cut. Win rate (prepared Standard): 100% with the Z, 97% without (design/Z_MOVES.md §5) |
| Sigrun, Gym 18 (85) | Salamence "Dreamwing" | was Hard only |
| Juno J4 (90) | Gardevoir "Veil" | replaces Comfey (not the starter: Core swaps it, and most lines have no Mega); J7 (partner): none |
| Festival draws | Marisol Gyarados, Anja Glalie, Sigrun, Odessa, Celestine (her Z-move), Kaito Lucario, Ysolde, Brann v96 Camerupt, Dorian Lopunny (replaces Ambipom; Rook none) | Rowan, Imre Dask: none (no ring; Imre's Rev 20 Hard Mega Sableye removed) |
| Valen (96) | Gallade | was Hard only |
| Voss (100) | Ampharos "Lumen" | replaces Klinklang |
| Directorate Captain (97) | Scizor | |
| Cameo Garret | v1 (46): none now; v2 (100): Lucario on every mode | `cameos.py` |

**Z-moves (SPINE Rev 23, `design/Z_MOVES.md`):** the player's one ring (the Mega Ring, after Badge 13) wakes Z-crystals
too; NPCs need a story reason for a crystal and never hold a stone and a crystal at once. Z users: the Eevee Octave
(unchanged) and Celestine (instead of her Mega). In `gen.py` a Z user simply holds its crystal; `run_mega.rb` allows
it in place of a Mega only for the listed Z users.

**Mega-less for story reasons** (no ring by then): the Mourner and Rowan, Kestrel before Morwen's Ring, Imre Dask,
Morwen's Echo, Aurelius, the war officers (MEGA_EVOLUTION.md §6.3).

**Win rates** (prepared team at the cap, no Mega on the player's side; `run_winrates.rb` cells G7M, G10M, M12M, K5M, G11M (renamed in round 4; G7, G10 ... are now the round-4 cells)
with `PRISM_PREPARED=1`, 60 fights a cell; `PRISM_FOE_NOMEGA=1` is the same fight with the foe's ring taken away):
MEGA_EVOLUTION.md §8.

## 7. True finale — Arceus boss spec (for Core / Field Effects / EBDX Bridge)

Core already runs this stage through `EliteBattle.bossBattle(:ARCEUS, 100, 1, false, options)` on `:PRISM_ARENA`
(SYSTEMS.md §6). This section supplies the numbers and the phase logic.

**Base Pokémon** (`ARCEUS_SETUP` / `:prismfall_festival_boss` handler): Lv 100, ability Multitype, IV 31, EVs 4 HP /
252 SpA / 252 Spe, Timid. Uncatchable, cannot run. Status immunities on (EBDX `IMMUNITIES`).

| | Casual | Standard | Hard |
|---|---|---|---|
| `:bossboost` HP / other stats | 1.5 / 1.1 | 2.0 / 1.25 (Core default) | 2.5 / 1.3 (Spe 1.15) |
| Bar HP (× boosted max HP; bar count is set by the story variant) | 0.6 | 1.0 | 1.25 |
| Recover in sets | no | yes, max 2 uses per phase | yes |
| Telegraph next Plate | 2 turns ahead | 1 turn ahead | 1 turn ahead |

**Alignment with NARRATIVE_KEYS §6.6 (authoritative for bar counts):** a "phase" below = one **bar**. Default
`ARCEUS_BOUND` has 6 bars; bar *k* holds the Plates of gyms 3k−2..3k (bar 1 Normal/Bug/Water since SPINE Rev 14 … bar 6 Dark/Fairy/Dragon), so
within a bar Arceus cycles only among those three Plates/fields. Forced locks (+1 all stats per refusing Warden) stack on top.
Variants: `_MISCALIBRATED` 5 bars (bar 5 cycles all six Plates of gyms 13–18 — use bar HP ×0.85 to keep it fair);
`_GILDED` 6 bars, bar 6 refills 3× (use the Casual bar HP for refills on every difficulty); `_WAR` 7 bars, every lock
forced — cap Arceus's stages at +2 on Casual/Standard; bar 7 = Legend Plate phase; `_JUDGMENT` (Ruin) 7 bars with the
Giratina-Origin partner (`player_side 2`), bar 7 on `:INVERSE`. The HP-% thresholds in the difficulty table become
"bar HP": each bar = Arceus's boosted max HP × 0.6 (Casual) / 1.0 (Standard) / 1.25 (Hard); bar count never changes with
difficulty. HARMONY_BUFF (Resonance ≥ 6) applies at every bar break as specified there.

**Phase logic ("Judgment of the Plates").**
1. Battle starts on `:PRISM_ARENA`, which (per FIELD_API `:borrow`, `:order => :sequential`) cycles gym fields every
   3 turns. Arceus's Plate **always matches the active borrowed field**: on each `:prismfall_field_changed` event, set
   `pkmn.item` to that type's Plate and call `battler.pbChangeForm(form, "Arceus takes up the X Plate!")`; Judgment follows.
2. **Phase break** (crossing an HP threshold): Arceus forces a field cycle immediately (skipping to the field whose type
   is best against the player's active Pokémon), resets its own negative stat stages and loses status, and swaps to that
   phase's moveset (table below). Display "The Plates answer their god!" — this is the multi-bar moment; EBDX Bridge may
   flash the backdrop.
3. **Telegraph:** the turn before an automatic cycle, show "The X Plate begins to glow..." so players can switch.
4. **Final phase (below the last threshold) — the Legend Plate:** the player's Legend Plate fragment resonates. Arceus
   becomes **form 9 (??? type)**, Judgment becomes typeless (neutral to all), the field cycling stops and the arena settles
   by the player's **Resonance** (Rev 3): Harmony → `:RAINBOW`, Ruin → `:BLEED`, neutral → `:NONE`. Final-phase moves:
   JUDGMENT, EXTREMESPEED, CALMMIND, RECOVER (Casual: no Recover).

**Moveset per Plate** (slot 1 is always JUDGMENT; slot 4 is RECOVER unless noted; all legal for Arceus):

| Field → type (form) | Slots 2–3 | Field note |
|---|---|---|
| SILKWOOD → Bug (6, Insect) | EARTHPOWER, SHADOWBALL | never Fire (would burn the field) |
| GRAND_STAGE → Normal (0, no Plate) | SHADOWBALL, FOCUSBLAST | slot 4 CALMMIND |
| WATER_SURFACE → Water (11, Splash) | ICEBEAM, THUNDERBOLT | Ice Beam ×3 can freeze to Frozen Lake |
| NEON_GRID → Electric (13, Zap) | FLASHCANNON, ICEBEAM | Flash Cannon hits as Electric here |
| DESERT → Ground (4, Earth) | FIREBLAST, SHADOWBALL | |
| CORROSIVE_MIRE → Poison (3, Toxic) | EARTHPOWER, SHADOWBALL | never Fire (fumes explode) |
| VOLCANIC → Fire (10, Flame) | EARTHPOWER, WILLOWISP | Earth Power ×1.3 + burn chance |
| COLOSSEUM → Fighting (1, Fist) | SHADOWBALL, PSYCHIC | |
| FLOWER_GARDEN → Grass (12, Meadow) | EARTHPOWER, SLUDGEBOMB | |
| FROZEN_LAKE → Ice (15, Icicle) | THUNDERBOLT, EARTHPOWER | |
| STORMFRONT → Flying (2, Sky) | THUNDERBOLT, FOCUSBLAST | |
| MINDSCAPE → Psychic (14, Mind) | FOCUSBLAST, SHADOWBALL | slot 4 CALMMIND (Hard: TRICKROOM) |
| CRYSTAL_CAVERN → Rock (5, Stone) | EARTHPOWER, FIREBLAST | |
| HOLLOW_CATHEDRAL → Ghost (7, Spooky) | FOCUSBLAST, WILLOWISP | Hard slot 4 PERISHSONG once per battle |
| FACTORY → Steel (8, Iron) | EARTHPOWER, THUNDERBOLT | |
| NEW_MOON → Dark (17, Dread) | FOCUSBLAST, FLAMETHROWER | slot 4 CALMMIND |
| FAIRY_TALE → Fairy (18, Pixie) | FLAMETHROWER, EARTHPOWER | |
| DRAGONS_DEN → Dragon (16, Draco) | FIREBLAST, EARTHPOWER | |

Balance intent: each Plate's coverage hits the types that resist its Judgment, so the counterplay is switching on the
telegraph, not one wall. Kestrel (tag partner in the hijack per cast) does **not** join the Arceus fight (`player_side 1`).

## 8. Notes for other workstreams

- **Core:** ✔ variant fallback, ✔ J3 on `LEADER_JUNO` 30/31/32, ✔ ability-slot preservation on starter swap (we rely on
  `AbilityIndex = 2` surviving). Trainer names: Wardens by first name (`Tamsin` ...), `Kestrel`, `Juno`, `Valen`,
  `MERIDIAN_VOSS` name **`Aurelian`**. Warden Festival versions 50 are NPC-only (no data written).
- **Field team:** explicit fields for rival, admin and Festival battles are in `FIELD_DEFAULTS.yaml` → `exceptions.trainers`
  (TRAINER_FIELD_PLAYBOOK.md §1). The Festival bracket is set to `:PRISM_ARENA` there, following story/08_ACT_V; confirm or revert.
  Galarian Weezing deliberately never has Misty Surge. Voss's Silvally hook and the Arceus Plate hook are specified in §6–7.
- **Story:** nicknames used — Bobbin, Lucky, Camera, Effigy, Ward, Anvil, Memory, Matriarch, Taxi, Hush, Geode, Vigil,
  Mark One, Nobody, Vow (Celestine's Sylveon, the ace; Togekiss keeps "Vigilant"), Dreamwing (aces); Morwen (Kestrel's Honedge line), Sweetpea (Juno's Bounsweet line),
  Rowan (Juno's Hard Roserade), Ferry (Valen's Lapras), Gilder, NULL (Voss). Rename freely (≤10 chars).
- Gen 9 note: the live base `pokemon.txt` does not list Bisharp→Kingambit (the Gen 9 Pack adds it only through its optional
  Auto-Updates PBS); the validator treats such Gen 9 evolutions as prevolutions (`MANUAL_PREVO`).

## 9. Win rates (harness, round 3; Gyms 4–18 and the late game: §9b)

`tools/harness/run_winrates.rb` (real Essentials v21.1 battle code + Prismfall plugins, AI on both sides): a **realistic**
challenger is a starter plus catches drawn from what `POKEMON_AVAILABILITY.md` (Rev 16 distribution) and
`EVENT_POKEMON.md` allow before that fight, weighted by encounter rate (no Fighting type and only a 3% Sandygast before
Gym 1; no Fire / Rock / Flying gift and ≤ 4% wild Fire / Rock before Gym 2), six Pokémon from Gym 1 on, the starter at
the cap and the rest 1–3 under, level-up moves plus the story's TMs, random natures, IV 5–25, an Oran Berry and a few
Potions (none on Hard), piloted by the AI at skill 100. **Prepared** = grinded to the cap with the best type answers the
distribution allows by then (rare finds included). 60 fights per cell (20 per starter); ±6 points of noise.

| Fight | Casual | Standard | Hard (realistic) | Hard (prepared) |
|---|---|---|---|---|
| Picnicker Ada (Ch1 Windfall Row, Meadow; starter 9 + two catches) | 99% | 96% (Water 52 of 60) | 93% (Water 50 of 60) | — |
| K1 Kestrel (Lv 5, can be lost) | 100% | 15% | 0% | — |
| J1 Juno (Meadow) | 100% | 63% | 50% | 55% |
| Gym 1 Dorian, sparse house (stage 1) | 93% | 42% | 2% | 33% (old troupe) |
| Gym 1 Dorian, good house (stage 2 + fans) | 97% | 62% | 5% | 50% (old troupe) |
| Gym 1 Dorian, full house (stage 3 + fans) | 100% | 75% | 5% | 62% (old troupe) |
| Gym 2 Tamsin (Silkwood, double) | 100% | 45% | 3% | 35% |
| K2 Kestrel (Mountain) | 98% | 58% | 5% | 35% |
| Gym 3 Marisol (Water Surface) | 82% | 23% | 0% | 37% |
| Gym 3 Marisol, a team that found the Glade's night Emolga | 98% | 63% (Fire 8 of 20; 60 Fire runs: 42%) | 3% | — |

Reading: the AI challenger plays worse than a person (no planned leads, little stalling), so Standard's 25–60% means
"a realistic team loses a few times and wins with the field notes"; a **prepared** team wins Standard J1 83%, Gym 1
95%, Gym 2 98% (one run crashed on the Gen 9 Pack's Psycho Shift bug, counted as a loss; fixed since, Base Fixes 003), K2 85%, Gym 3 100%. Hard is for prepared teams (30–55%); a realistic team loses there, as on Reborn's harder modes. Casual
is 82–100%.

**Picnicker Ada (2026-11-20):** the playtest's "Ch1 wall" (Oddish 6, Budew 7 beat the bot's Water starter 7 of 8) is the
bot's way of playing (it heals only by blacking out). A sensible player at Windfall Row (starter Lv 9, two catches from
520 / 521 at Lv 6–7, two Potions; cells `ADA` / `ADA1`, 60 fights per starter): Water starter **87%** on Standard (Grass
and Fire 100%), 83% on Hard; the Water starter **alone** wins 50%. A real Grass wall for a lone Water starter, gone once
it has a bird (Pidove, Pikipek, Rookidee and Hoothoot are 8–20% on those two roads): Reborn-style, so her set is unchanged.

**Gym 3 with a Fire starter (2026-11-20):** a realistic Fire-starter six wins **0 of 20** (2 of 60) on Standard: Marisol's
Gyarados (Whirlpool ×2 on the surface) sweeps it, and a Lv 22 Flaaffy, Luxio, Joltik or Grass catch lifts that only to
0–13% (a forced catch, 30 runs each; Chinchou's Volt Absorb walls the slow ones). No counter is handed out (rule R4
forbids an Electric or Grass gift with 1–2 badges). Instead the answer is **earned, Reborn-style (P5: a time condition
on a side map):** **Emolga, 5% at night only, in the secret Rimewood Glade** (563, behind the Cut sapling; its night
table is Emolga 5 + Joltik 3, the 8% cap). Lv 17–19, Nuzzle / Quick Attack / Thunder Shock (Charge at 20). A Fire-starter
six that found it wins **42%** on Standard (25 of 60; a second 60: 30%), Casual 95%, Hard 0% (Hard is for prepared
teams: prepared 37%). Grass and Water starters that find it reach 73–80%. Pachirisu tested at 63% (too strong for a
"modest" find); Emolga is the pick. The `G3E` cell in `run_winrates.rb` forces it into the team.

**Multi-bar legend bosses (2026-11-24; `winrates_r4.rb` cells BKYO, BGRO, BGIR, BZEK; 30 fights a cell on Standard / Hard,
60 on Casual).** Reuben's ruling: these are meant to be hard for an average player; **nothing is nerfed outside Casual.**
The 2026-11-23 rebuild (no offensive EVs, setup moves swapped, breaks hardening instead of sharpening, Standard ×0.9)
was reverted in full: Standard and Hard are the original designs. The harness plays without a strategy (no revives, no
field play, no boss-specific items), so its Standard / Hard numbers are a floor, not what a planning player gets.
Casual only: HP ×0.75 and offence ×0.6 (Kyogre and Zekrom HP ×0.7, offence ×0.5), and Kyogre / Groudon / Giratina trade
their setup move (Calm Mind, Bulk Up) for a utility move.
| Boss (cap) | Casual typical | Standard typical | Standard prepared | Hard prepared |
|---|---|---|---|---|
| Kyogre, Isenmar (55) | 85% | 0% | 7% | 0% |
| Groudon, Undersands (67) | 82% | 0% | 33% | 17% |
| Giratina, Reverse Depths (71) | 100% | 0% | 0% (the prepared model picks answers by the normal chart, wrong on Inverse) | 0% |
| Zekrom, the Engine (75) | 93% | 0% | 77% | 20% |
| Gilded King Aurelius (100, Ruin) | 47% | 13% | 57% | 67% |

**Ch10 Loyal Three (2026-11-23; Bosses 112, cells L3O / L3M / L3F with the Ogre, L3OA / L3FA alone):** Lv 48 / 49 / 50,
1 / 2 / 3 bars, Standard HP ×1.5 and ×1.15–1.25 elsewhere, Hard HP ×1.5 and ×1.2–1.25. A typical Lv 49–51 six (60 a
cell): with the Ogre Standard 75 / 95 / 98%, alone Okidogi 53% and Fezandipiti 92%; Hard typical 18 / 40 / 58% (alone
5 / 57%), Hard prepared 90–100%; Casual 100%. First pass (Lv 46–48, HP ×1.2) was 100% everywhere in 3–9 turns;
Okidogi's Bulk Up then snowballed with the break's +1 Attack (Hard alone 3%), so it has Low Kick instead.

**Gym 1, Reuben's locked troupe (2026-11-23):** Smeargle, Chatot, Hisuian Zorua, Ditto, Kecleon, Meloetta (Gemini
proposal 2026-11-23 Part C). As proposed (Lv 10–15, Echoed Voice Chatot, Oran Meloetta 15) the realistic Standard team
won **8%** (sparse; 60 fights) and Casual 58%: the Grand Stage made Chatot's Echoed Voice (then Round) the sweeper, and
the Matinee Meloetta finished what was left. Tuned to: Chatot without damaging sound moves (Standard / Casual),
Smeargle 9, Zorua 11 (Swift / Scratch; Shadow Sneak is Hard's, Lv 12), Ditto 11, Kecleon 12 Hardy (Lick for Thief),
Meloetta **14 with no held item** at the proposal's ×0.80; Hard Chatot Sing, no Fury Swipes on Hard Kecleon. Result
(120 fights sparse, 60 per house): Casual 93 / 97 / 100%, Standard **42 / 62 / 75%** (old troupe 41–45 / 63 / 73%),
Hard realistic 2 / 5 / 5% (old 2 / 2 / 5%). A ×0.70 Matinee also reached 42%, but kept the proposal's ×0.80 and took
the Oran instead. The validator warns that the ace (L14) sits under the cap: intended (Act One).

**The Saltmere crowd (Gym 1 rows, 2026-11-20):** the bigger the house you gathered, the more Standing Ovation is
yours (`102_Field_GrandStage.rb`; `FieldEffects.home_crowd_foe?` / `home_crowd_full?` in Puzzles
`007_Puzzles_SaltmereCrowd.rb`). Sparse (0–6): unchanged. Good (7–13): your fans heal your side from Encore up, and at
Standing Ovation Dorian's troupe basks at half (1/32). Full (14+): at Standing Ovation only your side basks, only your
attacks get the +1 crit stage, and Dorian's Sing can miss (×1.3 instead of never missing; Jigglypuff's sure Sing was
what made a full house no better than a good one). The crowd rules are `:ai_safe`, so both AIs still weigh who the
house is cheering. Standard, realistic Lv 15 team, **180 fights a cell: sparse / good / full 45 / 63 / 73%** (before
the crowd rules 43 / 52 / 45%; with only the home-side bask 46 / 68 / 64%). Lv 14 team (60 a cell) 22 / 32 / 45%,
Hard prepared 33 / 50 / 62%, Casual 100%. Tried and dropped: the home-side crit alone (72 / 69%), Sing alone
(73 / 76%), both at every house (76 / 73%): the good house also reaches Standing Ovation, so only full-house rules
separate the two.

Late fights (`/home/claude/work/trainers2/run_late.rb`, a well-built six at the cap, Full Restores, 8–10 runs): the
Eevee Octave gauntlet (Lv 87 / 89) 9 of 10 Standard and 8 of 10 Hard with planned leads, 1 and 0 of 10 without; the war
legendaries Reshiram 7/8 Standard, 5/8 Hard; Kyogre 5/8 Standard, 0/8 Hard (a counter-team fight); war partner doubles
6/8 (Isenmar) and 8/8 (Ashkaar) on Standard. Details: TRAINER_FIELD_PLAYBOOK.md §6.

## 9b. Win rates, round 4 (Gyms 4–18, the rivals, the villains, the Festival bosses)

`tools/harness/run_winrates.rb` cells G4–G18, K3–K9, J2, J4, WICK, Q8, MOURN, M12, KR13, M14, KR17, Q17, VALEN, VOSS,
QH (`tools/harness/winrates_r4.rb`). 60 fights a cell (20 per starter), each mode's own trainer version, every fight
at the player's hard level cap, on the battle's own field. Two player models, both built only from what the game has
handed out by that badge count (wild tables and badge tiers: `tools/trainer_gen/pools.py` → `winrate_pools.json`;
gifts, quest Pokémon, the three starter eggs and the Act IV fossils; level, stone, trade and friendship evolutions
from Lumen on; gym TMs, field TMs and HMs by badge; the Mega Ring, its stones and the Z-crystals from 13 badges):
- **Typical:** the starter at the cap and five catches drawn by encounter rate × (final BST / 450)^4, spreading types,
  cap−0..2, random natures, IV 5–25, battle EVs (min(1.5 × level, 85)), the three best attacks it can have plus a
  fourth or a setup move, a Sitrus and a few found items, a Mega only if a team member's stone is out (6 in 10), no
  foe knowledge. 3 Hyper Potions (Super / Hyper before 6 badges; 2 Full Restores + 2 Hyper from 13); none on Hard.
- **Prepared:** the starter plus five of the six best answers to that foe's actual team, by type against its team
  **weighed by the field's type multipliers** (the field notes), rare finds included; all at the cap, IV 20–31, a
  fitting nature, 252/252 EVs from 8 badges, moves chosen against the foe with every TM out by then, setup or
  recovery, Protect in doubles; Life Orb / Choice / Leftovers / Sash / Assault Vest by role; one Mega and one Z from 13.

Final numbers (after the round 4 changes, TRAINER_FIELD_PLAYBOOK.md §8b), typical / prepared:

| Fight | Casual typ / prep | Standard typ / prep | Hard typ / prep |
|---|---|---|---|
| Gym 4 Rook (Neon Grid) | 98% / 100% | 40% / 98% | 2% / 62% |
| Gym 5 Sahar (Desert) | 98% / 100% | 60% / 100% | 15% / 70% |
| Gym 6 Corvin (Corrosive Mire, double) | 93% / 100% | 28% / 100% | 2% / 75% |
| Gym 7 Brann (Volcanic; locked) | 75% / 100% | 15% / 93% | 2% / 70% |
| Gym 8 Kaito (Colosseum) | 85% / 100% | 15% / 75% | 0% / 28% |
| Gym 9 Juno, J3 (Flower Garden) | 97% / 100% | 57% / 98% | 15% / 88% |
| Gym 10 Anja (Frozen Lake; Mega Glalie) | 93% / 100% | 7% / 55% | 2% / 23% |
| Gym 11 Odessa (Stormfront, double; Mega Pidgeot) | 95% / 100% | 7% / 98% | 0% / 67% |
| Gym 12 Ilsa (Mindscape; Mega Slowbro) | 77% / 100% | 12% / 88% | 7% / 55% |
| Gym 13 Bastian (Crystal Cavern; Mega Aerodactyl) | 87% / 100% | 18% / 100% | 18% / 97% |
| Gym 14 Ysolde (Hollow Cathedral; Mega Sableye) | 92% / 100% | 12% / 93% | 0% / 50% |
| Gym 15 Magnus (Factory; Mega Metagross) | 77% / 100% | 12% / 87% | 0% / 35% |
| Gym 16 Nyx (New Moon, double; Mega Absol) | 90% / 100% | 0% / 83% | 0% / 45% |
| Gym 17 Celestine (Fairy Tale, double; Z-move) | 83% / 100% | 12% / 97% | 0% / 50% |
| Gym 18 Sigrun (Dragon's Den; Mega Salamence) | 70% / 100% | 2% / 50% | 0% / 28% |
| K3 Kestrel (5 badges, Desert) | 100% / 100% | 58% / 97% | 13% / 85% |
| J2 Juno (5, Corrosive Mire) | 100% / 100% | 98% / 100% | 62% / 100% |
| K4 Kestrel (7, Colosseum) | 93% / 100% | 25% / 85% | 0% / 42% |
| K5 Kestrel (10, Stormfront) | 97% / 100% | 17% / 93% | 2% / 62% |
| K6 Kestrel (13, Hollow Cathedral) | 95% / 100% | 10% / 97% | 7% / 63% |
| K7 Kestrel (16, Fairy Tale) | 90% / 100% | 15% / 90% | 2% / 60% |
| K8 Kestrel (Festival SF, Prism Arena) | 93% / 100% | 10% / 92% | 0% / 53% |
| K9 Kestrel, fallen (Festival SF) | 63% / 100% | 2% / 82% | 2% / 48% |
| J4 Juno (Festival R16; Mega Gardevoir) | 85% / 100% | 20% / 98% | 8% / 85% |
| Ch7 Brother Wick (5) | 100% / 100% | 70% / 100% | 12% / 93% |
| Ch8 Dr. Quent (6, Volcanic) | 100% / 100% | 60% / 87% | 13% / 55% |
| Ch9 the Mourner (7; Trevenant boss) | 92% / 100% | 58% / 100% | 10% / 97% |
| Ch12 Marchetti (10; Mega Manectric) | 98% / 100% | 25% / 95% | 3% / 63% |
| Ch13 Kroll (11; Mega Sharpedo) | 98% / 100% | 17% / 98% | 2% / 93% |
| Ch14 Marchetti (13; Mega Houndoom) | 95% / 100% | 27% / 92% | 2% / 77% |
| Ch17 Kroll (15, Cave) | 100% / 100% | 25% / 100% | 3% / 98% |
| Ch17 Quent, alt. (15, Cave) | 93% / 100% | 33% / 98% | 2% / 80% |
| Final: Valen (96; Mega Gallade) | 72% / 98% | 3% / 48% | 2% / 35% |
| Hijack: Voss (100; Mega Ampharos) | 73% / 100% | 7% / 68% | 3% / 77% |
| Hijack: Quent (100) | 83% / 100% | 15% / 87% | 3% / 82% |

**Difficulty curve.** Standard: a typical team wins 40–70% at Gyms 4, 5 and 9 and the Act II story fights before
Gym 8 (K3, Wick, Quent, the Mourner), 15–28% at Gyms 6–8 and K4, then **0–33% from Gym 10 to the Festival** (0–7% at
Gyms 10, 11, 16 and 18, K9, the Final and Voss); a prepared team wins 75–100% almost everywhere. **Walls:** Gym 10
Anja (prepared 55%: her heavy blows, Avalugg's Body Press and Matriarch's High Horsepower, crack the lake into water,
which halves the Fire answer, as designed: Fighting and Steel are the counterplay), Gym 18 Sigrun (50%: Dragon x1.5
that becomes x2 once the Den wakes, which it did in 22 of 30 logged runs; a field request in `mapgen/REQUESTS.md`)
and the Final (Valen 48%), the three steepest steps; Gym 8 Kaito (75%) is Act II's. **Soft spots:** J2 (typical 98%:
the friendly rival's Grass team, with a middle-stage starter, loses its own Corrosive Mire to her Misty Terrain),
Gym 9 Juno (typical 57%, prepared 98%), Gym 13 Bastian (prepared 100%, Hard prepared 97%), the Act II–IV villains for
prepared Hard teams (Wick, the Mourner, Kroll 93–98%). **Hard:** a typical team almost never wins (0–18%; J2 62%), a
prepared one 23–35% at the hardest (Gyms 8, 10, 15, 18, the Final) and 42–100% elsewhere: Hard demands preparation.
**Casual:** 83–100% for most fights; the lowest are Kestrel fallen (K9, 63%: Hard sets promoted, by design), Sigrun
(70%), the Final and Voss (72–73%), Brann (75%, locked), Ilsa and Magnus (77%).

**Against the targets.** Prepared Standard teams sit in or above the 70–95% band except the three walls. Typical
Standard teams reach the 35–60% band only up to Gym 9; from Gym 10 on they win 5–20%. The stat side was not the
cause: Standard is already softer than Reborn's and Rejuvenation's normal modes (§1c), and in experiments (Gyms
10–18 and K6, a typical team) two levels off every non-ace, IV 20, no Life Orb / Choice items, Hyper Potions for
Full Restores and Casual's roster, all at once, moved the typical win rate only from about 6% to about 28% (Gym 10
30%, Gym 12 18%, Gym 14 38%, Gym 16 13%, Gym 18 7%, K6 62%); even Casual (five Pokémon, 4–7 levels under the cap,
IV 12–20, no EVs) is won 63–100% by this AI-piloted typical team. What beats
a team that was not built for the fight is the field (the Warden's own type x1.2–1.5, often with a second boost) and
the foe's AI using it, which is the point of the field design (§1: "you must use the field and type matchups"). So
round 4 removed every one-Pokémon sweep the knockout counts showed (§8b) and left the type-and-field puzzle in place:
a player who reads the field notes and brings the answers wins, as in both reference games. The AI pilot plays worse
than a person (no planned leads, no stalling out a Trick Room or a Tailwind), so a human's typical team will do
better than these numbers.

## 9c. Field logic audit (SPINE Rev 24): win-rate deltas

The field changes of `design/FIELD_LOGIC_AUDIT.md`, measured before and after with the same seeds and the same
`pbs/trainers.txt` (two private run copies, one with the old field files). Standard only.

**Round-4 cells** (`run_winrates.rb` / `winrates_r4.rb`, 10 fights per starter, 30 a cell):

| Fight (field change) | Typical before -> after | Prepared before -> after |
|---|---|---|
| G4 Rook (Neon Grid: no Pulse x1.5) | 12/30 -> 12/30 | 30/30 -> 30/30 |
| G10 Anja (Frozen Lake: sun thaws over 3 rounds) | 3/30 -> 3/30 | 19/30 -> 19/30 |
| G13 Bastian (Crystal Cavern: no sun / rain / hail) | 8/30 -> 8/30 | 30/30 -> 30/30 |
| G15 Magnus (Factory: no sun) | 5/30 -> 5/30 | 26/30 -> 26/30 |
| M14 Marchetti (Dark Crystal: no sun / rain / hail, no sunlight relight) | 8/30 -> 8/30 | 27/30 -> 27/30 |

No change at all: these teams don't bring weather or Pulse moves. So three **weather teams** were run against the
gyms whose weather rule changed (a hand-built six at the cap that brings the weather the old rule rewarded, 12 fights,
Hyper Potions; `tools/harness/run_weather_cells.rb`):

| Fight | Team | Before -> after | Field sequences after |
|---|---|---|---|
| G10 Anja | Drought Torkoal, Arcanine, Lucario, Magnezone, Chlorophyll Venusaur, Heracross | 3/12 -> 4/12 | 7x lake -> water -> lake, 4x lake -> water, 1x lake (was: melted at once every time) |
| G13 Bastian | Drizzle Pelipper, Swift Swim Kingdra and Ludicolo, Swampert, Lucario, Ferrothorn | 12/12 -> 12/12 | rain now fails; the team wins on Water / Fighting / Steel coverage alone |
| G15 Magnus | Drought Torkoal, Arcanine, Chandelure, Chlorophyll Venusaur, Garchomp, Gyarados | 12/12 -> 9/12 | sun now fails in the foundry; Fire x1.2 from the crucibles still helps |

Gym 10 is unchanged in practice (melting the lake at once used to hand Anja's Walrein open water as often as it
helped the sun team). Gym 15 loses its easiest answer: a dedicated sun team drops from 12/12 to 9/12; the prepared
cell is unchanged (26/30). No re-tune proposed.

**The war on 926** (the trainer designer's `run_late.rb`, a well-built Lv 85 six, 8 runs; singles 4):

| Fight | Before -> after | What the Glass Dunes did after |
|---|---|---|
| Reshiram (`RESHIRAM_GLASS_DUNES`) | 7/8 -> 7/8 | 3 of 8 cooled into Mirror Glass under the storm's rain; one was reheated by Reshiram's fire |
| Kyogre (`KYOGRE_GLASS_DUNES`) | 5/8 -> 5/8 | no glass (Kyogre's side) |
| Partner double vs Isenmar | 6/8 -> 6/8 | no glass |
| Partner double vs Ashkaar | 8/8 -> 8/8 | glass in 5 of 8; 2 re-flooded by Marisol's side (was: 1 cracked back to sand) |
| Singles 920 / 924 / 925 / 926 (12 trainers) | all 4/4 -> 4/4 | unchanged sequences |

No war fight changed its result; the cooling shows up only where the Fire side stops using Fire (Reshiram in its own
storm), which is the point of it.

## 9d. Open flag: Kyogre (Ch11, `:KYOGRE_ISENMAR`) in the real engine (2026-11-21)
In the Ch11 key-events capture (`tools/harness/visual/ch11/008_Ch11Keys.rb`, the engine's AI playing the player's side),
Kyogre beat two cap-level parties:
- a Lv 54 general team: 7 turns, first bar barely broken;
- a Lv 55 team built for it (Lanturn, Ludicolo, Ferrothorn, Toxtricity, Raichu, Lucario): 10 turns, first bar broken.

On Frozen Lake its Ice Beam one-shots most of a Lv 54–55 team. Aqua Ring and Calm Mind then outheal the AI's damage.
The headless suite's Lv 100 run still wins in 3 turns (§9).

The engine AI misplays, so this is a flag, not a verdict. Before Ch11 ships, run the round-4 harness at cap 55.
Options if it confirms:
- drop Calm Mind or Aqua Ring from bar 1;
- open on Frozen Lake without the Ice boost on Kyogre's own moves;
- or keep bars at 2 on Standard.

## Intentional non-learnable moves (validator allowlist)

Rows here are read by `tools/validate_trainers.py`: `| TYPE,Name,Version | SPECIES | MOVE or ABILITY | reason |`.
Version `*` = every version of that trainer. Rotom's appliance moves are granted by its form handler and are special-cased
in the validator, so they need no row.

| Trainer | Species | Move | Reason |
|---|---|---|---|
| FESTIVAL_LIN,Lin,* | TOGEKISS | OBLIVIONWING | Lin's Reborn signature: a Togekiss with an illegal move (CAMEOS.md). Casual swaps it for Air Slash. |
| LEADER_ILSA,Ilsa,* | HATTERENE | PSYCHICNOISE | Legal in Scarlet/Violet (TM 213); the base pokemon.txt has no DLC TM learnsets. Her transition play: 3 damaging sound moves crack the Mindscape into the Inverse Field (TRAINER_FIELD_PLAYBOOK.md). Casual uses Psychic. |

## Status

- Wardens, rivals (K1–K9, J1–J4, J7), villains/admins (Thistle, Teo, Ch21 foes), Valen/Voss/Quent/Aurelius/Morwen,
  every Festival entry in NARRATIVE_KEYS §7 (Rev 5/6), the Ruin teams, the cameo sidequests and
  every route/gym trainer the built maps reference: **done, 0 validator errors** (`--maps maps_out/Data`: all resolve).
- Not trainer data (specified in §7 for Prismfall Bosses): the Arceus configs, `GIRATINA_ORIGIN_TRIAL`, `KYOGRE_WEATHER`.
- Rev 10 field re-tune: done for Wardens, rivals, Thistle, Teo, Valen, Voss, the Festival draws and the route trainers
  (TRAINER_FIELD_PLAYBOOK.md). Not re-tuned: cameo sidequests, Quent, Aurelius, the Ch21 tag foes.
- Story teams: the Mourner, Wick, Sable, Marchetti 0–2, Quent 0–2, Kroll 0–1 all exist (round 2). Ashe has no story
  battle in the script (no team needed until one is written).
- **Eevee Octave (SPINE Rev 19), round 3: done in `gen.py`** (moved out of `pbs/trainers_trials.txt`). Lyra 0 (Eevee 17)
  + Vesper 0 (Eevee 18) for the Ch2 double; Vesper 1 (Ch13); duels v50 at the next cap − 1 (18 / 22 / 26 / 30 / 34 /
  38 / 58 / 88); **gauntlet v60: one Eeveelution each with its Z-crystal, Lv 87 (Hard 88, Casual 83); Vesper's Eevee
  with the Eevium Z, Lv 89 (Hard 90, Casual 85)** against the Festival cap of 90. Retired: Carol 0, singers 1–8,
  Vesper 2. Harness results: TRAINER_FIELD_PLAYBOOK.md §6 and mapgen/REQUESTS.md (trainer designer, round 3).
- **The war (SPINE Rev 18), round 3:** the Battle of the Glass Dunes is on land. Gauntlets on 920 (Desert), 924
  (Cinderglass), 925 (the Bleed); crest singles and the partner doubles on 926 (Desert → flood / glass); partners
  `LEADER_SIGRUN` / `LEADER_MARISOL` 19 (one version: the same ally in every mode); war legendaries
  `:RESHIRAM_GLASS_DUNES` / `:KYOGRE_GLASS_DUNES` in Prismfall Bosses (`106_Boss_WarLegends.rb`; the trainer designer
  took the Bosses plugin over). Cap 85.
- Little Crucible (Trials) re-levelled to the 2-badge band (19–21). K1 Standard: no type move (Reborn / Rejuvenation).
- **Round 4 (2026-11-21):** Gyms 4–18, K3–K9, J2, J4, the villains and the Festival bosses measured against typical
  and prepared teams in every mode (§9b, `winrates_r4.rb`), calibrated against Reborn / Rejuvenation (§1c), sweep tools
  moved to Hard (TRAINER_FIELD_PLAYBOOK.md §8b); the 577 / 578 route trainers built (map builder 13's cells).
  Open: the Ch5–7 story and route trainers in `mapgen/REQUESTS.md` (the Gala tag, 580/581/592–595, the Directorate).
- Pending: new maps' trainers as they are generated. Done: Gym 3's earned Electric answer for the Fire starter (the
  Glade's night Emolga, §9); the Saltmere audience rules (the bigger the house, the more Standing
  Ovation is yours; §9).
