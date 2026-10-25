"""Stage 3b exam-grade question bank (pattern library P1–P14). Called by build_content.py: Q = bank.build(module).

Every question is slide-only (R0–R8) and carries: id, lec, slide, type (legacy for the current UI: mcq|tf|spell|analyze),
kind (mcq|tf|typed|typed2|analyze), pattern, difficulty, score, skill, q, options, answer, accept, acceptNotSlide, key,
evidence [{file, page, quote}], tests, leak, errorMap, explain_ar (+ fields / blanks / mistakes / correction when relevant).

Difficulty = cognitive operation (never the pattern name alone):
  easy   one-step recall in the slide's own direction (named part → meaning), hints allowed      P2e, P14
  medium one step reversed or produced (meaning → part, isolate the part, complete a definition)  P2, P4, P5, P6, P10, P14
  hard   two steps / discrimination (definition → term, specialty from scope, contrast, transfer, 2-part analysis,
         irregular plural)                                                                      P1, P3, P7, P8, P9, P10, P13
  max    ≥ 2 distinct steps, zero hints (error-find, odd-one-out + meaning, both halves of a contrast,
         two-part transfer, analysis of a 3+-part term)                                         P1, P8, P9, P11, P12

Score 1–100 = band floor (easy 1 · medium 26 · hard 51 · max 76) + points, capped at band floor + 24:
  +6 typed · +4 reverse direction · +3 per part beyond the first · +3 no hint · +4 look-alike distractors/partner
  · +0..4 answer length / irregular spelling (rrh, ph, ps/pn/pt, x, y inside, double letters) · +3 rule exception
  · +4 two-part transfer (+2 more across lectures; a one-part transfer is capped at +6 = start of the hard band)
  · +5 error-find / odd-one-out · analysis: +3 per graded field beyond the first, +4 multi-step.  Ties broken by a seeded number.
"""
import re, random

LEVELS = ["easy", "medium", "hard", "max"]
FLOOR = {"easy": 1, "medium": 26, "hard": 51, "max": 76}
TYPED_KINDS = {"typed", "typed2", "analyze"}
NO_MISTAKE = ["no mistake", "no mistakes", "none", "correct", "all correct"]
KIND_NAME = {"prefix": "prefix", "root": "root", "suffix": "suffix"}


def build(B):
    rng = random.Random(B.SEED + 7)
    D = B.D
    Q = []
    TPL = {}

    # ------------------------------------------------------------------ helpers
    def norm(s):
        return B.gnorm(s)

    def core(p):
        return re.sub(r"[^a-z]", "", str(p).lower().split(",")[0])

    def comps(m):
        """accepted pieces of a slide meaning: the whole cell + each comma / dash piece (and 'x or y' pieces)."""
        m = m.strip()
        out = [m]
        pieces = re.split(r",\s*|\s+-\s+", m)
        if " or " in m and " for " not in f" {m} ":
            pieces = [x for p in pieces for x in p.split(" or ")]
        for p in pieces + [re.sub(r"\s*\(.*?\)", "", m)]:
            p = p.strip()
            for v in (p, re.sub(r"^(a|an) ", "", p, flags=re.I)):
                if len(v) >= 2 and v not in out and v.lower() not in ("of", "the", "and", "or", "to"):
                    out.append(v)
        for a, bs in SPELL_VARIANTS.items():
            for x in list(out):
                if a in x.lower():
                    out += [x.lower().replace(a, b) for b in bs if x.lower().replace(a, b) not in out]
        return out

    SPELL_VARIANTS = {"rupture": ["reputure", "rapture"], "grey": ["gray"], "gray": ["grey"]}
    TAGS = {"-gram": ["record"], "-ectomy": ["excision"], "-rhage": ["flow"], "-pathy": ["disease"], "-rhexis": ["rupture"], "-oma": ["tumor"], "-schisis": ["splitting"]}  # slide example labels (L4 s14)
    ALIAS = {"karyoclasis": ["karyolysis"]}   # printed beside the term on L4 s13
    EXCLUDE_TERMS = {"Xerosis"}               # slide colour split is ambiguous (Xero|sis vs Xer|osis): never asked "as split"

    def ref(lec, page):
        return f"L{lec}·s{page}"

    LEC_OF = {f: l for l, f in B.FILE.items()}
    def evref(e):   # cite the lecture the evidence page belongs to, not the term's lecture (4f: rule 1 is L2·s10)
        return ref(LEC_OF[e["file"]], e["page"])

    def forms_accept(r):
        acc = []
        for x in B.accept_parts(r):
            for v in (x, x.strip("-"), x.replace("/", ""), x.rstrip("/").split("/")[0]):
                v = v.strip()
                if v and v not in acc:
                    acc.append(v)
        return acc

    def forms_exact(r, only_self=False):
        acc = []
        rows = [r] if only_self else [o for o in ROWS if norm(o["meaning"]) == norm(r["meaning"]) and o["kind"] == r["kind"]]
        for o in rows:
            for f in o["forms"] + B.ACCEPT_BOTH.get(o["part"], []):
                for v in (f, f.strip("-"), f.replace("/", ""), f.rstrip("/").split("/")[0]):
                    v = v.strip().lower()
                    if v and v not in acc: acc.append(v)
        return acc

    def disp(part):
        return part[0].upper() + part[1:] if part[0].isalpha() else part[0] + part[1].upper() + part[2:]

    def Ex(w):
        return w[0].upper() + w[1:] if w else w

    def tpl(key, variants, i):
        t = variants[i % len(variants)]
        TPL.setdefault(f"{key}:{variants.index(t)}", 0)
        TPL[f"{key}:{variants.index(t)}"] += 1
        return t, f"{key}:{variants.index(t)}"

    def add(lec, kind, pattern, level, skill, q, key, accept, evidence, tests, ar, tplid, options=None, **kw):
        legacy = {"mcq": "mcq", "tf": "tf", "typed": "spell", "typed2": "analyze", "analyze": "analyze"}[kind]
        if kind == "mcq":
            answer = key
        elif kind == "tf":
            answer = key
        elif kind == "typed":
            answer = list(dict.fromkeys([key] + list(accept) + list(kw.get("acceptNotSlide", []))))
        else:
            answer = accept or [key]
        if not re.search(r"L\d·s\d", ar):
            ar += f" ({evref(evidence[0])})"
        item = {"id": "", "lec": lec, "slide": str(evidence[0]["page"]), "type": legacy, "kind": kind, "pattern": pattern,
                "difficulty": level, "skill": skill, "q": q, "options": options or [], "answer": answer, "key": key,
                "accept": [a for a in accept], "acceptNotSlide": kw.pop("acceptNotSlide", []), "explain_ar": ar,
                "evidence": evidence, "tests": sorted({t.lower() for t in tests if t}), "tpl": tplid}
        item.update(kw)
        Q.append(item)
        return item

    ROWS = [r for r in B.ROWS]
    for r in ROWS:
        r["comps"] = comps(r["meaning"])
        for x in TAGS.get(r["part"], []):
            r["comps"] += [c for c in comps(x) if c not in r["comps"]]
        r["one"] = r["ex1"] if re.fullmatch(r"[A-Za-z]+", r["ex1"] or "") and not r["typo"] else ""

    for r in ROWS:
        for o in ROWS:
            if o is not r and o["kind"] == r["kind"] and core(o["part"]) == core(r["part"]):
                r["comps"] += [c for c in o["comps"] if c not in r["comps"]]

    def best_form(r, word):
        """the form of the part that the slide example actually uses (An- in Analgesia, -ician in Physician)."""
        w = (word or "").lower()
        fs = sorted(r["forms"], key=lambda f: -len(core(f)))
        for f in fs:
            c = core(f)
            if c and ((r["kind"] == "suffix" and w.endswith(c)) or (r["kind"] != "suffix" and w.startswith(c))):
                return f
        return r["part"]

    def find_row(part):
        p = part.lower()
        for r in ROWS:
            if p in [f.lower() for f in r["forms"]] and r["sid"] != "numchart":
                return r
        return None

    LOOK = [g for g in B.LOOK]
    def look_of(r):
        return next((g for g in LOOK if r in g), None)

    def distinct(a, b):
        """two rows that are safe as each other's distractor / swap partner."""
        return a is not b and not B.row_near(a, b)

    def neighbours(r, n, need=lambda o: True):
        """look-alike group first, then same slide table, then same lecture & kind — mutually distinct."""
        g = look_of(r) or []
        pools = [[o for o in g if o is not r], [o for o in ROWS if o["sid"] == r["sid"]],
                 [o for o in ROWS if o["lec"] == r["lec"] and o["kind"] == r["kind"]]]
        out = []
        for i, pool in enumerate(pools):
            cands = [o for o in pool if distinct(r, o) and need(o) and o not in out and o["sid"] != "numchart"]
            rng.shuffle(cands)
            for o in cands:
                if len(out) == n: break
                if any(not distinct(o, d) for d in out): continue
                out.append(o)
        return out if len(out) == n else None

    def emap(r, extra=()):
        """pre-computed E1 targets: the meanings / forms of the look-alike rows → why they are wrong here."""
        out = {}
        for o in (look_of(r) or []) + [x for x in ROWS if x["sid"] == r["sid"]] + list(extra):
            if o is r or B.syn(o["part"], r["part"]): continue
            for m in o["comps"][:3]:
                out.setdefault(norm(m), f"{m} دا معنى {o['part']} ({ref(o['lec'], o['page'])}). الإجابة هنا: {r['part']} = {r['meaning']} ({ref(r['lec'], r['page'])}).")
            for f in o["forms"]:
                out.setdefault(norm(f), f"{f} معناها {o['meaning']} ({ref(o['lec'], o['page'])}). الإجابة هنا: {r['part']} = {r['meaning']} ({ref(r['lec'], r['page'])}).")
        return dict(list(out.items())[:10])

    def same_in(r, exclude=""):
        exs = [e for e in r["ex"] if e.lower() != exclude.lower()]
        return exs[:2]

    def expl(r, extra=""):
        sp = same_in(r)
        tail = f" نفس الجزء في: {'، '.join(Ex(x) for x in sp)}." if len(sp) > 1 else ""
        return f"{r['part']} معناها {r['meaning']}" + (f" — مثال السلايد: {Ex(r['ex1'])} = {r['def1']}" if r["ex1"] and r["def1"] else "") + f" ({ref(r['lec'], r['page'])}).{extra}{tail}"

    SLOT = [0]
    def mcq_opts(key, ds):
        ds = ds[:]
        rng.shuffle(ds)
        pos = SLOT[0] % 4
        SLOT[0] += 1
        return ds[:pos] + [key] + ds[pos:]

    def short_ok(a, ds):
        L = [len(x) for x in [a] + ds]
        return max(L) <= 3 * min(L) + 8

    multi_meaning = {}
    for r in ROWS:
        if r["sid"] == "numchart": continue
        multi_meaning.setdefault(norm(r["meaning"]), []).append(r)

    # ------------------------------------------------------------------ row patterns
    def P2e(r, i):  # easy: named part in a named term -> meaning (typed, hint)
        if r["one"] and core(r["part"])[:3] in r["one"].lower():
            t, tid = tpl("P2e", ["In the term {ex}, the {k} {p} means ……", "{p} in \"{ex}\" means ……", "What does the {k} {p} mean in {ex}? ……"], i)
            q = t.format(ex=Ex(r["one"]), k=r["kind"], p=disp(best_form(r, r["one"])))
        else:
            t, tid = tpl("P2e0", ["The {k} {p} means ……", "Write the slide meaning of the {k} {p}: ……"], i)
            q = t.format(k=r["kind"], p=disp(r["part"]))
        return add(r["lec"], "typed", "P2", "easy", "recall", q, r["meaning"], r["comps"], [B.rev(r)], [r["part"]], expl(r), tid,
                   hint=True, errorMap=emap(r))

    def P14e(r, i):  # easy MCQ: part -> meaning, look-alike distractors
        ds = neighbours(r, 3, lambda o: not B.overlap(o["meaning"], r["meaning"]))
        if not ds: return None
        dm = [d["meaning"] for d in ds]
        if not short_ok(r["meaning"], dm) or len({norm(x) for x in dm + [r["meaning"]]}) < 4: return None
        t, tid = tpl("P14e", ["According to the slides, the {k} {p} means:", "On the slide, {p} (as in {ex}) means:"], i if r["one"] else 0)
        q = t.format(k=r["kind"], p=disp(best_form(r, r["one"]) if r["one"] else r["part"]), ex=Ex(r["one"]))
        return add(r["lec"], "mcq", "P14", "easy", "recall", q, r["meaning"], [r["meaning"]], [B.rev(r)] + [B.rev(d) for d in ds],
                   [r["part"]], expl(r), tid, options=mcq_opts(r["meaning"], dm), close=bool(look_of(r)), errorMap=emap(r, ds))

    def P2m(r, i):  # medium: isolate the part inside the slide term, give its meaning
        w = r["one"]
        if not w or r["kind"] == "root": return None
        c = core(r["part"])
        if r["kind"] == "prefix" and not w.lower().startswith(c[:3]): return None
        if r["kind"] == "suffix" and not w.lower().endswith(c[-3:]): return None
        t, tid = tpl("P2", ["The {k} in the term \"{ex}\" means ……", "In \"{ex}\", the {k} means ……", "Give the slide meaning of the {k} in {ex}: ……"], i)
        q = t.format(k=r["kind"], ex=Ex(w))
        return add(r["lec"], "typed", "P2", "medium", "isolate", q, r["meaning"], r["comps"], [B.rev(r)], [r["part"]], expl(r), tid,
                   errorMap=emap(r), term=w)

    def P6(r, i):  # medium: meaning -> part (typed)
        if r["sid"] in ("numchart",) or len(multi_meaning[norm(r["meaning"])]) >= 3: return None
        if core(r["part"])[:4] in norm(r["meaning"]).replace(" ", ""): return None
        t, tid = tpl("P6", ["Write the {k} that means \"{m}\".", "Which {k} on the slides means \"{m}\"? Write it: ……", "\"{m}\" — write the {k}: ……"], i)
        q = t.format(k=r["kind"], m=r["meaning"])
        if any(o is not r and norm(o["meaning"]) != norm(r["meaning"]) and norm(r["meaning"]) in [norm(c) for c in o["comps"]] for o in ROWS):
            return None
        acc = forms_exact(r)
        return add(r["lec"], "typed", "P6", "medium", "reverse", q, r["part"], acc, [B.rev(r)], [r["part"]], expl(r), tid,
                   errorMap=emap(r))

    def P4(r, i):  # medium: "<Term> means …… <rest of slide definition>"
        w, d = r["one"], r["def1"]
        if not w or not d: return None
        dl = d.lower()
        for m in sorted(r["comps"], key=len, reverse=True):
            ml = m.lower()
            if dl.startswith(ml + " ") and len(dl) > len(ml) + 3:
                rest = d[len(m):].strip()
                if any(re.search(r"(?<![a-z])" + re.escape(c.lower()) + r"(?![a-z])", rest.lower()) for c in r["comps"]): return None
                if r["sid"] in ("dir", "pos"):
                    pat = "P5"
                else:
                    pat = "P4"
                q = f"{Ex(w)} means …… {rest}."
                fit = [x for x in r["comps"] if x.lower() == ml or (x.lower() in ml and x.lower() in [y.lower() for y in TAGS.get(r["part"], [])])]
                fit += [v for a, bs in SPELL_VARIANTS.items() if a in ml for v in [ml.replace(a, b) for b in bs]]
                return add(r["lec"], "typed", pat, "medium", "isolate", q, m, list(dict.fromkeys(fit)), [B.rev(r)], [r["part"]],
                           expl(r), f"{pat}:0", errorMap=emap(r), term=w)
            if dl.endswith(" " + ml) and r["sid"] in ("dir", "pos") and len(dl) > len(ml) + 3:
                rest = d[: len(d) - len(m)].strip()
                q = f"{Ex(w)}: {rest[0].lower() + rest[1:]} the …… ." if rest.lower().endswith("the") is False else f"{Ex(w)} is {rest[0].lower() + rest[1:]} …… ."
                q = f"{Ex(w)} is {rest[0].lower() + rest[1:]} …… ."
                return add(r["lec"], "typed", "P5", "medium", "isolate", q, m, [m], [B.rev(r)], [r["part"]], expl(r), "P5:1",
                           errorMap=emap(r), term=w)
        return None

    def P14m(r, i):  # medium MCQ: meaning -> part, look-alike parts as distractors
        if len(multi_meaning[norm(r["meaning"])]) >= 2: return None
        ds = neighbours(r, 3, lambda o: not B.overlap(o["meaning"], r["meaning"]))
        if not ds: return None
        t, tid = tpl("P14m", ["According to the slides, which {k} means \"{m}\"?", "\"{m}\" is the meaning of which {k}?"], i)
        q = t.format(k=r["kind"], m=r["meaning"])
        return add(r["lec"], "mcq", "P14", "medium", "reverse", q, r["part"], [r["part"]], [B.rev(r)] + [B.rev(d) for d in ds],
                   [r["part"]], expl(r), tid, options=mcq_opts(r["part"], [d["part"] for d in ds]), close=bool(look_of(r)), errorMap=emap(r, ds))

    def P14tf(r, i):  # medium T/F: one subtle swap with a look-alike
        g = look_of(r)
        if not g: return None
        ds = [o for o in g if distinct(r, o) and not B.overlap(o["meaning"], r["meaning"])]
        if not ds: return None
        if i % 2 == 0:
            q = f"True or false: according to the slides, {r['part']} means \"{r['meaning']}\"."
            return add(r["lec"], "tf", "P14", "medium", "discriminate", q, True, ["true"], [B.rev(r)], [r["part"]],
                       "صح. " + expl(r), "P14tf:0")
        d = ds[i % len(ds)]
        q = f"True or false: according to the slides, {r['part']} means \"{d['meaning']}\"."
        corr = f"{r['part']} = {r['meaning']}; \"{d['meaning']}\" is {d['part']}."
        return add(r["lec"], "tf", "P14", "medium", "discriminate", q, False, ["false"], [B.rev(r), B.rev(d)], [r["part"]],
                   f"غلط: {r['part']} = {r['meaning']}، و \"{d['meaning']}\" دي {d['part']} ({ref(d['lec'], d['page'])}). " + expl(r),
                   "P14tf:1", correction=corr)

    def P3(r, i, k=0):  # hard: slide definition -> slide term, no hint
        if k >= min(len(r["ex"]), len(r["defs"])): return None
        w = r["ex"][k]
        d = r["defs"][k]
        if not re.fullmatch(r"[A-Za-z]+", w) or not d or w.lower() in ("diarrhea", "rupture"): return None
        typo = w.lower() in B.TYPO_WORDS
        stem_d = re.sub(r"^(ferric|ferrous):\s*", "", d, flags=re.I)
        # drop slide parentheticals that name a word part of the answer, e.g. "(cyst/o)", "(lysis)", "(gravid)"
        stem_d = re.sub(r"\s*\(([^)]*)\)", lambda m: "" if ("/" in m[1] or core(m[1])[:4] in w.lower()) else m[0], stem_d).strip()
        flat = norm(stem_d).replace(" ", "").replace("/", "")
        c = core(r["part"])
        if (len(c) >= 3 and c[:4] in flat) or w.lower()[:4] in flat: return None
        words = sorted(B.DEF_WORDS.get(B.gnorm(d), {w.lower()}))
        acc = []
        for x in words:
            acc += [y for y in B.accept_word(x) if y not in acc]
        acc += [y for y in ALIAS.get(w.lower(), []) if y not in acc]
        # the same word built with a slide synonym suffix (-algia = -dynia, -rhage = -rhagia): accepted, flagged as not slide wording
        ans = []
        used = best_form(r, w)
        cu = core(used)
        if r["kind"] == "suffix" and w.lower().endswith(cu):
            stem = w.lower()[: -len(cu)]
            pair = {"algia": ["-dynia"], "dynia": ["-algia"]}    # the two "Pain" suffixes on L4 s13
            same_row = [f for f in r["forms"] if core(f) != cu and cu not in core(f) and core(f) not in cu]   # -rhage/-rhagia, not -ian/-ician
            for f in same_row + pair.get(cu, []):
                cf = core(f)
                if cf.startswith("dys"): continue   # -Dysnia is not used to build terms
                s2 = stem
                if f in pair.get(cu, []):           # a different suffix: apply the combining-vowel rules 1 and 2
                    s2 = stem[:-1] if cf[0] in "aeiou" and stem.endswith("o") else stem
                    if cf[0] not in "aeiou" and s2[-1] not in "aeiou": s2 += "o"
                v = s2 + cf
                if v != w.lower() and v not in acc and not B.grounded_word(v): ans.append(v)
        if r["sid"] == "spec":
            pat, t, tid = "P7", *tpl("P7", ["Write the name of the specialty / specialist that suits this scope: {d}.", "Scope of practice: \"{d}\". Write the slide term: ……"], i)
        elif r["sid"] in ("diag", "surg") and re.match(r"(instrument|endoscope|device)", d, re.I):
            pat, t, tid = "P6", *tpl("P6i", ["…… is an {d0}.", "Write the slide term: {d} = ……"], i)
        else:
            pat = "P13" if B.is_trap(w.lower()) and not typo else "P3"
            t, tid = tpl(pat, ["Write the term: …… is {d0}.", "…… = \"{d}\". Write the slide term.", "Write the slide term for: \"{d}\" ……"], i)
        q = t.format(d=stem_d, d0=stem_d[0].lower() + stem_d[1:])
        return add(r["lec"], "typed", pat, "hard", "spell" if pat == "P13" else "reverse", q, w.lower(), acc, [B.rev(r)], [r["part"], w],
                   f"الكلمة زي السلايد: {Ex(w)} — {r['part']} = {r['meaning']} ({ref(r['lec'], r['page'])}).", tid, term=w, acceptNotSlide=ans)

    # ------------------------------------------------------------------ look-alike contrasts (P8)
    def P8(a, b, level, i):
        if level == "hard":
            q = f"{disp(a['part'])} means \"{a['meaning']}\", while {disp(b['part'])} means ……"
            return add(b["lec"], "typed", "P8", "hard", "discriminate", q, b["meaning"], b["comps"], [B.rev(b), B.rev(a)], [b["part"]],
                       f"{b['part']} = {b['meaning']}، أما {a['part']} = {a['meaning']} ({ref(a['lec'], a['page'])}). " + expl(b), "P8:1",
                       errorMap=emap(b, [a]))
        q = f"{disp(a['part'])} means …… , while {disp(b['part'])} means …… ."
        blanks = [{"answer": a["meaning"], "accept": a["comps"], "errorMap": emap(a, [b])},
                  {"answer": b["meaning"], "accept": b["comps"], "errorMap": emap(b, [a])}]
        return add(a["lec"], "typed2", "P8", "max", "discriminate", q, f"{a['meaning']} / {b['meaning']}", [], [B.rev(a), B.rev(b)],
                   [a["part"], b["part"]], f"{a['part']} = {a['meaning']} ({ref(a['lec'], a['page'])})؛ {b['part']} = {b['meaning']} ({ref(b['lec'], b['page'])}).",
                   "P8:2", blanks=blanks)

    # ------------------------------------------------------------------ analysis-based patterns
    AN = [a for a in B.analysis if a["term"].lower() not in B.TYPO_WORDS and a["term"] != "Diarrhea" and a["term"] not in EXCLUDE_TERMS]
    LABEL = {"amnior": "amnio"}   # Amniorrhexis: the slide label reads "amnio = amniotic sac"

    def ptext(p):
        x = re.sub(r"[()]", "", p["text"])
        return LABEL.get(x, x)

    def split_ok(v, a):
        """drop split variants that move the r of a slide suffix written -rrh… (Herniorrhaphy: only herni/o/rrhaphy)."""
        rr = [p["text"] for p in a["parts"] if p["text"].startswith("rrh")]
        segs = v.split(" / ")
        return all(any(s == x for s in segs) for x in rr) and all(len(s) >= 2 or s in ("o", "i") for s in segs)

    WORKED = [w for w in B.analysis if w["workedOnSlide"]]

    def part_ev(a):
        """evidence for every graded part: its slide table row, else a worked slide example that gives the same part meaning."""
        out = []
        for p in tested_parts(a):
            if not graded(p): continue
            r = part_row(p)
            if r:
                e = [B.rev(r)]
            else:
                w = next((w for w in WORKED if w is not a and any(core(x["text"]) == core(p["text"]) and x["meaning"] and norm(x["meaning"]) == norm(gmean(p)) for x in w["parts"])), None)
                e = B.an_quote(w) if w else []
            out += [x for x in e if x not in out]
        return out
    TYPE_NAME = {"prefix": "Prefix", "root": "Root", "suffix": "Suffix"}

    def tested_parts(a):
        return [p for p in a["parts"] if p["type"] != "vowel"]

    def gmean(p):
        """the slide wording of a part's meaning: the analysis text if it is slide text, else its table row's meaning."""
        if not p["meaning"] or p["from"] not in ("slide", "table"): return None
        if B.grounded(p["meaning"]): return p["meaning"]
        r = part_row(p)
        if r and B.overlap(r["meaning"], p["meaning"]): return r["meaning"]
        return None

    def graded(p):
        return bool(gmean(p))

    def part_row(p):
        t = p["text"].replace("(", "").replace(")", "").lower()
        for r in ROWS:
            for f in r["forms"]:
                fc = core(f)
                ct = core(t)
                if fc and (fc == ct or fc.rstrip("o") == ct or ct.rstrip("o") == fc.rstrip("io") or (ct.startswith("rrh") and ct[1:] == fc)):
                    if r["kind"] == p["type"] or (r["kind"] == "prefix" and p["type"] == "prefix"):
                        return r
        return None

    def part_variants(a, p):
        t = p["text"].replace("(", "").replace(")", "").lower()
        base = re.sub(r"\(.*?\)", "", p["text"]).lower()
        out = [t, base]
        if p["type"] == "prefix": out += [t + "-", base + "-"]
        if p["type"] == "suffix": out += ["-" + t, "-" + base]
        r = part_row(p)
        if r:
            for f in r["forms"]:
                out += [f.lower(), f.lower().strip("-"), f.lower().replace("/", "")]
        for sp in B.seg_variants(a["parts"]) + B.SPLIT_EXTRA.get(a["term"], []):
            for seg in sp.split(" / "):
                if seg and len(seg) >= 2 and (seg.startswith(base[:3]) or base.startswith(seg[:3])) and abs(len(seg) - len(base)) <= 2:
                    out.append(seg)
        if base.startswith("rh"): out += ["r" + base, "-r" + base]
        if base in LABEL: out.append(LABEL[base])
        return list(dict.fromkeys(x for x in out if x and len(x.strip("-")) >= 2))

    def an_ok(a):
        real = tested_parts(a)
        return B.split_shown(a) or all(p["from"] in ("slide", "table", "extra") for p in real)

    def P1(a, i):
        if not an_ok(a): return None
        real = tested_parts(a)
        g = [p for p in real if graded(p)]
        if len(g) < 2: return None
        evd = B.an_quote(a)
        if not evd: return None
        fields = []
        if not any(p["type"] == "prefix" for p in real):
            fields.append({"name": "Prefix", "answer": "—", "accept": ["", "-", "—", "none", "no prefix", "x", "0"]})
        for p in real:
            m = gmean(p)
            pr = part_row(p) if m else None
            am = list(dict.fromkeys((comps(m) if m else []) + (pr["comps"] if pr and B.overlap(pr["meaning"], m) else [])))
            fields.append({"name": TYPE_NAME[p["type"]], "part": ptext(p), "answer": f"{ptext(p)} = {m}" if m else f"{ptext(p)} (meaning not on the slides — part only)",
                           "accept_part": part_variants(a, p), "accept_meaning": am, "meaningGraded": bool(m)})
        if not any(p["type"] == "suffix" for p in real):
            fields.append({"name": "Suffix", "answer": "—", "accept": ["", "-", "—", "none", "no suffix", "x", "0"]})
        med = [a["medical"]] + ([x for x in [a.get("def")] if x] if a.get("def") else [])
        fields.append({"name": "Medical meaning", "answer": a["medical"], "accept": med,
                       "keywords": [w for w in re.findall(r"[a-z]+", a["medical"].lower()) if len(w) > 3 and w not in ("with", "that", "used", "from")]})
        level = "max" if len(g) >= 3 or (len(real) >= 3 and len(a["term"]) >= 12) else "hard"
        t, tid = tpl("P1", ["Illustrate by word structural analysis: {t}", "Using the rules for forming medical terms, analyse {t} (prefix / root / suffix + meanings + medical meaning)."], i)
        plain = " / ".join(re.sub(r"\(.*?\)", "", p["text"]) for p in a["parts"] if p["type"] != "vowel")
        acc = [plain] if "(" in "".join(p["text"] for p in a["parts"]) else []
        acc += [v for v in B.seg_variants(a["parts"]) + [x for x in B.SPLIT_EXTRA.get(a["term"], []) if x not in B.seg_variants(a["parts"])] if split_ok(v, a)]
        evd = evd + [e for e in part_ev(a) if e not in evd]
        bits = " + ".join(f"{p['text']} ({gmean(p)})" if graded(p) else p["text"] for p in real)
        return add(a["lec"], "analyze", "P1", level, "analyze", t.format(t=a["term"]), " · ".join(f["answer"] for f in fields), acc, evd,
                   [p["text"] for p in real], f"التحليل زي السلايد: {a['term']} = {bits} → {a['medical']}", tid, fields=fields, term=a["term"])

    def P11(a, i, mistakes):
        real = tested_parts(a)
        g = [p for p in real if graded(p)]
        if len(g) < 2 or not an_ok(a): return None
        evd = B.an_quote(a)
        if not evd: return None
        lines, swap, key, acc, ems = [], None, "No mistake", list(NO_MISTAKE), {}
        target = None
        def visible(p):
            return any(len(c) >= 4 and re.search(r"(?<![a-z])" + re.escape(c.lower()), a["medical"].lower()) for c in comps(gmean(p)))
        if mistakes:
            order = g[::-1] if i % 2 else g
            for p in sorted(order, key=visible):
                r = part_row(p)
                if not r: continue
                partners = [o for o in (look_of(r) or []) if distinct(r, o) and not B.overlap(o["meaning"], gmean(p)) and o["kind"] == r["kind"]]
                if not partners:
                    partners = [o for o in ROWS if o["sid"] == r["sid"] and distinct(r, o) and not B.overlap(o["meaning"], gmean(p))]
                if partners:
                    target, swap = p, partners[i % len(partners)]
                    break
            if not target: return None
        for p in real:
            m = gmean(p)
            shown = swap["meaning"] if p is target else m
            lines.append(f"{TYPE_NAME[p['type']]}: {ptext(p)}" + (f" = {shown}" if shown else ""))
        if not (target and visible(target)):
            lines.append(f"Medical meaning: {a['medical']}")
        q = (f"A student analysed {a['term']} as:  " + " | ".join(lines) +
             ".  The analysis may contain 0, 1 or 2 mistakes. Write each correction, or write \"no mistake\".")
        if target:
            tp = ptext(target)
            tm = gmean(target)
            key = f"{tp} = {tm}"
            tr = part_row(target)
            cs = list(dict.fromkeys(comps(tm) + (tr["comps"] if tr else [])))
            acc = [key] + cs + [f"{tp} = {c}" for c in cs] + [f"-{tp} = {c}" for c in cs]
            ar = (f"الغلطة: الطالب حط معنى {swap['part']} ({swap['meaning']}, {ref(swap['lec'], swap['page'])}) لـ {tp}. "
                  f"الصح: {tp} = {tm}. الباقي صح. → {a['medical']}")
            ems = {norm(x): "فيه غلطة واحدة: " + ar for x in NO_MISTAKE}
            ems[norm(swap["meaning"])] = "دا معنى " + swap["part"] + " — هو نفسه الغلط اللي في التحليل. " + ar
        else:
            ar = "التحليل كله صح: " + " + ".join(f"{p['text']} = {gmean(p)}" for p in g) + f" → {a['medical']}"
        evd = evd + [e for e in part_ev(a) if e not in evd] + ([B.rev(swap)] if swap and B.rev(swap) not in evd else [])
        return add(a["lec"], "typed", "P11", "max", "error-find", q, key, acc, evd, [p["text"] for p in real], ar,
                   "P11:0", mistakes=1 if target else 0, swap=(f"{swap['part']} ↔ {target['text']}" if target else ""), errorMap=ems, term=a["term"])

    def P9(a, i):
        """transfer: a part learned in another slide term (row example), asked inside this analysis term."""
        if not an_ok(a): return []
        out = []
        real = tested_parts(a)
        cands = []
        for p in real:
            if not graded(p) or sum(x["type"] == p["type"] for x in real) != 1: continue
            if p["from"] == "slide": continue   # meaning printed beside this very term: recall, not transfer
            r = part_row(p)
            if not r or a["term"].lower() in [e.lower() for e in r["ex"]]: continue
            if B.overlap(r["meaning"], p["meaning"]) is False and norm(r["meaning"]) != norm(p["meaning"]): continue
            cands.append((p, r))
        if not cands: return []
        evd = B.an_quote(a)
        if not evd: return []
        p, r = cands[i % len(cands)]
        cross = r["lec"] != a["lec"]
        q = f"Lecture {a['lec']} lists the term {a['term']}. According to the slides, its {p['type']}" + (" (as split on the slide)" if B.split_shown(a) and a["slide"] != "24" else "") + " means ……"
        out.append(add(a["lec"], "typed", "P9", "max" if cross and len(cands) == 1 and False else "hard", "transfer", q, r["meaning"], r["comps"],
                       evd + [B.rev(r)], [p["text"]], f"{r['part']} اتعلمناها في {Ex(r['ex1'])} ({ref(r['lec'], r['page'])}) = {r['meaning']} — ونفس الجزء في {a['term']}.",
                       "P9:1", cross=cross, errorMap=emap(r), term=a["term"]))
        if len(cands) >= 2:
            (p1, r1), (p2, r2) = cands[0], cands[1]
            if not B.overlap(r1["meaning"], r2["meaning"]):
                q = f"Lecture {a['lec']} lists the term {a['term']}. Write the slide meaning of its {p1['type']} …… and of its {p2['type']} …… ."
                blanks = [{"answer": r1["meaning"], "accept": r1["comps"], "errorMap": emap(r1)}, {"answer": r2["meaning"], "accept": r2["comps"], "errorMap": emap(r2)}]
                out.append(add(a["lec"], "typed2", "P9", "max", "transfer", q, f"{r1['meaning']} / {r2['meaning']}", [], evd + [B.rev(r1), B.rev(r2)],
                               [p1["text"], p2["text"]], f"{r1['part']} = {r1['meaning']} ({ref(r1['lec'], r1['page'])})؛ {r2['part']} = {r2['meaning']} ({ref(r2['lec'], r2['page'])}) → {a['term']}.",
                               "P9:2", blanks=blanks, cross=r1["lec"] != a["lec"] or r2["lec"] != a["lec"], term=a["term"]))
        return out

    # ------------------------------------------------------------------ odd one out (P12): ≥ 2 slide tables
    def P12(members, odd, i):
        items = [m["part"] for m in members] + [odd["part"]]
        rng.shuffle(items)
        shared = members[0]["meaning"]
        q = f"Odd one out: {', '.join(items)}. Three share one slide meaning. Write the odd {odd['kind']} …… and its slide meaning …… ."
        blanks = [{"answer": odd["part"], "accept": forms_exact(odd, only_self=True)}, {"answer": odd["meaning"], "accept": odd["comps"], "errorMap": emap(odd)}]
        return add(odd["lec"], "typed2", "P12", "max", "discriminate", q, f"{odd['part']} / {odd['meaning']}", [], [B.rev(odd)] + [B.rev(m) for m in members[:2]],
                   items, f"{odd['part']} = {odd['meaning']} ({ref(odd['lec'], odd['page'])})؛ الباقي ({', '.join(m['part'] for m in members)}) = {shared}.",
                   "P12:0", blanks=blanks, items=items, tables=sorted({m["sid"] for m in members} | {odd["sid"]}))

    # ------------------------------------------------------------------ rules / plurals (P10)
    def P10_plural(p, i):
        reg = p["singular"] in B.REGULAR
        q = f"According to the slides (Singular and Plural Forms), the plural of {p['singular']} ({p['meaning']}) is ……"
        return add(2, "typed", "P10", "medium" if reg else "hard", "apply-rule", q, p["plural"], [p["plural"]], B.pl_ev(p), ["pl:" + p["singular"]],
                   f"الجمع حسب السلايد: {p['ending']} → {p['pluralEnding']}، {p['singular']} → {p['plural']}", "P10:pl",
                   exception=not reg, errorMap={norm(w): f"{w} مش الجمع اللي في السلايد — القاعدة {p['ending']} → {p['pluralEnding']}." for w in B.PL_WRONG[p["singular"]] if not B.grounded_word(w)})

    def P10_rule(term, parts, rid, i):
        ds = [k for k in B.RULE_TEXT if k != rid]
        rng.shuffle(ds)
        exc = rid in ("3", "4", "4b")
        evr = B.rule_evidence(term, rid) + [B.ev(2, B.RULE_PAGE[k], B.RULE_QUOTE[k]) for k in ds[:3]]
        focus = {"3": f"Which rule explains why {term} has only one i ({' + '.join(parts)})?",
                 "4": f"Which rule explains why the final a of {parts[0]} is dropped in {term}?",
                 "4b": f"Which rule explains why a combining vowel o is kept between {parts[0]} and {parts[1]} in {term}, even though {parts[1]} begins with a vowel?"}
        stemr = focus.get(rid, f"Which combining-vowel rule explains {' + '.join(parts)} → {term}?")
        out = [add(B.term_lec(term), "mcq", "P10", "medium", "apply-rule", stemr,
                   B.RULE_TEXT[rid], [B.RULE_TEXT[rid]], evr, [term] + parts, f"{term}: القاعدة {rid} — {B.RULE_TEXT[rid]}",
                   "P10:rule", options=mcq_opts(B.RULE_TEXT[rid], [B.RULE_TEXT[k] for k in ds[:3]]), exception=exc)]
        w = B.wrong_joins(term, parts, rid)
        out.append(add(B.term_lec(term), "typed", "P10", "hard", "apply-rule", f"Join the parts using the slide combining-vowel rules: {' + '.join(parts)} = ……",
                       term.lower(), [term.lower()], B.rule_evidence(term, rid), [term] + parts, f"{term.lower()} — القاعدة {rid}: {B.RULE_TEXT[rid]}",
                       "P10:join", exception=exc, errorMap={norm(x): f"{x} — راجع القاعدة {rid}: {B.RULE_TEXT[rid]}" for x in w}))
        return out

    # ------------------------------------------------------------------ concept / pronunciation (slide statements)
    def CQ(c, i):
        evd = [B.ev(c["lec"], c["p"], c["quote"])]
        c = dict(c, level="hard" if c["level"] == "max" else c["level"])
        if c["type"] == "tf":
            return add(c["lec"], "tf", "P14", c["level"], c["skill"], c["q"], c["a"], [str(c["a"]).lower()], evd, c["tests"], c["ar"], "CQ:tf",
                       correction=c.get("fix"))
        o = c["o"]
        if "colour-code slide as a" in c["q"]:
            o = [x.strip("-") for x in o]
        return add(c["lec"], "mcq", "P14", c["level"], c["skill"], c["q"], o[0], [o[0]], evd, c["tests"], c["ar"], "CQ:mcq",
                   options=mcq_opts(o[0], o[1:]))

    # =========================================================== generate (deterministic)
    for c_i, c in enumerate(D.CONCEPT_Q):
        CQ(c, c_i)
    for i, r in enumerate(ROWS):
        if r["sid"] == "numchart":
            if i % 2 == 0: P2e(r, i)
            else: P2m(r, i) or P2e(r, i)
            continue
        # easy
        if i % 3 == 1:
            P14e(r, i) or P2e(r, i)
        else:
            P2e(r, i)
        # medium (one or two per row)
        made = P4(r, i) or P2m(r, i)
        if not made or i % 2:
            (P6(r, i) or (i % 3 == 0 and P14m(r, i)))
        if i % 3 == 2:
            P14tf(r, i)
        if r["sid"] == "easy":
            continue
        # hard
        P3(r, i)
        if len(r["ex"]) > 1 and len(r["defs"]) > 1:
            P3(r, i + 1, 1)
    # contrasts from the slide look-alike tables
    k = 0
    for g in LOOK:
        pairs = [(a, b) for a in g for b in g if a is not b and distinct(a, b) and not B.overlap(a["meaning"], b["meaning"])]
        for j, (a, b) in enumerate(pairs):
            if j % 2 == 0 and j < 6:
                P8(a, b, "hard", k); k += 1
            if j % 3 == 1 and j < 7:
                P8(a, b, "max", k); k += 1
    # analyses
    for i, a in enumerate(AN):
        P1(a, i)
        P9(a, i)
        P11(a, i, mistakes=(i % 3 != 0))
    # odd one out: 3 rows sharing a slide meaning + 1 look-alike from ANOTHER table
    groups = {}
    for r in ROWS:
        if r["sid"] in ("numchart", "easy"): continue
        groups.setdefault((r["kind"], norm(r["meaning"])), []).append(r)
    j = 0
    for (kind, m), mem in groups.items():
        if len(mem) < 3: continue
        mem_sids = {x["sid"] for x in mem}
        odds = [o for o in ROWS if o["kind"] == kind and o["sid"] not in mem_sids and o["sid"] not in ("numchart", "easy")
                and not B.overlap(o["meaning"], m) and not any(B.near(o["part"], x["part"]) for x in mem)]
        odds.sort(key=lambda o: (o["lec"] != mem[0]["lec"], o["part"]))
        for t in range(min(2, len(odds))):
            mm = mem[:]
            rng.shuffle(mm)
            P12(mm[:3], odds[(t * 3 + j) % len(odds)], j); j += 1
    for p in B.plurals:
        P10_plural(p, 0)
    for t, ps, rid in B.RULE_EX:
        if t != "Bronchiole":
            P10_rule(t, ps, rid, 0)

    # ------------------------------------------------------------------ de-duplicate, score, leak tokens, ids
    seen, uniq = set(), []
    for q in Q:
        k2 = (q["kind"], norm(q["q"]))
        if k2 in seen: continue
        seen.add(k2); uniq.append(q)
    Q = uniq

    IRREG = B.IRREG
    def score(q):
        pts = 0
        if q["kind"] in TYPED_KINDS: pts += 6
        if q["skill"] in ("reverse", "spell") or q["pattern"] in ("P3", "P6", "P7", "P13"): pts += 4
        n = len(q.get("fields", [])) if q["kind"] == "analyze" else len(q.get("blanks", [])) or 1
        pts += 3 * max(0, n - 1)
        if q["kind"] == "analyze": pts += 4   # split + part meanings + medical meaning: always above a one-term item of its level (4d re-run)
        if not q.get("hint"): pts += 3
        if q.get("close") or q["pattern"] == "P8": pts += 4
        a = q["key"] if isinstance(q["key"], str) else ""
        if q["kind"] == "typed":
            w = re.sub(r"[^a-z]", "", a.lower())
            pts += min(4, len(w) // 5 + (1 if w and IRREG.search(w) else 0))
        if q.get("exception"): pts += 3
        if q["pattern"] == "P9" and q["kind"] == "typed2": pts += 4 + (2 if q.get("cross") else 0)
        if q["pattern"] == "P9" and q["kind"] == "typed": pts = min(pts, 6)   # one-part transfer = entry point of the hard band (4d ramp check)
        if q["pattern"] in ("P11", "P12"): pts += 5
        return FLOOR[q["difficulty"]] + min(24, pts)

    def leak(q):
        toks = set()
        if q["kind"] == "tf": return []
        keys = [q["key"]] if isinstance(q["key"], str) else []
        keys += [b["answer"] for b in q.get("blanks", [])]
        for k3 in keys:
            k3 = norm(k3)
            if len(k3.strip("-")) >= 4 and k3 not in ("no mistake", "condition of", "pertaining to", "small", "true", "false"):
                toks.add(k3.strip("-"))
        for t in q["tests"]:
            c3 = core(t)
            if len(c3) >= 3: toks.add(c3)
        if q.get("term"): toks.add(norm(q["term"]))
        return sorted(toks)

    for q in Q:
        q["score"] = score(q)
        q["tie"] = rng.randrange(10 ** 6)
        q["leak"] = leak(q)
        q.setdefault("errorMap", {})
        q.pop("close", None)
    Q.sort(key=lambda q: (q["lec"], LEVELS.index(q["difficulty"]), q["score"], q["tie"]))
    for i, q in enumerate(Q, 1):
        q["id"] = f"q{i:03d}"
    B.BANK_TPL = TPL
    return Q
