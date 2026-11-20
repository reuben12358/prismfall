# BADGE_TIERS — rarer Pokémon on old roads after each badge (SPINE Revision 13, item 5)

> User: "after you get badges, more rarer pokemon start appearing in previously visited areas"

**Data:** `pbs/encounters_badgetiers.txt` (76 overlay sections, 132 slots, every Chapter 0–4 map with wild encounters, plus the
Badge-8 pseudo-legend revisits of rule R7).
**Code:** `plugins/Prismfall Trials/007_Trials_BadgeTiers.rb`. **Hints:** `140_BadgeTier_Rumours.rb`.
**Check:** `python3 -I tools/validate_badge_tiers.py` (0 errors, 0 warnings; it also checks the Revision 16 gates on the
combined base + overlay table at every badge count). **Test:** `tools/harness/run_trials.rb` §5 (the Ferrymen's Mile before/after Badges 1–3).

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
| Gym 1 leg (0) | Ferrow's Landing (100) | Chinchou 5 (OldRod) | Horsea 4, Luvdisc 3 (OldRod) | Clauncher 4, Skrelp 3 (GoodRod) | Staryu 3, Shellder 2 (GoodRod) |
|  | The Ferrymen's Mile (520) | Teddiursa 4, Munchlax 3, Zorua 4 (LandNight) | Farfetch'd 4, Audino 3, Murkrow 3 (LandNight) | Swablu 4, Hawlucha 2 | Stufful 3, Togepi 2 |
|  | Windfall Row (521) | Applin 4, Skiddo 3 | Eevee 4, Hoppip 3, Shuckle 3 (HeadbuttHigh) | Toedscool 4, Pawmi 3 | Fomantis 3, Scyther 2 |
|  | Lacecliff Walk (527) | Binacle 3, Spearow 3 | Pyukumuku 3 | Wimpod 3 | Cramorant 3, Skarmory 2 |
|  | Marram Down (528) | Helioptile 3, Buneary 3 | Rolycoly 3, Cacnea 3 | Maractus 3 | Tropius 2 |
|  | Saltmere - Promenade & Market (140) | Clamperl 3 (OldRod) | Finizen 3 (OldRod) | Bruxish 3, Mantyke 3 (GoodRod) | Frillish 3, Dhelmise 2 (GoodRod) |
| Weavers' Road (1) | The Grey Saltings (541) | — | Krabby 4, Ducklett 3 | Cramorant 3, Pyukumuku 3 | Mareanie 3, Wimpod 2 |
|  | Brinecut Mine 1F (544) | — | Drilbur 4, Carbink 2 | Bronzor 3, Glimmet 3 | Stonjourner 2 |
|  | Brinecut Mine B1F (545) | — | Onix 3, Tinkatink 3, Nosepass 3 | Carkol 3 | Naclstack 2 |
|  | The Dyers' Ford (552) | — | Wooper 3, Smeargle 3 | Lotad 3, Spritzee 3 | Flaaffy 3, Dewpider 2 |
|  | Thistledown Lea (540) | — | Deerling 4, Hoppip 3, Misdreavus 3 (LandNight) | Tauros 3, Girafarig 3 | Bouffalant 3, Riolu 1 |
|  | Thistledown Manor (546) | — | Litwick 3 | Honedge 3 | Drifloon 2 |
|  | Gossamer Wood (524) | — | Joltik 4, Venipede 3 | Scyther 3, Surskit 3 | Bramblin 3, Larvesta 2 |
| Cut-gated (2) | Gossamer Deepwood (525) | — | — | Tangela 3, Fomantis 3 | Phantump 3, Shiinotic 2 |
|  | Cocoonfall Hollow (548) | — | — | Bergmite 3, Carbink 2 | Cryogonal 3, Charjabug 2 |
| Gym 3 leg (2) | Spinners' Rise (566) | — | — | Ponyta 3, Hoppip 3 | Dubwool 3, Miltank 2 |
|  | Frostwick Pass (577) | — | — | Sneasel 3, Absol 2 | Bouffalant 3, Cetoddle 2 |
|  | Frostwick (570) | — | — | Feebas 3 (GoodRod) | Veluza 2 (GoodRod) |
|  | Rimewood Path (578) | — | — | Smoochum 3, Delibird 3 | Cryogonal 2, Stantler 2 |
|  | The Rimewood (562) | — | — | Absol 2, Eiscue 3 | Cryogonal 3, Milcery 2 |
|  | Rimewood Glade (563) | — | — | Milcery 3 | Hatenna 2 |
|  | Frostflat Causeway (560) | — | — | Eiscue 3, Sneasel 3 | Bouffalant 3, Absol 2 |
|  | The Rehearsal (568) | — | — | Impidimp 3 | Mimikyu 2 |
|  | Gullcry Cliffs (561) | — | — | Flamigo 3, Wattrel 3 | Pelipper 3, Drampa 2 |
|  | Gullcry Caves 1F (564) | — | — | Clauncher 3, Eiscue 3 | Relicanth 2 |
|  | Gullcry Caves B1F (565) | — | — | Frillish 3 | Slowpoke 2 |
|  | Ebbmouth (160) | — | — | — | Corsola 3, Feebas 2 (GoodRod) |

Generated from `pbs/encounters_badgetiers.txt` (weights against the base table's 100). Every Chapter 0–4 road now has a
base table, so every overlay is live. **Revision 16:** no tier slot on these maps is a pseudo-legend (they wait for Badge 8,
rule R7: the Dratini, Beldum and Goomy sightings at Badge 4 are gone), and tier slots count toward the base table's limit
for answers to the next Wardens (≤5% a slot, ≤8% together with the base, checked on the combined table at every badge).
Badge-8 revisits that took over Act II's early pseudo-legend slots: `[601,108]` Gabite (the Rib Road), `[605,108]` Pupitar and
Metang (Static Tunnels Depths), `[648,108]` Sliggoo (the Weeping Fen).

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
7. **Revision 16** (`design/DISTRIBUTION_STUDY.md`, `design/warden_gates.json`): a tier slot that is a *gated* answer to a
   Warden still ahead (Tamsin: Fire/Rock; Marisol: Electric; Rook: Ground; later Wardens once their gates are set, R9) is
   at most 5 and keeps the combined table under 8%; nothing Fighting before Badge 1; no pseudo-legend line before Badge 8.
   `validate_badge_tiers.py` checks the base table plus every overlay open at each badge count.

## 6. Notes for other workstreams

- **World lead / Revision 16:** base tables for 527, 528, 552, 566, 577 and 578 now exist (Revision 16 pass). Revision 14's
  "one Fighting family wild before Saltmere" is withdrawn: Fighting arrives after Badge 1 (the Timburr berth quest, the
  tide-pool duel, Brinecut Mine's Machop/Timburr/Meditite, the Grey Saltings' Crabrawler).
- **Renumbering:** overlays are keyed by map ID. If a map ever moves, move its `[id,1xx]` sections and its rumours too;
  `validate_badge_tiers.py` reports overlays for IDs missing from maps.json.
- **Packaging:** `tools/package.sh` copies `pbs/encounters_badgetiers.txt` to `PBS/` unchanged; v21.1 merges it as an
  `encounters_*` suffix file.
