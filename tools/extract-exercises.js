#!/usr/bin/env node
/* استخراج صناديق التمارين من content.js إلى JSON — المحتوى مصدر واحد للحقيقة.
   الاستعمال:  node _extract.js [word|ppt|excel|access]   (الافتراضي word) */
const fs = require('fs');
const path = require('path');

const dir = __dirname;
const TRACK = process.argv[2] || 'word';
const LETTER = { word: 'w', ppt: 'p', excel: 'x', access: 'a' }[TRACK] || 'w';

new Function(fs.readFileSync(path.join(dir, 'content.js'), 'utf8') + '\nglobalThis.__M = MODULES; globalThis.__C = COURSE;')();
const MODULES = globalThis.__M, COURSE = globalThis.__C;

/* وحدات المسار قد تسكن أي موديول — تُجمع من كل الموديولات بحقل track */
const units = MODULES.flatMap(m => m.sections)
  .filter(s => s.track === TRACK && /<div class="lab">/.test(s.html.ar));

function grab(html) {
  const i = html.indexOf('<div class="lab">');
  if (i < 0) return null;
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

/* خريطة الأزرار: من عنوانها حتى بداية صندوق التمرين */
function grabMap(html) {
  const i = html.indexOf('<h3>خريطة الأزرار');
  if (i < 0) return '';
  const j = html.indexOf('<div class="lab">', i);
  return j < 0 ? '' : html.slice(i, j);
}

function field(lab, re) { const m = lab.match(re); return m ? m[1] : ''; }

const out = units.map(u => {
  const labAr = grab(u.html.ar);
  const warnAr = (u.html.ar.match(/<div class="box warn"><span class="label">تنبيه العربي<\/span>([\s\S]*?)<\/div>/) || [])[1] || '';
  return {
    id: u.id,
    num: Number(u.id.replace(LETTER, '')),
    titleAr: u.title.ar,
    titleEn: u.title.en,
    tagAr: field(labAr, /<span class="tag">([^<]+)<\/span>/),
    headAr: field(labAr, /<span class="tag">[^<]+<\/span><span>([^<]+)<\/span>/),
    goalAr: field(labAr, /<p class="goal">([\s\S]*?)<\/p>/),
    bodyAr: (labAr.match(/<div class="lab-body">([\s\S]*)<\/div>\s*<\/div>$/) || [])[1] || '',
    mapAr: grabMap(u.html.ar),
    warnAr: warnAr.trim()
  };
});

const file = path.join(dir, '_exercises_' + TRACK + '.json');
fs.writeFileSync(file, JSON.stringify({
  track: TRACK,
  course: { code: COURSE.code, title: COURSE.title, author: COURSE.author, authorRole: COURSE.authorRole },
  units: out
}, null, 1), 'utf8');
console.log('استُخرج', out.length, 'تمريناً للمسار', TRACK + ':', out.map(u => u.num).join(', '),
            '| خرائط:', out.filter(u => u.mapAr).length);
