"""Verify the cited City scans and inspection-record text anchors."""
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
parser.add_argument("alteration_packet", type=Path)
args = parser.parse_args()
ledger = json.loads(Path(__file__).with_name("SOURCE-PINS.json").read_text())
docs = {}
for pin in ledger["sources"]:
    name = pin["file"]
    path = args.alteration_packet if name == "WTCI-000182-P.PDF" else args.sources / name
    data = path.read_bytes()
    require(len(data) == pin["bytes"], name)
    require(hashlib.sha256(data).hexdigest() == pin["sha256"], f"{name} SHA-256")
    docs[name] = fitz.open(stream=data, filetype="pdf")
    require(len(docs[name]) == pin["pages"], f"{name} page count")


def page(name, number):
    return " ".join(docs[name + ".pdf"][number - 1].get_text().split()).lower()


anchors = [
    ("000172163", 1, "preliminary walk-through"),
    ("000172163", 1, "inergen discharge"),
    ("000172166", 1, "preliminary walk-through"),
    ("000172166", 2, "2-hour fire rated"),
    ("000172166", 2, "ul listed"),
    ("000172165", 1, "cat. cut for hatch"),
    ("000172168", 1, "cat. cut for hatch"),
    ("000172168", 2, "january 7, 2000"),
    ("000171497", 1, "existing frre rated hatch"),
    ("000171557", 1, "sign-off included"),
]
for name, number, value in anchors:
    require(value in page(name, number), f"{name} p. {number}: {value}")
print(f"8 PDF hashes, sizes and page counts, plus {len(anchors)} extracted text anchors passed")
