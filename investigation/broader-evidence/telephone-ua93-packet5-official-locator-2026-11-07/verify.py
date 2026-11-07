#!/usr/bin/env python3
"""Verify the public metadata/index observations only; never opens the packet body."""
from pathlib import Path
import argparse
import hashlib
import json
import re

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument("--catalog-capture", type=Path, required=True, help="Preserved official public catalog accessibility snapshot")
ap.add_argument("--zip-index", type=Path, required=True, help="Previously parsed public ZIP central-directory JSON")
ap.add_argument("--research-root", type=Path, help="Optional native root for predecessor preservation checks")
args = ap.parse_args()
pins = json.loads(Path(__file__).with_name("SOURCE-PINS.json").read_text())
def require(ok, message):
    if not ok:
        raise AssertionError(message)
def check_file(path, size, digest, label):
    data = path.read_bytes()
    require(len(data) == size, label + " bytes")
    require(hashlib.sha256(data).hexdigest() == digest, label + " SHA-256")
    return data

cat = pins["official_catalog"]
ax = check_file(args.catalog_capture,cat["capture_bytes"],cat["capture_sha256"],"catalog capture").decode()
for literal in ["NAID: 2608311","DOJ documents re requests #35-13: Packet #5",
    "Access: Possibly Restricted","Use: Possibly Restricted",
    "Paper (Container ID: 12)","/id/2555805","Not Yet Available Online"]:
    require(literal in ax, "captured metadata anchor: " + literal)
index = pins["zip_index"]
raw = check_file(args.zip_index,index["derived_index_bytes"],index["derived_index_sha256"],"held ZIP index")
rows = json.loads(raw)
require(len(rows) == index["indexed_entries"], "indexed path count")
exts = set(index["native_extensions"])
native = [r for r in rows if Path(r["path"]).suffix.lower() in exts]
named = [r for r in rows if re.search(index["workbook_name_pattern"],Path(r["path"]).name)]
packet = [r for r in rows if "T7 B12" in r["path"] and "404" in Path(r["path"]).name and "35-13" in r["path"]]
require(len(native) == index["native_extension_hits"], "declared extension screen")
require(len(named) == index["workbook_name_hits"], "workbook filename screen")
require(packet == index["packet5_candidates"], "exact catalog candidate selection")
checks = {"official_catalog_capture":"PASS","metadata_anchors":7,
    "indexed_paths":len(rows),"native_extension_hits":len(native),
    "workbook_name_hits":len(named),"candidate_PDF_entries":len(packet)}
if args.research_root:
    for item in pins["protected_predecessors"]:
        check_file(args.research_root / item["relative_to_research_root"],
            item["bytes"],item["sha256"],"predecessor")
    checks["predecessors_unchanged"] = len(pins["protected_predecessors"])
else:
    checks["predecessors_unchanged"] = "NOT TESTED: no native root supplied"
print(json.dumps({"status":"PASS","checks":checks,
    "limits":"Public catalog representation and declared filenames only. Does not open or authenticate the packet body, establish its release/reproduction status, identify a caller, validate native carrier values, prove complete holdings or complete a missing-original criterion."},indent=2))
