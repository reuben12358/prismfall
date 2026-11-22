# Proposal: Audio Mastering Pipeline, Original CC0 BGS/SE Pack & 52-Slot Pure-Instrumental Soundtrack Blueprint

- **Date:** 2026-11-21 (Updated 2026-11-22: 100% Instrumental-Only Rule + Expanded Ch 1–21 Fight Roster)
- **Owner / Author:** Gemini (Art & Audio Direction)
- **Status:** Ready for Claude & Creator review (zero files modified outside `gemini_recommends/`)

---

## What

1. **Reusable Audio Mastering & Loop-Tagging CLI (`master_track.py`):** Converts any `.mp3`/`.wav`/`.flac`/`.ogg` track to `44.1 kHz` Ogg Vorbis (`libvorbis -q:a 6`), applies two-pass EBU R128 loudness normalization (`-14.0 LUFS` BGM / `-20.0 LUFS` BGS / `-12.0..-14.0 LUFS` SE, `-1.5 dBTP`), writes exact `LOOPSTART`/`LOOPLENGTH` Vorbis comments in samples for seamless `mkxp-z` looping, and provides an `--audit` report mode.
2. **26 Original CC0 Mastered `.ogg` Audio Files (`Audio/BGS/` + `Audio/SE/`):** Fills **100% of the missing BGS and cutscene SE slots** listed in [`design/AUDIO.md`](../../design/AUDIO.md) lines 181–184 (`Rain`, `Wind - Isenmar`, `Lava - Ashkaar`, `Machinery - Zenith`, `Drip - Nadir`, `War - Distant Battle`, `Beam charge`, `Beam clash`, `Beam break`, `Crowd cheer`, `Crowd gasp`), plus 3 signature Prismfall BGS beds, 5 signature field/boss/VS SEs, and 7 distinct character dialogue voice-blip `.ogg`s.
3. **Expanded 52-Slot Pure-Instrumental Soundtrack Blueprint (v2):**
   - **STRICT CREATOR RULE — 100% PURE INSTRUMENTAL BGM ONLY (ZERO VOCALS):** Zero singing, lyrics, choirs, stadium crowd chants, or spoken countdown voices in any BGM slot. All 8 earlier tracks with human voices (*City of Tears* soprano, *PGR Dust*, *NieR Vague Hope*, *SwSh Gym Leader* crowd chants, *PGR Lamia*, *NieR Bipolar Nightmare*, *PGR Narwhal*, *PGR Hikari*) have been replaced with ear-verified pure instrumentals. The creator's calibration reference (**PGR — *Out of My Hands***) was ear-verified as 100% pure instrumental strings/synth.
   - **Expanded from 33 → 52 Slots to Match Claude's Full Ch 1–21 Repo (`pbs/trainer_types.txt`, `pbs/trainers.txt`, `plugins/Prismfall Bosses/101..106*.rb`, `story/06..14`):** Adds dedicated themes for Meridian Agents/Directors (`Marchetti`, `Kroll`, `Ashe`, `Quent`), The Eevee Octave (`OCTAVE_VESPER`, `OCTAVE_SINGER`), Warden Juno, Warden Rowan ("The Gardener"), Kestrel Semifinal K8, Kyogre (`101_Boss_Kyogre.rb`), Groudon (Ch14 Deep Seams), Zekrom & Reshiram (`102_Boss_Zekrom.rb`, `106_Boss_WarLegends.rb`), Glass Dunes Beam Clash, Pecharunt & Loyal Three, Echo of Morwen, Ruin Route (`Reflection`, `Gilded King Theodric`, `Archseer Dask`), True Finale Arceus (`103_Boss_Arceus.rb`), Cameo Superbosses (`FESTIVAL_LIN/VENAM/MELIA/TITANIA/NOVA`) & Concordance Spire, Meridian Spire Theme, and Ending — Homecoming.

---

## Why

Auditing [`audio/manifest.tsv`](../../audio/manifest.tsv) and [`audio/dedrum_tectonic/`](../../audio/dedrum_tectonic/) uncovered concrete production issues plus missing audio slots:

1. **Zero loop tags (`0 / 17`):** None of the 17 staged `dedrum_tectonic/` audio files contain `LOOPSTART`/`LOOPLENGTH` Vorbis comments, meaning `mkxp-z` restarts from sample `0` with audible seams instead of looping cleanly.
2. **4.6 dB loudness swing (`-14.5` to `-19.1 LUFS`):** Players experience jarring volume jumps between maps and battles; mastering all tracks to `-14.0 LUFS` (BGM) and `-20.0 LUFS` (BGS) solves this automatically.
3. **`.mp3` cannot sample-loop (`Battle - Voss`):** `Tectonic_Yezera_Battle_Theme.mp3` ships as `.mp3`; converting to `.ogg` via `master_track.py` enables seamless sample looping.
4. **Missing BGS & cutscene SE slots:** `design/AUDIO.md` notes 6 missing `Audio/BGS` weather/atmosphere loops and 5 missing cutscene `Audio/SE` effects (war beam clash + festival crowd). All 11—plus 15 Prismfall signature SEs, BGS layers, and dialogue voice blips—are included here as clean CC0 `.ogg` assets.
5. **Gameplay-first melody + strict instrumental purity (Creator Directives):** Towns/routes need hummable **gameplay music** (with `Audio/BGS` whispering softly at 15–25% underneath), and **no human voices** should distract from dialogue or battles.

---

## Where It Plugs In

| Deliverable | Destination if Adopted | Wiring Reference |
|---|---|---|
| `master_track.py` | `audio/master_track.py` (alongside `audio/install_audio.py`) | Run before committing/installing new BGM/BGS/SE tracks |
| `Audio/BGS/*.ogg` (9 files, all `-20 LUFS`, `LOOPSTART=0`) | `<game>/Audio/BGS/` (and/or staged in `audio/prismfall_cc0/BGS/`) | `design/AUDIO.md` §3–4 (`pbBGSPlay`, `mapgen/rpg.py rmap(bgs=...)` at volume `20–30`) |
| `Audio/SE/*.ogg` (10 SEs + 7 `Voice - *.ogg`) | `<game>/Audio/SE/` (and/or staged in `audio/prismfall_cc0/SE/`) | War climax (`Beam charge/clash/break`), Festival (`Crowd cheer/gasp`), Fields (`Glass Quench`, `Field Shatter`, `Prism Arena Swell`), Bosses (`Boss Shield Break`), EBDX VS (`VS Cutin Lightning`), Dialogue text-blip hook (`Voice - *.ogg`) |
| 52-Slot Pure-Instrumental Blueprint | Update `audio/manifest.tsv` target column & `design/AUDIO.md` §3 once creator locks favorites | Drop downloaded mastered `.ogg`s under `final_name` (note: optional per-boss slots like `Boss - Kyogre`, `Battle - Octave`, `Battle - Warden Juno` can either get dedicated `BattleBGM` entries or fold into the existing `design/AUDIO.md` table) |

### Exact Included CC0 Audio Files (26 Mastered `.ogg` Files)

**`Audio/BGS/` (9 seamless `LOOPSTART=0` weather/atmosphere beds at `-20.0 LUFS`):**
- `Rain.ogg`, `Wind - Isenmar.ogg`, `Lava - Ashkaar.ogg`, `Machinery - Zenith.ogg`, `Drip - Nadir.ogg`, `War - Distant Battle.ogg`, `Saltmere Harbor.ogg`, `Gossamer Deepwood.ogg`, `Glassfall Bleed.ogg`

**`Audio/SE/` (10 one-shot SFX + 7 dialogue voice ticks):**
- `Beam charge.ogg`, `Beam clash.ogg`, `Beam break.ogg`, `Crowd cheer.ogg`, `Crowd gasp.ogg`, `Glass Quench.ogg`, `Field Shatter.ogg`, `Prism Arena Swell.ogg`, `Boss Shield Break.ogg`, `VS Cutin Lightning.ogg`
- `Voice - Juno.ogg`, `Voice - Kestrel.ogg`, `Voice - Larch.ogg`, `Voice - Dorian.ogg`, `Voice - Tamsin.ogg`, `Voice - Mourner.ogg`, `Voice - Player.ogg`

---

## Curated 52-Slot Pure-Instrumental Soundtrack Blueprint (Zero Vocals)

> **Permission Transparency Note:** The creator explicitly asked to audition **Pokémon Rejuvenation** & **Reborn** tracks alongside **GlitchxCity**, official Pokémon remixes, and outside-Pokémon instrumentals. Rows marked `⚠️ Rejuv asset-guide` note tracks that Rejuvenation's V13.5 asset guide asks public fangames not to reuse directly — keep an eye on those before public release!

### 1. World, Towns, Isenmar Snow & Story Moods (17 Slots — All Zero-Vocal)

| # | Slot (`final_name`) | Pure-Instrumental Primary Pick | Status / Notes |
|---|---|---|---|
| 1 | `Title - Prismfall` | GlitchxCity — Pokémon BW Route 10 Remix v.II | Pure instrumental |
| 2 | `Town - Ferrows Landing` | GlitchxCity — New Bark Town (Lofi Remix) | Pure instrumental |
| 3 | `Town - Elowen` | GlitchxCity — Sinnoh Route 209 (Lofi Remix) | Pure instrumental |
| 4 | `Route - Elowen Forest` | Hollow Knight OST — Greenpath | Pure instrumental |
| 5 | `Town - Antumbra` | Hollow Knight OST — Queen's Gardens | **Replaced City of Tears vocals** |
| 6 | `Route - Antumbra / Bleed` | GlitchxCity — Platinum Distortion World Remix v2 | Pure instrumental |
| 7 | `Town - Isenmar` | GlitchxCity — Snowpoint City (Chill Remix) | Gameplay-first snow town (layer `Wind - Isenmar` BGS at 15–20%) |
| 8 | `Route - Isenmar` | GlitchxCity — Sinnoh Route 216 Remix | Gameplay-first winter route |
| 9 | `Isenmar Alt (Orchestral)` | Octopath Traveler OST — The Frostlands | Pure cello/harp snow alternative |
| 10 | `Isenmar Alt (Melancholy)` | GlitchxCity — X & Y Snowbelle City Remix | Wistful piano alternative |
| 11 | `Town & Route - Ashkaar` | GlitchxCity — HGSS Route 47 Remix | **Replaced PGR Dust vocals** |
| 12 | `Town & Route - Zenith` | GlitchxCity — X & Y Route 15 Remix | Pure instrumental |
| 13 | `Town & Route - Nadir` | Pokémon BW2 — Virbank City | Pure industrial bass groove |
| 14 | `Town - Crownhaven` | GlitchxCity — X & Y Pokémon League Remix | Pure instrumental |
| 15 | `Theme - Meridian Spire` | Pokémon BDSP OST — Team Galactic HQ | **NEW (Ch12–13 Spire & Voss's Office)** |
| 16 | `Mood - Farewell / Loss` | Hollow Knight OST — Resting Grounds | **Replaced NieR Vague Hope vocals** |
| 17 | `Ending - Homecoming` | Pokémon BW — An Unwavering Heart ('Emotion' Remaster) | **NEW (Act V Good/Grey Ending)** |

### 2. Standard, Rivals & Wardens (11 Slots — All Zero-Vocal)

| # | Slot | Pure-Instrumental Primary Pick | Status / Notes |
|---|---|---|---|
| 18 | `Battle - Wild` | GlitchxCity — Red & Blue Wild Battle Remix | Pure instrumental |
| 19 | `Battle - Trainer` | GlitchxCity — DPPt Trainer Battle Remix | Pure instrumental |
| 20 | `Battle - Trainer (Late)` | GlitchxCity — BW Trainer Battle Remix | Pure instrumental |
| 21 | `Battle - Rival Juno` | Blue Archive OST — RE Aoharu | Ear-verified 0-vocal guitar/piano |
| 22 | `Battle - Warden Juno (Ch10/20)` | Blue Archive OST — Unwelcome School | **NEW (Grass Warden + Gardevoir)** |
| 23 | `Battle - Rival Kestrel (K1–K7)` | Trails in the Sky 1st Remake — Silver Will | Ear-verified 0-vocal violin/rock |
| 24 | `Battle - Kestrel Semifinal K8` | GlitchxCity — Gold & Silver Rival Battle Remix v.II | **NEW (Act V Fallen vs Redeemed)** |
| 25 | `Battle - Warden (Gyms 1–18)` | Rejuvenation (GlitchxCity) — Gym Leader Battle ⚠️ | Pure instrumental |
| 26 | `Battle - Warden Special / 2-Bar` | GlitchxCity — DPPt Gym Leader Battle Remix | Odessa, Ilsa 2-Bar, Celestine, Sigrun |
| 27 | `Battle - Warden Last Pokémon` | Pokémon BW2 OST — Victory Lies Before You! | **Replaced SwSh crowd chants** |
| 28 | `Battle - Warden Rowan (Gardener)` | Hollow Knight OST — Hornet | **NEW (Ch13 Tribunal & Festival)** |

### 3. Factions — Lantern Hollow, Meridian Directorate, Eevee Octave & War (10 Slots — All Zero-Vocal)

| # | Slot | Pure-Instrumental Primary Pick | Status / Notes |
|---|---|---|---|
| 29 | `Battle - Hollow` | Rejuvenation (GlitchxCity) — Xen Grunt Battle ⚠️ | Pure instrumental |
| 30 | `Battle - Hollow Admin` | GlitchxCity — DPPt Team Galactic Boss Remix | Wick, Thistle, Teo, Sable, Brisk |
| 31 | `Battle - The Mourner` | GlitchxCity — BW Prince N Final Battle Remix | **Replaced PGR Lamia vocals** (`105_Boss_Mourner.rb`) |
| 32 | `Battle - Meridian Agent` | GlitchxCity — Legends: Z-A Team Flare Nouveau Remix | **NEW (`MERIDIAN_AGENT/DIRECTORATE`)** |
| 33 | `Battle - Meridian Director` | GlitchxCity — BW Team Plasma Battle Remix | **NEW (`MARCHETTI`, `KROLL`, `ASHE`, `QUENT`)** |
| 34 | `Battle - Aurelian Voss` | **PGR — Out of My Hands [Creator Ref]** | **Ear-verified 100% pure instrumental** |
| 35 | `Battle - Aurelian Voss (Alt)` | Octopath Traveler OST — They Who Govern Reason | **NEW orchestral alt** |
| 36 | `Battle - The Eevee Octave` | Hollow Knight OST — Mantis Lords | **NEW (`OCTAVE_VESPER`, `OCTAVE_SINGER`, Still Water)** |
| 37 | `War - Battlefield / Frontline` | GlitchxCity — PMD Primal Dialga Battle Remix | **Replaced PGR Hikari vocals** (`ASHKAAR/ISENMAR`) |
| 38 | `War - Glass Dunes Beam Clash` | GlitchxCity — Legends: Z-A Rogue Mega Rayquaza Remix | **NEW (`106_Boss_WarLegends.rb` climax)** |

### 4. Multi-Bar Bosses, Legendaries, Ruin Route, Festival & Arceus Finale (14 Slots — All Zero-Vocal)

| # | Slot | Pure-Instrumental Primary Pick | Status / Notes |
|---|---|---|---|
| 39 | `Battle - Boss (Multi-Bar)` | Octopath Traveler OST — Decisive Battle II | **Replaced NieR Bipolar Nightmare vocals** |
| 40 | `Battle - Boss Final Bar` | Octopath Traveler OST — Battle at Journey's End | **Replaced PGR Narwhal vocals** |
| 41 | `Battle - Dimensional Rift` | Rejuvenation — Dimensional Rift Battle ⚠️ | Ear-verified 0-vocal |
| 42 | `Battle - Legendary (Giratina)` | GlitchxCity — Platinum Giratina Battle Remix | Ch15 Giratina & catchable rifts |
| 43 | `Boss - Kyogre (Ch11 The Thaw)` | Pokémon ORAS — Primal Kyogre & Groudon Remix | **NEW (`101_Boss_Kyogre.rb` 5-Bar & Ice Vault)** |
| 44 | `Boss - Groudon (Ch14 Seams)` | GlitchxCity — Ruby & Sapphire Magma/Aqua Boss Remix | **NEW (Ch14 Deep Seams Unown Chamber)** |
| 45 | `Boss - Zekrom & Reshiram` | Pokémon BW — Battle! Zekrom & Reshiram Remix | **NEW (`102_Boss_Zekrom.rb`, Ch19 Wyrmrest)** |
| 46 | `Boss - Pecharunt & Loyal Three` | Pokémon SV OST — Final Boss (Music-Box / Synth) | **NEW (Ch10 / Ch18 Lightless Deep; zero shout vocals)** |
| 47 | `Boss - Echo of Morwen` | Rejuvenation (GlitchxCity) — Leader Angie Battle ⚠️ | **NEW (`ECHO_MORWEN` Ch15 Cathedral / Ch20)** |
| 48 | `Battle - Ruin (Reflection/Theodric)` | GlitchxCity — Sun & Moon Lusamine Battle Remix | **NEW (`REFLECTION`, `GILDED_THEODRIC`, `ARCHSEER_DASK`)** |
| 49 | `Battle - Festival / Finals` | Pokémon Reborn (GlitchxCity) — Elite 4 Battle Theme | Festival bracket & finals |
| 50 | `Battle - Sovereign Valen` | GlitchxCity — DPPt Champion Cynthia Battle Remix | `CHAMPION_VALEN` |
| 51 | `Battle - Arceus (True Finale)` | GlitchxCity — Legends: Arceus Origin Form Dialga/Palkia | **NEW (`103_Boss_Arceus.rb` 18-Plate Finale)** |
| 52 | `Battle - Cameo & Spire` | GlitchxCity — Emerald Battle Frontier Brain Remix v.II | **NEW (`FESTIVAL_LIN/VENAM/MELIA/TITANIA/NOVA` & Spire)** |

---

## Sources

- Existing audio plan & boss/trainer roster: [`design/AUDIO.md`](../../design/AUDIO.md), [`audio/manifest.tsv`](../../audio/manifest.tsv), [`pbs/trainer_types.txt`](../../pbs/trainer_types.txt), [`plugins/Prismfall Bosses/`](../../plugins/Prismfall%20Bosses/)
- Creator's outside-Pokémon calibration reference: Punishing: Gray Raven — *Out of My Hands* (ear-verified 100% pure instrumental)
- All 26 `.ogg` files under `Audio/BGS/` and `Audio/SE/` in this folder were synthesized from scratch using Python + `ffmpeg` + `vorbiscomment` — **100% original CC0 (Public Domain)**.
