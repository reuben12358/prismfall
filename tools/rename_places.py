# -*- coding: utf-8 -*-
"""Renames places everywhere from design/PLACE_NAMES.md (SPINE Revision 13: no "Route N").

  python3 -I tools/rename_places.py            dry run: writes tools/worldmap/last_rename.diff and prints a summary
  python3 -I tools/rename_places.py --apply    rewrites the files
  python3 -I tools/rename_places.py --grep     report every "Route <number>" left in the scanned files

What it rewrites (sources only; generated files are rebuilt by their own tools):
  design/*.md|*.yaml|maps.json, story/*.md, pbs/*.txt, mapgen/specs/*.yaml, mapgen/layouts/*.py|*.yaml,
  tools/trainer_gen/*.py
Rules, in order: (1) every full old name in the table (e.g. "Route 5 - Frostflat Causeway", "Route 32 Seabed",
"Mt. Cinder 1F"); (2) "Route N" with an optional " - [The] <new name>" tail, any case (signs say "ROUTE 5 - THE
FROSTFLAT CAUSEWAY"); (3) the prose forms ("Mt. Cinder" -> "the Cinderhorn"); (4) in story/design prose only, the
shorthand "R5", "R15b" (never on lines about the Festival bracket, the Ruin Route or gym puzzle rooms, and R16 only
next to "Ironway"). A new name that starts with "The" is lowercased mid-sentence ("on the Ferrymen's Mile").
Lines that name audio or tilesets (bgm, BGM, GlitchxCity, "Rejuvenation Route 2", "Route 2_new") are never touched.
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
    if SKIP_LINE.search(line):
        return line
    if rel.endswith('.py'):
        return _py_safe(line, rewrite_text(line, rules, abbr, rel))
    return rewrite_text(line, rules, abbr, rel)


def _py_safe(old, new):
    """escape apostrophes a new name brought into a single-quoted Python string"""
    if new == old or "'" not in new:
        return new
    out, q, i = [], None, 0
    while i < len(new):
        ch = new[i]
        if q is None:
            if ch == '#':
                out.append(new[i:])
                break
            if ch in '\'"':
                q = ch
            out.append(ch)
        else:
            if ch == '\\':
                out.append(new[i:i + 2])
                i += 2
                continue
            if ch == q:
                # a quote that closes the string only if what follows looks like the end of a literal
                rest = new[i + 1:i + 2]
                if q == "'" and rest and (rest.isalpha() or rest == ' ' and new[i + 1:i + 3].strip()[:1].isalpha()
                                         and not new[i + 1:].lstrip().startswith(('if', 'else', 'for', 'and', 'or', 'in'))):
                    out.append("\\'")
                    i += 1
                    continue
                q = None
            out.append(ch)
        i += 1
    return ''.join(out)


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
    if '--grep' in sys.argv:
        n = 0
        for f, rel in files():
            for i, line in enumerate(open(f, encoding='utf-8'), 1):
                if re.search(r'(?<![\w])Route \d', line, re.I):
                    tag = 'skipped (audio/tileset)' if SKIP_LINE.search(line) else 'LEFT'
                    print('%s:%d: [%s] %s' % (rel, i, tag, line.strip()[:150]))
                    n += 1
        print('%d lines' % n)
        return
    diffs = []
    changed = 0
    nlines = 0
    for f, rel in files():
        text = open(f, encoding='utf-8').read()
        lines = text.split('\n')
        new = [rewrite_line(l, rules, abbr, rel) for l in lines]
        if new != lines:
            changed += 1
            nl = sum(1 for a, b in zip(lines, new) if a != b)
            nlines += nl
            diffs.extend(difflib.unified_diff(lines, new, rel, rel, lineterm='', n=0))
            if apply:
                open(f, 'w', encoding='utf-8').write('\n'.join(new))
    os.makedirs(os.path.dirname(DIFF_OUT), exist_ok=True)
    open(DIFF_OUT, 'w', encoding='utf-8').write('\n'.join(diffs) + '\n')
    print('%s: %d files, %d lines %s. Diff: %s' % ('APPLIED' if apply else 'DRY RUN', changed, nlines,
                                                 'changed' if apply else 'would change', os.path.relpath(DIFF_OUT, ROOT)))
    if not apply:
        print('Re-run with --apply to write them. Then regenerate: ruby tools/field_defaults_to_rb.rb, mapgen build.')


if __name__ == '__main__':
    main()
