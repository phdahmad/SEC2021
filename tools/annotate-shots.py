#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""تعليم لقطات وورد: إطار عنبري حول الزر المقصود + رقم اختياري، ثم حفظ WebP.

الوضوح: تُكبَّر اللقطة بـ LANCZOS قبل الرسم، فتُرسم الإطارات والأرقام بدقّتها
الكاملة لا مكبّرة عن بكسلات خشنة؛ ثم تُعرض الصورة في الورقة والموقع بعرض أصغر
من حجمها الحقيقي، فترتفع كثافتها النقطية وتبدو حادّة في الطباعة وعلى الشاشة.
"""
import sys, json, pathlib
from PIL import Image, ImageDraw, ImageFont

AMBER = (200, 118, 26)      # --amber-bright
LINE  = (220, 215, 203)

FONT_PATHS = ["/root/.fonts/Saudi-Bold.otf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]

def font(size):
    for p in FONT_PATHS:
        if pathlib.Path(p).exists():
            try: return ImageFont.truetype(p, size)
            except Exception: pass
    return ImageFont.load_default()

def annotate(src, dst, boxes, upscale=2.0, crop=None, quality=90):
    """boxes: [(x0,y0,x1,y1,label|None), ...] بإحداثيات صورة المصدر.
    crop: (x0,y0,x1,y1) قصّ أضيق حول المهمّ قبل التكبير — يُطبَّق على الإحداثيات أيضاً."""
    im = Image.open(src).convert("RGB")

    if crop:
        cx0, cy0, cx1, cy1 = crop
        im = im.crop((cx0, cy0, cx1, cy1))
        boxes = [(x0 - cx0, y0 - cy0, x1 - cx0, y1 - cy0, l) for x0, y0, x1, y1, l in boxes]

    f = float(upscale)
    if f != 1.0:
        im = im.resize((int(im.width * f), int(im.height * f)), Image.LANCZOS)
        boxes = [(x0 * f, y0 * f, x1 * f, y1 * f, l) for x0, y0, x1, y1, l in boxes]

    pad    = max(8, int(7 * f))
    stroke = max(3, int(2.2 * f))
    gap    = max(3, int(2.5 * f))

    canvas = Image.new("RGB", (im.width + pad * 2, im.height + pad * 2), (255, 255, 255))
    canvas.paste(im, (pad, pad))
    d = ImageDraw.Draw(canvas)
    d.rectangle([0, 0, canvas.width - 1, canvas.height - 1], outline=LINE,
                width=max(2, int(1.5 * f)))

    # حجم الرقم يُشتقّ من ارتفاع الإطار نفسه، ثم يُقيَّد بحجم اللقطة حتى لا يطغى
    hs = sorted(y1 - y0 for _, y0, _, y1, _ in boxes) or [60]
    size = max(26, min(64, int(hs[len(hs) // 2] * 0.5)))
    limit = min(canvas.width * 0.16, canvas.height * 0.50) / (2 * 0.82)
    fnt = font(max(16, int(min(size, limit))))
    placed = []
    for x0, y0, x1, y1, label in boxes:
        x0, y0 = x0 + pad - gap, y0 + pad - gap
        x1, y1 = x1 + pad + gap, y1 + pad + gap
        for w in range(stroke):
            d.rectangle([x0 - w, y0 - w, x1 + w, y1 + w], outline=AMBER)
        if label:
            r = int(fnt.size * 0.82)
            wide = (x1 - x0) > canvas.width * 0.35
            # المربع العريض: الرقم على حافته اليسرى حتى لا يحجب تسمية الحقل يمينه
            first = (x0 - r - stroke, y0 - 2) if wide else (x1 + r + stroke, y0 - 2)
            alts = [first,
                    (x1 + r + stroke, y0 - 2) if wide else (x0 - r - stroke, y0 - 2),
                    (x1 + r + stroke, y1 + 2), (x0 - r - stroke, y1 + 2)]
            cx, cy = first
            for ax, ay in alts:                     # تجنّب تداخل الأرقام بعضها ببعض
                ax = min(max(ax, r + 1), canvas.width - r - 1)
                ay = min(max(ay, r + 1), canvas.height - r - 1)
                if all((ax - px) ** 2 + (ay - py) ** 2 > (2 * r) ** 2 for px, py in placed):
                    cx, cy = ax, ay
                    break
                cx, cy = ax, ay
            placed.append((cx, cy))
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=AMBER,
                      outline=(255, 255, 255), width=max(2, int(1.5 * f)))
            bb = d.textbbox((0, 0), label, font=fnt)
            d.text((cx - (bb[2] - bb[0]) / 2, cy - (bb[3] - bb[1]) / 2 - bb[1]),
                   label, font=fnt, fill=(255, 255, 255))

    canvas.save(dst, "WEBP", quality=quality, method=6)
    return canvas.size, pathlib.Path(dst).stat().st_size

if __name__ == "__main__":
    cfg = json.loads(sys.argv[1])
    jobs = cfg if isinstance(cfg, list) else [cfg]
    for c in jobs:
        size, b = annotate(c["src"], c["dst"], [tuple(x) for x in c["boxes"]],
                           upscale=c.get("upscale", 2.0),
                           crop=tuple(c["crop"]) if c.get("crop") else None)
        print(pathlib.Path(c["dst"]).name, size, round(b / 1024), "KB")
