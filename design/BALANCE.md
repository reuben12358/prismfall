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
| Bag items | Standard −1 | 1 Super Potion → 2 Super → 2 Hyper → 2 Full Restore | 2 Super → 2 Hyper → 2 → 3 Full Restore |
| AI skill | trainer type's own (Core sets no ceiling) | trainer type's own | Core floor 48 (`ai_skill_min`) |

Rules of thumb used when writing teams:
- **Every team has one "field engine"** (the mon that turns the field on or abuses it hardest) and **one honest answer** the
  player can learn from the field notes (e.g. Ground moves short out Neon Grid; Rain/Surf quench Volcanic).
- Standard never uses: OHKO moves, evasion abilities (Sand Veil/Snow Cloak), Moody, Baton Pass chains, sleep + Dream
  Eater loops, Shadow Tag. Hard may use Shadow Tag (Gothitelle) and Perish trapping (Mega Gengar) once each.
- Moves learned "early" (by level-up above the mon's level) are allowed only on Hard. The validator warns about them
  (34 Hard-only warnings at the moment, all intentional); Standard and Casual have zero.

## 2. Level curve

Wardens: ace = cap (validator-enforced on Standard/Hard). The curve between caps assumes ~4 levels per gym:
route trainers sit at **previous cap → cap−3**, gym trainers at **cap−4 → cap−2**, wild routes at **previous cap −3 → cap−5**.
The level cap (Core) means grinding past the cap is impossible, so Standard difficulty comes from sets, not levels.

| Gym | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Cap / ace | 15 | 19 | 23 | 27 | 31 | 35 | 39 | 43 | 47 | 51 | 55 | 59 | 63 | 67 | 71 | 75 | 80 | 85 |
| Std size | 3 | 4 | 4 | 4 | 4 | 5 | 5 | 5 | 5 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 6 |
| Hard size | 4 | 5 | 5 | 5 | 5 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 6 |
| Casual size | 2 | 3 | 3 | 3 | 3 | 4 | 4 | 4 | 4 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 |

Rival max levels (Standard; Hard same top, others +1): K1 6 · J1 17 · K2 21 · K3 33 · J2 33 · K4 42 · J3 47 · K5 54 · K6 66 ·
K7 79. Festival aces (coordinator, SPINE Rev 3): R16 **90** · QF **92** · SF **94** · Final **96** · Hijack **100** · Arceus **100**;
rest of each team 1–4 below. (Casual Festival teams keep 6 mons at −4 levels.) Sister-game cameos are optional sidequest fights
(SPINE Rev 4) — see §6.

## 3. AI skill per trainer class (`trainer_types.txt`)

v21.1 tiers: 1–31 basic (uses Pokémon in order), 32+ adds switching + HP awareness, 48+ high-skill scoring, 100+ adds
ReserveLastPokemon. Skill is per **trainer type**, so difficulty scaling is done by Core (`ai_skill_min` 48 on Hard).

| Class | SkillLevel | BaseMoney |
|---|---|---|
| Wardens 1–2 (Tamsin, Dorian) | 48 | 100 |
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

Kingdoms (Rev 3): Elowen = Gyms 1, 2, 9, 17 · Isenmar = 3, 10 · Zenith = 4, 11, 15 · Ossaria = 5, 13 · Nadir = 6, 8, 16 ·
Ashkaar = 7, 18 · Antumbra = 12, 14.

1. **Tamsin — Silkwood (cap 15).** Joltik, Surskit *(−C)*, **+Hard** Vivillon, ace **Swadloon "Bobbin"** (Eviolite, Overcoat).
   Silkwood makes Electroweb/String Shot never miss and String Shot −2 Spe, Fury Cutter ×1.2 (cutting) + Bug ×1.5,
   Swarm always on, Bug types heal 1/16. The plan is speed control → Swadloon outlasts. Answer: Fire ×1.3 and 3 Fire moves
   burn the field to Ashen Waste; Flying is ×0.8 here, so bring Fire.
2. **Dorian — Grand Stage (19), DOUBLE battle** (hence one extra mon at every difficulty: 4 / 5 / 3). Chatot, Ambipom
   (Technician Dual Chop/Swift; Hard Fake Out), Loudred *(−C)* (Hard spread Hyper Voice), **+Hard** Furfrou, ace **Kecleon**
   (Color Change = costume change; Hard: Protean + Fake Out ×1.5). Sound ×1.5 + Normal ×1.5 make Chatter/Uproar/Echoed Voice
   the threats; Sing gets ×1.3 accuracy (Hard Chatot drops Sing for Taunt). Answer: Fighting, Soundproof, and no weather.
3. **Marisol — Water Surface (23).** Pelipper (Drizzle; rain +3 turns on this field), Lanturn *(−C)*, **+Hard** Araquanid,
   Floatzel (Swift Swim is always ×1.5 here), ace **Gyarados "Lucky"** (Intimidate; Hard Dragon Dance). Electric is ×1.5 vs
   grounded — Lanturn punishes your Grass/Electric answers via Volt Absorb. Hazards and Ground moves fail on this field.
   Answer: Electric on Flying/Levitating users, Grass; 3 Ice Beams freeze the lake (Frozen Lake, removes Swift Swim boost).
4. **Rook — Neon Grid (27).** Luxio, Electabuzz *(−C)*, **+Hard** Heliolisk (Dry Skin), Toxtricity (Punk Rock; Plus/Minus
   +1 SpA on entry; Hard Overdrive + Throat Spray), ace **Rotom-Wash "Camera"** — Hydro Pump gets the field's 30% paralysis.
   Answer: Ground types (immune and two Earthquakes short the grid to no field).
5. **Sahar — Desert (31).** Hippopotas (Sand Stream, Smooth Rock → 8+3 turns), **+Hard** Dugtrio (Arena Trap), Sandaconda
   *(−C)* (Sand Spit, Glare), Krokorok (Moxie; Sand Tomb ×2 traps), ace **Claydol "Effigy"** (Levitate; Hard Scorching Sands ×1.5).
   Answer: Water/Grass (Water is ×0.8 here, Grass neutral — bring Grass); Ice users lose 1/16 per turn.
6. **Corvin — Corrosive Mire (35).** Galarian Weezing (Levitate; **never** Misty Surge — it would purify the field),
   Crobat *(−C)*, **+Hard** Salazzle (Corrosion; its Fire moves ignite the fumes for 1/8 to every non-Fire mon), Amoonguss,
   Drapion (Sniper), ace **Toxapex "Ward"** (Merciless + the field's 20%/turn poison = constant crits; Casual: Limber).
   Poison hits Steel here, so Steel walls fail. Answer: Ground/Psychic, and Misty Terrain or Purify ×2 to convert the field.
7. **Brann — Volcanic (39).** Torkoal (Drought; sun +3 turns), Camerupt *(−C)* (Solid Rock; Hard Eruption), **+Hard**
   Centiskorch, Magmortar, Arcanine, ace **Coalossal "Anvil"** — on Volcanic its Rock moves also hit as Fire, Tar Shot doubles
   Fire, Steam Engine/Heat Crash. Grounded non-Fire take burn chip every turn. Answer: Water — but sun halves it, so remove
   Torkoal first; 2 Surfs (or rain) quench to Ashen Waste.
8. **Kaito — Colosseum (43) [assume: Fighting ×1.5, contact ×1.2, a "crowd" Attack boost on KO].** Hawlucha (Unburden +
   Sitrus), **+Hard** Medicham (Pure Power), Machamp (No Guard Dynamic Punch), Hitmontop *(−C)*, Conkeldurr (Guts + Flame Orb),
   ace **Lucario "Memory"** (Std special Life Orb; **Hard Mega Lucario**, physical Swords Dance/Meteor Mash/ES).
   Answer: Psychic/Flying/Fairy, Intimidate, burns (except vs Conkeldurr).
9. **Juno (J3) — Flower Garden (47)** — see §5.
10. **Anja — Frozen Lake (51) [assume: Ice ×1.5, Slush Rush active, Fire melts → Water Surface].** Alolan Ninetales (Snow
    Warning + Aurora Veil), Cloyster (Skill Link Shell Smash; Casual: no Shell Smash), Beartic *(−C)* (Slush Rush), Walrein,
    Avalugg, ace **Mamoswine "Matriarch"**. If you melt the lake it becomes Water Surface, which still favours Cloyster/Walrein.
    Answer: Fire + Steel + Fighting, and Brick Break the veil.
11. **Odessa — Stormfront (55) [assume: Flying ×1.5, wind moves boosted, Hurricane/Thunder never miss, Tailwind +2 turns].**
    Pelipper (rain makes Hurricane perfect), Swanna *(−C)*, Pom-Pom Oricorio (Dancer copies dances), Noivern, Talonflame
    (Gale Wings), ace **Corviknight "Taxi"** (Mirror Armor, Bulk Up/Roost). Answer: Electric/Rock, Ground-immune-proof leads.
12. **Ilsa — Mindscape (59) [assume: Psychic ×1.5, Trick Room +3 turns, grounded priority blocked].** Bronzong, Musharna
    *(−C)*, Espeon (the fast exception, Magic Bounce), Gothitelle (Hard: Shadow Tag), Reuniclus (Magic Guard LO), ace
    **Hatterene "Hush"**. Trick Room team (Hard: Spe IV 0). Answer: Dark/Ghost/Bug, Taunt, or stall Trick Room out.
13. **Bastian — Crystal Cavern (63) [assume: Rock ×1.5, gem/light moves boosted, Dark moves darken → Dark Crystal].**
    Carbink (screens + Rocks), Alolan Golem *(−C)* (Galvanize), Aurorus (Refrigerate), Dusk Lycanroc (Tough Claws Accelerock),
    Rhyperior (Solid Rock, AV), ace **Gigalith "Geode"** (Sand Stream SpD boost; Hard Weakness Policy + Meteor Beam).
    Answer: Water/Grass/Fighting/Steel; using Dark moves to darken the cave weakens his boosts.
14. **Ysolde — Hollow Cathedral (67) [assume: Ghost ×1.5, sound ×1.5, Will-O-Wisp never misses].** Sableye (Prankster),
    Spiritomb *(−C)*, Dusknoir, Cofagrigus (Mummy), Gengar (**Hard Mega Gengar + Perish Song**), ace **Chandelure "Vigil"**.
    No Mismagius (it goes to Kestrel after K6, per cast). Answer: Dark types, Normal-type pivots, Infiltrator-proof bulk.
15. **Magnus — Factory (71) [assume: Steel ×1.5, Electric ×1.2, gear moves double effect, Explosion → Scrapyard].**
    Ferrothorn, Excadrill *(−C)*, Kingambit (Gen 9 upgrade of the cast's Bisharp), Klinklang "Mark One" (Shift Gear), Scizor,
    ace **Metagross "Engine"** (AV; **Hard Mega Metagross**). Answer: Fire/Ground; wrecking the Factory into Scrapyard ends gear boosts.
16. **Nyx — New Moon (75) [assume: Dark ×1.5, Psychic/Fairy weakened, accuracy of status moves up].** Grimmsnarl (Prankster
    screens), Weavile, Malamar *(−C)* (Contrary Superpower), Umbreon, ace **Zoroark "Nobody"** in slot 5 with Honchkrow
    last — **Illusion disguises the ace as Honchkrow**. Answer: Fairy/Fighting/Bug; check for the illusion before committing.
17. **Celestine — Fairy Tale (80) [assume: Fairy ×1.5, Steel "knight" moves ×1.5, Dragon weakened].** Alcremie, Mimikyu
    *(−C)*, Azumarill (Huge Power; Hard Belly Drum), Tinkaton (Gigaton Hammer), Sylveon (Pixilate Hyper Voice), ace
    **Togekiss "Vigilant"** (Serene Grace Air Slash). Answer: Steel/Poison; Tinkaton punishes Steel, so lead Poison.
18. **Sigrun — Dragon's Den (85) [assume: Dragon ×1.5, Fire ×1.5, Ice ×0.5, magma chip on grounded non-Fire/Dragon].**
    Flygon (Scarf), Kommo-o (Clangorous Soul + Throat Spray), Goodra *(−C)*, Haxorus, Dragapult, ace **Salamence "Dreamwing"**
    (**Hard Mega Salamence**, Aerilate Double-Edge). Answer: Fairy + Ice (Ice is halved here: bring Fairy + Steel).

## 4b. Route and gym trainers (stock trainer types)

Built from the Map Builder's events (`maps_out/Data/*.rxdata` / `trainers_needed.txt`). Rules: no bag items, level-up
movesets (always level-legal), IV 8 Standard / 20 Hard / 0 + EV 0 Casual, Casual −1 level, Hard +1 level.
Levels: Route 1 4–5 · Route 2 6–7 · Gossamer Wood 8–10 · Loomhouse Gym 11–13 · Deepwood 11–12 · Route 3 12–14 ·
Route 4 14–16 · Pell Playhouse actors 15–18 · Pageant Hall grunts 16–17; species from `encounters.txt` for that map,
leaning Bug/Grass/Normal/Fairy (Elowen). `[YOUNGSTER,Ben]` (map 990 test dummy, Snorlax Lv 50) collides with the base
project's sample Ben — ours normally compiles later and wins, but packaging should drop the base sample trainers.
**Generic villains** (`HOLLOW_GRUNT_M/F`, `MERIDIAN_AGENT_M/F`, name "Grunt"/"Agent"): version = encounter number
(0 = Saltmere Pageant Hall tag battle, then 1, 2, ... in story order; < 100), +100/+200 as usual. Map events must pass
the version. Named admins (Thistle v0 = Briarwick, Lv 13–15) use 0, 1, 2 ... per rematch.
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
| J1 (17) | Cottonee *(−C)*, Bounsweet "Sweetpea", starter — Hard +Petilil |
| J2 (33) | Whimsicott, Lilligant *(−C)*, Steenee, starter — Hard +Shiinotic |
| J3 (47, `LEADER_JUNO` 30–32) | Whimsicott, Shiinotic *(−C)*, Lilligant, starter, ace **Tsareena** — Hard +Roserade "Rowan". Flower Garden: Growth/Quiver Dance/Leech Seed grow the garden; burn it down with Fire. |
| J4 (90) | Shiinotic, Whimsicott, Lilligant, Comfey, starter, **Tsareena** |

## 6. Festival of Champions

- **Valen** (`CHAMPION_VALEN,Valen`, ace 96): Bronzong, Lapras "Ferry", Kingdra, Gallade (**Hard Mega Gallade**), Volcarona,
  **Zygarde** (50%, **Power Construct** → Complete Forme below half HP). Suggested field: none or `:RAINBOW` (balanced team, his
  field is "order").
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
  **v2** post-game at 100, each +100/+200. Shelly v1 17 (double; Lv-17 roster: Masquerain, Joltik, Larvesta, Scyther, Hard
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
`ARCEUS_BOUND` has 6 bars; bar *k* holds the Plates of gyms 3k−2..3k (bar 1 Bug/Normal/Water … bar 6 Dark/Fairy/Dragon), so
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
- **Field team:** Gyms 8–18 teams assume the **[assume]** notes above; tell balance if a field lands differently.
  Galarian Weezing deliberately never has Misty Surge. Voss's Silvally hook and the Arceus Plate hook are specified in §6–7.
- **Story:** nicknames used — Bobbin, Lucky, Camera, Effigy, Ward, Anvil, Memory, Matriarch, Taxi, Hush, Geode, Vigil,
  Mark One, Nobody, Vigilant, Dreamwing (aces); Morwen (Kestrel's Honedge line), Sweetpea (Juno's Bounsweet line),
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

## Status

- Wardens, rivals (K1–K9, J1–J4, J7), villains/admins (Thistle, Teo, Ch21 foes), Valen/Voss/Quent/Theodric/Morwen,
  every Festival entry in NARRATIVE_KEYS §7 (Rev 5/6), the Ruin teams, the cameo sidequests and
  every route/gym trainer the built maps reference: **done, 0 validator errors** (`--maps maps_out/Data`: all resolve).
- Not trainer data (specified in §7 for Prismfall Bosses): the Arceus configs, `GIRATINA_ORIGIN_TRIAL`, `KYOGRE_WEATHER`.
- Pending: war-arc soldier/officer teams (types `ASHKAAR_*` / `ISENMAR_*` exist; teams once the story lead writes the war);
  new maps' trainers as they are generated.
