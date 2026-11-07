"""Check four pinned bodies and the Table A–1 right-hand location field.

Requires PyMuPDF. Supply the four paths in source-ledger order.
"""
import argparse
import hashlib
import json
from pathlib import Path

import fitz


def check(condition, description):
    if not condition:
        raise SystemExit(f"Failed: {description}")


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("body", nargs=4, type=Path)
args = parser.parse_args()
ledger = json.loads(Path(__file__).with_name("SOURCE-PINS.json").read_text())
anchor_count = 0
for path, source in zip(args.body, ledger["sources"], strict=True):
    body = path.read_bytes()
    check(len(body) == source["bytes"], f"{source['label']} byte length")
    check(hashlib.sha256(body).hexdigest() == source["sha256"], f"{source['label']} SHA-256")
    if source["format"] == "html":
        lines = body.decode().splitlines()
        for line, needles in source["anchors"].items():
            for needle in needles:
                check(needle in lines[int(line) - 1], f"HTML line {line}: {needle}")
                anchor_count += 1
        continue
    with fitz.open(stream=body, filetype="pdf") as pdf:
        for page, needles in source["anchors"].items():
            words = " ".join(pdf[int(page) - 1].get_text().split())
            for needle in needles:
                check(needle in words, f"{source['label']} p. {page}: {needle}")
                anchor_count += 1

with fitz.open(args.body[2], filetype="pdf") as pdf:
    hits = []
    for number in range(87, 93):
        words = pdf[number - 1].get_text("words")
        for x, y, _, _, value, *_ in words:
            if x > 475 and value == "B":
                row = sorted((w for w in words if abs(w[1] - y) < 4.5), key=lambda w: w[0])
                hits.append((number, " ".join(w[4] for w in row)))
expected = [(87, "C-14 or S-18"), (89, "C-128 Ch Channel"), (91, "M-34 Ch Channel")]
check(len(hits) == len(expected), "count of standalone B locations on Table A–1 pages")
for (page, row), (expected_page, name) in zip(hits, expected, strict=True):
    check(page == expected_page and name in row, f"location row for {name}")

print(f"4 hashes and lengths, {anchor_count} source anchors and all 3 standalone B location rows passed")
