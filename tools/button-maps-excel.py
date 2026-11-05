#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""يكتب «خريطة الأزرار» داخل وحدات مسار إكسل في content.js — عربي وإنجليزي."""
import io, re, sys

HEAD_AR = ('<h3>خريطة الأزرار: أين تجد ما ستحتاجه</h3>'
           '<p>قبل أن تبدأ التمرين، هذه لقطات من شريط إكسل بواجهته العربية، '
           'والرقم في الدائرة هو رقم الخطوة التي يُستخدم فيها الزر.</p>')
HEAD_EN = ('<h3>Button map: where to find what you need</h3>'
           '<p>Before starting the exercise, here are screenshots of the Excel ribbon in its '
           'Arabic interface. The number in each circle is the step where that button is used.</p>')

# (اسم الصورة, تسمية عربية, تسمية إنجليزية, بديل عربي, بديل إنجليزي)
MAPS = {
1: [
 ('sec2021-xl-01-window',
  'أجزاء النافذة: مربع الاسم (4)، وشريط الصيغة (2)، ورؤوس الأعمدة (3)، ومنطقة الخلايا (5)، وتبويب الورقة (11)، وشريط الحالة (8). ولاحظ أن العمود <span class="spec">A</span> على اليمين لأن الورقة من اليمين إلى اليسار.',
  'The parts of the window: the Name Box (4), the formula bar (2), the column headers (3), the cell area (5), the sheet tab (11) and the status bar (8). Note that column <span class="spec">A</span> is on the right because the sheet is right-to-left.',
  'نافذة إكسل كاملة بواجهة عربية وورقة من اليمين إلى اليسار، وأجزاؤها محاطة بأطر عنبرية ومرقّمة',
  'The full Excel window in its Arabic interface with a right-to-left sheet, each part framed in amber and numbered'),
 ('sec2021-xl-01-bottom',
  'طرف النافذة السفلي: تبويب الورقة الذي تعيد تسميته بالنقر عليه بالزر الأيمن (11)، وزر إضافة ورقة (12)، وشريط الحالة الذي يعرض المجموع والمتوسط عند تحديد أرقام (8).',
  'The foot of the window: the sheet tab you rename by right-clicking it (11), the add-sheet button (12), and the status bar that shows sum and average when numbers are selected (8).',
  'تبويبات الأوراق وشريط الحالة في إكسل، والتبويب وزر الإضافة وشريط الحالة محاطة بأطر ومرقّمة 11 و12 و8',
  'The sheet tabs and status bar with the tab, the add button and the status bar framed and numbered 11, 12 and 8'),
 ('sec2021-xl-01-rtl',
  'تبويب «تخطيط الصفحة» ← مجموعة «خيارات الورقة»: زر <strong>«ورقة من اليمين لليسار»</strong> (13) — وهو خاصية على مستوى الورقة لا ترتيب أعمدة.',
  'Page Layout tab → Sheet Options: the <strong>Sheet Right-to-Left</strong> button (13) — a sheet-level property, not a rearrangement of columns.',
  'مجموعة خيارات الورقة في تبويب تخطيط الصفحة، وزر ورقة من اليمين لليسار محاط بإطار ومرقّم بالخطوة 13',
  'The Sheet Options group with the Sheet Right-to-Left button framed and numbered step 13'),
],
2: [
 ('sec2021-xl-02-align',
  'مجموعة «محاذاة» في الصفحة الرئيسية: <strong>«التفاف النص»</strong> (11) و<strong>«دمج وتوسيط»</strong> (8).',
  'The Alignment group on the Home tab: <strong>Wrap Text</strong> (11) and <strong>Merge &amp; Centre</strong> (8).',
  'مجموعة محاذاة في شريط إكسل، وزر التفاف النص مرقّم 11 وزر دمج وتوسيط مرقّم 8',
  'The Alignment group with the Wrap Text button numbered 11 and Merge and Centre numbered 8'),
 ('sec2021-xl-02-font',
  'مجموعة «خط»: <strong>لون التعبئة</strong> (9) و<strong>الحدود</strong> (10)، وبجوارهما نوع الخط وحجمه والغامق والمائل.',
  'The Font group: <strong>Fill Colour</strong> (9) and <strong>Borders</strong> (10), beside the typeface, size, bold and italic.',
  'مجموعة خط في شريط إكسل، ودلو لون التعبئة مرقّم 9 وزر الحدود مرقّم 10',
  'The Font group with the fill-colour bucket numbered 9 and the Borders button numbered 10'),
 ('sec2021-xl-02-number',
  'مجموعة «رقم»: قائمة تنسيق الأرقام (12 و14) وزر <strong>النسبة المئوية</strong> (13)، وبجوارهما العملة والفاصل الألفي وزيادة المنازل العشرية وإنقاصها.',
  'The Number group: the number-format list (12 and 14) and the <strong>Percentage</strong> button (13), beside currency, the thousands separator and the decimal-place buttons.',
  'مجموعة رقم في شريط إكسل، وقائمة تنسيق الأرقام مرقّمة 12 وزر النسبة المئوية مرقّم 13',
  'The Number group with the number-format list numbered 12 and the percentage button numbered 13'),
 ('sec2021-xl-02-painter',
  'مجموعة «الحافظة»: <strong>«نسخ التنسيق»</strong> (15) — الفرشاة التي تنقل التنسيق وحده بلا محتوى.',
  'The Clipboard group: <strong>Format Painter</strong> (15) — the brush that moves formatting alone, without content.',
  'مجموعة الحافظة في شريط إكسل، وزر نسخ التنسيق محاط بإطار ومرقّم بالخطوة 15',
  'The Clipboard group with the Format Painter button framed and numbered step 15'),
 ('sec2021-xl-02-freeze',
  'تبويب «عرض» ← مجموعة «نافذة»: <strong>«تجميد أجزاء»</strong> (16) الذي يُبقي صف الرؤوس ظاهراً عند التمرير.',
  'View tab → Window group: <strong>Freeze Panes</strong> (16), which keeps the header row visible as you scroll.',
  'مجموعة نافذة في تبويب عرض، وزر تجميد أجزاء محاط بإطار ومرقّم بالخطوة 16',
  'The Window group on the View tab with the Freeze Panes button framed and numbered step 16'),
],
3: [
 ('sec2021-xl-03-audit',
  'تبويب «الصيغ» ← مجموعة «تدقيق الصيغة»: <strong>«إظهار الصيغ»</strong> (14) و<strong>«تتبع السابقات»</strong> (15)، وتحتهما «تدقيق الأخطاء» و«تقييم الصيغة».',
  'Formulas tab → Formula Auditing: <strong>Show Formulas</strong> (14) and <strong>Trace Precedents</strong> (15), with Error Checking and Evaluate Formula below them.',
  'مجموعة تدقيق الصيغة في تبويب الصيغ، وزر إظهار الصيغ مرقّم 14 وزر تتبع السابقات مرقّم 15',
  'The Formula Auditing group with the Show Formulas button numbered 14 and Trace Precedents numbered 15'),
],
4: [
 ('sec2021-xl-04-autosum',
  'مجموعة «تحرير» في طرف الصفحة الرئيسية: <strong>«جمع تلقائي»</strong> (5) — ينشئ لك دالة <span class="spec">SUM</span> ويقترح النطاق بنفسه.',
  'The Editing group at the end of the Home tab: <strong>AutoSum</strong> (5) — it writes a <span class="spec">SUM</span> function and proposes the range itself.',
  'مجموعة تحرير في شريط إكسل، وزر المجموع التلقائي محاط بإطار ومرقّم بالخطوة 5',
  'The Editing group with the AutoSum button framed and numbered step 5'),
],
5: [
 ('sec2021-xl-05-cf',
  'مجموعة «أنماط» في الصفحة الرئيسية: زر <strong>«تنسيق شرطي»</strong> (7).',
  'The Styles group on the Home tab: the <strong>Conditional Formatting</strong> button (7).',
  'زر تنسيق شرطي في مجموعة أنماط محاط بإطار ومرقّم بالخطوة 7',
  'The Conditional Formatting button in the Styles group framed and numbered step 7'),
 ('sec2021-xl-05-cf-menu',
  'قائمة «تنسيق شرطي» بعد فتحها: <strong>«قواعد تمييز الخلايا»</strong> (7)، و<strong>«أشرطة البيانات»</strong> (8)، و<strong>«إدارة القواعد»</strong> في أسفلها (16).',
  'The Conditional Formatting menu once opened: <strong>Highlight Cells Rules</strong> (7), <strong>Data Bars</strong> (8), and <strong>Manage Rules</strong> at its foot (16).',
  'قائمة التنسيق الشرطي مفتوحة في إكسل، وثلاثة من بنودها محاطة بأطر ومرقّمة 7 و8 و16',
  'The open Conditional Formatting menu with three of its items framed and numbered 7, 8 and 16'),
],
6: [
 ('sec2021-xl-06-table',
  'تبويب «إدراج» ← مجموعة «جداول»: زر <strong>«جدول»</strong> (5)، وبديله المختصر <span class="kbd">Ctrl + T</span>.',
  'Insert tab → Tables group: the <strong>Table</strong> button (5), whose shortcut is <span class="kbd">Ctrl + T</span>.',
  'مجموعة جداول في تبويب إدراج، وزر جدول محاط بإطار ومرقّم بالخطوة 5',
  'The Tables group on the Insert tab with the Table button framed and numbered step 5'),
 ('sec2021-xl-06-dialog',
  'نافذة «إنشاء جدول»: نطاق البيانات الذي اقترحه إكسل، ومربع <strong>«يحتوي الجدول على رؤوس»</strong>، وزر «موافق» (5). تأكّد من المربع قبل الموافقة.',
  'The Create Table dialog: the range Excel proposed, the <strong>My table has headers</strong> box, and OK (5). Check the box before confirming.',
  'نافذة إنشاء جدول في إكسل، والنطاق ومربع الرؤوس وزر موافق محاطة بأطر ومرقّمة بالخطوة 5',
  'The Create Table dialog with the range, the headers checkbox and the OK button framed and numbered step 5'),
 ('sec2021-xl-06-design',
  'تبويب «تصميم الجدول» الذي يظهر بعد إنشاء الجدول: مربع <strong>«اسم الجدول»</strong> (6) و<strong>«صف الإجمالي»</strong> (7).',
  'The Table Design tab that appears once the table exists: the <strong>Table Name</strong> box (6) and <strong>Total Row</strong> (7).',
  'تبويب تصميم الجدول في إكسل، ومربع اسم الجدول مرقّم 6 وخيار صف الإجمالي مرقّم 7',
  'The Table Design tab with the Table Name box numbered 6 and the Total Row option numbered 7'),
 ('sec2021-xl-06-sort',
  'تبويب «بيانات» ← مجموعة «فرز وتصفية»: <strong>«فرز»</strong> للفرز على مستويات (9) و<strong>«تصفية»</strong> (10). وزر «مسح» بجوارهما باهت لأنه لا توجد تصفية مطبّقة بعد.',
  'Data tab → Sort &amp; Filter: <strong>Sort</strong> for multi-level sorting (9) and <strong>Filter</strong> (10). The Clear button beside them is greyed out because no filter is applied yet.',
  'مجموعة فرز وتصفية في تبويب بيانات، وزر فرز مرقّم 9 وزر تصفية مرقّم 10',
  'The Sort and Filter group with the Sort button numbered 9 and Filter numbered 10'),
 ('sec2021-xl-06-freeze',
  'تبويب «عرض»: <strong>«تجميد أجزاء»</strong> (15) لإبقاء الرؤوس ظاهرة في جدول طويل.',
  'View tab: <strong>Freeze Panes</strong> (15), to keep the headers visible in a long table.',
  'زر تجميد أجزاء في تبويب عرض محاط بإطار ومرقّم بالخطوة 15',
  'The Freeze Panes button on the View tab framed and numbered step 15'),
],
7: [
 ('sec2021-xl-07-charts',
  'تبويب «إدراج»: مجموعة «مخططات» وفيها <strong>العمودي</strong> (4) و<strong>الخطي</strong> (11) و<strong>الدائري</strong> (14)، ومجموعة «خطوط المؤشر» وفيها <strong>«خط»</strong> (18).',
  'The Insert tab: the Charts group with <strong>Column</strong> (4), <strong>Line</strong> (11) and <strong>Pie</strong> (14), and the Sparklines group with <strong>Line</strong> (18).',
  'تبويب إدراج في إكسل، وأزرار المخطط العمودي والخطي والدائري وخط المؤشر محاطة بأطر ومرقّمة 4 و11 و14 و18',
  'The Insert tab with the column, line and pie chart buttons and the sparkline button framed and numbered 4, 11, 14 and 18'),
 ('sec2021-xl-07-element',
  'تبويب «تصميم المخطط» الذي يظهر عند تحديد المخطط: <strong>«إضافة عنصر مخطط»</strong> (5 و6 و7) — ومنه العنوان وعناوين المحاور وتسميات البيانات.',
  'The Chart Design tab, which appears when a chart is selected: <strong>Add Chart Element</strong> (5, 6 and 7) — the source of the title, axis titles and data labels.',
  'زر إضافة عنصر مخطط في تبويب تصميم المخطط محاط بإطار ومرقّم بالخطوة 5',
  'The Add Chart Element button on the Chart Design tab framed and numbered step 5'),
 ('sec2021-xl-07-move',
  'في التبويب نفسه: <strong>«نقل المخطط»</strong> (17) لنقله إلى ورقة مستقلة، وبجواره «تغيير نوع المخطط» و«تحديد البيانات».',
  'On the same tab: <strong>Move Chart</strong> (17) to put it on a sheet of its own, beside Change Chart Type and Select Data.',
  'زر نقل المخطط في تبويب تصميم المخطط محاط بإطار ومرقّم بالخطوة 17',
  'The Move Chart button on the Chart Design tab framed and numbered step 17'),
],
8: [
 ('sec2021-xl-08-lookup',
  'تبويب «الصيغ»: <strong>«إدراج دالة»</strong> و<strong>«بحث وإشارة»</strong> (6) حيث تجد <span class="spec">VLOOKUP</span> و<span class="spec">XLOOKUP</span>، و<strong>«تقييم الصيغة»</strong> (16) لتتبّع صيغة خطوة خطوة.',
  'The Formulas tab: <strong>Insert Function</strong> and <strong>Lookup &amp; Reference</strong> (6), where <span class="spec">VLOOKUP</span> and <span class="spec">XLOOKUP</span> live, and <strong>Evaluate Formula</strong> (16) to step through a formula.',
  'تبويب الصيغ في إكسل، وأزرار إدراج دالة وبحث وإشارة وتقييم الصيغة محاطة بأطر ومرقّمة 6 و16',
  'The Formulas tab with the Insert Function, Lookup and Reference, and Evaluate Formula buttons framed and numbered 6 and 16'),
],
9: [
 ('sec2021-xl-09-page',
  'تبويب «تخطيط الصفحة»: حقلا <strong>العرض والطول</strong> في «تغيير الحجم بغرض الملاءمة» و<strong>«الاتجاه»</strong> (20)، و<strong>«طباعة العناوين»</strong> (21)، و<strong>«منطقة الطباعة»</strong> (22).',
  'The Page Layout tab: the <strong>Width</strong> and <strong>Height</strong> fields in Scale to Fit and <strong>Orientation</strong> (20), <strong>Print Titles</strong> (21) and <strong>Print Area</strong> (22).',
  'تبويب تخطيط الصفحة في إكسل، وحقول الحجم والاتجاه وطباعة العناوين ومنطقة الطباعة محاطة بأطر ومرقّمة 20 و21 و22',
  'The Page Layout tab with the scale fields, Orientation, Print Titles and Print Area framed and numbered 20, 21 and 22'),
 ('sec2021-xl-09-protect',
  'تبويب «مراجعة» ← مجموعة «حماية»: <strong>«حماية ورقة»</strong> (26) لجعل اللوحة للقراءة فقط.',
  'Review tab → Protect: <strong>Protect Sheet</strong> (26), to make the dashboard read-only.',
  'مجموعة حماية في تبويب مراجعة، وزر حماية ورقة محاط بإطار ومرقّم بالخطوة 26',
  'The Protect group on the Review tab with the Protect Sheet button framed and numbered step 26'),
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
        num = 'شكل ك%d.%d' % (n, i) if lang == 'ar' else 'Figure E%d.%d' % (n, i)
        figs.append('<figure class="fig ui"><img src="images/%s.webp" alt="%s" loading="lazy">'
                    '<figcaption><span class="n">%s</span> %s</figcaption></figure>'
                    % (img, alt, num, cap))
    return esc(head + ''.join(figs))


LAB = '<div class=\\"lab\\">'
H_AR = '<h3>خريطة الأزرار'
H_EN = '<h3>Button map'


def main(path):
    s = io.open(path, encoding='utf-8').read()
    for n in range(9, 0, -1):
        m = re.search(r'id:\s*"x%d"' % n, s)
        if not m:
            print('تعذّر العثور على الوحدة x%d' % n); continue
        start = m.end()
        nxt = re.search(r'id:\s*"[a-z]\d+"', s[start:])
        end = start + (nxt.start() if nxt else len(s) - start)
        seg = s[start:end]
        out, pos, search = [], 0, 0
        for lang, head in (('ar', H_AR), ('en', H_EN)):
            lab = seg.index(LAB, search)
            h = seg.find(head, pos, lab)
            cut = h if h >= 0 else lab
            out.append(seg[pos:cut])
            out.append(block(n, lang))
            pos, search = lab, lab + len(LAB)
        out.append(seg[pos:])
        s = s[:start] + ''.join(out) + s[end:]
        print('x%d: %d لقطة' % (n, len(MAPS[n])))
    io.open(path, 'w', encoding='utf-8').write(s)


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'content.js')
