"""Verify report bytes, text anchors and the printed C14-SP coefficient difference.

Requires PyMuPDF. Supply three PDFs in the order recorded in SOURCE-PINS.json.
"""
import argparse
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import re

import fitz


def check(condition, description):
    if not condition:
        raise SystemExit(f"Failed: {description}")


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("pdf", nargs=3, type=Path)
args = parser.parse_args()
ledger = json.loads(Path(__file__).with_name("SOURCE-PINS.json").read_text())
count = 0
for path, source in zip(args.pdf, ledger["sources"], strict=True):
    body = path.read_bytes()
    check(len(body) == source["bytes"], f"{source['label']} byte length")
    check(hashlib.sha256(body).hexdigest() == source["sha256"], f"{source['label']} SHA-256")
    with fitz.open(stream=body, filetype="pdf") as pdf:
        for page, needles in source["anchors"].items():
            text = " ".join(pdf[int(page) - 1].get_text().split())
            for needle in needles:
                check(needle in text, f"{source['label']} p. {page}: {needle}")
                count += 1

with fitz.open(args.pdf[0]) as pdf:
    table = pdf[118].get_text()
    figure = pdf[258].get_text()
    table_match = re.search(r"TS: m=([0-9.]+)±0\.0015\s+75\s+C14-SP", table)
    plot_match = re.search(r"m=([0-9.]+)±0\.0015 TS Longitudinal", figure)
    check(table_match and plot_match, "both printed coefficient values")
    table_m, plot_m = Decimal(table_match[1]), Decimal(plot_match[1])
    check((table_m, plot_m) == (Decimal("0.0108"), Decimal("0.0109")), "printed coefficients")
    check(plot_m - table_m == Decimal("0.0001"), "coefficient difference")

print(f"3 PDF hashes and lengths, {count} source anchors and both printed coefficient values passed")
