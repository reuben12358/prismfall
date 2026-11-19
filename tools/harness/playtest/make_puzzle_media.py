#!/usr/bin/env python3
"""Puzzle engine proof media: python3 -I make_puzzle_media.py gym1|gym2 [--step 7] [--ms 220]
Reads $RUN/puzzle_out/<session>/ (bot.log, shots/, frames/) and writes docs/playtest/puzzles/<session>_NN_*.png
(real engine frames, caption strip added below) and <session>_solve.gif (slow, battles cut, a card between rooms)."""
import os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
RUN = os.environ.get('RUN', '/home/claude/run')
DOCS = os.path.join(HERE, '..', '..', '..', 'docs', 'playtest', 'puzzles')
CAP = {
    'g1_00': "Gym 1: outside the Loomhouse (Briarwick's elder tree)", 'g1_01': 'Foyer: the plank starts on the left balcony',
    'g1_02': 'Foyer: one pull of the training heddle, the plank slides to the middle', 'g1_03': 'Foyer: two pulls, the plank is under the stairs',
    'g1_04': 'Foyer: across the loom bed', 'g1_05': 'Weaving Hall: start (the middle bed has no plank at all)',
    'g1_06': 'Weaving Hall: Red heddle lifts beds A and B', 'g1_07': 'Weaving Hall: Gold lifts B and C',
    'g1_08': 'Weaving Hall: Green lifts C and A: every bed lifted twice, all planks on the right', 'g1_09': 'Weaving Hall: climbing the right-hand column',
    'g1_10': 'Weaving Hall: top ledge', 'g1_11': 'Canopy Lofts: first deck', 'g1_12': 'Canopy Lofts: alpha cord, then the spool throws you west',
    'g1_13': 'Canopy Lofts: the brass Meridian wire swings a bridge out', 'g1_14': 'Canopy Lofts: three more rides to the north deck',
    'g1_15': 'Canopy Lofts: on the bridge only the brass wire opens', 'g1_16': 'The Spindle: Warden Tamsin',
    'g2_00': 'Gym 2: outside Pell Playhouse (Saltmere Old Town)', 'g2_01': 'Foyer: the curtain is in',
    'g2_02': 'Foyer: Cue: Overture, called from the mark', 'g2_03': 'Revolving Stage: work lights',
    'g2_04': 'Stage: Cue: the Shipwreck (a gangplank crosses the pit)', 'g2_05': 'Stage: over the gangplank to stage left',
    'g2_06': 'Stage: Cue: the Forest (the ship drops go, the ladder is free)', 'g2_07': 'Fly Loft: up the left ladder',
    'g2_08': 'Fly Loft, RIGHT rail: rope 2 flies flats B and C', 'g2_09': 'Fly Loft: rope 3 flies A and drops the rostrum back in',
    'g2_10': 'Stage: down the right ladder', 'g2_11': 'Stage: Cue: the Throne', 'g2_12': 'Stage: through the gap where flat B stood',
    'g2_13': 'Stage: on the rostrum, flat A gone, the dais ahead', 'g2_14': 'The Grand Stage: Warden Dorian'}
ROOM = {130: 'Foyer', 131: 'Weaving Hall', 132: 'Canopy Lofts', 133: 'The Spindle', 120: 'Briarwick', 147: 'Saltmere Old Town',
        150: 'Foyer', 151: 'Revolving Stage', 152: 'Fly Loft', 154: 'The Grand Stage'}


def main():
    ses = sys.argv[1]; step = 7; ms = 220
    if '--step' in sys.argv: step = int(sys.argv[sys.argv.index('--step') + 1])
    if '--ms' in sys.argv: ms = int(sys.argv[sys.argv.index('--ms') + 1])
    run = os.path.join(RUN, 'puzzle_out', ses)
    log = open(os.path.join(run, 'bot.log'), encoding='utf-8', errors='replace').read().split('\n')
    nfr = len(os.listdir(os.path.join(run, 'frames')))
    rec = int(os.environ.get('REC_EVERY', 4)); f0 = None; segs = []; cur = None; battle = None
    for l in log:
        m = re.match(r'\[\s*(\d+)\] (.*)', l)
        if not m: continue
        f, t = int(m.group(1)), m.group(2)
        if t.startswith('puzzle session'): f0 = f
        if f0 is None: continue
        idx = lambda fr: max(0, min(nfr - 1, (fr - f0) // rec))
        mm = re.match(r'on map (\d+)', t)
        if mm:
            if cur: segs.append((cur[0], cur[1], idx(f) - 2))
            cur = (int(mm.group(1)), idx(f) + 10)
        if t.startswith('battle prepared') and cur:
            segs.append((cur[0], cur[1], idx(f) - 14)); battle = cur[0]; cur = None
        if battle is not None and t.startswith('step ') and cur is None:
            cur = (battle, idx(f) - 30); battle = None
        if t.startswith('plan done') and cur:
            segs.append((cur[0], cur[1], idx(f)))
    segs = [s for s in segs if s[2] - s[1] > 10]
    shots = []
    for fn in sorted(os.listdir(os.path.join(run, 'shots'))):
        m = re.match(r'\d+_(g\d_\d\d)_', fn)
        if m: shots.append('%s:%s' % (fn, CAP[m.group(1)]))
    os.makedirs(DOCS, exist_ok=True)
    for old in os.listdir(DOCS):
        if old.startswith(ses + '_'): os.remove(os.path.join(DOCS, old))
    tmp = os.path.join(run, 'media'); os.makedirs(tmp, exist_ok=True)
    for old in os.listdir(tmp): os.remove(os.path.join(tmp, old))
    labels = '|'.join('%s: %s' % ('Gym 1' if ses == 'gym1' else 'Gym 2', ROOM.get(m, str(m))) for m, _, _ in segs)
    cmd = ['python3', '-I', os.path.join(HERE, 'make_playtest_media.py'), run, tmp, '--step', str(step), '--ms', str(ms), '--name', 'solve',
           '--gif', ','.join('%d-%d' % (a, b) for _, a, b in segs), '--labels', labels]
    for s in shots: cmd += ['--shot', s]
    subprocess.check_call(cmd)
    for fn in sorted(os.listdir(tmp)):
        os.replace(os.path.join(tmp, fn), os.path.join(DOCS, ses + '_' + fn))
    print('segments:', segs)


if __name__ == '__main__':
    main()
