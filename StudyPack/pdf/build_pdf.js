// Builds the A4 study-pack PDF from StudyPack/content/content.json.
// Run: node StudyPack/pdf/build_pdf.js   → pdf/print.html + pdf/MedTerm-L1-L5-Study-Pack.pdf
// Uses the Playwright Chromium already installed in StudyPack/qa (no extra dependency).
const fs = require("fs");
const path = require("path");
const { chromium } = require(path.join(__dirname, "..", "qa", "node_modules", "playwright"));

const here = __dirname;
const C = JSON.parse(fs.readFileSync(path.join(here, "..", "content", "content.json"), "utf8"));
const M = C.meta;
const OUT_HTML = path.join(here, "print.html");
const SITE_URL = process.env.SITE_URL || "https://terminology-med-revision.vercel.app";
const OUT_PDF = path.join(here, "MedTerm-L1-L5-Study-Pack.pdf");

const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const ar = s => s ? `<p class="ar" lang="ar" dir="rtl">${esc(s)}</p>` : "";
const EXTRA_AR = `<span class="xtra">(زيادة للفهم)</span>`;
const ref = (lec, slide) => `<span class="ref">${lec ? `L${lec} ` : ""}p${esc(slide)}</span>`;

// word part with the slide colour code; "/o" combining vowel in amber (same rule as the site)
function partHTML(p, kind) {
  const k = kind === "plural" || kind === "analysis" ? "root" : kind;
  const m = /^(.*?)(\/[aeiou])$/.exec(p);
  if (m && k !== "suffix") return `<span class="part"><span class="hl k-${k}">${esc(m[1])}</span><span class="hl k-vowel">${esc(m[2])}</span></span>`;
  return `<span class="part"><span class="hl k-${k}">${esc(p)}</span></span>`;
}
const termHTML = parts => `<span class="part">${parts.map((p, i) =>
  `${i ? '<span class="sep">/</span>' : ""}<span class="hl k-${p.type}">${esc(p.text)}</span>`).join("")}</span>`;

// colour of a bare part (look-alikes): the kind of its own table row; hyphen position only as a fallback
const KIND = {};
C.sections.forEach(s => s.rows.forEach(r => [r.part, ...r.alts].forEach(f => { KIND[f.toLowerCase()] = KIND[f.toLowerCase()] || s.kind; })));
const kindOfPart = p => (p = p.split(/,\s*/)[0], KIND[p.toLowerCase()]) || (p.startsWith("-") ? "suffix" : p.endsWith("-") ? "prefix" : "root");
const byLec = (arr, l) => arr.filter(x => x.lec === l);
const lecTitle = l => M.lectures.find(x => x.n === l);

/* ---------- cover ---------- */
const sample = C.analysis.find(a => ["prefix", "root", "vowel", "suffix"].every(t => a.parts.some(p => p.type === t))) || C.analysis[0];
const ex = M.exam, g = ex.grading;
const cover = `
<section class="cover">
  <div class="kicker">${esc(M.course)}</div>
  <h1>Medical Terminology<br><span>Lectures 1–5 study pack</span></h1>
  <div class="exam">
    <div><b>${esc(ex.name)}</b> · ${esc(ex.day)} 25 October 2026 · written · covers ${esc(ex.covers)}</div>
    <div class="muted">Grading (L1 p8): class activity / periodicals ${g.class_activity_periodicals} (mid-term / quiz ${g.midterm_quiz} + research ${g.research}) · final written ${g.final_written}</div>
    <div class="muted">Written exam → spelling, word-structure analysis and meanings matter most.</div>
  </div>
  <div class="key">
    <div class="key-title">Colour code (L4 p2 highlighters)</div>
    <div class="key-row">
      <span class="hl k-prefix">prefix</span><span class="hl k-root">root</span><span class="hl k-vowel">combining vowel</span><span class="hl k-suffix">suffix</span>
    </div>
    <div class="key-ex">${termHTML(sample.parts)} <span class="muted">= ${esc(sample.medical)}</span></div>
    <div class="small muted">Amber for the combining vowel is our addition. ${ref(sample.lec, sample.slide)}</div>
  </div>
  <ol class="toc">
    <li><b>Foundations</b> — L1 & L2: definitions, word parts, rules, pronunciation, plurals</li>
    <li><b>Word-part tables</b> — L3 roots & prefixes · L4 prefixes & suffixes · L5 suffixes</li>
    <li><b>Term analysis</b> — ${C.analysis.length} terms split into parts</li>
    <li><b>Look-alikes</b> — ${C.lookalikes.length} groups that are easy to mix up</li>
    <li><b>Spelling traps</b> — ${C.spellingTraps.length} words to write correctly</li>
    <li><b>Self-test</b> with answer key · blank analysis sheet</li>
  </ol>
  <div class="sources">
    <div class="key-title">Source: the doctors' slides</div>
    ${M.lectures.map(l => `<div><b>L${l.n}</b> ${esc(l.title)} — <span class="muted">${esc(l.doctor)}</span></div>`).join("")}
    <div><b>Training sheet</b> — <span class="muted">${esc(M.trainingSheet.by)}</span></div>
  </div>
  <div class="credit">
    <div><b>${esc(M.disclaimer)}</b></div>
    <div>Flashcards & quizzes: <b>${esc(SITE_URL)}</b></div>
    <div class="muted">${esc(M.credit)} · page refs like “L3 p24” point to the PDF page of that lecture · items marked (extra) / (زيادة للفهم) are not on the slides.</div>
  </div>
</section>`;

/* ---------- part 1: foundations ---------- */
function concept(c) {
  return `<div class="concept${c.lowPriority ? " low" : ""}"><h4>${esc(c.title)} ${ref(c.lec, c.slide)}</h4>
    <ul>${c.body.map(b => `<li>${esc(b)}</li>`).join("")}</ul>${ar(c.ar)}</div>`;
}
const L1C = byLec(C.concepts, 1).filter(c => c.id !== "grading");
const L2C = byLec(C.concepts, 2);
const foundations = `
<section class="part-open"><div class="pn">1</div><h2>Foundations <span>L1 · L2</span></h2></section>
<h3 class="lec">Lecture 1 — ${esc(lecTitle(1).title)}</h3>
<div class="concepts">${L1C.map(concept).join("")}</div>
<h3 class="lec">Lecture 2 — ${esc(lecTitle(2).title)}</h3>
<div class="concepts">${L2C.filter(c => !["graphtrio", "lumen"].includes(c.id)).map(concept).join("")}</div>
<h4 class="tt">Rules for building terms ${ref(C.rules_intro.lec, C.rules_intro.slide)}</h4>
<p class="small muted">${C.rules_intro.body.map(esc).join(" ")}</p>
<table class="t rules"><thead><tr><th>#</th><th>Rule</th><th>Example</th></tr></thead><tbody>
${C.rules.map(r => `<tr><td class="num">${esc(r.id)}</td><td>${esc(r.rule)}${ar(r.ar)}</td><td>${esc(r.example)} ${ref(r.lec, r.slide)}</td></tr>`).join("")}
</tbody></table>
<div class="two">
<div><h4 class="tt">Pronunciation at the start of a word</h4>
<table class="t"><thead><tr><th>Letters</th><th>Sound</th><th>Examples</th></tr></thead><tbody>
${C.pronunciation.map(p => `<tr><td><b>${esc(p.letters)}</b></td><td>${esc(p.sound)}</td><td>${esc(p.examples.join(", "))} ${ref(p.lec, p.slide)}</td></tr>`).join("")}
</tbody></table></div>
<div><h4 class="tt">Plurals (Latin / Greek)</h4>
<table class="t"><thead><tr><th>Ending</th><th>Singular</th><th>Plural</th></tr></thead><tbody>
${C.plurals.map(p => `<tr><td>-${esc(p.ending)} → -${esc(p.pluralEnding)}</td><td>${esc(p.singular)} <span class="muted small">${esc(p.meaning)}</span></td><td><b>${esc(p.plural)}</b> ${ref(p.lec, p.slide)}</td></tr>`).join("")}
</tbody></table>
<p class="small muted">Slide header “Pleural” = Plural.</p></div>
</div>
<div class="concepts">${L2C.filter(c => ["graphtrio", "lumen"].includes(c.id)).map(concept).join("")}</div>
<div class="hw"><b>Homework on the slide ${ref(M.homework.lec, M.homework.slide)}:</b> analyse ${M.homework.terms.map(esc).join(", ")} — answers are in Part 3. <span class="muted small">${esc(M.homework.note)}</span></div>`;

/* ---------- part 2: tables ---------- */
function sectionTable(s) {
  const head = `<h4 class="tt">${esc(s.title)}${s.subtitle ? ` <span class="muted">— ${esc(s.subtitle)}</span>` : ""} ${ref(s.lec, s.slide)}</h4>${s.note ? `<p class="small muted">${esc(s.note)}</p>` : ""}`;
  if (s.id === "numchart") {
    return `${head}<table class="t"><thead><tr><th>Prefix</th><th>Number</th><th>Examples on the chart</th></tr></thead><tbody>
${s.rows.map(r => `<tr><td>${partHTML(r.part, "prefix")}</td><td>${esc(r.meaning)}</td><td>${esc(r.definition || r.example)}</td></tr>`).join("")}</tbody></table>`;
  }
  return `${head}<table class="t parts"><thead><tr><th>${s.kind}</th><th>Meaning</th><th>Example</th><th>Definition of the example</th></tr></thead><tbody>
${s.rows.map(r => `<tr><td>${partHTML(r.part, s.kind)}${r.alts.length ? `<div class="alts">also ${r.alts.map(a => partHTML(a, s.kind)).join(" ")}</div>` : ""}</td>
<td><b>${esc(r.meaning)}</b></td><td class="exm">${esc(r.example)}</td><td>${esc(r.definition)}${r.note ? `<div class="note">${esc(r.note)}</div>` : ""}</td></tr>`).join("")}
</tbody></table>`;
}
const lecConcepts = l => byLec(C.concepts, l).filter(c => !["numchart", "anti"].includes(c.id));
const tables = `
<section class="part-open"><div class="pn">2</div><h2>Word-part tables <span>L3 · L4 · L5</span></h2></section>
${[3, 4, 5].map(l => `
<h3 class="lec">Lecture ${l} — ${esc(lecTitle(l).title)}</h3>
${lecConcepts(l).length ? `<div class="concepts">${lecConcepts(l).map(concept).join("")}</div>` : ""}
${byLec(C.sections, l).map(s => s.id === "anti" ? `${sectionTable(s)}${concept(C.concepts.find(c => c.id === "anti"))}` : sectionTable(s)).join("")}`).join("")}`;

/* ---------- part 3: analysis ---------- */
const FROM = { slide: "", table: "", def: "", extra: "*" };
const analysis = `
<section class="part-open"><div class="pn">3</div><h2>Term analysis <span>prefix / root / vowel / suffix</span></h2></section>
<p class="small muted">Write it like the training sheet: term → structure → meaning of each part → meaning of the term. ★ = worked on the slide. * = part meaning is extra (not written on the slide).</p>
<table class="t an"><thead><tr><th>Term & structure</th><th>Parts</th><th>Meaning of the term</th></tr></thead><tbody>
${C.analysis.map(a => `<tr><td><div class="term">${esc(a.term)}${a.workedOnSlide ? ' <span class="star">★</span>' : ""}</div>${termHTML(a.parts)} ${ref(a.lec, a.slide)}</td>
<td class="pm">${a.parts.filter(p => p.type !== "vowel").map(p => `<span class="hl k-${p.type}">${esc(p.text)}</span> ${p.meaning ? esc(p.meaning) + (FROM[p.from] || "") : '<span class="muted">—</span>'}`).join("<br>")}</td>
<td>${esc(a.medical)}${a.note ? (/[؀-ۿ]/.test(a.note) ? ar(a.note) : `<div class="note">${esc(a.note)}</div>`) : ""}</td></tr>`).join("")}
</tbody></table>`;

/* ---------- part 4: look-alikes ---------- */
const look = `
<section class="part-open"><div class="pn">4</div><h2>Look-alikes <span>don't mix them up</span></h2></section>
<div class="looks">${C.lookalikes.map(g => `<div class="look"><h4>${esc(g.title)} <span class="ref">${esc(g.slide)}</span></h4>
<table class="t mini"><tbody>${g.rows.map(r => `<tr><td>${r.part ? partHTML(r.part, kindOfPart(r.part)) : ""}</td><td>${esc(r.meaning)}</td><td class="exm">${esc(r.example || "")}</td></tr>`).join("")}</tbody></table>
${g.tip ? `<p class="ar" lang="ar" dir="rtl">${esc(g.tip)} ${g.tipIsExtra ? EXTRA_AR : ""}</p>` : ""}</div>`).join("")}</div>`;

/* ---------- part 5: spelling traps ---------- */
// strike only the wrong spellings; the "(…)" note after them stays readable
const trapHTML = t => { const m = /^(.*?)\s*(\(.*\))?$/.exec(t); return `<span class="${/accepted/.test(m[2] || "") ? "" : "bad"}">${esc(m[1])}</span>${m[2] ? ` <span class="note">${esc(m[2])}</span>` : ""}`; };
const traps = `
<section class="part-open"><div class="pn">5</div><h2>Spelling traps <span>written exam</span></h2></section>
<p class="small muted">Write the left column exactly (American spelling, as on the slides). “Say” is a pronunciation guide (extra).</p>
<table class="t traps"><thead><tr><th>Correct</th><th>Don't write</th><th>Say (extra)</th></tr></thead><tbody>
${C.spellingTraps.map(t => `<tr><td><b>${esc(t.word)}</b> ${ref(t.lec, t.slide)}</td><td>${trapHTML(t.trap)}</td><td class="muted">${esc(t.say)}</td></tr>`).join("")}
</tbody></table>`;

/* ---------- part 6: self-test ---------- */
// deterministic pick spread over the lectures: every k-th question of each type
function every(arr, n) { if (arr.length <= n) return arr; const step = arr.length / n; return Array.from({ length: n }, (_, i) => arr[Math.floor(i * step)]); }
const QM = every(C.questions.filter(q => q.type === "mcq"), 36);
const QT = every(C.questions.filter(q => q.type === "tf"), 14);
const QS = every(C.questions.filter(q => q.type === "spell"), 20);
const L = "abcd";
let n = 0;
const qnum = new Map();
[...QM, ...QT, ...QS].forEach(q => qnum.set(q.id, ++n));
const test = `
<section class="part-open"><div class="pn">6</div><h2>Self-test <span>${n} questions · answers at the end</span></h2></section>
<p class="small muted">More (${C.questions.length} questions, typed answers, flashcards) on the website: <b>${esc(SITE_URL)}</b></p>
<h4 class="tt">A. Choose the correct answer</h4>
<ol class="qs">${QM.map(q => `<li value="${qnum.get(q.id)}">${esc(q.q)} ${ref(q.lec, q.slide)}<div class="opts">${q.options.map((o, i) => `<span>${L[i]}) ${esc(o)}</span>`).join("")}</div></li>`).join("")}</ol>
<h4 class="tt">B. True or false — correct the false ones</h4>
<ol class="qs">${QT.map(q => `<li value="${qnum.get(q.id)}">${esc(q.q)} ${ref(q.lec, q.slide)}</li>`).join("")}</ol>
<h4 class="tt">C. Write the term / plural (spelling counts)</h4>
<ol class="qs">${QS.map(q => `<li value="${qnum.get(q.id)}">${esc(q.q)} ${ref(q.lec, q.slide)}<div class="line"></div></li>`).join("")}</ol>
<div class="answers"><h4 class="tt">Answer key</h4><ol class="ak">
${QM.map(q => `<li value="${qnum.get(q.id)}"><b>${L[q.options.indexOf(q.answer)]}</b> ${esc(q.answer)}</li>`).join("")}
${QT.map(q => `<li value="${qnum.get(q.id)}"><b>${q.answer ? "True" : "False"}</b>${q.correction ? " — " + esc(q.correction) : ""}</li>`).join("")}
${QS.map(q => `<li value="${qnum.get(q.id)}"><b>${esc(q.answer[0])}</b>${q.answer.length > 1 ? ` <span class="muted">(also accepted: ${q.answer.slice(1).map(esc).join(", ")})</span>` : ""}</li>`).join("")}
</ol></div>`;

/* ---------- training sheet + appendix ---------- */
const sheet = `
<section class="sheet"><h2>Analysis practice sheet</h2>
<p class="small muted">Same layout as the training sheet by ${esc(M.trainingSheet.by)}. Try the homework terms and any term from Part 3, then check.</p>
<table class="t blank"><thead><tr><th rowspan="2">Medical term</th><th colspan="3">Term structure</th><th rowspan="2">Meaning of the medical term</th></tr>
<tr><th class="k-prefix">Prefix-</th><th class="k-root">-Root-</th><th class="k-suffix">-Suffix</th></tr></thead>
<tbody>${Array.from({ length: 10 }, (_, i) => `<tr><td>${i < M.homework.terms.length ? esc(M.homework.terms[i]) : ""}</td><td></td><td></td><td></td><td></td></tr>`).join("")}</tbody></table>
<h4 class="tt">Notes on the slides</h4>
<ul class="small">${M.slideTypos.filter(t => t.how !== "silent").map(t => `<li>${esc(t.where)}: slide writes “${esc(t.slide)}” → <b>${esc(t.correct)}</b></li>`).join("")}
<li>Medical idioms is listed in the course plan for L4, but no slide covers it, so it is not in this pack.</li></ul>
<p class="credit-end">${esc(M.credit)} · ${esc(M.disclaimer)}</p>
</section>`;

const css = `
@page{size:A4;margin:14mm 13mm 16mm}
:root{--ink:#15222E;--ink-2:#55646F;--line:#CBD5DD;--sunk:#EEF2F5;--accent:#0B5C6B;--bad:#B93229;
--p-bg:#CDE6FF;--p-ink:#0A4F94;--r-bg:#CBF0C3;--r-ink:#1A6A2B;--s-bg:#FFD2E7;--s-ink:#A11E5F;--v-bg:#FFE5A3;--v-ink:#7A5000;
--display:"Bricolage Grotesque","Segoe UI",Arial,sans-serif;--text:"IBM Plex Sans","Segoe UI",Arial,sans-serif;--arabic:"IBM Plex Sans Arabic","Noto Sans Arabic","Segoe UI",Tahoma,sans-serif}
*{box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact}
html{font-size:11pt}
body{margin:0;background:#fff;color:var(--ink);font:400 1rem/1.42 var(--text)}
h1,h2,h3,h4{font-family:var(--display);line-height:1.15;margin:0}
p{margin:.25em 0}
.muted{color:var(--ink-2)}.small{font-size:.86rem}
.ar{font-family:var(--arabic);direction:rtl;text-align:right;font-size:.95rem;line-height:1.6;color:#2F3D49;margin:.2em 0}
.xtra{font-size:.8em;color:var(--ink-2)}
.ref{font:500 .72rem var(--text);color:var(--ink-2);white-space:nowrap;background:var(--sunk);border-radius:3px;padding:0 .3em}
.hl{border-radius:.25em .5em .3em .45em;padding:0 .12em;-webkit-box-decoration-break:clone;box-decoration-break:clone}
.k-prefix{background:var(--p-bg);color:var(--p-ink)}.k-root{background:var(--r-bg);color:var(--r-ink)}
.k-suffix{background:var(--s-bg);color:var(--s-ink)}.k-vowel{background:var(--v-bg);color:var(--v-ink)}
.part{font-family:var(--display);font-weight:700;white-space:nowrap}
.sep{color:#9AA7B1;font-weight:400;padding:0 .05em}
/* cover */
.cover{min-height:265mm;display:flex;flex-direction:column;gap:7mm;break-after:page}
.kicker{font:600 .85rem var(--text);color:var(--accent);letter-spacing:.04em;text-transform:uppercase;border-top:3px solid var(--accent);padding-top:3mm}
.cover h1{font-size:34pt;font-weight:800;letter-spacing:-.02em}
.cover h1 span{display:block;font-size:17pt;font-weight:500;color:var(--ink-2);margin-top:2mm}
.exam{border-left:4px solid var(--accent);padding:2mm 0 2mm 4mm;display:grid;gap:1mm}
.key{background:var(--sunk);border-radius:8px;padding:4mm 5mm;display:grid;gap:2mm}
.key-title{font:700 .78rem var(--text);text-transform:uppercase;letter-spacing:.06em;color:var(--ink-2)}
.key-row{display:flex;gap:3mm;flex-wrap:wrap;font:700 1rem var(--display)}.key-row .hl{padding:.5mm 2mm}
.key-ex{font-size:1.25rem}.key-ex .muted{font:400 .95rem var(--text)}
.toc{margin:0;padding-left:6mm;display:grid;gap:1mm}
.sources{display:grid;gap:1mm;font-size:.88rem}
.credit{margin-top:auto;border-top:1px solid var(--line);padding-top:3mm;font-size:.88rem}
/* parts */
.part-open{break-before:page;display:flex;align-items:baseline;gap:4mm;border-bottom:2px solid var(--ink);padding-bottom:2mm;margin-bottom:4mm}
.pn{font:800 30pt/1 var(--display);color:var(--accent)}
.part-open h2{font-size:20pt;font-weight:800}.part-open h2 span{font-size:11pt;font-weight:500;color:var(--ink-2);margin-left:2mm}
h3.lec{font-size:13.5pt;margin:6mm 0 2mm;color:var(--accent);break-after:avoid}
h4.tt{font-size:11.5pt;margin:5mm 0 1.5mm;break-after:avoid}
.concepts{display:grid;grid-template-columns:1fr 1fr;gap:3mm 5mm}
.concept{border:1px solid var(--line);border-radius:6px;padding:2.5mm 3mm;break-inside:avoid}
.concept h4{font-size:10.5pt;margin-bottom:1mm}.concept ul{margin:0;padding-left:4.5mm}.concept li{margin:.5mm 0;font-size:.92rem}
.concept.low{opacity:.75}
.two{display:grid;grid-template-columns:1fr 1fr;gap:5mm}
.hw{margin-top:4mm;background:var(--v-bg);border-radius:6px;padding:2.5mm 3.5mm;font-size:.92rem;break-inside:avoid}
table.t{width:100%;border-collapse:collapse;font-size:.92rem}
.t thead{display:table-header-group}
.t th{text-align:left;font:700 .74rem var(--text);text-transform:uppercase;letter-spacing:.05em;color:var(--ink-2);border-bottom:1.5px solid var(--ink);padding:1.2mm 1.5mm}
.t td{border-bottom:1px solid var(--line);padding:1.4mm 1.5mm;vertical-align:top}
.t tr{break-inside:avoid}
.t.parts td:first-child{width:22%;font-size:1.05rem}.t.parts td:nth-child(2){width:22%}.t.parts td:nth-child(3){width:17%}
.exm{font-style:italic}
.alts{font-size:.8rem;color:var(--ink-2);margin-top:.5mm;white-space:normal}
.note{font-size:.8rem;color:var(--ink-2);margin-top:.5mm}
.num{font:800 1rem var(--display);color:var(--accent);width:7mm}
.rules td:nth-child(3){width:38%;font-size:.88rem}
.an td:first-child{width:34%}.an .term{font-weight:600;font-size:.9rem;color:var(--ink-2)}.an .part{font-size:1.08rem}
.an .pm{width:30%;font-size:.86rem;line-height:1.55}.an .pm .hl{font-weight:700}
.star{color:#C98A00}
.looks{display:grid;grid-template-columns:1fr 1fr;gap:4mm 5mm}
.look{break-inside:avoid;border-top:2px solid var(--ink);padding-top:1.5mm}.look h4{font-size:10.5pt;margin-bottom:1mm}
.t.mini td{padding:1mm 1.2mm;font-size:.86rem}.t.mini td:first-child{width:28%}
.traps .bad{color:var(--bad);text-decoration:line-through;text-decoration-thickness:1px}
.qs{padding-left:7mm;margin:0}.qs li{margin:0 0 2.6mm;break-inside:avoid}
.opts{display:grid;grid-template-columns:1fr 1fr;gap:.5mm 4mm;margin-top:.8mm;font-size:.92rem}
.line{border-bottom:1px solid var(--line);height:6mm;width:70%}
.answers{break-before:page}.ak{columns:2;column-gap:7mm;padding-left:7mm;font-size:.88rem}.ak li{break-inside:avoid;margin-bottom:1mm}
.sheet{break-before:page}.sheet h2{font-size:18pt;font-weight:800;margin-bottom:2mm}
.blank td{height:13mm;border:1px solid var(--line)}.blank th{border:1px solid var(--line);text-align:center}
.blank th.k-prefix{color:var(--p-ink)}.blank th.k-root{color:var(--r-ink)}.blank th.k-suffix{color:var(--s-ink)}
.credit-end{margin-top:6mm;font-size:.82rem;color:var(--ink-2);border-top:1px solid var(--line);padding-top:2mm}`;

const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><title>${esc(M.title)}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=IBM+Plex+Sans+Arabic:wght@400;600&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400&display=block">
<style>${css}</style></head><body>${cover}${foundations}${tables}${analysis}${look}${traps}${test}${sheet}</body></html>`;
fs.writeFileSync(OUT_HTML, html);

(async () => {
  const browser = await chromium.launch({ channel: "chrome" }); // installed Google Chrome, like qa/playwright.config.js
  const page = await browser.newPage();
  await page.goto("file:///" + OUT_HTML.replace(/\\/g, "/"), { waitUntil: "networkidle", timeout: 60000 });
  await page.evaluate(() => document.fonts.ready);
  const fonts = await page.evaluate(() => ["Bricolage Grotesque", "IBM Plex Sans", "IBM Plex Sans Arabic"].map(f => [f, document.fonts.check(`700 12px "${f}"`) || document.fonts.check(`400 12px "${f}"`)]));
  const missing = fonts.filter(f => !f[1]).map(f => f[0]);
  if (missing.length) { console.error("FONTS NOT LOADED (no network?):", missing.join(", ")); process.exitCode = 1; }
  const foot = `<div style="font:7.5px Arial,sans-serif;color:#55646F;width:100%;padding:0 13mm;display:flex;justify-content:space-between">
    <span>Medical Terminology L1–L5 · ${esc(M.disclaimer)} · ${esc(SITE_URL.replace(/^https:\/\//, ""))}</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>`;
  await page.pdf({ path: OUT_PDF, format: "A4", printBackground: true, preferCSSPageSize: true, displayHeaderFooter: true,
    headerTemplate: "<span></span>", footerTemplate: foot });
  await browser.close();
  console.log(`written ${path.relative(process.cwd(), OUT_PDF)} (${(fs.statSync(OUT_PDF).size / 1024).toFixed(0)} KB) · self-test ${n} q`);
})();
