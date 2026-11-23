# MEGA_EVOLUTION — Mega Evolution in Prismfall (SPINE Revisions 20 and 21)

> User (Rev 20): "speaking of adding z moves, u also gotta add mega evolutions."
> SPINE Rev 20: Megas are earned the Reborn/Rejuvenation way (the ring from a story beat, stones from quests, puzzles and
> exploration after badges); Wardens and bosses Mega Evolve where it fits their theme and field; Megas, Z-moves and fields
> work together; one Mega and one Z-move per side per battle, under EBDX.
> User (Rev 21): "see how late reborn/rejuv give out the mega ring, its usually like later gyms" and "Every important
> story fight after level 50-55 ish should have mega evolutions", then, of Brann's Mega Camerupt: "he could have one as
> long as its considered 'Weak'".
> SPINE Rev 21: the Mega Ring comes **after Badge 13** (cap 63) from a story beat; earlier stones "hum and wait". From an
> ace of about 50 (Gym 10 on) **every important story fight has a Mega**, any tier, before the player has a ring; below
> that only a **weak** Mega, and only where the design calls for it. No theme exceptions. The Eevee Octave keeps Z.

Status: **working** in the headless harness (run_mega.rb, see §8) and in the real engine (the player's EBDX Mega button,
the Mega animation, the AI's Mega, on a Prismfall field; Rev 20 capture). Code: `plugins/Prismfall Mega/` (4 files).
Quests: `plugins/Prismfall Trials/114_Quests_Megas.rb`, `132_EventMons_Megas.rb`, `152_Talk_Megas.rb`. Map events:
`design/TRIAL_EVENTS.yaml` ("Mega Evolution" maps). Trainers: `tools/trainer_gen/gen.py` (`mega=` on a Pokémon,
`MEGA_FROM`, `WEAK_MEGA`) → `pbs/trainers.txt`. Tests: `tools/harness/run_mega.rb` (report `docs/mega_test/REPORT.md`),
`tools/harness/run_winrates.rb` (cells G7M, G10M, K5M, G11M; round 4 renamed them, §9 of BALANCE.md), `tools/harness/playtest/run_mega.sh` (GIF
`docs/battle_captures/mega/mega_evolution_ebdx.gif`).

---------------------------------------------------------------------------------------------------
## 1. Lore: heartstones and rings

Prismfall's Megas come out of the Plates and Imprints (story/01_WORLD_LORE.md §3, §5), so the story team can use them:

### 1.1 Heartstones and Warden's rings
- **A Mega Stone is a heartstone.** Where an Imprint soaks into one line of Pokémon for long enough, it pearls inside
  them, the way Imprints condense into seeds at their borders. Velmorans say *heartstone*; the Accord says *Mega Stone*.
  Holding one, a Pokémon can carry its whole Imprint for one battle. That's why the stones turn up in Imprint-heavy
  places: the Cinderhorn slag, the Bride Tree's roots, a sap tree, a lighthouse lens.
- **A Mega Ring is a Warden's ring.** It is a gold band holding a chip of stone with no colour at all. The chip is
  **grind**: dust from the Crown's own stone (in truth the Legend Plate shard, which only the Secret Articles say),
  kept by Cindervault's **Hearthguild**. It has no colour of its own, so it takes any colour and opens any heartstone.
  The guild has cut one ring for every Warden's seat since the Concordance.
  - **What anyone may say before Ch15:** "grind off the Crown's own stone", nothing more. Nobody names the Legend Plate
    or says "reset": 09_MYSTERIES #5 (the One in Keeping is the Legend Plate) and #6 (the Crown is cracked) are revealed
    in Ch15–17. Bastian's Ch14 account of the AF 290 break is #6's planned mid-clue and stays as written.
- **One heart at a time.** Two rings on the same side "ring against each other". That is the in-world reason for the
  rule of one Mega per side, partner battles included.

### 1.2 Who carries a ring (story and theme first: a fighter Megas only if the story gives them a ring)
The user (Rev 21): "dont make one off exceptions, keep it in theme/story". So the "every important fight from Lv 50 has
a Mega" rule gives way wherever the story gives the fighter no ring by then, and no ring is invented to make it fit.
- **Wardens** are Accord officers: every seated Warden has a Hearthguild ring, and Valen wears the Sovereign's. That
  covers the gyms, the Festival's Warden draws and exhibitions, and the Ruin route's Wardens.
- **Meridian has the tech.** It can't buy Crown grind, so its R&D (Quent's Arbiter people) makes its own keystone, a
  sliver of **Lattice-glass** in a steel band that *forces* a heartstone open instead of answering it. Meridian's own
  people use them: **Voss, Quent, Marchetti (Security Directorate), Kroll (Special Accounts) and the Directorate
  Captain.** Bands never sing, and Meridian doesn't lend them out.
- **Juno** inherits Rowan's Grass Warden's ring with the seat (his testament, 06_ACT_III Ch10). At first it won't answer
  her (the Heartgarden scene after J3); **by the Festival (J4) it does**, and she Megas her **Gardevoir "Veil"**.
- **Kestrel** has no ring of his own: **no Mega at K1–K7**. **Morwen's Ring** (Key Item, 07_ACT_IV Ch15) is with Edda
  until she gives it to the PC at Morwen's grave, and reaches Kestrel only through the PC (`:ch18_kestrel_ring`). Given
  in Ch18, it answers him the first time he wears it: **K8 Megas his Scizor**, his duelist since K4
  (`PrismfallMega::MORWEN_RING`, at battle start). Given at the SF instead (after K8), it first shows in the hijack tag
  battle, on the player's side. K9 happens only if he never got it: no Mega.
- **The PC's ring** is the odd one out (§4).
- **No ring in the story, so no Mega:** listed in §6.3 (Rowan and the Mourner, Archseer Imre Dask, Morwen's Echo,
  Theodric, the war officers). Sister-game cameo champions bring the rings of their own worlds (their Hard teams).

### 1.3 Foreshadowing (09_MYSTERIES #1)
The PC's ring was cut by Brann "ten years back" from the grind of the AF 290 reset (nobody says that part), the same
break the splinter flew from. It "sulked" on every hand and went to Bastian, under his mountain. It **sings** for the PC.
Brann's Ch8 chestnut slip ("After the accident. Ten years back.") and Bastian's Ch14 crown story bracket it: a player can
put the three together before Ch17 says it. Pre-Ring stones hum when the PC picks them up, and go quiet at the Ring-Day.

Z-crystals stay what EEVEE_OCTAVE.md made them: slivers of Glassfall glass, each tuned by the Choir to one Imprint.
**SPINE Rev 23: the same Warden's ring wakes them** ("the glass came out of the night it cracked. Same crown, one way or another"), so the player
has one ring for both; Vesper's Z-Power Ring is no longer handed out. Crystals, their placement and the Z users:
`design/Z_MOVES.md`.

---------------------------------------------------------------------------------------------------
## 2. Study: how Reborn and Rejuvenation hand out Megas

Sources: BigJra's walkthroughs (Reborn 19.5.18, Rejuvenation 14.0.28; saved at `/home/claude/dl_bigjra_*`). Each stone
and enemy Mega was timed against the badge headings (`/home/claude/work/mega/timeline.py`). The games' own scripts were
read for the rules (`ref/games/reborn/Scripts/Battle.rb` `pbMegaEvolve`, Rejuvenation `Battle.rb`, `PokemonBossBattle.rb`).

| | Reborn (18 badges) | Rejuvenation (18 badges) |
|---|---|---|
| The ring | **Mega-Z Ring** (Mega + Z in one) from DJ Arclight's quest (return five Pokémon bought from the Seventh Street seller), Episode 16, **after badge 12**. "If we skip this section... locked for another two badges." | **Omni Ring** (Mega + Z): an optional chain (Mega Bangle sidequest: Secret Patent → Updated Patent → a casino crafter wanting shards, Heart Scales, Blast Powder, Dawn and Shiny Stones), about **badge 11**; otherwise given at Axis High graduation, about **badge 14**. Rival Karen gets a Mega Ring in Chapter 2 and the player doesn't ("Consolation prize..."). |
| Stones before the ring | From **badge 8** (Ampharosite in the Underroot): "We can't use Mega Stones or Z-Crystals yet." 3 more by badge 11 (Aerodactylite, Banettite for a Floral Charm, Charizardite X behind Charlotte's gym secret, Abomasite). | From **badge 4** (Steelixite), then Meowsticite, Charizardite X, Chandelurite (a grave puzzle), Houndoominite, Banettite **or** Heracronite ("though we can't use them yet"). |
| Bulk of the stones | Badges 12–15: quest rewards (Venusaurite for four mulches, Absolite for funding three projects, Houndoominite from a PC girl, Lopunnite from a computer), puzzle and exploration finds (Sablenite and Gyaradosite in the glass-pallet puzzle, Heracronite after changing a field, Pinsirite up a waterfall). | Badges 8–15: help-center quest rewards (Abomasite, Mawilite, Altarianite "+1 Karma"), gauntlets (Cameruptite, Audinite with a shiny Eevee), relationship gifts (Greninjite at 45 points), hidden finds. |
| Strongest stones | **Badge 17**: Tyranitarite, Gengarite, Metagrossite, Lucarionite, Salamencite. Garchompite 12, Mawilite/Gardevoirite 12, Kangaskhanite 15, Alakazite 16. | Badges 13–15: Gengarite 13, Tyranitarite/Scizorite/Lucarionite/Salamencite 14, Metagrossite/Gyaradosite 15. |
| Legendary stones | Post-game. | Post-game. |
| First enemy Megas | A single-Pokémon **boss Mega Steelix at badge 6**; the first leader Mega is **Ciel's Mega Altaria at badge 12**; then nearly every major fight (Adrienn's Mawile 13, Titania's Scizor 14, Solaris's Garchomp 15, the Elite Four). | A **boss SOS Mega Charizard X at badge 6**; the first leader Mega is **Mega Banette at badge 8**, before the player can Mega; then Alakazam 11, Pidgeot 12, Blastoise 13. |
| Rules | One Mega per trainer (`@megaEvolution[side][owner]`). On Mega Evolution, switch-in abilities re-run (`pbAbilitiesOnSwitchIn(true)`), which re-runs the fields' ability effects. Fields have no Mega-specific rules: they work through the Mega's ability and type. | Same; a boss can be scripted to revert a Mega ("steals the charge"). |

**What Prismfall takes (M1–M6):**
- **M1:** the ring is a **story beat late in the game** (Rev 21: after Badge 13, where Reborn's earliest is and just
  before Rejuvenation's), and it is ours alone (not combined with Z).
- **M2:** stones turn up **before** the ring and "hum and wait", as in both games (Reborn 4–5, Rejuvenation about 6;
  ours 12, because they were placed for a ring at 7). All but Alakazite (12 badges) are B-tier or weaker.
- **M3:** after the ring there are **2–5 stones per badge**, spread across quests, Trial ranks, puzzles, bosses and hidden spots.
- **M4:** **S-tier stones come late** (none before 10 badges; most at 13–17); the legendary ones come post-game.
- **M5:** **no stone that answers the next Warden** (rule R4 with the ring, §5.2).
- **M6:** **the foes Mega first** (Rejuvenation's Mega Banette at badge 8, before the player can). Ours: one weak Mega at
  Gym 7 (Brann's Camerupt), then every important fight from Gym 10 (Rev 21), three Wardens before the ring arrives.

Rev 20 had the ring at 7 badges; Rev 21 moved it to 13, so the stones placed for a ring at 7 were re-checked against
the new ring point (§5.3). The ones that stayed before 13 "hum and wait", as in both games.

---------------------------------------------------------------------------------------------------
## 3. Mechanics

### 3.1 What the engine already does
- **Essentials v21.1** has Mega Evolution natively: `Battle#pbCanMegaEvolve?` / `pbRegisterMegaEvolution` /
  `pbMegaEvolve`, the `MegaRing` item flag (the base `MEGARING`), `MegaStone`/`MegaMove` in `pokemon_forms.txt`, the
  AI's `pbEnemyShouldMegaEvolve?` (Mega as soon as it can), and NPC rings via the trainer's `Items` (`pbGetOwnerItems`).
  Megas revert after battle.
- **Elite Battle DX Renovation** draws the **Mega button** on its Fight menu (click it, or press Action, to toggle; the
  move types preview the Mega form). It plays the `MEGAEVOLUTION` + `MEGAEVOLUTION2` ("Primega Shatter") common
  animations and shows the Mega symbol on the databox. Its scripted-battle module also gives each trainer a
  **"mega"/"megaOpp" battle-speech** line (`pbTrainerBattleSpeech`): Wardens can say something as they Mega Evolve (§6).
- **Data:** all 48 Gen 6/7 Megas are in the base PBS (47 stones plus Rayquaza's Dragon Ascent), each with its stone
  item and its sprites. The shipped base (Gen 9 Pack 3.3.8) also carries the **Legends Z-A Megas** (50 forms, the
  new Mega abilities and their sprites). See §3.5.

### 3.2 Prismfall rules (`plugins/Prismfall Mega/002_Mega_Battle.rb`)
- **One Mega per side per battle** (`LIMIT = :side`). Essentials allows one per trainer, so in a tag battle both
  partners could Mega. `pbCanMegaEvolve?` now also says no while another trainer on the same side has chosen or used
  theirs. The player chooses first, so in a partner battle the player's Mega always wins; the partner keeps theirs if
  the player doesn't Mega.
- **One Z-move per side per battle** (`Z_LIMIT = :side`). This is the same rule for Prismfall Z-Power, which is per
  trainer on its own. It works by alias-chaining `PrismfallZ.owner_key` to key on the side alone; no Z-Power file was
  edited (§7 asks the Z owner to adopt it in their config).
- **A Mega and a Z-move may both be used in one battle**, by different Pokémon (one Pokémon has one held item). Tested
  for one trainer, for two trainers on one side, and for the player's side.
- **A Pokémon holding a Z-crystal can't Mega Evolve** (Gen 7). This only matters for stone-less Megas (Rayquaza).
- Event `:prismfall_mega_evolved (battle, battler, old_ability_id)`, and `PrismfallMega.log(battle)` for tests.

### 3.3 Fields (`003_Mega_Fields.rb`)
Neither Reborn nor Rejuvenation has a field rule keyed on "a Mega Evolution happened". Their fields meet Megas through
the Mega's **ability**, because both games re-run switch-in abilities on Mega Evolution. Everything else already
follows the Mega in our engine: type boosts, always-on abilities, speed and damage rules all read the battler as it is
now. A Mega's weather ability (Drought, Sand Stream, Snow Warning) starts its weather through the normal path, so field
weather rules apply.

**Integration bug fixed:** a field's **on-entry rules keyed on abilities** ran only when a Pokémon entered, so a Mega
that gained such an ability got nothing. These are Reborn-style ability entry effects (FIELD_API §4.6), for example
Inverse's Magic Bounce +1 Sp. Def, Colosseum's No Guard +1 Attack, Frozen Lake's Thick Fat +1 Defense and Scrapyard's
Scrappy +1 Attack. Now the rules for the **gained** ability fire at the moment of Mega Evolution, and never twice: a rule
that already matched the old ability is skipped. Affected Megas include Pidgeot (No Guard), Absol, Sableye and Diancie
(Magic Bounce), Slowbro (Shell Armor), Lopunny (Scrappy), Venusaur (Thick Fat) and Sceptile (Lightning Rod).

**Mega showpieces** (Reborn-style flavour, chosen where a Warden's Mega or the field's theme makes them land). Each is a
Field Effects battler-effect rule in `PrismfallMega::FIELD_RULES`, on the current field only:

| Field | When a Pokémon Mega Evolves here | Why |
|---|---|---|
| Grand Stage | the applause rises one stage ("A Mega Evolution! The audience gasps at the costume change!") | the biggest costume change there is; matches Z-Power's Grand Stage showpiece |
| Volcanic | a **Fire-type** Mega primes the volcano: it erupts at the end of the round (Fire types ride it +1, lava 1/8 on grounded non-Fire foes) | Brann's Mega Camerupt is a living volcano (kept as designed, per the user); quenching (Surf ×2 → Cinderglass) is the honest answer |
| Colosseum | the crowd counts it like a knockout toward the Frenzy (not once the Frenzy is on) | Kaito's Festival Mega Lucario plays to the crowd |
| Frozen Lake | an **Ice-type** Mega seals every crack (the crack meter resets) | Anja's Mega Glalie (Gym 10, every mode) undoes one Fire plan |
| Crystal Cavern | the crystals take the Mega's colour if it is Fire, Water, Grass or Psychic | Mega light through a geode |
| Hollow Cathedral | a **Ghost-type** Mega re-haunts a consecrated nave (stage 2 → 1) | Ysolde's Mega Sableye/Gengar |
| Factory | a **Steel-type** Mega's plating is hammered home (+1 Defense) | Magnus's Mega Metagross |
| Bleed | the Bleed lurches at once to new borrowed effects | a Mega pulls a whole Imprint into one body |

No showpiece on the Dragon's Den (Sigrun's Den already favours dragons), Prism Arena (its Plate cycle stays the
Festival's clock) or the rest. **Field Notes:** each showpiece field lists its Mega line. Fields whose ability entry
rules include a Mega ability also say "A Mega Evolution's new ability triggers this field's on-entry ability effects."
These are appended by an alias on `FieldNotes.effect_lines`; no field file was edited. FIELDS.md is generated from the
field files, so the field workstream should add `PrismfallMega::FIELD_NOTES` when they next regenerate it.

### 3.4 Other plugins checked
- **Z-Power:** the two systems are independent (`pbRegisterMove` vs the Mega registration). Mega-stone holders never see
  the Z box. The AI uses both in one battle (§8).
- **EBDX Bridge:** nothing to change. The Mega animation draws over the field backdrops (Volcanic in the capture), and
  the bridge's overlays don't get in its way.
- **Bosses:** HP bars live on the battler, so a trainer boss can Mega Evolve between bars. Wild bosses can't Mega:
  Essentials never lets a wild Pokémon Mega Evolve, and `pbMegaEvolve` needs an owner name. A Rejuvenation-style "Mega
  on shield break" for trainer bosses is a proposal for the Bosses owner (§9).
- **Core:** the rival starter swap already remaps a held Mega Stone to the new species' stone, or to `MEGA_STONE_FALLBACK_ITEM`
  (Life Orb). In the shipped base that also covers the Z-A starter stones (Meganiumite, Feraligite, Emboarite,
  Chesnaughtite, Delphoxite, Greninjite). Level-cap disobedience doesn't stop a Mega, which happens before the move.
- **Gen 9 Pack 3.3.8 (shipped base):** it aliases `pbCanMegaEvolve?` (Commander) and `pbMegaEvolve` (Z-A form hooks), and
  ours chains after both. `CHAMPIONS_MECHANICS` (move locks) didn't touch the Mega in the engine test.

### 3.5 Legends Z-A Megas: in the game's data, not placed yet
The shipped base already has them (data, abilities, sprites), so they are "easy to source". They are **not placed
yet** because the rest of our tooling doesn't know them. The headless harness, `tools/validate_trainers.py` and the
reference PBS (`ref/ebdx/PBS`) are Gen 9 Pack 3.2.5 and have no Z-A stones. A Z-A stone in `pbs/trainers.txt` or a
Trials reward would break every harness compile. **Phase 2**, once the harness copies move to 3.3.8: a short list that
suits our Wardens. Mega Chandelure for Ysolde, Froslass for Anja, Starmie for Marisol, Excadrill for Sahar, Hawlucha
for Kaito, Dragalge for Corvin, Skarmory for Odessa, Malamar for Nyx, Clefable/Floette for Celestine, Dragonite for
Sigrun, Scolipede for Tamsin's Festival team. Their stones would go after badge 12, as in §5.

---------------------------------------------------------------------------------------------------
## 4. The Mega Ring beat: "The Ring-Day" (Chapter 14, Cragholm, after Gym 13)

SPINE Rev 21 withdrew the Ch8 Ring-Day (7 badges); `story/archive/22_SCRIPT_CH8_withdrawn.md` keeps the old scene.

- **When:** right after **Gym 13** (Bastian, Crystal Cavern, cap 63), **13 badges**, before Larch takes the badge case
  apart (`:ch14_telemetry`) and before Marchetti's raid. Unlock `badges >= 13 && !mega_ring`. The raid's admin battle
  (Marchetti in the Darkglass gallery, Mega Houndoom) is the first fight in which both sides can Mega, a few hours later.
- **Why there and him:** Chapter 14 is the crown chapter. Bastian is the eyewitness to the AF 290 break (09_MYSTERIES
  #6's mid-clue), the oldest Warden, half-deaf, "Rock's patient". He has kept the odd ring under his mountain for ten
  years; he Mega Evolved his own Aerodactyl in the gym an hour earlier; and the raid that night needs a ring on the PC.
  The ring's provenance stays Brann's (cut in Cindervault "ten years back"), so the Ch8 chestnut slip still pays off.
- **Where:** Bastian's lamp-room, at the bottom of the Cragholm Lift Galleries (map 363, the deep seams). Pip on a
  crate, Larch by the door with a book she isn't reading.
- **Scene** (`OS_RING_DAY`, hidden, `pf_trial_talk(:BASTIAN_LAMPROOM)`; lines in `114_Quests_Megas.rb`):
  1. "Flawless cut, that was. Don't tell the cavern I said so. It sulks."
  2. What his Amber did in the gym: a Warden's ring (the Hearthguild cuts one for every seat), the colourless chip (grind
     off the Crown's own stone, so it takes any colour), heartstones, and the rule, one Mega to a side ("Remember it in
     a double").
  3. The odd ring: "Holloway cut this one... Ten years back. He sent it to me in a sock, with a note: 'It sulks. Keep it
     where nobody asks questions.'" / "Two old men who don't ask each other things. That's how you get to seventy-four."
  4. **The ring sings**, and something under the PC's ribs answers. Pip: "Grandad, it's SINGING." Bastian, half-deaf:
     "Is it? Can't hear a thing." Then: "...I can feel it in the table, though. Holloway swore they don't sing." Larch
     lowers her book.
  5. The **Aggronite** ("The Aron down the east seam wear these like warts"); earlier stones "are warm now, and quiet,
     as if they had stopped waiting"; and "If Meridian's linesmen come down my lifts tonight, I'd like them to meet a
     ferry child with a Warden's ring."
- **Gives:** `MEGARING` and `AGGRONITE` (Mega Aggron is pure Steel: it answers neither Ysolde nor Magnus). No Trial gong.
  **SPINE Rev 23:** the ring also wakes Z-crystals; Bastian says so in one line ("The chip's grind off the Crown's stone,
  and the glass came out of the night it cracked. Same crown, one way or another. One Z-move a fight, and one to a side,
  same as the hearts"). `design/Z_MOVES.md`.
- **Must not say:** "reset" or "Legend Plate" (checked by `run_mega.rb`). Brann isn't in the scene, so the Light Stone
  choice doesn't touch it; his reaction is in his follow-up below.
- **Follow-up beats:** Marchetti's raid (both sides Mega). **15 badges:** Brann's spare heartstone at the Hearthguild
  (`AS_FORGE_REMEMBERS`, Cameruptite): he knows his ring on the PC's hand ("That's my ring. The odd one. So old Ore
  finally gave it away"), and if `choice(:ch8_lightstone) == :dominar` he says he hasn't forgotten the Light Stone and
  won't talk about it; then "Your ring still singing? ...No. Don't tell me." **Ch15:** Morwen's Ring to the PC (Edda).
  **Ch18/SF:** Morwen's Ring answers Kestrel (his first Mega: Scizor at K8). **J4:** Rowan's ring answers Juno (Mega
  Gardevoir).
- **Story editor:** the scene is written in the Trials data so it plays and tests now. To stage it as a story event,
  keep the lines and call `pbReceiveItem(:MEGARING)` and `pbReceiveItem(:AGGRONITE)` (`mapgen/REQUESTS.md`).

---------------------------------------------------------------------------------------------------
## 5. Stone distribution

### 5.1 The 44 placed stones
| Badges | Stone | Mega (types) | Where (map) | How | Rev 20 |
|---|---|---|---|---|---|
| 2 | Manectite | Mega Manectric (Electric) | The Prize Exchange, rank 3 (Fellow) (194) | Trial rank reward `ZENITH` |  |
| 2 | Glalitite | Mega Glalie (Ice) | The Tally, rank 3 (Harpooner) (306) | Trial rank reward `ISENMAR` | was 11, Frostfang Pass 2F |
| 3 | Ampharosite | Mega Ampharos (Electric/Dragon) | Ferrow Lighthouse lamp room: Hesper's lamp lens (106) | quest `EL_LAMP_LENS` |  |
| 8 | Sceptilite | Mega Sceptile (Grass/Dragon) | The Royal Chase, the old hunting lodge's mantel (682) | item |  |
| 8 | Blastoisinite | Mega Blastoise (Water) | Prism Falls, behind the falls (Surf) (681) | hidden item |  |
| 9 | Venusaurite | Mega Venusaur (Grass/Poison) | The Heartgarden, Verdance: Juno, after J3 (294) | story gift `EL_BRIDE_TREE_HEART` |  |
| 9 | Beedrillite | Mega Beedrill (Bug/Poison) | Gossamer Heartwood, inside the old hive (703) | hidden item |  |
| 10 | Altarianite | Mega Altaria (Dragon/Fairy) | The Tetherline, a cloud-nest on a tether pylon (732) | item |  |
| 10 | Slowbronite | Mega Slowbro (Water/Psychic) | Ebbmouth Sea Grotto, the tide-pool shelf (723) | hidden item |  |
| 12 | Alakazite | Mega Alakazam (Psychic) | Lucent Athenaeum, the Sealed Stacks: the Unread Shelf (345) | **puzzle** |  |
| 12 | Aerodactylite | Mega Aerodactyl (Rock/Flying) | Sahar's Dig Lab, Duneholt: bring her a revived Aerodactyl (209) | quest `OS_AMBER_AGAIN` |  |
| 12 | Pinsirite | Mega Pinsir (Bug/Flying) | Gossamer Heartwood: the Old Pincer (703) | **boss** `EL_OLD_PINCER` |  |
| **13** | **Aggronite** (+ **Mega Ring**) | Mega Aggron (Steel) | Cragholm Lift Galleries, Bastian's lamp-room in the deep seams: with the Mega Ring (363) | story gift `OS_RING_DAY` | was 7, Brann (244) |
| 13 | Gardevoirite | Mega Gardevoir (Psychic/Fairy) | The Looking-Glass Wood, the heart of the mirror maze (752) | **puzzle** |  |
| 13 | Mawilite | Mega Mawile (Steel/Fairy) | The Speculum, Lucent: the smile behind the glass (Rite of Reflection rank 2) (346) | quest `AN_SMILE_BEHIND_GLASS` |  |
| 13 | Scizorite | Mega Scizor (Bug/Steel) | Vane Hall, Gravenmoor: Morwen Vane's trophy case (383) | item |  |
| 13 | Abomasite | Mega Abomasnow (Grass/Ice) | The Hoarwood, under the frost-giant pine (701) | hidden item |  |
| 14 | Absolite | Mega Absol (Dark) | The Slag Mesa, under the warning-cairn on the mesa's lip (801) | hidden item | was 2, Frostwick Pass |
| 14 | Sablenite | Mega Sableye (Dark/Ghost) | Barrow of the Wardens, a looted grave-niche the Sableye mine for its gems (804) | hidden item | was 8, Grudgestone Quarry |
| 14 | Banettite | Mega Banette (Ghost) | Thistledown Manor attic: the doll who waited (547) | quest `EL_DOLL_WHO_WAITED` | was 9 |
| 14 | Pidgeotite | Mega Pidgeot (Normal/Flying) | Gale Post Hall, Skyreach: the dead-letter bag (325) | quest `ZE_RETURN_TO_SENDER` | was 10 |
| 14 | Metagrossite | Mega Metagross (Steel/Psychic) | Strade Works Foundry Floor, the sorting-line puzzle (403) | **puzzle** |  |
| 14 | Gengarite | Mega Gengar (Ghost/Poison) | Barrow Sanctum, the altar of the nameless Warden (805) | item |  |
| 15 | Sharpedonite | Mega Sharpedo (Water/Dark) | Underveil Sump Docks, a harpooned Sharpedo jaw in the net-loft (424) | hidden item | was 2, Tally rank 3 |
| 15 | Swampertite | Mega Swampert (Water/Ground) | The Drownings, a mud-bank islet (Surf) (821) | hidden item | was 8, the Rootdeep |
| 15 | Charizardite Y | Mega Charizard Y (Fire/Flying) | The Brink, the wind-scoured ledge above the drop (832) | hidden item | was 10, Cloudstair Summit |
| 15 | Cameruptite | Mega Camerupt (Fire/Ground) | Hearthguild Hall, Cindervault: Brann's spare (244) | quest `AS_FORGE_REMEMBERS` | was 10 |
| 15 | Charizardite X | Mega Charizard X (Fire/Dragon) | Pyre Keep Dragon Roosts: Old Cinder, a retired Legion war-Charizard (248) | **boss** `AS_OLD_CINDER` | was 11 |
| 15 | Gyaradosite | Mega Gyarados (Water/Dark) | Aurelia - Drowned Spires, the flooded bell (Dive) (824) | hidden item |  |
| 15 | Houndoominite | Mega Houndoom (Dark/Fire) | Underveil Moon Market: the Barons' kennel (Gutter Book) (423) | quest `NA_MOON_MARKET_DOGS` |  |
| 15 | Tyranitarite | Mega Tyranitar (Rock/Dark) | Cragholm rack: the tyrant's heart (Rolls of Unearthing rank 2) (360) | quest `OS_TYRANT_HEART` |  |
| 15 | Garchompite | Mega Garchomp (Dragon/Ground) | The Dry Tide, a sand-sunk caravan (810) | hidden item |  |
| 15 | Salamencite | Mega Salamence (Dragon/Flying) | The Crucible, Cindervault: the brazier writ (Trial by Flames rank 2) (240) | quest `AS_BRAZIER_WRIT` |  |
| 16 | Galladite | Mega Gallade (Psychic/Fighting) | The Gloamwood Verge, the knight's barrow (841) | item |  |
| 16 | Medichamite | Mega Medicham (Fighting/Psychic) | The Iron Pit, the meditation shelf above the top tier (Rock Climb) (263) | hidden item |  |
| 16 | Heracronite | Mega Heracross (Bug/Fighting) | Gossamer Wood, the old sap tree (524) | hidden item |  |
| 16 | Lopunnite | Mega Lopunny (Normal/Fighting) | Pell Playhouse, the Grand Stage: Dorian's encore (154) | quest `EL_ENCORE` |  |
| 16 | Kangaskhanite | Mega Kangaskhan (Normal) | Frostflat Causeway: the Causeway Matriarch (560) | **boss** `IS_CAUSEWAY_MATRIARCH` |  |
| 17 | Steelixite | Mega Steelix (Steel/Ground) | Wyrmscar Rift, an iron-snake's shed skin in the rift wall (864) | hidden item | was 4, Static Tunnels |
| 17 | Blazikenite | Mega Blaziken (Fire/Fighting) | Thornwatch, the war-brazier on the gate tower (870) | hidden item |  |
| 17 | Lucarionite | Mega Lucario (Fighting/Steel) | The Last Rung, Ironreach: the Memory Kata (Gutter Book rank 2) (260) | quest `NA_MEMORY_KATA` |  |
| 18 | Audinite | Mega Audino (Normal/Fairy) | Corvin Mott's Infirmary, Mirefen: Wenlow (post-game) (223) | quest `NA_BEDSIDE_MANNER` | was 8 |
| 18 | Latiasite | Mega Latias (Dragon/Psychic) | Shardfall Isles, the eon nest (post-game) (905) | item |  |
| 18 | Latiosite | Mega Latios (Dragon/Psychic) | Shardfall Isles, the eon nest (post-game) (905) | item |  |

**Not placed:** Mewtwonite X/Y and Diancite. Their species aren't in Velmora (POKEMON_AVAILABILITY §4). If they're
added, put the stones in the post-game Concordance Spire shop.

**By method:** 25 found in the world (15 hidden, 7 visible, 3 puzzle rewards), 12 quests (4 of them Trial-rank
commissions), 3 bosses, 2 Trial rank rewards, 2 story gifts (plus the ring). **12 before the ring, 32 after it.**

### 5.2 The gates (checked by `run_mega.rb`)
- **R4 with the Ring:** a stone first obtainable with *b* badges is usable from *u* = max(*b*, 13). Its Mega's types
  must not answer Warden *u*+1 or *u*+2. Answers are `warden_gates.json` where the trainer designer has set them,
  otherwise the type chart: super-effective types plus types immune to the Warden's type. At 13 that rules out Ghost,
  Dark and Normal (Ysolde) and Fire, Fighting and Ground (Magnus); at 14 Fire, Fighting, Ground, Bug, Fairy; at 15
  Fighting, Bug, Fairy, Poison, Steel; at 16 Poison, Steel, Ice, Dragon, Fairy; at 17 Ice, Dragon, Fairy.
- **Before the ring:** 12 stones "hum and wait" (`TEASER_TEXT`), every one safe at 13. **S-tier stones:** none before
  10 (Alakazite, 12, is the earliest).
- **Rank rewards** aren't badge-gated in the Trials plugin, so only two stones are rank rewards, both reachable before
  the ring and safe at 13: Manectite (Prize Exchange rank 3) and Glalitite (Tally rank 3, was Sharpedonite). Later
  "rank rewards" are rank-gated **commissions** with a badge unlock: Mawilite, Tyranitarite, Salamencite, Lucarionite.
- **Map events** carry the gate as their visibility condition: `badges >= N && !has_item(:STONE)`, then self switch A.

### 5.3 What Rev 21 moved (the stones placed for a ring at 7 that fail R4 at 13)
| Stone | Rev 20 | Rev 21 | Why |
|---|---|---|---|
| Absolite | 2, Frostwick Pass | **14**, the Slag Mesa (801), hidden | Dark answers Ysolde |
| Sharpedonite | 2, Tally rank 3 | **15**, Underveil Sump Docks (424), hidden | Dark answers Ysolde; at 14 Water/Dark is fine but the Sump Docks are a 15-badge place |
| Steelixite | 4, Static Tunnels Depths | **17**, Wyrmscar Rift (864), hidden | Steel/Ground answers Magnus (Ground), Nyx and Celestine (Steel) |
| Sablenite | 8, Grudgestone Quarry | **14**, Barrow of the Wardens (804), hidden | Dark/Ghost answers Ysolde |
| Swampertite | 8, the Rootdeep | **15**, the Drownings (821), hidden | Ground answers Magnus |
| Audinite | 8, `NA_BEDSIDE_MANNER` | **18** (post-game), same quest | Normal/Fairy answers Ysolde, then Nyx and Sigrun (Fairy) |
| Banettite | 9, `EL_DOLL_WHO_WAITED` | **14**, same quest | Ghost answers Ysolde |
| Charizardite Y | 10, Cloudstair Summit | **15**, the Brink (832), hidden | Fire answers Magnus |
| Pidgeotite | 10, `ZE_RETURN_TO_SENDER` | **14**, same quest | Normal is immune to Ysolde's Ghosts |
| Cameruptite | 10, `AS_FORGE_REMEMBERS` | **15**, same quest, after the Ring-Day | Fire/Ground answers Magnus |
| Charizardite X | 11, `AS_OLD_CINDER` (Lv 58) | **15**, same boss at Lv 72 | Fire answers Magnus; Dragon answers Sigrun from 16 |
| Glalitite | 11, Frostfang Pass 2F | **2**, Tally rank 3 (takes Sharpedonite's place) | safe at 13; Ice for the ice kingdom's Trial |

The early map events for the moved stones (577, 605, 680, 685, 705, 726) are gone from `TRIAL_EVENTS.yaml`; the new
ones are there. Quests moved by badge keep their dialogue (the Postmaster's "And a ring, I see" now fits; Old Cinder's
rider died "on the Rimed Sands", since the Glass Dunes are the Ch19 battle).

---------------------------------------------------------------------------------------------------
## 6. Who Mega Evolves, and from when (SPINE Rev 21)

**The rule.** From an ace of about **Lv 50** (`MEGA_FROM` / `MEGA_FULL_LEVEL` = 50: Gym 10, cap 51, on) **every important
story fight whose fighter has a ring in the story (§1.2) has exactly one Mega**, on Standard, Hard **and** Casual: the
Wardens, Valen, Meridian and Juno, all before the player has a ring. Story and theme win over the rule: §6.3 lists who
stays Mega-less and why. **Below Lv 50 a fight may use a Mega only if its design
calls for one, and only a weak one (§6.1), on Standard and Hard**; nobody else does. No theme exceptions: where a
Warden's signature Mega would fight the field (Bastian's Sand Stream Tyranitar on Crystal Cavern), a different Mega
goes in. One Mega per side: in tag battles only one of the pair holds a stone, and the player's partners hold none (the
player's side keeps its one Mega for the player). Nobody holds a Mega Stone and a Z-crystal; the Eevee Octave keeps Z.
`gen.py` applies it (`P(..., mega="STONE")`, the trainer's cap against `MEGA_FROM`, `mega_low=True` for a designed weak
Mega) and `run_mega.rb` checks `pbs/trainers.txt` against it.

### 6.1 Weak Megas (allowed below Lv 50 when the design calls for one)
`PrismfallMega::WEAK_STONES` / `gen.py WEAK_MEGA`, roughly the lower competitive tiers: **Camerupt, Glalie, Abomasnow,
Banette, Audino, Steelix, Pidgeot, Beedrill, Sableye, Ampharos, Manectric, Houndoom, Absol** and, at a stretch,
**Sharpedo**. Not weak: Lucario, Metagross, Gengar, Salamence, Kangaskhan, Mawile, Medicham, the Charizards, Gardevoir,
Gallade, Alakazam, Lopunny, Garchomp, Tyranitar, Scizor and the rest. Brann's Mega Camerupt is one of these and stays
exactly as designed, per the user (his set, the Volcanic prime and its eruption boost).

### 6.2 The trainer Mega table (`pbs/trainers.txt`)
| Fight (field, cap) | Mega | Modes | Notes |
|---|---|---|---|
| **Brann**, Gym 7 (Volcanic, 39) | **Camerupt** (weak) | Std, Hard | **kept as designed, per the user**: his committed set (Lava Plume, Earth Power, Rock Slide, Amnesia; Hard Eruption) with the Cameruptite in place of the Elemental Seed; its Mega primes the Volcanic eruption as §3.3 says. |
| Kaito, Gym 8 (43) | none | — | Mega Lucario isn't weak, so it waits for his Festival draw. Hard's Lucario holds a Life Orb. |
| Juno J3, Gym 9 (47) | none | — | the ring won't answer her yet. |
| **Anja**, Gym 10 (Frozen Lake, 51) | **Glalie** (replaces Beartic) | all | Refrigerate Double-Edge; seals the lake's cracks once. Cloyster is the Casual cut. |
| **Marchetti**, Ch12 Skyreach (Stormfront, 55) | **Manectric** | all | the guard dog; Intimidate on Mega. Mabosstiff is the Casual cut. |
| Kestrel K5 (55), K6 (67), K7 (80) | none | — | no ring of his own yet (§1.2). From K7 Mismagius takes Krookodile's place, so his Scizor stays for K8. |
| **Odessa**, Gym 11 (Stormfront, double, 55) | **Pidgeot "Post"** (replaces Swanna) | all | No Guard Hurricane; Oricorio is the Casual cut. |
| **Kroll**, Ch13 Lucent tribunal (Mindscape, 59) | **Sharpedo** (replaces Skuntank) | all | Special Accounts' shark. Toxicroak is the Casual cut. |
| **Ilsa**, Gym 12 (Mindscape, 59) | **Slowbro** (replaces Musharna) | all | a Trick Room Mega (Shell Armor); Calm Mind still soothes a Nightmare. Gothitelle is the Casual cut. |
| **Bastian**, Gym 13 (Crystal Cavern, 63) | **Aerodactyl "Amber"** (replaces Lycanroc) | all | the miner's fossil (Velmora has it from 10 badges); Tough Claws, no sand, so his crystals stay lit. |
| **Marchetti**, Ch14 Darkglass raid (Dark Crystal, 63) | **Houndoom** | all | the first fight where both sides can Mega. Arcanine is the Casual cut. |
| **Ysolde**, Gym 14 (Hollow Cathedral, 67) | Std/Casual **Sableye**; Hard **Gengar** | all | Shadow Tag + Perish Song is Hard-only (BALANCE §1). |
| **Magnus**, Gym 15 (Factory, 71) | **Metagross "Engine"** | all | the foundry hammers its plating home (+1 Def). |
| **Marchetti + Quent**, Ch16 tag (Factory, 71) | **Houndoom** (Marchetti, replaces Arcanine) | all | the pair's one Mega; Quent has none. |
| **Kroll**, Ch17 Sun Court (Cave, 75) / **Quent** (alt., 75) | **Sharpedo** / **Metagross** | all | |
| **Nyx**, Gym 16 (New Moon, double, 75) | **Absol "Omen"** (replaces Malamar) | all | Magic Bounce guards the Illusion games; Honchkrow is the Casual cut. |
| **Celestine**, Gym 17 (Fairy Tale, double, 80) | none: **a Z-move instead** (Rev 23): Mimikyu @ Mimikium Z | all | Gloaming's dusk-chapels tuned it (Z_MOVES.md §4); Mimikyu is back in the slot Mega Mawile took. Azumarill is the Casual cut. |
| **Sigrun**, Gym 18 (Dragon's Den, 85) | **Salamence "Dreamwing"** | all | |
| **Kestrel K8**, Festival SF (Prism Arena, 94) | **Scizor**, only with Morwen's Ring | all | `MORWEN_RING`: ring and Scizorite at battle start when `:ch18_kestrel_ring` = *give_now*; otherwise none. |
| Kestrel K9 (fallen, 94) | none | — | he never got the ring. Genesect "Gauntlet" replaces Staraptor (Krookodile is gone from K7 on). |
| **Juno J4**, Festival R16 (Prism Arena, 90) | **Gardevoir "Veil"** (replaces Comfey) | all | not her starter: Core swaps it to the player's generation, and most starter lines have no Mega. J7 (Ch21 partner): none. |
| Festival R16 / QF / Final draws | Marisol **Gyarados**, Anja **Glalie**, Sigrun **Salamence**, Odessa **Pidgeot**, Celestine (Z: Mimikyu), Kaito **Lucario**, Ysolde **Sableye**/Gengar, Brann **Camerupt** (v96), Dorian **Lopunny** (the Pageant Bout's one Mega; Rook none) | all | |
| **Valen** (Final 96; Ruin's Last Tuning) | **Gallade** | all | |
| **Voss** (Festival hijack, 100) | **Ampharos "Lumen"** (replaces Klinklang) | all | Meridian's lamp, "light for everyone"; Dragon resists the first four Plates. |
| **Quent** (hijack 100, Ch21 tag 97) | **Metagross** | all | |
| Ch21 tag foes (97) | Kroll **Sharpedo**, Marchetti **Manectric** (replaces Arcanine), Directorate Captain **Scizor** | all | one fires per side. |
| Ruin Gyms 15–18 (v1) | as their Wardens (Celestine's is her Z) | all | |
| Cameos | Garret's v1 (ace 46) has **no** Mega now (Lucario isn't weak); v2 (100) Megas in every mode; the others unchanged (Hard-only, all past Lv 50) | | optional sidequests, not story fights |
| The Eevee Octave | none (Z-moves) | | |
| Wild bosses (Old Cinder 72, Old Pincer 62, the Matriarch 78) | none (wild) | | |

**Counts:** 36 Standard / 36 Hard / 36 Casual trainer entries at ace 50+ hold one Mega each and 3 per mode use
Celestine's Z-move instead (run_mega.rb), plus Kestrel's K8 when he has Morwen's Ring; one below Lv 50 (Brann),
Standard and Hard only.

### 6.3 Mega-less for story reasons (no ring by that point)
| Fighter | Why |
|---|---|
| Kestrel K1–K7 (and K9) | no ring of his own; Morwen's Ring reaches him only through the PC, from Ch18 (K8). |
| The Mourner (Ch9, 43) and Rowan at the Festival (R16, 90) | his Warden's ring went into the sealed testament before he first wore the mask, and to Juno with the seat. |
| Archseer Imre Dask (Ruin QF, 92) | the Veiled Synod's Archseer is no Warden and has no Hearthguild ring. Rev 20's Hard-only Mega Sableye is gone too. |
| Morwen's Echo (Exhibition, 90) | her ring is Morwen's Ring, in the PC's or Kestrel's hands by then; an echo has none. |
| Theodric, the Gilded Reflection (Ruin hijack, 100) | a reflection of the Gilded King; the rings came three centuries after him. |
| The war officers (Ch19, 84): Ashkaar's and Isenmar's captains | soldiers of the two kingdoms, not Accord officers; the story gives them no rings. |
| Juno J7, the war partners (Sigrun, Marisol) | on the player's side: the side's one Mega is the player's. |
| Quent at the Ch16 tag, Rook at the Pageant Bout | they share a side with Marchetti / Dorian, whose Mega is the pair's one. |

**EBDX battle speech** (optional, trainer designer): a `megaOpp` line per Mega fight, e.g. Brann "Some things you forge
to last!", Bastian "Rock's patient. So's this.", Kestrel with Morwen's Ring "Mum. Just this once. Answer me."

---------------------------------------------------------------------------------------------------
## 7. Implementation

| File | What |
|---|---|
| `plugins/Prismfall Mega/001_Mega_Config.rb` | limits, `RING_BADGES` (13), `MEGA_FULL_LEVEL`, `WEAK_STONES`, `MORWEN_RING`, `STONES` (44 rows), `UNPLACED`, `FIELD_RULES`, `FIELD_NOTES` |
| `002_Mega_Battle.rb` | one Mega per side, Z-crystal block, the event and log; the per-side owner key for Z-Power |
| `003_Mega_Fields.rb` | gained-ability entry rules, the 8 showpieces, Field Notes lines (unchanged in Rev 21) |
| `004_Mega_Story.rb` | `pf_mega_stone(:ITEM[, "line"])` (teaser line before the ring), conditions `mega_ring` / `mega_stones`, Kestrel's Morwen's Ring swap (`:on_trainer_load`), Debug menu "Prismfall Mega..." |
| `plugins/Prismfall Trials/114_Quests_Megas.rb` | `OS_RING_DAY` (Bastian), Brann's spare (15, the Light Stone line), Juno's Venusaurite and 14 stone quests |
| `132_EventMons_Megas.rb`, `152_Talk_Megas.rb` | the three boss guardians (Old Cinder now Lv 72 at 15); talk rows (`BASTIAN_LAMPROOM` new; `BRANN_HEARTHGUILD` keeps only the spare) |
| `001_Trials_Config.rb` | rank 3 rewards: Manectite (Zenith), Glalitite (Isenmar) |
| `design/TRIAL_EVENTS.yaml` | "Mega Evolution" maps: 25 stone events + the quest NPCs and objects (Rev 21: 6 blocks gone, 7 new) |
| `tools/trainer_gen/gen.py`, `cameos.py` → `pbs/trainers.txt` | `mega=` / `mega_low=` / `mega_set` / `mega_modes`, `MEGA_FROM`, `WEAK_MEGA`; every assignment in §6.2 |
| `tools/harness/run_mega.rb`, `run_winrates.rb` (G7M, G10M, K5M, G11M cells, `PRISM_FOE_NOMEGA`), `playtest/run_mega.sh`, `004_MegaBot.rb`, `make_mega_gif.py` | tests |

Requests to other workstreams are in `mapgen/REQUESTS.md` ("From the Mega Evolution workstream", Revisions 20 and 21).

---------------------------------------------------------------------------------------------------
## 8. Tests

**Headless** (`PRISM_RUN_DIR=<run copy> PRISM_COMPILE=1 ruby tools/harness/run_mega.rb`): **69/69 passed** (Rev 23 adds the
one-ring, crystal-distribution, species Z-move and crystal-teaser checks: `design/Z_MOVES.md` §5)
(`docs/mega_test/REPORT.md`, transcript alongside). The run covers:
- data: 47 stones + Rayquaza; every stone placed or unplaced; the Ring at 13 (Cragholm, Bastian); R4 at the new Ring
  point; 12 stones before the ring; S-tier none before 10; quest, rank and event sources; every Mega talk key placed.
- a Mega in a field battle: the player's Camerupt on Volcanic primes and erupts, and the Mega comes before moves.
- the AI: Anja's Standard gym battle through `Prismfall.gym_battle(10)`: Mega Glalie the turn it comes out, on the
  Frozen Lake; Brann's Standard Camerupt (kept as designed) Megas on Volcanic and primes the eruption.
- `pbs/trainers.txt` against the Rev 21 rules: 39 Standard / 39 Hard / 39 Casual entries at ace 50+ hold one stone and
  the ring; the story's ring-less fighters (§6.3) hold none; below Lv 50 only Brann (weak, Std + Hard); no trainer
  holds two stones or a stone and a Z-crystal.
- Kestrel's K8: no ring and no stone; with `:ch18_kestrel_ring` = *give_now*, the ring and the Scizorite at battle start.
- Mega + Z in one battle; one Mega and one Z per side; no ring means no Mega; wild Pokémon never Mega; a Z-crystal
  blocks Rayquaza; all 8 showpieces; No Guard and Magic Bounce entry rules on Mega Evolution; the Field Notes lines.
- the quests: the teaser at 3 badges; the Ring-Day locked at 12 badges and open at 13 in Bastian's lamp-room (the ring
  sings, Pip hears it, the earlier stones stop waiting, no "reset" or "Legend Plate"); Brann's spare at 15 badges with
  the Light Stone line (`:ch8_lightstone` = *dominar*); the Old Pincer boss (with the player's Mega Charizard); the
  brazier writ.

`tools/harness/run_trials.rb` still passes **142/142**. `tools/validate_trainers.py`: 0 errors (the same 35 Hard-only
warnings as before). `tools/trainer_gen/field_fit.py --all`: 92 important Standard teams, 0 problems.

**Win rates** (`tools/harness/run_winrates.rb`, `PRISM_PREPARED=1`, Standard, 60 fights a cell = 20 per starter): a
**prepared** team at the cap with no Mega (the player has no ring before 13): the starter plus five of six listed
answers with mid-game TMs, IV 20–31, EV 85 each, piloted by the v21 AI. `PRISM_FOE_NOMEGA=1` takes the foe's ring away:
the same fight without its Mega.

| Fight | Foe's Mega | With the Mega | Without it |
|---|---|---|---|
| Gym 7 Brann (Volcanic, 39), as designed | Camerupt (weak) | **88%** (53/60) | **93%** (56/60) |
| Gym 10 Anja (Frozen Lake, 51) | Glalie | **35%** (21/60) | **38%** (23/60) |
| Ch12 Marchetti (Stormfront, 55) | Manectric | **82%** (49/60) | **88%** (53/60) |
| Gym 11 Odessa (Stormfront, double, 55) | Pidgeot | **85%** (51/60) | **95%** (57/60) |

Reading: the Megas cost a prepared team 0–10 points; Brann, Marchetti and Odessa are hard-but-fair wins. **Anja is hard
with or without her Mega** (Walrein's Surf and Blizzard on the Frozen Lake did most of the damage in the logged runs),
so that is her base design, not the Mega (§9). Kestrel's K5 is no Mega fight any more (no ring). For the AI pilot's
limits see BALANCE §9: it plays worse than a person.

**Real engine** (Rev 20; `tools/harness/playtest/run_mega.sh assemble | install | mega | gif`; a lean copy: Audio and the
big Graphics folders are hard links, because mkxp-z's PhysFS won't follow symlinks). The run is the player's own Fight
menu against a test "Brann" (Torkoal, then Camerupt with a ring) on Volcanic:
- Fight, then Action **lights the EBDX Mega button** (`005_mg_02_mega_button_on.png`); Use on Flamethrower plays the
  Mega animation, and Mega Charizard X has Tough Claws.
- The Volcanic showpiece fired ("Charizard's Mega Evolution stirred the magma... the volcano is about to erupt!").
- Then the AI's Camerupt Mega Evolved when it came out (`015_mg_after_MegaEvolution2_Camerupt.png`). One Mega per side.
- **GIF:** `docs/battle_captures/mega/mega_evolution_ebdx.gif` (179 frames, 2.4× slow, 15.7 s), with key shots and the
  bot log beside it. Rev 21 changed no battle code, so the capture still stands.

---------------------------------------------------------------------------------------------------
## 9. Proposals and open items

1. **A shared Mega/Z button on EBDX's Fight menu** (for the EBDX Bridge owner and the Z owner). EBDX's Mega button
   already toggles with Action and previews the Mega form's move types. The proposal is to make that one slot a
   **"power" button** that shows Mega or Z depending on what the battler can do (a Mega-stone holder can't hold a
   Z-crystal, so they never clash). Toggling Z would preview the Z-move names and power on the move buttons, and the
   Z Yes/No box after the move pick would go away. Hook point: `FightWindowEBDX#megaButton` and the `-2` toggle in
   `Battle#pbFightMenu`'s block, with `PrismfallZ.after_register` reading it.
2. **Z-Power config:** fold the per-side owner key into Prismfall Z-Power itself (one line in `PrismfallZ.owner_key`).
3. **Bosses:** an optional `:mega => true` break effect for trainer bosses (Rejuvenation's Latios in its second bar).
4. **Phase 2:** Legends Z-A Megas once the harness runs Gen 9 Pack 3.3.8 (§3.5).
5. **FIELDS.md:** include `PrismfallMega::FIELD_NOTES` in the generated sections.
6. **Anja (trainer designer):** a prepared Standard team wins about 38% with or without her Mega; if Gym 10 should be
   easier than that, the lever is Walrein (Surf + Blizzard on the Frozen Lake), not the Glalie.
7. **Story editor:** Juno's Gardevoir "Veil" needs an introduction before the Festival; Meridian's Lattice-glass
   keystones need one line before Marchetti's Ch12 fight (`mapgen/REQUESTS.md`).
