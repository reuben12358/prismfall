#!/usr/bin/env python3
"""
Prismfall trainer data validator.

Checks /home/claude/fangame/pbs/trainers.txt and trainer_types.txt against the
base-project reference PBS (/home/claude/ref/ebdx/PBS: Essentials v21.1 + EBDX + Gen 9 Pack) (species, forms, moves, abilities, items,
natures) and against the SPINE trainer versioning scheme.

Usage:
  python3 tools/validate_trainers.py                 # validate, exit 1 on errors
  python3 tools/validate_trainers.py --summary       # also print every team
  python3 tools/validate_trainers.py --strict        # warnings count as errors
  python3 tools/validate_trainers.py --maps maps_out/Data
                                                     # also check every trainer that map
                                                     # events reference exists (raw string
                                                     # scan of Map*.rxdata, no Marshal load)
  python3 tools/validate_trainers.py --learnset SPECIES[,FORM] [LEVEL]
                                                     # show every legal move

Paths can be overridden with --ref DIR (reference PBS folder) and
--pbs DIR (our PBS folder).  --balance FILE points at BALANCE.md, which holds
the allowlist of intentional non-learnable moves (see the table under the
heading "Intentional non-learnable moves").

Pure standard library; Python 3.8+.
"""
import argparse
import os
import re
import sys
from collections import defaultdict, OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_REF = "/home/claude/ref/ebdx/PBS"   # Essentials 21.1 + EBDX + Gen 9 Pack (Gen 1-9)
DEFAULT_PBS = os.path.normpath(os.path.join(HERE, "..", "pbs"))
DEFAULT_BALANCE = os.path.normpath(os.path.join(HERE, "..", "design", "BALANCE.md"))

NATURES = """HARDY LONELY BRAVE ADAMANT NAUGHTY BOLD DOCILE RELAXED IMPISH LAX TIMID
HASTY SERIOUS JOLLY NAIVE MODEST MILD QUIET BASHFUL RASH CALM GENTLE SASSY
CAREFUL QUIRKY""".split()
GENDERS = {"M", "m", "Male", "male", "0", "F", "f", "Female", "female", "1"}
TT_GENDERS = {"Male", "male", "M", "m", "0", "Female", "female", "F", "f", "1",
              "Unknown", "unknown", "Other", "other", "Mixed", "mixed", "X", "x", "2"}
AI_FLAGS = {"PredictMoveFailure", "ScoreMoves", "PreferMultiTargetMoves", "HPAware",
            "ConsiderSwitching", "ReserveLastPokemon", "UsePokemonInOrder"}
TT_KEYS = {"Name", "Gender", "BaseMoney", "SkillLevel", "Flags", "IntroBGM",
           "BattleBGM", "VictoryBGM"}
TRAINER_KEYS = {"Items", "LoseText", "Pokemon"}
PKMN_KEYS = {"Form", "Name", "Moves", "Ability", "AbilityIndex", "Item", "Gender",
             "Nature", "IV", "EV", "Happiness", "Shiny", "SuperShiny", "Shadow", "Ball"}
MAX_LEVEL = 100
ROTOM_FORM_MOVES = {1: "OVERHEAT", 2: "HYDROPUMP", 3: "BLIZZARD", 4: "AIRSLASH", 5: "LEAFSTORM"}
# Gen 9 evolutions that the live base-project pokemon.txt does not list (the
# Gen 9 Pack only adds them via its optional "Auto-Updates" PBS). Treated as
# prevolutions for move-learnability purposes.
MANUAL_PREVO = {"KINGAMBIT": "BISHARP", "ANNIHILAPE": "PRIMEAPE", "FARIGIRAF": "GIRAFARIG",
                "DUDUNSPARCE": "DUNSPARCE", "URSALUNA": "URSARING", "WYRDEER": "STANTLER",
                "KLEAVOR": "SCYTHER", "SNEASLER": "SNEASEL", "OVERQWIL": "QWILFISH",
                "BASCULEGION": "BASCULIN"}

# --- SPINE data (LOCKED) ------------------------------------------------------
# gym number -> (trainer type, trainer name, level cap)
WARDENS = OrderedDict([
    (1, ("LEADER_TAMSIN", "Tamsin", 15)),
    (2, ("LEADER_DORIAN", "Dorian", 19)),
    (3, ("LEADER_MARISOL", "Marisol", 23)),
    (4, ("LEADER_ROOK", "Rook", 27)),
    (5, ("LEADER_SAHAR", "Sahar", 31)),
    (6, ("LEADER_CORVIN", "Corvin", 35)),
    (7, ("LEADER_BRANN", "Brann", 39)),
    (8, ("LEADER_KAITO", "Kaito", 43)),
    (9, ("LEADER_JUNO", "Juno", 47)),       # J3: rival-versioned (30/31/32)
    (10, ("LEADER_ANJA", "Anja", 51)),
    (11, ("LEADER_ODESSA", "Odessa", 55)),
    (12, ("LEADER_ILSA", "Ilsa", 59)),
    (13, ("LEADER_BASTIAN", "Bastian", 63)),
    (14, ("LEADER_YSOLDE", "Ysolde", 67)),
    (15, ("LEADER_MAGNUS", "Magnus", 71)),
    (16, ("LEADER_NYX", "Nyx", 75)),
    (17, ("LEADER_CELESTINE", "Celestine", 80)),
    (18, ("LEADER_SIGRUN", "Sigrun", 85)),
])
# Rival battle -> (trainer type, name, max allowed level on Standard/Hard)
RIVAL_BATTLES = OrderedDict([
    (("RIVAL_KESTREL", 1), ("Kestrel", 7)),
    (("RIVAL_KESTREL", 2), ("Kestrel", 23)),
    (("RIVAL_KESTREL", 3), ("Kestrel", 35)),
    (("RIVAL_KESTREL", 4), ("Kestrel", 43)),
    (("RIVAL_KESTREL", 5), ("Kestrel", 55)),
    (("RIVAL_KESTREL", 6), ("Kestrel", 67)),
    (("RIVAL_KESTREL", 7), ("Kestrel", 80)),
    (("RIVAL_KESTREL", 8), ("Kestrel", 94)),
    (("RIVAL_KESTREL", 9), ("Kestrel", 94)),    # Festival SF variant "Kestrel (Fallen)"
    (("RIVAL_JUNO", 1), ("Juno", 19)),
    (("RIVAL_JUNO", 2), ("Juno", 35)),
    (("LEADER_JUNO", 3), ("Juno", 47)),     # J3 is the Gym 9 Warden battle
    (("RIVAL_JUNO", 4), ("Juno", 90)),
    (("RIVAL_JUNO", 7), ("Juno", 97)),          # Ch21 tag-battle partner (when Kestrel is Fallen)
])
# Gen 1 starter line written in PBS for each starter_slot of the player
# (0 = player chose Grass, 1 = Fire, 2 = Water).
GRASS_LINE = ["BULBASAUR", "IVYSAUR", "VENUSAUR"]
FIRE_LINE = ["CHARMANDER", "CHARMELEON", "CHARIZARD"]
WATER_LINE = ["SQUIRTLE", "WARTORTLE", "BLASTOISE"]
RIVAL_STARTER = {
    # Kestrel picks the starter with type advantage over the player's
    "RIVAL_KESTREL": {0: FIRE_LINE, 1: WATER_LINE, 2: GRASS_LINE},
    # Juno picks the starter weak to the player's
    "RIVAL_JUNO": {0: WATER_LINE, 1: GRASS_LINE, 2: FIRE_LINE},
    "LEADER_JUNO": {0: WATER_LINE, 1: GRASS_LINE, 2: FIRE_LINE},
}
SINGLE_BOSSES = [  # (type, name, min ace level, max ace level) - Standard/Hard
    ("CHAMPION_VALEN", "Valen", 96, 96),
    ("MERIDIAN_VOSS", "Aurelian", 100, 100),
]
# Every FESTIVAL_<NAME> cameo type that has trainer data must have 0/100/200 and an
# ace in this range (Standard/Hard).
# design/CAMEOS.md placements: {type: {version: ace level}}
CAMEO_PLACEMENT = {
    "FESTIVAL_SHELLY": {1: 17, 2: 100}, "FESTIVAL_VENAM": {1: 38, 2: 100}, "FESTIVAL_GARRET": {1: 46, 2: 100},
    "FESTIVAL_MELIA": {1: 50, 2: 100}, "FESTIVAL_ALEXANDRA": {1: 56, 2: 100}, "FESTIVAL_AMARIA": {1: 78, 2: 100},
    "FESTIVAL_TITANIA": {1: 78, 2: 100}, "FESTIVAL_SHIV": {1: 84, 2: 100}, "FESTIVAL_LIN": {1: 100},
    "FESTIVAL_NOVA": {1: 90},
}
DIFF_NAMES = {0: "Standard", 1: "Hard", 2: "Casual"}


# --- generic PBS reading --------------------------------------------------------
def read_lines(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        for no, raw in enumerate(f, 1):
            line = raw.rstrip("\r\n")
            yield no, line


def parse_sections(path):
    """Generic [Section] / Key = Value reader (keys may repeat -> list)."""
    sections = OrderedDict()
    cur = None
    for no, line in read_lines(path):
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        m = re.match(r"^\[\s*(.+?)\s*\]$", s)
        if m:
            cur = OrderedDict()
            cur["__line__"] = no
            sections[m.group(1)] = cur
            continue
        m = re.match(r"^(\w+)\s*=\s*(.*)$", s)
        if m and cur is not None:
            cur.setdefault(m.group(1), []).append(m.group(2).strip())
    return sections


def csv(v):
    return [x.strip() for x in v.split(",") if x.strip() != ""]


# --- reference data ---------------------------------------------------------------
class RefData:
    def __init__(self, ref_dir):
        self.ref_dir = ref_dir
        self.species = {}      # "SPECIES" or "SPECIES_n" -> dict
        self.moves = set()
        self.move_info = {}
        self.abilities = set()
        self.items = {}
        self.mega_stones = {}  # item -> (species, form)
        self.ref_trainer_types = set()
        self._load()

    def _load(self):
        r = self.ref_dir
        for sid, sec in parse_sections(os.path.join(r, "pokemon.txt")).items():
            self.species[sid] = self._species_entry(sid, 0, sec)
        # prevolutions (base forms)
        self.prevo = {}
        for sid, d in list(self.species.items()):
            for evo in d["evolutions"]:
                self.prevo.setdefault(evo, sid)
        for evo, pre in MANUAL_PREVO.items():
            if evo in self.species and pre in self.species:
                self.prevo.setdefault(evo, pre)
        for key, sec in parse_sections(os.path.join(r, "pokemon_forms.txt")).items():
            sp, form = csv(key)
            form = int(form)
            base = self.species[sp]
            entry = self._species_entry(sp, form, sec, base)
            self.species["%s_%d" % (sp, form)] = entry
            if "MegaStone" in sec:
                self.mega_stones[sec["MegaStone"][0]] = (sp, form)
        for mid, sec in parse_sections(os.path.join(r, "moves.txt")).items():
            self.moves.add(mid)
            self.move_info[mid] = {
                "type": sec.get("Type", ["?"])[0],
                "cat": sec.get("Category", ["?"])[0],
                "power": sec.get("Power", ["0"])[0],
            }
        for aid in parse_sections(os.path.join(r, "abilities.txt")):
            self.abilities.add(aid)
        for iid, sec in parse_sections(os.path.join(r, "items.txt")).items():
            flags = []
            for f in sec.get("Flags", []):
                flags += csv(f)
            self.items[iid] = {"flags": set(flags), "name": sec.get("Name", [iid])[0]}
        for tid in parse_sections(os.path.join(r, "trainer_types.txt")):
            self.ref_trainer_types.add(tid)
        self.ref_trainers = set()
        for key in parse_sections(os.path.join(r, "trainers.txt")):
            parts = [x.strip() for x in key.split(",")]
            if len(parts) >= 2:
                ver = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 0
                self.ref_trainers.add((parts[0], parts[1], ver))

    @staticmethod
    def _species_entry(sp, form, sec, base=None):
        def get_list(key, default):
            if key in sec:
                out = []
                for v in sec[key]:
                    out += csv(v)
                return out
            return list(default) if default is not None else []

        lvl_moves = []
        if "Moves" in sec:
            vals = []
            for v in sec["Moves"]:
                vals += csv(v)
            for i in range(0, len(vals) - 1, 2):
                lvl_moves.append((int(vals[i]), vals[i + 1]))
        elif base is not None:
            lvl_moves = list(base["levelmoves"])
        evos = []
        if "Evolution" in sec or "Evolutions" in sec:
            # v21.1 writes one "Evolution = A,Method,Param" per line; the Gen 9 Pack
            # writes "Evolutions = A,Method,Param,B,Method,Param,..." (triples).
            for v in sec.get("Evolution", []):
                evos.append(csv(v)[0])
            for v in sec.get("Evolutions", []):
                vals = [x.strip() for x in v.split(",")]
                evos += [vals[i] for i in range(0, len(vals), 3) if vals[i]]
        elif base is not None:
            evos = list(base["evolutions"])
        return {
            "species": sp,
            "form": form,
            "name": sec.get("Name", [base["name"] if base else sp])[0],
            "formname": sec.get("FormName", [""])[0],
            "types": get_list("Types", base["types"] if base else None),
            "abilities": get_list("Abilities", base["abilities"] if base else None),
            "hidden": get_list("HiddenAbilities", base["hidden"] if base else None),
            "levelmoves": lvl_moves,
            "tutor": set(get_list("TutorMoves", base["tutor"] if base else None)),
            "egg": set(get_list("EggMoves", base["egg"] if base else None)),
            "evolutions": evos,
            "generation": int(sec.get("Generation", [base["generation"] if base else 0])[0]),
            "mega": "MegaStone" in sec,
            "flags": set(get_list("Flags", base["flags"] if base else None)),
        }

    def get_form(self, sp, form):
        if form and ("%s_%d" % (sp, form)) in self.species:
            return self.species["%s_%d" % (sp, form)]
        return self.species.get(sp)

    def family(self, sp, form):
        """species entry + all prevolutions (same form number where it exists)."""
        out = []
        cur = sp
        seen = set()
        while cur and cur not in seen:
            seen.add(cur)
            e = self.get_form(cur, form)
            if e:
                out.append(e)
            cur = self.prevo.get(cur)
        return out

    def learn_sources(self, sp, form, move):
        """Returns list of (how, min_level) for this move on this species/form."""
        res = []
        for e in self.family(sp, form):
            for lv, m in e["levelmoves"]:
                if m == move:
                    res.append(("level", lv if lv > 0 else 1, e["name"]))
            if move in e["tutor"]:
                res.append(("tutor", 1, e["name"]))
            if move in e["egg"]:
                res.append(("egg", 1, e["name"]))
        return res

    def all_learnable(self, sp, form, level=MAX_LEVEL):
        out = {}
        for e in self.family(sp, form):
            for lv, m in e["levelmoves"]:
                if lv <= level:
                    out.setdefault(m, "L%d(%s)" % (lv, e["name"]))
            for m in e["tutor"]:
                out.setdefault(m, "tutor")
            for m in e["egg"]:
                out.setdefault(m, "egg")
        return out


# --- our PBS ---------------------------------------------------------------------
class Mon:
    def __init__(self, species, level, line):
        self.species = species
        self.level = level
        self.line = line
        self.props = {}


class Trainer:
    def __init__(self, ttype, name, version, line):
        self.ttype = ttype
        self.name = name
        self.version = version
        self.line = line
        self.items = []
        self.lose_text = None
        self.mons = []

    @property
    def key(self):
        return (self.ttype, self.name, self.version)

    def label(self):
        return "[%s,%s,%d]" % self.key


class Report:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def err(self, where, msg):
        self.errors.append("%s: %s" % (where, msg))

    def warn(self, where, msg):
        self.warnings.append("%s: %s" % (where, msg))


def parse_trainers(path, rep):
    trainers = []
    cur = None
    mon = None
    for no, line in read_lines(path):
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        where = "trainers.txt:%d" % no
        m = re.match(r"^\[\s*(.+?)\s*\]$", s)
        if m:
            parts = [p.strip() for p in m.group(1).split(",")]
            if len(parts) < 2 or len(parts) > 3:
                rep.err(where, "bad section header %r" % s)
                cur = None
                continue
            ver = 0
            if len(parts) == 3:
                if not parts[2].isdigit():
                    rep.err(where, "version must be a non-negative integer: %r" % parts[2])
                    continue
                ver = int(parts[2])
            cur = Trainer(parts[0], parts[1], ver, no)
            trainers.append(cur)
            mon = None
            continue
        m = re.match(r"^(\w+)\s*=\s*(.*)$", s)
        if not m:
            rep.err(where, "unparseable line %r" % s)
            continue
        if cur is None:
            rep.err(where, "property before any section")
            continue
        key, val = m.group(1), m.group(2).strip()
        if key == "Pokemon":
            p = csv(val)
            if len(p) != 2 or not p[1].isdigit():
                rep.err(where, "Pokemon line must be SPECIES,LEVEL: %r" % val)
                mon = None
                continue
            mon = Mon(p[0], int(p[1]), no)
            cur.mons.append(mon)
        elif key == "Items":
            cur.items = csv(val)
        elif key == "LoseText":
            cur.lose_text = val
        elif key in PKMN_KEYS:
            if mon is None:
                rep.err(where, "%s before any Pokemon line" % key)
                continue
            if key in mon.props:
                rep.err(where, "duplicate %s for %s" % (key, mon.species))
            mon.props[key] = (val, no)
        else:
            rep.err(where, "unknown key %r" % key)
    return trainers


def load_allowlist(balance_path):
    """Rows of the table under '## Intentional non-learnable moves':
    | TYPE,Name,Version | SPECIES | MOVE | reason |"""
    allow = set()
    if not balance_path or not os.path.exists(balance_path):
        return allow
    in_sec = False
    for _, line in read_lines(balance_path):
        if line.startswith("#"):
            in_sec = "intentional non-learnable moves" in line.lower()
            continue
        if in_sec and line.strip().startswith("|"):
            cells = [c.strip().strip("`") for c in line.strip().strip("|").split("|")]
            if len(cells) >= 3 and "," in cells[0] and not cells[0].startswith("-"):
                tparts = [p.strip() for p in cells[0].split(",")]
                if len(tparts) == 3 and (tparts[2].isdigit() or tparts[2] == "*"):
                    ver = int(tparts[2]) if tparts[2].isdigit() else "*"
                    allow.add((tparts[0], tparts[1], ver, cells[1], cells[2]))
    return allow


def is_allowed(allow, t, species, what):
    return ((t.ttype, t.name, t.version, species, what) in allow or
            (t.ttype, t.name, "*", species, what) in allow)


# --- validation ---------------------------------------------------------------------
def validate_trainer_types(path, ref, rep):
    types = {}
    if not os.path.exists(path):
        rep.err("trainer_types.txt", "file not found: %s" % path)
        return types
    secs = parse_sections(path)
    for tid, sec in secs.items():
        where = "trainer_types.txt:%d [%s]" % (sec["__line__"], tid)
        if not re.match(r"^[A-Z0-9_]+$", tid):
            rep.err(where, "trainer type ID should be UPPER_SNAKE_CASE")
        for k in sec:
            if k != "__line__" and k not in TT_KEYS:
                rep.err(where, "unknown key %r" % k)
        if "Name" not in sec:
            rep.err(where, "missing Name")
        if "Gender" in sec and sec["Gender"][0] not in TT_GENDERS:
            rep.err(where, "bad Gender %r" % sec["Gender"][0])
        for k in ("BaseMoney", "SkillLevel"):
            if k in sec:
                v = sec[k][0]
                if not v.isdigit() or int(v) > 9999:
                    rep.err(where, "%s must be 0-9999" % k)
        if "Flags" in sec:
            for f in csv(sec["Flags"][0]):
                base = f[4:] if f.startswith("Anti") else f
                if base not in AI_FLAGS:
                    rep.warn(where, "flag %r is not a v21.1 AI skill flag (fine if custom)" % f)
        if tid in ref.ref_trainer_types:
            rep.warn(where, "also defined in reference trainer_types.txt (will override)")
        skill = int(sec.get("SkillLevel", sec.get("BaseMoney", ["30"]))[0])
        types[tid] = {"skill": skill, "name": sec.get("Name", [""])[0]}
    return types


def validate_mon(t, mon, ref, rep, allow, megaring_items):
    where = "trainers.txt:%d %s %s" % (mon.line, t.label(), mon.species)
    sp = ref.species.get(mon.species)
    if sp is None:
        rep.err(where, "unknown species %s" % mon.species)
        return
    if not (1 <= mon.level <= MAX_LEVEL):
        rep.err(where, "level %d out of range" % mon.level)
    form = 0
    if "Form" in mon.props:
        fv = mon.props["Form"][0]
        if not fv.isdigit():
            rep.err(where, "Form must be an integer")
        else:
            form = int(fv)
            if form != 0 and ("%s_%d" % (mon.species, form)) not in ref.species:
                rep.err(where, "species has no form %d" % form)
            elif form and ref.species["%s_%d" % (mon.species, form)]["mega"]:
                rep.err(where, "Form %d is a Mega form; give the Mega Stone instead" % form)
    data = ref.get_form(mon.species, form)
    # nickname
    if "Name" in mon.props and len(mon.props["Name"][0]) > 10:
        rep.err(where, "nickname longer than 10 chars")
    # moves
    if "Moves" in mon.props:
        mv = csv(mon.props["Moves"][0])
        if len(mv) > 4:
            rep.err(where, "more than 4 moves")
        if len(set(mv)) != len(mv):
            rep.err(where, "duplicate moves")
        for m in mv:
            if m not in ref.moves:
                rep.err(where, "unknown move %s" % m)
                continue
            src = ref.learn_sources(mon.species, form, m)
            allowed = is_allowed(allow, t, mon.species, m)
            # Rotom's appliance forms are always taught their signature move by the
            # form handler (Data/Scripts/014_Pokemon/001_Pokemon-related/001_FormHandlers.rb).
            if mon.species == "ROTOM" and ROTOM_FORM_MOVES.get(form) == m:
                continue
            if not src:
                if allowed:
                    continue
                rep.err(where, "%s cannot learn %s (not in level-up/tutor/egg lists of it or its prevolutions)"
                        % (data["name"], m))
            else:
                if all(s[0] == "level" for s in src):
                    lvl = min(s[1] for s in src)
                    if lvl > mon.level and not allowed and not t.ttype.startswith("FESTIVAL_"):
                        rep.warn(where, "%s learns %s only by level-up at L%d (> L%d)"
                                 % (data["name"], m, lvl, mon.level))
    elif t.ttype not in ref.ref_trainer_types and not re.search(r"_(GRUNT|AGENT|SOLDIER)(_[MF])?$", t.ttype):
        # stock route trainers and generic grunts may use level-up movesets
        rep.warn(where, "no Moves given (will use level-up moveset)")
    # ability
    if "Ability" in mon.props:
        ab = mon.props["Ability"][0]
        if ab not in ref.abilities:
            rep.err(where, "unknown ability %s" % ab)
        else:
            legal = set(data["abilities"]) | set(data["hidden"])
            # Megas: ability legal on the base form is fine (it changes on Mega Evolution)
            if ab not in legal and not is_allowed(allow, t, mon.species, ab):
                rep.err(where, "%s cannot have ability %s (has %s)"
                        % (data["name"], ab, "/".join(sorted(legal))))
    if "AbilityIndex" in mon.props:
        v = mon.props["AbilityIndex"][0]
        if not v.isdigit() or int(v) > 5:
            rep.err(where, "AbilityIndex must be 0-5")
    # item
    if "Item" in mon.props:
        it = mon.props["Item"][0]
        if it not in ref.items:
            rep.err(where, "unknown item %s" % it)
        elif it in ref.mega_stones:
            msp, mform = ref.mega_stones[it]
            if msp != mon.species:
                rep.err(where, "%s is a Mega Stone for %s, not %s" % (it, msp, mon.species))
            elif not megaring_items:
                rep.warn(where, "holds %s but trainer Items has no MegaRing-flagged item -> cannot Mega Evolve" % it)
    # nature
    if "Nature" in mon.props and mon.props["Nature"][0] not in NATURES:
        rep.err(where, "unknown nature %s" % mon.props["Nature"][0])
    elif "Nature" not in mon.props:
        rep.warn(where, "no Nature (random-but-fixed will be used)")
    if "Gender" in mon.props and mon.props["Gender"][0] not in GENDERS:
        rep.err(where, "bad Gender %r" % mon.props["Gender"][0])
    for k, lim, tot in (("IV", 31, None), ("EV", 252, 510)):
        if k in mon.props:
            vals = csv(mon.props[k][0])
            if not all(v.isdigit() for v in vals) or not (1 <= len(vals) <= 6):
                rep.err(where, "%s must be 1-6 integers" % k)
                continue
            vals = [int(v) for v in vals]
            if len(vals) < 6:
                vals = vals + [vals[0]] * (6 - len(vals))
            if any(v > lim for v in vals):
                rep.err(where, "%s value above %d" % (k, lim))
            if tot and sum(vals) > tot:
                rep.err(where, "%s total %d > %d" % (k, sum(vals), tot))
    if "Happiness" in mon.props:
        v = mon.props["Happiness"][0]
        if not v.isdigit() or int(v) > 255:
            rep.err(where, "Happiness must be 0-255")
    for k in ("Shiny", "SuperShiny", "Shadow"):
        if k in mon.props and mon.props[k][0].lower() not in ("true", "false", "yes", "no", "y", "n", "1", "0"):
            rep.err(where, "%s must be boolean" % k)
    if "Ball" in mon.props:
        b = mon.props["Ball"][0]
        if b not in ref.items or "PokeBall" not in ref.items[b]["flags"]:
            rep.err(where, "%s is not a Poke Ball" % b)


def stage_of(species):
    for line in (GRASS_LINE, FIRE_LINE, WATER_LINE):
        if species in line:
            return line.index(species)
    return None


def validate_scheme(trainers, types, rep):
    by_key = {}
    for t in trainers:
        by_key[t.key] = t

    def need(key, why):
        if key not in by_key:
            rep.err("scheme", "missing %s %s" % ("[%s,%s,%d]" % key, why))
            return None
        return by_key[key]

    # Wardens
    for gym, (tt, nm, cap) in WARDENS.items():
        if tt not in types:
            rep.err("scheme", "trainer type %s missing from trainer_types.txt" % tt)
        bases = [0] if tt != "LEADER_JUNO" else [30, 31, 32]
        for b in bases:
            for d in (0, 1, 2):
                t = need((tt, nm, b + 100 * d), "(Gym %d %s)" % (gym, DIFF_NAMES[d]))
                if not t:
                    continue
                top = max(m.level for m in t.mons)
                if top > cap:
                    rep.err(t.label(), "level %d exceeds Gym %d cap %d" % (top, gym, cap))
                if d in (0, 1) and top != cap:
                    rep.warn(t.label(), "ace is L%d, expected L%d (cap)" % (top, cap))
    # Rivals
    for (tt, num), (nm, cap) in RIVAL_BATTLES.items():
        if tt not in types:
            rep.err("scheme", "trainer type %s missing from trainer_types.txt" % tt)
        stages = {}
        for slot in (0, 1, 2):
            for d in (0, 1, 2):
                v = num * 10 + slot + 100 * d
                t = need((tt, nm, v), "(rival battle %s%d slot %d %s)"
                         % (nm[0], num, slot, DIFF_NAMES[d]))
                if not t:
                    continue
                want = RIVAL_STARTER[tt][slot]
                starters = [m for m in t.mons if stage_of(m.species) is not None]
                if len(starters) != 1:
                    rep.err(t.label(), "must contain exactly one Gen 1 starter-line Pokemon (found %d)"
                            % len(starters))
                elif starters[0].species not in want:
                    rep.err(t.label(), "starter slot %d needs the %s line, found %s"
                            % (slot, want[0], starters[0].species))
                else:
                    stages.setdefault(d, set()).add(stage_of(starters[0].species))
                top = max(m.level for m in t.mons)
                if top > cap:
                    rep.err(t.label(), "level %d exceeds expected max %d" % (top, cap))
        for d, st in stages.items():
            if len(st) > 1:
                rep.warn("scheme", "%s%d %s: starter evolution stage differs between slots %s"
                         % (nm[0], num, DIFF_NAMES[d], sorted(st)))
    # Festival / single bosses
    for tt, nm, lo, hi in SINGLE_BOSSES:
        if tt not in types:
            rep.err("scheme", "trainer type %s missing from trainer_types.txt" % tt)
        for d in (0, 1, 2):
            t = need((tt, nm, 100 * d), "(%s)" % DIFF_NAMES[d])
            if not t:
                continue
            top = max(m.level for m in t.mons)
            if d != 2 and not (lo <= top <= hi):
                rep.warn(t.label(), "ace level %d outside expected %d-%d" % (top, lo, hi))
    # Cameos (design/CAMEOS.md, SPINE Rev 4): optional sidequest fights. v1 = sidequest at its
    # placement level, v2 = post-game rematch at 100; every base needs +100/+200.
    cameo_names = sorted({(t.ttype, t.name) for t in trainers if t.ttype.startswith("FESTIVAL_")})
    for tt, nm in cameo_names:
        if tt not in types:
            rep.err("scheme", "trainer type %s missing from trainer_types.txt" % tt)
        bases = sorted({t.version % 100 for t in trainers if (t.ttype, t.name) == (tt, nm)})
        want = CAMEO_PLACEMENT.get(tt)
        if want is None:
            rep.warn("scheme", "cameo %s has no placement in the validator's CAMEO_PLACEMENT table" % tt)
            continue
        for b in sorted(set(bases) | set(want)):
            if b not in want:
                rep.warn("scheme", "cameo [%s,%s,%d] is not a version listed in CAMEOS.md" % (tt, nm, b))
                continue
            for d in (0, 1, 2):
                t = need((tt, nm, b + 100 * d), "(cameo %s)" % DIFF_NAMES[d])
                if t and d != 2:
                    top = max(m.level for m in t.mons)
                    if top != want[b]:
                        rep.warn(t.label(), "cameo ace level %d, CAMEOS.md placement says %d" % (top, want[b]))
    # Every Prismfall (non-stock) base version must have its Hard and Casual variants
    for t in trainers:
        if t.version < 100 and t.ttype in types:
            for d in (1, 2):
                if (t.ttype, t.name, t.version + 100 * d) not in by_key:
                    rep.warn(t.label(), "no %s variant (v+%d); Core falls back to Standard" % (DIFF_NAMES[d], 100 * d))
    # Every trainer: variants of any version must have a base
    for t in trainers:
        if t.version >= 100:
            base = (t.ttype, t.name, t.version % 100)
            if base not in by_key:
                rep.err(t.label(), "difficulty variant without a Standard base version %d" % base[2])


def validate(args):
    rep = Report()
    ref = RefData(args.ref)
    types = validate_trainer_types(os.path.join(args.pbs, "trainer_types.txt"), ref, rep)
    all_types = set(types) | ref.ref_trainer_types
    tpath = os.path.join(args.pbs, "trainers.txt")
    if not os.path.exists(tpath):
        rep.err("trainers.txt", "file not found: %s" % tpath)
        return rep, [], ref, types
    trainers = parse_trainers(tpath, rep)
    allow = load_allowlist(args.balance)
    seen = {}
    megaring = {i for i, d in ref.items.items() if "MegaRing" in d["flags"]}
    for t in trainers:
        where = "trainers.txt:%d %s" % (t.line, t.label())
        if t.key in seen:
            rep.err(where, "duplicate trainer (first at line %d)" % seen[t.key])
        seen[t.key] = t.line
        if t.ttype not in all_types:
            rep.err(where, "unknown trainer type %s" % t.ttype)
        if t.key in ref.ref_trainers:
            rep.warn(where, "also defined in the base trainers.txt; ours usually wins (trainers_prismfall.txt sorts after it) but Dir.glob order is not guaranteed - rename or drop the base entry to be safe")
        if not t.mons:
            rep.err(where, "no Pokemon")
        if len(t.mons) > 6:
            rep.err(where, "more than 6 Pokemon")
        if t.lose_text is None:
            rep.warn(where, "no LoseText")
        for it in t.items:
            if it not in ref.items:
                rep.err(where, "unknown trainer item %s" % it)
        has_ring = any(i in megaring for i in t.items)
        species_seen = set()
        megas = 0
        for mon in t.mons:
            validate_mon(t, mon, ref, rep, allow, has_ring)
            if mon.species in species_seen:
                rep.warn(where, "duplicate species %s" % mon.species)
            species_seen.add(mon.species)
            if "Item" in mon.props and mon.props["Item"][0] in ref.mega_stones:
                megas += 1
        if megas > 1:
            rep.warn(where, "%d Mega Stones on one team (only one can Mega Evolve)" % megas)
    # allowlist sanity: every allowlisted move must actually be used
    used = set()
    for t in trainers:
        for mon in t.mons:
            if "Moves" in mon.props:
                for m in csv(mon.props["Moves"][0]):
                    used.add((t.ttype, t.name, t.version, mon.species, m))
            if "Ability" in mon.props:
                used.add((t.ttype, t.name, t.version, mon.species, mon.props["Ability"][0]))
    used |= {(a[0], a[1], "*", a[3], a[4]) for a in used}
    for a in sorted(allow - used, key=str):
        rep.warn("BALANCE.md allowlist", "entry not used by any trainer: %s" % (a,))
    validate_scheme(trainers, types, rep)
    return rep, trainers, ref, types


def check_maps(maps_dir, trainers, rep):
    """Scans Map*.rxdata event script strings (bytes only, never deserialized) for
    TrainerBattle.start(:TYPE, "Name"[, v]), [:TYPE, "Name"] arrays and
    Prismfall.rival_battle(:TYPE, "Name", N)."""
    keys = {t.key for t in trainers}
    names = {(t.ttype, t.name) for t in trainers}
    pat_start = re.compile(rb'TrainerBattle\.start\(([^)]{0,200})\)')
    pat_pair = re.compile(rb':([A-Z][A-Z0-9_]+), *"([^"]+)"(?:, *(\d+))?')
    pat_arr = re.compile(rb'\[:([A-Z][A-Z0-9_]+), *"([^"]+)"\]')
    pat_rival = re.compile(rb'rival_battle\(:([A-Z][A-Z0-9_]+), *"([^"]+)", *(\d+)')
    n = 0
    for fn in sorted(os.listdir(maps_dir)):
        if not re.match(r"Map\d+\.rxdata$", fn):
            continue
        data = open(os.path.join(maps_dir, fn), "rb").read()
        found = []
        for m in pat_start.finditer(data):
            for p in pat_pair.finditer(m.group(1)):
                found.append((p.group(1).decode(), p.group(2).decode("utf-8", "replace"),
                              int(p.group(3)) if p.group(3) else 0))
        for p in pat_arr.finditer(data):
            found.append((p.group(1).decode(), p.group(2).decode("utf-8", "replace"), 0))
        for p in pat_rival.finditer(data):
            for slot in (0, 1, 2):
                found.append((p.group(1).decode(), p.group(2).decode("utf-8", "replace"),
                              int(p.group(3)) * 10 + slot))
        for k in sorted(set(found)):
            n += 1
            if k not in keys:
                if k[2] == 0 and (k[0], k[1]) in names:
                    rep.warn(fn, "event uses %s,%s with no version 0" % k[:2])
                else:
                    rep.err(fn, "event battles [%s,%s,%d] which is not in trainers.txt" % k)
    return n


def print_summary(trainers, ref):
    for t in trainers:
        print("%s  (%d mons) items=%s" % (t.label(), len(t.mons), ",".join(t.items) or "-"))
        for m in t.mons:
            p = {k: v[0] for k, v in m.props.items()}
            print("   L%-3d %-12s %-14s %-12s %-8s %s" % (
                m.level, m.species, p.get("Ability", "-"), p.get("Item", "-"),
                p.get("Nature", "-"), p.get("Moves", "-")))


def show_learnset(ref, spec, level):
    parts = spec.upper().split(",")
    sp = parts[0]
    form = int(parts[1]) if len(parts) > 1 else 0
    data = ref.get_form(sp, form)
    if not data:
        print("unknown species", spec)
        return 1
    print("%s %s types=%s abilities=%s hidden=%s gen=%d" % (
        data["name"], data["formname"], "/".join(data["types"]), "/".join(data["abilities"]),
        "/".join(data["hidden"]), data["generation"]))
    fam = ref.family(sp, form)
    print("family:", " <- ".join(e["name"] for e in fam))
    moves = ref.all_learnable(sp, form, level)
    groups = defaultdict(list)
    for m, how in sorted(moves.items()):
        info = ref.move_info.get(m, {})
        groups[info.get("type", "?")].append("%s[%s %s %s]" % (m, info.get("cat", "?")[:2],
                                                              info.get("power", "?"), how))
    for ty in sorted(groups):
        print("  %-9s %s" % (ty, "  ".join(groups[ty])))
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ref", default=DEFAULT_REF)
    ap.add_argument("--pbs", default=DEFAULT_PBS)
    ap.add_argument("--balance", default=DEFAULT_BALANCE)
    ap.add_argument("--summary", action="store_true")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--quiet-warnings", action="store_true")
    ap.add_argument("--learnset", nargs="+", metavar=("SPECIES[,FORM]", "LEVEL"))
    ap.add_argument("--maps", metavar="DIR", help="folder of Map*.rxdata to cross-check")
    args = ap.parse_args()
    if args.learnset:
        ref = RefData(args.ref)
        lvl = int(args.learnset[1]) if len(args.learnset) > 1 else MAX_LEVEL
        return show_learnset(ref, args.learnset[0], lvl)
    rep, trainers, ref, types = validate(args)
    if args.maps:
        print("Map trainer references checked: %d" % check_maps(args.maps, trainers, rep))
    if args.summary:
        print_summary(trainers, ref)
    gens = sorted({d["generation"] for d in ref.species.values() if d["form"] == 0})
    print("Reference species: %d (generations %s)" % (
        sum(1 for d in ref.species.values() if d["form"] == 0), ",".join(map(str, gens))))
    print("Trainer types: %d   Trainers: %d   Pokemon: %d" % (
        len(types), len(trainers), sum(len(t.mons) for t in trainers)))
    if not args.quiet_warnings:
        for w in rep.warnings:
            print("WARNING " + w)
    for e in rep.errors:
        print("ERROR   " + e)
    print("%d error(s), %d warning(s)" % (len(rep.errors), len(rep.warnings)))
    if rep.errors or (args.strict and rep.warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
