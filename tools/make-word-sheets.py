#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""يولّد أوراق تمارين وورد PDF من المحتوى نفسه — مصدر واحد للحقيقة.
   RTL مضبوط كخاصية على <html> والقوائم والجداول، بلا أي حيلة نصية."""
import json, pathlib, re, subprocess, sys

DIR = pathlib.Path(__file__).parent
OUT = DIR / "_sheets2"
OUT.mkdir(exist_ok=True)
data = json.loads((DIR / "_exercises.json").read_text(encoding="utf-8"))
C = data["course"]

CSS = """
@page { size: A4; margin: 22mm 18mm 20mm; }
*,*::before,*::after{box-sizing:border-box}
html{ direction: rtl; }
body{
  margin:0; font-family:"Saudi Text","Noto Naskh Arabic",Tahoma,Arial,sans-serif;
  font-size:11.5pt; line-height:1.85; color:#16202E; direction:rtl; text-align:right;
}
h1,h2,h3{ font-family:"Saudi","Noto Kufi Arabic",Tahoma,sans-serif; color:#0E2340; margin:0 }

/* ترويسة الورقة */
.sheet-head{
  border-bottom:3px solid #C8761A; padding-bottom:10px; margin-bottom:6px;
  display:flex; align-items:flex-end; gap:12px;
}
.sheet-head .code{
  font-family:"Courier New",monospace; font-size:9pt; letter-spacing:.06em;
  color:#A85F0E; direction:ltr; unicode-bidi:isolate;
}
.sheet-head .course{ font-size:9.5pt; color:#53606F; }
.sheet-head .spacer{ flex:1 }
.sheet-head .unit{
  background:#17355C; color:#fff; border-radius:999px; padding:3px 14px;
  font-size:9.5pt; font-family:"Courier New",monospace; direction:ltr; unicode-bidi:isolate;
}
h1.sheet-title{ font-size:17pt; margin:10px 0 4px; }
.sheet-sub{ font-size:10pt; color:#53606F; margin-bottom:12px }

/* خانات الطالب */
.student{
  display:flex; gap:10px; margin:12px 0 16px; font-size:9.5pt; color:#53606F;
}
.student > div{ flex:1; border-bottom:1px dotted #9AA6B4; padding-bottom:3px }

/* صندوق الهدف */
.goal{
  background:#F1EEE6; border-right:4px solid #17355C; border-radius:6px;
  padding:9px 13px; margin-bottom:14px; font-size:10.5pt;
}
.goal b{ color:#0E2340 }

/* الخطوات: ترقيم حقيقي عبر <ol> */
ol.steps{
  counter-reset:st; list-style:none; margin:0 0 4px; padding:0;
}
ol.steps > li{
  counter-increment:st; position:relative;
  padding-right:34px; margin-bottom:9px;
  break-inside:avoid; page-break-inside:avoid;
}
ol.steps > li::before{
  content:counter(st); position:absolute; right:0; top:1px;
  width:23px; height:23px; border-radius:50%;
  background:#17355C; color:#fff; text-align:center; line-height:23px;
  font-family:"Courier New",monospace; font-size:9pt;
}
.where{
  display:inline-block; font-size:8.5pt; color:#53606F;
  background:#F1EEE6; border:1px solid #DCD7CB; border-radius:4px;
  padding:0 7px; margin-left:7px;
}
.phase{
  font-family:"Saudi","Noto Kufi Arabic",sans-serif; font-weight:700;
  color:#17355C; font-size:11.5pt; margin:16px 0 8px;
  border-bottom:1px solid #DCD7CB; padding-bottom:4px;
}
.kbd{
  display:inline-block; direction:ltr; unicode-bidi:isolate;
  font-family:"Courier New",monospace; font-size:9pt;
  background:#F1EEE6; border:1px solid #DCD7CB; border-bottom-width:2px;
  border-radius:4px; padding:0 6px; color:#0E2340;
}
.num{ direction:ltr; unicode-bidi:isolate; font-family:"Courier New",monospace; font-size:9.5pt }
/* plaintext: الاتجاه يُحدَّد من أول حرف قوي — فاللاتيني LTR والعربي RTL */
.spec{ unicode-bidi:plaintext; font-family:"Courier New","Saudi Text","Noto Naskh Arabic",Tahoma; font-size:10pt }
.term{
  direction:ltr; unicode-bidi:isolate; font-family:"Courier New",monospace;
  font-size:9pt; background:#F1EEE6; border:1px solid #DCD7CB;
  border-radius:4px; padding:0 5px; white-space:nowrap;
}
/* النص المقتبس للكتابة */
.doc-text{
  background:#F1EEE6; border-right:3px solid #31558A; border-radius:5px;
  padding:9px 12px; margin:8px 0; font-size:10.5pt;
  direction:rtl; text-align:right; unicode-bidi:isolate;
  break-inside:avoid; page-break-inside:avoid;
}
.doc-text .lbl{
  display:block; font-size:8.5pt; color:#53606F; margin-bottom:3px;
  font-family:"Courier New",monospace; direction:ltr; unicode-bidi:isolate;
}
.doc-text.en{
  direction:ltr; text-align:left; border-right:none; border-left:3px solid #31558A;
  font-family:"Segoe UI",Arial,sans-serif; unicode-bidi:isolate;
}
/* تنبيه العربي */
.warn{
  border:1px solid #C8761A; border-right-width:4px; border-radius:6px;
  background:#FBF4EA; padding:10px 13px; margin-top:16px; font-size:10.5pt;
  break-inside:avoid; page-break-inside:avoid;
}
.warn .lbl{
  display:block; font-family:"Saudi","Noto Kufi Arabic",sans-serif;
  font-weight:700; color:#A85F0E; margin-bottom:4px; font-size:10.5pt;
}
.warn p{ margin:0 }
/* قائمة تحقق */
.check{ margin-top:16px; break-inside:avoid; page-break-inside:avoid }
.check .lbl{
  font-family:"Saudi","Noto Kufi Arabic",sans-serif; font-weight:700;
  color:#0E2340; font-size:11pt; margin-bottom:6px; display:block;
}
ul.check-list{ list-style:none; margin:0; padding:0; font-size:10.5pt }
ul.check-list > li{ position:relative; padding-right:26px; margin-bottom:5px }
ul.check-list > li::before{
  content:""; position:absolute; right:0; top:4px;
  width:13px; height:13px; border:1.5px solid #53606F; border-radius:3px;
}
/* لقطات الشاشة في الورقة */
figure.fig{ margin:10px 0; break-inside:avoid; page-break-inside:avoid; text-align:center }
figure.fig img{ max-width:100%; width:auto; border:1px solid #DCD7CB; border-radius:5px }
figure.fig figcaption{
  margin-top:5px; font-size:9pt; color:#53606F; text-align:right;
}
figure.fig figcaption .n{ font-family:"Courier New",monospace; color:#A85F0E; margin-left:5px }
.map-head{
  font-family:"Saudi","Noto Kufi Arabic",sans-serif; font-weight:700;
  color:#17355C; font-size:12pt; margin:4px 0 8px;
}
strong{ color:#0E2340 }
em{ font-style:italic }
p{ margin:0 0 8px }
ul:not(.check-list){ padding-right:1.4em; padding-left:0; margin:6px 0 }
"""

CHECKS = {
 1: ["كتبت الفقرات الأربع كاملة (أ، ب، ج، د)",
     "الفقرتان العربيتان اتجاههما من اليمين إلى اليسار",
     "أرقام القائمة في الفقرة (د) ظهرت على يمين البنود",
     "الملف محفوظ بصيغة <span class=\"spec\">.docx</span> وبصيغة <span class=\"spec\">.pdf</span>"],
 2: ["استبدلت «التحديات» بـ«المعضلات» في كل مواضعها",
     "استبدلت <span class=\"spec\">crucial</span> بـ<span class=\"spec\">essential</span>",
     "راجعت النتيجة ولم يتغيّر نص لم يكن مقصوداً",
     "الملف محفوظ بالصيغتين"],
 3: ["الصورة مدرجة والنص يلتف حولها",
     "العلامة المائية تظهر في كل الصفحات",
     "رقم الصفحة يظهر في موضعه وبالترتيب الصحيح",
     "حدود الصفحة مطبّقة على المستند بأكمله"],
 4: ["الخط <span class=\"spec\">Traditional Arabic</span> بحجم <span class=\"num\">14</span> على الفقرة كاملة",
     "القائمة المرقّمة بنمط (أ، ب، ج) لا بأرقام",
     "الصفحة الثانية أفقية والأولى والثالثة عموديتان",
     "العنوان يحمل نمط «عنوان 1» ويظهر في جزء التنقل",
     "فهرس المحتويات مولَّد ويتحدّث بزر «تحديث الجدول»"],
 5: ["الجدول 4 أعمدة × 6 صفوف ومملوء بمدن سعودية",
     "العمود الأول في أقصى يمين الجدول",
     "الصفوف مفروزة تصاعدياً حسب «المدينة»",
     "رأس الجدول يتكرر في أعلى كل صفحة يمتد إليها"],
 6: ["صحّحت الأخطاء الإملائية بزر «تغيير»",
     "الكلمة المخصّصة أُضيفت إلى القاموس ولم تعد تُعدّ خطأً",
     "جرّبت تتبّع التغييرات ورأيت المحذوف مشطوباً",
     "قبلت تعديلاً ورفضت آخر وحذفت التعليق"],
 7: ["مصدر البيانات 9 أعمدة × 6 صفوف وأسماء حقوله بلا مسافات",
     "القالب مربوط بمصدر البيانات فعلياً",
     "كل الحقول التسعة مدرجة في مواضعها",
     "المعاينة تعرض السجلات الخمسة ببيانات مختلفة",
     "التنسيق مطبّق على الحقل لا على نص بعينه"],
 8: ["نطاق الطباعة <span class=\"spec\">1, 4-6, 9</span> ظهر أثره في المعاينة",
     "جرّبت الهوامش الضيقة والاتجاه الأفقي ولاحظت الفرق",
     "عرضت «طباعة معلومات المستند» ثم أعدت الخيار",
     "لم تُستهلك ورقة واحدة"],
 9: ["التشفير بـ<span class=\"spec\">Pass123</span> يطلب كلمة المرور عند الفتح",
     "ألغيت التشفير ونجح فتح الملف بلا كلمة مرور",
     "الجملة المستثناة قابلة للتعديل وبقية المستند محمية",
     "أوقفت الحماية بـ<span class=\"spec\">Edit456</span>",
     "بعد حماية البنية لم تستطع تغيير نمط «عنوان 1»"],
}

def clean(html: str) -> str:
    """تحويل HTML الموقع إلى HTML الورقة: نفس المحتوى بأصناف الطباعة."""
    h = html
    h = h.replace('<ol class="lab-steps">', '<ol class="steps">')
    h = re.sub(r'<ol class="lab-steps" style="counter-reset:ls (\d+)">',
               lambda m: '<ol class="steps" style="counter-reset:st %s">' % m.group(1), h)
    h = re.sub(r'<p style="font-weight:700;margin-block:[^"]*">([\s\S]*?)</p>',
               r'<p class="phase">\1</p>', h)
    h = h.replace('<p class="goal">', '<p class="goal-inner">')
    return h

GOAL_RE = re.compile(r'^الهدف:\s*')

def clean_map(h):
    h = h.replace('images/', '../images/')
    h = h.replace('<h3>خريطة الأزرار: أين تجد ما ستحتاجه</h3>', '<p class="map-head">خريطة الأزرار: أين تجد ما ستحتاجه</p>')
    h = h.replace('<h3>خريطة الأزرار</h3>', '<p class="map-head">خريطة الأزرار</p>')
    h = h.replace('<figure class="fig ui">', '<figure class="fig">')
    return h

def sheet_html(u):
    goal = GOAL_RE.sub('', u["goalAr"])
    body = clean(u["bodyAr"])
    body = re.sub(r'<p class="goal-inner">[\s\S]*?</p>', '', body, count=1)  # الهدف يُعرض في صندوقه
    warn = ('<div class="warn"><span class="lbl">تنبيه العربي</span>%s</div>'
            % re.sub(r'^<p>|</p>$', lambda m: '<p>' if m.group(0)=='<p>' else '</p>', u["warnAr"])) if u["warnAr"] else ''
    checks = ''.join('<li>%s</li>' % c for c in CHECKS.get(u["num"], []))
    amap = clean_map(u.get("mapAr", ""))
    return f"""<!DOCTYPE html>
<html dir="rtl" lang="ar"><head><meta charset="utf-8">
<title>{u['tagAr']} — {u['headAr']}</title><style>{CSS}</style></head>
<body>
<div class="sheet-head">
  <span class="code">{C['code']}</span>
  <span class="course">{C['title']['ar']}</span>
  <span class="spacer"></span>
  <span class="unit">{u['tagAr']}</span>
</div>
<h1 class="sheet-title">{u['headAr']}</h1>
<p class="sheet-sub">مسار Word — الوحدة {u['num']} · ورقة تمرين عملي</p>
<div class="student"><div>الاسم:</div><div>الرقم الجامعي:</div><div>الشعبة:</div><div>التاريخ:</div></div>
<div class="goal"><b>الهدف:</b> {goal}</div>
{amap}
{body}
{warn}
<div class="check"><span class="lbl">تحقّق قبل التسليم</span><ul class="check-list">{checks}</ul></div>
</body></html>"""

files = []
for u in data["units"]:
    p = OUT / ("word-%02d.html" % u["num"])
    p.write_text(sheet_html(u), encoding="utf-8")
    files.append((u, p))
print("كُتب %d ملف HTML" % len(files))

from playwright.sync_api import sync_playwright
FOOT = ('<div dir="rtl" style="width:100%;text-align:center;font-size:8pt;'
        'font-family:Tahoma,Arial;color:#53606F;padding:0 18mm">'
        'SEC2021 · إعداد وإشراف علمي: د. أحمد الهندي · رخصة CC BY 4.0'
        ' &nbsp;—&nbsp; صفحة <span class="pageNumber"></span> من <span class="totalPages"></span></div>')

with sync_playwright() as pw:
    b = pw.chromium.launch()
    page = b.new_page()
    for u, p in files:
        page.goto("file://" + str(p.resolve()))
        page.wait_for_timeout(300)
        pdf = OUT / ("SEC2021_Word_تمرين_%02d.pdf" % u["num"])
        page.pdf(path=str(pdf), format="A4", print_background=True,
                 display_header_footer=True, header_template="<span></span>",
                 footer_template=FOOT,
                 margin={"top": "16mm", "bottom": "16mm", "right": "16mm", "left": "16mm"})
    b.close()
print("تم توليد %d ملف PDF" % len(files))
for f in sorted(OUT.glob("*.pdf")):
    n = subprocess.run(["pdfinfo", str(f)], capture_output=True, text=True).stdout
    pages = [l for l in n.splitlines() if l.startswith("Pages")]
    print(" ", f.name, "|", pages[0] if pages else "?", "|", round(f.stat().st_size/1024), "KB")
