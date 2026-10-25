// Grading-drift guard, step 2: grade qa/parity_samples.json with the JS port in site/src/app.html and compare with
// the Python reference results (tools/quizlib.py). Exit 1 on any difference.
// Run from StudyPack:  python -I -X utf8 qa/grader_parity.py && node qa/grader_parity.js
const fs = require("fs");
const path = require("path");
const root = path.join(__dirname, "..");
const app = fs.readFileSync(path.join(root, "site", "src", "app.html"), "utf8");
const m = /\/\*GRADER:BEGIN[\s\S]*?\/\*GRADER:END\*\//.exec(app);
if (!m) throw new Error("GRADER block not found in app.html");
const QL = new Function(m[0] + "\nreturn QL;")();
const C = JSON.parse(fs.readFileSync(path.join(root, "content", "content.json"), "utf8"));
const B = new QL.Bank(C);
const QI = Object.fromEntries(B.Q.map(q => [q.id, q]));
const S = JSON.parse(fs.readFileSync(path.join(__dirname, "parity_samples.json"), "utf8"));
const pick = r => ({ ok: r.ok, code: r.code ?? null, ar: r.ar, credit: r.credit, max: r.max, firstWrong: r.firstWrong ?? null,
  notes: (r.notes || []).map(n => [n.blank ?? n.field ?? null, n.code ?? null, n.ar]) });
let bad = 0;
for (const s of S) {
  const js = pick(B.grade(QI[s.id], s.resp)), py = pick(s.py);
  const a = JSON.stringify(js), b = JSON.stringify(py);
  if (a !== b) { bad++; console.log(`DIFF ${s.id} [${s.why}] resp=${JSON.stringify(s.resp)}\n  py: ${b}\n  js: ${a}`); }
}
console.log(`${S.length - bad}/${S.length} samples graded identically by quizlib.py and the JS port`);
process.exit(bad ? 1 : 0);
