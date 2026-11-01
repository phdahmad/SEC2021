#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""خريطة اللقطات: من أي لقطة خام، وأي زر يُؤطَّر، وبأي رقم خطوة.
   الإحداثيات بوحدات بكسل اللقطة الخام في shots2/ (دقّة الشاشة الأصلية)."""
import sys
sys.path.insert(0, '/home/claude/sec2021')
from _annotate import annotate

S = 'shots2/%s.jpg'
D = 'images/%s.webp'

JOBS = [
 # ───────── تمرين 1 ─────────
 ('status-language', 'sec2021-word-01-language-status', None,
  [(282, 8, 525, 48, '2')]),
 ('home-paragraph', 'sec2021-word-01-rtl-button', None,
  [(128, 26, 172, 70, '6')]),
 ('home-font', 'sec2021-word-01-font-group', None,
  [(558, 90, 592, 138, '7'), (44, 90, 88, 138, '7'),
   (512, 90, 542, 138, '12'), (259, 20, 357, 70, '12')]),
 ('home-paragraph', 'sec2021-word-01-paragraph-group', None,
  [(496, 26, 540, 70, '8'), (248, 91, 291, 136, '9'),
   (243, 26, 284, 70, '10'), (412, 26, 458, 70, '11'),
   (341, 91, 384, 136, '13')]),

 # ───────── تمرين 2 ─────────
 ('home-editing', 'sec2021-word-02-editing-group', None,
  [(14, 8, 192, 54, '2'), (14, 57, 192, 104, '3')]),
 ('dlg-replace', 'sec2021-word-02-replace-dialog', (0, 58, 1258, 412),
  [(20, 126, 1130, 162, '2'), (20, 248, 1130, 284, '3'),
   (372, 366, 504, 398, '4')]),

 # ───────── تمرين 3 ─────────
 ('ins-table-illus', 'sec2021-word-03-insert-picture', (412, 0, 572, 206),
  [(464, 18, 542, 138, '2')]),
 ('design-page-bg', 'sec2021-word-03-page-background', None,
  [(238, 8, 334, 152, '4'), (48, 8, 147, 152, '6')]),
 ('ins-header-footer', 'sec2021-word-03-page-number', None,
  [(16, 8, 130, 152, '5')]),

 # ───────── تمرين 4 ─────────
 ('home-font', 'sec2021-word-04-font-group', None,
  [(257, 20, 606, 70, '2'),
   (558, 90, 592, 138, '3'), (512, 90, 542, 138, '3'),
   (130, 90, 170, 138, '4'), (44, 90, 88, 138, '4')]),
 ('home-paragraph', 'sec2021-word-04-list-spacing', None,
  [(248, 91, 291, 136, '5'), (412, 26, 458, 70, '6'),
   (379, 34, 405, 62, '7')]),
 ('dlg-replace', 'sec2021-word-04-replace-options', (0, 58, 1258, 545),
  [(20, 126, 1130, 162, '8'), (20, 248, 1130, 284, '8'),
   (1082, 366, 1234, 398, '9'), (980, 495, 1212, 526, '9'),
   (372, 366, 504, 398, '9')]),
 ('layout-page-setup', 'sec2021-word-04-page-setup', None,
  [(60, 10, 182, 54, '10'), (356, 8, 434, 140, '11')]),
 ('home-styles', 'sec2021-word-04-styles', None,
  [(506, 18, 694, 114, '13')]),
 ('view-show', 'sec2021-word-04-navigation', None,
  [(8, 101, 234, 152, '14')]),
 ('ref-toc', 'sec2021-word-04-toc', None,
  [(210, 8, 330, 152, '15'), (26, 56, 210, 102, '15')]),

 # ───────── تمرين 5 ─────────
 ('ins-table-grid', 'sec2021-word-05-insert-table', None,
  [(176, 56, 392, 378, '1')]),
 ('tbl-merge-size', 'sec2021-word-05-merge-size', None,
  [(780, 8, 864, 152, '3'), (686, 8, 780, 152, '4'),
   (146, 10, 387, 58, '5'), (146, 90, 387, 140, '5')]),
 ('tbl-data', 'sec2021-word-05-data', None,
  [(320, 8, 404, 152, '6'), (210, 8, 314, 154, '9')]),
 ('tbl-styles', 'sec2021-word-05-styles', (1000, 0, 1509, 206),
  [(1118, 10, 1366, 138, '7')]),

 # ───────── تمرين 6 ─────────
 ('review-proofing', 'sec2021-word-06-proofing', None,
  [(140, 8, 302, 152, '2')]),
 ('review-track', 'sec2021-word-06-track', (40, 0, 400, 206),
  [(226, 8, 312, 152, '6'), (150, 8, 226, 152, '8'),
   (76, 8, 150, 152, '8')]),
 ('review-comments', 'sec2021-word-06-comments', (268, 0, 480, 206),
  [(390, 8, 478, 152, '7'), (303, 8, 380, 152, '8')]),

 # ───────── تمرين 7 ─────────
 ('mail-start', 'sec2021-word-07-mailings-start', None,
  [(786, 8, 882, 156, '1'), (684, 8, 784, 156, '2'),
   (2, 8, 74, 156, '3')]),
 ('mail-preview-finish', 'sec2021-word-07-mailings-finish', None,
  [(486, 8, 607, 154, '1'), (6, 8, 122, 154, '2')]),

 # ───────── تمرين 8 ─────────
 ('print-settings', 'sec2021-word-08-print', None,
  [(16, 40, 484, 124, '1'), (48, 136, 382, 186, '2'),
   (16, 541, 484, 624, '3'), (16, 370, 484, 448, '4')]),

 # ───────── تمرين 9 ─────────
 ('review-protect', 'sec2021-word-09-restrict-button', None,
  [(50, 8, 152, 152, '2')]),
 ('protect-pane-2', 'sec2021-word-09-restrict-pane', (0, 150, 462, 545),
  [(6, 225, 454, 285, '2'), (140, 286, 454, 324, '2'),
   (333, 494, 414, 530, '3')]),
 ('protect-pane-1', 'sec2021-word-09-enforce', (0, 350, 462, 541),
  [(170, 472, 427, 518, '4')]),
]

if __name__ == '__main__':
    for src, dst, crop, boxes in JOBS:
        size, b = annotate(S % src, D % dst, boxes, upscale=2.0, crop=crop)
        print('%-44s %-12s %4d KB' % (dst, '%dx%d' % size, round(b / 1024)))
