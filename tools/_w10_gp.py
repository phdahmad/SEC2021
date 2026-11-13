#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""يضيف وحدة «وورد 10 — تقرير مشروع التخرج بنمط القسم» إلى content.js قبل وحدة الاستعداد للاختبار،
ويعيد ترقيم وحدة الاستعداد إلى w11، ويحدّث عدد وحدات مسار وورد في المقدمة، ويربط الوحدة الرابعة بالجديدة."""
import io, re

P = '/home/claude/sec2021/content.js'
TPL = 'files/SEC2021-graduation-project-template-APA7.docx'


def fig(name, alt, n, cap):
    return ('<figure class="fig ui"><img src="images/sec2021-%s.webp" alt="%s" loading="lazy">'
            '<figcaption><span class="n">%s</span> %s</figcaption></figure>' % (name, alt, n, cap))


def steps(items, start=0):
    s = '<ol class="lab-steps"%s>' % ((' style="counter-reset:ls %d"' % start) if start else '')
    for where, body in items:
        s += '<li><span class="where">%s</span>%s</li>' % (where, body)
    return s + '</ol>'


def part(t, first=False):
    return '<p style="font-weight:700;margin-block:%s;color:var(--ink)">%s</p>' % ('14px 8px' if first else '18px 8px', t)


sp = lambda t: '<span class="spec">%s</span>' % t
num = lambda t: '<span class="num">%s</span>' % t
term = lambda t: '<span class="term">(%s)</span>' % t
kbd = lambda t: '<span class="kbd">%s</span>' % t

# ======================================================================== العربية
AR1 = (
 '<p>تقرير مشروع التخرج أطول مستند ستكتبه في البرنامج: ثلاثون صفحة أو أكثر، يكتبه فريق، ويُنظر في شكله قبل أن يُقرأ محتواه. '
 'والقسم يعتمد له قالباً بأسلوب <strong>APA</strong> في إصداره السابع: خط واحد، وتباعد واحد، ومواصفات ثابتة للعناوين والجداول والمراجع. '
 'هذه الوحدة تحوّل تلك المواصفات إلى <strong>أنماط</strong> في وورد، فيلتزمها المستند وحده مهما طال، بدل أن تضبطها بيدك صفحةً صفحة.</p>'
 '<div class="box define"><span class="label">ما APA 7؟</span><p>دليل لأسلوب الكتابة العلمية تصدره الجمعية الأمريكية لعلم النفس '
 + term('American Psychological Association') +
 '، يحدّد شكل الصفحة والعناوين والجداول وطريقة الإحالة إلى المصادر، وتعتمده كثير من كليات الصحة. لا يُطلب منك حفظه: القالب يطبّقه، '
 'والمطلوب أن تفهم ما يفعله القالب لتحافظ عليه ولا تكسره.</p></div>'
 '<p><a class="btn btn-primary" href="' + TPL + '" download>حمّل قالب القسم (نسخة الطلبة) — Word</a></p>'
 '<p>هذه النسخة بشكل قالب القسم نفسه، وفيها تصحيحات صغيرة: سطر القسم صار قسم الإدارة الصحية والمستشفيات، و«العنوان 1» يبدأ صفحة جديدة وحده بدل الفواصل اليدوية، '
 'وعنوان الشكل فوقه كما في APA 7، وفيها نمطان جاهزان للتسمية التوضيحية والمراجع، ومثال لجدول ومثالان للمراجع.</p>'
 + fig('word-10-title', 'صفحة الغلاف في قالب مشروع التخرج: شعار الجامعة والعنوان والأسماء والقسم والكلية والجامعة، ورأس الصفحة بالعنوان المختصر ورقم الصفحة',
       'شكل و10.1', 'صفحة الغلاف في القالب: الشعار، والعنوان غامقاً في الوسط، ثم الأسماء والمقرر والمشرف والقسم والكلية والجامعة وتاريخ التسليم. وفي أعلاها رأس الصفحة: العنوان المختصر بأحرف كبيرة ورقم الصفحة.') +
 '<h3>مواصفات القالب: ما الذي يطلبه القسم؟</h3>'
 '<div class="table-wrap"><table><caption>مواصفات قالب مشروع التخرج (APA 7)</caption><thead><tr><th>العنصر</th><th>المواصفة</th><th>أين في وورد</th></tr></thead><tbody>'
 '<tr><td>الورق والهوامش</td><td>' + sp('Letter') + '، وهامش ' + num('2.54') + ' سم (بوصة) من كل جانب</td><td>تخطيط ← الحجم، الهوامش ← «عادي»</td></tr>'
 '<tr><td>الخط</td><td>' + sp('Times New Roman') + ' بحجم ' + num('12') + ' لكل شيء، والعناوين أيضاً</td><td>نمط «عادي»</td></tr>'
 '<tr><td>تباعد الأسطر</td><td>مزدوج في المستند كله، بلا تباعد قبل الفقرة ولا بعدها</td><td>نمط «عادي»</td></tr>'
 '<tr><td>بداية الفقرة</td><td>مسافة بادئة للسطر الأول ' + num('1.27') + ' سم (نصف بوصة)</td><td>نمط «عادي» ← خاصة: السطر الأول</td></tr>'
 '<tr><td>العنوان الرئيس</td><td>في الوسط، غامق، ويبدأ صفحة جديدة</td><td>نمط «العنوان 1»</td></tr>'
 '<tr><td>العنوان الفرعي</td><td>على اليسار، غامق؛ والذي تحته غامق مائل</td><td>«عنوان 2» و«عنوان 3»</td></tr>'
 '<tr><td>رأس الصفحة</td><td>العنوان المختصر بأحرف كبيرة يساراً، ورقم الصفحة يميناً، في كل الصفحات</td><td>إدراج ← الرأس، رقم الصفحة</td></tr>'
 '<tr><td>الجداول والأشكال</td><td>الرقم غامقاً فوقها، ثم العنوان مائلاً في السطر التالي</td><td>مراجع ← إدراج تسمية توضيحية</td></tr>'
 '<tr><td>المراجع</td><td>مرتّبة أبجدياً، بمسافة بادئة معلّقة ' + num('1.27') + ' سم</td><td>فقرة ← خاصة: معلّقة</td></tr>'
 '</tbody></table></div>'
 '<h3>ترتيب الأقسام</h3><p>كل قسم رئيس يبدأ صفحة جديدة، وبهذا الترتيب:</p>'
 '<ol><li><strong>Abstract</strong>: ملخص في فقرة واحدة، أقل من 250 كلمة، تتبعه الكلمات المفتاحية.</li>'
 '<li><strong>Introduction and Background</strong>: المشكلة وأهميتها، وما سبقها من دراسات، والفجوة، والأهداف.</li>'
 '<li><strong>Methodology</strong>: تصميم الدراسة ومكانها وعيّنتها وطريقة جمع البيانات وتحليلها والجوانب الأخلاقية، بعناوين فرعية.</li>'
 '<li><strong>Results</strong> ثم <strong>Discussion</strong> ثم <strong>Summary and Conclusion</strong>.</li>'
 '<li><strong>References</strong> ثم <strong>Appendix</strong>.</li></ol>'
 '<div class="box recall"><span class="label">المقترح والجزء الأول</span><p>في المقترح والجزء الأول من المشروع تكفي الأقسام حتى Methodology، ثم References وAppendix. أما Results وما بعدها فللجزء الثاني. والقالب ينبّه على ذلك بسطر أحمر قبل Results.</p></div>'
 '<h3>ثلاث أفكار يقوم عليها القالب</h3>'
 '<p><strong>أولاً: الشكل في النمط لا في النص.</strong> لا تختر الخط والتباعد من الشريط لكل فقرة. عدّل نمط «عادي» مرة واحدة فيتبعه كل النص، كما رأيت في <strong>وورد 4</strong>. '
 'وإن وصلتك فقرة من زميل بخط آخر، فطبّق عليها «عادي» تعد إلى المواصفات.</p>'
 '<p><strong>ثانياً: القسم يبدأ صفحة جديدة بخاصية، لا بالمفاتيح.</strong> لا تضغط ' + kbd('Enter') + ' مرات حتى تصل إلى صفحة جديدة، ولا تضع فاصل صفحة قبل كل قسم. '
 'فعّل «فاصل صفحات قبل» في نمط «العنوان 1»، فيبدأ كل قسم رئيس صفحته مهما زاد النص قبله أو نقص.</p>'
 '<p><strong>ثالثاً: الأرقام يولّدها وورد.</strong> رقم الصفحة حقل، ورقم الجدول ' + sp('Table 1') + ' حقل، والإحالة إليه في النص حقل. '
 'أضف جدولاً قبله يصِر ' + sp('Table 2') + ' وتتغيّر الإحالة معه. وإن لم تتحدّث الأرقام فحدّد الكل ' + kbd('Ctrl + A') + ' ثم اضغط ' + kbd('F9') + '.</p>'
 '<div class="box scenario"><span class="label">من واقع العمل</span><p>فريق من أربعة يكتب كل عضو فيه فصلاً في ملف مستقل، ثم تُجمع الفصول قبل التسليم: '
 'ملف بخط Calibri، وآخر بتباعد 1.5، وثالث كبّر صاحبه عناوينه بيده. فيقضي الفريق ليلة التسليم في توحيد الشكل. '
 'والحل أن يبدأ الجميع من القالب نفسه ويستعملوا الأنماط لا التنسيق المباشر، فإذا جُمعت الفصول توحّد شكلها وحده.</p></div>'
 '<div class="box warn"><span class="label">تنبيه العربي</span><p>التقرير بالإنجليزية ووورد بواجهة عربية، ومن هنا ثلاثة مزالق. '
 '<strong>الاتجاه:</strong> إن كان اتجاه الفقرة من اليمين، صار النص الإنجليزي محاذياً لليمين وقفزت النقطة والأقواس إلى غير مكانها؛ فاجعل «الاتجاه: اليسار لليمين» في نمط «عادي» نفسه (الخطوة 3)، لا في كل فقرة. '
 '<strong>الأرقام:</strong> إن ظهرت السنة ' + sp('٢٠٢٦') + ' بدل ' + sp('2026') + '، فمن ملف ← خيارات ← خيارات متقدمة اجعل «رقمي» «عربي» بدل «سياق» أو «هندي». '
 '<strong>الوحدات:</strong> مواصفات APA بالبوصة ووورد العربي يعرضها بالسنتيمتر: البوصة ' + num('2.54') + ' سم، ونصف البوصة ' + num('1.27') + ' سم.</p></div>'
)

AR_MAP = (
 '<h3>خريطة الأزرار: أين تجد ما ستحتاجه</h3><p>قبل أن تبدأ التمرين، هذه لقطات من وورد بواجهته العربية، والرقم في الدائرة هو رقم الخطوة التي يُستخدم فيها الزر.</p>'
 + fig('word-10-styles', 'معرض الأنماط في تبويب الشريط الرئيسي، والأنماط عادي والعنوان 1 وعنوان 2 محاطة بإطارات مرقّمة 2 و4 و6',
       'شكل و10.2', 'معرض «أنماط»: انقر بالزر الأيمن على النمط ثم «تعديل...» — «عادي» (2)، و«العنوان 1» (4)، و«عنوان 2» (6).')
 + fig('word-10-modify', 'نافذة تعديل النمط لنمط عادي، والخط Times New Roman بحجم 12 مرقّم 2، وزر تنسيق مرقّم 3',
       'شكل و10.3', 'نافذة «تعديل النمط»: الخط وحجمه (2)، وزر «تنسيق» أسفلها ومنه «فقرة...» (3).')
 + fig('word-10-paragraph', 'نافذة فقرة بتبويب المسافات البادئة والتباعد: المحاذاة يسار، والاتجاه من اليسار لليمين، وخاصة السطر الأول 1.27 سم، وتباعد الأسطر مزدوج',
       'شكل و10.4', 'نافذة «فقرة»: المحاذاة «يسار» (3)، والاتجاه «اليسار لليمين»، و«خاصة: السطر الأول» بمقدار 1.27 سم، و«تباعد الأسطر: مزدوج»، و«قبل» و«بعد» صفراً.')
 + fig('word-10-pagebreak', 'تبويب فواصل صفحات وأسطر في نافذة فقرة، ومربع فاصل صفحات قبل مفعّل ومرقّم 5',
       'شكل و10.5', 'تبويب «فواصل صفحات وأسطر» لنمط «العنوان 1»: مربع «فاصل صفحات قبل» (5).')
 + fig('word-10-nav', 'جزء التنقل يعرض عناوين التقرير من Abstract إلى Appendix، والقائمة محاطة بإطار مرقّم 9',
       'شكل و10.6', '«جزء التنقل» من تبويب «عرض»: كل عنوان أخذ نمطاً يظهر هنا (9). العنوان الفرعي يظهر تحت عنوانه الرئيس.')
 + fig('word-10-header-buttons', 'مجموعة رأس وتذييل في تبويب إدراج، وزر الرأس مرقّم 10 وزر رقم الصفحة مرقّم 11',
       'شكل و10.7', 'تبويب «إدراج» ← «رأس وتذييل»: «الرأس» (10)، و«رقم الصفحة» (11).')
 + fig('word-10-header-tab', 'تبويب رأس وتذييل الصفحة، ومربع صفحة أولى مختلفة مرقّم 12، وزر إغلاق الرأس والتذييل',
       'شكل و10.8', 'تبويب «رأس وتذييل الصفحة» الذي يظهر عند تحرير الرأس: «صفحة أولى مختلفة» يبقى غير مفعّل (12)، ثم «إغلاق الرأس والتذييل».')
 + fig('word-10-references', 'تبويب مراجع: زر إدراج تسمية توضيحية مرقّم 13، وإسناد ترافقي مرقّم 16، والنمط APA مرقّم 20',
       'شكل و10.9', 'تبويب «مراجع»: «إدراج تسمية توضيحية» (13)، و«إسناد ترافقي» (16)، و«النمط: APA» في مجموعة «المراجع والاقتباسات» (20).')
 + fig('word-10-caption', 'نافذة تسمية توضيحية، والوصف Table والموضع أعلى العنصر المحدد، والتسمية Table 1',
       'شكل و10.10', 'نافذة «تسمية توضيحية»: «الوصف» ' + sp('Table') + ' و«الموضع» «أعلى العنصر المحدد» (13).')
 + fig('word-10-table', 'جدول بأسلوب APA: Table 1 غامقاً، وتحته العنوان مائلاً، وثلاثة خطوط أفقية فقط، وملاحظة أسفل الجدول',
       'شكل و10.11', 'النتيجة المتوقعة: ' + sp('Table 1') + ' غامقاً (13)، والعنوان مائلاً في السطر التالي (14)، وجدول بثلاثة خطوط أفقية ولا خطوط رأسية.')
 + fig('word-10-hanging', 'نافذة فقرة لفقرة مرجع، وخاصة معلّقة بمقدار 1.27 سم مرقّمة 18',
       'شكل و10.12', 'نافذة «فقرة» لقائمة المراجع: «خاصة: معلّقة» بمقدار 1.27 سم (18).')
 + fig('word-10-refs-result', 'صفحة References في القالب: رأس الصفحة بالعنوان المختصر ورقم الصفحة، وفي أسفلها مرجعان بمسافة بادئة معلّقة',
       'شكل و10.13', 'النتيجة المتوقعة: رأس الصفحة في أعلاها، والمراجع في أسفلها؛ السطر الأول من المرجع على الهامش والأسطر التالية مزاحة.')
)

W1 = 'World Health Organization. (2020). <em>WHO guidelines on physical activity and sedentary behaviour</em>. https://www.who.int/publications/i/item/9789240015128'
W2 = 'American Psychological Association. (2020). <em>Publication manual of the American Psychological Association</em> (7th ed.). https://doi.org/10.1037/0000165-000'

AR_LAB = (
 '<div class="lab"><div class="lab-head"><span class="tag">تمرين 10</span><span>تقرير مشروع التخرج بنمط القسم</span></div><div class="lab-body">'
 '<p class="goal">الهدف: تبني هيكل تقرير مشروع تخرج من مستند فارغ بمواصفات قالب القسم، ثم تقارن نتيجتك بالقالب. موضوع التدريب: ' + sp('Sleep Habits of University Students in Makkah') + '.</p>'
 + part('أولاً: الصفحة ونمط النص', True) + steps([
  ('ملف ثم تخطيط', 'أنشئ مستنداً فارغاً واحفظه باسم ' + sp('مشروع التخرج - تدريب.docx') + '. ثم من «تخطيط» اجعل «الحجم» ' + sp('Letter') + ' و«الهوامش» <strong>«عادي»</strong>.'),
  ('الشريط الرئيسي ← أنماط', 'انقر بالزر الأيمن على نمط <strong>«عادي»</strong> واختر <strong>«تعديل...»</strong>. واجعل الخط ' + sp('Times New Roman') + ' والحجم ' + num('12') + '.'),
  ('تعديل النمط ← تنسيق', 'انقر «تنسيق» ← <strong>«فقرة...»</strong>، واضبط: المحاذاة «يسار»، والاتجاه <strong>«اليسار لليمين»</strong>، و«خاصة: السطر الأول» بمقدار ' + num('1.27') + ' سم، و«تباعد الأسطر: مزدوج»، و«قبل» و«بعد» صفراً. ثم «موافق» في النافذتين.'),
 ])
 + part('ثانياً: العناوين') + steps([
  ('أنماط', 'عدّل <strong>«العنوان 1»</strong> بالطريقة نفسها: ' + sp('Times New Roman') + ' ' + num('12') + ' غامق بلون أسود، في الوسط. ومن «تنسيق ← فقرة» اجعل «خاصة» <strong>«(بلا)»</strong> حتى لا ينزاح العنوان عن الوسط.'),
  ('فقرة ← فواصل صفحات وأسطر', 'في نافذة الفقرة نفسها انتقل إلى تبويب «فواصل صفحات وأسطر» وفعّل <strong>«فاصل صفحات قبل»</strong>.'),
  ('أنماط', 'عدّل <strong>«عنوان 2»</strong>: ' + sp('Times New Roman') + ' ' + num('12') + ' غامق أسود، بمحاذاة يسار، و«خاصة: (بلا)».'),
 ], 3)
 + part('ثالثاً: الهيكل') + steps([
  ('لوحة المفاتيح', 'اكتب صفحة الغلاف، كل سطر في فقرة: عنوان المشروع غامقاً، ثم ' + sp('Name of students') + ' و' + sp('Course Name &amp; Number') + ' و' + sp('Supervisor') + '، ثم ' + sp('Department of Health Administration and Hospitals') + ' و' + sp('College of Public Health and Health Informatics') + ' و' + sp('Umm Al-Qura University') + ' وتاريخ التسليم. حدّدها كلها واجعلها في الوسط، و«خاصة: (بلا)».'),
  ('أنماط', 'اكتب بعدها عناوين الأقسام بالترتيب وطبّق على كل منها <strong>«العنوان 1»</strong>: Abstract، Introduction and Background، Methodology، Results، Discussion، Summary and Conclusion، References، Appendix. وتحت Methodology ثلاثة عناوين بنمط <strong>«عنوان 2»</strong>: Study Design، Data Collection Methods، Data Analysis. واكتب تحت كل عنوان سطراً تجريبياً. النتيجة المتوقعة: انتقل Abstract إلى صفحة جديدة وحده، وكذلك كل عنوان رئيس، بلا أي فاصل يدوي.'),
  ('عرض', 'فعّل <strong>«جزء التنقل»</strong>: يجب أن ترى الأقسام الثمانية، وتحت Methodology عناوينه الثلاثة. العنوان الذي لا يظهر هنا لم يأخذ نمط عنوان.'),
 ], 6)
 + part('رابعاً: رأس الصفحة') + steps([
  ('إدراج ← رأس وتذييل', 'انقر <strong>«الرأس»</strong> ← «فارغ»، واكتب العنوان المختصر بأحرف كبيرة ' + sp('SLEEP HABITS OF UNIVERSITY STUDENTS') + '، ثم اضغط ' + kbd('Tab') + ' مرتين لينتقل المؤشر إلى أقصى اليمين. وإن ظهر الرأس مزاحاً أو متباعد الأسطر فهو يرث «عادي»: اجعل لفقرته «خاصة: (بلا)» و«تباعد الأسطر: مفرد».'),
  ('إدراج ← رأس وتذييل', 'انقر <strong>«رقم الصفحة»</strong> ← «الموضع الحالي» ← «رقم عادي».'),
  ('رأس وتذييل الصفحة', 'تأكد أن <strong>«صفحة أولى مختلفة»</strong> غير مفعّل، لأن رأس القسم يظهر في الغلاف أيضاً. ثم «إغلاق الرأس والتذييل»، وقلّب الصفحات وتأكد أن الأرقام متسلسلة من ' + num('1') + '.'),
 ], 9)
 + part('خامساً: جدول بأسلوب APA') + steps([
  ('مراجع ← تسميات توضيحية', 'ضع المؤشر في سطر فارغ تحت Results، ثم <strong>«إدراج تسمية توضيحية»</strong>: «الوصف» ' + sp('Table') + '، و«الموضع» «أعلى العنصر المحدد»، ثم «موافق». فيظهر ' + sp('Table 1') + '.'),
  ('أنماط', 'يظهر ' + sp('Table 1') + ' صغيراً مائلاً ملوّناً، وهذا شكل نمط «تسمية توضيحية» الافتراضي. افتح جزء الأنماط ' + kbd('Ctrl + Alt + Shift + S') + '، وانقر السهم بجوار «تسمية توضيحية» ← «تعديل...»، واجعله ' + sp('Times New Roman') + ' ' + num('12') + ' غامقاً غير مائل بلون أسود. ثم اضغط ' + kbd('Enter') + ' بعده واكتب العنوان مائلاً بلا مسافة بادئة: ' + sp('Sleep Duration by Gender') + '.'),
  ('إدراج ← جدول', 'أدرج تحت العنوان جدولاً من ' + num('3') + ' أعمدة و' + num('3') + ' صفوف: ' + sp('Gender') + ' و' + sp('n') + ' و' + sp('%') + '، ثم ' + sp('Female') + ' و' + sp('Male') + '. حدّد الجدول، ومن «الشريط الرئيسي ← حدود» اختر «بلا حدود»، ثم «حد علوي» و«حد سفلي». ثم حدّد الصف الأول وأضف له «حد سفلي». هذا شكل جدول APA: ثلاثة خطوط أفقية ولا خطوط رأسية.'),
  ('مراجع ← تسميات توضيحية', 'في سطر قبل الجدول اكتب ' + sp('As shown in') + ' ثم انقر <strong>«إسناد ترافقي»</strong>: «نوع المرجع» ' + sp('Table') + '، و«إدراج مرجع إلى» «التسمية والرقم فقط»، ثم «إدراج». فتصير الجملة ' + sp('As shown in Table 1') + '، ويتحدّث الرقم وحده إن تغيّر.'),
 ], 12)
 + part('سادساً: المراجع والتسليم') + steps([
  ('الشريط الرئيسي ← فقرة', 'تحت References اكتب المرجعين بهذا الترتيب، كلاً في فقرة، وعنوان الكتاب مائلاً:<br>' + W1 + '<br>' + W2 + '<br>ثم حدّدهما وانقر <strong>«فرز»</strong> تصاعدياً، فيتقدّم American على World.'),
  ('فقرة', 'مع بقاء التحديد افتح نافذة «فقرة» واجعل <strong>«خاصة: معلّقة»</strong> بمقدار ' + num('1.27') + ' سم. يبقى السطر الأول من كل مرجع على الهامش، وتنزاح الأسطر التالية.'),
  ('ملف', 'احفظ المستند ثم احفظ نسخة PDF. افتح قالب القسم وقارن: الغلاف، ورأس الصفحة، وبداية كل قسم، والجدول، والمراجع.'),
  ('مراجع', '<strong>إضافة:</strong> تأكد أن «النمط» ' + sp('APA') + '، ثم «إدراج اقتباس» ← «إضافة مصدر جديد» وأدخل بيانات مصدر، ثم «المراجع» لإدراج قائمة مراجع تلقائية تُحدَّث كلما أضفت مصدراً.'),
  ('ملف ← حفظ باسم', '<strong>إضافة:</strong> احفظ نسختك باسم ' + sp('قالب الفريق') + ' واختر النوع «قالب Word» ' + sp('.dotx') + '. يفتح منه كل عضو في الفريق مستنداً جديداً بالأنماط نفسها.'),
 ], 16)
 + '</div></div>'
)

AR_END = ('<h3>خلاصة الوحدة</h3><p>مواصفات القسم تُكتب مرة واحدة في الأنماط: «عادي» للنص، و«العنوان 1» يبدأ كل قسم صفحة جديدة، والتسمية التوضيحية لأرقام الجداول. '
          'وما بعد ذلك يولّده وورد: أرقام الصفحات والجداول والإحالات وجزء التنقل. ابدأ مشروعك من القالب، واكتب، ودع الأنماط تحفظ الشكل.</p>')

# ======================================================================== English
EN1 = (
 '<p>The graduation project report is the longest document you will write in the programme: thirty pages or more, written by a team, and judged on its look before its content is read. '
 'The department sets an <strong>APA</strong> 7th edition template for it: one font, one line spacing, and fixed rules for headings, tables, and references. '
 'This unit turns those rules into Word <strong>styles</strong>, so the document keeps them by itself however long it grows, instead of you fixing them page by page.</p>'
 '<div class="box define"><span class="label">What is APA 7?</span><p>A scientific writing style guide published by the American Psychological Association. '
 'It sets the page layout, headings, tables, and how sources are cited, and many health colleges adopt it. You do not need to memorise it: the template applies it. '
 'You need to understand what the template does so you keep it intact.</p></div>'
 '<p><a class="btn btn-primary" href="' + TPL + '" download>Download the department template (student copy) — Word</a></p>'
 '<p>This copy looks exactly like the department template, with small corrections: the department line now reads Health Administration and Hospitals, '
 'Heading 1 starts a new page by itself instead of manual breaks, the figure title sits above the figure as in APA 7, and it adds ready styles for captions and references, a sample table, and two sample references.</p>'
 + fig('word-10-title', 'The template title page: university logo, title, names, department, college, university, and a header with the short title and page number',
       'Figure W10.1', 'The template title page: the logo, the title in bold and centred, then the names, course, supervisor, department, college, university, and due date. At the top is the page header: the short title in capitals and the page number.') +
 '<h3>The template rules: what the department asks for</h3>'
 '<div class="table-wrap"><table><caption>Graduation project template rules (APA 7)</caption><thead><tr><th>Element</th><th>Rule</th><th>Where in Word</th></tr></thead><tbody>'
 '<tr><td>Paper and margins</td><td>Letter, 1 inch (2.54 cm) on every side</td><td>Layout, Size; Margins, Normal</td></tr>'
 '<tr><td>Font</td><td>Times New Roman 12 for everything, headings included</td><td>Normal style</td></tr>'
 '<tr><td>Line spacing</td><td>Double throughout, no space before or after paragraphs</td><td>Normal style</td></tr>'
 '<tr><td>Paragraph start</td><td>First-line indent of 0.5 inch (1.27 cm)</td><td>Normal style, Special: First line</td></tr>'
 '<tr><td>Main heading</td><td>Centred, bold, starts a new page</td><td>Heading 1 style</td></tr>'
 '<tr><td>Subheading</td><td>Flush left, bold; the level below is bold italic</td><td>Heading 2 and Heading 3</td></tr>'
 '<tr><td>Page header</td><td>Short title in capitals on the left, page number on the right, on every page</td><td>Insert, Header, Page Number</td></tr>'
 '<tr><td>Tables and figures</td><td>Number in bold above, then the title in italics on the next line</td><td>References, Insert Caption</td></tr>'
 '<tr><td>References</td><td>Alphabetical, with a 0.5 inch (1.27 cm) hanging indent</td><td>Paragraph, Special: Hanging</td></tr>'
 '</tbody></table></div>'
 '<h3>Order of sections</h3><p>Each main section starts a new page, in this order:</p>'
 '<ol><li><strong>Abstract</strong>: one paragraph under 250 words, followed by keywords.</li>'
 '<li><strong>Introduction and Background</strong>: the problem and why it matters, previous studies, the gap, and the objectives.</li>'
 '<li><strong>Methodology</strong>: design, setting, sample, data collection, analysis, and ethics, under subheadings.</li>'
 '<li><strong>Results</strong>, then <strong>Discussion</strong>, then <strong>Summary and Conclusion</strong>.</li>'
 '<li><strong>References</strong>, then <strong>Appendix</strong>.</li></ol>'
 '<div class="box recall"><span class="label">The proposal and part one</span><p>For the proposal and the first part of the project, the sections up to Methodology are enough, followed by References and Appendix. Results onwards belong to part two. The template marks this with a red line before Results.</p></div>'
 '<h3>Three ideas the template rests on</h3>'
 '<p><strong>First: the look lives in the style, not in the text.</strong> Do not pick the font and spacing from the ribbon for each paragraph. Modify the Normal style once and all text follows, as you saw in <strong>Word 4</strong>. '
 'If a teammate sends you a paragraph in another font, apply Normal to it and it returns to the rules.</p>'
 '<p><strong>Second: a section starts a new page through a setting, not keystrokes.</strong> Do not press ' + kbd('Enter') + ' repeatedly to reach a new page, and do not put a page break before every section. '
 'Turn on "Page break before" in the Heading 1 style, and every main section starts its own page however much text comes before it.</p>'
 '<p><strong>Third: Word generates the numbers.</strong> The page number is a field, the table number ' + sp('Table 1') + ' is a field, and the reference to it in the text is a field. '
 'Add a table before it and it becomes ' + sp('Table 2') + ', with the reference following. If numbers do not refresh, select all with ' + kbd('Ctrl + A') + ' and press ' + kbd('F9') + '.</p>'
 '<div class="box scenario"><span class="label">From working life</span><p>A team of four writes one chapter each in separate files, then merges them before submission: '
 'one file in Calibri, another at 1.5 spacing, a third whose author enlarged the headings by hand. The team spends the night before the deadline making it consistent. '
 'The fix is for everyone to start from the same template and use styles rather than direct formatting, so the merged chapters line up by themselves.</p></div>'
 '<div class="box warn"><span class="label">Arabic note</span><p>The report is in English but Word has an Arabic interface, which brings three pitfalls. '
 '<strong>Direction:</strong> if the paragraph runs right to left, English text aligns right and full stops and brackets jump to the wrong place; set "Direction: Left-to-right" in the Normal style itself (step 3), not paragraph by paragraph. '
 '<strong>Digits:</strong> if the year shows as ' + sp('٢٠٢٦') + ' instead of ' + sp('2026') + ', go to File, Options, Advanced and set Numeral to "Arabic" rather than "Context" or "Hindi". '
 '<strong>Units:</strong> APA rules are in inches while Arabic Word shows centimetres: one inch is 2.54 cm and half an inch is 1.27 cm.</p></div>'
)

EN_MAP = (
 '<h3>Button map: where to find what you need</h3><p>Before starting the exercise, here are screenshots of Word in its Arabic interface. The number in each circle is the step where that button is used.</p>'
 + fig('word-10-styles', 'The Styles gallery on the Home tab, with Normal, Heading 1, and Heading 2 framed and numbered 2, 4, and 6',
       'Figure W10.2', 'The Styles gallery: right-click a style, then Modify — Normal (2), Heading 1 (4), and Heading 2 (6).')
 + fig('word-10-modify', 'The Modify Style dialog for Normal, with Times New Roman 12 numbered 2 and the Format button numbered 3',
       'Figure W10.3', 'The Modify Style dialog: font and size (2), and the Format button at the bottom, which leads to Paragraph (3).')
 + fig('word-10-paragraph', 'The Paragraph dialog on Indents and Spacing: alignment Left, direction left-to-right, Special First line 1.27 cm, line spacing Double',
       'Figure W10.4', 'The Paragraph dialog: alignment Left (3), direction Left-to-right, Special: First line by 1.27 cm, Line spacing: Double, and Before and After at zero.')
 + fig('word-10-pagebreak', 'The Line and Page Breaks tab with Page break before ticked and numbered 5',
       'Figure W10.5', 'The Line and Page Breaks tab for Heading 1: the "Page break before" box (5).')
 + fig('word-10-nav', 'The Navigation Pane listing the report headings from Abstract to Appendix, framed and numbered 9',
       'Figure W10.6', 'The Navigation Pane from the View tab: every heading that has a style appears here (9), with subheadings under their main heading.')
 + fig('word-10-header-buttons', 'The Header and Footer group on the Insert tab, with Header numbered 10 and Page Number numbered 11',
       'Figure W10.7', 'Insert tab, Header and Footer: Header (10) and Page Number (11).')
 + fig('word-10-header-tab', 'The Header and Footer tab with the Different First Page box numbered 12 and the Close Header and Footer button',
       'Figure W10.8', 'The Header and Footer tab shown while editing the header: "Different First Page" stays unticked (12), then Close Header and Footer.')
 + fig('word-10-references', 'The References tab: Insert Caption numbered 13, Cross-reference numbered 16, and Style APA numbered 20',
       'Figure W10.9', 'The References tab: Insert Caption (13), Cross-reference (16), and Style: APA in the Citations and Bibliography group (20).')
 + fig('word-10-caption', 'The Caption dialog with label Table, position Above selected item, and caption Table 1',
       'Figure W10.10', 'The Caption dialog: label ' + sp('Table') + ' and position "Above selected item" (13).')
 + fig('word-10-table', 'An APA table: Table 1 in bold, the title in italics below it, only three horizontal lines, and a note under the table',
       'Figure W10.11', 'Expected result: ' + sp('Table 1') + ' in bold (13), the title in italics on the next line (14), and a table with three horizontal lines and no vertical ones.')
 + fig('word-10-hanging', 'The Paragraph dialog for a reference paragraph, with Special Hanging by 1.27 cm numbered 18',
       'Figure W10.12', 'The Paragraph dialog for the reference list: Special: Hanging by 1.27 cm (18).')
 + fig('word-10-refs-result', 'The References page in the template: the header with short title and page number, and two references with a hanging indent at the bottom',
       'Figure W10.13', 'Expected result: the page header at the top and the references at the bottom; the first line of each reference sits at the margin and later lines are indented.')
)

EN_LAB = (
 '<div class="lab"><div class="lab-head"><span class="tag">Exercise 10</span><span>The graduation project report in department style</span></div><div class="lab-body">'
 '<p class="goal">Goal: build the skeleton of a graduation project report from a blank document using the department template rules, then compare your result with the template. Practice topic: ' + sp('Sleep Habits of University Students in Makkah') + '.</p>'
 + part('First: the page and the text style', True) + steps([
  ('File, then Layout', 'Create a blank document and save it as ' + sp('Graduation project - practice.docx') + '. On Layout, set Size to ' + sp('Letter') + ' and Margins to <strong>Normal</strong>.'),
  ('Home, Styles', 'Right-click the <strong>Normal</strong> style and choose <strong>Modify</strong>. Set the font to ' + sp('Times New Roman') + ' and the size to ' + num('12') + '.'),
  ('Modify Style, Format', 'Click Format, then <strong>Paragraph</strong>, and set: alignment Left, direction <strong>Left-to-right</strong>, Special: First line by ' + num('1.27') + ' cm, Line spacing: Double, and Before and After at zero. Click OK in both dialogs.'),
 ])
 + part('Second: headings') + steps([
  ('Styles', 'Modify <strong>Heading 1</strong> the same way: ' + sp('Times New Roman') + ' ' + num('12') + ', bold, black, centred. Under Format, Paragraph, set Special to <strong>(none)</strong> so the heading stays centred.'),
  ('Paragraph, Line and Page Breaks', 'In the same Paragraph dialog, open the Line and Page Breaks tab and tick <strong>Page break before</strong>.'),
  ('Styles', 'Modify <strong>Heading 2</strong>: ' + sp('Times New Roman') + ' ' + num('12') + ', bold, black, aligned left, Special: (none).'),
 ], 3)
 + part('Third: the structure') + steps([
  ('Keyboard', 'Type the title page, one line per paragraph: the project title in bold, then ' + sp('Name of students') + ', ' + sp('Course Name &amp; Number') + ', ' + sp('Supervisor') + ', then ' + sp('Department of Health Administration and Hospitals') + ', ' + sp('College of Public Health and Health Informatics') + ', ' + sp('Umm Al-Qura University') + ', and the due date. Select them all, centre them, and set Special: (none).'),
  ('Styles', 'Below them type the section headings in order and apply <strong>Heading 1</strong> to each: Abstract, Introduction and Background, Methodology, Results, Discussion, Summary and Conclusion, References, Appendix. Under Methodology add three <strong>Heading 2</strong> headings: Study Design, Data Collection Methods, Data Analysis. Type one sample line under each heading. Expected result: Abstract moved to a new page by itself, as did every main heading, with no manual break.'),
  ('View', 'Turn on the <strong>Navigation Pane</strong>: you should see the eight sections, with the three subheadings under Methodology. A heading that does not appear here has no heading style.'),
 ], 6)
 + part('Fourth: the page header') + steps([
  ('Insert, Header and Footer', 'Click <strong>Header</strong>, then Blank, and type the short title in capitals ' + sp('SLEEP HABITS OF UNIVERSITY STUDENTS') + '. Press ' + kbd('Tab') + ' twice to move the cursor to the far right. If the header looks indented or double spaced, it is inheriting Normal: give its paragraph Special: (none) and Line spacing: Single.'),
  ('Insert, Header and Footer', 'Click <strong>Page Number</strong>, then Current Position, then Plain Number.'),
  ('Header and Footer', 'Check that <strong>Different First Page</strong> is unticked, because the department header appears on the title page too. Then Close Header and Footer, page through, and check that numbering runs from ' + num('1') + '.'),
 ], 9)
 + part('Fifth: an APA table') + steps([
  ('References, Captions', 'Put the cursor on an empty line under Results, then <strong>Insert Caption</strong>: label ' + sp('Table') + ', position "Above selected item", then OK. ' + sp('Table 1') + ' appears.'),
  ('Styles', sp('Table 1') + ' appears small, italic, and coloured: the default look of the Caption style. Open the Styles pane with ' + kbd('Ctrl + Alt + Shift + S') + ', click the arrow next to Caption, then Modify, and set ' + sp('Times New Roman') + ' ' + num('12') + ', bold, not italic, black. Then press ' + kbd('Enter') + ' after it and type the title in italics with no indent: ' + sp('Sleep Duration by Gender') + '.'),
  ('Insert, Table', 'Insert a table of ' + num('3') + ' columns and ' + num('3') + ' rows under the title: ' + sp('Gender') + ', ' + sp('n') + ', ' + sp('%') + ', then ' + sp('Female') + ' and ' + sp('Male') + '. Select the table and from Home, Borders choose No Border, then Top Border and Bottom Border. Then select the first row and add a Bottom Border. This is the APA table look: three horizontal lines and no vertical ones.'),
  ('References, Captions', 'On a line before the table type ' + sp('As shown in') + ', then click <strong>Cross-reference</strong>: reference type ' + sp('Table') + ', insert reference to "Only label and number", then Insert. The sentence becomes ' + sp('As shown in Table 1') + ', and the number updates by itself if it changes.'),
 ], 12)
 + part('Sixth: references and submission') + steps([
  ('Home, Paragraph', 'Under References type these two entries in this order, one per paragraph, with the book title in italics:<br>' + W1 + '<br>' + W2 + '<br>Then select both and click <strong>Sort</strong> ascending, so American comes before World.'),
  ('Paragraph', 'With them still selected, open the Paragraph dialog and set <strong>Special: Hanging</strong> by ' + num('1.27') + ' cm. The first line of each reference stays at the margin and the following lines are indented.'),
  ('File', 'Save the document, then save a PDF copy. Open the department template and compare: title page, header, the start of each section, the table, and the references.'),
  ('References', '<strong>Extra:</strong> check that Style is ' + sp('APA') + ', then Insert Citation, Add New Source, and enter a source; then Bibliography to insert an automatic reference list that updates whenever you add a source.'),
  ('File, Save As', '<strong>Extra:</strong> save your copy as ' + sp('Team template') + ' with the type Word Template ' + sp('.dotx') + '. Every team member opens a new document from it with the same styles.'),
 ], 16)
 + '</div></div>'
)

EN_END = ('<h3>Unit summary</h3><p>The department rules are written once, into styles: Normal for the text, Heading 1 starting each section on a new page, and Caption for table numbers. '
          'Word generates the rest: page numbers, table numbers, cross-references, and the Navigation Pane. Start your project from the template, write, and let the styles hold the look.</p>')


def js(s):
    return s.replace('\\', '\\\\').replace('"', '\\"')


def section():
    return ('{\n      id: "w10", track: "word",\n'
            '      title: { ar: "وورد 10 — تقرير مشروع التخرج بنمط القسم", en: "Word 10 — The graduation project report in department style" },\n'
            '      html: {\n'
            '        ar: "' + js(AR1) + '" +\n            "' + js(AR_MAP + AR_LAB) + '" +\n            "' + js(AR_END) + '",\n'
            '        en: "' + js(EN1) + '" +\n            "' + js(EN_MAP + EN_LAB) + '" +\n            "' + js(EN_END) + '"\n'
            '      }\n    },\n    ')


def main():
    t = io.open(P, encoding='utf-8').read()
    assert 'graduation project report in department style' not in t, 'already applied'
    old = 'id: "w10", track: "word",'
    assert t.count(old) == 1
    i = t.index(old)
    j = t.rfind('{', 0, i)
    t = t[:i] + t[i:].replace(old, 'id: "w11", track: "word",', 1)
    t = t[:j] + section() + t[j:]
    # عدد وحدات وورد في مقدمة المسار
    a = '<strong>Word</strong> عشر وحدات تبدأ من فتح البرنامج وتنتهي بالحماية وكلمة المرور.'
    b = '<strong>Word</strong> إحدى عشرة وحدة تبدأ من فتح البرنامج وتنتهي بتقرير مشروع التخرج بنمط القسم.'
    assert t.count(js(a)) == 1, 'intro ar'
    t = t.replace(js(a), js(b))
    a = '<strong>Word</strong>: ten units from opening the program to passwords and protection.'
    b = '<strong>Word</strong>: eleven units from opening the program to the graduation project report in department style.'
    assert t.count(js(a)) == 1, 'intro en'
    t = t.replace(js(a), js(b))
    # ربط وورد 4 بالوحدة الجديدة
    a = 'وفاصل المقطع هو ما يسمح لمستند واحد أن يحمل إعدادات صفحات مختلفة.</p>'
    b = a[:-4] + ' وفي <strong>وورد 10</strong> تطبّق هذا كله على تقرير مشروع تخرجك بنمط القسم.</p>'
    assert t.count(js(a)) == 1, 'w4 ar'
    t = t.replace(js(a), js(b))
    a = 'And a section break is what lets one document carry different page settings.</p>'
    b = a[:-4] + ' In <strong>Word 10</strong> you apply all of this to your graduation project report in department style.</p>'
    assert t.count(js(a)) == 1, 'w4 en'
    t = t.replace(js(a), js(b))
    io.open(P, 'w', encoding='utf-8').write(t)
    print('ok')


if __name__ == '__main__':
    main()
