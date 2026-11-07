#!/usr/bin/env python3
# يقصّ منطقة من لقطة ويرسم عليها شبكة إحداثيات (كل step بكسل) لقراءة المواضع بدقة
import sys
from PIL import Image, ImageDraw, ImageFont
F = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
src, x0, y0, x1, y1, out = sys.argv[1], *map(int, sys.argv[2:6]), sys.argv[6]
step = int(sys.argv[7]) if len(sys.argv) > 7 else 50
z = float(sys.argv[8]) if len(sys.argv) > 8 else 1.0
im = Image.open('shots_png/%s.png' % src).convert('RGB').crop((x0, y0, x1, y1))
im = im.resize((int(im.width * z), int(im.height * z)))
d = ImageDraw.Draw(im)
for x in range((x0 // step + 1) * step, x1, step):
    X = (x - x0) * z; d.line([(X, 0), (X, im.height)], fill=(255, 0, 200), width=1); d.text((X + 2, 2), str(x), fill=(200, 0, 150), font=F)
for y in range((y0 // step + 1) * step, y1, step):
    Y = (y - y0) * z; d.line([(0, Y), (im.width, Y)], fill=(0, 170, 255), width=1); d.text((2, Y + 2), str(y), fill=(0, 120, 200), font=F)
im.save(out); print(im.size)
