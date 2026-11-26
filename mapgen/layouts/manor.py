#!/usr/bin/env python3
"""layouts/manor.py - Thistledown Manor (546) and its attic (547), map builder 14, on tileset 59 "PF Rejuv Manor"
(the manor kit, mdraw.py).  Story: story/21_SCRIPT_CH3.md (maps 546/547); puzzle: DUNGEON_PUZZLES D5, whose grids
and proofs are mapgen/puzzles/manor.py (the rooms below are carved round those grids, so map and proof cannot drift).

546, ground floor:  the vestibule (checker marble, the front doors to the Lea), the stair hall (TEACH: one armchair
      between you and the grand staircase), the conservatory (Scene 3, the graveyard; the Cleanse Tag), the parlour
      (Dame Rosamund by the cold fireplace; Scene 2, the closet), the dining room (COMBINE: two armchairs in the
      back-stair nook under the attic hatch, two trapdoors to the wine cellar; locked until the portraits are set).
      Upstairs (the grand staircase): the landing (Scene 1, the battlements; the grandfather clock), the portrait
      gallery (TWIST: four crooked portraits, two armchairs, two alcoves) and the green room (the Channeler).
547, the attic: rafters, the oculus, the company's old costumes and flats, a little stage; Greavard under a sheet.

    python3 -I layouts/manor.py && python3 -I build.py 546 547"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cavekit import Cave, FLOOR, TER, MASS, P1
import cavekit as CK
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
from puzzles import manor as PZ
import trial_overlay as TO

TID = 59
FIELD = 'HOLLOW_CATHEDRAL'
TONE = [-26, -30, -2, 34]
SUFFIX = ['lipw', 'lipm', 'lipe', 'facew', 'facem', 'facee', 'basew', 'basem', 'basee', 'lipm1', 'facem1', 'basem1',
          'facem2', 'lipm2', 'Nw', 'Nm', 'Ne', 'W', 'E', 'inW0', 'inW1', 'inE0', 'inE1', 'shadow']


class Manor(Cave):
    """a Cave whose rooms each get their own wallpaper (reskin) and floor"""
    def __init__(self, W, H, seed):
        super().__init__(W, H, 'F', seed, pool='Cave Pool', tid=TID)
        self.kit = {'default': 'cvF', TER: 'cvB'}
        self.STAIRS = tuple(P1('mn_stair_' + k) for k in 'lmr')
        self.rooms = []                          # (x0, y0, x1, y1, wall palette, floor palette)

    def room_box(self, x0, y0, x1, y1, h, wall, floor):
        self.box(x0, y0, x1, y1, h)
        self.rooms.append((x0, y0, x1, y1, wall, floor))

    def pal_at(self, x, y):
        best = None
        for (x0, y0, x1, y1, w, f) in self.rooms:
            d = max(0, x0 - x, x - x1) + max(0, y0 - y, y - y1)
            k = (d, -y0)
            if best is None or k < best[0]: best = (k, w, f)
        return best[1], best[2]

    def reskin(self):
        rev = {}
        for s in SUFFIX:
            rev.setdefault(P1('F_' + s), s)
        L = self.L
        for y in range(self.H):
            for x in range(self.W):
                w, f = self.pal_at(x, y)
                for z in range(3):
                    t = int(L[z, y, x])
                    if t in rev and w != 'F':
                        L[z, y, x] = P1('%s_%s' % (w, rev[t]))
                if self.cls[y, x] == '.' and L[0, y, x] in self.floor_ids:
                    v = (x * 7 + y * 13 + (x // 3) * 5) % 9
                    L[0, y, x] = P1('%s_f%d' % (f, 0 if v < 4 else 1 if v < 7 else 2 if v < 8 else 3))

    def paint(self):
        self.floor_ids = {P1('F_f%d' % v) for v in range(4)}
        super().paint()
        self.reskin()
        rugs = {P1('mn_rug%s_%s' % (k, p)) for k in 'RBG' for p in ('nw', 'n', 'ne', 'w', 'c', 'e', 'sw', 's', 'se', 'c2')}
        for z, x, y, t in getattr(self, 'late', []):
            if z == 1 and self.L[1, y, x] in rugs and t not in rugs and not self.L[2, y, x]: z = 2     # furniture stands on the rug
            self.L[z, y, x] = t
        ts = self.ts(); VB = CK.K.RC.VBASE
        for y in range(self.H):                  # a shade / dust decal never sits over furniture (it would make it walkable)
            for x in range(self.W):
                t1, t2 = int(self.L[1, y, x]), int(self.L[2, y, x])
                if t1 and t1 < VB and t2 and t2 < VB and ts['passages'][t1] & 15 == 15 and ts['passages'][t2] & 15 == 0 and ts['priorities'][t2] == 0:
                    self.L[2, y, x] = 0
        return self.L

    # ---------------------------------------------------------------- dressing helpers
    def on(self, name, x, y, z=None):
        """a piece's tiles straight onto the layers (after paint); solid ones mark the cell taken"""
        L = CK.STAMPS[name]['layers']
        for dy in range(len(L[0])):
            for dx in range(len(L[0][0])):
                for zz in range(3):
                    t = L[zz][dy][dx]
                    if t: self.late.append((zz if z is None else z, x + dx, y + dy, t))

    def rug(self, k, x0, y0, x1, y1, medallion=True):
        cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                part = ('n' if y == y0 else 's' if y == y1 else '') + ('w' if x == x0 else 'e' if x == x1 else '')
                if not part: part = 'c2' if medallion and (x, y) == (cx, cy) else 'c'
                self.late.append((1, x, y, P1('mn_rug%s_%s' % (k, part))))

    def table(self, x0, y0, x1, y1):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                part = ('n' if y == y0 else 's' if y == y1 else '') + ('w' if x == x0 else 'e' if x == x1 else '') or 'c'
                self.late.append((1, x, y, P1('mn_dt_' + part)))

    def scatter(self, names, cells, every=5, seed=0):
        for i, (x, y) in enumerate(sorted(cells)):
            if (x * 31 + y * 17 + seed) % every == 0:
                self.late.append((2, x, y, P1(names[(x + y + seed) % len(names)])))


def trainer(at, ttype, name, d, intro, after, sight=3):
    return {'type': 'trainer', 'at': list(at), 'sight': sight, 'dir': d, 'sprite': 'trainer_' + ttype,
            'trainer': [ttype, name], 'intro': intro, 'after': after, 'rules': ['setBattleRule("field", :%s)' % FIELD]}


def trial(name, at, key=None, tile=None, condition=None, cmds=None, sprite=None):
    e = TO.ev(name, at, key, tile=tile, condition=condition, cmds=cmds, sprite=sprite)
    e.pop('near'); e['at'] = list(at)
    return e


def zone_free(m):
    """cells the puzzles own: no solid dressing, no other event may stand on them"""
    out = set()
    for k in PZ.ZONES:
        out |= PZ.Zone(k).floor
    return out


# ================================================================================================ 546
def build_546():
    m = Manor(56, 40, 546)
    R = m.room_box
    R(3, 7, 18, 13, TER, 'H', 'H')               # the portrait gallery (TWIST)
    m.box(19, 7, 21, 9, TER)                     # its door from the landing (the top two rows are the doorway's wall)
    R(22, 7, 35, 16, TER, 'F', 'H')              # the landing
    m.box(36, 10, 37, 12, TER)                   # the green room's door
    R(38, 7, 52, 14, TER, 'P', 'P')              # the green room: warm honey-oak dressing salon (contrasts landing!)
    R(24, 17, 33, 25, FLOOR, 'F', 'H')           # the stair hall (TEACH): rich dark walnut parquet (zero loud chessboard!)
    m.box(28, 26, 29, 27, FLOOR)                 # the arch to the vestibule
    R(21, 28, 36, 37, FLOOR, 'F', 'H')           # the vestibule: rich dark walnut parquet + mahogany inlays
    m.box(28, 38, 29, 39, FLOOR)                 # the front doors
    m.box(18, 32, 20, 34, FLOOR)                 # to the conservatory
    R(3, 28, 17, 37, FLOOR, 'G', 'N')            # the conservatory: dark mahogany boardwalk framing central tiled garden beds!
    m.box(10, 25, 11, 27, FLOOR)                 # conservatory -> parlour
    R(3, 17, 17, 24, FLOOR, 'P', 'P')            # the parlour
    m.box(37, 29, 39, 31, FLOOR)                 # vestibule -> dining (the locked door at 38)
    R(40, 25, 53, 31, FLOOR, 'N', 'N')           # the dining room (COMBINE)
    m.box(49, 22, 49, 24, FLOOR)                 # the back-stair nook (hatch stand 49,24)
    # Sculpted chamfered Gothic room corners & recessed mezzanine shoulders (100% outside all 3 D5 puzzle zone grids!)
    m.mass_at([(21, 37), (22, 37), (35, 37), (36, 37),          # vestibule south foyer chamfer
               (3, 37), (4, 37), (16, 37), (17, 37),            # conservatory glasshouse apse chamfer
               (17, 24),                                        # parlour east library corner recess (west corner kept square for grand piano!)
               (22, 16), (35, 16),                              # upper landing stair-head gallery shoulders (clear of flats & palm!)
               (38, 14), (52, 14)])                             # green room dressing wing chamfer
    m.stairs(27, 16, w=4, n=3, c='.')            # the grand staircase: landing -> stair hall
    m.plan_cliffs(rows=3)
    E = m.events
    late = m.late = []
    free = zone_free(m)

    # ------------------------------------------------------------ the puzzles' furniture (solid cells of the grids)
    for name, x, y in (('mn_case_l', 13, 11), ('mn_case_m', 14, 11), ('mn_case_r', 15, 11), ('mn_plinth', 13, 12), ('mn_plinth', 15, 12),
                       ('mn_case_l', 9, 12), ('mn_case_m', 10, 12), ('mn_case_r', 11, 12), ('mn_plinth', 9, 13), ('mn_plinth', 11, 13)):
        m.on(name, x, y)
    m.table(41, 27, 45, 28)                      # the dining table, flush in the north-west corner
    for x in range(41, 46): late.append((1, x, 29, P1('mn_dch_up')))
    late.append((1, 40, 28, P1('mn_dch_right'))); late.append((1, 40, 27, P1('mn_fern'))); late.append((1, 40, 29, P1('mn_fern')))
    # Dress all 5 dining table columns (41..45, 27..28) with candelabras & tableware to calm the stark white tablecloth
    for x, y in ((42, 27), (44, 27), (41, 28), (42, 28), (44, 28), (45, 28)): late.append((2, x, y, P1('mn_dt_plate')))
    for x, y in ((41, 27), (43, 27), (45, 27), (43, 28)): late.append((2, x, y, P1('mn_dt_cand')))
    for x, y in PZ.Zone('d').trap: late.append((1, x, y, P1('mn_trap')))

    # ------------------------------------------------------------ walls: windows, portraits, sconces, cobwebs
    for x in (6, 10, 14): m.on('mn_window', x, 6)                         # the gallery's north wall (lip + face)
    for x in (24, 33): m.on('mn_window', x, 6)
    for x in (41, 44, 50): m.on('mn_window_bare', x, 6)
    for x in (6, 9, 12, 15): m.on('mn_window', x, 27)                    # conservatory: tall windows in the glass
    for x in (5, 15): m.on('mn_window', x, 16)
    for x in (42, 46, 52): m.on('mn_window', x, 24)
    for x, y in ((3, 7), (7, 7), (11, 7), (15, 7), (18, 7), (26, 7), (31, 7), (23, 29), (34, 29),
                 (40, 25), (48, 25), (53, 25), (41, 7), (48, 7)):
        late.append((2, x, y, P1('mn_sconce')))
    for x, y, n in ((3, 6, 'mn_web_l'), (18, 6, 'mn_web_r'), (22, 6, 'mn_web_l'), (35, 6, 'mn_web_r'), (21, 27, 'mn_web_l'), (36, 27, 'mn_web_r'),
                    (3, 16, 'mn_web_l'), (17, 16, 'mn_web_r'), (40, 24, 'mn_web_l'), (53, 24, 'mn_web_r'), (38, 6, 'mn_web_l'), (52, 6, 'mn_web_r')):
        late.append((2, x, y, P1(n)))
    for x in (5, 8, 13, 16): late.append((2, x, 29, P1('mn_ivy%d' % (x % 2))))
    late.append((2, 7, 28, P1('mn_pane_broken'))); late.append((2, 14, 29, P1('mn_pane_broken')))
    m.on('mn_company', 28, 7)                                             # the company portrait over the landing
    late.append((2, 25, 29, P1('mn_portK'))); late.append((2, 32, 29, P1('mn_portX')))   # the vestibule's two
    late.append((2, 7, 17, P1('mn_portQ'))); late.append((2, 13, 17, P1('mn_portL')))
    late.append((2, 44, 25, P1('mn_portX'))); late.append((2, 50, 25, P1('mn_portF')))

    # ------------------------------------------------------------ rugs and floors (tailored per room, ZERO cloned red rugs!)
    m.rug('R', 24, 31, 33, 35)                    # Vestibule: the manor's ONE grand crimson-and-gold medallion carpet
    # Stair hall (TEACH): warm inlaid parquet aisle (painted on L0 below; no cloned red runner!)
    m.rug('B', 6, 20, 13, 22)                     # Parlour: deep royal-blue fireside salon carpet
    m.rug('B', 24, 10, 33, 13)                    # Upper Landing: grand royal-blue tapestry carpet
    m.rug('G', 4, 9, 17, 10, medallion=False)     # Portrait Gallery (TWIST): tailored emerald-velvet gallery runner
    m.rug('G', 40, 10, 50, 12)                    # Green Room: namesake emerald-velvet medallion carpet on warm honey-oak!

    # ------------------------------------------------------------ vestibule (outside the stair-hall zone)
    def put(name, x, y):
        L = CK.STAMPS[name]['layers']; h, w = len(L[0]), len(L[0][0])
        cells = [(x + dx, y + dy) for dx in range(w) for dy in range(h)]
        assert not any(c in free for c in cells), (name, x, y)
        m.on(name, x, y)
    put('mn_console', 22, 30); put('mn_palm', 21, 31); put('mn_coat', 35, 30); put('mn_umbrella', 36, 32)
    put('mn_statue', 21, 35); put('mn_statue', 36, 35); put('mn_palm', 24, 36); put('mn_palm', 33, 36)
    put('mn_console', 34, 34); put('mn_candelabra', 26, 29); put('mn_candelabra', 31, 29)
    put('mn_armour', 24, 29); put('mn_armour', 33, 29)
    put('mn_candelabra', 22, 35); put('mn_candelabra', 35, 35)
    put('mn_bust', 25, 36); put('mn_bust', 32, 36)
    late.append((1, 28, 37, P1('mn_mat')))
    # ------------------------------------------------------------ landing (TER)
    put('mn_clock', 23, 8); put('mn_armour', 34, 8); put('mn_bust', 26, 8); put('mn_bust', 31, 8)
    put('mn_flats', 22, 13); put('mn_palm', 35, 13); put('mn_books', 22, 11)
    put('mn_candelabra', 24, 14); put('mn_candelabra', 33, 14)
    for x in (26, 31): late.append((1, x, 15, P1('mn_newel')))            # newels at the stair head
    # ------------------------------------------------------------ stair hall: only the newels at the foot (on the gallery front)
    late.append((2, 26, 18, P1('mn_newel'))); late.append((2, 31, 18, P1('mn_newel')))
    # ------------------------------------------------------------ green room (TER): the company's dressing room
    put('mn_rail', 39, 8); put('mn_mirror', 42, 8); put('mn_dummy', 44, 8); put('mn_mirror', 46, 8); put('mn_books2', 50, 8)
    put('mn_sideboard', 48, 8); put('mn_candelabra', 40, 9); put('mn_candelabra', 49, 9)
    put('mn_trunk_open', 39, 13); put('mn_hatboxes', 40, 13); put('mn_sideboard2', 42, 13)
    put('mn_sofaG', 46, 13); put('mn_rocking', 50, 13)
    put('mn_trunk', 52, 10); put('mn_chair_left', 52, 11)
    # ------------------------------------------------------------ parlour
    put('mn_fire', 9, 18)                                                 # the cold fireplace
    put('mn_candelabra', 7, 18); put('mn_candelabra', 12, 18); put('mn_china', 13, 18)
    put('mn_books', 4, 18); put('mn_books', 5, 18); put('mn_books2', 15, 18)
    put('mn_sofaG', 9, 22); put('mn_chairR_right', 7, 21); put('mn_chairR_left', 13, 21); put('mn_tea', 10, 21)
    put('mn_piano', 3, 22); put('mn_harp', 17, 21); put('mn_gramophone', 16, 24); put('mn_globe', 14, 24)
    put('mn_sideboard2', 7, 24); put('mn_palm', 3, 20); put('mn_table_s', 17, 19)
    # ------------------------------------------------------------ conservatory
    put('mn_palm_big', 3, 30); put('mn_palm_big', 16, 30); put('mn_fountain', 9, 32)
    put('mn_grave_l', 4, 36); put('mn_grave_r', 5, 36); put('mn_trough_l', 14, 36); put('mn_trough_r', 15, 36)
    put('mn_bench', 9, 36); put('mn_fern', 7, 30); put('mn_orchid', 13, 30); put('mn_deadplant', 17, 33)
    put('mn_fern', 3, 34); put('mn_deadplant', 12, 34)
    put('mn_fern', 7, 33); put('mn_orchid', 13, 33); put('mn_candelabra', 8, 30); put('mn_candelabra', 12, 30)

    # ------------------------------------------------------------ dust, leaves, moonlight (walkable decals)
    top = {(x, y) for z, x, y, t in late if z == 2}
    for y in range(m.H):
        for x in range(m.W):
            if m.cls[y, x] != '.' or m.cliff[y, x] or (x, y) in top: continue
            r = (x * 37 + y * 101) % 23
            in_cons = (3 <= x <= 17 and 28 <= y <= 37)
            if in_cons and r < 4: late.append((2, x, y, P1('mn_leaves%d' % (r % 3))))
            elif in_cons and r == 5: late.append((2, x, y, P1('mn_shards')))
            elif r < 2: late.append((2, x, y, P1('mn_dust%d' % ((x + y) % 3))))
    for x, y in ((7, 9), (11, 9), (15, 9), (25, 9), (34, 9), (7, 31), (10, 31), (13, 31), (53, 27), (47, 27)):
        late.append((2, x, y, P1('mn_moon%d' % ((x + y) % 2))))
    for x, y in ((25, 33), (26, 34), (27, 35)): late.append((2, x, y, P1('mn_feet')))
    late.append((2, 6, 35, P1('mn_soil'))); late.append((2, 5, 35, P1('mn_soil')))
    late.append((2, 10, 24, P1('mn_petals'))); late.append((2, 30, 37, P1('mn_wax')))

    # ---- Subtle Gothic Atmosphere: Balanced Moonlight Window Shafts & Flickering Chandelier/Candelabra Glows! ----
    for sx, sy in ((6, 29), (13, 29),                             # Conservatory twin arched glass moonlight shafts
                   (6, 8), (14, 8),                               # Portrait Gallery flanking window shafts
                   (24, 8), (33, 8),                              # Upper Landing twin moonlight beams
                   (5, 18), (15, 18),                             # Parlour flanking window beams
                   (51, 26)):                                     # Dining Room east moonlight shaft (clear of table!)
        m.stamps.append(('cv_shaft', sx, sy))
    for gx, gy in ((26, 29), (31, 29), (9, 32), (9, 18)):         # Vestibule candelabras, Fountain & Parlour Hearth
        m.stamps.append(('pf_glow', gx, gy))

    # ------------------------------------------------------------ events
    O = PZ.ORDER
    E += [
        {'type': 'exit', 'at': [28, 39], 'link': 'R3_MANOR', 'arrive': [28, 38, 'up']},
        {'type': 'exit', 'at': [29, 39], 'link': 'R3_MANOR', 'arrive': [29, 38, 'up']},
        {'type': 'event', 'name': 'Dining-room door', 'at': [38, 31], 'pages': [
            {'graphic': {'tile': P1('mn_door')}, 'commands': [
                "The dining-room doors are locked. Somebody has scratched into the paint, over and over: ORDER. ORDER. ORDER.",
                {'if': '$game_variables[%d] > 0' % PZ.V_PORTRAIT, 'then': ["From upstairs comes the faint knock of a picture frame against a wall."]}]},
            {'cond': {'switch': PZ.S_GALLERY}, 'through': True}]},
        {'type': 'npc', 'name': 'Fenwick', 'at': [33, 33], 'sprite': 'NPC 03', 'dir': 'left', 'commands': [
            "Fenwick, the butler (a ghost): *(bows)* The Players are rehearsing. Do come in. Do not, under any circumstances, do anything you are asked.",
            "Fenwick: And mind the furniture. It moves when it thinks nobody is looking. Look at it, and it remembers its manners.",
            "Fenwick: If you must pass a chair, give it a wide berth: step aside early, while it's still far off, and keep a clear pace between you."]},
        {'type': 'sign', 'name': 'Portrait L', 'at': [25, 29], 'post': False,
         'text': "A portrait of a Thistledown actor in a crown. The eyes follow the light."},
        {'type': 'sign', 'name': 'Portrait R', 'at': [28, 8], 'post': False,
         'text': "A portrait of the whole company, AF 211. One face has been painted over."},
        {'type': 'sign', 'name': "Rosamund's diary", 'at': [17, 19], 'post': False, 'text':
         "A diary on the side table, in a looping hand: \"Hal always said the curtain call is the truest scene in any play. "
         "We bow in order of billing, smallest part first: the Fool, then dear young Laertes, then I, and my Hal last of all.\""},
        {'type': 'sign', 'name': 'Gallery note', 'at': [19, 8], 'post': False, 'text':
         "A note pinned by the door, in a butler's tidy hand: \"Mistress, the chairs will not stay out of the alcoves. "
         "Once one backs in under a case it cannot get out, so long as one keeps to the portrait side. - F.\""},
        {'type': 'sign', 'name': 'Nook card', 'at': [48, 26], 'post': False, 'text':
         "A card tucked into the wainscot: \"Mind the trapdoors to the cellar. They'll hold a child, but not a good armchair.\""},
    ]
    for key in PZ.ZONES:                                                   # the creeping armchairs
        for i, (x, y) in enumerate(PZ.Zone(key).chairs):
            pages = [{'graphic': {'sprite': 'pf_armchair', 'dir': 'down'}, 'commands': [
                "An armchair in faded green velvet. It's very still. Too still."]}]
            if key == 'd': pages.append({'cond': {'self': 'A'}})
            E.append({'type': 'event', 'name': 'Armchair %s%d' % (key, i + 1), 'at': [x, y], 'pages': pages})
    for pos, (x, y) in sorted(((k, c) for c, k in PZ.Zone('g').portrait.items())):
        who = PZ.WHO[pos]; rank = O.index(pos)
        E.append({'type': 'event', 'name': 'Portrait %d' % pos, 'at': [x, y - 1], 'pages': [
            {'graphic': {'tile': P1('mn_port%s_c' % who)}, 'commands': [{'script': 'pfm_portrait(%d)' % pos}]},
            {'cond': {'var': [PZ.V_PORTRAIT, rank + 1]}, 'graphic': {'tile': P1('mn_port%s' % who)}, 'commands': [{'script': 'pfm_portrait(%d)' % pos}]},
            {'cond': {'switch': PZ.S_GALLERY}, 'graphic': {'tile': P1('mn_port%s' % who)}, 'commands': [{'script': 'pfm_portrait(%d)' % pos}]}]})
    hx, hy = next(iter(PZ.Zone('d').portrait))
    E.append({'type': 'event', 'name': 'Attic hatch', 'at': [hx, hy - 1], 'pages': [
        {'graphic': {'tile': P1('mn_hatch')}, 'commands': [{'script': 'pfm_manor_hatch'}]},
        {'cond': {'switch': PZ.S_HATCH}, 'graphic': {'tile': P1('mn_ladder')}, 'commands': [
            "The attic ladder hangs down into the nook.",
            {'choices': ['Climb up.', 'Not yet.'], 'cancel': 2, 'branches': [[{'se': 'Door exit'}, {'transfer': {'map': 547, 'x': 4, 'y': 11, 'dir': 'up'}}], []]}]}]})
    # the ghosts' three scenes (existing events, kept), Dame Rosamund, the ghost girl, the Channeler, the Cleanse Tag
    E += scenes()
    E.append({'type': 'item', 'at': [16, 35], 'item': 'CLEANSETAG'})
    E.append(trainer((47, 11), 'CHANNELER', 'Mireille', 'left', "The spirits asked me to audition you!",
                     "They say you have presence. Ghostly presence.", sight=4))
    # the doll quest (TRIAL_EVENTS 546): three buttons
    cond = "quest_step(:EL_DOLL_WHO_WAITED) == :buttons"
    E.append(trial('Doll button 1', (43, 29), 'DOLL_BUTTON', tile=None, condition=cond))
    E.append(trial('Doll button 2', (10, 19), 'DOLL_BUTTON', tile=None, condition=cond))
    E.append(trial('Doll button 3', (24, 9), 'DOLL_BUTTON', tile=None, condition=cond))
    for e in E:
        if e.get('at') and tuple(e['at']) in free and not e.get('name', '').startswith(('Armchair', 'Portrait ', 'Attic hatch')):
            raise SystemExit('event %s stands in a puzzle room: %r' % (e.get('name'), e['at']))
    m.keep_clear |= free
    m.paint()

    # ---- Post-Paint Rich Parquet, Corridor Trim & Botanical Inlay Craft (100% L0 passable floor — ZERO puzzle passability changes!) ----
    # 1. Vestibule: rich dark-mahogany inlaid border framing the grand crimson carpet
    for y in range(28, 38):
        for x in range(21, 37):
            if m.cls[y, x] == '.' and (x in (23, 34) or y in (30, 36)):
                m.L[0, y, x] = P1('N_f%d' % ((x + y) % 4))
    # 2. Stair Hall (TEACH): warm honey-oak herringbone grand approach runner (27..30, 19..25) framed by mahogany trim (26, 31)!
    for y in range(19, 26):
        for x in range(24, 34):
            if m.cls[y, x] != '.':
                continue
            if 27 <= x <= 30:
                m.L[0, y, x] = P1('P_f%d' % ((x * 3 + y) % 4))
            elif x in (25, 26, 31, 32) or y in (19, 25):
                m.L[0, y, x] = P1('N_f%d' % ((x + y) % 4))
    # 3. Upper Landing & Green Room & Parlour & Gallery & Dining Room inlaid architectural floor borders!
    for y in range(9, 15):
        for x in range(23, 35):
            if m.cls[y, x] == '.' and (x in (23, 34) or y in (9, 14)):
                m.L[0, y, x] = P1('P_f%d' % ((x + y) % 4))
    for y in range(9, 14):
        for x in range(39, 52):
            if m.cls[y, x] == '.' and (x in (39, 51) or y in (9, 13)):
                m.L[0, y, x] = P1('N_f%d' % ((x + y) % 4))
    for y in range(19, 24):
        for x in range(4, 17):
            if m.cls[y, x] == '.' and (x in (4, 16) or y in (19, 23)):
                m.L[0, y, x] = P1('H_f%d' % ((x + y) % 4))
    for y in range(9, 14):
        for x in range(3, 19):
            if m.cls[y, x] == '.' and (y == 11 or x in (3, 18)):
                m.L[0, y, x] = P1('N_f%d' % ((x + y) % 4))
    for y in range(27, 32):
        for x in range(46, 53):
            if m.cls[y, x] == '.' and (x in (46, 52) or y in (27, 31)):
                m.L[0, y, x] = P1('H_f%d' % ((x + y) % 4))
    # 4. Crisp architectural corridor thresholds linking every manor wing (front doors, arches, hall passages!)
    for tx, ty in ((28, 37), (29, 37), (28, 38), (29, 38), (28, 39), (29, 39),  # Grand front foyer threshold
                   (28, 26), (29, 26), (28, 27), (29, 27),        # Vestibule <-> Stair Hall arch
                   (19, 9), (20, 9), (21, 9),                     # Landing <-> Portrait Gallery corridor
                   (36, 12), (37, 12),                            # Landing <-> Green Room corridor
                   (18, 33), (19, 33), (20, 33), (18, 34), (19, 34), (20, 34),  # Vestibule <-> Conservatory
                   (10, 26), (11, 26), (10, 27), (11, 27),        # Conservatory <-> Parlour
                   (37, 31), (38, 31), (39, 31)):                 # Vestibule <-> Dining Room corridor
        if m.cls[ty, tx] == '.':
            m.L[0, ty, tx] = P1('P_f%d' % ((tx + ty) % 2))
    # 5. Conservatory: dark stone/walnut (H_f*) garden court around fountain (8..10, 31..33) & grave/trough bays (zero harsh G_f* checker!)
    for y in range(31, 34):
        for x in range(8, 11):
            if m.cls[y, x] == '.':
                m.L[0, y, x] = P1('H_f%d' % ((x * 3 + y * 5) % 4))
    for bx0, bx1 in ((4, 6), (14, 16)):
        for y in (35, 36):
            for x in range(bx0, bx1 + 1):
                if m.cls[y, x] == '.':
                    m.L[0, y, x] = P1('H_f%d' % ((x + y) % 4))
    return m


def scenes():
    out = []
    def scene(name, at, sprite, d, opacity, line, choices, wins, loses, mon, after):
        n = int(name.split()[-1])                  # map builder 16: a won scene sets pfm :manor_scene_N (the attic finale reads it)
        out.append({'type': 'event', 'name': name, 'at': list(at), 'pages': [
            {'graphic': {'sprite': sprite, 'dir': d, 'opacity': opacity}, 'commands': [
                line, {'choices': choices, 'cancel': 0, 'branches': [
                    [wins, {'script': 'pfm_set(:manor_scene_%d)' % n}, {'selfswitch': ['A', True]}],
                    [loses[0], {'script': 'WildBattle.start(:%s, 13)' % mon}],
                    [loses[1], {'script': 'WildBattle.start(:%s, 13)' % mon}]]}]},
            {'cond': {'self': 'A'}, 'commands': [after]}]})
    scene('Scene 1', (30, 11), 'NPC 25', 'down', 160,
          "A ghostly actor in a ruff glares at you. \"You're late! Scene one - the battlements! Your line?\"",
          ["\"Who's there?\"", "\"Is this a Poké Ball I see before me?\"", "\"Line?\""],
          "\"...Perfect. PERFECT.\" The ghost wipes away a spectral tear.", ["\"WRONG PLAY!\" The ghost's Pokémon lunges out of the dark!", "\"LINE?! Off with them!\""],
          'GASTLY', "Only a cold spot where the actor stood.")
    scene('Scene 2', (6, 20), 'NPC 28', 'right', 255,
          "A ghostly queen sweeps toward you. \"Scene two! The closet! What do you say to your mother?\"",
          ["\"I must be cruel only to be kind.\"", "\"Mother, I've caught a Magikarp.\"", "*bow silently*"],
          "\"Exquisite.\" She fades, delighted.", ["\"HOW DARE YOU.\"", "\"A mime? In MY production?\""],
          'MISDREAVUS', "A faint scent of greasepaint lingers.")
    scene('Scene 3', (6, 34), 'NPC 03', 'down', 255,
          "A ghostly gravedigger holds up a Poké Ball like a skull. \"Scene three! The graveyard! Well?\"",
          ["\"Alas, poor Voltorb!\"", "\"Is it... empty?\"", "\"I'll take it.\""],
          "\"Alas indeed!\" He bows, cackling, and is gone.", ["\"EMPTY?!\"", "\"Props are NOT for keeping!\""],
          'DUSKULL', "Freshly turned earth on the conservatory tiles.")
    out.append({'type': 'event', 'name': 'Dame Rosamund', 'at': [12, 20], 'pages': [   # map builder 16: the welcome; the finale is the attic's
        {'graphic': {'sprite': 'NPC 28', 'dir': 'down', 'opacity': 180}, 'commands': [
            {'if': SCENES_DONE, 'then': [
                "Dame Rosamund: Three scenes, three triumphs! Darling, the second act is UPSTAIRS. The attic. The company is waiting.",
                "Dame Rosamund: Through the dining room and up the back stair. Mind the furniture. It is terribly jealous of the talent."],
             'else': [
                "Dame Rosamund: A visitor! An AUDIENCE! No - better! An ACTOR! We're one short for the second act. Our Laertes passed on. Again.",
                "Dame Rosamund: Three scenes, darling. Hit your marks, say your lines. Miss them, and the company gets... restless.",
                "Dame Rosamund: We heard there was trouble at the Lantern two nights ago. Somebody stopped the show. (A shudder blows out three candles.) Unthinkable. Nobody stops the show."]}]},
        {'cond': {'switch': 'THISTLEDOWN_CLEARED'}, 'commands': ["The parlour is quiet. On the mantel, a playbill: THE THISTLEDOWN PLAYERS - FINAL SEASON."]}]})
    out.append({'type': 'event', 'name': 'Ghost girl', 'at': [23, 34], 'pages': [
        {'graphic': {'sprite': 'NPC 07', 'dir': 'down', 'opacity': 140}, 'commands': [
            "A little girl in an old-fashioned dress: \"Mama says the play never ends. Is that true?\"", "When you blink, she's gone.",
            {'selfswitch': ['A', True]}]},
        {'cond': {'self': 'A'}}]})
    return out


SCENES_DONE = 'pfm?(:manor_scene_1) && pfm?(:manor_scene_2) && pfm?(:manor_scene_3)'


def finale():
    """Dame Rosamund's finale on the attic stage (story/21_SCRIPT_CH3.md, "Attic (547), after the third scene"; map builder
    16 moved it here from the parlour).  The gift is Sinistea, not the script's Litwick (Fire answers Tamsin: the
    distribution pass, POKEMON_AVAILABILITY Ch3)."""
    R = lambda t: 'Dame Rosamund: ' + t
    offer = [R("Stay. Join the company. Forever. The run never closes here, you know. Not ever. Nobody here has ever stopped a show."),
             "(In the wings, Fenwick the butler mouths a single word, very slowly: don't.)",
             {'choices': ['Thank you, but I have a gym to get to.', "I'd love to."], 'cancel': 1, 'branches': [
                 [R("(sighs) They always do. The good ones always have somewhere to be."), {'selfswitch': ['A', True]}],
                 [R("Wonderful! Wonderful! Places, everyone!"), "Fenwick: (very quietly) Oh, dear.",
                  "(The candles all go out at once. When they come back up, you are on the attic stage in a ruff, and the dust sheets are an audience.)",
                  {'script': 'Prismfall.game_over(:GO_CURTAIN_CALL)'}]]}]
    gfx = {'sprite': 'NPC 28', 'dir': 'down', 'opacity': 180}
    return {'type': 'event', 'name': 'Dame Rosamund', 'at': [17, 5], 'pages': [
        {'graphic': gfx, 'commands': [
            {'if': SCENES_DONE, 'then': [
                R("Bravo. BRAVO. Darling, you have it. The thing. We've been rehearsing for sixty years and never had it."),
                {'script': 'pbReceiveItem(:SPELLTAG)'},
                "A chipped teacup rattles out of a costume trunk and follows you. It wants to see the second act.",
                {'script': 'pbAddPokemon(:SINISTEA, 14)'},
                {'switch': ['THISTLEDOWN_CLEARED', True]}, {'selfswitch': ['B', True]},
                {'script': 'Prismfall.checkpoint'}] + offer,         # (a reload after the curtain call lands on page B: the offer again, no second gift)
             'else': [R("Not yet, darling! The second act can't begin without the first. Your scenes: the battlements, the closet, the graveyard.")]}]},
        {'cond': {'self': 'B'}, 'graphic': gfx, 'commands': offer},
        {'cond': {'self': 'A'}, 'commands': ["The little stage is empty. In the front row the dust sheets seem to be applauding, very quietly."]}]}


# ================================================================================================ 547 the attic
def build_547():
    m = Manor(24, 16, 547)
    m.kit = {'default': 'cvF'}
    m.room_box(2, 2, 21, 13, FLOOR, 'A', 'A')
    m.box(4, 14, 4, 14, FLOOR)                     # the ladder hole down to the nook
    m.plan_cliffs(rows=3)
    late = m.late = []
    E = m.events
    m.on('mn_oculus', 11, 1)                       # the round gable window (lip + face rows)
    for x, y in ((11, 4), (12, 5), (12, 4), (13, 5)): late.append((2, x, y, P1('mn_moon%d' % ((x + y) % 2))))
    for x, y, n in ((2, 1, 'mn_web_l'), (21, 1, 'mn_web_r'), (6, 2, 'mn_webhang'), (17, 2, 'mn_webhang')):
        late.append((2, x, y, P1(n)))
    for name, x, y in (('mn_rail', 2, 3), ('mn_flats', 5, 3), ('mn_mirror', 8, 3), ('mn_dummy', 15, 3), ('mn_flats', 17, 3),
                       ('mn_trunk_open', 20, 4), ('mn_hatboxes', 21, 5), ('mn_rocking', 2, 8), ('mn_trunk', 2, 12),
                       ('mn_sheet_sofa', 7, 12), ('mn_sheet_tall', 20, 9), ('mn_sheet_chair', 13, 12), ('mn_trunk', 21, 12),
                       ('mn_sheet_chair', 16, 12), ('mn_sheet_table', 9, 8), ('mn_books', 13, 3), ('mn_trunk', 3, 6),
                       ('hb_crates4', 18, 11), ('mn_hatboxes', 19, 12), ('mn_sheet_tall', 6, 9), ('mn_trunk_open', 21, 7),
                       ('mn_umbrella', 3, 10), ('mn_globe', 12, 9), ('mn_sheet_chair', 4, 8)):
        m.on(name, x, y)
    for x in range(14, 20): late.append((2, x, 7, P1('mn_footlight')))   # the little stage's footlights
    m.rug('R', 14, 4, 19, 6, medallion=False)
    for y in range(4, 14):
        for x in range(2, 22):
            if (x * 13 + y * 7) % 11 == 0: late.append((2, x, y, P1('mn_dust%d' % ((x + y) % 3))))
    E += [
        {'type': 'warp', 'name': 'Stairs down', 'at': [4, 14], 'to': {'map': 546, 'x': 49, 'y': 24, 'dir': 'down'}, 'se': 'Door exit'},
        {'type': 'event', 'name': 'Greavard', 'at': [10, 11], 'pages': [
            {'graphic': {'tile': P1('mn_sheet_chair')}, 'commands': [
                "Something under a dust sheet wags its tail.", {'script': 'WildBattle.start(:GREAVARD, 16)'}, {'selfswitch': ['A', True]}]},
            {'cond': {'self': 'A'}}]},
        {'type': 'item', 'at': [19, 5], 'item': 'REVIVE'},                          # (the Spell Tag is Dame Rosamund's now)
        finale(),
        trial('Rag doll', (13, 4), 'ATTIC_DOLL', sprite='Followers/SHUPPET', condition='badges >= 14'),
        {'type': 'sign', 'name': 'Attic stage', 'at': [16, 4], 'post': False, 'text':
         "A little stage of packing-case boards, with tin footlights. Chalked on the back wall: ACT II - TONIGHT - AND EVERY NIGHT."},
    ]
    m.paint()
    return m


def write(m, mid, name, extra=None):
    head = {'id': mid, 'name': name, 'parent': 540 if mid == 546 else 546, 'bgm': 'Cave', 'field': FIELD,
            'metadata': {'MapPosition': [0, 12, 21]}, 'tone': TONE, '_file': '%d_thistledown_manor.yaml' % mid}
    head.update(extra or {})
    m.write(mid, head, comment='# GENERATED by mapgen/layouts/manor.py (map builder 14): Thistledown Manor on the manor kit (tileset 59),\n'
                               '# DUNGEON_PUZZLES D5 (puzzles/manor.py).  Edit the layout script, not this file.\n')


def main(which=None):
    sel = set(which or [])
    os.makedirs('/tmp/mb14', exist_ok=True)
    if not sel or '546' in sel:
        m = build_546(); m.preview('/tmp/mb14/m546.png', scale=0.5)
        write(m, 546, 'Thistledown Manor', {'gates': [{'name': 'Dining room (locked until the portraits are set)', 'from': [[28, 37]],
                                                       'sealed': [[46, 30], [49, 24]]}]})
    if not sel or '547' in sel:
        m = build_547(); m.preview('/tmp/mb14/m547.png', scale=0.5)
        write(m, 547, 'Thistledown Manor - Attic')


if __name__ == '__main__':
    main(sys.argv[1:])
