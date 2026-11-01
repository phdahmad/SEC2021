#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""شبكة إحداثيات فوق لقطة، لقراءة مواضع الأزرار بدقّة قبل التعليم."""
import sys, pathlib
from PIL import Image, ImageDraw, ImageFont

def grid(src, dst, step=50, scale=1.0):
    im = Image.open(src).convert("RGB")
    if scale != 1.0:
        im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    try:
        f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 12)
    except Exception:
        f = ImageFont.load_default()
    for x in range(0, im.width, step):
        major = (x // step) % 2 == 0
        d.line([(x, 0), (x, im.height)], fill=(255, 0, 0) if major else (255, 180, 180))
        if major: d.text((x + 2, 1), str(int(x / scale)), fill=(190, 0, 0), font=f)
    for y in range(0, im.height, step):
        major = (y // step) % 2 == 0
        d.line([(0, y), (im.width, y)], fill=(0, 0, 255) if major else (180, 180, 255))
        if major: d.text((1, y + 1), str(int(y / scale)), fill=(0, 0, 190), font=f)
    im.save(dst)
    return im.size

if __name__ == "__main__":
    print(grid(sys.argv[1], sys.argv[2],
               int(sys.argv[3]) if len(sys.argv) > 3 else 50,
               float(sys.argv[4]) if len(sys.argv) > 4 else 1.0))
