# Z_MOVES — Z-moves in the main game (SPINE Revision 23)

> SPINE Rev 23 (user): Z-moves join the main game, tied to the Mega Ring, Reborn/Rejuvenation-style. The ring Bastian
> gives after Badge 13 enables both Mega Evolution and Z-moves, still one of each per side per battle. All 18 type
> crystals are spread from 13 badges on (finds, quests, boss drops), with the same "no counter to the next two Wardens"
> rule as stones. The Eevee Octave's reward becomes the Eevee plus the Eevium Z, with no separate ring. Some late fights
> may use a Z instead of a Mega where the story fits.

Before Rev 23, Z-moves were only the Eevee Octave's (8 type crystals on the Octave's trainers, and Vesper's Z-Power
Ring as the post-game reward). The battle code is unchanged: `plugins/Prismfall Z-Power` (design/EEVEE_OCTAVE.md §5)
and `plugins/Prismfall Mega` (one Mega and one Z per side). Stones: `design/MEGA_EVOLUTION.md`.

## 1. One ring
- **The item:** the base project's **Mega Ring** (`MEGARING`), the Warden's ring Bastian gives in Cragholm after
  Gym 13 (`OS_RING_DAY`, MEGA_EVOLUTION.md §4). `PrismfallZ::RING = :MEGARING`; the player's check is
  `PrismfallZ.player_ring?`. The name stays the base item's ("Mega Ring"); in the story it is a Warden's ring.
- **Why it answers crystals** (Bastian says it in the Ring-Day scene, Vesper again at the Octave): a Z-crystal is a
  sliver of **Glassfall glass**, tuned by the Choir to one Imprint; the ring's chip is grind off the Crown's own stone.
  "The chip's grind off the Crown's stone, and the glass came out of the night it cracked. Same crown, one way or
  another" (Bastian): the ring hears a sliver as it hears a heartstone. **The glass is not the Crown's stone or a
  Plate**; the PC's splinter stays the only missing piece (story editor; 01_WORLD_LORE §3 "Choir glass", 09_MYSTERIES
  "Wording rules"). How slivers got everywhere: Choir pilgrims left them to soak where each Imprint runs strongest.
- **One of each per side per battle:** a side may use one Mega and one Z-move (`PrismfallMega::LIMIT` / `Z_LIMIT`).
  A Pokémon holding a crystal can't Mega Evolve; a stone holder can't hold a crystal.
- **Save compatibility:** `ZPOWERRING` stays in `pbs/items_zpower.txt` (re-described as an old cantor's ring) and
  still counts (`PrismfallZ::LEGACY_RINGS`), so a save that holds it loses nothing. Nobody hands it out any more.
- **NPCs** need no ring for a crystal, only a story reason to have one (§4). Wild Pokémon never use Z-Power.

## 2. Crystals and Z-moves
`pbs/items_zpower.txt` (21 crystals + the legacy ring), `pbs/moves_zpower.txt` (20 Z-moves + Extreme Evoboost),
`PrismfallZ::CRYSTALS` / `TYPE_ZMOVES` / `EXCLUSIVE`.
- **18 type crystals:** Normalium (Breakneck Blitz), Fightinium (All-Out Pummeling), Flyinium (Supersonic Skystrike),
  Poisonium (Acid Downpour), Groundium (Tectonic Rage), Rockium (Continental Crush), Buginium (Savage Spin-Out),
  Ghostium (Never-Ending Nightmare), Steelium (Corkscrew Crash), Firium (Inferno Overdrive), Waterium (Hydro Vortex),
  Grassium (Bloom Doom), Electrium (Gigavolt Havoc), Psychium (Shattered Psyche), Icium (Subzero Slammer), Dragonium
  (Devastating Drake), Darkinium (Black Hole Eclipse), Fairium (Twinkle Tackle). Power from the base move (Gen 7 table),
  category from the base move, through Protect for 1/4.
- **Species crystals** (Velmora has the species): **Snorlium Z** (Snorlax, Giga Impact → Pulverizing Pancake, 210) and
  **Mimikium Z** (Mimikyu, Play Rough → Let's Snuggle Forever, 190). They keep their own power (`002_ZPower_Moves.rb`).
  The Eevium Z (Eevee, Last Resort → Extreme Evoboost) stays the Octave's reward. Not added: Pikanium (Volt Tackle is
  an egg move here), the Alolan and Gen 7 starter crystals (a different region's lines), legendary crystals.

## 3. Where the player finds them (`PrismfallMega::Z_CRYSTALS`)
The same rule as the stones (MEGA_EVOLUTION.md §5.2): a crystal first obtainable with *b* badges is usable from
*u* = max(*b*, 13), and its Z-move's type must not answer Warden *u*+1 or *u*+2. Checked by `run_mega.rb`.

| Badges | Crystal | Where (map) | How |
|---|---|---|---|
| 2 | Icium Z | Frostwick Pass, the avalanche gully (Rock Smash) (577) | hidden; "rings and waits" |
| 4 | Steelium Z | Static Tunnels Depths, the magnetite seam (Flash) (605) | hidden; "rings and waits" |
| 8 | Rockium Z | Grudgestone Quarry B1F, the gem seam (685) | hidden; "rings and waits" |
| 8 | Grassium Z | The Rootdeep, a root-wrapped ledge (Surf) (680) | hidden; "rings and waits" |
| 10 | Flyinium Z | Cloudstair Summit, the wind-scoured ledge (726) | hidden; "rings and waits" |
| **13** | *(the ring)* | Cragholm, Bastian (363) | story |
| 13 | Psychium Z | Hindmoor, the humming standing stone (781) | hidden |
| 13 | Buginium Z | The Jawbone Ridge, in a dead tree's resin (780) | hidden |
| 13 | Fairium Z | Darkglass Mine B1F, under the shot-out lamps (785) | hidden |
| 13 | Mimikium Z | Lantern Hospice, Gravenmoor: sewn into a Pikachu-shaped rag doll (384) | item |
| 14 | Poisonium Z | The Smokestack Parade, a soot-black vent (811) | hidden |
| 14 | Ghostium Z | Thistledown Manor attic: the doll who waited (547) | quest `EL_DOLL_WHO_WAITED` (with the Banettite) |
| 14 | Electrium Z | Gale Post Hall, Skyreach: the dead-letter drawer (325) | quest `ZE_RETURN_TO_SENDER` (with the Pidgeotite) |
| 15 | Firium Z | The Crucible: the brazier's own sliver (240) | quest `AS_BRAZIER_WRIT` (with the Salamencite) |
| 15 | Groundium Z | Cragholm rack, the tyrant's heart dig (360) | quest `OS_TYRANT_HEART` (with the Tyranitarite) |
| 15 | Darkinium Z | Underveil Moon Market, the Barons' kennel (423) | quest `NA_MOON_MARKET_DOGS` (with the Houndoominite) |
| 15 | Dragonium Z | Pyre Keep: sewn into Old Cinder's harness (248) | **boss** `AS_OLD_CINDER` (with the Charizardite X) |
| 15 | Waterium Z | Under the Drownings, a drowned shrine (Dive) (822) | hidden |
| 16 | Normalium Z | Pell Playhouse: Dorian's encore, the Pageant's "prop jewel" (154) | quest `EL_ENCORE` (with the Lopunnite) |
| 16 | Snorlium Z | Mothwell, the hay barn with a Snorlax-sized dent (850) | item |
| 17 | Fightinium Z | The Last Rung, Ironreach: in Kaito's unit's armband (260) | quest `NA_MEMORY_KATA` (with the Lucarionite) |
| 21 (post-game) | Eevium Z | Crownhaven, the Eevee Octave (489) | the gauntlet's reward |

Why each sits where it does: Bug and Fairy answer Magnus and Nyx (and Fairy, Celestine and Sigrun too), so they must
come by 13; Ghost, Dark and Normal answer Ysolde, so not before 14; Fire and Ground answer Magnus, so 15; Fighting
answers Magnus and Nyx, so 17 (16 would also pass); Poison and Steel answer Celestine, so 14 at the latest. The five
before the ring use `pf_z_crystal`, whose teaser is "The crystal is cold, and it rings very faintly against your
fingers... then it falls silent, as if listening for something."

## 4. Who uses Z-moves (trainers)
The story rule (MEGA_EVOLUTION.md §1.2) carries over: an NPC uses a crystal only if the story gives them one, and never
a stone and a crystal on one trainer unless designed. From 13 badges a fight may use a Z-move **instead of** its Mega
where that fits the character better.
- **The Eevee Octave** (unchanged): Choir orphans, so Choir-tuned crystals; the gauntlet design is the same.
- **Celestine, Gym 17** (Fairy Tale, double, 80), her Ruin-route copy and her Festival draw: **Mimikium Z on her Mimikyu**
  (Let's Snuggle Forever) **instead of Mega Mawile**. Story reason: Gloaming's dusk-chapels still sing the complete
  Hymn (01_WORLD_LORE), and they tuned the crystal for the costume-ghost of her storybook. Mimikyu returns to the slot
  Mawile took; Azumarill stays the Casual cut.
- **Nobody else:** no other fighter has a story reason for a crystal yet. Brann is unchanged (as designed, per the user).
- **Trainer lines:** when a trainer's Z-move fires (after "...unleashed its full-force Z-Move!", before it hits) or
  their Pokemon Mega Evolves, they may say a line: `PrismfallSpeech::LINES` in
  `plugins/Prismfall Z-Power/005_ZPower_TrainerSpeech.rb`, keyed by trainer type and name (all versions) or type, name
  and version; once per battle each. With EBDX the trainer slides in and speaks (EBDX's `pbTrainerSpeak`, as its battle
  scripts do); without EBDX, or while the trainer has no front sprite yet, it is a named battle message. Celestine:
  *"This is the part where it hugs you. Hold still. It's worse if you don't."* Real engine:
  `docs/battle_captures/speech/`.

## 5. Tests
- `tools/harness/run_mega.rb` **74/74** (section 9: Celestine's Z-move line, once, right after the unleash; no line for
  a trainer without one): the one ring (Mega Ring alone gives the player one Mega and one Z in one
  battle; the legacy Z-Power Ring alone still wakes crystals, not stones; no ring, no Z), the crystal distribution (all
  18 + 2 placed once, R4 with the Ring, quest/boss/event sources and gates), a species Z-move (Pulverizing Pancake), the
  crystal teaser before the Ring, and the trainer rule (36 entries per mode Mega, 3 per mode use Celestine's Z).
- `tools/harness/run_trials.rb` **142/142**, including the Z-Power section (now with the Mega Ring) and the Octave
  reward (the Eevee + the Eevium Z, no ring).
- `tools/validate_trainers.py` 0 errors; `tools/validate_fields.rb` 0 errors.
- **Win rates** (`run_winrates.rb` cell G17M (renamed in round 4), `PRISM_PREPARED=1`, Standard, 60 fights; `PRISM_FOE_NOZ=1` swaps the
  foe's crystal for a Life Orb): Celestine with her Z-move **100%** (60/60), without it **97%** (58/60). A prepared
  Steel and Poison team at the cap beats her either way; the Z-move fires (Let's Snuggle Forever) in the logged runs.
  The other Mega fights are unchanged (MEGA_EVOLUTION.md §8).
- Real engine: not re-run for Rev 23 (no battle code changed beyond the ring check and the species-crystal power);
  `tools/harness/playtest/run_zpower.sh` still applies and now needs `MEGARING` in the Bag instead of `ZPOWERRING`.
