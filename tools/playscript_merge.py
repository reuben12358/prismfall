#!/usr/bin/env python3
"""Merge the presentation layer of Gemini's "playscripts" into the canonical story scripts, without changing a word.

  python3 -I tools/playscript_merge.py --check                 # what would change, per file (writes nothing)
  python3 -I tools/playscript_merge.py --write [FILE ...]      # apply (FILE = 35_SCRIPT_CH16.md ...; default: all 22)
  python3 -I tools/playscript_merge.py --report /tmp/div.txt   # the full divergence list (what was NOT taken, and why)
  python3 -I tools/playscript_merge.py --check --out /tmp/dir  # merged copies for a look, story/ untouched

Source: gemini_recommends/2026-11-24_playscript-dialogue-and-expressions/act1_2 and act3_5 (22 files), each a copy of
story/NN_SCRIPT_*.md with (a) long lines cut into one- or two-line boxes, (b) fewer expression changes
([name: Speaker] holds the last face), (c) emote cues, and (d) some reworded lines and stage directions.

The canonical scripts keep every word. Inside fenced blocks only, for each canonical line:
  * its words are aligned with the playscript's (case-insensitively, tags aside);
  * where the playscript starts a new box at a point the alignment can place exactly in the canonical line, the
    canonical line is cut there, so the boxes are the playscript's and the words are the canon's;
  * each box takes the playscript's tag when it names the same speaker and the portrait file exists
    (graphics/Portraits/ID_expr.png): [portrait: ID, expr] for a change of face, [name: Speaker] for a hold. A hold
    is only written where it yields the face the playscript meant; otherwise the tag is spelled out;
  * an inline "(stage direction)" the playscript moved to its own line becomes its own line, in the canon's words;
  * an emote cue (\\pfe[kind] or [emote: kind]) is written as [emote: kind] after the speaker tag.
Never taken: a changed word or punctuation mark, a new or dropped line, a new speaker id (a portrait for someone the
canon keeps plain), a new [bubble: ...], an expression with no art. Those are listed by --report.
Running it again on merged files changes nothing.
"""
import collections
import difflib
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORY = os.path.join(ROOT, "story")
PLAY = os.path.join(ROOT, "gemini_recommends", "2026-11-24_playscript-dialogue-and-expressions")
PORTRAITS = os.path.join(ROOT, "graphics", "Portraits")
EMOTES = {"exclaim", "double_exclaim", "question", "dots", "anger", "sweat", "heart", "idea", "music", "jolt"}

TAG = re.compile(r"\[(portrait|bubble|name):\s*([^\]]*)\]")
EMO = re.compile(r"\\pfe\[([^\]]*)\]|\[emote:\s*([^\]]*)\]")
TOKEN = re.compile(r"[^\W_]+(?:['’][^\W_]+)*|[^\w\s]|_")
NORM = {"’": "'", "‘": "'", "“": '"', "”": '"'}


def files():
    out = []
    for sub in ("act1_2", "act3_5"):
        for f in sorted(os.listdir(os.path.join(PLAY, sub))):
            if f.endswith(".md") and os.path.exists(os.path.join(STORY, f)):
                out.append((f, os.path.join(PLAY, sub, f)))
    return sorted(out)


def art_aliases():
    """register(:SALLOW, ..., art: :RENATA) lines in 014_Portraits.rb: a script id that borrows another's files."""
    out = {}
    path = os.path.join(ROOT, "plugins", "Prismfall Cutscenes", "014_Portraits.rb")
    if os.path.exists(path):
        for m in re.finditer(r"register\(:(\w+),[^\n]*?\bart:\s*:(\w+)", open(path, encoding="utf-8").read()):
            out[m.group(1).upper()] = m.group(2).upper()
    return out


ALIASES = art_aliases()


def art_exists(pid, expr):
    pid = ALIASES.get(pid, pid)
    ids = ["PLAYER_A", "PLAYER_B"] if pid == "PLAYER" else [pid]
    return all(os.path.exists(os.path.join(PORTRAITS, "%s_%s.png" % (i, expr))) for i in ids)


class Line:
    """One line inside a fenced block."""
    __slots__ = ("no", "raw", "indent", "kind", "who", "fields", "emotes", "body", "tokens", "spans", "late_tag", "block")

    def __init__(self, no, raw, block):
        self.no = no
        self.raw = raw
        self.block = block
        m = re.match(r"\s*", raw)
        self.indent = m.group(0)
        rest = raw[len(self.indent):]
        self.kind = None          # portrait / bubble / name / None
        self.who = None           # the id (portrait, bubble) or the display name (name)
        self.fields = []
        m = TAG.match(rest)
        if m:
            self.kind = m.group(1)
            self.fields = [x.strip() for x in m.group(2).split(",")]
            self.who = self.fields[0].upper() if self.kind != "name" else self.fields[0]
            rest = rest[m.end():]
        self.emotes = [(a or b).strip() for a, b in EMO.findall(rest)]
        self.late_tag = bool(TAG.search(rest))
        self.body = rest                      # emote cues still inside; spans index into this
        self.tokens = []
        self.spans = []
        masked = EMO.sub(lambda mm: " " * len(mm.group(0)), rest)
        for t in TOKEN.finditer(masked):
            self.tokens.append(NORM.get(t.group(0), t.group(0)).lower().replace("’", "'"))
            self.spans.append(t.span())

    @property
    def expr(self):
        return (self.fields[1].lower() if len(self.fields) > 1 and self.fields[1] else "neutral") if self.kind in ("portrait", "bubble") else None


def fenced(text):
    """-> (all lines, [Line] for the lines inside ``` fences)"""
    lines = text.split("\n")
    out = []
    inside = False
    block = 0
    for i, l in enumerate(lines):
        if l.lstrip().startswith("```"):
            inside = not inside
            block += 1 if inside else 0
            continue
        if inside:
            out.append(Line(i, l, block))
    return lines, out


def clean_body(text):
    """A piece of a canonical body with its emote cues taken out."""
    return re.sub(r"[ \t]{2,}", " ", EMO.sub("", text)).strip()


def sentence_direction(text):
    """(She checks the seals.) / (A pause.) - a full sentence, which can stand on a line of its own."""
    t = text.strip()
    return bool(re.match(r"^\([A-Z\\][^()]*[.!?…][\"'”’]?\)$", t))


def pure_direction(text):
    return bool(re.match(r"^\([^()]*(?:\([^()]*\)[^()]*)*\)[.!?…]*$", text.strip()))


def same_speaker(c, p):
    """The playscript line's tag names the canonical line's speaker."""
    if p.kind is None or c.kind is None:
        return False
    if c.kind in ("portrait", "bubble"):
        if p.kind in ("portrait", "bubble"):
            return p.who == c.who
        name = p.who.lower()
        cid = c.who.lower().replace("_", " ")
        return name == cid or cid in name.split() or name.split()[0] == cid.split()[0]
    if p.kind == "name":
        return p.who.lower() == c.who.lower()
    return False


def merge_file(name, play_path, report):
    canon_text = open(os.path.join(STORY, name), encoding="utf-8").read()
    lines, cl = fenced(canon_text)
    _, pl = fenced(open(play_path, encoding="utf-8").read())
    ct = [(i, k) for i, l in enumerate(cl) for k in range(len(l.tokens))]
    pt = [(j, k) for j, l in enumerate(pl) for k in range(len(l.tokens))]
    sm = difflib.SequenceMatcher(None, [cl[i].tokens[k] for i, k in ct], [pl[j].tokens[k] for j, k in pt], autojunk=False)
    p2c = {}
    for a, b, n in sm.get_matching_blocks():
        for d in range(n):
            p2c[b + d] = a + d
    c2p = {v: k for k, v in p2c.items()}
    pstart = {}
    off = 0
    for j, l in enumerate(pl):
        pstart[j] = off
        off += len(l.tokens)
    cstart = {}
    off = 0
    for i, l in enumerate(cl):
        cstart[i] = off
        off += len(l.tokens)
    # play lines by the canonical line most of their matched words fall in
    owner = {}
    straddle = set()
    for j, l in enumerate(pl):
        hits = collections.Counter(ct[p2c[pstart[j] + k]][0] for k in range(len(l.tokens)) if pstart[j] + k in p2c)
        if not hits:
            continue
        owner[j] = hits.most_common(1)[0][0]
        if len(hits) > 1:
            straddle.update(hits.keys())
    by_canon = collections.defaultdict(list)
    for j, i in owner.items():
        by_canon[i].append(j)
    # the face each playscript line shows (a hold = the speaker's last tag in the same block)
    play_face = {}
    state = {}
    last_block = None
    for j, l in enumerate(pl):
        if l.block != last_block:
            state = {}
            last_block = l.block
        if l.kind in ("portrait", "bubble"):
            state[l.who] = l.expr
            play_face[j] = (l.who, l.expr)
    stats = collections.Counter()
    out_lines = {}
    merged_state = {}
    last_block = None
    used_play = set()
    last_indent = None
    for i, c in enumerate(cl):
        # a hold is only safe in a straight run of lines: a new block, a choice ("> ...") or a branch (the indent
        # changes) starts again with the face spelled out
        if c.block != last_block or c.indent != last_indent or c.raw.lstrip().startswith(">"):
            merged_state = {}
            last_block = c.block
            last_indent = c.indent
        js = sorted(by_canon.get(i, []))
        used_play.update(js)
        identical = bool(js) and [t for j in js for t in pl[j].tokens] == c.tokens and not (i in straddle)
        result = None
        if js and not c.late_tag and i not in straddle and not any(pl[j].late_tag for j in js) and c.tokens:
            result = reflow(c, [pl[j] for j in js], js, cstart[i], pstart, p2c, play_face, merged_state, stats, report, name)
        if result is None:
            result = [c.raw]
            if c.kind in ("portrait", "bubble"):
                merged_state[c.who] = c.expr
        elif c.kind in ("portrait", "bubble") and not any(TAG.match(r.strip()) for r in result):
            pass
        if not identical and c.tokens:
            if not js:
                stats["canon_only"] += 1
                report.append((name, c.no + 1, "canon only (kept)", c.raw.strip(), ""))
            else:
                kind = "direction / system line differs (canon kept)"
                if c.kind:
                    sub = difference(c, [pl[j] for j in js])
                    kind = "%s (canon kept)" % sub
                    stats["diff: " + sub] += 1
                stats["reworded" if c.kind else "direction"] += 1
                report.append((name, c.no + 1, kind, c.raw.strip(), " / ".join(pl[j].raw.strip() for j in js)))
        if result != [c.raw]:
            stats["lines_changed"] += 1
            stats["boxes_added"] += len(result) - 1
            out_lines[c.no] = result
    for j, l in enumerate(pl):
        if j not in used_play and l.tokens:
            stats["play_only"] += 1
            report.append((name, 0, "playscript only (not taken)", "", l.raw.strip()))
        elif j not in used_play and l.emotes:
            stats["emote_alone"] += 1
            report.append((name, 0, "emote cue on a line of its own (not taken)", "", l.raw.strip()))
    new = []
    for n, l in enumerate(lines):
        new.extend(out_lines.get(n, [l]))
    return canon_text, "\n".join(new), stats


def reflow(c, plist, js, c0, pstart, p2c, play_face, merged_state, stats, report, name):
    """-> the lines that replace canonical line c, or None to keep it as it is."""
    # where each playscript box starts, as a token index of the canonical line (None = cannot be placed)
    cuts = [0]
    groups = [[0]]
    for n in range(1, len(plist)):
        prev, cur = plist[n - 1], plist[n]
        a = pstart[js[n - 1]] + len(prev.tokens) - 1
        b = pstart[js[n]]
        ca, cb = p2c.get(a), p2c.get(b)
        ok = prev.tokens and cur.tokens and ca is not None and cb is not None and cb > ca and 0 < cb - c0 < len(c.tokens) and ca >= c0
        if ok and cb != ca + 1:                  # only a canon-only cue or aside may sit between: *(music note)*, (a beat)
            gap = c.body[c.spans[ca - c0][1]:c.spans[cb - c0][0]].strip()
            ok = bool(re.match(r"^(?:\*?\([^()]*\)\*?\s*)+$", gap))
        if ok:
            cuts.append(cb - c0)
            groups.append([n])
        else:
            groups[-1].append(n)
    # a bracketed fragment the playscript set on its own line ("(pulling)", "(a shrug)") says who does it only while it
    # sits in that speaker's line: keep it there (joined to the box after it, or the one before at the end of a line)
    g = 0
    while g < len(cuts) and len(cuts) > 1:
        start = c.spans[cuts[g]][0] if cuts[g] else 0
        end = c.spans[cuts[g + 1]][0] if g + 1 < len(cuts) else len(c.body)
        text = clean_body(c.body[start:end])
        if plist[groups[g][0]].kind is None and pure_direction(text) and not sentence_direction(text):
            if g + 1 < len(cuts):
                groups[g + 1] = groups[g + 1] + groups[g]      # the tagged box's line first
                del cuts[g + 1]
                del groups[g]
            else:
                groups[g - 1] = groups[g - 1] + groups[g]
                del cuts[g]
                del groups[g]
            continue
        g += 1
    pieces = []
    for g, cut in enumerate(cuts):
        start = c.spans[cut][0] if cut else 0
        end = c.spans[cuts[g + 1]][0] if g + 1 < len(cuts) else len(c.body)
        raw_piece = c.body[start:end]
        pieces.append((clean_body(raw_piece), [e for e in (x.strip() for a, b in EMO.findall(raw_piece) for x in [a or b]) if e]))
    if any(not text for text, _ in pieces):
        return None
    out = []
    state = dict(merged_state)
    for g, (text, own_emotes) in enumerate(pieces):
        p = plist[groups[g][0]]
        emotes = list(own_emotes)
        for n in groups[g]:
            for e in plist[n].emotes:
                kind = e.split(",")[0].strip().lower()
                if kind in EMOTES and e not in emotes and same_or_plain(c, plist[n]):
                    emotes.append(e)
                    stats["emotes"] += 0 if e in c.emotes else 1
        emo = "".join(" [emote: %s]" % e for e in emotes)
        if c.kind is None:
            if p.kind is not None or len(pieces) > 1:
                return None                      # the canon line has no speaker: leave it whole
            return None
        if p.kind is None:
            if pure_direction(text) and not emotes:
                out.append(c.indent + text)      # a stage direction on its own line
                stats["directions_out"] += 1
                continue
            return None
        tag = None
        if not same_speaker(c, p):
            if g == 0:
                stats["speaker_differs"] += 1
                what = "a face for a line the canon keeps plain" if c.kind == "name" else "speaker id differs"
                report.append((name, c.no + 1, "%s (canon tag kept)" % what, c.raw.strip()[:160], p.raw.strip()[:160]))
            tag = canon_tag(c, g, state)
        elif c.kind == "name":
            tag = "[name: %s]" % c.who
        elif c.kind == "bubble":
            tag = canon_tag(c, g, state)          # the canon's own bubble stays as written
        else:
            want = None
            if p.kind == "bubble":
                if g == 0:
                    stats["bubble_new"] += 1
                    report.append((name, c.no + 1, "new [bubble:] (kept as a face)", c.raw.strip()[:160], p.raw.strip()[:160]))
                want = p.expr
            elif p.kind == "portrait":
                want = p.expr
            else:
                want = play_face.get(("hold", js[groups[g][0]]))
            if p.kind == "name":
                want = hold_expr(plist, groups[g][0], js, play_face, c.who)
            if want is None or not art_exists(c.who, want):
                if want is not None and g == 0:
                    report.append((name, c.no + 1, "expression has no art (canon tag kept)", c.raw.strip()[:160], p.raw.strip()[:160]))
                want = c.expr if g == 0 else state.get(c.who, c.expr)
                if not art_exists(c.who, want):
                    want = c.expr
            if p.kind == "name" and state.get(c.who) == want:
                tag = "[name: %s]" % p.who
                stats["holds"] += 1
            else:
                tag = "[portrait: %s, %s]" % (c.who, want)
                if g == 0 and want != c.expr:
                    stats["expr_changed"] += 1
            state[c.who] = want
        out.append("%s%s%s %s" % (c.indent, tag, emo, text))
    merged_state.clear()
    merged_state.update(state)
    return out


def difference(c, plist):
    """What the playscript changed in a spoken line."""
    word = re.compile(r"^[^\W_]")
    cw = [t for t in c.tokens if word.match(t)]
    pw = [t for l in plist for t in l.tokens if word.match(t)]
    if cw == pw:
        return "punctuation only"
    stripped = Line(0, re.sub(r"\*?\([^()]*\)\*?", " ", c.body), 0)
    pstripped = [Line(0, re.sub(r"\*?\([^()]*\)\*?", " ", l.body), 0) for l in plist]
    if [t for t in stripped.tokens if word.match(t)] == [t for l in pstripped for t in l.tokens if word.match(t)]:
        return "bracketed cue or aside dropped or reworded"
    return "words changed"


def same_or_plain(c, p):
    return p.kind is None or same_speaker(c, p) or c.kind is None


def canon_tag(c, g, state):
    """The canonical line's own tag for its first box; later boxes hold."""
    if c.kind == "name":
        return "[name: %s]" % c.who
    if g == 0:
        state[c.who] = c.expr
        return "[%s: %s]" % (c.kind, ", ".join(c.fields))
    if c.kind == "bubble":
        return "[portrait: %s, %s]" % (c.who, state.get(c.who, c.expr))
    return "[portrait: %s, %s]" % (c.who, state.get(c.who, c.expr))


_HOLD = {}


def hold_expr(plist, n, js, play_face, who):
    """The face a [name: X] hold shows in the playscript: X's last portrait tag earlier in the same block."""
    return _HOLD.get(js[n])


def prepare_holds(play_path):
    _HOLD.clear()
    _, pl = fenced(open(play_path, encoding="utf-8").read())
    state = {}
    last = None
    for j, l in enumerate(pl):
        if l.block != last:
            state = {}
            last = l.block
        if l.kind in ("portrait", "bubble"):
            state[l.who] = l.expr
            for word in l.who.lower().split("_"):
                state.setdefault("name:" + word, None)
                state["name:" + word] = l.expr
            state["name:" + l.who.lower().replace("_", " ")] = l.expr
        elif l.kind == "name":
            key = l.who.lower()
            e = state.get("name:" + key) or state.get("name:" + key.split()[0])
            if e:
                _HOLD[j] = e


def check_tags(text, name, problems):
    """Every [portrait:] / [bubble:] in a merged file has art; every emote is a known kind."""
    for no, l in enumerate(text.split("\n"), 1):
        for m in TAG.finditer(l):
            if m.group(1) == "name":
                continue
            f = [x.strip() for x in m.group(2).split(",")]
            pid = f[0].upper()
            expr = f[1].lower() if len(f) > 1 and f[1] else "neutral"
            if not re.match(r"^[A-Z][A-Z0-9_]*$", f[0]) or pid in ("NAME", "ID", "SPEAKER", "CAST_ID") or not re.match(r"^[a-z_]+$", expr) or expr in ("expr", "expression"):
                continue                                   # a template such as [portrait: NAME, expr]
            if not art_exists(pid, expr):
                real = ALIASES.get(pid, pid)
                base = all(os.path.exists(os.path.join(PORTRAITS, i + ".png")) for i in (["PLAYER_A", "PLAYER_B"] if real == "PLAYER" else [real]))
                problems.append((name, no, pid, expr, "falls back to %s.png" % pid if base else "NO ART: plain box"))
        for a, b in EMO.findall(l):
            kind = (a or b).split(",")[0].strip().lower()
            if kind not in EMOTES and kind not in ("emote", "kind"):
                problems.append((name, no, "emote", kind, "unknown emote"))


def main():
    global STORY
    args = sys.argv[1:]
    if "--story" in args:                                  # another folder of scripts (to test a merged copy)
        STORY = args[args.index("--story") + 1]
    write = "--write" in args
    rep_path = args[args.index("--report") + 1] if "--report" in args else None
    out_dir = args[args.index("--out") + 1] if "--out" in args else None     # merged copies, for a look before --write
    only = [a for a in args if a.endswith(".md")]
    report = []
    problems = []
    total = collections.Counter()
    for name, play_path in files():
        if only and name not in only:
            continue
        prepare_holds(play_path)
        old, new, stats = merge_file(name, play_path, report)
        check_tags(new, name, problems)
        total.update(stats)
        print("%-24s boxes +%-4d lines cut %-4d holds %-4d faces changed %-3d emotes +%-2d directions out %-3d | not taken: reworded %-3d directions %-3d play-only %-3d canon-only %-3d speaker %-2d bubbles %d%s" % (
            name, stats["boxes_added"], stats["lines_changed"], stats["holds"], stats["expr_changed"], stats["emotes"], stats["directions_out"],
            stats["reworded"], stats["direction"], stats["play_only"], stats["canon_only"], stats["speaker_differs"], stats["bubble_new"],
            "" if new != old else "  (no change)"))
        if write and new != old:
            with open(os.path.join(STORY, name), "w", encoding="utf-8") as f:
                f.write(new)
        if out_dir:
            with open(os.path.join(out_dir, name), "w", encoding="utf-8") as f:
                f.write(new)
    print("TOTAL " + ", ".join("%s %d" % kv for kv in sorted(total.items())))
    for p in problems:
        print("TAG %s:%d %s %s -> %s" % p)
    print("%d tag problems" % len(problems))
    if rep_path:
        with open(rep_path, "w", encoding="utf-8") as f:
            for name, no, kind, canon, play in report:
                f.write("%s:%s  %s\n    canon: %s\n    play:  %s\n" % (name, no or "-", kind, canon, play))
        print("report: %s (%d entries)" % (rep_path, len(report)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
