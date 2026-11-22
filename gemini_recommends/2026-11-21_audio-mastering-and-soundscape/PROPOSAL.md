# Proposal: Audio Mastering Pipeline, Original CC0 BGS/SE Pack & Gameplay-First Soundtrack Blueprint

- **Date:** 2026-11-21
- **Owner / Author:** Gemini (Art & Audio Direction)
- **Status:** Ready for Claude & Creator review (zero files modified outside `gemini_recommends/`)

---

## What

1. **Reusable Audio Mastering & Loop-Tagging CLI (`master_track.py`):** Converts any `.mp3`/`.wav`/`.flac`/`.ogg` track to `44.1 kHz` Ogg Vorbis (`libvorbis -q:a 6`), applies two-pass EBU R128 loudness normalization (`-14.0 LUFS` BGM / `-20.0 LUFS` BGS / `-12.0..-14.0 LUFS` SE, `-1.5 dBTP`), writes exact `LOOPSTART`/`LOOPLENGTH` Vorbis comments in samples for seamless `mkxp-z` looping, and provides an `--audit` report mode.
2. **26 Original CC0 Mastered `.ogg` Audio Files (`Audio/BGS/` + `Audio/SE/`):** Fills **100% of the missing BGS and cutscene SE slots** listed in [`design/AUDIO.md`](../../design/AUDIO.md) lines 181–184 (`Rain`, `Wind - Isenmar`, `Lava - Ashkaar`, `Machinery - Zenith`, `Drip - Nadir`, `War - Distant Battle`, `Beam charge`, `Beam clash`, `Beam break`, `Crowd cheer`, `Crowd gasp`), plus 3 signature Prismfall BGS beds, 5 signature field/boss/VS SEs, and 7 distinct character dialogue voice-blip `.ogg`s.
3. **Updated 33-Slot Gameplay-First Soundtrack Blueprint:** Expands `design/AUDIO.md` per the creator's latest direction — prioritizing **memorable, hummable gameplay melodies** (never bland ambience-as-BGM), inclusive of **GlitchxCity**, **Pokémon Rejuvenation**, **Pokémon Reborn**, **Dedrum/Tectonic**, and **outside-Pokémon OSTs** calibrated to the creator's reference track (**Punishing: Gray Raven — *"Out of My Hands"***).

---

## Why

Auditing [`audio/manifest.tsv`](../../audio/manifest.tsv) and [`audio/dedrum_tectonic/`](../../audio/dedrum_tectonic/) uncovered four concrete production issues plus missing audio slots:

1. **Zero loop tags (`0 / 17`):** None of the 17 staged `dedrum_tectonic/` audio files contain `LOOPSTART`/`LOOPLENGTH` Vorbis comments, meaning `mkxp-z` restarts from sample `0` with audible seams instead of looping cleanly.
2. **4.6 dB loudness swing (`-14.5` to `-19.1 LUFS`):** Players experience jarring volume jumps between maps and battles; mastering all tracks to `-14.0 LUFS` (BGM) and `-20.0 LUFS` (BGS) solves this automatically.
3. **`.mp3` cannot sample-loop (`Battle - Voss`):** `Tectonic_Yezera_Battle_Theme.mp3` ships as `.mp3`; converting to `.ogg` via `master_track.py` enables seamless sample looping.
4. **Missing BGS & cutscene SE slots:** `design/AUDIO.md` notes 6 missing `Audio/BGS` weather/atmosphere loops and 5 missing cutscene `Audio/SE` effects (war beam clash + festival crowd). All 11—plus 15 Prismfall signature SEs, BGS layers, and dialogue voice blips—are included here as clean CC0 `.ogg` assets.
5. **Gameplay-first melody over realistic ambience (Creator Directive):** The creator auditioned `Isenmar Gale` solo and rightly noted that towns/routes need joyful, iconic **gameplay music** (like *Snowpoint City*, *Sinnoh Route 216*, or *Ametrine/Calcenon*) — while `Audio/BGS` should whisper subtly at ~15–25% volume *underneath* melodic BGM during storms or cutscenes.

---

## Where It Plugs In

| Deliverable | Destination if Adopted | Wiring Reference |
|---|---|---|
| `master_track.py` | `audio/master_track.py` (alongside `audio/install_audio.py`) | Run before committing/installing new BGM/BGS/SE tracks |
| `Audio/BGS/*.ogg` (9 files, all `-20 LUFS`, `LOOPSTART=0`) | `<game>/Audio/BGS/` (and/or staged in `audio/prismfall_cc0/BGS/`) | `design/AUDIO.md` §3–4 (`pbBGSPlay`, `mapgen/rpg.py rmap(bgs=...)` at volume `20–30`) |
| `Audio/SE/*.ogg` (10 SEs + 7 `Voice - *.ogg`) | `<game>/Audio/SE/` (and/or staged in `audio/prismfall_cc0/SE/`) | War climax (`Beam charge/clash/break`), Festival (`Crowd cheer/gasp`), Fields (`Glass Quench`, `Field Shatter`, `Prism Arena Swell`), Bosses (`Boss Shield Break`), EBDX VS (`VS Cutin Lightning`), Dialogue text-blip hook (`Voice - *.ogg`) |
| Soundtrack Blueprint (33 slots) | Update `audio/manifest.tsv` target column & `design/AUDIO.md` §3 once creator locks favorites | Drop downloaded mastered `.ogg`s under the existing `final_name` — **zero PBS changes required** |

### Exact Included CC0 Audio Files (26 Mastered `.ogg` Files)

**`Audio/BGS/` (9 seamless `LOOPSTART=0` weather/atmosphere beds at `-20.0 LUFS`):**
- `Rain.ogg` — gentle steady rain bed (Antumbra / rainy routes)
- `Wind - Isenmar.ogg` — arctic blizzard layer (play at vol 15–25 under melodic Isenmar BGM!)
- `Lava - Ashkaar.ogg` — basalt magma cavern rumble
- `Machinery - Zenith.ogg` — clockwork dynamo hum & subtle brass ticks
- `Drip - Nadir.ogg` — hollow cavern water drips
- `War - Distant Battle.ogg` — muffled distant valley rumble for war cutscenes
- `Saltmere Harbor.ogg` — soft coastal surf swells
- `Gossamer Deepwood.ogg` — woodland breeze + faint silk chimes
- `Glassfall Bleed.ogg` — crystalline harmonic drone for Bleed rift cutscenes

**`Audio/SE/` (10 one-shot SFX + 7 dialogue voice ticks):**
- `Beam charge.ogg`, `Beam clash.ogg`, `Beam break.ogg` — Ashkaar–Isenmar war climax
- `Crowd cheer.ogg`, `Crowd gasp.ogg` — Sovereign Festival crowd stings (SE so BGM never pauses!)
- `Glass Quench.ogg` — Ashkaar fire-meets-Isenmar ice field quench transition
- `Field Shatter.ogg` — field terrain shatter crunch + crystal shards
- `Prism Arena Swell.ogg` — Prism Arena activation harmonic chord
- `Boss Shield Break.ogg` — multi-bar boss shield shatter impact
- `VS Cutin Lightning.ogg` — B2W2 VS cut-in electric flash + slam
- `Voice - Juno.ogg`, `Voice - Kestrel.ogg`, `Voice - Larch.ogg`, `Voice - Dorian.ogg`, `Voice - Tamsin.ogg`, `Voice - Mourner.ogg`, `Voice - Player.ogg`

---

## Curated 33-Slot Gameplay-First Soundtrack Blueprint (Verified YouTube IDs)

> **Permission Transparency Note:** The creator explicitly asked to include **Pokémon Rejuvenation** & **Reborn** tracks alongside **GlitchxCity** and outside-Pokémon OSTs during auditioning. Rows marked `⚠️ Rejuv asset-guide` note tracks that Rejuvenation's V13.5 asset guide asks other public fangames not to reuse directly — every such slot includes a clean non-Rejuv Alt pick so the creator can decide knowingly before final release!

### Towns, Isenmar Snow, Routes & Moods (15 Slots)
- **Playlist URL:** `https://www.youtube.com/watch_videos?video_ids=1ZbJXPL6wXM,uXSevd_JfRQ,O8ZsUHwpcEw,E1CVSjd-Yz0,VL5qP9UOX84,no4whNjQ0iY,stFT3rMthYs,2k9pjKkHZXo,7Jvmh04otBI,ZwZC4vlZTbI,ar6fbyeWj8U,m46OcZwqSHo,6MfVMVa5H60,Ml8WWBKZ79s,rn5AI4_mfbc`

| Slot (`final_name`) | Primary Pick | Alt / A-B Compare |
|---|---|---|
| `Title - Prismfall` | Rejuvenation V14 — Finality (`1ZbJXPL6wXM`) ⚠️ | GlitchxCity — BW Route 10 Remix (`bkhZ5ewS7U4`) |
| `Town - Ferrows Landing` | GlitchxCity — New Bark Town Remix (`uXSevd_JfRQ`) | GlitchxCity — Sinnoh Route 209 Remix (`O8ZsUHwpcEw`) |
| `Town - Elowen` | GlitchxCity — Sinnoh Route 209 Remix (`O8ZsUHwpcEw`) | Hollow Knight — Greenpath (`E1CVSjd-Yz0`) |
| `Route - Elowen Forest` | Hollow Knight — Greenpath (`E1CVSjd-Yz0`) | GlitchxCity — Eterna Forest Remix (`fEg21u_d2eA`) |
| `Town - Antumbra` | Hollow Knight — City of Tears (`VL5qP9UOX84`) | GlitchxCity — Lavender Town Remix (`lQoG1uj74Lc`) |
| `Route - Antumbra` | GlitchxCity — Distortion World Remix (`no4whNjQ0iY`) | Reborn — Atmosphere: Majesty Slowed (`llmgdHnFo8Q`) |
| `Town - Isenmar` | GlitchxCity — Snowpoint City Chill Remix (`stFT3rMthYs`) | Octopath Traveler — Flamesgrace, Guiding Light (`YI7VG-xJl-c`) |
| `Route - Isenmar` | GlitchxCity — Sinnoh Route 216 Remix (`2k9pjKkHZXo`) | Octopath Traveler — The Frostlands (`6dgmy3JXz3g`) |
| `Town/Route - Isenmar (Alt)` | GlitchxCity — X & Y Snowbelle City Remix (`7Jvmh04otBI`) | Kamex — Sinnoh Route 216/217 Remix (`F_wV6rZdg9A`) |
| `Town/Route - Ashkaar` | Punishing: Gray Raven — Dust (`ZwZC4vlZTbI`) | GlitchxCity — HGSS Route 47 Remix (`KCTDQr5nR60`) |
| `Town/Route - Zenith` | GlitchxCity — X & Y Route 15 Remix (`ar6fbyeWj8U`) | Rejuvenation V14 — GDC Indoor Transience (`wCVG93A6sYs`) ⚠️ |
| `Town/Route - Nadir` | Rejuvenation V14 — Dystopian GDC Vacuity (`m46OcZwqSHo`) ⚠️ | Mewmore — Ruins of Alph 2nd Remix (`cCJOvgcSojY`) |
| `Town - Crownhaven` | Arknights — All Quiet Under the Thunder 02 (`6MfVMVa5H60`) | Arknights — All Quiet Under the Thunder Boss (`DEbzZQ4AdcY`) |
| `Mood - Farewell` | Rejuvenation — Ana's Lament (`Ml8WWBKZ79s`) ⚠️ | NieR: Automata — Vague Hope Cold Rain (`Ez_c6qJkcbg`) |
| `Mood - Tension` | Rejuvenation — Dimensional Rift Battle (`rn5AI4_mfbc`) ⚠️ | Reborn — Atmosphere: Majesty Slowed (`llmgdHnFo8Q`) |

### Battles, Rivals, Wardens, War & Bosses (18 Slots)
- **Playlist URL:** `https://www.youtube.com/watch_videos?video_ids=mVPkrTapziE,ml6ajlfDyLE,Cn_dUvod_OE,2FMm402bhpk,QW8JrqrubQQ,d9FrTg8TRkI,paddC43Al1A,CXHrZpKJkQc,ZjbmOIDk9KU,NIlHPOK2p70,J9IwRWu70NQ,KQ4Fay0xn0Y,QdlUIgMRVPQ,tjYI_ie-kvw,q2DBeby7ni8,6wDr3SmdKKs,cOgnPxz3LAg,McyY7OZ9PkU`

| Slot (`final_name`) | Primary Pick | Alt / A-B Compare |
|---|---|---|
| `Battle - Wild` | GlitchxCity — Red & Blue Wild Battle 2026 (`mVPkrTapziE`) | GlitchxCity — Kanto Wild Battle XY Remix (`rWw6d56J-GE`) |
| `Battle - Trainer` | GlitchxCity — DPPt Trainer Battle Remix (`ml6ajlfDyLE`) | Trails in the Sky — Sophisticated Fight (`xHpzhJ5O2Cs`) |
| `Battle - Trainer (Late)` | GlitchxCity — Champions Arena Trainer (`Cn_dUvod_OE`) | GlitchxCity — BW Trainer Battle Remix (`UxsKutZbTcs`) |
| `Battle - Juno` | Blue Archive — RE Aoharu (`2FMm402bhpk`) | Blue Archive — Unwelcome School (`pEg_d2f6myw`) |
| `Battle - Kestrel` | Trails in the Sky — Silver Will (`QW8JrqrubQQ`) | Punishing: Gray Raven — To The Limit (`a545Gv3jGzg`) |
| `Battle - Warden` | Rejuvenation — Gym Leader Battle (`d9FrTg8TRkI`) ⚠️ | Octopath Traveler — Decisive Battle II (`-atmoakW2W8`) |
| `Battle - Warden (Special)` | Rejuvenation — Leader Angie Battle (`paddC43Al1A`) ⚠️ | Rejuvenation — Battle! The Angel of Ice (`vWAk02ZXuyc`) ⚠️ |
| `Battle - Warden Last` | GlitchxCity — SwSh Gym Leader Remix (`CXHrZpKJkQc`) | GlitchxCity — DPPt Gym Leader Remix (`Djn9ErGKcPg`) |
| `Battle - Hollow` | Rejuvenation — Xen Grunt Battle (`ZjbmOIDk9KU`) ⚠️ | Hollow Knight — Mantis Lords (`5IqjfubS6Ow`) |
| `Battle - Hollow Admin` | Rejuvenation — Xen Executive Battle (`NIlHPOK2p70`) ⚠️ | GlitchxCity — Team Galactic Boss Remix (`k5csqndnC7Q`) |
| `Battle - Mourner` | Punishing: Gray Raven — Lamia (`J9IwRWu70NQ`) | Hollow Knight — Sealed Vessel (`ze0Rk-m0w2A`) |
| `Battle - Voss` | **PGR — Out of My Hands (`KQ4Fay0xn0Y`) [Creator Pick]** | Rejuvenation — VS Madame X (`FRzN84EqlAA`) ⚠️ |
| `Battle - Boss` | GlitchxCity — Deoxys Battle Remix (`QdlUIgMRVPQ`) | NieR: Automata — Bipolar Nightmare (`btQBL-8fM3U`) |
| `Battle - Legendary` | GlitchxCity — Giratina Battle Remix (`tjYI_ie-kvw`) | GlitchxCity — DPPt Legendary Battle Remix (`GM-9R44lMxg`) |
| `Battle - Boss Final Bar` | Punishing: Gray Raven — Narwhal (`q2DBeby7ni8`) | Rejuvenation — Battle of the Soul (`TgOcv80DeII`) ⚠️ |
| `War - Beam Clash` | Punishing: Gray Raven — Hikari (`6wDr3SmdKKs`) | GlitchxCity — Ultra Necrozma Remix (`0JPfyxV_K94`) |
| `Battle - Festival Final` | Reborn — Elite 4 Battle Theme (`cOgnPxz3LAg`) | GlitchxCity — SV BBA Trainer Battle Remix (`E5UJ1iTwd5g`) |
| `Battle - Valen` | Reborn — Champion Battle Theme (`McyY7OZ9PkU`) | Octopath Traveler — Battle at Journey's End (`N34wHrmoym8`) |

---

## Sources

- Existing audio plan & slot naming: [`design/AUDIO.md`](../../design/AUDIO.md), [`audio/manifest.tsv`](../../audio/manifest.tsv), [`audio/install_audio.py`](../../audio/install_audio.py)
- Creator's outside-Pokémon calibration reference: [Punishing: Gray Raven — *Out of My Hands*](https://youtu.be/KQ4Fay0xn0Y)
- Artist & OST catalogs: [GlitchxCity](https://www.youtube.com/@GlitchxCity), Pokémon Rejuvenation / Reborn OSTs, Vanguard Sound (*Punishing: Gray Raven*), Yasunori Nishiki (*Octopath Traveler*), Christopher Larkin (*Hollow Knight*), Monster Siren (*Arknights*), Keiichi Okabe (*NieR: Automata*), Falcom Sound Team jdk (*Trails in the Sky*), Mitsukiyo/KARUT (*Blue Archive*), Dedrum (*Pokémon Tectonic*, CC BY-NC-SA 4.0)
- All 26 `.ogg` files under `Audio/BGS/` and `Audio/SE/` in this folder were synthesized from scratch using Python + `ffmpeg` + `vorbiscomment` — **100% original CC0 (Public Domain)**, zero external copyright issues.
