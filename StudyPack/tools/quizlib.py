"""Quiz assembly + answer grading / mistake diagnosis (E1–E6) for the Stage 3b bank.

Reference implementation: the website's JS mirrors these rules, and the QA scripts (ramp check, feedback check,
spot-check) call it directly.
    from quizlib import Bank
    b = Bank(content)                       # content = parsed content.json
    qs, short = b.assemble(level="mix", n=20, seed=1, order="ramp")
    res = b.grade(q, response)              # {ok, code, ar, credit, max, notes}
Codes: None correct · OK-NS correct but not slide wording · E1 look-alike · E2 wrong part isolated · E3 spelling ·
E4 combining-vowel rule · E5 right part, wrong meaning · E6 blank / unknown.
"""
import re, random, unicodedata

LEVELS = ["easy", "medium", "hard", "max"]
MIX = {"easy": 20, "medium": 35, "hard": 30, "max": 15}
BLANK = {"", "?", "-", "idk", "i don't know", "dont know", "مش عارف"}


def norm(s):
    s = unicodedata.normalize("NFKC", str(s)).lower().strip()
    s = s.replace("–", "-").replace("—", "-").replace("’", "'").replace("“", '"').replace("”", '"')
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"^(the )?(prefix|suffix|root|answer|it is|it's)\s*(is\s*)?[:=]?\s*", "", s)
    return s.strip(" .")


def nform(s):
    """compare word parts: hyphens, slashes and spaces ignored (ante- = ante = Ante; cyst/o = cysto)."""
    return re.sub(r"[\s\-/]", "", norm(s))


def lev(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def first_diff(a, b):
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y: return i
    return min(len(a), len(b))


def slip(resp, ans):
    r, a = resp, ans
    if "rrh" in a and "rrh" not in r: return "الـ rrh لازم r مرتين + h"
    if len(r) == len(a) - 1 and any(a[i] == a[i + 1] and a[:i] + a[i + 1:] == r for i in range(len(a) - 1)): return "حرف مضاعف ناقص"
    if len(r) == len(a) + 1 and any(r[i] == r[i + 1] and r[:i] + r[i + 1:] == a for i in range(len(r) - 1)): return "حرف مضاعف زيادة"
    if r.replace("f", "ph") == a: return "ph مش f"
    if len(r) == len(a) and sum(x != y for x, y in zip(r, a)) == 1 and {r[first_diff(r, a)], a[first_diff(r, a)]} == {"i", "y"}: return "y مش i"
    if re.search(r"ae|oe", r) and not re.search(r"ae|oe", a): return "دي spelling بريطاني — السلايد أمريكي"
    return None


class Bank:
    def __init__(self, content):
        self.C = content
        self.Q = content["questions"]
        self.rows = []
        for s in content["sections"]:
            for r in s["rows"]:
                self.rows.append(dict(r, lec=s["lec"], sid=s["id"], kind=s["kind"]))
        self.analysis = {a["term"].lower(): a for a in content["analysis"]}
        self.lec_of = {l["file"]: l["n"] for l in content["meta"]["lectures"]}

    def _ref(self, e):   # the lecture the evidence page belongs to (a rule on L2 cited for an L5 term)
        return f"L{self.lec_of.get(e['file'], '?')}·s{e['page']}"

    def _prefix_o(self, best, j):
        """the o at index j ends a prefix (homo-, hypo-) → a misspelled prefix, not a combining vowel"""
        for row in self.rows:
            if row["kind"] != "prefix": continue
            for f in [row["part"]] + row["alts"]:
                f = nform(f)
                if f.endswith("o") and len(f) == j + 1 and best.startswith(f):
                    return row
        return None

    # ------------------------------------------------------------------ assembly
    def _text(self, q):
        return norm(q["q"] + " " + " ".join(map(str, q.get("options", []))))

    def _leaks(self, a, b):
        """True if a's answer / tested parts / term would be given away by b's stem or options (G3)."""
        tb = self._text(b)
        return any(re.search(r"(?<![a-z])" + re.escape(t) + r"(?![a-z])", tb) for t in a.get("leak", []))

    def _parts(self, q):
        return {re.sub(r"[^a-z]", "", t.split(",")[0]) for t in q["tests"]} - {""}

    def assemble(self, level="mix", n=20, lecs=None, patterns=None, seed=0, order="ramp"):
        rng = random.Random(seed)
        pool = [q for q in self.Q if (not lecs or q["lec"] in lecs) and (not patterns or q["pattern"] in patterns)]
        if level != "mix":
            want = {level: n}
        else:
            raw = {l: n * MIX[l] / 100 for l in LEVELS}
            want = {l: int(raw[l]) for l in LEVELS}
            for l in sorted(LEVELS, key=lambda l: raw[l] - int(raw[l]), reverse=True)[: n - sum(want.values())]:
                want[l] += 1
        picked = []
        for l in LEVELS:
            cand = [q for q in pool if q["difficulty"] == l]
            rng.shuffle(cand)
            got = 0
            for c in cand:
                if got >= want.get(l, 0): break
                if any(self._leaks(c, p) or self._leaks(p, c) for p in picked): continue
                if any(p.get("term") and p.get("term") == c.get("term") for p in picked): continue
                picked.append(c); got += 1
        short = n - len(picked)
        if order == "ramp":
            picked.sort(key=lambda q: (q["score"], q["tie"]))
        else:
            rng.shuffle(picked)
        # no two consecutive questions on the same word part (swap with the nearest safe neighbour)
        for i in range(1, len(picked)):
            if self._parts(picked[i]) & self._parts(picked[i - 1]):
                for j in range(i + 1, len(picked)):
                    ok_prev = not (self._parts(picked[j]) & self._parts(picked[i - 1]))
                    ok_next = i + 1 >= len(picked) or not (self._parts(picked[i]) & self._parts(picked[j + 1] if j + 1 < len(picked) else {"tests": []}))
                    if ok_prev and ok_next:
                        picked[i], picked[j] = picked[j], picked[i]
                        break
        if order == "ramp":   # keep the ramp non-decreasing by level after the swaps
            picked.sort(key=lambda q: LEVELS.index(q["difficulty"]))
        return picked, max(0, short)

    # ------------------------------------------------------------------ grading
    def _row_of(self, part):
        p = nform(part)
        for r in self.rows:
            if p in [nform(f) for f in [r["part"]] + r["alts"]]:
                return r
        return None

    def _same_part(self, q):
        out = []
        for t in q["tests"]:
            r = self._row_of(t)
            if r:
                out += [f"{e.strip()} (L{r['lec']}·s{r['page']})" for e in re.split(r"\s*·\s*", r["example"]) if e.strip() and e.strip().lower() != str(q.get("term", "")).lower()]
        return out[:2]

    def _typed(self, q, resp, accept, answer, emap):
        r = norm(resp)
        ref = self._ref(q["evidence"][0])
        if r in BLANK:
            return dict(ok=False, code="E6", ar=f"الإجابة: {answer}. {q['explain_ar']}")
        if r in [norm(a) for a in q.get("acceptNotSlide", [])]:
            return dict(ok=True, code="OK-NS", ar=f"صح كتركيب، بس الكلمة اللي في السلايد {answer} — اكتبها هي في الامتحان.")
        accs = [norm(a) for a in accept] + [norm(answer)]
        if r in accs or nform(r) in [nform(a) for a in accs]:
            return dict(ok=True, code=None, ar="صح")
        if q["pattern"] == "P11":
            if r in ("no mistake", "no mistakes", "none", "correct", "all correct") and q.get("mistakes"):
                return dict(ok=False, code="E1", ar=emap.get(norm("no mistake"), q["explain_ar"]))
            if not q.get("mistakes"):
                return dict(ok=False, code="E1", ar=f"التحليل كان صح ومفيهوش غلطة. {q['explain_ar']}")
        if r in emap or nform(r) in {nform(k): v for k, v in emap.items()}:
            txt = emap.get(r) or {nform(k): v for k, v in emap.items()}[nform(r)]
            return dict(ok=False, code="E1", ar=txt)
        # look-alike against the whole slide index (another part or another part's meaning)
        for row in self.rows:
            forms = [nform(f) for f in [row["part"]] + row["alts"]]
            if nform(r) in forms and nform(r) not in [nform(t) for t in q["tests"]] and len(nform(r)) >= 2:
                return dict(ok=False, code="E1", ar=f"{row['part']} معناها {row['meaning']} (L{row['lec']}·s{row['page']})، ومش هي المطلوبة هنا. الإجابة: {answer}. {q['explain_ar']}")
        # wrong part isolated: the meaning of ANOTHER part of the same term
        a = self.analysis.get(str(q.get("term", "")).lower())
        if a:
            for p in a["parts"]:
                if p["meaning"] and norm(p["meaning"]) == r and nform(p["text"]) not in [nform(t) for t in q["tests"]]:
                    split = " | ".join(x["text"] for x in a["parts"])
                    tr = next((self._row_of(t) for t in q["tests"] if self._row_of(t)), None)
                    aref = f" (L{tr['lec']}·s{tr['page']})" if tr else ""
                    return dict(ok=False, code="E2", ar=f"دا معنى الـ {p['type']} {p['text']}، مش الجزء المطلوب. التقسيم: {split} ({ref}). الإجابة: {answer}{aref}.")
        # spelling: small edit distance to an accepted answer
        best = min(accs, key=lambda x: lev(r, x))
        if 0 < lev(r, best) <= max(1, len(best) // 5) and len(best) >= 4:
            i = first_diff(r, best)
            miss = next((j for j, ch in enumerate(best) if ch == "o" and best[:j] + best[j + 1:] == r), None)   # o left out
            extra = next((j for j, ch in enumerate(r) if ch == "o" and r[:j] + r[j + 1:] == best), None)    # o added
            j = miss if miss is not None else extra
            pre = self._prefix_o(best, j) if miss is not None else None
            if pre:   # the o belongs to the prefix itself (homo-, hypo-): a misspelled prefix, not a combining vowel (4e)
                return dict(ok=False, code="E3", ar=f"قريبة جدًا! الـ o هنا جزء من الـ prefix {pre['part']} ({pre['meaning']}, L{pre['lec']}·s{pre['page']}) — اكتبه كامل. الصح: {answer} ({ref}).", index=i)
            if miss is not None:
                return dict(ok=False, code="E4", ar=f"قريبة جدًا! ناقص الـ combining vowel o بعد \"{best[:j]}\" — بنحط o بين root و root أو قبل suffix بيبدأ بـ consonant (L2·s10). الصح: {answer} ({ref}).", index=i)
            if extra is not None and best[j:j + 1] in tuple("aeiouy"):
                return dict(ok=False, code="E4", ar=f"قريبة جدًا! الـ o بعد \"{r[:j]}\" زيادة — مفيش combining vowel قبل suffix بيبدأ بـ vowel (L2·s13). الصح: {answer} ({ref}).", index=i)
            if extra is not None:
                return dict(ok=False, code="E3", ar=f"قريبة جدًا! الـ o بعد \"{r[:j]}\" زيادة — مش موجودة في كلمة السلايد. الصح: {answer} ({ref}).", index=i)
            return dict(ok=False, code="E3", ar=f"قريبة جدًا! أول حرف غلط عند الحرف رقم {i + 1} (\"{r[:i]}‹{r[i:i + 1] or '∅'}›…\"). {slip(r, best) or 'راجع الإملاء زي السلايد'}. الصح: {answer} ({ref}).", index=i)
        # copied a word from the slide definition instead of the part's meaning
        for t in q["tests"]:
            row = self._row_of(t)
            if row and len(r) >= 3 and re.search(r"(?<![a-z])" + re.escape(r) + r"(?![a-z])", norm(row["definition"])):
                return dict(ok=False, code="E5", ar=f"\"{resp}\" كلمة من تعريف {row['example']} ({row['definition']})، مش معنى {row['part']}. معنى {row['part']} على السلايد: {row['meaning']} (L{row['lec']}·s{row['page']}).")
        same = self._same_part(q)
        tail = f" نفس الجزء في: {'، '.join(same)}." if same else ""
        return dict(ok=False, code="E5", ar=f"المعنى في السلايد: {answer}. {q['explain_ar']}{tail}")

    def grade(self, q, resp):
        k = q["kind"]
        if k == "mcq":
            ok = resp == q["key"]
            if ok: return dict(ok=True, code=None, ar="صح", credit=1, max=1)
            txt = q.get("errorMap", {}).get(norm(resp)) or f"اخترت {resp}، بس المطلوب {q['key']}. {q['explain_ar']}"
            return dict(ok=False, code="E1", ar=txt, credit=0, max=1)
        if k == "tf":
            ok = (resp is True or str(resp).lower() == "true") == q["answer"]
            return dict(ok=ok, code=None if ok else "E1", ar="صح" if ok else (q.get("correction") or q["explain_ar"]) + " " + q["explain_ar"], credit=int(ok), max=1)
        if k == "typed":
            res = self._typed(q, resp, q["accept"], q["key"], q.get("errorMap", {}))
            return dict(res, credit=int(res["ok"]), max=1)
        if k == "typed2":
            resps = resp if isinstance(resp, list) else [x.strip() for x in str(resp).split("|")]
            notes, credit = [], 0
            for i, (b, rr) in enumerate(zip(q["blanks"], resps + [""] * len(q["blanks"])), 1):
                res = self._typed(q, rr, b["accept"], b["answer"], b.get("errorMap", {}))
                credit += int(res["ok"])
                if not res["ok"]: notes.append(dict(blank=i, **res))
            first = notes[0] if notes else None
            return dict(ok=credit == len(q["blanks"]), code=first["code"] if first else None, ar=first["ar"] if first else "صح",
                        credit=credit, max=len(q["blanks"]), notes=notes)
        # analyze: field by field, partial credit, first wrong field named
        resps = resp if isinstance(resp, list) else [x.strip() for x in str(resp).split("|")]
        credit, first, notes = 0, None, []
        for f, rr in zip(q["fields"], resps + [""] * len(q["fields"])):
            if "accept_part" in f:
                part, _, mean = rr.partition("=")
                ok_p = nform(part) in [nform(x) for x in f["accept_part"]]
                ok_m = (not f.get("meaningGraded")) or norm(mean) in [norm(x) for x in f["accept_meaning"]]
                ok = ok_p and ok_m
                if not ok:
                    if not ok_p:
                        notes.append(dict(field=f["name"], code="E2" if nform(part) else "E6", ar=f"{f['name']}: التقسيم زي السلايد — {f['answer']}"))
                    else:
                        sub = self._typed(q, mean, f["accept_meaning"], f["accept_meaning"][0] if f["accept_meaning"] else "", {})
                        notes.append(dict(field=f["name"], code=sub["code"], ar=f"{f['name']}: {sub['ar']}"))
            elif f["name"] == "Medical meaning":
                r = norm(rr)
                kw = f.get("keywords", [])
                ok = r in [norm(x) for x in f["accept"]] or (kw and sum(w in r for w in kw) / len(kw) >= 0.6)
                if not ok: notes.append(dict(field=f["name"], code="E6" if not r else "E5", ar=f"Medical meaning زي السلايد: {f['answer']}"))
            else:
                ok = norm(rr) in [norm(x) for x in f["accept"]]
                if not ok: notes.append(dict(field=f["name"], code="E2", ar=f"{f['name']}: {f['answer']}"))
            credit += int(ok)
            if not ok and first is None: first = f["name"]
        return dict(ok=credit == len(q["fields"]), code=notes[0]["code"] if notes else None, ar=notes[0]["ar"] if notes else "صح",
                    credit=credit, max=len(q["fields"]), firstWrong=first, notes=notes)
