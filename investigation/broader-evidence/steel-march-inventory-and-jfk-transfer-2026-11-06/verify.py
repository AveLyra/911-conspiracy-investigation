"""Check pinned PDF bytes, text anchors and published transcription counts.

Requires PyMuPDF. Supply all four local source paths in ledger order.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

import fitz


def check(condition, description):
    if not condition:
        raise SystemExit(f"Failed: {description}")


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("pdf", nargs=4, type=Path)
args = parser.parse_args()
folder = Path(__file__).resolve().parent
ledger = json.loads((folder / "SOURCE-PINS.json").read_text(encoding="utf-8"))
checks = 0
for pdf, source in zip(args.pdf, ledger["sources"], strict=True):
    data = pdf.read_bytes()
    check(len(data) == source["bytes"], f"length of {pdf.name}")
    check(hashlib.sha256(data).hexdigest() == source["sha256"], f"SHA-256 of {pdf.name}")
    with fitz.open(stream=data, filetype="pdf") as doc:
        for page, anchors in source["anchors"].items():
            page_text = " ".join(doc[int(page) - 1].get_text().split())
            for anchor in anchors:
                check(anchor in page_text, f"{pdf.name} p. {page}: {anchor}")
                checks += 1

report = folder / "README.md"
if not report.exists():
    report = folder / "REPORT.md"
rows = re.findall(
    r"^\| (B-\d+(?:-\d+)?) \| (\w+) \| (.*?) \| (.*?) \|$",
    report.read_text(encoding="utf-8"),
    flags=re.MULTILINE,
)
check(len(rows) == len({row[0] for row in rows}) == 12, "12 unique B-series rows")
check(
    Counter(row[3] for row in rows) == {"JFK/PL": 5, "JFK": 1, "205": 2, "202": 2, "PL": 2},
    "location-code counts",
)
check(
    Counter(row[2] for row in rows) == {"WTC 1": 3, "WTC 2": 3, "—": 6},
    "building-field counts",
)
print(f"4 PDF hashes and lengths, {checks} text anchors and 3 transcription count checks passed")
