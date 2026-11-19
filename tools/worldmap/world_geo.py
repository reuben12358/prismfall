# -*- coding: utf-8 -*-
"""Velmora's physical geography in town-map grid units (x 0-30 east, y 0-20 south; square (x, y) spans x..x+1).

Owner: world cartographer. Read by gen_world_map.py (both images) and quoted by design/WORLD_MAP.md.
Kept apart from world_data.py so names and roads can change without redrawing the coast.
"""

MAINLAND = [
    (1.6, 2.1), (2.3, 1.7), (2.9, 1.9), (3.0, 2.95), (3.7, 3.2), (4.3, 2.8), (4.7, 2.05), (5.6, 2.15), (6.0, 1.75),
    (6.25, 0.95), (6.9, 0.75), (7.35, 1.55), (8.2, 1.6), (9.4, 1.75), (10.7, 1.45), (11.6, 1.25), (12.25, 1.95),
    (13.2, 2.2), (13.95, 1.95), (14.25, 1.15), (15.1, 0.95), (16.3, 1.0), (17.1, 1.35), (18.4, 1.65), (19.7, 1.5),
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
    # the Rime Isles (Isenmar; Skaldfast) at the far end of the frozen north sea
    [(27.25, 0.45), (28.0, 0.12), (28.75, 0.2), (29.3, 0.65), (29.05, 1.3), (28.3, 1.45), (27.6, 1.25)],
    [(29.35, 1.55), (29.85, 1.65), (29.9, 2.25), (29.4, 2.35), (29.15, 1.95)],
    # the Shardfall Isles (postgame) in the Hallow Strait
    [(18.9, 19.25), (19.6, 19.05), (20.2, 19.35), (19.9, 19.75), (19.15, 19.7)],
    [(20.7, 19.45), (21.15, 19.35), (21.35, 19.7), (20.9, 19.85)],
    [(17.9, 19.55), (18.3, 19.45), (18.45, 19.75), (18.05, 19.85)],
    # sea stacks off Lacecliff Walk
    [(10.3, 19.3), (10.55, 19.25), (10.6, 19.45), (10.35, 19.5)],
]
LAKES = {
    'Lake Sallow': dict(poly=[(19.05, 9.85), (19.6, 9.55), (20.5, 9.6), (21.05, 10.0), (20.85, 10.75), (20.1, 10.95),
                             (19.4, 10.8), (19.0, 10.35)], kind='sulfur'),
    'Mirror Mere': dict(poly=[(14.25, 10.25), (14.7, 10.1), (15.0, 10.4), (14.85, 10.8), (14.4, 10.85), (14.15, 10.55)],
                        kind='mirror'),
    'Saltmere Lagoon': dict(poly=[(7.25, 17.55), (7.75, 17.35), (8.1, 17.6), (7.9, 18.0), (7.4, 18.05)], kind='salt'),
    'Lake Rime': dict(poly=[(3.05, 2.9), (3.5, 2.55), (4.1, 2.6), (4.05, 3.05), (3.6, 3.2)], kind='frozen'),
}
# Zenith's plateau (the City Above): a raised tableland; its edge is the Escarpment
PLATEAU = [(8.55, 2.2), (10.5, 1.85), (12.1, 2.25), (14.1, 2.05), (15.4, 1.4), (16.9, 1.75), (17.7, 2.6),
           (17.3, 3.9), (16.6, 5.3), (15.3, 6.25), (13.6, 6.55), (11.6, 6.75), (10.1, 6.6), (9.15, 6.0), (8.6, 4.8),
           (8.35, 3.3)]
# mountain ridges: (polyline, height, width)
RIDGES = [
    ([(4.2, 6.3), (4.9, 5.2), (5.8, 4.4), (6.7, 3.7), (7.6, 3.4)], 1.0, 0.75),            # the Frostfang Mountains
    ([(1.9, 4.2), (2.6, 3.7)], 0.55, 0.45),                                                 # Stillwater fells
    ([(19.8, 2.4), (21.0, 2.1), (22.3, 2.3), (23.4, 2.1), (25.0, 2.3), (25.7, 3.0)], 0.9, 0.7),  # the Crags of Ossaria
    ([(23.4, 3.2), (23.6, 4.3), (23.4, 5.4), (23.6, 6.3)], 0.85, 0.45),                   # the Jawbone Ridge
    ([(24.6, 10.4), (25.6, 11.5), (26.2, 12.6)], 1.0, 0.6),                                # the Cinderhorn's shoulders
    ([(21.4, 16.0), (22.5, 16.35), (23.6, 16.2), (24.6, 16.6)], 0.85, 0.5),               # the Wyrmspine
    ([(9.0, 12.1), (10.2, 12.4)], 0.45, 0.6),                                               # the Spinners' fells
    ([(26.0, 6.2), (26.6, 7.6), (26.9, 9.0)], 0.6, 0.6),                                    # the Dragonback (east coast)
    ([(18.2, 5.8), (19.0, 6.9)], 0.35, 0.5),                                                # the Kneeling hills
]
VOLCANO = (25.55, 11.55)            # the Cinderhorn
CROWNWALL = dict(c=(19.5, 14.45), r=1.75, w=0.5, gap_angle=-25)   # gap: the Pilgrim Pass on the east side
GLACIER = [(6.15, 0.95), (6.9, 0.75), (7.3, 1.6), (7.1, 2.6), (6.4, 2.8), (6.0, 2.0)]
FROZEN_SEA_EDGE_Y = 2.7             # the frozen north sea: everything north of this (west of the strait) is ice
SHATTERED_ICE = (26.3, 1.4, 29.5, 3.6)  # broken floes between the Rime Isles and Cinder Cape

RIVERS = {
    'River Ebb': dict(pts=[(9.3, 7.2), (8.2, 7.45), (7.0, 7.3), (5.8, 7.55), (4.7, 7.35), (3.6, 7.55), (3.0, 7.55)],
                      w=(0.05, 0.16), kind='water'),
    'River Selvedge': dict(pts=[(11.9, 13.9), (11.3, 14.8), (10.4, 15.75), (9.4, 15.65), (8.5, 15.8), (7.7, 16.6),
                                (7.5, 17.4)], w=(0.04, 0.12), kind='water'),
    'The Prism': dict(pts=[(14.4, 10.6), (13.3, 11.2), (12.3, 11.3), (11.6, 11.9), (11.8, 12.9), (11.9, 13.9)],
                      w=(0.03, 0.08), kind='water'),
    'River Leach': dict(pts=[(22.2, 7.2), (21.3, 7.8), (20.4, 8.6), (19.3, 8.4), (18.2, 8.7), (17.2, 9.3), (16.6, 9.7)],
                        w=(0.03, 0.1), kind='toxic'),
    'The Outfall': dict(pts=[(13.6, 6.5), (14.4, 7.6), (15.4, 8.6), (16.2, 9.4)], w=(0.03, 0.08), kind='water'),
    'Spinefall': dict(pts=[(24.6, 2.9), (24.5, 4.2), (24.8, 5.5), (24.4, 6.6), (23.6, 7.3)], w=(0.03, 0.07), kind='water'),
    'Gloam Water': dict(pts=[(15.3, 15.9), (15.9, 16.6), (16.3, 17.6), (16.6, 18.7)], w=(0.04, 0.1), kind='water'),
    'Thornrun': dict(pts=[(20.6, 15.8), (20.9, 16.9), (20.7, 18.3)], w=(0.03, 0.07), kind='water'),
}
# the Blindwater runs underground from Underveil to the Gloamwood (drawn dotted)
BLINDWATER = [(12.4, 2.0), (12.2, 4.5), (12.9, 7.5), (13.4, 10.0), (13.7, 12.6), (14.4, 14.3), (15.2, 15.7)]

# forests: (x, y, radius, kind)
FORESTS = [
    (11.3, 14.2, 1.55, 'silk'), (12.6, 14.6, 0.75, 'silk'), (10.2, 13.6, 0.8, 'broad'), (8.4, 11.2, 0.95, 'broad'),
    (9.6, 9.1, 1.0, 'broad'), (13.2, 16.6, 0.6, 'broad'), (16.6, 16.7, 1.65, 'gloam'), (14.8, 17.6, 0.7, 'gloam'),
    (4.8, 10.6, 1.35, 'rime'), (5.9, 9.3, 1.15, 'rime'), (6.9, 10.6, 0.6, 'rime'), (5.0, 5.4, 1.0, 'pine'),
    (2.8, 4.9, 0.85, 'pine'), (7.5, 8.4, 0.6, 'pine'), (11.5, 7.9, 0.85, 'wired'), (12.7, 9.6, 0.75, 'glass'),
    (14.6, 12.6, 0.75, 'fungus'), (19.6, 17.1, 1.15, 'ash'), (24.4, 8.4, 0.6, 'petrified'), (8.0, 13.9, 0.6, 'broad'),
    (7.0, 14.6, 0.5, 'broad'), (13.9, 15.4, 0.5, 'broad'),
]
MARSHES = [(16.2, 9.9, 0.95), (15.4, 9.2, 0.55), (6.6, 17.1, 0.6), (17.9, 10.4, 0.5)]
DESERT_DUNES = [(18.0, 4.6, 1.2), (20.5, 4.6, 1.3), (21.0, 6.3, 1.0), (16.5, 5.0, 0.8), (22.5, 5.2, 0.8)]
OBSIDIAN = [(25.2, 8.7, 0.9)]
SULFUR = [(20.0, 10.2, 1.2)]

# zone anchors (extra Voronoi seeds that shape the kingdoms; road cells and towns are seeds too)
ANCHORS = [
    ('Elowen', 8.5, 17.0), ('Elowen', 10.5, 16.6), ('Elowen', 14.2, 17.8), ('Elowen', 9.2, 13.6), ('Elowen', 7.4, 14.2),
    ('Elowen', 13.2, 15.3), ('Elowen', 10.9, 12.2), ('Elowen', 14.0, 16.9), ('Elowen', 7.6, 10.4), ('Elowen', 9.8, 8.6),
    ('Isenmar', 2.6, 4.6), ('Isenmar', 3.0, 6.1), ('Isenmar', 5.6, 3.3), ('Isenmar', 2.3, 2.4), ('Isenmar', 4.0, 5.6),
    ('Isenmar', 3.0, 7.0),
    ('Zenith', 12.4, 3.2), ('Zenith', 14.4, 3.6), ('Zenith', 10.6, 5.1), ('Zenith', 13.6, 4.4), ('Zenith', 15.6, 4.2),
    ('Ossaria', 20.2, 3.0), ('Ossaria', 22.6, 2.4), ('Ossaria', 19.4, 5.2), ('Ossaria', 22.4, 6.4), ('Ossaria', 20.4, 2.0),
    ('Ashkaar', 26.4, 8.2), ('Ashkaar', 26.4, 11.0), ('Ashkaar', 24.4, 12.6), ('Ashkaar', 25.2, 13.8),
    ('Ashkaar', 23.4, 12.4), ('Ashkaar', 26.6, 6.6), ('Ashkaar', 26.2, 3.0), ('Ashkaar', 24.6, 14.6),
    ('Nadir', 15.6, 10.2), ('Nadir', 16.2, 11.6), ('Nadir', 17.6, 9.4), ('Nadir', 12.8, 1.7), ('Nadir', 11.5, 1.6),
    ('Crownhaven', 19.5, 14.45), ('Crownhaven', 18.7, 14.0), ('Crownhaven', 20.2, 15.0),
]

SEAS = [  # label, x, y, angle, size
    ("THE FROZEN NORTH SEA", 13.5, 0.55, 0, 1.0),
    ("Isenmar's Waters", 3.6, 0.85, 0, 0.7),
    ("THE SHATTERED ICE", 27.8, 2.45, -18, 0.62),
    ("THE HALLOW STRAIT", 8.6, 19.62, 0, 0.9),
    ("THE WESTERN DEEP", 0.75, 12.0, 90, 0.85),
    ("THE EMBER SEA", 29.0, 9.5, -90, 0.85),
]
LANDMARKS = [  # label, x, y, size, angle
    ("The Frostfang Mountains", 5.6, 4.15, 0.55, -38),
    ("The Escarpment", 8.25, 4.8, 0.45, -80),
    ("ZENITH PLATEAU", 13.3, 2.85, 0.5, 0),
    ("The Crags", 21.0, 1.9, 0.48, 0),
    ("Jawbone Ridge", 23.05, 4.6, 0.42, -85),
    ("The Cinderhorn", 25.9, 12.3, 0.5, 0),
    ("The Crownwall", 19.5, 12.45, 0.45, 0),
    ("The Wyrmspine", 22.9, 16.75, 0.45, 0),
    ("Gossamer Wood", 12.25, 15.05, 0.5, 0),
    ("The Gloamwood", 17.2, 16.45, 0.5, 0),
    ("The Rimewood", 4.6, 11.25, 0.5, 0),
    ("Lake Sallow", 20.05, 10.25, 0.4, 0),
    ("Mirror Mere", 14.6, 11.1, 0.36, 0),
    ("Lake Rime", 3.6, 3.45, 0.36, 0),
    ("River Ebb", 6.4, 7.75, 0.34, 0),
    ("The Brass Dunes", 16.6, 5.95, 0.4, 0),
    ("Cinderglass Barrens", 25.0, 9.5, 0.38, 0),
    ("The Mast Glacier", 6.75, 0.45, 0.38, 0),
    ("Drowned Aurelia", 13.1, 0.4, 0.4, 0),
    ("The Thornwar Marches", 19.8, 18.0, 0.4, 0),
    ("Mirefen Marsh", 16.0, 10.75, 0.36, 0),
    ("Selvedge", 9.4, 16.15, 0.32, 0),
]
KINGDOM_LABELS = [  # name, subtitle, x, y
    ("ELOWEN", "the Evergreen Crown", 8.6, 16.25),
    ("ISENMAR", "the Frozen Sea", 3.2, 5.6),
    ("ZENITH", "the City Above", 13.6, 3.6),
    ("NADIR", "the City Below", 15.7, 12.5),
    ("OSSARIA", "the Bone Sands", 20.0, 3.2),
    ("ASHKAAR", "the Dragonfire Dominion", 25.8, 13.15),
    ("CROWNHAVEN", "the Accord's Seat", 19.5, 15.75),
]
SEA_LANES = [  # (points, kind, label)
    ([(12.5, 18.6), (12.4, 19.6), (12.0, 20.4)], 'ferry', "the Last Ferry (from beyond the Strait)"),
    ([(3.6, 2.5), (6.0, 1.0), (10.0, 0.6), (16.0, 0.6), (22.0, 0.5), (26.8, 0.6), (28.2, 0.8)], 'sled',
     "the Thane's sled-road over the ice"),
    ([(26.6, 3.4), (27.4, 2.8), (28.2, 1.4)], 'war', "the war crossing"),
    ([(6.4, 18.7), (5.0, 19.4), (3.0, 18.6), (1.6, 14.0), (1.6, 9.5), (3.0, 7.7)], 'ferry', "the coast packet"),
    ([(12.5, 18.6), (15.0, 19.4), (19.4, 19.4)], 'ferry', ""),
]
AIR_LANES = [[(10.5, 3.5), (7.5, 2.5)], [(10.5, 3.5), (12.5, 5.5)], [(10.5, 3.5), (15.0, 9.0), (19.5, 14.45)]]
