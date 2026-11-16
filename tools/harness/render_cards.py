#!/usr/bin/env python3
"""Renders "battle log cards" (PNG) from the headless harness logs.

These are typeset excerpts of TEXT logs produced by tools/harness/run_all.rb.
They are logic-test output, NOT game screenshots: every card says so.

    python3 -I tools/harness/render_cards.py [captures_dir]
"""
import os
import re
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.normpath(os.path.join(HERE, "..", "..", "docs", "battle_captures"))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    except OSError:
        return ImageFont.load_default()


MONO = font("DejaVuSansMono.ttf", 17)
MONO_B = font("DejaVuSansMono-Bold.ttf", 17)
SANS_B = font("DejaVuSans-Bold.ttf", 26)
SANS = font("DejaVuSans.ttf", 16)
TAG = font("DejaVuSans-Bold.ttf", 14)

BG, PANEL, INK, DIM = (17, 20, 28), (27, 32, 44), (226, 230, 238), (128, 138, 156)
ACCENT, FIELD, WARN, GOOD = (255, 196, 84), (126, 214, 255), (255, 120, 120), (140, 226, 150)


def section(path, title_part=None):
    """Lines of one battle inside a log file (the whole file if title_part is None)."""
    with open(os.path.join(OUT, path), encoding="utf-8") as f:
        lines = f.read().split("\n")
    if title_part is None:
        return lines
    start = next(i for i, l in enumerate(lines) if title_part in l and i + 1 < len(lines) and set(lines[i + 1]) == {"="})
    end = next((i for i in range(start + 2, len(lines) - 1) if lines[i + 1] and set(lines[i + 1]) == {"="}), len(lines))
    return lines[start:end]


def excerpt(lines, start_re, end_re=None, max_lines=22, skip=("(anim:",)):
    out, on = [], False
    for l in lines:
        if not on and re.search(start_re, l):
            on = True
        if on:
            if end_re and out and re.search(end_re, l):
                break
            if l.strip() and not any(s in l for s in skip):
                out.append(l.rstrip())
            if len(out) >= max_lines:
                break
    return out


def colour_for(line, highlights):
    s = line.strip()
    if s.startswith("##"):
        return ACCENT, MONO_B
    if any(h in line for h in highlights):
        return FIELD, MONO_B
    if s.startswith("HP ") or s.startswith("[") or s.startswith(">>") or s.startswith("<<") or s.startswith("xx"):
        return DIM, MONO
    if s.startswith("---"):
        return GOOD, MONO_B
    return INK, MONO


def card(filename, title, subtitle, blocks, highlights, note=None):
    """blocks: list of (caption or None, [lines])."""
    width, pad, lh = 1180, 34, 25
    n_lines = sum(len(b[1]) + (2 if b[0] else 0) for b in blocks) + (len(blocks) - 1)
    height = 190 + n_lines * lh + (58 if note else 0) + 94
    img = Image.new("RGB", (width, height), BG)
    d = ImageDraw.Draw(img)
    # Banner: what this image is.
    d.rectangle([0, 0, width, 40], fill=(74, 52, 12))
    d.text((pad, 11), "LOGIC-TEST OUTPUT  -  headless battle harness log excerpt  -  NOT A GAME SCREENSHOT",
           font=TAG, fill=ACCENT)
    d.text((pad, 58), title, font=SANS_B, fill=INK)
    d.text((pad, 96), subtitle, font=SANS, fill=DIM)
    y = 136
    d.rounded_rectangle([pad - 14, y - 12, width - pad + 14, y + n_lines * lh + 14], radius=10, fill=PANEL)
    for caption, lines in blocks:
        if caption:
            d.text((pad, y), caption, font=TAG, fill=GOOD)
            y += lh * 2 - 8
            y += 8
        for line in lines:
            colour, fnt = colour_for(line, highlights)
            d.text((pad, y), line[:108], font=fnt, fill=colour)
            y += lh
        y += lh
    y -= lh - 22
    if note:
        d.text((pad, y + 6), note, font=SANS, fill=GOOD)
        y += 58
    d.text((pad, height - 68), "Lines starting with ## are harness event markers; indented HP/[..] lines are harness state "
           "readouts; everything else is battle message text.", font=SANS, fill=DIM)
    d.text((pad, height - 44), "Real Pokemon Essentials v21.1 battle code + Prismfall Core / Field Effects / Bosses plugins, "
           "run in plain Ruby. No EBDX visuals were rendered.", font=SANS, fill=DIM)
    path = os.path.join(OUT, filename)
    img.save(path)
    print("wrote", path, img.size)


def main():
    silk = section("logs/01_silkwood.txt")
    card("card_1_field_intro.png", "Field intro - Silkwood (Gym 1, Warden Tamsin)",
         "Source: docs/battle_captures/logs/01_silkwood.txt  (battle started with Prismfall.gym_battle(1))",
         [(None, excerpt(silk, r"--- Battle start ---", r"--- Turn 2 ---", 24))],
         ["Giant webs glisten", "sticky web", "Telluric Seed", "Silkwood", "silk", "web strands", "nectar"])

    on = section("probes/volcanic.txt", "boosted move FLAMETHROWER (on field)")
    off = section("probes/volcanic.txt", "boosted move FLAMETHROWER (baseline")
    hp = lambda ls: next(int(a) - int(b) for a, b in re.findall(r"HP Snorlax \(foe\): (\d+) -> (\d+)", "\n".join(ls))[:1])
    card("card_2_boosted_move.png", "Field-boosted move - Flamethrower on the Volcanic Field",
         "Source: docs/battle_captures/probes/volcanic.txt  (same user, target and damage roll in both runs)",
         [("ON THE VOLCANIC FIELD", excerpt(on, r"used Flamethrower", r"used Splash", 6)),
          ("BASELINE - NO FIELD", excerpt(off, r"used Flamethrower", r"used Splash", 6))],
         ["The magma roared!"],
         note="Damage %d on the field vs %d without it  ->  x%.2f (field definition: Fire-type moves x1.5)"
              % (hp(on), hp(off), hp(on) / hp(off)))

    tr = section("probes/volcanic.txt", "transition [stage 1: moves SURF")
    card("card_3_field_transition.png", "Field transition - Volcanic Field -> Ashen Waste (Surf used twice)",
         "Source: docs/battle_captures/probes/volcanic.txt  (scripted probe: player uses Surf, foe uses Splash)",
         [(None, excerpt(tr, r"--- Turn 1 ---", r"--- Turn 3 ---", 26))],
         ["Steam hisses", "quenched the magma", "scorched by the magma"])

    boss = section("logs/boss_zekrom.txt")
    card("card_4_boss_bar_break.png", "Boss bar break - Zekrom (3 HP bars), Factory -> Scrapyard on the 2nd break",
         "Source: docs/battle_captures/logs/boss_zekrom.txt  (Prismfall::Bosses.wild_battle(:ZEKROM_ENGINE), over-levelled party)",
         [(None, excerpt(boss, r"--- Turn 1 ---", r"Garchomp fainted", 30))],
         ["containment cable", "Engine's grip", "Engine core buckles", "learned Bolt Strike"])


if __name__ == "__main__":
    main()
