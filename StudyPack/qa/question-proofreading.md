# Stage 3b — Step 4: independent proofreading of the question bank

Bank: `content/content.json`, built by `tools/build_content.py` → `tools/bank.py` (seed 25102026), gated by `tools/check_content.py` (**ALL CHECKS PASSED**).
Final size: **739 questions**. Reviewed snapshots: `qa/review/reviewed-bank-v1.json` (4a), `v2` (L2 re-run, 4c), `v3` (4d/4e/4f packets).

## Final counts

| Lecture | easy | medium | hard | max | total | typed |
|---|---:|---:|---:|---:|---:|---:|
| L1 | 11 | 6 | 3 | 7 | 27 | 10 |
| L2 | 6 | 13 | 12 | 12 | 43 | 28 |
| L3 | 84 | 98 | 100 | 23 | 305 | 274 |
| L4 | 49 | 71 | 70 | 25 | 215 | 186 |
| L5 | 33 | 52 | 43 | 21 | 149 | 127 |
| **Total** | **183** | **240** | **228** | **88** | **739** | **625** |

- Production (typed / two-blank / analysis): **85%** (G1 ≥ 60%). MCQ share: medium 13%, hard 2%, max 0% (G1 ≤ 30%).
- T/F **3.7%**, 15 true / 12 false (G5). MCQ answer slots 22/22/22/21 (G4). Largest stem template **6.9%** (G6 ≤ 8%).
- L3+L4+L5 = 91% of the bank.
- Shortfalls (< 8 per lecture × level; not padded): L1 medium 6, L1 hard 3, L1 max 7, L2 easy 6. L1/L2 are mostly concept slides.
- P9 transfer: L1 0, L2 2, L3 8, L4 4, L5 2. L1 has none because every L1 term shows its own part meanings on its own slide, so asking it is recall, not transfer. Only 1 max P9.

Lecture × pattern:
```
       P1   P2   P3   P4   P5   P6   P7   P8   P9  P10  P11  P12  P13  P14
L1      5    0    0    0    0    0    0    0    0    0    5    0    0   17
L2      7    0    0    0    0    0    0    0    2   18    6    0    0   10
L3      8   95   42    9    3   44    0   24    8    0    8    2   31   31
L4     11   61   12   18    0   16    5   15    4   12   11    6   21   23
L5     10   31   11   24    0   11    0   16    2   14   10    4    1   15
```
Score histogram: 1–10: 164 · 11–20: 19 · 21–30: 35 · 31–40: 194 · 41–50: 11 · 51–60: 21 · 61–70: 207 · 71–80: 0 · 81–90: 33 · 91–100: 55.

## 4a — blind slide-fidelity review (6 fresh agents, slide images only, no levels)
Reports: `review/4a_L1L2.md`, `4a_L3a.md`, `4a_L3b.md`, `4a_L4a.md`, `4a_L4b.md`, `4a_L5.md`, `4a_L2_rerun.md`.

| Lecture | level agreement (blind level = ours) |
|---|---|
| L1 | 25/28 = 89% |
| L2 | 32/47 = **68%** → revised, re-run once on a shuffled packet: 37/43 = **86%** |
| L3 | 303/307 = 99% (*) |
| L4 | 196/218 = 90% |
| L5 | 138/151 = 91% |
| all | 694/751 = 92% |

(*) The first-round packets listed each lecture's questions in level order, which can bias a blind rater. L3's 99% is probably inflated by that. The L2 re-run packet was shuffled (order no longer reveals the level).

No question was found to be **invented** or contradicted by a slide. All failures were accept-list, wording or citation problems. Every one was fixed in the **generator**, so the fix applies to all similar questions:

| Problem found | Fix (all questions of that kind) |
|---|---|
| "Complete the definition" blanks accepted every meaning of the part (Hypertension means …… blood pressure accepted "over/excess"; Euthanasia accepted "true/good") | P4/P5 accept only the word that fits the blank (+ slide spelling variants) |
| "Write the part" accepted a slide synonym with a *different* slide meaning (hemi ↔ semi, iso ↔ homo, noct/i ↔ nyct/o, ante- ↔ pre-/pro-) | P6 accepts only parts with the identical slide meaning; skipped when another slide part also carries that meaning (ab / ex/o "away from") |
| Slide wording missing from accepts: rhage = flow, pathy = disease, gram = record, ectomy = surgical removal, di = twice, gray/grey, Reputure/Rapture, "record of data" without "a", karyolysis | meaning pieces now include the slide example labels, the same part on another slide table, article-free forms, slide spellings and printed aliases |
| Odd-one-out blank 1 accepted synonyms of the odd item (-ia also accepted -iasis…) | blank 1 accepts only the odd item's own forms |
| Analysis splits: Optometry root accepted a bare "o"; Herniorrhaphy accepted "hernior / rhaphy"; Carditis lacked "card / itis"; Amniorrhexis root shown as "amnior" (slide label "amnio") | split filter, bracket-free split, slide label used |
| Graded analysis meanings that were paraphrases ("under, below, abnormally low") | analysis grading uses the slide row's exact wording, or the field is part-only |
| Missing citations: "emia = blood condition", "card = heart" (L1 worked examples), cyst/o (L4 s13), rule distractor pages, swap partner of an error-find | every graded part, swap partner and rule option now cites its own slide page |
| Stems that leaked the answer: "(cyst/o)", "(lysis)" in definitions; "(25 Marks)"; "-emia" only option with a leading hyphen; "A-" for Analgesia / "-ian" for Physician | parentheticals naming a part are dropped; hyphen cue removed; the part is shown in the form the slide example uses |
| Rule MCQs with two defensible rules (Cardioesophageal, Parenteral) | the stem names the exact vowel the rule explains |
| "As split on the slide" where no split is shown (Hypothermia), Xerosis colour split ambiguous | phrase only when the slide shows the split; Xerosis excluded from split-based items |
| P9 "transfer" on L1/L2 worked examples whose meaning is printed beside the term | removed (recall, not transfer) |
| Concept MCQ distractor that is itself a slide description of the answer ("Meaning after the root"); "Additional Roots" stem giving the answer | distractor and stem replaced in `slide_data.py` |
| "(Latin plural)" not slide wording | "According to the slides (Singular and Plural Forms)" |

Level disagreements kept on purpose: regular plurals stay **medium** and irregular plurals **hard** (as the spec defines). One-blank contrasts P8 stay hard (the spec's discrimination level).

## 4c — test-wise student (no slides)
- Pilot L4: first version 9/20 answered from cues → 12–14/20 after fixes (cues left are everyday-English words such as un-, post-, hypo-).
- Full bank, 40 random medium+ questions (`review/4c_answers.md`): the main finding was **cross-question leakage inside one random set**, e.g. a Dextrocardia error-find showing the analysis another question asks for. The quiz assembler prevents it: each question's `leak` tokens (answer, tested parts, **term**) must not appear in any other stem or option of the same quiz. Result: **0 leaks in 50 generated Mix-40 quizzes** (`tools/quizlib.py`).
- Self-revealing error-finds (brady = thick while "Slow heart rate" is shown): the generator now picks a part whose true meaning is not visible, or hides the medical-meaning line.
- Remaining guessable-by-English items (fungi, multi, hypothermia, heterosexual…) are kept as warm-ups at easy/medium.

## 4d — ramp check (3 Mix quizzes of 20)
First run: Quiz 1 = 1, Quiz 2 = **5**, Quiz 3 = 0 clear inversions. All 5 in Quiz 2 came from one one-part transfer (P9) scoring at the top of the hard band. **Weights fixed:** a one-part transfer is capped at the entry of the hard band; only two-part transfers get the transfer bonus. Re-check 1 (fresh blind agent, `review/4d_result_v2.md`): **18 clear inversions** (Quiz 1: 4, Quiz 2: 8, Quiz 3: 6), almost all from one cause: a hard **two-part analysis** scored 63, *below* single-term hard items (65–68), so it landed mid-band. **Weights fixed (25 Oct):** analysis now earns +3 per graded field beyond the first and +4 as a multi-step item (hard 2-part analysis = 73, top of the hard band); error-find / odd-one-out +3 → +5. After the fix every hard analysis sits after all one-term hard items (script check on the 3 regenerated quizzes; no second blind run).
Kept on purpose (level definitions, not ramp bugs): medium T/F after easy open recall; error-find vs two-blank contrast inside max (borderline).

## 4e — feedback check (30 simulated wrong answers, 5 per E1–E6)
`review/4e_feedback.md`: the engine (`tools/quizlib.py`) returns the intended code for **30/30** cases (E1 5, E2 5, E3 5, E4 5, E5 5, E6 5). One bug was found and fixed on the way: a dropped combining vowel in the middle of the word (onclysis) was reported as E3 instead of E4.
Independent agent check of the Arabic (`review/4e_arabic_check.md`, all 22 cited slide images opened): accurate 27/30, Arabic OK 25/30, helpful 27/30; nothing invented, every page citation right. Fixed in the engine/generator:
- E1 look-alike text no longer says "المطلوب معنى …" on *write-the-part* questions: now "X دا معنى Y (ref). الإجابة هنا: part = meaning (ref)."
- E4 fired when a dropped o belonged to a **prefix** (homo-thermic, hypo-thermia): now E3 naming the prefix. Real combining-vowel slips state one definite rule (missing o → L2·s10; extra o before a vowel → L2·s13), one line.
- E2 names the part type and cites the answer's own slide.
- Engine vs reviewed codes after the fix: 30/30 (the packet's two "intended E4" cases are now correctly E3).
Not done (nice-to-have): naming the missing doubled letter in E3, dropping a repeated meaning in E5/E6, LRM before a leading hyphen in RTL text (do in the website renderer).

## 4f — final spot-check (40 random, ≥ 8 per level)
Independent agent run (`review/4f_result.md`, 36 slide images opened): **38/40 pass all checks** (grounded 40, accepts 39, unambiguous 40, level fair 40, feedback 39). Fixed:
- Dextrocardia: the slide colour split **Dextro | cardia** (L3 p40, verified) is now accepted (`SPLIT_EXTRA`).
- Rule citations used the term's lecture with the rule page ("L5·s10"): every citation now takes the lecture from the evidence file (`bank.py evref`, `quizlib._ref`) → "L2·s10".

## Pilot (Phase 1)
See `qa/pilot-L4.md`: 25 L4 questions, 4a agreement 88–92%, every review rule from 24 Oct carried into `bank.py`:
- max ≥ 2 steps
- subtle error-finds ("0, 1 or 2 mistakes", some fully correct, look-alike swaps)
- odd-one-out from ≥ 2 tables
- accepted-not-slide answers flagged with "صح كتركيب، بس الكلمة اللي في السلايد … — اكتبها هي في الامتحان."
- P9 transfer items
- the `difficulty` field
- per-blank / per-field partial credit
