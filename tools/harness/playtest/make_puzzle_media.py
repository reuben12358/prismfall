#!/usr/bin/env python3
"""Puzzle engine proof media: python3 -I make_puzzle_media.py gym1|gym2|lofts|d1 [--step 7] [--ms 220]
Reads $RUN/puzzle_out/<session>/ (bot.log, shots/, frames/) and writes docs/playtest/puzzles/<session>_NN_*.png
(real engine frames, caption strip added below) and <session>_solve.gif (slow, battles cut, a card between rooms)."""
import os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
RUN = os.environ.get('RUN', '/home/claude/run')
DOCS = os.path.join(HERE, '..', '..', '..', 'docs', 'playtest', 'puzzles')
CAP = {
    'g1_00': 'Gym 1: outside the Pell Playhouse (map 147)', 'g1_01': 'Gym 1 lobby (map 150)',
    'g1_02': 'Gym 1 auditorium (map 154): the aisle runs between the seat rows to the stage',
    'g1_03': 'Up the aisle: the actors in the aisle battle you', 'g1_04': 'On the apron: the house curtain is in',
    'g1_05': 'The one interaction: haul the curtain rope; the curtain flies out', 'g1_06': 'Before Warden Dorian', 'g1_07': 'After the battle: the badge',
    'g2_00': 'Gym 2: outside the Loomhouse, the elder tree (map 120)', 'g2_01': "Gym 2 lobby (map 130): Granny Loom's weavers",
    'g2_02': 'The Canopy (map 131): the hollow of the elder, webs across the drop', 'g2_03': 'A taut web: step on it',
    'g2_04': 'It throws you three bounds the way you stepped on', 'g2_05': 'A web can throw you onto a web',
    'g2_06': 'A sticky web holds you in mid-air', 'g2_07': 'Step sideways off it onto a taut web: thrown sideways',
    'g2_08': 'Ledge three: the Joltik strands', 'g2_09': 'Joltik 1 sparks the gold strand: webs A and B change',
    'g2_10': 'Joltik 2 on the perch sparks the blue strand: B and C', 'g2_11': 'A throws you up onto B, which holds you',
    'g2_12': "C throws you across to Tamsin's ledge", 'g2_13': 'After the double battle: the badge',
    'bs_00': 'Playhouse Backstage (D9, map 151): work lights', 'bs_01': 'Cue the Shipwreck from the mark: a gangplank crosses the pit',
    'bs_02': 'Over the gangplank to stage left', 'bs_03': 'Cue the Forest: the ship drops go, the ladder is free',
    'bs_04': 'Fly Loft (map 152)', 'bs_05': 'RIGHT rail: rope 2 flies flats B and C', 'bs_06': 'Rope 3 flies A and drops the rostrum back in',
    'bs_07': 'Down the right ladder: cue the Throne', 'bs_08': 'Through the gap where flat B stood', 'bs_09': 'On the rostrum, flat A gone, the dais ahead',
    'bs_10': 'The upstage door: the old script, and back to the auditorium',
    'lf_00': 'Upper Lofts (optional, after Badge 2): the stairs behind the Warden', 'lf_01': 'Weaving Hall: start (the middle bed has no plank at all)',
    'lf_02': 'Weaving Hall: Red heddle lifts beds A and B', 'lf_03': 'Weaving Hall: Gold lifts B and C',
    'lf_04': 'Weaving Hall: Green lifts C and A: every bed lifted twice, all planks on the right', 'lf_05': 'Weaving Hall: climbing the right-hand column',
    'lf_06': 'Canopy Lofts: first deck', 'lf_07': 'Canopy Lofts: alpha cord, then the spool throws you west',
    'lf_08': 'Canopy Lofts: the brass Meridian wire swings a bridge out', 'lf_09': 'Canopy Lofts: three more rides to the north deck',
    'lf_10': 'Canopy Lofts: on the bridge only the brass wire opens', 'lf_11': "Granny's Knot: five threads, five treadles",
    'lf_12': "Granny's Knot: treadles 1, 4, 5: up, down, up, down, up", 'lf_13': "Granny's chest opens",
    'd1_00': 'D1 Glassed Orchard: the chime spur plays low, middle, high', 'd1_01': 'A wrong note first: the failure line says which note was wanted',
    'hs_00': 'Gym 1 auditorium: the house tonight', 'hs_01': 'The stalls: everyone you met in Saltmere has a seat by the aisle',
    'hs_02': "After Dorian's show",
    'd2_00': 'D2 the Deepwood (map 525): the lantern hollow, walled with silk', 'd2_01': 'Post alpha: the Joltik lights cocoons 1 and 2',
    'd2_02': 'Curtain 1 now leans in: through it', 'd2_03': 'Post beta, inside: cocoons 2 and 3 (2 goes dark again)',
    'd2_04': 'Curtain 3 leans north now: onto the island', 'd2_05': 'TM19 Giga Drain',
    'd7_00': 'D7 the Rimewood (map 562): the Frost Loom', 'd7_01': 'The left thread cracks curtains 1 and 2',
    'd7_02': 'The right thread cracks curtain 3', 'd7_03': 'Up the east path, all three broken', 'd7_04': "The trapper's cache",
    'd1_02': 'Low', 'd1_03': 'Middle', 'd1_04': 'High: the glass hedge shatters', 'd1_05': 'Past where the hedge stood', 'd1_06': "The lost child's satchel"}
ROOM = {525: 'The Deepwood', 562: 'The Rimewood', 130: 'Loomhouse lobby', 131: 'The Canopy', 154: 'Auditorium', 150: 'Lobby', 151: 'Old revolve', 152: 'Fly Loft', 132: 'Canopy Lofts', 134: "Granny's Knot", 120: 'outside (map 120)', 147: 'outside (map 147)', 522: 'The Glassed Orchard',
        }


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
        m = re.match(r'\d+_([a-z][a-z0-9]_\d\d)_', fn)
        if m: shots.append('%s:%s' % (fn, CAP[m.group(1)]))
    os.makedirs(DOCS, exist_ok=True)
    for old in os.listdir(DOCS):
        if old.startswith(ses + '_'): os.remove(os.path.join(DOCS, old))
    tmp = os.path.join(run, 'media'); os.makedirs(tmp, exist_ok=True)
    for old in os.listdir(tmp): os.remove(os.path.join(tmp, old))
    labels = '|'.join('%s: %s' % ({'gym1': 'Gym 1', 'gym2': 'Gym 2', 'lofts': 'Upper Lofts', 'backstage': 'Backstage', 'd1': 'Dungeon 1'}.get(ses, ses), ROOM.get(m, str(m))) for m, _, _ in segs)
    cmd = ['python3', '-I', os.path.join(HERE, 'make_playtest_media.py'), run, tmp, '--step', str(step), '--ms', str(ms), '--name', 'solve',
           '--gif', ','.join('%d-%d' % (a, b) for _, a, b in segs), '--labels', labels]
    for s in shots: cmd += ['--shot', s]
    subprocess.check_call(cmd)
    for fn in sorted(os.listdir(tmp)):
        os.replace(os.path.join(tmp, fn), os.path.join(DOCS, ses + '_' + fn))
    print('segments:', segs)


if __name__ == '__main__':
    main()
