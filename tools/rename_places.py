# -*- coding: utf-8 -*-
"""Renames places everywhere from design/PLACE_NAMES.md (SPINE Revision 13: no "Route N").

  python3 -I tools/rename_places.py            dry run: writes tools/worldmap/last_rename.diff and prints a summary
  python3 -I tools/rename_places.py --apply    rewrites the files (then checks the whole project, see below)
  python3 -I tools/rename_places.py --grep     report every "Route <number>" left in the scanned files
  python3 -I tools/rename_places.py --selftest quoting/skip regression cases (py, yaml, rb, md)

What it rewrites (sources only; generated files are rebuilt by their own tools):
  design/*.md|*.yaml|maps.json, story/*.md, pbs/*.txt, mapgen/specs/*.yaml, mapgen/layouts/*.py|*.yaml,
  tools/trainer_gen/*.py, plugins/**/*.rb, mapgen/ruby/*.rb, README.md
Rules, in order: (1) every full old name in the table (e.g. "Route 5 - Frostflat Causeway", "Route 32 Seabed",
"Mt. Cinder 1F"); (2) "Route N" with an optional " - [The] <new name>" tail, any case (signs say "ROUTE 5 - THE
FROSTFLAT CAUSEWAY"); (3) the prose forms ("Mt. Cinder" -> "the Cinderhorn"); (4) in story/design prose only, the
shorthand "R5", "R15b" (never on lines about the Festival bracket, the Ruin Route or gym puzzle rooms, and R16 only
next to "Ironway"). A new name that starts with "The" is lowercased mid-sentence ("on the Ferrymen's Mile").
Lines that name audio or tilesets (bgm, BGM, GlitchxCity, "Rejuvenation Route 2", "Route 2_new") are never touched.

Apostrophes (the Ferrymen's Mile, the Dyers' Ford, Spinners' Rise, Hale's Bramble). Every apostrophe a rename
inserts is tracked (it is written as a marker first), and the file's own lexer says where it landed: Python
`tokenize`, Ruby `Ripper`, the PyYAML scanner. Then:
  - Python '...' and Ruby '...' / :'...' strings: \\'      - YAML '...' scalars: ''
  - Python r'...' (a raw string cannot hold a bare '): the line is SKIPPED (left as it was) and reported
  - Python '''...''' strings: \\' only next to another quote; double-quoted strings, heredocs, %q(), comments: as is
  - Ruby code inside a Python or YAML string (event `script:` values such as "pbMessage('on Route 1')"): the
    apostrophe is escaped for Ruby too, so the script still parses in the game ("...Ferrymen\\\\'s..." in Python).
Checks: each rewritten file must parse (.py ast, .rb ruby -c, .yaml, .json) and, for .py, keep the same AST apart
from string values; Ruby inside changed string values must still parse. A file that fails is refused (not written).
After --apply every .py in the project is parsed with `python3 -I` (ast) and every .rb is checked with `ruby -c`;
if anything that parsed before no longer does, or the run fails half way, every file the run wrote is restored and
it exits 1. Idempotent: a second run changes nothing.
"""
import concurrent.futures
import difflib
import glob
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABLE = os.path.join(ROOT, 'design', 'PLACE_NAMES.md')
DIFF_OUT = os.path.join(ROOT, 'tools', 'worldmap', 'last_rename.diff')

INCLUDE = ['design/*.md', 'design/*.yaml', 'design/maps.json', 'story/*.md', 'pbs/*.txt', 'mapgen/specs/*.yaml',
           'mapgen/layouts/*.py', 'mapgen/layouts/*.yaml', 'tools/trainer_gen/*.py', 'plugins/**/*.rb',
           'mapgen/ruby/*.rb', 'README.md']
EXCLUDE = {'design/PLACE_NAMES.md', 'design/SPINE.md', 'design/SPINE_FEEDBACK.md', 'design/ROUTES.yaml'}
SKIP_DIRS = {'.git', 'dist', 'dist_web', '__pycache__', 'node_modules'}
SKIP_I = re.compile(r'GlitchxCity|Rejuvenation Route|Reborn Route|rejuv_wll|\.ogg|\.mid\b|BGM/|`bgm:`', re.I)
BGM_VAL = re.compile(r'''(bgm['"]?\s*[:=]\s*['"]?)(Route \d+)''', re.I)
SKIP_CS = re.compile(r'Route \d+_|Route2|Route4|`Route \d+`')
MARK = '\ue000'          # stands for an apostrophe the rename inserted, until the file's lexer has placed it
APOS = "(?:\\\\'|''|'|" + MARK + ')'    # an apostrophe in a pattern: as is, escaped, doubled or still a marker


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


def pat(s):
    """regex for a literal name whose apostrophes may already be escaped, doubled or marked"""
    return re.escape(s).replace("'", APOS)


def marked(s):
    return s.replace("'", MARK)


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
    """(regex, new name) pairs; new names carry MARK where they have an apostrophe"""
    rules = []
    # (1) full old names, longest first (only those that are not bare "Route N")
    full = sorted([(o, n) for _, o, n in rows if not re.fullmatch(r'Route \d+b?', o)], key=lambda t: -len(t[0]))
    for old, new in full:
        rx = re.compile(r'(?<![\w])' + pat(old) + r'(?![\w])', re.I)
        rules.append((rx, marked(new)))
    # (2) Route N with an optional tail
    for mid, old, new in rows:
        m = re.match(r'Route (\d+b?)(?:$| - )', old)
        if not m:
            continue
        num = m.group(1)
        tail = pat(new[4:] if new.startswith('The ') else new)
        rx = re.compile(r'(?<![\w])Route ' + re.escape(num) + r'(?:\s*[-–—]\s*(?:the\s+)?' + tail + r')?(?![\w])', re.I)
        rules.append((rx, marked(new)))
    for a, b in prose:
        rules.append((re.compile(r'(?<![\w])' + pat(a) + r'(?![\w])'), marked(b[0].upper() + b[1:])))
    return rules


def abbrev_rules(rows):
    out = {}
    for mid, old, new in rows:
        m = re.match(r'Route (\d+b?)(?:$| - (.*))', old)
        if m:
            tails = [pat(new[4:] if new.startswith('The ') else new)]
            if m.group(2):
                ot = m.group(2)
                tails.append(pat(ot[4:] if ot.startswith('The ') else ot))
            out[m.group(1)] = (marked(new), re.compile(r'(?<![\w`-])R' + m.group(1) + r'(?:,?\s+(?:the\s+)?(?:' +
                                                      '|'.join(tails) + r'))?(?![\w`])', re.I))
    return out


def sub_keep_marks(rx, tmpl, line):
    """rx.sub(tmpl, line), matched on the line with markers read as apostrophes (so a new "Ferrymen's" equals an old
    one) while the result keeps the markers. tmpl: a literal or \\N group references only."""
    if MARK not in line:
        return rx.sub(tmpl, line)
    norm = line.replace(MARK, "'")
    out, pos = [], 0
    for m in rx.finditer(norm):
        out.append(line[pos:m.start()])
        out.append(re.sub(r'\\(\d)', lambda g: line[m.start(int(g.group(1))):m.end(int(g.group(1)))]
                          if m.group(int(g.group(1))) is not None else '', tmpl))
        pos = m.end()
    out.append(line[pos:])
    return ''.join(out)


FIXUPS = [(re.compile(r'\b[Tt]he Drownings Seabed\b'), 'Under the Drownings')]
DOUBLE_PAREN = re.compile(r"((?:[Tt]he )?([A-Z][\w']+(?:[ -][A-Z][\w']+)*)) \((?:[Tt]he )?\2\)")
_CC = {}


def collapse(line, names):
    for rx, rep in FIXUPS:
        line = sub_keep_marks(rx, rep, line)
    norm = line.replace(MARK, "'")
    for core, last in names:
        if core not in norm:
            continue
        if core not in _CC:
            e = re.escape(core)
            _CC[core] = [(re.compile(r'(?:[Tt]he )?' + e + r' \*\*((?:[Tt]he )?' + e + r')\*\*'), r'**\1**'),
                         (re.compile(r'((?:[Tt]he )?' + e + r')(?:,? (?:[Tt]he )?' + e + r')(?![\w])'), r'\1'),
                         (re.compile(r'(' + e + r') ' + re.escape(last.lower()) + r'(?![\w])'), r'\1'),
                         (re.compile(r'(' + e + r'\b[^()]{0,60}?\()(?:[Tt]he )?' + e + r'[;,] '), r'\1')]
        for rx, rep in _CC[core]:
            line = sub_keep_marks(rx, rep, line)
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
    line = sub_keep_marks(DOUBLE_PAREN, r'\1', line)
    return line


# ----------------------------------------------------------------------------- where each inserted apostrophe landed
def lang_of(rel):
    for ext, lang in (('.py', 'py'), ('.rb', 'rb'), ('.yaml', 'yaml'), ('.yml', 'yaml'), ('.json', 'json')):
        if rel.endswith(ext):
            return lang
    return None


RUBY_LEX = r'''
require 'ripper'
require 'json'
MARK = [0xE000].pack('U')
# per marker, in source order: "sq" inside a '...' or :'...' literal, "str" inside any other string, regexp or heredoc,
# "comment", or "code"
def classify(src)
  stack = []; pending = []; out = []
  Ripper.lex(src).each do |(_pos, type, tok, _state)|
    case type
    when :on_heredoc_beg then pending << tok
    when :on_heredoc_end then stack.pop; stack.push(pending.shift) unless pending.empty?
    when :on_tstring_beg, :on_regexp_beg, :on_backtick, :on_qwords_beg, :on_words_beg, :on_qsymbols_beg,
         :on_symbols_beg then stack.push(tok)
    when :on_symbeg then stack.push(tok) if tok.length > 1
    when :on_tstring_end, :on_label_end, :on_regexp_end then stack.pop
    when :on_embexpr_beg then stack.push('#{')
    when :on_embexpr_end then stack.pop
    end
    n = tok.count(MARK)
    if n > 0
      kind = case type
             when :on_tstring_content then (["'", ":'"].include?(stack.last) ? 'sq' : 'str')
             when :on_comment, :on_embdoc then 'comment'
             else 'code'
             end
      n.times { out << kind }
    end
    if [:on_nl, :on_ignored_nl].include?(type) || (type == :on_comment && tok.end_with?("\n"))
      stack.push(pending.shift) if !pending.empty? && !stack.last.to_s.start_with?('<<')
    end
  end
  out
end
def code_like(v)
  c = v.gsub(/%EV\[[^\]]*\]%/, '1')          # mapgen event-name placeholders
  (c =~ /\w\(|\$[a-z_]/) && !Ripper.sexp(c).nil? ? c : nil
end
req = JSON.parse(File.read(ARGV[0], encoding: 'UTF-8'))
res = {}
res['file'] = classify(req['file']) if req['file']
# Ruby inside string values: per value, nil when it is not Ruby code, else the class of each marker
res['nested'] = (req['nested'] || []).map do |v|
  c = code_like(v)
  next nil if c.nil? || c.count(MARK) != v.count(MARK)
  classify(c)
end
# (old, new) pairs: true when old was Ruby code and new no longer parses
res['regress'] = (req['pairs'] || []).map do |(a, b)|
  ca = code_like(a)
  !ca.nil? && Ripper.sexp(b.gsub(/%EV\[[^\]]*\]%/, '1')).nil?
end
res['parses'] = (req['parse'] || []).map { |v| !Ripper.sexp(v.gsub(/%EV\[[^\]]*\]%/, '1')).nil? }
puts JSON.generate(res)
'''


def ruby_query(req):
    """run RUBY_LEX on a request dict (file / nested / pairs); None if Ruby is missing or fails"""
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        rq, scr = os.path.join(td, 'req.json'), os.path.join(td, 'lex.rb')
        open(rq, 'w', encoding='utf-8').write(json.dumps(req))
        open(scr, 'w', encoding='utf-8').write(RUBY_LEX)
        try:
            r = subprocess.run(['ruby', scr, rq], capture_output=True, text=True, encoding='utf-8', timeout=120)
        except (OSError, subprocess.TimeoutExpired):
            return None
        if r.returncode != 0:
            return None
        return json.loads(r.stdout)


def py_contexts(text):
    """per marker: (ctx, k) with ctx a dict (kind str/comment/code, quote, triple, raw, value) and k the marker's index
    inside that string's value; None if the text does not tokenize"""
    import ast
    import io
    import tokenize
    out = []
    fstack = []
    try:
        for tok in tokenize.generate_tokens(io.StringIO(text).readline):
            name = tokenize.tok_name.get(tok.type, '')
            s = tok.string
            if name == 'FSTRING_START':
                fstack.append(s)
            elif name == 'FSTRING_END' and fstack:
                fstack.pop()
            n = s.count(MARK)
            if not n:
                continue
            if tok.type == tokenize.STRING:
                pre = re.match(r'[A-Za-z]*', s).group(0)
                body = s[len(pre):]
                q = body[:3] if body[:3] in ("'''", '"""') else body[:1]
                try:
                    val = ast.literal_eval(s)
                except Exception:
                    val = None
                ctx = dict(kind='str', quote=q[:1], triple=len(q) == 3, raw='r' in pre.lower(),
                           value=val if isinstance(val, str) else None)
            elif name == 'FSTRING_MIDDLE' and fstack:
                st = fstack[-1]
                pre = re.match(r'[A-Za-z]*', st).group(0)
                q = st[len(pre):]
                ctx = dict(kind='str', quote=q[:1], triple=len(q) == 3, raw='r' in pre.lower(), value=None)
            elif tok.type == tokenize.COMMENT:
                ctx = dict(kind='comment')
            else:
                ctx = dict(kind='code')
            out.extend((ctx, k) for k in range(n))
    except (tokenize.TokenError, SyntaxError, IndentationError, ValueError):
        return None
    return out


def yaml_contexts(text):
    import yaml
    spans = []
    try:
        for t in yaml.scan(text):
            if isinstance(t, yaml.ScalarToken):
                spans.append((t.start_mark.index, t.end_mark.index, t.style or '', t.value))
    except yaml.YAMLError:
        return None
    out = []
    for p in [i for i, c in enumerate(text) if c == MARK]:
        hit = next((s for s in spans if s[0] <= p < s[1]), None)
        if hit:
            out.append((dict(kind='str', style=hit[2], value=hit[3]), text[hit[0]:p].count(MARK)))
        else:
            out.append((dict(kind='other'), 0))
    return out


SKIP = None


def encode(lang, ctx, nested_sq, prev, nxt):
    """the text that replaces one marker, or SKIP when the host string cannot hold an apostrophe"""
    if lang == 'py':
        if ctx['kind'] != 'str':
            return "'"
        sq, raw = ctx['quote'] == "'", ctx['raw']
        if nested_sq:                                   # Ruby needs \' in the value
            return "\\'" if raw else "\\\\" + ("\\'" if sq else "'")
        if not sq:
            return "'"
        if ctx['triple'] and prev != "'" and nxt != "'":
            return "'"
        return SKIP if raw else "\\'"
    if lang == 'rb':
        return "\\'" if ctx == 'sq' else "'"
    if lang == 'yaml':
        if ctx['kind'] != 'str':
            return "'"
        st = ctx['style']
        if nested_sq:
            return {"'": "\\''", '"': "\\\\'"}.get(st, "\\'")
        return "''" if st == "'" else "'"
    return "'"


def resolve_marks(old_lines, new_lines, lang, rel, notes):
    """replace every marker by the right apostrophe for where it landed; lines that cannot take one are kept as they
    were (reported in notes). Returns the final lines."""
    text = '\n'.join(new_lines)
    if MARK not in text:
        return new_lines
    if lang not in ('py', 'rb', 'yaml'):
        return [l.replace(MARK, "'") for l in new_lines]
    if lang == 'py':
        ctxs = py_contexts(text)
    elif lang == 'yaml':
        ctxs = yaml_contexts(text)
    else:
        r = ruby_query({'file': text})
        ctxs = r['file'] if r else None
    n = text.count(MARK)
    if ctxs is None or len(ctxs) != n:
        notes.append('%s: could not lex the renamed file; apostrophes written as is (the parse check decides)' % rel)
        return [l.replace(MARK, "'") for l in new_lines]
    nested = [False] * n
    if lang in ('py', 'yaml'):
        vals, owners = [], []
        for i, (ctx, k) in enumerate(ctxs):
            if ctx.get('kind') == 'str' and ctx.get('value') is not None and MARK in ctx['value']:
                key = id(ctx)
                if key not in owners:
                    owners.append(key)
                    vals.append(ctx['value'])
        if vals:
            r = ruby_query({'nested': vals})
            if r:
                per = dict(zip(owners, r['nested']))
                for i, (ctx, k) in enumerate(ctxs):
                    cls = per.get(id(ctx)) if ctx.get('kind') == 'str' else None
                    if cls and k < len(cls) and cls[k] == 'sq':
                        nested[i] = True
    out, mi = [], 0
    for li, line in enumerate(new_lines):
        if MARK not in line:
            out.append(line)
            continue
        pieces, skip, start = [], False, 0
        for j, ch in enumerate(line):
            if ch != MARK:
                continue
            ctx = ctxs[mi][0] if lang != 'rb' else ctxs[mi]
            prev = line[j - 1] if j > 0 else ''
            nxt = line[j + 1] if j + 1 < len(line) else ''
            rep = encode(lang, ctx, nested[mi], prev, nxt)
            mi += 1
            if rep is SKIP:
                skip = True
            pieces.append(line[start:j])
            pieces.append(rep or "'")
            start = j + 1
        pieces.append(line[start:])
        if skip:
            notes.append("%s:%d: SKIPPED (a raw r'...' string cannot hold the apostrophe; rename it by hand): %s"
                         % (rel, li + 1, old_lines[li].strip()[:120]))
            out.append(old_lines[li])
        else:
            out.append(''.join(pieces))
    return out


# ----------------------------------------------------------------------------- validation
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
            json.loads(text)
        elif lang == 'rb':
            import tempfile
            with tempfile.NamedTemporaryFile('w', suffix='.rb', delete=False, encoding='utf-8') as t:
                t.write(text)
            r = subprocess.run(['ruby', '-c', t.name], capture_output=True, text=True)
            os.unlink(t.name)
            if r.returncode != 0:
                raise SyntaxError(r.stderr.strip()[:200])
    except Exception as e:
        return '%s: %s' % (type(e).__name__, str(e).split('\n')[0][:160])
    return None


def _py_strings(tree):
    import ast
    return [n.value for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, str)]


def _py_shape(tree):
    import ast
    for n in ast.walk(tree):
        if isinstance(n, ast.Constant) and isinstance(n.value, str):
            n.value = ''
    return ast.dump(tree, include_attributes=False)


def _yaml_pairs(a, b, out):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in a:
            if k in b:
                _yaml_pairs(a[k], b[k], out)
    elif isinstance(a, list) and isinstance(b, list):
        for x, y in zip(a, b):
            _yaml_pairs(x, y, out)
    elif isinstance(a, str) and isinstance(b, str) and a != b:
        out.append((a, b))


def deep_check(old_text, new_text, lang):
    """beyond parsing: .py keeps its AST apart from string values, and Ruby code inside changed string values (event
    scripts) still parses. None if fine, else the problem."""
    pairs = []
    if lang == 'py':
        import ast
        a, b = ast.parse(old_text), ast.parse(new_text)
        sa, sb = _py_strings(a), _py_strings(b)
        if _py_shape(a) != _py_shape(b) or len(sa) != len(sb):
            return 'the code around the strings changed (a quote ended a string early?)'
        pairs = [(x, y) for x, y in zip(sa, sb) if x != y]
    elif lang == 'yaml':
        import yaml
        for x, y in zip(yaml.safe_load_all(old_text), yaml.safe_load_all(new_text)):
            _yaml_pairs(x, y, pairs)
    if not pairs:
        return None
    r = ruby_query({'pairs': pairs})
    if r is None:
        return None
    bad = [p for p, flag in zip(pairs, r['regress']) if flag]
    if bad:
        return 'Ruby inside a string no longer parses: %r' % bad[0][1][:120]
    return None


def all_code_files():
    py, rb = [], []
    for d, subdirs, fs in os.walk(ROOT):
        subdirs[:] = [s for s in subdirs if s not in SKIP_DIRS]
        for f in fs:
            if f.endswith('.py'):
                py.append(os.path.join(d, f))
            elif f.endswith('.rb'):
                rb.append(os.path.join(d, f))
    return sorted(py), sorted(rb)


PY_CHECK = ("import ast, sys\n"
            "for p in sys.argv[1:]:\n"
            "    try:\n"
            "        ast.parse(open(p, encoding='utf-8').read(), p)\n"
            "    except Exception:\n"
            "        print(p)\n")


def code_health():
    """the files that do NOT parse: every .py (python3 -I, ast) and every .rb (ruby -c) in the project"""
    py, rb = all_code_files()
    bad = set()
    for i in range(0, len(py), 100):
        r = subprocess.run(['python3', '-I', '-c', PY_CHECK] + py[i:i + 100], capture_output=True, text=True,
                           cwd='/')
        if r.returncode != 0:
            raise RuntimeError('python3 -I ast check failed to run: ' + r.stderr[-300:])
        bad.update(l for l in r.stdout.split('\n') if l)

    def rbc(f):
        return f if subprocess.run(['ruby', '-c', f], capture_output=True).returncode != 0 else None
    with concurrent.futures.ThreadPoolExecutor(8) as ex:
        bad.update(f for f in ex.map(rbc, rb) if f)
    return bad


# ----------------------------------------------------------------------------- the run
def apostrophe_free(text):
    return MARK not in text


def process(apply, rules, abbr):
    diffs = []
    changed = 0
    nlines = 0
    notes = []
    refused = []
    before_bad = code_health() if apply else set()
    written = {}
    try:
        for f, rel in files():
            text = open(f, encoding='utf-8').read()
            if not apostrophe_free(text):
                notes.append('%s: contains U+E000 (the rename marker); skipped' % rel)
                continue
            lines = text.split('\n')
            new = [rewrite_line(l, rules, abbr, rel) for l in lines]
            if new == lines:
                continue
            lang = lang_of(rel)
            new = resolve_marks(lines, new, lang, rel, notes)
            if new == lines:
                continue
            new_text = '\n'.join(new)
            if lang:
                err = validate(new_text, lang)
                if err is None and lang in ('py', 'yaml'):
                    err = deep_check(text, new_text, lang)
                if err and not validate(text, lang):
                    refused.append((rel, err))
                    continue
            changed += 1
            nlines += sum(1 for a, b in zip(lines, new) if a != b)
            diffs.extend(difflib.unified_diff(lines, new, rel, rel, lineterm='', n=0))
            if apply:
                written[f] = text
                with open(f, 'w', encoding='utf-8') as fh:
                    fh.write(new_text)
        if apply and written:
            broke = sorted(code_health() - before_bad)
            if broke:
                raise RuntimeError('the rename broke %s' % ', '.join(os.path.relpath(b, ROOT) for b in broke))
    except BaseException as e:
        for f, text in written.items():
            with open(f, 'w', encoding='utf-8') as fh:
                fh.write(text)
        if written:
            print('ROLLED BACK (%s: %s): every file this run wrote (%d) is restored' % (type(e).__name__, e, len(written)))
        if isinstance(e, (KeyboardInterrupt, SystemExit)):
            raise
        sys.exit(1)
    for rel, err in refused:
        print('REFUSED %s: the renamed file would not pass its checks (%s); left unchanged' % (rel, err))
    for n in notes:
        print(n)
    return diffs, changed, nlines


def files():
    out = []
    for p in INCLUDE:
        for f in sorted(glob.glob(os.path.join(ROOT, p), recursive=True)):
            rel = os.path.relpath(f, ROOT)
            if rel not in EXCLUDE and not (set(rel.split(os.sep)) & SKIP_DIRS):
                out.append((f, rel))
    return out


# ----------------------------------------------------------------------------- self test
SELFTEST = [
    # (file, old lines, expected new lines)
    ('t.py', ["QUEST('biscuit', 'Biscuit', 'Go to the old orchard on Route 1.')"],
     ["QUEST('biscuit', 'Biscuit', 'Go to the old orchard on the Ferrymen\\'s Mile.')"]),
    ('t.py', ["h = {'name': 'Route 1', 'bgm': 'Route 1', 'x': 'Route 1 and Route 1'}  # Route 1"],
     ["h = {'name': 'The Ferrymen\\'s Mile', 'bgm': 'Route 1', 'x': 'The Ferrymen\\'s Mile and the Ferrymen\\'s Mile'}"
      "  # The Ferrymen's Mile"]),
    ('t.py', ['"""doc', "Route 1 in 'Route 1'", '"""', "y = 'Route 1'", "z = '''Route 1'''"],
     ['"""doc', "The Ferrymen's Mile in 'The Ferrymen's Mile'", '"""', "y = 'The Ferrymen\\'s Mile'",
      "z = '''The Ferrymen's Mile'''"]),
    ('t.py', ["x = 'Route 1'", "p = r'on Route 1'", "q = r\"on Route 1\"", "f = f'{n} on Route 1'"],   # raw '': skipped
     ["x = 'The Ferrymen\\'s Mile'", "p = r'on Route 1'", "q = r\"on the Ferrymen's Mile\"",
      "f = f'{n} on the Ferrymen\\'s Mile'"]),
    ('t.py', ["E.append({'script': \"pbMessage('Go to Route 1.')\", 'text': \"Route 1's sign\"})",
              "S = 'pbMessage(\"on Route 1\")'", "T = 'pbMessage(\\'on Route 1\\')'"],
     ["E.append({'script': \"pbMessage('Go to the Ferrymen\\\\'s Mile.')\", 'text': \"The Ferrymen's Mile's sign\"})",
      "S = 'pbMessage(\"on the Ferrymen\\'s Mile\")'", "T = 'pbMessage(\\'on the Ferrymen\\\\\\'s Mile\\')'"]),
    ('t.yaml', ["text: 'ROUTE 1", "", "    Ferrow''s Landing - Route 3 - Route 1.'"],
     ["text: 'THE FERRYMEN''S MILE", "", "    Ferrow''s Landing - Thistledown Lea - The Ferrymen''s Mile.'"]),
    ('t.yaml', ["- {script: 'pfm_quest(:biscuit, \"Biscuit\", \"on Route 1.\")'}",
                "- {script: \"pbMessage('on Route 1')\"}", "- {script: 'pbMessage(''on Route 1'')'}",
                "- text: Go to Route 1 now  # Route 1"],
     ["- {script: 'pfm_quest(:biscuit, \"Biscuit\", \"on the Ferrymen''s Mile.\")'}",
      "- {script: \"pbMessage('on the Ferrymen\\\\'s Mile')\"}", "- {script: 'pbMessage(''on the Ferrymen\\''s Mile'')'}",
      "- text: Go to the Ferrymen's Mile now  # The Ferrymen's Mile"]),
    ('t.rb', ["t = \"on Route 15\"; u = 'Route 1' # Route 1", "x = <<~'EOS'", "  Route 1 sign", "EOS",
              "y = 'two", "Route 1 lines'", "z = %q(Route 1) + :'Route 1'.to_s"],
     ["t = \"on the Ashmarch\"; u = 'The Ferrymen\\'s Mile' # The Ferrymen's Mile", "x = <<~'EOS'",
      "  The Ferrymen's Mile sign", "EOS", "y = 'two", "The Ferrymen\\'s Mile lines'",
      "z = %q(The Ferrymen's Mile) + :'The Ferrymen\\'s Mile'.to_s"]),
    ('t.md', ["| `Route 2_new` (39), `Route 3` (8) |", "GlitchxCity - Route 10 remix", "bgm: Route 2"], None),
]


def selftest(rules, abbr):
    import yaml
    ok = True
    for rel, lines, want in SELFTEST:
        notes = []
        lang = lang_of(rel)
        new = [rewrite_line(l, rules, abbr, rel) for l in lines]
        new = resolve_marks(lines, new, lang, rel, notes)
        err = validate('\n'.join(new), lang) if lang else None
        if not err and lang in ('py', 'yaml'):
            err = deep_check('\n'.join(lines), '\n'.join(new), lang)
        if not err and want is not None and new != want:
            err = 'got %r' % new
        if not err and want is None and new != lines:
            err = 'audio/tileset line changed'
        if not err and lang in ('py', 'yaml'):     # Ruby inside script values must still parse after the rename
            vals = []
            if lang == 'py':
                import ast
                vals = [v for v in _py_strings(ast.parse('\n'.join(new))) if v.startswith('pb')]
            else:
                for d in yaml.safe_load_all('\n'.join(new)):
                    vals += [x['script'] for x in (d or []) if isinstance(x, dict) and 'script' in x]
            r = ruby_query({'parse': vals})
            if r is None or not all(r['parses']):
                err = 'a script value does not parse as Ruby: %r' % vals
        print('%s %s %s%s' % ('ok  ' if not err else 'FAIL', rel, err or new, (' | ' + '; '.join(notes)) if notes else ''))
        ok = ok and not err
    return ok


def main():
    rows, prose = load_table()
    global NAMES
    NAMES = [(n[4:] if n.startswith('The ') else n, n.split()[-1]) for _, o, n in rows]
    rules = build_rules(rows, prose)
    abbr = abbrev_rules(rows)
    apply = '--apply' in sys.argv
    if '--selftest' in sys.argv:
        sys.exit(0 if selftest(rules, abbr) else 1)
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
    diffs, changed, nlines = process(apply, rules, abbr)
    os.makedirs(os.path.dirname(DIFF_OUT), exist_ok=True)
    open(DIFF_OUT, 'w', encoding='utf-8').write('\n'.join(diffs) + '\n')
    print('%s: %d files, %d lines %s. Diff: %s' % ('APPLIED' if apply else 'DRY RUN', changed, nlines,
                                                 'changed' if apply else 'would change', os.path.relpath(DIFF_OUT, ROOT)))
    if not apply:
        print('Re-run with --apply to write them. Then regenerate: ruby tools/field_defaults_to_rb.rb, mapgen build.')


if __name__ == '__main__':
    main()
