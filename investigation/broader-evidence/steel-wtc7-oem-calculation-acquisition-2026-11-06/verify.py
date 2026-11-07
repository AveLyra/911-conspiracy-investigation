"""Verify the OEM source pin, bounded ZIP filename screen and arithmetic."""
import argparse
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import re
import struct

import fitz


def require(condition, label):
    if not condition:
        raise SystemExit(f"Check failed: {label}")


def read_pin(path, pin, length):
    data = path.read_bytes()
    require(len(data) == length, path.name)
    require(hashlib.sha256(data).hexdigest() == pin["sha256"], f"{path.name} SHA-256")
    return data


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("pdf", type=Path)
parser.add_argument("source_directory", type=Path)
args = parser.parse_args()
ledger = json.loads(Path(__file__).with_name("SOURCE-PINS.json").read_text())
pin = ledger["pdf"]
data = read_pin(args.pdf, pin, pin["bytes"])
with fitz.open(stream=data, filetype="pdf") as pdf:
    require(len(pdf) == pin["pages"], "182-P physical page count")

pin = ledger["metadata"]
metadata = json.loads(read_pin(args.source_directory / pin["file"], pin, pin["bytes"]))
archive_sizes = {entry["name"]: int(entry["size"]) for entry in metadata["files"] if entry.get("size")}
pattern = re.compile(ledger["filename_pattern"], re.IGNORECASE)
total_entries = 0
for pin in ledger["directories"]:
    label = pin["archive_name"]
    require(archive_sizes[label] == pin["total"] == pin["last"] + 1, label)
    data = read_pin(args.source_directory / pin["file"], pin, pin["total"] - pin["first"])
    end = len(data) - 22
    eocd = struct.unpack_from("<4s4H2LH", data, end)
    require(eocd[0] == b"PK\x05\x06" and eocd[-1] == 0, f"{label} directory footer")
    require(eocd[1:5] == (0, 0, pin["count"], pin["count"]), f"{label} disk and entry counts")
    index = eocd[-2] - pin["first"]
    require(index >= 0 and index + eocd[-3] == end, f"{label} complete directory")
    found = 0
    while index < end:
        fields = struct.unpack_from("<4s6H3L5H2L", data, index)
        require(fields[0] == b"PK\x01\x02", f"{label} entry header")
        raw = data[index + 46:index + 46 + fields[10]]
        name = raw.decode("utf-8" if fields[3] & 2048 else "cp437")
        require(not pattern.search(name), f"{label} unexpected candidate filename")
        index += 46 + sum(fields[10:13])
        found += 1
    require(index == end and found == pin["count"], f"{label} directory read")
    total_entries += found

d = Decimal
require((d(80) / (42 * 2)).quantize(d("0.01")) == d("0.95"), "p. 86 notch expression")
require((d("0.85") * d("3.5") * 6 * 24).quantize(d(1)) == 428, "p. 87 bearing expression")
require(d(500) * 10 / 2 / 1000 == d("2.5"), "p. 42 post reaction")
require(d(25) * d("18.2") / 2 == d("227.5"), "p. 17 unrounded conduit reaction")
print(f"182-P pin and page count, metadata pin, six ZIP directories ({total_entries} entries, zero matches), and four arithmetic checks passed")
