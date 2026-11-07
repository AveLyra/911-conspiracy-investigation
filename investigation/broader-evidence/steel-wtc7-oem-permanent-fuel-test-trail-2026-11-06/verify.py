"""Verify source pins, date and pump references, and transcribed airflow sums."""
import argparse
import hashlib
import json
from pathlib import Path

import fitz


def require(condition, label):
    if not condition:
        raise SystemExit(f"Failed: {label}")


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("sources", type=Path)
parser.add_argument("marked_memo", type=Path)
parser.add_argument("nist_pdf", type=Path)
args = parser.parse_args()
ledger = json.loads(Path(__file__).with_name("SOURCE-PINS.json").read_text())
existing = {"000172389.pdf": args.marked_memo, "ncstar1-1j.pdf": args.nist_pdf}
docs = {}
for pin in ledger["sources"]:
    name = pin["file"]
    data = existing.get(name, args.sources / name).read_bytes()
    require(len(data) == pin["bytes"], name)
    require(hashlib.sha256(data).hexdigest() == pin["sha256"], f"{name} SHA-256")
    docs[name] = fitz.open(stream=data, filetype="pdf")
    require(len(docs[name]) == pin["pages"], f"{name} PDF page count")


def page(name, number):
    return " ".join(docs[name + ".pdf"][number - 1].get_text().split())


anchors = [
    ("000168654", 1, "Peoria"),
    ("000171252", 1, "7/31/99"),
    ("000171252", 1, "enclosed please find a copy"),
    ("000171520", 1, "February 15,2000"),
    ("000171520", 1, "1854"),
    ("000172395", 1, "July 17,1999"),
    ("000172397", 1, "3 pages (including cover sheet)"),
    ("000174147", 1, "PRECISION TESTING"),
    ("ncstar1-1j", 58, "LO-207"),
    ("ncstar1-1j", 58, "LO-203"),
    ("ncstar1-1j", 58, "anti-siphon valve"),
]
for name, number, anchor in anchors:
    require(anchor in page(name, number), f"{name} p. {number}: {anchor}")
for row in ledger["airflow_rows"]:
    for column in ("required", "final"):
        require(sum(row[f"{column}_cfm"]) == row[f"expected_{column}_total"],
                f"{row['system']} {column} column")
print("8 PDF hashes, sizes and page counts, 11 text anchors, and 6 airflow-column sums passed")
