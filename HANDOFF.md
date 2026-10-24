# HANDOFF: Medical Terminology Study Pack, Stage 1 (content)

## Goal
Stage 1 of 5: `StudyPack\content\content.json` becomes the single verified source for the PDF and the website. The user's spec asks for:
- page images and `inventory.md`
- `content.json` in the exact schema
- ≥150 questions, ≥40 of them typed
- an independent verifier subagent
- a script that runs the self-checks
- `verification-report.md`

**Stop after Stage 1** and show the user the summary table and the list of uncertain items.
Project rules are in `CLAUDE.md`, which also holds the decisions. The exam is **Sunday 25 Oct 2026**; today is 24 Oct, so time matters.

## Done
- `StudyPack\content\pages\L{1-5}_pNN.png`, `TS_p01.png`: all 114 pages, 110 dpi; dense image tables at 150 dpi (`tools\rasterize.py`).
- `StudyPack\content\inventory.md`: one line per page with a USE / ADMIN / DECOR / EXCLUDE tag.
- `StudyPack\content\slide-transcription.md`: my page-by-page transcription of what each slide says.
- `StudyPack\tools\slide_data.py`: all slide data (META, CONCEPTS, RULES, PRON, PLURALS, SECTIONS, ANALYSIS via `A()`, CONFUSE, QUIZ, SLIDE_TYPOS, EXCLUDED).
- `StudyPack\tools\build_content.py`: converts that data to the user's schema and adds the extra analyses, spelling traps (with `say`, marked extra) and generated questions. The seed is fixed, so output is deterministic.
- `StudyPack\tools\check_content.py`: checks schema, lec/slide, duplicate parts, answer-in-options, synonym distractors, false T/F corrections and accepted alternatives, then prints the summary table. It imports `build_content`, so running it also rebuilds `content.json`.
- `StudyPack\content\content.json`: built and **ALL CHECKS PASSED**.
  - 23 sections, 163 rows, 73 analyses, 56 traps, 25 look-alikes
  - 484 questions, 157 typed; 82% from L3–L5
- `StudyPack\qa\independent-verification.md`: the verifier subagent's findings: **0 ERROR, 0 MISSING, 5 QUESTION, 14 MINOR**.

## Current state
- The verifier's findings are **not applied yet**.
- `StudyPack\content\verification-report.md` is **outdated**: it's from the first pass, which used the old schema. It must be rewritten.

## Next steps (in order)
1. Apply the verifier's fixes in `slide_data.py` / `build_content.py`:
   - **q400 Hemorrhage analyze:** also accept the slide split `hemor / rhage`. Make `analyze` answers a list of accepted splits, or add an `accept` field.
   - **q403 Diarrhea analyze:** explain why the slide split "diarr = through / hea = flow" isn't used; the slide also misprints "Diarrrhea".
   - **q407 / q409 / q415:** reword to "According to the slide (Latin plural)…", or drop lumens / indexes / ganglions as distractors (they are valid English plurals).
   - **q189 hint:** analgesia uses `an-` (not `a-`). Fix the spell-question hint for multi-form rows, e.g. show `a-, an-`.
   - **Analysis notes:** Hyperlipoproteinemia parts are marked "slide" but L2 p7 gives no part meanings; mark them `table`. Cardiograph `medical` should get the full slide definition ("…to check for different heart conditions"). The note saying "Rule 5" should say "rule 4b".
   - **Page numbers:** the `Ch` pronunciation row → slide 18 (`PRON_PAGE` in `build_content.py`). The phys section slide → "4–9".
   - **Spelling traps:** don't list valid British spellings as misspellings (diarrhoea, paediatrics, amoebiasis, haem-, tachypnoea, hyponatraemia, hyperkalaemia, coeliocentesis, leucoplakia). Label them "British spelling — use American (slide) spelling", or replace them.
   - Small wording fixes: ferrous "reduced form" (the slide has no "form"; add a note or drop it); oliguria "out put" (slide wording).
2. Rebuild and recheck: `python -I StudyPack/tools/check_content.py` must print ALL CHECKS PASSED.
3. Rewrite `StudyPack\content\verification-report.md` with:
   - counts per lecture (rows and questions, from the check output)
   - the verifier's findings and how each was fixed
   - uncertain items (see below)
   - every (extra) item: `say` pronunciations, look-alike tips with `tipIsExtra`, the meaning "against" for anti-, analysis parts with `meaning: null` (`-ion`, `-ia` in analgesia, `-a` in primigravida), and invented quiz distractors
   - excluded content
4. Report to the user: what was made and where, the summary table, and the uncertain list. Then **stop**: Stage 2 (PDF) only starts on the user's go.

## Uncertain items to report
- Diarrhea split slip (L4 p14).
- Hemorrhage slide split "hemor + rhage".
- "-Dysnia" kept as an alt of -dynia (probably a slide slip).
- "Sinistro/o" shown as sinistr/o.
- `def`-inferred part meanings (cutane = skin, encephal = brain, pnea = breathing, …).
- Anti- has no written meaning on its slide.
- L5 p3 table titled "Suffix pertaining to disease" but its content is instruments.
- Medical idioms: no slide covers it, so no content was written.
- The old Anki files in `Revision\` were never verified and probably carry v1 errors (radi/o, kal/i, icter/o).

## Decisions & why
- `slide` = PDF page number(s) as a string, e.g. "7–9", so students can find the page.
- Rules use ids 1, 2, 3, 4, 4b: the slides number two rules "4", and the user asked for 1–4 (+4b).
- Analysis parts carry an extra `from` key (slide / table / def / extra) so inferred meanings stay honest. Meanings that can't be derived are `null`.
- Some non-schema keys are added (`ar`, `note`, `subtitle`, `lowPriority`, `workedOnSlide`, `alsoSee`, `sayIsExtra`, `correction`); all schema keys are kept as named. Extra meta (credit, disclaimer, colors, slideTypos, excluded, homework) lives under `meta`.
- Questions are generated two per table row (types rotate). Distractors must have distinct meanings and must not come from `SYN_GROUPS`. A "Which X means…" question is skipped when its meaning is shared by several parts (e.g. "condition of", "pertaining to").
- Python is run with `-I`. PyMuPDF was installed with the user's approval (option "A"). There is no git repo.

## Failed approaches (do not retry)
- `sed`-replacing a docstring in `slide_data.py` broke the triple quotes once; it's fixed now. Edit with Python or the Edit tool instead.
- Writing `build_content.py` with the Write tool without reading it first failed. The old file was moved aside, then deleted.
- Early distractor picking allowed duplicate or synonymous options (di/bi both "two, twice"). It is fixed by the mutual `clash()` check in `distractors()`.

## How to verify
- `python -I StudyPack/tools/check_content.py` should end with ALL CHECKS PASSED, with ≥150 questions, ≥40 typed and an L3–L5 share of 70–90%.
- Spot-check rows against `StudyPack\content\pages\*.png` using the `slide` field.

## Update 2026-10-24
Steps 1–3 done: verifier fixes applied, check_content.py ALL CHECKS PASSED (484 q / 157 typed / 82% L3–L5), verification-report.md rewritten. Next: Stage 2 (PDF) on the user's go.
