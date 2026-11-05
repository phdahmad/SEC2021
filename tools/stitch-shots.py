#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""لصق قطع اللقطة بترتيب صريح: اسم الناتج ثم معرّفات القطع من يسار الصورة إلى يمينها.
   python3 _grab.py ribbon-home 62eqop fcpn7j z9u551"""
import sys, glob, os
from PIL import Image

BLOBS = '/root/.claude/projects/-home-claude/aea6d358-d5a9-5f32-a37c-e40d280bd1a7/tool-results'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shots_xl')

def find(tag):
    hits = glob.glob(os.path.join(BLOBS, '*%s.jpg' % tag))
    if not hits:
        raise SystemExit('لم أجد قطعة بالمعرّف %s' % tag)
    return hits[0]

def main(name, tags):
    ims = [Image.open(find(t)).convert('RGB') for t in tags]
    if len(ims) == 1:
        out = ims[0]
    else:
        H = max(i.height for i in ims); W = sum(i.width for i in ims)
        out = Image.new('RGB', (W, H), (255, 255, 255)); x = 0
        for i in ims:
            out.paste(i, (x, 0)); x += i.width
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, name + '.jpg')
    out.save(p, quality=96)
    print(p, out.size, '|', ' + '.join('%dx%d' % i.size for i in ims))

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2:])
