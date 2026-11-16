#!/usr/bin/env python3
"""Copy the staged stand-in tracks into an Essentials project under their final names.
Usage: python3 install_audio.py <path-to-game-project> [--force]
Reads manifest.tsv next to this script. Stock-file rows are skipped. Never overwrites
an existing file unless --force (so a real remix you dropped in is kept)."""
import csv, os, shutil, sys
here = os.path.dirname(os.path.abspath(__file__))
if len(sys.argv) < 2:
    sys.exit(__doc__)
proj, force = sys.argv[1], '--force' in sys.argv
done = skipped = 0
with open(os.path.join(here, 'manifest.tsv'), newline='', encoding='utf-8') as f:
    for row in csv.DictReader(f, delimiter='\t'):
        src = row['local_source']
        if src.startswith('('):
            continue
        ext = os.path.splitext(src)[1]
        dest_dir = os.path.join(proj, 'Audio', row['folder'])
        os.makedirs(dest_dir, exist_ok=True)
        # any extension counts as "already there": Essentials looks names up without one
        existing = [n for n in os.listdir(dest_dir) if os.path.splitext(n)[0] == row['final_name']]
        if existing and not force:
            skipped += 1
            continue
        for n in existing:
            os.remove(os.path.join(dest_dir, n))
        shutil.copyfile(os.path.join(here, src), os.path.join(dest_dir, row['final_name'] + ext))
        done += 1
print(f'installed {done}, kept {skipped} existing')
