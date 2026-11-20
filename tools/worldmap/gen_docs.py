# -*- coding: utf-8 -*-
"""Writes the cartographer's outputs from tools/worldmap/world_data.py:
  design/PLACE_NAMES.md          old -> new for every map ID (drives tools/rename_places.py)
  design/ROUTES.yaml             the route plan, machine-readable (map builder input)
  design/WORLD.md                section 11 (between the ROUTES markers; the rest of the file is untouched)
  pbs/town_map.txt               region 0 Velmora (packaged as PBS/town_map_prismfall.txt)
  mapgen/data/town_map_positions.json   MapPosition for every map (build.py applies it)
and updates design/maps.json (new road maps, route_plan, sizes, segments of the Revision 14 chain, town_map_pos,
borderland route lists) and design/FIELD_DEFAULTS.yaml (entries for the new maps).
Idempotent: run it again after changing world_data.py.   python3 -I tools/worldmap/gen_docs.py
"""
import glob
import json
import os
import re
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import world_data as W  # noqa: E402

MAPS_JSON = os.path.join(ROOT, 'design', 'maps.json')
ACT = {'Ch 1-2': 1, 'Ch 3': 1, 'Ch 4': 1, 'Ch 5': 1, 'Act II': 2, 'Act III': 3, 'Act IV': 4, 'Act V': 5}
KIT = {'MEADOW': 'G5_TEMPERATE', 'BEACH': 'G4_COAST', 'SILKWOOD': 'G4_OLDWOOD', 'SNOWY_MOUNTAIN': 'G4_SNOW_COAST',
       'MOUNTAIN': 'G4_MOUNTAIN', 'NEON_GRID': 'G5_METROPOLIS_OUTSKIRTS', 'DESERT': 'G5_DESERT_CANYON',
       'WASTELAND': 'G5_DESERT_CANYON', 'CORROSIVE_MIRE': 'G4_MARSH', 'ASHEN_WASTE': 'G4_VOLCANIC',
       'SCRAPYARD': 'G5_UNDERCITY', 'VOLCANIC': 'G4_VOLCANIC', 'CAVE': 'G4_CAVE', 'RAINBOW': 'G5_TEMPERATE',
       'FAIRY_TALE': 'G4_OLDWOOD', 'STORMFRONT': 'G5_METROPOLIS_OUTSKIRTS', 'MINDSCAPE': 'G4_DISTORTION',
       'INVERSE': 'G4_DISTORTION', 'FACTORY': 'G5_UNDERCITY', 'WATER_SURFACE': 'G4_COAST', 'NEW_MOON': 'G5_UNDERCITY',
       'DRAGONS_DEN': 'G4_VOLCANIC', 'GRAND_STAGE': 'G45_CASTLE_CITY'}
BGM = {'Elowen': 'Route 2', 'Isenmar': 'Route 3', 'Zenith': 'Route 3', 'Nadir': 'Route 3', 'Ashkaar': 'Route 3',
       'Ossaria': 'Route 3', 'Antumbra': 'Route 3', 'Crownhaven': 'Route 3'}
# Revision 14: badges held when each early map is first reached
SEG_FIX = {}
for i in list(range(140, 160)) + [146, 147]:
    SEG_FIX[i] = 0
for i in list(range(120, 140)) + [524, 526]:
    SEG_FIX[i] = 1
for i in (525, 548, 151, 152, 153, 132, 134):      # after Tamsin's badge (SWAP_GYM1_GYM2.md section 0)
    SEG_FIX[i] = 2
SEG_FIX[810] = 13       # the Dry Tide: Road 14's side road from Duneholt to the front, walked after Badge 13 (story, geo v2)

E = lambda d, to, note='': dict(type='edge', dir=d, to=to, **({'note': note} if note else {}))
WP = lambda at, to, link, note='': dict(type='warp', at=list(at), to=to, link=link, **({'note': note} if note else {}))
# Revision 14 connections (SWAP_GYM1_GYM2.md 1A), declarative: `edges` is the COMPLETE edge list of the map and is
# rebuilt from this table on every run, so the script is idempotent (the old retarget/add form stacked a new
# "570 south -> 577" edge on each run). Every edge pair joins opposite sides, as Essentials requires. A `span` the
# map builder wrote is kept while the edge stays on the same side; `to_span` only while the neighbour is the same.
# Warps/doors are kept, except `drop_links`; `links` adds or updates warps by link name; `notes` annotate by link.
REV14 = {
    520: dict(edges=[E('south', 100), E('north', 521),
                     E('west', 527, 'at the Hale Bell; the quarantine roadblock (Accord guards) moves here from 521 and '
                                    'lifts on S105')]),
    521: dict(edges=[E('south', 520)],
              notes={'R2_WOOD': 'the corded forest road: a "Forest-road cordon" event blocks it from this side always, '
                                'and from 524\'s side until V105 BRIARWICK_GLASSWOOD >= 1'}),
    527: dict(edges=[E('east', 520, 'the Hale Bell exit'), E('west', 528)]),
    528: dict(edges=[E('east', 527), E('west', 140, 'Saltmere East Gate')]),
    140: dict(edges=[E('north', 541, 'North Gate: closed until S108 (Gate Warden event, Chapter 2 close)'),
                     E('west', 560, 'West Gate: the Frostflat Causeway, chained at the Border Stones until the player '
                                    'reaches Frostwick'),
                     E('east', 528, 'East Gate (from Marram Down)')]),
    541: dict(edges=[E('north', 552), E('south', 140, 'North Gate')]),
    552: dict(edges=[E('south', 541), E('north', 540)]),
    540: dict(edges=[E('east', 524, "the Gossamer's west eaves (replaces the Briarwick edge)"),
                     E('south', 552, 'replaces the Grey Saltings edge (the built map already has its 541 edge on the '
                                     'south side, x 2-9)')],
              drop_links=['R3_COCOON']),
    524: dict(edges=[E('west', 540, 'from Thistledown Lea')],
              notes={'R2_WOOD': 'the corded forest road to Windfall Row: opens from this side when V105 >= 1',
                     'WOOD_DEEP': 'behind a CUT tree: HM01 from the Cutter after Tamsin\'s badge (Badge 2)'}),
    525: dict(links=[WP((43, 20), 548, 'DEEP_COCOON', 'through the Veil (Juno and Tamsin wait here): the only way into '
                                                      'Cocoonfall Hollow')]),
    548: dict(drop_links=['R3_COCOON'],
              links=[WP((0, 16), 525, 'DEEP_COCOON', 'back to the Deepwood; the Thistledown Lea warp (R3_COCOON) is gone')]),
    132: dict(links=[WP((22, 2), 134, 'BWG_3', "Granny's door (it led to 133 The Spindle before Revision 14)")]),
    120: dict(edges=[E('north', 566, 'North Gate')]),
    566: dict(edges=[E('south', 120, 'Briarwick North Gate'), E('north', 577)]),
    577: dict(edges=[E('south', 566), E('west', 570, 'Frostwick East Gate')]),
    570: dict(edges=[E('east', 577, 'East Gate (the whale-rib palisade)'), E('north', 578, 'North Gate'),
                     E('south', 560, 'South Gate: the Frostflat Causeway, the side road back to Saltmere')]),
    578: dict(edges=[E('south', 570, 'Frostwick North Gate'), E('north', 562)]),
    562: dict(edges=[E('south', 578), E('north', 561)],
              notes={'RIME_GLADE': 'behind a frosted sapling (Cut: HM01 comes after Badge 2)'}),
    560: dict(edges=[E('east', 140),
                     E('north', 570, "to Frostwick's South Gate: Essentials joins opposite edges, so turn the Causeway's "
                                     "last stretch north (N edge <-> 570 S) or use a warp. The chain at the Border Stones "
                                     "opens from the Frostwick side")]),
}
# maps the builder has built that maps.json did not list (Revision 14 segments must be explicit for them)
EXTRA_MAPS = {
    134: dict(id=134, name="Loomhouse Upper Lofts - Granny's Knot", act=1, kingdom='Elowen', kind='gym', size=[20, 15],
              tileset='Gyms interior', bgm='Gym', field='SILKWOOD', segment=2, puzzle='GYM_PUZZLES.md#134',
              connections=[dict(type='warp', at=[9, 12], to=132, link='BWG_3', note="back to the Canopy Lofts")],
              note='Upper Lofts mastery room (optional, after Tamsin\'s badge); added by the cartographer so its segment '
                   'is explicit (validate_encounters falls back to the pre-swap ID scheme otherwise)',
              tileset_kit='G5_GYM_INTERIOR', border='building walls (interior)'),
    # small maps the war story asks for (story editor, geo v2; story/13_CUTSCENES.md "Requested small maps")
    928: dict(id=928, name="Ashkaar Siege Camp - Command Pavilion", act=4, kingdom='Ossaria (Ashkaar camp)',
              kind='interior', size=[24, 18], tileset='Outside', bgm=None, field='NONE', segment=13, detail='outline',
              war_theatre=True, parent=924,
              connections_outline=["door: the Dominar's war-tent on the Siege Camp (924). Story: Anja's cage "
                                   "(`:war_prisoner`, Ch15-16) and the Dominar's petition (`:ch19_dominar`, after the "
                                   "Battle of the Glass Dunes)"],
              key_features=["the Dominar's command pavilion: red lacquer screens, a map table of the western dunes, the "
                            "oath-brazier (lies are a capital crime here), the Light Stone's empty stand, a prisoner's "
                            "cage at the back"],
              tileset_kit='G45_GRAND_INTERIOR', border='tent walls (interior)'),
    929: dict(id=929, name="The Observers' Mesa", act=5, kingdom='Ossaria', kind='dungeon', size=[36, 28],
              tileset='Outside', bgm=None, field='DESERT', segment=17, detail='outline', war_theatre=True,
              connections_outline=["story-gated: reached in the Ch19 battle (WAR-1 shot 14), from the south edge of the "
                                   "Glass Dunes (926) or the Dry Tide's west end (810)"],
              key_features=["a flat-topped sandstone mesa behind the lines: Meridian's white tents, brass tripods and "
                            "dial-boxes, a field telegraph; the whole battlefield below. Dr. Quent packs up here"],
              tileset_kit='G5_DESERT_CANYON', border='mesa cliffs on every side; one goat-path up'),
    930: dict(id=930, name="The Bone-Carters' Camp", act=4, kingdom='Ossaria', kind='town', size=[44, 32],
              tileset='Outside', bgm=None, field='DESERT', segment=13, detail='outline', war_theatre=True,
              connections_outline=["E: the Dry Tide's west end (810). W: the war maps (the Siege Camp 924, the Glass "
                                   "Dunes 926; story-gated). Sigrun sets the PC down here in Ch19"],
              key_features=["Ossaria's burial guild at the war's edge: the white bone-banner on a pole, burial carts, "
                            "a tally-wall of names, an embalmers' tent; the elder's quest (bring out the dead the carts "
                            "can't reach)"],
              tileset_kit='G5_DESERT_CANYON', border='dunes and the Dry Tide\'s shell pavements'),
}
RETIRED = {133: 'GYM_PUZZLES.md: retired in Revision 14 (Tamsin battles on 131\'s top ledge); not built'}


def apply_rev14(by):
    for mid, r in REV14.items():
        m = by.get(mid)
        if m is None:
            continue
        cs = list(m.get('connections') or [])
        old_edges = [c for c in cs if c.get('type') == 'edge']
        others = [dict(c) for c in cs if c.get('type') != 'edge' and c.get('link') not in (r.get('drop_links') or [])]
        if 'edges' in r:
            edges = []
            for e in r['edges']:
                ne = dict(type='edge', dir=e['dir'], to=e['to'])
                side = next((c for c in old_edges if c.get('dir') == e['dir']), None)
                if side and 'span' in side:
                    ne['span'] = side['span']
                if side and side.get('to') == e['to'] and 'to_span' in side:
                    ne['to_span'] = side['to_span']
                if e.get('note'):
                    ne['note'] = e['note']
                edges.append(ne)
        else:
            edges = [dict(c) for c in old_edges]
        for w in r.get('links') or []:
            ex = next((c for c in others if c.get('link') == w['link']), None)
            if ex is None:
                others.append(dict(w))
            else:
                ex.update(w)
        for link, note in (r.get('notes') or {}).items():
            for c in others:
                if c.get('link') == link:
                    c['note'] = note
        m['connections'] = edges + others
        m['rev14_connections'] = 'SWAP_GYM1_GYM2.md 1A; spans of new/moved edges: map builder'


def check_edge_pairs(by):
    """every edge in the early chain must be answered by the neighbour's opposite edge"""
    opp = {'north': 'south', 'south': 'north', 'east': 'west', 'west': 'east'}
    bad = []
    for mid in REV14:
        for c in (by.get(mid) or {}).get('connections') or []:
            if c.get('type') != 'edge':
                continue
            n = by.get(c['to'])
            if n is None:
                continue
            if not any(x.get('type') == 'edge' and x.get('to') == mid and x.get('dir') == opp[c['dir']]
                       for x in n.get('connections') or []):
                bad.append('%d %s -> %d' % (mid, c['dir'], c['to']))
    return bad


# ----------------------------------------------------------------------------- Geography v2 (Revision 18)
WAR_TEXT = {
    920: dict(kingdom='Ossaria (Isenmar lines)', field='DESERT', tileset_kit='G5_DESERT_CANYON',
              key_features=["Isenmar's front in the western dunes: sand its host has frozen into white trench-lines, "
                            "rime-crusted dune crests, burnt sled-forts dragged overland"],
              border='frozen dunes and ice-glazed sandstone; the Steamline to the east'),
    921: dict(key_features=["Isenmar's border fortress on Ossaria's western edge, besieged from the east: ice-and-granite "
                            "curtain wall over the dunes, breached gatehouse, dragonfire scorch"],
              border='frozen dunes, the Mast Glacier snout and granite outcrops', tileset_kit='G4_SNOW_FORTRESS',
              visual_brief={'landmarks': ['breached gatehouse', "rime-glazed granite walls on the sand's edge",
                                          'sled-yards', 'Rime Keep over a frozen spring'],
                            'silhouette': "squat rime-white fortress at the Mast Glacier's foot, the dunes running east "
                                          "from its walls, smoke and dragon shapes over them",
                            'materials': 'granite, packed ice, whalebone, scorched timber, drifted sand',
                            'palette': 'Rejuvenation winter against the desert: steel blue, rime white, sand ochre, '
                                       'fire orange',
                            'set_pieces': ['dragonfire run along the wall', 'sortie onto the Rimed Sands',
                                           'hospital in the great hall']}),
    922: dict(key_features=["Skaldfast's inner keep, built over a frozen spring; the war council's hall"],
              border='fortress walls', tileset_kit='G4_SNOW_FORTRESS'),
    924: dict(kingdom='Ossaria (Ashkaar camp)', tileset_kit='G5_DESERT_CANYON',
              key_features=["legion tents, dragon pickets and trebuchets on the eastern dunes; the Dominar's war-tent"],
              border='dunes, sandstone mesas and the Ashkaar war road'),
    925: dict(kingdom='Ossaria (contested)', field='ASHEN_WASTE', tileset_kit='G5_DESERT_CANYON',
              key_features=["no-man's-land where the two Imprints meet: ice on one side, fire on the other, a permanent "
                            "steam wall and sand fused to glass between the fronts"],
              border='steam walls, glassed dunes'),
    926: dict(kingdom='Ossaria (contested)', field='DESERT', tileset_kit='G5_DESERT_CANYON',
              key_features=["the war's battlefield in the dunes: in the climax Primal Kyogre drags a flood-sea into the "
                            "desert and Reshiram's fire turns the dunes to glass (field transition: the fields team)"],
              border='dune ridges; glass after the climax',
              visual_brief={'landmarks': ['bone-white dunes across the caravan road', "the bone-carters' white banner "
                                          "on a crest", 'wrecked sled-forts and siege engines', 'two war banners'],
                            'silhouette': 'rolling white dunes between two hosts under a steam sky; after the climax a '
                                          'glass plain with glassed soldiers standing in it',
                            'materials': 'sand, flood-water, steam-glass',
                            'palette': 'bone white and sand ochre; flood grey-blue; glass cyan and magma orange at the '
                                       'clash',
                            'set_pieces': ["Kyogre's flood-sea pouring in over the sand", 'glass where the fire passes',
                                           "afterwards: a glass plain of standing glassed soldiers and the "
                                           "bone-carters' banner"]}),
}
WAR_WHEN = 'Ashkaar-Isenmar war active (story key)'
WAR_STATES = {
    160: "the Thane requisitions the Ebb Guild's sleds for the front and the Guild refuses; Thaw refugees; Ashkaar "
         "envoys expelled",
    300: "war footing: levies drilling, refugees from Skaldfast, sleds requisitioned for the front",
    460: "the legions gone to the war in Ossaria; Sigrun's riders hold the gate",
    660: "supply and conscript columns north to the Cinderglass Barrens",
    200: "Kassan's neutrality notices (the Elector's Lease) on the Sandgate; caravans leaving by the east gate; foreign "
         "quartermasters, Isenmar's and Ashkaar's, in the Hall of Audience (206); bone-carters loading at the west gate",
    360: "refugees from both kingdoms in Bastian's seams, Ossarian well-folk among them",
    670: "furnace apprentices taken by the levy; the glass market shut",
    662: "legion columns marching west across the barrens to the Siege Camp",
    730: "sled-convoys over the Mast Glacier by night; dragon patrols overhead",
    810: "the bone-carters' carts and white banner on the road west; their camp (930) at the west end",
}
WAR_OUTLINE = ("Revision 18: the war is fought on land, in Ossaria's western dunes (fire and ice share no border). "
               "Isenmar side: " + W.WAR['isenmar'] + ". Ashkaar side: " + W.WAR['ashkaar'] + ". Front: " +
               W.WAR['front'] + ".") if getattr(W, 'WAR', None) else ''


def crossings_of(code):
    """gym legs that cross a borderland, from the road table"""
    out = []
    members = set(W.BORDERLANDS[code][3]) | {W.BORDERLANDS[code][2]}
    for r in W.ROADS:
        hit = [l['name'] for l in r['legs'] if l['id'] in members]
        via = [W.leg_by_id()[i][1]['name'] for i in getattr(W, 'VIA', {}).get(r['n'], []) if i in members]
        if hit or via:
            out.append('%d->%d (%s: %s)' % (r['n'] - 1, r['n'], r['name'], ', '.join(hit + via)))
    return out


def apply_geography_v2(d, by):
    if not getattr(W, 'BORDERLANDS', None):
        return
    old = {b['code']: b for b in d.get('borderlands', [])}
    recs = []
    member_of = {}
    for code, (name, ks, town, routes, biome, wild) in W.BORDERLANDS.items():
        rec = dict(old.get(code) or {})
        rec.update(code=code, kingdoms=list(ks), name=name, crossings=crossings_of(code), biome=biome, wild=wild,
                   routes=list(routes), town=town)
        rec.setdefault('landmarks', [])
        rec.setdefault('field', '')
        recs.append(rec)
        for i in list(routes) + [town, town + 1] + ([850] if code == 'F' else []):
            if i in by and (i == town or i in routes or by[i].get('kind') == 'interior' or i == 850):
                member_of[i] = (name, ks)
    d['borderlands'] = recs
    for m in d['maps']:
        if m['id'] in member_of:
            name, ks = member_of[m['id']]
            m['borderland'] = name
            m['kingdom'] = 'Borderland (%s/%s)' % ks
        elif m.get('borderland'):
            m.pop('borderland')
    legs = W.leg_by_id()
    for i, (r, l) in legs.items():
        if i in by and i not in member_of:
            by[i]['kingdom'] = kingdom_field(l['kingdom'])
    for i, (n, x, y, rank, k) in W.SETTLEMENTS.items():
        if i in by and i not in member_of and '/' not in k:
            by[i]['kingdom'] = k
    for i, (oldn, new, origin) in getattr(W, 'REPLACED', {}).items():
        if i in by:
            by[i]['name'] = new
    for i in getattr(W, 'WAR', {}).get('theatre', []):
        m = by.get(i)
        if not m:
            continue
        m['connections_outline'] = [WAR_OUTLINE]
        for k, v in WAR_TEXT.get(i, {}).items():
            m[k] = v
        m['geography_v2'] = 'Revision 18: the war moved onto land in Ossaria (design/GEOGRAPHY_V2_STORY_FIXES.md)'
    for i, change in WAR_STATES.items():
        m = by.get(i)
        if not m:
            continue
        st = m.get('states') or [{'id': 'default'}]
        if not any(x.get('id') == 'default' for x in st):
            st.insert(0, {'id': 'default'})
        war = [x for x in st if x.get('id') == 'war']
        if war:
            war[0]['change'] = change
            war[0].setdefault('when', WAR_WHEN)
        else:
            st.append({'id': 'war', 'when': WAR_WHEN, 'change': change})
        m['states'] = st
    # Static Tunnels: the Mainline's buried tunnels under the Brass Dunes (side of 600)
    for i in (604, 605):
        if i in by:
            by[i]['kingdom'] = 'Borderland (Elowen/Ossaria)'
    notes = d.setdefault('notes', [])
    tag = 'GEOGRAPHY v2 (cartographer, Revision 18)'
    if not any(n.startswith(tag) for n in notes):
        notes.append(tag + ': Ossaria north, Isenmar west, Ashkaar east, Zenith (Nadir beneath it) south, Elowen in the '
                     'middle touching every kingdom, Crownhaven at its heart. Kingdom fields, borderland records and '
                     'members come from tools/worldmap/world_data.py BORDERLANDS; the war theatre (920-927) is on land in '
                     'Ossaria. New Elowen transit maps: 594 Wallshadow Row, 595 Coppice Ride, 602 Candle Down, 603 the '
                     'Highwold, 634 Wormwood Lea, 756 Kingsmead (the Crown Road and its spokes).')


def kingdom_field(k):
    return 'Borderland (%s)' % k if '/' in k else k


def load_maps():
    return json.load(open(MAPS_JSON, encoding='utf-8'))


def leg_road_segment(r, l):
    if l.get('seg') is not None:          # the Crown Road and other transit legs: first reached on an earlier road
        return l['seg']
    if l['role'] == 'branch':
        return r['n'] - 1
    if l['id'] in (662, 673):
        return 7
    return r['n'] - 1


# ----------------------------------------------------------------------------- names
def name_table(maps):
    """id -> dict(old, new, status, kingdom, origin)"""
    by_id = {m['id']: m for m in maps}
    out = {}
    for m in maps:
        cur = m['name']
        out[m['id']] = dict(old=cur, new=cur, status='kept', kingdom=m['kingdom'], origin='')
    for r, l in W.all_legs():
        k = kingdom_field(l['kingdom'])
        if l['id'] in out and (l['old'] or not by_id[l['id']].get('added_by')):
            e = out[l['id']]
            old = l['old'] or e['old']
            e.update(old=old, new=l['name'], kingdom=k, origin=l['origin'],
                     status='renamed' if old != l['name'] else 'kept')
        else:
            out[l['id']] = dict(old='', new=l['name'], status='new', kingdom=k, origin=l['origin'])
    for i, (old, new, origin) in W.OTHER_RENAMES.items():
        e = out[i]
        e.update(old=old, new=new, origin=origin, status='renamed')
    for i, (old, new, origin) in getattr(W, 'REPLACED', {}).items():
        if i in out:          # Geography v2: a new place on an old ID; never auto-renamed in prose
            out[i].update(old=old, new=new, origin=origin, status='replaced' if old != new else 'kept')
    for i, why in RETIRED.items():
        if i in out:          # in the plan but never built (GYM_PUZZLES)
            out[i].update(status='retired (unbuilt)')
    for i, o in W.SETTLEMENT_ORIGINS.items():
        if i in out and not out[i]['origin']:
            out[i]['origin'] = o
    return out


# ----------------------------------------------------------------------------- squares
def build_squares(maps):
    sq = {}
    legs = W.leg_by_id()
    for i, (n, x, y, r, k) in W.SETTLEMENTS.items():
        sq[i] = (x, y)
        for j in W.TOWN_EXTRA_IDS.get(i, []):
            sq[j] = (x, y)
    for r, l in W.all_legs():
        sq[l['id']] = l['cells'][0]
        for j in l['side']:
            sq.setdefault(j, l['cells'][0])
    for i, c in W.OWN_SQUARE.items():
        sq[i] = c
    for i, v in W.OWN_SQUARE_INHERIT.items():
        sq[i] = v if isinstance(v, tuple) else W.OWN_SQUARE.get(v, sq.get(v))
    parents = {}
    mi = os.path.join(ROOT, 'maps_out', 'mapinfos_prismfall.txt')
    if os.path.exists(mi):
        for line in open(mi, encoding='utf-8'):
            if line.startswith('#') or not line.strip():
                continue
            a = line.rstrip('\n').split('\t')
            parents[int(a[0])] = int(a[1])
    ids = sorted(m['id'] for m in maps)
    towns = sorted(W.SETTLEMENTS)
    for i in ids:
        if i in sq:
            continue
        p = parents.get(i)
        while p and p not in sq and p in parents:
            p = parents[p]
        if p and p in sq:
            sq[i] = sq[p]
            continue
        cand = [t for t in towns if t <= i < t + 20 and (t < 520 or i - t < 10 or t in (570,))]
        if cand:
            sq[i] = sq[max(cand)]
            continue
        lower = [j for j in ids if j < i and j in sq and j // 20 == i // 20]
        if lower:
            sq[i] = sq[max(lower)]
    return sq


def via_text(r):
    legs = W.leg_by_id()
    return ', '.join('%s (%d)' % (legs[i][1]['name'], i) for i in getattr(W, 'VIA', {}).get(r['n'], []))


# ----------------------------------------------------------------------------- PLACE_NAMES.md
def write_place_names(maps, names, sq):
    L = ['# PLACE_NAMES - every map of Velmora, old name -> new name',
         '',
         '> Owner: world cartographer. **Source of truth:** `tools/worldmap/world_data.py` (regenerate this file with',
         '> `python3 -I tools/worldmap/gen_docs.py`). `tools/rename_places.py` reads the table below and renames every',
         '> reference in the project (dry run by default). SPINE Revisions 13 and 14. Map IDs never change: Saltmere stays',
         '> 140 and Briarwick 120 after the Gym 1/2 swap; `segment` in maps.json carries the badge count.',
         '',
         '## Naming voices',
         '',
         'No place is called "Route N". Roads are named the way Westeros names them (the Kingsroad, the Neck, Blackwater',
         'Rush): from geography, history, lords, trades and legends, in each kingdom\'s own voice. A road between two towns',
         'has one road name (the Strand Road, the Hoar Road) and every map along it has its own name.',
         '']
    for k, v in W.VOICES.items():
        L.append('- **%s.** %s Examples: %s.' % (k, v['voice'], ', '.join(v['examples'])))
    L += ['- **Borderlands** blend both voices (Frostwick Pass: an Elowen word for an Isenmar pass; the Icecutters\' Haul: '
          'Isenmar work on an Elowen river).', '',
          '**Geography v2** (user, 2026-11-19; SPINE Revision 18): Ossaria north, Isenmar west, Ashkaar east, Zenith (Nadir '
          'beneath it) south, Elowen in the middle touching every kingdom, Crownhaven at its heart. Every journey between '
          'kingdoms that do not border runs through Elowen, most of them round **the Crown Road** (Wallshadow Row, Candle '
          'Down, the Highwold, Kingsmead). "via" lists legs a road walks that an earlier road introduced.', '',
          '## The Eighteen Roads (plus the Pilgrim Road)', '',
          '| Road | Name | From -> to | Maps in order |', '|---|---|---|---|']
    for r in W.ROADS:
        frm = W.SETTLEMENTS[r['frm']][0]
        to = W.SETTLEMENTS[r['to']][0]
        legs = ', '.join('%s (%d)%s' % (l['name'], l['id'], '' if l['role'] == 'main' else ' [%s]' % l['role'])
                         for l in r['legs'])
        via = via_text(r)
        L.append('| %d | %s | %s -> %s | %s%s |' % (r['n'], r['name'], frm, to, legs, ('; via ' + via) if via else ''))
    L += ['', '## Every map', '',
          '`Status`: renamed / new / kept / replaced. `Square` = town-map square (x, y) on region 0 (Velmora). The rename',
          'script uses `renamed` rows only; `replaced` rows are places re-conceived by Geography v2 / Revision 18 (the war',
          'moved onto land), whose story lines are rewritten by hand (design/GEOGRAPHY_V2_STORY_FIXES.md).', '',
          '| ID | Old name | New name | Status | Kingdom | Square | Origin |', '|---|---|---|---|---|---|---|']
    for i in sorted(names):
        e = names[i]
        s = sq.get(i)
        L.append('| %d | %s | %s | %s | %s | %s | %s |' % (
            i, e['old'] or '-', e['new'], e['status'], e['kingdom'], '%d, %d' % s if s else '-', e['origin'] or ''))
    L += ['', '## Prose forms', '', 'Besides the map names above, the rename script also rewrites these phrases:', '',
          '| Old | New |', '|---|---|']
    for a, b in W.PROSE_ALIASES:
        L.append('| %s | %s |' % (a, b))
    open(os.path.join(ROOT, 'design', 'PLACE_NAMES.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')


# ----------------------------------------------------------------------------- ROUTES.yaml
def fields_by_map():
    fd = yaml.safe_load(open(os.path.join(ROOT, 'design', 'FIELD_DEFAULTS.yaml'), encoding='utf-8'))
    return {int(k): v for k, v in (fd.get('maps') or {}).items()}


def sizewas(l, m):
    if l['was']:
        return list(l['was'])
    if m is None or m.get('added_by'):
        return None
    return m.get('size_was') or m['size']


def write_routes_yaml(maps, sq):
    fdm = fields_by_map()
    mj = {m['id']: m for m in maps}
    doc = {'schema': 'prismfall-routes/1',
           'notes': ['Owner: world cartographer. Generated by tools/worldmap/gen_docs.py from tools/worldmap/world_data.py.',
                     'One road joins two gym towns; each road is two or more maps (legs), each with its own name, landmark, '
                     'field, wild flavour, fill list and at least one secret.',
                     'size = target map size in tiles [w, h]; size_was = the current built/planned size. The map builder '
                     'grows built maps toward the target when it next rebuilds them.',
                     'fill = what occupies the space (density list): build every item, then decorate between them.',
                     'role: main (on the road), branch (dead-end side road off it), side (an alternative road).',
                     'segment = badges held on arrival (drives level caps). Revision 14 order: Saltmere is Gym 1, Briarwick Gym 2.',
                     'town_map: squares on the Velmora town map (region 0); first square = MapPosition.',
                     'paths: the order of stops as drawn on the maps (style road / side / under / sea / inset; ints are map ids, '
                     'P:<id> a dungeon square, G:<letter> an Antumbra gate, pts:<name> a polyline in world_geo.py).',
                     'connections for the Revision 14 early chain are in design/maps.json (rev14_connections).',
                     'Geography v2 (Revision 18): Ossaria north, Isenmar west, Ashkaar east, Zenith/Nadir south, Elowen in '
                     'the middle. via = legs of an earlier road this road walks (mostly the Crown Road round the '
                     'Crownwall: crown_road). air = an airship lane (the Mast Road only).'],
           'crown_road': getattr(W, 'CROWN_ROAD', []),
           'roads': []}
    for r in W.ROADS:
        R = {'n': r['n'], 'name': r['name'], 'from': r['frm'], 'from_name': W.SETTLEMENTS[r['frm']][0], 'to': r['to'],
             'to_name': W.SETTLEMENTS[r['to']][0], 'chapter': r['chapter'], 'detail': r['detail'], 'note': r['note'],
             'paths': [{'style': st, 'stops': stops} for st, stops in W.ROAD_PATHS[r['n']]],
             'via': getattr(W, 'VIA', {}).get(r['n'], []), 'legs': []}
        for l in r['legs']:
            fld = (fdm.get(l['id']) or {}).get('field') or l['field']
            leg = {'id': l['id'], 'name': l['name'], 'old_name': l['old'], 'origin': l['origin'],
                   'kingdom': kingdom_field(l['kingdom']), 'role': l['role'], 'mode': l['mode'],
                   'segment': leg_road_segment(r, l), 'field': fld, 'size': list(l['size']),
                   'size_was': sizewas(l, mj.get(l['id'])),
                   'built': bool(l['id'] in built_ids()), 'town_map': [list(c) for c in l['cells']],
                   'landmark': l['landmark'], 'wild': l['wild'], 'exits': l['exits'], 'fill': l['fill'],
                   'secret': l['secret'], 'side_maps': l['side']}
            R['legs'].append(leg)
        doc['roads'].append(R)
    with open(os.path.join(ROOT, 'design', 'ROUTES.yaml'), 'w', encoding='utf-8') as f:
        f.write('# ROUTES.yaml - the roads of Velmora (SPINE Revisions 13-14). GENERATED by tools/worldmap/gen_docs.py; edit\n'
                '# tools/worldmap/world_data.py instead. Human version: design/WORLD.md section 11.\n')
        yaml.safe_dump(doc, f, sort_keys=False, allow_unicode=True, width=118)


_BUILT = None


def built_ids():
    global _BUILT
    if _BUILT is None:
        try:
            _BUILT = set(json.load(open(os.path.join(ROOT, 'maps_out', 'manifest.json')))['built'])
        except Exception:
            _BUILT = set()
    return _BUILT


# ----------------------------------------------------------------------------- maps.json
def update_maps_json(sq):
    d = load_maps()
    maps = d['maps']
    by = {m['id']: m for m in maps}
    for r in W.ROADS:
        for l in r['legs']:
            plan = {'road': r['n'], 'road_name': r['name'], 'role': l['role'], 'landmark': l['landmark'],
                    'origin': l['origin'], 'wild': l['wild'], 'exits': l['exits'], 'fill': l['fill'],
                    'secret': l['secret'], 'town_map': [list(c) for c in l['cells']]}
            if l['id'] in by:
                m = by[l['id']]
                if 'size_was' not in m and list(m['size']) != list(l['size']):
                    m['size_was'] = list(m['size'])
                m['size'] = list(l['size'])
                m['route_plan'] = plan
                if m.get('detail') == 'outline' and r['detail'] in ('full', 'medium'):
                    m['detail'] = 'planned'
            else:
                k = l['kingdom']
                m = {'id': l['id'], 'name': l['name'], 'act': ACT.get(r['chapter'], 1), 'kingdom': kingdom_field(k),
                     'kind': 'route', 'size': list(l['size']), 'tileset': 'Outside', 'bgm': BGM.get(k.split('/')[0], 'Route 3'),
                     'field': l['field'], 'segment': leg_road_segment(r, l),
                     'detail': 'planned' if r['detail'] in ('full', 'medium') else 'outline',
                     'connections_outline': [l['exits'] or 'see design/ROUTES.yaml'],
                     'key_features': [l['landmark']] + l['fill'][:3],
                     'tileset_kit': KIT.get(l['field'], 'G5_TEMPERATE'), 'added_by': 'cartographer (SPINE Rev 13)',
                     'border': 'from the landform of this stretch (see route_plan.fill); no tree-row walls',
                     'route_plan': plan}
                maps.append(m)
                by[m['id']] = m
    for i, e in EXTRA_MAPS.items():
        if i not in by:
            m = json.loads(json.dumps(e))
            maps.append(m)
            by[i] = m
    for i, why in RETIRED.items():
        if i in by:
            by[i]['retired'] = why
    for i, s in SEG_FIX.items():
        if i in by:
            by[i]['segment'] = s
    apply_rev14(by)
    for m in maps:                      # safety net: never keep two identical connections
        seen, keep = set(), []
        for c in m.get('connections') or []:
            k = json.dumps(c, sort_keys=True)
            if k not in seen:
                seen.add(k)
                keep.append(c)
        if 'connections' in m:
            m['connections'] = keep
    bad = check_edge_pairs(by)
    if bad:
        print('WARNING: early-chain edges without an opposite edge on the neighbour: ' + ', '.join(bad))
    for m in maps:
        s = sq.get(m['id'])
        if s:
            m.setdefault('metadata', {})['town_map_pos'] = [0, s[0], s[1]]
    apply_geography_v2(d, by)
    maps.sort(key=lambda m: m['id'])
    notes = d.setdefault('notes', [])
    tag = 'REV13/14 (cartographer): every road is named (design/PLACE_NAMES.md) and planned as several large maps'
    if not any(n.startswith('REV13/14') for n in notes):
        notes.append(tag + ' (design/ROUTES.yaml, WORLD.md section 11). `size` is the target; `size_was` the old size. '
                     '`route_plan` holds the landmark, fill list, exits and secret. Saltmere (140) is Gym 1 and Briarwick '
                     '(120) Gym 2: their maps keep their IDs, `segment` is authoritative. metadata.town_map_pos is set for '
                     'every map (pbs/town_map.txt, mapgen/data/town_map_positions.json).')
    with open(MAPS_JSON, 'w', encoding='utf-8') as f:
        json.dump(d, f, indent=1, ensure_ascii=True)
        f.write('\n')
    return d


# ----------------------------------------------------------------------------- FIELD_DEFAULTS.yaml
def update_field_defaults():
    p = os.path.join(ROOT, 'design', 'FIELD_DEFAULTS.yaml')
    text = open(p, encoding='utf-8').read()
    lines = text.split('\n')
    start = lines.index('maps:')
    existing = set()
    for ln in lines[start + 1:]:
        m = re.match(r'^  (\d+): ', ln)
        if m:
            existing.add(int(m.group(1)))
    # keep existing entries in step with maps.json: names always (renames such as the Rev 18 war sites), and the
    # field of entries whose source is the world spec
    maps = {int(m['id']): m for m in load_maps()['maps']}
    synced = 0
    for i in range(start + 1, len(lines)):
        m = re.match(r'^  (\d+): \{name: "((?:[^"\\]|\\.)*)"', lines[i])
        if not m or int(m.group(1)) not in maps:
            continue
        mp = maps[int(m.group(1))]
        ln = lines[i]
        if mp.get('name') and mp['name'] != m.group(2).replace('\\"', '"'):
            ln = ln[:m.start(2)] + mp['name'].replace('"', "'") + ln[m.end(2):]
        if 'source: spec,' in ln and mp.get('field'):
            ln = re.sub(r'(field: )[A-Z_]+', lambda q: q.group(1) + mp['field'], ln, count=1)
        if ln != lines[i]:
            lines[i] = ln
            synced += 1
    new = {}
    for r, l in W.all_legs():
        if l['id'] in existing:
            continue
        new[l['id']] = '  %d: {name: "%s", kind: route, field: %s, battles: [trainer], encounters: [Land], source: hand, ' \
                       'why: "ROUTES.yaml: %s"}' % (l['id'], l['name'].replace('"', "'"), l['field'],
                                                   l['landmark'].replace('"', "'")[:110])
    for i, e in EXTRA_MAPS.items():
        if i in existing or i not in maps or not e.get('war_theatre'):
            continue
        battles = '' if e['kind'] == 'interior' else ', battles: [trainer]'
        new[i] = '  %d: {name: "%s", kind: %s, field: %s%s, source: spec, why: "world spec"}' % (
            i, e['name'].replace('"', "'"), e['kind'], e.get('field') or 'NONE', battles)
    if not new:
        if synced:
            open(p, 'w', encoding='utf-8').write('\n'.join(lines))
        return 0
    out = lines[:start + 1]
    body = lines[start + 1:]
    i = 0
    pending = sorted(new)
    while i < len(body):
        m = re.match(r'^  (\d+): ', body[i])
        while pending and m and pending[0] < int(m.group(1)):
            out.append(new[pending.pop(0)])
        if pending and not m and body[i].strip() and not body[i].startswith('  '):
            while pending:
                out.append(new[pending.pop(0)])
        out.append(body[i])
        i += 1
    while pending:
        out.append(new[pending.pop(0)])
    open(p, 'w', encoding='utf-8').write('\n'.join(out))
    return len(new)


# ----------------------------------------------------------------------------- town map PBS + positions
def heal_spots():
    spots = {}
    for f in glob.glob(os.path.join(ROOT, 'mapgen', 'specs', '*.yaml')):
        t = open(f, encoding='utf-8').read()
        for m in re.finditer(r'HealingSpot:\s*\[(\d+),\s*(\d+),\s*(\d+)\]', t):
            spots[int(m.group(1))] = (int(m.group(2)), int(m.group(3)))
    return spots


def write_town_map(names, sq, maps):
    legs = W.leg_by_id()
    pts = {}   # square -> [name, [pois], fly]

    def add(c, name, poi=None):
        e = pts.setdefault(tuple(c), [name, [], None])
        if poi and poi != e[0] and poi not in e[1]:
            e[1].append(poi)
    for i, (n, x, y, r, k) in W.SETTLEMENTS.items():
        add((x, y), n)
    for r, l in W.all_legs():
        for c in l['cells']:
            add(c, l['name'])
    for i, c in sorted(W.OWN_SQUARE.items()):
        nm = names[i]['new'] if i in names else str(i)
        nm = re.sub(r'\s+(1F|2F|B1F|- .*)$', '', nm)
        add(c, nm, nm)
    for r, l in W.all_legs():
        for j in l['side']:
            if j in names and j not in W.OWN_SQUARE:
                nm = re.sub(r'\s+(1F|2F|B1F|- .*)$', '', names[j]['new'])
                add(l['cells'][0], l['name'], nm)
    for c, nm in W.EXTRA_POINTS.items():
        add(c, nm, nm)
    for g, (real, inset, nm) in W.GATES.items():
        add(inset, 'Antumbra Gate %s' % g, nm)
    spots = heal_spots()
    for i, (n, x, y, r, k) in W.SETTLEMENTS.items():
        if i in spots:
            pts[(x, y)][2] = (i, spots[i][0], spots[i][1])
    L = ['# Velmora, region 0 (SPINE Rev 2 note: must be region 0). GENERATED by tools/worldmap/gen_docs.py from',
         '# tools/worldmap/world_data.py - edit that and re-run. Packaged as PBS/town_map_prismfall.txt; the Prismfall Maps',
         '# plugin (009_TownMap.rb) compiles it instead of the stock town_map.txt, whose region 0 (Essen) it replaces.',
         '# Graphic: Graphics/UI/Town Map/prismfall_velmora.png (480x320, 30x20 squares of 16 px), drawn by',
         '# tools/worldmap/gen_world_map.py. Point = x,y,name,point of interest,fly map,fly x,fly y',
         '# Fly spots exist only for built towns (their PC HealingSpot); add one when a town is built.',
         '#-------------------------------',
         '[0]',
         'Name = Velmora',
         'Filename = prismfall_velmora.png']
    for (x, y) in sorted(pts, key=lambda c: (c[1], c[0])):
        name, pois, fly = pts[(x, y)]
        poi = ' & '.join(pois[:2])
        f = ',%d,%d,%d' % fly if fly else ''
        if fly:
            L.append('Point = %d,%d,%s,%s%s' % (x, y, name.replace(',', ''), poi.replace(',', ''), f))
        elif poi:
            L.append('Point = %d,%d,%s,%s' % (x, y, name.replace(',', ''), poi.replace(',', '')))
        else:
            L.append('Point = %d,%d,%s' % (x, y, name.replace(',', '')))
    open(os.path.join(ROOT, 'pbs', 'town_map.txt'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    pos = {str(i): [0, c[0], c[1]] for i, c in sorted(sq.items())}
    os.makedirs(os.path.join(ROOT, 'mapgen', 'data'), exist_ok=True)
    json.dump({'_note': 'GENERATED by tools/worldmap/gen_docs.py: MapPosition per map id (region 0 Velmora). '
                        'build.py applies these over spec metadata.', 'positions': pos},
              open(os.path.join(ROOT, 'mapgen', 'data', 'town_map_positions.json'), 'w'), indent=0)
    return len(pts)


# ----------------------------------------------------------------------------- WORLD.md section 11
BEGIN = '<!-- ROUTES:BEGIN (generated by tools/worldmap/gen_docs.py) -->'
END = '<!-- ROUTES:END -->'


def world_section(sq):
    L = [BEGIN, '## 11. The Eighteen Roads (SPINE Revisions 13-14)', '',
         'No place is called "Route N" any more. Each **road** joins two gym towns and has a name; each road is **two or '
         'more large maps** (legs), each with its own name, landmark, wild flavour, field and at least one secret or side '
         'path. Machine-readable plan: **`design/ROUTES.yaml`** (the map builder\'s input). Every map\'s old and new name: '
         '**`design/PLACE_NAMES.md`**. Geography and the region map: **`design/WORLD_MAP.md`**, '
         '`art/previews/world_map.png`. Source of all three: `tools/worldmap/world_data.py`.', '',
         '**Size means density.** Early legs grow to 64-140 tiles on their long side (2-4x the old maps). Size is never '
         'empty: every leg lists what fills it (`fill`), roughly one feature per 400 tiles, plus 4-6 trainers, a heal point '
         'on long legs, a Road Stone (the collectible milestone, one per road), shortcuts that open from the far end, '
         'and grass in separate patches with sight lines broken by the landform. Rule of thumb for the builder: no '
         'straight empty corridor longer than 12 tiles, and every dead end pays (item, view, NPC or secret).', '',
         '**Revision 14 chain.** Ferrow\'s Landing -> the Strand Road (coast) -> **Saltmere, Gym 1** -> the Weavers\' Road '
         '(inland, up the Selvedge) -> Gossamer Wood -> **Briarwick, Gym 2** -> the Hoar Road (north over the fells into '
         'the Rimewood) -> Frostwick -> **Ebbmouth, Gym 3**. Map IDs do not change; `segment` in maps.json does.', '',
         '| Road | Name | From -> to | Legs (target size, tiles) | Chapter |', '|---|---|---|---|---|']
    for r in W.ROADS:
        legs = ' -> '.join('%s %d %dx%d%s' % (l['name'], l['id'], l['size'][0], l['size'][1],
                                             '' if l['role'] == 'main' else ' (%s)' % l['role']) for l in r['legs'])
        L.append('| %d | **%s** | %s -> %s | %s | %s |' % (r['n'], r['name'], W.SETTLEMENTS[r['frm']][0],
                                                          W.SETTLEMENTS[r['to']][0], legs, r['chapter']))
    L += ['']
    for r in W.ROADS:
        if r['detail'] not in ('full', 'medium'):
            continue
        L += ['### Road %d: %s (%s -> %s, %s)' % (r['n'], r['name'], W.SETTLEMENTS[r['frm']][0],
                                                   W.SETTLEMENTS[r['to']][0], r['chapter']), '', r['note'], '']
        for l in r['legs']:
            was = ('was %dx%d' % tuple(l['was'])) if l['was'] else 'new map'
            L.append('**%s (%d)**, %s, `:%s`, target **%dx%d** (%s). %s' % (
                l['name'], l['id'], kingdom_field(l['kingdom']), l['field'], l['size'][0], l['size'][1], was,
                '' if l['role'] == 'main' else '*%s road.* ' % l['role'].capitalize()))
            L.append('*Name:* %s' % l['origin'])
            L.append('- **Landmark:** %s' % l['landmark'])
            L.append('- **Exits:** %s' % (l['exits'] or '-'))
            L.append('- **Wild:** %s' % l['wild'])
            if r['detail'] == 'full':
                L.append('- **Fill:** ' + '; '.join(l['fill']) + '.')
            else:
                L.append('- **Fill:** ' + '; '.join(l['fill']) + '.')
            L.append('- **Secret:** %s' % l['secret'])
            L.append('')
    L += ['### Roads 5-19 (outline)', '', 'Each leg: name, target size, landmark, secret. Fill lists follow when the act is '
          'detailed.', '']
    for r in W.ROADS:
        if r['detail'] in ('full', 'medium'):
            continue
        L.append('**Road %d, %s** (%s -> %s, %s). %s' % (r['n'], r['name'], W.SETTLEMENTS[r['frm']][0],
                                                          W.SETTLEMENTS[r['to']][0], r['chapter'], r['note']))
        for l in r['legs']:
            L.append('- **%s** (%d, %s, `:%s`, %dx%d%s): %s *Landmark:* %s *Secret:* %s' % (
                l['name'], l['id'], kingdom_field(l['kingdom']), l['field'], l['size'][0], l['size'][1],
                '' if l['role'] == 'main' else ', %s road' % l['role'], l['origin'], l['landmark'], l['secret']))
        L.append('')
    L += ['### What the map builder rebuilds', '',
          'Listed in `mapgen/REQUESTS.md` (cartographer entry): the Revision 14 relinks of the early maps, the new maps '
          '527, 528, 552, 566, 577, 578, the growth of built maps to their target sizes, and the renamed names and signs '
          'in specs and layouts (already changed in the sources by `tools/rename_places.py`).', '', END]
    return '\n'.join(L)


def update_world_md(sq):
    p = os.path.join(ROOT, 'design', 'WORLD.md')
    t = open(p, encoding='utf-8').read()
    sec = world_section(sq)
    if BEGIN in t:
        a = t.index(BEGIN)
        b = t.index(END) + len(END)
        t = t[:a] + sec + t[b:]
    else:
        t = t.rstrip('\n') + '\n\n---\n' + sec + '\n'
    open(p, 'w', encoding='utf-8').write(t)


def main():
    d = load_maps()
    have = {m['id'] for m in d['maps']}
    d['maps'] += [json.loads(json.dumps(e)) for i, e in EXTRA_MAPS.items() if i not in have]   # one pass: names too
    extra = []
    mi = os.path.join(ROOT, 'maps_out', 'mapinfos_prismfall.txt')
    if os.path.exists(mi):          # built maps that maps.json does not list (e.g. 134 Granny's Knot)
        extra = [{'id': int(l.split('\t')[0])} for l in open(mi, encoding='utf-8')
                 if l.strip() and not l.startswith('#') and int(l.split('\t')[0]) < 990]
    sq = build_squares(d['maps'] + [{'id': l['id']} for r, l in W.all_legs()] + extra)
    if '--no-maps-json' not in sys.argv:
        d = update_maps_json(sq)        # first: names and kingdoms below read the updated records (one pass)
    names = name_table(d['maps'])
    write_place_names(d['maps'], names, sq)
    write_routes_yaml(d['maps'], sq)
    n_pts = write_town_map(names, sq, d['maps'])
    nf = update_field_defaults()
    update_world_md(sq)
    miss = [m['id'] for m in d['maps'] if m['id'] not in sq]
    print('maps: %d  squares: %d  town-map points: %d  new FIELD_DEFAULTS entries: %d  maps without square: %s' % (
        len(d['maps']), len(sq), n_pts, nf, miss))


if __name__ == '__main__':
    main()
