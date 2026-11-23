# Pokémon Prismfall — Bespoke Trainer Classes, Expanded Cast, Story Rematches & Character Codex (Master Bundle)

**Status:** Proposal for Claude's Wednesday Sprint (and Gemini Art/Audio Follow-Up)  
**Scope:** Four tightly coordinated specifications answering the creator's Reborn/Rejuvenation character-depth directives:

| Spec File | Focus | Key Deliverable |
|---|---|---|
| [`CLASSES_PROPOSAL.md`](./CLASSES_PROPOSAL.md) | Bespoke Reborn-Style Trainer Classes & Evil-Org Depth | Moves all **18 Leaders** + **19 Named Rivals/Officers** off generic `"Warden"` / `"Hollow Keeper"` / `"Meridian Director"` (keeping `"Warden"` as institutional lore rank), upgrades `010_Bridge_VersusIntro.rb` to 2-line Class + Name splash, and adds **8 colorful named villain sub-bosses & 4th-power wildcards**. |
| [`SIDE_CAST_PROPOSAL.md`](./SIDE_CAST_PROPOSAL.md) | Memorable Side Cast & Recurring Rivals | Elevates **12 existing minor NPCs** (Pip, Coll, Bersi, Ottoline, P-3NNY, all 8 Octave Choristers, etc.) + introduces **14 original Reborn/Rejuv-energy recurring side characters** (`DJ Chroma`, `Kal Drayton`, `Mags Doyle`, `Meridian Interns`, `Ezra "Coda"`, `Willa "Snap"`, `Gideon Hawthorne`, `Zainab Darzi`, `Master Magda`, `Zed "Static"`, `Lord Julian`, `Madame Colette`, `Captain Orson`, `Simeon Finch`). |
| [`STORY_REMATCHES_PROPOSAL.md`](./STORY_REMATCHES_PROPOSAL.md) | Mid-Story Escalating Rematches & 4 Glass-Style Gauntlets | Fixes the audited 17/18 "1-and-done" Warden drop-off with **10 organic mid-story rematches (`M1–M10`, incl. Prof. Larch & Apprentice Wenlow)** + **4 signature Reborn Glass-Factory-tier gauntlets** (Ch13 Glass Court Refraction, Ch16 Nadir Siege, Ch19 War-Front + Voss/Quent Tag Boss, Ruin Route R4–R7 Oathbreakers' Last Stand) with 46 collision-free PBS blocks. |
| [`CODEX_SPEC.md`](./CODEX_SPEC.md) | In-Game `Prismfall::Codex` & Repeatable Cast Hub | Full `512×384` 4-tab People Directory (`027_Codex_Data.rb`, `028_Codex_Scene.rb`), unified `[L/R]` Field Notes Notebook hub, auto-discovery toasts, spoiler-free progressive bios, Ties Lantern + `:OPEN_BOOK` integration, **World Hangouts**, and **Lumen Battle Pavilion / Festival Training Court** (`029_Rematches.rb`) with `LevelCap`-scaled Singles/Doubles/2v2 Tag-Partner rematches. |

---

## Cross-Document Coordinator Reconciliations (Apply These Canonical Names/IDs!)

Because these four specs were drafted in parallel by specialist teams, use these **5 canonical reconciliations** so zero name or ID collisions enter `pbs/`, `story/`, or `plugins/`:

1. **`Sloane` Deduplication:** Keep **`Glassrunner` Sloane Vargo** (`ROGUE_SLOANE` in `CLASSES_PROPOSAL.md`) as the black-market Prism Cell smuggler; rename Meridian's junior intern in `SIDE_CAST_PROPOSAL.md` from `Intern Sloane Pendergast` → **`Intern Priya Pendergast`** (paired with `Intern Bret Halvorsen`).
2. **`Falk` Deduplication:** Keep **`Iconoclast` Cressida Falk** (`HOLLOW_FALK` in `CLASSES_PROPOSAL.md`) as the Hollow's Marrowgate survivor; rename the retired Isenmar admiral superboss in `SIDE_CAST_PROPOSAL.md` from `Captain Orson Falk` → **`Captain Orson "Deep-Bell" Krag`**.
3. **Ninth-Orphan / Octave Musician Differentiation:** Keep **`Dissonant` Scherzo** (`OCTAVE_SCHERZO` in `CLASSES_PROPOSAL.md`) as the mischievous **underground rival accompanist / Vesper's rogue foil** (Punk/Obstagoon trickster within the Octave faction), and keep **`Rogue Virtuoso` Ezra "Coda" Kovacs** (`SIDE_CELLIST` in `SIDE_CAST_PROPOSAL.md`) as a **former Prism Choir conservatory cellist** who defected from Crownhaven's Choir orchestra (no longer a duplicate "ninth Glassfall orphan" — they even share optional Ch20 banter!).
4. **Canonical Trainer Type ID for Wenlow & Prof. Larch:** Standardize on **`MEDIC_WENLOW`** (`Name = Ward Intern`, matching `CLASSES_PROPOSAL.md`) and **`PROFESSOR_LARCH`** (`Name = Field Scholar`, matching `STORY_REMATCHES_PROPOSAL.md` M5/R5).
5. **Canonical Codex Save Schema:** Use `CODEX_SPEC.md`'s **`Prismfall.state.codex`** (migrated cleanly in `002_SaveState.rb` with `Codex.sync_from_progress!(silent: true)` backfill) and store `STORY_REMATCHES_PROPOSAL.md`'s rematch tier counters (`:rematch_tier`, `:wins`, `:tag_wins`) directly inside each entry of `Prismfall.state.codex[:entries][id]`. Also rebuild the Web Story Bible Codex (`python3 tools/build_codex.py` → `dist_web/codex.html`) after adding the new cast to `story/03_CAST.md`!

---

## Recommended Rollout Order for Claude's Wednesday Sprint
1. **Quick High-Impact Win (~1 hour):** Apply the **37 bespoke Trainer Class renames** in `pbs/trainer_types.txt` + 2-line Class/Name VS splash in `010_Bridge_VersusIntro.rb` (`CLASSES_PROPOSAL.md` §4).
2. **Core Infrastructure:** Implement `Prismfall::Codex` (`027_Codex_Data.rb`, `028_Codex_Scene.rb`) + `Prismfall::Rematches` (`029_Rematches.rb`) + Lumen Battle Pavilion (`Map 940`) + `Prismfall::Gauntlet.run` helper (`CODEX_SPEC.md` & `STORY_REMATCHES_PROPOSAL.md`).
3. **Wave 1 Gameplay Content (Acts I–II + Ch13 Gauntlet):** Wire **M1–M4** (Teo, Tamsin, Dorian, Marisol), **G1** (Ch13 Glass Court Refraction Gauntlet), **Camille Ashe** (`MERIDIAN_ASHE`), **DJ Chroma**, **Kal Drayton**, **Mags Doyle**, **Meridian Interns**, and **Master Magda's Anvil Drill**!
4. **Wave 2–3 Full Cast & Late Gauntlets:** Wire remaining villain sub-bosses, recurring side cast, **M5–M10**, **G2–G4** (Nadir Siege, War-Front, Ruin Route R4–R7 Oathbreakers' Last Stand), and update `story/03_CAST.md` → `dist_web/codex.html`.
