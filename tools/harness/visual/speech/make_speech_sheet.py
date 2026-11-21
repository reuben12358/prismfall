#!/usr/bin/env python3
"""GIF + captioned key-frame sheet from the trainer speech capture (004_SpeechCapture.rb).
  python3 -I make_speech_sheet.py <speech_dir> <out_dir>
Writes <out_dir>/celestine_zmove_speech.gif (her Z turn, every 3rd engine frame, real time, captioned) and
<out_dir>/zmove_speech_keys.png (Celestine's line as it ships; EBDX's slide-in path with a stand-in trainer)."""
import csv, os, sys
from PIL import Image, ImageDraw

src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
rows = {r["case"]: r for r in csv.DictReader(open(os.path.join(src, "speech.tsv")), delimiter="\t")}


def frames(case):
    d = os.path.join(src, "sp_" + case)
    return [os.path.join(d, f) for f in sorted(os.listdir(d)) if f.endswith((".bmp", ".png"))]


# GIF: Celestine's turn, from the Z-move choice to ~3 s after her line
fs = frames("celestine")
shot = int(rows["celestine"]["shot"])
fs = fs[:min(len(fs), shot + 60)]
cap = 16
q = []
for k, p in enumerate(fs):
    fr = Image.open(p).convert("RGB")
    c = Image.new("RGB", (fr.width, fr.height + cap), (14, 14, 18))
    c.paste(fr, (0, 0))
    d = ImageDraw.Draw(c)
    d.text((4, fr.height + 2), "Gym 17 Celestine: her Mimikyu's Z-move - real engine, Prismfall Z-Power speech hook",
           fill=(220, 220, 220))
    d.text((fr.width - 40, fr.height + 2), "%4.1fs" % (k * 3 / 60.0), fill=(255, 220, 120))
    q.append(c.quantize(160, dither=Image.NONE))
q[0].save(os.path.join(out, "celestine_zmove_speech.gif"), save_all=True, append_images=q[1:], duration=50, loop=0,
          optimize=False)

# key frames: two rows of four, each captioned
ROWS = [("celestine", [(-30, "the Z-move is unleashed"), (-4, "her line (no front sprite yet: named message)"),
                       (6, "Let's Snuggle Forever"), (40, "the hit")],
         "Celestine (Gym 17, the real data): she has no trainer sprite yet, so the line is a named battle message."),
        ("ebdx_demo", [(-26, "EBDX slides the speaker in"), (-10, "the line in EBDX's trainer dialogue"),
                       (8, "the move goes on"), (34, "the hit")],
         "EBDX path (capture-only stand-in: a stock Beauty with a demo line): trainers with a front sprite slide in "
         "and speak, like EBDX's battle scripts.")]
head, lab, sub = 34, 14, 14
W, H = 512, 384
sheet = Image.new("RGB", (4 * W, head + 2 * (sub + lab + H)), (14, 14, 18))
d = ImageDraw.Draw(sheet)
d.text((6, 4), "Trainer speech when a trainer's Z-move fires - real engine (mkxp-z + Essentials v21.1 + EBDX + Prismfall "
               "plugins). Data: PrismfallSpeech::LINES (plugins/Prismfall Z-Power/005_ZPower_TrainerSpeech.rb).",
       fill=(235, 235, 235))
d.text((6, 19), "Fires on :prismfall_zmove_unleashed (after '...unleashed its full-force Z-Move!', before the move hits) "
                "and :prismfall_mega_evolved; once per battle per trainer.", fill=(200, 200, 200))
y = head
for case, picks, title in ROWS:
    fs = frames(case)
    shot = int(rows[case]["shot"])
    d.text((6, y), title, fill=(255, 220, 120))
    for k, (off, label) in enumerate(picks):
        i = max(0, min(len(fs) - 1, shot + off))
        d.text((k * W + 4, y + sub), "%d. %s" % (k + 1, label), fill=(255, 255, 255))
        sheet.paste(Image.open(fs[i]).convert("RGB"), (k * W, y + sub + lab))
    y += sub + lab + H
sheet.save(os.path.join(out, "zmove_speech_keys.png"), optimize=True)
print("wrote", out, len(q), "GIF frames")
