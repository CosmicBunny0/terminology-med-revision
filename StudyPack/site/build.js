// Builds StudyPack/site/index.html: src/app.html + content.json embedded as a JS constant.
// Run: node StudyPack/site/build.js
const fs = require("fs");
const path = require("path");

const SITE_URL = process.env.SITE_URL || "https://example.com/medterm"; // placeholder until hosting (CLAUDE.md)
const here = __dirname;
const content = JSON.parse(fs.readFileSync(path.join(here, "..", "content", "content.json"), "utf8"));
const tpl = fs.readFileSync(path.join(here, "src", "app.html"), "utf8");

// "</" must not appear inside an inline <script>; U+2028/2029 are escaped for old JS engines
const json = JSON.stringify(content)
  .split("</").join("<\\/")
  .split(" ").join("\\u2028")
  .split(" ").join("\\u2029");
if (!tpl.includes("/*__CONTENT__*/null") || !tpl.includes("/*__SITE_URL__*/")) throw new Error("placeholders missing in src/app.html");
const out = tpl.replace("/*__CONTENT__*/null", () => json).replace("/*__SITE_URL__*/", () => SITE_URL);
// fail the build on a JS syntax error instead of shipping a blank page
for (const m of out.matchAll(/<script>([\s\S]*?)<\/script>/g)) new Function(m[1]);
fs.writeFileSync(path.join(here, "index.html"), out);
console.log(`index.html written: ${(out.length / 1024).toFixed(0)} KB, ${content.questions.length} questions`);
