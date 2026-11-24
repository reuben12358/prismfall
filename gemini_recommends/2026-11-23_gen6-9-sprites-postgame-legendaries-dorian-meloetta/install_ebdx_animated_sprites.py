#!/usr/bin/env python3
"""Pokémon Prismfall — Gen 6–9, Regional Variants & Mega Evolutions EBDX Animated B2W2 Sprite Importer.

Sources STRICTLY genuine 2D Gen 5 B2W2-style pixel-art animated sprites (ZERO 3D XY/SM/SwSh/SV
model renders) and converts animated .gif or pre-built horizontal .png strips into Pokémon
Essentials Unofficial EBDX's exact `N*S × S` square-frame horizontal RGBA PNG strip format.

Supported strictly-2D Gen 5 B2W2 sources:
  1. Open-Source EBDX Renovation Project 4.0 (ChromeValiant — integrates Lucidious89 Animated
     Pokémon System [SPRITES], Smogon XY/SM/SwSh/SV 2D Sprite Projects, Aronousqui Megas,
     mangalos810, Spanish *Sprites Animados* / La Base de Sky, and Ghasty_001)
     https://github.com/ChromeValiant/Pokemon-Essentials-21-With-Unofficial-EBDX
  2. Ghasty001 Animated Sprites (hand-animated 2D Gen 6–9 / Hisuian / Mega B2W2 GIFs)
     https://github.com/Ghasty001/Animated_sprites_by_Ghasty001
  3. Pokémon Showdown `gen5ani*` CDN buckets ONLY (`gen5ani`, `gen5ani-back`, `gen5ani-shiny`,
     `gen5ani-back-shiny` — NEVER `ani/` 3D renders!)
     https://play.pokemonshowdown.com/sprites/gen5ani/

Usage examples:
  # 1. Read-only audit of current EBDX animation gaps across Prismfall's live roster + full Pokédex
  python3 install_ebdx_animated_sprites.py \\
      --engine /home/antigravity/pf_engine_run/base \\
      --prismfall-pbs /home/antigravity/reuben12358/prismfall/pbs \\
      --audit

  # 2. Download verified 2D open-source GitHub packs (no git required)
  python3 install_ebdx_animated_sprites.py \\
      --download-sources /home/antigravity/pf_engine_run/sprite_sources

  # 3. Install Prismfall live gaps (+ spotlight story/postgame bosses) into a standalone pack
  python3 install_ebdx_animated_sprites.py \\
      --engine /home/antigravity/pf_engine_run/base \\
      --prismfall-pbs /home/antigravity/reuben12358/prismfall/pbs \\
      --source renovation4=/home/antigravity/pf_engine_run/sprite_sources/chromevaliant_ebdx/Graphics/Pokemon \\
      --source ghasty=/home/antigravity/pf_engine_run/sprite_sources/ghasty001 \\
      --fetch-showdown-gaps \\
      --install-prismfall \\
      --out-battlers /home/antigravity/pf_engine_run/ebdx_gen6_9_animated_pack \\
      --verify-strips

  # 4. Verify an existing battlers directory or staged pack
  python3 install_ebdx_animated_sprites.py \\
      --engine /home/antigravity/pf_engine_run/base \\
      --verify-strips --verify-dir /home/antigravity/pf_engine_run/ebdx_gen6_9_animated_pack
"""

from __future__ import annotations

import argparse
import concurrent.futures
import io
import json
import os
import re
import sys
import tarfile
import time
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

from PIL import Image, ImageSequence

# ---------------------------------------------------------------------------
# Constants & Safety Allowlists
# ---------------------------------------------------------------------------

VIEWS = ("Front", "Back", "FrontShiny", "BackShiny")

# Hardcoded strictly-2D Showdown buckets. NEVER add `ani/`, `ani-back/`, etc. (3D models!).
SHOWDOWN_2D_BUCKETS = {
    "Front": "https://play.pokemonshowdown.com/sprites/gen5ani",
    "Back": "https://play.pokemonshowdown.com/sprites/gen5ani-back",
    "FrontShiny": "https://play.pokemonshowdown.com/sprites/gen5ani-shiny",
    "BackShiny": "https://play.pokemonshowdown.com/sprites/gen5ani-back-shiny",
}

GITHUB_TARBALLS = {
    "chromevaliant_ebdx": (
        "https://github.com/ChromeValiant/Pokemon-Essentials-21-With-Unofficial-EBDX/archive/refs/heads/main.tar.gz",
        (
            "README",
            "Graphics/Pokemon/Front/",
            "Graphics/Pokemon/Back/",
            "Graphics/Pokemon/Front shiny/",
            "Graphics/Pokemon/Back shiny/",
            "PBS/pokemon_forms",
        ),
    ),
    "ghasty001": (
        "https://github.com/Ghasty001/Animated_sprites_by_Ghasty001/archive/refs/heads/main.tar.gz",
        None,
    ),
}

# Prismfall Part A / B / C spotlight story & postgame boss species/forms
# (ensures Gym 1 Dorian, Ch10/Ch18/Act V Ogerpon + Loyal Three + Pecharunt,
# Ch11/Ch14/PG Primals, and Postgame Tier 1–3 Legendaries are ALWAYS animated).
SPOTLIGHT_BOSS_FORMS: Set[Tuple[str, int]] = {
    ("ZORUA", 1), ("ZOROARK", 1),
    ("MELOETTA", 0), ("MELOETTA", 1),
    ("OGERPON", 0), ("OGERPON", 1), ("OGERPON", 2), ("OGERPON", 3),
    ("OKIDOGI", 0), ("MUNKIDORI", 0), ("FEZANDIPITI", 0),
    ("PECHARUNT", 0),
    ("GHOLDENGO", 0), ("ANNIHILAPE", 0),
    ("KYOGRE", 1), ("GROUDON", 1),
    ("TYPENULL", 0), ("SILVALLY", 0),
    ("KUBFU", 0), ("URSHIFU", 0), ("URSHIFU", 1),
    ("REGIELEKI", 0), ("REGIDRAGO", 0),
    ("ZYGARDE", 2),
    ("TERAPAGOS", 0), ("TERAPAGOS", 1), ("TERAPAGOS", 2),
}

# Strict 2D Gen 5 B2W2 pixel-art verification thresholds
MAX_2D_UNIQUE_RGB = 180          # Gen 5 sprites are ~15-32 colors; complex crystals (Glimmora/Mega Sableye) reach ~129
MAX_PRE_CLEAN_SEMI_RATIO = 0.05  # >5% semi-transparent pixels => anti-aliased 3D render / soft art -> REJECT
MAX_1X_FRAME_SIZE = 192          # Largest stock B2W2 strip is Lugia (154px); allows wide 1x wingspans like Noivern (182px)
MIN_1X_FRAME_SIZE = 16
MAX_GIF_FRAMES = 200

# Stock EBDX form-ID bugs: stock Front/658_1.png mistakenly stores Ash-Greninja (which is GRENINJA_2 in v21.1 PBS),
# whereas GRENINJA_1 is pre-transform Battle Bond Greninja (visually identical to base GRENINJA).
STOCK_MISSLOTTED_FORM_ALIASES: Dict[Tuple[str, int], Tuple[str, int]] = {
    ("GRENINJA", 1): ("GRENINJA", 0),
}

# Ghasty001 filename aliases -> canonical Essentials (SPECIES, form) key
GHASTY_ALIASES = {
    "ABSOL_MEGA": "ABSOL_1",
    "ALTARIA_MEGA": "ALTARIA_1",
    "AMPHAROS_MEGA": "AMPHAROS_1",
    "BEEDRILL_MEGA": "BEEDRILL_1",
    "BRAVIARY": "BRAVIARY_1",      # Ghasty001's Braviary is Hisuian Braviary (per README)
    "SNEASEL-M": "SNEASEL_1",      # Hisuian Sneasel male
    "SNEASEL-F": "SNEASEL_1",      # Hisuian Sneasel female
}

# Source directory subfolder naming conventions
SOURCE_SUBDIR_CANDIDATES = {
    "Front": ("Front", "FRONT"),
    "Back": ("Back", "BACK"),
    "FrontShiny": ("FrontShiny", "Front shiny", "FRONT_SHINY", "Front_Shiny"),
    "BackShiny": ("BackShiny", "Back shiny", "BACK_SHINY", "Back_Shiny"),
}


# ---------------------------------------------------------------------------
# Data Structures
# ---------------------------------------------------------------------------

@dataclass
class FormEntry:
    species: str
    form: int
    dex: int
    form_name: str = ""
    mega_stone: str = ""
    mega_move: str = ""
    category: str = "Base"  # Base, Mega, Primal, Alolan, Galarian, Hisuian, Paldean, Other

    @property
    def key(self) -> Tuple[str, int]:
        return (self.species, self.form)

    @property
    def sym_name(self) -> str:
        return f"{self.species}_{self.form}" if self.form > 0 else self.species

    @property
    def ebdx_stem(self) -> str:
        return f"{self.dex:03d}_{self.form}" if self.form > 0 else f"{self.dex:03d}"

    @property
    def generation(self) -> int:
        if self.dex <= 151:
            return 1
        if self.dex <= 251:
            return 2
        if self.dex <= 386:
            return 3
        if self.dex <= 493:
            return 4
        if self.dex <= 649:
            return 5
        if self.dex <= 721:
            return 6
        if self.dex <= 809:
            return 7
        if self.dex <= 905:
            return 8
        return 9


@dataclass
class PBSIndex:
    species_order: List[str]
    species_to_dex: Dict[str, int]
    dex_to_species: Dict[int, str]
    entries: Dict[Tuple[str, int], FormEntry]
    mega_stone_map: Dict[Tuple[str, str], Tuple[str, int]]


@dataclass
class RosterSlices:
    trainers: Set[Tuple[str, int]] = field(default_factory=set)
    trainer_megas: Set[Tuple[str, int]] = field(default_factory=set)
    encounters: Set[Tuple[str, int]] = field(default_factory=set)
    live_795: Set[Tuple[str, int]] = field(default_factory=set)
    live_796: Set[Tuple[str, int]] = field(default_factory=set)       # + Dorian Gym 1 Hisuian Zorua
    live_spotlight: Set[Tuple[str, int]] = field(default_factory=set)  # + Story/Postgame Bosses


@dataclass
class ConversionResult:
    species: str
    form: int
    dex: int
    view: str
    ebdx_filename: str
    source_name: str
    source_path: str
    frame_size: int
    frame_count: int
    unique_frames: int
    unique_rgb: int
    was_downscaled_2x: bool
    output_bytes: int
    female: bool = False


# ---------------------------------------------------------------------------
# PBS & Live Roster Parsing
# ---------------------------------------------------------------------------

def classify_form(form: int, form_name: str, mega_stone: str, mega_move: str) -> str:
    if form == 0:
        return "Base"
    fn = form_name.lower()
    if "primal" in fn:
        return "Primal"
    if mega_stone or mega_move or "mega" in fn:
        return "Mega"
    if "alolan" in fn:
        return "Alolan"
    if "galarian" in fn:
        return "Galarian"
    if "hisuian" in fn:
        return "Hisuian"
    if "paldean" in fn:
        return "Paldean"
    return "Other"


def load_pbs_index(engine_dir: Path) -> PBSIndex:
    pbs_dir = engine_dir / "PBS"
    pokemon_txt = pbs_dir / "pokemon.txt"
    forms_txt = pbs_dir / "pokemon_forms.txt"
    if not pokemon_txt.exists():
        raise FileNotFoundError(f"Missing PBS/pokemon.txt under {engine_dir}")

    species_order: List[str] = []
    species_to_dex: Dict[str, int] = {}
    dex_to_species: Dict[int, str] = {}
    entries: Dict[Tuple[str, int], FormEntry] = {}

    with pokemon_txt.open(encoding="utf-8-sig") as f:
        for line in f:
            # Must allow lowercase letters (e.g. NIDORANfE, NIDORANmA)
            m = re.match(r"^\[([A-Za-z0-9_]+)\]\s*$", line.strip())
            if m:
                sp = m.group(1)
                dex = len(species_order) + 1
                species_order.append(sp)
                species_to_dex[sp] = dex
                dex_to_species[dex] = sp
                entries[(sp, 0)] = FormEntry(species=sp, form=0, dex=dex, category="Base")

    mega_stone_map: Dict[Tuple[str, str], Tuple[str, int]] = {}
    if forms_txt.exists():
        cur_key: Optional[Tuple[str, int]] = None
        cur_data: Dict[str, str] = {}

        def flush():
            if cur_key is None:
                return
            sp, fm = cur_key
            if sp not in species_to_dex:
                return
            fn = cur_data.get("FormName", "")
            ms = cur_data.get("MegaStone", "")
            mm = cur_data.get("MegaMove", "")
            cat = classify_form(fm, fn, ms, mm)
            entries[(sp, fm)] = FormEntry(
                species=sp,
                form=fm,
                dex=species_to_dex[sp],
                form_name=fn,
                mega_stone=ms,
                mega_move=mm,
                category=cat,
            )
            if ms:
                mega_stone_map[(sp, ms)] = (sp, fm)

        with forms_txt.open(encoding="utf-8-sig") as f:
            for line in f:
                s = line.strip()
                m = re.match(r"^\[([A-Za-z0-9_]+)[,\s]+(\d+)\]\s*$", s)
                if m:
                    flush()
                    cur_key = (m.group(1), int(m.group(2)))
                    cur_data = {}
                elif cur_key and "=" in s:
                    k, v = [x.strip() for x in s.split("=", 1)]
                    if k in ("FormName", "MegaStone", "MegaMove"):
                        cur_data[k] = v
        flush()

    return PBSIndex(
        species_order=species_order,
        species_to_dex=species_to_dex,
        dex_to_species=dex_to_species,
        entries=entries,
        mega_stone_map=mega_stone_map,
    )


def load_prismfall_roster(pbs_index: PBSIndex, prismfall_pbs_dir: Path) -> RosterSlices:
    slices = RosterSlices()
    if not prismfall_pbs_dir or not prismfall_pbs_dir.exists():
        return slices

    for fname in ("trainers.txt", "trainers_trials.txt"):
        p = prismfall_pbs_dir / fname
        if not p.exists():
            continue
        cur_sp: Optional[str] = None
        cur_fm = 0
        with p.open(encoding="utf-8-sig") as f:
            for line in f:
                s = line.strip()
                if s.startswith("Pokemon ="):
                    if cur_sp and cur_sp in pbs_index.species_to_dex:
                        slices.trainers.add((cur_sp, cur_fm))
                    cur_sp = s.split("=", 1)[1].split(",")[0].strip()
                    cur_fm = 0
                elif s.startswith("Form =") and cur_sp:
                    try:
                        cur_fm = int(s.split("=", 1)[1].strip())
                    except ValueError:
                        cur_fm = 0
                elif s.startswith("Item =") and cur_sp:
                    item = s.split("=", 1)[1].strip()
                    if (cur_sp, item) in pbs_index.mega_stone_map:
                        slices.trainer_megas.add(pbs_index.mega_stone_map[(cur_sp, item)])
                elif s.startswith("[") and cur_sp:
                    if cur_sp in pbs_index.species_to_dex:
                        slices.trainers.add((cur_sp, cur_fm))
                    cur_sp = None
                    cur_fm = 0
            if cur_sp and cur_sp in pbs_index.species_to_dex:
                slices.trainers.add((cur_sp, cur_fm))

    for fname in ("encounters.txt", "encounters_badgetiers.txt"):
        p = prismfall_pbs_dir / fname
        if not p.exists():
            continue
        with p.open(encoding="utf-8-sig") as f:
            for line in f:
                s = line.strip()
                if not s or s.startswith("#") or s.startswith("[") or "," not in s:
                    continue
                parts = [x.strip() for x in s.split(",")]
                if parts[0].isdigit() and len(parts) >= 3:
                    raw = parts[1]
                    if "_" in raw and raw.rsplit("_", 1)[1].isdigit():
                        sp, fm_s = raw.rsplit("_", 1)
                        fm = int(fm_s)
                    else:
                        sp, fm = raw, 0
                    if sp in pbs_index.species_to_dex:
                        slices.encounters.add((sp, fm))

    slices.live_795 = slices.trainers | slices.trainer_megas | slices.encounters
    slices.live_796 = slices.live_795 | {("ZORUA", 1)}
    valid_spotlight = {k for k in SPOTLIGHT_BOSS_FORMS if k in pbs_index.entries}
    slices.live_spotlight = slices.live_796 | valid_spotlight
    return slices


# ---------------------------------------------------------------------------
# Showdown `gen5ani` Slug Mapper (Strictly 2D!)
# ---------------------------------------------------------------------------

SHOWDOWN_SPECIES_OVERRIDES = {
    "NIDORANfE": "nidoranf",
    "NIDORANmA": "nidoranm",
    "FARFETCHD": "farfetchd",
    "MRMIME": "mrmime",
    "MRRIME": "mrrime",
    "MIMEJR": "mimejr",
    "HOOH": "hooh",
    "PORYGONZ": "porygonz",
    "FLABEBE": "flabebe",
    "TYPENULL": "typenull",
    "JANGMOO": "jangmoo",
    "HAKAMOO": "hakamoo",
    "KOMMOO": "kommoo",
    "TAPUKOKO": "tapukoko",
    "TAPULELE": "tapulele",
    "TAPUBULU": "tapubulu",
    "TAPUFINI": "tapufini",
    "SIRFETCHD": "sirfetchd",
    "GREATTUSK": "greattusk",
    "SCREAMTAIL": "screamtail",
    "BRUTEBONNET": "brutebonnet",
    "FLUTTERMANE": "fluttermane",
    "SLITHERWING": "slitherwing",
    "SANDYSHOCKS": "sandyshocks",
    "IRONTREADS": "irontreads",
    "IRONBUNDLE": "ironbundle",
    "IRONHANDS": "ironhands",
    "IRONJUGULIS": "ironjugulis",
    "IRONMOTH": "ironmoth",
    "IRONTHORNS": "ironthorns",
    "ROARINGMOON": "roaringmoon",
    "IRONVALIANT": "ironvaliant",
    "WALKINGWAKE": "walkingwake",
    "IRONLEAVES": "ironleaves",
    "GOUGINGFIRE": "gougingfire",
    "RAGINGBOLT": "ragingbolt",
    "IRONBOULDER": "ironboulder",
    "IRONCROWN": "ironcrown",
    "WOCHIEN": "wochien",
    "CHIENPAO": "chienpao",
    "TINGLU": "tinglu",
    "CHIYU": "chiyu",
}


def to_showdown_slug(entry: FormEntry) -> Optional[str]:
    base = SHOWDOWN_SPECIES_OVERRIDES.get(entry.species, entry.species.lower())
    if entry.form == 0:
        return base
    fn = entry.form_name.lower()
    if entry.category == "Alolan":
        return f"{base}-alola"
    if entry.category == "Galarian":
        if entry.species == "DARMANITAN" and "zen" in fn:
            return "darmanitan-galarzen"
        return f"{base}-galar"
    if entry.category == "Hisuian":
        return f"{base}-hisui"
    if entry.category == "Paldean":
        if entry.species == "TAUROS":
            if "blaze" in fn:
                return "tauros-paldeablaze"
            if "aqua" in fn:
                return "tauros-paldeaaqua"
            return "tauros-paldeacombat"
        return f"{base}-paldea"
    if entry.category == "Primal":
        return f"{base}-primal"
    if entry.category == "Mega":
        if fn.endswith(" x"):
            return f"{base}-megax"
        if fn.endswith(" y"):
            return f"{base}-megay"
        return f"{base}-mega"
    if entry.species == "OGERPON":
        mask_map = {1: "wellspring", 2: "hearthflame", 3: "cornerstone"}
        if entry.form in mask_map:
            return f"ogerpon-{mask_map[entry.form]}"
    if entry.species == "MELOETTA" and entry.form == 1:
        return "meloetta-pirouette"
    if entry.species == "ORICORIO":
        omap = {1: "pompom", 2: "pau", 3: "sensu"}
        if entry.form in omap:
            return f"oricorio-{omap[entry.form]}"
    if entry.species == "URSHIFU" and entry.form == 1:
        return "urshifu-rapidstrike"
    if entry.species == "ZYGARDE":
        zmap = {1: "10", 2: "complete", 3: "complete"}
        if entry.form in zmap:
            return f"zygarde-{zmap[entry.form]}"
    if entry.species == "TERAPAGOS":
        tmap = {1: "terastal", 2: "stellar"}
        if entry.form in tmap:
            return f"terapagos-{tmap[entry.form]}"
    if entry.species == "ZACIAN" and entry.form == 1:
        return "zacian-crowned"
    if entry.species == "ZAMAZENTA" and entry.form == 1:
        return "zamazenta-crowned"
    if entry.species == "CALYREX":
        return {1: "calyrex-ice", 2: "calyrex-shadow"}.get(entry.form)
    if entry.species == "NECROZMA":
        return {1: "necrozma-duskmane", 2: "necrozma-dawnwings", 3: "necrozma-ultra", 4: "necrozma-ultra"}.get(entry.form)
    if entry.species == "LYCANROC":
        return {1: "lycanroc-midnight", 2: "lycanroc-dusk"}.get(entry.form)
    if entry.species == "MIMIKYU" and entry.form == 1:
        return "mimikyu-busted"
    if entry.species == "WISHIWASHI" and entry.form == 1:
        return "wishiwashi-school"
    if entry.species == "EISCUE" and entry.form == 1:
        return "eiscue-noice"
    if entry.species == "MORPEKO" and entry.form == 1:
        return "morpeko-hangry"
    if entry.species == "TATSUGIRI":
        return {1: "tatsugiri-droopy", 2: "tatsugiri-stretchy"}.get(entry.form)
    if entry.species == "URSALUNA" and entry.form == 1:
        return "ursaluna-bloodmoon"
    if entry.species == "MAUSHOLD" and entry.form == 1:
        return "maushold-four"
    if entry.species == "AEGISLASH" and entry.form == 1:
        return "aegislash-blade"
    if entry.species == "HOOPA" and entry.form == 1:
        return "hoopa-unbound"
    if entry.species == "MAGEARNA" and entry.form == 1:
        return "magearna-original"
    if entry.species == "BASCULIN":
        return {1: "basculin-bluestriped", 2: "basculin-whitestriped"}.get(entry.form)
    if entry.species == "TOXTRICITY" and entry.form == 1:
        return "toxtricity-lowkey"
    if entry.species == "PALAFIN" and entry.form == 1:
        return "palafin-hero"
    if entry.species == "MINIOR":
        return {
            7: "minior-red", 8: "minior-orange", 9: "minior-yellow", 10: "minior-green",
            11: "minior-blue", 12: "minior-indigo", 13: "minior-violet",
        }.get(entry.form)
    if entry.species == "SILVALLY" and fn.startswith("type: "):
        t = fn.replace("type: ", "").strip()
        return f"silvally-{t}" if t and t != "unknown" else None
    if entry.species == "ARCEUS" and fn.startswith("type: "):
        t = fn.replace("type: ", "").strip()
        return f"arceus-{t}" if t and t != "unknown" else None
    if entry.species == "FLABEBE" and fn:
        return f"flabebe-{fn.split()[0]}"
    if entry.species == "VIVILLON" and fn:
        return f"vivillon-{fn.replace(' pattern', '').replace(' ', '').replace('-', '')}"
    if entry.species == "ALCREMIE" and fn:
        return f"alcremie-{fn.replace(' ', '')}"
    if entry.species == "DARMANITAN" and "zen" in fn:
        return "darmanitan-zen"
    if entry.species == "KELDEO" and entry.form == 1:
        return "keldeo-resolute"
    if entry.species == "KYUREM":
        return {1: "kyurem-white", 2: "kyurem-black"}.get(entry.form)
    if entry.species == "SHAYMIN" and entry.form == 1:
        return "shaymin-sky"
    if entry.species == "DEOXYS":
        return {1: "deoxys-attack", 2: "deoxys-defense", 3: "deoxys-speed"}.get(entry.form)
    if entry.species == "ROTOM":
        return {1: "rotom-heat", 2: "rotom-wash", 3: "rotom-frost", 4: "rotom-fan", 5: "rotom-mow"}.get(entry.form)
    if entry.species == "CASTFORM":
        return {1: "castform-sunny", 2: "castform-rainy", 3: "castform-snowy"}.get(entry.form)
    if "origin" in fn:
        return f"{base}-origin"
    if "therian" in fn:
        return f"{base}-therian"
    return None


# ---------------------------------------------------------------------------
# EBDX Battlers Lookup & Inspection
# ---------------------------------------------------------------------------

def is_animated_strip_fast(path: Optional[Path]) -> Tuple[bool, Tuple[int, int]]:
    if not path or not path.exists():
        return False, (0, 0)
    try:
        with Image.open(path) as im:
            w, h = im.size
        return (h > 0 and w > h and w % h == 0), (w, h)
    except Exception:
        return False, (0, 0)


def resolve_ebdx_battler(battlers_dirs: Sequence[Path], view: str, entry: FormEntry) -> Optional[Path]:
    """Check numeric (%03d[_form]) then symbolic (SPECIES[_form]) across ordered battlers dirs."""
    candidates = [entry.ebdx_stem, entry.sym_name]
    for bdir in battlers_dirs:
        vdir = bdir / view
        if not vdir.exists():
            continue
        for stem in candidates:
            for ext in (".png", ".PNG"):
                p = vdir / f"{stem}{ext}"
                if p.exists():
                    return p
    return None


# ---------------------------------------------------------------------------
# Pixel-Art Verification, 2x Scale Guard & EBDX Strip Conversion Engine
# ---------------------------------------------------------------------------

def _is_uniform_2x_upscaled(frame: Image.Image) -> bool:
    """Detect exact 2× pixel-grid upscaling (e.g. 192×192 sheets where every pixel is 2×2)."""
    w, h = frame.size
    if h < 140 or w % 2 != 0 or h % 2 != 0:
        return False
    px = frame.load()
    total = 0
    mism = 0
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            p00 = px[x, y]
            p10 = px[x + 1, y]
            p01 = px[x, y + 1]
            p11 = px[x + 1, y + 1]
            if p00[3] or p10[3] or p01[3] or p11[3]:
                total += 1
                if not (p00 == p10 == p01 == p11):
                    mism += 1
    return total > 0 and (mism / total) < 0.02


def _clean_alpha_and_measure_2d(frames: List[Image.Image]) -> Tuple[List[Image.Image], int, float]:
    """Validate 2D pixel-art palette/alpha on sampled frames and binarize alpha to {0, 255}."""
    sample_indices = sorted({0, len(frames) // 2, len(frames) - 1})
    max_semi_ratio = 0.0
    rgb_set: Set[Tuple[int, int, int]] = set()

    for idx in sample_indices:
        raw = frames[idx].get_flattened_data()
        non_t = 0
        semi = 0
        for r, g, b, a in raw:
            if a > 0:
                non_t += 1
                if a < 255:
                    semi += 1
                if a >= 128:
                    rgb_set.add((r, g, b))
        if non_t > 0:
            max_semi_ratio = max(max_semi_ratio, semi / non_t)

    if max_semi_ratio > MAX_PRE_CLEAN_SEMI_RATIO:
        raise ValueError(
            f"Rejected non-2D/anti-aliased sprite: semi-transparent pixel ratio={max_semi_ratio:.3f} > {MAX_PRE_CLEAN_SEMI_RATIO}"
        )
    if len(rgb_set) > MAX_2D_UNIQUE_RGB:
        raise ValueError(
            f"Rejected non-2D/3D-rendered sprite: unique RGB colors={len(rgb_set)} > {MAX_2D_UNIQUE_RGB}"
        )

    # Binarize alpha cleanly (zero semi-transparent halo!) and clear RGB on fully transparent pixels
    cleaned: List[Image.Image] = []
    for f in frames:
        r, g, b, a = f.split()
        # Lookup table: <128 -> 0, >=128 -> 255
        a_bin = a.point(lambda v: 255 if v >= 128 else 0)
        out = Image.new("RGBA", f.size, (0, 0, 0, 0))
        out.paste(Image.merge("RGBA", (r, g, b, a_bin)), (0, 0), a_bin)
        cleaned.append(out)
    return cleaned, len(rgb_set), max_semi_ratio


def extract_frames_from_gif(data_or_path: Path | bytes) -> List[Image.Image]:
    """Decode animated GIF respecting disposal methods and normalizing variable frame holds."""
    im = Image.open(io.BytesIO(data_or_path)) if isinstance(data_or_path, bytes) else Image.open(data_or_path)
    try:
        raw_frames: List[Image.Image] = []
        durations: List[int] = []
        for frame in ImageSequence.Iterator(im):
            dur = int(frame.info.get("duration", 100) or 100)
            durations.append(dur)
            raw_frames.append(frame.convert("RGBA"))
    finally:
        im.close()

    if len(raw_frames) < 2:
        raise ValueError(f"GIF is not animated (only {len(raw_frames)} frame)")

    # Normalize variable frame durations relative to shortest positive delay (uniform 100ms stays 1x!)
    pos_durs = [d for d in durations if d > 0]
    base_dur = min(pos_durs) if pos_durs else 100
    expanded: List[Image.Image] = []
    for fr, dur in zip(raw_frames, durations):
        rep = max(1, min(4, int(round(dur / base_dur)))) if base_dur > 0 else 1
        for _ in range(rep):
            expanded.append(fr)
            if len(expanded) >= MAX_GIF_FRAMES:
                break
        if len(expanded) >= MAX_GIF_FRAMES:
            break
    return expanded


def extract_frames_from_png_strip(path: Path) -> List[Image.Image]:
    """Slice a horizontal `N*H × H` PNG strip into N square RGBA frames."""
    with Image.open(path) as im:
        w, h = im.size
        if h <= 0 or w <= h or w % h != 0:
            raise ValueError(f"Not a valid horizontal square-frame strip: {w}x{h}")
        rgba = im.convert("RGBA")
        n = w // h
        return [rgba.crop((i * h, 0, (i + 1) * h, h)) for i in range(n)]


def count_unique_frames(frames: Sequence[Image.Image]) -> int:
    return len({f.tobytes() for f in frames})


def build_ebdx_strip(
    frames: List[Image.Image],
    min_frame_size: int = 0,
    keep_union_square: bool = True,
) -> Tuple[Image.Image, int, int, int, int, bool]:
    """Convert RGBA frames into a verified, drift-free EBDX `N*S × S` horizontal RGBA PNG strip.

    Returns: (strip_image, frame_size_S, frame_count_N, unique_frames, unique_rgb, was_downscaled_2x)
    """
    if len(frames) < 2:
        raise ValueError(f"Too few frames: {len(frames)}")

    # 1. Verify frames aren't all identical (fake animation guard)
    b0 = frames[0].tobytes()
    if all(f.tobytes() == b0 for f in frames[1:]):
        raise ValueError("Rejected fake animation: all frames are byte-identical")

    # 2. Strict 2D pixel-art check & halo removal
    cleaned, uniq_rgb, _ = _clean_alpha_and_measure_2d(frames)
    uniq_frames = count_unique_frames(cleaned)
    if uniq_frames < 2:
        raise ValueError("Rejected fake animation: all cleaned frames are identical")

    # 3. Auto-downscale exact 2× pre-upscaled pixel art back to native 1× Gen 5 resolution
    was_2x = False
    if _is_uniform_2x_upscaled(cleaned[0]):
        w, h = cleaned[0].size
        cleaned = [f.resize((w // 2, h // 2), Image.Resampling.NEAREST) for f in cleaned]
        was_2x = True

    # 4. Compute exact UNION opaque bounding box across ALL frames (ZERO frame drift!)
    fw, fh = cleaned[0].size
    ux0, uy0, ux1, uy1 = fw, fh, 0, 0
    for f in cleaned:
        bb = f.getbbox()
        if bb:
            ux0 = min(ux0, bb[0])
            uy0 = min(uy0, bb[1])
            ux1 = max(ux1, bb[2])
            uy1 = max(uy1, bb[3])
    if ux1 <= ux0 or uy1 <= uy0:
        raise ValueError("Empty transparent sprite across all frames")

    uw = ux1 - ux0
    uh = uy1 - uy0
    if keep_union_square:
        cell = max(uw, uh, min_frame_size)
    else:
        cell = max(fw, fh, min_frame_size)

    if cell < MIN_1X_FRAME_SIZE or cell > MAX_1X_FRAME_SIZE:
        raise ValueError(f"Frame size {cell}px outside valid 1× Gen 5 bounds [{MIN_1X_FRAME_SIZE}, {MAX_1X_FRAME_SIZE}]")

    # 5. Assemble horizontal strip (N * cell) × cell, centering union bbox uniformly on EVERY frame
    n = len(cleaned)
    strip = Image.new("RGBA", (n * cell, cell), (0, 0, 0, 0))
    dx = (cell - uw) // 2
    dy = (cell - uh) // 2
    for i, f in enumerate(cleaned):
        crop = f.crop((ux0, uy0, ux1, uy1))
        strip.paste(crop, (i * cell + dx, dy))

    return strip, cell, n, uniq_frames, uniq_rgb, was_2x


# ---------------------------------------------------------------------------
# Multi-Source Indexing & Resolution
# ---------------------------------------------------------------------------

class LocalSpriteSource:
    """Indexes a local PNG-strip or animated-GIF sprite repository."""

    def __init__(self, name: str, root: Path):
        self.name = name
        self.root = root
        self.index: Dict[str, Dict[str, Path]] = {v: {} for v in VIEWS}
        self.female_index: Dict[str, Dict[str, Path]] = {v: {} for v in VIEWS}
        self._scan()

    def _canonical_stem(self, raw_stem: str) -> Tuple[str, bool]:
        s = raw_stem.strip()
        low = s.lower()
        # Strip Ghasty001 trailing labels like " back shiny", " back", " shiny"
        for suffix in (" back shiny", " shiny back", " back", " shiny"):
            if low.endswith(suffix):
                s = s[: -len(suffix)].strip()
                low = s.lower()
        is_female = False
        if low.endswith("_female"):
            is_female = True
            s = s[:-7]
        elif low.endswith("-f"):
            is_female = True
        up = s.upper()
        up = GHASTY_ALIASES.get(up, up)
        return up, is_female

    def _scan(self) -> None:
        if not self.root.exists():
            raise FileNotFoundError(f"Source directory not found: {self.root}")
        for view, candidates in SOURCE_SUBDIR_CANDIDATES.items():
            sub_dir = None
            for cand in candidates:
                d = self.root / cand
                if d.is_dir():
                    sub_dir = d
                    break
            if sub_dir is None:
                continue
            for p in sorted(sub_dir.iterdir()):
                if not p.is_file():
                    continue
                ext = p.suffix.lower()
                if ext not in (".png", ".gif"):
                    continue
                key, is_female = self._canonical_stem(p.stem)
                if is_female:
                    self.female_index[view].setdefault(key, p)
                    # Also allow SNEASEL-f to populate SNEASEL_1 if SNEASEL-m not present
                    if key == "SNEASEL_1":
                        self.index[view].setdefault(key, p)
                else:
                    # Prefer animated PNG/GIF over static
                    if key not in self.index[view]:
                        self.index[view][key] = p

    def lookup(self, view: str, entry: FormEntry, female: bool = False) -> Optional[Path]:
        table = self.female_index[view] if female else self.index[view]
        for key in (entry.sym_name.upper(), entry.ebdx_stem.upper()):
            if key in table:
                return table[key]
        return None


class ShowdownGen5AniSource:
    """Fetches ONLY strictly-2D Gen 5 animated GIFs from play.pokemonshowdown.com/sprites/gen5ani*."""

    def __init__(self, cache_dir: Optional[Path] = None):
        self.cache_dir = cache_dir
        self._dir_indices: Dict[str, Set[str]] = {}

    def _ensure_index(self, view: str) -> Set[str]:
        if view in self._dir_indices:
            return self._dir_indices[view]
        bucket_url = SHOWDOWN_2D_BUCKETS[view]
        cache_file = self.cache_dir / f"showdown_{bucket_url.rsplit('/', 1)[-1]}.txt" if self.cache_dir else None
        names: Set[str] = set()
        if cache_file and cache_file.exists():
            names = {line.strip().lstrip("./") for line in cache_file.read_text(encoding="utf-8").splitlines() if line.strip()}
        else:
            req = urllib.request.Request(bucket_url + "/", headers={"User-Agent": "PrismfallSpritePipeline/1.0"})
            with urllib.request.urlopen(req, timeout=20) as resp:
                html_text = resp.read().decode("utf-8", errors="ignore")
            names = {m.lstrip("./") for m in re.findall(r'href="([^"]+\.gif)"', html_text)}
            if cache_file:
                cache_file.parent.mkdir(parents=True, exist_ok=True)
                cache_file.write_text("\n".join(sorted(names)) + "\n", encoding="utf-8")
        self._dir_indices[view] = names
        return names

    def fetch_gif(self, view: str, entry: FormEntry) -> Optional[Tuple[bytes, str]]:
        slug = to_showdown_slug(entry)
        if not slug:
            return None
        fname = f"{slug}.gif"
        if fname not in self._ensure_index(view):
            return None
        url = f"{SHOWDOWN_2D_BUCKETS[view]}/{fname}"
        if self.cache_dir:
            local = self.cache_dir / "showdown_gifs" / view / fname
            if local.exists():
                return local.read_bytes(), url
        req = urllib.request.Request(url, headers={"User-Agent": "PrismfallSpritePipeline/1.0"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = resp.read()
        if self.cache_dir:
            local = self.cache_dir / "showdown_gifs" / view / fname
            local.parent.mkdir(parents=True, exist_ok=True)
            local.write_bytes(data)
        return data, url


# ---------------------------------------------------------------------------
# Source Downloader (No `git` Needed!)
# ---------------------------------------------------------------------------

def download_sources(dest_root: Path) -> None:
    dest_root.mkdir(parents=True, exist_ok=True)
    for name, (url, prefixes) in GITHUB_TARBALLS.items():
        target = dest_root / name
        if target.exists() and any(target.iterdir()):
            print(f"[download] {name} already present at {target}, skipping.")
            continue
        print(f"[download] Fetching {name} from {url} ...")
        target.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(url, headers={"User-Agent": "PrismfallSpritePipeline/1.0"})
        with urllib.request.urlopen(req, timeout=180) as resp:
            with tarfile.open(fileobj=resp, mode="r|gz") as tf:
                count = 0
                for member in tf:
                    if not member.isfile():
                        continue
                    parts = Path(member.name).parts
                    if len(parts) < 2:
                        continue
                    rel = Path(*parts[1:])
                    rel_posix = rel.as_posix()
                    if prefixes is not None and not any(rel_posix.startswith(pf) for pf in prefixes):
                        continue
                    out_path = target / rel
                    out_path.parent.mkdir(parents=True, exist_ok=True)
                    src_f = tf.extractfile(member)
                    if src_f is not None:
                        out_path.write_bytes(src_f.read())
                        count += 1
        print(f"[download] Extracted {count} files into {target}")


# ---------------------------------------------------------------------------
# Audit Engine
# ---------------------------------------------------------------------------

def audit_battlers(
    pbs: PBSIndex,
    roster: RosterSlices,
    battlers_dirs: Sequence[Path],
) -> Dict[str, object]:
    """Audit EBDX animation coverage across live Prismfall roster, spotlight bosses, and full Pokédex."""

    def count_slice(keys: Iterable[Tuple[str, int]]) -> Dict[str, object]:
        key_list = sorted(set(keys))
        res: Dict[str, object] = {"total": len(key_list)}
        for v in VIEWS:
            anim = 0
            gaps: List[str] = []
            for k in key_list:
                entry = pbs.entries.get(k)
                if not entry:
                    continue
                p = resolve_ebdx_battler(battlers_dirs, v, entry)
                ok, _ = is_animated_strip_fast(p)
                if ok:
                    anim += 1
                else:
                    gaps.append(entry.sym_name)
            res[v] = {"animated": anim, "gaps": len(gaps), "missing_list": gaps}
        return res

    # Category buckets across full Pokédex (1,420 entries)
    by_category: Dict[str, List[Tuple[str, int]]] = {
        "Gen 1-5 Base (#001-#649)": [],
        "Gen 6 Base (#650-#721)": [],
        "Gen 7 Base (#722-#809)": [],
        "Gen 8 Base (#810-#905)": [],
        "Gen 9 Base (#906-#1025)": [],
        "Alolan Forms": [],
        "Galarian Forms": [],
        "Hisuian Forms": [],
        "Paldean Forms": [],
        "Primal Reversions": [],
        "Mega Evolutions (All 48)": [],
        "Other Alt Forms": [],
    }
    for k, e in pbs.entries.items():
        if e.form == 0:
            if e.generation <= 5:
                by_category["Gen 1-5 Base (#001-#649)"].append(k)
            else:
                by_category[f"Gen {e.generation} Base (#{ {6:'650-#721',7:'722-#809',8:'810-#905',9:'906-#1025'}[e.generation] })"].append(k)
        elif e.category == "Alolan":
            by_category["Alolan Forms"].append(k)
        elif e.category == "Galarian":
            by_category["Galarian Forms"].append(k)
        elif e.category == "Hisuian":
            by_category["Hisuian Forms"].append(k)
        elif e.category == "Paldean":
            by_category["Paldean Forms"].append(k)
        elif e.category == "Primal":
            by_category["Primal Reversions"].append(k)
        elif e.category == "Mega":
            by_category["Mega Evolutions (All 48)"].append(k)
        else:
            by_category["Other Alt Forms"].append(k)

    # Also slice Prismfall Live 796 + Spotlight 819 by category!
    live_by_cat: Dict[str, List[Tuple[str, int]]] = defaultdict(list)
    for k in sorted(roster.live_spotlight):
        e = pbs.entries[k]
        if e.form == 0:
            label = "Gen 1-5 Base" if e.generation <= 5 else f"Gen {e.generation} Base"
        else:
            label = e.category
        live_by_cat[label].append(k)

    spotlight_detail = []
    spotlight_order = [
        ("ZORUA", 1), ("ZOROARK", 1), ("MELOETTA", 0), ("MELOETTA", 1),
        ("OGERPON", 0), ("OGERPON", 1), ("OGERPON", 2), ("OGERPON", 3),
        ("OKIDOGI", 0), ("MUNKIDORI", 0), ("FEZANDIPITI", 0), ("PECHARUNT", 0),
        ("GHOLDENGO", 0), ("ANNIHILAPE", 0), ("KYOGRE", 1), ("GROUDON", 1),
        ("AERODACTYL", 1), ("CAMERUPT", 1), ("GALLADE", 1), ("HOUNDOOM", 1),
        ("LATIAS", 1), ("LOPUNNY", 1), ("MANECTRIC", 1), ("METAGROSS", 1),
        ("SALAMENCE", 1), ("SHARPEDO", 1), ("SLOWBRO", 2),
        ("BANETTE", 1), ("GENGAR", 1), ("GYARADOS", 1), ("SABLEYE", 1),
    ]
    for k in spotlight_order:
        if k not in pbs.entries:
            continue
        e = pbs.entries[k]
        row = {"species": e.sym_name, "dex": e.ebdx_stem, "category": e.category}
        for v in VIEWS:
            p = resolve_ebdx_battler(battlers_dirs, v, e)
            ok, (w, h) = is_animated_strip_fast(p)
            row[v] = f"ANIM {h}px/{w//h}f" if ok else "STATIC/MISSING"
        spotlight_detail.append(row)

    return {
        "slices": {
            "trainers": count_slice(roster.trainers),
            "trainer_megas": count_slice(roster.trainer_megas),
            "encounters": count_slice(roster.encounters),
            "live_795": count_slice(roster.live_795),
            "live_796": count_slice(roster.live_796),
            "live_spotlight_819": count_slice(roster.live_spotlight),
            "full_pokedex_1420": count_slice(pbs.entries.keys()),
        },
        "full_by_category": {cat: count_slice(ks) for cat, ks in by_category.items()},
        "prismfall_by_category": {cat: count_slice(ks) for cat, ks in sorted(live_by_cat.items())},
        "spotlight": spotlight_detail,
    }


def print_audit(audit: Dict[str, object], title: str = "EBDX ANIMATED SPRITE AUDIT") -> None:
    print(f"\n{'=' * 96}")
    print(f"  {title}")
    print(f"{'=' * 96}")
    print(f"{'Roster Slice':<32s} {'Total':>5s}  {'Front':>12s}  {'Back':>12s}  {'FrontShiny':>12s}  {'BackShiny':>12s}")
    print("-" * 96)
    for label, key in [
        ("Trainers (PBS)", "trainers"),
        ("Live Trainer Megas", "trainer_megas"),
        ("Encounters + BadgeTiers", "encounters"),
        ("Combined Live PBS (795)", "live_795"),
        ("Live PBS + Dorian ZORUA_1", "live_796"),
        ("Live + Spotlight Bosses (819)", "live_spotlight_819"),
        ("Full Pokédex (1,420)", "full_pokedex_1420"),
    ]:
        s = audit["slices"][key]
        t = s["total"]
        cols = [f"{s[v]['animated']:4d} (-{s[v]['gaps']:<3d})" for v in VIEWS]
        print(f"{label:<32s} {t:5d}  {cols[0]:>12s}  {cols[1]:>12s}  {cols[2]:>12s}  {cols[3]:>12s}")

    print(f"\n{'Full National Dex Category':<32s} {'Total':>5s}  {'Front':>12s}  {'Back':>12s}  {'FrontShiny':>12s}  {'BackShiny':>12s}")
    print("-" * 96)
    for cat, s in audit["full_by_category"].items():
        t = s["total"]
        cols = [f"{s[v]['animated']:4d} (-{s[v]['gaps']:<3d})" for v in VIEWS]
        print(f"{cat:<32s} {t:5d}  {cols[0]:>12s}  {cols[1]:>12s}  {cols[2]:>12s}  {cols[3]:>12s}")

    print(f"\n{'Prismfall Live+Spotlight Category':<32s} {'Total':>5s}  {'Front':>12s}  {'Back':>12s}  {'FrontShiny':>12s}  {'BackShiny':>12s}")
    print("-" * 96)
    for cat, s in audit["prismfall_by_category"].items():
        t = s["total"]
        cols = [f"{s[v]['animated']:4d} (-{s[v]['gaps']:<3d})" for v in VIEWS]
        print(f"{cat:<32s} {t:5d}  {cols[0]:>12s}  {cols[1]:>12s}  {cols[2]:>12s}  {cols[3]:>12s}")

    print(f"\n{'Spotlight Species/Form':<16s} {'EBDX File':<10s} {'Front':<16s} {'Back':<16s} {'FrontShiny':<16s} {'BackShiny':<16s}")
    print("-" * 96)
    for r in audit["spotlight"]:
        print(f"{r['species']:<16s} {r['dex']:<10s} {r['Front']:<16s} {r['Back']:<16s} {r['FrontShiny']:<16s} {r['BackShiny']:<16s}")


# ---------------------------------------------------------------------------
# Installer Engine
# ---------------------------------------------------------------------------

def select_target_entries(pbs: PBSIndex, roster: RosterSlices, scope: str) -> List[FormEntry]:
    if scope == "live":
        keys = roster.live_796
    elif scope == "prismfall":
        keys = roster.live_spotlight
    elif scope == "prismfall-plus-forms":
        extra = {k for k, e in pbs.entries.items() if e.category in ("Mega", "Primal", "Alolan", "Galarian", "Hisuian", "Paldean")}
        keys = roster.live_spotlight | extra
    elif scope == "all":
        keys = set(pbs.entries.keys())
    else:
        raise ValueError(f"Unknown scope: {scope}")
    return [pbs.entries[k] for k in sorted(keys, key=lambda kv: (pbs.entries[kv].dex, kv[1])) if k in pbs.entries]


def _is_non_b2w2_entry(entry: FormEntry) -> bool:
    """True for Gen 6–9 or Mega/Primal/Regional forms (NOT official Game Freak Gen 1–5 B2W2 rips)."""
    return entry.generation >= 6 or entry.category in ("Mega", "Primal", "Alolan", "Galarian", "Hisuian", "Paldean")


def _convert_and_write_one(
    entry: FormEntry,
    lookup_entry: FormEntry,
    view: str,
    sources: Sequence[LocalSpriteSource],
    showdown: Optional[ShowdownGen5AniSource],
    out_battlers: Path,
    min_frame_size: int,
    prefer_more_frames: bool,
    showdown_upgrade_threshold: int = 25,
    min_beat_stock: Optional[Tuple[int, int]] = None,
    female: bool = False,
) -> Tuple[Optional[ConversionResult], List[str], bool]:
    """Convert best strictly-2D candidate for `(entry, view)` and write EBDX strip.

    Returns: `(result_or_None, errors, kept_stock)`
    """
    errors: List[str] = []
    # Each built candidate: (src_name, src_path, strip, cell, nframes, uniq_frames, uniq_rgb, was_2x)
    built: List[Tuple[str, str, Image.Image, int, int, int, int, bool]] = []

    for src in sources:
        p = src.lookup(view, lookup_entry, female=female)
        if not p:
            continue
        try:
            frames = extract_frames_from_gif(p) if p.suffix.lower() == ".gif" else extract_frames_from_png_strip(p)
            strip, cell, nframes, uniq_frames, uniq_rgb, was_2x = build_ebdx_strip(frames, min_frame_size=min_frame_size)
            built.append((src.name, str(p), strip, cell, nframes, uniq_frames, uniq_rgb, was_2x))
            if not prefer_more_frames:
                break
        except Exception as exc:
            errors.append(f"{src.name}:{p.name}: {exc}")

    # Pick candidate with best (unique_frames, total_frames) when prefer_more_frames is enabled
    chosen = None
    if built:
        chosen = max(built, key=lambda c: (c[5], c[4])) if prefer_more_frames else built[0]

    # Check strictly-2D Showdown gen5ani* GIFs if missing OR if current best is low-frame and prefer_more_frames is on
    should_try_showdown = (
        showdown is not None
        and not female
        and (
            chosen is None
            or (prefer_more_frames and showdown_upgrade_threshold > 0 and chosen[4] <= showdown_upgrade_threshold)
        )
    )
    if should_try_showdown:
        try:
            fetched = showdown.fetch_gif(view, lookup_entry)
            if fetched is not None:
                gif_bytes, url = fetched
                frames = extract_frames_from_gif(gif_bytes)
                strip, cell, nframes, uniq_frames, uniq_rgb, was_2x = build_ebdx_strip(frames, min_frame_size=min_frame_size)
                sd_cand = ("showdown_gen5ani", url, strip, cell, nframes, uniq_frames, uniq_rgb, was_2x)
                # Only replace existing local candidate when Showdown genuinely has STRICTLY MORE unique frames
                if chosen is None or sd_cand[5] > chosen[5]:
                    chosen = sd_cand
        except Exception as exc:
            errors.append(f"showdown_gen5ani: {exc}")

    if chosen is None:
        return None, errors, False

    src_name, src_path, strip, cell, nframes, uniq_frames, uniq_rgb, was_2x = chosen

    # If upgrading an already-animated stock Gen 6 / Mega strip, only overwrite if strictly smoother!
    if min_beat_stock is not None:
        stock_uniq, stock_total = min_beat_stock
        if (uniq_frames, nframes) <= (stock_uniq, stock_total):
            return None, [], True

    sub_dir = out_battlers / view / ("Female" if female else "")
    sub_dir.mkdir(parents=True, exist_ok=True)
    out_file = sub_dir / f"{entry.ebdx_stem}.png"
    strip.save(out_file, format="PNG", optimize=True)
    return (
        ConversionResult(
            species=entry.species,
            form=entry.form,
            dex=entry.dex,
            view=view,
            ebdx_filename=f"{view}/{'Female/' if female else ''}{entry.ebdx_stem}.png",
            source_name=src_name,
            source_path=src_path,
            frame_size=cell,
            frame_count=nframes,
            unique_frames=uniq_frames,
            unique_rgb=uniq_rgb,
            was_downscaled_2x=was_2x,
            output_bytes=out_file.stat().st_size,
            female=female,
        ),
        errors,
        False,
    )


def run_install(
    pbs: PBSIndex,
    roster: RosterSlices,
    engine_battlers: Path,
    out_battlers: Path,
    sources: Sequence[LocalSpriteSource],
    showdown: Optional[ShowdownGen5AniSource],
    scope: str,
    overwrite_existing: bool,
    upgrade_stock_non_b2w2: bool,
    showdown_upgrade_threshold: int,
    min_frame_size: int,
    prefer_more_frames: bool,
    include_female: bool,
    workers: int,
) -> Tuple[List[ConversionResult], List[Dict[str, object]]]:
    entries = select_target_entries(pbs, roster, scope)
    if showdown is not None:
        # Pre-warm directory indices on the main thread for thread-safe parallel lookups
        for v in VIEWS:
            showdown._ensure_index(v)

    # Job tuple: (target_entry, lookup_entry, view, female, min_beat_stock)
    jobs: List[Tuple[FormEntry, FormEntry, str, bool, Optional[Tuple[int, int]]]] = []

    for entry in entries:
        alias_key = STOCK_MISSLOTTED_FORM_ALIASES.get(entry.key) if upgrade_stock_non_b2w2 else None
        lookup_entry = pbs.entries[alias_key] if (alias_key and alias_key in pbs.entries) else entry

        for view in VIEWS:
            existing = resolve_ebdx_battler([engine_battlers], view, entry)
            already_anim, (ew, eh) = is_animated_strip_fast(existing)

            if alias_key is not None:
                # Explicitly replace stock's mis-slotted form (e.g. stock Front/658_1.png Ash-Greninja -> base Greninja)
                jobs.append((entry, lookup_entry, view, False, None))
            elif not already_anim or overwrite_existing:
                jobs.append((entry, lookup_entry, view, False, None))
            elif upgrade_stock_non_b2w2 and _is_non_b2w2_entry(entry) and existing is not None:
                try:
                    st_frames = extract_frames_from_png_strip(existing)
                    st_uniq = count_unique_frames(st_frames)
                    st_total = len(st_frames)
                except Exception:
                    st_uniq, st_total = 0, (ew // eh if eh else 0)
                jobs.append((entry, lookup_entry, view, False, (st_uniq, st_total)))

            # Always check distinct animated Female/ variants even when the base/male sprite is already animated!
            if include_female and alias_key is None:
                has_anim_fem = False
                for s in sources:
                    fp = s.lookup(view, entry, female=True)
                    if fp is not None and (fp.suffix.lower() == ".gif" or is_animated_strip_fast(fp)[0]):
                        has_anim_fem = True
                        break
                if has_anim_fem:
                    fem_path = engine_battlers / view / "Female" / f"{entry.ebdx_stem}.png"
                    fem_anim, _ = is_animated_strip_fast(fem_path)
                    if overwrite_existing or not fem_anim:
                        jobs.append((entry, entry, view, True, None))
                    elif upgrade_stock_non_b2w2 and _is_non_b2w2_entry(entry):
                        try:
                            st_frames = extract_frames_from_png_strip(fem_path)
                            jobs.append((entry, entry, view, True, (count_unique_frames(st_frames), len(st_frames))))
                        except Exception:
                            jobs.append((entry, entry, view, True, None))

    print(f"[install] Scope='{scope}' -> {len(entries)} species/forms, {len(jobs)} candidate sprite jobs across {VIEWS}...")
    t0 = time.time()
    installed: List[ConversionResult] = []
    skipped: List[Dict[str, object]] = []
    kept_stock = 0

    def worker(job: Tuple[FormEntry, FormEntry, str, bool, Optional[Tuple[int, int]]]):
        e, le, v, fem, min_beat = job
        return e, v, fem, *_convert_and_write_one(
            entry=e,
            lookup_entry=le,
            view=v,
            sources=sources,
            showdown=showdown,
            out_battlers=out_battlers,
            min_frame_size=min_frame_size,
            prefer_more_frames=prefer_more_frames,
            showdown_upgrade_threshold=showdown_upgrade_threshold,
            min_beat_stock=min_beat,
            female=fem,
        )

    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, workers)) as ex:
        for idx, (e, v, fem, res, errs, was_kept) in enumerate(ex.map(worker, jobs), 1):
            if res is not None:
                installed.append(res)
            elif was_kept:
                kept_stock += 1
            else:
                skipped.append({"species": e.sym_name, "dex": e.ebdx_stem, "view": v, "female": fem, "errors": errs})
            if idx % 200 == 0 or idx == len(jobs):
                print(f"  progress: {idx}/{len(jobs)} processed ({len(installed)} installed, {kept_stock} kept stock, {len(skipped)} unresolved)")

    elapsed = time.time() - t0
    total_mb = sum(r.output_bytes for r in installed) / (1024 * 1024)
    print(f"[install] Done in {elapsed:.1f}s -> {len(installed)} strips written ({total_mb:.2f} MB), {kept_stock} stock preserved, {len(skipped)} unresolved.")
    return installed, skipped


# ---------------------------------------------------------------------------
# Strict Strip Verifier (Motion, Unique Frames, 2D Palette/Alpha, Canonical Names)
# ---------------------------------------------------------------------------

def verify_strips_dir(verify_dir: Path, pbs: Optional[PBSIndex] = None) -> Dict[str, object]:
    """Verify every PNG strip in `verify_dir/{Front,Back,FrontShiny,BackShiny}[/Female]`."""
    failures: List[Dict[str, object]] = []
    checked = 0
    total_bytes = 0
    per_view = Counter()
    heights: List[int] = []
    frames_list: List[int] = []
    unique_frames_list: List[int] = []
    low4_strips: List[str] = []
    low10_strips: List[Dict[str, object]] = []
    uniq_le4_strips: List[Dict[str, object]] = []
    high_rgb_gt64: List[Dict[str, object]] = []

    for view in VIEWS:
        vdir = verify_dir / view
        if not vdir.exists():
            continue
        for p in sorted(vdir.rglob("*.png")):
            checked += 1
            sz = p.stat().st_size
            total_bytes += sz
            rel = p.relative_to(verify_dir).as_posix()
            per_view[view] += 1

            # Filename check
            stem = p.stem
            m = re.match(r"^(\d+)(?:_(\d+))?$", stem)
            if pbs and m:
                dex = int(m.group(1))
                fm = int(m.group(2)) if m.group(2) else 0
                sp = pbs.dex_to_species.get(dex)
                if not sp or (sp, fm) not in pbs.entries:
                    failures.append({"file": rel, "reason": f"Dex/form {dex}_{fm} not found in PBS"})
                    continue
            elif not m:
                failures.append({"file": rel, "reason": f"Non-canonical EBDX filename: {p.name}"})
                continue

            try:
                with Image.open(p) as im:
                    if im.mode != "RGBA":
                        failures.append({"file": rel, "reason": f"Mode is {im.mode}, expected RGBA"})
                        continue
                    w, h = im.size
                    if h < MIN_1X_FRAME_SIZE or h > MAX_1X_FRAME_SIZE:
                        failures.append({"file": rel, "reason": f"Height {h}px outside [{MIN_1X_FRAME_SIZE}, {MAX_1X_FRAME_SIZE}]"})
                        continue
                    if w <= h or w % h != 0:
                        failures.append({"file": rel, "reason": f"Not a multi-frame square strip: {w}x{h}"})
                        continue
                    nf = w // h
                    frame_bytes = [im.crop((fi * h, 0, (fi + 1) * h, h)).tobytes() for fi in range(nf)]
                    uniq_f = len(set(frame_bytes))
                    if uniq_f <= 1:
                        failures.append({"file": rel, "reason": f"Frozen animation: all {nf} frames are identical"})
                        continue
                    f0 = im.crop((0, 0, h, h))
                    # Strict 2D pixel art verification on frame 0
                    data = f0.get_flattened_data()
                    semi = 0
                    nont = 0
                    rgb = set()
                    for r, g, b, a in data:
                        if a > 0:
                            nont += 1
                            if a < 255:
                                semi += 1
                            rgb.add((r, g, b))
                    if nont == 0:
                        failures.append({"file": rel, "reason": "Empty transparent frame 0"})
                        continue
                    if semi > 0:
                        failures.append({"file": rel, "reason": f"Has {semi} semi-transparent halo pixels"})
                        continue
                    if len(rgb) > MAX_2D_UNIQUE_RGB:
                        failures.append({"file": rel, "reason": f"Too many RGB colors ({len(rgb)} > {MAX_2D_UNIQUE_RGB})"})
                        continue
                    heights.append(h)
                    frames_list.append(nf)
                    unique_frames_list.append(uniq_f)
                    if nf <= 4:
                        low4_strips.append(rel)
                    if nf <= 10:
                        low10_strips.append({"file": rel, "frames": nf, "unique_frames": uniq_f, "h": h})
                    if uniq_f <= 4:
                        uniq_le4_strips.append({"file": rel, "frames": nf, "unique_frames": uniq_f, "h": h})
                    if len(rgb) > 64:
                        high_rgb_gt64.append({"file": rel, "unique_rgb": len(rgb), "frames": nf, "h": h})
            except Exception as exc:
                failures.append({"file": rel, "reason": f"Unreadable PNG: {exc}"})

    heights.sort()
    frames_list.sort()
    unique_frames_list.sort()
    summary = {
        "verify_dir": str(verify_dir),
        "checked_strips": checked,
        "passed_strips": checked - len(failures),
        "failed_strips": len(failures),
        "total_mb": round(total_bytes / (1024 * 1024), 2),
        "per_view": dict(per_view),
        "height_min_med_max": (
            (heights[0], heights[len(heights) // 2], heights[-1]) if heights else (0, 0, 0)
        ),
        "frames_min_med_max": (
            (frames_list[0], frames_list[len(frames_list) // 2], frames_list[-1]) if frames_list else (0, 0, 0)
        ),
        "unique_frames_min_med_max": (
            (unique_frames_list[0], unique_frames_list[len(unique_frames_list) // 2], unique_frames_list[-1])
            if unique_frames_list else (0, 0, 0)
        ),
        "low4_count": len(low4_strips),
        "low10_count": len(low10_strips),
        "uniq_le4_count": len(uniq_le4_strips),
        "high_rgb_gt64_count": len(high_rgb_gt64),
        "high_rgb_gt64": high_rgb_gt64,
        "failures": failures,
    }
    return summary


# ---------------------------------------------------------------------------
# Hygiene: Lowercase .PNG Extensions
# ---------------------------------------------------------------------------

def normalize_png_extensions(graphics_pokemon_dir: Path) -> List[Tuple[str, str]]:
    renamed: List[Tuple[str, str]] = []
    if not graphics_pokemon_dir.exists():
        return renamed
    for p in sorted(graphics_pokemon_dir.rglob("*.PNG")):
        target = p.with_suffix(".png")
        if target.exists() and target != p:
            continue
        p.rename(target)
        renamed.append((str(p), str(target)))
    return renamed


# ---------------------------------------------------------------------------
# CLI Entrypoint
# ---------------------------------------------------------------------------

def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description="Pokémon Prismfall — Full National Dex (#001–#1025 + 395 Forms) EBDX Animated B2W2 Sprite Importer"
    )
    ap.add_argument("--engine", type=Path, default=Path("/home/antigravity/pf_engine_run/base"),
                    help="Path to Essentials + EBDX engine directory containing PBS/ and Graphics/EBDX/Battlers/")
    ap.add_argument("--prismfall-pbs", type=Path, default=Path("/home/antigravity/reuben12358/prismfall/pbs"),
                    help="Path to Prismfall repo pbs/ directory (trainers.txt, encounters.txt, etc.)")
    ap.add_argument("--download-sources", type=Path, default=None,
                    help="Download verified open-source 2D sprite packs into this directory")
    ap.add_argument("--source", action="append", default=[],
                    help="Local sprite source in `name=/path/to/dir` format (repeatable in priority order)")
    ap.add_argument("--fetch-showdown-gaps", action="store_true",
                    help="Fetch strictly-2D Pokémon Showdown gen5ani* GIFs for missing slots and low-frame upgrades")
    ap.add_argument("--showdown-cache", type=Path, default=None,
                    help="Optional cache directory for Showdown gen5ani indices/GIFs")
    ap.add_argument("--showdown-upgrade-threshold", type=int, default=25,
                    help="With --prefer-more-frames & --fetch-showdown-gaps, probe Showdown when local best <= N frames (default: 25)")
    ap.add_argument("--audit", action="store_true",
                    help="Print quantitative before/after EBDX animation coverage audit")
    ap.add_argument("--install-prismfall", action="store_true",
                    help="Install missing/static/upgradable animated strips into --out-battlers (or engine)")
    ap.add_argument("--scope", choices=("live", "prismfall", "prismfall-plus-forms", "all"), default="all",
                    help="Species/form scope for --install-prismfall (default: all = full 1,420-entry National Dex + 395 forms)")
    ap.add_argument("--out-battlers", type=Path, default=None,
                    help="Target Graphics/EBDX/Battlers/ directory (defaults to <engine>/Graphics/EBDX/Battlers/)")
    ap.add_argument("--overlay-audit", type=Path, default=None,
                    help="Additional battlers overlay directory to include during --audit")
    ap.add_argument("--overwrite-existing", action="store_true",
                    help="Overwrite already-animated EBDX strips (default: preserve stock Gen 1–5 & existing strips)")
    ap.add_argument("--upgrade-stock-non-b2w2", action="store_true",
                    help="Upgrade low-frame stock Gen 6 & Mega/Regional fan strips when sources have strictly more unique frames (NEVER touches Gen 1–5 official B2W2!) and fix stock 658_1 mis-slot")
    ap.add_argument("--prefer-more-frames", action="store_true",
                    help="When multiple sources provide a sprite, pick the one with the most unique frames")
    ap.add_argument("--include-female", action="store_true",
                    help="Also install distinct animated Female/ variants when provided by sources")
    ap.add_argument("--min-frame-size", type=int, default=0,
                    help="Optional minimum square frame size in px (default: 0 = tight union square matching stock #001-#649)")
    ap.add_argument("--verify-strips", action="store_true",
                    help="Strictly verify every PNG strip in --verify-dir (or --out-battlers)")
    ap.add_argument("--verify-dir", type=Path, default=None,
                    help="Directory to verify when using --verify-strips")
    ap.add_argument("--normalize-extensions", type=Path, default=None,
                    help="Rename uppercase *.PNG files to lowercase *.png under this Graphics/Pokemon directory")
    ap.add_argument("--write-manifest", type=Path, default=None,
                    help="Write detailed JSON installation & audit manifest to this path")
    ap.add_argument("--workers", type=int, default=8,
                    help="Parallel conversion workers (default: 8)")
    return ap.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)

    if args.download_sources is not None:
        download_sources(args.download_sources)

    pbs = load_pbs_index(args.engine)
    roster = load_prismfall_roster(pbs, args.prismfall_pbs)
    engine_battlers = args.engine / "Graphics" / "EBDX" / "Battlers"
    out_battlers = args.out_battlers or engine_battlers

    manifest: Dict[str, object] = {
        "engine": str(args.engine),
        "prismfall_pbs": str(args.prismfall_pbs),
        "out_battlers": str(out_battlers),
        "scope": args.scope,
        "upgrade_stock_non_b2w2": args.upgrade_stock_non_b2w2,
        "showdown_upgrade_threshold": args.showdown_upgrade_threshold,
    }

    if args.audit:
        before_dirs = [engine_battlers]
        if args.overlay_audit:
            before_dirs = [args.overlay_audit, engine_battlers]
        before_audit = audit_battlers(pbs, roster, before_dirs)
        manifest["audit_before"] = before_audit
        print_audit(before_audit, title="BEFORE — EBDX ANIMATED SPRITE AUDIT")

    if args.install_prismfall:
        local_sources: List[LocalSpriteSource] = []
        for spec in args.source:
            if "=" not in spec:
                raise ValueError(f"--source must be `name=/path/to/dir`, got: {spec}")
            sname, spath = spec.split("=", 1)
            local_sources.append(LocalSpriteSource(sname.strip(), Path(spath.strip())))

        showdown = ShowdownGen5AniSource(cache_dir=args.showdown_cache) if args.fetch_showdown_gaps else None
        if not local_sources and showdown is None:
            raise ValueError("Provide at least one --source or --fetch-showdown-gaps with --install-prismfall")

        installed, skipped = run_install(
            pbs=pbs,
            roster=roster,
            engine_battlers=engine_battlers,
            out_battlers=out_battlers,
            sources=local_sources,
            showdown=showdown,
            scope=args.scope,
            overwrite_existing=args.overwrite_existing,
            upgrade_stock_non_b2w2=args.upgrade_stock_non_b2w2,
            showdown_upgrade_threshold=args.showdown_upgrade_threshold,
            min_frame_size=args.min_frame_size,
            prefer_more_frames=args.prefer_more_frames,
            include_female=args.include_female,
            workers=args.workers,
        )
        manifest["installed_count"] = len(installed)
        manifest["skipped_count"] = len(skipped)
        manifest["installed_mb"] = round(sum(r.output_bytes for r in installed) / (1024 * 1024), 2)
        manifest["by_source"] = dict(Counter(r.source_name for r in installed))
        manifest["by_view"] = dict(Counter(r.view for r in installed))
        manifest["installed"] = [r.__dict__ for r in installed]
        manifest["skipped"] = skipped

        if args.audit:
            after_dirs = [out_battlers, engine_battlers] if out_battlers != engine_battlers else [engine_battlers]
            after_audit = audit_battlers(pbs, roster, after_dirs)
            manifest["audit_after"] = after_audit
            print_audit(after_audit, title="AFTER — EBDX ANIMATED SPRITE AUDIT")

    if args.normalize_extensions is not None:
        renamed = normalize_png_extensions(args.normalize_extensions)
        print(f"[hygiene] Lowercased {len(renamed)} uppercase .PNG files under {args.normalize_extensions}")
        manifest["normalized_extensions"] = renamed

    if args.verify_strips:
        vdir = args.verify_dir or out_battlers
        vsummary = verify_strips_dir(vdir, pbs=pbs)
        manifest["verify"] = vsummary
        print(f"\n{'=' * 96}")
        print(f"  STRIP VERIFICATION: {vdir}")
        print(f"{'=' * 96}")
        print(
            f"  Checked: {vsummary['checked_strips']} | Passed: {vsummary['passed_strips']} | "
            f"Failed: {vsummary['failed_strips']} | Total Size: {vsummary['total_mb']} MB"
        )
        print(f"  Per view: {vsummary['per_view']}")
        print(f"  Frame size (min/med/max): {vsummary['height_min_med_max']} px")
        print(f"  Frame count (min/med/max): {vsummary['frames_min_med_max']} frames")
        print(f"  Unique frames (min/med/max): {vsummary['unique_frames_min_med_max']} unique")
        print(
            f"  Quality flags: <=4f={vsummary['low4_count']} | <=10f={vsummary['low10_count']} | "
            f"<=4 unique={vsummary['uniq_le4_count']} | >64 RGB={vsummary['high_rgb_gt64_count']}"
        )
        if vsummary["failures"]:
            print("  FAILURES (first 20):")
            for fail in vsummary["failures"][:20]:
                print(f"    - {fail['file']}: {fail['reason']}")

    if args.write_manifest is not None:
        args.write_manifest.parent.mkdir(parents=True, exist_ok=True)
        args.write_manifest.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        print(f"[manifest] Wrote {args.write_manifest}")

    if args.verify_strips and manifest.get("verify", {}).get("failed_strips", 0) > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
