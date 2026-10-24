"""Self-checks for StudyPack/content/content.json. Exit code 1 on any failure.
Run:  python StudyPack/tools/check_content.py
"""
import json, os, sys, re, collections

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build_content import clash, same_group, overlap  # same synonym rules the generator uses

C = json.load(open(os.path.join(HERE, "..", "content", "content.json"), encoding="utf-8"))
errors, warns = [], []

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
    "questions": ["id", "lec", "slide", "type", "q", "options", "answer", "explain_ar"],
}
ROW = ["part", "alts", "meaning", "example", "definition", "note"]
PART = ["type", "text", "meaning"]
for k, keys in SCHEMA.items():
    if k not in C:
        errors.append(f"missing top-level key {k}"); continue
    items = [C[k]] if k == "meta" else C[k]
    for i, it in enumerate(items):
        for key in keys:
            if key not in it:
                errors.append(f"{k}[{i}] missing '{key}'")
        if k not in ("meta", "lookalikes"):
            if not isinstance(it.get("lec"), int) or not str(it.get("slide", "")).strip():
                errors.append(f"{k}[{i}] needs lec (int) + slide")
for l in C["meta"]["lectures"]:
    for key in ("n", "title", "doctor", "file", "pages"):
        if key not in l: errors.append(f"meta.lectures missing {key}")

# sections
for s in C["sections"]:
    if s["kind"] not in ("prefix", "root", "suffix"): errors.append(f"section {s['id']} bad kind")
    seen = set()
    for r in s["rows"]:
        for key in ROW:
            if key not in r: errors.append(f"section {s['id']} row {r.get('part')} missing {key}")
        if not isinstance(r.get("alts"), list): errors.append(f"{s['id']}/{r['part']} alts not a list")
        forms = [r["part"]] + r["alts"]
        for f in forms:
            if f.lower() in seen: errors.append(f"duplicate part '{f}' in section {s['id']}")
            seen.add(f.lower())
        if not r["meaning"]: errors.append(f"{s['id']}/{r['part']} empty meaning")

# analysis
for a in C["analysis"]:
    for p in a["parts"]:
        for key in PART:
            if key not in p: errors.append(f"analysis {a['term']} part missing {key}")
        if p["type"] not in ("prefix", "root", "vowel", "suffix"): errors.append(f"analysis {a['term']} bad type")
    joined = re.sub(r"\(.*?\)", "", "".join(p["text"] for p in a["parts"]))
    if joined.lower() != a["term"].lower():
        errors.append(f"analysis {a['term']}: parts spell '{joined}'")

# questions
MEANING_OF = {}  # (kind, part-or-alt) -> meaning, for "Which X means …?" option checks
for s_ in C["sections"]:
    for r in s_["rows"]:
        for f in [r["part"]] + r["alts"]:
            MEANING_OF.setdefault((s_["kind"], f.lower()), r["meaning"])
TYPES = ("mcq", "tf", "spell", "build", "analyze")
ids = collections.Counter(q["id"] for q in C["questions"])
for d, n in ids.items():
    if n > 1: errors.append(f"duplicate question id {d}")
qtexts = collections.Counter(q["q"] for q in C["questions"])
for t, n in qtexts.items():
    if n > 1: warns.append(f"same question text x{n}: {t[:70]}")
for q in C["questions"]:
    if q["type"] not in TYPES: errors.append(f"{q['id']} bad type")
    if q["type"] == "mcq":
        o = q["options"]
        if q["answer"] not in o: errors.append(f"{q['id']} answer not in options")
        if len(o) != 4: errors.append(f"{q['id']} has {len(o)} options")
        if len({x.lower() for x in o}) != len(o): errors.append(f"{q['id']} duplicate options")
        if o.count(q["answer"]) != 1: errors.append(f"{q['id']} answer appears {o.count(q['answer'])}x")
        # synonym check for generated part/meaning questions
        if q["q"].startswith("Which ") and " means “" in q["q"]:
            for x in o:
                if x != q["answer"] and same_group(x, q["answer"]): errors.append(f"{q['id']} synonym option {x} ~ {q['answer']}")
        # no two options may share a meaning word (else two answers look correct)
        m = re.match(r"The (prefix|root|suffix) “.+” means:$", q["q"])
        if m:
            for i, x in enumerate(o):
                for y in o[i + 1:]:
                    if overlap(x, y): errors.append(f"{q['id']} overlapping meanings: {x} ~ {y}")
        m = re.match(r"Which (prefix|root|suffix) means “(.+)”\?$", q["q"])
        if m:
            means = [MEANING_OF.get((m[1], x.lower())) for x in o]
            for x, mx in zip(o, means):
                if x != q["answer"] and mx and overlap(mx, m[2]): errors.append(f"{q['id']} option {x} ({mx}) overlaps “{m[2]}”")
            for i in range(len(o)):
                for j in range(i + 1, len(o)):
                    if means[i] and means[j] and overlap(means[i], means[j]):
                        errors.append(f"{q['id']} options {o[i]} ~ {o[j]} share a meaning word")
    if q["type"] == "tf":
        if not isinstance(q["answer"], bool): errors.append(f"{q['id']} tf answer not bool")
        if q["answer"] is False and not q.get("correction"): errors.append(f"{q['id']} false T/F without correction")
    if q["type"] in ("spell", "build", "analyze"):
        if not isinstance(q["answer"], list) or not q["answer"]: errors.append(f"{q['id']} typed answer must be a non-empty list")
    if not q.get("explain_ar"): warns.append(f"{q['id']} no explanation")

# accepted alternatives present
ALT = {"oliguria": "oligouria", "polioencephalitis": "polioencephalities", "hemithorax": "hemi thorax"}
for q in C["questions"]:
    if q["type"] in ("spell", "build"):
        for w, alt in ALT.items():
            if w in q["answer"] and alt not in q["answer"]:
                errors.append(f"{q['id']} accepts {w} but not slide form '{alt}'")

# summary
rows = collections.Counter(); qs = collections.Counter(); typed = collections.Counter()
for s in C["sections"]: rows[s["lec"]] += len(s["rows"])
for q in C["questions"]:
    qs[q["lec"]] += 1
    if q["type"] in ("spell", "build"): typed[q["lec"]] += 1
total_q = sum(qs.values())
print("\nLecture | table rows | questions | typed (spell/build)")
print("--------|-----------:|----------:|-------------------:")
for l in range(1, 6):
    print(f"L{l}      | {rows[l]:10} | {qs[l]:9} | {typed[l]:19}")
print(f"Total   | {sum(rows.values()):10} | {total_q:9} | {sum(typed.values()):19}")
share = (qs[3] + qs[4] + qs[5]) / total_q
print(f"\nL3+L4+L5 share of questions: {share:.0%}")
print("by type:", dict(collections.Counter(q['type'] for q in C['questions'])))
print(f"sections={len(C['sections'])} analysis={len(C['analysis'])} concepts={len(C['concepts'])} rules={len(C['rules'])} "
      f"plurals={len(C['plurals'])} pronunciation={len(C['pronunciation'])} lookalikes={len(C['lookalikes'])} traps={len(C['spellingTraps'])}")
if total_q < 150: errors.append("fewer than 150 questions")
if sum(typed.values()) < 40: errors.append("fewer than 40 typed questions")
if not 0.7 <= share <= 0.9: warns.append(f"L3–L5 share {share:.0%} outside 70–90%")
for w in warns[:15]: print("WARN", w)
if len(warns) > 15: print(f"... {len(warns) - 15} more warnings")
if errors:
    for e in errors: print("FAIL", e)
    sys.exit(1)
print("\nALL CHECKS PASSED")
