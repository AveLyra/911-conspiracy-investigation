#!/usr/bin/env python3
"""Bounded OCR locator test. Does not export page text or defeat redactions."""
import concurrent.futures
import hashlib
import re
import subprocess
import sys
from pathlib import Path
import fitz

source = Path(sys.argv[1])
expected = "ccbb8e3b92af9efcdd09b427375ea25659134a9b8bc027b45c3bf7d138e2259c"
assert hashlib.sha256(source.read_bytes()).hexdigest() == expected, "Unexpected source bytes"
doc = fitz.open(source)
assert len(doc) == 22
images = [page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5), colorspace=fitz.csGRAY).tobytes("png") for page in doc]
def search(item):
    index, image = item
    completed = subprocess.run(["tesseract", "stdin", "stdout", "--psm", "3"], input=image, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    text = completed.stdout.decode("utf-8", errors="replace")
    return (index + 1, bool(re.search(r"notifications?\s+to\s+military", text, re.I)), bool(re.search(r"09\s*[/.-]\s*20\s*[/.-]\s*0?1", text)), bool(text))
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = sorted(pool.map(search, enumerate(images)))
print("pages:", len(results))
print("title matches:", [n for n, title, date, nonempty in results if title])
print("date-pattern matches:", [n for n, title, date, nonempty in results if date])
print("nonempty OCR results:", sum(nonempty for n, title, date, nonempty in results))
assert len(results) == 22 and all(nonempty for n, title, date, nonempty in results)
assert [n for n, title, date, nonempty in results if title] == [11]
assert not [n for n, title, date, nonempty in results if date]
