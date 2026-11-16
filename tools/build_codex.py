#!/usr/bin/env python3
"""Render the story bible (story/*.md + design/CAMEOS.md) into one readable HTML page: dist_web/codex.html."""
import html, pathlib, re, markdown

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "dist_web" / "codex.html"

# (file, anchor, short label)
CHAPTERS = [
    ("story/00_OVERVIEW.md", "overview", "Overview"),
    ("story/01_WORLD_LORE.md", "world", "World & lore"),
    ("story/02_FACTIONS.md", "factions", "Factions"),
    ("story/03_CAST.md", "cast", "Cast"),
    ("story/04_ACT_I.md", "act-1", "Act I"),
    ("story/20_SCRIPT_CH0-2.md", "script-1", "Script: first hour"),
    ("story/05_ACT_II.md", "act-2", "Act II"),
    ("story/06_ACT_III.md", "act-3", "Act III"),
    ("story/07_ACT_IV.md", "act-4", "Act IV"),
    ("story/08_ACT_V.md", "act-5", "Act V"),
    ("story/09_MYSTERIES_FORESHADOWING.md", "mysteries", "Mysteries"),
    ("story/14_WAR_AND_BLESSING.md", "war", "War & the Blessing"),
    ("story/10_CHOICES_ENDINGS.md", "choices", "Choices & endings"),
    ("story/12_RUIN_ROUTE.md", "ruin", "Ruin Route"),
    ("story/13_CUTSCENES.md", "cutscenes", "Cutscenes"),
    ("story/15_COMEDY.md", "comedy", "Comedy"),
    ("story/11_FINALE_LINES.md", "finale", "Finale lines"),
    ("design/CAMEOS.md", "cameos", "Sidequest cameos"),
]

# Gym order (SPINE): type, city
GYMS = [("Bug","Briarwick"),("Normal","Saltmere"),("Water","Ebbmouth"),("Electric","Lumen City"),
        ("Ground","Duneholt"),("Poison","Mirefen"),("Fire","Cindervault"),("Fighting","Ironreach"),
        ("Grass","Verdance"),("Ice","Rimeholt"),("Flying","Skyreach"),("Psychic","Lucent"),
        ("Rock","Cragholm"),("Ghost","Gravenmoor"),("Steel","Cogsworth"),("Dark","Underveil"),
        ("Fairy","Gloaming"),("Dragon","Wyrmrest")]
TYPE_COL = {"Bug":"#91a119","Normal":"#9fa19f","Water":"#2980ef","Electric":"#fac000","Ground":"#915121",
            "Poison":"#9141cb","Fire":"#e62829","Fighting":"#ff8000","Grass":"#3fa129","Ice":"#3dcef3",
            "Flying":"#81b9ef","Psychic":"#ef4179","Rock":"#afa981","Ghost":"#704170","Steel":"#60a1b8",
            "Dark":"#624d4e","Fairy":"#ef70ef","Dragon":"#5060e1"}

def render(md_text, prefix):
    md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists", "toc"],
                           extension_configs={"toc": {"slugify": lambda v, s: prefix + "-" + re.sub(r"[^a-z0-9]+", "-", v.lower()).strip("-")}})
    body = md.convert(md_text)
    # wide tables scroll on phones
    body = body.replace("<table>", '<div class="scroll"><table>').replace("</table>", "</table></div>")
    return body

def prism_svg():
    rays = []
    n = len(GYMS)
    for i, (t, city) in enumerate(GYMS):
        y = 40 + i * (520 / (n - 1))
        rays.append(f'<path d="M300 300 L1000 {y:.1f}" stroke="{TYPE_COL[t]}" stroke-width="9" stroke-linecap="round" opacity=".9"/>'
                    f'<text x="1010" y="{y + 5:.1f}" class="ray">{i + 1}. {html.escape(city)}</text>')
    return f'''<svg viewBox="0 0 1200 600" role="img" aria-label="A prism splitting light into the eighteen gym types">
  <defs><linearGradient id="beam" x1="0" x2="1"><stop offset="0" stop-color="currentColor" stop-opacity="0"/><stop offset="1" stop-color="currentColor" stop-opacity=".9"/></linearGradient>
  <linearGradient id="glass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="#9fb6c8" stop-opacity=".18"/></linearGradient></defs>
  <path d="M0 300 L300 300" stroke="url(#beam)" stroke-width="12" stroke-linecap="round"/>
  {''.join(rays)}
  <polygon points="300,120 430,420 170,420" fill="url(#glass)" stroke="currentColor" stroke-opacity=".5" stroke-width="3"/>
  <polygon points="300,120 330,420 170,420" fill="#fff" opacity=".12"/>
</svg>'''

def main():
    sections, toc = [], []
    for path, anchor, label in CHAPTERS:
        p = ROOT / path
        if not p.exists():
            continue
        toc.append(f'<a href="#{anchor}">{html.escape(label)}</a>')
        sections.append(f'<section class="chapter" id="{anchor}">{render(p.read_text(encoding="utf-8"), anchor)}</section>')
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
.ray{{font:600 17px Inter,system-ui,sans-serif;fill:var(--muted)}}
nav{{position:sticky;top:0;z-index:5;background:var(--bg);border-bottom:1px solid var(--rule);padding:10px max(5vw,16px);display:flex;flex-wrap:wrap;gap:6px 18px;font:600 14px/1.3 Inter,system-ui,sans-serif}}
nav a{{color:var(--muted);text-decoration:none;padding:8px 0;min-height:44px;display:inline-flex;align-items:center}}
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
<nav aria-label="Chapters">{''.join(toc)}</nav>
<main>{''.join(sections)}</main>
<a class="top" href="#" aria-label="Back to top">↑</a>
</body></html>'''
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(page, encoding="utf-8")
    print(f"wrote {OUT} ({OUT.stat().st_size//1024} KB, {words} words, {len(sections)} chapters)")

if __name__ == "__main__":
    main()
