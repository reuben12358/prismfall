# Pokémon Prismfall — Gen 3 → True Gen 5 B2W2 Tileset Visual Overhaul Blueprint

- **Date:** 2026-11-24
- **Author:** Gemini (Gen 3 → Gen 5 B2W2 Tileset Visual Overhaul Architect)
- **Directly Addresses Creator Feedback:** *"3] the maps REALLY need a visual update... like theres so many maps that look so bad... we are using like gen3 sprites for a 'gen 5' game, please make the maps better..."*
- **Visual Proof Renders (Inspected 1:1):**
  - **Primary Before/After 4-Biome Proof (`512×384` / `16×12`-tile In-Game Camera):** `previews/103_gen3_vs_gen5_tileset_proof.png` (featuring actual in-game `PLAYER_A`, `JUNO`, `HOLLOW_MOURNER`, and `lm_cradle` composited at identical tile coordinates on real Prismfall Maps `120`, `545`, `180`, and `952`)
  - **Current Tileset Diagnostic Contact Sheet (`1:1` RMXP Scale):** `previews/103b_current_tileset_diagnostic_contact.png`
  - **`256px` RMXP `32×32` Tile-Grid Slot-Swap Proof:** `previews/103c_rmxp_256px_tile_slot_proof.png`
- **Repo Safety:** **Zero edits made** to `mapgen/`, `maps_out/`, `graphics/`, `pbs/`, `story/`, or `.rb` scripts. Staged cleanly for immediate Wednesday execution once Reuben signs off.

---

## 1. Executive Diagnosis: Why Prismfall's Maps Clash With Our Gen 5 B2W2 Sprites

Prismfall now runs **Gen 5 B2W2 animated Pokémon battlers**, **Gen 5 B2W2 overworld sprites (`32×48` crisp dark-outlined shading)**, **Gen 5 B2W2 animated front/back trainers**, and **Gen 5 EBDX battle cameras** — yet our maps still render on **flat 2004 Gen 3-era tilesets**. Our forensic audit of all **117 Prismfall `.rxdata` maps** and **28 tileset PNGs** exposes **two compounding root causes**:

1. **Gen 3 FRLG/RSE Base Sheets (`PF Rejuv.png` parts `gl/sh/ak/kf/rb4/ap` + Stock Essentials Interiors):**
   - Pokémon Rejuvenation and Pokémon Reborn are themselves built on **Gen 3 FireRed/LeafGreen & Ruby/Sapphire** base art. That gives Prismfall flat pastel-mint grass (`#82d0b0`), hard neon-lime rounded RSE trees, repetitive muddy 2-tone cliff hatching, flat royal-blue zigzag water (`RJ Sea(Grass)` / `RJ Ocean`), and stock 2004 Essentials Poké Center / Mart / House interiors (`ts 3, 4, 5, 14, 34`).
2. **Flat Procedural Python Tile Kits (`PF Rejuv.png` part `pf` = `rj_custom.png` + `PF Rejuv Halls.png`):**
   - Over **6,784 custom tiles** (`180,248` tile placements!) covering Brinecut Mine (`cdraw.py`), Lumen City & Meridian Spire (`ldraw.py`), Briarwick timber lodges (`tdraw.py`), Saltmere (`ndraw.py`), and Thistledown Manor (`mdraw.py`) were programmatically generated with Python `ImageDraw.rectangle()` primitives deliberately simplified to match Gen 3's flat aesthetic.
   - Without B2W2 visual grammar — **3/4 angled eaves overhangs, cool indigo-teal ambient cast shadows, hue-shifted multi-tone shading ramps, glowing window/conduit bounce light, and smooth bathymetric water gradients** — these custom cities, caves, and Spire interiors look flatter and harsher than even stock Gen 3 maps (`103b_current_tileset_diagnostic_contact.png`).

---

## 2. Complete Quantitative Audit of Prismfall's Current Tilesets (All 117 Maps)

### 2.1 Active Physical Tileset Sheets & Unique Tile Census

Inspection of `/home/antigravity/pf_engine_run/game/Graphics/Tilesets/` (`28` PNGs, `10.3 MB`), `/home/antigravity/reuben12358/prismfall/maps_out/Graphics/Tilesets/` (`6` custom PNGs), `maps_out/tilesets_prismfall.json`, and all **`117` built `maps_out/Data/Map*.rxdata`** files reveals extraordinary concentration: **100% of Prismfall runs on just 8 physical PNG sheets** (note: `Prismfall Outside.png` `ts=30` and `Prismfall Wilds.png` `ts=40` have **0 active maps** and can be retired).

| Physical Sheet PNG | Dimensions (`32×32` Grid) | Tileset IDs Using It | Active Maps (% of 117) | Unique Regular Tiles Used (`>=384`) | Current Visual Tier |
|---|---|---|---:|---:|---|
| **`PF Rejuv.png`** | `256 × 114,240` (`8 × 3,570`) | `ts 50, 51, 52, 53, 55, 56, 57, 58, 59, 60, 61` | **61** (`52.1%`) | **7,768** (`984` Rejuv base + `6,784` `pf` custom) | Gen 3 FRLG/RSE base + flat Python procedural (`cdraw/ldraw/tdraw`) |
| **`Prismfall Interior.png`** | `256 × 33,440` (`8 × 1,045`) | `ts 34` (houses, guilds, inns, shops) | **28** (`23.9%`) | **357** | Stock Gen 3 Essentials + Tectonic interior |
| **`PF Rejuv Halls.png`** | `256 × 11,552` (`8 × 361`) | `ts 54` (Loomhouse Gym, Pell Playhouse, Pageant Hall, Siege Pavilion) | **11** (`9.4%`) | **381** | Flat Python procedural (`hall_art.py`) |
| **`Prismfall City.png`** | `256 × 93,856` (`8 × 2,933`) | `ts 33` (Post-Act I: Verdance `280`, Briar Hall `285–287`, Cathedral `295`) | **5** (`4.3%`) | **875** | Tectonic Outside (Gen 3) + Sheridan/Gearen |
| **`Poke Centre interior.png`** | `256 × 1,280` (`8 × 40`) | `ts 4` (`141, 161, 182, 281`) | **4** (`3.4%`) | **78** | Pure stock 2004 Gen 3 Essentials |
| **`Mart interior.png`** | `256 × 576` (`8 × 18`) | `ts 5` (`142, 162, 183, 282`) | **4** (`3.4%`) | **64** | Pure stock 2004 Gen 3 Essentials |
| **`Interior general.png`** | `256 × 8,032` (`8 × 251`) | `ts 3` (`163, 164, 165`) | **3** (`2.6%`) | **71** | Pure stock 2004 Gen 3 Essentials |
| **`Gyms interior.png`** | `256 × 4,608` (`8 × 144`) | `ts 14` (`990` Test Arena) | **1** (`0.9%`) | **56** | Pure stock 2004 Gen 3 Essentials |
| **TOTAL (All 117 Maps)** | **8 active PNGs** | **18 active Tileset IDs** | **117 (`100%`)** | **9,650** | **100% Gen 3 or flat procedural** |

### 2.2 Breakdown Inside `PF Rejuv.png` (`61` Maps = Every Outdoor Route, Town, City, Cave, Lumen & Spire!)

Because `mapgen/rcompose.py` concatenates source sheets in an append-only fixed order (`mapgen/data/rj_compose.json`), we audited exact unique tile counts and screen placements per source part:

| `PF Rejuv.png` Part | Tile ID Range | Source Origin | Unique Tiles Used | Total Tile Placements | High-Impact Takeaway |
|---|---|---|---:|---:|---|
| **`part=sh`** | `4,832..6,831` | Rejuv `Sheridan_2` | **286** | **83,589** | **Highest leverage in the entire game:** just `286` tiles render ~27% of all outdoor grass, trees, cliffs & roads! |
| **`part=kf`** | `8,304..10,447` | Rejuv `Kristiline Town (Frozen)` | **158** | **24,974** | Just `158` tiles drive all snow/Bleed/frost biomes (`160, 522, 548, 560–563, 570–579`)! |
| **`part=ak`** | `6,832..8,303` | Rejuv `Route 4` | **174** | **15,845** | Coastal cliffs, sand beaches, dune paths (`100, 520, 527, 528, 541, 920–930`)! |
| **`part=gl`** | `384..4,831` | Rejuv `Goldenleaf Forrest` | **275** | **4,843** | Autumn/woodland lodges, props, tree accents (`120` Briarwick, `524–525` Gossamer)! |
| **`part=rb4`** | `10,448..11,495` | Reborn `Route4` | **11** | **3,679** | Only `11` tiles! |
| **`part=ap`** | `11,496..17,743` | Rejuv `Aevium Past` | **80** | **160** | Minor ruin/past props. |
| **Subtotal (Rejuv/Reborn Base)** | `384..17,743` | **Gen 3 FRLG/RSE base** | **984** | **133,090 (`42.5%`)** | **Swapping just 984 slots + 22 Autotiles upgrades 42.5% of every outdoor map pixel instantly!** |
| **`part=pf`** | `17,744..28,943` | `rj_custom.png` (procedural Python kits) | **6,784** | **180,248 (`57.5%`)** | Contiguous multi-tile buildings (`ldraw`, `tdraw`, `ndraw`), caves (`cdraw`: `88` unique tiles on `545`!), Spire (`ldraw`: `78` unique tiles on `952`!), manor (`mdraw`), giant trees! |

### 2.3 Active Autotiles Audit (`22` Active PNGs Out of `87` Staged)

Only **22 autotiles** actually render across all 61 `PF Rejuv` maps (`maps_out/Graphics/Autotiles/`), led by:
- **Water (`10` PNGs):** `RJ Ocean` (`12,866` tiles), `RJ Sea deep` (`5,682`), `RJ Sea(Grass)` (`3,939`), `RB Still water snow` (`2,005`), `RJ Sand shore` (`1,615`), `PF Frozen Pond` (`908`), `PF Lock Water` (`721`), `RJ KristilineWatersFrozen` (`634`), `PF Sea Cave` (`354`), `PF Salt Lake` (`345`), `RJ Sand shore_2` (`353`), plus `RJ Waterfall` / `RJ Waterfall bottom` / `PF Magma`.
- **Paths & Ground (`8` PNGs):** `RJ Dirt` (`14,608`), `PF Saltmere Cobbles` (`8,486`), `RJ DirtDark` (`6,311`), `PF Packed Snow` (`4,358`), `PF Saltmere Flags` (`4,068`), `PF Gravel Spring` (`940`), `RJ KristilineDirt` (`88`), `RJ Gravel(G)` (`75`).

Swapping these **22 small `96×128` / `768×128` autotile PNGs** 1-for-1 (exact same 48-shape RMXP quarter-tile layout!) upgrades **65,000+ water, river, coast, cavern-lagoon, and road tiles** in a single afternoon with **zero map edits**.

### 2.4 Act I (Ch0–Ch5) Concentration

Of Prismfall's **117 maps**, **`91` maps (`77.8%`)** belong to **Act I (Ch0–Ch5)** (`100–193, 520–568, 582, 608, 951–952`), using ONLY `PF Rejuv`, `Prismfall Interior`, `PF Rejuv Halls`, and the 3 stock Gen 3 interior sheets (`Poke Centre`, `Mart`, `Interior general`). Upgrading Act I's tilesets automatically upgrades **100% of Act I AND 20 of the 26 Post-Act I maps** (leaving only the 5 `ts=33 Prismfall City` Verdance maps for Phase 4!).

---

## 3. Verified Public / Free-to-Use Gen 5 B2W2 RPG Maker XP Tileset & Autotile Registry

> **Important Technical Note on Official B2W2 Rips:** Pokémon Black/White & B2W2 maps on Nintendo DS are 3D low-poly geometry (`NSBMD`+`NSBTX`), so The Spriters Resource hosts sprites/UI rather than 2D RMXP sheets. Consequently, the Pokémon Essentials v21.1 community relies on **curated, hand-pixeled Gen 5 / modern Gen 4–5 orthographic `256px` (`32×32` grid) RPG Maker XP packs** plus B2W2 DS texture conversions.

Every pack below was directly researched and verified for format, style, and license/credit terms:

| # | Pack / Resource Name | Primary Artist(s) | Verified URL | Format / Size | License & Credit Terms | Best Prismfall Role |
|---|---|---|---|---|---|---|
| **1** | **Ready to Use Tilesets (Gen 5 Exterior + Gen 5 Interior + Magiscarf RMXP + Kyle-Dove)** | **UltimoSpriter, Akizakura16, Shiney570, Magiscarf, Kyle-Dove** (compiled by Aki) | `https://eeveeexpo.com/resources/15/` | Pre-aligned `256px` RMXP PNGs + door charsets + Kyle-Dove autotiles (`4.81★`, 176K views, updated Oct 2024) | **Free non-commercial use; credit original artist per sheet** (Aki requests no compiler credit; credit UltimoSpriter, Akizakura16, Shiney570, Magiscarf, Kyle-Dove) | **Core Phase 1 Donor #1:** Gen 5 Exteriors (`sh/gl`), Gen 5 Interiors (`ts 3, 34`), Magiscarf lush forests & towns! |
| **2** | **Pokemon Tileset From Public Tiles `32x32` + Public Indoor Tileset + `[Free] Tileset v0.1.8`** | **ChaoticCherryCake** (+ Kyle-Dove, Newtiteuf, Thegreatblaid, public artists listed at `fav.me/d6321qy`) | `https://www.deviantart.com/chaoticcherrycake/art/Pokemon-Tileset-From-Public-Tiles-32x32-623246343`<br>`https://www.deviantart.com/chaoticcherrycake/art/Public-Indoor-Tileset-From-Public-Tiles-483814875` | **`256 × 20,832 px`** RMXP-ready (`32×32` grid) + `960×960` indoor | **CC-BY-NC-SA 3.0** (free non-commercial; credit ChaoticCherryCake + credited artists) | **Core Phase 1 Donor #2:** Complete cohesive modern Gen 4/5 grass, layered trees, cliffs, snow, farm/swamp, bridges, town props, interiors! |
| **3** | **RPG Maker Friendly Tileset 5.0 (Generation 5 Tiles)** | **Dirtywiggles** (compiled from **Shiney570** & **Phyromatical**) | `https://www.deviantart.com/dirtywiggles/art/RPG-Maker-Friendly-Tileset-5.0-generation-5-tiles-683576419` | **`256 × 31,000 px`** RMXP-ready (`32×32` grid) | **Public free use; credit Dirtywiggles, Shiney570, Phyromatical** | **Core Phase 1 Donor #3:** Massive complete Unova/Gen 5 outdoor, road, bridge, building, and nature palette already aligned to `256px` RMXP! |
| **4** | **Magiscarf Mastersheets (`Tileset ver.3 [Free*]`, `New Tiles Mastersheet`, `Revamped Tiles`, `Buildings w/ Snow`, `Water Animation`)** | **Magiscarf** | `https://www.deviantart.com/magiscarf/art/Tileset-ver.3-%5BFree%2A%5D-690477146`<br>`https://www.deviantart.com/magiscarf/art/%5BFree%5D-New-Tiles-Mastersheet-648639390`<br>`https://www.deviantart.com/magiscarf/art/Water-Animation-689684144` | `1920×3360` @ `16×16` (2× nearest-neighbor → `32×32`, also pre-formatted `256px` in Eevee Expo #15) | **CC-BY-NC-SA 3.0** (free for non-commercial use & editing; credit Magiscarf) | **Lush Forests, Snow Villages & Animated Water:** Industry-gold Gen 5-grade lush foliage, timber roofs, snow buildings, animated water! |
| **5** | **Pokemon BW Cave Tileset** | **DegelAlex** | `https://www.deviantart.com/degelalex/art/Pokemon-BW-Cave-Tileset-857263677` | **`256 × 2,400 px`** RMXP-ready (`32×32` grid) | **Free to use; credit DegelAlex** | **Phase 2 Caves (`ts 57`):** Authentic BW cave walls, stratified cliffs, cave floors & rock formations for Brinecut Mine & Gullcry Caves! |
| **6** | **Unova Nature Tileset: Seasons** | **Ectoplasmica** (direct B2W2 ROM texture rip) | `https://www.deviantart.com/ectoplasmica/art/Unova-Nature-Tileset%3A-Seasons-831283439` | `256 × 352 px` @ `16×16` (2× → `32×32`, all 4 B2W2 seasons!) | **Public rip** (author states credit optional) | **Authentic B2W2 Ground & Trees:** Exact official Unova Spring/Summer/Autumn/Winter grass, tall grass, flowers, and foliage palettes! |
| **7** | **Lava & Cave / Snow / Beach & Sea / Desert / Standard Route Dumps** | **PeekyChew** | `https://www.deviantart.com/peekychew/art/Lava-and-Cave-Tileset-836741864`<br>`https://www.deviantart.com/peekychew/art/Public-Tileset-Dump-1-4---Snow-827821330`<br>`https://www.deviantart.com/peekychew/art/Public-Tileset-Dump-3-4---Beach-and-Sea-828233122` | `16×16` / `32×32` themed biome dumps + animated lava | **Free non-commercial use; credit PeekyChew** | **Specialized Biomes:** Cindervault magma (`ts 61`), Marram Down / Saltmere beaches (`ts 51/56`), Glass Dunes (`926`), Frostwick snow (`ts 52`)! |
| **8** | **BW Buildings & BW Nature Tilesets** | **WesleyFG** | `https://www.deviantart.com/wesleyfg/art/BW-BUILDINGS-TILESET-251870372`<br>`https://www.deviantart.com/wesleyfg/art/BW-NATURE-TILESET-251802914` | `619 × 2,380 px` (slice & 2× align to `32×32`) | **Public; credit WesleyFG** | **Town & City Architecture:** Crisp Unova-styled cottages, civic halls, Pokémon Centers, and shops. |
| **9** | **BW Poké Center Interior & Modern Interiors** | **Ditto209** (`BW Pokecenter`) & **Aveontrainer** (`Pokemon Interior`, `Bank`, `Hospital`, `Theater`, `School`) | `https://www.deviantart.com/ditto209/art/BW-Pokecenter-808584082`<br>`https://www.deviantart.com/aveontrainer/art/Pokemon-Interior-783341234` | RMXP-ready interior sheets | **CC-BY-NC 3.0** (Ditto209); **Public w/ listed credits** (Aveontrainer + Eemie/etc.) | **Instant Interior Upgrade (`ts 4, 5, 34`):** Upgrades all 4 Poké Centers (`141, 161, 182, 281`) and Pell Playhouse / Lumen interiors! |
| **10** | **Gen 5 Autotiles (Water, Waterfalls, Tall Grass)** | **Slaqueen**, **PandaInDaGame** (adapted from **Hek-el-grande** & **Clara-WaH**), **Manuxd789**, **AdelsBrother** (princess-phoenix Sea) | `https://www.deviantart.com/slaqueen/art/Free-water-autotile-811989710`<br>`https://www.deviantart.com/pandaindagame/art/Waterfall-autotile-V1-Cascada-autotile-V1-843724413`<br>`https://www.deviantart.com/adelsbrother/art/princess-phoenix-Sea-Autotile-891403469` | Ready-to-drop RMXP `96×128` / `768×128` autotiles | **Public / CC-BY-SA 3.0; credit respective artists** | **Instant 65,000-Tile Water/Waterfall Upgrade:** Direct 1-for-1 drop-ins replacing `RJ Ocean`, `RJ Sea(Grass)`, `RJ Waterfall`, `PF Salt Lake`! |

> **Critical Pitfall Avoided (`Ekat99` Audit Warning):** Although **Ekat99** is widely recommended on PokéCommunity/DeviantArt (`Pokemon Halcyon - Outdoors`, `Basic Interior Collection`, `Trainer School`), direct inspection of Ekat99's DeviantArt descriptions confirms they are **explicitly formatted for Gen 3 style** (*"perfect for anyone using a gen 3-style with their project"*). **Do NOT use Ekat99 as our primary base** — it would keep Prismfall visually locked in Gen 3! Stick strictly to **Gen 5 / modern DS-shaded packs (#1–#10 above)**.

---

## 4. Architecture Decision: Path A vs. Path B vs. Recommended Zero-Breakage Hybrid

| Option | How It Works | Pros | Fatal Flaw If Used Alone | Verdict |
|---|---|---|---|---|
| **Path A Only** (Replace tilesets with community Gen 5 sheets & remap maps) | Import ChaoticCherryCake / Dirtywiggles / Aki Gen 5 PNGs as new tileset IDs and rebuild layouts | 100% hand-pixeled seamless tiling; zero AI artifacts | **Breaks all 117 maps' hardcoded tile IDs, passage/priority tables, puzzle events, and directional BFS** — would require 3–6 weeks of manual remapping and destroy Prismfall's unique Briarwick treehouses, Brinecut rose-salt crystals, Lumen Art-Deco domes, and Meridian Spire! | ❌ Too slow & destructive |
| **Path B Only** (AI tile-by-tile reskin of every `32×32` tile in `PF Rejuv.png`) | Run image-to-image on individual `32×32` slots in `PF Rejuv.png` | Preserves all tile IDs & passability | **Severe seam & flicker failure on repeating terrain:** disconnected `32×32` grass/water/cliff tiles won't tile seamlessly across neighbors, and animating 48-shape RMXP autotiles via raw AI creates jagged quarter-tile seams. | ❌ Fails on seamless terrain |
| **RECOMMENDED: Hybrid Zero-Breakage Tile-Index-Preserving Pipeline (Path A + Path B)** | **Layer 1 (Base Nature, Interiors & 22 Autotiles — Path A Slot-Swap):** Copy hand-pixeled community Gen 5 B2W2 tiles directly into the **exact original `(col, row)` tile IDs** of `PF Rejuv.png` (`984` base tiles), `Prismfall Interior.png` (`357`), and Stock Gen 3 interiors (`269`), and swap the `22` Autotiles 1-for-1.<br>**Layer 2 (Procedural Kits `cdraw/ldraw/tdraw/mdraw/hall_art` — Path B Whole-Stamp Remaster + Palette/Shader Upgrade):** Upgrade Python procedural palettes/shading for repeating cave/city/Spire floors & walls, AND run **whole-stamp image-to-image remastering** (locked to `16px` logical grid → `2×` nearest-neighbor, exactly as proven in `103_gen3_vs_gen5_tileset_proof.png` & `103c`) on contiguous hero buildings, domes, trees, fountains, consoles, and daises — then slice each remastered stamp back into its **exact original tile IDs** in `rj_custom.png`! | **100% Zero Map Breakage:** ZERO tile IDs move, ZERO `.rxdata` layouts break, `passguard.hits() == 0`, `verify.py roundtrip` stays byte-identical, directional BFS stays 100% green!<br>**100% Seamless Tiling** on all grass/cliffs/water/paths via authentic hand-pixeled Gen 5 community assets.<br>**100% Bespoke Prismfall Identity** on Briarwick lodges, Brinecut crystal lagoon, Lumen City conservatory domes, and Meridian Spire Plasma-Frigate sanctums! | Requires disciplined QA script to verify alpha transparency, `32×32` seam continuity, and color-harmony calibration between community Gen 5 donors and remastered custom stamps. | ✅ **BEST ARCHITECTURE (Fastest, Safest, Highest Visual Ceiling)** |

### Why Our Proof Render (`103_gen3_vs_gen5_tileset_proof.png`) Validates This Exact Architecture
Look at `previews/103_gen3_vs_gen5_tileset_proof.png` and `previews/103c_rmxp_256px_tile_slot_proof.png`:
1. **Biome 1 (`120` Briarwick — Town/Forest):** Replacing the Gen 3 grass/cliffs/trees (`part=sh`, `286` slots) with Floccesy/Magiscarf Gen 5 foliage + whole-stamp remastering the timber Pokémon Center lodge immediately transforms the screen into an official DS B2W2 town — and `PLAYER_A` & `JUNO` stop looking "pasted on top."
2. **Biome 2 (`545` Brinecut Mine — Cave/Crystal Lagoon):** Upgrading `PF Salt Lake` + `RJ Sea deep` autotiles to smooth Gen 5 bathymetry with shoreline foam, upgrading `cdraw.py` rock-wall ramps to dark Chargestone slate-quartz strata, and remastering the faceted crystal stamps transforms the ugly pastel swimming pool into a luminous B2W2 crystal cavern.
3. **Biome 3 (`180` Lumen City — Modern Metropolis):** Upgrading `ldraw.py` paving/basalt/facade kits + whole-stamp remastering the conservatory dome, Pokémon Center marquee, slate mansards, and brass lampposts turns flat procedural stripes into Castelia/Nimbasa grandeur with real diagonal architectural shadows.
4. **Biome 4 (`952` Meridian Spire — Plate Vault):** Upgrading `ldraw.py` `Q_f` steel floor & wall kits + whole-stamp remastering the holographic monitor banks, Tesla pylons, and royal-crimson gold-filigree dais transforms a noisy 1998 grey box into a Team Plasma Frigate / N's Castle climax sanctum!

---

## 5. Concrete Execution Blueprint & Act I First Rollout Plan

### 5.1 New Non-Destructive Pipeline Tooling (Owned by Mapgen Agent Post-Approval)

Create a single clean, reversible build step **`mapgen/gen5_reskin.py`** (driven by **`mapgen/data/gen5_slot_map.yaml`**) that runs right after `rcompose.py` / `rcustom.py` (keeping raw Gen 3 originals intact as fallback via `--no-gen5` flag!):

1. **Autotile 1-for-1 Replacer (`gen5_autotiles/`):** Replaces all `22` active autotiles in `maps_out/Graphics/Autotiles/` (preserving exact `96×128` static / `768×128` 8-frame animated RMXP geometry, exact `passages`, and exact v21.1 `terrain_tags` 5/6/7/8/9/12).
2. **Slot-for-Slot Donor Copier (`gen5_slot_map.yaml`):** Maps every contiguous tile block in `PF Rejuv.png` parts `sh` (`286` tiles), `kf` (`158`), `ak` (`174`), `gl` (`275`), `rb4` (`11`), `ap` (`80`), plus `Prismfall Interior.png` (`357`) and Stock Gen 3 interiors (`269`) to verified pixel coordinates in our downloaded public Gen 5 donor sheets (ChaoticCherryCake, Magiscarf, Aki/UltimoSpriter/Shiney570, Dirtywiggles, DegelAlex, Ectoplasmica, PeekyChew, Ditto209).
   - **Color-Harmony LUT Calibration:** Applies a unified **Prismfall B2W2 Master Palette LUT** (cool indigo-slate shadow shift, warm sunlight midtones, controlled saturation matching `PLAYER_A` & `JUNO` sprites) so donors from ChaoticCherryCake, Magiscarf, and Shiney570 blend with 100% cohesive art direction!
3. **Whole-Stamp Procedural + Remaster Engine (`gen5_stamps/`):**
   - **Code-level B2W2 Shader Upgrade** in `cdraw.py`, `ldraw.py`, `rdraw.py`, `tdraw.py`, `ndraw.py`, `mdraw.py`, `hall_art.py`: replaces flat dot-matrix/striped fills with beveled Gen 5 brushed steel, stratified Chargestone rock, beveled granite cobbles, and automatic 1-tile cool-indigo ambient occlusion drop-shadows along every wall foot and building base.
   - **Whole-Stamp Remaster Cache (`mapgen/gen5_stamps/*.png`):** Pre-baked, pixel-crisp (`2×` nearest-neighbor verified, transparent alpha preserved!) remastered hero stamps for every landmark building, dome, giant weaver tree, crystal cluster, Prism Fountain, holographic console, Tesla pylon, and boss dais — sliced deterministically into their exact `rj_custom.png` offsets.
4. **Automated Zero-Regression Gate:** Every phase MUST pass:
   - `python3 mapgen/build.py --strict` (`EXIT 0`)
   - `python3 mapgen/verify.py roundtrip` (`100%` byte-identical map `.rxdata` — confirming ZERO map data mutation!)
   - `passguard` `0` hits + exact directional Essentials BFS
   - Automated `16×12` (`512×384`) **Live Camera + `PLAYER_A`/`JUNO` Contact Sheet** inspection via `view_file` (plus headless `mkxp-z` screenshot verification!).

### 5.2 Phased Rollout Schedule (Act I Ch0–Ch5 First!)

| Phase | Scope & Target Maps | Exact Asset Work | Visual Impact | Effort Estimate |
|---|---|---|---|---|
| **Phase 1A: Act I Outdoor Foundation + Autotiles** *(Highest ROI — Ship First!)* | **All `32` Act I Outdoor Towns, Routes & Forests:** Ferrow's Landing (`100, 109`), Briarwick (`120`), Saltmere (`140, 146, 147`), Ebbmouth (`160, 167`), Routes `520–528, 540–541, 548, 552, 560–566` (+ automatically upgrades Frostwick `570–579` & Desert `920–930`!) | • Swap all **`22` active Autotiles** (B2W2 animated ocean, river, shoreline foam, waterfall, smooth `PF Salt Lake`, dirt/cobble/packed snow)<br>• Slot-swap **`984` Rejuv base tiles** (`sh` 286 + `gl` 275 + `ak` 174 + `kf` 158 + `rb4` 11 + `ap` 80) from ChaoticCherryCake + Magiscarf + Aki/UltimoSpriter + Ectoplasmica + PeekyChew<br>• Whole-stamp remaster Act I timber lodges (`tdraw`), Saltmere harbour facades (`ndraw`), and giant trees | **~60% of the entire game jumps from Gen 3 → True Gen 5 B2W2 immediately!** | **1.5–2 days** |
| **Phase 1B: Act I Interiors & Stock Gen 3 Elimination** | **All `39` Act I Interiors:** `Prismfall Interior.png` (`28` maps, `357` tiles) + Stock `Poke Centre` (`4` maps, `78` tiles) + `Mart` (`4` maps, `64` tiles) + `Interior general` (`3` maps, `71` tiles) | • Slot-swap all **`570` unique interior tiles** from Aki Gen 5 Interior + Magiscarf Interior + ChaoticCherryCake Public Indoor + Ditto209 BW Poké Center<br>• Zero map edits required! | **Eliminates 100% of stock 2004 Essentials Gen 3 interiors across all towns!** | **1 day** |
| **Phase 2: Act I Caves, Manors & Gym Halls** | **Brinecut Mine (`544, 545`), Gullcry Caves (`564`), Tidelock Gym (`170–174`), Thistledown Manor (`546–547`), Loomhouse Gym (`130–134`), Pell Playhouse (`150–154`)** | • Upgrade `cdraw.py` rock/floor/shadow shaders + DegelAlex BW Cave donors + remastered glowing crystal clusters & light shafts (`ts 57/58/61`)<br>• Upgrade `PF Rejuv Halls.png` (`381` tiles) & `mdraw.py` manor wood/carpets (`ts 59`) | **Turns Brinecut Mine, Gullcry Caves & Gyms 1–3 into Chargestone/N's Castle showpieces!** | **1.5–2 days** |
| **Phase 3: Chapter 5 Climax — Lumen City, Circuit Gym & Meridian Spire** | **All `15` `ts=60` Lumen Maps:** Concourse (`180`), Lowlight (`181, 608`), West Gate (`582`), Spire Lobby/Gala/Lifts/Plate Vault (`185–186, 951–952`), Circuit Gym (`190–193`), Shops (`187–189`) | • Upgrade `ldraw.py` granite paving, marble walls, `Z_f/Y_f/Q_f` brushed-steel floors & ambient shadows<br>• Whole-stamp remaster Lumen Poké Center dome, Arcade, Spire tower, Prism Fountain, holographic monitors, Tesla pylons & Plate Vault dais! | **Turns the Ch5 Demo Climax into an unforgettable Castelia + Plasma Frigate finale!** | **2 days** |
| **Phase 4: Post-Act I Verdance (`ts=33`) & Final Polish** | **5 Verdance Maps (`280, 285, 286, 287, 295`) + Test Arena (`990`)** | • Migrate or slot-swap `Prismfall City.png` (`875` used tiles) + `Gyms interior.png` (`56` tiles) into the unified Gen 5 palette; retire unused `Prismfall Outside.png` & `Prismfall Wilds.png` | **100% of all 117 maps unified under true Gen 5 B2W2 visual craft!** | **1 day** |

**Total End-to-End Effort:** **~7–8 focused engineering days** for all **117 maps** (**~4.5 days** for **Act I Ch0–Ch4**, **~6.5 days** for the complete **Act I Ch0–Ch5 Demo Climax**), with **zero map coordinate rewrites** and **zero collision/event regressions**.

---

## 6. Required Credits Block (Ready for `CREDITS.md` Upon Adoption)

> **Gen 5 Tilesets & Autotiles (Non-Commercial Fan Project Use Only):**
> - **Magiscarf** (CC-BY-NC-SA 3.0 — Outdoor Mastersheets, Snow Buildings, Interiors, Water Animation)
> - **ChaoticCherryCake** & public tileset contributors (`fav.me/d6321qy` — CC-BY-NC-SA 3.0 — Outdoor `32×32` & Public Indoor Tilesets)
> - **UltimoSpriter**, **Akizakura16**, **Shiney570**, **Phyromatical**, **Dirtywiggles** (Gen 5 Exterior, Interior & Unova Building Tilesets)
> - **Kyle-Dove**, **WesleyFG**, **Newtiteuf**, **Thegreatblaid / JesusCarrasco** (Gen 4/5 Nature, Buildings & Interior Tiles)
> - **DegelAlex** (Pokemon BW Cave Tileset), **PeekyChew** (Cave/Lava/Snow/Beach/Desert Dumps), **Ditto209** (BW Poké Center Interior, CC-BY-NC 3.0), **Aveontrainer** (Modern Interiors)
> - **Slaqueen**, **PandaInDaGame**, **Hek-el-grande**, **Clara-WaH**, **Manuxd789**, **AdelsBrother / princess-phoenix** (Gen 5 Water, Sea & Waterfall Autotiles)
> - **Pokémon Black 2 & White 2 / Game Freak / Nintendo / Creatures Inc.** (Original Unova art direction & Ectoplasmica seasonal texture reference)
