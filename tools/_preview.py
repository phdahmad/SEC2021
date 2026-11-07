#!/usr/bin/env python3
# معاينة سريعة: يرسم القصّ والإطارات من ملف _remap على اللقطة الجديدة ويرصّها في ورقة واحدة
import sys, json
from PIL import Image, ImageDraw, ImageFont
F = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
track, out = sys.argv[1], sys.argv[2]
keys = sys.argv[3:]
d = json.load(open('_remap_%s.json' % track))
tiles = []
for k, v in d.items():
    if keys and not any(s in k for s in keys): continue
    im = Image.open('shots_png/%s.png' % v['src']).convert('RGB')
    x0, y0, x1, y1 = v['crop']
    pad = 20
    c = im.crop((x0 - pad, y0 - pad, x1 + pad, y1 + pad))
    dr = ImageDraw.Draw(c)
    dr.rectangle([pad, pad, pad + x1 - x0, pad + y1 - y0], outline=(0, 160, 255), width=2)
    for b in v['boxes']:
        bx0, by0, bx1, by1 = [b[i] - (x0 if i % 2 == 0 else y0) + pad for i in range(4)]
        dr.rectangle([bx0, by0, bx1, by1], outline=(230, 0, 0), width=4)
        dr.text((bx0 + 4, by0 + 2), str(b[4]), fill=(230, 0, 0), font=F)
    r = min(900 / c.width, 600 / c.height, 1.5)
    c = c.resize((int(c.width * r), int(c.height * r)))
    tiles.append((k.replace('sec2021-', ''), c))
cols = 2
cw = 920; ch = max(t.height for _, t in tiles) + 40
rows = (len(tiles) + 1) // cols
S = Image.new('RGB', (cw * cols, ch * rows), 'white'); dr = ImageDraw.Draw(S)
for i, (n, t) in enumerate(tiles):
    x, y = (i % cols) * cw, (i // cols) * ch
    dr.text((x + 6, y + 4), n, fill=(0, 0, 0), font=F); S.paste(t, (x + 6, y + 34))
S.save(out); print(S.size)
