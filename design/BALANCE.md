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
| Levels | Standard −2 (cap <40), −3 (<70), −4 (70+) | Ace **at the cap**, others 1–4 below | Ace at the cap, others +1 (never above cap) |
| IVs / EVs | IV 4→20 by tier, **EV 0** | IV 12 / 18 / 24 / 28 / 31 (caps ≤23 / ≤35 / ≤51 / ≤71 / 72+), default EVs (min(lv×1.5, 85) each) | IV 31 (Trick Room mons Spe IV 0), 252/252/4-style EVs by role |
| Sets | Standard sets minus the nastiest tool (setup / sleep / signature ability swapped, e.g. Toxapex Limber, Araquanid-free) | Full sets: 4 moves, ability, item, nature; field-synergy core of each team is present | Upgraded coverage, Hidden Abilities, Megas (trainer gets `MEGARING`), Choice/Life Orb/Weakness Policy, one extra synergy piece |
| Bag items | Standard −1 | 1 Potion (cap 15) → 1 Super (to 23) → 2 Super → 2 Hyper → 2 Full Restore | 2 Super → 2 Hyper → 2 → 3 Full Restore |
| AI skill | trainer type's own (Core sets no ceiling) | trainer type's own | Core floor 48 (`ai_skill_min`) |

Rules of thumb used when writing teams:
- **Every team has one "field engine"** (the mon that turns the field on or abuses it hardest) and **one honest answer** the
  player can learn from the field notes (e.g. Ground moves short out Neon Grid; Rain/Surf quench Volcanic).
- Standard never uses: OHKO moves, evasion abilities (Sand Veil/Snow Cloak), Moody, Baton Pass chains, sleep + Dream
  Eater loops, Shadow Tag. Hard may use Shadow Tag (Gothitelle) and Perish trapping (Mega Gengar) once each.
- Moves learned "early" (by level-up above the mon's level) are allowed only on Hard. The validator warns about them
  (34 Hard-only warnings at the moment, all intentional); Standard and Casual have zero.

## 2. Level curve

Double battles (story, SPINE Rev 14): **Gyms 2, 6, 11, 16, 17** (`GYMS[:double]`; `Prismfall.gym_battle` sets the rule).
Gym 1 (Dorian) is always a single battle. Doubles carry the same team sizes as the table below.

Wardens: ace = cap (validator-enforced on Standard/Hard). The curve between caps assumes ~4 levels per gym:
route trainers sit at **previous cap → cap−3**, gym trainers at **cap−4 → cap−2**, wild routes at **previous cap −3 → cap−5**.
The level cap (Core) means grinding past the cap is impossible, so Standard difficulty comes from sets, not levels.

| Gym | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Cap / ace | 15 | 19 | 23 | 27 | 31 | 35 | 39 | 43 | 47 | 51 | 55 | 59 | 63 | 67 | 71 | 75 | 80 | 85 |
| Std size | 3 | 4 | 4 | 4 | 4 | 5 | 5 | 5 | 5 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 6 |
| Hard size | 4 | 5 | 5 | 5 | 5 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 6 |
| Casual size | 2 | 3 | 3 | 3 | 3 | 4 | 4 | 4 | 4 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 |

Rival max levels (Standard; Hard same top, others +1): K1 6 · J1 14 (Saltmere, before Gym 1 since SPINE Rev 14) · K2 21 · K3 33 · J2 33 · K4 42 · J3 47 · K5 54 · K6 66 ·
K7 79. Festival aces (coordinator, SPINE Rev 3): R16 **90** · QF **92** · SF **94** · Final **96** · Hijack **100** · Arceus **100**;
rest of each team 1–4 below. (Casual Festival teams keep 6 mons at −4 levels.) Sister-game cameos are optional sidequest fights
(SPINE Rev 4) — see §6.

## 3. AI skill per trainer class (`trainer_types.txt`)

v21.1 tiers: 1–31 basic (uses Pokémon in order), 32+ adds switching + HP awareness, 48+ high-skill scoring, 100+ adds
ReserveLastPokemon. Skill is per **trainer type**, so difficulty scaling is done by Core (`ai_skill_min` 48 on Hard).

| Class | SkillLevel | BaseMoney |
|---|---|---|
| Wardens 1–2 (Dorian, Tamsin) | 48 | 100 |
| Wardens 3–18, `LEADER_JUNO` | 100 | 100 |
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
| 1 | **Dorian**, Grand Stage, 15, single (SPINE Rev 14) | Aipom *(−C)* 11, **+Hard** Chatot, Minccino 12 (Cute Charm; Hard Technician), Kecleon 15 | none on Standard (Hard: Kecleon Synthetic Seed) | Minccino's two songs raise the applause; stalling lowers it |
| 2 | **Tamsin**, Silkwood, 19, **double** (Rev 14) | Joltik 14, Surskit 15, **+Hard** Vivillon (Rage Powder), Spidops 16 *(−C)*, Swadloon "Bobbin" 19 | Bobbin: Telluric Seed (Hard: Eviolite) | lead pair: Rain Dance wets the silk for Electroweb (spread); Rain douses a Wildfire |
| 3 | Marisol, Water Surface, 23 | Pelipper (Keen Eye; **Hard Drizzle**), Lanturn *(−C)*, **+Hard** Araquanid, Floatzel, Gyarados "Lucky" | Lanturn: Elemental Seed | Lucky's Dive → Underwater |
| 4 | Rook, Neon Grid, 27 | Luxio, Electabuzz *(−C)*, **+Hard** Heliolisk, Toxtricity, Rotom-Wash "Camera" | Electabuzz: Synthetic Seed | Charge reboots a Blackout |
| 5 | Sahar, Desert, 31 | Hippopotas, **+Hard** Dugtrio, Sandaconda *(−C)*, Krokorok, Claydol "Effigy" | Sandaconda: Telluric Seed | sandstorm or Fire Fang bakes a Superbloom back |
| 6 | Corvin, Corrosive Mire, 35, **double** | Galarian Weezing (never Misty Surge), Crobat *(−C)*, **+Hard** Salazzle, Amoonguss, Drapion, Toxapex "Ward" | Crobat: Synthetic Seed | Weezing's Heat Wave ×2 → Wasteland |
| 7 | Brann, Volcanic, 39 | Torkoal, Camerupt *(−C)* (Magma Armor), **+Hard** Centiskorch, Magmortar, Arcanine, Coalossal "Anvil" | Camerupt: Elemental Seed | Lava Plume ×3 re-melts Cinderglass; Anvil is built for Cinderglass |
| 8 | Kaito, Colosseum, 43 | Hawlucha, **+Hard** Medicham, Machamp, Hitmontop *(−C)*, Conkeldurr, Lucario "Memory" (Std Scope Lens; **Hard Mega**) | Hawlucha: Synthetic Seed + Unburden | Frenzy by knockouts |
| 9 | Juno (J3), Flower Garden, 47 | see §5 | Whimsicott: Telluric Seed | growth moves; regrow from Embers |
| 10 | Anja, Frozen Lake, 51 | Alolan Ninetales, Cloyster, Beartic *(−C)*, Walrein, Avalugg, Mamoswine "Matriarch" | Matriarch: Elemental Seed (Hard: Life Orb) | Body Press / High Horsepower crack the lake → Water Surface; Ice moves refreeze |
| 11 | Odessa, Stormfront, 55, **double** | Pelipper (Keen Eye, Tailwind), Swanna *(−C)*, Pom-Pom Oricorio, Noivern, **Kilowattrel** (replaces Talonflame), Corviknight "Taxi" | Oricorio: Elemental Seed | Noivern's Sunny Day ×2 → Rainbow |
| 12 | Ilsa, Mindscape, 59 | Bronzong, Musharna *(−C)*, Espeon, Gothitelle (Hard: Shadow Tag), Reuniclus, Hatterene "Hush" | — | Hush's Psychic Noise ×3 → Inverse; Calm Mind ×2 calms a Nightmare |
| 13 | Bastian, Crystal Cavern, 63 | Carbink, Alolan Golem *(−C)*, Aurorus, Dusk Lycanroc, Rhyperior, Gigalith "Geode" (Sturdy, no Sand Stream) | Geode: Magical Seed (Hard: Weakness Policy + Meteor Beam) | Golem's Explosion or 3 quakes → Cave; light moves relight a Dark Crystal |
| 14 | Ysolde, Hollow Cathedral, 67 | Sableye, Spiritomb *(−C)*, Dusknoir, Cofagrigus, Gengar (**Hard Mega + Perish Song**), Chandelure "Vigil" | Cofagrigus: Magical Seed | Curse / Destiny Bond re-haunt a consecrated nave |
| 15 | Magnus, Factory, 71 | Ferrothorn, Excadrill *(−C)* (Mold Breaker), Kingambit, Klinklang "Mark One", Scizor, Metagross "Engine" (**Hard Mega**) | Mark One: Synthetic Seed | Magnet Rise + Wild Charge restart a Scrapyard; nobody quakes |
| 16 | Nyx, New Moon, 75, **double** | Grimmsnarl, Weavile, Malamar *(−C)*, Umbreon (Wish), Zoroark "Nobody" (slot 5, Illusion of Honchkrow), Honchkrow | Weavile: Magical Seed (opens the Abyss) | Night Daze ×3 → Abyss; Dark attacks snuff the Lamplight |
| 17 | Celestine, Fairy Tale, 80, **double** | Alcremie, Mimikyu *(−C)*, Azumarill, Tinkaton, Togekiss "Vigilant", **Sylveon "Vow"** (ace, per 03_CAST) | Alcremie: Magical Seed | Fairy attacks ×3 tame a roused Dragon's Den |
| 18 | Sigrun, Dragon's Den, 85 | Flygon, Kommo-o, **Dragonite** *(−C)* (Multiscale; replaces Goodra), Haxorus, Dragapult, Salamence "Dreamwing" (**Hard Mega**) | Dreamwing: Amulet Coin (status-proof in the Den) | Draco Meteor reopens a cooled Cave; Dragon attacks retake a Fairy Tale |

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
| K3 (33) | Staravia, Krokorok *(−C)*, Doublade (Eviolite), starter — Hard +Scyther |
| K4 (42) | Staraptor, Krookodile *(−C)*, Scizor, Doublade, starter — Hard +Zweilous |
| K5 (54) / K6 (66) | Staraptor, Krookodile *(−C)*, Scizor, Zweilous→Hydreigon (K6), starter, **Aegislash "Morwen"** |
| K7 (79) / K8 (94) | Staraptor, Krookodile *(−C)*, **Mismagius** (from Ysolde), Hydreigon, starter, **Aegislash** ace |
| J1 (14) | Cottonee *(−C)*, Bounsweet "Sweetpea", starter (unevolved) — Hard +Petilil. Saltmere, before Gym 1 (Rev 14) |
| J2 (33) | Whimsicott, Lilligant *(−C)*, Steenee, starter — Hard +Floette "Everbloom" (white, SPINE Rev 12) |
| J3 (47, `LEADER_JUNO` 30–32) | Whimsicott (Telluric Seed), Florges "Everbloom" *(−C)* (white, Flower Veil), Lilligant, starter, ace **Tsareena** — Hard +Roserade "Rowan". Flower Garden: the seed, Growth, Leech Seed, Aromatherapy and Grassy Terrain grow the garden; burn it down with Fire at stage 5. |
| J4 (90) | Florges "Everbloom", Whimsicott, Lilligant, Comfey, starter, **Tsareena** |

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
  | `GILDED_THEODRIC,Theodric,0` | Golurk, Aegislash, Kyogre, Groudon, Regigigas, **Gholdengo "Gilt"** (100) |
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

## Intentional non-learnable moves (validator allowlist)

Rows here are read by `tools/validate_trainers.py`: `| TYPE,Name,Version | SPECIES | MOVE or ABILITY | reason |`.
Version `*` = every version of that trainer. Rotom's appliance moves are granted by its form handler and are special-cased
in the validator, so they need no row.

| Trainer | Species | Move | Reason |
|---|---|---|---|
| FESTIVAL_LIN,Lin,* | TOGEKISS | OBLIVIONWING | Lin's Reborn signature: a Togekiss with an illegal move (CAMEOS.md). Casual swaps it for Air Slash. |
| LEADER_ILSA,Ilsa,* | HATTERENE | PSYCHICNOISE | Legal in Scarlet/Violet (TM 213); the base pokemon.txt has no DLC TM learnsets. Her transition play: 3 damaging sound moves crack the Mindscape into the Inverse Field (TRAINER_FIELD_PLAYBOOK.md). Casual uses Psychic. |

## Status

- Wardens, rivals (K1–K9, J1–J4, J7), villains/admins (Thistle, Teo, Ch21 foes), Valen/Voss/Quent/Theodric/Morwen,
  every Festival entry in NARRATIVE_KEYS §7 (Rev 5/6), the Ruin teams, the cameo sidequests and
  every route/gym trainer the built maps reference: **done, 0 validator errors** (`--maps maps_out/Data`: all resolve).
- Not trainer data (specified in §7 for Prismfall Bosses): the Arceus configs, `GIRATINA_ORIGIN_TRIAL`, `KYOGRE_WEATHER`.
- Rev 10 field re-tune: done for Wardens, rivals, Thistle, Teo, Valen, Voss, the Festival draws and the route trainers
  (TRAINER_FIELD_PLAYBOOK.md). Not re-tuned: cameo sidequests, Quent, Theodric, the Ch21 tag foes.
- Still no teams: the Mourner, Wick, Sable, Ashe, pre-Ch21 Marchetti/Quent/Kroll fights.
- **Eevee Octave (SPINE Rev 19):** provisional teams from the Trials workstream in `pbs/trainers_trials.txt`
  (`OCTAVE_SINGER <name>` v50 kingdom duels at the next cap − 1, v60 gauntlet bouts at 90 with Z-crystals,
  `OCTAVE_VESPER Vesper` v60 Eevee 92 with the Eevium Z); levels, balance findings and the retired v0 Carol / v1–8 / Vesper v2
  sets: `design/EEVEE_OCTAVE.md` §4 and mapgen/REQUESTS.md ("From the Eevee Octave workstream"). For the trainer designer to tune.
- Pending: war-arc soldier/officer teams (types `ASHKAAR_*` / `ISENMAR_*` exist; teams once the story lead writes the war);
  new maps' trainers as they are generated.
