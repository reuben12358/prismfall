# -*- coding: utf-8 -*-
"""Renames places everywhere from design/PLACE_NAMES.md (SPINE Revision 13: no "Route N").

  python3 -I tools/rename_places.py            dry run: writes tools/worldmap/last_rename.diff and prints a summary
  python3 -I tools/rename_places.py --apply    rewrites the files
  python3 -I tools/rename_places.py --grep     report every "Route <number>" left in the scanned files
  python3 -I tools/rename_places.py --selftest quoting/skip regression cases (py, yaml, rb, md)

What it rewrites (sources only; generated files are rebuilt by their own tools):
  design/*.md|*.yaml|maps.json, story/*.md, pbs/*.txt, mapgen/specs/*.yaml, mapgen/layouts/*.py|*.yaml,
  tools/trainer_gen/*.py
Rules, in order: (1) every full old name in the table (e.g. "Route 5 - Frostflat Causeway", "Route 32 Seabed",
"Mt. Cinder 1F"); (2) "Route N" with an optional " - [The] <new name>" tail, any case (signs say "ROUTE 5 - THE
FROSTFLAT CAUSEWAY"); (3) the prose forms ("Mt. Cinder" -> "the Cinderhorn"); (4) in story/design prose only, the
shorthand "R5", "R15b" (never on lines about the Festival bracket, the Ruin Route or gym puzzle rooms, and R16 only
next to "Ironway"). A new name that starts with "The" is lowercased mid-sentence ("on the Ferrymen's Mile").
Lines that name audio or tilesets (bgm, BGM, GlitchxCity, "Rejuvenation Route 2", "Route 2_new") are never touched.
Names with an apostrophe (Ferrymen's, Dyers') are escaped inside single-quoted strings: \\' in .py/.rb, '' in YAML.
Each rewritten .py/.yaml/.json/.rb file is parsed before it is written (a file that would not parse is refused), and
after --apply every .py in mapgen/ and tools/ (ast) and every .rb in plugins/ and mapgen/ruby (ruby -c) is checked: if
anything newly fails, every file the run wrote is restored and it exits 1.
Idempotent: a second run changes nothing.
"""
import difflib
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABLE = os.path.join(ROOT, 'design', 'PLACE_NAMES.md')
DIFF_OUT = os.path.join(ROOT, 'tools', 'worldmap', 'last_rename.diff')

INCLUDE = ['design/*.md', 'design/*.yaml', 'design/maps.json', 'story/*.md', 'pbs/*.txt', 'mapgen/specs/*.yaml',
           'mapgen/layouts/*.py', 'mapgen/layouts/*.yaml', 'tools/trainer_gen/*.py', 'README.md']
EXCLUDE = {'design/PLACE_NAMES.md', 'design/SPINE.md', 'design/SPINE_FEEDBACK.md', 'design/ROUTES.yaml'}
SKIP_I = re.compile(r'GlitchxCity|Rejuvenation Route|Reborn Route|rejuv_wll|\.ogg|\.mid\b|BGM/|`bgm:`', re.I)
BGM_VAL = re.compile(r'''(bgm['"]?\s*[:=]\s*['"]?)(Route \d+)''', re.I)
SKIP_CS = re.compile(r'Route \d+_|Route2|Route4|`Route \d+`')


class _Skip:
    @staticmethod
    def search(line):
        return SKIP_I.search(line) or SKIP_CS.search(line)


SKIP_LINE = _Skip()
ABBREV_FILES = re.compile(r'^(story/0[4-8]_.*|story/20_.*|design/WORLD\.md|design/BALANCE\.md|design/POKEMON_AVAILABILITY\.md|'
                          r'design/TRAINER_FIELD_PLAYBOOK\.md|design/DUNGEON_PUZZLES\.md|design/CAMEOS\.md|design/MAPGEN\.md|'
                          r'design/AUDIO\.md|design/FIELDS\.md|design/FLAGS\.md)$')
ABBREV_SKIP = re.compile(r'\b(QF|SF|Final|Festival|bracket|Ruin|RUIN|Run\b|Ledger|draw)', re.I)


def load_table():
    rows = []
    started = False
    for line in open(TABLE, encoding='utf-8'):
        if line.startswith('| ID | Old name | New name'):
            started = True
            continue
        if not started:
            continue
        if not line.startswith('|'):
            if line.strip():
                break
            continue
        c = [x.strip() for x in line.strip().strip('|').split('|')]
        if c[0].startswith('---'):
            continue
        mid, old, new, status = int(c[0]), c[1], c[2], c[3]
        if status == 'renamed' and old != new and old != '-':
            rows.append((mid, old, new))
    prose = []
    sec = False
    for line in open(TABLE, encoding='utf-8'):
        if line.startswith('## Prose forms'):
            sec = True
            continue
        if sec and line.startswith('|') and not line.startswith('| Old') and not line.startswith('|---'):
            a, b = [x.strip() for x in line.strip().strip('|').split('|')[:2]]
            prose.append((a, b))
    return rows, prose


def case_like(src, new):
    if src.isupper() and any(ch.isalpha() for ch in src):
        return new.upper()
    return new


def article(text, start, new):
    """lowercase a leading 'The' mid-sentence; drop it after an existing article"""
    if not new.startswith('The '):
        return new
    before = text[:start]
    m = re.search(r'(\S+)\s*$', before)
    prev = m.group(1) if m else ''
    if re.search(r'(^|\s)(the|The|THE)\s+$', before[-5:] if len(before) >= 5 else ' ' + before):
        return new[4:]
    if prev and (prev[-1].islower() or prev[-1] in ',;') and not prev.endswith(('e.g.', 'i.e.')):
        return 'the ' + new[4:]
    return new


def build_rules(rows, prose):
    rules = []   # (regex, replacement fn)
    # (1) full old names, longest first (only those that are not bare "Route N")
    full = sorted([(o, n) for _, o, n in rows if not re.fullmatch(r'Route \d+b?', o)], key=lambda t: -len(t[0]))
    for old, new in full:
        rx = re.compile(r'(?<![\w])' + re.escape(old) + r'(?![\w])', re.I)
        rules.append((rx, new))
    # (2) Route N with an optional tail
    for mid, old, new in rows:
        m = re.match(r'Route (\d+b?)(?:$| - )', old)
        if not m:
            continue
        num = m.group(1)
        tail = re.escape(new[4:] if new.startswith('The ') else new)
        rx = re.compile(r'(?<![\w])Route ' + re.escape(num) + r'(?:\s*[-–—]\s*(?:the\s+)?' + tail + r')?(?![\w])', re.I)
        rules.append((rx, new))
    for a, b in prose:
        rules.append((re.compile(r'(?<![\w])' + re.escape(a) + r'(?![\w])'), b[0].upper() + b[1:]))
    return rules


def abbrev_rules(rows):
    out = {}
    for mid, old, new in rows:
        m = re.match(r'Route (\d+b?)(?:$| - (.*))', old)
        if m:
            tails = [re.escape(new[4:] if new.startswith('The ') else new)]
            if m.group(2):
                ot = m.group(2)
                tails.append(re.escape(ot[4:] if ot.startswith('The ') else ot))
            out[m.group(1)] = (new, re.compile(r'(?<![\w`-])R' + m.group(1) + r'(?:,?\s+(?:the\s+)?(?:' + '|'.join(tails) +
                                              r'))?(?![\w`])', re.I))
    return out


FIXUPS = [(re.compile(r'\b[Tt]he Drownings Seabed\b'), 'Under the Drownings')]


_CC = {}


def collapse(line, names):
    for rx, rep in FIXUPS:
        line = rx.sub(rep, line)
    for core, last in names:
        if core not in line:
            continue
        if core not in _CC:
            e = re.escape(core)
            _CC[core] = [(re.compile(r'(?:[Tt]he )?' + e + r' \*\*((?:[Tt]he )?' + e + r')\*\*'), r'**\1**'),
                         (re.compile(r'((?:[Tt]he )?' + e + r')(?:,? (?:[Tt]he )?' + e + r')(?![\w])'), r'\1'),
                         (re.compile(r'(' + e + r') ' + re.escape(last.lower()) + r'(?![\w])'), r'\1'),
                         (re.compile(r'(' + e + r'\b[^()]{0,60}?\()(?:[Tt]he )?' + e + r'[;,] '), r'\1')]
        for rx, rep in _CC[core]:
            line = rx.sub(rep, line)
    return line


NAMES = []


def rewrite_line(line, rules, abbr, rel):
    """one line: untouched if it names audio or a tileset; rewrite_text keeps bgm values (audio file names)"""
    if SKIP_LINE.search(line):
        return line
    return rewrite_text(line, rules, abbr, rel)


def rewrite_text(line, rules, abbr, rel):
    saved = []

    def mask(m):
        saved.append(m.group(2))
        return m.group(1) + '\x00%d\x00' % (len(saved) - 1)
    line = BGM_VAL.sub(mask, line)
    line = _rewrite(line, rules, abbr, rel)
    return re.sub('\x00(\\d+)\x00', lambda m: saved[int(m.group(1))], line)


def _rewrite(line, rules, abbr, rel):
    for rx, new in rules:
        def rep(m, new=new):
            r = article(m.string, m.start(), new)
            return case_like(m.group(0), r)
        line = rx.sub(rep, line)
    if abbr and ABBREV_FILES.match(rel) and not ABBREV_SKIP.search(line):
        for k, (new, rx) in abbr.items():
            if k == '16' and 'Ironway' not in line:
                continue
            line = rx.sub(lambda m, new=new: article(m.string, m.start(), new), line)
    line = collapse(line, NAMES)
    # collapse "X (X)" doubles produced by "Gullcry Cliffs (Route 6)"
    line = re.sub(r"((?:[Tt]he )?([A-Z][\w']+(?:[ -][A-Z][\w']+)*)) \((?:[Tt]he )?\2\)", r'\1', line)
    return line


# ----------------------------------------------------------------------------- quoting and validation
def lang_of(rel):
    for ext, lang in (('.py', 'py'), ('.rb', 'rb'), ('.yaml', 'yaml'), ('.yml', 'yaml'), ('.json', 'json')):
        if rel.endswith(ext):
            return lang
    return None


TRIPLES = ("'" * 3, '"' * 3)


def scan_line(line, state, lang):
    """the quote state before each character of one line, and the state carried to the next line"""
    st = []
    i = 0
    n = len(line)
    if state == '#':
        state = ''
    while i < n:
        ch = line[i]
        st.append(state)
        if state == '':
            if lang in ('py', 'rb') and ch == '#':
                state = '#'
            elif lang == 'yaml' and ch == '#' and (i == 0 or line[i - 1] in ' \t'):
                state = '#'
            elif lang == 'py' and line.startswith(TRIPLES, i):
                state = line[i:i + 3]
                st += [state, state]
                i += 3
                continue
            elif ch in ('"', "'"):
                if lang == 'yaml':
                    before = line[:i].rstrip()
                    if before == '' or before[-1] in ':-[{,?':
                        state = ch
                else:
                    state = ch
        elif state in ("'", '"'):
            if ch == '\\' and (lang != 'yaml' or state == '"'):
                st.append(state)
                i += 2
                continue
            if ch == state:
                if lang == 'yaml' and state == "'" and line[i + 1:i + 2] == "'":
                    st.append(state)
                    i += 2
                    continue
                state = ''
        elif state in TRIPLES:
            if line.startswith(state, i):
                st += [state, state]
                i += 3
                state = ''
                continue
        i += 1
    if state == '#' or (state in ("'", '"') and lang in ('py', 'rb')):
        state = ''          # comments and one-line strings never carry over
    return st, state


def escape_apostrophes(old_lines, new_lines, lang, names):
    """inside single-quoted strings, write the apostrophe of a newly inserted name as \\' (py/rb) or '' (yaml).
    Works left to right and rescans after every fix, so one bad quote cannot mislead the rest of the line."""
    if lang not in ('py', 'rb', 'yaml'):
        return new_lines
    rep = "\\'" if lang in ('py', 'rb') else "''"
    out = []
    state = ''
    for a, b in zip(old_lines, new_lines):
        if a != b and "'" in b:
            pos = 0
            while True:
                st, _ = scan_line(b, state, lang)
                hit = None
                for nm in names:
                    if b.lower().count(nm.lower()) <= a.lower().count(nm.lower()) and nm.lower() in a.lower():
                        continue
                    for m in re.finditer(re.escape(nm), b, re.I):
                        if m.start() < pos:
                            continue
                        j = b.index("'", m.start(), m.end()) if "'" in m.group(0) else -1
                        if j >= 0 and st[m.start()] == "'" and (hit is None or j < hit[0]):
                            hit = (j, m.end())
                if hit is None:
                    break
                j, end = hit
                b = b[:j] + rep + b[j + 1:]
                pos = end + len(rep) - 1
        _, state = scan_line(b, state, lang)
        out.append(b)
    return out


def validate(text, lang):
    """None if the text parses, else the error"""
    try:
        if lang == 'py':
            import ast
            ast.parse(text)
        elif lang == 'yaml':
            import yaml
            list(yaml.safe_load_all(text))
        elif lang == 'json':
            import json
            json.loads(text)
        elif lang == 'rb':
            import subprocess
            import tempfile
            with tempfile.NamedTemporaryFile('w', suffix='.rb', delete=False) as t:
                t.write(text)
            r = subprocess.run(['ruby', '-c', t.name], capture_output=True, text=True)
            os.unlink(t.name)
            if r.returncode != 0:
                raise SyntaxError(r.stderr.strip()[:200])
    except Exception as e:
        return '%s: %s' % (type(e).__name__, str(e).split('\n')[0][:160])
    return None


def code_health():
    """every .py in mapgen/ and tools/ (ast) and every .rb in plugins/ and mapgen/ruby (ruby -c): the broken ones"""
    import ast
    import subprocess
    bad = set()
    for f in glob.glob(os.path.join(ROOT, 'mapgen', '**', '*.py'), recursive=True) + \
            glob.glob(os.path.join(ROOT, 'tools', '**', '*.py'), recursive=True):
        try:
            ast.parse(open(f, encoding='utf-8').read())
        except Exception:
            bad.add(f)
    for f in glob.glob(os.path.join(ROOT, 'plugins', '**', '*.rb'), recursive=True) + \
            glob.glob(os.path.join(ROOT, 'mapgen', 'ruby', '*.rb')):
        r = subprocess.run(['ruby', '-c', f], capture_output=True, text=True)
        if r.returncode != 0:
            bad.add(f)
    return bad


def process(apply, rules, abbr, rows):
    diffs = []
    changed = 0
    nlines = 0
    apos = sorted({v for _, o, n in rows if "'" in n
                   for v in (n, n.upper(), ('the ' + n[4:]) if n.startswith('The ') else n)}, key=len, reverse=True)
    before_bad = code_health() if apply else set()
    written = {}
    refused = []
    for f, rel in files():
        text = open(f, encoding='utf-8').read()
        lines = text.split('\n')
        new = [rewrite_line(l, rules, abbr, rel) for l in lines]
        if new == lines:
            continue
        lang = lang_of(rel)
        new = escape_apostrophes(lines, new, lang, apos)
        if lang and validate('\n'.join(new), lang) and not validate(text, lang):
            refused.append((rel, validate('\n'.join(new), lang)))
            continue
        changed += 1
        nlines += sum(1 for a, b in zip(lines, new) if a != b)
        diffs.extend(difflib.unified_diff(lines, new, rel, rel, lineterm='', n=0))
        if apply:
            written[f] = text
            open(f, 'w', encoding='utf-8').write('\n'.join(new))
    if apply and written:
        broke = sorted(code_health() - before_bad)
        if broke:
            for f, text in written.items():
                open(f, 'w', encoding='utf-8').write(text)
            print('ROLLED BACK: the rename broke %s; every file this run wrote is restored'
                  % ', '.join(os.path.relpath(b, ROOT) for b in broke))
            sys.exit(1)
    for rel, err in refused:
        print('REFUSED %s: the renamed file would not parse (%s); left unchanged' % (rel, err))
    return diffs, changed, nlines


def files():
    out = []
    for pat in INCLUDE:
        for f in sorted(glob.glob(os.path.join(ROOT, pat))):
            rel = os.path.relpath(f, ROOT)
            if rel not in EXCLUDE:
                out.append((f, rel))
    return out


def main():
    rows, prose = load_table()
    global NAMES
    NAMES = [(n[4:] if n.startswith('The ') else n, n.split()[-1]) for _, o, n in rows]
    rules = build_rules(rows, prose)
    abbr = abbrev_rules(rows)
    apply = '--apply' in sys.argv
    if '--selftest' in sys.argv:
        apos = sorted({v for _, o, n in rows if "'" in n
                       for v in (n, n.upper(), ('the ' + n[4:]) if n.startswith('The ') else n)}, key=len, reverse=True)
        cases = [('t.py', ["QUEST('biscuit', 'Biscuit', 'Go to the old orchard on Route 1.')"]),
                 ('t.py', ["h = {'name': 'Route 1', 'bgm': 'Route 1', 'x': 'Route 1 and Route 1'}  # Route 1"]),
                 ('t.py', ['"""doc', "Route 1 in 'Route 1'", '"""', "y = 'Route 1'"]),
                 ('t.yaml', ["text: 'ROUTE 1", "", "    Ferrow''s Landing - Route 3 - Route 1.'"]),
                 ('t.yaml', ["- {script: 'pfm_quest(:biscuit, \"Biscuit\", \"on Route 1.\")'}"]),
                 ('t.rb', ["t = \"on Route 15\"; u = 'Route 1' # Route 1"]),
                 ('t.md', ["| `Route 2_new` (39), `Route 3` (8) |", "GlitchxCity - Route 10 remix", "bgm: Route 2"])]
        ok = True
        for rel, lines in cases:
            new = escape_apostrophes(lines, [rewrite_line(l, rules, abbr, rel) for l in lines], lang_of(rel), apos)
            err = validate('\n'.join(new), lang_of(rel)) if lang_of(rel) else None
            if rel == 't.md' and new != lines:
                err = 'audio/tileset line changed'
            print('%s %s %s' % ('ok  ' if not err else 'FAIL', rel, err or new))
            ok = ok and not err
        sys.exit(0 if ok else 1)
    if '--grep' in sys.argv:
        n = 0
        for f, rel in files():
            for i, line in enumerate(open(f, encoding='utf-8'), 1):
                if re.search(r'(?<![\w])Route \d', line, re.I):
                    rest = BGM_VAL.sub('', line)
                    tag = 'skipped (audio/tileset)' if SKIP_LINE.search(line) else \
                        ('bgm file name' if not re.search(r'(?<![\w])Route \d', rest, re.I) else 'LEFT')
                    print('%s:%d: [%s] %s' % (rel, i, tag, line.strip()[:150]))
                    n += 1
        print('%d lines' % n)
        return
    diffs, changed, nlines = process(apply, rules, abbr, rows)
    os.makedirs(os.path.dirname(DIFF_OUT), exist_ok=True)
    open(DIFF_OUT, 'w', encoding='utf-8').write('\n'.join(diffs) + '\n')
    print('%s: %d files, %d lines %s. Diff: %s' % ('APPLIED' if apply else 'DRY RUN', changed, nlines,
                                                 'changed' if apply else 'would change', os.path.relpath(DIFF_OUT, ROOT)))
    if not apply:
        print('Re-run with --apply to write them. Then regenerate: ruby tools/field_defaults_to_rb.rb, mapgen build.')


if __name__ == '__main__':
    main()
