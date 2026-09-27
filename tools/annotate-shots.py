#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""تعليم لقطات وورد: إطار عنبري حول الزر المقصود + رقم اختياري، ثم حفظ WebP."""
import sys, pathlib
from PIL import Image, ImageDraw, ImageFont

AMBER = (200, 118, 26)      # --amber-bright
INK   = (23, 53, 92)        # --ink
LINE  = (220, 215, 203)

FONT_PATHS = ["/root/.fonts/Saudi-Bold.otf", "/root/.fonts/SaudiText-Bold.otf"]

def font(size):
    for p in FONT_PATHS:
        if pathlib.Path(p).exists():
            try: return ImageFont.truetype(p, size)
            except Exception: pass
    return ImageFont.load_default()

def annotate(src, dst, boxes, pad=10, scale=1.0):
    """boxes: [(x0,y0,x1,y1,label|None), ...] بإحداثيات صورة المصدر"""
    im = Image.open(src).convert("RGB")
    if scale != 1.0:
        im = im.resize((int(im.width*scale), int(im.height*scale)), Image.LANCZOS)
        boxes = [(int(x0*scale), int(y0*scale), int(x1*scale), int(y1*scale), l) for x0,y0,x1,y1,l in boxes]

    # إطار خارجي فاتح حول اللقطة كلها
    canvas = Image.new("RGB", (im.width + pad*2, im.height + pad*2), (255, 255, 255))
    canvas.paste(im, (pad, pad))
    d = ImageDraw.Draw(canvas)
    d.rectangle([0, 0, canvas.width-1, canvas.height-1], outline=LINE, width=2)

    f = font(max(15, int(im.height * 0.10)))
    for x0, y0, x1, y1, label in boxes:
        x0, y0, x1, y1 = x0+pad, y0+pad, x1+pad, y1+pad
        x0, y0, x1, y1 = x0-4, y0-4, x1+4, y1+4   # هامش حول العنصر
        for w in range(4):                        # إطار سميك
            d.rectangle([x0-w, y0-w, x1+w, y1+w], outline=AMBER)
        if label:
            r = int(f.size * 0.85)
            wide = (x1 - x0) > canvas.width * 0.35
            # المربع العريض: الرقم على حافته اليسرى حتى لا يحجب تسمية الحقل يمينه
            cx, cy = (x0 - r - 4, y0 - 2) if wide else (x1 + r + 4, y0 - 2)
            if cx - r < 0: cx = x0 + r + 4
            if cx + r > canvas.width: cx = x1 - r - 4
            d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=AMBER, outline=(255,255,255), width=2)
            bb = d.textbbox((0,0), label, font=f)
            d.text((cx - (bb[2]-bb[0])/2, cy - (bb[3]-bb[1])/2 - bb[1]), label, font=f, fill=(255,255,255))

    canvas.save(dst, "WEBP", quality=93, method=6)
    return canvas.size, pathlib.Path(dst).stat().st_size

if __name__ == "__main__":
    import json
    cfg = json.loads(sys.argv[1])
    size, b = annotate(cfg["src"], cfg["dst"], [tuple(x) for x in cfg["boxes"]],
                       scale=cfg.get("scale", 1.0))
    print(pathlib.Path(cfg["dst"]).name, size, round(b/1024), "KB")
