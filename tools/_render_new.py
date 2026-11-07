#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""يولّد صور الأشكال من اللقطات الجديدة (PNG بلا فقدان) بالقصّ والإطارات الناتجة عن _remap.py.

  python3 _render_new.py xl [مرشّح]     ← يكتب images/<الشكل>.webp
  OUT=/مسار python3 _render_new.py xl   ← يكتب إلى مجلد آخر للمعاينة
"""
import sys, os, json
sys.path.insert(0, '/home/claude/sec2021')
from _annotate import annotate

def run(track, only=None, out='images'):
    data = json.load(open('_remap_%s.json' % track))
    os.makedirs(out, exist_ok=True)
    for dst, d in data.items():
        if only and only not in dst:
            continue
        x0, y0, x1, y1 = d['crop']
        w = x1 - x0
        # الشكل الواسع يُكبَّر أقل حتى لا يتجاوز عرضه 2700 بكسل
        up = 2.0 if w <= 1350 else max(1.0, 2700.0 / w)
        boxes = [tuple(b[:5]) for b in d['boxes']]
        size, nbytes = annotate('shots_png/%s.png' % d['src'], os.path.join(out, dst + '.webp'),
                                boxes, upscale=up, crop=tuple(d['crop']))
        print('%-36s %-11s %4d KB' % (dst, '%dx%d' % size, round(nbytes / 1024)))

if __name__ == '__main__':
    run(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None, os.environ.get('OUT', 'images'))
