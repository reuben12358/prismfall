import sys, os, re, json, glob
sys.path.insert(0, '/home/claude/fangame/mapgen')
import rmarshal as M
out = {}
pat = re.compile(r".")
for p in sorted(glob.glob('/home/claude/fangame/maps_out/Data/Map[0-9]*.rxdata')):
    mid = int(re.search(r'Map(\d+)', p).group(1))
    m = M.load_file(p)
    evs = m.ivars.get('events', {})
    rec = []
    for eid, ev in sorted(evs.items()):
        name = str(ev.ivars.get('name', ''))
        x, y = ev.ivars.get('x'), ev.ivars.get('y')
        pages = ev.ivars.get('pages', [])
        g = ''
        if pages:
            gr = pages[0].ivars.get('graphic')
            if gr is not None:
                g = str(gr.ivars.get('character_name', '')) + ('#tile%s' % gr.ivars.get('tile_id') if gr.ivars.get('tile_id') else '')
        scripts = []; texts = []
        for pg in pages:
            for cmd in pg.ivars.get('list', []):
                code = cmd.ivars.get('code'); params = cmd.ivars.get('parameters', [])
                if code in (355, 655, 111, 108, 408) and params:
                    s = params[-1] if code == 111 else params[0]
                    if isinstance(s, str) and pat.search(s):
                        scripts.append(s.strip())
                elif code in (101, 401) and params and isinstance(params[0], str):
                    if 'Received' in params[0] or 'received' in params[0] or 'obtained' in params[0]:
                        texts.append(params[0])
        rec.append({'id': eid, 'name': name, 'at': [x, y], 'g': g, 'scripts': scripts, 'texts': texts})
    out[mid] = rec
json.dump(out, open('/tmp/wt/map_events.json', 'w'), indent=1, default=str)
