"""Verify the held City scans and repeated generator-test observations."""
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
args = parser.parse_args()
ledger = json.loads(Path(__file__).with_name("SOURCE-PINS.json").read_text())
docs = {}
for pin in [ledger["discovery"], *ledger["sources"]]:
    name = pin["file"]
    data = (args.sources / name).read_bytes()
    require(len(data) == pin["bytes"], name)
    require(hashlib.sha256(data).hexdigest() == pin["sha256"], f"{name} SHA-256")
    if "pages" in pin:
        docs[name] = fitz.open(stream=data, filetype="pdf")
        require(len(docs[name]) == pin["pages"], f"{name} physical pages")


def page(source_id, number):
    return " ".join(docs[source_id + ".pdf"][number - 1].get_text().split())


checks = 0
for source_id in ("000172389", "000172539", "000172543", "000174096"):
    for n, anchor in [
        (1, "7/31/99"),
        (2, "7 seconds"),
        (2, "temporary use"),
        (3, "ready to deliver emergency power at demand"),
        (3, "air in the"),
    ]:
        require(anchor in page(source_id, n), f"{source_id} p. {n}: {anchor}")
        checks += 1
for source_id, n, anchor in [
    ("000169712", 1, "April 7,1998"),
    ("000169712", 1, "May 4,1998"),
    ("000172978", 1, "none was logged"),
    ("000172978", 1, "to 3 seconds"),
    ("000173489", 2, "generator installation"),
    ("000173495", 2, "generator installation"),
]:
    require(anchor in page(source_id, n), f"{source_id} p. {n}: {anchor}")
    checks += 1
print(f"10 source hashes and sizes, 9 PDF page counts and {checks} textual checks passed")
