# Complete 117-Map, 67-Trainer & 50-File CC0 Audio Wiring Blueprint (v4.3)

- **Date:** 2026-11-22
- **Author:** Gemini (Audio & Wiring Verification)
- **Scope:** All **117** built maps (`maps_out/Data/Map100.rxdata`–`Map990.rxdata`), `audio/manifest.tsv`, `audio/install_audio.py`, `audio/gemini_cc0/`, `pbs/trainer_types.txt`, and `plugins/Prismfall */*.rb`.

---

## 1. Current Staging & Wiring Gaps (Verified)
1. **0 / 69** `audio/manifest.tsv` BGMs and **0 / 9** `Audio/BGS/` loops are wired into the 117 built maps (`93` use stock Essentials placeholders, `2` point to nonexistent BGMs `Briarwick`/`Ebbmouth` and play silence, `8` have empty `bgm: ""`, `14` Poké Centers/Marts intentionally keep stock).
2. **`audio/gemini_cc0/` is stale:** `18 / 19` files are pre-v4.3 builds (old synth BGS + `192 kHz` SEs), and `31 / 50` v4.3 files (all **6 ME jingles** + all **25 Cast `Voice - *.ogg` blips**) are missing from `audio/gemini_cc0/` and `audio/manifest.tsv` (`manifest.tsv:67-69,71` still say `(stock base project)` so `install_audio.py:15` skips them).
3. **`design/AUDIO_SOUNDTRACK_PLAN.md`** is stale at v4 (`139` tracks, `26` CC0) vs `PROPOSAL.md` v4.3 (`145` tracks, `50` CC0).
4. **0 / 67** NPC trainer types in `pbs/trainer_types.txt` use Prismfall manifest BGMs (`AUDIO.md:210-224` also predates 11 newer types: `ARCHSEER_DASK`, `ASHKAAR_*`, `ISENMAR_*`, `OCTAVE_*`).
5. **Plugin Audio Hooks Missing:** `Warden Badge Get`, `Trial Rank Up`, `Prismfall game over`, `VS Cutin Lightning`, `Boss Shield Break`, `Glass Quench`, `Field Shatter`, `Prism Arena Swell`, all `25` Cast `Voice - *.ogg` blips (`014_Portraits.rb`), `0/10` Boss `:music`, Festival `:bgm`, Endings `:bgm`, and `$data_system.title_bgm`.

---

## 2. `mapgen/rpg.py` + `mapgen/build.py` BGS & `design/MAP_AUDIO.yaml` SSOT Diff

> **RMXP/Essentials Indoor BGS Rule:** `autoplay_bgs = false` does **not** stop the previous map's BGS — outdoor loops will bleed indoors unless indoor maps set `autoplay_bgs = true` with `bgs = ""`. Also, never hardcode `bgs: Rain` on probabilistic `Rain,10/20/30` maps (`140, 146, 147, 160, 167, 561`); trigger `Rain.ogg` dynamically when weather rolls rain.

**`mapgen/rpg.py:61-65`:**
```python
def rmap(tileset_id, width, height, data, events, bgm='', bgs='', autoplay_bgm=None, encounter_step=30,
         bgm_volume=100, bgs_volume=80, autoplay_bgs=True):
    return O('RPG::Map', bgm=audio(bgm, bgm_volume), tileset_id=tileset_id, events=events,
             bgs=audio(bgs, bgs_volume),
             autoplay_bgm=bool(bgm) if autoplay_bgm is None else autoplay_bgm, data=data,
             autoplay_bgs=autoplay_bgs,
             height=height, encounter_step=encounter_step, width=width, encounter_list=[])
```

**`mapgen/build.py:367-368`** (loads optional `design/MAP_AUDIO.yaml` SSOT mirroring `FIELD_DEFAULTS.yaml` at `L724`, so re-running `gen_*.py` / `layouts/*.py` never reverts maps back to stock placeholders):
```python
    au = map_audio_for(mid) if hasattr(ctx, 'audio_map') else {}
    bgm = au.get('bgm', spec.get('bgm', ''))
    bgs = au.get('bgs', spec.get('bgs', ''))
    bgs_vol = int(au.get('bgs_volume', spec.get('bgs_volume', 80)))
    auto_bgs = au.get('autoplay_bgs', spec.get('autoplay_bgs', True))
    m = G.rmap(spec['_tileset'], W, H, G.table3(layers), events, bgm=bgm, bgs=bgs,
               bgs_volume=bgs_vol, autoplay_bgs=auto_bgs, encounter_step=spec.get('encounter_step', 30))
```

**Dynamic `Rain.ogg` hook in `mapgen/build.py:761-772` (`005_MapAtmosphere.rb`, called in `:on_enter_map`):**
```ruby
  def self.apply_weather_bgs
    return if !$game_map || !$game_screen || !FileTest.respond_to?(:audio_exist?)
    return if !FileTest.audio_exist?("Audio/BGS/Rain")
    wt = ($game_screen.weather_type rescue :None)
    pbBGSPlay("Rain", 65) if [:Rain, :Storm, :HeavyRain].include?(wt)
  end
```

---

## 3. Complete 117-Map BGM & CC0 BGS Matrix (`100`–`990`)
*(`—` = `bgs: ""` with `autoplay_bgs: true` to cleanly silence outdoor ambience indoors. All `Target Manifest BGM` names exist in `audio/manifest.tsv` today.)*

| ID | Map | Target Manifest BGM | Target CC0 BGS (vol) | Notes |
|---:|---|---|---|---|
| 100 | Ferrow's Landing | `Town - Ferrows Landing` | `Saltmere Harbor` (60) | Coastal fog |
| 101–102 | Ferrow PC / Mart | `Poke Center` / `Poke Mart` | — | Keep stock |
| 103 | Larch Research Station | `Intro - Larch Lab` | — | `AUDIO.md:253` |
| 104–105, 107–108 | Ferrow Interiors | `Town - Ferrows Landing` | — | Indoor |
| 106 | Ferrow Lighthouse Lamp Room | `Town - Ferrows Landing` | `Saltmere Harbor` (50) | High coastal tower |
| 109 / 110 | The Dovetail Deck / Cabin | `Intro - Last Ferry` | `Saltmere Harbor` (70 / 35) | Ferry hull ambience |
| 120 | Briarwick | `Town - Elowen` | `Gossamer Deepwood` (55) | v4.3 `#7 Town - Briarwick` |
| 121–122 | Briarwick PC / Mart | `Poke Center` / `Poke Mart` | — | Keep stock |
| 123–126 | Briarwick Interiors (incl. `126` broken `Briarwick`) | `Town - Elowen` | — | Fixes `126` silent BGM |
| 130 | Loomhouse Gym Lobby | `Gym - Warden Hall` | — | Gym 2 foyer |
| 131–132, 134 | Loomhouse Canopy / Lofts | `Gym - Warden Hall` | `Gossamer Deepwood` (45) | Open timber canopy |
| 140, 146, 147 | Saltmere / Harbour / Old Town | `Town - Elowen` | `Saltmere Harbor` (70 / 80 / 55) | Dynamic `Rain.ogg`; v4.3 `#6` |
| 141–142 | Saltmere PC / Mart | `Poke Center` / `Poke Mart` | — | Keep stock |
| 143–145, 148 | Saltmere Interiors & Pageant Hall | `Town - Elowen` | — | Indoor |
| 150–154 | Pell Playhouse (Gym 1) | `Gym - Warden Hall` | — | Gym 1 |
| 160 | Ebbmouth | `Town - Isenmar` | `Wind - Isenmar` (60) | Dynamic `Rain.ogg`; v4.3 `#17` |
| 161–162 | Ebbmouth PC / Mart | `Poke Center` / `Poke Mart` | — | Keep stock |
| 163–165, 168 | Ebbmouth Interiors (incl. `168` broken `Ebbmouth`) | `Town - Isenmar` | — | Fixes `168` silent BGM |
| 167 | Ebbmouth - Mill Quay | `Town - Isenmar` | `Saltmere Harbor` (65) | Wooden quay (`Rain,30`) |
| 170 | Tidelock Gym Lock Hall | `Gym - Warden Hall` | — | Gym 3 lobby |
| 171–174 | Tidelock Basins & Warden's Pool | `Gym - Warden Hall` | `Drip - Nadir` (45–55) | Stone water acoustics |
| 180 | Lumen City - The Concourse | `Town - Zenith` | `Machinery - Zenith` (55) | v4.3 `#24` |
| 181 | Lumen City - The Lowlight | `Town - Nadir` | `Machinery - Zenith` (65) | v4.3 `#25` |
| 182–183 | Lumen PC / Arcade 1F | `Poke Center` / `Poke Mart` | — | Keep stock |
| 185 / 186 | Meridian Spire Lobby / Gala Hall (`186` was `""`) | `Theme - Meridian` | `Machinery - Zenith` (40) / — | Fixes empty Gala BGM |
| 187, 189 | Glide Cycles / Lumen Apt (were `""`) | `Town - Zenith` | — | Fixes empty BGM |
| 188 | Lumen Fossil Lab (was `""`) | `Intro - Larch Lab` | `Machinery - Zenith` (35) | Fixes empty BGM |
| 190–193 | Circuit Gym (Gym 4) | `Gym - Warden Hall` | `Machinery - Zenith` (45–60) | Relay hum |
| 255 | Cindervault - Tap Chamber | `Route - Ashkaar` | `Lava - Ashkaar` (75) | Volcanic caldera |
| 280, 285 | Verdance Market Terraces / Briar Upper Court | `Town - Elowen` | `Gossamer Deepwood` (45 / 40) | v4.3 `#9 Town - Verdance` |
| 281–282 | Verdance PC / Mart | `Poke Center` / `Poke Mart` | — | Keep stock |
| 286–287 | Briar Hall Great Hall / Throne Room | `Theme - Accord` | — | Royal palace |
| 295 | Cathedral of the Evergreen | `Mood - Mystery` | — | Sacred interior |
| 520, 527, 528, 541 | Coastal Elowen Routes (`Ferrymen`, `Lacecliff`, `Marram`, `Saltings`) | `Route - Elowen` | `Saltmere Harbor` (45–60) | Coastal surf |
| 521, 540, 552, 566 | Inland Elowen Routes (`Windfall`, `Thistledown`, `Dyers`, `Spinners`) | `Route - Elowen` | — | Sunny meadow roads |
| 522, 568 | The Glassed Orchard / The Rehearsal | `Mood - Mystery` | `Glassfall Bleed` (70) | Bleed anomalies (`#74`) |
| 523 / 542 | Hale Farmhouse / Brinewife's Rest | `Town - Ferrows Landing` / `Town - Elowen` | — | Cozy interiors |
| 524, 525, 526 | Gossamer Wood / Deepwood / Woodward's Hut | `Route - Elowen Forest` | `Gossamer Deepwood` (65 / 75 / —) | `AUDIO.md:259` |
| 544, 545, 564 | Brinecut Mine 1F/B1F & Gullcry Caves | `Dungeon - Cave` | `Drip - Nadir` (60 / 70 / 65) | `AUDIO.md:260` |
| 546 / 547 | Thistledown Manor / Attic | `Dungeon - Manor` | — / `Wind - Isenmar` (35) | Cold haunted attic |
| 548, 608 | Cocoonfall Hollow / Shattered Lowlight | `Route - Antumbra` | `Glassfall Bleed` (75) | Active Bleed zones |
| 560, 577 | Frostflat Causeway / Frostwick Pass | `Route - Borderlands` | `Wind - Isenmar` (55 / 70) | Borderland winds |
| 561–563, 578–579 | Isenmar Roads (`Gullcry`, `Rimewood`, `Glade`, `Path`, `Wolfsrime`) | `Route - Isenmar` | `Wind - Isenmar` (55–65) | `561` also dynamic `Rain.ogg` |
| 570 | Frostwick | `Town - Isenmar` | `Wind - Isenmar` (50) | v4.3 `#8` |
| 571–572 | Frostwick PC / Exchange Mart | `Poke Center` / `Poke Mart` | — | Keep stock |
| 573–576 | Frostwick Interiors (were `""`) | `Town - Isenmar` | — | Fixes empty BGM |
| 582 | Lumen West Gate | `Town - Zenith` | `Machinery - Zenith` (40) | Gatehouse hum |
| 920, 924, 928, 929 | War Arc Front (`Rimed Sands`, `Siege Camp`, `Pavilion`, `Mesa`) | `War - March` | `War - Distant Battle` (65/70/35/55) | Ch19 War Theatre |
| 925 / 926 | The Steamline / The Glass Dunes | `War - Battlefield` | `Glassfall Bleed` (70) / `War - Distant Battle` (75) | Ch19 Climax |
| 930 | The Bone-Carters' Camp | `Route - Ossaria` | `War - Distant Battle` (40) | Scavenger camp |
| 951 / 952 | Meridian Spire Service Lifts / Plate Vault | `Route - Nadir` / `Mood - Tension` | `Machinery - Zenith` (65) / `Glassfall Bleed` (55) | Ch5 climax |
| 990 | Prismfall Test Arena | `Town - Crownhaven` | — | QA arena |

---

## 4. `pbs/trainer_types.txt` + Plugin Hooks (6 ME, 10 SE, 25 Voice Blips, Bosses, Festival, Title)

### 4A. `pbs/trainer_types.txt` (All 67 NPC Types → Manifest BGMs)
- `17 LEADER_*` (excl. `JUNO`) + `LEADER_ROWAN` → `Battle - Warden` *(Phase-2 v4.3: bespoke `Battle - Warden <Name>`, esp. creator-locked `Battle - Warden Nyx`)*
- `RIVAL_JUNO` & `LEADER_JUNO` → `Battle - Juno` | `RIVAL_KESTREL` → `Battle - Kestrel` (`IntroBGM = Theme - Kestrel`)
- `CHAMPION_VALEN` → `Battle - Valen` (`IntroBGM = Theme - Accord`, `VictoryBGM = Victory - Sovereign`)
- `HOLLOW_GRUNT{,_M,_F}` → `Battle - Hollow` | `HOLLOW_ADMIN/_WICK/_THISTLE/_TEO/_SABLE` → `Battle - Hollow Admin` | `HOLLOW_MOURNER` → `Battle - Mourner` (`IntroBGM = Theme - Hollow`)
- `MERIDIAN_AGENT{,_M,_F}` → `Battle - Meridian` | `MERIDIAN_ADMIN/_MARCHETTI/_KROLL/_ASHE/_QUENT/_DIRECTORATE` → `Battle - Meridian Admin` | `MERIDIAN_VOSS` → `Battle - Voss` (`IntroBGM = Theme - Meridian`)
- `10 FESTIVAL_*` cameos → `Battle - Cameo` | `GILDED_THEODRIC` → `Battle - Voss` (or `Battle - Ruin`) | `ECHO_MORWEN` → `Battle - Warden` | `REFLECTION` & `ARCHSEER_DASK` → `Battle - Ruin`
- `ASHKAAR_SOLDIER{,_M,_F}` / `_OFFICER` & `ISENMAR_SOLDIER{,_M,_F}` / `_OFFICER` → `War - Battlefield`
- `OCTAVE_VESPER` & `OCTAVE_SINGER` → `Battle - Cameo` (or new `Battle - Octave`)

### 4B. 6 CC0 `Audio/ME/` & 5 Unwired CC0 `Audio/SE/` Hooks
- **Sync all 50 CC0 `.ogg`s** (`gemini_recommends/2026-11-21_audio-mastering-and-soundscape/Audio/{BGS,ME,SE}/*.ogg` → `audio/gemini_cc0/`), update `audio/manifest.tsv:67-69,71` from `(stock base project)` to `gemini_cc0/ME/...`, and append `2 ME` (`Warden Badge Get`, `Trial Rank Up`) + `25 SE` (`Voice - *.ogg`) rows → **119 manifest rows**.
- **3 ME hooks:** `017_GameOver.rb:14` (`GAME_OVER_ME = "Prismfall game over"`); `003_Badges_Gyms.rb:79` (`pbMEPlay("Warden Badge Get")` on new badge); `005_Trials_Quests.rb:258` (`\me[Trial Rank Up]`).
- **5 SE hooks:** `010_Bridge_VersusIntro.rb:309` (`"VS Cutin Lightning"`), `005_Bosses_Effects.rb:51` (`"Boss Shield Break"`), `008_Bridge_Transitions.rb:124` (`"Glass Quench"`), `003_Bridge_EBDX.rb:53` (`"Field Shatter"` on non-staged field swaps), `136_Field_PrismArena.rb:95` (`"Prism Arena Swell"`).
- **Title / Bosses / Festival / Endings:** Set `$data_system.title_bgm = "Title - Prismfall"` in `017_GameOver.rb:179`; add `:music` to all 10 bosses (`101–106` & `mapgen/bosses.yaml`); add `:bgm`/`:victory_bgm` to `008_Festival_Data.rb:121-136` & `009_Festival.rb:281-288`; play `:bgm` in `018_Endings.rb:60`.

### 4C. Selftest-Safe `VoiceTicker` Hook for All 25 Cast `Voice - *.ogg` Blips (`014_Portraits.rb`)
Every one of the 25 v4.3 `Voice - *.ogg` files maps 1-to-1 from `CAST` (`014_Portraits.rb:86-96`) via `"Voice - #{key.to_s.sub(/_[AB]\z/, '').capitalize}"`. Adding a ~25-line `VoiceTicker` inside `pbMessageDisplay` (`014_Portraits.rb:815-833`, guarded by `msgwindow.respond_to?(:busy?) && msgwindow.respond_to?(:position)` for selftest safety, `VOICE_STRIDE = 3` chars, `VOICE_COOLDOWN = 0.068s`, `±3` pitch variance, skipped on instant-complete bursts `delta > 8`) activates character dialogue voices across all 25 cast members immediately — even in `:plain` portrait mode.
