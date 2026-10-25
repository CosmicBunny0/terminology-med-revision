"""Slide data transcribed from the rasterized pages (see content/slide-transcription.md).
"p" numbers are PDF page numbers. Imported by build_content.py."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "content.json")

META = {
    "title": "Medical Terminology L1–L5 Study Pack",
    "course": "Medical Terminology (ENG 101) · PharmD Clinical Pharmacy · October 6 University",
    "credit": "Prepared by Mohammed Aymen · PharmD Clinical 3 · Fall 2026",
    "disclaimer": "Unofficial student summary — the doctors' slides are the reference.",
    "sources": [
        {"lec": 1, "file": "Lecture (1) Terminology (Clinical) - 2027.pdf", "by": "Dr. Shaimaa Gomaa Ibrahim", "pages": 21},
        {"lec": 2, "file": "Lecture (2) Terminology (Clinical) - 2027-students.pdf", "by": "Dr. Shaimaa Gomaa Ibrahim", "pages": 25},
        {"lec": 3, "file": "Lecture (3) Terminology-2027-students.pdf", "by": "Dr. Shaimaa Gomaa Ibrahim", "pages": 42},
        {"lec": 4, "file": "4-Medical Terminology - Clinical - Fall 26-27.pdf", "by": "Made by Assoc. Prof. Amira Ahmed · edited by Dr. Hagar Belal Ahmad", "pages": 16},
        {"lec": 5, "file": "Lecture 5-Medical Terminology - Clinical - Fall 26-27.pdf", "by": "Made by Assoc. Prof. Dr. Amira A. Alqazar · edited by Dr. Hagar Belal Ahmad", "pages": 9},
        {"lec": 0, "file": "Medical terminology Training Sheet.pdf", "by": "Dr. Hagar Belal Ahmad Abo-Zalam", "pages": 1},
    ],
    "exam": {
        "name": "Term Work Exam", "date": "2026-10-25", "day": "Sunday",
        "covers": "Lecture 1 → Lecture 5", "place": "Analytical Pharmaceutical Chemistry Lab 1 (according to group distribution)",
        "src": "L5 p9",
        "grading": {"class_activity_periodicals": 25, "midterm_quiz": 20, "research": 5, "final_written": 75,
                    "practical": "(-)", "attendance_behavior_bonus": "2 to 3", "src": "L1 p8"},
    },
    "colors": {"prefix": "blue", "root": "green", "suffix": "pink", "vowel": "amber",
               "src": "L4 p2 (Color Code for Medical Terminology); combining vowel = amber is our addition"},
    "lectures": [
        {"lec": 1, "title": "Introduction: definition, word parts, structural analysis"},
        {"lec": 2, "title": "Medical term components: combining vowels, rules, pronunciation, plurals"},
        {"lec": 3, "title": "Roots (physical, time, chemistry, diseases) + prefixes (numbers, size, color, direction, position)"},
        {"lec": 4, "title": "Prefixes (time/position, disease, degree, negative) + suffixes (specialties, condition, disease)"},
        {"lec": 5, "title": "Suffixes (recording/instruments, small, surgery, adjective)"},
    ],
}

# ---------- CONCEPTS (definitions & facts stated on slides) ----------
CONCEPTS = [
    {"id": "def", "lec": 1, "src": "L1 p9", "title": "Medical terminology — definition",
     "points": ["It is the language used to precisely describe the human body including its components, processes, conditions affecting it, and procedures performed upon it.",
                "Medical terminology is used in the field of medicine and pharmacy."],
     "ar": "لغة بتوصف جسم الإنسان بدقة: مكوناته، العمليات اللي بتحصل فيه، الحالات اللي بتأثر عليه، والإجراءات اللي بتتعمل عليه."},
    {"id": "origin", "lec": 1, "src": "L1 p10", "title": "Word parts & origin",
     "points": ["Most medical terms are a combination of word parts: prefix, root (stem), suffix.",
                "Most of them come from Latin or Greek words.",
                "Other languages such as English, German and French."],
     "ar": "معظم الكلمات Latin أو Greek."},
    {"id": "parts", "lec": 1, "src": "L1 p11–12", "title": "The word parts",
     "points": ["Root: the word part that is the core of the word.",
                "Prefix: a word part attached to the beginning of a word root to modify its meaning.",
                "Suffix: a word part attached to the end of the word root to modify its meaning.",
                "Combining vowel: a word part, usually an “o” or “i”."],
     "ar": "الـ Root هو قلب الكلمة. الـ prefix في الأول والـ suffix في الآخر، والاتنين بيعدّلوا المعنى."},
    {"id": "analysis", "lec": 1, "src": "L1 p13, p16–20", "title": "Defining medical terms through word structural analysis",
     "points": ["You can define a term according to word structure analysis by: prefix, root, suffix.",
                "Patterns on the slides: Root + suffix (lipemia) · Prefix + root + suffix (hyperlipemia) · Root + combining vowel + suffix (carcinogen)."],
     "ar": "عشان تعرّف أي term: قسّمه prefix / root / suffix وهات معنى كل جزء."},
    {"id": "cv", "lec": 2, "src": "L2 p4–8", "title": "Combining vowels",
     "points": ["[o] is the most common combining vowel; [i] is the second most common.",
                "When a medical term has more than one root, each is joined by a vowel.",
                "They are used to join: (i) root to root, (ii) root to suffix.",
                "Why? To ease pronunciation.",
                "Is their presence mandatory? No — not all medical terms have combining vowels.",
                "Additional roots: often a medical term is formed of two or more roots (hyper/lip/o/protein/emia)."],
     "ar": "o الأشهر وبعدها i. بتربط root بـ root أو root بـ suffix، ومش إجبارية."},
    {"id": "formation", "lec": 2, "src": "L2 p17", "title": "Formation of medical terms",
     "points": ["All medical terms build from the root.",
                "Prefixes and suffixes are attached to the root to modify its meaning.",
                "Often two or more roots are linked before being modified."]},
    {"id": "color", "lec": 4, "src": "L4 p2", "title": "Color code for medical terminology",
     "points": ["Prefix- (blue): meaning before the root · modifies the meaning · e.g. hyper-, hypo-, anti-, pre-",
                "-Root- (green): main meaning of the term · usually indicates the organ, system or action · e.g. cardi-, nephro-, hepat-, gastr-",
                "-Suffix (pink): meaning after the root · indicates condition, procedure, disease, drug class, etc. · e.g. -itis, -emia, -ology, -logy, -ase"]},
    {"id": "prefcat", "lec": 4, "src": "L4 p3", "title": "Prefix categories (L4)",
     "points": ["Time and position", "Disease", "Degree", "Negative prefix"]},
    {"id": "suffix", "lec": 4, "src": "L4 p9 · L5 p2", "title": "Suffixes",
     "points": ["Suffixes are the ending part of medical terms.",
                "Suffixes tend to bring an action to the medical terms.",
                "Medical suffixes can be categorized into: specialties, condition of, disease, small, surgery, adjective suffix."],
     "ar": "الـ suffix آخر الكلمة وبيدّيها action."},
    {"id": "disease", "lec": 4, "src": "L4 p12", "title": "Disease — definition",
     "points": ["A condition of a person, animal, or plant in which its body or structure is harmed because an organ or part is unable to work as it usually does."]},
    {"id": "adj", "lec": 5, "src": "L5 p7", "title": "Adjective suffix — definition",
     "points": ["A suffix added to a root word to form an adjective."]},
    {"id": "competency", "lec": 1, "src": "L1 p6–7", "title": "Competency (intro slide)",
     "points": ["It is a set of characteristics including knowledge, skills and attitude. All are integrated within a situation which takes place in a setting.",
                "Consists of a description of the essential skills, knowledge, attitudes, and behaviors required for effective performance of a real-world task or activity (Mrowicki, 1986).",
                "الجدارات = Knowledge + Skills + Behaviors + Attitudes · الكفاءات = القدرة على توظيف هذه العناصر في الأداء الفعلي"],
     "low_priority": True},
]

RULES = [
    {"n": 1, "src": "L2 p10", "rule": "A combining vowel is used to join root to root as well as to any suffix beginning with a consonant.",
     "ex": "electr/o/cardi/o/gram — electrical record of the heart",
     "ar": "o بين root وroot، وقبل أي suffix بيبدأ بـ consonant."},
    {"n": 2, "src": "L2 p12–13", "rule": "A combining vowel is not used before a suffix that begins with a vowel.",
     "ex": "vas + ectomy → vasectomy — excision of a vessel",
     "ar": "الـ suffix بيبدأ بـ vowel؟ يبقى مفيش o."},
    {"n": 3, "src": "L2 p14", "rule": "If the root ends in a vowel and the suffix begins with the same vowel, drop the final vowel from the root and do not use a combining vowel.",
     "ex": "cardi + itis → carditis — inflammation of heart",
     "ar": "نفس الحرف مرتين؟ شيل حرف الـ root."},
    {"n": 4, "src": "L2 p15", "rule": "When a prefix ends in a vowel and the root begins with a vowel, the final vowel is dropped from the prefix.",
     "ex": "para + enter + al → parenteral — pertaining to alongside of the intestine",
     "ar": "هنا اللي بيتشال حرف الـ prefix مش الـ root."},
    {"n": 5, "src": "L2 p16", "rule": "Most often a combining vowel is inserted between two roots even when the second root begins with a vowel.",
     "ex": "cardi/o/esophag/eal — pertaining to heart and esophagus",
     "note": "The slide numbers this rule “4” again (two slides are labelled 4); here it is listed as rule 4b.",
     "ar": "بين two roots حط o حتى لو التاني بيبدأ بـ vowel."},
]
RULES_INTRO = {"src": "L2 p9", "points": [
    "Memorizing and spelling basic medical word components are the first steps for learning how to form medical terms.",
    "The next step is to construct the words using the following steps (rules)."]}

PRON = {"src": "L2 p17–19", "title": "Silent letters at the start of a word and unusual pronunciation", "rows": [
    ["Ch", "k", "chemical"], ["C (before a, o, u)", "k", "cavity, colon, cure"], ["C (before e, i)", "s", "cephalic, cirrhosis"],
    ["Dys", "dis", "dystrophy"], ["Eu", "u", "euphoria"], ["Gn", "n", "gnathic"], ["Ph", "f", "pharmacy"],
    ["Pn", "n", "pneumonia"], ["Ps", "s", "pseudo"], ["Pt", "t", "ptosis"], ["Rh", "r", "rheumatic"], ["X", "z", "xenon"]]}

PLURALS = {"src": "L2 p20–23", "title": "Singular and plural forms",
           "note": "Slide header says “Pleural” — the correct word is Plural (pleural = of the pleura).",
           "rows": [
    # word ending, plural ending, singular, meaning, plural, wrong options (quiz distractors, not from slides)
    ["a", "ae", "vertebra", "bone of the spine", "vertebrae", ["vertebres", "vertebri", "vertebrina"]],
    ["en", "ina", "lumen", "central opening", "lumina", ["lumena", "lumices", "lumenae"]],
    ["ex, ix", "ices", "index", "indicator", "indices", ["indexa", "indici", "indicea"]],
    ["is", "es", "diagnosis", "identification of diseases", "diagnoses", ["diagnosises", "diagnosa", "diagnosae"]],
    ["nx (anx, inx, ynx)", "nges", "phalanx", "bone of finger or toe", "phalanges", ["phalanxi", "phalanxa", "phalanices"]],
    ["on", "a", "ganglion", "mass of nerve tissue", "ganglia", ["ganglii", "ganglies", "ganglionae"]],
    ["um", "a", "ovum", "egg", "ova", ["ovi", "ovae", "ovums"]],
    ["us", "i", "fungus", "mold", "fungi", ["funga", "fungae", "fungices"]]]}


def S(id, lec, src, kind, title, rows, note=None, subtitle=None):
    out = []
    for r in rows:
        d = {"part": r[0], "meaning": r[1], "example": r[2], "definition": r[3]}
        if len(r) > 4 and r[4]:
            d["note"] = r[4]
        out.append(d)
    s = {"id": id, "lec": lec, "src": src, "kind": kind, "title": title, "rows": out}
    if note: s["note"] = note
    if subtitle: s["subtitle"] = subtitle
    return s


SECTIONS = [
    # ---------- L3 ROOTS ----------
    S("phys", 3, "L3 p4–9", "root", "Roots pertaining to physical factors", [
        ["aer/o", "air, gas", "aerobe", "Organism that requires air (oxygen) to live"],
        ["bar/o", "pressure", "barotrauma", "Injury (trauma) caused by pressure"],
        ["chrom/o, chromat/o", "color, stain", "chromatic", "Pertaining to color"],
        ["cry/o", "cold", "cryoprobe", "Instrument used to apply extreme cold to tissues", "The picture version (p4) adds: apply extreme cold (freeze) to tissues, e.g. to destroy & remove prostate."],
        ["electr/o", "electricity", "electroshock", "Shock produced by electricity"],
        ["kine, kinesi/o, kinet/o", "movement", "kinesis", "Movement"],
        ["phot/o", "light", "photosensitive", "Abnormally sensitive to light"],
        ["radio", "radiation (X-ray)", "radioactive", "Giving off radiation"],
        ["son/o", "sound", "ultrasound", "Pertaining to high frequency sound waves (beyond human hearing)"],
        ["therm/o", "heat, temperature", "hypothermia", "Low body temperature"]]),
    S("time", 3, "L3 p11", "root", "Roots pertaining to time", [
        ["chron/o", "time", "synchronous", "Occurring together"],
        ["noct/i", "night", "nocturnal", "Occurring at night"],
        ["nyct/o", "night, darkness", "nyctophobia", "Fear of night or darkness"]]),
    S("chem", 3, "L3 p13–16", "root", "Roots pertaining to chemistry", [
        ["adip/o", "fat", "adiposis", "Accumulation of fat in the body (the process)"],
        ["amyl/o", "starch", "amyloid · amylase", "Resembling (like) starch · Enzyme breaks down starch into sugar"],
        ["azot/o", "nitrogen compound", "azoturia", "Increased nitrogen compounds in urine"],
        ["ferr/i, ferr/o", "iron", "ferric · ferrous", "Ferric: containing iron in oxidized form · Ferrous: containing iron in reduced"],
        ["glyc/o", "sugar, glucose", "hypoglycemia", "Low blood glucose"],
        ["kal/", "potassium", "hyperkalemia", "Excess potassium in the blood"],
        ["lip/o", "lipid", "liposuction", "Surgical removal of fat by suction"],
        ["hydr/o", "water, fluid", "dehydrate", "To lose water"],
        ["natr/i", "sodium", "hyponatremia", "Decrease of sodium in the blood"],
        ["prote/o", "protein", "proteolysis", "Dissolving of protein in blood"],
        ["steat/o", "fatty", "steatorrhea", "Fatty diarrhea"]]),
    S("easy", 3, "L3 p17", "root", "Easily recognized roots", [
        ["oxy", "oxygen", "", ""],
        ["calci", "calcium", "", ""]]),
    S("dis", 3, "L3 p19–20", "root", "Roots pertaining to diseases", [
        ["carcin/o", "cancer", "carcinogen", "Substance that produces cancer"],
        ["lith", "stone", "lithiasis", "Stone formation"],
        ["onc/o", "tumor", "oncolysis", "Destruction (lysis) of a tumor"],
        ["path/o", "disease", "pathogenic", "Producing disease"],
        ["py/o", "pus", "pyorrhea", "Discharge (rhea) of pus"],
        ["pyr/o", "fever, fire", "pyretic", "Pertaining to fever"],
        ["scler/o", "hard", "sclerosis", "Hardening of tissue"],
        ["tox/o", "poison, toxin", "toxic", "Poisonous, damaging"]]),
    # ---------- L3 PREFIXES ----------
    S("num", 3, "L3 p24–30", "prefix", "Prefixes pertaining to numbers", [
        ["prim/i", "first", "primigravida", "Woman pregnant (gravid) for the first time"],
        ["mon/o", "one", "monoclonal", "A cell colony (clone) arising from a single cell"],
        ["uni", "one", "unicellular", "Organism composed of a single cell"],
        ["di", "two, twice", "diplegia", "Double paralysis"],
        ["diplo", "double", "diplopia", "Double vision"],
        ["bi", "two, twice", "bicuspid", "Having or ending in two points (cuspus)", "Picture on slide: bicuspid aortic valve vs normal tricuspid valve."],
        ["hemi", "half, one side", "hemithorax", "One side of the chest (thorax)", "Slide writes “Hemi thorax” (both spellings accepted)."],
        ["semi", "half, partial", "semilunar", "Resembling a half moon"],
        ["tri", "three", "triad", "Group of three"],
        ["quadr/i", "four", "quadrant", "One fourth of an area"],
        ["penta", "five", "pentanoic", "An acid with 5 carbons"],
        ["multi", "many", "multiple", "Consisting of many parts"],
        ["poly", "many, much", "polymorphic", "Having many shapes (morph/o)"]]),
    S("numchart", 3, "L3 p23", "prefix", "Number prefixes in medical & pharmaceutical terms (chart)", [
        ["mono-", "one", "monotherapy", "Monotherapy · Monoclonal antibody · Monosaccharide"],
        ["di-", "two", "dicarboxylic acid", "Dicarboxylic acid · Dibasic · Diphenhydramine"],
        ["tri-", "three", "tricyclic antidepressant", "Tricyclic antidepressant · Triiodothyronine (T3) · Triglyceride"],
        ["tetra-", "four", "tetracycline", "Tetracycline · Tetramethyl · Tetrahydrate"],
        ["penta-", "five", "pentamidine", "Pentamidine · Pentose · Pentapeptide"],
        ["hexa-", "six", "hexachlorophene", "Hexachlorophene · Hexose · Hexamethonium"],
        ["hepta-", "seven", "heptavalent", "Heptavalent · Heptanoic acid · Heptahydrate"],
        ["octa-", "eight", "octanol", "Octanol · Octapeptide · Octahydrate"],
        ["nona-", "nine", "nonavalent", "Nonavalent · Nonapeptide · Nonanoic acid"],
        ["deca-", "ten", "decamethonium", "Decamethonium · Decanoic acid · Decapeptide"]],
      note="Chart slide: it lists examples only, no definitions."),
    S("size", 3, "L3 p32–35", "prefix", "Prefixes pertaining to size and comparison", [
        ["eu", "true, good, easy, normal", "euthanasia", "Easy or painless death"],
        ["hetero", "other, different, unequal", "heterosexual", "Pertaining to the opposite sex"],
        ["homo, homeo", "same, unchanging", "homothermic", "Maintaining the body temp"],
        ["iso", "same, equal", "isograft", "Graft between two genetically identical individuals"],
        ["macro", "large, abnormally large", "macroscopic", "Visible with the naked eye (without a microscope)"],
        ["mega, megalo", "large, abnormally large", "megabladder", "Permanent enlargement of the bladder"],
        ["micro", "small", "microsurgery", "Surgery of extremely small structures under the microscope"],
        ["neo", "new", "neonate", "Newborn infant; Infant in the first 28 days after birth"],
        ["normo", "normal", "normovolemia", "Normal blood volume"],
        ["ortho", "straight, upright", "orthosis", "Appliance/device used to correct or prevent deformities"],
        ["pseudo", "false", "pseudoparalysis · pseudocyesis", "False paralysis · False pregnancy"],
        ["re", "again, back", "reflux", "Backward or return flow (reflux esophagitis)"]]),
    S("color", 3, "L3 p36–37", "prefix", "Prefixes pertaining to color", [
        ["cyan/o", "blue", "cyanosis", "Bluish discoloration of the skin due to lack of oxygen"],
        ["erythr/o", "red", "erythrocyte", "Red blood cell"],
        ["leuk/o", "white, colorless", "leukoplakia", "White patches in the mouth"],
        ["melan/o", "black, dark", "melanin", "The dark pigment that colors the hair and skin"],
        ["xanth/o", "yellow", "xanthoma", "Yellow raised area on the skin"],
        ["icter/", "yellow", "icterus index", "Index denoting blood concentration of bilirubin"],
        ["polio, glauc/o", "grey", "polioencephalitis", "Inflammation of the gray matter of the brain", "Slide writes “Polioencephalities” (both spellings accepted)."],
        ["verd/o", "green", "verdoglobin", "Any of several green compounds derived from hemoglobin or related compounds"]]),
    S("dir", 3, "L3 p38–39, p41", "prefix", "Prefixes pertaining to direction", [
        ["ab", "away from", "abduct", "To move away from the midline"],
        ["ad", "toward, near", "adhesion", "An attachment of parts"],
        ["dia", "through", "dialysis", "Separation (-lysis) by passage through a membrane"],
        ["per", "through", "percutaneous", "Through the skin"],
        ["trans", "through", "transfusion", "Introduction of blood or blood components into blood stream"],
        ["ex/o", "away from, outside", "excise", "To cut out"],
        ["endo", "in, within", "endoscope", "Device for viewing the inside of a cavity or organ"]]),
    S("pos", 3, "L3 p40", "prefix", "Prefixes pertaining to position", [
        ["dextro", "right", "dextrocardia", "(Rare condition) Location of the heart in the right side of the chest"],
        ["levo", "left", "levorotation", "Rotation towards the left"],
        ["sinistro/o", "left", "sinistrad", "Towards the left", "Written “Sinistro/o” on the slide."],
        ["ecto", "out, outside", "ectopic", "Outside the normal position (ectopic pregnancy: outside the uterus)"]]),
    # ---------- L4 PREFIXES ----------
    S("tpos", 4, "L4 p4", "prefix", "Prefixes pertaining to time and/or position", [
        ["ante-", "before", "antenatal", "Before birth"],
        ["pre-", "before, in front of", "predisposing", "Leading to a condition such as a disease (predisposing factors)"],
        ["pro-", "before, in front of", "prophylaxis", "Prevention of disease"],
        ["post-", "after, behind", "postoperative", "After a surgical operation"]]),
    S("pdis", 4, "L4 p5", "prefix", "Prefixes pertaining to disease", [
        ["brady-", "slow", "bradycardia", "Slow heart rate"],
        ["tachy-", "rapid", "tachypnea", "Rapid breathing"],
        ["dys-", "abnormal, painful, difficult", "dysfunction", "Abnormal function"],
        ["mal-", "bad", "malnutrition", "Poor nutrition"],
        ["pachy-", "thick", "pachyderma", "Thickness of the skin"],
        ["xero-", "dry", "xerosis", "Dryness of the skin or membranes"]]),
    S("deg", 4, "L4 p6", "prefix", "Prefixes pertaining to degree", [
        ["hyper-", "over, excess, abnormally high, high, increased", "hypertension", "High blood pressure"],
        ["hypo-", "under - below, abnormally low, decreased", "hypoventilation", "Lower amount of air entering lungs"],
        ["olig/o", "few or deficiency of", "oligospermia · oliguria", "Low number of sperm in the semen · Low urine output", "Slide spells it “Oligouria” (both spellings accepted)."],
        ["pan-", "all", "panplegia", "Total paralysis"],
        ["super-", "above or excess", "superinfection", "Second infection"]]),
    S("neg", 4, "L4 p7", "prefix", "Negative prefixes", [
        ["dis-", "down, removal, separation", "disinfectant", "To remove infectious organisms"],
        ["in-, im-", "not", "incontinence · imbalance", "Lack of control over excretion • Not moving · Not being in balance"],
        ["un-", "not", "unconscious", "Not responsive or aware or awake"],
        ["a-, an-", "not", "analgesia", "Pain killer"]]),
    S("anti", 4, "L4 p8", "prefix", "Anti-", [
        ["anti-", "against", "anti-hypertensive drugs", "Examples on slide: anti-hypertensive drugs (Concor 5 mg) · anti-protozoal drugs (Flagyl 500 mg) · anti-viral drugs (Acyclovir 5%) · antibiotics (Augmentin 1 g)",
         "The slide gives no written meaning for anti- (the meaning “against” is extra and never tested)."]],
      note="Separate picture slide after the negative-prefix table."),
    # ---------- L4 SUFFIXES ----------
    S("spec", 4, "L4 p10", "suffix", "Suffixes pertaining to specialties", [
        ["-logy", "study of", "physiology", "Study of function in a living organism", "Indicates a FIELD of study"],
        ["-iatrics", "field of medicine", "pediatrics", "Study of treatment of children diseases", "Indicates a FIELD of study"],
        ["-iatry", "field of medicine", "psychiatry", "Study of treatment of mental illness", "Indicates a FIELD of study"],
        ["-ist", "specialist in a field of study", "dentist", "Specialist in study and treatment of the teeth and mouth", "Indicates a PERSON (specialist)"],
        ["-ian, -ician", "specialist in a field of study", "physician", "Practitioner of medicines", "Indicates a PERSON (specialist)"],
        ["-iatrist", "specialist in a field of study", "podiatrist", "Specialist in study and treatment of the foot", "Indicates a PERSON (specialist)"]]),
    S("cond", 4, "L4 p11", "suffix", "Suffixes that mean “condition of”", [
        ["-ia", "condition of", "insomnia", "Inability to sleep"],
        ["-iasis", "condition of", "amebiasis", "Infection with ameba (parasites)"],
        ["-ism", "condition of", "alcoholism", "Chronic dependence or addiction to alcohol"],
        ["-osis", "condition of", "neurosis", "Abnormal condition of the neurons"],
        ["-y", "condition of", "atony", "Lack of muscle tone"]]),
    S("sdis", 4, "L4 p13–14", "suffix", "Suffixes pertaining to disease", [
        ["-algia", "pain", "gastralgia", "Pain in the stomach"],
        ["-dynia, -dysnia", "pain", "cephalodynia", "Pain in the head (headache)", "The slide lists both “-Dysnia” and “-Dynia”; its example, cephalodynia, uses -dynia."],
        ["-cele", "hernia", "cystocele", "Hernia of the urinary bladder (cyst/o)"],
        ["-clasis, -clasia", "breaking", "karyoclasis (karyolysis) · cytoclasis", "Breaking of a cell nucleus · Breaking or destruction of a cell"],
        ["-itis", "inflammation", "colitis", "Inflammation of the colon"],
        ["-megaly", "enlargement", "hepatomegaly", "Enlargement of the liver (hepat/o)"],
        ["-oma", "tumor", "lipoma", "Fatty tumor", "Slide split of the example: lip = fat, oma = tumor."],
        ["-pathy", "any disease of", "neuropathy", "Any disease of the nervous system", "Slide split of the example: neuro = nerve, pathy = disease."],
        ["-rhage, -rhagia", "bursting, profuse flow", "hemorrhage", "Profuse flow of blood", "Slide split of the example: hemor = blood, rhage = flow."],
        ["-rhea", "flow, discharge", "diarrhea", "Frequent passage of watery stool", "Slide split of the example: diarr = through, hea = flow. The slide prints the word “Diarrrhea”."],
        ["-rhexis", "rupture", "amniorrhexis", "Rupture of the amniotic sac (bag of waters)", "Slide split of the example: amnio = amniotic sac, rhexis = rupture. The slide spells the meaning “Reputure” (both spellings accepted)."],
        ["-schisis", "fissure, splitting", "retinoschisis", "Splitting of the retina of the eye"]]),
    # ---------- L5 SUFFIXES ----------
    S("diag", 5, "L5 p3", "suffix", "Suffixes pertaining to disease", [
        ["-graph", "instrument for recording data", "cardiograph", "Instrument used to record the electrical signal from the heart to check for different heart conditions"],
        ["-graphy", "recording data", "roentgenography, radiography", "Obtaining pictures with roentgen rays (x-rays)"],
        ["-gram", "a record of data", "sonogram", "Record obtained by ultrasonography"],
        ["-meter", "instrument for measuring", "spirometer", "Instrument for measuring ventilation and breathing"],
        ["-metry", "measurement", "optometry", "Measurement of vision (opt/o) for glasses"],
        ["-scope", "instrument for viewing or for examining", "cystoscope", "Endoscope used to examine the urinary bladder"],
        ["-scopy", "examination", "laparoscopy", "Examination of the abdomen through the abdominal wall (lapar/o)"]],
      subtitle="recording, measuring & viewing (-graph, -gram, -meter, -scope …)",
      note="Slide title: “Suffix pertaining to disease” (L5 p3)."),
    S("small", 5, "L5 p4", "suffix", "Suffixes that mean “small”", [
        ["-cle", "small", "ventricle", "Small belly or pouch - A cavity"],
        ["-ole", "small", "bronchiole", "Small airway"],
        ["-ula", "small", "macula", "Small spot"],
        ["-ule", "small", "pustule", "Small pimple"]]),
    S("surg", 5, "L5 p5–6", "suffix", "Suffixes pertaining to surgery", [
        ["-centesis", "puncture or tap", "celiocentesis", "Puncture of the abdomen"],
        ["-ectomy", "excision, surgical removal", "tonsillectomy", "Excision of the tonsils (tonsill/o)"],
        ["-desis", "binding, fusion", "pleurodesis", "Binding the pleural membranes (around the lungs)"],
        ["-pexy", "surgical fixation", "uteropexy", "Surgical fixation of the uterus (uter/o)"],
        ["-plasty", "plastic repair, reconstruction", "septoplasty", "Plastic repair of the nasal septum (partition)"],
        ["-rrhaphy", "surgical repair, suture", "herniorrhaphy", "Surgical repair of the hernia (herni/o)"],
        ["-stomy", "surgical creation of an opening", "colostomy", "Creation of an opening into the colon"],
        ["-tome", "instrument for incision (cutting)", "dermatome", "Instrument for cutting the skin"],
        ["-tomy", "incision, cutting", "laparotomy", "Surgical incision of the abdominal wall"],
        ["-tripsy", "crushing", "lithotripsy", "Crushing of a stone"]]),
    S("adj", 5, "L5 p8", "suffix", "Adjective suffixes", [
        ["-ac", "pertaining to", "cardiac", "Pertaining to the heart"],
        ["-al", "pertaining to", "skeletal", "Pertaining to the skeleton"],
        ["-ar", "pertaining to", "muscular", "Pertaining to the muscles"],
        ["-ary", "pertaining to", "urinary", "Pertaining to the urine"],
        ["-ic", "pertaining to", "pelvic", "Pertaining to the pelvis"],
        ["-ical", "pertaining to", "surgical", "Pertaining to surgery"],
        ["-ile", "pertaining to", "febrile", "Pertaining to fever"],
        ["-ous", "pertaining to", "venous", "Pertaining to a vein"],
        ["-ive", "pertaining to", "effective", "Pertaining to having an intended effect"],
        ["-form", "similar to", "epileptiform", "Like or resembling epilepsy"],
        ["-oid", "similar to", "mucoid", "Like or resembling mucus"]]),
]

# ---------- WORD-STRUCTURE ANALYSIS ----------
# part = [type, text, meaning, src]; type p/r/v/s; src: "slide" = split+meaning shown on the slide,
# "table" = meaning taken from a slide table, "def" = inferred from the slide's definition of the word,
# "extra" = not on slides.
def A(term, lec, src, parts, d, kind="built", note=None):
    a = {"term": term, "lec": lec, "src": src, "kind": kind, "def": d,
         "parts": [{"t": p[0], "x": p[1], "m": p[2], "src": p[3]} for p in parts]}
    if note: a["note"] = note
    return a

V = ["v", "o", "", "slide"]
ANALYSIS = [
    A("Carcinogen", 1, "L1 p13", [["r", "carcin", "cancer", "slide"], V, ["s", "gen", "producing", "slide"]], "Substance that promotes the formation of cancer", "slide"),
    A("Pericarditis", 1, "L1 p14", [["p", "peri", "around", "slide"], ["r", "card", "heart", "slide"], ["s", "itis", "inflammation", "slide"]], "Inflammation around the heart", "slide"),
    A("Lipemia", 1, "L1 p15", [["r", "lip", "fat", "slide"], ["s", "emia", "blood condition", "slide"]], "A condition of fat in blood", "slide"),
    A("Hyperlipemia", 1, "L1 p19", [["p", "hyper", "excessive", "slide"], ["r", "lip", "fat", "slide"], ["s", "emia", "blood condition", "slide"]], "A condition of excessive fat in blood", "slide"),
    A("Cardiac", 1, "L1 p20", [["r", "cardi", "heart", "slide"], ["s", "ac", "pertaining to / related to", "slide"]], "Pertaining to heart", "slide"),
    A("Hyperlipoproteinemia", 2, "L2 p7", [["p", "hyper", "excessive", "table"], ["r", "lip", "fat", "table"], V, ["r", "protein", "protein", "def"], ["s", "emia", "blood condition", "table"]], "A condition of excessive fat and protein in blood", "slide"),
    A("Electrocardiogram", 2, "L2 p10", [["r", "electr", "electric", "slide"], V, ["r", "cardi", "heart", "slide"], V, ["s", "gram", "record", "slide"]], "Electrical record of the heart", "slide"),
    A("Vasectomy", 2, "L2 p13", [["r", "vas", "vessel", "slide"], ["s", "ectomy", "excision", "slide"]], "Excision of a vessel", "slide", "Rule 2: no combining vowel before a suffix that begins with a vowel."),
    A("Carditis", 2, "L2 p14", [["r", "card(i)", "heart", "slide"], ["s", "itis", "inflammation", "slide"]], "Inflammation of heart", "slide", "Rule 3: root ends in i, suffix begins with i → drop the root's i."),
    A("Parenteral", 2, "L2 p15", [["p", "par(a)", "alongside of", "slide"], ["r", "enter", "intestine", "slide"], ["s", "al", "pertaining to", "slide"]], "Pertaining to alongside of the intestine", "slide", "Rule 4: prefix ends in a vowel, root begins with a vowel → drop the prefix's a."),
    A("Cardioesophageal", 2, "L2 p16", [["r", "cardi", "heart", "slide"], V, ["r", "esophag", "esophagus", "def"], ["s", "eal", "pertaining to", "slide"]], "Pertaining to heart and esophagus", "slide", "Rule 4b: combining vowel between two roots even when the second root begins with a vowel."),
    # L2 p24 "Your turn" (no answers on slide) — built from slide tables
    A("Hypothermia", 2, "L2 p24 (Your turn) · L3 p9", [["p", "hypo", "under, below, abnormally low", "table"], ["r", "therm", "heat, temperature", "table"], ["s", "ia", "condition of", "table"]], "Low body temperature"),
    A("Oncolysis", 2, "L2 p24 (Your turn) · L3 p19", [["r", "onc", "tumor", "table"], V, ["s", "lysis", "destruction", "def"]], "Destruction (lysis) of a tumor"),
    A("Primigravida", 2, "L2 p24 (Your turn) · L3 p25", [["p", "primi", "first", "table"], ["r", "gravid", "pregnant", "def"], ["s", "a", "", "extra"]], "Woman pregnant (gravid) for the first time", note="The final -a is a noun ending; the slides don't give it a meaning."),
    A("Megabladder", 2, "L2 p24 (Your turn) · L3 p33", [["p", "mega", "large, abnormally large", "table"], ["r", "bladder", "bladder", "def"]], "Permanent enlargement of the bladder", note="No suffix — prefix + root only."),
    # L3
    A("Hypoglycemia", 3, "L3 p14", [["p", "hypo", "under, below, decreased", "table"], ["r", "glyc", "sugar, glucose", "table"], ["s", "emia", "blood condition", "table"]], "Low blood glucose"),
    A("Hyperkalemia", 3, "L3 p15", [["p", "hyper", "over, excess, increased", "table"], ["r", "kal", "potassium", "table"], ["s", "emia", "blood condition", "table"]], "Excess potassium in the blood"),
    A("Hyponatremia", 3, "L3 p16", [["p", "hypo", "under, below, decreased", "table"], ["r", "natr", "sodium", "table"], ["s", "emia", "blood condition", "table"]], "Decrease of sodium in the blood"),
    A("Steatorrhea", 3, "L3 p16", [["r", "steat", "fatty", "table"], V, ["s", "rrhea", "flow, discharge", "table"]], "Fatty diarrhea"),
    A("Azoturia", 3, "L3 p13", [["r", "azot", "nitrogen compound", "table"], ["s", "uria", "urine (condition)", "def"]], "Increased nitrogen compounds in urine", note="On the slide “uria” and “urine” are highlighted in red."),
    A("Pyorrhea", 3, "L3 p20", [["r", "py", "pus", "table"], V, ["s", "rrhea", "discharge", "table"]], "Discharge (rhea) of pus"),
    A("Cyanosis", 3, "L3 p36", [["p", "cyan", "blue", "table"], ["s", "osis", "condition of", "table"]], "Bluish discoloration of the skin due to lack of oxygen"),
    A("Erythrocyte", 3, "L3 p36", [["p", "erythr", "red", "table"], V, ["r", "cyte", "cell", "def"]], "Red blood cell"),
    A("Polioencephalitis", 3, "L3 p37", [["p", "polio", "grey", "table"], ["r", "encephal", "brain", "def"], ["s", "itis", "inflammation", "table"]], "Inflammation of the gray matter of the brain"),
    A("Diplopia", 3, "L3 p26", [["p", "dipl(o)", "double", "table"], ["s", "opia", "vision", "def"]], "Double vision", note="The o of diplo is dropped before opia."),
    A("Hemithorax", 3, "L3 p29", [["p", "hemi", "half, one side", "table"], ["r", "thorax", "chest", "def"]], "One side of the chest (thorax)"),
    A("Normovolemia", 3, "L3 p34", [["p", "normo", "normal", "table"], ["r", "vol", "volume", "def"], ["s", "emia", "blood condition", "table"]], "Normal blood volume"),
    A("Percutaneous", 3, "L3 p39", [["p", "per", "through", "table"], ["r", "cutane", "skin", "def"], ["s", "ous", "pertaining to", "table"]], "Through the skin"),
    A("Endoscope", 3, "L3 p41", [["p", "endo", "in, within", "table"], ["s", "scope", "instrument for viewing or examining", "table"]], "Device for viewing the inside of a cavity or organ"),
    A("Dextrocardia", 3, "L3 p40", [["p", "dextro", "right", "table"], ["r", "card", "heart", "table"], ["s", "ia", "condition of", "table"]], "Location of the heart in the right side of the chest"),
    # L4
    A("Bradycardia", 4, "L4 p5", [["p", "brady", "slow", "table"], ["r", "card", "heart", "table"], ["s", "ia", "condition of", "table"]], "Slow heart rate"),
    A("Tachypnea", 4, "L4 p5", [["p", "tachy", "rapid", "table"], ["r", "pnea", "breathing", "def"]], "Rapid breathing"),
    A("Xerosis", 4, "L4 p5", [["p", "xer(o)", "dry", "table"], ["s", "osis", "condition of", "table"]], "Dryness of the skin or membranes"),
    A("Pachyderma", 4, "L4 p5", [["p", "pachy", "thick", "table"], ["r", "derm", "skin", "def"], ["s", "a", "", "extra"]], "Thickness of the skin", note="Split as coloured on the slide: Pachy|derm|a."),
    A("Oliguria", 4, "L4 p6", [["p", "olig", "few or deficiency of", "table"], ["s", "uria", "urine (condition)", "def"]], "Low urine output", note="Slide spells it “Oligouria”."),
    A("Panplegia", 4, "L4 p6", [["p", "pan", "all", "table"], ["r", "pleg", "paralysis", "def"], ["s", "ia", "condition of", "table"]], "Total paralysis"),
    A("Gastralgia", 4, "L4 p13", [["r", "gastr", "stomach", "def"], ["s", "algia", "pain", "table"]], "Pain in the stomach"),
    A("Cephalodynia", 4, "L4 p13", [["r", "cephal", "head", "def"], V, ["s", "dynia", "pain", "table"]], "Pain in the head (headache)"),
    A("Cystocele", 4, "L4 p13", [["r", "cyst", "urinary bladder", "slide"], V, ["s", "cele", "hernia", "table"]], "Hernia of the urinary bladder"),
    A("Colitis", 4, "L4 p13", [["r", "col", "colon", "def"], ["s", "itis", "inflammation", "table"]], "Inflammation of the colon"),
    A("Hepatomegaly", 4, "L4 p13", [["r", "hepat", "liver", "slide"], V, ["s", "megaly", "enlargement", "table"]], "Enlargement of the liver"),
    A("Lipoma", 4, "L4 p14", [["r", "lip", "fat", "slide"], ["s", "oma", "tumor", "slide"]], "Fatty tumor", "slide"),
    A("Neuropathy", 4, "L4 p14", [["r", "neuro", "nerve", "slide"], ["s", "pathy", "disease", "slide"]], "Any disease of the nervous system", "slide"),
    A("Hemorrhage", 4, "L4 p14", [["r", "hemor", "blood", "slide"], ["s", "rhage", "flow", "slide"]], "Profuse flow of blood", "slide", "Split exactly as on the slide: hemor = blood, rhage = flow."),
    A("Diarrhea", 4, "L4 p14", [["r", "diarr", "through", "slide"], ["s", "hea", "flow", "slide"]], "Frequent passage of watery stool", "slide", "Split exactly as on the slide: diarr = through, hea = flow (the slide prints the word “Diarrrhea”)."),
    A("Amniorrhexis", 4, "L4 p14", [["r", "amnior", "amniotic sac", "slide"], ["s", "rhexis", "rupture", "slide"]], "Rupture of the amniotic sac (bag of waters)", "slide", "Slide labels: amnio = amniotic sac, rhexis = rupture; the word is coloured Amnior|rhexis."),
    A("Retinoschisis", 4, "L4 p14", [["r", "retino", "retina", "slide"], ["s", "schisis", "splitting", "slide"]], "Splitting of the retina of the eye", "slide"),
    # L5
    A("Cardiograph", 5, "L5 p3", [["r", "cardi", "heart", "table"], V, ["s", "graph", "instrument for recording data", "table"]], "Instrument used to record the electrical signal from the heart to check for different heart conditions"),
    A("Sonogram", 5, "L5 p3", [["r", "son", "sound", "table"], V, ["s", "gram", "a record of data", "table"]], "Record obtained by ultrasonography"),
    A("Optometry", 5, "L5 p3", [["r", "opt", "vision", "slide"], V, ["s", "metry", "measurement", "table"]], "Measurement of vision for glasses"),
    A("Cystoscope", 5, "L5 p3", [["r", "cyst", "urinary bladder", "table"], V, ["s", "scope", "instrument for viewing or examining", "table"]], "Endoscope used to examine the urinary bladder"),
    A("Laparoscopy", 5, "L5 p3", [["r", "lapar", "abdomen", "slide"], V, ["s", "scopy", "examination", "table"]], "Examination of the abdomen through the abdominal wall"),
    A("Bronchiole", 5, "L5 p4", [["r", "bronchi", "airway (bronchus)", "def"], ["s", "ole", "small", "table"]], "Small airway"),
    A("Celiocentesis", 5, "L5 p5", [["r", "celi", "abdomen", "def"], V, ["s", "centesis", "puncture or tap", "table"]], "Puncture of the abdomen"),
    A("Tonsillectomy", 5, "L5 p5", [["r", "tonsill", "tonsils", "slide"], ["s", "ectomy", "excision, surgical removal", "table"]], "Excision of the tonsils"),
    A("Pleurodesis", 5, "L5 p5", [["r", "pleur", "pleura (membranes around the lungs)", "def"], V, ["s", "desis", "binding, fusion", "table"]], "Binding the pleural membranes (around the lungs)"),
    A("Uteropexy", 5, "L5 p5", [["r", "uter", "uterus", "slide"], V, ["s", "pexy", "surgical fixation", "table"]], "Surgical fixation of the uterus"),
    A("Septoplasty", 5, "L5 p5", [["r", "sept", "septum (partition)", "def"], V, ["s", "plasty", "plastic repair, reconstruction", "table"]], "Plastic repair of the nasal septum (partition)"),
    A("Herniorrhaphy", 5, "L5 p5", [["r", "herni", "hernia", "slide"], V, ["s", "rrhaphy", "surgical repair, suture", "table"]], "Surgical repair of the hernia"),
    A("Colostomy", 5, "L5 p6", [["r", "col", "colon", "def"], V, ["s", "stomy", "surgical creation of an opening", "table"]], "Creation of an opening into the colon"),
    A("Dermatome", 5, "L5 p6", [["r", "derma", "skin", "def"], ["s", "tome", "instrument for incision (cutting)", "table"]], "Instrument for cutting the skin"),
    A("Laparotomy", 5, "L5 p6", [["r", "lapar", "abdomen", "slide"], V, ["s", "tomy", "incision, cutting", "table"]], "Surgical incision of the abdominal wall"),
    A("Lithotripsy", 5, "L5 p6", [["r", "lith", "stone", "table"], V, ["s", "tripsy", "crushing", "table"]], "Crushing of a stone"),
]

HOMEWORK = {"src": "L2 p24", "title": "Your turn (analyse these)", "terms": ["Hypothermia", "Oncolysis", "Primigravida", "Megabladder"],
            "note": "No answers on the slide; answers in the analysis list are built from the L3 tables."}

GRAPH_TRIO = {"src": "L2 p11", "rows": [["Electrocardiograph", "-graph", "the machine (instrument)"],
                                        ["Electrocardiogram", "-gram", "the record"],
                                        ["Electrocardiography", "-graphy", "the process of recording"]]}

# ---------- LOOK-ALIKES ----------
CONFUSE = [
    {"t": "-graph · -graphy · -gram", "src": "L5 p3 · L2 p11", "rows": [["-graph", "instrument for recording data", "cardiograph"], ["-graphy", "recording data", "radiography"], ["-gram", "a record of data", "sonogram"]],
     "tip": "الماكينة ← العملية ← الورقة اللي طالعة: graph ← graphy ← gram", "tip_extra": True},
    {"t": "-meter · -metry", "src": "L5 p3", "rows": [["-meter", "instrument for measuring", "spirometer"], ["-metry", "measurement", "optometry"]],
     "tip": "اللي بيخلص بـ y هو العملية: metry, scopy, graphy, tomy", "tip_extra": True},
    {"t": "-scope · -scopy", "src": "L5 p3", "rows": [["-scope", "instrument for viewing or for examining", "cystoscope, endoscope"], ["-scopy", "examination", "laparoscopy"]],
     "tip": "scope = الأداة، scopy = الفحص نفسه"},
    {"t": "-tome · -tomy · -ectomy · -stomy", "src": "L5 p5–6", "rows": [["-tome", "instrument for incision (cutting)", "dermatome"], ["-tomy", "incision, cutting", "laparotomy"], ["-ectomy", "excision, surgical removal", "tonsillectomy"], ["-stomy", "surgical creation of an opening", "colostomy"]],
     "tip": "ec = out: ectomy بتشيل العضو. stomy = فتحة", "tip_extra": True},
    {"t": "-rhage · -rhea · -rhexis · -rrhaphy", "src": "L4 p14 · L5 p5", "rows": [["-rhage, -rhagia", "bursting, profuse flow", "hemorrhage"], ["-rhea", "flow, discharge", "diarrhea"], ["-rhexis", "rupture", "amniorrhexis"], ["-rrhaphy", "surgical repair, suture", "herniorrhaphy"]],
     "tip": "rrhaphy بس هي اللي surgery (L5)، الباقي disease (L4)"},
    {"t": "-pexy · -desis · -plasty", "src": "L5 p5", "rows": [["-pexy", "surgical fixation", "uteropexy"], ["-desis", "binding, fusion", "pleurodesis"], ["-plasty", "plastic repair, reconstruction", "septoplasty"]], "tip": ""},
    {"t": "-algia · -dynia", "src": "L4 p13", "rows": [["-algia", "pain", "gastralgia"], ["-dynia", "pain", "cephalodynia"]], "tip": "الاتنين = pain"},
    {"t": "-iatry · -iatrics · -iatrist", "src": "L4 p10", "rows": [["-iatry", "field of medicine", "psychiatry"], ["-iatrics", "field of medicine", "pediatrics"], ["-iatrist", "specialist (person)", "podiatrist"]], "tip": "-ist في الآخر = شخص"},
    {"t": "Hyper · Hypo · Super · Olig/o · Pan", "src": "L4 p6", "rows": [["hyper-", "over, excess, abnormally high, high, increased", "hypertension"], ["hypo-", "under - below, abnormally low, decreased", "hypoventilation"], ["super-", "above or excess", "superinfection"], ["olig/o", "few or deficiency of", "oliguria"], ["pan-", "all", "panplegia"]], "tip": ""},
    {"t": "Ante · Pre · Pro · Post", "src": "L4 p4", "rows": [["ante-", "before", "antenatal"], ["pre-", "before, in front of", "predisposing"], ["pro-", "before, in front of", "prophylaxis"], ["post-", "after, behind", "postoperative"]], "tip": ""},
    {"t": "Dia · Per · Trans", "src": "L3 p38–39", "rows": [["dia", "through", "dialysis"], ["per", "through", "percutaneous"], ["trans", "through", "transfusion"]], "tip": "التلاتة = through"},
    {"t": "Ab · Ad · Ex/o · Endo · Ecto", "src": "L3 p38–41", "rows": [["ab", "away from", "abduct"], ["ad", "toward, near", "adhesion"], ["ex/o", "away from, outside", "excise"], ["endo", "in, within", "endoscope"], ["ecto", "out, outside", "ectopic"]],
     "tip": "Ab = Away، Ad = aDd (يقرّب)", "tip_extra": True},
    {"t": "Dextro · Levo · Sinistro/o", "src": "L3 p40", "rows": [["dextro", "right", "dextrocardia"], ["levo", "left", "levorotation"], ["sinistro/o", "left", "sinistrad"]], "tip": ""},
    {"t": "Mon/o · Uni · Prim/i", "src": "L3 p24–25", "rows": [["mon/o", "one", "monoclonal"], ["uni", "one", "unicellular"], ["prim/i", "first", "primigravida"]], "tip": "prim = first مش one"},
    {"t": "Di · Diplo · Bi", "src": "L3 p26", "rows": [["di", "two, twice", "diplegia"], ["diplo", "double", "diplopia"], ["bi", "two, twice", "bicuspid"]], "tip": ""},
    {"t": "Hemi · Semi", "src": "L3 p29", "rows": [["hemi", "half, one side", "hemithorax"], ["semi", "half, partial", "semilunar"]], "tip": ""},
    {"t": "Macro · Mega · Micro", "src": "L3 p33", "rows": [["macro", "large, abnormally large", "macroscopic"], ["mega, megalo", "large, abnormally large", "megabladder"], ["micro", "small", "microsurgery"]], "tip": ""},
    {"t": "Homo · Iso · Hetero", "src": "L3 p32", "rows": [["homo, homeo", "same, unchanging", "homothermic"], ["iso", "same, equal", "isograft"], ["hetero", "other, different, unequal", "heterosexual"]], "tip": ""},
    {"t": "Noct/i · Nyct/o · Chron/o", "src": "L3 p11", "rows": [["noct/i", "night", "nocturnal"], ["nyct/o", "night, darkness", "nyctophobia"], ["chron/o", "time", "synchronous"]], "tip": ""},
    {"t": "Py/o · Pyr/o", "src": "L3 p20", "rows": [["py/o", "pus", "pyorrhea"], ["pyr/o", "fever, fire", "pyretic"]], "tip": "pyR = fiRe", "tip_extra": True},
    {"t": "Adip/o · Lip/o · Steat/o", "src": "L3 p13–16", "rows": [["adip/o", "fat", "adiposis"], ["lip/o", "lipid", "liposuction"], ["steat/o", "fatty", "steatorrhea"]], "tip": ""},
    {"t": "Kal · Natr/i · Calci · Ferr/o", "src": "L3 p14–17", "rows": [["kal/", "potassium", "hyperkalemia"], ["natr/i", "sodium", "hyponatremia"], ["calci", "calcium", "—"], ["ferr/i, ferr/o", "iron", "ferric, ferrous"]],
     "tip": "K = Kalium, Na = Natrium", "tip_extra": True},
    {"t": "Yellow · Grey · Green", "src": "L3 p37", "rows": [["xanth/o, icter/", "yellow", "xanthoma, icterus index"], ["polio, glauc/o", "grey", "polioencephalitis"], ["verd/o", "green", "verdoglobin"]], "tip": ""},
    {"t": "Small: -cle · -ole · -ula · -ule", "src": "L5 p4", "rows": [["-cle", "small", "ventricle"], ["-ole", "small", "bronchiole"], ["-ula", "small", "macula"], ["-ule", "small", "pustule"]], "tip": "الأربعة = small"},
    {"t": "Pertaining to vs similar to", "src": "L5 p8", "rows": [["-ac, -al, -ar, -ary, -ic, -ical, -ile, -ous, -ive", "pertaining to", "cardiac … effective"], ["-form, -oid", "similar to (like, resembling)", "epileptiform, mucoid"]], "tip": ""},
]

# ---------- CONCEPT QUESTIONS (every option is slide text; "o"[0] is the correct answer) ----------
# p = page in that lecture's PDF, quote = exact slide text proving the answer.
_PDEF = "Prefix a word part attached to the beginning of a word root to modify its meaning"
_SDEF = "Suffix a word part attached to the end of the word root to modify its meaning"
_RDEF = "Root the word part that is the core of the word"
_CDEF = "Combining Vowel a word part, usually an “O” or “i”"
_DEFS = {"Prefix": "a word part attached to the beginning of a word root to modify its meaning",
         "Suffix": "a word part attached to the end of the word root to modify its meaning",
         "Root": "the word part that is the core of the word",
         "Combining vowel": "a word part, usually an “O” or “i”"}
_DEFQ = {"Prefix": (11, _PDEF), "Suffix": (11, _SDEF), "Root": (11, _RDEF), "Combining vowel": (12, _CDEF)}
CONCEPT_Q = []
for _k, (_p, _quote) in _DEFQ.items():
    _others = [v for kk, v in _DEFS.items() if kk != _k]
    CONCEPT_Q.append({"lec": 1, "p": _p, "quote": _quote, "level": "easy", "skill": "recall", "type": "mcq", "tests": ["c:" + _k],
                      "q": f"According to the slides, the {_k.lower()} is:", "o": [_DEFS[_k]] + _others,
                      "ar": f"تعريف الـ {_k} من السلايد: {_DEFS[_k]}."})
    CONCEPT_Q.append({"lec": 1, "p": _p, "quote": _quote, "level": "medium", "skill": "reverse", "type": "mcq", "tests": ["c:" + _k],
                      "q": f"“{_DEFS[_k][0].upper() + _DEFS[_k][1:]}” is the definition of the:", "o": [_k] + [kk for kk in _DEFS if kk != _k],
                      "ar": f"ده تعريف الـ {_k} (L1)."})
CONCEPT_Q += [
    {"lec": 1, "p": 8, "quote": "Final Written Exam= 75 Marks", "level": "easy", "skill": "recall", "type": "mcq", "tests": ["c:grading"],
     "q": "On the grading slide, the Final Written Exam is worth:", "o": ["75 Marks", "25 Marks", "20 Marks", "5 Marks"],
     "ar": "الـ Final written = 75 درجة."},
    {"lec": 1, "p": 8, "quote": "•Research= 5 Marks", "level": "easy", "skill": "recall", "type": "mcq", "tests": ["c:grading2"],
     "q": "On the grading slide, Research is worth:", "o": ["5 Marks", "20 Marks", "25 Marks", "75 Marks"],
     "ar": "الـ Research = 5 درجات، والـ Mid-term/Quiz = 20."},
    {"lec": 1, "p": 8, "quote": "•Mid-term/ Quiz= 20 Marks •Research= 5 Marks Class Activity/ Periodicals (25 Marks)", "level": "medium", "skill": "recall", "type": "mcq", "tests": ["c:grading3"],
     "q": "On the grading slide, Class Activity / Periodicals is made of:", "o": ["Mid-term/ Quiz= 20 Marks and Research= 5 Marks", "Final Written Exam= 75 Marks", "Practical Exam (-) Marks", "Bonus= 2 to 3 Marks"],
     "ar": "الـ 25 درجة = 20 (Mid-term/Quiz) + 5 (Research)."},
    {"lec": 1, "p": 9, "quote": "Medical terminology is used in the field of medicine and pharmacy", "level": "easy", "skill": "recall", "type": "tf", "tests": ["c:def"],
     "q": "Medical terminology is used in the field of medicine and pharmacy.", "a": True, "ar": "صح — مكتوبة كده في L1 p9."},
    {"lec": 1, "p": 9, "quote": "It is the language used to precisely describe the human body including its components, processes, conditions affecting it, and procedures performed upon it", "level": "easy", "skill": "recall", "type": "tf", "tests": ["c:def2"],
     "q": "Medical terminology is the language used to precisely describe the human body including its components, processes, conditions affecting it, and procedures performed upon it.", "a": True,
     "ar": "صح — ده التعريف بالنص (L1 p9)."},
    {"lec": 1, "p": 10, "quote": "Most of them comes from Latin or Greek words Other language such as English ,German", "level": "easy", "skill": "recall", "type": "mcq", "tests": ["c:origin"],
     "q": "According to the slides, most medical terms come from:", "o": ["Latin or Greek words", "English", "German", "French"],
     "ar": "معظمها Latin أو Greek؛ English وGerman وFrench لغات تانية أقل."},
    {"lec": 1, "p": 10, "quote": "Most medical terms are a combination of word parts prefix Root Suffix /Stem", "level": "easy", "skill": "recall", "type": "tf", "tests": ["c:parts"],
     "q": "Most medical terms are a combination of word parts: prefix, root (stem) and suffix.", "a": True, "ar": "صح (L1 p10)."},
    {"lec": 1, "p": 11, "quote": _RDEF, "level": "easy", "skill": "recall", "type": "tf", "tests": ["c:Root"],
     "q": "The suffix is the word part that is the core of the word.", "a": False,
     "fix": "The ROOT is the word part that is the core of the word.", "ar": "غلط — الـ Root هو الـ core."},
    {"lec": 1, "p": 11, "quote": _PDEF, "level": "medium", "skill": "error-find", "type": "mcq", "tests": ["c:Prefix"],
     "q": "“A prefix is a word part attached to the end of the word root.” Choose the correct judgement:",
     "o": ["False — the prefix is “a word part attached to the beginning of a word root to modify its meaning”", "True", "False — the prefix is “the word part that is the core of the word”", "False — the prefix is “a word part, usually an “O” or “i””"],
     "ar": "الـ prefix في الأول (beginning)، والـ suffix في الآخر (end)."},
    # ---------- L2 ----------
    {"lec": 2, "p": 6, "quote": "[ o ] is the most common combining vowel [ i ] is the second most common combining vowel.", "level": "easy", "skill": "recall", "type": "tf", "tests": ["c:cv1"],
     "q": "[i] is the most common combining vowel.", "a": False, "fix": "[o] is the most common combining vowel; [i] is the second most common.",
     "ar": "غلط — o الأشهر، و i التاني."},
    {"lec": 2, "p": 6, "quote": "When a medical term has more than one root, each is joined by a vowel", "level": "easy", "skill": "recall", "type": "tf", "tests": ["c:cv2"],
     "q": "When a medical term has more than one root, each is joined by a vowel.", "a": True, "ar": "صح (L2 p6)."},
    {"lec": 2, "p": 8, "quote": "Is their presence mandatory Not all medical terms have combining vowels", "level": "easy", "skill": "recall", "type": "tf", "tests": ["c:cv3"],
     "q": "All medical terms must have combining vowels.", "a": False, "fix": "Not all medical terms have combining vowels.",
     "ar": "غلط — مش إجبارية: Not all medical terms have combining vowels."},
    {"lec": 2, "p": 8, "quote": "Why we use Combining vowels To ease pronunciation", "level": "easy", "skill": "recall", "type": "tf", "tests": ["c:cv4"],
     "q": "We use combining vowels to ease pronunciation.", "a": True, "ar": "صح — عشان النطق يبقى أسهل."},
    {"lec": 2, "p": 17, "quote": "All medical terms build from the root.", "level": "easy", "skill": "recall", "type": "mcq", "tests": ["c:formation"],
     "q": "According to the slides, all medical terms build from the:", "o": ["Root", "Prefix", "Suffix", "Combining vowel"],
     "ar": "كل الـ medical terms بتتبني من الـ root (L2 p17)."},
    {"lec": 2, "p": 17, "quote": "Prefixes and suffixes are attached to the root to modify its meaning", "level": "easy", "skill": "recall", "type": "tf", "tests": ["c:formation2"],
     "q": "Prefixes and suffixes are attached to the root to modify its meaning.", "a": True, "ar": "صح (L2 p17)."},
    {"lec": 2, "p": 7, "quote": "Additional Roots {often a medical term is formed of two or more roots} Hyper/lip/o/protein/emia", "level": "medium", "skill": "recall", "type": "mcq", "tests": ["c:addroots"],
     "q": "Which of these slide terms is formed of two roots?", "o": ["Hyperlipoproteinemia", "Hyperlipemia", "Lipemia", "Carditis"],
     "ar": "Hyper/lip/o/protein/emia فيها root اتنين: lip و protein."},
    # graph trio (L2 p11 picture labels)
    {"lec": 2, "p": 11, "quote": "Electrocardiograph (machine)", "level": "medium", "skill": "discriminate", "type": "mcq", "tests": ["c:graph"],
     "q": "On the -graph / -gram / -graphy picture slide, the machine (instrument) is the:", "o": ["Electrocardiograph", "Electrocardiogram", "Electrocardiography", "Cardiograph"],
     "ar": "graph = الماكينة، gram = الورقة، graphy = العملية."},
    {"lec": 2, "p": 11, "quote": "Electrocardiogram (record)", "level": "medium", "skill": "discriminate", "type": "mcq", "tests": ["c:gram"],
     "q": "On the -graph / -gram / -graphy picture slide, the record is the:", "o": ["Electrocardiogram", "Electrocardiograph", "Electrocardiography", "Cardiograph"],
     "ar": "gram = الـ record (الورقة اللي بتطلع)."},
    {"lec": 2, "p": 11, "quote": "Electrocardiography (process)", "level": "medium", "skill": "discriminate", "type": "mcq", "tests": ["c:graphy"],
     "q": "On the -graph / -gram / -graphy picture slide, the process of recording is:", "o": ["Electrocardiography", "Electrocardiogram", "Electrocardiograph", "Cardiograph"],
     "ar": "graphy = العملية نفسها (process)."},
    # ---------- L4 ----------
    {"lec": 4, "p": 2, "quote": "Main meaning of the term; Usually indicates the organ, system or action; e.g. cardi-, nephro-, hepat-, gastr-", "level": "easy", "skill": "recall", "type": "mcq", "tests": ["c:color-root"],
     "q": "On the colour-code slide, which word part is highlighted green?", "o": ["Root", "Prefix", "Suffix", "Combining vowel"],
     "ar": "Prefix أزرق · Root أخضر · Suffix بينك."},
    {"lec": 4, "p": 2, "quote": "Meaning before the root; Modifies the meaning; e.g. hyper-, hypo-, anti-, pre-", "level": "easy", "skill": "recall", "type": "mcq", "tests": ["c:color-prefix"],
     "q": "On the colour-code slide, which word part is highlighted blue?", "o": ["Prefix", "Root", "Suffix", "Combining vowel"],
     "ar": "الـ Prefix أزرق."},
    {"lec": 4, "p": 2, "quote": "Meaning after the root; Indicates condition, procedure, disease, drug class, etc.; e.g. -itis, -emia, -ology, -logy, -ase", "level": "easy", "skill": "recall", "type": "mcq", "tests": ["c:color-suffix"],
     "q": "On the colour-code slide, which word part is highlighted pink?", "o": ["Suffix", "Prefix", "Root", "Combining vowel"],
     "ar": "الـ Suffix بينك."},
    {"lec": 4, "p": 2, "quote": "Main meaning of the term; Usually indicates the organ, system or action", "level": "easy", "skill": "recall", "type": "mcq", "tests": ["c:color-root2"],
     "q": "On the colour-code slide, the root usually indicates:", "o": ["the organ, system or action", "condition, procedure, disease, drug class, etc.", "Meaning before the root", "Meaning after the root"],
     "ar": "الـ Root = main meaning وغالبًا العضو أو الجهاز أو الـ action."},
    {"lec": 4, "p": 2, "quote": "e.g. cardi-, nephro-, hepat-, gastr-", "level": "medium", "skill": "reverse", "type": "mcq", "tests": ["c:color-ex1"],
     "q": "Which one is given on the colour-code slide as a ROOT example?", "o": ["cardi-", "hyper-", "-itis", "anti-"],
     "ar": "أمثلة الـ Root: cardi-, nephro-, hepat-, gastr-."},
    {"lec": 4, "p": 2, "quote": "e.g. -itis, -emia, -ology, -logy, -ase", "level": "medium", "skill": "reverse", "type": "mcq", "tests": ["c:color-ex2"],
     "q": "Which one is given on the colour-code slide as a SUFFIX example?", "o": ["-emia", "hypo-", "nephro-", "pre-"],
     "ar": "أمثلة الـ Suffix: -itis, -emia, -ology, -logy, -ase."},
    {"lec": 4, "p": 2, "quote": "e.g. hyper-, hypo-, anti-, pre-", "level": "medium", "skill": "reverse", "type": "mcq", "tests": ["c:color-ex3"],
     "q": "Which one is given on the colour-code slide as a PREFIX example?", "o": ["anti-", "hepat-", "-ase", "-logy"],
     "ar": "أمثلة الـ Prefix: hyper-, hypo-, anti-, pre-."},
    {"lec": 4, "p": 3, "quote": "Prefix- categories: Time and position; Disease; Degree; Negative prefix", "level": "max", "skill": "discriminate", "type": "mcq", "tests": ["c:prefcat"],
     "q": "Which one is NOT a prefix category in Lecture 4?", "o": ["Surgery", "Time and position", "Degree", "Negative prefix"],
     "ar": "Surgery دي فئة suffix. فئات الـ prefix: Time and position, Disease, Degree, Negative."},
    {"lec": 4, "p": 9, "quote": "Medical suffixes can be categorized into: Specialties; Condition of; Disease; Small; Surgery; Adjective suffix", "level": "max", "skill": "discriminate", "type": "mcq", "tests": ["c:sufcat"],
     "q": "Which one is NOT a suffix category on the slides?", "o": ["Degree", "Specialties", "Small", "Adjective suffix"],
     "ar": "Degree دي فئة prefix (L4 p3)."},
    {"lec": 4, "p": 9, "quote": "Suffixes tend to bring an action to the medical terms.", "level": "easy", "skill": "recall", "type": "tf", "tests": ["c:suffix"],
     "q": "Suffixes tend to bring an action to the medical terms.", "a": True, "ar": "صح (L4 p9)."},
    {"lec": 4, "p": 9, "quote": "Suffixes are the ending part of medical terms.", "level": "easy", "skill": "recall", "type": "tf", "tests": ["c:suffix2"],
     "q": "Suffixes are the beginning part of medical terms.", "a": False, "fix": "Suffixes are the ENDING part of medical terms.", "ar": "غلط — الـ suffix هو الـ ending part."},
    {"lec": 4, "p": 12, "quote": "A condition of a person, animal, or plant in which its body or structure is harmed because an organ or part is unable to work as it usually does", "level": "easy", "skill": "recall", "type": "tf", "tests": ["c:disease"],
     "q": "Disease is a condition of a person, animal, or plant in which its body or structure is harmed because an organ or part is unable to work as it usually does.", "a": True,
     "ar": "صح — ده تعريف الـ disease (L4 p12)."},
    {"lec": 4, "p": 10, "quote": "Indicates a PERSON (specialist): -ist · -ian, -ician · -iatrist", "level": "hard", "skill": "discriminate", "type": "mcq", "tests": ["c:person"],
     "q": "Which suffix indicates a PERSON (specialist), not a field of study?", "o": ["-iatrist", "-iatry", "-iatrics", "-logy"],
     "ar": "-ist, -ian/-ician, -iatrist = شخص. -logy, -iatrics, -iatry = field."},
    {"lec": 4, "p": 10, "quote": "Indicates a FIELD of study: -logy · -iatrics · -iatry", "level": "max", "skill": "discriminate", "type": "mcq", "tests": ["c:field"],
     "q": "Which suffix does NOT indicate a FIELD of study?", "o": ["-ist", "-logy", "-iatrics", "-iatry"],
     "ar": "-ist = شخص (specialist)، الباقي field."},
    # ---------- L5 ----------
    {"lec": 5, "p": 7, "quote": "A suffix added to a root word to form an adjective.", "level": "easy", "skill": "recall", "type": "tf", "tests": ["c:adj"],
     "q": "An adjective suffix is a suffix added to a root word to form an adjective.", "a": True, "ar": "صح (L5 p7)."},
    {"lec": 5, "p": 8, "quote": "suffixes that mean “Similar to”: -form Epileptiform · -oid Mucoid", "level": "medium", "skill": "reverse", "type": "mcq", "tests": ["c:similar"],
     "q": "Which pair of suffixes means “similar to”?", "o": ["-form and -oid", "-ac and -al", "-ile and -ous", "-ic and -ical"],
     "ar": "-form و -oid = similar to. الباقي pertaining to."},
]

# Slide spellings. "accept" = medical word: typed answers accept BOTH forms and the slide form is never
# marked wrong or used as a spelling trap. "silent" = plain-English typo, fixed silently.
SLIDE_TYPOS = [
    ["L2 p20–23", "Pleural (table header)", "Plural", "silent"],
    ["L2 p10", "combing vowel", "combining vowel", "silent"],
    ["L2 p10", "suffix beginning with a constant", "consonant", "silent"],
    ["L3 p25–26", "Defination", "Definition", "silent"],
    ["L3 p38", "memberane", "membrane", "silent"],
    ["L3 p15", "to loss water", "to lose water", "silent"],
    ["L4 p6", "out put", "output", "silent"],
    ["L5 p8", "having and intended effect", "having an intended effect", "silent"],
    ["L3 p29", "Hemi thorax", "Hemithorax", "accept"],
    ["L3 p37", "Polioencephalities", "Polioencephalitis", "accept"],
    ["L4 p6", "Oligouria", "Oliguria", "accept"],
    ["L4 p14", "Reputure", "Rupture", "accept"],
    ["L4 p14", "Diarrrhea (example word)", "Diarrhea", "accept"],
    ["L2 p16", "Rule numbered 4 twice", "listed here as rule 4b", "note"],
]
# typed answers: every form below is accepted wherever the key is accepted (slide form + standard form)
ACCEPT_BOTH = {"oliguria": ["oligouria"], "hemithorax": ["hemi thorax"], "polioencephalitis": ["polioencephalities"],
               "rupture": ["reputure"], "diarrhea": ["diarrrhea"], "sinistro/o": ["sinistr/o"],
               "-rhage": ["-rrhage"], "-rhagia": ["-rrhagia"], "-rhea": ["-rrhea"], "-rhexis": ["-rrhexis"]}
# never used as spelling-trap targets or as "wrong option" distractors
TYPO_WORDS = {"oliguria", "oligouria", "hemithorax", "polioencephalitis", "polioencephalities", "diarrhea", "diarrrhea",
              "rupture"}

EXCLUDED = [
    "Photos of doctors (L1 p2 poster, L4 p1, L5 p1)",
    "Condolence slides (L4 p15–16)",
    "Decorative AI title/divider/end illustrations (L2 p1, p25; L3 p1–3, p10, p12, p18, p21–22, p31, p42; L5 p7 artwork)",
    "Third-party clinical photos (L2 p19 ptosis photo, L3 p33 microsurgery photo, L3 p34 newborn photo)",
    "Course-file / specification admin infographics (L1 p3–5) — only grading kept",
    "Drug brand images (L4 p8) — drug classes kept as text",
    "Medical idioms: listed in the course plan (L1 p4) for L4, but no slide covers it — no content written",
]

