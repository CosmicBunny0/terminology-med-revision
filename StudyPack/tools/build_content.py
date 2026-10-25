"""Builds StudyPack/content/content.json from slide_data.py.

Run:  python -I StudyPack/tools/build_content.py   then   python -I StudyPack/tools/check_content.py
"slide" = PDF page number(s) inside that lecture's file.

Question bank (Stage 3b): every question is slide-grounded (rules R0–R8 in CLAUDE.md / HANDOFF.md) and carries
difficulty (easy|medium|hard|max), skill, score (1–100, computed below) and evidence [{file, page, quote}].
"""
import json, os, re, random, sys, datetime, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import slide_data as D

OUT = os.path.join(HERE, "..", "content", "content.json")
KIND = {"p": "prefix", "r": "root", "v": "vowel", "s": "suffix"}
SEED = 25102026
rng = random.Random(SEED)
FILE = {s["lec"]: s["file"] for s in D.META["sources"]}
NPAGES = {s["lec"]: s["pages"] for s in D.META["sources"]}


def pages(src):
    """'L3 p4, p7–9' -> '4, 7–9'"""
    return re.sub(r"L\d p|p", "", src).strip()


def lec_of(src):
    return int(re.match(r"L(\d)", src).group(1))


# =====================================================================================
# Slide corpus + grounding (shared with check_content.py)
# =====================================================================================
CONTENT_DIR = os.path.join(HERE, "..", "content")
# plain-English slide typos are fixed silently (R5): the corpus is matched with these fixes applied
SILENT = [("to loss water", "to lose water"), ("out put", "output"), ("having and intended", "having an intended"),
          ("defination", "definition"), ("memberane", "membrane"), ("combing vowel", "combining vowel"),
          ("reputure", "rupture"), ("rapture of the amniotic", "rupture of the amniotic")]


def gnorm(s):
    s = unicodedata.normalize("NFKC", str(s)).lower()
    s = s.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'").replace("—", "-").replace("–", "-")
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"\(\s+", "(", s); s = re.sub(r"\s+\)", ")", s); s = re.sub(r"\s+([,;:.])", r"\1", s)
    s = re.sub(r"\s*-\s*", "-", s); s = re.sub(r",\s*", ",", s)
    return s.strip().rstrip(".")


def _corpus():
    txt = open(os.path.join(CONTENT_DIR, "slide-transcription.md"), encoding="utf-8").read()
    layer = json.load(open(os.path.join(CONTENT_DIR, "slide-text-layer.json"), encoding="utf-8"))
    c = gnorm(txt + "\n" + "\n".join(layer.values()))
    fixed = c
    for a, b in SILENT:
        fixed = fixed.replace(a, b)
    c = c + "\n" + fixed
    return c + "\n" + c.replace("/", "")  # slide splits written with "/" (electr/o/cardi/o/gram) also count joined


CORPUS = _corpus()


def grounded(s):
    """True if the string is slide text (case/space-insensitive)."""
    n = gnorm(s)
    return bool(n) and n in CORPUS


def grounded_word(w):
    """True if w occurs as a whole word in the slide text (used to make sure a deliberate misspelling is not a real slide word)."""
    return re.search(r"(?<![a-z])" + re.escape(gnorm(w)) + r"(?![a-z])", CORPUS) is not None


def grounded_pieces(s):
    """Composite strings ("False — “x” means “y”", "term: part = meaning", "a | b | c"): every piece must be slide text."""
    if grounded(s):
        return True
    s = re.sub(r"^(True|False)\s*[—-]\s*", "", s)
    quoted = re.findall(r"“([^”]+)”", s)
    if quoted:
        return all(grounded(x) for x in quoted)
    pieces = [p for p in re.split(r"\s*(?:\||;|·| = |: | → | – | and )\s*", s) if p.strip()]
    return len(pieces) > 1 and all(grounded(p) for p in pieces)


# =====================================================================================
# meta / concepts / rules / pronunciation / plurals / sections / analysis
# =====================================================================================
M = D.META
meta = {
    "course": M["course"], "exam": M["exam"],
    "lectures": [{"n": s["lec"], "title": next(l["title"] for l in M["lectures"] if l["lec"] == s["lec"]),
                  "doctor": s["by"], "file": s["file"], "pages": s["pages"]} for s in M["sources"] if s["lec"]],
    "generated": datetime.date.today().isoformat(),
    "title": M["title"], "credit": M["credit"], "disclaimer": M["disclaimer"], "colors": M["colors"],
    "trainingSheet": next(s for s in M["sources"] if s["lec"] == 0),
    "slideTypos": [{"where": t[0], "slide": t[1], "correct": t[2], "how": t[3]} for t in D.SLIDE_TYPOS],
    "excluded": D.EXCLUDED,
    "homework": {"lec": 2, "slide": "24", "terms": D.HOMEWORK["terms"], "note": D.HOMEWORK["note"]},
}

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

rules = []
RULE_PAGE = {"1": 10, "2": 13, "3": 14, "4": 15, "4b": 16}
RULE_QUOTE = {"1": "1-A combing vowel is used to join root to root as well as to any suffix beginning with a constant",
              "2": "2-A combining vowel is not used before a suffix that begins with a vowel",
              "3": "3-If the roots ends in a vowel and the suffix begins with the same vowel, drop the final vowel from the root and do not use a combining vowel",
              "4": "4- when a prefix ends in a vowel and the root begins with a vowel, the final vowel is dropped from the prefix",
              "4b": "4-Most often a combining vowel is inserted between two roots even when the second root begins with a vowel."}
for r in D.RULES:
    rid = "4b" if r["n"] == 5 else str(r["n"])
    rules.append({"id": rid, "lec": 2, "slide": pages(r["src"]), "rule": r["rule"], "example": r["ex"],
                  **({"ar": r["ar"]} if r.get("ar") else {})})
rules_intro = {"lec": 2, "slide": "9", "body": D.RULES_INTRO["points"]}

pronunciation = []
PRON_PAGE = {"Ch": 18, "C (before a, o, u)": 18, "C (before e, i)": 18, "Dys": 18, "Eu": 18, "Gn": 18}
for l, snd, ex in D.PRON["rows"]:
    pronunciation.append({"letters": l, "sound": snd, "examples": [e.strip() for e in ex.split(",")],
                          "lec": 2, "slide": str(PRON_PAGE.get(l, 19))})

PLURAL_QUOTE = {"vertebra": (20, "a ae vertebra (Bone of the spine ) vertebrae"), "lumen": (20, "en ina lumen (Central opening) lumina"),
                "index": (20, "ex, ix ices index (indicator) indices"), "diagnosis": (20, "is es diagnosis (identification of diseases) diagnoses"),
                "phalanx": (23, "nx (anx,inx,ynx) nges Phalanx ( bone of finger or toe) Phalanges"), "ganglion": (23, "On a Ganglion (mass of nerve tissue ) Ganglia"),
                "ovum": (23, "Um a Ovum (egg) Ova"), "fungus": (23, "Us i Fungus (mold) Fungi")}
plurals = []
PL_WRONG = {}  # deliberate misspellings for plural spelling questions (never valid English plurals)
for end, pend, sing, mean, plur, _wrong in D.PLURALS["rows"]:
    PL_WRONG[sing] = _wrong
    plurals.append({"ending": end, "pluralEnding": pend, "singular": sing, "plural": plur, "meaning": mean,
                    "lec": 2, "slide": "20, 22" if PLURAL_QUOTE[sing][0] == 20 else "23"})

# one page per table row (the page that shows that row; text pages preferred over picture duplicates)
ROW_PAGES = {
    "phys": [7, 7, 7, 7, 8, 8, 8, 9, 9, 9], "time": [11] * 3, "chem": [13, 13, 13, 14, 14, 15, 15, 15, 16, 16, 16], "easy": [17] * 2,
    "dis": [19, 19, 19, 19, 20, 20, 20, 20], "num": [25, 25, 25, 26, 26, 26, 29, 29, 29, 30, 30, 30, 30], "numchart": [23] * 10,
    "size": [32, 32, 32, 32, 33, 33, 33, 34, 34, 34, 35, 35], "color": [36, 36, 36, 36, 37, 37, 37, 37], "dir": [38, 38, 38, 39, 39, 41, 41],
    "pos": [40] * 4, "tpos": [4] * 4, "pdis": [5] * 6, "deg": [6] * 5, "neg": [7] * 4, "anti": [8], "spec": [10] * 6, "cond": [11] * 5,
    "sdis": [13] * 6 + [14] * 6, "diag": [3] * 7, "small": [4] * 4, "surg": [5] * 6 + [6] * 4, "adj": [8] * 11}
# exact slide text where the row data differs from the slide (slide spellings / silent English fixes)
QUOTE_OVERRIDE = {
    "hydr/o": "hydr/o | water, fluid | dehydrate | to loss water",
    "hemi": "Hemi | Half, one side | Hemi thorax | One side of the chest ( thorax)",
    "polio": "Polio, Glauc/o | grey | Polioencephalities | Inflammation of the gray matter of the brain",
    "olig/o": "Olig/o | Few or deficiency of | Oligospermia; Oligouria | Low number of sperm in the semen; Low urine out put",
    "-dynia": "-Dysnia, -Dynia | Pain | Cephalodynia | Pain in the head (headache)",
    "-rhage": "-Rhage, -Rhagia | Bursting, Profuse flow | Hemorrhage (hemor = blood, rhage = flow) | Profuse flow of blood",
    "-rhea": "-Rhea | Flow, discharge | Diarrrhea (diarr = through, hea = flow) | Frequent passage of watery stool",
    "-rhexis": "-Rhexis | Reputure | Amniorrhexis (amnio = amniotic sac, rhexis = rupture) | Rapture of the amniotic sac (bag of waters)",
    "ferr/i": "ferr/i, ferr/o | Iron | Ferric; Ferrous | ferric: containing iron in oxidized form; ferrous: containing iron in reduced",
    "in-": "In-, Im- | Not | Incontinence; Imbalance | Lack of control over excretion • Not moving; Not being in balance",
    "-oma": "-Oma | Tumor | Lipoma (lip = fat, oma = tumor) | Fatty tumor",
    "-pathy": "-Pathy | Any disease of | Neuropathy (neuro = nerve, pathy = disease) | Any disease of the nervous system",
    "-ive": "suffixes that mean “pertaining to”: -ive | Effective | Pertaining to having and intended effect",
}
TITLE_QUOTE = {"cond": "Suffix that mean “condition of”", "small": "suffixes that mean “small”"}


def row_quote(sid, r):
    if r["part"] in QUOTE_OVERRIDE:
        return QUOTE_OVERRIDE[r["part"]]
    exs = "; ".join(x.strip() for x in re.split(r"\s*·\s*", r["example"]) if x.strip())
    dfs = "; ".join(x.strip() for x in re.split(r"\s*·\s*", r["definition"]) if x.strip())
    forms = ", ".join([r["part"]] + r["alts"])
    if sid == "numchart":
        return f"{r['part'].capitalize()}({r['meaning']}): {r['definition'].replace(' · ', ', ')}"
    if sid == "easy":
        return f"{r['part']} → {r['meaning']}"
    if sid in TITLE_QUOTE:
        return f"{TITLE_QUOTE[sid]}: {forms} | {exs} | {dfs}"
    if sid == "adj":
        t = "suffixes that mean “Similar to”" if r["part"] in ("-form", "-oid") else "suffixes that mean “pertaining to”"
        return f"{t}: {forms} | {exs} | {dfs}"
    return f"{forms} | {r['meaning']} | {exs} | {dfs}"


sections = []
for s in D.SECTIONS:
    rows = []
    pg = ROW_PAGES[s["id"]]
    assert len(pg) == len(s["rows"]), s["id"]
    for r, p in zip(s["rows"], pg):
        forms = [f.strip() for f in r["part"].split(",")]
        row = {"part": forms[0], "alts": forms[1:], "meaning": r["meaning"], "example": r["example"],
               "definition": r["definition"], "note": r.get("note", ""), "page": p}
        row["quote"] = row_quote(s["id"], row)
        rows.append(row)
    sec = {"id": s["id"], "lec": s["lec"], "slide": pages(s["src"]), "kind": s["kind"], "title": s["title"], "rows": rows}
    if s.get("subtitle"): sec["subtitle"] = s["subtitle"]
    if s.get("note"): sec["note"] = s["note"]
    sections.append(sec)

A = D.A
EXTRA_ANALYSIS = [
    A("Antenatal", 4, "L4 p4", [["p", "ante", "before", "table"], ["r", "nat", "birth", "def"], ["s", "al", "pertaining to", "table"]], "Before birth"),
    A("Postoperative", 4, "L4 p4", [["p", "post", "after, behind", "table"], ["r", "operat", "(surgical) operation", "def"], ["s", "ive", "pertaining to", "table"]], "After a surgical operation"),
    A("Hypertension", 4, "L4 p6", [["p", "hyper", "over, excess, abnormally high, high, increased", "table"], ["r", "tens", "(blood) pressure", "def"], ["s", "ion", None, "extra"]], "High blood pressure"),
    A("Superinfection", 4, "L4 p6", [["p", "super", "above or excess", "table"], ["r", "infect", "infection", "def"], ["s", "ion", None, "extra"]], "Second infection"),
    A("Imbalance", 4, "L4 p7", [["p", "im", "not", "table"], ["r", "balance", "balance", "def"]], "Not being in balance"),
    A("Analgesia", 4, "L4 p7", [["p", "an", "not", "table"], ["r", "alges", "pain", "def"], ["s", "ia", None, "extra"]], "Pain killer"),
    A("Ventricle", 5, "L5 p4", [["r", "ventri", "belly, pouch", "def"], ["s", "cle", "small", "table"]], "Small belly or pouch - A cavity"),
    A("Pustule", 5, "L5 p4", [["r", "pust", "pimple", "def"], ["s", "ule", "small", "table"]], "Small pimple"),
    A("Mucoid", 5, "L5 p8", [["r", "muc", "mucus", "def"], ["s", "oid", "similar to", "table"]], "Like or resembling mucus"),
    A("Febrile", 5, "L5 p8", [["r", "febr", "fever", "def"], ["s", "ile", "pertaining to", "table"]], "Pertaining to fever"),
]
# exact slide text for the worked examples (L1, L2 text layer)
ANALYSIS_QUOTE = {
    "Carcinogen": (1, 13, "Carcinogen Carcin gen + Root Suffix carcin/o/gen O + Combining Vowel Producing Cancer Substance that promotes the formation of cancer"),
    "Pericarditis": (1, 14, "Pericarditis Peri card itis + + prefix Root Suffix Around Inflammation Heart inflammation around the heart"),
    "Lipemia": (1, 15, "Lipemia lip emia + Root Suffix Blood condition Fat A condition of fat in blood"),
    "Hyperlipemia": (1, 19, "hyperlipemia lip emia + Root Suffix Blood condition Fat A condition of excessive fat in blood + Hyper prefix Excessive"),
    "Cardiac": (1, 20, "Cardiac Cardi / ac ac + Cardi root suffix Pertaining to / Related to Heart Pertaining to heart"),
    "Hyperlipoproteinemia": (2, 7, "Hyper/lip/o/protein/emia Root Suffix prefix Root vowel A condition of excessive fat and protein in blood Hyperlipoproteinemia"),
    "Electrocardiogram": (2, 10, "Electr cardi gram + + Root Root Suffix Electric Record Electr/o/cardi/o/gram Electrical record of the heart Heart"),
    "Vasectomy": (2, 13, "Vas Ectomy + Root Suffix Vessel excision Excision of a vessel"),
    "Carditis": (2, 14, "Inflammation of heart Heart cardi itis + Inflammation Carditis"),
    "Parenteral": (2, 15, "para enter al + + prefix Root Suffix Alongside of Pertaining to Pertaining to alongside of the intestine Parenteral"),
    "Cardioesophageal": (2, 16, "Cardi esophag eal Root Root Suffix cardi/o/esophag/eal pertaining to heart and esophagus Pertaining to Heart"),
}
# colour splits shown on the slides (slide-transcription.md, "Colour splits"): term -> (lec, page, split)
COLOUR = {}
for line in open(os.path.join(CONTENT_DIR, "slide-transcription.md"), encoding="utf-8").read().split("## Colour splits", 1)[1].splitlines()[1:]:
    m = re.match(r"L(\d) p(\d+): (.*)", line.strip())
    if not m: continue
    for item in m[3].split(" · "):
        sp = re.sub(r"\s*\(.*\)$", "", item).strip()
        COLOUR[sp.replace("|", "").lower()] = (int(m[1]), int(m[2]), sp)
COLOUR["diarrhea"] = (4, 14, "Diarr|rhea")  # slide word is printed "Diarrrhea"

analysis = []
for a in D.ANALYSIS + EXTRA_ANALYSIS:
    parts = [{"type": KIND[p["t"]], "text": p["x"], "meaning": None if p["src"] == "extra" else (p["m"] or None),
              "from": p["src"]} for p in a["parts"]]
    item = {"term": a["term"], "lec": a["lec"], "slide": pages(a["src"]), "parts": parts,
            "literal": " + ".join(p["meaning"] for p in parts if p["meaning"] and p["from"] in ("slide", "table")),
            "medical": a["def"], "workedOnSlide": a["kind"] == "slide"}
    if "Your turn" in a["src"]:
        item["slide"] = "24"; item["alsoSee"] = a["src"].split("·")[-1].strip()
    if a.get("note"): item["note"] = a["note"]
    analysis.append(item)

lookalikes = [{"title": c["t"], "lec": lec_of(c["src"]), "slide": c["src"],
               "rows": [{"part": r[0], "meaning": r[1], "example": r[2]} for r in c["rows"]],
               "tip": c["tip"], "tipIsExtra": bool(c.get("tip_extra"))} for c in D.CONFUSE]

# ---------------- spelling traps ("say" is (extra)); slide-typo words and British spellings are never listed ----------------
TRAPS = [  # word, common wrong forms, say, lec, slide
    ("hemorrhage", "hemorage · hemmorhage", "HEM-or-ij", 4, "14"),
    ("amniorrhexis", "amniorexis · amniorhexis", "am-nee-or-REK-sis", 4, "14"),
    ("herniorrhaphy", "herniorraphy · herniorhaphy", "her-nee-OR-uh-fee", 5, "5"),
    ("steatorrhea", "steatorhea · steatorrea", "stee-at-oh-REE-uh", 3, "16"),
    ("pyorrhea", "pyorhea · pyrorrhea", "pye-oh-REE-uh", 3, "20"),
    ("tonsillectomy", "tonsilectomy", "ton-sil-LEK-tuh-mee", 5, "5"),
    ("parenteral", "paraenteral · parentral", "par-EN-ter-al", 2, "15"),
    ("carditis", "cardiitis · cardioitis", "kar-DYE-tis", 2, "14"),
    ("cardioesophageal", "cardiesophageal · cardesophageal", "KAR-dee-oh-ee-sof-uh-JEE-al", 2, "16"),
    ("electrocardiogram", "electrcardiogram · electrocardiagram", "ee-LEK-troh-KAR-dee-oh-gram", 2, "10"),
    ("vasectomy", "vasoectomy", "vas-EK-tuh-mee", 2, "13"),
    ("hyperlipoproteinemia", "hyperlipproteinemia", "HY-per-LIP-oh-PRO-teen-EE-mee-uh", 2, "7"),
    ("pediatrics", "pedeatrics · pediatrix", "pee-dee-AT-riks", 4, "10"),
    ("psychiatry", "sychiatry · psychiatery", "sy-KY-uh-tree", 4, "10"),
    ("podiatrist", "podiatrest", "poh-DYE-uh-trist", 4, "10"),
    ("nyctophobia", "nictophobia · nyctofobia", "nik-toh-FOH-bee-uh", 3, "11"),
    ("synchronous", "sinchronous · synchronus", "SIN-kruh-nus", 3, "11"),
    ("euthanasia", "euthenasia · uthanasia", "yoo-thuh-NAY-zhuh", 3, "32"),
    ("pseudocyesis", "psudocyesis · pseudocysis", "SOO-doh-sye-EE-sis", 3, "35"),
    ("xanthoma", "zanthoma · xantoma", "zan-THOH-muh", 3, "37"),
    ("leukoplakia", "leukoplasia · lukoplakia", "loo-koh-PLAY-kee-uh", 3, "36"),
    ("erythrocyte", "erythrosyte · erithrocyte", "eh-RITH-roh-site", 3, "36"),
    ("cyanosis", "cyanosys · cianosis", "sye-uh-NOH-sis", 3, "36"),
    ("vertebrae", "vertebras · vertebrea", "VER-tuh-bray", 2, "20"),
    ("phalanges", "phalanxes · phalanxs", "fuh-LAN-jeez", 2, "23"),
    ("ganglia", "ganglii · ganglions (according to the slides the plural is ganglia)", "GANG-lee-uh", 2, "23"),
    ("lumina", "lumena · lumens (according to the slides the plural is lumina)", "LOO-min-uh", 2, "20"),
    ("indices", "indicies · indexes (according to the slides the plural is indices)", "IN-dih-seez", 2, "20"),
    ("diagnoses", "diagnosises", "dye-ag-NOH-seez", 2, "20"),
    ("primigravida", "primagravida · primigravidia", "pry-mih-GRAV-ih-duh", 3, "25"),
    ("tachypnea", "tachypnia · takypnea", "tak-ip-NEE-uh", 4, "5"),
    ("pachyderma", "pachiderma · pakyderma", "pak-ee-DER-muh", 4, "5"),
    ("hyponatremia", "hyponatrimia · hyponatremea", "HY-poh-nuh-TREE-mee-uh", 3, "16"),
    ("hyperkalemia", "hypercalemia · hyperkalimia", "HY-per-kuh-LEE-mee-uh", 3, "15"),
    ("prophylaxis", "profylaxis · prophylaxes", "proh-fuh-LAK-sis", 4, "4"),
    ("xerosis", "zerosis · xerosys", "zih-ROH-sis", 4, "5"),
    ("cephalodynia", "cephalodinia · kephalodynia", "SEF-uh-loh-DIN-ee-uh", 4, "13"),
    ("retinoschisis", "retinoshisis · retinoschysis", "RET-in-OS-kih-sis", 4, "14"),
    ("karyoclasis", "kariyoclasis · karioclasis", "kar-ee-OK-luh-sis", 4, "13"),
    ("amebiasis", "ameobiasis · amebiasys", "am-ee-BYE-uh-sis", 4, "11"),
    ("celiocentesis", "celiocentisis · seliocentesis", "SEE-lee-oh-sen-TEE-sis", 5, "5"),
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

# =====================================================================================
# QUESTION BANK
# =====================================================================================
LEVELS = ["easy", "medium", "hard", "max"]
BAND = {"easy": 0, "medium": 25, "hard": 50, "max": 75}
# ---- DIFFICULTY SCORE WEIGHTS (points added inside the level band; band = 25 points, raw is capped at 24) ----
W = {
    "typed": 6,            # typed answer instead of MCQ/TF
    "reverse": 4,          # reverse direction (meaning -> part, definition -> term)
    "parts2": 2,           # 2 word parts involved
    "parts3": 4,           # 3+ word parts involved
    "nohint": 3,           # typed answer with no hint in the stem
    "close_table": 2,      # all distractors come from the SAME slide table
    "close_lookalike": 4,  # distractors come from a look-alike comparison table
    "len10": 1,            # answer of 10+ letters
    "len14": 2,            # answer of 14+ letters (replaces len10)
    "irregular": 2,        # irregular spelling in the answer (rrh, ph, ps/pn/pt/gn start, y inside, double letters)
    "exception": 3,        # irregular plural or a combining-vowel rule exception (rules 3, 4, 4b)
}
# score = band start + 1 + min(24, sum of the weights that apply); ties are broken by "tie" (seeded random), never lecture order

TYPED = {"spell", "build", "analyze"}
ACCEPT_BOTH = D.ACCEPT_BOTH
TYPO_WORDS = D.TYPO_WORDS
STOP = {"the", "and", "for", "with", "into", "from", "pertaining", "condition", "abnormal", "abnormally", "state", "of", "or", "in", "to", "a", "an"}


def otoks(s):
    return {w for w in re.findall(r"[a-z]+", str(s).lower()) if len(w) > 2 and w not in STOP}


def overlap(m1, m2):
    """True if two meanings are equal or share any content word."""
    return str(m1).strip().lower() == str(m2).strip().lower() or bool(otoks(m1) & otoks(m2))


# R4 synonym groups (slides give the same meaning): never distractors against each other; typed answers accept all
SYN = [{"mon/o", "uni", "mono-"}, {"di", "bi", "di-"}, {"levo", "sinistro/o"}, {"dia", "per", "trans"},
       {"-algia", "-dynia"}, {"in-", "un-", "a-"}, {"macro", "mega"}, {"ante-", "pre-", "pro-"}, {"xanth/o", "icter/"},
       {"homo", "iso"}, {"noct/i", "nyct/o"}, {"hemi", "semi"}, {"multi", "poly"}, {"tri", "tri-"}, {"penta", "penta-"},
       {"quadr/i", "tetra-"}, {"-iatrics", "-iatry"}, {"-ist", "-ian", "-iatrist"}]
# near-synonyms: never distractors against each other (but not accepted for each other)
NEAR = [{"adip/o", "lip/o", "steat/o"}, {"ex/o", "ecto", "ab"}, {"hyper-", "super-"}, {"-rhage", "-rhea"}, {"di", "diplo"},
        {"bi", "diplo"}, {"dis-", "in-", "un-", "a-"}, {"prim/i", "mon/o", "uni"}, {"-cle", "-ole", "-ula", "-ule"},
        {"chrom/o", "cyan/o", "erythr/o", "leuk/o", "melan/o", "xanth/o", "icter/", "polio", "verd/o"}]


def syn(a, b):
    return a == b or any(a in g and b in g for g in SYN)


def near(a, b):
    return syn(a, b) or any(a in g and b in g for g in NEAR)


# ---------------- testable rows ----------------
ROWS = []
for s in sections:
    if s["id"] == "anti":   # anti- has no slide meaning (R3)
        continue
    for r in s["rows"]:
        exs = [x.strip() for x in re.split(r"\s*·\s*|,\s*", r["example"]) if x.strip()]
        dfs = [x.strip() for x in re.split(r"\s*·\s*", r["definition"]) if x.strip()]
        ROWS.append({"sid": s["id"], "title": s["title"], "kind": s["kind"], "lec": s["lec"], "page": r["page"], "quote": r["quote"],
                     "part": r["part"], "forms": [r["part"]] + r["alts"], "meaning": r["meaning"],
                     "ex": [re.split(r"\s+\(", e)[0].strip() for e in exs], "defs": dfs})
SLIDE_FORM = {"hemithorax": "Hemi thorax", "polioencephalitis": "Polioencephalities", "oliguria": "Oligouria"}
for r in ROWS:
    r["ex1"] = r["ex"][0] if r["ex"] else ""
    r["typo"] = r["ex1"].lower() in SLIDE_FORM
    r["ex1s"] = SLIDE_FORM.get(r["ex1"].lower(), r["ex1"])  # shown exactly as the slide prints it
    r["def1"] = r["defs"][0] if r["defs"] else ""
    r["word"] = r["ex1"].lower() if re.fullmatch(r"[A-Za-z]+", r["ex1"]) else ""


def same_meaning(a, b):
    return a["kind"] == b["kind"] and (a["meaning"].strip().lower() == b["meaning"].strip().lower() or syn(a["part"], b["part"]))


def row_near(a, b):
    return a is b or same_meaning(a, b) or near(a["part"], b["part"]) or overlap(a["meaning"], b["meaning"])


def stems(f):
    out = {f}
    st = re.sub(r"/[aeiou]?$", "", f)
    if st != f: out.add(st)
    return out


def accept_parts(r):
    out = []
    for o in ROWS:
        if same_meaning(r, o):
            for f in o["forms"]:
                for x in sorted(stems(f)) + ACCEPT_BOTH.get(f, []):
                    if x not in out: out.append(x)
    return out


def accept_word(w):
    w = w.lower()
    return [w] + [x for x in ACCEPT_BOTH.get(w, []) if x != w]


# terms that share a definition on the slides (e.g. "Pertaining to fever": pyretic AND febrile) are all accepted
DEF_WORDS = {}
for r in ROWS:
    if r["word"] and r["def1"]:
        DEF_WORDS.setdefault(gnorm(r["def1"]), set()).add(r["word"])


def ev(lec, page, quote):
    return {"file": FILE[lec], "page": page, "quote": quote}


def rev(r):
    return ev(r["lec"], r["page"], r["quote"])


IRREG = re.compile(r"rrh|rh|ph|^ps|^pn|^pt|^gn|^x|y(?!$)|([bcdfgklmnprstz])\1")

Q = []


def add(lec, typ, q, answer, level, skill, evidence, tests, explain, options=None, correction=None, feat=None, **kw):
    if not re.search(r"L\d", explain):
        explain += f" (L{lec} p{evidence[0]['page']})"
    item = {"id": "", "lec": lec, "slide": str(evidence[0]["page"]), "type": typ, "q": q, "options": options or [],
            "answer": answer, "explain_ar": explain, "difficulty": level, "skill": skill, "evidence": evidence,
            "tests": sorted({t.lower().strip("-/ ") for t in tests if t})}
    if correction: item["correction"] = correction
    item.update(kw)
    f = dict(feat or {})
    f.setdefault("typed", typ in TYPED)
    item["_feat"] = f
    Q.append(item)
    return item


def mcq(lec, q, correct, distractors, level, skill, evidence, tests, explain, feat=None, **kw):
    opts = [correct] + list(distractors)
    assert len(set(o.lower() for o in opts)) == 4, (q, opts)
    rng.shuffle(opts)
    return add(lec, "mcq", q, correct, level, skill, evidence, tests, explain, options=opts, feat=feat, **kw)


def pick_rows(r, n, ok, pools):
    """n distractor rows (pool order = preference), mutually non-near."""
    out = []
    for pool in pools:
        cands = [o for o in pool if o is not r and ok(o) and o not in out]
        rng.shuffle(cands)
        for o in cands:
            if len(out) == n: break
            if any(row_near(o, d) for d in out): continue
            out.append(o)
    return out if len(out) == n else None


def pools_for(r):
    same = [o for o in ROWS if o["sid"] == r["sid"]]
    lec_kind = [o for o in ROWS if o["lec"] == r["lec"] and o["kind"] == r["kind"] and o["sid"] != r["sid"]]
    kind = [o for o in ROWS if o["kind"] == r["kind"] and o["lec"] != r["lec"]]
    return [same, lec_kind, kind]


def closeness(r, ds):
    return 1 if all(d["sid"] == r["sid"] for d in ds) else 0


def expl_row(r):
    ex = f" — مثال السلايد: {r['ex1']}" + (f" = {r['def1']}" if r['def1'] else "") if r["ex1"] else ""
    return f"“{r['part']}” معناها {r['meaning']}{ex}. (L{r['lec']} p{r['page']})"


# ---------------- row families ----------------
def E1(r):  # part -> meaning
    ds = pick_rows(r, 3, lambda o: not row_near(r, o), pools_for(r))
    if not ds: return None
    return mcq(r["lec"], f"The {r['kind']} “{r['part']}” means:", r["meaning"], [d["meaning"] for d in ds], "easy", "recall",
               [rev(r)], [r["part"]], expl_row(r), feat={"close": closeness(r, ds)})


def E2(r):  # term -> its slide definition
    if not (r["ex1"] and r["def1"]): return None
    ds = pick_rows(r, 3, lambda o: o["def1"] and gnorm(o["def1"]) != gnorm(r["def1"]) and o["ex1"].lower() != r["ex1"].lower(), pools_for(r))
    if not ds: return None
    return mcq(r["lec"], f"On the slides, “{r['ex1s']}” is defined as:", r["def1"], [d["def1"] for d in ds], "easy", "recall",
               [rev(r)], [r["part"]], expl_row(r), feat={"close": closeness(r, ds)})


def E3(r):  # single-fact true/false
    if rng.random() < 0.5:
        return add(r["lec"], "tf", f"The {r['kind']} “{r['part']}” means “{r['meaning']}”.", True, "easy", "recall", [rev(r)], [r["part"]],
                   "صح. " + expl_row(r))
    ds = pick_rows(r, 1, lambda o: not row_near(r, o), pools_for(r))
    if not ds: return None
    d = ds[0]
    return add(r["lec"], "tf", f"The {r['kind']} “{r['part']}” means “{d['meaning']}”.", False, "easy", "recall", [rev(r), rev(d)], [r["part"]],
               "غلط. " + expl_row(r), correction=f"“{r['part']}” means “{r['meaning']}”; “{d['part']}” means “{d['meaning']}”.")


def M1(r):  # meaning -> part (MCQ)
    ds = pick_rows(r, 3, lambda o: not row_near(r, o), pools_for(r))
    if not ds: return None
    return mcq(r["lec"], f"Which {r['kind']} means “{r['meaning']}”?", r["part"], [d["part"] for d in ds], "medium", "reverse",
               [rev(r)], [r["part"]], expl_row(r), feat={"reverse": True, "close": closeness(r, ds)})


def M2(r):  # meaning -> part (typed)
    acc = accept_parts(r)
    return add(r["lec"], "spell", f"Write the {r['kind']} from the slides that means “{r['meaning']}” ({r['title']}).", acc, "medium", "reverse",
               [rev(r)], [r["part"]], expl_row(r) + (" مقبول كمان: " + ", ".join(acc) if len(acc) > 1 else ""),
               feat={"reverse": True, "hint": True}, answerShown=r["part"])


def M4(r):  # true/false with correction, as a 4-option judgement
    ds = pick_rows(r, 3, lambda o: not row_near(r, o), pools_for(r))
    if not ds: return None
    wrong = ds[0]
    correct = f"False — “{r['part']}” means “{r['meaning']}”"
    opts = [f"True", f"False — “{r['part']}” means “{ds[1]['meaning']}”", f"False — “{r['part']}” means “{ds[2]['meaning']}”"]
    return mcq(r["lec"], f"“The {r['kind']} {r['part']} means: {wrong['meaning']}.” Choose the correct judgement:", correct, opts, "medium", "error-find",
               [rev(r), rev(wrong)], [r["part"]], "غلط. " + expl_row(r), feat={"close": closeness(r, ds)})


def is_trap(w):
    return bool(IRREG.search(w)) or len(w) >= 12


def SPELL(r, level, k=0):  # definition -> term (typed); medium/hard with a part hint, max without
    if k >= min(len(r["ex"]), len(r["defs"])): return None
    w = r["ex"][k].lower() if re.fullmatch(r"[A-Za-z]+", r["ex"][k]) else ""
    d1 = r["defs"][k]
    if not w or not d1: return None
    words = sorted(DEF_WORDS.get(gnorm(d1), {w}))
    acc = []
    for x in words:
        acc += [y for y in accept_word(x) if y not in acc]
    hint = level != "max"
    q = f"Write the slide term for: “{d1}”" + (f" (hint: {r['part']} = {r['meaning']})." if hint else ".")
    shown = SLIDE_FORM.get(w, r["ex"][k])
    return add(r["lec"], "spell", q, acc, level, "spell", [rev(r)], [r["part"], w],
               f"الكلمة: {shown}" + (f" (مقبول كمان: {', '.join(acc[1:])})" if len(acc) > 1 else "") + f" — {r['part']} = {r['meaning']}. (L{r['lec']} p{r['page']})",
               feat={"reverse": True, "hint": hint, "word": w}, answerShown=shown)


def edits1(w):
    """one-letter misspellings of w (deliberate, for near-miss spelling sets)."""
    out = []
    for i in range(len(w) - 1):  # drop one of a doubled letter
        if w[i] == w[i + 1]: out.append(w[:i] + w[i + 1:])
    for i, ch in enumerate(w):  # double a single consonant
        if ch in "lmnprst" and (i + 1 >= len(w) or w[i + 1] != ch) and (i == 0 or w[i - 1] != ch) and 0 < i < len(w) - 1:
            out.append(w[:i] + ch + w[i:])
    sub = {"y": "i", "i": "e", "e": "i", "a": "e", "o": "a", "c": "k", "k": "c", "s": "c"}
    for i, ch in enumerate(w):
        if ch in sub and 0 < i:
            out.append(w[:i] + sub[ch] + w[i + 1:])
    bad = re.compile(r"ae|oe")  # never British-looking forms (R5)
    seen, res = {w}, []
    for x in out:
        if x in seen or (bad.search(x) and not bad.search(w)) or grounded_word(x): continue
        seen.add(x); res.append(x)
    return res


def X7(r):  # near-miss spelling set (4 options, one letter apart, only the slide spelling is right)
    w = r["word"]
    if not w or w in TYPO_WORDS or not r["def1"] or not is_trap(w): return None
    vs = edits1(w)
    if len(vs) < 3: return None
    rng.shuffle(vs)
    return mcq(r["lec"], f"Which spelling is the slide term for “{r['def1']}”?", w, vs[:3], "max", "spell", [rev(r)], [r["part"], w],
               f"الإملا الصح زي السلايد: {w}. (L{r['lec']} p{r['page']})", feat={"word": w}, misspellings=vs[:3])


# look-alike tables (L3–L5 comparison groups): rows looked up by part
def find_row(part):
    for r in ROWS:
        if part in r["forms"] and r["sid"] != "numchart":
            return r
    return None


LOOK = []
for c in D.CONFUSE:
    grp = [find_row(x[0].split(",")[0].strip()) for x in c["rows"]]
    grp = [g for g in grp if g]
    if len(grp) >= 2: LOOK.append(grp)


def H1(r):  # discriminate between look-alikes: definition -> term (or meaning -> part)
    grp = next((g for g in LOOK if r in g), None)
    if not grp: return None
    cands = [o for o in grp if o is not r and not same_meaning(r, o) and not syn(r["part"], o["part"]) and not o["typo"]]
    use_term = bool(r["ex1"] and r["def1"]) and all(o["ex1"] for o in cands)
    ds = []
    for o in cands:
        if any(same_meaning(o, d) or (use_term and o["ex1"].lower() == d["ex1"].lower()) for d in ds): continue
        if use_term and o["ex1"].lower() == r["ex1"].lower(): continue
        ds.append(o)
    if len(ds) < 1: return None
    pools = pools_for(r)
    fill = pick_rows(r, 3 - len(ds), lambda o: o not in ds and not o["typo"] and not row_near(r, o) and not any(row_near(o, d) for d in ds) and (not use_term or o["ex1"]), pools) if len(ds) < 3 else []
    if fill is None: return None
    ds = (ds + fill)[:3]
    if use_term:
        return mcq(r["lec"], f"Which slide term means “{r['def1']}”?", r["ex1s"], [d["ex1"] for d in ds], "hard", "discriminate",
                   [rev(r)] + [rev(d) for d in ds[:2]], [r["part"]], expl_row(r), feat={"close": 2, "reverse": True})
    return mcq(r["lec"], f"Which {r['kind']} means “{r['meaning']}”?", r["part"], [d["part"] for d in ds], "hard", "discriminate",
               [rev(r)] + [rev(d) for d in ds[:2]], [r["part"]], expl_row(r), feat={"close": 2, "reverse": True})


# ---------------- analysis (word structure) ----------------
def seg_variants(parts):
    """accepted splits: the slide split, the vowel joined to the part before it, and r moved across an rrh/rh seam."""
    base = [p["text"].replace("(", "").replace(")", "") for p in parts]
    out = []

    def push(segs):
        s = " / ".join(x for x in segs if x)
        if s not in out: out.append(s)
    push(base)
    merged = []
    for p, t in zip(parts, base):
        if p["type"] == "vowel" and merged: merged[-1] += t
        else: merged.append(t)
    push(merged)
    for segs in (list(base), list(merged)):
        for i in range(1, len(segs)):
            if segs[i].startswith("rrh"):
                v = segs[:]; v[i - 1] += "r"; v[i] = v[i][1:]; push(v)
            elif segs[i].startswith("rh") and segs[i - 1].endswith("r"):
                v = segs[:]; v[i - 1] = v[i - 1][:-1]; v[i] = "r" + v[i]; push(v)
    return out


SPLIT_EXTRA = {"Dextrocardia": ["dextro / cardia"],   # colour split Dextro|cardia on L3 p40 (4f)
               "Amniorrhexis": ["amnio / rrhexis", "amni / o / rrhexis"], "Hemorrhage": ["hem / o / rrhage", "hemo / rrhage"],
               "Neuropathy": ["neur / o / pathy"], "Retinoschisis": ["retin / o / schisis"], "Diarrhea": ["diar / rhea"],
               "Pachyderma": ["pachy / derma"], "Primigravida": ["primi / gravida"]}


def an_quote(a):
    if a["term"] in ANALYSIS_QUOTE:
        l, p, qt = ANALYSIS_QUOTE[a["term"]]
        return [ev(l, p, qt)]
    out = []
    c = COLOUR.get(a["term"].lower())
    if c:
        out.append(ev(c[0], c[1], f"{c[2]} (colour split on the slide)"))
    for r in ROWS:
        if a["term"].lower() in [e.lower() for e in r["ex"]]:
            out.append(rev(r)); break
    if a.get("alsoSee") or a["slide"] == "24":
        out.insert(0, ev(2, 24, "1-Hypothermia 2-Oncolysis 3-Primigravida 4-Megabladder"))
    return out


def meaning_parts(a):
    return [p for p in a["parts"] if p["type"] != "vowel" and p["meaning"] and p["from"] in ("slide", "table")]


def split_shown(a):
    return a["workedOnSlide"] or a["term"] in ANALYSIS_QUOTE or a["term"].lower() in COLOUR


def an_expl(a):
    bits = [f"{p['text']} = {p['meaning']}" if (p["meaning"] and p["from"] in ("slide", "table")) else p["text"] for p in a["parts"] if p["type"] != "vowel" or True]
    return f"التقسيم زي السلايد — {a['term']}: " + " + ".join(bits) + f" → {a['medical']}. (L{a['lec']} p{a['slide']})"


def H3(a):  # full split (typed)
    if a["term"].lower() in TYPO_WORDS - {"diarrhea"}: return None
    real = [p for p in a["parts"] if p["type"] != "vowel"]
    if not split_shown(a) and any(p["from"] not in ("slide", "table") for p in real): return None
    acc = seg_variants(a["parts"]) + [x for x in SPLIT_EXTRA.get(a["term"], []) if x not in seg_variants(a["parts"])]
    evd = an_quote(a)
    if not evd: return None
    return add(a["lec"], "analyze", f"Split “{a['term']}” into its word parts as shown on the slides (write / between the parts).", acc, "hard", "analyze",
               evd, [p["text"] for p in real], an_expl(a), feat={"parts": len(real), "word": a["term"].lower()}, answerShown=acc[0])


def X1(a):  # build the term from its part meanings (typed)
    mp = meaning_parts(a)
    real = [p for p in a["parts"] if p["type"] != "vowel"]
    if a["term"].lower() in TYPO_WORDS or len(mp) < 2 or len(mp) != len(real): return None
    evd = an_quote(a)
    if not evd: return None
    return add(a["lec"], "build", f"Build the slide term: {' + '.join(p['meaning'] for p in mp)} (meaning “{a['medical']}”).",
               accept_word(a["term"]), "max", "analyze", evd, [p["text"] for p in real], an_expl(a),
               feat={"parts": len(mp), "word": a["term"].lower(), "hint": False}, answerShown=a["term"])


WORKED = [a for a in analysis if a["workedOnSlide"]]
WORKED_PARTS = [(a, p) for a in WORKED for p in a["parts"] if p["type"] != "vowel" and p["meaning"] and p["from"] == "slide"]


def E7(a, p):  # meaning of a part inside a worked slide example
    others = [(b, x) for b, x in WORKED_PARTS if b["lec"] == a["lec"] and not overlap(x["meaning"], p["meaning"]) and x["text"] != p["text"]]
    others += [(b, x) for b, x in WORKED_PARTS if b["lec"] != a["lec"] and not overlap(x["meaning"], p["meaning"]) and x["text"] != p["text"]]
    ds = []
    for b, x in others:
        if any(overlap(x["meaning"], d) for d in ds): continue
        ds.append(x["meaning"])
        if len(ds) == 3: break
    if len(ds) < 3: return None
    return mcq(a["lec"], f"In “{a['term']}” on the slide, “{p['text']}” means:", p["meaning"], ds, "easy", "recall", an_quote(a), [p["text"]],
               an_expl(a), feat={"parts": 1})


def M8(a):  # which part of this worked example carries a given meaning
    mp = [p for p in a["parts"] if p["type"] != "vowel" and p["meaning"] and p["from"] == "slide"]
    if len(mp) < 2: return None
    tgt = mp[-1] if len(a["term"]) % 2 else mp[0]
    cl = lambda t: re.sub(r"\(.*?\)", "", t)
    ds = [cl(p["text"]) for p in mp if p is not tgt and not overlap(p["meaning"], tgt["meaning"])]
    for b, x in WORKED_PARTS:
        if len(ds) >= 3: break
        if cl(x["text"]) not in ds and cl(x["text"]) != cl(tgt["text"]) and not overlap(x["meaning"], tgt["meaning"]): ds.append(cl(x["text"]))
    if len(ds) < 3: return None
    return mcq(a["lec"], f"In “{a['term']}”, which part means “{tgt['meaning']}”?", cl(tgt["text"]), ds[:3], "medium", "reverse", an_quote(a),
               [tgt["text"]], an_expl(a), feat={"reverse": True, "parts": len(mp)})


# ---------------- combining-vowel rules ----------------
RULE_TEXT = {r["id"]: r["rule"] for r in rules}
# (term, parts, rule id) — slide rule examples + slide words whose colour split shows the seam
RULE_EX = [("Electrocardiogram", ["electr", "cardi", "gram"], "1"), ("Vasectomy", ["vas", "ectomy"], "2"), ("Carditis", ["cardi", "itis"], "3"),
           ("Parenteral", ["para", "enter", "al"], "4"), ("Cardioesophageal", ["cardi", "esophag", "eal"], "4b"),
           ("Hepatomegaly", ["hepat", "megaly"], "1"), ("Cephalodynia", ["cephal", "dynia"], "1"), ("Cystocele", ["cyst", "cele"], "1"),
           ("Gastralgia", ["gastr", "algia"], "2"), ("Colitis", ["col", "itis"], "2"), ("Lipoma", ["lip", "oma"], "2"),
           ("Uteropexy", ["uter", "pexy"], "1"), ("Laparotomy", ["lapar", "tomy"], "1"), ("Lithotripsy", ["lith", "tripsy"], "1"),
           ("Tonsillectomy", ["tonsill", "ectomy"], "2"), ("Bronchiole", ["bronchi", "ole"], "2"), ("Sonogram", ["son", "gram"], "1"),
           ("Optometry", ["opt", "metry"], "1"), ("Mucoid", ["muc", "oid"], "2")]


def rule_evidence(term, rid):
    e = [ev(2, RULE_PAGE[rid], RULE_QUOTE[rid])]
    if term not in ANALYSIS_QUOTE:
        c = COLOUR.get(term.lower())
        if c: e.append(ev(c[0], c[1], f"{c[2]} (colour split on the slide)"))
    return e


def term_lec(term):
    a = next((x for x in analysis if x["term"] == term), None)
    return a["lec"] if a else 2


def M5(term, parts, rid):  # which rule applies
    others = [k for k in RULE_TEXT if k != rid]
    rng.shuffle(others)
    return mcq(term_lec(term), f"Which combining-vowel rule explains {' + '.join(parts)} → {term}?", RULE_TEXT[rid], [RULE_TEXT[k] for k in others[:3]],
               "medium", "apply-rule", rule_evidence(term, rid), [term] + parts, f"{term}: القاعدة {rid} — {RULE_TEXT[rid]}",
               feat={"exception": rid in ("3", "4", "4b"), "parts": len(parts)})


def wrong_joins(term, parts, rid):
    t = term.lower()
    a, b = parts[0], parts[-1]
    if rid == "1":
        c = ["".join(parts[:-1]).replace("cardi", "cardi") + b, t.replace(a + "o", a + "i", 1), t.replace(a + "o", a + "oo", 1)]
        c = [t.replace(a + "o", a, 1), t.replace(a + "o", a + "i", 1), t.replace(a + "o", a + "e", 1)]
    elif rid == "2":
        c = [a + "o" + b, a + "i" + b, a[:-1] + b if a[-1] == a[-2] else a + "o" + b[1:]]
    elif rid == "3":
        c = ["cardiitis", "cardioitis", "cardtis"]
    elif rid == "4":
        c = ["paraenteral", "paroenteral", "parentral"]
    else:
        c = ["cardiesophageal", "cardesophageal", "cardiesophagoeal"]
    return [x for x in dict.fromkeys(c) if x != t and not grounded_word(x)][:3]


def H4(term, parts, rid):  # apply the rule: join the parts
    w = wrong_joins(term, parts, rid)
    if len(w) < 3: return None
    return mcq(term_lec(term), f"Join the parts using the slide rules: {' + '.join(parts)} = ?", term.lower(), w, "hard", "apply-rule",
               rule_evidence(term, rid), [term] + parts, f"{term.lower()} — القاعدة {rid}: {RULE_TEXT[rid]}",
               feat={"exception": rid in ("3", "4", "4b"), "parts": len(parts), "word": term.lower()}, misspellings=w)


# ---------------- plurals ----------------
PL_ENDINGS = ["ae", "i", "es", "a", "ina", "ices"]
REGULAR = {"vertebra", "diagnosis", "ovum", "fungus"}


def pl_wrong(p):
    out = [x for x in PL_WRONG[p["singular"]] if not grounded_word(x)]
    rng.shuffle(out)
    return out[:3]


def pl_ev(p):
    pg, qt = PLURAL_QUOTE[p["singular"]]
    return [ev(2, pg, qt)]


def PL(p):
    reg = p["singular"] in REGULAR
    w = pl_wrong(p)
    ex = f"الجمع حسب السلايد: {p['ending']} → {p['pluralEnding']}، {p['singular']} → {p['plural']}. (L2 p{PLURAL_QUOTE[p['singular']][0]})"
    tests = ["pl:" + p["singular"]]
    mcq(2, f"According to the slides (Latin plural), the plural of “{p['singular']}” is:", p["plural"], w, "easy" if reg else "hard",
        "recall" if reg else "spell", pl_ev(p), tests, ex, feat={"exception": not reg, "word": p["plural"]}, misspellings=w)
    add(2, "spell", f"According to the slides (Latin plural), write the plural of “{p['singular']}” ({p['meaning']}).", [p["plural"]],
        "medium" if reg else "hard", "spell", pl_ev(p), tests, ex, feat={"exception": not reg, "word": p["plural"], "hint": False}, answerShown=p["plural"])


def X4(k):
    good = [p for p in plurals]
    rng.shuffle(good)
    bad = good[0]
    wrong = pl_wrong(bad)[0]
    lines = [f"{bad['singular']} → {wrong}"] + [f"{p['singular']} → {p['plural']}" for p in good[1:4]]
    return mcq(2, "According to the slides (Latin plurals), which singular → plural pair is WRONG?", lines[0], lines[1:], "max", "error-find",
               pl_ev(bad), ["pl:" + bad["singular"]], f"الصح: {bad['singular']} → {bad['plural']} ({bad['ending']} → {bad['pluralEnding']}).",
               feat={"exception": True}, wrongLine=wrong)


# ---------------- pronunciation ----------------
SOUNDS = sorted({p["sound"] for p in pronunciation})


def pr_ev(p):
    return [ev(2, int(p["slide"]), f"{p['letters']} | {p['sound']} | {', '.join(p['examples'])}")]


def E5(p):
    ds = [s for s in SOUNDS if s != p["sound"]]
    rng.shuffle(ds)
    return mcq(2, f"On the pronunciation slide, “{p['letters']}” at the start of a word is pronounced like:", p["sound"], ds[:3], "easy", "recall",
               pr_ev(p), ["pron:" + p["letters"]], f"النطق: {p['letters']} بتتنطق {p['sound']} ({', '.join(p['examples'])}). (L2 p{p['slide']})")


def M9(p):
    others = [x for x in pronunciation if x["sound"] != p["sound"]]
    rng.shuffle(others)
    ds = []
    for x in others:
        if x["examples"][0] not in ds: ds.append(x["examples"][0])
        if len(ds) == 3: break
    return mcq(2, f"Which slide example begins with letters pronounced like “{p['sound']}”?", p["examples"][0], ds, "medium", "reverse",
               pr_ev(p), ["pron:" + p["letters"]], f"النطق: {p['examples'][0]} — {p['letters']} بتتنطق {p['sound']}. (L2 p{p['slide']})", feat={"reverse": True})


# ---------------- max: synonym pairs and odd-one-out ----------------
SYN_PAIRS = {3: [("mon/o", "uni"), ("di", "bi"), ("levo", "sinistro/o"), ("dia", "per"), ("per", "trans"), ("macro", "mega"), ("xanth/o", "icter/")],
             4: [("-algia", "-dynia"), ("un-", "a-"), ("in-", "un-"), ("pre-", "pro-"), ("-iatrics", "-iatry"), ("-ist", "-iatrist")],
             5: [("-cle", "-ole"), ("-ula", "-ule"), ("-ac", "-ic"), ("-al", "-ous"), ("-form", "-oid")]}
NONSYN = {3: [("py/o", "pyr/o"), ("ecto", "endo"), ("ab", "ad"), ("dextro", "levo"), ("macro", "micro"), ("prim/i", "mon/o")],
          4: [("hyper-", "hypo-"), ("ante-", "post-"), ("brady-", "tachy-"), ("-iatry", "-iatrist")],
          5: [("-tome", "-tomy"), ("-scope", "-scopy"), ("-graph", "-gram"), ("-meter", "-metry"), ("-ectomy", "-stomy")]}


def X5(lec, k):
    ns = NONSYN[lec][k % len(NONSYN[lec])]
    sp = SYN_PAIRS[lec][:]
    rng.shuffle(sp)
    pairs = sp[:3]
    rows = [find_row(x) for pr in pairs + [ns] for x in pr]
    for pr in pairs: assert find_row(pr[0])["meaning"].lower() == find_row(pr[1])["meaning"].lower(), pr
    f = lambda pr: f"{pr[0]} – {pr[1]}"
    a, b = find_row(ns[0]), find_row(ns[1])
    return mcq(lec, "According to the slides, which pair is NOT synonymous?", f(ns), [f(p) for p in pairs], "max", "discriminate",
               [rev(a), rev(b)], [ns[0], ns[1]], f"{a['part']} = {a['meaning']} لكن {b['part']} = {b['meaning']}. باقي الأزواج نفس المعنى.",
               feat={"close": 2})


ODD = [("cond", "condition of"), ("small", "small"), ("adj", "pertaining to"), ("spec", "specialist in a field of study"),
       ("neg", "not"), ("dir", "through")]


def X6(sid, meaning, k):
    members = [r for r in ROWS if r["sid"] == sid and r["meaning"].lower() == meaning]
    if len(members) < 3: return None
    rng.shuffle(members)
    lec = members[0]["lec"]
    outs = [r for r in ROWS if r["lec"] == lec and r["kind"] == members[0]["kind"] and not overlap(r["meaning"], meaning)
            and not any(near(r["part"], m["part"]) for m in members)]
    rng.shuffle(outs)
    o = outs[k % len(outs)]
    kind = members[0]["kind"]
    return mcq(lec, f"Which {kind} does NOT mean “{meaning}”?", o["part"], [m["part"] for m in members[:3]], "max", "discriminate",
               [rev(members[0]), rev(o)], [o["part"]] + [m["part"] for m in members[:3]],
               f"{o['part']} = {o['meaning']}؛ الباقي = {meaning}. (L{lec})", feat={"close": 1})


def X3(lec, k):  # find the error in an analysis
    pool = [(a, p) for a in analysis if a["lec"] == lec for p in meaning_parts(a)]
    if len(pool) < 6: return None
    rng.shuffle(pool)
    lines, used = [], set()
    for a, p in pool:
        if a["term"] in used or p["text"] in used: continue
        used.add(a["term"]); used.add(p["text"]); lines.append((a, p))
        if len(lines) == 4: break
    if len(lines) < 4: return None
    ba, bp = lines[0]
    wrongs = [p2["meaning"] for a2, p2 in pool if not overlap(p2["meaning"], bp["meaning"]) and p2["type"] == bp["type"]]
    if not wrongs: return None
    wm = wrongs[k % len(wrongs)]
    txt = lambda a, p, m: f"{a['term']}: {p['text']} = {m}"
    bad = txt(ba, bp, wm)
    return mcq(lec, "Which line of word analysis is WRONG according to the slides?", bad, [txt(a, p, p["meaning"]) for a, p in lines[1:]], "max", "error-find",
               an_quote(ba), [bp["text"]], f"الصح: {ba['term']}: {bp['text']} = {bp['meaning']}. (L{ba['lec']} p{ba['slide']})", feat={"parts": 2})


# ---------------- concept questions (slide_data.CONCEPT_Q) ----------------
def CQ(c):
    evd = [ev(c["lec"], c["p"], c["quote"])]
    if c["type"] == "tf":
        return add(c["lec"], "tf", c["q"], c["a"], c["level"], c["skill"], evd, c["tests"], c["ar"], correction=c.get("fix"))
    return mcq(c["lec"], c["q"], c["o"][0], c["o"][1:], c["level"], c["skill"], evd, c["tests"], c["ar"],
               feat={"reverse": c["skill"] == "reverse", "close": 1})


# =====================================================================================
# generate: Stage 3b exam-grade bank (tools/bank.py — pattern library P1–P14, documented score weights)
# =====================================================================================
import bank
Q = bank.build(sys.modules[__name__])

content = {"meta": meta, "concepts": concepts, "rules_intro": rules_intro, "rules": rules, "pronunciation": pronunciation,
           "plurals": plurals, "sections": sections, "analysis": analysis, "lookalikes": lookalikes,
           "spellingTraps": spellingTraps, "questions": Q,
           "bank": {"levels": bank.LEVELS, "band": bank.FLOOR, "seed": SEED, "scoreDoc": bank.__doc__.split("Score 1–100", 1)[1].strip(),
                    "mix": {"easy": 20, "medium": 35, "hard": 30, "max": 15},
                    "lectureWeights": {"1": 8, "2": 12, "3": 40, "4": 22, "5": 18}}}
if __name__ == "__main__" or True:
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(content, fh, ensure_ascii=False, indent=1)
    if __name__ == "__main__":
        print("written", os.path.normpath(OUT), "questions:", len(Q))
