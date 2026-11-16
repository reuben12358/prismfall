#!/usr/bin/env python3
"""Inspect an RMXP map file (safe parser).
usage: python3 -I inspect_map.py <MapNNN.rxdata> [--events] [--event ID] [--structure]"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rmarshal as M

CODES = {0: 'end', 101: 'text', 401: 'text+', 102: 'choices', 402: 'when', 403: 'cancel', 404: 'endchoice',
         103: 'numinput', 104: 'textopts', 105: 'btninput', 106: 'wait', 108: 'comment', 408: 'comment+',
         111: 'if', 411: 'else', 412: 'endif', 112: 'loop', 413: 'repeat', 113: 'break', 115: 'exit',
         116: 'erase', 117: 'common', 118: 'label', 119: 'jump', 121: 'switch', 122: 'var', 123: 'selfsw',
         124: 'timer', 125: 'gold', 126: 'item', 129: 'party', 132: 'battlebgm', 201: 'transfer', 202: 'setevloc',
         203: 'scroll', 204: 'mapsettings', 205: 'fogtone', 206: 'fogopac', 207: 'anim', 208: 'transparent',
         209: 'moveroute', 509: 'mr+', 210: 'waitmove', 221: 'prepare', 222: 'execute', 223: 'tone', 224: 'flash',
         225: 'shake', 231: 'pic', 241: 'bgm', 242: 'fadebgm', 245: 'bgs', 249: 'me', 250: 'se', 251: 'stopse',
         314: 'recover', 351: 'menu', 353: 'gameover', 354: 'title', 355: 'script', 655: 'script+'}


def struct_of(o, depth=0, seen=None):
    pad = '  ' * depth
    if isinstance(o, M.RObject):
        print(pad + o.cls)
        for k, v in o.ivars.items():
            if isinstance(v, (M.RObject, list, dict)) and depth < 4:
                print(pad + '  @' + k + ':')
                if isinstance(v, list):
                    if v: struct_of(v[0], depth + 2)
                elif isinstance(v, dict):
                    if v: struct_of(next(iter(v.values())), depth + 2)
                else:
                    struct_of(v, depth + 2)
            else:
                print(pad + '  @%s = %r' % (k, v if not isinstance(v, (list, dict)) else type(v)))
    else:
        print(pad + repr(o)[:80])


def dump_event(ev):
    print('EVENT %d "%s" at (%d,%d) pages=%d' % (ev.id, ev.name, ev.x, ev.y, len(ev.pages)))
    for pi, pg in enumerate(ev.pages):
        c = pg.condition; g = pg.graphic
        conds = []
        if c.switch1_valid: conds.append('sw%d' % c.switch1_id)
        if c.switch2_valid: conds.append('sw%d' % c.switch2_id)
        if c.variable_valid: conds.append('var%d>=%d' % (c.variable_id, c.variable_value))
        if c.self_switch_valid: conds.append('self' + c.self_switch_ch)
        print('  page %d cond=%s trig=%d gfx=%r/%d dir=%d pat=%d tile=%d move=%d thru=%s anim=%s step=%s fix=%s pri=%s' % (
            pi, conds, pg.trigger, g.character_name, g.character_hue, g.direction, g.pattern, g.tile_id,
            pg.move_type, pg.through, pg.walk_anime, pg.step_anime, pg.direction_fix, pg.always_on_top))
        for cmd in pg.list:
            print('    %s%d %s %r' % ('  ' * cmd.indent, cmd.code, CODES.get(cmd.code, '?'), cmd.parameters)[:200])


def main():
    m = M.load_file(sys.argv[1])
    a = sys.argv[2:]
    if '--structure' in a:
        struct_of(m)
        ev = next(iter(m.events.values()), None)
        if ev:
            print('--- first event'); struct_of(ev)
            print('--- page ivars:', list(ev.pages[0].ivars.keys()))
            print('--- cond ivars:', list(ev.pages[0].condition.ivars.keys()))
            print('--- gfx ivars:', list(ev.pages[0].graphic.ivars.keys()))
            print('--- moveroute ivars:', list(ev.pages[0].move_route.ivars.keys()),
                  [list(x.ivars.keys()) for x in ev.pages[0].move_route.list[:1]])
            print('--- cmd ivars:', list(ev.pages[0].list[0].ivars.keys()))
        print('--- bgm', m.bgm.ivars, 'enc', m.encounter_list, m.encounter_step)
    if '--events' in a:
        for k in sorted(m.events):
            dump_event(m.events[k])
    if '--event' in a:
        dump_event(m.events[int(a[a.index('--event') + 1])])


if __name__ == '__main__':
    main()
