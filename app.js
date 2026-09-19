/* =============================================================
   SEC2021 — app.js
   اللغة والوضع والتنقّل وتتبّع التقدم وأسئلة التقييم الذاتي.
   جافاسكربت أصلية فقط، بلا أي مكتبة خارجية.
   ============================================================= */

/* ---------- 1) نصوص الواجهة (كل مفتاح له ar و en) ---------- */
const UI = {
  toAr:            { ar: "العربية",            en: "العربية" },
  toEn:            { ar: "English",             en: "English" },
  dark:            { ar: "ليلي",                en: "Dark" },
  light:           { ar: "نهاري",               en: "Light" },
  progress:        { ar: "التقدم",              en: "Progress" },
  contents:        { ar: "محتويات المقرر",      en: "Course contents" },
  home:            { ar: "الصفحة الرئيسة",      en: "Home" },
  about:           { ar: "عن المقرر",           en: "About" },
  reset:           { ar: "تصفير التقدم",        en: "Reset progress" },
  resetAsk:        { ar: "سيُمحى سجل القراءة لكل الموديولات. هل تريد المتابعة؟", en: "Your reading record for all modules will be erased. Continue?" },
  hours:           { ar: "ساعة",                en: "hours" },
  hoursFew:        { ar: "ساعات",               en: "hours" },
  sectionsFew:     { ar: "أقسام",               en: "sections" },
  questionsFew:    { ar: "أسئلة",               en: "questions" },
  module:          { ar: "الموديول",            en: "Module" },
  clo:             { ar: "مخرج التعلم",         en: "Learning outcome" },
  clos:            { ar: "مخرجات التعلم",       en: "Learning outcomes" },
  recall:          { ar: "تذكير سريع",          en: "Quick recall" },
  cheat:           { ar: "ورقة مراجعة سريعة",   en: "Quick reference sheet" },
  quiz:            { ar: "أسئلة التقييم الذاتي", en: "Self-check questions" },
  quizHint:        { ar: "اختر إجابة واحدة لكل سؤال، وسيظهر التفسير فوراً.", en: "Pick one answer per question. The explanation appears at once." },
  markRead:        { ar: "تمت القراءة",         en: "Mark as read" },
  isRead:          { ar: "تمت القراءة ✓",       en: "Read ✓" },
  printMod:        { ar: "طباعة الموديول",      en: "Print module" },
  zoomHint:        { ar: "اضغط الصورة لتكبيرها",  en: "Tap the image to enlarge" },
  closeImg:        { ar: "إغلاق الصورة",          en: "Close image" },
  next:            { ar: "التالي",              en: "Next" },
  prev:            { ar: "السابق",              en: "Previous" },
  soon:            { ar: "قيد الإعداد",         en: "In preparation" },
  soonNote:        { ar: "هذا الموديول ضمن الخطة المعتمدة وسيُنشر في دفعة لاحقة.", en: "This module is in the approved plan and will be published in a later batch." },
  sections:        { ar: "قسماً",               en: "sections" },
  questions:       { ar: "سؤالاً",              en: "questions" },
  correctIs:       { ar: "إجابة صحيحة",         en: "Correct" },
  wrongIs:         { ar: "إجابة غير صحيحة",     en: "Not correct" },
  scoreLine:       { ar: "نتيجتك في هذا الموديول", en: "Your score in this module" },
  courseMap:       { ar: "خريطة المقرر",        en: "Course map" },
  cloTable:        { ar: "مخرجات التعلم وارتباطها بالموديولات", en: "Learning outcomes and the modules that serve them" },
  code:            { ar: "الرمز",               en: "Code" },
  outcome:         { ar: "المخرج",              en: "Outcome" },
  servedBy:        { ar: "تخدمه الموديولات",    en: "Served by modules" },
  refs:            { ar: "المراجع المعتمدة",    en: "Approved references" },
  creditHours:     { ar: "3 ساعات معتمدة",      en: "3 credit hours" },
  contactHours:    { ar: "60 ساعة اتصال",       en: "60 contact hours" },
  level:           { ar: "المستوى الثالث",      en: "Level 3" },
  startHere:       { ar: "ابدأ من الموديول الأول", en: "Start with Module 1" },
  backHome:        { ar: "الرئيسة",             en: "Home" },
  footer:          { ar: "SEC2021 — جامعة أم القرى · إعداد وإشراف علمي: د. أحمد الهندي · رخصة CC BY 4.0", en: "SEC2021 — Umm Al-Qura University · Prepared and supervised by Dr. Ahmad Al-Hindi · CC BY 4.0" }
};

/* ---------- 2) الحالة والتخزين ---------- */
const STORE_KEY = "sec2021-progress-v1";

const defaultState = { lang: "ar", theme: "light", read: {} };

function loadState() {
  try {
    const raw = localStorage.getItem(STORE_KEY);
    if (!raw) return Object.assign({}, defaultState);
    const parsed = JSON.parse(raw);
    return {
      lang: parsed.lang === "en" ? "en" : "ar",
      theme: parsed.theme === "dark" ? "dark" : "light",
      read: parsed.read && typeof parsed.read === "object" ? parsed.read : {}
    };
  } catch (e) {
    return Object.assign({}, defaultState);
  }
}

function saveState() {
  try { localStorage.setItem(STORE_KEY, JSON.stringify(state)); } catch (e) { /* التخزين غير متاح */ }
}

let state = loadState();

/* ---------- 3) أدوات مساعدة ---------- */
const $ = (sel) => document.querySelector(sel);
const t = (key) => (UI[key] ? UI[key][state.lang] : key);
const L = (obj) => (obj && obj[state.lang] !== undefined ? obj[state.lang] : "");
/* الأرقام غربية دائماً في اللغتين: لا نستخدم toLocaleString بلغة عربية */
const n = (x) => String(x);
const pct = (x) => n(Math.round(x)) + "%";
/* صيغة العدد العربية: من 3 إلى 10 جمع، وما عداها مفرد */
function unit(count, key) {
  const few = count >= 3 && count <= 10;
  return n(count) + " " + t(few ? key + "Few" : key);
}

function readyModules() { return MODULES.filter(m => m.status === "ready"); }
function findModule(id) { return MODULES.find(m => m.id === id); }
function readKey(modId, secId) { return modId + ":" + secId; }
function isRead(modId, secId) { return state.read[readKey(modId, secId)] === true; }

function moduleProgress(mod) {
  if (!mod.sections || mod.sections.length === 0) return 0;
  const done = mod.sections.filter(s => isRead(mod.id, s.id)).length;
  return (done / mod.sections.length) * 100;
}

function overallProgress() {
  const mods = readyModules();
  const total = mods.reduce((a, m) => a + m.sections.length, 0);
  if (total === 0) return 0;
  const done = mods.reduce((a, m) => a + m.sections.filter(s => isRead(m.id, s.id)).length, 0);
  return (done / total) * 100;
}

/* ---------- 4) اللغة والوضع ---------- */
function applyLang() {
  const html = document.documentElement;
  html.lang = state.lang;
  html.dir = state.lang === "ar" ? "rtl" : "ltr";
  document.title = COURSE.code + " — " + L(COURSE.title);
  $("#brandName").textContent = L(COURSE.title);
  $("#langBtn").textContent = state.lang === "ar" ? UI.toEn.ar : UI.toAr.en;
  $("#progLabel").textContent = t("progress");
  $("#footText").textContent = t("footer");
  $("#sidebar").setAttribute("aria-label", t("contents"));
  applyThemeLabel();
}

function applyThemeLabel() {
  $("#themeLabel").textContent = state.theme === "dark" ? t("light") : t("dark");
  $("#themeIcon").textContent = state.theme === "dark" ? "☀" : "☾";
}

function applyTheme() {
  document.documentElement.setAttribute("data-theme", state.theme);
  applyThemeLabel();
}

/* ---------- 5) شريط التقدم ---------- */
function refreshProgressBar() {
  const p = overallProgress();
  $("#progBar").style.inlineSize = pct(p);
  $("#progPct").textContent = pct(p);
  $("#progBarWrap").setAttribute("aria-valuenow", n(Math.round(p)));
}

/* ---------- 6) القائمة الجانبية ---------- */
function renderSidebar(activeId) {
  const mods = MODULES.map(m => {
    const ready = m.status === "ready";
    const p = moduleProgress(m);
    const done = ready && p >= 100;
    const active = m.id === activeId;
    const href = ready ? "#/" + m.id : "#/";
    const sub = (active && ready)
      ? '<ul class="nav-sub">' + m.sections.map(s =>
          '<li><a href="#/' + m.id + '/' + s.id + '" data-spy="' + s.id + '">' + L(s.title) + "</a></li>"
        ).join("") + "</ul>"
      : "";
    return '<li><a href="' + href + '" class="' + (active ? "active " : "") + (done ? "done" : "") +
      (ready ? "" : " pending") + '"><span class="dot">' + n(m.n) + "</span><span>" + L(m.title) +
      '</span><span class="pct">' + (ready ? pct(p) : "—") + "</span></a>" + sub + "</li>";
  }).join("");

  $("#sidebar").innerHTML =
    '<details class="nav-wrap" id="navWrap"><summary>' + t("contents") + "</summary>" +
    '<ul class="nav-mod">' +
      '<li><a href="#/" class="' + (activeId === "home" ? "active" : "") + '"><span class="dot">•</span><span>' + t("home") + "</span></a></li>" +
      mods +
      '<li><a href="#/about" class="' + (activeId === "about" ? "active" : "") + '"><span class="dot">؟</span><span>' + t("about") + "</span></a></li>" +
    "</ul>" +
    '<button class="btn btn-sm" id="resetBtn" type="button" style="margin-block-start:12px;inline-size:100%;justify-content:center">' + t("reset") + "</button></details>";

  syncNavOpen();
  $("#sidebar").querySelectorAll(".nav-mod a").forEach(function (a) {
    a.addEventListener("click", function () {
      if (!wideScreen.matches) $("#navWrap").open = false;
    });
  });

  $("#resetBtn").addEventListener("click", function () {
    if (window.confirm(t("resetAsk"))) {
      state.read = {};
      saveState();
      route();
    }
  });
}

const wideScreen = window.matchMedia("(min-width:980px)");
function syncNavOpen() {
  const w = document.getElementById("navWrap");
  if (w) w.open = wideScreen.matches;
}
wideScreen.addEventListener("change", syncNavOpen);

/* ---------- 7) الصفحة الرئيسة ---------- */
function cloChips(codes) {
  return codes.map(c => '<span class="chip amber">' + t("clo") + " " + c + "</span>").join("");
}

function renderHome() {
  const cards = MODULES.map(m => {
    const ready = m.status === "ready";
    const p = moduleProgress(m);
    const foot = ready
      ? '<div class="foot"><span class="mini-bar"><span style="inline-size:' + pct(p) + '"></span></span><span class="num">' + pct(p) + "</span></div>"
      : '<div class="foot"><span>' + t("soon") + "</span></div>";
    const inner =
      '<div class="top"><span class="n">' + n(m.n) + "</span><h3>" + L(m.title) + '</h3><span class="hrs">' +
      unit(m.hours, "hours") + "</span></div><p>" + L(m.summary) + "</p>" + foot;
    return ready
      ? '<a class="mod-card" href="#/' + m.id + '">' + inner + "</a>"
      : '<div class="mod-card pending">' + inner + "</div>";
  }).join("");

  const cloRows = COURSE.clos.map(c => {
    const serving = MODULES.filter(m => m.clos.indexOf(c.code) !== -1).map(m => n(m.n)).join(" · ");
    return "<tr><td class=\"num\">" + c.code + "</td><td>" + L(c.text) + "</td><td class=\"num\">" + serving + "</td></tr>";
  }).join("");

  const refs = COURSE.refs.map(r => "<li>" + L(r) + "</li>").join("");

  $("#view").innerHTML =
    '<section class="hero">' +
      '<p class="eyebrow">' + COURSE.code + "</p>" +
      "<h1>" + L(COURSE.title) + "</h1>" +
      "<p>" + L(COURSE.lede) + "</p>" +
      '<p style="color:var(--muted);margin-block-start:10px">' + L(COURSE.program) + "</p>" +
      '<div class="meta"><span class="chip">' + t("creditHours") + '</span><span class="chip">' +
        t("contactHours") + '</span><span class="chip">' + t("level") + "</span></div>" +
      '<p style="margin-block-start:16px"><a class="btn btn-primary" href="#/m1">' + t("startHere") + "</a></p>" +
    "</section>" +
    '<h2 style="margin-block:8px 14px">' + t("courseMap") + "</h2>" +
    '<div class="mod-grid">' + cards + "</div>" +
    '<section class="section" style="margin-block-start:22px"><h2>' + t("cloTable") + "</h2>" +
      '<div class="table-wrap"><table><thead><tr><th>' + t("code") + "</th><th>" + t("outcome") +
      "</th><th>" + t("servedBy") + "</th></tr></thead><tbody>" + cloRows + "</tbody></table></div>" +
      "<h3>" + t("refs") + "</h3><ul>" + refs + "</ul></section>";
}

/* ---------- 8) صفحة الموديول ---------- */
function renderModule(mod) {
  const secs = mod.sections.map((s, i) =>
    '<section class="section" id="' + s.id + '"><h2><span class="sn">' + n(mod.n) + "." + n(i + 1) +
    "</span><span>" + L(s.title) + "</span></h2>" + L(s.html) +
    '<div class="sec-foot"><button class="btn read-btn' + (isRead(mod.id, s.id) ? " is-read" : "") +
    '" type="button" data-sec="' + s.id + '">' + (isRead(mod.id, s.id) ? t("isRead") : t("markRead")) +
    "</button></div></section>"
  ).join("");

  const cheat = mod.cheat && mod.cheat.length
    ? '<section class="cheat"><h2>' + t("cheat") + '</h2><div class="grid">' +
      mod.cheat.map(c => '<div class="item"><b>' + L(c.t) + "</b><span>" + L(c.d) + "</span></div>").join("") +
      "</div></section>"
    : "";

  const qs = QUIZZES[mod.id] || [];
  const quiz = qs.length
    ? '<section class="quiz" id="quiz"><h2>' + t("quiz") + '</h2><p class="hint">' + t("quizHint") + "</p>" +
      qs.map((q, qi) =>
        '<div class="q" id="q' + n(qi) + '"><div class="qt"><span class="qn">' + n(qi + 1) + "</span><span>" +
        L(q.q) + "</span></div><div class=\"opts\">" +
        q.options.map((o, oi) =>
          '<button class="opt" type="button" data-q="' + n(qi) + '" data-o="' + n(oi) + '"><span class="mark">' +
          "ABCD".charAt(oi) + "</span><span>" + L(o) + "</span></button>"
        ).join("") +
        '</div><div class="why" id="why' + n(qi) + '" hidden></div></div>'
      ).join("") +
      '<div class="score" id="score" hidden></div></section>'
    : "";

  const ready = readyModules();
  const idx = ready.findIndex(m => m.id === mod.id);
  const prev = idx > 0 ? ready[idx - 1] : null;
  const next = idx < ready.length - 1 ? ready[idx + 1] : null;
  const pager = '<nav class="pager">' +
    (prev ? '<a href="#/' + prev.id + '"><span>' + t("prev") + "</span><b>" + L(prev.title) + "</b></a>" : "") +
    (next ? '<a href="#/' + next.id + '"><span>' + t("next") + "</span><b>" + L(next.title) + "</b></a>" : "") +
    "</nav>";

  $("#view").innerHTML =
    '<header class="page-head"><p class="eyebrow">' + t("module") + " " + n(mod.n) + " · " +
      unit(mod.hours, "hours") + " · " + unit(mod.sections.length, "sections") + " · " +
      unit(qs.length, "questions") + "</p><h1>" + L(mod.title) + "</h1><p>" + L(mod.summary) + '</p>' +
      '<div class="meta" style="display:flex;gap:8px;flex-wrap:wrap;margin-block-start:12px">' + cloChips(mod.clos) +
      '<button class="btn btn-sm" type="button" id="printBtn">' + t("printMod") + "</button></div></header>" +
    '<section class="box recall" style="margin-block-end:18px"><span class="label">' + t("recall") + "</span>" +
      L(mod.recall) + "</section>" +
    secs + cheat + quiz + pager;

  /* أزرار «تمت القراءة» */
  document.querySelectorAll(".read-btn").forEach(btn => {
    btn.addEventListener("click", function () {
      const secId = btn.getAttribute("data-sec");
      const key = readKey(mod.id, secId);
      if (state.read[key]) { delete state.read[key]; } else { state.read[key] = true; }
      saveState();
      btn.classList.toggle("is-read");
      btn.textContent = state.read[key] ? t("isRead") : t("markRead");
      refreshProgressBar();
      renderSidebar(mod.id);
      startSpy();
    });
  });

  $("#printBtn").addEventListener("click", function () { window.print(); });

  bindFigures();

  bindQuiz(mod);
  startSpy();
}

/* ---------- 8ب) تكبير الصور التوضيحية ---------- */
function bindFigures() {
  document.querySelectorAll(".fig img").forEach(function (img) {
    img.title = t("zoomHint");
    img.tabIndex = 0;
    img.addEventListener("click", function () { openLightbox(img); });
    img.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); openLightbox(img); }
    });
  });
}

function openLightbox(img) {
  const box = document.createElement("div");
  box.className = "lightbox";
  box.setAttribute("role", "dialog");
  box.setAttribute("aria-modal", "true");
  box.setAttribute("aria-label", img.alt || t("zoomHint"));

  const big = document.createElement("img");
  big.src = img.src;
  big.alt = img.alt;

  const close = document.createElement("button");
  close.type = "button";
  close.className = "close";
  close.setAttribute("aria-label", t("closeImg"));
  close.textContent = "✕";

  box.appendChild(big);
  box.appendChild(close);
  document.body.appendChild(box);
  document.body.style.overflow = "hidden";
  close.focus();

  function shut() {
    document.body.removeChild(box);
    document.body.style.overflow = "";
    document.removeEventListener("keydown", onKey);
    img.focus({ preventScroll: true });
  }
  function onKey(e) { if (e.key === "Escape") shut(); }

  box.addEventListener("click", function (e) { if (e.target !== big) shut(); });
  document.addEventListener("keydown", onKey);
}

/* ---------- 9) محرّك الأسئلة ---------- */
function bindQuiz(mod) {
  const qs = QUIZZES[mod.id] || [];
  if (!qs.length) return;
  const answered = {};

  document.querySelectorAll(".opt").forEach(btn => {
    btn.addEventListener("click", function () {
      const qi = parseInt(btn.getAttribute("data-q"), 10);
      const oi = parseInt(btn.getAttribute("data-o"), 10);
      if (answered[qi] !== undefined) return;
      answered[qi] = oi;

      const q = qs[qi];
      const good = oi === q.correct;
      const block = document.getElementById("q" + n(qi));

      block.querySelectorAll(".opt").forEach(b => {
        b.disabled = true;
        const bi = parseInt(b.getAttribute("data-o"), 10);
        if (bi === q.correct) b.classList.add("correct");
        else if (bi === oi) b.classList.add("wrong");
      });

      const why = document.getElementById("why" + n(qi));
      why.className = "why " + (good ? "good" : "bad");
      why.innerHTML = "<b>" + (good ? t("correctIs") : t("wrongIs")) + "</b>" + L(q.why);
      why.hidden = false;

      const count = Object.keys(answered).length;
      if (count === qs.length) {
        const right = Object.keys(answered).filter(k => answered[k] === qs[k].correct).length;
        const box = document.getElementById("score");
        box.innerHTML = "<span>" + t("scoreLine") + '</span><span class="big num">' + n(right) + " / " +
          n(qs.length) + "</span>";
        box.hidden = false;
      }
    });
  });
}

/* ---------- 10) تتبّع موضع القراءة (scroll-spy) ---------- */
let spy = null;
function startSpy() {
  if (spy) { spy.disconnect(); spy = null; }
  const links = document.querySelectorAll('.nav-sub a[data-spy]');
  if (!links.length) return;
  const secs = document.querySelectorAll(".content .section[id]");
  if (!secs.length) return;

  spy = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (!en.isIntersecting) return;
      links.forEach(a => a.classList.toggle("current", a.getAttribute("data-spy") === en.target.id));
    });
  }, { rootMargin: "-100px 0px -60% 0px", threshold: 0 });

  secs.forEach(s => spy.observe(s));
}

/* ---------- 11) صفحة «عن المقرر» ---------- */
function renderAbout() {
  $("#view").innerHTML =
    '<header class="page-head"><p class="eyebrow">' + COURSE.code + '</p><h1>' + t("about") + "</h1></header>" +
    '<section class="section about">' + L(COURSE.about) + "</section>";
}

/* ---------- 12) التوجيه ---------- */
function route() {
  const hash = (location.hash || "#/").replace(/^#\/?/, "");
  const parts = hash.split("/").filter(Boolean);
  let activeId = "home";

  if (parts.length === 0) {
    renderHome();
  } else if (parts[0] === "about") {
    activeId = "about";
    renderAbout();
  } else {
    const mod = findModule(parts[0]);
    if (mod && mod.status === "ready") {
      activeId = mod.id;
      renderModule(mod);
    } else {
      location.hash = "#/";
      return;
    }
  }

  renderSidebar(activeId);
  refreshProgressBar();

  const target = parts[1] ? document.getElementById(parts[1]) : null;
  if (target) {
    target.scrollIntoView({ block: "start" });
  } else {
    window.scrollTo(0, 0);
  }
  $("#view").focus({ preventScroll: true });
}

/* ---------- 13) الإقلاع ---------- */
function init() {
  applyTheme();
  applyLang();

  $("#langBtn").addEventListener("click", function () {
    state.lang = state.lang === "ar" ? "en" : "ar";
    saveState();
    applyLang();
    route();
  });

  $("#themeBtn").addEventListener("click", function () {
    state.theme = state.theme === "dark" ? "light" : "dark";
    saveState();
    applyTheme();
  });

  window.addEventListener("hashchange", route);
  route();
}

document.addEventListener("DOMContentLoaded", init);
