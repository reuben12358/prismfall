# MEGA_EVOLUTION — Mega Evolution in Prismfall (SPINE Revision 20)

> User: "speaking of adding z moves, u also gotta add mega evolutions."
> SPINE Rev 20: Megas are earned the Reborn/Rejuvenation way (the ring from a story beat, stones from quests, puzzles and
> exploration after badges); Wardens and bosses Mega Evolve where it fits their theme and field; Megas, Z-moves and fields
> work together; one Mega and one Z-move per side per battle, under EBDX.

Status: **working** in the headless harness (59/59 checks) and in the real engine (the player's EBDX Mega button, the
Mega animation, the AI's Mega, on a Prismfall field). Code: `plugins/Prismfall Mega/` (4 files). Quests:
`plugins/Prismfall Trials/114_Quests_Megas.rb`, `132_EventMons_Megas.rb`, `152_Talk_Megas.rb`. Map events:
`design/TRIAL_EVENTS.yaml` ("Mega Evolution" maps). Tests: `tools/harness/run_mega.rb` (report `docs/mega_test/REPORT.md`),
`tools/harness/playtest/run_mega.sh` (GIF `docs/battle_captures/mega/mega_evolution_ebdx.gif`).

---------------------------------------------------------------------------------------------------
## 1. Lore: heartstones and Warden's rings

Prismfall's Megas come out of the Plates and Imprints (story/01_WORLD_LORE.md §3, §5), so the story team can use them:

- **A Mega Stone is a heartstone.** Where an Imprint soaks into one line of Pokémon for long enough, it pearls inside
  them, the way Imprints condense into seeds at their borders. Velmorans say *heartstone*; the Accord says *Mega Stone*.
  Holding one, a Pokémon can carry its whole Imprint for one battle. That's why the stones turn up in Imprint-heavy
  places: the Cinderhorn slag, the Bride Tree's roots, a sap tree, a lighthouse lens.
- **A Mega Ring is a Warden's ring.** It is a gold band holding a chip of stone with no colour at all. The chip is
  **grind**: dust from the Crown's own stone (in truth the Legend Plate shard, which only the Secret Articles say),
  kept by Cindervault's **Hearthguild**. It has no colour of its own, so it takes any colour and opens any heartstone.
  The guild has cut one ring for every Warden's seat since the Concordance. That's why Wardens Mega Evolve and
  ordinary trainers don't.
  - **What Brann may say in Ch8:** "grind off the Crown's own stone", nothing more. He never names the Legend Plate and
    never says "reset". 09_MYSTERIES #5 (the One in Keeping is the Legend Plate) and #6 (the Crown is cracked) are
    revealed in Ch15–17; his chestnut slip the night before is the only Ch8 clue to #4/#6.
- **One heart at a time.** Two rings on the same side "ring against each other". That is the in-world reason for the
  rule of one Mega per side, partner battles included.
- **Rings people carry:** every seated Warden has one. Valen wears the Sovereign's. Meridian has no ring and wants
  none: Voss wants the whole Crown, not a fleck of it.
  - **Morwen's ring** is the Key Item **Morwen's Ring** (07_ACT_IV Ch15). She paid Edda with it for the AF 290 night
    ferry, and Edda gives it to the PC at Morwen's grave. Kestrel wears it only once the PC gives it to him:
    `:ch18_kestrel_ring` *give now* (after K7), or at the SF if he's Redeemed. **It answers him the first time he
    wears it into battle**, so Kestrel has **no Mega before then** (no ring of his own; through Acts III–IV Meridian's
    Resonance Gauntlet is his power-up instead). Giving the ring early makes him safe from falling and also makes K8
    harder: he Megas at the SF.
  - **Rowan's ring.** Rowan takes it off before he first puts on the mask and leaves it with his sealed Warden's
    testament (Interlude II, 05_ACT_II), so the Mourner never Megas. The testament names Juno heir (06_ACT_III Ch10),
    and the ring comes to her with it. At first it won't answer her (the Heartgarden scene); at J4 it does.
- **Foreshadowing (09_MYSTERIES #1):** the PC's ring is **the odd one out**. Brann cut it "ten years back" from the
  grind of the AF 290 reset (he doesn't say that part), the same break the splinter flew from. It has "sulked on every
  hand" he's tried it on, and it **sings** for the PC ("They don't sing. Thirty years at this anvil..."). Pre-Ring stones
  hum when the PC picks them up. Brann's drunken line the night before ("After the accident. Ten years back. It was
  smaller than it should've been") lands the next morning, when a ring he cut ten years back sings in the PC's hand.

Z-crystals stay what EEVEE_OCTAVE.md made them: slivers of Glassfall glass, each tuned by the Choir to one Imprint. The
Z-Power Ring stays Vesper's Octave reward. Rings and crystals are separate things in the story too.

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
- **M1:** the ring is a **story beat** around the middle of the game, and it is ours alone (not combined with Z).
- **M2:** a few stones turn up **before** the ring and "hum and wait", as in both games. They are modest ones.
- **M3:** after the ring there are **2–5 stones per badge**, spread across quests, Trial ranks, puzzles, bosses and hidden spots.
- **M4:** **S-tier stones come late** (none before 10 badges; most at 13–17); the legendary ones come post-game.
- **M5:** **no stone that answers the next Warden** (rule R4 with the ring, §5.2).
- **M6:** the first enemy Megas are a showpiece **by a Warden around the time of the ring** (Rejuvenation's Mega Banette).
  After that, Megas are the norm for big fights. No trainer Megas before the Ring-Day.

Prismfall gives the ring **earlier** than both games (7 of 18 badges, SPINE's "mid-Act II"). M3–M5 make up for that:
the stones usable at 7–9 badges are B/A-tier and none of them answers Kaito or Juno.

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
| Volcanic | a **Fire-type** Mega primes the volcano: it erupts at the end of the round (Fire types ride it +1, lava 1/8 on grounded non-Fire foes) | Brann's Mega Camerupt is a living volcano; quenching (Surf ×2 → Cinderglass) is the honest answer |
| Colosseum | the crowd counts it like a knockout toward the Frenzy (not once the Frenzy is on) | Kaito's Mega Lucario plays to the crowd |
| Frozen Lake | an **Ice-type** Mega seals every crack (the crack meter resets) | Anja's Hard Mega Glalie undoes one Fire plan |
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
## 4. The Mega Ring beat: "The Ring-Day" (Chapter 8, Cindervault)

- **When:** the morning after the Caldera Crisis (05_ACT_II Ch8), with **7 badges**, after Brann's gym (where Mega
  Camerupt is the first Warden Mega the player meets) and the Light Stone choice. It comes before the Dominar's
  herald (the chapter's cliffhanger). That's mid-Act II, right before Ch9's Ironreach, where Kaito's Mega Lucario
  is the first Warden fight in which both sides can Mega.
- **Where:** the Hearthguild Hall (map 244). Brann is at the guild anvil and Larch sits by the door.
- **Script:** `story/22_SCRIPT_CH8.md` (authoritative lines; the plugin matches it). Storyboard of the ring's note:
  `story/13_CUTSCENES.md` RD-1.
- **Scene** (`AS_RING_DAY`, hidden; `pf_trial_talk(:BRANN_HEARTHGUILD)`). The opening depends on the caldera choice:
  vent ("Cold for a season... A ring wants a candle, not a caldera"), dampers ("You kept 'em lit"), shutdown ("The
  Dominar hasn't stopped talking about it"). Then:
  1. Brann waves off last night's chestnuts ("Forget the fool. Forget the chestnuts too. They were burnt").
  2. He gives the ring: what a Warden's ring is, and that this one is the odd one out ("I cut it ten years back, and
     it's sulked on every hand I've tried it on"); what the colourless chip is (grind off the Crown's stone, which takes
     any colour); what a heartstone is; and the rule, one Mega to a side ("Remember it in a double").
  3. **The ring sings.** "Somewhere under your ribs, something answers it." Brann goes quiet ("They don't sing. Thirty
     years at this anvil, and not one of them has ever sung"). Larch lowers her book.
  4. He covers it up, badly ("It's the forge-hum. That's a lie, and lying's a crime in Ashkaar, so you never heard
     it"), and adds the **Aggronite**.
  5. Any stones already in the Bag "are warm now, and quiet, as if they had stopped waiting." He signs off: Aron burrow
     under the Brinecut cliffs, and "Go and show Kaito what a ferry child does with a Warden's ring."
- **Gives:** `MEGARING` and `AGGRONITE`. No Trial gong: the scene closes quietly.
- **Follow-up beats:** Ch9 Kaito's Mega Lucario. J3/the Heartgarden: Juno's ring won't answer her yet
  (`EL_BRIDE_TREE_HEART`, Venusaurite). Act III: Brann's spare heartstone (`AS_FORGE_REMEMBERS`, "Your ring still
  singing? ...No. Don't tell me"). Ch18/SF: Morwen's Ring answers Kestrel the first time he wears it. J4: Juno's ring
  answers her.
- **Open for the Trials owner:** one reactive line if `choice(:ch8_lightstone) == :dominar` (Brann is hurt; see the
  script). It needs a new `:if` entry, so it isn't in the plugin yet (`mapgen/REQUESTS.md`, story editor 2026-11-20).
- For the story editor: the scene is written in the Trials data so it plays and tests now. If you'd rather stage it as a
  story event, keep the lines and call `pbReceiveItem(:MEGARING)` and `pbReceiveItem(:AGGRONITE)`.

---------------------------------------------------------------------------------------------------
## 5. Stone distribution

### 5.1 The 44 placed stones
| Badges | Stone | Mega (types) | Where (map) | How |
|---|---|---|---|---|
| 2 | Absolite | Mega Absol (Dark) | Frostwick Pass, the avalanche gully (Rock Smash) (577) | hidden item |
| 2 | Manectite | Mega Manectric (Electric) | The Prize Exchange, rank 3 (Fellow) (194) | Trial rank reward `ZENITH` |
| 2 | Sharpedonite | Mega Sharpedo (Water/Dark) | The Tally, rank 3 (Harpooner) (306) | Trial rank reward `ISENMAR` |
| 3 | Ampharosite | Mega Ampharos (Electric/Dragon) | Ferrow Lighthouse lamp room: Hesper's lamp lens (106) | quest `EL_LAMP_LENS` |
| 4 | Steelixite | Mega Steelix (Steel/Ground) | Static Tunnels Depths, the magnetite seam (Flash) (605) | hidden item |
| **7** | **Aggronite** (+ **Mega Ring**) | Mega Aggron (Steel) | Hearthguild Hall, Cindervault: Brann (244) | story gift `AS_RING_DAY` |
| 8 | Sablenite | Mega Sableye (Dark/Ghost) | Grudgestone Quarry B1F, the gem seam the Sableye feed on (685) | hidden item |
| 8 | Sceptilite | Mega Sceptile (Grass/Dragon) | The Royal Chase, the old hunting lodge's mantel (682) | item |
| 8 | Swampertite | Mega Swampert (Water/Ground) | The Rootdeep, the underground river (Surf) (680) | hidden item |
| 8 | Blastoisinite | Mega Blastoise (Water) | Prism Falls, behind the falls (Surf) (681) | hidden item |
| 8 | Audinite | Mega Audino (Normal/Fairy) | Corvin Mott's Infirmary, Mirefen: Wenlow (Corvin after Ch16) (223) | quest `NA_BEDSIDE_MANNER` |
| 9 | Venusaurite | Mega Venusaur (Grass/Poison) | The Heartgarden, Verdance: Juno, after J3 (294) | story gift `EL_BRIDE_TREE_HEART` |
| 9 | Beedrillite | Mega Beedrill (Bug/Poison) | Gossamer Heartwood, inside the old hive (703) | hidden item |
| 9 | Banettite | Mega Banette (Ghost) | Thistledown Manor attic: the doll who waited (547) | quest `EL_DOLL_WHO_WAITED` |
| 10 | Charizardite Y | Mega Charizard Y (Fire/Flying) | Cloudstair Summit, the wind-scoured ledge (726) | hidden item |
| 10 | Pidgeotite | Mega Pidgeot (Normal/Flying) | Gale Post Hall, Skyreach: the dead-letter bag (325) | quest `ZE_RETURN_TO_SENDER` |
| 10 | Altarianite | Mega Altaria (Dragon/Fairy) | The Tetherline, a cloud-nest on a tether pylon (732) | item |
| 10 | Slowbronite | Mega Slowbro (Water/Psychic) | Ebbmouth Sea Grotto, the tide-pool shelf (723) | hidden item |
| 10 | Cameruptite | Mega Camerupt (Fire/Ground) | Hearthguild Hall, Cindervault: Brann's spare (244) | quest `AS_FORGE_REMEMBERS` |
| 11 | Charizardite X | Mega Charizard X (Fire/Dragon) | Pyre Keep Dragon Roosts: Old Cinder, a retired Legion war-Charizard (248) | **boss** `AS_OLD_CINDER` |
| 11 | Glalitite | Mega Glalie (Ice) | Frostfang Pass 2F, behind the thawed ice wall (705) | item |
| 12 | Alakazite | Mega Alakazam (Psychic) | Lucent Athenaeum, the Sealed Stacks: the Unread Shelf (345) | **puzzle** |
| 12 | Aerodactylite | Mega Aerodactyl (Rock/Flying) | Sahar's Dig Lab: bring her a revived Aerodactyl (209) | quest `OS_AMBER_AGAIN` |
| 12 | Pinsirite | Mega Pinsir (Bug/Flying) | Gossamer Heartwood: the Old Pincer (703) | **boss** `EL_OLD_PINCER` |
| 13 | Gardevoirite | Mega Gardevoir (Psychic/Fairy) | The Looking-Glass Wood, the heart of the mirror maze (752) | **puzzle** |
| 13 | Mawilite | Mega Mawile (Steel/Fairy) | The Speculum, Lucent: the smile behind the glass (346) | **Trial rank 2** quest `AN_SMILE_BEHIND_GLASS` |
| 13 | Scizorite | Mega Scizor (Bug/Steel) | Vane Hall, Gravenmoor: Morwen Vane's trophy case ("MUM'S. DON'T TOUCH. - K.") (383) | item |
| 13 | Abomasite | Mega Abomasnow (Grass/Ice) | The Hoarwood, under the frost-giant pine (701) | hidden item |
| 14 | Metagrossite | Mega Metagross (Steel/Psychic) | Strade Works Foundry Floor, the sorting-line puzzle (403) | **puzzle** |
| 14 | Gengarite | Mega Gengar (Ghost/Poison) | Barrow Sanctum, the altar of the nameless Warden (805) | item |
| 15 | Gyaradosite | Mega Gyarados (Water/Dark) | Aurelia - Drowned Spires, the flooded bell (Dive) (824) | hidden item |
| 15 | Houndoominite | Mega Houndoom (Dark/Fire) | Underveil Moon Market: the Barons' kennel (423) | quest `NA_MOON_MARKET_DOGS` |
| 15 | Tyranitarite | Mega Tyranitar (Rock/Dark) | Cragholm rack: the tyrant's heart in the Vertebrae (360/773) | **Trial rank 2** quest `OS_TYRANT_HEART` |
| 15 | Garchompite | Mega Garchomp (Dragon/Ground) | The Dry Tide, a sand-sunk caravan (810) | hidden item |
| 15 | Salamencite | Mega Salamence (Dragon/Flying) | The Crucible, Cindervault: the brazier writ (say true) (240) | **Trial rank 2** quest `AS_BRAZIER_WRIT` |
| 16 | Galladite | Mega Gallade (Psychic/Fighting) | The Gloamwood Verge, the knight's barrow (841) | item |
| 16 | Medichamite | Mega Medicham (Fighting/Psychic) | The Iron Pit, the meditation shelf (Rock Climb) (263) | hidden item |
| 16 | Heracronite | Mega Heracross (Bug/Fighting) | Gossamer Wood, the old sap tree (524) | hidden item |
| 16 | Lopunnite | Mega Lopunny (Normal/Fighting) | Pell Playhouse, the Grand Stage: Dorian's encore (154) | quest `EL_ENCORE` |
| 16 | Kangaskhanite | Mega Kangaskhan (Normal) | Frostflat Causeway: the Causeway Matriarch (560) | **boss** `IS_CAUSEWAY_MATRIARCH` |
| 17 | Blazikenite | Mega Blaziken (Fire/Fighting) | Thornwatch, the war-brazier on the gate tower (870) | hidden item |
| 17 | Lucarionite | Mega Lucario (Fighting/Steel) | The Last Rung, Ironreach: the Memory Kata, Kaito's old unit's stone (260) | **Trial rank 2** quest `NA_MEMORY_KATA` |
| 18 | Latiasite / Latiosite | Mega Latias / Latios (Dragon/Psychic) | Shardfall Isles, the eon nest (post-game) (905) | items |

**Not placed:** Mewtwonite X/Y and Diancite. Their species aren't in Velmora (POKEMON_AVAILABILITY §4). If they're
added, put the stones in the post-game Concordance Spire shop.

**By method:** 25 found in the world (14 hidden, 8 visible, 3 puzzle rewards), 12 quests (4 of them Trial-rank
commissions), 3 bosses, 2 Trial rank rewards and 2 story gifts (plus the ring). 5 come before the ring and 39 after it.

### 5.2 The gates (checked by `run_mega.rb`)
- **R4 with the Ring:** a stone first obtainable with *b* badges is usable from *u* = max(*b*, 7). Its Mega's types must
  not answer Warden *u*+1 or *u*+2. Answers are `warden_gates.json` where the trainer designer has set them, otherwise
  the type chart: super-effective types plus types immune to the Warden's type. This is why Ghost Megas (immune to
  Kaito's Fighting) and Fire, Ice, Poison or Bug Megas (Juno's Grass) aren't usable at 7. It's also why Lucarionite
  waits for 17 (Fighting/Steel answers Anja, Bastian, Magnus and Nyx in turn) and Gardevoirite skips 14–17 (Fairy
  answers Nyx and Sigrun).
- **Teasers** (before the ring): 5 stones, all B/A-tier and all safe at 7. **S-tier stones:** none before 10.
- **Rank rewards** aren't badge-gated in the Trials plugin. So only two stones are rank rewards, at ranks reachable
  before the Ring-Day: Manectite (Prize Exchange rank 3) and Sharpedonite (Tally rank 3). Later "rank rewards" are
  rank-gated **commissions** with a badge unlock (`:rank => 2` + `badges >= N`): Mawilite, Tyranitarite, Salamencite
  and Lucarionite. Raise their `:rank` as the Trials gain quests.
- **Map events** carry the gate as their visibility condition: `badges >= N && !has_item(:STONE)`, then self switch A.

---------------------------------------------------------------------------------------------------
## 6. Who Mega Evolves, and from when

No trainer Mega Evolves before the Ring-Day chapter (7 badges). Brann's Mega Camerupt is the first, the Rejuvenation
way: the Warden shows it, then hands you the means. From Gym 8 on, most big fights have one Mega (at most one per side).
**Casual** never gets Warden Megas below Gym 15 (those Megas sit on *(−C)* slots or are Std/Hard-only); Festival and
post-game teams keep them on all difficulties.

| Trainer (field, cap) | Mega | Difficulty | Why this one |
|---|---|---|---|
| **Brann**, Gym 7 (Volcanic, 39) | **Camerupt "Kiln"** (move it to slot 5, before Anvil; the Elemental Seed goes to Torkoal) | Std, Hard | the living volcano for the forge-Warden. On Volcanic its Mega primes an eruption (+1 Sp. Atk for Fire, lava for grounded foes). The answer is honest: 4× Water, and Surf ×2 quenches the field. Brann's team has no Charizard; Charizard X is Ashkaar's dragon-rider stone, which the player earns from Old Cinder at 11. |
| **Kestrel** K8 (Festival SF, 94) and K9, **only if he wears Morwen's Ring** (`:ch18_kestrel_ring` = *give_now*) | **Scizor** | all | Morwen's Ring is with Edda until Ch15 and reaches Kestrel only through the PC (07 Ch15, 08 Ch18), so he has **no Mega at K4–K7**: Meridian's Gauntlet is his power-up then. The ring answers him the first time he wears it. If it's given at the SF instead (Redeemed, after K8), his first Mega is in the hijack tag battle, where the player's Mega has priority (one per side). Scizor is his duelist and doesn't depend on the player's starter. |
| **Kaito**, Gym 8 (Colosseum, 43) | **Lucario "Memory"** (Lucarionite instead of the Std Scope Lens) | Std, Hard | "It remembers for me." The crowd roars for its Mega (a knockout toward the Frenzy). The first Warden fight where both sides can Mega. |
| **Juno** J3, Gym 9 (Flower Garden, 47) | none | — | Rowan's ring won't answer her yet (the Heartgarden scene). |
| **Juno** J4 (Festival R16, 90), J7 (Ch21 partner) | her **starter**: write the Gen 1 line with its stone (Blastoisinite / Venusaurite / Charizardite X by slot). Core remaps it to the swapped starter's stone, or Life Orb | all | the ring answers at last. As Ch21 partner she Megas only if the player doesn't (one per side). |
| **Anja**, Gym 10 (Frozen Lake, 51) | **Glalie** (replaces Beartic *(−C)*) | **Hard only** | Standard Anja stays the ice-crack fight. On Hard her Mega Glalie seals every crack once, undoing one Fire plan. |
| **Odessa**, Gym 11 (Stormfront, 55, double) | **Pidgeot "Post"** (replaces Swanna *(−C)*) | Std, Hard | the Gale Post's courier bird; No Guard Hurricane in the storm. The player's own Pidgeotite came out of her Post's drawer at 10. |
| **Ilsa**, Gym 12 (Mindscape, 59) | **Alakazam** (replaces Musharna *(−C)*) | Std, Hard | the scholar's Pokémon for the Athenaeum's daughter. Trace on the Mindscape. |
| **Bastian**, Gym 13 (Crystal Cavern, 63) | none | — | Mega Tyranitar's Sand Stream would blot out his own crystal light (→ Dark Crystal). Aerodactyl is Sahar's fossil line; Diancie isn't in Velmora. His ace stays the Sturdy Gigalith. |
| **Ysolde**, Gym 14 (Hollow Cathedral, 67) | Std: **Sableye** (lead); Hard: **Gengar** (as BALANCE already has it: Shadow Tag + Perish Song) | Std, Hard | Standard never uses Shadow Tag, so Standard gets Magic Bounce Sableye. Either Ghost Mega re-haunts a consecrated nave. |
| **Magnus**, Gym 15 (Factory, 71) | **Metagross "Engine"** | all | was Hard-only. The foundry hammers its plating home (+1 Def). |
| **Nyx**, Gym 16 (New Moon, 75, double) | **Absol** (replaces Malamar *(−C)*) | Std, Hard | the omen of disaster for the spymaster. Magic Bounce guards Zoroark's Illusion games. |
| **Celestine**, Gym 17 (Fairy Tale, 80, double) | **Mawile** (replaces Mimikyu *(−C)*) | Std, Hard | the wolf in the storybook: a deceiver with a hidden maw. Huge Power Play Rough with Intimidate support. |
| **Sigrun**, Gym 18 (Dragon's Den, 85) | **Salamence "Dreamwing"** | all | was Hard-only. She arrives on a Salamence in Ch8. |
| **Valen** (Festival Final 96, Last Tuning v1) | **Gallade** | all | was Hard-only. The Sovereign's blade, wearing the Sovereign's ring. |
| **Marisol** v90 (Festival) | **Gyarados "Lucky"** | all | was Hard-only. |
| Festival v92 draws (Kaito, Ysolde, Sigrun, Odessa, Celestine), Brann v96 | their gym Mega | all | — |
| Cameo sidequests | unchanged (Garret's Mega Lucario at 46, Titania's Mawile, Lin's Gardevoir, Alexandra's Latias, Nova's Banette) | — | all after the Ring-Day |
| **Voss**, Quent, the Octave gauntlet | none | — | Meridian has no ring (Silvally NULL is its answer). The Octave is Z-moves' showcase. |
| **The Mourner** (Ch9 boss) | none | — | a mask can't hide a Warden's ring, so Rowan left his with his sealed testament before he ever put the mask on (Interlude II). His bare ring-finger, pale where the band sat for 24 years, is a detail at the unmasking. |
| **Wild bosses** (Old Cinder 58, Old Pincer 62, the Causeway Matriarch 78) | none (wild) | — | they guard stones; none joins. |

**EBDX battle speech** (optional, trainer designer): give each Mega Warden a `megaOpp` line, for example Brann: "Some
things you forge to last!", Kaito: "Memory. Remember." and Kestrel at K8 wearing Morwen's Ring: "Mum. Just this
once. Answer me."

---------------------------------------------------------------------------------------------------
## 7. Implementation

| File | What |
|---|---|
| `plugins/Prismfall Mega/001_Mega_Config.rb` | limits, `STONES` (44 rows), `UNPLACED`, `FIELD_RULES`, `FIELD_NOTES` |
| `002_Mega_Battle.rb` | one Mega per side, Z-crystal block, the event and log; the per-side owner key for Z-Power |
| `003_Mega_Fields.rb` | gained-ability entry rules, the 8 showpieces, Field Notes lines |
| `004_Mega_Story.rb` | `pf_mega_stone(:ITEM[, "line"])` for map events (teaser line before the ring), conditions `mega_ring` and `mega_stones`, Debug menu "Prismfall Mega..." |
| `plugins/Prismfall Trials/114_Quests_Megas.rb` | the Ring-Day, Brann's spare, Juno's Venusaurite and 14 stone quests (3 bosses, 4 rank-gated commissions) |
| `132_EventMons_Megas.rb`, `152_Talk_Megas.rb` | the three boss guardians; talk rows (new keys plus rows on Hesper and the Crucible Legate) |
| `001_Trials_Config.rb` | rank 3 rewards: Manectite (Zenith), Sharpedonite (Isenmar) |
| `design/TRIAL_EVENTS.yaml` | "Mega Evolution" maps: 25 stone events + the quest NPCs and objects, for the map builder |
| `pbs/` | nothing new: `MEGARING`, the stones and the forms are base data |
| `tools/harness/run_mega.rb`, `tools/harness/playtest/run_mega.sh`, `004_MegaBot.rb`, `make_mega_gif.py` | tests |

Requests to other workstreams are in `mapgen/REQUESTS.md` ("From the Mega Evolution workstream") and `design/BALANCE.md` §6b.

---------------------------------------------------------------------------------------------------
## 8. Tests

**Headless** (`PRISM_RUN_DIR=<run copy> PRISM_COMPILE=1 ruby tools/harness/run_mega.rb`): **59/59 passed**
(`docs/mega_test/REPORT.md`, transcript alongside). The run covers:
- data: 47 stones + Rayquaza; every stone placed or unplaced; R4 gates; quest, rank and event sources.
- a Mega in a field battle: the player's Camerupt on Volcanic primes and erupts, and the Mega comes before moves.
- the AI: Kaito's Hard gym battle through `Prismfall.gym_battle(8)`; Mega Lucario the turn it comes out, on the Colosseum.
- Mega + Z in one battle: one trainer's double (Mega Lucario + Hydro Vortex on turn 1), the player's side with both
  rings, and two trainers on one side.
- the per-side limit: two foe trainers with stones get one Mega (two under Essentials' own rule, as a control); two
  with Z-crystals get one Z (two under Z-Power's own rule).
- no ring means no Mega; wild Pokémon never Mega; a Z-crystal blocks Rayquaza.
- all 8 showpieces; No Guard and Magic Bounce entry rules on Mega Evolution, not fired twice; the Field Notes lines.
- the quests: the teaser at 3 badges, the Ring-Day gate (6 badges no, 7 badges without the Caldera choice no, then
  yes), the ring and Aggronite, the Old Pincer boss paying out the Pinsirite (with the player's Mega Charizard), and
  the brazier writ (a lie fails, the truth pays).

`tools/harness/run_trials.rb` still passes **142/142** with the new quests, talk keys and events.

**Real engine** (`tools/harness/playtest/run_mega.sh assemble | install | mega | gif`; a lean copy: Audio and the big
Graphics folders are hard links, because mkxp-z's PhysFS won't follow symlinks). The run is the player's own Fight menu
against a test "Brann" (Torkoal, then Camerupt with a ring) on Volcanic:
- Fight, then Action **lights the EBDX Mega button** (`005_mg_02_mega_button_on.png`); Use on Flamethrower plays the
  Mega animation, and Mega Charizard X has Tough Claws.
- The Volcanic showpiece fired ("Charizard's Mega Evolution stirred the magma... the volcano is about to erupt!").
- Then the AI's Camerupt Mega Evolved when it came out (`015_mg_after_MegaEvolution2_Camerupt.png`). The run logged
  one Mega per side.
- **GIF:** `docs/battle_captures/mega/mega_evolution_ebdx.gif` (179 frames, 2.4× slow, 15.7 s), with key shots and the
  bot log beside it.
- **Balance note from that run:** a Lv 56 Mega Camerupt on Volcanic beat a Lv 60 Mega Charizard X and Snorlax. The
  Mega primes an eruption, Earth Power primes more, and each eruption gives +1 Sp. Atk. At Gym 7 the trainer designer
  should keep its set honest (BALANCE §6b).

---------------------------------------------------------------------------------------------------
## 9. Proposals and open items

1. **A shared Mega/Z button on EBDX's Fight menu** (for the EBDX Bridge owner and the Z owner). EBDX's Mega button
   already toggles with Action and previews the Mega form's move types. The proposal is to make that one slot a
   **"power" button** that shows Mega or Z depending on what the battler can do (a Mega-stone holder can't hold a
   Z-crystal, so they never clash). Toggling Z would preview the Z-move names and power on the move buttons, and the
   Z Yes/No box after the move pick would go away. Same keys and mouse as now. Hook point: `FightWindowEBDX#megaButton`
   and the `-2` toggle in `Battle#pbFightMenu`'s block (register a pending Z instead of a Mega), with
   `PrismfallZ.after_register` reading it.
2. **Z-Power config:** fold the per-side owner key into Prismfall Z-Power itself (one line in `PrismfallZ.owner_key`).
   This plugin's alias can then go.
3. **Bosses:** an optional `:mega => true` break effect for trainer bosses (Mega Evolve when the first shield breaks,
   as Rejuvenation's Latios does in its second bar). It would need the ring checks bypassed and the owner's name.
4. **Phase 2:** Legends Z-A Megas once the harness runs Gen 9 Pack 3.3.8 (§3.5).
5. **FIELDS.md:** include `PrismfallMega::FIELD_NOTES` in the generated sections.
