# Proposal: Memorable Side-Cast, Elevated NPCs & 14 Recurring Rivals (Codex & Repeatable Cast Expansion)

- **Date:** 2026-11-22
- **Author:** Gemini (Side-Cast & Recurring Rivals Design)
- **Target Scope:** `story/03_CAST.md`, `dist_web/codex.html` (`tools/build_codex.py`), `plugins/Prismfall Core/` (In-Game Character Codex / Cast Roll), `plugins/Prismfall Cutscenes/014_Portraits.rb` (`Prismfall::Portrait::CAST`), `pbs/trainer_types.txt`, `pbs/trainers_trials.txt`, and `design/AUDIO_SOUNDTRACK_PLAN.md`.
- **Design Goal:** Address the creator's feedback that Velmora currently feels dominated by the "Three Powers" (Accord / Meridian / Hollow) and the 18 Wardens, whereas *Pokémon Reborn* and *Pokémon Rejuvenation* stay unforgettable because of their vibrant ecosystem of recurring weirdos, chaotic local icons, multi-act rivals, comic-relief duos, and eccentric regulars (Rorim B., Novae, Sandy, DJ Arclight, Cain, Victoria, Bennett, Laura, Crescent, Amber, Ren). Every character below is **100% original to Prismfall**, obeys `design/CHARACTER_DESIGN_STUDY.md` §6 (distinct silhouettes, unused two-colour palettes, bold props, personality poses), follows `story/15_COMEDY.md` (character-driven humor that never undercuts dark beats), and is **wired into both the Web Story Codex and an In-Game Repeatable Character Codex**.

---

## Executive Summary & Architecture Overview

1. **Part 1 — Audit & Elevation of 12 Existing Minor NPCs / Ensembles:** Prismfall's Trials plugins (`110–120_Quests_*.rb`) and Ch0–13 scripts already hide absolute gems (**Pip Ore, Coll Hale, Bersi Gullsong, Six-Fingers Ottoline, Grant Kiosk P-3NNY, Sister Hollin & Brother Teasel, Sergeant Brakka & Legate Kosk, the 8 Eevee Octave Choristers, Postmaster Halloran, Recruit Tamm, Ottilie & Nell, and the unbattled Codex regulars like Hesper/Edda/Calla/Renata/Fenwright/Saffi/Nasrin**). Instead of clashing with them, we elevate them with bespoke portraits, optional/repeatable battles or hangouts, and full Codex cards.
2. **Part 2 — 14 Unforgettable New Recurring Side Characters & Rivals:** Spanning every kingdom in Velmora (**Elowen, Isenmar, Zenith, Nadir, Ossaria, Ashkaar, Antumbra, Crownhaven**) across **Acts I–V, Postgame, and the Ruin Route** — all 14 verified **zero name collisions** against `pbs/trainers.txt`, `story/03_CAST.md`, and `plugins/Prismfall Trials/`, with **zero duplicated two-colour palettes** against `design/CHARACTER_ART.md` §8.
3. **Part 3 — Dual Codex & Repeatable Rematch System:**
   - **Web Codex (`dist_web/codex.html`):** Adds a `"Recurring Side Cast & Repeatable Rivals"` section to `story/03_CAST.md` (and updates `"Important Side Characters"`).
   - **In-Game Character Codex (`Prismfall::Codex` / Ledger "Cast Roll" Tab):** Tracks `met`, 3-tier progressive bios, live **Repeatable Rematch / Hangout Location**, and **Side-Cast Affinity (`0–5 ★`)** stored separately from Core's 10 ending-critical `BONDS` (`012_Narrative_Data.rb`) so existing ending math (`DERIVED_FLAGS`, `WARDEN_CONSENT`) remains 100% untouched.
4. **Part 4 — Production-Ready Integration Tables:** Copy-paste-ready `pbs/trainer_types.txt` definitions, `Prismfall::Portrait::CAST` additions, pure-instrumental `Audio/BGM/` + `Voice - *.ogg` slots (matching v4.3 Audio Spec), and a Chapter-by-Chapter Distribution Map.

---

# Part 1: Audit of Existing Minor NPCs Worth Elevating to Recurring Codex Cast

A full sweep of `story/03_CAST.md`, `story/13_CUTSCENES.md`, `story/15_COMEDY.md`, `story/20–32_SCRIPT_*.md`, `plugins/Prismfall Cutscenes/014_Portraits.rb`, and `plugins/Prismfall Trials/110–120_Quests_*.rb` reveals **12 standout minor NPCs/ensembles** already loved in dialogue that currently lack portraits, battles, repeatable hangouts, or Codex cards.

> **Continuity Note on the Ossaria Bone-Carters:** Because the Bone-Carters (`13_CUTSCENES.md` WAR-1, `14_WAR_AND_BLESSING.md`, map `930`) currently have only an unnamed "Elder," we elevate the entire guild by giving them a full flagship recurring character in **Part 2 (#8: Zainab Darzi, Bone Chronicler)** rather than duplicating them here.

### 1.1 Elevation Matrix (12 Hidden Gems Already Seeded in Prismfall)

| # | Existing NPC / Group | Current Canon Footprint | Current Status | Elevation Plan (Portrait · Battle/Hangout · Codex Card) |
|---|---|---|---|---|
| **E1** | **Pip Ore** (14, Bastian's granddaughter & lamp-runner) | Ch14 Cragholm (`360/363`), Ring-Day (`OS_RING_DAY`), Ch20–21 (`15_COMEDY` gag #5). Referenced earlier via "Pip's friend" in Ironreach (`NA_LAMPLIGHTER_KIDS`, `260`). | In `Portrait::CAST` (`:PIP`); **no trainer type, no battle, no Ch9 appearance**. | **Seed her earlier in Ch9 Ironreach (`260`)** leading the lamp-runner search! Add `[SIDE_LAMPRUNNER] -> Lamp-Runner`, fast Rock/Electric/Ground doubles spar on `:CRYSTAL_CAVERN` / `:DARK_CRYSTAL` (Ace: **Glimmora** / **Boltund** / **Carbink**). Repeatable **"Tunnel Relay"** in Cragholm Lift Galleries (`363`) rewarding **Gems, Escape Ropes, Light Clay, and Hard Stone / Star Pieces**. Codex unlocks in Ch9/Ch14; tracks Bastian's "selective deafness" biscuit-tin tally. |
| **E2** | **Coll Hale** (Juno's deadpan farmer father) | Ch0–2 Ferrow's Landing (`100`) & Hale Farmhouse (`523`), `EL_SCARECROW` ("I didn't build a scarecrow"), reads Gale Post upside down (`20_SCRIPT_CH0-2.md`). | Explicitly **excluded** from `Portrait::CAST` (`13_CUTSCENES.md:24`), while his wife `:WENNA` IS in `CAST`! | Add `:COLL` to `Portrait::CAST` (broad-shouldered, straw hat jammed low, permanently deadpan mug). Add optional **"Orchard Spar"** (`[SIDE_FARMHAND] -> Berry Farmer`) after Badge 2 using **Sudowoodo**, **Gogoat ("Parsnip")**, and **Miltank** on `:MEADOW`. Repeatable hangout at Hale Farmhouse (`523`) where Coll slips you **EV-reducing Berries & Bramble Tarts** (full HP/status cure) and dryly comments on Juno's latest Warden headlines. |
| **E3** | **Bersi Gullsong** (Ebbmouth Skald & Tally Keeper) | Ch4 Ebbmouth Net Loft (`160/168`: `IS_OATH_PARCEL`, `IS_SKALDS_SAGA`, `IS_OCTAVE_DROWNED_NOTE`) → Ch19/20 Skaldfast (`921`: `IS_SAGA_OF_THE_ICE`, where he finally sings straight without lying). | Plain-text Trial speaker only (`:BERSI`). **No portrait, no battle, no Codex entry.** | Add `:BERSI` to `Portrait::CAST` (braided ginger beard with bone beads, cracked horn-lute). Add `[TRIAL_SKALD] -> Saga Skald` optional **"Saga Spar"** on `:WATER_SURFACE` / `:FROZEN_LAKE` (Ace: **Toxtricity**? No—**Lapras**, **Exploud**, **Perrserker**, **Eiscue**). Repeatable **"Tall-Tale Recital"** at Net Loft (`168`) / Skaldfast (`921`): after every major boss, Bersi sings an absurdly exaggerated verse recorded in his **Codex Saga Log**! |
| **E4** | **Six-Fingers Ottoline** (Nadir Gutter Book Fixer) | Runs 6+ Nadir quests across Mirefen (`220`), Ironreach (`260`), Underveil (`423`), incl. `NA_OCTAVE_LAMPS_OUT`, `NA_MOON_MARKET_DOGS`, `NA_MEMORY_KATA`, Venam & Garret pointers. Iconic line: *"It's yours. Don't make it mine."* | Plain-text Trial speaker only (`:OTTOLINE`). **No portrait, no battle, no Codex entry.** | Add `:OTTOLINE` to `Portrait::CAST` (chalk-dusted trench coat, six nimble fingers tapping a pawn ledger, lopsided gold-tooth smirk). Add `[TRIAL_FIXER] -> Sump Fixer` battle on `:NEW_MOON` / `:CORROSIVE_MIRE` (Ace: **Honchkrow**, **Drapion**, **Weavile**, **Grimmsnarl**). Repeatable **"House Cut Wager"** at The Last Rung (`260`) / Moon Market (`423`): wager ₽5,000 to win rare **Pawn-Shelf Held Items** (Focus Sash, Choice Items, Black Sludge, Flame/Toxic Orbs). |
| **E5** | **Grant Kiosk P-3NNY** (Sentient Meridian Ticket-Rotom) | Ferrow's Customs (`108`), Saltmere Harbour (`143`), Ebbmouth Lattice (`160`), Lumen (`180/194`): `ZE_FORM_7B`, `ZE_FIELD_SURVEY`, `ZE_LATTICE_HUM`, `ZE_OCTAVE_OFF_BEAT`. Beloved deadpan ALL-CAPS comedy (*"I HAVE BEEN PROGRAMMED WITH ONE (1) JOKE."*). | Plain-text only (`:PENNY`). **No portrait, no battle, no Codex entry.** | Add `:PENNY` to `Portrait::CAST` (glowing brass-framed CRT monitor showing minimalist pixel emoticons `[ ^_^ ]`, `[ ! _ ! ]`, `[ -_- ]`!). Unlock secret **"DIAGNOSTIC STRESS-TEST #9999"** battle (`[SIDE_KIOSK] -> Grant Kiosk`) in Lumen Prize Exchange (`194`) after Badge 4: P-3NNY pilots a full **Appliance-Rotom** squad (Heat/Wash/Frost/Fan/Mow) + **Porygon2** on `:NEON_GRID`! Repeatable for **Cell Batteries, Upgrades, Exp Candy M/L**. |
| **E6** | **Sister Hollin, Brother Teasel & Mother Aldreth** (The Quiet Way Keepers) | Ferrow's (`100`), Saltmere (`140`), Briarwick (`120/126`): 10+ wired Elowen quests (`EL_FIRST_LESSON`, `EL_LANTERNS`, `EL_SOUND_OF_SALTMERE`, `EL_THREE_KNOTS`, `EL_MATRIARCH_HUM`). | Plain-text only. **No portraits, no battles, no Codex entries.** | Add `:TEASEL`, `:HOLLIN`, `:ALDRETH` to `Portrait::CAST` (Hollin's portrait holds up her ALL-CAPS chalk slate!). Add optional repeatable **"Silent Koan Spar"** (`[TRIAL_MONK] -> Quiet Way Keeper`) with Sister Hollin at Saltmere Lantern House (`148`) on `:MEADOW` / `:FLOWER_GARDEN` (Ace: **Gallade** / **Komala** / **Chimecho** / **Shiinotic** — Soundproof & Calm Mind gimmick; using loud Sound moves makes Hollin hold up `"TOO LOUD"`!). Codex tracks your realm-wide **Quiet Deeds** count. |
| **E7** | **Sergeant Brakka Emberhide & Legate Varra Kosk** (Ashkaar Crucible Officers) | Saltmere Barge (`146`: `AS_LITTLE_CRUCIBLE`), Cindervault Crucible (`240`: `AS_OCTAVE_TOO_LOUD`, `AS_SEVEN_BOUTS`, `AS_BRAZIER_WRIT`), Wyrmrest (`460`: `AS_DRAGONSWORN`). `REVIEW.md` notes Kosk needs extra pre-Festival visibility. | Use generic `ASHKAAR_OFFICER`; plain-text dialogue. **No portraits, no Codex entries.** | Add `:BRAKKA` and `:KOSK` to `Portrait::CAST` + bespoke `[TRIAL_LEGATE] -> Crucible Legate` for Kosk (and `[TRIAL_SERGEANT] -> Legion Sergeant` for Brakka). Give Kosk a non-optional Act IV camp beat (`924`) so players recognize her before Act V! Make the **Crucible Oath-Rule Gauntlet** repeatable at Cindervault (`240`) — strict "No Switching" or "No Healing" streaks paying **Charcoal, Flame Orb, Life Orb, Bottle Caps, and Exp Candy L/XL**. |
| **E8** | **The Eight Eevee Octave Choristers (`Lyra, Aria, Cadence, Sona, Noct, Forte, Lento, Carol`) + Vesper Lindqvist** | `design/EEVEE_OCTAVE.md` & `113_Quests_Octave.rb` — one singer per kingdom, culminating in Ch20 Crownhaven 9-bout Z-Move gauntlet (`489`). | Only `:VESPER` is in `Portrait::CAST`. All 8 choristers share generic `[OCTAVE_SINGER]` and have **no portraits or Codex entries**, and cannot be rematched individually! | Add `:LYRA, :ARIA, :CADENCE, :SONA, :NOCT, :FORTE, :LENTO, :CAROL` to `Portrait::CAST` (each wearing their distinct kingdom-modified Choir robe: Cadence's cut-down drum vest, Forte's scorched sleeve, Noct's soot-black lamplighter cloak, Lento's mirrored trim!). Add an **"Octave Ensemble" Codex Page** that fills in each chorister's card & Z-Move field as you help them, AND enable **repeatable individual or Tag-Duet rematches** in Crownhaven Memorial Garden (`489`) post-gauntlet (great for testing all 8 Eeveelution fields & farming **Type Gems / PP Ups / Evolutionary Stones**!). |
| **E9** | **Postmaster Halloran** (Skyreach Gale Post Chief) | Skyreach Gale Post Hall (`325`: `ZE_RETURN_TO_SENDER`). Dry comedic foil to Odessa Gale (*"Knock twice. Nobody in Skyreach answers one knock."*). | Plain-text only (`:POSTMASTER`). | Add `:HALLORAN` to `Portrait::CAST` (visor cap, ink-stained mustache, brass franking stamp). Link him directly with new side-character **#6 Willa Quigley** (below). Repeatable **"Dead-Letter Express"** courier deliveries unlocked post-Ch12 paying **Rare Balls (Fast/Level/Moon/Heavy) & Heart Scales**. |
| **E10** | **Recruit Tamm** (The Heights-Terrified Ashkaar Dragon-Rider) | Cindervault Dragon Roosts (`248`: `AS_AFRAID_OF_HEIGHTS`, `15_COMEDY.md` §5) — assigned a Trapinch for two years because he's scared of heights. | Designed stub only (`:stub`), one-off gag. | **Elevate to 3-Act Recurring Comic Ally (`:TAMM`, `[SIDE_RECRUIT] -> Grounded Rider`)!** Ch8 Cindervault (`248`: Trapinch → Vibrava hovers 3 feet high!), Ch14 Glasswake/Duneholt (`670`/`200`: proudly riding a newly evolved **Flygon** *four* feet off the ground, refuses to go higher, optional Ground/Dragon spar on `:DESERT`), Ch19 War Camp (`924`: rescues wounded scouts by skimming low under enemy radar because he still won't fly above rooftops!). Repeatable spar at Dragon Roosts (`248`) rewarding **Dragon Fang / Soft Sand / Exp Candy M**. |
| **E11** | **Ottilie (Saltmere Stagehand) & Nell (Ironreach Chalk-Girl)** | Ottilie (`EL_LANTERNS`, `145`): stage-fright understudy practicing lines to a stolen lantern. Nell (`27_SCRIPT_CH9.md`, `263/264`): stands on a crate running Kaito's Open bracket (`KESTREL VANE (TEAM COMPOST)`), shielded by Juno during the Shatter. | Plain-text one-chapter NPCs. | **Give Velmora's "ordinary kids" a multi-act payoff!** Ottilie (`:OTTILIE`) reappears in Ch20 Crownhaven (`483`) overcoming stage fright to play **young Princess Maren** in Dorian's *Gilded King* (if you left her the lantern in `EL_LANTERNS`, she still keeps it on the footlights!). Nell (`:NELL`) reappears in Ch17 Underveil helping evacuate Ironreach kids and runs the **Postgame Concordance Spire (`493`)** registration counter with her crate! Both get warm non-combat Codex entries (with Ottilie granting **Encore/Substitute TM or Silk Scarf** and Nell tracking Spire win streaks). |
| **E12** | **Existing Supporting Cast Missing Codex / Repeatable Hooks** | **Hesper Vane** (`:HESPER`), **Captain Edda Morrow** (`:EDDA`), **Calla Wren** (`:CALLA`), **Councillor Renata Sallow** (`:RENATA`), **Mother Gutter** (`:GUTTER`), **Curator-Elect Nasrin Vael**, **Lector Saffi Ivarne**, **Clerk-Superior Amadeus Fenwright**. | Already in `CAST` (first 5) or Trial Keepers (last 3), but **zero battles** and no repeatable Codex loop. | Give all 8 full **Codex Dossier Cards**! Furthermore, add **3 unforgettable optional battles** among them: **(a) Mother Gutter** (`[NADIR_BARON] -> Sump Baron`, Ch17 `423` / Post-Ch18 friendly rematch — her cart-sized **Muk** + **Alolan Muk** + **Swalot** + **Pecharunt-survivor Garbodor** on `:CORROSIVE_MIRE`!); **(b) Lector Saffi Ivarne & Her Reflection** (`[TRIAL_LECTOR] -> Speculum Lector`, Ch13/15 `346` — a hilarious double battle where Saffi and her own reflection argue mid-fight on `:INVERSE`!); **(c) Clerk-Superior Fenwright** (`[ACCORD_CLERK] -> Clerk-Superior`, Ch20 `496` — surprisingly ruthless stall/trick-room bureaucrat team with **Audino, Klefki, Bronzong, Indeedee** when testing you for `CR_ACCORD_CHAMPIONS`!). |

---

# Part 2: 14 Unforgettable New Recurring Side Characters & Rivals

Every character below includes a **production-ready spec card** covering:
1. **Trainer Type ID & Bespoke Class** (for `pbs/trainer_types.txt`)
2. **Visual Design Sheet** (following `CHARACTER_DESIGN_STUDY.md` §6 — specific concept, 1× silhouette, unused two-colour palette, bold prop, pose, asymmetric face, ready for Gemini sprite/portrait sheets)
3. **Personality, Catchphrases & Banter Pairings** (bouncing directly off Prismfall's main cast)
4. **Multi-Act Encounter & Battle Arc** (exact Chapters, canonical Map IDs from `design/WORLD.md`, Ace Pokémon, Field specialty, and **Repeatable Rematch Location & Rewards**)
5. **Codex Entry** (unlock condition, 3 progressive bio beats, Affinity perks, `Prismfall::Portrait::CAST` key, and `Audio` BGM + Voice Blip tag)

---

## 1. Clement "DJ Chroma" Okafor — *"Chroma-C."* (The "Rorim B." Soul-Sibling)

- **Archetype:** Larger-than-life Pirate Gale-Radio Host & Disco-Prism Showstopper
- **Trainer Type ID & Bespoke Class:** `[SIDE_GROOVE]` → **`Groove Monarch`** *(Name in battle: `Groove Monarch Chroma`)*
- **Home Region / Span:** Zenith / Nadir / Realm-Wide Pirate Broadcasts (Acts I–V + Postgame)

### Visual Design Sheet
- **Core Concept:** *An outlawed disco-prism pirate DJ who rigs stolen Lattice amplifiers into a chest-mounted turntable backpack to blast illegal funk music into quarantined towns and Nadir's dark alleys.*
- **Unused Colour Pair:** **Electric Magenta (`#E0218A`) + Warm Ivory (`#FAF3E0`)**, accent **Prism Gold (`#FFD15C`)** (hair beads shift colour to mirror the active Field Effect!).
- **1× Silhouette:** Enormous spherical halo of towering curls framing flared retro bell-bottom trousers, broken diagonally by two brass telescoping broadcast antennas jutting from his backpack.
- **Iconic Prop:** A brass-and-glass **portable prism-turntable rig** strapped across his torso like an accordion, complete with glowing spinning vinyl discs and a handheld silver mic-wand.
- **Pose & Face:** Mid-slide disco lunge leaning 30° back on his heels, left hand balancing a Poké Ball spinning like a 45-RPM record on one fingertip, right hand pointing skyward; star-shaped rose-tinted shades slid down his nose so one radiant winking eye and a massive open-mouthed laugh shine over the frames.

### Personality, Catchphrases & Banter Pairings
- **Personality:** Unstoppable, infectious, hilariously melodramatic groove philosopher who treats every gloomy road as a dancefloor waiting to happen. Underneath the 110% volume and funky slang, **he is a grieving older brother**: in AF 290 he was a teen percussionist in Lower Crownhaven's Prism Choir whose little sister **Mina** was Fixed in the Glassfall Scar. Because silence reminds him of that night, he swore Velmora would never go quiet again — running **"Radio Free Prism (18.0 FM)"** to smuggle missing-persons bulletins, warm food drops, and banned music across Mandate curfews.
- **Catchphrases:**
  - *"DROP THE NEEDLE, BABY! 18.0 FM IS LIVE ON YOUR FOREHEAD!"*
  - *"Eighteen Plates, eighteen genres — and honey, you're playing ALL of 'em in stereo!"*
  - *(Rare quiet Act IV line in Lower Crownhaven):* *"People think funk is just noise, kiddo. Nah. Funk is proof your heart's still beating."*
- **Banter Pairings:**
  - **Dorian Pell:** Theatrical bromance-rivalry — Dorian insists Chroma has *"appalling diction and magnificent lighting."*
  - **Rook Calder:** Chroma is Rook's idol-turned-rival; Rook's chat loses its mind whenever Chroma hijacks Rook's livestream frequency (`"Chat, who let the disco guy onto my frequency?! ...Wait, don't subscribe to him!"`).
  - **Kestrel Vane:** Chroma calls Kestrel *"Little Cloud-Coat"* and relentlessly tries to make him clap on the two-and-four; Kestrel's eye visibly twitches.
  - **Professor Larch:** When Kroll bombs the Skyreach relay in Ch12, Chroma's illegal Nadir boosters catch the broken signal and **re-broadcast the Larch Papers straight into the Sump** — Larch begrudgingly calls him *"an acoustic felony with decent ethics."*

### Multi-Act Encounter & Battle Arc
- **Act I — Ch2 (Saltmere Promenade, `140`):** Crashes the promenade with a portable speaker stack right after Gym 1; challenges you to a joyous **Double Battle** on `:GRAND_STAGE` to "test the acoustics of your Footlight Badge." (Lv 15–16: **Lombre**, **Oricorio-Baile**).
- **Act I — Ch5 (Lumen City Concourse / Lowlight Steps, `180/181`):** Hijacks Meridian's "Tenth Year of Light" billboard to play funk over Voss's promotional loop! Optional Double Battle on `:NEON_GRID` (Lv 25–26: **Lombre**, **Oricorio-Pom-Pom**, **Loudred**). After the Shatter, he quietly turns his speakers off and leaves a glowing disco-prism lamp at Dex's shrine.
- **Act III — Ch12 (Skyreach Lower Gantries, `323`):** Appears mid-Mandate raid with a stolen Gale Post relay dish — teams up with you or holds a back-alley transmitter so Larch's broadcast punches through the bombing! Optional fight on `:STORMFRONT` → `:RAINBOW` (Lv 53–55: **Ludicolo**, **Oricorio-Pom-Pom**, **Exploud**, **Quaxwell→Quaquaval**).
- **Act IV — Ch17 (Underveil Moon Market, `423`):** Broadcasting emergency medical frequencies during the Sump Purge; grimly focused, then throws a defiant roof-top morale dance battle on `:NEW_MOON` (Lv 73–75: **Ludicolo**, **Oricorio-Sensu**, **Exploud**, **Quaquaval**, **Volcarona? No → Bellossom** [Chlorophyll/Quiver Dance] / **Porygon? No → Toxtricity-Amped**).
- **Act V — Ch20 (Crownhaven Market Ring, `496`):** Hosts the **Festival Eve Street Block-Party** — reveals Mina's statue in Lower Crownhaven (`888`) in a tender optional talk; full 6-mon Double Showstopper on `:GRAND_STAGE` (Lv 87–89).
- **Ace Pokémon:** **Ludicolo ("Mirrorball")** (Rain Dance / Teeter Dance / Giga Drain / Hydro Pump — pure Rorim B. homage!) paired with **Quaquaval ("Showtime")** (Aqua Step + Moxie + Dancer chains with **Oricorio**!).
- **Field Specialty:** `:GRAND_STAGE` (forces Standing Ovation by Turn 2 with Dances & Sound moves!), `:NEON_GRID`, `:RAINBOW`.
- **Repeatable Rematch Location & Rewards:** **Saltmere Promenade Bandstand (`140`)** (Acts I–III) and **Underveil Pirate Studio (`423`) / Crownhaven Market Ring (`496`)** (Acts IV–Postgame). *"Funk-Off Double Battle"* scaling to current cap — awards **Synthetic Seeds, Magical Seeds, Heart Scales, Big Nuggets, and unlockable Custom Battle BGM Vinyls** (lets players swap wild/trainer battle music!).

### Codex Entry
- **Unlock Flag:** `codex_met(:CHROMA)` (Ch2 Saltmere encounter)
- **Progressive Bio Beats:**
  1. *Beat 1 (Ch2):* Outlawed Gale-Radio DJ broadcasting "18.0 FM" from a chest-mounted turntable. Claims the Accord banned disco "out of cowardice."
  2. *Beat 2 (Ch12):* Kept Larch's suppressed broadcast alive across Nadir after the Skyreach bombing using salvaged Lattice relays.
  3. *Beat 3 (Ch20):* Former Prism Choir percussionist whose sister Mina was Fixed in AF 290. Plays loud enough to wake the whole region.
- **Affinity Perks (0–5 ★):** ★2 unlocks **Battle BGM Jukebox** in Pause Menu; ★4 grants **Throat Spray + Choice Scarf**; ★5 unlocks his postgame Lv 95 **"18-Genre Encore"** tag rematch with Rook Calder!
- **`Portrait::CAST` & Audio:** `:CHROMA` (full 10-expression sheet) | `BattleBGM = Battle - Groove Monarch` (funky brass-synth disco battle theme — pure instrumental, zero vocals, e.g., Miror B. / *Persona 5* Acid Jazz energy) | `Voice - Chroma.ogg` (warm, bouncy low-baritone bass-pluck blip).

---

## 2. Kallista "Kal" Drayton — *"The Field-Breaker"* (The "Novae" Bounty / Gauntlet Rival)

- **Archetype:** Sharp, Relentless Field-Hunter & Wandering Tactical Duelist (6-Chapter Escalating Rival)
- **Trainer Type ID & Bespoke Class:** `[SIDE_HUNTER]` → **`Field Hunter`** *(Name in battle: `Field Hunter Kal`)*
- **Home Region / Span:** Ossaria / Greyfen (erased Quiet Town) — tracks PC across **6 Chapters** (Ch2, Ch4, Ch6, Ch10, Ch14, Ch18) + Postgame Gauntlets!

### Visual Design Sheet
- **Core Concept:** *An obsessive wandering field-tactician who treats Velmora's 35 battlefields like a live chessboard, collecting brass colour-tags for every environment she breaks.*
- **Unused Colour Pair:** **Storm Petrol-Teal (`#1A6B72`) + Burnt Ochre (`#C86D2D`)**, accent **Antiqued Brass (`#D4AF37`)**.
- **1× Silhouette:** Razor-sharp asymmetric highwayman poncho cut shorter on the throwing arm, long jagged silver-streaked raven ponytail sweeping horizontally to the right like a blade.
- **Iconic Prop:** A mechanical **brass astrolabe-compass gauntlet** (strictly non-Meridian clockwork — she scoffs at Lattice tech!) set with spinning coloured glass filters, plus 18 clinking field-tags braided onto her belt sash.
- **Pose & Face:** Crouched forward in a predator's low lunge, right hand tracing a glowing tactical diagram in the dust with a brass stylus while her left hand flicks a Dusk Ball upward; narrow amber eyes, one eyebrow cocked high, biting the end of her field-pencil with a sharp side-smirk.

### Personality, Catchphrases & Banter Pairings
- **Personality:** Pure *Pokémon Rejuvenation* **Novae** energy — sharp, ruthless in battle, allergic to small talk, deeply respectful of genuine tactical skill, and secretly terrified of losing anyone else to the Bleed. She refuses to let the PC win by brute-forcing type charts: every time you meet her, her team is engineered specifically to **transform the current Field Effect mid-battle** (`Silkwood → Wildfire`, `Desert → Glass Dunes`, `Crystal Cavern → Dark Crystal`, `Fairy Tale → Dragon's Den`) to punish complacent players! Secret backstory: her hometown **Greyfen** was quietly erased from Accord maps as a Quiet Town in AF 291; she believes the only person who can survive Crownhaven is someone who masters the land itself.
- **Catchphrases:**
  - *"Your badge case hums. Let's see if you actually read the ground you're standing on."*
  - *"Cute setup. Shame the floor's about to catch fire."*
  - *(Ch18, after 6th duel):* *"Six fields. Six wins. Fine. You're not going to die in Crownhaven. ...Don't make me a liar."*
- **Banter Pairings:**
  - **Sahar Ostrand:** Kal trades desert field telemetry for Sahar's ancient terrain maps — Sahar calls her *"the only student who listens to sand faster than she talks."*
  - **Kestrel Vane:** Fierce tactical tension — Kal mocks his Meridian Gauntlet in Ch12 (`"Borrowing a machine to bend a field? Amateur."`), which actually stings Kestrel's pride before K8!
  - **Ilsa Marr:** Ilsa hates being near Kal because Kal's thoughts are *"loud, geometric, and entirely composed of damage calculations."*

### Multi-Act Encounter & Battle Arc (6 Escalating Optional Battles!)
1. **Act I — Ch2 (Marram Down, `528`):** Spots your NULL-immune tracks; tests you on `:BEACH` (forces Rain/Surf → `:WATER_SURFACE`! Lv 15: **Larvesta**, **Wingull**, **Buizel**).
2. **Act I — Ch4 (The Rimewood / Gossamer Edge, `562`):** Tests field-burning! `:SILKWOOD` → `:WILDFIRE` (Lv 22: **Larvesta**, **Fletchinder**, **Mienfoo**, **Chinchou**).
3. **Act II — Ch6 (The Brass Dunes, `600`):** Tests weather/terrain pivots! `:DESERT` → Superbloom or `:GLASS_DUNES` preview (Lv 30: **Larvesta**, **Vibrava**, **Pelipper**, **Kilowattrel**).
4. **Act III — Ch10 (Prism Falls, `681`):** First fight after Larvesta evolves! `:RAINBOW` weather-burst showcase (Lv 46: **Volcarona**, **Flygon**, **Kilowattrel**, **Gliscor**, **Malamar**).
5. **Act IV — Ch14 (Geode Hollow, `764`):** Triggers `:CRYSTAL_CAVERN` → `:DARK_CRYSTAL` with Dark Pulse + Sandstorm, then reverses it with Signal Beam/Dazzling Gleam! (Lv 62: **Volcarona**, **Flygon**, **Malamar**, **Gliscor**, **Weavile**, **Hawlucha**).
6. **Act V — Ch18 (Gloamwood Verge, `841`):** Final pre-Festival exam! `:FAIRY_TALE` → `:DRAGONS_DEN` via triple Dragon strikes + full team synergy (Lv 79: **Volcarona**, **Flygon**, **Kingambit**, **Malamar**, **Gliscor**, **Hawlucha** — holds **Firium Z** or **Mega Gallade/Houndoom**? Let's give her **Firium Z** on Volcarona or **Mega Lucario? No, Kaito/Garret → Mega Aerodactyl? Bastian → Mega Pinsir? → Mega Mawile / Mega Gyarados? → Mega Garchomp!** Actually **Z-Move Firium Z on Volcarona** fits her anti-Meridian lone-wolf aesthetic!).
- **Ace Pokémon:** **Volcarona ("Catalyst")** (raised from Lv 15 **Larvesta** across 6 chapters — ignites Silkwood, melts Frozen Lake, anneals Glass Dunes, lights Dark Crystal!).
- **Field Specialty:** **Master of Field Transitions** (deliberately triggers transform strikes for the ×1.3 bonus!).
- **Repeatable Rematch Location & Rewards:** **Duneholt Caravanserai (`200`)** (Act II–III) and **Crownhaven Concordance Spire Lobby (`493`)** (Act V–Postgame) — **"Kal's 6-Tier Field Gauntlets"** (pick Elemental, Telluric, Synthetic, Magical, War-Glass, or Inverse 3-battle mini-gauntlets, no healing between bouts, scalable to current cap!). Rewards: **All 4 Field Seeds (Elemental/Telluric/Synthetic/Magical), Ability Capsules, Bottle Caps, Terrain Extender, and Exp Candy L/XL**.

### Codex Entry
- **Unlock Flag:** `codex_met(:KAL)` (Ch2 Marram Down encounter)
- **Progressive Bio Beats:**
  1. *Beat 1 (Ch2):* Wandering bounty-duelist collecting brass tags for every Prismfall battlefield. Obsessed with testing the Unimprinted challenger.
  2. *Beat 2 (Ch10):* Refuses Meridian tech; maps how Imprint fields transform under combat pressure.
  3. *Beat 3 (Ch18):* Sole survivor of Greyfen, an erased Quiet Town. Trained you across six chapters so you would outlive Crownhaven's trap.
- **Affinity Perks (0–5 ★):** ★2 unlocks **Field Transition Cheat-Sheet** pin in Field Notes (highlights every field's exit moves!); ★4 grants **1× of every Field Seed + Heavy-Duty Boots**; ★5 unlocks **"Kal's Apex Inverse Gauntlet"** (Lv 98 Postgame rematch).
- **`Portrait::CAST` & Audio:** `:KAL` (full 10-expression sheet) | `BattleBGM = Battle - Field Hunter` (razor-sharp high-BPM tactical rock/strings, Novae/Rejuv rival energy) | `Voice - Kal.ogg` (crisp, dry alto click-blip).

---

## 3. Mags Doyle — *"Scrap-Queen Mags"* (The "Sandy" Chaotic Ally / Local Icon)

- **Archetype:** Street-Smart Lowlight / Nadir Force of Nature, Stray-Pokémon Wrangler & Unexpected Clutch Savior
- **Trainer Type ID & Bespoke Class:** `[SIDE_WILDCARD]` → **`Sump Wildcard`** *(Name in battle: `Sump Wildcard Mags`)*
- **Home Region / Span:** Lumen Lowlight (`181`) ↔ Mirefen (`220`) ↔ Underveil (`424`) (Acts I–V)

### Visual Design Sheet
- **Core Concept:** *A feral, golden-hearted Nadir bike-courier and stray-Pokémon rescuer who treats every Meridian checkpoint like a personal insult and carries a giant spanner + stray-lunchbox everywhere.*
- **Unused Colour Pair:** **High-Vis Chartreuse (`#B7E82A`) + Grease-Black (`#232629`)**, accent **Rusty Copper (`#C45B2C`)**.
- **1× Silhouette:** Compact, scrappy athletic build crowned by a crooked backwards yellow safety hardhat and a massive curved pipe-wrench jutting diagonally behind her shoulders like a battle-axe.
- **Iconic Prop:** A battered **tin megaphone taped to a lunchbox** overflowing with stray-Pokémon biscuits, plus protest patches pinned across her vest (`"FIX THE LIFTS"`, `"FEED STRAY MEOWTH"`, `"NO LATTICE"`).
- **Pose & Face:** Leaning far back on one heavy steel-toed boot, wrench resting across her shoulders, flipping a Great Ball backward over her shoulder without looking; spiky bleached-copper bangs sticking out from under the hardhat, band-aid across her nose, cocky toothy grin with one chipped canine.

### Personality, Catchphrases & Banter Pairings
- **Personality:** Pure *Pokémon Reborn* **Sandy** meets **Cain** chaotic loyalty! Loud, profane-adjacent (`"Aw, rust and rivets!"`), fiercely protective of Nadir's strays and street kids, and possesses an uncanny habit of showing up at the absolute worst moment in a commandeered utility vehicle to pull the PC out of trouble. She ran a fizzbolt-and-soup stand in Lumen's Lowlight right next to **Dex** (`181`) — after the Shatter Fixes Dex, Mags refuses to move his empty milk-crate (`"Nobody touches the kid's seat. He's comin' back for his change."`).
- **Catchphrases:**
  - *"Step aside, topsider — I've got six strays, a stolen forklift, and ZERO patience!"*
  - *"Ugly Pokémon? Pal, look in a puddle. My Garbodor's got better posture than Voss!"*
  - *(Ch16 Sump Purge clutch save):* *"Get in the cargo-lift, null-kid! Don't argue, I cut the brakes already!"*
- **Banter Pairings:**
  - **Dex & Rook Calder:** Before the Shatter, Mags bullies Rook into buying 20 Fizzbolts from Dex; after the Shatter, she quietly slips Rook a hot bowl of Mirefen noodles when he's sitting off-camera by Dex's glass figure.
  - **Corvin Mott & Wenlow:** She dumps half-frozen strays on Corvin's doorstep; Corvin invoices her ₽0 and threatens to adopt her wrench. Wenlow's death in Ch16 turns her jokes razor-sharp and furious.
  - **Zed Navarro (#10):** Her fiercely guarded "little brother" in the Sump — she yells at him to eat vegetables while he hacks Meridian doors for her.
  - **Marisol Reyes:** Instant union-solidarity best friends in Ch11's Ebbmouth Strike!

### Multi-Act Encounter & Battle Arc
- **Act I — Ch5 (Lumen Lowlight, `181`):** Blocks a Meridian sanitation drone from rounding up alley Trubbish; energetic optional battle on `:SCRAPYARD` / `:NEON_GRID` (Lv 24–25: **Scraggy**, **Trubbish**, **Alolan Meowth**). After the Shatter (`608`), she helps pull un-glassed neighbors out of the dark.
- **Act II — Ch7 (Mirefen Boardwalk, `220`):** Running an illegal street soup-kettle; tags alongside you or spars on `:CORROSIVE_MIRE` to chase off a Sweetrot pusher (Lv 33–34: **Scrafty**, **Garbodor**, **Grafaiai**, **Alolan Persian**).
- **Act III — Ch12 (Skyreach Lower Docks, `323`):** **Clutch Save #1!** Crashes a cargo-sled into a Directorate squad chasing you out of the Gale Post raid so you escape cleanly.
- **Act IV — Ch16–17 (Midstair / Underveil Sump Docks, `830/424`):** **Clutch Save #2!** Hauls civilians and stray Pokémon past the Purge barricades alongside Mother Gutter's Muk; fierce morale-boost spar on `:SCRAPYARD` (Lv 72–74: **Scrafty**, **Garbodor**, **Revavroom**, **Grafaiai**, **Alolan Persian**, **Obstagoon**).
- **Act V — Ch21 (Crownhaven Hijack Montage):** Drives a commandeered Meridian parade float straight through a Directorate cordon to clear the exit for Lower Crownhaven evacuees!
- **Ace Pokémon:** **Scrafty ("Knuckles")** & **Revavroom ("Forklift")** + **Garbodor ("Dumpster Princess")**.
- **Field Specialty:** `:SCRAPYARD` (uses Gunk Shot / Spin Out / Trash-hazard boosts!) & `:CORROSIVE_MIRE`.
- **Repeatable Rematch Location & Rewards:** **Mirefen Boardwalk Soup-Pot (`220`)** (Act II–III) and **Underveil Sump Docks (`424`)** (Act IV–Postgame) — *"Alley Brawl"* repeatable battle + daily **"Stray Rummage Box"** giving **Leftovers, Black Sludge, Focus Sash, Toxic Orb, Choice Band, and Exp Candy M/L**.

### Codex Entry
- **Unlock Flag:** `codex_met(:MAGS)` (Ch5 Lowlight encounter)
- **Progressive Bio Beats:**
  1. *Beat 1 (Ch5):* Lowlight bike-courier and stray-Pokémon rescuer who wears a stolen Meridian hardhat covered in protest stickers.
  2. *Beat 2 (Ch12):* Smuggles soup, medicine, and fugitives between Lumen, Skyreach, and Mirefen. Owns at least four illegally modified forklifts.
  3. *Beat 3 (Ch17):* Held the Sump Docks barricades during Operation Clear Air. Keeps Dex's milk-crate dusted every morning until Homecoming.
- **Affinity Perks (0–5 ★):** ★2 unlocks **Free Stray-Box Rummage** once per badge tier (free held items!); ★4 gifts a **hidden-ability Varoom / Shroodle** rescued from the Sump; ★5 lets her join you as an optional **Tag Partner** in Postgame Concordance Spire doubles!
- **`Portrait::CAST` & Audio:** `:MAGS` (full 10-expression sheet) | `BattleBGM = Battle - Sump Wildcard` (chaotic garage-punk ska / clanking percussion, Sandy/Team Skull energy) | `Voice - Mags.ogg` (raspy, rapid-fire street-alto blip).

---

## 4. Intern Bret Halvorsen & Intern Sloane Pendergast (Chaotic Meridian Intern Duo)

- **Archetype:** Team-Rocket-Meets-Corporate-Burnout Recurring Comic-Relief Double Battle (4-Act Radicalization Arc!)
- **Trainer Type ID & Bespoke Class:** `[SIDE_INTERNS]` → **`Meridian Interns`** *(Name in battle: `Meridian Interns Bret & Sloane`)*
- **Home Region / Span:** Zenith HQ — dragged miserably across Briarwick, Duneholt, Skyreach, and Cogsworth (Acts I–IV + Act V Redemption!)

### Visual Design Sheet
- **Core Concept:** *Two catastrophically underpaid, over-caffeinated Meridian "Junior Synergy Associates" dragging a creaking wheeled whiteboard across four kingdoms because HR refuses to reimburse their train tickets.*
- **Unused Colour Pair:** **Corporate Cyan (`#38B6CC`) + Bleached Khaki (`#D9CBB1`)**, accent **HR-Warning Red (`#D93838`)** lanyards.
- **1× Silhouette:** Hilarious tall-and-tiny comic-duo contrast! **Bret** is 6'3", slumped like a question mark under a wobbling skyscraper of clipboards; **Sloane** is 5'0", vibrating with espresso rage in an oversized promo blazer whose sleeves hang past her wrists, framed behind them by a crooked rolling easel-whiteboard.
- **Iconic Prop:** A **wheeled corporate whiteboard** covered in frantic red-marker arrows (`"STOP NULL KID -> ??? -> GET DENTAL?"`), a **laser pointer** Sloane wields like a fencing rapier, and a giant dented travel thermos taped `"UNPAID"`.
- **Pose & Face:** Bret awkwardly dropping two clipboards while fumbling a Premier Ball with huge dark eyebags and a pleading smile; Sloane thrusting her laser pointer directly at the camera with manic caffeinated pupils and a tiny vein throbbing on her temple!

### Personality, Catchphrases & Banter Pairings
- **Personality:** Pure *Reborn/Rejuvenation* recurring comic-relief double-battle gold, completely grounded in Prismfall's satirical corporate-villainy (`ZE_CUSTOMER_SUPPORT` energy!). They open every encounter with a rehearsed HR mission statement that collapses halfway through. Best of all, they have a **genuinely heartwarming 4-Act burnout-to-union arc**: in Act I they desperately want full-time health benefits; in Act II Quent demotes them to "unpaid legacy interns"; in Act III they start secretly slipping you free Hyper Potions *"billed to Voss's dry-cleaning account"*; and in Act IV (Cogsworth) they **quit live mid-cutscene**, chuck their lanyards into a furnace, and fight *beside* you against a Directorate goon!
- **Catchphrases:**
  - **Sloane:** *"PREPARE FOR ALIGNMENT!"* **Bret:** *"And make it... uh... cross-functional?"* **Sloane:** *"BRET, READ SLIDE TWO!!"*
  - **Bret:** *"Look, if we don't log at least one 'challenger impediment' by Friday, Director Marchetti takes away the breakroom kettle!"*
  - *(Act IV resignation):* **Sloane:** *"Effective immediately, Bret and I are pivoting to UNEMPLOYED VIOLENCE!"*
- **Banter Pairings:**
  - **Calla Wren:** Calla feels deeply guilty about them and secretly approves their fake meal receipts.
  - **Dr. Percival Quent:** Quent literally forgets their names in every chapter (`"Ah yes, Bread and Scone! Hold this glowing canister!"`).
  - **Director Marchetti:** Terrifies Bret into dropping his clipboard just by clearing her throat.
  - **Juno & Kestrel ("Team Compost"):** Sloane insists `"Team Compost"` is *"a terrible brand name with shockingly strong grassroots engagement."*

### Multi-Act Encounter & Battle Arc (4 Acts + Act V Payoff!)
- **Act I — Ch3 (The Weavers' Road / Briarwick Pylon, `540/120`):** Assigned to "guard the orange survey flags" — completely lost in the silk woods. Double Battle on `:SILKWOOD` (Lv 17–18: Bret's **Klefki** & **Audino**; Sloane's **Morpeko** & **Wattrel**).
- **Act II — Ch6 (Copperdune / Brass Dunes Railway Depot, `610`):** Demoted to inventorying Duneholt drill crates in blistering heat while wearing wool blazers. Double Battle on `:DESERT` (Lv 29–30: Bret's **Klefki**, **Porygon**; Sloane's **Morpeko**, **Kilowattrel**, **Tandemaus→Maushold**).
- **Act III — Ch12 (Skyreach Conductors' Causeway, `740`):** Ordered to enforce curfew; they awkwardly "lose" a mandatory-looking Double Battle on `:STORMFRONT` (Lv 52–54: Bret's **Klefki**, **Porygon2**, **Audino**; Sloane's **Morpeko**, **Kilowattrel**, **Maushold**), then accidentally drop a bag of **Full Restores** at your feet (`"Oops. Clumsy us. Expense code 9."`).
- **Act IV — Ch16 (Cogsworth Strade Works Courtyard, `403`):** **The Great Resignation!** Ordered to confiscate workers' lunches during Operation Clear Air; they snap, rip off their badges, and join a hilarious co-op spar/celebration on `:FACTORY` → `:SCRAPYARD` (Lv 68–70).
- **Act V — Ch20 (Crownhaven Market Ring, `496`):** Running an independent lemonade-and-strategy kiosk called **"Synergy-Free Consulting"** — handing out free flyers for Dorian's *Gilded King*!
- **Ace Duo:** **Morpeko ("Overtime")** (Hangry Mode = Sloane without coffee!) & **Maushold ("Team Building")** + **Klefki ("Badge Access")** + **Kilowattrel ("Deadline")** + **Porygon2 ("Spreadsheet")**.
- **Field Specialty:** `:FACTORY` / `:NEON_GRID` / `:SCRAPYARD` (Bret runs Screens/Thunder Wave/Follow Me "Red Tape" while Sloane sweeps with Aura Wheel/Population Bomb!).
- **Repeatable Rematch Location & Rewards:** **Lumen City Concourse Coffee Cart (`180`)** (post-Ch16) & **Crownhaven Market Ring (`496`)** — *"Quarterly Performance Review"* Double Battle paying **Big Nuggets ("unclaimed stipends"), Choice Specs, Light Clay, and Exp Candy M/L**.

### Codex Entry
- **Unlock Flag:** `codex_met(:INTERNS)` (Ch3 Weavers' Road encounter)
- **Progressive Bio Beats:**
  1. *Beat 1 (Ch3):* Meridian Junior Synergy Associates #4091 and #4092. Dragging a rolling whiteboard across Elowen in hopes of earning dental coverage.
  2. *Beat 2 (Ch12):* Demoted twice by Dr. Quent; quietly slipping supplies to fugitives on Voss's corporate expense card.
  3. *Beat 3 (Ch16):* Resigned live in Cogsworth by chucking their lanyards into a slag pit. Now co-founders of Velmora's tiniest independent consultancy.
- **Affinity Perks (0–5 ★):** ★2 unlocks **15% Mart Reimbursement Rebate** (Bret "processes your receipts" once per chapter for bonus cash!); ★4 gifts **Light Clay + Wide Lens**; ★5 unlocks **"Slide Deck #99"** Lv 92 Double Exhibition in Postgame.
- **`Portrait::CAST` & Audio:** `:BRET` and `:SLOANE` (paired 6-expression sets, frequent `\pfb` comic bubbles!) | `BattleBGM = Battle - Meridian Interns` (frantic office-jazz / *Unwelcome School*-adjacent syncopated brass + typewriter percussion, pure instrumental!) | `Voice - Bret.ogg` (tired sigh-baritone) & `Voice - Sloane.ogg` (jittery rapid-soprano blip).

---

## 5. Ezra "Coda" Kovacs (The Runaway Octave Virtuoso / Street Cellist)

- **Archetype:** Defector from the Prism Choir & Soulful Rebel Street Cellist
- **Trainer Type ID & Bespoke Class:** `[SIDE_CELLIST]` → **`Rogue Virtuoso`** *(Name in battle: `Rogue Virtuoso Ezra`)*
- **Home Region / Span:** Crownhaven (runaway) → Saltmere (`146`) → Mirefen (`220`) → Lucent (`340`) → Crownhaven (`489`) (Acts I–V)

### Visual Design Sheet
- **Core Concept:** *The unspoken "Ninth Orphan" of the Prism Choir — a brooding, tender-hearted cello prodigy who tore off his Choir hem, bolted before Vesper could assign him a Plate, and busks aching rebel chords across every port and undercity.*
- **Unused Colour Pair:** **Deep Wine-Burgundy (`#6B1D3A`) + Tarnished Brass (`#B59449`)**, accent **Dusk Violet (`#6E548C`)** messy hair.
- **1× Silhouette:** Lean bohemian silhouette anchored by a **massive scarred wooden cello case** strapped diagonally across his back (covered in transit stamps and taped setlists), with his tattered half-Choir cloak draped over only his left shoulder like a punk shawl.
- **Iconic Prop:** A cracked, varnish-peeling **acoustic travel cello** & horsehair bow dusted in white rosin (a tiny carved white lily scratched out near the scroll).
- **Pose & Face:** Perched sideways on his upended cello case, right arm drawing a dramatic sweeping bow stroke across the strings while his left hand flicks a Luxury Ball off the fingerboard; dark violet bangs half-shading brooding tired eyes, faint bitter-warm half-smile.

### Personality, Catchphrases & Banter Pairings
- **Personality:** Pure *Rejuvenation* **Ren / Crescent** quiet melancholy mixed with genuine punk warmth. Ezra isn't angry at Vesper out of malice — he's angry because the Choir raised Glassfall orphans to believe their *only* purpose was to sit gracefully beside a Plate and sing pretty hymns about "endurance." He ran away with no Eeveelution at all (preserving `design/EEVEE_OCTAVE.md`'s sacred 8-singer count!), instead bonding with stray Sound-type Pokémon who sing *out of tune*! Helping him across 4 acts doesn't drag him back into the Choir — instead, Vesper visits him in Crownhaven, hands him his folded robe, and says *"You don't have to come back to be my brother,"* leading to an optional acoustic duet in the Memorial Garden (`489`)!
- **Catchphrases:**
  - *"The Choir only teaches major chords. Funny how nobody in Velmora lives in a major key."*
  - *"You've got eighteen notes humming in that case, kid. Care to hear the sharp ninth?"*
  - *(Ch20 reconciliation with Vesper):* *"I'm still not wearing the collar, Vesper. ...Yeah. Okay. D-minor. Count us in."*
- **Banter Pairings:**
  - **Vesper Lindqvist:** Tender, aching sibling rift — Vesper secretly kept his choir pew empty for ten years; Ezra refuses to admit he attends her Saltmere Pageant from the cheap balcony every spring.
  - **Cadence (Octave #3):** His closest confidante among the Octave — they jam together on the Lowlight steps (`181`) before the Shatter!
  - **Dorian Pell:** Dorian tries to hire Ezra as Lantern Theatre pit-orchestra director; Ezra refuses on principle, then secretly scores the cello lament for Dorian's banned *Gilded King* in Ch20!
  - **Juno Hale:** Ezra lets Juno's Ralts (`Veil`) sit on his cello case in Lucent (`340`) because the vibrations calm it down.

### Multi-Act Encounter & Battle Arc
- **Act I — Ch2 (Saltmere Breakwater Arch, `146`):** Busking away from the Pageant crowds right after Vesper's backstage duet; tests your ear on `:GRAND_STAGE` / `:BEACH` (Lv 16: **Kricketune**, **Toxel**, **Swablu**).
- **Act II — Ch7 (Mirefen Stilt-Market, `220`):** Playing melancholy cello outside Corvin's Infirmary so the Quiet Ward patients have something gentle to dream to! Optional duel on `:CORROSIVE_MIRE` (Lv 34: **Kricketune**, **Toxtricity-Low Key**, **Altaria**, **Chimecho**).
- **Act III — Ch13 (Lucent Athenaeum Cloister Wall, `344`):** Outside the court watching Vesper & the Octave guard Hierophant Ellery; emotional confrontation if you've helped ≥3 Octave singers. Duel on `:MINDSCAPE` (Lv 57: **Toxtricity-Low Key**, **Altaria**, **Noivern**, **Chimecho**, **Primarina**).
- **Act IV — Ch15 (Gravenmoor Barrow Steps, `380`):** Playing a silent bow-less dirge to Gravenmoor's lingering echoes; duel on `:HOLLOW_CATHEDRAL` (Lv 66: adds **Skeledirge** or **Mega Altaria** — wait, let's give him **Mega Altaria** post-Ch14 via a chipped Choir tuning-pin!).
- **Act V — Ch20 (Crownhaven Memorial Garden Bench, `489`):** **Music Quest Finale!** Bring Vesper's letter (unlocked after helping any 4+ Octave singers or clearing Ch13) to trigger the **Cello & Choir Duet**; final battle on `:GRAND_STAGE` (Lv 88: **Toxtricity-Low Key**, **Mega Altaria**, **Primarina**, **Noivern**, **Skeledirge**, **Kricketune** [Sticky Web + Perish Song tech!]).
- **Ace Pokémon:** **Toxtricity (Low Key Form) ("Dissonance")** (Punk Rock bass-cello partner!) & **Mega Altaria ("Harmonic")** (Pixilate Hyper Voice on Grand Stage!).
- **Field Specialty:** `:GRAND_STAGE` (Sound moves ×1.5 + Punk Rock stacking!) & `:HOLLOW_CATHEDRAL` (turns Echo/Sound moves into Inverse cracks if careless!).
- **Repeatable Rematch Location & Rewards:** **Saltmere Breakwater Arch (`146`)** (Acts I–III) and **Crownhaven Memorial Garden Bench (`489`)** (Act V–Postgame) — *"Encore Jam Session"* rewarding **Throat Spray, Metronome, Sound-Move Tutor** (*Hyper Voice, Alluring Voice, Snarl, Parting Shot, Perish Song*), and **Exp Candy L**.

### Codex Entry
- **Unlock Flag:** `codex_met(:EZRA)` (Ch2 Saltmere Breakwater encounter)
- **Progressive Bio Beats:**
  1. *Beat 1 (Ch2):* A moody busker carrying a scarred travel cello and a torn Choir cloak. Refuses to speak to the Eevee Octave.
  2. *Beat 2 (Ch7):* Plays quietly outside Mirefen's Quiet Ward at dusk. Believes music should comfort the broken, not dress up propaganda.
  3. *Beat 3 (Ch20):* The Choir's runaway ninth orphan. Reconciled with Vesper on his own terms and scored the cello lament for *The Gilded King*.
- **Affinity Perks (0–5 ★):** ★2 unlocks **Ezra's Acoustic Move Tutor**; ★4 grants **Throat Spray + Altarianite** (if Altarianite isn't already placed, else **Soundproof/Punk Rock Ability Capsule + Metronome**); ★5 unlocks a **Tag Battle alongside Ezra vs Vesper & Cadence** in Postgame!
- **`Portrait::CAST` & Audio:** `:EZRA` (full 10-expression sheet) | `BattleBGM = Battle - Rogue Virtuoso` (passionate cello-rock concerto with distorted bassline — pure instrumental!) | `Voice - Ezra.ogg` (resonant low cello-pizzicato blip).

---

## 6. Willa "Snap" Quigley (Cryptid / Field-Phenomenon Photographer & Gale Post Courier)

- **Archetype:** Hyper-Enthusiastic Gale Post Air-Courier & Paranormal Field-Shutterbug
- **Trainer Type ID & Bespoke Class:** `[SIDE_PHOTOGRAPHER]` → **`Rift Shutterbug`** *(Name in battle: `Rift Shutterbug Willa`)*
- **Home Region / Span:** Skyreach Gale Post (`325`) — chases Bleed Veils & EventMons across every kingdom (Acts I–V)

### Visual Design Sheet
- **Core Concept:** *A fearless, zero-self-preservation Gale Post rookie & underground cryptid-zine editor draped in three clacking brass cameras who tries to photograph every Bleed anomaly, EventMon, and legendary in Velmora.*
- **Unused Colour Pair:** **Sunset Terracotta (`#D95D39`) + Warm Canvas Cream (`#F2E6D0`)**, accent **Prism-Filter Cyan (`#45D1E8`)**.
- **1× Silhouette:** Forward-leaning aerodynamic silhouette: billowing flight-scarf fluttering straight back, bulky boxy vintage bellows-camera slung wide across her ribs, and oversized flip-down multi-lens brass eyepiece perched on her aviator cap like bug-eyes.
- **Iconic Prop:** A triple-lens **clockwork prism-bellows camera** dripping wet developed photo-strips clipped directly to her coat hem with clothespins.
- **Pose & Face:** Leaning radically forward toward the camera at a 45° angle, peering through her giant brass viewfinder aimed straight at the player with a blinding flashburst; wide sparkling freckles, huge lopsided ecstatic grin, stray ginger curls escaping her leather flight-cap.

### Personality, Catchphrases & Banter Pairings
- **Personality:** Relentlessly curious, slightly unhinged journalist-adventurer energy (*Rejuvenation* **Amber / Erin** curiosity + *Pokémon Snap* mania!). She edits an illegal photocopied broadsheet called **"THE BLEED GAZETTE"** distributed on the bottom of Gale Post mailbags. Every time you explore an optional Bleed Zone or rare EventMon den, Willa is camped three inches outside the Veil holding a camera on a broomstick (`"I can't cross it, my eyelashes start crystallizing — PLEASE go snap a shot for page three!!"`). Mechanically, she acts as an **in-world Explorer's Guide** who rewards `fields_seen`, rare EventMon captures, and optional dungeon visits!
- **Catchphrases:**
  - *"HOLD STILL! The Bleed lighting on your face is PURE FRONT-PAGE GOLD!"*
  - *"Postmaster Halloran says 'stick to parcels.' I say a glassed Galvantula IS a parcel — of NEWS!"*
  - *"Wait, wait, don't beat me yet — trigger the weather first! My shutter speed needs drama!"*
- **Banter Pairings:**
  - **Odessa Gale:** Her cool older-sister boss who officially tells Willa *"no diving into Bleed zones"* and unofficially slips her spare film canisters.
  - **Postmaster Halloran (Elevated E9):** Constantly deducting broken camera lenses from Willa's salary (`"Knock twice, Quigley, and STOP photographing the franking machine!"`).
  - **Professor Larch:** Willa desperately wants an exclusive photo of Larch's kelp tea under a microscope (`"One droplet, Professor! My readers deserve to know what's living in it!"`).
  - **Juno Hale:** Swap sketches and pressed-flower prints whenever they cross paths!

### Multi-Act Encounter & Battle Arc
- **Act I — Ch1/2 (Windfall Row outside Glassed Orchard `521` → Gossamer Wood `524`):** Gives you the **"Shutterbug's Checklist"** (tracks `fields_seen` & EventMons!). First friendly photo-shoot battle on `:MEADOW` / `:SILKWOOD` (Lv 14–15: **Fletchling**, **Helioptile**, **Natu**).
- **Act I — Ch4 (Frostflat Causeway outside The Rehearsal, `560`):** Trying to photograph the 5-second looping ghost wagon crash (`EL_REHEARSAL`). Optional fight on `:BEACH` / `:MEADOW` (Lv 22: **Fletchinder**, **Helioptile**, **Xatu**, **Wingull→Pelipper**).
- **Act II — Ch7 (Outside Weeping Fen, `648`):** Holding an upside-down umbrella trying to snap photos of upward-falling rain! Fight on `:CORROSIVE_MIRE` (Lv 35: **Talonflame**, **Heliolisk**, **Xatu**, **Bombirdier**).
- **Act III — Ch12 (Skyreach Gale Post Balcony, `325`):** Helps sneak prints of the **Larch Papers** onto civilian mail-skiffs during Marchetti's raid! Fight on `:STORMFRONT` (Lv 54: **Talonflame**, **Heliolisk**, **Sigilyph**, **Bombirdier**, **Mimikyu**).
- **Act IV — Ch16/17 (Ironbloom Edge, `828` / The Drownings `821`):** Photographing rust-flowers & Aurelia's rising golden spires! Fight on `:WATER_SURFACE` / `:SCRAPYARD` (Lv 73: **Talonflame**, **Heliolisk**, **Sigilyph**, **Bombirdier**, **Mimikyu**, **Kilowattrel**).
- **Ace Pokémon:** **Heliolisk ("Flashbulb")** (Parabolic Charge / Glare / Weather Ball / Surf — literally reacts to Rain, Sun, Sand, Electric, and Light fields!) + **Talonflame ("Express")** + **Sigilyph ("Cryptid")**.
- **Field Specialty:** `:STORMFRONT` & `:RAINBOW` (loves Weather Ball + Flash/light moves!).
- **Repeatable Rematch Location & Rewards:** **Skyreach Gale Post Sorting Balcony (`325`)** — *"Action Shoot Rematch"* (battle on a rotating weekly/selectable field she wants photographed!) + **Exploration Milestone Rewards** (for hitting 10 / 20 / 30 `fields_seen` and catching 5 / 12 / 20 EventMons): **Quick Balls, Dusk Balls, Moon Balls, Dream Balls, Rare Candies, Zoom Lens, and Rumor Tips for hidden EventMons/Bleed Shards**.

### Codex Entry
- **Unlock Flag:** `codex_met(:WILLA)` (Ch1/2 Windfall Row or Saltmere encounter)
- **Progressive Bio Beats:**
  1. *Beat 1 (Ch2):* Over-caffeinated Gale Post rookie and editor of *The Bleed Gazette*. Wears three clacking brass cameras at all times.
  2. *Beat 2 (Ch12):* Smuggled printed copies of the Larch Papers out of Skyreach during the Directorate raid hidden inside seed catalogs.
  3. *Beat 3 (Ch17):* Her photographs of the Drownings and the Lowlight shrines became Envoy Okoro's visual evidence against Severance.
- **Affinity Perks (0–5 ★):** ★2 unlocks **Unvisited Bleed Zone & EventMon Rumor Radar** (tells you which secrets you missed per kingdom!); ★4 gifts **Apricorn/Special Ball Pack (5× Moon/Dream/Heavy/Love Balls)**; ★5 prints a **Commemorative Team Photo** entry in your Codex!
- **`Portrait::CAST` & Audio:** `:WILLA` (full 10-expression sheet) | `BattleBGM = Battle - Rift Shutterbug` (breezy upbeat sky-adventure accordion/brass + camera-shutter hi-hat ticks, pure instrumental!) | `Voice - Willa.ogg` (bright, bouncy staccato soprano blip).

---

## 7. Gideon Hawthorne (The Bitter-Sweet Rival Botanist & Kelp-Tea Sommelier)

- **Archetype:** Theatrical Aristocrat-Botanist, Larch's 30-Year Academic Rival & Secretly Warm Mentor to Juno
- **Trainer Type ID & Bespoke Class:** `[SIDE_BOTANIST]` → **`Tea Sommelier`** *(Name in battle: `Tea Sommelier Gideon`)*
- **Home Region / Span:** Verdance (`283` Glasshouse Ward) — roams Elowen, Ossaria, and Gloaming (Acts I–V)

### Visual Design Sheet
- **Core Concept:** *A scandalized, monocle-wearing royal botanist and tea purist who wages a thirty-year cold war against Imelda Larch's kelp tea while hauling a glowing glass bell-jar walking cane full of rare flora.*
- **Unused Colour Pair:** **Sage Olive (`#6B8E6E`) + Porcelain White (`#F5F2EB`)**, accent **Steeped Crimson (`#8C2D3B`)** cravat.
- **1× Silhouette:** Tall, immaculate hourglass waistcoat silhouette broken by a wide-brimmed velvet botanical beret tilted sharply right and a tall **glowing glass bell-jar walking staff** towering past his shoulder.
- **Iconic Prop:** A silver-rimmed **bell-jar cane** cradling a hovering miniature crystalline Bleed-fern, plus a delicate porcelain teacup balanced permanently in his white-gloved left hand (with green chlorophyll stains on the fingertips!).
- **Pose & Face:** Leaning languidly on his bell-jar cane with pinky rigidly raised on his saucer, tossing a Nest Ball lazily with two fingers; monocle clipped to a silver tea-strainer chain, sharp aristocrat nose, one horrified twitching brow whenever kelp is mentioned.

### Personality, Catchphrases & Banter Pairings
- **Personality:** Think *Reborn* **Bennett / Radomus** refinement blended with pure *Prismfall* dry British comedy! Gideon and Professor Imelda Larch were rival top-of-their-class scholars at Lucent Athenaeum thirty years ago (`"She went into electrical engineering to escape proper botany, and look what happened — she broke the sky AND ruined tea!"`). He acts insufferably refined, yet gets fired from Queen Maelis's court in Ch10 for telling her to her face that Verdance's un-rotting soil is suffocating the kingdom — and quietly becomes **Juno's fussiest horticultural mentor** after Rowan's arrest, refusing to admit how deeply he respects her courage.
- **Catchphrases:**
  - *"Imelda Larch boiling tide-wrack is NOT a tisane — it is a felony committed against hot water!"*
  - *"You dare bring a dusty road-team onto my conservatory tile? Very well. Let us steep."*
  - *(Ch10, watching Juno as Warden):* *"Her pruning technique is atrocious. Her wreath is crooked. ...And she is the finest Warden Verdance has had in a century. Do NOT quote me."*
- **Banter Pairings:**
  - **Professor Larch:** Glorious running feud tying straight into **Running Gag #1 (Kelp Tea)**! In `NA_SWEETROT` (Ch18), Gideon is physically devastated when Larch's kelp tea turns out to be the *only* brew bitter enough to cure the Sweetrot vendors (`"I am retiring from tongue-having."`).
  - **Juno Hale:** He initially lectures her on her Bride Tree wreath in Ch2, freezes in genuine horror/tenderness when she cheerfully explains *"Oh, it's my aunt!"*, and spends Acts III–V smuggling her rare Verdance soil tonics.
  - **Rowan Ashby:** Deep quiet respect — Rowan was the one person who agreed with Gideon's banned paper on *"The Necessity of Compost."*

### Multi-Act Encounter & Battle Arc
- **Act I — Ch2 (Saltmere Promenade Tea Stall, `140`):** Spits out a sample of Ferrow's kelp blend, spots your Tidewatch starter, and demands an educational duel on `:MEADOW` (Lv 15: **Poltchageist**, **Roselia**, **Smoliv**).
- **Act II — Ch6 (Duneholt Aquifer Quarter, `204`):** Investigating how desert flora survive the shrinking well; triggers `:DESERT` **Superbloom** stage! (Lv 30: **Poltchageist**, **Roserade**, **Dolliv**, **Cacturne/Lilligant**).
- **Act III — Ch10 (Verdance Glasshouse Ward, `283`):** Fired by Queen Maelis for defending Juno; helps Juno contain the runaway vines and challenges you on `:FLOWER_GARDEN` (forces Growth Stage 5!) (Lv 47: **Sinistcha**, **Roserade**, **Arboliva**, **Florges**, **Polteageist**).
- **Act V — Ch18 (Gloaming Dusk-Garden, `440`):** Sampling dusk-blooming petals that only open in twilight; deeply moved by Celestine's impending first night sky. Duel on `:FAIRY_TALE` / `:FLOWER_GARDEN` (Lv 80: **Sinistcha**, **Polteageist**, **Roserade**, **Arboliva**, **Florges**, **Mega Venusaur / Meganium** — let's use **Mega Venusaur** or **Grassium Z Sinistcha**? Since Juno gets Venusaurite, give Gideon **Sinistcha + Polteageist + Arboliva + Roserade + Florges + Tsareena? No, Juno → Lilligant-Hisui**!).
- **Ace Pokémon:** **Sinistcha ("Oolong")** (literal Hospitality Matcha Tea Pokémon!) paired with **Polteageist ("Earl")** & **Arboliva ("Estate")**.
- **Field Specialty:** `:FLOWER_GARDEN` (rushes Stage 5 Bloom!) & `:DESERT` (Superbloom) & `:MEADOW`.
- **Repeatable Rematch Location & Rewards:** **Verdance Glasshouse Conservatory (`283`)** — *"High Tea Exhibition"* repeatable battle awarding **Nature Mints (Modest/Timid/Calm/Bold), Telluric Seeds, Revival Herbs, EV-Reducing Berries, and Unremarkable/Masterpiece Teacups**!

### Codex Entry
- **Unlock Flag:** `codex_met(:GIDEON)` (Ch2 Saltmere tea stall encounter)
- **Progressive Bio Beats:**
  1. *Beat 1 (Ch2):* Elowen's former Royal Botanical Conservator and Imelda Larch's thirty-year rival. Treats bad tea as a capital offense.
  2. *Beat 2 (Ch10):* Dismissed from Briar Keep for warning Queen Maelis that Verdance's un-rotting soil was choking. Quietly mentors Warden Juno.
  3. *Beat 3 (Ch18):* Publicly wept when Larch's kelp tea cured Underveil's Sweetrot victims. Has begrudgingly ordered one (1) tin of kelp for "research."
- **Affinity Perks (0–5 ★):** ★2 unlocks **Gideon's Botanical Mint & Berry Bar** (buy EV Berries + Nature Mints at a discount!); ★4 gifts a **Masterpiece Teacup + Poltchageist/Sinistea**; ★5 unlocks a hilarious **Tag Spar: You + Larch (using Kelp Tea buffs!) vs Gideon + Juno** in Postgame!
- **`Portrait::CAST` & Audio:** `:GIDEON` (full 10-expression sheet) | `BattleBGM = Battle - Tea Sommelier` (crisp harpsichord & baroque strings waltz, pure instrumental!) | `Voice - Gideon.ogg` (clipped, posh nasal tenor blip).

---

## 8. Zainab Darzi — *"White-Flag Zainab"* (The Ossaria Bone-Carter Chronicler)

- **Archetype:** Soulful Face of the Ossaria Burial Guild (`13_CUTSCENES.md` & `14_WAR_AND_BLESSING.md`)
- **Trainer Type ID & Bespoke Class:** `[SIDE_CARTER]` → **`Bone Chronicler`** *(Name in battle: `Bone Chronicler Zainab`)*
- **Home Region / Span:** Ossaria (Duneholt `203`, Cragholm `360`, Bone-Carters' Camp `930`, Glass Dunes `926`, Crownhaven `489`) (Acts II–V)

### Visual Design Sheet
- **Core Concept:** *A young, grave-eyed chronicler of the Ossarian Bone-Carters' Guild who walks fearlessly between warring armies under the white bone-banner, recording the real names of every soldier the crowns forget.*
- **Unused Colour Pair:** **Sun-Bleached Bone White (`#EAE2D1`) + Desert Indigo (`#263B5E`)**, accent **Clay Ochre (`#B87344`)**.
- **1× Silhouette:** Sweeping desert traveler's hooded mantle towering upward via a **tall white rib-bone banner standard** planted at her side, topped with a hollow whistling bone wind-chime.
- **Iconic Prop:** The **White Bone-Banner** (the sole flag both Ashkaar and Isenmar refuse to fire upon in `13_CUTSCENES.md` WAR-1!) plus a strapped brass charcoal-rubbing slate and wax-sealed name-tubes at her hip.
- **Pose & Face:** Planting her bone-banner staff firmly into the sand with her left hand while pressing a clay-dusted Poké Ball against her collarbone in solemn guild salute; face half-wrapped in an indigo sand-scarf embroidered with neat bone-tally marks, warm, fiercely steady dark eyes, faint dry crease of gallows humor at the corner of her gaze.

### Personality, Catchphrases & Banter Pairings
- **Personality:** Grounded, dignified, quietly hilarious in a razor-dry desert way (`"Both kings pay Kassan rent to fight on our sand. Neither remembers how to dig a proper hole. Good thing we're unionized."`). She transforms the Bone-Carters from background lore in `13_CUTSCENES.md` and `14_WAR_AND_BLESSING.md` into one of Prismfall's most unforgettable emotional anchors — someone who carries zero weapons, bows to zero kings, and treats every fallen soldier (Isenmar, Ashkaar, or Ossarian) with equal tenderness.
- **Catchphrases:**
  - *"Under the white bone, no sword leaves its sheath. Except Pokémon. Pokémon are polite about it."*
  - *"Kassan sells the dirt. We keep the names."*
  - *(Ch19, stepping onto the fresh Glass Dunes after WAR-1):* *"Don't apologize for the glass, child. You kept half of them standing. Now help me count the rest."*
- **Banter Pairings:**
  - **Sahar Ostrand:** Old comrades — Zainab brings Sahar unearthed fossils while Sahar slips Zainab sealed Accord casualty lists.
  - **Bastian Ore & Anja Sorrel:** Zainab is the chronicler who marches Anja's frostbitten Rimeholt refugee column across the war lines to Cragholm under her white banner in Ch14!
  - **Ysolde Ashgrave:** Two caretakers of the dead sharing tea in Ch20 — Ysolde envies that Ossaria's dead actually *rest*, while Zainab gently asks Ysolde to greet the echoes for her.
  - **Kaito Ren:** Quiet, wordless mutual respect over Marrowgate.

### Multi-Act Encounter & Battle Arc
- **Act II — Ch6 (The Rib Road / Duneholt Sandgate, `601/203`):** First met charting an old caravan burial cairn toppled by Meridian's drills; tests your footing on `:DESERT` (Lv 30: **Greavard**, **Yamask-Galar**, **Vullaby**, **Hippopotas**).
- **Act IV — Ch14 (Cragholm Refugee Seam `360` → Bone-Carters' Camp `930`):** Arrives leading Anja's Rimeholt refugees; then at the Dry Tide camp (`930`), gives the canonical **Steamline Dog-Tag Recovery** mission (`14_WAR_AND_BLESSING.md` — asks the Unimprinted PC to walk into the glass to recover lost soldiers' tags!). Respectful honor-duel on `:DESERT` / `:GLASS_DUNES` (Lv 63: **Houndstone**, **Runerigus**, **Mandibuzz**, **Hippowdon**, **Alolan Marowak**).
- **Act V — Ch19 (Bone-Carters' Camp `930` / Glass Dunes `926` Aftermath):** Stands beside you right after WAR-1 as the Bone-Carters claim the new Glass Dunes necropolis under Ossarian tomb-law; cathartic battle on `:GLASS_DUNES` (Lv 83: **Houndstone**, **Runerigus**, **Mandibuzz**, **Hippowdon**, **Alolan Marowak**, **Palossand**).
- **Act V — Ch20 (Crownhaven Memorial Garden, `489`):** Reads the war's true casualty scroll aloud outside the Pavilions so neither crown can pretend it was bloodless!
- **Ace Pokémon:** **Houndstone ("Epitaph")** (Last Respects / Sand Rush — literal desert burial hound!) + **Runerigus ("Headstone")** + **Alolan Marowak ("Cairn")**.
- **Field Specialty:** `:DESERT` & `:GLASS_DUNES` (Sandstorm + Ghost/Ground mastery; avoids shattering glass unless forced!).
- **Repeatable Rematch Location & Rewards:** **The Bone-Carters' Camp (`930`)** & **Duneholt Mural Gallery Steps (`207`)** — *"Vigil Spar"* rewarding **Random Fossils (Skull/Armor/Sail/Jaw/Plume/Cover/Old Amber)** for Sahar's Dig Lab, **Soft Sand, Spell Tag, Reaper Cloth, and Exp Candy L**.

### Codex Entry
- **Unlock Flag:** `codex_met(:ZAINAB)` (Ch6 Rib Road / Sandgate encounter)
- **Progressive Bio Beats:**
  1. *Beat 1 (Ch6):* Chronicler of the Ossarian Bone-Carters' Guild. Carries the white bone-banner that binds every desert caravan to truce.
  2. *Beat 2 (Ch14):* Marched Anja's Rimeholt refugees across the war front under her banner, defying both crowns and Prince-Elector Kassan.
  3. *Beat 3 (Ch19):* Claimed the Glass Dunes as an Ossarian necropolis so neither army could march over its dead again.
- **Affinity Perks (0–5 ★):** ★2 unlocks **Daily Unearthed Fossil Gift** (free unrevived fossil per visit!); ★4 gifts a **Thick Club + Sand-Force/Last-Respects Greavard egg/item**; ★5 unlocks **Zainab's Bone-Banner Decoration** & Lv 95 Glass Dunes rematch!
- **`Portrait::CAST` & Audio:** `:ZAINAB` (full 10-expression sheet) | `BattleBGM = Battle - Bone Chronicler` (haunting desert oud, frame-drum, and cello dirge that builds into stoic resolve — pure instrumental!) | `Voice - Zainab.ogg` (warm, calm dry-alto woodblock blip).

---

## 9. Master Magda "Slag-Hammer" Vorn (Grumpy Master Forgemaster & Move-Tutor Rival)

- **Archetype:** Pint-Sized Volcanic-Tempered Hearthguild Renegade, Sparring Rival & Move-Tutor / Exp-Candy Engine
- **Trainer Type ID & Bespoke Class:** `[SIDE_FORGEMASTER]` → **`Iron Tutor`** *(Name in battle: `Iron Tutor Magda`)*
- **Home Region / Span:** Ashkaar (Cindervault Slag Ward `249`) — hauls a fold-out portable anvil cart to Frostwick, Cindervault, Cragholm, Cogsworth, and Crownhaven (Acts I–V)

### Visual Design Sheet
- **Core Concept:** *A 4-foot-11 terrifyingly muscular silver-haired master smith — the woman who trained giant Brann Holloway — who quit the Hearthguild over war-forging and now roams Velmora aggressively beating sloppy trainer teams into tactical shape.*
- **Unused Colour Pair:** **Molten Forge-Orange (`#FF5A1F`) + Soot Iron (`#36393F`)**, accent **White-Hot Steel (`#EBF2F7`)** welding visor & straps.
- **1× Silhouette:** Low, broad, immovable anvil-like stance: wild iron-grey bun pinned under a flipped-up steel welder's visor, dwarfed by **ONE absurdly oversized bronze forge-gauntlet** on her right arm hefting a glowing square-headed smith's hammer! (Brilliant silhouette contrast against tall 6'6" Brann!)
- **Iconic Prop:** A white-hot **tuning hammer** and a leather **Move-Tutor Brand Bandolier** rattling with red-hot iron sigils (each representing a combat discipline: Fang, Fist, Gale, Edge).
- **Pose & Face:** Right heavy iron-toed boot slammed squarely onto a portable glowing anvil, leaning forward pointing her hammer straight between the player's eyes; fierce bushy grey eyebrows angled sharp down, one corner of her mouth curled in an approving battle-scowl, soot smudge across one cheek.

### Personality, Catchphrases & Banter Pairings
- **Personality:** Every beloved *Reborn/Rejuvenation* crusty veteran mentor & Move-Tutor rolled into one explosive pint-sized powerhouse! She yells at you because she refuses to watch another fifteen-year-old walk into a meat-grinder with `Tackle` and `Scratch` still on their moveset. **Brann Holloway was her apprentice forty years ago** — watching giant booming Brann instantly stand up straight and say *"Yes, Boss"* when tiny Magda walks into Hearthguild Hall is pure gold. Mechanically, she solves the #1 fangame QoL desire: **a repeatable, cap-scaling Exp-Candy & EV-Training "Anvil Drill" sparring partner + progressive Move Tutor!**
- **Catchphrases:**
  - *"WHAT is that moveset?! Four Normal attacks and a prayer?! GET ON THE ANVIL!"*
  - *"Brann cries at weddings. I hit steel till it apologizes. Guess which one keeps you alive."*
  - *(After losing a hard spar):* *"...Hmph. Good edge. Terrible footwork, still. Come back Tuesday."*
- **Banter Pairings:**
  - **Brann Holloway:** Endless comic respect — Magda critiques his welding seams; Brann sneaks her fresh roasted chestnuts and pretends they "fell off a wagon."
  - **Magnus Strade:** Bitter philosophical foil — Magda roasts his sterile Cogsworth automation (`"If a blade doesn't have hammer-marks, Magnus, it's just jewelry for cowards!"`).
  - **Kaito Ren:** Zero wasted words — they spar silently for twenty minutes, nod once, and drink black tea.
  - **Professor Larch:** Magda asks for a bucket of Larch's kelp tea *"strictly for quenching high-carbon steel"* (directly paying off **Running Gag #1** from `15_COMEDY.md` Ch8!).

### Multi-Act Encounter & Battle Arc
- **Act I — Ch4 (Frostwick Pass, `577`):** Hammering a cracked Isenmar refugee sled axle in the snow; mocks your early-game movesets and forces your first tactical spar on `:MOUNTAIN` (Lv 21: **Tinkatink**, **Drilbur**, **Torkoal**). Unlocks **Tier 1 Move Tutors** (Elemental Fangs, Low Kick, Vacuum Wave, Covet, Snore).
- **Act II — Ch8 (Cindervault Slag Ward, `249`):** Kicks Dominar war-lance recruiters out of her alley and scolds Brann; fierce spar on `:VOLCANIC` → `:ASHEN_WASTE` (Lv 38: **Tinkatuff**, **Excadrill**, **Torkoal**, **Turtonator**, **Lairon**). Unlocks **Tier 2 Move Tutors** (Elemental Punches, Iron Head, Zen Headbutt, Liquidation, Foul Play, Earth Power).
- **Act IV — Ch14 (Cragholm Lift Yard, `360`):** Forging mining braces for Bastian's refugee seams; spar on `:CRYSTAL_CAVERN` (Lv 63: **Tinkaton**, **Excadrill**, **Torkoal**, **Turtonator**, **Mega Aggron**, **Conkeldurr**). Unlocks **Tier 3 Move Tutors** (Knock Off, Defog, Tailwind, Stealth Rock, Scorching Sands, Flip Turn, Coaching).
- **Act IV — Ch16 (Cogsworth Foundry Alley, `400`):** Quietly spiking Meridian's Prism-lance molds with brittle slag so they snap on the first swing! Spar on `:SCRAPYARD` (Lv 71: full 6-mon team!). Unlocks **Tier 4 Master Tutors** (Draco Meteor / Steel Beam / Meteor Beam / Poltergeist / Triple Axel / Scale Shot).
- **Ace Pokémon:** **Tinkaton ("Anvil-Bite")** (tiny powerhouse with a gigantic hammer — literally her spirit animal!) + **Mega Aggron ("Slag-Wall")** + **Excadrill ("Quench")**.
- **Field Specialty:** `:VOLCANIC` / `:ASHEN_WASTE` (Cinderglass) / `:SCRAPYARD`.
- **Repeatable Rematch Location & Rewards:** **Cindervault Slag Ward (`249`)** + her **Travelling Anvil Cart** parked near major hubs (Lumen/Cragholm/Crownhaven) — TWO repeatable options:
  1. **"Anvil Drill" (Exp-Candy Grinder):** Chansey/Blissey/Audino + Tinkaton sparring squad scaled cleanly to `level_cap - 2` (zero blackout on loss!) paying **Exp Candy S/M/L/XL** (by act) + **Heart Scales**.
  2. **"Master Spar" (Real Fight):** Full competitive team paying **Heavy-Duty Boots, Choice Band, Rocky Helmet, Assault Vest, and Move-Tutor Discounts**.

### Codex Entry
- **Unlock Flag:** `codex_met(:MAGDA)` (Ch4 Frostwick Pass encounter)
- **Progressive Bio Beats:**
  1. *Beat 1 (Ch4):* Pint-sized former Hearthguild master smith who hauls a portable anvil across Velmora. Trained Warden Brann Holloway forty years ago.
  2. *Beat 2 (Ch8):* Walked out of Cindervault's guildhall when the Dominar ordered war-lances forged on Meridian contracts.
  3. *Beat 3 (Ch16):* Quietly sabotaged Cogsworth's Prism-lance molds and forged half the rescue gear used at Crownhaven. Still refuses to say she's proud of you.
- **Affinity Perks (0–5 ★):** ★1–4 unlock **Move Tutor Tiers 1–4**; ★3 cuts Move-Tutor fees by 50%; ★5 grants **Aggronite backup / Tinkaton Gigaton-Hammer coaching + Lv 96 Master Forge Rematch**!
- **`Portrait::CAST` & Audio:** `:MAGDA` (full 10-expression sheet) | `BattleBGM = Battle - Iron Tutor` (rhythmic anvil-clang industrial rock with blistering guitar riffs — pure instrumental!) | `Voice - Magda.ogg` (metallic gruff alto anvil-tap blip).

---

## 10. Zed "Static" Navarro (Underground Nadir Sump Info-Broker & Glitch Hacker)

- **Archetype:** Teenage Nadir Lattice-Hacker, Rook's Secret Chat Moderator & Nyx's Shadow Technician
- **Trainer Type ID & Bespoke Class:** `[SIDE_HACKER]` → **`Lattice Splicer`** *(Name in battle: `Lattice Splicer Zed`)*
- **Home Region / Span:** Lumen Lowlight (`181`) ↔ Mirefen (`220`) ↔ Cogsworth (`400`) ↔ Underveil (`423`) (Acts I–V)

### Visual Design Sheet
- **Core Concept:** *A nocturnal, wire-tangled Nadir kid prodigy who splices pirated Zenith bandwidth through drainage pipes, runs Rook's stream moderation anonymously from a basement, and sells stolen Meridian blueprints for noodle money.*
- **Unused Colour Pair:** **Acid Mint-Green (`#3EE8A5`) + Matte Midnight-Slate (`#1B212C`)**, accent **Phosphor-Cyan (`#62F5FF`)** visor glow.
- **1× Silhouette:** Slouched hooded silhouette coiled in thick glowing fiber-optic conduit cables draped around his neck like a scarf, with a bulky forearm-mounted salvaged cyberdeck protruding horizontally left.
- **Iconic Prop:** A cracked **brass-and-glass mono-visor** projecting scrolling emerald telemetry over his left eye, plus a cobbled-together non-Rotom **Lattice Splicer Gauntlet** trailing alligator clips.
- **Pose & Face:** Hunched sideways typing rapidly in mid-air over glowing holographic keys while an Ultra Ball levitates in a green static arc above his palm; shadowed dark curls, huge sly asymmetrical smirk, one bright green-lit eye peeking behind data lines.

### Personality, Catchphrases & Banter Pairings
- **Personality:** Pure *Reborn* **DJ Arclight / Radomus-tech** meets *Rejuvenation* **Saki / Huey** witty gremlin energy — cynical about topsiders, obsessed with code & glitches, fiercely loyal once you prove you aren't a Meridian snitch. **HUGE CANON PAYOFF:** Zed is **`@Null_Zero`**, the sarcastic moderator in **Rook Calder's livestream chat** (`story/15_COMEDY.md` Running Gag #4: *"Chat is always wrong about battles and always right about feelings"*)! Zed started trolling Rook from Nadir's lift grates, realized Rook was actually a lonely kid trapped by Meridian debt, and secretly becomes the guy who helps Rook **clone the Strade Works keycards (Ch16)** and **route Nyx's comms blackout (Ch21)**!
- **Catchphrases:**
  - *"Shh—don't step on the blue cable, that's carrying three floors of Meridian payroll and my lunch order."*
  - *"Hey, NULL-kid! You show up as `0x0000` on my scanner. Do you have ANY idea how cool that is?!"*
  - *(Ch16 reveal to Rook):* *"Wait—YOU'RE `@Null_Zero`?! You told me my haircut looked like a charged Voltorb!"* *"And I stand by it, Calder. Now plug in the drive."*
- **Banter Pairings:**
  - **Rook Calder:** Electric comedy-to-brotherhood arc! Rook is floored when he realizes his harsh anonymous chat-mod is a 16-year-old Nadir hacker who kept him sane after the Lowlight Shatter.
  - **Nyx Calloway:** Zed sells her scrubbed Spire memos in the Moon Market; he acts tough around everyone *except* Nyx, who makes him stutter with one raised eyebrow.
  - **Calla Wren:** Calla quietly leaves unencrypted Meridian memory-sticks taped beneath the Lumen Concourse vending machine for Zed to find.
  - **Mags Doyle (#3):** Mags bullies him into drinking water and threatens to confiscate his cyberdeck if he pulls three all-nighters in a row.

### Multi-Act Encounter & Battle Arc
- **Act I — Ch5 (Lumen Concourse Grate / Voltaic Sluiceworks, `180/584`):** Caught siphoning free current from a Meridian junction; challenges you to a "firewall test" on `:NEON_GRID` (Lv 25: **Porygon**, **Charjabug**, **Voltorb-Hisui**, **Sableye**).
- **Act II — Ch7 (Mirefen Roof-Relay, `220`):** Traces Sable's pirate broadcast back to an encrypted Meridian sub-carrier (first subtle technical clue that Sable = Meridian!). Optional battle on `:CORROSIVE_MIRE` / `:NEON_GRID` (Lv 35: **Porygon2**, **Charjabug→Vikavolt**, **Electrode-Hisui**, **Sableye**).
- **Act III — Ch12 (Skyreach Lower Gantries, `323`):** Works alongside DJ Chroma (#1) to bounce Larch's signal past Meridian's jammer.
- **Act IV — Ch16 (Cogsworth Canteen Alley, `400`):** Reveals himself as `@Null_Zero` to Rook and helps prep the Strade Works heist! Battle on `:FACTORY` (Lv 70: **Porygon2**, **Vikavolt**, **Electrode-Hisui**, **Mega Sableye**, **Rotom-Wash**, **Malamar**).
- **Act IV — Ch17 (Underveil Moon Market Signal-Den, `423`):** Runs Nadir's emergency mesh radio during the Sump Purge; intense battle on `:NEW_MOON` (Lv 75).
- **Ace Pokémon:** **Porygon2 ("Proxy")** (Eviolite Download/Trace tank!) & **Mega Sableye ("Trojan")** + **Hisuian Electrode ("Ping")** + **Vikavolt ("Overclock")**.
- **Field Specialty:** `:NEON_GRID` (deliberately triggers **Blackout** stage with Mud/Earthquake or abuses Conductors!) & `:NEW_MOON` & `:FACTORY`.
- **Repeatable Rematch Location & Rewards:** **Underveil Moon Market Signal-Den (`423`)** — *"Firewall Penetration Test"* repeatable battle awarding **Eviolite (★3 milestone), Upgrade, Dubious Disc, Ability Capsule, Synthetic Seeds, and Black-Market Tech TMs (Trick Room / Volt Switch / Taunt / Substitute)**!

### Codex Entry
- **Unlock Flag:** `codex_met(:ZED)` (Ch5 Lumen Sluiceworks/Concourse encounter)
- **Progressive Bio Beats:**
  1. *Beat 1 (Ch5):* Teenage Nadir Lattice-hacker who splices Zenith's power grid from beneath Lumen City. Fascinated by the PC's `NULL` scan signature.
  2. *Beat 2 (Ch16):* Revealed to be `@Null_Zero`, Rook Calder's sharpest livestream moderator. Helped clone the Strade Works keycards.
  3. *Beat 3 (Ch17):* Kept Underveil's emergency comms alive during Operation Clear Air and wired Nyx's Festival blackout relay.
- **Affinity Perks (0–5 ★):** ★2 unlocks **Black-Market Utility Shop** (cheap Bottle Caps, Power EV items, Ability Capsules); ★3 gifts **Eviolite**; ★5 unlocks **Zed & Rook Tag Exhibition** ("Stream Snipers") in Postgame!
- **`Portrait::CAST` & Audio:** `:ZED` (full 10-expression sheet) | `BattleBGM = Battle - Lattice Splicer` (glitch-hop cyber-synth breakbeat with crisp bass drops — pure instrumental!) | `Voice - Zed.ogg` (clean 8-bit-adjacent filtered synth-chirp — modern glitch, NOT Toby Fox chiptune!).

---

## 11. Lord Julian Montclair (Aristocratic Glass-Court Duelist — Pompous Rival with Genuine Redemption Arc)

- **Archetype:** Silver-Spoon Elowen Fencer-Rival → Disillusioned Noble → Mud-Stained Refugee Defender
- **Trainer Type ID & Bespoke Class:** `[SIDE_DUELIST]` → **`Glass-Court Duelist`** *(Acts I–III)* → shifts title in Codex/Act IV–V to **`Oathbound Duelist`** *(same type `[SIDE_DUELIST]` or versioned display!)*
- **Home Region / Span:** Elowen (Saltmere `140`, Highwold `603`, Verdance `285`, Cragholm `360`, Gloaming `841`, Crownhaven `499`) (Acts I–V)

### Visual Design Sheet
- **Core Concept:** *A flamboyantly pompous Elowen fencer-noble who treats the Festival like his birthright — until Prince Caedmon's betrayal strips away his illusions, leading him to tear up his silk coat into bandages and earn real knighthood in the mud.*
- **Unused Colour Pair:** **Royal Sapphire (`#1D3E8A`) + Champagne Gold (`#E6C97A`)**, accent **Crimson Silk (`#B8253A`)** sash. *(Visual Evolution Note for Act IV–V portrait/overworld variant: drops the gold-trimmed cape, jacket sleeves rolled up dusty, silk cravat tied around his Sirfetch'd's lance — and his Furfrou drops its pompous Royal Trim for tousled **Natural Trim**!)*
- **1× Silhouette:** Crisp dramatic aristocrat silhouette: half-cape flaring off one shoulder, absurdly tall sculpted blond hair-wave, and a gleaming silver **fencing foil** thrust diagonally forward like a lightning rod.
- **Iconic Prop:** A silver **monogrammed fencing foil** whose basket-hilt cradles a clipped Premier/Luxury Ball.
- **Pose & Face:** Classic sideways *en garde* lunge, foil tip aimed right at the player's nose, left hand arched pretentiously behind his head; chin tilted high, one sneering eyebrow raised in Acts I–II (shifting in Acts IV–V to a grounded, humble, fiercely determined squared-jaw gaze!).

### Personality, Catchphrases & Banter Pairings
- **Personality:** Channels the sharpest parts of *Reborn* **Fern**'s punchable early ego *fused with* *Rejuvenation* **Ren / Victoria**'s truly earned redemption arc! In Act I, Julian is hilariously unbearable (`"Unimprinted? How terribly quaint. My family has paid three Accord genealogists to verify our Meadow-blush!"`). He insists Meridian's Mandate is "good for commerce." Then Act III hits: Prince Caedmon sells out Elowen's forests in the Forest Compact, Directorate thugs beat Briarwick weavers right in front of Julian, and Queen Maelis is sidelined. Rather than doubling down into villainy, Julian snaps out of it: he pawns his family jewels to buy winter supplies for Cragholm's refugees, apologizes on one knee to **Juno** in Verdance, and fights beside you against Thornguard thugs at Gloamwood Verge (`841`)!
- **Catchphrases:**
  - *(Act I):* *"A colourless ferry stray entering the Festival? Please—at least iron your scarf before losing to me."*
  - *(Act III, rattled):* *"Prince Caedmon signed the Compact? Without the Queen? ...No, that's — that's not what nobility IS."*
  - *(Act IV, muddy in Cragholm):* *"I spent twenty years polishing a sword I never drew for anyone. Draw yours. Show me how a real knight fights."*
- **Banter Pairings:**
  - **Kestrel Vane:** Instant mutual loathing turned grudging respect! Kestrel calls him *"Ribbon-Boy"*; Julian calls Kestrel *"Four-Eels"*. By Ch20 Crownhaven, Julian quietly slips Kestrel a freshly ironed handkerchief before K8 and walks off without a word.
  - **Juno Hale:** He mocks her flower-girl dress in Ch2 Saltmere — then in Ch10/Act IV publicly apologizes and swears his sword to her Greenward bloc!
  - **Dorian Pell:** Dorian relentlessly critiques his posture (`"Too much wrist, Montclair! You look like a distressed heron!"`).

### Multi-Act Encounter & Battle Arc
- **Act I — Ch2 (Saltmere Promenade, `140`):** Scoffs at your Footlight Badge and demands a "proper gentleman's warm-up" on `:GRAND_STAGE` / `:BEACH` (Lv 16: **Farfetch'd-Galar**, **Furfrou (Debutante Trim)**, **Prinplup**).
- **Act II — Ch6 (The Highwold Crown Road, `603`):** Parading with a Meridian Mandate Pass, insists the Mandate keeps roads "tidy." Battle on `:MEADOW` (Lv 28–29: **Farfetch'd-Galar**, **Furfrou (Pharaoh Trim)**, **Prinplup**, **Karrablast**, **Ponyta-Galar**).
- **Act III — Ch10 (Verdance Briar Hall Upper Court, `285`):** Watches Prince Caedmon sneer at Elowen's refugees and hears Queen Maelis's cold truth; challenges you in a desperate identity-crisis duel on `:FLOWER_GARDEN` (Lv 46–47: **Sirfetch'd**, **Furfrou (Dandy Trim)**, **Empoleon**, **Escavalier**, **Rapidash-Galar**). Loses, drops his foil, and walks away silently.
- **Act IV — Ch14 (Cragholm Refugee Gallery, `360`):** **The Turn!** Found hauling water buckets with soot on his cheek and no cape; his **Furfrou is now in tousled Natural Trim**! Warm, earnest rematch on `:CRYSTAL_CAVERN` (Lv 63).
- **Act V — Ch18 (Gloamwood Verge, `841`):** **Redemption Payoff!** Stands shoulder-to-shoulder with you in a **Partner Tag Battle** against two Prince Caedmon Thornguard captains, then requests an honest **"Knight's Duel"** on `:FAIRY_TALE` (Lv 80: **Sirfetch'd**, **Empoleon**, **Escavalier**, **Rapidash-Galar**, **Furfrou-Natural**, **Ceruledge / Gallade** — let's use **Ceruledge** for blazing Sword/Knight Fairy Tale synergy!).
- **Act V — Ch20 (Crownhaven Court of Eight Pavilions, `499`):** Cheering wildly in the Unsworn section for the PC!
- **Ace Pokémon:** **Sirfetch'd ("Chevalier")** (Leek critical-hit monster!) + **Empoleon ("Sovereign")** + **Furfrou ("Velvet")** (visual Trim shift tracks his humility!).
- **Field Specialty:** `:FAIRY_TALE` (Knight/Blade/Steel/Fairy/Dragon boosts turn Sirfetch'd, Escavalier, Empoleon & Ceruledge into monsters!) & `:COLOSSEUM`.
- **Repeatable Rematch Location & Rewards:** **Verdance Royal Gallery (`288`)** / **Crownhaven Basilica Close (`483`)** — *"Honour Duel"* (Set style, no items) rewarding **Scope Lens, Leek, Razor Claw, King's Rock, Silver Bottle Caps, and Exp Candy L**.

### Codex Entry
- **Unlock Flag:** `codex_met(:JULIAN)` (Ch2 Saltmere encounter)
- **Progressive Bio Beats:**
  1. *Beat 1 (Ch2):* Third cousin to Briar Keep's court and self-proclaimed front-runner for the Boon. Insists his Furfrou has better pedigree than most Wardens.
  2. *Beat 2 (Ch10):* Shattered by Prince Caedmon's Forest Compact and Meridian's brutality in Briarwick. Abandoned his title to carry supplies to Cragholm.
  3. *Beat 3 (Ch18):* Stood down the Thornguard at Gloamwood Verge without a retinue or cape. Finally earned the knighthood he used to brag about.
- **Affinity Perks (0–5 ★):** ★2 unlocks **Free Furfrou Trim Salon** (any Trim on demand!) + **Scope Lens**; ★4 gifts a **Galarian Farfetch'd (Scrappy) with Leek**; ★5 unlocks **"Knights of the Fairy Tale"** Lv 94 Tag Rematch alongside Kestrel!
- **`Portrait::CAST` & Audio:** `:JULIAN` (full 10-expression sheet — smug early, humble/determined late!) | `BattleBGM = Battle - Glass-Court Duelist` (rapid violin-fencing duel concerto, noble & fierce — pure instrumental!) | `Voice - Julian.ogg` (crisp, theatrical tenor-rapier blip).

---

## 12. Madame Colette Lavigne (Wandering Pokémon Contest & Theatre Critic)

- **Archetype:** Withering Aesthetics Critic Who Ties Dorian, Tamsin, Kaito & the Grand Stage Together
- **Trainer Type ID & Bespoke Class:** `[SIDE_CRITIC]` → **`Grand Critic`** *(Name in battle: `Grand Critic Colette`)*
- **Home Region / Span:** Saltmere (`150/145`) → Briarwick (`130`) → Ironreach (`263`) → Crownhaven (`483`) (Acts I–V)

### Visual Design Sheet
- **Core Concept:** *Velmora's most feared arts-and-combat critic, who grades every gym battle, silk weave, and underground pit-fight out of five stars in her velvet opera ledger — and secretly bankrupts herself funding struggling artisans.*
- **Unused Colour Pair:** **Imperial Plum-Velvet (`#5E2363`) + Pearlescent Silver (`#DCE2EB`)**, accent **Gilded Opera-Brass (`#E0B84C`)**.
- **1× Silhouette:** Sweeping, high-fashion silhouette dominated by an **enormous tilted saucer-hat** sweeping diagonally over one eye with a curling moth-silk plume, draped in a billowing floor-length moth-silk stole.
- **Iconic Prop:** Long-handled **gold opera glasses** held loftily to her visible eye, and a ruby-tipped fountain pen hovering over a star-rated review card (`★★☆☆☆`).
- **Pose & Face:** Turned 3/4 aloofly away from the opponent, glancing sharply back over her fur-stole shoulder through her opera glasses while delicately balancing a Heal Ball on her fingertips; silver bob, haughty pursed lips, one imperiously arched brow.

### Personality, Catchphrases & Banter Pairings
- **Personality:** Sharp-tongued, hilariously pretentious on the surface, yet possessing an incorruptible eye for genuine soul. She is the glue tying together **three completely different Wardens**:
  - **Dorian Pell (Gym 1):** She gave Dorian's debut play *two stars* thirty years ago; he still recites her review from memory while weeping.
  - **Tamsin Loom (Gym 2):** Colette's signature moth-silk stole was woven by Old Mother Loom; Colette terrifies anxious Tamsin by showing up unannounced to commission twenty bolts of Briarwick silk at triple price (*"Don't cry, child, tears ruin the dye — and DO NOT tell anyone I paid retail!"*).
  - **Kaito Ren (Gym 8):** Colette attends illegal Ironreach pit-fights in full evening wear with opera glasses, writing glowing five-page reviews of Kaito's brawls as *"avant-garde kinetic tragedy"* — Kaito stares at her in total, silent bewilderment (`"Stand up. ...What is 'brachial pathos'?"`).
- **Catchphrases:**
  - *"Two stars. Pedestrian lead-in, vulgar item choice — and yet your partner's finale made my mascara run. Three and a half."*
  - *"Darling, a punch in a mine shaft and a pirouette in Saltmere are the SAME art form. Only the lighting differs."*
  - *(Ch20, Night of Masques):* *"Five stars, Dorian Pell. My first in forty years. Now bow before I change my mind."*
- **Banter Pairings:** Dorian, Tamsin, Kaito, **Ezra (#5)** (she immediately identifies his bow technique!), and **Ottilie (Elevated E11)** (Colette writes Ottilie's breakout glowing review!).

### Multi-Act Encounter & Battle Arc
- **Act I — Ch2 (Saltmere Pell Playhouse Lobby, `150`):** Critiques your Footlight Badge match right outside Dorian's auditorium; challenges you to a "Matinee Audition" on `:GRAND_STAGE` (Lv 16: **Feebas→Milotic? No, Lv 16: Glameow/Skitty/Buneary + Popplio/Snom** → **Buneary**, **Snom**, **Mienfoo**!).
- **Act I — Ch3 (Briarwick Loomhouse Lobby, `130`):** Inspecting Tamsin's weaves right after Gym 2; tests your Doubles choreography on `:SILKWOOD` (Lv 20: **Buneary**, **Frosmoth**, **Mienfoo**, **Ribombee** — yes, early-friendship Frosmoth showcase!).
- **Act II — Ch9 (Ironreach Iron Pit Gallery, `263`):** Sitting in the dusty pit-fighting bleachers in a velvet gown with opera glasses; tests your crowd-momentum mastery on `:COLOSSEUM` (Lv 42: **Milotic**, **Frosmoth**, **Mienshao**, **Lopunny**, **Brionne**).
- **Act V — Ch20 (Crownhaven Basilica Close, `483`):** After Dorian's *Gilded King*, invites you to a **"Command Performance"** exhibition on `:GRAND_STAGE` (Lv 87: **Milotic**, **Mega Lopunny**, **Mienshao**, **Frosmoth**, **Primarina**, **Cinccino**).
- **Ace Pokémon:** **Milotic ("Prima")** & **Mienshao ("Pirouette")** + **Mega Lopunny ("Ovation")** + **Frosmoth ("Velvet")**.
- **Field Specialty:** `:GRAND_STAGE` (explicitly punishes Protect/Recover stalling — calls you *"BORING!"* — and grants bonus rewards if you hit Standing Ovation Stage 3!), `:SILKWOOD`, `:COLOSSEUM`.
- **Repeatable Rematch Location & Rewards:** **Saltmere Lantern Theatre Balcony (`145`)** & **Crownhaven Basilica Close (`483`)** — *"Five-Star Critique Challenge"*: Colette grades your battle out of 5 Stars (no stall, field stage up, stylish finish!). 4–5★ awards **Prism Scale, Silk Scarf, Expert Belt, Choice Scarf, PP Ups, and massive prize money**!

### Codex Entry
- **Unlock Flag:** `codex_met(:COLETTE)` (Ch2 Pell Playhouse encounter)
- **Progressive Bio Beats:**
  1. *Beat 1 (Ch2):* Chief critic of *The Velmoran Review*. Feared by every playwright in Saltmere since giving Dorian Pell two stars thirty years ago.
  2. *Beat 2 (Ch9):* Secretly subsidizes Briarwick's looms through extravagant commissions and reviews Ironreach pit-fights as high ballet.
  3. *Beat 3 (Ch20):* Awarded Dorian's banned staging of *The Gilded King* her only five-star review in four decades — while Chancellor Hollis's guards stood ten feet away.
- **Affinity Perks (0–5 ★):** ★2 unlocks **Grand Stage Applause Tips** + free **Silk Scarf / Prism Scale**; ★4 unlocks **Style-Bonus Cash Multiplier** on all her rematches; ★5 unlocks **"The Five-Star Gala"** Double Battle (Colette & Dorian vs You & Juno/Kestrel)!
- **`Portrait::CAST` & Audio:** `:COLETTE` (full 10-expression sheet) | `BattleBGM = Battle - Grand Critic` (dramatic theatrical tango with snapping castanets & soaring strings — pure instrumental!) | `Voice - Colette.ogg` (sharp, clipped aristocratic alto-click blip).

---

## 13. Captain Orson "Deep-Bell" Falk (Retired Veteran Sea-Captain, Lore Keeper & Postgame Superboss)

- **Archetype:** Towering One-Eyed Isenmar Icebreaker Admiral, AF 290 Eyewitness & Optional Postgame Superboss
- **Trainer Type ID & Bespoke Class:** `[SIDE_CAPTAIN]` → **`Icebreaker Captain`** *(Name in battle: `Icebreaker Captain Orson`)*
- **Home Region / Span:** Saltmere Breakwater (`146`) → Gullcry/Ebbmouth (`561/167`) → Rimeholt (`303`) → The Drownings (`821`) → **Shardfall Isles (`905` Postgame Superboss!)**

### Visual Design Sheet
- **Core Concept:** *The retired one-eyed admiral who steered the last icebreaker fleet across the Hallow Strait before quarantine — hauls the salvaged brass fog-bell of his sunken flagship on his back like a tortoise shell and tests whether the next generation can weather the deep.*
- **Unused Colour Pair:** **Seafoam Pewter (`#5D7A7E`) + Patina-Brass (`#968B46`)**, accent **Coral-Red (`#D94B43`)** mooring rope.
- **1× Silhouette:** Massive sea-cliff broad-shouldered silhouette with a **huge curved brass ship's bell** strapped across his upper back forming an unmistakable dome-arch behind his head, flanked by a hooked whalebone gaff-staff.
- **Iconic Prop:** The salvaged **brass fog-bell of *The North Star*** (he strikes it with his knuckle before sending out his Ace!) and an engraved compass-rose **brass eyepatch** over his left eye.
- **Pose & Face:** Standing planted wide as a pier-piling against invisible gale winds, resting one huge weathered fist on his whalebone gaff while his other hand holds a Net Ball low by his hip; thick frost-white muttonchops, laughing crow's-feet around his sharp sea-blue eye, booming weathered grin.

### Personality, Catchphrases & Banter Pairings
- **Personality:** Warm, thunderous, gravelly old-salt mentor carrying three decades of maritime lore (*Reborn* **Samson / Hardy** jovial grit + *Pokémon* **Mr. Briney / Alder** veteran gravitas!). He isn't a Warden and turned down an Isenmar council seat twice (`"Chairs don't rock right, kid"`). He tells the player the *sailors' version* of Velmora's history: how in AF 290 the Hallow Strait flashed white at 23:40 and *the lamps of drowned Aurelia lit up under his keel*, how he pulled half the Ebbmouth fleet through Kyogre's swells, and how Edda Morrow was the only pilot crazy enough to out-sail him. In Postgame (`905` Shardfall Isles), he takes off his salt-coat, rings his fog-bell, and gives players a **genuine Lv 95–100 Optional Superboss** built around seamless 3-field weather mastery!
- **Catchphrases:**
  - *"Hear that bell, sprat? That's brass from thirty fathoms down. Means the tide's turning!"*
  - *"Edda Morrow still owes me a rudder from AF '88. Tell her I said her bowlines look like bird-nests!"*
  - *(Postgame Superboss intro, Shardfall Isles):* *"You beat the Crown, the Company, and the Sky. Good. Now let's see if you can beat the Sea!"*
- **Banter Pairings:**
  - **Captain Edda Morrow:** Old sea-partners who express deep affection exclusively through outrageous nautical insults (`"Orson, you barnacle-brained relic, get off my pier!"`).
  - **Marisol Reyes:** He sailed beside Marisol's late father and quietly guards the Ebbmouth picket line in Ch11 with his whalebone staff.
  - **Hesper Vane:** Friendly 40-year rivalry over whether Ferrow's lighthouse lens or Orson's old Gullcry fog-beacon saved more hulls.
  - **Anja Sorrel:** One of the very few Isenmar elders Anja listens to without saying `"Toes."`

### Multi-Act Encounter & Battle Arc
- **Act I — Ch2 (Saltmere Breakwater, `146`):** Leaning against the sea wall staring toward Aurelia's faint submarine glow; shares sailors' lore and offers a cheerful low-tide spar on `:BEACH` (Lv 16: **Skrelp**, **Spheal**, **Chinchou**).
- **Act I — Ch4 (Ebbmouth Mill Quay, `167`):** Listening to the stuttering river; warns you about the "Sleeping Whale" under the north ice! Optional spar on `:WATER_SURFACE` (Lv 23: **Skrelp**, **Sealeo**, **Lanturn**, **Dhelmise** [early preview!]).
- **Act III — Ch11 (Rimeholt Icewall Gate, `303` / Anchorhold `730`):** Hauls three stranded families out of the freezing Thaw water single-handedly! Optional bout on `:FROZEN_LAKE` (Lv 51: **Dhelmise**, **Walrein**, **Dragalge**, **Kingdra**, **Marshtomp→Swampert**).
- **Act IV — Ch17 (The Drownings, `821`):** Standing quietly beside the drained ribs of his old icebreaker *The North Star* (which surfaced when the Fault drained the south coast!); heartfelt bout on `:WATER_SURFACE` → `:UNDERWATER` (Lv 75: **Dhelmise**, **Walrein**, **Dragalge**, **Kingdra**, **Mega Swampert**, **Basculegion**).
- **Postgame — Shardfall Isles Old Beacon (`905`):** **OPTIONAL SUPERBOSS ("The Admiral of the Strait")!** Starts on `:WATER_SURFACE`, seamlessly weaponizes **Dive/Gravity → `:UNDERWATER`**, **Blizzard/Freeze-Dry → `:FROZEN_LAKE`**, and **Swift Swim Mega Swampert + Anchor Shot Dhelmise** (Lv 95 Standard / Lv 100 Hard; 2-bar boss Ace **Dhelmise "North Star"**!).
- **Ace Pokémon:** **Dhelmise ("North Star")** (the haunted anchor & helm of his own sunken flagship — 2× boosted Anchor Shot on `:UNDERWATER`!) + **Mega Swampert ("Icebreaker")** + **Basculegion ("Keel")** + **Walrein** + **Kingdra** + **Dragalge**.
- **Field Specialty:** **Tri-Sea Mastery** (`:WATER_SURFACE` ↔ `:UNDERWATER` ↔ `:FROZEN_LAKE`).
- **Repeatable Rematch Location & Rewards:** **Saltmere Breakwater Fog-Bell (`146`)** (Acts I–IV mid-game tiers) & **Shardfall Isles Old Beacon (`905`)** (Postgame Lv 100 Superboss!). Rewards: **Swampertite (or Mystic Water + Assault Vest if Swampertite is placed elsewhere), Deep Sea Tooth/Scale, Ability Patch (first Superboss win!), and Exp Candy XL**.

### Codex Entry
- **Unlock Flag:** `codex_met(:ORSON)` (Ch2 Saltmere Breakwater encounter)
- **Progressive Bio Beats:**
  1. *Beat 1 (Ch2):* Retired Isenmar icebreaker admiral carrying a salvaged ship's bell on his back. Old sailing partner and vocal critic of Captain Edda Morrow.
  2. *Beat 2 (Ch11):* Saved dozens during Rimeholt's Thaw and refused Thane Eirik's war commission. Believes the sea answers to no crown.
  3. *Beat 3 (Postgame):* Reunited with the hull of his flagship *The North Star* in the Drownings. Keeps watch at the Shardfall Isles beacon as Velmora's sea-tested superboss.
- **Affinity Perks (0–5 ★):** ★2 unlocks **Free Maritime Fast-Travel / Tide Tips** + **Mystic Water**; ★4 gifts a **Heavy-Ball Dhelmise/Basculin-White-Stripe egg**; ★5 unlocks **"Old Salts Tag Battle"** (Orson & Marisol vs You & Edda/Juno) + Superboss rematch!
- **`Portrait::CAST` & Audio:** `:ORSON` (full 10-expression sheet) | `BattleBGM = Battle - Icebreaker Captain` (booming sea-shanty brass, foghorn swells & accordion-fiddle storm tempo — pure instrumental!) | `Voice - Orson.ogg` (deep, gravelly bass foghorn-rumble blip).

---

## 14. Simeon Finch — *"Peddler Finch, the Silverer"* (Mysterious Mirror-Glass Peddler — Bleed & Ruin Route Foreshadower)

- **Archetype:** Creepy-Whimsical Wandering Antique-Mirror Merchant Who Reads Your Ledger & Bridges Normal and Ruin Routes
- **Trainer Type ID & Bespoke Class:** `[SIDE_PEDDLER]` → **`Mirror Peddler`** *(Name in battle: `Mirror Peddler Finch`)*
- **Home Region / Span:** Antumbra (exiled) — appears near Bleed Veils & mirrors across **All 8 Regions** + **Ruin Route (`960` Ledger Hall)**!

### Visual Design Sheet
- **Core Concept:** *An impossibly tall, grin-wide antique mirror-peddler pushing a velvet-draped handcart of pocket mirrors who sells forbidden curios, casually knows how many times you've died in the Ledger, and never quite casts a shadow in the right direction.*
- **Unused Colour Pair:** **Quicksilver Chrome (`#C8D3DC`) + Antique Ink-Black (`#14111A`)**, accent **Iridescent Prism-Crack (`#A87BFF` / `#66F0E0`)**.
- **1× Silhouette:** Tall, spindly storybook silhouette topped with a **crooked, backward-bent stovepipe hat**, long patchwork trench coat flaring wide open to show rows of dangling glinting hand-mirrors stitched to the inner lining!
- **Iconic Prop:** A **silvered mirror-glass half-mask** covering the left side of his face (literally reflecting a tiny glimpse of the PC's colours!), plus a rattling brass **flame-less lantern** that only shows fire in reflections.
- **Pose & Face:** Bowed deeply forward in an overly polite vaudeville-merchant flourish, extending an ornate cracked hand-mirror right toward the player's face while concealing a Premier/Dusk Ball behind his back; one impossibly bright silver eye smiling too wide beneath his crooked hat brim.

### Personality, Catchphrases & Banter Pairings
- **Personality:** Pure *Rejuvenation* **Madame X / Crescent / Puppet Master** eerie whimsy — *never* outright hostile, endlessly polite, weirdly fond of the PC, and chillingly meta-aware of Prismfall's **Ledger & Mirror Gag (`15_COMEDY.md` Gag #8 & `story/12_RUIN_ROUTE.md`)**! He sold **Hesper Vane** her cracked lighthouse mirror in Ch1 (`"She asked for one that shows the truth crooked. Best customer I ever had!"`). Dynamically reads `Prismfall::Ledger.game_overs_found.length` in dialogue (`"Zero cracks in your silvering? My, how careful!"` vs `"Twelve Game Overs?! Oh, darling, you're practically wholesale!"`). On the **Ruin Route (`story/12_RUIN_ROUTE.md`)**, when every friend recoils from you, Finch cheerfully flips his cart upside-down inside the **Ledger Hall (`960`)**, his mirror-mask cracks off revealing *empty reflections*, and he stays your sole loyal shopkeeper (`"Someone still has to sell Max Revives at the end of the world, dearie!"`).
- **Catchphrases:**
  - *"Fresh silvering, little traveller! Only lightly haunted — and no refunds past the Glass!"*
  - *"Careful now! Your shadow waved half a second late back there. ...Oh, don't fret, they get lonely."*
  - *(Ruin Route, Ledger Hall `960`):* *"Twenty-three graves and you STILL forgot to stock Full Heals? Come, come — Finch has you covered."*
- **Banter Pairings:**
  - **Celestine Aubade:** Celestine warns you away with precise phrasing: *"Finch sells true things facing the wrong way. Do not pay him in promises."*
  - **Archseer Imre Dask:** Exiled Finch from Lucent's Speculum twenty years ago for *"peddling unauthorized doorways to tourists."*
  - **Hesper Vane:** Old trading acquaintances — she keeps his cracked mirror hung inside Ferrow Lighthouse (`105`).
  - **The Reflection (Ruin Route):** The Reflection actively *hisses* at Finch (`"He knows where the hinges are."`).

### Multi-Act Encounter & Battle Arc
- **Act I — Ch1/2 (Windfall Row near Glassed Orchard `521`):** Non-combat introduction! Sells your first cheap **Elemental/Telluric/Synthetic/Magical Seeds** and mentions selling Hesper Vane her mirror.
- **Act I — Ch5 (Lumen Concourse Alley, `180`):** Eerily offers *"free glass-polish — you'll want it by tonight!"* right before the Gala Shatter.
- **Act III — Ch10 (Prism Falls Overlook, `681`):** Sells Evo Stones & remarks softly: *"Your reflection blinked after you did, dearie. Check a puddle in Skyreach."* (Directly foreshadows Ch12's cliffhanger!)
- **Act III — Ch13 (Glassmere Reading-Pool Jetty, `753`):** **First Optional Battle!** If you ask what's under his velvet tarp, he chuckles and tests you on `:INVERSE` (Lv 58: **Zoroark-Hisui**, **Cryogonal**, **Malamar**, **Banette**, **Bronzong**).
- **Act IV — Ch15 (Gravenmoor Fog-Lane, `380`):** Reads your live **Ledger Game-Over count** and gives a cryptic hint toward `GO_LOOKING_BACK` / Ruin Route (never spoils, purely atmospheric!).
- **Act V — Ch18 (Gloaming Lantern Market, `440`):** **Full Mirror-Duel!** Fights you on `:GLASS_DUNES` (Mirror Glass stage!) or `:INVERSE` (Lv 81: **Zoroark-Hisui**, **Mega Banette**, **Cryogonal**, **Malamar**, **Bronzong**, **Wobbuffet** [Mirror Coat/Counter mindgame!]).
- **Ruin Route — R1–R7 (The Ledger Hall, `960`):** Unlocks Finch's **"Inverted Emporium"** (sells Full Restores, Max Revives, Field Seeds, and rare TMs when normal shops reject the Renegade!).
- **Ace Pokémon:** **Hisuian Zoroark ("Quicksilver")** (Normal/Ghost = colourless + spectral — a literal mirror of the Unimprinted PC!) + **Cryogonal ("Pane")** + **Mega Banette ("Keepsake")** + **Malamar ("Widdershins")**.
- **Field Specialty:** `:INVERSE` & `:GLASS_DUNES` (**Mirror Glass** stage — beam ×1.5 + Mirror Coat/Reflect boosts!).
- **Repeatable Rematch Location & Rewards:** **Glassmere Reading-Pool Jetty (`753`)** & **Crownhaven Pilgrims' Quarter Curio Cart (`497`)** — *"Curio Wager"* battle on `:INVERSE` / `:GLASS_DUNES` rewarding **Mirror Herb, Clear Amulet, Focus Sash, Rare Candies, Bottle Caps, and rotating rare Evolutionary Items**!

### Codex Entry
- **Unlock Flag:** `codex_met(:FINCH)` (Ch1/2 Windfall Row encounter)
- **Progressive Bio Beats:**
  1. *Beat 1 (Ch1):* Eccentric antique-mirror merchant pushing a velvet-draped cart across Elowen. Sold Hesper Vane her cracked lighthouse mirror.
  2. *Beat 2 (Ch13):* Exiled from Antumbra by Archseer Dask for peddling unauthorized looking-glasses. Seems unnervingly aware of your Ledger.
  3. *Beat 3 (Ch18 / Ruin):* Neither Accord, Meridian, nor Hollow — merely a curator of spare reflections who keeps his shop open even at the end of the world.
- **Affinity Perks (0–5 ★):** ★2 unlocks **Finch's Rare Seed & Evo-Stone Cart**; ★3 gifts a **Mirror Herb + Clear Amulet**; ★5 unlocks **Ledger Hint Whispers** (atmospheric riddles hinting at unfound Game Overs without needing the postgame Ledger Lens!) + Lv 96 Inverse Rematch!
- **`Portrait::CAST` & Audio:** `:FINCH` (full 10-expression sheet — plus an eerie `cracked` expression for Ruin Route!) | `BattleBGM = Battle - Mirror Peddler` (creepy-whimsical music-box waltz transitioning into crooked reversed violins & harpsichord — pure instrumental!) | `Voice - Finch.ogg` (delicate crystalline glass-chime tinkling blip).

---

# Part 3: Dual Codex & Repeatable Cast Architecture

The creator specifically requested:
> *"and if they were not in the codex, make sure they are in there as repeatable cast"*

Because Prismfall has **both** a compiled Story Bible Web Codex (`dist_web/codex.html` built from `story/*.md` via `tools/build_codex.py`) **and** an in-game Cross-Save/Pause-Menu Ledger (`plugins/Prismfall Core/016_Ledger.rb` & `019_LedgerScene.rb`), we recommend wiring the Side Cast into **BOTH** cleanly:

### 3.1 Web Story Codex Integration (`story/03_CAST.md` + `tools/build_codex.py`)
1. Add a dedicated top-level section in `story/03_CAST.md` right after `## IMPORTANT SIDE CHARACTERS`:
   - `## RECURRING SIDE CAST & REPEATABLE RIVALS` — housing concise canon profiles for all **14 New Side Characters** + a cross-reference table of the **12 Elevated Trial/Quest Regulars** (marking `[Repeatable]` location & specialty).
2. Add a quick-filter pill (`Main Cast` / `Wardens` / `Recurring Side Cast` / `Factions`) to `tools/build_codex.py` when rendering `#cast` so readers can jump straight to repeatable allies and rivals.

### 3.2 In-Game Character Codex ("Cast Roll" inside `Prismfall Core`)
Rather than bloating switches (`FLAGS.md` S101–300 stays clean!), store Codex tracking in **`Prismfall.state.codex`** (per-save, mirroring `Prismfall.state.trials` and `Prismfall.state.narrative`):
```ruby
# Proposed schema inside Prismfall::SaveState (Prismfall Core)
# codex = {
#   :met       => { :CHROMA => true, :KAL => true, ... },
#   :stage     => { :CHROMA => 1..3, ... },       # unlocks progressive Bio Beats 1, 2, 3
#   :affinity  => { :CHROMA => 0..5, ... },       # 0..5 stars (separate from 10 main ending BONDS!)
#   :rematches => { :CHROMA => 4, ... },          # total repeatable battles won
#   :perk_got  => { :CHROMA => [2, 4], ... }      # claimed affinity milestone rewards
# }
```
- **Pause Menu / Ledger Access:** Add a **`Cast Roll` (Character Codex)** tab inside the Ledger / Pause Menu (alongside Game Overs, Endings, Cameos, and Field Notes!).
- **Each Codex Card Displays:**
  1. **96×96 Portrait** (`Graphics/Portraits/<ID>_happy.png` or `_neutral.png`) + **Class Title** (`Groove Monarch`, `Field Hunter`, etc.) + **Affinity Stars (`★★★☆☆`)**.
  2. **Progressive Bio Beats (1 / 2 / 3):** Beats unlock automatically as story flags or encounters progress — zero Act IV–V spoilers!
  3. **Signature Ace & Preferred Field:** e.g., `Ace: Ludicolo · Field: Grand Stage / Neon Grid`.
  4. **Live `"Currently Spotted / Rematch At"` Tracker:** Dynamically reads `$game_variables[101]` (`STORY_ACT`) so the player ALWAYS knows exactly where to walk/Fly for a repeatable rematch or hangout (e.g., `Ch2–11: Saltmere Promenade (140) → Ch17+: Underveil Studio (423)`).
  5. **Affinity Perk Status:** Shows unlocked perks (Move Tutors, BGM Jukebox, Stray Rummage Box, Mint Bar, Fossil Drops, Anvil Exp-Candy Drill).

### 3.3 Repeatable Rematch Scaling Convention (SPINE-Safe)
- **Scripted Story / Arc Encounters:** Use versions **`1` through `6`** (`[SIDE_HUNTER, Kal, 1]` … `[SIDE_HUNTER, Kal, 6]`), automatically inheriting Core's `+100` Hard / `+200` Casual offsets!
- **Repeatable Rematches:** Use reserved version band **`70–79`** (mirroring Trials' `50–99` band in `pbs/trainers_trials.txt`):
  - `70` = Act I–II Tier (Lv 25) · `71` = Act III Tier (Lv 50) · `72` = Act IV Tier (Lv 72) · `73` = Act V Tier (Lv 86) · `74` = Postgame Apex Tier (Lv 95–100).
  - A tiny helper `Prismfall::Codex.rematch_version` picks the highest tier `<= Prismfall.level_cap`, so every repeatable side-cast rematch stays fun, fair, and XP/candy-useful throughout the whole 18-gym run without breaking level caps!

---

# Part 4: Production-Ready Wiring Reference Tables

### 4.1 New `pbs/trainer_types.txt` Entries (14 New Side Cast + 7 Elevated Trial/NPC Classes)

| Trainer Type ID | Display Name (`Name =`) | Gender | BaseMoney | SkillLevel | Manifest `BattleBGM` | Notes |
|---|---|---|---:|---:|---|---|
| `[SIDE_GROOVE]` | `Groove Monarch` | Male | 80 | 100 | `Battle - Groove Monarch` | DJ Chroma ("Chroma-C.") — Doubles specialist |
| `[SIDE_HUNTER]` | `Field Hunter` | Female | 90 | 100 | `Battle - Field Hunter` | Kallista "Kal" Drayton — Field-transition specialist |
| `[SIDE_WILDCARD]` | `Sump Wildcard` | Female | 60 | 80 | `Battle - Sump Wildcard` | Mags Doyle — Scrapyard / Mire brawler |
| `[SIDE_INTERNS]` | `Meridian Interns` | Mixed | 50 | 64 | `Battle - Meridian Interns` | Bret & Sloane — Double battle duo |
| `[SIDE_CELLIST]` | `Rogue Virtuoso` | Male | 80 | 100 | `Battle - Rogue Virtuoso` | Ezra "Coda" Kovacs — Sound/Cello specialist |
| `[SIDE_PHOTOGRAPHER]` | `Rift Shutterbug` | Female | 65 | 80 | `Battle - Rift Shutterbug` | Willa "Snap" Quigley — Weather/Light explorer |
| `[SIDE_BOTANIST]` | `Tea Sommelier` | Male | 90 | 100 | `Battle - Tea Sommelier` | Gideon Hawthorne — Flower Garden / Tea specialist |
| `[SIDE_CARTER]` | `Bone Chronicler` | Female | 75 | 100 | `Battle - Bone Chronicler` | Zainab Darzi — Desert / Glass Dunes guild |
| `[SIDE_FORGEMASTER]` | `Iron Tutor` | Female | 85 | 100 | `Battle - Iron Tutor` | Master Magda Vorn — Move Tutor & Anvil Drill |
| `[SIDE_HACKER]` | `Lattice Splicer` | Male | 75 | 100 | `Battle - Lattice Splicer` | Zed "Static" Navarro — Neon Grid / New Moon tech |
| `[SIDE_DUELIST]` | `Glass-Court Duelist` | Male | 100 | 100 | `Battle - Glass-Court Duelist` | Lord Julian Montclair — Fairy Tale Knight |
| `[SIDE_CRITIC]` | `Grand Critic` | Female | 110 | 100 | `Battle - Grand Critic` | Madame Colette Lavigne — Grand Stage stylist |
| `[SIDE_CAPTAIN]` | `Icebreaker Captain` | Male | 120 | 100 | `Battle - Icebreaker Captain` | Captain Orson Falk — Postgame Tri-Sea Superboss |
| `[SIDE_PEDDLER]` | `Mirror Peddler` | Male | 100 | 100 | `Battle - Mirror Peddler` | Simeon Finch — Inverse / Mirror Glass enigma |
| `[SIDE_LAMPRUNNER]` | `Lamp-Runner` | Female | 55 | 64 | `Battle - Trainer` | Elevated **Pip Ore** (E1) |
| `[SIDE_FARMHAND]` | `Berry Farmer` | Male | 50 | 48 | `Battle - Trainer` | Elevated **Coll Hale** (E2) |
| `[TRIAL_SKALD]` | `Saga Skald` | Male | 70 | 80 | `Battle - Ace Trainer` | Elevated **Bersi Gullsong** (E3) |
| `[TRIAL_FIXER]` | `Sump Fixer` | Female | 80 | 100 | `Battle - Ace Trainer` | Elevated **Six-Fingers Ottoline** (E4) |
| `[SIDE_KIOSK]` | `Grant Kiosk` | Unknown | 75 | 100 | `Battle - Meridian` | Elevated **P-3NNY** Secret Diagnostic (E5) |
| `[TRIAL_MONK]` | `Quiet Way Keeper` | Female | 65 | 80 | `Battle - Ace Trainer` | Elevated **Sister Hollin** (E6) |
| `[TRIAL_LEGATE]` | `Crucible Legate` | Female | 100 | 100 | `War - Battlefield` | Elevated **Legate Varra Kosk** (E7) |
| `[NADIR_BARON]` | `Sump Baron` | Female | 100 | 100 | `Battle - Warden Nyx` | Elevated **Mother Gutter** (E12) |
| `[TRIAL_LECTOR]` | `Speculum Lector` | Female | 90 | 100 | `Battle - Ruin` | Elevated **Lector Saffi Ivarne** (E12) |
| `[ACCORD_CLERK]` | `Clerk-Superior` | Male | 95 | 100 | `Battle - Ace Trainer` | Elevated **Amadeus Fenwright** (E12) |

### 4.2 `Prismfall::Portrait::CAST` Additions (`plugins/Prismfall Cutscenes/014_Portraits.rb`)
- **14 New Recurring Cast (15 portrait IDs — Bret & Sloane separate):**
  `:CHROMA, :KAL, :MAGS, :BRET, :SLOANE, :EZRA, :WILLA, :GIDEON, :ZAINAB, :MAGDA, :ZED, :JULIAN, :COLETTE, :ORSON, :FINCH`
- **Elevated Minor Cast (21 portrait IDs — Pip/Hesper/Edda/Calla/Renata/Gutter/Vesper are already in `CAST`!):**
  `:COLL, :BERSI, :OTTOLINE, :PENNY, :TEASEL, :HOLLIN, :ALDRETH, :BRAKKA, :KOSK, :HALLORAN, :TAMM, :OTTILIE, :NELL, :NASRIN, :SAFFI, :FENWRIGHT` + the 8 Octave Choristers `:LYRA, :ARIA, :CADENCE, :SONA, :NOCT, :FORTE, :LENTO, :CAROL`

### 4.3 Audio Plan & Voice Blip Alignment (v4.3 Pure-Instrumental Standard)
- **Zero vocals, zero Toby Fox chiptune** — all 14 new `Battle - *` slots plug cleanly into `design/AUDIO_SOUNDTRACK_PLAN.md` (with immediate fallback to existing `Battle - Ace Trainer` / `Battle - Warden` manifest slots until custom tracks are mastered via `tools/audio/master_track.py`).
- **15 New Cast Voice Blips** (`Audio/SE/Voice - <Name>.ogg`, `56–74 ms`, `-19.5 LUFS`, `44.1 kHz` stereo Ogg q6) map 1-to-1 with `014_Portraits.rb`'s `VoiceTicker` hook:
  `Chroma, Kal, Mags, Bret, Sloane, Ezra, Willa, Gideon, Zainab, Magda, Zed, Julian, Colette, Orson, Finch`.

### 4.4 Chapter-by-Chapter Distribution Across Velmora (Zero Dead Stretches!)

| Act / Chapters | Kingdoms Visited | Active New Recurring Cast Beats | Elevated Regulars Highlighted |
|---|---|---|---|
| **Act I (Ch1–5)** | Elowen, Isenmar, Zenith | **Finch** (Ch1, Ch5), **Willa** (Ch1/2, Ch4), **DJ Chroma** (Ch2, Ch5), **Kal** (Ch2, Ch4), **Ezra** (Ch2), **Gideon** (Ch2), **Julian** (Ch2), **Colette** (Ch2, Ch3), **Orson** (Ch2, Ch4), **Bret & Sloane** (Ch3), **Magda** (Ch4), **Mags** (Ch5), **Zed** (Ch5) | Coll, Teasel, Hollin, Aldreth, Ottilie, P-3NNY, Bersi, Brakka, Lyra, Aria, Cadence |
| **Act II (Ch6–9)** | Ossaria, Nadir, Ashkaar | **Kal** (Ch6), **Bret & Sloane** (Ch6), **Gideon** (Ch6), **Zainab** (Ch6), **Julian** (Ch6), **Mags** (Ch7), **Ezra** (Ch7), **Willa** (Ch7), **Zed** (Ch7), **Magda** (Ch8), **Colette** (Ch9) | Sona, Noct, Forte, Ottoline, Kosk, Tamm, **Pip** (early Ironreach!), Nell |
| **Act III (Ch10–13)** | Elowen, Isenmar, Zenith, Antumbra | **Kal** (Ch10), **Gideon** (Ch10), **Julian** (Ch10), **Finch** (Ch10, Ch13), **Orson** (Ch11), **DJ Chroma** (Ch12), **Mags** (Ch12 save), **Bret & Sloane** (Ch12), **Willa** (Ch12), **Zed** (Ch12), **Ezra** (Ch13) | Halloran, Lento, Saffi Ivarne, Nasrin Vael |
| **Act IV (Ch14–17)** | Ossaria, Antumbra, Zenith, Nadir | **Kal** (Ch14), **Zainab** (Ch14), **Magda** (Ch14, Ch16), **Julian** (Ch14 turn), **Ezra** (Ch15), **Finch** (Ch15), **Bret & Sloane** (Ch16 resignation!), **Mags** (Ch16–17 save), **Zed** (Ch16–17), **Willa** (Ch16–17), **DJ Chroma** (Ch17), **Orson** (Ch17) | Pip (Cragholm), Tamm (Glasswake), Kosk (Siege Camp), Mother Gutter, Nell |
| **Act V (Ch18–21)** | Elowen, Ashkaar, Crownhaven | **Kal** (Ch18 final), **Gideon** (Ch18), **Julian** (Ch18 tag + Ch20), **Finch** (Ch18), **Zainab** (Ch19–20), **DJ Chroma** (Ch20), **Ezra** (Ch20 duet), **Colette** (Ch20 5★ review), **Bret & Sloane** (Ch20), **Mags** (Ch21 hijack float!) | Carol & full Octave Gauntlet, Ottilie (plays Maren!), Bersi (Saga of Glass Dunes), Fenwright |
| **Postgame & Ruin Route** | Shardfall Isles, Spire, Ledger Hall | **Captain Orson Falk** (Lv 100 Shardfall Isles Superboss!), **Kal** (6-Tier Field Gauntlets), **Magda** (Master Anvil Drills), **Finch** (Ruin Route Ledger Hall sole merchant!), **Tag Exhibitions** (Chroma+Rook, Zed+Rook, Ezra vs Vesper+Cadence, Colette+Dorian, Julian+Kestrel) | Nell (Concordance Spire desk), Fenwright (`CR_ACCORD_CHAMPIONS`), Octave individual/tag rematches |

---

## Suggested Implementation Priority (Phased Rollout)

1. **Wave 1 (Highest Immediate Charm — Acts I–II Impact):** Wire **DJ Chroma (#1)**, **Field Hunter Kal (#2)**, **Sump Wildcard Mags (#3)**, **Interns Bret & Sloane (#4)**, **Peddler Finch (#14)**, and elevate **Pip, Coll, Bersi, Ottoline, P-3NNY** — players will immediately feel Reborn/Rejuvenation side-cast electricity from Chapter 1 through Chapter 7!
2. **Wave 2 (Mechanical & Emotional Spine):** Add **Master Magda Vorn (#9)** (Move Tutors + Exp-Candy Anvil Drill!), **Willa Quigley (#6)** (EventMon/Field reward loop), **Zed Navarro (#10)** (Rook's chat-mod payoff), **Gideon Hawthorne (#7)** (Larch/Juno tea feud), and **Lord Julian Montclair (#11)** (multi-act redemption rival).
3. **Wave 3 (Deep Worldbuilding & Endgame Depth):** Add **Ezra Kovacs (#5)** (Octave ninth orphan), **Zainab Darzi (#8)** (Ossaria Bone-Carters' heart), **Madame Colette Lavigne (#12)** (Dorian/Tamsin/Kaito theatre critic), **Captain Orson Falk (#13)** (Postgame Tri-Sea Superboss), plus portraits/Codex entries for all 8 Eevee Octave choristers & Trial Keepers.
