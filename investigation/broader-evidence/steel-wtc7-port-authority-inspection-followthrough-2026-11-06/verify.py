"""Verify the five held PDF copies and cited NIST text anchors with PyMuPDF."""
import argparse
import hashlib
import json
from pathlib import Path

import fitz


def require(condition, message):
    if not condition:
        raise SystemExit(message)


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("sources", type=Path)
args = parser.parse_args()
ledger = json.loads(Path(__file__).with_name("SOURCE-PINS.json").read_text())
anchors = {
    "ncstar1-1.pdf": {
        238: ["each item was initialed as the corrections were verified"],
        241: ["700 gpm", "Intergen suppression system"],
    },
    "ncstar1-1j.pdf": {
        57: ["W98-7134", "94-7176"],
        58: ["700 gph", "LO-203", "walls and curbs for leakage"],
        59: ["M4.01"],
    },
}
total_anchors = 0
for pin in ledger["sources"]:
    name = pin["file"]
    data = (args.sources / name).read_bytes()
    require(len(data) == pin["bytes"], f"{name}: size differs")
    require(hashlib.sha256(data).hexdigest() == pin["sha256"], f"{name}: SHA-256 differs")
    with fitz.open(stream=data, filetype="pdf") as doc:
        require(len(doc) == pin["pages"], f"{name}: page count differs")
        for page, values in anchors.get(name, {}).items():
            value = " ".join(doc[page - 1].get_text().split())
            value = value.replace("W98-7 1 34", "W98-7134")
            for anchor in values:
                require(anchor in value, f"{name} p. {page}: missing {anchor}")
                total_anchors += 1

print(f"{len(ledger['sources'])} PDF hashes, sizes and page counts plus {total_anchors} NIST text anchors passed")
