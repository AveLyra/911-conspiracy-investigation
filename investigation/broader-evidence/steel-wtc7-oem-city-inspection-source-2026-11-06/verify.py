"""Verify the five held City PDFs and selected textual comparisons."""
import argparse
import hashlib
import json
from pathlib import Path

import fitz


def require(condition, label):
    if not condition:
        raise SystemExit(f"Failed: {label}")


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("source_directory", type=Path)
parser.add_argument("prior_memo", type=Path)
args = parser.parse_args()
ledger = json.loads(Path(__file__).with_name("SOURCE-PINS.json").read_text())
docs = {}
for pin in ledger["sources"]:
    name = pin["file"]
    path = args.prior_memo if name == "000169174.pdf" else args.source_directory / name
    data = path.read_bytes()
    require(len(data) == pin["bytes"], name)
    require(hashlib.sha256(data).hexdigest() == pin["sha256"], f"{name} digest")
    docs[name] = fitz.open(stream=data, filetype="pdf")
    require(len(docs[name]) == pin["pages"], f"{name} page count")


def page(file_id, number):
    return " ".join(docs[file_id + ".pdf"][number - 1].get_text().split())


comparisons = [
    (22, 21, "necessary sign-offs of The Port Authority"),
    (22, 21, "certified air balancing report approved by Landlord's engineer"),
    (23, 22, "Landlord's Completion Notice"),
    (23, 22, "three (3) business day period, shall be deemed Certification"),
    (25, 24, "Certificate of Occupancy or other sufficient indicia of legality"),
    (64, 62, "Tenant shall have the right to maintain a fuel tank"),
    (93, 98, "Pumps for fuel oil, water, etc."),
]
for left, right, value in comparisons:
    require(value in page("000166927", left) and value in page("000167068", right), value)
require("DD-5" in page("000166927", 79), "Lease A extracted label")
require("DD-3 7• Floor Plan" in page("000167068", 84), "Lease B OCR label")
require("A-8 or other report" in page("000169180", 13), "FDNY checklist")
require("Building Record Folder" in page("000169180", 14), "FDNY instructions")
require("8/17/90" in page("000169205", 12), "FDNY unrelated shutdown date")
print("5 PDF hashes, byte lengths and page counts, 7 cross-copy passage checks and 5 text locators passed")
