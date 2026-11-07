#!/usr/bin/env python3
"""Check preservation and ledger consistency; do not authenticate historical claims.
Run with Python and pypdf installed. Source and media inputs are not downloaded.
"""
from pathlib import Path
import argparse, hashlib, json, re
import pypdf

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument("--pins", type=Path, default=Path(__file__).with_name("SOURCE-PINS.json"))
ap.add_argument("--source-root", type=Path, required=True, help="Directory containing the three original acquired PDFs")
ap.add_argument("--predecessor-root", type=Path, help="Optional native research root for six prior-file preservation checks")
ap.add_argument("--media-root", type=Path, help="Optional verified render directory; resolve its location through media_path.py first")
args = ap.parse_args()
pins = json.loads(args.pins.read_text())
checks = {}
def require(ok, label):
    if not ok:
        raise AssertionError(label)
def check_file(path, item, label):
    data = path.read_bytes()
    require(len(data) == item["bytes"], label + " byte length")
    require(hashlib.sha256(data).hexdigest() == item["sha256"], label + " SHA-256")
    return data

sources = {s["file"]: s for s in pins["sources"]}
require(set(sources) == {"chronology-part1.pdf", "chronology-part2.pdf", "gonsalves-mfr.pdf"}, "source set")
extracted = {}
for name, item in sources.items():
    data = check_file(args.source_root / name, item, name)
    require(data.startswith(b"%PDF-"), name + " PDF signature")
    require(item["url"].startswith("https://www.archives.gov/files/declassification/iscap/pdf/"), "official URL")
    require(item["status"] == 200, name + " recorded acquisition status")
    reader = pypdf.PdfReader(args.source_root / name)
    require(len(reader.pages) == item["physical_pages"], name + " physical page count")
    extracted[name] = [page.extract_text() or "" for page in reader.pages]
checks["source_entities_and_page_counts"] = len(sources)

ledger = pins["manual_footer_ledger"]
require(len(ledger) == 40, "40 manually read footers")
expected_pages = [("chronology-part1.pdf", i) for i in range(1, 19)] + [("chronology-part2.pdf", i) for i in range(1, 23)]
require([(r["source"], r["physical_page"]) for r in ledger] == expected_pages, "physical-page coverage/order")
require([r["manual_NCT"] for r in ledger] == [f"NCT{n:07d}" for n in range(10874, 10914)], "manual NCT coverage/order")
require([r["manual_NCTA"] for r in ledger] == [f"NCTA{n:09d}" for n in range(162726, 162766)], "manual NCTA coverage/order")
for i, row in enumerate(ledger):
    require(row["manual_footer_date"] == ("5/22/2003" if i < 38 else "5/29/2003"), "manual footer-date ledger")
    text = extracted[row["source"]][row["physical_page"] - 1]
    # Word-bounded strict expressions reproduce the preserved hits; do not normalize source text.
    require(re.findall(r"\bNCT(\d{7})\b", text) == row["raw_strict_NCT_hits"], "raw NCT extraction " + str(i))
    require(re.findall(r"\bNCTA(\d{9})\b", text) == row["raw_strict_NCTA_hits"], "raw NCTA extraction " + str(i))
checks["manual_ledger_rows_consistent"] = len(ledger)
checks["strict_extraction_nonempty_pages"] = {
    "NCT": sum(bool(r["raw_strict_NCT_hits"]) for r in ledger),
    "NCTA": sum(bool(r["raw_strict_NCTA_hits"]) for r in ledger),
}
require(checks["strict_extraction_nonempty_pages"]["NCT"] == pins["identifier_counts"]["NCT_nonempty_strict_extraction_pages"], "NCT extraction count")
require(checks["strict_extraction_nonempty_pages"]["NCTA"] == pins["identifier_counts"]["NCTA_nonempty_strict_extraction_pages"], "NCTA extraction count")
require(pins["full_pages_read"] == {"chronology-part1.pdf": [1], "chronology-part2.pdf": [18,19,20,21,22], "gonsalves-mfr.pdf": [1,2]}, "declared substantive reading scope")
require(len(pins["observations"]) == 6 and len({o["id"] for o in pins["observations"]}) == 6, "observation identifiers")
checks["reading_scope_and_observation_ids"] = "consistent; not independently validated"

if args.predecessor_root:
    for item in pins["protected_predecessors"]:
        check_file(args.predecessor_root / item["relative_to_research_root"], item, "predecessor")
    checks["predecessor_files_unchanged"] = len(pins["protected_predecessors"])
else:
    checks["predecessor_files_unchanged"] = "NOT TESTED; root not supplied"
if args.media_root:
    for item in pins["rendered_images"] + pins["footer_composites"]:
        check_file(args.media_root / item["file"], item, "render")
    checks["render_entities_preserved"] = len(pins["rendered_images"]) + len(pins["footer_composites"])
else:
    checks["render_entities_preserved"] = "NOT TESTED; verified media root not supplied"
print(json.dumps({"status": "PASS", "pypdf": pypdf.__version__, "checks": checks,
    "limits": "Checks acquired bytes, extraction and declared ledger consistency only. Does not independently read handwriting or authenticate events, missing recordings, clock alignment, completeness, disposition, intent or conspiracy."}, indent=2))
