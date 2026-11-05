#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""يكتب «خريطة الأزرار» داخل وحدات مسار باوربوينت في content.js — عربي وإنجليزي.
   يستبدل الخريطة الموجودة إن وُجدت، ويُدرجها قبل صندوق التمرين إن لم توجد."""
import io, re, sys

HEAD_AR = ('<h3>خريطة الأزرار: أين تجد ما ستحتاجه</h3>'
           '<p>قبل أن تبدأ التمرين، هذه لقطات من شريط باوربوينت بواجهته العربية، '
           'والرقم في الدائرة هو رقم الخطوة التي يُستخدم فيها الزر.</p>')
HEAD_EN = ('<h3>Button map: where to find what you need</h3>'
           '<p>Before starting the exercise, here are screenshots of the PowerPoint ribbon in its '
           'Arabic interface. The number in each circle is the step where that button is used.</p>')

# (اسم الصورة, تسمية عربية, تسمية إنجليزية, بديل عربي, بديل إنجليزي)
MAPS = {
1: [
 ('sec2021-ppt-01-window',
  'أجزاء النافذة: شريط العنوان (3)، وشريط أدوات الوصول السريع (4)، والشريط (5)، وجزء الشرائح المصغّرة — وهو على اليمين في الواجهة العربية — (7)، ومنطقة الشريحة (8)، وجزء الملاحظات (10)، وشريط الحالة (11).',
  'The parts of the window: title bar (3), Quick Access Toolbar (4), the ribbon (5), the slide thumbnail pane — on the right in the Arabic interface — (7), the slide area (8), the notes pane (10) and the status bar (11).',
  'نافذة باوربوينت كاملة بواجهة عربية، وأجزاؤها محاطة بأطر عنبرية ومرقّمة من 3 إلى 11',
  'The full PowerPoint window in its Arabic interface with each part framed in amber and numbered 3 to 11'),
 ('sec2021-ppt-01-statusbar',
  'طرف شريط الحالة: زر «ملاحظات» (10)، وأيقونات طرق العرض (12)، وشريط التكبير/التصغير (13).',
  'The end of the status bar: the Notes button (10), the view icons (12) and the zoom slider (13).',
  'طرف شريط الحالة في باوربوينت، وزر ملاحظات مرقّم 10 وأيقونات طرق العرض مرقّمة 12 وشريط التكبير مرقّم 13',
  'The end of the status bar with the Notes button numbered 10, the view icons numbered 12 and the zoom slider numbered 13'),
],
2: [
 ('sec2021-ppt-02-quickaccess',
  'أيقونة الحفظ (شكل القرص المرن) في شريط أدوات الوصول السريع (خطوة 8)، وبجوارها مفتاح «حفظ تلقائي».',
  'The Save icon (a floppy disk) on the Quick Access Toolbar (step 8), next to the AutoSave switch.',
  'شريط أدوات الوصول السريع في باوربوينت، وأيقونة الحفظ محاطة بإطار عنبري ومرقّمة بالخطوة 8',
  'The Quick Access Toolbar with the Save icon framed in amber and numbered step 8'),
],
3: [
 ('sec2021-ppt-03-slides-group',
  'مجموعة «شرائح» في الصفحة الرئيسية: «تخطيط» (2)، والجزء العلوي من زر «شريحة جديدة» (4)، وجزؤه السفلي الذي يفتح قائمة التخطيطات (5).',
  'The Slides group on the Home tab: Layout (2), the upper half of the New Slide button (4) and its lower half, which opens the layout list (5).',
  'مجموعة شرائح في شريط باوربوينت، وزر تخطيط مرقّم 2، وجزءا زر شريحة جديدة مرقّمان 4 و5',
  'The Slides group with the Layout button numbered 2 and the two halves of the New Slide button numbered 4 and 5'),
 ('sec2021-ppt-03-layouts',
  'معرض التخطيطات: «عنوان فقط» (2)، و«مقارنة» (5)، و«فارغ» (6). وفيه أيضاً «شريحة عنوان» و«عنوان ومحتوى» و«محتويان» و«عنوان المقطع».',
  'The layout gallery: Title Only (2), Comparison (5) and Blank (6). It also holds Title Slide, Title and Content, Two Content and Section Header.',
  'معرض تخطيطات الشرائح في باوربوينت، وتخطيط عنوان فقط مرقّم 2 ومقارنة مرقّم 5 وفارغ مرقّم 6',
  'The slide layout gallery with Title Only numbered 2, Comparison numbered 5 and Blank numbered 6'),
 ('sec2021-ppt-03-views',
  'تبويب «عرض» ← «طرق عرض العروض التقديمية»: «فارز الشرائح» (10)، و«عادي» (11)، و«طريقة عرض المخطط التفصيلي» (14).',
  'View tab → Presentation Views: Slide Sorter (10), Normal (11) and Outline View (14).',
  'مجموعة طرق عرض العروض التقديمية في تبويب عرض، وفارز الشرائح مرقّم 10 وعادي مرقّم 11 والمخطط التفصيلي مرقّم 14',
  'The Presentation Views group with Slide Sorter numbered 10, Normal numbered 11 and Outline View numbered 14'),
],
4: [
 ('sec2021-ppt-04-themes',
  'معرض «سمات» في تبويب «تصميم»: مرّر فوق المربعات لترى المعاينة قبل الاختيار (خطوة 5).',
  'The Themes gallery on the Design tab: hover over the swatches to preview before choosing (step 5).',
  'معرض السمات في تبويب تصميم، ومجموعة السمات محاطة بإطار عنبري ومرقّمة بالخطوة 5',
  'The Themes gallery with the set of themes framed in amber and numbered step 5'),
 ('sec2021-ppt-04-customize',
  'بقية تبويب «تصميم»: «اقتراحات التصميم» (11) في مجموعة «تحرير»، ثم مجموعة «تخصيص» وفيها «أنماط خلفية» (15) و«ألوان» و«خطوط» (9) و«أشكال مختلفة» (8).',
  'The rest of the Design tab: Design Ideas (11) in the Editing group, then the Customize group with Background Styles (15), Colors and Fonts (9) and Variants (8).',
  'تبويب تصميم في باوربوينت، وأزرار اقتراحات التصميم وأنماط خلفية وألوان وخطوط وأشكال مختلفة محاطة بأطر ومرقّمة 11 و15 و9 و8',
  'The Design tab with Design Ideas, Background Styles, Colors, Fonts and Variants framed and numbered 11, 15, 9 and 8'),
 ('sec2021-ppt-04-background',
  'قائمة «أنماط خلفية» بعد فتحها، وفي أسفلها الأمر «تنسيق الخلفية…» الذي يفتح الجزء الجانبي (خطوة 15).',
  'The Background Styles menu once opened, with the Format Background… command at its foot that opens the side pane (step 15).',
  'قائمة أنماط الخلفية مفتوحة في باوربوينت، وأمر تنسيق الخلفية أسفلها محاط بإطار ومرقّم بالخطوة 15',
  'The open Background Styles menu with the Format Background command at the bottom framed and numbered step 15'),
 ('sec2021-ppt-04-master',
  'تبويب «عرض» ← «طرق عرض الشكل الرئيسي»: زر «الشكل الرئيسي للشريحة» (19) — وهذا هو اسمه في الواجهة العربية.',
  'View tab → Master Views: the Slide Master button (19) — this is its name in the Arabic interface.',
  'مجموعة طرق عرض الشكل الرئيسي في تبويب عرض، وزر الشكل الرئيسي للشريحة محاط بإطار ومرقّم بالخطوة 19',
  'The Master Views group with the Slide Master button framed and numbered step 19'),
],
5: [
 ('sec2021-ppt-05-insert',
  'تبويب «إدراج»: «صور» في مجموعة «الصور» (3)، و«أشكال» (8) و«أيقونات» (12) في مجموعة «رسومات توضيحية».',
  'The Insert tab: Pictures in the Images group (3), Shapes (8) and Icons (12) in the Illustrations group.',
  'تبويب إدراج في باوربوينت، وزر صور مرقّم 3 وزر أشكال مرقّم 8 وزر أيقونات مرقّم 12',
  'The Insert tab with the Pictures button numbered 3, Shapes numbered 8 and Icons numbered 12'),
],
6: [
 ('sec2021-ppt-06-placeholders',
  'الأيقونات الستّ داخل مربع المحتوى: أيقونة «إدراج مخطط» (3) وأيقونة «إدراج رسم SmartArt» (11).',
  'The six icons inside a content placeholder: Insert Chart (3) and Insert SmartArt Graphic (11).',
  'أيقونات مربع المحتوى في شريحة باوربوينت، وأيقونة إدراج مخطط مرقّمة 3 وأيقونة SmartArt مرقّمة 11',
  'The content placeholder icons with the Insert Chart icon numbered 3 and the SmartArt icon numbered 11'),
 ('sec2021-ppt-06-insert',
  'الطريق البديل من الشريط: «مخطط» (3) و SmartArt (11) في مجموعة «رسومات توضيحية» بتبويب «إدراج».',
  'The alternative route from the ribbon: Chart (3) and SmartArt (11) in the Illustrations group of the Insert tab.',
  'مجموعة رسومات توضيحية في تبويب إدراج، وزر مخطط مرقّم 3 وزر SmartArt مرقّم 11',
  'The Illustrations group with the Chart button numbered 3 and the SmartArt button numbered 11'),
 ('sec2021-ppt-06-smartart-dialog',
  'نافذة «اختيار رسم SmartArt»: قائمة الفئات على اليمين ومنها «هيكلي»، وزر «موافق» أسفل النافذة (12).',
  'The Choose a SmartArt Graphic dialog: the category list on the right, including Hierarchy, and the OK button at the foot (12).',
  'نافذة اختيار رسم SmartArt، وقائمة الفئات وزر موافق محاطان بإطارين ومرقّمان بالخطوة 12',
  'The Choose a SmartArt Graphic dialog with the category list and the OK button framed and numbered step 12'),
 ('sec2021-ppt-06-smartart-tools',
  'تبويب «تصميم SmartArt»: «جزء النص» (13) و«إضافة شكل» (14).',
  'The SmartArt Design tab: Text Pane (13) and Add Shape (14).',
  'تبويب تصميم SmartArt، وزر جزء النص مرقّم 13 وزر إضافة شكل مرقّم 14',
  'The SmartArt Design tab with the Text Pane button numbered 13 and Add Shape numbered 14'),
 ('sec2021-ppt-06-smartart-styles',
  'في التبويب نفسه: «تغيير الألوان» ومعرض «أنماط SmartArt» (15).',
  'On the same tab: Change Colors and the SmartArt Styles gallery (15).',
  'زر تغيير الألوان ومعرض أنماط SmartArt محاطان بإطارين ومرقّمان بالخطوة 15',
  'The Change Colors button and the SmartArt Styles gallery framed and numbered step 15'),
],
7: [
 ('sec2021-ppt-07-transitions',
  'معرض الانتقالات في تبويب «انتقالات» — مجموعة «انتقال إلى هذه الشريحة» (خطوة 5).',
  'The transition gallery on the Transitions tab — the Transition to This Slide group (step 5).',
  'معرض الانتقالات في تبويب انتقالات، ومجموعة الانتقالات محاطة بإطار ومرقّمة بالخطوة 5',
  'The transition gallery with the set of transitions framed and numbered step 5'),
 ('sec2021-ppt-07-timing',
  'مجموعة «توقيت»: مربعا «عند النقر بالماوس» و«بعد» مع حقل المدة (7)، وزر «خيارات التأثير» لضبط اتجاه الانتقال المطبَّق في الخطوة 6.',
  'The Timing group: the On Mouse Click and After boxes with the duration field (7), and the Effect Options button that sets the direction of the transition applied in step 6.',
  'مجموعة توقيت في تبويب انتقالات، ومربعا عند النقر وبعد مرقّمان 7 وزر خيارات التأثير مرقّم 6',
  'The Timing group with the On Mouse Click and After boxes numbered 7 and the Effect Options button numbered 6'),
 ('sec2021-ppt-07-animations',
  'تبويب «حركات»: «جزء الحركة» (10)، و«إضافة حركة» (11)، و«خيارات التأثير» (12).',
  'The Animations tab: Animation Pane (10), Add Animation (11) and Effect Options (12).',
  'تبويب حركات في باوربوينت، وزر جزء الحركة مرقّم 10 وزر إضافة حركة مرقّم 11 وزر خيارات التأثير مرقّم 12',
  'The Animations tab with the Animation Pane button numbered 10, Add Animation numbered 11 and Effect Options numbered 12'),
 ('sec2021-ppt-07-slideshow',
  'تبويب «عرض الشرائح»: «من البداية» (16)، و«من الشريحة الحالية» (18)، و«إعداد عرض الشرائح» (20).',
  'The Slide Show tab: From Beginning (16), From Current Slide (18) and Set Up Slide Show (20).',
  'تبويب عرض الشرائح، وزر من البداية مرقّم 16 وزر من الشريحة الحالية مرقّم 18 وزر إعداد عرض الشرائح مرقّم 20',
  'The Slide Show tab with From Beginning numbered 16, From Current Slide numbered 18 and Set Up Slide Show numbered 20'),
],
8: [
 ('sec2021-ppt-08-theme',
  'معرض «سمات» في تبويب «تصميم»: اختر سمة هادئة الألوان قبل أن تبدأ البناء (خطوة 2).',
  'The Themes gallery on the Design tab: pick a calm theme before you start building (step 2).',
  'معرض السمات في تبويب تصميم، ومجموعة السمات محاطة بإطار ومرقّمة بالخطوة 2',
  'The Themes gallery with the set of themes framed and numbered step 2'),
 ('sec2021-ppt-08-smartart-colors',
  'زر «تغيير الألوان» في تبويب «تصميم SmartArt» (خطوة 5).',
  'The Change Colors button on the SmartArt Design tab (step 5).',
  'زر تغيير الألوان في تبويب تصميم SmartArt محاط بإطار ومرقّم بالخطوة 5',
  'The Change Colors button on the SmartArt Design tab framed and numbered step 5'),
 ('sec2021-ppt-08-apply-all',
  'زر «تطبيق على الكل» في مجموعة «توقيت» بتبويب «انتقالات» (خطوة 12) — ينسخ الانتقال إلى كل الشرائح.',
  'The Apply To All button in the Timing group of the Transitions tab (step 12) — it copies the transition to every slide.',
  'زر تطبيق على الكل في مجموعة توقيت محاط بإطار ومرقّم بالخطوة 12',
  'The Apply To All button in the Timing group framed and numbered step 12'),
 ('sec2021-ppt-08-effect-options',
  'تبويب «حركات»: «خيارات التأثير» لإظهار العناصر واحداً تلو الآخر (13)، و«جزء الحركة» لضبط بدء الحركة الثانية (14).',
  'The Animations tab: Effect Options to reveal items one by one (13), and the Animation Pane to set when the second animation starts (14).',
  'تبويب حركات، وزر خيارات التأثير مرقّم 13 وزر جزء الحركة مرقّم 14',
  'The Animations tab with the Effect Options button numbered 13 and the Animation Pane button numbered 14'),
],
9: [
 ('sec2021-ppt-09-insert',
  'تبويب «إدراج» وأدوات هذا المشروع: SmartArt (5)، و«مخطط» (11)، و«جدول» (13).',
  'The Insert tab and this project’s tools: SmartArt (5), Chart (11) and Table (13).',
  'تبويب إدراج في باوربوينت، وزر SmartArt مرقّم 5 وزر مخطط مرقّم 11 وزر جدول مرقّم 13',
  'The Insert tab with the SmartArt button numbered 5, Chart numbered 11 and Table numbered 13'),
 ('sec2021-ppt-09-autoplay',
  'للتشغيل التلقائي: ألغِ «عند النقر بالماوس»، وضع علامة أمام «بعد» وحدّد المدة، ثم «تطبيق على الكل» (خطوة 22).',
  'For automatic playback: clear On Mouse Click, tick After and set the duration, then Apply To All (step 22).',
  'مجموعة توقيت في تبويب انتقالات، وحقل بعد وزر تطبيق على الكل محاطان بإطارين ومرقّمان بالخطوة 22',
  'The Timing group with the After field and the Apply To All button framed and numbered step 22'),
 ('sec2021-ppt-09-setup',
  'زر «إعداد عرض الشرائح» في تبويب «عرض الشرائح» (خطوة 23) — ومنه «تنفيذ حلقة مستمرة حتى الضغط على Esc».',
  'The Set Up Slide Show button on the Slide Show tab (step 23) — where you find “Loop continuously until Esc”.',
  'زر إعداد عرض الشرائح في تبويب عرض الشرائح محاط بإطار ومرقّم بالخطوة 23',
  'The Set Up Slide Show button on the Slide Show tab framed and numbered step 23'),
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
        num = 'شكل ب%d.%d' % (n, i) if lang == 'ar' else 'Figure P%d.%d' % (n, i)
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
        m = re.search(r'id:\s*"p%d"' % n, s)
        if not m:
            print('تعذّر العثور على الوحدة p%d' % n); continue
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
        print('p%d: %d لقطة' % (n, len(MAPS[n])))
    io.open(path, 'w', encoding='utf-8').write(s)


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'content.js')
