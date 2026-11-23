# Bespoke Trainer Classes & Expanded Antagonist / Wildcard Roster Proposal

- **Date:** 2026-11-22
- **Author:** Gemini (Bespoke Trainer Classes & Faction Roster Architect)
- **Target Sprint:** Claude Wednesday Sprint (`pbs/trainer_types.txt`, `003_Badges_Gyms.rb`, `010_Bridge_VersusIntro.rb`, `014_Portraits.rb`, `025_CharsetAliases.rb`, `story/03_CAST.md` → `dist_web/codex.html`)
- **Creator Brief:**
  1. Replace generic `"Warden"`, `"Rival"`, `"Hollow Keeper"`, `"Meridian Director"`, and `"Octave Cantor"` battle classes with **bespoke, character-defining Reborn-style Trainer Classes** (`Firebug Charlotte`, `Keeper Saphira`, `Puppet Master Radomus`, `Showman Ciel`, `Seer Adrienn`).
  2. Expand Velmora's antagonist & wildcard cast beyond the core "Three Powers" leadership with **8 colorful, memorable sub-bosses, ideological foils, and 4th-power wildcards** (Reborn's Team Meteor / Rejuvenation's Team Xen roster energy).

---

## 1. The Reborn Split Convention (Zero Lore Breakage)

In *Pokémon Reborn*, NPCs, story dialogue, and League documents still call the 18 leaders **"Gym Leaders"** as an institutional office — *while* battle intros (`"You are challenged by Firebug Charlotte!"`), VS splashes, and character profiles display each person's **bespoke Trainer Class**.

Prismfall should adopt this exact two-layer split so **zero words of existing lore, dialogue, quests, or SPINE documentation break**:

| Layer | Where It Appears | What It Displays | Example (Dorian Pell) |
|---|---|---|---|
| **Institutional Office (Unchanged)** | Overworld dialogue, Accord treaties, story scripts (`story/01–32`), `"Warden's ring"`, `"Warden Circular"`, `"Ask your Warden"`, `GYMS[i][:warden]` metadata | **Warden** (and *Sovereign*, *Pallbearer*, *Director*, *Cantor*) | *"Saltmere's Normal Warden, Dorian Pell."* |
| **Bespoke Battle Class (Upgraded)** | `pbs/trainer_types.txt` (`Name =`), Battle Intro (`"You are challenged by <Class> <Name>!"`), EBDX VS Splash 2-line nameplate (`010_Bridge_VersusIntro.rb`), Trainer Card badge tooltip (`007_TrainerCard.rb`), Character Codex (`story/03_CAST.md` → `dist_web/codex.html`) | **Unique 1–2 word class (≤16 chars)** rooted in their exact craft, silhouette, or narrative hook | **`Pageant Master Dorian`** |

### Formatting & Width Guardrails
- **Hard Length Cap:** **≤16 characters** (1–2 words) for every single `Name =` entry. Our recommended slate tops out at **14 chars** (`Pageant Master`, `Lantern Priest`, `Null Architect`, `Hammer Captain`).
- **Battle Intro Box Fit:** `"You are challenged by <Class> <Name>!"` stays clean without awkward mid-name wraps (~38–42 char single-line comfort zone).
- **EBDX VS Splash Fit (`512×384`):** In `010_Bridge_VersusIntro.rb`, the top band runs `x = 18` to the foe bust's left edge (`FOE_BUST_CX - 128 = 264 px`), giving a **230 px safe horizontal runway**. At `pbSetSmallFont` (~10–12 px/char uppercase), 14 chars renders at **~155–168 px** — leaving **60+ px of breathing room** with zero overlap!
- **Suffix Variety Discipline:** No generic Pokémon classes (`Black Belt`, `Beauty`, `Scientist`, `Swimmer`) and no repetitive `-master`/`-keeper` spam across the 18 Wardens.

---

## 2. Bespoke Trainer Classes — Full Cast Upgrade

### A. The 18 Gym Leaders (`LEADER_DORIAN` → `LEADER_SIGRUN`, SPINE Rev 14 Order)

Every #1 pick below is verified against `story/03_CAST.md` and `pbs/trainers.txt` (`<Class> <PBS Name>`).

| # | Trainer Type ID | City · Type | **#1 Recommended Class** *(len)* | Battle Intro Preview | Runner-Up Alt 1 | Runner-Up Alt 2 | Lore Grounding (`story/03_CAST.md`) |
|---|---|---|---|---|---|---|---|
| 1 | `LEADER_DORIAN` | Saltmere · Normal | **`Pageant Master`** *(14)* | *Pageant Master Dorian* | `Matinee Idol` *(12)* | `Impresario` *(10)* | Literally the Accord's Pageant-Master; stages both the official *Prismfall Pageant* and the banned *Gilded King*. |
| 2 | `LEADER_TAMSIN` | Briarwick · Bug | **`Silkweaver`** *(10)* | *Silkweaver Tamsin* | `Loomkeeper` *(10)* | `Seamstress` *(10)* | Inherited Old Mother Loom's Briarwick looms; wears a moth-wing shawl & measuring tape; ace Leavanny on `:SILKWOOD`. |
| 3 | `LEADER_MARISOL` | Ebbmouth · Water | **`Union Boss`** *(10)* | *Union Boss Marisol* | `Dockmaster` *(10)* | `Tidebreaker` *(11)* | Only elected Warden (by the Ebb Guild); wears a union pin, leads the Ebbmouth strike, swears *"tides take it"*. |
| 4 | `LEADER_ROOK` | Lumen City · Electric | **`Holo-Idol`** *(9)* | *Holo-Idol Rook* | `Livestreamer` *(12)* | `Headliner` *(9)* | Face of every Meridian billboard in a holo-jacket with a streaming Rotom drone & punk-idol Toxtricity; blacks out Lumen in Act V. |
| 5 | `LEADER_SAHAR` | Duneholt · Ground | **`Archaeologist`** *(13)* | *Archaeologist Sahar* | `Relic Seeker` *(12)* | `Excavator` *(9)* | 40 years in the dunes; runs Duneholt's Dig Lab, uncovered the Aurel murals & reads Groudon's Unown glyphs; ace Claydol. |
| 6 | `LEADER_CORVIN` | Mirefen · Poison | **`Plague Doctor`** *(13)* | *Plague Doctor Corvin* | `Apothecary` *(10)* | `Toxicologist` *(12)* | Gaunt oilcloth coat & plague-doctor half-mask; runs Mirefen's Quiet Ward Infirmary (*"Don't worry. I'm a doctor."*). |
| 7 | `LEADER_BRANN` | Cindervault · Fire | **`Forgemaster`** *(11)* | *Forgemaster Brann* | `Hearthsmith` *(11)* | `Anvilguard` *(10)* | Braided-beard giant of Cindervault's Hearthguild forges; reset the Sovereign's Crown after AF 290; ace Coalossal. |
| 8 | `LEADER_KAITO` | Ironreach · Fighting | **`Pit Champion`** *(12)* | *Pit Champion Kaito* | `Gladiator` *(9)* | `Pit Fighter` *(11)* | Ex-Wardguard captain who has held Nadir's Iron Trial pit-fighting seat for nine years on `:COLOSSEUM`; ace Lucario. |
| 9 | `LEADER_JUNO` | Verdance · Grass | **`Bloomkeeper`** *(11)* | *Bloomkeeper Juno* | `Everbloom` *(9)* | `Petal Heir` *(10)* | Succeeds Rowan under Aunt Elin's Bride Tree and leads the Greenward bloc; marks her coming-of-age from `Flower Girl Juno`. |
| 10 | `LEADER_ANJA` | Rimeholt · Ice | **`Matriarch`** *(9)* | *Matriarch Anja* | `Icefisher` *(9)* | `Frostbreaker` *(12)* | Mamoswine-hide ice-fisher matriarch of Lake Rime; mirrors both her `03_CAST` bio and her ace Mamoswine ("matriarch of the herd"). |
| 11 | `LEADER_ODESSA` | Skyreach · Flying | **`Sky Courier`** *(11)* | *Sky Courier Odessa* | `Stormpilot` *(10)* | `Gale Captain` *(12)* | Aviator-goggled Captain of the Gale Post flying mail & refugees through the permanent Stormfront; ace Corviknight. |
| 12 | `LEADER_ILSA` | Lucent · Psychic | **`Provost`** *(7)* | *Provost Ilsa* | `Mindreader` *(10)* | `Archivist` *(9)* | Provost of the Lucent Athenaeum; cool, razor-precise academic robes & noise-cancelling earmuffs; ace Hatterene. |
| 13 | `LEADER_BASTIAN` | Cragholm · Rock | **`Prospector`** *(10)* | *Prospector Bastian* | `Deep Miner` *(10)* | `Delver` *(6)* | 74-year-old miner with headlamp & clay pipe sheltering fugitives in Cragholm's deep seams; ace Gigalith & Mega Aerodactyl. |
| 14 | `LEADER_YSOLDE` | Gravenmoor · Ghost | **`Lantern Priest`** *(14)* | *Lantern Priest Ysolde* | `Sexton` *(6)* | `Echo Medium` *(11)* | Directly echoes `01_WORLD_LORE` §7 (*"lantern-priests guide the dead"*); always carries a lit lantern in Gravenmoor's Cathedral; ace Chandelure. |
| 15 | `LEADER_MAGNUS` | Cogsworth · Steel | **`Artificer`** *(9)* | *Artificer Magnus* | `Industrialist` *(13)* | `Machinist` *(9)* | Pocket watch, self-built prosthetic hand, utilitarian ethic; subtly echoes the ancient Gilder artificers whose Engine he is rebuilding. |
| 16 | `LEADER_NYX` | Underveil · Dark | **`Shadow Broker`** *(13)* | *Shadow Broker Nyx* | `Moon Queen` *(10)* | `Spymaster` *(9)* | Silky information broker & de facto undercity queen of Nadir's Moon Court, trading secrets as currency; ace Zoroark. |
| 17 | `LEADER_CELESTINE` | Gloaming · Fairy | **`Oathbound`** *(9)* | *Oathbound Celestine* | `Dusk Oracle` *(11)* | `Storyteller` *(11)* | Gloaming's twilight oath makes it impossible for her to lie; guards the suppressed *Hymn of Return*; ace Sylveon + Mimikium Z Mimikyu. |
| 18 | `LEADER_SIGRUN` | Wyrmrest · Dragon | **`Valkyrie`** *(8)* | *Valkyrie Sigrun* | `Wyrmrider` *(9)* | `Dragonknight` *(12)* | Braided red crown, dragonhide armor, strongest Warden weighing challengers at the final gate; leads Wyrmrest's dragons over Crownhaven. |

---

### B. Rivals, Sovereign, Existing Evil-Org Officers & Special Cast (19 Identities)

Every generic `"Rival"`, `"Hollow Keeper"`, `"Meridian Director"`, `"Octave Cantor"`, and over-long legacy class is upgraded below while checking exact PBS names from `pbs/trainers.txt`.

| Trainer Type ID | Current `Name =` | PBS Name | **#1 Recommended Class** *(len)* | Battle Intro Preview | Runner-Up Alts | Lore / Mechanics Note |
|---|---|---|---|---|---|---|
| `RIVAL_KESTREL` | `Rival` | `Kestrel` | **`Fallen Heir`** *(11)* | *Fallen Heir Kestrel* | `Outcast` *(7)* · `Lone Blade` *(10)* | Hooks players from K1 on his mother Morwen's disgrace; pairs with his coat & ace Aegislash. |
| `RIVAL_JUNO` | `Rival` | `Juno` | **`Flower Girl`** *(11)* | *Flower Girl Juno* | `Field Aide` *(10)* · `Seedkeeper` *(10)* | Straight from `03_CAST` (*"the flower girl of a wedding that never ended"*); upgrades cleanly to `Bloomkeeper Juno` at Gym 9! |
| `CHAMPION_VALEN` | `Sovereign` | `Valen` | **`Sovereign`** *(9 — keep)* | *Sovereign Valen* | `Crownbearer` *(11)* · `Last Sovereign` *(14)* | Already bespoke to Prismfall (never vanilla `"Champion"`). Use `Crownbearer` if you want extra mythic weight. |
| `HOLLOW_MOURNER` | `The Mourner` | `Mourner` | **`Ash-Masked`** *(10)* | *Ash-Masked Mourner* | `Weeping Mask` *(12)* · `Hollow Voice` *(12)* | Fixes awkward `"The Mourner"` / `"Mourner"` VS duplication AND plants a sneaky fair clue to Rowan **Ash**by's ash-bark mask! |
| `LEADER_ROWAN` | `Gardener` | `Rowan` | **`Ash Gardener`** *(12)* | *Ash Gardener Rowan* | `Gardener` *(8 — keep)* · `Lantern Elder` *(13)* | Bridges his unmasked penitence (`Ash-Masked` → `Ash Gardener`) while honoring his Festival alias `"The Gardener"`. |
| `HOLLOW_WICK` | `Hollow Keeper` | `Wick` | **`Apostate`** *(8)* | *Apostate Wick* | `Heretic Priest` *(14)* · `Hollow Friar` *(12)* | Defrocked Prism Choir priest who authored the Wound Doctrine; crisp, liturgical, unforgettable. |
| `HOLLOW_THISTLE` | `Hollow Keeper` | `Thistle` | **`Threadcutter`** *(12)* | *Threadcutter Thistle* | `Spiteweaver` *(11)* · `Pallbearer` *(10)* | Dark mirror to `Silkweaver Tamsin`! Directly echoes her Saltmere rope-cutting & line *"I know where a thread will fall."* |
| `HOLLOW_TEO` | `Hollow Keeper` | `Teo` | **`Firebrand`** *(9)* | *Firebrand Teo* | `Tide Saboteur` *(13)* · `Cell Runner` *(11)* | Captures Marisol's fiery 19-year-old brother both as Ebbmouth's cell leader and later as a Lantern Hollow organizer. |
| `HOLLOW_SABLE` | `Hollow Keeper` | `Sable` | **`Platebreaker`** *(12)* | *Platebreaker Sable* | `Glassbreaker` *(12)* · `Demolitionist` *(13)* | Instantly separates the Hammer's Splitter-wielding extremist from Rowan's mourners — zero spoiler of her Meridian identity. |
| `MERIDIAN_VOSS` | `Meridian CEO` | `Aurelian` | **`Gilded Heir`** *(11)* | *Gilded Heir Aurelian* | `Concord CEO` *(11)* · `Arbiter` *(7)* | Only battled in Ch21 (4 chapters *after* his Ch17 House Aurel reveal!), making the title drop in the Hijack pure chills. |
| `MERIDIAN_MARCHETTI` | `Meridian Director` | `Helene` | **`Iron Marshal`** *(12)* | *Iron Marshal Helene* | `Mandate Chief` *(13)* · `Chief Enforcer` *(14)* | Ex-Wardguard military bearing; cold, competent commander of Meridian's Directorate enforcers. |
| `MERIDIAN_KROLL` | `Meridian Director` | `Sabine` | **`Infiltrator`** *(11)* | *Infiltrator Sabine* | `Special Ops` *(11)* · `Double Agent` *(12)* | Pays off her Ch13 unmasking from `Platebreaker Sable` → `Infiltrator Sabine` of Meridian Special Accounts. |
| `MERIDIAN_QUENT` | `Meridian R&D Head` | `Percival` | **`Null Architect`** *(14)* | *Null Architect Percival* | `Mad Savant` *(10)* · `R&D Director` *(12)* | Ties directly to Project NULL (Silvally) and the Arbiter Engine blueprints; trims current 17-char label to 14. |
| `MERIDIAN_ASHE` | `Meridian Director` | `Camille` *(new)* | **`Spin Doctor`** *(11)* | *Spin Doctor Camille* | `Media Mogul` *(11)* · `PR Director` *(11)* | **Activates the orphaned `MERIDIAN_ASHE` PBS slot** (`BALANCE.md:594`) as Meridian's PR head (see §3 #3)! |
| `OCTAVE_VESPER` | `Octave Cantor` | `Vesper` | **`First Voice`** *(11)* | *First Voice Vesper* | `Choirmistress` *(13)* · `Prism Cantor` *(12)* | Elevates Vesper as the ninth, undecided voice guiding the eight Choir orphans & their Eeveelutions. |
| `GILDED_THEODRIC` | `The Gilded King` | `Theodric` | **`Gilded King`** *(11)* | *Gilded King Theodric* | `Aureate King` *(12)* · `Chain-Forger` *(12)* | Drops awkward leading `"The"` so `"You are challenged by Gilded King Theodric!"` reads cleanly. |
| `ECHO_MORWEN` | `Echo of the Ghost Warden` *(24!)* | `Morwen` | **`Fading Echo`** *(11)* | *Fading Echo Morwen* | `Pale Echo` *(9)* · `Soul Echo` *(9)* | **Fixes 24-char VS-bar overflow** AND removes `"Warden"` from her battle class. |
| `ARCHSEER_DASK` | `Archseer` | `Imre` | **`Veiled Seer`** *(11)* | *Veiled Seer Imre* | `Archseer` *(8 — keep)* · `Mirror Seer` *(11)* | Ties directly to Antumbra's Veiled Synod & mirrored speech (`"Behind, welcome. Welcome, behind."`). |
| `MEDIC_WENLOW` *(new)* | *(none yet)* | `Wenlow` | **`Ward Intern`** *(11)* | *Ward Intern Wenlow* | `Infirmary Aide` *(14)* · `Apprentice` *(10)* | Gives Corvin's doomed apprentice a battle/Interlude IV/Codex identity (`014_Portraits.rb` already lists `WENLOW` in `CAST`). |

### C. Rank-and-File & Existing Minor Boss Polish (Kept Distinct from Named Bosses)

| Trainer Type ID | Current `Name =` | Recommended `Name =` *(len)* | Rationale |
|---|---|---|---|
| `HOLLOW_GRUNT` / `_M` / `_F` | `Hollow Acolyte` | **`Hollow Bereaved`** *(15)* *(or keep `Hollow Acolyte`)* | Matches `02_FACTIONS.md` L24 (*"Rank-and-file call themselves the Bereaved"*). |
| `HOLLOW_ADMIN` *(Brisk in Ch9)* | `Hollow Keeper` | **`Hammer Captain`** *(14)* | Currently used solely by `[HOLLOW_ADMIN,Brisk]` in Ch9 → reads *"Hammer Captain Brisk"*. |
| `MERIDIAN_AGENT` / `_M` / `_F` | `Meridian Agent` | **`Meridian Agent`** *(14 — keep)* | Clean rank-and-file identity. |
| `MERIDIAN_DIRECTORATE` *(Ostrander, Vell, etc.)* | `Directorate Captain` *(19!)* | **`Mandate Officer`** *(15)* | Trims 19-char label under the 16-char cap and grounds them in Act II–IV's Mandate. |
| `OCTAVE_SINGER` *(8 orphans)* | `Chorister` | **`Chorister`** *(9 — keep)* | Crisp contrast against Vesper's `First Voice`. |
| `REFLECTION` | `Reflection` | **`Mirror Self`** *(11)* *(or keep `Reflection`)* | Uncanny Ruin Route / Ch12 mirror payoff. |

> **Optional Bonus Polish — Sister-Game Cameos (`FESTIVAL_*`, `L315–393`):** Swap generic `Gym Leader` / `Champion` to their beloved home-game classes: `Bookworm Shelly`, `Punk Girl Venam`, `Knight Titania`, `Mermaid Amaria`, `Wandering Star Melia` *(or `Reserve Leader`)*, `Brawler Garret`, `Acting Champ Alexandra`, `Team Crescent Nova`, `Champion Lin`, `Champion Shiv`.

---

## 3. Evil Organization & Wildcard Roster Expansion (8 New Colorful Named Characters)

### Why Prismfall Needs These 8
*Pokémon Reborn*'s Team Meteor (Taka, ZEL, Sirius, Solaris, Blake, Ace, Aster & Eclipse) and *Rejuvenation*'s Team Xen (Madelis, Neved, Geara, Zetta, Nastasia, Clear & Kieran) feel electric because every organization contains **clashing egos, comedic oddballs, bitter internal rivalries, and rogue third-party spoilers** — not just solemn bosses flanked by nameless grunts.

Right now, Prismfall's antagonists skew heavily serious/tragic, Meridian's PR division literally has `—` in `02_FACTIONS.md`, the Prism Choir has no ideological foil, and Velmora's underworld & Wardguard have zero recurring named wildcard rivals. All 8 names below were **verified against the entire repository for zero collisions**, and every design strictly obeys `01_WORLD_LORE.md` (e.g., Choir Glass is never called a Plate shard; the PC's Legend splinter stays unique).

---

### THE HOLLOW (2 New Sub-Bosses: Theatrical Comic-Tragic Propagandist + Unhinged Marrowgate Radical)

#### 1. Gaspard Knell — `Bellringer Gaspard` (`HOLLOW_GASPARD`)
- **Role & Archetype:** Hollow Choir street-dirge director & melodramatic propagandist (*Reborn Taka / Ace* theatrical oddball energy).
- **Visual Silhouette:** Gaunt 25-year-old in a moth-eaten ex-Choir cassock stitched with miniature brass funeral bells, a cracked bark Ogre mask pushed up onto his forehead like goggles, lugging an oversized bronze handbell.
- **Personality & Faction Dynamics:** Treats every Hollow raid like an avant-garde funeral opera. Idolizes **The Mourner** as a tragic poet, drives **Thistle** insane during ops (*"Mara, darling, you can't cut a Lattice without a third-act dirge!"*), and **openly despises Sable** because Splitters ruin the acoustics (*"Explosives are vulgar! Grief should resonate, not rattle my molars!"*). Secretly hates actual bloodshed: after Ch5's Lowlight Shatter traumatizes him, his bravado cracks and he turns into a sheepish, darkly funny frenemy who leaks Hammer patrol routes in Act III before rallying under Rowan's Lantern Hollow in Act IV.
- **Chapter Appearances:**
  - **Ch2 (Saltmere):** Warm-up theatrical duel in the Lantern Theatre wings before the Mourner's Pageant hijack.
  - **Ch5 (Lumen City):** Pre-Gala rooftop distraction battle; horrified witness to Sable's Shatter.
  - **Ch10 (Verdance):** Comedic street-protest cameo getting chased by Queen Maelis's Thornguard.
  - **Ch14 (Cragholm):** Reformed Lantern Hollow ally & optional rematch in the deep seams.
- **Signature Team / Ace:** **Houndstone** *(Ace — `Last Respects` literally weaponizes grief for fallen allies!)*, **Chimecho**, **Brambleghast**, **Sinistcha**, **Mismagius**.
- **Codex Entry (`03_CAST.md`):**
  > **Gaspard Knell — `Bellringer` (`HOLLOW_GASPARD`):** A 25-year-old funeral director turned Hollow propagandist who insists every sabotage requires proper acoustics. He worships the Mourner's liturgy, drives Thistle to distraction, and detests Sable's explosives. Too tender-hearted for the Hammer's cruelty, he defects to Rowan's Lantern Hollow after the Lowlight Shatter—still ringing his brass bell, now to warn refugees instead of frighten crowds. **Ace: Houndstone.**

#### 2. Cressida Falk — `Iconoclast Cressida` (`HOLLOW_CRESSIDA`)
- **Role & Archetype:** Sable's unhinged Hammer prodigy & sole child survivor of the Quiet Town of **Marrowgate** (*Reborn Blake / Rejuv Geara* venomous wildcard-zealot).
- **Visual Silhouette:** 21, cropped platinum hair with faint crystalline Stage-1 Bleed freckles along one collarbone (worn uncovered like war paint), patched Nadir welding apron, cracked Hammer-sigil bark mask slung at her belt, tapping an iron tuning fork against glass.
- **Personality & Faction Dynamics:** Fiercely devoted to **Sable** as the only adult willing to *"actually smash the nails"* instead of singing sad songs. Mocks **Teo** as a *"harbor-boy playing rebel"* and **Gaspard** as a *"choirboy in a tablecloth"*. Holds a searing grudge against **Kaito Ren** — she recognizes his scar from the night his Wardguard unit sealed Marrowgate in AF 285. When Sable is exposed as Meridian's **Sabine Kroll** in Ch13, Cressida suffers a volcanic betrayal meltdown, disowns BOTH Meridian and Rowan, and goes rogue leading the last die-hard true-believer Hammer splinter in Act IV until the PC & Kaito confront her.
- **Chapter Appearances:**
  - **Ch7 (Mirefen):** Leads the Hammer squad that actually cuts the Gutterfall junction during the Ward Night (`26_SCRIPT_CH7` hook!).
  - **Ch9 (Ironreach):** Upper-ring ambush before the Conclave attack; recognizes Kaito across the pit.
  - **Ch13 (Lucent):** Confronts an unmasked Kroll in fury (if `IRONREACH_EVIDENCE` is presented).
  - **Ch16 (Nadir Sump Purge):** Chaotic three-way fight battling Meridian Directorate AND testing the PC's resolve.
- **Signature Team / Ace:** **Glimmora** *(Ace — crystalline toxic glass petals mirroring a Bleed-Fixed bloom!)*, **Weavile**, **Obstagoon**, **Salazzle**, **Skuntank**.
- **Codex Entry (`03_CAST.md`):**
  > **Cressida Falk — `Iconoclast` (`HOLLOW_CRESSIDA`):** Escaped the Quiet Town of Marrowgate as a child just before the Wardguard sealed the gate—and carries Stage-1 crystal freckles along her collarbone as proof. She idolized Sable's Hammer until Ch13 shattered that illusion, turning her into a bitter, dangerous rogue extremist who hates Meridian, the Accord, and Kaito Ren with equal fire. **Ace: Glimmora.**

---

### MERIDIAN CONCORD (2 New Sub-Bosses: PR Spin Doctor + Smug Corporate Hardware Prodigy)

#### 3. Director Camille Ashe — `Spin Doctor Camille` (`MERIDIAN_ASHE` — *activates orphaned PBS slot!*)
- **Role & Archetype:** Head of Meridian Public Relations (`"Light for Everyone"` campaign — fills the blank `—` row in `story/02_FACTIONS.md:79`) and narrative warlord (*Rejuv Cassandra / Madelis* razor-glam corporate villain).
- **Visual Silhouette:** 36, razor-sharp champagne-gold bob, tailored cream-and-gold Zenith power-blazer, amber smart-glasses, glowing holographic earpiece, and a Meridian slate flashing live public-approval charts mid-battle.
- **Personality & Faction Dynamics:** Bubbly, condescending, ruthlessly photogenic. Owns **Rook Calder's** billboard contract and treats him like depreciating inventory (*"Smile wider, Rook—your Q3 engagement dipped two points during that dreary Lowlight vigil"*). Orchestrates the **Larch smear campaign** in Ch12, pressures Elowen's Prince Caedmon into shuttering **Dorian's** Lantern Theatre, and trades icy boardroom daggers with **Director Marchetti** (*"Helene, darling, shooting civilians polls terribly—rebrand it 'Operation Clear Air'"*).
- **Chapter Appearances:**
  - **Ch5 (Lumen Gala):** Manages Rook & attempts to PR-spin the PC's survival after the Lowlight Shatter.
  - **Ch10 (Verdance):** Coaches Prince Caedmon's *"generous offer"* press conference outside the Heartgarden.
  - **Ch12 (Skyreach):** Boss battle outside Stormwatch Spire trying to confiscate the Larch Papers broadcast!
  - **Ch20 (Crownhaven Media Booth):** Flashy Festival battle trying to kill Dorian's *Gilded King* broadcast feed.
- **Signature Team / Ace:** **Espathra** *(Ace — runway silhouette + `Opportunist` literally hijacking the opponent's boosts + `Lumina Crash` weaponizing "Light for Everyone"!)*, **Oricorio (Pom-Pom)**, **Alolan Raichu**, **Pyroar**, **Klefki**.
- **Codex Entry (`03_CAST.md`):**
  > **Director Camille Ashe — `Spin Doctor` (`MERIDIAN_ASHE`):** Head of Meridian's "Light for Everyone" PR machine, Rook Calder's contractual handler, and the architect of the smear campaign against Professor Larch. Armed with polling data and blinding glamour, she believes any catastrophe is survivable if you own the cameras—and treats Marchetti's blunt force as a public-relations headache. **Ace: Espathra.**

#### 4. Cassian Penn — `Asset Hunter Cassian` (`MERIDIAN_CASSIAN`)
- **Role & Archetype:** Meridian Special Projects field-tester & smug Zenith trust-fund wunderkind (*Rejuv Kieran / Zetta* meets *Reborn Fern* punchable rival-exec).
- **Visual Silhouette:** 23, crisp white-and-brass Zenith jumpsuit worn half-unzipped over a black turtleneck, cyan diagnostic monocle, twin brass wrist-consoles streaming battle telemetry in real time.
- **Personality & Faction Dynamics:** **Dr. Quent's** insufferable protégé who secretly tries to steal credit for **Project NULL** — sparking a hilarious workplace cold war where Quent giggles sweetly while subtly sabotaging Cassian's field prototypes. Calls the PC `"Specimen Zero"` because of their `NULL` dock scan, and rages with petty jealousy when Voss gives **Kestrel** the Resonance Gauntlet in Act III (*"You handed MY firmware to a moody lighthouse orphan?!"*). Shaken when Ch16's Sump Purge shows him the bloody reality behind his "clean metrics," setting up a sharp late-game clash at the Meridian Black Site.
- **Chapter Appearances:**
  - **Ch6 (Duneholt Drill Site):** Oversees the aquifer pump & battles the PC to log `NULL` resonance data.
  - **Ch12 (Skyreach):** Sneers at Kestrel during the Gale Post raid.
  - **Ch14 (Cragholm Raid):** Vanguard double/solo clash ahead of Marchetti in the crystal galleries.
  - **Ch16 (Cogsworth / Black Site):** Guards Project NULL's logs using a prototype Resonance rig.
- **Signature Team / Ace:** **Vikavolt** *(Ace — floating railgun-battery powering his telemetry rig!)*, **Revavroom**, **Alolan Golem**, **Heliolisk**, **Porygon2**.
- **Codex Entry (`03_CAST.md`):**
  > **Cassian Penn — `Asset Hunter` (`MERIDIAN_CASSIAN`):** A 23-year-old Zenith prodigy and Dr. Quent's ambitious field-tester who treats Pokémon battles as live hardware benchmarks. Obsessed with the PC's `NULL` scan and furiously jealous of Voss sponsoring Kestrel over him, his smug corporate math collides head-on with reality during Operation Clear Air. **Ace: Vikavolt.**

---

### THE PRISM CHOIR / OCTAVE CHORUS (2 New Characters: Dogma Inquisitor + Runaway Musical Rival)

#### 5. Malachi Stern — `Choir Censor Malachi` (`OCTAVE_MALACHI`)
- **Role & Archetype:** Ice-cold Prism Choir inquisitor enforcing **Odo Prell's AF 140 Reform** (*Reborn El / Elias* terrifyingly polite religious zealot).
- **Visual Silhouette:** 48, tall and severe in ivory-and-gold Choir robes bordered with eighteen tiny stained-glass tiles around a blank silver clasp, swinging a brass censer chiming with tuned Choir-glass slivers.
- **Personality & Faction Dynamics:** Sincerely believes Velmora will descend into panic and ruin if anyone learns the Plates are *borrowed*. Personally drafted **Brother Wick's** excommunication, condescendingly polices **Vesper Lindqvist** and the **Eevee Octave** (*"Orphans fed on Choir bread should sing the Benediction, not fraternize in Nadir's mud"*), and hunts banned texts like **Dorian's** copy of *The Gilded King* and **Celestine's** Gloaming Liturgy. Clashes dramatically with **Hierophant Maud Ellery** in Act V when Maud finally hears the complete Hymn of Return and realizes Malachi kept it buried deliberately.
- **Chapter Appearances:**
  - **Ch2/3 (Saltmere → Briarwick):** Frosty cameo questioning Dorian after the Pageant hijack.
  - **Ch7 (Weeping Fen edge):** Hunts Brother Wick; optional/story duel if the PC blocks his arrest.
  - **Ch13 (Lucent Athenaeum):** Sits as Choir prosecutor at Rowan's tribunal; fights the PC to lock the Sealed Stacks.
  - **Ch18/20 (Gloaming / Basilica):** Final ideological duel trying to stop Celestine & Vesper from singing the full Hymn.
- **Signature Team / Ace:** **Armarouge** *(Ace — radiant stained-glass cathedral knight of the "Church of the First Light"!)*, **Sigilyph**, **Gothitelle**, **Absol**, **Altaria**.
- **Codex Entry (`03_CAST.md`):**
  > **Malachi Stern — `Choir Censor` (`OCTAVE_MALACHI`):** Guardian of the Benediction Doctrine and chief enforcer of Odo Prell's suppressed-scripture laws. Polite, chilling, and utterly convinced that Velmora's survival depends on silence, he excommunicated Brother Wick, polices Vesper's Eevee Octave, and hunts down anyone who dares sing the missing verses of the Hymn of Return. **Ace: Armarouge.**

#### 6. Scherzo — `Dissonant Scherzo` (`OCTAVE_SCHERZO`)
- **Role & Archetype:** Runaway "ninth-note" Glassfall orphan & flamboyant street-busker rival to the Eevee Octave (*Reborn DJ Arclight / Rejuv Ren* charismatic rogue-sibling energy).
- **Visual Silhouette:** 22, tattered Choir tunic cropped and dyed electric indigo into a punk street-jacket, fingerless gloves, cracked tuning-glass pendant bouncing on his chest, lopsided grin.
- **Personality & Faction Dynamics:** Grew up in Crownhaven's Glassfall orphanage right beside **Vesper** and the eight Octave singers, then bolted at 16 because *"singing pretty hymns to a cracked sky won't un-glass our parents."* Despite mercilessly teasing Vesper's *"goody-two-shoes pilgrimage,"* he secretly shadows all seven sibling singers across Velmora — crashing the PC's Octave encounters to test whether the PC is tough enough to look after his family, heckling **Choir Censor Malachi** on sight, and standing quietly in the back row at Ch20's Crownhaven gauntlet pretending he *"just happened to be in the neighborhood."*
- **Chapter Appearances:**
  - **Ch2 (Saltmere alley):** Appears right after Vesper's backstage duet, mocking the Octave's *"nice harmonies."*
  - **Ch5 (Lumen Lowlight):** Jamming beside Cadence's Jolteon before the Gala.
  - **Ch8 (Cindervault):** Secretly checks on Forte before Ashkaar's Legion; spontaneous sound-battle challenge!
  - **Ch20 (Crownhaven):** Pre-gauntlet rival warm-up (or optional post-gauntlet duet!).
- **Signature Team / Ace:** **Obstagoon** *(Ace — loud, theatrical anti-Choir punk rebel with `Obstruct` + `Parting Shot`!)*, **Exploud**, **Noivern**, **Toxtricity (Low Key)**, **Chatot**.
- **Codex Entry (`03_CAST.md`):**
  > **Scherzo — `Dissonant` (`OCTAVE_SCHERZO`):** The Glassfall orphan who walked out on the Prism Choir before taking an Eeveelution pilgrimage. A loudmouthed street-busker who mocks Vesper's devotion while secretly keeping watch over all eight Octave siblings from the shadows, testing any trainer bold enough to walk beside them. **Ace: Obstagoon.**

---

### INDEPENDENT / 4TH-POWER WILDCARDS (2 Recurring Spoilers Playing Outside the Three Powers)

#### 7. Sloane Vargo — `Glassrunner Sloane` (`WILDCARD_SLOANE`)
- **Role & Archetype:** Charming, amoral captain of **the Glassrunners**, Velmora's black-market Choir-glass, fossil, and contraband smuggling syndicate (*Rejuv Flora / Erin* swaggering wildcard rogue).
- **Visual Silhouette:** 32, weathered Ossarian caravan trench coat lined inside with glowing stolen Prism Cells, Synthetic Seeds, and tuned Choir-glass slivers (strictly street-tuned Z-glass per `01_WORLD_LORE` §3 — never claiming to be Plate shards!), brass goggles pushed up on dark wavy hair, rolling an Ossarian bone-token across her knuckles.
- **Personality & Faction Dynamics:** Pure chaotic-neutral profit! She fences tapped Meridian Prism Cells to Hollow cells, bribes **Prince-Elector Kassan's** desert customs agents, runs a lively rivalry with **Captain Edda Morrow** (*"Old Edda runs charity ferries; I run a business"*) and **Odessa Gale** (*"Gale Post delivers on time; Glassrunners deliver what's illegal"*), and pays tithes to **Nyx Calloway** — the one person in Velmora she refuses to cross. Offers the PC shady mid-game deals (rare seeds/items at steep ₽ or Accord-Standing cost) and, once defeated, canonically anchors **the Smugglers' Route over the Glassfall Scar** into Crownhaven on low-Accord runs (`02_FACTIONS.md:156`)!
- **Chapter Appearances:**
  - **Ch4 (Ebbmouth Cove):** Caught fencing tapped Meridian cells on the fogbound quay; cheeky first boss clash.
  - **Ch6 (Duneholt Bone Sands):** Races Sahar & the PC to an Ossarian fossil/relic cache.
  - **Ch14 (Ossaria Border):** Raids the Meridian war-convoy mid-crossing to loot Prism lances!
  - **Ch17 / Ch19 (Underveil / Glassfall Scar):** Final duel for a Drowned Crown relic — then guides low-Accord players over the Scar into Crownhaven.
- **Signature Team / Ace:** **Golisopod** *(Ace — `First Impression` ambush + `Emergency Exit` smoke-bomb getaway: the literal smuggler's playbook!)*, **Bombirdier**, **Scrafty**, **Perrserker**, **Dhelmise**.
- **Codex Entry (`03_CAST.md`):**
  > **Sloane Vargo — `Glassrunner` (`WILDCARD_SLOANE`):** Captain of the Glassrunners, a smuggling ring moving stolen Prism Cells, Ossarian fossils, and street-tuned Choir glass across Velmora's quarantine. Loyal only to profit (and terrified only of Nyx Calloway), she plays Meridian, the Hollow, and the kingdoms against one another—and knows the secret smuggler climb over the Glassfall Scar. **Ace: Golisopod.**

#### 8. Commander Cormac Greer — `Iron Sentinel Cormac` (`WILDCARD_CORMAC`)
- **Role & Archetype:** Hardline commander of **the Iron Watch**, a rogue traditionalist **Wardguard** splinter that rejects both Voss's corporate Mandate and Valen's "weakness" (*Reborn Titania + Rejuv Neved* grimly honorable fourth-axis rival).
- **Visual Silhouette:** 44, dented cobalt-and-silver Wardguard half-plate with the Accord emblem half-scratched and repainted in iron grey, scarred knuckles, cloak hemmed in Quiet-Town ash, stern hawkish eyes.
- **Personality & Faction Dynamics:** Served as **Kaito Ren's** second-in-command at **Marrowgate** in AF 285. Where Kaito shattered under guilt and quit to atone in Ironreach, Cormac turned to iron: *"Someone had to turn the lock, Kaito. You walked away and left me holding the key."* He despises **Marchetti** as a corporate mercenary (*"You sold a Wardguard's oath for a Zenith pension"*), crushes Hollow cells mercilessly, hijacks Meridian Lattice convoys just as brutally, and initially treats the **Unimprinted PC** as a dangerous anomaly to be contained — creating a gripping 4th-axis philosophical triangle between **Kaito, Marchetti, and Valen**. If beaten in Ch19/20 (and if `KAITO_TESTIFIED`), his Iron Watch veterans arrive in Ch21 to hold Crownhaven's outer gates against Meridian's Directorate!
- **Chapter Appearances:**
  - **Ch8 (Cindervault Road):** Intercepts both Hollow & Meridian supply wagons; challenges the PC for carrying Voss's badge case.
  - **Ch11/12 (Isenmar Border):** Enforces a brutal self-declared quarantine cordon against Thaw refugees; tense clash!
  - **Ch15 (Gravenmoor Road):** Raw reunion confrontation with Kaito & the PC over Marrowgate.
  - **Ch19/20 (Crownhaven Outer Gate):** Honorable final duel testing whether the PC has the backbone to walk into the Festival; unlocks Iron Watch aid during Ch21's hijack.
- **Signature Team / Ace:** **Ceruledge** *(Ace — vengeful sworn-blade knight fueled by Marrowgate's ghosts, directly mirroring Malachi's `Armarouge`!)*, **Bastiodon** *(the sealed gate)*, **Falinks** *(his old unit)*, **Sirfetch'd**, **Aggron**.
- **Codex Entry (`03_CAST.md`):**
  > **Commander Cormac Greer — `Iron Sentinel` (`WILDCARD_CORMAC`):** Kaito Ren's former second-in-command at Marrowgate and leader of the Iron Watch, a rogue Wardguard faction disgusted by Meridian's Mandate and the Accord's paralysis alike. Incorruptible, unforgiving, and haunted by the gates he sealed, he raids both Hollow cells and Meridian trucks—until a challenger proves mercy can still hold the line. **Ace: Ceruledge.**

---

### Roster Chemistry Web (At a Glance)

| New Character | Primary Foil / Rivalry | Secondary Tie-In | Comic / Dramatic Register |
|---|---|---|---|
| `Bellringer Gaspard` | Thistle (exasperated partner) · Sable (hates explosives) | Rowan (Lantern Hollow redemption) | Dark comedy → heartfelt redemption |
| `Iconoclast Cressida` | Kaito (Marrowgate grudge) · Kroll (Ch13 betrayal) | Teo & Gaspard (mocks both) | Volatile rage & tragic radicalism |
| `Spin Doctor Camille` | Rook (contract handler) · Marchetti (PR vs force) | Dorian & Larch (censorship/smear) | Razor-glam corporate satire |
| `Asset Hunter Cassian` | Quent (credit-stealing war) · Kestrel (gauntlet envy) | PC (`Specimen Zero` obsession) | Smug rival-exec / punchable genius |
| `Choir Censor Malachi` | Wick (excommunicator) · Maud Ellery (Ch20 schism) | Celestine, Dorian, Vesper | Ice-cold religious thriller |
| `Dissonant Scherzo` | Vesper (teasing older-brother energy) · Malachi (heckler) | All 8 Octave Choristers | Cocky musical rogue / hidden softie |
| `Glassrunner Sloane` | Edda & Odessa (legit vs illegal) · Nyx (pays tithes) | Kassan · Low-Accord Scar route | Charming chaotic-neutral swagger |
| `Iron Sentinel Cormac` | Kaito (Marrowgate twin) · Marchetti (sellout ex-peer) | Valen & Quiet Towns | Grim soldier's code / 4th-axis judge |

---

## 4. Exact Technical Wiring Plan for Claude (Wednesday Sprint)

### Step 1 — `pbs/trainer_types.txt` Exact `Name =` Patch Table

Apply these direct line edits to `pbs/trainer_types.txt` (then recompile PBS so `Data/trainer_types.dat` updates):

| Lines | Section ID | Old `Name =` | New `Name =` | Len |
|---|---|---|---|---|
| L7 | `[LEADER_TAMSIN]` | `Warden` | `Silkweaver` | 10 |
| L15 | `[LEADER_DORIAN]` | `Warden` | `Pageant Master` | 14 |
| L23 | `[LEADER_MARISOL]` | `Warden` | `Union Boss` | 10 |
| L31 | `[LEADER_ROOK]` | `Warden` | `Holo-Idol` | 9 |
| L39 | `[LEADER_SAHAR]` | `Warden` | `Archaeologist` | 13 |
| L47 | `[LEADER_CORVIN]` | `Warden` | `Plague Doctor` | 13 |
| L55 | `[LEADER_BRANN]` | `Warden` | `Forgemaster` | 11 |
| L63 | `[LEADER_KAITO]` | `Warden` | `Pit Champion` | 12 |
| L71 | `[LEADER_JUNO]` | `Warden` | `Bloomkeeper` | 11 |
| L79 | `[LEADER_ANJA]` | `Warden` | `Matriarch` | 9 |
| L87 | `[LEADER_ODESSA]` | `Warden` | `Sky Courier` | 11 |
| L95 | `[LEADER_ILSA]` | `Warden` | `Provost` | 7 |
| L103 | `[LEADER_BASTIAN]` | `Warden` | `Prospector` | 10 |
| L111 | `[LEADER_YSOLDE]` | `Warden` | `Lantern Priest` | 14 |
| L119 | `[LEADER_MAGNUS]` | `Warden` | `Artificer` | 9 |
| L127 | `[LEADER_NYX]` | `Warden` | `Shadow Broker` | 13 |
| L135 | `[LEADER_CELESTINE]` | `Warden` | `Oathbound` | 9 |
| L143 | `[LEADER_SIGRUN]` | `Warden` | `Valkyrie` | 8 |
| L152 | `[RIVAL_KESTREL]` | `Rival` | `Fallen Heir` | 11 |
| L160 | `[RIVAL_JUNO]` | `Rival` | `Flower Girl` | 11 |
| L169 | `[CHAMPION_VALEN]` | `Sovereign` | `Sovereign` *(keep; or `Crownbearer`)* | 9 |
| L178, L186, L194 | `[HOLLOW_GRUNT*]` | `Hollow Acolyte` | `Hollow Bereaved` *(optional lore sync)* | 15 |
| L202 | `[HOLLOW_ADMIN]` | `Hollow Keeper` | `Hammer Captain` | 14 |
| L210 | `[HOLLOW_WICK]` | `Hollow Keeper` | `Apostate` | 8 |
| L218 | `[HOLLOW_THISTLE]` | `Hollow Keeper` | `Threadcutter` | 12 |
| L226 | `[HOLLOW_TEO]` | `Hollow Keeper` | `Firebrand` | 9 |
| L234 | `[HOLLOW_SABLE]` | `Hollow Keeper` | `Platebreaker` | 12 |
| L242 | `[HOLLOW_MOURNER]` | `The Mourner` | `Ash-Masked` | 10 |
| L283 | `[MERIDIAN_MARCHETTI]` | `Meridian Director` | `Iron Marshal` | 12 |
| L291 | `[MERIDIAN_KROLL]` | `Meridian Director` | `Infiltrator` | 11 |
| L299 | `[MERIDIAN_ASHE]` | `Meridian Director` | `Spin Doctor` | 11 |
| L307 | `[MERIDIAN_VOSS]` | `Meridian CEO` | `Gilded Heir` | 11 |
| L397 | `[LEADER_ROWAN]` | `Gardener` | `Ash Gardener` | 12 |
| L405 | `[MERIDIAN_QUENT]` | `Meridian R&D Head` | `Null Architect` | 14 |
| L413 | `[MERIDIAN_DIRECTORATE]` | `Directorate Captain` | `Mandate Officer` | 15 |
| L421 | `[GILDED_THEODRIC]` | `The Gilded King` | `Gilded King` | 11 |
| L429 | `[ECHO_MORWEN]` | `Echo of the Ghost Warden` | `Fading Echo` | 11 |
| L445 | `[ARCHSEER_DASK]` | `Archseer` | `Veiled Seer` | 11 |
| L519 | `[OCTAVE_VESPER]` | `Octave Cantor` | `First Voice` | 11 |

#### New PBS Blocks to Append to `pbs/trainer_types.txt` (7 Net-New Cast + Optional Wenlow)
*(Reminder: `MERIDIAN_ASHE` already exists at `L298–304` — no duplicate block needed!)*

```ini
# --- Expanded Antagonist, Choir & 4th-Power Wildcard Cast (2026-11-22) ---
#-------------------------------
[HOLLOW_GASPARD]
Name = Bellringer
Gender = Male
BaseMoney = 80
SkillLevel = 100
BattleBGM = Battle Elite
VictoryBGM = Battle victory leader
#-------------------------------
[HOLLOW_CRESSIDA]
Name = Iconoclast
Gender = Female
BaseMoney = 80
SkillLevel = 100
BattleBGM = Battle Elite
VictoryBGM = Battle victory leader
#-------------------------------
[MERIDIAN_CASSIAN]
Name = Asset Hunter
Gender = Male
BaseMoney = 80
SkillLevel = 100
BattleBGM = Battle Elite
VictoryBGM = Battle victory leader
#-------------------------------
[OCTAVE_MALACHI]
Name = Choir Censor
Gender = Male
BaseMoney = 100
SkillLevel = 100
BattleBGM = Battle Elite
VictoryBGM = Battle victory leader
#-------------------------------
[OCTAVE_SCHERZO]
Name = Dissonant
Gender = Male
BaseMoney = 80
SkillLevel = 100
BattleBGM = Battle Gym Leader
VictoryBGM = Battle victory leader
#-------------------------------
[WILDCARD_SLOANE]
Name = Glassrunner
Gender = Female
BaseMoney = 100
SkillLevel = 100
BattleBGM = Battle Elite
VictoryBGM = Battle victory leader
#-------------------------------
[WILDCARD_CORMAC]
Name = Iron Sentinel
Gender = Male
BaseMoney = 100
SkillLevel = 100
BattleBGM = Battle Gym Leader
VictoryBGM = Battle victory leader
#-------------------------------
[MEDIC_WENLOW]
Name = Ward Intern
Gender = Male
BaseMoney = 40
SkillLevel = 64
BattleBGM = Battle trainer
VictoryBGM = Battle victory trainer
```

---

### Step 2 — `plugins/Prismfall Core/003_Badges_Gyms.rb` (and `007_TrainerCard.rb` / `025_CharsetAliases.rb`) Display Check

1. **`003_Badges_Gyms.rb` — ALREADY CLEAN (Zero Hardcoded `"Warden"` Strings!):**
   - Audited lines 1–143: `Prismfall.gym_battle(n)` (L122–139) passes `g[:trainer_type]` and `g[:trainer_name]` straight to `TrainerBattle.start` / `Prismfall::Rival.battle`.
   - Updating `pbs/trainer_types.txt` immediately changes every Gym battle intro to `"You are challenged by Pageant Master Dorian!"`, `"Plague Doctor Corvin!"`, `"Valkyrie Sigrun!"`, etc.
   - **Optional convenience helper** to add right after `gym_for_trainer_type` (L71) so Trainer Card, Quest Log, and Debug Menu can display bespoke titles cleanly:
     ```ruby
     # Returns e.g. "Pageant Master Dorian" from compiled TrainerType data.
     def self.gym_display_title(n)
       g = gym(n)
       return "" if !g
       tt = GameData::TrainerType.try_get(g[:trainer_type])
       cls = tt ? tt.name : "Warden"
       return "#{cls} #{g[:trainer_name]}"
     end
     ```
2. **`007_TrainerCard.rb` (Optional Enhancement):**
   - Currently renders only the 2×9 badge icon grid (`draw_badges`, L37–60) without per-badge captions. If a badge-inspector overlay is added later, pull `Prismfall.gym_display_title(i + 1)` so owned badges show `Pageant Master Dorian · Saltmere` instead of `Warden Dorian`.
3. **`025_CharsetAliases.rb` — Dedup Check & New `NAME_ALIASES`:**
   - **Verified L54–62 (`Trainer#full_name`):** Deduplicates `tn.end_with?(name)`. With `HOLLOW_MOURNER` set to `Name = Ash-Masked` and PBS trainer name `Mourner`, `full_name` cleanly outputs `"Ash-Masked Mourner"` (and still protects against double-Mourner if an alt ending in `"Mourner"` is ever chosen).
   - Add to `NAME_ALIASES` (`L21–28`) once sprites land:
     ```ruby
     "Gaspard" => "GASPARD", "Cressida" => "CRESSIDA", "Camille" => "ASHE",
     "Ashe" => "ASHE", "Cassian" => "CASSIAN", "Malachi" => "MALACHI",
     "Scherzo" => "SCHERZO", "Sloane" => "SLOANE", "Cormac" => "CORMAC",
     "Wenlow" => "WENLOW"
     ```

---

### Step 3 — `plugins/Prismfall EBDX Bridge/010_Bridge_VersusIntro.rb` Banner Width Audit & 2-Line Nameplate Upgrade

#### Exact Pixel-Width Audit
- **Screen:** `512 × 384`. Top band (`@top`): `Viewport.new(0, 40, 512, 136)` (`TOP_Y = 40`, `BAND_H = 136`).
- **Foe Bust (`@s["bustT"]`):** `256 × 136` centered at `FOE_BUST_CX = 392` → **left edge = `264 px`** (`z = 5`).
- **Ghost Echo (`@s["ghostT"]`):** `opacity = 58` additive at `z = 3` (decorative backdrop beneath text at `z = 8`).
- **Nameplate Origin:** `x = 18`, `y = 8`, left-aligned (`z = 8`).
- **Clean Non-Overlapping Runway:** `264 - 18 = 246 px` → **`230 px` strict safe budget** (16 px breathing margin before bust edge).
- **Longest Bespoke Class in Proposed Slate:** `14 chars` (`Pageant Master`, `Lantern Priest`, `Null Architect`, `Hammer Captain`) / `15 chars` (`Hollow Bereaved`, `Mandate Officer`).
  - At `pbSetSmallFont` (~18–20 px, ~10–12 px/char uppercase): `14 chars ≈ 154–168 px` (**62+ px clear of the bust!**).
  - At `16 chars` (hard cap): `≈ 176–192 px` (**38+ px clear of the bust!**).
  - **Bug fixed by this proposal:** Old `ECHO_MORWEN` (`Echo of the Ghost Warden` = 24 chars ≈ `275 px`) would have **clipped straight across Morwen's bust**; `Fading Echo` (11 chars ≈ `125 px`) fixes it completely.

#### Recommended 2-Line B2W2/Reborn Nameplate Upgrade (`010_Bridge_VersusIntro.rb` L187 & L293–305)
Currently L187 renders **only** `@trainer.name.to_s` — hiding every bespoke Trainer Class on the VS screen! Upgrade `name_sprite` to render a crisp **Class Eyebrow + Bold Name** stack with automatic width clamping:

```ruby
# L187: pass opponent trainer class as eyebrow subtitle (guard against Mourner/Mourner duplication)
foe_name = @trainer.name.to_s
foe_cls  = (@trainer.trainer_type_name rescue "").to_s
foe_cls  = "" if !foe_name.empty? && foe_cls.downcase.end_with?(foe_name.downcase)
@s["nameT"] = name_sprite(@top, foe_name, 18, 6, :left, subtitle: foe_cls, max_w: 230)
@s["nameB"] = name_sprite(@bot, ($player ? $player.name : ""), w - 18, BAND_H - 46, :right)
```

```ruby
# L293-305: two-line nameplate with auto-shrink guard so no class can ever clip the foe bust
def name_sprite(vp, text, x, y, align, subtitle: "", max_w: 230)
  has_sub = !subtitle.to_s.empty?
  s = Sprite.new(vp); s.bitmap = make_bmp(Graphics.width, has_sub ? 66 : 44); s.z = 8
  if has_sub
    pbSetSmallFont(s.bitmap)
    s.bitmap.font.bold = true
    sub = subtitle.to_s.upcase
    while s.bitmap.text_size(sub).width > max_w && s.bitmap.font.size > 12
      s.bitmap.font.size -= 1
    end
    pbDrawTextPositions(s.bitmap, [
      [sub, x + 1, 5, align, Color.new(10, 10, 18, 180), Color.new(10, 10, 18, 180)],
      [sub, x,     4, align, Color.new(248, 224, 144), Color.new(20, 20, 34), :outline]
    ])
  end
  pbSetSystemFont(s.bitmap)
  s.bitmap.font.size += 6
  s.bitmap.font.bold = true
  while s.bitmap.text_size(text).width > max_w && s.bitmap.font.size > 18
    s.bitmap.font.size -= 1
  end
  ny = has_sub ? 26 : 6
  pbDrawTextPositions(s.bitmap, [
    [text, x + 2, ny + 2, align, Color.new(10, 10, 18, 190), Color.new(10, 10, 18, 190)],
    [text, x,     ny,     align, Color.new(252, 252, 255), Color.new(24, 24, 38), :outline]
  ])
  s.y = y
  return s
end
```

#### `VS_IDS` & `THEMES` Additions (`010_Bridge_VersusIntro.rb` L28–53)
*(Combine with Art Drop 13's `SABLE`/`KROLL`/`MARCHETTI`/`QUENT`/`THISTLE`/`VESPER` patch!)*
```ruby
# Add to VS_IDS (critical for PBS first-name -> cast-ID resolution):
:HOLLOW_WICK      => "WICK",
:HOLLOW_TEO       => "TEO",
:LEADER_ROWAN     => "ROWAN",
:ARCHSEER_DASK    => "DASK",
:GILDED_THEODRIC  => "THEODRIC",
:ECHO_MORWEN      => "MORWEN",
:MERIDIAN_ASHE    => "ASHE",       # PBS name "Camille"
:HOLLOW_GASPARD   => "GASPARD",
:HOLLOW_CRESSIDA  => "CRESSIDA",
:MERIDIAN_CASSIAN => "CASSIAN",
:OCTAVE_MALACHI   => "MALACHI",
:OCTAVE_SCHERZO   => "SCHERZO",
:WILDCARD_SLOANE  => "SLOANE",
:WILDCARD_CORMAC  => "CORMAC",

# Add to THEMES:
"WICK" => :green, "TEO" => :blue, "DASK" => :violet, "THEODRIC" => :gold, "MORWEN" => :violet,
"ASHE" => :gold, "GASPARD" => :green, "CRESSIDA" => :violet, "CASSIAN" => :blue,
"MALACHI" => :gold, "SCHERZO" => :violet, "SLOANE" => :red, "CORMAC" => :grey
```

---

### Step 4 — `plugins/Prismfall Cutscenes/014_Portraits.rb` (`CAST` & Registrations) & Character Codex

1. **`014_Portraits.rb` (`CAST`, L86–96):**
   - `WENLOW` is **already present** on L95!
   - Append a new line to `CAST` for the 8 expanded cast members (+ existing minor bosses `BRISK` and `CAEDMON` so Ch9/Ch10 scripts can show their faces once art lands):
     ```ruby
     GASPARD CRESSIDA ASHE CASSIAN MALACHI SCHERZO SLOANE CORMAC
     BRISK CAEDMON
     ```
   - Optional `Portrait.register` calls below `CAST` so `"Camille:"` and `"Ashe:"` both resolve to `:ASHE`:
     ```ruby
     Portrait.register(:ASHE,     name: "Camille",  trainer: :MERIDIAN_ASHE)
     Portrait.register(:GASPARD,  name: "Gaspard",  trainer: :HOLLOW_GASPARD)
     Portrait.register(:CRESSIDA, name: "Cressida", trainer: :HOLLOW_CRESSIDA)
     Portrait.register(:CASSIAN,  name: "Cassian",  trainer: :MERIDIAN_CASSIAN)
     Portrait.register(:MALACHI,  name: "Malachi",  trainer: :OCTAVE_MALACHI)
     Portrait.register(:SCHERZO,  name: "Scherzo",  trainer: :OCTAVE_SCHERZO)
     Portrait.register(:SLOANE,   name: "Sloane",   trainer: :WILDCARD_SLOANE)
     Portrait.register(:CORMAC,   name: "Cormac",   trainer: :WILDCARD_CORMAC)
     ```
2. **Character Codex (`story/03_CAST.md` → `tools/build_codex.py`):**
   - Update each Warden & officer heading in `story/03_CAST.md` to display their bespoke class badge (e.g., `### 1. Dorian Pell — Pageant Master — Normal — Saltmere — LEADER_DORIAN — :GRAND_STAGE`), append the 8 new cast entries above (and fill in `Director Camille Ashe` in `story/02_FACTIONS.md:79`), then run `python3 tools/build_codex.py` to refresh `dist_web/codex.html`.
