# Prismfall — Curated Resources (Essentials v21.1 + EBDX 1.4.7.1)

**How to read this list**
- **Verdict** is compatibility with our stack: Essentials v21.1, v21.1 Hotfixes, Manurocker95's EBDX port 1.4.7.1, and the Prismfall plugins.
  - ✅ = works with that stack: either confirmed by the resource's own page or by the base repo, or it never touches the battle scene.
  - ⚠ = plausible but **not verified**, or needs extra work.
  - ❌ = known incompatible.
- Versions and dates were read from the Eevee Expo pages on 2026-11-13/15.
- Always credit the authors the pages list.

## 1. Battle sprites (Gen 5 style, animated)

**EBDX sprite format** (from the [EBDX docs](https://luka-sj.com/essentials/resources/EBDX/docs?page=3) and the repo files):
- One horizontal strip of **square frames**. EBDX gets the frame count as width ÷ height (e.g. `Front/001.png` is 1862×38 = 49 frames).
- Folders: `Graphics/EBDX/Battlers/{Front,Back,FrontShiny,BackShiny}` (+ a `Female/` subfolder), names `001.png` / `001_1.png`. No GIFs.
- Sprites are found by number first, then name, then the stock `Graphics/Pokemon/` folder.

| Resource | What | Verdict |
|---|---|---|
| **Bundled EBDX battlers** (in the base repo) | Animated BW sprites for **Gen 1–5 (#001–649)**, about 55 Gen 6 species, and 35 Gigantamax forms. Gen 7–9 fall back to static sprites in `Graphics/Pokemon/`. | ✅ |
| [Generation 9 Resource Pack](https://eeveeexpo.com/resources/1101/) (Caruban) v3.3.8, Oct 2026 | Gen 9 species/moves/PBS plus **static** resized Gen 1–9 battlers (front 192 px, back 288 px). The repo bundles v3.2.5. | ✅ as bundled. ⚠ If you upgrade, re-check its Hotfixes requirement and EBDX metrics. |
| [Open-Source EBDX Renovation Project](https://eeveeexpo.com/resources/1831/) (ChromeValiant) v4.0, Oct 2026 | Fork of *this exact port* (rebuilt on NikDie's EBDX). Adds **animated Gen 1–9 sprites incl. Megas**, a 60-FPS cap, frame-rate/lag fixes, the trainer hotfix off by default, SOS allies and HP thresholds. | ⚠ It *replaces* our EBDX and is the strongest upgrade path. Before switching, check that its `meta.txt` Name is still `Elite Battle: DX` (our bridge `Requires` it) and that `BattleSceneRoom#reconfigure` / `Battle::Scene#loadBackdrop` still exist. DBK is not compatible with it (author's answer in its thread). |
| [Ghasty_001's animated sprites](https://eeveeexpo.com/resources/1774/) ([GitHub](https://github.com/Ghasty001/Animated_sprites_by_Ghasty001)) | Hand-picked species as **GIFs**, free with credit. | ✅ after converting each GIF to a horizontal strip (EzGif "stack horizontally" or Aseprite). |
| [EBS Gen 6 + Gen 7 animated sprites](https://eeveeexpo.com/resources/291/) (Sturdy Ghost, 2019) | #650–807, "EBS-compatible png". | ⚠ EBS is EBDX's predecessor. The strip format is probably the same, but this is unverified. |
| [Animated Pokemon System](https://eeveeexpo.com/resources/1544/) (Lucidious89) v1.1.3 | Animated Gen 1–9 sheets, shinies, icons. | ❌ as a plugin (it's a **DBK add-on**). Its sprite sheets may be reusable as EBDX strips, but the sheet layout isn't confirmed. |
| [Sprite Positioner port](https://eeveeexpo.com/resources/1339/) (Manurocker95) | Tool to set EBDX metrics (`PBS/EBDX/pokemon.txt`). | ✅ The tool for misplaced or oversized sprites. |

## 2. Move & battle animations

| Resource | What | Verdict |
|---|---|---|
| **Bundled EBDX coded animations** | 386 move + 34 common animations in `[002] Animation Code`. | ✅ |
| [EBDX move & common animation pack](https://eeveeexpo.com/resources/1230/) (NikDie) v1.0.0, Dec 2024 | About 95% of the PBS move list plus Shadow moves. Merge its Graphics/Audio/Plugins folders; back up custom animations first, since it overwrites. | ✅ Made for EBDX. The port page credits NikDie and reports it works well. |
| [Ball Burst animations](https://eeveeexpo.com/resources/909/) (lichen) | Burst effects for newer Poké Balls. | ⚠ Referenced by the Renovation Project; not checked against 1.4.7.1. |
| [EBDX Stat Change Overlay](https://eeveeexpo.com/resources/941/) | Stat-change overlay. | ⚠ The Renovation Project "restored compatibility", which suggests the plain port needs a patch. |
| Vanilla animation editor fallbacks | EBDX Config: `CUSTOM_MOVE_ANIM = true` uses Essentials' editor animations for moves without coded ones. | ✅ |

## 3. BW-style UI

EBDX already supplies a Gen 5-style **battle** UI, including databoxes, command/fight menus and the battle bag.
The items below are for out-of-battle screens.

| Resource | What | Verdict |
|---|---|---|
| [Gen 5 Font "Truth and Ideals"](https://eeveeexpo.com/resources/861/) (bonzairob) | Black 2 fonts as TTF (main, small and outlined battle variants). Use at 10 px. | ✅ Font only. The Renovation Project uses it optionally. |
| [BW PokéMart Screen](https://eeveeexpo.com/resources/904/) (DeepBlue PacificWaves) v3.0 | Gen 5 mart UI, v21. | ✅ |
| [Bag Screen with interactable Party](https://eeveeexpo.com/resources/723/) (DiegoWT) v2.7.5, Apr 2026 | Overworld bag with a party panel and a **BW/B2W2 background** option. Needs small edits to `UI_ItemStorage` / `UI_PokeMart`. | ✅ The overworld bag only; EBDX's battle bag is separate. |
| [Gen V Summary Pack DX](https://eeveeexpo.com/resources/569/) (DeepBlue PacificWaves) | BW party and summary screens. | ⚠ Officially v20.1 only; one reviewer reports it working on v21. Skip its ZUD patches. |
| [Modular UI Scenes](https://eeveeexpo.com/resources/1325/) (Lucidious89) v2.0.9 | Modular Summary/Pokédex pages (not BW-styled). Requires Hotfixes only, **not** DBK. | ⚠ Out of battle, so it should be fine; not tested with EBDX's capture Dex entry. |
| [Voltseon's Pause Menu](https://eeveeexpo.com/resources/692/) v2.2 | Compact modern pause menu, v21.1. | ✅ Out of battle. If you see a `safeExists?` warning, replace it with `FileTest.exist?` (from a review). |

## 4. Tilesets & overworld

The Map Builder uses **stock Essentials tilesets**, so nothing here is required.

| Resource | What | Verdict |
|---|---|---|
| [Banished Platinum Outdoor Tileset](https://eeveeexpo.com/resources/876/) (Zygoat) | Gen 5-style trees and grass with upscaled Gen 4 buildings. | ✅ Map art only. ⚠ RMXP column width (8 tiles) unverified. |
| [ALL Official Gen 4 Overworld Sprites](https://eeveeexpo.com/resources/404/) (VanillaSunshine) v1.5 | Every HGSS/DPPt trainer and NPC overworld, "formatted for RMXP". Link to it rather than redistributing it. | ✅ Gen 4 style; the closest complete set to BW. |
| [Gen 4 trainer customization kit](https://eeveeexpo.com/resources/317/) (Poltergeist) | Modular front/back/overworld parts for custom trainers, free to edit. | ✅ Good for the original Wardens. |
| [Fakemon Festival Pack](https://eeveeexpo.com/resources/654/) (NocTurn) | Gen 4/5-sized fakemon battlers with some PBS. | ✅ Optional (regional variants or fakemon). Credit the pack. |
| BW tilesets on DeviantArt, e.g. [BW Spring Tileset](https://www.deviantart.com/thefloofypanthar/art/BW-Spring-Tileset-version-2-WIP-817532857) and [BW Citrine (resized)](https://www.deviantart.com/chimcharsfireworkd/art/BW-Citrine-Tileset-Resized-227350418) | True BW-style tiles. | ⚠ Licensing and RMXP layout unverified; check each page. |
| Following Pokémon EX overworlds | Bundled with that plugin for v21.1 (see §6). | ✅ |

## 5. Music & audio

Essentials plays `.ogg` (with loop points), `.mid` and `.wav`.

| Resource | What | Verdict |
|---|---|---|
| [ENLS's Pre-Looped Music Library](https://eeveeexpo.com/resources/663/) | Pre-looped `.ogg` from the mainline games (towns, routes, battles), updated Nov 2025. Credit "ENLS's Pre-Looped Music Library". | ✅ Drop into `Audio/BGM`. Some S/V links were reported as 404. |
| [Battlers OK Mon: Resource Version](https://eeveeexpo.com/resources/1252/) (EndlessBeat) | **Original** music plus battler and background art. Credit EndlessBeat. | ⚠ File format not stated. |
| Per-field battle music | EBDX can set BGM per trainer or map (`PBS/EBDX/trainers.txt` `BattleBGM`; see thread page 1). | ✅ |

## 6. Recommended plugins — EBDX compatibility

| Plugin | Version | Verdict | Notes |
|---|---|---|---|
| v21.1 Hotfixes (Maruno) | 1.0.9 | ✅ | Bundled in the base repo. |
| Generation 9 Pack (Caruban) | 3.2.5 bundled | ✅ | Bundled. |
| Pokémon World Tournament | bundled | ✅ | Bundled. Could host the post-game Battle Tower / Warden rematches. |
| [Following Pokémon EX](https://eeveeexpo.com/resources/516/) (Golisopod User; maintained by NoNonever) | 2.5.1, Jan 2026 | ✅ | Its page says EBDX Super Shinies are natively supported and `SLIDE_INTO_BATTLE` doesn't affect EBDX. Keep EBDX's `USE_FOLLOWER_EXCEPTION = true`. Start a new save after installing. |
| [Voltseon's Pause Menu](https://eeveeexpo.com/resources/692/) | 2.2 | ✅ | Out of battle. |
| [Modern Quest System + UI](https://eeveeexpo.com/resources/709/) (ThatWelshOne_) | 1.1.0 | ✅ | v21.1 badge. Out of battle. The author warns the v21 update isn't official, so expect minor bugs. Good for the story's side-quests. |
| [Bag Screen with interactable Party](https://eeveeexpo.com/resources/723/) | 2.7.5 | ✅ | Overworld bag only. |
| [Modular UI Scenes](https://eeveeexpo.com/resources/1325/) / [Enhanced Pokemon UI](https://eeveeexpo.com/resources/1387/) (Lucidious89) | 2.0.9 / 1.0.6 | ⚠ | Not DBK add-ons; they touch Summary/Party/Storage screens only. Untested with EBDX. |
| [Deluxe Battle Kit](https://eeveeexpo.com/resources/1470/) (Lucidious89) and **every DBK add-on** (Animated Pokemon System, Enhanced Battle UI, Terastallization, Dynamax, Z-Power, Raid Battles, Wonder Launcher...) | — | ❌ | The author: *"I specifically made this plugin incompatible with EBDX"* ([thread](https://eeveeexpo.com/threads/7778/page-2)). Our Field Effects plugin, EBDX's boss-battle module and its scripted battles cover the same ground. |
| ZUD (Z-Moves/Dynamax) | — | ❌ | The EBDX port's page says it never will be compatible. |
| [Open-Source EBDX Renovation Project](https://eeveeexpo.com/resources/1831/) | 4.0 | ⚠ | A replacement for our EBDX, not an add-on (see §1). |

**Built into EBDX already** (check these before writing our own):
- Boss battles (`Battle Mechanics/Boss Battles.rb` + `Boss Immunities.rb`, configured in `PBS/EBDX/rules.txt`).
  These give stat boosts, base-stat overrides and status/OHKO immunities, but **no multiple HP bars**. The
  Rejuvenation-style multi-bar bosses from SPINE rev. 2 still need custom code; the Renovation Project's 4.0
  "HP threshold" scripting is one possible base.
- Nuzlocke and Randomizer modes, scripted mid-battle dialogue (`BattleScripts`), VS intros and low-HP BGM.
