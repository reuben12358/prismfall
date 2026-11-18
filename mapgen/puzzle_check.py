#!/usr/bin/env python3
"""python3 -I puzzle_check.py : run every puzzle proof in mapgen/puzzles/ (solvable, no soft-lock, intended minimum)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import puzzles

if __name__ == '__main__':
    bad, _ = puzzles.run_all()
    print('%d puzzle proof(s) FAILED' % bad if bad else 'all puzzle proofs passed')
    sys.exit(1 if bad else 0)
