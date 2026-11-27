#!/usr/bin/env python3
"""check_map_events: static checks of the map specs' events against the code and data they call.

    python3 -I tools/check_map_events.py [SPEC.yaml | MAP_ID ...] [--range A..B] [--strict] [--list KIND] [--quiet]

With no spec arguments every mapgen/specs/*.yaml is checked; `--range 5f233ad2..d543a354` checks only the specs that
`git diff --name-only A B -- mapgen/specs` lists (a reviewing pass over someone else's commits). Nothing is built or
executed: the specs are read as YAML, the Ruby the events run is read as text.

Kinds (one line per finding: LEVEL kind map NNN "event": message):
  trainer   every trainer an event battles exists in PBS with every version it asks for: trainer events, and in
            scripts TrainerBattle.start / pbTrainerBattle (pairs and [:T, "N", v] arrays), Prismfall.cameo_battle,
            Prismfall.rival_battle (n*10 + slot 0-2), Prismfall.gym_battle(n | pfm_gym(:LEADER_X)) through Core's
            GYMS table, pbRegisterPartner; pbTrainerIntro(:T) types. Missing Hard (+100) / Casual (+200): WARN
            (Core falls back to the Standard team).
  method    every method a script calls with no receiver (foo(...), and bare pbXxx / pf_xxx / pfm_xxx) and every
            Const.meth / Const::Const is defined somewhere in plugins/, maps_out/Plugins/, mapgen/ruby/, Essentials
            (--essentials, read only) or the base project's third-party plugins (--base/Plugins, read only).
  item / species / move   ids the events hand out, battle or test exist in PBS (base + Gen 9 pack + ours).
            pfm_item / pfm_has? / pfm_take of an id with no PBS entry is a story item (INFO).
  flag      switch / variable NAMES resolve (design/FLAGS.md, mapgen/flags.yaml) and numeric ids don't collide:
            ERROR when a numeric id is registered to (or used by) another area with another meaning; WARN when a
            puzzle id (>300) is used by number and not registered in flags.yaml; INFO for numeric story ids.
  registry  game over ids, narrative choice keys and values, Trials talk keys / trials / quests, event Pokémon,
            bosses and pfm_cutscene scene ids exist in the plugins' registries.
  graphic   every charset an event page shows exists (graphics/Characters, maps_out/Graphics, the base project).
  transfer  every map a transfer / warp / door sends the player to exists (a spec, a built map or a base map).
  ruby      every script block and script condition compiles (ruby, as a method body).
Exit status 1 on errors (and on warnings with --strict)."""
import argparse, collections, glob, json, os, re, subprocess, sys, tempfile
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPECS = os.path.join(ROOT, 'mapgen', 'specs')
DEF_ESS = '/home/claude/run/Data/Scripts'
DEF_BASE = '/home/claude/ref/ebdx_renovation'

RUBY_KEYWORDS = set('''if unless while until for in do end case when then else elsif begin rescue ensure return break
next redo retry yield super self nil true false and or not def class module alias undef defined? lambda proc loop
__method__ raise puts print p format sprintf rand srand sleep catch throw block_given? require require_relative
Integer Float String Array Hash Rational Complex exit abort at_exit binding caller freeze frozen? dup clone
attr_accessor attr_reader attr_writer private public protected include extend instance_variable_get
instance_variable_set respond_to? send public_send method is_a? kind_of? nil? tap then itself pp warn
open printf putc gets'''.split())
# RGSS / Ruby constants that are the engine's or the language's own (no def in any script file).
RGSS = set('''Graphics Input Audio Sprite Bitmap Viewport Color Tone Rect Table Plane Window Font RPG Kernel Math Time
File FileTest Dir Struct Object Marshal Zlib System ObjectSpace GC Process Comparable Enumerable Integer Float
String Array Hash Symbol Range Proc NilClass TrueClass FalseClass Exception StandardError RuntimeError
ArgumentError NameError NoMethodError IOError Errno Thread Mutex Random Regexp MatchData Numeric JSON
Encoding IO StringIO Set Rational Complex Fiber Method TypeError ZeroDivisionError'''.split())


# ------------------------------------------------------------------------------------------------ reference data
def rb_files(*dirs):
    out = []
    for d in dirs:
        if d and os.path.isdir(d):
            out += glob.glob(os.path.join(d, '**', '*.rb'), recursive=True)
    return sorted(out)


def read(path):
    with open(path, encoding='utf-8', errors='replace') as f:
        return f.read()


class Ruby:
    """Names defined in a body of Ruby (read as text, never run)."""
    DEF = re.compile(r'^\s*def\s+(?:self\.|[A-Z]\w*(?:::[A-Z]\w*)*\.)?([A-Za-z_]\w*[?!=]?)', re.M)
    ALIAS = re.compile(r'^\s*alias(?:_method)?\s+:?([A-Za-z_]\w*[?!]?)', re.M)
    ATTR = re.compile(r'^\s*(?:attr_reader|attr_accessor|attr_writer|cattr_accessor|mattr_accessor|attr)\s+(.+)$', re.M)
    DEFM = re.compile(r'define_(?:singleton_)?method\(?\s*:([A-Za-z_]\w*[?!]?)')
    CONST = re.compile(r'^\s*(?:module|class)\s+(?:[A-Z]\w*::)*([A-Z]\w*)|^\s*([A-Z][A-Za-z0-9_]*)\s*=[^=~]', re.M)

    def __init__(self, files):
        self.methods, self.consts = set(), set()
        for f in files:
            t = read(f)
            self.methods.update(self.DEF.findall(t))
            self.methods.update(self.ALIAS.findall(t))
            self.methods.update(self.DEFM.findall(t))
            for line in self.ATTR.findall(t):
                self.methods.update(re.findall(r':([A-Za-z_]\w*)', line))
            for a, b in self.CONST.findall(t):
                self.consts.add(a or b)
        # attr_writer / accessors also answer to name=
        self.methods.update(m.rstrip('=') for m in list(self.methods))


def pbs_ids(files):
    ids = set()
    for f in files:
        for line in open(f, encoding='utf-8-sig', errors='replace'):
            m = re.match(r'\[([A-Z0-9_]+)(?:,\s*\d+)?\]\s*$', line.strip())
            if m: ids.add(m.group(1))
    return ids


def pbs_files(dirs, base):
    out = []
    for d in dirs:
        if d and os.path.isdir(d):
            out += glob.glob(os.path.join(d, base + '.txt')) + glob.glob(os.path.join(d, base + '_*.txt'))
    return sorted(set(out))


def read_trainers(files):
    keys = set()
    for f in files:
        for line in open(f, encoding='utf-8-sig', errors='replace'):
            m = re.match(r'\[([A-Z0-9_]+),([^,\]]+)(?:,(\d+))?\]\s*$', line.strip())
            if m: keys.add((m.group(1), m.group(2), int(m.group(3) or 0)))
    return keys


def read_gyms(core):
    gyms = {}
    for f in glob.glob(os.path.join(core, '*.rb')):
        for line in open(f, encoding='utf-8'):
            m = re.search(r'index:\s*(\d+).*?trainer_name:\s*"([^"]+)".*?trainer_type:\s*:([A-Z0-9_]+)', line)
            if not m: continue
            ver = re.search(r'\bversion:\s*(\d+)', line)
            rival = re.search(r'rival_battle:\s*(\d+)', line)
            gyms[int(m.group(1))] = (m.group(3), m.group(2), int(ver.group(1)) if ver else 0, int(rival.group(1)) if rival else None)
    return gyms


def read_flags():
    """-> {('S'|'V', id): [(name, source)]}, {kind: {name: id}}"""
    by_id, by_name = collections.defaultdict(list), {'switches': {}, 'variables': {}}
    fy = yaml.safe_load(open(os.path.join(ROOT, 'mapgen', 'flags.yaml')))
    for kind, k in (('switches', 'S'), ('variables', 'V')):
        for name, i in (fy.get(kind) or {}).items():
            by_id[(k, int(i))].append((name, 'flags.yaml')); by_name[kind][name] = int(i)
    md = os.path.join(ROOT, 'design', 'FLAGS.md')
    for line in open(md, encoding='utf-8'):
        m = re.match(r'\|\s*([SV])(\d+)\s*\|\s*([^|]*)\|', line)
        if not m: continue
        kind = 'switches' if m.group(1) == 'S' else 'variables'
        cell = m.group(3).strip()
        bare = re.match(r'([A-Z][A-Z0-9_]+)$', cell)
        tick = re.search(r'`([A-Z][A-Z0-9_]+)`', cell)
        name = bare.group(1) if bare else (tick.group(1) if tick else cell[:40])
        by_id[(m.group(1), int(m.group(2)))].append((name, 'FLAGS.md'))
        if bare: by_name[kind][name] = int(m.group(2))      # build.py resolves only the bare-name rows
    return by_id, by_name


def registries(plugins, maps_plugins):
    core = os.path.join(plugins, 'Prismfall Core')
    trials = os.path.join(plugins, 'Prismfall Trials')
    all_rb = rb_files(plugins, maps_plugins)
    text = {f: read(f) for f in all_rb}
    R = {}
    nd = read(os.path.join(core, '012_Narrative_Data.rb'))
    def block(src, name):
        i = src.find(name + ' = {')
        if i < 0: return ''
        j, depth = src.index('{', i), 0
        for k in range(j, len(src)):
            if src[k] == '{': depth += 1
            elif src[k] == '}':
                depth -= 1
                if depth == 0: return src[j:k + 1]
        return src[j:]
    R['game_over'] = set(re.findall(r':(GO_[A-Z0-9_]+)\s*=>', block(nd, 'GAME_OVERS') + block(nd, 'GAME_OVER_ALIASES')))
    choices = {}
    for f, t in text.items():
        if 'Prismfall Core' not in f: continue
        for k, vals in re.findall(r'^\s*:([a-z][a-z0-9_]*)\s*=>\s*\{\s*:values\s*=>\s*\[([^\]]*)\]', t, re.M):
            choices[k] = set(re.findall(r':([a-z0-9_]+)', vals))
    for a, b in re.findall(r':([A-Z0-9_]+)\s*=>\s*:([a-z0-9_]+)', block(nd, 'CHOICE_ALIASES')):
        if b in choices: choices[a] = choices[b]
    R['choice'] = choices
    R['talk'], R['quest'], R['eventmon'] = set(), set(), set()
    for f, t in text.items():
        if os.path.dirname(f) != trials and 'Prismfall Trials' not in f: continue
        R['talk'].update(re.findall(r'^\s*:([A-Z][A-Z0-9_]*)\s*=>\s*\{\s*(?::board|:rows)', t, re.M))
        R['quest'].update(re.findall(r'\.quest\(\s*:([A-Z][A-Z0-9_]*)', t))
        R['eventmon'].update(re.findall(r'(?:\b[a-z_]+|EventMons)\.(?:register|call)\(\s*:([A-Z][A-Z0-9_]*)\s*,\s*\{', t))
    tc = read(os.path.join(trials, '001_Trials_Config.rb'))
    R['trial'] = set(re.findall(r'^\s{6}:([A-Z][A-Z0-9_]*)\s*=>\s*\{', block(tc, 'TRIALS'), re.M))
    R['boss'] = set()
    for f, t in text.items():
        R['boss'].update(re.findall(r'Bosses\.register(?:_trainer_boss)?\(\s*:([A-Z][A-Z0-9_]*)', t))
    mv = read(os.path.join(plugins, 'Prismfall Cutscenes', '016_Movies.rb'))
    sc = block(mv, 'SCENES') + block(mv, 'CUTSCENE_SCENES')
    R['scene'] = set(re.findall(r'^\s*:([A-Z][A-Z0-9_]*)\s*=>', sc, re.M)) | set(re.findall(r':([A-Z][A-Z0-9_]*)', ' '.join(re.findall(r':aliases\s*=>\s*\[([^\]]*)\]', sc))))
    return R


# ------------------------------------------------------------------------------------------------ the specs
def spec_docs(path):
    head = open(path, encoding='utf-8').readline()
    m = re.search(r'(?:WRITTEN BY|GENERATED by)\s+(?:mapgen/)?layouts/([\w.]+)', head) or re.search(r'by ([\w.]+\.py)', head)
    owner = m.group(1) if m else os.path.basename(path)
    for d in yaml.safe_load_all(open(path, encoding='utf-8')):
        if d and 'id' in d: yield d, owner


class Uses:
    def __init__(self):
        self.items = []          # (kind, payload, where)

    def add(self, kind, payload, where, guards=frozenset()): self.items.append((kind, payload, where, guards))


def walk_cmds(cmds, U, where, guards=frozenset()):
    """guards: maps an enclosing `if pbRgssExists?("Data/MapNNN.rxdata")` proves built (a transfer there is safe)"""
    for c in cmds or []:
        if isinstance(c, str): U.add('text', c, where); continue
        if not isinstance(c, dict): continue
        if 'if' in c: U.add('cond', str(c['if']), where, guards)
        if 'if_switch' in c: U.add('switch', c['if_switch'][0], where)
        if 'if_var' in c: U.add('var', c['if_var'][0], where)
        g = guards | {int(x) for x in P_GUARD.findall(str(c['if']))} | set(P_IGUARD.findall(str(c['if']))) if 'if' in c else guards
        if 'then' in c: walk_cmds(c['then'], U, where, g)
        if 'else' in c: walk_cmds(c['else'], U, where, guards)
        if 'branches' in c:
            for b in c['branches']: walk_cmds(b, U, where, guards)
        if 'choices' in c or 'if' in c or 'if_switch' in c or 'if_var' in c: continue
        if len(c) != 1: continue
        (k, v), = c.items()
        if k == 'text': U.add('text', str(v), where)
        elif k == 'script': U.add('script', str(v), where, guards)
        elif k == 'switch': U.add('switch', v[0], where)
        elif k == 'var': U.add('var', v[0], where)
        elif k == 'transfer': U.add('transfer', v.get('map'), where, guards)
        elif k == 'boss': U.add('boss', v, where)
        elif k == 'move': walk_route(v.get('route'), U, where)
        elif k == 'raw' and isinstance(v, list) and len(v) > 1:
            code, params = v[0], v[1]
            if code in (355, 655) and params: U.add('script', str(params[0]), where, guards)
            elif code == 111 and params and params[0] == 12: U.add('cond', str(params[1]), where, guards)
            elif code in (101, 401) and params: U.add('text', str(params[0]), where)
            elif code == 201 and len(params) > 1 and params[0] == 0: U.add('transfer', params[1], where, guards)


def walk_route(route, U, where):
    for r in route or []:
        if not isinstance(r, dict): continue
        for k, v in r.items():
            if k == 'script': U.add('script', str(v), where)
            elif k in ('switch_on', 'switch_off'): U.add('switch', v, where)
            elif k == 'graphic' and v: U.add('graphic', v[0] if isinstance(v, list) else v, where)


def walk_cond(c, U, where):
    if not c: return
    if c.get('switch') is not None: U.add('switch', c['switch'], where)
    if c.get('switch2') is not None: U.add('switch', c['switch2'], where)
    if c.get('var'): U.add('var', c['var'][0], where)


def walk_event(e, U, mid):
    name = e.get('name') or e.get('type')
    where = (mid, name)
    t = e.get('type')
    walk_cond(e.get('cond'), U, where)
    if t == 'trainer':
        tr = e['trainer']
        U.add('trainer', (tr[0], str(tr[1]), int(tr[2]) if len(tr) > 2 else 0, 'trainer event'), where)
        U.add('graphic', e.get('sprite', 'trainer_' + tr[0]), where)
        for r in e.get('rules') or []: U.add('script', str(r), where)
        U.add('script', 'pbTrainerIntro(:%s)' % tr[0], where)
    elif t == 'item':
        U.add('item', (e['item'], 'item ball'), where)
    elif t == 'mart':
        for i in e.get('items', []): U.add('item', (i, 'mart'), where)
    elif t == 'berry':
        U.add('item', (e['berry'], 'berry'), where)
    elif t in ('npc', 'sign'):
        walk_cmds(e.get('commands') or [{'text': e.get('text', '')}], U, where)
        if t == 'npc' and e.get('sprite'): U.add('graphic', e['sprite'], where)
    elif t == 'door':
        if e.get('gfx'): U.add('graphic', e['gfx'][0], where)
        if e.get('to'): U.add('transfer', e['to'].get('map'), where)
        if e.get('locked'):
            U.add('switch', e['locked']['until'], where)
            walk_cmds(e['locked'].get('commands'), U, where)
    elif t in ('warp', 'exit'):
        if e.get('to'): U.add('transfer', e['to'].get('map'), where)
    elif t == 'rock_smash':
        if e.get('sprite'): U.add('graphic', e['sprite'], where)
    elif t == 'event':
        for i, p in enumerate(e.get('pages') or []):
            w = (mid, '%s p%d' % (name, i + 1))
            walk_cond(p.get('cond'), U, w)
            g = p.get('graphic') or {}
            if g.get('sprite'): U.add('graphic', g['sprite'], w)
            walk_route(p.get('route'), U, w)
            walk_cmds(p.get('commands'), U, w)


# ------------------------------------------------------------------------------------------------ Ruby text analysis
def strip_ruby(src):
    """Drop string contents (keeping #{...} code) and comments; symbols stay (:FOO)."""
    out, i, n = [], 0, len(src)
    while i < n:
        ch = src[i]
        if ch == '#' and not src.startswith('#{', i):
            j = src.find('\n', i); i = n if j < 0 else j; continue
        if ch in '"\'':
            q, j = ch, i + 1
            out.append('""')
            while j < n and src[j] != q:
                if src[j] == '\\': j += 2; continue
                if q == '"' and src.startswith('#{', j):
                    depth, k = 1, j + 2
                    while k < n and depth:
                        if src[k] == '{': depth += 1
                        elif src[k] == '}': depth -= 1
                        k += 1
                    out.append(' ' + src[j + 2:k - 1] + ' '); j = k; continue
                j += 1
            i = j + 1; continue
        out.append(ch); i += 1
    return ''.join(out)


STR = r'"((?:[^"\\]|\\.)*)"'
P_PAIR = re.compile(r':([A-Z][A-Z0-9_]+)\s*,\s*' + STR + r'(?:\s*,\s*(\d+))?')
P_TB = re.compile(r'(?:TrainerBattle\.start\w*|pbTrainerBattle|pbDoubleTrainerBattle|cameo_battle)\s*\(')
P_RIVAL = re.compile(r'rival_battle\(\s*:([A-Z][A-Z0-9_]+)\s*,\s*' + STR + r'\s*,\s*(\d+)')
P_GYM = re.compile(r'gym_battle\(\s*(?:(\d+)|pfm_gym\(\s*:([A-Z][A-Z0-9_]+)\s*\))')
P_PARTNER = re.compile(r'pbRegisterPartner\(\s*:([A-Z][A-Z0-9_]+)\s*,\s*' + STR + r'(?:\s*,\s*(\d+))?')
P_INTRO = re.compile(r'pbTrainerIntro\(\s*:([A-Z][A-Z0-9_]+)')
ITEM_CALLS = r'pbItemBall|pbReceiveItem|pbStoreItem|pbHasItem\?|\$bag\.(?:add|has\?|remove|quantity|can_add\?)|GameData::Item\.(?:get|try_get)|pf_mega_stone|pf_z_crystal'
P_IGUARD = re.compile(r'GameData::Item\.exists\?\(\s*:([A-Z][A-Z0-9_]*)')
P_ITEM = re.compile(r'(?:' + ITEM_CALLS + r')\(\s*:([A-Z][A-Z0-9_]*)')
P_STORY_ITEM = re.compile(r'(?:pfm_item|pfm_has\?|pfm_take)\(\s*:([A-Z][A-Z0-9_]*)')
P_MART = re.compile(r'pbPokemonMart\(\s*\[([^\]]*)\]')
SPECIES_CALLS = r'pbAddPokemon(?:Silent)?|pbAddToParty(?:Silent)?|pbAddForeignPokemon|WildBattle\.start\w*|pbWildBattle|pbDoubleWildBattle|Pokemon\.new|GameData::Species\.(?:get|try_get|exists\?|get_species_form)|pbHasSpecies\?|has_species\?|pbPlayCry|Pokemon::new|pbSeenForm|register_seen|register_caught|set_seen|set_owned'
P_SPECIES = re.compile(r'(?:' + SPECIES_CALLS + r')\(\s*:([A-Z][A-Z0-9_]*)')
P_SPECIES_WB = re.compile(r'WildBattle\.start\w*\(([^)]*)\)')
MOVE_CALLS = r'hasMove\?|has_move\?|pbHasMove\?|learn_move|forget_move|pbCheckMove|pbCanUseHM\?|pbMoveTutorChoose|pbHiddenMoveAnimation|pbLearnMove\([^,()]+,\s*|GameData::Move\.(?:get|try_get|exists\?)|Pokemon::Move\.new'
P_MOVE = re.compile(r'(?:' + MOVE_CALLS + r')\(?\s*:([A-Z][A-Z0-9_]*)')
P_SWVAR = re.compile(r'\$game_(switches|variables)\[\s*(\d+)\s*\]|\bpb(Set|Get)\(\s*(\d+)')
P_ATAT = re.compile(r'@@([A-Z][A-Z0-9_]*)')
P_TEXTVAR = re.compile(r'\\[vV]\[(\d+)\]')
P_EVREF = re.compile(r'%EV\[([^\]]+)\]%')
P_TRANSFER = re.compile(r'player_new_map_id\s*=\s*(\d+)|pbTransferPlayer\w*\(\s*(\d+)|reserve_transfer\(\s*(\d+)')
REG_CALLS = [('game_over', re.compile(r'game_over\(\s*:([A-Z][A-Z0-9_]*)')),
             ('choice', re.compile(r'\bpf_choose\(\s*:([A-Za-z0-9_]+)\s*,\s*:([a-z0-9_]+)')),
             ('choice', re.compile(r'\bpf_choice\(\s*:([A-Za-z0-9_]+)\s*\)')),
             ('talk', re.compile(r'\bpf_trial_(?:talk|ready\?)\(\s*:([A-Z][A-Z0-9_]*)')),
             ('trial', re.compile(r'\bpf_trial_(?:board|keeper)\(\s*:([A-Z][A-Z0-9_]*)')),
             ('quest', re.compile(r'\bpf_quest_\w+\?\(\s*:([A-Z][A-Z0-9_]*)')),
             ('eventmon', re.compile(r'(?:pf_event_\w+|EventMons\.\w+)\(\s*:([A-Z][A-Z0-9_]*)')),
             ('boss', re.compile(r'Bosses\.(?:wild_battle|exists\?|get)\(\s*:([A-Z][A-Z0-9_]*)')),
             ('scene', re.compile(r'(?:pfm_cutscene|Cutscene\.play_scene)\(\s*:([A-Z][A-Z0-9_]*)'))]
P_BARE_CALL = re.compile(r'(?<![.\w:$@?!])([a-z_][A-Za-z0-9_]*[?!]?)\s*\(')
P_BARE_PREFIX = re.compile(r'(?<![.\w:$@])((?:pb[A-Z]|pfm?_)[A-Za-z0-9_]*[?!]?)(?![\w(?!])')
P_CONST_CALL = re.compile(r'(?<![\w:$@])((?:[A-Z]\w*::)*[A-Z]\w*)\.([a-z_][A-Za-z0-9_]*[?!]?)')
P_CONST_PATH = re.compile(r'(?<![\w:.$@])([A-Z]\w*(?:::[A-Z]\w*)+)')
P_GUARD = re.compile(r'(?:pbRgssExists\?|FileTest\.exist\?|File\.exist\?|safeExists\?)\(\s*"Data/Map0*(\d+)\.rxdata"\s*\)')
OBJECT_METHODS = {'new', 'class', 'name', 'constants', 'const_get', 'const_defined?', 'instance_methods',
                  'method_defined?', 'respond_to?', 'send', 'public_send', 'is_a?', 'nil?', 'instance_variable_get',
                  'instance_variable_set', 'instance_variable_defined?', 'freeze', 'frozen?', 'inspect', 'to_s',
                  'methods', 'singleton_class', 'module_eval', 'class_eval', 'define_method', 'private_method_defined?'}


def locals_of(code):
    names = set(re.findall(r'(?<![.\w:$@])([a-z_]\w*)\s*(?:=(?![=~>])|\+=|-=|\|\|=)', code))
    for blk in re.findall(r'\|([^|]*)\|', code): names.update(re.findall(r'[a-z_]\w*', blk))
    names.update(re.findall(r'\bfor\s+([a-z_]\w*)', code))
    names.update(re.findall(r'\brescue\s*(?:[A-Z]\w*\s*)?=>\s*([a-z_]\w*)', code))
    return names


# ------------------------------------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('specs', nargs='*', help='spec files or map ids (default: every spec)')
    ap.add_argument('--range', help='A..B: only the specs git diff --name-only A B -- mapgen/specs lists')
    ap.add_argument('--essentials', default=DEF_ESS, help='Essentials v21.1 scripts folder (*.rb), read only')
    ap.add_argument('--base', default=DEF_BASE, help='the base project (PBS/, Plugins/, Graphics/, Data/), read only')
    ap.add_argument('--strict', action='store_true', help='warnings count as errors')
    ap.add_argument('--list', default='', help='comma list of kinds to print in full (default: errors and warnings of all kinds)')
    ap.add_argument('--info', action='store_true', help='print INFO lines too')
    ap.add_argument('--quiet', action='store_true', help='counts only')
    ap.add_argument('--no-ruby', action='store_true', help='skip the ruby syntax pass')
    a = ap.parse_args()

    files = []
    if a.range:
        x, y = a.range.split('..')
        out = subprocess.check_output(['git', '-C', ROOT, 'diff', '--name-only', x, y, '--', 'mapgen/specs'], text=True)
        files = [os.path.join(ROOT, f) for f in out.split() if f.endswith('.yaml')]
        files = [f for f in files if os.path.exists(f)]
    want_ids = set()
    for s in a.specs:
        if s.isdigit(): want_ids.add(int(s))
        else: files.append(os.path.abspath(s))
    all_files = sorted(glob.glob(os.path.join(SPECS, '*.yaml')))
    if not files: files = all_files

    plugins, maps_plugins, mruby = os.path.join(ROOT, 'plugins'), os.path.join(ROOT, 'maps_out', 'Plugins'), os.path.join(ROOT, 'mapgen', 'ruby')
    base_plugins = os.path.join(a.base, 'Plugins')
    rb = Ruby(rb_files(plugins, maps_plugins, mruby, a.essentials, base_plugins))
    pbs_dirs = [os.path.join(ROOT, 'pbs'), os.path.join(a.base, 'PBS')]
    items = pbs_ids(pbs_files(pbs_dirs, 'items'))
    species = pbs_ids(pbs_files(pbs_dirs, 'pokemon') + pbs_files(pbs_dirs, 'pokemon_base'))
    moves = pbs_ids(pbs_files(pbs_dirs, 'moves'))
    ours = read_trainers(pbs_files([os.path.join(ROOT, 'pbs'), os.path.join(ROOT, 'maps_out', 'PBS')], 'trainers'))
    stock = read_trainers(pbs_files([os.path.join(a.base, 'PBS')], 'trainers'))
    ttypes = pbs_ids(pbs_files(pbs_dirs, 'trainer_types'))
    gyms = read_gyms(os.path.join(plugins, 'Prismfall Core'))
    gym_by_type = {g[0]: n for n, g in gyms.items()}
    flag_ids, flag_names = read_flags()
    R = registries(plugins, maps_plugins)
    char_dirs = [os.path.join(ROOT, 'graphics', 'Characters'), os.path.join(ROOT, 'maps_out', 'Graphics', 'Characters'),
                 os.path.join(a.base, 'Graphics', 'Characters')]
    built = {int(m) for f in glob.glob(os.path.join(ROOT, 'maps_out', 'Data', 'Map*.rxdata')) for m in re.findall(r'Map(\d+)', f)}
    built |= {int(m) for f in glob.glob(os.path.join(a.base, 'Data', 'Map*.rxdata')) for m in re.findall(r'Map(\d+)', f)}
    for missing, what in ((not os.path.isdir(a.essentials), 'Essentials scripts (--essentials)'), (not os.path.isdir(a.base), 'base project (--base)')):
        if missing: print('note: no %s: stock methods / PBS / charsets count as missing' % what)

    # every spec: map ids, owners, and every switch / variable use (the collision index)
    spec_ids, owner_of, uses_all = set(), {}, collections.defaultdict(set)
    selected = []
    for f in all_files + [f for f in files if f not in all_files]:
        for d, owner in spec_docs(f):
            spec_ids.add(d['id']); owner_of[d['id']] = owner
            U = Uses()
            for e in d.get('events') or []: walk_event(e, U, d['id'])
            for kind, payload, where, _g in U.items:
                for k, i in id_uses(kind, payload, flag_names):
                    uses_all[(k, i)].add(d['id'])
            if f in files and (not want_ids or d['id'] in want_ids):
                selected.append((f, d, owner, U))

    findings = []          # (level, kind, mid, event, msg)
    checked = collections.Counter()   # references looked at, by kind
    def F(level, kind, where, msg): findings.append((level, kind, where[0], where[1], msg))
    def C(kind, n=1): checked[kind] += n
    ruby_blocks = []
    mart_seen = set()
    for f, d, owner, U in selected:
        mid = d['id']
        ev_names = {e.get('name') for e in d.get('events') or []}
        for kind, payload, where, guards in U.items:
            C({'script': 'script', 'cond': 'script', 'switch': 'flag', 'var': 'flag', 'boss': 'species'}.get(kind, kind))
            if kind == 'trainer':
                check_trainer(payload, where, ours, stock, ttypes, F)
            elif kind == 'item':
                iid, how = payload
                if iid not in items: F('ERROR', 'item', where, ':%s (%s) is not in PBS items' % (iid, how))
            elif kind == 'graphic':
                if not graphic_exists(payload, char_dirs): F('ERROR', 'graphic', where, 'charset %r not found' % payload)
            elif kind == 'transfer':
                if payload is not None and int(payload) not in spec_ids and int(payload) not in built:
                    if int(payload) in guards: F('INFO', 'transfer', where, 'exit to unbuilt map %s, guarded by pbRgssExists?' % payload)
                    else: F('ERROR', 'transfer', where, 'sends the player to map %s, which has no spec and no built map' % payload)
            elif kind == 'boss':
                if payload.get('id') not in R['boss']: F('WARN', 'registry', where, 'boss :%s not registered (plain WildBattle fallback)' % payload.get('id'))
                if payload.get('species') not in species: F('ERROR', 'species', where, 'boss species :%s not in PBS' % payload.get('species'))
            elif kind in ('switch', 'var'):
                check_flag_name(kind, payload, where, flag_names, F)
            elif kind == 'text':
                for v in P_TEXTVAR.findall(payload):
                    pass   # \v[n] reads a variable: no meaning to collide with
            elif kind in ('script', 'cond'):
                for n in P_EVREF.findall(payload):
                    if n not in ev_names: F('ERROR', 'evref', where, '%%EV[%s]%% names no event on this map (build.py fails)' % n)
                payload = P_EVREF.sub('1', payload)
                payload = P_ATAT.sub(lambda m: str(flag_names['variables'].get(m.group(1), flag_names['switches'].get(m.group(1), 0))) if (m.group(1) in flag_names['variables'] or m.group(1) in flag_names['switches']) else m.group(0), payload)
                check_script(payload, kind, where, rb, items, species, moves, ours, stock, ttypes, gyms, gym_by_type, R,
                             flag_names, spec_ids, built, F, guards)
                ruby_blocks.append((where, kind, payload))
        # numeric ids: collisions
        seen = set()
        for kind, payload, where, _g in U.items:
            for k, i in id_uses(kind, payload, flag_names, numeric_only=True):
                if (k, i, where[0]) in seen: continue
                seen.add((k, i, where[0]))
                check_collision(k, i, where, flag_ids, uses_all, owner_of, owner, F)

    if not a.no_ruby and ruby_blocks:
        ruby_syntax(ruby_blocks, F)

    # report
    lv_rank = {'ERROR': 0, 'WARN': 1, 'INFO': 2}
    show = set(k for k in a.list.split(',') if k)
    findings.sort(key=lambda r: (lv_rank[r[0]], r[1], r[2], r[3], r[4]))
    dedup = []
    for r in findings:
        if not dedup or dedup[-1] != r: dedup.append(r)
    if not a.quiet:
        for lv, kind, mid, ev, msg in dedup:
            if lv == 'INFO' and not a.info and kind not in show: continue
            if show and kind not in show and lv != 'ERROR': continue
            print('%-5s %-8s map %3d %-34s %s' % (lv, kind, mid, '"%s"' % ev[:32], msg))
    counts = collections.Counter((r[0], r[1]) for r in dedup)
    kinds = sorted({k for _, k in counts})
    print('checked %d map(s) in %d spec file(s): %d events, %d script blocks' % (
        len(selected), len({s[0] for s in selected}), sum(len(s[1].get('events') or []) for s in selected), len(ruby_blocks)))
    checked.update(SCRIPT_REFS)
    print('references: ' + ', '.join('%s %d' % kv for kv in sorted(checked.items()) if kv[0] != 'text'))
    for lv in ('ERROR', 'WARN', 'INFO'):
        parts = ['%s %d' % (k, counts[(lv, k)]) for k in kinds if counts[(lv, k)]]
        print('%-5s %d%s' % (lv, sum(counts[(lv, k)] for k in kinds), (' (' + ', '.join(parts) + ')') if parts else ''))
    errs = sum(v for (lv, _), v in counts.items() if lv == 'ERROR') + (sum(v for (lv, _), v in counts.items() if lv == 'WARN') if a.strict else 0)
    sys.exit(1 if errs else 0)


def id_uses(kind, payload, flag_names, numeric_only=False):
    """(S|V, id) pairs a use touches."""
    out = []
    if kind in ('switch', 'var'):
        k = 'S' if kind == 'switch' else 'V'
        if isinstance(payload, int): out.append((k, payload))
        elif not numeric_only and isinstance(payload, str):
            i = flag_names['switches' if k == 'S' else 'variables'].get(payload)
            if i is not None: out.append((k, i))
    elif kind in ('script', 'cond'):
        for m in P_SWVAR.finditer(payload):
            if m.group(1): out.append(('S' if m.group(1) == 'switches' else 'V', int(m.group(2))))
            else: out.append(('V', int(m.group(4))))         # pbSet / pbGet: variables
        if not numeric_only:
            for n in P_ATAT.findall(payload):
                if n in flag_names['variables']: out.append(('V', flag_names['variables'][n]))
                elif n in flag_names['switches']: out.append(('S', flag_names['switches'][n]))
    return out


def check_flag_name(kind, payload, where, flag_names, F):
    if isinstance(payload, str):
        reg = flag_names['switches' if kind == 'switch' else 'variables']
        if payload not in reg: F('ERROR', 'flag', where, 'unknown %s name %r (build.py fails)' % (kind, payload))


GLOBAL_PUZZLE = {('S', 301), ('S', 302)}


def check_collision(k, i, where, flag_ids, uses_all, owner_of, owner, F):
    regs = flag_ids.get((k, i), [])
    label = '%s%d' % (k, i)
    if i <= 100:
        F('INFO', 'flag', where, '%s by number: an Essentials / temporary id (1-100)' % label)
        return
    if 101 <= i <= 300:
        if not regs: F('ERROR', 'flag', where, '%s is a story id with no FLAGS.md row' % label)
        else: F('INFO', 'flag', where, '%s by number = %s' % (label, '/'.join(n for n, _ in regs)))
        return
    if (k, i) in GLOBAL_PUZZLE:
        return
    others = sorted({owner_of.get(m, '?') for m in uses_all.get((k, i), ()) if owner_of.get(m) != owner})
    if regs:
        F('INFO', 'flag', where, '%s by number = %s' % (label, '/'.join('%s (%s)' % r for r in regs)))
    if others:
        maps = sorted(m for m in uses_all[(k, i)] if owner_of.get(m) != owner)
        F('ERROR', 'flag', where, '%s is also used by %s (maps %s)%s' % (
            label, ', '.join(others), ', '.join(map(str, maps[:8])), (' and registered as ' + '/'.join(n for n, _ in regs)) if regs else ''))
    elif regs:
        pass
    else:
        F('WARN', 'flag', where, '%s is not registered in mapgen/flags.yaml' % label)


SCRIPT_REFS = collections.Counter()   # references found inside scripts, by kind


def check_trainer(t, where, ours, stock, ttypes, F):
    tt, name, ver, how = t
    SCRIPT_REFS['trainer'] += 1
    label = '[%s,%s%s] (%s)' % (tt, name, '' if ver == 0 else ',%d' % ver, how)
    if tt not in ttypes: F('ERROR', 'trainer', where, '%s: no such trainer type' % label); return
    if (tt, name, ver) in ours:
        if ver < 100 and 'partner' not in how:
            miss = [mode for extra, mode in ((100, 'Hard'), (200, 'Casual')) if (tt, name, ver + extra) not in ours]
            if miss: F('WARN', 'trainer', where, '%s has no %s variant' % (label, ' / '.join(miss)))
    elif (tt, name, ver) in stock:
        F('WARN', 'trainer', where, '%s is a base-project sample trainer' % label)
    else:
        F('ERROR', 'trainer', where, '%s is not in pbs/trainers*.txt' % label)


def graphic_exists(name, dirs):
    if not name: return True
    for d in dirs:
        for ext in ('.png', '.PNG', '.gif'):
            if os.path.exists(os.path.join(d, name + ext)): return True
    return False


def check_script(code, kind, where, rb, items, species, moves, ours, stock, ttypes, gyms, gym_by_type, R, flag_names,
                 spec_ids, built, F, guards=frozenset()):
    raw = code
    guards = guards | {int(x) for x in P_GUARD.findall(raw)} | set(P_IGUARD.findall(raw))
    # trainers
    for m in P_TB.finditer(raw):
        depth, j = 1, m.end()
        while j < len(raw) and depth:
            depth += {'(': 1, ')': -1}.get(raw[j], 0); j += 1
        for p in P_PAIR.finditer(raw[m.end():j]):
            check_trainer((p.group(1), p.group(2).replace('\\"', '"'), int(p.group(3) or 0), 'battle'), where, ours, stock, ttypes, F)
    for p in P_RIVAL.finditer(raw):
        for slot in (0, 1, 2):
            check_trainer((p.group(1), p.group(2), int(p.group(3)) * 10 + slot, 'rival battle %s' % p.group(3)), where, ours, stock, ttypes, F)
    for p in P_GYM.finditer(raw):
        n = int(p.group(1)) if p.group(1) else gym_by_type.get(p.group(2))
        g = gyms.get(n)
        if g is None: F('ERROR', 'trainer', where, 'gym_battle(%s): no such Warden in Core GYMS' % (p.group(1) or ':' + p.group(2))); continue
        if g[3] is not None:
            for slot in (0, 1, 2): check_trainer((g[0], g[1], g[3] * 10 + slot, 'gym %d (rival-versioned)' % n), where, ours, stock, ttypes, F)
        else:
            check_trainer((g[0], g[1], g[2], 'gym %d' % n), where, ours, stock, ttypes, F)
    for p in P_PARTNER.finditer(raw):
        check_trainer((p.group(1), p.group(2), int(p.group(3) or 0), 'partner'), where, ours, stock, ttypes, F)
    for p in P_INTRO.finditer(raw):
        if p.group(1) not in ttypes: F('ERROR', 'trainer', where, 'pbTrainerIntro(:%s): no such trainer type' % p.group(1))
    # ids
    SCRIPT_REFS['item'] += len(P_ITEM.findall(raw)) + len(P_STORY_ITEM.findall(raw))
    SCRIPT_REFS['species'] += len(P_SPECIES.findall(raw))
    SCRIPT_REFS['move'] += len(P_MOVE.findall(raw))
    SCRIPT_REFS['registry'] += sum(len(p.findall(raw)) for _, p in REG_CALLS)
    for i in P_ITEM.findall(raw):
        if i in items: continue
        if i in guards: F('INFO', 'item', where, ':%s has no PBS entry; guarded by GameData::Item.exists?' % i)
        else: F('ERROR', 'item', where, ':%s is not in PBS items' % i)
    for i in P_STORY_ITEM.findall(raw):
        if i not in items: F('INFO', 'item', where, ':%s is a story item (pfm_item, no PBS entry)' % i)
    for blk in P_MART.findall(raw):
        for i in re.findall(r':([A-Z][A-Z0-9_]*)', blk):
            if i not in items: F('ERROR', 'item', where, 'mart :%s is not in PBS items' % i)
    for s in P_SPECIES.findall(raw):
        if s not in species: F('ERROR', 'species', where, ':%s is not in PBS pokemon' % s)
    for s in P_MOVE.findall(raw):
        if s not in moves: F('ERROR', 'move', where, ':%s is not in PBS moves' % s)
    # registries
    for reg, pat in REG_CALLS:
        for m in pat.finditer(raw):
            if reg == 'choice':
                key = m.group(1)
                vals = R['choice'].get(key)
                if vals is None: F('ERROR', 'registry', where, 'narrative choice :%s is not in CHOICES' % key)
                elif m.lastindex and m.lastindex > 1 and m.group(2) not in vals:
                    F('ERROR', 'registry', where, 'pf_choose(:%s, :%s): not one of %s' % (key, m.group(2), sorted(vals)))
            elif m.group(1) not in R[reg]:
                F('ERROR', 'registry', where, '%s :%s is not registered' % (reg, m.group(1)))
    # flags
    for n in P_ATAT.findall(raw):
        if n not in flag_names['variables'] and n not in flag_names['switches']:
            F('ERROR', 'flag', where, '@@%s is not a registered switch / variable name (build.py fails)' % n)
    for m in P_TRANSFER.finditer(raw):
        t = int(next(g for g in m.groups() if g))
        if t not in spec_ids and t not in built:
            if t in guards: F('INFO', 'transfer', where, 'script exit to unbuilt map %d, guarded by pbRgssExists?' % t)
            else: F('ERROR', 'transfer', where, 'script transfer to map %d: no spec, no built map' % t)
    # methods
    s = strip_ruby(raw)
    loc = locals_of(s)
    called = set(P_BARE_CALL.findall(s)) | set(P_BARE_PREFIX.findall(s))
    SCRIPT_REFS['method'] += len(called) + len(set(P_CONST_CALL.findall(s)))
    for name in sorted(called):
        if name in RUBY_KEYWORDS or name in loc or name in rb.methods: continue
        F('ERROR', 'method', where, '%s is not defined in plugins, maps_out/Plugins, mapgen/ruby or Essentials' % name)
    for const, meth in set(P_CONST_CALL.findall(s)):
        segs = const.split('::')
        if segs[0] in RGSS: continue
        bad = [x for x in segs if x not in rb.consts and x not in RGSS]
        if bad: F('ERROR', 'method', where, '%s: constant %s is not defined' % (const, bad[0])); continue
        if meth in OBJECT_METHODS: continue
        if meth not in rb.methods: F('ERROR', 'method', where, '%s.%s is not defined' % (const, meth))
    for path in set(P_CONST_PATH.findall(s)):
        segs = path.split('::')
        if segs[0] in RGSS: continue
        bad = [x for x in segs if x not in rb.consts and x not in RGSS]
        if bad: F('ERROR', 'method', where, '%s: constant %s is not defined' % (path, bad[0]))


RUBY_CHECK = r'''
require "json"
JSON.parse(File.read(ARGV[0])).each_with_index do |(kind, code), i|
  src = kind == "cond" ? "def __pf_c\n(#{code})\nend" : "def __pf_s\n#{code}\nend"
  begin
    RubyVM::InstructionSequence.compile(src)
  rescue SyntaxError => e
    puts "#{i}\t#{e.message.lines.first(3).map(&:strip).join(' | ')}"
  end
end
'''


def ruby_syntax(blocks, F):
    with tempfile.TemporaryDirectory(prefix='cme_') as td:
        jp, rp = os.path.join(td, 'blocks.json'), os.path.join(td, 'check.rb')
        json.dump([[k, c] for _, k, c in blocks], open(jp, 'w'))
        open(rp, 'w').write(RUBY_CHECK)
        try:
            out = subprocess.run(['ruby', rp, jp], capture_output=True, text=True, timeout=300).stdout
        except (OSError, subprocess.TimeoutExpired) as e:
            print('note: ruby syntax pass skipped (%s)' % e); return
    for line in out.splitlines():
        i, msg = line.split('\t', 1)
        where, kind, _ = blocks[int(i)]
        F('ERROR', 'ruby', where, '%s block does not compile: %s' % (kind, msg[:200]))


if __name__ == '__main__':
    main()
