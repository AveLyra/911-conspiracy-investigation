#!/usr/bin/env python3
"""Classify named directory entries in a locally supplied 12-009 ZIP suffix."""
import argparse, hashlib, io, json
from collections import Counter
from pathlib import PurePosixPath, Path
from zipfile import ZipFile

EXPECTED_SHA256 = "a4d62dd226e97a30fa097f861d6491ef84e34451bd4a06f4f6c6e3759de3ca53"
BASE = "NIST_WTC7_FOIA_12-009/"
GROUPS = {
    "detail_1": BASE + "NIST_WTC7_FOIA_12-009_WTC7_Details_1/Detail Sheets 1",
    "detail_2": BASE + "NIST_WTC7_FOIA_12-009_WTC7_Details_2/Detail Sheets 2/7WTC - D2",
    "erection_tif": BASE + "NIST_WTC7_FOIA_12-009_WTC7_E_Sheets/E Sheets/7WTC - E1",
    "erection_pdf": BASE + "NIST_WTC7_FOIA_12-009_WTC7_E_Sheets/E Sheets",
}
parser = argparse.ArgumentParser()
parser.add_argument("suffix", type=Path, help="previously preserved 524288-byte ZIP tail")
args = parser.parse_args()
body = args.suffix.read_bytes()
digest = hashlib.sha256(body).hexdigest()
if digest != EXPECTED_SHA256:
    raise SystemExit("Source suffix hash does not match the pinned observation")
with ZipFile(io.BytesIO(body)) as archive:
    entries = archive.infolist()
files = [entry for entry in entries if not entry.is_dir()]
dirs = [entry for entry in entries if entry.is_dir()]
rows = {}
for key, directory in GROUPS.items():
    matched = [entry for entry in files if str(PurePosixPath(entry.filename).parent) == directory]
    rows[key] = {
        "directory": directory,
        "entries": len(matched),
        "extensions": dict(sorted(Counter(PurePosixPath(e.filename).suffix.lower() for e in matched).items())),
        "unique_full_paths": len({e.filename for e in matched}),
    }
expected = {"detail_1": (1248, ".tif"), "detail_2": (1275, ".tif"),
            "erection_tif": (42, ".tif"), "erection_pdf": (22, ".pdf")}
for key, (count, ext) in expected.items():
    assert rows[key]["entries"] == count
    assert rows[key]["extensions"] == {ext: count}
    assert rows[key]["unique_full_paths"] == count
assert len(entries) == 2597 and len(dirs) == 9 and len(files) == 2588
unmatched = [e for e in files if str(PurePosixPath(e.filename).parent) not in GROUPS.values()]
assert len(unmatched) == 1 and PurePosixPath(unmatched[0].filename).suffix.lower() == ".png"
assert 1248 + 1275 == 2523 and 42 + 2523 == 2565 and 22 + 42 + 2523 == 2587
print(json.dumps({"suffix_sha256": digest, "total_entries": len(entries),
                  "directories": len(dirs), "file_entries": len(files),
                  "groups": rows, "other_png": len(unmatched)}, indent=2))
