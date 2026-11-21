"""Write art/research/SOURCES.md from registry.py + the moodboard tile lists. python3 -I sources_md.py"""
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import registry, moodboards as mb

rows = registry.rows()
used = collections.defaultdict(list)
for board, tiles in (('portraits', mb.PORTRAITS), ('characters', mb.CHARACTERS), ('pixel', mb.PIXEL)):
    for key, *_ in tiles:
        used[key.split(':', 1)[1]].append(board)

L = []
w = L.append
w('# Art study sources (2026-11-20)\n')
w('Study material for `art/STYLE_GUIDE.md`. **Nothing here ships in the game, and no piece is copied or traced:** we take principles, not pixels. '
  'Downloads are untrusted data kept outside the repo in `/home/claude/ref/art_refs/<source>/` (one folder per source, never executed, '
  'read only by `python3 -I` scripts in `art/research/scripts/`: `normalize.py` converted and downscaled each download). Large images were downscaled to <= 1200 px for study and the originals deleted. '
  'VGen pages expose service thumbnails (about 550 px, WebP); animated previews (WebM) were reduced to one frame.\n')
w('Moodboards: `moodboard_portraits.png`, `moodboard_characters.png`, `moodboard_pixel.png` (built by `scripts/moodboards.py`). '
  'Machine-readable list: `sources_registry.tsv`.\n')
w('## Summary\n')
cnt = collections.Counter(r[1] for r in rows)
w('| Artist / source | Images | Where |')
w('|---|---|---|')
for a, n in cnt.most_common():
    page = next(r[2] for r in rows if r[1] == a)
    w(f'| {a} | {n} | {page} |')
w('| Pokémon Desolation, in-game `Graphics/Faces` (90), `Transitions` (56 VS), `Characters` | studied in place | `/home/claude/ref/games/desolation/` (read-only) |')
w('| Pokémon Rejuvenation, in-game `Faces` (13), `Transitions` (132 VS), `Characters` (339 fronts at 180 px, overworlds) | studied in place | `/home/claude/ref/games/rejuvenation/` (read-only) |')
w('| Pokémon Reborn, in-game `Transitions` (98 VS), `Characters` (210 fronts at 160 px) | studied in place | `/home/claude/ref/games/reborn/` (read-only) |')
w('| Official B2W2 VS busts (Game Freak), fangame resource rip already on disk | 8 studied | `/home/claude/ref/art/sprites_gen5_vs_tech/` |')
w('| kyledove, Gen 5-style SWSH trainer classes | 2 on the moodboard | https://eeveeexpo.com/resources/942/ (`/home/claude/ref/art/sprites_kyledove_swsh/`) |')
w('| VanillaSunshine, Gen 4 overworlds for Essentials | 1 on the moodboard | https://eeveeexpo.com/resources/404/ (`/home/claude/ref/art/sprites_gen4_ow_vanillasunshine/`) |')
w(f'\nDownloaded: **{len(rows)} images from {len(cnt) - 1} artists** ({len(cnt)} sources: honnojis has two, the site and VGen). '
  'Plus the in-game art of three fangames and two Essentials resource packs already on disk.\n')
w('## Reached and not reached\n')
w('- **honnojis.art** (Squarespace): the whole gallery (44 items) is listed by the site; 32 still images downloaded at 1500 px via '
  '`images.squarespace-cdn.com/...?format=1500w`, the two pixel pieces at original size. Skipped: one GIF, 10 fan-art prints of other franchises not needed '
  'for the study (Estinien, Deltarune print, Eizen, Dimitri, id, omen, nendo, kyo koro, dandadan, okarun print). The site names no clients; '
  'the "rejuv" files, Erin and Aelita (both in Rejuvenation\'s own credits scene as main cast) and the V14 cover tie the work to Rejuvenation, and the '
  'artist\'s VGen bio says "Artist for Pokemon Rejuvenation". Rejuvenation\'s quest data also has a dev cameo "Zumi" (`Scripts/Rejuv/Quest/Data.rb`, read as text).')
w('- **vgen.co/honnojis**: profile and service pages render server-side, so WebFetch could read them; 18 service thumbnails downloaded '
  'from `storage.vgen.co`. Full-size portfolio images are not exposed without JavaScript. Commissions are closed.')
w('- **Other VGen artists**: VGen search (`/search?q=`) needs JavaScript and returned nothing. Artists were found with web search restricted to vgen.co '
  '("pokemon trainer sprite", "pixel portrait dialogue", "overworld sprite"), then read the same way: angeceleste, SilverSrini, Princeloppy, NoodlesXL, '
  'Mossgrover, InkyFrosty, Nifast Greentail, Fiorne. `azuregemmabyte` failed (client error); Akari-Yuu showed no services. NSFW-labelled sections '
  '(one artist has one) were not downloaded, and one borderline thumbnail was deleted.')
w('- **Not reached**: rebornevo.com forum (robots disallowed); The Spriters Resource, Bulbapedia, PokéCommunity, Reddit returned 403 in the earlier study '
  '(`design/CHARACTER_DESIGN_STUDY.md` §1) and were not retried. Web search for "fangame sprite artist" mostly returns Fiverr gigs, which were not used.\n')
w('## Every downloaded image\n')
w('| Local file (`/home/claude/ref/art_refs/`) | Artist | Moodboard | Image URL |')
w('|---|---|---|---|')
for f, a, page, url in rows:
    w(f'| `{f}` | {a} | {", ".join(used.get(f, [])) or "-"} | {url} |')
w('\n## In-game and library images used on the moodboards\n')
w('| File | Source | Moodboard |')
w('|---|---|---|')
for key, boards in sorted(used.items()):
    if key.startswith('honnojis/') or key.startswith('vgen_'): continue
    src = 'Desolation' if 'desolation' in key else 'Rejuvenation' if 'rejuvenation' in key else 'Reborn' if 'reborn' in key else \
          'official B2W2 (resource rip)' if 'gen5_vs' in key else 'kyledove' if 'kyledove' in key else 'VanillaSunshine' if 'vanilla' in key else 'Prismfall (ours)'
    w(f'| `{key}` | {src} | {", ".join(sorted(set(boards)))} |')
open('/home/claude/fangame/art/research/SOURCES.md', 'w').write('\n'.join(L) + '\n')
print(len(rows), 'downloads;', len(used), 'moodboard keys')
