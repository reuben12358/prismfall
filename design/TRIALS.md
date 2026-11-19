# TRIALS — the kingdoms' side-quest institutions (SPINE Revision 13)

> User: "Just like how rejuvenation has help centers with a bunch of random quests, we need the equivalent of those side
> quests in our game. But because we have these kingdoms, instead of help centers, why dont we make something like a
> 'trial center' (ex: the fire/dragon kingdom has the trial by flames which usually involves around something like combat
> (think noxus from league of legends), the fairy forest has some sort of spiritual quests (think ionia from league of
> legends), etc)"

**Companion files.** Every quest, with full dialogue for the wired ones: `design/TRIALS_QUESTS.md` (generated).
Event and quest-reward Pokémon: `design/EVENT_POKEMON.md` (generated). Badge-gated encounters: `design/BADGE_TIERS.md`.
Map events: `design/TRIAL_EVENTS.yaml`. Code: `plugins/Prismfall Trials/`. Test: `tools/harness/run_trials.rb`
(report in `docs/trials_test/REPORT.md`). Regenerate the docs with `ruby tools/trials_docs.rb`.

Order and names follow SPINE **Revision 14** (Ferrow's Landing → the Strand Road → Saltmere, Gym 1 Normal → the Weavers'
Road → Briarwick, Gym 2 Bug → Spinners' Rise / Frostwick / the Rimewood → Ebbmouth, Gym 3) and `design/SWAP_GYM1_GYM2.md`.
Maps are keyed by **ID**; names are given as they stand today and may change.

---

## 1. What we took from Rejuvenation's Help Centers

Rejuvenation's Help Center events (read from its map data) are a board menu: each request shows a title and a
**"Rec Lv."**, and is either open, *answered* (taken), *completed* or *expired*. Accepting says where the giver waits
("I'll be at the lumber yard east of the Weather Institute") and calls `activateQuest(:id)` for the quest log; the giver
then runs the quest; completion flips a switch and adds a log line. Clearing a whole board earns a special reward (April's
egg with an egg move). Reborn's event Pokémon are plain events: a `pbWildBattle` with follow-up branches (the Pinsir/Heracross
pair where the one you help clears a log or a web).

We keep all of it and change the frame:

| Rejuvenation | Prismfall |
|---|---|
| One Help Center chain, same everywhere | **Eight Trials, one per kingdom**, each with its own name, hall, keeper, board, rank names and kind of quest |
| Title + Rec. Lv | Title + **★ rank needed** + Rec. Lv; quests at a higher rank stay hidden until you rise |
| answered / completed / expired | `:available → :active → :done` (or `:failed`, `:expired`); state lives in Core save data, never in switches |
| "I'll be at..." | the board says where the giver waits; the giver still gives their **briefing** once (`:from_board`) |
| board-clear egg | **rank-up rewards** (5 ranks per Trial, some are Pokémon) |
| quest log (`activateQuest`) | **Quests** in the pause menu: Active / Done / Rumours; it also lists the map builder's story quests (`pfm_quest`) |
| — | **Joint quests** on borderland boards count for both kingdoms |
| — | **Rumours**: the Trial halls are where you hear that rarer Pokémon now walk old roads (`BADGE_TIERS.md`) |

**Ranks.** Points from quests (1–5 each). Rank thresholds: 0 / 3 / 8 / 15 / 25 points (`RANK_POINTS`). Each Trial's
hall keeper hands out the reward for every rank you've reached since you last spoke to them.

**Choices and bonds.** Quests only move registered keys: Bonds (`JUNO`, `KESTREL`, `MARISOL`, `VALEN`...), Standing
(`MERIDIAN`, `HOLLOW`, `ACCORD`) and Resonance (`RES±`, Harmony/Ruin), through Core's `apply_effects`. A quest's own
decisions (which side you took, whether you opened the parcel) are its **outcome**, kept in Trials state and readable in
conditions (`quest_outcome(:IS_OATH_PARCEL) == :opened`). No new NARRATIVE_KEYS were needed.

**Why not the Ledger.** The Ledger is the cross-save record (game overs, endings, cameos beaten). Quests are per save, so
they live in the quest log. Cameo quests still write the Ledger through Core's `cameo_battle`, as before.

---

## 2. The eight Trials

Each entry: name and halls · philosophy · who runs it · how quests are posted and ranked · the flavour of its quests ·
its final (rank-5) trial. Counts are total / wired now.

### Elowen — **The Quiet Way** (19 / 14) · *Ionia*
- **Halls.** Lantern Houses, run by the **Order of the Listening Root**. Early: the *wayshrine* in **Ferrow's Landing (100)**
  (a lantern rope over a roadside shrine, Brother Teasel), the **Saltmere Lantern House** (suggested 148, sharing a wall
  with the Lantern Theatre: the only silent building in the noisiest town in Elowen, which is the joke), the **Briarwick
  Lantern House** (suggested 126, a hollow tree, the oldest in the south). Seat: the **Hall of the Listening Root** in
  Verdance (280). Inner house: the **Twilight Cloister** in Gloaming (440). Borderland board: the Half-Tally at Frostwick.
- **Philosophy.** "The Root listens." Balance, grief allowed to finish, spirits treated as neighbours, kindness done for
  its own sake. Elowen's fairy-tale monarchy keeps the Plates; the Quiet Way keeps the people who live around them.
- **Keepers.** Brother **Teasel** (Ferrow's; under a vow of soft voice; can't be heard, then accidentally shouts), Sister
  **Hollin** (Saltmere; lost the war for silence years ago; earplugs and a slate, writes in capitals), Mother **Aldreth**
  (Briarwick; blind, weaves the lanterns, knows what you did before you say it), Sister **Maelon** (Frostwick, married to
  Isenmar's Ingrith), the **Abbess** in Verdance.
- **Posting and ranks.** Each request is a paper lantern on a rope; you untie it to take it; when it's done the lantern is
  lit and let go over the roofs. Ranks: **Seedling, Sapling, Bough, Heartwood, Evergreen**. Rewards: Soothe Bell, TM20
  Safeguard, a Triage Comfey, Magical Seeds.
- **Quest flavour.** Pilgrimages and riddling shrines (*Three Loyal, Three Knots*, which seeds the Loyal Three / Ogerpon
  story), spirits that need finishing (*The Rehearsal*, *The Rootward Wake*), koans that are really puzzles (*The Sound of
  Saltmere*: find three silences), chases through Bleed zones only you can enter (*The Orchard Sings*), and kindness.
  **Quiet Deeds** are its signature: unposted kindnesses the map offers (hang up blown washing, sit with an old sailor);
  the Quiet Way counts them realm-wide, and *telling* the keeper what you did halves the reward ("That's boasting.").
- **Final trial.** *The Twilight Cloister*: cross seven dusk-chapels where every choice list hides one silent option.
  Speaking sends you back to the start. Celestine is waiting in the eighth.

### Isenmar — **The Tally** (10 / 4) · *the saga-hall*
- **Halls.** The **Net Loft** in Ebbmouth (suggested 168), the **Half-Tally** at the Two Hearths in **Frostwick (573)**
  (borderland: one board, runes on the Isenmar side and lanterns on the Elowen side), the **Great Tally** in the Mead Hall
  of Rimeholt (306).
- **Philosophy.** "The sea keeps count. So do we." Deeds, endurance, oaths kept, the whale-road. Isenmar is poor, proud and
  in debt for its heat; what it can still give you is a name in a song.
- **Keepers.** **Bersi Gullsong**, Ebbmouth's skald (exaggerates everything; a skald never checks his sources), **Ingrith**
  the rune-carver at Frostwick, **Old Halla Brinesdottir** at the Great Tally.
- **Posting and ranks.** Requests are runes carved on the **Tally Mast**; a finished deed gets a notch beside your name and a
  verse. Ranks: **Driftwood, Oarhand, Harpooner, Shieldwall, Sagaborn**. Rewards: Mystic Water, TM72 Avalanche, Never-Melt
  Ice, and at Sagaborn the Lapras "Saga" (Freeze-Dry).
- **Quest flavour.** Oaths you must not break (*The Oathbound Parcel*: it's a Snom, and it's eating the oath), feasts and
  contests (*A Deed for the Skald*: flatten the dock bully, out-fish Old Gudrun, or simply lie, and Bersi sings it anyway),
  endurance rites on the ice (*The Harpoon Rite*: stand your ground against the Old Bull Cetitan), sea-rescues and the
  refugees of the Thaw, and finally the war (*The Saga of the Shattered Ice*, sung straight for once from your war choices).
- **Final trial.** Be the witness Bersi needs to sing the war truthfully.

### Zenith — **The Prize Exchange** (9 / 3) · *Piltover: invention grants*
- **Halls.** A **Rotom kiosk, P-3NNY**, everywhere Meridian has a desk: the Ferrow's customs hall (108), the Saltmere
  Harbour Office (143), the Ebbmouth Lattice station (160). The seat is the **Prize Exchange floor** in Lumen's Council
  Ward (194): a brass trading floor with a split-flap board.
- **Philosophy.** Progress you can measure. Data is the currency of the future ("so is currency"). Every Call is funded by
  someone, usually Meridian, and the moral grey is the point: the efficient answer and the kind one are rarely the same form.
- **Keepers.** P-3NNY (ALL CAPS, polite, has been programmed with one joke) and later **Registrar Odalys Venn** (precise,
  courteous, terrifying).
- **Posting and ranks.** "Calls for Proposals" clack onto the split-flap board; accepting flips your name into the ACCEPTED
  column. Ranks are licence grades: **Applicant, Licensee, Fellow, Patent-Holder, Laureate**. Rewards: Exp. Candies, Cell
  Batteries, Synthetic Seeds, an Ability Patch.
- **Quest flavour.** Bureaucracy as comedy and as conscience (*Form 7-B*: sign the disposal form, or walk the adoption form
  past three stamps and get a Charcadet), field surveys (battle on three fields; Field Notes count them), data with a moral
  (*The Lattice Hums Wrong*: who gets the recordings, Meridian, the Ebb Guild or Larch), sentient appliances, couriers
  under embargo, and Cogsworth's rigged invention bout.
- **Final trial.** *The Laureate's Prize*: win a rigged contest and hear the Registrar admit it.

### Nadir — **The Gutter Book** (9 / 0) · *Zaun: undercity odd jobs*
- **Halls.** Chalk boards wherever the City Below drinks: the Mirefen noodle cart (220), the Charwell char-burners' wall
  (630, borderland D), **the Last Rung** at the bottom of an Ironreach lift-shaft (260), a Moon Market stall in Underveil (423).
- **Philosophy.** Nobody down here gets anything free. You earn, you owe, you pay. Jobs come with a cut, and some of them
  you shouldn't take.
- **Keeper.** **Six-Fingers Ottoline**, fixer. "It's yours. Don't make it mine."
- **Posting and ranks.** Chalk marks; Ottoline wipes one off with her thumb when you take it and takes her cut when it's done.
  Ranks: **Drip, Runner, Fixer, Sumpwise, Undercrown**.
- **Quest flavour.** Pit fights (*Pit Ringer*: six bouts and a boss Falinks troop), clean water and who owns it, debt
  collecting for Mother Gutter (pay one, forgive one, fight one), lift strikes, lamp-runner children lost in the sumps, a
  noodle cart that has never given anyone above a four, and the Sweetrot vendors' craving for terrible tea (the payoff of
  running gag 1). Venam's and Garret's cameo quests are posted here.
- **Final trial.** Mother Gutter's ledger: whatever you did, do it on purpose.

### Ashkaar — **The Trial by Flames** (9 / 1) · *Noxus: strength*
- **Halls.** **The Crucible**, an arena on the Cindervault caldera rim (240), the Scaldwater truce-baths (650, borderland E),
  the Wyrmrest proving ground (460). Early outpost: the **Legion recruiting barge** moored in Saltmere's free harbour (146),
  where bouts are legal because the Elowen crown can't stop them.
- **Philosophy.** "Strength is the only honest coin." Anyone from anywhere can rise; nobody asks who your mother was, only
  how hard you hit. Lying is a crime in Ashkaar, so even its quests are honest about their price ("Will I get hurt?" "Yes.").
- **Keepers.** **Sergeant Brakka Emberhide** (the barge), **Legate Varra Kosk** (the Crucible), **Herald Pyke** (the gong).
- **Posting and ranks.** **Writs of Flame**: iron tokens branded with your mark. Finished writs go up on the Wall of the
  Proven. Ranks: **Kindling, Ember, Brand, Pyre, Dragonsworn**. Rewards: Charcoal, a Flame Orb, a Deino egg, a Life Orb.
- **Quest flavour.** Arena gauntlets with no healing (*The Little Crucible*, *Seven Bouts*), boss-Pokémon hunts
  (*The Lava-Tube Terror*, a Druddigon that joins), honesty trials by combat (*The Trial of Truth*, *Adequate Swords*),
  escorts that turn out to be about the war (*Ashes Home*: a Nadir-born legionnaire's urn and his Houndour), dragon-egg runs,
  and one terrified dragon-rider recruit.
- **Final trial.** *Dragonsworn*: the Legate's dragons on the Dragon's Den, and the oath, which you may refuse.

### Ossaria — **The Rolls of Unearthing** (8 / 0) · *bone sands*
- **Halls.** Tablet racks at the Copperdune caravanserai (610, borderland C), the **Hall of Unearthing** at Duneholt's
  Dig Lab (200/209), the Vigil embalmers (770), the Cragholm lift-house (360).
- **Philosophy.** Everything is buried somewhere. Digging is how Ossaria remembers, and whoever owns the dig owns the past.
- **Keepers.** **Curator-Elect Nasrin Vael** and the caravan houses.
- **Posting and ranks.** Baked **clay tablets**: finished work breaks the tablet in two. Ranks: **Sandsifter, Digger,
  Delver, Tombwise, Bonewright**.
- **Quest flavour.** Excavation and fossils (Kevin, the interns' 'fossil', who is a Carbink and has heard all their gossip),
  riddle-trading caravans, tomb freight and who it belongs to, Unown inscriptions that read differently from the official
  story, sinkhole rescues in a Bleed zone, a dead Elector who wants to cast one last vote.
- **Final trial.** *The Bonewright's Rite*: reassemble a whole skeleton from the pieces you dug across the kingdom.

### Antumbra — **The Rite of Reflection** (8 / 0) · *the mirror world*
- **Halls.** The Glassmere reading-pool (753, borderland H), **the Speculum** in Lucent (346), the lantern-priests' glass in
  Gravenmoor (380).
- **Philosophy.** Your reflection knows you better than you do. The Veiled Synod mediates with Giratina; the Rite teaches
  the living to live with their other halves.
- **Keepers.** **Lector Saffi Ivarne** and her reflection, who disagree about everything.
- **Posting and ranks.** Requests in mirror-writing, read in the glass. Your reflection signs the Speculum when you finish
  (a little late). Ranks: **Glimpse, Gleam, Mirror, Speculum, Behind-the-Glass**.
- **Quest flavour.** Inverse-logic puzzles (an umbrella that keeps the rain in), reflections that came back reversed
  (*Your Other Half*), a student whose reflection gets better marks, echoes that answer before you ask, shadows that fall
  upward, and Shiv's dream-walking cameo.
- **Final trial.** *Behind the Glass*: one playable night as your own reflection (and the payoff of the mirror gag).

### Crownhaven — **The Hall of Petitions** (8 / 0) · *the capital*
- **Halls.** The Pilgrim's Rest shrine-post (890, borderland K), the **Hall of Petitions** in the Market Ring (496), the
  Pilgrims' Quarter board (497).
- **Philosophy.** All eighteen gates send their troubles here. The Accord is a bureaucracy that has forgotten it was meant
  to help; answering petitions is how you remind it.
- **Keeper.** **Clerk-Superior Amadeus Fenwright** (stamps everything twice, for luck and for the archive).
- **Posting and ranks.** Petitions sealed in each kingdom's wax. Ranks: **Petitioner, Courier, Envoy, Concordant, Hand of the
  Accord**. The capital's board mixes every kingdom's flavour: it is where they all meet.
- **Quest flavour.** Festival-week errands and diplomacy (four inches of pavilion), the lost-property tent's eel receipt
  (Kestrel's, from Chapter 4), Masque invitations, the Chancellor's second ledger, Valen's last errand, the Eighteen Shrines,
  and the postgame Warden gauntlet. Lin's postgame cameo is posted here.
- **Final trial.** *Hand of the Accord*: one petition from every kingdom in a day (needs rank 4+ in five Trials).

### Borderland outposts
Borderland towns carry a small board that is both kingdoms' at once: the **Half-Tally** in Frostwick (wired), the
Charwell wall, the Scaldwater truce-baths, Copperdune's rack, Glassmere's pool, Vigil's rack, Pilgrim's Rest. Quests there
can be **joint** (`:joint => { :ELOWEN => 2 }`), like *Two Hearths, One Pot*.

---

## 3. The early game in brief (all wired, full dialogue in `TRIALS_QUESTS.md`)

| Ch | Quest (Trial) | Where (map) | Hook and twist | Reward |
|---|---|---|---|---|
| 1 | The First Lesson (Elowen) | Ferrow's wayshrine (100) | do one unasked kindness; *don't tell* the monk | Harmony +1, 2 pts; starts Quiet Deeds |
| 1 | The Tart Thief (Elowen) | Ferrow's Landing (100, 103) | chase a Nickit round the village; it has been feeding Kestrel | **Nickit** (Stakeout); Kestrel ±1 |
| 1 | The Scarecrow Walks (Elowen) | Windfall Row (521, 523) | Coll didn't build a scarecrow; water it | **Sudowoodo**, or spare it (Harmony) |
| 1 | Master of Nothing (Elowen) | Dockmaster's House, the Dovetail (107, 109) | something is still aboard the last ferry | **Wattrel "Mast"** |
| 1 | The Last Plank (Elowen) | the empty berth (100) | a Timburr mends a berth for a ferry that won't come | **Timburr "Plank"** (Mach Punch) |
| 1 | Form 7-B (Zenith) | customs hall, lighthouse (108, 103, 106, 107) | sign the disposal or chase three stamps; Hesper warms the crate | **Charcadet**, or $500 + Meridian |
| 2 | The Tide-Pool Feud (Elowen) | Lacecliff Walk (527) | Reborn-style rival duel: pick a side; the winner punches open a sea-cave | **Crabrawler** or **Clobbopus** |
| 2 | The Borrowed Lanterns (Elowen) | Saltmere (140, 145–147) | five lanterns; one is a Kecleon; one is a stagehand's only audience | **Kecleon** (Protean), Silk Scarf |
| 2 | Field Survey: Coastal (Zenith) | any P-3NNY kiosk | battle on three fields | Exp. Candies |
| 2 | The Little Crucible (Ashkaar) | Legion barge (146) | three bouts, no healing; then the mascot boss | **Litleo "Cinderpaw"** (boss joins) |
| 2 | A Hole in the Sky (Elowen) | Lantern Theatre paint loft (145) | the Mourner walked through the painted sky; repaint it | **Smeargle "Brush"** (your palette) |
| 2 | The Sound of Saltmere (Elowen) | Saltmere, breakwater (140, 146, 147) | koan: three silences | **Ralts** |
| 2 | The Orchard Sings (Elowen) | the Glassed Orchard (522) | chiming hoofprints in the glass | **Galarian Ponyta** |
| 3 | Three Loyal, Three Knots (Elowen) | Dyers' Ford, Gossamer, Briarwick (552, 524, 120) | three riddling shrines tell the true Loyal Three story | Magical Seeds; lore |
| 3 | The Horn and the Pincer (Elowen) | Gossamer Wood (524) | Heracross vs Pinsir; the one you help clears a shortcut | **Heracross** or **Pinsir** (Moxie) |
| 3 | The Silkthief (Elowen) | Guildhall, Deepwood (123, 525) | the silk thief was keeping the moths warm | **Spidops** (boss) or leave it guarding |
| 4 | Two Hearths, One Pot (Isenmar + Elowen) | Frostwick, Rimewood, Halvard's (573, 562, 576) | 19-year cook-off; or put both in one pot | joint points, Rare Candy |
| 4 | The Oathbound Parcel (Isenmar) | Frostwick → Ebbmouth (573, 561, 168) | don't open it; it's a Snom eating the oath | **Snom** (Ice Scales) |
| 4 | A Deed for the Skald (Isenmar) | Ebbmouth (160, 168) | beat the bully, out-fish Gudrun, or lie | Mystic Water; Marisol +1 |
| 4 | The Rehearsal (Elowen) | the Rehearsal (568) | a Ditto replaying a crash it saw once | **Ditto** (Imposter) |
| 4 | The Lattice Hums Wrong (Zenith) | Ebbmouth mill-wheels (160, 167) | who gets the recordings | Meridian +1 / Marisol +1 / Larch |
| 4 | The Egg Thief of Gullcry (Isenmar) | Gullcry Cliffs (561) | it's a Bombirdier delivering eggs to the wrong nests | **Bombirdier** (boss) or let it work |

**Fighting before the Normal Gym 1** (SWAP_GYM1_GYM2 §8): Timburr (Ferrow's, Ch1) and the Crabrawler/Clobbopus duel
(Lacecliff Walk, Ch2), both before Saltmere. Eevee "Understudy" now comes with Badge 1, and the Saltmere Eevee breeder
and Abra magician rows in POKEMON_AVAILABILITY moved to after Badge 1.

**Sister-game cameos** stay where `CAMEOS.md` puts them, but each now has a board entry so players can find it: Shelly
(Elowen, Deepwood, after Gym 2 since Rev 14), Venam and Garret (Nadir), Alexandra (Isenmar), Shiv (Antumbra board,
Gloaming), Lin (Crownhaven, postgame). The cameo event calls `pf_quest_complete(:ID)` after its fight.

---

## 4. Implementation (`plugins/Prismfall Trials`, requires Prismfall Core)

| File | What |
|---|---|
| `001_Trials_Config.rb` | the eight Trials (names, halls by map ID, rank names, board flavour), rank thresholds and rank rewards, switches |
| `002_Trials_State.rb` | `Prismfall.state.trials` (quests, points, rank rewards paid, event Pokémon, chases, deeds, tiers seen, rumours) |
| `003_Trials_Registry.rb` | `Prismfall::Trials.quest(:ID, {...})` and `Prismfall::EventMons.register(:ID, {...})` |
| `004_Trials_Script.rb` | the scene interpreter (lines, choices, conditions, battles, gifts, steps, rewards) |
| `005_Trials_Quests.rb` | lifecycle, rewards, points/ranks, chases, quiet deeds, battle helpers, condition functions, `pf_quest_*` |
| `006_Trials_EventMons.rb` | event Pokémon: wild battles, gifts, eggs, boss battles (via Prismfall Bosses) that join |
| `007_Trials_BadgeTiers.rb` | badge-tier encounter overlays + rumours + the "rustling" notice |
| `008_Trials_Board.rb` | boards (`pf_trial_board`) and keepers (`pf_trial_keeper`) |
| `009_Trials_QuestLog.rb` | the **Quests** pause-menu scene |
| `010_Trials_PageConditions.rb` | `Condition:` comments on event pages (alias-chained `Game_Event#refresh`) |
| `011_Trials_Debug.rb` | Debug > Prismfall Trials... |
| `110–112_Quests_*.rb` | wired quests (Elowen; Isenmar; Zenith + Ashkaar outposts) |
| `120_Quests_Catalogue.rb` | designed quests (`:stub`, hidden from boards until wired) |
| `130/131_EventMons_*.rb` | event Pokémon (implemented / designed) |
| `140_BadgeTier_Rumours.rb` | the hint lines |
| `150_Trials_Talk.rb` | `pf_trial_talk(:KEY)`: one call per map event; the plugin decides which scene runs |

**Adding a quest.** Register it in a `1xx` file with `:scenes`, add its NPCs to `TALK`, list its events in
`TRIAL_EVENTS.yaml`, run `ruby tools/trials_docs.rb` and the harness test. The test checks every scene command, condition,
step, trainer, item, event Pokémon (species, form, ability, legal moves), `TALK` row and event spec.

**Engine hooks** (all alias-chained): `PokemonEncounters#setup` and `#choose_wild_pokemon_for_map` (overlays),
`Game_Event#refresh` (page conditions). Handlers: `:prismfall_badge_awarded` (rumours, table refresh), `:on_enter_map`,
`:on_frame_update` (notice), `:on_wild_battle_end` (Gudrun's fishing count). New PBS: `pbs/encounters_badgetiers.txt`
and `pbs/trainers_trials.txt` (versions 50–99 reserved for Trial trainers); `tools/package.sh` ships both unchanged.
