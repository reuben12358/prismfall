# -*- coding: utf-8 -*-
"""Velmora's physical geography in town-map grid units (x 0-30 east, y 0-20 south; square (x, y) spans x..x+1).

Owner: world cartographer. Read by gen_world_map.py (both images) and quoted by design/WORLD_MAP.md.
Kept apart from world_data.py so names and roads can change without redrawing the coast.
Geography v2 (user, 2026-11-19; SPINE Revision 18): Ossaria north, Isenmar west, Ashkaar east, Zenith (with Nadir
beneath it) south, Elowen in the middle around the Crownwall. The Ashkaar-Isenmar war is fought on land, in Ossaria's
western dunes (WAR below). The coast is unchanged except the north shore by the war front and the islands.
"""

MAINLAND = [
    (1.6, 2.1), (2.3, 1.7), (2.9, 1.9), (3.0, 2.95), (3.7, 3.2), (4.3, 2.8), (4.7, 2.05), (5.6, 2.15), (6.0, 1.75),
    (6.25, 0.95), (6.9, 0.75), (7.35, 1.55), (8.2, 1.6), (9.4, 1.75), (10.7, 1.45), (11.6, 1.25), (12.25, 1.05),
    (13.2, 0.95), (13.95, 1.0), (14.25, 1.15), (15.1, 0.95), (16.3, 1.0), (17.1, 1.35), (18.4, 1.65), (19.7, 1.5),
    (20.9, 1.45), (22.1, 1.3), (23.2, 1.55), (24.3, 1.45), (25.1, 1.75), (25.9, 2.5), (26.6, 2.75), (27.15, 3.1),
    (27.25, 3.85), (27.05, 4.6), (27.35, 5.6), (27.1, 6.4), (27.6, 7.2), (28.0, 8.2), (27.7, 9.3), (28.0, 10.4),
    (27.7, 11.5), (27.2, 12.4), (26.6, 13.3), (25.7, 14.15), (24.95, 15.0), (24.85, 16.2), (24.3, 17.25), (23.6, 17.9),
    (22.4, 18.35), (21.2, 18.55), (20.2, 18.3), (19.1, 18.45), (17.9, 18.7), (16.9, 18.95), (15.9, 18.6),
    (14.8, 18.25), (13.7, 18.5), (13.05, 18.95), (12.1, 19.05), (11.0, 18.9), (10.0, 19.05), (8.9, 18.95),
    (7.9, 19.1), (7.0, 19.0), (6.1, 19.1), (5.2, 18.85), (4.55, 18.3), (4.35, 17.5), (4.6, 16.7), (4.25, 16.05),
    (3.8, 15.45), (4.1, 14.85), (4.55, 14.3), (4.6, 13.55), (4.15, 12.8), (3.55, 12.05), (3.3, 11.1), (2.95, 10.2),
    (2.55, 9.6), (2.15, 8.85), (2.35, 8.05), (2.75, 7.75), (3.25, 7.3), (2.45, 6.95), (1.95, 6.25), (2.15, 5.55),
    (1.7, 4.6), (1.85, 3.6), (1.45, 2.9),
]
ISLANDS = [
    # the Shardfall Isles (postgame) in the Hallow Strait, south of the Gloamwood
    [(21.4, 19.25), (22.1, 19.05), (22.7, 19.35), (22.4, 19.75), (21.65, 19.7)],
    [(23.2, 19.45), (23.65, 19.35), (23.85, 19.7), (23.4, 19.85)],
    [(20.4, 19.55), (20.8, 19.45), (20.95, 19.75), (20.55, 19.85)],
    # sea stacks off Lacecliff Walk
    [(10.3, 19.3), (10.55, 19.25), (10.6, 19.45), (10.35, 19.5)],
]
LAKES = {
    'Lake Sallow': dict(poly=[(21.45, 11.05), (21.95, 10.85), (22.65, 10.95), (22.95, 11.4), (22.6, 11.9), (21.95, 11.95),
                              (21.5, 11.6)], kind='sulfur'),
    'Mirror Mere': dict(poly=[(10.2, 6.35), (10.6, 6.15), (10.9, 6.4), (10.8, 6.8), (10.4, 6.85), (10.15, 6.6)],
                        kind='mirror'),
    'Saltmere Lagoon': dict(poly=[(7.25, 17.55), (7.75, 17.35), (8.1, 17.6), (7.9, 18.0), (7.4, 18.05)], kind='salt'),
    'Lake Rime': dict(poly=[(3.05, 2.9), (3.5, 2.55), (4.1, 2.6), (4.05, 3.05), (3.6, 3.2)], kind='frozen'),
}
# Zenith's plateau (the City Above) in the south: a raised tableland; its edge is the Escarpment. Nadir lies beneath
# it (the same footprint): Ironreach and Mirefen at its north foot, Underveil on the drowned coast under its south cliff.
PLATEAU = [(15.1, 13.95), (16.6, 13.85), (18.3, 13.95), (19.8, 13.8), (20.6, 13.95), (21.0, 14.6), (21.05, 15.6),
           (20.8, 16.6), (20.35, 17.5), (19.6, 17.85), (18.4, 17.95), (17.1, 17.9), (15.9, 17.75), (15.2, 17.2),
           (14.95, 16.2), (14.95, 14.9)]
# mountain ridges: (polyline, height, width)
RIDGES = [
    ([(4.2, 6.3), (4.9, 5.2), (5.8, 4.4), (6.7, 3.7), (7.6, 3.4)], 1.0, 0.75),            # the Frostfang Mountains
    ([(1.9, 4.2), (2.6, 3.7)], 0.55, 0.45),                                                 # Stillwater fells
    ([(19.6, 1.85), (20.7, 1.65), (21.9, 1.9), (23.0, 2.2)], 0.9, 0.55),                   # the Crags of Ossaria
    ([(19.1, 2.3), (19.35, 3.1)], 0.7, 0.35),                                               # the Jawbone Ridge
    ([(24.9, 11.0), (25.8, 11.5), (26.4, 12.1)], 1.0, 0.5),                               # the Cinderhorn's shoulders
    ([(23.5, 14.7), (24.4, 14.15), (25.3, 13.75)], 0.8, 0.4),                               # the Wyrmspine
    ([(9.0, 12.1), (10.2, 12.4)], 0.45, 0.6),                                               # the Spinners' fells
    ([(26.2, 5.0), (26.8, 6.5), (27.0, 8.0)], 0.6, 0.55),                                   # the Dragonback (east coast)
    ([(18.1, 4.7), (18.7, 5.25)], 0.35, 0.4),                                               # the Kneeling hills
]
VOLCANO = (25.7, 10.3)               # the Cinderhorn, above Cindervault
CROWNWALL = dict(c=(14.5, 9.5), r=1.6, w=0.42, gap_angle=27)   # gap: towards Pilgrim's Rest (south-east)
GLACIER = [(6.15, 0.95), (6.9, 0.75), (7.3, 1.6), (7.1, 2.6), (6.4, 2.8), (6.0, 2.0)]
FROZEN_SEA_EDGE_Y = 2.7             # Isenmar's frozen sea: north of this line and west of FROZEN_SEA_X_MAX
FROZEN_SEA_X_MAX = 9.6              # east of it the northern sea is open water along Ossaria's coast
SHATTERED_ICE = None                # Revision 18: the war is not fought at sea any more

RIVERS = {
    'River Ebb': dict(pts=[(11.1, 8.3), (10.0, 8.0), (8.9, 7.65), (7.6, 7.3), (6.4, 7.5), (5.2, 7.35), (4.2, 7.55),
                           (3.0, 7.55)], w=(0.04, 0.16), kind='water'),
    'River Selvedge': dict(pts=[(11.9, 13.9), (11.3, 14.8), (10.4, 15.75), (9.4, 15.65), (8.5, 15.8), (7.7, 16.6),
                                (7.5, 17.4)], w=(0.04, 0.12), kind='water'),
    'The Prism': dict(pts=[(10.6, 6.8), (10.75, 8.0), (11.0, 9.4), (11.35, 10.7), (11.6, 11.9), (11.8, 12.9),
                           (11.9, 13.9)], w=(0.03, 0.08), kind='water'),
    'River Leach': dict(pts=[(18.5, 4.6), (19.1, 5.6), (19.6, 6.8), (20.2, 8.2), (20.4, 9.8), (20.6, 11.3),
                             (20.6, 12.4), (20.8, 13.3)], w=(0.03, 0.1), kind='water'),
    'The Outfall': dict(pts=[(19.8, 13.9), (20.4, 13.0)], w=(0.03, 0.06), kind='toxic'),
    'Spinefall': dict(pts=[(22.4, 2.2), (22.5, 3.3), (22.3, 4.4), (21.7, 5.3)], w=(0.03, 0.07), kind='water'),
    'Gloam Water': dict(pts=[(22.2, 15.6), (22.5, 16.7), (22.7, 18.3)], w=(0.04, 0.1), kind='water'),
    'Thornrun': dict(pts=[(24.0, 15.3), (24.1, 16.4), (23.9, 17.6)], w=(0.03, 0.07), kind='water'),
}
# the Blindwater runs underground from Underveil east under the plateau's south cliff to the Gloamwood (drawn dotted)
BLINDWATER = [(16.9, 18.45), (17.9, 18.55), (18.9, 18.5), (19.9, 18.55), (20.9, 18.4), (21.5, 18.5)]

# forests: (x, y, radius, kind)
FORESTS = [
    (11.3, 14.2, 1.55, 'silk'), (12.6, 14.6, 0.75, 'silk'), (10.2, 13.6, 0.8, 'broad'), (8.4, 11.2, 0.95, 'broad'),
    (9.6, 9.1, 1.0, 'broad'), (13.2, 16.6, 0.6, 'broad'), (22.8, 16.8, 1.15, 'gloam'), (21.9, 17.7, 0.6, 'gloam'),
    (4.8, 10.6, 1.35, 'rime'), (5.9, 9.3, 1.15, 'rime'), (6.9, 10.6, 0.6, 'rime'), (5.0, 5.4, 1.0, 'pine'),
    (2.8, 4.9, 0.85, 'pine'), (7.5, 8.4, 0.6, 'pine'), (17.9, 12.3, 0.7, 'wired'), (11.2, 7.2, 0.7, 'glass'),
    (13.6, 12.9, 0.6, 'fungus'), (23.4, 15.9, 0.8, 'ash'), (21.4, 8.1, 0.75, 'ash'), (23.1, 12.1, 0.5, 'ash'),
    (24.3, 5.4, 0.55, 'petrified'), (8.0, 13.9, 0.6, 'broad'), (7.0, 14.6, 0.5, 'broad'), (13.9, 15.4, 0.5, 'broad'),
    (17.9, 7.6, 0.7, 'broad'), (12.0, 10.4, 0.45, 'broad'), (19.0, 9.6, 0.55, 'broad'), (16.6, 5.9, 0.4, 'broad'),
]
MARSHES = [(20.8, 13.35, 0.8), (21.4, 12.6, 0.4), (6.6, 17.1, 0.6), (20.3, 9.0, 0.35)]
DESERT_DUNES = [(11.0, 2.6, 1.2), (13.6, 2.4, 1.1), (16.0, 3.2, 1.0), (14.4, 4.2, 0.8), (18.8, 4.4, 0.6),
                (21.6, 3.4, 0.6), (9.8, 3.8, 0.6)]
OBSIDIAN = [(23.8, 5.6, 0.85)]   # the Cinderglass Barrens
SULFUR = [(22.3, 11.0, 0.9)]

# zone anchors (extra Voronoi seeds that shape the kingdoms; road cells and towns are seeds too). Nadir has no surface
# zone: it is beneath Zenith (gen_world_map maps Nadir seeds to Zenith).
ANCHORS = [
    ('Elowen', 8.5, 17.0), ('Elowen', 10.5, 16.6), ('Elowen', 13.9, 17.6), ('Elowen', 9.2, 13.6), ('Elowen', 7.4, 14.2),
    ('Elowen', 13.2, 15.3), ('Elowen', 10.9, 12.2), ('Elowen', 7.6, 10.4), ('Elowen', 9.8, 8.6), ('Elowen', 12.0, 6.0),
    ('Elowen', 13.2, 5.9), ('Elowen', 17.4, 6.2), ('Elowen', 18.8, 8.4), ('Elowen', 19.2, 10.2), ('Elowen', 17.6, 12.2),
    ('Elowen', 12.2, 10.4), ('Elowen', 16.6, 8.2), ('Elowen', 21.0, 6.4), ('Elowen', 22.5, 17.6), ('Elowen', 22.8, 15.4),
    ('Elowen', 22.3, 13.2), ('Elowen', 10.0, 6.2), ('Elowen', 14.4, 12.6), ('Elowen', 22.2, 13.9),
    ('Elowen', 22.3, 14.7), ('Elowen', 22.2, 15.6), ('Elowen', 22.0, 16.3), ('Elowen', 22.6, 12.6), ('Elowen', 21.4, 12.4),
    ('Elowen', 20.0, 11.7), ('Elowen', 13.7, 11.45), ('Elowen', 15.4, 11.4), ('Elowen', 12.6, 10.9),
    ('Isenmar', 2.6, 4.6), ('Isenmar', 3.0, 6.1), ('Isenmar', 5.6, 3.3), ('Isenmar', 2.3, 2.4), ('Isenmar', 4.0, 5.6),
    ('Isenmar', 3.0, 7.0), ('Isenmar', 6.6, 4.6), ('Isenmar', 7.4, 5.6), ('Isenmar', 5.0, 1.6),
    ('Ossaria', 10.6, 3.2), ('Ossaria', 12.6, 3.6), ('Ossaria', 14.2, 1.8), ('Ossaria', 16.2, 2.0), ('Ossaria', 18.1, 2.6),
    ('Ossaria', 20.0, 1.8), ('Ossaria', 21.6, 3.3), ('Ossaria', 17.6, 4.4), ('Ossaria', 11.2, 4.4), ('Ossaria', 9.9, 2.4),
    ('Ossaria', 13.4, 4.4), ('Ossaria', 20.4, 4.5), ('Ossaria', 22.6, 2.6),
    ('Ashkaar', 26.4, 8.2), ('Ashkaar', 26.4, 11.0), ('Ashkaar', 24.6, 11.0), ('Ashkaar', 25.2, 12.4),
    ('Ashkaar', 26.0, 4.0), ('Ashkaar', 26.6, 6.6), ('Ashkaar', 24.6, 7.0), ('Ashkaar', 24.8, 14.3), ('Ashkaar', 23.9, 9.8),
    ('Ashkaar', 25.0, 2.5),
    ('Zenith', 16.0, 14.8), ('Zenith', 18.0, 15.8), ('Zenith', 20.0, 15.0), ('Zenith', 17.0, 17.4), ('Zenith', 19.5, 16.6),
    ('Zenith', 15.6, 16.8), ('Zenith', 20.4, 14.6), ('Zenith', 18.8, 13.6), ('Zenith', 20.4, 16.4),
    ('Crownhaven', 14.5, 9.5), ('Crownhaven', 13.9, 9.0), ('Crownhaven', 15.1, 10.1),
]

SEAS = [  # label, x, y, angle, size
    ("THE NORTHERN SEA", 17.6, 0.45, 0, 0.9),
    ("THE HALLOW STRAIT", 8.6, 19.62, 0, 0.9),
    ("THE WESTERN DEEP", 0.75, 12.0, 90, 0.85),
    ("THE EMBER SEA", 29.0, 9.5, -90, 0.85),
]
LANDMARKS = [  # label, x, y, size, angle
    ("The Frostfang Mountains", 5.6, 4.15, 0.55, -38),
    ("The Escarpment", 14.55, 16.0, 0.42, -84),
    ("The Crags", 21.3, 1.15, 0.46, 0),
    ("The Cinderhorn", 26.4, 11.2, 0.5, 0),
    ("The Crownwall", 14.5, 7.55, 0.45, 0),
    ("Gossamer Wood", 12.25, 15.05, 0.5, 0),
    ("The Gloamwood", 23.0, 18.25, 0.45, 0),
    ("The Rimewood", 4.6, 11.25, 0.5, 0),
    ("Lake Sallow", 22.2, 12.25, 0.34, 0),
    ("Mirror Mere", 10.1, 5.7, 0.34, 0),
    ("Lake Rime", 3.6, 3.45, 0.36, 0),
    ("River Ebb", 6.4, 7.95, 0.34, 0),
    ("River Leach", 20.95, 9.3, 0.32, -80),
    ("The Brass Dunes", 13.3, 4.7, 0.38, 0),
    ("Cinderglass Barrens", 24.9, 5.0, 0.36, 0),
    ("The Mast Glacier", 6.75, 0.45, 0.38, 0),
    ("Drowned Aurelia", 17.4, 19.45, 0.4, 0),
    ("Mirefen Marsh", 21.9, 13.0, 0.32, 0),
    ("Selvedge", 9.4, 16.15, 0.32, 0),
    ("The Crownlands", 17.1, 6.35, 0.36, 0),
]
KINGDOM_LABELS = [  # name, subtitle, x, y
    ("ELOWEN", "the Evergreen Crown", 9.2, 16.4),
    ("ISENMAR", "the Frozen Sea", 3.7, 0.62),
    ("ZENITH", "the City Above", 17.75, 15.35),
    ("NADIR", "the City Below", 19.25, 18.95),
    ("OSSARIA", "the Bone Sands", 18.0, 1.4),
    ("ASHKAAR", "the Dragonfire Dominion", 26.0, 11.6),
    ("CROWNHAVEN", "the Accord's Seat", 14.5, 11.1),
]
KINGDOM_LABELS_FIXED = ('ZENITH', 'NADIR')   # Nadir is beneath Zenith: its name sits on the drowned coast
SEA_LANES = [  # (points, kind, label)
    ([(12.5, 18.6), (12.4, 19.6), (12.0, 20.4)], 'ferry', "the Last Ferry (from beyond the Strait)"),
    ([(6.4, 18.7), (5.0, 19.4), (3.0, 18.6), (1.6, 14.0), (1.6, 9.5), (3.0, 7.7)], 'ferry', "the coast packet"),
    ([(12.5, 18.6), (15.0, 19.55), (21.6, 19.55)], 'ferry', ""),
]
AIR_LANES = []   # the Mast Road's airship leg (Anchorhold -> Skyreach) is drawn from ROAD_PATHS ('air')

# the war in the sands (Revision 18): fire and ice never border, so they meet on neutral Ossarian ground
WAR = dict(
    isenmar=[(3.5, 2.5), (4.6, 1.6), (5.6, 1.5), (6.5, 2.4), (7.6, 2.5), (9.5, 2.5), (11.5, 2.5), (12.5, 2.5)],
    ashkaar=[(24.5, 8.5), (24.4, 6.5), (23.5, 5.5), (23.5, 4.5), (22.9, 5.25), (20.9, 5.25), (19.3, 4.1),
             (18.2, 1.6), (16.6, 1.6), (15.5, 2.5), (14.2, 2.5)],
    front=[(12.95, 0.95), (13.15, 1.6), (12.85, 2.3), (13.15, 3.0), (12.9, 3.6)],   # the Steamline
    battlefield=(13.5, 2.5),        # the Glass Dunes (map 926)
    camps={'isenmar': (9.5, 2.5), 'ashkaar': (15.5, 2.5)},   # Skaldfast; the Ashkaar Siege Camp (924)
    labels=[("The Glass Dunes", 13.6, 3.25, 0.42), ("the Steamline", 12.6, 0.62, 0.3),
            ("The Rimed Sands", 11.3, 1.55, 0.32), ("Siege Camp", 15.9, 1.55, 0.3)],
)
