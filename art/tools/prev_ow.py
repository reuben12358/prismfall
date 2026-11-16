import sys
from PIL import Image
from overworld import OW
import cast
REF = '/home/claude/ref/ebdx_renovation/Graphics/Characters/'
def sheet(ids, path, S=4, refs=('trainer_RIVAL1', 'trainer_LEADER_Misty'), per_row=7):
    ims = [Image.open(REF + r + '.png').convert('RGBA').resize((64, 96), Image.NEAREST) for r in refs]
    ims += [OW(cast.CAST[c]['O']).sheet() for c in ids]
    rows = (len(ims) + per_row - 1) // per_row
    sh = Image.new('RGBA', (min(per_row, len(ims)) * 68, rows * 98), (120, 140, 150, 255))
    for i, im in enumerate(ims):
        sh.alpha_composite(im, ((i % per_row) * 68, (i // per_row) * 98))
    sh.resize((sh.width * S, sh.height * S), Image.NEAREST).save(path)
if __name__ == '__main__':
    sheet(sys.argv[2].split(','), sys.argv[1], int(sys.argv[3]) if len(sys.argv) > 3 else 4)
