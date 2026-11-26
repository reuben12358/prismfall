# Prismfall — Audio plan (soundtrack, naming, wiring)

Owner: Audio. Staging: `audio/` (files + `manifest.tsv` + `install_audio.py`). Credits: `docs/CREDITS.md` → Music.
Last checked 2026-11-16. Covers SPINE Rev 1–6 (incl. the Ashkaar–Isenmar war and Festival highlight stings).

## 0. Where this stands (read first)

- **Every slot boots today** with a stand-in we have locally (62 staged slots + stock base-project files).
- **No GlitchxCity file is on disk.** Her tracks live on YouTube / Spotify / Bandcamp / SoundCloud, none reachable from
  this sandbox (shell is blocked; only GitHub clones work), and no GitHub repo mirrors them. You download them, name
  them per §3, drop them in `Audio/BGM`, and they replace the stand-ins with zero PBS changes.
- **"Copyright-free" needs a caveat.** A remixer can only license their own arrangement. The melodies stay
  Nintendo / Game Freak / Creatures property. Fangames live with that (non-commercial, credited); this is that same
  footing, not a clean licence. The only tracks here with a real licence are the Tectonic originals (CC BY-NC-SA 4.0).
- **Stand-in quality is unheard.** I matched by title and couldn't listen. The `.mid` stand-ins were written for GBA
  voicegroups, so through the base project's `soundfont.sf2` some instruments will be wrong. Treat them as temp track.

## 1. Artists and terms

| Artist | What | Terms found | Status |
|---|---|---|---|
| **GlitchxCity** ([YouTube](https://www.youtube.com/@GlitchxCity), [Bandcamp](https://glitchxcity.bandcamp.com/)) | Electronic Pokémon remixes; the fangame default (Rejuvenation commissioned her) | Channel: "Refer to each video description about usage. Please do not re-upload my videos without permission." 2018 tweet: content is "free to use on your streams". PokéCommunity advice: she and Vetrom are "happy to allow you to use their tracks as long as you credit them" ([thread](https://www.pokecommunity.com/threads/what-kinds-of-music-am-i-allowed-to-use-for-my-fangame.540032/)). | **Target artist. Per-video descriptions NOT read** (YouTube rate-limited/blocked here). Check each video's description before using; credit "GlitchxCity" + link. |
| **GlitchxCity tracks made for Rejuvenation** | "Battle - Gyms", "GDC - City of Dreams", Team Xen themes, "Battle - Soul" | Rejuvenation's asset guide lists these as **not allowed in other fangames** ([guide](https://rebornevo.com/forums/topic/73688-rejuvenation-assets-%E2%80%94-a-guide-on-usage-permissions-as-of-v135)). Same for Zumi and ShinPino tracks. | **Do not use**, even though Rev 6 allows Rejuvenation tilesets. |
| **Vetrom** | Pokémon remixes | Same PokéCommunity post: fine with credit. No first-party statement found. | Backup; confirm on the channel. |
| **Dedrum** (Pokémon Tectonic, lead composer) | 17 **original** tracks, `.ogg`/`.mp3` | Repo licence CC BY-NC-SA 4.0: credit, non-commercial, share-alike. | **Downloaded.** Cleanest licence we have. |
| **NMM / lequietriot** (Team Aqua's Asset Repo) | 126 FRLG-style MIDI arrangements of Pokémon themes | "Open Source, free to use… You can provide credit if you wish, although it is not required." | **Downloaded.** We credit anyway. |
| **nico, Celia Dawn, Kasen, ShinyDragonHunter, camgotay, Specker, quadrupleabatteries** (same repo) | 22 MIDIs (battle themes, dungeons, a few originals) | Repo: "free to use and edit by default", credit the creator. Specker: "credit preferred". | **Downloaded.** |
| meeowsie — [Meeow's Music](https://eeveeexpo.com/resources/1527/) | Gen 3-style arrangements | "free to use"; no credit rule stated | Not reachable (Google Drive). Optional. |
| TidusBeats / Scizor92 — [resource](https://eeveeexpo.com/resources/1285/) | 10 Pokémon-style originals, MP3+OGG | "Credits needed" | Not reachable (Eevee Expo blocked from shell). Optional. |
| seth_piano — [Seth's Ultima OST](https://eeveeexpo.com/resources/1836/) | Full pre-looped original fangame OST | Terms not read | Worth a look as a non-remix fallback. |
| ENLS Pre-Looped Library | Official game rips | n/a | **Not a remix source.** Official audio, off-brief. |

Rejected after download: Tectonic's `Battle *.ogg` set. The tags show official soundtrack rips (DPPt, BW2, SV) or
no provenance at all, so they were deleted from staging.

## 2. Formats and naming

- Essentials 21.1 resolves names without extension, trying `.mid .midi .ogg .wav .wma` (`FileTests.rb`
  `AUDIO_EXTENSIONS`; in the shipped 21.1 scripts `.mp3` is commented out of that list). **Use `.ogg`**: mkxp-z loops
  it from `LOOPSTART` / `LOOPLENGTH` Vorbis comments (in samples). **Never stage an `.mp3`**: `audio_exist?` does not
  see it, so the engine plays nothing (found 2026-11-25 with `Battle - Voss`, now an `.ogg`). `.mid` plays through
  `soundfont.sf2`.
- One file per name. If `Battle - Warden.mid` and `Battle - Warden.ogg` both exist, delete the stand-in
  (`install_audio.py --force` does it for the names it installs).
- Names follow the Reborn/Rejuvenation habit, `Category - Name`: `Title`, `Intro`, `Town`, `Route`, `Dungeon`, `Gym`,
  `Battle`, `Victory`, `Mood`, `Theme`, `War`, `Festival`, `Ending`. ASCII only, no apostrophes, **no colons**
  (`pbStringToAudioFile` reads `name:80:100` as volume and pitch).
- Folders: `Audio/BGM` (loops, and victory themes too: Essentials plays `VictoryBGM` out of `Audio/BGM`),
  `Audio/ME` (one-shot jingles), `Audio/BGS` (ambience loops), `Audio/SE`.
- Stock names (`Battle victory trainer`, `Credits`, `Evolution`, `Poke Center`…) are left alone; the kit never
  overwrites stock files.

## 3. Soundtrack plan

✔ = remix title seen in search results this session. "(confirm title)" = a pick from memory of her catalogue; check
it exists on the channel, or swap for any remix of the named source theme. Stand-in paths are under `audio/`;
"(stock base project)" files already ship with Essentials/EBDX. Everything in the last column is on disk; **every
"Target track" still needs downloading.**

### Front end

| Slot | File (Audio/…) | Target track | Stand-in we have now |
|---|---|---|---|
| Title screen | `BGM/Title - Prismfall.ogg` | GlitchxCity - Pokemon Main Theme / Title remix (pick one) ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `dedrum_tectonic/Tectonic_Intro.ogg` |
| Splash / boot | `BGM/Title - Boot.ogg` | (keep local original) | `dedrum_tectonic/Tectonic_Boot_Intro.ogg` |
| Prologue: the Dovetail ferry | `BGM/Intro - Last Ferry.ogg` | GlitchxCity - Undella Town or S.S. Anne remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `dedrum_tectonic/Tectonic_Mainland_Dock.ogg` |
| Intro lecture (Larch) / lab | `BGM/Intro - Larch Lab.mid` | GlitchxCity - Professor lab remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `nmm_lequietriot/mus_elm_lab.mid` |

### Towns

| Slot | File (Audio/…) | Target track | Stand-in we have now |
|---|---|---|---|
| Ferrow's Landing | `BGM/Town - Ferrows Landing.ogg` | GlitchxCity - Twinleaf / Littleroot Town remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `dedrum_tectonic/Tectonic_Casaba_Villa.ogg` |
| Elowen towns (Briarwick, Saltmere, Verdance, Gloaming) | `BGM/Town - Elowen.ogg` | GlitchxCity - Floaroma / Eterna City remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `dedrum_tectonic/Tectonic_Floral_Rest.ogg` |
| Antumbra towns (Lucent, Gravenmoor) | `BGM/Town - Antumbra.mid` | GlitchxCity - Lavender Town remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `nmm_lequietriot/mus_lavender_peace.mid` |
| Isenmar towns (Ebbmouth, Rimeholt) | `BGM/Town - Isenmar.ogg` | GlitchxCity - Snowpoint / Snowbelle City remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `dedrum_tectonic/Tectonic_Frostflow_Farms.ogg` |
| Ashkaar towns (Cindervault, Wyrmrest) | `BGM/Town - Ashkaar.mid` | GlitchxCity - Lavaridge / Blackthorn / Opelucid remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `nmm_lequietriot/mus_mt_ember.mid` |
| Ossaria towns (Duneholt, Cragholm) | `BGM/Town - Ossaria.mid` | GlitchxCity - Relic Castle / desert remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `nmm_lequietriot/mus_pewter.mid` |
| Zenith (Lumen City, Skyreach, Cogsworth) | `BGM/Town - Zenith.ogg` | GlitchxCity - Castelia / Lumiose / Nimbasa remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `dedrum_tectonic/Tectonic_Prizca_East.ogg` |
| Nadir (Mirefen, Ironreach, Underveil) | `BGM/Town - Nadir.ogg` | GlitchxCity - Virbank City / Po Town remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `dedrum_tectonic/Tectonic_Prizca_Unused.ogg` |
| Crownhaven (capital, Festival week) | `BGM/Town - Crownhaven.mid` | GlitchxCity - Pokemon League / PWT remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `nmm_lequietriot/mus_indigo_plateau_league.mid` |

### Routes

| Slot | File (Audio/…) | Target track | Stand-in we have now |
|---|---|---|---|
| Elowen routes | `BGM/Route - Elowen.ogg` | GlitchxCity - Route 209 / Route 10 remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `dedrum_tectonic/Tectonic_Scenic_Trail.ogg` |
| Elowen forest (Gossamer Wood, Glasswood) | `BGM/Route - Elowen Forest.ogg` | GlitchxCity - Eterna Forest remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `dedrum_tectonic/Tectonic_Repora_Forest.ogg` |
| Antumbra routes (behind the Glass) | `BGM/Route - Antumbra.ogg` | GlitchxCity - Distortion World / Old Chateau remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `dedrum_tectonic/Tectonic_Primal_Clay_Fear.ogg` |
| Isenmar routes | `BGM/Route - Isenmar.mid` | GlitchxCity - Route 216 remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `nmm_lequietriot/mus_ice_path.mid` |
| Ashkaar routes | `BGM/Route - Ashkaar.mid` | GlitchxCity - Mt. Chimney / Route 113 remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `nmm_lequietriot/mus_dragons_den.mid` |
| Ossaria routes | `BGM/Route - Ossaria.mid` | GlitchxCity - Route 111 desert / Route 4 (BW) remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `nmm_lequietriot/mus_route47.mid` |
| Zenith routes / skyways | `BGM/Route - Zenith.ogg` | GlitchxCity - X and Y Route 15 remix ([link](https://www.youtube.com/watch?v=ar6fbyeWj8U)) ✔ | `dedrum_tectonic/Tectonic_Sky_Walk.ogg` |
| Nadir tunnels / sumps | `BGM/Route - Nadir.mid` | GlitchxCity - Castelia Sewers / Team hideout remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `nmm_lequietriot/mus_rocket_warehouse.mid` |
| Borderland routes (default) | `BGM/Route - Borderlands.mid` | GlitchxCity - Route 1 / Route 201 remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `nmm_lequietriot/mus_route29.mid` |

### Dungeons

| Slot | File (Audio/…) | Target track | Stand-in we have now |
|---|---|---|---|
| Caves (generic) | `BGM/Dungeon - Cave.mid` | GlitchxCity - Mt. Moon / Union Cave remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `nmm_lequietriot/mus_dark_cave.mid` |
| Ruins / Ossuary of Dunes / Aurelia | `BGM/Dungeon - Ruins.ogg` | GlitchxCity - Ruins of Alph / Sealed Chamber remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `dedrum_tectonic/Tectonic_Regi_Dungeon.ogg` |
| Late dungeons / Victory-Road type | `BGM/Dungeon - Deep.mid` | GlitchxCity - Victory Road remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `nmm_lequietriot/mus_victory_road_cave.mid` |
| Haunted houses (Thistledown Manor, Vane Hall) | `BGM/Dungeon - Manor.mid` | GlitchxCity - Old Chateau / Strange House remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `nmm_lequietriot/mus_poke_mansion.mid` |
| Gym interiors | `BGM/Gym - Warden Hall.mid` | GlitchxCity - Gym remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `nmm_lequietriot/mus_gym_sinnoh.mid` |

### Battles

| Slot | File (Audio/…) | Target track | Stand-in we have now |
|---|---|---|---|
| Wild | `BGM/Battle - Wild.mid` | GlitchxCity - Wild Battle remix (DPPt or BW) ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `nmm_lequietriot/mus_vs_wild_sinnoh.mid` |
| Trainer | `BGM/Battle - Trainer.mid` | GlitchxCity - Trainer Battle remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `nmm_lequietriot/mus_vs_trainer_sinnoh.mid` |
| Rival Kestrel | `BGM/Battle - Kestrel.mid` | GlitchxCity - Rival Battle remix (Silver / Hugh) ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `nmm_lequietriot/mus_vs_rival.mid` |
| Rival Juno | `BGM/Battle - Juno.mid` | GlitchxCity - Hop / Hau / Wally battle remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `team_aquas_misc/nico/mus_vs_champion_nemona.mid` |
| Warden (gym leader) | `BGM/Battle - Warden.mid` | GlitchxCity - Gym Leader Battle remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `nmm_lequietriot/mus_vs_gym_leader_sinnoh.mid` |
| Warden, last Pokemon | `BGM/Battle - Warden Last.mid` | GlitchxCity - Gym Leader Last Pokemon (BW) remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `nmm_lequietriot/mus_vs_gym_leader_rematch.mid` |
| Hollow grunt | `BGM/Battle - Hollow.mid` | GlitchxCity - Team Plasma Theme / battle remix ([link](https://www.youtube.com/@GlitchxCity)) ✔ | `nmm_lequietriot/mus_vs_team_rocket.mid` |
| Hollow admin | `BGM/Battle - Hollow Admin.mid` | GlitchxCity - Team Magma and Aqua Boss Battle remix ([link](https://www.youtube.com/@GlitchxCity)) ✔ | `nmm_lequietriot/mus_vs_team_rocket_admin.mid` |
| Meridian agent | `BGM/Battle - Meridian.mid` | GlitchxCity - Team Galactic / Team Flare battle remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `team_aquas_misc/nico/mus_vs_cipher_admin.mid` |
| Meridian admin (Marchetti, Kroll, Quent) | `BGM/Battle - Meridian Admin.mid` | GlitchxCity - Galactic Commander / Colress battle remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `team_aquas_misc/camgotay/hgss_rocket_hideout.mid` |
| The Mourner | `BGM/Battle - Mourner.mid` | GlitchxCity - N Battle / Ghetsis remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `nmm_lequietriot/mus_vs_team_rocket_boss.mid` |
| Aurelian Voss | `BGM/Battle - Voss.ogg` | GlitchxCity - Lysandre / Cyrus / Rose battle remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `dedrum_tectonic/Tectonic_Yezera_Battle_Theme.ogg` |
| Legendary (catchable) | `BGM/Battle - Legendary.mid` | GlitchxCity - Giratina Battle remix ([link](https://www.youtube.com/watch?v=tjYI_ie-kvw)) ✔ | `team_aquas_misc/nico/mus_bw_vs_legendary.mid` |
| Boss (multi-bar) | `BGM/Battle - Boss.mid` | GlitchxCity - Deoxys Battle remix ([link](https://www.youtube.com/watch?v=QdlUIgMRVPQ)) ✔ | `nmm_lequietriot/mus_vs_legend.mid` |
| Boss, final bar | `BGM/Battle - Boss Final Bar.mid` | GlitchxCity - Ultra Necrozma / Zinnia remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `team_aquas_misc/ShinyDragonHunter/mus_c_vs_legend_beast.mid` |
| Festival bracket | `BGM/Battle - Festival.mid` | GlitchxCity - PWT / Battle Subway remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `nmm_lequietriot/mus_vs_rank_match.mid` |
| Festival final rounds (SF/Final) | `BGM/Battle - Festival Final.mid` | GlitchxCity - PWT Final Round remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `nmm_lequietriot/mus_vs_elite_four.mid` |
| Champion Valen | `BGM/Battle - Valen.mid` | GlitchxCity - Champion Cynthia remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `nmm_lequietriot/mus_cynthia.mid` |
| Arceus finale | `BGM/Battle - Arceus.ogg` | GlitchxCity - Arceus Battle remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `dedrum_tectonic/Tectonic_Epitaph_of_the_Demiurge.ogg` |
| Ruin Route | `BGM/Battle - Ruin.mid` | GlitchxCity - Giratina Battle remix (pitch 90) or a second dark remix ([link](https://www.youtube.com/watch?v=tjYI_ie-kvw)) ✔ | `team_aquas_misc/Celia Dawn/mus_dmca_battle.mid` |
| Sidequest cameo fights | `BGM/Battle - Cameo.mid` | GlitchxCity - Battle Frontier Brain remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `team_aquas_misc/Kasen/mus_vs_iris.mid` |

### Victory

| Slot | File (Audio/…) | Target track | Stand-in we have now |
|---|---|---|---|
| Wild victory | `BGM/Battle victory wild` | keep stock | `(stock base project)` |
| Trainer victory | `BGM/Battle victory trainer` | keep stock | `(stock base project)` |
| Warden / boss victory | `BGM/Battle victory leader` | keep stock | `(stock base project)` |
| Festival round won | `BGM/Victory - Festival` | keep stock track | `(stock base project) B2W2 213 Winning in the PWT!` |
| Champion / Festival won | `BGM/Victory - Sovereign` | keep stock track | `(stock base project) B2W2 214 PWT Victor!` |

### Mood

| Slot | File (Audio/…) | Target track | Stand-in we have now |
|---|---|---|---|
| Emotional | `BGM/Mood - Emotion.mid` | GlitchxCity - Emotion (BW) remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `nmm_lequietriot/mus_kanto_emotion.mid` |
| Farewell / loss | `BGM/Mood - Farewell.mid` | GlitchxCity - N's Farewell remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `nmm_lequietriot/mus_lavender_peace_intro.mid` |
| Tension | `BGM/Mood - Tension.mid` | GlitchxCity - Looker / Unwavering Emotions remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `nmm_lequietriot/mus_encounter_rocket_boss.mid` |
| Mystery / the Bleed | `BGM/Mood - Mystery.ogg` | GlitchxCity - Lake Guardians / Mt. Pyre remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `dedrum_tectonic/Tectonic_Primal_Clay.ogg` |
| Hollow theme | `BGM/Theme - Hollow.mid` | GlitchxCity - Team Plasma Theme ([link](https://www.youtube.com/@GlitchxCity)) ✔ | `nmm_lequietriot/mus_encounter_rocket.mid` |
| Meridian theme | `BGM/Theme - Meridian.mid` | GlitchxCity - Team Galactic HQ / Silph Co. remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `nmm_lequietriot/mus_global_terminal_tower.mid` |
| Accord / Valen theme | `BGM/Theme - Accord.mid` | GlitchxCity - Champion encounter / League remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `nmm_lequietriot/mus_indigo_plateau.mid` |
| Rival encounter | `BGM/Theme - Kestrel.mid` | GlitchxCity - Rival encounter remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `nmm_lequietriot/mus_encounter_johto_shady.mid` |

### War (Rev 6)

| Slot | File (Audio/…) | Target track | Stand-in we have now |
|---|---|---|---|
| War march (mustering, fronts) | `BGM/War - March.mid` | GlitchxCity - Victory Road / Route 10 (BW) remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `nmm_lequietriot/mus_route23_badge7.mid` |
| Battlefield (maps + war battles) | `BGM/War - Battlefield.mid` | GlitchxCity - Battle Dialga/Palkia or Zekrom/Reshiram remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `team_aquas_misc/nico/mus_waterfall_colosseum.mid` |
| Beam-clash cutscene climax | `BGM/War - Beam Clash.mid` | GlitchxCity - Kyurem / Rayquaza battle remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `team_aquas_misc/camgotay/hgss_entei_battle.mid` |
| Aftermath | `BGM/War - Aftermath.mid` | GlitchxCity - Mt. Pyre / Emotion remix (slow) ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `team_aquas_misc/Specker/mus_sadpop.mid` |

### Festival highlights (Rev 6)

| Slot | File (Audio/…) | Target track | Stand-in we have now |
|---|---|---|---|
| Highlight intro sting | `ME/Festival highlight start` | cut 3-5 s from the Festival battle remix | `(stock base project) ME: BP Fanfare` |
| Key-moment sting (KO, clutch) | `ME/Festival highlight hit` | cut 2-3 s hit from the same remix | `(stock base project) ME: Slots win` |
| Match result sting | `ME/Festival highlight result` | cut 4-6 s cadence | `(stock base project) ME: Slots big win` |
| Highlight reel bed (loop under the cutscene) | `BGM/Festival - Highlights` | GlitchxCity - PWT remix (same as bracket, lower volume) ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `(stock base project) B2W2 212 PWT Final Round!` |

### Endings

| Slot | File (Audio/…) | Target track | Stand-in we have now |
|---|---|---|---|
| Game over | `ME/Prismfall game over` | short cut from Mood - Farewell | `(stock base project) ME: Voltorb Flip game over` |
| Ending: Good / Grey (hopeful) | `BGM/Ending - Homecoming.ogg` | GlitchxCity - Ending / Hall of Fame remix ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `dedrum_tectonic/Tectonic_Casaba_Villa_Remix.ogg` |
| Ending: Bad / Ruin | `BGM/Ending - Ruin.mid` | GlitchxCity - Lavender Town remix (pitch 85) ([link](https://www.youtube.com/@GlitchxCity)) (confirm title) | `team_aquas_misc/ShinyDragonHunter/mus_rg_sevii_dungeon.mid` |
| Credits | `BGM/Credits` | keep stock name (Scene_Credits::BGM) | `(stock base project)` |

**Ambience and cutscene SE:** the nine `Audio/BGS` loops and the cutscene / battle SE are staged in
`audio/gemini_cc0/` (CC0 pack; the BGS are the v5 field-audio loops since 2026-11-25). Three cues named in the
cinematics spec have no file of their own yet (`Blade Pierce`, `Mask Crack`, `Bell Break`); the nearest CC0 hit stands in.

Install the stand-ins: `python3 audio/install_audio.py <game project>` (skips any name already present).

## 4. Wiring guide (keys verified against `ref/essentials` and `ref/ebdx`)

| What | Where | Key / call |
|---|---|---|
| Map music and ambience | `design/MAP_AUDIO.yaml` (one row per built map: `bgm`, `bgs`, volumes, `rain`). `mapgen/map_audio.py` writes `Prismfall Maps/013_MapAudio.rb`, which patches the map as it loads, only with installed files. | Edit the yaml, run `python3 -I mapgen/map_audio.py` (or any `build.py`). A spec's `map_audio: {...}` block wins for its map. The spec's `bgm:` is baked into the map file and plays when the Prismfall track is not installed. |
| Per-map battle music | `PBS/map_metadata_prismfall.txt` | `WildBattleBGM`, `TrainerBattleBGM`, `WildVictoryBGM`, `TrainerVictoryBGM`, `WildCaptureME` |
| Global defaults | `PBS/metadata.txt` section `[0]` | same five keys plus `SurfBGM`, `BicycleBGM` |
| Trainer music | `PBS/trainer_types_prismfall.txt` | `IntroBGM` (eye-contact theme), `BattleBGM`, `VictoryBGM` |
| EBDX override | `PBS/EBDX/trainers.txt`, `pokemon.txt`, `maps.txt` | `BattleBGM`, `VictoryTheme` (optional; trainer_types is enough) |
| One-off override | event script before the battle | `$PokemonGlobal.nextBattleBGM = "Battle - Boss"`, `nextBattleVictoryBGM`, `nextBattleCaptureME`. Wins over everything above. |
| Bosses | `Prismfall Bosses` registry | `:music` (battle BGM) and `:music` inside a `:breaks` entry (phase change, `pbBGMPlay`) |
| Festival | `Prismfall Core/008_Festival_Data.rb` `RULESETS` | no music key today; see edit C3 |
| Game over | `Prismfall Core/017_GameOver.rb` | `GAME_OVER_ME` constant, per-entry `:me` in `GAME_OVERS` (plays from `Audio/ME`) |
| Title screen | `Data/System.rxdata` `title_bgm`, currently `"Title"` | RMXP Database → System → Title BGM, or edit C5 |
| Credits / evolution / Hall of Fame | hard-coded names | `Scene_Credits::BGM = "Credits"`, `"Evolution"`, `HALL_OF_FAME_BGM = "Hall of Fame"` |
| Cutscene / mood | events or `Prismfall Cutscenes` | `pbBGMPlay("Mood - Tension")`, `pbBGMFade(1.0)`, `pbMEPlay("Festival highlight hit")`, `pbBGSPlay`, `pbSEPlay` |

Battle BGM priority (`003_Utilities_BattleAudio.rb`): `nextBattleBGM` → trainer type → map metadata → global
metadata → `"Battle trainer"` / `"Battle wild"`.

## 4b. What is wired (Audio v4.3, 2026-11-25)

| Area | State |
|---|---|
| Maps | All 117 built maps have a `MAP_AUDIO.yaml` row: 103 with a Prismfall BGM (Poké Centers / Marts keep stock), 60 with an ambience loop, 57 interiors that stop the loop. `Rain` replaces the ambience while it rains. |
| Trainer types | `BattleBGM` / `IntroBGM` per §5.A in `pbs/trainer_types.txt` (every type except the Gilded King, whose music is on hold). `Prismfall Core/031_AudioCues.rb` plays the old stock track while a file is not installed. `VictoryBGM` is still stock: `Victory - Sovereign` has no staged file. |
| Jingles | `Warden Badge Get` (new badge), `Trial Rank Up` (rank message), `Prismfall game over`. |
| Battle SE | `Boss Shield Break` (a boss bar breaks), `Field Shatter` / `Glass Quench` (field changes), `Prism Arena Swell` (the Plates turn), `VS Cutin Lightning` (VS intro bolts). |
| Boss music | A wild boss with no `:music` gets `Battle - Boss` (`Battle - Legendary` if it can be caught, `Battle - Arceus` for Arceus) and `Battle - Boss Final Bar` on its last bar. |
| Title | `Title - Prismfall` when installed. |
| Voices | `Prismfall Cutscenes/014_Portraits_Voice.rb`: `Voice - <Name>` blips on tagged, carried and "Name: " lines. Options > Voice Blips turns them off. |
| Cutscene cues | `Prismfall::Cutscene::AUDIO` (`001_Config.rb`): 90 cues, each ending on a file that exists. |
| Not wired yet | Festival ruleset music (§5.C3), ending themes (§5.C4), per-boss `:music` in the boss files, `metadata.txt` global battle BGMs (§5.B), the bespoke `Battle - Warden <Name>` themes (no files). |

The dev kit does not ship audio: run `python3 audio/install_audio.py <game project>` (add `--force` to replace older loops).

## 5. Integration edits (for other owners; I changed none of these files)

**A. Trainer data — `pbs/trainer_types.txt`**
| Sections | BattleBGM | Also |
|---|---|---|
| all `LEADER_*` (incl. `LEADER_ROWAN`), `ECHO_MORWEN` | `Battle - Warden` | `VictoryBGM = Battle victory leader` (unchanged) |
| `RIVAL_KESTREL` | `Battle - Kestrel` | `IntroBGM = Theme - Kestrel` |
| `RIVAL_JUNO` | `Battle - Juno` | |
| `CHAMPION_VALEN` | `Battle - Valen` | `IntroBGM = Theme - Accord`, `VictoryBGM = Victory - Sovereign` |
| `HOLLOW_GRUNT*` | `Battle - Hollow` | `IntroBGM = Theme - Hollow` |
| `HOLLOW_ADMIN`, `_WICK`, `_THISTLE`, `_TEO`, `_SABLE` | `Battle - Hollow Admin` | `IntroBGM = Theme - Hollow` |
| `HOLLOW_MOURNER` | `Battle - Mourner` | |
| `MERIDIAN_AGENT*` | `Battle - Meridian` | `IntroBGM = Theme - Meridian` |
| `MERIDIAN_ADMIN`, `_MARCHETTI`, `_KROLL`, `_ASHE`, `_QUENT`, `_DIRECTORATE` | `Battle - Meridian Admin` | `IntroBGM = Theme - Meridian` |
| `MERIDIAN_VOSS`, `GILDED_AURELIUS` | `Battle - Voss` | |
| `FESTIVAL_*` (now sidequest cameos, Rev 4) | `Battle - Cameo` | |
| `REFLECTION` | `Battle - Ruin` | |
Also fix the header comment on line 3 (it says BGM names are stock).

**B. Base project — `PBS/metadata.txt` `[0]`** (SETUP.md step, since the kit doesn't ship this file):
`WildBattleBGM = Battle - Wild`, `TrainerBattleBGM = Battle - Trainer`. Leave the victory keys stock.

**C. Core / Bosses / Cutscenes plugins**
1. `017_GameOver.rb`: `GAME_OVER_ME = "Prismfall game over"`.
2. Bosses registry: `:music => "Battle - Boss"` as default, `"Battle - Legendary"` for catchable ones, Arceus
   `"Battle - Arceus"`; in each boss's last `:breaks` entry add `:music => "Battle - Boss Final Bar"`.
3. `008_Festival_Data.rb` + `009_Festival.rb`: add `:bgm` / `:victory_bgm` to `RULESETS` and, in
   `apply_battle_rules`, set `$PokemonGlobal.nextBattleBGM = rules[:bgm] if rules[:bgm]` (same for
   `nextBattleVictoryBGM`). Values: `:bracket`, `:bracket_qf`, `:exhibition` → `Battle - Festival` /
   `Victory - Festival`; `:bracket_sf`, `:bracket_final` → `Battle - Festival Final`; `:finale` → leave nil so
   Voss's trainer type and the Arceus boss `:music` apply. Caveat: this overrides rival themes in the bracket. If
   Kestrel/Juno/Valen should keep their own themes there, only set it when the opponent's type has the default BGM.
4. Endings (`012_Narrative_Data.rb` `ENDINGS`): add `:bgm` per ending (`Ending - Homecoming` for good/grey,
   `Ending - Ruin` for bad/ruin) and play it in `Endings.trigger` before the credits.
5. Title: at boot, `$data_system.title_bgm = RPG::AudioFile.new("Title - Prismfall", 100, 100)` (alias-chained),
   or set it once in RMXP's database. Keeps stock `Title.ogg` untouched.
6. `Prismfall Cutscenes` (not in `plugins/` yet): expose `bgm:`, `me:`, `se:` per step. War climax script:
   `War - Battlefield` → fade 0.5 s → `War - Beam Clash` on the clash frame → cut to silence on the break →
   `War - Aftermath`. Festival highlights: `Festival - Highlights` at volume 70 with the three `Festival highlight *`
   MEs. Note an ME pauses the BGM while it plays, so keep them under ~5 s or ship them as SE instead.

**D. Mapgen specs (`bgm:`)** — current specs use stock `Lappet Town`, `Lerucean Town`, `Route 1–3`, `Gym`, `Islands`.
| Spec | bgm |
|---|---|
| `109_dovetail` | `Intro - Last Ferry` |
| `100/101_ferrows_landing*` | `Town - Ferrows Landing` (lab interior: `Intro - Larch Lab`) |
| `120/121_briarwick*`, `140/141_saltmere*` | `Town - Elowen` |
| `160/161_ebbmouth*` | `Town - Isenmar` |
| `130`, `150`, `170` gyms | `Gym - Warden Hall` |
| `520`, `521`, `540` routes | `Route - Elowen`; `560` → `Route - Borderlands` (Elowen→Isenmar) |
| `522_glassed_orchard` | `Mood - Mystery` |
| `524`, `525` woods | `Route - Elowen Forest` |
| `544_brinecut_mine` | `Dungeon - Cave` |
| later kingdoms | `Town - <Kingdom>` / `Route - <Kingdom>` per §3 |
Poké Center / Mart interiors keep stock `Poke Center` / `Poke Mart`. War-time revisits of Ashkaar/Isenmar maps
swap to `War - March` by event (`Change Map BGM`), not by spec.

## 6. Blockers and fallbacks

| Wanted | Blocked because | Reachable fallback |
|---|---|---|
| GlitchxCity audio files | YouTube/Bandcamp/SoundCloud/Spotify unreachable; not on GitHub | Dedrum originals + NMM MIDIs (staged). User downloads the remixes. |
| GlitchxCity per-video usage text | YouTube fetches rate-limited or refused | Channel-level statement + community thread (quoted in §1). Confirm before release. |
| Eevee Expo packs (Meeow, TidusBeats, Seth) | Eevee Expo and Google Drive blocked from shell | Team Aqua's Asset Repo on GitHub (staged) |
| Listening / loop-point check | no audio playback here | Loop tags must be set by ear (Audacity → export OGG with `LOOPSTART`/`LOOPLENGTH`) |
