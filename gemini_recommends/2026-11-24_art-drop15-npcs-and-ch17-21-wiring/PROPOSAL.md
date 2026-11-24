# Art Drop 15 NPCs, Unwired Cast Overworlds, Ch9 Unmasking Movie (`016_Movies.rb`), and Full National Dex EBDX Packaging — Wiring Proposal

- **Date:** 2026-11-24
- **Author:** Gemini (Full-Game Art Coverage & Claude Wiring Gap Auditor)
- **Status:** 100% file-and-line verified against live `plugins/`, `pbs/`, `tools/`, `graphics/`, `Movies/`, and all 117 built `maps_out/Data/Map*.rxdata` files. Zero repo source files modified by this audit.
- **Verification Scope:** Every asset referenced below is **already pushed on disk** in `graphics/` and `Movies/` (verified 2026-11-24).

---

## Executive Summary — What Is Pushed on Disk Right Now vs. What Is Unwired

| Category | Pushed on Disk | Currently Wired in Ruby / PBS / Packager | Exact Unwired Gap Found |
|---|---:|---:|---|
| **Dialogue Portraits** (`graphics/Portraits/`) | **613 PNGs** (51 prefixes; 12× each, Juno 13×) | All 51 prefixes are in `014_Portraits.rb` `CAST` | `:surprised` missing from `EXPRESSIONS` (51/51 have `*_surprised.png`!); script tags `OKORO` / `SALLOW` / `REFLECTION` not mapped in `014_Portraits.rb` |
| **Overworld Charsets** (`graphics/Characters/`) | **50 cast PNGs** (all portrait cast except `EIRIK`) + 39 `trainer_*` + 3 `act_*` | Only 30 cast in `025_CharsetAliases.rb`; **AND L42 `name.start_with?("trainer_")` silently blocks all `"NPC XX"` events!** | **17 pushed cast overworlds unwired** (10 Drop-15 NPCs + `MAELIS`, `ROWAN`, `TEO`, `WICK`, `WENLOW`, `MORWEN`, `DASK`, `VENAM`) + **Vesper silently broken on built `Map 145 #10`** (`NPC 14`)! |
| **Trainer Battle Strips** (`graphics/Trainers/`) | **52 PNGs** (40 front strips + 12 back strips) | 38 of 40 fronts in `pbs/trainer_types.txt` | `[LARCH]` and `[WENLOW]` (`WENLOW.png` + `WENLOW_back.png`) pushed on disk but **missing from `pbs/trainer_types.txt`** |
| **VS Busts** (`graphics/EBDX/VS/`) | **38 cast busts** + 29 UI PNGs | All 38 resolve (26 explicit in `VS_IDS`, 12 Wardens via name); all 38 in `THEMES` | Minor symmetry: add explicit `VS_IDS` for the 12 Wardens + `"WENLOW" => :teal` theme |
| **Pillar 2 Sakuga Movies & Acting Sheets** (`Movies/` + `graphics/Characters/act_*`) | **4 `.ogv` movies** (`pf_ch5_spire_shatter(_safe)` + `pf_ch9_mourner_unmask(_safe)`) + **3 `act_*` sheets** | Only Ch5 `:SH1` / `:SH1_BURN` / `:SH1_EXIT` wired in `016_Movies.rb`; **`Movies/` omitted from `tools/package.sh`!** | **`pf_ch9_mourner_unmask(_safe).ogv` + `act_ch9_mourner_unmask.png` unwired in `016_Movies.rb`**, no `PF_NO_MOVIE` guard, no `Movies/` copy in `tools/package.sh` |
| **Full National Dex EBDX Animated Sprites** | `install_ebdx_animated_sprites.py` (`--scope all`, verified **1,408 / 1,420** dex, **819 / 819** live+spotlight, **2,663** strips, 0 failures) | Sits in `gemini_recommends/2026-11-23_.../` only | Not yet promoted to `tools/` or hooked into `tools/package.sh` |

---

## 1. Critical Fix + Full Cast Wiring: `plugins/Prismfall Core/025_CharsetAliases.rb`

### Two Verified Bugs Caught by Simulating All 117 Built `Map*.rxdata` Files
1. **Line 42 blocks every `"NPC XX"` event:**
   `if !target && event_name && name.start_with?("trainer_")` skips stock Essentials `NPC 01`–`NPC 29` sprites. Verified across all 117 built RXDATA maps, this **already silently broke `Vesper`** (`Map 145 #10`, event `'Vesper'`, sprite `'NPC 14'`) even though `"Vesper" => "VESPER"` is on line 29, and blocks **7 more live built-map cast events**:
   - `Map 100 #15` & `Map 109 #9`: `'Captain Edda'` (`NPC 14`)
   - `Map 100 #31`: `'Wenna Hale'` (`NPC 19`), `Map 523 #3`: `'Wenna'` (`NPC 16`)
   - `Map 100 #32`: `'Coll Hale'` (`NPC 03`), `Map 521 #23`: `'Coll (Headbutt tutor)'` (`NPC 03`)
   - `Map 106 #2`: `'Hesper Vane'` (`NPC 11`)
   - `Map 181 #25`: `'Dex'` (`NPC 02`)
   - `Map 287 #1`: `'Queen Maelis'` (`NPC 25`)
   - Plus `trainer_*` events already on built maps that lacked `NAME_ALIASES` entries: `Map 100 #14` & `Map 186 #6` (`'Calla'`, `trainer_SCIENTIST`), `Map 186 #8` (`'Hollis'`, `trainer_GENTLEMAN`), `Map 103 #6` (`'Rowan Ashby'`, `trainer_POKEMONRANGER_M`), `Map 160 #28` (`'Teo'`, `trainer_BURGLAR`), `Map 255 #5` (`'Wick'`, `trainer_CHANNELER`).
2. **Two false-positive collision traps caught & prevented:**
   - **Possessive trap (`Map 520 #41`):** Event `'Wenna\'s cousin'` (`NPC 16`) on Ferrymen's Mile would falsely match `/\bWenna\b/` because `'` is a regex word boundary! Guarding with `event_name[/\b#{who}\b(?!['’]s\b)/]` cleanly blocks `"Wenna's cousin"` while matching `"Wenna"` and `"Wenna Hale"`.
   - **Bare `"Pip"` trap (`Map 151 #57` + 2 Act I route trainers):** `Map 151 #57` is `'Apprentice Pip'` (`NPC 07`, Saltmere Playhouse stage manager — NOT Bastian's granddaughter **Pip Ore** from Ch14 Cragholm!), and `routes_craft.py` also has `TUBER_F Pip` (`541`) and `YOUNGSTER Pip` (`520`). Therefore **DO NOT alias bare `"Pip"`** — alias `"Pip Ore" => "PIP"` only (and future Ch14 Cragholm maps should name the event `"Pip Ore"` or set charset `"PIP"` directly).
3. **Note on `EIRIK`:** `graphics/Portraits/EIRIK*.png` (12 PNGs) is pushed, but **`graphics/Characters/EIRIK.png` does not exist yet** (queued for Art Drop 16). Adding `"Eirik" => "EIRIK"` now is 100% safe because line 45's `pbResolveBitmap("Graphics/Characters/#{target}")` guard falls back to the placeholder until `EIRIK.png` lands.

### Exact Unified Diff (`plugins/Prismfall Core/025_CharsetAliases.rb`)
```diff
--- a/plugins/Prismfall Core/025_CharsetAliases.rb
+++ b/plugins/Prismfall Core/025_CharsetAliases.rb
@@ -30,7 +30,18 @@ module Prismfall
     "Quent" => "QUENT", "Percival" => "QUENT", "Kroll" => "KROLL", "Sabine" => "KROLL", "Sable" => "SABLE",
     # The Gilded King (Path B rename, 2026-11-23): "Aurelius" never matches Voss's "Aurelian" (whole words). Not bare
     # "Gilded King": the Night of Masques actor who plays him would get the real King's sprite.
-    "Aurelius" => "THEODRIC", "Theodric" => "THEODRIC"
+    "Aurelius" => "THEODRIC", "Theodric" => "THEODRIC",
+    # Art Drop 14 & earlier cast (already pushed in Graphics/Characters/):
+    "Maelis" => "MAELIS", "Rowan" => "ROWAN", "Teo" => "TEO", "Wick" => "WICK",
+    "Wenlow" => "WENLOW", "Morwen" => "MORWEN", "Dask" => "DASK", "Imre" => "DASK", "Venam" => "VENAM",
+    # Art Drop 15 — 10 Core Story NPCs (all pushed in Graphics/Characters/):
+    # Not bare "Pip": Map 151 #57 is Saltmere stagehand "Apprentice Pip" (and routes 520/541 have trainers named Pip).
+    "Edda" => "EDDA", "Calla" => "CALLA", "Wenna" => "WENNA", "Hesper" => "HESPER",
+    "Coll" => "COLL", "Dex" => "DEX", "Pip Ore" => "PIP", "Hollis" => "HOLLIS",
+    "Maud" => "MAUD", "Ellery" => "MAUD", "Hierophant" => "MAUD", "Martin" => "MARTIN",
+    # Future-safe (line 45 guards missing files; EIRIK.png overworld queued in Art Drop 16):
+    "Eirik" => "EIRIK"
   }
 
   def self.charset_alias(name, event_name = nil)
@@ -39,8 +50,9 @@ module Prismfall
     key = [name, event_name]
     return @charset_alias_cache[key] if @charset_alias_cache.key?(key)
     target = CHARSET_ALIASES[name]
-    if !target && event_name && name.start_with?("trainer_")
-      NAME_ALIASES.each { |who, cs| target = cs if event_name[/\b#{who}\b/] }
+    if !target && event_name && (name.start_with?("trainer_") || name.start_with?("NPC "))
+      # Possessive guard (?!['’]s\b): prevents "Wenna's cousin" (Map 520 #41) from wearing Wenna's sprite.
+      NAME_ALIASES.each { |who, cs| target = cs if event_name[/\b#{who}\b(?!['’]s\b)/] }
     end
     target = nil if target && !pbResolveBitmap("Graphics/Characters/#{target}")
     @charset_alias_cache[key] = target || name
```

**Immediate Live Result (Zero Map Rebuilds Needed):** 16 built-map events across Maps `100`, `103`, `106`, `109`, `145` (Vesper!), `160`, `181`, `186`, `255`, `287`, `521`, and `523` immediately switch from generic placeholders to bespoke pixel-art charsets, with **0 false positives** across all 117 built RXDATA maps.

---

## 2. Portrait Wiring & Script Tag Alignment: `plugins/Prismfall Cutscenes/014_Portraits.rb`

### Verified Findings
- **Good news:** All 51 pushed portrait prefixes (`EDDA`, `CALLA`, `WENNA`, `HESPER`, `COLL`, `DEX`, `PIP`, `HOLLIS`, `MAUD`, `MARTIN`, `MAELIS`, `EIRIK`, `WENLOW`, etc.) are **already listed in `CAST` (`L86–97`)** — zero missing pushed prefixes!
- **4 real wiring gaps remaining in `014_Portraits.rb`:**
  1. **`:surprised` missing from `EXPRESSIONS` (`L59–70`):** All 51 pushed cast already have `*_surprised.png` on disk, and `mapgen/layouts/saltmere_rj.py:486,536,553,557` calls `surprised`. Adding `:surprised` gives bubble mode the proper backdrop & shock emote instead of falling back to `:neutral` *(verified safe against `selftest/suite.ruby_stub:518-519`, which only asserts `Bubble` & `art_kind == :expression`)*.
  2. **`OKORO` vs `DELPHINE` script mismatch:** `CAST:94` has `DELPHINE`, but `story/39_SCRIPT_CH20.md:248,260,264` writes `[portrait: OKORO, ...]`. Aliasing `:OKORO` → `art: :DELPHINE` ensures Ch20 resolves cleanly the moment Art Drop 16 pushes `DELPHINE*.png`. *(Reminder for Claude: `selftest/suite.ruby_stub:418-477` uses `:DELPHINE` and `L576` uses `:KASSAN` as no-art test fixtures — swap those selftest fixtures to a dedicated `:NO_ART_FIXTURE` once Art Drop 16 lands!)*
  3. **`SALLOW` vs `RENATA` script mismatch:** `CAST:94` has `RENATA` (`story/24_SCRIPT_CH5.md`), while `story/35_SCRIPT_CH16.md:226` writes `[portrait: SALLOW, neutral]`. Aliasing `:SALLOW` → `art: :RENATA` covers both tags.
  4. **`REFLECTION` missing from `CAST`:** `story/42_SCRIPT_RUIN_KING.md:23` writes `[portrait: REFLECTION, neutral]`. Adding `REFLECTION` to `CAST` (plus display-name registrations for `MAUD`, `GUTTER`, `OKORO`, `SALLOW`) ensures zero plain-box drops once Art Drop 16 ships.

### Exact Unified Diff (`plugins/Prismfall Cutscenes/014_Portraits.rb`)
```diff
--- a/plugins/Prismfall Cutscenes/014_Portraits.rb
+++ b/plugins/Prismfall Cutscenes/014_Portraits.rb
@@ -66,7 +66,8 @@ module Prismfall
       :deadpan => { :bg => [168, 168, 176], :emotes => [:dots] },
       :panic   => { :bg => [176, 216, 248], :emotes => [:sweat, :shock], :shake => 2 },
       :sad     => { :bg => [112, 128, 184], :emotes => [], :face => [:gloom] },
-      :blush   => { :bg => [255, 192, 208], :emotes => [], :face => [:blush] }
+      :blush   => { :bg => [255, 192, 208], :emotes => [], :face => [:blush] },
+      :surprised => { :bg => [255, 240, 176], :emotes => [:exclaim], :jolt => true }
     }
 
     # Optional per-character data: Prismfall::Portrait.register(:MARTIN,
@@ -91,9 +92,9 @@ module Prismfall
       DORIAN TAMSIN MARISOL ROOK SAHAR CORVIN BRANN KAITO ANJA
       ODESSA ILSA BASTIAN YSOLDE MAGNUS NYX CELESTINE SIGRUN
       HESPER TEO THISTLE SABLE KROLL QUENT MARCHETTI HOLLIS PIP MAUD DEX MORWEN
-      MAELIS DASK EIRIK HROTHGAR KASSAN RENATA GUTTER DELPHINE
+      MAELIS DASK EIRIK HROTHGAR KASSAN RENATA SALLOW GUTTER DELPHINE OKORO
       VESPER WENNA MARTIN WENLOW
-      THEODRIC VENAM COLL
+      THEODRIC VENAM COLL REFLECTION
     ]
 
     class << self
@@ -863,3 +864,7 @@ end
 # The Gilded King keeps his THEODRIC_* portrait files (Gemini rework 2026-11-23, Option 1 / Path B) but is shown as
 # "Gilded King Aurelius": [portrait: THEODRIC, smug] in scripts.
 Prismfall::Portrait.register(:THEODRIC, name: "Gilded King Aurelius", trainer: :GILDED_THEODRIC, cast: true)
+Prismfall::Portrait.register(:OKORO,    name: "Envoy Okoro",          art: :DELPHINE, cast: true)
+Prismfall::Portrait.register(:SALLOW,   name: "Councillor Sallow",    art: :RENATA,   cast: true)
+Prismfall::Portrait.register(:MAUD,     name: "Hierophant Ellery",    cast: true)
+Prismfall::Portrait.register(:GUTTER,   name: "Mother Gutter",        cast: true)
```

---

## 3. Ch9 Mourner Unmasking Movie + Acting Sheet Wiring: `plugins/Prismfall Cutscenes/016_Movies.rb`

### Verified Assets Already Pushed on Disk
- `Movies/pf_ch9_mourner_unmask.ogv` — 512×384, 24 fps Ogg Theora + 44.1 kHz Vorbis stereo, **14.000 s** (4.14 MB). Real `mkxp-z` native X11 playback verified (`movie_test_proof_ch9/movie_test.log`: `Graphics.play_movie` returned cleanly in `14.189 s`, post-movie `Graphics.update` clean).
- `Movies/pf_ch9_mourner_unmask_safe.ogv` — photosensitive-safe master, **14.000 s** (3.86 MB).
- `graphics/Characters/act_ch9_mourner_unmask.png` — **128×192** RGBA 4×4 sheet (32×48 per cell, all 16 cells populated and visually verified):
  - **Cells `0..3`** (Row 0): Masked Mourner braces → crimson energy crack → purple-white crystalline impact burst across mask.
  - **Cells `4..6`** (Row 1, cols 0–2): Mask fractures down center → flash → splits cleanly into two falling halves, lily flying off.
  - **Cell `7`** (Row 1, col 3): Unmasked Rowan Ashby revealed in Mourner cowl, staggering upright.
  - **Cells `8..11`** (Row 2): Wide-eyed shock, mask shard on floor, crystal glass sprouting on shoulder, dropping to knees.
  - **Cells `12..15`** (Row 3): Kneeling grim → head bowed (*"Look at the flowers. Look at what they're standing on."*) → listing sideways → collapsed forward onto the glass (*"like a tree going over"*).

### Critical Engine Note — `mkxp-z` OpenAL EOF & Trailing Black Frames
Inspected directly in `mkxp-z/src/display/graphics.cpp:236-296, 319-417`:
1. `Movie::play()` exits the loop as soon as `THEORAPLAY_isDecoding(decoder)` flips `false` and immediately runs `~Movie()`, which calls `alSourceStop(audioSource)` (`L410`) **before** OpenAL Soft has finished draining any buffered PCM tail (`AUDIO_BUFFER_LEN_MS = 2000`). Furthermore, `streamMovieAudio()`'s `while(true)` wait on `AL_BUFFERS_PROCESSED` (`L289-293`) does not poll `audioThreadTermReq`, and `~Movie()` destroys `audioMutex` (`L404`) before `SDL_WaitThread(audioThread)` (`L407`).
2. **Consequence for `.ogv` masters:** Every Pillar 2 `.ogv` MUST include **≥ 0.5 s (12 frames) of trailing pure-black video (`YAVG = 16.0`) + matching Vorbis silence** at EOF so (a) final SFX/music tails finish playing through OpenAL before `alSourceStop`, and (b) the hard cut back to the map exits from pure black rather than flashing mid-frame.
3. **Audit of current `.ogv` tails (`ffmpeg signalstats`):**
   - `pf_ch5_spire_shatter(_safe).ogv`: ends cleanly at `YAVG = 16.0` (2 black frames).
   - `pf_ch9_mourner_unmask(_safe).ogv`: currently ends mid-fade at `YAVG = 41.6` (still plays cleanly in `14.189 s` in mkxp-z, zero crash). Holding a black screen tone around `Graphics.play_movie` in `016_Movies.rb` prevents any bright-frame snap on return, and any future re-encode (plus Peak #3–#5 movies) should pad 12 frames of pure black + Vorbis silence at EOF.

### Exact Unified Diff (`plugins/Prismfall Cutscenes/016_Movies.rb`)
```diff
--- a/plugins/Prismfall Cutscenes/016_Movies.rb
+++ b/plugins/Prismfall Cutscenes/016_Movies.rb
@@ -35,17 +35,28 @@ module Prismfall
       end
 
       def movie(name, volume: 100, skippable: true)
+        return false if ENV["PF_NO_MOVIE"] && !ENV["PF_NO_MOVIE"].empty?
         file = movie_file(name)
         return false if !file || !Graphics.respond_to?(:play_movie)
         pbBGMStop(0.0) rescue nil
         pbBGSStop(0.0) rescue nil
+        # Hold black on both sides of Graphics.play_movie (prevents bright-frame flash on return).
+        # Authoring contract (mkxp-z graphics.cpp OpenAL EOF): encode >=0.5s (12f) trailing pure-black
+        # video + matching Vorbis silence on every .ogv so OpenAL drains before ~Movie calls alSourceStop.
+        prev_tone = ($game_screen.tone.clone rescue nil) if defined?($game_screen) && $game_screen
+        $game_screen.start_tone_change(Tone.new(-255, -255, -255, 0), 0) if defined?($game_screen) && $game_screen
         2.times { Graphics.update }
         begin
           Graphics.play_movie(file, volume, skippable)
         rescue ArgumentError
           Graphics.play_movie(file, volume)      # older mkxp-z: no skippable argument
         end
+        if defined?($game_screen) && $game_screen
+          $game_screen.start_tone_change(prev_tone || Tone.new(0, 0, 0, 0), 6)
+        end
         2.times { Graphics.update }
         return true
       rescue StandardError => e
@@ -107,6 +118,22 @@ module Prismfall
       :SH1_EXIT => proc {
         ev = Cutscene.find_event("Mourner")
         ev&.erase
+      },
+      # Ch9 Peak #2, the Mourner Unmasked (Map 264 Reliquary, story/27_SCRIPT_CH9.md IR-1):
+      # 1) :IR1 plays the brace/blast anticipation (cells 0..3), fires Movies/pf_ch9_mourner_unmask(_safe).ogv
+      #    (14.0s; on fallback without movie, steps through mask split cells 4..6), and holds cell 7 (Rowan
+      #    revealed in cowl) for Juno's "...Uncle Rowan?" dialogue.
+      # 2) :IR1_COLLAPSE plays cells 8..15 after Rowan's "Look at the flowers..." line as he folds forward.
+      :IR1 => proc {
+        Cutscene.act("Mourner", "act_ch9_mourner_unmask", frames: 0..3, hold: [0.28, 0.16, 0.10, 0.08])
+        if !Cutscene.movie("pf_ch9_mourner_unmask")
+          Cutscene.fallback_flash([255, 180, 210])
+          Cutscene.act("Mourner", "act_ch9_mourner_unmask", frames: 4..6, hold: [0.14, 0.12, 0.18])
+        end
+        Cutscene.act("Mourner", "act_ch9_mourner_unmask", frames: [7], hold: 0.25)
+      },
+      :IR1_COLLAPSE => proc {
+        Cutscene.act("Mourner", "act_ch9_mourner_unmask", frames: 8..15, hold: [0.26, 0.22, 0.20, 0.22, 0.28, 0.32, 0.28, 0.40])
       }
     }
   end
```

---

## 4. Packaging & Full National Dex Animated Sprite Hooks: `tools/package.sh`

### Two Verified Gaps in `tools/package.sh`
1. **`Movies/*.ogv` is NEVER packaged into `Prismfall_DevKit.zip`!** (`package.sh:45-54` copies `graphics/` and `art/out/Graphics/Portraits/`, omitting `Movies/` completely — so DevKit installs silently fall back to `fallback_flash`!)
2. **Upgraded `--scope all` Full National Dex `install_ebdx_animated_sprites.py` (`1a783fd`, verified `1,408 / 1,420` across all 4 views, `819 / 819` live+spotlight, `2,663` strips / `80.48 MB`, `0` failures):** Currently sits in `gemini_recommends/2026-11-23_gen6-9-sprites-postgame-legendaries-dorian-meloetta/install_ebdx_animated_sprites.py`.
   - Copy it to `tools/install_ebdx_animated_sprites.py` (then `package.sh:65` automatically includes it in `$OUT/Tools/`), AND add a clean 1-line optional hook in `tools/package.sh` so packaging can either bundle a prebuilt `--scope all` battlers directory (`PF_EBDX_BATTLERS`) or regenerate it on demand (`PF_EBDX_ENGINE` + `PF_SPRITE_SOURCES`).

### Exact Unified Diff (`tools/package.sh`)
```diff
--- a/tools/package.sh
+++ b/tools/package.sh
@@ -51,6 +51,12 @@ fi
 if [[ -d "$ROOT/art/out/Graphics/Portraits" ]]; then
   mkdir -p "$OUT/Graphics/Portraits" && cp "$ROOT"/art/out/Graphics/Portraits/*.png "$OUT/Graphics/Portraits/"
 fi
+# Pillar 2 sakuga cutscenes (Ogg Theora .ogv for mkxp-z Graphics.play_movie; 016_Movies.rb)
+[[ -d "$ROOT/Movies" ]] && mkdir -p "$OUT/Movies" && cp "$ROOT"/Movies/*.ogv "$OUT/Movies/" 2>/dev/null || true
+# Optional Full National Dex (--scope all, 1,408/1,420) EBDX animated battlers overlay:
+# Build with: python3 tools/install_ebdx_animated_sprites.py --engine "$ENGINE" --prismfall-pbs "$ROOT/pbs" --source renovation4="$SRC/chromevaliant_ebdx/Graphics/Pokemon" --source ghasty="$SRC/ghasty001" --fetch-showdown-gaps --install-prismfall --scope all --prefer-more-frames --upgrade-stock-non-b2w2 --out-battlers "$PACK" --verify-strips
+[[ -n "${PF_EBDX_BATTLERS:-}" && -d "$PF_EBDX_BATTLERS" ]] && mkdir -p "$OUT/Graphics/EBDX/Battlers" && cp -r "$PF_EBDX_BATTLERS"/{Front,Back,FrontShiny,BackShiny} "$OUT/Graphics/EBDX/Battlers/"
+[[ -f "$ROOT/gemini_recommends/2026-11-23_gen6-9-sprites-postgame-legendaries-dorian-meloetta/install_ebdx_animated_sprites.py" && ! -f "$ROOT/tools/install_ebdx_animated_sprites.py" ]] && cp "$ROOT/gemini_recommends/2026-11-23_gen6-9-sprites-postgame-legendaries-dorian-meloetta/install_ebdx_animated_sprites.py" "$OUT/Tools/"
 
 # Docs
 cp "$ROOT"/design/*.md "$OUT/Design/" 2>/dev/null || true
```

---

## 5. Minor Parity Cleanup: `pbs/trainer_types.txt` & `010_Bridge_VersusIntro.rb`

1. **`pbs/trainer_types.txt` (bottom, after line 548):** Two pushed trainer sprites (`graphics/Trainers/LARCH.png`, `graphics/Trainers/WENLOW.png` + `WENLOW_back.png`) currently have **no trainer type definition in `pbs/trainer_types.txt`** (needed for Ch14 optional Larch spar M5 and Ch16 Interlude IV playable Wenlow `V119 = 4`):
   ```ini
   #-------------------------------
   [LARCH]
   Name = Lattice Scholar
   Gender = Female
   BaseMoney = 100
   SkillLevel = 100
   BattleBGM = Battle Elite
   VictoryBGM = Battle victory leader
   #-------------------------------
   [WENLOW]
   Name = Apprentice Medic
   Gender = Male
   BaseMoney = 60
   SkillLevel = 100
   BattleBGM = Battle trainer
   VictoryBGM = Battle victory trainer
   ```
2. **`plugins/Prismfall EBDX Bridge/010_Bridge_VersusIntro.rb`:** All 38 pushed VS busts already resolve cleanly. Optional hygiene: add `"WENLOW" => :teal` to `THEMES` (line 69) and check `player_id` (lines 97–102) when Ch16 Interlude IV (`V119 = 4`) is built so playable Wenlow uses his portrait/bust instead of `PLAYER_A`.

---

## 6. Gemini-Owned Map Fixes (`TODO_QUOTA.md` §1) — Exact Verified Diffs & Ownership Sign-Off

Per `TODO_QUOTA.md` §1 and `REVIEW.md:131`, the following bugs live in Gemini-owned layout scripts (`mapgen/layouts/routes_craft.py`, `saltmere_rj.py`, `briarwick_rj.py`, `story_ch5.py`, `lumen_interiors.py`). **All line numbers were re-verified live on 2026-11-24** (still unpatched):

| # | File & Verified Lines | Exact Verified Bug | Minimal Fix |
|---|---|---|---|
| **A11** | `mapgen/layouts/routes_craft.py:281, 285` | Map `528` Marram Down north dune stairs use `range(H)`, placing them on the south beach foredune (`y=53..56`) and isolating 10 events (Saltmere Beacon, Sledge Run, 2 trainers, 4 items) | Change `range(H)` → `range(40)` on **L281** and **L285** (`for x0, h in ((61, 1), (57, 2), (53, 3)):` and `yy = max(y for y in range(40) if m.ht[y, 99] == 1)`) |
| **G1** | `mapgen/layouts/routes_craft.py:165, 315, 578, 765, 2361` | 5 two-choice prompts set `'cancel': 1` (1-indexed = runs Option 1 on Escape/B instead of Option 2!) on `527`/`528`/`541`/`552`/`566` | Change `'cancel': 1` → `'cancel': 2` on all 5 lines |
| **G2** | `mapgen/layouts/routes_craft.py` (520/521/524/528/540) | Zero `HeadbuttTree` events anywhere (5 wild lines unobtainable); `528` hollow `ak_rock2` sea rock & `540` roof pine on `sh_big`; repeatable healers missing on `528`/`540` | Add `pbHeadbutt` tree events on routes matching `pbs/encounters.txt`, fix `ak_rock2`/`sh_big` stamps, add repeatable Beacon/camp heal |
| **G3** | `mapgen/layouts/saltmere_rj.py:486, 536, 553, 557` + `806, 911` | 4 `:surprised` tags (fixed automatically by §2 above!); `146` Harbour & `147` Old Town missing `SnapEdges = true` | Add `SnapEdges = true` metadata to `build_146` and `build_147` |
| **G4** | `mapgen/layouts/briarwick_rj.py` (`120`/`126`) | `Map 126` (`bgm: Briarwick`) points to nonexistent BGM; `120` south skirt `SnapEdges` | Fix `126` BGM to valid track (`Lappet Town` / `Poke Center`) and add south-skirt `SnapEdges` |
| **G5** | `mapgen/layouts/story_ch5.py:134, 167-170, 215` & `lumen_interiors.py:253` | Spark the Pichu uses `'Followers'` instead of `'Followers/PICHU'` (invisible!); `181` Junction Boxes 1–4 clear on flee/loss; `Map 186` Gala Hall has `bgm=''` (dead silence!) | `'Followers'` → `'Followers/PICHU'` (L134, L215); wrap `WildBattle.start` win check around `pfm_lumen_box` & `Self:A` (L167–170); set `bgm='Cedolan City'` (or Gala BGM) on `186` (L253) |

**Ownership Recommendation for Reuben:** Since Gemini's focus is Art Drop 16+ & QA while Claude's map agent is already running Wednesday Pass 2 (`TODO_QUOTA.md` §1), **authorize Claude's map agent to apply A11 + G1–G5 directly** using the exact verified file:line table above so zero map softlocks wait on handoffs.

---

## 7. Next Art Queue Summary (Art Drop 16 → 17)

Full Ch0–Postgame breakdown + canon visual descriptions are catalogued in our scratch roadmap (`ART_COVERAGE_CH0_TO_POSTGAME.md`). Headlines for planning:
- **Art Drop 16 (Must-Have Bosses, Tag Partners & Ch14–21 Story Speakers):**
  1. **Mother Gutter (`GUTTER` / `SUMP_BARON`)** — Full boss+partner pack (12 portraits, OW, 16f front, **5f back**, VS bust) — 8 portrait calls + Ch17 critical tag partner + Ch18 + Postgame!
  2. **Dominar Hrothgar (`HROTHGAR`)** — 12 portraits + OW (10 speaking lines Ch15/Ch19 + live on built `Map 928 #3`!)
  3. **Prince-Elector Idris Kassan (`KASSAN`)** — 12 portraits + OW (8 portrait calls Ch14/Ch19)
  4. **Envoy Delphine Okoro (`DELPHINE` / `OKORO`)** — 12 portraits + OW (3 portrait calls Ch20 ending branch)
  5. **Councillor Renata Sallow (`RENATA` / `SALLOW`)** — 12 portraits + OW (2 portrait calls Ch5/Ch16 + live on built `Map 186 #9`!)
  6. **Thane Eirik OW (`Characters/EIRIK.png`)** — sole portrait cast member missing an overworld sheet!
  7. **Missing Tag-Partner / Follower Sprites:** `Trainers/HOLLOW_THISTLE_back.png` (Ch14 tag partner!), `Trainers/PARTNER_OGRE.png` + `PARTNER_OGRE_back.png` + `Characters/Followers/OGERPON.png` (Ch10 tag partner + Ch18 `S223` follower!)
  8. **Ch9/Ch17/Ch18 Boss & Officer Battle Sprites:** `THORNGUARD` (Captain Rowe, Ch18), `GILDER_AUTOMATON` (Terrace Warden Golurk, Ch17), `MERIDIAN_DIRECTORATE` (Mallory & Kade Ch17 + 15 PBS fights), `HOLLOW_ADMIN` (Hammer Captain Brisk, Ch9), `REFLECTION` (Ruin Route R1–R7 portraits + front + VS bust).
- **Art Drop 17 (Supporting Cast, Faction Grunts, Act V Variants & Cameos):**
  - Supporting cast: **Zainab Darzi** (`ZAINAB`/`SIDE_CARTER`), **Legate Varra Kosk** (`KOSK`), **Director Camille Ashe** (`MERIDIAN_ASHE`), **Prince Caedmon** (`CAEDMON`), **Carol** (`CAROL` + `OCTAVE_SINGER`), **Tage**, **Elder Ossa**.
  - Faction grunt battle strips: `HOLLOW_GRUNT_M/F`, `MERIDIAN_AGENT_M/F`, `ASHKAAR_SOLDIER_M/F` + `ASHKAAR_OFFICER`, `ISENMAR_SOLDIER_M/F` + `ISENMAR_OFFICER`.
  - Act IV–V story portrait variants (explicitly requested in `story/36–40`): Valen no-glove crystal arm + light, Voss pressure suit + harness, Ilsa no-earmuffs, Anja thin, Arceus speech bust, Ines memory.
  - Remaining 9 sister-game cameos (starting with **`FESTIVAL_SHELLY`**, already live on built Act I `Map 525`!).
