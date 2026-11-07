"""Verify the source bodies and selected request, receipt and process fields.

Requires PyMuPDF. Supply the three source paths in ledger order.
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
parser.add_argument("pdf", nargs=3, type=Path)
args = parser.parse_args()
ledger = json.loads(Path(__file__).with_name("SOURCE-PINS.json").read_text())
for path, pin in zip(args.pdf, ledger["sources"], strict=True):
    data = path.read_bytes()
    check(len(data) == pin["bytes"], f"{pin['label']} byte length")
    check(hashlib.sha256(data).hexdigest() == pin["sha256"], f"{pin['label']} SHA-256")
    with fitz.open(path, filetype="pdf") as pdf:
        check(len(pdf) == pin["pages"], f"{pin['label']} page count")

anchors = [
    {
        2: ["09-15 11/24/2008", "09-42 1/27/2009", "WTC - Photos/videos", "09-48 2/5/2009"],
        3: ["09-63 3/4/2009", "09-88 4/27/2009", "WTC7 Docs"],
    },
    {
        1: ["November 20, 2008", "NOV 24 2008"],
        11: ["February 27, 2009", "High strength bolt testing", "Welding testing"],
        12: ["February 26, 2009"], 13: ["February 26, 2009"],
        14: ["April 21, 2009", "APR 27 2009"],
        15: ["Native source files for all images in Chapter 5"],
    },
    {
        2: ["request Log# 10-038", "administrative processing file contents"],
        5: ["your February 4, 2009", "FOIA control Desk on February 6, 2009", "FOIA Log #09-48"],
        17: ["On February 18, 2009", "BFRL proceed with the actual search"],
        35: ["Enclosed you will find a disc", "8,910 files", "withholding 3,370 files"],
    },
]
count = 0
for path, pages in zip(args.pdf, anchors, strict=True):
    with fitz.open(path, filetype="pdf") as pdf:
        for page, strings in pages.items():
            text = " ".join(pdf[page - 1].get_text().split())
            for anchor in strings:
                check(anchor in text, f"{path.name} p. {page}: {anchor}")
                count += 1
print(f"3 PDF hashes, lengths and page counts and {count} content anchors passed")
