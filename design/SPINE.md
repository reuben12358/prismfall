# PROJECT SPINE — "Pokémon Prismfall" (working title)

## >>> REVISION 15 (user, 2026-11-19) <<<
**Character portraits are parked:** "skip the whole portrait thing for now, work on more important things." Juno keeps the pass-3 stopgap portraits. When portraits resume, use the 360 VS busts in Graphics/Transitions of the three games (see art/PORTRAIT_SOURCES.md). Spend effort on gameplay, maps, story and systems instead.

## >>> REVISION 14 (user decision, 2026-11-19) <<<
**Gym 1 is Normal-type**, to ease the player in (user: "gym 1 should be normal type to ease the player into the game"). Gym 2 was already Normal (Dorian), so the user left the fix to us ("whatever u think is correct"). Decision: **swap the town order of Saltmere and Briarwick.**
- **Gym 1 = Dorian Pell, Saltmere, Normal, `:GRAND_STAGE`.** Cap 15, a single battle. The gym is a simple, handsome theatre: a Jasmine-style walk-through (aisle, seats, a few trainers, the stage) with at most one gentle interaction. Grand Stage is the player's first field and must teach fields gently (the audience cheers flashy moves). Eevee "Understudy" is gifted after Gym 1.
- **Gym 2 = Tamsin Loom, Briarwick, Bug, `:SILKWOOD`.** Cap 19, a **double battle** ("a thread holds because it's twisted with others"). The linked-heddle Weaving Hall becomes Gym 2's puzzle: the first real puzzle, still friendly.
- **Story:** Chapter 2 becomes "Curtain Call" (Saltmere, Gym 1, J1, the Mourner's pageant hijack, the Gilded King page) and Chapter 3 becomes "The Weaver's Debt" (Briarwick, Gym 2, Tamsin's contract, Thistle). Re-check every cross-reference: the badge-case hum, Juno lines, Tamsin's Act V, the Plate bar order (bar 1 = Normal/Bug/Water, Normal still has no Plate), BALANCE caps, the Festival.
- **Geography:** Ferrow's Landing → coast → Saltmere (Elowen's free port) → inland → Gossamer Wood/Briarwick → north → Rimewood/Frostwick → Ebbmouth. Characters and their types are unchanged.

## >>> REVISION 13 (user feedback, 2026-11-19) <<<
1. **Trial Centers replace help centers.** Rejuvenation has Help Centers with many side quests; ours are per-kingdom "Trials" that express each kingdom's culture. Ashkaar: the Trial by Flames, combat-centred (think Noxus in League of Legends). Elowen: spiritual quests (think Ionia). Every other kingdom gets its own flavour. Lots of quests, some random and funny.
2. **No "Route 1 / Route 2" names.** Name every route the way Game of Thrones names places (the user's examples: "Frostwick Pass", "Rimewood Path").
3. **Routes are massive.** A route between two places can be split into two or more connected maps/paths.
4. **A world map of the region** is needed (the in-game Town Map and a design-level map).
5. **Encounters grow with badges.** Rarer Pokémon start appearing in previously visited areas after badges. Quest-reward and event Pokémon in the style of: chasing the Nidoran around the first town before battling and catching it (Rejuvenation), a Spidops/Litleo for beating boss Pokémon (Rejuvenation), the Pinsir/Heracross fights and the Torchic (Reborn).
6. **Gym puzzle difficulty curve.** Gym 1 is simple, with a layout like Jasmine's gym in HeartGold/SoulSilver: nothing complicated. From Gym 2 onwards the puzzles get more fun and ramp to Reborn level.
7. **Juno's portrait was rejected:** "it looks like burgh wore a wig". Portraits must not be one recognizable character repainted; build from female donors and change the features.

## >>> REVISION 12 (user decision, 2026-11-18) <<<
Juno's design direction is EVER-BLOOM (user: "everbloom kinda looked cooler ngl"): she wears the never-wilting blossoms of her aunt's Bride Tree, the flower girl of a wedding that never ended. Wreath, long veil-train, bouquet, white dress. Her personality stays warm, chatty and funny; the costume carries the sadness. Under Glass and Rot & Bloom are shelved. Story and script references to Juno's look should follow this.

## >>> REVISION 11 (user feedback, 2026-11-17 10:38) <<<
Character art v5 (the four Juno concept thumbnails) was rejected: "it looks god awful... theres so much good pixel art out there, surely we can do better."
- Drawing trainer sprites from scratch, pixel by pixel in code, has failed five times. Stop doing it.
- New method: KITBASH (frankensprite) from professional pixel art, the way real fangames build their casts. Use ~830 trainer fronts in the Reborn, Rejuvenation and Desolation folders, plus portraits (Faces), PIF/Uranium/Tectonic/Valhalla art and online resource packs. Take the base body, head/hair, outfit pieces and props from several donors at matching pixel density. Repaint by region with designed ramps. Hand-edit only small seams and details.
- Quality gate: nothing reaches the user unless it is indistinguishable in quality from its donors, shown side by side at 1x and 2x. An independent critic who didn't make the art reviews it first.
- Design still matters: each character needs a hook (silhouette, prop, pose, expression). The concepts are kept as design input, not as art.

## >>> REVISION 10 (user feedback, 2026-11-17) <<<
1. **Field effects, deeper.** Study how Reborn/Rejuvenation/Desolation implement fields (their Scripts/*.rb, fields.dat,
   fieldnotes.dat are in /home/claude/ref/games/<name>/) and bring their logic and depth into ours, keeping our good
   original ideas (e.g. Electroweb travelling along Silkwood's threads). Flavor must treat Pokémon as amazing creatures that
   harness and transform their surroundings, not victims ("choking on ash" is the wrong tone). Transitions must lead to fields
   that are as interesting as the one they replace (Volcanic quenched → not "nothing").
2. **Every battle has a field** (except tutorial and a few special indoor battles): default fields for every map, every route,
   cave, town, interior where battles happen, every trainer and wild battle.
3. **Every field gets a backdrop as good as the Volcanic and Silkwood ones** (the user loved those). Bland backdrops (e.g. the
   Factory/Zekrom boss) are not acceptable. The games' Battlebacks folders are available as source.
4. **Opponents are thematically consistent and build for their field**: Wardens and trainers pick Pokémon, abilities, items and
   moves that exploit their field, and the AI plays the field.
5. **Characters must be exciting.** Juno v4 read as "soulless" and "a recolor gender swap of Sword/Shield's grass leader".
   Characters need a bold, specific concept with personality in pose, face and silhouette. Study a wide range of sprite art
   to learn what makes characters remarkable; show the user several distinct concepts before polishing one.
6. **Puzzles at Reborn's level.** Gym and dungeon puzzles must be genuinely complex and satisfying (study Reborn's puzzles).
7. **Keep hunting** the internet for great tilesets and sprite resources.

## >>> REVISION 9 (user feedback, 2026-11-16 23:36) <<<
**Borderlands.** Kingdoms connect only through borderland regions that blend the two kingdoms' biomes, cultures and
wild Pokémon, each with at least one intermediate town showcasing how the two peoples live and trade together (or don't).
Ashkaar (fire) and Isenmar (ice) must NOT share a border; their war is fought across the sea (the Shattered Ice strait).
User's examples: Ashkaar–Ossaria = a volcanic, ash-laden desert/forest; Isenmar–Elowen = frozen forests. World design defines
the full adjacency graph, every borderland and its town, consistent with the locked gym order.

## >>> REVISION 8 (user feedback, 2026-11-16 12:19) <<<
1. **PRIORITY: the early game.** Get the prologue and first two chapters (through Gym 1 and its aftermath, then Gym 2's arc)
   fully fleshed out and playable — final-quality maps, full scripted dialogue, events, trainers, comedy scenes — before more
   mid/late-game work. Other workstreams continue at lower priority.
2. **Tileset rule clarified:** the ban is on the basic stock FRLG/RSE-looking tiles. Rejuvenation/Reborn-style tiles are all
   fine even when saturated. Use best judgement; the only test is "is this visually beautiful?". Keep finding more beautiful
   tilesets and use them. Maps need FAR more density and detail than the current drafts.
3. **Original character art.** Named characters need original trainer sprites, overworld sprites and expressive portraits made
   for this game, in the style of Rejuvenation/Reborn custom trainers. Reused stock sprites are placeholders only.
4. **A working visual battle demo** (Gen 5-style EBDX scene + field effects) must be shown to the user.

## >>> REVISION 7 (user feedback, 2026-11-16 10:02) <<<
**The game needs funny moments.** Rejuvenation-style comedy alongside the dark plot: expressive character-portrait speech
bubbles over the overworld (circular portrait with an expression: crying-yelling, deadpan, smug, panicking; plus emote
effects like sweat drops and shock lines), running gags, banter between companions, a comic-relief recurring character or two,
and absurd optional moments. Roughly one good laugh per chapter, never undercutting the big dramatic beats.
Dialogue lines carry `[portrait: NAME, expression]` tags; the `Prismfall Cutscenes` plugin renders them.

## >>> REVISION 6 (user feedback, 2026-11-16) — supersedes everything below where they conflict <<<
1. **The Ashkaar–Isenmar War.** At some point in the main story (story team picks the act; mid-game, Act III–IV suggested) open
   war breaks out between Ashkaar (Fire/Dragon) and Isenmar (Water/Ice). It must feel like a full war (fronts, sieges, the
   player caught between, choices with consequences) and its climax is shown as a **fully pixel-animated cutscene** (like
   Rejuvenation's Renegade Route set pieces) containing **at least one beam clash** (e.g. the kingdoms' legendaries or
   Wardens' aces: fire/dragon beam vs water/ice beam).
2. **Festival of Champions reframed.** It is a sacred ceremony held by ALL kingdoms to choose the one person who receives
   **Arceus's Blessing** (the story team decides exactly what the Blessing is and how it ties to the Sovereign Seat, the
   Plates/Tuning and Voss's plan). **Each kingdom sends its champions/delegates** and those are the people you fight: Wardens,
   rivals, royals, faction figures, all met earlier in the story (Rev 5 rule stands). Who each kingdom sends depends on your choices.
3. **Companion matches.** Your companions/rivals can be drawn against each other. Those NPC-vs-NPC matches resolve according
   to your choices, and the player can optionally **watch each match's key moments as a pixel-animated highlight** cutscene.
4. **Cutscene engine.** A 6th plugin, `Prismfall Cutscenes`, provides code-driven pixel-animated cutscenes (Pokémon/trainer
   sprites, camera pans, beams, beam clashes, impacts, screen shake, text) used for the war climax and Festival highlights.
5. **Art target = Pokémon Rejuvenation's look** (user sent a screenshot: tall detailed timber buildings, lush layered
   foliage, textured paths, moody weather/lighting overlays). The user is fine with using the actual tilesets from
   Rejuvenation/Reborn/Desolation for this personal project; credit their artists in CREDITS.md.

## >>> REVISION 5 (user feedback, 2026-11-15 21:21) — superseded by Revision 6 where they conflict <<<
1. **Festival opponents must be characters the player has met in the story.** Every Festival entrant who can be the player's
   opponent (all draw pools and exhibitions) must have ≥2 meaningful prior story encounters and be introduced by Act IV at the latest.
   No new characters introduced at the Festival "for plot reasons". The Rev-4 foreign entrants (Isaura, Drey, Mireille, Thorne)
   are REMOVED unless the story team weaves one in as a genuine recurring character from early acts; their narrative functions
   move to established characters. (Ruin-only figures must be met earlier on the Ruin Route.)
2. **Art style: Gen 4 or Gen 5 (DPPt/HGSS/BW) only. No Gen 3 tiles or Gen 3 palette anywhere** (the stock Essentials FRLG/RSE
   "Outside" look is banned). Maps must not use generic tree walls as filler: borders and backgrounds come from what the place IS
   (cliffs, sea, city walls, rooftops, mountains, ruins, canals, forest canopy appropriate to the biome).
3. **Authentic places at real scale.** A kingdom seat is a castle city (think King's Landing as a Pokémon game would draw it):
   curtain walls and gatehouses, districts, a keep or palace on high ground, harbours, markets, cathedrals, slums, multi-screen
   city maps and grand interiors (throne room, great hall, galleries), never a small house. Same for Zenith (towering tech city),
   Nadir (vertical undercity), Ashkaar (volcanic dragon-citadel), Isenmar (frozen sea fortress-ports), Ossaria (desert/canyon
   cities and tombs), Antumbra (mirror-world palace), Crownhaven (the Accord's capital and Festival arena).

## >>> REVISION 4 (user feedback, 2026-11-15 21:11) — superseded by Revision 5 where they conflict <<<
**Sister-game cameos are OUT of the Festival.** The Festival of Champions (bracket, exhibitions, draw pools) uses
**original characters only**: Wardens, rivals, Valen and his successor candidates, faction figures (Mourner/Rowan, Meridian's
champions, etc.), and new ORIGINAL foreign entrants if needed. The Reborn/Rejuvenation/Desolation cameos (Lin, Amaria, Shelly,
Alexandra, Venam, Shiv, Garret, Melia, Titania, Nova) become **optional sidequest cameos**, the way Rejuvenation features
Reborn's Aya and Adrienn: each appears in a small optional sidequest somewhere in the world (Antumbra's distortion is the
in-universe reason), usually ending in **one optional, tough fight** levelled for where it sits (some can be post-game).
Never required, never in the main finale. The QF "headline cameo" slot is replaced by an original character from the draw.

## >>> REVISION 3 (user feedback, 2026-11-15 evening) — superseded by Revision 4 where they conflict <<<
1. **Kingdom names (final):** Sylvan Crown → **Elowen, the Evergreen Crown** · Umbra → **Antumbra, the Kingdom Behind the Glass** ·
   Glaciem → **Isenmar, the Frozen Sea** · Ember Dominion → **Ashkaar, the Dragonfire Dominion** · Dunelands → **Ossaria, the Bone Sands**
   (fossil country) · Lumen → **Zenith, the City Above** (Lumen City is its capital district) · Undercity → **Nadir, the City Below**.
   Crownhaven unchanged. Same types/cities as the Revision 2 table.
2. **Choices matter (Reborn/Rejuvenation/Desolation-style).** Core tracks: **Bonds** (affinity with key characters), faction
   **Standing** (Hollow / Meridian / Accord), **Resonance** (the player's Legend Plate axis: Harmony ↔ Ruin), and a **Choice log** of
   named decisions. Narrative spec: `story/10_CHOICES_ENDINGS.md` (written by the Narrative Systems designer; uses symbolic keys
   stored in Core save data — not Game Switches).
3. **The Festival bracket is choice-driven (replaces the LOCKED player path).** Stages and caps are unchanged (R16 90, QF 92, SF 94,
   Final 96, Hijack 100, True Finale 100), but each stage's OPPONENT is drawn from a candidate pool by rules over bonds/standing/
   choices (e.g. Juno or someone you wronged in R16; Kestrel redeemed or fallen in the SF; Valen or his successor in the Final; the
   hijacker depends on what you exposed). The default path in Revision 2 is the fallback when no rule matches. Every candidate
   (and variant, like "Kestrel (Fallen)") needs a trainer team.
4. **Game overs** (Rejuvenation/Desolation-style): ≥12 story game overs, each with an ID, title, epitaph and fair foreshadowing,
   recorded in a cross-save **Ledger** file. Finding them all unlocks the **Ruin Route** — a secret alternate storyline
   (cf. Rejuvenation's Renegade Route) with its own ending(s).
5. **Endings:** 1 canon **Good**, 1 canon **Bad**, ≥4 **Grey** endings, plus the **Ruin** ending(s). Decided by accumulated choices +
   the final decision. Seen endings are also recorded in the Ledger.
6. **Also adding:** Rejuvenation-style new-game **passwords** (QoL/challenge toggles), **Field Notes** (in-game field encyclopedia
   that fills in as you encounter fields), playable **interludes** as other characters, and a **quest log**.

7. **Coordinator rulings (2026-11-15):** Game Switches/Variables **301–400** are reserved for gym and dungeon puzzles
   (gym n uses 300+5n … 300+5n+4; World design owns them). Drowned **Aurelia** lies beneath Underveil on the **north**
   coast, under Zenith's cliffs. Rejuvenation-style multi-bar **boss battles** live in a 5th plugin, `Prismfall Bosses`.
   Core adds **Rock Climb** (`BADGE_FOR_ROCKCLIMB`). Velmora is town-map **region 0**.

## >>> REVISION 2 (user feedback, 2026-11-15) — superseded where Revision 3 conflicts <<<
1. **Kingdoms.** Velmora is a realm of seven kingdoms plus the neutral capital. Each kingdom's wild Pokémon are
   dominated (~70%) by its types; borderland routes between kingdoms are mixed. Gym order/cities/wardens/fields/caps are
   UNCHANGED, so the journey criss-crosses kingdoms and revisits each one 2–3 times as the story escalates (each return
   shows consequences: Bleed spread, political fallout).
   | Kingdom | Character | Wild types | Gym cities (gym #) |
   |---|---|---|---|
   | **The Sylvan Crown** | vast fairy-tale forest kingdom, old monarchy | Fairy, Grass, Bug, Normal | Briarwick (1), Saltmere (2, its free port), Verdance (9), Gloaming (17, the forest's heart). Ferrow's Landing is its southern ferry dock. |
   | **Umbra** (the Reverse Kingdom) | a mirrored realm behind the Sylvan forest (cf. Platinum's Distortion World); upside-down rules, `:INVERSE` territory, Giratina's domain | Ghost, Psychic, Dark | Lucent (12), Gravenmoor (14) |
   | **Glaciem** | frozen northern coast kingdom | Water, Ice | Ebbmouth (3), Rimeholt (10) |
   | **The Ember Dominion** | volcanic dragon-lord kingdom | Fire, Dragon | Cindervault (7), Wyrmrest (18) |
   | **The Dunelands** | desert and canyon kingdom | Ground, Rock | Duneholt (5), Cragholm (13) |
   | **Lumen** | gleaming tech city-state of progress and airships (Piltover-like); Meridian Concord's home | Electric, Steel, Flying | Lumen City (4), Skyreach (11, airship spire), Cogsworth (15, foundry district) |
   | **The Undercity** | the slums and sumps beneath Lumen (Zaun-like); the Hollow recruits here | Poison, Dark, Fighting | Mirefen (6, toxic runoff marsh), Ironreach (8, pit-fighting arenas in old mine shafts), Underveil (16, the undercity's heart) |
   | **Crownhaven** (neutral) | the Accord's capital at the realm's center | — | Festival venue |
2. **Tone:** easy to get into like Rejuvenation (warm, accessible Act I hook), then steadily darker — Desolation-leaning by Act III–V.
3. **All original characters.** NO canon-game characters (Cynthia, Lance, Steven, Alder, Diantha, Leon, Geeta are REMOVED).
   Festival invitees are **cameos from the sister fangames — Pokémon Reborn, Rejuvenation and Desolation** — plus Velmoran entrants.
   The story team researches those games and fixes the roster in `design/CAMEOS.md` (7 cameo champions: trainer type IDs
   `FESTIVAL_<NAME>`, ace teams in the spirit of their source game). The player's Quarterfinal opponent (was Cynthia) becomes
   the headline cameo chosen there. Everything else in the player path is unchanged.
4. **Tropes the user loves** (from Rejuvenation and the mainline games) — work several in: an Eeveelution battle/gauntlet,
   gym double/tag battles, partner battles with rivals, Rejuvenation-style multi-bar **boss battles** for legendaries/villains
   (EBDX ships a boss-battle module — check it before building our own), one legendary arc per kingdom (Giratina in Umbra, etc.),
   classic set pieces (haunted house, fossil revival, Unown ruins, Safari-style reserve, post-game Battle Tower / Warden rematch gauntlet).
5. **Maps are being built for the user.** A Map Builder tool generates RPG Maker XP map files programmatically using the stock
   Essentials tilesets; World design owns the map ID scheme (100+) and the layout specs it consumes.
6. **Base project & reference.** Recommended base project = Manurocker95's *Pokemon-Essentials-21-With-Unofficial-EBDX*
   (Essentials 21.1 + Hotfixes + EBDX 1.4.7.1 + Gen 9 Pack + Luka's Scripting Utilities + PWT), cloned read-only at
   `/home/claude/ref/ebdx` (full project: PBS with **Gen 1–9 / 1,025 species**, Plugins/, Graphics/, Data/*.rxdata, 71 sample maps).
   Use `/home/claude/ref/ebdx/PBS` for ID validation and `/home/claude/ref/ebdx/Plugins/Elite Battle DX` for EBDX code;
   `/home/claude/ref/essentials/Data/Scripts` for readable core scripts. Starters: **any Gen 1–9 starter**.
   Never `Marshal.load` the reference .rxdata files in Ruby (untrusted data); parse them with a pure-Python reader run as `python3 -I`.
7. **PBS ships as suffixed files** (v21.1 merges `PBS/<base>_<suffix>.txt`): trainers_prismfall.txt, trainer_types_prismfall.txt,
   items_prismfall.txt, encounters_prismfall.txt, map_metadata_prismfall.txt. Packaging renames our pbs/ files automatically.

This is the single source of truth every workstream builds from. Items marked **LOCKED** must not be
renamed or reordered by any agent (other files depend on them). Everything else may be expanded.
If you think a LOCKED item is genuinely wrong, finish your work using it as-is and write the
objection to `/home/claude/fangame/design/SPINE_FEEDBACK.md` (append, don't overwrite).

## Tech stack (LOCKED)
- Engine: **Pokémon Essentials v21.1** + **v21.1 Hotfixes** plugin. Runs on mkxp-z (Ruby 3.1 — avoid Ruby 3.2+ only syntax/features).
- Battle scene: **Elite Battle: DX (EBDX) — unofficial port for Essentials v21.1, v1.4.7.1 (Manurocker95)**, Gen 5–style animated sprites + dynamic camera.
- Reference source (read-only, do NOT execute anything in it): `/home/claude/ref/essentials` (Maruno17/pokemon-essentials master, based on v21.1). Scripts: `Data/Scripts/`, PBS: `PBS/`. Grep it to verify every class/method/constant/PBS key you use.
- Our code ships as Essentials plugins in `/home/claude/fangame/plugins/<Plugin Name>/` (each with `meta.txt` + numbered `.rb` files). PBS additions go in `/home/claude/fangame/pbs/`.
- Syntax-check all Ruby with `ruby -c <file>` (Ruby 3.3 is installed locally; keep code 3.1-compatible).
- Plugins (LOCKED names):
  - `Prismfall Core` — 18 badges, level caps, difficulty modes, Festival of Champions tournament manager, shared constants.
  - `Prismfall Field Effects` — the field effect engine + all fields + seed items.
  - `Prismfall EBDX Bridge` — swaps EBDX battle backdrops/visual FX when a field is set or changes. Requires EBDX + Field Effects.

## Shared integration contract (LOCKED)
- Namespaces: `Prismfall` (core), `FieldEffects` (fields). Never monkey-patch without `alias`-chaining the original.
- Setting a field for the next battle: `setBattleRule("field", :VOLCANIC)` (Field Effects plugin must extend the battle rule system to accept this). Default per-map fields via `FieldEffects::MAP_FIELDS = { map_id => :FIELD_ID }`.
- In battle: `battle.field_effect` → Symbol (`:NONE` if none). Change with `battle.change_field(:NEW_ID, "message")`.
- Every field change MUST call `FieldEffects.notify_change(battle, old_id, new_id)`, which runs `EventHandlers.trigger(:prismfall_field_changed, battle, old_id, new_id)`. The EBDX Bridge listens to this.
- Every field definition exposes `:name`, `:backdrop` (String, base name of battle background graphic, e.g. `"field_volcanic"`), `:intro_message`.
- Story flags: Game Switches **101–300** and Variables **101–300** reserved for story (story team owns the registry in `design/FLAGS.md`). Systems (Core plugin) store state in their own save data, NOT switches.
- Trainer type IDs: `LEADER_<FIRSTNAME>` (e.g. `LEADER_TAMSIN`), rivals `RIVAL_KESTREL`, `RIVAL_JUNO`, champion `CHAMPION_VALEN`, villains `HOLLOW_*`, `MERIDIAN_*`, cameo champions `FESTIVAL_<NAME>`.

## Trainer versioning scheme (LOCKED — shared by trainer data + Core plugin)
- `trainers.txt` sections are `[TRAINER_TYPE,Name,Version]`.
- Difficulty: base version `v` = **Standard**. `v+100` = **Hard** variant, `v+200` = **Casual** variant. Core plugin picks the variant for the active difficulty and falls back to `v` if the variant doesn't exist.
- Rival battles: base version = `battle_number*10 + starter_slot`, where starter_slot is 0 = player chose a Grass starter, 1 = Fire, 2 = Water (e.g. Kestrel K3 vs a Fire-starter player = version 31).
  The rival's starter is written in PBS as the **Gen 1 line** (Bulbasaur/Charmander/Squirtle lines). At battle start, Core swaps it to the **same-generation counterpart** of the player's starter (matching evolution stage; level-up moveset regenerated for that species; item/nature/EVs/IVs kept).

## Fixed places (LOCKED)
- Starting village: **Ferrow's Landing** (ferry dock on the south coast; the "last ferry" arrives here).
- Capital + Festival venue: **Crownhaven** (seat of the Accord; only reachable after Badge 18 / story-gated).

## World
- Region: **Velmora** — a fractured continent of highlands, drowned coasts, and old-growth forest, ringed by islands. 18 cities, each built around an **Imprint**.
- Core myth: Three hundred years ago, in **the Prismfall**, Arceus's 18 Plates fell from the sky and embedded in Velmora's land. Each Plate "imprints" its type onto the surrounding land — the in-world reason **field effects** exist. Cities grew around Imprints because they are resources (geothermal fire, endless current, fertile soil...).
- Governance: **The Accord**. Each city's Gym Leader is its **Warden** — hereditary-ish guardian of its Plate and de facto governor. Above them sits the **Sovereign Seat** (Champion). Badges = a Warden's formal endorsement.
- The threat: **the Bleed** — Imprints have begun spreading beyond their cities, warping land (towns frozen, forests turned to crystal). Velmora is under border quarantine.
- The **Festival of Champions**: held once a decade; champions of other regions are invited; the winner holds the Sovereign Seat. 18 badges are the entry requirement for a Velmoran challenger. All 18 Plates are brought together for the opening ceremony.
- The protagonist is **Unimprinted** — immune to Imprints and able to walk into Bleed zones. (Secret, revealed late: they carry a fragment of the **Legend Plate**, the 19th plate that holds every type and none.)

## Factions (names LOCKED, depth open)
- **The Hollow** — eco-zealots who believe the Plates are poisoning Velmora and must be destroyed. Leader: masked **"the Mourner"** (identity is the story team's call). Main antagonists Acts I–II, sympathetic, partially right.
- **Meridian Concord** — energy conglomerate that harvests Imprints to power the region. CEO **Aurelian Voss**. Ally-seeming early, true antagonist by Act IV: plans to use the Festival convergence to forge an artificial Judgment and bind Arceus.
- **The Accord / League** — Champion **Valen Corrigan**, Sovereign for 30 years. Has known about the Bleed for decades; the Festival's ceremony secretly re-tunes the Plates. Tragic guardian, not a villain — but has lied to everyone.

## Main cast (names LOCKED)
- **Kestrel Vane** — aggressive rival; child of the disgraced former Ghost Warden. Picks the starter with type advantage over the player's.
- **Juno Hale** — friendly rival; picks the starter weak to the player's. Becomes Grass Warden in Act III (player battles her for Badge 9).
- **Aurelian Voss**, **Valen Corrigan**, **the Mourner** — see factions.
- Starters: the player may choose **any Gen 1–9 starter** (Reborn-style).

## Acts (LOCKED boundaries)
| Act | Title | Gyms |
|---|---|---|
| I | The Last Ferry | 1–4 |
| II | Imprints | 5–8 |
| III | Fault Lines | 9–12 |
| IV | The Drowned Crown | 13–16 |
| V | Sovereign | 17–18 + Festival of Champions |

## The 18 Gyms (LOCKED: order, type, city, leader, field ID, level cap)
| # | Type | City | Warden | Signature field ID | Level cap |
|---|---|---|---|---|---|
| 1 | Normal | Saltmere | Dorian Pell | `:GRAND_STAGE` | 15 |
| 2 | Bug | Briarwick | Tamsin Loom | `:SILKWOOD` | 19 |
| 3 | Water | Ebbmouth | Marisol Reyes | `:WATER_SURFACE` | 23 |
| 4 | Electric | Lumen City | Rook Calder | `:NEON_GRID` | 27 |
| 5 | Ground | Duneholt | Sahar Ostrand | `:DESERT` | 31 |
| 6 | Poison | Mirefen | Corvin Mott | `:CORROSIVE_MIRE` | 35 |
| 7 | Fire | Cindervault | Brann Holloway | `:VOLCANIC` | 39 |
| 8 | Fighting | Ironreach | Kaito Ren | `:COLOSSEUM` | 43 |
| 9 | Grass | Verdance | Juno Hale (succeeds Rowan Ashby) | `:FLOWER_GARDEN` | 47 |
| 10 | Ice | Rimeholt | Anja Sorrel | `:FROZEN_LAKE` | 51 |
| 11 | Flying | Skyreach | Odessa Gale | `:STORMFRONT` | 55 |
| 12 | Psychic | Lucent | Ilsa Marr | `:MINDSCAPE` | 59 |
| 13 | Rock | Cragholm | Bastian Ore | `:CRYSTAL_CAVERN` | 63 |
| 14 | Ghost | Gravenmoor | Ysolde Ashgrave | `:HOLLOW_CATHEDRAL` | 67 |
| 15 | Steel | Cogsworth | Magnus Strade | `:FACTORY` | 71 |
| 16 | Dark | Underveil | Nyx Calloway | `:NEW_MOON` | 75 |
| 17 | Fairy | Gloaming | Celestine Aubade | `:FAIRY_TALE` | 80 |
| 18 | Dragon | Wyrmrest | Sigrun Ashfall | `:DRAGONS_DEN` | 85 |

Festival of Champions caps rise per round to match that round's ace: R16 90, QF 92, SF 94, Final 96, Hijack + Arceus 100.

## Field roster (LOCKED IDs; ~30 fields)
Gym fields (above) plus story/route fields:
`:CAVE`, `:MOUNTAIN`, `:SNOWY_MOUNTAIN`, `:BEACH`, `:UNDERWATER`, `:RAINBOW`, `:WASTELAND`, `:ASHEN_WASTE`,
`:DARK_CRYSTAL`, `:SCRAPYARD`, `:INVERSE`, `:BLEED` (this game's signature corrupted field — unstable, borrows random
effects from other fields), `:PRISM_ARENA` (Festival finale — cycles through gym fields).
Known transitions (more allowed): VOLCANIC→ASHEN_WASTE (quenched), FROZEN_LAKE→WATER_SURFACE (melted),
WATER_SURFACE↔UNDERWATER (Dive), CRYSTAL_CAVERN→DARK_CRYSTAL (darkened), FACTORY→SCRAPYARD (wrecked),
FLOWER_GARDEN has 5 growth stages, any field→BLEED in specific story battles.
Built-in Electric/Grassy/Misty/Psychic Terrain must interact sensibly with fields (overlay, suppress, or transform).
Field "seed" items (Reborn-style): `ELEMENTALSEED`, `MAGICALSEED`, `TELLURICSEED`, `SYNTHETICSEED` — effect varies by field.

## Festival of Champions (LOCKED player path)
Entrants include the Velmoran challenger (player), Kestrel, Juno, selected Wardens, and 7 invited cameo champions from the
sister fangames (Reborn / Rejuvenation / Desolation — roster in `design/CAMEOS.md`) (+ the reigning Sovereign, Valen).
Player's bracket path:
1. Round of 16 — **Juno Hale** (ace 90)
2. Quarterfinal — **headline sister-game cameo** (see CAMEOS.md) (ace 92)
3. Semifinal — **Kestrel Vane** (ace 94)
4. Final — **Champion Valen Corrigan** (ace 96)
5. Hijack — **Aurelian Voss** on `:PRISM_ARENA` (ace 100)
6. True finale — **Arceus** boss battle, type and field shifting (lv 100)
Other cameo champions are optional exhibition battles during the Festival week.

## Rival battle slots (LOCKED)
- Kestrel: K1 intro (lv 6), K2 before Gym 3, K3 after Gym 5, K4 at Gym 8 arc, K5 Gym 11 arc, K6 Gym 14 arc, K7 Gym 17 arc, K8 Festival semifinal.
- Juno: J1 Gym 1 arc (Saltmere promenade, before Dorian), J2 Gym 6 arc, J3 = Gym 9 leader battle, J4 Festival Round of 16.

## Tone
Reborn/Rejuvenation-style: dark, politically tangled, character-driven, mature themes (loss, corruption, sacrifice)
but ultimately hopeful. Gyms are puzzles + set-piece battles; difficulty is high, with selectable difficulty modes.

## Output locations
- Story: `/home/claude/fangame/story/` — Design docs: `/home/claude/fangame/design/` — Setup/docs: `/home/claude/fangame/docs/`
- Plugins: `/home/claude/fangame/plugins/` — PBS: `/home/claude/fangame/pbs/`
