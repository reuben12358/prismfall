# Audio-to-Cutscene Sync, Expanded-Cast Soundtrack & DJ Chroma Jukebox Addendum (v4.4)

- **Date:** 2026-11-23
- **Author:** Gemini (Audio-to-Cutscene & Expanded-Cast Soundtrack Sync Director)
- **Addendum To:** [`WIRING_SPEC.md`](file:///home/antigravity/reuben12358/prismfall/gemini_recommends/2026-11-21_audio-mastering-and-soundscape/WIRING_SPEC.md) & [`PROPOSAL.md` (v4.3)](file:///home/antigravity/reuben12358/prismfall/gemini_recommends/2026-11-21_audio-mastering-and-soundscape/PROPOSAL.md)
- **Cross-Verified Against:**
  - [`gemini_recommends/2026-11-22_rejuv-v14-cutscene-cinematics-spec/PROPOSAL.md`](file:///home/antigravity/reuben12358/prismfall/gemini_recommends/2026-11-22_rejuv-v14-cutscene-cinematics-spec/PROPOSAL.md) (30 Anime Cutscenes + Layer 0 Anime Juice)
  - [`gemini_recommends/2026-11-22_unique-trainer-classes-and-expanded-cast/CLASSES_PROPOSAL.md`](file:///home/antigravity/reuben12358/prismfall/gemini_recommends/2026-11-22_unique-trainer-classes-and-expanded-cast/CLASSES_PROPOSAL.md) (8 New Villain Sub-Bosses + Bespoke Classes)
  - [`gemini_recommends/2026-11-22_unique-trainer-classes-and-expanded-cast/SIDE_CAST_PROPOSAL.md`](file:///home/antigravity/reuben12358/prismfall/gemini_recommends/2026-11-22_unique-trainer-classes-and-expanded-cast/SIDE_CAST_PROPOSAL.md) (14 New Recurring Side Characters + 12 Elevated NPCs + DJ Chroma's Jukebox)
  - [`audio/manifest.tsv`](file:///home/antigravity/reuben12358/prismfall/audio/manifest.tsv) (92 live staged rows), `audio/gemini_cc0/` (19 stale files), `gemini_recommends/2026-11-21_audio-mastering-and-soundscape/Audio/` (50 mastered v4.3 CC0 `.ogg`s), [`001_Config.rb`](file:///home/antigravity/reuben12358/prismfall/plugins/Prismfall%20Cutscenes/001_Config.rb), and [`014_Portraits.rb`](file:///home/antigravity/reuben12358/prismfall/plugins/Prismfall%20Cutscenes/014_Portraits.rb)
- **Status:** Ready for Claude (Wednesday Engine Sprint) & Gemini DSP Synthesis Pass — zero edits made to `.rb`, `pbs/`, or `story/`.

---

## Executive Audit Summary (Critical Silence & Collision Bugs Caught)

1. **16 / 30 Cutscenes Would Play Silent BGM Today if Wired Literally:** The 30-cutscene spec cites **Phase-2 145-track OST slot names** (plus 3 shortened/mismatched labels: `War - Frontlines` vs `War - March`, `Battle - Sovereign Valen` vs `Battle - Valen`, and `Boss - Loyal Three` vs `Boss - Pecharunt & Loyal Three`) that do **not** exist in [`audio/manifest.tsv`](file:///home/antigravity/reuben12358/prismfall/audio/manifest.tsv) yet. Section 1B provides a drop-in [`AUDIO`](file:///home/antigravity/reuben12358/prismfall/plugins/Prismfall%20Cutscenes/001_Config.rb#L67-L90) fallback table (`[Phase-2 filename, Phase-1 manifest.tsv filename, stock fallback]`) so **0 / 30 cutscenes ever play silent** and all 30 automatically upgrade the day Phase-2 tracks drop in.
2. **3 Critical Missing Cutscene SEs & 9 Missing Anime Juice SEs:**
   - **`Directorate Rifle Crack.ogg`** is completely missing — Scene `#19` (`:CH16_ZEKROM_CLEAR_AIR`, Wenlow's Quiet Ward sacrifice) calls for a single stark gunshot into silence and would play **completely silent** today.
   - **`Beam fire.ogg`** is referenced in [`001_Config.rb:69`](file:///home/antigravity/reuben12358/prismfall/plugins/Prismfall%20Cutscenes/001_Config.rb#L69) and Scenes `#10`, `#23`, `#25`, yet does **not** exist in the 50-file CC0 pack (falling back only to stock `Anim/HyperBeam`).
   - **`Ferry Foghorn.ogg`** is requested in Scene `#1` (`:PRO_DOVETAIL_ARRIVAL` Shot 1) and does not exist anywhere.
   - Section 4 specifies all **12 pure-DSP CC0 anime cutscene SEs** Gemini can synthesize & ear-audit right now (zero image quota needed!).
3. **11 Existing Cutscene / VS-Bust Speakers Missing `Voice - *.ogg`:** The 50-file CC0 pack contains **25 / 25** core cast voices, but **5 / 31** EBDX VS busts (`MARCHETTI`, `KROLL`, `QUENT`, `SABLE`, `THISTLE` — note Scene `#10` explicitly calls `Voice - Quent`!) and **6** speaking cutscene actors (`CALLA`, `TEO`, `PIP`, `WENLOW`, `MORWEN`, `DASK`/`THEODRIC`) are unvoiced. Section 2E maps their exact fallback pitches and DSP synthesis targets.
4. **Expanded-Cast OST Discipline (`145 → 151` Tracks, +6 Genre-Gap Signatures Only):** Rather than bloating the OST by 22 tracks, Section 2 cleanly reuses existing Phase-1/Phase-2 themes for 14 of the 22 new characters and identifies **exactly 6 high-impact pure-instrumental signature themes (`#146–#151`)** worth sourcing (*DJ Chroma*, *Field Hunter Kal*, *Captain Orson Superboss*, *Simeon Finch*, *Ezra/Scherzo*, *Cormac/Malachi*), plus **23 acoustic-verified CC0 Voice specs** calibrated against the real measured fundamentals (`88–588 Hz`, `53–91 ms`) of our 25 existing `.ogg` blips.
5. **Cross-Proposal Naming Collision Caught (`:SLOANE`):** Both [`CLASSES_PROPOSAL.md`](file:///home/antigravity/reuben12358/prismfall/gemini_recommends/2026-11-22_unique-trainer-classes-and-expanded-cast/CLASSES_PROPOSAL.md) (`WILDCARD_SLOANE` — Glassrunner Sloane Vargo) and [`SIDE_CAST_PROPOSAL.md`](file:///home/antigravity/reuben12358/prismfall/gemini_recommends/2026-11-22_unique-trainer-classes-and-expanded-cast/SIDE_CAST_PROPOSAL.md) (`SIDE_INTERNS` — Intern Bret & Intern Sloane Pendergast) claim portrait ID `:SLOANE` and `Voice - Sloane.ogg`. Section 2 flags the clean disambiguation (`:SLOANE` vs `:INTERN_SLOANE`, or renaming Intern Sloane before Wednesday merge).
6. **DJ Chroma's `Prismfall::Jukebox` (`18.0 FM — Radio Free Prism`):** Section 3 delivers a drop-in, save-compatible, boss-safe Ruby hook (`plugins/Prismfall Core/027_Jukebox.rb`) using `Prismfall.state.custom[:jukebox]` and code-drawn Pause Menu UI.

---

## 1. 30-Cutscene + Layer 0 Audio Cue Verification Matrix

### 1A. Complete Cue Audit (`Layer 0` + Scenes `#1`–`#30`)

> **Legend:**
> - **Live Phase-1 (`manifest.tsv` / 50-Pack):** Exact filename present today in [`audio/manifest.tsv`](file:///home/antigravity/reuben12358/prismfall/audio/manifest.tsv) or the mastered 50-file CC0 pack in `gemini_recommends/2026-11-21_audio-mastering-and-soundscape/Audio/` *(prerequisite: sync all 50 CC0 `.ogg`s → `audio/gemini_cc0/` per [`WIRING_SPEC.md` §4B](file:///home/antigravity/reuben12358/prismfall/gemini_recommends/2026-11-21_audio-mastering-and-soundscape/WIRING_SPEC.md#L128-L132))*.
> - **Phase-2 (145-Track OST):** Exact canonical filename once the v4.3 145-track OST is installed.
> - **Flags:** `OK` = verified on disk today; `P1-FALLBACK` = `PROPOSAL.md` name is Phase-2-only (must use `AUDIO` alias); `NAME-FIX` = cue string mismatch; `NEW-SE` = needs Section 4 CC0 SFX; `MISSING-VOICE` = speaker lacks `Voice - *.ogg` in 25-voice pack.

| # | Scene ID (Ch) | `PROPOSAL.md` Requested BGM | Exact Phase-1 BGM (`manifest.tsv`) | Exact Phase-2 BGM (145-OST) | Exact BGS / ME (`Audio/BGS`, `Audio/ME`) | Exact SE & Cast Voices (`Audio/SE`) | Verification Flags & Fixes |
|---:|---|---|---|---|---|---|---|
| **L0** | **Layer 0** `cutin_flash` / `chapter_card` / `cine_bars` | *(inherits active battle/map BGM)* | *(none)* | *(none)* | — | `VS Cutin Lightning`, `Boss Shield Break`, `Field Shatter`, `Prism Arena Swell`, 25× `Voice - *.ogg` | `P1-FALLBACK`: add `:vs_lightning`, `:boss_shield`, `:field_shatter`, `:prism_swell` to `001_Config.rb`. `NEW-SE`: `Ace Eye-Flash Zing`, `Chapter Card Prismatic Wipe`, `Glitch Tear Static` (Ruin cards). `MISSING-VOICE`: 5 VS busts (`Marchetti`, `Kroll`, `Quent`, `Sable`, `Thistle`). |
| **1** | `:PRO_DOVETAIL_ARRIVAL` (Ch0) | `Intro - Last Ferry` (#76) | `Intro - Last Ferry` | `Intro - Last Ferry` (#76) | BGS: `Saltmere Harbor` | SE: `Prism Arena Swell` (p75), `Glass Quench`, **`ship horn`** · Voice: `Voice - Voss`, *(Calla)* | `NEW-SE`: **`ship horn` does not exist** → synthesize `Ferry Foghorn` (interim: `Prism Arena Swell` p60) + `Glitch Tear Static` (Shot 5 CRT). `MISSING-VOICE`: `Calla`. |
| **2** | `:CH1_GLASSED_ORCHARD` (Ch1) | `Dungeon - Bleed Zones` (#74) | `Mood - Mystery` *(or `Route - Antumbra`)* | `Dungeon - Bleed Zones` (#74) | BGS: `Glassfall Bleed` | SE: `Glass Quench`, `VS Cutin Lightning` (`cutin_flash :JUNO`) · Voice: `Voice - Juno`, `Voice - Larch` | `P1-FALLBACK`: `Dungeon - Bleed Zones` not in `manifest.tsv` → alias `:bgm_bleed_zone`. |
| **3** | `:CH2_PAGEANT_MOURNER` (Ch2) | `Town - Elowen` (#6) → silence → `Theme - Hollow` (#82) | `Town - Elowen` → `Theme - Hollow` | `Town - Saltmere` (#6) → `Theme - Hollow` (#82) | — | SE: `Crowd gasp`, `Field Shatter`, `Beam break` · Voice: `Voice - Mourner`, `Voice - Juno` | `OK` for all BGM/Voices. `NEW-SE`: `Impact Hitstop Boom` (Shot 2 blackout `sakuga_flash`), `Heartbeat Sub-Pulse` (Shot 5 eye-lock), `Chapter Card Prismatic Wipe` (`title_slam`). |
| **4** | `:CH3_GLASS_MATRIARCH` (Ch3) | `Mood - Mystery` (#77) | `Mood - Mystery` | `Mood - Mystery` (#77) | BGS: `Glassfall Bleed` | SE: `Glass Quench` (p75 drain / p125 ping), `Boss Shield Break` · Voice: `Voice - Tamsin` | `OK` for all BGM/BGS/Voices. `NEW-SE`: `Glitch Tear Static` (`:silence` branch tell). |
| **5** | `:CH4_NIGHT_EBB_STOPPED` (Ch4) | `Mood - Tension` (#78) | `Mood - Tension` | `Mood - Tension` (#78) | BGS: `Saltmere Harbor` (vol 65→95) | SE: `Beam break`, `Field Shatter`, `VS Cutin Lightning` (`:MARISOL`) · Voice: `Voice - Marisol`, `Voice - Larch`, *(Teo)* | `OK` for BGM/BGS. `NEW-SE`: `Impact Hitstop Boom` (Shot 2 sluice lock). `MISSING-VOICE`: `Teo`. |
| **6** | `:CH5A_SPIRE_SHATTER` (`SH1`, Ch5) | `Theme - Meridian` (#81) → `Mood - Tension` (#78) → silence | `Theme - Meridian` → `Mood - Tension` | `Theme - Meridian` (#81) → `Mood - Tension` (#78) | BGS: `Machinery - Zenith` | SE: `Boss Shield Break`, `Beam charge`, `VS Cutin Lightning`, `Field Shatter` · Voice: `Voice - Voss`, `Voice - Mourner`, `Voice - Rook`, *(Sable)* | `OK` for BGM/BGS. `NEW-SE`: `Impact Hitstop Boom` (Shot 4 3f `impact_cg`), `Glass Shatter Burst` (Shot 5 28-shard Voronoi), `Heartbeat Sub-Pulse` (Shot 1 Dark Stone). `MISSING-VOICE`: `Sable`. |
| **7** | `:CH5B_LOWLIGHT_TWELVE` (Ch5) | `Mood - Farewell` (#79) | `Mood - Farewell` | `Mood - Farewell` (#79) | BGS: `Glassfall Bleed` | SE: `Glass Quench` · Voice: `Voice - Rook`, `Voice - Valen` | `OK` (100% live today after 50-pack sync). `NEW-SE`: `Chapter Card Prismatic Wipe` (Act I end card). |
| **8** | `:CH6_OSSUARY_MURALS` (Ch6) | `Dungeon - Ruins` (#65) | `Dungeon - Ruins` | `Dungeon - Ruins` (#65) | BGS: `Wind - Isenmar` (opt. vol 30, p85) | SE: `Prism Arena Swell` (p85), `Glass Quench`, `VS Cutin Lightning` (`:KESTREL`) · Voice: `Voice - Sahar`, `Voice - Kestrel` | `OK` (100% live today — `Dungeon - Ruins` is already Dedrum `Regi_Dungeon`). |
| **9** | `:CH7_QUIET_WARD_NIGHT` (Ch7) | `Town - Nadir` (#37) → `Mood - Tension` (#78) → `Mood - Emotion` (#80) | `Town - Nadir` → `Mood - Tension` → `Mood - Emotion` | `Town - Mirefen` (#37) → `Mood - Tension` (#78) → `Mood - Theme of Hope` (#80) | BGS: `Drip - Nadir` → `Glassfall Bleed` | SE: `Glass Quench` · Voice: `Voice - Corvin`, `Voice - Juno`, *(Sable)* | `OK` on Phase-1 names! Alias `:bgm_mirefen` & `:bgm_mood_hope` for Phase-2 auto-upgrade. `NEW-SE`: `Glitch Tear Static` (Shot 1 hijack). `MISSING-VOICE`: `Sable`. |
| **10** | `:CH8_CALDERA_CRISIS` (Ch8) | `Route - Ashkaar` (#46) → **`War - Frontlines`** (#84) | `Route - Ashkaar` → **`War - March`** | `Route - Ashkaar` (#46) → `War - Frontlines` (#84) | BGS: `Lava - Ashkaar` | SE: `Field Shatter`, **`Beam fire`**, `VS Cutin Lightning` (`:QUENT`, `:SIGRUN`) · Voice: `Voice - Sigrun`, `Voice - Brann`, **`Voice - Quent`** | **3 FLAGS:** `NAME-FIX` (`War - Frontlines` → `War - March` in P1); `NEW-SE` (`Beam fire.ogg` missing from CC0 pack); `MISSING-VOICE` (**`Voice - Quent`** explicitly requested, missing from 25-pack!). |
| **11** | `:CH9_MOURNER_UNMASKED` (Ch9) | `Battle - Mourner` (#114) → silence → `Mood - Farewell` (#79) | `Battle - Mourner` → `Mood - Farewell` | `Battle - Mourner` (#114) → `Mood - Farewell` (#79) | BGS: `Glassfall Bleed` | SE: `Field Shatter`, `Beam break`, `Crowd gasp` · Voice: `Voice - Juno`, `Voice - Kestrel`, `Voice - Mourner` *(p112 for unmasked Rowan)* | `OK` for BGM/BGS/Voices. `NEW-SE`: `Mirror Crack` + `Impact Hitstop Boom` + `Glass Shatter Burst` (Shot 3 mask split). |
| **12** | `:CH10_OGERPON_GROVE` (Ch10) | `Town - Verdance` (#9) → `Boss - Pecharunt & Loyal Three` / `Boss - Loyal Three` (#130) | `Town - Elowen` → `Battle - Boss` | `Town - Verdance` (#9) → `Boss - Loyal Three` (#130) | BGS: `Gossamer Deepwood` | SE: `Prism Arena Swell`, `Sound.cry(:OGERPON)` · Voice: `Voice - Juno` | **2 FLAGS:** `P1-FALLBACK` (`Town - Verdance` → `Town - Elowen`); `NAME-FIX` + `P1-FALLBACK` (unify header/Shot 3 to `:bgm_boss_loyal_three` → `Battle - Boss`). |
| **13** | `:CH11_KYOGRE_THAW` (Ch11) | `Mood - Tension` (#78) → `Boss - Kyogre` (#125) | `Mood - Tension` → `Battle - Legendary` | `Mood - Tension` (#78) → `Boss - Kyogre` (#125) | BGS: `Wind - Isenmar` → `Rain` | SE: `Field Shatter`, `Beam charge` (p55), `VS Cutin Lightning`, `Sound.cry(:KYOGRE)` · Voice: `Voice - Anja`, `Voice - Juno` | `P1-FALLBACK`: `Boss - Kyogre` → `Battle - Legendary`. `NEW-SE`: `Mirror Crack` (Shot 1 ice web), `Glass Shatter Burst` (Shot 3 upward ice shatter). |
| **14** | `:CH12_DEAD_LETTERS` (Ch12) | `Dungeon - Sky Tower` (#69) → `Battle - Marchetti` (#117) | `Route - Zenith` → `Battle - Meridian Admin` | `Dungeon - Sky Tower` (#69) → `Battle - Marchetti` (#117) | BGS: `Rain` (vol 45, Shot 3 puddle) | SE: `Beam break`, `VS Cutin Lightning`, `Glass Quench` (p85) · Voice: `Voice - Larch`, `Voice - Odessa`, *(Marchetti)* | **3 FLAGS:** `P1-FALLBACK` (`Dungeon - Sky Tower` → `Route - Zenith`, `Battle - Marchetti` → `Battle - Meridian Admin`); `NEW-SE`: `Glitch Tear Static` + `Mirror Crack` (Shot 3 puddle blink); `MISSING-VOICE`: `Marchetti`. |
| **15** | `:CH13A_MINDSCAPE_290` (Ch13) | `Boss - Mindscape Nightmare` (#124) → `Mood - Farewell` (#79) | `Route - Antumbra` → `Mood - Farewell` | `Boss - Mindscape Nightmare` (#124) → `Mood - Farewell` (#79) | BGS: `Glassfall Bleed` (vol 45) | SE: `Glass Quench`, `Field Shatter`, `VS Cutin Lightning` (`:ILSA`) · Voice: `Voice - Ilsa`, `Voice - Player` | `P1-FALLBACK`: `Boss - Mindscape Nightmare` → `Route - Antumbra`. `NEW-SE`: `Glitch Tear Static` (Shot 1), `Impact Hitstop Boom` (Shot 3 Crown crack). |
| **16** | `:CH13B_GLASS_COURT_FAULT` (Ch13) | `Battle - Tribunal Ambush` / `Pursuit` (#118) → `Mood - Tension` (#78) | `Battle - Meridian Admin` → `Mood - Tension` | `Battle - Tribunal Ambush` (#118) → `Mood - Tension` (#78) | BGS: `Glassfall Bleed` + `Saltmere Harbor` (vol 85, p80 flood) | SE: `Crowd gasp`, `Field Shatter`, `Beam break`, `:rumble`, `VS Cutin Lightning` (`:KAITO`, `:KROLL`) · Voice: `Voice - Kaito`, `Voice - Ilsa`, *(Kroll, Rowan)* | **3 FLAGS:** `P1-FALLBACK` (`Battle - Tribunal Ambush` → `Battle - Meridian Admin`); `NEW-SE`: `Glass Shatter Burst` (Shot 3 stained windows), `Heartbeat Sub-Pulse` (Shot 4); `MISSING-VOICE`: `Kroll`. |
| **17** | `:RD_1` *"The Ring Sings"* (Ch14) | *(Fades to canon silence)* | *(BGM fade out 0.8s)* | *(BGM fade out 0.8s)* | — *(opt. quiet indoor room tone)* | SE: `Glass Quench` (p115), `Prism Arena Swell` (vol 35) · Voice: *(Pip on map resume)* | `OK` live today! `NEW-SE`: **`Ring Glass Harmonic.ogg`** (pure sustained 18-overtone crystal bloom — signature sound of `RD-1`!) + `Heartbeat Sub-Pulse` (Shot 3 sternum pulse). `MISSING-VOICE`: `Pip`. |
| **18** | `:CH15_CATHEDRAL_ECHO` (Ch15) | `Boss - Echo of Morwen` (#131) → `Mood - Farewell` (#79) | `Battle - Warden` → `Mood - Farewell` | `Boss - Echo of Morwen` (#131) → `Mood - Farewell` (#79) | BGS: `Glassfall Bleed` | SE: `Beam break`, `Boss Shield Break`, `Field Shatter`, `Crowd gasp`, `Glass Quench`, `VS Cutin Lightning`, `Sound.cry(:GIRATINA)` · Voice: `Voice - Ysolde`, `Voice - Kestrel`, *(Morwen)* | **2 FLAGS:** `P1-FALLBACK` (`Boss - Echo of Morwen` → `Battle - Warden`); `NEW-SE`: `Glitch Tear Static` (Shot 1), `Impact Hitstop Boom` (Shot 3 bell), `Glass Shatter Burst` (Shot 4); `MISSING-VOICE`: `Morwen`. |
| **19** | `:CH16_ZEKROM_CLEAR_AIR` (Ch16) | `Boss - Zekrom` (#127) → hard cut to dead silence | `Battle - Legendary` → dead silence | `Boss - Zekrom` (#127) → dead silence | BGS: `Machinery - Zenith` → hard stop | SE: `Boss Shield Break`, `VS Cutin Lightning`, `Sound.cry(:ZEKROM)`, **`single stark gunshot SE`** · Voice: `Voice - Magnus`, *(Wenlow)* | **CRITICAL SILENCE BUG:** `P1-FALLBACK` (`Boss - Zekrom` → `Battle - Legendary`); **`NEW-SE` P0:** **`Directorate Rifle Crack.ogg`** does not exist anywhere (Shot 3 Wenlow climax!). `MISSING-VOICE`: `Wenlow`. |
| **20** | `:CH17_CRADLE_SINGS` (Ch17) | `Dungeon - Drowned Aurelia` (#71) → `Theme - Meridian` (#81) | `Dungeon - Ruins` → `Theme - Meridian` | `Dungeon - Drowned Aurelia` (#71) → `Theme - Meridian` (#81) | BGS: `Drip - Nadir` (vol 40) | SE: `Prism Arena Swell`, `Glass Quench`, `VS Cutin Lightning` (`:VOSS`) · Voice: `Voice - Nyx`, `Voice - Sahar`, `Voice - Voss` | `P1-FALLBACK`: `Dungeon - Drowned Aurelia` → `Dungeon - Ruins`. `NEW-SE`: `Ring Glass Harmonic` (Shot 1 18-hue Cradle wake). |
| **21** | `:CH18_HYMN_OF_RETURN` (Ch18) | `Town - Gloaming` (#10) → `Mood - Theme of Hope` (#80) | `Town - Elowen` → `Mood - Emotion` | `Town - Gloaming` (#10) → `Mood - Theme of Hope` (#80) | BGS: `Gossamer Deepwood` (vol 45) | SE: `Field Shatter`, `Glass Quench`, `Prism Arena Swell`, `VS Cutin Lightning` (`:KESTREL`) · Voice: `Voice - Celestine`, `Voice - Kestrel` | **2 FLAGS:** `P1-FALLBACK` (`Town - Gloaming` → `Town - Elowen`, `Mood - Theme of Hope` → `Mood - Emotion`). |
| **22** | `:CH19A_WYRMSCAR_OATH` (Ch19) | `Dungeon - Cinderhorn` (#67) → `Boss - Reshiram` (#128) | `Route - Ashkaar` → `Battle - Legendary` | `Dungeon - Cinderhorn` (#67) → `Boss - Reshiram` (#128) | BGS: `Lava - Ashkaar` | SE: `Beam break`, `VS Cutin Lightning`, `Sound.cry(:RESHIRAM)` · Voice: `Voice - Sigrun`, `Voice - Player` | **2 FLAGS:** `P1-FALLBACK` (`Dungeon - Cinderhorn` → `Route - Ashkaar`, `Boss - Reshiram` → `Battle - Legendary`). `NEW-SE`: `Impact Hitstop Boom` (Shot 2 brazier flare). |
| **23** | `:WAR_CLIMAX` (`WAR-1` v2, Ch19) | `War - Battlefield` → `War - Beam Clash` → `War - Aftermath` | `War - Battlefield` → `War - Beam Clash` → `War - Aftermath` | `War - Battlefield` (#120) → `War - Beam Clash` (#121) → `War - Aftermath` (#85) | BGS: `War - Distant Battle`, `Rain` | SE: `Beam charge`, **`Beam fire`**, `Beam clash`, `Beam break`, `Field Shatter`, `Glass Quench`, `Crowd gasp`, `Sound.cry(:KYOGRE/:RESHIRAM)` · Voice: `Voice - Sigrun`, `Voice - Marisol`, `Voice - Larch`, *(Quent, Eirik, Hrothgar)* | `OK` on all 3 War BGMs & 2 BGSs! `NEW-SE`: **`Beam fire.ogg`** (missing CC0), `Impact Hitstop Boom` (Shot 5 clash), `Glass Shatter Burst` (`:A2`), **`Void Eat Bass Implosion`** (`:R`). `MISSING-VOICE`: `Quent`, `Eirik`, `Hrothgar`. |
| **24** | `:CH20_FESTIVAL_EVE` (Ch20) | `Theme - Accord` (#83) → `Battle - Kestrel K8` (#97) | `Theme - Accord` → `Battle - Kestrel` | `Theme - Accord` (#83) → `Battle - Kestrel K8` (#97) | — | SE: `Prism Arena Swell`, `Crowd cheer`, `Crowd gasp`, `Glass Quench`, `VS Cutin Lightning` · Voice: `Voice - Valen`, `Voice - Voss`, `Voice - Kestrel` | `P1-FALLBACK`: `Battle - Kestrel K8` → `Battle - Kestrel`. `NEW-SE`: `Ring Glass Harmonic` (Shot 2 Eye vision), `Ace Eye-Flash Zing` (Shot 3 dual cut-ins). |
| **25** | `:CH21A_VALEN_ZYGARDE` (Ch21) | **`Battle - Sovereign Valen`** (#136) → `Victory - Sovereign` | **`Battle - Valen`** → `Victory - Sovereign` *(stock)* | `Battle - Valen` (#136) → `Victory - Sovereign` | — | SE: `Prism Arena Swell`, `Beam charge`, **`Beam fire`**, `Field Shatter`, `Boss Shield Break`, `Glass Quench`, `Crowd cheer`, `VS Cutin Lightning` · Voice: `Voice - Valen`, `Voice - Ilsa`, `Voice - Voss` | **2 FLAGS:** `NAME-FIX` (`Battle - Sovereign Valen` → `Battle - Valen` in `manifest.tsv:46`!); `NEW-SE`: **`Beam fire.ogg`**, `Impact Hitstop Boom` (Shot 3 Core Enforcer), `Glass Shatter Burst` (Shot 5 hijack). |
| **26** | `:CH21B_ARCEUS_CONVERGENCE` (Ch21) | `Battle - Voss` (#3) → `Battle - Arceus` (#137/#138) → `Ending - Homecoming` (#86) | `Battle - Voss` → `Battle - Arceus` → `Ending - Homecoming` | `Battle - Voss` (#3) → `Battle - Arceus` (#137) / `Battle - Arceus Final` (#138) → `Ending - Homecoming` (#86) | BGS: `Glassfall Bleed` → fade out | SE: `Prism Arena Swell`, `Boss Shield Break`, `Field Shatter`, `VS Cutin Lightning`, `Glass Quench`, `Sound.cry(:ARCEUS)` · Voice: `Voice - Rook`, `Voice - Magnus`, `Voice - Larch`, `Voice - Voss`, `Voice - Ilsa`, `Voice - Valen`, *(Marchetti)* | `OK` on all 3 BGMs! `NEW-SE`: `Ace Eye-Flash Zing` (Shot 1 allies wipes), `Impact Hitstop Boom` + `Glass Shatter Burst` (Shot 3 chains lock), `Heartbeat Sub-Pulse` (Shot 5 pylons). `MISSING-VOICE`: `Marchetti`. |
| **27** | `:RUIN_R1_LOOK_BACK` (Ruin R1) | `Mood - Mystery` (p100→65) → silence → `Dungeon - Distortion Core` (#72) | `Mood - Mystery` → `Route - Antumbra` *(or `Ending - Ruin`)* | `Mood - Mystery` (#77) → `Dungeon - Distortion Core` (#72) | BGS: `Glassfall Bleed` (p75) | SE: `Field Shatter`, `Glass Quench` (p65), `Sound.cry(:GIRATINA)` · Voice: `Voice - Juno`, *(Dask)* | **3 FLAGS:** `P1-FALLBACK` (`Dungeon - Distortion Core` → `Route - Antumbra`); `NEW-SE`: `Glitch Tear Static` (Shot 2 22-slice VHS), `Mirror Crack` + `Glass Shatter Burst` (Shot 3 inward implode), `Void Eat Bass Implosion`; `MISSING-VOICE`: `Dask`. |
| **28** | `:RUIN_R2_REFLECTION_DUEL` (Ruin R1–R2) | `Battle - Ruin Reflection` (#132) → dead silence | `Battle - Ruin` → dead silence | `Battle - Ruin Reflection` (#132) → dead silence | BGS: `Glassfall Bleed` (p80) | SE: `VS Cutin Lightning` (p82), `Glass Quench` · Voice: `Voice - Player` (p78) | `P1-FALLBACK`: `Battle - Ruin Reflection` → `Battle - Ruin`. `NEW-SE`: `Glitch Tear Static` (Shot 1 reversed speech), `Mirror Crack` + `Ace Eye-Flash Zing` (Shot 2 mirror clash). |
| **29** | `:RUIN_R3_THEODRIC_VOID` (Ruin R3–R5) | `Dungeon - Ruins` (#71*) → mute → `Ruin - Gilded King` (#133) → `Ruin - Archseer Dask` (#134) | `Dungeon - Ruins` → `Battle - Ruin` | `Dungeon - Drowned Aurelia` (#71) → `Ruin - Gilded King` (#133) → `Ruin - Archseer Dask` (#134) | BGS: `Glassfall Bleed` | SE: `Glass Quench`, `Field Shatter`, `Beam break` · Voice: `Voice - Voss` | **3 FLAGS:** `NAME-FIX` (header wrote `#71` on `Dungeon - Ruins`, #71 is `Dungeon - Drowned Aurelia`); `P1-FALLBACK` (`Ruin - Gilded King` & `Ruin - Archseer Dask` → `Battle - Ruin`); `NEW-SE`: `Glitch Tear Static` (Shot 2 eye-snap), `Mirror Crack` (Shot 4 palm), `Void Eat Bass Implosion` (Shot 5). |
| **30** | `:RUIN_R7_DISTORTION_FINALE` (Ruin R7) | `TRUE FINALE - Arceus Legend Plate Phase` (#138) → silence → `Ending - Ruin` (#87) | `Battle - Arceus` → silence → `Ending - Ruin` *(p98 on `:reflection`)* | `Battle - Arceus Final` (#138) → silence → `Ending - Ruin` (#87) | BGS: `Glassfall Bleed` | SE: `Prism Arena Swell`, `Beam clash`, `Field Shatter`, `Boss Shield Break`, `Glass Quench`, `Sound.cry(:ARCEUS/:GIRATINA)` · Voice: `Voice - Valen`, `Voice - Juno`, *(Theodric)* | **3 FLAGS:** `P1-FALLBACK` + `NAME-FIX` (`TRUE FINALE - ...` → `:bgm_ruin_arceus` → `Battle - Arceus`); `NEW-SE`: `Glass Shatter Burst` (Shot 1), `Impact Hitstop Boom` + `Void Eat Bass Implosion` + `Glitch Tear Static` (Shot 3 color-strip), `Mirror Crack` (Shot 6); `MISSING-VOICE`: `Theodric`. |

---

### 1B. Drop-In `Prismfall::Cutscene::AUDIO` Expansion (`001_Config.rb:67-90`)

Because [`Sound.resolve`](file:///home/antigravity/reuben12358/prismfall/plugins/Prismfall%20Cutscenes/002_Util.rb#L283-L286) iterates each array and plays the **first file that exists**, replacing/extending `AUDIO` in [`plugins/Prismfall Cutscenes/001_Config.rb`](file:///home/antigravity/reuben12358/prismfall/plugins/Prismfall%20Cutscenes/001_Config.rb#L67-L90) guarantees **0% silence today** (Phase-1 `manifest.tsv` + 50-pack) AND **zero-code auto-upgrade** when Phase-2 tracks and the 12 new CC0 SFX land:

```ruby
    AUDIO = {
      # --- Existing War / Battle / UI SEs ---
      :beam_charge      => ["Beam charge", "Anim/Charge_Beam", "Anim/Flash2"],
      :beam_fire        => ["Beam fire", "Anim/HyperBeam"],
      :beam_clash       => ["Beam clash", "Anim/HyperBeam", "Anim/Explosion"],
      :beam_break       => ["Beam break", "Anim/Explosion", "Voltorb Flip explosion"],
      :impact           => ["Battle damage normal"],
      :impact_super     => ["Battle damage super"],
      :explosion        => ["Anim/Explosion", "Voltorb Flip explosion"],
      :rumble           => ["Mining collapse", "Anim/Earth1"],
      :crowd_cheer      => ["Crowd cheer", "Anim/Applause"],
      :crowd_gasp       => ["Crowd gasp"],
      :faint            => ["Pkmn faint"],
      :chime            => ["Mining ping", "Pkmn exp full"],
      :card             => ["GUI trainer card open"],

      # --- v4.3 Existing CC0 SE Aliases (50-File Pack) ---
      :field_shatter    => ["Field Shatter", "Anim/Explosion"],
      :boss_shield      => ["Boss Shield Break", "Battle damage super"],
      :glass_quench     => ["Glass Quench", "Mining ping"],
      :prism_swell      => ["Prism Arena Swell", "Anim/Flash2"],
      :vs_lightning     => ["VS Cutin Lightning", "Anim/Thunder1"],

      # --- v4.4 New CC0 Anime Cutscene SE Aliases (Section 4 Shopping List, safe fallbacks!) ---
      :glass_shatter    => ["Glass Shatter Burst", "Field Shatter", "Anim/Explosion"],
      :hitstop_boom     => ["Impact Hitstop Boom", "Boss Shield Break", "Battle damage super"],
      :glitch_tear      => ["Glitch Tear Static", "Glass Quench", "Anim/Static"],
      :chapter_wipe     => ["Chapter Card Prismatic Wipe", "Prism Arena Swell", "Pkmn exp full"],
      :mirror_crack     => ["Mirror Crack", "Glass Quench", "Field Shatter"],
      :eye_flash        => ["Ace Eye-Flash Zing", "VS Cutin Lightning", "Anim/Flash2"],
      :rifle_crack      => ["Directorate Rifle Crack", "Beam break", "Anim/Explosion"],
      :ring_harmonic    => ["Ring Glass Harmonic", "Glass Quench", "Mining ping"],
      :void_implode     => ["Void Eat Bass Implosion", "Beam break", "Mining collapse"],
      :heartbeat        => ["Heartbeat Sub-Pulse", "Battle damage normal"],
      :ferry_horn       => ["Ferry Foghorn", "Prism Arena Swell"],

      # --- All 9 CC0 BGS Loops ---
      :bgs_war          => ["War - Distant Battle"],
      :bgs_rain         => ["Rain"],
      :bgs_bleed        => ["Glassfall Bleed"],
      :bgs_harbor       => ["Saltmere Harbor"],
      :bgs_isenmar      => ["Wind - Isenmar"],
      :bgs_ashkaar      => ["Lava - Ashkaar"],
      :bgs_machinery    => ["Machinery - Zenith"],
      :bgs_drip         => ["Drip - Nadir"],
      :bgs_deepwood     => ["Gossamer Deepwood"],

      # --- All 6 CC0 ME Jingles ---
      :me_hl_start      => ["Festival highlight start", "BP Fanfare"],
      :me_hl_hit        => ["Festival highlight hit", "Slots win"],
      :me_hl_result     => ["Festival highlight result", "Slots big win"],
      :me_game_over     => ["Prismfall game over", "Voltorb Flip game over"],
      :me_badge_get     => ["Warden Badge Get", "Badge get"],
      :me_trial_rank    => ["Trial Rank Up", "Item get"],

      # --- Cutscene BGMs (Phase-2 145-Track First -> Phase-1 manifest.tsv Guaranteed Fallback) ---
      :bgm_last_ferry      => ["Intro - Last Ferry"],
      :bgm_saltmere        => ["Town - Saltmere", "Town - Elowen"],
      :bgm_verdance        => ["Town - Verdance", "Town - Elowen"],
      :bgm_gloaming        => ["Town - Gloaming", "Town - Elowen"],
      :bgm_mirefen         => ["Town - Mirefen", "Town - Nadir"],
      :bgm_bleed_zone      => ["Dungeon - Bleed Zones", "Mood - Mystery", "Route - Antumbra"],
      :bgm_ruins           => ["Dungeon - Ruins"],
      :bgm_sky_tower       => ["Dungeon - Sky Tower", "Route - Zenith", "Dungeon - Deep"],
      :bgm_drowned_aurelia => ["Dungeon - Drowned Aurelia", "Dungeon - Ruins"],
      :bgm_cinderhorn      => ["Dungeon - Cinderhorn", "Route - Ashkaar", "Dungeon - Deep"],
      :bgm_ashkaar_route   => ["Route - Ashkaar"],
      :bgm_ruin_purgatorium=> ["Dungeon - Distortion Core", "Route - Antumbra", "Ending - Ruin"],
      :bgm_mood_mystery    => ["Mood - Mystery"],
      :bgm_mood_tension    => ["Mood - Tension"],
      :bgm_mood_farewell   => ["Mood - Farewell"],
      :bgm_mood_hope       => ["Mood - Theme of Hope", "Mood - Emotion"],
      :bgm_theme_hollow    => ["Theme - Hollow"],
      :bgm_theme_meridian  => ["Theme - Meridian"],
      :bgm_theme_accord    => ["Theme - Accord"],
      :bgm_war_march       => ["War - Frontlines", "War - March"],
      :bgm_war_field       => ["War - Battlefield", "Battle Elite"],
      :bgm_war_clash       => ["War - Beam Clash", "Battle Champion"],
      :bgm_war_after       => ["War - Aftermath"],
      :bgm_mourner         => ["Battle - Mourner"],
      :bgm_marchetti       => ["Battle - Marchetti", "Battle - Meridian Admin"],
      :bgm_tribunal        => ["Battle - Tribunal Ambush", "Battle - Meridian Admin", "Mood - Tension"],
      :bgm_kestrel_k8      => ["Battle - Kestrel K8", "Battle - Kestrel"],
      :bgm_voss            => ["Battle - Voss"],
      :bgm_valen           => ["Battle - Sovereign Valen", "Battle - Valen"],
      :bgm_arceus          => ["Battle - Arceus"],
      :bgm_ruin_arceus     => ["Battle - Arceus Final", "Battle - Arceus", "Battle - Ruin"],
      :bgm_boss_loyal_three=> ["Boss - Loyal Three", "Battle - Boss"],
      :bgm_boss_kyogre     => ["Boss - Kyogre", "Battle - Legendary", "Battle - Boss"],
      :bgm_boss_zekrom     => ["Boss - Zekrom", "Battle - Legendary", "Battle - Boss"],
      :bgm_boss_reshiram   => ["Boss - Reshiram", "Battle - Legendary", "Battle - Boss Final Bar"],
      :bgm_mindscape       => ["Boss - Mindscape Nightmare", "Route - Antumbra", "Mood - Mystery"],
      :bgm_echo_morwen     => ["Boss - Echo of Morwen", "Battle - Warden", "Dungeon - Manor"],
      :bgm_ruin_reflection => ["Battle - Ruin Reflection", "Battle - Ruin"],
      :bgm_ruin_theodric   => ["Ruin - Gilded King", "Battle - Ruin", "Battle - Voss"],
      :bgm_ruin_dask       => ["Ruin - Archseer Dask", "Battle - Ruin"],
      :bgm_highlight       => ["Festival - Highlights", "B2W2 212 PWT Final Round!"],
      :bgm_victory_sov     => ["Victory - Sovereign", "Battle victory leader"],
      :bgm_end_homecoming  => ["Ending - Homecoming"],
      :bgm_end_ruin        => ["Ending - Ruin"]
    }
```

---

## 2. Audio & CC0 Voice Mapping: 8 New Villain Sub-Bosses & 14 New Recurring Side Characters

> [!WARNING]
> **Cross-Proposal ID Collisions Caught Before Wednesday Merge:**
> 1. **`:SLOANE` Collision:** `CLASSES_PROPOSAL.md` #7 defines **Glassrunner Sloane Vargo** (`WILDCARD_SLOANE`, `:SLOANE`), while `SIDE_CAST_PROPOSAL.md` #4 defines **Intern Bret & Intern Sloane Pendergast** (`SIDE_INTERNS`, `:SLOANE`). **Resolution:** Keep `:SLOANE` / `Voice - Sloane.ogg` for **Glassrunner Sloane Vargo**, and assign Intern Sloane to `:INTERN_SLOANE` / `Voice - Intern Sloane.ogg` *(or rename Intern Sloane → e.g. **Intern Priya / Tessa Pendergast** in `SIDE_CAST_PROPOSAL.md` before PBS/Portrait wiring so no player confuses the two Sloanes!)*.
> 2. **Runaway Choir Sibling Pairing (`OCTAVE_SCHERZO` & `SIDE_CELLIST` Ezra):** Both proposals create a runaway ninth Glassfall orphan foil to Vesper. Whether kept as a comedic/dramatic pair or merged during Wednesday's canon pass, both share slot `#150 Battle - Rogue Virtuoso` cleanly below so zero soundtrack work is wasted.

### 2A. Top 6 Brand-New Signature Themes Worth Sourcing (`#146–#151`, 100% Pure Instrumental)

Instead of adding 22 separate tracks, **just 6 brand-new pure-instrumental themes** (zero vocals, zero Toby Fox chiptune) close every remaining genre gap in our 145-track OST — expanding it cleanly to **151 tracks**:

| New OST # | Canonical Filename (`Audio/BGM/`) | Assigned Character(s) | Musical Brief (Pure Instrumental) | Top Candidate Sources to Ear-Audit | Phase-1 Live Fallback (`manifest.tsv`) |
|---:|---|---|---|---|---|
| **#146** | `Battle - Groove Monarch` | **DJ Chroma** (`SIDE_GROOVE`) | High-energy brass/slap-bass acid-jazz funk-disco groove — the ONLY funk battle theme in Prismfall! | *Pokémon Colosseum — Miror B. Retro Groove (GlitchxCity / Mewmore / Zame Remix)* OR *Persona 5 — Blooming Villain / Last Surprise (Instrumental Acid-Jazz)* | `Battle - Festival` |
| **#147** | `Battle - Field Hunter` | **Field Hunter Kal** (`SIDE_HUNTER`) | Razor-sharp 155–165 BPM tactical violin/guitar rival duel (*Rejuv* Novae energy for her 6-chapter arc!) | *Pokémon Rejuvenation — Battle: Novae* (Zumi/CatchDalgo) OR *Octopath Traveler II — Critical Clash I* (Yasunori Nishiki) | `Battle - Cameo` |
| **#148** | `Battle - Icebreaker Captain` | **Captain Orson Falk** (`SIDE_CAPTAIN`, Postgame Lv 100 Superboss) | Thunderous sea-shanty brass, low foghorn swells & storm-fiddle superboss marathon | *Pokémon ORAS — Team Aqua/Magma Leader Archie & Maxie (GlitchxCity / Zame Remix)* OR *Octopath Traveler — Decisive Battle II* | `Battle - Boss Final Bar` |
| **#149** | `Battle - Mirror Peddler` | **Simeon Finch** (`SIDE_PEDDLER`, Normal & Ruin Bridge) | Eerie-whimsical antique music-box waltz snapping into crooked harpsichord & reversed strings | *Pokémon Rejuvenation — Puppet Master Battle* OR *Hollow Knight — The Grimm Troupe (Pure Instrumental)* | `Battle - Ruin` |
| **#150** | `Battle - Rogue Virtuoso` | **Ezra "Coda" Kovacs** (`SIDE_CELLIST`) & **Dissonant Scherzo** (`OCTAVE_SCHERZO`) | Passionate minor-key distorted cello-rock concerto bridging classical Choir strings & punk rebellion | *Hollow Knight — Sisters of Battle* (Christopher Larkin) OR *Trails in the Sky — Fateful Confrontation* (Falcom jdk) | `Battle - Kestrel` |
| **#151** | `Battle - Iron Sentinel` | **Commander Cormac Greer** (`WILDCARD_CORMAC`) & **Choir Censor Malachi** (`OCTAVE_MALACHI`) | Severe, relentless knightly brass & cathedral-organ battle march for Velmora's 4th-axis hardliners | *Fire Emblem: Three Houses — Between Heaven and Earth* (Takeru Kanazaki) OR *Octopath Traveler II — Critical Clash II* | `Battle - Valen` *(or `Battle - Warden`)* |

---

### 2B. Measured Baseline of Existing 25 CC0 `Voice - *.ogg` Blips (DSP Calibration Reference)

Measured directly from the 25 mastered `.ogg` files in `gemini_recommends/2026-11-21_audio-mastering-and-soundscape/Audio/SE/Voice - *.ogg` (`44.1 kHz` stereo Ogg q6, `-18.8 to -20.0 LUFS` on 10-blip bursts, Hann zero-click window):
- **Low Bass / Baritone (`88–205 Hz`, `53–74 ms`):** `Mourner` (88 Hz), `Bastian` (141 Hz), `Brann` (151 Hz), `Valen` (162 Hz), `Ysolde` (181 Hz), `Kaito` (195 Hz), `Voss` (195 Hz), `Magnus` (205 Hz).
- **Mid-Tenor / Rich Alto (`222–292 Hz`, `55–89 ms`):** `Dorian` (222 Hz), `Anja` (232 Hz), `Corvin` (240 Hz), `Marisol` (245 Hz), `Larch` (249 Hz), `Sigrun` (253 Hz), `Nyx` (276 Hz), `Sahar` (276 Hz), `Kestrel` (292 Hz).
- **Bright Alto / Soprano (`390–588 Hz`, `53–91 ms`):** `Player` (390 Hz), `Ilsa` (420 Hz), `Odessa` (459 Hz), `Vesper` (485 Hz), `Rook` (507 Hz), `Juno` (531 Hz), `Celestine` (558 Hz), `Tamsin` (588 Hz).

Every new voice below is placed in an **open frequency + timbre pocket** separated by `>= 35 Hz` or distinct formant color from its primary banter partners!

---

### 2C. All 8 New Villain Sub-Bosses (`CLASSES_PROPOSAL.md`) + `MEDIC_WENLOW` — BGM & Voice Matrix

*(Note: `CLASSES_PROPOSAL.md` PBS stubs currently put stock `Battle Elite` / `Battle Gym Leader` — replace those with the exact Phase-1 manifest BGMs below on Wednesday!)*

| # | Trainer Type & Display | Phase-1 BGM (`manifest.tsv`) | Phase-2 Target BGM (`#1–#151`) | Intro / Victory BGM | CC0 Voice File (`Audio/SE/`) | DSP Spec (`f0` · Formants F1/F2 · Dur · Timbre) | Foil Separation Check |
|---:|---|---|---|---|---|---|---|
| 1 | `HOLLOW_GASPARD` (`Bellringer Gaspard`) | `Battle - Hollow Admin` | `#113 Battle - Hollow Keepers` *(Xen Executive)* | `Theme - Hollow` / `Battle victory leader` | `Voice - Gaspard.ogg` | `262 Hz` · F1 `580` / F2 `1650 Hz` · `74 ms` · Theatrical warm tenor + faint `1310 Hz` brass handbell shimmer (-18 dB) | Clear of Mourner (88 Hz), Thistle (375 Hz), Dorian (222 Hz) |
| 2 | `HOLLOW_CRESSIDA` (`Iconoclast Cressida`) | `Battle - Hollow Admin` | `#113 Battle - Hollow Keepers` *(or `#93 Geara & Zetta` for Ch16 rogue!)* | `Theme - Hollow` / `Battle victory leader` | `Voice - Cressida.ogg` | `365 Hz` · F1 `760` / F2 `2200 Hz` · `50 ms` · Sharp raspy alto + subtle glassy tuning-fork overtone, clipped attack | Clear of Kaito (195 Hz), Sable/Kroll (330 Hz), Teo (265 Hz) |
| 3 | `MERIDIAN_ASHE` (`Spin Doctor Camille`) | `Battle - Meridian Admin` | `#116 Battle - Meridian Directors` *(already names Director Ashe!)* | `Theme - Meridian` / `Battle victory leader` | `Voice - Ashe.ogg` *(alias `:ASHE`)* | `438 Hz` · F1 `690` / F2 `2350 Hz` · `58 ms` · Polished, silky-sharp corporate broadcast alto with slight upward smirk glide (+4%) | Clear of Rook (507 Hz), Marchetti (218 Hz), Dorian (222 Hz) |
| 4 | `MERIDIAN_CASSIAN` (`Asset Hunter Cassian`) | `Battle - Meridian Admin` | `#116 Battle - Meridian Directors` *(Interpol Admin White Wolf)* | `Theme - Meridian` / `Battle victory leader` | `Voice - Cassian.ogg` | `338 Hz` · F1 `620` / F2 `1980 Hz` · `54 ms` · Smug crisp nasal tenor with subtle high-pass telemetry-mic edge | Clear of Quent (315 Hz shaky), Kestrel (292 Hz), Voss (195 Hz) |
| 5 | `OCTAVE_MALACHI` (`Choir Censor Malachi`) | `Battle - Valen` *(or `Battle - Hollow Admin`)* | **`#151 Battle - Iron Sentinel`** *(NEW — liturgical severity!)* | `Theme - Accord` / `Battle victory leader` | `Voice - Malachi.ogg` | `148 Hz` · F1 `410` / F2 `1120 Hz` · `76 ms` · Cold austere cathedral-pipe baritone, zero vibrato, dry hall tail | Clear of Vesper (485 Hz), Celestine (558 Hz), Dorian (222 Hz) |
| 6 | `OCTAVE_SCHERZO` (`Dissonant Scherzo`) | `Battle - Kestrel` *(or `Battle - Cameo`)* | **`#150 Battle - Rogue Virtuoso`** *(NEW — shared Choir rebel!)* | `Theme - Kestrel` / `Battle victory leader` | `Voice - Scherzo.ogg` | `310 Hz` · F1 `700` / F2 `1850 Hz` · `54 ms` · Punchy raspy punk-tenor string-pluck with cheeky pitch bounce | Clear of Vesper (485 Hz), Malachi (148 Hz), Ezra (212 Hz) |
| 7 | `WILDCARD_SLOANE` (`Glassrunner Sloane`) | `Battle - Cameo` | `#92 Battle - Ace Trainer` *(Frontier Brain Tucker — keeps #2 Corbeau Nyx-exclusive!)* | `Theme - Kestrel` / `Battle victory leader` | `Voice - Sloane.ogg` | `288 Hz` · F1 `610` / F2 `1740 Hz` · `60 ms` · Smoky confident low-alto with quick sly upward tail (+3%), warm mid saturation | Clear of Nyx (276 Hz, 88ms breathy), Odessa (459 Hz), Sahar (276 Hz) |
| 8 | `WILDCARD_CORMAC` (`Iron Sentinel Cormac`) | `Battle - Warden` | **`#151 Battle - Iron Sentinel`** *(NEW — 4th-axis Wardguard!)* | `Theme - Accord` / `Battle victory leader` | `Voice - Cormac.ogg` | `136 Hz` · F1 `390` / F2 `1040 Hz` · `64 ms` · Heavy gravel-iron baritone, tight percussive jaw-clip envelope | Clear of Kaito (195 Hz), Marchetti (218 Hz), Valen (162 Hz) |
| + | `MEDIC_WENLOW` (`Ward Intern Wenlow`) | `Battle - Trainer` | `#90 Battle - Trainer (Early/Mid)` | — / `Battle victory trainer` | `Voice - Wenlow.ogg` | `326 Hz` · F1 `650` / F2 `1900 Hz` · `62 ms` · Gentle earnest young tenor, soft warm sine-triangle blend | Clear of Corvin (240 Hz), Mags (382 Hz) |

---

### 2D. All 14 New Recurring Side Characters (`SIDE_CAST_PROPOSAL.md`, 15 Voices) — BGM & Voice Matrix

| # | Trainer Type & Display | Phase-1 BGM (`manifest.tsv`) | Phase-2 Target BGM (`#1–#151`) | CC0 Voice File (`Audio/SE/`) | DSP Spec (`f0` · Formants F1/F2 · Dur · Timbre) | Banter Separation Check |
|---:|---|---|---|---|---|---|
| 1 | `SIDE_GROOVE` (`Groove Monarch Chroma`) | `Battle - Festival` | **`#146 Battle - Groove Monarch`** *(NEW — Funk-Off Groove!)* | `Voice - Chroma.ogg` | `172 Hz` · F1 `490` / F2 `1380 Hz` · `66 ms` · Warm, bouncy low-baritone slap-bass pluck with groovy +5% scoop | Clear of Rook (507 Hz), Dorian (222 Hz), Kestrel (292 Hz) |
| 2 | `SIDE_HUNTER` (`Field Hunter Kal`) | `Battle - Cameo` | **`#147 Battle - Field Hunter`** *(NEW — Tactical Duel!)* | `Voice - Kal.ogg` | `348 Hz` · F1 `710` / F2 `2150 Hz` · `52 ms` · Crisp, dry tactical alto wood-click attack, zero excess tail | Clear of Sahar (276 Hz), Kestrel (292 Hz), Ilsa (420 Hz) |
| 3 | `SIDE_WILDCARD` (`Sump Wildcard Mags`) | `Battle - Hollow` | `#91 Battle - Trainer (Late / Z-A)` *(or `#102 Inconsistent_sea`)* | `Voice - Mags.ogg` | `382 Hz` · F1 `800` / F2 `2100 Hz` · `50 ms` · Raspy, rapid-fire street-alto with gritty formant bite | Clear of Zed (304 Hz), Corvin (240 Hz), Marisol (245 Hz) |
| 4a | `SIDE_INTERNS` (`Intern Bret`) | `Battle - Meridian` | **`#1 Mood - Comedy (Unwelcome School)`** *(Creator-locked!)* | `Voice - Bret.ogg` | `178 Hz` · F1 `440` / F2 `1260 Hz` · `78 ms` · Exhausted baritone with gentle downward sigh-glide (`-7%`) | Hilarious contrast vs Intern Sloane (542 Hz, 48ms)! |
| 4b | `SIDE_INTERNS` (`Intern Sloane`) | *(same duo battle)* | *(same — `#1 Unwelcome School`)* | `Voice - Intern Sloane.ogg` *(fix `:SLOANE` clash!)* | `542 Hz` · F1 `860` / F2 `2550 Hz` · `48 ms` · Hyper-caffeinated rapid-fire staccato soprano with crisp click | Clear of Bret (178 Hz) & Glassrunner Sloane (288 Hz)! |
| 5 | `SIDE_CELLIST` (`Rogue Virtuoso Ezra`) | `Battle - Kestrel` | **`#150 Battle - Rogue Virtuoso`** *(NEW — Cello-Rock Concerto!)* | `Voice - Ezra.ogg` | `212 Hz` · F1 `500` / F2 `1440 Hz` · `72 ms` · Resonant low cello-pizzicato baritone-tenor, warm woody decay | Clear of Vesper (485 Hz), Dorian (222 Hz), Juno (531 Hz) |
| 6 | `SIDE_PHOTOGRAPHER` (`Rift Shutterbug Willa`) | `Battle - Trainer` | `#108 Battle - Odessa` *(Sunshine Coastline)* or `#90` | `Voice - Willa.ogg` | `518 Hz` · F1 `830` / F2 `2480 Hz` · `52 ms` · Bright bouncy staccato soprano + tiny crisp mechanical shutter-tick attack | Clear of Odessa (459 Hz), Larch (249 Hz), Juno (531 Hz, 86ms) |
| 7 | `SIDE_BOTANIST` (`Tea Sommelier Gideon`) | `Battle - Cameo` | `#101 Battle - Dorian` *(Subcon's Royal Waltz — baroque!)* | `Voice - Gideon.ogg` | `318 Hz` · F1 `640` / F2 `2080 Hz` · `60 ms` · Clipped, posh nasal oboe-tenor, crisp theatrical articulation | Clear of Larch (249 Hz, 88ms), Juno (531 Hz) |
| 8 | `SIDE_CARTER` (`Bone Chronicler Zainab`) | `Battle - Warden` | `#142 Battle - Sahar` *(Blue Radiance)* | `Voice - Zainab.ogg` | `258 Hz` · F1 `560` / F2 `1620 Hz` · `68 ms` · Calm, warm dry-alto hollow woodblock-reed timbre | Clear of Sahar (276 Hz), Bastian (141 Hz), Ysolde (181 Hz) |
| 9 | `SIDE_FORGEMASTER` (`Iron Tutor Magda`) | `Battle - Boss` | `#122 Battle - Multi-Bar` *(You Will Know Our Names)* or `#104` | `Voice - Magda.ogg` | `215 Hz` · F1 `530` / F2 `1780 Hz` · `52 ms` · Gruff metallic-alto hammer-tap punch (tiny fiery mentor!) | Hilarious contrast vs booming Brann (151 Hz, 69ms)! |
| 10 | `SIDE_HACKER` (`Lattice Splicer Zed`) | `Battle - Meridian` | `#115 Battle - Meridian Agent` *(or `#102 Inconsistent_sea`)* | `Voice - Zed.ogg` | `304 Hz` · F1 `680` / F2 `2250 Hz` · `50 ms` · Clean filtered modern glitch-chirp (band-limited FM, zero chiptune!) | Clear of Rook (507 Hz), Nyx (276 Hz, 88ms), Mags (382 Hz) |
| 11 | `SIDE_DUELIST` (`Glass-Court Duelist Julian`) | `Battle - Kestrel` | `#92 Battle - Ace Trainer` *(Frontier Brain Tucker)* | `Voice - Julian.ogg` | `280 Hz` · F1 `600` / F2 `1920 Hz` · `58 ms` · Crisp theatrical rapier-tenor with haughty quick-release flourish | Clear of Kestrel (292 Hz), Juno (531 Hz), Dorian (222 Hz) |
| 12 | `SIDE_CRITIC` (`Grand Critic Colette`) | `Battle - Festival` | `#101 Battle - Dorian` *(Subcon's Royal Waltz)* or `#135 Z-A Royale` | `Voice - Colette.ogg` | `398 Hz` · F1 `720` / F2 `2320 Hz` · `56 ms` · Sharp clipped aristocratic alto with crisp castanet-click transient | Clear of Dorian (222 Hz), Tamsin (588 Hz), Kaito (195 Hz) |
| 13 | `SIDE_CAPTAIN` (`Icebreaker Captain Orson`) | `Battle - Boss Final Bar` | **`#148 Battle - Icebreaker Captain`** *(NEW — Sea Superboss!)* | `Voice - Orson.ogg` | `118 Hz` · F1 `350` / F2 `940 Hz` · `76 ms` · Deep gravelly bass foghorn-rumble, warm brass chest resonance | Clear of Marisol (245 Hz), Anja (232 Hz), Bastian (141 Hz) |
| 14 | `SIDE_PEDDLER` (`Mirror Peddler Finch`) | `Battle - Ruin` | **`#149 Battle - Mirror Peddler`** *(NEW — Mirror Waltz!)* | `Voice - Finch.ogg` | `265 Hz` + `640 Hz` glass bell · `72 ms` · Delicate antique silvered-glass chime over soft whispered undertone | Unmistakable eerie timbre — clear of Celestine (558 Hz) & Dask (128 Hz) |

---

### 2E. Bonus Coverage: 11 Unvoiced Cutscene/VS-Bust Cast + 12 Elevated Minor NPCs

So **zero** cutscene lines or Layer 0 VS busts fall silent when `VoiceTicker` lands in [`014_Portraits.rb`](file:///home/antigravity/reuben12358/prismfall/plugins/Prismfall%20Cutscenes/014_Portraits.rb):

| Cast Group | Priority Voices to Synthesize (11 Cutscene-Active) | Interim Pitch Fallback (Existing 25-Pack) | Elevated NPCs (`E1–E12`, `SIDE_CAST_PROPOSAL.md`) |
|---|---|---|---|
| **5 Missing VS Busts** (`Layer 0` + Cutscenes `#6, #10, #14, #16, #26`) | `Quent` (315 Hz jittery), `Marchetti` (218 Hz steely alto), `Kroll` / `Sable` (330 Hz cool sharp alto; alias `:SABLE` → `Voice - Kroll` or separate `342 Hz`), `Thistle` (375 Hz dry brittle alto) | `Quent`→`Corvin` p122; `Marchetti`→`Sigrun` p92; `Kroll`/`Sable`→`Nyx` p108; `Thistle`→`Sahar` p118 | `E1 Pip` (`565 Hz` bright kid), `E2 Coll` (`168 Hz` deadpan bass), `E3 Bersi` (`186 Hz` jolly skald), `E4 Ottoline` (`268 Hz` sly raspy alto), `E5 P-3NNY` (`440 Hz` clean CRT beep-blip!) |
| **6 Speaking Cutscene Cast** (`#1, #5, #17, #18, #19, #27, #30`) | `Calla` (408 Hz tired alto), `Teo` (265 Hz fiery young tenor), `Pip` (565 Hz), `Morwen` (468 Hz hollow airy soprano), `Dask` (128 Hz eerie reversed-envelope bass), `Theodric` (154 Hz regal hollow brass-baritone) | `Calla`→`Player` p104; `Teo`→`Kestrel` p92; `Pip`→`Juno` p106; `Morwen`→`Ysolde` p118; `Dask`→`Mourner` p115; `Theodric`→`Valen` p92 | `E6 Hollin` (chalk-slate click!), `E7 Kosk/Brakka` (reuse `Sigrun`/`Brann` pitch offsets), `E8 8 Octave Choristers` (pitch-scaled `Voice - Vesper` p88–112 across an actual musical scale!), `E9–E12` (reuse archetype blips until Wave 3) |

---

## 3. DJ Chroma's Battle BGM Jukebox Spec (`Prismfall::Jukebox` — *"18.0 FM: Radio Free Prism"*)

### 3A. Design Contract
- **Unlock Trigger:** Granted automatically at **DJ Chroma Affinity `★2`** (or via Event Script `Prismfall::Jukebox.unlock!` after winning Chroma's Ch2/Ch5 *"Funk-Off Double Battle"*).
- **Save-Safe Storage:** Persists inside `Prismfall.state.custom[:jukebox]` ([`002_SaveState.rb:26`](file:///home/antigravity/reuben12358/prismfall/plugins/Prismfall%20Core/002_SaveState.rb#L26)) — zero changes to `SaveState` schema, 100% old-save compatible!
- **Auto-Discovery:** Whenever ANY battle track plays via `pbBGMPlay` (matching `LABELS` or `Battle - ` / `Boss - ` / `War - ` / `Ruin - `), it is silently recorded into `heard` so players naturally build their vinyl crate as they travel Velmora. Winning DJ Chroma rematches can also award exclusive bonus vinyls via `Prismfall::Jukebox.add_track("Battle - Groove Monarch")`.
- **Story & Boss Safety Rules (Reborn/Rejuvenation Standard):**
  1. **NEVER overrides `$PokemonGlobal.nextBattleBGM`** — multi-bar bosses ([`006_Bosses_Start.rb:23`](file:///home/antigravity/reuben12358/prismfall/plugins/Prismfall%20Bosses/006_Bosses_Start.rb#L23)), Festival Finals ([`009_Festival.rb`](file:///home/antigravity/reuben12358/prismfall/plugins/Prismfall%20Core/009_Festival.rb)), and scripted story fights always keep their canon music!
  2. **3 Independent Channels:**
     - `:wild` — replaces wild battle music (`pbGetWildBattleBGM`) with any heard track, `:random` (Shuffle Heard), or `nil` (Area Default).
     - `:rematch` — replaces music for **repeatable side-cast rematches (`trainer.version >= 70`)**, **Festival Exhibitions / Pavilion / Concordance Spire / Test Arena** (`PAVILION_MAPS`, still guarding first-time story finales on Map `491`), so grinding & rematches stay endlessly fresh!
     - `:trainer` — opt-in override for regular route trainers (still protects `PROTECTED_PREFIXES`: Wardens, Rivals, Sovereign, Evil-Org bosses, Legendaries!).
  3. **Zero-Silence Guarantee:** Always validates `FileTest.audio_exist?("Audio/BGM/#{name}")` before returning an override; falls back seamlessly if a Phase-2 track isn't installed.

### 3B. Drop-In Lightweight Ruby Hook (`plugins/Prismfall Core/027_Jukebox.rb`)

```ruby
#===============================================================================
# Prismfall Core - 027 DJ Chroma's Battle BGM Jukebox ("18.0 FM: Radio Free Prism")
#-------------------------------------------------------------------------------
# Event usage:
#   Prismfall::Jukebox.unlock!                       # DJ Chroma Affinity 2★ gift
#   Prismfall::Jukebox.add_track("Battle - Groove Monarch")
#   Prismfall::Jukebox.show                          # Open Jukebox UI directly
#===============================================================================
module Prismfall
  module Jukebox
    ENABLED = true
    # Pavilion / Concordance Spire / Test Arena maps where rematch channel applies
    PAVILION_MAPS = [491, 493, 499, 990]
    # First-time story bosses & Wardens never get overwritten by standard trainer mode
    PROTECTED_PREFIXES = %w[LEADER_ RIVAL_ CHAMPION_ HOLLOW_ MERIDIAN_ GILDED_ ECHO_ ARCHSEER_ REFLECTION]
    # Display labels for cataloged battle tracks (Phase-1 & Phase-2 unified)
    LABELS = {
      "Battle - Wild"               => "Wild Encounter (Standard)",
      "Battle - Trainer"            => "Velmora Trainer",
      "Battle - Kestrel"            => "Rival Kestrel",
      "Battle - Kestrel K8"         => "Kestrel Semifinal (K8)",
      "Battle - Juno"               => "Rival Juno",
      "Battle - Warden"             => "Warden Challenge",
      "Battle - Warden Nyx"         => "Shadow Broker Nyx",
      "Battle - Hollow"             => "The Hollow Bereaved",
      "Battle - Hollow Admin"       => "Hollow Keepers",
      "Battle - Mourner"            => "The Mourner",
      "Battle - Meridian"           => "Meridian Concord",
      "Battle - Meridian Admin"     => "Meridian Directors",
      "Battle - Marchetti"          => "Iron Marshal Marchetti",
      "Battle - Voss"               => "Aurelian Voss",
      "Battle - Legendary"          => "Titan Awakening",
      "Battle - Boss"               => "Dimensional Threat",
      "Battle - Boss Final Bar"     => "Final Shield Break",
      "Battle - Festival"           => "Festival Bracket",
      "Battle - Festival Final"     => "Festival Finals",
      "Battle - Valen"              => "Sovereign Valen",
      "Battle - Arceus"             => "Arceus Convergence",
      "Battle - Ruin"               => "Dark Mirror (Ruin)",
      "Battle - Cameo"              => "Concordance Cameo",
      "War - Battlefield"           => "Glass Dunes Frontline",
      "War - Beam Clash"            => "Clash of Titans",
      "Battle - Groove Monarch"     => "18.0 FM — DJ Chroma",
      "Battle - Field Hunter"       => "Field Hunter Kal",
      "Battle - Icebreaker Captain" => "Admiral Orson Falk",
      "Battle - Mirror Peddler"     => "Mirror Peddler Finch",
      "Battle - Rogue Virtuoso"     => "Rogue Virtuoso (Cello)",
      "Battle - Iron Sentinel"      => "Iron Sentinel / Censor"
    }

    def self.data
      c = Prismfall.state.custom
      c[:jukebox] ||= { :unlocked => false, :heard => [], :wild => nil, :rematch => nil, :trainer => nil }
      return c[:jukebox]
    end

    def self.unlocked?; return ENABLED && data[:unlocked] == true; end
    def self.unlock!;   data[:unlocked] = true; end

    def self.audio_ok?(name)
      return false if name.nil? || name.to_s.empty?
      return true if !FileTest.respond_to?(:audio_exist?)
      return FileTest.audio_exist?("Audio/BGM/#{name}")
    rescue StandardError
      return false
    end

    def self.battle_track?(name)
      s = name.to_s
      return true if LABELS.key?(s)
      return !!(s =~ /\A(?:Battle - |Boss - |War - (?:Battlefield|Beam Clash)|Ruin - )/i)
    end

    def self.record_heard(bgm)
      return if !ENABLED
      name = bgm.respond_to?(:name) ? bgm.name.to_s : bgm.to_s
      return if name.empty? || !battle_track?(name)
      h = data[:heard]
      h.push(name) if !h.include?(name)
    end

    def self.add_track(name)
      record_heard(name) if audio_ok?(name)
    end

    def self.available_tracks
      return data[:heard].select { |n| audio_ok?(n) }
    end

    def self.pick_for(channel)
      return nil if !unlocked?
      sel = data[channel]
      return nil if sel.nil?
      if sel == :random
        pool = available_tracks
        return pool.empty? ? nil : pool.sample
      end
      return audio_ok?(sel) ? sel : nil
    end

    def self.rematch_or_pavilion?(trainers)
      list = Array(trainers).compact
      return true if list.any? { |t| t.respond_to?(:version) && t.version.to_i >= 70 }
      return false if protected_trainer?(list)
      map_id = ($game_map.map_id rescue 0)
      return PAVILION_MAPS.include?(map_id)
    end

    def self.protected_trainer?(trainers)
      list = Array(trainers).compact
      return list.any? do |t|
        tt = (t.respond_to?(:trainer_type) ? t.trainer_type.to_s : "")
        ver = (t.respond_to?(:version) ? t.version.to_i : 0)
        ver < 70 && PROTECTED_PREFIXES.any? { |p| tt.start_with?(p) }
      end
    end

    def self.show
      pbFadeOutIn do
        PrismfallJukeboxScene.new.main
      end
    end
  end
end

# --- Essentials v21.1 Battle BGM & Discovery Hooks (Alias-Chained, Boss-Safe) ---
if defined?(pbBGMPlay) && !defined?(prismfall_jukebox_pbBGMPlay)
  alias prismfall_jukebox_pbBGMPlay pbBGMPlay
  def pbBGMPlay(param, volume = nil, pitch = nil)
    Prismfall::Jukebox.record_heard(param) rescue nil
    return prismfall_jukebox_pbBGMPlay(param, volume, pitch)
  end
end

if defined?(pbGetWildBattleBGM) && !defined?(prismfall_jukebox_pbGetWildBattleBGM)
  alias prismfall_jukebox_pbGetWildBattleBGM pbGetWildBattleBGM
  def pbGetWildBattleBGM(wildParty)
    if !$PokemonGlobal&.nextBattleBGM
      pick = Prismfall::Jukebox.pick_for(:wild)
      return RPG::AudioFile.new(pick) if pick
    end
    ret = prismfall_jukebox_pbGetWildBattleBGM(wildParty)
    Prismfall::Jukebox.record_heard(ret) rescue nil
    return ret
  end
end

if defined?(pbGetTrainerBattleBGM) && !defined?(prismfall_jukebox_pbGetTrainerBattleBGM)
  alias prismfall_jukebox_pbGetTrainerBattleBGM pbGetTrainerBattleBGM
  def pbGetTrainerBattleBGM(trainer)
    if !$PokemonGlobal&.nextBattleBGM && Prismfall::Jukebox.unlocked?
      pick = nil
      if Prismfall::Jukebox.rematch_or_pavilion?(trainer)
        pick = Prismfall::Jukebox.pick_for(:rematch)
      elsif !Prismfall::Jukebox.protected_trainer?(trainer)
        pick = Prismfall::Jukebox.pick_for(:trainer)
      end
      return RPG::AudioFile.new(pick) if pick
    end
    ret = prismfall_jukebox_pbGetTrainerBattleBGM(trainer)
    Prismfall::Jukebox.record_heard(ret) rescue nil
    return ret
  end
end

# --- Code-Drawn "18.0 FM" Jukebox Scene (Zero Art Needed; Mirrors LedgerScene) ---
class PrismfallJukeboxScene
  CHANNELS = [[:wild, "Wild Battles"], [:rematch, "Rematches & Spire"], [:trainer, "Route Trainers"]]
  ROWS     = 7
  ROW_H    = 30
  LIST_TOP = 64
  BG       = Color.new(22, 12, 28)
  PANEL    = Color.new(44, 24, 52)
  SELECT   = Color.new(184, 34, 114)  # DJ Chroma Electric Magenta
  GOLD     = Color.new(255, 209, 92)  # Prism Gold
  TEXT     = Color.new(250, 243, 224) # Warm Ivory
  DIM      = Color.new(144, 126, 152)
  SHADOW   = Color.new(0, 0, 0)

  def initialize
    @tab = 0
    @idx = [0, 0, 0]
    @top = [0, 0, 0]
    @previewing = nil
  end

  def rows_list
    return [nil, :random] + Prismfall::Jukebox.available_tracks
  end

  def label_for(val)
    return _INTL("[ Area / Default Theme ]") if val.nil?
    return _INTL("[ Shuffle All Heard Vinyls ]") if val == :random
    return Prismfall::Jukebox::LABELS[val] || val
  end

  def refresh
    bmp = @overlay.bitmap
    bmp.clear
    w = Graphics.width
    ch_key, _ = CHANNELS[@tab]
    active = Prismfall::Jukebox.data[ch_key]
    list = rows_list
    pbSetSystemFont(bmp)
    pbDrawTextPositions(bmp, [[_INTL("18.0 FM — CHROMA'S JUKEBOX"), w / 2, 4, :center, GOLD, SHADOW]])
    pbSetSmallFont(bmp)
    tab_w = (w - 32 - 16) / 3
    CHANNELS.each_with_index do |(_, title), i|
      x = 16 + (i * (tab_w + 8))
      bmp.fill_rect(x, 34, tab_w, 24, (i == @tab) ? SELECT : PANEL)
      pbDrawTextPositions(bmp, [[title, x + (tab_w / 2), 36, :center, (i == @tab) ? TEXT : DIM, SHADOW]])
    end
    bmp.fill_rect(16, LIST_TOP, w - 32, ROWS * ROW_H, PANEL)
    texts = []
    top = @top[@tab]
    list[top, ROWS].to_a.each_with_index do |val, i|
      idx = top + i
      y = LIST_TOP + (i * ROW_H)
      bmp.fill_rect(16, y, w - 32, ROW_H, SELECT) if idx == @idx[@tab]
      mark = (val == active) ? "★" : (val == @previewing ? "♪" : " ")
      texts.push([mark, 26, y + 6, :left, GOLD, SHADOW])
      texts.push([label_for(val), 48, y + 6, :left, (idx == @idx[@tab] || val == active) ? TEXT : DIM, SHADOW])
    end
    pbDrawTextPositions(bmp, texts)
    pbDrawTextPositions(bmp, [
      [_INTL("USE: Set   ACTION: Preview   LEFT/RIGHT: Channel"), w / 2, Graphics.height - 52, :center, DIM, SHADOW],
      [_INTL("Vinyls Heard: {1}", Prismfall::Jukebox.available_tracks.length), 20, Graphics.height - 26, :left, TEXT, SHADOW],
      [_INTL("Active: {1}", label_for(active)), w - 20, Graphics.height - 26, :right, GOLD, SHADOW]
    ])
  end

  def main
    $game_system.bgm_memorize if $game_system
    @viewport = Viewport.new(0, 0, Graphics.width, Graphics.height)
    @viewport.z = 99999
    @bg = ColoredPlane.new(BG, @viewport)
    @overlay = BitmapSprite.new(Graphics.width, Graphics.height, @viewport)
    refresh
    loop do
      Graphics.update
      Input.update
      list = rows_list
      if Input.trigger?(Input::BACK)
        pbPlayCloseMenuSE
        break
      elsif Input.trigger?(Input::LEFT) || Input.trigger?(Input::RIGHT)
        @tab = (@tab + (Input.trigger?(Input::LEFT) ? 2 : 1)) % 3
        @idx[@tab] = [@idx[@tab], list.length - 1].min
        pbPlayCursorSE
        refresh
      elsif (Input.repeat?(Input::UP) || Input.repeat?(Input::DOWN)) && !list.empty?
        @idx[@tab] = (@idx[@tab] + (Input.repeat?(Input::UP) ? -1 : 1)) % list.length
        @top[@tab] = @idx[@tab] if @idx[@tab] < @top[@tab]
        @top[@tab] = @idx[@tab] - ROWS + 1 if @idx[@tab] >= @top[@tab] + ROWS
        pbPlayCursorSE
        refresh
      elsif Input.trigger?(Input::USE) && !list.empty?
        ch_key = CHANNELS[@tab][0]
        Prismfall::Jukebox.data[ch_key] = list[@idx[@tab]]
        pbPlayDecisionSE
        refresh
      elsif Input.trigger?(Input::ACTION) && !list.empty?
        val = list[@idx[@tab]]
        if val.is_a?(String)
          @previewing = val
          pbBGMPlay(val)
          refresh
        end
      end
    end
    $game_system.bgm_restore if $game_system && @previewing
    @overlay.dispose
    @bg.dispose
    @viewport.dispose
  end
end

MenuHandlers.add(:pause_menu, :prismfall_jukebox, {
  "name"      => _INTL("18.0 FM Jukebox"),
  "order"     => 46,
  "condition" => proc { next Prismfall::Jukebox.unlocked? },
  "effect"    => proc { |menu|
    pbPlayDecisionSE
    Prismfall::Jukebox.show
    menu.pbRefresh
    next false
  }
})
```

---

## 4. Missing CC0 Cutscene SFX Shopping List (12 Pure-DSP Anime SEs — Zero Image Quota Needed!)

All 12 sound effects below are designed for **immediate pure-Python/DSP synthesis + ear-audit + EBU R128 mastering via `master_track.py`** (`44.1 kHz` stereo Ogg Vorbis `-q:a 6`, `-13.5 LUFS` integrated / `-1.5 dBTP` true peak, zero-click Hann fades). Synthesizing these 12 files turns all 30 cutscenes + Layer 0 Anime Juice from functional into studio-grade Rejuvenation V14 cinema:

| # | Exact Filename (`Audio/SE/*.ogg`) | `001_Config.rb` Key | Dur | Priority | Cutscenes Served | Pure-DSP Synthesis Recipe (CC0) |
|---:|---|---|---:|---|---|---|
| **1** | `Directorate Rifle Crack.ogg` | `:rifle_crack` | `0.65s` | **P0** *(Fixes silent climax!)* | `#19 :CH16_ZEKROM_CLEAR_AIR` (Shot 3 — Wenlow's Quiet Ward sacrifice) | `3 ms` hard supersonic impulse + `45 ms` band-passed white-noise crack (`1.8–6.5 kHz`) + `120 Hz` body thump + cold tiled-hall convolution decay (`520 ms` stereo early reflections) fading into dead zero. |
| **2** | `Beam fire.ogg` | `:beam_fire` | `1.45s` | **P0** *(Fixes missing Config file!)* | `#10` Caldera, `#23` WAR-1 (Origin Pulse + Blue Flare launch), `#25` Zygarde Core Enforcer | Explosive plasma-ignition transient (`90→42 Hz` pitch drop + `1.2–4 kHz` resonant roar) blending into a wide stereo detuned-sawtooth harmonic jet with subtle `18 Hz` flutter; bridges `Beam charge` → `Beam clash`. |
| **3** | `Impact Hitstop Boom.ogg` | `:hitstop_boom` | `0.85s` | **P0** *(11+ Cutscenes)* | `#3, #5, #6, #11, #15, #18, #22, #23, #25, #26, #30` (`hitstop` / `impact_cg` / `sakuga_flash`) | `65 ms` reverse-suck air-vacuum swell → `8 ms` absolute silence → massive sakuga anime bass-drop (`95→34 Hz` exponential sine punch + saturated mid-crack `900 Hz` + tight `480 ms` dark sub-tail). |
| **4** | `Glass Shatter Burst.ogg` | `:glass_shatter` | `1.35s` | **P0** *(9 Cutscenes)* | `#6, #11, #13, #16, #18, #23 (:A2), #25, #26, #27, #30` (`shatter_screen` Voronoi bursts) | Crisp `12 ms` glass-pane snap + 24 stochastically-panned high-Q metallic/glass modal pings (`2.2–9.8 kHz`, inharmonic ratios) cascading over `1.1s` like falling Voronoi shards on stone. |
| **5** | `Glitch Tear Static.ogg` | `:glitch_tear` | `0.75s` | **P0** *(11 Cutscenes + Ruin Cards)* | `#1, #4, #9, #14, #15, #18, #19, #27, #28, #29, #30` + Ruin `chapter_card` | Modern dark VHS/chromatic tear (NOT chiptune!): sample-and-hold stutter chunks (`14–28 ms`) of filtered pink noise + bitter ring-modulated `210 Hz × 1.73 kHz` buzz + hard stereo L/R phase flip snaps. |
| **6** | `Ace Eye-Flash Zing.ogg` | `:eye_flash` | `0.70s` | **P1** *(Layer 0 60-hr Game!)* | Layer 0 `cutin_flash mode: :eye_strip` (all Ace send-outs, Megas, Z-Moves, `#24`, `#26`, `#28`) | Tight Persona/anime eye-gleam: `80 ms` upward metallic blade-sweep (`1.4→5.2 kHz`) locking onto a bright fifth-interval shimmer (`A5 + E6`) backed by a crisp `110 Hz` snap. Faster & sharper than `VS Cutin Lightning`. |
| **7** | `Chapter Card Prismatic Wipe.ogg` | `:chapter_wipe` | `2.40s` | **P1** *(All 22 Main Chapters!)* | Layer 0 `chapter_card` (Ch0–Ch21) + Act `title_slam` (`#1, #3, #7, #16, #25, #26`) | Lush stereo L→R crystalline harp arpeggio ascending an 18-note Lydian prism scale (`0.0–0.85s`) locking onto a warm brass/celesta major-9 chord swell (`0.85–2.40s`) with concert-hall tail. |
| **8** | `Mirror Crack.ogg` | `:mirror_crack` | `0.65s` | **P1** *(7 Cutscenes)* | `#11` Mask crack, `#13` Lake ice web, `#14` Puddle, `#27, #28, #29` Palm on glass, `#30` Hesper's mirror | Intimate, bone-chilling single razor-sharp obsidian fracture (`3.4 kHz` + `5.8 kHz` impulse) followed by 5 micro-creak branching ticks (`180–580 ms`) — zero boom, pure tension! |
| **9** | `Ring Glass Harmonic.ogg` | `:ring_harmonic` | `3.40s` | **P1** *(Canon `RD-1` Signature!)* | `#17 :RD_1` (*The Ring Sings*), `#4` Wounded Crown, `#20` Cradle Sings, `#24` Arceus Eye | Pure bowed glass-harp crystal bloom: slow `0.6s` attack into beating stereo crystal harmonics (`C5, G5, B5, D6, F#6` with subtle `0.8 Hz` beating shimmer), pure ethereal decay — zero drums, zero vocals. |
| **10** | `Void Eat Bass Implosion.ogg` | `:void_implode` | `1.90s` | **P1** *(Ruin Route Signature!)* | `#23 WAR-1 :R`, `#27 R1`, `#29 R5 Void Dunes`, `#30 R7 Color-Strip & Unmaking` | Inverted-envelope vacuum implosion: `1.1s` rising reverse-noise & downward-sweeping sub (`120→28 Hz`) sucked abruptly into a `40 ms` dead-black silence pocket, followed by a hollow sub-38 Hz gravity thud. |
| **11** | `Heartbeat Sub-Pulse.ogg` | `:heartbeat` | `0.95s` | **P2** *(5 Cutscenes)* | `#3` Mourner eye-lock, `#6` Dark Stone core, `#16` Undercroft dilemma, `#17` Sternum star, `#26` Valen pylons | Organic muffled double-thump (`48 Hz` *lub* at `0.0s`, `42 Hz` *DUB* at `0.24s`, low-passed at `160 Hz` with subtle chest-cavity resonance). Loop-safe for tense choice prompts. |
| **12** | `Ferry Foghorn.ogg` | `:ferry_horn` | `2.80s` | **P2** *(Game Opening + Orson!)* | `#1 :PRO_DOVETAIL_ARRIVAL` (Shot 1 — first SFX of the game!) + **Captain Orson Falk** intro cue | Warm maritime brass foghorn (`Bb1 = 58.3 Hz` fundamental + rich `F2`/`Bb2`/`D3` brass formants, slight breathy pitch settle `-1.5%` on release, wide foggy sea-reverb tail). |

---

## 5. Immediate Pure-DSP Execution Order (Zero Image Quota Required)

1. **Sync Existing 50-File CC0 Pack** (`gemini_recommends/2026-11-21_audio-mastering-and-soundscape/Audio/{BGS,ME,SE}/*.ogg` → `audio/gemini_cc0/` and update [`audio/manifest.tsv`](file:///home/antigravity/reuben12358/prismfall/audio/manifest.tsv) per `WIRING_SPEC.md` §4B) — activates all 9 organic BGS loops, 6 ME jingles, 10 SEs, and 25 core cast voices immediately.
2. **Synthesize & Ear-Audit Batch A — The 12 Anime Cutscene SFX (`Section 4`):** `50 → 62` CC0 files (eliminates the Ch16 Wenlow gunshot silence bug, missing `Beam fire`, missing `Ferry Foghorn`, and upgrades every `shatter_screen`/`hitstop`/`glitch_tear`/`chapter_card`/`RD-1` moment).
3. **Synthesize & Ear-Audit Batch B — The 34 New Voice Blips (`23` Villain/Side-Cast from §§2C–2D + `11` Unvoiced Cutscene/VS-Bust Cast from §2E):** `62 → 96` CC0 files, all `-19.5 LUFS`, `44.1 kHz` stereo Ogg q6, zero frequency clashes.
4. **Claude Wednesday Engine Sprint Wiring:**
   - Drop Section 1B `AUDIO` fallback table into [`plugins/Prismfall Cutscenes/001_Config.rb`](file:///home/antigravity/reuben12358/prismfall/plugins/Prismfall%20Cutscenes/001_Config.rb#L67-L90).
   - Wire `VoiceTicker` into [`014_Portraits.rb`](file:///home/antigravity/reuben12358/prismfall/plugins/Prismfall%20Cutscenes/014_Portraits.rb) (including `:INTERN_SLOANE` disambiguation).
   - Add `plugins/Prismfall Core/027_Jukebox.rb` (Section 3B) for DJ Chroma's `"18.0 FM"` Jukebox.
   - Use Phase-1 `manifest.tsv` BGMs in `pbs/trainer_types.txt` for all 8 villain sub-bosses + 14 side characters, upgrading seamlessly as the 6 new Phase-2 signature tracks (`#146–#151`) are sourced & mastered via `master_track.py`.
