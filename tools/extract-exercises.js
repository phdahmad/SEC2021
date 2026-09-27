#!/usr/bin/env node
/* استخراج صناديق التمارين من content.js إلى JSON — المحتوى مصدر واحد للحقيقة */
const fs = require('fs');
const path = require('path');

const dir = __dirname;
new Function(fs.readFileSync(path.join(dir, 'content.js'), 'utf8') + '\nglobalThis.__M = MODULES; globalThis.__C = COURSE;')();
const MODULES = globalThis.__M, COURSE = globalThis.__C;

const m4 = MODULES.find(m => m.id === 'm4');
const units = m4.sections.filter(s => s.track === 'word' && /<div class="lab">/.test(s.html.ar));

function grab(html) {
  const i = html.indexOf('<div class="lab">');
  if (i < 0) return null;
  // إيجاد نهاية div.lab بعدّ الوسوم
  let depth = 0, j = i;
  const re = /<\/?div\b[^>]*>/g;
  re.lastIndex = i;
  let m;
  while ((m = re.exec(html))) {
    depth += m[0].startsWith('</') ? -1 : 1;
    if (depth === 0) { j = m.index + m[0].length; break; }
  }
  return html.slice(i, j);
}

function field(lab, re) { const m = lab.match(re); return m ? m[1] : ''; }

const out = units.map(u => {
  const labAr = grab(u.html.ar), labEn = grab(u.html.en);
  // خريطة الأزرار: من عنوانها إلى بداية صندوق التمرين
  const mi = u.html.ar.indexOf('<h3>خريطة الأزرار');
  const li = u.html.ar.indexOf('<div class="lab">');
  const mapAr = (mi >= 0 && li > mi) ? u.html.ar.slice(mi, li) : '';
  // التنبيه العربي الخاص بالوحدة (box warn بعنوان "تنبيه العربي")
  const warnAr = (u.html.ar.match(/<div class="box warn"><span class="label">تنبيه العربي<\/span>([\s\S]*?)<\/div>/) || [])[1] || '';
  return {
    id: u.id,
    num: Number(u.id.replace('w', '')),
    titleAr: u.title.ar,
    titleEn: u.title.en,
    tagAr: field(labAr, /<span class="tag">([^<]+)<\/span>/),
    headAr: field(labAr, /<span class="tag">[^<]+<\/span><span>([^<]+)<\/span>/),
    goalAr: field(labAr, /<p class="goal">([\s\S]*?)<\/p>/),
    bodyAr: (labAr.match(/<div class="lab-body">([\s\S]*)<\/div>\s*<\/div>$/) || [])[1] || '',
    mapAr: mapAr,
    warnAr: warnAr.trim()
  };
});

fs.writeFileSync(path.join(dir, '_exercises.json'),
  JSON.stringify({ course: { code: COURSE.code, title: COURSE.title, author: COURSE.author, authorRole: COURSE.authorRole }, units: out }, null, 1), 'utf8');
console.log('استُخرج', out.length, 'تمريناً:', out.map(u => u.num).join(', '));
