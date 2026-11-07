#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ينقل إطارات الأشكال من اللقطات القديمة (JPEG) إلى اللقطات الجديدة (PNG بلا فقدان).

لكل شكل: يبحث عن منطقة القصّ القديمة داخل اللقطة الجديدة المقابلة بمطابقة القوالب
على مقاييس متعددة (فالمجموعات قد تنزاح أفقياً بين الإصدارين)، ثم يبحث عن كل زر
داخل الإطار منفرداً في جوار موضعه المتوقَّع ليضبطه بدقة.

  python3 _remap.py word|xl|ppt
يكتب _remap_<track>.json: لكل شكل مصدره الجديد وقصّه وإطاراته ودرجات التطابق.
"""
import sys, json, importlib
import numpy as np, cv2

TRACKS = {
 'word': ('_shots', {
    'home-paragraph': 'word-home', 'home-font': 'word-home', 'home-editing': 'word-home',
    'home-styles': 'word-home', 'status-language': 'word-status',
    'ins-table-illus': 'word-insert', 'ins-header-footer': 'word-insert',
    'design-page-bg': 'word-design', 'layout-page-setup': 'word-layout',
    'view-show': 'word-view', 'ref-toc': 'word-references',
    'review-proofing': 'word-review', 'review-track': 'word-review',
    'review-comments': 'word-review', 'review-protect': 'word-review',
    'mail-start': 'word-mailings', 'mail-preview-finish': 'word-mailings',
    # حالات خاصة التُقطت لاحقاً (نوافذ وقوائم وتبويبات سياقية)
    'dlg-replace': 'word-replace', 'ins-table-grid': 'word-tablegrid',
    'tbl-merge-size': 'word-tablelayout', 'tbl-data': 'word-tablelayout',
    'tbl-styles': 'word-tabledesign', 'print-settings': 'word-print',
    'protect-pane-2': 'word-protect2', 'protect-pane-1': 'word-protect1'}),
 'xl': ('_shots_xl', {
    'ribbon-home': 'xl-home', 'ribbon-insert': 'xl-insert', 'ribbon-pagelayout': 'xl-pagelayout',
    'ribbon-formulas': 'xl-formulas', 'ribbon-data': 'xl-data', 'ribbon-review': 'xl-review',
    'ribbon-view': 'xl-view',
    'window': 'xl-window', 'bottombar': 'xl-window', 'cf-menu': 'xl-cfmenu',
    'table-dialog': 'xl-tabledialog', 'ribbon-tabledesign': 'xl-tabledesign',
    'ribbon-chartdesign': 'xl-chartdesign'}),
 'ppt': ('_shots_ppt', {
    'statusbar': 'ppt-home', 'quickaccess': 'ppt-home', 'home-slides': 'ppt-home',
    'view-modes': 'ppt-view', 'view-masters': 'ppt-view',
    'design-themes': 'ppt-design', 'design-left': 'ppt-design',
    'insert-wide': 'ppt-insert', 'transitions-gallery': 'ppt-transitions',
    'transitions-timing': 'ppt-transitions', 'anim-add': 'ppt-animations',
    'slideshow': 'ppt-slideshow',
    'window-full': 'ppt-home', 'layout-gallery': 'ppt-layouts', 'bg-styles': 'ppt-bgstyles',
    'content-icons': 'ppt-content', 'smartart-dialog': 'ppt-smartart-dialog',
    'smartart-create': 'ppt-smartart', 'smartart-styles': 'ppt-smartart'}),
}
BOTTOM = {'status-language', 'statusbar', 'bottombar'}
# مصادر ليست شريطاً: يُبحث عنها في الشاشة كلها
FULL = {'dlg-replace', 'ins-table-grid', 'print-settings', 'protect-pane-2', 'protect-pane-1',
        'window', 'cf-menu', 'table-dialog', 'window-full', 'layout-gallery', 'bg-styles',
        'content-icons', 'smartart-dialog'}

_cache = {}
def gray(p):
    if p not in _cache:
        im = cv2.imread(p, cv2.IMREAD_GRAYSCALE)
        if im is None:
            raise SystemExit('تعذّر فتح ' + p)
        _cache[p] = im
    return _cache[p]

def rs(img, s):
    h, w = img.shape
    return cv2.resize(img, (max(1, int(round(w * s))), max(1, int(round(h * s)))),
                      interpolation=cv2.INTER_AREA if s < 1 else cv2.INTER_CUBIC)

def best_in(hay, tpl, scales):
    best = (-1.0, None, None)
    for s in scales:
        t = rs(tpl, s)
        if t.shape[0] >= hay.shape[0] or t.shape[1] >= hay.shape[1] or min(t.shape) < 6:
            continue
        r = cv2.matchTemplate(hay, t, cv2.TM_CCOEFF_NORMED)
        _, mv, _, ml = cv2.minMaxLoc(r)
        if mv > best[0]:
            best = (float(mv), float(s), ml)
    return best

def locate(tpl, new, band, s_hint=None):
    """بحث خشن بربع/نصف الدقة ثم تنقيح."""
    y0, y1 = band
    hay = new[y0:y1]
    k = 0.5
    hay_k = rs(hay, k)
    scales = np.arange(0.40, 1.16, 0.02) if s_hint is None else np.arange(s_hint - 0.06, s_hint + 0.061, 0.01)
    sc, s0, (lx, ly) = best_in(hay_k, tpl, [s * k for s in scales])
    s0 = s0 / k
    cx, cy = int(lx / k), int(ly / k)
    th, tw = int(tpl.shape[0] * s0), int(tpl.shape[1] * s0)
    xa, xb = max(0, cx - 30), min(hay.shape[1], cx + tw + 30)
    ya, yb = max(0, cy - 30), min(hay.shape[0], cy + th + 30)
    sc2, s1, (fx, fy) = best_in(hay[ya:yb, xa:xb], tpl, np.arange(s0 - 0.03, s0 + 0.031, 0.005))
    if s1 is None:
        return sc, s0, cx, cy + y0
    return sc2, s1, xa + fx, ya + fy + y0

def refine_box(old, new, box, guess, s):
    """يبحث عن محتوى الإطار القديم في جوار ±60 بكسل حول موضعه المتوقَّع."""
    x0, y0, x1, y1 = [int(round(v)) for v in box[:4]]
    tpl = old[max(0, y0):y1, max(0, x0):x1]
    gx, gy = guess
    tw, th = int(tpl.shape[1] * s), int(tpl.shape[0] * s)
    R = 60
    xa, xb = max(0, int(gx) - R), min(new.shape[1], int(gx) + tw + R)
    ya, yb = max(0, int(gy) - R), min(new.shape[0], int(gy) + th + R)
    sc, s1, loc = best_in(new[ya:yb, xa:xb], tpl, [s])
    if s1 is None:
        return 0.0, gx, gy
    return sc, xa + loc[0], ya + loc[1]

def run(track, only=None):
    """only: قائمة مصادر قديمة تُعاد معالجتها وتُدمج في الملف القائم (يحفظ التصحيحات اليدوية)."""
    modname, mapping = TRACKS[track]
    m = importlib.import_module(modname)
    out, weak = {}, []
    if only:
        try: out = json.load(open('_remap_%s.json' % track))
        except FileNotFoundError: pass
    s_by_src = {}
    for src, dst, crop, boxes in m.JOBS:
        if src not in mapping or (only and src not in only):
            continue
        old = gray(m.SRC(src) if hasattr(m, 'SRC') else m.S % src)
        newname = mapping[src]
        new = gray('shots_png/%s.png' % newname)
        cx0, cy0, cx1, cy1 = crop if crop else (0, 0, old.shape[1], old.shape[0])
        tpl = old[cy0:cy1, cx0:cx1]
        band = ((new.shape[0] - 260, new.shape[0]) if src in BOTTOM else
                (0, new.shape[0]) if src in FULL else (0, 760))
        sc, s, ox, oy = locate(tpl, new, band, s_by_src.get(src))
        s_by_src.setdefault(src, s)
        nb = []
        for b in boxes:
            gx = ox + (b[0] - cx0) * s
            gy = oy + (b[1] - cy0) * s
            bs, bx, by = refine_box(old, new, b, (gx, gy), s)
            w, h = (b[2] - b[0]) * s, (b[3] - b[1]) * s
            if bs < 0.6:          # المطابقة الدقيقة ضعيفة: اعتمد الإسقاط الهندسي
                bx, by = gx, gy
            nb.append([int(round(bx)), int(round(by)), int(round(bx + w)), int(round(by + h)), b[4], round(bs, 3)])
        ncrop = [int(round(ox)), int(round(oy)), int(round(ox + (cx1 - cx0) * s)), int(round(oy + (cy1 - cy0) * s))]
        out[dst] = dict(src=newname, s=round(s, 4), crop=ncrop, score=round(sc, 3), boxes=nb)
        low = [b for b in nb if b[5] < 0.75]
        tag = '' if sc >= 0.75 and not low else '   ← افحص'
        if tag: weak.append(dst)
        print('%-36s s=%.3f  قصّ=%-24s تطابق=%.3f  أزرار=%s%s' % (
            dst.replace('sec2021-', ''), s, ncrop, sc, ' '.join('%.2f' % b[5] for b in nb), tag))
    json.dump(out, open('_remap_%s.json' % track, 'w'), ensure_ascii=False, indent=1)
    print('\n%d شكلاً، منها %d تحتاج فحصاً بالعين' % (len(out), len(weak)))

if __name__ == '__main__':
    run(sys.argv[1], sys.argv[2:] or None)
