"""Render every slide page to StudyPack/content/pages/L{n}_p{NN}.png (110 dpi; dense image tables at 150 dpi)."""
import pymupdf, os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "StudyPack", "content", "pages")
FILES = {"L1": "Lecture (1) Terminology (Clinical) - 2027.pdf", "L2": "Lecture (2) Terminology (Clinical) - 2027-students.pdf",
         "L3": "Lecture (3) Terminology-2027-students.pdf", "L4": "4-Medical Terminology - Clinical - Fall 26-27.pdf",
         "L5": "Lecture 5-Medical Terminology - Clinical - Fall 26-27.pdf", "TS": "Medical terminology Training Sheet.pdf"}
DENSE = {"L1": {5}, "L3": {4, 19, 20, 23, 24, 30, 36, 40}, "L4": set(range(2, 15)), "L5": set(range(2, 9)), "TS": {1}}
for k, f in FILES.items():
    doc = pymupdf.open(os.path.join(ROOT, f))
    for i, page in enumerate(doc, 1):
        dpi = 150 if i in DENSE.get(k, ()) else 110
        page.get_pixmap(dpi=dpi).save(os.path.join(OUT, f"{k}_p{i:02d}.png"))
    print(k, len(doc), "pages")
