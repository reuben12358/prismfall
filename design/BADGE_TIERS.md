# BADGE_TIERS — rarer Pokémon on old roads after each badge (SPINE Revision 13, item 5)

> User: "after you get badges, more rarer pokemon start appearing in previously visited areas"

**Data:** `pbs/encounters_badgetiers.txt` (72 overlay sections, 126 slots, every Chapter 0–4 map with wild encounters).
**Code:** `plugins/Prismfall Trials/007_Trials_BadgeTiers.rb`. **Hints:** `140_BadgeTier_Rumours.rb`.
**Check:** `python3 -I tools/validate_badge_tiers.py` (0 errors; its warnings list the new Rev 14 routes that don't have a
base table yet). **Test:** `tools/harness/run_trials.rb` §5 (the Ferrymen's Mile before/after Badges 1–3).

---

## 1. How it works

- **Overlays, not replacements.** Each section of `encounters_badgetiers.txt` is an ordinary v21.1 encounters section
  (the compiler validates it) whose *version* encodes the badge: `[520,101]` = map 520 with 1+ badges, `[520,104]` = 4+.
  When the game builds a map's encounter table, the plugin **appends** every unlocked overlay's slots to the live table.
  Nothing is removed, so the common species stay common and the new ones are rare by weight (2–5 against ~100).
- **Encounter versions still work.** Overlay version = `100 × (encounter_version + 1) + badges`. The normal world (0) uses
  101–118. When the Bleed-spread version 1 starts in Act IV, the 1xx overlays switch off and only 2xx overlays (if anyone
  writes them) apply, because a Bleed-touched map is a new table and gets its own tiers.
- **Time of day.** A `Land` overlay also feeds `LandNight`/`LandDay`/`LandMorning`... when the base table splits Land by
  time, unless the overlay defines that variant itself (then the variant is the tier's night list). Same for `Cave`/`Water`.
- **New methods.** An overlay may add a method the base table lacks (e.g. `HeadbuttHigh`); its step chance is the header's
  or the encounter type's default. A map with **no base table at all** gets nothing, so a route still being built is never
  filled with nothing but rare spawns; its overlays light up the moment `pbs/encounters.txt` gains the map.
- **Badge mid-map.** When a badge is awarded, the current map's table is rebuilt at once.
- **Bug-Catching-Contest style lookups** (`choose_wild_pokemon_for_map`) see the same overlays.

## 2. The hint ("the grass rustles")

1. **Rumours at the Trial halls.** Every overlay section has a rumour (`[map, badge] => "..."`, `{map}` becomes the current
   map name). When you earn badge *b*, every map with a tier at *b* becomes a rumour. Each Trial keeper offers the newest
   rumours you haven't followed yet (`pf_trial_keeper`), and every board has a **Rumours** option. They hint, they don't
   list: "Big pawprints in the heather on the Ferrymen's Mile. Something's been at the honey pots."
2. **The rustling notice.** The first time you step back onto a map after its tier opened, a short line plays:
   *"The grass here rustles differently than you remember..."* (`TIER_ENTRY_NOTICE`, once per tier per map).
3. **Quest log → Rumours** keeps every rumour you've heard, tagged with its badge.
4. *(Optional, map builder)* a "rustling grass" tile animation on tier maps: `Condition: tier(map_id) >= 1`.

## 3. Tiers and levels

| Tier | Opens with | Levels | Weight | What goes in |
|---|---|---|---|---|
| 1 | Badge 1 (Dorian) | 13–16 | 3–5 | a rarer local and a "visitor" from the next kingdom over |
| 2 | Badge 2 (Tamsin) | 17–20 | 3–4 | the same, one step stronger; Eevee returns to the hedgerows |
| 3 | Badge 3 (Marisol) | 21–24 | 2–4 | something fierce (Hawlucha, Scyther, Absol) |
| 4 | Badge 4 (Rook, end of Act I) | 25–28 | 2–3 | one **early sighting** of a pseudo-legend or a rare line, plus one rare local |

**Level rule:** tier *b* = [cap(*b*) − 6, cap(*b*) − 3], where cap(*b*) is the level cap while holding *b* badges
(19, 23, 27, 31...). So a tier is always worth meeting at the level you are now, on a road you walked at level 5.

**Only revisits.** A map gets tier *b* only if it is first reached with fewer than *b* badges (maps.json `segment`, which
Rev 14 made authoritative; the Deepwood and Cocoonfall count from 2 because Cut needs 2 badges now).

## 4. The early maps (Chapters 0–4)

| Leg (segment) | Map (ID) | Tier 1 | Tier 2 | Tier 3 | Tier 4 |
|---|---|---|---|---|---|
| Gym 1 leg (0) | Ferrow's Landing (100), rods | Chinchou | Horsea, Luvdisc | Clauncher, Skrelp (Good Rod) | Staryu, **Dratini** |
| | the Ferrymen's Mile (520) | Teddiursa, Munchlax; night Zorua | Farfetch'd, Audino; night Murkrow | Swablu, Hawlucha | Stufful, Togepi |
| | Windfall Row (521) | Applin, Skiddo | Eevee, Hoppip; Headbutt Shuckle | Toedscool, Pawmi | Fomantis, Scyther |
| | Lacecliff Walk (527)* | Binacle, Krabby | Pyukumuku | Wimpod | Cramorant, Skarmory |
| | Marram Down (528)* | Helioptile, Buneary | Sandygast, Gossifleur | Maractus | Tropius |
| | Saltmere (140), rods | Clamperl | Finizen | Bruxish, Mantyke (Good Rod) | Frillish, Dhelmise |
| Weavers' Road (1) | the Grey Saltings (541) | — | Krabby, Ducklett | Cramorant, Pyukumuku | Mareanie, Wimpod |
| | Brinecut Mine 1F / B1F (544/545) | — | Drilbur, Carbink / Onix, Tinkatink | Bronzor, Glimmet / Beldum | **Larvitar** / **Gible** |
| | the Dyers' Ford (552)* | — | Wooper, Smeargle | Lotad, Spritzee | Mareep, **Goomy** |
| | Thistledown Lea (540) | — | Deerling, Hoppip; night Misdreavus | Tauros, Girafarig | Bouffalant, **Riolu** |
| | Thistledown Manor (546) | — | Litwick | Honedge | **Dreepy** |
| | Gossamer Wood (524) | — | Joltik, Venipede | Scyther, Surskit | Bramblin, Larvesta |
| Cut-gated (2) | Gossamer Deepwood (525) | — | — | Tangela, Fomantis | Phantump, Shiinotic |
| | Cocoonfall Hollow (548, Bleed) | — | — | Bergmite, Carbink | Cryogonal, Charjabug |
| Gym 3 leg (2) | Spinners' Rise (566)* | — | — | Mareep, Skiddo | Dubwool, Tauros |
| | Frostwick Pass (577)* | — | — | Sneasel, Absol | Bouffalant, **Frigibax** |
| | Frostwick (570), rods | — | — | Feebas (Good Rod) | Veluza |
| | Rimewood Path (578)* | — | — | Snorunt, Smoochum | Cryogonal, Stantler |
| | the Rimewood (562) / Glade (563) | — | — | Sneasel, Absol / Milcery | Cryogonal, Milcery / Hatenna |
| | Frostflat Causeway (560), side road | — | — | Eiscue, Sneasel | Bouffalant, Absol |
| | the Rehearsal (568, Bleed) | — | — | Impidimp | Mimikyu |
| | Gullcry Cliffs (561) | — | — | Flamigo, Wattrel | Pelipper, Drampa |
| | Gullcry Caves 1F / B1F (564/565) | — | — | Clauncher, Eiscue / Frillish | Relicanth / **Bagon** |
| | Ebbmouth (160), rods | — | — | — | Corsola, Feebas (Good Rod) |

\* No base table in `pbs/encounters.txt` yet (new Rev 14 routes); their overlays wait for it.
**Bold** = an early pseudo-legend sighting (weight 2, base form, evolves well after its tier). These run ahead of
POKEMON_AVAILABILITY's schedule on purpose (Dratini and Bagon by one act, Dreepy by most of the game, as a haunted-manor
secret). **For the world lead to confirm or trim.**

## 5. The rule for the rest of the game (Chapters 5+)

1. **Cadence.** A map gets an overlay at each of the **three badges after it is first reached** (*s*+1, *s*+2, *s*+3),
   then one at each Act boundary it outlives (Badges **4, 8, 12, 16**). From Act IV's Bleed-spread (encounter version 1),
   write `2xx` overlays only for maps the story sends the player back to.
2. **Two slots per tier**, weights 2–5: one **rarer local** (the kingdom's types, a family not yet on that map) and one
   **visitor** (a neighbouring kingdom's or borderland's type, or the route's "secret"). Every fourth tier may carry one
   early pseudo-legend or rare line at weight 2.
3. **Levels** by the formula above. Evolved forms only at or above their evolution level; stone/trade/friendship
   evolutions not below 20 (the encounters validator's rules).
4. **Never**: legendaries, mythicals, Paradox Pokémon (postgame only), the 27 starter lines, gift-only lines (Abra,
   Pansage/Panpour, Spiritomb), or an event Pokémon's exact species+ability on its own map. Imprinted variants (regional
   forms) only in Bleed zones or next to their Imprint.
5. **Methods follow unlocks**: Good Rod 3, Rock Smash 2, Surf 6, Super Rod 10 badges (the validator enforces it).
6. **Every overlay gets a rumour** that a local would say. The validator warns about missing ones.

## 6. Notes for other workstreams

- **World lead:** base tables for 527, 528, 552, 566, 577, 578 are needed; the overlays are ready. Please keep one
  Fighting family wild before Saltmere (SWAP §8): Crabrawler on Lacecliff Walk or Mankey on Marram Down. Event Pokémon
  cover it already (Timburr in Ferrow's, the Crabrawler/Clobbopus duel on Lacecliff Walk).
- **Renumbering:** overlays are keyed by map ID. If a map ever moves, move its `[id,1xx]` sections and its rumours too;
  `validate_badge_tiers.py` reports overlays for IDs missing from maps.json.
- **Packaging:** `tools/package.sh` copies `pbs/encounters_badgetiers.txt` to `PBS/` unchanged; v21.1 merges it as an
  `encounters_*` suffix file.
