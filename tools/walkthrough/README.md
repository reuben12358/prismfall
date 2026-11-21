# Walkthrough generator (from the walkthrough writer, 2026-11-21)

The parsers (parse_*.py, scan_maps*.py, names.py) dump game data to JSON, and gen.py fills the {{...}} placeholders in template.md to produce design/WALKTHROUGH.md.
The scripts were written to work in /tmp/wt, so before re-running them, point their paths at a scratch folder (they read the repo and write dumps there).
