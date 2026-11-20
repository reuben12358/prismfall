#!/usr/bin/env python3
"""Seam check for map edge connections (playtest tool; events are ignored, tile passability as in Essentials).
For every open edge tile of map A toward map B it prints the arrival tile on B and whether it is blocked, off the map,
or how much open ground it reaches (400+ = fine). Optional start tile: also says which edge tiles A's start reaches.
  python3 -I seam_check.py MAPGEN_DIR DATA_DIR CONNECTIONS_TXT A B [sx sy]
  e.g. python3 -I tools/harness/playtest/seam_check.py mapgen maps_out/Data maps_out/PBS/map_connections_prismfall.txt 520 521
DATA_DIR needs MapNNN.rxdata and Tilesets_prismfall.rxdata (maps_out/Data or an unzipped kit's Data/)."""
import sys, os
sys.path.insert(0, sys.argv[1])
import rmarshal as M
data_dir, conn_file, A, B = sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
start = (int(sys.argv[6]), int(sys.argv[7])) if len(sys.argv) > 7 else None
tsets = {}
for k, t in M.load_file(os.path.join(data_dir, "Tilesets_prismfall.rxdata")).items():
    tsets[k] = t.ivars

class Map:
    def __init__(self, mid):
        m = M.load_file(os.path.join(data_dir, "Map%03d.rxdata" % mid)).ivars
        self.w, self.h, self.data = m['width'], m['height'], m['data']
        self.tid = m['tileset_id']
        ts = tsets[m['tileset_id']]
        self.pas, self.pri = ts['passages'], ts['priorities']
    def valid(self, x, y): return 0 <= x < self.w and 0 <= y < self.h
    def tile_ok(self, x, y, d):
        bit = (1 << (d // 2 - 1)) & 0x0f
        for z in (2, 1, 0):
            t = int(self.data.data[z, y, x])
            if t == 0: continue
            p = int(self.pas.data[0, 0, t])
            if p & bit or (p & 0x0f) == 0x0f: return False
            pr = int(self.pri.data[0, 0, t])
            if pr == 0: return True
        return True
    def step(self, x, y, d):
        dx, dy = {2: (0, 1), 4: (-1, 0), 6: (1, 0), 8: (0, -1)}[d]
        nx, ny = x + dx, y + dy
        if not self.valid(nx, ny) or not self.tile_ok(x, y, d) or not self.tile_ok(nx, ny, 10 - d): return None
        return nx, ny
    def region(self, sx, sy, cap=10**6):
        seen = {(sx, sy)}; q = [(sx, sy)]
        while q and len(seen) < cap:
            x, y = q.pop()
            for d in (2, 4, 6, 8):
                n = self.step(x, y, d)
                if n and n not in seen: seen.add(n); q.append(n)
        return seen

a, b = Map(A), Map(B)
conns = []
for line in open(conn_file, encoding="utf-8"):
    line = line.split("#")[0].strip()
    if not line: continue
    p = [x.strip() for x in line.split(",")]
    m1, e1, o1, m2, e2, o2 = int(p[0]), p[1], int(p[2]), int(p[3]), p[4], int(p[5])
    if (m1, m2) == (A, B): conns.append((e1, o1, e2, o2))
    elif (m1, m2) == (B, A): conns.append((e2, o2, e1, o1))
reach = a.region(*start) if start else None
for ea, oa, eb, ob in conns:
    print(f"connection {A} {ea} @{oa} <-> {B} {eb} @{ob}  ({A} is {a.w}x{a.h}, {B} is {b.w}x{b.h})")
    rows = []
    for i in range(max(a.w, a.h)):
        if ea in ("N", "S"):
            ax, ay, d = i, (0 if ea == "N" else a.h - 1), (8 if ea == "N" else 2)
            if ax >= a.w: break
            bx, by = ax - oa + ob, (b.h - 1 if ea == "N" else 0)
        else:
            ax, ay, d = (0 if ea == "W" else a.w - 1), i, (4 if ea == "W" else 6)
            if ay >= a.h: break
            bx, by = (b.w - 1 if ea == "W" else 0), ay - oa + ob
        if not a.tile_ok(ax, ay, d): continue
        if not b.valid(bx, by): rows.append(f"  {A}({ax},{ay}) open -> {B}({bx},{by}) OFF THE MAP"); continue
        if not b.tile_ok(bx, by, 10 - d): rows.append(f"  {A}({ax},{ay}) open -> {B}({bx},{by}) BLOCKED"); continue
        size = len(b.region(bx, by, 400))
        r = "" if reach is None else ("  reachable from start" if (ax, ay) in reach else "  NOT reachable from start")
        rows.append(f"  {A}({ax},{ay}) open -> {B}({bx},{by}) region {size}{'+' if size >= 400 else ''}{r}")
    print("\n".join(rows) if rows else "  no open edge tiles")
