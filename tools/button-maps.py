#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""يكتب «خريطة الأزرار» داخل وحدات مسار وورد في content.js — عربي وإنجليزي.
   يستبدل الخريطة الموجودة إن وُجدت، ويُدرجها قبل صندوق التمرين إن لم توجد."""
import io, re, sys

HEAD_AR = ('<h3>خريطة الأزرار: أين تجد ما ستحتاجه</h3>'
           '<p>قبل أن تبدأ التمرين، هذه لقطات من شريط وورد بواجهته العربية، '
           'والرقم في الدائرة هو رقم الخطوة التي يُستخدم فيها الزر.</p>')
HEAD_EN = ('<h3>Button map: where to find what you need</h3>'
           '<p>Before starting the exercise, here are screenshots of the Word ribbon in its '
           'Arabic interface. The number in each circle is the step where that button is used.</p>')

# (اسم الصورة, تسمية عربية, تسمية إنجليزية, بديل عربي, بديل إنجليزي)
MAPS = {
1: [
 ('sec2021-word-01-language-status',
  'شريط الحالة أسفل النافذة: مؤشر لغة الكتابة الحالية. تحقّق منه قبل أن تكتب.',
  'The status bar: the current keyboard language indicator. Check it before you type.',
  'شريط الحالة أسفل نافذة وورد، ومؤشر لغة الكتابة «العربية (المملكة العربية السعودية)» محاط بإطار ومرقّم بالخطوة 2',
  'The status bar at the bottom of the Word window, with the keyboard language indicator framed and numbered step 2'),
 ('sec2021-word-01-rtl-button',
  'زر «اتجاه نص من اليمين لليسار» في مجموعة «فقرة» — أهم زر في هذه الوحدة.',
  'The right-to-left text direction button in the Paragraph group — the key button of this unit.',
  'مجموعة فقرة في شريط وورد وزر اتجاه النص من اليمين إلى اليسار محاط بإطار عنبري ومرقّم بالخطوة 6',
  'The Paragraph group with the right-to-left direction button framed in amber and numbered step 6'),
 ('sec2021-word-01-font-group',
  'مجموعة «خط»: الغامق ولون الخط (خطوة 7)، والمائل وحجم الخط (خطوة 12).',
  'The Font group: bold and font colour (step 7), italic and font size (step 12).',
  'مجموعة خط في شريط وورد، وأزرار الغامق ولون الخط مرقّمة بالخطوة 7، والمائل وحجم الخط بالخطوة 12',
  'The Font group with bold and font colour numbered step 7, italic and font size numbered step 12'),
 ('sec2021-word-01-paragraph-group',
  'بقية مجموعة «فقرة»: التعداد النقطي (8)، وتباعد الأسطر (9)، وإنقاص المسافة البادئة (10)، والترقيم (11)، والضبط (13).',
  'The rest of the Paragraph group: bullets (8), line spacing (9), decrease indent (10), numbering (11), justify (13).',
  'مجموعة فقرة وأزرارها مرقّمة: التعداد النقطي 8، وتباعد الأسطر 9، وإنقاص المسافة البادئة 10، والترقيم 11، والضبط 13',
  'The Paragraph group with buttons numbered: bullets 8, line spacing 9, decrease indent 10, numbering 11, justify 13'),
],
2: [
 ('sec2021-word-02-editing-group',
  'مجموعة «تحرير» في طرف الشريط الرئيسي: «بحث» (خطوة 2) و«استبدال» (خطوة 3).',
  'The Editing group at the end of the Home tab: Find (step 2) and Replace (step 3).',
  'مجموعة تحرير في شريط وورد، وزر بحث مرقّم بالخطوة 2 وزر استبدال مرقّم بالخطوة 3',
  'The Editing group with the Find button numbered step 2 and the Replace button numbered step 3'),
 ('sec2021-word-02-replace-dialog',
  'نافذة «بحث واستبدال»: حقل «البحث عن» (2)، وحقل «استبدال بـ» (3)، وزر «استبدال الكل» (4).',
  'The Find and Replace dialog: the Find what field (2), the Replace with field (3), and Replace All (4).',
  'نافذة بحث واستبدال في وورد، وحقل البحث عن مرقّم 2، وحقل استبدال بـ مرقّم 3، وزر استبدال الكل مرقّم 4',
  'The Find and Replace dialog with the Find what field numbered 2, Replace with numbered 3, Replace All numbered 4'),
],
3: [
 ('sec2021-word-03-insert-picture',
  'تبويب «إدراج» ← مجموعة «رسومات توضيحية»: زر «صور» (خطوة 2).',
  'Insert tab → Illustrations group: the Pictures button (step 2).',
  'مجموعة رسومات توضيحية في تبويب إدراج، وزر صور محاط بإطار ومرقّم بالخطوة 2',
  'The Illustrations group on the Insert tab with the Pictures button framed and numbered step 2'),
 ('sec2021-word-03-page-number',
  'تبويب «إدراج» ← مجموعة «رأس وتذييل»: زر «رقم الصفحة» (خطوة 5).',
  'Insert tab → Header & Footer group: the Page Number button (step 5).',
  'مجموعة رأس وتذييل في تبويب إدراج، وزر رقم الصفحة محاط بإطار ومرقّم بالخطوة 5',
  'The Header & Footer group with the Page Number button framed and numbered step 5'),
 ('sec2021-word-03-page-background',
  'تبويب «تصميم» ← مجموعة «خلفية الصفحة»: «علامة مائية» (4) و«حدود الصفحة» (6).',
  'Design tab → Page Background group: Watermark (4) and Page Borders (6).',
  'مجموعة خلفية الصفحة في تبويب تصميم، وزر علامة مائية مرقّم 4 وزر حدود الصفحة مرقّم 6',
  'The Page Background group with the Watermark button numbered 4 and Page Borders numbered 6'),
],
4: [
 ('sec2021-word-04-font-group',
  'مجموعة «خط»: نوع الخط وحجمه (2)، والغامق والمائل (3)، ولون تمييز النص ولون الخط (4).',
  'The Font group: typeface and size (2), bold and italic (3), text highlight and font colour (4).',
  'مجموعة خط وأزرارها مرقّمة: نوع الخط والحجم 2، والغامق والمائل 3، ولون التمييز ولون الخط 4',
  'The Font group with typeface and size numbered 2, bold and italic 3, highlight and font colour 4'),
 ('sec2021-word-04-list-spacing',
  'مجموعة «فقرة»: تباعد الأسطر (5)، وزر «ترقيم» (6)، والسهم بجواره لتغيير نمط الترقيم (7).',
  'The Paragraph group: line spacing (5), the Numbering button (6), and its arrow for the numbering style (7).',
  'مجموعة فقرة وزر تباعد الأسطر مرقّم 5 وزر الترقيم مرقّم 6 والسهم المجاور له مرقّم 7',
  'The Paragraph group with line spacing numbered 5, numbering numbered 6 and its dropdown arrow numbered 7'),
 ('sec2021-word-04-replace-options',
  'نافذة «بحث واستبدال» موسّعة: الحقلان (8)، ثم «المزيد» و«مطابقة حالة الأحرف» و«استبدال الكل» (9). الزر يصير «أقل» بعد التوسيع.',
  'The expanded Find and Replace dialog: the two fields (8), then More, Match case and Replace All (9). The button reads “Less” once expanded.',
  'نافذة بحث واستبدال موسّعة، وحقلا البحث والاستبدال مرقّمان 8، وزر المزيد وخيار مطابقة حالة الأحرف وزر استبدال الكل مرقّمة 9',
  'The expanded Find and Replace dialog with both fields numbered 8 and the More button, Match case option and Replace All numbered 9'),
 ('sec2021-word-04-page-setup',
  'تبويب «تخطيط» ← «إعداد الصفحة»: «الفواصل» (خطوتا 10 و12) و«الاتجاه» (11).',
  'Layout tab → Page Setup: Breaks (steps 10 and 12) and Orientation (11).',
  'مجموعة إعداد الصفحة في تبويب تخطيط، وزر الفواصل مرقّم 10 وزر الاتجاه مرقّم 11',
  'The Page Setup group on the Layout tab with Breaks numbered 10 and Orientation numbered 11'),
 ('sec2021-word-04-styles',
  'معرض «أنماط» في الشريط الرئيسي: نمط «عنوان 1» (خطوة 13).',
  'The Styles gallery on the Home tab: the Heading 1 style (step 13).',
  'معرض أنماط في شريط وورد ونمط عنوان 1 محاط بإطار ومرقّم بالخطوة 13',
  'The Styles gallery with the Heading 1 style framed and numbered step 13'),
 ('sec2021-word-04-navigation',
  'تبويب «عرض» ← مجموعة «إظهار»: مربع «جزء التنقل» (خطوة 14).',
  'View tab → Show group: the Navigation Pane checkbox (step 14).',
  'مجموعة إظهار في تبويب عرض ومربع جزء التنقل محاط بإطار ومرقّم بالخطوة 14',
  'The Show group on the View tab with the Navigation Pane checkbox framed and numbered step 14'),
 ('sec2021-word-04-toc',
  'تبويب «مراجع» ← «جدول المحتويات»: إدراج الفهرس ثم «تحديث الجدول» (خطوة 15).',
  'References tab → Table of Contents: inserting the index and Update Table (step 15).',
  'مجموعة جدول المحتويات في تبويب مراجع، وزر جدول المحتويات وزر تحديث الجدول مرقّمان بالخطوة 15',
  'The Table of Contents group with both the Table of Contents and Update Table buttons numbered step 15'),
],
5: [
 ('sec2021-word-05-insert-table',
  'تبويب «إدراج» ← «جدول»: مرّر على الشبكة لاختيار 4 أعمدة × 6 صفوف (خطوة 1).',
  'Insert tab → Table: drag across the grid to pick 4 columns × 6 rows (step 1).',
  'شبكة إدراج جدول في وورد ومنطقة أربعة أعمدة وستة صفوف محاطة بإطار ومرقّمة بالخطوة 1',
  'The Insert Table grid with a four-column six-row area framed and numbered step 1'),
 ('sec2021-word-05-merge-size',
  'تبويب «تخطيط الجدول»: «دمج الخلايا» (3) و«تقسيم الخلايا» (4)، وحقلا الارتفاع والعرض (5).',
  'Table Layout tab: Merge Cells (3), Split Cells (4), and the height and width fields (5).',
  'مجموعتا دمج وحجم الخلية في تبويب تخطيط الجدول، وأزرارها مرقّمة 3 و4 و5',
  'The Merge and Cell Size groups on the Table Layout tab with buttons numbered 3, 4 and 5'),
 ('sec2021-word-05-data',
  'تبويب «تخطيط الجدول» ← «بيانات»: «فرز» (6) و«تكرار صفوف الرؤوس» (9).',
  'Table Layout tab → Data: Sort (6) and Repeat Header Rows (9).',
  'مجموعة بيانات في تبويب تخطيط الجدول، وزر فرز مرقّم 6 وزر تكرار صفوف الرؤوس مرقّم 9',
  'The Data group with the Sort button numbered 6 and Repeat Header Rows numbered 9'),
 ('sec2021-word-05-styles',
  'تبويب «تصميم الجدول» ← معرض «أنماط الجدول» (خطوة 7).',
  'Table Design tab → the Table Styles gallery (step 7).',
  'معرض أنماط الجدول في تبويب تصميم الجدول، ومجموعة من الأنماط محاطة بإطار ومرقّمة بالخطوة 7',
  'The Table Styles gallery with a set of styles framed and numbered step 7'),
],
6: [
 ('sec2021-word-06-proofing',
  'تبويب «مراجعة» ← «تدقيق»: «تدقيق إملائي وتدقيق نحوي» (خطوة 2)، وبديله المفتاح F7.',
  'Review tab → Proofing: Spelling & Grammar (step 2), or the F7 key.',
  'مجموعة تدقيق في تبويب مراجعة، وزر تدقيق إملائي ونحوي محاط بإطار ومرقّم بالخطوة 2',
  'The Proofing group with the Spelling and Grammar button framed and numbered step 2'),
 ('sec2021-word-06-track',
  'مجموعة «تعقب»: «تعقّب التغييرات» (6)، و«قبول» و«رفض» (8).',
  'The Tracking group: Track Changes (6), Accept and Reject (8).',
  'مجموعة تعقب في تبويب مراجعة، وزر تعقب التغييرات مرقّم 6 وزرا قبول ورفض مرقّمان 8',
  'The Tracking group with Track Changes numbered 6 and the Accept and Reject buttons numbered 8'),
 ('sec2021-word-06-comments',
  'مجموعة «تعليقات»: «تعليق جديد» (7) و«حذف» (8).',
  'The Comments group: New Comment (7) and Delete (8).',
  'مجموعة تعليقات في تبويب مراجعة، وزر تعليق جديد مرقّم 7 وزر حذف مرقّم 8',
  'The Comments group with the New Comment button numbered 7 and Delete numbered 8'),
],
7: [
 ('sec2021-word-07-mailings-start',
  'تبويب «مراسلات»: «بدء دمج المراسلات» (1)، و«تحديد المستلمين» (2)، و«إدراج حقل دمج» (3) — أرقام مرحلة «ثالثاً».',
  'Mailings tab: Start Mail Merge (1), Select Recipients (2), Insert Merge Field (3) — the steps of part three.',
  'تبويب مراسلات في وورد، وأزرار بدء دمج المراسلات وتحديد المستلمين وإدراج حقل دمج مرقّمة 1 و2 و3',
  'The Mailings tab with Start Mail Merge, Select Recipients and Insert Merge Field numbered 1, 2 and 3'),
 ('sec2021-word-07-mailings-finish',
  '«معاينة النتائج» (1) و«إنهاء ودمج» (2) — أرقام مرحلة «رابعاً».',
  'Preview Results (1) and Finish & Merge (2) — the steps of part four.',
  'مجموعتا معاينة النتائج وإنهاء في تبويب مراسلات، والزران مرقّمان 1 و2',
  'The Preview Results and Finish groups on the Mailings tab with both buttons numbered 1 and 2'),
],
8: [
 ('sec2021-word-08-print',
  'شاشة «ملف ← طباعة»: قائمة نطاق الطباعة (الخطوتان 1 و5)، ومربع «الصفحات» (2)، والهوامش (3)، واتجاه الورق (4).',
  'The File → Print screen: the print-range list (steps 1 and 5), the Pages box (2), margins (3) and paper orientation (4).',
  'عمود إعدادات الطباعة في وورد، وقائمة نطاق الطباعة مرقّمة 1 ومربع الصفحات مرقّم 2 والهوامش مرقّمة 3 والاتجاه مرقّم 4',
  'The print settings column with the print-range list numbered 1, the Pages box 2, margins 3 and orientation 4'),
],
9: [
 ('sec2021-word-09-restrict-button',
  'تبويب «مراجعة» ← «حماية»: زر «تقييد التحرير» (خطوة 2 من «ثانياً»).',
  'Review tab → Protect: the Restrict Editing button (step 2 of part two).',
  'مجموعة حماية في تبويب مراجعة، وزر تقييد التحرير محاط بإطار ومرقّم بالخطوة 2',
  'The Protect group with the Restrict Editing button framed and numbered step 2'),
 ('sec2021-word-09-restrict-pane',
  'جزء «تقييد التحرير»: «السماح فقط بهذا النوع من التحرير» ونوعه (2)، ومربع «الكل» في الاستثناءات (3).',
  'The Restrict Editing pane: “Allow only this type of editing” and its type (2), and the Everyone box under Exceptions (3).',
  'جزء تقييد التحرير في وورد، ومربع السماح فقط بهذا النوع من التحرير مرقّم 2 ومربع الكل مرقّم 3',
  'The Restrict Editing pane with the allow-only checkbox numbered 2 and the Everyone box numbered 3'),
 ('sec2021-word-09-enforce',
  'أسفل الجزء نفسه: زر «نعم، ابدأ بفرض الحماية» (4).',
  'Lower in the same pane: the “Yes, Start Enforcing Protection” button (4).',
  'قسم بدء الفرض في جزء تقييد التحرير، وزر نعم ابدأ بفرض الحماية محاط بإطار ومرقّم بالخطوة 4',
  'The Start Enforcement section with the Yes, Start Enforcing Protection button framed and numbered step 4'),
],
}

def esc(t):
    return t.replace('"', '\\"')

def block(n, lang):
    head = HEAD_AR if lang == 'ar' else HEAD_EN
    figs = []
    for i, (img, cap_ar, cap_en, alt_ar, alt_en) in enumerate(MAPS[n], 1):
        cap = cap_ar if lang == 'ar' else cap_en
        alt = alt_ar if lang == 'ar' else alt_en
        num = 'شكل و%d.%d' % (n, i) if lang == 'ar' else 'Figure W%d.%d' % (n, i)
        figs.append('<figure class="fig ui"><img src="images/%s.webp" alt="%s" loading="lazy">'
                    '<figcaption><span class="n">%s</span> %s</figcaption></figure>'
                    % (img, alt, num, cap))
    return esc(head + ''.join(figs))

LAB = '<div class=\\"lab\\">'
H_AR = '<h3>خريطة الأزرار'
H_EN = '<h3>Button map'

def main(path):
    s = io.open(path, encoding='utf-8').read()
    for n in range(9, 0, -1):                       # من الأخير للأول حتى لا تتزحزح المواضع
        m = re.search(r'id:\s*"w%d"' % n, s)
        if not m:
            print('تعذّر العثور على الوحدة w%d' % n); continue
        start = m.end()
        nxt = re.search(r'id:\s*"[a-z]\d+"', s[start:])
        end = start + (nxt.start() if nxt else len(s) - start)
        seg = s[start:end]
        out, pos, search = [], 0, 0
        for lang, head in (('ar', H_AR), ('en', H_EN)):
            lab = seg.index(LAB, search)
            h = seg.find(head, pos, lab)
            cut = h if h >= 0 else lab            # استبدال خريطة قائمة، أو إدراج جديدة
            out.append(seg[pos:cut])
            out.append(block(n, lang))
            pos, search = lab, lab + len(LAB)
        out.append(seg[pos:])
        s = s[:start] + ''.join(out) + s[end:]
        print('w%d: %d لقطة' % (n, len(MAPS[n])))
    io.open(path, 'w', encoding='utf-8').write(s)

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'content.js')
