# Project: Medical Terminology L1–L5 Study Pack

## Who and why
I'm Mohammed Aymen, PharmD Clinical Pharmacy year 1, October 6 University (Clinical 3).
Course: Medical Terminology (ENG 101). I'm building a free study pack for my whole batch:
a PDF to send to the batch WhatsApp group + an interactive website (flashcards, quizzes).
It must be accurate (100+ students will study from it), clean, easy, and look professional.

## Exam facts (from the slides)
- Term Work Exam: Sunday 25 October 2026, covers Lecture 1 → Lecture 5. Written exam.
- Grading: class activity/periodicals 25 (mid-term/quiz 20 + research 5) + final written 75.
- Written exam ⇒ spelling, word-structure analysis and meanings matter most.

## Source files (the ONLY reference — this folder)
- `Lecture (1) Terminology (Clinical) - 2027.pdf` — Dr. Shaimaa Gomaa Ibrahim (21 pages)
- `Lecture (2) Terminology (Clinical) - 2027-students.pdf` — Dr. Shaimaa Gomaa Ibrahim (25 pages)
- `Lecture (3) Terminology-2027-students.pdf` — Dr. Shaimaa Gomaa Ibrahim (42 pages)
- `4-Medical Terminology - Clinical - Fall 26-27.pdf` — made by Assoc. Prof. Amira Ahmed, edited by Dr. Hagar Belal Ahmad (16 pages)
- `Lecture 5-Medical Terminology - Clinical - Fall 26-27.pdf` — made by Assoc. Prof. Dr. Amira A. Alqazar, edited by Dr. Hagar Belal Ahmad (9 pages)
- `Medical terminology Training Sheet.pdf` — Dr. Hagar Belal Ahmad Abo-Zalam (blank analysis template: Medical term | Term structure (Prefix- / -Root- / -Suffix) | Meaning | Meaning of the medical term)
- `Revision\Terminology Sprint (offline).html` — v1 study page already built from these slides. Its inline `<script>` holds draft data (SECTIONS, ANALYSIS, PLURALS, PRON, RULES, CONCEPTS, CONFUSE) and a spelling-traps list (TRAPS). Use it as a STARTING DRAFT ONLY; every item must be re-verified against the slides.

CRITICAL: most slides are IMAGES (no text layer). All of L4 and L5 are images, and so are about half of L3.
Text extraction alone will miss most of the content. Rasterize every page (e.g. `pdftoppm -r 110 -png`)
and LOOK at each image. Never conclude "not in the slides" from text extraction alone.

## Content rules
- Slides are the exam reference. Anything not in the slides (pronunciation guides, mnemonics,
  extra notes) is labelled "(زيادة للفهم)" in Arabic UI or "(extra)" in English.
- Spelling: copy the slides exactly (they use American spelling: diarrhea, pediatrics, esophag-).
  Known slide typos → write the correct form + a small note:
  "Reputure" → Rupture (-rrhexis) · "Pleural" (plural table header) → Plural ·
  "Polioencephalities" → Polioencephalitis · "Hemi thorax" → Hemithorax ·
  "Oligouria" → write "Oliguria (slide: Oligouria)" and accept both in quizzes ·
  "Defination", "combing vowel", "memberane" → fix silently.
- "Medical idioms" appears in the course plan for L4, but no slide covers it. Do NOT invent content for it.
- Never include: photos of people (doctors, students), the two condolence slides at the end of L4,
  decorative AI illustrations from the slides, or anything personal (my student ID, phone).
- Credit the doctors as the source on the cover/footer. Add the line "Unofficial student summary — the
  doctors' slides are the reference."

## Visual identity (shared by PDF and website)
- Colour code from the L4 slide "Color Code for Medical Terminology" (highlighters):
  prefix = blue, root = green, suffix = pink. Add combining vowel = amber.
  Use it consistently everywhere a word part appears.
- Phone-first: most students will read on phones from WhatsApp.
- Arabic notes in Egyptian colloquial, short; all terms in English exactly as on the slides.
  Arabic text must render with proper shaping and RTL (use Noto Sans Arabic or IBM Plex Sans Arabic).
- Use the design skills available (frontend-design / artifact-design / theme-factory if installed).
  Avoid generic AI looks (purple gradients, emoji section headers, everything centred, cream + terracotta).

## Decisions
- CREDIT_LINE: Prepared by Mohammed Aymen · PharmD Clinical 3 · Fall 2026
- PAGE_SIZE: A4 portrait   (alternative: phone format 108×192 mm)
- EXPLANATION_LANG: English content + short Egyptian-Arabic notes
- HOSTING: Vercel   (alternatives: GitHub Pages · claude.ai artifact public link)
- SITE_URL: https://terminology-med-revision.vercel.app

## Output folder
Everything goes in `StudyPack\` inside this folder:
StudyPack\content\content.json, StudyPack\content\verification-report.md,
StudyPack\pdf\…, StudyPack\site\index.html, StudyPack\qa\…
Never modify or delete the original slide PDFs.

## Working style
- Ask me only when blocked on a real decision; otherwise pick the sensible default and tell me.
- After each stage: list what you made, where, and anything you were unsure about.
