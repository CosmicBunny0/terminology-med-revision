"""Builds StudyPack/content/content.json (Stage 1 schema) from slide_data.py.

Run:  python StudyPack/tools/build_content.py   then   python StudyPack/tools/check_content.py
"slide" = PDF page number(s) inside that lecture's file.
"""
import json, os, re, random, sys, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import slide_data as D

OUT = os.path.join(HERE, "..", "content", "content.json")
KIND = {"p": "prefix", "r": "root", "v": "vowel", "s": "suffix"}
rng = random.Random(25102026)


def pages(src):
    """'L3 p4, p7–9' -> '4, 7–9'"""
    return re.sub(r"L\d p|p", "", src).strip()


def lec_of(src):
    return int(re.match(r"L(\d)", src).group(1))


# ---------------- meta ----------------
M = D.META
meta = {
    "course": M["course"],
    "exam": M["exam"],
    "lectures": [{"n": s["lec"], "title": next(l["title"] for l in M["lectures"] if l["lec"] == s["lec"]),
                  "doctor": s["by"], "file": s["file"], "pages": s["pages"]} for s in M["sources"] if s["lec"]],
    "generated": datetime.date.today().isoformat(),
    "title": M["title"], "credit": M["credit"], "disclaimer": M["disclaimer"], "colors": M["colors"],
    "trainingSheet": next(s for s in M["sources"] if s["lec"] == 0),
    "slideTypos": [{"where": t[0], "slide": t[1], "correct": t[2], "how": t[3]} for t in D.SLIDE_TYPOS],
    "excluded": D.EXCLUDED,
    "homework": {"lec": 2, "slide": "24", "terms": D.HOMEWORK["terms"], "note": D.HOMEWORK["note"]},
}

# ---------------- concepts ----------------
concepts = []
for c in D.CONCEPTS:
    concepts.append({"id": c["id"], "lec": c["lec"], "slide": pages(c["src"].split("·")[0]),
                     "title": c["title"], "body": c["points"], **({"ar": c["ar"]} if c.get("ar") else {}),
                     **({"lowPriority": True} if c.get("low_priority") else {})})
concepts += [
    {"id": "graphtrio", "lec": 2, "slide": "11", "title": "-graph · -gram · -graphy (picture slide)",
     "body": ["Electrocardiograph = the machine (instrument) — -graph",
              "Electrocardiogram = the record — -gram",
              "Electrocardiography = the process of recording — -graphy"],
     "ar": "الماكينة / الورقة / العملية"},
    {"id": "lumen", "lec": 2, "slide": "21", "title": "Lumen (picture slide)",
     "body": ["Lumen = central opening (diagrams: a capillary with red blood cells inside the lumen; a cross-section with the lumen in the centre).",
              "Plural: lumina."]},
    {"id": "diplopia", "lec": 3, "slide": "27", "title": "Diplopia (picture slide)",
     "body": ["Healthy: normal vision (one image). Diplopia: double vision (two images)."]},
    {"id": "bicuspid", "lec": 3, "slide": "28", "title": "Bicuspid (picture slide)",
     "body": ["Normal tricuspid valve vs bicuspid aortic valve."]},
    {"id": "numchart", "lec": 3, "slide": "23", "title": "Number prefixes in medical & pharmaceutical terms",
     "body": ["mono- 1 · di- 2 · tri- 3 · tetra- 4 · penta- 5 · hexa- 6 · hepta- 7 · octa- 8 · nona- 9 · deca- 10",
              "Three examples for each — see the 'numchart' section."]},
    {"id": "anti", "lec": 4, "slide": "8", "title": "Anti- (picture slide)",
     "body": ["Anti-hypertensive drugs (Concor 5 mg)", "Anti-protozoal drugs (Flagyl 500 mg)",
              "Anti-viral drugs (Acyclovir 5%)", "Antibiotics (Augmentin 1 g)"]},
    {"id": "grading", "lec": 1, "slide": "8", "title": "Grading system",
     "body": ["Class activity / periodicals (25 marks): mid-term / quiz = 20 marks · research = 5 marks",
              "Practical exam: (-) marks", "Lecture attendance & behavior: bonus = 2 to 3 marks",
              "Final written exam = 75 marks"]},
]

# ---------------- rules ----------------
rules = []
for r in D.RULES:
    rid = "4b" if r["n"] == 5 else str(r["n"])
    rules.append({"id": rid, "lec": 2, "slide": pages(r["src"]), "rule": r["rule"], "example": r["ex"],
                  **({"ar": r["ar"]} if r.get("ar") else {})})
rules_intro = {"lec": 2, "slide": "9", "body": D.RULES_INTRO["points"]}

pronunciation = []
PRON_PAGE = {"Ch": "18", "C (before a, o, u)": "18", "C (before e, i)": "18", "Dys": "18", "Eu": "18", "Gn": "18"}
for l, snd, ex in D.PRON["rows"]:
    pronunciation.append({"letters": l, "sound": snd, "examples": [e.strip() for e in ex.split(",")],
                          "lec": 2, "slide": PRON_PAGE.get(l, "19")})

plurals = []
for end, pend, sing, mean, plur, wrong in D.PLURALS["rows"]:
    plurals.append({"ending": end, "pluralEnding": pend, "singular": sing, "plural": plur, "meaning": mean,
                    "lec": 2, "slide": "20, 22" if end in ("a", "en", "ex, ix", "is") else "23", "_wrong": wrong})

# ---------------- sections ----------------
sections = []
for s in D.SECTIONS:
    rows = []
    for r in s["rows"]:
        forms = [f.strip() for f in r["part"].split(",")]
        rows.append({"part": forms[0], "alts": forms[1:], "meaning": r["meaning"], "example": r["example"],
                     "definition": r["definition"], "note": r.get("note", "")})
    sec = {"id": s["id"], "lec": s["lec"], "slide": pages(s["src"]), "kind": s["kind"], "title": s["title"], "rows": rows}
    if s.get("subtitle"): sec["subtitle"] = s["subtitle"]
    if s.get("note"): sec["note"] = s["note"]
    sections.append(sec)

# ---------------- analysis ----------------
A = D.A
EXTRA_ANALYSIS = [
    A("Diarrhea", 4, "L4 p14", [["p", "dia", "through", "table"], ["s", "rrhea", "flow, discharge", "table"]],
      "Frequent passage of watery stool", "slide", "Slide split “diarr = through, hea = flow” (word printed “Diarrrhea”) is a slip: the same slide table gives -rrhea = flow, so dia = through + -rrhea = flow."),
    A("Antenatal", 4, "L4 p4", [["p", "ante", "before", "table"], ["r", "nat", "birth", "def"], ["s", "al", "pertaining to", "table"]], "Before birth"),
    A("Postoperative", 4, "L4 p4", [["p", "post", "after, behind", "table"], ["r", "operat", "(surgical) operation", "def"], ["s", "ive", "pertaining to", "table"]], "After a surgical operation"),
    A("Hypertension", 4, "L4 p6", [["p", "hyper", "over, excess, abnormally high, high, increased", "table"], ["r", "tens", "(blood) pressure", "def"], ["s", "ion", None, "extra"]], "High blood pressure"),
    A("Superinfection", 4, "L4 p6", [["p", "super", "above or excess", "table"], ["r", "infect", "infection", "def"], ["s", "ion", None, "extra"]], "Second infection"),
    A("Imbalance", 4, "L4 p7", [["p", "im", "not", "table"], ["r", "balance", "balance", "def"]], "Not being in balance"),
    A("Analgesia", 4, "L4 p7", [["p", "an", "not", "table"], ["r", "alges", "pain", "def"], ["s", "ia", None, "extra"]], "Pain killer"),
    A("Ventricle", 5, "L5 p4", [["r", "ventri", "belly, pouch", "def"], ["s", "cle", "small", "table"]], "Small belly or pouch — a cavity"),
    A("Pustule", 5, "L5 p4", [["r", "pust", "pimple", "def"], ["s", "ule", "small", "table"]], "Small pimple"),
    A("Mucoid", 5, "L5 p8", [["r", "muc", "mucus", "def"], ["s", "oid", "similar to (like, resembling)", "table"]], "Like or resembling mucus"),
    A("Febrile", 5, "L5 p8", [["r", "febr", "fever", "def"], ["s", "ile", "pertaining to", "table"]], "Pertaining to fever"),
]
analysis = []
for a in D.ANALYSIS + EXTRA_ANALYSIS:
    parts = [{"type": KIND[p["t"]], "text": p["x"], "meaning": None if p["src"] == "extra" else (p["m"] or None),
              "from": p["src"]} for p in a["parts"]]
    item = {"term": a["term"], "lec": a["lec"], "slide": pages(a["src"]), "parts": parts,
            "literal": " + ".join(p["meaning"] for p in parts if p["meaning"]),
            "medical": a["def"], "workedOnSlide": a["kind"] == "slide"}
    if "Your turn" in a["src"]:
        item["slide"] = "24"; item["alsoSee"] = a["src"].split("·")[-1].strip()
    if a.get("note"): item["note"] = a["note"]
    analysis.append(item)

# ---------------- look-alikes ----------------
lookalikes = [{"title": c["t"], "lec": lec_of(c["src"]), "slide": c["src"],
               "rows": [{"part": r[0], "meaning": r[1], "example": r[2]} for r in c["rows"]],
               "tip": c["tip"], "tipIsExtra": bool(c.get("tip_extra"))} for c in D.CONFUSE]

# ---------------- spelling traps ("say" is (extra)) ----------------
TRAPS = [  # word, common wrong forms, say, lec, slide
    ("diarrhea", "diarhea · diarrhoea (British spelling — use the slide spelling)", "dye-uh-REE-uh", 4, "14"),
    ("hemorrhage", "hemorage · hemmorhage", "HEM-or-ij", 4, "14"),
    ("amniorrhexis", "amniorexis · amniorhexis", "am-nee-or-REK-sis", 4, "14"),
    ("herniorrhaphy", "herniorraphy · herniorhaphy", "her-nee-OR-uh-fee", 5, "5"),
    ("steatorrhea", "steatorhea · steatorrea", "stee-at-oh-REE-uh", 3, "16"),
    ("pyorrhea", "pyorhea · pyrorrhea", "pye-oh-REE-uh", 3, "20"),
    ("tonsillectomy", "tonsilectomy", "ton-sil-LEK-tuh-mee", 5, "5"),
    ("oliguria", "oligouria (slide spelling — accepted)", "ol-ig-YOO-ree-uh", 4, "6"),
    ("parenteral", "paraenteral · parentral", "par-EN-ter-al", 2, "15"),
    ("carditis", "cardiitis · cardioitis", "kar-DYE-tis", 2, "14"),
    ("cardioesophageal", "cardiesophageal · cardesophageal", "KAR-dee-oh-ee-sof-uh-JEE-al", 2, "16"),
    ("electrocardiogram", "electrcardiogram · electrocardiagram", "ee-LEK-troh-KAR-dee-oh-gram", 2, "10"),
    ("vasectomy", "vasoectomy", "vas-EK-tuh-mee", 2, "13"),
    ("hyperlipoproteinemia", "hyperlipproteinemia", "HY-per-LIP-oh-PRO-teen-EE-mee-uh", 2, "7"),
    ("pediatrics", "pedeatrics · paediatrics (British spelling — use the slide spelling)", "pee-dee-AT-riks", 4, "10"),
    ("psychiatry", "sychiatry · psychiatery", "sy-KY-uh-tree", 4, "10"),
    ("podiatrist", "podiatrest", "poh-DYE-uh-trist", 4, "10"),
    ("polioencephalitis", "polioencephalities (slide typo)", "POH-lee-oh-en-SEF-uh-LYE-tis", 3, "37"),
    ("hemithorax", "hemi thorax (slide writes two words)", "hem-ee-THOR-aks", 3, "29"),
    ("nyctophobia", "nictophobia · nyctofobia", "nik-toh-FOH-bee-uh", 3, "11"),
    ("synchronous", "sinchronous · synchronus", "SIN-kruh-nus", 3, "11"),
    ("euthanasia", "euthenasia · uthanasia", "yoo-thuh-NAY-zhuh", 3, "32"),
    ("pseudocyesis", "psudocyesis · pseudocysis", "SOO-doh-sye-EE-sis", 3, "35"),
    ("xanthoma", "zanthoma · xantoma", "zan-THOH-muh", 3, "37"),
    ("leukoplakia", "leukoplasia · leucoplakia (British spelling — use the slide spelling)", "loo-koh-PLAY-kee-uh", 3, "36"),
    ("erythrocyte", "erythrosyte · erithrocyte", "eh-RITH-roh-site", 3, "36"),
    ("cyanosis", "cyanosys · cianosis", "sye-uh-NOH-sis", 3, "36"),
    ("icterus", "ictirus · ecterus", "IK-ter-us", 3, "37"),
    ("vertebrae", "vertebras · vertebrea", "VER-tuh-bray", 2, "20"),
    ("phalanges", "phalanxes · phalanxs", "fuh-LAN-jeez", 2, "23"),
    ("ganglia", "ganglii · ganglions (English plural — the slide wants Latin ganglia)", "GANG-lee-uh", 2, "23"),
    ("lumina", "lumena · lumens (English plural — the slide wants Latin lumina)", "LOO-min-uh", 2, "20"),
    ("indices", "indicies · indexes (English plural — the slide wants Latin indices)", "IN-dih-seez", 2, "20"),
    ("diagnoses", "diagnosises", "dye-ag-NOH-seez", 2, "20"),
    ("primigravida", "primagravida · primigravidia", "pry-mih-GRAV-ih-duh", 3, "25"),
    ("tachypnea", "tachypnia · tachypnoea (British spelling — use the slide spelling)", "tak-ip-NEE-uh", 4, "5"),
    ("pachyderma", "pachiderma · pakyderma", "pak-ee-DER-muh", 4, "5"),
    ("hyponatremia", "hyponatrimia · hyponatraemia (British spelling — use the slide spelling)", "HY-poh-nuh-TREE-mee-uh", 3, "16"),
    ("hyperkalemia", "hypercalemia · hyperkalaemia (British spelling — use the slide spelling)", "HY-per-kuh-LEE-mee-uh", 3, "15"),
    ("prophylaxis", "profylaxis · prophylaxes", "proh-fuh-LAK-sis", 4, "4"),
    ("xerosis", "zerosis · xerosys", "zih-ROH-sis", 4, "5"),
    ("cephalodynia", "cephalodinia · kephalodynia", "SEF-uh-loh-DIN-ee-uh", 4, "13"),
    ("retinoschisis", "retinoshisis · retinoschysis", "RET-in-OS-kih-sis", 4, "14"),
    ("karyoclasis", "kariyoclasis · karioclasis", "kar-ee-OK-luh-sis", 4, "13"),
    ("amebiasis", "ameobiasis · amoebiasis (British spelling — use the slide spelling)", "am-ee-BYE-uh-sis", 4, "11"),
    ("celiocentesis", "celiocentisis · coeliocentesis (British spelling — use the slide spelling)", "SEE-lee-oh-sen-TEE-sis", 5, "5"),
    ("pleurodesis", "pleurodisis · pleuradesis", "ploo-ROD-uh-sis", 5, "5"),
    ("lithotripsy", "lithotripsey · lithotrypsy", "LITH-oh-trip-see", 5, "6"),
    ("laparoscopy", "laproscopy · laparascopy", "lap-uh-ROS-kuh-pee", 5, "3"),
    ("roentgenography", "rontgenography · roentgenograpy", "RENT-gen-OG-ruh-fee", 5, "3"),
    ("dextrocardia", "dextracardia · dextrocardya", "dek-stroh-KAR-dee-uh", 3, "40"),
    ("sinistrad", "sinestrad · sinistrid", "SIN-is-trad", 3, "40"),
    ("ptosis", "tosis · ptoses", "TOH-sis", 2, "19"),
    ("pneumonia", "neumonia · pnuemonia", "noo-MOH-nee-uh", 2, "19"),
    ("gnathic", "nathic · gnatic", "NATH-ik", 2, "18"),
    ("rheumatic", "reumatic · rhuematic", "roo-MAT-ik", 2, "19"),
]
spellingTraps = [{"word": w, "trap": t, "say": s, "sayIsExtra": True, "lec": l, "slide": p} for w, t, s, l, p in TRAPS]

# accepted alternative spellings for typed answers
ACCEPT = {"oliguria": ["oliguria", "oligouria"], "hemithorax": ["hemithorax", "hemi thorax", "hemi-thorax"],
          "polioencephalitis": ["polioencephalitis", "polioencephalities"],
          "roentgenography": ["roentgenography", "radiography"], "radiography": ["radiography", "roentgenography"]}

# ---------------- questions ----------------
STOP = set("of or and a an the to in for by with from into on its as data".split())
GENERIC = {"abnormally", "condition", "instrument", "surgical", "specialist", "field", "study", "pertaining",
           "like", "resembling", "similar"}


def toks(s):
    return {w for w in re.findall(r"[a-z]+", s.lower()) if w not in STOP}


def clash(m1, m2):
    """True if two meanings are equal or share a meaningful word (synonym risk)."""
    if m1.strip().lower() == m2.strip().lower():
        return True
    return bool((toks(m1) - GENERIC) & (toks(m2) - GENERIC))


# stricter rule for MCQ options (same rule the site used to patch at runtime): any shared content word,
# even "instrument" / "surgical" / "study", makes two options too close to offer side by side
OVERLAP_STOP = {"the", "and", "for", "with", "into", "from", "pertaining", "condition", "abnormal", "abnormally", "state"}


def otoks(s):
    return {w for w in re.findall(r"[a-z]+", s.lower()) if len(w) > 2 and w not in OVERLAP_STOP}


def overlap(m1, m2):
    """True if two MCQ option meanings are equal or share any content word."""
    return m1.strip().lower() == m2.strip().lower() or bool(otoks(m1) & otoks(m2))


# explicit synonym / near-synonym groups — never offered as each other's distractor
SYN_GROUPS = [{"mon/o", "uni", "mono-"}, {"di", "bi", "di-", "diplo"}, {"levo", "sinistr/o"}, {"dia", "per", "trans"},
              {"-algia", "-dynia"}, {"in-", "un-", "a-", "dis-"}, {"hemi", "semi"}, {"macro", "mega"},
              {"homo", "iso"}, {"noct/i", "nyct/o"}, {"xanth/o", "icter/"}, {"ex/o", "ecto", "ab"},
              {"pre-", "pro-", "ante-"}, {"hyper-", "super-"}, {"-iatrics", "-iatry", "-logy"}, {"-ist", "-ian", "-iatrist"},
              {"adip/o", "lip/o", "steat/o"}, {"-rrhage", "-rrhea"}, {"multi", "poly"}, {"-graph", "-gram", "-graphy"},
              {"-tome", "-tomy", "-ectomy"}, {"-scope", "-scopy"}, {"-meter", "-metry"}]


def same_group(a, b):
    return any(a in g and b in g for g in SYN_GROUPS)


Q = []
qid = [0]


def add(lec, slide, typ, q, options=None, answer=None, explain="", correction=None, **kw):
    qid[0] += 1
    item = {"id": f"q{qid[0]:03d}", "lec": lec, "slide": slide, "type": typ, "q": q, "options": options or [],
            "answer": answer, "explain_ar": explain}
    if correction: item["correction"] = correction
    item.update(kw)
    Q.append(item)


def pick(cands, n, ok):
    cands = [c for c in cands if ok(c)]
    rng.shuffle(cands)
    out = []
    for c in cands:
        if c in out: continue
        out.append(c)
        if len(out) == n: break
    return out


def mcq(lec, slide, q, correct, distractors, explain):
    opts = [correct] + list(distractors)
    rng.shuffle(opts)
    add(lec, slide, "mcq", q, opts, correct, explain)


ALLROWS = [(s, r) for s in sections if s["id"] not in ("numchart", "anti", "easy") for r in s["rows"]]
by_kind = {}
for s, r in ALLROWS:
    by_kind.setdefault(s["kind"], []).append((s, r))


def first_example(ex):
    return re.split(r"\s*[·,/]\s*|\s+\(", ex)[0].strip()


def ok_distractor(r, o):
    return o is not r and not clash(r["meaning"], o["meaning"]) and not same_group(r["part"], o["part"])


def distractors(r, pool_same, pool_kind, n=3):
    """Pick n wrong rows: not synonyms of r, and with meanings distinct from each other."""
    ds = []
    for pool in (pool_same, pool_kind):
        cands = [o for o in pool if ok_distractor(r, o) and not overlap(r["meaning"], o["meaning"])]
        rng.shuffle(cands)
        for o in cands:
            if len(ds) == n: break
            if o in ds or any(overlap(o["meaning"], d["meaning"]) or first_example(o["example"]).lower() == first_example(d["example"]).lower() for d in ds):
                continue
            ds.append(o)
    return ds if len(ds) == n else None


MEANING_COUNT = {}
for _s, _r in ALLROWS:
    MEANING_COUNT[(_s["kind"], _r["meaning"].lower())] = MEANING_COUNT.get((_s["kind"], _r["meaning"].lower()), 0) + 1


ROT = ["meaning", "part", "spell", "tf", "def"]
for i, (s, r) in enumerate(ALLROWS):
    kind, lec, slide = s["kind"], s["lec"], s["slide"]
    pool_same = [o for ss, o in ALLROWS if ss is s]
    pool_kind = [o for ss, o in by_kind[kind]]
    ex1 = first_example(r["example"])
    expl = f"{r['part']} = {r['meaning']} (مثال: {ex1})."
    ts = [ROT[i % 5], ROT[(i + 2) % 5]]  # two questions per table row
    if "part" in ts and MEANING_COUNT[(kind, r["meaning"].lower())] > 1:
        # several parts share this meaning -> "Which part means X?" would be ambiguous
        alt = "spell" if re.fullmatch(r"[A-Za-z]+", ex1) and "spell" not in ts else "meaning"
        ts[ts.index("part")] = alt if alt not in ts else "tf"
    for t in ts:
        if t == "meaning":
            ds = distractors(r, pool_same, pool_kind)
            if ds: mcq(lec, slide, f"The {kind} “{r['part']}” means:", r["meaning"], [d["meaning"] for d in ds], expl)
        elif t == "part":
            ds = distractors(r, pool_same, pool_kind)
            if ds and t == "part":
                mcq(lec, slide, f"Which {kind} means “{r['meaning']}”?", r["part"], [d["part"] for d in ds], expl)
            elif ds:
                mcq(lec, slide, f"“{r['definition'].split(' · ')[0]}” is the definition of:", ex1,
                    [first_example(d["example"]) for d in ds], expl)
        elif t == "spell":
            if re.fullmatch(r"[A-Za-z]+", ex1):
                add(lec, slide, "spell", f"Write the medical term ({', '.join([r['part']] + r['alts'])} = {r['meaning']}): “{r['definition'].split(' · ')[0]}”",
                    [], ACCEPT.get(ex1.lower(), [ex1.lower()]), f"الكلمة: {ex1}.")
        elif t == "tf":
            if rng.random() < 0.5:
                add(lec, slide, "tf", f"“{r['part']}” means {r['meaning']}.", [], True, expl)
            else:
                ds = pick(pool_same + pool_kind, 1, lambda o: ok_distractor(r, o))
                if ds:
                    add(lec, slide, "tf", f"“{r['part']}” means {ds[0]['meaning']}.", [], False, expl,
                        correction=f"“{r['part']}” means {r['meaning']}; “{ds[0]['part']}” means {ds[0]['meaning']}.")
        elif t == "def":
            ds = distractors(r, pool_same, pool_kind)
            if ds and ex1:
                mcq(lec, slide, f"“{r['definition'].split(' · ')[0]}” is the definition of:", ex1,
                    [first_example(d["example"]) for d in ds], expl)

chart = next(s for s in sections if s["id"] == "numchart")
for r in chart["rows"]:
    ds = pick(chart["rows"], 3, lambda o: o is not r)
    mcq(3, "23", f"In the number-prefix chart, “{r['part']}” means:", r["meaning"], [d["meaning"] for d in ds],
        f"{r['part']} = {r['meaning']}: {r['definition']}.")

for a in analysis:  # typed: build the term from its parts
    pieces = [p["text"] + (f" ({p['meaning']})" if p["meaning"] else "") for p in a["parts"]]
    add(a["lec"], a["slide"], "build", "Build the term: " + " + ".join(pieces), [],
        ACCEPT.get(a["term"].lower(), [a["term"].lower()]), f"{a['term']} = {a['medical']}.")
SPLIT_ALSO = {"Hemorrhage": ["hemor / rhage"]}  # the slide's own split is also accepted
SPLIT_NOTE = {"Hemorrhage": "تقسيم السلايد hemor (blood) / rhage (flow) مقبول برضه.",
              "Diarrhea": "السلايد كاتب diarr = through / hea = flow وده سهو: نفس الجدول بيقول -rrhea = flow، فالصح dia (through) + rrhea (flow)."}
for a in analysis:  # typed: split worked examples + homework
    if a["workedOnSlide"] or a["slide"] == "24":
        split = " / ".join(re.sub(r"\(.*?\)", "", p["text"]) for p in a["parts"])
        accept = [split] + SPLIT_ALSO.get(a["term"], [])
        add(a["lec"], a["slide"], "analyze", f"Analyse {a['term']} into its parts (prefix / root / combining vowel / suffix).",
            [], accept, f"{a['term']}: {split} → {a['medical']}." + (" " + SPLIT_NOTE[a["term"]] if a["term"] in SPLIT_NOTE else ""))

for p in plurals:
    add(2, p["slide"], "spell", f"According to the slide (Latin plural), write the plural of “{p['singular']}” ({p['meaning']}).", [], [p["plural"]],
        f"{p['ending']} → {p['pluralEnding']}: {p['singular']} → {p['plural']}.")
    mcq(2, p["slide"], f"According to the slide (Latin plural), the plural of “{p['singular']}” is:", p["plural"], p["_wrong"], f"{p['ending']} → {p['pluralEnding']}.")
for p in plurals:
    p.pop("_wrong")

SOUNDS = sorted({x["sound"] for x in pronunciation})
for p in pronunciation:
    ds = [s for s in SOUNDS if s != p["sound"]]
    rng.shuffle(ds)
    mcq(2, p["slide"], f"At the start of a word, “{p['letters']}” is pronounced like:", p["sound"], ds[:3],
        f"{p['letters']} → {p['sound']} ({', '.join(p['examples'])}).")

for c in D.QUIZ:
    lec, slide = c["lec"], pages(c["s"])
    if c["type"] == "mcq":
        add(lec, slide, "mcq", c["q"], c["o"], c["o"][c["a"]], c["ex"])
    else:
        add(lec, slide, "tf", c["q"], [], c["a"], c.get("fix") or "صح — زي ما مكتوب في السلايد.", correction=c.get("fix"))

for r in rules:
    others = [x["rule"] for x in rules if x is not r]
    rng.shuffle(others)
    mcq(2, r["slide"], f"Which rule explains: {r['example'].split(' — ')[0]}?", r["rule"], others[:3], r.get("ar", ""))

content = {"meta": meta, "concepts": concepts, "rules_intro": rules_intro, "rules": rules, "pronunciation": pronunciation,
           "plurals": plurals, "sections": sections, "analysis": analysis, "lookalikes": lookalikes,
           "spellingTraps": spellingTraps, "questions": Q}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(content, f, ensure_ascii=False, indent=1)
print("written", os.path.normpath(OUT), "questions:", len(Q))
