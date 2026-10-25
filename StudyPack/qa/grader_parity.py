"""Grading-drift guard, step 1: pick sample answers across every question kind / E-code, grade them with
tools/quizlib.py and write qa/parity_samples.json. Step 2 (node qa/grader_parity.js) grades the same answers with the
JS port inside site/src/app.html and fails on any difference.
Run from StudyPack:  python -I -X utf8 qa/grader_parity.py && node qa/grader_parity.js
"""
import json, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
from quizlib import Bank  # noqa: E402

C = json.load(open(os.path.join(HERE, "..", "content", "content.json"), encoding="utf-8"))
B = Bank(C)
rng = random.Random(7)
S = []  # (qid, response, why)


def pick(pred, k):
    c = [q for q in B.Q if pred(q)]
    rng.shuffle(c)
    return c[:k]


# typed (spelling / meaning)
for q in pick(lambda q: q["kind"] == "typed" and q["pattern"] != "P11" and len(q["key"]) >= 8 and q["key"].isalpha(), 4):
    k = q["key"]
    S.append((q["id"], k.upper(), "correct, case"))
    i = k.find("o", 2)
    if i > 0: S.append((q["id"], k[:i] + k[i + 1:], "o dropped"))
    S.append((q["id"], k[:3] + "o" + k[3:], "o added"))
    S.append((q["id"], k[:-2] + k[-1] + k[-2], "letters swapped"))
for q in pick(lambda q: q["kind"] == "typed" and "rrh" in str(q["key"]), 1):
    S.append((q["id"], q["key"].replace("rrh", "rh"), "rrh slip"))
for q in pick(lambda q: q["kind"] == "typed" and q.get("errorMap") and q["pattern"] != "P11", 3):
    S.append((q["id"], next(iter(q["errorMap"])), "errorMap key"))
for q in pick(lambda q: q["kind"] == "typed" and q["pattern"] != "P11", 3):
    S.append((q["id"], "", "blank"))
    S.append((q["id"], "idk", "idk"))
    S.append((q["id"], "gastr/o", "other slide part"))
    S.append((q["id"], "pain", "other meaning"))
for q in pick(lambda q: q["kind"] == "typed" and q.get("acceptNotSlide"), 1):
    S.append((q["id"], q["acceptNotSlide"][0], "accept-not-slide"))
for q in pick(lambda q: q["kind"] == "typed" and q.get("term") and q["term"].lower() in B.analysis, 3):
    a = B.analysis[q["term"].lower()]
    for p in a["parts"]:
        if p["meaning"]:
            S.append((q["id"], p["meaning"], "meaning of a part of the term")); break
for q in pick(lambda q: q["pattern"] == "P11", 4):
    S.append((q["id"], "no mistake", "P11 no mistake"))
    S.append((q["id"], q["key"], "P11 correct"))
# mcq / tf
for q in pick(lambda q: q["kind"] == "mcq", 3):
    S.append((q["id"], q["key"], "mcq right"))
    S.append((q["id"], next(o for o in q["options"] if o != q["key"]), "mcq wrong"))
for q in pick(lambda q: q["kind"] == "tf", 3):
    S.append((q["id"], True, "tf true"))
    S.append((q["id"], False, "tf false"))
# two blanks: both right / one wrong / blank
for q in pick(lambda q: q["kind"] == "typed2", 3):
    ans = [b["answer"] for b in q["blanks"]]
    S.append((q["id"], ans, "typed2 right"))
    S.append((q["id"], [ans[0], "pain"], "typed2 half"))
    S.append((q["id"], ["", ""], "typed2 blank"))
# full analysis: right / wrong part / wrong meaning / empty
for q in pick(lambda q: q["kind"] == "analyze", 3):
    right = []
    for f in q["fields"]:
        if "accept_part" in f: right.append(f["accept_part"][0] + "=" + (f["accept_meaning"][0] if f["accept_meaning"] else ""))
        else: right.append(f["accept"][0])
    S.append((q["id"], right, "analyze right"))
    wrong = list(right)
    for i, f in enumerate(q["fields"]):
        if "accept_part" in f: wrong[i] = f["accept_part"][0] + "=pain"; break
    S.append((q["id"], wrong, "analyze wrong meaning"))
    wrong2 = list(right)
    for i, f in enumerate(q["fields"]):
        if "accept_part" in f: wrong2[i] = "xyz=" + (f["accept_meaning"][0] if f["accept_meaning"] else ""); break
    S.append((q["id"], wrong2, "analyze wrong part"))
    S.append((q["id"], [""] * len(q["fields"]), "analyze empty"))

QI = {q["id"]: q for q in B.Q}
out = [dict(id=i, resp=r, why=w, py=B.grade(QI[i], r)) for i, r, w in S]
json.dump(out, open(os.path.join(HERE, "parity_samples.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
codes = sorted({str(o["py"]["code"]) for o in out})
print(f"{len(out)} samples written; kinds: {sorted({QI[o['id']]['kind'] for o in out})}; codes: {codes}")
