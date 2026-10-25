"""Self-checks for StudyPack/content/content.json. Exit code 1 on any failure.
Run:  python -I StudyPack/tools/check_content.py      (imports build_content, so it also rebuilds content.json)
Gates R0–R8 (CLAUDE.md, Stage 3b): evidence, grounding of answer + every distractor, slide-typo words, def/extra parts,
synonym clashes, exactly one correct answer, difficulty + score bands, coverage, counts.
"""
import json, os, sys, re, collections
sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_content as B  # same synonym rules + slide corpus the generator uses
import slide_data as D

C = json.load(open(os.path.join(HERE, "..", "content", "content.json"), encoding="utf-8"))
errors, warns = [], []
E = errors.append

SCHEMA = {
    "meta": ["course", "exam", "lectures", "generated"],
    "concepts": ["id", "lec", "slide", "title", "body"],
    "rules": ["id", "lec", "slide", "rule", "example"],
    "pronunciation": ["letters", "sound", "examples", "lec", "slide"],
    "plurals": ["ending", "pluralEnding", "singular", "plural", "meaning", "lec", "slide"],
    "sections": ["id", "lec", "slide", "kind", "title", "rows"],
    "analysis": ["term", "lec", "slide", "parts", "literal", "medical"],
    "lookalikes": ["title", "rows", "tip", "tipIsExtra"],
    "spellingTraps": ["word", "trap", "say", "lec", "slide"],
    "questions": ["id", "lec", "slide", "type", "q", "options", "answer", "explain_ar", "difficulty", "score", "skill", "evidence", "tests"],
}
for k, keys in SCHEMA.items():
    if k not in C:
        E(f"missing top-level key {k}"); continue
    items = [C[k]] if k == "meta" else C[k]
    for i, it in enumerate(items):
        for key in keys:
            if key not in it: E(f"{k}[{i}] missing '{key}'")
        if k not in ("meta", "lookalikes") and (not isinstance(it.get("lec"), int) or not str(it.get("slide", "")).strip()):
            E(f"{k}[{i}] needs lec (int) + slide")

# ---------------- content: sections / analysis ----------------
for s in C["sections"]:
    if s["kind"] not in ("prefix", "root", "suffix"): E(f"section {s['id']} bad kind")
    seen = set()
    for r in s["rows"]:
        for f in [r["part"]] + r["alts"]:
            if f.lower() in seen: E(f"duplicate part '{f}' in section {s['id']}")
            seen.add(f.lower())
        if not r["meaning"]: E(f"{s['id']}/{r['part']} empty meaning")
        # R0: every table cell is slide text
        for cell in re.split(r"\s*\|\s*", r["quote"].split(": ", 1)[-1] if s["id"] in ("cond", "small", "adj") else r["quote"]):
            for piece in re.split(r";\s*", cell):
                if piece and not B.grounded(piece) and s["id"] not in ("numchart", "easy", "anti"):
                    E(f"row quote not slide text: {s['id']}/{r['part']}: '{piece}'")
        if s["id"] != "anti":
            for fld in ("meaning",):
                if not B.grounded(r[fld]): E(f"row {s['id']}/{r['part']} {fld} not slide text: '{r[fld]}'")
for a in C["analysis"]:
    joined = re.sub(r"\(.*?\)", "", "".join(p["text"] for p in a["parts"]))
    if joined.lower() != a["term"].lower(): E(f"analysis {a['term']}: parts spell '{joined}'")
    for p in a["parts"]:
        if p["type"] not in ("prefix", "root", "vowel", "suffix"): E(f"analysis {a['term']} bad type")

# ---------------- questions ----------------
Q = C["questions"]
LEVELS = ["easy", "medium", "hard", "max"]
BAND = {"easy": (1, 25), "medium": (26, 50), "hard": (51, 75), "max": (76, 100)}
SKILLS = {"recall", "reverse", "spell", "analyze", "discriminate", "apply-rule", "error-find"}
FILES = {s["file"]: s for s in D.META["sources"]}
TYPO_SLIDE = {"oligouria", "polioencephalities", "hemi thorax", "diarrrhea", "reputure"}
EXCLUDED_PAGES = {(1, 2), (1, 3), (1, 4), (1, 5), (4, 1), (4, 15), (4, 16), (5, 1)}
# meanings that only come from a definition (def) or nowhere (extra): never a target or a distractor (R3)
SLIDE_M = {p["meaning"].lower() for a in C["analysis"] for p in a["parts"] if p["meaning"] and p["from"] in ("slide", "table")}
SLIDE_M |= {r["meaning"].lower() for s in C["sections"] for r in s["rows"]}
DEF_M = {p["meaning"].lower() for a in C["analysis"] for p in a["parts"] if p["meaning"] and p["from"] not in ("slide", "table")} - SLIDE_M
PART_FORMS = {}
for s in C["sections"]:
    for r in s["rows"]:
        for f in [r["part"]] + r["alts"]:
            PART_FORMS.setdefault(f, r)
BRIT = re.compile(r"aemia|haem|paed|oesoph|oedem|coel|rrhoea|pnoea|amoeb|leuc|aetio|foet|kalaem|natraem|glycaem|lipaem|anaem")


def norm(s):
    return re.sub(r"[\s\-/‐-―.·]", "", str(s).lower())


ids = collections.Counter(q["id"] for q in Q)
for d, n in ids.items():
    if n > 1: E(f"duplicate question id {d}")
for t, n in collections.Counter((q["kind"], q["q"]) for q in Q).items():
    if n > 1: E(f"same question text x{n}: {t[1][:70]}")

SKILLS |= {"isolate", "transfer"}
PATTERNS = {f"P{i}" for i in range(1, 15)}
NEVER_MAX = {"P2", "P3", "P4", "P5", "P6", "P7", "P13", "P14"}
KINDS = {"mcq": "mcq", "tf": "tf", "typed": "spell", "typed2": "analyze", "analyze": "analyze"}
FLOOR = {"easy": 1, "medium": 26, "hard": 51, "max": 76}


def steps(q):
    if q["kind"] == "analyze": return sum(1 for f in q["fields"] if f.get("meaningGraded"))
    if q["kind"] == "typed2": return len(q["blanks"])
    if q["pattern"] in ("P11", "P9"): return 2
    return 1


def ground_ev(qid, e):
    src = FILES.get(e.get("file"))
    if not src: E(f"{qid} evidence file unknown: {e.get('file')}"); return
    if not (isinstance(e.get("page"), int) and 1 <= e["page"] <= src["pages"]): E(f"{qid} evidence page {e.get('page')} outside {src['file']}")
    if (src["lec"], e["page"]) in EXCLUDED_PAGES: E(f"{qid} evidence from an excluded page (R7)")
    quote = re.sub(r"\s*\((colour split on the slide)\)$", "", e.get("quote", ""))
    if "|" in quote and re.search(r"\w\|\w", quote):
        if not B.grounded(quote.replace("|", "")) and not B.grounded(quote): E(f"{qid} colour-split quote not on slide: {quote}")
    elif not B.grounded_pieces(quote):
        bad = [c for c in re.split(r"\s*\|\s*|;\s*", quote.split(": ", 1)[-1]) if c and not B.grounded(c)]
        if bad: E(f"{qid} evidence quote not slide text: {bad[:2]}")


def is_part(x):
    return x in PART_FORMS or x.lower() in {f.lower() for f in PART_FORMS}


slots = collections.Counter()
for q in Q:
    qid, k = q["id"], q.get("kind")
    if k not in KINDS: E(f"{qid} bad kind {k}"); continue
    if q["type"] != KINDS[k]: E(f"{qid} legacy type {q['type']} does not match kind {k}")
    if q["difficulty"] not in LEVELS: E(f"{qid} bad difficulty"); continue
    lo = FLOOR[q["difficulty"]]
    if not (isinstance(q["score"], int) and lo <= q["score"] <= lo + 24): E(f"{qid} score {q['score']} outside {q['difficulty']} band")
    if q["pattern"] not in PATTERNS: E(f"{qid} bad pattern {q['pattern']}")
    if q["skill"] not in SKILLS: E(f"{qid} bad skill {q['skill']}")
    if not q["tests"]: E(f"{qid} has no tested word part")
    # R2 evidence
    if not q["evidence"]: E(f"{qid} no evidence")
    for e in q["evidence"]: ground_ev(qid, e)
    # R8 / R0 / R7
    if not re.search(r"[؀-ۿ]", q["explain_ar"]): E(f"{qid} explain_ar has no Arabic")
    if not re.search(r"L\d", q["explain_ar"]): E(f"{qid} explain_ar cites no slide ref")
    if re.search(r"slip|typo|wrong on the slide|error on the slide|سهو|غلطة السلايد", q["explain_ar"] + (q.get("correction") or "") + q["q"], re.I):
        E(f"{qid} implies the slide is wrong (R0)")
    if re.search(r"idiom", q["q"], re.I): E(f"{qid} medical idioms (R7)")
    # max rules (review 2026-10-24): ≥ 2 steps, never a one-step pattern
    if q["difficulty"] == "max":
        if steps(q) < 2: E(f"{qid} max with < 2 steps")
        if q["pattern"] in NEVER_MAX: E(f"{qid} {q['pattern']} can never be max")
    if q["pattern"] == "P11":
        if "0, 1 or 2 mistakes" not in q["q"] or "exactly" in q["q"].lower(): E(f"{qid} P11 must say 'may contain 0, 1 or 2 mistakes'")
        if q.get("mistakes") and not q.get("swap"): E(f"{qid} P11 mistake is not a named slide look-alike swap")
    if q["pattern"] == "P12" and len(q.get("tables", [])) < 2: E(f"{qid} odd-one-out items from one slide table")
    for a in q.get("acceptNotSlide", []):
        if B.grounded_word(a): E(f"{qid} acceptNotSlide '{a}' is actually slide text")
    stem = q["q"]
    if k == "mcq":
        o = q["options"]
        if len(o) != 4: E(f"{qid} has {len(o)} options")
        if len({x.lower() for x in o}) != len(o): E(f"{qid} duplicate options")
        if o.count(q["key"]) != 1: E(f"{qid} key appears {o.count(q['key'])}x")
        slots[o.index(q["key"]) if q["key"] in o else -1] += 1
        if any(re.search(r"all of the above|none of the above", x, re.I) for x in o): E(f"{qid} all/none option")
        kinds = {is_part(x) for x in o}
        if len(kinds) > 1 and not q["tpl"].startswith("CQ"): E(f"{qid} options of mixed kind {o}")
        L = [len(x) for x in o]
        if q["pattern"] == "P14" and q["tpl"].startswith("P14") and max(L) > 3 * min(L) + 8: E(f"{qid} option length cue {L}")
        for x in o:
            if not B.grounded_pieces(x): E(f"{qid} option not slide text (R1): '{x}'")
            if x != q["key"] and (x.lower() in TYPO_SLIDE or (BRIT.search(x.lower()) and not BRIT.search(str(q["key"]).lower()))):
                E(f"{qid} slide-typo / British form as a wrong option: {x}")
            if x.lower() in DEF_M: E(f"{qid} def/extra meaning used as option (R3): {x}")
        if is_part(q["key"]):
            for x in o:
                if x != q["key"] and x in PART_FORMS and q["key"] in PART_FORMS and B.syn(PART_FORMS[x]["part"], PART_FORMS[q["key"]]["part"]):
                    E(f"{qid} synonym of the key offered as a distractor: {x}")
        elif q["tpl"].startswith("P14e"):
            for i, x in enumerate(o):
                for y in o[i + 1:]:
                    if B.overlap(x, y): E(f"{qid} overlapping meanings: {x} ~ {y}")
    elif k == "tf":
        if not isinstance(q["answer"], bool): E(f"{qid} tf answer not bool")
        if q["answer"] is False and not q.get("correction"): E(f"{qid} false T/F without correction")
        for x in re.findall(r"\"([^\"]+)\"|“([^”]+)”", stem):
            x = x[0] or x[1]
            if not B.grounded(x): E(f"{qid} T/F fact not slide text: {x}")
    elif k == "typed":
        if not isinstance(q["answer"], list) or not q["answer"]: E(f"{qid} typed answer must be a non-empty list")
        ground = q["key"]
        if q["pattern"] == "P11":
            ground = q["key"].split(" = ", 1)[-1] if q.get("mistakes") else None
        if ground and not B.grounded(ground) and not any(B.grounded(a) for a in q["accept"]):
            E(f"{qid} key not slide text: {q['key']}")
        if q["pattern"] == "P13" and str(q["key"]).lower() in B.TYPO_WORDS: E(f"{qid} slide-typo word as a spelling trap (R5)")
        if str(q["key"]).lower() in DEF_M: E(f"{qid} def-only meaning as the key (R3)")
    elif k == "typed2":
        for b in q["blanks"]:
            if not B.grounded(b["answer"]) and not any(B.grounded(a) for a in b["accept"]): E(f"{qid} blank answer not slide text: {b['answer']}")
            if b["answer"].lower() in DEF_M: E(f"{qid} def-only meaning in a blank (R3)")
    elif k == "analyze":
        for f in q["fields"]:
            for m in ([f["accept_meaning"][0]] if f.get("meaningGraded") else []):
                if not B.grounded(m): E(f"{qid} graded field meaning not slide text: {m}")
        for sp in q["accept"]:
            for seg in sp.split(" / "):
                if not B.grounded(seg) and seg not in ("r",): E(f"{qid} split segment not on slides: {seg}")
    # G2: no answer / tested part in the stem at medium+
    if q["difficulty"] != "easy" and k in ("typed", "typed2") and q["pattern"] not in ("P11", "P12"):
        keys = [q["key"]] if k == "typed" else [b["answer"] for b in q["blanks"]]
        for kk in keys:
            if len(str(kk)) > 3 and re.search(r"(?<![a-z])" + re.escape(str(kk).lower()) + r"(?![a-z])", stem.lower()):
                E(f"{qid} answer '{kk}' shown in its own stem (G2)")
        if q["pattern"] in ("P3", "P6", "P7", "P13"):
            for t in q["tests"]:
                c = re.sub(r"[^a-z]", "", t.split(",")[0])
                if len(c) >= 3 and c[:4] in re.sub(r"[^a-z]", "", stem.lower()) and not q["tpl"].startswith("P6:"):
                    E(f"{qid} tested part '{t}' shown in the stem (G2)")

# G1 / G4 / G5 / G6 bank-level
prod = sum(q["kind"] in ("typed", "typed2", "analyze") for q in Q) / len(Q)
if prod < 0.60: E(f"production share {prod:.0%} < 60% (G1)")
for lvl in ("medium", "hard", "max"):
    qs = [q for q in Q if q["difficulty"] == lvl]
    if qs and sum(q["kind"] == "mcq" for q in qs) / len(qs) > 0.30: E(f"MCQ share > 30% at {lvl} (G1)")
tfs = [q for q in Q if q["kind"] == "tf"]
if len(tfs) / len(Q) > 0.10: E(f"T/F share {len(tfs) / len(Q):.0%} > 10% (G5)")
if tfs and not 0.35 <= sum(q["answer"] is True for q in tfs) / len(tfs) <= 0.65: E("T/F true/false not ≈ 50/50 (G5)")
nm = sum(v for s, v in slots.items() if s >= 0)
for s in range(4):
    if nm and not 0.15 <= slots[s] / nm <= 0.35: E(f"MCQ answer slot {s} used {slots[s] / nm:.0%} (G4 wants ≈ 25%)")
tplc = collections.Counter(q["tpl"] for q in Q)
for t, n in tplc.items():
    if n / len(Q) > 0.08: E(f"stem template {t} used by {n / len(Q):.0%} of the bank (G6 ≤ 8%)")

# R5: slide typo + standard spelling both accepted somewhere; slide splits accepted
if not any("oligouria" in q["answer"] and "oliguria" in q["answer"] for q in Q if isinstance(q["answer"], list)):
    E("no typed question accepts both oliguria and oligouria")
if not any(isinstance(q["answer"], list) and "hemor / rhage" in q["answer"] for q in Q):
    E("the slide split hemor / rhage is not accepted anywhere")

# ---------------- coverage ----------------
def tcore(t):
    return re.sub(r"[^a-z]", "", t.split(",")[0].lower())
TESTS = {tcore(t) for q in Q for t in q["tests"]}
for s in C["sections"]:
    if s["id"] == "anti": continue
    for r in s["rows"]:
        if tcore(r["part"]) not in TESTS: E(f"row not covered by any question: {s['id']}/{r['part']}")
for a in C["analysis"]:
    if not any(a["term"].lower() in (q["q"] + json.dumps(q["answer"]) + q.get("term", "")).lower() for q in Q):
        (warns if a["term"].lower() in B.TYPO_WORDS or a["term"] == "Diarrhea" else errors).append(f"analysis term not asked anywhere: {a['term']}")

# ---------------- tables ----------------
cnt = collections.Counter((q["lec"], q["difficulty"]) for q in Q)
typ = collections.Counter((q["lec"], q["kind"] in ("typed", "typed2", "analyze")) for q in Q)
print("\nLecture | easy | medium | hard | max | total | typed")
print("--------|-----:|-------:|-----:|----:|------:|------:")
for l in range(1, 6):
    row = [cnt[(l, d)] for d in LEVELS]
    print(f"L{l}      | {row[0]:4} | {row[1]:6} | {row[2]:4} | {row[3]:3} | {sum(row):5} | {typ[(l, True)]:5}")
tot = [sum(cnt[(l, d)] for l in range(1, 6)) for d in LEVELS]
print(f"Total   | {tot[0]:4} | {tot[1]:6} | {tot[2]:4} | {tot[3]:3} | {len(Q):5} | {sum(typ[(l, True)] for l in range(1, 6)):5}")
short = [f"L{l} {d}: {cnt[(l, d)]}" for l in range(1, 6) for d in LEVELS if cnt[(l, d)] < 8]
print("\nShortfalls (< 8 per lecture × level):", ", ".join(short) or "none")
hist = collections.Counter((q["score"] - 1) // 10 for q in Q)
print("\nScore histogram")
for b in range(10):
    print(f"{b * 10 + 1:3}–{b * 10 + 10:3} | {hist[b]:4} {'#' * (hist[b] // 5)}")
typed_share = prod
share = sum(q["lec"] >= 3 for q in Q) / len(Q)
print(f"\ntyped share {typed_share:.0%} · L3+L4+L5 share {share:.0%} · by type {dict(collections.Counter(q['type'] for q in Q))}")
print("by skill", dict(collections.Counter(q["skill"] for q in Q)))
PAT = sorted({q["pattern"] for q in Q}, key=lambda x: int(x[1:]))
pc = collections.Counter((q["lec"], q["pattern"]) for q in Q)
print("\nLecture × pattern\n     " + " ".join(f"{p:>4}" for p in PAT))
for l in range(1, 6):
    print(f"L{l}   " + " ".join(f"{pc[(l, p)]:4}" for p in PAT))
lp = collections.Counter((q["difficulty"], q["pattern"]) for q in Q)
print("\nLevel × pattern\n       " + " ".join(f"{p:>4}" for p in PAT))
for d in LEVELS:
    print(f"{d:6} " + " ".join(f"{lp[(d, p)]:4}" for p in PAT))
print(f"MCQ answer slots {dict(sorted(slots.items()))} · T/F {len(tfs)} ({len(tfs) / len(Q):.1%}) · top templates {[(t, round(n / len(Q) * 100, 1)) for t, n in tplc.most_common(4)]}")
if typed_share < 0.35: E(f"typed share {typed_share:.0%} < 35%")
if not 0.7 <= share <= 0.9: warns.append(f"L3–L5 share {share:.0%} outside 70–90%")
for w in warns[:20]: print("WARN", w)
if errors:
    for e in errors[:80]: print("FAIL", e)
    if len(errors) > 80: print(f"... {len(errors) - 80} more")
    sys.exit(1)
print("\nALL CHECKS PASSED")
