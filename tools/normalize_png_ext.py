#!/usr/bin/env python3
"""Rename upper-case .PNG files to .png under an engine's Graphics folders (Gemini sprite audit 2026-11-23, bug 2).

Case-sensitive file systems (Linux, mkxp-z) can't find ZORUA_1.PNG when Essentials asks for ZORUA_1.png. The EBDX
Bridge (011_Bridge_SpriteFixes.rb) retries .PNG at run time; this makes the fix permanent in a game folder.

    python3 -I tools/normalize_png_ext.py --engine /path/to/game            # dry run: list what would change
    python3 -I tools/normalize_png_ext.py --engine /path/to/game --apply    # rename

Only Graphics/Pokemon and Graphics/EBDX are scanned. A file whose .png twin already exists is reported, not touched.
"""
import argparse
import os
import sys


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--engine", required=True, help="game folder holding Graphics/")
    ap.add_argument("--apply", action="store_true", help="rename (default: dry run)")
    args = ap.parse_args()
    roots = [os.path.join(args.engine, "Graphics", d) for d in ("Pokemon", "EBDX")]
    todo, clash = [], []
    for root in roots:
        if not os.path.isdir(root):
            continue
        for dirpath, _dirs, files in os.walk(root):
            for f in files:
                stem, ext = os.path.splitext(f)
                if ext == ".png" or ext.lower() != ".png":
                    continue
                src = os.path.join(dirpath, f)
                dst = os.path.join(dirpath, stem + ".png")
                (clash if os.path.exists(dst) else todo).append((src, dst))
    for src, dst in todo:
        print(("rename " if args.apply else "would rename ") + os.path.relpath(src, args.engine))
        if args.apply:
            os.rename(src, dst)
    for src, _dst in clash:
        print("skipped (a .png twin exists): " + os.path.relpath(src, args.engine))
    print("%d file(s) %s, %d skipped" % (len(todo), "renamed" if args.apply else "to rename", len(clash)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
