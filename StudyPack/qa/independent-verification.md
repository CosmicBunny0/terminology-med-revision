# Independent verification: content.json against the slide images

Scope: sections, concepts, rules, pronunciation, plurals, analysis, questions (all 484), meta.exam/grading.
I read every page image directly; no text extraction was used. The intended typo corrections listed in the brief are not reported.

Result: no ERROR found. Every section row, concept, rule, pronunciation row, plural and analysis definition matches its cited slide. Every MCQ has exactly one correct option, every TF key is right and every false item has a correct correction.

## Findings

[QUESTION] questions q400 (analyze Hemorrhage) — L4 p14 — slide splits the word as "hemor = blood" + "rhage = flow" — key is "hem / o / rrhage" only. A student who copies the slide's split would be marked wrong. Accept both splits, or add a note saying the slide's split is also acceptable.
[QUESTION] questions q403 (analyze Diarrhea) — L4 p14 — slide splits "diarr = through" + "hea = flow" (and the example word is printed "Diarrrhea") — key is "dia / rrhea". The correction is right and is documented in meta.slideTypos, but the answer screen should say why the slide's split is not used.
[QUESTION] questions q407 (plural of lumen) — L2 p20/22 — slide: lumina — distractor "lumens" is also a valid English plural. Reword as "According to the slide (Latin plural) …".
[QUESTION] questions q409 (plural of index) — L2 p20/22 — slide: indices — distractor "indexes" is also a valid English plural. Same rewording fix.
[QUESTION] questions q415 (plural of ganglion) — L2 p23 — slide: ganglia — distractor "ganglions" is also a valid English plural. Same rewording fix.
[MINOR] questions q189 (spell, "Pain killer") — L4 p7 — slide row is "A- / An-" and the example uses an- — the hint says "(a- = not)" while the answer analgesia uses an-. Better: "(a-/an- = not)".
[MINOR] questions q333 / q335 / q344 (build) — L3 p37, L3 p29, L4 p6 — slide typos "polioencephalities", "hemi thorax", "oligouria" — these are accepted as correct answers. This is consistent with the notes, but it reinforces typo spellings.
[MINOR] sections chem / ferr/i definition — L3 p14 — "(ferrous : containing iron in reduced)" — JSON: "containing iron in reduced form" (adds the word "form").
[MINOR] sections deg / olig/o definition — L4 p6 — "Low urine out put" — JSON: "Low urine output".
[MINOR] sections sdis / -dynia alts — L4 p13 — slide lists "-Dysnia" above "-Dynia" — JSON keeps "-dysnia" as an alternative form. It is faithful to the slide but is probably a slide slip; consider a note so students don't learn "-dysnia".
[MINOR] sections phys slide — L3 p4–9 — rows also appear on p5–6 (picture versions) — JSON cites "4, 7–9". The content is identical.
[MINOR] pronunciation Ch.slide and questions q420.slide — L2 p18 — the Ch → k row is in the table on p18 (p17 is "Formation of medical terms") — JSON cites slide 17.
[MINOR] concepts analysis body — L1 p13 vs p16–20 — the "Root + combining vowel + suffix (carcinogen)" pattern is on p13 — the concept cites "16–20".
[MINOR] analysis Hyperlipoproteinemia — L2 p7 — slide shows only the labels prefix/root/vowel/root/suffix, with no part meanings — parts are marked from:"slide". The meanings hyper/lip/emia come from L1 p19, and "protein = protein" is not on any slide. The marking should be "table" or "def".
[MINOR] analysis Hemorrhage — L4 p14 — slide split "hemor / rhage" — JSON uses "hem / o / rrhage" (this is noted in the entry).
[MINOR] analysis Cardiograph medical — L5 p3 — "…from the heart to check for different heart conditions" — JSON drops "to check for different heart conditions". The section row has the full text.
[MINOR] analysis Cardioesophageal note — L2 p16 — the note says "Rule 5" while the rules list uses id "4b" (meta.slideTypos also says "listed as rule 5"). This is an internal naming inconsistency.
[MINOR] analysis Dermatome — L5 p6 — split "derma + tome" — the usual root is dermat/o. It produces the right word, so nothing changes for the student.
[MINOR] spellingTraps (outside the requested scope) — several "traps" are valid British spellings, not misspellings: diarrhoea, paediatrics, amoebiasis, hyponatraemia, hyperkalaemia, tachypnoea, leucoplakia, coeliocentesis. Label them "British spelling; use the slide spelling" rather than as errors.

## Checked and correct (no finding)
- sections: all 23 sections and every row (part, alts, meaning, example, definition) against L3 p4–41, L4 p4–14, L5 p3–8. There are no missing or invented rows. The anti- "against" meaning is correctly flagged as (extra), and no question depends on it.
- concepts (19), rules_intro, rules 1–4b, pronunciation (12), plurals (8): all match L1 p6–12, L2 p4–23, L4 p2/3/8/9/12, L5 p7. Rule 1's "constant" is silently fixed to consonant, as intended.
- analysis (73): all `medical` definitions match their slides. Slide-split words (L1 p13–15, p19–20; L2 p7, p10, p13–16; L4 p14) match apart from the notes above. All `from:"def"` inferences are reasonable (e.g. lysis = destruction, gravid = pregnant, opia = vision, pnea = breathing, cyte = cell, encephal = brain, alges = pain, nat = birth).
- questions: 223 MCQ (exactly one correct option each, and no synonym clash: no question offers both mon/o and uni, levo and sinistro, dia/per/trans, -algia and -dynia, and so on), 83 TF (all keys correct, all corrections correct), 84 spell, 73 build and 21 analyze (all answers use the slide spelling, with the noted exceptions).
- meta.exam: Term Work Exam, Sunday 25 October 2026 (the weekday is verified), Lecture 1 → Lecture 5, Analytical Pharmaceutical Chemistry Lab 1, according to the group distribution — matches L5 p9. Grading: 25 (mid-term/quiz 20 + research 5), practical (-), bonus 2 to 3, final written 75 — matches L1 p8.

## Pages checked
All 114 images: L1 p01–21, L2 p01–25, L3 p01–42, L4 p01–16, L5 p01–09, TS p01.
I read the content pages at full resolution. I read the title, divider, photo and admin pages (L1 p1–7, p21; L2 p1, p25; L3 p1–3, 10, 12, 18, 21–22, 31, 42; L4 p1, 15–16; L5 p1) and L2 p2–10, p12–24 and TS p1 on reduced-resolution contact sheets. All were legible enough for this check.
Not fully readable: the small print on the L1 p3–5 course-file infographics and the L5 p9 lab-distribution table (only reduced resolution). That content is excluded from the pack, apart from the exam facts, which are readable.
