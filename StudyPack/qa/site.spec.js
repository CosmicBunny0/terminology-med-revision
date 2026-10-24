// Acceptance tests for StudyPack/site/index.html (build it first: node ../site/build.js)
const { test, expect } = require("@playwright/test");
const path = require("path");
const fs = require("fs");

// BASE_URL=https://terminology-med-revision.vercel.app npx playwright test  -> run against the live site
const URL = process.env.BASE_URL || "file:///" + path.resolve(__dirname, "..", "site", "index.html").replace(/\\/g, "/");
const SHOTS = path.join(__dirname, "shots");
fs.mkdirSync(SHOTS, { recursive: true });
const CONTENT = JSON.parse(fs.readFileSync(path.join(__dirname, "..", "content", "content.json"), "utf8"));

function watchErrors(page) {
  const errs = [];
  page.on("console", m => { if (m.type() === "error") errs.push(m.text()); });
  page.on("pageerror", e => errs.push(String(e)));
  return errs;
}
async function noOverflow(page, where) {
  const o = await page.evaluate(() => ({ sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth }));
  expect(o.sw, `horizontal overflow on ${where}`).toBe(o.cw);
}

/* ---------- layout: viewports x themes ---------- */
const VIEWPORTS = [[360, 740], [390, 844], [400, 850], [1280, 800]];
for (const scheme of ["light", "dark"]) {
  for (const [w, h] of VIEWPORTS) {
    test(`layout ${w}x${h} ${scheme}`, async ({ page }) => {
      await page.emulateMedia({ colorScheme: scheme });
      await page.setViewportSize({ width: w, height: h });
      const errs = watchErrors(page);
      await page.goto(URL + "#home");
      await page.waitForLoadState("networkidle");
      const tag = `${w}x${h}-${scheme}`;
      await noOverflow(page, "home"); await page.screenshot({ path: path.join(SHOTS, `home-${tag}.png`), fullPage: true });

      await page.click('.tab[data-tab="study"]');
      await page.click('button[data-lec="3"]');
      await page.check("#hideM");
      await page.evaluate(() => document.querySelectorAll("details.sec").forEach((d, i) => { if (i < 2) d.open = true; }));
      await page.locator("details.sec .m").first().click();
      await noOverflow(page, "study"); await page.screenshot({ path: path.join(SHOTS, `study-${tag}.png`) });
      await page.evaluate(() => document.querySelectorAll("details.sec").forEach(d => d.open = true));
      await noOverflow(page, "study (all open)");
      await page.click('button[data-lec="2"]');
      await page.evaluate(() => document.querySelectorAll("details.sec").forEach(d => d.open = true));
      await noOverflow(page, "study L2");
      for (const sub of ["look", "trap"]) { await page.click(`button[data-sub="${sub}"]`); await noOverflow(page, "study " + sub); }

      await page.click('.tab[data-tab="cards"]');
      await noOverflow(page, "cards picker"); await page.screenshot({ path: path.join(SHOTS, `cards-pick-${tag}.png`) });
      await page.click("#fcStart");
      await page.keyboard.press("Space");
      await page.waitForTimeout(600);
      await noOverflow(page, "card"); await page.screenshot({ path: path.join(SHOTS, `card-${tag}.png`) });

      await page.click('.tab[data-tab="practice"]');
      if (await page.locator('[data-a="quit"]').count()) { await page.click('[data-a="quit"]'); await page.click('[data-a="again"]').catch(() => {}); }
      await page.click('button[data-mode="spell"]');
      await page.click('[data-a="start"]');
      await page.fill("#tin", "hemorhage");
      await page.press("#tin", "Enter");
      await noOverflow(page, "practice"); await page.screenshot({ path: path.join(SHOTS, `practice-${tag}.png`) });

      await page.click('.tab[data-tab="about"]');
      await page.waitForTimeout(800);
      await noOverflow(page, "about"); await page.screenshot({ path: path.join(SHOTS, `about-${tag}.png`) });
      expect(errs, errs.join("\n")).toEqual([]);
    });
  }
}

/* ---------- flashcards ---------- */
test("flashcards: flip, keys, swipe, again reappears, summary, reload", async ({ page }) => {
  await page.setViewportSize({ width: 400, height: 850 });
  const errs = watchErrors(page);
  await page.goto(URL + "#cards");
  await page.uncheck("#fcShuf");
  await page.click("#fcStart");
  const flip = page.locator("#flip");
  const first = await flip.getAttribute("data-id");
  await page.keyboard.press("Space");
  await expect(flip).toHaveClass(/flipped/);
  await page.keyboard.press("1"); // Again -> 3 cards later
  const seen = [];
  for (let i = 0; i < 3; i++) {
    seen.push(await flip.getAttribute("data-id"));
    await page.keyboard.press("Space");
    if (i === 0) { // swipe right on touch = Got it
      await expect(flip).toHaveClass(/flipped/);
      const b = await page.locator("#flip").boundingBox();
      await page.mouse.move(b.x + 60, b.y + 150); await page.mouse.down();
      await page.mouse.move(b.x + 160, b.y + 150, { steps: 5 }); await page.mouse.move(b.x + 260, b.y + 150, { steps: 5 }); await page.mouse.up();
    } else await page.keyboard.press("3");
  }
  expect(seen).not.toContain(first);
  expect(await flip.getAttribute("data-id")).toBe(first); // the Again card came back
  // swipe left = Again
  await page.keyboard.press("Space");
  await expect(flip).toHaveClass(/flipped/);
  const b = await page.locator("#flip").boundingBox();
  await page.mouse.move(b.x + 300, b.y + 150); await page.mouse.down();
  await page.mouse.move(b.x + 200, b.y + 150, { steps: 5 }); await page.mouse.move(b.x + 80, b.y + 150, { steps: 5 }); await page.mouse.up();
  const st = await page.evaluate(() => window.MT.FC.s.stats);
  expect(st).toEqual({ got: 3, hard: 0, again: 2 });

  // progress survives reload
  const boxesBefore = await page.evaluate(() => window.MT.store.get("boxes", {}));
  expect(boxesBefore[first].b).toBe(1);
  await page.reload();
  const boxesAfter = await page.evaluate(() => window.MT.store.get("boxes", {}));
  expect(boxesAfter).toEqual(boxesBefore);
  await expect(page.locator('[data-a="resume"]')).toBeVisible();
  await expect(page.locator("button[data-weak]")).toContainText("(1)");

  // summary on a small deck: a Again, b Got, c Got, a Got (Hard checked with key 2 once)
  await page.evaluate(() => { const ids = window.MT.CARDS.slice(0, 3).map(c => c.id); window.MT.FC.cfg.shuffle = false; window.MT.FC.begin(ids, "test"); });
  const seq = ["1", "2", "3", "3", "3"]; // a again; b hard (8 later -> end); c got; a got; b got
  for (const k of seq) { await page.keyboard.press("Space"); await page.keyboard.press(k); }
  await expect(page.locator("#sumStats [data-k=got]")).toHaveText("3");
  await expect(page.locator("#sumStats [data-k=hard]")).toHaveText("1");
  await expect(page.locator("#sumStats [data-k=again]")).toHaveText("1");
  await expect(page.locator('[data-a="drill"]')).toContainText("Drill these 2");
  await page.screenshot({ path: path.join(SHOTS, "cards-summary-400.png") });
  expect(errs, errs.join("\n")).toEqual([]);
});

test("works with localStorage throwing", async ({ page }) => {
  await page.addInitScript(() => {
    Object.defineProperty(window, "localStorage", { configurable: true, get() { throw new DOMException("blocked", "SecurityError"); } });
  });
  const errs = watchErrors(page);
  await page.goto(URL + "#home");
  await expect(page.locator(".hero .word")).toBeVisible();
  await page.click('[data-act="cards"]');
  await page.click("#fcStart");
  await page.keyboard.press("Space"); await page.keyboard.press("3");
  await page.click('.tab[data-tab="practice"]');
  await page.click('[data-a="start"]');
  await expect(page.locator("#qnum")).toContainText("1 /");
  await page.click('.tab[data-tab="study"]');
  expect(await page.locator("tr[data-row]").count()).toBeGreaterThan(0);
  expect(errs, errs.join("\n")).toEqual([]);
});

/* ---------- practice ---------- */
test("practice: 30 quizzes x all modes, MCQs valid; typed answers", async ({ page }) => {
  const errs = watchErrors(page);
  await page.goto(URL + "#practice");
  const r = await page.evaluate(() => {
    const { makeQuiz, overlap, retryForm } = window.MT, bad = [];
    let mcqs = 0;
    const checkMcq = (q, where) => {
      mcqs++;
      const o = q.options;
      if (o.length !== 4) bad.push(`${where} ${q.id} has ${o.length} options`);
      if (new Set(o.map(x => x.toLowerCase())).size !== o.length) bad.push(`${where} ${q.id} duplicate options`);
      if (o.filter(x => x === q.answer).length !== 1) bad.push(`${where} ${q.id} answer count`);
      if (/^The (prefix|root|suffix) “/.test(q.q)) { const c = o.filter(x => overlap(x, q.answer)).length; if (c !== 1) bad.push(`${where} ${q.id} ${c} options overlap the answer: ${o.join(" | ")}`); }
      const m = /^Which (prefix|root|suffix) means “(.+)”?$/.exec(q.q);
      if (m) { const c = o.filter(p => window.MT.meaningOfPart(p, m[1]) && overlap(window.MT.meaningOfPart(p, m[1]), m[2])).length; if (c !== 1) bad.push(`${where} ${q.id} ${c} parts share the meaning: ${o.join(" | ")}`); }
    };
    for (const mode of ["mixed", "spell", "mcq", "analyze"]) for (let i = 0; i < 30; i++) {
      const qs = makeQuiz(mode, [1, 2, 3, 4, 5], 40);
      qs.forEach(q => { if (q.type === "mcq") checkMcq(q, mode); const rf = retryForm(q); if (rf.type === "mcq") checkMcq(rf, "retry"); });
    }
    return { bad, mcqs };
  });
  expect(r.bad, r.bad.slice(0, 10).join("\n")).toEqual([]);
  expect(r.mcqs).toBeGreaterThan(500);

  const t = await page.evaluate(() => {
    const { QS, checkTyped, firstDiff, genPartQ, CARD } = window.MT;
    const olig = QS.find(q => (q.type === "spell" || q.type === "build") && q.answer.includes("oliguria"));
    const hem = QS.find(q => (q.type === "spell" || q.type === "build") && q.answer[0] === "hemorrhage");
    const one = genPartQ(CARD["r:num:mon/o"]);
    return { o1: checkTyped(olig, "Oligouria"), o2: checkTyped(olig, "oliguria"), o3: checkTyped(olig, " Olig-uria "),
      h: checkTyped(hem, "hemorhage"), hd: firstDiff("hemorrhage", "hemorhage"),
      uni: checkTyped(one, "uni"), mono: checkTyped(one, "mon/o"), mono2: checkTyped(one, "mono"), di: checkTyped(one, "di") };
  });
  expect(t).toEqual({ o1: true, o2: true, o3: true, h: false, hd: 4, uni: true, mono: true, mono2: true, di: false });

  // same through the UI
  await page.evaluate(() => {
    const { QS, PR, genPartQ, CARD } = window.MT;
    PR.begin([QS.find(q => q.answer && q.answer[0] === "hemorrhage"), genPartQ(CARD["r:num:mon/o"])], "ui");
  });
  await page.fill("#tin", "hemorhage"); await page.press("#tin", "Enter");
  await expect(page.locator(".fb.no")).toBeVisible();
  await expect(page.locator(".diff")).toHaveAttribute("data-diff", "4");
  await expect(page.locator(".diff mark")).toHaveText("r");
  await page.click("#next");
  await page.fill("#tin", "uni"); await page.press("#tin", "Enter");
  await expect(page.locator(".fb.ok")).toBeVisible();
  await page.click("#next");
  await expect(page.locator("h2")).toContainText("Score: 1 / 2");
  await page.click('[data-a="retry"]');
  await expect(page.locator("#qnum")).toContainText("1 / 1");
  // analyse mode: reveal + self grade, missed term comes back
  await page.evaluate(() => window.MT.PR.start({ mode: "analyze", lecs: [4], n: 3 }));
  await page.click('[data-a="reveal"]');
  await expect(page.locator(".ptable")).toBeVisible();
  await page.click('[data-self="0"]');
  await expect(page.locator("#qnum")).toContainText("/ 4");
  expect(errs, errs.join("\n")).toEqual([]);
});

/* ---------- study completeness ---------- */
test("every content.json row appears in Study", async ({ page }) => {
  await page.goto(URL + "#study");
  let total = 0;
  for (const l of [1, 2, 3, 4, 5]) {
    await page.click(`button[data-lec="${l}"]`);
    for (const s of CONTENT.sections.filter(x => x.lec === l)) {
      const n = await page.locator(`tr[data-row="${s.id}"]`).count();
      expect(n, `section ${s.id}`).toBe(s.rows.length);
      total += n;
    }
    if (l === 2) {
      expect(await page.locator("tr[data-pron]").count()).toBe(CONTENT.pronunciation.length);
      expect(await page.locator("tr[data-plural]").count()).toBe(CONTENT.plurals.length);
    }
  }
  expect(total).toBe(CONTENT.sections.reduce((a, s) => a + s.rows.length, 0));
});

/* ---------- regressions (bugs fixed 2026-10-24) ---------- */
const KIND_OF = {};
CONTENT.sections.forEach(s => s.rows.forEach(r => [r.part, ...r.alts].forEach(f => { KIND_OF[f.toLowerCase()] = KIND_OF[f.toLowerCase()] || s.kind; })));

test("look-alikes: every part has the colour of its own table (prefixes were green)", async ({ page }) => {
  await page.goto(URL + "#study");
  await page.click('button[data-sub="look"]');
  const cells = await page.$$eval("td.c-part", tds => tds.map(td => ({ text: td.innerText.replace(/\s+/g, ""), cls: [...td.querySelectorAll(".hl")].map(e => e.className) })));
  const rows = CONTENT.lookalikes.flatMap(g => g.rows);
  expect(cells.length).toBe(rows.length);
  const bad = [];
  rows.forEach((r, i) => {
    const want = KIND_OF[r.part.split(/,\s*/)[0].toLowerCase()];
    if (want && cells[i].cls.some(c => !c.includes("k-vowel") && !c.includes("k-" + want))) bad.push(`${r.part}: want ${want}, got ${cells[i].cls}`);
  });
  expect(bad, bad.join("\n")).toEqual([]);
  // spot checks that were wrong before
  for (const p of ["dia", "hyper-", "mon/o", "pre-"]) expect(KIND_OF[p]).toBe("prefix");
});

test("practice: lengths 15/25/40/60; exact count, or a clear message when fewer exist", async ({ page }) => {
  await page.goto(URL + "#practice");
  await expect(page.locator("button[data-n]")).toHaveText(["15", "25", "40", "60"]);
  const pick = async (lec, n) => {
    await page.evaluate(() => { window.MT.PR.run = null; }); await page.click('.tab[data-tab="home"]'); await page.click('.tab[data-tab="practice"]');
    await page.click('button[data-mode="mixed"]');
    for (const x of [1, 2, 3, 4, 5]) { const on = await page.getAttribute(`button.chip[data-lec="${x}"]`, "aria-pressed") === "true"; if (on !== (x === lec)) await page.click(`button.chip[data-lec="${x}"]`); }
    await page.click(`button[data-n="${n}"]`);
    await page.click('[data-a="start"]');
  };
  await pick(3, 15);
  await expect(page.locator("#qnum")).toHaveText("1 / 15");
  await expect(page.locator("#shortMsg")).toHaveCount(0);
  await pick(1, 60); // L1 has fewer than 60
  const have = await page.evaluate(() => window.MT.makeQuiz("mixed", [1], 9999).length);
  expect(have).toBeLessThan(60);
  await expect(page.locator("#qnum")).toHaveText(`1 / ${have}`);
  await expect(page.locator("#shortMsg")).toContainText(`Only ${have} questions`);
  // an old saved length (10) maps to a valid option
  await page.evaluate(() => localStorage.setItem("mt:prCfg", JSON.stringify({ mode: "mixed", lecs: [3], n: 10 })));
  await page.reload();
  await expect(page.locator('button[data-n="15"]')).toHaveAttribute("aria-pressed", "true");
});

test("flashcards: a swipe right after flipping (mid-animation) still grades", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto(URL + "#cards");
  await page.click("#fcStart");
  const flip = page.locator("#flip");
  for (let i = 0; i < 5; i++) {
    const before = await page.evaluate(() => ({ ...window.MT.FC.s.stats }));
    await page.keyboard.press("Space");
    const b = await flip.boundingBox(); // no wait for the 0.45 s rotation
    await page.mouse.move(b.x + b.width - 40, b.y + 120); await page.mouse.down();
    await page.mouse.move(b.x + b.width / 2, b.y + 120, { steps: 4 }); await page.mouse.move(b.x + 30, b.y + 120, { steps: 4 }); await page.mouse.up();
    await expect.poll(() => page.evaluate(() => window.MT.FC.s.stats.again)).toBe(before.again + 1);
  }
});

test("share: live SITE_URL, no placeholder, link is a 44px tap target", async ({ page }) => {
  await page.goto(URL + "#about");
  await page.click('.tab[data-tab="about"]');
  expect(await page.content()).not.toContain("example.com");
  await expect(page.locator("#siteLink")).toHaveAttribute("href", "https://terminology-med-revision.vercel.app");
  const b = await page.locator("#siteLink").boundingBox();
  expect(b.height).toBeGreaterThanOrEqual(44);
});

test("no failed network requests (favicon.ico was a 404 on Vercel)", async ({ page }) => {
  const bad = [];
  page.on("response", r => { if (r.status() >= 400) bad.push(r.status() + " " + r.url()); });
  page.on("requestfailed", r => { if (!/fonts\.(googleapis|gstatic)\.com/.test(r.url())) bad.push("failed " + r.url()); }); // font CDN timeouts = local network, not the site
  await page.goto(URL + "#home", { waitUntil: "networkidle" });
  for (const tab of ["study", "cards", "practice", "about"]) await page.click(`.tab[data-tab="${tab}"]`);
  await page.waitForLoadState("networkidle");
  await expect(page.locator('link[rel="icon"]')).toHaveCount(1);
  expect(bad, bad.join("\n")).toEqual([]);
});
