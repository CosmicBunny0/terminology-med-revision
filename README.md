# MedTerm L1–L5 Study Pack

Unofficial student summary for Medical Terminology (ENG 101), PharmD Clinical — Fall 2026. The doctors' slides are the reference.

- `StudyPack/site/` — the website (deployed on Vercel, root directory = `StudyPack/site`). Rebuild: `node StudyPack/site/build.js`
- `StudyPack/content/content.json` — single verified data source. Rebuild + check: `python -I StudyPack/tools/check_content.py`
- `StudyPack/pdf/` — printable PDF + its builder
- `StudyPack/qa/` — Playwright tests for the site

Slide PDFs and page images are not in this repo.
