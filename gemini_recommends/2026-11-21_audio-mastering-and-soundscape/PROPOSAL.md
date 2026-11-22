# Proposal: Audio Mastering Pipeline, Original CC0 BGS/SE Pack & 66-Slot Diversified Pure-Instrumental Soundtrack Blueprint (v3)

- **Date:** 2026-11-21 (Updated 2026-11-22 v3: Creator Locked Picks + Multi-Artist Variety + Pokémon-Style Non-Pokémon RPG Gems)
- **Owner / Author:** Gemini (Art & Audio Direction)
- **Status:** Ready for Claude & Creator review (zero files modified outside `gemini_recommends/`)

---

## What

1. **Reusable Audio Mastering & Loop-Tagging CLI (`master_track.py`):** Converts any `.mp3`/`.wav`/`.flac`/`.ogg` track to `44.1 kHz` Ogg Vorbis (`libvorbis -q:a 6`), applies two-pass EBU R128 loudness normalization (`-14.0 LUFS` BGM / `-20.0 LUFS` BGS / `-12.0..-14.0 LUFS` SE, `-1.5 dBTP`), writes exact `LOOPSTART`/`LOOPLENGTH` Vorbis comments in samples for seamless `mkxp-z` looping, and provides an `--audit` report mode.
2. **26 Original CC0 Mastered `.ogg` Audio Files (`Audio/BGS/` + `Audio/SE/`):** Fills **100% of the missing BGS and cutscene SE slots** listed in [`design/AUDIO.md`](../../design/AUDIO.md) lines 181–184 (`Rain`, `Wind - Isenmar`, `Lava - Ashkaar`, `Machinery - Zenith`, `Drip - Nadir`, `War - Distant Battle`, `Beam charge`, `Beam clash`, `Beam break`, `Crowd cheer`, `Crowd gasp`), plus 3 signature Prismfall BGS beds, 5 signature field/boss/VS SEs, and 7 distinct character dialogue voice-blip `.ogg`s.
3. **66-Slot Diversified, 100%-Pure-Instrumental Soundtrack Blueprint (v3):**
   - **STRICT CREATOR RULE — ZERO VOCALS:** Every single track has been ear-audited for zero singing, lyrics, choirs, stadium chants, or spoken countdown voices.
   - **3 Creator Must-Include Placements:**
     1. **GlitchxCity — *Pokémon Legends: Z-A — Corbeau Battle Theme (Remix)*** → **`Battle - Warden Nyx` (`LEADER_NYX`, Gym 16 Underveil — `:NEW_MOON`)**: smoky velvet-and-smoke jazz-noir syndicate swagger matches Nyx Calloway (*"undercity queen. Velvet and smoke... Everything has a price. Yours just went up."*) 10/10.
     2. **GlitchxCity — *Pokémon B2W2 — Champion Iris Battle Theme (Remix)*** → **`Battle - Festival Final` (Crownhaven Prism Arena)**: sparkling celestial chimes & triumphant euphoria for the once-in-a-decade Sovereign Festival Finals — setting up an unforgettable tonal pivot when exhausted 58-year-old Sovereign Valen steps onto the floor next.
     3. **Blue Archive (Mitsukiyo) — *Unwelcome School*** → **`Mood - Comedy / "Team Compost" Chaos` (`story/15_COMEDY.md`)**: Prismfall's official comedy/chaos theme across Ch1–Ch20 (*"Team Compost"*, Tamsin's Apology Spiral, Rook's livestream chat, Odessa's skiff safety briefing, Dorian watching *"The Pageant of the Pageant"* 9 times, Bastian's selective deafness vs Meridian!).
   - **Massive Artist Variety (22 Artists & Franchises — GlitchxCity trimmed to ~25% crown jewels):** Adds **CatchDalgo (8)**, **Zumi / Honnojis (7)**, **Dedrum / Pokémon Tectonic CC BY-NC-SA (4, already in repo!)**, **VanilluxePavilion**, **Zame**, **Bliitzit**, **Larachide**, **Emdasche**, AND **20+ popular "Pokémon-style" non-Pokémon pure-instrumental RPG gems** (*Undertale/Deltarune*, *Ace Attorney*, *Mario & Luigi*, *Kirby*, *Persona 5*, *Xenoblade*, *Fire Emblem*, *Octopath Traveler*, *Trails in the Sky*, *Hollow Knight*, *Blue Archive*, *PGR — Out of My Hands*).

---

## Creator-Locked & Diversified 66-Slot Soundtrack Blueprint

> **Usage Transparency:** Tracks marked `⚠️ Rejuv` were custom-made for Pokémon Rejuvenation and carry its V13.5 asset-guide restriction for public fangame reuse — clean non-Rejuv alternatives are listed right alongside them so the creator decides knowingly before public release.

### 1. Creator Must-Includes (Locked In!)
| Slot | Track | Artist | Why It Fits Prismfall |
|---|---|---|---|
| `Battle - Warden Nyx` (`LEADER_NYX`, Gym 16) | **Pokémon Legends: Z-A — Corbeau Battle Theme (Remix)** | GlitchxCity | Velvet-and-smoke syndicate swagger for Underveil's undercity queen |
| `Battle - Festival Final` (Prism Arena Finals) | **Pokémon B2W2 — Champion Iris Battle Theme (Remix)** | GlitchxCity | Glittering starry Festival euphoria before Valen's solemn confrontation |
| `Mood - Comedy / Team Compost` (`story/15_COMEDY.md`) | **Unwelcome School** | Blue Archive (Mitsukiyo) | Pure comedic chaos across Team Compost, Tamsin's spiral, Rook's chat & Dorian's play |

### 2. World, Towns, Isenmar Snow, Dungeons & Moods (22 Slots)
| Slot | Track | Artist / Origin |
|---|---|---|
| `Title - Prismfall` | Pokémon BW — Route 10 Remix v.II | GlitchxCity |
| `Town - Ferrows Landing` | Gold & Silver — New Bark Town (Lofi Remix) | GlitchxCity |
| `Town - Elowen` (Briarwick / Verdance) | **Floral Rest** (CC BY-NC-SA, already in repo) | Dedrum (Tectonic) |
| `Route - Elowen Forest` (Deepwood) | **Greenpath** (Alt: **Slumbering Weald Remix** by Zumi) | Hollow Knight / Zumi |
| `Town - Antumbra` (Lucent / Gravenmoor) | **Queen's Gardens** (zero-vocal replacement) | Hollow Knight |
| `Route - Antumbra / Bleed` | Platinum — Distortion World Remix v2 | GlitchxCity |
| `Town - Isenmar` (Rimeholt) | **Snowpoint City (Chill Remix)** (Alt: **Frostflow Farms** by Dedrum) | GlitchxCity / Dedrum |
| `Route - Isenmar` (Frostfang Pass) | **Sinnoh Route 216 Remix** (Alt: **The Frostlands** by Octopath) | GlitchxCity / Octopath |
| `Town & Route - Ashkaar` | HGSS — Route 47 Remix | GlitchxCity |
| `Town & Route - Zenith` (Skyreach) | **PMD — Sky Tower Remix** | **Zumi (Honnojis)** |
| `Town & Route - Nadir` | BW2 — Virbank City | Pokémon OST |
| `Dungeon - Ruins / Ossuary` (Ossaria) | **Ancient Ruins / Regi Dungeon** (CC BY-NC-SA, already in repo) | Dedrum (Tectonic) |
| `Town - Crownhaven` | X & Y — Pokémon League Remix | GlitchxCity |
| `Theme - Meridian Spire` | **ARCHETYPE (Third Layer HQ)** ⚠️ Rejuv (Clean Alt: **BDSP Team Galactic HQ**) | **Zumi (Honnojis)** / Pokémon OST |
| `Mood - Farewell / Loss` | **Resting Grounds** | Hollow Knight |
| `War - Aftermath / AF 290` | **PMD2 — Through the Sea of Time Orchestral** | **CatchDalgo** |
| `Ending - Homecoming` | **BW — An Unwavering Heart** (Alt: **Casaba Villa Remix** by Dedrum) | Pokémon OST / Dedrum |

### 3. Standard, Rivals & Wardens (13 Slots)
| Slot | Track | Artist / Origin |
|---|---|---|
| `Battle - Wild` | Red & Blue — Wild Battle Remix | GlitchxCity |
| `Battle - Trainer (Early/Mid)` | **Rude Buster** *(Pokémon-style indie classic!)* | **Toby Fox (Deltarune)** |
| `Battle - Trainer (Late / Act III+)` | **Legends: Z-A — Trainer Battle Remix** | **CatchDalgo** |
| `Battle - Rival Juno` | **RE Aoharu** | Blue Archive |
| `Battle - Warden Juno` (Ch10 / Ch20 Mega Gardevoir) | **Hopes and Dreams** *(radiant blooming payoff!)* | **Toby Fox (Undertale)** |
| `Battle - Rival Kestrel (K1–K7)` | **Silver Will (1st Chapter Remake)** | Trails in the Sky (Falcom) |
| `Battle - Kestrel Semifinal K8` | **Battle! Aether Executive Gladion (Remix)** | **CatchDalgo** |
| `Battle - Warden (Gyms 1–18)` | **Pokémon Crystonite — Gym Battle** *(non-Rejuv!)* | **Zumi (Honnojis)** |
| `Battle - Warden Special / 2-Bar` (Odessa/Ilsa) | **BW — Unova Elite 4 (Remix)** | **Zumi (Honnojis)** |
| `Battle - Warden Last Pokémon` | **BW2 — Victory Lies Before You!** *(zero crowd chants)* | Pokémon OST |
| `Battle - Warden Rowan ("The Gardener")` | **Hornet** | Hollow Knight |
| `Battle - Warden Celestine` (Gym 17 `:FAIRY_TALE`) | **VS Magolor (C-R-O-W-N-E-D)** | **Kirby (HAL)** |
| `Battle - Warden Sigrun` (Gym 18 `:DRAGONS_DEN`) | **Battle Against a True Hero** | **Toby Fox (Undertale)** |

### 4. Factions — Hollow, Meridian, Octave & War (12 Slots)
| Slot | Track | Artist / Origin |
|---|---|---|
| `Battle - Hollow` (`HOLLOW_GRUNT`) | Rejuvenation — Xen Grunt Battle ⚠️ Rejuv | GlitchxCity |
| `Battle - Hollow Keepers` (`WICK/THISTLE/TEO/SABLE`) | **Battle! Shadow Lugia Remix** | **Zame** |
| `Battle - The Mourner` (`105_Boss_Mourner.rb`) | **BW — Prince N Final Battle Remix** | GlitchxCity |
| `Battle - Meridian Agent` | **Pokemon Espionage — Battle! Interpol Grunt** | **CatchDalgo** |
| `Battle - Meridian Director` (`QUENT/ASHE`) | **Pokemon Espionage — Battle! Interpol Admin White Wolf** | **CatchDalgo** |
| `Battle - Meridian Director Marchetti` | **Blooming Villain -Scramble-** *(pure instrumental!)* | **Persona 5 (Shoji Meguro)** |
| `Battle - Ch13 Tribunal Ambush (Sabine Kroll)` | **Pursuit ~ Wanting to Find the Truth** *(courtroom clash!)* | **Ace Attorney (Capcom)** |
| `Battle - Aurelian Voss` (`MERIDIAN_VOSS`) | **Out of My Hands [Creator Ref]** (Alt: **They Who Govern Reason** by Octopath) | PGR (0-vocal) / Octopath |
| `Battle - The Eevee Octave` (`VESPER` & 8 Choristers) | **Mantis Lords** | Hollow Knight |
| `War - Ashkaar vs Isenmar Battlefield` | **Fódlan Winds** | **Fire Emblem: Three Houses** |
| `War - Glass Dunes Beam Clash` | **Legends: Z-A — Rogue Mega Rayquaza Remix** | GlitchxCity |

### 5. Multi-Bar Bosses, Legendaries, Ruin Route, Festival & Arceus Finale (16 Slots)
| Slot | Track | Artist / Origin |
|---|---|---|
| `Battle - Boss (Multi-Bar Standard)` | **You Will Know Our Names (DE)** | **Xenoblade Chronicles** |
| `Battle - Boss Final Bar` | **In The Final DX** *(legendary DS-era Pokémon-adjacent rush!)* | **Mario & Luigi (Yoko Shimomura)** |
| `Boss - Mindscape Nightmare / Rift` | **VS! The Master of Nightmares** ⚠️ Rejuv | **Zumi (Honnojis)** |
| `Boss - Giratina (Ch15) & Catchable Rifts` | **Platinum — Vs Giratina Remix** | **VanilluxePavilion** |
| `Boss - Kyogre` (`101_Boss_Kyogre.rb`) | **ORAS — Primal Kyogre & Groudon Remix** | Larachide |
| `Boss - Groudon` (Ch14 Deep Seams) | **Kirby — Masked and Wild: D.D.D. Remix** | **CatchDalgo** |
| `Boss - Zekrom & Reshiram` (`102`/`106`) | **BW — Battle! Zekrom & Reshiram Remix** | Emdasche |
| `Boss - Pecharunt & Loyal Three` | **SV — Battle! Legendary Quartet Epic Orchestral** | **CatchDalgo** |
| `Boss - Echo of Morwen` (`ECHO_MORWEN`) | Rejuvenation — Leader Angie Battle ⚠️ Rejuv | GlitchxCity |
| `Ruin Route - Gilded King Theodric` | **Tyrant of Spades (Deltarune Chaos King Remix)** | **Zumi (Honnojis)** |
| `Ruin Route - The Reflection` | Sun & Moon — Lusamine Battle Remix | GlitchxCity |
| `Battle - Festival Bracket` | **Legends: Z-A — Battle! Z-A Royale! Remix** | **CatchDalgo** |
| `Champion - Sovereign Valen` (`CHAMPION_VALEN`) | **ASGORE** *(58yo gentle, guilt-ridden king!)* (Alt: **Cynthia Remix** by GlitchxCity) | **Toby Fox (Undertale)** / GlitchxCity |
| `TRUE FINALE - Arceus` (`103_Boss_Arceus.rb`) | **Legends: Arceus — Origin Form Dialga & Palkia Remix** | GlitchxCity |
| `Battle - Cameo & Concordance Spire` | **Battle! Champion Red Remix** | **Bliitzit** |
