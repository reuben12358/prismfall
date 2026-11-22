#!/usr/bin/env python3
"""Render the story bible, the playable scripts and the guides (story/*.md, design/WALKTHROUGH, CHAPTER_BEATS,
FIELD_LOGIC_AUDIT, WORLD_MAP, CAMEOS) into one readable HTML page: dist_web/codex.html."""
import html, pathlib, re, markdown

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "dist_web" / "codex.html"

# (group, [(file, anchor, short label, spoiler?)]) - Gemini review 2026-11-21: bible first, guides last
GROUPS = [
    ("Story bible", [
        ("story/00_OVERVIEW.md", "overview", "Overview", False),
        ("story/01_WORLD_LORE.md", "world", "World & lore", False),
        ("design/WORLD_MAP.md", "geography", "Geography", False),   # Geography v2 (SPINE Rev 18)
        ("story/02_FACTIONS.md", "factions", "Factions", False),
        ("story/03_CAST.md", "cast", "Cast", False),
        ("story/04_ACT_I.md", "act-1", "Act I", False),
        ("story/05_ACT_II.md", "act-2", "Act II", False),
        ("story/06_ACT_III.md", "act-3", "Act III", True),
        ("story/07_ACT_IV.md", "act-4", "Act IV", True),
        ("story/08_ACT_V.md", "act-5", "Act V", True),
        ("story/09_MYSTERIES_FORESHADOWING.md", "mysteries", "Mysteries", True),
        ("story/14_WAR_AND_BLESSING.md", "war", "War & the Blessing", True),
        ("story/10_CHOICES_ENDINGS.md", "choices", "Choices & endings", True),
        ("story/12_RUIN_ROUTE.md", "ruin", "Ruin Route", True),
        ("story/13_CUTSCENES.md", "cutscenes", "Cutscenes", False),
        ("story/15_COMEDY.md", "comedy", "Comedy", False),
        ("story/11_FINALE_LINES.md", "finale", "Finale lines", True),
    ]),
    ("Playable scripts", [
        ("story/20_SCRIPT_CH0-2.md", "script-ch0-2", "Ch 0-2", False),
        ("story/21_SCRIPT_CH3.md", "script-ch3", "Ch 3", False),
        ("story/23_SCRIPT_CH4.md", "script-ch4", "Ch 4", False),
        ("story/24_SCRIPT_CH5.md", "script-ch5", "Ch 5", False),
        ("story/25_SCRIPT_CH6.md", "script-ch6", "Ch 6", False),
        ("story/26_SCRIPT_CH7.md", "script-ch7", "Ch 7", False),
        ("story/29_SCRIPT_CH8.md", "script-ch8", "Ch 8", False),      # the real Ch8 when written (22_ is the withdrawn Ring-Day stub)
        ("story/27_SCRIPT_CH9.md", "script-ch9", "Ch 9", True),
        ("story/28_SCRIPT_CH10.md", "script-ch10", "Ch 10", True),
        ("story/30_SCRIPT_CH11.md", "script-ch11", "Ch 11", True),
        ("story/31_SCRIPT_CH12.md", "script-ch12", "Ch 12", True),
        ("story/32_SCRIPT_CH13.md", "script-ch13", "Ch 13", True),
    ]),
    ("Guides & reference", [
        ("design/WALKTHROUGH.md", "walkthrough", "Walkthrough", True),   # BIGJRA-style player's guide
        ("design/CHAPTER_BEATS.md", "chapter-beats", "Chapter beats", True),
        ("design/FIELD_LOGIC_AUDIT.md", "field-audit", "Field logic", False),
        ("design/CAMEOS.md", "cameos", "Sidequest cameos", False),
    ]),
]
CHAPTERS = [(f, a, l) for _, items in GROUPS for (f, a, l, _) in items]

# Gym order (SPINE; Revision 14 put Saltmere first): type, city
GYMS = [("Normal","Saltmere"),("Bug","Briarwick"),("Water","Ebbmouth"),("Electric","Lumen City"),
        ("Ground","Duneholt"),("Poison","Mirefen"),("Fire","Cindervault"),("Fighting","Ironreach"),
        ("Grass","Verdance"),("Ice","Rimeholt"),("Flying","Skyreach"),("Psychic","Lucent"),
        ("Rock","Cragholm"),("Ghost","Gravenmoor"),("Steel","Cogsworth"),("Dark","Underveil"),
        ("Fairy","Gloaming"),("Dragon","Wyrmrest")]
TYPE_COL = {"Bug":"#91a119","Normal":"#9fa19f","Water":"#2980ef","Electric":"#fac000","Ground":"#915121",
            "Poison":"#9141cb","Fire":"#e62829","Fighting":"#ff8000","Grass":"#3fa129","Ice":"#3dcef3",
            "Flying":"#81b9ef","Psychic":"#ef4179","Rock":"#afa981","Ghost":"#704170","Steel":"#60a1b8",
            "Dark":"#624d4e","Fairy":"#ef70ef","Dragon":"#5060e1"}

LIST_RE = re.compile(r"^(\s*)([-*+]\s+|\d+\.\s+)")
TABLE_HEAD_RE = re.compile(r"^\|.*\|\s*$")

def prepass(md_text):
    """Python-Markdown needs a blank line before a list or table that follows prose (GitHub doesn't)."""
    out, fence = [], False
    lines = md_text.split("\n")
    for i, ln in enumerate(lines):
        if ln.lstrip().startswith("```"):
            fence = not fence
        prev = out[-1] if out else ""
        if not fence and prev.strip() and not ln.startswith(" "):
            starts_list = LIST_RE.match(ln) and not LIST_RE.match(prev) and not prev.lstrip().startswith(("|", ">", "#"))
            nxt = lines[i + 1] if i + 1 < len(lines) else ""
            starts_table = TABLE_HEAD_RE.match(ln) and re.match(r"^\|[\s:|-]+\|\s*$", nxt) and not TABLE_HEAD_RE.match(prev)
            if starts_list or starts_table:
                out.append("")
        out.append(ln)
    return "\n".join(out)

TAG_RE = re.compile(r"\[(portrait|bubble|name): ([^\]]+)\]")

def style_script(body):
    """Script readability: \\PN -> [Player], [portrait: NAME, expr] -> a small speaker tag."""
    body = body.replace("\\PN", '<span class="pc">[Player]</span>')
    def tag(m):
        parts = [p.strip() for p in m.group(2).split(",")]
        who = parts[0].title().replace("_", " ")
        rest = " · ".join(parts[1:])
        return f'<span class="tag tag-{m.group(1)}">{html.escape(who)}{(" · " + html.escape(rest)) if rest else ""}</span>'
    return TAG_RE.sub(tag, body)

def render(md_text, prefix):
    md_text = prepass(md_text)
    md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists", "toc"],
                           extension_configs={"toc": {"slugify": lambda v, s: prefix + "-" + re.sub(r"[^a-z0-9]+", "-", v.lower()).strip("-")}})
    body = md.convert(md_text)
    # wide tables scroll on phones
    body = body.replace("<table>", '<div class="scroll"><table>').replace("</table>", "</table></div>")
    return style_script(body)

def prism_svg():
    rays = []
    n = len(GYMS)
    for i, (t, city) in enumerate(GYMS):
        y = 40 + i * (520 / (n - 1))
        rays.append(f'<path d="M260 300 L800 {y:.1f}" stroke="{TYPE_COL[t]}" stroke-width="9" stroke-linecap="round" opacity=".9"/>'
                    f'<text x="815" y="{y + 7:.1f}" class="ray">{i + 1}. {html.escape(city)}</text>')
    return f'''<svg viewBox="0 0 1200 600" role="img" aria-label="A prism splitting light into the eighteen gym types">
  <defs><linearGradient id="beam" x1="0" x2="1"><stop offset="0" stop-color="currentColor" stop-opacity="0"/><stop offset="1" stop-color="currentColor" stop-opacity=".9"/></linearGradient>
  <linearGradient id="glass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="#9fb6c8" stop-opacity=".18"/></linearGradient></defs>
  <path d="M0 300 L260 300" stroke="url(#beam)" stroke-width="12" stroke-linecap="round"/>
  {''.join(rays)}
  <polygon points="260,120 390,420 130,420" fill="url(#glass)" stroke="currentColor" stroke-opacity=".5" stroke-width="3"/>
  <polygon points="260,120 290,420 130,420" fill="#fff" opacity=".12"/>
</svg>'''

def main():
    sections, navgroups = [], []
    for group, items in GROUPS:
        links = []
        for path, anchor, label, spoiler in items:
            p = ROOT / path
            if not p.exists():
                continue
            pill = '<span class="spoil" title="Spoilers">spoilers</span>' if spoiler else ""
            links.append(f'<a href="#{anchor}">{html.escape(label)}{pill}</a>')
            banner = '<p class="spoilbar">Spoilers ahead: this chapter covers late-game twists.</p>' if spoiler else ""
            sections.append(f'<section class="chapter" id="{anchor}" data-label="{html.escape(label)}">{banner}{render(p.read_text(encoding="utf-8"), anchor)}</section>')
        if links:
            navgroups.append(f'<div class="grp"><span class="gl">{html.escape(group)}</span>{"".join(links)}</div>')
    words = sum(len((ROOT / c[0]).read_text(encoding="utf-8").split()) for c in CHAPTERS if (ROOT / c[0]).exists())
    page = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Prismfall Codex</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Spectral:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@400;600&display=swap" rel="stylesheet">
<style>
/* VOICE: a chronicle you settle into — calm, bookish, unhurried.
   IDEA: an illuminated codex of Velmora, opened at the Prismfall.
   PICTURE: a glass prism splitting one beam into the eighteen type-coloured gym rays, each named.
   COLOUR and TYPE: white page / deep slate night; ink near-black; the 18 type colours are the only accents. Spectral for reading, Inter for navigation.
   LAYOUT: title + prism band, chapter nav that wraps (sticky on wide screens), then a single 68ch reading column. */
:root{{color-scheme:light dark;--bg:light-dark(#ffffff,#12161b);--ink:light-dark(#17191d,#e7e9ec);--muted:light-dark(#5b6068,#9aa3ad);--rule:light-dark(#e4e6ea,#262c33);--panel:light-dark(#f4f6f8,#192027);--link:light-dark(#1f5fbf,#8db8ff)}}
:root[data-theme=light]{{color-scheme:light}}:root[data-theme=dark]{{color-scheme:dark}}
*{{box-sizing:border-box;min-width:0}}
body{{margin:0;background:var(--bg);color:var(--ink);font:17px/1.65 Spectral,Georgia,serif;overflow-x:clip}}
.band{{padding:clamp(28px,4vw,64px) max(5vw,16px)}}
header.band{{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.4fr);gap:clamp(16px,3vw,48px);align-items:center;border-bottom:1px solid var(--rule)}}
h1{{font:700 clamp(34px,5vw,52px)/1.05 Spectral,Georgia,serif;margin:0 0 14px;text-wrap:balance}}
.lede{{color:var(--muted);font-size:18px;max-width:42ch;margin:0}}
.meta{{font:13px/1.4 Inter,system-ui,sans-serif;color:var(--muted);margin-top:16px}}
.prism{{color:var(--ink)}} .prism svg{{width:100%;height:auto;display:block}}
.ray{{font:600 22px Inter,system-ui,sans-serif;fill:var(--muted)}}
nav{{position:sticky;top:0;z-index:5;background:var(--bg);border-bottom:1px solid var(--rule);padding:8px max(5vw,16px);font:600 14px/1.3 Inter,system-ui,sans-serif}}
nav details{{}} nav summary{{cursor:pointer;min-height:44px;display:flex;align-items:center;gap:12px;color:var(--ink)}}
.grp{{display:flex;flex-wrap:wrap;gap:2px 16px;align-items:center;padding:4px 0}}
.gl{{font:700 11px/1 Inter,system-ui,sans-serif;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);min-width:9.5em}}
nav a{{color:var(--muted);text-decoration:none;padding:6px 0;min-height:36px;display:inline-flex;align-items:center;gap:6px}}
.spoil{{font:700 10px/1 Inter,sans-serif;text-transform:uppercase;letter-spacing:.05em;color:#b4542a;border:1px solid currentColor;border-radius:9px;padding:2px 6px}}
.spoilbar{{font:600 13px/1.4 Inter,sans-serif;color:#b4542a;background:var(--panel);border-left:3px solid #b4542a;padding:8px 12px;border-radius:4px}}
.tools{{display:flex;gap:10px;align-items:center;margin-left:auto}}
#q{{font:15px Inter,sans-serif;padding:8px 10px;border:1px solid var(--rule);border-radius:6px;background:var(--panel);color:var(--ink);width:min(320px,60vw)}}
#hits{{position:absolute;right:max(5vw,16px);top:100%;width:min(460px,90vw);max-height:60vh;overflow:auto;background:var(--bg);border:1px solid var(--rule);border-radius:8px;box-shadow:0 8px 24px rgb(0 0 0/.18);font:14px/1.4 Inter,sans-serif;display:none}}
#hits a{{display:block;padding:8px 12px;color:var(--ink);text-decoration:none;border-bottom:1px solid var(--rule)}} #hits a small{{color:var(--muted);display:block}}
#theme{{font:600 14px Inter,sans-serif;min-height:40px;padding:0 12px;border:1px solid var(--rule);border-radius:6px;background:var(--panel);color:var(--ink);cursor:pointer}}
.chapter :is(h1,h2,h3,h4),.chapter{{scroll-margin-top:84px}}
.tag{{font:600 12px/1 Inter,sans-serif;color:var(--muted);background:var(--bg);border:1px solid var(--rule);border-radius:4px;padding:1px 5px}}
.pc{{font-weight:700;color:var(--link)}}
nav a:hover,nav a:focus-visible{{color:var(--ink)}}
main{{padding:0 max(5vw,16px) 80px}}
.chapter{{max-width:68ch;margin:0 auto;padding-top:48px;border-top:1px solid var(--rule)}}
.chapter:first-child{{border-top:0}}
.chapter h1{{font-size:clamp(30px,4vw,42px);margin-top:0}}
h2{{font:600 26px/1.2 Spectral,Georgia,serif;margin:2.2em 0 .6em;text-wrap:balance}}
h3{{font:600 20px/1.3 Spectral,Georgia,serif;margin:1.8em 0 .4em}}
h4{{font:600 16px/1.3 Inter,system-ui,sans-serif;margin:1.6em 0 .3em}}
a{{color:var(--link)}}
blockquote{{margin:1.2em 0;padding:.2em 1.1em;border-left:3px solid var(--rule);color:var(--muted);font-style:italic}}
code{{font:14px/1.4 ui-monospace,Menlo,monospace;background:var(--panel);padding:1px 5px;border-radius:4px}}
pre{{background:var(--panel);padding:14px;border-radius:6px;overflow-x:auto}} pre code{{background:none;padding:0}}
.scroll{{overflow-x:auto;margin:1.2em 0}}
table{{border-collapse:collapse;font:14px/1.45 Inter,system-ui,sans-serif;min-width:100%}}
th,td{{text-align:left;vertical-align:top;padding:8px 10px;border-bottom:1px solid var(--rule)}}
th{{font-weight:600;background:var(--panel)}}
hr{{border:0;border-top:1px solid var(--rule);margin:2.4em 0}}
.top{{position:fixed;right:16px;bottom:16px;width:44px;height:44px;border-radius:50%;display:grid;place-items:center;background:var(--panel);color:var(--ink);text-decoration:none;border:1px solid var(--rule);font:600 18px Inter,sans-serif}}
@media(max-width:760px){{header.band{{grid-template-columns:1fr}} nav{{position:static}} body{{font-size:16.5px}}}}
@media(prefers-reduced-motion:no-preference){{html{{scroll-behavior:smooth}}}}
</style></head>
<body>
<header class="band">
  <div><h1>The Prismfall Codex</h1>
  <p class="lede">The story bible for Pokémon Prismfall: the realm of Velmora, its seven kingdoms, eighteen Wardens and the Festival of Champions.</p>
  <p class="meta">Working draft · {words:,} words · {len(sections)} chapters</p></div>
  <div class="prism">{prism_svg()}</div>
</header>
<nav aria-label="Chapters"><details open id="navd"><summary>Chapters<span class="tools"><input id="q" type="search" placeholder="Search headings..." aria-label="Search the Codex headings"><button id="theme" type="button">Theme</button></span></summary>{''.join(navgroups)}</details><div id="hits" role="listbox"></div></nav>
<main>{''.join(sections)}</main>
<a class="top" href="#" aria-label="Back to top">↑</a>
<script>
(function(){{
  var root=document.documentElement, btn=document.getElementById('theme');
  var saved=null; try{{saved=localStorage.getItem('codex-theme');}}catch(e){{}}
  if(saved) root.setAttribute('data-theme',saved);
  btn.addEventListener('click',function(e){{e.preventDefault();
    var cur=root.getAttribute('data-theme')||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');
    var nxt=cur==='dark'?'light':'dark'; root.setAttribute('data-theme',nxt);
    try{{localStorage.setItem('codex-theme',nxt);}}catch(e){{}} }});
  var q=document.getElementById('q'), hits=document.getElementById('hits');
  q.addEventListener('click',function(e){{e.stopPropagation();}}); q.addEventListener('keydown',function(e){{e.stopPropagation();}});
  var heads=[].slice.call(document.querySelectorAll('.chapter h1[id],.chapter h2[id],.chapter h3[id]')).map(function(h){{
    return {{id:h.id,t:h.textContent,c:h.closest('.chapter').getAttribute('data-label')}};}});
  q.addEventListener('input',function(){{
    var v=q.value.trim().toLowerCase(); hits.innerHTML='';
    if(v.length<2){{hits.style.display='none';return;}}
    var n=0; heads.forEach(function(h){{ if(n<40 && h.t.toLowerCase().indexOf(v)>=0){{
      var a=document.createElement('a'); a.href='#'+h.id; a.textContent=h.t;
      var s=document.createElement('small'); s.textContent=h.c; a.appendChild(s); hits.appendChild(a); n++; }} }});
    hits.style.display=n?'block':'none'; }});
  hits.addEventListener('click',function(){{hits.style.display='none';}});
  if(matchMedia('(max-width:760px)').matches) document.getElementById('navd').removeAttribute('open');
}})();
</script>
</body></html>'''
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(page, encoding="utf-8")
    print(f"wrote {OUT} ({OUT.stat().st_size//1024} KB, {words} words, {len(sections)} chapters)")

if __name__ == "__main__":
    main()
