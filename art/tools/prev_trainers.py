import sys
from PIL import Image
from trainer import Fig
import cast
REF = '/home/claude/ref/ebdx_renovation/Graphics/Trainers/'
def sheet(ids, path, S=4, refs=('RIVAL1', 'LEADER_Misty'), per_row=8):
    ims = []
    for r in refs:
        im = Image.open(REF + r + '.png').convert('RGBA'); ims.append(im.resize((64, 64), Image.NEAREST))
    for cid in ids:
        ims.append(Fig(cast.CAST[cid]['T']).build())
    rows = (len(ims) + per_row - 1) // per_row
    sh = Image.new('RGBA', (min(len(ims), per_row) * 64, rows * 64), (120, 140, 150, 255))
    for i, im in enumerate(ims):
        sh.alpha_composite(im, ((i % per_row) * 64, (i // per_row) * 64))
    sh.resize((sh.width * S, sh.height * S), Image.NEAREST).save(path)
    for cid, im in zip(ids, ims[len(refs):]):
        print(cid, len(im.getcolors(9999)) - 1, 'colours')
if __name__ == '__main__':
    sheet(sys.argv[2].split(','), sys.argv[1], int(sys.argv[3]) if len(sys.argv) > 3 else 4)
